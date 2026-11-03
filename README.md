# KOS Weather

Standalone Weather application from NextKde. Version **0.1.0**, application ID
`org.nextkde.Weather`, executable and desktop entry `kos-weather` /
`kos-weather.desktop`. No NextKde checkout, shell, KWin plugin, telemetry daemon,
or global service is required.

## Build and install

Requirements: Linux, CMake >=3.25, C++20 compiler, Go >=1.22, Qt >=6.8 with Core,
DBus, Gui, Network, Qml, Quick, QuickControls2 and LinguistTools. KF6WindowSystem
is optional (desktop activation/effects integration). Qt Quick Effects, Layouts,
Controls and QtCore QML runtime modules must be installed. System dependencies
come from your distribution; the build never downloads dependencies or Go toolchains.
All QML, shader sources and compiled QSB assets are included at pinned provenance.

Arch Linux:

```sh
sudo pacman -S --needed base-devel cmake ninja go qt6-base qt6-declarative qt6-tools qt6-wayland
```

Ubuntu 26.04 (Qt 6.8 or newer is required; Ubuntu 24.04's default Qt 6.4 is too old):

```sh
sudo apt install build-essential cmake ninja-build golang-go qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-tools-dev-tools qt6-l10n-tools qt6-wayland qml6-module-qtquick qml6-module-qtquick-controls qml6-module-qtquick-layouts qml6-module-qtquick-effects qml6-module-qtquick-window qml6-module-qtqml-workerscript qml6-module-qtcore
```

Use a dedicated version prefix, not the NextKde installation prefix:

```sh
cmake -S . -B build -DBUILD_TESTING=OFF -DCMAKE_INSTALL_PREFIX="$HOME/.local/opt/kos-weather/0.1.0"
cmake --build build --parallel 4
cmake --install build
"$HOME/.local/opt/kos-weather/0.1.0/bin/kos-weather"
```

The universal per-user installer entry point is `install.sh` (installer packaging
is integrated separately). Its public repository is https://github.com/NextKde/kos-weather.
Do not install this app over an existing core-managed `kos-weather` desktop/binary;
use the universal installer's explicit ownership/conflict handling.

## Backend ownership and integration

Selection is fixed when the Weather client is constructed:

* **Standalone default:** launches the sibling `bin/kos-weather-backend` from the
  app's own immutable version prefix (the local CMake build artifact is a development
  fallback). This is a weather-only Go helper using the original Open-Meteo provider,
  cache, refresh/backoff, city-list and v1 weather API code. There is no telemetry,
  active-app tracking, desktop indexing, core binary, or systemd unit.
* Private runtime files: `$XDG_RUNTIME_DIR/kos-weather-<uid>/weather.sock` and
  `weather.sock.lock` (private uid-specific `/tmp` fallback). Private persistent
  state and offline snapshot: `$XDG_STATE_HOME/quickshell/kos-weather/standalone-backend/`.
  The helper's stdin pipe belongs to the app; EOF also terminates it after an app
  crash. Normal app shutdown waits briefly, then terminates only its own child.
  Failed launches/errors go to the app's stderr; they are not discarded.
* **Explicit core integration:** start with `KOS_DATA_SOCKET=/path/to/kos-data.sock`.
  The installed NextKde service must already support version-1 `weather.snapshot`,
  `weather.search`, `weather.refresh`, `weather.set-location`,
  `weather.remove-location`, `weather.set-units` and `weather.changed` notifications.
  The app neither launches nor stops that service. Core backend failure stays a
  visible core connection failure; it never silently starts a private replacement.
  Explicit custom sockets use socket snapshots only (no guessed core state file).

A socket filename or presence of a `kos-data-service` executable is **not** a
compatibility guarantee. Until core publishes a versioned compatibility marker,
automatic installed-core detection is intentionally unavailable: opt in with the
explicit environment variable. A restart is required to change backend ownership.
Existing Qt app preferences (`NextKde/KosApplications`) are retained. Private and
core city lists/cache are separate; there is no automatic migration or merge,
so selecting core shows the cities owned by core. Both versions share the desktop
entry and activation identity; simultaneous installs require ownership arbitration.

Forecast/geocoding/AQI require internet and Open-Meteo availability and policy
compliance. Provider failures retain cached conditions; AQI is best-effort. The
standalone app cannot update NextKde shell weather widgets unless explicitly
connected to the same compatible core backend. Optional compositor-specific
surface controls gracefully fall back on ordinary desktops; native NextKde
compositor integration is not bundled.

## Backend validation

Reusable weather-only protocol/concurrency checks (no downloaded Go modules):

```sh
mkdir -p tmp/go-tests
TMPDIR="$PWD/tmp/go-tests" GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go -C backend test -race -count=1 ./...
python3 tests/backend-lifecycle.py "$PWD/build/backend/kos-weather-backend"
```

The subprocess check covers private socket exclusivity, multiple clients and
notifications, EOF/owner-crash exit, private persistence, invalid path rejection,
and unchanged core sentinel files. Temporary fixtures stay under `tmp/`.

## Manual verification

Build/install into a private prefix. Launch normally and check initial forecast,
search, selecting/removing cities, units, offline cached content, window controls,
and translations. Close the app and check its private helper exits. Check that no
`kos-data-service` binary/unit or core `kos-data.sock` / core state file was installed
or changed. With an already-running compatible NextKde session, launch with explicit
`KOS_DATA_SOCKET` and check shared city changes; disconnect core and confirm the app
does not start a private helper mid-session. Final visual/desktop integration
acceptance is manual.

See [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
and [LICENSE](LICENSE).

## Independent stable releases

A maintainer publishes a reviewed `vX.Y.Z` tag matching `VERSION`. The application
workflow must build and validate successfully before its release job publishes
`app-release.json`. The manifest records the exact source commit and source
archive SHA-256. Settings checks this repository's latest stable GitHub Release
on **Check for updates**, then offers **Update**; users do not need a new NextKDE
release. Drafts and prereleases are not offered, and updates are never automatic.

The bundled installer is reviewed code, not a script fetched by a release check.
Publication permissions on this GitHub repository are the trust boundary; hashes
protect transfer integrity, not a compromised publisher. Never publish a release
for an unverified source commit. See `packaging/INSTALLATION.md` for CLI actions,
network error handling, offline removal, installation ownership and preserved data.
