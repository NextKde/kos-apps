# Weather Flatpak bundle preparation (not published)

Distribution uses signed `.flatpak` GitHub Release assets, not a hosted NextKde
app repository or a Flathub submission. No public signing key, secret, bundle or
Release has been provisioned by this work. Source installation remains separate.

## Sandbox contract

- App/desktop/icon/AppStream/single-instance ID: `org.nextkde.Weather`.
- KDE Platform/Sdk 6.11; review runtime support before publication.
- IPC, Wayland, fallback X11, GPU and network permissions only. Weather forecasts
  and place searches require outbound HTTPS. Flatpak network permission is not
  restricted to individual hosts; no narrower network-isolation claim is made.
- No broad host/home filesystem, host runtime socket or broad session-bus permission.
  KDE 6.11 inherits read-only xdg-config/kdeglobals and talk access to
  com.canonical.AppMenu.Registrar, org.kde.kconfig.notify and org.kde.KGlobalSettings;
  inspect final exported metadata rather than only the manifest.
- The app includes and starts its own `kos-weather-backend` from the same prefix.
  A Flatpak build ignores `KOS_DATA_SOCKET`; it never selects the desktop's global
  data service even when that variable is inherited.
- Helper socket is under `$XDG_RUNTIME_DIR/app/org.nextkde.Weather/backend/` to
  avoid the native helper path even when network/IPC namespaces are shared.
- Existing private state paths resolve inside the Flatpak's XDG directories,
  below `~/.var/app/org.nextkde.Weather/`. No automatic migration from native
  saved locations/cache is performed. Ordinary uninstall preserves this data.
- Forecast/provider attribution and service usage limits remain applicable; see
  `THIRD_PARTY_NOTICES.md`. A sandbox does not grant new API usage rights.

## Build inputs

The checked-in manifest is for local development (`dir` source). The release
helper replaces only the final application module with a fixed-repository full
Git commit and requires a clean, reviewed checkout. Source and packaging changes
must be committed and available at that revision before an actual release build.
VERSION is the single application/AppStream/release version source.

The Go toolchain is pinned to 1.27.3 for x86_64/aarch64 using upstream HTTPS
archives and SHA256 values retrieved from `https://go.dev/dl/?mode=json` during
preparation. No third-party Go modules are used. The toolchain is build-only and
removed by cleanup; its LICENSE/PATENTS are retained under `/app/share/licenses/go`
for the linked standard-library code. Qt/runtime redistribution obligations remain
separate. Builds set GOTOOLCHAIN=local, GOPROXY=off, GOSUMDB=off and CGO_ENABLED=0;
CMake must not silently download another compiler or Go module.

## Artifact preparation

Provision flatpak-builder, Flatpak, OSTree, Python and GnuPG plus the KDE SDK/runtime
in an isolated build environment. Provision a signing home/key separately; do not
commit or transmit private keys in chat. No tools, SDKs or keys are installed by
the helper. An unattended signer must be usable without interactive passphrase input
or use separately managed signing integration.

```sh
python3 packaging/flatpak/prepare-bundle.py \
  --output tmp/flatpak-release \
  --gpg-homedir /private/signing-home \
  --fingerprint FULL_UPPERCASE_PRIMARY_FINGERPRINT \
  --release-date YYYY-MM-DD
```

The helper builds with BUILD_TESTING=OFF, signs the OSTree commit, exports a full
bundle without embedded repo-url/runtime-repo, and signs the original bytes of
`flatpak-release.json` containing version/revision/ref/commit/size/SHA256. No tests,
application launch, installation, remote configuration or publication occurs.
A local export repository is only an intermediate, not a hosting requirement.
On 2026-11-04, the authorized isolated KDE 6.11 SDK build completed for the app
and Go backend. AppStream composition, a cleaned local OSTree export and unsigned
development bundle export completed;
the temporary Go build toolchain was removed from the staged runtime files. This
local-dir development output is not a clean immutable signed release and was not
installed or launched. Signing and manual sandbox acceptance remain pending.
One architecture is prepared per manifest; default x86_64. Multiple architectures
need a reviewed combined manifest and new detached signature, not competing assets
with the same manifest filename. Temporary build files stay below `tmp/`.

The manual `flatpak-artifacts.yml` workflow is artifact-only, contents:read, and
independent of existing test jobs. A maintainer separately configures the protected
flatpak-signing environment, required reviewers, FLATPAK_SIGNING_KEY secret and
FLATPAK_SIGNING_FINGERPRINT variable. Build source/workflow revisions must be trusted
because their build scripts run in the signing job. CI runtime provisioning adds
Flathub only to its disposable build user, not consumers. The signing directory
is removed before uploading only artifacts/. No workflow has been run here.

After manual review, attach the bundle, flatpak-release.json and detached .sig to
a NEW stable vX.Y.Z release matching VERSION; never rewrite historical source
releases. Keep app-release.json source compatibility. Ship the reviewed public
key/fingerprint in audited core separately, not as a key trusted from this download.
Runtime delivery still requires separately approved/configured sources.

## Management and manual acceptance

Settings/kos-apps verifies the signed release, hash/size and exact app/ref/commit,
then uses explicit trusted key bytes with libflatpak. GitHub bundle updates are
checked by Settings/CLI, not promised through Discover or flatpak update when the
app origin has no URL. External Flatpak tools can uninstall the same installed ref.
Local origin/key records may remain after a refused/cancelled transaction.

Manual bundle installation is possible after independently verifying the manifest
signature with the reviewed key and the bundle's signed size/hash/identity:

```sh
flatpak --user install --gpg-file=/trusted/publisher.gpg ./application.flatpak
flatpak --user uninstall org.nextkde.Weather
```

Do not use --no-gpg-verify or --delete-data for normal management. In an isolated
HOME/XDG environment, manually inspect desktop/icon/window identity, forecast and
place search, offline/error presentation, data persistence, helper exit on window
close, no host/core socket use, update and both directions of uninstall/state sync.
The SDK development build and unsigned bundle export completed; sandbox/runtime
acceptance has not. Compilation does not establish these behaviors.


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
