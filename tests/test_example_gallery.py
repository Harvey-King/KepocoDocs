# SPDX-License-Identifier: GPL-3.0-or-later
"""Host logic tests, not physical button/display or firmware verification.

Vertical TDD evidence (each slice implemented and GREEN before next slice):
Command: python -m unittest discover -s tests -p test_example_gallery.py -v
03 movement: RED missing file -> GREEN 1 test.
03 safety/exit: RED offscreen rectangle -> GREEN 2 tests.
04 sprite animation: RED missing file -> GREEN 3 tests.
04 pause/movement/exit: RED 20 frames instead of 6 -> GREEN 4 tests.
05 collect: RED missing file -> GREEN 5 tests.
05 respawn/reset/bounds: RED missing respawn -> GREEN 6 tests.
06 start/time: RED missing file -> GREEN 7 tests.
06 pause/reset/limit/exit: RED 20 frames instead of 9 -> GREEN 8 tests.
06 latched simultaneous edges: RED reset restarted next frame -> GREEN 8 tests.
"""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class Hardware:
    """Frame-scripted controls and a wrapping MicroPython-style tick clock."""
    PERIOD = 1 << 20

    def __init__(self, controls=None, step=50, start=0):
        self.controls = controls or {}
        self.step, self.start = step, start
        self.frames = 0
        self.rectangles, self.texts, self.sprites = [], [], []
        self.font = None
        self.rate = None
        self.BLACK, self.WHITE = 0, 1
        self.width, self.height = 72, 40
        self.kepoco = types.SimpleNamespace(display=self, Sprite=Sprite)
        for name in ('L', 'R', 'U', 'D', 'A', 'B'):
            setattr(self.kepoco, 'button' + name, Button(self, name))
        self.clock = types.SimpleNamespace(ticks_ms=self.ticks_ms, ticks_diff=self.ticks_diff)

    def ticks_ms(self):
        return (self.start + self.frames * self.step) % self.PERIOD

    def ticks_diff(self, a, b):
        half = self.PERIOD // 2
        return ((a - b + half) % self.PERIOD) - half

    def down(self, name, frame):
        return frame in self.controls.get(name, ())

    def setFPS(self, rate):
        self.rate = rate

    def setFont(self, *args):
        self.font = args

    def fill(self, colour):
        assert colour == self.BLACK

    @staticmethod
    def bounds(x, y, w, h):
        assert isinstance(x, int) and isinstance(y, int)
        assert 0 <= x and x + w <= 72 and 0 <= y and y + h <= 40

    def drawFilledRectangle(self, x, y, w, h, colour):
        self.bounds(x, y, w, h)
        self.rectangles.append((self.frames, x, y, w, h))

    def drawText(self, text, x, y, colour):
        # Archived drawText calls memoryview(text): str is not accepted.
        assert isinstance(text, bytes), 'drawText must receive bytes'
        self.bounds(x, y, max(0, len(text) * 6 - 1), 7)
        self.texts.append((self.frames, text, x, y))

    def drawSprite(self, sprite):
        self.bounds(sprite.x, sprite.y, sprite.width, sprite.height)
        self.sprites.append((self.frames, sprite.x, sprite.y, sprite.getFrame(), bytes(sprite.bitmap)))

    def update(self):
        # Firmware update() polls and latches edges while frame-pacing.
        for name in ('L', 'R', 'U', 'D', 'A', 'B'):
            getattr(self.kepoco, 'button' + name).update()
        self.frames += 1


class Button:
    def __init__(self, hardware, name):
        self.hardware, self.name = hardware, name
        self.last_state = False
        self.latched = False

    def pressed(self):
        return self.hardware.down(self.name, self.hardware.frames)

    def justPressed(self):
        current = self.pressed()
        edge = (current and not self.last_state) or self.latched
        self.last_state = current
        self.latched = False
        return edge

    def update(self):
        current = self.pressed()
        if current and not self.last_state:
            self.latched = True
        self.last_state = current


class Sprite:
    """Bytearray-only subset matching audited thumbySprite.py frame offsets."""
    def __init__(self, width, height, bitmapData, x=0, y=0, key=-1,
                 mirrorX=False, mirrorY=False):
        assert isinstance(bitmapData, bytearray)
        self.width, self.height = width, height
        self.bitmapSource = bitmapData
        self.bitmapByteCount = width * ((height + 7) // 8)
        self.frameCount = len(bitmapData) // self.bitmapByteCount
        self.x, self.y, self.key = x, y, key
        self.mirrorX, self.mirrorY = mirrorX, mirrorY
        self.setFrame(0)

    def setFrame(self, frame):
        self.currentFrame = frame % self.frameCount
        offset = self.currentFrame * self.bitmapByteCount
        self.bitmap = memoryview(self.bitmapSource)[offset:offset + self.bitmapByteCount]

    def getFrame(self):
        return self.currentFrame


def load_example(stem, hardware):
    path = ROOT / 'examples' / (stem + '.py')
    assert path.exists(), 'Missing standalone example: ' + stem
    spec = importlib.util.spec_from_file_location(stem, path)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {'kepoco': hardware.kepoco, 'time': hardware.clock}):
        spec.loader.exec_module(module)
    assert hardware.frames == 0, 'Import must not start the game loop'
    return module


class GalleryTests(unittest.TestCase):
    def test_03_elapsed_held_movement_and_finite_draw(self):
        hw = Hardware({'R': range(4)}, step=50)
        module = load_example('03_smooth_movement', hw)
        state = module.main(max_frames=4)
        self.assertEqual(hw.frames, 4)
        self.assertEqual(hw.font, ('/lib/font5x7.bin', 5, 7, 1))
        self.assertEqual(hw.rate, 30)
        self.assertAlmostEqual(state['x'], 36 + 3 * 30 * 0.05)
        self.assertEqual(state['y'], 18)
        self.assertGreater(hw.rectangles[-1][1], hw.rectangles[0][1])
        self.assertIn('B: exit', module.__doc__)

    def test_03_all_directions_wrap_cap_bounds_and_b_exit(self):
        for name, coordinate, sign in [('L', 'x', -1), ('R', 'x', 1),
                                       ('U', 'y', -1), ('D', 'y', 1)]:
            hw = Hardware({name: range(3)}, start=Hardware.PERIOD - 25)
            state = load_example('03_smooth_movement', hw).main(max_frames=3)
            origin = 36 if coordinate == 'x' else 18
            self.assertAlmostEqual(state[coordinate], origin + sign * 3)
        hw = Hardware({'R': range(20), 'D': range(20), 'B': [15]}, step=2000)
        state = load_example('03_smooth_movement', hw).main(max_frames=20)
        self.assertEqual(hw.frames, 15)
        self.assertEqual((state['x'], state['y']), (68, 27))
        hw = Hardware({'R': [0, 1]}, step=2000)
        state = load_example('03_smooth_movement', hw).main(max_frames=2)
        self.assertEqual(state['x'], 39)  # 100ms cap, not a 60-pixel jump.
        hw = Hardware({'L': range(20), 'U': range(20)})
        state = load_example('03_smooth_movement', hw).main(max_frames=20)
        self.assertEqual(state['y'], 9)
        hw = Hardware({'B': [0]})
        load_example('03_smooth_movement', hw).main()
        self.assertEqual(hw.frames, 0)

    def test_04_sprite_frames_use_byte_offsets_and_wrapping_clock(self):
        hw = Hardware(step=100, start=Hardware.PERIOD - 50)
        module = load_example('04_animated_sprite', hw)
        state = module.main(max_frames=5)
        self.assertEqual(hw.frames, 5)
        self.assertEqual([s[3] for s in hw.sprites], [0, 0, 1, 1, 0])
        self.assertEqual(hw.sprites[0][4], bytes(module.BITMAP[:8]))
        self.assertEqual(hw.sprites[2][4], bytes(module.BITMAP[8:16]))
        self.assertNotEqual(hw.sprites[0][4], hw.sprites[2][4])
        self.assertEqual(state['frame'], 0)
        self.assertEqual(hw.font, ('/lib/font5x7.bin', 5, 7, 1))
        for control in ('A: pause/resume', 'L/R', 'B: exit'):
            self.assertIn(control, module.__doc__)

    def test_04_pause_resume_held_movement_bounds_and_exit(self):
        hw = Hardware({'A': [1, 2, 4], 'R': range(7), 'B': [6]}, step=100)
        state = load_example('04_animated_sprite', hw).main(max_frames=20)
        self.assertEqual(hw.frames, 6)
        self.assertEqual([s[3] for s in hw.sprites], [0, 0, 0, 0, 0, 1])
        self.assertEqual(state['x'], 47)
        self.assertFalse(state['paused'])
        for direction, expected in [('L', 0), ('R', 64)]:
            hw = Hardware({direction: range(40)}, step=2000)
            state = load_example('04_animated_sprite', hw).main(max_frames=40)
            self.assertEqual(state['x'], expected)
        hw = Hardware({'B': [0]})
        load_example('04_animated_sprite', hw).main()
        self.assertEqual(hw.frames, 0)

    def test_05_move_collect_score_and_draw(self):
        hw = Hardware({'R': range(5)}, step=100, start=Hardware.PERIOD - 50)
        module = load_example('05_collect_the_dot', hw)
        state = module.main(max_frames=5)
        self.assertEqual(hw.frames, 5)
        self.assertEqual(state['score'], 1)
        self.assertEqual(state['x'], 16)
        self.assertTrue(any(text == b'S:1' for _, text, _, _ in hw.texts))
        self.assertEqual(hw.font, ('/lib/font5x7.bin', 5, 7, 1))
        for control in ('L/R/U/D', 'A: reset', 'B: exit'):
            self.assertIn(control, module.__doc__)

    def test_05_collision_edges_safe_respawn_reset_and_exit(self):
        hw = Hardware()
        module = load_example('05_collect_the_dot', hw)
        self.assertFalse(module.overlaps(12, 18, 16, 18))
        self.assertTrue(module.overlaps(13, 18, 16, 18))
        self.assertFalse(module.overlaps(16, 14, 16, 18))
        self.assertTrue(module.overlaps(16, 15, 16, 18))
        # Every possible drawn player position must respawn a visible dot
        # away from the player, with no random retries or hidden file state.
        self.assertTrue(callable(getattr(module, 'respawn', None)))
        for x in range(69):
            for y in range(9, 28):
                dot = module.respawn(x, y)
                Hardware.bounds(*dot, 2, 2)
                self.assertGreaterEqual(dot[1], 9)
                self.assertLessEqual(dot[1] + 2, 31)
                self.assertFalse(module.overlaps(x, y, *dot))
                self.assertEqual(dot, module.respawn(x, y))
        hw = Hardware({'R': range(5), 'A': [5, 6], 'B': [7]}, step=100)
        state = load_example('05_collect_the_dot', hw).main(max_frames=20)
        self.assertEqual(hw.frames, 7)
        self.assertEqual((state['x'], state['y'], state['score'], state['dot']),
                         (4, 18, 0, (16, 18)))
        for controls, expected in [({'L': range(30), 'U': range(30)}, (0, 9)),
                                   ({'R': range(30), 'D': range(30)}, (68, 27))]:
            hw = Hardware(controls, step=2000)
            state = load_example('05_collect_the_dot', hw).main(max_frames=30)
            self.assertEqual((state['x'], state['y']), expected)
        hw = Hardware({'B': [0]})
        load_example('05_collect_the_dot', hw).main()
        self.assertEqual(hw.frames, 0)

    def test_06_start_accumulates_wrap_safe_tenths_and_draws(self):
        hw = Hardware({'A': [0, 1]}, step=100, start=Hardware.PERIOD - 50)
        module = load_example('06_stopwatch', hw)
        state = module.main(max_frames=5)
        self.assertEqual(hw.frames, 5)
        self.assertTrue(state['running'])
        self.assertEqual(state['elapsed_ms'], 400)
        self.assertTrue(any(text == b'00:00.4' for _, text, _, _ in hw.texts))
        self.assertEqual(hw.font, ('/lib/font5x7.bin', 5, 7, 1))
        for control in ('A: start/pause', 'L: reset', 'B: exit'):
            self.assertIn(control, module.__doc__)

    def test_06_pause_resume_reset_exit_and_bounded_minutes(self):
        hw = Hardware({'A': [0, 1, 3, 6], 'B': [9]}, step=100,
                      start=Hardware.PERIOD - 250)
        state = load_example('06_stopwatch', hw).main(max_frames=20)
        self.assertEqual(hw.frames, 9)
        self.assertEqual(state['elapsed_ms'], 500)
        self.assertTrue(state['running'])
        paused = [t for f, t, x, y in hw.texts if y == 12 and 3 <= f <= 6]
        self.assertEqual(paused, [b'00:00.3'] * 4)
        hw = Hardware({'A': [0, 4], 'L': [4, 5]}, step=100)
        state = load_example('06_stopwatch', hw).main(max_frames=6)
        self.assertEqual(state, {'elapsed_ms': 0, 'running': False})
        # Many individually valid (< half period) intervals, crossing wrap
        # repeatedly. Stop at 99:59.9 instead of widening/rolling the label.
        hw = Hardware({'A': [0]}, step=400000)
        state = load_example('06_stopwatch', hw).main(max_frames=20)
        self.assertEqual(state['elapsed_ms'], 5999900)
        self.assertFalse(state['running'])
        self.assertEqual([t for _, t, _, y in hw.texts if y == 12][-1], b'99:59.9')
        hw = Hardware({'B': [0]})
        load_example('06_stopwatch', hw).main()
        self.assertEqual(hw.frames, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
