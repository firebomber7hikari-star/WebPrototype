# -*- coding: utf-8 -*-
"""Heian Japan, part 2 (paper-craft side views):
  Level77 凤凰堂 - the Phoenix Hall of Byodo-in across its lotus pond, wisteria in the foreground
  Level78 雪之晨 - "the snow of Kouro peak": a palace on a snowy morning, a lady rolls up the blind; snow weather cycle
"""
import math
import random

from fdcore import CLEAR, E, OVERCAST, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, drift_across, layer, sky
from levels_heian import GOLD, VERMILION, curved_roof, hall, kasumi, lady_seated, pine_jp, blossom_tree
from jp_kit import SKIN, ellipse_top, kimono
from weather import CLOUDY, cloud, snow_layer

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def phoenix(c, x, y, flip=False):
    k = -1 if flip else 1
    piece(c, [Poly([(x, y), (x + 8 * k, y - 6), (x + 6 * k, y - 16), (x + 2 * k, y - 10), (x - 6 * k, y - 4)]),
              Poly([(x - 2 * k, y - 4), (x - 14 * k, y - 16), (x - 18 * k, y - 8)])], GOLD, border=1, shadow=SMALL)


def monk(c, x, base, robe, h=1.0):
    piece(c, [Poly([(x - 11 * h, base), (x + 11 * h, base), (x + 8 * h, base - 32 * h), (x - 8 * h, base - 32 * h)])], robe, border=1.5, shadow=PROP)
    flat(c, Thick(x - 8 * h, base - 30 * h, x + 8 * h, base - 8 * h, 3 * h), (200, 170, 90))
    flat(c, Circ(x + 1 * h, base - 39 * h, 7 * h), SKIN)
    flat(c, Circ(x + 4 * h, base - 40 * h, 1.1 * h), INK)


# =================================================================== Level 77 Phoenix Hall
WIST77 = list(range(26, 200, 18))
WIST_DIFF = 5


def l77_bg(c, d):
    sky(c, (196, 218, 238), (250, 236, 214), 380)
    kasumi(c, 64, 560, 920, 20)
    kasumi(c, 110, -20, 300, 18)
    layer(c, 250, [(22, 0.007, 0.4), (8, 0.02, 1.2)], (150, 176, 166))
    layer(c, 292, [(10, 0.012, 1.0)], (128, 162, 140))
    c.rect(0, 356, W, 530, (110, 160, 182))
    for y in range(372, 528, 12):
        for x in range((y * 13) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (140, 186, 204))
    # reflection of the hall
    for x in range(200, 704, 34):
        flat(c, RRect(x - 3, 372, x + 3, 420), (196, 100, 80, 0.3))
    flat(c, Ell(450, 432, 150, 12), (90, 80, 80, 0.25))
    piece(c, RRect(120, 332, 780, 368, 2), (196, 186, 160), border=1.5, shadow=PROP)
    # wing towers, wings, central hall
    for tx, has in ((188, True), (718, "hoju" not in d)):
        hall(c, tx - 20, tx + 20, 334, 270, 30, 366, 1, blinds_up=(0,), rail=False)
        if has:
            piece(c, [Circ(tx, 230, 4), Poly([(tx - 2, 228), (tx + 2, 228), (tx, 218)])], GOLD, shadow=None)
    hall(c, 210, 372, 344, 298, 26, 366, 4, blinds_up=(0, 1, 2, 3))
    hall(c, 528, 690, 344, 298, 26, 366, 4, blinds_up=(0, 1, 2, 3))
    hall(c, 380, 520, 332, 236, 66, 366, 3, blinds_up=(0, 2))
    curved_roof(c, 372, 528, 296, 14, overhang=26)
    piece(c, Circ(450, 266, 16), (110, 80, 60), border=1.5, shadow=SMALL)
    if "amida" in d:
        for k in range(-2, 3):
            flat(c, [Thick(450 + k * 5, 252, 450 + k * 5, 280, 1.2), Thick(436, 266 + k * 5, 464, 266 + k * 5, 1.2)], (70, 50, 40))
    else:
        soft_union(c, [Circ(450, 266, 12)], (255, 220, 120), 0.6, spread=6)
        flat(c, Circ(450, 266, 8), (236, 196, 90))
        flat(c, [Circ(447, 265, 1), Circ(453, 265, 1)], INK)
    phoenix(c, 411, 166, flip=True)
    if "phoenix" not in d:
        phoenix(c, 489, 166)
    # bronze lantern on the island
    if "lantern" not in d:
        col = (110, 140, 120)
        piece(c, [RRect(442, 352, 458, 364, 1), RRect(447, 316, 453, 352, 1), RRect(438, 304, 462, 316, 2), Poly([(432, 304), (468, 304), (450, 290)]),
                  Circ(450, 287, 3)], col, border=1.2, shadow=PROP)
        flat(c, RRect(444, 306, 456, 314, 1), (255, 220, 140))
    # lotus
    for x, y in ((240, 470), (300, 492), (620, 482), (690, 500), (380, 506)):
        flat(c, Ell(x, y, 22, 6), (90, 150, 90))
    for x, y, col in ((248, 460, (240, 150, 180)), (628, 472, (250, 250, 246) if "lotus" in d else (240, 150, 180)), (386, 496, (240, 150, 180))):
        piece(c, [Poly([(x - 8, y), (x + 8, y), (x + 10, y - 8), (x + 4, y - 4), (x, y - 14), (x - 4, y - 4), (x - 10, y - 8)])], col, shadow=SMALL)
    # near bank, monks, pine, wisteria trellis
    piece(c, hill_strip(522, [(5, 0.012, 0.4), (2, 0.04, 1.0)]), (204, 192, 150), shadow=LAYER)
    for y in range(536, 600, 10):
        flat(c, Thick(220, y, 900, y + 2 * math.sin(y), 1), (190, 176, 136))
    monk(c, 520, 586, (110, 110, 120) if "monk" in d else (230, 150, 60))
    monk(c, 572, 590, (40, 40, 46))
    pine_jp(c, 850, 606, 1.6)
    piece(c, [RRect(14, 466, 22, 612, 1), RRect(196, 466, 204, 612, 1), RRect(0, 460, 216, 470, 1)], (130, 96, 70), shadow=PROP)
    for i, x in enumerate(WIST77):
        col = (246, 244, 250) if (i == WIST_DIFF and "wisteria" in d) else (160, 110, 200)
        ln = 50 + (i * 17) % 30
        piece(c, [Ell(x, 470 + ln * 0.5, 7, ln * 0.5)], col, shadow=SMALL)
        for j in range(0, ln, 8):
            flat(c, Circ(x + (2 if j % 16 else -2), 474 + j, 3), lit(col, 1.12))
        flat(c, Ell(x + 6, 472, 8, 3), (90, 150, 80))


def l77_boat(c, m):
    piece(c, Poly([(600, 440), (680, 440), (670, 452), (610, 452)]), (130, 90, 60), border=1.2, shadow=SMALL)
    monk(c, 652, 442, (40, 40, 46), h=0.6)
    flat(c, Thick(620, 410, 600, 458, 1.6), (110, 80, 60))


L77_ELEMENTS = [
    E("boat", l77_boat, pivot=(640, 452), anim=dict(drift_across(596, 684, 10), bobAmplitude=(0, 1.5), bobSpeed=0.4)),
    bird_el("bird0", 300, 150, 8, speed=16), bird_el("bird1", 326, 140, 6, speed=16),
] + [E("sparkle%d" % i, (lambda x, y: lambda c, m: flat(c, Poly(star_pts(x, y, 5, 1.6, points=4, rot=0)), (250, 250, 240)))(x, y),
       anim=dict(twinkle=0.9, twinkleSpeed=0.5 + i * 0.13, phase=i * 0.21)) for i, (x, y) in enumerate(((300, 400), (520, 420), (760, 410),
                                                                                                       (420, 470), (840, 480)))]

L77_DIFFS = [
    ("phoenix", 489, 158, 0),
    ("amida", 450, 266, 0),
    ("hoju", 718, 226, 0),
    ("lantern", 450, 324, 0),
    ("lotus", 628, 466, 0),
    ("wisteria", WIST77[WIST_DIFF], 500, 0),
    ("monk", 520, 566, 0),
]


# =================================================================== Level 78 snowy morning at the palace
STEPS78 = [(SNOW, 10), (OVERCAST, 6), (CLEAR, 8)]
WEATHER78 = dict(steps=STEPS78, blend=3.0, tints={SNOW: (0.9, 0.92, 0.98), OVERCAST: (0.88, 0.9, 0.94)})
PINE78 = (660, 432, 1.3)


def snow_cap_pine(c, x, base, s):
    pads = [(x - 20 * s, base - 46 * s, 24 * s), (x + 30 * s, base - 62 * s, 22 * s), (x + 4 * s, base - 82 * s, 26 * s), (x - 26 * s, base - 70 * s, 18 * s)]
    piece(c, [Ell(px, py - r * 0.26, r * 0.9, r * 0.24) for px, py, r in pads], (248, 250, 255), shadow=None)


def l78_bg(c, d):
    sky(c, (200, 210, 226), (238, 240, 246), 380)
    layer(c, 250, [(22, 0.007, 0.4), (8, 0.02, 1.2)], (226, 232, 242))
    layer(c, 296, [(10, 0.012, 1.0)], (212, 220, 234))
    piece(c, hill_strip(380, [(4, 0.01, 0.4)]), (240, 244, 250), shadow=LAYER)
    for x, y, rx in ((620, 420, 120), (300, 470, 160), (780, 520, 140)):
        flat(c, Ell(x, y, rx, 10), (222, 230, 244))
    piece(c, Ell(740, 452, 130, 22), (200, 222, 238), shadow=SMALL)
    flat(c, Thick(650, 450, 820, 446, 2), (236, 244, 250))
    # palace hall with snow on the roof
    up = () if "blind" in d else (2,)
    hall(c, 20, 520, 352, 250, 70, 384, 5, blinds_up=up)
    flat(c, [Ell(270, 182, 150, 9), Ell(140, 214, 70, 8), Ell(400, 214, 70, 8), Ell(60, 238, 40, 6), Ell(480, 238, 40, 6)], (250, 252, 255))
    if not up == ():
        lady_seated(c, 270, 348, [(150, 40, 70), (250, 220, 230), (200, 80, 110), (240, 240, 246)])
        flat(c, Thick(276, 300, 300, 258, 2), (110, 90, 60))
    lady_seated(c, 360, 348, [(70, 90, 150), (240, 200, 200), (250, 240, 236)])
    if "brazier" not in d:
        piece(c, Poly([(392, 348), (424, 348), (420, 330), (396, 330)]), (60, 50, 50), border=1.2, shadow=SMALL)
        soft_union(c, [Ell(408, 330, 10, 4)], (255, 150, 60), 0.7, spread=8)
        flat(c, Ell(408, 331, 8, 2.5), (255, 120, 50))
    piece(c, RRect(440, 340, 500, 348, 2), (40, 30, 34), border=1, shadow=SMALL)
    piece(c, Ell(470, 334, 18, 9), (250, 252, 255), shadow=SMALL)
    if "rabbit" not in d:
        flat(c, [Circ(478, 331, 1.8), Circ(484, 332, 1.8)], (220, 30, 40))
        flat(c, [Ell(474, 323, 3, 7), Ell(480, 322, 3, 7)], (70, 140, 70))
    # pine with snow and a crow, plum in bloom
    x, b, s = PINE78
    pine_jp(c, x, b, s)
    snow_cap_pine(c, x, b, s)
    if "crow" not in d:
        cx, cy = x + 30 * s, b - 62 * s - 10
        piece(c, [Ell(cx, cy, 9, 6), Circ(cx + 8, cy - 5, 4.5), Poly([(cx - 8, cy), (cx - 16, cy - 4), (cx - 14, cy + 3)])], (30, 30, 36), shadow=SMALL)
        flat(c, Poly([(cx + 12, cy - 5), (cx + 18, cy - 4), (cx + 12, cy - 3)]), (60, 60, 60))
    blossom_tree(c, 830, 610, 1.6, (246, 244, 250) if "plum" in d else (210, 50, 80), 781, trunk=(70, 56, 54))
    # children building a snow mountain
    piece(c, ellipse_top(560, 572, 54, 40), (250, 252, 255), shadow=PROP)
    if "stick" not in d:
        flat(c, Thick(560, 532, 560, 506, 2), (110, 80, 60))
        flat(c, Poly([(561, 506), (576, 510), (561, 516)]), (220, 50, 60))
    kimono(c, 490, 584, (90, 140, 200) if "child" in d else (220, 120, 60), h=0.75)
    kimono(c, 626, 586, (120, 60, 110), h=0.72, hair="woman")
    rnd = random.Random(78)
    for k in range(16):
        flat(c, Ell(200 + k * 18, 560 + 8 * math.sin(k), 3, 2), (214, 222, 238))
    pine_jp(c, 40, 612, 1.5)
    snow_cap_pine(c, 40, 612, 1.5)


def l78_sun(c, m):
    piece(c, Circ(820, 80, 24), (255, 236, 180), border=2, shadow=PROP)


L78_ELEMENTS = [
    E("sun", l78_sun, weather=W_(CLEAR), anim=dict(pulse=0.03, scaleSpeed=0.3)),
    cloud("cloudA", 200, 70, 0.9, (226, 230, 238), W_(SNOW, OVERCAST), anim=dict(bobAmplitude=(26, 0), bobSpeed=0.02)),
    cloud("cloudB", 600, 50, 1.0, (214, 220, 230), W_(SNOW, OVERCAST), anim=dict(bobAmplitude=(-22, 0), bobSpeed=0.025)),
    snow_layer("snowFar", 781, 50, 1.4, 2.6, 26),
    snow_layer("snowNear", 782, 26, 3.0, 4.6, 46, sway=12),
    E("brazier_glow", lambda c, m: soft_union(c, [Circ(408, 330, 8)], (255, 170, 80), 0.5, spread=14), show="A",
      anim=dict(twinkle=0.3, twinkleSpeed=1.3)),
    bird_el("bird0", 380, 140, 8, col=(40, 40, 46), speed=14, weather=W_(CLEAR)),
]

L78_DIFFS = [
    ("blind", 270, 300, 0),
    ("brazier", 408, 336, 0),
    ("rabbit", 480, 328, 0),
    ("crow", int(PINE78[0] + 30 * PINE78[2]), int(PINE78[1] - 62 * PINE78[2] - 12), 0),
    ("plum", 830, 470, 0),
    ("stick", 566, 512, 0),
    ("child", 490, 560, 0),
]

LEVELS = [
    ("Level77", "凤凰堂", l77_bg, L77_ELEMENTS, L77_DIFFS, 140, OPTS),
    ("Level78", "雪之晨", l78_bg, L78_ELEMENTS, L78_DIFFS, 140, dict(OPTS, weather=WEATHER78, anim_seconds=24.0, frames=48)),
]
