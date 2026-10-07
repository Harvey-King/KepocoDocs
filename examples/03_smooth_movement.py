# SPDX-License-Identifier: GPL-3.0-or-later
"""03: Smooth movement. Hold L/R/U/D to move; B: exit.

Run/upload this single file with the Kepoco USB tooling. Importing does not
start the movement loop; call main(max_frames=60) for a finite smoke run,
or main() to play until B. The kepoco import still initializes target hardware.
"""
import kepoco
from time import ticks_ms, ticks_diff


def main(max_frames=None):
    display = kepoco.display
    display.setFPS(30)  # update() handles frame pacing; do not add blocking sleeps.
    display.setFont('/lib/font5x7.bin', 5, 7, 1)
    # The 7-pixel header and footer leave y=9..30 for the playfield.
    # Keep subpixel positions as floats; convert only when drawing.
    x, y = 36.0, 18.0
    previous = ticks_ms()
    frames = 0
    while max_frames is None or frames < max_frames:
        if kepoco.buttonB.justPressed():
            break  # Edge input exits once; directions below are held inputs.
        now = ticks_ms()
        # ticks_diff handles clock wrap. Cap stalls at 100ms so resuming a
        # debugger does not teleport the player; negative deltas are ignored.
        dt = min(100, max(0, ticks_diff(now, previous))) / 1000.0
        previous = now
        x += (int(kepoco.buttonR.pressed()) - int(kepoco.buttonL.pressed())) * 30 * dt
        y += (int(kepoco.buttonD.pressed()) - int(kepoco.buttonU.pressed())) * 30 * dt
        # Clamp the whole 4x4 square, not just its top-left corner.
        x = min(68.0, max(0.0, x))
        y = min(27.0, max(9.0, y))
        display.fill(display.BLACK)
        # Archived drawText uses memoryview(): pass bytes, not ordinary str.
        display.drawText(b'MOVE', 0, 0, display.WHITE)
        display.drawFilledRectangle(int(x), int(y), 4, 4, display.WHITE)
        display.drawText(b'B:EXIT', 0, 33, display.WHITE)
        display.update()
        frames += 1
    return {'x': x, 'y': y}


if __name__ == '__main__':
    main()
