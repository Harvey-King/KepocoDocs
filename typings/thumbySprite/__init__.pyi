"""Generated from supplied thumbySprite.py; source SHA-256 544b829c89309c5f0b8e1f907b1293efae53257c8b9dbb8f1f9366367c283dd3.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]

class Sprite:
    'Source class thumbySprite.py:26. Backend-dependent branches are merged for editing; consult firmware notes.'
    _shaded: bool
    _usesFile: bool
    bitmap: Any
    bitmapByteCount: int
    bitmapSource: BitmapData
    currentFrame: int
    file: Any
    files: tuple[Any, ...]
    frameCount: int
    height: int
    key: int
    mirrorX: bool | int
    mirrorY: bool | int
    width: int
    x: int
    y: int

    def __init__(self, width: int, height: int, bitmapData: BitmapData, x: int = 0, y: int = 0, key: int = -1, mirrorX: bool | int = False, mirrorY: bool | int = False) -> None:
        'Create a sprite from bytearray data or a filename. Two matching bitplanes may be supplied as a tuple/list. Frame byte size is width * ceil(height/8).\nSource: thumbySprite.py:28. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getFrame(self) -> int:
        'Source-declared method: getFrame(self).\nSource: thumbySprite.py:80. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setFrame(self, frame: int) -> None:
        'Select an animation frame modulo frameCount. Negative indices do not update the frame.\nSource: thumbySprite.py:84. Editor-only hints; not a hardware execution guarantee.'
        ...
__version__: str
stat: Any
