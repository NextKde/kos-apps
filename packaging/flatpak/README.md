# Signed Flatpak bundles — release preparation, not published

Calculator is prepared for GitHub Release `.flatpak` assets, not a hosted NextKde
app repository and not a Flathub submission. The source installer is unchanged.
An unsigned local development bundle has been exported; no signed release, key
or CI secret has been provisioned/published by this work.

## Identity and permissions

- App/desktop/icon/AppStream ID and sandbox activation: `org.nextkde.Calculator`.
- Desktop Exec remains `kos-calculator`; Flatpak rewrites the exported launcher.
- Native builds retain their existing identity/data paths.
- KDE Platform/Sdk `6.11`; review its support window before a real release.
- Manifest permissions: IPC, Wayland, fallback X11 and GPU, with no network,
  broad session-bus access or host-spawn. KDE 6.11 additionally inherits read-only
  xdg-config/kdeglobals and talk permissions for com.canonical.AppMenu.Registrar,
  org.kde.kconfig.notify and org.kde.KGlobalSettings; inspect final metadata.
- Private Flatpak data is `~/.var/app/org.nextkde.Calculator`. No automatic native
  history/preferences migration is claimed.

The checked-in JSON is a **development** local-dir manifest. The release helper
replaces that source with the exact reviewed clean checkout commit from the fixed
GitHub repository and records an explicit AppStream release date. Packaging
changes must first be committed/reviewed and available at that immutable revision;
the helper refuses dirty source trees. No source or revision is published for you.

## Prepare artifacts manually

Provision `flatpak-builder`, `flatpak`, `ostree`, Python 3 and GnuPG, plus the KDE
SDK/runtime, in a separate build environment. Independently provision a signing
home and reviewed full primary fingerprint. Never send a private key in chat,
commit it, or distribute it in artifacts. The helper does not generate/import keys
or add remotes. An unattended build needs a dedicated signing key usable without
an interactive passphrase prompt (or separately managed signing integration).

```sh
python3 packaging/flatpak/prepare-bundle.py \
  --output tmp/flatpak-release \
  --gpg-homedir /private/signing-home \
  --fingerprint FULL_UPPERCASE_PRIMARY_FINGERPRINT \
  --release-date YYYY-MM-DD
```

This can take many minutes: it fetches the immutable source, builds with
`BUILD_TESTING=OFF`, signs the exported OSTree commit, exports a full bundle with
**no repo-url/runtime-repo**, computes size/SHA256, generates schema-1
`flatpak-release.json` and signs its original bytes with SHA256. It never runs
tests, launches the app, installs it or publishes anything. It only prepares one
architecture (default x86_64); missing architectures remain explicitly unavailable.
Do not merge architecture manifests without regenerating/re-signing the complete
manifest. Build intermediates and artifacts remain below `tmp/`.

`tmp/flatpak-release/artifacts/` contains the bundle, signed manifest, detached
signature and source-pinned build manifest. The local OSTree export is only a
build intermediate; no server is required for it. Review artifacts/permissions,
version, identity, AppStream metadata and actual launch behavior manually in an
isolated user environment before delivery. On 2026-11-04, an authorized isolated
KDE 6.11 SDK build, AppStream composition, local OSTree export and unsigned
development bundle export completed. This used the local-dir development manifest,
not a clean immutable release revision. The bundle was not installed or launched;
signing resources, a signed release and manual runtime acceptance remain pending.
An unsigned development bundle cannot be used by the verified Settings install path.

## CI preparation, separately authorized publication

`.github/workflows/flatpak-artifacts.yml` is manual and artifact-only. It does not
depend on the existing test jobs, does not create GitHub Releases, and has only
contents:read. It installs build runtime dependencies in the disposable CI user's
Flatpak installation; those remotes are not added on consumers' systems.

A maintainer must separately configure a protected `flatpak-signing` environment,
required reviewers, `FLATPAK_SIGNING_KEY` secret and
`FLATPAK_SIGNING_FINGERPRINT` variable. Restrict dispatch to reviewed workflow/source
revisions: application build scripts run in the signing job and must be trusted.
The disposable signing home is removed before artifact upload; only artifacts/
is uploaded. No secret configuration or workflow execution occurred here.

After manual review, create a **new** stable `vX.Y.Z` Release matching VERSION and
attach the bundle, `flatpak-release.json` and `.sig`. Do not rewrite published
source tags/assets. Keep `app-release.json` source compatibility. Ship the reviewed
binary public key and full primary fingerprint separately in an audited core
release; a key beside the bundle is not a trust anchor.

## Installation and management

Settings/`kos-apps` verifies the signed manifest, bundle hash/identity/commit and
publisher-signed OSTree commit using its own trusted public key. Runtime sources
are separately approved/configured. It never automatically adds an online app or
runtime source. Libflatpak can create a URL-less local bundle origin/key record,
even before a cancelled/refused deployment; no complete rollback is claimed.

The shared CLI supports status/check-update/install/update/uninstall with
`--app calculator`. For manual installation, first independently verify the signed
manifest and bundle size/hash/ref/commit, then supply the trusted key explicitly:

```sh
flatpak --user install --gpg-file=/trusted/publisher.gpg ./application.flatpak
flatpak --user uninstall org.nextkde.Calculator
```

Never use `--no-gpg-verify`. Ordinary uninstall omits `--delete-data` and retains
personal data. Flatpak tools operate on the same ref; Settings discovers GitHub
bundle updates. Do not promise that Discover or `flatpak update` can discover
GitHub bundle updates when there is no online app origin.


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
