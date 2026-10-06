# Kepoco source-derived API reference

Generated from your downloaded sources. Exact spellings, parameter names and defaults are retained.
Type hints in typings are editor annotations, not guarantees of hardware support.
Backend branches are merged for discoverability; read FIRMWARE_NOTES.md before relying on them.

## Module index

- [demo](#demo)
- [dummyScreen](#dummyscreen)
- [kepoco](#kepoco)
- [kepocoConfig](#kepococonfig)
- [kepocoDisplayDriver](#kepocodisplaydriver)
- [kepocoDisplayST77xx](#kepocodisplayst77xx)
- [kepocoVGA](#kepocovga)
- [ssd1306](#ssd1306)
- [thumby](#thumby)
- [thumbyAudio](#thumbyaudio)
- [thumbyButton](#thumbybutton)
- [thumbyGraphics](#thumbygraphics)
- [thumbyGrayscale](#thumbygrayscale)
- [thumbyHardware](#thumbyhardware)
- [thumbyLink](#thumbylink)
- [thumbySaves](#thumbysaves)
- [thumbySprite](#thumbysprite)

## demo

Source: [source-library/demo.py](../source-library/demo.py).
SHA-256: `d99e4dcd13d99dbb86329adcae0668426f50d123d09d0e25d99ceba285f40ad4`.

- `demo(button_src: str | list[str], duration: int | None=None, run: str | None=None, rseed=3235823343, return_module: bool=False)` — Source-declared function. [demo.py:3]
- `record(run: str)` — Source-declared function. [demo.py:154]

## dummyScreen

Source: [source-library/dummyScreen.py](../source-library/dummyScreen.py).
SHA-256: `990007d7edc738f25c59d9c35674acde38274640e9d56260c06c37b50ad10341`.


### DummyScreen (dummyScreen.py:57)

- `__init__(self, width, height)` — Source-declared method; backend-specific implementation. [dummyScreen.py:58]
- `initEmuScreen(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:80]
- `init_display(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:83]
- `poweroff(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:86]
- `poweron(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:89]
- `contrast(self, contrast)` — Source-declared method; backend-specific implementation. [dummyScreen.py:92]
- `invert(self, invert)` — Source-declared method; backend-specific implementation. [dummyScreen.py:95]
- `setFont(self, fontFile, width, height, space)` — Source-declared method; backend-specific implementation. [dummyScreen.py:99]
- `setFPS(self, newFrameRate)` — Source-declared method; backend-specific implementation. [dummyScreen.py:109]
- `update(self)` — Push the buffer to the hardware display. [dummyScreen.py:114]
- `brightness(self, setting)` — Set display brightness, valid values 0 to 127 [dummyScreen.py:133]
- `fill(self, color: int)` — Fill the buffer with a given color. [dummyScreen.py:142]
- `setPixel(self, x: int, y: int, color: int)` — Source-declared method; backend-specific implementation. [dummyScreen.py:152]
- `getPixel(self, x: int, y: int)` — Source-declared method; backend-specific implementation. [dummyScreen.py:167]
- `drawLine(self, x1: int, y1: int, x2: int, y2: int, color: int)` — Draw a line from (x1, y1) to (x2, y2) in a given color- taken from MicroPython FrameBuf implementation [dummyScreen.py:181]
- `drawRectangle(self, x: int, y: int, width: int, height: int, color: int)` — Source-declared method; backend-specific implementation. [dummyScreen.py:238]
- `drawFilledRectangle(self, x: int, y: int, width: int, height: int, color: int)` — Fill a rectangle with top left corner (x, y) and size (width, height) in a given color. [dummyScreen.py:246]
- `drawText(self, stringToPrint: ptr8, x: int, y: int, color: int)` — Draw a string with top left corner (x, y) in a given color. [dummyScreen.py:283]
- `blit(self, sprtptr: ptr8, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int)` — Source-declared method; backend-specific implementation. [dummyScreen.py:336]
- `drawSprite(self, s)` — Draw a sprite to the screen [dummyScreen.py:391]
- `blitWithMask(self, sprtptr: ptr8, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, maskptr: ptr8)` — Source-declared method; backend-specific implementation. [dummyScreen.py:395]
- `drawSpriteWithMask(self, s, m)` — Source-declared method; backend-specific implementation. [dummyScreen.py:431]
- `reset(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:435]
- `show(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:440]
- `show(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:461]
- `show(self)` — Source-declared method; backend-specific implementation. [dummyScreen.py:465]

## kepoco

Source: [source-library/kepoco.py](../source-library/kepoco.py).
SHA-256: `2cb5452df0aba44052c63a7abad5910ecf6c428ad07be327a22a2bb3901a109b`.


## kepocoConfig

Source: [source-library/kepocoConfig.py](../source-library/kepocoConfig.py).
SHA-256: `3ce182cc6aa6fde8355e28b47caf1a90840c1eba49867daa306889082635ba8f`.


### Configuration (kepocoConfig.py:12)

- `__init__(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:42]
- `__getitem__(self, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:55]
- `__setitem__(self, key, value)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:58]
- `__getattr__(self, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:70]
- `getOption(self, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:79]
- `getValue(self, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:87]
- `items(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:93]
- `keys(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:96]
- `values(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:99]
- `options(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:102]
- `__len__(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:105]
- `toKey(cls, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:109]
- `settings(cls)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:118]
- `allSettings(cls)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:122]
- `getOptions(cls, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:126]
- `getValues(cls, key)` — WARNING: the final fallback uses the undefined name Nones in the supplied file. That branch raises NameError. [kepocoConfig.py:131]
- `getShortName(cls, key)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:140]
- `__repr__(self)` — Source-declared method; backend-specific implementation. [kepocoConfig.py:143]
- `updateAudio(newval)` — Source-declared function. [kepocoConfig.py:2]
- `updateBirghtness(newval)` — Source-declared function. [kepocoConfig.py:7]

## kepocoDisplayDriver

Source: [source-library/kepocoDisplayDriver.py](../source-library/kepocoDisplayDriver.py).
SHA-256: `ae491095a1c2d4259cc06d3543324f787ec0096ba530822769c1ccad4f7d6dd6`.


### DisplayDriver (kepocoDisplayDriver.py:3)

- `__init__(self, width: int, height: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:5]
- `init_display(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:11]
- `poweroff(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:14]
- `poweron(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:17]
- `contrast(self, contrast)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:20]
- `invert(self, invert)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:23]
- `setModeGreyscale(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:26]
- `setModeMono(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:29]
- `setModeTinted(self, red, green, blue)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:32]
- `setModeRGB(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:35]
- `enableVGA(self, transferBuffer)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:38]
- `show(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:41]
- `brightness(self, setting)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:44]
- `fill(self, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:48]
- `drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:52]
- `drawEllispe(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:86]
- `drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:90]
- `drawRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:96]
- `setPixel(self, x: int, y: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:102]
- `getPixel(self, x: int, y: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:105]
- `drawHLine(self, x: int, y: int, width: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:109]
- `drawVLine(self, x: int, y: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:115]
- `drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:122]
- `blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:147]
- `blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:150]
- `calibrate(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayDriver.py:153]

## kepocoDisplayST77xx

Source: [source-library/kepocoDisplayST77xx.py](../source-library/kepocoDisplayST77xx.py).
SHA-256: `3885cd64823c1881b64ca93f5983cb9b22277009700ace9dd4d94f33cfc9d047`.


### AbstractST77xxDriver (kepocoDisplayST77xx.py:8)

- `__init__(self, width: int, height: int, rotation: int, spi: SPI, dc: Pin, res: Pin, cs: Pin)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:68]
- `init_display(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:86]
- `_full_clear(self, width, height, color)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:147]
- `poweroff(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:166]
- `poweron(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:170]
- `contrast(self, contrast)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:174]
- `invert(self, invert)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:179]
- `_reset(self)` — Reset the device. [kepocoDisplayST77xx.py:184]
- `_setWindow(self, left: int, top: int, width: int, height: int)` — Set a rectangular area for drawing a color to. [kepocoDisplayST77xx.py:195]
- `_writeCommand(self, command: int)` — Write given command to the device. [kepocoDisplayST77xx.py:213]
- `_writeCommandAndData(self, command: int, data)` — Write given command to the device. [kepocoDisplayST77xx.py:226]
- `brightness(self, setting)` — Set display brightness, valid values 0 to 127 [kepocoDisplayST77xx.py:244]
- `show(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:252]

### ST77xxCompatDriver (kepocoDisplayST77xx.py:262)

- `__init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin, rot: int, actualSize: tuple[int, int], alignX='center', alignY='center')` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:270]
- `fill(self, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:299]
- `drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:312]
- `drawRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:389]
- `setPixel(self, x: int, y: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:397]
- `getPixel(self, x: int, y: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:417]
- `drawHLine(self, x: int, y: int, width: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:434]
- `drawVLine(self, x: int, y: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:438]
- `drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:442]
- `blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:528]
- `blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:629]

### ST7735CompatDriver (kepocoDisplayST77xx.py:730)

- `__init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:731]
- `init_display(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:738]
- `setModeMono(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:743]
- `setModeGreyscale(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:747]
- `setModeTinted(self, red, green, blue)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:751]
- `_show_mono(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:767]
- `_show_grey(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:846]
- `_show_tinted(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:943]

### ST7789CompatDriver (kepocoDisplayST77xx.py:1041)

- `__init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1042]
- `init_display(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1050]
- `setModeMono(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1054]
- `setModeGreyscale(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1058]
- `setModeTinted(self, red, green, blue)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1062]
- `_show_mono(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1078]
- `_show_grey(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1167]
- `_show_tinted(self)` — Source-declared method; backend-specific implementation. [kepocoDisplayST77xx.py:1271]

## kepocoVGA

Source: [source-library/kepocoVGA.py](../source-library/kepocoVGA.py).
SHA-256: `f29ea1a23a965c2e5218fc1d9a0c87408dd2c6d3539b1038782b63d54112b1ea`.

WARNING: original syntax failure at line 223; index-only body placeholder used. The source was not repaired.

### VGADriver (kepocoVGA.py:123)

- `detect_vga(cls)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:126]
- `read_edid(cls)` — Derived from https://gist.github.com/shirriff/dd9e35da12879cf1c5ed9ed92ff704ec [kepocoVGA.py:137]
- `supported_refresh_rates(cls)` — WARNING: the downloaded implementation has a syntax error at line 223. The stub describes the intended callable signature, not a repaired driver. [kepocoVGA.py:221]
- `__init__(self, wrapped_driver, refreshRate=None)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:228]
- `init_display(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:256]
- `resumeVGA(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:329]
- `pauseVGA(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:342]
- `enablePhysicalScreen(self, enabled)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:366]
- `show(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:370]
- `poweroff(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:433]
- `poweron(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:437]
- `contrast(self, contrast)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:441]
- `invert(self, invert)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:445]
- `setModeGreyscale(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:449]
- `setModeMono(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:453]
- `setModeTinted(self, red, green, blue)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:457]
- `setModeRGB(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:461]
- `brightness(self, setting)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:464]
- `fill(self, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:468]
- `drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:472]
- `drawEllispe(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:475]
- `drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:479]
- `drawRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:483]
- `setPixel(self, x: int, y: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:487]
- `getPixel(self, x: int, y: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:491]
- `drawHLine(self, x: int, y: int, width: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:495]
- `drawVLine(self, x: int, y: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:499]
- `drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:503]
- `blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:507]
- `blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:511]
- `calibrate(self)` — Source-declared method; backend-specific implementation. [kepocoVGA.py:515]
- `paral_Hsync()` — statemachine configuration sm0 is used for H sync signal [kepocoVGA.py:58]
- `paral_Vsync()` — # #sm1 is used for V sync signal [kepocoVGA.py:78]
- `paral_RGB()` — sm4 is used for RGB signal [kepocoVGA.py:107]

## ssd1306

Source: [source-library/ssd1306.py](../source-library/ssd1306.py).
SHA-256: `53190af3773ab6fc60edc244205d16db2411dfb79d48b25ea05b4f652842281a`.


### SSD1306 (ssd1306.py:115)

- `__init__(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:123]
- `__enter__(self)` — allow use of 'with' [ssd1306.py:220]
- `__exit__(self, type, value, traceback)` — Source-declared method; backend-specific implementation. [ssd1306.py:223]
- `_initEmuScreen(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:228]
- `_clearEmuFunctions(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:236]
- `reset(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:248]
- `init_display(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:256]
- `enableGrayscale(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:293]
- `disableGrayscale(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:311]
- `write_cmd(self, cmd)` — Source-declared method; backend-specific implementation. [ssd1306.py:334]
- `poweroff(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:361]
- `poweron(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:363]
- `invert(self, invert: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:368]
- `show(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:378]
- `show_async(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:391]
- `setFPS(self, newFrameRate)` — Source-declared method; backend-specific implementation. [ssd1306.py:400]
- `update(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:404]
- `brightness(self, c: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:424]
- `_init_grayscale(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:472]
- `_display_thread(self)` — GPU (Gray Processing Unit) thread function [ssd1306.py:556]
- `_deinit_grayscale(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:736]
- `fill(self, colour: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:746]
- `drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:759]
- `drawRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:835]
- `setPixel(self, x: int, y: int, colour: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:844]
- `getPixel(self, x: int, y: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:862]
- `drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:877]
- `setFont(self, fontFile, width, height, space)` — Source-declared method; backend-specific implementation. [ssd1306.py:962]
- `drawText(self, stringToPrint, x: int, y: int, colour: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:974]
- `blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int)` — Source-declared method; backend-specific implementation. [ssd1306.py:1020]
- `drawSprite(self, s)` — Source-declared method; backend-specific implementation. [ssd1306.py:1119]
- `blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask)` — Source-declared method; backend-specific implementation. [ssd1306.py:1123]
- `drawSpriteWithMask(self, s, m)` — Source-declared method; backend-specific implementation. [ssd1306.py:1222]
- `calibrate(self)` — Source-declared method; backend-specific implementation. [ssd1306.py:1225]

## thumby

Source: [source-library/thumby.py](../source-library/thumby.py).
SHA-256: `bd7c4a032fed705fdedb4949bd21fc503865c1c05c0cce5fc25cb1311051b70b`.


## thumbyAudio

Source: [source-library/thumbyAudio.py](../source-library/thumbyAudio.py).
SHA-256: `fc6dd47549dbf03d91b89f8ee8d78d9d450871af49be8dfbad1a0bc811514375`.


### TimerDummy (thumbyAudio.py:46)

- `__init__(self)` — Source-declared method; backend-specific implementation. [thumbyAudio.py:47]
- `init(self, period, mode, callback)` — Source-declared method; backend-specific implementation. [thumbyAudio.py:50]

### AudioClass (thumbyAudio.py:59)

- `__init__(self, pwm)` — Source-declared method; backend-specific implementation. [thumbyAudio.py:60]
- `setEnabled(self, setting=1)` — Set the audio to disabled, mid, or high output [thumbyAudio.py:75]
- `stop(self, dummy=None)` — Stop audio. [thumbyAudio.py:84]
- `set(self, freq)` — Set the frequency and duty of the PWM audio if currently enabled. [thumbyAudio.py:92]
- `play(self, freq, duration)` — Play frequency freq (Hz) for duration milliseconds without waiting for completion. Requires a working audio backend. [thumbyAudio.py:102]
- `playBlocking(self, freq, duration)` — Play a tone and busy-wait for duration milliseconds, blocking gameplay. Requires a working audio backend. [thumbyAudio.py:113]

## thumbyButton

Source: [source-library/thumbyButton.py](../source-library/thumbyButton.py).
SHA-256: `3335ac9611054d342758c8b5aea692aebd7a6f5efeb5c4abf41ade49357b3fc3`.


### ButtonClass (thumbyButton.py:43)

- `__init__(self, pin)` — Source-declared method; backend-specific implementation. [thumbyButton.py:44]
- `pressed(self)` — Source-declared method; backend-specific implementation. [thumbyButton.py:52]
- `pressed(self)` — Source-declared method; backend-specific implementation. [thumbyButton.py:56]
- `justPressed(self)` — Return a new or latched button edge and consume the latch. Read once per frame and store the result if multiple systems need it. [thumbyButton.py:61]
- `update(self)` — Latches a button press state to be returned later through justPressed [thumbyButton.py:74]
- `inputPressed(buttons=allButtons)` — Returns true if any buttons are currently pressed on the thumby. [thumbyButton.py:109]
- `inputJustPressed(buttons=allButtons)` — Returns true if any buttons were just pressed on the thumby. [thumbyButton.py:114]
- `dpadPressed()` — Returns true if any dpad buttons are currently pressed on the thumby. [thumbyButton.py:119]
- `dpadJustPressed()` — Returns true if any dpad buttons were just pressed on the thumby. [thumbyButton.py:124]
- `actionPressed()` — Returns true if either action button is pressed on the thumby. [thumbyButton.py:129]
- `actionJustPressed()` — Returns true if either action button was just pressed on the thumby. [thumbyButton.py:134]
- `updateButtons(buttons=allButtons)` — Source-declared function. [thumbyButton.py:138]
- `updateButtons(buttons=allButtons)` — Source-declared function. [thumbyButton.py:143]

## thumbyGraphics

Source: [source-library/thumbyGraphics.py](../source-library/thumbyGraphics.py).
SHA-256: `ba193e731f3f03a64b05c71db1a65ac7ee70ea0cc4c77136619dcca883c1ee9f`.


### DisplayInterface (thumbyGraphics.py:9)

- `__init__(self, driver: DisplayDriver)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:16]
- `poweroff(self)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:31]
- `poweron(self)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:34]
- `contrast(self, contrast)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:37]
- `invert(self, inverted)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:40]
- `flash(self)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:43]
- `enableGrayscale(self)` — Deprecated [thumbyGraphics.py:49]
- `disableGrayscale(self)` — Deprecated [thumbyGraphics.py:53]
- `enableGreyscale(self)` — Deprecated [thumbyGraphics.py:57]
- `disableGreyscale(self)` — Deprecated [thumbyGraphics.py:61]
- `setColourTint(self, red, green, blue)` — Deprecated [thumbyGraphics.py:65]
- `setModeMono(self)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:68]
- `setModeGreyscale(self)` — Select four-tone greyscale if supported by the active driver. Support is backend-dependent. [thumbyGraphics.py:71]
- `setModeTinted(self, red, green, blue)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:74]
- `show(self)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:77]
- `setFPS(self, newFrameRate)` — Set the requested FPS, clamped to 0..60 in this library. Zero disables frame limiting; actual delivered FPS may be lower. [thumbyGraphics.py:81]
- `update(self)` — Present the buffer and enforce the frame-rate cap. While waiting, button edges are latched. Does not return a frame count. [thumbyGraphics.py:86]
- `brightness(self, setting)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:100]
- `fill(self, colour: int)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:104]
- `drawFilledRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:108]
- `drawRectangle(self, x: int, y: int, width: int, height: int, colour: int)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:112]
- `drawFilledEllispe(self, x: int, y: int, width: int, height: int, colour: int)` — Exact source spelling: Ellispe, not Ellipse. Draw a filled ellipse through the current driver. [thumbyGraphics.py:116]
- `drawEllispe(self, x: int, y: int, width: int, height: int, colour: int)` — Exact source spelling: Ellispe, not Ellipse. Delegates to the active driver; the base driver may raise NotImplementedError. [thumbyGraphics.py:120]
- `setPixel(self, x: int, y: int, colour: int)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:124]
- `getPixel(self, x: int, y: int)` — WARNING: this wrapper calls driver.getPixel but does not return it. In the supplied source this returns None, not a pixel colour. [thumbyGraphics.py:128]
- `drawLine(self, x0: int, y0: int, x1: int, y1: int, colour: int)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:132]
- `setFont(self, fontFile, width=None, height=None, space=1)` — Load a .bin font; width and height can be inferred from a fontWIDTHxHEIGHT filename. space is inter-character spacing. The file must exist on the target. [thumbyGraphics.py:135]
- `drawText(self, stringToPrint, x: int, y: int, colour: int)` — Draw text with the selected bitmap font. This source constructs memoryview(stringToPrint); bytes are a safer choice when porting across runtimes. Call update to show it. [thumbyGraphics.py:153]
- `blit(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:181]
- `drawSprite(self, s)` — Draw a Sprite using its bitmap, position, key and mirror fields. Rendering remains in the buffer until update/show. [thumbyGraphics.py:185]
- `blitWithMask(self, src, x: int, y: int, width: int, height: int, key: int, mirrorX: int, mirrorY: int, mask)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:189]
- `drawSpriteWithMask(self, s, m)` — Draw sprite s with sprite m as its mask. Both arguments must expose bitmap data. [thumbyGraphics.py:193]
- `calibrate(self)` — Source-declared method; backend-specific implementation. [thumbyGraphics.py:196]
- `detect_vga(i2c, guess=False)` — Source-declared function. [thumbyGraphics.py:218]
- `do_test()` — Source-declared function. [thumbyGraphics.py:282]

## thumbyGrayscale

Source: [source-library/thumbyGrayscale.py](../source-library/thumbyGrayscale.py).
SHA-256: `f2cdeaf3d15009c3896d293b4f9163599e2f61d64312d2020cd5bbdf6cf348ae`.


## thumbyHardware

Source: [source-library/thumbyHardware.py](../source-library/thumbyHardware.py).
SHA-256: `dbe958477b3513ecb54a80b4318b7d352cc0474fb036ddc2e0a416bad02bf4c5`.


### PwmDummy (thumbyHardware.py:53)

- `__init__(self)` — Source-declared method; backend-specific implementation. [thumbyHardware.py:54]
- `duty_u16(self, value)` — Source-declared method; backend-specific implementation. [thumbyHardware.py:57]
- `freq(self, value)` — Source-declared method; backend-specific implementation. [thumbyHardware.py:60]
- `reset()` — Source-declared function. [thumbyHardware.py:50]
- `reset()` — Source-declared function. [thumbyHardware.py:69]
- `reset()` — Wrap machine.reset() to be accessible as thumby.reset() [thumbyHardware.py:133]

## thumbyLink

Source: [source-library/thumbyLink.py](../source-library/thumbyLink.py).
SHA-256: `a332dfa2886df1de615a071fe51194d9eec39d7d33beea1950bfbbd3320d2ccc`.


### LinkClass (thumbyLink.py:38)

- `__init__(self)` — Source-declared method; backend-specific implementation. [thumbyLink.py:39]
- `init(self)` — Source-declared method; backend-specific implementation. [thumbyLink.py:43]
- `send(self, data)` — Physical branch sends up to 512 bytes and returns success/failure. Emulator/colour branches are no-ops returning None. [thumbyLink.py:47]
- `receive(self)` — Physical branch receives a checked packet or None. Emulator/colour branches are no-ops returning None. [thumbyLink.py:51]

### LinkClass (thumbyLink.py:57)

- `__init__(self)` — Source-declared method; backend-specific implementation. [thumbyLink.py:58]
- `init(self)` — Source-declared method; backend-specific implementation. [thumbyLink.py:63]
- `send(self, data)` — Physical branch sends up to 512 bytes and returns success/failure. Emulator/colour branches are no-ops returning None. [thumbyLink.py:78]
- `receive(self)` — Physical branch receives a checked packet or None. Emulator/colour branches are no-ops returning None. [thumbyLink.py:131]

## thumbySaves

Source: [source-library/thumbySaves.py](../source-library/thumbySaves.py).
SHA-256: `98967a204a4c4503ce38b7f69716fa07ab3411aee02c549f7754f8f7838860cd`.


### SavesClass (thumbySaves.py:49)

- `__init__(self)` — Source-declared method; backend-specific implementation. [thumbySaves.py:50]
- `setName(self, subdir)` — Select a game-specific save directory under /Saves and load its persistent or backup JSON. [thumbySaves.py:74]
- `setItem(self, key, value)` — Set a value in the in-memory save dictionary. Use save() to persist. Keys beginning __b are reserved for byte metadata. [thumbySaves.py:104]
- `getItem(self, key)` — Get a saved value, decoding stored byte data if needed; returns None when missing. [thumbySaves.py:117]
- `delItem(self, key)` — Delete entry in volatile dictionary [thumbySaves.py:127]
- `hasItem(self, key)` — Check if save data entry exists in volatile dictionary [thumbySaves.py:136]
- `save(self, backup=False)` — Write the in-memory dictionary to persistent.json. backup=True renames the prior file to backup.json first. [thumbySaves.py:145]
- `getName(self)` — Return the current save path [thumbySaves.py:170]

## thumbySprite

Source: [source-library/thumbySprite.py](../source-library/thumbySprite.py).
SHA-256: `544b829c89309c5f0b8e1f907b1293efae53257c8b9dbb8f1f9366367c283dd3`.


### Sprite (thumbySprite.py:26)

- `__init__(self, width, height, bitmapData, x=0, y=0, key=-1, mirrorX=False, mirrorY=False)` — Create a sprite from bytearray data or a filename. Two matching bitplanes may be supplied as a tuple/list. Frame byte size is width * ceil(height/8). [thumbySprite.py:28]
- `getFrame(self)` — Source-declared method; backend-specific implementation. [thumbySprite.py:80]
- `setFrame(self, frame)` — Select an animation frame modulo frameCount. Negative indices do not update the frame. [thumbySprite.py:84]
