# KOS Apps readiness — source validation, not signed runtime acceptance

As of 2026-11-05, the public [NextKde/kos-apps](https://github.com/NextKde/kos-apps)
repository contains Calendar, Calculator and Weather under apps/org.nextks.<app>,
one shared implementation and VERSION=0.2.0. Each application has a selectable
CMake build and its own Flatpak manifest, desktop/AppStream identity, bundle and
app-prefixed release manifest. ListenFree and KMusic remain separate. The three
obsolete single-app GitHub repositories were deleted with maintainer approval;
their source ancestry and notices are retained here.

## Measured hosted validation

[PR validation run 41941538122](https://github.com/NextKde/kos-apps/actions/runs/41941538122)
passed on source commit 76068d787af68a1d5f759146787c00e8a71a8d1c using Ubuntu 26.04:

- Calendar, Calculator and Weather each configured, compiled and installed into
  a disposable staging prefix with only the selected application enabled.
- The isolated source-installer suite passed all 52 tests, including the three
  consolidated application lifecycles, unchanged ListenFree identity, network
  errors, integrity checks, cancellation, ownership and interrupted cleanup.
- Calendar passed all 12 registered CTests, including PIM store, private-session
  D-Bus service/client regressions, shared preferences and language cases.
- Calculator passed all 10 registered CTests, including the QML calculation engine.
- Weather passed all 10 registered CTests, including its Go backend.

These counts include repeated shared tests across application jobs. They do not
mean that graphical acceptance, real Flatpak transactions or signed packages were
validated. The earlier installer fixture failure was corrected without changing
ListenFree's production identity. Host compilation recorded in earlier local
reports is historical evidence, not the current verification route; builds and
tests now run only in hosted CI or the dedicated VM.

## Outstanding signed-delivery gates

The exact consolidated source ee0175f4a6c2025a9c9ce5b6b8a6ba66e769cfba completed
all three new-ID KDE 6.11 app/Sources exports and candidate integrity checks in
[SDK run 41953958502](https://github.com/NextKde/kos-apps/actions/runs/41953958502).
[Native PR validation 41953958540](https://github.com/NextKde/kos-apps/actions/runs/41953958540)
and push validation 41953949348 passed: 64 Python cases (52 installer and 12
packaging), Calendar 12 CTests, Calculator 10 and Weather 10. Shared cases repeat
across application jobs. This revision retains Calendar's libical/KCalendarCore
license texts and application shader/Demo UI provenance; older ff5ed00 candidates
predate that correction and must not be published as final.

All three corrected SDK candidates have separately signed app/Sources bundles,
manifests, checksums and material archives prepared with the existing publisher
key. Weather's recovered archive SHA256 matches the hosted artifact digest. VM
verification passed signatures, retained hashes, exact source/version/ref/commit
and absence of embedded online origins/runtime URLs. No private key was uploaded.
Full source/license review and final accepted-source publication remain outstanding.

Core ffda70a2277e3aeca8bd19dd0ae276e3ab688488 passed
[Tests 41960909858](https://github.com/NextKde/NextKde/actions/runs/41960909858)
and [Nix 41960909783](https://github.com/NextKde/NextKde/actions/runs/41960909783).
It embeds the reviewed runtime-only Flathub policy and guards bundle cleanup in an
isolated bounded companion process before download. Unpatched libflatpak 1.16.6
mis-releases retained GBytes as a GObject; upstream fix
95b70b71e366c78d16abadaa7e33f6d6bcdc01f4 corrects that cleanup. The VM system
package remains unpatched: production install/update safely reports
FLATPAK_INCOMPATIBLE rather than exposing Settings to a crash. Users still configure
their own runtime source; no consumer remote is added.

With only a process-local upstream-corrected library in isolated VM profiles,
all three signed candidates installed offline with dependencies disabled; production
kos-apps verified their installed publisher signatures and exact commits, then
uninstalled them and preserved private-data SHA256 sentinels. Calendar/Calculator
also passed duplicate-install refusal and explicit same-bundle reinstall. Disabling
origin verification on the Calculator fixture revoked update eligibility without
blocking offline uninstall. These are not runtime, launch, true version-upgrade,
Settings GUI or stable Release acceptance.

Calendar retains scoped sandbox PIM/private storage, pre-store ownership locking
and Background portal request/refusal/partial/timeout handling. Portal, closing,
relogin, reminder activation and notifications need real desktop acceptance. The
lock cannot protect against old non-cooperating native writers. The unpublished
host profile copier and first-launch finalizer have been withdrawn. Existing ICS
exchange does not package metadata/images or hand over reminders; sandbox file
access is not yet accepted. Unfinished development markers block opening a partial
profile. Identity-bound read-only widget summaries are implemented; new-ID sandbox
access, source selection, stale/error display and exact app navigation still need
acceptance. No host filesystem permission was added. See WidgetIntegration.md,
ProfileMigration.md and ProfileMigrationAcceptance.md for compatibility limits.
Weather backend lifecycle, real install/update/uninstall behavior, identity
conflicts, network failures and cancellation likewise need acceptance with
disposable profiles. Normal removal preserves data/shared runtimes and never
migrates or removes retired org.nextkde.* refs automatically.

The dedicated VM is reachable again. Targeted kos-apps/kos-settings compilation,
three affected Settings CTests and 23 core deployment/source-release regressions
passed there; those local builds include unrelated working-tree changes and are
not clean exact-core desktop acceptance. Original-library pre-download rejection
and corrected-library normal cleanup were both exercised. Hosted checks above
validate the exact committed core source independently.

No verified hypervisor recovery point is available for the remote VMware desktop.
Per the approved safety boundary, historical core install/upgrade, whole-NextKde
uninstall, Plasma recovery and reinstall have not been performed. No runtimes or
apps were launched during the isolated transactions; live Settings, portal,
notification, widget and backend lifecycle acceptance remains open. No automatic
profile migration, consumer remote setup, signing-workflow dispatch, PR merge or
stable Release publication was performed.

See flatpak/README.md and INSTALLATION.md for contracts and manual acceptance.
