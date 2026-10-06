# SWERVE - driver's-eye Kepoco MicroPython game, 72 x 40.
# Left/right: steer. A: start/retry; hold to boost. B: quit.
class Game:
    def __init__(self):
        self.state = 'title'
        self.score = 0
        self.best = 0
        self.x = 32
        self.cars = []
        self.elapsed = 0
        self.spawn = 700
        self.scroll = 0
        self.boost = False

    def step(self, dt, left, right, boost, start, quit_pressed, lane):
        if quit_pressed:
            self.state = 'quit'
            return
        if self.state != 'play':
            if start:
                self.state = 'play'
                self.score = 0
                self.x = 32
                self.cars = []
                self.elapsed = 0
                self.spawn = 700
                self.scroll = 0
            return
        dt = max(0, min(dt, 100))
        self.x = max(17, min(48, self.x + (int(right) - int(left)) * dt * 0.055))
        self.elapsed += dt
        self.boost = bool(boost)
        speed = min(0.048, 0.019 + self.elapsed * 0.00000025)
        if self.boost:
            speed *= 1.5
        movement = dt * speed
        self.scroll = (self.scroll + movement) % 10
        for car in self.cars:
            old_y = car[1]
            car[1] += movement
            # World-space overlap; contact only when traffic reaches the bonnet.
            # Swept depth catches crossings even during a long boosted frame.
            if (self.x + 6 > car[0] + 1 and self.x + 1 < car[0] + 6
                    and car[1] >= 35 and old_y < 40):
                self.state = 'crash'
                self.best = max(self.best, self.score)
                return
        for i in range(len(self.cars) - 1, -1, -1):
            if self.cars[i][1] >= 40:
                self.score += 1
                del self.cars[i]
        self.spawn -= dt
        if self.spawn <= 0:
            self.cars.append([19 + (lane % 3) * 13, -1.0])
            # At least 23 pixels between cars, so there is always a gap.
            self.spawn += 23 / speed


# Built-in 3x5 font: no font files, sprites or other assets to install.
FONT = {
    '0': (7,5,5,5,7), '1': (2,6,2,2,7), '2': (7,1,7,4,7),
    '3': (7,1,7,1,7), '4': (5,5,7,1,1), '5': (7,4,7,1,7),
    '6': (7,4,7,5,7), '7': (7,1,2,2,2), '8': (7,5,7,5,7),
    '9': (7,5,7,1,7), 'A': (2,5,7,5,5), 'B': (6,5,6,5,6),
    'C': (7,4,4,4,7), 'E': (7,4,6,4,7), 'H': (5,5,7,5,5),
    'I': (7,2,2,2,7), 'L': (4,4,4,4,7), 'O': (7,5,5,5,7),
    'R': (6,5,6,5,5), 'S': (7,4,7,1,7), 'T': (7,2,2,2,2),
    'V': (5,5,5,5,2), 'W': (5,5,5,7,5), 'X': (5,5,2,5,5),
    'Y': (5,5,2,2,2), ':': (0,2,0,2,0), '!': (2,2,2,0,2),
    '<': (1,2,4,2,1), '>': (4,2,1,2,4)
}


def text(d, message, y, scale=1):
    x = (72 - (len(message) * 4 - 1) * scale) // 2
    for ch in message:
        rows = FONT.get(ch, (0,0,0,0,0))
        for row in range(5):
            for col in range(3):
                if rows[row] & (4 >> col):
                    d.drawFilledRectangle(x + col * scale, y + row * scale,
                                          scale, scale, d.WHITE)
        x += 4 * scale


def rect(d, x, y, w, h, colour):
    # Clip sprites to the road, leaving the score area untouched.
    x, y = int(x), int(y)
    right, bottom = min(72, x + w), min(40, y + h)
    x, y = max(0, x), max(8, y)
    if right > x and bottom > y:
        d.drawFilledRectangle(x, y, right - x, bottom - y, colour)


def project_car(world_x, progress, driver_x):
    depth = max(0.0, min(1.15, (progress + 1) / 41.0))
    perspective = depth * depth
    half_road = 4 + 32 * perspective
    width = max(3, int(3 + 19 * perspective))
    height = max(2, int(width * 0.55))
    centre = 36 + (world_x - driver_x) * half_road / 19.5
    bottom = int(11 + 32 * perspective)
    return (int(centre - width / 2), bottom - height, width, height)


def car(d, x, y, w, h):
    # Front view: roof, dark windscreen, headlights and bumper.
    roof = max(1, w // 5)
    rect(d, x + roof, y, w - 2 * roof, h, d.WHITE)
    rect(d, x, y + h // 2, w, h - h // 2, d.WHITE)
    if w >= 7:
        rect(d, x + roof + 1, y + 1, max(1, w - 2 * roof - 2),
             max(1, h // 3), d.BLACK)
        rect(d, x + 1, y + h - 2, w - 2, 1, d.BLACK)
        rect(d, x + 1, y + h // 2, 1, 1, d.BLACK)
        rect(d, x + w - 2, y + h // 2, 1, 1, d.BLACK)


def road(d, g):
    # Scanlines form a trapezoid; steering moves the view, not a player sprite.
    for y in range(11, 37):
        half = 4 + (y - 11)
        centre = 36 + (32 - g.x) * half / 19.5
        rect(d, centre - half, y, 1, 1, d.WHITE)
        rect(d, centre + half, y, 1, 1, d.WHITE)
    for progress in range(0, 40, 10):
        p = (progress + g.scroll) % 40
        start = ((p + 1) / 41.0) ** 2
        end = ((p + 5) / 41.0) ** 2
        for y in range(int(11 + 32 * start), int(11 + 32 * end) + 1):
            if y > 36:
                continue
            half = 4 + y - 11
            for lane_edge in (25.5, 38.5):
                x = 36 + (lane_edge - g.x) * half / 19.5
                rect(d, x, y, 1, 1, d.WHITE)


def bonnet(d, boost):
    rect(d, 27, 35, 18, 1, d.WHITE)
    rect(d, 23, 36, 26, 1, d.WHITE)
    rect(d, 18, 37, 36, 1, d.WHITE)
    rect(d, 15, 38, 42, 1, d.WHITE)
    rect(d, 12, 39, 48, 1, d.WHITE)
    rect(d, 30, 37, 1, 3, d.BLACK)
    rect(d, 41, 37, 1, 3, d.BLACK)
    if boost:
        rect(d, 3, 32, 1, 5, d.WHITE)
        rect(d, 68, 32, 1, 5, d.WHITE)


def draw(d, g):
    d.fill(d.BLACK)
    if g.state == 'title':
        text(d, 'SWERVE', 2, 2)
        text(d, '< STEER >', 17)
        text(d, 'A START', 26)
        text(d, 'B EXIT', 34)
    elif g.state == 'crash':
        text(d, 'CRASH!', 1, 2)
        text(d, 'S:' + str(min(g.score, 99999)), 15)
        text(d, 'BEST:' + str(min(g.best, 99999)), 23)
        text(d, 'A RETRY', 34)
    elif g.state == 'play':
        text(d, 'S:' + str(min(g.score, 99999)), 1)
        road(d, g)
        # Newest cars are furthest away: draw them first for correct occlusion.
        for i in range(len(g.cars) - 1, -1, -1):
            item = g.cars[i]
            x, y, w, h = project_car(item[0], item[1], g.x)
            car(d, x, y, w, h)
        bonnet(d, g.boost)
    d.update()


def main():
    from kepoco import display, buttonL, buttonR, buttonA, buttonB
    import time
    import random
    display.setFPS(30)
    game = Game()
    last = time.ticks_ms()
    while game.state != 'quit':
        now = time.ticks_ms()
        dt = time.ticks_diff(now, last)
        last = now
        start = buttonA.justPressed()
        quit_pressed = buttonB.justPressed()
        game.step(dt, buttonL.pressed(), buttonR.pressed(),
                  buttonA.pressed(), start, quit_pressed, random.getrandbits(8))
        draw(display, game)


if __name__ == '__main__':
    main()
