# Calendar Flatpak readiness — preparation, not runtime acceptance

Implemented locally (2026-11-04): opt-in org.nextkde.Calendar desktop/activation
identity, org.nextkde.Calendar.Pim client/server/activation file, private remapped
storage ignoring host KOS_PIM_STORAGE_DIR, bus ownership and storage lock before
PimStore construction, sandbox-only reminder activation, Background portal
permission/autostart request with refusal/partial/timeout messages, pinned
ECM/libical/KCalendarCore manifest, bundle helper and artifact-only workflow.
Native Calendar and PIM compile successfully. Sandbox identity compilation with
host libraries and an actual KDE 6.11 SDK build/export have both succeeded. An
unsigned development bundle was produced; none of this is sandbox acceptance.
Tasks stay integrated; no standalone Todo app is restored.

See [the packaging guide](flatpak/README.md) for permissions and behavior.
Outstanding: signed release helper execution including Sources/provenance artifacts;
desktop portal/service lifecycle and notification/relogin acceptance; full-profile
migration UI; optional host shell widget bridge. No native profile is automatically shared or migrated. The new lock
cannot protect against older non-cooperating native writers; sandbox storage stays
separate. iCalendar import is not full-fidelity profile migration.

No real service, data migration, application install, Release, graphical session
or automated test was operated for this preparation. Dedicated publisher signing
resources have been provisioned locally, but no signed release artifacts were
produced. Runtime trust provisioning and manual acceptance remain prerequisites.
