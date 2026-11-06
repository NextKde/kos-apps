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
are retired, distinct applications. Breaking change is intentional: no in-place
rename, source ownership adoption, old profile readback or migration. Settings
only manages the new IDs. Explicit legacy cleanup (program AND personal data) is
provided by NextKde core's tools/purge-legacy-apps.py, preview-only by default;
unproven system/core ownership stays with its original manager. See
[boundaries and cleanup](packaging/ProfileMigration.md).

Native source program/state roots and Qt preferences now use org.nextks.<app>.
Native Calendar data is $XDG_DATA_HOME/org.nextks.calendar/pim; native and sandbox
PIM both use org.nextks.calendar.Pim. Sandbox storage stays private and ignores
inherited host storage overrides. Native Weather uses its own org.nextks.weather
state/runtime namespace; both builds ignore KOS_DATA_SOCKET and only use the
bundled helper. Background reminders require the desktop Background portal's
permission. Existing ICS exchange is optional, not full-profile migration: it
does not package metadata or images. Old development migration journals are
neither read nor finalized. Current-ID updates and normal uninstalls retain
current-ID data; this is unrelated to old-to-new migration.
Identity-bound read-only widget summaries are implemented; see
[the widget contract](packaging/WidgetIntegration.md). They do not synchronize
profiles or transfer reminders. Do not run competing native PIM writers against
the same storage.

The three temporary per-app GitHub repositories were deleted on 2026-11-05
with maintainer approval in favor of this repository. Their Git ancestry and
original notices are retained here. See
`SOURCE_PROVENANCE.md`, `LICENSE` and retained third-party/shader notices. No real profiles, credentials or machine settings
belong in this repository. Runtime lifecycle, portal and update/uninstall behavior
remain subject to manual acceptance using disposable profiles.
