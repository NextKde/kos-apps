#!/usr/bin/env python3
"""Build signed application bundle artifacts locally; never install or publish them."""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile

APPS = ("calendar", "calculator", "weather")
REPOSITORY = "https://github.com/NextKde/kos-apps.git"
ROOT = Path(__file__).resolve().parents[2]


def run(*args, capture=False):
    result = subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE if capture else None)
    return result.stdout.strip() if capture else None


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(128 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def build_environment(manifest, arch):
    refs = {role: f"{manifest[role]}/{arch}/{manifest['runtime-version']}"
            for role in ("runtime", "sdk")}
    commits = {}
    for role, ref in refs.items():
        commit = run("flatpak", "info", "--user", "--show-commit", ref, capture=True)
        if not re.fullmatch(r"[0-9a-f]{64}", commit):
            raise ValueError(f"Missing exact user-level {role} commit: {ref}")
        commits[role] = {"ref": ref, "commit": commit}
    return commits


def candidate_manifest(app_id, revision, release_date):
    source = run("git", "-C", str(ROOT), "show",
                 f"{revision}:packaging/flatpak/{app_id}.json", capture=True)
    manifest = json.loads(source)
    manifest["modules"][-1]["sources"] = [{"type": "git", "url": REPOSITORY, "commit": revision}]
    manifest["modules"][-1]["config-opts"].append(f"-DKOS_FLATPAK_RELEASE_DATE={release_date}")
    return manifest


def import_candidate(candidate, app_id, revision, args, work):
    # Only explicitly reviewed CI artifacts are inputs; their contents do not
    # establish publisher trust. Never mutate or sign the downloaded repository.
    if any(path.is_symlink() for path in candidate.rglob("*")):
        raise ValueError("Candidate must not contain symlinks")
    manifest = json.loads((candidate / f"{app_id}.json").read_text())
    if manifest != candidate_manifest(app_id, revision, args.release_date):
        raise ValueError("Candidate manifest differs from the exact reviewed source/date")
    environment = json.loads((candidate / "evidence/environment.json").read_text())
    if set(environment) != {"runtime", "sdk"}:
        raise ValueError("Candidate must record its runtime and SDK")
    for role, entry in environment.items():
        expected = f"{manifest[role]}/{args.arch}/{manifest['runtime-version']}"
        if entry.get("ref") != expected or not re.fullmatch(r"[0-9a-f]{64}", entry.get("commit", "")):
            raise ValueError(f"Invalid candidate {role} environment")
    original = candidate / "repo"
    refs = set(run("ostree", f"--repo={original}", "refs", capture=True).splitlines())
    expected = {f"app/{app_id}/{args.arch}/stable",
                f"runtime/{app_id}.Sources/{args.arch}/stable"}
    if not expected <= refs or refs - expected - {f"runtime/{app_id}.Debug/{args.arch}/stable"}:
        raise ValueError("Candidate contains missing or unexpected refs")
    run("ostree", f"--repo={original}", "fsck")
    shutil.copytree(original, work / "repo")
    shutil.copytree(candidate / "evidence", work / "evidence")
    (work / f"{app_id}.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return environment


def retain_sources(app_id, environment, work, artifacts, repo, version, revision, args, homedir):
    # Sources contains builder-managed module inputs, not the cleaned /app tree.
    source_id = app_id + ".Sources"
    source_ref = f"runtime/{source_id}/{args.arch}/stable"
    source_commit = run("ostree", f"--repo={repo}", "rev-parse", source_ref, capture=True)
    if not re.fullmatch(r"[0-9a-f]{64}", source_commit):
        raise ValueError("Source export did not produce an exact OSTree commit")
    run("flatpak", "build-sign", "--runtime", f"--arch={args.arch}",
        f"--gpg-homedir={homedir}", f"--gpg-sign={args.fingerprint}",
        str(repo), source_id, "stable")
    source_asset = f"{source_id}-{version}-{args.arch}.flatpak"
    run("flatpak", "build-bundle", "--runtime", f"--arch={args.arch}",
        str(repo), str(artifacts / source_asset), source_id, "stable")
    run("git", "-C", str(ROOT), "archive", "--format=tar.gz",
        f"--output={artifacts / (app_id + '-' + revision + '-source.tar.gz')}", revision)
    shutil.copyfile(work / f"{app_id}.json", artifacts / f"{app_id}.build-manifest.json")
    if (work / "source-inputs").exists():
        shutil.copytree(work / "source-inputs", artifacts / "source-inputs")
    metadata = run("ostree", f"--repo={repo}", "cat",
                   f"app/{app_id}/{args.arch}/stable", "/metadata", capture=True)
    (artifacts / f"{app_id}.flatpak-metadata.ini").write_text(metadata + "\n")
    if (work / "evidence").is_dir():
        shutil.copytree(work / "evidence", artifacts / f"{app_id}.sdk-evidence")
    inventory = run("ostree", f"--repo={repo}", "ls", "-R",
                    f"app/{app_id}/{args.arch}/stable", capture=True)
    (artifacts / f"{app_id}.runtime-files.txt").write_text(inventory + "\n")
    provenance = {
        "schemaVersion": 1, "appId": app_id, "version": version, "revision": revision,
        "environment": environment,
        "tools": {tool: run(tool, "--version", capture=True)
                  for tool in (("flatpak", "ostree") if args.candidate
                               else ("flatpak", "flatpak-builder", "ostree"))},
        "unsignedCandidate": bool(args.candidate),
        "sources": {"ref": source_ref, "commit": source_commit, "asset": source_asset},
        "reviewRequired": "Review source completeness, SDK/runtime source obligations, "
                          "linked component configuration and notices before publication."
    }
    (artifacts / f"{app_id}.build-info.json").write_text(json.dumps(provenance, indent=2) + "\n")
    # The legacy installer also follows releases/latest; retain its source contract.
    run(sys.executable, str(ROOT / "packaging/prepare-release.py"),
        "--app", app_id.rsplit(".", 1)[-1].lower(), "--version", version,
        "--revision", revision, "--output", str(artifacts / f"{app_id}.app-release.json"))
    # Bind every retained artifact, including nested patches, to the publisher key.
    checksums = artifacts / f"{app_id}.SHA256SUMS"
    checksums.write_text("".join(
        f"{sha256(path)}  {path.relative_to(artifacts).as_posix()}\n"
        for path in sorted(artifacts.rglob("*")) if path.is_file()))
    run("gpg", "--batch", "--homedir", str(homedir), "--local-user", args.fingerprint,
        "--digest-algo", "SHA256", "--detach-sign", "--output", str(checksums) + ".sig", str(checksums))
    # GitHub assets are flat; preserve nested patches in a directly signed archive.
    archive = artifacts / f"{app_id}-{version}-{args.arch}-release-materials.tar.gz"
    entries = sorted(artifacts.iterdir())
    with tarfile.open(archive, "w:gz") as stream:
        for path in entries:
            stream.add(path, arcname=path.name)
    run("gpg", "--batch", "--homedir", str(homedir), "--local-user", args.fingerprint,
        "--digest-algo", "SHA256", "--detach-sign", "--output", str(archive) + ".sig", str(archive))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", choices=APPS, required=True)
    parser.add_argument("--output", type=Path, required=True, help="New directory below this checkout's tmp/")
    parser.add_argument("--gpg-homedir", type=Path, required=True, help="Existing private signing home; no keys are generated")
    parser.add_argument("--fingerprint", required=True, help="Reviewed full primary signing-key fingerprint")
    parser.add_argument("--arch", choices=("x86_64", "aarch64"), default="x86_64")
    parser.add_argument("--release-date", required=True, help="YYYY-MM-DD for AppStream")
    parser.add_argument("--candidate", type=Path, help="Extracted reviewed unsigned SDK candidate; skip building")
    parser.add_argument("--revision", help="Full reviewed source commit, required with --candidate")
    args = parser.parse_args()
    if bool(args.candidate) != bool(args.revision):
        parser.error("--candidate and --revision must be supplied together")
    if args.revision and not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("Candidate revision must be a full lowercase commit SHA")
    app_id = "org.nextks." + args.app
    tools = ("git", "flatpak", "ostree", "gpg") + (() if args.candidate else ("flatpak-builder",))
    for tool in tools:
        if not shutil.which(tool):
            parser.error(f"Required build tool is missing: {tool}")
    if not re.fullmatch(r"[0-9A-F]{40}(?:[0-9A-F]{24})?", args.fingerprint):
        parser.error("Use the full uppercase primary fingerprint, not a short key ID")
    if date.fromisoformat(args.release_date).isoformat() != args.release_date:
        parser.error("Invalid release date")
    homedir = args.gpg_homedir.resolve()
    if not homedir.is_dir():
        parser.error("Signing home does not exist; provision it separately")
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / "tmp") or output == ROOT / "tmp" or output.exists():
        parser.error("Output must be a new directory below this checkout's tmp/")
    # Publication builds must include the reviewed packaging work in the source pin.
    if run("git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=normal", capture=True):
        parser.error("Commit/review source and packaging first; the checkout must be clean")
    revision = args.revision or run("git", "-C", str(ROOT), "rev-parse", "HEAD", capture=True)
    run("git", "-C", str(ROOT), "merge-base", "--is-ancestor", revision, "HEAD")
    version = run("git", "-C", str(ROOT), "show", f"{revision}:VERSION", capture=True)
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
        parser.error("Expected an immutable commit and stable X.Y.Z VERSION")
    # A signing subkey may be used, but the configured identity must be its primary.
    listing = run("gpg", "--batch", "--homedir", str(homedir), "--with-colons", "--list-secret-keys", args.fingerprint, capture=True)
    primary = []
    expect_primary = False
    for line in listing.splitlines():
        fields = line.split(":")
        if fields[0] == "sec":
            expect_primary = True
        elif fields[0] == "ssb":
            expect_primary = False
        elif fields[0] == "fpr" and expect_primary:
            primary.append(fields[9])
            expect_primary = False
    if primary != [args.fingerprint]:
        parser.error("Signing home did not resolve exactly the requested primary key")
    output.mkdir(parents=True, mode=0o700)
    work = output / "work"
    artifacts = output / "artifacts"
    work.mkdir(mode=0o700)
    artifacts.mkdir(mode=0o700)
    manifest = candidate_manifest(app_id, revision, args.release_date)
    build_manifest = work / f"{app_id}.json"
    repo = work / "repo"
    if args.candidate:
        candidate = args.candidate.resolve()
        if not candidate.is_relative_to(ROOT / "tmp") or not candidate.is_dir():
            parser.error("Candidate must be an extracted directory below this checkout's tmp/")
        environment = import_candidate(candidate, app_id, revision, args, work)
    else:
        build_manifest.write_text(json.dumps(manifest, indent=2) + "\n")
        environment = build_environment(manifest, args.arch)
        # Runtime/SDK must already be provisioned in the build environment. The builder
        # may fetch the pinned source; it never installs the resulting application.
        run("flatpak-builder", "--user", f"--arch={args.arch}", "--default-branch=stable", "--disable-rofiles-fuse", "--disable-tests", "--bundle-sources",
            f"--state-dir={work / 'state'}", f"--repo={repo}", str(work / "build"), str(build_manifest))
        if build_environment(manifest, args.arch) != environment:
            raise ValueError("SDK/runtime changed during the build; rebuild before signing")
    run("flatpak", "build-sign", f"--arch={args.arch}", f"--gpg-homedir={homedir}",
        f"--gpg-sign={args.fingerprint}", str(repo), app_id, "stable")
    ref = f"app/{app_id}/{args.arch}/stable"
    commit = run("ostree", f"--repo={repo}", "rev-parse", ref, capture=True)
    if not re.fullmatch(r"[0-9a-f]{64}", commit):
        raise ValueError("Export did not produce an exact OSTree commit")
    asset = f"{app_id}-{version}-{args.arch}.flatpak"
    bundle = artifacts / asset
    # No repo-url/runtime-repo: the bundle cannot inject an online app/runtime source.
    run("flatpak", "build-bundle", f"--arch={args.arch}", str(repo), str(bundle), app_id, "stable")
    size = bundle.stat().st_size
    if not 0 < size <= 2 * 1024 * 1024 * 1024:
        raise ValueError("Bundle exceeds the client size contract")
    digest = hashlib.sha256()
    with bundle.open("rb") as stream:
        while chunk := stream.read(128 * 1024):
            digest.update(chunk)
    release = {"schemaVersion": 1, "appId": app_id, "version": version, "revision": revision,
               "bundles": {args.arch: {"ref": ref, "commit": commit, "asset": asset,
                                       "size": size, "sha256": digest.hexdigest()}}}
    metadata = artifacts / f"{app_id}.flatpak-release.json"
    metadata.write_text(json.dumps(release, indent=2) + "\n")
    run("gpg", "--batch", "--homedir", str(homedir), "--local-user", args.fingerprint,
        "--digest-algo", "SHA256", "--detach-sign", "--output", str(metadata) + ".sig", str(metadata))
    retain_sources(app_id, environment, work, artifacts, repo, version, revision, args, homedir)
    print(f"Prepared {artifacts}. Nothing was installed or published.")
    print(f"Review artifacts and source, then attach ALL artifacts (including Sources and signed checksums) to a NEW stable v{version} release.")
    print("Ship the reviewed public key/fingerprint in core separately; never trust a key downloaded beside these files.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Bundle preparation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
