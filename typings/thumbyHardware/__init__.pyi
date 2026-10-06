"""Generated from supplied thumbyHardware.py; source SHA-256 dbe958477b3513ecb54a80b4318b7d352cc0474fb036ddc2e0a416bad02bf4c5.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from dummyScreen import DummyScreen as DummyScreen
from machine import I2C as I2C
from machine import PWM as PWM
from machine import Pin as Pin
from machine import SPI as SPI
from ssd1306 import SSD1306 as SSD1306
from kepocoDisplayST77xx import ST7735CompatDriver as ST7735CompatDriver
from kepocoDisplayST77xx import ST7789CompatDriver as ST7789CompatDriver
from machine import freq as freq
from machine import reset as machineReset

class PwmDummy:
    'Source class thumbyHardware.py:53. Backend-dependent branches are merged for editing; consult firmware notes.'

    def __init__(self) -> None:
        'Source-declared method: __init__(self).\nSource: thumbyHardware.py:54. Editor-only hints; not a hardware execution guarantee.'
        ...

    def duty_u16(self, value: Any) -> None:
        'Source-declared method: duty_u16(self, value).\nSource: thumbyHardware.py:57. Editor-only hints; not a hardware execution guarantee.'
        ...

    def freq(self, value: Any) -> None:
        'Source-declared method: freq(self, value).\nSource: thumbyHardware.py:60. Editor-only hints; not a hardware execution guarantee.'
        ...

def reset() -> None:
    'Wrap machine.reset() to be accessible as thumby.reset()\nSource: thumbyHardware.py:133. Editor-only hints; not a hardware execution guarantee.'
    ...
HWID: int
IDPin: Pin
IS_EMULATOR: bool
IS_THUMBY_COLOR: Any
IS_THUMBY_COLOR_LINUX: Any
__version__: str
buzzerEn: Pin
displayDriver: DummyScreen
emulator: Any
engine: Any
i2c: I2C
spi: Any
swA: Pin
swB: Pin
swBuzzer: PWM
swC: Any
swD: Pin
swL: Pin
swR: Pin
swU: Pin
sys: Any
