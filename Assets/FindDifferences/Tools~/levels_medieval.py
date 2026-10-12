# -*- coding: utf-8 -*-
"""
Medieval pack (paper-craft):
  Level19 城堡要塞 - side view castle on a hill, day/night cycle (torches and windows light up at night)
  Level20 中世纪集市 - isometric market square, weather: clear -> overcast -> rain -> fog -> overcast
  Level21 酒馆内景 - front view inside a tavern, day/night (the hall gets dim, candles and the fire glow)
"""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, hill_y, paper_post, piece, soft_union, star_pts
from levels_views import ISO_SH, P, THICK, iso_box, iso_cyl, iso_quad, iso_roof, iso_tree
from stylekit import (INK, LAYER, PROP, SMALL, celestial, day_night, drift_across, figure, flame, moon_element, smoke,
                      star_field, sun_element, window_glow)
from weather import CLOUDY, WET, cloud, fog_layer, puddles, rain_layer, splash_rings

STONE = (176, 170, 166)
STONE_D = (150, 144, 142)


def stone_blocks(c, x0, y0, x1, y1, col=STONE_D, h=12, w=22):
    for k, y in enumerate(range(int(y0) + h, int(y1), h)):
        flat(c, Thick(x0, y, x1, y, 1.2), col)
        off = (k % 2) * w / 2
        x = x0 + off
        while x < x1:
            flat(c, Thick(x, y - h, x, y, 1.2), col)
            x += w


def crenels(c, x0, x1, y, col, size=10):
    x = x0
    while x + size <= x1 + 0.1:
        piece(c, RRect(x, y - size, x + size, y + 1, 1), col, shadow=SMALL)
        x += size * 2


def arch(c, x, y_top, w, y_bottom, col):
    flat(c, [RRect(x - w / 2, y_top + w / 2, x + w / 2, y_bottom, 0), Circ(x, y_top + w / 2, w / 2)], col)


# =================================================================== Level 19 castle (side view, day/night)
DN19 = day_night(40.0, tint=(0.30, 0.33, 0.58))
SUN19, MOON19 = celestial((450, 190), (420, 150), 40.0)   # sun clears the keep flag at noon


def l19_background(c, d):
    """城堡要塞 - static part"""
    c.rect(0, 0, W, 660, (172, 208, 235))
    fill_levels.back_Level19(c, d)
    piece(c, Poly([(-20, 330), (120, 200), (220, 260), (330, 170), (450, 250), (560, 180), (700, 240), (820, 160), (940, 260), (940, 400), (-20, 400)]),
          (150, 165, 198), shadow=LAYER)
    piece(c, hill_strip(330, [(12, 0.01, 0.4), (6, 0.03, 1.1)]), (152, 196, 140), shadow=LAYER)
    piece(c, Poly([(150, 420), (240, 330), (330, 310), (580, 310), (680, 330), (760, 420)]), (128, 180, 108), shadow=LAYER)
    # back wall + crenellations
    piece(c, RRect(290, 240, 610, 322, 1), STONE, shadow=PROP)
    stone_blocks(c, 290, 240, 610, 322)
    crenels(c, 290, 610, 240, STONE)
    # keep
    piece(c, RRect(400, 150, 500, 322, 1), lit(STONE, 1.05), shadow=PROP)
    stone_blocks(c, 400, 150, 500, 322)
    crenels(c, 400, 500, 150, lit(STONE, 1.05), size=11)
    for x, y in ((425, 180), (475, 180), (450, 215)):
        arch(c, x, y, 14, y + 24, (60, 50, 70))
    piece(c, Thick(450, 150, 450, 104, 3), (110, 95, 90), shadow=SMALL)
    # towers (right roof colour differs)
    for x, roof in ((300, (80, 110, 180)), (600, (90, 150, 90) if "roof" in d else (190, 70, 70))):
        piece(c, RRect(x - 24, 190, x + 24, 324, 2), lit(STONE, 0.97), shadow=PROP)
        stone_blocks(c, x - 24, 190, x + 24, 324)
        piece(c, Poly([(x - 32, 194), (x + 32, 194), (x, 136)]), roof, border=2, shadow=PROP)
        arch(c, x, 220, 12, 244, (60, 50, 70))
    # gate (portcullis down in A, raised in B) and shield
    arch(c, 450, 262, 44, 322, (55, 42, 50))
    bars_bottom = 286 if "gate" in d else 320
    for x in range(434, 470, 8):
        flat(c, Thick(x, 266, x, bars_bottom, 2.2), (120, 110, 105))
    for y in range(272, int(bars_bottom), 12):
        flat(c, Thick(430, y, 470, y, 2), (120, 110, 105))
    shield = (60, 120, 210) if "shield" in d else (210, 60, 60)
    piece(c, Poly([(438, 240), (462, 240), (462, 252), (450, 262), (438, 252)]), shield, border=1.5, shadow=SMALL)
    flat(c, Thick(450, 242, 450, 258, 2), (250, 220, 90))
    # archer on the wall (missing in B)
    if "archer" not in d:
        figure(c, 548, 240, (90, 130, 80), h=0.55, hat=(90, 130, 80))
        flat(c, [Thick(558, 214, 564, 232, 1.4)], (140, 100, 70))
    # moat + drawbridge
    piece(c, RRect(240, 322, 660, 340, 6), (100, 160, 210), shadow=SMALL)
    piece(c, Poly([(428, 320), (472, 320), (476, 346), (424, 346)]), (150, 105, 70), border=1.5, shadow=PROP)
    # road and front hill with the village
    piece(c, hill_strip(430, [(10, 0.012, 2.0), (5, 0.03, 0.5)]), (116, 170, 96), shadow=LAYER)
    piece(c, Poly([(424, 346), (476, 346), (640, 600), (520, 600)]), (214, 190, 140), shadow=SMALL)
    for x0, x1, top, roof, door_key in ((40, 140, 380, (200, 168, 108), None), (160, 250, 396, (170, 80, 60), "door")):
        b = hill_y(430, [(10, 0.012, 2.0), (5, 0.03, 0.5)], (x0 + x1) / 2) + 12
        piece(c, RRect(x0, top, x1, b, 1), (248, 238, 214), border=2, shadow=PROP)
        for xx in (x0 + 4, (x0 + x1) / 2, x1 - 4):
            flat(c, Thick(xx, top, xx, b, 3), (110, 75, 55))
        flat(c, [Thick(x0, top + 4, x1, top + 4, 3), Thick(x0, (top + b) / 2, x1, (top + b) / 2, 3),
                 Thick(x0 + 4, top, (x0 + x1) / 2, (top + b) / 2, 2.4), Thick(x1 - 4, top, (x0 + x1) / 2, (top + b) / 2, 2.4)],
             (110, 75, 55))
        piece(c, Poly([(x0 - 10, top + 2), (x1 + 10, top + 2), ((x0 + x1) / 2, top - 40)]), roof, border=2, shadow=PROP)
        door = (70, 110, 190) if (door_key and door_key in d) else (120, 80, 60)
        flat(c, RRect((x0 + x1) / 2 - 9, b - 26, (x0 + x1) / 2 + 9, b, 2), door)
        flat(c, RRect(x0 + 10, top + 16, x0 + 24, top + 30, 1), (255, 220, 140))
    for x, s in ((720, 1.0), (800, 1.2), (870, 0.9)):
        b = hill_y(430, [(10, 0.012, 2.0), (5, 0.03, 0.5)], x) + 8
        piece(c, [Thick(x, b, x, b - 30 * s, 6 * s), Circ(x, b - 48 * s, 24 * s), Circ(x - 16 * s, b - 36 * s, 16 * s),
                  Circ(x + 16 * s, b - 36 * s, 16 * s)], (80, 150, 85), shadow=PROP)
    fill_levels.front_Level19(c, d)


def l19_keep_flag(c, m):
    piece(c, Poly([(451, 104), (480, 111), (451, 118)]), (250, 210, 80), border=1.2, shadow=SMALL)


def l19_banner(c, m):
    col = (60, 150, 90) if m else (200, 60, 60)
    flat(c, Thick(326, 200, 344, 200, 2), (110, 95, 90))
    piece(c, Poly([(328, 200), (344, 200), (344, 238), (336, 232), (328, 238)]), col, border=1.2, shadow=SMALL)
    flat(c, Poly(star_pts(336, 214, 5, 2)), (250, 220, 90))


def l19_dragon(c, m):
    x, y = 640, 90
    col = (90, 140, 100)
    piece(c, [Ell(x, y, 22, 9), Poly([(x + 18, y - 4), (x + 34, y - 10), (x + 38, y - 4), (x + 22, y + 4)]),
              Poly([(x - 20, y), (x - 48, y - 6), (x - 20, y + 6)])], col, border=1.5, shadow=SMALL)
    piece(c, Poly([(x - 6, y - 4), (x + 4, y - 30), (x + 14, y - 8)]), lit(col, 1.2), border=1.2, shadow=SMALL)
    flat(c, Circ(x + 32, y - 7, 1.4), (255, 220, 80))


def l19_knight(c, m):
    x, b = 560, 520
    piece(c, [RRect(x - 26, b - 34, x + 22, b - 16, 7), Thick(x - 20, b - 18, x - 22, b, 4), Thick(x + 16, b - 18, x + 18, b, 4),
              Poly([(x + 18, b - 30), (x + 34, b - 44), (x + 40, b - 36), (x + 24, b - 24)])], (245, 240, 232), border=1.5, shadow=PROP)
    piece(c, [RRect(x - 10, b - 58, x + 6, b - 32, 3), Circ(x - 2, b - 64, 7)], (170, 175, 190), border=1.5, shadow=PROP)
    flat(c, Thick(x + 6, b - 50, x + 30, b - 74, 2.2), (120, 90, 70))
    flat(c, Poly([(x + 30, b - 74), (x + 40, b - 78), (x + 32, b - 68)]), (210, 60, 60))


def l19_bat(x, y):
    def d(c, m):
        piece(c, [Poly([(x, y), (x - 12, y - 6), (x - 8, y), (x - 14, y + 2)]), Poly([(x, y), (x + 12, y - 6), (x + 8, y), (x + 14, y + 2)]),
                  Ell(x, y, 3, 4)], (40, 34, 50), shadow=None)
    return d


L19_ELEMENTS = [
    star_field("stars", 19, 50, 220),
    moon_element("moon", (450, 190), MOON19),
    sun_element("sun", (450, 190), SUN19, r=26),
    cloud("cloud1", 200, 70, 0.7, (252, 250, 245), 0, anim=drift_across(160, 260, 7)),
    cloud("cloud2", 760, 110, 0.6, (252, 250, 245), 0, anim=drift_across(725, 810, 5)),
    E("dragon", l19_dragon, pivot=(640, 90),
      anim=dict(drift_across(590, 680, -14), stretch=(0, 0.35), scaleSpeed=1.1, bobAmplitude=(0, 10), bobSpeed=0.15)),
] + [
    E("bat%d" % i, l19_bat(x, y), pivot=(x, y), daynight="night",
      anim=dict(orbitRadius=(26, 12), orbitSpeed=0.25 * (1 if i % 2 else -1), stretch=(0, 0.5), scaleSpeed=3, phase=i * 0.3))
    for i, (x, y) in enumerate(((300, 120), (600, 120), (520, 90)))
] + [
    E("keepflag", l19_keep_flag, pivot=(451, 111), anim=dict(stretch=(0.25, 0), scaleSpeed=1.5, swingAngle=5, swingSpeed=1.1),
      animB={}),
    E("banner", l19_banner, variant=True, pivot=(336, 200), anim=dict(swingAngle=3, swingSpeed=0.4)),
    window_glow("windows", [(418, 181, 432, 204), (468, 181, 482, 204), (443, 216, 457, 239), (294, 221, 306, 244),
                            (594, 221, 606, 244), (50, 396, 64, 410)]),
] + flame("torch1", 418, 288) + flame("torch2", 482, 288) + smoke("smoke", 90, 330, n=3) + [
    E("knight", l19_knight, pivot=(560, 520),
      anim=dict(bobAmplitude=(70, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85, swingAngle=3, swingSpeed=1.2)),
]

L19_DIFFS = [
    ("banner", 336, 220, 22),
    ("keepflag", 465, 111, 18),
    ("roof", 600, 166, 46),
    ("gate", 450, 295, 26),
    ("shield", 450, 250, 14),
    ("archer", 550, 224, 30),
    ("door", 205, int(hill_y(430, [(10, 0.012, 2.0), (5, 0.03, 0.5)], 205) - 2), 18),
]


# =================================================================== Level 20 market (isometric, weather)
STEPS20 = [(CLEAR, 12), (OVERCAST, 6), (RAIN, 12), (FOG, 6), (OVERCAST, 4)]
COBBLE = (196, 190, 178)


def timber_house(c, X, Y, dx, dy, dz, roof):
    top, left, right = iso_box(c, X, Y, 0, dx, dy, dz, (246, 238, 220))
    beam = (110, 76, 56)
    for t in (0.0, 0.5, 1.0):
        a, b = P(X + dx * t, Y + dy, 0), P(X + dx * t, Y + dy, dz)
        flat(c, Thick(a[0], a[1], b[0], b[1], 2.4), beam)
        a, b = P(X + dx, Y + dy * t, 0), P(X + dx, Y + dy * t, dz)
        flat(c, Thick(a[0], a[1], b[0], b[1], 2.4), beam)
    for z in (dz * 0.5, dz):
        a, b = P(X, Y + dy, z), P(X + dx, Y + dy, z)
        flat(c, Thick(a[0], a[1], b[0], b[1], 2.4), beam)
        a, b = P(X + dx, Y, z), P(X + dx, Y + dy, z)
        flat(c, Thick(a[0], a[1], b[0], b[1], 2.4), beam)
    flat(c, Poly([P(X + dx * 0.3, Y + dy, 0), P(X + dx * 0.45, Y + dy, 0), P(X + dx * 0.45, Y + dy, dz * 0.42),
                  P(X + dx * 0.3, Y + dy, dz * 0.42)]), (120, 80, 60))
    flat(c, Poly([P(X + dx * 0.62, Y + dy, dz * 0.62), P(X + dx * 0.8, Y + dy, dz * 0.62), P(X + dx * 0.8, Y + dy, dz * 0.86),
                  P(X + dx * 0.62, Y + dy, dz * 0.86)]), (255, 222, 140))
    iso_box(c, X + dx * 0.15, Y + dy * 0.2, dz, 0.28, 0.28, 0.75, (160, 95, 80), border=1.5)
    iso_roof(c, X - 0.1, Y - 0.1, dz, dx + 0.2, dy + 0.2, 0.7, roof)


def stall(c, X, Y, cloth, stripe, goods):
    iso_box(c, X, Y, 0, 1.2, 0.7, 0.45, (170, 120, 80))
    for px, py in ((X, Y), (X + 1.2, Y), (X, Y + 0.7), (X + 1.2, Y + 0.7)):
        a, b = P(px, py, 0.45), P(px, py, 1.25)
        piece(c, Thick(a[0], a[1], b[0], b[1], 2.4), (130, 90, 60), shadow=None)
    gx, gy = P(X + 0.6, Y + 0.35, 0.5)
    for i in range(6):
        piece(c, Circ(gx - 20 + (i % 3) * 14 + (i // 3) * 6, gy - 2 + (i // 3) * 5, 5), goods, shadow=(1, 1, 2, 0.3))
    iso_roof(c, X - 0.1, Y - 0.1, 1.2, 1.4, 0.9, 0.35, cloth, stripe=stripe)


def church(c, flag):
    X, Y, dx, dy, dz = 0.9, 0.9, 1.8, 1.6, 2.4
    iso_box(c, X, Y, 0, dx, dy, dz, (200, 194, 186))
    for wx in (0.25, 0.65):
        flat(c, [Poly([P(X + dx * wx, Y + dy, dz * 0.45), P(X + dx * wx + 0.22, Y + dy, dz * 0.45), P(X + dx * wx + 0.22, Y + dy, dz * 0.8),
                       P(X + dx * wx, Y + dy, dz * 0.8)])], (90, 110, 160))
    iso_roof(c, X - 0.1, Y - 0.1, dz, dx + 0.2, dy + 0.2, 0.9, (110, 90, 120))
    # bell tower
    tx, ty = X + dx - 0.7, Y + 0.25
    iso_box(c, tx, ty, dz, 0.6, 0.6, 1.6, (205, 200, 192))
    belfry = Poly([P(tx + 0.12, ty + 0.6, dz + 0.9), P(tx + 0.48, ty + 0.6, dz + 0.9), P(tx + 0.48, ty + 0.6, dz + 1.4),
                   P(tx + 0.12, ty + 0.6, dz + 1.4)])
    flat(c, belfry, (60, 50, 70))
    apex = P(tx + 0.3, ty + 0.3, dz + 2.6)
    for poly, col in ((Poly([P(tx, ty + 0.6, dz + 1.6), P(tx + 0.6, ty + 0.6, dz + 1.6), apex]), (120, 95, 130)),
                      (Poly([P(tx + 0.6, ty, dz + 1.6), P(tx + 0.6, ty + 0.6, dz + 1.6), apex]), (95, 75, 105))):
        piece(c, poly, col, border=1.5, shadow=ISO_SH)
    piece(c, Thick(apex[0], apex[1], apex[0], apex[1] - 16, 2), (90, 80, 90), shadow=None)
    if flag:
        piece(c, Poly([(apex[0], apex[1] - 16), (apex[0] + 16, apex[1] - 12), (apex[0], apex[1] - 8)]), (230, 80, 80), shadow=None)
    return P(tx + 0.3, ty + 0.6, dz + 1.3)


def l20_decor(c, X, Y, r):
    x, y = P(X, Y)
    if r < 0.4:
        timber_house(c, X - 0.5, Y - 0.5, 1.1, 1.0, 0.9 + r, [(190, 70, 60), (150, 100, 70), (110, 120, 160)][int(r * 30) % 3])
    elif r < 0.65:
        iso_tree(c, X, Y, 0.8)
    elif r < 0.85:
        for k in range(2):
            bx, by, bex, bey = iso_cyl(c, X + k * 0.35, Y, 0, 0.5, 0.18, (160, 110, 70), border=1.5)
    else:
        iso_box(c, X, Y, 0, 0.5, 0.5, 0.4, (190, 150, 100), border=1.5)


def _l20_surround():
    from fill_iso import surround_points
    return surround_points(20, step=76, keep=0.62)


L20_SURROUND = _l20_surround()
BELL20 = P(0.9 + 1.8 - 0.7 + 0.3, 0.9 + 0.25 + 0.6, 2.4 + 1.3)
JUGGLER20 = (4.7, 7.2)


def l20_background(c, d):
    """中世纪集市 - static part"""
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (186, 180, 168), (176, 170, 158))
    flat(c, iso_quad(0, 0, 10, 10), COBBLE)
    draw_surround(c, L20_SURROUND, l20_decor, "back")
    for k in range(1, 10):
        for a, b in ((P(k, 0), P(k, 10)), (P(0, k), P(10, k))):
            flat(c, Thick(a[0], a[1], b[0], b[1], 1), (178, 172, 160))
    for q in (iso_quad(0.2, 8.4, 3.0, 9.8), iso_quad(8.4, 0.2, 9.8, 3.0)):
        piece(c, q, (140, 190, 110), shadow=(1, 2, 3, 0.2))
    church(c, "flag" not in d)
    timber_house(c, 4.0, 0.6, 1.5, 1.2, 1.4, (190, 70, 60))
    timber_house(c, 7.2, 0.9, 1.6, 1.3, 1.3, (150, 100, 70))
    timber_house(c, 0.6, 5.2, 1.3, 1.5, 1.2, (110, 120, 160))
    # well
    wx, wy, ex, ey = iso_cyl(c, 5.0, 5.0, 0, 0.45, 0.55, (170, 166, 162))
    flat(c, Ell(wx, wy, ex * 0.7, ey * 0.7), (60, 70, 90))
    for dxp in (-ex * 0.8, ex * 0.8):
        piece(c, Thick(wx + dxp, wy, wx + dxp, wy - 40, 3), (140, 95, 70), shadow=SMALL)
    piece(c, Poly([(wx - ex - 8, wy - 38), (wx + ex + 8, wy - 38), (wx, wy - 58)]), (150, 80, 60), border=1.5, shadow=SMALL)
    # stalls (S2 stripes differ; apples red/green)
    stall(c, 2.8, 3.7, (250, 248, 240), (60, 120, 200), (120, 200, 90) if "apples" in d else (225, 60, 60))
    stall(c, 6.4, 3.6, (250, 248, 240), (90, 170, 90) if "stall" in d else (220, 80, 80), (250, 200, 70))
    stall(c, 6.2, 6.5, (250, 248, 240), (230, 180, 60), (170, 110, 200))
    # barrels and crates (one barrel fewer in B)
    barrels = [(7.9, 7.6), (8.3, 7.4), (8.1, 8.0)] + ([] if "barrels" in d else [(8.5, 7.9)])
    for X, Y in barrels:
        bx, by, bex, bey = iso_cyl(c, X, Y, 0, 0.55, 0.2, (160, 110, 70), border=1.5)
        flat(c, Ell(bx, by + 6, bex, bey * 0.6), (120, 80, 55))
    iso_box(c, 2.2, 7.6, 0, 0.5, 0.5, 0.4, (190, 150, 100), border=1.5)
    iso_box(c, 2.3, 7.7, 0.4, 0.35, 0.35, 0.3, (200, 160, 110), border=1.5)
    # cart (wheel colour differs)
    iso_box(c, 3.6, 8.6, 0.25, 1.2, 0.6, 0.35, (170, 120, 80), border=1.5)
    cx, cy = P(4.2, 9.2, 0.22)
    piece(c, Circ(cx, cy, 11), (80, 120, 200) if "wheel" in d else (140, 95, 60), border=1.5, shadow=SMALL)
    flat(c, [Thick(cx - 9, cy, cx + 9, cy, 1.4), Thick(cx, cy - 9, cx, cy + 9, 1.4)], (90, 70, 55))
    # trees + people
    for X, Y in ((9.2, 4.6), (0.5, 3.6), (9.3, 6.4)):
        iso_tree(c, X, Y, 0.9)
    for X, Y, col in ((3.4, 4.7, (150, 90, 160)), (7.0, 4.6, (90, 140, 90)), (6.8, 7.4, (180, 90, 80)), (2.0, 6.6, (90, 110, 170))):
        x, y = P(X, Y)
        figure(c, x, y, col, h=0.7)
    jx, jy = P(*JUGGLER20)
    figure(c, jx, jy, (230, 180, 60), h=0.75, hat=(200, 60, 60))
    from fill_iso import draw_surround
    draw_surround(c, L20_SURROUND, l20_decor, "front")


def l20_bell(c, m):
    x, y = BELL20
    piece(c, Poly([(x - 6, y + 2), (x + 6, y + 2), (x + 4, y - 8), (x - 4, y - 8)]), (220, 180, 70), border=1, shadow=None)


def l20_ball(i):
    jx, jy = P(*JUGGLER20)
    cx, cy = jx + 2, jy - 62
    col = [(230, 80, 80), (80, 150, 230), (250, 210, 70)][i]

    def d(c, m):
        piece(c, Circ(cx, cy, 4.5), col, border=1, shadow=SMALL)
    return d, (cx, cy)


def l20_pigeon(x, y):
    def d(c, m):
        piece(c, [Ell(x, y, 7, 5), Circ(x + 6, y - 4, 3.5)], (150, 150, 165), shadow=SMALL)
        flat(c, Poly([(x + 9, y - 4), (x + 12, y - 3), (x + 9, y - 2)]), (230, 160, 60))
    return d


L20_ELEMENTS = [
    cloud("cloud_w1", 170, 70, 0.8, (252, 252, 248), W_(CLEAR), anim=drift_across(125, 235, 7)),
    cloud("cloud_w2", 700, 50, 0.6, (252, 252, 248), W_(CLEAR), anim=drift_across(665, 750, 5)),
] + [cloud("cloud_g%d" % i, x, y, k, (170, 175, 190), W_(OVERCAST, RAIN, FOG)) for i, (x, y, k) in
     enumerate(((90, 50, 1.3), (330, 30, 1.5), (580, 50, 1.4), (820, 40, 1.3)))] + [
    E("bell", l20_bell, pivot=(BELL20[0], BELL20[1] - 10), anim=dict(swingAngle=24, swingSpeed=0.6), animB={}),
] + smoke("smoke", *P(4.0 + 1.5 * 0.15 + 0.14, 0.6 + 1.2 * 0.2 + 0.14, 1.4 + 0.85)) \
  + smoke("smoke2_", *P(7.2 + 1.6 * 0.15 + 0.14, 0.9 + 1.3 * 0.2 + 0.14, 1.3 + 0.85)) + [
    E("ball%d" % i, l20_ball(i)[0], pivot=l20_ball(i)[1],
      anim=dict(orbitRadius=(14, 18), orbitSpeed=0.7, phase=i / 3), animB=dict(bobAmplitude=(0, 0)))
    for i in range(3)
] + [
    E("pigeon%d" % i, l20_pigeon(x, y), pivot=(x, y), anim=dict(swingAngle=14, swingSpeed=0.5 + 0.2 * i, phase=i * 0.3))
    for i, (x, y) in enumerate((P(5.6, 4.3), P(4.2, 5.8), P(5.4, 6.0)))
] + [
    puddles("puddles", [Ell(*P(3.6, 6.0), 34, 10), Ell(*P(6.0, 2.6), 28, 8), Ell(*P(7.6, 5.4), 30, 9), Ell(*P(2.0, 3.2), 26, 8)]),
] + splash_rings("splash", [(P(3.6, 6.0)[0], P(3.6, 6.0)[1], 8), (P(6.0, 2.6)[0], P(6.0, 2.6)[1], 7),
                            (P(7.6, 5.4)[0], P(7.6, 5.4)[1], 8), (P(5.0, 7.8)[0], P(5.0, 7.8)[1], 7)]) + [
    rain_layer("rain", 20, 80, 24, 1.3, 0.75, 240, mask=W_(RAIN)),
    fog_layer("fog1", 2, 160, 320, 0.5, 10, 1),
    fog_layer("fog2", 6, 320, 500, 0.55, 13, -1),
]

L20_DIFFS = [
    ("stall", int(P(7.0, 4.0, 1.4)[0]) - 8, int(P(7.0, 4.0, 1.4)[1]), 52),
    ("juggler", int(P(*JUGGLER20)[0] + 2), int(P(*JUGGLER20)[1] - 60), 30),
    ("bell", int(BELL20[0]), int(BELL20[1] - 4), 18),
    ("barrels", int(P(8.5, 7.9)[0]) - 4, int(P(8.5, 7.9)[1] - 14), 32),
    ("apples", int(P(3.4, 4.05, 0.5)[0]), int(P(3.4, 4.05, 0.5)[1]), 24),
    ("flag", int(P(0.9 + 1.8 - 0.4, 1.45, 5.0)[0] + 8), int(P(0.9 + 1.8 - 0.4, 1.45, 5.0)[1] - 12), 16),
    ("wheel", int(P(4.2, 9.2, 0.22)[0]), int(P(4.2, 9.2, 0.22)[1]), 16),
]


# =================================================================== Level 21 tavern (front view, day/night)
DN21 = day_night(40.0, tint=(0.42, 0.36, 0.48), phase=0.0)
WIN21 = [(300, 150, 380, 262), (520, 150, 600, 262)]


def l21_background(c, d):
    """酒馆内景 - static part"""
    c.rect(0, 0, W, 660, (176, 206, 232))
    # sky in the windows is the bare background; walls are drawn around them
    plaster = (246, 230, 198)
    wall_shapes = [RRect(0, 0, W, 150, 0), RRect(0, 262, W, 600, 0), RRect(0, 150, 300, 262, 0), RRect(380, 150, 520, 262, 0),
                   RRect(600, 150, W, 262, 0)]
    flat(c, wall_shapes, plaster)
    piece(c, RRect(0, 340, W, 500, 0), STONE, shadow=(0, -3, 8, 0.3))
    stone_blocks(c, 0, 340, W, 500, h=16, w=30)
    for x0, y0, x1, y1 in WIN21:
        piece(c, [RRect(x0 - 8, y0 - 8, x1 + 8, y0 + 2), RRect(x0 - 8, y1 - 2, x1 + 8, y1 + 10), RRect(x0 - 8, y0 - 8, x0 + 2, y1 + 10),
                  RRect(x1 - 2, y0 - 8, x1 + 8, y1 + 10), RRect((x0 + x1) / 2 - 3, y0, (x0 + x1) / 2 + 3, y1),
                  RRect(x0, (y0 + y1) / 2 - 3, x1, (y0 + y1) / 2 + 3)], (120, 80, 55), shadow=PROP)
    # ceiling beams and posts
    piece(c, RRect(-10, 0, W + 10, 54, 0), (110, 74, 52), shadow=PROP)
    for x in (60, 270, 450, 630, 840):
        piece(c, RRect(x - 10, 54, x + 10, 500, 2), (126, 86, 60), shadow=PROP)
    # floor
    piece(c, RRect(-10, 500, W + 10, 610, 0), (170, 120, 80), shadow=(0, -3, 8, 0.3))
    for x in range(-20, 920, 46):
        flat(c, Thick(x, 500, x - 30, 600, 1.6), (145, 100, 66))
    # shields and swords between the windows
    for i, (x, col) in enumerate(((410, (200, 60, 60)), (450, (60, 110, 190)), (490, (240, 200, 70)))):
        if i == 1 and "shield" in d:
            col = (90, 160, 90)
        piece(c, Poly([(x - 14, 176), (x + 14, 176), (x + 14, 196), (x, 212), (x - 14, 196)]), col, border=1.5, shadow=PROP)
        flat(c, Thick(x, 180, x, 206, 2.4), (250, 240, 220))
    swords = [((420, 240), (480, 222)), ((420, 222), (480, 240))]
    if "swords" in d:
        swords = swords[:1]
    for (a, b) in swords:
        piece(c, [Thick(a[0], a[1], b[0], b[1], 3), Thick(a[0] + 8, a[1] - 8, a[0] + 8, a[1] + 8, 3)], (205, 210, 220), shadow=SMALL)
    # fireplace
    piece(c, [RRect(70, 290, 250, 500, 4)], (160, 150, 146), shadow=PROP)
    stone_blocks(c, 70, 290, 250, 500, h=18, w=26)
    piece(c, RRect(60, 280, 260, 296, 2), (130, 90, 62), shadow=PROP)
    flat(c, [RRect(100, 380, 220, 500, 0), Circ(160, 380, 60)], (50, 36, 40))
    flat(c, [Thick(110, 494, 210, 486, 7), Thick(115, 486, 205, 494, 7)], (120, 76, 52))
    # bar counter with barrels and taps
    piece(c, RRect(640, 270, 880, 300, 2), (140, 96, 66), shadow=PROP)
    for i, x in enumerate((680, 740, 800, 860)):
        piece(c, Circ(x, 330, 24), (165, 115, 75), border=2, border_col=(110, 75, 55), shadow=PROP)
        flat(c, Circ(x, 330, 8), (130, 88, 60))
        tap = (70, 130, 210) if (i == 2 and "tap" in d) else (210, 180, 80)
        piece(c, Thick(x, 344, x, 360, 4), tap, shadow=SMALL)
    piece(c, RRect(630, 400, 890, 500, 3), (150, 104, 70), border=2, shadow=PROP)
    piece(c, RRect(620, 392, 900, 408, 3), (176, 124, 84), shadow=PROP)
    for x in (660, 720, 820):
        piece(c, [RRect(x - 9, 372, x + 9, 394, 3), Thick(x + 9, 378, x + 15, 386, 3)], (220, 210, 190), border=1.2, shadow=SMALL)
        flat(c, RRect(x - 7, 372, x + 7, 378, 2), (250, 245, 230))
    # table with mugs (one missing in B), bread and candle
    piece(c, [RRect(370, 440, 570, 456, 3), RRect(390, 456, 404, 500, 2), RRect(536, 456, 550, 500, 2)], (160, 110, 72), border=2,
          shadow=PROP)
    mugs = [(400, 420), (520, 420)] + ([] if "mug" in d else [(548, 422)])
    for x, y in mugs:
        piece(c, [RRect(x - 9, y, x + 9, y + 20, 3), Thick(x + 9, y + 5, x + 15, y + 13, 3)], (200, 190, 170), border=1.2, shadow=SMALL)
    piece(c, Ell(450, 432, 22, 8), (215, 170, 100), border=1.2, shadow=SMALL)
    piece(c, RRect(475, 412, 483, 440, 2), (250, 245, 230), shadow=SMALL)
    # bard (feather on the hat in A only)
    hx, hy = figure(c, 300, 500, (90, 70, 140), h=1.4, hat=(160, 60, 70))
    if "feather" not in d:
        piece(c, Ell(hx + 8, hy - 22, 3, 10), (250, 240, 120), shadow=None)
    piece(c, [Ell(318, 456, 12, 9), Thick(326, 452, 350, 436, 3)], (200, 140, 80), border=1.2, shadow=SMALL)
    # sleeping cat (tail is animated)
    piece(c, [Ell(200, 520, 22, 11), Circ(220, 512, 9), Poly([(214, 506), (216, 496), (222, 504)]), Poly([(222, 504), (228, 496), (229, 507)])],
          (110, 100, 110), border=1.5, shadow=SMALL)
    fill_levels.front_Level21(c, d)


def l21_window_sky(c, m):
    """Stars visible through the windows at night."""
    rnd = random.Random(21)
    for x0, y0, x1, y1 in WIN21:
        for _ in range(7):
            x, y = rnd.uniform(x0 + 6, x1 - 6), rnd.uniform(y0 + 6, y1 - 6)
            flat(c, Poly(star_pts(x, y, 3, 1, points=4, rot=0)), (255, 248, 210))
    soft_union(c, [Circ(578, 180, 12)], (255, 250, 220), 0.35, spread=10)
    flat(c, Circ(578, 180, 12), (252, 246, 220))


def l21_chandelier(c, m):
    x, y = 470, 140
    flat(c, Thick(x, 54, x, y - 10, 2), (60, 50, 50))
    c.ellipse_ring(x, y, 70, 14, 4, (70, 55, 50))
    candles = [-56, -28, 0, 28, 56] if not m else [-56, -28, 28, 56]
    for dx in candles:
        yy = y + 13 * math.sqrt(max(0, 1 - (dx / 70) ** 2))
        flat(c, RRect(x + dx - 3, yy - 14, x + dx + 3, yy, 1), (250, 245, 225))
        flat(c, Poly([(x + dx - 3, yy - 14), (x + dx + 3, yy - 14), (x + dx, yy - 25)]), (255, 170, 60))
        flat(c, Poly([(x + dx - 1.5, yy - 14), (x + dx + 1.5, yy - 14), (x + dx, yy - 20)]), (255, 238, 150))


def l21_chandelier_glow(c, m):
    soft_union(c, [Ell(470, 125, 70, 12)], (255, 200, 110), 0.45, spread=40)


def l21_tail(c, m):
    piece(c, [Thick(180, 524, 160, 520, 4), Thick(160, 520, 150, 506, 4)], (110, 100, 110), border=1.2, shadow=SMALL)


def l21_spit(c, m):
    flat(c, Thick(100, 430, 220, 430, 2.5), (90, 80, 80))
    piece(c, Ell(160, 430, 24, 13), (190, 110, 60), border=1.2, shadow=SMALL)
    flat(c, Ell(154, 426, 10, 4), (215, 140, 80))


L21_ELEMENTS = [
    E("window_sky", l21_window_sky, daynight="night"),
] + flame("fire1", 140, 488, 2.2) + flame("fire2", 175, 490, 2.6) + flame("candle", 479, 412, 0.8) + [
    E("spit", l21_spit, pivot=(160, 430), anim=dict(spinSpeed=0.2, spinShade=0.4)),
    E("chandelier_glow", l21_chandelier_glow, pivot=(470, 54), daynight="night", anim=dict(swingAngle=2, swingSpeed=0.15)),
    E("chandelier", l21_chandelier, pivot=(470, 54), variant=True, daynight="untinted", anim=dict(swingAngle=2, swingSpeed=0.15)),
    E("tail", l21_tail, pivot=(180, 524), anim=dict(swingAngle=18, swingSpeed=0.45), animB={}),
] + smoke("steam", 400, 416, n=3, col=(250, 250, 252), r=4, length=34)

L21_DIFFS = [
    ("shield", 450, 194, 18),
    ("swords", 450, 231, 36),
    ("chandelier", 470, 128, 30),
    ("mug", 548, 432, 16),
    ("tap", 800, 352, 14),
    ("feather", 310, 424, 18),
    ("tail", 164, 514, 22),
]


LEVELS = [
    ("Level19", "城堡要塞", l19_background, L19_ELEMENTS, L19_DIFFS, 140,
     dict(post=paper_post, day_night=DN19, anim_seconds=40.0, frames=80)),
    ("Level20", "中世纪集市", l20_background, L20_ELEMENTS, L20_DIFFS, 140,
     dict(post=paper_post, weather=dict(steps=STEPS20, blend=3.0), anim_seconds=40.0, frames=80)),
    ("Level21", "酒馆内景", l21_background, L21_ELEMENTS, L21_DIFFS, 140,
     dict(post=paper_post, day_night=DN21, anim_seconds=40.0, frames=80)),
]
