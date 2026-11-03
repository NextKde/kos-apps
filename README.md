# KOS Calendar

Standalone Calendar and Reminders for Linux, extracted from [NextKde](https://github.com/NextKde/NextKde). This repository builds without a NextKde checkout, Quickshell, Settings, or KWin plugins. License: GPL-3.0; see `LICENSE` and `SOURCE_PROVENANCE.md`. Application release version: `VERSION`.

Calendar includes day/week/month/year views, events, reminders, iCalendar import/export, and the compatible `kos-todo` launcher. The existing desktop IDs (`kos-calendar.desktop`, `kos-todo.desktop`), executables, preference/data paths, and PIM D-Bus identity `org.nextkde.Kos.Pim1` are preserved. The release catalog appId is `org.nextkde.Calendar`; it does not rename the existing desktop or D-Bus identities.

## Dependencies

CMake 3.21+, C++20 compiler, Qt 6.5+ (Core, DBus, Gui, Network, Qml, Quick, QuickControls2, QuickDialogs2, LinguistTools), KDE Frameworks 6 CalendarCore / libical. KF6 WindowSystem is optional (native window effects). QtTest is only required with `BUILD_TESTING=ON`.

Ubuntu 26.04 (24.04's standard Qt 6.4 is too old):

```sh
sudo apt install build-essential cmake ninja-build python3 pkg-config \
  qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-tools-dev-tools \
  qt6-l10n-tools qt6-declarative-dev-tools qt6-qpa-plugins libkf6calendarcore-dev \
  qml6-module-qtquick qml6-module-qtquick-controls qml6-module-qtquick-templates \
  qml6-module-qtquick-layouts qml6-module-qtquick-window qml6-module-qtquick-dialogs \
  qml6-module-qtquick-effects qml6-module-qtqml-workerscript qml6-module-qtcore
```

Arch Linux: `base-devel cmake ninja python qt6-base qt6-declarative qt6-tools kcalendarcore`; optional `kwindowsystem`. A normal Qt Wayland/X11 platform plugin is needed for interactive use. Tests additionally need QtTest/Qt Quick Test and `dbus-run-session` / `dbus-send` (Ubuntu: `qml6-module-qttest dbus`).

## Build and run

```sh
cmake -S . -B build -G Ninja -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$HOME/.local/share/kos-calendar-dev"
cmake --build build --parallel 2
cmake --install build
```

For a source-tree development run without changing real data:

```sh
mkdir -p tmp/dev/config tmp/dev/data tmp/dev/cache
export XDG_CONFIG_HOME="$PWD/tmp/dev/config" XDG_DATA_HOME="$PWD/tmp/dev/data"
export XDG_CACHE_HOME="$PWD/tmp/dev/cache" KOS_PIM_STORAGE_DIR="$PWD/tmp/dev/pim"
dbus-run-session -- sh -c './build/services/pim-service/kos-pim-service & service=$!; trap "kill $service" EXIT; ./build/apps/calendar/kos-calendar'
```

Use `kos-calendar --help` for entry points, including `--view` and `--item`; `kos-todo` forwards legacy reminder launches to Calendar. Do not launch a second PIM service on a session already owning `org.nextkde.Kos.Pim1`.

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

The wrapper delegates to the universal Python installer with `--app calendar`. It builds the standalone root with `BUILD_TESTING=OFF` into an immutable per-user version prefix. The generic engine owns desktop/activation links and conflict detection, not CMake. User data is not removed on uninstall. Stable `app-release.json` uses schemaVersion 1, appId `org.nextkde.Calendar`, version `0.1.0`, the published repository's 40-hex revision, and archiveSha256; publication supplies the actual revision/hash.

## Private runtime and activation

Kos.Ui, Kos.Demo, and Kos.Pim QML/resources are statically embedded in the app; nothing is installed over core Settings or global shared QML. All CMake installation paths stay under the configured prefix. Binaries: `bin/kos-calendar`, `bin/kos-todo`, `bin/kos-pim-service`. The installer exposes the first two on PATH; the PIM executable need not have a public link.

`share/dbus-1/services/org.nextkde.Kos.Pim1.service` defaults to direct D-Bus activation using the configured final prefix. Configure `KOS_PIM_SERVICE_EXECUTABLE` for a different activation executable, or `KOS_INSTALL_PIM_ACTIVATION=OFF` when an existing desktop installation already owns the service. Never overwrite a foreign activation file or running desktop service. `KOS_INSTALL_PIM_SYSTEMD_UNIT=ON` optionally installs a user unit and enables systemd delegation in the private activation file; the default is OFF, so the app never depends on an unmanaged systemd unit. CMake does not enable/start units.

Notification actions find sibling `kos-calendar` first, preserving relocation within a prefix; `KOS_CALENDAR_EXECUTABLE` can explicitly override the launch path. Desktop/D-Bus Exec entries bind the final configured prefix: reconfigure when relocating the installation, rather than moving generated activation files unchanged.

## App-local tests

Optional `BUILD_TESTING=ON` registers shared application preferences/language tests, Calendar version/QML smoke, PIM store/private-bus tests, and legacy unified activation. No unrelated desktop/sibling tests are registered. `.github/workflows/build.yml` compiles and runs these on Ubuntu with private data directories and D-Bus. Local test runs must likewise isolate `XDG_DATA_HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, and `KOS_PIM_STORAGE_DIR` under `tmp/` and use `dbus-run-session`.

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
