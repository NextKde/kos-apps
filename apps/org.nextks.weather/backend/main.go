// The standalone Weather helper owns only Weather state, never shell telemetry.
package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"path/filepath"
	"sync"
	"syscall"
	"time"
)

type State struct {
	Weather WeatherState `json:"weather"`
}
type Service struct {
	mu                      sync.Mutex
	persistMu               sync.Mutex
	subscribersMu           sync.Mutex
	subscribers             map[*subscriberConn]struct{}
	state                   State
	statePath, snapshotPath string
	weatherProvider         WeatherProvider
	weatherRequestSerial    uint64
	weatherCache            map[string]cachedWeather
	weatherFailStreak       int
}

func (s *Service) persist() {
	s.persistMu.Lock()
	defer s.persistMu.Unlock()
	s.mu.Lock()
	raw, err := json.Marshal(s.state)
	s.mu.Unlock()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return
	}
	for _, path := range []string{s.statePath, s.snapshotPath} {
		if err = os.WriteFile(path+".tmp", raw, 0600); err == nil {
			err = os.Rename(path+".tmp", path)
		}
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
	}
}

func run() error {
	// No KOS_DATA_* inputs: even an accidental direct launch cannot own core paths.
	socket := flag.String("socket", "", "private app socket")
	stateDir := flag.String("state-dir", "", "private weather state directory")
	flag.Parse()
	if *socket == "" || *stateDir == "" || filepath.Base(*socket) != "weather.sock" || filepath.Base(*stateDir) != "standalone-backend" {
		return errors.New("explicit private weather.sock and standalone-backend state directory are required")
	}
	if err := os.MkdirAll(filepath.Dir(*socket), 0700); err != nil {
		return err
	}
	if err := os.MkdirAll(*stateDir, 0700); err != nil {
		return err
	}
	lock, err := os.OpenFile(*socket+".lock", os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		return err
	}
	defer lock.Close()
	if err = syscall.Flock(int(lock.Fd()), syscall.LOCK_EX|syscall.LOCK_NB); err != nil {
		return fmt.Errorf("private helper is already active: %w", err)
	}
	s := &Service{state: State{Weather: defaultWeatherState()}, statePath: filepath.Join(*stateDir, "state.json"), snapshotPath: filepath.Join(*stateDir, "snapshot.json"), weatherProvider: newOpenMeteoProvider(), subscribers: map[*subscriberConn]struct{}{}}
	if raw, err := os.ReadFile(s.statePath); err == nil {
		var saved State
		if err = json.Unmarshal(raw, &saved); err != nil {
			return fmt.Errorf("invalid private weather state (file preserved): %w", err)
		}
		if saved.Weather.SchemaVersion != weatherSchemaVersion || saved.Weather.Provider != weatherProviderName || saved.Weather.Locations == nil {
			return errors.New("unsupported private weather state (file preserved); no legacy conversion is available")
		}
		s.state = saved
	} else if !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("read private weather state: %w", err)
	}
	normalizeWeatherState(&s.state.Weather)
	s.persist()
	// Parent owns stdin: EOF handles normal exit AND app crashes without a global service.
	stop := make(chan struct{})
	go func() {
		var b [1]byte
		for {
			if _, err := os.Stdin.Read(b[:]); err != nil {
				close(stop)
				return
			}
		}
	}()
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGTERM, syscall.SIGINT)
	defer signal.Stop(signals)
	failure := make(chan error, 1)
	go func() { failure <- serve(s, *socket) }()
	defer os.Remove(*socket)
	s.startWeatherRefresh(false)
	tick := time.NewTicker(10 * time.Second)
	defer tick.Stop()
	for {
		select {
		case <-stop:
			s.persist()
			return nil
		case <-signals:
			s.persist()
			return nil
		case err := <-failure:
			if !errors.Is(err, net.ErrClosed) {
				return err
			}
			return nil
		case <-tick.C:
			s.startWeatherRefresh(false)
		}
	}
}
func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
