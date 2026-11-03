# Source provenance

Initial standalone export: 2026-11-03, version 0.1.0.

Upstream repository: https://github.com/NextKde/NextKde

Pinned upstream commit: `fe00a434b9d873d82c7ccbf51ef3aedb38db88f0`.
The export was made from the local working source at that commit. Unrelated
working changes (GTK/settings/KWin/packaging) are excluded.

Included source closure:

* `apps/weather`: Weather C++/QML, icon, desktop metadata, shaders and particle
  assets. No unrelated app sources or test harnesses.
* `apps/common`: shared application lifecycle, preferences, localization and
  headers; translation source inputs narrowed to Weather and exported UI modules.
* `shared/qml`: files listed by its CMake QML module, including the lazily loaded
  optional compositor-control resource; no shell, wallpaper, colorize or test tree.
* `shared/demo-ui`: files listed by its CMake QML module and retained
  `upstream-sha256.json` recording the canonical `nextkdeAppDemo` source asset hashes.
* `shared/i18n/SystemLanguage.h`, `cmake/KosApplication.cmake`, upstream `LICENSE`.
* `backend/weather.go`: original `services/data-service/weather.go` Weather
  provider/state/cache implementation, reformatted only by gofmt.
* `backend/protocol.go` and `backend/subscriptions.go`: adapted from the pinned
  data-service's version-1 protocol/connection serialization, with all non-weather
  operations and desktop notifications removed. No metrics/activity/desktop code,
  third-party Go modules, or shared data-service launcher/unit is included.

Standalone additions/adaptations: independent root CMake, weather-only stdlib Go
entry point and persistence, app-owned helper lifecycle, private backend paths,
explicit immutable core/backend choice, application ID `org.nextkde.Weather`,
metainfo, independent CI/build instructions and installer integration metadata.
Executable, desktop filename and existing app preferences remain compatible.

All source/assets are local pinned copies. Go is built with `GOTOOLCHAIN=local`,
`GOPROXY=off`, `GOSUMDB=off`, `-mod=readonly`; there are no runtime module/toolchain
fetches, FetchContent, submodules, or mutable dependency downloads. Qt/KF/C++/Go
build/runtime dependencies are distribution-provided and not vendored.

No Git repository was initialized or published as part of the export. Public
publication and the release/installer engine are managed by the coordinating task.
