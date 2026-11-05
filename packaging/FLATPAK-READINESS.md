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

The exact consolidated source ff5ed00f7d954d83c3e9621866f08153e372fd94 completed
all three new-ID KDE 6.11 app/Sources exports and retained-candidate integrity checks
in [SDK run 41951329778](https://github.com/NextKde/kos-apps/actions/runs/41951329778).
[Native PR validation 41951329916](https://github.com/NextKde/kos-apps/actions/runs/41951329916)
also passed: 63 Python cases (52 installer and 11 packaging), Calendar 12 CTests,
Calculator 10 and Weather 10. Shared cases repeat across application jobs.
Separately signed local app/Sources bundles, manifests, checksums and material
archives were prepared from those three candidates with the existing publisher
key; no private key was uploaded. They are not published or accepted final bundles.

Material inspection found Calendar's bundled libical/KCalendarCore libraries lacked
their license-text directories in the runtime inventory. The current packaging
retains those upstream texts/notices and installs application shader/Demo UI
provenance. Native staging and SDK inventory gates check their presence. The
ff5ed00 candidates predate this correction and must not be published as final;
a matched-source set must be rebuilt, checked and signed after the fix passes.
Full source/license review, final bundle/installed-commit verification, actual
transactions and desktop acceptance still remain, as does a signed stable Release.

Core d7075a1703967cce6613ff6f5c05264669eb389e embeds the reviewed Flathub runtime-only
URL/primary policy and passed its hosted gates, including genuine publisher
signature acceptance and tampering rejection through the production verifier.
That public fixture is not final-bundle verification. Users still configure their
own runtime source; no consumer remote is added. Source upload, SDK exports and
green native CI are not an installable signed release.

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

The dedicated VM remains inaccessible over SSH; no successful VM sync/build/
install/relogin/shot is recorded for this candidate. Core Settings/platform/widget
regressions and the runtime-only trust update passed all jobs in
[run 41950649175](https://github.com/NextKde/NextKde/actions/runs/41950649175),
including 17/17 data/platform, 58/58 logic, 27/27 headless and 2/2 widget tests;
both Nix configurations passed run 41950649198. This is not live VM acceptance.
No real new-ID installation, data migration, graphical session, signing-workflow
dispatch, consumer remote setup or stable Release publication was performed.

See flatpak/README.md and INSTALLATION.md for contracts and manual acceptance.
