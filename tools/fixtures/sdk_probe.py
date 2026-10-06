"""STATIC-ONLY SDK check. Do not run this on desktop or hardware."""
from typing import assert_type
import kepoco
from kepoco import display, buttonL, buttonU, buttonD, buttonC, Sprite
from thumbyGraphics import DisplayInterface
from thumbyButton import ButtonClass
from thumbyAudio import AudioClass
from thumbySaves import SavesClass
from thumbyLink import LinkClass
from kepocoConfig import settings
from kepocoVGA import VGADriver
import time
import utime
import machine

assert_type(kepoco.display, DisplayInterface)
assert_type(display.width, int)
assert_type(display.height, int)
assert_type(buttonL, ButtonClass)
assert_type(buttonU.pressed(), bool)
assert_type(buttonD.justPressed(), bool)
assert_type(buttonC.justPressed(), bool)
assert_type(kepoco.audio, AudioClass)
assert_type(kepoco.saveData, SavesClass)
assert_type(kepoco.link, LinkClass)
assert_type(display.getPixel(0, 0), None)
assert_type(kepoco.inputPressed(), bool)
assert_type(kepoco.dpadJustPressed(), bool)
assert_type(kepoco.actionJustPressed(), bool)

display.setFPS(newFrameRate=30)
display.setFont(fontFile='/lib/font3x5.bin', width=3, height=5, space=1)
display.drawText(stringToPrint=b'HELLO', x=0, y=0, colour=display.WHITE)
display.drawFilledRectangle(x=1, y=2, width=3, height=4, colour=display.LIGHTGRAY)
display.drawLine(0, 0, 10, 10, display.WHITE)
display.drawEllispe(0, 0, 8, 8, display.DARKGRAY)
sprite = Sprite(width=8, height=8, bitmapData=bytearray([0] * 8), x=0, y=0)
display.drawSprite(sprite)
sprite.setFrame(frame=0)
assert_type(sprite.getFrame(), int)
kepoco.audio.play(freq=440, duration=100)
kepoco.saveData.setName(subdir='SDKTest')
kepoco.saveData.setItem(key='score', value=1)
assert_type(kepoco.saveData.hasItem(key='score'), bool)
assert_type(kepoco.saveData.getName(), str)
kepoco.saveData.save(backup=False)
now = time.ticks_ms()
dt = time.ticks_diff(now, now)
utime.sleep_ms(0)
settings.getOption('brightness')
VGADriver.detect_vga()
machine.freq()
