import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class RepositoryTests(unittest.TestCase):
    def test_link_checker_reports_missing_files(self):
        file=ROOT/'tools/check_repository.py'
        self.assertTrue(file.exists(),'Repository checker missing')
        spec=importlib.util.spec_from_file_location('check_repository',file)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.broken_links(ROOT/'readme.md','[ok](swerve.py) [external](https://example.com)'),[])
        self.assertEqual(mod.broken_links(ROOT/'readme.md','[bad](does-not-exist.py)'),['does-not-exist.py'])

if __name__=='__main__': unittest.main()
