# KOS Apps readiness — source validation, not signed runtime acceptance

As of 2026-11-05, the public [NextKde/kos-apps](https://github.com/NextKde/kos-apps)
repository contains Calendar, Calculator and Weather under apps/org.nextks.<app>,
one shared implementation and VERSION=0.2.0. Each application has a selectable
CMake build and its own Flatpak manifest, desktop/AppStream identity, bundle and
app-prefixed release manifest. ListenFree and KMusic remain separate. The three
obsolete single-app GitHub repositories were deleted with maintainer approval;
their source ancestry and notices are retained here.

## Current breaking boundary (2026-11-05)

The working-tree boundary supersedes native compatibility and cross-identity
ownership upgrades below. Old and new apps are separate: native Qt preferences,
source installation roots, Calendar storage/service and Weather state/socket use
new identities. No old-data readback or migration is required. Settings only
manages current IDs. Explicit old-program/data deletion belongs to core's separate
purge-legacy-apps.py, not normal install/update/uninstall. See ProfileMigration.md.
All hosted/runtime results below describe their named earlier revisions, not
these uncommitted changes. Production compilation is recorded separately in the
core task report. A subsequent explicitly authorized VM-only disposable purge
fixture run passed 27 cases after real Flatpak output exposed and prompted a fix
for abbreviated list commits. Only fake old data was deleted; no real applications
were uninstalled. Current-source Flatpak lifecycle preparation is now authorized
in a separate isolated VM profile; KDE Platform 6.11 was imported with signature
verification, while SDK provisioning and app builds/launches remain pending.
See ProfileMigrationAcceptance.md for exact scope and evidence. Human acceptance
and publication remain outstanding.

## Measured hosted validation (historical)

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
access is not yet accepted. Under the current boundary old development profiles
are not read or finalized. Identity-bound read-only widget summaries are implemented; new-ID sandbox
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
uninstall, Plasma recovery and reinstall have not been performed. Subsequent
runtime-ready isolated profiles completed genuine signed install/current-version
check/network-failure/uninstall cycles for all three apps through the production
backend and a process-local HTTPS fixture, not actual published Latest. Offscreen
sandbox smoke launches exited zero; optional QML warnings remain, so this is not
interactive desktop acceptance. External Flatpak removal/refresh/reinstall passed
for Calculator and Weather before transaction supervision, and Calendar afterward.
Core now supervises mutations in a bounded companion process because an observed
upstream runtime-summary request omitted cancellation propagation. Four affected
VM regressions pass (14.34s); subsequent Calendar and Calculator lifecycle runs
cancelled during transaction waits and reconciled empty inventory/busy=false,
not successful final installs. These core changes are committed as
c35eabfc8f2da41141a0f3a371e46d47b47af002; its exact hosted Tests
41974741788 (all nine jobs) and Nix 41974741789 (both configurations) subsequently
completed successfully. Calculator also passed a complete two-version signed
metadata-fixture lifecycle through production discovery/download, supervised
install/update, current-version checks and uninstall, with data/runtime retention.
These were separate user operations with standard runtime-cache warmup between
deployments, not one uninterrupted cold-cache run. Both fixture versions retain
the same executable source revision; historical executable/data-schema upgrade,
live Settings, portal, notification and interactive widget acceptance remain open.
Actual Calendar service mutations reached the production core widget reader via
app-published sandbox summaries; removal preserved data but hid the summary.
Weather published a real summary, correctly classified as missing without a
current reading, and left no sandbox backend process after normal window exit.
A matching upstream-fixed CLI installed only in the temporary prefix allowed all
three unmodified desktop Exec commands to start with added isolated offscreen and
app-owned screenshot arguments and exit normally. This does not validate actual
desktop clicking, single-instance activation or repair the system CLI. A longer
application-owned window also fetched real online weather and published a ready
summary; the current reading matched the production widget payload. Supervised
removal preserved data and runtime. The three signed bundles also launched and
exited normally in the VM's real Wayland session with nonempty app-owned
screenshots and no remaining sandbox processes. Visual inspection shows actual
Calculator/Weather content. Calendar's forced software-backend capture was black,
but removing that override rendered correctly; with the isolated activation bus,
the native-rendered Calendar also visibly recovered the retained synthetic event.
Real signed Calendar/Weather deployments plus an owned synthetic native launcher
also produce ambiguous/no widget payload; supervised Flatpak removal preserves
the launcher and sandbox data, and native-only lookup does not consume sandbox
summaries. This is not two running applications, user/system duplicates, click,
portal, notification, single-instance or live Settings acceptance. Calculator's source route separately passed real native-artifact
installation, repeat/current checks, cleanup preview and offline removal with data
retention, using retained verified codeload transport and a persistent CMake
source/build-path fixture. A separate fresh-profile run then completed unchanged
cold configure/build/install in about134 seconds, launched the actual installed
executable, and passed repeat/current/cleanup/offline-removal checks with data
retention. Only retained verified transport replaces the unpublished release; no
build artifacts or CMake paths are reused. Earlier short diagnostic cancellation
remains incomplete. Calendar/Weather separately completed unchanged cold source
build/install in fresh profiles (about247/206 seconds), repeat/current/cleanup/prune
and offline removal with data-sentinel retention and owned-state cleanup. These two
runs did not launch applications or validate business data. Shared verified archive
transport does not mean reused builds, unprovisioned-OS or published Latest acceptance.
A separate genuine Calculator source lifecycle installed
historical0.1.0/9432b21d with its original installer, updated using the current
installer to0.2.0/ee0175f4, and removed both owned program revisions offline. Both
revisions were freshly built and actually launched, binary hashes differ, retired
ownership/launcher handed over to org.nextks.calculator, and the original data
sentinel survived. Retained verified archives replace unpublished release transport;
this is not historical Flatpak upgrade or actual history/preferences compatibility
across identities. Calendar also completed genuine native source0.1.0/ce8b36b5
(original installer) to0.2.0/ee0175f4 (current installer), with fresh builds,
different binary hashes, new ownership and removal of old managed Todo activation
links. Actual old PIM service created an event/todo on a private bus in isolated
storage, then exited normally; the actual new service read identical rows without
changing calendar.ics/metadata.json hashes. Repeat/current checks and offline
removal passed, removing both owned program revisions/activation state while
preserving the real PIM files. Historical archive comes from the exact retained
consolidated Git commit, not original deleted-repository release bytes. This is
native compatibility for these records, not historical Flatpak migration, all PIM
data shapes, GUI or desktop activation acceptance. Weather also passed genuine
native source0.1.0/de8f9769 (original installer) to0.2.0/ee0175f4 (current installer),
fresh application builds with different executable hashes, retired ownership/desktop
handover, repeat/current checks and offline removal of both owned revisions.
Installed old helper saved selected city, two-city list and imperial units; installed
new helper read identical preference fields from the same isolated native state path.
Go helper hashes are identical; no changed helper schema inferred. Forecast requests
were deliberately blocked and transient status/timestamps changed file hashes on
restart. Uninstall retained real state/snapshot files with exact pre-uninstall
hashes. A subsequent fresh source reinstall after removal completed196.76s without
changing retained real data files. Reinstalled helper read identical old preference
fields; second offline removal cleaned owned program/activation state and retained
state/snapshot files with exact pre-removal hashes. This does not cover Weather GUI
or historical Flatpak migration. No automatic
profile migration, consumer remote setup, signing-workflow dispatch, PR merge or
stable Release publication was performed.

See flatpak/README.md and INSTALLATION.md for contracts and manual acceptance.
