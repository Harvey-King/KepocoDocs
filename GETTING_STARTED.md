# Getting started with Kepoco in this workspace

## Open the game project, not the firmware dump

Open **`C:/Users/Win1122h2/KepocoSwerve`** as the VS Code folder. The existing **`swerve.py`** is the game. Its target imports are inside `main()` (`swerve.py:176–180`); the entry point calls that function (`swerve.py:194–195`). Left/right steer, A starts/retries and boosts while held, and B exits (`swerve.py:183–191`).

The supplied library is in `C:/Users/Win1122h2/Downloads`. These documents describe that specific source snapshot, not a generic Thumby API or a guarantee about your installed firmware. Source citations below refer to files in that Downloads directory unless marked `swerve.py`.

**Editor typings are editor-only.** Keep `typings/` and `.pyi` files on the PC, out of device uploads. Do not add a fake `kepoco.py` beside the game: it could shadow the real firmware module. In this workspace, the intended editor configuration is `python.analysis.stubPath: "./typings"`; use the workspace's editor setup rather than importing the downloaded firmware into desktop Python. Completion describes source-declared members, not whether a particular board can execute them. See [FEATURE_GUIDE.md](FEATURE_GUIDE.md) and [FIRMWARE_NOTES.md](FIRMWARE_NOTES.md).

## Runtime requirements and deployment boundary

Use the Kepoco/MicroPython target or its configured emulator to run the game. `import kepoco` is not a passive desktop-library import: the supplied facade requests `machine.freq(250_000_000)`, imports hardware and instantiates graphics/audio/saves (`kepoco.py:39–60`). Hardware initialization occurs at module scope (`thumbyHardware.py:72–137`), and save initialization can create filesystem directories (`thumbySaves.py:49–70,173–174`).

The display interface copies its logical dimensions from the selected driver; the source's Kepoco HWID 9/10 branches instantiate 72×40 drivers (`thumbyGraphics.py:16–24`; `thumbyHardware.py:103–118`). This does not identify your actual board. Confirm the installed firmware, selected driver and reported dimensions before assuming compatibility.

Deploy `swerve.py` through the upload/run mechanism you already use for your device or emulator. No uploader, firmware version, or verified connection is established by this source audit. Do not overwrite firmware libraries or copy the entire Downloads folder to the target. Existing SWERVE uses its own rectangle-based font (`swerve.py:59–83`) and does not call library `drawText`; the library still loads `/lib/font5x7.bin` during display construction (`thumbyGraphics.py:23,135–145`).

## Target-runtime example: moving a rectangle

**For the target runtime only; not hardware-tested.** This avoids the audited `drawText` and `getPixel` problems. Poll each edge once per frame; use held input for continuous movement.

```python
from kepoco import display, buttonL, buttonR, buttonB

display.setFPS(30)
x = 0
while not buttonB.justPressed():
    x += int(buttonR.pressed()) - int(buttonL.pressed())
    x = max(0, min(display.width - 4, x))
    display.fill(display.BLACK)
    display.drawFilledRectangle(x, 16, 4, 4, display.WHITE)
    display.update()
```

`pressed()` reports current input; `justPressed()` consumes a latched press and updates its previous state (`thumbyButton.py:49–78`). `display.update()` shows the frame, waits for the requested cap and polls buttons during its millisecond wait (`thumbyGraphics.py:86–98`). `setFPS` clamps to 0–60; 0 disables its wait, not display rendering (`thumbyGraphics.py:81–98`). A requested cap is not measured FPS.

## Target-runtime example: a text probe

**For a known-working target only; not hardware-tested.** `drawText` iterates `memoryview(stringToPrint)` in this snapshot, so use a byte-oriented ASCII input for the initial probe rather than assuming ordinary `str` works (`thumbyGraphics.py:153–178`).

```python
from kepoco import display

display.fill(display.BLACK)
display.drawText(b"KEPOCO", 0, 0, display.WHITE)
display.update()
```

The default font is 5×7 with spacing 1 (`thumbyGraphics.py:23`). Font presence and backend mask support remain runtime prerequisites.

## If startup fails

Capture the exact exception, filename, line number, firmware identification and emulator/device name. First check the audit's import blockers: comma-format `kepoco.cfg`, conditional `buttonC`, missing display annotation name and broken fallback/VGA source. A green editor or successful host syntax check cannot repair those issues.

Nothing in this documentation task imports the original hardware modules, flashes firmware, or changes downloaded files. Host syntax checks are reported separately from unperformed device/emulator execution in the audit.

## Redistribution hygiene

Several downloaded files carry Thumby-origin GPL v3-or-later notices and original author attribution (`kepoco.py:5–21`; `thumbySprite.py:3–19`; `ssd1306.py:4–15`). If redistributing those sources or derivatives, preserve their notices/attribution and include the applicable license material; review the source-origin obligations for what you distribute. The supplied `credits.txt` is a credits list, not a substitute for license notices. This is an origin reminder, not a claim about the license of newly written editor tooling.
