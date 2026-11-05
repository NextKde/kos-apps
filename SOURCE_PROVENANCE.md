# KOS Apps source provenance

Calendar, Calculator and Weather were consolidated on 2026-11-04 from reviewed
local checkouts of these repositories and exact branch tips:

| Source | Packaging commit | Imported tip (CI-skip successor) |
| --- | --- | --- |
| https://github.com/NextKde/kos-calendar | `87e29fcf8014d54668810274708280f449211a7f` | `6dc4ea4c372449f89ad78b859f06d1445ed0aaef` |
| https://github.com/NextKde/kos-calculator | `75d44cf9224e2f92aecc41b59137a967366481c3` | `d196f901285917d40e0c005e375d7c14b4a6b5cd` |
| https://github.com/NextKde/kos-weather | `974e619d366c43995e34cf8e2c8b0583c62c3e6c` | `3914dbdcb2a804a02c8a36451f67745db3811a78` |

Calendar history is the base. Merge `354f1a2aaf6e710e7986faba4f7a7531a4a5d8e8`
retains Calculator and Weather commit ancestry using an explicit history-only
ours merge; the subsequent consolidation commit imports their selected source
files into the mappings below. The merge alone is not a source content merge.
The original repository URLs above are historical provenance, not active download
endpoints. Those temporary GitHub repositories were deleted on 2026-11-05
with maintainer approval. Their commit ancestry remains part of this repository.

## Path mapping and shared sources

- Calendar `apps/calendar` → `apps/org.nextks.calendar`.
- Calculator `apps/calculator` → `apps/org.nextks.calculator`.
- Weather `apps/weather` → `apps/org.nextks.weather`; `backend` → that app's `backend`.
- Calendar `apps/common` → `shared/common`; translations now list all three apps.
- Shared QML, i18n, demo-ui, PIM and services use Calendar's complete copies.
  Shared QML implementation, i18n and CMake helper were compared across sources;
  differences included notice/README presence and optional test declarations.
  The shader NOTICE and demo-ui nested provenance are retained, not deduplicated away.
- Weather third-party notices are retained as `THIRD_PARTY_NOTICES.weather.md`.
- Original extraction records are retained in `SOURCE_PROVENANCE.kos-calendar.md`,
  `.kos-calculator.md` and `.kos-weather.md`. Those records describe historical
  paths/workflows, not current release claims.

The original source was extracted from NextKde/NextKde commit
`fe00a434b9d873d82c7ccbf51ef3aedb38db88f0`; the copied GPL-3.0 `LICENSE`,
source copyright and third-party/shader notices remain applicable. Qt/KDE and
Flatpak runtime/SDK are external dependencies with separate distribution duties.

## Consolidation changes

The root selects `KOS_APPS` and only required dependencies. One VERSION (0.2.0)
feeds target-scoped new desktop/AppStream/Flatpak identities `org.nextks.<app>`.
Commands, native preference/data paths and the native PIM wire/bus contract are
retained. Sandbox PIM and Weather socket paths use the new identity. No old
Flatpak data or ref is renamed or migrated. Calendar contains reminders; no
standalone Todo launcher is restored.

Packaging uses three pinned per-app manifests, one parameterized bundle helper,
app-prefixed Release attachments, retained Sources/build/license materials and
manual build/artifact workflows. The generic source installer selects one app
and recognizes only fixed retired ownership IDs for offline compatibility.
Automated regression coverage is being updated for the consolidated identities,
selective builds and installer lifecycle. CI enables BUILD_TESTING; developer
builds still default to BUILD_TESTING=OFF. Current build/release readiness and
actual validation results are recorded in packaging/FLATPAK-READINESS.md,
not inferred from historical records.

No private keys, credentials, real profiles or machine configuration are source
inputs. Source is published at https://github.com/NextKde/kos-apps; source upload
and CI execution do not constitute signed-package release publication.
