import ast
import importlib.util
import json
import re
import sys
import types
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ExamplesTests(unittest.TestCase):
    def test_quickstart_starts_moves_draws_and_exits(self):
        path = ROOT / 'examples' / '01_quickstart.py'
        self.assertTrue(path.exists(), 'The complete starter example is missing')
        class Display:
            BLACK, WHITE, width, height = 0, 1, 72, 40
            def __init__(self):
                self.frames = 0
                self.xs = []
            def setFPS(self, rate):
                self.rate = rate
            def fill(self, colour):
                pass
            def drawFilledRectangle(self, x, y, width, height, colour):
                self.assert_bounds(x, y, width, height)
                self.xs.append(x)
            def assert_bounds(self, x, y, w, h):
                assert 0 <= x and x + w <= 72 and 0 <= y and y + h <= 40
            def update(self):
                self.frames += 1
        display = Display()
        button = lambda held=False, edge=False: types.SimpleNamespace(pressed=lambda: held, justPressed=lambda: edge)
        fake = types.SimpleNamespace(display=display, buttonL=button(), buttonR=button(True),
            buttonB=types.SimpleNamespace(justPressed=lambda: display.frames >= 8))
        old = {n:sys.modules.get(n) for n in ('kepoco','time')}
        sys.modules['kepoco'] = fake
        sys.modules['time'] = types.SimpleNamespace(ticks_ms=lambda: display.frames*33, ticks_diff=lambda a,b:a-b)
        try:
            code = compile(path.read_text(), str(path), 'exec')
            exec(code, {'__name__':'__main__'})
        finally:
            for name, value in old.items():
                if value is None: sys.modules.pop(name,None)
                else: sys.modules[name] = value
        self.assertEqual(display.rate,30)
        self.assertEqual(display.frames,9)
        self.assertGreater(display.xs[-1],display.xs[0])

    def test_all_snippet_default_expansions_are_complete_python(self):
        snippets = json.loads((ROOT/'vscode-extension/snippets/kepoco.json').read_text())
        self.assertEqual(len(snippets),8)
        for name, snippet in snippets.items():
            code = '\n'.join(snippet['body'])
            code = re.sub(r'\$\{\d+:([^}]*)\}',lambda m:m.group(1),code)
            code = re.sub(r'\$\d+','',code)
            ast.parse(code,filename=name)
            self.assertIn('import kepoco',code)

if __name__ == '__main__':
    unittest.main(verbosity=2)
