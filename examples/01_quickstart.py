"""Kepoco target example: steer a square with L/R; press B to exit.
Run through your Kepoco editor, not desktop Python.
"""
import kepoco
import time


def main():
    kepoco.display.setFPS(30)
    x = 32.0
    last = time.ticks_ms()
    while True:
        now = time.ticks_ms()
        dt = max(0, min(100, time.ticks_diff(now, last)))
        last = now
        if kepoco.buttonB.justPressed():
            break
        direction = int(kepoco.buttonR.pressed()) - int(kepoco.buttonL.pressed())
        x = max(0, min(kepoco.display.width - 6, x + direction * dt * 0.05))
        kepoco.display.fill(kepoco.display.BLACK)
        kepoco.display.drawFilledRectangle(int(x), 20, 6, 6, kepoco.display.WHITE)
        kepoco.display.update()
    kepoco.display.fill(kepoco.display.BLACK)
    kepoco.display.update()


if __name__ == '__main__':
    main()
