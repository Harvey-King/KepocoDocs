"""Generated from supplied kepocoDisplayDriver.py; source SHA-256 ae491095a1c2d4259cc06d3543324f787ec0096ba530822769c1ccad4f7d6dd6.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]

class DisplayDriver:
    'Source class kepocoDisplayDriver.py:3. Backend-dependent branches are merged for editing; consult firmware notes.'
    height: int
    max_x: Any
    max_y: Any
    width: int

    def __init__(self, width: int, height: int) -> None:
        'Source-declared method: __init__(self, width: int, height: int).\nSource: kepocoDisplayDriver.py:5. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init_display(self) -> None:
        'Source-declared method: init_display(self).\nSource: kepocoDisplayDriver.py:11. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweroff(self) -> None:
        'Source-declared method: poweroff(self).\nSource: kepocoDisplayDriver.py:14. Editor-only hints; not a hardware execution guarantee.'
        ...

    def poweron(self) -> None:
        'Source-declared method: poweron(self).\nSource: kepocoDisplayDriver.py:17. Editor-only hints; not a hardware execution guarantee.'
        ...

    def contrast(self, contrast: int) -> None:
        'Source-declared method: contrast(self, contrast).\nSource: kepocoDisplayDriver.py:20. Editor-only hints; not a hardware execution guarantee.'
        ...

    def invert(self, invert: Any) -> None:
        'Source-declared method: invert(self, invert).\nSource: kepocoDisplayDriver.py:23. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeGreyscale(self) -> None:
        'Source-declared method: setModeGreyscale(self).\nSource: kepocoDisplayDriver.py:26. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeMono(self) -> None:
        'Source-declared method: setModeMono(self).\nSource: kepocoDisplayDriver.py:29. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeTinted(self, red: int, green: int, blue: int) -> None:
        'Source-declared method: setModeTinted(self, red, green, blue).\nSource: kepocoDisplayDriver.py:32. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setModeRGB(self) -> None:
        'Source-declared method: setModeRGB(self).\nSource: kepocoDisplayDriver.py:35. Editor-only hints; not a hardware execution guarantee.'
        ...

    def enableVGA(self, transferBuffer: Any) -> Any:
        'Source-declared method: enableVGA(self, transferBuffer).\nSource: kepocoDisplayDriver.py:38. Editor-only hints; not a hardware execution guarantee.'
        ...

    def show(self) -> None:
        'Source-declared method: show(self).\nSource: kepocoDisplayDriver.py:41. Editor-only hints; not a hardware execution guarantee.'
        ...

    def brightness(self, setting: int) -> None:
        'Source-declared method: brightness(self, setting).\nSource: kepocoDisplayDriver.py:44. Editor-only hints; not a hardware execution guarantee.'
        ...

    def fill(self, colour: int) -> None:
        'Source-declared method: fill(self, colour: int).\nSource: kepocoDisplayDriver.py:48. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoDisplayDriver.py:52. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawEllispe(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawEllispe(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoDisplayDriver.py:86. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoDisplayDriver.py:90. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawRectangle(self, x: int, y: int, width: int, height: int, colour: int) -> None:
        'Source-declared method: drawRectangle(self, x: int, y: int, width: int, height: int, colour: int).\nSource: kepocoDisplayDriver.py:96. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setPixel(self, x: int, y: int, colour: int) -> None:
        'Source-declared method: setPixel(self, x: int, y: int, colour: int).\nSource: kepocoDisplayDriver.py:102. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getPixel(self, x: int, y: int) -> None:
        'Source-declared method: getPixel(self, x: int, y: int).\nSource: kepocoDisplayDriver.py:105. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawHLine(self, x: int, y: int, width: int, colour: int) -> None:
        'Source-declared method: drawHLine(self, x: int, y: int, width: int, colour: int).\nSource: kepocoDisplayDriver.py:109. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawVLine(self, x: int, y: int, height: int, colour: int) -> None:
        'Source-declared method: drawVLine(self, x: int, y: int, height: int, colour: int).\nSource: kepocoDisplayDriver.py:115. Editor-only hints; not a hardware execution guarantee.'
        ...

    def drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int) -> None:
        'Source-declared method: drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int).\nSource: kepocoDisplayDriver.py:122. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blit(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int) -> None:
        'Source-declared method: blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int).\nSource: kepocoDisplayDriver.py:147. Editor-only hints; not a hardware execution guarantee.'
        ...

    def blitWithMask(self, src: Any, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask: Any) -> None:
        'Source-declared method: blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask).\nSource: kepocoDisplayDriver.py:150. Editor-only hints; not a hardware execution guarantee.'
        ...

    def calibrate(self) -> None:
        'Source-declared method: calibrate(self).\nSource: kepocoDisplayDriver.py:153. Editor-only hints; not a hardware execution guarantee.'
        ...
math: Any
