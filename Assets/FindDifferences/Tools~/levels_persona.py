# -*- coding: utf-8 -*-
"""Stylish high-contrast school-life RPG levels: bold black inks, a limited per-level palette (red / blue / yellow on black
and white), halftone dots, diagonal slashes, stars and silhouette crowds - imitating the graphic language of modern
Japanese school-life RPGs. Characters, places and props are original (no game UI, logos, text or iconic characters).
  Level1615 放学天台   - red: a school rooftop at sunset, giant sun, chain-link fence, students, crows
  Level1616 午夜路口   - red / black: a midnight scramble crossing, silhouette crowd, big screen, neon stars
  Level1617 蓝色车厢   - blue: a velvet-blue train-car lounge between worlds, an attendant with a book
  Level1618 雨夜商店街 - yellow: a rainy shopping arcade at night, a TV glowing in a shop window
  Level1619 黄金殿堂   - red / gold: a golden palace vault, the treasure on its pedestal, a masked thief
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, el, fbm1, mixc, real_post, smooth, vgrad
from levels_remake import ComicS, _size
from levels_isostyle import halftone
from toon import Grow
from styled_kit import person, sparkle_el

BLACK = (14, 12, 16)
WHITE = (250, 248, 244)


class PersonaS(ComicS):
    """Comic inks pushed further: thick black lines, solid black shadow crescents with dot screens, punchy grade."""
    name = "persona"
    ink = BLACK

    def __init__(self, accent):
        self.accent = accent

    def obj(self, g, shape, col, seed=0, kind="plain", depth=0.0, line=True, hi=False):
        w, h = _size(shape)
        o = -min(12, max(2, min(w, h) * 0.18))
        if line:
            g.fill(Grow(shape, 3.2 * (1 - depth * 0.5)), BLACK)
        g.fill(shape, col)
        cres = Diff(shape, Moved(shape, o, o))
        g.fill(cres, tuple(c * 0.55 for c in col))
        g.fill(cres, BLACK, alpha=halftone(0.45, 4.0))
        if hi and depth < 0.5:
            b = shape.bbox()
            g.fill(Ell(b[0] + w * 0.28, b[1] + h * 0.25, w * 0.1, h * 0.07), WHITE)

    def glow(self, g, x, y, r, col, k=0.4):
        g.fill(Circ(x, y, r * 0.5), col, alpha=0.45)
        g.fill(Circ(x, y, r * 0.5), BLACK, alpha=halftone(0.25, 5.0))

    def finish(self, g):
        g.grade(contrast=1.18, sat=1.3)


OPTS = dict(post=lambda rows, w, h, ox, oy, a: real_post(rows, w, h, ox, oy, a, grain=1.2, vignette=0.1), anim_seconds=12.0, frames=60)


def make(S, scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, S, d)
        S.finish(g)
        g.commit()
    return bg


class Ring:
    """Outline band of width w around a shape boundary."""

    def __init__(self, s, w):
        self.s, self.w = s, w

    def bbox(self):
        b = self.s.bbox()
        return (b[0] - self.w, b[1] - self.w, b[2] + self.w, b[3] + self.w)

    def sdf(self, X, Y):
        return np.abs(self.s.sdf(X, Y)) - self.w


def slashes(g, col, n=7, seed=0, alpha=1.0, w=(30, 90), angle=0.45):
    """Diagonal graphic slashes across the background."""
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(-200, 900)
        ww = rnd.uniform(*w)
        g.fill(Poly([(x, -10), (x + ww, -10), (x + ww + 700 * angle, 620), (x + 700 * angle, 620)]), col, alpha=alpha)


def star(cx, cy, r, n=5, inner=0.45, rot=-90):
    return Poly([(cx + math.cos(math.radians(rot + i * 180 / n)) * (r if i % 2 == 0 else r * inner),
                  cy + math.sin(math.radians(rot + i * 180 / n)) * (r if i % 2 == 0 else r * inner)) for i in range(2 * n)])


def silhouette(g, x, base, h, col, face=1, skirt=False, bag=False, seed=0):
    """Flat crowd silhouette (single colour, no ink)."""
    k = h / 200.0
    parts = [Ell(x, base - 184 * k, 15 * k, 17 * k), Box(x - 18 * k, base - 160 * k, x + 18 * k, base - 96 * k, 8 * k),
             Seg(x - 18 * k, base - 152 * k, x - 22 * k, base - 104 * k, 6 * k), Seg(x + 18 * k, base - 152 * k, x + 22 * k, base - 104 * k, 6 * k)]
    if skirt:
        parts += [Poly([(x - 24 * k, base - 70 * k), (x + 24 * k, base - 70 * k), (x + 16 * k, base - 104 * k), (x - 16 * k, base - 104 * k)]),
                  Box(x - 12 * k, base - 72 * k, x - 4 * k, base), Box(x + 4 * k, base - 72 * k, x + 12 * k, base)]
    else:
        parts += [Box(x - 15 * k, base - 100 * k, x - 3 * k, base), Box(x + 3 * k, base - 100 * k, x + 15 * k, base)]
    if bag:
        parts.append(Box(x + face * 18 * k, base - 120 * k, x + face * 40 * k, base - 92 * k, 3 * k))
    g.fill(Union(parts), col)


def student(g, S, x, base, h, blazer, face=1, skirt=False, hair=(30, 26, 30), seed=0, bag=None, tie=(200, 30, 40)):
    person(S, g, x, base, h, blazer, pants=(40, 40, 50) if not skirt else (60, 50, 70), skirt=skirt, hair=hair, hair_long=skirt, face=face, seed=seed, bag=bag)
    k = h / 200.0
    g.fill(Poly([(x - 4 * k, base - 158 * k), (x + 4 * k, base - 158 * k), (x + 3 * k, base - 120 * k), (x, base - 114 * k), (x - 3 * k, base - 120 * k)]), tie)
    g.fill(Poly([(x - 10 * k, base - 160 * k), (x, base - 140 * k), (x + 10 * k, base - 160 * k)]), WHITE)


# =================================================================== Level 1615 rooftop at sunset (red)
SR = PersonaS((220, 30, 40))


def l1615(g, S, d):
    S.sky(g, [(0, (160, 10, 30)), (360, (250, 90, 60))])
    slashes(g, (120, 0, 20), n=6, seed=1, alpha=0.6)
    S.obj(g, Circ(620, 230, 130), (255, 220, 80), 1, line=True)
    for i in range(4):
        y = 250 + i * 26
        g.fill(Inter(Box(480, y, 760, y + 10 + i * 3), Circ(620, 230, 130)), (220, 60, 50) if not ("sun" in d and i == 1) else (250, 250, 240))
    # city skyline in black
    rnd = random.Random(1615)
    x = -10
    while x < 910:
        w = rnd.uniform(30, 70)
        hh = rnd.uniform(40, 150)
        g.fill(Box(x, 360 - hh, x + w, 380), BLACK)
        for wy in np.arange(360 - hh + 8, 370, 14):
            for wx in np.arange(x + 6, x + w - 6, 12):
                if rnd.random() < 0.25:
                    g.fill(Box(wx, wy, wx + 5, wy + 6), (250, 200, 80))
        x += w + 2
    if "tower" not in d:
        g.fill(Union([Poly([(150, 380), (175, 140), (200, 380)]), Seg(175, 140, 175, 100, 2)]), BLACK)
    # rooftop floor and fence
    S.ground(g, Box(-2, 380, W + 2, H + 2), (180, 170, 170), "stone", 2, line=True)
    g.fill(Box(-2, 380, W + 2, 470), BLACK, alpha=lambda X, Y: 0.6 * (((np.abs(np.sin((X + Y) * 0.25)) > 0.93) | (np.abs(np.sin((X - Y) * 0.25)) > 0.93))))
    g.fill(Union([Box(-2, 376, W + 2, 384), Box(-2, 466, W + 2, 474)] + [Box(x, 376, x + 6, 474) for x in range(20, 900, 120)]), BLACK)
    # water tank (left)
    S.obj(g, Union([Box(40, 250, 200, 380, 10), Ell(120, 250, 80, 14)]), (230, 230, 230), 3, hi=True)
    g.fill(Box(40, 300, 200, 316), (220, 30, 40) if "tank" not in d else (40, 60, 160))
    for x in (60, 180):
        g.fill(Box(x - 4, 380, x + 4, 420), BLACK)
    # stair door hut (right)
    S.obj(g, Box(760, 300, 900, 460), (200, 190, 190), 4)
    S.obj(g, Box(790, 340, 850, 460), (120, 110, 120), 5)
    if "lamp" not in d:
        S.glow(g, 820, 320, 40, (255, 220, 120), 0.5)
        S.obj(g, Box(810, 312, 830, 326, 2), (255, 230, 140), 6)
    # students (original)
    student(g, S, 300, 590, 230, (40, 40, 60), face=1, seed=7, bag=(90, 60, 40) if "bag" not in d else (220, 30, 40))
    student(g, S, 430, 590, 220, (40, 40, 60), face=-1, skirt=True, hair=(120, 60, 40), seed=8)
    student(g, S, 560, 596, 230, (40, 40, 60), face=-1, seed=9, hair=(60, 40, 40), tie=(200, 30, 40) if "tie" not in d else (250, 210, 60))
    # crows on the fence
    for x, key in ((640, None), (700, "crow")):
        if key and key in d:
            continue
        g.fill(Union([Ell(x, 356, 18, 14), Circ(x + 15, 340, 9), Poly([(x + 21, 337), (x + 36, 342), (x + 21, 346)]), Poly([(x - 15, 356), (x - 40, 368), (x - 12, 366)])]), BLACK)
    g.fill(star(870, 60, 26), WHITE)
    g.fill(Ring(star(870, 60, 26), 2), BLACK)


L1615_EL = [E("crowsfly", el(lambda g, m: [g.fill(Union([Seg(x - 9, y - 4, x, y, 2.4), Seg(x, y, x + 9, y - 4, 2.4)]), BLACK) for x, y in ((300, 120), (330, 104), (360, 126))]),
              anim=dict(bobAmplitude=(60, 10), bobSpeed=0.05)),
            sparkle_el("glint", [(860, 60)], col=WHITE, r=10, speed=0.6)]
L1615_DIFFS = [("sun", 620, 288, 0), ("tower", 175, 260, 0), ("tank", 120, 308, 0), ("lamp", 820, 319, 0), ("bag", 260, 480, 0),
               ("crow", 704, 360, 0), ("tie", 560, 450, 0)]


# =================================================================== Level 1616 midnight scramble crossing (red / black)
def l1616(g, S, d):
    g.fill(Box(-2, -2, W + 2, H + 2), BLACK)
    slashes(g, (150, 10, 30), n=8, seed=2, alpha=0.9, angle=-0.4)
    # black buildings with white window grids
    for x0, x1, top in ((-20, 220, 40), (240, 420, 120), (680, 920, 20)):
        g.fill(Box(x0, top, x1, 420), (24, 20, 26))
        g.fill(Ring(Box(x0, top, x1, 420), 2), WHITE)
        for wy in range(top + 20, 400, 30):
            for wx in range(x0 + 16, x1 - 20, 26):
                g.fill(Box(wx, wy, wx + 14, wy + 16), WHITE if (wx + wy) % 3 else (230, 30, 40))
    # giant screen with an abstract graphic
    S.obj(g, Box(440, 70, 660, 220, 4), (30, 30, 34), 1)
    g.fill(Box(450, 80, 650, 210), (230, 30, 40) if "screen" not in d else (40, 70, 200))
    g.fill(star(550, 145, 54), WHITE)
    g.fill(star(550, 145, 26), BLACK)
    # neon stars and a traffic light
    for x, y, r, key in ((120, 80, 20, None), (790, 100, 28, "star")):
        if key and key in d:
            continue
        g.fill(Ring(star(x, y, r), 3), (255, 240, 120))
    g.fill(Box(470, 240, 480, 430), WHITE)
    S.obj(g, Box(440, 236, 510, 266, 3), (30, 30, 34), 2)
    S.obj(g, Box(430, 230, 520, 272, 4), (30, 30, 34), 22)
    g.fill(Circ(455, 251, 14), (230, 30, 40) if "signal" not in d else (40, 220, 120))
    g.fill(Circ(495, 251, 14), (80, 80, 80))
    # the crossing: diagonal zebra stripes
    g.fill(Box(-2, 420, W + 2, H + 2), (40, 36, 40))
    for k in range(-6, 14):
        x = k * 80
        g.fill(Poly([(x, 420), (x + 40, 420), (x - 80, 600), (x - 120, 600)]), WHITE)
    # crowd silhouettes in red, one hero student in colour
    rnd = random.Random(1616)
    for i in range(14):
        x = 40 + i * 64 + rnd.uniform(-10, 10)
        hh = rnd.uniform(150, 220)
        col = (200, 20, 40) if not ("crowd" in d and i == 10) else (250, 248, 244)
        silhouette(g, x, 600 - rnd.uniform(0, 20), hh, col, skirt=i % 3 == 0, bag=i % 4 == 1, seed=i)
    student(g, S, 360, 600, 250, (30, 30, 40), face=1, seed=3, hair=(20, 20, 24))
    if "umbrella" not in d:
        g.fill(Seg(392, 380, 392, 470, 2), BLACK)
        S.obj(g, Inter(Ell(392, 384, 70, 34), Box(320, 340, 470, 384)), WHITE, 4)
    # a black cat on the guard rail
    g.fill(Box(700, 440, 900, 448), WHITE)
    if "cat" not in d:
        g.fill(Union([Ell(780, 430, 22, 12), Circ(804, 418, 10), Poly([(796, 412), (798, 400), (804, 410)]), Poly([(806, 410), (812, 400), (814, 412)]), Seg(758, 426, 744, 404, 3)]), BLACK)
        g.fill(Circ(808, 418, 2.4), (255, 220, 60))


L1616_EL = [E("flash", el(lambda g, m: g.fill(Box(450, 80, 650, 210), WHITE, alpha=0.5)), daynight="untinted", anim=dict(blinkInterval=3.0, blinkDuration=0.2)),
            sparkle_el("stars", [(120, 80), (300, 40), (840, 260)], col=(255, 240, 120), r=8, speed=0.7)]
L1616_DIFFS = [("screen", 550, 100, 0), ("star", 790, 100, 0), ("signal", 458, 251, 0), ("crowd", 690, 480, 0), ("umbrella", 392, 370, 0),
               ("cat", 784, 420, 0)]


# =================================================================== Level 1617 velvet-blue train-car lounge (blue)
SB = PersonaS((40, 60, 200))


def l1617(g, S, d):
    g.fill(Box(-2, -2, W + 2, H + 2), (20, 30, 110))
    g.fill(Box(-2, -2, W + 2, H + 2), (60, 90, 220), alpha=halftone(lambda X, Y: 0.4 * smooth(600, 0, Y), 6.0))
    # windows with a starry void passing by
    for x0 in (60, 340, 620):
        S.obj(g, Box(x0, 70, x0 + 220, 230, 30), (10, 14, 50), x0)
        for sx, sy in ((x0 + 40, 110), (x0 + 120, 150), (x0 + 180, 100), (x0 + 80, 190)):
            g.fill(star(sx, sy, 6), WHITE)
    if "moon" not in d:
        S.obj(g, Circ(450, 140, 34) - Circ(466, 130, 30), (250, 248, 220), 1)
    # brass rails, velvet seats
    g.fill(Box(-2, 260, W + 2, 270), (220, 180, 70))
    for x0, x1 in ((20, 300), (600, 880)):
        S.obj(g, Box(x0, 300, x1, 440, 16), (40, 60, 180), x0 + 1, hi=True)
        S.obj(g, Box(x0, 420, x1, 480, 10), (30, 46, 150), x0 + 2)
    # floor carpet with a diamond pattern
    g.fill(Box(-2, 480, W + 2, H + 2), (16, 20, 70))
    for k in range(-2, 12):
        g.fill(Ring(Poly([(k * 100, 540), (k * 100 + 50, 500), (k * 100 + 100, 540), (k * 100 + 50, 580)]), 1.5), (80, 120, 240))
    # table with a gramophone, cards and a rose
    S.obj(g, Box(330, 420, 570, 440, 4), (30, 30, 50), 3)
    S.obj(g, Box(440, 440, 460, 560), (30, 30, 50), 4)
    S.obj(g, Box(360, 390, 420, 420, 3), (120, 70, 40), 5)
    S.obj(g, Union([Poly([(380, 392), (350, 330), (420, 320), (396, 392)])]), (220, 180, 70) if "horn" not in d else (200, 200, 210), 6, hi=True)
    for k, c in enumerate(((250, 250, 250), (250, 250, 250), (230, 30, 40))):
        if "card" in d and k == 2:
            c = (250, 210, 60)
        S.obj(g, Poly([(466 + k * 28, 420), (492 + k * 28, 420), (498 + k * 28, 382), (472 + k * 28, 382)]), c, 7 + k)
    S.obj(g, Union([Ell(546, 400, 10, 20), Box(540, 416, 552, 420)]), (180, 200, 250), 10, hi=True)
    S.obj(g, Circ(546, 366, 15), (40, 60, 200) if "rose" not in d else (230, 30, 40), 11, hi=True)
    # the attendant (original) holding a book
    student(g, S, 720, 600, 270, (30, 50, 170), face=-1, skirt=True, hair=(230, 230, 240), seed=12, tie=(40, 60, 200))
    S.obj(g, Box(660, 436, 704, 470, 2), (40, 60, 200) if "book" not in d else (230, 30, 40), 13)
    g.fill(Box(680, 436, 684, 470), (220, 180, 70))
    # lamp
    g.fill(Seg(160, -2, 160, 30, 1.6), (220, 180, 70))
    if "lamp" not in d:
        S.glow(g, 160, 50, 60, (180, 210, 255), 0.4)
    S.obj(g, Union([Poly([(140, 30), (180, 30), (190, 56), (130, 56)])]), (220, 180, 70), 14)


L1617_EL = [E("void", el(lambda g, m: [g.fill(star(x, y, 4), WHITE) for x, y in ((100, 120), (380, 200), (660, 120), (760, 180))]),
              anim=dict(driftVelocity=(-80, 0), driftLength=240, driftFade=True)),
            sparkle_el("tw", [(200, 110), (500, 180), (800, 100)], col=WHITE, r=6, speed=0.5)]
L1617_DIFFS = [("moon", 440, 145, 0), ("horn", 386, 356, 0), ("card", 534, 405, 0), ("rose", 546, 370, 0), ("book", 682, 453, 0),
               ("lamp", 160, 44, 0)]


# =================================================================== Level 1618 rainy shopping arcade (yellow)
SY = PersonaS((250, 210, 30))


def l1618(g, S, d):
    g.fill(Box(-2, -2, W + 2, H + 2), (250, 210, 30))
    slashes(g, (230, 170, 10), n=6, seed=3, alpha=0.8)
    g.fill(Box(-2, -2, W + 2, H + 2), BLACK, alpha=halftone(lambda X, Y: 0.3 * smooth(0, 300, Y) * smooth(600, 300, Y), 5.0))
    # arcade roof
    S.obj(g, Poly([(-20, 0), (920, 0), (920, 60), (-20, 60)]), (40, 36, 40), 1)
    for x in range(0, 900, 90):
        g.fill(Box(x, 0, x + 6, 60), (250, 210, 30))
    # shops
    shops = ((-20, 280, (230, 230, 220)), (300, 600, (200, 200, 210)), (620, 920, (230, 220, 200)))
    for i, (x0, x1, c) in enumerate(shops):
        S.obj(g, Box(x0, 80, x1, 470), c, 2 + i)
        S.obj(g, Box(x0 + 10, 90, x1 - 10, 140, 4), BLACK, 5 + i)
        g.fill(Box(x0 + 30, 108, x0 + 30 + (x1 - x0) * 0.5, 122, 4), (250, 210, 30))
    # shutters (left) with stripes
    S.obj(g, Box(20, 170, 260, 470), (200, 200, 200), 8)
    for y in range(176, 470, 12):
        g.fill(Box(20, y, 260, y + 3), (140, 140, 140))
    if "graffiti" not in d:
        g.fill(star(140, 300, 40), (250, 210, 30))
        g.fill(Ring(star(140, 300, 40), 2.5), BLACK)
    # electronics shop window with a glowing TV (abstract static)
    S.obj(g, Box(330, 170, 570, 400, 4), (30, 30, 40), 9)
    S.obj(g, Box(380, 220, 520, 330, 8), (60, 60, 70), 10)
    g.fill(Box(392, 232, 508, 318), (250, 230, 120) if "tv" not in d else (120, 200, 250))
    g.fill(Box(392, 232, 508, 318), BLACK, alpha=halftone(lambda X, Y: 0.35 + 0.2 * np.sin(Y * 0.8), 3.0))
    S.obj(g, Box(430, 330, 470, 350), (60, 60, 70), 11)
    # vending machine (right shop)
    S.obj(g, Box(650, 200, 760, 460, 4), (230, 30, 40), 12)
    S.obj(g, Box(664, 214, 746, 330, 3), (250, 250, 240) if "vend" not in d else (60, 60, 70), 13)
    for k in range(3):
        for j in range(3):
            S.obj(g, Box(672 + j * 26, 224 + k * 34, 690 + j * 26, 250 + k * 34, 2), [(40, 120, 220), (250, 210, 30), (60, 180, 90)][(k + j) % 3], 14)
    # wet street
    g.fill(Box(-2, 470, W + 2, H + 2), (40, 36, 40))
    for x, w in ((100, 120), (420, 160), (720, 100)):
        g.fill(Ell(x, 540, w / 2, 10), (250, 210, 30), alpha=0.5)
    # student with an umbrella, and a cat
    student(g, S, 820, 596, 240, (30, 30, 40), face=-1, seed=15, hair=(80, 50, 30))
    g.fill(Seg(796, 370, 796, 470, 2), BLACK)
    S.obj(g, Inter(Ell(796, 374, 80, 40), Box(716, 330, 880, 374)), (250, 210, 30) if "umbrella" not in d else (230, 30, 40), 16)
    if "cat" not in d:
        g.fill(Union([Ell(560, 560, 24, 14), Circ(586, 548, 11), Poly([(578, 540), (580, 528), (586, 538)]), Poly([(588, 538), (594, 528), (596, 540)]), Seg(536, 556, 520, 534, 3)]), (250, 248, 244))
        g.fill(Ring(Union([Ell(560, 560, 24, 14), Circ(586, 548, 11)]), 1.5), BLACK)


L1618_EL = [E("rain", el(lambda g, m: [g.fill(Seg(x, y, x - 6, y + 22, 1.4), BLACK) for x, y in ((80, 160), (240, 300), (400, 120), (560, 260), (720, 140), (860, 320), (300, 420), (640, 400))]),
              bbox=(-20, 60, 920, 620), anim=dict(driftVelocity=(-60, -300), driftLength=160)),
            E("static", el(lambda g, m: g.fill(Box(392, 232, 508, 318), WHITE, alpha=0.35)), daynight="untinted", anim=dict(blinkInterval=0.6, blinkDuration=0.15))]
L1618_DIFFS = [("graffiti", 140, 300, 0), ("tv", 450, 275, 0), ("vend", 705, 300, 0), ("umbrella", 796, 356, 0), ("cat", 566, 552, 0)]


# =================================================================== Level 1619 golden palace vault (red / gold)
SG = PersonaS((220, 30, 40))


def l1619(g, S, d):
    g.fill(Box(-2, -2, W + 2, H + 2), (120, 10, 30))
    slashes(g, (180, 20, 40), n=7, seed=4, alpha=0.9)
    # golden columns and arches
    for x in (60, 240, 660, 840):
        S.obj(g, Box(x - 34, 40, x + 34, 520), (230, 180, 60), x, hi=True)
        for k in range(4):
            g.fill(Box(x - 30 + k * 18, 50, x - 26 + k * 18, 510), (180, 130, 30))
    S.obj(g, Diff(Box(-20, -2, 920, 80), Union([Ell(450, 80, 300, 60)])), (230, 180, 60), 1)
    # chandelier
    if "chandelier" not in d:
        g.fill(Seg(450, -2, 450, 60, 2), BLACK)
        S.obj(g, Ell(450, 80, 90, 14), (240, 200, 80), 2, hi=True)
        for x in range(380, 530, 30):
            g.fill(Union([Poly([(x - 6, 80), (x, 96), (x + 6, 80)])]), WHITE)
    # pedestal with the treasure under a spotlight
    g.fill(Poly([(420, -2), (480, -2), (560, 400), (340, 400)]), (255, 240, 180), alpha=0.25)
    S.obj(g, Box(390, 330, 510, 470, 4), (240, 230, 220), 3)
    S.obj(g, Box(380, 316, 520, 334, 3), (230, 180, 60), 4)
    if "crown" not in d:
        S.obj(g, Poly([(410, 316), (410, 270), (430, 290), (450, 256), (470, 290), (490, 270), (490, 316)]), (250, 210, 60), 5, hi=True)
        g.fill(Circ(450, 296, 8), (60, 120, 220))
    # red carpet and floor
    g.fill(Box(-2, 470, W + 2, H + 2), (40, 10, 20))
    S.obj(g, Poly([(380, 470), (520, 470), (640, 610), (260, 610)]), (210, 30, 40), 6)
    g.fill(Poly([(380, 470), (392, 470), (276, 610), (260, 610)]), (240, 200, 80))
    g.fill(Poly([(508, 470), (520, 470), (640, 610), (624, 610)]), (240, 200, 80))
    # knight statues
    for x, key in ((150, None), (750, "statue")):
        S.obj(g, Box(x - 40, 420, x + 40, 470), (200, 190, 180), x + 1)
        S.obj(g, Union([Box(x - 22, 300, x + 22, 420, 6), Ell(x, 286, 18, 20)]), (210, 200, 190), x + 2, hi=True)
        if not (key and key in d):
            g.fill(Seg(x + 26, 230, x + 26, 420, 3), (230, 230, 240))
            g.fill(Box(x + 14, 400, x + 38, 406), (230, 180, 60))
    # the masked thief (original: long dark coat, white domino mask, red gloves)
    x, base = 600, 600
    S.obj(g, Poly([(x - 36, base - 210), (x + 30, base - 210), (x + 60, base - 20), (x - 70, base - 30)]), (24, 20, 28), 7)
    S.obj(g, Box(x - 18, base - 120, x - 4, base, 3), (30, 26, 34), 8)
    S.obj(g, Box(x + 4, base - 120, x + 18, base, 3), (30, 26, 34), 9)
    S.obj(g, Seg(x + 24, base - 200, x + 70, base - 260, 7), (24, 20, 28), 10)
    S.obj(g, Circ(x + 72, base - 264, 15), (220, 30, 40) if "gloves" not in d else (250, 250, 240), 11)
    S.obj(g, Ell(x, base - 236, 22, 26), (240, 210, 190), 12)
    S.obj(g, Union([Ell(x - 4, base - 254, 24, 16), Poly([(x - 26, base - 250), (x - 30, base - 214), (x - 14, base - 240)])]), BLACK, 13)
    g.fill(Union([Ell(x - 6, base - 236, 10, 6), Ell(x + 12, base - 236, 10, 6), Poly([(x - 20, base - 238), (x - 34, base - 248), (x - 16, base - 232)])]), WHITE)
    g.fill(Circ(x + 10, base - 236, 2.4), BLACK)
    # a red rose dropped on the carpet
    if "rose" not in d:
        g.fill(Seg(330, 560, 380, 540, 2), (40, 120, 60))
        S.obj(g, Circ(330, 562, 12), (230, 30, 40), 14, hi=True)
    g.fill(star(820, 560, 30), (250, 210, 60))
    g.fill(Ring(star(820, 560, 30), 2.5), BLACK)


L1619_EL = [sparkle_el("treasure", [(450, 290), (430, 270), (480, 300)], col=WHITE, r=8, speed=0.7),
            E("beam", el(lambda g, m: g.fill(Poly([(430, -2), (470, -2), (530, 400), (370, 400)]), (255, 250, 220), alpha=0.12)), daynight="untinted",
              anim=dict(twinkle=0.6, twinkleSpeed=0.3))]
L1619_DIFFS = [("chandelier", 450, 80, 0), ("crown", 450, 290, 0), ("statue", 776, 320, 0), ("gloves", 672, 336, 0), ("rose", 340, 556, 0)]


LEVELS = [
    ("Level1615", "放学天台", make(SR, l1615), L1615_EL, L1615_DIFFS, 60, OPTS),
    ("Level1616", "午夜路口", make(SR, l1616), L1616_EL, L1616_DIFFS, 60, OPTS),
    ("Level1617", "蓝色车厢", make(SB, l1617), L1617_EL, L1617_DIFFS, 60, OPTS),
    ("Level1618", "雨夜商店街", make(SY, l1618), L1618_EL, L1618_DIFFS, 60, OPTS),
    ("Level1619", "黄金殿堂", make(SG, l1619), L1619_EL, L1619_DIFFS, 60, OPTS),
]
