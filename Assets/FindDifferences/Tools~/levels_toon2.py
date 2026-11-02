# -*- coding: utf-8 -*-
"""Cel-shaded (toon render) fairy-tale levels - toon.py helpers (ink outlines, flat colour, one hard cool shadow,
small highlights, gradient skies). Original designs of public-domain fairy-tale motifs:
  Level1542 糖果小屋   - a candy cottage in a forest clearing: icing-trimmed cookie walls, lollipop trees, candy-cane fence
  Level1543 高塔长发   - a stone tower in the woods, a long golden braid from its window, a knight on a white horse
  Level1544 蘑菇精灵村 - a mushroom fairy village at night: lit mushroom houses, lantern strings, pond, fireflies
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, el, fbm1, lgrad, mixc, rgrad, vgrad
from toon import (INK, Grow, bird_el, cel, cloud_el, figure, hill, ink, puff_el, shade_of, sparkle_el, tint_of, toon_cloud,
                  toon_post, toon_tree, toon_window)

OPTS = dict(post=toon_post, anim_seconds=12.0, frames=60)


def star(cx, cy, r, ri=None, n=5, rot=-math.pi / 2):
    ri = ri or r * 0.45
    return Poly([(cx + (r if i % 2 == 0 else ri) * math.cos(rot + i * math.pi / n), cy + (r if i % 2 == 0 else ri) * math.sin(rot + i * math.pi / n))
                 for i in range(2 * n)])


def heart(cx, cy, s):
    return Union([Circ(cx - s * 0.5, cy - s * 0.2, s * 0.55), Circ(cx + s * 0.5, cy - s * 0.2, s * 0.55),
                  Poly([(cx - s * 1.02, cy - s * 0.05), (cx + s * 1.02, cy - s * 0.05), (cx, cy + s * 1.1)])])


def lollipop(g, x, base, h, r, cols, seed=0):
    cel(g, Box(x - 3, base - h, x + 3, base, 1.5), (250, 246, 236), w=1.6, off=(-2, 0))
    cx, cy = x, base - h - r
    cel(g, Circ(cx, cy, r), cols[0], w=2.0, off=(-r * 0.25, -r * 0.25))
    for k in range(1, 4):
        g.fill(Circ(cx, cy, r * (1 - k * 0.22)) - Circ(cx, cy, r * (1 - k * 0.22) - r * 0.09), cols[k % len(cols)])
    g.fill(Ell(cx - r * 0.4, cy - r * 0.45, r * 0.22, r * 0.12), (255, 255, 255))


def candy_cane(g, x, base, h, seed=0, stripe=(220, 40, 50)):
    body = Union([Box(x - 4, base - h, x + 4, base, 2), Inter(Circ(x + 10, base - h, 14) - Circ(x + 10, base - h, 6), Box(x - 6, base - h - 16, x + 26, base - h))])
    cel(g, body, (250, 248, 240), w=1.6, off=(-2.5, 0))
    for k in range(int(h / 12)):
        y = base - 6 - k * 12
        g.fill(Inter(Poly([(x - 5, y), (x + 5, y - 6), (x + 5, y - 11), (x - 5, y - 5)]), body), stripe)


def gumdrop(g, x, y, r, col):
    cel(g, Inter(Ell(x, y, r, r * 1.05), Box(x - r - 1, y - r * 1.1, x + r + 1, y + 1)), col, w=1.6, off=(-r * 0.3, -r * 0.2), hi=True, hi_off=(r * 0.12, r * 0.14))
    for k in range(5):
        g.fill(Circ(x - r * 0.6 + k * r * 0.3, y - r * 0.45 - (k % 2) * r * 0.2, 1.3), (255, 255, 255))


def icing(g, x0, x1, y, r=6, col=(255, 255, 255), drip=True, seed=0):
    rnd = random.Random(seed)
    n = max(2, int((x1 - x0) / (r * 1.6)))
    parts = [Circ(x0 + (x1 - x0) * k / (n - 1), y, r) for k in range(n)]
    if drip:
        parts += [Box(x - 2.4, y, x + 2.4, y + rnd.uniform(6, 14), 2.4) for x in np.linspace(x0 + 6, x1 - 6, max(1, n // 2))]
    sh = Union(parts)
    ink(g, sh, col, 1.4)
    g.fill(Diff(sh, Moved(sh, -1.5, -2)), (226, 220, 236))


# =================================================================== Level 1542 candy cottage
def l1542_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, 330), vgrad([(0, (110, 190, 250)), (300, (250, 226, 196))]))
    toon_cloud(g, 160, 70, 90, 26, seed=4201)
    toon_cloud(g, 720, 50, 110, 30, seed=4202)
    hill(g, lambda x: 250 - 30 * fbm1(x, 140, 3, 4203), (150, 200, 170), rim=0)
    for k, x in enumerate(range(-20, 940, 46)):
        h = 130 + (k * 37 % 50)
        toon_tree(g, x, 310 + (k % 2) * 8, h, col=(60, 130, 90) if k % 2 else (50, 116, 84), seed=4210 + k, w=1.4, round_=False)
    hill(g, lambda x: 330 + 10 * np.sin(x * 0.01), (140, 214, 110), w=2.0, rim=8, tufts=140, seed=4204)
    # path of gumdrops leading to the door
    g.fill(Poly([(400, H + 4), (560, H + 4), (500, 432), (450, 432)]), (246, 222, 170))
    g.fill(Diff(Poly([(400, H + 4), (560, H + 4), (500, 432), (450, 432)]), Poly([(406, H + 4), (554, H + 4), (497, 436), (453, 436)])), INK)
    for k, t in enumerate(np.linspace(0.08, 0.92, 6)):
        for side in (-1, 1):
            x = 475 + side * (25 + 55 * t) + (5 if side > 0 else -5)
            y = 432 + (H - 432) * t
            if side > 0 and k == 3 and "gumdrop" in d:
                continue
            gumdrop(g, x, y, 8 + 8 * t, ((240, 80, 120), (90, 190, 240), (250, 200, 60), (140, 210, 90))[(k + (side > 0)) % 4])
    # cottage: cookie walls, chocolate roof with pink frosting, candies
    x0, x1, base, wh = 330, 610, 432, 130
    g.mul(Box(x0 + 6, base - 4, x1 + 30, base + 10), 0.45)
    wall = Box(x0, base - wh, x1, base)
    cel(g, wall, (210, 150, 90), w=2.4, off=(-24, 0))
    rnd = random.Random(4220)
    for _ in range(40):
        g.fill(Circ(rnd.uniform(x0 + 8, x1 - 8), rnd.uniform(base - wh + 10, base - 8), 2.2), (160, 100, 60))
    icing(g, x0 + 2, x1 - 2, base - 6, 6, seed=4221, drip=False)
    roof = Poly([(x0 - 30, base - wh + 6), ((x0 + x1) / 2, base - wh - 150), (x1 + 30, base - wh + 6)])
    cel(g, roof, (120, 70, 50), w=2.4, off=(-30, 0), hi=True, hi_off=(6, 4))
    for k in range(5):                    # chocolate bar grid
        t = (k + 1) / 6
        a = ((x0 - 30) + ((x0 + x1) / 2 - (x0 - 30)) * t, (base - wh + 6) + (-150 - 6) * t)
        b = ((x1 + 30) + ((x0 + x1) / 2 - (x1 + 30)) * t, (base - wh + 6) + (-150 - 6) * t)
        g.fill(Seg(a[0], a[1], b[0], b[1], 2.2), (90, 50, 36))
    for side in (-1, 1):                  # pink frosting along the eaves
        for k in range(9):
            t = k / 8
            px = (x0 + x1) / 2 + side * (((x1 - x0) / 2 + 30) * t)
            py = base - wh - 150 + (156) * t
            sh = Union([Circ(px, py, 9), Box(px - 3, py, px + 3, py + 8 + (k % 3) * 5, 3)])
            ink(g, sh, (250, 160, 200), 1.4)
            g.fill(Diff(sh, Moved(sh, -1.5, -2)), (220, 120, 170))
    for k, (cx, cy, col) in enumerate(((430, 236, (240, 70, 90)), (510, 236, (90, 190, 240)), (470, 196, (250, 210, 60)), (400, 270, (140, 210, 90)),
                                       (540, 270, (240, 140, 200)))):
        if k == 2 and "candy" in d:
            continue
        cel(g, Circ(cx, cy, 13), col, w=1.8, off=(-4, -4), hi=True, hi_off=(2, 2))
        g.fill(Poly([(cx - 13, cy), (cx - 24, cy - 8), (cx - 24, cy + 8)]), col)
        g.fill(Poly([(cx + 13, cy), (cx + 24, cy - 8), (cx + 24, cy + 8)]), col)
    # chimney (difference: stripes)
    ch = Box(552, 168, 584, 236, 3)
    cel(g, ch, (250, 248, 240), w=2.0, off=(-8, 0))
    if "chimney" not in d:
        for k in range(5):
            y = 176 + k * 13
            g.fill(Inter(Poly([(552, y), (584, y - 8), (584, y - 2), (552, y + 6)]), ch), (220, 40, 50))
    icing(g, 548, 588, 170, 5, seed=4222, drip=True)
    # windows (difference: right one heart shaped) and cake door
    wl = Circ(380, 360, 26)
    ink(g, Grow(wl, 6), (255, 255, 255), 1.8)
    toon_window(g, 358, 338, 402, 382, glass=(160, 220, 250), frame=(255, 255, 255), w=0)
    wr_shape = Circ(560, 360, 26) if "window" not in d else heart(560, 364, 26)
    ink(g, Grow(wr_shape, 6), (255, 255, 255), 1.8)
    g.fill(wr_shape, (160, 220, 250))
    g.fill(Inter(wr_shape, Poly([(540, 390), (556, 390), (580, 330), (564, 330)])), (210, 240, 255))
    door = Union([Box(440, 350, 500, base), Circ(470, 350, 30)])
    cel(g, door, (250, 200, 210), w=2.2, off=(-10, 0))
    for y in (372, 400):
        g.fill(Box(440, y, 500, y + 6), (240, 120, 160))
    g.fill(Circ(492, 396, 3.2), (250, 220, 90))
    icing(g, 438, 502, 322, 5, seed=4223, drip=False)
    # cupcake on the step (difference)
    if "cupcake" not in d:
        cx, cy = 520, 444
        cel(g, Poly([(cx - 14, cy - 16), (cx + 14, cy - 16), (cx + 10, cy), (cx - 10, cy)]), (240, 120, 160), w=1.6, off=(-4, 0))
        cel(g, Union([Circ(cx, cy - 24, 13), Circ(cx - 8, cy - 18, 8), Circ(cx + 8, cy - 18, 8)]), (255, 250, 240), w=1.6, off=(-4, -4))
        cel(g, Circ(cx, cy - 38, 5), (220, 40, 50), w=1.2, off=(-2, -2))
    # lollipop trees (difference: right one's colour)
    lollipop(g, 230, 440, 120, 46, [(240, 80, 120), (255, 255, 255), (250, 200, 220)], 4230)
    lollipop(g, 740, 450, 140, 52, [(90, 190, 240), (255, 255, 255), (200, 236, 250)] if "lolly" not in d else [(140, 210, 90), (255, 255, 255), (220, 250, 200)], 4231)
    lollipop(g, 860, 420, 90, 34, [(250, 200, 60), (255, 255, 255), (255, 240, 180)], 4232)
    # candy-cane fence (difference: one cane)
    for k, x in enumerate(range(30, 330, 42)):
        if k == 4 and "cane" in d:
            continue
        candy_cane(g, x, 560, 70, 4240 + k)
    g.fill(Box(20, 520, 330, 528, 3), (250, 248, 240))
    # children (original) walking to the house
    figure(g, 300, 560, 64, (90, 150, 220), pants=(70, 80, 120), hair=(120, 80, 40))
    figure(g, 350, 566, 56, (240, 110, 120), pants=(240, 110, 120), hair=(230, 180, 80))
    # crow on a branch (difference)
    g.fill(Seg(760, 120, 900, 100, 7, 4), (110, 80, 60))
    if "crow" not in d:
        cel(g, Ell(820, 98, 18, 12), (50, 50, 66), w=1.6, off=(-5, -4))
        cel(g, Circ(802, 88, 9), (50, 50, 66), w=1.6, off=(-3, -3))
        g.fill(Poly([(794, 88), (782, 92), (794, 94)]), (250, 200, 60))
        g.fill(Circ(800, 86, 2), (255, 255, 255))
        g.fill(Poly([(836, 98), (856, 108), (838, 106)]), (50, 50, 66))
    # foreground flowers
    rnd = random.Random(4250)
    for _ in range(14):
        x, y = rnd.uniform(560, 890), rnd.uniform(500, 590)
        col = rnd.choice([(250, 120, 160), (250, 220, 80), (255, 255, 255)])
        g.fill(Seg(x, y + 12, x, y, 1.6), (70, 140, 60))
        cel(g, Union([Circ(x + 5 * math.cos(a), y + 5 * math.sin(a), 4) for a in np.linspace(0, math.tau, 5, endpoint=False)]), col, w=1.2, off=(-1.5, -1.5))
        g.fill(Circ(x, y, 2.4), (250, 180, 60))
    g.commit()


L1542_ELEMENTS = [
    puff_el("smoke1", 568, 150, r=10, rise=60, wind=-12, col=(255, 230, 240)),
    puff_el("smoke2", 572, 150, r=8, rise=60, wind=-10, phase=0.5, col=(255, 230, 240)),
    cloud_el("cloud", 420, 90, 60, 18, speed=5, seed=4260),
    sparkle_el("sparkle", [(470, 196), (380, 360), (740, 252), (230, 274)], r=6, speed=0.7),
    bird_el("bird", 300, 140, s=7, speed=-20),
]

L1542_DIFFS = [
    ("candy", 470, 196, 0),
    ("chimney", 568, 200, 0),
    ("window", 560, 362, 0),
    ("cupcake", 520, 424, 0),
    ("lolly", 740, 258, 0),
    ("cane", 198, 520, 0),
    ("crow", 816, 94, 0),
    ("gumdrop", 532, 520, 0),
]


# =================================================================== Level 1543 the tower and the long braid
def l1543_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, 340), vgrad([(0, (100, 120, 200)), (160, (200, 160, 210)), (320, (255, 200, 170))]))
    g.fill(Circ(760, 90, 30), (255, 250, 220))
    g.fill(Circ(772, 82, 26), vgrad([(0, (100, 120, 200)), (160, (200, 160, 210))]))
    toon_cloud(g, 520, 80, 110, 26, col=(255, 230, 240), shade=(230, 190, 220), line=(200, 150, 190), seed=4301)
    hill(g, lambda x: 270 - 40 * fbm1(x, 160, 3, 4302), (150, 140, 200), rim=0)
    hill(g, lambda x: 310 - 30 * fbm1(x, 120, 3, 4303), (110, 150, 160), rim=0)
    for k, x in enumerate(range(380, 940, 40)):
        toon_tree(g, x, 336, 100 + (k * 23 % 40), col=(70, 130, 100), seed=4310 + k, w=1.2, round_=k % 3 != 0)
    hill(g, lambda x: 360 + 12 * np.sin(x * 0.008 + 1), (120, 196, 110), w=2.0, rim=8, tufts=120, seed=4304)
    # stream with stepping stones (difference: one stone)
    stream = Poly([(560, 360), (620, 360), (560, 450), (360, 540), (300, H + 4), (160, H + 4), (260, 520), (480, 430)])
    ink(g, stream, (120, 200, 240), 2.0)
    rnd = random.Random(4305)
    for _ in range(26):
        x, y = rnd.uniform(220, 600), rnd.uniform(370, 590)
        g.fill(Inter(Seg(x, y, x + rnd.uniform(10, 30), y, 2), stream), (236, 248, 255))
    for k, (x, y) in enumerate(((330, 548), (380, 512), (430, 478), (482, 446))):
        if k == 2 and "stone" in d:
            continue
        cel(g, Ell(x, y, 22, 10), (190, 190, 200), w=1.8, off=(-6, -3), hi=True, hi_off=(2, 2))
    # the tower
    tx0, tx1, tb, tt = 170, 290, 480, 150
    g.mul(Box(tx0 + 10, tb - 4, tx1 + 50, tb + 12), 0.4)
    tower = Box(tx0, tt, tx1, tb)
    cel(g, tower, (210, 200, 196), w=2.4, off=(-34, 0))
    for r_, y in enumerate(range(int(tt) + 12, tb, 20)):
        g.fill(Seg(tx0 + 2, y, tx1 - 2, y, 1.4), shade_of((210, 200, 196), 0.85))
        for x in range(tx0 + (10 if r_ % 2 else 30), tx1, 40):
            g.fill(Seg(x, y, x, y + 20, 1.4), shade_of((210, 200, 196), 0.85))
    roof = Poly([(tx0 - 24, tt + 6), ((tx0 + tx1) / 2, tt - 92), (tx1 + 24, tt + 6)])
    cel(g, roof, (80, 110, 200), w=2.4, off=(-30, 0), hi=True, hi_off=(4, 3))
    for k in range(4):
        y = tt - 72 + k * 20
        hw = (y - (tt - 92)) / 98 * ((tx1 - tx0) / 2 + 24)
        g.fill(Seg((tx0 + tx1) / 2 - hw, y, (tx0 + tx1) / 2 + hw, y, 1.6), shade_of((80, 110, 200), 0.8))
    apx = (tx0 + tx1) / 2
    g.fill(Seg(apx, tt - 92, apx, tt - 132, 2.4), INK)
    if "flag" not in d:
        cel(g, Poly([(apx + 1, tt - 130), (apx + 44, tt - 120), (apx + 1, tt - 106)]), (240, 90, 100), w=1.6, off=(0, -5))
    # window with the girl and the braid
    win = Union([Box(204, 196, 256, 250), Circ(230, 196, 26)])
    ink(g, Grow(win, 6), (190, 180, 176), 2.0)
    g.fill(win, (60, 50, 70))
    cel(g, Circ(230, 214, 13), (250, 214, 186), w=1.6, off=(-4, -4))
    g.fill(Ell(230, 204, 15, 9), (250, 210, 90))
    g.fill(Circ(225, 214, 1.6), INK)
    g.fill(Circ(235, 214, 1.6), INK)
    g.fill(Seg(227, 220, 233, 220, 1.2), (200, 90, 90))
    cel(g, Box(214, 228, 246, 250, 6), (170, 120, 210), w=1.6, off=(-6, 0))
    braid = []
    for k in range(18):
        t = k / 17
        bx = 244 + 30 * math.sin(t * 3.0) * (1 - t) + t * 40
        by = 230 + t * 250
        braid.append(Ell(bx + (3 if k % 2 else -3), by, 9, 12))
    cel(g, Union(braid), (250, 206, 80), w=1.6, off=(-4, -4))
    for k in range(18):
        t = k / 17
        bx = 244 + 30 * math.sin(t * 3.0) * (1 - t) + t * 40
        by = 230 + t * 250
        g.fill(Seg(bx - 6, by - 4, bx + 6, by + 4, 1.2), (220, 160, 50))
    if "flowers" not in d:              # window box
        cel(g, Box(198, 252, 262, 264, 2), (160, 110, 70), w=1.6, off=(-4, 0))
        for k, x in enumerate(range(204, 260, 10)):
            cel(g, Circ(x, 248, 5), ((250, 110, 140), (255, 220, 80), (255, 255, 255))[k % 3], w=1.2, off=(-1.5, -1.5))
    # tower door and ivy
    cel(g, Union([Box(208, 410, 252, tb), Circ(230, 410, 22)]), (130, 90, 70), w=2.0, off=(-8, 0))
    for k in range(18):
        x, y = 176 + (k * 13) % 30, 300 + k * 10
        cel(g, Ell(x, y, 8, 5), (80, 160, 80), w=1.2, off=(-2, -2))
    # knight on a white horse (difference: saddle cloth colour)
    hx, hb = 640, 500
    g.mul(Ell(hx + 10, hb + 2, 110, 10), 0.4)
    for lx in (-60, -40, 36, 56):
        cel(g, Box(hx + lx - 6, hb - 60, hx + lx + 6, hb, 3), (246, 244, 240), w=1.8, off=(-3, 0))
        g.fill(Box(hx + lx - 7, hb - 8, hx + lx + 7, hb, 2), (120, 110, 120))
    body = Ell(hx, hb - 80, 80, 34)
    cel(g, body, (250, 248, 244), w=2.2, off=(-12, -10))
    neck = Poly([(hx + 50, hb - 100), (hx + 74, hb - 160), (hx + 98, hb - 150), (hx + 80, hb - 86)])
    cel(g, neck, (250, 248, 244), w=2.2, off=(-6, 0))
    cel(g, Ell(hx + 100, hb - 160, 26, 14), (250, 248, 244), w=2.2, off=(-6, -4))
    g.fill(Circ(hx + 102, hb - 166, 2.4), INK)
    cel(g, Poly([(hx + 64, hb - 168), (hx + 76, hb - 172), (hx + 62, hb - 104), (hx + 52, hb - 106)]), (210, 180, 90), w=1.4, off=(-3, 0))
    cel(g, Poly([(hx - 78, hb - 96), (hx - 108, hb - 74), (hx - 102, hb - 44), (hx - 84, hb - 78)]), (210, 180, 90), w=1.4, off=(-3, 0))
    # rider seated: torso + cape, legs hidden by the saddle cloth
    cel(g, Poly([(hx - 10, hb - 160), (hx + 8, hb - 160), (hx - 30, hb - 104), (hx - 44, hb - 112)]), (220, 70, 80), w=1.6, off=(-4, 0))
    cel(g, Box(hx - 12, hb - 156, hx + 12, hb - 110, 5), (170, 176, 196), w=1.6, off=(-5, -2))
    cel(g, Seg(hx + 8, hb - 146, hx + 30, hb - 126, 8), (170, 176, 196), w=1.4, off=(-2, 0))
    cel(g, Circ(hx, hb - 166, 10), (250, 214, 186), w=1.6, off=(-3, -3))
    sc = (60, 110, 200) if "saddle" not in d else (220, 70, 80)
    cel(g, Poly([(hx - 30, hb - 116), (hx + 30, hb - 116), (hx + 36, hb - 64), (hx - 36, hb - 64)]), sc, w=1.8, off=(-6, 0))
    g.fill(Box(hx - 36, hb - 70, hx + 36, hb - 64), (250, 210, 90))
    cel(g, Box(hx - 6, hb - 112, hx + 6, hb - 70, 3), (150, 156, 176), w=1.4, off=(-2, 0))
    cel(g, Union([Circ(hx, hb - 172, 11), Box(hx - 11, hb - 172, hx + 11, hb - 164)]) - Box(hx - 6, hb - 170, hx + 6, hb - 164), (190, 196, 210), w=1.6, off=(-3, -3))
    cel(g, Ell(hx - 4, hb - 190, 8, 12), (240, 90, 100), w=1.4, off=(-2, -3))
    # trees, mushrooms (difference), bluebird on a branch (difference)
    toon_tree(g, 60, 500, 260, col=(80, 160, 90), seed=4320, w=2.2)
    toon_tree(g, 860, 520, 230, col=(90, 170, 80), seed=4321, w=2.2)
    g.fill(Seg(60, 330, 140, 300, 6, 3), (130, 90, 60))
    if "bird" not in d:
        cel(g, Ell(128, 292, 12, 8), (80, 150, 230), w=1.6, off=(-4, -3))
        cel(g, Circ(118, 284, 6), (80, 150, 230), w=1.4, off=(-2, -2))
        g.fill(Poly([(112, 284), (104, 286), (112, 288)]), (250, 200, 60))
        g.fill(Ell(130, 296, 6, 4), (250, 160, 120))
    if "mush" not in d:
        for k, (x, y, r) in enumerate(((760, 560, 18), (790, 570, 12), (740, 576, 10))):
            cel(g, Box(x - r * 0.3, y - r * 0.2, x + r * 0.3, y + r * 0.7, 2), (250, 244, 230), w=1.4, off=(-2, 0))
            cel(g, Inter(Ell(x, y, r, r * 0.75), Box(x - r - 1, y - r, x + r + 1, y)), (230, 70, 70), w=1.6, off=(-r * 0.3, -r * 0.2))
            g.fill(Circ(x - r * 0.3, y - r * 0.4, r * 0.15), (255, 255, 255))
            g.fill(Circ(x + r * 0.35, y - r * 0.3, r * 0.12), (255, 255, 255))
    rnd = random.Random(4330)
    for _ in range(18):
        x, y = rnd.uniform(20, 900), rnd.uniform(520, 595)
        if 160 < x < 420:
            continue
        col = rnd.choice([(250, 120, 160), (250, 220, 80), (180, 140, 250)])
        g.fill(Seg(x, y + 10, x, y, 1.6), (70, 140, 60))
        cel(g, Circ(x, y, 5), col, w=1.2, off=(-1.5, -1.5))
    g.commit()


L1543_ELEMENTS = [
    sparkle_el("stars", [(60, 40), (300, 30), (420, 70), (860, 40), (640, 30)], r=5, speed=0.6),
    sparkle_el("fireflies", [(330, 420), (560, 470), (130, 440), (810, 420)], col=(255, 240, 140), r=4, speed=0.4, phase=0.3),
    bird_el("bird2", 500, 150, s=7, speed=22),
    E("leaf", el(lambda g, m: cel(g, Ell(700, 180, 7, 4), (90, 170, 80), w=1.2, off=(-2, -2))),
      anim=dict(driftVelocity=(-14, -40), driftLength=260, driftFade=True, swingAngle=40, swingSpeed=0.7)),
]

L1543_DIFFS = [
    ("flag", 254, 32, 0),
    ("flowers", 230, 254, 0),
    ("stone", 430, 478, 0),
    ("saddle", 640, 400, 0),
    ("bird", 124, 290, 0),
    ("mush", 766, 560, 0),
]


# =================================================================== Level 1544 mushroom fairy village at night
NIGHT_SKY = [(0, (24, 26, 70)), (200, (70, 56, 130)), (320, (130, 80, 150))]


def mush_house(g, cx, base, stem_w, stem_h, cap_rx, cap_ry, cap, spots=True, lit=True, door=(120, 80, 60), seed=0, nspots=7):
    st = Box(cx - stem_w / 2, base - stem_h, cx + stem_w / 2, base, stem_w * 0.15)
    g.mul(Ell(cx + 10, base + 2, stem_w * 0.9, 8), 0.45)
    cel(g, st, (246, 232, 206), w=2.2, off=(-stem_w * 0.3, 0))
    dw = stem_w * 0.32
    cel(g, Union([Box(cx - dw / 2, base - stem_h * 0.42, cx + dw / 2, base), Circ(cx, base - stem_h * 0.42, dw / 2)]), door, w=1.8, off=(-dw * 0.25, 0))
    g.fill(Circ(cx + dw * 0.3, base - stem_h * 0.2, 2.4), (250, 220, 120))
    wy = base - stem_h * 0.7
    wl = Circ(cx - stem_w * 0.22, wy, stem_w * 0.12)
    ink(g, Grow(wl, 3), (150, 110, 80), 1.4)
    g.fill(wl, (255, 220, 120) if lit else (60, 60, 100))
    if lit:
        g.glow(cx - stem_w * 0.22, wy, stem_w * 0.4, (255, 200, 110), 0.35)
    cap_s = Inter(Ell(cx, base - stem_h, cap_rx, cap_ry), Box(cx - cap_rx - 2, base - stem_h - cap_ry - 2, cx + cap_rx + 2, base - stem_h + cap_ry * 0.25))
    cel(g, cap_s, cap, w=2.4, off=(-cap_rx * 0.22, -cap_ry * 0.25), hi=True, hi_off=(cap_rx * 0.05, cap_ry * 0.08))
    g.fill(Box(cx - cap_rx * 0.95, base - stem_h + cap_ry * 0.12, cx + cap_rx * 0.95, base - stem_h + cap_ry * 0.25), shade_of(cap, 0.6))
    if spots:
        rnd = random.Random(seed)
        for _ in range(nspots):
            a = rnd.uniform(0.15, math.pi - 0.15)
            rr = rnd.uniform(0.3, 0.8)
            x, y = cx + math.cos(a) * cap_rx * rr, base - stem_h - math.sin(a) * cap_ry * rr
            g.fill(Ell(x, y, cap_rx * 0.09, cap_ry * 0.1), (255, 250, 240))


def l1544_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, 330), vgrad(NIGHT_SKY))
    rnd = random.Random(4401)
    for _ in range(40):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, 240), rnd.uniform(1.2, 2.6)
        g.fill(star(x, y, r * 2, r * 0.6, 4), (255, 250, 220))
    g.fill(Circ(150, 80, 34), (255, 248, 210))
    g.fill(Circ(164, 70, 30), vgrad(NIGHT_SKY))
    g.glow(140, 86, 90, (255, 240, 200), 0.15)
    hill(g, lambda x: 280 - 40 * fbm1(x, 150, 3, 4402), (60, 60, 120), rim=0)
    for k, x in enumerate(range(-10, 940, 70)):           # giant grass blades silhouettes
        g.fill(Poly([(x, 330), (x + 24, 330), (x + 10 + (k % 3 - 1) * 20, 180 + (k * 31) % 60)]), (50, 70, 110))
    hill(g, lambda x: 340 + 14 * np.sin(x * 0.007 + 2), (70, 120, 100), w=2.0, rim=6, tufts=100, seed=4403)
    # pebble path
    for k in range(16):
        x = 420 + math.sin(k * 0.6) * 40 + k * 4
        y = 600 - k * 16
        cel(g, Ell(x, y, 14 - k * 0.5, 6 - k * 0.2), (170, 170, 190), w=1.2, off=(-3, -2))
    # pond with lily pads and a frog (difference)
    pond = Ell(660, 540, 150, 40)
    ink(g, pond, (60, 90, 150), 2.0)
    g.fill(Ell(640, 530, 120, 22), (80, 120, 180))
    for k, (x, y) in enumerate(((600, 540), (700, 530), (760, 552))):
        cel(g, Ell(x, y, 26, 10) - Poly([(x, y), (x + 30, y - 6), (x + 30, y + 2)]), (90, 170, 100), w=1.6, off=(-6, -3))
    if "frog" not in d:
        fx, fy = 600, 530
        cel(g, Ell(fx, fy, 16, 11), (110, 200, 100), w=1.8, off=(-5, -4))
        for e in (-1, 1):
            cel(g, Circ(fx + e * 8, fy - 11, 5), (110, 200, 100), w=1.4, off=(-1.5, -1.5))
            g.fill(Circ(fx + e * 8, fy - 11, 2.2), INK)
    # mushroom houses
    mush_house(g, 220, 470, 110, 150, 170, 110, (220, 60, 60), lit="win1" not in d, seed=4410, nspots=9)
    mush_house(g, 600, 440, 80, 110, 116, 70, (90, 130, 220) if "cap" not in d else (170, 90, 210), seed=4411, nspots=6)
    mush_house(g, 820, 430, 60, 80, 80, 50, (250, 200, 70), lit="win3" not in d, seed=4412, nspots=5)
    g.fill(Seg(640, 330, 640, 300, 8), (150, 140, 150))       # chimney on the blue one
    cel(g, Box(632, 290, 648, 300, 2), (150, 140, 150), w=1.4, off=(-3, 0))
    # lantern string between the houses (difference: one lantern colour)
    pts = [(360 + 220 * t, 330 + 40 * math.sin(t * math.pi)) for t in np.linspace(0, 1, 30)]
    for p0, p1 in zip(pts[:-1], pts[1:]):
        g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 1.4), (40, 30, 50))
    for k, t in enumerate(np.linspace(0.12, 0.88, 5)):
        x, y = 360 + 220 * t, 330 + 40 * math.sin(t * math.pi)
        col = ((255, 120, 120), (255, 220, 100), (140, 230, 160), (130, 190, 255), (240, 150, 240))[k]
        if k == 2 and "lantern" in d:
            col = (255, 150, 60)
        g.glow(x, y + 12, 26, col, 0.3)
        cel(g, Ell(x, y + 12, 8, 11), col, w=1.4, off=(-2.5, -3))
    # fairy resting on a bell flower (difference)
    fx, fy = 420, 360
    g.fill(Seg(fx, 470, fx - 6, fy + 10, 2.4), (70, 140, 80))
    cel(g, Inter(Ell(fx - 6, fy + 18, 16, 14), Box(fx - 24, fy + 2, fx + 12, fy + 20)), (180, 170, 255), w=1.6, off=(-4, -2))
    if "fairy" not in d:
        for e in (-1, 1):
            g.fill(Ell(fx - 6 + e * 12, fy - 10, 12, 7), (220, 240, 255), alpha=0.85)
            g.fill(Diff(Ell(fx - 6 + e * 12, fy - 10, 12, 7), Ell(fx - 6 + e * 12, fy - 10, 10.5, 5.5)), (150, 170, 230))
        cel(g, Poly([(fx - 12, fy + 6), (fx, fy + 6), (fx - 3, fy - 10), (fx - 9, fy - 10)]), (250, 160, 200), w=1.4, off=(-2, 0))
        cel(g, Circ(fx - 6, fy - 16, 6), (250, 220, 196), w=1.4, off=(-2, -2))
        g.fill(Ell(fx - 6, fy - 21, 7, 4), (250, 230, 120))
        g.glow(fx - 6, fy - 6, 30, (255, 240, 180), 0.25)
    # snail on a big leaf (difference) + bell flowers in the foreground
    cel(g, Poly([(30, 600), (60, 520), (150, 490), (210, 520), (170, 580), (90, 610)]), (70, 150, 90), w=2.0, off=(-12, -6))
    g.fill(Seg(60, 590, 180, 510, 2), (110, 190, 120))
    if "snail" not in d:
        sx_, sy_ = 130, 520
        cel(g, Ell(sx_, sy_ + 4, 30, 7), (220, 200, 160), w=1.6, off=(-4, -2))
        cel(g, Circ(sx_ + 4, sy_ - 12, 17), (230, 140, 80), w=1.8, off=(-5, -5))
        g.fill(Diff(Circ(sx_ + 4, sy_ - 12, 10), Circ(sx_ + 7, sy_ - 14, 6)), shade_of((230, 140, 80)))
        for e in (0, 6):
            g.fill(Seg(sx_ - 24 + e, sy_, sx_ - 30 + e, sy_ - 16, 1.4), (220, 200, 160))
            g.fill(Circ(sx_ - 30 + e, sy_ - 16, 2.4), (220, 200, 160))
    for k, x in enumerate((300, 860, 520)):
        g.fill(Seg(x, 600, x + 10, 470, 3), (70, 140, 80))
        for j in range(3):
            bx, by = x + 10 + (j - 1) * 16, 480 + j * 14
            cel(g, Inter(Ell(bx, by, 9, 11), Box(bx - 10, by - 12, bx + 10, by + 6)), (200, 170, 255), w=1.4, off=(-3, -2))
            g.glow(bx, by, 14, (220, 200, 255), 0.25)
    g.commit()


L1544_ELEMENTS = [
    sparkle_el("fireflies1", [(300, 400), (520, 300), (760, 380), (90, 380)], col=(255, 250, 150), r=5, speed=0.5),
    sparkle_el("fireflies2", [(360, 450), (680, 360), (880, 330), (40, 300)], col=(200, 255, 170), r=4, speed=0.35, phase=0.5),
    puff_el("smoke", 640, 286, r=8, rise=60, wind=-10, col=(200, 196, 230)),
    E("fairyfly", el(lambda g, m: (g.fill(Ell(500, 230, 9, 5), (220, 240, 255)), g.fill(Ell(516, 230, 9, 5), (220, 240, 255)),
                                   cel(g, Circ(508, 236, 4), (250, 200, 230), w=1.2, off=(-1, -1)), g.glow(508, 236, 18, (255, 240, 200), 0.4))),
      pivot=(508, 236), daynight="untinted", anim=dict(orbitRadius=(120, 40), orbitSpeed=0.08, stretch=(0.5, 0), scaleSpeed=4)),
    sparkle_el("stars", [(300, 40), (520, 80), (700, 30), (840, 110), (420, 140)], r=5, speed=0.6, phase=0.2),
]

L1544_DIFFS = [
    ("win1", 196, 365, 0),
    ("cap", 600, 300, 0),
    ("lantern", 470, 380, 0),
    ("fairy", 414, 352, 0),
    ("frog", 600, 522, 0),
    ("win3", 807, 374, 0),
    ("snail", 130, 506, 0),
]


LEVELS = [
    ("Level1542", "糖果小屋", l1542_bg, L1542_ELEMENTS, L1542_DIFFS, 60, OPTS),
    ("Level1543", "高塔长发", l1543_bg, L1543_ELEMENTS, L1543_DIFFS, 60, OPTS),
    ("Level1544", "蘑菇精灵村", l1544_bg, L1544_ELEMENTS, L1544_DIFFS, 60, OPTS),
]
