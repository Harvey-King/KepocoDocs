# SPDX-License-Identifier: GPL-3.0-or-later
"""04: Animated sprite. A: pause/resume; hold L/R to move; B: exit.

Run/upload this one file with the Kepoco USB tooling. For a finite smoke run,
import it and call main(max_frames=60); importing alone does not start play.
"""
import kepoco
from time import ticks_ms, ticks_diff

# MONO_VLSB: each byte is one vertical column, bit 0 at the top.
# For 8x8, each frame needs 8 bytes (width * ceil(height / 8)).
# Concatenate frames in ONE bytearray: frame 0 uses bytes [0:8], frame 1
# uses [8:16]. A list of two bytearrays means shaded bitplanes, NOT frames!
# These two faces change their mouth; no external bitmap file is needed.
BITMAP = bytearray([
    0x3C, 0x42, 0x95, 0xA1, 0xA1, 0x95, 0x42, 0x3C,
    0x3C, 0x42, 0xA5, 0x91, 0x91, 0xA5, 0x42, 0x3C,
])


def main(max_frames=None):
    display = kepoco.display
    display.setFPS(30)
    display.setFont('/lib/font5x7.bin', 5, 7, 1)
    # The real SDK Sprite constructor stores a memoryview of the frame.
    # setFrame(index), not slicing pixels by hand, selects its byte offset.
    sprite = kepoco.Sprite(8, 8, BITMAP, 32, 18, 0)
    previous = ticks_ms()
    animation_ms = 0
    paused = False
    x = 32.0
    frames = 0
    while max_frames is None or frames < max_frames:
        if kepoco.buttonB.justPressed():
            break
        now = ticks_ms()
        elapsed = max(0, ticks_diff(now, previous))
        previous = now  # Refresh even when paused; no catch-up on resume.
        # Credit the interval to the OLD state: the edge happens at now.
        if not paused:
            animation_ms += elapsed
        if kepoco.buttonA.justPressed():
            paused = not paused
        # Pause stops animation only; held movement still works.
        dt = min(100, elapsed) / 1000.0
        x += (int(kepoco.buttonR.pressed()) - int(kepoco.buttonL.pressed())) * 30 * dt
        x = min(64.0, max(0.0, x))
        sprite.x = int(x)
        sprite.setFrame((animation_ms // 200) % 2)
        display.fill(display.BLACK)
        # Bytes avoid archived drawText's memoryview(str) incompatibility.
        display.drawText(b'ANIMATE', 0, 0, display.WHITE)
        display.drawSprite(sprite)
        display.drawText(b'A:PAUSE B:X', 0, 33, display.WHITE)
        display.update()
        frames += 1
    return {'frame': sprite.getFrame(), 'x': sprite.x, 'paused': paused}


if __name__ == '__main__':
    main()
