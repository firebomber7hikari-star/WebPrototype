# -*- coding: utf-8 -*-
"""
Paper-craft levels seen from straight above (top-down camera):
  Level08 纸艺野餐 (picnic in the park: blanket, pond with koi, ants, frisbee)
  Level09 纸艺小镇 (little town: roads with traffic, pool, fountain, hot-air balloon)

Height is sold by the shadow offset: flat things (blanket, plates) barely lift off the
ground, roofs and tree crowns throw long shadows, the balloon's shadow is far away and
changes with its altitude. Drifting cloud shadows sweep over the whole scene.
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union

OPTS = {"post": paper_post}
INK = (70, 55, 65)
FLAT = (1, 2, 4, 0.3)        # paper lying on the ground
LOW = (2, 4, 6, 0.36)        # plates, cups, cars
MID = (5, 8, 8, 0.38)        # roofs, umbrellas
TREE = (9, 13, 11, 0.4)      # tree crowns


# ------------------------------------------------------------------- helpers
def drift_line(span_min, span_max, extent, speed, axis="x", sign=1):
    """Looping straight drift across the picture.
    span_*: element extent on the moving axis (scene px), sign: +1 = towards larger scene coordinate."""
    if sign > 0:
        s_min, s_max = -(span_max + 10), extent + 10 - span_min
    else:
        s_min, s_max = -(extent + 10 - span_min), span_max + 10
    length = s_max - s_min
    if axis == "x":
        v = (speed * sign, 0)
    else:
        v = (0, -speed * sign)        # Unity y is up
    return dict(driftVelocity=v, driftLength=length, driftStart=s_min, phase=(-s_min / length) % 1.0)


def rot_poly(cx, cy, w, h, deg):
    a = math.radians(deg)
    ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    return Poly([(cx + ux * w / 2 * sx + vx * h / 2 * sy, cy + uy * w / 2 * sx + vy * h / 2 * sy)
                 for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))])


def canopy(c, x, y, r, base=(72, 150, 82)):
    shapes = [Circ(x + dx * r, y + dy * r, rr * r)
              for dx, dy, rr in ((0, 0, 1.0), (-0.55, -0.2, 0.62), (0.5, -0.3, 0.6), (0.35, 0.5, 0.6), (-0.4, 0.45, 0.55))]
    piece(c, shapes, base, shadow=TREE)
    piece(c, Circ(x - 0.15 * r, y - 0.15 * r, 0.62 * r), lit(base, 1.15), shadow=(2, 3, 6, 0.25))
    piece(c, Circ(x - 0.32 * r, y - 0.32 * r, 0.3 * r), lit(base, 1.32), shadow=(1, 2, 4, 0.2))


def gable_roof(c, x, y, w, h, col, ridge_x=True, chimney=None):
    piece(c, RRect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 3), col, border=2.5, shadow=MID)
    if ridge_x:
        flat(c, RRect(x - w / 2, y - h / 2, x + w / 2, y, 3), lit(col, 1.14))
        flat(c, Thick(x - w / 2 + 3, y, x + w / 2 - 3, y, 2.5), lit(col, 1.3))
    else:
        flat(c, RRect(x - w / 2, y - h / 2, x, y + h / 2, 3), lit(col, 1.14))
        flat(c, Thick(x, y - h / 2 + 3, x, y + h / 2 - 3, 2.5), lit(col, 1.3))
    if chimney:
        cx, cy = chimney
        piece(c, RRect(cx - 6, cy - 6, cx + 6, cy + 6, 1.5), (150, 95, 85), border=1.5, shadow=(3, 5, 5, 0.35))


def car(c, x, y, d, col, shadow=LOW):
    """Top-down car; d = 'R', 'L', 'D', 'U' (direction it faces in the picture)."""
    fx, fy = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1)}[d]

    def box(cx, cy, along, side, r):
        hw = along / 2 if fx else side / 2
        hh = side / 2 if fx else along / 2
        return RRect(cx - hw, cy - hh, cx + hw, cy + hh, r)
    piece(c, box(x, y, 36, 19, 6), col, border=2, shadow=shadow)
    flat(c, box(x + fx * 6, y + fy * 6, 7, 15, 2), (70, 80, 105))
    flat(c, box(x - fx * 3, y - fy * 3, 11, 15, 3), lit(col, 1.2))
    flat(c, box(x - fx * 12, y - fy * 12, 4, 14, 1.5), (70, 80, 105))
    sx, sy = -fy, fx
    for k in (-1, 1):
        flat(c, Circ(x + fx * 16 + sx * 6 * k, y + fy * 16 + sy * 6 * k, 2.2), (255, 245, 190))


def cloud_shadow(cx, cy, k):
    def d(c, m):
        shapes = [Circ(cx + dx * k, cy + dy * k, r * k) for dx, dy, r in
                  ((0, 0, 40), (45, -12, 48), (92, 4, 38), (40, 22, 36), (-36, 14, 26))]
        soft_union(c, shapes, (40, 50, 60), 0.16, spread=14)
    return d


def butterfly_td(x, y, col):
    def d(c, m):
        for sy in (-1, 1):
            piece(c, [Ell(x - 2, y + sy * 8, 7, 7), Ell(x + 6, y + sy * 6, 5, 5)], col, shadow=(3, 5, 4, 0.3))
        flat(c, Ell(x + 1, y, 8, 2), INK)
    return d


def ripple(x, y, r):
    def d(c, m):
        c.ellipse_ring(x, y, r, r * 0.75, 1.6, (235, 248, 255, 0.85))
    return d


# =================================================================== Level 08
POND = (760, 135)
BLANKET = (440, 320, 330, 240, -8)


def blanket_pt(u, v):
    cx, cy, w, h, deg = BLANKET
    a = math.radians(deg)
    return (cx + math.cos(a) * u * w - math.sin(a) * v * h, cy + math.sin(a) * u * w + math.cos(a) * v * h)


def blanket_band(u0, u1, v0, v1):
    return Poly([blanket_pt(u0, v0), blanket_pt(u1, v0), blanket_pt(u1, v1), blanket_pt(u0, v1)])


def l8_background(c, d):
    """纸艺野餐 - static part"""
    c.rect(0, 0, W, 660, (150, 204, 112))
    rnd = random.Random(21)
    for _ in range(9):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(40, 80)
        piece(c, [Circ(x, y, r), Circ(x + r * 0.8, y + r * 0.2, r * 0.7), Circ(x - r * 0.7, y + r * 0.3, r * 0.6)],
              (162, 214, 124), shadow=FLAT)
    for _ in range(70):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        flat(c, Poly([(x - 5, y + 4), (x - 2, y - 6), (x, y + 1), (x + 3, y - 7), (x + 5, y + 4)]), (118, 176, 92))
    # stepping-stone path
    for i in range(7):
        t = i / 6
        x, y = 60 + 230 * t, 590 - 190 * t + 30 * math.sin(t * 3)
        piece(c, Ell(x, y, 19, 14), (236, 226, 202), shadow=LOW)
    # pond: stepped paper rings get darker and deeper towards the middle
    px, py = POND
    piece(c, Ell(px, py, 165, 105), (205, 190, 150), shadow=FLAT)
    for rx, ry, col in ((150, 92, (118, 190, 222)), (112, 68, (96, 172, 214)), (70, 42, (78, 152, 202)), (34, 20, (62, 134, 190))):
        c.ellipse(px + 3, py + 4, rx + 3, ry + 3, (30, 60, 90, 0.18))
        flat(c, Ell(px, py, rx, ry), col)
    # flower bed (bottom left); one flower changes colour
    piece(c, RRect(30, 470, 230, 585, 28), (150, 105, 80), shadow=FLAT)
    for i, (x, y) in enumerate(((60, 500), (100, 520), (145, 495), (190, 520), (75, 555), (125, 560), (175, 558), (210, 490))):
        col = [(255, 120, 160), (255, 220, 90), (255, 255, 250), (200, 140, 255)][i % 4]
        if i == 6:
            col = (180, 120, 255) if "flower" in d else (255, 120, 160)
        petals = [Circ(x + 8 * math.cos(math.radians(a)), y + 8 * math.sin(math.radians(a)), 6.5) for a in range(0, 360, 72)]
        piece(c, petals, col, shadow=LOW)
        flat(c, Circ(x, y, 4.5), (255, 200, 70))

    # picnic blanket with a gingham pattern
    cx, cy, w, h, deg = BLANKET
    piece(c, rot_poly(cx, cy, w, h, deg), (222, 72, 72), border=3, shadow=FLAT)
    for k in range(-5, 6):
        u = k / 11
        flat(c, blanket_band(u - 0.022, u + 0.022, -0.5, 0.5), (255, 255, 255, 0.38))
    for k in range(-4, 5):
        v = k / 9
        flat(c, blanket_band(-0.5, 0.5, v - 0.03, v + 0.03), (255, 255, 255, 0.38))
    # basket
    bx, by = 355, 270
    piece(c, Ell(bx, by, 54, 40), (195, 135, 72), border=2.5, shadow=MID)
    flat(c, Ell(bx, by, 44, 31), (176, 116, 60))
    for k in range(-3, 4):
        flat(c, Thick(bx + k * 11, by - 28, bx + k * 11, by + 28, 2), (210, 155, 90))
    flat(c, Poly([(bx - 30, by - 8), (bx - 6, by - 24), (bx + 4, by - 6), (bx - 20, by + 10)]), (240, 240, 235))
    piece(c, [Thick(bx - 44, by + 2, bx - 20, by - 30, 5), Thick(bx - 20, by - 30, bx + 20, by - 30, 5),
              Thick(bx + 20, by - 30, bx + 44, by + 2, 5)], (150, 95, 50), shadow=(5, 8, 5, 0.35))
    # plate with sandwich (missing in B)
    piece(c, Circ(478, 262, 36), (252, 250, 245), border=0, shadow=LOW)
    flat(c, Circ(478, 262, 27), (236, 234, 228))
    if "sandwich" not in d:
        piece(c, Poly([(458, 248), (500, 252), (470, 284)]), (240, 205, 140), border=2, shadow=FLAT)
        flat(c, Poly([(462, 251), (495, 254), (471, 278)]), (250, 228, 180))
        flat(c, Thick(458, 248, 500, 252, 2.5), (110, 190, 90))
    # watermelon slices
    piece(c, Circ(528, 365, 38), (252, 250, 245), shadow=LOW)
    flat(c, Circ(528, 365, 29), (236, 234, 228))
    flesh = (250, 212, 80) if "watermelon" in d else (232, 72, 84)
    for ox, oy, rot in ((-8, -4, 200), (10, 6, 30)):
        x0, y0 = 528 + ox, 365 + oy
        pts = [(x0 + 22 * math.cos(math.radians(rot + a)), y0 + 22 * math.sin(math.radians(rot + a))) for a in range(0, 181, 15)]
        piece(c, Poly(pts), (90, 170, 80), shadow=FLAT)
        inner = [(x0 + 17 * math.cos(math.radians(rot + a)), y0 + 17 * math.sin(math.radians(rot + a))) for a in range(0, 181, 15)]
        flat(c, Poly(inner), flesh)
        for a in (50, 90, 130):
            flat(c, Ell(x0 + 10 * math.cos(math.radians(rot + a)), y0 + 10 * math.sin(math.radians(rot + a)), 1.6, 1.6), INK)
    # strawberries
    piece(c, Circ(330, 375, 30), (250, 238, 215), shadow=LOW)
    for x, y in ((320, 368), (338, 364), (330, 382), (316, 384), (344, 380)):
        piece(c, Ell(x, y, 7, 6), (230, 60, 70), shadow=(1, 2, 3, 0.3))
        flat(c, Circ(x - 3, y - 3, 2.6), (90, 170, 80))
    # cup (blue in A, green in B)
    cup = (100, 190, 110) if "cup" in d else (90, 150, 232)
    piece(c, Circ(418, 395, 17), cup, border=2, shadow=MID)
    flat(c, Circ(418, 395, 12), (165, 105, 70))
    flat(c, Circ(414, 391, 3), (215, 170, 130))
    # trees (crowns cast long shadows)
    for x, y, r in ((70, 70, 62), (210, 40, 44), (60, 330, 50), (850, 545, 64), (700, 560, 40)):
        canopy(c, x, y, r)


def l8_koi(x, y, body, spot):
    def d(c, m):
        piece(c, [Ell(x, y, 17, 7), Poly([(x - 14, y), (x - 27, y - 8), (x - 23, y), (x - 27, y + 8)])], body, shadow=(2, 4, 4, 0.3))
        flat(c, [Ell(x + 4, y - 1, 5, 3), Ell(x - 6, y + 1, 4, 2.5)], spot)
        flat(c, [Circ(x + 12, y - 3, 1.3), Circ(x + 12, y + 3, 1.3)], INK)
    return d


def l8_lily(x, y, r, flower=False):
    def d(c, m):
        a0 = random.Random(int(x * 7 + y)).uniform(0, 360)
        pts = [(x, y)] + [(x + r * math.cos(math.radians(a0 + a)), y + r * math.sin(math.radians(a0 + a))) for a in range(20, 341, 20)]
        piece(c, Poly(pts), (90, 170, 95), shadow=LOW)
        if flower:
            for a in range(0, 360, 60):
                flat(c, Ell(x + 4 * math.cos(math.radians(a)), y + 4 * math.sin(math.radians(a)), 4, 4), (255, 170, 205))
            flat(c, Circ(x, y, 2.5), (255, 225, 110))
    return d


def l8_frisbee(c, m):
    x, y, r = 215, 455, 27
    piece(c, Circ(x, y, r), (255, 165, 60), border=2, shadow=LOW)
    flat(c, Circ(x, y, r - 7), (255, 190, 95))
    for k in (-1, 0, 1):
        off = k * 9
        half = math.sqrt(max(0.0, (r - 3) ** 2 - off ** 2))
        flat(c, Thick(x - half, y + off, x + half, y + off, 2.5), (255, 245, 225))
    flat(c, Circ(x, y, 4), (230, 110, 50))


def l8_ant(x, y, dx, dy):
    def d(c, m):
        for k, r in ((0, 3.2), (1, 2.4), (2, 3.6)):
            flat(c, Circ(x - dx * k * 5, y - dy * k * 5, r), (55, 40, 45))
        sx, sy = -dy, dx
        for k in (0.5, 1.2, 1.9):
            px, py = x - dx * k * 5, y - dy * k * 5
            flat(c, Thick(px - sx * 5, py - sy * 5, px + sx * 5, py + sy * 5, 0.9), (55, 40, 45))
    return d


def l8_bee(x, y):
    def d(c, m):
        piece(c, [Ell(x - 2, y - 6, 5, 4), Ell(x - 2, y + 6, 5, 4)], (235, 245, 255), shadow=(4, 6, 4, 0.25))
        piece(c, Ell(x, y, 7, 5), (255, 210, 60), shadow=(4, 6, 4, 0.3))
        flat(c, [Thick(x - 2, y - 5, x - 2, y + 5, 2), Thick(x + 3, y - 4, x + 3, y + 4, 2)], INK)
    return d


ANT_A, ANT_B = (566, 572), (536, 440)
_adx, _ady = ANT_B[0] - ANT_A[0], ANT_B[1] - ANT_A[1]
_alen = math.hypot(_adx, _ady)
ANT_DIR = (_adx / _alen, _ady / _alen)

L8_ELEMENTS = [
    E("lily1", l8_lily(700, 110, 18, True), anim=dict(swingAngle=8, swingSpeed=0.1, bobAmplitude=(3, 2), bobSpeed=0.15)),
    E("lily2", l8_lily(820, 165, 15), anim=dict(swingAngle=10, swingSpeed=0.12, bobAmplitude=(3, 2), bobSpeed=0.13, phase=0.5)),
    E("lily3", l8_lily(790, 85, 13), anim=dict(swingAngle=9, swingSpeed=0.09, bobAmplitude=(2, 3), bobSpeed=0.17, phase=0.3)),
    E("koi1", l8_koi(POND[0], POND[1], (255, 140, 60), (255, 250, 240)), pivot=POND,
      anim=dict(orbitRadius=(105, 58), orbitSpeed=0.07, orbitAlign=True, swingAngle=8, swingSpeed=1.2)),
    # the white koi swims the other way round in the modified picture
    E("koi", l8_koi(POND[0], POND[1], (252, 250, 245), (235, 70, 60)), pivot=POND,
      anim=dict(orbitRadius=(66, 38), orbitSpeed=0.09, orbitAlign=True, swingAngle=8, swingSpeed=1.4, phase=0.5),
      animB=dict(orbitRadius=(66, 38), orbitSpeed=-0.09, orbitAlign=True, swingAngle=8, swingSpeed=1.4, phase=0.5)),
    E("ripple1", ripple(700, 160, 14), anim=dict(driftVelocity=(0, -0.5), driftLength=2, driftFade=True, driftGrow=1.6)),
    E("ripple2", ripple(805, 120, 12), anim=dict(driftVelocity=(0, -0.5), driftLength=2, driftFade=True, driftGrow=1.6, phase=0.5)),
    E("frisbee", l8_frisbee, pivot=(215, 455), anim=dict(rotateSpeed=-160), animB={}),
] + [
    E("ant%d" % i, l8_ant(ANT_A[0], ANT_A[1], *ANT_DIR), show="A", pivot=ANT_A,
      anim=dict(driftVelocity=(ANT_DIR[0] * 14, -ANT_DIR[1] * 14), driftLength=_alen, driftFade=True, phase=i / 6))
    for i in range(6)
] + [
    E("butterfly1", butterfly_td(300, 160, (255, 150, 200)), pivot=(300, 160),
      anim=dict(orbitRadius=(70, 45), orbitSpeed=0.12, orbitAlign=True, stretch=(0, 0.6), scaleSpeed=4)),
    E("butterfly2", butterfly_td(640, 470, (255, 215, 80)), pivot=(640, 470),
      anim=dict(orbitRadius=(55, 70), orbitSpeed=-0.1, orbitAlign=True, stretch=(0, 0.6), scaleSpeed=4.6, phase=0.3)),
    E("bee", l8_bee(140, 520), pivot=(140, 520),
      anim=dict(orbitRadius=(40, 28), orbitSpeed=0.3, orbitAlign=True, bobAmplitude=(5, 5), bobSpeed=1.5)),
    E("cloudshadow1", cloud_shadow(200, 150, 1.6), anim=drift_line(140, 390, W, 14, sign=1)),
    E("cloudshadow2", cloud_shadow(600, 430, 1.3), anim=dict(drift_line(555, 750, W, 10, sign=1), phase=0.6)),
]

L8_DIFFS = [
    ("koi", POND[0], POND[1], 75),
    ("ants", 551, 506, 70),
    ("watermelon", 528, 365, 36),
    ("cup", 418, 395, 22),
    ("sandwich", 478, 264, 30),
    ("frisbee", 215, 455, 32),
    ("flower", 175, 558, 18),
]


# =================================================================== Level 09
ROAD_Y, ROAD_X = 300, 330
RIVER_X = 715
POOL = (85, 410, 235, 520)
FOUNTAIN = (815, 140)


def l9_background(c, d):
    """纸艺小镇 - static part"""
    c.rect(0, 0, W, 660, (152, 202, 118))
    # river with soft banks
    left = [(RIVER_X - 38 + 10 * math.sin(y * 0.02), y) for y in range(-20, 641, 20)]
    right = [(RIVER_X + 38 + 10 * math.sin(y * 0.02 + 1), y) for y in range(640, -21, -20)]
    piece(c, Poly([(x - 9, y) for x, y in left] + [(x + 9, y) for x, y in right]), (214, 198, 156), shadow=FLAT)
    flat(c, Poly(left + right), (104, 178, 222))
    flat(c, Poly([(x + 12, y) for x, y in left] + [(x - 12, y) for x, y in right]), (90, 165, 214))
    # roads
    piece(c, RRect(-20, ROAD_Y - 30, 920, ROAD_Y + 30, 2), (152, 150, 160), shadow=FLAT)
    piece(c, RRect(ROAD_X - 30, -20, ROAD_X + 30, 620, 2), (152, 150, 160), shadow=FLAT)
    for x in range(0, 900, 44):
        if abs(x + 11 - ROAD_X) > 40:
            flat(c, RRect(x, ROAD_Y - 2, x + 22, ROAD_Y + 2, 1), (250, 248, 240))
    for y in range(0, 600, 44):
        if abs(y + 11 - ROAD_Y) > 40:
            flat(c, RRect(ROAD_X - 2, y, ROAD_X + 2, y + 22, 1), (250, 248, 240))
    if "crosswalk" not in d:
        for k in range(6):
            y = ROAD_Y - 25 + k * 9
            flat(c, RRect(ROAD_X + 38, y, ROAD_X + 58, y + 5, 1), (250, 248, 240))
    for k in range(6):
        x = ROAD_X - 25 + k * 9
        flat(c, RRect(x, ROAD_Y - 58, x + 5, ROAD_Y - 38, 1), (250, 248, 240))
    # bridge over the river
    piece(c, RRect(RIVER_X - 62, ROAD_Y - 36, RIVER_X + 62, ROAD_Y + 36, 3), (182, 160, 135), border=2, shadow=MID)
    flat(c, RRect(RIVER_X - 62, ROAD_Y - 28, RIVER_X + 62, ROAD_Y + 28, 1), (165, 162, 172))
    for sy in (-1, 1):
        piece(c, Thick(RIVER_X - 60, ROAD_Y + sy * 33, RIVER_X + 60, ROAD_Y + sy * 33, 5), (120, 90, 75), shadow=(3, 5, 4, 0.35))

    # houses (top-left block); the middle roof changes colour
    gable_roof(c, 80, 90, 96, 70, (215, 95, 85), chimney=(105, 74))
    gable_roof(c, 205, 105, 80, 90, (90, 140, 210) if "roof" in d else (220, 95, 80), ridge_x=False, chimney=(190, 80))
    gable_roof(c, 120, 205, 110, 60, (240, 190, 90))
    # houses (top-right block, left of the river)
    gable_roof(c, 430, 90, 92, 66, (130, 170, 120), chimney=(455, 74))
    gable_roof(c, 560, 120, 76, 96, (200, 120, 170), ridge_x=False)
    gable_roof(c, 470, 215, 120, 56, (120, 150, 200), chimney=(505, 205))
    # bottom-left block: pool with umbrella
    x0, y0, x1, y1 = POOL
    piece(c, RRect(x0 - 16, y0 - 16, x1 + 16, y1 + 16, 6), (245, 238, 225), border=0, shadow=FLAT)
    flat(c, RRect(x0, y0, x1, y1, 5), (118, 204, 236))
    flat(c, Poly([(x0, y0), (x1, y0), (x1 - 6, y0 + 6), (x0 + 6, y0 + 6), (x0 + 6, y1 - 6), (x0, y1)]), (30, 70, 100, 0.22))
    for k in (1, 2):
        y = y0 + (y1 - y0) * k / 3
        for x in range(int(x0) + 6, int(x1) - 6, 12):
            flat(c, Circ(x, y, 2.2), (255, 255, 255) if (x // 12) % 2 else (235, 80, 80))
    um_x, um_y = 270, 410
    tris = [Poly([(um_x, um_y), (um_x + 34 * math.cos(math.radians(a)), um_y + 34 * math.sin(math.radians(a))),
                  (um_x + 34 * math.cos(math.radians(a + 45)), um_y + 34 * math.sin(math.radians(a + 45)))])
            for a in range(0, 360, 45)]
    piece(c, tris, (250, 248, 240), border=2, shadow=MID)
    stripe = (90, 180, 110) if "umbrella" in d else (230, 80, 80)
    for i, t in enumerate(tris):
        if i % 2 == 0:
            flat(c, t, stripe)
    flat(c, Circ(um_x, um_y, 3.5), (120, 90, 75))
    gable_roof(c, 130, 575, 120, 50, (170, 120, 95))
    # bottom-right block: parking lot
    piece(c, RRect(400, 360, 640, 570, 6), (128, 128, 138), shadow=FLAT)
    for x in range(410, 640, 46):
        flat(c, Thick(x, 368, x, 410, 2), (245, 245, 240))
        flat(c, Thick(x, 520, x, 562, 2), (245, 245, 240))
    parked = [(433, 390, (230, 80, 80)), (479, 390, (250, 250, 245)), (571, 390, (80, 140, 210)),
              (456, 541, (120, 190, 120)), (548, 541, (240, 200, 70)), (594, 541, (160, 160, 170))]
    for x, y, col in parked:
        if (x, y) == (548, 541) and "parkedcar" in d:
            col = (160, 110, 210)
        car(c, x, y, "D" if y < 450 else "U", col)
    # park with fountain (east of the river)
    fx, fy = FOUNTAIN
    piece(c, Circ(fx, fy, 70), (232, 222, 200), shadow=FLAT)
    for a in range(0, 360, 30):
        flat(c, Thick(fx + 50 * math.cos(math.radians(a)), fy + 50 * math.sin(math.radians(a)),
                      fx + 68 * math.cos(math.radians(a)), fy + 68 * math.sin(math.radians(a)), 1.5), (210, 198, 175))
    piece(c, Circ(fx, fy, 44), (205, 200, 210), border=0, shadow=LOW)
    flat(c, Circ(fx, fy, 37), (118, 196, 232))
    piece(c, Circ(fx, fy, 9), (215, 210, 220), shadow=LOW)
    # trees; one in the top-right block is missing in B
    trees = [(30, 270, 26), (265, 200, 30), (380, 160, 28), (620, 50, 34), (610, 235, 26), (300, 560, 32),
             (860, 40, 36), (870, 260, 30), (790, 420, 34), (860, 520, 40), (680, 560, 0), (240, 30, 22)]
    for x, y, r in trees:
        if r == 0:
            continue
        if (x, y) == (380, 160) and "tree" in d:
            continue
        canopy(c, x, y, r)


def l9_swimmer(c, m):
    x, y = 160, 465
    flat(c, Ell(x - 16, y, 14, 7), (220, 245, 255, 0.7))
    piece(c, [Thick(x - 4, y - 14, x + 10, y - 18, 4), Thick(x - 4, y + 14, x + 10, y + 18, 4)], (240, 190, 160),
          shadow=(1, 2, 3, 0.3))
    piece(c, Ell(x - 6, y, 11, 7), (240, 90, 90), shadow=(1, 2, 3, 0.3))
    piece(c, Circ(x + 9, y, 6.5), (250, 210, 80), shadow=(1, 2, 3, 0.3))


def l9_spray(c, m):
    fx, fy = FOUNTAIN
    for k in range(8):
        a = math.radians(k * 45)
        for j, (r, s) in enumerate(((14, 3.2), (22, 2.6), (29, 2.0))):
            b = a + j * 0.18
            flat(c, Circ(fx + r * math.cos(b), fy + r * math.sin(b), s), (235, 248, 255))
    piece(c, Circ(fx, fy, 6), (225, 245, 255), shadow=None)


def l9_boat(c, m):
    x, y = RIVER_X, 470
    piece(c, [Ell(x, y, 11, 26), Poly([(x - 9, y - 18), (x, y - 36), (x + 9, y - 18)])], (200, 120, 70), border=2, shadow=LOW)
    flat(c, Ell(x, y + 2, 7, 18), (225, 165, 105))
    flat(c, [Thick(x - 7, y - 4, x + 7, y - 4, 2.5), Thick(x - 7, y + 10, x + 7, y + 10, 2.5)], (150, 90, 55))
    piece(c, [Thick(x - 20, y + 2, x + 20, y + 6, 2.5)], (150, 100, 70), shadow=(1, 2, 3, 0.3))


def l9_balloon(c, m):
    x, y, r = 520, 440, 34
    gores = [Poly([(x, y), (x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))),
                   (x + r * math.cos(math.radians(a + 30)), y + r * math.sin(math.radians(a + 30)))]) for a in range(0, 360, 30)]
    piece(c, Circ(x, y, r), (240, 95, 90), border=2.5, shadow=None)
    for i, g in enumerate(gores):
        if i % 2:
            flat(c, g, (255, 220, 110))
    flat(c, Circ(x, y, r * 0.28), (250, 248, 240))
    flat(c, Circ(x - 9, y - 10, 6), (255, 255, 255, 0.45))


def l9_balloon_shadow(c, m):
    c.ellipse(575, 520, 30, 28, (35, 45, 55, 0.24))


def l9_bird(x, y):
    """Seagull seen from above, flying towards +x."""
    def d(c, m):
        wings = [Poly([(x - 2, y - 1), (x - 8, y - 15), (x - 3, y - 17), (x + 4, y - 2)]),
                 Poly([(x - 2, y + 1), (x - 8, y + 15), (x - 3, y + 17), (x + 4, y + 2)])]
        piece(c, wings + [Ell(x, y, 9, 3.2)], (250, 250, 246), shadow=(14, 20, 5, 0.2))
        flat(c, [Poly([(x - 8, y - 15), (x - 3, y - 17), (x - 5, y - 12)]), Poly([(x - 8, y + 15), (x - 3, y + 17), (x - 5, y + 12)])],
             (70, 70, 85))
        flat(c, Poly([(x + 9, y - 1), (x + 13, y), (x + 9, y + 1)]), (240, 170, 60))
    return d


BALLOON_MOVE = dict(bobAmplitude=(10, 6), bobSpeed=0.08)
L9_ELEMENTS = [
    E("boat", l9_boat, pivot=(RIVER_X, 470), anim=dict(swingAngle=10, swingSpeed=0.12, bobAmplitude=(3, 6), bobSpeed=0.15)),
    E("swimmer", l9_swimmer, pivot=(160, 465),
      anim=dict(bobAmplitude=(48, 0), bobSpeed=0.08, spinSpeed=0.08, spinSnap=0.85), animB={}),
    E("spray", l9_spray, pivot=FOUNTAIN, anim=dict(rotateSpeed=45, pulse=0.08, scaleSpeed=0.8),
      animB=dict(rotateSpeed=-45, pulse=0.08, scaleSpeed=0.8)),
    # traffic: two lanes each way, cars loop across the picture
    E("car_e", lambda c, m: car(c, 200, ROAD_Y + 14, "R", (230, 80, 80)), anim=drift_line(180, 220, W, 55, sign=1)),
    E("car_w", lambda c, m: car(c, 600, ROAD_Y - 14, "L", (80, 140, 220)), anim=drift_line(580, 620, W, 45, sign=-1)),
    E("car_s", lambda c, m: car(c, ROAD_X - 14, 120, "D", (250, 200, 70)), anim=drift_line(100, 140, H, 40, axis="y", sign=1)),
    E("car_n", lambda c, m: car(c, ROAD_X + 14, 480, "U", (120, 190, 120)), anim=drift_line(460, 500, H, 50, axis="y", sign=-1)),
    E("balloon_shadow", l9_balloon_shadow, anim=dict(BALLOON_MOVE, pulse=-0.08, scaleSpeed=0.12, twinkle=0.4, twinkleSpeed=0.12)),
    E("balloon", l9_balloon, pivot=(520, 440), anim=dict(BALLOON_MOVE, pulse=0.08, scaleSpeed=0.12, rotateSpeed=6)),
] + [
    E("bird%d" % i, l9_bird(x, y), pivot=(x, y),
      anim=dict(drift_line(x - 8, x + 6, W, 30, sign=1), stretch=(0, 0.5), scaleSpeed=2.4 + 0.3 * i,
                bobAmplitude=(0, 8), bobSpeed=0.2, phase=0.3))
    for i, (x, y) in enumerate(((150, 250), (170, 238), (168, 264)))
] + [
    E("cloudshadow1", cloud_shadow(120, 420, 1.7), anim=drift_line(60, 330, W, 12, sign=1)),
    E("cloudshadow2", cloud_shadow(560, 60, 1.4), anim=dict(drift_line(510, 720, W, 9, sign=1), phase=0.5)),
]

L9_DIFFS = [
    ("roof", 205, 105, 40),
    ("crosswalk", ROAD_X + 48, ROAD_Y, 30),
    ("umbrella", 270, 410, 36),
    ("swimmer", 160, 465, 62),
    ("fountain", FOUNTAIN[0], FOUNTAIN[1], 40),
    ("parkedcar", 548, 541, 24),
    ("tree", 380, 160, 32),
]


LEVELS = [
    ("Level08", "纸艺野餐", l8_background, L8_ELEMENTS, L8_DIFFS, 130, OPTS),
    ("Level09", "纸艺小镇", l9_background, L9_ELEMENTS, L9_DIFFS, 140, OPTS),
]
