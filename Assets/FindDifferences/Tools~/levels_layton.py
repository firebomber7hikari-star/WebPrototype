# -*- coding: utf-8 -*-
"""Storybook puzzle-adventure levels in the manner of the Professor Layton games' look (warm hand-painted
watercolour, thin dark-brown ink lines, soft edge-darkening, crooked tall European houses, sepia-warm light).
Every place and character is original (no characters, logos or text from the series).
  Level1644 坡上小镇   - a hillside town of crooked houses under a windmill-clock tower at golden hour
  Level1645 教授书房   - a scholar's study crammed with books, puzzle boxes, a globe, a telescope and tea
  Level1646 蒸汽餐车   - the dining car of a steam train rolling through the countryside
  Level1647 黄昏游园会 - a fairground at dusk: carousel, balloon seller, Ferris wheel, string lights
  Level1648 钟表匠工坊 - a clockmaker's shop full of clocks, gears, a cuckoo clock and a workbench
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (C, Box, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, el, fbm, fbm1, mixc, real_post,
                  smooth, vgrad)
from toon import Grow
from styled_kit import sparkle_el

INK = (74, 52, 40)


class LaytonS:
    """Watercolour storybook style: thin brown ink outline, mottled wash, darker pooled edges, soft lower-right shade."""
    name = "layton"
    haze = (236, 214, 176)

    def sky(self, g, stops, y1=H):
        g.fill(Box(-2, -2, W + 2, y1), vgrad(stops))
        g.fill(Box(-2, -2, W + 2, y1), (255, 250, 236), alpha=lambda X, Y: 0.18 * smooth(0.5, 0.8, fbm(X, Y, 90, 40, 3, 11)))

    def _wash(self, col, seed, depth):
        c = C(mixc(col, self.haze, depth * 0.55))

        def f(X, Y):
            n = fbm(X, Y, 18, 14, 3, seed)
            n2 = fbm(X, Y, 3, 3, 2, seed + 5)
            return c * (0.9 + 0.16 * n + 0.05 * n2)[..., None]
        return f

    def obj(self, g, shape, col, seed=0, kind="plain", depth=0.0, line=True, hi=False):
        if line:
            g.fill(Grow(shape, 1.3 * (1 - depth * 0.7)), mixc(INK, self.haze, depth * 0.6))
        g.fill(shape, self._wash(col, seed, depth))
        b = shape.bbox()
        w, h = b[2] - b[0], b[3] - b[1]
        o = -min(10, max(2, min(w, h) * 0.14))
        g.mul(Diff(shape, Moved(shape, o, o)), 0.22, tint=(90, 60, 80))
        g.mul(Diff(shape, Grow(shape, -2.2)), 0.12, feather=1.2)
        if kind == "wood":
            g.fill(shape, mixc(col, (0, 0, 0), 0.3), alpha=lambda X, Y: 0.25 * smooth(0.12, 0.0, np.abs((Y / 7.0) % 1.0 - 0.5) - 0.4))
        elif kind == "roof":
            g.fill(shape, mixc(col, (0, 0, 0), 0.35), alpha=lambda X, Y: 0.3 * smooth(0.1, 0.0, np.abs((Y / 6.0) % 1.0 - 0.5) - 0.42))
        elif kind == "brick":
            g.fill(shape, mixc(col, (255, 255, 255), 0.25), alpha=lambda X, Y: 0.25 * (np.abs(np.sin(Y * 0.5)) > 0.92))
        if hi and depth < 0.5:
            g.fill(Ell(b[0] + w * 0.3, b[1] + h * 0.26, w * 0.1, h * 0.07), (255, 250, 236), alpha=0.7)

    def flat(self, g, shape, col):
        g.fill(shape, col)

    def shadow(self, g, shape, k=1.0):
        g.mul(shape, 0.3 * k, feather=6, tint=(80, 50, 70))

    def ground(self, g, shape, col, kind="grass", seed=0, line=False):
        if line:
            g.fill(Grow(shape, 1.3), INK)
        g.fill(shape, self._wash(col, seed, 0.0))

    def water(self, g, shape, top, bottom, seed=0):
        b = shape.bbox()
        g.fill(shape, vgrad([(b[1], top), (b[3], bottom)]))
        rnd = random.Random(seed)
        for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 2600)):
            x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
            g.fill(Inter(Seg(x, y, x + rnd.uniform(12, 30), y, 1.4), shape), (255, 250, 236), alpha=0.6)

    def line(self, g, x0, y0, x1, y1, w=2.0, col=(80, 60, 50)):
        g.fill(Seg(x0, y0, x1, y1, w + 1.2), INK)
        g.fill(Seg(x0, y0, x1, y1, w), col)

    def glow(self, g, x, y, r, col, k=0.4):
        g.glow(x, y, r, col, k)

    def finish(self, g):
        g.grade(contrast=1.03, sat=0.95, warm=7)


S = LaytonS()
OPTS = dict(post=lambda rows, w, h, ox, oy, a: real_post(rows, w, h, ox, oy, a, grain=3.0, vignette=0.22), anim_seconds=12.0, frames=60)


def make(scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, d)
        S.finish(g)
        g.commit()
    return bg


# =================================================================== shared props and original characters
def crooked_house(g, x0, base, w, h, wall, roof, seed, lean=0.0, lit=(), wins=(2, 2), chimney=True, door=True, box_col=None):
    """Tall narrow storybook house that leans a little, with a steep roof and small windows."""
    sk = lambda y: (base - y) * lean
    body = Poly([(x0, base), (x0 + w, base), (x0 + w + sk(base - h), base - h), (x0 + sk(base - h), base - h)])
    S.obj(g, body, wall, seed, "brick")
    top = base - h
    rp = Poly([(x0 - 8 + sk(top), top + 2), (x0 + w / 2 + sk(top) + lean * w * 0.6, top - w * 0.75), (x0 + w + 8 + sk(top), top + 2)])
    if chimney:
        cx = x0 + w * 0.66 + sk(top)
        S.obj(g, Box(cx, top - w * 0.65, cx + w * 0.22, top - w * 0.1), (150, 90, 70), seed + 1, "brick")
    S.obj(g, rp, roof, seed + 2, "roof")
    rows, cols = wins
    for r in range(rows):
        for k in range(cols):
            wx = x0 + w * (0.18 + k * (0.64 / max(1, cols - 1) if cols > 1 else 0.32)) - 7 + sk(base - h * (0.4 + r * 0.3))
            wy = base - h * (0.38 + r * 0.3)
            on = (r, k) in lit
            if on:
                g.glow(wx + 7, wy, 30, (255, 210, 130), 0.3)
            S.obj(g, Union([Box(wx, wy - 10, wx + 14, wy + 10), Circ(wx + 7, wy - 10, 7)]), (255, 214, 140) if on else (110, 130, 150), seed + 3 + r * 5 + k)
            if box_col is not None and r == 0 and k == 0:
                S.obj(g, Box(wx - 8, wy + 10, wx + 22, wy + 20), box_col, seed + 20)
                for fx in (wx - 4, wx + 3, wx + 10, wx + 17):
                    S.obj(g, Circ(fx, wy + 6, 5), (230, 80, 90), seed + 21)
    if door:
        dx = x0 + w * 0.5 - 9 + sk(30)
        S.obj(g, Union([Box(dx, base - 32, dx + 18, base), Circ(dx + 9, base - 32, 9)]), (120, 80, 60), seed + 30, "wood")


def professor(g, x, base, h, face=1, coat=(130, 90, 60), hat=(60, 44, 40), seed=0, scarf=(170, 50, 50)):
    """Original elderly scholar: long coat, bowler hat, round spectacles, walking cane."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    S.shadow(g, Ell(x + 6 * k, base, 50 * k, 7 * k))
    for lx in (-10, 10):
        S.obj(g, Seg(sx(lx), sy(120), sx(lx * 1.2), sy(10), 9 * k, 8 * k), (70, 60, 60), seed)
        S.obj(g, Ell(sx(lx * 1.2 + 6), sy(5), 13 * k, 6 * k), (50, 36, 30), seed + 1)
    S.obj(g, Poly([(sx(-30), sy(236)), (sx(30), sy(236)), (sx(44), sy(70)), (sx(-40), sy(70))]), coat, seed + 2)
    S.obj(g, Seg(sx(26), sy(226), sx(48), sy(130), 9 * k, 8 * k), coat, seed + 3)
    S.obj(g, Seg(sx(50), sy(132), sx(64), sy(6), 2.6 * k), (60, 40, 30), seed + 4)
    S.obj(g, Ell(sx(50), sy(130), 7 * k, 7 * k), (240, 210, 180), seed + 5)
    S.obj(g, Poly([(sx(-16), sy(240)), (sx(16), sy(240)), (sx(10), sy(206)), (sx(-10), sy(206))]), scarf, seed + 6)
    hx, hy = sx(2), sy(262)
    S.obj(g, Ell(hx, hy, 17 * k, 21 * k), (244, 214, 186), seed + 7)
    S.obj(g, Ell(hx + f * 15 * k, hy + 2 * k, 5 * k, 6 * k), (244, 214, 186), seed + 8)
    S.obj(g, Union([Ell(hx - f * 4 * k, hy + 14 * k, 16 * k, 8 * k)]), (220, 220, 220), seed + 9)
    for ex in (4, 13):
        g.fill(Circ(hx + f * ex * k, hy - 3 * k, 4.4 * k) - Circ(hx + f * ex * k, hy - 3 * k, 3.2 * k), INK)
    S.obj(g, Union([Ell(hx, hy - 18 * k, 30 * k, 6 * k), Inter(Ell(hx, hy - 20 * k, 19 * k, 22 * k), Box(hx - 20 * k, hy - 46 * k, hx + 20 * k, hy - 18 * k))]),
          hat, seed + 10)


def apprentice(g, x, base, h, face=1, coat=(80, 120, 170), cap=(200, 80, 60), seed=0):
    """Original young apprentice: newsboy cap, short coat, satchel."""
    k = h / 200.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    S.shadow(g, Ell(x, base, 34 * k, 6 * k))
    for lx in (-8, 8):
        S.obj(g, Box(sx(lx) - 5 * k, sy(80), sx(lx) + 5 * k, sy(6), 2 * k), (70, 70, 90), seed)
        S.obj(g, Ell(sx(lx + 4), sy(4), 9 * k, 5 * k), (60, 40, 30), seed + 1)
    S.obj(g, Box(sx(-22), sy(150), sx(22), sy(72), 6 * k), coat, seed + 2)
    S.obj(g, Box(sx(-30), sy(120), sx(-14), sy(92), 3 * k), (170, 120, 70), seed + 3)
    hx, hy = sx(2), sy(176)
    S.obj(g, Ell(hx, hy, 22 * k, 24 * k), (248, 220, 196), seed + 4)
    S.obj(g, Union([Ell(hx - f * 2 * k, hy - 16 * k, 26 * k, 12 * k), Ell(hx + f * 20 * k, hy - 10 * k, 12 * k, 4 * k)]), cap, seed + 5)
    for ex in (6, 16):
        g.fill(Ell(hx + f * ex * k, hy + 2 * k, 2.6 * k, 3.6 * k), INK)


def lamp(g, x, base, h, lit=True):
    S.obj(g, Box(x - 3, base - h, x + 3, base), (60, 56, 60), 1)
    if lit:
        g.glow(x, base - h - 10, 60, (255, 210, 130), 0.35)
    S.obj(g, Union([Poly([(x - 10, base - h), (x + 10, base - h), (x + 13, base - h - 22), (x - 13, base - h - 22)])]), (255, 220, 150) if lit else (110, 120, 130), 2)
    S.obj(g, Poly([(x - 15, base - h - 22), (x, base - h - 32), (x + 15, base - h - 22)]), (60, 56, 60), 3)


def clock_face(g, x, y, r, hand_a=0.9, hand_b=4.2, col=(246, 236, 210), rim=(170, 130, 70), seed=0):
    S.obj(g, Circ(x, y, r), rim, seed, hi=True)
    S.obj(g, Circ(x, y, r * 0.84), col, seed + 1, line=False)
    for i in range(12):
        a = i * math.tau / 12
        g.fill(Seg(x + math.cos(a) * r * 0.66, y + math.sin(a) * r * 0.66, x + math.cos(a) * r * 0.78, y + math.sin(a) * r * 0.78, 1.4), INK)
    for a, ln, w in ((hand_a, 0.45, 2.4), (hand_b, 0.7, 1.6)):
        aa = a - math.pi / 2
        g.fill(Seg(x, y, x + math.cos(aa) * r * ln, y + math.sin(aa) * r * ln, w), INK)
    g.fill(Circ(x, y, 2.4), INK)


# =================================================================== Level 1644 hillside town
def l1644(g, d):
    S.sky(g, [(0, (150, 180, 210)), (220, (240, 210, 170)), (330, (250, 220, 170))])
    for x, y, w in ((150, 70, 90), (640, 50, 120)):
        S.obj(g, Union([Ell(x, y, w, 18), Ell(x - w * 0.4, y - 10, w * 0.4, 16), Ell(x + w * 0.3, y - 14, w * 0.45, 18)]), (255, 246, 232), x, line=False)
    S.ground(g, Under(lambda x: 330 - 90 * np.exp(-((x - 640) / 260.0) ** 2), -20, W + 20), (150, 170, 110), "grass", 1)
    # windmill clock tower on the hilltop
    S.obj(g, Poly([(600, 250), (620, 110), (680, 110), (700, 250)]), (230, 210, 180), 2, "brick")
    S.obj(g, Poly([(608, 116), (650, 60), (692, 116)]), (170, 80, 60), 3, "roof")
    clock_face(g, 650, 160, 24, hand_b=4.2, col=(246, 236, 210) if "clock" not in d else (180, 210, 230), seed=4)
    g.fill(Seg(650, 60, 650, 36, 1.6), INK)
    vk = 1 if "vane" not in d else -1
    S.obj(g, Union([Poly([(650, 32), (650 + vk * 40, 41), (650, 50)]), Poly([(650, 36), (650 - vk * 22, 30), (650 - vk * 16, 41), (650 - vk * 22, 52), (650, 46)])]), (70, 60, 60), 5)
    # crooked houses climbing the hill
    houses = ((-10, 470, 110, 230, (236, 214, 180), (110, 120, 150), 0.03), (110, 450, 90, 260, (220, 180, 150), (160, 70, 60), -0.03),
              (210, 420, 100, 210, (240, 226, 196), (90, 120, 100), 0.04), (320, 400, 90, 190, (214, 200, 220), (150, 80, 70), -0.02),
              (720, 410, 100, 200, (236, 210, 170), (110, 110, 150), 0.03), (830, 440, 100, 250, (220, 196, 170), (160, 80, 60), -0.04))
    for i, (x0, base, w, h, wall, roof, lean) in enumerate(houses):
        crooked_house(g, x0, base, w, h, wall, roof, 10 + i * 40, lean=lean, lit={(1, 0)} if i % 2 else set(),
                      box_col=(120, 80, 60) if i == 2 and "flowers" not in d else None, chimney=not (i == 4 and "chimney" in d))
    # cobbled street winding up
    street = Poly([(380, 610), (620, 610), (560, 470), (600, 330), (560, 330), (480, 470)])
    S.ground(g, street, (200, 180, 150), "dirt", 6, line=True)
    for k in range(40):
        rnd = random.Random(k)
        t = k / 40
        x = 500 + 60 * math.sin(t * 3) + rnd.uniform(-30, 30)
        y = 600 - t * 270
        g.fill(Ell(x, y, 6 - t * 3, 3 - t * 1.5), (170, 150, 120), alpha=0.6)
    # laundry line between two houses, a cat on a roof, a balloon
    S.line(g, 300, 270, 410, 290, 1, (90, 70, 60))
    for i, (x, c) in enumerate(((320, (240, 120, 120)), (350, (120, 160, 220)), (380, (250, 220, 120)))):
        if "laundry" in d and i == 1:
            continue
        S.obj(g, Box(x - 9, 274 + (x - 300) * 0.18, x + 9, 300 + (x - 300) * 0.18), c, 60 + i)
    if "cat" not in d:
        S.obj(g, Union([Ell(250, 190, 16, 9), Circ(264, 180, 7), Poly([(260, 176), (262, 166), (266, 175)]), Poly([(266, 175), (270, 166), (272, 178)])]), (70, 60, 70), 70)
    S.obj(g, Union([Ell(820, 120, 24, 28), Poly([(808, 140), (832, 140), (824, 152), (816, 152)])]), (220, 90, 80) if "balloon" not in d else (90, 150, 210), 71, hi=True)
    S.line(g, 820, 152, 818, 190, 0.8, (90, 70, 60))
    lamp(g, 440, 560, 80)
    professor(g, 620, 590, 170, face=-1, seed=80)
    apprentice(g, 680, 594, 100, face=-1, seed=81)


L1644_EL = [E("sails", el(lambda g, m: [S.obj(g, Poly([(650, 110), (650 + math.cos(a) * 90 - math.sin(a) * 12, 110 + math.sin(a) * 90 + math.cos(a) * 12),
                                                   (650 + math.cos(a) * 90 + math.sin(a) * 12, 110 + math.sin(a) * 90 - math.cos(a) * 12)]), (246, 236, 214), 90)
                                for a in (0.3, 0.3 + math.pi / 2, 0.3 + math.pi, 0.3 + 1.5 * math.pi)]), pivot=(650, 110), anim=dict(rotateSpeed=-20)),
            E("birds", el(lambda g, m: [g.fill(Union([Seg(x - 7, y - 3, x, y, 1.4), Seg(x, y, x + 7, y - 3, 1.4)]), INK) for x, y in ((420, 90), (440, 80))]),
              anim=dict(bobAmplitude=(40, 6), bobSpeed=0.05))]
L1644_DIFFS = [("clock", 650, 160, 0), ("vane", 655, 42, 0), ("flowers", 240, 330, 0), ("chimney", 800, 180, 0), ("laundry", 350, 294, 0),
               ("cat", 260, 184, 0), ("balloon", 820, 128, 0)]


# =================================================================== Level 1645 the scholar's study
def l1645(g, d):
    S.obj(g, Box(-2, -2, W + 2, 440), (176, 140, 110), 1, line=False)
    S.obj(g, Box(-2, 300, W + 2, 440), (130, 90, 64), 2, "wood")
    # bookshelves (left, right)
    rnd = random.Random(1645)
    for x0, x1 in ((20, 260), (650, 880)):
        S.obj(g, Box(x0, 40, x1, 440), (120, 80, 56), 3 + x0, "wood")
        for y in (60, 150, 240, 330):
            x = x0 + 12
            while x < x1 - 20:
                w = rnd.uniform(12, 22)
                hh = rnd.uniform(50, 76)
                S.obj(g, Box(x, y + 80 - hh, x + w, y + 80), [(160, 60, 50), (60, 90, 130), (90, 130, 80), (200, 160, 80), (130, 80, 120)][rnd.randrange(5)], 5)
                x += w + 1.5
            S.obj(g, Box(x0, y + 80, x1, y + 88), (140, 96, 66), 6, "wood")
    # window with a view of rooftops
    S.obj(g, Box(330, 60, 570, 260, 4), (130, 90, 60), 7, "wood")
    g.fill(Box(342, 72, 558, 248), vgrad([(72, (200, 220, 230)), (248, (250, 220, 180))]))
    for x0, w, h in ((350, 50, 90), (410, 40, 120), (460, 60, 80), (520, 40, 100)):
        S.obj(g, Union([Box(x0, 248 - h, x0 + w, 248), Poly([(x0 - 4, 250 - h), (x0 + w / 2, 230 - h - w * 0.4), (x0 + w + 4, 250 - h)])]), (180, 170, 190), 8 + x0, depth=0.4)
    g.fill(Union([Box(447, 72, 453, 248), Box(342, 157, 558, 163)]), (130, 90, 60))
    # desk with puzzle box, teapot, magnifier, papers; globe; armchair; telescope
    S.obj(g, Box(260, 380, 640, 404, 3), (140, 92, 62), 10, "wood")
    for lx in (280, 610):
        S.obj(g, Box(lx, 404, lx + 18, 520), (120, 80, 54), 11, "wood")
    S.obj(g, Box(300, 340, 360, 380, 3), (180, 120, 70) if "puzzle" not in d else (90, 130, 170), 12)
    g.fill(Union([Box(300, 358, 360, 361), Box(329, 340, 332, 380)]), (110, 70, 40))
    g.fill(Circ(330, 359, 6), (230, 190, 80))
    S.obj(g, Union([Ell(440, 362, 26, 20), Seg(462, 356, 480, 344, 4), Box(430, 336, 450, 344, 3)]), (90, 130, 160) if "teapot" not in d else (190, 90, 90), 13, hi=True)
    S.obj(g, Union([Box(492, 360, 510, 380, 3), Ell(501, 360, 9, 3)]), (246, 240, 226), 14)
    S.obj(g, Poly([(540, 380), (600, 372), (606, 380), (546, 386)]), (246, 238, 216), 15)
    S.obj(g, Union([Circ(580, 352, 14) - Circ(580, 352, 10), Seg(590, 362, 606, 380, 3)]), (180, 150, 80), 16)
    S.ground(g, Box(-2, 440, W + 2, H + 2), (150, 100, 70), "wood", 17, line=True)
    S.obj(g, Ell(460, 540, 280, 46), (150, 60, 60), 18)
    S.obj(g, Ell(460, 540, 240, 34) - Ell(460, 540, 228, 28), (220, 180, 100), 19)
    gx, gy = 150, 480
    S.obj(g, Union([Seg(gx, gy + 40, gx, gy + 110, 3), Box(gx - 30, gy + 108, gx + 30, gy + 116, 2)]), (130, 90, 60), 20)
    S.obj(g, Circ(gx, gy, 40), (110, 160, 190), 21, hi=True)
    S.obj(g, Union([Rough(Ell(gx - 8, gy - 6, 18, 14), 4, 6, 1), Rough(Ell(gx + 16, gy + 16, 10, 12), 3, 5, 2)]), (160, 170, 100), 22, line=False)
    S.obj(g, Circ(gx, gy, 46) - Circ(gx, gy, 42), (190, 150, 80) if "globe" not in d else (120, 120, 130), 23)
    S.obj(g, Union([Box(720, 440, 860, 560, 14), Box(706, 470, 740, 560, 8), Box(840, 470, 874, 560, 8)]), (90, 120, 90), 24)
    if "cushion" not in d:
        S.obj(g, Ell(790, 470, 40, 16), (220, 180, 90), 25)
    S.obj(g, Union([Seg(560, 300, 640, 250, 7, 5), Seg(600, 296, 590, 380, 2), Seg(600, 296, 620, 380, 2)]), (180, 150, 80) if "scope" not in d else (100, 100, 110), 26)
    # clock on the wall and a portrait
    clock_face(g, 600, 100, 30, hand_b=4.2, rim=(170, 130, 70) if "hand" not in d else (90, 110, 150), seed=27)
    professor(g, 520, 600, 200, face=-1, seed=28)


L1645_EL = [E("steam", el(lambda g, m: [g.glow(436 + k * 6, 330 - k * 14, 8, (255, 250, 240), 0.5) for k in range(3)]), daynight="untinted",
              anim=dict(driftVelocity=(3, 30), driftLength=40, driftFade=True)),
            sparkle_el("dust", [(400, 160), (480, 210), (520, 140)], col=(255, 246, 220), r=3, speed=0.5)]
L1645_DIFFS = [("puzzle", 330, 359, 0), ("teapot", 446, 358, 0), ("globe", 150, 480, 0), ("cushion", 790, 470, 0), ("scope", 600, 290, 0),
               ("hand", 600, 100, 0)]


# =================================================================== Level 1646 steam-train dining car
def l1646(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (140, 60, 50), 1, line=False)
    S.obj(g, Box(-2, 360, W + 2, 440), (110, 70, 50), 2, "wood")
    # windows with the countryside
    for i, x0 in enumerate((40, 330, 620)):
        S.obj(g, Box(x0, 70, x0 + 240, 300, 18), (190, 150, 90), 3 + i)
        g.fill(Box(x0 + 12, 82, x0 + 228, 288, 12), vgrad([(82, (170, 200, 220)), (288, (240, 230, 190))]))
        g.fill(Box(x0 + 12, 220, x0 + 228, 288, 12), (150, 180, 110))
    # tables with lamps, teacups, a cake
    for i, x0 in enumerate((60, 350, 640)):
        S.obj(g, Box(x0, 380, x0 + 200, 400, 3), (246, 240, 226), 10 + i)
        S.obj(g, Box(x0 + 90, 400, x0 + 110, 520), (110, 70, 50), 13 + i, "wood")
        lx = x0 + 100
        lit = not ("lamp" in d and i == 2)
        if lit:
            g.glow(lx, 330, 60, (255, 210, 130), 0.35)
        S.obj(g, Union([Box(lx - 3, 340, lx + 3, 380), Poly([(lx - 18, 342), (lx + 18, 342), (lx + 10, 318), (lx - 10, 318)])]), (240, 200, 140) if lit else (150, 140, 130), 16 + i)
    for x, key in ((110, None), (420, "cup"), (700, None)):
        c = (246, 240, 226) if not (key and key in d) else (120, 170, 210)
        S.obj(g, Union([Box(x - 10, 362, x + 10, 380, 3), Ell(x, 380, 16, 4)]), c, 20, hi=True)
    if "cake" not in d:
        S.obj(g, Union([Box(470, 350, 520, 380, 2)]), (246, 220, 200), 21)
        S.obj(g, Box(470, 350, 520, 358, 2), (230, 120, 140), 22)
        g.fill(Circ(495, 346, 5), (210, 40, 50))
    S.ground(g, Box(-2, 440, W + 2, H + 2), (120, 50, 50), "plain", 23, line=True)
    for x in range(-20, 900, 60):
        g.fill(Poly([(x, 440), (x + 30, 440), (x + 60, 600), (x + 30, 600)]), (140, 60, 56), alpha=0.6)
    # luggage rack with a hat box
    S.obj(g, Box(-2, 40, W + 2, 50), (200, 170, 100), 24)
    S.obj(g, Union([Box(150, 10, 210, 40, 6)]), (90, 130, 110) if "hatbox" not in d else (190, 100, 120), 25)
    S.obj(g, Box(700, 16, 790, 40, 4), (150, 100, 60), 26, "wood")
    # waiter and passengers
    apprentice(g, 260, 580, 160, face=1, coat=(240, 236, 226), cap=(40, 40, 50), seed=27)
    S.obj(g, Union([Ell(300, 470, 30, 6), Seg(286, 474, 296, 500, 3)]), (200, 200, 210), 28)
    professor(g, 560, 600, 210, face=-1, seed=29, scarf=(170, 50, 50) if "scarf" not in d else (60, 110, 170))
    apprentice(g, 820, 590, 150, face=-1, seed=30)


L1646_EL = [E("scenery", el(lambda g, m: [S.obj(g, Union([Circ(x, 240, 18), Box(x - 3, 240, x + 3, 270)]), (90, 140, 80), 1, depth=0.3) for x in (100, 420, 720)]),
              bbox=(60, 210, 760, 280), anim=dict(driftVelocity=(-120, 0), driftLength=300, driftFade=True)),
            E("steam", el(lambda g, m: [g.glow(x, 120, 30, (255, 255, 250), 0.5) for x in (200, 500)]), anim=dict(driftVelocity=(-80, 6), driftLength=200, driftFade=True))]
L1646_DIFFS = [("lamp", 740, 330, 0), ("cup", 420, 372, 0), ("cake", 495, 360, 0), ("hatbox", 180, 25, 0), ("scarf", 560, 380, 0)]


# =================================================================== Level 1647 fairground at dusk
def l1647(g, d):
    S.sky(g, [(0, (70, 80, 140)), (200, (200, 140, 150)), (330, (250, 200, 150))])
    # Ferris wheel (rim static, cabins rotate)
    S.obj(g, Circ(700, 200, 150) - Circ(700, 200, 142), (240, 230, 220), 1)
    for a in range(12):
        aa = a * math.tau / 12
        g.fill(Seg(700, 200, 700 + math.cos(aa) * 146, 200 + math.sin(aa) * 146, 1.2), INK)
    S.obj(g, Union([Seg(640, 400, 700, 200, 5), Seg(760, 400, 700, 200, 5)]), (200, 190, 180), 2)
    S.ground(g, Box(-2, 380, W + 2, H + 2), (180, 160, 130), "dirt", 3, line=True)
    # striped tents
    for x, col, key in ((120, (200, 60, 60), None), (380, (60, 110, 170), "tent")):
        c = col if not (key and key in d) else (90, 150, 90)
        S.obj(g, Poly([(x - 90, 400), (x - 70, 300), (x, 250), (x + 70, 300), (x + 90, 400)]), (246, 236, 214), x)
        for k in range(4):
            g.fill(Inter(Poly([(x - 90 + k * 45, 400), (x - 70 + k * 35, 300), (x - 50 + k * 35, 300), (x - 68 + k * 45, 400)]),
                         Poly([(x - 90, 400), (x - 70, 300), (x, 250), (x + 70, 300), (x + 90, 400)])), c)
        S.line(g, x, 250, x, 220, 1.6, INK)
        S.obj(g, Poly([(x + 1, 220), (x + 24, 228), (x + 1, 236)]), (250, 210, 90), x + 1)
    # carousel (centre)
    S.obj(g, Union([Poly([(330, 420), (450, 360), (570, 420)])]), (230, 90, 90), 10, "roof")
    S.obj(g, Box(340, 420, 560, 432), (246, 230, 190), 11)
    S.obj(g, Box(340, 500, 560, 516, 4), (200, 160, 100), 12)
    for x in (360, 420, 480, 540):
        g.fill(Seg(x, 432, x, 500, 2), (230, 190, 90))
    for i, x in enumerate((390, 450, 510)):
        c = (246, 240, 226) if not ("horse" in d and i == 1) else (120, 90, 70)
        S.obj(g, Union([Ell(x, 474, 20, 10), Circ(x + 18, 462, 7), Seg(x - 12, 480, x - 14, 494, 2), Seg(x + 12, 480, x + 14, 494, 2)]), c, 13 + i)
    # string lights
    pts = [(0, 300), (200, 330), (450, 300), (700, 330), (900, 300)]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        g.fill(Seg(x0, y0, x1, y1, 0.8), INK)
        for k in range(7):
            t = (k + 0.5) / 7
            g.fill(Circ(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + 3, 3), (255, 230, 150))
    # balloon seller with a bunch of balloons
    apprentice(g, 200, 580, 150, face=1, coat=(170, 90, 60), cap=(80, 60, 50), seed=20)
    for i, (bx, by, c) in enumerate(((180, 400, (230, 80, 90)), (210, 390, (90, 150, 210)), (240, 405, (250, 210, 90)), (206, 420, (120, 180, 110)))):
        if "balloon" in d and i == 2:
            continue
        S.line(g, 214, 480, bx, by + 18, 0.6, INK)
        S.obj(g, Ell(bx, by, 14, 17), c, 21 + i, hi=True)
    # candy stall, professor and apprentice
    S.obj(g, Box(620, 470, 760, 540, 3), (246, 220, 200), 30)
    S.obj(g, Poly([(610, 470), (770, 470), (750, 440), (630, 440)]), (230, 120, 150) if "awning" not in d else (130, 190, 220), 31)
    for k in range(4):
        S.obj(g, Circ(645 + k * 30, 492, 10), (250, 200, 220), 32 + k)
    professor(g, 520, 600, 180, face=1, seed=40)
    apprentice(g, 860, 600, 120, face=-1, seed=41)


def l1647_cabins(g, m):
    for a in range(8):
        aa = a * math.tau / 8
        x, y = 700 + math.cos(aa) * 146, 200 + math.sin(aa) * 146
        S.obj(g, Box(x - 12, y - 8, x + 12, y + 12, 3), [(230, 90, 90), (90, 150, 210), (250, 210, 90), (120, 180, 110)][a % 4], 50 + a)


L1647_EL = [E("wheel", el(l1647_cabins), pivot=(700, 200), anim=dict(rotateSpeed=-8)),
            E("carousel", el(lambda g, m: [g.glow(x, 426, 8, (255, 230, 150), 0.6) for x in (350, 400, 450, 500, 550)]), daynight="untinted",
              anim=dict(twinkle=0.6, twinkleSpeed=1.2)),
            sparkle_el("lights", [(100, 318), (300, 318), (560, 318), (800, 318)], col=(255, 240, 180), r=5, speed=0.6)]
L1647_DIFFS = [("tent", 380, 330, 0), ("horse", 456, 470, 0), ("balloon", 240, 405, 0), ("awning", 690, 455, 0)]


# =================================================================== Level 1648 clockmaker's shop
def l1648(g, d):
    S.obj(g, Box(-2, -2, W + 2, 440), (150, 120, 90), 1, line=False)
    S.obj(g, Box(-2, 320, W + 2, 440), (120, 80, 56), 2, "wood")
    # wall of clocks
    clocks = ((90, 90, 34, 0.5, 2.0), (200, 70, 26, 2.0, 5.0), (300, 110, 30, 3.5, 1.0), (620, 80, 30, 1.0, 3.2), (720, 120, 36, 4.0, 0.4),
              (830, 80, 26, 0.2, 4.6), (150, 200, 24, 5.0, 2.5), (780, 220, 28, 2.6, 5.4))
    for i, (x, y, r, a, b) in enumerate(clocks):
        rimc = [(170, 130, 70), (120, 80, 50), (180, 160, 120), (150, 100, 60)][i % 4]
        if "clock" in d and i == 4:
            rimc = (90, 130, 110)
        clock_face(g, x, y, r, a, b, rim=rimc, seed=10 + i * 3)
    # cuckoo clock (centre) - the bird pops out as an element
    S.obj(g, Union([Box(400, 80, 500, 230, 4), Poly([(388, 84), (450, 30), (512, 84)])]), (130, 86, 56), 40, "wood")
    clock_face(g, 450, 140, 30, 1.2, 4.0, seed=41)
    S.obj(g, Union([Box(440, 84, 460, 104, 3)]), (60, 40, 30), 42)
    for x, key in ((430, None), (470, "weight")):
        g.fill(Seg(x, 230, x, 300, 1), INK)
        S.obj(g, Box(x - 9, 296, x + 9, 344, 4), (180, 150, 70) if not (key and key in d) else (120, 120, 130), 43)
    # workbench with gears, loupe, tools
    S.obj(g, Box(80, 400, 820, 424, 3), (150, 100, 66), 50, "wood")
    for lx in (100, 790):
        S.obj(g, Box(lx, 424, lx + 18, 560), (120, 80, 54), 51, "wood")
    for i, (x, r, c) in enumerate(((180, 26, (200, 160, 80)), (240, 16, (170, 170, 180)), (290, 20, (200, 160, 80)))):
        if "gear" in d and i == 1:
            c = (190, 100, 80)
        teeth = Union([Circ(x, 380, r)] + [Box(x + math.cos(t) * (r + 2) - 3, 380 + math.sin(t) * (r + 2) - 3, x + math.cos(t) * (r + 2) + 3,
                                                 380 + math.sin(t) * (r + 2) + 3) for t in np.linspace(0, math.tau, 12, endpoint=False)])
        S.obj(g, Diff(teeth, Circ(x, 380, r * 0.35)), c, 52 + i, hi=True)
    if "loupe" not in d:
        S.obj(g, Union([Circ(560, 384, 14) - Circ(560, 384, 9), Seg(570, 394, 590, 398, 3)]), (60, 56, 60), 60)
    S.obj(g, Union([Seg(640, 396, 700, 386, 2.4), Seg(640, 392, 700, 392, 2.4)]), (170, 170, 180), 61)
    S.ground(g, Box(-2, 440, W + 2, H + 2), (140, 96, 66), "wood", 62, line=True)
    # grandfather clock (right) and a cat
    S.obj(g, Union([Box(840, 240, 900, 560, 4), Poly([(834, 244), (870, 210), (906, 244)])]), (110, 70, 46), 63, "wood")
    clock_face(g, 870, 280, 22, 0.7, 3.4, seed=64)
    S.obj(g, Box(850, 330, 890, 520, 3), (90, 56, 36), 65)
    if "cat" not in d:
        S.obj(g, Union([Ell(330, 580, 26, 14), Circ(354, 566, 11), Poly([(348, 558), (350, 546), (356, 556)]), Poly([(358, 556), (364, 546), (364, 560)])]), (230, 150, 80), 66)
    professor(g, 500, 600, 190, face=1, seed=70, coat=(90, 70, 60))
    apprentice(g, 650, 600, 130, face=-1, seed=71)


L1648_EL = [E("cuckoo", el(lambda g, m: S.obj(g, Union([Ell(450, 92, 9, 6), Poly([(442, 90), (434, 92), (442, 94)])]), (240, 200, 80), 80)),
              pivot=(450, 104), anim=dict(bobAmplitude=(0, 6), bobSpeed=0.5)),
            E("pendulum", el(lambda g, m: (g.fill(Seg(870, 330, 870, 480, 1.4), (200, 170, 80)), S.obj(g, Circ(870, 490, 12), (220, 190, 90), 81, hi=True))),
              pivot=(870, 330), anim=dict(swingAngle=10, swingSpeed=0.5)),
            sparkle_el("glints", [(180, 372), (560, 380), (720, 120)], col=(255, 250, 220), r=4, speed=0.6)]
L1648_DIFFS = [("clock", 720, 120, 0), ("weight", 470, 318, 0), ("gear", 240, 380, 0), ("loupe", 566, 386, 0), ("cat", 340, 572, 0)]


LEVELS = [
    ("Level1644", "坡上小镇", make(l1644), L1644_EL, L1644_DIFFS, 60, OPTS),
    ("Level1645", "教授书房", make(l1645), L1645_EL, L1645_DIFFS, 60, OPTS),
    ("Level1646", "蒸汽餐车", make(l1646), L1646_EL, L1646_DIFFS, 60, OPTS),
    ("Level1647", "黄昏游园会", make(l1647), L1647_EL, L1647_DIFFS, 60, OPTS),
    ("Level1648", "钟表匠工坊", make(l1648), L1648_EL, L1648_DIFFS, 60, OPTS),
]
