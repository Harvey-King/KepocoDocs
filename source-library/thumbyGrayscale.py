# Compatibility layer for greyscale

# Written by Keith Greenhow for Kent Thumby.
# 08-Jan-2025

'''
    This file is part of the Kent Extention to the Thumby API.

    The Thumby API is free software: you can redistribute it and/or modify
    it under the ter
    ms of the GNU General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The Thumby API is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    the Thumby API. If not, see <https://www.gnu.org/licenses/>.
'''

from thumbyGraphics import display
from thumbySprite import Sprite

# imports purely for edge-case backwards compatibility
from utime import sleep_ms, ticks_diff, ticks_ms, sleep_us
from machine import Pin, SPI, idle, mem32
import _thread
from os import stat
from math import sqrt, floor
from array import array
from thumbyAudio import audio
from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR
from thumbyHardware import HWID
from sys import modules

display.enableGrayscale()