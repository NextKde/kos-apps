# Source provenance

Upstream repository: https://github.com/NextKde/NextKde

Upstream commit: `fe00a434b9d873d82c7ccbf51ef3aedb38db88f0`

Exported from the corresponding source paths in that working checkout. The application closure had no uncommitted upstream changes at extraction. The independent distribution is GPL-3.0 under the copied root `LICENSE`; all source copyright and shader notices are retained. `shared/demo-ui/upstream-sha256.json` (Calendar only) and `shared/qml/controls/shaders/NOTICE.md` retain nested material provenance. Qt and KDE Frameworks remain external system dependencies.

## Exported source paths

- `apps/common`
- `shared/i18n`
- `cmake/KosApplication.cmake`
- `shared/qml/CMakeLists.txt and only its listed QML/resources plus controls/shaders/NOTICE.md`
- `apps/calculator`

## Extraction changes

- CMakeLists.txt (new standalone root)
- VERSION (independent application version)
- apps/common/CMakeLists.txt (app-local translation sources and language test path)
- apps/common/tests/LanguageTest.cpp (moved from tests/localization/LanguageTest.cpp)
- install.sh (new generic installer entry point)
- README.md (new independent build/install documentation)
- .github/workflows/build.yml (new app-only Ubuntu build/tests)
- .gitignore (app-local build artifacts)
- apps/calculator/CMakeLists.txt (local optional engine test registration)
- apps/calculator/tests/tst_engine.qml (moved from tests/calculator/tst_engine.qml and relative imports adjusted)
- `SOURCE_PROVENANCE.md` (this record).

The generic `packaging/installer.py` is separately supplied from the upstream installer implementation during publication. Stable `app-release.json` is generated from the new repository revision and release archive hash, never copied from the desktop distribution. No user data, credentials, build outputs or machine configuration belong to this source export.
