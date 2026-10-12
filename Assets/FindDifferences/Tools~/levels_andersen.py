# -*- coding: utf-8 -*-
"""Andersen's fairy tales, paper-craft side views, full-bleed:
  Level104 海的女儿     - the little mermaid on a rock below the prince's ship; the sea king's palace beneath the waves
  Level105 卖火柴的小女孩 - a snowy New Year's eve street; each match shows a vision; snow weather cycle
  Level106 丑小鸭       - the farmyard pond: ducks, the grey duckling, swans flying over
  Level107 皇帝的新装   - the procession: the emperor under his canopy in his "new clothes", a child pointing
  Level108 拇指姑娘     - Thumbelina's world at flower scale: tulip, walnut-shell bed, toad, swallow
"""
import math
import random

from fdcore import CLEAR, E, H, OVERCAST, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bubbles_el, cloud_el, drift_across, fish, gy, house, layer, person, sky, smoke_el,
                 tree_round)
from stylekit import window_glow
from weather import cloud, snow_layer
from levels_heian import blossom_tree
from levels_europe import arch, ellipse_top, lady, top_hat, tricorne

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 226, 204)


def mermaid(c, x, y, tail=(70, 170, 150), hair=(230, 120, 60), flip=False, s=1.0):
    k = -1 if flip else 1
    piece(c, [Poly([(x - 8 * s, y), (x + 8 * s, y), (x + 14 * k * s, y + 30 * s), (x + 30 * k * s, y + 40 * s), (x + 44 * k * s, y + 30 * s),
                    (x + 40 * k * s, y + 46 * s), (x + 22 * k * s, y + 48 * s), (x - 4 * k * s, y + 34 * s)])], tail, border=1.5, shadow=PROP)
    for j in range(4):
        flat(c, Thick(x - 4 * s + j * 6 * k * s, y + 10 * s + j * 6 * s, x + 6 * s + j * 6 * k * s, y + 12 * s + j * 6 * s, 1), lit(tail, 1.2))
    piece(c, [RRect(x - 7 * s, y - 22 * s, x + 7 * s, y + 2 * s, 4), Circ(x, y - 30 * s, 8 * s)], SKIN, border=1.2, shadow=SMALL)
    flat(c, [Ell(x - 4 * k * s, y - 22 * s, 9 * s, 20 * s), Ell(x, y - 34 * s, 9 * s, 6 * s)], hair)
    flat(c, Circ(x + 3 * k * s, y - 30 * s, 1.2 * s), INK)
    flat(c, [Circ(x - 3 * s, y - 14 * s, 3 * s), Circ(x + 3 * s, y - 14 * s, 3 * s)], (240, 150, 170))


def coral(c, x, base, s, col):
    shapes = [Thick(x, base, x, base - 40 * s, 6 * s), Thick(x, base - 20 * s, x - 18 * s, base - 46 * s, 5 * s),
              Thick(x, base - 26 * s, x + 16 * s, base - 54 * s, 5 * s), Thick(x - 18 * s, base - 46 * s, x - 22 * s, base - 62 * s, 4 * s)]
    piece(c, shapes, col, shadow=SMALL)
    flat(c, [Circ(x - 22 * s, base - 62 * s, 3 * s), Circ(x + 16 * s, base - 54 * s, 3 * s), Circ(x, base - 40 * s, 3 * s)], lit(col, 1.2))


# =================================================================== Level 104 the little mermaid
def l104_bg(c, d):
    sky(c, (150, 196, 236), (250, 220, 200), 220)
    piece(c, Circ(780, 90, 28), (255, 220, 140), border=2, shadow=PROP)
    c.gradient(210, 600, (70, 150, 190), (20, 60, 110))
    for y in range(214, 236, 8):
        for x in range((y * 13) % 60, 900, 60):
            flat(c, Thick(x, y, x + 24, y, 2), (140, 200, 230))
    # prince's ship at the surface
    piece(c, Poly([(470, 196), (720, 196), (700, 226), (490, 226)]), (110, 70, 50), border=1.5, shadow=PROP)
    for mx, top in ((540, 70), (620, 50)):
        flat(c, Thick(mx, 196, mx, top, 3), (110, 80, 60))
        piece(c, Poly([(mx - 34, top + 12), (mx + 34, top + 12), (mx + 30, top + 80), (mx - 30, top + 80)]), (246, 240, 226), border=1.2, shadow=SMALL)
    flat(c, Poly([(621, 50), (650, 56), (621, 62)]), (60, 140, 80) if "flag" in d else (220, 50, 60))
    for k in range(6):
        flat(c, Circ(500 + k * 36, 210, 4), (60, 50, 50))
    person(c, 690, 196, (60, 70, 140), h=0.7, hat=None)
    # rocks with the mermaid
    piece(c, Poly([(60, 260), (100, 196), (170, 190), (220, 230), (250, 300), (40, 310)]), (110, 110, 120), shadow=LAYER)
    mermaid(c, 150, 214, tail=(70, 170, 150) if "tail" not in d else (200, 100, 160))
    # sea floor with the sea king's palace
    piece(c, hill_strip(530, [(10, 0.01, 0.4), (5, 0.04, 1.0)]), (200, 186, 140), shadow=LAYER)
    piece(c, RRect(560, 360, 820, 540, 2), (230, 170, 180), border=2, shadow=PROP)
    for x, h in ((560, 220), (690, 260), (820, 220)):
        piece(c, [RRect(x - 18, 540 - h, x + 18, 540, 2), Poly([(x - 22, 542 - h), (x + 22, 542 - h), (x, 500 - h)])], (240, 190, 200), border=1.5,
              shadow=PROP)
        flat(c, Circ(x, 502 - h, 5), (250, 230, 140))
    for x in (600, 650, 730, 780):
        flat(c, arch(x - 12, x + 12, 400, 450), (60, 90, 130))
    flat(c, arch(670, 710, 470, 540), (40, 60, 100))
    if "pearl" not in d:
        piece(c, [Ell(690, 368, 20, 10)], (240, 180, 190), border=1, shadow=SMALL)
        flat(c, Circ(690, 362, 7), (250, 250, 246))
    for x, s, col in ((80, 1.4, (240, 110, 110)), (200, 1.0, (250, 170, 90)), (420, 1.3, (230, 100, 160)), (880, 1.2, (250, 140, 120))):
        coral(c, x, 560, s, (120, 200, 230) if ("coral" in d and x == 420) else col)
    for x in range(300, 520, 22):
        flat(c, [Thick(x, 560, x + 8 * math.sin(x), 470, 3)], (60, 140, 90))
    mermaid(c, 300, 420, tail=(220, 120, 80), hair=(240, 220, 120), s=1.1)
    mermaid(c, 480, 460, tail=(240, 200, 80) if "sister" in d else (110, 120, 220), hair=(120, 70, 50), flip=True, s=1.0)
    # treasure chest and statue of the prince
    piece(c, [RRect(180, 520, 240, 556, 3), ellipse_top(210, 522, 30, 12)], (150, 100, 60), border=1.5, shadow=PROP)
    flat(c, [RRect(182, 530, 238, 536, 0)], (230, 190, 80))
    if "chest" not in d:
        flat(c, [Circ(200, 516, 5), Circ(214, 512, 5), Circ(226, 518, 5)], (250, 220, 90))
    piece(c, [RRect(340, 500, 380, 560, 2), Circ(360, 488, 10), Poly([(348, 500), (372, 500), (368, 470), (352, 470)])],
          (220, 220, 230) if "statue" not in d else (110, 180, 140), border=1.2, shadow=PROP)


L104_ELEMENTS = [
    cloud_el("cloud0", 200, 50, 0.7, 6), bird_el("gull0", 360, 90, 9, col=(250, 250, 250), speed=14),
] + bubbles_el("bub", 300, 380, n=4) + bubbles_el("bubB", 480, 420, n=3) + [
    E("fish%d" % i, (lambda x, y, col: lambda c, m: fish(c, x, y, 1.0, col))(x, y, col), pivot=(x, y),
      anim=dict(drift_across(x - 16, x + 16, sp, x), bobAmplitude=(0, 6), bobSpeed=0.3)) for i, (x, y, col, sp) in
    enumerate(((100, 330, (250, 200, 60), 18), (440, 300, (250, 130, 80), -14), (820, 320, (150, 200, 250), 12)))] + [
    E("wave", lambda c, m: flat(c, Thick(460, 228, 730, 228, 3), (220, 240, 250)), anim=dict(bobAmplitude=(8, 0), bobSpeed=0.2))]

L104_DIFFS = [
    ("flag", 635, 56, 0),
    ("tail", 170, 244, 0),
    ("pearl", 690, 364, 0),
    ("coral", 420, 520, 0),
    ("chest", 212, 514, 0),
    ("statue", 360, 500, 0),
    ("sister", 456, 490, 0),
]


# =================================================================== Level 105 the little match girl (snow)
STEPS105 = [(SNOW, 12), (OVERCAST, 8)]
WEATHER105 = dict(steps=STEPS105, blend=3.0, tints={SNOW: (0.92, 0.94, 1.0), OVERCAST: (0.9, 0.9, 0.96)})
GIRL = (450, 566)
WARM = (255, 214, 130)


def snowy_house(c, x0, x1, base, h, wall, roof, lit_wins=(), dark_wins=(), door=(110, 70, 50), wreath=False):
    piece(c, RRect(x0, base - h, x1, base, 1), wall, border=1.5, shadow=PROP)
    w = x1 - x0
    piece(c, Poly([(x0 - 10, base - h + 2), (x1 + 10, base - h + 2), ((x0 + x1) / 2, base - h - w * 0.45)]), roof, border=1.5, shadow=PROP)
    flat(c, Poly([(x0 - 12, base - h + 2), ((x0 + x1) / 2, base - h - w * 0.45 - 4), (x1 + 12, base - h + 2), (x1, base - h - 4), ((x0 + x1) / 2,
                                                                                                                                    base - h - w * 0.45 + 6),
                  (x0, base - h - 4)]), (246, 248, 255))
    for i, (wx, wy) in enumerate(lit_wins + dark_wins):
        col = WARM if i < len(lit_wins) else (60, 66, 90)
        if col == WARM:
            soft_union(c, [RRect(wx, wy, wx + 26, wy + 32, 2)], (255, 200, 110), 0.45, spread=14)
        flat(c, RRect(wx - 3, wy - 3, wx + 29, wy + 35, 1), (240, 236, 226))
        flat(c, RRect(wx, wy, wx + 26, wy + 32, 0), col)
        flat(c, [Thick(wx + 13, wy, wx + 13, wy + 32, 1.6), Thick(wx, wy + 16, wx + 26, wy + 16, 1.6)], (240, 236, 226))
    dx = (x0 + x1) / 2
    flat(c, RRect(dx - 12, base - 40, dx + 12, base, 2), door)
    if wreath:
        c.ellipse_ring(dx, base - 30, 7, 7, 4, (60, 130, 70))
        flat(c, Circ(dx, base - 24, 2.5), (220, 40, 50))


def l105_bg(c, d):
    sky(c, (40, 50, 90), (120, 110, 150), 480)
    snowy_house(c, 396, 526, 476, 150, (110, 100, 110), (60, 56, 70), dark_wins=((416, 380), (480, 380)))
    snowy_house(c, -10, 200, 470, 200, (170, 120, 100), (90, 70, 80), lit_wins=((20, 330), (120, 330), (20, 400)), dark_wins=((120, 400),),
                wreath="wreath" not in d)
    snowy_house(c, 206, 400, 476, 230, (130, 140, 160), (70, 70, 90), lit_wins=((236, 300), (330, 300)) if "window" not in d else ((236, 300),),
                dark_wins=() if "window" not in d else ((330, 300),))
    snowy_house(c, 520, 720, 476, 210, (190, 170, 130), (100, 80, 70), lit_wins=((560, 320), (650, 320)))
    snowy_house(c, 726, 910, 470, 190, (150, 100, 90), (80, 60, 60), lit_wins=((760, 340), (840, 340)))
    # shop window with a roast goose and a Christmas tree
    soft_union(c, [RRect(540, 396, 700, 456, 3)], (255, 200, 110), 0.5, spread=16)
    flat(c, RRect(540, 396, 700, 456, 2), (255, 226, 160))
    flat(c, RRect(536, 392, 704, 398, 1), (240, 236, 226))
    piece(c, [Poly([(660, 452), (640, 452), (660, 410), (680, 452)])], (40, 90, 150) if "star" in d else (50, 120, 70), shadow=SMALL)
    piece(c, Poly(star_pts(660, 408, 6, 2.6)), (250, 200, 60), shadow=None)
    if "goose" not in d:
        piece(c, [Ell(586, 444, 26, 10), Ell(586, 438, 22, 10)], (190, 120, 60), border=1, shadow=SMALL)
        flat(c, Ell(586, 450, 34, 4), (240, 240, 246))
    # snowy street
    piece(c, hill_strip(476, [(4, 0.012, 0.3), (2, 0.04, 1.0)]), (232, 236, 246), shadow=LAYER)
    for y in range(500, 600, 22):
        flat(c, Thick(0, y, 900, y + 2 * math.sin(y), 1.2), (214, 220, 236))
    piece(c, [Thick(800, 600, 800, 470, 4), RRect(790, 594, 810, 600, 2)], (40, 44, 50), shadow=PROP)
    piece(c, Poly([(790, 470), (810, 470), (814, 446), (786, 446)]), (40, 44, 50), shadow=SMALL)
    if "lamp" not in d:
        soft_union(c, [Circ(800, 458, 10)], (255, 214, 130), 0.5, spread=26)
    flat(c, Poly([(793, 468), (807, 468), (810, 450), (790, 450)]), (90, 100, 130) if "lamp" in d else (255, 230, 160))
    # the girl in the corner, with her matches
    gx, gb = GIRL
    piece(c, [Ell(gx, gb - 14, 22, 16), Circ(gx + 2, gb - 38, 9)], (110, 90, 90), border=1.2, shadow=PROP)
    piece(c, Poly([(gx - 16, gb - 30), (gx + 18, gb - 30), (gx + 12, gb - 48), (gx - 8, gb - 50)]), (60, 120, 170) if "shawl" in d else (180, 60, 70),
          border=1, shadow=SMALL)
    flat(c, Circ(gx + 3, gb - 38, 7.5), SKIN)
    flat(c, Circ(gx + 6, gb - 39, 1.2), INK)
    flat(c, [RRect(gx - 26, gb - 6, gx - 10, gb, 2)], (150, 110, 70))
    for k in range(4):
        flat(c, Thick(gx - 24 + k * 4, gb - 6, gx - 24 + k * 4, gb - 12, 1), (220, 60, 50))
    if "slipper" not in d:
        piece(c, Ell(gx + 30, gb + 2, 10, 5), (60, 60, 80), shadow=SMALL)
    # passers-by
    hx, hy = person(c, 140, 590, (40, 40, 50))
    top_hat(c, hx, hy, 1.0, (30, 30, 34), (30, 30, 34))
    hx, hy = lady(c, 640, 592, (110, 60, 110))
    piece(c, RRect(650, 556, 666, 566, 4), (240, 236, 226), shadow=SMALL)
    hx, hy = person(c, 300, 594, (90, 70, 60), h=0.8)
    flat(c, [Ell(hx, hy - 6, 8, 4)], (150, 40, 50))


def l105_match(c, m):
    gx, gb = GIRL
    soft_union(c, [Circ(gx + 22, gb - 30, 10)], (255, 190, 90), 0.6, spread=26)
    flat(c, Thick(gx + 14, gb - 22, gx + 22, gb - 30, 1.4), (240, 230, 200))
    flat(c, Poly([(gx + 19, gb - 30), (gx + 25, gb - 30), (gx + 22, gb - 40)]), (255, 210, 110))


def l105_vision(c, m):
    gx, gb = GIRL
    x, y = gx + 70, gb - 140
    soft_union(c, [Circ(x, y, 56)], (255, 230, 160), 0.45, spread=22)
    piece(c, [Poly([(x, y - 44), (x - 30, y + 26), (x + 30, y + 26)])], (60, 140, 80), shadow=SMALL)
    for k in range(6):
        flat(c, Circ(x - 18 + k * 7, y - 6 + (k % 3) * 10, 3), [(255, 210, 60), (230, 60, 60), (120, 180, 250)][k % 3])
    piece(c, Poly(star_pts(x, y - 46, 8, 3.4)), (255, 220, 80), shadow=None)


L105_ELEMENTS = [
    E("match", l105_match, pivot=(GIRL[0] + 22, GIRL[1] - 30), daynight="untinted", anim=dict(stretch=(0.1, 0.25), scaleSpeed=3.0, twinkle=0.2,
                                                                                           twinkleSpeed=2.5)),
    E("vision", l105_vision, daynight="untinted", anim=dict(twinkle=0.95, twinkleSpeed=0.08, pulse=0.05, scaleSpeed=0.3)),
    snow_layer("snowFar", 1051, 50, 1.4, 2.6, 24),
    snow_layer("snowNear", 1052, 26, 3.0, 4.6, 44, sway=12),
] + smoke_el("chimney", 140, 220, n=3, col=(200, 200, 210), r=7, rise=(4, 18), length=60)

L105_DIFFS = [
    ("wreath", 95, 440, 0),
    ("window", 343, 316, 0),
    ("star", 660, 434, 0),
    ("goose", 586, 440, 0),
    ("shawl", GIRL[0] + 2, GIRL[1] - 40, 0),
    ("slipper", GIRL[0] + 30, GIRL[1] + 2, 0),
    ("lamp", 800, 458, 0),
]


# =================================================================== Level 106 the ugly duckling
def duck(c, x, y, body, bill=(240, 150, 40), s=1.0, flip=False):
    k = -1 if flip else 1
    piece(c, [Ell(x, y, 16 * s, 9 * s), Circ(x + 13 * k * s, y - 10 * s, 7 * s)], body, border=1.2, shadow=SMALL)
    flat(c, Poly([(x + 18 * k * s, y - 11 * s), (x + 26 * k * s, y - 9 * s), (x + 18 * k * s, y - 7 * s)]), bill)
    flat(c, Circ(x + 15 * k * s, y - 12 * s, 1.2 * s), INK)
    flat(c, Ell(x - 4 * k * s, y - 2 * s, 8 * s, 4 * s), lit(body, 0.88))


def l106_bg(c, d):
    sky(c, (170, 210, 240), (246, 240, 222), 340)
    layer(c, 250, [(16, 0.008, 0.4)], (160, 190, 160))
    # barn and fence
    piece(c, RRect(20, 240, 220, 400, 1), (180, 70, 60), border=2, shadow=PROP)
    piece(c, Poly([(6, 244), (234, 244), (180, 190), (66, 190)]), (110, 90, 80), border=1.5, shadow=PROP)
    piece(c, RRect(84, 300, 156, 400, 2), (60, 110, 160) if "door" in d else (240, 236, 226), border=1.2, shadow=SMALL)
    flat(c, [Thick(84, 300, 156, 400, 3), Thick(156, 300, 84, 400, 3)], (180, 70, 60))
    piece(c, hill_strip(380, [(5, 0.01, 0.4)]), (130, 180, 100), shadow=LAYER)
    for x in range(220, 900, 30):
        piece(c, Poly([(x - 3, 396), (x - 3, 360), (x + 3, 360), (x + 3, 396)]), (240, 232, 214), shadow=SMALL)
    flat(c, [Thick(220, 370, 900, 370, 2.5), Thick(220, 384, 900, 384, 2.5)], (226, 216, 196))
    # cat on the fence, hen with chicks
    cat = (120, 120, 130) if "cat" in d else (240, 160, 80)
    piece(c, [Ell(700, 356, 14, 9), Circ(712, 344, 8), Poly([(706, 338), (708, 330), (712, 338)]), Poly([(714, 338), (718, 330), (720, 340)])], cat,
          border=1, shadow=SMALL)
    hen = (150, 90, 50) if "hen" in d else (250, 246, 236)
    piece(c, [Ell(300, 420, 18, 13), Circ(314, 404, 8), Poly([(286, 414), (276, 402), (282, 420)])], hen, border=1.2, shadow=PROP)
    flat(c, [Poly([(310, 396), (314, 390), (318, 396)]), Poly([(320, 404), (326, 406), (320, 408)])], (220, 50, 50))
    for x in (340, 356, 370):
        piece(c, Circ(x, 428, 5), (250, 220, 90), shadow=None)
    # pond
    piece(c, Ell(520, 500, 330, 70), (100, 160, 200), shadow=None)
    flat(c, Ell(520, 494, 300, 56), (126, 184, 216))
    duck(c, 400, 490, (170, 130, 90) if "bill" in d else (250, 250, 246))
    for i, x in enumerate((440, 470, 500, 530)):
        if i == 3 and "duckling" in d:
            continue
        duck(c, x, 500, (250, 220, 80), s=0.6)
    duck(c, 590, 506, (150, 150, 160), s=0.8)
    for x, y in ((720, 470), (790, 480)):
        piece(c, [Ell(x, y, 22, 10), Thick(x + 16, y - 6, x + 22, y - 34, 5), Ell(x + 26, y - 36, 7, 4)], (250, 250, 252), border=1.2, shadow=SMALL)
        flat(c, Poly([(x + 30, y - 37), (x + 38, y - 35), (x + 30, y - 33)]), (240, 140, 50))
    for x, y, col in ((660, 530, (240, 150, 180)), (440, 540, (250, 250, 246) if "lily" not in d else (240, 200, 60))):
        flat(c, Ell(x, y, 16, 5), (90, 150, 90))
        piece(c, Poly([(x - 7, y - 2), (x + 7, y - 2), (x + 9, y - 10), (x, y - 14), (x - 9, y - 10)]), col, shadow=SMALL)
    # reeds and near bank
    piece(c, hill_strip(560, [(4, 0.012, 0.3)]), (110, 160, 90), shadow=LAYER)
    for x in range(10, 220, 16):
        flat(c, Thick(x, 600, x + 4, 470 + (x % 30), 2.4), (90, 140, 80))
    for i, x in enumerate((40, 90, 150, 190)):
        if i == 2 and "reed" in d:
            continue
        piece(c, RRect(x - 3, 470 + (x % 30) - 6, x + 5, 470 + (x % 30) + 18, 3), (120, 80, 50), shadow=SMALL)
    for x in range(700, 900, 16):
        flat(c, Thick(x, 600, x - 3, 500 + (x % 40), 2.4), (90, 140, 80))
    tree_round(c, 850, 380, 1.6, (90, 150, 90))


L106_ELEMENTS = [
    cloud_el("cloud0", 300, 70, 0.7, 6), cloud_el("cloud1", 700, 50, 0.6, 5),
] + [E("swan%d" % i, (lambda x, y: lambda c, m: (piece(c, [Ell(x, y, 18, 6), Poly([(x - 4, y), (x - 26, y - 22), (x + 6, y - 2)]),
                                                         Poly([(x + 4, y), (x + 18, y - 24), (x + 10, y - 2)]), Thick(x + 14, y - 2, x + 34, y - 6, 3)],
                                                        (250, 250, 252), shadow=SMALL),
                                                  flat(c, Poly([(x + 34, y - 8), (x + 40, y - 6), (x + 34, y - 4)]), (240, 140, 50))))(x, y),
       pivot=(x, y), anim=dict(drift_across(x - 30, x + 40, 20, x), stretch=(0, 0.4), scaleSpeed=1.4)) for i, (x, y) in
     enumerate(((300, 130), (360, 110), (420, 140)))] + [
    E("tail", lambda c, m: flat(c, Thick(688, 356, 676, 336, 3), (120, 120, 130) if m else (240, 160, 80)), pivot=(688, 356), variant=True,
      anim=dict(swingAngle=20, swingSpeed=0.5)),
]

L106_DIFFS = [
    ("door", 120, 350, 0),
    ("cat", 708, 350, 0),
    ("hen", 300, 412, 0),
    ("duckling", 530, 496, 0),
    ("lily", 440, 532, 0),
    ("reed", 150, 486, 0),
    ("bill", 420, 480, 0),
]


# =================================================================== Level 107 the emperor's new clothes
def l107_bg(c, d):
    sky(c, (170, 206, 236), (246, 236, 216), 340)
    # town hall and houses
    for i, (x0, x1, col, rf) in enumerate(((-10, 160, (230, 200, 160), (170, 70, 60)), (160, 300, (200, 220, 230), (80, 90, 120)),
                                           (600, 740, (240, 210, 180), (170, 70, 60)), (740, 910, (210, 190, 220), (90, 70, 110)))):
        house(c, (x0 + x1) / 2, 380, x1 - x0, 200, col, rf, wins=3)
    piece(c, RRect(300, 150, 600, 380, 1), (236, 226, 206), border=2, shadow=PROP)
    piece(c, Poly([(290, 152), (610, 152), (450, 90)]), (100, 120, 160), border=1.5, shadow=PROP)
    piece(c, [RRect(430, 40, 470, 152, 1), Poly([(424, 42), (476, 42), (450, 0)])], (236, 226, 206), border=1.5, shadow=PROP)
    for x in range(320, 590, 40):
        flat(c, arch(x, x + 20, 190, 240), (90, 110, 140))
    # weavers at the window with an empty loom
    flat(c, RRect(330, 280, 420, 340, 2), (60, 54, 60))
    if "loom" not in d:
        piece(c, [RRect(344, 300, 404, 306, 1), RRect(344, 320, 404, 326, 1), RRect(344, 296, 350, 340, 1), RRect(398, 296, 404, 340, 1)],
              (170, 120, 80), shadow=SMALL)
    for x in (480, 540):
        flat(c, arch(x, x + 30, 280, 380), (90, 70, 60))
    # bunting
    pts = [(k * 60, 150 + 30 * abs(math.sin(math.pi * k / 5))) for k in range(16)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(15)], (70, 60, 60))
    for i in range(15):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        col = ((60, 160, 90) if "bunting" in d else (220, 50, 50)) if i == 11 else [(220, 50, 50), (250, 210, 60), (70, 130, 220)][i % 3]
        flat(c, Poly([(mx - 9, my), (mx + 9, my), (mx, my + 16)]), col)
    # crowd behind the barrier
    piece(c, RRect(-10, 380, 910, 612, 0), (200, 186, 160), shadow=LAYER)
    rnd = random.Random(107)
    for x in range(10, 900, 22):
        col = rnd.choice(((60, 70, 110), (150, 60, 70), (90, 110, 80), (200, 160, 100), (110, 70, 110)))
        piece(c, [Ell(x, 430, 10, 16), Circ(x, 410, 7)], col, shadow=SMALL)
        flat(c, Circ(x, 410, 6), SKIN)
    flat(c, Thick(0, 440, 900, 440, 4), (150, 110, 70))
    # child on father's shoulders, pointing
    piece(c, [Ell(160, 430, 12, 18), Circ(160, 404, 8)], (90, 80, 70), shadow=SMALL)
    piece(c, [Ell(160, 384, 8, 10), Circ(160, 368, 6)], (220, 60, 60) if "child" not in d else (60, 140, 200), shadow=SMALL)
    flat(c, Circ(160, 368, 5), SKIN)
    flat(c, Thick(166, 380, 186, 366, 2), SKIN)
    # procession: canopy carried by pages, the emperor in his underwear
    for x in (360, 540):
        flat(c, Thick(x, 470, x, 560, 3), (200, 170, 90))
    piece(c, Poly([(350, 470), (550, 470), (540, 450), (360, 450)]), (60, 120, 70) if "canopy" in d else (150, 40, 60), border=1.5, shadow=PROP)
    for x in range(360, 540, 16):
        flat(c, Poly([(x, 470), (x + 16, 470), (x + 8, 480)]), (230, 190, 80))
    for x in (350, 550):
        person(c, x, 592, (230, 190, 80), h=0.9)
    piece(c, [RRect(434, 520, 466, 552, 6), Circ(450, 508, 11), RRect(436, 552, 446, 590, 2), RRect(454, 552, 464, 590, 2)], SKIN, border=1.2,
          shadow=PROP)
    flat(c, RRect(434, 540, 466, 556, 3), (250, 250, 250))
    flat(c, Circ(453, 507, 1.4), INK)
    if "crown" not in d:
        piece(c, Poly([(438, 500), (462, 500), (466, 486), (458, 494), (450, 482), (442, 494), (434, 486)]), (230, 190, 60), shadow=SMALL)
        flat(c, [Circ(450, 494, 2.4), Circ(441, 496, 2), Circ(459, 496, 2)], (220, 40, 50))
    for x in (410, 490):
        person(c, x, 594, (90, 60, 110), h=0.85)
        flat(c, [Thick(x + 6, 566, x + 14, 546, 2)], SKIN)
    # trumpeters and a dog
    for x in (220, 680):
        person(c, x, 596, (40, 60, 120), h=1.0)
        flat(c, Thick(x + 8, 556, x + 34, 548, 2.4), (230, 190, 60))
        flat(c, Poly([(x + 14, 552), (x + 28, 549), (x + 28, 562), (x + 14, 562)]), (60, 160, 90) if ("banner" in d and x == 680) else (220, 50, 50))
    if "dog" not in d:
        piece(c, [Ell(780, 582, 18, 9), Circ(796, 572, 7), Ell(800, 566, 3, 6)], (200, 160, 110), border=1, shadow=SMALL)


L107_ELEMENTS = [
    cloud_el("cloud0", 200, 50, 0.6, 5), cloud_el("cloud1", 720, 70, 0.6, 6),
    bird_el("bird0", 600, 70, 8, speed=14),
]

L107_DIFFS = [
    ("loom", 374, 312, 0),
    ("bunting", 690, 176, 0),
    ("child", 160, 376, 0),
    ("canopy", 450, 460, 0),
    ("crown", 450, 494, 0),
    ("banner", 702, 556, 0),
    ("dog", 786, 576, 0),
]


# =================================================================== Level 108 Thumbelina
def l108_bg(c, d):
    sky(c, (190, 226, 240), (250, 244, 220), 300)
    layer(c, 260, [(10, 0.01, 0.4)], (170, 206, 150))
    # giant grass blades and leaves at the back
    rnd = random.Random(108)
    for k in range(30):
        x = rnd.uniform(0, 900)
        flat(c, Poly([(x - 8, 420), (x + 8, 420), (x + rnd.uniform(-30, 30), rnd.uniform(140, 260))]), lit((110, 170, 90), rnd.uniform(0.8, 1.1)))
    # pond with lily pads
    piece(c, Ell(560, 480, 320, 60), (110, 170, 200), shadow=None)
    flat(c, Ell(560, 474, 290, 46), (136, 192, 214))
    for x, y, r in ((470, 470, 70), (660, 490, 60), (800, 462, 46)):
        piece(c, Poly([(x + r * math.cos(a), y + r * 0.3 * math.sin(a)) for a in [i * 0.3 for i in range(20)]] + [(x, y)]), (90, 160, 90), shadow=SMALL)
    # Thumbelina on her lily pad, the toad on another
    hx, hy = lady(c, 470, 474, (90, 140, 220) if "dress" in d else (240, 140, 180), hair=(240, 200, 100), h=0.6)
    toad = (160, 120, 60) if "toad" in d else (110, 140, 70)
    piece(c, [Ell(660, 478, 26, 14), Circ(676, 464, 10)], toad, border=1.2, shadow=SMALL)
    flat(c, [Circ(672, 458, 3.5), Circ(682, 458, 3.5)], (250, 230, 90))
    # giant tulip and daisies
    flat(c, Thick(140, 600, 150, 300, 8), (80, 150, 70))
    piece(c, [Poly([(110, 300), (190, 300), (196, 250), (172, 268), (150, 230), (128, 268), (104, 250)])], (230, 220, 90) if "tulip" in d else (220, 50, 60),
          border=1.5, shadow=PROP)
    piece(c, Ell(122, 420, 40, 14), (90, 160, 80), shadow=SMALL)
    for x, y in ((300, 330), (860, 300)):
        flat(c, Thick(x, 600, x, y, 5), (90, 150, 70))
        piece(c, [Ell(x + 30 * math.cos(a), y + 30 * math.sin(a), 14, 6) for a in [i * math.pi / 6 for i in range(12)]], (250, 250, 246), shadow=SMALL)
        piece(c, Circ(x, y, 14), (240, 200, 60) if not ("daisy" in d and x == 860) else (220, 120, 60), shadow=None)
    # field mouse's door in a tree root, beetle, ladybird
    piece(c, Poly([(700, 600), (720, 520), (800, 500), (900, 520), (910, 600)]), (130, 96, 70), shadow=LAYER)
    piece(c, [arch(772, 812, 530, 590)[0], arch(772, 812, 530, 590)[1]], (60, 120, 170) if "door" in d else (200, 70, 50), border=1.5, shadow=SMALL)
    flat(c, Circ(804, 562, 3), (240, 200, 90))
    if "beetle" not in d:
        piece(c, [Ell(260, 560, 18, 12), Circ(276, 554, 7)], (40, 90, 70), border=1.2, shadow=SMALL)
        flat(c, [Thick(260, 548, 260, 572, 1.2), Thick(278, 548, 288, 540, 1.4), Thick(280, 550, 290, 546, 1.4)], (20, 40, 30))
    piece(c, [Ell(400, 580, 12, 9)], (240, 200, 50) if "spots" in d else (220, 40, 40), border=1, shadow=SMALL)
    flat(c, [Circ(396, 576, 2.4), Circ(404, 584, 2.4), Circ(404, 574, 2.4), Circ(396, 584, 2.4)], INK)
    piece(c, hill_strip(590, [(3, 0.02, 0.3)]), (110, 170, 90), shadow=LAYER)


L108_ELEMENTS = [
    cloud_el("cloud0", 300, 60, 0.7, 6),
    E("swallow", lambda c, m: (piece(c, [Ell(560, 120, 18, 7), Poly([(556, 118), (520, 100), (550, 124)]), Poly([(564, 118), (600, 96), (570, 124)]),
                                         Poly([(542, 122), (526, 134), (540, 128)])], (40, 50, 90), shadow=SMALL),
                               flat(c, Ell(566, 124, 8, 3), (250, 250, 250))), pivot=(560, 120),
      anim=dict(drift_across(510, 610, 24), bobAmplitude=(0, 14), bobSpeed=0.2, stretch=(0, 0.3), scaleSpeed=1.6)),
] + [E("dew%d" % i, (lambda x, y: lambda c, m: flat(c, Circ(x, y, 3), (240, 250, 255)))(x, y), anim=dict(twinkle=0.9, twinkleSpeed=0.5 + i * 0.1,
                                                                                                          phase=i * 0.2))
     for i, (x, y) in enumerate(((122, 414), (300, 300), (860, 270), (470, 464)))] + [
    E("butterfly", lambda c, m: flat(c, [Ell(700, 300, 7, 6), Ell(714, 300, 7, 6), Ell(702, 310, 5, 4), Ell(712, 310, 5, 4)], (250, 180, 60)),
      pivot=(707, 304), anim=dict(stretch=(0.6, 0), scaleSpeed=3, bobAmplitude=(40, 20), bobSpeed=0.1)),
]

L108_DIFFS = [
    ("dress", 470, 452, 0),
    ("toad", 666, 472, 0),
    ("tulip", 150, 272, 0),
    ("daisy", 860, 300, 0),
    ("door", 792, 560, 0),
    ("beetle", 266, 558, 0),
    ("spots", 400, 578, 0),
]

LEVELS = [
    ("Level104", "海的女儿", l104_bg, L104_ELEMENTS, L104_DIFFS, 140, OPTS),
    ("Level105", "卖火柴的小女孩", l105_bg, L105_ELEMENTS, L105_DIFFS, 140, dict(OPTS, weather=WEATHER105, anim_seconds=20.0, frames=40)),
    ("Level106", "丑小鸭", l106_bg, L106_ELEMENTS, L106_DIFFS, 140, OPTS),
    ("Level107", "皇帝的新装", l107_bg, L107_ELEMENTS, L107_DIFFS, 140, OPTS),
    ("Level108", "拇指姑娘", l108_bg, L108_ELEMENTS, L108_DIFFS, 140, OPTS),
]
