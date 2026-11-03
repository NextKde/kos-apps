# KOS Calculator

Standalone Qt Quick calculator for Linux, extracted from [NextKde](https://github.com/NextKde/NextKde). No NextKde checkout, Quickshell, Settings, PIM daemon or KWin plugin is required. License: GPL-3.0; see `LICENSE` and `SOURCE_PROVENANCE.md`. Independent release version: `VERSION`.

Includes basic/scientific calculation, history, memory, and unit conversion. Existing executable `kos-calculator`, desktop ID `kos-calculator.desktop`, application identity and settings/history data paths are preserved. The release catalog appId `org.nextkde.Calculator` does not rename desktop/D-Bus identities.

## Dependencies

CMake 3.21+, C++20 compiler, Qt 6.5+ Core/DBus/Gui/Qml/Quick/QuickControls2/LinguistTools. Optional KF6 WindowSystem enables native window effects. QtTest and Qt Quick Test are only needed with `BUILD_TESTING=ON`.

Ubuntu 26.04 (24.04's standard Qt 6.4 is too old):

```sh
sudo apt install build-essential cmake ninja-build python3 pkg-config \
  qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-tools-dev-tools \
  qt6-l10n-tools qt6-declarative-dev-tools qt6-qpa-plugins \
  qml6-module-qtquick qml6-module-qtquick-controls qml6-module-qtquick-templates \
  qml6-module-qtquick-layouts qml6-module-qtquick-window qml6-module-qtquick-effects \
  qml6-module-qtqml-workerscript qml6-module-qtcore
```

Arch Linux: `base-devel cmake ninja python qt6-base qt6-declarative qt6-tools`; optional `kwindowsystem`. A Qt Wayland/X11 platform plugin is needed for interactive use. Tests additionally use `qml6-module-qttest dbus` on Ubuntu.

## Build and use

```sh
cmake -S . -B build -G Ninja -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$HOME/.local/share/kos-calculator-dev"
cmake --build build --parallel 2
cmake --install build
"$HOME/.local/share/kos-calculator-dev/bin/kos-calculator"
```

For isolated development, set `XDG_DATA_HOME`, `XDG_CONFIG_HOME`, and `XDG_CACHE_HOME` to directories under this repository's `tmp/` and run via `dbus-run-session`. `kos-calculator --help` lists supported switches. History/preferences otherwise retain their existing user data locations.

## Stable user installer

Once the published release includes `packaging/installer.py`:

```sh
./install.sh check
./install.sh check-update
./install.sh install
./install.sh update
./install.sh status
./install.sh uninstall
```

The wrapper delegates to the universal Python installer with `--app calculator`. The engine builds this standalone CMake root with `BUILD_TESTING=OFF` into an immutable per-user version prefix and owns desktop/binary links. Uninstall preserves user data. Stable `app-release.json` uses schemaVersion 1, appId `org.nextkde.Calculator`, version `0.1.0`, the published repository's 40-hex revision, and archiveSha256; publication supplies the actual revision/hash.

## Private installation

Installs `bin/kos-calculator`, `share/applications/kos-calculator.desktop`, its icon, metadata and license under the configured prefix. Kos.Ui QML and shader resources are statically embedded: this app does not overwrite Settings, the desktop's shared QML, or any PIM service. Desktop Exec entries use the final configured prefix; reconfigure instead of moving generated entries unchanged.

## App-local tests and CI

`BUILD_TESTING=ON` registers application preferences/language tests, Calculator version/QML smoke, and the local calculator engine/conversion suite when qmltestrunner is available. No Calendar, Weather, shell or Settings tests are registered. `.github/workflows/build.yml` builds/tests on Ubuntu with private XDG directories and a private session bus. Local test runs must likewise isolate data under `tmp/` and use `dbus-run-session`.

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
