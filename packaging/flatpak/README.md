# GitHub Flatpak bundles — unified source, separate applications

No renamed signed release is published. Three manifests build one selected app
each: `org.nextks.calendar.json`, `org.nextks.calculator.json`, and
`org.nextks.weather.json`. Calendar keeps dependency translations in its main
bundle (`separate-locales: false`), avoiding an undeployed Locale extension in
URL-less bundle installations. They use KDE Platform/Sdk 6.11 and preserve pinned
build dependencies, disabled tests and per-app permissions. A source-only or host
build is not SDK or sandbox acceptance.

## Preparation contract

`prepare-bundle.py --app calendar|calculator|weather` also requires `--output`
(new directory below checkout tmp/), `--gpg-homedir` (separately provisioned),
`--fingerprint` (full trusted primary), `--release-date YYYY-MM-DD` and optional
`--arch x86_64|aarch64`. It requires a clean reviewed commit available from the
fixed `https://github.com/NextKde/kos-apps.git` repository. It does not install or
publish applications, generate keys, add consumer remotes or configure secrets.
Run each app separately using the same repository commit and VERSION. Each
architecture invocation creates a separate manifest; combining architectures
requires deliberately merging and re-signing that app's manifest, not overwriting
one architecture's metadata with another's.

A single stable `vX.Y.Z` release contains app-ID-prefixed files:

- `<appId>-<version>-<arch>.flatpak`
- `<appId>.flatpak-release.json` and `.sig` (client-facing, schema 2 with an exact installation plan)
- `<appId>.app-release.json` (explicit source installer compatibility)
- `<appId>.Sources-<version>-<arch>.flatpak` (signed source runtime bundle)
- `<appId>-<revision>-source.tar.gz`
- `<appId>.build-manifest.json`, `.build-info.json`, `.flatpak-metadata.ini`,
  `.runtime-files.txt`, `.SHA256SUMS` and `.SHA256SUMS.sig`
- `<appId>-<version>-<arch>-release-materials.tar.gz` and `.sig`

The signed material archive preserves the complete retained tree, including
checksums/signature, but not itself. Every flat Release filename is app-specific.
Do not publish only the executable bundle. Source manifests hash GitHub codeload
bytes of the exact same commit, not a potentially different local archive.
SDK/runtime commits are recorded and changes during building are rejected.
Application metadata is signed as the original binary byte sequence, including
terminal newlines; never strip or normalize it. Before signing the release
manifest, the helper reopens the final bundle through libflatpak, compares its
metadata bytes and digest with the repository plan, and reads the installed size
from that same bundle. A mismatch stops artifact preparation. Both SDK candidate
and signed-artifact CI run `python3 packaging/flatpak/test_bundle_plan.py -v`
before provisioning build tools or signing material. These regressions cover
newlines/non-ASCII bytes and refusal of stripped metadata, wrong hashes and sizes.
If a release was signed with different metadata bytes, publish a corrected new
version after this gate passes; do not weaken the client's exact comparison.
Sources are retained before runtime cleanup, are not app dependencies, and are
not installed by Settings. They do not automatically satisfy external runtime/
SDK corresponding-source obligations or prove aggregate license compliance;
inspect actual source completeness, configuration, linking and notices manually.

`flatpak-sdk.yml` builds unsigned candidates on packaging pull requests or by
manual dispatch. It retains the app/Sources OSTree repository, pinned manifest,
SDK/runtime commits, and official build-remote metadata as CI artifacts. It has
no signing secrets and does not install apps or publish Releases. A PR build is
not a signed release, and its release date is only candidate metadata. Downloaded
remote keys are inspection evidence, not automatic core trust-policy updates.

For a separately reviewed successful CI candidate, extract its archive below this
checkout's `tmp/`, then pass `--candidate tmp/<candidate>` and `--revision <full SHA>`
to `prepare-bundle.py` with the normal signing/output/date arguments. This skips
SDK provisioning and compilation. The source commit must be an ancestor of the
clean helper checkout; VERSION and packaging are read at that exact commit.
The importer rejects manifest/date/permission changes, missing Sources or foreign
refs, malformed environment pins, symlinks and failed OSTree integrity checks.
It signs a private working copy, retaining the original unsigned input and SDK
evidence. These checks do not prove who built an arbitrary archive: verify the
CI run, exact source and downloaded artifact before authorizing signing. No key
is uploaded and no app is installed. Signing and artifact integrity do not replace
isolated transaction, sandbox, source/license or graphical acceptance.

The separate signed artifact workflow has one matrix job per app and a protected
signing environment. A usable signing subkey must be provisioned separately;
never commit a private key or infer trust from a public key beside a download.
No signing or workflow execution is authorized merely by editing these files.

## Identity and boundaries

Native and sandbox desktop/AppStream IDs use `org.nextks.<app>`, retaining the
`kos-<app>` command names. Native programs, preferences and data now use new-ID
namespaces too. Old org.nextkde.* applications are not adopted or migrated;
legacy cleanup is a separate explicit core script that deletes listed old data.
Normal current-ID Flatpak uninstall preserves private data and shared runtimes.

Calendar alone builds libical/KCalendarCore and its PIM service. Sandbox client,
service and activation use `org.nextks.calendar.Pim`, retaining the existing wire
interface. It ignores inherited host PIM storage/executable overrides and uses
private `$XDG_DATA_HOME/kos/pim`. Native PIM also uses `org.nextks.calendar.Pim`
and its default data is `$XDG_DATA_HOME/org.nextks.calendar/pim`; no old profile is
read. Explicit custom native profiles remain the caller's responsibility. Background
reminders require explicit desktop portal permission. Denial/partial/timeout
messages exist, but close/relogin/notification behavior needs manual acceptance.
iCalendar import is not full-profile migration. Identity-bound read-only host
widget summaries are implemented; see ../WidgetIntegration.md for their limited
scope and pending sandbox/runtime acceptance.

Weather runs its own Go helper, ignores inherited KOS_DATA_SOCKET in both builds,
and uses an app-ID-scoped runtime socket. Calculator needs neither Go nor PIM.
No broad host filesystem or unrestricted session bus access is added. Inspect
final permissions: KDE 6.11 runtime may inherit read-only kdeglobals and scoped
KDE/AppMenu talk permissions beyond finish-args. Runtime distribution requires
separately configured and approved sources; bundles contain no online app or
runtime repository URLs. Discover is not promised to discover GitHub updates.

## Manual acceptance still required

Use disposable HOME/XDG data and a private session bus: single-app installation,
menu launch, independent update/uninstall, external uninstall synchronization,
old/new ID conflict handling, network failure/cancellation/signature errors,
Calendar portal/PIM/background/notification lifecycle, and Weather backend exit.
Do not use personal profiles or equate compilation with runtime acceptance.
Old-ID unsigned SDK development bundles are historical evidence only. New-ID
SDK exports and separately signed local candidates exist; their exact revisions
and remaining gates are recorded in ../FLATPAK-READINESS.md. Neither signing nor
successful SDK compilation establishes end-to-end acceptance.

Calendar explicitly retains libical's license selection, full LICENSES directory,
third-party notices and contributors, and KCalendarCore's LICENSES and README under
`/app/share/licenses/`. These supplement the corresponding Sources bundle, not
replace it. Application shader and Demo UI provenance are installed under
`/app/share/doc/kos-apps/`. External KDE runtime/SDK redistribution and complete
source/relinking obligations remain a separate review; these notice copies are
not a blanket license-compliance certification.

## Cooperative KWin controls

The bundle includes `Kos.SurfaceShape` from NextKde/NextKde commit
`d7b34a8e8b37a9fb7605333f10d02f7b16e70743`, built against the shared
KDE 6.11 SDK. Its license is installed under `/app/share/licenses/kos-surface-shape`.
`QML_IMPORT_PATH` exposes the module inside the sandbox. Window control slots
reserve actual button geometry; client controls disappear only after KWin
acknowledges takeover. Desktops without this protocol retain working controls.
Release acceptance must exercise the actual bundle under a cooperating Wayland
compositor; an X11 smoke test alone does not establish decoration ownership.
