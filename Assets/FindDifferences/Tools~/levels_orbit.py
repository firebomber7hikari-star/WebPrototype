# -*- coding: utf-8 -*-
"""
Level28 纸艺转盘村 - camera-orbit level.

A small paper village on a turntable, seen from three main angles 120° apart. The camera holds each view
for 5 s and turns to the next in 1 s (a switch every 6 s); after 18 s it is back where it started.
Some differences are easier to spot from one particular side.
"""
import math

from fdcore import E, H, W
from orbit3d import Cam, box, circle_pts, cone, cylinder, decal, roof, sphere
from paper import Circ, Poly, RRect, Thick, flat, paper_post, piece, soft_union
from stylekit import drift_across
from weather import cloud

SMALL = (1, 2, 3, 0.3)
CHIMNEY_TOP = (-0.55, -6.55, 3.25)
DIFF_TREE = (6.2, 7.6)        # its ground shadow disappears with it, so the region covers tree + shadow
MILL = (-6.0, 1.5)
MILL_HUB = (-6.0, 1.5, 3.3)
FLAG_TOP = (7.5, -6.0, 4.1)
SHEEP = [(-5.4, 5.6), (-4.2, 6.6), (-6.5, 6.9)]


def sky(c):
    """The turntable stands on a crafting desk: cutting mat, paper sheets and tools fill the frame."""
    c.rect(-10, -10, W + 10, H + 70, (196, 150, 108))
    for y in range(-10, H + 60, 46):
        flat(c, Thick(-10, y, W + 10, y + 6, 2), (178, 134, 96))
    piece(c, RRect(40, 30, 860, 590, 10), (70, 130, 100), shadow=(3, 6, 10, 0.35))
    for x in range(60, 860, 40):
        flat(c, Thick(x, 30, x, 590, 1), (100, 160, 128))
    for y in range(50, 590, 40):
        flat(c, Thick(40, y, 860, y, 1), (100, 160, 128))
    # paper sheets, scissors, pencils, glue and a ruler around the turntable
    piece(c, Poly([(20, 20), (230, 4), (250, 150), (40, 170)]), (250, 220, 120), shadow=(2, 4, 8, 0.35))
    piece(c, Poly([(700, 10), (890, 30), (870, 180), (680, 150)]), (240, 140, 160), shadow=(2, 4, 8, 0.35))
    piece(c, Poly([(10, 440), (190, 420), (210, 590), (20, 600)]), (140, 190, 240), shadow=(2, 4, 8, 0.35))
    for k, col in enumerate(((230, 70, 70), (70, 130, 220), (250, 200, 60))):
        y = 470 + k * 26
        piece(c, [Thick(700, y, 860, y - 20, 9), Poly([(860, y - 20), (884, y - 26), (862, y - 13)])], col, border=1.5, shadow=(2, 4, 4, 0.35))
    piece(c, [Thick(60, 260, 150, 320, 6), Thick(60, 320, 150, 260, 6)], (190, 190, 200), border=1.5, shadow=(2, 4, 4, 0.35))
    piece(c, [Circ(52, 254, 12), Circ(52, 326, 12)], (230, 80, 80), border=1.5, shadow=(2, 4, 4, 0.35))
    piece(c, [RRect(800, 300, 836, 380, 8), RRect(808, 286, 828, 302, 3)], (250, 250, 245), border=1.5, shadow=(2, 4, 4, 0.35))
    flat(c, RRect(804, 320, 832, 350, 3), (120, 170, 230))
    piece(c, RRect(260, 548, 660, 576, 3), (240, 230, 200), border=1.5, shadow=(2, 4, 4, 0.35))
    for x in range(270, 660, 12):
        flat(c, Thick(x, 548, x, 556 if x % 60 else 562, 1.4), (90, 80, 70))


def scene(d):
    o = []
    # ground decals: paths, field, pond
    o.append(decal([(-9.6, -0.8), (9.6, -0.8), (9.6, 0.8), (-9.6, 0.8)], (226, 206, 160)))
    o.append(decal([(-0.8, 0.8), (0.8, 0.8), (0.8, 9.6), (-0.8, 9.6)], (226, 206, 160)))
    o.append(decal([(-8.6, 2.8), (-3.6, 2.8), (-3.6, 8.2), (-8.6, 8.2)], (196, 172, 110)))
    for k in range(6):
        y = 3.3 + k * 0.85
        o.append(decal([(-8.4, y), (-3.8, y), (-3.8, y + 0.3), (-8.4, y + 0.3)], (170, 146, 92), z=0.001))
    o.append(decal(circle_pts(4.6, 4.8, 2.3), (205, 190, 150)))
    o.append(decal(circle_pts(4.6, 4.8, 2.0), (110, 176, 216), z=0.001))
    o.append(decal(circle_pts(4.2, 4.4, 0.7), (160, 205, 232), z=0.002))
    # houses
    o += [box(-4.5, -4.6, 0, 3.0, 2.4, 1.9, (246, 234, 208), rot=15), roof(-4.5, -4.6, 1.9, 3.0, 2.4, 1.3, (200, 76, 66), rot=15)]
    o += [box(4.6, -4.3, 0, 2.6, 2.6, 2.2, (238, 226, 202), rot=-10),
          roof(4.6, -4.3, 2.2, 2.6, 2.6, 1.4, (90, 160, 100) if "roof" in d else (80, 120, 190), rot=-10)]
    o += [box(-1.4, -7.0, 0, 2.8, 2.0, 1.7, (244, 232, 210), rot=5), roof(-1.4, -7.0, 1.7, 2.8, 2.0, 1.1, (150, 96, 70), rot=5),
          box(CHIMNEY_TOP[0], CHIMNEY_TOP[1], 1.9, 0.45, 0.45, CHIMNEY_TOP[2] - 1.9, (170, 96, 82))]
    # door / window boxes stuck on the houses (thin boxes slightly in front of the walls)
    o.append(box(-4.0, -3.4, 0, 0.6, 0.12, 1.1, (120, 80, 60), rot=15))
    o.append(box(4.4, -2.98, 0, 0.6, 0.12, 1.2, (120, 80, 60), rot=-10))
    # windmill
    o += [cylinder(MILL[0], MILL[1], 0, 3.6, 1.0, (242, 234, 216)), cone(MILL[0], MILL[1], 3.6, 4.9, 1.25, (170, 90, 70))]
    # trees (one missing in B)
    for x, y in ((7.6, 1.0), (6.2, 7.6), (-2.4, 7.9), (-8.0, -2.4), (2.1, 3.0), (8.4, -2.8)):
        if (x, y) == DIFF_TREE and "tree" in d:
            continue
        o += [cylinder(x, y, 0, 1.2, 0.25, (130, 90, 64), n=10), sphere(x, y, 1.9, 1.05, (86, 166, 92))]
    # well
    o += [cylinder(1.8, -2.0, 0, 0.7, 0.7, (186, 182, 176)), box(1.25, -2.0, 0.7, 0.12, 0.12, 0.9, (130, 90, 64)),
          box(2.35, -2.0, 0.7, 0.12, 0.12, 0.9, (130, 90, 64)), roof(1.8, -2.0, 1.6, 1.5, 0.9, 0.5, (170, 80, 70))]
    # cart (colour differs)
    cart = (90, 140, 210) if "cart" in d else (176, 116, 72)
    o += [box(3.0, 1.9, 0.35, 1.7, 0.9, 0.5, cart, rot=20)]
    for wx, wy in ((2.4, 1.3), (3.6, 2.5), (2.2, 1.9), (3.4, 2.9)):
        o.append(sphere(wx, wy, 0.32, 0.32, (80, 70, 70)))
    # sheep (one is black in B)
    for x, y in SHEEP:
        col = (60, 56, 62) if ((x, y) == SHEEP[1] and "sheep" in d) else (248, 248, 242)
        o += [sphere(x, y, 0.5, 0.48, col), sphere(x + 0.45, y + 0.1, 0.7, 0.22, (70, 64, 70))]
    # haystack, rocks, fence, flag pole
    o.append(cone(-8.3, 4.2, 0, 1.5, 1.0, (232, 200, 90)))
    for x, y, r in ((8.6, 3.6, 0.45), (-2.6, -3.2, 0.35), (6.8, -7.2, 0.4)):
        o.append(sphere(x, y, r * 0.6, r, (170, 168, 175)))
    for k in range(6):
        o.append(box(-8.7 + k * 1.0, 2.5, 0, 0.14, 0.14, 0.8, (236, 228, 210)))
    o.append(box(-6.2, 2.5, 0.45, 5.2, 0.08, 0.12, (236, 228, 210)))
    o.append(cylinder(FLAG_TOP[0], FLAG_TOP[1], 0, FLAG_TOP[2], 0.08, (120, 110, 115), n=8))
    return o


def view_elements(cam, v):
    """Animated parts placed for one main view."""
    hx, hy = cam.proj(*MILL_HUB)
    # put the blades on the side of the tower that faces the viewer a little
    cx, cy = cam.proj(MILL[0], MILL[1], MILL_HUB[2])
    hx, hy = cx, cy
    sx, sy = cam.proj(*CHIMNEY_TOP)
    fx, fy = cam.proj(*FLAG_TOP)

    def blades(c, m):
        for k in range(4):
            a = math.radians(45 + k * 90)
            ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
            piece(c, Poly([(hx + ux * 8, hy + uy * 8), (hx + ux * 66, hy + uy * 66), (hx + ux * 66 + vx * 16, hy + uy * 66 + vy * 16),
                           (hx + ux * 12 + vx * 11, hy + uy * 12 + vy * 11)]), (250, 246, 236), border=1.5, shadow=SMALL)
        piece(c, Circ(hx, hy, 6), (140, 95, 70), shadow=None)

    def flag(c, m):
        col = (60, 170, 110) if m else (230, 80, 80)
        piece(c, Poly([(fx + 1, fy), (fx + 34, fy + 8), (fx + 1, fy + 16)]), col, border=1.2, shadow=SMALL)

    def puff(c, m):
        piece(c, Circ(sx, sy - 6, 9), (242, 240, 236), shadow=SMALL)

    out = [
        E("mill_v%d" % v, blades, pivot=(hx, hy), anim=dict(rotateSpeed=-80),
          animB=dict(rotateSpeed=80) if "windmill" in USED28 else None),
        E("flag_v%d" % v, flag, pivot=(fx + 1, fy + 8), variant=True,
          anim=dict(stretch=(0.25, 0), scaleSpeed=1.5, swingAngle=4, swingSpeed=1.1)),
    ]
    out += [E("smoke_v%d_%d" % (v, i), puff, show="A" if "smoke" in USED28 else "both",
              anim=dict(driftVelocity=(5, 22), driftLength=64, driftFade=True, driftGrow=1.3, phase=i / 3)) for i in range(3)]
    return out


def bird(x, y, s):
    def d(c, m):
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.25), Thick(x, y, x + s, y - s * 0.4, s * 0.25)], (90, 95, 110),
              shadow=(1, 3, 4, 0.25))
    return d


GLOBAL_ELEMENTS = []

DIFFS3D = [
    ("roof", (4.6, -4.3, 2.8), 68),
    ("tree", (DIFF_TREE[0] + 0.95, DIFF_TREE[1] - 0.8, 1.1), 86),
    ("smoke", (CHIMNEY_TOP[0], CHIMNEY_TOP[1], CHIMNEY_TOP[2] + 1.5), 48),
    ("windmill", (MILL[0], MILL[1], MILL_HUB[2]), 66),
    ("flag", FLAG_TOP, 30, (18, 8)),
    ("sheep", (SHEEP[1][0] + 0.2, SHEEP[1][1], 0.55), 26),
    ("cart", (3.0, 1.9, 0.6), 40),
]


# differences actually used: 3-5 that stay >= 135 px apart (edge to edge) in all three camera views (see diff_select.py)
USED28 = {"tree", "flag", "sheep"}


def build(name, title, time_limit, **kw):
    from orbit3d import build_orbit_level
    build_orbit_level(name, title, scene, view_elements, GLOBAL_ELEMENTS, [d for d in DIFFS3D if d[0] in USED28], time_limit, sky,
                      frames=24, view_count=3, hold=5.0, turn=1.0, post=paper_post, **kw)


LEVELS = [
    ("Level28", "纸艺转盘村", None, None, None, 150, {"custom": build}),
]
