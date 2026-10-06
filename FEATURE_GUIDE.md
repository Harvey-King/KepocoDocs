# Kepoco feature guide: the archived API

[Overview](readme.md) · [Getting started](GETTING_STARTED.md) · [Features](FEATURE_GUIDE.md) · [API reference](API_REFERENCE.md) · [Firmware notes](FIRMWARE_NOTES.md) · [USB workflow](USB_WORKFLOW.md)

This guide describes **source-declared** features, not device-tested capabilities. References use filenames under `source-library/` and their original line numbers. `source-library/` is the repository’s archived reference copy, not a replacement runtime. The generated [API reference](API_REFERENCE.md) provides the larger inventory; [firmware notes](FIRMWARE_NOTES.md) explain why some declared calls may fail.

## Imports and display model

The `kepoco` facade exports `Sprite`, six directional/action buttons plus an unconditional import of conditional `buttonC`, input helpers, `audio`, `link`, `saveData`, and `display` (`kepoco.py:49–60`). `thumby.py` is a parallel facade over the same modules (`thumby.py:46–57`), not a separate graphics implementation. `reset` is imported only on selected facade branches (`kepoco.py:43–47`). Do not assume it exists everywhere.

`display` is a `DisplayInterface` instance; `width` and `height` come from its driver. `display.driver` is the backend; `display.display` is a deprecated alias (`thumbyGraphics.py:16–24,253`). Use the public interface unless debugging a specific backend.

| Constant on `display` | Value |
|---|---:|
| `BLACK` | 0 |
| `WHITE` | 1 |
| `DARKGRAY` | 2 |
| `LIGHTGRAY` | 3 |

These exact values are declared in `thumbyGraphics.py:11–14`. They are not a monotonically ordered brightness scale. Four constants do not prove every backend supports four visible shades. No public `DisplayInterface.setModeRGB` is declared, even though the base driver has an RGB-mode method (`kepocoDisplayDriver.py:35–36`).

## Drawing and presenting frames

Signatures below omit `self`; positional parameter names and defaults follow the source.

| Method | Purpose / limitation | Source |
|---|---|---|
| `fill(colour)` | Clear the drawing buffer | `thumbyGraphics.py:103–105` |
| `setPixel(x, y, colour)` | Draw one pixel | `thumbyGraphics.py:123–125` |
| `getPixel(x, y)` | **Broken wrapper: no returned value** | `thumbyGraphics.py:127–129` |
| `drawLine(x0, y0, x1, y1, colour)` | Backend-dependent line drawing | `thumbyGraphics.py:131–133` |
| `drawRectangle(x, y, width, height, colour)` | Outline rectangle | `thumbyGraphics.py:111–113` |
| `drawFilledRectangle(x, y, width, height, colour)` | Filled rectangle | `thumbyGraphics.py:107–109` |
| `drawEllispe(x, y, width, height, colour)` | Exact misspelling; base driver raises `NotImplementedError` | `thumbyGraphics.py:119–121`; `kepocoDisplayDriver.py:86–87` |
| `drawFilledEllispe(x, y, width, height, colour)` | Exact misspelling; base implementation has colour issue | `thumbyGraphics.py:115–117`; `kepocoDisplayDriver.py:52–84` |
| `setFPS(newFrameRate)` | Clamp requested cap to 0–60; 0 means no wait | `thumbyGraphics.py:81–82,90–98` |
| `show()` | Present through driver; no interface frame wait | `thumbyGraphics.py:77–78` |
| `update()` | Present, pace frame, poll buttons during wait | `thumbyGraphics.py:86–98` |

Do not invent corrected names `drawEllipse` or `drawFilledEllipse`. Keep coordinates and dimensions within the logical screen when possible; behavior outside it belongs to the backend implementation.

### Text and fonts

- `setFont(fontFile, width=None, height=None, space=1)` appends `.bin` if missing, infers dimensions from a `fontWxH` filename when either dimension is omitted, and reads the whole font into memory (`thumbyGraphics.py:135–150`). Pass explicit dimensions for differently named files.
- `drawText(stringToPrint, x, y, colour)` uses the current font, treats newline as a new row, and iterates a `memoryview` of its argument (`thumbyGraphics.py:153–178`). Ordinary `str` acceptance must be checked on the actual MicroPython build. Initial ASCII probes can use `bytes` or `bytearray`; do not assume Unicode layout support.
- The default path is `/lib/font5x7.bin`, 5×7 with spacing 1 (`thumbyGraphics.py:23`). The game SWERVE has its own font, but importing the library still requires that default font.

### Sprites and buffers

`Sprite(width, height, bitmapData, x=0, y=0, key=-1, mirrorX=False, mirrorY=False)` accepts a `bytearray`, a filename string, or a two-plane tuple/list of matching-type bytearrays or filename strings (`thumbySprite.py:28–72`). A plain `bytes` input is not one of its accepted constructor branches. Each plane's frame storage is width times the number of eight-row pages (`thumbySprite.py:32–34`); choose positive dimensions and supply complete frames to avoid a zero `frameCount`.

Sprite position/transparency/mirroring are fields `x`, `y`, `key`, `mirrorX`, `mirrorY` (`thumbySprite.py:73–77`). `getFrame()` reports `currentFrame`; `setFrame(frame)` selects a nonnegative frame modulo `frameCount` (`thumbySprite.py:79–102`).

Drawing calls (`thumbyGraphics.py:180–194`):

```text
blit(src, x, y, width, height, key, mirrorX, mirrorY)
drawSprite(s)
blitWithMask(src, x, y, width, height, key, mirrorX, mirrorY, mask)
drawSpriteWithMask(s, m)
```

**Target-runtime example; not hardware-tested:**

```python
from kepoco import display, Sprite

# One 8-row column per byte: an 8 by 8 solid bitmap.
sprite = Sprite(8, 8, bytearray([255] * 8), x=8, y=16, key=-1)
display.fill(display.BLACK)
display.drawSprite(sprite)
display.update()
```

## Controls

`buttonL`, `buttonR`, `buttonU`, `buttonD`, `buttonA`, `buttonB` are constructed in both main input branches (`thumbyButton.py:81–95`). `buttonC` is constructed **only if `swC` is truthy**, then appended to action buttons (`thumbyButton.py:100–104`). This is an import hazard, not merely an optional control you can safely import everywhere.

Every `ButtonClass` declares `pressed()`, `justPressed()`, and `update()` (`thumbyButton.py:49–78`). `justPressed()` consumes a latched event and mutates previous-state tracking; poll it once per frame and reuse the result. Helpers are `inputPressed(buttons=allButtons)`, `inputJustPressed(buttons=allButtons)`, `dpadPressed()`, `dpadJustPressed()`, `actionPressed()`, `actionJustPressed()`, and module-level `updateButtons(buttons=allButtons)` (`thumbyButton.py:107–145`). The edge helpers use short-circuiting `any`, so they are not a per-button event queue.

## Audio, saves and linking

**Audio:** `audio.setEnabled(setting=1)` clamps to 0 or 1; `stop(dummy=None)`, `set(freq)`, `play(freq, duration)`, and `playBlocking(freq, duration)` are the actual methods (`thumbyAudio.py:73–126`). `play` schedules a timer callback, while `playBlocking` busy-waits against millisecond ticks even when disabled. Do not assume a speaker or emulator audio support from the API names. Linux's dummy timer lacks the `ONE_SHOT` used by `play` (`thumbyAudio.py:46–53,109`).

**Saves:** `saveData.setName(subdir)` selects a directory below `/Saves` (or Linux engine root); `setItem(key, value)`, `getItem(key)`, `delItem(key)`, `hasItem(key)`, `save(backup=False)`, `getName()` are declared (`thumbySaves.py:74–171`). `setItem` edits RAM; `save` writes JSON. Missing reads return `None`. Keys beginning `__b` are reserved for byte data (`thumbySaves.py:104–123`). Keep names simple; `setName` concatenates them into a filesystem path. The backup-recovery branch contains an undefined `write` method; see the audit.

**Link:** `link.init()`, `send(data)`, `receive()` are declared. On Color/Linux/emulator, `send` and `receive` are no-ops returning `None` (`thumbyLink.py:37–52`). The other branch configures UART, limits sends to 512 bytes, returns a boolean from `send`, and returns received checksum-validated data or no data (`thumbyLink.py:62–88,118–179`). Physical link support is not hardware-tested.

## Modes, configuration and specialist features

`poweroff()`, `poweron()`, `contrast(contrast)`, `invert(inverted)`, `flash()`, `brightness(setting)`, `calibrate()` forward to the driver; `flash` inverts, shows, then restores inversion without a second `show` (`thumbyGraphics.py:31–46,100–101,196–197`).

The preferred declared mode methods are `setModeMono()`, `setModeGreyscale()`, `setModeTinted(red, green, blue)` (`thumbyGraphics.py:68–75`). Deprecated aliases are `enableGrayscale()`, `disableGrayscale()`, `enableGreyscale()`, `disableGreyscale()`, `setColourTint(red, green, blue)` (`thumbyGraphics.py:48–66`). Backend support varies; the supplied SSD1306 class does not declare the mode methods expected by these wrappers. Importing `thumbyGrayscale` immediately calls `display.enableGrayscale()` (`thumbyGrayscale.py:23–38`).

Configuration is accessed separately with `from kepocoConfig import settings`, not `kepoco.settings`. `settings[key]` returns a raw stored value/index; `getOption(key)` resolves an option/value; `getValue(key)` resolves a numeric value where provided. Assignment writes `kepoco.cfg` and invokes callbacks (`kepocoConfig.py:55–91`). Declared keys are `audioenabled`, `lastgame`, `brightness`, `vga`, with default indices/values 1, `/Games/Evaluator/Evaluator.py`, 1, 1 respectively (`kepocoConfig.py:14–37`). The exact callback name is **`updateBirghtness(newval)`** (`kepocoConfig.py:7–9,30`), not `updateBrightness`. The supplied comma-format cfg does not match this reader.

VGA routing is chosen by `settings["vga"]`: positive values trigger I2C address probing, mode 2 requests physical-screen disable after a driver wrap (`thumbyGraphics.py:214–249`). This is source logic, not proof of connected VGA hardware. The source VGA file has a syntax failure; do not enable it without addressing that in the actual firmware. Demo recording/playback is a separate monkeypatching helper, not a game-loop API or a verified desktop runner (`demo.py:3–45,79–94,154–207`).


## Using these features on a device

Start with [Getting started](GETTING_STARTED.md), then use the repository’s [USB workflow](USB_WORKFLOW.md) to run saved game files. Editor hints and this archive inventory do not establish support on an installed runtime. The prior SWERVE device smoke test is documented separately; it did not test every API here or visually verify physical controls.
