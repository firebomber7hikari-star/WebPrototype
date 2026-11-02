# -*- coding: utf-8 -*-
"""Cel-shaded (toon render) levels - toon.py on top of the real.py numpy painter: flat colour blocks,
one hard cool-tinted shadow tone, ink outlines, small hard highlights, gradient skies, puffy clouds:
  Level1510 港口小镇   - a hillside harbour town: colourful houses, church spire, lighthouse, boats, quay
  Level1511 风车草原   - a windmill on rolling meadows: cottage, sheep, tulip rows, apple tree, balloon
  Level1512 山谷小火车 - a little steam train crossing a stone viaduct between snowy peaks, river, station
  Level1513 阁楼卧室   - a cosy attic bedroom at dusk: round window, bed with a sleeping cat, desk lamp, shelf
  Level1514 天空浮岛   - floating islands above a sea of clouds: cottage, waterfall, tower, airship
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, C, Circ, Ctx, Diff, Ell, Moved, Poly, Seg, Under, Union, el, fbm1, lgrad, mixc, rgrad, vgrad
from toon import (INK, Grow, bird_el, cel, cloud_el, face_x, figure, hill, house, ink, peak, puff_el, shade_of,
                  sparkle_el, tint_of, toon_cloud, toon_post, toon_tree, toon_water, toon_window)

OPTS = dict(post=toon_post, anim_seconds=12.0, frames=60)


def boat(g, x, y, s, hull, sail=None, cabin=None):
    """Side-view boat: hull (+ sail or wheelhouse)."""
    cel(g, Poly([(x - 50 * s, y - 14 * s), (x + 50 * s, y - 14 * s), (x + 38 * s, y + 4 * s), (x - 40 * s, y + 4 * s)]),
        hull, w=1.8, off=(0, -6 * s))
    g.fill(Box(x - 50 * s, y - 14 * s, x + 50 * s, y - 10 * s), (250, 250, 244))
    if sail:
        g.fill(Seg(x, y - 14 * s, x, y - 100 * s, 2.4 * s), (110, 80, 60))
        cel(g, Poly([(x + 3 * s, y - 96 * s), (x + 3 * s, y - 20 * s), (x + 46 * s, y - 20 * s)]), sail, w=1.8, off=(6 * s, 0))
        cel(g, Poly([(x - 3 * s, y - 88 * s), (x - 3 * s, y - 20 * s), (x - 34 * s, y - 20 * s)]), (250, 250, 244), w=1.8, off=(4 * s, 0))
    if cabin:
        cel(g, Box(x - 6 * s, y - 40 * s, x + 26 * s, y - 14 * s, 3 * s), cabin, w=1.8, off=(-6 * s, 0))
        toon_window(g, x + 2 * s, y - 34 * s, x + 18 * s, y - 24 * s, bars=False, w=1)


# =================================================================== Level 1510 harbour town
SEA0 = 262


def l1510_town(x):
    return 440 - np.clip(x - 470, 0, 420) * 0.6


def l1510_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, SEA0 + 4), vgrad([(0, (86, 168, 244)), (SEA0, (206, 236, 255))]))
    toon_cloud(g, 560, 70, 90, 30, seed=1)
    toon_cloud(g, 330, 150, 60, 20, seed=2)
    hill(g, lambda x: 236 - 46 * fbm1(x, 140, 3, 3), (156, 200, 220), rim=0)
    hill(g, lambda x: 252 - 30 * fbm1(x, 90, 3, 4), (130, 190, 176), rim=4)
    # kite (left sky)
    kc = (240, 200, 60) if "kite" not in d else (90, 190, 110)
    kx, ky = 130, 100
    cel(g, Poly([(kx, ky - 28), (kx + 20, ky), (kx, ky + 30), (kx - 20, ky)]), kc, w=1.8, off=(8, 0))
    g.fill(Seg(kx, ky - 28, kx, ky + 30, 1.2), INK)
    g.fill(Seg(kx - 20, ky, kx + 20, ky, 1.2), INK)
    for k in range(5):
        g.fill(Seg(kx + k * 6, ky + 30 + k * 12, kx + 6 + k * 6, ky + 42 + k * 12, 1.4), INK)
        g.fill(Poly([(kx + 3 + k * 6, ky + 36 + k * 12), (kx + 9 + k * 6, ky + 32 + k * 12), (kx + 8 + k * 6, ky + 40 + k * 12)]), (230, 70, 70))
    # sea
    toon_water(g, SEA0, H + 2, (90, 186, 230), (40, 120, 200), seed=5, dashes=90)
    # headland with lighthouse
    ink(g, Under(lambda x: 268 - 34 * np.clip(1 - np.abs(x - 470) / 90, 0, 1) ** 0.6, 370, 570, 282), (120, 176, 100), 1.6)
    st = (220, 60, 60) if "stripe" not in d else (60, 110, 220)
    lx = 470
    tower = Poly([(lx - 15, 244), (lx + 15, 244), (lx + 11, 168), (lx - 11, 168)])
    cel(g, tower, (250, 250, 246), w=1.8, off=(-8, 0))
    for y0 in (180, 212):
        band = tower & Box(lx - 20, y0, lx + 20, y0 + 15)
        g.fill(band, st)
        g.fill(band & Box(lx + 4, 0, lx + 20, 300), shade_of(st))
    cel(g, Box(lx - 9, 150, lx + 9, 168, 2), (255, 236, 140), w=1.6, off=(-4, 0))
    cel(g, Poly([(lx - 14, 152), (lx, 134), (lx + 14, 152)]), (220, 60, 60), w=1.6, off=(-5, 0))
    # sailboat
    boat(g, 180, 372, 0.9, (40, 80, 150), sail=(250, 250, 244) if "sail" not in d else (250, 150, 60))
    # town on the hill
    hill(g, l1510_town, (120, 180, 90), x0=440, w=2.0, rim=6)
    rows = [
        [(620, 300, (250, 220, 170), (220, 90, 70)), (690, 258, (170, 210, 236), (230, 140, 60)), (760, 216, (250, 236, 210), (90, 140, 200))],
        [(560, 366, (250, 200, 200), (90, 140, 200)), (640, 330, (255, 236, 160), (220, 90, 70)), (720, 292, (200, 230, 190), (200, 80, 90)),
         (800, 250, (250, 214, 170), (230, 140, 60))],
        [(500, 440, (170, 210, 236), (220, 90, 70)), (585, 420, (250, 236, 210), (90, 140, 200)), (670, 394, (250, 200, 200), (230, 140, 60)),
         (755, 366, (255, 236, 160), (90, 160, 120)), (840, 340, (200, 230, 190), (220, 90, 70))],
    ]
    for row in rows:
        for x, base, wall, roof in row:
            house(g, x - 32, base, 64, 50, wall, roof, side=10, roof_h=26, door=(130, 90, 70), windows=2, w_ink=1.6)
    # window box with flowers on the house at (585, 420)
    if "flowers" not in d:
        cel(g, Box(560, 392, 610, 400, 2), (150, 100, 70), w=1.4, off=(-4, 0))
        for k in range(7):
            g.fill(Circ(563 + k * 7.4, 388 + (k % 2) * 3, 4.2), (240, 70, 110) if k % 2 else (250, 210, 60))
            g.fill(Circ(563 + k * 7.4, 388 + (k % 2) * 3, 1.6), (255, 250, 230))
    # church tower with a spire (top right)
    tx = 862
    cel(g, Box(tx - 20, 120, tx + 20, 230), (246, 236, 220), w=2.0, off=(-8, 0))
    toon_window(g, tx - 8, 150, tx + 8, 176, glass=(60, 60, 90), w=1.2)
    g.fill(Circ(tx, 134, 9), (255, 255, 250))
    g.fill(Seg(tx, 134, tx, 128, 1.4), INK)
    g.fill(Seg(tx, 134, tx + 5, 134, 1.4), INK)
    sp = (90, 160, 140) if "spire" not in d else (220, 90, 70)
    cel(g, Poly([(tx - 24, 122), (tx, 58), (tx + 24, 122)]), sp, w=2.0, off=(-10, 0))
    g.fill(Seg(tx, 58, tx, 44, 1.6), INK)
    g.fill(Seg(tx - 5, 49, tx + 5, 49, 1.6), INK)
    # quay along the bottom
    cel(g, Box(-10, 500, W + 10, 530), (214, 206, 190), w=2.0, off=(0, -6))
    g.fill(Box(-10, 530, W + 10, H + 10), (150, 140, 130))
    for row in range(4):
        for k in range(20):
            x = k * 50 + (row % 2) * 25 - 10
            ink(g, Box(x + 2, 534 + row * 18, x + 48, 548 + row * 18, 2), (176, 164, 150) if (k + row) % 3 else (160, 150, 138), 0)
    for x in (60, 240, 460, 680):
        cel(g, Box(x - 8, 486, x + 8, 506, 4), (70, 70, 80), w=1.6, off=(-4, 0))
    # lifebuoy on a post
    g.fill(Seg(330, 506, 330, 462, 4), (120, 90, 70))
    if "buoy" not in d:
        ring = Circ(330, 476, 16) - Circ(330, 476, 9)
        cel(g, ring, (240, 90, 70), w=1.6, off=(-4, -4))
        for a in (0.3, 1.9, 3.5, 5.1):
            g.fill(ring & Poly([(330, 476), (330 + 30 * math.cos(a), 476 + 30 * math.sin(a)), (330 + 30 * math.cos(a + 0.5), 476 + 30 * math.sin(a + 0.5))]),
                   (250, 250, 244))
    # crates on the quay (right)
    crates = [(812, 500, 40), (852, 500, 40), (832, 462, 38)]
    for k, (x, y, s) in enumerate(crates):
        if k == 2 and "crates" in d:
            continue
        cel(g, Box(x - s / 2, y - s, x + s / 2, y), (200, 150, 90), w=1.8, off=(-7, 0))
        g.fill(Seg(x - s / 2 + 3, y - s + 3, x + s / 2 - 3, y - 3, 2.4), (160, 110, 60))
    # fishing net heap + barrel
    cel(g, Ell(150, 498, 40, 14), (110, 150, 120), w=1.6, off=(-8, -4))
    cel(g, Box(600, 466, 628, 504, 6), (150, 100, 60), w=1.8, off=(-6, 0))
    g.fill(Box(600, 476, 628, 479), INK)
    g.fill(Box(600, 492, 628, 495), INK)
    g.commit()


def l1510_fishing(g, m):
    boat(g, 460, 452, 0.8, (220, 80, 60), cabin=(250, 246, 236))


L1510_ELEMENTS = [
    E("fishing", el(l1510_fishing), pivot=(460, 452), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.4, swingAngle=2, swingSpeed=0.4)),
    cloud_el("cloud", 720, 34, 60, 18, speed=6, seed=7),
    bird_el("gull1", 360, 80, s=8, speed=-22, col=(250, 250, 250)),
    bird_el("gull2", 300, 220, s=6, speed=18, col=(250, 250, 250)),
    sparkle_el("sparkle", [(80, 300), (300, 330), (240, 440), (120, 420)], r=6, speed=0.6),
]

L1510_DIFFS = [
    ("kite", 130, 100, 0),
    ("stripe", 470, 204, 0),
    ("spire", 862, 92, 0),
    ("sail", 200, 320, 0),
    ("flowers", 585, 392, 0),
    ("buoy", 330, 476, 0),
    ("crates", 832, 446, 0),
]


# =================================================================== Level 1511 windmill meadow
def l1511_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, 320), vgrad([(0, (100, 180, 246)), (300, (214, 240, 255))]))
    toon_cloud(g, 600, 80, 100, 32, seed=11)
    toon_cloud(g, 330, 54, 70, 22, seed=12)
    if "balloon" not in d:
        bx, by = 130, 90
        env = Union([Ell(bx, by, 30, 34), Poly([(bx - 22, by + 20), (bx + 22, by + 20), (bx + 8, by + 46), (bx - 8, by + 46)])])
        cel(g, env, (240, 90, 80), w=1.8, off=(-9, -6), hi=True, hi_off=(4, 4))
        g.fill(env & Box(bx - 40, by - 6, bx + 40, by + 6), (255, 220, 90))
        for k in (-1, 1):
            g.fill(Seg(bx + k * 7, by + 46, bx + k * 6, by + 56, 1.2), INK)
        cel(g, Box(bx - 8, by + 55, bx + 8, by + 66, 2), (170, 120, 70), w=1.4, off=(-3, 0))
    hill(g, lambda x: 262 - 40 * fbm1(x, 160, 3, 13), (150, 206, 150), rim=0)
    hill(g, lambda x: 300 - 34 * np.sin(x * 0.009 + 1) - 10 * fbm1(x, 60, 2, 14), (120, 196, 100), w=1.4, rim=6)
    for x in (60, 200, 360, 520, 700, 860):
        toon_tree(g, x, 300 - 34 * math.sin(x * 0.009 + 1) + 6, 40, col=(80, 160, 80), seed=x, w=1.2)
    hill(g, lambda x: 380 - 22 * np.sin(x * 0.006 + 2.2), (130, 210, 90), w=2.0, rim=8, tufts=120, seed=15)
    # tulip rows (lower right, perspective stripes)
    cols = [(240, 70, 90), (250, 210, 60), (240, 140, 200), (250, 120, 60)]
    for k in range(4):
        y0, y1 = 470 + k * 34, 470 + (k + 1) * 34
        g.fill(Poly([(560 - k * 30, y0), (W + 10, y0 - 10), (W + 10, y1 - 14), (530 - k * 30, y1 - 4)]), cols[k])
        g.fill(Poly([(560 - k * 30, y1 - 8), (W + 10, y1 - 22), (W + 10, y1 - 14), (530 - k * 30, y1 - 4)]), (90, 170, 70))
        g.fill(Poly([(560 - k * 30, y0), (W + 10, y0 - 10), (W + 10, y0 - 6), (560 - k * 30, y0 + 4)]), tint_of(cols[k], 0.35))
    # cottage (left)
    house(g, 60, 400, 170, 80, (250, 240, 220), (90, 120, 180), side=0, roof_h=60, door=None, windows=0, chimney=True)
    toon_window(g, 80, 340, 116, 372)
    toon_window(g, 176, 340, 212, 372)
    dc = (200, 80, 60) if "door" not in d else (80, 150, 210)
    cel(g, Box(132, 340, 162, 400, 3), dc, w=1.8, off=(-6, 0))
    g.fill(Circ(156, 372, 2.2), (250, 220, 120))
    # windmill
    mx = 620
    body = Poly([(mx - 40, 404), (mx + 40, 404), (mx + 24, 236), (mx - 24, 236)])
    cel(g, body, (246, 238, 222), w=2.2, off=(-18, 0))
    cel(g, Ell(mx, 236, 30, 18) - Box(mx - 40, 238, mx + 40, 260), (200, 80, 70), w=2.2, off=(-8, -2))
    toon_window(g, mx - 8, 280, mx + 8, 300, w=1.2)
    wd = (120, 80, 60) if "mdoor" not in d else (90, 160, 110)
    cel(g, Box(mx - 13, 366, mx + 13, 404, 12), wd, w=1.8, off=(-5, 0))
    # apple tree (right)
    ax, ab = 830, 430
    cel(g, Box(ax - 9, ab - 120, ax + 9, ab, 3), (140, 96, 60), w=2.0, off=(-6, 0))
    crown = Union([Circ(ax, 270, 64), Circ(ax - 50, 300, 42), Circ(ax + 50, 300, 42), Circ(ax - 20, 230, 40), Circ(ax + 30, 236, 40)])
    cel(g, crown, (90, 170, 70), w=2.2, off=(-16, -16), hi=True, hi_off=(6, 6))
    if "apples" not in d:
        for x, y in ((846, 230), (870, 290), (842, 272), (850, 320), (884, 252)):
            cel(g, Circ(x, y, 7), (230, 50, 50), w=1.2, off=(-3, -3), hi=(255, 200, 190), hi_off=(1.5, 1.5))
    # fence
    for x in range(250, 520, 34):
        cel(g, Box(x, 386, x + 7, 420), (250, 246, 236), w=1.4, off=(-3, 0))
    g.fill(Box(250, 394, 520, 399), (250, 246, 236))
    g.fill(Box(250, 408, 520, 413), (250, 246, 236))
    # sheep
    for k, (x, y) in enumerate(((300, 470), (420, 470), (250, 540), (380, 560))):
        wool = (250, 250, 246) if not (k == 1 and "sheep" in d) else (70, 64, 80)
        for dx in (-12, 12):
            g.fill(Box(x + dx - 2.5, y + 8, x + dx + 2.5, y + 24), INK)
        cel(g, Union([Circ(x + dx, y + dy, 13) for dx, dy in ((-14, 0), (0, -6), (14, 0), (-6, 8), (8, 8))]), wool, w=1.8, off=(-5, -5))
        cel(g, Ell(x + 26, y - 4, 9, 11), (60, 56, 70), w=1.6, off=(-3, -3))
    # dog (front right)
    if "dog" not in d:
        dx_, dy_ = 760, 548
        for lx in (-14, -6, 8, 14):
            g.fill(Box(dx_ + lx - 2.5, dy_, dx_ + lx + 2.5, dy_ + 18), INK)
        cel(g, Ell(dx_, dy_ - 2, 22, 12), (200, 140, 80), w=1.8, off=(-5, -4))
        cel(g, Circ(dx_ + 24, dy_ - 16, 11), (200, 140, 80), w=1.8, off=(-3, -3))
        g.fill(Ell(dx_ + 18, dy_ - 22, 4, 8), (130, 80, 50))
        g.fill(Circ(dx_ + 28, dy_ - 18, 1.8), INK)
        g.fill(Seg(dx_ - 22, dy_ - 6, dx_ - 32, dy_ - 18, 3), (200, 140, 80))
    g.commit()


def l1511_sails(g, m):
    cx, cy = 620, 230
    for k in range(4):
        a = k * math.pi / 2 + 0.3
        ca, sa = math.cos(a), math.sin(a)
        px, py = -sa, ca
        p = [(cx + ca * 14 + px * 2, cy + sa * 14 + py * 2), (cx + ca * 104 + px * 2, cy + sa * 104 + py * 2),
             (cx + ca * 104 + px * 24, cy + sa * 104 + py * 24), (cx + ca * 30 + px * 24, cy + sa * 30 + py * 24)]
        ink(g, Poly(p), (250, 248, 240), 1.6)
        for t in (0.35, 0.6, 0.85):
            g.fill(Seg(cx + ca * 104 * t + px * 2, cy + sa * 104 * t + py * 2, cx + ca * 104 * t + px * 24, cy + sa * 104 * t + py * 24, 1.2), (170, 150, 130))
        g.fill(Seg(cx, cy, cx + ca * 106, cy + sa * 106, 3.4), (130, 90, 60))
    cel(g, Circ(cx, cy, 9), (130, 90, 60), w=1.6, off=(-3, -3))


L1511_ELEMENTS = [
    E("sails", el(l1511_sails), pivot=(620, 230), anim=dict(rotateSpeed=-30)),
    puff_el("smoke", 210, 280, r=7, rise=50, wind=-10),
    cloud_el("cloud", 420, 150, 50, 16, speed=5, seed=16),
    bird_el("bird1", 280, 110, s=7, speed=-18),
    bird_el("bird2", 310, 126, s=6, speed=-18),
    sparkle_el("butterfly", [(480, 420), (700, 440), (200, 450)], col=(255, 230, 120), r=5, speed=0.8, daynight="tinted"),
]

L1511_DIFFS = [
    ("balloon", 130, 106, 0),
    ("door", 147, 370, 0),
    ("mdoor", 620, 385, 0),
    ("apples", 860, 270, 0),
    ("sheep", 420, 470, 0),
    ("dog", 768, 540, 0),
]


# =================================================================== Level 1512 valley train
def l1512_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, 320), vgrad([(0, (80, 160, 240)), (300, (200, 230, 252))]))
    toon_cloud(g, 420, 60, 80, 24, seed=21)
    if "glider" not in d:
        gx, gy = 800, 60
        wing = Ell(gx, gy, 40, 14) - Ell(gx, gy + 10, 42, 14)
        cel(g, wing, (250, 140, 50), w=1.6, off=(0, -4))
        for k in (-1, 1):
            g.fill(Seg(gx + k * 34, gy - 2, gx + k * 4, gy + 34, 1), INK)
        cel(g, Box(gx - 5, gy + 32, gx + 5, gy + 48, 3), (60, 90, 160), w=1.4, off=(-3, 0))
        g.fill(Circ(gx, gy + 30, 4.5), (250, 210, 176))
    peak(g, 300, 760, 520, 70, 330, (120, 140, 190), snow=(250, 252, 255), w=2.0)
    peak(g, 60, 420, 260, 110, 330, (110, 130, 176), snow=(250, 252, 255), w=2.0)
    peak(g, 600, 980, 790, 130, 330, (106, 124, 170), snow=(250, 252, 255), w=2.0)
    # mountain hut on the left peak
    if "hut" not in d:
        house(g, 182, 196, 40, 22, (180, 120, 80), (200, 70, 60), side=8, roof_h=16, windows=1, w_ink=1.4)
    hill(g, lambda x: 300 + 20 * np.sin(x * 0.012) + 10 * fbm1(x, 40, 2, 22), (110, 180, 90), w=1.8, rim=6)
    for x in range(-10, 920, 46):
        if 180 < x < 760:
            continue
        toon_tree(g, x, 340 + (x % 3) * 8, 56, col=(60, 140, 90), seed=x, w=1.4, round_=False)
    hill(g, lambda x: 420 + 20 * np.sin(x * 0.008 + 2), (120, 196, 90), w=2.0, rim=8, tufts=60, seed=23)
    # river (back to front)
    river = Poly([(430, 330), (470, 330), (680, H + 4), (240, H + 4)])
    ink(g, river, (80, 170, 230), 2.0)
    rnd = random.Random(24)
    for _ in range(50):
        y = rnd.uniform(340, 600)
        t = (y - 330) / 270
        half = 20 + 200 * t
        x = rnd.uniform(450 - half + 10, 450 + half - 30)
        g.fill(Seg(x, y, x + 6 + 26 * t, y, 1 + 2 * t), (236, 248, 255), alpha=0.8)
    # viaduct
    deck = 318
    cel(g, Box(170, deck, 770, deck + 16), (200, 180, 160), w=2.0, off=(0, -5))
    for k in range(6):
        x0 = 170 + k * 100
        pier = Diff(Box(x0, deck + 14, x0 + 100, 420), Ell(x0 + 50, 420, 38, 70))
        cel(g, pier, (196, 176, 156), w=2.0, off=(-10, 0))
    for x in range(176, 770, 12):
        g.fill(Box(x, deck - 8, x + 3, deck), INK)
    g.fill(Box(170, deck - 9, 770, deck - 6), INK)
    # train: loco (left) + 2 coaches
    lc = (60, 110, 200) if "loco" not in d else (210, 60, 60)
    lx = 470
    cel(g, Box(lx - 50, deck - 40, lx + 20, deck - 8, 6), lc, w=2.0, off=(0, -6))
    cel(g, Box(lx - 6, deck - 62, lx + 30, deck - 8, 3), lc, w=2.0, off=(-6, 0))
    toon_window(g, lx + 2, deck - 56, lx + 22, deck - 42, bars=False, w=1.2)
    cel(g, Box(lx - 40, deck - 64, lx - 26, deck - 38, 2), (60, 60, 70), w=1.6, off=(-4, 0))
    g.fill(Box(lx - 44, deck - 68, lx - 22, deck - 62, 2), INK)
    cel(g, Ell(lx - 52, deck - 24, 6, 9), (250, 230, 120), w=1.4, off=(0, 0))
    for wx in (lx - 34, lx - 10, lx + 14):
        cel(g, Circ(wx, deck - 8, 9), (60, 60, 70), w=1.6, off=(-3, -3))
    for k, col in enumerate(((230, 180, 60), (90, 170, 120))):
        x0 = lx + 36 + k * 92
        cel(g, Box(x0, deck - 52, x0 + 84, deck - 10, 5), col, w=2.0, off=(0, -6))
        for j in range(3):
            toon_window(g, x0 + 8 + j * 26, deck - 44, x0 + 24 + j * 26, deck - 30, bars=False, w=1)
        for wx in (x0 + 16, x0 + 68):
            cel(g, Circ(wx, deck - 8, 8), (60, 60, 70), w=1.6, off=(-3, -3))
    # fisherman on a rock (left bank)
    cel(g, Ell(150, 470, 50, 22), (150, 146, 140), w=2.0, off=(-12, -8))
    figure(g, 150, 462, 52, (230, 110, 60) if "fisher" not in d else (80, 170, 110), hat=(230, 200, 90))
    g.fill(Seg(162, 430, 250, 380, 2), (110, 80, 60))
    g.fill(Seg(250, 380, 262, 470, 0.8), (60, 60, 70))
    # kayak in the river
    if "kayak" not in d:
        kx, ky = 430, 560
        cel(g, Ell(kx, ky, 56, 11), (250, 210, 50), w=2.0, off=(0, -4))
        figure(g, kx, ky - 4, 36, (220, 70, 60))
        g.fill(Seg(kx - 34, ky - 30, kx + 34, ky - 4, 2.4), INK)
        for e in ((kx - 34, ky - 30), (kx + 34, ky - 4)):
            g.fill(Ell(e[0], e[1], 6, 3.5), (90, 160, 220))
    # station (right)
    sr = (200, 80, 70) if "station" not in d else (70, 150, 110)
    house(g, 720, 470, 120, 60, (250, 236, 210), sr, side=16, roof_h=34, door=(120, 80, 60), windows=2)
    cel(g, Box(700, 470, 880, 482), (190, 186, 180), w=1.8, off=(0, -4))
    g.fill(Seg(860, 470, 860, 420, 3), (90, 90, 100))
    cel(g, Circ(860, 414, 10), (250, 250, 246), w=1.6, off=(-2, -2))
    g.commit()


L1512_ELEMENTS = [
    puff_el("steam1", 437, 240, r=9, rise=60, wind=-30),
    puff_el("steam2", 437, 240, r=7, rise=60, wind=-30, phase=0.5),
    cloud_el("cloud", 640, 40, 60, 18, speed=-5, seed=25),
    bird_el("eagle", 330, 150, s=9, speed=14, col=INK),
    sparkle_el("river", [(420, 380), (470, 450), (560, 500), (330, 520)], r=5, speed=0.7),
]

L1512_DIFFS = [
    ("glider", 800, 74, 0),
    ("hut", 206, 184, 0),
    ("loco", 470, 290, 0),
    ("fisher", 150, 432, 0),
    ("kayak", 430, 548, 0),
    ("station", 790, 420, 0),
]


# =================================================================== Level 1513 attic bedroom
FLOOR = 420


def l1513_bg(c, d):
    g = Ctx(c)
    wall = (250, 226, 190)
    g.fill(Box(-2, -2, W + 2, FLOOR), wall)
    g.fill(Box(-2, -2, W + 2, FLOOR), (255, 180, 120), alpha=lambda X, Y: 0.25 * np.clip(1 - np.hypot(X - 450, Y - 150) / 420, 0, 1))
    # slanted ceilings (planks) left and right
    for poly, sh in (([(-2, -2), (260, -2), (-2, 250)], 0.86), ([(640, -2), (W + 2, -2), (W + 2, 250)], 0.78)):
        ink(g, Poly(poly), shade_of((230, 190, 140), sh), 2.0)
        for k in range(1, 9):
            t = k / 9
            if poly[0][0] < 0:
                g.fill(Seg(260 * t, -2, -2, 250 * t, 1.4), shade_of((230, 190, 140), sh * 0.85))
            else:
                g.fill(Seg(640 + 260 * t, -2, W + 2, 250 * (1 - t), 1.4), shade_of((230, 190, 140), sh * 0.85))
    for x in (300, 600):
        cel(g, Box(x - 9, -2, x + 9, FLOOR), (180, 130, 90), w=2.0, off=(-6, 0))
    # round window with dusk sky
    wx, wy, wr = 450, 150, 76
    ink(g, Circ(wx, wy, wr + 10), (190, 140, 100), 2.0)
    g.fill(Circ(wx, wy, wr), vgrad([(wy - wr, (90, 90, 180)), (wy, (240, 140, 140)), (wy + wr, (255, 210, 140))]))
    g.fill(Circ(wx, wy, wr) & Under(lambda x: wy + 40 - 20 * np.sin(x * 0.05), wx - wr, wx + wr, wy + wr), (90, 80, 130))
    if "moon" not in d:
        g.fill(Circ(wx - 28, wy - 32, 22) - Circ(wx - 18, wy - 39, 19), (255, 250, 210))
    g.fill(Circ(wx + 40, wy - 50, 2), (255, 255, 240))
    g.fill(Circ(wx + 20, wy - 20, 1.6), (255, 255, 240))
    g.fill(Box(wx - 3, wy - wr, wx + 3, wy + wr) & Circ(wx, wy, wr), (190, 140, 100))
    g.fill(Box(wx - wr, wy - 3, wx + wr, wy + 3) & Circ(wx, wy, wr), (190, 140, 100))
    # poster on the left slope
    pc = (90, 120, 200)
    cel(g, Box(76, 76, 144, 160), pc, w=2.0, off=(0, 0))
    g.fill(Box(82, 82, 138, 154), (40, 50, 110))
    if "poster" not in d:
        pts = [(110 + 22 * math.cos(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45),
                116 + 22 * math.sin(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45)) for k in range(10)]
        g.fill(Poly(pts), (255, 220, 90))
    else:
        g.fill(Circ(110, 116, 20) - Circ(118, 110, 18), (255, 220, 90))
    # hanging plant (right)
    g.fill(Seg(770, -2, 770, 150, 1.4), INK)
    pot = (220, 120, 80) if "plant" not in d else (90, 150, 210)
    for a in (-1.0, -0.4, 0.3, 0.9):
        g.fill(Seg(770, 150, 770 + 60 * math.sin(a), 150 + 60 * math.cos(a) * 0.8 + 20, 3.4, 1.4), (70, 150, 80))
        cel(g, Ell(770 + 60 * math.sin(a), 150 + 60 * math.cos(a) * 0.8 + 20, 7, 4), (90, 180, 90), w=1, off=(-2, -2))
    cel(g, Poly([(744, 150), (796, 150), (788, 186), (752, 186)]), pot, w=2.0, off=(-10, 0))
    g.fill(Box(744, 150, 796, 156), shade_of(pot))
    # floor
    g.fill(Box(-2, FLOOR, W + 2, H + 2), (190, 130, 90))
    for k in range(9):
        y = FLOOR + 4 + k * 22
        g.fill(Box(-2, y, W + 2, y + 2), (150, 100, 70))
    g.fill(Box(-2, FLOOR - 6, W + 2, FLOOR + 2), (170, 120, 84))
    cel(g, Ell(470, 560, 260, 34), (120, 170, 200), w=2.0, off=(0, -6))
    g.fill(Ell(470, 560, 220, 24) - Ell(470, 560, 206, 20), (250, 240, 220))
    # desk + lamp + mug (left)
    cel(g, Box(30, 404, 270, 420, 2), (160, 110, 70), w=2.0, off=(0, -5))
    for x in (40, 252):
        cel(g, Box(x, 418, x + 12, 530), (150, 100, 64), w=2.0, off=(-4, 0))
    cel(g, Box(50, 420, 140, 470), (170, 120, 80), w=1.8, off=(-6, 0))
    g.fill(Circ(95, 446, 3), INK)
    lamp = (250, 200, 80) if "lamp" not in d else (100, 200, 140)
    g.fill(Seg(200, 404, 186, 360, 3), (70, 70, 80))
    g.fill(Seg(186, 360, 214, 336, 3), (70, 70, 80))
    cel(g, Poly([(190, 344), (232, 316), (246, 344), (216, 360)]), lamp, w=1.8, off=(-6, 0))
    cel(g, Ell(200, 404, 16, 5), (70, 70, 80), w=1.4, off=(0, -2))
    g.add(Poly([(214, 356), (244, 342), (280, 404), (190, 404)]), (255, 230, 150), 0.25)
    for k, col in enumerate(((220, 80, 80), (90, 140, 210), (240, 200, 80))):
        cel(g, Box(60 + k * 16, 360 + k * 3, 74 + k * 16, 404), col, w=1.4, off=(-4, 0))
    cel(g, Box(130, 380, 152, 404, 4), (250, 250, 244), w=1.6, off=(-5, 0))
    g.fill(Ell(156, 390, 6, 7) - Ell(156, 390, 3, 4), INK)
    # bed (centre) with quilt and the cat
    cel(g, Box(330, 330, 620, 400, 10), (170, 110, 80), w=2.2, off=(-10, 0))
    cel(g, Box(320, 396, 630, 470, 6), (250, 250, 244), w=2.2, off=(0, -6))
    quilt = Box(330, 404, 630, 476, 6)
    cel(g, quilt, (240, 150, 150), w=2.2, off=(0, -8))
    for k in range(5):
        for j in range(2):
            if (k + j) % 2 == 0:
                g.fill(Box(334 + k * 59, 412 + j * 30, 386 + k * 59, 438 + j * 30, 3), (250, 196, 190))
    cel(g, Ell(380, 386, 40, 16), (250, 250, 244), w=1.8, off=(0, -4))
    for x in (330, 618):
        cel(g, Box(x - 4, 470, x + 10, 500), (150, 100, 64), w=1.8, off=(-4, 0))
    cat = (240, 150, 60) if "cat" not in d else (130, 130, 146)
    cx, cy = 500, 404
    cel(g, Ell(cx, cy, 36, 20), cat, w=2.0, off=(-8, -6))
    cel(g, Circ(cx - 32, cy - 6, 15), cat, w=2.0, off=(-5, -5))
    for k in (-1, 1):
        cel(g, Poly([(cx - 32 + k * 4, cy - 18), (cx - 32 + k * 13, cy - 30), (cx - 32 + k * 14, cy - 12)]), cat, w=1.6, off=(0, 0))
    for k in (-1, 1):
        g.fill(Seg(cx - 32 + k * 5 - 3, cy - 6, cx - 32 + k * 5 + 3, cy - 6, 1.6), INK)
    g.fill(Seg(cx + 30, cy + 10, cx - 10, cy + 20, 7), cat)
    # bookshelf (right) with a globe
    sx0, sx1 = 680, 860
    cel(g, Box(sx0, 260, sx1, 520), (160, 110, 70), w=2.2, off=(-10, 0))
    rnd = random.Random(31)
    for k, y in enumerate((330, 400, 470)):
        g.fill(Box(sx0 + 8, y - 62, sx1 - 8, y), (110, 74, 50))
        cel(g, Box(sx0 + 4, y, sx1 - 4, y + 8), (176, 124, 80), w=1.4, off=(0, -3))
        x = sx0 + 12
        while x < sx1 - 30:
            if k == 2 and x > 740:
                break
            bw = rnd.uniform(10, 18)
            bh = rnd.uniform(36, 56)
            col = rnd.choice([(220, 80, 80), (90, 140, 210), (240, 200, 80), (110, 180, 120), (200, 140, 220)])
            cel(g, Box(x, y - bh, x + bw, y), col, w=1.2, off=(-3, 0))
            x += bw + 2
    if "globe" not in d:
        gx, gy = 800, 440
        g.fill(Seg(gx, gy + 22, gx, gy + 30, 3), (200, 170, 60))
        cel(g, Ell(gx, gy + 30, 14, 3), (200, 170, 60), w=1.2, off=(0, -1))
        cel(g, Circ(gx, gy, 22), (90, 160, 220), w=1.8, off=(-6, -6), hi=True, hi_off=(3, 3))
        g.fill(Circ(gx, gy, 22) & Union([Ell(gx - 8, gy - 6, 9, 7), Ell(gx + 9, gy + 8, 8, 6)]), (110, 190, 100))
    g.commit()


def l1513_mobile(g, m):
    g.fill(Seg(620, -2, 620, 40, 1), INK)
    g.fill(Seg(580, 40, 660, 40, 1.6), INK)
    for x, y in ((580, 70), (660, 64)):
        g.fill(Seg(x, 40, x, y - 10, 1), INK)
        r = 9
        cel(g, Poly([(x + r * math.cos(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45),
                      y + r * math.sin(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45)) for k in range(10)]),
            (255, 220, 90), w=1.2, off=(-2, -2))


L1513_ELEMENTS = [
    E("mobile", el(l1513_mobile), pivot=(620, 0), anim=dict(swingAngle=3, swingSpeed=0.3)),
    E("lampglow", el(lambda g, m: g.glow(226, 350, 70, (255, 220, 140), 0.35)), daynight="untinted",
      anim=dict(twinkle=0.25, twinkleSpeed=0.4)),
    puff_el("steam", 141, 372, r=4, rise=36, wind=4),
    sparkle_el("stars", [(486, 96), (420, 120), (514, 140)], col=(255, 255, 230), r=4, speed=0.5),
    E("zzz", el(lambda g, m: [g.fill(Poly([(x, y), (x + s, y), (x, y + s), (x + s, y + s)]) - Poly([(x + 1.6, y + 1.6), (x + s - 2.6, y + 1.6), (x + 1.6, y + s - 1.6)]),
                                     INK) for x, y, s in ((440, 360, 8), (452, 346, 10))]), pivot=(450, 360),
      anim=dict(driftVelocity=(4, 20), driftLength=30, driftFade=True)),
]

L1513_DIFFS = [
    ("poster", 110, 118, 0),
    ("moon", 424, 112, 0),
    ("plant", 770, 168, 0),
    ("lamp", 218, 338, 0),
    ("cat", 490, 400, 0),
    ("globe", 800, 446, 0),
]


# =================================================================== Level 1514 floating islands
def island(g, x0, x1, top, depth, grass=(110, 200, 90), rock=(170, 130, 110), seed=0, w=2.0):
    """Floating island: grassy top band over a jagged rocky underside (cone)."""
    rnd = random.Random(seed)
    cx = (x0 + x1) / 2
    pts = [(x0, top)]
    n = 7
    for k in range(1, n):
        t = k / n
        x = x0 + (x1 - x0) * t
        y = top + depth * math.sin(t * math.pi) ** 0.7 * rnd.uniform(0.7, 1.0)
        pts.append((x, y))
    pts.append((x1, top))
    under = Poly([(x0, top + 6)] + pts[1:-1] + [(x1, top + 6), (x1, top), (x0, top)])
    cel(g, under, rock, w=w, off=(-(x1 - x0) * 0.1, 0))
    for k in range(4):
        y = top + 14 + k * depth * 0.18
        g.fill(under & Box(x0, y, x1, y + 3), shade_of(rock, 0.85))
    topband = Union([Ell(cx, top, (x1 - x0) / 2 + 4, 12), Box(x0 - 2, top, x1 + 2, top + 10, 4)])
    cel(g, topband, grass, w=w, off=(0, -6), hi=True, hi_off=(0, 3))


def l1514_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, H + 2), vgrad([(0, (70, 140, 236)), (420, (190, 226, 255)), (600, (230, 244, 255))]))
    g.glow(760, 70, 140, (255, 250, 220), 0.35)
    cel(g, Circ(760, 70, 26), (255, 246, 200), w=0, off=(-4, -4))
    toon_cloud(g, 260, 210, 70, 20, seed=41)
    # small floating rock with a tree (top left)
    if "rocktree" not in d:
        island(g, 112, 192, 140, 46, seed=42, w=1.8)
        toon_tree(g, 150, 136, 50, col=(90, 180, 80), seed=43, w=1.6)
    # right upper island with a tower
    island(g, 680, 860, 220, 90, seed=44)
    tc = (240, 236, 226)
    cel(g, Box(746, 132, 784, 222), tc, w=2.0, off=(-10, 0))
    roof = (90, 130, 210) if "tower" not in d else (220, 90, 70)
    cel(g, Poly([(740, 136), (765, 96), (790, 136)]), roof, w=2.0, off=(-10, 0))
    toon_window(g, 758, 150, 772, 172, w=1.2)
    # rope bridge between the islands
    for dy in (0, 10):
        g.fill(Seg(500, 300 + dy, 690, 222 + dy, 1.4), (120, 90, 60))
    for k in range(1, 12):
        t = k / 12
        x, y = 500 + 190 * t, 300 - 78 * t + 6 * math.sin(t * math.pi)
        g.fill(Box(x - 3, y, x + 3, y + 10), (170, 120, 70))
    # main island
    island(g, 110, 520, 300, 170, seed=45)
    house(g, 200, 298, 100, 54, (250, 236, 210), (200, 80, 70) if "cottage" not in d else (90, 160, 110),
          side=14, roof_h=36, door=(130, 90, 60), windows=2)
    toon_tree(g, 420, 298, 90, col=(90, 180, 80), seed=46)
    cel(g, Box(478, 302, 500, 470), (150, 210, 250), w=1.8, off=(-6, 0))     # waterfall
    for k in range(6):
        g.fill(Box(482 + (k % 3) * 5, 316 + k * 26, 484 + (k % 3) * 5, 334 + k * 26), (240, 250, 255))
    # lower right island with a flag
    island(g, 760, 900, 400, 70, seed=47)
    g.fill(Seg(830, 400, 830, 340, 2.4), (110, 80, 60))
    if "flag" not in d:
        cel(g, Poly([(832, 342), (870, 352), (832, 364)]), (240, 200, 60), w=1.6, off=(0, -4))
    toon_tree(g, 790, 398, 40, col=(90, 180, 80), seed=48, w=1.6)
    # small island with a bench (bottom left)
    if "bench" not in d:
        island(g, 60, 150, 448, 40, seed=49, w=1.8)
        cel(g, Box(80, 432, 130, 438, 2), (200, 140, 80), w=1.4, off=(0, -2))
        cel(g, Box(80, 420, 130, 427, 2), (200, 140, 80), w=1.4, off=(0, -2))
        for x in (84, 124):
            g.fill(Box(x, 436, x + 3, 448), INK)
    # hot-air balloon above the cloud sea
    bx, by = 590, 420
    env = Union([Ell(bx, by, 30, 34), Poly([(bx - 22, by + 20), (bx + 22, by + 20), (bx + 8, by + 46), (bx - 8, by + 46)])])
    bc = (250, 160, 60) if "balloon" not in d else (180, 90, 210)
    cel(g, env, bc, w=1.8, off=(-9, -6), hi=True, hi_off=(4, 4))
    for k in (-14, 0, 14):
        g.fill(env & Box(bx + k - 3, by - 40, bx + k + 3, by + 50), (250, 246, 236))
    for k in (-1, 1):
        g.fill(Seg(bx + k * 7, by + 46, bx + k * 6, by + 56, 1.2), INK)
    cel(g, Box(bx - 8, by + 55, bx + 8, by + 66, 2), (170, 120, 70), w=1.4, off=(-3, 0))
    # sea of clouds
    rnd = random.Random(50)
    for k in range(10):
        x = -40 + k * 110 + rnd.uniform(-20, 20)
        toon_cloud(g, x, 540 + rnd.uniform(-16, 10), 90, 34, seed=60 + k)
    for k in range(9):
        x = 10 + k * 110 + rnd.uniform(-20, 20)
        toon_cloud(g, x, 590, 90, 30, seed=80 + k)
    g.commit()


def l1514_airship(g, m):
    x, y = 470, 90
    env = Ell(x, y, 70, 22)
    cel(g, env, (230, 220, 200), w=2.0, off=(-10, -8), hi=True, hi_off=(4, 4))
    for k in (-40, 0, 40):
        g.fill(env & Box(x + k - 2, y - 30, x + k + 2, y + 30), (200, 180, 150))
    cel(g, Poly([(x - 72, y), (x - 92, y - 18), (x - 88, y + 16)]), (220, 90, 70), w=1.8, off=(0, -4))
    cel(g, Box(x - 22, y + 24, x + 22, y + 38, 4), (150, 100, 60), w=1.8, off=(0, -3))
    for k in (-18, 18):
        g.fill(Seg(x + k, y + 20, x + k, y + 25, 1.4), INK)


L1514_ELEMENTS = [
    E("airship", el(l1514_airship), pivot=(470, 90), anim=dict(bobAmplitude=(10, 5), bobSpeed=0.12)),
    cloud_el("cloud", 300, 34, 60, 16, speed=6, seed=51),
    bird_el("bird1", 640, 280, s=7, speed=-16),
    bird_el("bird2", 666, 296, s=6, speed=-16),
    sparkle_el("spray", [(486, 470), (500, 460), (476, 456)], r=5, speed=0.9),
]

L1514_DIFFS = [
    ("rocktree", 152, 130, 0),
    ("tower", 765, 118, 0),
    ("cottage", 250, 250, 0),
    ("flag", 850, 352, 0),
    ("bench", 105, 440, 0),
    ("balloon", 590, 430, 0),
]


LEVELS = [
    ("Level1510", "港口小镇", l1510_bg, L1510_ELEMENTS, L1510_DIFFS, 60, OPTS),
    ("Level1511", "风车草原", l1511_bg, L1511_ELEMENTS, L1511_DIFFS, 60, OPTS),
    ("Level1512", "山谷小火车", l1512_bg, L1512_ELEMENTS, L1512_DIFFS, 60, OPTS),
    ("Level1513", "阁楼卧室", l1513_bg, L1513_ELEMENTS, L1513_DIFFS, 60, OPTS),
    ("Level1514", "天空浮岛", l1514_bg, L1514_ELEMENTS, L1514_DIFFS, 60, OPTS),
]
