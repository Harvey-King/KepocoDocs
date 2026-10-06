import ast
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'tools' / 'generate_sdk.py'

class SourceIndexTests(unittest.TestCase):
    def test_all_sources_are_indexed_without_importing_hardware(self):
        self.assertTrue(GENERATOR.exists(), 'Source-index generator is missing')
        spec = importlib.util.spec_from_file_location('generate_sdk', GENERATOR)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        inventory = mod.index_sources(ROOT / 'source-library')
        self.assertEqual(len(inventory), 17)
        by_name = {item['name']: item for item in inventory}
        self.assertEqual(by_name['kepoco.py']['module'], 'kepoco')
        self.assertTrue(by_name['kepoco.py']['sha256'])
        self.assertEqual(by_name['kepocoVGA.py']['parse_warning']['line'], 223)
        self.assertIn('VGADriver', [c['name'] for c in by_name['kepocoVGA.py']['classes']])
        for item in inventory:
            self.assertTrue(item['source_path'])
            self.assertGreater(item['line_count'], 0)

    def test_generated_stubs_cover_source_signatures_and_hover_docs(self):
        import os
        import tempfile
        spec = importlib.util.spec_from_file_location('generate_sdk', GENERATOR)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertTrue(hasattr(mod, 'build_sdk'), 'Full stub and documentation generation is missing')
        scratch = ROOT / '.cache'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix='kepoco-sdk-test-') as folder:
            output = Path(folder)
            report = mod.build_sdk(ROOT / 'source-library', output)
            self.assertEqual(report['source_count'], 17)
            self.assertEqual(report['source_stub_count'], 17)
            manifest = json.loads((output / 'docs' / 'SOURCE_MANIFEST.json').read_text())
            self.assertEqual(len(manifest['sources']), 17)
            for item in manifest['sources']:
                stub = output / 'typings' / item['module'] / '__init__.pyi'
                tree = ast.parse(stub.read_text())
                classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
                for cls in item['classes']:
                    self.assertIn(cls['name'], classes)
                    methods = {n.name: n for n in classes[cls['name']].body if isinstance(n, ast.FunctionDef)}
                    for method in cls['methods']:
                        self.assertIn(method['name'], methods)
                        fn = methods[method['name']]
                        names = [a.arg for a in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs]
                        self.assertEqual(names, method['parameters'])
                        self.assertTrue(ast.get_docstring(fn), 'Missing hover documentation')
                self.assertEqual((output/'source-library'/item['name']).read_bytes(), Path(item['source_path']).read_bytes())
            graphics = ast.parse((output/'typings/thumbyGraphics/__init__.pyi').read_text())
            display_cls = next(n for n in graphics.body if isinstance(n, ast.ClassDef) and n.name == 'DisplayInterface')
            methods = {n.name:n for n in display_cls.body if isinstance(n,ast.FunctionDef)}
            self.assertEqual(ast.unparse(methods['getPixel'].returns), 'None')
            self.assertIn('drawEllispe', methods)
            self.assertNotIn('drawEllipse', methods)
            self.assertTrue((output/'docs/API_REFERENCE.md').exists())

if __name__ == '__main__':
    unittest.main(verbosity=2)
