# SPDX-License-Identifier: GPL-3.0-or-later
"""05: Collect the dot. Hold L/R/U/D to move; A: reset; B: exit.

Run/upload this one file with Kepoco USB tooling. main(max_frames=60) gives
an importable finite smoke run; main() plays indefinitely until B is pressed.
"""
import kepoco
from time import ticks_ms, ticks_diff


def overlaps(x, y, dot_x, dot_y):
    # Axis-aligned rectangle collision: 4x4 player against a 2x2 dot.
    # Strict inequalities mean merely touching edges is NOT collecting.
    return x < dot_x + 2 and x + 4 > dot_x and y < dot_y + 2 and y + 4 > dot_y


def respawn(x, y):
    # Choose the horizontally opposite corner deterministically. This is
    # guaranteed clear of a 4x4 player, so no random retry loop is necessary.
    # Both 2x2 targets remain inside the y=9..30 playfield.
    return (66 if x < 36 else 2, 27 if y < 20 else 10)


def main(max_frames=None):
    display = kepoco.display
    display.setFPS(30)
    display.setFont('/lib/font5x7.bin', 5, 7, 1)
    x, y = 4.0, 18.0
    dot_x, dot_y = 16, 18
    score = 0
    previous = ticks_ms()
    frames = 0
    while max_frames is None or frames < max_frames:
        if kepoco.buttonB.justPressed():
            break
        now = ticks_ms()
        # A 100ms movement cap limits each axis to 3px, so a 4px player
        # cannot skip a 2px target even after a long stalled frame.
        dt = min(100, max(0, ticks_diff(now, previous))) / 1000.0
        previous = now
        if kepoco.buttonA.justPressed():
            x, y, score = 4.0, 18.0, 0
            dot_x, dot_y = 16, 18
        else:
            x += (int(kepoco.buttonR.pressed()) - int(kepoco.buttonL.pressed())) * 30 * dt
            y += (int(kepoco.buttonD.pressed()) - int(kepoco.buttonU.pressed())) * 30 * dt
            x = min(68.0, max(0.0, x))
            y = min(27.0, max(9.0, y))
            # Use drawn integer positions so scoring matches visible pixels.
            if overlaps(int(x), int(y), dot_x, dot_y):
                score = min(9999, score + 1)  # Keep the HUD readable forever.
                dot_x, dot_y = respawn(int(x), int(y))
        display.fill(display.BLACK)
        # Archived drawText requires bytes (it calls memoryview); encode
        # variable labels. The tiny HUD is separate from y=9..30 playfield.
        display.drawText(('S:%d' % score).encode(), 0, 0, display.WHITE)
        display.drawFilledRectangle(int(x), int(y), 4, 4, display.WHITE)
        display.drawFilledRectangle(dot_x, dot_y, 2, 2, display.WHITE)
        display.drawText(b'A:RST B:X', 0, 33, display.WHITE)
        display.update()
        frames += 1
    return {'x': x, 'y': y, 'score': score, 'dot': (dot_x, dot_y)}


if __name__ == '__main__':
    main()
