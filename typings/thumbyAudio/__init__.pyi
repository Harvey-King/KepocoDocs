"""Generated from supplied thumbyAudio.py; source SHA-256 fc6dd47549dbf03d91b89f8ee8d78d9d450871af49be8dfbad1a0bc811514375.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]
from machine import Timer as Timer
from thumbyHardware import swBuzzer as swBuzzer

class TimerDummy:
    'Source class thumbyAudio.py:46. Backend-dependent branches are merged for editing; consult firmware notes.'

    def __init__(self) -> None:
        'Source-declared method: __init__(self).\nSource: thumbyAudio.py:47. Editor-only hints; not a hardware execution guarantee.'
        ...

    def init(self, period: Any, mode: Any, callback: Any) -> None:
        'Source-declared method: init(self, period, mode, callback).\nSource: thumbyAudio.py:50. Editor-only hints; not a hardware execution guarantee.'
        ...

class AudioClass:
    'Source class thumbyAudio.py:59. Backend-dependent branches are merged for editing; consult firmware notes.'
    dutyCycle: Any
    enabled: int
    pwm: Any
    timer: Timer

    def __init__(self, pwm: Any) -> None:
        'Source-declared method: __init__(self, pwm).\nSource: thumbyAudio.py:60. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setEnabled(self, setting: int = 1) -> None:
        'Set the audio to disabled, mid, or high output\nSource: thumbyAudio.py:75. Editor-only hints; not a hardware execution guarantee.'
        ...

    def stop(self, dummy: Any = None) -> None:
        'Stop audio.\nSource: thumbyAudio.py:84. Editor-only hints; not a hardware execution guarantee.'
        ...

    def set(self, freq: int) -> None:
        'Set the frequency and duty of the PWM audio if currently enabled.\nSource: thumbyAudio.py:92. Editor-only hints; not a hardware execution guarantee.'
        ...

    def play(self, freq: int, duration: int) -> None:
        'Play frequency freq (Hz) for duration milliseconds without waiting for completion. Requires a working audio backend.\nSource: thumbyAudio.py:102. Editor-only hints; not a hardware execution guarantee.'
        ...

    def playBlocking(self, freq: int, duration: int) -> None:
        'Play a tone and busy-wait for duration milliseconds, blocking gameplay. Requires a working audio backend.\nSource: thumbyAudio.py:113. Editor-only hints; not a hardware execution guarantee.'
        ...
IS_EMULATOR: bool
IS_THUMBY_COLOR: Any
IS_THUMBY_COLOR_LINUX: Any
__version__: str
audio: AudioClass
emulator: Any
engine: Any
root: Any
sys: Any
ticks_diff: Any
ticks_ms: Any
