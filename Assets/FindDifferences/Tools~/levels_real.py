# -*- coding: utf-8 -*-
"""Realistic-style levels (real.py + real_kit.py: numpy painting with soft light, textures, haze,
reflections and film grain instead of paper-craft pieces):
  Level1500 晨雾山湖   - a mountain lake at dawn: snowy peaks, pine forest, mist, cabin, dock and canoe
  Level1501 海岸灯塔   - a lighthouse on a sea cliff: keeper's house, sailboat, buoy, rocky beach, gulls
  Level1502 秋林小径   - an autumn forest path in backlit morning haze: sunbeams, bench, lamp, falling leaves
  Level1503 峡谷落日   - a desert canyon road at sunset: mesas, saguaros, telephone poles, a car, a hawk
  Level1504 雪夜小屋   - a log cabin on a snowy night: moon, aurora, snowy pines, snowman, sled, falling snow
  Level1505 麦田谷仓   - golden-hour farm: wheat field, red barn, silo, windpump, hay bales, tractor, scarecrow
  Level1506 雨夜街道   - a city street on a rainy night: lit shop, cafe sign, lamps, wet reflections, parked car
  Level1507 热带海滩   - a tropical beach: palms, turquoise shallows, outrigger boat, umbrella, sandcastle
  Level1508 窗边静物   - a still life by the window: pitcher, bottle, fruit bowl, teacup on books, flowers
  Level1509 星空露营   - camping under the Milky Way: lake, glowing tent, campfire, chairs, canoe
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (Box, C, Circ, Ctx, Diff, Ell, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm, fbm1,
                  grain_tex, hgrad, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, solid, sphere_paint, tex,
                  vgrad)
from real_kit import (bird_el, blades, bricks, broadleaf, cloud_el, cloud_layer, crown, cumulus, fall_el, figure,
                      gable_house, glint_el, grass_field, mist_el, pine, planks, ridge, ripples_light, rock, sky,
                      rock_face, smoke_el, stars, stone_wall, sun, treeline, trunk, water, window_glass)
from weather import rain_layer, snow_layer

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)


# =================================================================== Level 1500 dawn mountain lake
SHORE = 318


def l1500_upper(g, d):
    sky(g, [(0, (78, 104, 150)), (120, (150, 160, 190)), (230, (238, 196, 170)), (SHORE, (252, 214, 172))])
    sun(g, 610, 236, r=16, halo=(255, 200, 140), k=0.9)
    cloud_layer(g, 20, 150, (252, 214, 196), (150, 140, 170), cover=0.42, sx=190, sy=34, seed=11, alpha=0.85)
    if "moon" not in d:                                   # pale crescent moon in the dawn sky
        g.fill(Circ(120, 80, 16) - Circ(127, 76, 14), (250, 244, 236), alpha=0.85)
    # far range with snow, then nearer darker range
    ridge(g, 268, 150, 230, 3, (120, 128, 160), snow=(172, (240, 238, 248)), haze=((214, 190, 190), 0.3, 0.62))
    ridge(g, 300, 110, 150, 8, (70, 84, 96), snow=(205, (226, 228, 240)), haze=((200, 176, 176), 0.12, 0.4))
    g.fog(220, 310, (240, 206, 190), 0.0, 0.45)
    treeline(g, SHORE - 4, 34, 9, 21, (36, 54, 50), haze=((190, 170, 170), 0.35, 0.15))
    treeline(g, SHORE + 2, 24, 12, 22, (26, 40, 36), haze=((170, 150, 150), 0.15, 0.05))
    # cabin on the far right shore
    roof = (150, 52, 40) if "roof" not in d else (60, 96, 70)
    h = gable_house(g, 690, SHORE + 2, 70, 30, 24, (128, 92, 64), roof, seed=5, side=(96, 70, 50), side_w=22,
                    wall_paint=planks("h", (128, 92, 64), seed=6, width=5, x_or_y0=SHORE))
    window_glass(g, 702, SHORE - 20, 716, SHORE - 8, lit=(255, 196, 110), sky_top=(120, 120, 140), sky_bot=(60, 60, 70), frame=(210, 200, 180))
    window_glass(g, 740, SHORE - 20, 754, SHORE - 8, lit=(255, 196, 110), frame=(210, 200, 180))
    g.fill(Box(744, SHORE - 64, 752, SHORE - 34), light_x((90, 80, 76), 744, 752))       # chimney
    for x in (650, 790, 812, 640):
        pine(g, x, SHORE + 4, 70 + (x % 7) * 6, col=(30, 50, 42), seed=x)


def l1500_bg(c, d):
    g = Ctx(c)
    l1500_upper(g, set())           # the lake mirrors the unmodified shore, so differences are not doubled
    g.snapshot("s")
    l1500_upper(g, d)
    # lake with reflection
    water(g, SHORE, 470, (200, 180, 176), (70, 90, 110), seed=31)
    g.reflect(SHORE, SHORE, 470, k=0.78, tint=(40, 60, 80), tint_k=0.22, ripple=2.6, fade=0.5, streak=0.25)
    ripples_light(g, SHORE + 2, 460, (255, 220, 180), k=0.55, cx=610, spread=60)
    g.fog(SHORE - 6, SHORE + 30, (236, 210, 200), 0.35, 0.0)
    # small island with pines
    g.fill(Rough(Ell(250, 374, 70, 9), 3, 18, 41), tex((50, 56, 46), 0.2, 6, 3))
    for k, (x, hh) in enumerate(((215, 50), (238, 66), (262, 58), (286, 40))):
        if k == 2 and "isle" in d:
            continue
        pine(g, x, 374, hh, col=(30, 48, 40), seed=60 + k)
    # canoe on the water
    can = (176, 50, 36) if "canoe" not in d else (220, 180, 50)
    g.mul(Ell(500, 434, 56, 6), 0.35, feather=6)
    g.fill(Poly([(448, 422), (552, 422), (542, 434), (458, 434)]), light_y(can, 420, 434, 1.2, 0.7))
    g.fill(Box(452, 419, 548, 423, 2), (230, 210, 170))
    g.fill(Ell(500, 414, 8, 9), (60, 80, 110))                      # paddler
    g.fill(Circ(500, 400, 6), (220, 180, 150))
    g.fill(Seg(478, 442, 524, 396, 2.4), (110, 80, 50))
    # foreground shore: grass, rocks, dock
    def fy(x):
        return 470 + 14 * np.sin(x * 0.012) + (fbm1(x, 50, 3, 7) - 0.5) * 22
    g.fill(Under(fy, -10, W + 10, H + 10), vgrad([(450, (110, 116, 70)), (600, (60, 70, 36))]))
    grass_field(g, 470, 600, (70, 84, 40), (120, 124, 76), seed=51)
    # dock (left)
    g.fill(Poly([(20, 456), (300, 456), (330, 476), (0, 476)]), planks("v", (150, 116, 82), seed=9, width=12))
    g.mul(Box(0, 476, 330, 488), 0.5, feather=6)
    for x in (30, 110, 190, 270):
        g.fill(Box(x, 470, x + 9, 520), light_x((90, 70, 52), x, x + 9))
    post_col = (90, 70, 52)
    if "lantern" not in d:
        g.fill(Box(290, 410, 296, 458), light_x(post_col, 290, 296))
        g.fill(Box(284, 398, 302, 414, 2), (50, 46, 44))
        g.fill(Box(287, 401, 299, 411), (255, 210, 120))
        g.glow(293, 406, 22, (255, 190, 100), 0.6)
    rock(g, 520, 500, 46, 24, (128, 124, 116), seed=71, moss=(90, 110, 60))
    rock(g, 580, 516, 26, 14, (118, 114, 108), seed=72)
    if "rock" not in d:
        rock(g, 856, 520, 40, 22, (124, 120, 112), seed=73, moss=(96, 112, 60))
    # birch-ish tree on the right foreground
    trunk(g, 870, 600, 878, 300, 16, 9, (214, 210, 200), seed=81)
    for y in range(320, 590, 23):
        g.fill(Rough(Box(864 + (y % 3), y, 878, y + 3.5), 1, 3, y), (60, 56, 50))
    crown(g, 880, 250, 70, 80, (110, 140, 70), seed=82)
    crown(g, 846, 300, 34, 30, (120, 150, 72), seed=83)
    blades(g, 520, 600, (90, 110, 50), n=380, seed=91)
    # backpack on the dock
    bp = (60, 110, 160) if "bag" not in d else (200, 120, 40)
    g.shadow(Box(46, 452, 78, 458), 6, 2, 4, 0.4)
    g.fill(Box(46, 422, 78, 458, 6), sphere_paint(56, 434, 24, bp, ry=28, amb=0.4, spec=0.1, shin=8))
    g.fill(Box(50, 438, 74, 452, 3), mixc(bp, (0, 0, 0), 0.25))
    g.bloom(220, 18, 0.35)
    g.grade(contrast=1.05, sat=1.02, warm=4)
    g.commit()


L1500_ELEMENTS = [
    mist_el("mist1", 70, 320, 80, 7, (240, 214, 206), alpha=0.55, length=40),
    mist_el("mist2", 520, 322, 150, 8, (240, 214, 206), alpha=0.45, length=60, seed=6),
    bird_el("bird1", 300, 90, s=6, speed=22, col=(60, 50, 60)),
    bird_el("bird2", 330, 104, s=5, speed=22, col=(60, 50, 60), phase=0.0),
    glint_el("glint", [(600, 360), (626, 380), (612, 410)], r=5, speed=0.6),
    smoke_el("smoke", 748, SHORE - 70, r=6, col=(210, 200, 200), rise=50, wind=8),
]

L1500_DIFFS = [
    ("moon", 118, 80, 0),
    ("roof", 725, 300, 0),
    ("isle", 262, 346, 0),
    ("canoe", 500, 425, 0),
    ("lantern", 293, 428, 0),
    ("rock", 856, 520, 0),
    ("bag", 62, 440, 0),
]


# =================================================================== Level 1501 lighthouse on a sea cliff
HZ1 = 250


def l1501_cliff(x):
    return 292 + np.maximum(0, 640 - x) * 2.6 + (fbm1(x, 30, 3, 15) - 0.5) * 12


def l1501_bg(c, d):
    g = Ctx(c)
    sky(g, [(0, (52, 108, 190)), (150, (120, 170, 220)), (HZ1, (196, 220, 236))])
    cumulus(g, 160, 90, 150, 46, seed=12)
    cumulus(g, 520, 60, 120, 34, seed=13, alpha=0.85)
    cloud_layer(g, 150, 230, (250, 250, 250), (200, 210, 225), cover=0.4, sx=200, sy=20, seed=14, alpha=0.7)
    # distant headland (left)
    ridge(g, HZ1 + 4, 46, 260, 16, (96, 120, 110), x0=-20, x1=420, ridged=False, haze=((176, 200, 216), 0.55, 0.35))
    g.snapshot("s")
    water(g, HZ1, H, (110, 160, 196), (26, 74, 112), seed=17, streak=0.18)
    g.reflect(HZ1 + 2, HZ1 + 2, HZ1 + 34, x0=-2, x1=420, k=0.5, tint=(60, 110, 150), tint_k=0.45, fade=1.0, ripple=2)
    ripples_light(g, HZ1 + 2, H, (255, 255, 245), k=0.32, seed=18)
    # whitecaps
    (j0, j1, i0, i1), X, Y = g.win((0, HZ1 + 20, W, H), pad=0)
    wc = smooth(0.74, 0.86, fbm(X, Y, 22 + (Y - HZ1) * 0.25, 2 + (Y - HZ1) * 0.03, 4, 19))
    g.img[j0:j1, i0:i1] += (250 - g.img[j0:j1, i0:i1]) * (wc * 0.7)[..., None]
    # sailboat
    g.fill(Poly([(178, 318), (276, 318), (264, 332), (190, 332)]), light_y((40, 46, 60), 318, 332, 1.2, 0.7))
    g.fill(Box(226, 214, 229, 320), (90, 80, 70))
    sail = (246, 244, 236) if "sail" not in d else (230, 120, 60)
    g.fill(Poly([(231, 218), (231, 314), (276, 314)]), light_x(sail, 231, 276, 1.05, 0.82))
    g.fill(Poly([(224, 224), (224, 312), (184, 312)]), light_x((240, 238, 228), 184, 224, 1.05, 0.85))
    g.mul(Ell(227, 334, 56, 4), 0.35, feather=4)
    # buoy
    if "buoy" not in d:
        bx, by = 480, 440
        g.fill(Poly([(bx - 13, by), (bx + 13, by), (bx + 6, by - 36), (bx - 6, by - 36)]), light_x((200, 50, 40), bx - 13, bx + 13, 1.25, 0.7))
        g.fill(Box(bx - 12, by - 14, bx + 12, by - 8), (240, 240, 230))
        g.fill(Box(bx - 2, by - 52, bx + 2, by - 34), (60, 60, 60))
        g.fill(Ell(bx, by + 2, 20, 4), (230, 240, 245), alpha=0.6)
    # distant airliner high in the sky
    if "plane" not in d:
        g.fill(Seg(96, 66, 150, 58, 4, 3), (236, 238, 242))
        g.fill(Poly([(118, 62), (128, 61), (116, 76), (110, 76)]), (210, 214, 222))
        g.fill(Poly([(144, 59), (150, 58), (152, 50), (148, 50)]), (210, 214, 222))
        g.add(Seg(150, 58, 330, 34, 2.5, 4), (255, 255, 255), 0.35, feather=2)
    # cliff with grass cap
    cliff = Under(l1501_cliff, 470, W + 20, H + 20)
    g.fill(cliff, rock_face((136, 120, 102), seed=21))
    (j0, j1, i0, i1), X, Y = g.win(cliff.bbox(), pad=0)
    top = l1501_cliff(X[0])[None, :]
    lit_k = np.clip(1.15 - (Y - top) / 600, 0.6, 1.2) * np.clip(0.8 + (X - 470) / 900, 0.8, 1.2)
    g.img[j0:j1, i0:i1] *= np.where(Y > top, lit_k, 1.0)[..., None]
    g.fill(Diff(cliff, Under(lambda x: l1501_cliff(x) + 14 + (fbm1(x, 9, 3, 23) - 0.5) * 12, 470, W + 20, H + 20)),
           tex((96, 128, 60), 0.25, 3, 6, 3, 24))
    # surf at the cliff foot
    (j0, j1, i0, i1), X, Y = g.win((470, 420, 720, H), pad=0)
    top = l1501_cliff(X[0])[None, :]
    edge = np.clip(1 - np.abs(Y - top) / 30, 0, 1) * (Y < top + 4)
    fm = edge * smooth(0.4, 0.7, fbm(X, Y, 10, 5, 4, 25))
    g.img[j0:j1, i0:i1] += (248 - g.img[j0:j1, i0:i1]) * fm[..., None]
    # lighthouse
    lx, lb, lt = 720, 300, 120
    g.mul(Ell(lx + 30, lb, 40, 6), 0.5, feather=6)

    def tower(y0, y1):
        t0, t1 = (y0 - lt) / (lb - lt), (y1 - lt) / (lb - lt)
        w0, w1 = 15 + 9 * t0, 15 + 9 * t1
        return Poly([(lx - w0, y0), (lx + w0, y0), (lx + w1, y1), (lx - w1, y1)])
    g.fill(tower(lt, lb), cyl_paint(lx, 24, (246, 244, 238), amb=0.45, spec=0.12))
    band = (196, 44, 40) if "stripe" not in d else (40, 90, 170)
    for y0, y1 in ((150, 172), (206, 230), (262, 284)):
        g.fill(tower(y0, y1), cyl_paint(lx, 24, band if y0 == 206 else (196, 44, 40), amb=0.42, spec=0.1))
    g.fill(Box(lx - 22, 112, lx + 22, 120), light_x((40, 40, 44), lx - 22, lx + 22))         # gallery
    for k in range(-20, 22, 5):
        g.fill(Box(lx + k, 102, lx + k + 1.4, 112), (40, 40, 44))
    g.fill(Box(lx - 22, 100, lx + 22, 103), (40, 40, 44))
    g.fill(Box(lx - 12, 88, lx + 12, 112), lgrad(lx - 12, 88, lx + 12, 112, [(0, (255, 248, 210)), (1, (220, 190, 120))]))
    g.fill(Box(lx - 1, 88, lx + 1, 112), (50, 50, 54))
    g.fill(Ell(lx, 88, 15, 10), sphere_paint(lx, 86, 15, (180, 40, 36), ry=10))
    g.fill(Box(lx - 16, 86, lx + 16, 89), (40, 40, 44))
    g.fill(Seg(lx, 78, lx, 66, 2), (40, 40, 44))
    g.glow(lx, 100, 30, (255, 240, 200), 0.35)
    for y in (180, 240):
        g.fill(Box(lx - 3, y, lx + 3, y + 10, 1), (60, 70, 90))
    # sea cave at the foot of the cliff
    if "cave" not in d:
        g.fill(Rough(Ell(770, 560, 40, 46) - Box(700, 572, 840, 620), 3, 8, 26), lgrad(770, 514, 770, 572, [(0, (30, 26, 24)), (1, (60, 66, 70))]))
        g.mul(Ell(770, 556, 52, 54), 0.25, feather=10)
    # keeper's house
    door = (60, 90, 140)
    gable_house(g, 790, 304, 92, 40, 30, (238, 234, 224), (176, 60, 44), seed=31)
    g.fill(Box(828, 276, 846, 304), light_x(door, 828, 846))
    window_glass(g, 800, 274, 818, 290, frame=(250, 250, 250))
    window_glass(g, 856, 274, 874, 290, frame=(250, 250, 250))
    # fence along the cliff edge
    for k, x in enumerate(range(600, 700, 16)):
        if "fence" in d and 2 <= k <= 5:
            continue
        g.fill(Box(x, 280, x + 4, 306), light_x((240, 236, 226), x, x + 4))
    rail_end = 632 if "fence" in d else 694
    g.fill(Box(600, 284, rail_end, 287), (230, 226, 216))
    g.fill(Box(600, 294, rail_end, 297), (230, 226, 216))
    # rocky beach (bottom left)
    def beach(x):
        return 520 + (fbm1(x, 60, 3, 33) - 0.5) * 30 + x * 0.05
    g.fill(Under(beach, -10, 480, H + 10), grain_tex(vgrad([(500, (210, 196, 166)), (600, (176, 160, 130))]), 0.12, 3))
    (j0, j1, i0, i1), X, Y = g.win((-10, 490, 480, H), pad=0)
    top = beach(X[0])[None, :]
    wet = np.clip(1 - (Y - top) / 14, 0, 1) * (Y > top)
    g.img[j0:j1, i0:i1] *= (1 - wet * 0.25)[..., None]
    rock(g, 80, 556, 60, 30, (110, 104, 96), seed=41, wet=True)
    rock(g, 260, 566, 44, 22, (120, 112, 100), seed=42)
    rock(g, 380, 548, 30, 16, (116, 110, 100), seed=43)
    if True:
        pts = []
        for i in range(10):
            a = i * math.pi / 5 - math.pi / 2
            rr = 21 if i % 2 == 0 else 8.5
            pts.append((176 + rr * math.cos(a), 578 + rr * math.sin(a)))
        g.fill(Poly(pts), sphere_paint(176, 578, 21, (232, 120, 50), amb=0.5))
    if "gull" not in d:
        gull_c, gx, gy = (244, 244, 240), 262, 528
        g.fill(Ell(gx, gy, 18, 10), sphere_paint(gx, gy - 2, 18, gull_c, ry=10, amb=0.55))
        g.fill(Ell(gx + 11, gy - 5, 14, 7), light_y((120, 124, 130), gy - 12, gy, 1.1, 0.8))
        g.fill(Poly([(gx + 22, gy - 6), (gx + 34, gy - 2), (gx + 22, gy)]), (40, 40, 44))
        g.fill(Circ(gx - 14, gy - 12, 7.5), sphere_paint(gx - 14, gy - 12, 7.5, gull_c, amb=0.6))
        g.fill(Circ(gx - 16, gy - 13, 1.4), (20, 20, 20))
        g.fill(Poly([(gx - 21, gy - 12), (gx - 32, gy - 9), (gx - 21, gy - 9)]), (240, 180, 50))
        for dx in (-3, 4):
            g.fill(Seg(gx + dx, gy + 8, gx + dx, gy + 18, 2), (230, 170, 60))
    g.grade(contrast=1.05, sat=1.06)
    g.commit()


L1501_ELEMENTS = [
    cloud_el("cloud1", 380, 150, 90, 24, speed=5, alpha=0.75, seed=51),
    bird_el("gull1", 420, 160, s=8, speed=-18, col=(250, 250, 250)),
    bird_el("gull2", 600, 60, s=6, speed=-24, col=(240, 240, 240), phase=200),
    glint_el("glint", [(340, 300), (100, 420), (580, 470), (420, 280)], r=4, speed=0.5),
]

L1501_DIFFS = [
    ("plane", 124, 64, 0),
    ("stripe", 720, 218, 0),
    ("sail", 252, 280, 0),
    ("buoy", 480, 420, 0),
    ("fence", 660, 292, 0),
    ("cave", 770, 540, 0),
    ("gull", 262, 524, 0),
]


# =================================================================== Level 1502 autumn forest path
def l1502_bg(c, d):
    g = Ctx(c)
    g.fill(Box(-2, -2, W + 2, H + 2), rgrad(560, 180, 700, [(0, (255, 240, 200)), (0.45, (220, 170, 110)), (1, (110, 70, 40))]))
    # far hazy canopy and trunks (three depths)
    cloud_layer(g, -40, 260, (240, 190, 110), (180, 110, 60), cover=0.65, sx=60, sy=40, seed=61, alpha=0.75)
    rnd = random.Random(62)
    for depth, (n, wmin, wmax, haze) in enumerate(((26, 4, 8, 0.7), (16, 8, 14, 0.5), (9, 14, 22, 0.3))):
        for _ in range(n):
            x = rnd.uniform(-20, W + 20)
            w = rnd.uniform(wmin, wmax)
            dx = rnd.uniform(-6, 6)
            base = 330 + depth * 18 + rnd.uniform(-6, 6)
            if 380 < x < 560 and depth == 2:
                continue
            col = mixc((70, 52, 40), (240, 210, 160), haze)
            g.fill(Seg(x, base, x + dx, -20, w, w * 0.7), light_x(col, x - w / 2, x + w / 2, 1.15, 0.85))
        cloud_layer(g, -40, 200 + depth * 30, mixc((230, 140, 50), (255, 220, 160), haze * 0.8),
                    mixc((150, 70, 30), (220, 170, 120), haze), cover=0.45 + depth * 0.05, sx=50 - depth * 8,
                    sy=36 - depth * 6, seed=63 + depth, alpha=0.85)
    g.fog(230, 360, (250, 220, 170), 0.0, 0.45)
    # forest floor with leaf litter
    g.fill(Box(-2, 330, W + 2, H + 2), vgrad([(330, (200, 150, 90)), (600, (120, 70, 36))]))
    (j0, j1, i0, i1), X, Y = g.win((-2, 330, W + 2, H), pad=0)
    t = np.clip((Y - 330) / 270, 0, 1)
    n = fbm(X, Y, 3 + 9 * t, 2 + 5 * t, 4, 64)
    n2 = fbm(X, Y, 6 + 14 * t, 4 + 8 * t, 3, 65)
    sub = g.img[j0:j1, i0:i1]
    leaf = np.stack([np.full_like(n, 230), 120 + 80 * n2, 40 + 20 * n], -1)
    sub += (leaf - sub) * (smooth(0.55, 0.7, n) * 0.7)[..., None]
    sub *= (0.75 + 0.45 * n)[..., None]
    # path
    path = Rough(Poly([(300, H + 4), (680, H + 4), (520, 420), (478, 336), (462, 336), (430, 420)]), 6, 14, 66)
    g.fill(path, grain_tex(vgrad([(336, (226, 196, 150)), (600, (168, 128, 86))]), 0.12, 67), feather=1.5)
    (j0, j1, i0, i1), X, Y = g.win(path.bbox(), pad=0)
    pm = g.cover(path, X, Y)
    lv = smooth(0.66, 0.74, fbm(X, Y, 3 + (Y - 330) / 30, 2 + (Y - 330) / 50, 3, 68))
    g.img[j0:j1, i0:i1] += (np.array([220, 110, 40], np.float32) - g.img[j0:j1, i0:i1]) * (pm * lv * 0.8)[..., None]
    # sunbeams
    for k, (xa, xb) in enumerate(((560, 590), (620, 670), (700, 730), (480, 500))):
        g.add(Poly([(xa, -10), (xb, -10), (xb - 260 - k * 40, H), (xa - 330 - k * 40, H)]), (255, 230, 170), 0.08, feather=14)
    # big trunks (left + right)
    for x, w, s, b in ((60, 70, 71, H + 20), (830, 84, 72, H + 20), (700, 26, 73, 420)):
        g.fill(Seg(x, b, x + 6, -20, w, w * 0.8), tex(light_x((92, 70, 52), x - w / 2, x + w / 2, 1.1, 0.45), 0.3, 2.2, 14, 4, s))
        g.mul(Ell(x + 10, min(b, H) - 6, w * 0.9, 10 * w / 70), 0.4, feather=8 * w / 70)
    crown(g, 120, -10, 220, 90, (220, 120, 40), seed=74)
    crown(g, 820, -20, 200, 90, (230, 150, 40), seed=75)
    # birdhouse on the right trunk
    if "birdhouse" not in d:
        g.shadow(Box(790, 210, 818, 246), 6, 4, 5, 0.4)
        g.fill(Box(790, 210, 818, 246), light_x((170, 120, 70), 790, 818))
        g.fill(Poly([(784, 212), (804, 190), (824, 212)]), light_x((110, 60, 40), 784, 824))
        g.fill(Circ(804, 226, 5), (40, 26, 20))
    # lamp post (left of path)
    g.fill(Box(318, 300, 324, 470), cyl_paint(321, 3, (50, 50, 52)))
    g.fill(Box(312, 466, 330, 474, 2), (40, 40, 42))
    lamp = (255, 214, 140) if "lamp" not in d else (120, 140, 150)
    g.fill(Poly([(308, 282), (334, 282), (330, 306), (312, 306)]), lamp)
    g.fill(Poly([(304, 284), (321, 268), (338, 284)]), (46, 46, 48))
    g.fill(Box(310, 304, 332, 308), (46, 46, 48))
    if "lamp" not in d:
        g.glow(321, 294, 40, (255, 200, 120), 0.45)
    # deer in the hazy distance at the end of the path
    if "deer" not in d:
        dc = (150, 116, 84)
        dx, db = 560, 336
        g.fill(Ell(dx, db - 22, 18, 8), dc)
        for lx in (-12, -6, 9, 14):
            g.fill(Seg(dx + lx, db - 18, dx + lx * 1.05, db, 2.4, 1.6), dc)
        g.fill(Seg(dx + 14, db - 26, dx + 22, db - 40, 5, 4), dc)
        g.fill(Ell(dx + 25, db - 42, 6, 4), dc)
        for a in (-1, 1):
            g.fill(Seg(dx + 22, db - 46, dx + 20 + a * 7, db - 58, 1.4), (120, 96, 74))
        g.fill(Box(dx - 30, db - 60, dx + 40, db + 2), (250, 222, 176), alpha=0.35)
    # signpost
    g.fill(Box(196, 400, 203, 500), light_x((120, 90, 60), 196, 203))
    sgn = [(150, 410), (232, 410), (246, 422), (232, 434), (150, 434)]
    g.shadow(Poly(sgn), 4, 4, 4, 0.35)
    g.fill(Poly(sgn), planks("h", (176, 130, 84), seed=76, width=8, x_or_y0=410))
    # mushrooms by the left trunk
    cap = (196, 50, 36) if "mush" not in d else (150, 110, 70)
    for x, y, r in ((118, 566, 14), (142, 574, 10), (100, 580, 8)):
        g.fill(Box(x - r * 0.25, y, x + r * 0.25, y + r * 1.1, 2), (236, 226, 206))
        g.fill(Ell(x, y, r, r * 0.6), sphere_paint(x, y - 2, r, cap, ry=r * 0.7, amb=0.4, spec=0.3))
        if "mush" not in d:
            for a in (0.3, 1.6, 2.6):
                g.fill(Circ(x + r * 0.5 * math.cos(a), y - r * 0.25 * math.sin(a) - 1, r * 0.13), (250, 240, 230))
    # bench (right of the path)
    bc = (150, 96, 56)
    g.mul(Ell(690, 524, 90, 8), 0.45, feather=8)
    for x in (622, 752):
        g.fill(Box(x, 470, x + 6, 522), (40, 40, 42))
    g.fill(Box(610, 480, 770, 488, 2), light_y(bc, 480, 488, 1.2, 0.8))
    g.fill(Box(610, 490, 770, 496, 2), light_y(bc, 490, 496, 1.1, 0.75))
    for y in (446, 458):
        g.fill(Box(612, y, 768, y + 8, 2), planks("h", bc, seed=77, width=8, x_or_y0=y))
    # knitted hat left on the bench
    if "hat" not in d:
        g.shadow(Ell(742, 478, 18, 4), 4, 2, 4, 0.4)
        g.fill(Ell(742, 470, 18, 14) - Box(720, 478, 764, 500), tex(sphere_paint(742, 470, 18, (40, 110, 170), ry=14, amb=0.45), 0.12, 1.5, 3))
        g.fill(Box(724, 474, 760, 480, 2), (230, 230, 220))
        g.fill(Circ(742, 454, 6), sphere_paint(742, 454, 6, (240, 240, 232), amb=0.6))
    # fallen log with a backpack leaning on it
    g.fill(Seg(470, 580, 300, 560, 24, 22), tex(cyl_paint(570, 12, (110, 80, 56), horizontal=True), 0.25, 14, 1.5, 4, 78))
    g.fill(Ell(470, 580, 7, 12), rgrad(470, 580, 10, [(0, (210, 170, 120)), (1, (150, 100, 60))]))
    if "pack" not in d:
        g.shadow(Box(420, 540, 452, 580), 8, 2, 6, 0.4)
        g.fill(Box(420, 536, 452, 582, 8), sphere_paint(430, 550, 26, (170, 50, 40), ry=30, amb=0.4, spec=0.1))
        g.fill(Box(424, 556, 448, 572, 3), (130, 36, 30))
        g.fill(Seg(426, 538, 446, 538, 3), (60, 40, 30))
    blades(g, 540, 600, (130, 110, 50), n=160, seed=79, hmax=20)
    g.bloom(215, 20, 0.4)
    g.grade(contrast=1.06, sat=1.08, warm=6)
    g.commit()


def l1502_leaf(col):
    def one(g, x, y):
        g.fill(Ell(x, y, 6, 3.4), light_x(col, x - 6, x + 6, 1.2, 0.8))
        g.fill(Seg(x - 6, y, x + 6, y, 0.8), mixc(col, (60, 30, 10), 0.4))
    return one


L1502_ELEMENTS = [
    fall_el("leaf1", 300, 120, l1502_leaf((220, 110, 30)), vx=14, vy=-50, length=260, swing=40),
    fall_el("leaf2", 560, 80, l1502_leaf((240, 170, 40)), vx=-10, vy=-46, length=300, phase=0.4, swing=50),
    fall_el("leaf3", 760, 140, l1502_leaf((200, 80, 30)), vx=8, vy=-40, length=220, phase=0.7, swing=40),
    fall_el("leaf4", 160, 200, l1502_leaf((230, 140, 40)), vx=10, vy=-44, length=240, phase=0.2, swing=60),
    E("beam", el(lambda g, m: g.add(Poly([(640, 0), (680, 0), (430, 600), (360, 600)]), (255, 236, 190), 0.12, feather=18)),
      daynight="untinted", anim=dict(twinkle=0.7, twinkleSpeed=0.2)),
]

L1502_DIFFS = [
    ("birdhouse", 804, 222, 0),
    ("lamp", 321, 292, 0),
    ("deer", 566, 316, 0),
    ("mush", 120, 570, 0),
    ("hat", 742, 466, 0),
    ("pack", 436, 560, 0),
]


# =================================================================== Level 1503 canyon road at sunset
HZ3 = 300


def mesa(x0, x1, top, base, slope=18, seed=0):
    def f(x):
        e = np.minimum(np.clip((x - x0) / slope, 0, 1), np.clip((x1 - x) / slope, 0, 1))
        n = (fbm1(x, 14, 3, seed) - 0.5) * 6
        return base - (base - top) * e ** 0.6 + n * e
    return f


def strata(base, light, seed):
    def f(X, Y):
        n = fbm(X, Y, 120, 3.0, 4, seed)
        band = 0.82 + 0.3 * n + 0.08 * np.sin(Y * 0.55 + n * 6)
        out = C(base) * band[..., None]
        out = out * light(X, Y)[..., None]
        return out * (1 + 0.15 * (fbm(X, Y, 4, 10, 3, seed + 1) - 0.5))[..., None]
    return f


def cactus(g, x, base, h, arms, seed, col=(70, 104, 60)):
    w = h * 0.12
    g.mul(Ell(x + 18, base, h * 0.3, 5), 0.45, feather=6)
    g.fill(Box(x - w, base - h, x + w, base, w), tex(cyl_paint(x, w, col, amb=0.35, spec=0.15), 0.25, 1.2, 10, 3, seed))
    for side, ay, ah in arms:
        ax = x + side * w * 2.6
        g.fill(Box(min(x, ax) - w * 0.7, base - h * ay - w * 0.7, max(x, ax) + w * 0.7, base - h * ay + w * 0.7, w * 0.7),
               tex(cyl_paint(base - h * ay, w * 0.7, col, horizontal=True), 0.2, 6, 1.2, 3, seed + 1))
        g.fill(Box(ax - w * 0.75, base - h * ay - h * ah, ax + w * 0.75, base - h * ay + w * 0.3, w * 0.75),
               tex(cyl_paint(ax, w * 0.75, col, amb=0.35, spec=0.15), 0.25, 1.2, 10, 3, seed + 2))


def l1503_bg(c, d):
    g = Ctx(c)
    sky(g, [(0, (40, 46, 100)), (120, (130, 80, 120)), (230, (240, 130, 70)), (HZ3, (255, 196, 120))])
    sun(g, 420, 276, r=22, halo=(255, 150, 70), k=1.0)
    cloud_layer(g, 40, 170, (255, 170, 110), (120, 60, 90), cover=0.45, sx=220, sy=16, seed=81, alpha=0.8)
    if "moon" not in d:
        g.glow(120, 90, 40, (255, 230, 220), 0.25)
        g.fill(Circ(120, 90, 15), sphere_paint(120, 90, 15, (250, 236, 226), amb=0.8, spec=0.0))
    if "balloon" not in d:                                # distant hot-air balloon catching the last light
        bx, by = 700, 150
        g.fill(Ell(bx, by, 20, 24) | Poly([(bx - 16, by + 12), (bx + 16, by + 12), (bx + 5, by + 32), (bx - 5, by + 32)]),
               sphere_paint(bx - 2, by + 2, 22, (230, 90, 60), ry=28, amb=0.35))
        for k in (-1, 1):
            g.fill(Seg(bx + k * 4, by + 32, bx + k * 3, by + 40, 0.8), (60, 40, 40))
        g.fill(Box(bx - 4, by + 39, bx + 4, by + 46, 1), (90, 60, 40))
    # far mesas (hazy purple)
    for x0, x1, top, seed in ((-40, 260, 214, 82), (300, 380, 240, 83), (540, 940, 200, 84)):
        f = mesa(x0, x1, top, HZ3 + 4, 26, seed)
        g.fill(Under(f, x0 - 10, x1 + 10, HZ3 + 6), strata((150, 90, 110), lambda X, Y: np.full(X.shape, 0.9, np.float32), seed))
    g.fog(190, HZ3, (240, 160, 120), 0.35, 0.55)
    # mid buttes: sunlit left faces, shaded right faces
    for x0, x1, top, base, seed in ((40, 230, 246, 360, 85), (640, 880, 232, 372, 86)):
        f = mesa(x0, x1, top, base, 20, seed)
        lightf = (lambda xa, xb: lambda X, Y: (1.25 - 0.63 * smooth(-6, 6, X - (xa + (xb - xa) * 0.62) + (fbm(X, Y, 10, 14, 3, 7) - 0.5) * 30)).astype(np.float32))(x0, x1)
        g.fill(Under(f, x0 - 10, x1 + 10, base + 4), strata((190, 96, 56), lightf, seed))
    # desert floor
    g.fill(Box(-2, HZ3, W + 2, H + 2), vgrad([(HZ3, (220, 150, 100)), (420, (190, 120, 76)), (600, (150, 90, 56))]))
    (j0, j1, i0, i1), X, Y = g.win((-2, HZ3, W + 2, H), pad=0)
    t = np.clip((Y - HZ3) / 300, 0, 1)
    g.img[j0:j1, i0:i1] *= (0.82 + 0.3 * fbm(X, Y, 8 + 50 * t, 2 + 10 * t, 4, 87))[..., None]
    rnd = random.Random(88)
    for _ in range(70):
        y = rnd.uniform(HZ3 + 4, H)
        x = rnd.uniform(0, W)
        s = 1.5 + (y - HZ3) / 30
        if abs(x - 460) < 40 + (y - HZ3) * 1.1:
            continue
        g.fill(Rough(Ell(x, y, s * 2.2, s), s * 0.4, s, int(x)), tex((90, 86, 50), 0.3, 1.5, 1.5, 2))
    # road to the vanishing point (460, HZ3)
    g.fill(Poly([(450, HZ3), (470, HZ3), (760, H + 4), (170, H + 4)]), grain_tex(vgrad([(HZ3, (110, 92, 96)), (H, (66, 60, 64))]), 0.18, 89))
    for k in range(14):
        t0 = (k / 14) ** 2.1
        t1 = ((k + 0.45) / 14) ** 2.1
        y0, y1 = HZ3 + t0 * 300, HZ3 + t1 * 300
        w0, w1 = 0.6 + t0 * 6, 0.6 + t1 * 6
        g.fill(Poly([(460 - w0 / 2, y0), (460 + w0 / 2, y0), (460 + w1 / 2, y1), (460 - w1 / 2, y1)]), (240, 200, 90))
    for side in (-1, 1):
        g.fill(Poly([(460 + side * 9, HZ3), (460 + side * 10.5, HZ3), (460 + side * 292, H + 4), (460 + side * 280, H + 4)]),
               (220, 214, 200), alpha=0.85)
    # telephone poles receding on the left
    for k, (x, y, h) in enumerate(((440, 304, 16), (400, 314, 30), (330, 332, 56), (200, 366, 110), (-20, 420, 200))):
        w = max(1.2, h * 0.045)
        g.fill(Box(x - w, y - h, x + w, y), light_x((70, 50, 40), x - w, x + w, 1.3, 0.6))
        g.fill(Box(x - h * 0.2, y - h * 0.92, x + h * 0.2, y - h * 0.88), (70, 50, 40))
    # saguaros
    cactus(g, 110, 560, 210, [(-1, 0.45, 0.3), (1, 0.6, 0.25)] if "arm" not in d else [(-1, 0.45, 0.3)], 90)
    cactus(g, 800, 420, 90, [(1, 0.5, 0.3), (-1, 0.62, 0.22)] if "cactus" not in d else [(1, 0.5, 0.3)], 91)
    # road sign (right)
    if True:
        g.fill(Box(668, 380, 672, 450), (120, 120, 124))
        g.fill(Poly([(670, 350), (690, 370), (670, 390), (650, 370)]), light_x((240, 190, 40), 650, 690, 1.1, 0.8))
        g.fill(Seg(662, 376, 678, 364, 3), (30, 30, 30))
    # car (rear view, right lane)
    cc = (40, 90, 150) if "car" not in d else (220, 220, 214)
    cx, cb = 545, 520
    g.mul(Ell(cx + 4, cb + 2, 62, 8), 0.6, feather=6)
    g.fill(Box(cx - 56, cb - 40, cx + 56, cb - 6, 8), light_y(cc, cb - 40, cb - 6, 1.25, 0.7))
    g.fill(Poly([(cx - 40, cb - 40), (cx + 40, cb - 40), (cx + 32, cb - 66), (cx - 32, cb - 66)]), light_y(cc, cb - 66, cb - 40, 1.2, 0.9))
    g.fill(Poly([(cx - 34, cb - 42), (cx + 34, cb - 42), (cx + 28, cb - 62), (cx - 28, cb - 62)]),
           lgrad(cx - 30, cb - 62, cx + 30, cb - 42, [(0, (255, 190, 130)), (1, (60, 50, 70))]))
    for s in (-1, 1):
        g.fill(Box(cx + s * 50 - 8, cb - 34, cx + s * 50 + 8, cb - 26, 2), (230, 40, 30))
        g.glow(cx + s * 50, cb - 30, 18, (255, 60, 40), 0.35)
        g.fill(Box(cx + s * 44 - 9, cb - 8, cx + s * 44 + 9, cb + 4, 3), (24, 24, 26))
    g.fill(Box(cx - 14, cb - 24, cx + 14, cb - 16), (230, 230, 220))
    g.fill(Box(cx - 50, cb - 12, cx + 50, cb - 6, 2), (40, 40, 44))
    g.bloom(220, 18, 0.4)
    g.grade(contrast=1.07, sat=1.1, warm=6)
    g.commit()


def l1503_hawk(g, m):
    g.fill(Seg(400, 80, 420, 86, 4, 2), (50, 36, 30))
    g.fill(Seg(420, 86, 440, 80, 2, 4), (50, 36, 30))
    g.fill(Ell(420, 87, 6, 3), (60, 44, 36))


L1503_ELEMENTS = [
    E("hawk", el(l1503_hawk), pivot=(420, 84), anim=dict(orbitRadius=(60, 20), orbitSpeed=-0.08, orbitAlign=True)),
    glint_el("shimmer", [(300, 304), (560, 306), (620, 302)], col=(255, 230, 190), r=7, speed=0.4),
    mist_el("dust", 790, 574, 110, 18, (220, 176, 130), alpha=0.45, length=50, seed=92),
]

L1503_DIFFS = [
    ("moon", 120, 90, 0),
    ("balloon", 700, 160, 0),
    ("car", 545, 490, 0),
    ("arm", 140, 450, 0),
    ("cactus", 780, 380, 0),
]


# =================================================================== Level 1504 snowy cabin at night
def l1504_bg(c, d):
    g = Ctx(c)
    sky(g, [(0, (6, 10, 28)), (160, (16, 26, 58)), (330, (40, 56, 96))])
    stars(g, 160, 260, seed=101)
    # aurora
    (j0, j1, i0, i1), X, Y = g.win((-2, 20, W + 2, 220), pad=0)
    curve = 110 + 50 * np.sin(X * 0.007 + 1.2) + 20 * np.sin(X * 0.02)
    band = np.exp(-((Y - curve) / 26) ** 2) * (0.35 + 0.65 * fbm(X, Y, 8, 60, 3, 102))
    g.img[j0:j1, i0:i1] += np.stack([band * 40, band * 150, band * 100], -1)
    g.glow(720, 90, 120, (150, 170, 220), 0.25)
    if "moon" not in d:
        g.fill(Circ(720, 90, 24), sphere_paint(720, 90, 24, (236, 236, 226), amb=0.75, spec=0.0))
        g.fill(Circ(726, 96, 7), (200, 200, 196), alpha=0.35)
        g.fill(Circ(712, 82, 5), (200, 200, 196), alpha=0.3)
    else:
        g.fill(Circ(720, 90, 24) - Circ(731, 84, 22), sphere_paint(720, 90, 24, (236, 236, 226), amb=0.75, spec=0.0))
    ridge(g, 340, 150, 220, 103, (40, 50, 80), snow=(250, (150, 166, 200)), haze=((50, 64, 104), 0.35, 0.6))
    treeline(g, 380, 40, 10, 104, (14, 24, 30), haze=((40, 56, 90), 0.4, 0.2))
    # snow ground with drifts
    g.fill(Box(-2, 370, W + 2, H + 2), vgrad([(370, (130, 146, 184)), (600, (186, 200, 232))]))
    (j0, j1, i0, i1), X, Y = g.win((-2, 370, W + 2, H), pad=0)
    hf = lambda dx, dy: fbm(X + dx, Y + dy, 160, 30, 3, 105)
    bump = (hf(-4, -4) - hf(4, 4)) * 5
    g.img[j0:j1, i0:i1] *= np.clip(1 + bump, 0.88, 1.1)[..., None]
    # snowy pines around
    for x, h, s in ((40, 200, 106), (120, 150, 107), (560, 120, 108), (830, 220, 109), (900, 180, 110), (610, 90, 111)):
        pine(g, x, 380 + h * 0.6, h, col=(20, 40, 40), seed=s, snow=(220, 230, 248), light=(1.0, 0.6))
    # cabin
    x0, x1, base = 230, 480, 450
    g.mul(Box(x0, base - 6, x1 + 30, base + 14), 0.5, feather=10)
    g.fill(Box(x0, base - 90, x1, base), planks("h", (110, 72, 46), seed=112, width=12, x_or_y0=base - 90))
    g.fill(Box(x0, base - 90, x1, base), (20, 30, 70), alpha=0.25)
    g.fill(Poly([(x0 - 24, base - 84), (355, base - 160), (x1 + 24, base - 84)]), tex(light_y((80, 60, 50), base - 160, base - 84), 0.15, 6, 3, 3, 113))
    g.fill(Rough(Poly([(x0 - 30, base - 80), (355, base - 168), (x1 + 30, base - 80), (x1 + 30, base - 88), (355, base - 156),
                       (x0 - 30, base - 88)]), 3, 10, 114), sphere_paint(355, base - 140, 200, (220, 230, 250), ry=60, amb=0.6, spec=0.05))
    g.fill(Box(410, base - 190, 432, base - 130), stone_wall((90, 90, 100), 115, 8, 6))
    g.fill(Rough(Box(406, base - 196, 436, base - 186, 4), 2, 6, 116), (220, 230, 250))
    lit = (255, 190, 100)
    window_glass(g, 260, base - 70, 300, base - 34, lit=lit, frame=(80, 56, 40))
    if "window" in d:                                     # curtains drawn in the left window
        for x0c, x1c in ((262, 279), (281, 298)):
            g.fill(Box(x0c, base - 68, x1c, base - 36), tex(lambda X, Y: C((176, 50, 44)) * (0.75 + 0.25 * np.sin(X * 1.3))[..., None], 0.05, 2, 6))
    window_glass(g, 410, base - 70, 450, base - 34, lit=lit, frame=(80, 56, 40))
    g.fill(Box(334, base - 76, 374, base), planks("v", (80, 52, 34), seed=117, width=10))
    g.fill(Circ(366, base - 38, 2.5), (220, 190, 120))
    g.glow(280, base - 52, 60, (255, 170, 80), 0.3)
    g.add(Poly([(256, base), (304, base), (330, base + 70), (230, base + 70)]), (255, 170, 90), 0.18, feather=14)
    g.glow(430, base - 52, 60, (255, 170, 80), 0.3)
    g.add(Poly([(406, base), (454, base), (480, base + 70), (380, base + 70)]), (255, 170, 90), 0.18, feather=14)
    # firewood stack
    if True:
        for row in range(3):
            for k in range(5 - row):
                x = 498 + k * 14 + row * 7
                y = base - 8 - row * 12
                g.fill(Circ(x, y, 6.5), rgrad(x, y, 7, [(0, (210, 170, 120)), (0.7, (160, 110, 70)), (1, (90, 60, 40))]))
        g.fill(Rough(Box(494, base - 46, 568, base - 38, 3), 2, 5, 118), (220, 230, 250))
    # lantern on a post (left)
    lx, ly = 80, 530
    g.fill(Box(lx - 3, ly, lx + 3, ly + 70), light_x((60, 44, 34), lx - 3, lx + 3))
    g.glow(lx, ly - 14, 50, (255, 170, 80), 0.45)
    lc = (40, 36, 34) if "lantern" not in d else (190, 40, 36)
    g.fill(Box(lx - 14, ly - 30, lx + 14, ly + 2, 3), lc)
    g.fill(Box(lx - 10, ly - 26, lx + 10, ly - 2, 2), (255, 210, 120))
    g.fill(Poly([(lx - 18, ly - 30), (lx, ly - 44), (lx + 18, ly - 30)]), lc)
    g.fill(Ell(lx, ly - 48, 5, 5) - Ell(lx, ly - 48, 2.5, 2.5), lc)
    # snowman
    sx, sb = 640, 520
    g.mul(Ell(sx + 16, sb, 50, 8), 0.4, feather=8)
    for cy, r in ((sb - 34, 36), (sb - 86, 26), (sb - 124, 18)):
        g.fill(Circ(sx, cy, r), sphere_paint(sx, cy, r, (226, 234, 252), amb=0.5, spec=0.1, bounce=(120, 140, 200)))
    scarf = (200, 40, 40) if "scarf" not in d else (40, 130, 80)
    g.fill(Box(sx - 22, sb - 110, sx + 22, sb - 100, 4), light_x(scarf, sx - 22, sx + 22))
    g.fill(Box(sx + 6, sb - 104, sx + 16, sb - 80, 3), light_x(scarf, sx + 6, sx + 16))
    for dx in (-6, 6):
        g.fill(Circ(sx + dx, sb - 128, 2.4), (20, 20, 24))
    g.fill(Poly([(sx, sb - 122), (sx + 18, sb - 119), (sx, sb - 117)]), (230, 120, 40))
    g.fill(Box(sx - 16, sb - 144, sx + 16, sb - 140), (20, 20, 24))
    g.fill(Box(sx - 11, sb - 166, sx + 11, sb - 142, 2), light_x((30, 30, 34), sx - 11, sx + 11))
    g.fill(Seg(sx - 24, sb - 90, sx - 54, sb - 112, 3, 2), (70, 50, 36))
    # sled
    sc = (190, 40, 36) if "sled" not in d else (40, 100, 170)
    g.mul(Ell(440, 576, 54, 6), 0.4, feather=6)
    g.fill(Box(394, 552, 486, 564, 3), planks("v", sc, seed=119, width=12))
    for x in (410, 470):
        g.fill(Box(x, 562, x + 4, 574), (60, 60, 64))
    g.fill(Seg(386, 576, 490, 576, 3), (70, 70, 76))
    g.fill(Seg(490, 576, 500, 562, 3), (70, 70, 76))
    # owl on the big pine (right)
    if "owl" not in d:
        ox, oy = 838, 300
        g.fill(Ell(ox, oy, 13, 18), tex(sphere_paint(ox, oy, 14, (150, 120, 90), ry=19, amb=0.5), 0.15, 1.5, 2))
        g.fill(Ell(ox, oy + 4, 8, 11), (196, 176, 150))
        for k in (-1, 1):
            g.fill(Circ(ox + k * 5, oy - 9, 4.5), (236, 220, 140))
            g.fill(Circ(ox + k * 5, oy - 9, 2), (20, 20, 20))
            g.fill(Poly([(ox + k * 4, oy - 17), (ox + k * 12, oy - 24), (ox + k * 10, oy - 14)]), (130, 100, 74))
        g.fill(Poly([(ox - 2, oy - 6), (ox + 2, oy - 6), (ox, oy - 1)]), (200, 160, 60))
        g.fill(Seg(ox - 24, oy + 18, ox + 24, oy + 20, 4), (70, 52, 40))
    # fence posts with snow caps (right)
    for k, x in enumerate(range(760, 900, 34)):
        g.fill(Box(x, 470, x + 8, 530), light_x((70, 52, 40), x, x + 8))
        g.fill(Rough(Ell(x + 4, 470, 7, 4), 1, 3, x), (226, 234, 250))
    g.fill(Box(760, 486, 900, 490), (70, 52, 40))
    g.bloom(200, 16, 0.5)
    g.grade(contrast=1.05, sat=1.05)
    g.commit()


L1504_ELEMENTS = [
    snow_layer("snow1", 121, 60, 1.0, 1.8, 26, mask=0, alpha=0.8),
    snow_layer("snow2", 122, 24, 2.0, 3.0, 44, mask=0, alpha=0.9),
    smoke_el("smoke", 421, 254, r=8, col=(150, 160, 180), rise=70, wind=-10, alpha=0.45),
    glint_el("twinkle", [(120, 60), (300, 30), (520, 160), (860, 200), (60, 220)], col=(255, 255, 240), r=3, speed=0.7),
    E("aurora", el(lambda g, m: g.glow(400, 120, 260, (40, 160, 110), 0.12, power=1.2, ry=60)), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=0.12)),
]

L1504_DIFFS = [
    ("moon", 726, 90, 0),
    ("window", 280, 398, 0),
    ("lantern", 80, 512, 0),
    ("scarf", 640, 410, 0),
    ("sled", 440, 564, 0),
    ("owl", 838, 296, 0),
]


# =================================================================== Level 1505 wheat field and red barn
HZ5 = 290


def wheat(g, y0, y1, seed=0, x0=-2, x1=W + 2):
    """Golden wheat: vertical stalk texture growing coarser towards the viewer, ears catching the light."""
    g.fill(Box(x0, y0, x1, y1), vgrad([(y0, (226, 186, 110)), (y1, (176, 120, 50))]))
    (j0, j1, i0, i1), X, Y = g.win((x0, y0, x1, y1), pad=0)
    t = np.clip((Y - y0) / max(1, y1 - y0), 0, 1)
    n = fbm(X, Y, 0.8 + 3 * t, 6 + 26 * t, 4, seed)
    ears = fbm(X, Y, 1.5 + 4 * t, 3 + 8 * t, 3, seed + 1)
    wave = fbm(X, Y, 90, 30, 3, seed + 2)
    k = (0.7 + 0.5 * n) * (0.85 + 0.3 * wave)
    sub = g.img[j0:j1, i0:i1]
    sub *= k[..., None]
    sub += (np.array([255, 226, 150], np.float32) - sub) * (smooth(0.66, 0.8, ears) * 0.5)[..., None]


def l1505_bg(c, d):
    g = Ctx(c)
    sky(g, [(0, (84, 128, 190)), (160, (170, 180, 196)), (HZ5, (250, 214, 160))])
    sun(g, 110, 250, r=20, halo=(255, 196, 120), k=0.9)
    cumulus(g, 380, 90, 170, 50, col=(255, 236, 214), shade=(176, 160, 170), seed=111)
    cumulus(g, 760, 140, 120, 36, col=(255, 232, 210), shade=(180, 166, 176), seed=112, alpha=0.85)
    ridge(g, HZ5 + 6, 46, 280, 113, (110, 140, 120), ridged=False, haze=((214, 200, 180), 0.55, 0.4), light=False)
    treeline(g, HZ5 + 16, 26, 26, 114, (70, 96, 60), conifer=False, haze=((200, 190, 160), 0.4, 0.25))
    grass_field(g, HZ5 + 10, 380, (110, 130, 60), (150, 160, 100), seed=115)
    # silo
    sx = 760
    g.fill(Box(sx - 26, 200, sx + 26, 382), tex(cyl_paint(sx, 26, (196, 196, 190), amb=0.4, spec=0.3), 0.06, 30, 2, 2, 116))
    for y in range(214, 380, 18):
        g.fill(Box(sx - 26, y, sx + 26, y + 1.5), (120, 120, 120), alpha=0.5)
    dome = (200, 204, 210) if "dome" not in d else (60, 130, 90)
    g.fill(Ell(sx, 200, 27, 20), sphere_paint(sx, 196, 27, dome, ry=22, amb=0.45, spec=0.5, shin=20))
    g.fill(Box(sx - 27, 200, sx + 27, 204), (150, 150, 150))
    # barn (gambrel roof)
    bx0, bx1, bb = 500, 700, 384
    g.mul(Box(bx0 + 10, bb - 6, bx1 + 40, bb + 10), 0.5, feather=10)
    g.fill(Box(bx0, bb - 110, bx1, bb), tex(planks("v", (168, 44, 36), seed=117, width=11, grain=0.22), 0.06, 4, 4))
    g.fill(Poly([(bx0 - 10, bb - 108), (bx0 + 26, bb - 166), (600, bb - 196), (bx1 - 26, bb - 166), (bx1 + 10, bb - 108)]),
           tex(light_y((70, 66, 66), bb - 196, bb - 108, 1.2, 0.8), 0.12, 8, 2, 3, 118))
    g.fill(Poly([(bx0 + 8, bb - 110), (bx0 + 30, bb - 156), (600, bb - 182), (bx1 - 30, bb - 156), (bx1 - 8, bb - 110)]),
           tex(planks("v", (178, 48, 38), seed=119, width=11), 0.05, 4, 4))
    g.mul(Box(bx0, bb - 112, bx1, bb - 100), 0.4, feather=6)
    trim = (240, 236, 226)
    g.fill(Box(560, bb - 76, 640, bb), planks("v", (150, 38, 32), seed=120, width=10))
    for a, b in (((560, bb - 76), (640, bb)), ((640, bb - 76), (560, bb))):
        g.fill(Seg(a[0], a[1], b[0], b[1], 5), trim)
    g.fill(Box(556, bb - 80, 644, bb - 74), trim)
    g.fill(Box(556, bb - 80, 562, bb), trim)
    g.fill(Box(638, bb - 80, 644, bb), trim)
    g.fill(Box(598, bb - 80, 602, bb), trim)
    if True:
        g.fill(Box(584, bb - 160, 616, bb - 120), lgrad(584, bb - 160, 616, bb - 120, [(0, (90, 60, 30)), (1, (220, 180, 90))]))
    else:
        g.fill(Box(584, bb - 160, 616, bb - 120), planks("v", (150, 38, 32), seed=121, width=8))
    g.fill(Box(580, bb - 164, 620, bb - 160), trim)
    g.fill(Box(580, bb - 120, 620, bb - 116), trim)
    for x in (514, 670):
        window_glass(g, x, bb - 96, x + 18, bb - 74, frame=trim, sky_top=(220, 190, 150), sky_bot=(90, 70, 60))
    # windpump
    wx, wb, wt = 380, 392, 236
    for s in (-1, 1):
        g.fill(Seg(wx + s * 22, wb, wx + s * 4, wt, 3), (110, 104, 100))
    for k in range(5):
        y = wb - (wb - wt) * (k + 0.5) / 5
        hw = 4 + 18 * (y - wt) / (wb - wt)
        g.fill(Seg(wx - hw, y, wx + hw, y - 22, 1.4), (110, 104, 100))
        g.fill(Seg(wx + hw, y, wx - hw, y - 22, 1.4), (110, 104, 100))
    vane = (196, 50, 40) if "vane" not in d else (236, 232, 222)
    g.fill(Seg(wx, wt, wx + 40, wt + 2, 3), (90, 86, 84))
    g.fill(Poly([(wx + 34, wt - 12), (wx + 66, wt - 16), (wx + 66, wt + 18), (wx + 34, wt + 12)]), light_x(vane, wx + 34, wx + 66, 1.1, 0.85))
    # fence along the pasture
    for x in range(-10, 470, 30):
        g.fill(Box(x, 360, x + 5, 394), light_x((120, 96, 70), x, x + 5))
    g.fill(Box(-10, 368, 470, 371), (130, 104, 76))
    g.fill(Box(-10, 380, 470, 383), (130, 104, 76))
    # wheat field
    def edge(x):
        return 392 + (fbm1(x, 40, 3, 122) - 0.5) * 8
    g.fill(Under(edge, -10, W + 10, H + 10), (200, 160, 90))
    wheat(g, 386, H + 2, seed=123)
    g.fill(Diff(Box(-2, 380, W + 2, H + 2), Under(edge, -10, W + 10, H + 10)), (0, 0, 0), alpha=0.0)
    # round hay bales
    bales = [(150, 430, 30), (236, 424, 26), (88, 470, 36)]
    for k, (x, y, r) in enumerate(bales):
        if k == 1 and "bale" in d:
            continue
        g.mul(Ell(x + r * 0.9, y + r * 0.85, r * 1.3, r * 0.25), 0.5, feather=r * 0.3)
        g.fill(Box(x - r * 0.9, y - r, x + r * 0.9, y + r, r * 0.25), tex(cyl_paint(y, r, (214, 178, 100), horizontal=True), 0.25, 1.5, 8, 3, 124 + k))
        g.fill(Ell(x + r * 0.9, y, r * 0.45, r), tex(rgrad(x + r * 0.9, y, r, [(0, (190, 150, 80)), (1, (226, 196, 120))], ry=r), 0.3, 2, 2, 3, 130 + k))
    # tractor
    tc = (60, 120, 60) if "tractor" not in d else (190, 50, 40)
    tx, tb = 790, 570
    g.mul(Ell(tx + 10, tb + 2, 80, 8), 0.5, feather=8)
    g.fill(Box(tx - 70, tb - 46, tx + 20, tb - 18, 6), light_y(tc, tb - 46, tb - 18, 1.25, 0.75))
    g.fill(Box(tx - 10, tb - 92, tx + 40, tb - 40, 4), light_y(tc, tb - 92, tb - 40, 1.2, 0.8))
    g.fill(Box(tx - 4, tb - 86, tx + 34, tb - 58, 2), lgrad(tx, tb - 86, tx + 34, tb - 58, [(0, (230, 210, 180)), (1, (90, 90, 100))]))
    g.fill(Box(tx - 54, tb - 70, tx - 48, tb - 44), (50, 50, 50))
    for wxx, r in ((tx + 26, 32), (tx - 56, 18)):
        g.fill(Circ(wxx, tb - r + 2, r), rgrad(wxx - r * 0.2, tb - r - r * 0.2, r * 1.2, [(0, (60, 60, 60)), (1, (20, 20, 22))]))
        g.fill(Circ(wxx, tb - r + 2, r * 0.5), sphere_paint(wxx, tb - r + 2, r * 0.5, (230, 200, 60), amb=0.5))
    # scarecrow
    sx2, sb2 = 520, 596
    g.fill(Box(sx2 - 3, sb2 - 140, sx2 + 3, sb2), (110, 86, 60))
    g.fill(Box(sx2 - 50, sb2 - 112, sx2 + 50, sb2 - 106), (110, 86, 60))
    g.fill(Poly([(sx2 - 22, sb2 - 116), (sx2 + 22, sb2 - 116), (sx2 + 26, sb2 - 60), (sx2 - 26, sb2 - 60)]),
           tex(light_x((80, 110, 150), sx2 - 26, sx2 + 26, 1.2, 0.7), 0.12, 3, 3))
    for s in (-1, 1):
        g.fill(Seg(sx2 + s * 20, sb2 - 112, sx2 + s * 46, sb2 - 104, 12, 9), light_y((80, 110, 150), sb2 - 118, sb2 - 98))
        for k in range(3):
            g.fill(Seg(sx2 + s * 52, sb2 - 106, sx2 + s * (60 + k * 3), sb2 - 96 + k * 5, 1.5), (220, 190, 110))
    g.fill(Circ(sx2, sb2 - 130, 15), sphere_paint(sx2, sb2 - 130, 15, (220, 196, 150), amb=0.5))
    hat = (120, 84, 50) if "hat" not in d else (40, 40, 44)
    g.fill(Ell(sx2, sb2 - 142, 26, 6), light_x(hat, sx2 - 26, sx2 + 26))
    g.fill(Box(sx2 - 13, sb2 - 162, sx2 + 13, sb2 - 140, 5), light_x(hat, sx2 - 13, sx2 + 13))
    blades(g, 540, 600, (200, 160, 80), n=240, seed=125, hmax=30, lean=6)
    g.bloom(220, 20, 0.35)
    g.grade(contrast=1.05, sat=1.08, warm=6)
    g.commit()


def l1505_wheel(g, m):
    cx, cy, r = 380, 236, 30
    for k in range(16):
        a = k * math.tau / 16
        g.fill(Seg(cx + 6 * math.cos(a), cy + 6 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a), 4.5, 7),
               (176, 172, 166) if k % 2 else (150, 146, 142))
    g.fill(Circ(cx, cy, 6), (80, 76, 74))


L1505_ELEMENTS = [
    E("wheel", el(l1505_wheel), pivot=(380, 236), anim=dict(rotateSpeed=-60)),
    cloud_el("cloud", 580, 60, 80, 22, col=(255, 236, 214), shade=(190, 170, 176), speed=6, alpha=0.8, seed=131),
    bird_el("crow1", 220, 170, s=7, speed=20, col=(30, 30, 34)),
    bird_el("crow2", 250, 190, s=6, speed=20, col=(30, 30, 34)),
]

L1505_DIFFS = [
    ("dome", 760, 196, 0),
    ("vane", 430, 236, 0),
    ("bale", 236, 424, 0),
    ("tractor", 780, 530, 0),
    ("hat", 520, 446, 0),
]


# =================================================================== Level 1506 rainy street at night
STREET = 400


def l1506_facade(g, d):
    g.fill(Box(-2, -2, W + 2, STREET), vgrad([(0, (14, 16, 30)), (STREET, (40, 36, 50))]))
    # facades
    g.fill(Box(-2, -2, 290, STREET), tex(light_x(bricks((110, 54, 44), (70, 60, 58), 22, 8, seed=141), -2, 290, 0.9, 0.6), 0.05, 4, 4))
    g.fill(Box(290, 30, 620, STREET), tex(lgrad(290, 30, 620, STREET, [(0, (120, 112, 104)), (1, (70, 66, 64))]), 0.08, 6, 6, 3, 142))
    g.fill(Box(620, -2, W + 2, STREET), tex(light_x(bricks((70, 60, 70), (50, 46, 50), 24, 9, seed=143), 620, W, 0.9, 0.55), 0.05, 4, 4))
    g.fill(Box(286, 20, 624, 32), (60, 56, 56))
    # upper windows (some lit)
    lit_set = {(0, 0), (1, 1), (2, 0), (4, 1), (5, 0), (6, 1)}
    cols = [40, 130, 210, 330, 430, 530, 680, 790]
    for i, x in enumerate(cols):
        for j, y in enumerate((60, 170)):
            lit = (i, j) in lit_set
            if (i, j) == (5, 0) and "window" in d:
                lit = False
            if (i, j) == (0, 0) and "window2" in d:
                lit = False
            window_glass(g, x, y, x + 50, y + 70, lit=(255, 200, 120) if lit else None, frame=(60, 56, 54),
                         sky_top=(40, 46, 70), sky_bot=(20, 22, 30), fw=3)
            if lit:
                g.glow(x + 25, y + 35, 60, (255, 170, 90), 0.15)
    # shop window with awning (middle)
    g.fill(Box(320, 280, 600, 392), lgrad(320, 280, 600, 392, [(0, (255, 214, 150)), (1, (200, 130, 70))]))
    for k in range(5):
        x = 340 + k * 54
        g.fill(Box(x, 330, x + 34, 380, 3), sphere_paint(x + 17, 350, 30, (190, 110, 70), ry=30, amb=0.5))   # loaves / goods on shelves
    g.fill(Box(320, 320, 600, 326), (120, 80, 50))
    g.fill(Box(316, 276, 604, 282), (50, 46, 44))
    g.fill(Box(456, 280, 462, 392), (50, 46, 44))
    aw = (40, 110, 80)
    for k in range(10):
        col = aw if k % 2 == 0 else (230, 226, 216)
        g.fill(Poly([(310 + k * 30, 240), (340 + k * 30, 240), (344 + k * 30, 276), (306 + k * 30, 276)]), light_y(col, 240, 276, 1.0, 0.75))
    g.glow(460, 336, 200, (255, 180, 100), 0.25, ry=90)
    # cafe sign (right building) - a glowing cup shape, no text
    sc = (90, 220, 255)
    g.fill(Box(700, 274, 820, 330, 6), (24, 22, 30))
    g.fill(Ell(744, 304, 20, 16) - Box(700, 270, 820, 300), sc)
    g.fill(Box(724, 296, 764, 300), sc)
    g.fill(Ell(768, 300, 7, 6) - Ell(768, 300, 3.5, 3), sc)
    g.fill(Seg(790, 290, 806, 290, 3), sc)
    g.fill(Seg(790, 302, 806, 302, 3), sc)
    g.glow(760, 302, 80, sc, 0.35, ry=50)
    window_glass(g, 650, 340, 860, 396, lit=(240, 170, 100), frame=(40, 36, 40), bars=False)
    # sidewalk
    g.fill(Box(-2, STREET - 8, W + 2, 430), grain_tex(vgrad([(STREET - 8, (70, 66, 70)), (430, (50, 48, 54))]), 0.15, 144))
    g.fill(Box(-2, 428, W + 2, 434), (90, 88, 92))


def l1506_bg(c, d):
    g = Ctx(c)
    l1506_facade(g, set())          # reflections show the unmodified street, so differences are not mirrored
    g.snapshot("s")
    l1506_facade(g, d)
    # wet asphalt with long smeared reflections
    g.fill(Box(-2, 434, W + 2, H + 2), grain_tex(vgrad([(434, (34, 34, 40)), (H, (20, 20, 24))]), 0.25, 145))
    g.reflect(STREET - 6, 434, H, k=0.6, tint=(20, 22, 30), tint_k=0.3, ripple=6, rsx=40, rsy=12, fade=0.35, streak=0.6)
    g.fill(Box(-2, 434, W + 2, H + 2), (24, 24, 30), alpha=lambda X, Y: 0.45 * smooth(0.45, 0.62, fbm(X, Y, 60, 14, 4, 146)))
    # street lamps
    for k, x in enumerate((170, 860)):
        g.fill(Box(x - 4, 150, x + 4, 430), cyl_paint(x, 4, (40, 42, 46)))
        g.fill(Box(x - 10, 420, x + 10, 432, 2), (30, 30, 34))
        if k == 1 and "lamp" in d:
            g.fill(Box(x - 3, 150, x + 3, 158), (30, 30, 34))
            g.fill(Circ(x, 136, 18), (255, 230, 170))
            g.fill(Box(x - 10, 114, x + 10, 120, 2), (30, 30, 34))
        else:
            g.fill(Poly([(x - 16, 130), (x + 16, 130), (x + 10, 156), (x - 10, 156)]), (255, 230, 170))
            g.fill(Poly([(x - 20, 132), (x, 114), (x + 20, 132)]), (30, 30, 34))
        if True:
            g.glow(x, 142, 140, (255, 190, 110), 0.35)
            g.glow(x, 142, 40, (255, 240, 200), 0.7)
            g.add(Poly([(x - 10, 156), (x + 10, 156), (x + 70, 430), (x - 70, 430)]), (255, 200, 130), 0.1, feather=20)
            g.glow(x, 520, 30, (255, 200, 130), 0.25, ry=90)
    # parked car (side view)
    cc = (150, 30, 36)
    cx0, cb = 380, 496
    g.mul(Ell(cx0 + 120, cb + 2, 140, 8), 0.7, feather=6)
    g.fill(Poly([(cx0, cb - 18), (cx0 + 8, cb - 46), (cx0 + 60, cb - 50), (cx0 + 96, cb - 84), (cx0 + 178, cb - 84),
                 (cx0 + 214, cb - 50), (cx0 + 244, cb - 44), (cx0 + 250, cb - 18), (cx0 + 240, cb - 8), (cx0 + 6, cb - 8)]),
           tex(light_y(cc, cb - 84, cb - 8, 1.3, 0.55), 0.04, 20, 4))
    g.add(Seg(cx0 + 20, cb - 46, cx0 + 230, cb - 44, 2), (255, 220, 180), 0.35)
    g.fill(Poly([(cx0 + 70, cb - 50), (cx0 + 102, cb - 78), (cx0 + 134, cb - 78), (cx0 + 134, cb - 50)]),
           lgrad(cx0 + 70, cb - 78, cx0 + 134, cb - 50, [(0, (90, 100, 120)), (1, (20, 22, 30))]))
    g.fill(Poly([(cx0 + 140, cb - 50), (cx0 + 140, cb - 78), (cx0 + 172, cb - 78), (cx0 + 202, cb - 50)]),
           lgrad(cx0 + 140, cb - 78, cx0 + 202, cb - 50, [(0, (90, 100, 120)), (1, (20, 22, 30))]))
    for wx in (cx0 + 52, cx0 + 196):
        g.fill(Circ(wx, cb - 10, 20), (16, 16, 18))
        g.fill(Circ(wx, cb - 10, 10), sphere_paint(wx, cb - 10, 10, (170, 170, 176), amb=0.4, spec=0.6))
    if "roofbox" not in d:                                # roof box on the car
        g.fill(Box(cx0 + 96, cb - 104, cx0 + 180, cb - 86, 7), light_y((50, 54, 62), cb - 104, cb - 86, 1.4, 0.7))
        g.fill(Box(cx0 + 110, cb - 88, cx0 + 116, cb - 84), (30, 30, 34))
        g.fill(Box(cx0 + 160, cb - 88, cx0 + 166, cb - 84), (30, 30, 34))
    g.fill(Box(cx0 + 238, cb - 40, cx0 + 250, cb - 32, 2), (255, 240, 200))
    g.glow(cx0 + 250, cb - 36, 40, (255, 230, 180), 0.4)
    # pedestrian with umbrella
    figure(g, 110, 470, 66, (60, 70, 90), pants=(30, 30, 36), hair=(30, 24, 20))
    um = (200, 160, 40) if "umbrella" not in d else (60, 140, 200)
    g.fill(Seg(110, 420, 116, 360, 2), (30, 30, 30))
    g.fill(Ell(116, 366, 48, 26) - Box(60, 366, 180, 400), sphere_paint(116, 372, 48, um, ry=30, amb=0.45, spec=0.4))
    for k in range(-2, 3):
        g.fill(Seg(116, 342, 116 + k * 22, 366, 1), mixc(um, (0, 0, 0), 0.3))
    # fire hydrant
    if "hydrant" not in d:
        g.mul(Ell(820, 432, 20, 4), 0.5, feather=4)
        g.fill(Box(808, 396, 832, 430, 4), cyl_paint(820, 12, (200, 50, 40), spec=0.5))
        g.fill(Ell(820, 396, 12, 8), sphere_paint(820, 394, 12, (200, 50, 40), ry=8))
        g.fill(Box(800, 406, 840, 414, 3), cyl_paint(410, 4, (180, 40, 34), horizontal=True))
    g.bloom(190, 16, 0.55)
    g.grade(contrast=1.08, sat=1.05, lift=(4, 4, 10))
    g.commit()


L1506_ELEMENTS = [
    rain_layer("rain1", 151, 70, 18, 1.0, 0.35, 260, mask=0, step=(30, 120), col=(200, 210, 230)),
    rain_layer("rain2", 152, 30, 26, 1.4, 0.45, 380, mask=0, step=(40, 150), col=(220, 226, 240)),
    glint_el("puddle", [(250, 520), (620, 560), (780, 500), (120, 580)], col=(255, 220, 170), r=6, speed=0.9),
    E("flicker", el(lambda g, m: g.glow(170, 142, 60, (255, 210, 140), 0.5)), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=1.7)),
]

L1506_DIFFS = [
    ("window", 555, 95, 0),
    ("window2", 65, 95, 0),
    ("lamp", 860, 138, 0),
    ("roofbox", 518, 400, 0),
    ("umbrella", 116, 360, 0),
    ("hydrant", 820, 412, 0),
]


# =================================================================== Level 1507 tropical beach
HZ7 = 240


def palm(g, x0, y0, x1, y1, bend, seed, fronds=9, coconuts=True, col=(60, 120, 50)):
    """Curved palm trunk (ringed) + crown of drooping fronds."""
    rnd = random.Random(seed)
    pts = []
    for k in range(25):
        t = k / 24
        x = x0 + (x1 - x0) * t + bend * math.sin(t * math.pi) * (1 - t * 0.3)
        y = y0 + (y1 - y0) * t
        pts.append((x, y))
    for k in range(24):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]
        w = 22 - 10 * k / 24
        g.fill(Seg(ax, ay, bx, by, w, w - 0.4), tex(light_x((150, 120, 90), min(ax, bx) - w / 2, max(ax, bx) + w / 2, 1.2, 0.6), 0.2, 3, 1.2, 3, seed + k))
        g.fill(Seg(ax - w * 0.48, ay, ax + w * 0.48, ay - 1, 1.2), (90, 70, 56), alpha=0.6)
    cx, cy = pts[-1]
    if coconuts:
        for dx, dy in ((-10, 10), (9, 11), (0, 20), (-2, 4)):
            g.fill(Circ(cx + dx, cy + dy, 10), sphere_paint(cx + dx, cy + dy, 10, (110, 80, 40), amb=0.4, spec=0.2))
    for k in range(fronds):
        a = -math.pi + k * math.pi / (fronds - 1) * 1.0 + rnd.uniform(-0.15, 0.15)
        ln = rnd.uniform(90, 130)
        droop = rnd.uniform(30, 60)
        prev = (cx, cy)
        for j in range(1, 13):
            t = j / 12
            px = cx + math.cos(a) * ln * t
            py = cy + math.sin(a) * ln * t * 0.55 + droop * t * t
            wd = 10 * math.sin(t * math.pi) + 1
            colk = mixc(col, (200, 220, 120), 0.15 * (1 - t))
            g.fill(Seg(prev[0], prev[1], px, py, 3, 2.5), mixc(col, (40, 50, 20), 0.3))
            nx, ny = -(py - prev[1]), (px - prev[0])
            nl = math.hypot(nx, ny) or 1
            for s in (-1, 1):
                g.fill(Seg(px, py, px + s * nx / nl * wd * 1.6 + (px - prev[0]) * 0.6, py + s * ny / nl * wd * 1.6 + 6, 2.6, 0.6),
                       light_y(colk, cy - 40, cy + 80, 1.2, 0.7))
            prev = (px, py)


def l1507_bg(c, d):
    g = Ctx(c)
    sky(g, [(0, (30, 110, 200)), (140, (100, 170, 226)), (HZ7, (200, 228, 242))])
    cumulus(g, 300, 120, 160, 50, seed=161)
    cumulus(g, 700, 80, 110, 34, seed=162, alpha=0.9)
    cloud_layer(g, 170, 232, (255, 255, 255), (210, 222, 236), cover=0.35, sx=180, sy=14, seed=163, alpha=0.7)
    # distant island
    ridge(g, HZ7 + 3, 50, 120, 164, (70, 120, 90), x0=560, x1=820 if "island" not in d else 750, ridged=False,
          haze=((170, 210, 220), 0.55, 0.4))
    g.fill(Box(-2, HZ7, W + 2, H), vgrad([(HZ7, (30, 100, 160)), (330, (30, 150, 180)), (440, (70, 210, 200))]))
    water(g, HZ7, 460, (30, 100, 160), (70, 210, 200), seed=165, streak=0.12)
    ripples_light(g, HZ7 + 2, 450, (255, 255, 250), k=0.45, seed=166)
    # outrigger boat
    bc = (220, 80, 50) if "boat" not in d else (240, 200, 60)
    g.mul(Ell(440, 308, 56, 5), 0.3, feather=4)
    g.fill(Poly([(390, 296), (490, 296), (478, 308), (402, 308)]), light_y(bc, 296, 308, 1.2, 0.7))
    g.fill(Box(394, 292, 486, 297, 2), (240, 236, 220))
    g.fill(Seg(414, 296, 414, 316, 2), (120, 90, 60))
    g.fill(Seg(466, 296, 466, 316, 2), (120, 90, 60))
    g.fill(Seg(400, 316, 480, 316, 5), (200, 190, 170))
    figure(g, 440, 296, 36, (240, 240, 230), hair=(40, 30, 24), sitting=True)
    # beach with wet band and foam
    def shore(x):
        return 430 + 26 * np.sin(x * 0.006 + 0.5) + (fbm1(x, 40, 3, 167) - 0.5) * 10
    g.fill(Under(shore, -10, W + 10, H + 10), grain_tex(vgrad([(420, (226, 206, 170)), (600, (240, 222, 186))]), 0.08, 168))
    (j0, j1, i0, i1), X, Y = g.win((-10, 380, W + 10, H), pad=0)
    top = shore(X[0])[None, :]
    wetb = np.clip(1 - (Y - top) / 22, 0, 1) * (Y > top)
    g.img[j0:j1, i0:i1] *= (1 - wetb * 0.22)[..., None]
    foam = np.clip(1 - np.abs(Y - top + 2) / 4, 0, 1) * smooth(0.35, 0.6, fbm(X, Y, 8, 3, 3, 169))
    foam2 = np.clip(1 - np.abs(Y - top + 16) / 3, 0, 1) * smooth(0.45, 0.7, fbm(X, Y, 10, 3, 3, 170)) * 0.7
    g.img[j0:j1, i0:i1] += (250 - g.img[j0:j1, i0:i1]) * np.clip(foam + foam2, 0, 1)[..., None]
    # palms
    palm(g, 70, H + 20, 150, 140, 60, 171, coconuts="coco" not in d)
    palm(g, 860, H + 20, 790, 190, -40, 172, fronds=8)
    # umbrella + towel + lounger
    uc = (230, 70, 60) if "umbrella" not in d else (60, 140, 220)
    ux, uy = 680, 452
    g.mul(Ell(ux + 10, 560, 76, 14), 0.35, feather=14)
    g.fill(Seg(ux - 14, 590, ux, uy, 3), (230, 230, 226))
    canopy = Ell(ux, uy, 64, 28) - Box(ux - 80, uy, ux + 80, uy + 50)
    g.fill(canopy, sphere_paint(ux, uy + 8, 64, (246, 244, 236), ry=34, amb=0.5))
    for k in range(-3, 4, 2):
        g.fill(canopy & Poly([(ux, uy - 30), (ux + k * 19 - 10, uy), (ux + k * 19 + 10, uy)]), sphere_paint(ux, uy + 8, 64, uc, ry=34, amb=0.5))
    tw = (60, 150, 210)
    g.fill(Poly([(470, 540), (590, 530), (610, 570), (480, 584)]), tex(light_x(tw, 470, 610, 1.1, 0.85), 0.05, 6, 6))
    for k in range(4):
        g.fill(Poly([(476 + k * 3, 548 + k * 10), (594 + k * 3, 538 + k * 10), (596 + k * 3, 542 + k * 10), (478 + k * 3, 552 + k * 10)]),
               (250, 250, 246), alpha=0.8)
    # sandcastle with flag
    g.mul(Ell(270 - 80, 552, 54, 8), 0.35, feather=6)
    for x0, x1, top in ((144, 236, 520), (160, 186, 494), (196, 222, 490)):
        g.fill(Box(x0, top, x1, 552, 3), grain_tex(light_x((216, 190, 140), x0, x1, 1.15, 0.8), 0.15, 171))
        for k in range(int((x1 - x0) / 8)):
            if k % 2 == 0:
                g.fill(Box(x0 + k * 8, top - 6, x0 + k * 8 + 6, top, 1), light_x((216, 190, 140), x0, x1, 1.15, 0.8))
    g.fill(Seg(209, 490, 209, 440, 2), (90, 80, 70))
    fc = (220, 40, 50) if "flag" not in d else (40, 160, 90)
    g.fill(Poly([(210, 440), (250, 450), (210, 462)]), light_y(fc, 440, 462, 1.15, 0.85))
    # bucket and shells
    g.fill(Poly([(360, 526), (390, 526), (386, 556), (364, 556)]), cyl_paint(375, 15, (60, 160, 220)))
    for x, y in ((290, 560), (360, 586), (760, 586)):
        g.fill(Ell(x, y, 7, 5), sphere_paint(x, y, 7, (250, 220, 200), ry=5, amb=0.6))
    # crab on the sand
    if "crab" not in d:
        kx, ky = 452, 572
        g.mul(Ell(kx + 4, ky + 8, 22, 4), 0.35, feather=4)
        for k in (-1, 1):
            for j in range(3):
                g.fill(Seg(kx + k * 10, ky + 2, kx + k * (22 + j * 2), ky + 6 + j * 4, 2), (200, 70, 40))
            g.fill(Seg(kx + k * 12, ky - 4, kx + k * 22, ky - 12, 3), (210, 80, 46))
            g.fill(Ell(kx + k * 24, ky - 15, 6, 5), sphere_paint(kx + k * 24, ky - 15, 6, (220, 90, 50), ry=5))
        g.fill(Ell(kx, ky, 16, 10), sphere_paint(kx, ky - 2, 16, (220, 90, 50), ry=11, amb=0.45, spec=0.3))
        for k in (-1, 1):
            g.fill(Circ(kx + k * 5, ky - 12, 2.2), (30, 20, 20))
    g.grade(contrast=1.04, sat=1.1)
    g.commit()


def l1507_frond(g, m):
    cx, cy = 790, 190
    for a, ln in ((0.35, 120), (0.75, 100)):
        prev = (cx, cy)
        for j in range(1, 12):
            t = j / 11
            px, py = cx + math.cos(a) * ln * t, cy + math.sin(a) * ln * t * 0.4 + 40 * t * t
            wd = 9 * math.sin(t * math.pi) + 1
            g.fill(Seg(prev[0], prev[1], px, py, 2.6), (40, 80, 30))
            for s in (-1, 1):
                g.fill(Seg(px, py, px + s * 3 + (px - prev[0]) * 0.6, py + s * wd * 1.4 + 6, 2.4, 0.6), (70, 130, 50))
            prev = (px, py)


L1507_ELEMENTS = [
    E("frond", el(l1507_frond), pivot=(790, 190), anim=dict(swingAngle=5, swingSpeed=0.3)),
    bird_el("gull", 480, 120, s=8, speed=-20, col=(250, 250, 250)),
    cloud_el("cloud", 520, 190, 70, 18, speed=4, alpha=0.7, seed=173),
    glint_el("sparkle", [(140, 300), (300, 280), (560, 380), (640, 330), (240, 400)], r=4, speed=0.6),
    mist_el("wash", 450, 412, 300, 6, (250, 252, 250), alpha=0.6, length=24, seed=174),
]

L1507_DIFFS = [
    ("island", 790, 232, 0),
    ("boat", 440, 302, 0),
    ("coco", 150, 155, 0),
    ("umbrella", 680, 440, 0),
    ("crab", 452, 568, 0),
    ("flag", 225, 450, 0),
]


# =================================================================== Level 1508 still life by the window
TABLE = 400


def l1508_bg(c, d):
    g = Ctx(c)
    # plaster wall, warm light falling from the window on the left
    wall = tex(hgrad([(0, (226, 212, 188)), (500, (196, 180, 156)), (900, (140, 124, 106))]), 0.05, 10, 10, 4, 181)
    g.fill(Box(-2, -2, W + 2, TABLE), wall)
    # window (left): bright soft-focus garden outside
    wx0, wy0, wx1, wy1 = 40, 40, 300, 330
    g.fill(Box(wx0, wy0, wx1, wy1), vgrad([(wy0, (190, 220, 240)), (wy1, (236, 240, 230))]))
    crown(g, 110, 250, 110, 80, (130, 170, 100), seed=182)
    crown(g, 260, 270, 90, 70, (110, 156, 90), seed=183)
    g.blur((wx0, wy0, wx1, wy1), 5)
    if "bird" not in d:                                   # a bird on a branch outside (in focus)
        g.fill(Seg(196, 136, 290, 128, 4, 2.5), (90, 70, 56))
        g.fill(Ell(236, 118, 14, 10), sphere_paint(236, 116, 14, (150, 110, 80), ry=10, amb=0.5))
        g.fill(Ell(240, 124, 9, 6), (230, 120, 70))
        g.fill(Circ(226, 110, 7), sphere_paint(226, 110, 7, (140, 100, 74), amb=0.5))
        g.fill(Circ(223, 108, 1.4), (20, 20, 20))
        g.fill(Poly([(219, 110), (212, 112), (219, 113)]), (60, 50, 40))
        g.fill(Poly([(248, 116), (266, 110), (264, 118)]), (110, 80, 60))
    g.fill(Box(wx0, wy0, wx1, wy1), (255, 255, 250), alpha=0.25)
    g.fill(Diff(Box(-2, -2, W + 2, TABLE), Box(wx0, wy0, wx1, wy1)), wall)        # wall again around the glass
    g.fill(Diff(Box(wx0 - 14, wy0 - 14, wx1 + 14, wy1 + 20), Box(wx0, wy0, wx1, wy1)), light_y((236, 232, 222), wy0, wy1, 1.05, 0.9))
    g.fill(Box(166, wy0, 174, wy1), (236, 232, 222))
    g.fill(Box(wx0, 180, wx1, 188), (236, 232, 222))
    g.mul(Box(wx0, wy0, wx1, wy0 + 6), 0.3, feather=4)
    g.fill(Box(wx0 - 24, wy1 + 14, wx1 + 24, wy1 + 26, 2), light_y((240, 236, 228), wy1 + 14, wy1 + 26))
    # curtain (right of the window): soft folds
    def folds(X, Y):
        k = 0.78 + 0.22 * np.sin((X - 300) * 0.22 + np.sin(Y * 0.02) * 1.5)
        return C((200, 170, 120)) * k[..., None]
    g.fill(Poly([(296, 20), (370, 20), (360, 200), (380, 396), (300, 396)]), tex(folds, 0.04, 3, 30))
    g.fill(Box(20, 14, 420, 22, 4), cyl_paint(18, 4, (120, 90, 60), horizontal=True))
    # light patch on the wall
    g.add(Poly([(420, 60), (600, 80), (640, 380), (460, 380)]), (255, 230, 180), 0.16, feather=24)
    # framed picture (right wall)
    pc = (70, 110, 150)
    g.shadow(Box(640, 70, 820, 210), 8, 8, 10, 0.4)
    g.fill(Box(640, 70, 820, 210), light_x((150, 110, 60), 640, 820, 1.15, 0.8))
    g.fill(Box(656, 86, 804, 194), vgrad([(86, (200, 210, 214)), (150, (230, 220, 196)), (194, pc)]))
    g.fill(Under(lambda x: 168 - 50 * fbm1(x, 60, 4, 184), 656, 804, 194) & Box(656, 86, 804, 194),
           light_y((110, 120, 120), 120, 194, 1.1, 0.8))
    g.fill(Box(656, 170, 804, 194), pc)
    if "boat" not in d:                                   # sailboat in the painting
        g.fill(Poly([(712, 130), (712, 172), (736, 172)]), (246, 240, 226))
        g.fill(Poly([(708, 136), (708, 172), (692, 172)]), (236, 228, 214))
        g.fill(Poly([(688, 174), (740, 174), (732, 182), (696, 182)]), (120, 60, 40))
    # table top (wood) and its front edge
    g.fill(Box(-2, TABLE, W + 2, 560), planks("h", (150, 102, 62), seed=185, width=26, grain=0.25, x_or_y0=TABLE))
    g.fill(Box(-2, TABLE, W + 2, 560), (255, 230, 190), alpha=lambda X, Y: 0.18 * np.clip(1 - X / 700, 0, 1))
    g.fill(Box(-2, 560, W + 2, H + 2), light_y((100, 64, 36), 560, 600, 1.0, 0.6))
    g.mul(Box(-2, 556, W + 2, 562), 0.4, feather=3)
    # linen runner
    g.fill(Poly([(330, TABLE + 4), (760, TABLE + 4), (800, 556), (300, 556)]), tex((232, 226, 210), 0.06, 1.2, 1.2, 2, 186))
    # book stack (left)
    bk = (60, 80, 120)
    for k, col in enumerate(((120, 40, 40), (40, 90, 60), bk)):
        y1 = 516 - k * 22
        g.shadow(Box(70 + k * 6, y1 - 20, 220 - k * 4, y1), 10, 6, 8, 0.35)
        g.fill(Box(70 + k * 6, y1 - 20, 220 - k * 4, y1, 3), light_y(col, y1 - 20, y1, 1.2, 0.75))
        g.fill(Box(74 + k * 6, y1 - 16, 216 - k * 4, y1 - 4), (236, 228, 210))
        g.fill(Box(70 + k * 6, y1 - 20, 80 + k * 6, y1, 3), light_y(col, y1 - 20, y1, 1.2, 0.75))
    # teacup on saucer on the books
    cup = (240, 240, 236) if "cup" not in d else (90, 150, 200)
    g.fill(Ell(150, 452, 40, 8), sphere_paint(150, 448, 40, (236, 236, 232), ry=10, amb=0.6))
    g.fill(Poly([(124, 412), (176, 412), (170, 448), (130, 448)]), cyl_paint(150, 26, cup, amb=0.5, spec=0.4))
    g.fill(Ell(150, 412, 26, 6), (120, 70, 40))
    g.fill(Ell(180, 426, 10, 10) - Ell(180, 426, 6, 6), cyl_paint(180, 10, cup, amb=0.5))
    # ceramic pitcher
    px, pb = 440, 520
    g.shadow(Ell(px, pb, 50, 10), 30, 0, 16, 0.4)
    body = Union([Ell(px, pb - 60, 52, 62), Box(px - 40, pb - 150, px + 40, pb - 60), Ell(px, pb - 4, 42, 6)])
    g.fill(body, cyl_paint(px, 52, (236, 230, 216), amb=0.4, spec=0.45, shin=26))
    band = (40, 80, 150) if "band" not in d else (200, 120, 40)
    g.fill(body & Box(px - 60, pb - 110, px + 60, pb - 92), cyl_paint(px, 52, band, amb=0.4, spec=0.3))
    g.fill(Poly([(px - 40, pb - 150), (px - 62, pb - 164), (px - 30, pb - 158)]), (226, 220, 206))
    g.fill(Ell(px + 52, pb - 100, 26, 40) - Ell(px + 52, pb - 100, 16, 30) - Box(px, pb - 160, px + 46, pb - 40),
           cyl_paint(px + 60, 20, (232, 226, 212), amb=0.4))
    g.fill(Ell(px, pb - 150, 40, 6), (90, 80, 70))
    # glass bottle
    bx = 560
    g.shadow(Box(bx - 22, pb - 10, bx + 22, pb), 20, 0, 12, 0.3)
    btl = Union([Box(bx - 22, pb - 130, bx + 22, pb, 8), Box(bx - 8, pb - 190, bx + 8, pb - 120, 3)])
    g.fill(btl, cyl_paint(bx, 22, (40, 90, 60), amb=0.5, spec=0.8, shin=30), alpha=0.85)
    g.fill(Box(bx - 9, pb - 196, bx + 9, pb - 186, 2), (150, 110, 70))
    g.fill(Box(bx - 22, pb - 100, bx + 22, pb - 60, 2), (226, 214, 180))
    g.fill(Box(bx - 14, pb - 92, bx + 14, pb - 68), (150, 60, 50), alpha=0.6)
    # fruit bowl
    fx, fb = 680, 516
    g.shadow(Ell(fx, fb, 90, 10), 30, 0, 18, 0.45)
    apple = (190, 30, 30) if "apple" not in d else (130, 180, 50)
    fruits = [(640, 450, 26, (190, 30, 30)), (690, 440, 28, (240, 140, 30)), (734, 456, 24, apple), (668, 470, 24, (220, 190, 60))]
    for x, y, r, col in fruits:
        g.fill(Circ(x, y, r), sphere_paint(x, y, r, col, amb=0.3, spec=0.45, shin=24, bounce=(200, 160, 120)))
    g.fill(Seg(642, 424, 646, 414, 2.5), (90, 60, 30))
    for k in range(9):
        x, y = 700 + (k % 3) * 11 + (k // 3) * 5, 470 + (k // 3) * 10
        g.fill(Circ(x, y, 7), sphere_paint(x, y, 7, (90, 40, 110), amb=0.3, spec=0.6))
    bowl = Ell(fx, fb - 30, 96, 46) - Box(fx - 100, fb - 90, fx + 100, fb - 30)
    g.fill(bowl, cyl_paint(fx, 96, (176, 120, 70), amb=0.4, spec=0.3))
    g.fill(Ell(fx, fb - 30, 96, 10) - Ell(fx, fb - 33, 92, 8), (200, 150, 100))
    # lemon on the table (front)
    if "lemon" not in d:
        g.shadow(Ell(300, 548, 30, 8), 16, 0, 10, 0.4)
        g.fill(Ell(300, 530, 32, 22), tex(sphere_paint(300, 530, 32, (246, 214, 60), ry=22, amb=0.35, spec=0.4), 0.06, 1.5, 1.5, 2))
        g.fill(Ell(332, 530, 5, 4), (220, 190, 50))
    # vase with flowers (right)
    vx = 830
    g.shadow(Ell(vx, 520, 30, 8), 20, 0, 12, 0.4)
    g.fill(Union([Ell(vx, 480, 32, 40), Box(vx - 12, 400, vx + 12, 450)]), cyl_paint(vx, 32, (70, 110, 140), amb=0.4, spec=0.5))
    fl = (230, 90, 120)
    for k, (dx, dy) in enumerate(((-30, -90), (0, -120), (28, -96), (-12, -60), (34, -56))):
        g.fill(Seg(vx, 404, vx + dx, 404 + dy, 2.4), (70, 110, 50))
        col = fl if k in (1, 2) else (240, 200, 70)
        for a in range(6):
            aa = a * math.pi / 3
            g.fill(Ell(vx + dx + 9 * math.cos(aa), 404 + dy + 9 * math.sin(aa), 7, 7), sphere_paint(vx + dx, 404 + dy, 18, col, amb=0.55))
        g.fill(Circ(vx + dx, 404 + dy, 4.5), (120, 80, 30))
    g.grade(contrast=1.05, sat=1.04, warm=4)
    g.commit()


L1508_ELEMENTS = [
    smoke_el("steam1", 146, 396, r=7, col=(250, 250, 250), rise=60, wind=6, alpha=0.4),
    smoke_el("steam2", 156, 396, r=6, col=(250, 250, 250), rise=56, wind=-4, alpha=0.35, phase=0.5, seed=9),
    glint_el("motes", [(420, 120), (480, 220), (530, 160), (600, 300), (460, 330)], col=(255, 240, 200), r=2.5, speed=0.3),
    E("curtain", el(lambda g, m: g.fill(Poly([(368, 22), (390, 22), (384, 200), (396, 396), (378, 396), (372, 200)]),
                                         light_x((190, 160, 110), 368, 396, 1.0, 0.7))), pivot=(380, 22),
      anim=dict(swingAngle=1.2, swingSpeed=0.25)),
]

L1508_DIFFS = [
    ("bird", 238, 120, 0),
    ("boat", 714, 156, 0),
    ("cup", 150, 430, 0),
    ("band", 440, 418, 0),
    ("apple", 734, 456, 0),
    ("lemon", 300, 530, 0),
]


# =================================================================== Level 1509 camping under the stars
LAKE9 = 330


def l1509_bg(c, d):
    g = Ctx(c)
    sky(g, [(0, (4, 6, 20)), (200, (14, 20, 46)), (LAKE9, (36, 44, 76))])
    # milky way band (diagonal)
    (j0, j1, i0, i1), X, Y = g.win((-2, -2, W + 2, LAKE9), pad=0)
    u = (X * 0.42 + Y * 0.9 - 260) / 90
    band = np.exp(-u * u) * (0.55 + 0.5 * fbm(X, Y, 70, 60, 5, 191))
    dust = smooth(0.5, 0.72, fbm(X, Y, 26, 30, 5, 192)) * np.exp(-u * u * 3)
    glow = band * (1 - dust * 0.45)
    pink = smooth(0.45, 0.7, fbm(X, Y, 90, 70, 3, 193)) * band
    g.img[j0:j1, i0:i1] += np.stack([glow * 66 + pink * 26, glow * 60 + pink * 8, glow * 86 + pink * 20], -1)
    stars(g, 260, LAKE9, seed=194)
    rnd = random.Random(195)
    for _ in range(300):
        x, y = rnd.uniform(0, W), rnd.uniform(0, LAKE9)
        if math.exp(-((x * 0.42 + y * 0.9 - 260) / 90) ** 2) > rnd.random():
            g.glow(x, y, 1.6, (250, 246, 240), 0.8, power=1)
    ridge(g, LAKE9 - 2, 110, 180, 196, (12, 14, 26), ridged=True, light=False, rock_tex=0.05)
    treeline(g, LAKE9 + 2, 30, 9, 197, (6, 8, 14), light=0.0)
    g.snapshot("s")
    water(g, LAKE9, 470, (30, 36, 64), (10, 12, 24), seed=198, streak=0.1)
    g.reflect(LAKE9, LAKE9, 470, k=0.7, tint=(10, 14, 30), tint_k=0.2, ripple=2.0, fade=0.4)
    # shore
    def shore(x):
        return 440 + (fbm1(x, 60, 3, 199) - 0.5) * 30 - x * 0.02
    g.fill(Under(shore, -10, W + 10, H + 10), tex(vgrad([(430, (26, 30, 26)), (600, (14, 16, 14))]), 0.3, 4, 6, 4, 200))
    # fire light on the ground
    fx, fy = 520, 530
    g.glow(fx, fy, 320, (255, 130, 50), 0.35, ry=150)
    # tent (A-frame, glowing from inside)
    tc = (230, 130, 50)
    g.mul(Ell(300, 512, 130, 12), 0.5, feather=10)
    g.fill(Poly([(190, 512), (300, 380), (410, 512)]), lgrad(300, 380, 300, 512, [(0, mixc(tc, (255, 240, 200), 0.3)), (1, tc)]))
    g.fill(Poly([(300, 380), (410, 512), (440, 506), (330, 382)]), light_y(mixc(tc, (40, 20, 10), 0.45), 380, 512))
    g.fill(Poly([(270, 512), (300, 430), (330, 512)]), lgrad(300, 430, 300, 512, [(0, (255, 230, 160)), (1, (255, 180, 90))]))
    g.glow(300, 470, 140, tc, 0.3, ry=90)
    g.fill(Seg(300, 382, 300, 340, 2), (60, 50, 40))
    if "pennant" not in d:
        g.fill(Poly([(301, 340), (350, 352), (301, 366)]), light_y((230, 220, 90), 340, 366, 1.1, 0.8))
    # backpack by the tent
    if "pack" not in d:
        g.fill(Box(150, 520, 186, 564, 8), sphere_paint(160, 534, 30, (60, 90, 150), ry=34, amb=0.35, spec=0.1))
        g.fill(Box(154, 540, 182, 556, 4), (40, 60, 100))
        g.add(Box(176, 520, 186, 564, 6), (255, 140, 60), 0.2)
    # lantern (left, on a stump)
    g.fill(Box(84, 500, 120, 540, 4), tex(light_x((90, 66, 46), 84, 120, 1.0, 0.6), 0.2, 2, 6))
    g.fill(Ell(102, 500, 18, 5), (150, 110, 70))
    if True:
        g.fill(Box(92, 466, 112, 498, 3), (255, 220, 140))
        g.fill(Box(90, 462, 114, 468, 2), (40, 40, 40))
        g.fill(Ell(102, 460, 6, 6) - Ell(102, 460, 3.5, 3.5), (40, 40, 40))
        g.glow(102, 482, 70, (255, 200, 110), 0.45)
    # campfire: stone ring + logs (flames are an animated element)
    for k in range(10):
        a = k * math.tau / 10
        x, y = fx + 46 * math.cos(a), fy + 12 * math.sin(a)
        g.fill(Ell(x, y, 11, 7), sphere_paint(x, y - 2, 11, (110, 100, 96), ry=7, amb=0.3))
    g.fill(Seg(fx - 34, fy + 4, fx + 30, fy - 8, 10), tex(light_y((100, 70, 50), fy - 14, fy + 8, 1.4, 0.6), 0.2, 6, 1.5))
    g.fill(Seg(fx - 30, fy - 8, fx + 34, fy + 4, 10), tex(light_y((90, 64, 44), fy - 14, fy + 8, 1.4, 0.6), 0.2, 6, 1.5))
    g.glow(fx, fy - 4, 30, (255, 120, 30), 0.8)
    # camp chairs
    ch = (40, 100, 150) if "chair" not in d else (170, 40, 50)
    for x, col in ((650, ch), (372, (60, 120, 70))):
        g.mul(Ell(x + 6, 572, 34, 5), 0.5, feather=5)
        g.fill(Seg(x - 22, 572, x + 22, 532, 3), (60, 60, 64))
        g.fill(Seg(x + 22, 572, x - 22, 532, 3), (60, 60, 64))
        g.fill(Poly([(x - 26, 530), (x + 26, 530), (x + 22, 546), (x - 22, 546)]), light_y(col, 530, 546, 1.0, 0.6))
        g.fill(Poly([(x - 24, 486), (x + 24, 486), (x + 26, 530), (x - 26, 530)]), lgrad(x - 30, 486, x + 30, 530,
               [(0, mixc(col, (255, 150, 70), 0.25)), (1, mixc(col, (0, 0, 0), 0.4))]))
    # kettle by the fire
    if "kettle" not in d:
        kx, ky = 418, 572
        g.fill(Ell(kx, ky, 20, 16) - Box(kx - 22, ky + 2, kx + 22, ky + 22), sphere_paint(kx, ky - 4, 20, (170, 170, 176), ry=18, amb=0.3, spec=0.6))
        g.fill(Box(kx - 20, ky - 2, kx + 20, ky + 8, 3), (140, 140, 146))
        g.fill(Ell(kx, ky - 20, 14, 10) - Ell(kx, ky - 20, 11, 7) - Box(kx - 16, ky - 20, kx + 16, ky - 8), (60, 60, 64))
        g.fill(Seg(kx + 16, ky - 6, kx + 30, ky - 16, 4, 2), (150, 150, 156))
    # moon low over the mountains
    if "moon" not in d:
        g.glow(780, 110, 50, (200, 210, 255), 0.2)
        g.fill(Circ(780, 110, 17) - Circ(788, 104, 15), (240, 236, 220))
    # canoe pulled up on the shore (right)
    cn = (190, 60, 40)
    g.mul(Ell(790, 482, 100, 8), 0.5, feather=8)
    g.fill(Poly([(690, 462), (890, 462), (870, 482), (710, 482)]), light_y(cn, 462, 482, 0.9, 0.45))
    g.fill(Box(694, 458, 886, 464, 3), (150, 120, 90))
    g.bloom(200, 18, 0.45)
    g.grade(contrast=1.06, sat=1.05)
    g.commit()


def l1509_flame(g, m):
    fx, fy = 520, 518
    g.fill(Rough(Poly([(fx - 26, fy + 4), (fx - 14, fy - 30), (fx - 4, fy - 14), (fx + 4, fy - 52), (fx + 14, fy - 18),
                       (fx + 22, fy - 34), (fx + 28, fy + 4)]), 3, 6, 5), lgrad(fx, fy - 52, fx, fy + 4,
                                                                                [(0, (255, 120, 30)), (0.6, (255, 190, 70)), (1, (255, 240, 170))]))
    g.fill(Poly([(fx - 10, fy + 4), (fx, fy - 26), (fx + 10, fy + 4)]), (255, 250, 210))


L1509_ELEMENTS = [
    E("flame", el(l1509_flame), pivot=(520, 522), daynight="untinted", anim=dict(stretch=(0.06, 0.18), scaleSpeed=1.6, pulse=0.04)),
    E("sparks", el(lambda g, m: [g.glow(520 + dx, 470 + dy, 3, (255, 200, 90), 1.0) for dx, dy in ((-8, 0), (10, -14), (2, -30))]),
      daynight="untinted", anim=dict(driftVelocity=(4, 40), driftLength=80, driftFade=True)),
    E("meteor", el(lambda g, m: (g.add(Seg(140, 40, 220, 80, 2, 0.5), (220, 230, 255), 0.8), g.glow(220, 80, 4, (255, 255, 255), 1.0))),
      daynight="untinted", anim=dict(driftVelocity=(120, -60), driftLength=200, driftFade=True)),
    glint_el("twinkle", [(60, 40), (400, 30), (600, 120), (820, 60), (300, 200), (760, 240)], col=(255, 255, 250), r=3.5, speed=0.6),
    glint_el("fireflies", [(240, 430), (460, 410), (760, 420), (60, 440)], col=(200, 255, 120), r=3, speed=0.4, phase=0.3),
]

L1509_DIFFS = [
    ("pennant", 320, 352, 0),
    ("pack", 168, 542, 0),
    ("moon", 776, 112, 0),
    ("chair", 650, 520, 0),
    ("kettle", 422, 566, 0),
]


LEVELS = [
    ("Level1500", "晨雾山湖", l1500_bg, L1500_ELEMENTS, L1500_DIFFS, 60, OPTS),
    ("Level1501", "海岸灯塔", l1501_bg, L1501_ELEMENTS, L1501_DIFFS, 60, OPTS),
    ("Level1502", "秋林小径", l1502_bg, L1502_ELEMENTS, L1502_DIFFS, 60, OPTS),
    ("Level1503", "峡谷落日", l1503_bg, L1503_ELEMENTS, L1503_DIFFS, 60, OPTS),
    ("Level1504", "雪夜小屋", l1504_bg, L1504_ELEMENTS, L1504_DIFFS, 60, OPTS),
    ("Level1505", "麦田谷仓", l1505_bg, L1505_ELEMENTS, L1505_DIFFS, 60, OPTS),
    ("Level1506", "雨夜街道", l1506_bg, L1506_ELEMENTS, L1506_DIFFS, 60, OPTS),
    ("Level1507", "热带海滩", l1507_bg, L1507_ELEMENTS, L1507_DIFFS, 60, OPTS),
    ("Level1508", "窗边静物", l1508_bg, L1508_ELEMENTS, L1508_DIFFS, 60, OPTS),
    ("Level1509", "星空露营", l1509_bg, L1509_ELEMENTS, L1509_DIFFS, 60, OPTS),
]
