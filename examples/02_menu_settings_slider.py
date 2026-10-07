# SPDX-License-Identifier: GPL-3.0-or-later
"""Menu -> settings -> moving square: a complete 72x40 teaching script.

Run this saved file with the repository's Kepoco USB task (Ctrl+S, then
Ctrl+Shift+B); do not replace a firmware/library module.
Menu: U/D selects (wraps), A opens Play/Settings or activates Quit, B exits.
Settings: tap L/R to change speed by STEP; B returns to the menu.
Play: the square moves automatically at speed pixels/second; B returns.

speed is an integer shared by the pages of one App, stored only in RAM.
Restarting main() resets it to START_SPEED. No saves or firmware writes occur.
The slider maps that value to pixels, rather than being the source of truth.
The square wraps across the screen; fractional x preserves subpixel motion.

Text uses bytes literals and .encode() for numbers because the archived
thumbyGraphics.drawText uses memoryview(text): a plain str is not compatible.
The existing /lib/font5x7.bin is read by setFont, never written. Its 6-pixel
character pitch and 7-pixel height keep labels, controls and slider separate.
main(max_frames=120) offers a finite smoke run; importing never starts play.
Host tests use fake hardware/time; they are not physical-device verification.
"""
import kepoco
import time

# Change START_SPEED for the initial pixels/second; STEP for each button tap.
# Keep MAX_SPEED > MIN_SPEED; these bounds define the slider's real data range.
MIN_SPEED = 0
MAX_SPEED = 100
START_SPEED = 40
STEP = 5


class App:
    def __init__(self):
        self.page = "menu"
        self.selection = 0
        self.running = True
        self.speed = max(MIN_SPEED, min(MAX_SPEED, START_SPEED))
        self.x = 0.0

    def update(self, edges: dict, dt: float):
        # Back wins over simultaneous actions, so one press changes one page.
        if edges.get("B", False):
            if self.page == "menu":
                self.running = False
            else:
                self.page = "menu"
            return
        if self.page == "menu":
            if edges.get("U", False):
                self.selection = (self.selection - 1) % 3
            elif edges.get("D", False):
                self.selection = (self.selection + 1) % 3
            if edges.get("A", False):
                if self.selection == 0:
                    self.page = "play"
                elif self.selection == 1:
                    self.page = "settings"
                else:
                    self.running = False
        elif self.page == "settings":
            change = STEP * (int(edges.get("R", False)) - int(edges.get("L", False)))
            self.speed = max(MIN_SPEED, min(MAX_SPEED, self.speed + change))
        elif self.page == "play":
            # speed is real pixels/second, not the slider's drawing coordinate.
            # Cap a stalled frame at 100 ms; negative deltas cannot move backwards.
            dt = max(0.0, min(0.1, dt))
            self.x = (self.x + self.speed * dt) % (kepoco.display.width - 4 + 1)

    def slider_x(self) -> int:
        # Map real data to a drawing position; moving the knob alone changes nothing.
        # Change these drawing endpoints to relocate the track, not the speed bounds.
        return 8 + (self.speed - MIN_SPEED) * 56 // (MAX_SPEED - MIN_SPEED)

    def draw(self):
        display = kepoco.display
        display.fill(display.BLACK)
        if self.page == "menu":
            for index, label in enumerate((b"Play", b"Settings", b"Quit")):
                display.drawText(label, 8, index * 8, display.WHITE)
            display.drawText(b">", 0, self.selection * 8, display.WHITE)
            display.drawText(b"U/D A:go", 0, 24, display.WHITE)
            display.drawText(b"B:exit", 0, 32, display.WHITE)
        elif self.page == "settings":
            display.drawText(b"Settings", 0, 0, display.WHITE)
            display.drawText(("Speed:%d" % self.speed).encode(), 0, 8, display.WHITE)
            display.drawLine(8, 24, 64, 24, display.WHITE)
            display.drawFilledRectangle(self.slider_x() - 1, 22, 3, 5, display.WHITE)
            display.drawText(b"L/R B:back", 0, 32, display.WHITE)
        else:
            display.drawText(("%d px/s" % self.speed).encode(), 0, 0, display.WHITE)
            display.drawFilledRectangle(int(self.x), 19, 4, 4, display.WHITE)
            display.drawText(b"B:menu", 0, 32, display.WHITE)


def main(max_frames=None):
    """Run until Quit/B, or stop after max_frames display updates for a smoke test."""
    display = kepoco.display
    display.setFPS(30)
    display.setFont("/lib/font5x7.bin", 5, 7, 1)
    app = App()
    frames = 0
    previous = time.ticks_ms()
    buttons = (("U", kepoco.buttonU), ("D", kepoco.buttonD),
               ("L", kepoco.buttonL), ("R", kepoco.buttonR),
               ("A", kepoco.buttonA), ("B", kepoco.buttonB))
    while app.running and (max_frames is None or frames < max_frames):
        now = time.ticks_ms()
        dt = time.ticks_diff(now, previous) / 1000.0
        previous = now
        # Consume ALL six edges once even on screens that ignore some buttons.
        # A short-circuit expression here could leave a stale edge for another page.
        edges = {name: button.justPressed() for name, button in buttons}
        app.update(edges, dt)
        if not app.running:
            break
        app.draw()
        display.update()  # Firmware handles FPS pacing and button latching here.
        frames += 1
    return app


if __name__ == "__main__":
    main()
