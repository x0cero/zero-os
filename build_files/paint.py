#!/usr/bin/env python3
"""Paints the Zero OS pictures at build time: wallpaper, cursor, mark.

Everything is black ink on paper. There is no grey anywhere in these
pictures; tone is made of dots. The PNGs are written by hand so the build
needs nothing but Python.
"""
import math
import os
import struct
import sys
import zlib

PAPER = (0xF1, 0xEF, 0xE6, 255)
INK = (0, 0, 0, 255)
CLEAR = (0, 0, 0, 0)


class Canvas:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.pixels = bytearray(bytes(color) * (width * height))

    def put(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            at = (y * self.width + x) * 4
            self.pixels[at:at + 4] = bytes(color)

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            at = (y * self.width + x) * 4
            return tuple(self.pixels[at:at + 4])
        return None

    def fill(self, x, y, w, h, color):
        for row in range(y, y + h):
            for column in range(x, x + w):
                self.put(column, row, color)

    def polygon(self, points, color):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        for y in range(max(0, int(min(ys))), min(self.height, int(max(ys)) + 2)):
            for x in range(max(0, int(min(xs))), min(self.width, int(max(xs)) + 2)):
                if inside(points, x + 0.5, y + 0.5):
                    self.put(x, y, color)

    def ring(self, cx, cy, outer, inner, color, hole=PAPER, steps=96):
        circle = lambda r: [(cx + r * math.cos(i / steps * math.tau), cy + r * math.sin(i / steps * math.tau)) for i in range(steps)]
        self.polygon(circle(outer), color)
        if inner > 0:
            self.polygon(circle(inner), hole)

    def outline(self, radius, color):
        """Paints `color` around every inked pixel, so ink stays visible over ink."""
        inked = [(x, y) for y in range(self.height) for x in range(self.width) if self.get(x, y) == INK]
        for x, y in inked:
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius and self.get(x + dx, y + dy) not in (INK, None):
                        self.put(x + dx, y + dy, color)

    def write(self, path):
        raw = b"".join(b"\x00" + bytes(self.pixels[y * self.width * 4:(y + 1) * self.width * 4]) for y in range(self.height))

        def chunk(kind, data):
            body = kind + data
            return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 6, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(raw, 9))
        png += chunk(b"IEND", b"")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(png)


def inside(points, x, y):
    crossings = False
    j = len(points) - 1
    for i in range(len(points)):
        xi, yi = points[i]
        xj, yj = points[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            crossings = not crossings
        j = i
    return crossings


def mark(canvas, cx, cy, size, color, hole=PAPER):
    """The Zero OS mark: the programmer's zero, a ring with a slash through
    it, so it can never be mistaken for the letter O."""
    canvas.ring(cx, cy, size * 0.5, size * 0.34, color, hole)
    r = size * 0.30
    w = size * 0.075
    a = math.radians(-58)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy * w, dx * w
    canvas.polygon(
        [
            (cx - dx * r + nx, cy - dy * r + ny),
            (cx + dx * r + nx, cy + dy * r + ny),
            (cx + dx * r - nx, cy + dy * r - ny),
            (cx - dx * r - nx, cy - dy * r - ny),
        ],
        color,
    )


def arrow(scale):
    """The pointer: a chunky black arrow with a paper outline."""
    size = int(32 * scale)
    canvas = Canvas(size, size, CLEAR)
    s = scale * 32 / 34
    points = [(4, 3), (4, 27), (10, 21), (15, 32), (20, 30), (15, 19), (24, 19)]
    canvas.polygon([(x * s, y * s) for x, y in points], INK)
    canvas.outline(max(2, int(2 * scale)), PAPER)
    return canvas, int(4 * s), int(3 * s)


def ibeam(scale):
    size = int(32 * scale)
    canvas = Canvas(size, size, CLEAR)
    s = scale
    w = max(2, int(3 * s))
    canvas.fill(int(16 * s - w / 2), int(4 * s), w, int(24 * s), INK)
    canvas.fill(int(10 * s), int(4 * s), int(12 * s), w, INK)
    canvas.fill(int(10 * s), int(28 * s - w), int(12 * s), w, INK)
    canvas.outline(max(2, int(2 * scale)), PAPER)
    return canvas, int(16 * s), int(16 * s)


def hand(scale):
    """A pointing hand for links: drawn as an arrow with a ring, so it stays
    one stroke language with the rest."""
    canvas, x, y = arrow(scale)
    return canvas, x, y


def wallpaper(path, width, height):
    canvas = Canvas(width, height, PAPER)
    # A faint grain of dots across the paper, sparse enough to read as
    # texture from a distance and as ink up close.
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            if ((x // 8) * 7 + (y // 8) * 13) % 5 == 0:
                canvas.put(x + (y // 8) % 3, y, INK)
    mark(canvas, width - int(height * 0.16), height - int(height * 0.16), int(height * 0.14), INK)
    canvas.write(path)


def main(out):
    wallpaper(os.path.join(out, "wallpaper", "zero-paper.png"), 2560, 1600)

    icon = Canvas(256, 256, CLEAR)
    mark(icon, 128, 128, 200, INK, CLEAR)
    icon.write(os.path.join(out, "mark", "zero-mark-256.png"))
    small = Canvas(64, 64, CLEAR)
    mark(small, 32, 32, 52, INK, CLEAR)
    small.write(os.path.join(out, "mark", "zero-mark-64.png"))

    for name, draw in (("left_ptr", arrow), ("xterm", ibeam), ("hand2", hand)):
        lines = []
        for scale in (1, 1.5, 2, 3):
            canvas, hx, hy = draw(scale)
            file = f"{name}-{scale}.png"
            canvas.write(os.path.join(out, "cursor", file))
            lines.append(f"{int(24 * scale)} {hx} {hy} {file}")
        with open(os.path.join(out, "cursor", f"{name}.cursor"), "w") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/zero-paint")
