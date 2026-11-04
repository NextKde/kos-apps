# KOS Apps readiness — preparation, not runtime acceptance

As of 2026-11-04, the local monorepo contains Calendar, Calculator and Weather
under apps/org.nextks.<app>, one shared implementation and VERSION=0.2.0.
Each application has a selectable CMake build and its own Flatpak manifest,
desktop/AppStream identity, bundle and app-prefixed release manifest. ListenFree
and KMusic remain separate.

Host native compilation and isolated tmp/ staging succeeded for all three apps,
including Calendar's PIM service and Weather's Go helper. Calculator stages only
its own executable/desktop/icon/metainfo; Weather adds only its own backend;
Calendar adds only its PIM helper and native activation service. No application
or automated test was run. These host builds do not validate sandbox behavior.

Previous independent org.nextkde.* checkouts completed KDE 6.11 SDK builds and
unsigned development bundles. That historical evidence does NOT validate the
new org.nextks.* identities or the consolidated source. The renamed SDK build,
signed helper execution including Sources/provenance, reviewed immutable remote
source and signed stable Release remain outstanding. The new remote repository
has not been created or pushed. Local signing resources exist, but no package
was signed; runtime trust provisioning remains incomplete.

Calendar retains scoped sandbox PIM/private storage, pre-store ownership locking
and Background portal request/refusal/partial/timeout handling. Portal, closing,
relogin, reminder activation and notifications need manual acceptance. The lock
cannot protect against old non-cooperating native writers. Full-profile migration
and a host-widget bridge are not implemented; iCalendar import is not equivalent.
Weather backend lifecycle, source/update/uninstall behavior, identity conflicts,
network failures and cancellation likewise need manual acceptance with disposable
profiles. Normal removal preserves data/shared runtimes and never migrates or
removes retired org.nextkde.* refs automatically.

See flatpak/README.md and INSTALLATION.md for contracts and manual acceptance.
No real installation, data migration, graphical session, workflow dispatch,
consumer remote setup or Release publication was performed for this consolidation.
