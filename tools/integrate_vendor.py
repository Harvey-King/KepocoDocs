"""Connect vendored MicroPython time hints without replacing runtime modules."""
from pathlib import Path
import ast
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
vendor = ROOT / 'vendor/micropython'
target = ROOT / 'typings/time/__init__.pyi'
target.parent.mkdir(parents=True, exist_ok=True)
ast.parse((vendor/'time.pyi').read_text(encoding='utf-8'))
shutil.copy2(vendor/'time.pyi', target)
report = {
    'purpose': 'Editor-only RP2 baseline; not proof of the Kepoco firmware MicroPython version or available hardware.',
    'packages': ['micropython-rp2-rpi_pico-stubs==1.29.0.post1', 'micropython-stdlib-stubs==1.29.0.post2'],
    'source': 'https://pypi.org/project/micropython-rp2-rpi_pico-stubs/',
    'time_override': 'typings/time/__init__.pyi',
    'note': 'The project-local time stub selects MicroPython ticks_* hints instead of CPython time. Vendor files and their notices are kept intact.'
}
(ROOT/'evidence/VENDOR_MANIFEST.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Installed project-local MicroPython time hints; original vendor files retained.')
