"""Generated from supplied thumbyButton.py; source SHA-256 3335ac9611054d342758c8b5aea692aebd7a6f5efeb5c4abf41ade49357b3fc3.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from thumbyHardware import swA as swA
from thumbyHardware import swB as swB
from thumbyHardware import swC as swC
from thumbyHardware import swD as swD
from thumbyHardware import swL as swL
from thumbyHardware import swR as swR
from thumbyHardware import swU as swU

class ButtonClass:
    'Source class thumbyButton.py:43. Backend-dependent branches are merged for editing; consult firmware notes.'
    lastState: Any
    latchedPress: bool
    pin: Any

    def __init__(self, pin: Any) -> None:
        'Source-declared method: __init__(self, pin).\nSource: thumbyButton.py:44. Editor-only hints; not a hardware execution guarantee.'
        ...

    def pressed(self) -> bool:
        'Source-declared method: pressed(self).\nSource: thumbyButton.py:56. Editor-only hints; not a hardware execution guarantee.'
        ...

    def justPressed(self) -> bool:
        'Return a new or latched button edge and consume the latch. Read once per frame and store the result if multiple systems need it.\nSource: thumbyButton.py:61. Editor-only hints; not a hardware execution guarantee.'
        ...

    def update(self) -> None:
        'Latches a button press state to be returned later through justPressed\nSource: thumbyButton.py:74. Editor-only hints; not a hardware execution guarantee.'
        ...

def inputPressed(buttons: Iterable[ButtonClass] = ...) -> bool:
    'Returns true if any buttons are currently pressed on the thumby.\nSource: thumbyButton.py:109. Editor-only hints; not a hardware execution guarantee.'
    ...

def inputJustPressed(buttons: Iterable[ButtonClass] = ...) -> bool:
    'Returns true if any buttons were just pressed on the thumby.\nSource: thumbyButton.py:114. Editor-only hints; not a hardware execution guarantee.'
    ...

def dpadPressed() -> bool:
    'Returns true if any dpad buttons are currently pressed on the thumby.\nSource: thumbyButton.py:119. Editor-only hints; not a hardware execution guarantee.'
    ...

def dpadJustPressed() -> bool:
    'Returns true if any dpad buttons were just pressed on the thumby.\nSource: thumbyButton.py:124. Editor-only hints; not a hardware execution guarantee.'
    ...

def actionPressed() -> bool:
    'Returns true if either action button is pressed on the thumby.\nSource: thumbyButton.py:129. Editor-only hints; not a hardware execution guarantee.'
    ...

def actionJustPressed() -> bool:
    'Returns true if either action button was just pressed on the thumby.\nSource: thumbyButton.py:134. Editor-only hints; not a hardware execution guarantee.'
    ...

def updateButtons(buttons: Iterable[ButtonClass] = ...) -> None:
    'Source-declared function: updateButtons(buttons=allButtons).\nSource: thumbyButton.py:143. Editor-only hints; not a hardware execution guarantee.'
    ...
IS_EMULATOR: bool
IS_THUMBY_COLOR: Any
IS_THUMBY_COLOR_LINUX: Any
__version__: str
actionButtons: list[Any]
allButtons: Any
buttonA: ButtonClass
buttonB: ButtonClass
buttonC: ButtonClass
buttonD: ButtonClass
buttonL: ButtonClass
buttonR: ButtonClass
buttonU: ButtonClass
dpadButtons: list[Any]
emulator: Any
engine_io: Any
sys: Any
