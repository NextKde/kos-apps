# Source provenance

Upstream repository: https://github.com/NextKde/NextKde

Upstream commit: `fe00a434b9d873d82c7ccbf51ef3aedb38db88f0`

Exported from the corresponding source paths in that working checkout. The application closure had no uncommitted upstream changes at extraction. The independent distribution is GPL-3.0 under the copied root `LICENSE`; all source copyright and shader notices are retained. `shared/demo-ui/upstream-sha256.json` (Calendar only) and `shared/qml/controls/shaders/NOTICE.md` retain nested material provenance. Qt and KDE Frameworks remain external system dependencies.

## Exported source paths

- `apps/common`
- `shared/i18n`
- `cmake/KosApplication.cmake`
- `shared/qml/CMakeLists.txt and only its listed QML/resources plus controls/shaders/NOTICE.md`
- `apps/calendar`
- `apps/todo/CMakeLists.txt, src/, data/kos-todo.desktop.in (legacy launcher only; obsolete Todo UI excluded)`
- `shared/demo-ui`
- `shared/pim`
- `services/pim-service`

## Extraction changes

- CMakeLists.txt (new standalone root)
- VERSION (independent application version)
- apps/common/CMakeLists.txt (app-local translation sources and language test path)
- apps/common/tests/LanguageTest.cpp (moved from tests/localization/LanguageTest.cpp)
- install.sh (new generic installer entry point)
- README.md (new independent build/install documentation)
- .github/workflows/build.yml (new app-only Ubuntu build/tests)
- .gitignore (app-local build artifacts)
- services/pim-service/CMakeLists.txt (configurable PIM activation; optional systemd ownership)
- services/pim-service/data/org.nextkde.Kos.Pim1.service.in (private executable/direct activation)
- services/pim-service/data/kos-pim-service.service.in (configurable executable)
- services/pim-service/src/PimStore.cpp (KOS_CALENDAR_EXECUTABLE override, sibling-first relocation)
- apps/calendar/tests/run-unified-activation-review.py (standalone default build directory and repo-local temporary isolation)
- apps/calendar/README.md, README.zh-CN.md, ITERATION_PLAN.zh-CN.md omitted (monorepo-only presets/docs references; replaced by root README)
- `SOURCE_PROVENANCE.md` (this record).

The generic `packaging/installer.py` is separately supplied from the upstream installer implementation during publication. Stable `app-release.json` is generated from the new repository revision and release archive hash, never copied from the desktop distribution. No user data, credentials, build outputs or machine configuration belong to this source export.
