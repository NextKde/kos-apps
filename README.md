# KOS Apps

Calendar (including reminders), Calculator and Weather share one independent
source repository, `NextKde/kos-apps`, and one release version (`VERSION`). They do
not require a NextKde core checkout, Quickshell or KWin plugins. ListenFree and
KMusic are separate projects.

| Application | Source directory / application ID | Executable |
| --- | --- | --- |
| Calendar | `apps/org.nextks.calendar` / `org.nextks.calendar` | `kos-calendar` |
| Calculator | `apps/org.nextks.calculator` / `org.nextks.calculator` | `kos-calculator` |
| Weather | `apps/org.nextks.weather` / `org.nextks.weather` | `kos-weather` |

## Selective build

CMake 3.25+, C++20, Ninja and Qt 6.8+ Core/DBus/Gui/Network/Qml/Quick/
QuickControls2/LinguistTools are required. Calendar additionally needs Qt
QuickDialogs2 and KF6 CalendarCore/libical; Weather needs Go 1.22+. KF6 WindowSystem
is optional. A Calculator-only configuration does not require Go or CalendarCore.

```sh
cmake -S . -B tmp/build-calculator -G Ninja -DKOS_APPS=calculator \
  -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/tmp/stage-calculator"
cmake --build tmp/build-calculator --parallel 2
cmake --install tmp/build-calculator
```

Use `-DKOS_APPS=calendar` or `weather` for a single application, or
`'-DKOS_APPS=calendar;calculator;weather'` for a combined native build. Installation
contains only the selected applications and their required helpers. Shared Qt/QML
components are embedded, not installed over global modules.

## Installation and releases

The intended distribution is three independently installable signed Flatpak bundles
in one stable `vX.Y.Z` GitHub Release. See [packaging](packaging/flatpak/README.md).
Source is maintained at [NextKde/kos-apps](https://github.com/NextKde/kos-apps).
No renamed signed release is available yet. Existing old-ID development builds
do not validate these new IDs.

The explicit developer/source entry point selects exactly one application:
`./install.sh --app calculator install` (also status/check-update/update/uninstall).
It consumes the selected app's source manifest, not a replacement installer script.
No application data is deleted by normal uninstall.

## Compatibility and data

`org.nextkde.Calendar`, `org.nextkde.Calculator` and `org.nextkde.Weather` Flatpaks
are retired, distinct identities. There is no in-place Flatpak rename, automatic
uninstall, adoption or migration of their private data. Settings detects them;
no cross-identity profile import is provided. Exact-user-ref removal is a separate
confirmed operation that keeps data and does not install a replacement. Keep the
old installation until an acceptable replacement is ready. System/ambiguous refs
stay with their external manager. See [compatibility](packaging/ProfileMigration.md).

Native preference/data paths remain unchanged. Native Calendar retains the PIM
bus `org.nextkde.Kos.Pim1`; sandbox Calendar uses `org.nextks.calendar.Pim` and
private Flatpak storage, ignoring inherited host storage overrides. Background
reminders require the desktop Background portal's permission. Existing ICS exchange
is not a complete backup: it does not package metadata or image files, and sandbox
file access still needs manual acceptance. The unpublished copier/finalizer has
been withdrawn; unfinished development markers block opening a partial profile.
Identity-bound read-only widget summaries are implemented; see
[the widget contract](packaging/WidgetIntegration.md). They do not synchronize
profiles or transfer reminders. Do not run competing native PIM writers against
the same storage.

The three temporary per-app repositories are being retired in favor of this
repository. Their Git ancestry and original notices are retained here; their
original Release metadata/assets are backed up before deletion. See
`SOURCE_PROVENANCE.md`, `LICENSE` and retained third-party/shader notices. No real profiles, credentials or machine settings
belong in this repository. Runtime lifecycle, portal and update/uninstall behavior
remain subject to manual acceptance using disposable profiles.
