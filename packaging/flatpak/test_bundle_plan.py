"""Regression checks for byte-exact signed plans; run in the build VM/CI."""
import hashlib
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('prepare_bundle', Path(__file__).with_name('prepare-bundle.py'))
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class BundlePlanTest(unittest.TestCase):
    def test_metadata_preserves_whitespace_and_non_ascii_bytes(self):
        metadata = '\n# 计算器\n[Application]\nname=org.nextks.calculator\nruntime=org.kde.Platform/x86_64/6.11\n\n'.encode()
        with patch.object(helper.subprocess, 'run', return_value=SimpleNamespace(stdout=metadata)) as command:
            plan = helper.metadata_plan('/repo', 'org.nextks.calculator', 'x86_64')
        self.assertEqual(plan['metadata'], metadata)
        self.assertEqual(plan['metadataSha256'], hashlib.sha256(metadata).hexdigest())
        self.assertEqual(plan['runtime']['ref'], 'runtime/org.kde.Platform/x86_64/6.11')
        self.assertNotIn('text', command.call_args.kwargs)

    def test_signing_gate_rejects_stripped_metadata(self):
        original = b'[Application]\nname=org.nextks.calculator\n'
        stripped = original.strip()
        with patch.object(helper, 'bundle_metadata_and_size', return_value=(original, 1024)):
            with self.assertRaisesRegex(ValueError, 'refusing to sign'):
                helper.check_bundle_plan(Path('/bundle'), {'metadata': stripped, 'metadataSha256': hashlib.sha256(stripped).hexdigest()})

    def test_signing_gate_rejects_wrong_digest(self):
        with patch.object(helper, 'bundle_metadata_and_size', return_value=(b'metadata\n', 1024)):
            with self.assertRaisesRegex(ValueError, 'digest'):
                helper.check_bundle_plan(Path('/bundle'), {'metadata': b'metadata\n', 'metadataSha256': '0' * 64})

    def test_signing_gate_uses_bundle_size_and_rejects_out_of_range(self):
        plan = {'metadata': b'metadata\n', 'metadataSha256': hashlib.sha256(b'metadata\n').hexdigest()}
        with patch.object(helper, 'bundle_metadata_and_size', return_value=(b'metadata\n', 2867968)):
            self.assertEqual(helper.check_bundle_plan(Path('/bundle'), plan), 2867968)
        with patch.object(helper, 'bundle_metadata_and_size', return_value=(b'metadata\n', 2**31 + 1)):
            with self.assertRaisesRegex(ValueError, 'outside'):
                helper.check_bundle_plan(Path('/bundle'), plan)


if __name__ == '__main__':
    unittest.main()
