"""Generated from supplied ssd1306.py; source SHA-256 53190af3773ab6fc60edc244205d16db2411dfb79d48b25ea05b4f652842281a.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from thumbyHardware import HWID as HWID
from machine import Pin as Pin
from machine import SPI as SPI
from thumbyAudio import audio as audio
from thumbyButton import buttonA as buttonA
from thumbyButton import buttonB as buttonB
from thumbyButton import buttonD as buttonD
from thumbyButton import buttonL as buttonL
from thumbyButton import buttonR as buttonR
from thumbyButton import buttonU as buttonU
from machine import idle as idle
from machine import mem32 as mem32
from utime import sleep_ms as sleep_ms
from utime import sleep_us as sleep_us
from utime import ticks_diff as ticks_diff
from utime import ticks_ms as ticks_ms

class SSD1306:
    'Source class ssd1306.py:115. Backend-dependent branches are merged for editing; consult firmware notes.'
    BLACK: int
    DARKGRAY: int
    LIGHTGRAY: int
    WHITE: int
    _brightness: int
    _contrast: bytearray
    _contrastSrc: bytearray
    _cs: Pin
    _dc: Pin
    _pendingCmds: bytearray
    _res: Pin
    _spi: SPI
    _state: Any
    _subframes: Any
    buffer: Any
    display: Any
    drawBuffer: bytearray
    font_bmap: bytearray
    font_glyphcnt: Any
    font_height: int
    font_space: int
    font_width: int
    frameRate: float
    height: Any
    lastUpdateEnd: Any
    max_x: Any
    max_y: Any
    pages: Any
    shading: Any
    width: Any

    def __init__(self) -> None:
        'Source-declared method: __init__(self).\nSource: ssd1306.py:123. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __enter__(self) -> Any:
        "allow use of 'with'\nSource: ssd1306.py:220. Editor-only hints; not a hardware execution guarantee."
        ...

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        'Source-declared method: __exit__(self, type, value, traceback).\nSource: ssd1306.py:223. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _initEmuScreen(self) -> None:
        'Source-declared method: _initEmuScreen(self).\nSource: ssd1306.py:228. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _clearEmuFunctions(self) -> None:
        'Source-declared method: _clearEmuFunctions(self).\nSource: ssd1306.py:236. Editor-only hints; not a hardware execution guarantee.'
        ...

    def reset(self) -> None:
        'Source-declared method: reset(self).\nSource: ssd1306.py:248. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: ssd1306.py:256. Editor-only hints; not a hardware execution guarantee.'
        ...

    def enableGrayscale(self) -> None:
        'Source-declared method: enableGrayscale(self).\nSource: ssd1306.py:293. Editor-only hints; not a hardware execution guarantee.'
        ...

    def disableGrayscale(self) -> None:
        'Source-declared method: disableGrayscale(self).\nSource: ssd1306.py:311. Editor-only hints; not a hardware execution guarantee.'
        ...

    def write_cmd(self, cmd: Any) -> None:
        'Source-declared method: write_cmd(self, cmd).\nSource: ssd1306.py:334. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweroff(self) -> None:
        'Source-declared method: poweroff(self).\nSource: ssd1306.py:361. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweron(self) -> None:
        'Source-declared method: poweron(self).\nSource: ssd1306.py:363. Editor-only hints; not a hardware execution guarantee.'
        ...

    def invert(self, invert: int) -> None:
        'Source-declared method: invert(self, invert: int).\nSource: ssd1306.py:368. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show(self) -> None:
        'Source-declared method: show(self).\nSource: ssd1306.py:378. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show_async(self) -> None:
        'Source-declared method: show_async(self).\nSource: ssd1306.py:391. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFPS(self, newFrameRate: float) -> None:
        'Source-declared method: setFPS(self, newFrameRate).\nSource: ssd1306.py:400. Editor-only hints; not a hardware execution guarantee.'
        ...

    def update(self) -> None:
        'Source-declared method: update(self).\nSource: ssd1306.py:404. Editor-only hints; not a hardware execution guarantee.'
        ...

    def brightness(self, c: int) -> None:
        'Source-declared method: brightness(self, c: int).\nSource: ssd1306.py:424. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _init_grayscale(self) -> None:
        'Source-declared method: _init_grayscale(self).\nSource: ssd1306.py:472. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _display_thread(self) -> None:
        'GPU (Gray Processing Unit) thread function\nSource: ssd1306.py:556. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _deinit_grayscale(self) -> None:
        'Source-declared method: _deinit_grayscale(self).\nSource: ssd1306.py:736. Editor-only hints; not a hardware execution guarantee.'
        ...

    def fill(self, colour: int) -> None:
        'Source-declared method: fill(self, colour: int).\nSource: ssd1306.py:746. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: ssd1306.py:759. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: ssd1306.py:835. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setPixel(self, x: int, y: int, colour: int) -> None:
        'Source-declared method: setPixel(self, x: int, y: int, colour: int).\nSource: ssd1306.py:844. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getPixel(self, x: int, y: int) -> int:
        'Source-declared method: getPixel(self, x: int, y: int).\nSource: ssd1306.py:862. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int) -> None:
        'Source-declared method: drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int).\nSource: ssd1306.py:877. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFont(self, fontFile: str, width: int, height: int, space: int) -> None:
        'Source-declared method: setFont(self, fontFile, width, height, space).\nSource: ssd1306.py:962. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawText(self, stringToPrint: str | bytes | bytearray | memoryview, x: int, y: int, colour: int) -> None:
        'Source-declared method: drawText(self, stringToPrint, x: int, y: int, colour: int).\nSource: ssd1306.py:974. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blit(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int) -> None:
        'Source-declared method: blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int).\nSource: ssd1306.py:1020. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawSprite(self, s: Any) -> None:
        'Source-declared method: drawSprite(self, s).\nSource: ssd1306.py:1119. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blitWithMask(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask: Any) -> None:
        'Source-declared method: blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask).\nSource: ssd1306.py:1123. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawSpriteWithMask(self, s: Any, m: Any) -> None:
        'Source-declared method: drawSpriteWithMask(self, s, m).\nSource: ssd1306.py:1222. Editor-only hints; not a hardware execution guarantee.'
        ...

    def calibrate(self) -> Any:
        'Source-declared method: calibrate(self).\nSource: ssd1306.py:1225. Editor-only hints; not a hardware execution guarantee.'
        ...
__version__: str
_thread: Any
array: Any
emulator: Any
floor: Any
modules: Any
sqrt: Any
stat: Any
