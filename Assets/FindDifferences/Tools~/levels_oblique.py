# -*- coding: utf-8 -*-
"""Level123 纸艺露营地 - a paper campsite in 45-degree overhead view (oblique.py): every object is a paper cut-out solid
(lit top, darker front, light and shaded roof slopes) and the sun at the upper left casts real shadows onto the ground.
Animated: campfire flames and smoke, a waving flag, a bird crossing the site with its shadow gliding over the grass,
butterflies and sparkles on the lake.
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, drift_across
from oblique import (K, SHADOW_COL, SX, SY, Scene, ball, box, cone, cylinder, figure, ground_ellipse, ground_poly, p, shadow_pt, tent, tree_pine,
                     tree_round)

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
FIRE = (330, 300)
FLAG = (470, 420, 160)
LAKE = (690, 640, 220, 170)
TREE_DIFF = (870, 430)


def l123_scene(d):
    sc = Scene()
    # tents, campfire with log seats and campers
    tent(sc, 170, 430, 96, 120, 74, (230, 120, 50))
    tent(sc, 330, 520, 84, 104, 62, (80, 170, 110) if "tent" in d else (70, 120, 200))
    for k in range(10):
        a = 2 * math.pi * k / 10
        ball(sc, FIRE[0] + 26 * math.cos(a), FIRE[1] + 26 * math.sin(a), 5, 6, (150, 146, 140))
    box(sc, FIRE[0] - 18, FIRE[1] - 4, FIRE[0] + 18, FIRE[1] + 4, 6, (120, 80, 56))
    box(sc, FIRE[0] - 4, FIRE[1] - 18, FIRE[0] + 4, FIRE[1] + 18, 10, (110, 74, 50))
    box(sc, 270, 228, 390, 244, 14, (140, 96, 64), front=(110, 74, 50))
    box(sc, 230, 270, 248, 340, 14, (140, 96, 64), front=(110, 74, 50))
    figure(sc, 300, 222, (200, 60, 70))
    figure(sc, 360, 220, (60, 90, 160), hair=(220, 180, 90))
    figure(sc, 222, 300, (90, 140, 90))
    # picnic table with a basket and a lantern
    for x, y in ((508, 266), (612, 266), (508, 314), (612, 314)):
        cylinder(sc, x, y, 3, 30, (130, 90, 60))
    box(sc, 498, 258, 622, 322, 6, (170, 120, 80), z0=30)
    box(sc, 498, 236, 622, 248, 4, (160, 110, 72), z0=18)
    box(sc, 498, 332, 622, 344, 4, (160, 110, 72), z0=18)
    if "basket" not in d:
        box(sc, 528, 280, 562, 302, 14, (190, 150, 90), z0=36, detail=lambda c: flat(c, Thick(*p(530, 280, 50), *p(560, 280, 50), 1.4), (150, 110, 60)), sort_y=257)
    cylinder(sc, 594, 296, 5, 14, (60, 70, 80), z0=36, top=(250, 230, 150), sort_y=257)
    # cooler and camper van
    box(sc, 640, 200, 690, 230, 26, (230, 230, 236), top=(60, 140, 220) if "cooler" in d else (220, 60, 60))

    def van_detail(c):
        stripe = (60, 150, 220) if "van" in d else (230, 120, 50)
        flat(c, Poly([p(96, 150, 30), p(264, 150, 30), p(264, 150, 38), p(96, 150, 38)]), stripe)
        for x0 in (110, 160, 210):
            flat(c, Poly([p(x0, 150, 46), p(x0 + 36, 150, 46), p(x0 + 36, 150, 64), p(x0, 150, 64)]), (170, 210, 230))
        for x in (126, 236):
            xx, yy = p(x, 150, 0)
            flat(c, Ell(xx, yy, 14, 9), (40, 40, 46))
    box(sc, 96, 150, 264, 214, 72, (240, 232, 214), detail=van_detail)
    # flag pole
    cylinder(sc, FLAG[0], FLAG[1], 3, FLAG[2], (200, 200, 210))
    # dog, rocks, cooler, firewood stack
    box(sc, 420, 250, 446, 262, 12, (200, 160, 110), z0=6)
    ball(sc, 450, 256, 22, 7, (200, 160, 110))
    for x, y, r in ((90, 300, 14), (110, 312, 9), (780, 470, 12), (450, 600, 10)):
        ball(sc, x, y, r * 0.5, r, (160, 156, 150))
    for k in range(3):
        cylinder(sc, 420 + k * 12, 360, 6, 8, (130, 90, 60), top=(220, 190, 140))
    # kids playing near a picnic blanket
    figure(sc, 560, 110, (240, 200, 60), s=0.8)
    figure(sc, 690, 96, (150, 90, 200), hair=(220, 180, 90), s=0.8)
    box(sc, 200, 70, 250, 100, 30, (90, 150, 210), top=(120, 180, 230))
    for x, y in ((180, 110), (300, 90)):
        tree_round(sc, x, y, 0.8, (110, 180, 90)) if x == 300 else ball(sc, x, y, 12, 16, (90, 160, 80))
    # trees around the site (one round tree is missing in B)
    for x, y, s in ((50, 700, 1.3), (150, 790, 1.4), (260, 850, 1.2), (420, 880, 1.3), (60, 560, 1.1), (900, 880, 1.2), (760, 880, 1.0), (40, 260, 1.0)):
        tree_pine(sc, x, y, s)
    for x, y, s, col in ((560, 860, 1.2, (90, 160, 90)), (TREE_DIFF[0], TREE_DIFF[1], 1.1, (100, 170, 80)), (880, 260, 1.2, (80, 150, 90)),
                         (760, 140, 1.0, (110, 170, 90))):
        if (x, y) == TREE_DIFF and "tree" in d:
            continue
        tree_round(sc, x, y, s, col)
    return sc


def l123_bg(c, d):
    c.rect(0, 0, W, H, (140, 190, 110))
    rnd = random.Random(123)
    for _ in range(260):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        flat(c, Thick(x, y, x + rnd.uniform(-3, 3), y - rnd.uniform(4, 8), 1.4), rnd.choice(((120, 172, 96), (160, 206, 126))))
    # lake with a pier and a canoe
    lx, ly, rx, ry = LAKE
    ground_ellipse(c, lx, ly, rx + 14, ry + 12, (200, 190, 150))
    ground_ellipse(c, lx, ly, rx, ry, (90, 160, 200))
    ground_ellipse(c, lx + 20, ly + 20, rx * 0.7, ry * 0.6, (110, 180, 214))
    # dirt path and flower patches
    ground_poly(c, [(360, 40), (420, 40), (400, 200), (370, 260), (300, 260), (330, 200)], (214, 190, 140))
    ground_poly(c, [(300, 340), (360, 340), (520, 520), (560, 560), (520, 570), (480, 540)], (214, 190, 140))
    for _ in range(40):
        x, y = rnd.uniform(0, 900), rnd.uniform(60, 900)
        if (x - lx) ** 2 / (rx + 30) ** 2 + (y - ly) ** 2 / (ry + 30) ** 2 < 1:
            continue
        flat(c, Circ(*p(x, y), 3), rnd.choice(((250, 230, 90), (250, 250, 250), (240, 150, 190))))
    for k in range(6):
        for j in range(4):
            col = (230, 80, 80) if (k + j) % 2 else (250, 246, 240)
            ground_poly(c, [(760 + k * 20, 70 + j * 18), (780 + k * 20, 70 + j * 18), (780 + k * 20, 88 + j * 18), (760 + k * 20, 88 + j * 18)], col)
    ground_ellipse(c, 625, 150, 10, 6, (90, 110, 90))
    sc = l123_scene(d)
    # pier and canoe live on the lake: their shadows go onto the water
    box(sc, 520, 560, 556, 700, 6, (170, 130, 90))
    canoe = (230, 200, 70) if "canoe" in d else (220, 80, 60)

    def canoe_d(c):
        pts = [p(620 + 70 * math.cos(a), 660 + 14 * math.sin(a), 8) for a in [k * math.pi / 12 for k in range(24)]]
        piece(c, Poly(pts), canoe, border=1.2, shadow=None)
        flat(c, Poly([p(620 + 58 * math.cos(a), 660 + 9 * math.sin(a), 9) for a in [k * math.pi / 12 for k in range(24)]]), lit(canoe, 0.7))
    sc.cast([(620 + 70 * math.cos(a), 660 + 14 * math.sin(a), 8) for a in [k * math.pi / 6 for k in range(12)]])
    sc.add(646, canoe_d)
    sc.paint(c)


def l123_flame(c, m):
    x, y = p(FIRE[0], FIRE[1], 14)
    soft_union(c, [Circ(x, y - 8, 16)], (255, 170, 70), 0.55, spread=22)
    flat(c, Poly([(x - 12, y), (x + 12, y), (x + 8, y - 16), (x, y - 34), (x - 8, y - 16)]), (255, 130, 40))
    flat(c, Poly([(x - 6, y), (x + 6, y), (x, y - 18)]), (255, 230, 130))


def l123_flag(c, m):
    X, Y, Z = FLAG
    x, y = p(X, Y, Z)
    col = (60, 160, 90) if m else (230, 60, 60)
    piece(c, Poly([(x + 2, y + 2), (x + 46, y + 8), (x + 46, y + 32), (x + 2, y + 30)]), col, border=1.2, shadow=None)
    flat(c, Circ(x + 22, y + 17, 6), (250, 250, 246))


def l123_flag_shadow(c, m):
    X, Y, Z = FLAG
    pts = [shadow_pt(X + dx, Y, Z - dz) for dx, dz in ((0, 0), (46, 8), (46, 32), (0, 30))]
    soft_union(c, [Poly([p(x, y) for x, y in pts])], SHADOW_COL, 0.3, spread=4)


def bird_with_shadow(i, X, Y, Z, s=9, speed=22):
    def d(c, m):
        sx, sy = shadow_pt(X, Y, Z)
        gx, gy = p(sx, sy)
        soft_union(c, [Thick(gx - s, gy - s * 0.3, gx, gy, s * 0.35), Thick(gx, gy, gx + s, gy - s * 0.3, s * 0.35)], SHADOW_COL, 0.3, spread=3)
        x, y = p(X, Y, Z)
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.28), Thick(x, y, x + s, y - s * 0.4, s * 0.28)], (60, 64, 80), shadow=None)
    return E("bird%d" % i, d, anim=dict(drift_across(X - 20, X + 200, speed, X), bobAmplitude=(0, 0)))


L123_ELEMENTS = [
    E("flag_shadow", l123_flag_shadow, pivot=p(*shadow_pt(FLAG[0], FLAG[1], FLAG[2] - 16)), anim=dict(stretch=(0.15, 0), scaleSpeed=1.2)),
    E("flag", l123_flag, pivot=p(FLAG[0], FLAG[1], FLAG[2] - 16), variant=True, anim=dict(stretch=(0.15, 0), scaleSpeed=1.2, swingAngle=3, swingSpeed=0.8)),
    E("flame", l123_flame, pivot=p(FIRE[0], FIRE[1], 14), daynight="untinted",
      anim=dict(stretch=(0.12, 0.25), scaleSpeed=2.6, twinkle=0.15, twinkleSpeed=3.0)),
] + [E("smoke%d" % i, (lambda: lambda c, m: piece(c, Circ(*p(FIRE[0] + 4, FIRE[1], 40), 8), (230, 230, 236), shadow=None))(),
       anim=dict(driftVelocity=(8, 26), driftLength=110, driftFade=True, driftGrow=1.4, phase=i / 3)) for i in range(3)] + [
    E("kid_ball", lambda c, m: (piece(c, Circ(*p(625, 150, 14), 9), (240, 90, 80), border=1, shadow=None),
                                flat(c, Thick(p(625, 150, 14)[0] - 9, p(625, 150, 14)[1], p(625, 150, 14)[0] + 9, p(625, 150, 14)[1], 2), (250, 250, 250))),
      pivot=p(625, 150, 6), anim=dict(bobAmplitude=(0, 50), bobSpeed=0.5, bounce=True)),
    bird_with_shadow(0, 200, 520, 220, 10, 24), bird_with_shadow(1, 240, 560, 230, 8, 24),
] + [E("sparkle%d" % i, (lambda x, y: lambda c, m: flat(c, Poly(star_pts(x, y, 6, 1.8, points=4, rot=0)), (255, 255, 250)))(*p(X, Y)),
       anim=dict(twinkle=0.95, twinkleSpeed=0.5 + i * 0.12, phase=i * 0.2)) for i, (X, Y) in enumerate(((640, 700), (760, 600), (700, 560), (820, 680)))] + [
    E("butterfly%d" % i, (lambda x, y, col: lambda c, m: flat(c, [Ell(x - 5, y - 3, 5, 4), Ell(x + 5, y - 3, 5, 4), Ell(x - 4, y + 3, 4, 3),
                                                                   Ell(x + 4, y + 3, 4, 3)], col))(*p(X, Y, 30), col), pivot=p(X, Y, 30),
      anim=dict(stretch=(0.6, 0), scaleSpeed=3, bobAmplitude=(30, 16), bobSpeed=0.12 + i * 0.03, phase=i * 0.3))
    for i, (X, Y, col) in enumerate(((150, 260, (250, 200, 70)), (720, 340, (240, 150, 200))))]

L123_DIFFS = [
    ("tent", *p(330, 560, 30), 0),
    ("basket", *p(545, 291, 43), 0),
    ("cooler", *p(665, 215, 26), 0),
    ("van", *p(180, 150, 34), 0),
    ("tree", *p(TREE_DIFF[0], TREE_DIFF[1], 66), 0),
    ("canoe", *p(620, 660, 8), 0),
    ("flag", *p(FLAG[0] + 22, FLAG[1], FLAG[2] - 17), 0),
]

LEVELS = [
    ("Level123", "纸艺露营地", l123_bg, L123_ELEMENTS, L123_DIFFS, 140, OPTS),
]
