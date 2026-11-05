"""Validate the narrow unsigned-candidate import before using publisher keys."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("prepare_bundle", ROOT / "packaging/flatpak/prepare-bundle.py")
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class CandidateTest(unittest.TestCase):
    def setUp(self):
        temporary = ROOT / "tmp" / "candidate-tests"
        temporary.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temporary)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.candidate = self.root / "candidate"
        self.work = self.root / "work"
        self.candidate.mkdir()
        self.work.mkdir()
        (self.candidate / "repo").mkdir()
        (self.candidate / "repo/config").write_text("[core]\nmode=archive-z2\n")
        (self.candidate / "evidence").mkdir()
        self.app_id = "org.nextks.calendar"
        self.revision = "a" * 40
        self.args = SimpleNamespace(arch="x86_64", release_date="2026-11-05")
        self.manifest = json.loads((ROOT / f"packaging/flatpak/{self.app_id}.json").read_text())
        self.manifest["modules"][-1]["sources"] = [{
            "type": "git", "url": bundle.REPOSITORY, "commit": self.revision}]
        self.manifest["modules"][-1]["config-opts"].append("-DKOS_FLATPAK_RELEASE_DATE=2026-11-05")
        self.environment = {
            role: {"ref": f"{self.manifest[role]}/x86_64/6.11", "commit": "b" * 64}
            for role in ("runtime", "sdk")}
        self.refs = [f"app/{self.app_id}/x86_64/stable",
                     f"runtime/{self.app_id}.Sources/x86_64/stable"]
        self.save()
        self.run = self.enterContext(patch.object(bundle, "run", side_effect=self.command))
        self.enterContext(patch.object(bundle, "candidate_manifest", return_value=self.manifest))

    def command(self, *args, **kwargs):
        if args[-1] == "refs":
            return "\n".join(self.refs)
        if args[-1] == "fsck":
            return None
        self.fail(f"Unexpected command before signing: {args}")

    def save(self):
        (self.candidate / f"{self.app_id}.json").write_text(json.dumps(self.manifest))
        (self.candidate / "evidence/environment.json").write_text(json.dumps(self.environment))

    def import_candidate(self):
        return bundle.import_candidate(self.candidate, self.app_id, self.revision, self.args, self.work)

    def test_calendar_keeps_translations_in_main_bundle(self):
        manifest = json.loads((ROOT / "packaging/flatpak/org.nextks.calendar.json").read_text())
        self.assertIs(manifest["separate-locales"], False)

    def test_calendar_retains_upstream_license_directories(self):
        manifest = json.loads((ROOT / "packaging/flatpak/org.nextks.calendar.json").read_text())
        modules = {module["name"]: module for module in manifest["modules"]}
        for name in ("libical", "kcalendarcore"):
            with self.subTest(module=name):
                self.assertIn(f"cp -a LICENSES /app/share/licenses/{name}/",
                              modules[name]["post-install"])
        self.assertIn(
            "install -m644 LICENSE.txt COPYING.LESSER.txt 3RDPARTY.md CONTRIBUTORS.md README.md /app/share/licenses/libical/",
            modules["libical"]["post-install"])

    def test_valid_candidate_is_copied_not_modified(self):
        self.assertEqual(self.import_candidate(), self.environment)
        self.assertTrue((self.work / "repo/config").is_file())
        self.assertTrue((self.work / "evidence/environment.json").is_file())
        self.assertTrue((self.candidate / "repo/config").is_file())
        self.assertEqual(self.run.call_count, 2)

    def test_symlink_rejected_before_commands(self):
        (self.candidate / "repo/redirect").symlink_to(self.root)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.import_candidate()
        self.run.assert_not_called()

    def test_unretained_build_tree_is_not_imported(self):
        (self.candidate / "build").mkdir()
        (self.candidate / "build/link").symlink_to(self.root)
        self.assertEqual(self.import_candidate(), self.environment)
        self.assertFalse((self.work / "build").exists())

    def test_symlinked_input_directory_rejected(self):
        (self.candidate / "repo/config").unlink()
        (self.candidate / "repo").rmdir()
        (self.candidate / "repo").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.import_candidate()
        self.run.assert_not_called()

    def test_manifest_changes_rejected(self):
        altered = dict(self.manifest, **{"finish-args": ["--filesystem=host"]})
        (self.candidate / f"{self.app_id}.json").write_text(json.dumps(altered))
        with self.assertRaisesRegex(ValueError, "manifest differs"):
            self.import_candidate()
        self.run.assert_not_called()

    def test_runtime_and_sdk_are_required(self):
        del self.environment["sdk"]
        self.save()
        with self.assertRaisesRegex(ValueError, "runtime and SDK"):
            self.import_candidate()

    def test_environment_identity_and_commit_rejected(self):
        for value in ({"ref": "org.kde.Platform/aarch64/6.11", "commit": "b" * 64},
                      {"ref": "org.kde.Platform/x86_64/6.11", "commit": "short"}):
            with self.subTest(value=value):
                self.environment["runtime"] = value
                self.save()
                with self.assertRaisesRegex(ValueError, "runtime environment"):
                    self.import_candidate()

    def test_missing_sources_rejected(self):
        self.refs.pop()
        with self.assertRaisesRegex(ValueError, "missing or unexpected refs"):
            self.import_candidate()

    def test_foreign_ref_rejected(self):
        self.refs.append("app/org.example.Other/x86_64/stable")
        with self.assertRaisesRegex(ValueError, "missing or unexpected refs"):
            self.import_candidate()

    def test_optional_debug_export_accepted(self):
        self.refs.append(f"runtime/{self.app_id}.Debug/x86_64/stable")
        self.assertEqual(self.import_candidate(), self.environment)


if __name__ == "__main__":
    unittest.main()
