# -*- coding: utf-8 -*-
"""Heian-period Japan (794-1185), paper-craft side views in a yamato-e mood (gold mist bands, cypress-bark roofs,
bamboo blinds, layered court robes), full-bleed:
  Level74 寝殿庭园 - a shinden-zukuri mansion in spring: pond, arched bridge, court ladies, kemari players, falling petals
  Level75 葵祭     - the Aoi festival procession before the Suzaku gate: ox carriage hung with wisteria, riders, parasols
  Level76 月夜舟游 - an autumn boating party: dragon- and heron-headed boats with musicians, a great drum; day / night
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, drift_across, gy, layer, sky
from stylekit import day_night, star_field, window_glow
from levels_europe import ellipse_top

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
GOLD = (238, 206, 130)
VERMILION = (206, 72, 50)
ROOF = (104, 82, 72)
BLIND = (206, 192, 128)
HAIR = (26, 22, 26)


# ------------------------------------------------------------------- props
def kasumi(c, y, x0, x1, h=22, col=GOLD):
    """Yamato-e gold mist band."""
    shapes = [RRect(x0, y - h / 2, x1, y + h / 2, h / 2)]
    for k in range(int((x1 - x0) // 90)):
        shapes.append(RRect(x0 + 30 + k * 90, y - h * 0.9, x0 + 90 + k * 90, y, h / 2))
    piece(c, shapes, col, shadow=SMALL)
    flat(c, RRect(x0 + 10, y - 2, x1 - 10, y + 2, 2), lit(col, 1.08))


def curved_roof(c, x0, x1, base, h, col=ROOF, overhang=22):
    w = x1 - x0
    pts = [(x0 - overhang, base + 4)]
    for k in range(1, 6):
        t = k / 6
        pts.append((x0 - overhang + (w * 0.22 + overhang) * t, base + 4 - h * (t ** 1.8)))
    pts += [(x1 - w * 0.22, base - h)]
    for k in range(5, 0, -1):
        t = k / 6
        pts.append((x1 + overhang - (w * 0.22 + overhang) * t, base + 4 - h * (t ** 1.8)))
    pts.append((x1 + overhang, base + 4))
    piece(c, Poly(pts), col, border=2, shadow=PROP)
    flat(c, Thick(x0 + w * 0.22, base - h, x1 - w * 0.22, base - h, 5), lit(col, 0.7))
    flat(c, RRect(x0 - overhang + 6, base + 2, x1 + overhang - 6, base + 8, 2), (190, 150, 110))


def hall(c, x0, x1, floor_y, wall_top, roof_h, ground_y, bays, blinds_up=(), rail=True):
    """Raised hall: stilts, floor, vermilion pillars, bamboo blinds (rolled up in `blinds_up` bays), curved roof."""
    for x in [x0 + (x1 - x0) * k / bays for k in range(bays + 1)]:
        flat(c, RRect(x - 3, floor_y, x + 3, ground_y, 1), (120, 92, 70))
    piece(c, RRect(x0 - 12, floor_y, x1 + 12, floor_y + 9, 1), (176, 134, 96), border=1.5, shadow=PROP)
    bw = (x1 - x0) / bays
    for k in range(bays):
        bx = x0 + k * bw
        flat(c, RRect(bx, wall_top, bx + bw, floor_y, 0), (66, 54, 52))
        if k in blinds_up:
            piece(c, RRect(bx + 4, wall_top + 2, bx + bw - 4, wall_top + 10, 4), BLIND, shadow=SMALL)
        else:
            piece(c, RRect(bx + 3, wall_top, bx + bw - 3, wall_top + (floor_y - wall_top) * 0.72, 1), BLIND, shadow=SMALL)
            for y in range(int(wall_top + 5), int(wall_top + (floor_y - wall_top) * 0.72), 5):
                flat(c, Thick(bx + 4, y, bx + bw - 4, y, 0.8), lit(BLIND, 0.85))
            flat(c, [Thick(bx + bw * 0.3, wall_top, bx + bw * 0.3, wall_top + 20, 1.5), Thick(bx + bw * 0.7, wall_top, bx + bw * 0.7, wall_top + 20, 1.5)],
                 (160, 60, 60))
    for x in [x0 + bw * k for k in range(bays + 1)]:
        piece(c, RRect(x - 4, wall_top - 4, x + 4, floor_y, 1), VERMILION, shadow=SMALL)
    if rail:
        flat(c, [Thick(x0 - 10, floor_y - 14, x1 + 10, floor_y - 14, 3)], VERMILION)
        for x in range(int(x0 - 8), int(x1 + 12), 26):
            flat(c, Thick(x, floor_y - 16, x, floor_y, 2.5), VERMILION)
    curved_roof(c, x0, x1, wall_top - 4, roof_h)


def lady_seated(c, x, base, layers, fan=None, h=1.0):
    """Court lady in layered robes (juni-hitoe), kneeling; long black hair; optional folding fan."""
    for i, col in enumerate(layers):
        e = (len(layers) - i) * 2.5 * h
        piece(c, Poly([(x - 26 * h - e, base), (x + 26 * h + e, base), (x + 12 * h + e * 0.4, base - 34 * h), (x - 12 * h - e * 0.4, base - 34 * h)]),
              col, border=1.2 if i == 0 else 0, shadow=PROP if i == 0 else None)
    flat(c, Poly([(x - 6 * h, base - 46 * h), (x + 4 * h, base - 46 * h), (x + 4 * h, base - 4 * h), (x - 14 * h, base - 2 * h)]), HAIR)
    piece(c, Circ(x, base - 44 * h, 8 * h), HAIR, shadow=None)
    flat(c, Circ(x + 2 * h, base - 42 * h, 6.4 * h), (250, 236, 226))
    flat(c, [Thick(x + 1 * h, base - 44 * h, x + 4 * h, base - 44 * h, 1.2), Circ(x + 3 * h, base - 39 * h, 1.2 * h)], (40, 30, 30))
    if fan:
        piece(c, Poly([(x + 10 * h, base - 30 * h), (x + 30 * h, base - 46 * h), (x + 32 * h, base - 32 * h)]), fan, border=1, shadow=SMALL)


def courtier(c, x, base, robe, h=1.0, hat=(28, 26, 30), ornament=None):
    """Courtier in a wide robe with a tall black eboshi; returns head centre."""
    piece(c, [Poly([(x - 16 * h, base), (x + 16 * h, base), (x + 9 * h, base - 32 * h), (x - 9 * h, base - 32 * h)]),
              Poly([(x - 9 * h, base - 30 * h), (x - 22 * h, base - 14 * h), (x - 12 * h, base - 10 * h)]),
              Poly([(x + 9 * h, base - 30 * h), (x + 22 * h, base - 14 * h), (x + 12 * h, base - 10 * h)])], robe, border=1.5, shadow=PROP)
    hx, hy = x + 1 * h, base - 40 * h
    flat(c, Circ(hx, hy, 7 * h), (250, 230, 210))
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    flat(c, Poly([(hx - 7 * h, hy - 4 * h), (hx + 6 * h, hy - 4 * h), (hx + 4 * h, hy - 20 * h), (hx - 2 * h, hy - 22 * h), (hx - 6 * h, hy - 16 * h)]),
         hat)
    if ornament:
        flat(c, [Ell(hx - 9 * h, hy - 12 * h, 4 * h, 3 * h), Ell(hx - 12 * h, hy - 8 * h, 3.5 * h, 2.6 * h)], ornament)
    return hx, hy


def pine_jp(c, x, base, s=1.0, col=(60, 110, 80)):
    piece(c, [Thick(x, base, x - 10 * s, base - 40 * s, 8 * s), Thick(x - 10 * s, base - 40 * s, x + 6 * s, base - 76 * s, 6 * s),
              Thick(x - 4 * s, base - 50 * s, x + 30 * s, base - 58 * s, 4 * s)], (120, 90, 70), shadow=SMALL)
    pads = [(x - 20 * s, base - 46 * s, 24 * s), (x + 30 * s, base - 62 * s, 22 * s), (x + 4 * s, base - 82 * s, 26 * s), (x - 26 * s, base - 70 * s, 18 * s)]
    piece(c, [Ell(px, py, r, r * 0.42) for px, py, r in pads], col, border=1.2, shadow=PROP)
    flat(c, [Ell(px - r * 0.2, py - r * 0.12, r * 0.6, r * 0.18) for px, py, r in pads], lit(col, 1.18))


def blossom_tree(c, x, base, s, col, seed, trunk=(110, 80, 70)):
    rnd = random.Random(seed)
    piece(c, [Thick(x, base, x - 6 * s, base - 50 * s, 9 * s), Thick(x - 6 * s, base - 50 * s, x - 34 * s, base - 80 * s, 5 * s),
              Thick(x - 6 * s, base - 50 * s, x + 30 * s, base - 84 * s, 5 * s)], trunk, shadow=SMALL)
    blobs = [Circ(x + rnd.uniform(-50, 50) * s, base - rnd.uniform(60, 110) * s, rnd.uniform(16, 26) * s) for _ in range(9)]
    piece(c, blobs, col, border=1.2, shadow=PROP)
    for _ in range(26):
        flat(c, Circ(x + rnd.uniform(-58, 58) * s, base - rnd.uniform(52, 120) * s, rnd.uniform(2, 4) * s), lit(col, rnd.choice((0.86, 1.1))))


def stone_lantern(c, x, base, s=1.0):
    col = (170, 168, 160)
    piece(c, [RRect(x - 12 * s, base - 8 * s, x + 12 * s, base, 2), RRect(x - 4 * s, base - 40 * s, x + 4 * s, base - 8 * s, 1),
              RRect(x - 10 * s, base - 46 * s, x + 10 * s, base - 40 * s, 1), RRect(x - 8 * s, base - 62 * s, x + 8 * s, base - 46 * s, 1),
              Poly([(x - 18 * s, base - 62 * s), (x + 18 * s, base - 62 * s), (x, base - 76 * s)]), Circ(x, base - 78 * s, 3 * s)], col, border=1.2,
          shadow=PROP)
    flat(c, RRect(x - 4 * s, base - 58 * s, x + 4 * s, base - 50 * s, 1), (70, 64, 60))


def petal_el(i, x, y, col=(250, 200, 214)):
    def d(c, m):
        flat(c, Ell(x, y, 3.2, 2.2), col)
    return E("petal%d" % i, d, pivot=(x, y), anim=dict(driftVelocity=(14, -24), driftLength=380, driftFade=True, rotateSpeed=90 + i * 13,
                                                       spinSpeed=0.6 + 0.07 * i, spinShade=0.3, bobAmplitude=(10, 0), bobSpeed=0.4,
                                                       phase=(i * 0.137) % 1))


# =================================================================== Level 74 shinden garden in spring
BRIDGE74 = (470, 650, 440, 392)          # x0, x1, base, top
GIBOSHI = [478, 528, 590, 642]
KOI74 = [(560, 476, (230, 80, 60)), (628, 488, (250, 250, 246)), (700, 470, (240, 190, 60))]


def l74_bg(c, d):
    sky(c, (196, 220, 240), (252, 238, 222), 400)
    kasumi(c, 70, -20, 380)
    kasumi(c, 118, 520, 920, 18)
    layer(c, 244, [(20, 0.007, 0.5), (8, 0.02, 1.4)], (156, 182, 172))
    rnd = random.Random(74)
    for _ in range(40):
        x = rnd.uniform(0, W)
        flat(c, Circ(x, gy(244, [(20, 0.007, 0.5), (8, 0.02, 1.4)], x) + rnd.uniform(4, 30), rnd.uniform(4, 8)), (240, 200, 210))
    layer(c, 286, [(10, 0.01, 1.0), (5, 0.03, 0.2)], (134, 170, 142))
    kasumi(c, 286, 300, 700, 18)
    # garden ground and pond
    piece(c, hill_strip(352, [(4, 0.01, 0.4)]), (176, 196, 140), shadow=LAYER)
    piece(c, Ell(600, 452, 360, 64), (118, 170, 190), shadow=None)
    flat(c, Ell(600, 446, 330, 50), (132, 184, 204))
    for x in range(300, 900, 46):
        flat(c, Thick(x, 446 + (x % 3) * 8, x + 20, 446 + (x % 3) * 8, 1.5), (160, 204, 220))
    for x, y, col in KOI74:
        if col == (240, 190, 60) and "koi" in d:
            col = (40, 40, 46)
        piece(c, [Ell(x, y, 13, 5), Poly([(x - 12, y), (x - 20, y - 5), (x - 20, y + 5)])], col, shadow=None)
    # island with pine
    piece(c, Ell(790, 456, 70, 16), (150, 176, 120), shadow=SMALL)
    pine_jp(c, 790, 456, 1.0)
    # main hall (shinden) + corridor + fishing pavilion
    hall(c, 30, 420, 350, 252, 74, 384, 5, blinds_up=(1,) if "blind" in d else ())
    piece(c, Poly([(212, 360), (238, 360), (250, 392), (200, 392)]), (176, 134, 96), border=1.2, shadow=PROP)
    for k in range(4):
        flat(c, Thick(204 + k * 1.5, 368 + k * 7, 246 - k * 1.5, 368 + k * 7, 1.5), (140, 104, 74))
    hall(c, 432, 600, 356, 300, 34, 400, 3, blinds_up=(0, 1, 2), rail=False)
    hall(c, 620, 760, 372, 302, 46, 430, 3, blinds_up=(1,))
    # ladies on the veranda, koto
    lady_seated(c, 150, 346, [(150, 40, 70), (230, 120, 140), (250, 220, 200), (120, 160, 110)], fan=(80, 140, 200) if "fan" in d else (220, 60, 60))
    lady_seated(c, 254, 346, [(70, 90, 150), ((150, 200, 120) if "robe" in d else (240, 170, 60)), (250, 230, 220), (180, 60, 80)])
    if "koto" not in d:
        piece(c, Poly([(318, 346), (392, 338), (394, 344), (320, 350)]), (170, 120, 70), border=1.2, shadow=SMALL)
        for k in range(5):
            flat(c, Thick(324 + k * 2, 345 - k * 0.2, 388, 339.5 + k * 0.5 - k * 0.1, 0.6), (250, 240, 210))
    # arched bridge
    x0, x1, base, top = BRIDGE74
    arc = [(x0 + (x1 - x0) * k / 16, base - (base - top) * math.sin(math.pi * k / 16)) for k in range(17)]
    piece(c, Poly(arc + [(x1, base + 8), (x0, base + 8)]), VERMILION, border=1.5, shadow=PROP)
    rail = [(x, y - 18) for x, y in arc]
    flat(c, [Thick(rail[i][0], rail[i][1], rail[i + 1][0], rail[i + 1][1], 3) for i in range(16)], VERMILION)
    for i, gx in enumerate(GIBOSHI):
        gy_ = base - (base - top) * math.sin(math.pi * (gx - x0) / (x1 - x0))
        flat(c, Thick(gx, gy_, gx, gy_ - 22, 3), VERMILION)
        if not (i == 2 and "giboshi" in d):
            piece(c, [Circ(gx, gy_ - 25, 4.5), Poly([(gx - 2, gy_ - 28), (gx + 2, gy_ - 28), (gx, gy_ - 34)])], (200, 170, 90), shadow=None)
    # near bank: raked gravel, stone lantern, kemari players
    piece(c, hill_strip(500, [(5, 0.01, 0.3), (2, 0.04, 1.0)]), (232, 228, 214), shadow=LAYER)
    for y in range(512, 600, 9):
        flat(c, Thick(0, y, 900, y + 3 * math.sin(y), 1.2), (214, 208, 192))
    if "lantern" not in d:
        stone_lantern(c, 470, 540)
    for x, robe in ((560, (60, 100, 160)), (650, (170, 60, 70)), (740, (90, 140, 90))):
        courtier(c, x, 590, robe)
    pine_jp(c, 30, 604, 1.6)
    blossom_tree(c, 860, 612, 2.0, (246, 196, 210), 741)


def l74_ball(c, m):
    piece(c, Circ(650, 520, 7), (246, 242, 230), border=1, shadow=SMALL)
    flat(c, Thick(644, 520, 656, 520, 1.2), (190, 160, 120))


L74_ELEMENTS = [
    bird_el("bird0", 420, 160, 8, speed=16), bird_el("bird1", 446, 150, 6, speed=16),
    E("ball", l74_ball, pivot=(650, 527), anim=dict(bobAmplitude=(0, 60), bobSpeed=0.45, bounce=True, rotateSpeed=-90)),
] + [petal_el(i, x, y) for i, (x, y) in enumerate(((800, 420), (840, 380), (760, 440), (880, 460), (820, 500), (700, 400), (860, 330),
                                                       (740, 360)))]

L74_DIFFS = [
    ("blind", 30 + 78 * 1.5, 290, 0),
    ("giboshi", GIBOSHI[2], 380, 0),
    ("fan", 172, 308, 0),
    ("robe", 254, 330, 0),
    ("koto", 356, 342, 0),
    ("lantern", 470, 500, 0),
    ("koi", 700, 470, 0),
]


# =================================================================== Level 75 Aoi festival before the Suzaku gate
WILLOWS75 = [(110, 400), (790, 400)]


def tsuiji(c, x0, x1, top, base):
    piece(c, RRect(x0, top, x1, base, 0), (236, 214, 170), border=1.5, shadow=PROP)
    for y in (top + 14, top + 26, top + 38):
        flat(c, Thick(x0, y, x1, y, 1.2), (214, 190, 146))
    piece(c, Poly([(x0 - 6, top + 2), (x1 + 6, top + 2), (x1, top - 10), (x0, top - 10)]), (80, 84, 92), shadow=SMALL)


def l75_bg(c, d):
    sky(c, (190, 216, 236), (250, 236, 214), 380)
    kasumi(c, 60, 560, 920, 20)
    kasumi(c, 100, -20, 300, 18)
    layer(c, 250, [(24, 0.006, 0.3), (10, 0.02, 1.1)], (150, 170, 176))
    layer(c, 290, [(12, 0.01, 1.4)], (128, 160, 140))
    tsuiji(c, -10, 320, 318, 376)
    tsuiji(c, 580, 910, 318, 376)
    # Suzaku gate (two storeys)
    for x in range(316, 600, 46):
        piece(c, RRect(x - 6, 292, x + 6, 378, 1), VERMILION, shadow=SMALL)
    flat(c, [RRect(322, 300, 356, 378, 0), RRect(544, 300, 578, 378, 0)], (240, 236, 226))
    curved_roof(c, 300, 600, 290, 30, overhang=34)
    piece(c, RRect(330, 228, 570, 286, 1), VERMILION, border=1.5, shadow=PROP)
    for x in range(342, 570, 30):
        flat(c, RRect(x, 238, x + 16, 278, 1), (240, 236, 226))
    flat(c, Thick(326, 258, 574, 258, 3), (240, 236, 226))
    curved_roof(c, 330, 570, 226, 46, overhang=36)
    piece(c, RRect(430, 236, 470, 270, 2), (60, 140, 90) if "plaque" in d else (40, 50, 110), border=1.5, border_col=GOLD, shadow=SMALL)
    flat(c, [Thick(442, 244, 458, 244, 2), Thick(450, 244, 450, 262, 2), Thick(442, 254, 458, 254, 2)], GOLD)
    # avenue
    piece(c, RRect(-10, 376, 910, 612, 0), (224, 208, 170), shadow=LAYER)
    for y in range(392, 600, 20):
        flat(c, Thick(0, y, 900, y, 1), (210, 192, 152))
    # spectators along the wall
    rnd = random.Random(75)
    for x in list(range(20, 300, 34)) + list(range(600, 890, 34)):
        col = rnd.choice(((150, 60, 70), (70, 100, 150), (200, 170, 90), (90, 130, 90)))
        piece(c, [Ell(x, 392, 9, 12), Circ(x, 376, 6)], col, shadow=SMALL)
        flat(c, Circ(x, 376, 5), (250, 230, 210))
    for x, base in WILLOWS75:
        piece(c, [Thick(x, base, x - 4, base - 120, 9), Thick(x - 4, base - 100, x - 30, base - 130, 4), Thick(x, base - 110, x + 26, base - 136, 4)],
              (110, 90, 70), shadow=SMALL)
    # furyu parasol bearer
    courtier(c, 150, 566, (230, 220, 190))
    flat(c, Thick(160, 540, 168, 420, 3), (120, 90, 60))
    piece(c, ellipse_top(168, 428, 60, 30), (200, 50, 50), border=1.5, shadow=PROP)
    for k in range(7):
        a = math.pi * (k + 0.5) / 7
        fx, fy = 168 + 50 * math.cos(a), 428 - 24 * math.sin(a)
        flat(c, Thick(fx, fy, fx, fy + 26, 1), (230, 220, 190))
    flowers = (250, 250, 246) if "umbrella" in d else (250, 200, 60)
    for dx in (-24, -8, 8, 24):
        piece(c, Circ(168 + dx, 398 - abs(dx) * 0.3, 7), flowers, shadow=None)
    flat(c, [Ell(168, 392, 14, 6)], (90, 150, 80))
    # rider
    hc = (170, 100, 60)
    for lx in (-22, -12, 14, 24):
        flat(c, RRect(296 + lx - 3, 540, 296 + lx + 3, 572, 1), lit(hc, 0.8))
    piece(c, [Ell(296, 534, 36, 16), Poly([(326, 530), (340, 494), (350, 498), (338, 534)]), Ell(350, 494, 12, 8)], hc, border=1.5, shadow=PROP)
    tas = (60, 110, 200) if "tassel" in d else (220, 50, 50)
    for tx in (270, 290, 310, 330):
        flat(c, [Thick(tx, 540, tx, 552, 2), Circ(tx, 554, 3)], tas)
    flat(c, Thick(262, 524, 264, 556, 3), (70, 60, 60))
    courtier(c, 294, 528, (190, 50, 60), ornament=None if "aoi" in d else (70, 150, 80))
    # ox carriage
    wheel = (180, 50, 40) if "wheel" in d else (40, 34, 34)
    piece(c, RRect(400, 476, 540, 556, 3), (60, 50, 50), border=1.5, shadow=PROP)
    flat(c, [RRect(410, 484, 470, 548, 2)], BLIND)
    for y in range(488, 548, 5):
        flat(c, Thick(412, y, 468, y, 0.8), lit(BLIND, 0.85))
    flat(c, RRect(480, 488, 530, 540, 2), (150, 40, 50))
    piece(c, Poly([(388, 478), (552, 478), (540, 452), (470, 440), (400, 452)]), (40, 34, 36), border=1.5, shadow=PROP)
    wist = (240, 236, 246) if "wisteria" in d else (160, 110, 200)
    for k in range(9):
        x = 398 + k * 18
        for j in range(4):
            flat(c, Circ(x + (j % 2) * 2, 484 + j * 7, 3.6 - j * 0.5), wist)
    c.ellipse_ring(500, 560, 34, 34, 6, wheel)
    for k in range(10):
        a = math.pi * k / 5
        flat(c, Thick(500, 560, 500 + 31 * math.cos(a), 560 + 31 * math.sin(a), 2), wheel)
    flat(c, Circ(500, 560, 6), (200, 170, 90))
    flat(c, [Thick(540, 520, 640, 530, 4), Thick(540, 530, 640, 540, 4)], (40, 34, 34))
    # ox and driver
    ox = (130, 90, 60) if "ox" in d else (40, 36, 40)
    for lx in (-26, -14, 16, 28):
        flat(c, RRect(668 + lx - 3.5, 550, 668 + lx + 3.5, 590, 1), lit(ox, 0.8))
    piece(c, [Ell(668, 540, 40, 20), Ell(714, 534, 14, 12)], ox, border=1.5, shadow=PROP)
    flat(c, [Thick(706, 524, 698, 512, 3), Thick(720, 524, 728, 512, 3)], (230, 220, 200))
    flat(c, [Thick(726, 538, 770, 548, 1.6)], (200, 60, 60))
    courtier(c, 780, 588, (240, 236, 226))
    # palanquin with phoenix (the saio)
    piece(c, RRect(820, 500, 892, 560, 3), (160, 40, 50), border=1.5, shadow=PROP)
    piece(c, Poly([(812, 502), (900, 502), (856, 478)]), (40, 34, 36), shadow=SMALL)
    piece(c, [Poly([(852, 478), (860, 478), (858, 462), (854, 462)]), Poly([(856, 466), (872, 456), (860, 470)])], GOLD, shadow=None)
    flat(c, Thick(800, 540, 910, 540, 4), (110, 80, 60))
    for x in (812, 896):
        courtier(c, x, 594, (230, 220, 190), h=0.9)


def l75_willow(x, base, i):
    def d(c, m):
        for k in range(9):
            sx = x - 44 + k * 11
            pts = [(sx + 4 * math.sin(j * 0.7 + k), base - 128 + j * 16) for j in range(7)]
            flat(c, [Thick(pts[j][0], pts[j][1], pts[j + 1][0], pts[j + 1][1], 1.4) for j in range(6)], (100, 150, 80))
            for j in range(1, 7):
                flat(c, Ell(pts[j][0] + 2, pts[j][1], 3, 1.6), (120, 176, 96))
    return E("willow%d" % i, d, pivot=(x, base - 128), anim=dict(swingAngle=3, swingSpeed=0.18 + i * 0.03, phase=i * 0.4))


def l75_streamer(x, y, col, i):
    def d(c, m):
        flat(c, Thick(x, y + 120, x, y, 2.5), (110, 80, 60))
        piece(c, Poly([(x + 1, y + 4), (x + 12, y + 8), (x + 10, y + 70), (x + 1, y + 74)]), col, shadow=SMALL)
    return E("streamer%d" % i, d, pivot=(x, y + 40), anim=dict(swingAngle=5, swingSpeed=0.6 + i * 0.1, stretch=(0.1, 0), scaleSpeed=1.2))


L75_ELEMENTS = [l75_willow(x, b, i) for i, (x, b) in enumerate(WILLOWS75)] + [
    l75_streamer(236, 440, (250, 246, 236), 0), l75_streamer(380, 430, (220, 60, 60), 1), l75_streamer(760, 440, (90, 140, 200), 2),
    E("oxtail", lambda c, m: flat(c, [Thick(628, 534, 620, 566, 2), Circ(620, 568, 3)], (40, 36, 40)), pivot=(628, 534),
      anim=dict(swingAngle=14, swingSpeed=0.6)),
    bird_el("bird0", 560, 150, 8, speed=16), bird_el("bird1", 588, 138, 6, speed=16),
]

L75_DIFFS = [
    ("plaque", 450, 253, 0),
    ("umbrella", 168, 396, 0),
    ("tassel", 300, 550, 0),
    ("aoi", 284, 480, 0),
    ("wisteria", 470, 494, 0),
    ("ox", 668, 540, 0),
    ("wheel", 500, 560, 0),
]


# =================================================================== Level 76 autumn boating party (day / night)
DN76 = day_night(40.0, tint=(0.30, 0.30, 0.56))
MOON76 = (700, 86)
DRAGON = (300, 432)
HERON = (540, 478)
PAVILION_WIN = [(670 + k * 52, 250, 670 + k * 52 + 44, 300) for k in range(4)]


def maple(c, x, base, s, col, seed):
    blossom_tree(c, x, base, s, col, seed, trunk=(96, 70, 62))


def l76_bg(c, d):
    sky(c, (170, 200, 230), (250, 220, 190), 340)
    kasumi(c, 150, -20, 260, 18)
    layer(c, 236, [(22, 0.007, 0.8), (8, 0.02, 0.2)], (150, 140, 150))
    rnd = random.Random(76)
    for _ in range(46):
        x = rnd.uniform(0, W)
        flat(c, Circ(x, gy(236, [(22, 0.007, 0.8), (8, 0.02, 0.2)], x) + rnd.uniform(6, 40), rnd.uniform(5, 9)),
             rnd.choice(((220, 90, 60), (240, 150, 60), (200, 60, 50))))
    layer(c, 296, [(10, 0.012, 1.0)], (150, 130, 100))
    # far shore with a deer and a maple (one maple stays green in B)
    piece(c, hill_strip(330, [(4, 0.01, 0.5)]), (170, 150, 104), shadow=LAYER)
    maple(c, 560, 336, 0.9, (110, 160, 80) if "maple" in d else (214, 70, 50), 761)
    maple(c, 200, 334, 0.8, (236, 140, 50), 762)
    deer = (170, 120, 80)
    for lx in (-10, -4, 8, 14):
        flat(c, RRect(420 + lx - 1.5, 314, 420 + lx + 1.5, 334, 1), lit(deer, 0.8))
    piece(c, [Ell(422, 310, 18, 8), Poly([(434, 306), (444, 290), (450, 292), (440, 310)]), Ell(450, 290, 7, 4)], deer, border=1.2, shadow=SMALL)
    if "deer" not in d:
        flat(c, [Thick(446, 286, 440, 270, 1.6), Thick(442, 276, 436, 272, 1.4), Thick(450, 286, 456, 270, 1.6), Thick(454, 276, 460, 272, 1.4)],
             (120, 90, 60))
    # pond
    c.rect(0, 338, W, 530, (76, 124, 152))
    for y in range(350, 528, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (104, 150, 176))
    # great drum on the left shore (flame ornament changes colour)
    piece(c, RRect(30, 360, 190, 380, 2), (150, 110, 80), border=1.5, shadow=PROP)
    for x in (40, 180):
        flat(c, RRect(x - 3, 380, x + 3, 420, 1), (120, 90, 70))
    flame = GOLD if "drum" in d else VERMILION
    rim = [(110 + 74 * math.cos(2 * math.pi * k / 16), 270 + 74 * math.sin(2 * math.pi * k / 16)) for k in range(16)]
    piece(c, [Poly([(x - 10, y), (x + 10, y), (110 + (x - 110) * 1.35, 270 + (y - 270) * 1.35)]) for x, y in rim], flame, border=1.2, shadow=PROP)
    piece(c, Circ(110, 270, 62), (60, 40, 40), border=2, shadow=PROP)
    piece(c, Circ(110, 270, 50), (230, 220, 196), shadow=None)
    for k in range(3):
        a = 2 * math.pi * k / 3
        flat(c, [Circ(110 + 18 * math.cos(a), 270 + 18 * math.sin(a), 12),
                 Poly([(110 + 18 * math.cos(a) + 12 * math.cos(a + 1.6), 270 + 18 * math.sin(a) + 12 * math.sin(a + 1.6)),
                       (110 + 30 * math.cos(a + 0.9), 270 + 30 * math.sin(a + 0.9)),
                       (110 + 18 * math.cos(a) + 12 * math.cos(a - 1.6), 270 + 18 * math.sin(a) + 12 * math.sin(a - 1.6))])],
             [(200, 50, 50), (60, 90, 160), (240, 190, 60)][k])
    flat(c, Thick(110, 336, 110, 362, 6), (60, 40, 40))
    # fishing pavilion on the right with a lady writing a poem slip
    hall(c, 660, 880, 316, 246, 50, 400, 4, blinds_up=(1, 2) if "blind" in d else (1,))
    lady_seated(c, 744, 312, [(110, 50, 80), (240, 150, 60), (250, 230, 210), (170, 60, 50)])
    piece(c, RRect(764, 284, 772, 310, 1), (120, 170, 220) if "tanzaku" in d else (240, 200, 210), border=1, shadow=SMALL)
    # near bank
    piece(c, hill_strip(528, [(6, 0.012, 0.4), (3, 0.04, 1.0)]), (150, 140, 92), shadow=LAYER)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(540, 600)
        flat(c, Poly(star_pts(x, y, 5, 2.4, points=5, rot=rnd.uniform(0, 70))), rnd.choice(((220, 80, 50), (240, 160, 60), (200, 60, 50))))
    stone_lantern(c, 620, 590, 0.9)
    hx, hy = courtier(c, 520, 592, (60, 60, 110))
    lady_seated(c, 450, 590, [(60, 70, 120), (200, 80, 90), (250, 230, 220)])
    maple(c, 30, 616, 2.0, (214, 70, 50), 763)
    maple(c, 880, 616, 1.8, (236, 120, 50), 764)


def boat(x, y, head, head_col, banner, roof_col, players):
    def d(c, m):
        hc = head_col(m) if callable(head_col) else head_col
        bc = banner(m) if callable(banner) else banner
        piece(c, Poly([(x - 90, y - 10), (x + 80, y - 10), (x + 66, y + 10), (x - 76, y + 10)]), (120, 80, 60), border=1.5, shadow=SMALL)
        flat(c, Thick(x - 88, y - 6, x + 78, y - 6, 2), GOLD)
        if head == "dragon":
            piece(c, [Poly([(x + 76, y - 10), (x + 98, y - 40), (x + 118, y - 44), (x + 112, y - 30), (x + 92, y - 8)]),
                      Poly([(x + 104, y - 44), (x + 100, y - 58), (x + 110, y - 46)])], hc, border=1.5, shadow=SMALL)
            flat(c, [Circ(x + 108, y - 38, 2)], INK)
            flat(c, Thick(x + 116, y - 36, x + 126, y - 30, 1.5), (220, 60, 50))
        else:
            piece(c, [Poly([(x + 76, y - 10), (x + 90, y - 50), (x + 98, y - 52), (x + 92, y - 10)]), Ell(x + 98, y - 54, 8, 5),
                      Poly([(x + 104, y - 56), (x + 122, y - 52), (x + 104, y - 50)])], hc, border=1.5, shadow=SMALL)
            flat(c, Circ(x + 100, y - 55, 1.5), INK)
        for px in (x - 60, x + 40):
            flat(c, Thick(px, y - 10, px, y - 58, 2.5), VERMILION)
        piece(c, Poly([(x - 70, y - 56), (x + 50, y - 56), (x + 40, y - 70), (x - 60, y - 70)]), roof_col, border=1.2, shadow=SMALL)
        flat(c, Thick(x - 80, y - 10, x - 80, y - 100, 2), (110, 80, 60))
        piece(c, Poly([(x - 79, y - 98), (x - 64, y - 94), (x - 66, y - 60), (x - 79, y - 62)]), bc, shadow=SMALL)
        for i, (px, robe) in enumerate(players):
            courtier(c, x + px, y - 10, robe, h=0.62)
    return d


def l76_lantern_glow(c, m):
    for x, y in ((DRAGON[0] - 60, DRAGON[1] - 52), (DRAGON[0] + 40, DRAGON[1] - 52), (HERON[0] - 60, HERON[1] - 52),
                 (HERON[0] + 40, HERON[1] - 52)):
        soft_union(c, [Circ(x, y, 6)], (255, 200, 110), 0.6, spread=18)
        flat(c, RRect(x - 4, y - 6, x + 4, y + 6, 3), (255, 226, 150))


def l76_moon(c, m):
    x, y = MOON76
    soft_union(c, [Circ(x, y, 36)], (255, 250, 220), 0.4, spread=24)
    piece(c, Circ(x, y, 28), (252, 246, 220), border=2, shadow=PROP)
    flat(c, [Circ(x - 8, y - 6, 6), Circ(x + 10, y + 8, 4)], (232, 224, 196))


def l76_reflection(c, m):
    x = MOON76[0]
    for k, y in enumerate(range(352, 520, 14)):
        w = 26 - k * 1.2
        flat(c, RRect(x - w, y, x + w, y + 4, 2), (255, 246, 210, 0.55))


def l76_sun(c, m):
    piece(c, Poly(star_pts(MOON76[0], MOON76[1], 40, 30, points=12)), (255, 190, 80), shadow=PROP)
    piece(c, Circ(MOON76[0], MOON76[1], 26), (255, 216, 100), border=2, shadow=PROP)


def leaf_el(i, x, y):
    col = [(220, 80, 50), (240, 150, 60), (200, 60, 50)][i % 3]

    def d(c, m):
        flat(c, Poly(star_pts(x, y, 6, 2.6, points=5)), col)
    return E("leaf%d" % i, d, pivot=(x, y), anim=dict(driftVelocity=(16, -22), driftLength=420, driftFade=True, rotateSpeed=70 + i * 11,
                                                      spinSpeed=0.5 + 0.08 * i, spinShade=0.3, bobAmplitude=(14, 0), bobSpeed=0.3,
                                                      phase=(i * 0.173) % 1))


L76_ELEMENTS = [
    E("sun", l76_sun, daynight="day", anim=dict(pulse=0.03, scaleSpeed=0.3)),
    E("moon", l76_moon, daynight="night"),
    E("reflection", l76_reflection, daynight="night", anim=dict(stretch=(0.15, 0), scaleSpeed=0.7, twinkle=0.25, twinkleSpeed=0.9)),
    star_field("stars", 76, 40, 200, avoid=[(640, 30, 760, 150)]),
    E("dragon_boat", boat(*DRAGON, "dragon", lambda m: GOLD if m else (70, 150, 110), lambda m: (90, 120, 200) if m else (220, 60, 60),
                          (60, 50, 60), [(-40, (180, 60, 70)), (-10, (70, 100, 150)), (20, (230, 200, 120))]),
      pivot=(DRAGON[0], DRAGON[1] + 10), variant=True, anim=dict(bobAmplitude=(0, 2), bobSpeed=0.3, swingAngle=1, swingSpeed=0.2)),
    E("heron_boat", boat(*HERON, "heron", (246, 244, 236), (240, 200, 60), (60, 50, 60), [(-40, (90, 130, 90)), (-10, (150, 60, 90)),
                                                                                         (20, (60, 80, 130))]),
      pivot=(HERON[0], HERON[1] + 10), anim=dict(bobAmplitude=(0, 2), bobSpeed=0.27, swingAngle=1, swingSpeed=0.18, phase=0.4)),
    E("boat_lanterns", l76_lantern_glow, daynight="night", anim=dict(twinkle=0.15, twinkleSpeed=0.8)),
    window_glow("pavilion", PAVILION_WIN),
    bird_el("goose0", 560, 120, 9, col=(70, 70, 80), speed=14), bird_el("goose1", 584, 134, 8, col=(70, 70, 80), speed=14),
    bird_el("goose2", 608, 148, 7, col=(70, 70, 80), speed=14),
] + [leaf_el(i, x, y) for i, (x, y) in enumerate(((40, 440), (90, 400), (860, 430), (820, 470), (600, 330), (520, 300), (880, 380)))]

L76_DIFFS = [
    ("dragon", DRAGON[0] + 104, DRAGON[1] - 36, 0),
    ("banner", DRAGON[0] - 72, DRAGON[1] - 80, 0),
    ("drum", 110, 270, 0),
    ("maple", 560, 260, 0),
    ("deer", 450, 278, 0),
    ("tanzaku", 768, 296, 0),
    ("blind", 778, 270, 0),
]

LEVELS = [
    ("Level74", "寝殿庭园", l74_bg, L74_ELEMENTS, L74_DIFFS, 140, OPTS),
    ("Level75", "葵祭", l75_bg, L75_ELEMENTS, L75_DIFFS, 140, OPTS),
    ("Level76", "月夜舟游", l76_bg, L76_ELEMENTS, L76_DIFFS, 140, dict(OPTS, day_night=DN76, anim_seconds=40.0, frames=80)),
]
