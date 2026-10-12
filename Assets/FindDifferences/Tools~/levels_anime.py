# -*- coding: utf-8 -*-
"""
Japanese anime pack (cel shading: ink outlines, flat colour + shade band, light grain):
  Level25 樱花坂道 - side view: sloped street with cherry trees, weather: clear -> overcast -> rain -> overcast
  Level26 夏祭神社 - isometric shrine festival, day/night cycle with lanterns and fireworks at night
  Level27 仰望夏空 - worm's-eye view under a summer sky, weather: heat -> clear -> overcast -> shower -> clear
"""
import math
import random

from fdcore import CLEAR, E, H, HEAT, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, soft_union, star_pts
from levels_views import P, THICK, iso_quad
from stylekit import (INK, anime_post, cel, cel_flat, celestial, cumulus, day_night, drift_across, moon_element, smoke,
                      star_field, sun_element)
from weather import CLOUDY, WET, heat_haze, puddles, rain_layer, splash_rings, sun_glare

SAKURA, SAKURA_S = (255, 196, 214), (240, 150, 182)


def anime_opts(**kw):
    out = dict(post=anime_post, anim_seconds=40.0, frames=80)
    out.update(kw)
    return out


def anime_cloud(eid, x, y, k, mask, anim=None, base=(255, 255, 255), shade=(196, 210, 236)):
    def d(c, m):
        cumulus(c, x, y, k, base=base, shade=shade)
    return E(eid, d, anim=anim or dict(bobAmplitude=(16 * k, 0), bobSpeed=0.03), daynight="untinted", weather=mask)


# =================================================================== Level 25 sakura slope (side view)
STEPS25 = [(CLEAR, 14), (OVERCAST, 6), (RAIN, 10), (OVERCAST, 4)]


def slope_y(x):
    """Street surface rises to the right."""
    return 560 - (x / W) * 150


def l25_background(c, d):
    """樱花坂道 - static part"""
    c.gradient(0, 660, (88, 156, 236), (210, 232, 250))
    cumulus(c, 700, 130, 0.9)
    cumulus(c, 180, 190, 0.55)
    # houses up the slope (right side)
    for i, (x0, x1, wall, roof) in enumerate(((430, 560, (250, 244, 230), (80, 92, 120)), (580, 720, (240, 232, 214), (120, 90, 80)),
                                              (740, 900, (246, 240, 226), (70, 100, 110)))):
        base = slope_y((x0 + x1) / 2) - 40
        top = base - 120
        cel(c, RRect(x0, top, x1, base + 40, 1), wall)
        cel(c, Poly([(x0 - 14, top + 6), (x1 + 14, top + 6), (x1 - 10, top - 34), (x0 + 10, top - 34)]), roof)
        for k in range(1, 4):
            yy = top - 34 + k * 10
            flat(c, Thick(x0 + 10 - k * 3, yy, x1 - 10 + k * 3, yy, 1.4), lit(roof, 0.75))
        curtain = (240, 120, 150)
        if i == 1 and "curtain" in d:
            curtain = (120, 190, 240)
        cel_flat(c, RRect(x0 + 18, top + 22, x0 + 58, top + 60, 1), (200, 225, 245))
        flat(c, [RRect(x0 + 18, top + 22, x0 + 30, top + 60, 1), RRect(x0 + 46, top + 22, x0 + 58, top + 60, 1)], curtain)
        cel_flat(c, RRect(x1 - 52, top + 22, x1 - 18, top + 60, 1), (200, 225, 245))
    # block wall along the street
    pts = [(x, slope_y(x) - 46) for x in range(0, 920, 20)]
    cel(c, Poly(pts + [(920, slope_y(920) - 8), (0, slope_y(0) - 8)]), (205, 200, 196))
    for x in range(0, 920, 40):
        flat(c, Thick(x, slope_y(x) - 46, x, slope_y(x) - 8, 1.2), (175, 170, 168))
    # utility poles + wires
    poles = [(120, slope_y(120)), (520, slope_y(520)), (860, slope_y(860))]
    for x, b in poles:
        cel(c, [RRect(x - 7, b - 300, x + 7, b, 2), RRect(x - 34, b - 280, x + 34, b - 272, 2)], (150, 150, 160))
        if x == 520:
            cel(c, RRect(x + 8, b - 240, x + 30, b - 206, 3), (130, 140, 150))
    for k in range(3):
        for (x0, b0), (x1, b1) in zip(poles, poles[1:]):
            y0, y1 = b0 - 278 + k * 4, b1 - 278 + k * 4
            pts = [(x0 + (x1 - x0) * t / 10, y0 + (y1 - y0) * t / 10 + 18 * math.sin(math.pi * t / 10)) for t in range(11)]
            flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.3) for i in range(10)], INK)
    # street
    road = Poly([(0, slope_y(0) - 8)] + [(x, slope_y(x) - 8) for x in range(0, 920, 40)] + [(920, H + 20), (0, H + 20)])
    cel_flat(c, road, (150, 150, 162))
    for x in range(20, 900, 90):
        flat(c, Thick(x, slope_y(x) + 30, x + 40, slope_y(x + 40) + 30, 3), (245, 245, 245))
    # vending machine (colour differs) and mailbox (missing in B)
    vm = (70, 120, 220) if "vending" in d else (220, 60, 70)
    vb = slope_y(360) - 8
    cel(c, RRect(330, vb - 96, 390, vb, 3), vm)
    cel_flat(c, RRect(336, vb - 88, 384, vb - 46, 2), (235, 245, 255))
    for k in range(4):
        flat(c, RRect(340 + k * 11, vb - 82, 347 + k * 11, vb - 52, 1), [(255, 120, 120), (120, 200, 255), (255, 220, 110), (150, 230, 150)][k])
    if "mailbox" not in d:
        mb = slope_y(420) - 8
        cel(c, [RRect(406, mb - 66, 434, mb - 20, 4), RRect(416, mb - 20, 424, mb, 1)], (225, 50, 50))
        flat(c, RRect(410, mb - 56, 430, mb - 52, 1), INK)
    # bicycle
    bx, bb = 250, slope_y(250) - 8
    for wx in (bx - 26, bx + 26):
        c.ellipse_ring(wx, bb - 18, 18, 18, 2.5, INK)
    flat(c, [Thick(bx - 26, bb - 18, bx, bb - 40, 2.5), Thick(bx, bb - 40, bx + 26, bb - 18, 2.5), Thick(bx - 26, bb - 18, bx + 6, bb - 18, 2.5),
             Thick(bx, bb - 40, bx - 4, bb - 50, 2.5), Thick(bx + 18, bb - 46, bx + 26, bb - 18, 2.5)], (80, 140, 200))
    cel_flat(c, RRect(bx + 14, bb - 56, bx + 34, bb - 44, 2), (200, 170, 120) if "basket" not in d else (90, 150, 210))
    # cherry trees (the cluster on the right tree is missing in B)
    for x, s in ((70, 1.1), (260, 0.9)):
        b = slope_y(x) - 40
        cel(c, [Poly([(x - 10 * s, b), (x + 10 * s, b), (x + 6 * s, b - 120 * s), (x - 6 * s, b - 120 * s)]),
                Thick(x, b - 90 * s, x + 50 * s, b - 150 * s, 7 * s), Thick(x, b - 100 * s, x - 46 * s, b - 160 * s, 7 * s)], (110, 76, 70))
        clusters = [(x, b - 170 * s, 60 * s), (x - 52 * s, b - 150 * s, 44 * s), (x + 56 * s, b - 150 * s, 46 * s), (x + 20 * s, b - 210 * s, 40 * s)]
        if x == 260 and "sakura" in d:
            clusters = clusters[:2] + clusters[3:]
        cel(c, [Circ(cx, cy, r) for cx, cy, r in clusters], SAKURA, shade=SAKURA_S, highlight=(255, 226, 236))


def l25_petal(x, y):
    def d(c, m):
        cel_flat(c, Poly([(x - 5, y), (x, y - 3), (x + 5, y), (x, y + 3)]), SAKURA, w=1.0)
    return d


def l25_cat(c, m):
    x, b = 640, slope_y(640) - 46
    cel(c, [Ell(x, b - 12, 18, 11), Circ(x + 16, b - 22, 9), Poly([(x + 10, b - 28), (x + 12, b - 38), (x + 18, b - 30)]),
            Poly([(x + 18, b - 30), (x + 24, b - 38), (x + 25, b - 27)])], (245, 240, 235))
    flat(c, [Thick(x + 13, b - 22, x + 16, b - 21, 1.2), Thick(x + 19, b - 21, x + 22, b - 22, 1.2)], INK)


def l25_tail(c, m):
    x, b = 640, slope_y(640) - 46
    cel(c, [Thick(x - 16, b - 10, x - 30, b - 2, 4), Thick(x - 30, b - 2, x - 34, b + 14, 4)], (245, 240, 235), w=1.6)


def l25_crow(c, m):
    x, y = 540, slope_y(520) - 286
    cel(c, [Ell(x, y, 11, 7), Circ(x + 10, y - 6, 5), Poly([(x - 8, y), (x - 20, y + 4), (x - 8, y + 4)])], (50, 50, 66), w=1.4)
    flat(c, Poly([(x + 14, y - 6), (x + 20, y - 5), (x + 14, y - 3)]), (90, 90, 100))


L25_ELEMENTS = [
    anime_cloud("cloud_g1", 200, 90, 0.8, CLOUDY, base=(214, 218, 230), shade=(170, 176, 196)),
    anime_cloud("cloud_g2", 560, 70, 1.0, CLOUDY, base=(214, 218, 230), shade=(170, 176, 196)),
    anime_cloud("cloud_g3", 860, 110, 0.7, CLOUDY, base=(214, 218, 230), shade=(170, 176, 196)),
    E("crow", l25_crow, show="A", pivot=(540, slope_y(520) - 282), anim=dict(swingAngle=10, swingSpeed=0.4)),
    E("cat", l25_cat),
    E("tail", l25_tail, pivot=(624, slope_y(640) - 56), anim=dict(swingAngle=16, swingSpeed=0.45), animB={}),
] + [
    E("petal%d" % i, l25_petal(x, y), pivot=(x, y),
      anim=dict(driftVelocity=(26, -22), driftLength=520, driftFade=True, rotateSpeed=90 + 15 * i, spinSpeed=0.6, spinShade=0.3,
                bobAmplitude=(10, 6), bobSpeed=0.5, phase=i / 10))
    for i, (x, y) in enumerate(((40, 60), (120, 30), (200, 80), (90, 140), (260, 40), (30, 200), (180, 170), (300, 120), (60, 90), (230, 10)))
] + [
    puddles("puddles", [Ell(200, slope_y(200) + 20, 50, 7), Ell(520, slope_y(520) + 40, 60, 8), Ell(760, slope_y(760) + 24, 44, 6)]),
] + splash_rings("splash", [(200, slope_y(200) + 20, 9), (520, slope_y(520) + 40, 10), (760, slope_y(760) + 24, 8), (380, slope_y(380) + 50, 8)]) + [
    rain_layer("rain", 25, 80, 26, 1.3, 0.7, 250),
]

L25_DIFFS = [
    ("vending", 360, int(slope_y(360) - 52), 58),
    ("tail", 612, int(slope_y(640) - 44), 22),
    ("sakura", int(260 + 56 * 0.9), int(slope_y(260) - 40 - 150 * 0.9), 40),
    ("curtain", 618, int(slope_y(650) - 40 - 120 + 41), 24),
    ("mailbox", 420, int(slope_y(420) - 40), 40),
    ("basket", 274, int(slope_y(250) - 58), 16),
    ("crow", 542, int(slope_y(520) - 288), 18),
]


# =================================================================== Level 26 shrine festival (isometric, day/night)
DN26 = day_night(40.0, tint=(0.36, 0.30, 0.58))
SUN26, MOON26 = celestial((450, 160), (400, 110), 40.0)


def iso_box_cel(c, X, Y, Z, dx, dy, dz, col):
    top = Poly([P(X, Y, Z + dz), P(X + dx, Y, Z + dz), P(X + dx, Y + dy, Z + dz), P(X, Y + dy, Z + dz)])
    left = Poly([P(X, Y + dy, Z + dz), P(X + dx, Y + dy, Z + dz), P(X + dx, Y + dy, Z), P(X, Y + dy, Z)])
    right = Poly([P(X + dx, Y, Z + dz), P(X + dx, Y + dy, Z + dz), P(X + dx, Y + dy, Z), P(X + dx, Y, Z)])
    for s in (top, left, right):
        s.draw(c, INK, 2.0)
    flat(c, top, lit(col, 1.12))
    flat(c, left, col)
    flat(c, right, lit(col, 0.74))
    return top, left, right


def iso_roof_cel(c, X, Y, Z, dx, dy, h, col, overhang=0.25):
    X, Y, dx, dy = X - overhang, Y - overhang, dx + 2 * overhang, dy + 2 * overhang
    m = Y + dy / 2
    back = Poly([P(X, Y, Z), P(X + dx, Y, Z), P(X + dx, m, Z + h), P(X, m, Z + h)])
    front = Poly([P(X, m, Z + h), P(X + dx, m, Z + h), P(X + dx, Y + dy, Z), P(X, Y + dy, Z)])
    gable = Poly([P(X + dx, Y, Z), P(X + dx, Y + dy, Z), P(X + dx, m, Z + h)])
    for s in (back, front, gable):
        s.draw(c, INK, 2.0)
    flat(c, back, lit(col, 1.18))
    flat(c, front, col)
    flat(c, gable, lit(col, 0.7))
    a, b = P(X, m, Z + h), P(X + dx, m, Z + h)
    flat(c, Thick(a[0], a[1] - 2, b[0], b[1] - 2, 5), lit(col, 0.6))


def stone_lantern(c, X, Y):
    x, y = P(X, Y)
    cel(c, [RRect(x - 10, y - 12, x + 10, y, 2), RRect(x - 4, y - 34, x + 4, y - 12, 1), RRect(x - 12, y - 48, x + 12, y - 34, 2),
            Poly([(x - 16, y - 48), (x + 16, y - 48), (x, y - 62)])], (190, 186, 178), w=1.6)
    flat(c, RRect(x - 6, y - 45, x + 6, y - 37, 1), (255, 220, 140))


def l26_decor(c, X, Y, r):
    x, y = P(X, Y)
    if r < 0.6:
        s = 0.8 + 0.4 * r
        cel(c, Thick(x, y, x, y - 30 * s, 7 * s), (120, 85, 70), w=1.6)
        cel(c, [Circ(x, y - 50 * s, 24 * s), Circ(x - 16 * s, y - 38 * s, 16 * s), Circ(x + 16 * s, y - 38 * s, 16 * s)],
            (80 + int(30 * r), 160, 90))
    elif r < 0.75:
        for k in range(4):
            cel(c, Thick(x + k * 6 - 9, y, x + k * 6 - 9, y - 70 - k * 6, 4), (120, 180, 110), w=1.2)
    elif r < 0.88:
        stone_lantern(c, X, Y)
    else:
        cel(c, [Circ(x - 8, y - 8, 9), Circ(x + 6, y - 10, 10)], (100, 170, 100), w=1.4)


def _l26_surround():
    from fill_iso import surround_points
    return surround_points(26, step=64)


L26_SURROUND = _l26_surround()
LANTERN_LINE = (P(0.3, 3.0, 1.8), P(2.8, 0.5, 1.8))     # along the back-left edge, clear of other differences
POOL26 = (6.6, 6.6)
BELL26 = P(4.4, 2.6, 1.3)


def l26_background(c, d):
    """夏祭神社 - static part"""
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (118, 184, 102), None)
    top = iso_quad(0, 0, 10, 10)
    top.draw(c, INK, 2.0)
    flat(c, top, (130, 196, 110))
    for q in (iso_quad(4.2, 10, 5.4, 26),):
        cel_flat(c, q, (214, 208, 196), w=1.5)
    draw_surround(c, L26_SURROUND, l26_decor, "back")
    # stone path
    for q in (iso_quad(4.2, 3.6, 5.4, 10), iso_quad(2.6, 2.6, 7.0, 3.6)):
        cel_flat(c, q, (214, 208, 196), w=1.5)
    for k in range(4, 10):
        a, b = P(4.2, k), P(5.4, k)
        flat(c, Thick(a[0], a[1], b[0], b[1], 1.2), (180, 174, 162))
    # shrine
    iso_box_cel(c, 3.0, 0.6, 0, 3.2, 2.0, 1.1, (236, 226, 206))
    for t in (0.0, 0.33, 0.66, 1.0):
        a, b = P(3.0 + 3.2 * t, 2.6, 0), P(3.0 + 3.2 * t, 2.6, 1.1)
        flat(c, Thick(a[0], a[1], b[0], b[1], 4), (200, 60, 50))
    iso_roof_cel(c, 3.0, 0.6, 1.1, 3.2, 2.0, 0.9, (60, 90, 80))
    # offering box + bell frame
    iso_box_cel(c, 4.2, 2.6, 0, 0.8, 0.4, 0.4, (150, 100, 70))
    bx, by = BELL26
    flat(c, Thick(bx - 20, by - 40, bx + 20, by - 40, 3), INK)
    # torii (front)
    for X in (4.0, 5.6):
        a, b = P(X, 8.6), P(X, 8.6, 2.0)
        cel(c, Thick(a[0], a[1], b[0], b[1], 8), (215, 60, 50), w=1.8)
    for z, ext in ((2.0, 0.5), (1.6, 0.1)):
        a, b = P(4.0 - ext, 8.6, z), P(5.6 + ext, 8.6, z)
        cel(c, Thick(a[0], a[1], b[0], b[1], 7 if z == 2.0 else 5), (40, 36, 40) if z == 2.0 else (215, 60, 50), w=1.8)
    plaque = (60, 140, 90) if "plaque" in d else (30, 30, 40)
    px, py = P(4.8, 8.6, 1.8)
    cel_flat(c, RRect(px - 8, py - 8, px + 8, py + 8, 1), plaque, w=1.5)
    # stone lanterns (one missing in B)
    for X, Y in ((3.4, 4.4), (6.2, 4.4), (3.4, 7.0), (6.2, 7.0)):
        if (X, Y) == (6.2, 7.0) and "lantern" in d:
            continue
        stone_lantern(c, X, Y)
    # festival stalls (awning colour differs on the second)
    for i, (X, Y) in enumerate(((1.0, 4.0), (1.4, 7.2), (7.6, 3.6))):
        iso_box_cel(c, X, Y, 0, 1.2, 0.8, 0.5, (190, 150, 110))
        col = [(230, 70, 70), (70, 130, 220), (250, 190, 70)][i]
        if i == 1 and "awning" in d:
            col = (120, 200, 120)
        iso_roof_cel(c, X, Y, 1.2, 1.2, 0.8, 0.3, col, overhang=0.1)
        for px_, py_ in ((X, Y + 0.8), (X + 1.2, Y + 0.8)):
            a, b = P(px_, py_, 0.5), P(px_, py_, 1.2)
            flat(c, Thick(a[0], a[1], b[0], b[1], 2.5), INK)
    # goldfish pool
    gx, gy = P(*POOL26)
    ex = 1.1 * 36 * math.sqrt(2)
    cel_flat(c, Ell(gx, gy, ex, ex / 2), (90, 170, 220), w=3)
    flat(c, Ell(gx - 10, gy - 4, ex * 0.4, ex * 0.12), (150, 210, 240))
    # ema boards (one fewer in B)
    for k in range(3 if "ema" in d else 4):
        x, y = P(2.0 + k * 0.32, 3.1, 0.8)        # in the open, not hidden by trees
        cel_flat(c, Poly([(x - 7, y), (x + 7, y), (x + 7, y - 9), (x, y - 14), (x - 7, y - 9)]), (230, 200, 150), w=1.2)
    # lantern string poles
    for (x, y) in LANTERN_LINE:
        cel(c, Thick(x, y, x, y + 60, 3), (120, 90, 70), w=1.2)
    # trees
    for X, Y, s in ((0.6, 0.8, 1.0), (9.0, 1.0, 1.1), (9.2, 5.8, 1.0), (0.6, 9.0, 0.9), (8.8, 8.8, 1.0)):
        x, y = P(X, Y)
        cel(c, Thick(x, y, x, y - 30 * s, 7 * s), (120, 85, 70), w=1.6)
        cel(c, [Circ(x, y - 50 * s, 24 * s), Circ(x - 16 * s, y - 38 * s, 16 * s), Circ(x + 16 * s, y - 38 * s, 16 * s)], (90, 170, 90))
    from fill_iso import draw_surround
    draw_surround(c, L26_SURROUND, l26_decor, "front")


def l26_lanterns(c, m):
    (x0, y0), (x1, y1) = LANTERN_LINE
    pts = [(x0 + (x1 - x0) * t / 10, y0 + (y1 - y0) * t / 10 + 14 * math.sin(math.pi * t / 10)) for t in range(11)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(10)], INK)
    for i, (x, y) in enumerate(pts[1:-1]):
        col = ((70, 130, 220) if m else (230, 60, 60)) if i % 2 == 0 else (255, 250, 240)
        cel(c, Ell(x, y + 10, 7, 9), col, w=1.4)


def l26_lantern_glow(c, m):
    (x0, y0), (x1, y1) = LANTERN_LINE
    pts = [(x0 + (x1 - x0) * t / 10, y0 + (y1 - y0) * t / 10 + 14 * math.sin(math.pi * t / 10)) for t in range(1, 10)]
    soft_union(c, [Circ(x, y + 10, 6) for x, y in pts], (255, 200, 120), 0.6, spread=16)
    for i, x in enumerate((P(1.6, 4.4, 1.0), P(2.0, 7.6, 1.0), P(8.2, 4.0, 1.0))):
        soft_union(c, [Circ(x[0], x[1], 10)], (255, 210, 140), 0.5, spread=24)


def l26_fish(i):
    gx, gy = P(*POOL26)

    def d(c, m):
        cel_flat(c, [Ell(gx, gy, 7, 3.5), Poly([(gx - 6, gy), (gx - 13, gy - 4), (gx - 13, gy + 4)])], (255, 120, 40), w=1.0)
    return d


def l26_rope(c, m):
    x, y = BELL26
    cel(c, Ell(x, y - 40, 7, 6), (220, 180, 70), w=1.4)
    flat(c, Thick(x, y - 34, x, y, 3), (230, 60, 60))
    flat(c, Thick(x + 2, y - 34, x + 2, y, 1.4), (250, 250, 250))


def l26_firework(x, y, col, n=14):
    def d(c, m):
        shapes = [Thick(x + 8 * math.cos(a), y + 8 * math.sin(a), x + 30 * math.cos(a), y + 30 * math.sin(a), 2.4)
                  for a in (2 * math.pi * k / n for k in range(n))]
        soft_union(c, shapes, col, 0.6, spread=8)
        flat(c, shapes, lit(col, 1.2))
    return d


L26_ELEMENTS = [
] + [
    E("firework%d" % i, l26_firework(x, y, col), pivot=(x, y), daynight="night",
      anim=dict(driftVelocity=(0, -2), driftLength=6, driftFade=True, driftGrow=2.2, phase=ph))
    for i, (x, y, col, ph) in enumerate(((260, 120, (255, 120, 160), 0.0), (650, 90, (120, 220, 255), 0.35), (480, 60, (255, 220, 100), 0.7)))
] + [
    E("rope", l26_rope, pivot=(BELL26[0], BELL26[1] - 40), anim=dict(swingAngle=14, swingSpeed=0.5), animB={}),
] + [
    E("fish%d" % i, l26_fish(i), pivot=P(*POOL26),
      anim=dict(orbitRadius=(22 + 12 * i, 10 + 6 * i), orbitSpeed=0.15 + 0.03 * i, orbitAlign=True, phase=i * 0.33),
      animB=dict(orbitRadius=(22 + 12 * i, 10 + 6 * i), orbitSpeed=-(0.15 + 0.03 * i) if i == 0 else 0.15 + 0.03 * i,
                 orbitAlign=True, phase=i * 0.33))
    for i in range(3)
] + [
    E("lanterns", l26_lanterns, variant=True, anim=dict(swingAngle=1, swingSpeed=0.3), pivot=LANTERN_LINE[0]),
    E("lantern_glow", l26_lantern_glow, daynight="night", anim=dict(twinkle=0.15, twinkleSpeed=1.0)),
] + smoke("smoke", *P(1.6, 4.2, 1.6), n=3, col=(245, 245, 245), r=6)

_llx = (LANTERN_LINE[0][0] + LANTERN_LINE[1][0]) / 2
_lly = (LANTERN_LINE[0][1] + LANTERN_LINE[1][1]) / 2 + 24
L26_DIFFS = [
    ("lanterns", int(_llx), int(_lly), 98),
    ("goldfish", int(P(*POOL26)[0]), int(P(*POOL26)[1]), 36),
    ("awning", int(P(2.0, 7.6, 1.4)[0]), int(P(2.0, 7.6, 1.4)[1]), 48),
    ("lantern", int(P(6.2, 7.0)[0]), int(P(6.2, 7.0)[1] - 34), 32),
    ("rope", int(BELL26[0]), int(BELL26[1] - 22), 20),
    ("ema", int(P(2.96, 3.1, 0.8)[0]), int(P(2.96, 3.1, 0.8)[1] - 7), 20),
    ("plaque", int(P(4.8, 8.6, 1.8)[0]), int(P(4.8, 8.6, 1.8)[1]), 14),
]


# =================================================================== Level 27 summer sky (worm's-eye)
STEPS27 = [(HEAT, 14), (CLEAR, 6), (OVERCAST, 6), (RAIN, 8), (CLEAR, 6)]
VP27 = (450.0, 300.0)
POLE_ANGLES = [215, 325, 105]


def polar27(r, a):
    return (VP27[0] + r * math.cos(math.radians(a)), VP27[1] + r * math.sin(math.radians(a)))


def l27_background(c, d):
    """仰望夏空 - static part"""
    c.rect(0, 0, W, 660, (120, 186, 245))
    for r, col in ((440, (140, 200, 248)), (330, (110, 176, 240)), (220, (84, 152, 232)), (120, (64, 132, 222))):
        flat(c, Circ(*VP27, r), col)
    # towering clouds rising from the edges
    cumulus(c, 120, 520, 1.2)
    cumulus(c, 800, 90, 1.0)
    if "cloud" not in d:
        cumulus(c, 820, 560, 0.9)
    # sunflowers and leaves framing the bottom corners
    for x, y, r in ((60, 590, 60), (190, 640, 50), (840, 620, 56)):
        cel(c, [Ell(x - r, y - 10, r * 0.9, r * 0.35), Ell(x + r, y - 4, r * 0.8, r * 0.3)], (90, 170, 80))


def l27_poles(c, d):
    """Utility poles converge on the zenith; wires between them. An element so passing clouds stay behind it."""
    tips = []
    for i, a in enumerate(POLE_ANGLES):
        base_l, base_r = polar27(700, a - 4), polar27(700, a + 4)
        tip_l, tip_r = polar27(150, a - 1.6), polar27(150, a + 1.6)
        cel(c, Poly([base_l, tip_l, tip_r, base_r]), (150, 150, 162), w=2)
        tip = polar27(165, a)
        tips.append(tip)
        cross_a, cross_b = polar27(205, a - 9), polar27(205, a + 9)
        cel(c, Thick(cross_a[0], cross_a[1], cross_b[0], cross_b[1], 7), (140, 140, 150), w=1.6)
        if i == 1:
            tr = polar27(250, a + 5)
            col = (90, 160, 120) if "transformer" in d else (120, 130, 145)
            cel(c, Circ(tr[0], tr[1], 20), col, w=2)
    for k in (-8, 0, 8):
        ends = [polar27(205, a + k) for a in POLE_ANGLES]
        for (x0, y0), (x1, y1) in ((ends[0], ends[1]), (ends[1], ends[2]), (ends[2], ends[0])):
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            sx, sy = (mx - VP27[0]) * 0.12, (my - VP27[1]) * 0.12
            pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * (mx + sx) + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (my + sy) + t * t * y1)
                   for t in (j / 16 for j in range(17))]
            flat(c, [Thick(pts[j][0], pts[j][1], pts[j + 1][0], pts[j + 1][1], 1.4) for j in range(16)], INK)
    # birds on the wire (two in B)
    ends = [polar27(205, a) for a in POLE_ANGLES]
    birds = [0.3, 0.45, 0.6] if "birds" not in d else [0.3, 0.6]
    for t in birds:
        x = ends[0][0] + (ends[1][0] - ends[0][0]) * t
        y = ends[0][1] + (ends[1][1] - ends[0][1]) * t + 8
        cel(c, [Ell(x, y + 7, 6, 8), Circ(x, y - 2, 4.5)], (60, 60, 75), w=1.2)


def l27_sunflower(x, y, r, variant):
    def d(c, m):
        petal = (250, 150, 60) if (m and variant) else (255, 210, 50)
        cel(c, Poly(star_pts(x, y, r, r * 0.62, points=14)), petal, w=2)
        cel(c, Circ(x, y, r * 0.45), (120, 80, 50), w=1.6)
        for k in range(6):
            a = math.radians(k * 60)
            flat(c, Circ(x + r * 0.22 * math.cos(a), y + r * 0.22 * math.sin(a), r * 0.06), (90, 58, 38))
    return d


def l27_plane(c, m):
    col = (90, 150, 230) if m else (240, 240, 245)
    x, y = 520, 210
    flat(c, Thick(240, 270, x - 30, y + 6, 4), (255, 255, 255, 0.75))
    cel(c, [Ell(x, y, 26, 5), Poly([(x - 4, y), (x - 14, y - 22), (x + 4, y)]), Poly([(x - 4, y), (x - 14, y + 22), (x + 4, y)]),
            Poly([(x - 22, y), (x - 30, y - 9), (x - 18, y)])], col, w=1.4)


def l27_dragonfly(c, m):
    x, y = 300, 400
    cel(c, Ell(x, y, 16, 2.5), (60, 140, 120), w=1.0)
    for sy in (-1, 1):
        flat(c, [Ell(x + 3, y + sy * 8, 4, 8), Ell(x - 4, y + sy * 7, 3.5, 7)], (220, 240, 255, 0.7))
    flat(c, Circ(x + 14, y, 3), (60, 140, 120))


def l27_chime(c, m):
    x, y = 110, 20
    flat(c, Thick(x, -10, x, y, 1.2), INK)
    cel(c, Ell(x, y + 12, 14, 13), (230, 245, 255), w=1.6)
    flat(c, [Thick(x - 8, y + 10, x + 8, y + 10, 2)], (230, 80, 80))
    flat(c, Thick(x, y + 24, x, y + 44, 1), INK)
    cel_flat(c, RRect(x - 6, y + 44, x + 6, y + 66, 1), (250, 245, 230), w=1.2)


def l27_drop(a):
    def d(c, m):
        x, y = polar27(70, a)
        cel_flat(c, [Circ(x, y, 3.5), Poly([(x - 3, y - 1), (x + 3, y - 1), (x, y - 9)])], (215, 235, 255), w=1.0)
    return d


def outward27(a, speed, length):
    ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
    return dict(driftVelocity=(ux * speed, -uy * speed), driftLength=length, driftFade=True, driftGrow=3.0)


L27_ELEMENTS = [
    sun_glare("glare", 700, 70, 280, mask=W_(HEAT, CLEAR)),
    E("plane", l27_plane, pivot=(520, 210), variant=True, anim=dict(bobAmplitude=(10, 4), bobSpeed=0.06), daynight="untinted"),
    anime_cloud("cloud_o1", 330, 250, 1.2, CLOUDY, base=(214, 218, 230), shade=(160, 168, 190)),
    anime_cloud("cloud_o2", 600, 360, 1.0, CLOUDY, base=(214, 218, 230), shade=(160, 168, 190)),
    E("poles", lambda c, m: l27_poles(c, {"birds", "transformer"} if m else set()), variant=True),
    E("dragonfly", l27_dragonfly, show="A", pivot=(300, 400),
      anim=dict(orbitRadius=(60, 36), orbitSpeed=0.12, orbitAlign=True, stretch=(0, 0.3), scaleSpeed=6)),
    E("chime", l27_chime, pivot=(110, -10), anim=dict(swingAngle=10, swingSpeed=0.35), animB={}),
    E("sunflower1", l27_sunflower(70, 560, 56, False), pivot=(70, 560), anim=dict(swingAngle=3, swingSpeed=0.2)),
    E("sunflower2", l27_sunflower(200, 610, 46, True), pivot=(200, 610), variant=True, anim=dict(swingAngle=4, swingSpeed=0.25, phase=0.3)),
    E("sunflower3", l27_sunflower(845, 590, 52, False), pivot=(845, 590), anim=dict(swingAngle=3, swingSpeed=0.22, phase=0.6)),
] + [heat_haze("haze%d" % i, y, phase=i * 0.3) for i, y in enumerate((150, 330, 500))] + [
    # rain seen from below: drops fall towards the camera, i.e. fly outwards from the zenith and grow
    E("drop%d" % i, l27_drop(a), pivot=polar27(70, a), daynight="untinted", weather=W_(RAIN),
      anim=dict(outward27(a, 180, 300), phase=(i * 0.37) % 1))
    for i, a in enumerate(range(0, 360, 24))
]

_e0, _e1 = polar27(205, POLE_ANGLES[0]), polar27(205, POLE_ANGLES[1])
L27_DIFFS = [
    ("plane", 516, 210, 32),
    ("birds", int(_e0[0] + (_e1[0] - _e0[0]) * 0.45), int(_e0[1] + (_e1[1] - _e0[1]) * 0.45 + 10), 16),
    ("sunflower", 200, 610, 44),
    ("transformer", int(polar27(250, POLE_ANGLES[1] + 5)[0]), int(polar27(250, POLE_ANGLES[1] + 5)[1]), 24),
    ("dragonfly", 300, 400, 70),
    ("chime", 110, 50, 30),
    ("cloud", 792, 540, 124),
]


LEVELS = [
    ("Level25", "樱花坂道", l25_background, L25_ELEMENTS, L25_DIFFS, 140,
     anime_opts(weather=dict(steps=STEPS25, blend=3.0), anim_seconds=34.0, frames=68)),
    ("Level26", "夏祭神社", l26_background, L26_ELEMENTS, L26_DIFFS, 140, anime_opts(day_night=DN26)),
    ("Level27", "仰望夏空", l27_background, L27_ELEMENTS, L27_DIFFS, 140,
     anime_opts(weather=dict(steps=STEPS27, blend=3.0), anim_seconds=40.0, frames=80)),
]
