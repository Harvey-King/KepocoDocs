"""Generated from supplied kepocoVGA.py; source SHA-256 f29ea1a23a965c2e5218fc1d9a0c87408dd2c6d3539b1038782b63d54112b1ea.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
WARNING: original source syntax failure at line 223; index-only body placeholder used.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from kepocoDisplayDriver import DisplayDriver as DisplayDriver
from rp2 import PIO as PIO
from machine import Pin as Pin
from rp2 import StateMachine as StateMachine
from uctypes import addressof as addressof
from rp2 import asm_pio as asm_pio
from micropython import const as const
from machine import freq as freq
from machine import mem32 as mem32

class VGADriver(DisplayDriver):
    'Source class kepocoVGA.py:123. Backend-dependent branches are merged for editing; consult firmware notes.'
    H_buffer_line: Any
    H_buffer_line_address: Any
    paral_write_Hsync: StateMachine
    paral_write_RGB: StateMachine
    paral_write_Vsync: StateMachine
    refreshRate: float | None
    shift: Any
    show_physical_screen: Any
    visible_pix: int
    wrapped_driver: Any

    @classmethod
    def detect_vga(cls) -> bool:
        'Source-declared method: detect_vga(cls).\nSource: kepocoVGA.py:126. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def read_edid(cls) -> dict[str, Any] | None:
        'Derived from https://gist.github.com/shirriff/dd9e35da12879cf1c5ed9ed92ff704ec\nSource: kepocoVGA.py:137. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def supported_refresh_rates(cls) -> list[int]:
        'WARNING: the downloaded implementation has a syntax error at line 223. The stub describes the intended callable signature, not a repaired driver.\nSource: kepocoVGA.py:221. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __init__(self, wrapped_driver: Any, refreshRate: float | None = None) -> None:
        'Source-declared method: __init__(self, wrapped_driver, refreshRate=None).\nSource: kepocoVGA.py:228. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: kepocoVGA.py:256. Editor-only hints; not a hardware execution guarantee.'
        ...

    def resumeVGA(self) -> None:
        'Source-declared method: resumeVGA(self).\nSource: kepocoVGA.py:329. Editor-only hints; not a hardware execution guarantee.'
        ...

    def pauseVGA(self) -> None:
        'Source-declared method: pauseVGA(self).\nSource: kepocoVGA.py:342. Editor-only hints; not a hardware execution guarantee.'
        ...

    def enablePhysicalScreen(self, enabled: Any) -> None:
        'Source-declared method: enablePhysicalScreen(self, enabled).\nSource: kepocoVGA.py:366. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show(self) -> None:
        'Source-declared method: show(self).\nSource: kepocoVGA.py:370. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweroff(self) -> None:
        'Source-declared method: poweroff(self).\nSource: kepocoVGA.py:433. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweron(self) -> None:
        'Source-declared method: poweron(self).\nSource: kepocoVGA.py:437. Editor-only hints; not a hardware execution guarantee.'
        ...

    def contrast(self, contrast: int) -> None:
        'Source-declared method: contrast(self, contrast).\nSource: kepocoVGA.py:441. Editor-only hints; not a hardware execution guarantee.'
        ...

    def invert(self, invert: Any) -> None:
        'Source-declared method: invert(self, invert).\nSource: kepocoVGA.py:445. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeGreyscale(self) -> None:
        'Source-declared method: setModeGreyscale(self).\nSource: kepocoVGA.py:449. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeMono(self) -> None:
        'Source-declared method: setModeMono(self).\nSource: kepocoVGA.py:453. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeTinted(self, red: int, green: int, blue: int) -> None:
        'Source-declared method: setModeTinted(self, red, green, blue).\nSource: kepocoVGA.py:457. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeRGB(self) -> None:
        'Source-declared method: setModeRGB(self).\nSource: kepocoVGA.py:461. Editor-only hints; not a hardware execution guarantee.'
        ...

    def brightness(self, setting: int) -> None:
        'Source-declared method: brightness(self, setting).\nSource: kepocoVGA.py:464. Editor-only hints; not a hardware execution guarantee.'
        ...

    def fill(self, colour: int) -> None:
        'Source-declared method: fill(self, colour: int).\nSource: kepocoVGA.py:468. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoVGA.py:472. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawEllispe(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawEllispe(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoVGA.py:475. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoVGA.py:479. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoVGA.py:483. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setPixel(self, x: int, y: int, colour: int) -> None:
        'Source-declared method: setPixel(self, x: int, y: int, colour: int).\nSource: kepocoVGA.py:487. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getPixel(self, x: int, y: int) -> None:
        'Source-declared method: getPixel(self, x: int, y: int).\nSource: kepocoVGA.py:491. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawHLine(self, x: int, y: int, width: int, colour: int) -> None:
        'Source-declared method: drawHLine(self, x: int, y: int, width: int, colour: int).\nSource: kepocoVGA.py:495. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawVLine(self, x: int, y: int, height: int, colour: int) -> None:
        'Source-declared method: drawVLine(self, x: int, y: int, height: int, colour: int).\nSource: kepocoVGA.py:499. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int) -> None:
        'Source-declared method: drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int).\nSource: kepocoVGA.py:503. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blit(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int) -> None:
        'Source-declared method: blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int).\nSource: kepocoVGA.py:507. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blitWithMask(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask: Any) -> None:
        'Source-declared method: blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask).\nSource: kepocoVGA.py:511. Editor-only hints; not a hardware execution guarantee.'
        ...

    def calibrate(self) -> None:
        'Source-declared method: calibrate(self).\nSource: kepocoVGA.py:515. Editor-only hints; not a hardware execution guarantee.'
        ...

def paral_Hsync() -> None:
    'statemachine configuration\nsm0 is used for H sync signal\nSource: kepocoVGA.py:58. Editor-only hints; not a hardware execution guarantee.'
    ...

def paral_Vsync() -> None:
    '#\n#sm1 is used for V sync signal\nSource: kepocoVGA.py:78. Editor-only hints; not a hardware execution guarantee.'
    ...

def paral_RGB() -> None:
    'sm4 is used for RGB signal\nSource: kepocoVGA.py:107. Editor-only hints; not a hardware execution guarantee.'
    ...
BLACK: int
DARK: int
DMA1_Addr: int
DMA2_Addr: int
DMA3_Addr: int
DMA_CHAN_ABORT: int
DMA_Ctrl: int
DMA_Ctrl_Trigger: int
DMA_Len: int
DMA_Len_Trigger: int
DMA_MULTI_CHAN_TRIGGER: int
DMA_Read: int
DMA_Read_Trigger: int
DMA_Write: int
DMA_Write_Trigger: int
GREY_PINS: int
HSYNC_PIN: int
H_res: int
LIGHT: int
VSYNC_PIN: int
V_res: int
WHITE: int
array: Any
bit_per_pix: int
cos: Any
log: Any
pi: Any
pix_per_word: int
pixel_bitmask: int
sin: Any
usable_bits: int
words_per_line: int
