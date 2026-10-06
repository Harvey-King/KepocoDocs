from os import stat
from utime import sleep_ms, ticks_diff, ticks_ms, sleep_us
from thumbyButton import updateButtons
import math

ones  = bytes([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
zeros = bytes([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

class DisplayInterface:
    
    BLACK = 0
    WHITE = 1
    DARKGRAY  = 2
    LIGHTGRAY = 3

    def __init__(self, driver: DisplayDriver):
        self.width = driver.width
        self.height = driver.height
        self.driver = driver
        self.display = driver # Deprecated
        self.frameRate = 0
        self.lastUpdateEnd = 0
        self.setFont("/lib/font5x7.bin", 5, 7, 1)
        self.fill(0)
        
        # self.driver.init_display()

    # def init_display(self):
    #     self.driver.init_display()

    def poweroff(self):
        self.driver.poweroff()

    def poweron(self):
        self.driver.poweron()

    def contrast(self, contrast):
        self.driver.contrast(contrast)

    def invert(self, inverted):
        self.driver.invert(inverted)
    
    def flash(self):
        self.driver.invert(True)
        self.show()
        self.driver.invert(False)
    
    # Deprecated
    def enableGrayscale(self):
        self.driver.setModeGreyscale()
    
    # Deprecated
    def disableGrayscale(self):
        self.driver.setModeMono()
    
    # Deprecated
    def enableGreyscale(self):
        self.driver.setModeGreyscale()
    
    # Deprecated
    def disableGreyscale(self):
        self.driver.setModeMono()
    
    # Deprecated
    def setColourTint(self, red, green, blue):
        self.driver.setModeTinted(red, green, blue)
    
    def setModeMono(self):
        self.driver.setModeMono()
    
    def setModeGreyscale(self):
        self.driver.setModeGreyscale()
    
    def setModeTinted(self, red, green, blue):
        self.driver.setModeTinted(red, green, blue)
    
    def show(self):
        self.driver.show()
            
    @micropython.native
    def setFPS(self, newFrameRate):
        self.frameRate = min(max(newFrameRate, 0), 60)
    
    # Push the buffer to the hardware display.
    @micropython.native
    def update(self):
        self.show()
        fr = self.frameRate
        lue = self.lastUpdateEnd
        if fr>0:
            frameTimeRemaining = round(1000/fr) - ticks_diff(ticks_ms(), lue)
            while(frameTimeRemaining>1):
                updateButtons()
                sleep_ms(1)
                frameTimeRemaining = round(1000/fr) - ticks_diff(ticks_ms(), lue)
            while(frameTimeRemaining>0):
                frameTimeRemaining = round(1000/fr) - ticks_diff(ticks_ms(), lue)
        self.lastUpdateEnd=ticks_ms()

    def brightness(self,setting):
        self.driver.brightness(setting)

    @micropython.native
    def fill(self, colour:int):
        self.driver.fill(colour)
    
    @micropython.native
    def drawFilledRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        self.driver.drawFilledRectangle(x, y, width, height, colour)

    @micropython.native
    def drawRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        self.driver.drawRectangle(x, y, width, height, colour)
        
    @micropython.native
    def drawFilledEllispe(self, x:int, y:int, width:int, height:int, colour:int):
        self.driver.drawFilledEllispe(x, y, width, height, colour)
    
    @micropython.native
    def drawEllispe(self, x:int, y:int, width:int, height:int, colour:int):
        self.driver.drawEllispe(x, y, width, height, colour)

    @micropython.native
    def setPixel(self, x:int, y:int, colour:int):
        self.driver.setPixel(x, y, colour)

    @micropython.native
    def getPixel(self, x:int, y:int):
        self.driver.getPixel(x, y)

    @micropython.native
    def drawLine(self, x0:int, y0:int, x1:int, y1:int, colour:int):
        self.driver.drawLine(x0, y0, x1, y1, colour)

    def setFont(self, fontFile, width=None, height=None, space=1):
        if not fontFile.endswith(".bin"):
            fontFile += ".bin"
        if width is None or height is None:
            x = fontFile.find("x")
            width = int(fontFile[fontFile.find("font")+4:x])
            height = int(fontFile[x+1:-4])
        sz = stat(fontFile)[6]
        self.font_bmap = bytearray(sz)
        with open(fontFile, 'rb') as fh:
            fh.readinto(self.font_bmap)
            
        self.font_width = width
        self.font_height = height
        self.font_space = space
        self.font_glyphcnt = sz // width

    @micropython.native
    def drawText(self, stringToPrint, x:int, y:int, colour:int):
        w = self.width
        h = self.height
        newline = x
        font_bmap = self.font_bmap
        font_width = self.font_width
        font_height = self.font_height
        font_space = self.font_space
        font_glyphcnt = self.font_glyphcnt
        fore = (ones if colour & 1 else zeros, ones if colour & 2 else zeros)
        for c in memoryview(stringToPrint):
            if isinstance(c, str):
                co = int(ord(c))
            else:
                co = int(c)
            if co == 0x0A: # newline
                x = newline
                y += font_height+font_space
                if y >= h:
                    break
            else:
                co -= 0x20
                if co < font_glyphcnt:
                    if 0 <= x < w:
                        self.driver.blitWithMask(fore, x, y, font_width, font_height, -1, 0, 0, font_bmap[co*font_width:(co+1)*font_width])
                    x += font_width+font_space

    @micropython.native
    def blit(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int):
        self.driver.blit(src, x, y, width, height, key, mirrorX, mirrorY)

    @micropython.native
    def drawSprite(self, s):
        self.driver.blit(s.bitmap, s.x, s.y, s.width, s.height, s.key, s.mirrorX, s.mirrorY)

    @micropython.native
    def blitWithMask(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int, mask):
        self.driver.blitWithMask(src, x, y, width, height, key, mirrorX, mirrorY, mask)

    @micropython.native
    def drawSpriteWithMask(self, s, m):
        self.driver.blitWithMask(s.bitmap, s.x, s.y, s.width, s.height, s.key, s.mirrorX, s.mirrorY, m.bitmap)

    def calibrate(self):
        self.driver.calibrate()

import sys

__version__ = '2.0'

root = ""

# On Thumby Color Linux, need to get filesystem path to the working directory
if "linux" in sys.implementation._machine:
    import engine
    root = engine.root_dir()

from thumbyHardware import displayDriver, IS_EMULATOR



from kepocoConfig import settings
vga_mode = settings["vga"]


def detect_vga(i2c, guess=False):
    if i2c is None:
        return False
    if guess:
        return 0x50 in i2c.scan()
        
    if 0x50 not in i2c.scan():
        return False
    try:
        return i2c.readfrom_mem(0x50, 0, 8) == b'\x00\xff\xff\xff\xff\xff\xff\x00'
    except OSError as e:
        if e.errno == 5:
            return False
        raise e

if vga_mode > 0:
    old_Driver = None
    from thumbyHardware import i2c
    try:
        if detect_vga(i2c, guess=True):
            print("Enable VGA")
            import kepocoVGA
            old_Driver = displayDriver
            displayDriver = kepocoVGA.VGADriver(displayDriver, 60)
            displayDriver.init_display()
            if vga_mode == 2:
                displayDriver.enablePhysicalScreen(False)
        elif vga_mode == 2:
            print("VGA not detected")
    except OSError as e:
        print("VGA detect failed: ", type(e), e)
        vga_mode = 0
        pass


display = DisplayInterface(displayDriver)

if vga_mode == 2 and old_Driver is not None:
    display.drawText("VGA ONLY", (72-47)//2, (40-7)//2, 1)
    old_Driver.show()
    display.fill(0)


if __name__ == "__main__":
    
    from machine import freq
    freq(250_000_000)
    
    # Run this file directly for a simple max frame rate testing tool.
    # display.enableThumbyCompat()
    # display.display.init_display()

    display.setFPS(0)
    display.fill(display.BLACK)
    # quincunx pattern of squares, 2 white in top row, 1 dark grey in middle, 2 light grey on bottom
    display.drawFilledRectangle(21, 5,10,10,display.WHITE)
    display.drawFilledRectangle(41, 5,10,10,display.WHITE)
    display.drawFilledRectangle(31,15,10,10,display.DARKGRAY)
    display.drawFilledRectangle(21,25,10,10,display.LIGHTGRAY)
    display.drawFilledRectangle(41,25,10,10,display.LIGHTGRAY)
    
    from time import ticks_us
    repeats = 60
    
    def do_test():
        s = ticks_us()
        for _ in range(repeats):
            display.show()
        e = ticks_us()
        print(f"\tTotal display time: {(e-s)/1000:.2f}ms")
        print(f"\tAverage display time per update(): {(e-s)/(repeats*1000):.2f}ms")
        print(f"\tTheoretical max frame rate: {repeats*1_000_000/(e-s):.2f}")
        if e-s < 16.66*repeats:
            print(f"\tSpare time capacity at 60fps: {(16666.66 - (e-s)/repeats)/1000:.2f}ms")
        print()
    
    
    
    print("Mono 1")
    display.contrast(1)
    display.disableGrayscale()
    do_test()
    
    # print("Mono 28")
    # display.contrast(28)
    # display.disableGrayscale()
    # do_test()
    
    # print("Mono 127")
    # display.contrast(127)
    # display.disableGrayscale()
    # do_test()
    
    print("Grey")
    display.enableGrayscale()
    do_test()
    
    # print("Tint")
    # display.setColourTint(0,255,255)
    # do_test()
