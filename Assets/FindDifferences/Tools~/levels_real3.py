# -*- coding: utf-8 -*-
"""Realistic-style levels, third set (real.py + real_kit.py; god rays / reflections where the subject asks for it):
  Level1520 薰衣草庄园 - lavender rows converging to a stone farmhouse at sunset, cypresses, beehives, bicycle
  Level1521 水城运河   - a canal of a water city: colourful facades mirrored in green water, boats, mooring poles
  Level1522 珊瑚礁     - a coral reef under sun shafts from the surface: corals, anemone, fish, clam, starfish
  Level1523 冰川峡湾   - a fjord: steep cliffs, glacier, waterfall, red boathouse, kayak, mirrored water
  Level1524 梯田晨雾   - rice terraces at dawn: water mirrors on curved terraces, mist, farmhouses, egrets
  Level1525 沙漠绿洲   - a desert oasis: sculpted dunes, palms around a pool, tents, camels, pottery
  Level1526 森林瀑布   - a mossy forest waterfall with sun shafts through the canopy, ferns, pool, log bridge
  Level1527 渔港清晨   - a fishing harbour at dawn: boats mirrored in the calm water, pier, nets, crates, gulls
  Level1528 乡村厨房   - a rustic kitchen in morning window light: bread, vegetables, copper pots, hearth, cat
  Level1529 葡萄园秋收 - an autumn vineyard at golden hour: vine rows on hills, villa, crates of grapes, barrel

Water scenes paint the upper picture twice (unmodified -> snapshot -> with differences) so reflections never
double a difference; god-ray scenes use levels_real2.make_bg for the same reason.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (F32, Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el,
                  fbm, fbm1, grain_tex, hgrad, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint,
                  tex, vgrad)
from real_kit import (bird_el, blades, bricks, broadleaf, cloud_el, cloud_layer, crown, cumulus, fall_el, figure,
                      gable_house, glint_el, grass_field, mist_el, pine, planks, ridge, ripples_light, rock, rock_face,
                      sky, smoke_el, stars, stone_wall, sun, treeline, trunk, water, window_glass)
from levels_real import palm
from levels_real2 import arch, ashlar, beam_el, fog_band, make_bg, motes_el, persp_floor, rim, stains, twigs

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)


def two_pass(upper, lower, bloom=(215, 16, 0.35), grade=None):
    """Background for water scenes: upper part painted unmodified -> snapshot 's' -> again with d; then lower."""
    def bg(c, d):
        g = Ctx(c)
        if d:
            upper(g, set())
            g.snapshot("s")
        upper(g, d)
        if not d:
            g.snapshot("s")
        lower(g, d)
        if bloom:
            g.bloom(*bloom)
        g.grade(**(grade or dict(contrast=1.05, sat=1.05)))
        g.commit()
    return bg


def flat_bg(scene, bloom=(215, 16, 0.35), grade=None):
    def bg(c, d):
        g = Ctx(c)
        scene(g, d)
        if bloom:
            g.bloom(*bloom)
        g.grade(**(grade or dict(contrast=1.05, sat=1.05)))
        g.commit()
    return bg


def cypress(g, x, base, h, col=(40, 66, 40), seed=0, light=(1.3, 0.55)):
    w = h * 0.13
    shape = Rough(Union([Ell(x, base - h * 0.45, w, h * 0.5), Poly([(x - w * 0.6, base - h * 0.75), (x, base - h), (x + w * 0.6, base - h * 0.75)])]),
                  w * 0.14, w * 0.3, seed, 3)
    g.mul(Ell(x + w * 1.5, base, w * 2.2, 4), 0.4, feather=4)
    g.fill(shape, lambda X, Y: C(col) * ((light[0] + (light[1] - light[0]) * np.clip((X - x + w) / (2 * w), 0, 1))
                                         * (0.7 + 0.55 * fbm(X, Y, w * 0.4, w * 0.35, 4, seed + 1)))[..., None])


def fish(g, x, y, L, col, stripe=None, face=1, fin=None, stripe_n=2):
    """Side-view reef fish, lit from above; face = +1 right / -1 left."""
    hh = L * 0.36
    fin = fin or mixc(col, (0, 0, 0), 0.2)
    g.fill(Poly([(x - face * L * 0.42, y), (x - face * L * 0.68, y - hh * 0.75), (x - face * L * 0.62, y), (x - face * L * 0.68, y + hh * 0.75)]),
           light_y(fin, y - hh, y + hh, 1.2, 0.7))
    g.fill(Poly([(x - face * L * 0.1, y - hh * 0.8), (x + face * L * 0.12, y - hh * 1.25), (x + face * L * 0.2, y - hh * 0.7)]), fin)
    body = Ell(x, y, L * 0.48, hh)
    g.fill(body, sphere_paint(x, y - hh * 0.4, L * 0.5, col, ry=hh * 1.2, light=(0.0, -0.8, 0.6), amb=0.45, spec=0.35))
    if stripe is not None:
        for k in range(stripe_n):
            sx = x + face * L * (0.18 - k * 0.3)
            g.fill(Inter(body, Box(sx - L * 0.05, y - hh - 2, sx + L * 0.05, y + hh + 2)), stripe)
    g.fill(Circ(x + face * L * 0.3, y - hh * 0.15, L * 0.06), (250, 250, 250))
    g.fill(Circ(x + face * L * 0.31, y - hh * 0.15, L * 0.035), (10, 10, 14))


def hot_air_balloon(g, x, y, r, cols):
    env = Union([Ell(x, y, r, r * 1.08), Poly([(x - r * 0.86, y + r * 0.45), (x + r * 0.86, y + r * 0.45), (x + r * 0.24, y + r * 1.45), (x - r * 0.24, y + r * 1.45)])])
    n = len(cols)
    for i in range(n * 2):
        x0 = x - r + i * r / n
        g.fill(Inter(env, Box(x0, y - r * 1.2, x0 + r / n, y + r * 1.5)), sphere_paint(x - r * 0.3, y - r * 0.3, r * 1.1, cols[i % n], ry=r * 1.3, amb=0.45, spec=0.2))
    for sx in (-1, 1):
        g.fill(Seg(x + sx * r * 0.24, y + r * 1.45, x + sx * r * 0.14, y + r * 1.75, 0.8), (60, 50, 40))
    g.fill(Box(x - r * 0.16, y + r * 1.75, x + r * 0.16, y + r * 2.0, 1), (130, 90, 50))


def bicycle(g, x, base, s=1.0, col=(40, 110, 140), basket=True):
    r = 24 * s
    for wx in (x - 36 * s, x + 36 * s):
        g.fill(Circ(wx, base - r, r) - Circ(wx, base - r, r - 3 * s), (34, 32, 32))
        for a in range(0, 180, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            g.fill(Seg(wx - ca * (r - 3), base - r - sa * (r - 3), wx + ca * (r - 3), base - r + sa * (r - 3), 0.7), (160, 160, 160))
    p = dict(rear=(x - 36 * s, base - r), crank=(x - 4 * s, base - r), seat=(x - 14 * s, base - r - 34 * s),
             head=(x + 26 * s, base - r - 32 * s), front=(x + 36 * s, base - r))
    for a, b in (("rear", "crank"), ("crank", "seat"), ("rear", "seat"), ("crank", "head"), ("seat", "head"), ("head", "front")):
        g.fill(Seg(*p[a], *p[b], 3.4 * s), light_y(col, p["head"][1], base, 1.3, 0.8))
    g.fill(Ell(x - 16 * s, base - r - 38 * s, 9 * s, 3 * s), (50, 36, 30))
    g.fill(Seg(x + 26 * s, base - r - 32 * s, x + 22 * s, base - r - 42 * s, 2.4 * s), (40, 40, 40))
    g.fill(Seg(x + 14 * s, base - r - 44 * s, x + 30 * s, base - r - 42 * s, 2.4 * s), (40, 40, 40))
    if basket:
        bx, by = x + 40 * s, base - r - 40 * s
        for k in range(14):
            a = -1.2 + k * 0.18
            g.fill(Seg(bx + math.cos(a) * 6 * s, by - 2 * s, bx + math.cos(a) * 14 * s, by - 24 * s - (k % 3) * 3 * s, 1.6 * s), (80, 110, 60))
            g.fill(Ell(bx + math.cos(a) * 14 * s, by - 26 * s - (k % 3) * 3 * s, 2.2 * s, 5 * s), (140, 100, 190))
        g.fill(Poly([(bx - 13 * s, by - 6 * s), (bx + 13 * s, by - 6 * s), (bx + 10 * s, by + 12 * s), (bx - 10 * s, by + 12 * s)]),
               lambda X, Y: C((180, 140, 80)) * (0.75 + 0.3 * np.abs(np.sin(X * 1.4 / s) * np.sin(Y * 1.4 / s)))[..., None])


# =================================================================== Level 1520 lavender farm at sunset
HZ20 = 272
VP20 = 560


def l1520_field(X, Y):
    dd = np.maximum(Y - HZ20, 4)
    xg = (X - VP20) / dd
    fr = (xg / 0.22) % 1.0
    ridge_ = 1 - np.abs(fr - 0.5) * 2
    n = fbm(X, Y, 1.0 + dd * 0.02, 1.0 + dd * 0.015, 3, 2010)
    lav = smooth(0.32, 0.5, ridge_ + (n - 0.5) * 0.3)
    side = np.clip((fr - 0.5) * 2, -1, 1)
    flower = C((128, 86, 170)) * (0.7 + 0.6 * n)[..., None] * (1 + 0.25 * side)[..., None]
    flower = flower + C((255, 170, 110)) * (0.25 * smooth(0.6, 1.0, ridge_) * smooth(0.3, 0.7, n))[..., None]
    soil = C((86, 90, 50)) * (0.6 + 0.5 * fbm(X, Y, 2 + dd * 0.03, 2, 3, 2011))[..., None]
    out = soil + (flower - soil) * lav[..., None]
    haze = np.clip(1 - (dd - 4) / 150, 0, 1) ** 1.4
    far = smooth(40, 12, dd)
    out = out + (C((150, 110, 160)) - out) * far[..., None]
    return out + (C((236, 170, 150)) - out) * (haze * 0.7)[..., None]


def l1520_scene(g, d):
    sky(g, [(0, (70, 86, 146)), (110, (150, 136, 170)), (210, (240, 166, 128)), (HZ20, (255, 204, 146))])
    sun(g, 700, 258, r=19, col=(255, 238, 196), halo=(255, 168, 100), k=1.1)
    cloud_layer(g, 50, 200, (255, 188, 150), (140, 106, 140), cover=0.35, sx=230, sy=18, seed=2001, alpha=0.8)
    if "balloon" not in d:
        hot_air_balloon(g, 600, 104, 20, [(220, 60, 50), (250, 200, 70)])
    ridge(g, HZ20 + 6, 60, 260, 2002, (140, 116, 146), ridged=False, haze=((244, 180, 150), 0.6, 0.45), rock_tex=0.06)
    ridge(g, HZ20 + 14, 36, 170, 2003, (100, 96, 104), ridged=False, haze=((226, 164, 140), 0.45, 0.3), rock_tex=0.06)
    treeline(g, HZ20 + 20, 16, 8, 2004, (66, 72, 50), conifer=False, haze=((214, 160, 130), 0.4, 0.25))
    g.fill(Box(-2, HZ20 + 18, W + 2, H + 2), l1520_field)
    # farmhouse (stone, terracotta roof) with shutters
    sw = light_x(stone_wall((206, 170, 128), 2005, 10, 7), 120, 300, 1.15, 0.85)
    gable_house(g, 120, 318, 170, 66, 44, (206, 170, 128), (186, 92, 60), seed=2006, side=(150, 116, 86), side_w=40,
                wall_paint=sw)
    shc = (70, 110, 150) if "shutters" not in d else (80, 140, 80)
    for wx in (140, 190, 240):
        window_glass(g, wx, 270, wx + 18, 292, lit=(255, 190, 110) if wx == 190 else None, sky_top=(250, 190, 150), sky_bot=(120, 90, 90), frame=(230, 220, 200))
        for sx in ((wx - 10, wx - 2), (wx + 20, wx + 28)):
            g.fill(Box(sx[0], 268, sx[1], 294, 1), lambda X, Y, sc=shc: C(sc) * (0.8 + 0.25 * np.abs(np.sin(Y * 1.2)))[..., None])
    g.fill(Box(272, 280, 290, 318, 1), planks("v", (120, 80, 50), seed=2007, width=6))
    g.fill(Box(250, 226, 262, 248), light_x((150, 120, 96), 250, 262))
    # cypresses + an oak
    for k, (x, h) in enumerate(((350, 118), (376, 140), (402, 112))):
        if k == 2 and "cypress" in d:
            continue
        cypress(g, x, 322, h, seed=2008 + k)
    broadleaf(g, 840, 324, 130, col=(70, 90, 42), seed=2012)
    # beehives at the field edge (left)
    for k, x in enumerate((30, 70, 110)):
        if k == 1 and "hive" in d:
            continue
        hc = ((236, 226, 200), (150, 190, 210), (236, 200, 120))[k]
        g.mul(Ell(x + 18, 362, 22, 4), 0.45, feather=4)
        g.fill(Box(x, 330, x + 30, 360, 1), light_x(hc, x, x + 30, 1.2, 0.75))
        g.fill(Box(x - 2, 326, x + 32, 332, 1), light_y((150, 120, 90), 326, 332, 1.2, 0.8))
        g.fill(Box(x + 3, 354, x + 27, 357), (40, 30, 24))
    # bicycle among the rows (difference: basket of lavender)
    bicycle(g, 470, 540, s=1.1, col=(40, 110, 140), basket="basket" not in d)
    g.mul(Ell(474, 542, 60, 5), 0.35, feather=5)
    # wooden post with a straw hat (difference)
    g.fill(Box(242, 470, 252, 560), tex(light_x((120, 90, 60), 242, 252, 1.3, 0.6), 0.2, 1.5, 6))
    if "hat" not in d:
        g.fill(Ell(247, 466, 26, 6), sphere_paint(240, 464, 26, (230, 196, 120), ry=6, amb=0.5))
        g.fill(Ell(247, 456, 13, 12) - Box(230, 464, 264, 480), sphere_paint(242, 452, 13, (226, 190, 116), ry=12, amb=0.5))
        g.fill(Box(234, 458, 260, 462), (150, 40, 40))
    # cart with lavender bundles (difference: cart colour)
    cc = (60, 90, 140) if "cart" not in d else (170, 60, 50)
    g.mul(Ell(780, 560, 90, 8), 0.45, feather=8)
    g.fill(Poly([(700, 490), (860, 490), (850, 530), (710, 530)]), planks("h", cc, seed=2013, width=10, x_or_y0=490))
    for k in range(8):
        bx = 712 + k * 18
        g.fill(Seg(bx, 492, bx + 8, 450, 8, 4), lambda X, Y: C((130, 90, 176)) * (0.6 + 0.6 * fbm(X, Y, 2, 2, 2, 2014 + k))[..., None])
        g.fill(Seg(bx, 492, bx - 6, 508, 4), (90, 120, 60))
    for wx in (730, 830):
        g.fill(Circ(wx, 540, 22) - Circ(wx, 540, 17), light_x((90, 64, 40), wx - 22, wx + 22, 1.3, 0.6))
        for a in range(0, 180, 45):
            g.fill(Seg(wx - 18 * math.cos(math.radians(a)), 540 - 18 * math.sin(math.radians(a)),
                       wx + 18 * math.cos(math.radians(a)), 540 + 18 * math.sin(math.radians(a)), 2.4), (90, 64, 40))
    g.fill(Seg(700, 512, 640, 540, 4), (100, 72, 46))
    # foreground lavender stalks
    rnd = random.Random(2015)
    for _ in range(260):
        x, y = rnd.uniform(-10, W + 10), rnd.uniform(560, 610)
        hh = rnd.uniform(24, 50)
        lean = rnd.uniform(-6, 6)
        g.fill(Seg(x, y, x + lean, y - hh, 1.6, 0.8), (80, 104, 60))
        g.fill(Ell(x + lean, y - hh - 6, 3, 9), lambda X, Y: C((128, 84, 172)) * (0.6 + 0.6 * fbm(X, Y, 1.2, 1.6, 2, 2016))[..., None])
    g.add(Box(-2, HZ20, W + 2, H), (255, 160, 90), 0.06)


L1520_ELEMENTS = [
    cloud_el("cloud", 300, 150, 90, 16, col=(255, 196, 160), shade=(170, 120, 140), speed=4, alpha=0.6, seed=2020),
    bird_el("bird1", 480, 70, s=6, speed=22, col=(70, 50, 60)),
    bird_el("bird2", 510, 84, s=5, speed=22, col=(70, 50, 60)),
    smoke_el("smoke", 256, 220, r=6, col=(220, 200, 196), rise=50, wind=10, alpha=0.4),
    glint_el("bees", [(140, 420), (360, 470), (620, 430), (900, 470)], col=(255, 220, 120), r=3, speed=0.9),
]

L1520_DIFFS = [
    ("shutters", 184, 282, 0),
    ("cypress", 402, 262, 0),
    ("balloon", 600, 112, 0),
    ("hive", 85, 345, 0),
    ("basket", 514, 470, 0),
    ("hat", 247, 462, 0),
    ("cart", 780, 510, 0),
]


# =================================================================== Level 1521 water city canal
WL21 = 352
HOUSES21 = [(-10, 150, 92, (214, 160, 96)), (140, 140, 70, (196, 96, 72)), (280, 150, 110, (232, 196, 160)),
            (430, 150, 82, (204, 132, 110)), (580, 150, 62, (226, 184, 110)), (730, 180, 96, (180, 110, 96))]


def l1521_upper(g, d):
    sky(g, [(0, (110, 160, 214)), (120, (190, 214, 232))], y1=WL21)
    cumulus(g, 300, 40, 160, 30, seed=2101, alpha=0.8)
    for i, (x0, w, top, col) in enumerate(HOUSES21):
        x1 = x0 + w
        g.fill(Box(x0, top, x1, WL21), tex(light_x(col, x0, x1, 1.12, 0.82), 0.1, 14, 10, 4, 2102 + i))
        g.mul(Box(x0, top, x1, WL21), 0.18, alpha=lambda X, Y: smooth(0.5, 0.8, fbm(X, Y, 50, 70, 3, 2110 + i)))
        g.fill(Box(x0 - 3, top - 8, x1 + 3, top, 1), light_y((150, 80, 60), top - 8, top, 1.2, 0.8))
        g.mul(Box(x0, WL21 - 26, x1, WL21), 0.4, alpha=lambda X, Y: smooth(WL21 - 26, WL21, Y))
        g.fill(Box(x0 + w * 0.7, top - 30, x0 + w * 0.7 + 10, top - 8), light_x((170, 90, 70), x0 + w * 0.7, x0 + w * 0.7 + 10))
        g.fill(Poly([(x0 + w * 0.7 - 4, top - 30), (x0 + w * 0.7 + 14, top - 30), (x0 + w * 0.7 + 10, top - 40), (x0 + w * 0.7, top - 40)]), (150, 70, 56))
        floors = [y for y in range(int(top) + 24, WL21 - 70, 66)]
        n = max(2, int(w / 46))
        for fy in floors:
            for k in range(n):
                wx = x0 + (k + 0.5) * w / n
                g.fill(arch(wx - 8, wx + 8, fy + 8, fy + 34, pointed=(i % 2 == 0)), lgrad(wx, fy, wx, fy + 34, [(0, (60, 50, 50)), (1, (30, 26, 28))]))
                g.fill(Box(wx - 11, fy + 34, wx + 11, fy + 37), (230, 220, 200))
                shc = (60, 100, 70)
                if i == 1 and fy == floors[0] and "shutters" in d:
                    shc = (150, 60, 50)
                for sx in (-1, 1):
                    g.fill(Box(wx + sx * 9 - (6 if sx < 0 else 0), fy + 2, wx + sx * 9 + (6 if sx > 0 else 0), fy + 34, 1),
                           lambda X, Y, s=shc: C(s) * (0.75 + 0.3 * np.abs(np.sin(Y * 1.3)))[..., None])
        # water-level door
        dx = x0 + w * 0.5
        g.fill(arch(dx - 14, dx + 14, WL21 - 40, WL21, pointed=False), (34, 30, 30))
    # flower boxes on house 5 (difference: colour)
    fc = (220, 40, 60) if "flowers" not in d else (250, 220, 60)
    fy = 62 + 24 + 34
    for k in range(3):
        wx = 580 + (k + 0.5) * 150 / 3
        g.fill(Box(wx - 13, fy + 2, wx + 13, fy + 10, 1), (120, 70, 44))
        for j in range(6):
            g.fill(Circ(wx - 11 + j * 4.4, fy - 1 + (j % 2) * 2, 3.2), sphere_paint(wx - 12 + j * 4.4, fy - 2, 3.2, fc, amb=0.5))
        g.fill(Ell(wx, fy + 12, 10, 4), (60, 110, 50))
    # laundry line between house 3 and 4 windows (difference)
    if "laundry" not in d:
        g.fill(Seg(350, 160, 486, 168, 0.9), (60, 60, 60))
        for k, (lx, cl) in enumerate(((372, (240, 240, 236)), (402, (70, 120, 190)), (436, (230, 90, 70)), (462, (240, 220, 120)))):
            yy = 161 + (lx - 350) * 0.06
            g.fill(Poly([(lx - 9, yy), (lx + 9, yy), (lx + 10, yy + 22 - k * 2), (lx - 8, yy + 24 - k * 2)]), light_x(cl, lx - 9, lx + 9, 1.1, 0.8))
    # quay with lamp (left)
    g.fill(Box(-2, WL21 - 14, 300, WL21), light_y((180, 170, 156), WL21 - 14, WL21, 1.2, 0.7))
    if "lamp" not in d:
        g.fill(Box(226, 246, 230, WL21 - 14), (40, 40, 40))
        g.fill(Poly([(220, 230), (236, 230), (238, 248), (218, 248)]), (240, 230, 190))
        g.fill(Poly([(216, 230), (228, 220), (240, 230)]), (40, 40, 40))
    figure(g, 120, WL21 - 14, 52, (60, 80, 120), face_right=True, hat=None)


def l1521_lower(g, d):
    water(g, WL21, H, (70, 110, 96), (30, 60, 56), seed=2120, streak=0.1)
    g.reflect(WL21, WL21, H, k=0.7, tint=(30, 70, 60), tint_k=0.3, ripple=4.0, rsx=120, rsy=2.4, fade=0.5, streak=0.3)
    ripples_light(g, WL21 + 4, H, (255, 250, 230), k=0.25, seed=2121)
    # mooring poles (difference: stripe colour) with their reflections
    pc = (200, 50, 46) if "poles" not in d else (50, 90, 170)
    for x in (600, 632, 664):
        pc_ = pc if x == 632 else (200, 50, 46)
        g.fill(Box(x - 4, 270, x + 4, WL21 + 30), cyl_paint(x, 4, (236, 232, 222), amb=0.5, spec=0.2))
        for y in range(272, WL21 + 30, 22):
            g.fill(Box(x - 4, y, x + 4, y + 11), cyl_paint(x, 4, pc_, amb=0.5, spec=0.2))
        g.fill(Box(x - 4, WL21 + 30, x + 4, WL21 + 110), (110, 120, 112), alpha=lambda X, Y: 0.55 * smooth(WL21 + 110, WL21 + 30, Y))
        for y in range(WL21 + 38, WL21 + 110, 22):
            g.fill(Box(x - 4, y, x + 4, y + 11), mixc(pc_, (30, 60, 56), 0.45), alpha=lambda X, Y: 0.6 * smooth(WL21 + 110, WL21 + 30, Y))
        g.fill(Ell(x, WL21 + 30, 8, 2), (220, 230, 220), alpha=0.5)
    # small motor boat (left) with a tarp (difference)
    tc = (50, 100, 170) if "tarp" not in d else (200, 160, 60)
    g.mul(Ell(130, 438, 110, 8), 0.4, feather=8)
    g.fill(Poly([(30, 410), (240, 410), (220, 436), (50, 436)]), light_y((236, 232, 222), 410, 436, 1.15, 0.7))
    g.fill(Box(30, 406, 240, 412, 2), (110, 70, 44))
    g.fill(Rough(Ell(110, 404, 64, 16) - Box(40, 404, 180, 430), 2, 8, 2122), light_y(tc, 388, 404, 1.2, 0.8))
    # black canal boat in the foreground with a cushion (difference)
    g.mul(Ell(500, 520, 230, 14), 0.45, feather=10)
    hull = Poly([(270, 470), (300, 496), (700, 500), (740, 474), (760, 430), (746, 470), (700, 486), (310, 482)])
    g.fill(hull, light_y((30, 28, 32), 430, 500, 1.6, 0.8))
    g.add(Seg(310, 483, 700, 487, 1.6), (255, 255, 255), 0.25)
    g.fill(Seg(740, 474, 770, 420, 5, 3), (60, 56, 50))
    g.fill(Poly([(762, 416), (780, 420), (776, 436), (764, 434)]), (200, 190, 150))
    cu = (170, 30, 40) if "cushion" not in d else (40, 120, 90)
    g.fill(Box(440, 466, 520, 482, 4), sphere_paint(470, 470, 50, cu, ry=14, amb=0.45, spec=0.2))
    g.fill(Box(436, 460, 444, 484, 2), (200, 170, 90))
    g.fill(Box(516, 460, 524, 484, 2), (200, 170, 90))
    figure(g, 640, 482, 70, (240, 240, 236), pants=(30, 30, 36), hat=(220, 200, 150))
    g.fill(Seg(620, 400, 680, 560, 3), (110, 80, 50))


L1521_ELEMENTS = [
    bird_el("pigeon1", 520, 50, s=6, speed=-26, col=(90, 90, 100)),
    glint_el("glint", [(200, 470), (380, 560), (560, 420), (820, 520)], r=4, speed=0.5),
    mist_el("wake", 500, 506, 200, 4, (230, 240, 236), alpha=0.35, length=20, seed=2130),
]

L1521_DIFFS = [
    ("shutters", 175, 126, 0),
    ("laundry", 418, 176, 0),
    ("flowers", 655, 118, 0),
    ("lamp", 228, 260, 0),
    ("tarp", 110, 396, 0),
    ("poles", 632, 320, 0),
    ("cushion", 480, 474, 0),
]


# =================================================================== Level 1522 coral reef under sun shafts
def brain_coral(g, x, y, rx, ry, col, seed):
    sp = sphere_paint(x - rx * 0.2, y - ry * 0.3, rx * 1.1, col, ry=ry * 1.2, light=(-0.2, -0.9, 0.4), amb=0.4, spec=0.15)
    g.fill(Rough(Ell(x, y, rx, ry), 2, 8, seed),
           lambda X, Y: sp(X, Y) * (0.72 + 0.32 * np.abs(np.sin(fbm(X, Y, rx * 0.5, ry * 0.5, 3, seed) * 26)))[..., None])
    g.mul(Ell(x + 6, y + ry * 0.85, rx * 1.05, ry * 0.25), 0.5, feather=8)


def staghorn(g, x, base, h, col, seed):
    rnd = random.Random(seed)

    def br(x0, y0, a, ln, w, dep):
        x1, y1 = x0 + math.cos(a) * ln, y0 - math.sin(a) * ln
        g.fill(Seg(x0, y0, x1, y1, w, w * 0.8), light_x(col, min(x0, x1) - w, max(x0, x1) + w, 1.25, 0.7))
        if dep == 0:
            g.fill(Circ(x1, y1, w * 0.45), mixc(col, (255, 255, 240), 0.4))
            return
        for s in (-1, 1):
            br(x1, y1, a + s * rnd.uniform(0.25, 0.55), ln * rnd.uniform(0.62, 0.8), w * 0.78, dep - 1)
    for a in (1.2, 1.57, 1.95):
        br(x, base, a + rnd.uniform(-0.1, 0.1), h * 0.32, h * 0.07, 3)


def anemone(g, x, base, r, col, tip, seed):
    rnd = random.Random(seed)
    for k in range(46):
        a = math.pi * (0.05 + 0.9 * k / 45)
        ln = r * rnd.uniform(0.7, 1.1)
        x1, y1 = x + math.cos(a) * ln * 1.2, base - math.sin(a) * ln + rnd.uniform(-3, 3)
        g.fill(Seg(x, base - 4, (x + x1) / 2 + rnd.uniform(-5, 5), (base + y1) / 2 - 4, 4, 3.5), col)
        g.fill(Seg((x + x1) / 2, (base + y1) / 2 - 4, x1, y1, 3.5, 3), light_y(col, y1 - 4, base, 1.2, 0.8))
        g.fill(Circ(x1, y1, 2.2), tip)
    g.fill(Ell(x, base, r * 0.8, r * 0.18), mixc(col, (0, 0, 0), 0.3))


def l1522_scene(g, d):
    g.fill(Box(-2, -2, W + 2, H + 2), vgrad([(0, (110, 214, 226)), (70, (40, 150, 190)), (300, (14, 80, 140)), (600, (8, 36, 84))]))
    # bright rippled surface (the source of the sun shafts)
    r_ = g.win((-2, -2, W + 2, 44), pad=0)
    (j0, j1, i0, i1), X, Y = r_
    caus = smooth(0.42, 0.62, fbm(X, Y, 40, 9, 4, 2201)) * smooth(44, 0, Y)
    g.img[j0:j1, i0:i1] += (C((240, 255, 255)) - g.img[j0:j1, i0:i1]) * (caus * 0.85)[..., None]
    # distant reef silhouettes
    ridge(g, 440, 90, 200, 2202, (24, 90, 130), ridged=False, light=False, rock_tex=0.1, haze=((26, 96, 150), 0.6, 0.4))
    ridge(g, 480, 70, 140, 2203, (30, 80, 104), ridged=False, light=False, rock_tex=0.12, haze=((20, 76, 126), 0.4, 0.2))
    # sand with caustics
    def sand(x):
        return 488 + (fbm1(x, 80, 3, 2204) - 0.5) * 26
    g.fill(Under(sand, -10, W + 10, H + 10), grain_tex(vgrad([(470, (130, 160, 160)), (600, (190, 196, 170))]), 0.1, 2205))
    (j0, j1, i0, i1), X, Y = g.win((-2, 460, W + 2, H), pad=0)
    cn = 1 - np.abs(2 * fbm(X, Y, 34, 16, 3, 2206) - 1)
    g.img[j0:j1, i0:i1] += (C((200, 255, 240)) * (smooth(0.86, 0.97, cn) * 0.45 * (Y > sand(X[0])[None, :]))[..., None])
    # rock outcrop (left) with a brain coral and sponges
    rock(g, 150, 470, 150, 70, (70, 90, 96), seed=2207, moss=(120, 110, 80))
    brain_coral(g, 150, 420, 54, 40, (200, 170, 110) if "brain" not in d else (170, 110, 190), 2208)
    for k, (x, h) in enumerate(((250, 70), (266, 54), (234, 46))):
        g.fill(Box(x - 8, 470 - h, x + 8, 470, 6), cyl_paint(x, 8, (230, 170, 50), amb=0.45, spec=0.2))
        g.fill(Ell(x, 470 - h, 7, 3), (120, 70, 20))
    # staghorn coral (middle)
    staghorn(g, 360, 500, 160, (240, 140, 96), 2209)
    # sea fan (right) and a seahorse (difference)
    fx, fy = 740, 330
    fy = 420
    memb = Rough(Inter(Ell(fx, fy, 120, 190), Box(fx - 130, fy - 200, fx + 130, fy - 10)), 14, 40, 2210)
    g.fill(memb, lambda X, Y: C((150, 60, 140)) * (0.5 + 0.5 * np.abs(np.sin(X * 0.9) * np.sin(Y * 0.9)))[..., None],
           alpha=lambda X, Y: 0.35 + 0.3 * smooth(0.4, 0.7, fbm(X, Y, 10, 10, 3, 2211)))
    rnd_ = random.Random(2217)
    for k in range(9):
        a = math.pi * (0.18 + 0.64 * k / 8) + rnd_.uniform(-0.06, 0.06)
        ln = rnd_.uniform(130, 175)
        pts = [(fx + math.cos(a) * ln * t * 0.75 + rnd_.uniform(-6, 6), fy - 10 - math.sin(a) * ln * t) for t in (0, 0.35, 0.7, 1.0)]
        twigs(g, pts, 5, 1.6, (170, 70, 150), seed=2218 + k, n=3)
    rock(g, 760, 480, 90, 34, (70, 86, 92), seed=2212)
    if "seahorse" not in d:
        sx, sy = 650, 260
        body = Union([Ell(sx, sy, 9, 18), Seg(sx + 2, sy + 14, sx - 6, sy + 36, 8, 3), Ell(sx + 3, sy - 22, 8, 7), Seg(sx + 8, sy - 24, sx + 20, sy - 20, 4, 3)])
        g.fill(body, sphere_paint(sx - 2, sy - 8, 14, (240, 190, 60), ry=30, amb=0.45, spec=0.3))
        g.fill(Circ(sx - 6, sy + 38, 6) - Circ(sx - 6, sy + 38, 3), (230, 170, 50))
        g.fill(Circ(sx + 6, sy - 24, 1.8), (20, 20, 20))
    # anemone with two striped fish (difference: fish colour)
    anemone(g, 470, 510, 44, (180, 120, 170), (240, 220, 240), 2213)
    fc = (250, 120, 30) if "clown" not in d else (60, 140, 220)
    fish(g, 452, 448, 40, fc, stripe=(250, 250, 250), face=1)
    fish(g, 506, 470, 32, (250, 120, 30), stripe=(250, 250, 250), face=-1)
    # yellow tang above the coral
    fish(g, 300, 300, 52, (250, 214, 40), face=1)
    # starfish (difference: colour) and an urchin
    stc = (220, 70, 50) if "star" not in d else (60, 110, 200)
    pts = []
    for i in range(10):
        a = i * math.pi / 5 - math.pi / 2 + 0.2
        rr = 24 if i % 2 == 0 else 10
        pts.append((110 + rr * math.cos(a), 556 + rr * math.sin(a) * 0.75))
    g.mul(Moved(Poly(pts), 4, 4), 0.4, feather=4)
    g.fill(Poly(pts), grain_tex(sphere_paint(108, 552, 24, stc, ry=18, amb=0.5, spec=0.2), 0.2, 2214))
    ux, uy = 600, 560
    for k in range(30):
        a = k * math.tau / 30
        g.fill(Seg(ux, uy, ux + math.cos(a) * 22, uy + math.sin(a) * 16 - 4, 1.6, 0.5), (24, 20, 34))
    g.fill(Ell(ux, uy, 13, 10), sphere_paint(ux - 3, uy - 3, 13, (40, 30, 50), ry=10, amb=0.4, spec=0.4))
    # giant clam (difference: open with blue mantle / closed)
    cx, cy = 800, 560
    g.mul(Ell(cx + 6, cy + 16, 66, 8), 0.45, feather=6)
    shell = Ell(cx, cy, 60, 26)
    g.fill(shell, lambda X, Y: sphere_paint(cx, cy - 8, 60, (200, 196, 170), ry=30, amb=0.5)(X, Y) * (0.8 + 0.25 * np.abs(np.sin((X - cx) * 0.22)))[..., None])
    if "clam" not in d:
        g.fill(Ell(cx, cy - 2, 52, 9), lambda X, Y: C((40, 120, 200)) * (0.7 + 0.5 * fbm(X, Y, 4, 3, 3, 2215))[..., None])
        g.fill(Seg(cx - 50, cy - 2, cx + 50, cy - 2, 2.5), (220, 230, 210))
    else:
        g.fill(Seg(cx - 58, cy - 2, cx + 58, cy - 2, 3), (110, 104, 90))
    # seagrass
    rnd = random.Random(2216)
    for _ in range(40):
        x = rnd.choice((rnd.uniform(500, 560), rnd.uniform(860, 900), rnd.uniform(0, 40)))
        y = rnd.uniform(560, 600)
        twigs(g, [(x, y), (x + rnd.uniform(-8, 8), y - 30), (x + rnd.uniform(-14, 14), y - 60)], 3, 1.5, (60, 130, 80), seed=rnd.randint(0, 999), n=0)


L1522_RAYS = [dict(lx=450, ly=-240, col=(170, 236, 240), k=1.6, region=Box(-2, -2, W + 2, 46), threshold=150, soft=60,
                   density=0.9, decay=0.988, samples=80, receive=lambda X, Y: 0.6 + 0.4 * smooth(600, 100, Y))]


def l1522_turtle(g, m):
    x, y = 600, 100
    skin = (150, 140, 96)
    g.fill(Poly([(x - 16, y + 6), (x - 50, y + 30), (x - 64, y + 44), (x - 40, y + 40), (x - 6, y + 16)]), light_y(skin, y, y + 44, 1.2, 0.7))
    g.fill(Poly([(x + 30, y + 10), (x + 52, y + 26), (x + 60, y + 22), (x + 40, y + 6)]), light_y(skin, y, y + 30, 1.1, 0.7))
    g.fill(Poly([(x - 12, y - 8), (x - 46, y - 30), (x - 58, y - 30), (x - 24, y - 2)]), light_y(skin, y - 30, y, 1.3, 0.8))
    g.fill(Ell(x - 56, y + 2, 14, 10), sphere_paint(x - 60, y - 2, 14, skin, ry=10, amb=0.5, spec=0.2))
    g.fill(Circ(x - 62, y - 1, 2), (20, 20, 20))
    shell = Ell(x, y, 46, 24)
    sp = sphere_paint(x - 8, y - 10, 48, (120, 104, 60), ry=28, amb=0.45, spec=0.3)
    g.fill(shell, lambda X, Y: sp(X, Y) * (0.75 + 0.35 * smooth(0.15, 0.3, np.abs(np.sin((X - x) * 0.13 + np.sin((Y - y) * 0.2) * 1.4)) * np.abs(np.sin((Y - y) * 0.16 + (X - x) * 0.03))))[..., None])
    g.add(Diff(shell, Moved(shell, 0, 3)), (200, 240, 240), 0.3)


def l1522_school(g, m):
    rnd = random.Random(2230)
    for _ in range(14):
        fish(g, 300 + rnd.uniform(-60, 60), 150 + rnd.uniform(-22, 22), 18, (190, 200, 210), face=1)


L1522_ELEMENTS = [
    E("school", el(l1522_school), anim=dict(driftVelocity=(26, 0), driftLength=1100, driftStart=-500, bobAmplitude=(0, 6), bobSpeed=0.3)),
    E("turtle", el(l1522_turtle),
      anim=dict(driftVelocity=(-12, 0), driftLength=1100, driftStart=-300, bobAmplitude=(0, 5), bobSpeed=0.15)),
    E("bubbles", el(lambda g, m: [g.fill(Circ(60 + k * 6, 400 - k * 18, 3 + k % 3) - Circ(60 + k * 6 - 1, 400 - k * 18 - 1, 1.8 + k % 3), (220, 250, 255), alpha=0.7) for k in range(5)]),
      daynight="untinted", anim=dict(driftVelocity=(3, 60), driftLength=300, driftFade=True)),
    beam_el("beam1", 300, 0, 200, 500, 60, 160, col=(200, 250, 250), k=0.1),
    beam_el("beam2", 620, 0, 700, 480, 50, 140, col=(200, 250, 250), k=0.09, phase=0.5),
    motes_el("plankton", [(200, 260), (420, 220), (560, 330), (700, 200), (820, 280), (120, 330)], col=(220, 255, 250), r=1.6),
]

L1522_DIFFS = [
    ("brain", 150, 420, 0),
    ("seahorse", 650, 262, 0),
    ("clown", 452, 448, 0),
    ("star", 110, 556, 0),
    ("clam", 800, 556, 0),
]


# =================================================================== Level 1523 fjord with a glacier
WL23 = 362


def l23_left(x):
    return 40 + (np.maximum(x, 0) / 290.0) ** 1.6 * 320 + (fbm1(x, 26, 4, 2301) - 0.5) * 22


def l23_right(x):
    return 70 + (np.maximum(900 - x, 0) / 300.0) ** 1.5 * 260 + (fbm1(x, 28, 4, 2302) - 0.5) * 22


def l1523_upper(g, d):
    sky(g, [(0, (60, 120, 196)), (180, (150, 190, 226)), (WL23, (210, 226, 236))], y1=WL23)
    cumulus(g, 470, 70, 140, 34, seed=2303, alpha=0.9)
    cloud_layer(g, 120, 180, (250, 250, 252), (200, 210, 225), cover=0.3, sx=200, sy=12, seed=2304, alpha=0.6)
    ridge(g, 300, 170, 220, 2305, (110, 120, 140), snow=(240, (246, 248, 252)), haze=((190, 206, 224), 0.4, 0.5))
    # glacier tongue flowing to the water
    gl = Rough(Poly([(360, 220), (520, 214), (560, WL23), (330, WL23)]), 6, 20, 2306)
    g.fill(gl, lambda X, Y: (C((226, 238, 248)) * (0.9 + 0.14 * fbm(X, Y, 50, 6, 4, 2307))[..., None]
                            * (1 - 0.12 * smooth(0.9, 0.97, 1 - np.abs(2 * fbm(X, Y, 40, 5, 3, 2308) - 1)))[..., None]
                            * light_x((255, 255, 255), 340, 560, 1.0, 0.85)(X, Y) / 255.0))
    g.fill(Inter(gl, Box(300, WL23 - 22, 600, WL23)), (110, 170, 210), alpha=lambda X, Y: 0.6 * smooth(WL23 - 22, WL23, Y))
    ridge(g, 342, 60, 160, 2309, (52, 70, 56), ridged=False, light=False, rock_tex=0.04, haze=((160, 184, 200), 0.5, 0.2))
    treeline(g, 350, 22, 7, 2350, (34, 52, 40), x0=240, x1=660, haze=((150, 176, 196), 0.4, 0.15))
    # steep cliffs
    for f, x0, x1, s in ((l23_left, -20, 330, 2310), (l23_right, 600, W + 20, 2311)):
        cl = Under(f, x0, x1, WL23 + 2)
        g.fill(cl, rock_face((104, 100, 96), seed=s, sx=40, sy=60, strata=0.08))
        g.fill(cl, (40, 70, 40), alpha=lambda X, Y, f=f, s=s: 0.7 * smooth(0.55, 0.7, fbm(X, Y, 10, 6, 3, s + 5)) * smooth(f(X[0])[None, :] + 30, f(X[0])[None, :], Y))
        g.mul(cl, 0.35, alpha=lambda X, Y, x0=x0: smooth(WL23 - 120, WL23, Y))
    # waterfall down the left cliff
    wf = Rough(Poly([(196, 158), (214, 158), (238, WL23), (196, WL23)]), 2, 6, 2312)
    g.fill(wf, lambda X, Y: C((236, 244, 250)) * (0.75 + 0.3 * fbm(X, Y, 2, 30, 3, 2313))[..., None],
           alpha=lambda X, Y: 0.6 + 0.4 * smooth(0.4, 0.6, fbm(X, Y, 3, 40, 3, 2314)))
    g.fill(Ell(218, WL23 - 4, 40, 10), (240, 246, 250), alpha=0.6, feather=8)
    # cabin on the left clifftop (difference)
    if "cabin" not in d:
        gable_house(g, 70, 112, 46, 22, 16, (170, 60, 46), (70, 70, 74), seed=2315)
        window_glass(g, 82, 96, 92, 106, frame=(240, 240, 236))
    pine(g, 140, 120, 46, col=(36, 60, 44), seed=2316)
    pine(g, 30, 96, 40, col=(36, 60, 44), seed=2317)
    # grassy shore + red boathouse (right)
    shore = Rough(Poly([(640, WL23 + 2), (660, 318), (900, 300), (904, WL23 + 2)]), 3, 14, 2318)
    g.fill(shore, tex(vgrad([(300, (90, 120, 60)), (WL23, (60, 86, 44))]), 0.25, 4, 3, 3, 2319))
    gable_house(g, 700, 352, 90, 40, 30, (176, 46, 38), (60, 60, 64), seed=2320, side=(130, 34, 30), side_w=20,
                wall_paint=planks("v", (176, 46, 38), seed=2321, width=7))
    for x in (698, 788):
        g.fill(Box(x, 312, x + 4, 352), (240, 236, 228))
    dc = (240, 236, 228) if "door" not in d else (60, 110, 160)
    g.fill(Box(726, 322, 762, 352), planks("v", dc, seed=2322, width=6))
    g.fill(Box(742, 322, 746, 352), (40, 30, 30), alpha=0.4)
    g.fill(Box(846, 236, 849, 330), (230, 230, 226))
    if "pennant" not in d:
        g.fill(Poly([(849, 236), (896, 247), (849, 260)]), light_y((40, 90, 170), 236, 260, 1.2, 0.8))
    pine(g, 640, 330, 60, col=(36, 60, 44), seed=2323)
    pine(g, 878, 320, 50, col=(36, 60, 44), seed=2324)


def l1523_lower(g, d):
    water(g, WL23, H, (110, 150, 176), (30, 60, 80), seed=2325, streak=0.08)
    g.reflect(WL23, WL23, H, k=0.82, tint=(30, 70, 90), tint_k=0.2, ripple=2.0, fade=0.4, streak=0.2)
    ripples_light(g, WL23 + 2, H, (255, 255, 255), k=0.2, seed=2326)
    # sailboat (difference: sail colour)
    g.mul(Ell(560, 412, 40, 3), 0.3, feather=3)
    g.fill(Poly([(526, 400), (594, 400), (586, 410), (534, 410)]), light_y((240, 240, 236), 400, 410, 1.1, 0.7))
    g.fill(Box(558, 330, 560, 402), (70, 66, 60))
    sc = (246, 244, 236) if "sail" not in d else (210, 70, 60)
    g.fill(Poly([(561, 334), (561, 396), (592, 396)]), light_x(sc, 561, 592, 1.05, 0.85))
    g.fill(Poly([(556, 340), (556, 396), (532, 396)]), light_x((236, 234, 226), 532, 556, 1.05, 0.85))
    # kayak with paddler (difference: colour)
    kc = (230, 170, 40) if "kayak" not in d else (60, 160, 90)
    g.mul(Ell(370, 462, 60, 4), 0.35, feather=4)
    g.fill(Poly([(310, 456), (430, 456), (420, 464), (320, 464)]), light_y(kc, 456, 464, 1.2, 0.7))
    g.fill(Ell(370, 446, 7, 10), (200, 60, 50))
    g.fill(Circ(370, 432, 6), (220, 180, 150))
    g.fill(Seg(340, 470, 402, 428, 2), (40, 40, 40))
    g.fill(Ell(402, 428, 5, 2), (40, 40, 40))
    g.fill(Ell(340, 470, 5, 2), (40, 40, 40))
    # foreground: rocky shore with grass and a tent (difference)
    def fg(x):
        return 500 + 40 * np.sin(x * 0.005 + 2.4) + (fbm1(x, 40, 3, 2327) - 0.5) * 18 + np.maximum(0, x - 300) ** 1.6 * 0.12
    gnd = Under(fg, -20, 560, H + 20)
    g.fill(gnd, tex(vgrad([(470, (90, 110, 60)), (600, (60, 76, 40))]), 0.3, 3, 4, 4, 2328))
    blades(g, 500, 600, (90, 120, 50), n=160, seed=2329, x0=0, x1=400)
    rock(g, 380, 520, 50, 26, (120, 116, 110), seed=2330, wet=True)
    if "tent" not in d:
        g.mul(Ell(160, 530, 56, 6), 0.45, feather=6)
        g.fill(Poly([(112, 528), (160, 480), (208, 528)]), lgrad(160, 480, 160, 528, [(0, (250, 160, 60)), (1, (210, 110, 30))]))
        g.fill(Poly([(160, 480), (208, 528), (222, 525), (174, 482)]), light_y((170, 80, 20), 480, 528, 1.0, 0.7))
        g.fill(Poly([(146, 528), (160, 502), (174, 528)]), (60, 40, 30))
    # seal on a rock (difference)
    rock(g, 780, 560, 70, 26, (110, 108, 104), seed=2331, wet=True)
    if "seal" not in d:
        sx, sy = 780, 528
        g.fill(Union([Ell(sx, sy, 34, 13), Ell(sx - 30, sy - 8, 12, 10)]), sphere_paint(sx - 10, sy - 8, 36, (110, 104, 100), ry=16, amb=0.4, spec=0.4))
        g.fill(Circ(sx - 36, sy - 10, 1.8), (20, 20, 20))
        g.fill(Poly([(sx + 30, sy), (sx + 46, sy - 8), (sx + 44, sy + 6)]), (90, 84, 80))


L1523_ELEMENTS = [
    cloud_el("cloud", 700, 120, 90, 20, speed=4, alpha=0.75, seed=2340),
    bird_el("eagle", 300, 90, s=12, speed=14, col=(50, 46, 44)),
    mist_el("mist1", 450, 372, 260, 7, (236, 240, 246), alpha=0.45, length=40, seed=2341),
    mist_el("spray", 218, 350, 40, 12, (240, 246, 250), alpha=0.5, length=10, seed=2342),
    glint_el("glint", [(470, 420), (260, 400), (660, 470), (820, 420)], r=4, speed=0.5),
]

L1523_DIFFS = [
    ("cabin", 92, 98, 0),
    ("door", 744, 336, 0),
    ("pennant", 866, 246, 0),
    ("sail", 576, 366, 0),
    ("kayak", 370, 452, 0),
    ("tent", 162, 508, 0),
    ("seal", 774, 524, 0),
]


# =================================================================== Level 1524 rice terraces in morning mist
def l24_bands():
    ys, y, sp = [], 262, 9.0
    while y < H + 160:
        ys.append(y)
        y += sp
        sp *= 1.16
    return ys


def l24_curve(k, y0):
    amp = 6 + k * 2.2
    return lambda x: y0 + amp * np.sin(x * (0.009 - k * 0.0002) + k * 0.7) + (fbm1(x, 70, 3, 2400 + k) - 0.5) * (4 + k * 1.5)


def l1524_scene(g, d):
    sky(g, [(0, (110, 126, 170)), (110, (226, 176, 170)), (210, (252, 214, 170)), (300, (250, 226, 196))])
    sun(g, 640, 150, r=16, col=(255, 240, 210), halo=(255, 190, 140), k=0.9)
    for base, hgt, col, hz, s in ((214, 70, (150, 140, 170), 0.55, 2401), (238, 60, (120, 120, 150), 0.45, 2402), (262, 50, (90, 100, 120), 0.35, 2403)):
        ridge(g, base, hgt, 150, s, col, ridged=False, light=False, rock_tex=0.05, haze=((246, 214, 196), hz, hz * 0.6))
        fog_band(g, base - 30, base - 6, base + 6, (250, 230, 216), 0.6, seed=s + 10)
    if "pagoda" not in d:   # lone pine on the far ridge
        g.fill(Seg(333, 218, 335, 190, 3, 2), (70, 70, 84))
        for cy_, rx_ in ((192, 22), (182, 16), (174, 10)):
            g.fill(Rough(Ell(335, cy_, rx_, 5), 1.5, 4, cy_), (84, 84, 104))
    g.fill(Box(-2, 250, W + 2, H + 2), (96, 108, 64))
    ys = l24_bands()
    for k in range(len(ys) - 1):
        top_f, bot_f = l24_curve(k, ys[k]), l24_curve(k + 1, ys[k + 1])
        band = Diff(Under(top_f, -20, W + 20, H + 20), Under(bot_f, -20, W + 20, H + 20))
        green = (k % 3 == 1)
        def paint(X, Y, k=k, top_f=top_f, bot_f=bot_f, green=green):
            t = np.clip((Y - top_f(X[0])[None, :]) / np.maximum(bot_f(X[0])[None, :] - top_f(X[0])[None, :], 1), 0, 1)
            refl = C((250, 222, 196)) + (C((150, 150, 186)) - C((250, 222, 196))) * t[..., None]
            refl = refl * (0.94 + 0.12 * fbm(X, Y, 40, 1.5, 3, 2410 + k))[..., None]
            if green:
                rows = smooth(0.55, 0.8, np.abs(np.sin(X * (1.6 - k * 0.07) + fbm(X, Y, 20, 4, 2, 2420 + k) * 3)))
                refl = refl + (C((104, 146, 64)) * (0.8 + 0.3 * fbm(X, Y, 3, 2, 2, 2425 + k))[..., None] - refl) * (rows * 0.8)[..., None]
            return refl
        g.fill(band, paint)
        bund = Diff(Under(lambda x, f=bot_f: f(x) - 1.5 - k * 0.35, -20, W + 20, H + 20), Under(bot_f, -20, W + 20, H + 20))
        g.fill(bund, light_y((88, 104, 56), ys[k + 1] - 20, ys[k + 1] + 20, 1.2, 0.8))
        g.add(Diff(Under(lambda x, f=bot_f: f(x) - 1.5 - k * 0.35, -20, W + 20, H + 20), Under(lambda x, f=bot_f: f(x) - 0.6 - k * 0.15, -20, W + 20, H + 20)),
              (255, 220, 170), 0.25)
    fog_band(g, 260, 290, 340, (250, 232, 220), 0.45, seed=2430)
    # farmhouses (left) on the terraces (difference: roof colour)
    rc = (70, 64, 60) if "roof" not in d else (160, 60, 40)
    for x, base, w in ((70, 344, 70), (160, 330, 50)):
        g.mul(Ell(x + w / 2 + 6, base, w * 0.7, 4), 0.4, feather=4)
        g.fill(Box(x, base - 26, x + w, base), planks("v", (150, 110, 76), seed=x, width=6))
        g.fill(Poly([(x - 10, base - 24), (x + w / 2, base - 26 - w * 0.42), (x + w + 10, base - 24)]),
               tex(light_y(rc if x == 70 else (70, 64, 60), base - 60, base - 24, 1.2, 0.8), 0.2, 3, 2, 3, x + 1))
        window_glass(g, x + 8, base - 20, x + 18, base - 10, lit=(255, 200, 120), frame=(90, 70, 50))
    for x, h in ((240, 60), (30, 50), (820, 70), (860, 54)):
        crown(g, x, 330 - h * 0.6, h * 0.4, h * 0.36, (70, 96, 50), seed=2440 + x)
    # farmer with conical hat on a bund (difference: carrying baskets)
    fx, fb = 520, 404
    figure(g, fx, fb, 58, (70, 90, 120), pants=(50, 50, 60), face_right=False)
    g.fill(Poly([(fx - 18, fb - 60), (fx, fb - 74), (fx + 18, fb - 60)]), light_x((214, 190, 130), fx - 18, fx + 18, 1.2, 0.7))
    if "pole" not in d:
        g.fill(Seg(fx - 46, fb - 44, fx + 46, fb - 50, 3), (120, 90, 50))
        for bx in (fx - 44, fx + 44):
            g.fill(Seg(bx, fb - 47, bx - 6, fb - 26, 0.8), (60, 50, 40))
            g.fill(Seg(bx, fb - 47, bx + 6, fb - 26, 0.8), (60, 50, 40))
            g.fill(Poly([(bx - 10, fb - 26), (bx + 10, fb - 26), (bx + 7, fb - 10), (bx - 7, fb - 10)]),
                   lambda X, Y: C((176, 140, 80)) * (0.75 + 0.3 * np.abs(np.sin(X * 1.6) * np.sin(Y * 1.6)))[..., None])
    # egret standing in a paddy (difference)
    if "egret" not in d:
        ex, ey = 830, 470
        g.fill(Seg(ex, ey, ex - 2, ey - 26, 1.6), (40, 40, 40))
        g.fill(Seg(ex + 4, ey, ex + 2, ey - 26, 1.6), (40, 40, 40))
        g.fill(Ell(ex, ey - 36, 16, 10), sphere_paint(ex - 4, ey - 40, 16, (246, 246, 240), ry=10, amb=0.6))
        g.fill(Seg(ex - 10, ey - 40, ex - 16, ey - 64, 4, 3), (244, 244, 238))
        g.fill(Ell(ex - 18, ey - 66, 5, 4), (244, 244, 238))
        g.fill(Poly([(ex - 22, ey - 67), (ex - 38, ey - 64), (ex - 22, ey - 63)]), (230, 180, 40))
        g.fill(Ell(ex, ey + 2, 16, 3), (255, 255, 255), alpha=0.35)
    # scarecrow (difference)
    if "scarecrow" not in d:
        sx, sy = 300, 520
        g.fill(Seg(sx, sy + 30, sx, sy - 38, 3), (110, 80, 50))
        g.fill(Seg(sx - 30, sy - 22, sx + 30, sy - 25, 2.6), (110, 80, 50))
        g.fill(Rough(Poly([(sx - 22, sy - 26), (sx + 22, sy - 27), (sx + 16, sy + 6), (sx - 16, sy + 6)]), 1.5, 3, 2460),
               tex(light_x((120, 100, 140), sx - 22, sx + 22, 1.2, 0.7), 0.2, 2, 4))
        for k in range(5):
            g.fill(Seg(sx - 30 + k * 2, sy - 22, sx - 34 + k * 3, sy - 14, 1), (200, 170, 90))
        g.fill(Circ(sx, sy - 38, 9), sphere_paint(sx - 3, sy - 41, 9, (214, 190, 140), amb=0.5))
        g.fill(Poly([(sx - 20, sy - 41), (sx, sy - 58), (sx + 20, sy - 41)]), light_x((214, 190, 130), sx - 20, sx + 20, 1.2, 0.7))
    # water buffalo resting in a paddy (bottom right)
    bx, by = 640, 568
    g.fill(Union([Ell(bx, by, 56, 24), Ell(bx - 54, by - 8, 18, 14)]), sphere_paint(bx - 10, by - 14, 60, (74, 70, 70), ry=30, amb=0.4, spec=0.25))
    g.fill(Ell(bx - 58, by - 22, 22, 6) - Ell(bx - 58, by - 18, 16, 6), (200, 190, 170))
    g.fill(Ell(bx, by + 18, 60, 8), (230, 220, 210), alpha=0.4)


L1524_ELEMENTS = [
    mist_el("mist1", 450, 296, 300, 10, (252, 236, 224), alpha=0.5, length=80, seed=2450),
    mist_el("mist2", 300, 252, 200, 8, (252, 236, 224), alpha=0.4, length=60, seed=2451),
    bird_el("egret_fly", 400, 120, s=10, speed=-16, col=(250, 250, 246)),
    glint_el("glint", [(420, 330), (620, 520), (150, 470), (840, 380)], col=(255, 240, 210), r=4, speed=0.5),
    smoke_el("smoke", 100, 300, r=6, col=(236, 226, 220), rise=50, wind=6, alpha=0.4),
]

L1524_DIFFS = [
    ("pagoda", 335, 190, 0),
    ("roof", 105, 312, 0),
    ("pole", 520, 370, 0),
    ("egret", 822, 440, 0),
    ("scarecrow", 300, 490, 0),
]


# =================================================================== Level 1525 desert oasis
def dune_paint(f, col, seed, lit_k=1.25, shade_k=0.62):
    def p(X, Y):
        xs = X[0]
        sl = (f(xs + 14) - f(xs - 14)) / 28.0
        lit = shade_k + (lit_k - shade_k) * smooth(0.5, -0.5, sl[None, :] * 3) * np.ones_like(Y)
        rip = 1 + 0.06 * np.sin(X * 0.25 + Y * 1.4 + fbm(X, Y, 30, 10, 2, seed) * 8)
        depth = np.clip((Y - f(xs)[None, :]) / 60, 0, 1)
        return C(col) * (lit * rip * (1 - 0.12 * depth))[..., None]
    return grain_tex(p, 0.05, seed + 1)


def dune_curve(base, amp, freq, phase, seed, sharp=1.6):
    def f(x):
        u = np.sin(x * freq + phase)
        return base - amp * np.sign(u) * np.abs(u) ** (1 / sharp) * 0.5 - amp * 0.5 + (fbm1(x, 160, 2, seed) - 0.5) * amp * 0.25
    return f


POOL25 = Ell(450, 420, 190, 34)


def l1525_upper(g, d):
    sky(g, [(0, (60, 130, 210)), (180, (150, 196, 230)), (300, (236, 226, 200))], y1=430)
    sun(g, 780, 80, r=14, col=(255, 252, 236), halo=(255, 230, 180), k=0.7)
    for base, amp, fr, ph, col, s in ((300, 60, 0.008, 0.4, (226, 170, 110), 2501), (340, 70, 0.006, 2.0, (220, 150, 90), 2502)):
        f = dune_curve(base, amp, fr, ph, s)
        g.fill(Under(f, -20, W + 20, 440), dune_paint(f, col, s))
    g.fog(260, 330, (240, 220, 190), 0.3, 0.0)
    # palms around the pool (difference: one palm missing coconuts)
    palm(g, 300, 410, 260, 190, 30, 2503, fronds=8, coconuts=True)
    palm(g, 360, 412, 410, 220, -20, 2504, fronds=7, coconuts="coco" not in d)
    palm(g, 600, 410, 650, 170, -40, 2505, fronds=9, coconuts=True)
    palm(g, 690, 414, 700, 250, 20, 2506, fronds=7, coconuts=False)
    for x, w in ((230, 70), (520, 60), (760, 70)):
        g.fill(Rough(Ell(x, 404, w, 16), 4, 10, x), tex((80, 110, 50), 0.3, 4, 3))
    # tents (difference: stripe colour)
    sc = (180, 50, 40) if "tent" not in d else (40, 100, 160)
    for x0, w in ((470, 100),):
        g.fill(Poly([(x0, 404), (x0 + 10, 360), (x0 + w / 2, 350), (x0 + w - 10, 360), (x0 + w, 404)]), tex(light_x((60, 46, 36), x0, x0 + w, 1.2, 0.7), 0.15, 4, 2))
        for k in range(3):
            g.fill(Box(x0 + 8, 368 + k * 12, x0 + w - 8, 372 + k * 12), sc)
        g.fill(Poly([(x0 + 36, 404), (x0 + 50, 372), (x0 + 64, 404)]), (24, 18, 14))
    # camels by the trees (difference: second camel)
    for k, (cx, cb) in enumerate(((780, 402), (840, 404))):
        if k == 1 and "camel" in d:
            continue
        col = (190, 150, 100)
        g.mul(Ell(cx + 6, cb, 34, 4), 0.4, feather=4)
        for lx in (-16, -8, 12, 18):
            g.fill(Seg(cx + lx, cb - 30, cx + lx, cb, 4, 3), light_x(col, cx - 20, cx + 20, 1.1, 0.7))
        g.fill(Union([Ell(cx, cb - 38, 26, 12), Ell(cx - 2, cb - 48, 12, 10)]), sphere_paint(cx - 6, cb - 46, 28, col, ry=16, amb=0.45))
        g.fill(Seg(cx - 22, cb - 38, cx - 34, cb - 64, 7, 5), light_x(col, cx - 38, cx - 18, 1.2, 0.7))
        g.fill(Ell(cx - 40, cb - 66, 9, 5), col)


def l1525_lower(g, d):
    # sand around + pool with reflection
    f = dune_curve(470, 40, 0.007, 1.2, 2510, sharp=1.2)
    g.fill(Box(-2, 400, W + 2, H + 2), dune_paint(lambda x: 400 + 0 * x, (230, 180, 120), 2511))
    g.fill(POOL25, vgrad([(386, (120, 170, 190)), (454, (40, 100, 110))]))
    before = g.img.copy()
    g.reflect(404, 400, 460, x0=250, x1=650, k=0.75, tint=(30, 90, 100), tint_k=0.3, ripple=2.0, fade=0.3)
    r = g.win((250, 400, 650, 460), pad=0)
    (j0, j1, i0, i1), X, Y = r
    m = g.cover(POOL25, X, Y, 1.5)
    g.img[j0:j1, i0:i1] = before[j0:j1, i0:i1] + (g.img[j0:j1, i0:i1] - before[j0:j1, i0:i1]) * m[..., None]
    g.add(Diff(POOL25, Ell(450, 422, 186, 30)), (255, 250, 230), 0.25)
    # foreground dune
    g.fill(Under(f, -20, W + 20, H + 20), dune_paint(f, (236, 176, 110), 2512))
    # rug with pottery (difference: jar) and lantern (difference)
    g.mul(Poly([(120, 540), (330, 530), (350, 586), (110, 596)]), 0.4, feather=6)
    g.fill(Poly([(110, 530), (320, 520), (340, 576), (100, 586)]), lambda X, Y: C((160, 40, 40)) * (0.8 + 0.25 * np.abs(np.sin(X * 0.2 + Y * 0.3) * np.sin(X * 0.3 - Y * 0.2)))[..., None])
    for k, (x, r_, col) in enumerate(((170, 22, (190, 110, 70)), (230, 16, (170, 90, 60)), (280, 20, (60, 110, 140)))):
        if k == 2 and "jar" in d:
            continue
        g.fill(Union([Ell(x, 540, r_, r_ * 1.1), Box(x - r_ * 0.4, 540 - r_ * 1.6, x + r_ * 0.4, 540 - r_ * 0.8)]), sphere_paint(x - r_ * 0.3, 532, r_, col, ry=r_ * 1.2, amb=0.4, spec=0.3))
        g.fill(Ell(x, 540 - r_ * 1.6, r_ * 0.5, r_ * 0.15), mixc(col, (0, 0, 0), 0.4))
    if "lantern" not in d:
        lx, ly = 600, 540
        g.mul(Ell(lx + 10, ly + 30, 22, 4), 0.4, feather=4)
        g.fill(Poly([(lx - 14, ly), (lx + 14, ly), (lx + 10, ly + 30), (lx - 10, ly + 30)]), lambda X, Y: C((200, 160, 70)) * (0.6 + 0.5 * smooth(0.3, 0.7, np.abs(np.sin(X * 1.2) * np.sin(Y * 1.2))))[..., None])
        g.fill(Poly([(lx - 14, ly), (lx, ly - 22), (lx + 14, ly)]), light_x((190, 150, 60), lx - 14, lx + 14, 1.3, 0.7))
        g.fill(Ell(lx, ly - 26, 4, 4) - Ell(lx, ly - 26, 2, 2), (190, 150, 60))
    # bird (hoopoe-ish) on a stick (difference)
    if "bird" not in d:
        bx, by = 60, 420
        g.fill(Seg(bx, by + 60, bx + 4, by + 8, 3), (110, 80, 50))
        g.fill(Ell(bx, by, 14, 8), sphere_paint(bx - 3, by - 3, 14, (210, 150, 90), ry=8, amb=0.5))
        g.fill(Circ(bx - 12, by - 6, 6), (210, 150, 90))
        g.fill(Poly([(bx - 14, by - 10), (bx - 10, by - 22), (bx - 6, by - 10)]), (220, 140, 70))
        g.fill(Seg(bx - 16, by - 6, bx - 28, by - 2, 1.6), (40, 30, 30))
        for k in range(3):
            g.fill(Seg(bx + 2 + k * 4, by - 4, bx + 6 + k * 4, by + 4, 2), (30, 30, 30))
    # wind-blown footprints
    for k in range(8):
        g.mul(Ell(420 + k * 30, 590 - k * 12, 5, 2.5), 0.3, feather=1.5)


L1525_ELEMENTS = [
    E("sand", el(lambda g, m: g.fill(Box(-2, 540, W + 2, 600), (240, 210, 160), alpha=lambda X, Y: 0.25 * smooth(0.55, 0.75, fbm(X, Y, 60, 3, 3, 2530)) * smooth(540, 570, Y))),
      anim=dict(driftVelocity=(40, 0), driftLength=200, driftFade=True)),
    bird_el("kite", 300, 80, s=10, speed=12, col=(70, 50, 40)),
    glint_el("glint", [(400, 418), (520, 426), (330, 430)], col=(255, 255, 240), r=4, speed=0.6),
    E("heat", el(lambda g, m: g.fill(Box(-2, 290, W + 2, 330), (250, 230, 200), alpha=0.15)), anim=dict(twinkle=0.8, twinkleSpeed=0.3)),
]

L1525_DIFFS = [
    ("coco", 410, 232, 0),
    ("tent", 520, 380, 0),
    ("camel", 836, 372, 0),
    ("jar", 280, 530, 0),
    ("lantern", 600, 530, 0),
    ("bird", 56, 420, 0),
]


# =================================================================== shared foliage / props for 1526-1529
def fern(g, x, y, ln, ang, col=(70, 120, 50), seed=0, droop=0.5):
    """One fern frond: curved midrib with paired leaflets shrinking towards the tip."""
    rnd = random.Random(seed)
    prev = (x, y)
    n = 14
    for j in range(1, n + 1):
        t = j / n
        a = ang + droop * t * t * (1 if math.cos(ang) >= 0 else -1)
        px = x + math.cos(ang) * ln * t
        py = y - math.sin(ang) * ln * t + droop * ln * 0.5 * t * t
        g.fill(Seg(prev[0], prev[1], px, py, 2.2 * (1 - t) + 0.6), mixc(col, (30, 40, 20), 0.35))
        wl = ln * 0.16 * (1 - t * 0.85)
        dx, dy = px - prev[0], py - prev[1]
        dl = math.hypot(dx, dy) or 1
        nx, ny = -dy / dl, dx / dl
        for s in (-1, 1):
            ex, ey = px + s * nx * wl + dx / dl * wl * 0.5, py + s * ny * wl + dy / dl * wl * 0.5 + wl * 0.25
            g.fill(Seg(px, py, ex, ey, wl * 0.42, 0.8), light_y(mixc(col, (200, 230, 120), rnd.uniform(0, 0.15)), y - ln, y + ln, 1.25, 0.75))
        prev = (px, py)


def fern_clump(g, x, y, ln, col=(70, 120, 50), seed=0, n=7):
    rnd = random.Random(seed)
    for k in range(n):
        a = math.pi * (0.12 + 0.76 * k / (n - 1)) + rnd.uniform(-0.1, 0.1)
        fern(g, x, y, ln * rnd.uniform(0.75, 1.1), a, col, seed + k, droop=rnd.uniform(0.3, 0.6))


def crate(g, x0, y0, w, h, col=(176, 136, 90), seed=0):
    g.mul(Box(x0 + 4, y0 + h - 2, x0 + w + 8, y0 + h + 4), 0.5, feather=4)
    g.fill(Box(x0, y0, x0 + w, y0 + h, 1), planks("h", col, seed=seed, width=max(6, h / 4), x_or_y0=y0))
    for xx in (x0, x0 + w - 5):
        g.fill(Box(xx, y0, xx + 5, y0 + h), light_x(mixc(col, (0, 0, 0), 0.2), xx, xx + 5, 1.2, 0.7))


def grapes(g, x, y, s, col, seed=0):
    rnd = random.Random(seed)
    pts = []
    for row in range(6):
        n = max(1, 5 - row)
        for k in range(n):
            pts.append((x + (k - (n - 1) / 2) * 6.5 * s + rnd.uniform(-1, 1) * s, y + row * 6 * s))
    for px, py in pts:
        g.fill(Circ(px, py, 3.8 * s), sphere_paint(px - 1.2 * s, py - 1.4 * s, 3.8 * s, col, amb=0.35, spec=0.45, shin=24))
    g.fill(Seg(x, y - 4 * s, x + 2 * s, y - 10 * s, 1.4 * s), (100, 80, 50))


# =================================================================== Level 1526 forest waterfall with sun shafts
def l1526_scene(g, d):
    g.fill(Box(-2, -2, W + 2, H + 2), vgrad([(0, (210, 230, 210)), (200, (120, 150, 120)), (600, (40, 56, 40))]))
    # hazy depth: distant trunks + canopy
    rnd = random.Random(2601)
    for depth, (n, wmin, wmax, haze) in enumerate(((22, 4, 8, 0.65), (12, 9, 16, 0.4))):
        for _ in range(n):
            x, w = rnd.uniform(-20, W + 20), rnd.uniform(wmin, wmax)
            g.fill(Seg(x, 420, x + rnd.uniform(-4, 4), -10, w, w * 0.7), light_x(mixc((60, 54, 44), (190, 210, 190), haze), x - w, x + w, 1.1, 0.8))
        cloud_layer(g, -40, 140 + depth * 40, mixc((80, 120, 60), (200, 220, 190), haze), mixc((40, 70, 40), (150, 170, 150), haze),
                    cover=0.55, sx=46, sy=30, seed=2602 + depth, alpha=0.9)
    # cliff with the waterfall
    cliff = Rough(Poly([(250, 420), (290, 120), (360, 90), (560, 84), (640, 110), (680, 420)]), 10, 30, 2604)
    g.fill(cliff, rock_face((96, 96, 86), seed=2605, sx=30, sy=40, strata=0.05))
    g.fill(cliff, (60, 100, 50), alpha=lambda X, Y: 0.75 * smooth(0.5, 0.65, fbm(X, Y, 12, 10, 4, 2606)))
    g.mul(cliff, 0.35, alpha=lambda X, Y: smooth(250, 680, X) * 0.6)
    fall = Rough(Poly([(400, 100), (500, 96), (520, 392), (380, 392)]), 3, 8, 2607)
    g.fill(fall, lambda X, Y: C((236, 244, 246)) * (0.72 + 0.35 * fbm(X, Y, 3, 40, 4, 2608))[..., None],
           alpha=lambda X, Y: 0.75 + 0.25 * smooth(0.35, 0.6, fbm(X, Y, 4, 50, 3, 2609)))
    g.mul(fall, 0.25, alpha=lambda X, Y: smooth(0.5, 0.7, fbm(X, Y, 2.5, 30, 3, 2610)))
    g.fill(Box(392, 96, 508, 104, 3), (230, 240, 240), alpha=0.8)
    # pool
    def pool(x):
        return 380 + (fbm1(x, 60, 3, 2611) - 0.5) * 10
    g.fill(Inter(Under(pool, 150, 790, 480), Rough(Ell(470, 440, 300, 80), 8, 30, 2641)), vgrad([(380, (90, 130, 120)), (480, (40, 80, 70))]), feather=2)
    (j0, j1, i0, i1), X, Y = g.win((180, 378, 760, 480), pad=0)
    g.img[j0:j1, i0:i1] *= (1 + 0.15 * (fbm(X, Y, 30, 2, 3, 2612) - 0.5))[..., None]
    g.fill(Ell(450, 396, 110, 18), (240, 246, 246), alpha=lambda X, Y: 0.8 * smooth(0.4, 0.6, fbm(X, Y, 10, 4, 3, 2613)), feather=6)
    # banks
    def bank(x):
        return 470 + 50 * np.cos((x - 450) * 0.007) * -1 + (fbm1(x, 40, 3, 2614) - 0.5) * 20
    g.fill(Under(bank, -20, W + 20, H + 20), tex(vgrad([(430, (70, 90, 50)), (600, (40, 56, 30))]), 0.35, 4, 3, 4, 2615))
    for x, y, rx, ry, s in ((210, 420, 60, 34, 2616), (700, 420, 70, 36, 2617), (330, 470, 40, 20, 2618), (600, 480, 44, 22, 2619)):
        rock(g, x, y, rx, ry, (110, 110, 100), seed=s, moss=(80, 120, 50), wet=True)
    # framing trees (left / right) with branches
    for x, w, s in ((40, 70, 2620), (870, 80, 2621)):
        g.fill(Seg(x, H + 20, x + 4, -20, w, w * 0.8), tex(light_x((80, 66, 50), x - w / 2, x + w / 2, 1.2, 0.5), 0.3, 2, 14, 4, s))
        g.fill(Seg(x, H + 20, x + 4, -20, w, w * 0.8), (70, 110, 50), alpha=lambda X, Y, s=s: 0.6 * smooth(0.55, 0.7, fbm(X, Y, 6, 10, 3, s + 3)))
    g.fill(Seg(60, 210, 250, 190, 9, 4), light_y((80, 66, 50), 180, 220, 1.2, 0.7))
    crown(g, 90, -20, 170, 70, (60, 96, 44), seed=2622)
    crown(g, 840, -20, 160, 70, (66, 100, 44), seed=2623)
    # kingfisher on the branch (difference)
    if "bird" not in d:
        kx, ky = 200, 186
        g.fill(Ell(kx, ky, 10, 7), sphere_paint(kx - 3, ky - 3, 10, (240, 130, 50), ry=7, amb=0.5))
        g.fill(Ell(kx + 2, ky - 6, 10, 5), sphere_paint(kx, ky - 9, 10, (30, 130, 190), ry=6, amb=0.5, spec=0.5))
        g.fill(Circ(kx - 8, ky - 10, 6), sphere_paint(kx - 10, ky - 12, 6, (30, 130, 190), amb=0.5, spec=0.5))
        g.fill(Poly([(kx - 13, ky - 11), (kx - 28, ky - 8), (kx - 13, ky - 7)]), (30, 30, 30))
        g.fill(Poly([(kx + 8, ky - 4), (kx + 22, ky + 4), (kx + 10, ky + 2)]), (30, 110, 170))
        g.fill(Circ(kx - 9, ky - 11, 1.4), (10, 10, 10))
    # rhododendron bush (difference: flower colour)
    fc = (220, 90, 150) if "flowers" not in d else (250, 250, 240)
    crown(g, 780, 330, 60, 40, (50, 86, 40), seed=2624)
    rnd = random.Random(2625)
    for _ in range(16):
        x, y = 780 + rnd.uniform(-48, 48), 330 + rnd.uniform(-30, 26)
        g.fill(Circ(x, y, 6), sphere_paint(x - 2, y - 2, 6, fc, amb=0.5))
    # deer at the pool edge (difference)
    if "deer" not in d:
        dc, dx, db = (150, 110, 76), 650, 392
        g.fill(Ell(dx, db - 26, 24, 11), sphere_paint(dx - 4, db - 32, 26, dc, ry=13, amb=0.45))
        for lx in (-16, -9, 12, 18):
            g.fill(Seg(dx + lx, db - 20, dx + lx * 1.05, db, 3.2, 2.2), dc)
        g.fill(Seg(dx - 20, db - 30, dx - 34, db - 10, 8, 6), dc)
        g.fill(Ell(dx - 38, db - 6, 8, 5), dc)
        g.fill(Ell(dx - 26, db - 20, 4, 6), dc)
    # ferns and a backpack + mushrooms in the foreground
    fern_clump(g, 70, 600, 130, seed=2626, n=8)
    fern_clump(g, 820, 610, 140, seed=2627, n=8)
    fern_clump(g, 300, 600, 80, col=(80, 130, 56), seed=2628, n=6)
    if "pack" not in d:
        g.shadow(Box(470, 520, 504, 560), 6, 3, 6, 0.4)
        g.fill(Box(470, 516, 504, 562, 8), sphere_paint(480, 530, 28, (40, 90, 150), ry=32, amb=0.4, spec=0.1))
        g.fill(Box(474, 536, 500, 552, 3), (30, 70, 120))
    if "mush" not in d:
        for x, y, r in ((160, 560, 13), (184, 568, 9)):
            g.fill(Box(x - r * 0.25, y, x + r * 0.25, y + r * 1.1, 2), (236, 226, 206))
            g.fill(Ell(x, y, r, r * 0.6), sphere_paint(x, y - 2, r, (220, 160, 40), ry=r * 0.7, amb=0.4, spec=0.3))
    # stone cairn on the bank (difference)
    if "cairn" not in d:
        for k, (r, yy) in enumerate(((16, 540), (12, 522), (9, 508), (6, 498))):
            g.fill(Ell(620, yy, r, r * 0.55), sphere_paint(616, yy - 3, r, (140, 136, 126), ry=r * 0.6, amb=0.45))


L1526_RAYS = [dict(lx=640, ly=-160, col=(255, 246, 200), k=1.4, region=Box(-2, -2, W + 2, 150), threshold=150, soft=60,
                   density=0.9, decay=0.985, samples=80, receive=lambda X, Y: 0.4 + 0.6 * smooth(600, 300, Y))]

L1526_ELEMENTS = [
    mist_el("spray", 450, 380, 130, 20, (240, 246, 246), alpha=0.5, length=24, seed=2640),
    beam_el("beam1", 600, 0, 440, 440, 50, 120, col=(255, 246, 210), k=0.12),
    beam_el("beam2", 720, 0, 580, 420, 40, 100, col=(255, 246, 210), k=0.1, phase=0.5),
    motes_el("motes", [(480, 200), (540, 260), (600, 180), (520, 320), (660, 240)], col=(255, 250, 220), r=1.8),
    glint_el("glint", [(330, 420), (560, 430), (440, 450)], r=4, speed=0.6),
    E("leaf", el(lambda g, m: g.fill(Ell(300, 160, 6, 3.4), (200, 160, 60))), anim=dict(driftVelocity=(14, -40), driftLength=260, driftFade=True, swingAngle=40, swingSpeed=0.7)),
]

L1526_DIFFS = [
    ("bird", 192, 180, 0),
    ("flowers", 780, 330, 0),
    ("deer", 640, 366, 0),
    ("pack", 487, 538, 0),
    ("mush", 170, 566, 0),
    ("cairn", 620, 520, 0),
]


# =================================================================== Level 1527 fishing harbour at dawn
WL27 = 330


def l1527_upper(g, d):
    sky(g, [(0, (110, 120, 170)), (120, (230, 170, 170)), (250, (250, 200, 160)), (WL27, (250, 220, 190))], y1=WL27)
    sun(g, 180, 300, r=16, col=(255, 236, 200), halo=(255, 170, 120), k=0.9)
    cloud_layer(g, 40, 160, (255, 196, 170), (150, 120, 150), cover=0.38, sx=220, sy=16, seed=2701, alpha=0.75)
    # hillside town
    h27 = lambda x: 334 - 130 * smooth(240, 520, x) + (fbm1(x, 60, 3, 2702) - 0.5) * 14
    g.fill(Under(h27, -20, W + 20, WL27 + 2),
           tex(vgrad([(200, (176, 150, 140)), (WL27, (150, 130, 126))]), 0.12, 20, 10, 3, 2705))
    rnd = random.Random(2703)
    for row in range(4):
        for k in range(9):
            x = 330 + k * 62 + rnd.uniform(-10, 10) + row * 14
            base = 236 + row * 22 + rnd.uniform(-4, 4) - max(0, 6 - k) * 4 * (3 - row)
            col = rnd.choice([(230, 210, 180), (210, 150, 110), (240, 230, 210), (190, 120, 100), (220, 190, 120)])
            w, h = rnd.uniform(30, 44), rnd.uniform(18, 26)
            if base - h < float(h27(np.array([x + w / 2], F32))[0]) + 4:
                continue
            g.fill(Box(x, base - h, x + w, base), light_x(mixc(col, (240, 190, 170), 0.3), x, x + w, 1.1, 0.8))
            g.fill(Poly([(x - 3, base - h + 1), (x + w / 2, base - h - 10), (x + w + 3, base - h + 1)]), mixc((170, 80, 60), (230, 180, 160), 0.3))
            for wx in range(int(x + 5), int(x + w - 6), 10):
                g.fill(Box(wx, base - h + 6, wx + 4, base - h + 11), (90, 80, 90))
    # church tower (difference: spire)
    g.fill(Box(560, 150, 586, 232), light_x((236, 222, 200), 560, 586, 1.15, 0.8))
    g.fill(arch(567, 579, 168, 186, pointed=False), (70, 60, 70))
    if "spire" not in d:
        g.fill(Poly([(556, 152), (573, 104), (590, 152)]), light_x((90, 110, 120), 556, 590, 1.2, 0.7))
        g.fill(Seg(573, 104, 573, 92, 1.5), (60, 60, 60))
    else:
        g.fill(Ell(573, 150, 17, 14) - Box(550, 151, 600, 170), light_x((90, 110, 120), 556, 590, 1.2, 0.7))
    g.fog(200, WL27, (250, 214, 190), 0.0, 0.35)
    # breakwater + small lighthouse (right)
    g.fill(Box(640, WL27 - 14, W + 2, WL27 + 1), grain_tex(light_y((130, 120, 116), WL27 - 14, WL27, 1.2, 0.7), 0.15, 2704))
    g.fill(Box(800, 230, 822, WL27 - 14), cyl_paint(811, 11, (240, 236, 230), amb=0.5))
    for y in (246, 276):
        g.fill(Box(800, y, 822, y + 12), cyl_paint(811, 11, (200, 60, 50), amb=0.5))
    g.fill(Box(798, 220, 824, 232, 2), (60, 60, 60))
    g.fill(Box(803, 210, 819, 222), (255, 240, 200))
    g.fill(Poly([(798, 212), (811, 200), (824, 212)]), (200, 60, 50))


def boat_hull(g, x0, x1, wl, hgt, col, trim=(240, 240, 236), seed=0):
    hull = Poly([(x0, wl - hgt), (x1, wl - hgt - 8), (x1 - 20, wl + 6), (x0 + 16, wl + 6)])
    g.fill(hull, light_y(col, wl - hgt - 8, wl + 6, 1.25, 0.7))
    g.fill(Poly([(x0, wl - hgt), (x1, wl - hgt - 8), (x1, wl - hgt - 3), (x0, wl - hgt + 4)]), trim)
    # mirrored reflection blob
    g.fill(Poly([(x0 + 16, wl + 6), (x1 - 20, wl + 6), (x1, wl + hgt + 14), (x0, wl + hgt + 8)]), mixc(col, (60, 70, 80), 0.5), alpha=0.45, feather=3)
    return hull


def l1527_lower(g, d):
    water(g, WL27, H, (230, 200, 180), (60, 80, 100), seed=2710, streak=0.08)
    g.reflect(WL27, WL27, H, k=0.8, tint=(60, 70, 90), tint_k=0.2, ripple=2.4, fade=0.45, streak=0.2)
    g.blur((-2, WL27 + 2, W + 2, H), 1.6)
    ripples_light(g, WL27 + 2, H, (255, 220, 180), k=0.35, cx=180, spread=70, seed=2711)
    # fishing boat (difference: wheelhouse colour)
    wl = 404
    g.fill(Seg(430, wl - 40, 430, 230, 3), (80, 70, 60))
    g.fill(Seg(430, 236, 330, wl - 40, 1), (60, 60, 60))
    g.fill(Seg(430, 236, 540, wl - 44, 1), (60, 60, 60))
    wc = (240, 240, 236) if "cabin" not in d else (80, 140, 190)
    g.fill(Box(450, wl - 84, 516, wl - 36, 2), light_x(wc, 450, 516, 1.15, 0.8))
    g.fill(Box(444, wl - 90, 522, wl - 82, 1), (60, 70, 90))
    for wx in (458, 486):
        window_glass(g, wx, wl - 74, wx + 20, wl - 58, sky_top=(250, 200, 170), sky_bot=(90, 80, 90), frame=(240, 240, 236), bars=False)
    boat_hull(g, 290, 570, wl, 34, (180, 50, 44), seed=2712)
    g.fill(Seg(310, wl - 40, 350, wl - 70, 2), (60, 60, 60))
    for bx in (330, 380):
        g.fill(Circ(bx, wl - 22, 7), sphere_paint(bx - 2, wl - 24, 7, (240, 140, 40), amb=0.5))
    # rowboat (difference: colour)
    rc = (60, 120, 160) if "row" not in d else (230, 190, 60)
    boat_hull(g, 50, 190, 452, 16, rc, seed=2713)
    g.fill(Seg(80, 432, 160, 440, 2.5), (130, 100, 70))
    # pier (right foreground)
    for x in range(610, 900, 60):
        g.fill(Box(x, 470, x + 12, H + 2), light_x((90, 70, 54), x, x + 12, 1.2, 0.6))
        g.fill(Box(x, 520, x + 12, H + 2), (40, 70, 70), alpha=0.35)
    g.fill(Poly([(590, 470), (W + 2, 460), (W + 2, 488), (590, 496)]), planks("v", (150, 116, 84), seed=2714, width=14))
    g.mul(Poly([(590, 496), (W + 2, 488), (W + 2, 500), (590, 508)]), 0.5)
    # crates (difference: top crate), net pile (difference: colour), lifebuoy (difference)
    crate(g, 660, 432, 54, 36, seed=2715)
    crate(g, 716, 436, 50, 32, seed=2716)
    if "crate" not in d:
        crate(g, 684, 400, 50, 32, col=(140, 160, 170), seed=2717)
    nc = (220, 110, 50) if "net" not in d else (60, 150, 100)
    g.fill(Rough(Ell(830, 470, 52, 20) - Box(770, 474, 890, 500), 3, 6, 2718),
           lambda X, Y: C(nc) * (0.6 + 0.5 * np.abs(np.sin(X * 1.1) * np.sin(Y * 1.1)))[..., None])
    g.fill(Box(616, 380, 626, 470), light_x((90, 70, 54), 616, 626, 1.2, 0.6))
    if "ring" not in d:
        g.fill(Circ(621, 420, 20) - Circ(621, 420, 11), lambda X, Y: np.where((np.floor(np.arctan2(Y - 420, X - 621) / (math.pi / 4)) % 2 == 0)[..., None],
                                                                              C((240, 240, 236)), C((220, 60, 50))) * 1.0)
    # gull on a post (difference)
    g.fill(Box(876, 400, 888, 470), light_x((90, 70, 54), 876, 888, 1.2, 0.6))
    if "gull" not in d:
        gx, gy = 882, 388
        g.fill(Ell(gx, gy, 16, 9), sphere_paint(gx, gy - 2, 16, (244, 244, 240), ry=9, amb=0.55))
        g.fill(Ell(gx + 9, gy - 4, 12, 6), light_y((120, 124, 130), gy - 10, gy, 1.1, 0.8))
        g.fill(Circ(gx - 12, gy - 10, 6.5), sphere_paint(gx - 12, gy - 10, 6.5, (244, 244, 240), amb=0.6))
        g.fill(Poly([(gx - 18, gy - 10), (gx - 28, gy - 7), (gx - 18, gy - 7)]), (240, 180, 50))
        g.fill(Circ(gx - 14, gy - 11, 1.2), (20, 20, 20))
    figure(g, 760, 462, 62, (60, 80, 70), pants=(40, 40, 50), hat=(200, 170, 60))


L1527_ELEMENTS = [
    bird_el("gull1", 300, 90, s=8, speed=18, col=(250, 246, 240)),
    bird_el("gull2", 640, 130, s=7, speed=-22, col=(250, 246, 240)),
    mist_el("mist", 400, 336, 300, 8, (250, 226, 210), alpha=0.5, length=50, seed=2730),
    glint_el("glint", [(180, 360), (196, 400), (170, 440), (220, 500)], col=(255, 230, 190), r=5, speed=0.5),
    E("bob", el(lambda g, m: g.fill(Circ(240, 520, 9), sphere_paint(237, 517, 9, (240, 120, 40), amb=0.5))), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.4)),
]

L1527_DIFFS = [
    ("spire", 573, 130, 0),
    ("cabin", 483, 344, 0),
    ("row", 120, 440, 0),
    ("crate", 709, 416, 0),
    ("net", 830, 462, 0),
    ("ring", 621, 420, 0),
    ("gull", 876, 384, 0),
]


# =================================================================== Level 1528 rustic kitchen in morning light
WIN28 = (60, 80, 250, 320)
L28 = (-420, -260)


def l28_window():
    return Box(*WIN28)


def l1528_scene(g, d):
    # garden outside the window
    x0, y0, x1, y1 = WIN28
    g.fill(Box(x0, y0, x1, y1), vgrad([(y0, (220, 236, 246)), (y1, (250, 250, 236))]))
    crown(g, 120, 200, 90, 70, (150, 190, 110), seed=2801)
    crown(g, 220, 250, 70, 60, (170, 200, 120), seed=2802)
    # plaster walls + beams
    wall = Diff(Box(-2, -2, W + 2, 470), l28_window())
    g.fill(wall, tex(lgrad(0, 0, 900, 400, [(0, (214, 190, 156)), (1, (150, 120, 92))]), 0.08, 20, 16, 4, 2803))
    stains(g, wall, 0.12, sx=60, sy=60, seed=2804)
    g.fill(Box(-2, -2, W + 2, 40), planks("h", (90, 64, 44), seed=2805, width=20))
    for x in (300, 600):
        g.fill(Box(x, -2, x + 26, 40), light_x((80, 56, 38), x, x + 26, 1.2, 0.6))
    # window frame + sill
    g.fill(Diff(Box(x0 - 12, y0 - 12, x1 + 12, y1 + 6), l28_window()), light_x((236, 230, 216), x0 - 12, x1 + 12, 1.1, 0.8))
    for xm in ((x0 + x1) / 2,):
        g.fill(Box(xm - 4, y0, xm + 4, y1), (236, 230, 216))
    g.fill(Box(x0, (y0 + y1) / 2 - 4, x1, (y0 + y1) / 2 + 4), (236, 230, 216))
    g.fill(Box(x0 - 20, y1 + 4, x1 + 20, y1 + 16, 2), light_y((200, 190, 170), y1 + 4, y1 + 16, 1.2, 0.8))
    g.fill(Ell(110, y1 - 6, 16, 12), sphere_paint(106, y1 - 10, 16, (190, 100, 60), ry=12, amb=0.5))
    crown(g, 110, y1 - 30, 22, 18, (70, 120, 50), seed=2806)
    # light patch on the wall (window projected)
    g.add(Poly([(330, 170), (500, 190), (520, 420), (350, 400)]), (255, 230, 180), 0.12, feather=20)
    # copper pot rack (difference: middle pot)
    g.fill(Seg(330, 92, 620, 92, 4), (60, 50, 44))
    for k, (px, r) in enumerate(((370, 22), (440, 28), (512, 24), (580, 18))):
        if k == 2 and "pot" in d:
            continue
        g.fill(Seg(px, 92, px, 106, 1.5), (60, 50, 44))
        g.fill(Ell(px, 108 + r * 0.8, r, r * 0.85) - Box(px - r - 2, 90, px + r + 2, 108 + r * 0.2), sphere_paint(px - r * 0.3, 112 + r * 0.5, r, (196, 110, 60), amb=0.4, spec=0.6, shin=20))
        g.fill(Box(px - r, 108 + r * 0.2, px + r, 112 + r * 0.2, 1), (170, 90, 50))
        g.fill(Seg(px + r, 112, px + r + 22, 106, 4, 3), (60, 50, 44))
    # shelf with jars (difference: jar lid colour)
    g.fill(Box(320, 252, 600, 262, 2), light_y((120, 86, 56), 252, 262, 1.2, 0.7))
    for k, (jx, jh, col) in enumerate(((344, 40, (230, 200, 120)), (392, 52, (200, 90, 70)), (444, 34, (150, 170, 90)), (492, 46, (240, 230, 220)), (546, 38, (180, 120, 60)))):
        if k == 1 and "jar" in d:
            col = (240, 190, 60)
        g.fill(Box(jx - 16, 252 - jh, jx + 16, 252, 6), lambda X, Y, col=col, jx=jx: cyl_paint(jx, 16, col, amb=0.5, spec=0.5)(X, Y) * 0.9)
        g.add(Box(jx - 10, 252 - jh + 6, jx - 6, 248), (255, 255, 255), 0.25)
        lid = (180, 50, 40) if not (k == 1 and "jar" in d) else (60, 120, 180)
        g.fill(Box(jx - 17, 252 - jh - 8, jx + 17, 252 - jh + 2, 2), light_x(lid if k == 1 else (150, 120, 80), jx - 17, jx + 17, 1.2, 0.7))
    # drying herbs from the beam (difference)
    if "herbs" not in d:
        for k, hx in enumerate((660, 690, 720)):
            g.fill(Seg(hx, 40, hx, 70, 1.2), (110, 90, 60))
            for j in range(12):
                a = -0.5 + j * 0.09
                g.fill(Seg(hx, 70, hx + math.sin(a) * 30, 70 + math.cos(a) * 54, 2.2, 1.2), (100 + k * 10, 130, 70))
            g.fill(Box(hx - 4, 66, hx + 4, 74), (180, 60, 50))
    # hearth (right) with kettle (difference)
    g.fill(Box(660, 200, 900, 470), ashlar((150, 130, 110), 34, 18, 2807))
    g.fill(arch(700, 860, 330, 470, pointed=False), (34, 24, 20))
    g.glow(780, 450, 90, (255, 140, 50), 0.55, ry=50)
    for k in range(5):
        g.fill(Seg(730 + k * 20, 466, 750 + k * 20, 452, 7), (90, 60, 40))
    g.fill(Box(650, 190, 900, 206, 2), light_y((110, 80, 54), 190, 206, 1.2, 0.7))
    if "kettle" not in d:
        g.fill(Seg(780, 330, 780, 380, 1.6), (40, 40, 40))
        g.fill(Ell(780, 404, 30, 24) - Box(740, 410, 820, 440), sphere_paint(770, 396, 30, (70, 70, 74), ry=24, amb=0.3, spec=0.5))
        g.fill(Box(752, 404, 808, 418, 4), (60, 60, 64))
        g.fill(Seg(808, 400, 830, 384, 6, 3), (66, 66, 70))
    # table
    g.fill(Box(-2, 470, W + 2, H + 2), persp_floor((450, 250), 470, (150, 100, 70), tile=50, seed=2808))
    g.mul(Ell(470, 530, 330, 26), 0.5, feather=16)
    for lx in (200, 720):
        g.fill(Box(lx, 440, lx + 18, 560), light_x((100, 70, 46), lx, lx + 18, 1.2, 0.6))
    g.fill(Poly([(170, 404), (770, 404), (790, 440), (150, 440)]), planks("h", (150, 106, 70), seed=2809, width=9, x_or_y0=404))
    g.fill(Box(150, 440, 790, 452), light_y((110, 76, 50), 440, 452, 1.1, 0.7))
    # bread board, loaves, cheese
    g.fill(Ell(300, 412, 70, 12), light_y((180, 140, 96), 400, 424, 1.2, 0.8))
    for bx, rx in ((270, 34), (330, 26)):
        g.fill(Ell(bx, 398, rx, rx * 0.5) - Box(bx - rx - 2, 404, bx + rx + 2, 420), sphere_paint(bx - 8, 390, rx, (200, 130, 60), ry=rx * 0.6, amb=0.45, spec=0.15))
        for k in range(3):
            g.fill(Seg(bx - rx * 0.5 + k * rx * 0.45, 388, bx - rx * 0.3 + k * rx * 0.45, 396, 2), (230, 190, 130))
    g.fill(Poly([(380, 412), (430, 396), (436, 414)]), light_x((240, 200, 90), 380, 436, 1.1, 0.8))
    # bowl of tomatoes (difference: one tomato is green)
    g.fill(Ell(520, 410, 50, 16) - Box(460, 380, 580, 406), light_x((60, 100, 150), 470, 570, 1.2, 0.7))
    for k, (tx, ty) in enumerate(((498, 398), (520, 392), (542, 398), (510, 384), (532, 382))):
        tc = (210, 40, 30) if not (k >= 3 and "tomato" in d) else (110, 170, 60)
        g.fill(Circ(tx, ty, 11), sphere_paint(tx - 3, ty - 4, 11, tc, amb=0.4, spec=0.5))
        g.fill(Poly([(tx - 4, ty - 10), (tx, ty - 14), (tx + 4, ty - 10)]), (60, 110, 40))
    # milk jug + egg basket (difference: eggs)
    g.fill(Union([Box(612, 350, 648, 408, 10), Ell(630, 354, 18, 6)]), cyl_paint(630, 18, (236, 232, 222), amb=0.5, spec=0.3))
    g.fill(Ell(645, 376, 12, 14) - Ell(645, 376, 7, 9), (220, 216, 206))
    g.fill(Ell(710, 414, 36, 12) - Box(670, 380, 750, 410), lambda X, Y: C((176, 130, 80)) * (0.7 + 0.3 * np.abs(np.sin(X * 1.2) * np.sin(Y * 1.2)))[..., None])
    if "eggs" not in d:
        for ex, ey in ((696, 402), (714, 398), (730, 404), (706, 392)):
            g.fill(Ell(ex, ey, 7, 9), sphere_paint(ex - 2, ey - 3, 8, (236, 214, 180), ry=10, amb=0.5))
    g.fill(Seg(676, 404, 744, 404, 3), (150, 110, 70))
    # chair with a sleeping cat (difference)
    g.fill(Box(56, 400, 66, 580), light_x((110, 76, 50), 56, 66, 1.2, 0.6))
    g.fill(Box(56, 400, 160, 410, 2), (110, 76, 50))
    g.fill(Box(50, 486, 170, 498, 2), light_y((130, 90, 60), 486, 498, 1.2, 0.7))
    g.fill(Box(150, 498, 160, 580), (100, 70, 46))
    if "cat" not in d:
        cx, cy = 110, 470
        g.fill(Ell(cx, cy, 40, 17), tex(sphere_paint(cx - 8, cy - 8, 42, (200, 130, 60), ry=20, amb=0.45), 0.15, 2, 6))
        g.fill(Circ(cx - 34, cy - 4, 13), sphere_paint(cx - 38, cy - 8, 13, (200, 130, 60), amb=0.45))
        for e in (-1, 1):
            g.fill(Poly([(cx - 34 + e * 8, cy - 12), (cx - 34 + e * 10, cy - 24), (cx - 34 + e * 2, cy - 16)]), (190, 120, 56))
        g.fill(Seg(cx + 36, cy + 6, cx + 10, cy + 16, 7, 5), (190, 120, 56))
        g.fill(Seg(cx - 40, cy - 4, cx - 34, cy - 3, 1), (60, 40, 30))


L1528_RAYS = [dict(lx=L28[0], ly=L28[1], col=(255, 236, 190), k=1.3, region=l28_window(), threshold=170, soft=60,
                   density=0.85, decay=0.985, samples=80, receive=lambda X, Y: 0.3 + 0.7 * smooth(640, 400, X))]

L1528_ELEMENTS = [
    beam_el("beam", 200, 220, 460, 430, 120, 200, col=(255, 240, 200), k=0.1),
    motes_el("motes", [(300, 240), (360, 300), (420, 340), (330, 360), (400, 260)], col=(255, 246, 220), r=1.8),
    smoke_el("steam", 830, 380, r=7, col=(240, 236, 230), rise=60, wind=-6, alpha=0.4),
    E("fire", el(lambda g, m: g.glow(780, 446, 60, (255, 160, 60), 0.4, ry=30)), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=1.5)),
    E("leaves", el(lambda g, m: crown(g, 170, 150, 34, 26, (160, 200, 110), seed=2830)), pivot=(170, 176), anim=dict(swingAngle=3, swingSpeed=0.3)),
]

L1528_DIFFS = [
    ("pot", 512, 128, 0),
    ("jar", 392, 220, 0),
    ("herbs", 690, 96, 0),
    ("kettle", 784, 400, 0),
    ("tomato", 521, 383, 0),
    ("eggs", 712, 398, 0),
    ("cat", 100, 466, 0),
]


# =================================================================== Level 1529 autumn vineyard at golden hour
HZ29 = 250


def l29_rows(X, Y, y0, vp, col_a, col_b, seed):
    dd = np.maximum(Y - (y0 - 30), 4)
    xg = (X - vp) / dd
    fr = (xg / 0.3) % 1.0
    ridge_ = 1 - np.abs(fr - 0.5) * 2
    n = fbm(X, Y, 1.4 + dd * 0.03, 1.2 + dd * 0.02, 3, seed)
    vine = smooth(0.42, 0.6, ridge_ + (n - 0.5) * 0.35)
    leaf = C(col_a) + (C(col_b) - C(col_a)) * smooth(0.4, 0.7, fbm(X, Y, 30, 20, 3, seed + 1))[..., None]
    leaf = leaf * (0.65 + 0.6 * n)[..., None] * (1 + 0.2 * np.clip((0.5 - fr) * 2, -1, 1))[..., None]
    soil = C((120, 96, 66)) * (0.7 + 0.4 * fbm(X, Y, 2 + dd * 0.03, 2, 3, seed + 2))[..., None]
    return soil + (leaf - soil) * vine[..., None]


def l1529_scene(g, d):
    sky(g, [(0, (90, 120, 180)), (140, (230, 190, 150)), (HZ29, (255, 214, 150))])
    sun(g, 130, 210, r=18, col=(255, 240, 200), halo=(255, 180, 100), k=1.1)
    cloud_layer(g, 40, 160, (255, 210, 170), (170, 130, 130), cover=0.33, sx=230, sy=16, seed=2901, alpha=0.75)
    ridge(g, HZ29, 70, 260, 2902, (140, 120, 130), ridged=False, light=False, rock_tex=0.03, haze=((246, 200, 160), 0.55, 0.4))
    treeline(g, HZ29 + 6, 14, 8, 2909, (120, 110, 80), conifer=False, haze=((240, 196, 160), 0.5, 0.3))
    # rolling hill with contour vine rows + villa
    hill = lambda x: 300 - 70 * np.exp(-((x - 620) / 220.0) ** 2) + (fbm1(x, 90, 3, 2903) - 0.5) * 14
    g.fill(Under(hill, -20, W + 20, H + 20),
           lambda X, Y: (C((176, 150, 80)) + (C((200, 120, 50)) - C((176, 150, 80))) * smooth(0.45, 0.65, np.abs(np.sin((Y - hill(X[0])[None, :]) * 0.5 + X * 0.01)))[..., None])
           * (0.8 + 0.3 * fbm(X, Y, 6, 3, 3, 2904))[..., None] * light_x((255, 255, 255), 0, 900, 1.15, 0.85)(X, Y) / 255.0)
    rc = (186, 92, 60) if "roof" not in d else (80, 90, 110)
    gable_house(g, 560, 236, 110, 40, 26, (236, 214, 176), rc, seed=2905, side=(196, 170, 136), side_w=30)
    g.fill(Box(610, 166, 636, 200), light_x((236, 214, 176), 610, 636, 1.15, 0.8))
    g.fill(Poly([(606, 168), (623, 150), (640, 168)]), light_x(rc, 606, 640, 1.2, 0.7))
    for wx in (574, 600, 640):
        window_glass(g, wx, 210, wx + 12, 226, sky_top=(250, 200, 150), sky_bot=(110, 90, 80), frame=(240, 230, 210), bars=False)
    for k, x in enumerate((520, 540, 714, 734)):
        cypress(g, x, 242, 70 - k * 4, seed=2906 + k)
    g.fog(230, 320, (250, 210, 170), 0.15, 0.0)
    # near vineyard rows in perspective
    def near(x):
        return 330 + (fbm1(x, 120, 2, 2910) - 0.5) * 16
    g.fill(Under(near, -20, W + 20, H + 20), lambda X, Y: l29_rows(X, Y, 330, 520, (210, 150, 50), (190, 70, 40), 2911))
    g.add(Box(-2, HZ29, W + 2, H), (255, 170, 90), 0.05)
    # foreground vines with grape bunches (left / right)
    for x0, x1, s in ((-20, 300, 2920), (640, 920, 2921)):
        g.fill(Seg(x0, 420, x1, 430, 1), (60, 60, 60))
        for px in range(int(x0) + 40, int(x1), 120):
            g.fill(Box(px - 4, 400, px + 4, 600), light_x((110, 84, 60), px - 4, px + 4, 1.3, 0.6))
        for k in range(7):
            cx = x0 + 30 + k * (x1 - x0 - 40) / 6
            crown(g, cx, 444, 46, 32, ((210, 150, 50), (200, 100, 40), (180, 160, 60))[k % 3], seed=s + k)
    for k, (gx, gy) in enumerate(((80, 470), (180, 474), (700, 470), (840, 476))):
        col = (80, 40, 90)
        if k == 3 and "grape" in d:
            col = (170, 190, 80)
        grapes(g, gx, gy, 1.4, col, seed=2930 + k)
    # crates of grapes (difference: top crate), straw hat (difference), barrel (difference), wheelbarrow
    crate(g, 260, 520, 80, 44, seed=2940)
    crate(g, 350, 526, 76, 40, seed=2941)
    for k in range(12):
        x = 270 + (k % 6) * 12
        g.fill(Circ(x, 518 - (k // 6) * 6, 7), sphere_paint(x - 2, 514 - (k // 6) * 6, 7, (80, 40, 90), amb=0.35, spec=0.4))
    if "crate" not in d:
        crate(g, 290, 478, 76, 40, col=(160, 120, 80), seed=2942)
        for k in range(6):
            g.fill(Circ(302 + k * 11, 476, 7), sphere_paint(370 + k * 11, 472, 7, (80, 40, 90), amb=0.35, spec=0.4))
    if "hat" not in d:
        g.fill(Ell(388, 524, 30, 7), sphere_paint(382, 522, 30, (230, 200, 130), ry=7, amb=0.5))
        g.fill(Ell(388, 512, 15, 13) - Box(370, 522, 406, 540), sphere_paint(382, 508, 15, (226, 194, 120), ry=13, amb=0.5))
        g.fill(Box(373, 514, 403, 519), (60, 90, 150))
    if "barrel" not in d:
        bx, by = 560, 568
        g.mul(Ell(bx + 8, by + 24, 32, 5), 0.45, feather=5)
        g.fill(Union([Ell(bx, by, 26, 29)]) & Box(bx - 30, by - 24, bx + 30, by + 24), lambda X, Y: cyl_paint(bx, 26, (130, 86, 50), amb=0.4, spec=0.2)(X, Y)
               * (0.85 + 0.15 * np.abs(np.sin((X - bx) * 0.7)))[..., None])
        for yy in (by - 18, by - 6, by + 6, by + 18):
            g.fill(Box(bx - 25, yy, bx + 25, yy + 3), (60, 56, 56))
        g.fill(Ell(bx, by - 24, 21, 5), light_x((150, 100, 60), bx - 21, bx + 21, 1.2, 0.7))
    # wheelbarrow with a basket of grapes (difference: barrow colour)
    wc = (60, 110, 80)
    g.fill(Poly([(660, 520), (780, 520), (760, 556), (680, 556)]), light_y(wc, 520, 556, 1.2, 0.7))
    g.fill(Circ(690, 574, 18) - Circ(690, 574, 12), (40, 40, 40))
    g.fill(Seg(760, 540, 830, 560, 4), (100, 76, 50))
    g.fill(Seg(770, 556, 780, 590, 3), (60, 60, 60))
    for k in range(8):
        g.fill(Circ(680 + k * 12, 516, 8), sphere_paint(678 + k * 12, 512, 8, (80, 40, 90), amb=0.35, spec=0.4))


L1529_ELEMENTS = [
    bird_el("bird1", 300, 80, s=7, speed=20, col=(70, 50, 50)),
    bird_el("bird2", 330, 96, s=6, speed=20, col=(70, 50, 50)),
    fall_el("leaf1", 200, 300, lambda g, x, y: g.fill(Ell(x, y, 6, 3.4), (220, 130, 40)), vx=12, vy=-40, length=240, swing=40),
    fall_el("leaf2", 760, 320, lambda g, x, y: g.fill(Ell(x, y, 6, 3.4), (200, 80, 40)), vx=-8, vy=-36, length=220, phase=0.5, swing=50),
    smoke_el("smoke", 650, 160, r=5, col=(230, 210, 200), rise=40, wind=8, alpha=0.35),
    glint_el("bees", [(250, 500), (600, 470), (860, 520)], col=(255, 220, 120), r=3, speed=0.9),
]

L1529_DIFFS = [
    ("roof", 600, 220, 0),
    ("grape", 840, 490, 0),
    ("crate", 328, 492, 0),
    ("hat", 388, 516, 0),
    ("barrel", 560, 566, 0),
]


LEVELS = [
    ("Level1520", "薰衣草庄园", flat_bg(l1520_scene), L1520_ELEMENTS, L1520_DIFFS, 60, OPTS),
    ("Level1521", "水城运河", two_pass(l1521_upper, l1521_lower), L1521_ELEMENTS, L1521_DIFFS, 60, OPTS),
    ("Level1522", "珊瑚礁", make_bg(l1522_scene, L1522_RAYS, bloom=(220, 16, 0.3), grade=dict(contrast=1.05, sat=1.08)), L1522_ELEMENTS, L1522_DIFFS, 60, OPTS),
    ("Level1523", "冰川峡湾", two_pass(l1523_upper, l1523_lower), L1523_ELEMENTS, L1523_DIFFS, 60, OPTS),
    ("Level1524", "梯田晨雾", flat_bg(l1524_scene, bloom=(225, 18, 0.35)), L1524_ELEMENTS, L1524_DIFFS, 60, OPTS),
    ("Level1525", "沙漠绿洲", two_pass(l1525_upper, l1525_lower), L1525_ELEMENTS, L1525_DIFFS, 60, OPTS),
    ("Level1526", "森林瀑布", make_bg(l1526_scene, L1526_RAYS, bloom=(220, 16, 0.35), grade=dict(contrast=1.05, sat=1.05)), L1526_ELEMENTS, L1526_DIFFS, 60, OPTS),
    ("Level1527", "渔港清晨", two_pass(l1527_upper, l1527_lower), L1527_ELEMENTS, L1527_DIFFS, 60, OPTS),
    ("Level1528", "乡村厨房", make_bg(l1528_scene, L1528_RAYS, bloom=(225, 16, 0.3), grade=dict(contrast=1.05, sat=1.05)), L1528_ELEMENTS, L1528_DIFFS, 60, OPTS),
    ("Level1529", "葡萄园秋收", flat_bg(l1529_scene), L1529_ELEMENTS, L1529_DIFFS, 60, OPTS),
]
