# -*- coding: utf-8 -*-
"""
Paper-craft levels with a changing weather cycle (see weather.py / WeatherCycle):
  Level16 纸艺田园 - side view farm:        clear -> overcast -> rain -> thunderstorm -> rain -> overcast
  Level17 纸艺山村 - isometric mountain:    clear -> overcast -> snow (ground turns white) -> fog -> overcast
  Level18 纸艺海滩 - top-down beach:        heat wave -> clear -> overcast -> rain -> overcast -> clear
"""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, HEAT, OVERCAST, RAIN, SNOW, THUNDER, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, hill_y, paper_post, piece, soft_union, star_pts
from levels_views import ISO_SH, P, THICK, iso_box, iso_cyl, iso_quad, iso_roof
from weather import (CLOUDY, STORM, SUNNY, WET, cloud, flash, fog_layer, heat_haze, lightning, paper_sun, puddles,
                     rain_layer, snow_layer, sparkles, splash_rings, sun_glare)

INK = (70, 55, 65)
PROP = (2, 4, 7, 0.42)
LAYER = (1, 3, 11, 0.36)
SMALL = (1, 2, 3, 0.3)


def drift_across(x_left, x_right, speed):
    s_min = -(x_right + 10)
    length = W + 10 - x_left - s_min
    return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min, phase=(-s_min / length) % 1.0)


def opts(steps, blend=3.0, **extra):
    total = sum(d for _, d in steps)
    return dict(post=paper_post, weather=dict(steps=steps, blend=blend, **extra), anim_seconds=total,
                frames=int(total * 2))


# =================================================================== Level 16 (farm, side view)
H16 = [
    (300, [(14, 0.010, 0.5), (6, 0.03, 1.0)], (165, 205, 160)),
    (345, [(16, 0.009, 2.0), (7, 0.027, 0.3)], (128, 186, 112)),
    (405, [(8, 0.006, 1.0), (4, 0.02, 0.2)], (214, 188, 104)),
    (478, [(10, 0.012, 3.0), (5, 0.03, 1.4)], (112, 170, 88)),
]


def g16(layer, x):
    top, waves, _ = H16[layer]
    return hill_y(top, waves, x)


BARN_X = 620
BARN_B = g16(2, BARN_X) + 10
COW_X = 440
COW_B = g16(2, COW_X) + 14
SCARE_X = 300
SCARE_B = g16(2, SCARE_X) + 8
MILL_X = 840
MILL_B = g16(1, MILL_X) + 8
MILL_HUB = (MILL_X, MILL_B - 96)
CHICK_X = 300
CHICK_B = g16(3, CHICK_X) + 22
APPLE_TREE = (380, g16(1, 380) + 6)


def l16_background(c, d):
    """纸艺田园 - static part"""
    c.rect(0, 0, W, 660, (176, 214, 238))
    fill_levels.back_Level16(c, d)
    for li, (top, waves, col) in enumerate(H16):
        piece(c, hill_strip(top, waves), col, shadow=LAYER)
        if li == 0:
            for x in range(40, 900, 90):
                y = g16(0, x) + 4
                piece(c, [Thick(x, y, x, y - 14, 3), Circ(x, y - 22, 12)], (130, 180, 130), shadow=SMALL)
        elif li == 1:
            # farmhouse
            b = g16(1, 230) + 8
            piece(c, RRect(195, b - 44, 265, b, 2), (250, 236, 210), border=2, shadow=PROP)
            piece(c, Poly([(186, b - 42), (274, b - 42), (230, b - 74)]), (90, 120, 190), border=2, shadow=PROP)
            flat(c, [RRect(205, b - 32, 221, b - 18, 1), RRect(240, b - 32, 256, b - 18, 1)], (255, 222, 140))
            flat(c, RRect(224, b - 24, 236, b, 1), (130, 85, 70))
            # trees (the apples on one of them are missing in B)
            for x in (90, APPLE_TREE[0], 520):
                y = g16(1, x) + 6
                piece(c, [Thick(x, y, x, y - 30, 7), Circ(x, y - 50, 26), Circ(x - 18, y - 38, 17), Circ(x + 18, y - 38, 17)],
                      (90, 165, 90), shadow=PROP)
                flat(c, Thick(x, y, x, y - 24, 7), (135, 92, 66))
                if x == APPLE_TREE[0] and "apples" not in d:
                    for dx, dy in ((-12, -52), (8, -60), (14, -40), (-20, -36)):
                        piece(c, Circ(x + dx, y + dy, 5), (225, 55, 60), shadow=SMALL)
            # windmill tower
            piece(c, Poly([(MILL_X - 18, MILL_B), (MILL_X + 18, MILL_B), (MILL_X + 9, MILL_HUB[1] + 4), (MILL_X - 9, MILL_HUB[1] + 4)]),
                  (240, 230, 210), border=2, shadow=PROP)
            flat(c, RRect(MILL_X - 6, MILL_B - 22, MILL_X + 6, MILL_B, 2), (140, 95, 70))
        elif li == 2:
            for k in range(6):
                pts = [(x, g16(2, x) + 12 + k * 13) for x in range(-20, 940, 30)]
                flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 2) for i in range(len(pts) - 1)],
                     (195, 168, 86))
            # barn + silo
            b = BARN_B
            piece(c, [RRect(690, b - 110, 722, b, 2), Ell(706, b - 110, 16, 12)], (200, 200, 210), border=2, shadow=PROP)
            for y in range(int(b - 100), int(b), 16):
                flat(c, Thick(692, y, 720, y, 1.4), (175, 175, 190))
            piece(c, RRect(BARN_X - 60, b - 76, BARN_X + 60, b, 2), (200, 70, 60), border=2.5, shadow=PROP)
            piece(c, Poly([(BARN_X - 68, b - 74), (BARN_X - 40, b - 108), (BARN_X + 40, b - 108), (BARN_X + 68, b - 74)]),
                  (150, 50, 50), border=2.5, shadow=PROP)
            door = (90, 150, 100) if "door" in d else (150, 85, 62)
            flat(c, RRect(BARN_X - 20, b - 46, BARN_X + 20, b, 1), door)
            flat(c, [Thick(BARN_X - 20, b - 46, BARN_X + 20, b, 2.5), Thick(BARN_X + 20, b - 46, BARN_X - 20, b, 2.5),
                     Thick(BARN_X - 21, b - 46, BARN_X + 21, b - 46, 3)], (250, 245, 235))
            flat(c, RRect(BARN_X - 10, b - 68, BARN_X + 10, b - 54, 1), (255, 228, 150))
            # cow (3 spots in A, 2 in B)
            cb = COW_B
            piece(c, [RRect(COW_X - 24, cb - 28, COW_X + 22, cb - 10, 7), Thick(COW_X - 18, cb - 12, COW_X - 18, cb, 3),
                      Thick(COW_X + 16, cb - 12, COW_X + 16, cb, 3), Ell(COW_X + 30, cb - 26, 10, 8),
                      Thick(COW_X - 24, cb - 24, COW_X - 30, cb - 10, 2)], (252, 250, 245), border=1.5, shadow=PROP)
            spots = [(COW_X - 12, cb - 22, 6), (COW_X + 6, cb - 18, 5), (COW_X + 14, cb - 24, 4)]
            if "spots" in d:
                spots = spots[:2]
            flat(c, [Ell(x, y, r, r * 0.8) for x, y, r in spots], (60, 55, 65))
            flat(c, [Ell(COW_X + 37, cb - 24, 4, 3)], (245, 170, 170))
            flat(c, Circ(COW_X + 30, cb - 29, 1.4), INK)
            # scarecrow pole (the hat/head is an element)
            piece(c, [Thick(SCARE_X, SCARE_B, SCARE_X, SCARE_B - 60, 4), Thick(SCARE_X - 24, SCARE_B - 44, SCARE_X + 24, SCARE_B - 44, 4)],
                  (150, 105, 70), shadow=PROP)
            piece(c, Poly([(SCARE_X - 14, SCARE_B - 48), (SCARE_X + 14, SCARE_B - 48), (SCARE_X + 10, SCARE_B - 20),
                           (SCARE_X - 10, SCARE_B - 20)]), (110, 150, 200), border=1.5, shadow=PROP)
        elif li == 3:
            # pond, fence, flowers
            piece(c, Ell(130, 528, 92, 22), (110, 170, 215), border=3, border_col=(150, 120, 90), shadow=SMALL)
            flat(c, Ell(110, 524, 30, 5), (170, 210, 235))
            for x in range(330, 910, 30):
                y = g16(3, x) + 4
                piece(c, Poly([(x - 4, y + 12), (x - 4, y - 22), (x, y - 27), (x + 4, y - 22), (x + 4, y + 12)]), (245, 238, 220),
                      shadow=SMALL)
            pts = [(x, g16(3, x) - 10) for x in range(326, 910, 30)]
            flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 2.5) for i in range(len(pts) - 1)], (232, 222, 200))
            for x, y, col in ((60, 570, (255, 120, 160)), (220, 580, (255, 220, 90)), (820, 568, (255, 120, 160))):
                if x == 820 and "flower" in d:
                    col = (150, 120, 250)
                piece(c, [Thick(x, y + 14, x, y, 2.5)] + [Circ(x + 6 * math.cos(math.radians(a)), y + 6 * math.sin(math.radians(a)), 4.5)
                                                          for a in range(0, 360, 72)], col, shadow=SMALL)
                flat(c, Circ(x, y, 3), (255, 230, 120))
    fill_levels.front_Level16(c, d)


def l16_blades(c, m):
    x, y = MILL_HUB
    for k in range(4):
        a = math.radians(45 + k * 90)
        ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        piece(c, Poly([(x + ux * 6, y + uy * 6), (x + ux * 46, y + uy * 46), (x + ux * 46 + vx * 12, y + uy * 46 + vy * 12),
                       (x + ux * 10 + vx * 8, y + uy * 10 + vy * 8)]), (250, 246, 236), border=1.5, shadow=SMALL)
    piece(c, Circ(x, y, 5), (140, 95, 70), shadow=None)


def l16_scare_head(c, m):
    x, b = SCARE_X, SCARE_B
    piece(c, Circ(x, b - 66, 10), (240, 210, 160), border=1.5, shadow=SMALL)
    hat = (90, 130, 210) if m else (230, 190, 90)
    piece(c, [RRect(x - 18, b - 76, x + 18, b - 72, 2), Poly([(x - 9, b - 74), (x + 9, b - 74), (x + 5, b - 92), (x - 5, b - 92)])],
          hat, border=1.5, shadow=SMALL)
    flat(c, [Circ(x - 4, b - 67, 1.4), Circ(x + 4, b - 67, 1.4), Thick(x - 4, b - 61, x + 4, b - 61, 1.2)], INK)


def l16_chicken(c, m):
    x, b = CHICK_X, CHICK_B
    piece(c, [Ell(x, b - 12, 13, 10), Circ(x + 10, b - 22, 7), Poly([(x - 10, b - 14), (x - 20, b - 24), (x - 14, b - 10)])],
          (252, 250, 245), border=1.5, shadow=SMALL)
    flat(c, [Poly([(x + 16, b - 23), (x + 22, b - 21), (x + 16, b - 19)])], (245, 160, 50))
    flat(c, [Ell(x + 9, b - 30, 3, 3)], (230, 60, 60))
    flat(c, [Thick(x - 3, b - 3, x - 4, b + 4, 1.6), Thick(x + 3, b - 3, x + 4, b + 4, 1.6)], (245, 160, 50))
    flat(c, Circ(x + 12, b - 23, 1.2), INK)


def l16_bird(x, y, s):
    def d(c, m):
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.25), Thick(x, y, x + s, y - s * 0.4, s * 0.25)], (90, 95, 110),
              shadow=(1, 3, 4, 0.25))
    return d


STEPS16 = [(CLEAR, 12), (OVERCAST, 7), (RAIN, 10), (THUNDER, 10), (RAIN, 6), (OVERCAST, 6)]
GRAY, DARK = (168, 172, 186), (108, 112, 132)

L16_ELEMENTS = [
    sun_glare("glare", 130, 80, 160, mask=W_(CLEAR)),
    paper_sun("sun", 130, 80),
    cloud("cloud_w1", 330, 70, 0.8, (252, 252, 248), W_(CLEAR), anim=drift_across(285, 395, 8)),
    cloud("cloud_w2", 690, 110, 0.6, (252, 252, 248), W_(CLEAR), anim=drift_across(655, 740, 6)),
] + [
    cloud("cloud_g%d" % i, x, y, k, GRAY, CLOUDY) for i, (x, y, k) in enumerate(((90, 60, 1.4), (300, 40, 1.6), (520, 70, 1.5),
                                                                                 (740, 45, 1.5), (880, 90, 1.1)))
] + [
    cloud("cloud_d%d" % i, x, y, k, DARK, STORM) for i, (x, y, k) in enumerate(((160, 90, 1.5), (420, 80, 1.7), (690, 95, 1.6)))
] + [
    lightning("bolt1", 420, 115, 300, interval=4.3, phase=0.1, seed=3),
    lightning("bolt2", 700, 120, 320, interval=6.1, phase=0.55, seed=8),
] + [
    E("bird%d" % i, l16_bird(x, y, 9), pivot=(x, y), weather=W_(CLEAR, OVERCAST),
      anim=dict(drift_across(x - 12, x + 12, 20), stretch=(0, 0.5), scaleSpeed=2.2 + 0.3 * i, bobAmplitude=(0, 6), bobSpeed=0.2))
    for i, (x, y) in enumerate(((560, 150), (585, 140), (575, 165)))
] + [
    # the windmill turns the other way in B; the chicken only pecks in A
    E("windmill", l16_blades, pivot=MILL_HUB, anim=dict(rotateSpeed=-90), animB=dict(rotateSpeed=90)),
    E("scarecrow", l16_scare_head, pivot=(SCARE_X, SCARE_B - 60), variant=True, anim=dict(swingAngle=6, swingSpeed=0.35)),
    E("chicken", l16_chicken, pivot=(CHICK_X + 4, CHICK_B), anim=dict(swingAngle=22, swingSpeed=0.6), animB={}),
    puddles("puddles", [Ell(400, 545, 42, 7), Ell(600, 560, 55, 8), Ell(770, 538, 36, 6)]),
] + splash_rings("splash", [(110, 524, 12), (150, 530, 10), (90, 532, 9), (400, 545, 9), (600, 558, 10)]) + [
    rain_layer("rain", 16, 70, 24, 1.3, 0.75, 240),
    rain_layer("rain_heavy", 61, 80, 34, 1.6, 0.8, 360, mask=STORM),
    flash("flash1", 4.3, 0.1),
    flash("flash2", 6.1, 0.55),
]

L16_DIFFS = [
    ("door", BARN_X, int(BARN_B - 22), 26),
    ("windmill", MILL_HUB[0], int(MILL_HUB[1]), 44),
    ("spots", COW_X, int(COW_B - 20), 24),
    ("hat", SCARE_X, int(SCARE_B - 82), 20),
    ("apples", APPLE_TREE[0], int(APPLE_TREE[1] - 46), 28),
    ("chicken", CHICK_X + 2, int(CHICK_B - 14), 26),
    ("flower", 820, 570, 18),
]


# =================================================================== Level 17 (isometric mountain village)
def roof_polys(X, Y, Z, dx, dy, h):
    m = Y + dy / 2
    back = Poly([P(X, Y, Z), P(X + dx, Y, Z), P(X + dx, m, Z + h), P(X, m, Z + h)])
    front = Poly([P(X, m, Z + h), P(X + dx, m, Z + h), P(X + dx, Y + dy, Z), P(X, Y + dy, Z)])
    gable = Poly([P(X + dx, Y, Z), P(X + dx, Y + dy, Z), P(X + dx, m, Z + h)])
    return [back, front, gable]


def house17(c, X, Y, dx, dy, dz, wall, roof, door=(130, 85, 70), chimney=True):
    iso_box(c, X, Y, 0, dx, dy, dz, wall)
    flat(c, Poly([P(X + dx * 0.4, Y + dy, 0), P(X + dx * 0.6, Y + dy, 0), P(X + dx * 0.6, Y + dy, dz * 0.62),
                  P(X + dx * 0.4, Y + dy, dz * 0.62)]), door)
    for wx in (X + dx * 0.12, X + dx * 0.72):
        flat(c, Poly([P(wx, Y + dy, dz * 0.42), P(wx + dx * 0.16, Y + dy, dz * 0.42), P(wx + dx * 0.16, Y + dy, dz * 0.76),
                      P(wx, Y + dy, dz * 0.76)]), (255, 222, 140))
    if chimney:
        iso_box(c, X + dx * 0.7, Y + dy * 0.2, dz, 0.3, 0.3, 0.75, (170, 95, 80), border=1.5)
    iso_roof(c, X - 0.1, Y - 0.1, dz, dx + 0.2, dy + 0.2, 0.6, roof)


def pine17(c, X, Y, s=1.0, col=(70, 140, 95)):
    cx, cy = P(X, Y)
    soft_union(c, [Ell(cx + 18 * s, cy + 4, 22 * s, 9 * s)], (60, 80, 60), 0.25, spread=6)
    piece(c, Thick(cx, cy, cx, cy - 12 * s, 6 * s), (130, 90, 65), shadow=ISO_SH)
    piece(c, pine_tiers(X, Y, s), col, border=1.5, shadow=ISO_SH)


def pine_tiers(X, Y, s):
    cx, cy = P(X, Y)
    out = []
    for k in range(3):
        top = cy - 70 * s + k * 16 * s
        w = (16 + k * 7) * s
        out.append(Poly([(cx, top), (cx - w, top + 30 * s), (cx + w, top + 30 * s)]))
    return out


def pine_caps(X, Y, s):
    cx, cy = P(X, Y)
    out = []
    for k in range(3):
        top = cy - 70 * s + k * 16 * s
        w = (16 + k * 7) * s
        out.append(Poly([(cx, top - 1), (cx - w * 0.62, top + 16 * s), (cx, top + 11 * s), (cx + w * 0.62, top + 16 * s)]))
    return out


H17 = [(1.3, 1.4, 1.6, 1.2, 1.0), (3.8, 0.8, 1.4, 1.2, 1.1), (7.3, 1.1, 1.6, 1.3, 1.0)]


def l17_decor(c, X, Y, r):
    if r < 0.7:
        pine17(c, X, Y, 0.75 + 0.4 * r)
    else:
        x, y = P(X, Y)
        piece(c, [Ell(x, y - 8, 16, 11)], (150, 150, 158), shadow=ISO_SH)


def _l17_surround():
    from fill_iso import surround_points
    return surround_points(17, step=60, keep=0.9)


L17_SURROUND = _l17_surround()
PINES17 = [(0.6, 0.5, 1.0), (2.9, 0.4, 0.9), (9.2, 0.6, 1.0), (0.5, 4.6, 1.1), (9.3, 3.8, 0.9), (1.6, 8.6, 1.0),
           (8.8, 8.8, 1.1), (9.3, 5.9, 0.8)]
LAKE = (6.6, 6.4)
FLAGPOLE = (5.2, 2.6)
WELL = (2.6, 6.2)


def l17_background(c, d):
    """纸艺山村 - static part"""
    c.rect(0, 0, W, 660, (186, 212, 236))
    # mountains behind the paper base
    for pts, col in (([(60, 360), (260, 110), (330, 160), (470, 30), (600, 150), (690, 100), (860, 360)], (150, 160, 192)),
                     ([(180, 360), (360, 170), (470, 230), (620, 160), (760, 360)], (128, 140, 176))):
        piece(c, Poly(pts), col, shadow=LAYER)
    for px, py, w in ((260, 110, 34), (470, 30, 46), (690, 100, 32)):
        flat(c, Poly([(px, py), (px - w, py + w * 1.1), (px - w * 0.4, py + w * 0.8), (px, py + w * 1.05),
                      (px + w * 0.45, py + w * 0.8), (px + w, py + w * 1.1)]), (250, 252, 255))
    # the valley fills the picture: village in the middle, pine forest all around
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (140, 190, 112), None)
    flat(c, iso_quad(-0.2, -0.2, 10.2, 10.2), (150, 198, 118))
    for q in (iso_quad(4.4, 10, 5.4, 26), iso_quad(-16, 3.2, 1.0, 4.0), iso_quad(9.0, 3.2, 26, 4.0)):
        piece(c, q, (222, 206, 170), shadow=(1, 2, 3, 0.2))
    draw_surround(c, L17_SURROUND, l17_decor, "back")
    for q in (iso_quad(4.4, 2.4, 5.4, 10), iso_quad(1.0, 3.2, 9.0, 4.0)):
        piece(c, q, (222, 206, 170), shadow=(1, 2, 3, 0.2))
    # lake with a little dock
    cx, cy = P(*LAKE)
    ex = 1.6 * 36 * math.sqrt(2)
    piece(c, Ell(cx, cy, ex, ex / 2), (110, 175, 215), border=3, border_col=(205, 185, 140), shadow=SMALL)
    flat(c, Ell(cx - 20, cy - 8, ex * 0.4, ex * 0.12), (150, 200, 230))
    iso_box(c, 5.0, 6.2, 0.05, 0.9, 0.35, 0.08, (180, 135, 95), border=1.5)
    # houses (middle roof colour differs, door of the right house differs)
    house17(c, *H17[0], (240, 226, 200), (200, 80, 70))
    house17(c, *H17[1], (245, 236, 216), (100, 170, 110) if "roof" in d else (90, 130, 200))
    house17(c, *H17[2], (236, 220, 196), (160, 110, 80), door=(90, 150, 210) if "door" in d else (130, 85, 70),
            chimney=False)
    # flag pole
    fx, fy = P(*FLAGPOLE)
    piece(c, Thick(fx, fy, fx, fy - 70, 3), (120, 110, 115), shadow=ISO_SH)
    # well (missing in B)
    if "well" not in d:
        wx, wy, ex, ey = iso_cyl(c, WELL[0], WELL[1], 0, 0.45, 0.42, (175, 170, 180))
        flat(c, Ell(wx, wy, ex * 0.7, ey * 0.7), (60, 70, 90))
        for dxp in (-ex * 0.8, ex * 0.8):
            piece(c, Thick(wx + dxp, wy, wx + dxp, wy - 34, 3), (140, 95, 70), shadow=SMALL)
        piece(c, Poly([(wx - ex - 6, wy - 32), (wx + ex + 6, wy - 32), (wx, wy - 50)]), (180, 80, 70), border=1.5, shadow=SMALL)
    # pines (one missing in B)
    for X, Y, s in PINES17:
        if (X, Y) == (9.3, 5.9) and "pine" in d:
            continue
        pine17(c, X, Y, s)
    # lamps
    for X, Y in ((4.2, 3.0), (5.8, 5.2)):
        lx, ly = P(X, Y)
        piece(c, Thick(lx, ly, lx, ly - 46, 3), (70, 70, 85), shadow=ISO_SH)
        piece(c, Circ(lx, ly - 50, 6), (255, 230, 140), border=1.5, shadow=None)
    from fill_iso import draw_surround
    draw_surround(c, L17_SURROUND, l17_decor, "front")


def l17_snow_cover(c, m):
    white = (252, 253, 255)
    shapes = []
    for X, Y, dx, dy, dz in H17:
        shapes += roof_polys(X - 0.1, Y - 0.1, dz, dx + 0.2, dy + 0.2, 0.6)[:2]
    for X, Y, s in PINES17:
        if m and (X, Y) == (9.3, 5.9):      # this tree is missing in the modified picture
            continue
        shapes += pine_caps(X, Y, s)
    for X, Y, r in L17_SURROUND:
        if r < 0.7:
            shapes += pine_caps(X, Y, 0.75 + 0.4 * r)
        else:
            x, y = P(X, Y)
            shapes.append(Ell(x - 2, y - 14, 14, 6))
    for X, Y, r in L17_SURROUND[::3]:
        x, y = P(X, Y)
        shapes.append(Ell(x + 20, y + 8, 30, 10))
    rnd = random.Random(17)
    for X, Y, rx, ry in ((2.2, 2.8, 50, 18), (6.4, 3.6, 60, 20), (3.4, 5.2, 46, 16), (8.0, 5.6, 40, 15), (2.0, 7.4, 44, 16),
                         (7.4, 8.4, 50, 18), (4.6, 8.8, 36, 13), (8.6, 2.6, 30, 12), (1.0, 5.6, 34, 12), (6.0, 9.2, 30, 11)):
        x, y = P(X, Y)
        for _ in range(7):     # drift = cluster of flattened blobs, irregular outline
            bx, by = x + rnd.uniform(-rx, rx) * 0.7, y + rnd.uniform(-ry, ry) * 0.6
            shapes.append(Ell(bx, by, rx * rnd.uniform(0.35, 0.6), ry * rnd.uniform(0.4, 0.7)))
    soft_union(c, shapes, white, 0.9, spread=3)
    cx, cy = P(*LAKE)
    ex = 1.6 * 36 * math.sqrt(2)
    c.ellipse(cx, cy, ex - 4, ex / 2 - 3, (225, 238, 250, 0.7))


def l17_flag(c, m):
    fx, fy = P(*FLAGPOLE)
    col = (60, 170, 110) if m else (230, 80, 80)
    piece(c, Poly([(fx + 1, fy - 70), (fx + 30, fy - 63), (fx + 1, fy - 55)]), col, border=1.2, shadow=SMALL)


def l17_boat(c, m):
    x, y = P(6.9, 6.7)
    piece(c, Poly([(x - 18, y - 4), (x + 18, y - 4), (x + 12, y + 6), (x - 12, y + 6)]), (200, 110, 75), border=1.5, shadow=SMALL)
    flat(c, Thick(x, y - 4, x, y - 30, 1.6), (110, 85, 70))
    piece(c, Poly([(x + 1, y - 30), (x + 1, y - 7), (x + 16, y - 7)]), (250, 248, 240), border=1.2, shadow=SMALL)


def l17_smoke(X, Y, Z):
    x, y = P(X, Y, Z)

    def d(c, m):
        piece(c, Circ(x, y, 7), (240, 238, 236), shadow=SMALL)
    return d


def l17_bird(x, y, s):
    def d(c, m):
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.25), Thick(x, y, x + s, y - s * 0.4, s * 0.25)], (90, 95, 110),
              shadow=(1, 3, 4, 0.25))
    return d


STEPS17 = [(CLEAR, 10), (OVERCAST, 6), (SNOW, 14), (FOG, 10), (OVERCAST, 5)]
GREY17 = (200, 205, 216)
_h1 = H17[0]
SMOKE1 = (_h1[0] + _h1[2] * 0.85, _h1[1] + _h1[3] * 0.35, _h1[4] + 0.85)
_h2 = H17[1]
SMOKE2 = (_h2[0] + _h2[2] * 0.85, _h2[1] + _h2[3] * 0.35, _h2[4] + 0.85)

L17_ELEMENTS = [
    cloud("cloud_w1", 160, 70, 0.8, (252, 252, 248), W_(CLEAR), anim=drift_across(115, 225, 7)),
    cloud("cloud_w2", 640, 40, 0.6, (252, 252, 248), W_(CLEAR), anim=drift_across(605, 690, 5)),
] + [
    cloud("cloud_g%d" % i, x, y, k, GREY17, W_(OVERCAST, SNOW, FOG)) for i, (x, y, k) in
    enumerate(((90, 50, 1.3), (300, 30, 1.5), (560, 55, 1.4), (790, 40, 1.4)))
] + [
    E("bird%d" % i, l17_bird(x, y, 8), pivot=(x, y), weather=W_(CLEAR),
      anim=dict(drift_across(x - 10, x + 10, 18), stretch=(0, 0.5), scaleSpeed=2.4 + 0.3 * i, bobAmplitude=(0, 5), bobSpeed=0.2))
    for i, (x, y) in enumerate(((200, 160), (222, 150), (215, 174)))
] + [
    E("smoke%d" % i, l17_smoke(*SMOKE1), show="A",
      anim=dict(driftVelocity=(5, 20), driftLength=60, driftFade=True, driftGrow=1.2, phase=i / 3)) for i in range(3)
] + [
    E("smoke2_%d" % i, l17_smoke(*SMOKE2),
      anim=dict(driftVelocity=(5, 20), driftLength=60, driftFade=True, driftGrow=1.2, phase=i / 3 + 0.15)) for i in range(3)
] + [
    E("flag", l17_flag, variant=True, pivot=(P(*FLAGPOLE)[0], P(*FLAGPOLE)[1] - 63),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.5, swingAngle=4, swingSpeed=1.1)),
    E("boat", l17_boat, show="A", pivot=P(6.9, 6.7), anim=dict(bobAmplitude=(6, 2), bobSpeed=0.12, swingAngle=6, swingSpeed=0.3)),
    # snow settles on roofs, trees, ground and the lake while it snows, and melts away afterwards
    E("snow_cover", l17_snow_cover, variant=True, daynight="untinted", weather=W_(SNOW)),
    snow_layer("snow_far", 5, 80, 1.0, 2.0, 16),
    snow_layer("snow_near", 9, 32, 2.4, 4.0, 32, sway=12),
    fog_layer("fog1", 3, 180, 330, 0.55, 10, 1),
    fog_layer("fog2", 7, 330, 520, 0.6, 14, -1),
]

L17_DIFFS = [
    ("smoke", int(P(*SMOKE1)[0] + 6), int(P(*SMOKE1)[1] - 24), 28),
    ("boat", int(P(6.9, 6.7)[0]), int(P(6.9, 6.7)[1] - 12), 26),
    ("flag", int(P(*FLAGPOLE)[0] + 14), int(P(*FLAGPOLE)[1] - 63), 20),
    ("roof", int(P(_h2[0] + _h2[2] / 2, _h2[1] + _h2[3] / 2, _h2[4] + 0.3)[0]), int(P(_h2[0] + _h2[2] / 2, _h2[1] + _h2[3] / 2, _h2[4] + 0.3)[1]), 0),
    ("door", int(P(H17[2][0] + H17[2][2] * 0.5, H17[2][1] + H17[2][3], 0.3)[0]), int(P(H17[2][0] + H17[2][2] * 0.5, H17[2][1] + H17[2][3], 0.3)[1]), 0),
    ("pine", int(P(9.3, 5.9)[0]), int(P(9.3, 5.9)[1] - 36), 0),
    ("well", int(P(*WELL)[0]), int(P(*WELL)[1] - 22), 0),
]


# =================================================================== Level 18 (top-down beach)
def shore_x(y):
    return 560 + 22 * math.sin(y * 0.018) + 10 * math.sin(y * 0.05 + 1)


def l18_background(c, d):
    """纸艺海滩 - static part (seen from above)"""
    c.rect(0, 0, W, 660, (242, 222, 172))
    rnd = random.Random(18)
    for _ in range(140):
        x, y = rnd.uniform(0, 540), rnd.uniform(0, 600)
        flat(c, Circ(x, y, rnd.uniform(0.8, 1.8)), (225, 202, 150))
    # sea: shallow band then deeper paper layers
    ys = list(range(-20, 641, 12))
    piece(c, Poly([(shore_x(y), y) for y in ys] + [(940, 640), (940, -20)]), (125, 205, 222), shadow=(1, 3, 8, 0.25))
    piece(c, Poly([(shore_x(y) + 70 + 10 * math.sin(y * 0.03), y) for y in ys] + [(940, 640), (940, -20)]), (92, 175, 214),
          shadow=(1, 3, 8, 0.25))
    piece(c, Poly([(shore_x(y) + 190 + 14 * math.sin(y * 0.02 + 2), y) for y in ys] + [(940, 640), (940, -20)]), (70, 150, 202),
          shadow=(1, 3, 8, 0.25))
    # boardwalk
    piece(c, RRect(30, -20, 110, 620, 2), (195, 150, 105), border=2, shadow=PROP)
    for y in range(0, 600, 18):
        flat(c, Thick(32, y, 108, y, 1.4), (165, 122, 84))
    # palms (crowns cast long shadows)
    for x, y in ((180, 70), (470, 50)):
        soft_union(c, [Circ(x + 22, y + 30, 46)], (60, 50, 30), 0.25, spread=10)
        leaves = []
        for k in range(7):
            a = math.radians(k * 360 / 7 + 10)
            ex, ey = x + 52 * math.cos(a), y + 52 * math.sin(a)
            nx, ny = -math.sin(a) * 11, math.cos(a) * 11
            leaves.append(Poly([(x, y), ((x + ex) / 2 + nx, (y + ey) / 2 + ny), (ex, ey), ((x + ex) / 2 - nx, (y + ey) / 2 - ny)]))
        piece(c, leaves, (70, 160, 85), shadow=(6, 10, 8, 0.35))
        flat(c, [Thick(x, y, x + 46 * math.cos(math.radians(k * 360 / 7 + 10)), y + 46 * math.sin(math.radians(k * 360 / 7 + 10)), 1.6)
                 for k in range(7)], (110, 190, 110))
        for dx, dy in ((-5, -4), (5, -3), (0, 5)):
            piece(c, Circ(x + dx, y + dy, 5), (130, 85, 50), shadow=SMALL)
    # towels and umbrellas
    for (x, y, w, h, col, stripe, key) in ((230, 250, 96, 52, (90, 160, 230), (255, 255, 255), None),
                                          (440, 385, 100, 54, (255, 200, 80), (230, 90, 90), "towel")):
        if key == "towel" and "towel" in d:
            stripe = (90, 180, 120)
        piece(c, RRect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 3), col, border=2, shadow=(1, 2, 3, 0.3))
        for k in (-1, 1):
            flat(c, RRect(x - w / 2, y + k * h / 4 - 4, x + w / 2, y + k * h / 4 + 4, 1), stripe)
    for (x, y, col, key) in ((265, 205, (230, 80, 80), "umbrella"), (420, 335, (250, 200, 70), None)):
        if key == "umbrella" and "umbrella" in d:
            col = (80, 130, 220)
        tris = [Poly([(x, y), (x + 40 * math.cos(math.radians(a)), y + 40 * math.sin(math.radians(a))),
                      (x + 40 * math.cos(math.radians(a + 45)), y + 40 * math.sin(math.radians(a + 45)))]) for a in range(0, 360, 45)]
        piece(c, tris, (252, 250, 244), border=2, shadow=(8, 12, 9, 0.35))
        for i, t in enumerate(tris):
            if i % 2 == 0:
                flat(c, t, col)
        flat(c, Circ(x, y, 3.5), (120, 90, 75))
    # sand castle (flag missing in B)
    sx, sy = 330, 490
    for r, col in ((34, (222, 192, 130)), (24, (232, 204, 145)), (14, (240, 215, 158))):
        piece(c, RRect(sx - r, sy - r, sx + r, sy + r, 3), col, shadow=(3, 5, 5, 0.35))
    for dx, dy in ((-34, -34), (34, -34), (-34, 34), (34, 34)):
        piece(c, Circ(sx + dx, sy + dy, 9), (230, 200, 140), shadow=(3, 5, 5, 0.35))
    if "flag" not in d:
        piece(c, Poly([(sx, sy), (sx + 20, sy - 8), (sx, sy - 16)]), (230, 70, 70), border=1.2, shadow=(5, 8, 3, 0.35))
    # ball, bucket, starfish, shells
    if "ball" not in d:
        piece(c, Circ(180, 420, 18), (252, 250, 245), shadow=(3, 5, 5, 0.35))
        flat(c, [Ell(180, 420, 18, 7), Ell(180, 420, 6, 18)], (230, 80, 80))
        flat(c, Ell(180, 420, 18, 3), (80, 140, 220))
    piece(c, [Circ(270, 450, 14)], (80, 150, 220), border=2, shadow=(3, 5, 5, 0.35))
    flat(c, Circ(270, 450, 10), (60, 120, 190))
    if "starfish" not in d:
        piece(c, Poly(star_pts(500, 540, 16, 7)), (250, 140, 70), shadow=SMALL)
        flat(c, Circ(500, 540, 3), (255, 190, 120))
    for x, y in ((150, 560), (420, 470), (210, 330)):
        piece(c, Ell(x, y, 6, 5), (255, 225, 220), shadow=SMALL)


def l18_boat(c, m):
    x, y = 760, 250
    col = (90, 180, 120) if m else (230, 90, 80)
    piece(c, [Ell(x, y, 30, 12), Poly([(x + 26, y - 9), (x + 46, y), (x + 26, y + 9)])], col, border=2, shadow=(3, 5, 5, 0.35))
    flat(c, Ell(x + 2, y, 22, 7), (250, 240, 220))
    flat(c, [Thick(x - 8, y - 7, x - 8, y + 7, 2), Thick(x + 8, y - 7, x + 8, y + 7, 2)], (180, 130, 90))


def l18_ring(c, m):
    x, y = 660, 460
    piece(c, Circ(x, y, 16), (250, 120, 120), border=1.5, shadow=(3, 5, 4, 0.35))
    flat(c, Circ(x, y, 8), (125, 205, 222))
    for a in (0, 90, 180, 270):
        flat(c, Thick(x + 9 * math.cos(math.radians(a)), y + 9 * math.sin(math.radians(a)),
                      x + 16 * math.cos(math.radians(a)), y + 16 * math.sin(math.radians(a)), 4), (255, 255, 255))


def l18_crab(c, m):
    x, y = 400, 560
    for s in (-1, 1):
        for k in range(3):
            flat(c, Thick(x + s * 8, y - 4 + k * 4, x + s * 18, y - 8 + k * 7, 2), (200, 60, 50))
        piece(c, Circ(x + s * 16, y - 14, 5), (225, 75, 60), shadow=SMALL)
    piece(c, Ell(x, y, 12, 9), (230, 80, 65), shadow=SMALL)
    flat(c, [Circ(x - 4, y - 6, 1.6), Circ(x + 4, y - 6, 1.6)], INK)


def l18_foam(i, x_off, phase):
    def d(c, m):
        ys = list(range(-30, 650, 10))
        pts = [(shore_x(y) + x_off + 6 * math.sin(y * 0.06 + i), y) for y in ys]
        flat(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 2.4) for k in range(len(pts) - 1)], (250, 252, 255, 0.85))
    return E("foam%d" % i, d, anim=dict(bobAmplitude=(-12, 0), bobSpeed=0.12, twinkle=0.5, twinkleSpeed=0.12, phase=phase))


def cloud_shadow(eid, x, y, k, speed, mask=CLOUDY):
    def d(c, m):
        soft_union(c, [Circ(x + dx * k, y + dy * k, r * k) for dx, dy, r in
                       ((0, 0, 50), (55, -14, 58), (110, 6, 46), (50, 30, 44), (-44, 18, 34))], (40, 50, 60), 0.2, spread=16)
    return E(eid, d, anim=drift_across(x - 80 * k, x + 160 * k, speed), daynight="untinted", weather=mask)


STEPS18 = [(HEAT, 14), (CLEAR, 6), (OVERCAST, 6), (RAIN, 10), (OVERCAST, 5), (CLEAR, 5)]
SEA_SPARKLES = [(640, 90), (720, 160), (820, 120), (700, 330), (800, 380), (860, 260), (760, 520), (640, 560), (850, 560)]

L18_ELEMENTS = [
    l18_foam(0, 4, 0.0),
    l18_foam(1, 40, 0.5),
] + sparkles("sparkle", SEA_SPARKLES) + [
    E("boat", l18_boat, pivot=(760, 250), variant=True, anim=dict(bobAmplitude=(8, 4), bobSpeed=0.1, swingAngle=8, swingSpeed=0.2)),
    E("ring", l18_ring, pivot=(660, 460), anim=dict(bobAmplitude=(6, 6), bobSpeed=0.15, rotateSpeed=12)),
    E("crab", l18_crab, pivot=(400, 560), anim=dict(bobAmplitude=(40, 0), bobSpeed=0.1, swingAngle=8, swingSpeed=1.2), animB={}),
    puddles("wet_sand", [Ell(200, 300, 60, 26), Ell(380, 180, 50, 20), Ell(150, 520, 46, 20), Ell(470, 280, 40, 18)],
            col=(160, 140, 110), alpha=0.35),
] + splash_rings("ripple", [(620, 200, 10), (700, 420, 12), (820, 300, 11), (760, 560, 10), (680, 120, 9), (860, 470, 10),
                            (200, 300, 7), (380, 180, 6), (470, 300, 6)]) + [
    cloud_shadow("cloudshadow1", 180, 160, 1.6, 12),
    cloud_shadow("cloudshadow2", 600, 420, 1.4, 9),
    cloud_shadow("cloudshadow3", 380, 520, 1.2, 15),
    cloud("cloud_low1", 300, 90, 0.9, (238, 240, 245), CLOUDY, anim=drift_across(250, 380, 12), shadow=(16, 24, 14, 0.3)),
    rain_layer("rain", 42, 110, 12, 1.4, 0.75, 170, step=(24, 64)),
    sun_glare("glare", 40, 30, 300),
] + [heat_haze("haze%d" % i, y, phase=i * 0.3) for i, y in enumerate((130, 290, 450))]

L18_DIFFS = [
    ("umbrella", 265, 205, 40),
    ("towel", 440, 385, 34),
    ("crab", 400, 556, 30),
    ("ball", 180, 420, 22),
    ("flag", 340, 482, 18),
    ("boat", 770, 250, 36),
    ("starfish", 500, 540, 20),
]


LEVELS = [
    ("Level16", "纸艺田园", l16_background, L16_ELEMENTS, L16_DIFFS, 140, opts(STEPS16)),
    ("Level17", "纸艺山村", l17_background, L17_ELEMENTS, L17_DIFFS, 140, opts(STEPS17, blend=3.5)),
    ("Level18", "纸艺海滩", l18_background, L18_ELEMENTS, L18_DIFFS, 140, opts(STEPS18)),
]
