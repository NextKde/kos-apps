# Calendar GitHub Flatpak bundles (development preparation)

No signed binary Release has been published. Host compilation is not a KDE SDK
build or sandbox acceptance. Use `org.nextkde.Calendar.json` as the development
manifest; it pins ECM, libical and KCalendarCore sources and disables tests.

## Identity and ownership

`KOS_FLATPAK_BUILD=ON` selects desktop/application ID `org.nextkde.Calendar` and
PIM bus name `org.nextkde.Calendar.Pim`. The wire interface remains
`org.nextkde.Kos.Pim1`; the native service name is never used by the sandbox client.
The activation file has the sandbox name and invokes `/app/bin/kos-pim-service`.
No host systemd unit is installed. Native defaults are unchanged.

The service acquires its bus name and `service.lock` before loading the store.
The lock covers independent buses running this new service, not older native
binaries. Flatpak remaps data home; sandbox builds ignore `KOS_PIM_STORAGE_DIR`.
Calendar, metadata, images and widget snapshot remain in private
`$XDG_DATA_HOME/kos/pim`. No broad host filesystem or global bus permission is requested.
KDE 6.11 nevertheless inherits read-only xdg-config/kdeglobals and talk access to
com.canonical.AppMenu.Registrar, org.kde.kconfig.notify and org.kde.KGlobalSettings;
these are visible in the final exported metadata.
Network access supports holiday subscriptions. Notifications require a narrowly
scoped `org.freedesktop.Notifications` permission. File dialogs use the portal.

## Reminders

The independently activated PIM process may outlive the window. In the actions
menu, **Enable background reminders…** requests Background portal permission and
login autostart of `/app/bin/kos-pim-service`. No permission is assumed: denial,
partial approval and timeout have separate messages. The desktop may revoke this
permission or stop background apps. Logout stops the service when its bus goes
away; a granted autostart resumes it at next login. Missed reminders are governed
by the existing catch-up window, not a claim of guaranteed offline delivery.
Notification clicks target `org.nextkde.Calendar` or the fixed sibling application
inside `/app`; inherited host executable overrides are ignored.

## Data import and shell integration

No silent native migration is performed. iCalendar import/export is available,
but **does not constitute a full-fidelity profile migration** (organization,
images, source configuration and delivery history need separate handling).
For a full profile move, both owning services must be stopped, the complete
calendar/metadata/images set backed up together, and a copy imported into private
Flatpak storage with explicit user consent. A supported full-profile migration
UI is not implemented. Keep the original profile until manual acceptance.
Host shell widgets still read the native profile; this package does not silently
bridge sandbox data into host files or promise shared widgets.

## Preparing an artifact

`prepare-bundle.py` requires a clean reviewed commit, preinstalled KDE 6.11 SDK
and runtime, flatpak-builder, and a separately provisioned signing home. It creates
only build/signing artifacts under `tmp/`; it never installs or publishes apps.
The manual artifact-only CI workflow uses the protected `flatpak-signing`
environment. Key/secrets provisioning and actual publication remain maintainer
operations. The reviewed public key must ship in core separately.

Each invocation signs one architecture. Combining architectures requires a new
merged manifest/signature. Bundles contain no online origin/runtime-repo URL.
Runtime distribution remains a separate configured trust requirement.

## Manual acceptance remaining

In isolated HOME/XDG and a private bus: events/tasks/images, holiday networking,
portal import/export, duplicate-name and shared-directory lock refusal, window
close/background denial/approval/relogin, notification activation, uninstall data
retention and external-manager state synchronization. Do not use real profiles.
On 2026-11-04, the authorized KDE 6.11 SDK build completed for the pinned
dependencies, Calendar and PIM service. AppStream composition, local OSTree export
and unsigned development bundle export completed. The local-dir development source
is not an immutable signed release. No application/service was launched or installed;
portal behavior, signatures and Flatpak transactions remain unverified.


## Source artifacts and provenance

The release helper now passes `--bundle-sources` to flatpak-builder and exports
`APP_ID.Sources-VERSION-ARCH.flatpak` as a separately signed runtime bundle. This
is source delivery, not an application dependency: Settings does not install it.
Keep and publish it alongside the application, not just a GitHub source URL.
Builder-managed module sources include declared dependency inputs and patches;
the exact app Git archive and relocated patch inputs are retained separately.

`build-info.json` records user-level SDK/runtime refs and commits, tool versions,
and the Sources ref/commit. The helper rejects SDK/runtime commit changes during
construction. Provision these dependencies in the isolated **user** installation.
`flatpak-metadata.ini` and `runtime-files.txt` retain final permissions and file
inventory. `SHA256SUMS` recursively binds all retained artifacts, including nested
patches, and has its own detached publisher signature. Preserve the complete
artifacts directory and its relative paths when distributing or reviewing it.
The helper also prepares `APP_ID-VERSION-ARCH-release-materials.tar.gz` and a direct
detached signature, preserving that complete tree for GitHub's flat asset UI.
The archive contains the earlier checksums/signature, not itself; validate its
own signature before extracting. Publish the archive/signature alongside the
client-facing app bundle, `flatpak-release.json`/`.sig`, `app-release.json` and
Sources bundle. Do not upload only the runtime app and discard source material.

`app-release.json` is generated by the existing source-release preparer, fetching
and hashing GitHub's exact codeload archive for the same revision. This preserves
legacy `releases/latest` compatibility; its hash is not substituted with the local
`git archive` hash (the bytes can differ). The fixed source revision must already
be publicly available. Failure to prepare source metadata fails artifact preparation.

These are release-preparation code changes, not a completed signed helper run.
The Sources bundle does not supply the external SDK/runtime's corresponding
sources, prove relinkability or approve aggregate licensing. Maintainers still
must inspect the exported source contents, linked component configuration,
applicable licenses/notices and provider source-delivery obligations. Validate
`SHA256SUMS.sig` using an independently trusted publisher key before checking
hashes. Do not install the Sources bundle into a personal profile for inspection.
