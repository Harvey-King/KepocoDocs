# Archived firmware compatibility audit

[Overview](readme.md) · [Getting started](GETTING_STARTED.md) · [Features](FEATURE_GUIDE.md) · [API reference](API_REFERENCE.md) · [Firmware notes](FIRMWARE_NOTES.md) · [USB workflow](USB_WORKFLOW.md)

## Scope and evidence

This audit covers the archived source preserved under [`source-library/`](source-library/), without importing/executing its modules or modifying the original archive. Citations below use original filenames and line numbers within `source-library/`. The root-level `swerve.py` is a game, not firmware.

**Performed:** source reading, AST inspection where parsable, and in-memory desktop-Python `compile(..., "exec")` syntax checks of these 17 files: `kepoco.py`, `thumby.py`, `thumbyGraphics.py`, `thumbyButton.py`, `thumbySprite.py`, `thumbyAudio.py`, `thumbyLink.py`, `thumbySaves.py`, `thumbyHardware.py`, `kepocoDisplayDriver.py`, `kepocoDisplayST77xx.py`, `kepocoVGA.py`, `kepocoConfig.py`, `thumbyGrayscale.py`, `dummyScreen.py`, `ssd1306.py`, `demo.py`. Also read `kepoco.cfg` and `credits.txt`.

**Result:** desktop syntax compilation passed for 15 files; `kepocoVGA.py:223` failed with “Generator expression must be parenthesized”; `dummyScreen.py:54` failed with “‘return’ outside function”. AST parsing alone does not catch the latter compiler error. These checks do not evaluate imports, annotations, decorators, GPIO, PIO, filesystem initialization or MicroPython native/viper compilation.

**Not performed by the archive audit:** device/emulator execution of the archived modules, installed-firmware verification, flashing, GPIO/audio/link/VGA tests, display timing or rendering validation. Findings described as source defects are statically evidenced; the exact exception on a particular MicroPython build remains untested. Editor completion and host/mock tests cannot establish firmware compatibility.

The API-reference generator may neutralize only the bad VGA function-body line **in memory** so the remaining declarations can be indexed. That is an indexing workaround, explicitly recorded by the generator, not repaired firmware or evidence that the original file runs. The archived `source-library/` reference copies must retain the unmodified source.

## Separate installed-runtime evidence

Prior USB verification used the handheld’s existing **MicroPython 1.29.0 KEPOCO build**, not this archive. The display reported **72×40**; the SWERVE upload was verified by reading the remote file back; 60 gameplay frames and title/crash drawing executed. Physical controls, visible image quality, long-session playability and automatic menu registration were not visually verified. No firmware was flashed or startup files changed. See [USB workflow](USB_WORKFLOW.md#prior-real-device-verification).

These results do not invalidate the archive’s static defects or show that the archive can be installed unchanged. Compare the installed runtime with the archive before attributing an archive finding to your device.

## Runtime selection is source-declared, not board identification

| Source branch | Declared route | Caveat |
|---|---|---|
| Hardware ID 10 | Comment labels Kent Kepoco v1.3; `ST7789CompatDriver(72, 40, ...)`; `swC` supplied | `thumbyHardware.py:103–110`; not a detected board in this audit |
| Hardware ID 9 | Comment labels Kent Kepoco v1.0–v1.2; `ST7735CompatDriver(72, 40, ...)`; `swC` supplied | `thumbyHardware.py:111–118`; not hardware-tested |
| Other ID ≥1 | `SSD1306()`; `swC=None`, `i2c=None` | `thumbyHardware.py:119–124`; facade import and mode incompatibilities below |
| ID 0 | `DummyScreen(72, 40)`; `swC=None` | Name not imported in this branch (`thumbyHardware.py:125–130`) |
| Thumby Color / Linux machine string | `DummyScreen(72, 40)` | `thumbyHardware.py:27–28,37–70`; dummy source is broken and button code references absent `swC` |

The code uses `sys.implementation._machine` string tests and an `emulator` import probe, not a universal hardware capability registry (`kepoco.py:29–37`; `thumbyHardware.py:27–34`). The standard hardware branch probes ID pins and initializes the chosen display at import (`thumbyHardware.py:85–101,137`). Do not transplant its pinout to another board merely because the processor is similar.

## Startup blockers and high-priority mismatches

| Finding | Evidence and consequence | Practical boundary |
|---|---|---|
| Config reader/file mismatch | Reader splits every line on `=` and catches only `OSError` outside the loop (`kepocoConfig.py:44–53`). Supplied `kepoco.cfg:1` is one comma-separated record. If that file is found in the target working directory, unpacking cannot produce `k, v`; initialization is expected to fail with `ValueError`. | Do not upload the supplied cfg unchanged alongside this reader. Correct format belongs in a separate target copy after review, never by silently editing the dump. |
| Conditional C button, unconditional facade import | `buttonC` is defined only under `if swC` (`thumbyButton.py:100–102`); both facades import it unconditionally (`kepoco.py:51`; `thumby.py:48`). `swC=None` on SSD1306/ID0 branches (`thumbyHardware.py:122,129`). Color/Linux input imports `engine_io`, not `swC`, but later evaluates `if swC` (`thumbyButton.py:37–40,100`). | Even games importing only A/B can fail while the facade imports C. Fixes must be made in reviewed firmware, not hidden by optimistic typings. |
| Undefined annotation name | `DisplayInterface.__init__(self, driver: DisplayDriver)` uses `DisplayDriver` without an import or definition in `thumbyGraphics.py:1–16`. | Desktop syntax compilation passes, but normal eager annotation evaluation needs that name. MicroPython annotation handling must be verified on the target. |
| Runtime-provided compiler names assumed | `@micropython.native` appears without an explicit `import micropython` (`thumbyGraphics.py:80`, `thumbyButton.py:51`); `const` and viper pointer names are also used in backend source (`kepocoDisplayST77xx.py:265–268,298–302`; `ssd1306.py:40–42`). | These are firmware/runtime assumptions, not ordinary CPython modules. Verify provision of names/compiler support; do not execute the original source on the PC. |
| Broken dummy module | Top-level `return` at `dummyScreen.py:54` is rejected by the host compiler. Constructor also reads undefined `external_vcc` and `root` (`dummyScreen.py:62,75`); font method calls `stat` without an import (`dummyScreen.py:98–106`). | Simulator/fallback routes referencing this dump are not established as working. |
| ID0 fallback has missing driver name | `DummyScreen` is imported only in the preceding Color/Linux branches but used in the mutually exclusive standard ID0 branch (`thumbyHardware.py:47,66,125–130`). | Static name-resolution defect if ID0 route is reached unchanged. |
| VGA syntax error | `sorted` receives an unparenthesized generator together with `key=` (`kepocoVGA.py:223`); host AST and compilation fail. | `thumbyGraphics.py:237–248` imports VGA upon detection and catches only `OSError`, not syntax failures. Passing refresh 60 does not bypass parsing the module. |

## Graphics behavior and portability

- **`getPixel` loses the result:** wrapper calls the driver but omits `return` (`thumbyGraphics.py:127–129`). If the driver succeeds, the wrapper returns `None`, not a colour. A driver-level read is backend-specific and not a universal replacement.
- **Exact spelling is part of this snapshot:** methods are `drawEllispe` and `drawFilledEllispe` (`thumbyGraphics.py:115–121`). No corrected aliases are declared. ST77xx subclasses inherit the base outline ellipse, which raises `NotImplementedError` (`kepocoDisplayDriver.py:86–87`; `kepocoDisplayST77xx.py:8,262,730,1041`). Base filled ellipses use literal colour `2` for an odd-size centre line instead of the requested `colour` (`kepocoDisplayDriver.py:68–69,83–84`).
- **Mode mismatch on SSD1306:** the interface calls `setModeMono`, `setModeGreyscale`, `setModeTinted` (`thumbyGraphics.py:49–75`). AST inspection of the supplied `SSD1306` class found no methods with those names and no base class (`ssd1306.py:115`). `thumbyGrayscale` immediately calls the grayscale wrapper (`thumbyGrayscale.py:38`), so importing that compatibility layer is not necessarily safe on this backend. ST7735/ST7789 declare all three mode methods (`kepocoDisplayST77xx.py:743–751,1054–1062`).
- **Text buffer concern:** `drawText` calls `memoryview(stringToPrint)` (`thumbyGraphics.py:163`). Ordinary CPython `str` is not a byte buffer; target acceptance of `str` is not proven here. Start with ASCII bytes on a working target. The glyph check accepts negative indices for non-newline control bytes because it only checks `co < font_glyphcnt` after subtracting 0x20 (`thumbyGraphics.py:168–177`). Avoid other control characters.
- **Font import dependency:** interface construction immediately reads `/lib/font5x7.bin` (`thumbyGraphics.py:23,135–145,253`). Linux root is discovered later but not prepended to this interface font path (`thumbyGraphics.py:203–208`). Do not assume that an asset-free game avoids this library import dependency.
- **Frame cap is not throughput:** `setFPS` clamps to 0–60; `update` shows before waiting, polls buttons during the millisecond wait and records ticks at the end (`thumbyGraphics.py:81–98`). Zero disables pacing. Actual performance depends on target and driver.
- **Base line implementation:** horizontal/vertical length uses `abs(delta)` without the endpoint increment; reversed diagonal paths assign `y0, y1 = y1, x0` (`kepocoDisplayDriver.py:126–145`). ST77xx declares its own `drawLine` (`kepocoDisplayST77xx.py:442`), so do not attribute base-line behavior to every driver.
- **ST77xx alignment typo:** vertical offset branches inspect `alignX` for `top`/`bottom` instead of `alignY` (`kepocoDisplayST77xx.py:288–296`). Relevant to custom driver construction, not proof of a visible fault with default centered drivers.
- **Colour names differ in VGA internals:** VGA defines `WHITE=3`, `LIGHT=2`, `DARK=1` (`kepocoVGA.py:41–45`), whereas public display constants are WHITE=1, DARKGRAY=2, LIGHTGRAY=3 (`thumbyGraphics.py:11–14`). These are separate namespaces; do not copy backend constants into game code as public colour values.

## Configuration, storage and helper defects

- Preserve **`updateBirghtness(newval)`**, the callback's exact misspelling (`kepocoConfig.py:7–9,30`). `Configuration.getValues` falls through to undefined `Nones` for settings lacking options/values (`kepocoConfig.py:126–137`), such as `lastgame` (`kepocoConfig.py:21–24`).
- Configuration assignment normalizes the stored index with modulo, but calls `onchange` using the original `value` for indexing or passing (`kepocoConfig.py:63–68`). Out-of-range brightness assignment can write the cfg and then raise. Use valid declared indices, not arbitrary brightness values, when assigning `settings["brightness"]`.
- Config load does not invoke callbacks (`kepocoConfig.py:42–53`). Audio separately reads comma-format `/thumby.cfg` (`thumbyAudio.py:65–71`); SSD1306 brightness separately reads `thumby.cfg` (`ssd1306.py:157–168`). Do not assume `kepoco.cfg` automatically initializes all subsystems consistently.
- Save backup recovery calls `self.write(False)`, but the class declares `save`, not `write` (`thumbySaves.py:87–99,145`). If persistent JSON is missing/invalid and valid backup JSON is loaded, the recovery branch can fail instead of restoring it.
- Linux `TimerDummy` has no `ONE_SHOT`, although `audio.play` references it (`thumbyAudio.py:46–53,102–109`). Linux PWM methods are no-ops (`thumbyHardware.py:53–63`); method presence is not audible output.
- Color/Linux/emulator link `send` and `receive` are empty implementations (`thumbyLink.py:37–52`). They must not be documented as working multiplayer transports on those branches.
- `demo` unconditionally assigns `buttonC.pressed` before its main `try` (`demo.py:41,53`), restores `display.framerate` rather than `frameRate` (`demo.py:127`; `thumbyGraphics.py:21,82`), and accepts a `duration` argument not used in its body (`demo.py:3–152`). `record` restoration has no enclosing `finally` (`demo.py:194–220`); exceptions can leave button/display monkeypatches active. Its script error handler uses undefined `err`, `gamePath`, and `sleep_ms` (`demo.py:226–241`). Treat demo utilities as unverified helpers, not a safe launcher.
- `updateButtons` is defined twice with the same body (`thumbyButton.py:137–145`). This is redundant rather than evidence of different behavior.

## Safe next verification steps

1. Preserve this dump and its manifest; compare actual installed firmware rather than assuming it matches the downloaded files.
2. On an already configured target, record firmware identification, traceback, logical display dimensions and selected driver. Do not import the dump on desktop Python to obtain these values.
3. Resolve startup blockers in a separate reviewed firmware copy before attempting game behavior tests. No firmware changes were made by this audit.
4. Smoke-test A/B and directions, rectangle rendering and a byte-text probe; then verify sprites, modes, saves, audio and link separately only when relevant. VGA initialization writes hardware registers and configures PIO (`kepocoVGA.py:256–280`), so it is not a harmless feature probe.
5. Keep `typings/`, the VS Code extension and documentation on the PC. Editor commands open guides/reference or configure the current project; they do not upload games, flash firmware, repair runtime defects, or install the USB runner/tasks. The repository’s separate [USB tasks](USB_WORKFLOW.md) run or upload game files using the installed runtime.

## Origin notices

The facade and core Thumby files carry original attribution and GPL v3-or-later notices (`kepoco.py:5–21`; `thumbyButton.py:3–19`; `thumbySaves.py:4–20`); SSD1306 carries a GPL v3-or-later notice (`ssd1306.py:4–15`), and the grayscale layer attributes Keith Greenhow (`thumbyGrayscale.py:3–20`). Preserve origin/license material when redistributing these sources or derivatives and review obligations for the particular distribution. No conclusion about the license of novel stubs or editor tooling follows just from these source headers.
