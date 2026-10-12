# -*- coding: utf-8 -*-
"""
Reusable 'fill the frame' painters (paper style) used to remove large empty areas:
distant silhouettes, cloud banks, foreground framing foliage, ground scatter, wall decoration.
All of them are deterministic (seeded), so both pictures get exactly the same filler.
"""
import math
import random

from fdcore import H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union, star_pts

PROP = (2, 4, 7, 0.42)
SMALL = (1, 2, 3, 0.3)
LAYER = (1, 3, 11, 0.36)


# ------------------------------------------------------------------- distance
def far_ridge(c, base, amp, col, seed, step=60, shadow=LAYER, x0=-40, x1=W + 40):
    rnd = random.Random(seed)
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, base - rnd.uniform(0.2, 1.0) * amp))
        x += step * rnd.uniform(0.6, 1.3)
    pts.append((x1, base - rnd.uniform(0.2, 1.0) * amp))
    piece(c, Poly(pts + [(x1, base + 400), (x0, base + 400)]), col, shadow=shadow)


def far_forest(c, base, h, col, seed, spacing=26, x0=-20, x1=W + 20):
    rnd = random.Random(seed)
    shapes = []
    x = x0
    while x < x1:
        hh = h * rnd.uniform(0.7, 1.2)
        w = hh * 0.32
        shapes.append(Poly([(x, base - hh), (x - w, base), (x + w, base)]))
        x += spacing * rnd.uniform(0.7, 1.3)
    shapes.append(RRect(x0, base - 2, x1, base + 300, 0))
    piece(c, shapes, col, shadow=LAYER)


def far_round_trees(c, base, r, col, seed, spacing=40, x0=-20, x1=W + 20):
    rnd = random.Random(seed)
    shapes = [RRect(x0, base - r * 0.4, x1, base + 300, 0)]
    x = x0
    while x < x1:
        rr = r * rnd.uniform(0.7, 1.2)
        shapes.append(Circ(x, base - rr * 0.5, rr))
        x += spacing * rnd.uniform(0.7, 1.2)
    piece(c, shapes, col, shadow=LAYER)


def far_skyline(c, base, hmin, hmax, col, seed, win=None, x0=-20, x1=W + 20):
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w, h = rnd.randint(30, 70), rnd.randint(hmin, hmax)
        piece(c, RRect(x, base - h, x + w, base + 300, 1), col, shadow=None)
        if rnd.random() < 0.4:
            flat(c, Thick(x + w / 2, base - h, x + w / 2, base - h - 20, 2), col)
        if win:
            for y in range(int(base - h) + 8, int(base) - 4, 12):
                for xx in range(x + 5, x + w - 6, 10):
                    if rnd.random() < 0.3:
                        flat(c, RRect(xx, y, xx + 4, y + 5, 0.5), win)
        x += w + rnd.randint(1, 6)


def cloud_bank(c, y, col, seed, k=1.0, x0=-60, x1=W + 60, shadow=(1, 3, 8, 0.2)):
    rnd = random.Random(seed)
    shapes = [RRect(x0, y, x1, y + 40 * k, 0)]
    x = x0
    while x < x1:
        r = rnd.uniform(26, 50) * k
        shapes.append(Circ(x, y + rnd.uniform(-6, 10) * k, r))
        x += r * 1.3
    piece(c, shapes, col, shadow=shadow)


def puffs(c, items, col=(252, 252, 248), shadow=PROP):
    for x, y, k in items:
        piece(c, [Circ(x - 26 * k, y + 9 * k, 20 * k), Circ(x, y, 26 * k), Circ(x + 28 * k, y + 10 * k, 20 * k),
                  RRect(x - 56 * k, y + 8 * k, x + 56 * k, y + 26 * k, 9 * k)], col, shadow=shadow)


def birds(c, items, col=(80, 85, 100)):
    for x, y, s in items:
        flat(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.22), Thick(x, y, x + s, y - s * 0.4, s * 0.22)], col)


# ------------------------------------------------------------------- framing foreground
def corner_foliage(c, corner, col, seed, size=1.0, leaf=None):
    """Leafy branch reaching in from a picture corner: 'tl', 'tr', 'bl', 'br'."""
    rnd = random.Random(seed)
    sx = -1 if corner[1] == "l" else 1
    sy = -1 if corner[0] == "t" else 1
    cx, cy = (0 if sx < 0 else W), (0 if sy < 0 else H)
    shapes = []
    for k in range(9):
        a = rnd.uniform(0, math.pi / 2)
        dist = rnd.uniform(40, 150) * size
        x = cx - sx * math.cos(a) * dist
        y = cy - sy * math.sin(a) * dist
        r = rnd.uniform(28, 52) * size
        shapes.append(Circ(x, y, r))
    piece(c, shapes, col, shadow=PROP)
    for k in range(6):
        a = rnd.uniform(0.1, math.pi / 2 - 0.1)
        dist = rnd.uniform(60, 140) * size
        x = cx - sx * math.cos(a) * dist
        y = cy - sy * math.sin(a) * dist
        flat(c, Circ(x, y, rnd.uniform(10, 18) * size), leaf or lit(col, 1.18))


def hanging_vines(c, xs, length, col, seed):
    rnd = random.Random(seed)
    for x in xs:
        ln = length * rnd.uniform(0.6, 1.2)
        pts = [(x + 6 * math.sin(t * 0.8), t * ln / 8) for t in range(9)]
        flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 2.5) for i in range(8)], lit(col, 0.8))
        for i in range(1, 9):
            piece(c, Ell(pts[i][0] + (5 if i % 2 else -5), pts[i][1], 7, 4), col, shadow=None)


def side_bushes(c, base_fn, col, seed, xs=(20, 60, 840, 880), s=1.2):
    for x in xs:
        b = base_fn(x)
        piece(c, [Circ(x - 14 * s, b - 10 * s, 15 * s), Circ(x + 4 * s, b - 18 * s, 18 * s), Circ(x + 20 * s, b - 8 * s, 13 * s)],
              col, shadow=PROP)


# ------------------------------------------------------------------- ground scatter
def scatter(c, area, n, seed, kinds, avoid=()):
    """kinds: list of (weight, painter(c, x, y, rnd)). avoid: rects (x0, y0, x1, y1) kept free."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = area
    total = sum(w for w, _ in kinds)
    placed = 0
    tries = 0
    pts = []
    while placed < n and tries < n * 20:
        tries += 1
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if any(a <= x <= b and cc <= y <= dd for a, cc, b, dd in avoid):
            continue
        pts.append((y, x, rnd.random() * total, rnd.random()))
        placed += 1
    for y, x, pick, r in sorted(pts):
        acc = 0
        for w, painter in kinds:
            acc += w
            if pick <= acc:
                painter(c, x, y, random.Random(int(x * 13 + y * 7)))
                break


def tuft(col):
    def p(c, x, y, rnd):
        flat(c, Poly([(x - 7, y), (x - 4, y - 12), (x - 1, y - 2), (x + 2, y - 14), (x + 5, y - 2), (x + 8, y)]), col)
    return p


def pebble(col):
    def p(c, x, y, rnd):
        r = rnd.uniform(5, 11)
        piece(c, Ell(x, y, r * 1.3, r * 0.8), col, shadow=SMALL)
        flat(c, Ell(x - r * 0.3, y - r * 0.3, r * 0.5, r * 0.3), lit(col, 1.15))
    return p


def flowerlet(cols):
    def p(c, x, y, rnd):
        col = rnd.choice(cols)
        flat(c, Thick(x, y, x, y + 10, 1.6), (70, 140, 70))
        piece(c, [Circ(x + 4 * math.cos(a), y + 4 * math.sin(a), 3.4) for a in (0, 1.26, 2.5, 3.8, 5.0)], col, shadow=None)
        flat(c, Circ(x, y, 2), (255, 240, 160))
    return p


def shrub(col):
    def p(c, x, y, rnd):
        s = rnd.uniform(0.6, 1.1)
        piece(c, [Circ(x - 10 * s, y - 6 * s, 10 * s), Circ(x + 2 * s, y - 12 * s, 13 * s), Circ(x + 13 * s, y - 5 * s, 9 * s)], col, shadow=PROP)
    return p


# ------------------------------------------------------------------- walls
def wallpaper_stripes(c, rect, a, b, w=18):
    x0, y0, x1, y1 = rect
    flat(c, RRect(x0, y0, x1, y1, 0), a)
    x = x0
    while x < x1:
        flat(c, RRect(x, y0, min(x1, x + w / 2), y1, 0), b)
        x += w


def wallpaper_diamonds(c, rect, a, b, s=26):
    x0, y0, x1, y1 = rect
    flat(c, RRect(x0, y0, x1, y1, 0), a)
    for y in range(int(y0), int(y1) + s, s):
        for x in range(int(x0) - s, int(x1) + s, s):
            ox = (y // s % 2) * s / 2
            flat(c, Poly([(x + ox, y - s * 0.3), (x + ox + s * 0.2, y), (x + ox, y + s * 0.3), (x + ox - s * 0.2, y)]), b)


def wall_tiles(c, rect, a, line, s=30):
    x0, y0, x1, y1 = rect
    flat(c, RRect(x0, y0, x1, y1, 0), a)
    for y in range(int(y0), int(y1), s):
        flat(c, Thick(x0, y, x1, y, 1.2), line)
    for x in range(int(x0), int(x1), s):
        flat(c, Thick(x, y0, x, y1, 1.2), line)


def picture_frame(c, x, y, w, h, frame, art_cols, seed=0):
    rnd = random.Random(seed)
    piece(c, RRect(x, y, x + w, y + h, 2), frame, border=1.5, shadow=PROP)
    flat(c, RRect(x + 5, y + 5, x + w - 5, y + h - 5, 1), art_cols[0])
    flat(c, Poly([(x + 5, y + h - 5), (x + w * 0.4, y + h * 0.45), (x + w * 0.65, y + h * 0.65), (x + w - 5, y + h * 0.35), (x + w - 5, y + h - 5)]),
         art_cols[1 % len(art_cols)])
    if len(art_cols) > 2:
        flat(c, Circ(x + w * 0.75, y + h * 0.3, min(w, h) * 0.1), art_cols[2])


def shelf(c, x0, x1, y, wood, items_seed, cols):
    flat(c, Thick(x0, y, x1, y, 4), wood)
    rnd = random.Random(items_seed)
    x = x0 + 6
    while x < x1 - 12:
        kind = rnd.random()
        col = rnd.choice(cols)
        if kind < 0.5:
            w = rnd.uniform(8, 12)
            piece(c, RRect(x, y - rnd.uniform(18, 28), x + w, y - 1, 2), col, shadow=SMALL)
            x += w + 2
        elif kind < 0.8:
            piece(c, [Ell(x + 7, y - 8, 7, 8), RRect(x + 4, y - 20, x + 10, y - 14, 1)], col, shadow=SMALL)
            x += 18
        else:
            piece(c, Ell(x + 9, y - 4, 10, 4), col, shadow=SMALL)
            x += 22
