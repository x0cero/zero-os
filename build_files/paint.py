#!/usr/bin/env python3
"""Paints the Zero OS pictures at build time: the wallpaper and the mark.

The PNGs are written by hand so the build needs nothing but Python.
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


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))


def smooth(t):
    return t * t * (3 - 2 * t)


def wallpaper(path, width, height):
    """A wide, soft sweep of colour: warm light in the top left falling
    into a deep blue in the bottom right, with a lift of rose across the
    middle. No mark, no text; the desktop is not a billboard."""
    warm = (0xF3, 0xEC, 0xE2, 255)
    rose = (0xD9, 0xA8, 0xB4, 255)
    blue = (0x2E, 0x3F, 0x6E, 255)
    night = (0x14, 0x1B, 0x33, 255)
    canvas = Canvas(width, height, night)
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            t = (x / width * 0.55 + y / height * 0.45)
            # A gentle wave so the bands are not dead straight.
            t += 0.06 * math.sin(y / height * 4.2 + x / width * 2.1)
            t = min(1.0, max(0.0, t))
            if t < 0.35:
                c = lerp(warm, rose, smooth(t / 0.35))
            elif t < 0.72:
                c = lerp(rose, blue, smooth((t - 0.35) / 0.37))
            else:
                c = lerp(blue, night, smooth((t - 0.72) / 0.28))
            row += bytes(c)
        rows.append(bytes(row))
    canvas.pixels = bytearray(b"".join(rows))
    canvas.write(path)


def main(out):
    wallpaper(os.path.join(out, "wallpaper", "zero.png"), 2560, 1600)

    for size in (16, 22, 24, 32, 48, 64, 128, 256):
        icon = Canvas(size, size, CLEAR)
        mark(icon, size / 2, size / 2, size * 0.78, INK, CLEAR)
        icon.write(os.path.join(out, "mark", f"zero-mark-{size}.png"))
        light = Canvas(size, size, CLEAR)
        mark(light, size / 2, size / 2, size * 0.78, PAPER, CLEAR)
        light.write(os.path.join(out, "mark", f"zero-mark-light-{size}.png"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/zero-paint")
