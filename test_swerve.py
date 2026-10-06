import importlib.util
import pathlib
import unittest

PATH = pathlib.Path(__file__).with_name('swerve.py')

def load():
    spec = importlib.util.spec_from_file_location('swerve', PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class Tests(unittest.TestCase):
    def test_perspective_cars_grow_and_follow_driver_view(self):
        m = load()
        self.assertTrue(hasattr(m, 'project_car'), 'Perspective projection is missing')
        far = m.project_car(32, 0, 32)
        near = m.project_car(32, 34, 32)
        self.assertGreater(near[2], far[2])
        self.assertGreater(near[3], far[3])
        self.assertGreater(near[1] + near[3], far[1] + far[3])
        self.assertAlmostEqual(near[0] + near[2] / 2, 36, delta=1)
        right_view = m.project_car(32, 34, 45)
        self.assertLess(right_view[0], near[0])

    def test_initial_state(self):
        self.assertTrue(PATH.exists(), 'The game script has not been built yet')
        g = load().Game()
        self.assertEqual(g.state, 'title')
        self.assertEqual(g.score, 0)
        self.assertEqual(g.x, 32)

    def test_start_steering_and_bounds(self):
        g = load().Game()
        self.assertTrue(hasattr(g, 'step'), 'Gameplay update is missing')
        g.step(33, False, False, False, True, False, 1)
        self.assertEqual(g.state, 'play')
        g.step(100, True, False, False, False, False, 1)
        self.assertLess(g.x, 32)
        for _ in range(30):
            g.step(100, True, False, False, False, False, 0)
        self.assertGreaterEqual(g.x, 17)
        g.cars = []
        for _ in range(30):
            g.step(100, False, True, False, False, False, 0)
            g.cars = []
        self.assertLessEqual(g.x, 48)
        g.step(33, False, False, False, False, True, 0)
        self.assertEqual(g.state, 'quit')

    def test_traffic_collision_scoring_and_retry(self):
        g = load().Game()
        g.step(33, False, False, False, True, False, 0)
        g.spawn = 0
        g.step(33, False, False, False, False, False, 2)
        self.assertEqual(len(g.cars), 1, 'Traffic never spawned')
        self.assertEqual(g.cars[0][0], 45)
        g.cars = [[19, 39]]
        g.step(100, False, False, False, False, False, 0)
        self.assertEqual(g.score, 1)
        self.assertEqual(g.cars, [])
        g.cars = [[32, 35]]
        g.step(33, False, False, False, False, False, 0)
        self.assertEqual(g.state, 'crash')
        self.assertEqual(g.best, 1)
        g.step(33, False, False, False, True, False, 0)
        self.assertEqual(g.state, 'play')
        self.assertEqual(g.cars, [])
        self.assertEqual(g.score, 0)
        self.assertEqual(g.best, 1)

    def test_fast_car_entering_hitbox_is_detected_immediately(self):
        g = load().Game()
        g.step(33, False, False, False, True, False, 0)
        g.elapsed = 200000
        g.cars = [[32, 32]]
        g.step(100, False, False, True, False, False, 0)
        self.assertEqual(g.state, 'crash')

    def test_distant_car_is_not_a_collision(self):
        g = load().Game()
        g.step(33, False, False, False, True, False, 0)
        g.cars = [[32, 25]]
        g.step(33, False, False, False, False, False, 0)
        self.assertEqual(g.state, 'play', 'An approaching car collided before reaching the bonnet')

    def test_driver_view_road_widens_toward_bonnet(self):
        m = load()
        class Buffer:
            BLACK = 0
            WHITE = 1
            def fill(self, colour):
                self.pixels = [[colour] * 72 for _ in range(40)]
            def drawFilledRectangle(self, x, y, w, h, colour):
                for row in range(y, y + h):
                    for col in range(x, x + w):
                        self.pixels[row][col] = colour
            def update(self):
                pass
        d = Buffer()
        g = m.Game()
        g.state = 'play'
        m.draw(d, g)
        far = [x for x in range(72) if d.pixels[14][x]]
        near = [x for x in range(72) if d.pixels[30][x]]
        self.assertTrue(far and near)
        self.assertLess(max(far) - min(far), max(near) - min(near))
        self.assertEqual(d.pixels[39][36], 1, 'The bonnet should be visible at the bottom')

    def test_render_and_real_entry_loop(self):
        import sys
        import types
        m = load()
        self.assertTrue(hasattr(m, 'main'), 'The display and input loop is missing')
        class Display:
            BLACK = 0
            WHITE = 1
            def __init__(self):
                self.frames = 0
                self.rectangles = 0
            def setFPS(self, fps):
                self.fps = fps
            def fill(self, colour):
                pass
            def drawFilledRectangle(self, x, y, w, h, colour):
                assert 0 <= x < 72 and 0 <= y < 40
                assert w > 0 and h > 0 and x + w <= 72 and y + h <= 40
                self.rectangles += 1
            def update(self):
                self.frames += 1
        d = Display()
        class Button:
            def __init__(self, role):
                self.role = role
            def pressed(self):
                return self.role == 'right' and 2 <= d.frames < 7
            def justPressed(self):
                return (self.role == 'a' and d.frames == 1) or (self.role == 'b' and d.frames == 12)
        fake = types.SimpleNamespace(display=d, buttonL=Button('left'), buttonR=Button('right'), buttonA=Button('a'), buttonB=Button('b'))
        old_k = sys.modules.get('kepoco')
        old_t = sys.modules.get('time')
        sys.modules['kepoco'] = fake
        sys.modules['time'] = types.SimpleNamespace(ticks_ms=lambda: d.frames * 33, ticks_diff=lambda a, b: a - b)
        try:
            m.main()
        finally:
            if old_k is None:
                sys.modules.pop('kepoco', None)
            else:
                sys.modules['kepoco'] = old_k
            sys.modules['time'] = old_t
        self.assertEqual(d.fps, 30)
        self.assertEqual(d.frames, 13)
        self.assertGreater(d.rectangles, 100)
        g = m.Game()
        g.state = 'crash'
        g.best = 100000
        m.draw(d, g)
        g.state = 'play'
        g.cars = [[19, -3], [45, 39]]
        g.score = 100000
        m.draw(d, g)

if __name__ == '__main__':
    unittest.main(verbosity=2)
