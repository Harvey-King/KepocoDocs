"""Generated from supplied kepocoDisplayST77xx.py; source SHA-256 3885cd64823c1881b64ca93f5983cb9b22277009700ace9dd4d94f33cfc9d047.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from kepocoDisplayDriver import DisplayDriver as DisplayDriver
from machine import Pin as Pin
from machine import SPI as SPI
from uctypes import addressof as addressof
from utime import sleep_us as sleep_us

class AbstractST77xxDriver(DisplayDriver):
    'Source class kepocoDisplayST77xx.py:8. Backend-dependent branches are merged for editing; consult firmware notes.'
    CASET: int
    COLMOD: int
    DISPOFF: int
    DISPON: int
    DISSET5: int
    FRMCTR1: int
    FRMCTR2: int
    FRMCTR3: int
    GMCTRN1: int
    GMCTRP1: int
    INVCTR: int
    INVOFF: int
    INVON: int
    MADCTL: int
    NOP: int
    NORON: int
    PTLON: int
    PWCTR1: int
    PWCTR2: int
    PWCTR3: int
    PWCTR4: int
    PWCTR5: int
    PWCTR6: int
    RAMRD: int
    RAMWR: int
    RASET: int
    RDDID: int
    RDDST: int
    RDID1: int
    RDID2: int
    RDID3: int
    RDID4: int
    ROT_0DEG: int
    ROT_180DEG: int
    ROT_270DEG: int
    ROT_90DEG: int
    SLPIN: int
    SLPOUT: int
    SWRESET: int
    VMCTR1: int
    VSCRDEF: int
    VSCSAD: int
    WRDISBV: int
    _cmdBuffer: bytearray
    _rot: int
    _screen_lock: Any
    _windowLocData: bytearray
    cs: Any
    dc: Any
    rate: Any
    res: Any
    spi: Any

    def __init__(self, width: int, height: int, rotation: int, spi: SPI, dc: Pin, res: Pin, cs: Pin) -> None:
        'Source-declared method: __init__(self, width: int, height: int, rotation: int, spi: SPI, dc: Pin, res: Pin, cs: Pin).\nSource: kepocoDisplayST77xx.py:68. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: kepocoDisplayST77xx.py:86. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _full_clear(self, width: int, height: int, color: int) -> None:
        'Source-declared method: _full_clear(self, width, height, color).\nSource: kepocoDisplayST77xx.py:147. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweroff(self) -> None:
        'Source-declared method: poweroff(self).\nSource: kepocoDisplayST77xx.py:166. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweron(self) -> None:
        'Source-declared method: poweron(self).\nSource: kepocoDisplayST77xx.py:170. Editor-only hints; not a hardware execution guarantee.'
        ...

    def contrast(self, contrast: int) -> None:
        'Source-declared method: contrast(self, contrast).\nSource: kepocoDisplayST77xx.py:174. Editor-only hints; not a hardware execution guarantee.'
        ...

    def invert(self, invert: Any) -> None:
        'Source-declared method: invert(self, invert).\nSource: kepocoDisplayST77xx.py:179. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _reset(self) -> None:
        'Reset the device.\nSource: kepocoDisplayST77xx.py:184. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _setWindow(self, left: int, top: int, width: int, height: int) -> None:
        'Set a rectangular area for drawing a color to.\nSource: kepocoDisplayST77xx.py:195. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _writeCommand(self, command: int) -> None:
        'Write given command to the device.\nSource: kepocoDisplayST77xx.py:213. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _writeCommandAndData(self, command: int, data: Any) -> None:
        'Write given command to the device.\nSource: kepocoDisplayST77xx.py:226. Editor-only hints; not a hardware execution guarantee.'
        ...

    def brightness(self, setting: int) -> None:
        'Set display brightness, valid values 0 to 127\nSource: kepocoDisplayST77xx.py:244. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show(self) -> None:
        'Source-declared method: show(self).\nSource: kepocoDisplayST77xx.py:252. Editor-only hints; not a hardware execution guarantee.'
        ...

class ST77xxCompatDriver(AbstractST77xxDriver):
    'Source class kepocoDisplayST77xx.py:262. Backend-dependent branches are merged for editing; consult firmware notes.'
    _actualSize: Any
    _alignX: str
    _alignY: str
    _bank_offsets: bytearray
    _bg: int
    _buffSize: Any
    _dg: int
    _fg: int
    _lg: int
    _offsetL: Any
    _offsetT: Any
    _pixel_scale: Any
    buffer: Any
    drawBuffer: bytearray
    shading: Any

    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin, rot: int, actualSize: tuple[int, int], alignX: str = 'center', alignY: str = 'center') -> None:
        "Source-declared method: __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin, rot: int, actualSize: tuple[int, int], alignX='center', alignY='center').\nSource: kepocoDisplayST77xx.py:270. Editor-only hints; not a hardware execution guarantee."
        ...

    def fill(self, colour: int) -> None:
        'Source-declared method: fill(self, colour: int).\nSource: kepocoDisplayST77xx.py:299. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoDisplayST77xx.py:312. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoDisplayST77xx.py:389. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setPixel(self, x: int, y: int, colour: int) -> None:
        'Source-declared method: setPixel(self, x: int, y: int, colour: int).\nSource: kepocoDisplayST77xx.py:397. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getPixel(self, x: int, y: int) -> int:
        'Source-declared method: getPixel(self, x: int, y: int).\nSource: kepocoDisplayST77xx.py:417. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawHLine(self, x: int, y: int, width: int, colour: int) -> None:
        'Source-declared method: drawHLine(self, x: int, y: int, width: int, colour: int).\nSource: kepocoDisplayST77xx.py:434. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawVLine(self, x: int, y: int, height: int, colour: int) -> None:
        'Source-declared method: drawVLine(self, x: int, y: int, height: int, colour: int).\nSource: kepocoDisplayST77xx.py:438. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int) -> None:
        'Source-declared method: drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int).\nSource: kepocoDisplayST77xx.py:442. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blit(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int) -> None:
        'Source-declared method: blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int).\nSource: kepocoDisplayST77xx.py:528. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blitWithMask(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask: Any) -> None:
        'Source-declared method: blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask).\nSource: kepocoDisplayST77xx.py:629. Editor-only hints; not a hardware execution guarantee.'
        ...

class ST7735CompatDriver(ST77xxCompatDriver):
    'Source class kepocoDisplayST77xx.py:730. Backend-dependent branches are merged for editing; consult firmware notes.'
    _rowBuffer: bytearray
    _show_inner: Any
    _tint: Any
    show: Any

    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin) -> None:
        'Source-declared method: __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin).\nSource: kepocoDisplayST77xx.py:731. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: kepocoDisplayST77xx.py:738. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeMono(self) -> None:
        'Source-declared method: setModeMono(self).\nSource: kepocoDisplayST77xx.py:743. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeGreyscale(self) -> None:
        'Source-declared method: setModeGreyscale(self).\nSource: kepocoDisplayST77xx.py:747. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeTinted(self, red: int, green: int, blue: int) -> None:
        'Source-declared method: setModeTinted(self, red, green, blue).\nSource: kepocoDisplayST77xx.py:751. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _show_mono(self) -> None:
        'Source-declared method: _show_mono(self).\nSource: kepocoDisplayST77xx.py:767. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _show_grey(self) -> None:
        'Source-declared method: _show_grey(self).\nSource: kepocoDisplayST77xx.py:846. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _show_tinted(self) -> None:
        'Source-declared method: _show_tinted(self).\nSource: kepocoDisplayST77xx.py:943. Editor-only hints; not a hardware execution guarantee.'
        ...

class ST7789CompatDriver(ST77xxCompatDriver):
    'Source class kepocoDisplayST77xx.py:1041. Backend-dependent branches are merged for editing; consult firmware notes.'
    _rowBuffer: bytearray
    _show_inner: Any
    _tint: Any
    show: Any

    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin) -> None:
        'Source-declared method: __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin).\nSource: kepocoDisplayST77xx.py:1042. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: kepocoDisplayST77xx.py:1050. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeMono(self) -> None:
        'Source-declared method: setModeMono(self).\nSource: kepocoDisplayST77xx.py:1054. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeGreyscale(self) -> None:
        'Source-declared method: setModeGreyscale(self).\nSource: kepocoDisplayST77xx.py:1058. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeTinted(self, red: int, green: int, blue: int) -> None:
        'Source-declared method: setModeTinted(self, red, green, blue).\nSource: kepocoDisplayST77xx.py:1062. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _show_mono(self) -> None:
        'Source-declared method: _show_mono(self).\nSource: kepocoDisplayST77xx.py:1078. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _show_grey(self) -> None:
        'Source-declared method: _show_grey(self).\nSource: kepocoDisplayST77xx.py:1167. Editor-only hints; not a hardware execution guarantee.'
        ...

    def _show_tinted(self) -> None:
        'Source-declared method: _show_tinted(self).\nSource: kepocoDisplayST77xx.py:1271. Editor-only hints; not a hardware execution guarantee.'
        ...
_thread: Any
