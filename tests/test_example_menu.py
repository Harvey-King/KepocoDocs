# SPDX-License-Identifier: GPL-3.0-or-later
"""Host-only tests: fake hardware, real example logic; no archived imports."""
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "02_menu_settings_slider.py"


class FakeButton:
    def __init__(self, hardware, name):
        self.hardware = hardware
        self.name = name
        self.last = False
        self.calls = []

    def justPressed(self):
        self.calls.append(self.hardware.display.frames)
        held = self.name in self.hardware.keys()
        edge = held and not self.last
        self.last = held
        return edge


class FakeDisplay:
    BLACK, WHITE, width, height = 0, 1, 72, 40

    def __init__(self):
        self.frames = 0
        self.items = []
        self.history = []

    def setFPS(self, rate):
        self.rate = rate

    def setFont(self, *args):
        self.font = args

    def fill(self, colour):
        self.items = []

    def bounds(self, x, y, width, height):
        assert 0 <= x and x + width <= 72, (x, width)
        assert 0 <= y and y + height <= 40, (y, height)

    def drawText(self, text, x, y, colour):
        memoryview(text)  # Reject str like the source-library implementation.
        self.bounds(x, y, len(text) * 6 - 1, 7)
        self.items.append(("text", bytes(text), x, y))

    def drawFilledRectangle(self, x, y, width, height, colour):
        self.bounds(x, y, width, height)
        self.items.append(("rect", x, y, width, height))

    def drawLine(self, x0, y0, x1, y1, colour):
        self.bounds(min(x0, x1), min(y0, y1), abs(x1 - x0) + 1, abs(y1 - y0) + 1)
        self.items.append(("line", x0, y0, x1, y1))

    def update(self):
        self.history.append(list(self.items))
        self.frames += 1


class FakeHardware:
    def __init__(self, schedule=()):
        self.display = FakeDisplay()
        self.schedule = schedule
        for name in "UDLRAB":
            setattr(self, "button" + name, FakeButton(self, name))

    def keys(self):
        frame = self.display.frames
        return self.schedule[frame] if frame < len(self.schedule) else ""


class MenuTests(unittest.TestCase):
    def load_app(self, schedule=(), tick_step=33, tick_start=0):
        self.assertTrue(EXAMPLE.exists(), "menu/settings/slider example missing")
        hardware = FakeHardware(schedule)
        modulus = 1 << 30
        clock = types.SimpleNamespace(
            ticks_ms=lambda: (tick_start + hardware.display.frames * tick_step) % modulus,
            ticks_diff=lambda a, b: (a - b + modulus // 2) % modulus - modulus // 2,
        )
        previous = {name: sys.modules.get(name) for name in ("kepoco", "time")}
        sys.modules["kepoco"] = hardware
        sys.modules["time"] = clock
        try:
            module = types.ModuleType("menu_example")
            exec(compile(EXAMPLE.read_text(encoding="utf-8"), str(EXAMPLE), "exec"), module.__dict__)
        finally:
            for name, value in previous.items():
                if value is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = value
        self.assertEqual(hardware.display.frames, 0, "import must not run main")
        return module, hardware

    def test_menu_navigation_and_activation(self):
        module, _ = self.load_app()
        app = module.App()
        self.assertEqual((app.page, app.selection), ("menu", 0))
        app.update({"D": True}, 0)
        self.assertEqual(app.selection, 1)
        app.update({"A": True}, 0)
        self.assertEqual(app.page, "settings")
        app = module.App()
        app.update({"U": True}, 0)
        self.assertEqual(app.selection, 2)
        app.update({"D": True}, 0)
        app.update({"A": True}, 0)
        self.assertEqual(app.page, "play")

    def test_back_returns_from_pages_and_quit_exits(self):
        module, _ = self.load_app()
        app = module.App()
        for page in ("settings", "play"):
            app.page = page
            app.update({"B": True, "A": True}, 0)
            self.assertEqual(app.page, "menu")
            self.assertTrue(app.running)
        app.update({"B": True}, 0)
        self.assertFalse(app.running)
        app = module.App()
        app.update({"U": True}, 0)
        app.update({"A": True}, 0)
        self.assertFalse(app.running)

    def test_speed_edits_clamp_and_persist_in_ram(self):
        module, _ = self.load_app()
        app = module.App()
        self.assertEqual(app.speed, module.START_SPEED)
        app.update({"R": True}, 0)
        self.assertEqual(app.speed, module.START_SPEED, "menu ignores slider edits")
        app.update({"D": True}, 0)
        app.update({"A": True}, 0)
        app.update({"R": True}, 0)
        self.assertEqual(app.speed, module.START_SPEED + 5)
        self.assertIsInstance(app.speed, int)
        for _ in range(30):
            app.update({"L": True}, 0)
        self.assertEqual(app.speed, 0)
        for _ in range(30):
            app.update({"R": True}, 0)
        self.assertEqual(app.speed, 100)
        app.update({"B": True}, 0)
        app.update({"U": True}, 0)
        app.update({"A": True}, 0)
        self.assertEqual(app.page, "play")
        self.assertEqual(app.speed, 100)
        app.update({"B": True}, 0)
        app.update({"D": True}, 0)
        app.update({"A": True}, 0)
        self.assertEqual((app.page, app.speed), ("settings", 100))
        self.assertEqual(module.App().speed, module.START_SPEED)

    def test_play_consumes_speed_as_pixels_per_second_with_dt_cap(self):
        module, _ = self.load_app()
        app = module.App()
        app.page = "play"
        app.speed = 20
        start = app.x
        app.update({}, 0.1)
        self.assertAlmostEqual(app.x - start, 2)
        app.speed = 100
        app.update({}, 0.1)
        self.assertAlmostEqual(app.x - start, 12)
        app.speed = 0
        frozen = app.x
        app.update({}, 0.1)
        self.assertEqual(app.x, frozen)
        app.speed = 100
        app.update({}, 10)
        self.assertAlmostEqual(app.x - frozen, 10)
        app.update({}, -1)
        self.assertAlmostEqual(app.x - frozen, 10)
        app.x = 67.0
        app.update({}, 0.1)
        self.assertTrue(0 <= app.x <= 68)
        app.page = "settings"
        frozen = app.x
        app.update({}, 0.1)
        self.assertEqual(app.x, frozen)

    def test_draw_pages_fit_and_knob_tracks_real_value(self):
        module, hardware = self.load_app()
        app = module.App()
        for selection, label in enumerate((b"Play", b"Settings", b"Quit")):
            app.selection = selection
            app.draw()
            self.assertIn(("text", label, 8, selection * 8), hardware.display.items)
            self.assertIn(("text", b">", 0, selection * 8), hardware.display.items)
        app.page = "settings"
        for speed, position in ((0, 8), (50, 36), (100, 64)):
            app.speed = speed
            self.assertEqual(app.slider_x(), position)
            app.draw()
            self.assertIn(("rect", position - 1, 22, 3, 5), hardware.display.items)
            self.assertIn(("line", 8, 24, 64, 24), hardware.display.items)
            self.assertIn(("text", ("Speed:%d" % speed).encode(), 0, 8), hardware.display.items)
            # Track and knob stay between the value row and control row.
            self.assertIn(("text", b"L/R B:back", 0, 32), hardware.display.items)
        app.page = "play"
        app.x = 12.75
        app.draw()
        self.assertIn(("rect", 12, 19, 4, 4), hardware.display.items)
        self.assertIn(("text", b"B:menu", 0, 32), hardware.display.items)

    def test_finite_main_polls_every_edge_once_per_frame_and_held_is_one_edit(self):
        schedule = ("D", "", "A", "R", "R", "", "R", "B", "U", "A", "", "B", "", "B")
        module, hardware = self.load_app(schedule)
        self.assertTrue(callable(getattr(module, "main", None)), "finite main is missing")
        app = module.main(max_frames=30)
        self.assertFalse(app.running)
        self.assertEqual(app.speed, module.START_SPEED + 10)
        self.assertGreater(app.x, 0)
        self.assertEqual(hardware.display.frames, 13)
        self.assertEqual(hardware.display.rate, 30)
        self.assertEqual(hardware.display.font, ("/lib/font5x7.bin", 5, 7, 1))
        for name in "UDLRAB":
            self.assertEqual(getattr(hardware, "button" + name).calls, list(range(14)))
        module, hardware = self.load_app()
        self.assertTrue(module.main(max_frames=3).running)
        self.assertEqual(hardware.display.frames, 3)
        module, hardware = self.load_app()
        module.main(max_frames=0)
        self.assertEqual(hardware.display.frames, 0)

    def test_main_ticks_wrap_and_long_frame_cap(self):
        for tick_step, tick_start, expected in ((33, (1 << 30) - 20, 2.64), (1000, 0, 8.0)):
            module, hardware = self.load_app(("A", "", ""), tick_step, tick_start)
            app = module.main(max_frames=3)
            self.assertAlmostEqual(app.x, expected)
            positions = [item[1] for frame in hardware.display.history for item in frame if item[0] == "rect"]
            self.assertEqual(positions[-1], int(expected))

    def test_main_guard_runs_standalone_and_can_exit_without_frame(self):
        _, hardware = self.load_app(("B",))
        previous = {name: sys.modules.get(name) for name in ("kepoco", "time")}
        sys.modules["kepoco"] = hardware
        sys.modules["time"] = types.SimpleNamespace(ticks_ms=lambda: 0, ticks_diff=lambda a, b: a - b)
        try:
            exec(compile(EXAMPLE.read_text(encoding="utf-8"), str(EXAMPLE), "exec"), {"__name__": "__main__"})
        finally:
            for name, value in previous.items():
                if value is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = value
        self.assertEqual(hardware.display.frames, 0)
        for name in "UDLRAB":
            self.assertEqual(getattr(hardware, "button" + name).calls, [0])


if __name__ == "__main__":
    unittest.main()
