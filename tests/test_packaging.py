import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]

class PackagingTests(unittest.TestCase):
    def test_stage_removes_stale_assets_without_removing_originals(self):
        spec=importlib.util.spec_from_file_location('build_release',ROOT/'tools/build_release.py')
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            for name in ('typings','vendor/micropython','source-library','examples',
                         'evidence','assets','licenses'):
                shutil.copytree(ROOT/name,root/name)
            for name in (*mod.GUIDES,'swerve.py','LICENSE'):
                shutil.copy2(ROOT/name,root/name)
            originals={file.relative_to(root):file.read_bytes()
                       for file in root.rglob('*') if file.is_file()}
            extension=root/'vscode-extension'
            extension.mkdir()
            sibling=extension/'keep.txt'
            sibling.write_text('Not builder-owned assets')
            with patch.object(mod,'ROOT',root):
                assets=mod.stage()
                stale=assets/'source-library/stale_firmware.py'
                stale.write_text('Stale generated file')
                self.assertTrue(stale.exists())
                self.assertEqual(mod.stage(),assets)
                self.assertFalse(stale.exists(),'stage() retained stale generated assets')
            self.assertEqual(sibling.read_text(),'Not builder-owned assets')
            for relative,content in originals.items():
                with self.subTest(original=str(relative)):
                    self.assertEqual((root/relative).read_bytes(),content)
            self.assertTrue((assets/'docs/assets/banner.svg').is_file())
            self.assertTrue((assets/'docs/LICENSE').is_file())
            self.assertTrue((assets/'docs/examples/01_quickstart.py').is_file())

    def test_staged_assets_have_docs_sources_and_notices(self):
        file=ROOT/'tools/build_release.py'
        self.assertTrue(file.exists(),'Release builder missing')
        spec=importlib.util.spec_from_file_location('build_release',file)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assets=mod.stage()
        self.assertTrue((assets/'docs/USB_WORKFLOW.md').exists())
        self.assertTrue((assets/'typings/kepoco/__init__.pyi').exists())
        self.assertEqual((assets/'source-library/kepoco.py').read_bytes(),(ROOT/'source-library/kepoco.py').read_bytes())
        self.assertTrue((ROOT/'vscode-extension/LICENSE').exists())
        checker=ROOT/'tools/check_repository.py'
        spec=importlib.util.spec_from_file_location('check_repository',checker)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for doc in (assets/'docs').glob('*.md'):
            self.assertEqual(mod.broken_links(doc,doc.read_text(encoding='utf-8')),[],doc.name)

if __name__=='__main__': unittest.main()
