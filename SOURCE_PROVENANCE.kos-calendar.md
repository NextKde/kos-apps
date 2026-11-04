# Calendar source provenance before consolidation

The following is the retained extraction record from Calendar commit
`6dc4ea4c372449f89ad78b859f06d1445ed0aaef` (its packaging parent is
`87e29fcf8014d54668810274708280f449211a7f`). Paths and release names below refer
to that historical checkout, not the current layout.

Upstream repository: https://github.com/NextKde/NextKde

Upstream commit: `fe00a434b9d873d82c7ccbf51ef3aedb38db88f0`

Exported from the corresponding source paths in that working checkout. The application closure had no uncommitted upstream changes at extraction. The independent distribution is GPL-3.0 under the copied root `LICENSE`; all source copyright and shader notices are retained. `shared/demo-ui/upstream-sha256.json` and `shared/qml/controls/shaders/NOTICE.md` retain nested material provenance. Qt and KDE Frameworks remain external system dependencies.

## Exported source paths

- `apps/common`
- `shared/i18n`
- `cmake/KosApplication.cmake`
- `shared/qml/CMakeLists.txt and only its listed QML/resources plus controls/shaders/NOTICE.md`
- `apps/calendar`
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
- Removed the legacy apps/todo launcher and its unified-activation review; tasks remain integrated in Calendar.
- apps/calendar/README.md, README.zh-CN.md, ITERATION_PLAN.zh-CN.md omitted (monorepo-only presets/docs references; replaced by root README)
- SOURCE_PROVENANCE.md (original record).

The generic packaging/installer.py was separately supplied from the upstream installer implementation during publication. Stable app-release.json was generated from the independent repository revision and release archive hash, never copied from the desktop distribution. No user data, credentials, build outputs or machine configuration belong to this source export.
