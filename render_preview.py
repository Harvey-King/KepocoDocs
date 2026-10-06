"""Render actual game drawing calls as an enlarged PNG, no dependencies."""
import pathlib
import struct
import zlib
import swerve

class Display:
    BLACK = 0
    WHITE = 1
    def __init__(self):
        self.pixels = [[0] * 72 for _ in range(40)]
    def fill(self, colour):
        self.pixels = [[colour] * 72 for _ in range(40)]
    def drawFilledRectangle(self, x, y, w, h, colour):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.pixels[yy][xx] = colour
    def update(self):
        pass

def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)

panels = []
g = swerve.Game()
d = Display()
swerve.draw(d, g)
panels.append(d.pixels)
g.state = 'play'
g.score = 12
g.cars = [[45, 34], [19, 12]]
g.scroll = 4
swerve.draw(d, g)
panels.append(d.pixels)
g.state = 'crash'
g.best = 21
swerve.draw(d, g)
panels.append(d.pixels)
scale = 6
width = 72 * scale
height = (40 * 3 + 8 * 2) * scale
raw = bytearray()
rows = []
for n, panel in enumerate(panels):
    if n:
        rows.extend([[0] * 72 for _ in range(8)])
    rows.extend(panel)
for row in rows:
    scanline = bytes([0]) + bytes(255 if pixel else 0 for pixel in row for _ in range(scale))
    for _ in range(scale):
        raw.extend(scanline)
data = b'\x89PNG\r\n\x1a\n'
data += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0))
data += chunk(b'IDAT', zlib.compress(bytes(raw))) + chunk(b'IEND', b'')
path = pathlib.Path(__file__).with_name('preview.png')
path.write_bytes(data)
print('Rendered actual title, gameplay and crash screens:', path.resolve())
