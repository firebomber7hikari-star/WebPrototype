# -*- coding: utf-8 -*-
"""
Cyberpunk pack (paper-craft + neon glow):
  Level22 霓虹雨街   - side view street at night, weather: rain -> thunderstorm -> rain -> overcast
  Level23 天台都市   - isometric rooftop, day/night cycle + smog (fog) weather
  Level24 霓虹十字路口 - top-down intersection at night, weather: clear -> rain -> thunderstorm -> rain -> overcast
Neon parts are 'untinted' so they keep glowing when the scene darkens.
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, THUNDER, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union, star_pts
from levels_views import ISO_SH, P, THICK, iso_box, iso_cyl, iso_quad
from stylekit import (INK, LAYER, PROP, SMALL, day_night, drift_across, figure, neon, neon_glyphs, neon_post, smoke)
from weather import WET, flash, fog_layer, lightning, rain_layer, splash_rings

CYAN, MAGENTA, YELLOW, LIME, ORANGE = (60, 235, 255), (255, 60, 200), (255, 220, 70), (120, 255, 120), (255, 140, 60)
NIGHT_TINTS = {OVERCAST: (0.86, 0.86, 0.92), RAIN: (0.78, 0.80, 0.90), THUNDER: (0.62, 0.62, 0.76), FOG: (0.92, 0.94, 0.9)}


def window_grid(c, x0, y0, x1, y1, seed, cols=(CYAN, YELLOW, (255, 170, 220)), density=0.45, cw=10, ch=12, alpha=0.85):
    rnd = random.Random(seed)
    y = y0 + 6
    while y < y1 - 8:
        x = x0 + 5
        while x < x1 - 7:
            if rnd.random() < density:
                flat(c, RRect(x, y, x + cw * 0.55, y + ch * 0.5, 0.8), rnd.choice(cols) + (alpha,))
            x += cw
        y += ch


def opts(**kw):
    out = dict(post=neon_post, anim_seconds=40.0, frames=80)
    out.update(kw)
    return out


# =================================================================== Level 22 neon rain street (side)
STEPS22 = [(RAIN, 12), (THUNDER, 8), (RAIN, 8), (OVERCAST, 8)]


def l22_background(c, d):
    """霓虹雨街 - static part"""
    c.gradient(0, 420, (16, 12, 42), (78, 32, 96))
    rnd = random.Random(22)
    # far skyline
    x = -20
    while x < 920:
        w, h = rnd.randint(40, 90), rnd.randint(140, 300)
        piece(c, RRect(x, 420 - h, x + w, 430, 1), (44, 34, 86), shadow=None)
        window_grid(c, x, 420 - h, x + w, 420, rnd.randint(0, 999), density=0.25, alpha=0.6)
        x += w + rnd.randint(4, 14)
    # mid buildings
    for x0, x1, top in ((-10, 120, 160), (690, 820, 130), (820, 930, 190)):
        piece(c, RRect(x0, top, x1, 470, 1), (30, 26, 62), shadow=LAYER)
        window_grid(c, x0, top, x1, 300, rnd.randint(0, 999), density=0.4)
    # street-level facades
    fac = (40, 34, 72)
    for x0, x1, top in ((0, 230, 300), (230, 470, 250), (470, 700, 310), (700, 900, 270)):
        piece(c, RRect(x0, top, x1, 480, 1), fac, shadow=LAYER)
        window_grid(c, x0, top, x1, 380, rnd.randint(0, 999), density=0.35)
    # antennas on the arcade roof (one fewer in B)
    for i, x in enumerate((260, 300, 430)):
        if i == 1 and "antenna" in d:
            continue
        piece(c, [Thick(x, 250, x, 200 - i * 10, 2.5), Thick(x - 10, 214 - i * 10, x + 10, 214 - i * 10, 2)], (90, 85, 110), shadow=SMALL)
    # ramen stall awning + counter (B1)
    piece(c, Poly([(10, 380), (220, 380), (232, 410), (-2, 410)]), (200, 60, 70), shadow=PROP)
    for x in range(10, 220, 30):
        flat(c, Poly([(x, 380), (x + 15, 380), (x + 15, 410), (x, 410)]), (240, 230, 220))
    piece(c, RRect(20, 440, 210, 480, 2), (120, 80, 60), shadow=PROP)
    soft_union(c, [RRect(30, 412, 200, 440, 2)], (255, 200, 120), 0.5, spread=12)
    flat(c, RRect(30, 412, 200, 440, 2), (255, 214, 150))
    # arcade big sign frame (B2) + glyphs (static neon)
    piece(c, RRect(260, 290, 440, 360, 4), (24, 20, 44), shadow=PROP)
    neon(c, neon_glyphs(274, 302, 152, 46, 4, seed=5, width=4), MAGENTA)
    soft_union(c, [RRect(250, 400, 450, 480, 2)], (120, 80, 255), 0.4, spread=10)
    flat(c, RRect(250, 400, 450, 480, 2), (70, 50, 140))
    for x in range(262, 450, 30):
        flat(c, RRect(x, 412, x + 18, 470, 2), (150, 120, 255, 0.7))
    # vending machines (B3), second one changes colour
    for i, x in enumerate((500, 548)):
        col = (60, 140, 255) if i == 0 else ((255, 80, 80) if "vending" not in d else (90, 230, 120))
        soft_union(c, [RRect(x, 380, x + 40, 478, 3)], col, 0.4, spread=12)
        piece(c, RRect(x, 380, x + 40, 478, 3), lit(col, 0.6), border=1.5, border_col=lit(col, 1.2), shadow=PROP)
        flat(c, RRect(x + 5, 386, x + 35, 430, 2), (240, 248, 255))
        for k in range(3):
            flat(c, RRect(x + 7 + k * 9, 392, x + 13 + k * 9, 420, 1), [(255, 120, 120), (120, 220, 255), (255, 220, 120)][k])
    # stairs + door (B3)
    for k in range(5):
        flat(c, RRect(610 + k * 8, 440 - k * 12, 690, 452 - k * 12, 0), (55, 48, 90))
    # shutter (B4): open shop in A, closed in B
    if "shutter" in d:
        piece(c, RRect(720, 390, 880, 478, 1), (110, 110, 130), shadow=PROP)
        for y in range(394, 478, 7):
            flat(c, Thick(720, y, 880, y, 1.2), (85, 85, 100))
    else:
        soft_union(c, [RRect(720, 390, 880, 478, 1)], YELLOW, 0.35, spread=10)
        flat(c, RRect(720, 390, 880, 478, 1), (255, 236, 170))
        for x in (745, 790, 835):
            flat(c, RRect(x, 430, x + 24, 478, 2), (230, 150, 90))
    # balconies
    for y in (300, 340):
        flat(c, Thick(710, y, 890, y, 3), (120, 110, 150))
    # sidewalk + wet road with neon reflections
    piece(c, RRect(-10, 478, 910, 500, 0), (64, 58, 92), shadow=PROP)
    c.rect(0, 500, W, 660, (26, 24, 44))
    for x, col in ((120, (255, 200, 120)), (350, MAGENTA), (520, (60, 140, 255)), (568, (255, 80, 80)), (800, YELLOW)):
        for k in range(6):
            flat(c, Thick(x - 30 + k * 12, 510, x - 30 + k * 12, 600, 3), col + (0.16,))
    for x in range(0, 900, 70):
        flat(c, RRect(x, 548, x + 36, 552, 1), (200, 200, 220, 0.6))


def l22_sign(c, m):
    col = CYAN if m else ORANGE
    shapes = [Circ(120, 345, 22), Thick(96, 345, 144, 345, 3)]
    soft_union(c, shapes, col, 0.5, spread=14)
    flat(c, [Thick(98 + k * 8, 330, 104 + k * 8, 318, 2.5) for k in range(5)], col)
    c.ellipse_ring(120, 345, 22, 22, 4, col)
    flat(c, Thick(98, 345, 142, 345, 3), lit(col, 1.2))


def l22_holo(c, m):
    col = MAGENTA if m else CYAN
    x, y = 350, 200
    body = [Ell(x, y, 46, 20), Poly([(x + 40, y), (x + 78, y - 22), (x + 70, y), (x + 78, y + 22)]),
            Poly([(x - 10, y - 18), (x + 8, y - 40), (x + 14, y - 16)])]
    soft_union(c, body, col, 0.25, spread=18)
    for s in body:
        s.draw(c, col + (0.35,))
    flat(c, [Thick(x - 36, y - 6, x + 30, y - 6, 1.4), Thick(x - 30, y + 6, x + 26, y + 6, 1.4)], (255, 255, 255, 0.5))
    flat(c, Circ(x - 30, y - 4, 3), (255, 255, 255, 0.8))


def l22_car(x, y, col):
    def d(c, m):
        soft_union(c, [RRect(x - 70, y - 2, x - 20, y + 4, 2)], col, 0.4, spread=6)
        piece(c, [RRect(x - 22, y - 10, x + 22, y + 6, 6), Poly([(x - 12, y - 10), (x + 8, y - 10), (x + 2, y - 20), (x - 8, y - 20)])],
              (70, 70, 100), border=1.2, border_col=col, shadow=None)
        soft_union(c, [Circ(x + 22, y - 2, 3)], (255, 255, 230), 0.8, spread=8)
        flat(c, Circ(x + 22, y - 2, 2.5), (255, 255, 240))
    return d


def l22_drone(c, m):
    x, y = 640, 150
    piece(c, [RRect(x - 14, y - 4, x + 14, y + 6, 3), Thick(x - 26, y - 6, x + 26, y - 6, 2)], (90, 95, 120), border=1, shadow=None)
    soft_union(c, [Circ(x, y + 7, 3)], (255, 255, 230), 0.8, spread=6)


def l22_walker(x, col):
    def d(c, m):
        ucol = (col[1] if m else col[0])
        figure(c, x, 486, (50, 50, 70), head=(230, 200, 180), h=0.9, border=0, shadow=None)
        flat(c, Thick(x + 1, 446, x + 1, 418, 1.5), (200, 200, 210))
        soft_union(c, [Poly([(x - 24, 424), (x + 26, 424), (x + 1, 404)])], ucol, 0.35, spread=8)
        flat(c, Poly([(x - 24, 424), (x + 26, 424), (x + 1, 404)]), ucol + (0.75,))
    return d


L22_ELEMENTS = [
    E("holo", l22_holo, variant=True, daynight="untinted", pivot=(350, 200),
      anim=dict(bobAmplitude=(0, 8), bobSpeed=0.25, twinkle=0.35, twinkleSpeed=1.6, pulse=0.03, scaleSpeed=0.5)),
] + [
    E("car%d" % i, l22_car(x, y, col), daynight="untinted", anim=drift_across(x - 72, x + 26, sp))
    for i, (x, y, col, sp) in enumerate(((200, 120, MAGENTA, 60), (600, 170, CYAN, -45), (420, 235, YELLOW, 75)))
] + [
    E("drone", l22_drone, show="A", daynight="untinted", pivot=(640, 150), anim=dict(swingAngle=10, swingSpeed=0.2, bobAmplitude=(0, 6), bobSpeed=0.4)),
    E("sign", l22_sign, variant=True, daynight="untinted", anim=dict(twinkle=0.25, twinkleSpeed=2.5)),
] + smoke("steam", 90, 410, n=3, col=(230, 230, 240), r=8, length=50) + smoke("steam_b", 150, 410, n=3, col=(230, 230, 240), r=7, length=46) + [
    E("walker1", l22_walker(300, (CYAN, CYAN)), pivot=(300, 486), daynight="untinted",
      anim=dict(bobAmplitude=(60, 0), bobSpeed=0.04, spinSpeed=0.04, spinSnap=0.85)),
    E("walker2", l22_walker(640, (MAGENTA, LIME)), pivot=(640, 486), variant=True, daynight="untinted",
      anim=dict(bobAmplitude=(-40, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85, phase=0.5)),
] + splash_rings("splash", [(120, 560, 12), (300, 530, 10), (480, 580, 14), (660, 545, 11), (840, 575, 12), (220, 590, 10)]) + [
    lightning("bolt", 560, 40, 230, interval=5.0, phase=0.2, seed=22),
    rain_layer("rain", 22, 90, 28, 1.3, 0.6, 260, col=(200, 220, 255)),
    rain_layer("rain_heavy", 23, 80, 36, 1.5, 0.7, 380, mask=W_(THUNDER), col=(200, 220, 255)),
    flash("flash", 5.0, 0.2, alpha=0.35),
]

L22_DIFFS = [
    ("sign", 120, 338, 42),
    ("hologram", 362, 196, 74),
    ("vending", 568, 428, 62),
    ("shutter", 800, 434, 102),
    ("antenna", 300, 224, 30),
    ("drone", 640, 152, 36),
    ("umbrella", 640, 424, 44),
]


# =================================================================== Level 23 rooftop (isometric, day/night + smog)
DN23 = day_night(40.0, tint=(0.32, 0.30, 0.55))
STEPS23 = [(CLEAR, 14), (FOG, 10), (OVERCAST, 8)]
FANS23 = [(2.2, 2.0), (3.6, 2.0)]
TANK23 = (7.4, 2.0)
DISH23 = (8.2, 6.4)
LINE23 = ((1.2, 6.2), (3.8, 8.6))


def l23_background(c, d):
    """天台都市 - static part"""
    c.gradient(0, 600, (120, 150, 205), (220, 180, 200))
    rnd = random.Random(23)
    for x in range(-30, 930, 46):
        h = rnd.randint(160, 360)
        piece(c, RRect(x, 600 - h, x + 40, 620, 1), (92, 100, 140), shadow=None)
    # the city far below: lower rooftops fill everything around our building
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (58, 60, 80), (66, 68, 90))
    draw_surround(c, L23_SURROUND, l23_decor, "back")
    # rooftop slab: the building continues below the picture
    top = iso_quad(0, 0, 10, 10)
    l0, l1, r0 = P(0, 10), P(10, 10), P(10, 0)
    left = Poly([l0, l1, (l1[0], 660), (l0[0], 660)])
    right = Poly([r0, l1, (l1[0], 660), (r0[0], 660)])
    piece(c, [top, left, right], (176, 176, 186), border=2, shadow=(6, 16, 20, 0.3))
    flat(c, left, (70, 72, 100))
    flat(c, right, (54, 56, 82))
    for k in range(1, 10):
        for a, b in ((P(k, 0), P(k, 10)), (P(0, k), P(10, k))):
            flat(c, Thick(a[0], a[1], b[0], b[1], 1), (164, 164, 174))
    # parapet along the back edges
    iso_box(c, 0, 0, 0, 10, 0.2, 0.3, (150, 150, 162), border=1.5)
    iso_box(c, 0, 0.2, 0, 0.2, 9.8, 0.3, (150, 150, 162), border=1.5)
    # helipad (marking colour differs)
    hx, hy = P(5.6, 5.8)
    ex = 1.6 * 36 * math.sqrt(2)
    flat(c, Ell(hx, hy, ex, ex / 2), (90, 92, 104))
    c.ellipse_ring(hx, hy, ex - 6, ex / 2 - 3, 3, (250, 250, 250))
    mark = (90, 220, 255) if "helipad" in d else (255, 210, 60)
    for a, b in ((P(5.2, 5.4), P(5.2, 6.2)), (P(6.0, 5.4), P(6.0, 6.2)), (P(5.2, 5.8), P(6.0, 5.8))):
        flat(c, Thick(a[0], a[1], b[0], b[1], 5), mark)
    # AC units (fans are elements)
    for X, Y in FANS23:
        iso_box(c, X - 0.5, Y - 0.5, 0, 1.0, 1.0, 0.6, (205, 205, 214))
    # water tank (colour differs)
    for lx, ly in ((-0.4, -0.4), (0.4, -0.4), (-0.4, 0.4), (0.4, 0.4)):
        a, b = P(TANK23[0] + lx, TANK23[1] + ly, 0), P(TANK23[0] + lx, TANK23[1] + ly, 0.6)
        piece(c, Thick(a[0], a[1], b[0], b[1], 3), (90, 90, 105), shadow=SMALL)
    iso_cyl(c, TANK23[0], TANK23[1], 0.6, 1.9, 0.65, (90, 170, 120) if "tank" in d else (200, 120, 80))
    # solar panels
    for X in (4.6, 5.5, 6.4):
        q = Poly([P(X, 2.4, 0.3), P(X + 0.8, 2.4, 0.3), P(X + 0.8, 3.4, 0.05), P(X, 3.4, 0.05)])
        piece(c, q, (40, 60, 120), border=1.5, border_col=(200, 200, 210), shadow=ISO_SH)
    # planters (one fewer in B)
    planters = [(1.0, 3.6), (1.0, 4.4)] + ([] if "planters" in d else [(1.0, 5.2)])
    for X, Y in planters:
        iso_box(c, X, Y, 0, 0.6, 0.6, 0.35, (150, 105, 75), border=1.5)
        px, py = P(X + 0.3, Y + 0.3, 0.35)
        piece(c, [Circ(px, py - 10, 10), Circ(px - 8, py - 4, 7), Circ(px + 8, py - 4, 7)], (90, 170, 90), shadow=SMALL)
    # dish stand, antenna, neon sign frame, laundry poles
    dx_, dy_ = P(*DISH23)
    piece(c, Thick(dx_, dy_, dx_, dy_ - 30, 4), (110, 110, 125), shadow=ISO_SH)
    ax, ay = P(9.0, 1.2)
    piece(c, [Thick(ax, ay, ax, ay - 120, 3), Thick(ax - 12, ay - 90, ax + 12, ay - 90, 2), Thick(ax - 8, ay - 108, ax + 8, ay - 108, 2)],
          (110, 110, 125), shadow=ISO_SH)
    sx0, sy0 = P(2.0, 9.6, 0.2)
    sx1, sy1 = P(7.6, 9.6, 0.2)
    piece(c, Poly([(sx0, sy0), (sx1, sy1), (sx1, sy1 - 48), (sx0, sy0 - 48)]), (36, 34, 56), border=1.5, shadow=ISO_SH)
    for (X, Y) in LINE23:
        a, b = P(X, Y), P(X, Y, 1.4)
        piece(c, Thick(a[0], a[1], b[0], b[1], 3), (120, 110, 120), shadow=ISO_SH)
    a, b = P(LINE23[0][0], LINE23[0][1], 1.4), P(LINE23[1][0], LINE23[1][1], 1.4)
    flat(c, Thick(a[0], a[1], b[0], b[1], 1.2), (230, 230, 235))
    from fill_iso import draw_surround
    draw_surround(c, L23_SURROUND, l23_decor, "front")


def l23_decor(c, X, Y, r):
    h = 1.5 + r * 3.5
    col = [(150, 150, 165), (120, 130, 160), (170, 160, 150), (110, 120, 140)][int(r * 40) % 4]
    iso_box(c, X - 0.7, Y - 0.7, -h - 1.0, 1.4, 1.4, h, col, border=1.2)
    if r > 0.5:
        iso_box(c, X - 0.2, Y - 0.2, -1.0, 0.4, 0.4, 0.3, (190, 190, 200), border=1)


def _l23_surround():
    from fill_iso import surround_points
    return surround_points(23, step=66, margin=0.9, keep=0.95)


L23_SURROUND = _l23_surround()


def l23_city_lights(c, m):
    """Windows of the lower rooftops light up at night."""
    rnd = random.Random(230)
    for X, Y, r in L23_SURROUND:
        h = 1.5 + r * 3.5
        for k in range(3):
            z = -1.0 - h + 0.3 + k * h / 3
            if rnd.random() < 0.6:
                a = P(X + 0.7, Y - 0.2, z)
                flat(c, RRect(a[0] - 3, a[1] - 3, a[0] + 3, a[1] + 3, 1), rnd.choice((YELLOW, CYAN, (255, 170, 220))) + (0.9,))


def _unused_city_lights(c, m):
    rnd = random.Random(230)
    for x in range(-30, 930, 46):
        for _ in range(14):
            y = rnd.uniform(250, 590)
            xx = x + rnd.uniform(4, 34)
            flat(c, RRect(xx, y, xx + 5, y + 6, 0.8), rnd.choice((YELLOW, CYAN, (255, 170, 220))) + (0.9,))


def l23_sign(c, m):
    sx0, sy0 = P(2.0, 9.6, 0.2)
    sx1, sy1 = P(7.6, 9.6, 0.2)
    n = 5
    for k in range(n):
        t0, t1 = (k + 0.15) / n, (k + 0.85) / n
        x0, y0 = sx0 + (sx1 - sx0) * t0, sy0 + (sy1 - sy0) * t0
        x1, y1 = sx0 + (sx1 - sx0) * t1, sy0 + (sy1 - sy0) * t1
        col = [MAGENTA, CYAN, YELLOW, MAGENTA, CYAN][k]
        neon(c, [Thick(x0, y0 - 10, x1, y1 - 10, 3), Thick(x0, y0 - 38, x1, y1 - 38, 3), Thick(x0, y0 - 10, x0, y0 - 38, 3),
                 Thick(x1, y1 - 24, x0, y0 - 24, 3)][: 2 + k % 3], col, spread=9)


def l23_fan(X, Y):
    def d(c, m):
        cx, cy = P(X, Y, 0.6)
        c.ellipse(cx, cy, 24, 12, (60, 62, 76))
        for k in range(4):
            a = math.radians(k * 90 + 20)
            flat(c, Poly([(cx, cy), (cx + 22 * math.cos(a), cy + 11 * math.sin(a)), (cx + 22 * math.cos(a + 0.6), cy + 11 * math.sin(a + 0.6))]),
                 (170, 172, 185))
        flat(c, Ell(cx, cy, 4, 2), (220, 220, 230))
    return d


def l23_dish(c, m):
    x, y = P(*DISH23)
    y -= 34
    piece(c, [Ell(x, y, 22, 26), Thick(x, y, x + 18, y - 4, 2)], (225, 228, 236), border=1.5, shadow=ISO_SH)
    flat(c, Ell(x + 3, y, 14, 18), (200, 204, 214))


def l23_beacon(c, m):
    ax, ay = P(9.0, 1.2)
    soft_union(c, [Circ(ax, ay - 122, 4)], (255, 60, 60), 0.8, spread=12)
    flat(c, Circ(ax, ay - 122, 3.5), (255, 120, 120))


def l23_drone(c, m):
    x, y = P(5.6, 5.8, 2.2)
    piece(c, [RRect(x - 16, y - 5, x + 16, y + 5, 3), Thick(x - 28, y - 8, x + 28, y - 8, 2), RRect(x - 8, y + 6, x + 8, y + 18, 2)],
          (80, 85, 110), border=1.2, border_col=CYAN, shadow=(8, 30, 6, 0.3))
    flat(c, RRect(x - 7, y + 7, x + 7, y + 17, 2), (220, 170, 110))


def l23_laundry(c, m):
    a, b = P(LINE23[0][0], LINE23[0][1], 1.4), P(LINE23[1][0], LINE23[1][1], 1.4)
    for i, t in enumerate((0.25, 0.55, 0.8)):
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        col = [(250, 120, 140), (120, 200, 250), (250, 230, 120)][i]
        if i == 1 and m:
            col = (150, 230, 140)
        piece(c, Poly([(x - 10, y), (x + 10, y), (x + 12, y + 8), (x + 7, y + 6), (x + 7, y + 22), (x - 7, y + 22), (x - 7, y + 6),
                       (x - 12, y + 8)]), col, border=1, shadow=SMALL)


def l23_flyer(c, m):
    piece(c, [RRect(100, 90, 150, 104, 6), Poly([(112, 90), (138, 90), (132, 80), (118, 80)])], (60, 64, 90), border=1.2,
          border_col=CYAN, shadow=None)
    soft_union(c, [RRect(40, 96, 98, 100, 2)], CYAN, 0.45, spread=6)


L23_ELEMENTS = [
    E("city_lights", l23_city_lights, daynight="night"),
    E("flyer", l23_flyer, daynight="untinted", anim=dict(drift_across(40, 150, 40), bobAmplitude=(0, 6), bobSpeed=0.3)),
] + [
    # fan blades: the second fan spins the other way in B
    E("fan%d" % i, l23_fan(X, Y), pivot=P(X, Y, 0.6), anim=dict(rotateSpeed=-240),
      animB=dict(rotateSpeed=240 if i == 1 else -240))
    for i, (X, Y) in enumerate(FANS23)
] + [
    E("dish", l23_dish, pivot=(P(*DISH23)[0], P(*DISH23)[1] - 34), anim=dict(spinSpeed=0.12, spinShade=0.3), animB={}),
    E("beacon", l23_beacon, daynight="untinted", anim=dict(blinkInterval=1.4, blinkDuration=0.5)),
    E("sign", l23_sign, daynight="night", anim=dict(twinkle=0.12, twinkleSpeed=2.0)),
    E("drone", l23_drone, show="A", pivot=P(5.6, 5.8, 2.2), anim=dict(bobAmplitude=(0, 10), bobSpeed=0.35, swingAngle=4, swingSpeed=0.3)),
    E("laundry", l23_laundry, variant=True, pivot=P(LINE23[0][0], LINE23[0][1], 1.4), anim=dict(swingAngle=2, swingSpeed=0.5)),
] + smoke("vent", *P(2.2, 2.0, 0.8), n=3, col=(235, 235, 240), r=6) + [
    fog_layer("smog1", 23, 200, 380, 0.5, 10, 1, col=(206, 214, 200)),
    fog_layer("smog2", 24, 380, 560, 0.55, 14, -1, col=(206, 214, 200)),
]

L23_DIFFS = [
    ("fan", int(P(*FANS23[1], 0.6)[0]), int(P(*FANS23[1], 0.6)[1]), 26),
    ("dish", int(P(*DISH23)[0] + 4), int(P(*DISH23)[1] - 34), 26),
    ("tank", int(P(*TANK23, 1.3)[0]), int(P(*TANK23, 1.3)[1]) - 4, 48),
    ("planters", int(P(1.3, 5.5, 0.3)[0]), int(P(1.3, 5.5, 0.3)[1] - 4), 38),
    ("drone", int(P(5.6, 5.8, 2.2)[0]) + 4, int(P(5.6, 5.8, 2.2)[1] + 14), 44),
    ("shirt", int(P(*LINE23[0], 1.4)[0] + (P(*LINE23[1], 1.4)[0] - P(*LINE23[0], 1.4)[0]) * 0.55),
     int(P(*LINE23[0], 1.4)[1] + (P(*LINE23[1], 1.4)[1] - P(*LINE23[0], 1.4)[1]) * 0.55 + 12), 16),
    ("helipad", int(P(5.6, 5.8)[0]), int(P(5.6, 5.8)[1]), 30),
]


# =================================================================== Level 24 neon crossroads (top-down)
STEPS24 = [(CLEAR, 10), (RAIN, 14), (THUNDER, 6), (RAIN, 6), (OVERCAST, 6)]
RX0, RX1, RY0, RY1 = 410, 490, 260, 340


def rooftop(c, x0, y0, x1, y1, col, seed):
    piece(c, RRect(x0, y0, x1, y1, 2), col, border=2, border_col=lit(col, 1.35), shadow=(6, 9, 9, 0.45))
    rnd = random.Random(seed)
    for _ in range(3):
        ax, ay = rnd.uniform(x0 + 14, x1 - 34), rnd.uniform(y0 + 14, y1 - 34)
        piece(c, RRect(ax, ay, ax + 20, ay + 20, 2), (150, 150, 165), shadow=(3, 5, 4, 0.4))
        flat(c, Circ(ax + 10, ay + 10, 6), (90, 92, 104))


def l24_background(c, d):
    """霓虹十字路口 - static part (seen from above)"""
    c.rect(0, 0, W, 660, (34, 32, 50))
    # sidewalks
    for r in ((0, 0, RX0, RY0), (RX1, 0, W, RY0), (0, RY1, RX0, H), (RX1, RY1, W, H)):
        flat(c, RRect(*r, 0), (62, 60, 84))
    # glowing lane lines
    for x in range(0, W, 60):
        if not (RX0 - 30 < x < RX1 + 10):
            neon(c, [Thick(x, 300, x + 30, 300, 2.5)], CYAN, glow_alpha=0.35, spread=6)
    for y in range(0, H, 60):
        if not (RY0 - 30 < y < RY1 + 10):
            neon(c, [Thick(450, y, 450, y + 30, 2.5)], YELLOW, glow_alpha=0.35, spread=6)
    # crosswalks (the east one is missing in B)
    walks = [("n", [(RX0 + 6 + k * 13, RY0 - 34, RX0 + 14 + k * 13, RY0 - 6) for k in range(6)]),
             ("e", [(RX1 + 6, RY0 + 6 + k * 13, RX1 + 34, RY0 + 14 + k * 13) for k in range(6)]),
             ("s", [(RX0 + 6 + k * 13, RY1 + 6, RX0 + 14 + k * 13, RY1 + 34) for k in range(6)])]
    for key, rects in walks:
        if key == "e" and "crosswalk" in d:
            continue
        flat(c, [RRect(*r, 1) for r in rects], (220, 220, 235))
    # rooftops (inset from the sidewalks)
    rooftop(c, 20, 20, 380, 230, (52, 46, 86), 1)
    rooftop(c, 520, 20, 880, 230, (48, 56, 90), 2)
    rooftop(c, 20, 370, 380, 580, (56, 48, 80), 3)
    rooftop(c, 520, 370, 880, 580, (44, 52, 84), 4)
    # rooftop pool (colour differs)
    pool = (255, 90, 200) if "pool" in d else (60, 220, 255)
    soft_union(c, [RRect(600, 420, 760, 520, 8)], pool, 0.4, spread=12)
    piece(c, RRect(600, 420, 760, 520, 8), lit(pool, 0.75), border=2, border_col=(230, 230, 240), shadow=None)
    for y in (450, 480):
        flat(c, Thick(606, y, 754, y, 1.4), lit(pool, 1.2))
    # helipad + garden
    c.ellipse_ring(200, 125, 60, 60, 4, (240, 240, 250))
    flat(c, [Thick(180, 100, 180, 150, 6), Thick(220, 100, 220, 150, 6), Thick(180, 125, 220, 125, 6)], (240, 240, 250))
    for x, y in ((80, 470), (110, 520), (150, 470), (300, 520), (320, 460)):
        piece(c, Circ(x, y, 16), (70, 150, 100), shadow=(4, 6, 6, 0.4))
    # billboard on a rooftop (missing in B)
    if "billboard" not in d:
        soft_union(c, [RRect(560, 60, 700, 110, 3)], MAGENTA, 0.45, spread=14)
        piece(c, RRect(560, 60, 700, 110, 3), (60, 20, 70), border=2, border_col=MAGENTA, shadow=(6, 9, 8, 0.45))
        neon(c, neon_glyphs(572, 70, 116, 30, 4, seed=24, width=3), MAGENTA, spread=8)
    # parked cars along the curb (one changes colour)
    for i, (x, y) in enumerate(((60, 246), (130, 246), (200, 246))):
        col = [(200, 60, 80), (60, 120, 220), (230, 200, 70)][i]
        if i == 1 and "car" in d:
            col = (120, 220, 120)
        piece(c, RRect(x - 24, y - 9, x + 24, y + 9, 5), col, border=1.5, shadow=(2, 3, 3, 0.4))
        flat(c, RRect(x - 10, y - 7, x + 8, y + 7, 3), lit(col, 0.6))


def l24_car(x, y, d, col):
    fx = 1 if d == "R" else -1 if d == "L" else 0
    fy = 1 if d == "D" else -1 if d == "U" else 0

    def draw(c, m):
        ax, ay = x + fx * 24, y + fy * 24
        c.polygon([(ax, ay), (ax + fx * 90 - fy * 26, ay + fy * 90 + fx * 26), (ax + fx * 90 + fy * 26, ay + fy * 90 - fx * 26)],
                  (255, 250, 210, 0.18))
        hw, hh = (24, 10) if fx else (10, 24)
        piece(c, RRect(x - hw, y - hh, x + hw, y + hh, 5), col, border=1.5, border_col=lit(col, 1.4), shadow=(2, 3, 3, 0.4))
        flat(c, RRect(x - hw * 0.45, y - hh * 0.6, x + hw * 0.45, y + hh * 0.6, 3), lit(col, 0.6))
        bx, by = x - fx * 24, y - fy * 24
        soft_union(c, [Circ(bx, by, 3)], (255, 40, 60), 0.7, spread=7)
    return draw


def l24_holo(c, m):
    x, y = 740, 125
    for k in range(3):
        a = math.radians(k * 120)
        neon(c, [Thick(x, y, x + 34 * math.cos(a), y + 34 * math.sin(a), 3)], CYAN, glow_alpha=0.4, spread=8)
    c.ellipse_ring(x, y, 40, 40, 2.5, CYAN + (0.8,))
    neon(c, [Circ(x, y, 6)], LIME, spread=8)


def l24_walker(x, y, col, col_b=None):
    def d(c, m):
        u = col_b if (m and col_b) else col
        soft_union(c, [Circ(x, y, 14)], u, 0.35, spread=8)
        piece(c, Circ(x, y, 14), lit(u, 0.8), border=1.5, border_col=u, shadow=(3, 5, 4, 0.4))
        flat(c, Circ(x, y, 3), (230, 230, 240))
    return d


def l24_sign(c, m):
    col = LIME if m else YELLOW
    neon(c, neon_glyphs(70, 420, 120, 26, 4, seed=7, width=3), col, spread=8)


def l24_drone(x, y):
    def d(c, m):
        piece(c, [RRect(x - 8, y - 8, x + 8, y + 8, 3)] + [Circ(x + sx * 12, y + sy * 12, 6) for sx in (-1, 1) for sy in (-1, 1)],
              (90, 95, 120), border=1, shadow=(10, 16, 4, 0.3))
        soft_union(c, [Circ(x, y, 2)], (255, 60, 60), 0.8, spread=6)
    return d


L24_ELEMENTS = [
    E("carE", l24_car(150, 314, "R", (230, 70, 110)), daynight="untinted", anim=drift_across(126, 174, 70)),
    E("carW", l24_car(700, 286, "L", (60, 160, 240)), daynight="untinted", anim=drift_across(676, 724, -55)),
    E("carS", l24_car(434, 120, "D", (250, 200, 70)), daynight="untinted",
      anim=dict(driftVelocity=(0, -60), driftLength=700, driftStart=-160, phase=160 / 700)),
    E("carN", l24_car(466, 480, "U", (120, 230, 140)), daynight="untinted",
      anim=dict(driftVelocity=(0, 50), driftLength=700, driftStart=-160, phase=160 / 700)),
    E("holo", l24_holo, pivot=(740, 125), daynight="untinted", anim=dict(rotateSpeed=50, twinkle=0.25, twinkleSpeed=1.4),
      animB=dict(rotateSpeed=-50, twinkle=0.25, twinkleSpeed=1.4)),
    E("roofsign", l24_sign, variant=True, daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=2.2)),
    E("walker1", l24_walker(RX0 + 30, RY0 - 20, MAGENTA), pivot=(RX0 + 30, RY0 - 20), daynight="untinted",
      anim=dict(bobAmplitude=(26, 0), bobSpeed=0.06)),
    E("walker2", l24_walker(RX0 + 22, RY1 + 20, CYAN, (255, 150, 60)), pivot=(RX0 + 22, RY1 + 20), variant=True, daynight="untinted",
      anim=dict(bobAmplitude=(24, 0), bobSpeed=0.05, phase=0.4)),
] + [
    E("drone%d" % i, l24_drone(x, y), pivot=(x, y), daynight="untinted",
      anim=dict(orbitRadius=(60, 40), orbitSpeed=0.06 * (1 if i else -1), phase=i * 0.5))
    for i, (x, y) in enumerate(((300, 120), (300, 470)))
] + splash_rings("ripple", [(200, 300, 9), (600, 320, 10), (450, 150, 8), (450, 480, 9), (80, 290, 8), (820, 300, 9), (440, 560, 8)]) + [
    rain_layer("rain", 24, 120, 10, 1.4, 0.7, 170, step=(24, 64), col=(200, 220, 255)),
    flash("flash", 4.6, 0.3, alpha=0.3),
]

L24_DIFFS = [
    ("pool", 680, 470, 98),
    ("crosswalk", RX1 + 20, 300, 44),
    ("billboard", 630, 85, 82),
    ("hologram", 740, 125, 42),
    ("umbrella", RX0 + 22, RY1 + 20, 26),
    ("car", 130, 246, 24),
    ("sign", 130, 433, 72),
]


LEVELS = [
    ("Level22", "霓虹雨街", l22_background, L22_ELEMENTS, L22_DIFFS, 140,
     opts(weather=dict(steps=STEPS22, blend=3.0, tints=NIGHT_TINTS), anim_seconds=36.0, frames=72)),
    ("Level23", "天台都市", l23_background, L23_ELEMENTS, L23_DIFFS, 140,
     opts(day_night=DN23, weather=dict(steps=STEPS23, blend=3.5, tints={FOG: (0.9, 0.94, 0.88)}))),
    ("Level24", "霓虹十字路口", l24_background, L24_ELEMENTS, L24_DIFFS, 140,
     opts(weather=dict(steps=STEPS24, blend=3.0, tints=NIGHT_TINTS), anim_seconds=42.0, frames=84)),
]
