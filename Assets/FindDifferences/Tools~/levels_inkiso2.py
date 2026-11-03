# -*- coding: utf-8 -*-
"""Ink-sketch axonometric levels, set 2 - following the five-star favourites Level1530 / 1531: the same high-angle
camera and ballpoint-pen rendering (blue hatching by light, cross-hatched cast shadows, red-ink accents). Original scenes:
  Level1642 墨线山寺   - a mountain temple on stone terraces: hall, pagoda, stairs, bell frame, stone lanterns, pines
  Level1643 墨线城门集 - a market square inside a town gate: wall and gate tower, awning stalls, carts, well, crowd
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Union, el
from levels_inkiso import (INK, OPTS, PAPER, RED, WASH, Iso, bird_el, box, cyl, figure, hatch, ink_line, pine, rect_ring,
                           rockblock, shade_fill, shadow, shimmer_el, solid, water_fill)
from levels_inkiso import gable


def ground(g, iso, x0, y0, x1, y1, z=0.0, seed=0):
    g.fill(iso.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]), PAPER)


def hip_roof(g, iso, x0, y0, x1, y1, z0, h, seed, over=0.6, col=PAPER):
    """Pyramidal (hipped) roof over a rectangle."""
    bot = [(x0 - over, y0 - over, z0), (x1 + over, y0 - over, z0), (x1 + over, y1 + over, z0), (x0 - over, y1 + over, z0)]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    top = [(cx, cy, z0 + h)] * 4
    solid(g, iso, top, bot, seed=seed, w=1.2, side_base=col)


def flag(g, iso, x, y, z, h, col=RED, seed=0, size=30):
    a, b = iso.p(x, y, z), iso.p(x, y, z + h)
    g.fill(Seg(a[0], a[1], b[0], b[1], 1.6), INK)
    fl = Poly([(b[0] + 1, b[1]), (b[0] + size, b[1] + size * 0.22), (b[0] + 1, b[1] + size * 0.45)])
    g.fill(fl, col, alpha=0.9)
    ink_line(g, fl.p[0], fl.p[1], w=0.9, seed=seed, over=0.5, double=False)
    ink_line(g, fl.p[1], fl.p[2], w=0.9, seed=seed + 1, over=0.5, double=False)


def stone_lantern(g, iso, x, y, z, seed, top=True):
    shadow(g, iso, rect_ring(x - 0.4, y - 0.4, x + 0.4, y + 0.4), z, 2.2, seed=seed, k=0.6)
    box(g, iso, x - 0.5, y - 0.5, z, x + 0.5, y + 0.5, z + 0.3, seed=seed + 1, w=1.0)
    cyl(g, iso, x, y, z + 0.3, z + 1.2, 0.18, n=8, seed=seed + 2, w=0.9)
    box(g, iso, x - 0.4, y - 0.4, z + 1.2, x + 0.4, y + 0.4, z + 1.8, seed=seed + 3, w=1.0)
    if top:
        hip_roof(g, iso, x - 0.45, y - 0.45, x + 0.45, y + 0.45, z + 1.8, 0.6, seed + 4, over=0.25)


# =================================================================== Level 1642 mountain temple
I42 = Iso(390, 250, 19.0)


def l1642_bg(c, d):
    g = Ctx(c)
    iso = I42
    g.fill(Box(-2, -2, W + 2, H + 2), PAPER)
    # misty peaks behind (hatched silhouettes)
    for k, (x0, w, h) in enumerate(((-20, 300, 160), (220, 360, 210), (560, 380, 170))):
        shp = Poly([(x0, 280), (x0 + w * 0.45, 280 - h), (x0 + w * 0.6, 280 - h * 0.8), (x0 + w, 280)])
        shade_fill(g, shp, 0.5, 4200 + k, vertical=False, ang=70)
        ink_line(g, shp.p[0], shp.p[1], w=1.0, seed=4205 + k, double=False)
        ink_line(g, shp.p[1], shp.p[2], w=1.0, seed=4208 + k, double=False)
        ink_line(g, shp.p[2], shp.p[3], w=1.0, seed=4211 + k, double=False)
    # lower courtyard
    ground(g, iso, -14, -12, 30, 30, 0)
    for k in range(-10, 30, 3):
        a, b = iso.p(k, 14, 0), iso.p(k, 30, 0)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.6), INK, alpha=0.3)
    # back cliff rocks
    for k, (x, y, sx, sy, h) in enumerate(((-12, -10, 3, 2.5, 6), (-6, -11, 4, 2, 7), (2, -11, 3, 2, 8))):
        rockblock(g, iso, x, y, 0, sx, sy, h, seed=4220 + k)
    # upper terrace with the main hall
    shadow(g, iso, rect_ring(-8, -8, 14, 8), 0, 3, seed=4230)
    box(g, iso, -8, -8, 0, 14, 8, 3, seed=4231, w=1.4)
    shadow(g, iso, rect_ring(-4, -5, 7, 3), 3, 6.5, seed=4232, clip=iso.poly([(-8, -8, 3), (14, -8, 3), (14, 8, 3), (-8, 8, 3)]))
    gable(g, iso, -4, -5, 7, 3, 3, 3.2, 2.8, 4233, along_x=True, over=0.8)
    for wx in (-2.5, 1.0, 4.5):
        g.fill(iso.poly([(wx, 3, 3.6), (wx + 1.6, 3, 3.6), (wx + 1.6, 3, 5.8), (wx, 3, 5.8)]), (60, 70, 140))
    # pagoda (three tiers) on the right of the terrace
    px0, py0 = 9.5, -6.0
    shadow(g, iso, rect_ring(px0, py0, px0 + 3, py0 + 3), 3, 11, seed=4240, clip=iso.poly([(-8, -8, 3), (14, -8, 3), (14, 8, 3), (-8, 8, 3)]))
    z = 3.0
    for t, (inset, hh) in enumerate(((0.0, 2.6), (0.35, 2.2), (0.7, 1.9))):
        box(g, iso, px0 + inset, py0 + inset, z, px0 + 3 - inset, py0 + 3 - inset, z + hh, seed=4241 + t, w=1.1)
        box(g, iso, px0 + inset - 0.7, py0 + inset - 0.7, z + hh, px0 + 3 - inset + 0.7, py0 + 3 - inset + 0.7, z + hh + 0.35, seed=4245 + t, w=1.1,
            top_base=RED if not ("eave" in d and t == 1) else PAPER, top_dark=0.0)
        z += hh + 0.35
    tip = iso.p(px0 + 1.5, py0 + 1.5, z)
    g.fill(Seg(tip[0], tip[1], tip[0], tip[1] - 26, 2.0), INK)
    for k in range(3):
        g.fill(Ell(tip[0], tip[1] - 6 - k * 7, 4 - k, 1.6), INK)
    # stairs down from the terrace
    for k in range(6):
        zz = 3 - k * 0.5
        box(g, iso, 14 + k * 0.9, 0, 0, 14.9 + k * 0.9, 4, zz, seed=4250 + k, w=1.0)
    # bell frame (courtyard right)
    bx, by = 22, 2
    shadow(g, iso, rect_ring(bx - 1.6, by - 0.4, bx + 1.6, by + 0.4), 0, 4.5, seed=4260)
    for px in (bx - 1.5, bx + 1.5):
        box(g, iso, px - 0.2, by - 0.2, 0, px + 0.2, by + 0.2, 4.4, seed=4261 + int(px), w=1.0)
    box(g, iso, bx - 2.0, by - 0.4, 4.4, bx + 2.0, by + 0.4, 4.9, seed=4263, w=1.0)
    hip_roof(g, iso, bx - 2.0, by - 0.6, bx + 2.0, by + 0.6, 4.9, 1.0, 4264, over=0.4)
    if "bell" not in d:
        cyl(g, iso, bx, by, 2.0, 4.0, 0.9, r1=0.6, seed=4265, w=1.1)
    # stone lanterns
    for k, (x, y) in enumerate(((17, 9), (21, 12), (25, 9))):
        stone_lantern(g, iso, x, y, 0, 4270 + k * 7, top=not ("lantern" in d and k == 1))
    # water basin with a ladle
    box(g, iso, 9, 14, 0, 11.5, 16, 1.0, seed=4290, w=1.1)
    g.fill(iso.poly([(9.3, 14.3, 1.0), (11.2, 14.3, 1.0), (11.2, 15.7, 1.0), (9.3, 15.7, 1.0)]), WASH)
    if "ladle" not in d:
        a, b = iso.p(9.6, 15, 1.0), iso.p(12.4, 13.4, 2.0)
        g.fill(Seg(a[0], a[1], b[0], b[1], 2.2), INK)
        g.fill(Ell(a[0], a[1], 7, 4), INK)
    # koi pond with stepping stones in the foreground
    pond = Ell(*iso.p(-2, 26, 0), 120, 40)
    water_fill(g, pond, seed=4298)
    g.fill(Diff(pond, Ell(*iso.p(-2, 26, 0), 118, 38)), INK)
    for k, (x, y) in enumerate(((-6, 24), (-3, 26), (0, 28), (3, 30))):
        rockblock(g, iso, x, y, -0.2, 0.8, 0.6, 0.5, seed=4299 + k)
    if "koi" not in d:
        kx, ky = iso.p(1, 24.5, 0)
        g.fill(Ell(kx, ky, 10, 4), RED)
        g.fill(Poly([(kx + 9, ky), (kx + 16, ky - 4), (kx + 16, ky + 4)]), RED)
    # prayer-flag line between two poles
    p0, p1 = iso.p(4, 18, 4.5), iso.p(16, 22, 4.5)
    for pt, base_ in ((p0, iso.p(4, 18, 0)), (p1, iso.p(16, 22, 0))):
        g.fill(Seg(base_[0], base_[1], pt[0], pt[1], 1.6), INK)
    for k in range(9):
        t = (k + 0.5) / 9
        x, y = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t + 10 * math.sin(t * math.pi)
        col = RED if (k % 2 == 0 and not ("flags" in d)) else (WASH if k % 2 else (70, 120, 200))
        g.fill(Poly([(x - 6, y), (x + 6, y), (x, y + 12)]), col, alpha=0.9)
    ink_line(g, p0, (p0[0] + (p1[0] - p0[0]) * 0.5, (p0[1] + p1[1]) / 2 + 10), w=0.8, seed=4295, double=False)
    ink_line(g, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + 10), p1, w=0.8, seed=4296, double=False)
    # banner on the terrace
    flag(g, iso, -6, 6, 3, 5.5, col=RED if "banner" not in d else WASH, seed=4297, size=44)
    # pines
    for k, (x, y, z, h) in enumerate(((-11, 12, 0, 6), (27, -8, 0, 7), (6, 24, 0, 5), (28, 20, 0, 6))):
        if "pine" in d and k == 3:
            continue
        pine(g, iso, x, y, z, h, seed=4300 + k)
    # monks
    figure(g, *iso.p(18, 6, 0), 1.0, seed=4310, stick=True)
    figure(g, *iso.p(12, 18, 0), 0.9, accent=RED, seed=4311, face=-1)
    figure(g, *iso.p(2, 5, 3), 0.9, seed=4312)
    g.commit()


def _sp42(x, y, z=0.0):
    return tuple(round(v) for v in I42.p(x, y, z))


L1642_ELEMENTS = [
    bird_el("b1", 600, 50, s=8, speed=-22), bird_el("b2", 640, 66, s=6, speed=-22),
    E("incense", el(lambda g, m: [g.fill(Circ(x, y, r) - Circ(x - 1, y - 1, r - 1.4), INK, alpha=0.6) for x, y, r in
                                  ((_sp42(10.2, 15)[0], _sp42(10.2, 15)[1] - 30, 5), (_sp42(10.2, 15)[0] + 6, _sp42(10.2, 15)[1] - 42, 7))]),
      anim=dict(driftVelocity=(4, 30), driftLength=60, driftFade=True)),
]
L1642_DIFFS = [
    ("eave", *_sp42(11, -4.5, 6.2), 0),
    ("bell", *_sp42(22, 2, 3.0), 0),
    ("lantern", *_sp42(21, 12, 2.0), 0),
    ("ladle", *_sp42(10.6, 14.6, 1.3), 0),
    ("flags", _sp42(10, 20, 4.5)[0], _sp42(10, 20, 4.5)[1] + 8, 0),
    ("banner", _sp42(-6, 6, 8.5)[0] + 20, _sp42(-6, 6, 8.5)[1] + 10, 0),
    ("pine", *_sp42(28, 20, 3.0), 0),
    ("koi", *_sp42(1, 24.5, 0), 0),
]


# =================================================================== Level 1643 market inside the town gate
I43 = Iso(400, 300, 19.0)


def stall(g, iso, x0, y0, x1, y1, seed, awn=RED, goods=None):
    shadow(g, iso, rect_ring(x0, y0, x1, y1), 0, 2.4, seed=seed, k=0.6)
    box(g, iso, x0, y0, 0, x1, y1, 1.1, seed=seed + 1, w=1.1)
    for (x, y) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        a, b = iso.p(x, y, 1.1), iso.p(x, y, 2.8)
        g.fill(Seg(a[0], a[1], b[0], b[1], 1.3), INK)
    aw = [(x0 - 0.4, y0 - 0.4, 2.8), (x1 + 0.4, y0 - 0.4, 2.8), (x1 + 0.4, y1 + 0.4, 2.4), (x0 - 0.4, y1 + 0.4, 2.4)]
    g.fill(iso.poly(aw), PAPER)
    n = 6
    for k in range(n):
        if k % 2 == 0:
            xa = x0 - 0.4 + k * (x1 - x0 + 0.8) / n
            xb = xa + (x1 - x0 + 0.8) / n
            g.fill(iso.poly([(xa, y0 - 0.4, 2.8), (xb, y0 - 0.4, 2.8), (xb, y1 + 0.4, 2.4), (xa, y1 + 0.4, 2.4)]), awn, alpha=0.85)
    for i in range(4):
        ink_line(g, iso.p(*aw[i]), iso.p(*aw[(i + 1) % 4]), w=1.1, seed=seed + 2 + i)
    if goods:
        for k in range(3):
            cx_, cy_ = iso.p(x0 + 0.6 + k * (x1 - x0 - 1.2) / 2, (y0 + y1) / 2, 1.1)
            g.fill(Ell(cx_, cy_ - 2, 6, 3), goods)
            g.fill(Ell(cx_, cy_ - 2, 6, 3) - Ell(cx_, cy_ - 3, 5, 2.4), INK)


def cart(g, iso, x, y, seed, cargo=True):
    shadow(g, iso, rect_ring(x, y, x + 3, y + 1.6), 0, 1.4, seed=seed, k=0.6)
    box(g, iso, x, y, 0.6, x + 3, y + 1.6, 1.3, seed=seed + 1, w=1.1)
    for wx in (x + 0.7, x + 2.3):
        c_ = iso.p(wx, y + 1.6, 0.6)
        g.fill(Ell(c_[0], c_[1], 7, 7), PAPER)
        g.fill(Ell(c_[0], c_[1], 7, 7) - Ell(c_[0], c_[1], 5.6, 5.6), INK)
        g.fill(Seg(c_[0] - 5, c_[1], c_[0] + 5, c_[1], 0.8), INK)
    a, b = iso.p(x + 3, y + 0.8, 1.0), iso.p(x + 5, y + 0.8, 0.4)
    g.fill(Seg(a[0], a[1], b[0], b[1], 1.4), INK)
    if cargo:
        box(g, iso, x + 0.3, y + 0.2, 1.3, x + 1.5, y + 1.4, 2.2, seed=seed + 2, w=1.0)
        cyl(g, iso, x + 2.2, y + 0.8, 1.3, 2.3, 0.5, n=10, seed=seed + 3, w=0.9)


def l1643_bg(c, d):
    g = Ctx(c)
    iso = I43
    g.fill(Box(-2, -2, W + 2, H + 2), PAPER)
    ground(g, iso, -20, -12, 34, 32, 0)
    # paving joints
    for k in range(-14, 34, 3):
        a, b = iso.p(k, -6, 0), iso.p(k, 32, 0)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.6), INK, alpha=0.25)
    # town wall along the back with crenels and the gate tower
    shadow(g, iso, rect_ring(-20, -12, 34, -8), 0, 5, seed=4300)
    box(g, iso, -20, -12, 0, 6, -8, 5, seed=4301, w=1.4)
    box(g, iso, 13, -12, 0, 34, -8, 5, seed=4302, w=1.4)
    for x in np.arange(-19.5, 34, 2.0):
        if 6 <= x <= 13:
            continue
        box(g, iso, x, -8.8, 5, x + 1.0, -8, 5.8, seed=4303 + int(x * 3), w=0.9)
    box(g, iso, 6, -13, 0, 13, -7, 6.5, seed=4310, w=1.4)
    gable(g, iso, 5.5, -13.5, 13.5, -6.5, 6.5, 0.0, 2.6, 4311, along_x=True, over=0.6)
    g.fill(iso.poly([(7.5, -7, 0), (11.5, -7, 0), (11.5, -7, 3.8), (9.5, -7, 4.8), (7.5, -7, 3.8)]), (40, 50, 110))
    for k in range(5):
        a, b = iso.p(7.8 + k * 0.85, -7, 0.2), iso.p(7.8 + k * 0.85, -7, 4.0)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.9), PAPER, alpha=0.6 if "portcullis" not in d else 0.0)
    flag(g, iso, 0, -10, 5, 2.6, col=RED if "flag" not in d else WASH, seed=4312, size=40)
    # banners hung on the wall
    for k, x in enumerate((-12, 20, 28)):
        a = iso.p(x, -8, 4.6)
        col = RED if not ("banner" in d and k == 1) else WASH
        bn = Poly([(a[0] - 8, a[1]), (a[0] + 8, a[1] + 5), (a[0] + 8, a[1] + 40), (a[0], a[1] + 34), (a[0] - 8, a[1] + 36)])
        g.fill(bn, col, alpha=0.85)
        for i in range(5):
            ink_line(g, bn.p[i], bn.p[(i + 1) % 5], w=0.9, seed=4320 + k * 6 + i, over=0.5, double=False)
    # market stalls
    stall(g, iso, -14, 0, -8, 3, 4330, goods=(240, 200, 120))
    stall(g, iso, -4, 4, 2, 7, 4340, awn=RED if "awning" not in d else (70, 120, 200), goods=(200, 230, 160))
    stall(g, iso, 18, 2, 24, 5, 4350, goods=(240, 170, 170))
    stall(g, iso, 24, 12, 30, 15, 4360)
    stall(g, iso, 0, 24, 6, 27, 4365, goods=(250, 210, 120) if "fruit" not in d else (150, 210, 250))
    # well in the middle of the square
    shadow(g, iso, rect_ring(8, 10, 11, 13), 0, 3.6, seed=4370)
    cyl(g, iso, 9.5, 11.5, 0, 1.2, 1.4, seed=4371, w=1.2)
    g.fill(Ell(*iso.p(9.5, 11.5, 1.2), 18, 9), WASH)
    for px in (8.3, 10.7):
        a, b = iso.p(px, 11.5, 1.2), iso.p(px, 11.5, 3.6)
        g.fill(Seg(a[0], a[1], b[0], b[1], 1.4), INK)
    if "roof" not in d:
        gable(g, iso, 7.8, 10.6, 11.2, 12.4, 3.6, 0.0, 1.2, 4372, along_x=True, over=0.3)
    # carts, barrels, trees
    cart(g, iso, -10, 14, 4380, cargo="cargo" not in d)
    cart(g, iso, 14, 20, 4385)
    for k, (x, y) in enumerate(((3, 18), (4.3, 18.4), (3.5, 19.6))):
        if "barrel" in d and k == 2:
            continue
        shadow(g, iso, rect_ring(x - 0.5, y - 0.5, x + 0.5, y + 0.5), 0, 1.4, seed=4390 + k)
        cyl(g, iso, x, y, 0, 1.4, 0.55, seed=4393 + k, w=1.0)
    for k, (x, y, h) in enumerate(((-16, 22, 6), (30, 26, 5.5), (-6, -4, 5))):
        if "tree" in d and k == 0:
            continue
        pine(g, iso, x, y, 0, h, seed=4400 + k)
    # crowd
    for k, (x, y, acc) in enumerate(((-6, 9, None), (-1, 11, RED), (5, 6, None), (13, 9, None), (16, 14, RED), (21, 9, None), (8, 22, None), (-12, 6, None),
                                      (12, 28, None), (-4, 22, RED))):
        acc_ = acc if not ("hat" in d and k == 4) else (70, 120, 200)
        figure(g, *iso.p(x, y, 0), 0.95, accent=acc_, seed=4410 + k, face=1 if k % 2 else -1, pack=WASH if k == 5 else None)
    g.commit()


def _sp43(x, y, z=0.0):
    return tuple(round(v) for v in I43.p(x, y, z))


L1643_ELEMENTS = [
    bird_el("b1", 200, 60, s=8, speed=22), bird_el("b2", 240, 80, s=6, speed=22),
    E("smoke", el(lambda g, m: [g.fill(Circ(x, y, r) - Circ(x - 1, y - 1, r - 1.4), INK, alpha=0.6) for x, y, r in ((700, 120, 6), (710, 106, 8))]),
      anim=dict(driftVelocity=(6, 30), driftLength=60, driftFade=True)),
]
L1643_DIFFS = [
    ("portcullis", *_sp43(9.5, -7, 2.2), 0),
    ("flag", _sp43(0, -10, 7.6)[0] + 20, _sp43(0, -10, 7.6)[1] + 8, 0),
    ("banner", _sp43(20, -8, 4.6)[0], _sp43(20, -8, 4.6)[1] + 20, 0),
    ("awning", *_sp43(-1, 5.5, 2.6), 0),
    ("roof", *_sp43(9.5, 11.5, 4.2), 0),
    ("cargo", *_sp43(-8.8, 14.8, 1.8), 0),
    ("barrel", *_sp43(3.5, 19.6, 0.7), 0),
    ("tree", *_sp43(-16, 22, 3), 0),
    ("hat", _sp43(16, 14)[0], _sp43(16, 14)[1] - 28, 0),
    ("fruit", *_sp43(3, 25.5, 1.3), 0),
]


LEVELS = [
    ("Level1642", "墨线山寺", l1642_bg, L1642_ELEMENTS, L1642_DIFFS, 60, OPTS),
    ("Level1643", "墨线城门集", l1643_bg, L1643_ELEMENTS, L1643_DIFFS, 60, OPTS),
]
