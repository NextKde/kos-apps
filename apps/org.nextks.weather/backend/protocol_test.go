package main

import (
	"bufio"
	"encoding/json"
	"net"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"
)

func TestWeatherOnlyProtocol(t *testing.T) {
	root := t.TempDir()
	s := &Service{statePath: filepath.Join(root, "state.json"), snapshotPath: filepath.Join(root, "snapshot.json"), subscribers: map[*subscriberConn]struct{}{}, weatherProvider: newOpenMeteoProvider()}
	s.state.Weather = defaultWeatherState()
	s.persist()
	raw, err := os.ReadFile(s.snapshotPath)
	if err != nil {
		t.Fatal(err)
	}
	var state map[string]json.RawMessage
	if err = json.Unmarshal(raw, &state); err != nil {
		t.Fatal(err)
	}
	if len(state) != 1 || state["weather"] == nil {
		t.Fatalf("private state contains non-weather data: %s", raw)
	}
	for _, op := range []string{"metrics.snapshot", "activity.snapshot", "activity.active-app", "desktop.snapshot", "desktop.refresh", "desktop.place"} {
		response := s.handleRequest(DataRequest{Version: 1, RequestID: op, Operation: op})
		if response.OK || response.Error == nil || response.Error.Code != "unknown-operation" {
			t.Fatalf("non-weather operation accepted: %s %+v", op, response)
		}
	}
	for _, request := range []DataRequest{
		{Version: 8, Operation: "weather.snapshot"},
		{Version: 1, Operation: "weather.set-units", Payload: map[string]interface{}{"units": "invalid"}},
		{Version: 1, Operation: "weather.remove-location", Payload: map[string]interface{}{"id": ""}},
		{Version: 1, Operation: "weather.set-location", Payload: map[string]interface{}{"location": map[string]interface{}{"name": "invalid", "latitude": 200}}},
	} {
		if s.handleRequest(request).OK {
			t.Fatalf("invalid request accepted: %+v", request)
		}
	}
	response := s.handleRequest(DataRequest{Version: 1, RequestID: "snapshot", Operation: "weather.snapshot"})
	if !response.OK || response.RequestID != "snapshot" {
		t.Fatalf("snapshot: %+v", response)
	}
	id := s.state.Weather.Location.ID
	response = s.handleRequest(DataRequest{Version: 1, Operation: "weather.remove-location", Payload: map[string]interface{}{"id": id}})
	if !response.OK || len(s.state.Weather.Locations) != 0 {
		t.Fatalf("remove city: %+v", response)
	}
}

func TestSerializedWeatherSubscribers(t *testing.T) {
	s := &Service{subscribers: map[*subscriberConn]struct{}{}}
	const clients = 3
	const events = 12
	var wg sync.WaitGroup
	for i := 0; i < clients; i++ {
		server, client := net.Pipe()
		conn := &subscriberConn{Conn: server}
		defer conn.Close()
		defer client.Close()
		wg.Add(1)
		go func() {
			defer wg.Done()
			_ = client.SetReadDeadline(time.Now().Add(5 * time.Second))
			scanner := bufio.NewScanner(client)
			for n := 0; n < events+1; n++ {
				if !scanner.Scan() {
					t.Errorf("subscriber truncated: %v", scanner.Err())
					return
				}
				var item map[string]interface{}
				if err := json.Unmarshal(scanner.Bytes(), &item); err != nil {
					t.Error(err)
					return
				}
				if item["event"] != "weather.changed" {
					t.Errorf("wrong event: %s", scanner.Bytes())
					return
				}
			}
		}()
		s.subscribeWeather(conn)
	}
	var writers sync.WaitGroup
	for n := 0; n < events; n++ {
		writers.Add(1)
		go func() { defer writers.Done(); s.publishWeather() }()
	}
	writers.Wait()
	wg.Wait()
	if len(s.subscribers) != clients {
		t.Fatalf("lost subscribers: %d", len(s.subscribers))
	}
}
