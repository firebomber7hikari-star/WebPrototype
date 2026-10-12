# -*- coding: utf-8 -*-
"""Tang (618-907) and Song (960-1279) China, paper-craft side views, full-bleed:
  Level99  长安西市   - Chang'an west market: camel caravans, Sogdian merchants, wine flag, the Big Wild Goose Pagoda
  Level100 清明上河图 - the Rainbow Bridge over the Bian river: a cargo boat shooting the bridge, crowds, shops
  Level101 仕女游春   - Tang court ladies riding out in spring beside the Qujiang pond, peonies, kites
  Level102 西湖       - West Lake: Leifeng pagoda, the Broken Bridge, Su causeway willows, a lady with an umbrella; clear -> rain
  Level103 元宵灯会   - the lantern festival: lantern tower, dragon and lion dances, fireworks; day / night
"""
import math
import random

from fdcore import CLEAR, E, H, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_el, drift_across, gy, layer, sky, smoke_el
from stylekit import day_night, star_field, window_glow
from weather import CLOUDY, SUNNY, WET, cloud, rain_layer
from levels_heian import blossom_tree
from levels_europe import firework
from levels_meiji import willow_el, willow_trunk
from cn_kit import (GLAZE, GOLDEN, GREY_TILE, RED, SKIN, arch, arch_bridge, camel, cn_hall, cn_roof, city_wall, ellipse_top, gate_tower, hanfu,
                    horse_cn, junk, lantern_cn, lotus_pond, pagoda)

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def shop(c, x0, x1, base, h, wall=(180, 140, 100), roof=GREY_TILE, awning=None, sign=None):
    piece(c, RRect(x0, base - h, x1, base, 1), wall, border=1.5, shadow=PROP)
    flat(c, RRect(x0 + 8, base - h * 0.62, x1 - 8, base, 0), (90, 70, 56))
    cn_roof(c, x0, x1, base - h, 16, roof, curl=8, ornaments=False)
    if awning:
        piece(c, Poly([(x0 - 4, base - h * 0.62), (x1 + 4, base - h * 0.62), (x1 + 14, base - h * 0.45), (x0 - 14, base - h * 0.45)]), awning,
              border=1, shadow=SMALL)
    if sign:
        piece(c, RRect(x0 + 6, base - h * 0.95, x0 + 22, base - h * 0.66, 1), sign, border=1, shadow=SMALL)
        flat(c, Thick(x0 + 14, base - h * 0.92, x0 + 14, base - h * 0.7, 1.6), (240, 230, 200))


def wine_flag(eid, x, base, h, col, variant_col=None):
    def d(c, m):
        cc = variant_col if (m and variant_col) else col
        flat(c, Thick(x, base, x, base - h, 3), (110, 80, 60))
        piece(c, Poly([(x + 1, base - h + 2), (x + 34, base - h + 2), (x + 34, base - h + 70), (x + 26, base - h + 62), (x + 18, base - h + 70),
                       (x + 10, base - h + 62), (x + 1, base - h + 70)]), cc, border=1.2, shadow=SMALL)
        flat(c, Circ(x + 17, base - h + 26, 8), (240, 230, 200))
    return E(eid, d, pivot=(x, base - h + 30), variant=bool(variant_col), anim=dict(swingAngle=3, swingSpeed=0.5, stretch=(0.08, 0), scaleSpeed=1.1))


def rider_lady(c, x, base, horse_col, robe, saddle=(200, 40, 50), flip=False, fan=None):
    horse_cn(c, x, base, horse_col, flip=flip, saddle=saddle)
    hx, hy = hanfu(c, x, base - 46, robe, hat="tang_lady", h=0.9)
    if fan:
        flat(c, Thick(hx + 8, hy + 10, hx + 14, hy - 2, 1.2), (110, 80, 60))
        piece(c, Circ(hx + 15, hy - 6, 6), fan, border=1, shadow=SMALL)
    return hx, hy


# =================================================================== Level 99 Chang'an west market
def l99_bg(c, d):
    sky(c, (180, 206, 230), (250, 232, 200), 340)
    layer(c, 220, [(20, 0.007, 0.4)], (176, 180, 186))
    pagoda(c, 770, 300, 92, 7, 24, wall=(222, 196, 150), roof=(110, 100, 90), finial="finial" not in d)
    city_wall(c, -10, 910, 250, 330)
    gate_tower(c, 300, 250, w=180, h=56)
    # shops
    for i, (x0, x1) in enumerate(((-10, 120), (126, 250), (256, 380), (386, 510), (516, 640), (646, 770), (776, 910))):
        aw = ((80, 150, 200) if "awning" in d else (200, 80, 60)) if i == 3 else [(200, 80, 60), (90, 130, 90), (220, 180, 90)][i % 3]
        shop(c, x0, x1, 452, 110, awning=aw, sign=(40, 40, 60) if i % 2 else None)
    for i, x in enumerate((60, 316, 572, 830)):
        lantern_cn(c, x, 392, ((60, 160, 90) if "lantern" in d else (220, 50, 40)) if i == 2 else (220, 50, 40), r=9)
    piece(c, RRect(-10, 450, 910, 612, 0), (210, 190, 150), shadow=LAYER)
    for y in range(466, 600, 20):
        flat(c, Thick(0, y, 900, y, 1), (194, 174, 134))
    # caravan, merchants, ladies
    camel(c, 120, 586, load=(60, 110, 170) if "load" in d else (150, 60, 50))
    camel(c, 250, 590, col=(186, 150, 100), load=(220, 180, 80))
    hx, hy = hanfu(c, 330, 592, (60, 90, 120), hat="none", beard=(60, 40, 30))
    flat(c, Poly([(hx - 8, hy - 4), (hx + 8, hy - 4), (hx + 2, hy - 22)]), (90, 140, 90) if "hat" in d else (200, 60, 50))
    hanfu(c, 520, 594, (90, 120, 200) if "robe" in d else (220, 100, 120), hat="tang_lady")
    hanfu(c, 570, 594, (240, 200, 120), hat="tang_lady")
    piece(c, RRect(640, 520, 740, 560, 2), (150, 110, 70), border=1.2, shadow=PROP)
    for k in range(6):
        piece(c, [Circ(656 + k * 14, 514, 6), Circ(662 + k * 14, 506, 5)], (120, 60, 130), shadow=None)
    hanfu(c, 690, 596, (150, 110, 70), hat="futou")
    horse_cn(c, 830, 596, (200, 170, 130), flip=True)
    hanfu(c, 832, 552, (60, 80, 140), hat="futou", h=0.9)


def l99_dancer(c, m):
    x, base = 430, 596
    piece(c, [Poly([(x - 22, base), (x + 22, base), (x + 6, base - 30), (x - 6, base - 30)]), Circ(x, base - 40, 7)], (230, 80, 90), border=1.2,
          shadow=PROP)
    flat(c, Circ(x, base - 40, 6), SKIN)
    flat(c, [Thick(x - 6, base - 30, x - 30, base - 46, 2), Thick(x + 6, base - 30, x + 30, base - 46, 2)], (250, 220, 120))


L99_ELEMENTS = [
    cloud_el("cloud0", 160, 60, 0.7, 6), cloud_el("cloud1", 560, 80, 0.5, 5),
    wine_flag("wineflag", 760, 452, 200, (60, 100, 160), variant_col=(200, 60, 50)),
    E("dancer", l99_dancer, pivot=(430, 570), anim=dict(spinSpeed=0.5, spinShade=0.2)),
    bird_el("bird0", 450, 120, 8, speed=16), bird_el("bird1", 476, 110, 6, speed=16),
    bird_el("bird2", 620, 160, 7, speed=12),
]

L99_DIFFS = [
    ("finial", 770, 100, 0),
    ("awning", 448, 380, 0),
    ("lantern", 572, 392, 0),
    ("load", 120, 534, 0),
    ("hat", 331, 538, 0),
    ("robe", 520, 572, 0),
    ("wineflag", 777, 300, 0),
]


# =================================================================== Level 100 along the river at Qingming
def rainbow_bridge(c, x0, x1, base, top):
    n = 20
    arc = [(x0 + (x1 - x0) * k / n, base - (base - top) * math.sin(math.pi * k / n)) for k in range(n + 1)]
    for k in range(0, n + 1, 2):
        x, y = arc[k]
        flat(c, Thick(x, y, x + (8 if k < n / 2 else -8), base + 20, 4), (120, 86, 60))
    piece(c, Poly(arc + [(x, y + 12) for x, y in reversed(arc)]), (160, 120, 84), border=1.5, shadow=PROP)
    rail = [(x, y - 14) for x, y in arc]
    flat(c, [Thick(rail[i][0], rail[i][1], rail[i + 1][0], rail[i + 1][1], 2.5) for i in range(n)], (130, 96, 66))
    return arc


def l100_bg(c, d):
    sky(c, (200, 214, 222), (240, 232, 214), 300)
    layer(c, 230, [(14, 0.008, 0.4)], (180, 186, 176))
    for i, (x0, x1) in enumerate(((-10, 110), (114, 220), (680, 790), (794, 910))):
        shop(c, x0, x1, 340, 80, wall=(196, 170, 130), awning=[(200, 80, 60), (90, 130, 90)][i % 2])
    c.rect(0, 340, W, 480, (140, 160, 160))
    for y in range(350, 478, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (166, 184, 182))
    # cargo boat shooting the bridge (mast lowered)
    junk(c, 300, 470, 300, hull=(120, 86, 60), sail=None, roof=(60, 110, 160) if "boatroof" in d else (176, 150, 100))
    flat(c, Thick(380, 440, 560, 380, 4), (110, 80, 60))
    for x in (340, 380, 540, 580):
        hanfu(c, x, 440, (120, 100, 80), hat="straw", hat_col=(200, 176, 120), h=0.7)
    arc = rainbow_bridge(c, 160, 740, 340, 250)
    rnd = random.Random(100)
    for k in range(1, 20):
        x, y = arc[k]
        col = rnd.choice(((60, 70, 110), (150, 60, 70), (90, 110, 80), (200, 170, 110), (110, 70, 110)))
        hanfu(c, x, y, col, hat=rnd.choice(("futou", "bun", "straw")), h=0.62)
    # near bank: street with stalls
    piece(c, RRect(-10, 478, 910, 612, 0), (200, 180, 140), shadow=LAYER)
    for y in range(492, 600, 18):
        flat(c, Thick(0, y, 900, y, 1), (186, 164, 124))
    flat(c, Thick(140, 600, 146, 500, 2.5), (110, 80, 60))
    piece(c, ellipse_top(146, 504, 50, 22), (230, 200, 120) if "umbrella" in d else (240, 240, 230), border=1.2, shadow=PROP)
    piece(c, RRect(100, 540, 190, 566, 2), (150, 110, 70), border=1.2, shadow=PROP)
    hanfu(c, 210, 596, (110, 100, 80), hat="futou")
    flat(c, Thick(260, 520, 330, 520, 3), (110, 80, 60))
    piece(c, [RRect(278, 522, 312, 568, 3), Poly([(274, 524), (316, 524), (295, 510)])], (60, 110, 160) if "sedan" in d else (180, 50, 40), border=1.2,
          shadow=PROP)
    for bx in (250, 340):
        hanfu(c, bx, 598, (200, 180, 140), hat="straw", hat_col=(200, 176, 120), h=0.9)
    if "donkey" not in d:
        for lx in (-14, -6, 8, 14):
            flat(c, RRect(460 + lx - 2, 566, 460 + lx + 2, 592, 1), (110, 100, 100))
        piece(c, [Ell(460, 560, 22, 10), Poly([(476, 556), (488, 538), (494, 542), (482, 560)]), Ell(494, 540, 8, 5), Poly([(488, 534), (490, 522), (494, 534)])],
              (130, 120, 120), border=1.2, shadow=PROP)
        piece(c, RRect(446, 540, 474, 552, 2), (200, 180, 140), shadow=SMALL)
    hanfu(c, 560, 596, (60, 60, 90), hat="wing", hat_col=(60, 110, 160) if "hat" in d else (30, 28, 32))
    shop(c, 640, 900, 600, 100, wall=(196, 170, 130), awning=(200, 80, 60), sign=(60, 130, 80) if "sign" in d else (40, 40, 60))
    lantern_cn(c, 760, 520, (240, 236, 226) if "lantern" in d else (220, 50, 40), r=9)


L100_ELEMENTS = [
    cloud_el("cloud0", 300, 60, 0.7, 6), cloud_el("cloud1", 680, 80, 0.5, 5),
] + [willow_el("willow%d" % i, x, 340, i * 0.4) for i, x in enumerate((60, 840))] + [
    bird_el("bird0", 450, 150, 8, speed=14),
    E("ripple", lambda c, m: flat(c, Thick(300, 474, 600, 474, 2), (200, 220, 220)), anim=dict(twinkle=0.7, twinkleSpeed=0.8)),
]

L100_DIFFS = [
    ("boatroof", 440, 430, 0),
    ("umbrella", 146, 494, 0),
    ("sedan", 295, 544, 0),
    ("donkey", 470, 556, 0),
    ("hat", 561, 548, 0),
    ("sign", 662, 550, 0),
    ("lantern", 760, 520, 0),
]


# =================================================================== Level 101 Tang ladies' spring outing
def peony(c, x, y, col, r=12):
    piece(c, [Circ(x + r * 0.6 * math.cos(a), y + r * 0.5 * math.sin(a), r * 0.6) for a in (0, 1.26, 2.5, 3.8, 5.0)], col, shadow=SMALL)
    flat(c, Circ(x, y, r * 0.4), lit(col, 0.8))
    flat(c, Circ(x, y, r * 0.18), (250, 220, 100))


def l101_bg(c, d):
    sky(c, (180, 214, 236), (252, 238, 220), 340)
    layer(c, 230, [(20, 0.007, 0.4), (8, 0.02, 1.2)], (160, 186, 176))
    c.rect(0, 280, W, 380, (120, 170, 190))
    for y in range(290, 378, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (150, 194, 210))
    cn_hall(c, 600, 760, 300, 236, 34, roof=(60, 140, 120) if "roof" in d else GLAZE, bays=4)
    for x in range(590, 780, 30):
        flat(c, Thick(x, 300, x, 340, 3), (160, 50, 40))
    piece(c, hill_strip(380, [(5, 0.01, 0.3)]), (140, 180, 110), shadow=LAYER)
    for x, s in ((120, 1.0), (300, 0.9)):
        blossom_tree(c, x, 400, s, (246, 200, 214), 1010 + x)
    # peony beds
    rnd = random.Random(101)
    for k in range(18):
        x = 20 + k * 50 + rnd.uniform(-8, 8)
        y = 430 + rnd.uniform(0, 20)
        flat(c, [Ell(x - 8, y + 6, 10, 5), Ell(x + 8, y + 6, 10, 5)], (80, 140, 80))
        col = rnd.choice(((230, 80, 120), (250, 200, 220), (240, 240, 246), (200, 60, 90)))
        if k == 13 and "peony" in d:
            col = (250, 210, 80)
        peony(c, x, y, col)
    piece(c, hill_strip(470, [(3, 0.012, 0.4)]), (160, 196, 120), shadow=LAYER)
    # riders and attendants
    rider_lady(c, 200, 590, (240, 236, 226), (230, 100, 130), saddle=(200, 40, 50))
    rider_lady(c, 380, 594, (130, 90, 60) if "horse" in d else (60, 50, 50), (110, 150, 210), saddle=(60, 120, 90) if "saddle" in d else (220, 180, 70))
    rider_lady(c, 560, 592, (200, 170, 130), (240, 200, 110) if "robe" not in d else (120, 200, 160), saddle=(200, 40, 50),
               fan=(230, 90, 120) if "fan" not in d else (90, 140, 220))
    for x, col in ((690, (220, 120, 140)), (750, (200, 120, 60) if "attendant" in d else (120, 160, 200)), (810, (240, 200, 120))):
        hanfu(c, x, 596, col, hat="tang_lady")
    hanfu(c, 870, 598, (90, 80, 70), hat="futou")


def l101_kite(x, y, col, i):
    def d(c, m):
        piece(c, Poly([(x, y - 18), (x + 16, y), (x, y + 18), (x - 16, y)]), col, border=1.2, shadow=SMALL)
        flat(c, [Thick(x, y + 18, x - 6, y + 50, 1.2), Thick(x - 6, y + 50, x + 4, y + 80, 1.2)], (200, 60, 60))
    return E("kite%d" % i, d, pivot=(x, y + 20), anim=dict(bobAmplitude=(8, 10), bobSpeed=0.12 + i * 0.03, swingAngle=10, swingSpeed=0.3))


def butterfly_el(i, x, y, col):
    def d(c, m):
        flat(c, [Ell(x - 5, y - 3, 5, 4), Ell(x + 5, y - 3, 5, 4), Ell(x - 4, y + 3, 4, 3), Ell(x + 4, y + 3, 4, 3)], col)
        flat(c, Ell(x, y, 1.4, 5), (60, 50, 50))
    return E("butterfly%d" % i, d, pivot=(x, y), anim=dict(stretch=(0.6, 0), scaleSpeed=3, bobAmplitude=(30, 16), bobSpeed=0.12 + i * 0.03,
                                                           phase=i * 0.3))


L101_ELEMENTS = [
    l101_kite(200, 120, (230, 90, 110), 0), l101_kite(480, 90, (90, 150, 220), 1),
    cloud_el("cloud0", 720, 70, 0.6, 5),
] + [butterfly_el(i, x, y, col) for i, (x, y, col) in enumerate(((150, 430, (250, 220, 90)), (450, 420, (240, 150, 200)), (820, 440, (150, 200, 250))))] + \
    [willow_el("willow%d" % i, x, 300, i * 0.4) for i, x in enumerate((500, 860))]

L101_DIFFS = [
    ("roof", 680, 210, 0),
    ("peony", 20 + 13 * 50, 440, 0),
    ("horse", 380, 560, 0),
    ("saddle", 380, 546, 0),
    ("robe", 560, 520, 0),
    ("fan", 576, 484, 0),
    ("attendant", 750, 576, 0),
]


# =================================================================== Level 102 West Lake (clear -> rain)
STEPS102 = [(CLEAR, 9), (OVERCAST, 5), (RAIN, 9), (OVERCAST, 4)]
WEATHER102 = dict(steps=STEPS102, blend=3.0, tints={OVERCAST: (0.86, 0.88, 0.92), RAIN: (0.74, 0.78, 0.86)})
CAUSEWAY_WILLOWS = [120, 240, 420, 600, 780]


def _only_a(e, flag):
    if flag:
        e.show = "A"
    return e


def wupeng(x, y, awning, k=1.0):
    def d(c, m):
        aw = awning(m) if callable(awning) else awning
        piece(c, Poly([(x - 50 * k, y - 8 * k), (x + 50 * k, y - 10 * k), (x + 40 * k, y + 4 * k), (x - 42 * k, y + 4 * k)]), (90, 70, 56), border=1.2,
              shadow=SMALL)
        piece(c, ellipse_top(x - 4 * k, y - 8 * k, 24 * k, 16 * k), aw, border=1, shadow=SMALL)
        hanfu(c, x + 34 * k, y - 8 * k, (90, 90, 110), hat="straw", hat_col=(200, 176, 120), h=0.55 * k)
    return d


def l102_bg(c, d):
    sky(c, (190, 210, 222), (236, 234, 224), 300)
    layer(c, 200, [(30, 0.006, 0.4), (14, 0.02, 1.0)], (170, 184, 190))
    layer(c, 240, [(18, 0.01, 1.2)], (140, 166, 160))
    piece(c, Poly([(-20, 300), (60, 250), (160, 240), (240, 270), (300, 300)]), (120, 150, 120), shadow=LAYER)
    pagoda(c, 140, 260, 64, 5, 26, wall=(200, 150, 110), roof=(90, 84, 80), finial="finial" not in d)
    c.rect(0, 296, W, H, (150, 180, 186))
    for y in range(306, 600, 14):
        for x in range((y * 13) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (176, 200, 204))
    # Su causeway with willows
    piece(c, RRect(-10, 360, 910, 372, 2), (150, 170, 120), shadow=SMALL)
    for i, x in enumerate(CAUSEWAY_WILLOWS):
        if not (i == 3 and "willow" in d):
            willow_trunk(c, x, 366)
    # island pavilion
    piece(c, Ell(470, 336, 70, 12), (130, 160, 110), shadow=SMALL)
    cn_hall(c, 440, 500, 336, 300, 22, roof=(60, 140, 120) if "pavilion" in d else GREY_TILE, bays=2, terrace=6, doors=False)
    # Broken Bridge
    arch_bridge(c, 560, 860, 420, 380)
    # near bank with lotus and the lady in white
    lotus_pond(c, [(60, 490, True), (130, 510, False), (220, 486, (250, 250, 246) if "lotus" in d else True), (300, 520, False), (380, 500, True)])
    piece(c, hill_strip(540, [(5, 0.012, 0.3), (2, 0.04, 1.0)]), (120, 150, 100), shadow=LAYER)
    hx, hy = hanfu(c, 600, 594, (246, 246, 250), hat="lady")
    flat(c, Thick(hx + 8, hy + 10, hx + 12, hy - 34, 1.4), (110, 80, 60))
    piece(c, ellipse_top(hx + 12, hy - 32, 28, 14), (90, 140, 200) if "umbrella" in d else (220, 200, 150), border=1.2, shadow=PROP)
    hanfu(c, 660, 596, (60, 100, 150), hat="futou")
    hanfu(c, 540, 596, (90, 90, 160) if "qing" in d else (110, 170, 130), hat="bun", h=0.8)


L102_ELEMENTS = [
    E("sun", lambda c, m: piece(c, Circ(780, 80, 22), (255, 226, 150), border=2, shadow=PROP), weather=SUNNY),
    cloud("cloudA", 320, 70, 0.9, (252, 252, 248), W_(CLEAR, OVERCAST), anim=dict(bobAmplitude=(26, 0), bobSpeed=0.02)),
    cloud("cloudB", 600, 60, 1.0, (200, 206, 216), CLOUDY, anim=dict(bobAmplitude=(-22, 0), bobSpeed=0.025)),
    rain_layer("rain", 102, 46, 26, 1.8, 0.5, 300),
] + [_only_a(willow_el("willow%d" % i, x, 366, i * 0.3), i == 3) for i, x in enumerate(CAUSEWAY_WILLOWS)] + [
    E("boat1", wupeng(380, 440, lambda m: (200, 110, 60) if m else (40, 40, 46)), pivot=(380, 444), variant=True,
      anim=dict(bobAmplitude=(0, 2), bobSpeed=0.3, swingAngle=1, swingSpeed=0.2)),
    E("boat2", wupeng(760, 470, (40, 40, 46), 0.8), pivot=(760, 474), anim=dict(drift_across(716, 804, -8), bobAmplitude=(0, 2), bobSpeed=0.3)),
    bird_el("egret0", 300, 200, 10, col=(250, 250, 250), speed=14, weather=SUNNY),
]

L102_DIFFS = [
    ("finial", 140, 96, 0),
    ("willow", CAUSEWAY_WILLOWS[3], 300, 0),
    ("pavilion", 470, 280, 0),
    ("boat", 376, 424, 0),
    ("lotus", 220, 476, 0),
    ("umbrella", 613, 516, 0),
    ("qing", 540, 578, 0),
]


# =================================================================== Level 103 lantern festival (day / night)
DN103 = day_night(40.0, tint=(0.26, 0.26, 0.5))
STRING103 = [(k * 60 + 30, 150 + 18 * math.sin(math.pi * k / 7.5)) for k in range(15)]


def rabbit_lantern(c, x, y, col):
    piece(c, [Ell(x, y, 16, 11), Circ(x + 12, y - 6, 7), Ell(x + 10, y - 18, 3, 8), Ell(x + 15, y - 17, 3, 8)], col, border=1, shadow=SMALL)
    flat(c, Circ(x + 15, y - 7, 1.6), (220, 40, 50))
    for wx in (x - 8, x + 8):
        flat(c, Circ(wx, y + 12, 3.5), (120, 90, 60))


def l103_bg(c, d):
    sky(c, (160, 190, 220), (236, 214, 196), 440)
    for x0, x1 in ((330, 420), (480, 570)):
        shop(c, x0 - 6, x1 + 6, 430, 120, wall=(150, 104, 80), roof=GREY_TILE)
    for i, (x0, x1) in enumerate(((-10, 160), (166, 330), (570, 734), (740, 910))):
        shop(c, x0, x1, 420, 170, wall=(176, 120, 90), roof=GREY_TILE, awning=(200, 60, 50))
    # lantern tower in the middle
    piece(c, RRect(420, 200, 480, 430, 2), (150, 60, 40), border=1.5, shadow=PROP)
    for k, y in enumerate((210, 270, 330)):
        cn_roof(c, 400 + k * 6, 500 - k * 6, y, 14, (60, 60, 70), curl=8, ornaments=False)
    for y in (240, 300, 370):
        for x in (410, 450, 490):
            lantern_cn(c, x, y, (220, 50, 40), r=8)
    if "tower" not in d:
        piece(c, [Circ(450, 172, 10), Poly([(444, 166), (456, 166), (450, 148)])], GOLDEN, border=1, shadow=SMALL)
    # strings of lanterns across the street
    flat(c, [Thick(STRING103[i][0], STRING103[i][1], STRING103[i + 1][0], STRING103[i + 1][1], 1.2) for i in range(14)], (60, 50, 50))
    for i, (x, y) in enumerate(STRING103):
        if 6 <= i <= 8:
            continue
        col = (240, 190, 60) if i % 2 else (220, 50, 40)
        if i == 11 and "string" in d:
            col = (90, 160, 90)
        lantern_cn(c, x, y + 16, col, r=8)
    rabbit_lantern(c, 200, 300, (90, 160, 220) if "rabbit" in d else (250, 250, 246))
    if "fish" not in d:
        piece(c, [Ell(700, 300, 22, 10), Poly([(678, 300), (664, 290), (664, 310)])], (240, 120, 60), border=1, shadow=SMALL)
        flat(c, Circ(714, 298, 2), INK)
    piece(c, RRect(-10, 420, 910, 612, 0), (170, 150, 120), shadow=LAYER)
    for y in range(434, 600, 18):
        flat(c, Thick(0, y, 900, y, 1), (156, 136, 106))
    # lion dance, crowd, girl with a lantern, riddle slips
    lion = (60, 140, 200) if "lion" in d else (220, 170, 60)
    piece(c, [Ell(170, 548, 46, 22), Circ(120, 532, 20)], lion, border=1.5, shadow=PROP)
    flat(c, [Circ(112, 526, 4), Circ(126, 524, 4)], (250, 250, 250))
    flat(c, [Ell(120, 544, 10, 5)], (200, 40, 40))
    for lx in (130, 156, 190, 214):
        flat(c, RRect(lx - 4, 566, lx + 4, 596, 1), (230, 220, 200))
    hx, hy = hanfu(c, 330, 596, (220, 100, 130), hat="lady", h=0.9)
    flat(c, Thick(hx + 8, hy + 8, hx + 20, hy - 6, 1.2), (110, 80, 60))
    lantern_cn(c, hx + 20, hy + 6, (90, 160, 90) if "girl" in d else (220, 50, 40), r=7)
    for x, col in ((400, (60, 70, 110)), (620, (150, 60, 70)), (680, (90, 110, 80)), (850, (110, 70, 110))):
        hanfu(c, x, 598, col, hat="futou" if x % 3 else "bun")
    flat(c, Thick(740, 430, 900, 430, 1.4), (60, 50, 50))
    for k, x in enumerate(range(752, 900, 22)):
        piece(c, RRect(x - 5, 430, x + 5, 452, 1), ((90, 160, 220) if (k == 3 and "riddle" in d) else (240, 220, 140)), shadow=SMALL)


def dragon(c, m):
    for k in range(9):
        x = 360 + k * 34
        y = 520 + 10 * math.sin(k * 0.9)
        piece(c, Ell(x, y, 20, 14), (220, 60, 50) if k % 2 else (240, 190, 60), border=1.2, shadow=SMALL)
        flat(c, Thick(x, y + 12, x, y + 70, 2), (110, 80, 60))
    piece(c, [Ell(680, 510, 26, 18), Poly([(700, 500), (722, 490), (712, 512)])], (220, 60, 50), border=1.5, shadow=SMALL)
    flat(c, [Circ(690, 504, 3), Thick(670, 494, 660, 478, 2), Thick(684, 494, 680, 476, 2)], (250, 240, 200))


L103_ELEMENTS = [
    E("moon", lambda c, m: (soft_union(c, [Circ(800, 70, 28)], (255, 250, 220), 0.35, spread=16),
                            piece(c, Circ(800, 70, 22), (252, 246, 220), border=2, shadow=PROP)), daynight="night"),
    star_field("stars", 103, 30, 120, avoid=[(760, 30, 840, 110)]),
    cloud_el("cloud0", 300, 60, 0.6, 5, daynight="day"),
    E("glow", lambda c, m: soft_union(c, [Circ(x, y + 16, 8) for i, (x, y) in enumerate(STRING103) if not 6 <= i <= 8] +
                                     [Circ(x, y, 8) for y in (240, 300, 370) for x in (410, 450, 490)], (255, 190, 100), 0.5, spread=16),
      daynight="night", anim=dict(twinkle=0.12, twinkleSpeed=0.8)),
    E("dragon", dragon, pivot=(520, 560), anim=dict(bobAmplitude=(0, 10), bobSpeed=0.5)),
] + [E("firework%d" % i, firework(x, y, col, r), pivot=(x, y), daynight="night",
       anim=dict(blinkInterval=2.8 + i * 0.3, blinkDuration=1.1, phase=i * 0.3, pulse=0.15, scaleSpeed=0.8))
     for i, (x, y, col, r) in enumerate(((240, 80, (255, 130, 150), 36), (620, 60, (140, 220, 255), 40)))]

L103_DIFFS = [
    ("tower", 450, 164, 0),
    ("rabbit", 204, 298, 0),
    ("fish", 694, 300, 0),
    ("lion", 140, 540, 0),
    ("girl", 351, 562, 0),
    ("riddle", 818, 441, 0),
    ("string", int(STRING103[11][0]), int(STRING103[11][1] + 16), 0),
]

LEVELS = [
    ("Level99", "长安西市", l99_bg, L99_ELEMENTS, L99_DIFFS, 140, OPTS),
    ("Level100", "清明上河图", l100_bg, L100_ELEMENTS, L100_DIFFS, 140, OPTS),
    ("Level101", "仕女游春", l101_bg, L101_ELEMENTS, L101_DIFFS, 140, OPTS),
    ("Level102", "西湖", l102_bg, L102_ELEMENTS, L102_DIFFS, 140, dict(OPTS, weather=WEATHER102, anim_seconds=27.0, frames=54)),
    ("Level103", "元宵灯会", l103_bg, L103_ELEMENTS, L103_DIFFS, 140, dict(OPTS, day_night=DN103, anim_seconds=40.0, frames=80)),
]
