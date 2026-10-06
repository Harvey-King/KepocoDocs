import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]

class USBTests(unittest.TestCase):
    def load(self):
        path=ROOT/'tools/usb_device.py'
        self.assertTrue(path.exists(), 'Portable USB runner missing')
        spec=importlib.util.spec_from_file_location('usb_device',path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_run_is_temporary_and_starts_clean(self):
        module=self.load()
        cmd=module.command('run','COM7',ROOT/'swerve.py')
        self.assertEqual(cmd[-3:],['soft-reset','run',str(ROOT/'swerve.py')])
        self.assertNotIn('cp',cmd)

    def test_auto_refuses_missing_and_ambiguous_devices(self):
        module=self.load()
        port=lambda name: SimpleNamespace(device=name,vid=0x2e8a,pid=0x0005,serial_number='TEST')
        with self.assertRaises(ValueError): module.select_device('auto',[])
        with self.assertRaises(ValueError): module.select_device('auto',[port('COM7'),port('COM8')])
        self.assertEqual(module.select_device('auto',[port('COM7')]),'COM7')
        self.assertEqual(module.select_device('COM9',[]),'COM9')

    def test_upload_blocks_firmware_and_targets_game_only(self):
        module=self.load()
        self.assertEqual(module.destination(ROOT/'swerve.py'),'/Games/swerve/swerve.py')
        with self.assertRaises(ValueError): module.destination(ROOT/'main.py')
        with self.assertRaises(ValueError): module.destination(ROOT/'source-library/kepoco.py')

    def test_upload_rejects_archive_and_editor_support_directories(self):
        module=self.load()
        with tempfile.TemporaryDirectory() as temporary:
            for directory in ('source-library','vendor','typings'):
                with self.subTest(directory=directory):
                    file=Path(temporary)/directory/'nested/game.py'
                    file.parent.mkdir(parents=True)
                    file.write_text("raise RuntimeError('Never execute source')\n")
                    with self.assertRaises(ValueError):
                        module.destination(file)
                    # Temporary run continues to accept arbitrary saved Python files.
                    self.assertEqual(module.command('run','COM7',file)[-1],str(file.resolve()))
        self.assertEqual(module.destination(ROOT/'examples/01_quickstart.py'),
                         '/Games/01_quickstart/01_quickstart.py')
        self.assertEqual(module.destination(ROOT/'swerve.py'),'/Games/swerve/swerve.py')

    def test_upload_rejects_archived_module_names_outside_archive(self):
        module=self.load()
        sources=list((ROOT/'source-library').rglob('*.py'))
        self.assertTrue(sources)
        with tempfile.TemporaryDirectory() as temporary:
            for source in sources:
                for name in (source.name,source.name.upper()):
                    with self.subTest(name=name):
                        file=Path(temporary)/name
                        file.write_text("raise RuntimeError('Never execute source')\n")
                        with self.assertRaises(ValueError):
                            module.destination(file)
                        self.assertEqual(module.command('run','COM7',file)[-1],str(file.resolve()))

    def test_upload_requires_verified_remote_hash(self):
        module=self.load()
        import hashlib
        digest=hashlib.sha256((ROOT/'swerve.py').read_bytes()).hexdigest()
        with patch.object(module.subprocess,'run',side_effect=[SimpleNamespace(returncode=0),SimpleNamespace(returncode=0),SimpleNamespace(returncode=0,stdout=digest+'\n')]) as run:
            self.assertEqual(module.upload(ROOT/'swerve.py','COM7'),0)
            self.assertIn(':/Games/swerve/swerve.py',run.call_args_list[1].args[0])
        with patch.object(module.subprocess,'run',side_effect=[SimpleNamespace(returncode=0),SimpleNamespace(returncode=0),SimpleNamespace(returncode=0,stdout='bad\n')]):
            with self.assertRaises(RuntimeError): module.upload(ROOT/'swerve.py','COM7')

if __name__=='__main__': unittest.main()
