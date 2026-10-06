"""Generated from supplied kepocoConfig.py; source SHA-256 3ce182cc6aa6fde8355e28b47caf1a90840c1eba49867daa306889082635ba8f.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]

class Configuration:
    'Source class kepocoConfig.py:12. Backend-dependent branches are merged for editing; consult firmware notes.'
    _index2key: Any
    _key2index: Any
    _options: Any
    _settings: dict[Any, Any]

    def __init__(self) -> None:
        'Source-declared method: __init__(self).\nSource: kepocoConfig.py:42. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __getitem__(self, key: str | int) -> Any:
        'Source-declared method: __getitem__(self, key).\nSource: kepocoConfig.py:55. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __setitem__(self, key: str | int, value: Any) -> None:
        'Source-declared method: __setitem__(self, key, value).\nSource: kepocoConfig.py:58. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __getattr__(self, key: str | int) -> Any:
        'Source-declared method: __getattr__(self, key).\nSource: kepocoConfig.py:70. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getOption(self, key: str | int) -> Any:
        'Source-declared method: getOption(self, key).\nSource: kepocoConfig.py:79. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getValue(self, key: str | int) -> Any:
        'Source-declared method: getValue(self, key).\nSource: kepocoConfig.py:87. Editor-only hints; not a hardware execution guarantee.'
        ...

    def items(self) -> Any:
        'Source-declared method: items(self).\nSource: kepocoConfig.py:93. Editor-only hints; not a hardware execution guarantee.'
        ...

    def keys(self) -> Any:
        'Source-declared method: keys(self).\nSource: kepocoConfig.py:96. Editor-only hints; not a hardware execution guarantee.'
        ...

    def values(self) -> Any:
        'Source-declared method: values(self).\nSource: kepocoConfig.py:99. Editor-only hints; not a hardware execution guarantee.'
        ...

    def options(self) -> Any:
        'Source-declared method: options(self).\nSource: kepocoConfig.py:102. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __len__(self) -> Any:
        'Source-declared method: __len__(self).\nSource: kepocoConfig.py:105. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def toKey(cls, key: str | int) -> str:
        'Source-declared method: toKey(cls, key).\nSource: kepocoConfig.py:109. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def settings(cls) -> list[str]:
        'Source-declared method: settings(cls).\nSource: kepocoConfig.py:118. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def allSettings(cls) -> list[str]:
        'Source-declared method: allSettings(cls).\nSource: kepocoConfig.py:122. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def getOptions(cls, key: str | int) -> Any:
        'Source-declared method: getOptions(cls, key).\nSource: kepocoConfig.py:126. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def getValues(cls, key: str | int) -> Any:
        'WARNING: the final fallback uses the undefined name Nones in the supplied file. That branch raises NameError.\nSource: kepocoConfig.py:131. Editor-only hints; not a hardware execution guarantee.'
        ...

    @classmethod
    def getShortName(cls, key: str | int) -> Any:
        'Source-declared method: getShortName(cls, key).\nSource: kepocoConfig.py:140. Editor-only hints; not a hardware execution guarantee.'
        ...

    def __repr__(self) -> Any:
        'Source-declared method: __repr__(self).\nSource: kepocoConfig.py:143. Editor-only hints; not a hardware execution guarantee.'
        ...

def updateAudio(newval: Any) -> None:
    'Source-declared function: updateAudio(newval).\nSource: kepocoConfig.py:2. Editor-only hints; not a hardware execution guarantee.'
    ...

def updateBirghtness(newval: Any) -> None:
    'Source-declared function: updateBirghtness(newval).\nSource: kepocoConfig.py:7. Editor-only hints; not a hardware execution guarantee.'
    ...
settings: Configuration
