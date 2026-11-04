# Independent NextKde applications

Calendar, Calculator and Weather share the independent `NextKde/kos-apps` source
repository and release version. ListenFree remains in its own repository.
KMusic retains its existing installation controller and is not handled by this
installer. Settings and the independent repositories ship the same Python 3
standard-library installer, `tools/app-installer.py`; installation never fetches
or executes a replacement installer.

| Key | Fixed repository | Application ID | Executables / desktop IDs |
| --- | --- | --- | --- |
| `calendar` | `NextKde/kos-apps` | `org.nextks.calendar` | `kos-calendar` |
| `calculator` | `NextKde/kos-apps` | `org.nextks.calculator` | `kos-calculator` |
| `weather` | `NextKde/kos-apps` | `org.nextks.weather` | `kos-weather` |
| `listenfree` | `NextKde/ListenFree` | `org.nextkde.ListenFree` | `listenfree` |

Tasks are integrated in Calendar; no separate Todo entry is exposed. Legacy
installer-owned `kos-todo` links remain recognized for offline removal and
upgrade cleanup. Externally installed Todo files are never removed.

New native desktop filenames are `org.nextks.<app>.desktop`; ListenFree retains
`listenfree.desktop`. Executable names stay unchanged. No repository URL, executable
name, shell command or installation root is accepted from a store entry.

The first three apps use one VERSION/commit/Release but separate packages, source
manifests and `-DKOS_APPS=<app>` builds. Old `org.nextkde.Calendar`,
`org.nextkde.Calculator` and `org.nextkde.Weather` Flatpaks are distinct retired
refs: Settings reports RETIRED_FLATPAK_ID and requires external exact-ref management.
No automatic uninstall or private-data migration occurs. Old repositories remain
retained; the new remote and signed release are not yet published. Old installer-owned
source IDs/desktop links remain strictly recognized for offline status/uninstall.

## Command interface

```sh
python3 packaging/installer.py --app calculator check-update
python3 packaging/installer.py --app calculator check
python3 packaging/installer.py --app calculator install --version 0.2.0
python3 packaging/installer.py --app calculator status
python3 packaging/installer.py --app calculator update
python3 packaging/installer.py --app calculator uninstall
```

`--version X.Y.Z` is an optional consistency requirement against the discovered
latest stable release, not an arbitrary tag/revision selector. Only numeric,
three-component semantic versions without prerelease/build suffixes are
accepted. Update comparisons are numeric; downgrades and changed revisions
under the same version are refused.

- `check-update` discovers and validates release metadata without building.
- `check` additionally downloads/verifies source and runs real CMake configure
  to resolve the application's actual development dependencies. It does not
  build or install the application.
- `install` / `update` configure, build and install an immutable version before
  publishing it. An identical installed revision is idempotent. `update`
  requires an existing managed installation.
- `status` / `uninstall` are strictly offline. Uninstall removes only validated
  installer-owned activation links, immutable versions and ownership metadata;
  application settings and user data are preserved. Diagnostic logs remain.

The installer never runs sudo, installs system packages, replays a failed build,
or starts an application. Install Python 3, CMake, Ninja, a C++ compiler and the
app's documented development dependencies with your distribution's package
manager. Configure failures are `DEPENDENCY_UNSATISFIED`, with a private log to
inspect; missing tools are named explicitly.

## Result protocol

Stdout is JSON Lines. Every operation ends with exactly one `type: "result"`
record; earlier `type: "progress"` records are optional. Child output goes only
to a mode-0600 log, never into this protocol.

```json
{"schemaVersion":1,"appId":"org.nextks.calculator","action":"status","stage":"status","type":"result","success":true,"code":"INSTALLED","version":"0.1.0","revision":"0123456789012345678901234567890123456789","details":{"installed":true,"managed":true,"available":true,"version":"0.1.0","revision":"0123456789012345678901234567890123456789","currentVersion":"0.1.0","currentRevision":"0123456789012345678901234567890123456789","desktopFile":"/home/example/.local/share/applications/org.nextks.calculator.desktop","root":"/home/example/.local/share/nextkde-apps/calculator"}}
```

`available` means the local allowlisted engine supports this app; it does not
claim a release is published. Discovery errors such as `RELEASE_UNAVAILABLE`
remain errors and preserve known installed-version details. Successful
`check-update` includes `latestVersion` and `updateAvailable`. Conflicting
external installations return `EXTERNALLY_MANAGED`, `installed: true`,
`managed: false` and an existing fixed desktop path when one is available;
they are never adopted, upgraded or uninstalled. Consumers must not fabricate
an installed version from the catalog or from an error.

Exit statuses: 0 success, 2 expected failure (dependency/release/conflict/state),
3 child timeout, 130 cancellation, 1 unexpected installer error. Invalid CLI
arguments also produce one JSON result. `--help` prints usage normally.

## Release publication and trust

The fixed endpoint is
`https://api.github.com/repos/NextKde/<repository>/releases/latest`.
A published stable, non-draft release must have a `vX.Y.Z` tag and exactly one
`<appId>.app-release.json` asset for the selected kos-apps application
(or `app-release.json` for ListenFree). Example manifest:

```json
{
  "schemaVersion": 1,
  "appId": "org.nextks.calculator",
  "version": "0.1.0",
  "revision": "0123456789012345678901234567890123456789",
  "archiveSha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

The example hash must be replaced with the actual SHA256. The optional
`archiveUrl` must equal
`https://codeload.github.com/NextKde/<repository>/tar.gz/<revision>`.
Metadata is limited to 256 KiB per response, compressed source to 256 MiB and
extracted source to 1 GiB / 100,000 entries. SHA256 is checked before extraction.
Traversal, symbolic links, hard links, special files and duplicate archive paths
are rejected. The source archive must have one top-level CMake project.

Initial requests stay within the exact repository's HTTPS GitHub/API/codeload
paths. Redirects may additionally target GitHub's fixed release asset hosts;
non-HTTPS URLs, credentials and other hosts are rejected. Connection reads time
out after 15 seconds. Unix main-thread signal deadlines bound each complete
metadata/archive attempt to 45/300 seconds, including DNS, redirects and headers.
The complete release discovery (both JSON requests plus retries) additionally
has a 90-second deadline. Nested deadlines never extend an earlier deadline.
Transient failures have at most three attempts with bounded backoff;
integrity/TLS errors, 404 and rate limits are not retried. 404 is
`RELEASE_UNAVAILABLE`; 429 (or exhausted GitHub 403 rate limit) is `RATE_LIMITED`,
with `retryAfter` and `rateLimitReset` details when provided by GitHub.

**Trust is the fixed NextKde GitHub publication over HTTPS, not cryptographic
release signatures.** The checksum binds source bytes to that publication but
is not an independent authenticity proof. CMake source is executable build
logic: installing explicitly trusts the allowlisted publisher. Builds are not
sandboxed. Never install untrusted source by editing the allowlist.

## Storage, activation and ownership

- `${XDG_DATA_HOME:-~/.local/share}/nextkde-apps/KEY/versions/REVISION/`
- `.../KEY/current` — atomic symlink to the published immutable version
- `.../KEY/ownership.json` — exact owned revision and activation link inventory
- `${XDG_STATE_HOME:-~/.local/state}/nextkde-apps/KEY/{lock,logs/}`
- `~/.local/bin/EXECUTABLE` — owned symlink through `current/bin`
- `$XDG_DATA_HOME/applications/ID.desktop` — owned symlink through `current`
- `$XDG_DATA_HOME/dbus-1/services/NAME.service` — only when supplied by the app

CMake's installation prefix is the final immutable version path, not a renamed
staging path. Before publication the old `current` remains untouched. Build,
configure and install failures clean the candidate and preserve the old version.
Success retains prior versions until uninstall. Cancellation terminates the
entire child process group (TERM then KILL); the configured child deadline is
30 minutes per configure/build/install command. Direct SIGKILL or a forced
installer crash can bypass cleanup and leave a child build process running.

Existing user desktop/bin/service files and distro/Nix activation entries are
not overwritten. The installer checks executable PATH entries and system XDG
desktop/D-Bus locations. Calendar's shared PIM service must use its immutable
owned executable directly, not a systemd unit that could activate a different
installation. Existing core PIM service activation is a conflict, not a file to
replace. Stop conflicting applications/services and resolve the package
ownership manually before choosing an independent installation.

A private `transaction.json` in the app state directory records the explicit
owned candidate and old/new inventories before mutation. Under the app lock,
the next invocation (including offline status/uninstall) recovers interruptions:
pre-commit publication rolls back; a committed ownership metadata replacement
completes publication forward and resumes stale activation cleanup. Interrupted
uninstall resumes only its journal-owned inventory. Journal/metadata writes and
publication directory changes are flushed before discarding recovery records.
Cancellation after commit can therefore leave the new version installed rather
than pretending the old version was retained.

Corrupt journals, replaced activation paths, or missing ownership metadata/current
links without a valid journal are refused. This intentionally favors retaining
files over guessing ownership. Do not remove or rewrite metadata to force an
operation. Multi-file uninstall is resumable, not instantaneously atomic; disk
failure or external file replacement can still require manual recovery. No
stale-version garbage collection is performed.

## Manual verification

Use an isolated HOME/XDG directory before trying a real source release. Check
release discovery and dependency diagnostics, install an app, launch it from
its desktop entry, update to a newer version, cancel a build and confirm the
old launcher still works. Verify offline status/uninstall and that application
user data remains. Check that a distro/Nix or existing PIM activation yields a
conflict rather than replacing files. No compositor restart is needed for this
installer itself.
