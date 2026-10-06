"""Generated from supplied thumbyGrayscale.py; source SHA-256 f2cdeaf3d15009c3896d293b4f9163599e2f61d64312d2020cd5bbdf6cf348ae.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from thumbyHardware import HWID as HWID
from machine import Pin as Pin
from machine import SPI as SPI
from thumbySprite import Sprite as Sprite
from thumbyAudio import audio as audio
from thumbyButton import buttonA as buttonA
from thumbyButton import buttonB as buttonB
from thumbyButton import buttonD as buttonD
from thumbyButton import buttonL as buttonL
from thumbyButton import buttonR as buttonR
from thumbyButton import buttonU as buttonU
from thumbyGraphics import display as display
from machine import idle as idle
from machine import mem32 as mem32
from utime import sleep_ms as sleep_ms
from utime import sleep_us as sleep_us
from utime import ticks_diff as ticks_diff
from utime import ticks_ms as ticks_ms
_thread: Any
array: Any
floor: Any
modules: Any
sqrt: Any
stat: Any
