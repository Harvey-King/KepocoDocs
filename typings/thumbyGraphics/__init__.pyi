"""Generated from supplied thumbyGraphics.py; source SHA-256 ba193e731f3f03a64b05c71db1a65ac7ee70ea0cc4c77136619dcca883c1ee9f.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from kepocoDisplayDriver import DisplayDriver as DisplayDriver
from thumbyHardware import IS_EMULATOR as IS_EMULATOR
from thumbySprite import Sprite as Sprite
from thumbyHardware import displayDriver as displayDriver
from machine import freq as freq
from thumbyHardware import i2c as i2c
from kepocoConfig import settings as settings
from utime import sleep_ms as sleep_ms
from utime import sleep_us as sleep_us
from utime import ticks_diff as ticks_diff
from utime import ticks_ms as ticks_ms
from thumbyButton import updateButtons as updateButtons

class DisplayInterface:
    'Source class thumbyGraphics.py:9. Backend-dependent branches are merged for editing; consult firmware notes.'
    BLACK: int
    DARKGRAY: int
    LIGHTGRAY: int
    WHITE: int
    display: DisplayDriver
    driver: DisplayDriver
    font_bmap: bytearray
    font_glyphcnt: int
    font_height: int
    font_space: int
    font_width: int
    frameRate: float
    height: int
    lastUpdateEnd: Any
    width: int

    def __init__(self, driver: DisplayDriver) -> None:
        'Source-declared method: __init__(self, driver: DisplayDriver).\nSource: thumbyGraphics.py:16. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweroff(self) -> None:
        'Source-declared method: poweroff(self).\nSource: thumbyGraphics.py:31. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweron(self) -> None:
        'Source-declared method: poweron(self).\nSource: thumbyGraphics.py:34. Editor-only hints; not a hardware execution guarantee.'
        ...

    def contrast(self, contrast: int) -> None:
        'Source-declared method: contrast(self, contrast).\nSource: thumbyGraphics.py:37. Editor-only hints; not a hardware execution guarantee.'
        ...

    def invert(self, inverted: bool) -> None:
        'Source-declared method: invert(self, inverted).\nSource: thumbyGraphics.py:40. Editor-only hints; not a hardware execution guarantee.'
        ...

    def flash(self) -> None:
        'Source-declared method: flash(self).\nSource: thumbyGraphics.py:43. Editor-only hints; not a hardware execution guarantee.'
        ...

    def enableGrayscale(self) -> None:
        'Deprecated\nSource: thumbyGraphics.py:49. Editor-only hints; not a hardware execution guarantee.'
        ...

    def disableGrayscale(self) -> None:
        'Deprecated\nSource: thumbyGraphics.py:53. Editor-only hints; not a hardware execution guarantee.'
        ...

    def enableGreyscale(self) -> None:
        'Deprecated\nSource: thumbyGraphics.py:57. Editor-only hints; not a hardware execution guarantee.'
        ...

    def disableGreyscale(self) -> None:
        'Deprecated\nSource: thumbyGraphics.py:61. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setColourTint(self, red: int, green: int, blue: int) -> None:
        'Deprecated\nSource: thumbyGraphics.py:65. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeMono(self) -> None:
        'Source-declared method: setModeMono(self).\nSource: thumbyGraphics.py:68. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeGreyscale(self) -> None:
        'Select four-tone greyscale if supported by the active driver. Support is backend-dependent.\nSource: thumbyGraphics.py:71. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeTinted(self, red: int, green: int, blue: int) -> None:
        'Source-declared method: setModeTinted(self, red, green, blue).\nSource: thumbyGraphics.py:74. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show(self) -> None:
        'Source-declared method: show(self).\nSource: thumbyGraphics.py:77. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFPS(self, newFrameRate: float) -> None:
        'Set the requested FPS, clamped to 0..60 in this library. Zero disables frame limiting; actual delivered FPS may be lower.\nSource: thumbyGraphics.py:81. Editor-only hints; not a hardware execution guarantee.'
        ...

    def update(self) -> None:
        'Present the buffer and enforce the frame-rate cap. While waiting, button edges are latched. Does not return a frame count.\nSource: thumbyGraphics.py:86. Editor-only hints; not a hardware execution guarantee.'
        ...

    def brightness(self, setting: int) -> None:
        'Source-declared method: brightness(self, setting).\nSource: thumbyGraphics.py:100. Editor-only hints; not a hardware execution guarantee.'
        ...

    def fill(self, colour: int) -> None:
        'Source-declared method: fill(self, colour: int).\nSource: thumbyGraphics.py:104. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: thumbyGraphics.py:108. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: thumbyGraphics.py:112. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Exact source spelling: Ellispe, not Ellipse. Draw a filled ellipse through the current driver.\nSource: thumbyGraphics.py:116. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawEllispe(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Exact source spelling: Ellispe, not Ellipse. Delegates to the active driver; the base driver may raise NotImplementedError.\nSource: thumbyGraphics.py:120. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setPixel(self, x: int, y: int, colour: int) -> None:
        'Source-declared method: setPixel(self, x: int, y: int, colour: int).\nSource: thumbyGraphics.py:124. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getPixel(self, x: int, y: int) -> None:
        'WARNING: this wrapper calls driver.getPixel but does not return it. In the supplied source this returns None, not a pixel colour.\nSource: thumbyGraphics.py:128. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int) -> None:
        'Source-declared method: drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int).\nSource: thumbyGraphics.py:132. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFont(self, fontFile: str, width: int | None = None, height: int | None = None, space: int = 1) -> None:
        'Load a .bin font; width and height can be inferred from a fontWIDTHxHEIGHT filename. space is inter-character spacing. The file must exist on the target.\nSource: thumbyGraphics.py:135. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawText(self, stringToPrint: str | bytes | bytearray | memoryview, x: int, y: int, colour: int) -> None:
        'Draw text with the selected bitmap font. This source constructs memoryview(stringToPrint); bytes are a safer choice when porting across runtimes. Call update to show it.\nSource: thumbyGraphics.py:153. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blit(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int) -> None:
        'Source-declared method: blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int).\nSource: thumbyGraphics.py:181. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawSprite(self, s: Sprite) -> None:
        'Draw a Sprite using its bitmap, position, key and mirror fields. Rendering remains in the buffer until update/show.\nSource: thumbyGraphics.py:185. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blitWithMask(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask: Any) -> None:
        'Source-declared method: blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask).\nSource: thumbyGraphics.py:189. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawSpriteWithMask(self, s: Sprite, m: Sprite) -> None:
        'Draw sprite s with sprite m as its mask. Both arguments must expose bitmap data.\nSource: thumbyGraphics.py:193. Editor-only hints; not a hardware execution guarantee.'
        ...

    def calibrate(self) -> None:
        'Source-declared method: calibrate(self).\nSource: thumbyGraphics.py:196. Editor-only hints; not a hardware execution guarantee.'
        ...

def detect_vga(i2c: Any, guess: Any = False) -> bool:
    'Source-declared function: detect_vga(i2c, guess=False).\nSource: thumbyGraphics.py:218. Editor-only hints; not a hardware execution guarantee.'
    ...

def do_test() -> None:
    'Source-declared function: do_test().\nSource: thumbyGraphics.py:282. Editor-only hints; not a hardware execution guarantee.'
    ...
__version__: str
display: DisplayInterface
engine: Any
kepocoVGA: Any
math: Any
old_Driver: Any
ones: bytes
repeats: int
root: Any
stat: Any
sys: Any
ticks_us: Any
vga_mode: int
zeros: bytes
