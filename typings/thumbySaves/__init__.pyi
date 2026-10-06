"""Generated from supplied thumbySaves.py; source SHA-256 98967a204a4c4503ce38b7f69716fa07ab3411aee02c549f7754f8f7838860cd.
Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.
Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.
"""

from typing import Any, Iterable, TypeAlias
BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]

class SavesClass:
    'Source class thumbySaves.py:49. Backend-dependent branches are merged for editing; consult firmware notes.'
    saveFile: Any
    savesPath: Any
    volatileDict: Any

    def __init__(self) -> None:
        'Source-declared method: __init__(self).\nSource: thumbySaves.py:50. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setName(self, subdir: str) -> None:
        'Select a game-specific save directory under /Saves and load its persistent or backup JSON.\nSource: thumbySaves.py:74. Editor-only hints; not a hardware execution guarantee.'
        ...

    def setItem(self, key: str, value: Any) -> None:
        'Set a value in the in-memory save dictionary. Use save() to persist. Keys beginning __b are reserved for byte metadata.\nSource: thumbySaves.py:104. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getItem(self, key: str) -> Any:
        'Get a saved value, decoding stored byte data if needed; returns None when missing.\nSource: thumbySaves.py:117. Editor-only hints; not a hardware execution guarantee.'
        ...

    def delItem(self, key: str) -> Any:
        'Delete entry in volatile dictionary\nSource: thumbySaves.py:127. Editor-only hints; not a hardware execution guarantee.'
        ...

    def hasItem(self, key: str) -> bool:
        'Check if save data entry exists in volatile dictionary\nSource: thumbySaves.py:136. Editor-only hints; not a hardware execution guarantee.'
        ...

    def save(self, backup: bool = False) -> None:
        'Write the in-memory dictionary to persistent.json. backup=True renames the prior file to backup.json first.\nSource: thumbySaves.py:145. Editor-only hints; not a hardware execution guarantee.'
        ...

    def getName(self) -> str:
        'Return the current save path\nSource: thumbySaves.py:170. Editor-only hints; not a hardware execution guarantee.'
        ...
IS_EMULATOR: bool
IS_THUMBY_COLOR: Any
IS_THUMBY_COLOR_LINUX: Any
JSONDump: Any
JSONLoad: Any
__version__: str
b64dec: Any
b64enc: Any
chdir: Any
emulator: Any
engine: Any
getcwd: Any
listdir: Any
mkdir: Any
remove: Any
rename: Any
root: Any
saveData: SavesClass
stat: Any
sys: Any
