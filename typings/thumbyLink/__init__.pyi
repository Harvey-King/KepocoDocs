"""Generated from supplied thumbyLink.py; source SHA-256 a332dfa2886df1de615a071fe51194d9eec39d7d33beea1950bfbbd3320d2ccc.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from machine import Pin as Pin
from machine import UART as UART

class LinkClass:
    'Source class thumbyLink.py:57. Backend-dependent branches are merged for editing; consult firmware notes.'
    initialized: bool
    rxPin: Pin
    sent: bool
    timeAtLastSend: Any
    timeout: int
    uart: UART

    def __init__(self) -> None:
        'Source-declared method: __init__(self).\nSource: thumbyLink.py:58. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init(self) -> None:
        'Source-declared method: init(self).\nSource: thumbyLink.py:63. Editor-only hints; not a hardware execution guarantee.'
        ...

    def send(self, data: Any) -> bool | None:
        'Physical branch sends up to 512 bytes and returns success/failure. Emulator/colour branches are no-ops returning None.\nSource: thumbyLink.py:78. Editor-only hints; not a hardware execution guarantee.'
        ...

    def receive(self) -> bytes | None:
        'Physical branch receives a checked packet or None. Emulator/colour branches are no-ops returning None.\nSource: thumbyLink.py:131. Editor-only hints; not a hardware execution guarantee.'
        ...
IS_EMULATOR: bool
IS_THUMBY_COLOR: Any
IS_THUMBY_COLOR_LINUX: Any
__version__: str
emulator: Any
link: LinkClass
sys: Any
ticks_diff: Any
ticks_ms: Any
