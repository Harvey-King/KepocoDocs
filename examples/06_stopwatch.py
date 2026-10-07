# SPDX-License-Identifier: GPL-3.0-or-later
"""06: Stopwatch. A: start/pause; L: reset (also pauses); B: exit.

Run/upload this single file with Kepoco USB tooling. Import then call
main(max_frames=60) for a finite smoke run; main() runs until B is pressed.
"""
import kepoco
from time import ticks_ms, ticks_diff


def main(max_frames=None):
    display = kepoco.display
    display.setFPS(30)
    display.setFont('/lib/font5x7.bin', 5, 7, 1)
    elapsed_ms = 0
    running = False
    previous = ticks_ms()
    frames = 0
    while max_frames is None or frames < max_frames:
        if kepoco.buttonB.justPressed():
            break
        now = ticks_ms()
        # Accumulate short wrap-safe intervals rather than now - start.
        # This works across repeated wraps provided we poll more frequently
        # than half the tick period. Unlike movement, do NOT cap stopwatch dt.
        delta = max(0, ticks_diff(now, previous))
        previous = now
        if running:
            elapsed_ms = min(5999900, elapsed_ms + delta)
        # L reset has priority over A when both edges arrive together.
        # Reset also pauses, so the next start never includes idle time.
        # Poll BOTH edges once, even if reset wins. Otherwise the SDK can
        # leave A latched until the next frame and accidentally restart.
        start_pause = kepoco.buttonA.justPressed()
        reset = kepoco.buttonL.justPressed()
        if reset:
            elapsed_ms = 0
            running = False
        elif start_pause:
            running = not running
        if elapsed_ms >= 5999900:
            running = False  # Saturate at readable 99:59.9, never roll over.
        tenths = elapsed_ms // 100
        label = '%02d:%02d.%d' % (tenths // 600, (tenths // 10) % 60, tenths % 10)
        display.fill(display.BLACK)
        # Bytes/encode are necessary: archived drawText uses memoryview().
        display.drawText(b'STOPWATCH', 0, 0, display.WHITE)
        display.drawText(label.encode(), 15, 12, display.WHITE)
        display.drawText(b'RUN' if running else b'PAUSED', 0, 23, display.WHITE)
        display.drawText(b'A:GO L:0 B:X', 0, 33, display.WHITE)
        display.update()
        frames += 1
    return {'elapsed_ms': elapsed_ms, 'running': running}


if __name__ == '__main__':
    main()
