"""Generated from supplied dummyScreen.py; source SHA-256 990007d7edc738f25c59d9c35674acde38274640e9d56260c06c37b50ad10341.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]

class DummyScreen:
    'Source class dummyScreen.py:57. Backend-dependent branches are merged for editing; consult firmware notes.'
    buffer: bytearray
    display: Any
    external_vcc: Any
    frameRate: float
    height: int
    lastUpdateEnd: Any
    max_x: Any
    max_y: Any
    pages: Any
    textBitmap: bytearray
    textBitmapFile: Any
    textBitmapSource: str
    textCharCount: Any
    textHeight: int
    textSpaceWidth: int
    textWidth: int
    width: int

    def __init__(self, width: int, height: int) -> None:
        'Source-declared method: __init__(self, width, height).\nSource: dummyScreen.py:58. Editor-only hints; not a hardware execution guarantee.'
        ...

    def initEmuScreen(self) -> None:
        'Source-declared method: initEmuScreen(self).\nSource: dummyScreen.py:80. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: dummyScreen.py:83. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweroff(self) -> None:
        'Source-declared method: poweroff(self).\nSource: dummyScreen.py:86. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweron(self) -> None:
        'Source-declared method: poweron(self).\nSource: dummyScreen.py:89. Editor-only hints; not a hardware execution guarantee.'
        ...

    def contrast(self, contrast: int) -> None:
        'Source-declared method: contrast(self, contrast).\nSource: dummyScreen.py:92. Editor-only hints; not a hardware execution guarantee.'
        ...

    def invert(self, invert: Any) -> None:
        'Source-declared method: invert(self, invert).\nSource: dummyScreen.py:95. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFont(self, fontFile: str, width: int, height: int, space: int) -> None:
        'Source-declared method: setFont(self, fontFile, width, height, space).\nSource: dummyScreen.py:99. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFPS(self, newFrameRate: float) -> None:
        'Source-declared method: setFPS(self, newFrameRate).\nSource: dummyScreen.py:109. Editor-only hints; not a hardware execution guarantee.'
        ...

    def update(self) -> None:
        'Push the buffer to the hardware display.\nSource: dummyScreen.py:114. Editor-only hints; not a hardware execution guarantee.'
        ...

    def brightness(self, setting: int) -> None:
        'Set display brightness, valid values 0 to 127\nSource: dummyScreen.py:133. Editor-only hints; not a hardware execution guarantee.'
        ...

    def fill(self, color: int) -> None:
        'Fill the buffer with a given color.\nSource: dummyScreen.py:142. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setPixel(self, x: int, y: int, color: int) -> None:
        'Source-declared method: setPixel(self, x: int, y: int, color: int).\nSource: dummyScreen.py:152. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getPixel(self, x: int, y: int) -> int:
        'Source-declared method: getPixel(self, x: int, y: int).\nSource: dummyScreen.py:167. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawLine(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        'Draw a line from (x1, y1) to (x2, y2) in a given color- taken from MicroPython FrameBuf implementation\nSource: dummyScreen.py:181. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawRectangle(self, x: int, y: int, width: int, height: int, color: int) -> None:
        'Source-declared method: drawRectangle(self, x: int, y: int, width: int, height: int, color: int).\nSource: dummyScreen.py:238. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledRectangle(self, x: int, y: int, width: int, height: int, color: int) -> None:
        'Fill a rectangle with top left corner (x, y) and size (width, height) in a given color.\nSource: dummyScreen.py:246. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawText(self, stringToPrint: Any, x: int, y: int, color: int) -> None:
        'Draw a string with top left corner (x, y) in a given color.\nSource: dummyScreen.py:283. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blit(self, sprtptr: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int) -> None:
        'Source-declared method: blit(self, sprtptr: ptr8, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int).\nSource: dummyScreen.py:336. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawSprite(self, s: Any) -> None:
        'Draw a sprite to the screen\nSource: dummyScreen.py:391. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blitWithMask(self, sprtptr: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, maskptr: Any) -> None:
        'Source-declared method: blitWithMask(self, sprtptr: ptr8, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, maskptr: ptr8).\nSource: dummyScreen.py:395. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawSpriteWithMask(self, s: Any, m: Any) -> None:
        'Source-declared method: drawSpriteWithMask(self, s, m).\nSource: dummyScreen.py:431. Editor-only hints; not a hardware execution guarantee.'
        ...

    def reset(self) -> None:
        'Source-declared method: reset(self).\nSource: dummyScreen.py:435. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show(self) -> None:
        'Source-declared method: show(self).\nSource: dummyScreen.py:465. Editor-only hints; not a hardware execution guarantee.'
        ...
CameraNode: Any
GPIO_OE: Any
GPIO_OE_CLR: Any
GPIO_OE_SET: Any
GPIO_OE_XOR: Any
GPIO_OUT: Any
GPIO_OUT_CLR: Any
GPIO_OUT_SET: Any
GPIO_OUT_XOR: Any
IS_EMULATOR: bool
IS_THUMBY_COLOR: Any
IS_THUMBY_COLOR_LINUX: Any
SIO_BASE: int
Sprite2DNode: Any
TextureResource: Any
Vector2: Any
cam: Any
emulator: Any
engine: Any
engine_draw: Any
engine_main: Any
handshakePin: int
handshakePinToggle: Any
machine: Any
ssd1306_spr: Any
ssd1306_tex: Any
sys: Any
