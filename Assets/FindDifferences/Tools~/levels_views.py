# -*- coding: utf-8 -*-
"""
Paper-craft levels with two more camera angles:
  Level10 纸艺地下   - strict side view, a cross-section through the ground
                        (garden on top, burrows / ant nest / mole tunnel in the soil layers)
  Level11 纸艺游乐园 - 45° isometric view of a floating paper amusement park
                        (every building is a folded paper box: lit top, mid left face, dark right face)
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts

OPTS = {"post": paper_post}
INK = (70, 55, 65)
PROP = (2, 4, 7, 0.42)
LAYER = (1, 3, 11, 0.36)


def drift_across(x_left, x_right, speed):
    s_min = -(x_right + 10)
    length = W + 10 - x_left - s_min
    return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min, phase=(-s_min / length) % 1.0)


def paper_cloud(x, y, k, col=(252, 252, 248)):
    def d(c, m):
        piece(c, [Circ(x - 26 * k, y + 8 * k, 18 * k), Circ(x, y, 25 * k), Circ(x + 27 * k, y + 8 * k, 18 * k),
                  RRect(x - 42 * k, y + 4 * k, x + 44 * k, y + 24 * k, 9 * k)], col, shadow=PROP)
    return d


# =================================================================== Level 10 (side cross-section)
GROUND = 212
TUNNEL_DARK, TUNNEL = (72, 46, 40), (108, 72, 58)


def soil_line(top, waves, x):
    return top + sum(a * math.sin(x * f + p) for a, f, p in waves)


def soil_layer(top, waves):
    pts = [(x, soil_line(top, waves, x)) for x in range(-40, 950, 10)]
    return Poly(pts + [(950, 660), (-40, 660)])


S2 = (330, [(10, 0.012, 0.5), (5, 0.04, 1.3)])
S3 = (455, [(12, 0.01, 2.2), (6, 0.03, 0.4)])


def carve(c, shapes):
    """Tunnel cut into the soil: dark rim on top reads as the cut edge's shadow."""
    flat(c, shapes, TUNNEL_DARK)
    for s in shapes:
        s.draw(c, TUNNEL, -3, 0, 2)


ANT_E1 = ((268, 214), (228, 300))
NEST = [Thick(*ANT_E1[0], *ANT_E1[1], 12), Thick(228, 300, 206, 372, 12), Ell(205, 385, 36, 19),
        Thick(226, 392, 300, 430, 11), Ell(312, 438, 40, 21), Thick(190, 400, 176, 470, 11), Ell(170, 482, 32, 17)]
BURROW = [Thick(600, 214, 640, 282, 36), Thick(640, 282, 690, 322, 36), Ell(735, 330, 92, 44)]
MOLE_TUNNEL = [Thick(500, 522, 600, 512, 30), Thick(600, 512, 700, 528, 30), Thick(700, 528, 830, 506, 30)]
CARROTS = [430, 465, 500]


def l10_background(c, d):
    """纸艺地下 - static part"""
    c.rect(0, 0, W, GROUND + 20, (186, 222, 240))
    # soil strata (each layer's halo falls on the one above)
    piece(c, soil_layer(GROUND + 6, [(2, 0.02, 0)]), (176, 126, 88), shadow=None)
    piece(c, soil_layer(*S2), (150, 102, 74), shadow=LAYER)
    piece(c, soil_layer(*S3), (122, 82, 64), shadow=LAYER)
    rnd = random.Random(4)
    for _ in range(40):
        x, y = rnd.randint(0, W), rnd.randint(GROUND + 20, H)
        r = rnd.choice((3, 4, 6, 8))
        piece(c, Ell(x, y, r * 1.3, r), (150 + rnd.randint(-15, 15), 140, 135), shadow=(1, 2, 3, 0.3))
    # tree roots
    roots = [Thick(90, 214, 40, 300, 9), Thick(40, 300, 20, 360, 6), Thick(90, 214, 70, 330, 9),
             Thick(70, 330, 95, 400, 6), Thick(90, 214, 140, 290, 9), Thick(140, 290, 150, 350, 6), Thick(140, 290, 180, 320, 5)]
    piece(c, roots, (128, 88, 62), border=2, border_col=(196, 160, 120), shadow=PROP)
    # tunnels
    carve(c, NEST)
    carve(c, BURROW)
    carve(c, MOLE_TUNNEL)
    # ant nest contents: eggs, queen, seeds
    for x, y in ((192, 388), (203, 384), (214, 389), (224, 385)):
        piece(c, Ell(x, y, 5, 7), (252, 248, 236), shadow=(1, 2, 3, 0.3))
    piece(c, [Ell(318, 444, 14, 8), Circ(300, 441, 6), Ell(331, 446, 9, 6)], (60, 40, 40), shadow=(1, 2, 3, 0.3))
    for x, y in ((160, 488), (172, 485), (182, 489)):
        piece(c, Ell(x, y, 5, 4), (230, 190, 110), shadow=(1, 2, 3, 0.3))
    # rabbit chamber: straw bed and two sleeping bunnies
    for k in range(9):
        flat(c, Thick(670 + k * 15, 368, 682 + k * 15, 352, 3), (240, 205, 110))
    for x in (712, 765):
        piece(c, [Ell(x, 348, 24, 15), Circ(x + 18, 342, 10), Ell(x + 22, 330, 13, 4)], (250, 248, 242), shadow=PROP)
        flat(c, Thick(x + 15, 342, x + 21, 342, 1.4), INK)
    # carrots growing into the soil (one missing in B)
    for x in CARROTS:
        if x == 500 and "carrot" in d:
            continue
        piece(c, Poly([(x - 10, GROUND + 4), (x + 10, GROUND + 4), (x + 1, GROUND + 64)]), (245, 140, 50), shadow=PROP)
        for k in range(3):
            flat(c, Thick(x - 7 + k * 2, GROUND + 18 + k * 13, x + 2 + k, GROUND + 20 + k * 13, 1.4), (210, 105, 40))
    # fossil (missing in B)
    if "fossil" not in d:
        bone = (240, 230, 205)
        piece(c, [Thick(80, 560, 170, 556, 4), Poly([(170, 545), (200, 556), (170, 568)])]
              + [Thick(95 + k * 14, 546, 97 + k * 14, 570, 3) for k in range(5)]
              + [Poly([(80, 560), (62, 546), (66, 560), (62, 574)])], bone, shadow=(1, 2, 4, 0.35))
        flat(c, Circ(182, 554, 3), (122, 82, 64))
    # treasure chest (open with coins in A, closed in B)
    cx, cy = 700, 565
    piece(c, RRect(cx - 34, cy - 18, cx + 34, cy + 18, 3), (150, 92, 55), border=2, border_col=(230, 190, 90), shadow=PROP)
    flat(c, [RRect(cx - 34, cy - 4, cx + 34, cy + 2, 1), RRect(cx - 4, cy - 18, cx + 4, cy + 18, 1)], (230, 190, 90))
    if "chest" in d:
        piece(c, RRect(cx - 36, cy - 32, cx + 36, cy - 17, 6), (165, 102, 62), border=2, border_col=(230, 190, 90), shadow=PROP)
    else:
        piece(c, Poly([(cx - 34, cy - 18), (cx + 34, cy - 18), (cx + 40, cy - 46), (cx - 28, cy - 50)]), (165, 102, 62),
              border=2, border_col=(230, 190, 90), shadow=PROP)
        for k, (x, y) in enumerate(((cx - 20, cy - 20), (cx - 5, cy - 23), (cx + 10, cy - 21), (cx + 22, cy - 19), (cx + 2, cy - 30))):
            piece(c, Circ(x, y, 7), (250, 210, 70), shadow=(1, 2, 3, 0.3))
    # above ground: grass, tree, ant hill, fence
    pts = [(x, GROUND - 4 + 3 * math.sin(x * 0.07)) for x in range(-40, 950, 10)]
    piece(c, Poly(pts + [(950, GROUND + 16), (-40, GROUND + 16)]), (118, 190, 98), shadow=LAYER)
    for x in range(5, 900, 22):
        flat(c, Poly([(x - 4, GROUND - 2), (x - 1, GROUND - 13), (x + 2, GROUND - 2)]), (100, 170, 84))
    piece(c, [Thick(90, GROUND + 4, 90, 110, 22), Thick(90, 150, 120, 120, 8)], (138, 94, 66), border=2, shadow=PROP)
    piece(c, [Circ(90, 80, 55), Circ(45, 105, 35), Circ(135, 100, 38), Circ(110, 55, 35)], (88, 165, 92), shadow=PROP)
    piece(c, [Circ(75, 70, 24), Circ(120, 92, 16)], (110, 185, 105), shadow=(1, 2, 4, 0.25))
    piece(c, Poly([(238, GROUND + 2), (252, GROUND - 14), (268, GROUND - 20), (284, GROUND - 14), (298, GROUND + 2)]),
          (180, 130, 90), shadow=PROP)
    flat(c, Ell(268, GROUND - 3, 6, 4), TUNNEL_DARK)
    for x in range(770, 900, 26):
        piece(c, Poly([(x, GROUND + 2), (x, GROUND - 46), (x + 8, GROUND - 54), (x + 16, GROUND - 46), (x + 16, GROUND + 2)]),
              (250, 245, 232), shadow=PROP)
    flat(c, [RRect(760, GROUND - 38, 900, GROUND - 32, 1), RRect(760, GROUND - 18, 900, GROUND - 12, 1)], (232, 222, 205))
    # carrot tops
    for x in CARROTS:
        if x == 500 and "carrot" in d:
            continue
        piece(c, [Ell(x - 6, GROUND - 14, 4, 12), Ell(x + 6, GROUND - 14, 4, 12), Ell(x, GROUND - 18, 4, 14)], (90, 175, 80),
              shadow=PROP)


def l10_sunflower(x, h, petal):
    def d(c, m):
        col = (250, 150, 50) if (m and petal) else (255, 210, 60)
        top = GROUND - h
        piece(c, [Thick(x, GROUND + 2, x, top, 5), Ell(x - 12, top + h * 0.5, 12, 5), Ell(x + 12, top + h * 0.35, 12, 5)],
              (90, 165, 80), shadow=PROP)
        piece(c, Poly(star_pts(x, top, 26, 14, points=12)), col, border=2, shadow=PROP)
        flat(c, Circ(x, top, 12), (130, 85, 50))
        flat(c, [Circ(x - 4, top - 3, 2), Circ(x + 4, top + 2, 2), Circ(x, top + 5, 2)], (100, 62, 40))
    return d


def l10_ant(x, y, dx, dy):
    def d(c, m):
        ux, uy = (-dx, -dy) if m else (dx, dy)
        ant = (190, 62, 45)
        sx, sy = -uy, ux
        for k in (0.5, 1.2, 1.9):
            px, py = x - ux * k * 6, y - uy * k * 6
            flat(c, Thick(px - sx * 6, py - sy * 6, px + sx * 6, py + sy * 6, 1.1), (60, 25, 25))
        piece(c, [Circ(x - ux * k * 6, y - uy * k * 6, r) for k, r in ((0, 4), (1, 3), (2, 4.6))], ant,
              shadow=(1, 2, 2, 0.35))
    return d


def l10_rabbit(c, m):
    x, y = 628, 262
    piece(c, [Ell(x, y + 6, 13, 16), Circ(x - 4, y - 12, 10), Ell(x - 9, y - 32, 4, 12), Ell(x + 1, y - 33, 4, 12)],
          (235, 228, 220), shadow=PROP)
    flat(c, [Ell(x - 9, y - 32, 1.8, 8), Ell(x + 1, y - 33, 1.8, 8)], (245, 170, 180))
    flat(c, [Circ(x - 8, y - 13, 1.8), Circ(x - 13, y - 9, 1.4)], INK)


def l10_zzz(x, y, s):
    def d(c, m):
        piece(c, Poly([(x - s, y - s), (x + s, y - s), (x - s * 0.4, y + s * 0.6), (x + s, y + s * 0.6), (x + s, y + s),
                       (x - s, y + s), (x + s * 0.4, y - s * 0.6), (x - s, y - s * 0.6)]), (252, 250, 240), shadow=(1, 2, 3, 0.3))
    return d


def l10_worm(c, m):
    pts = [(300 + k * 7, 282 + 4 * math.sin(k * 1.1)) for k in range(9)]
    piece(c, [Circ(px, py, 5.5) for px, py in pts], (240, 140, 150), shadow=(1, 2, 3, 0.3))
    flat(c, [Thick(pts[2][0], pts[2][1] - 5, pts[2][0], pts[2][1] + 5, 2.5)], (220, 110, 125))
    flat(c, Circ(pts[-1][0] + 2, pts[-1][1] - 1.5, 1.3), INK)


def l10_mole(c, m):
    x, y = 518, 516
    piece(c, [Ell(x + 10, y, 22, 14), Ell(x - 10, y + 1, 10, 7)], (75, 60, 70), shadow=PROP)
    flat(c, [Circ(x - 20, y + 1, 4)], (245, 160, 170))
    for k in (-1, 1):
        piece(c, Ell(x - 4, y + k * 10, 7, 4), (245, 175, 175), shadow=(1, 2, 3, 0.3))
    flat(c, Circ(x - 9, y - 4, 1.4), (20, 15, 20))


def l10_clod(x, y, r):
    def d(c, m):
        piece(c, Circ(x, y, r), (150, 102, 74), shadow=(1, 2, 3, 0.3))
    return d


def l10_bee(c, m):
    x, y = 380, 110
    piece(c, [Ell(x - 3, y - 7, 6, 4), Ell(x + 3, y - 7, 6, 4)], (235, 245, 255), shadow=(2, 4, 4, 0.25))
    piece(c, Ell(x, y, 8, 6), (255, 210, 60), shadow=(2, 4, 4, 0.3))
    flat(c, [Thick(x - 2, y - 5, x - 2, y + 5, 2), Thick(x + 3, y - 5, x + 3, y + 5, 2)], INK)


def l10_sun(c, m):
    piece(c, Poly(star_pts(830, 60, 46, 34, points=12)), (255, 190, 80), shadow=PROP)
    piece(c, Circ(830, 60, 28), (255, 222, 95), border=2.5, shadow=PROP)


_e1x, _e1y = ANT_E1[1][0] - ANT_E1[0][0], ANT_E1[1][1] - ANT_E1[0][1]
_e1len = math.hypot(_e1x, _e1y)
E1_DIR = (_e1x / _e1len, _e1y / _e1len)
E1_MID = ((ANT_E1[0][0] + ANT_E1[1][0]) / 2, (ANT_E1[0][1] + ANT_E1[1][1]) / 2)
E3 = ((228, 394), (298, 428))
_e3x, _e3y = E3[1][0] - E3[0][0], E3[1][1] - E3[0][1]
_e3len = math.hypot(_e3x, _e3y)
RABBIT_DIR = (-40 / 77.4, 66 / 77.4)       # up the entrance tunnel (Unity y-up)

L10_ELEMENTS = [
    E("cloud1", paper_cloud(250, 55, 1.0), anim=drift_across(200, 300, 10)),
    E("cloud2", paper_cloud(600, 90, 0.75), anim=drift_across(565, 640, 7)),
    E("sun", l10_sun, pivot=(830, 60), anim=dict(rotateSpeed=-10)),
    E("sunflower", l10_sunflower(360, 118, True), pivot=(360, GROUND), variant=True, anim=dict(swingAngle=4, swingSpeed=0.25)),
    E("sunflower2", l10_sunflower(398, 92, False), pivot=(398, GROUND), anim=dict(swingAngle=5, swingSpeed=0.3, phase=0.4)),
    E("bee", l10_bee, pivot=(380, 110), anim=dict(orbitRadius=(40, 22), orbitSpeed=0.25, bobAmplitude=(0, 5), bobSpeed=1.2)),
] + [
    # ants walk down the entrance tunnel in A and up it in B
    E("ant_e1_%d" % i, l10_ant(E1_MID[0], E1_MID[1], *E1_DIR), pivot=E1_MID, variant=True,
      anim=dict(driftVelocity=(E1_DIR[0] * 12, -E1_DIR[1] * 12), driftLength=_e1len, driftStart=-_e1len / 2,
                driftFade=True, phase=i / 3),
      animB=dict(driftVelocity=(-E1_DIR[0] * 12, E1_DIR[1] * 12), driftLength=_e1len, driftStart=-_e1len / 2,
                 driftFade=True, phase=i / 3))
    for i in range(3)
] + [
    E("ant_e3_%d" % i, l10_ant(E3[0][0], E3[0][1], _e3x / _e3len, _e3y / _e3len), pivot=E3[0],
      anim=dict(driftVelocity=(_e3x / _e3len * 10, -_e3y / _e3len * 10), driftLength=_e3len, driftFade=True, phase=i / 2))
    for i in range(2)
] + [
    E("rabbit", l10_rabbit, pivot=(628, 262),
      anim=dict(bobAmplitude=(RABBIT_DIR[0] * 40, RABBIT_DIR[1] * 40), bobSpeed=0.2, bounce=True), animB={}),
] + [
    E("zzz%d" % i, l10_zzz(752, 310, 5 + i), show="A",
      anim=dict(driftVelocity=(6, 14), driftLength=45, driftFade=True, driftGrow=0.6, phase=i / 3))
    for i in range(3)
] + [
    E("worm", l10_worm, pivot=(328, 282), anim=dict(stretch=(0.15, -0.1), scaleSpeed=0.9, swingAngle=5, swingSpeed=0.7)),
    E("mole", l10_mole, pivot=(522, 518), anim=dict(swingAngle=10, swingSpeed=1.4, bobAmplitude=(-4, 0), bobSpeed=1.4)),
] + [
    E("clod%d" % i, l10_clod(498, 518, r), pivot=(498, 518),
      anim=dict(bobAmplitude=(-6 - 4 * i, 14 + 6 * i), bobSpeed=1.4, bounce=True, phase=i * 0.3))
    for i, r in enumerate((3.5, 2.5, 3))
]

L10_DIFFS = [
    ("rabbit", 618, 245, 40),
    ("ants", int(E1_MID[0]), int(E1_MID[1]), 46),
    ("carrot", 500, GROUND + 20, 34),
    ("fossil", 130, 558, 60),
    ("chest", 700, 545, 42),
    ("sunflower", 360, GROUND - 118, 32),
    ("zzz", 765, 290, 30),
]


# =================================================================== Level 11 (isometric)
T = 36.0
OX, OY = 450.0, 140.0
THICK = 32
ISO_SH = (3, 6, 7, 0.4)


def P(X, Y, Z=0.0):
    return (OX + (X - Y) * T, OY + (X + Y) * T / 2 - Z * T)


def iso_quad(X0, Y0, X1, Y1, Z=0.0):
    return Poly([P(X0, Y0, Z), P(X1, Y0, Z), P(X1, Y1, Z), P(X0, Y1, Z)])


def iso_box(c, X, Y, Z, dx, dy, dz, col, border=2.0, shadow=ISO_SH):
    top = iso_quad(X, Y, X + dx, Y + dy, Z + dz)
    left = Poly([P(X, Y + dy, Z + dz), P(X + dx, Y + dy, Z + dz), P(X + dx, Y + dy, Z), P(X, Y + dy, Z)])
    right = Poly([P(X + dx, Y, Z + dz), P(X + dx, Y + dy, Z + dz), P(X + dx, Y + dy, Z), P(X + dx, Y, Z)])
    piece(c, [top, left, right], col, border=border, shadow=shadow)
    flat(c, top, lit(col, 1.12))
    flat(c, right, lit(col, 0.76))
    return top, left, right


def iso_cyl(c, X, Y, Z0, Z1, r, col, border=2.0, shadow=ISO_SH):
    ex = r * T * math.sqrt(2)
    ey = ex / 2
    cx, cy0 = P(X, Y, Z0)
    cy1 = P(X, Y, Z1)[1]
    piece(c, [Ell(cx, cy0, ex, ey), RRect(cx - ex, cy1, cx + ex, cy0, 0.5), Ell(cx, cy1, ex, ey)], col, border=border, shadow=shadow)
    flat(c, RRect(cx + ex * 0.25, cy1, cx + ex, cy0, 0.5), lit(col, 0.82))
    flat(c, Ell(cx, cy1, ex, ey), lit(col, 1.12))
    return cx, cy1, ex, ey


def iso_tree(c, X, Y, s=1.0, col=(90, 170, 95)):
    cx, cy = P(X, Y)
    soft_union(c, [Ell(cx + 16 * s, cy + 4, 24 * s, 10 * s)], (40, 50, 40), 0.28, spread=6)
    piece(c, Thick(cx, cy, cx, cy - 30 * s, 6 * s), (135, 92, 66), border=1.5, shadow=ISO_SH)
    piece(c, [Circ(cx, cy - 44 * s, 20 * s), Circ(cx - 12 * s, cy - 34 * s, 13 * s), Circ(cx + 12 * s, cy - 33 * s, 13 * s)],
          col, border=2, shadow=ISO_SH)
    flat(c, Circ(cx - 6 * s, cy - 50 * s, 9 * s), lit(col, 1.2))


def iso_roof(c, X, Y, Z, dx, dy, h, col, stripe=None):
    """Gable roof with the ridge along X."""
    m = Y + dy / 2
    back = Poly([P(X, Y, Z), P(X + dx, Y, Z), P(X + dx, m, Z + h), P(X, m, Z + h)])
    front = Poly([P(X, m, Z + h), P(X + dx, m, Z + h), P(X + dx, Y + dy, Z), P(X, Y + dy, Z)])
    gable = Poly([P(X + dx, Y, Z), P(X + dx, Y + dy, Z), P(X + dx, m, Z + h)])
    piece(c, [back, front, gable], col, border=2, shadow=ISO_SH)
    flat(c, back, lit(col, 1.15))
    flat(c, gable, lit(col, 0.72))
    if stripe:
        n = 6
        for k in range(0, n, 2):
            x0, x1 = X + dx * k / n, X + dx * (k + 1) / n
            flat(c, Poly([P(x0, m, Z + h), P(x1, m, Z + h), P(x1, Y + dy, Z), P(x0, Y + dy, Z)]), stripe)


FERRIS = (360.0, 128.0)
FERRIS_R = 80.0
CAROUSEL = (6.5, 2.5)
FOUNTAIN = (5.0, 5.0)
BOOTH = (7.6, 6.2, 1.2, 1.0, 1.3)
VENDOR = (3.6, 7.6)
TRACK_Y = 9.35


def l11_background(c, d):
    """纸艺游乐园 - static part (the park fills the whole picture)"""
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (142, 198, 114), (134, 190, 108))
    # park boundary hedge and paths leading out of the picture
    flat(c, iso_quad(-0.3, -0.3, 10.3, 10.3), (150, 205, 120))
    for q in (iso_quad(4.4, 10, 5.6, 26), iso_quad(-16, 3.6, 0, 4.4), iso_quad(10, 2.0, 26, 3.0), iso_quad(1.8, -16, 3.0, 0)):
        piece(c, q, (238, 220, 186), shadow=(1, 2, 3, 0.25))
    draw_surround(c, L11_SURROUND, l11_decor, "back")
    # paths and plaza
    path = (238, 220, 186)
    for q in (iso_quad(4.4, 6.6, 5.6, 10), iso_quad(3.4, 3.4, 6.6, 6.6), iso_quad(6.6, 1.8, 8.2, 3.2), iso_quad(1.8, 3.6, 3.4, 4.6)):
        piece(c, q, path, shadow=(1, 2, 3, 0.25))
    for k in range(1, 6):
        flat(c, Poly([P(3.4 + k * 0.53, 3.4), P(3.4 + k * 0.53 + 0.03, 3.4), P(3.4 + k * 0.53 + 0.03, 6.6), P(3.4 + k * 0.53, 6.6)]),
             (222, 202, 168))
    # flower beds
    for X, Y in ((0.6, 2.2), (8.8, 8.6), (2.2, 6.2)):
        piece(c, iso_quad(X, Y, X + 1.1, Y + 1.1), (150, 110, 82), shadow=(1, 2, 3, 0.25))
        for i in range(5):
            fx, fy = P(X + 0.2 + (i % 3) * 0.35, Y + 0.25 + (i // 3) * 0.45)
            piece(c, Circ(fx, fy - 4, 5), [(255, 120, 160), (255, 220, 90), (250, 250, 245)][i % 3], shadow=(1, 2, 3, 0.3))
    # back trees
    for X, Y in ((0.7, 0.7), (3.0, 0.6), (9.3, 1.0), (0.6, 5.2)):
        iso_tree(c, X, Y)
    # ferris wheel support
    iso_box(c, 1.1, 3.6, 0, 1.0, 1.0, 0.18, (205, 200, 215))
    fx, fy = FERRIS
    for bx in (fx - 44, fx + 44):
        piece(c, Thick(fx, fy, bx, 232, 6), (190, 80, 90), border=1.5, shadow=ISO_SH)
    # carousel platform + pole
    X, Y = CAROUSEL
    iso_cyl(c, X, Y, 0, 0.3, 1.5, (245, 222, 190))
    cx, cy = P(X, Y, 0.3)
    piece(c, Thick(cx, cy, cx, P(X, Y, 2.25)[1], 5), (230, 190, 90), border=1.5, shadow=None)
    # fountain basin
    X, Y = FOUNTAIN
    bx, by, ex, ey = iso_cyl(c, X, Y, 0, 0.32, 0.85, (205, 205, 215))
    flat(c, Ell(bx, by, ex * 0.8, ey * 0.8), (120, 200, 235))
    flat(c, Ell(bx - ex * 0.2, by - ey * 0.15, ex * 0.3, ey * 0.25), (190, 232, 250))
    # ticket booth with striped roof (red in A, green in B)
    X, Y, dx, dy, dz = BOOTH
    _, front, _ = iso_box(c, X, Y, 0, dx, dy, dz, (250, 220, 185))
    flat(c, Poly([P(X + 0.25, Y + dy, 0.55), P(X + 0.95, Y + dy, 0.55), P(X + 0.95, Y + dy, 1.05), P(X + 0.25, Y + dy, 1.05)]),
         (80, 70, 90))
    flat(c, Poly([P(X + 0.2, Y + dy, 0.5), P(X + 1.0, Y + dy, 0.5), P(X + 1.0, Y + dy, 0.56), P(X + 0.2, Y + dy, 0.56)]),
         (230, 190, 90))
    iso_roof(c, X - 0.1, Y - 0.1, dz, dx + 0.2, dy + 0.2, 0.55, (250, 248, 240),
             stripe=(90, 180, 110) if "booth" in d else (230, 80, 80))
    # lamps around the plaza
    for X, Y in ((3.5, 3.5), (6.5, 6.5), (3.5, 6.5)):
        lx, ly = P(X, Y)
        piece(c, Thick(lx, ly, lx, ly - 42, 3), (80, 80, 95), shadow=ISO_SH)
        piece(c, Circ(lx, ly - 46, 6), (255, 230, 140), border=1.5, shadow=None)
    # balloon vendor (paper stand-up)
    vx, vy = P(*VENDOR)
    piece(c, [Poly([(vx - 9, vy), (vx + 9, vy), (vx + 6, vy - 30), (vx - 6, vy - 30)]), Circ(vx, vy - 38, 8)],
          (90, 140, 210), border=2, shadow=ISO_SH)
    flat(c, Circ(vx, vy - 38, 6.5), (250, 210, 180))
    flat(c, Poly([(vx - 8, vy - 44), (vx + 8, vy - 44), (vx, vy - 54)]), (230, 80, 80))
    # train track along the front-left edge
    a, b = P(0.6, TRACK_Y), P(9.6, TRACK_Y)
    for k in range(19):
        t = k / 18
        sx, sy = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        flat(c, Thick(sx - 7, sy - 7, sx + 7, sy + 7, 3), (150, 105, 75))
    for off in (-5, 5):
        flat(c, Thick(a[0] + off, a[1] - off, b[0] + off, b[1] - off, 2), (110, 110, 125))
    # front trees (one missing in B)
    for X, Y in ((9.3, 4.2), (9.4, 6.4), (1.3, 8.4), (7.0, 8.4)):
        if (X, Y) == (9.3, 4.2) and "tree" in d:
            continue
        iso_tree(c, X, Y, 0.9)
    from fill_iso import draw_surround
    draw_surround(c, L11_SURROUND, l11_decor, "front")


def l11_decor(c, X, Y, r):
    x, y = P(X, Y)
    if r < 0.45:
        iso_tree(c, X, Y, 0.75 + 0.35 * r)
    elif r < 0.65:
        piece(c, [Circ(x - 10, y - 8, 10), Circ(x + 6, y - 12, 12), Circ(x + 16, y - 6, 9)], (96, 172, 96), shadow=ISO_SH)
    elif r < 0.78:
        piece(c, Thick(x, y, x, y - 40, 3), (80, 80, 95), shadow=ISO_SH)
        piece(c, Circ(x, y - 44, 5), (255, 230, 140), border=1.5, shadow=None)
    elif r < 0.9:
        iso_box(c, X, Y, 0, 0.9, 0.3, 0.25, (170, 120, 85), border=1.5)
    else:
        for k in range(5):
            piece(c, Circ(x - 14 + k * 7, y - 4 + (k % 2) * 5, 4.5), [(255, 120, 160), (255, 220, 90), (250, 250, 245)][k % 3], shadow=(1, 2, 2, 0.3))


def _l11_surround():
    from fill_iso import surround_points
    return surround_points(11, step=62)


L11_SURROUND = _l11_surround()


def l11_wheel(c, m):
    fx, fy = FERRIS
    R = FERRIS_R
    rim = [Thick(fx + R * math.cos(math.radians(k * 22.5)), fy + R * math.sin(math.radians(k * 22.5)),
                 fx + R * math.cos(math.radians(k * 22.5 + 22.5)), fy + R * math.sin(math.radians(k * 22.5 + 22.5)), 5)
           for k in range(16)]
    spokes = [Thick(fx, fy, fx + R * math.cos(math.radians(a)), fy + R * math.sin(math.radians(a)), 2.5) for a in range(0, 360, 45)]
    piece(c, rim + spokes, (240, 90, 110), border=1.5, shadow=ISO_SH)
    inner = [Thick(fx + R * 0.55 * math.cos(math.radians(a)), fy + R * 0.55 * math.sin(math.radians(a)),
                   fx + R * 0.55 * math.cos(math.radians(a + 45)), fy + R * 0.55 * math.sin(math.radians(a + 45)), 2.5) for a in range(0, 360, 45)]
    flat(c, inner, (250, 200, 90))
    piece(c, Circ(fx, fy, 9), (250, 200, 90), border=1.5, shadow=None)


GONDOLA_COLS = [(90, 160, 220), (250, 200, 80), (120, 200, 130), (200, 130, 220)]


def l11_gondola(col):
    def d(c, m):
        fx, fy = FERRIS
        flat(c, Thick(fx, fy, fx, fy + 9, 1.6), (90, 80, 90))
        piece(c, [RRect(fx - 10, fy + 8, fx + 10, fy + 24, 4), Poly([(fx - 12, fy + 10), (fx + 12, fy + 10), (fx, fy + 3)])],
              col, border=1.5, shadow=(2, 4, 4, 0.35))
        flat(c, RRect(fx - 6, fy + 11, fx + 6, fy + 17, 2), (250, 245, 230))
    return d


def l11_horse(col):
    def d(c, m):
        cx, cy = P(*CAROUSEL, 1.0)
        flat(c, Thick(cx, cy - 26, cx, cy + 18, 2), (230, 190, 90))
        piece(c, [Ell(cx, cy, 13, 7), Poly([(cx - 10, cy - 3), (cx - 18, cy - 15), (cx - 11, cy - 17), (cx - 5, cy - 4)]),
                  Thick(cx - 7, cy + 4, cx - 9, cy + 13, 2.5), Thick(cx + 7, cy + 4, cx + 10, cy + 13, 2.5),
                  Thick(cx + 12, cy - 2, cx + 18, cy + 6, 2.5)], col, border=1.5, shadow=(1, 3, 4, 0.35))
        flat(c, Thick(cx - 12, cy - 15, cx - 7, cy - 4, 2), (230, 120, 90))
        flat(c, Circ(cx - 15, cy - 13, 1.2), INK)
    return d


def l11_canopy(c, m):
    X, Y = CAROUSEL
    apex = P(X, Y, 3.3)
    cx, cy = P(X, Y, 2.2)
    ex, ey = 1.75 * T * math.sqrt(2), 1.75 * T * math.sqrt(2) / 2
    stripe = (80, 130, 220) if m else (230, 80, 80)
    rim = [(cx + ex * math.cos(math.radians(a)), cy + ey * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    shape = Poly([apex] + [(cx + ex, cy)] + rim[1:-1] + [(cx - ex, cy)])
    piece(c, shape, (252, 248, 238), border=2, shadow=ISO_SH)
    for k in range(0, len(rim) - 1, 2):
        flat(c, Poly([apex, rim[k], rim[k + 1]]), stripe)
    for k in range(0, len(rim) - 1):
        mx = (rim[k][0] + rim[k + 1][0]) / 2
        my = (rim[k][1] + rim[k + 1][1]) / 2
        piece(c, Ell(mx, my + 3, 7, 6), stripe if k % 2 == 0 else (252, 248, 238), shadow=(1, 2, 3, 0.25))
    flat(c, Thick(apex[0], apex[1], apex[0], apex[1] - 16, 2), (120, 100, 90))
    piece(c, Poly([(apex[0], apex[1] - 16), (apex[0] + 14, apex[1] - 12), (apex[0], apex[1] - 8)]), (250, 200, 80), shadow=None)


def l11_spray(c, m):
    bx, by = P(*FOUNTAIN, 0.32)
    for k in range(8):
        a = math.radians(-90 + (k - 3.5) * 22)
        for j in range(4):
            t = (j + 1) / 4
            x = bx + math.cos(a) * 34 * t
            y = by - 46 * math.sin(t * math.pi) * 0.9 - 6 * t + math.sin(a) * 4
            flat(c, Circ(x, y, 3.2 - j * 0.4), (225, 245, 255))
    piece(c, Thick(bx, by, bx, by - 30, 4), (225, 245, 255), shadow=None)


def l11_balloon(dx, dy, col, col_b=None):
    def d(c, m):
        col_ = col_b if (m and col_b) else col
        hx, hy = P(*VENDOR)
        hx, hy = hx + 8, hy - 26
        tx, ty = hx + dx, hy - dy
        flat(c, Thick(hx, hy, tx, ty + 12, 1), (110, 100, 110))
        piece(c, [Ell(tx, ty, 10, 12), Poly([(tx - 3, ty + 11), (tx + 3, ty + 11), (tx, ty + 15)])], col_, border=1.5, shadow=ISO_SH)
        flat(c, Ell(tx - 3, ty - 4, 2.5, 3.5), lit(col_, 1.35))
    return d


FLAG_BASE = P(BOOTH[0] + BOOTH[2] + 0.1, BOOTH[1] + BOOTH[3] / 2, BOOTH[4] + 0.55)


def l11_flag(c, m):
    px, py = FLAG_BASE
    flat(c, Thick(px, py, px, py - 24, 1.8), (100, 90, 95))
    piece(c, Poly([(px, py - 24), (px + 20, py - 19), (px, py - 13)]), (250, 200, 70), border=1.2, shadow=(1, 3, 3, 0.3))


def l11_train(c, m):
    Y = TRACK_Y - 0.3
    for X0, col in ((2.0, (120, 190, 220)), (3.1, (250, 200, 90))):
        iso_box(c, X0, Y, 0.1, 0.95, 0.6, 0.5, col, border=1.5)
        for wx in (X0 + 0.2, X0 + 0.75):
            wcx, wcy = P(wx, Y + 0.6, 0.12)
            piece(c, Circ(wcx, wcy, 4.5), (70, 65, 80), shadow=None)
    iso_box(c, 4.2, Y, 0.1, 1.1, 0.6, 0.45, (230, 80, 80), border=1.5)
    iso_box(c, 4.2, Y, 0.55, 0.45, 0.6, 0.45, (230, 80, 80), border=1.5)
    cx, cy, ex, ey = iso_cyl(c, 5.0, Y + 0.3, 0.55, 0.95, 0.12, (70, 65, 80), border=1.2)
    for wx in (4.4, 5.05):
        wcx, wcy = P(wx, Y + 0.6, 0.12)
        piece(c, Circ(wcx, wcy, 5), (70, 65, 80), shadow=None)


def l11_puff(c, m):
    cx, cy = P(5.0, TRACK_Y, 1.2)
    piece(c, Circ(cx, cy, 6), (250, 248, 245), shadow=(1, 2, 3, 0.25))


_trk = (P(1, TRACK_Y)[0] - P(0, TRACK_Y)[0], P(1, TRACK_Y)[1] - P(0, TRACK_Y)[1])
_tl = math.hypot(*_trk)
TRACK_DIR = (_trk[0] / _tl, -_trk[1] / _tl)     # Unity y-up
TRAIN_SPEED = 30.0
TRAIN = dict(driftVelocity=(TRACK_DIR[0] * TRAIN_SPEED, TRACK_DIR[1] * TRAIN_SPEED), driftLength=_tl * 6.4,
             driftStart=-_tl * 1.6, driftFade=True)
_GONDOLA_SPEED = 0.035

L11_ELEMENTS = [
    E("cloud1", paper_cloud(150, 60, 0.9), anim=drift_across(110, 190, 8)),
    E("cloud2", paper_cloud(700, 40, 0.7), anim=drift_across(670, 730, 6)),
    E("cloud3", paper_cloud(820, 470, 0.8), anim=drift_across(785, 855, 9)),
    # ferris wheel turns the other way in B (spokes and gondolas together)
    E("ferris", l11_wheel, pivot=FERRIS, anim=dict(rotateSpeed=_GONDOLA_SPEED * 360),
      animB=dict(rotateSpeed=-_GONDOLA_SPEED * 360)),
] + [
    E("gondola%d" % i, l11_gondola(GONDOLA_COLS[i % 4]), pivot=FERRIS,
      anim=dict(orbitRadius=(FERRIS_R, FERRIS_R), orbitSpeed=_GONDOLA_SPEED, swingAngle=4, swingSpeed=0.5, phase=i / 8),
      animB=dict(orbitRadius=(FERRIS_R, FERRIS_R), orbitSpeed=-_GONDOLA_SPEED, swingAngle=4, swingSpeed=0.5, phase=i / 8))
    for i in range(8)
] + [
    E("horse%d" % i, l11_horse(col), pivot=P(*CAROUSEL, 1.0),
      anim=dict(orbitRadius=(58, 27), orbitSpeed=0.08, orbitDepth=0.28, bobAmplitude=(0, 7), bobSpeed=0.5, phase=i / 4))
    for i, col in enumerate(((252, 250, 245), (250, 190, 200), (190, 215, 250), (250, 225, 150)))
] + [
    E("canopy", l11_canopy, variant=True),
    E("spray", l11_spray, show="A", pivot=P(*FOUNTAIN, 0.32),
      anim=dict(stretch=(0.08, 0.18), scaleSpeed=0.7, twinkle=0.2, twinkleSpeed=1.4)),
    E("flag", l11_flag, show="A", pivot=(FLAG_BASE[0], FLAG_BASE[1] - 19),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.6, swingAngle=4, swingSpeed=1.2)),
] + [
    # the third balloon is blue in A and pink in B
    E("balloon%d" % i, l11_balloon(dx, dy, col, (250, 140, 190) if i == 2 else None),
      pivot=(P(*VENDOR)[0] + 8, P(*VENDOR)[1] - 26), variant=(i == 2),
      anim=dict(swingAngle=7, swingSpeed=0.3 + 0.05 * i, phase=i * 0.2))
    for i, (dx, dy, col) in enumerate(((-14, 48, (230, 80, 80)), (2, 58, (250, 200, 70)), (16, 50, (90, 150, 230)), (28, 40, (120, 200, 120))))
] + [
    E("balloon_free", l11_balloon(40, 70, (200, 130, 220)), anim=dict(driftVelocity=(4, 18), driftLength=150, driftFade=True,
                                                                        swingAngle=6, swingSpeed=0.4)),
    E("train", l11_train, anim=dict(TRAIN)),
]

L11_DIFFS = [
    ("ferris", int(FERRIS[0]), int(FERRIS[1]), 88),
    ("canopy", int(P(*CAROUSEL, 2.6)[0]), int(P(*CAROUSEL, 2.6)[1]), 0),
    ("booth", int(P(BOOTH[0] + 0.6, BOOTH[1] + 0.5, 1.6)[0]), int(P(BOOTH[0] + 0.6, BOOTH[1] + 0.5, 1.6)[1]), 0),
    ("balloon", int(P(*VENDOR)[0] + 24), int(P(*VENDOR)[1] - 76), 0),
    ("flag", int(FLAG_BASE[0] + 10), int(FLAG_BASE[1] - 18), 20),
    ("tree", int(P(9.3, 4.2)[0]), int(P(9.3, 4.2)[1] - 38), 0),
    ("fountain", int(P(*FOUNTAIN)[0]), int(P(*FOUNTAIN, 0.32)[1] - 24), 40),
]


LEVELS = [
    ("Level10", "纸艺地下", l10_background, L10_ELEMENTS, L10_DIFFS, 130, OPTS),
    ("Level11", "纸艺游乐园", l11_background, L11_ELEMENTS, L11_DIFFS, 140, OPTS),
]
