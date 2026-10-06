"""Generated from supplied thumby.py; source SHA-256 bd7c4a032fed705fdedb4949bd21fc503865c1c05c0cce5fc25cb1311051b70b.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from thumbyHardware import IDPin as IDPin
from thumbySprite import Sprite as Sprite
from thumbyButton import actionJustPressed as actionJustPressed
from thumbyButton import actionPressed as actionPressed
from thumbyAudio import audio as audio
from thumbyButton import buttonA as buttonA
from thumbyButton import buttonB as buttonB
from thumbyButton import buttonC as buttonC
from thumbyButton import buttonD as buttonD
from thumbyButton import buttonL as buttonL
from thumbyButton import buttonR as buttonR
from thumbyButton import buttonU as buttonU
from thumbyGraphics import display as display
from thumbyButton import dpadJustPressed as dpadJustPressed
from thumbyButton import dpadPressed as dpadPressed
from machine import freq as freq
from thumbyButton import inputJustPressed as inputJustPressed
from thumbyButton import inputPressed as inputPressed
from thumbyLink import link as link
from thumbyHardware import reset as reset
from thumbySaves import saveData as saveData
from thumbyHardware import spi as spi
from thumbyHardware import swA as swA
from thumbyHardware import swB as swB
from thumbyHardware import swBuzzer as swBuzzer
from thumbyHardware import swD as swD
from thumbyHardware import swL as swL
from thumbyHardware import swR as swR
from thumbyHardware import swU as swU
IS_EMULATOR: bool
IS_THUMBY_LEGACY: Any
__version__: str
emulator: Any
sys: Any
