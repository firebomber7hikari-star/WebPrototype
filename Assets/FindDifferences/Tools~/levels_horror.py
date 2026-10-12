# -*- coding: utf-8 -*-
"""Psychological-horror levels (perspective paper interiors, persp.Cam + paper25):
  Level66 无尽走廊 - endless hotel corridor: flickering lamps, numbered doors, a small figure far away
  Level67 童年卧室 - a child's bedroom at night: eyes under the bed and in the wardrobe, a shadow on the wall
  Level68 无人晚宴 - a dinner laid out for nobody: candles, portraits, someone standing in the mirror

Unsettling rather than gory: wrong details, watching eyes, things that should not be there.
"""
import math
import random

from fdcore import E, lit
from paper import paper_post
from paper25 import paper_level
from persp import Cam, seven_seg

OPTS = dict(post=paper_post, anim_seconds=10.0, frames=60)
INK = (24, 20, 22)


def glow_circles(c, x, y, r, col, a=0.07, n=5):
    for k in range(n):
        c.circle(x, y, r * (1 - k / n), tuple(col) + (a,))


def flame(c, x, y, s=1.0):
    """Candle flame with halo, (x, y) = wick."""
    glow_circles(c, x, y - 6 * s, 26 * s, (255, 200, 110), 0.06)
    c.polygon([(x - 4 * s, y - 2 * s), (x, y - 16 * s), (x + 4 * s, y - 2 * s), (x, y + 1 * s)], (255, 210, 110, 1.0))
    c.polygon([(x - 2 * s, y - 2 * s), (x, y - 9 * s), (x + 2 * s, y - 2 * s)], (255, 250, 220, 1.0))


def flame_el(eid, x, y, s, phase, show="both"):
    return E(eid, lambda c, m: flame(c, x, y, s), pivot=(x, y), show=show,
             anim=dict(stretch=(0.1, 0.18), scaleSpeed=1.7 + phase, twinkle=0.25, twinkleSpeed=2.3 + phase, phase=phase))


def rotate_pts(pts, a, ox=0.0, oy=0.0):
    ca, sa = math.cos(a), math.sin(a)
    return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in pts]


# =================================================================== Level 66 endless corridor
C66 = Cam(vpx=450, vpy=290, f=300, dark=(12, 14, 12), fog=(1.5, 15.0), fog_k=0.72)
XW, YF, YC, ZN, ZF = 1.5, -1.6, 1.25, 0.85, 15.0
LAMPS66 = [2.2, 4.6, 7.0, 9.4, 11.8, 14.2]
DOORS66 = [(-XW, 3.0, "101"), (-XW, 6.0, "103"), (-XW, 9.0, "105"), (-XW, 12.0, "107"),
           (XW, 4.5, "102"), (XW, 7.5, "104"), (XW, 10.5, "106"), (XW, 13.5, "108")]
XF_TABLE66 = C66.at(-1.18, YF, 2.0)
XF_CHAIR66 = C66.at(1.12, YF, 2.2)


def l66_door(c, X, zc, num, idx):
    cam = C66
    z0, z1 = zc - 0.45, zc + 0.45
    cam.wall_rect(c, X, z0 - 0.08, z1 + 0.08, YF, 0.58, (66, 48, 36))
    col = [(122, 92, 64), (108, 84, 62)][idx % 2]
    cam.wall_rect(c, X, z0, z1, YF, 0.5, col)
    for ya, yb in ((-1.35, -0.7), (-0.5, 0.1)):
        cam.wall_rect(c, X, z0 + 0.1, z1 - 0.1, ya, yb, lit(col, 0.86))
    kz = z1 - 0.1 if X < 0 else z0 + 0.1
    x, y = cam.p(X, -0.55, kz)
    c.circle(x, y, max(1.2, 0.035 * cam.s(kz)), cam.col((200, 170, 90), kz))
    cam.wall_rect(c, X, zc - 0.2, zc + 0.2, 0.2, 0.44, (186, 156, 88))
    seven_seg(c, cam, X, zc - 0.14 if X < 0 else zc + 0.14, 0.25, 0.14, num, (46, 36, 26), 0.014)


def l66_portrait(c, X, zc, eyes, female):
    cam = C66
    cam.wall_rect(c, X, zc - 0.36, zc + 0.36, -0.16, 0.76, (122, 92, 40))
    cam.wall_rect(c, X, zc - 0.3, zc + 0.3, -0.1, 0.7, (52, 50, 44) if eyes == "open" else (128, 36, 40))   # hollow-eyed: red ground
    cam.wall_ellipse(c, X, zc, -0.1, 0.24, 0.16, (40, 44, 60))                 # shoulders
    hair = (70, 50, 36) if female else (50, 44, 40)
    cam.wall_ellipse(c, X, zc, 0.42, 0.15, 0.2 if female else 0.15, hair)
    cam.wall_ellipse(c, X, zc, 0.36, 0.12, 0.16, (206, 186, 160))
    if eyes == "open":
        for dz in (-0.05, 0.05):
            cam.wall_ellipse(c, X, zc + dz, 0.39, 0.03, 0.018, (236, 232, 220), n=12)
            cam.wall_ellipse(c, X, zc + dz, 0.39, 0.013, 0.013, INK, n=10)
    else:                                                               # hollow black eyes
        for dz in (-0.05, 0.05):
            cam.wall_ellipse(c, X, zc + dz, 0.385, 0.035, 0.03, (8, 6, 8), n=12)
    cam.line(c, (X, 0.29, zc - 0.04), (X, 0.29, zc + 0.04), 0.012, (120, 70, 60))


CLOCK66 = (4.3, 0.62)


def l66_clock(c, hands):
    cam, X, (zc, yc) = C66, -XW, CLOCK66
    cam.wall_ellipse(c, X, zc, yc, 0.36, 0.36, (80, 60, 44))
    cam.wall_ellipse(c, X, zc, yc, 0.31, 0.31, (214, 206, 182) if hands else (150, 176, 206))
    for k in range(12):
        a = k * math.pi / 6
        cam.line(c, (X, yc + 0.25 * math.cos(a), zc + 0.25 * math.sin(a)), (X, yc + 0.29 * math.cos(a), zc + 0.29 * math.sin(a)), 0.016, INK)
    if hands:
        cam.line(c, (X, yc, zc), (X, yc + 0.24, zc + 0.03), 0.03, INK)
        cam.line(c, (X, yc, zc), (X, yc - 0.08, zc + 0.16), 0.04, INK)


def l66_tally(c, groups, extra):
    cam, X = C66, XW
    z = 3.25
    for g in range(groups + (1 if extra else 0)):
        n = 4 if g < groups else extra
        for k in range(n):
            cam.line(c, (X, -0.42, z + k * 0.04), (X, -0.16, z + k * 0.04), 0.012, (40, 34, 30))
        if g < groups:
            cam.line(c, (X, -0.38, z - 0.03), (X, -0.2, z + 0.15), 0.012, (40, 34, 30))
        z += 0.22


def l66_table(c, d):
    c.rect(-28, -80, 28, -73, (110, 74, 50))
    c.rect(-25, -73, 25, -56, (96, 64, 44))
    c.circle(0, -64, 2.5, (200, 170, 90))
    for x in (-24, 20):
        c.rect(x, -56, x + 4, 0, (90, 60, 42))
    c.polygon([(-8, -80), (8, -80), (11, -96), (5, -110), (-5, -110), (-11, -96)], (90, 110, 120))
    if "flowers" in d:          # wilted: drooping grey stems, petals fallen on the table
        for sx, ex, ey in ((-3, -18, -104), (0, 2, -122), (3, 17, -100)):
            c.line(sx, -108, (sx + ex) / 2, -128, 2, (110, 104, 80))
            c.line((sx + ex) / 2, -128, ex, ey, 2, (110, 104, 80))
            c.circle(ex, ey, 5, (96, 74, 70))
        for px in (-20, -14, 16):
            c.ellipse(px, -81, 3, 1.5, (110, 60, 60))
    else:
        for sx, ex, ey in ((-3, -12, -136), (0, 0, -146), (3, 11, -134)):
            c.line(sx, -108, ex, ey, 2, (60, 110, 60))
            c.circle(ex, ey, 6.5, (190, 30, 44))
            c.circle(ex - 1.5, ey - 1.5, 2.5, (230, 70, 80))


def l66_chair(c, d):
    parts = [([(-20, -48), (20, -48), (20, -42), (-20, -42)], (110, 76, 52)),
             ([(-20, -42), (-16, -42), (-16, 0), (-20, 0)], (92, 62, 44)), ([(16, -42), (20, -42), (20, 0), (16, 0)], (92, 62, 44)),
             ([(-20, -95), (-16, -95), (-16, -48), (-20, -48)], (92, 62, 44)), ([(16, -95), (20, -95), (20, -48), (16, -48)], (92, 62, 44)),
             ([(-18, -92), (18, -92), (18, -80), (-18, -80)], (110, 76, 52)), ([(-18, -70), (18, -70), (18, -62), (-18, -62)], (110, 76, 52))]
    tipped = "chair" in d
    for pts, col in parts:
        if tipped:
            pts = [(x, y) for x, y in rotate_pts(pts, math.radians(-84), 20, 0)]
        c.polygon(pts, col)


def l66_tricycle(c, d):
    c.circle(-22, -12, 12, (40, 40, 44))
    c.circle(-22, -12, 5, (150, 150, 160))
    c.circle(26, -9, 9, (40, 40, 44))
    c.line(-22, -12, 26, -9, 4, (170, 50, 50))
    c.line(-22, -12, -16, -42, 4, (170, 50, 50))
    c.line(-26, -42, -8, -42, 3, (60, 60, 64))
    c.round_rect(4, -24, 22, -18, 3, (60, 60, 64))


def l66_bg(c, d):
    cam = C66
    cam.depth_strips(c, lambda a, b: [(-XW, YC, a), (XW, YC, a), (XW, YC, b), (-XW, YC, b)], ZN, ZF, (74, 70, 60))
    cam.depth_strips(c, lambda a, b: [(-XW, YC, a), (-XW, YC, b), (-XW, YF, b), (-XW, YF, a)], ZN, ZF, (120, 130, 100))
    cam.depth_strips(c, lambda a, b: [(XW, YC, a), (XW, YC, b), (XW, YF, b), (XW, YF, a)], ZN, ZF, (112, 122, 94))
    cam.depth_strips(c, lambda a, b: [(-XW, YF, a), (XW, YF, a), (XW, YF, b), (-XW, YF, b)], ZN, ZF, (96, 72, 52))
    for X in (-XW, XW):                                                     # wainscot + dado rail + wallpaper stripes
        cam.depth_strips(c, lambda a, b, X=X: [(X, -0.55, a), (X, -0.55, b), (X, YF, b), (X, YF, a)], ZN, ZF, (80, 66, 52))
        cam.depth_strips(c, lambda a, b, X=X: [(X, -0.5, a), (X, -0.5, b), (X, -0.58, b), (X, -0.58, a)], ZN, ZF, (150, 128, 96), n=12)
        z = 0.95
        while z < ZF:
            cam.line(c, (X, YC, z), (X, -0.5, z), 0.03, (100, 112, 84))
            z += 0.3
    x = -XW
    while x <= XW + 0.01:                                                   # floor boards
        cam.line(c, (x, YF, ZN), (x, YF, ZF), 0.012, (70, 52, 40))
        x += 0.18
    cam.back_rect(c, ZF, -XW, XW, YF, YC, (108, 116, 90), flat=True)
    cam.back_rect(c, ZF, -XW, XW, YF, -0.55, (80, 66, 52), flat=True)
    # far door: ajar with warm light (A) / shut (B)
    cam.back_rect(c, ZF, -0.53, 0.53, YF, 0.58, (66, 48, 36), flat=True)
    if "door" in d:
        cam.back_rect(c, ZF, -0.45, 0.45, YF, 0.5, (118, 90, 62), flat=True)
    else:
        cam.back_rect(c, ZF, -0.45, 0.45, YF, 0.5, (255, 214, 140), flat=True, glow=True)
        cam.back_rect(c, ZF, -0.45, 0.18, YF, 0.5, (118, 90, 62), flat=True)
        cam.floor_poly(c, YF, [(0.18, ZF), (0.45, ZF), (0.8, ZF - 2.5), (0.25, ZF - 2.5)], (255, 214, 140, 0.25), glow=True)
    # runner carpet with diamonds and wet footprints
    cam.floor_rect(c, YF, -0.55, 0.55, ZN, ZF, (104, 34, 38))
    for X in (-0.47, 0.47):
        cam.line(c, (X, YF, ZN), (X, YF, ZF), 0.02, (160, 120, 70))
    z = 1.5
    while z < ZF:
        cam.floor_poly(c, YF, [(0, z - 0.3), (0.28, z), (0, z + 0.3), (-0.28, z)], (138, 64, 52))
        z += 1.0
    for k in range(16):
        z = 1.2 + k * 0.42
        xx = (0.12 if k % 2 else -0.12) - max(0.0, z - 4.6) * 0.32
        cam.floor_ellipse(c, YF, xx, z, 0.05, 0.11, (54, 18, 22), n=12)
    # light pools under the lamps
    for zl in LAMPS66:
        cam.floor_ellipse(c, YF, 0, zl, 0.95, 0.95, (255, 226, 150, 0.09), glow=True)
        cam.floor_ellipse(c, YF, 0, zl, 0.55, 0.55, (255, 226, 150, 0.07), glow=True)
    # wall furniture, far to near
    items = [(zc, l66_door, (X, zc, ("104" if "number" in d else num) if (X, zc) == (-XW, 3.0) else num, i))
             for i, (X, zc, num) in enumerate(DOORS66)]
    items += [(2.6, l66_portrait, (XW, 2.6, "hollow" if "portrait" in d else "open", False)),
              (7.5, l66_portrait, (-XW, 7.5, "open", True)), (12.0, l66_portrait, (XW, 12.0, "open", True)),
              (CLOCK66[0], l66_clock, ("clock" not in d,)), (3.5, l66_tally, ((2, 2) if "tally" in d else (3, 0)))]
    for zc, fn, args in sorted(items, key=lambda it: -it[0]):
        fn(c, *args)
    for zl in LAMPS66[1:]:                                                  # lamp shades (the nearest lamp is animated)
        cam.line(c, (0, YC, zl), (0, 0.9, zl), 0.012, (40, 40, 36))
        C66.at(0, 0.9, zl).canvas(c).polygon([(-7, 0), (7, 0), (17, 15), (-17, 15)], (62, 66, 52))
    if "vent" not in d:                                                     # air vent high on the near right wall
        cam.wall_rect(c, XW, 1.2, 1.62, 0.52, 0.92, (70, 72, 66))
        cam.wall_rect(c, XW, 1.24, 1.58, 0.56, 0.88, (150, 154, 146))
        y = 0.6
        while y < 0.86:
            cam.line(c, (XW, y, 1.25), (XW, y, 1.57), 0.012, (70, 72, 66))
            y += 0.05
    l66_tricycle(C66.at(-0.5, YF, 6.6).canvas(c), d)
    l66_chair(XF_CHAIR66.canvas(c), d)
    l66_table(XF_TABLE66.canvas(c), d)


def l66_bulb(zl, cord=False):
    def draw(c, m):
        cam = C66
        if cord:
            cam.line(c, (0, YC, zl), (0, 0.9, zl), 0.012, (40, 40, 36))
            C66.at(0, 0.9, zl).canvas(c).polygon([(-7, 0), (7, 0), (17, 15), (-17, 15)], (62, 66, 52))
        x, y = cam.p(0, 0.9 - 0.17, zl)
        s = cam.s(zl)
        glow_circles(c, x, y, 0.55 * s, (255, 220, 150), 0.06, 6)
        c.circle(x, y, 0.045 * s, (255, 244, 200, 1.0))
    return draw


def l66_figure(c, m):
    c.line(-6, 0, -6, -24, 5, (18, 18, 20))
    c.line(6, 0, 6, -24, 5, (18, 18, 20))
    c.polygon([(-24, -18), (24, -18), (10, -72), (-10, -72)], (18, 18, 20))
    c.polygon([(-13, -96), (13, -96), (16, -56), (-16, -56)], (18, 18, 20))
    c.circle(0, -86, 11, (30, 28, 30))


def l66_dust(i):
    rnd = random.Random(660 + i)
    x, y = C66.p(rnd.uniform(-0.6, 0.6), rnd.uniform(-1.0, 0.5), rnd.uniform(1.8, 3.0))
    return E("dust%d" % i, lambda c, m: c.circle(x, y, 1.6, (255, 240, 200, 0.7)),
             anim=dict(driftVelocity=(rnd.uniform(-3, 3), 6), driftLength=60, driftFade=True, phase=i / 6))


def _lamp_el(i, zl):
    if i == 0:
        return E("lamp0", l66_bulb(zl, cord=True), pivot=C66.p(0, YC, zl), anim=dict(swingAngle=4, swingSpeed=0.18, twinkle=0.1,
                                                                                         twinkleSpeed=0.4))
    if zl == 7.0:          # the broken one
        return E("lamp%d" % i, l66_bulb(zl), anim=dict(twinkle=0.95, twinkleSpeed=2.9, phase=0.3))
    return E("lamp%d" % i, l66_bulb(zl), anim=dict(twinkle=0.12, twinkleSpeed=0.35, phase=i * 0.2))


L66_ELEMENTS = [_lamp_el(i, zl) for i, zl in enumerate(LAMPS66)] + [
    E("figure", C66.at(0.06, YF, 14.0).draw(l66_figure), anim=dict(twinkle=0.9, twinkleSpeed=0.06, phase=0.35)),
] + [l66_dust(i) for i in range(6)]

L66_DIFFS = [
    ("number", *C66.p(-XW, 0.32, 3.0), 0),
    ("portrait", *C66.p(XW, 0.38, 2.6), 0),
    ("clock", *C66.p(-XW, CLOCK66[1], CLOCK66[0]), 0),
    ("tally", *C66.p(XW, -0.29, 3.6), 0),
    ("flowers", *XF_TABLE66.p(0, -120), 0),
    ("chair", *XF_CHAIR66.p(0, -45), 0),
    ("door", *C66.p(0.3, -0.5, ZF), 0),
    ("vent", *C66.p(XW, 0.72, 1.41), 0),
]


# =================================================================== Level 67 child's bedroom at night
C67 = Cam(vpx=450, vpy=270, f=320, dark=(12, 14, 30), fog=(1.3, 6.5), fog_k=0.45)
XL7, XR7, YF7, YC7, ZB7, ZN7 = -1.9, 1.9, -1.25, 1.5, 4.2, 0.9
XF_TEDDY = C67.at(-1.38, -0.78, 2.6)
XF_BLOCKS = C67.at(-0.3, YF7, 1.6)
XF_SLIPPERS = C67.at(-0.6, YF7, 1.25)
XF_HORSE = C67.at(0.62, YF7, 2.0)
XF_MUSIC = C67.at(0.05, YF7, 3.0)


def stick_figure(cam, c, Z, x, y, h, col, arms=0.06):
    cam.back_ellipse(c, Z, x, y + h * 0.82, h * 0.13, h * 0.13, col, n=12)
    cam.line(c, (x, y + h * 0.7, Z), (x, y + h * 0.3, Z), 0.012, col)
    cam.line(c, (x - arms, y + h * 0.55, Z), (x + arms, y + h * 0.55, Z), 0.012, col)
    cam.line(c, (x, y + h * 0.3, Z), (x - h * 0.15, y, Z), 0.012, col)
    cam.line(c, (x, y + h * 0.3, Z), (x + h * 0.15, y, Z), 0.012, col)


def l67_back_wall(c, d):
    cam, Z = C67, ZB7
    # window with the night outside
    cam.back_rect(c, Z, -0.64, 0.64, -0.2, 1.04, (226, 222, 206))
    cam.back_rect(c, Z, -0.55, 0.55, -0.11, 0.95, (30, 40, 82), glow=True)
    cam.back_ellipse(c, Z, 0.26, 0.64, 0.15, 0.15, (240, 238, 212), glow=True)
    cam.back_ellipse(c, Z, 0.31, 0.68, 0.12, 0.12, (30, 40, 82), glow=True)
    for a, b in (((-0.55, 0.1), (-0.1, 0.4)), ((-0.25, 0.27), (-0.2, 0.62)), ((-0.1, 0.4), (0.08, 0.5)), ((-0.55, 0.3), (-0.38, 0.38))):
        cam.line(c, (a[0], a[1], Z), (b[0], b[1], Z), 0.025, (14, 16, 30), glow=True)
    if "hand" in d:                     # a hand print on the glass
        hx, hy = -0.2, 0.18
        cam.back_ellipse(c, Z, hx, hy, 0.07, 0.08, (210, 216, 230, 0.6), glow=True)
        for k, (dx, ln) in enumerate(((-0.06, 0.1), (-0.025, 0.14), (0.01, 0.15), (0.045, 0.13), (0.085, 0.07))):
            cam.line(c, (hx + dx, hy + 0.04, Z), (hx + dx * 1.3, hy + 0.04 + ln, Z), 0.024, (210, 216, 230, 0.6), flat=False, glow=True)
    cam.back_rect(c, Z, -0.02, 0.02, -0.11, 0.95, (226, 222, 206))
    cam.back_rect(c, Z, -0.55, 0.55, 0.4, 0.44, (226, 222, 206))
    cam.back_rect(c, Z, -0.72, 0.72, -0.26, -0.19, (236, 232, 218))
    # crayon drawings
    cam.back_rect(c, Z, -1.58, -0.88, 0.22, 0.76, (236, 232, 218))
    cam.back_ellipse(c, Z, -1.47, 0.65, 0.05, 0.05, (240, 200, 60), n=12)
    cam.line(c, (-1.56, 0.27, Z), (-0.9, 0.27, Z), 0.02, (90, 170, 80))
    for x, h, col in ((-1.4, 0.26, (60, 90, 200)), (-1.26, 0.24, (210, 60, 90)), (-1.13, 0.15, (240, 140, 40))):
        stick_figure(cam, c, Z, x, 0.29, h, col)
    if "drawing" in d:
        stick_figure(cam, c, Z, -0.99, 0.29, 0.36, (20, 20, 24), arms=0.1)
    cam.back_rect(c, Z, -1.5, -1.0, -0.36, 0.06, (236, 232, 218))
    cam.back_poly(c, Z, [(-1.4, -0.3), (-1.1, -0.3), (-1.1, -0.12), (-1.25, 0.0), (-1.4, -0.12)], (200, 90, 70))
    # clock
    cx, cy = 1.2, 0.62
    cam.back_ellipse(c, Z, cx, cy, 0.22, 0.22, (90, 70, 60))
    cam.back_ellipse(c, Z, cx, cy, 0.18, 0.18, (240, 176, 170) if "clock" in d else (236, 232, 214))
    ha, ma = (math.pi / 2 + math.radians(-30 * 7), math.pi / 2) if "clock" not in d else (math.pi / 2 - math.radians(30 * 3), -math.pi / 2)
    cam.line(c, (cx, cy, Z), (cx + 0.09 * math.cos(ha), cy + 0.09 * math.sin(ha), Z), 0.022, INK)
    cam.line(c, (cx, cy, Z), (cx + 0.14 * math.cos(ma), cy + 0.14 * math.sin(ma), Z), 0.016, INK)
    # family photo
    cam.back_rect(c, Z, 0.92, 1.48, -0.42, 0.2, (130, 98, 70))
    cam.back_rect(c, Z, 0.97, 1.43, -0.37, 0.15, (214, 204, 184))
    for k, x in enumerate((1.06, 1.2, 1.34)):
        cam.back_rect(c, Z, x - 0.05, x + 0.05, -0.37, -0.12, [(80, 100, 150), (170, 70, 80), (90, 140, 90)][k])
        cam.back_ellipse(c, Z, x, -0.04, 0.045, 0.05, (230, 200, 170), n=14)
    if "photo" in d:                    # the middle face is scribbled out
        for k in range(7):
            cam.line(c, (1.15, -0.09 + k * 0.015, Z), (1.25, -0.08 + k * 0.015 + (0.02 if k % 2 else -0.02), Z), 0.012, (14, 12, 14))


def l67_bed(c, d):
    cam = C67
    x0, x1, z0, z1, top = -1.9, -0.95, 1.5, 3.3, -0.78
    cam.back_poly(c, z1, [(x0, YF7), (x1, YF7), (x1, -0.35), (-1.42, -0.22), (x0, -0.35)], (118, 82, 60))
    cam.poly(c, [(x0, top, z0), (x1, top, z0), (x1, top, z1), (x0, top, z1)], (138, 66, 92))
    cam.poly(c, [(-1.82, top + 0.04, 2.92), (-1.03, top + 0.04, 2.92), (-1.03, top + 0.04, 3.24), (-1.82, top + 0.04, 3.24)], (226, 226, 232))
    cam.line(c, (x0, top, 2.75), (x1, top, 2.75), 0.03, (110, 50, 74))
    cam.poly(c, [(x1, top, z0), (x1, top, z1), (x1, -1.02, z1), (x1, -1.02, z0)], (118, 56, 80))
    cam.poly(c, [(x1, -1.02, z0), (x1, -1.02, z1), (x1, YF7 + 0.12, z1), (x1, YF7 + 0.12, z0)], (100, 70, 52))
    cam.poly(c, [(x1, YF7 + 0.12, z0), (x1, YF7 + 0.12, z1), (x1, YF7, z1), (x1, YF7, z0)], (6, 6, 10), flat=True)


def l67_footboard(c, d):
    C67.back_poly(c, 1.5, [(-1.9, YF7), (-0.95, YF7), (-0.95, -0.6), (-1.42, -0.5), (-1.9, -0.6)], (126, 88, 64))
    C67.back_rect(c, 1.5, -1.8, -1.05, -1.0, -0.66, (112, 78, 58))


def l67_wardrobe(c, d):
    cam = C67
    X0, X1, z0, z1, top = 1.2, 1.9, 2.2, 3.5, 1.0
    cam.poly(c, [(X0, YF7, z0), (X0, YF7, z1), (X0, top, z1), (X0, top, z0)], (122, 88, 66))
    cam.wall_rect(c, X0, 2.83, 2.92, YF7 + 0.08, top - 0.08, (6, 6, 10))               # the door is ajar
    for za, zb in ((z0 + 0.06, 2.8), (2.95, z1 - 0.06)):
        cam.wall_rect(c, X0, za + 0.06, zb - 0.06, -0.9, -0.2, (110, 78, 58))
        cam.wall_rect(c, X0, za + 0.06, zb - 0.06, 0.0, 0.85, (70, 104, 136) if "wardrobe" in d else (110, 78, 58))
    for kz in (2.74, 3.0):
        x, y = cam.p(X0, -0.1, kz)
        c.circle(x, y, 0.025 * cam.s(kz), cam.col((200, 170, 90), kz))
    cam.poly(c, [(X0, YF7, z0), (X1, YF7, z0), (X1, top, z0), (X0, top, z0)], (100, 72, 56))
    cam.poly(c, [(X0 - 0.04, top, z0 - 0.04), (X1, top, z0 - 0.04), (X1, top + 0.08, z0 - 0.04), (X0 - 0.04, top + 0.08, z0 - 0.04)],
             (86, 60, 46))


def l67_teddy(c, d):
    col, dark = (176, 130, 84), (140, 100, 64)
    c.ellipse(-12, -4, 9, 6, col)
    c.ellipse(12, -4, 9, 6, col)
    c.ellipse(0, -20, 16, 18, col)
    c.ellipse(0, -16, 9, 10, (210, 180, 140))
    c.ellipse(-17, -26, 6, 11, col)
    if "teddy" in d:                    # right arm torn off, stuffing showing
        for dx, dy in ((15, -30), (19, -27), (17, -24)):
            c.circle(dx, dy, 3.5, (240, 238, 230))
    else:
        c.ellipse(17, -26, 6, 11, col)
    c.circle(-11, -52, 6, col)
    c.circle(11, -52, 6, col)
    c.circle(0, -44, 13, col)
    c.ellipse(0, -40, 6, 4.5, (210, 180, 140))
    c.circle(0, -42, 2.2, INK)
    c.circle(-5, -47, 2.2, INK)
    c.line(3, -50, 8, -45, 1.5, INK)
    c.line(8, -50, 3, -45, 1.5, INK)
    c.line(-4, -36, 4, -36, 1.2, (110, 60, 50))


def l67_blocks(c, d):
    blocks = [(-14, (210, 70, 70), "o"), (2, (80, 130, 210), "t")]
    if "blocks" not in d:
        blocks.append((-6, (240, 190, 60), "s"))
    for k, (x, col, sym) in enumerate(blocks):
        y = -k * 12
        c.rect(x - 6, y - 12, x + 6, y, col)
        c.polygon([(x - 6, y - 12), (x - 3, y - 15), (x + 9, y - 15), (x + 6, y - 12)], lit(col, 1.2))
        c.polygon([(x + 6, y - 12), (x + 9, y - 15), (x + 9, y - 3), (x + 6, y)], lit(col, 0.8))
        if sym == "o":
            c.circle(x, y - 6, 3, (250, 246, 230))
        elif sym == "t":
            c.polygon([(x - 3.5, y - 3), (x + 3.5, y - 3), (x, y - 9)], (250, 246, 230))
        else:
            c.star(x, y - 6, 4, 1.8, (250, 246, 230))


def l67_slippers(c, d):
    for x in ((-8,) if "slippers" in d else (-8, 8)):
        c.ellipse(x, -3, 6, 4, (240, 160, 190))
        c.ellipse(x, -6, 5, 2.5, (255, 200, 220))
        c.circle(x - 2, -8, 1.5, INK)
        c.circle(x + 2, -8, 1.5, INK)


def l67_music_box(c, d):
    c.rect(-10, -9, 10, 0, (170, 110, 160))
    c.rect(-10, -11, 10, -9, (200, 150, 190))
    c.line(-10, -4, 10, -4, 1.2, (240, 210, 120))


def l67_rug(c):
    cam = C67
    cam.floor_ellipse(c, YF7, 0.15, 2.4, 1.05, 0.85, (120, 70, 90))
    cam.floor_ellipse(c, YF7, 0.15, 2.4, 0.85, 0.68, (150, 100, 120))
    cam.floor_ellipse(c, YF7, 0.15, 2.4, 0.5, 0.4, (120, 70, 90))
    rnd = random.Random(67)
    for _ in range(9):                  # crayons on the floor
        x, z = rnd.uniform(-0.5, 0.6), rnd.uniform(1.15, 1.6)
        a = rnd.uniform(0, math.pi)
        cam.line(c, (x, YF7, z), (x + 0.07 * math.cos(a), YF7, z + 0.07 * math.sin(a)), 0.012,
                 rnd.choice(((220, 60, 60), (60, 120, 220), (240, 200, 60), (80, 170, 90))))


def l67_bg(c, d):
    cam = C67
    cam.depth_strips(c, lambda a, b: [(XL7, YC7, a), (XR7, YC7, a), (XR7, YC7, b), (XL7, YC7, b)], ZN7, ZB7, (64, 66, 96))
    cam.depth_strips(c, lambda a, b: [(XL7, YC7, a), (XL7, YC7, b), (XL7, YF7, b), (XL7, YF7, a)], ZN7, ZB7, (92, 102, 142))
    cam.depth_strips(c, lambda a, b: [(XR7, YC7, a), (XR7, YC7, b), (XR7, YF7, b), (XR7, YF7, a)], ZN7, ZB7, (86, 96, 136))
    cam.depth_strips(c, lambda a, b: [(XL7, YF7, a), (XR7, YF7, a), (XR7, YF7, b), (XL7, YF7, b)], ZN7, ZB7, (104, 80, 64))
    cam.back_rect(c, ZB7, XL7, XR7, YF7, YC7, (98, 108, 150), flat=True)
    for X in (XL7, XR7):                                                    # star wallpaper + skirting
        z = 1.5
        while z < ZB7:
            for y in (-0.7, -0.15, 0.4, 0.95):
                cam.wall_ellipse(c, X, z + (0.12 if y in (-0.15, 0.95) else 0), y, 0.035, 0.035, (130, 140, 180), n=8, flat=True)
            z += 0.32
        cam.depth_strips(c, lambda a, b, X=X: [(X, YF7 + 0.1, a), (X, YF7 + 0.1, b), (X, YF7, b), (X, YF7, a)], ZN7, ZB7, (60, 60, 80), n=8)
    for x in (-1.5, -0.6, 0.3, 1.2):
        for y in (-0.8, 1.2):
            cam.back_ellipse(c, ZB7, x, y, 0.035, 0.035, (130, 140, 180), n=8, flat=True)
    cam.back_rect(c, ZB7, XL7, XR7, YF7, YF7 + 0.1, (60, 60, 80), flat=True)
    x = XL7
    while x < XR7:
        cam.line(c, (x, YF7, ZN7), (x, YF7, ZB7), 0.01, (84, 64, 52))
        x += 0.24
    # moonlight falling through the window onto the floor
    cam.poly(c, [(-0.55, -0.11, ZB7), (0.55, -0.11, ZB7), (0.95, YF7, 2.7), (-0.2, YF7, 2.7)], (180, 200, 255, 0.07), glow=True)
    cam.floor_poly(c, YF7, [(-0.2, 2.7), (0.95, 2.7), (0.75, 3.5), (-0.3, 3.5)], (190, 210, 255, 0.1), glow=True)
    l67_back_wall(c, d)
    l67_rug(c)
    l67_wardrobe(c, d)
    l67_bed(c, d)
    l67_music_box(XF_MUSIC.canvas(c), d)
    l67_teddy(XF_TEDDY.canvas(c), d)
    l67_footboard(c, d)
    l67_blocks(XF_BLOCKS.canvas(c), d)
    l67_slippers(XF_SLIPPERS.canvas(c), d)


def l67_curtain(side):
    def draw(c, m):
        cam, Z = C67, ZB7 - 0.03
        xo, xi = (-0.86, -0.5) if side < 0 else (0.86, 0.5)
        pts = [(xo, 1.1), (xi, 1.1)] + [(xi + side * 0.05 * math.sin(k), 1.1 - k * 0.18) for k in range(1, 8)] + [(xo, -0.2)]
        cam.back_poly(c, Z, pts, (150, 120, 170))
        for k in range(3):
            xx = xo + (xi - xo) * (0.25 + k * 0.25)
            cam.line(c, (xx, 1.08, Z), (xx, -0.18, Z), 0.012, (120, 92, 140))
    return draw


def l67_horse(c, m):
    c.ellipse(0, -6, 38, 6, (150, 90, 60), ymin=-6)
    c.line(-30, -10, -18, -30, 4, (190, 150, 110))
    c.line(30, -10, 18, -30, 4, (190, 150, 110))
    c.ellipse(0, -36, 24, 11, (236, 230, 220))
    c.polygon([(16, -42), (26, -66), (36, -62), (28, -38)], (236, 230, 220))
    c.ellipse(35, -62, 9, 6, (236, 230, 220))
    c.polygon([(18, -46), (24, -66), (21, -44)], (180, 60, 60))
    c.polygon([(-22, -38), (-34, -24), (-24, -32)], (180, 60, 60))
    c.circle(35, -64, 1.6, INK)
    c.ellipse(-2, -46, 9, 4, (90, 120, 200))


def l67_eyes(c, m, x, y, s):
    for dx in (-5 * s, 5 * s):
        glow_circles(c, x + dx, y, 6 * s, (255, 230, 120), 0.12, 3)
        c.ellipse(x + dx, y, 2.4 * s, 1.6 * s, (255, 236, 150, 1.0))


def l67_ballerina(c, m):
    c.line(0, -12, 0, -18, 1.5, (240, 200, 210))
    c.polygon([(-6, -19), (6, -19), (0, -25)], (250, 200, 220))
    c.line(0, -25, 0, -31, 2, (250, 220, 220))
    c.circle(0, -33, 2.4, (250, 220, 200))
    c.line(-5, -30, 5, -30, 1.2, (250, 220, 200))


def l67_shadow(c, m):
    cam, X = C67, XL7
    pts = [(2.3, -0.5), (2.45, -0.5), (2.48, 0.6), (2.75, 0.2), (2.78, 0.26), (2.5, 0.8), (2.52, 1.0), (2.42, 1.12), (2.32, 1.0),
           (2.34, 0.8), (2.06, 0.25), (2.1, 0.2), (2.3, 0.6)]
    cam.wall_poly(c, X, [(z, y) for z, y in pts], (10, 10, 22, 0.55), glow=True)


_bx, _by = C67.p(-0.95, YF7 + 0.06, 2.45)
_wx, _wy = C67.p(1.2, 0.05, 2.875)
L67_ELEMENTS = [
    E("curtainL", l67_curtain(-1), pivot=C67.p(-0.68, 1.1, ZB7), anim=dict(swingAngle=1.5, swingSpeed=0.2)),
    E("curtainR", l67_curtain(1), pivot=C67.p(0.68, 1.1, ZB7), anim=dict(swingAngle=1.5, swingSpeed=0.23, phase=0.4)),
    E("shadow", l67_shadow, anim=dict(twinkle=0.95, twinkleSpeed=0.07, phase=0.6)),
    E("eyes_bed", lambda c, m: l67_eyes(c, m, _bx, _by, 1.0), anim=dict(blinkInterval=5.0, blinkDuration=1.6)),
    E("eyes_wardrobe", lambda c, m: l67_eyes(c, m, _wx, _wy, 0.8), anim=dict(blinkInterval=7.0, blinkDuration=2.0, phase=0.45)),
    E("horse", XF_HORSE.draw(l67_horse), pivot=XF_HORSE.p(0, -2), anim=dict(swingAngle=7, swingSpeed=0.35)),
    E("ballerina", XF_MUSIC.draw(l67_ballerina), pivot=XF_MUSIC.p(0, -20), anim=dict(spinSpeed=0.4, spinShade=0.3)),
]

L67_DIFFS = [
    ("teddy", *XF_TEDDY.p(17, -27), 0),
    ("drawing", *C67.p(-0.99, 0.47, ZB7), 0),
    ("clock", *C67.p(1.2, 0.62, ZB7), 0),
    ("photo", *C67.p(1.2, -0.04, ZB7), 0),
    ("hand", *C67.p(-0.2, 0.25, ZB7), 0),
    ("blocks", *XF_BLOCKS.p(-6, -30), 0),
    ("slippers", *XF_SLIPPERS.p(8, -5), 0),
    ("wardrobe", *C67.p(1.2, 0.42, 2.85), 0),
]


# =================================================================== Level 68 a dinner for nobody
C68 = Cam(vpx=450, vpy=250, f=330, dark=(16, 8, 6), fog=(1.5, 10.0), fog_k=0.6)
XL8, XR8, YF8, YC8, ZB8, ZN8 = -2.4, 2.4, -1.5, 1.75, 8.0, 0.9
TOP8 = -0.72
CHAIRS8 = [3.0, 4.2, 5.4, 6.6]
XF_CANDLE_NEAR = C68.at(0, TOP8, 3.9)
XF_CANDLE_FAR = C68.at(0, TOP8, 6.2)
XF_VASE = C68.at(0, TOP8, 5.1)
XF_CAKE = C68.at(0, TOP8, 2.75, 0.55)
XF_GLASS = C68.at(0.64, TOP8, 2.85)
XF_CLOCK8 = C68.at(1.95, YF8, 6.2)
XF_CAT = C68.at(1.25, YF8, 2.1)
XF_STAND = C68.at(-1.95, YF8, 2.0)
XF_TOPPLED = C68.at(-0.55, YF8, 1.75, 0.85)


def l68_portrait(c, X, zc, face, ground=(44, 36, 30)):
    cam = C68
    cam.wall_rect(c, X, zc - 0.48, zc + 0.48, -0.02, 1.2, (160, 120, 56))
    cam.wall_rect(c, X, zc - 0.4, zc + 0.4, 0.06, 1.12, ground)
    cam.wall_ellipse(c, X, zc, 0.12, 0.32, 0.2, (30, 34, 44))
    cam.wall_ellipse(c, X, zc, 0.72, 0.2, 0.24, (58, 40, 30))
    cam.wall_ellipse(c, X, zc, 0.64, 0.15, 0.2, (214, 192, 168))
    if face:
        for dz in (-0.06, 0.06):
            cam.wall_ellipse(c, X, zc + dz, 0.69, 0.028, 0.02, INK, n=10)
        cam.line(c, (X, 0.54, zc - 0.05), (X, 0.55, zc + 0.05), 0.014, (120, 60, 54))


def l68_chair_side(c, X, zc):
    cam = C68
    xo = X * 1.0
    for dz in (-0.2, 0.2):
        cam.line(c, (xo, YF8, zc + dz), (xo, 0.3, zc + dz), 0.05, (70, 40, 28), flat=False)
    cam.wall_poly(c, xo, [(zc - 0.22, -0.2), (zc + 0.22, -0.2), (zc + 0.22, 0.28), (zc, 0.4), (zc - 0.22, 0.28)], (90, 30, 34))
    cam.wall_rect(c, xo, zc - 0.17, zc + 0.17, -0.12, 0.22, (120, 44, 46))


def l68_head_chair(c):
    C68.back_poly(c, 7.6, [(-0.32, YF8), (0.32, YF8), (0.32, 0.5), (0.18, 0.7), (-0.18, 0.7), (-0.32, 0.5)], (76, 44, 30))
    C68.back_rect(c, 7.6, -0.22, 0.22, -0.3, 0.48, (100, 32, 36))


def l68_back_wall(c, d):
    cam, Z = C68, ZB8
    cam.back_rect(c, Z, XL8, XR8, YF8, YC8, (96, 34, 34), flat=True)
    cam.back_rect(c, Z, XL8, XR8, YF8, -0.6, (70, 44, 30), flat=True)
    # fireplace
    cam.back_rect(c, Z, -0.8, 0.8, YF8, -0.38, (120, 110, 100))
    cam.back_rect(c, Z, -0.48, 0.48, YF8, -0.86, (12, 8, 6), flat=True)
    cam.back_rect(c, Z, -0.9, 0.9, -0.38, -0.3, (90, 60, 40))
    # mirror: someone stands behind the empty chairs (A only)
    cam.back_rect(c, Z, -0.84, 0.84, -0.26, 1.52, (170, 130, 60))
    cam.back_rect(c, Z, -0.74, 0.74, -0.18, 1.42, (66, 66, 76), flat=True)
    cam.back_poly(c, Z, [(-0.74, -0.18), (0.74, -0.18), (0.74, 0.1), (-0.74, 0.1)], (92, 80, 76), flat=True)
    cam.back_poly(c, Z, [(-0.74, 1.0), (-0.2, 1.42), (-0.5, 1.42), (-0.74, 1.24)], (90, 90, 100, 0.6), glow=True)
    if "mirror" not in d:
        cam.back_poly(c, Z, [(0.18, -0.18), (0.44, -0.18), (0.38, 0.5), (0.24, 0.5)], (196, 192, 186), flat=True, glow=True)
        cam.back_ellipse(c, Z, 0.31, 0.62, 0.07, 0.09, (210, 206, 198), flat=True, glow=True)
        cam.back_poly(c, Z, [(0.23, 0.68), (0.39, 0.68), (0.42, 0.3), (0.2, 0.3)], (26, 22, 24), flat=True, glow=True)
        cam.back_ellipse(c, Z, 0.31, 0.61, 0.055, 0.075, (210, 206, 198), flat=True, glow=True)


def l68_table(c, d):
    cam = C68
    x0, x1, z0, z1 = -0.8, 0.8, 2.4, 7.2
    for X, z in ((-0.7, 7.1), (0.7, 7.1)):
        cam.line(c, (X, TOP8, z), (X, YF8, z), 0.08, (60, 36, 26), flat=False)
    cam.poly(c, [(x0, TOP8, z0), (x1, TOP8, z0), (x1, TOP8, z1), (x0, TOP8, z1)], (214, 206, 190), flat=True)
    cam.floor_rect(c, TOP8, -0.2, 0.2, z0, z1, (124, 30, 36))
    for X in (x0, x1):
        cam.poly(c, [(X, TOP8, z0), (X, TOP8, z1), (X, -1.0, z1), (X, -1.0, z0)], (190, 182, 166), flat=True)
    cam.poly(c, [(x0, TOP8, z0), (x1, TOP8, z0), (x1, -1.06, z0), (x0, -1.06, z0)], (204, 196, 180))
    for k in range(9):
        X = x0 + k * 0.2
        cam.line(c, (X, TOP8 - 0.02, z0), (X, -1.04, z0), 0.012, (180, 172, 156))
    for zc in CHAIRS8:                                                      # place settings
        for X in (-0.5, 0.5):
            cam.floor_ellipse(c, TOP8, X, zc, 0.15, 0.15, (238, 234, 226), flat=False)
            cam.floor_ellipse(c, TOP8, X, zc, 0.1, 0.1, (222, 216, 206))
            for dx in (-0.2, 0.2):
                cam.line(c, (X + dx, TOP8, zc - 0.1), (X + dx, TOP8, zc + 0.1), 0.012, (180, 180, 186))
    cam.floor_ellipse(c, TOP8, 0, 2.75, 0.17, 0.17, (240, 236, 228), flat=False)
    cam.floor_ellipse(c, TOP8, 0, 2.75, 0.12, 0.12, (222, 216, 206))
    if "glass" in d:
        cam.floor_ellipse(c, TOP8, 0.58, 2.95, 0.18, 0.1, (120, 16, 30))


def l68_glass(c, d, upright=True):
    if upright:
        c.line(0, 0, 0, -10, 1.6, (220, 226, 236))
        c.ellipse(0, 0, 6, 1.6, (220, 226, 236))
        c.polygon([(-7, -10), (7, -10), (6, -24), (-6, -24)], (220, 226, 236, 0.7))
        c.polygon([(-6.6, -12), (6.6, -12), (6.2, -18), (-6.2, -18)], (140, 20, 34))
    else:
        c.polygon([(-16, -2), (8, -6), (8, 6), (-16, 2)], (220, 226, 236, 0.75))
        c.line(8, 0, 20, 0, 1.6, (220, 226, 236))
        c.ellipse(20, 0, 1.6, 6, (220, 226, 236))


def l68_glasses(c, d):
    for zc in CHAIRS8:
        for X in (-0.66, 0.66):
            l68_glass(C68.at(X, TOP8, zc - 0.17).canvas(c), d)


def l68_candelabra(c, d, n):
    c.ellipse(0, -2, 14, 4, (190, 150, 70))
    c.line(0, -2, 0, -44, 4, (190, 150, 70))
    c.line(-22, -40, 22, -40, 3, (190, 150, 70))
    for k, x in enumerate((-22, 0, 22)[:n]):
        c.rect(x - 3, -40 - (14 if x == 0 else 0) - 22, x + 3, -40 - (14 if x == 0 else 0), (236, 228, 200))
    c.line(0, -40, 0, -54, 4, (190, 150, 70))


def l68_vase(c, d):
    c.polygon([(-7, 0), (7, 0), (10, -14), (4, -26), (-4, -26), (-10, -14)], (60, 70, 90))
    if "flowers" in d:
        for ex, ey in ((-16, -20), (-4, -36), (14, -18), (6, -30)):
            c.line(0, -24, (ex) / 2, -36, 1.6, (100, 92, 70))
            c.line(ex / 2, -36, ex, ey, 1.6, (100, 92, 70))
            c.circle(ex, ey, 4, (84, 64, 60))
    else:
        for ex, ey in ((-14, -46), (-4, -54), (8, -50), (15, -40), (-10, -36)):
            c.line(0, -24, ex, ey, 1.6, (60, 110, 60))
            c.circle(ex, ey, 5, (180, 24, 40))
            c.circle(ex - 1.2, ey - 1.2, 2, (220, 60, 70))


def l68_cake(c, d):
    if "cake" in d:                     # gone mouldy, the cherry is gone
        c.polygon([(-20, -4), (16, -2), (14, -20), (-18, -24)], (130, 140, 110))
        c.polygon([(-18, -24), (14, -20), (4, -28), (-22, -30)], (150, 160, 130))
        for x, y in ((-10, -14), (4, -10), (8, -18)):
            c.circle(x, y, 2.5, (90, 110, 80))
    else:
        c.polygon([(-20, -4), (16, -2), (14, -20), (-18, -24)], (250, 220, 200))
        c.polygon([(-20, -12), (15, -10), (15, -13), (-19, -15)], (230, 120, 140))
        c.polygon([(-18, -24), (14, -20), (4, -28), (-22, -30)], (255, 246, 240))
        c.circle(-6, -32, 4.5, (200, 20, 40))
        c.line(-6, -36, -2, -44, 1.2, (80, 120, 60))


def l68_clock(c, d):
    c.rect(-24, -210, 24, 0, (80, 50, 34))
    c.polygon([(-28, -210), (28, -210), (0, -232)], (70, 44, 30))
    c.circle(0, -180, 18, (230, 222, 196))
    c.line(0, -180, 0, -194, 2.5, INK)
    c.line(0, -180, 10, -176, 2.5, INK)
    c.rect(-14, -150, 14, -40, (24, 16, 12))


def l68_cat(c, d):
    col = (22, 20, 24)
    c.ellipse(0, -16, 15, 16, col)
    c.circle(0, -38, 11, col)
    c.polygon([(-10, -44), (-7, -56), (-2, -46)], col)
    c.polygon([(10, -44), (7, -56), (2, -46)], col)
    c.line(12, -4, 26, -14, 4, col)
    c.line(26, -14, 24, -30, 4, col)


def l68_toppled(c, d):
    """A chair knocked over on the rug, as if someone left in a hurry."""
    l66_chair(c, {"chair"})


def l68_stand(c, d):
    c.ellipse(0, -2, 22, 5, (60, 40, 30))
    c.line(0, -2, 0, -150, 6, (70, 46, 32))
    c.ellipse(0, -150, 12, 3, (190, 150, 70))
    c.rect(-4, -176, 4, -150, (236, 228, 200))


def l68_bg(c, d):
    cam = C68
    cam.depth_strips(c, lambda a, b: [(XL8, YC8, a), (XR8, YC8, a), (XR8, YC8, b), (XL8, YC8, b)], ZN8, ZB8, (56, 36, 30))
    cam.depth_strips(c, lambda a, b: [(XL8, YC8, a), (XL8, YC8, b), (XL8, YF8, b), (XL8, YF8, a)], ZN8, ZB8, (110, 40, 40))
    cam.depth_strips(c, lambda a, b: [(XR8, YC8, a), (XR8, YC8, b), (XR8, YF8, b), (XR8, YF8, a)], ZN8, ZB8, (104, 38, 38))
    cam.depth_strips(c, lambda a, b: [(XL8, YF8, a), (XR8, YF8, a), (XR8, YF8, b), (XL8, YF8, b)], ZN8, ZB8, (76, 52, 38))
    for X in (XL8, XR8):
        cam.depth_strips(c, lambda a, b, X=X: [(X, -0.6, a), (X, -0.6, b), (X, YF8, b), (X, YF8, a)], ZN8, ZB8, (70, 44, 30))
        z = 1.2
        while z < ZB8:                                                      # damask diamonds + wainscot panels
            for y in (0.0, 0.6, 1.2):
                cam.wall_poly(c, X, [(z, y - 0.12), (z + 0.1, y), (z, y + 0.12), (z - 0.1, y)], (124, 52, 50), flat=True)
            cam.wall_rect(c, X, z - 0.18, z + 0.18, -1.35, -0.75, (82, 54, 38), flat=True)
            z += 0.5
    x = XL8
    while x < XR8:
        cam.line(c, (x, YF8, ZN8), (x, YF8, ZB8), 0.012, (60, 40, 30))
        x += 0.3
    cam.floor_rect(c, YF8, -1.5, 1.5, 1.4, 7.6, (100, 30, 34))
    cam.floor_rect(c, YF8, -1.35, 1.35, 1.55, 7.45, (124, 70, 46))
    cam.floor_rect(c, YF8, -1.2, 1.2, 1.7, 7.3, (100, 30, 34))
    cam.floor_poly(c, YF8, [(0, 1.75), (0.9, 2.3), (0, 2.85), (-0.9, 2.3)], (150, 96, 56))          # rug medallion
    cam.floor_poly(c, YF8, [(0, 1.95), (0.55, 2.3), (0, 2.65), (-0.55, 2.3)], (100, 30, 34))
    cam.floor_ellipse(c, YF8, 0, 2.3, 0.18, 0.12, (190, 150, 70))
    rnd = random.Random(68)
    for _ in range(14):                                                     # rose petals on the rug
        x, z = rnd.uniform(-1.2, 1.2), rnd.uniform(1.3, 2.4)
        cam.floor_ellipse(c, YF8, x, z, 0.035, 0.02, (170, 20, 40), n=10)
    l68_back_wall(c, d)
    cam.wall_rect(c, XL8, 6.6, 7.4, YF8, 0.6, (60, 40, 28))               # dark doorway on the left
    cam.wall_rect(c, XL8, 6.68, 7.32, YF8, 0.52, (8, 4, 4), flat=True)
    for X in (XL8, XR8):
        for zc in (3.4, 5.6):
            blank_r = X == XR8 and zc == 3.4 and "portrait" in d          # hollow face on a red ground
            blue_l = X == XL8 and zc == 3.4 and "portraitL" in d
            l68_portrait(c, X, zc, not blank_r, (128, 36, 40) if blank_r else (44, 72, 110) if blue_l else (44, 36, 30))
        x, y = cam.p(X, 0.25, 4.5)
        cam.wall_rect(c, X, 4.42, 4.58, 0.12, 0.3, (190, 150, 70))
    l68_clock(XF_CLOCK8.canvas(c), d)
    l68_head_chair(c)
    for zc in sorted(CHAIRS8, reverse=True):
        for X in (-1.15, 1.15):
            if X < 0 and zc == 4.2 and "chair" in d:
                continue
            l68_chair_side(c, X, zc)
    l68_table(c, d)
    l68_candelabra(XF_CANDLE_FAR.canvas(c), d, 3)
    l68_vase(XF_VASE.canvas(c), d)
    l68_candelabra(XF_CANDLE_NEAR.canvas(c), d, 2 if "candle" in d else 3)
    l68_glasses(c, d)
    l68_glass(XF_GLASS.canvas(c), d, upright="glass" not in d)
    l68_cake(XF_CAKE.canvas(c), d)
    if "toppled" not in d:
        l68_toppled(XF_TOPPLED.canvas(c), d)
    l68_stand(XF_STAND.canvas(c), d)
    if "cat" not in d:
        l68_cat(XF_CAT.canvas(c), d)


def l68_chandelier(c, m):
    c.line(0, -300, 0, -40, 3, (120, 100, 60))
    c.ellipse(0, -30, 46, 10, (170, 130, 60))
    c.ellipse(0, -18, 16, 12, (150, 112, 50))
    for x in (-42, -21, 0, 21, 42):
        y = -30 - (6 if x == 0 else 0)
        c.rect(x - 3, y - 16, x + 3, y, (236, 228, 200))
        flame(c, x, y - 17, 0.9)


def _cand_flames(xf, n, prefix, missing=None):
    out = []
    for k, x in enumerate((-22, 0, 22)[:n]):
        y = -40 - (14 if x == 0 else 0) - 22
        px, py = xf.p(x, y - 1)
        out.append(flame_el("%s%d" % (prefix, k), px, py, xf.s, 0.17 * k + len(prefix) * 0.05,
                            show="A" if k == missing else "both"))
    return out


_cx, _cy = C68.p(0, YC8, 4.8)
_cat_eyes = XF_CAT.p(0, -39)
L68_ELEMENTS = [
    E("fire", lambda c, m: [flame(c, x, y, 1.0) for x, y in [C68.p(dx, YF8 + 0.08, ZB8 - 0.05) for dx in (-0.2, 0, 0.2)]],
      anim=dict(stretch=(0.1, 0.25), scaleSpeed=2.2, twinkle=0.2, twinkleSpeed=3.1)),
    E("chandelier", C68.at(0, 1.05, 4.8).draw(l68_chandelier), pivot=(_cx, _cy), anim=dict(swingAngle=2.5, swingSpeed=0.12)),
    E("pendulum", XF_CLOCK8.draw(lambda c, m: (c.line(0, -150, 0, -60, 2, (190, 150, 70)), c.circle(0, -60, 9, (200, 160, 80)))),
      pivot=XF_CLOCK8.p(0, -150), anim=dict(swingAngle=12, swingSpeed=0.5)),
    E("face", lambda c, m: C68.wall_ellipse(c, XL8 + 0.001, 7.0, 0.1, 0.12, 0.15, (200, 196, 190), glow=True),
      anim=dict(twinkle=1.0, twinkleSpeed=0.05, phase=0.7)),
    E("cat_eyes", lambda c, m: l67_eyes(c, m, _cat_eyes[0], _cat_eyes[1], XF_CAT.s * 1.4),
      anim=dict(blinkInterval=4.0, blinkDuration=3.6)),
] + _cand_flames(XF_CANDLE_NEAR, 3, "flameN", missing=2) + _cand_flames(XF_CANDLE_FAR, 3, "flameF") + [
    flame_el("flameS", *XF_STAND.p(0, -177), XF_STAND.s * 1.3, 0.21),
] + [flame_el("sconce%d" % i, *C68.p(X, 0.32, 4.5), C68.s(4.5) / 100 * 0.8, 0.3 + i * 0.1) for i, X in enumerate((XL8, XR8))]

L68_DIFFS = [
    ("mirror", *C68.p(0.31, 0.3, ZB8), 0),
    ("portrait", *C68.p(XR8, 0.64, 3.4), 0),
    ("chair", *C68.p(-1.15, 0.0, 4.2), 0),
    ("glass", *XF_GLASS.p(0, -8), 0),
    ("cake", *XF_CAKE.p(-4, -18), 0),
    ("candle", *XF_CANDLE_NEAR.p(22, -60), 0),
    ("flowers", *XF_VASE.p(0, -38), 0),
    ("portraitL", *C68.p(XL8, 0.6, 3.4), 0),
    ("cat", *XF_CAT.p(4, -28), 0),
    ("toppled", *XF_TOPPLED.p(0, -30), 0),
]

LEVELS = [paper_level(lv, edge_mix=0.75) for lv in [
    ("Level66", "无尽走廊", l66_bg, L66_ELEMENTS, L66_DIFFS, 140, OPTS),
    ("Level67", "童年卧室", l67_bg, L67_ELEMENTS, L67_DIFFS, 140, OPTS),
    ("Level68", "无人晚宴", l68_bg, L68_ELEMENTS, L68_DIFFS, 140, OPTS),
]]
