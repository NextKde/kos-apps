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

The exact consolidated source 03c92edd0b0c9f54013ba8c63ee1e591482eb928 completed
all three new-ID KDE 6.11 app/Sources exports in
[SDK run 41945820505](https://github.com/NextKde/kos-apps/actions/runs/41945820505).
Both native push and PR validation also succeeded at that revision. These exports
are unsigned candidates, not accepted production bundles. Separate candidate
import/signing is being validated; genuine publisher signatures including retained
Sources/provenance, source/license review and signed stable Release remain pending.
Core 3079b238e43ffa68ecbca90676ba39c63af245c1 embeds the reviewed Flathub runtime-only
URL/primary policy and passed its hosted gates. Users still configure their own
runtime source; no consumer remote is added. Source upload, SDK exports and green
native CI are not an installable signed release.

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
[run 41947645841](https://github.com/NextKde/NextKde/actions/runs/41947645841),
including 17/17 data/platform, 58/58 logic, 27/27 headless and 2/2 widget tests;
both Nix configurations passed run 41947645918. This is not live VM acceptance.
No real new-ID installation, data migration, graphical session, signing-workflow
dispatch, consumer remote setup or stable Release publication was performed.

See flatpak/README.md and INSTALLATION.md for contracts and manual acceptance.
