# -*- coding: utf-8 -*-
"""Everyday-town themes, part 10: more nature trips (paper-craft side views, full-bleed):
  Level590 冰川徒步 - a glacier hike: ice tongue with crevasses, roped hikers, peaks, meltwater lake; mist
  Level591 草莓田   - a strawberry farm: rows under low tunnels, pickers with baskets, farm stand
  Level592 蝴蝶谷   - a butterfly valley: wildflower meadow, stream, many butterflies, a photographer
  Level593 礁石潮池 - rocky tide pools: anemones, crabs, starfish, kids with nets, lighthouse far off
  Level594 火山口湖 - a crater lake: rim trail, turquoise lake, steam vents, hikers at a viewpoint
  Level595 骆驼商队 - a camel caravan crossing dunes; day / night with a starry sky
  Level596 雾凇森林 - a rime-frost forest: white trees, frozen river, red-capped walkers; snow
  Level597 油菜花田 - rapeseed fields: yellow terraces, farmhouses, bee boxes, cyclists; rain showers
  Level598 溶洞     - a limestone cave: stalactites, underground pool, coloured lights, a walkway with visitors
  Level599 海鹦悬崖 - puffin cliffs: grassy cliff top with burrows, puffins, sea stacks, birdwatchers
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, rock, sky, tree_pine, tree_round
from fills import cloud_bank, far_ridge, far_round_trees
from levels_akiba import modern
from levels_daily5 import hiker
from levels_daily7 import sea
from stylekit import celestial, day_night, moon_element, star_field, sun_element
from weather import cloud, fog_layer, paper_sun, puddles, rain_layer, snow_layer, splash_rings

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SNOWC = (246, 248, 252)


def butterfly_el(eid, x, y, col, phase=0.0, amp=(30, 16)):
    return E(eid, lambda c, m: (flat(c, [Ell(x - 7, y, 7, 5), Ell(x + 7, y, 7, 5), Ell(x - 5, y + 6, 5, 4), Ell(x + 5, y + 6, 5, 4)], col),
                                flat(c, Thick(x, y - 5, x, y + 8, 1.6), INK)),
             pivot=(x, y), anim=dict(bobAmplitude=amp, bobSpeed=0.3, stretch=(0.5, 0), scaleSpeed=3.0, phase=phase))


# =================================================================== Level 590 glacier hike (mist)
STEPS590 = [(CLEAR, 12), (FOG, 8)]


def l590_bg(c, d):
    sky(c, (110, 170, 230), (220, 232, 246), 460)
    # peaks
    piece(c, Poly([(-10, 260), (120, 70), (260, 200), (420, 30), (580, 190), (740, 60), (910, 210), (910, 300), (-10, 300)]), (150, 160, 186), shadow=LAYER)
    for (px, py), w in (((120, 70), 50), ((420, 30), 70), ((740, 60), 60)):
        flat(c, Poly([(px - w, py + w * 1.2), (px, py), (px + w, py + w * 1.2), (px + w * 0.3, py + w), (px, py + w * 1.1), (px - w * 0.3, py + w)]), SNOWC)
    # glacier tongue
    piece(c, Poly([(200, 240), (640, 240), (780, 470), (60, 470)]), (220, 236, 248), border=1.5, shadow=LAYER)
    for k in range(9):
        x = 160 + k * 60
        flat(c, Poly([(x, 300 + (k % 3) * 40), (x + 30, 296 + (k % 3) * 40), (x + 18, 330 + (k % 3) * 40)]), (150, 196, 226))
    # moraine + meltwater lake
    piece(c, RRect(-10, 440, 910, 612, 0), (150, 140, 130), shadow=LAYER)
    piece(c, Ell(620, 520, 200, 40), (120, 196, 214), border=1.5, shadow=SMALL)
    flat(c, [Poly([(560, 510), (600, 500), (620, 520), (580, 530)])], (240, 248, 252))          # floating ice
    for x, s in ((100, 1.6), (340, 1.2), (860, 1.8)):
        rock(c, x, 560, s=s)
    # flag on the summit route + hut
    piece(c, RRect(30, 380, 140, 440, 2), (200, 70, 60) if "hut" not in d else (60, 110, 180), border=1.5, shadow=PROP)
    piece(c, Poly([(20, 384), (150, 384), (85, 350)]), (90, 90, 100), border=1.5, shadow=PROP)
    flat(c, RRect(70, 404, 100, 440, 2), (90, 70, 60))
    flat(c, Thick(420, 240, 420, 180, 2), (90, 90, 100))
    piece(c, Poly([(421, 176), (470, 188), (421, 206)]), (240, 60, 60) if "flag" not in d else (250, 200, 60), border=1, shadow=SMALL)
    # roped hikers on the ice
    for k, x in enumerate((300, 380, 460)):
        hiker(c, x, 400, [(240, 90, 60), (60, 120, 210), (250, 200, 60)][k] if not (k == 1 and "jacket" in d) else (120, 200, 120),
              [(60, 60, 80), (200, 70, 70), (90, 150, 110)][k], h=1.5)
    flat(c, [Thick(300, 370, 380, 370, 1.4), Thick(380, 370, 460, 370, 1.4)], (220, 60, 60))
    # signpost near the lake
    flat(c, Thick(800, 520, 800, 450, 4), (120, 90, 60))
    piece(c, Poly([(800, 454), (850, 454), (860, 466), (850, 478), (800, 478)]), (230, 200, 120) if "sign" not in d else (110, 180, 210), border=1, shadow=SMALL)


L590_ELEMENTS = [
    E("ice", lambda c, m: piece(c, Poly([(660, 524), (690, 516), (704, 530), (676, 536)]), (240, 248, 252), border=1, shadow=None), pivot=(680, 526),
      anim=dict(bobAmplitude=(20, 2), bobSpeed=0.1)),
    bird_el("eagle", 600, 120, s=12, speed=-14),
    cloud_el("cloud", 300, 60, 0.7, 6),
    fog_layer("fog", 590, 200, 420, 0.4, 12),
]

L590_DIFFS = [
    ("hut", 85, 410, 0),
    ("flag", 436, 190, 0),
    ("jacket", 381, 344, 0),
    ("sign", 830, 466, 0),
]


# =================================================================== Level 591 strawberry farm
def strawberry_row(c, y, x0, x1, seed, berry=(220, 40, 50)):
    piece(c, RRect(x0, y - 12, x1, y + 12, 10), (110, 80, 60), shadow=SMALL)
    rnd = random.Random(seed)
    x = x0 + 14
    while x < x1 - 10:
        piece(c, [Circ(x, y - 18, 11), Circ(x + 10, y - 14, 9)], (70, 140, 70), shadow=None)
        if rnd.random() < 0.6:
            flat(c, Poly([(x - 4, y - 8), (x + 4, y - 8), (x, y + 2)]), berry)
        x += 24


def l591_bg(c, d):
    sky(c, (130, 194, 240), (226, 238, 244), 260)
    cloud_bg(c, 200, 60, 0.8)
    far_ridge(c, 200, 40, (150, 190, 140), 5911)
    # polytunnels at the back
    for k, x in enumerate((60, 330, 600)):
        pts = [(x + 120 + 120 * math.cos(math.radians(a)), 270 - 70 * math.sin(math.radians(a))) for a in range(0, 181, 12)]
        piece(c, Poly(pts), (230, 236, 240) if not (k == 1 and "tunnel" in d) else (250, 220, 160), border=1.5, shadow=PROP)
        for j in range(5):
            flat(c, Thick(x + 20 + j * 50, 270, x + 20 + j * 50, 270 - 60 * math.sin(math.acos(max(-1, min(1, (j * 50 - 100) / 120)))), 1.4), (200, 206, 214))
    # field rows
    piece(c, RRect(-10, 270, 910, 612, 0), (140, 110, 80), shadow=LAYER)
    for k, y in enumerate((320, 380, 450, 530)):
        strawberry_row(c, y, -10 + k * 10, 910, 5912 + k)
    # farm stand (right)
    piece(c, [RRect(700, 470, 880, 560, 3), Poly([(690, 470), (890, 470), (870, 430), (710, 430)])], (220, 70, 70), border=1.5, shadow=PROP)
    flat(c, [Poly([(700 + j * 36, 470), (718 + j * 36, 470), (714 + j * 32, 430), (706 + j * 32, 430)]) for j in range(5)], (250, 250, 250))
    for k in range(4):
        piece(c, RRect(714 + k * 40, 486, 746 + k * 40, 506, 2), (240, 236, 220), border=0.8, shadow=None)
        flat(c, [Circ(722 + k * 40, 484, 5), Circ(736 + k * 40, 484, 5)], (220, 40, 50))
    modern(c, 790, 470, (250, 250, 250) if "farmer" not in d else (90, 170, 120), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.7)
    # pickers with baskets
    for k, (x, col) in enumerate(((140, (240, 200, 90)), (380, (90, 150, 220)), (560, (220, 110, 150)))):
        if k == 1 and "shirt" in d:
            col = (250, 250, 250)
        modern(c, x, 600, col, bottom=(60, 70, 110), hair=[(90, 60, 40), (40, 30, 30), (220, 180, 90)][k], h=2.2, style="long" if k != 1 else "short")
        piece(c, [Ell(x + 1, 492, 26, 7), Ell(x + 1, 486, 12, 8)], (230, 200, 120), shadow=SMALL)
    piece(c, [Poly([(410, 600), (460, 600), (466, 560), (404, 560)])], (190, 140, 90) if "basket" not in d else (90, 150, 210), border=1, shadow=SMALL)
    flat(c, [Circ(418 + k * 9, 556, 6) for k in range(5)], (220, 40, 50))


L591_ELEMENTS = [
    E("bee%d" % i, (lambda x, y: lambda c, m: (flat(c, Ell(x, y, 5, 4), (250, 200, 50)), flat(c, [Ell(x - 2, y - 5, 4, 3), Ell(x + 3, y - 5, 4, 3)], (240, 250, 255))))(x, y),
      pivot=(x, y), anim=dict(bobAmplitude=(24, 12), bobSpeed=0.4 + i * 0.1, phase=i / 3)) for i, (x, y) in enumerate(((260, 360), (640, 420)))
] + [
    E("sprinkle", lambda c, m: [soft_union(c, [Circ(60 + k * 160, 300, 3)], (200, 230, 250), 0.7, spread=4) for k in range(6)], anim=dict(twinkle=0.6, twinkleSpeed=1.0)),
    bird_el("bird", 400, 70, s=8, speed=20),
]

L591_DIFFS = [
    ("tunnel", 450, 230, 0),
    ("farmer", 791, 436, 0),
    ("shirt", 381, 543, 0),
    ("basket", 435, 576, 0),
]


# =================================================================== Level 592 butterfly valley
def l592_bg(c, d):
    sky(c, (130, 196, 240), (230, 240, 236), 260)
    far_ridge(c, 150, 60, (150, 196, 170), 5921)
    far_round_trees(c, 220, 34, (100, 160, 110), 5922)
    piece(c, RRect(-10, 240, 910, 612, 0), (140, 196, 100), shadow=LAYER)
    # stream
    piece(c, Poly([(-10, 380), (300, 350), (600, 390), (910, 360), (910, 400), (600, 430), (300, 390), (-10, 420)]), (130, 190, 220), border=1.5, shadow=SMALL)
    # wildflower patches
    rnd = random.Random(5923)
    pal = [(240, 90, 120), (250, 200, 70), (150, 110, 220), (250, 250, 250), (240, 140, 60)]
    for k in range(120):
        x, y = rnd.uniform(0, 900), rnd.uniform(260, 600)
        if 350 < y < 430:
            continue
        flat(c, Circ(x, y, rnd.uniform(3, 5)), rnd.choice(pal))
    # flowering bushes (static butterfly hosts)
    for k, (x, b, col) in enumerate(((120, 330, (240, 160, 200)), (760, 320, (250, 220, 120)), (520, 560, (200, 160, 240)))):
        if k == 1 and "bush" in d:
            col = (250, 250, 250)
        piece(c, [Circ(x - 24, b - 20, 22), Circ(x, b - 32, 28), Circ(x + 26, b - 20, 22)], (90, 160, 90), shadow=PROP)
        flat(c, [Circ(x - 30 + j * 12, b - 40 + (j % 3) * 10, 6) for j in range(6)], col)
    # resting butterflies (static)
    for k, (x, y, col) in enumerate(((150, 290, (250, 160, 50)), (500, 520, (90, 160, 230)), (790, 280, (220, 70, 90)))):
        if k == 0 and "wing" in d:
            col = (120, 200, 120)
        flat(c, [Ell(x - 10, y, 10, 7), Ell(x + 10, y, 10, 7), Ell(x - 7, y + 9, 7, 5), Ell(x + 7, y + 9, 7, 5)], col)
        flat(c, Thick(x, y - 7, x, y + 12, 2), INK)
    # stepping stones + photographer + kid with a net
    for x in (420, 460, 500):
        piece(c, Ell(x, 395, 16, 7), (170, 166, 170), shadow=SMALL)
    modern(c, 300, 600, (90, 150, 110), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.3)
    piece(c, RRect(318, 510, 350, 534, 4), (40, 40, 46) if "camera" not in d else (220, 70, 70), border=1, shadow=SMALL)
    flat(c, Circ(350, 522, 7), (110, 150, 200))
    modern(c, 700, 600, (250, 200, 80) if "kid" not in d else (120, 200, 230), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.6, style="twin")
    flat(c, Thick(712, 540, 760, 470, 3), (150, 110, 70))
    c.ellipse_ring(768, 460, 16, 14, 2, (250, 250, 250))


L592_ELEMENTS = [
    butterfly_el("bf%d" % i, x, y, col, phase=i / 6) for i, (x, y, col) in enumerate(((240, 200, (250, 160, 50)), (400, 280, (90, 160, 230)),
                                                                                     (620, 220, (240, 120, 180)), (840, 420, (250, 220, 70)),
                                                                                     (180, 470, (150, 110, 220)), (580, 470, (250, 250, 250))))
] + [bird_el("bird", 500, 60, s=8, speed=-18)]

L592_DIFFS = [
    ("bush", 760, 290, 0),
    ("wing", 150, 294, 0),
    ("camera", 334, 522, 0),
    ("kid", 701, 562, 0),
]


# =================================================================== Level 593 rocky tide pools
def crab(c, x, y, col=(230, 90, 60)):
    piece(c, [Ell(x, y, 16, 10)] + [Thick(x + dx, y + 4, x + dx * 1.6, y + 14, 2.4) for dx in (-12, -6, 6, 12)] +
          [Thick(x - 12, y - 4, x - 22, y - 12, 3), Thick(x + 12, y - 4, x + 22, y - 12, 3), Circ(x - 24, y - 14, 5), Circ(x + 24, y - 14, 5)], col, border=1, shadow=SMALL)
    flat(c, [Circ(x - 5, y - 9, 2.4), Circ(x + 5, y - 9, 2.4)], INK)


def anemone(c, x, y, col):
    flat(c, [Thick(x, y, x + 14 * math.cos(a), y - 14 * math.sin(a), 3) for a in [math.pi * (0.1 + 0.8 * k / 6) for k in range(7)]], col)
    flat(c, Ell(x, y + 2, 10, 5), lit(col, 0.8))


def l593_bg(c, d):
    sky(c, (120, 186, 236), (230, 236, 240), 240)
    sea(c, 200, seed=5931, n=12)
    # far lighthouse on a headland
    piece(c, Poly([(700, 220), (760, 180), (910, 170), (910, 230)]), (150, 160, 140), shadow=SMALL)
    piece(c, Poly([(806, 180), (826, 180), (822, 110), (810, 110)]), (250, 250, 250), border=1, shadow=SMALL)
    flat(c, [RRect(808, 130, 824, 140, 0), RRect(808, 156, 824, 166, 0)], (220, 60, 60))
    # rock shelf with pools
    piece(c, Poly([(-10, 300), (200, 270), (450, 290), (700, 260), (910, 290), (910, 612), (-10, 612)]), (130, 120, 116), shadow=LAYER)
    for k in range(14):
        rnd = random.Random(5932 + k)
        flat(c, Ell(rnd.uniform(0, 900), rnd.uniform(300, 600), rnd.uniform(20, 50), 6), (116, 106, 104))
    for (x, y, rx, ry) in ((200, 390, 130, 40), (600, 360, 150, 46), (420, 520, 170, 50)):
        piece(c, Ell(x, y, rx, ry), (90, 160, 190), border=1.5, shadow=SMALL)
        flat(c, Ell(x - rx * 0.3, y - ry * 0.3, rx * 0.4, ry * 0.2), (140, 200, 220))
    # pool life
    anemone(c, 160, 400, (240, 100, 140))
    anemone(c, 250, 380, (90, 190, 160) if "anemone" not in d else (250, 200, 60))
    piece(c, Poly(star_pts(560, 360, 18, 8)), (250, 140, 60) if "star" not in d else (150, 110, 220), border=1, shadow=None)
    anemone(c, 660, 370, (220, 80, 80))
    crab(c, 420, 520, col=(230, 90, 60) if "crab" not in d else (90, 140, 210))
    flat(c, [Ell(470, 540, 6, 4), Ell(380, 536, 5, 3)], (250, 236, 220))
    # kids with nets + bucket
    modern(c, 100, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.8, style="twin")
    flat(c, Thick(110, 540, 160, 460, 3), (150, 110, 70))
    c.ellipse_ring(166, 450, 14, 12, 2, (250, 250, 250))
    modern(c, 780, 600, (90, 150, 220), bottom=(60, 70, 110), hair=(40, 30, 30), h=1.9)
    piece(c, Poly([(820, 600), (860, 600), (864, 566), (816, 566)]), (250, 90, 90) if "bucket" not in d else (90, 190, 120), border=1.2, shadow=PROP)
    c.ellipse_ring(840, 562, 22, 6, 2, (200, 60, 60))
    # seaweed + shells
    for x in (60, 300, 700, 880):
        flat(c, [Thick(x, 600, x - 10, 560, 4), Thick(x + 6, 600, x + 14, 566, 4)], (90, 130, 70))


L593_ELEMENTS = [
    E("wave", lambda c, m: flat(c, [Ell(150 + k * 180, 268, 60, 5) for k in range(5)], (250, 252, 255, 0.85)), anim=dict(bobAmplitude=(0, 6), bobSpeed=0.3)),
    E("scuttle", lambda c, m: crab(c, 0, 470, col=(240, 150, 90)), anim=dict(driftVelocity=(20, 0), driftStart=600, driftLength=200, bobAmplitude=(0, 2), bobSpeed=2.0)),
    E("sway", lambda c, m: anemone(c, 160, 400, (240, 100, 140)), pivot=(160, 400), anim=dict(swingAngle=6, swingSpeed=0.5)),
    bird_el("gull", 300, 120, s=9, speed=-20),
]

L593_DIFFS = [
    ("anemone", 250, 376, 0),
    ("star", 560, 360, 0),
    ("crab", 420, 512, 0),
    ("bucket", 840, 582, 0),
]


# =================================================================== Level 594 crater lake
def l594_bg(c, d):
    sky(c, (120, 186, 240), (230, 236, 244), 220)
    cloud_bg(c, 760, 60, 0.7)
    c.rect(0, 220, W, H, (160, 120, 110))
    # crater rim (far side)
    piece(c, Poly([(-10, 220), (150, 150), (400, 130), (650, 140), (910, 190), (910, 300), (-10, 300)]), (160, 120, 110), shadow=LAYER)
    for x in range(0, 900, 60):
        flat(c, Thick(x, 180 - abs(x - 450) * 0.05, x + 30, 250, 2), (140, 104, 96))
    # lake
    piece(c, Ell(450, 320, 420, 70), (80, 190, 190), border=1.5, shadow=SMALL)
    flat(c, Ell(450, 310, 300, 30), (120, 210, 206))
    # island
    piece(c, Ell(560, 300, 50, 14), (150, 140, 120), shadow=SMALL)
    flat(c, [Circ(550, 288, 10), Circ(570, 290, 8)], (90, 150, 90) if "island" not in d else (230, 150, 70))
    # near rim slopes
    piece(c, Poly([(-10, 280), (60, 330), (300, 400), (600, 390), (840, 330), (910, 280), (910, 612), (-10, 612)]), (180, 150, 120), shadow=LAYER)
    for k in range(20):
        rnd = random.Random(5941 + k)
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(420, 600), rnd.uniform(20, 50), 4), (166, 136, 108))
    # steam vents (static rocks around them)
    for x in (120, 780):
        piece(c, Ell(x, 430, 40, 12), (200, 190, 130), shadow=SMALL)
    # viewpoint platform + info board + hikers
    piece(c, RRect(320, 480, 600, 494, 2), (150, 110, 80), border=1.2, shadow=PROP)
    flat(c, [Thick(320, 450, 600, 450, 3)] + [Thick(330 + k * 30, 450, 330 + k * 30, 480, 2) for k in range(10)], (150, 110, 80))
    flat(c, [Thick(640, 520, 640, 460, 4), Thick(720, 520, 720, 460, 4)], (120, 90, 60))
    piece(c, RRect(620, 400, 740, 470, 3), (90, 140, 110) if "board" not in d else (200, 120, 60), border=1.5, shadow=PROP)
    flat(c, [Ell(660, 430, 22, 14), RRect(690, 414, 730, 424, 2), RRect(690, 432, 724, 442, 2)], (240, 236, 220))
    hiker(c, 380, 480, (240, 120, 60), (60, 110, 180), h=1.8)
    hiker(c, 450, 480, (90, 160, 120) if "pack" not in d else (250, 200, 60), (200, 70, 70), h=1.7, hair=(220, 180, 90), style="long")
    hiker(c, 200, 600, (60, 90, 150), (250, 200, 60), h=2.3)
    # cairn
    piece(c, [Ell(840, 590, 30, 10), Ell(840, 572, 22, 9), Ell(840, 556, 15, 7), Ell(840, 543, 9, 6)], (150, 146, 150) if "cairn" not in d else (200, 160, 110),
          border=1, shadow=PROP)


L594_ELEMENTS = [
    E("vent%d" % i, (lambda x: lambda c, m: soft_union(c, [Circ(x, 420, 10)], (246, 246, 250), 0.7, spread=12))(x),
      anim=dict(driftVelocity=(4, 30), driftLength=120, driftFade=True, driftGrow=2.0, phase=i / 4)) for i, x in enumerate((110, 130, 770, 790))
] + [
    E("ripple", lambda c, m: c.ellipse_ring(300, 330, 40, 8, 2, (200, 240, 236)), pivot=(300, 330), anim=dict(pulse=0.3, scaleSpeed=0.5, twinkle=0.4)),
    bird_el("bird", 500, 80, s=9, speed=20),
]

L594_DIFFS = [
    ("island", 560, 288, 0),
    ("board", 680, 435, 0),
    ("pack", 451, 436, 0),
    ("cairn", 840, 566, 0),
]


# =================================================================== Level 595 camel caravan (day / night)
DN595 = day_night(40.0, tint=(0.26, 0.26, 0.50))
SUN595, MOON595 = celestial((450, 320), (380, 260), 40.0)


def camel(c, x, base, col=(210, 170, 110), blanket=(200, 60, 60), s=1.0):
    legs = [RRect(x + dx * s - 4 * s, base - 50 * s, x + dx * s + 4 * s, base, 2) for dx in (-26, -16, 20, 30)]
    piece(c, legs + [Ell(x, base - 60 * s, 40 * s, 18 * s), Circ(x - 4 * s, base - 76 * s, 18 * s),
                     Poly([(x + 34 * s, base - 66 * s), (x + 46 * s, base - 60 * s), (x + 64 * s, base - 100 * s), (x + 54 * s, base - 106 * s)]),
                     Ell(x + 66 * s, base - 106 * s, 14 * s, 8 * s)], col, border=1.2, shadow=PROP)
    flat(c, Circ(x + 70 * s, base - 108 * s, 1.8 * s), INK)
    piece(c, Poly([(x - 26 * s, base - 70 * s), (x + 16 * s, base - 70 * s), (x + 20 * s, base - 46 * s), (x - 30 * s, base - 46 * s)]), blanket, border=1, shadow=None)


def l595_bg(c, d):
    sky(c, (120, 180, 236), (250, 216, 170), 360)
    # dunes (far to near)
    for k, (top, col) in enumerate(((300, (230, 180, 120)), (360, (240, 196, 130)), (440, (246, 206, 140)))):
        pts = [(x, top + 30 * math.sin(x / (120 + k * 40) + k)) for x in range(-10, 920, 20)] + [(910, 612), (-10, 612)]
        piece(c, Poly(pts), col, shadow=LAYER)
    # oasis palms far right
    for x in (780, 830):
        flat(c, Thick(x, 340, x + 6, 280, 4), (150, 110, 70))
        flat(c, [Ell(x + 6 + 18 * math.cos(a), 280 + 8 * math.sin(a), 16, 5) for a in (0.3, 1.6, 2.9, 4.2)], (90, 150, 80))
    # caravan
    for k, x in enumerate((200, 380, 560)):
        camel(c, x, 470 + k * 6, blanket=[(200, 60, 60), (60, 110, 190), (230, 170, 60)][k] if not (k == 1 and "blanket" in d) else (120, 190, 110), s=1.2)
        piece(c, [RRect(x - 18, 376 + k * 6, x + 14, 402 + k * 6, 4)], (170, 120, 80) if not (k == 2 and "pack" in d) else (90, 140, 200), border=1,
              shadow=SMALL)       # packs
    flat(c, [Thick(279, 342, 340, 400, 1.4), Thick(459, 348, 520, 406, 1.4)], (120, 90, 60))
    # guide walking in front
    modern(c, 700, 500, (250, 250, 246), bottom=(250, 250, 246), hair=(40, 30, 30), h=2.0)
    piece(c, [Ell(701, 410, 14, 10)], (60, 110, 190) if "turban" not in d else (220, 80, 80), shadow=SMALL)
    flat(c, Thick(720, 470, 740, 400, 3), (150, 110, 70))
    # footprints + desert plants + lantern
    for k in range(10):
        flat(c, Ell(60 + k * 60, 560 + (k % 2) * 8, 6, 3), (220, 180, 120))
    piece(c, [Circ(90, 596, 22), Circ(116, 592, 18)], (130, 150, 90) if "shrub" not in d else (200, 160, 90), shadow=SMALL)
    piece(c, [RRect(830, 540, 856, 580, 4), Poly([(826, 542), (860, 542), (843, 526)])], (60, 60, 70) if "lantern" not in d else (190, 150, 70), border=1, shadow=PROP)
    flat(c, RRect(836, 548, 850, 574, 2), (255, 220, 140))


L595_ELEMENTS = [
    sun_element("sun", (450, 320), SUN595, r=28),
    moon_element("moon", (450, 320), MOON595, r=22),
    star_field("stars", 595, 50, 260),
    E("lglow", lambda c, m: soft_union(c, [Circ(843, 560, 10)], (255, 210, 130), 0.6, spread=30), daynight="night", anim=dict(pulse=0.1, scaleSpeed=1.2)),
    E("sand", lambda c, m: [soft_union(c, [Circ(100 + k * 200, 470, 6)], (240, 210, 160), 0.5, spread=8) for k in range(4)],
      anim=dict(driftVelocity=(30, 4), driftLength=120, driftFade=True)),
    E("nod", lambda c, m: (piece(c, Ell(645, 336, 17, 10), (210, 170, 110), border=1.2, shadow=None), flat(c, Circ(650, 334, 2), INK)), pivot=(625, 350),
      anim=dict(swingAngle=6, swingSpeed=0.5)),
]

L595_DIFFS = [
    ("blanket", 375, 416, 0),
    ("turban", 701, 410, 0),
    ("lantern", 843, 556, 0),
    ("shrub", 100, 594, 0),
    ("pack", 558, 401, 0),
]


# =================================================================== Level 596 rime-frost forest (snow)
STEPS596 = [(CLEAR, 10), (SNOW, 14)]


def rime_tree(c, x, base, s=1.0):
    flat(c, Thick(x, base, x, base - 140 * s, 6 * s), (120, 110, 110))
    for k in range(6):
        y = base - 40 * s - k * 18 * s
        w = (60 - k * 8) * s
        flat(c, [Thick(x, y, x - w, y - 16 * s, 2.4 * s), Thick(x, y, x + w, y - 14 * s, 2.4 * s)], (120, 110, 110))
    piece(c, [Circ(x - 30 * s, base - 90 * s, 30 * s), Circ(x + 26 * s, base - 100 * s, 30 * s), Circ(x, base - 130 * s, 26 * s), Circ(x, base - 70 * s, 26 * s)],
          (250, 252, 255), border=1, border_col=(220, 226, 240), shadow=SMALL)


def l596_bg(c, d):
    sky(c, (150, 180, 220), (226, 232, 244), 300)
    far_ridge(c, 170, 50, (200, 212, 232), 5961)
    piece(c, RRect(-10, 260, 910, 612, 0), SNOWC, shadow=LAYER)
    # frozen river
    piece(c, Poly([(-10, 420), (300, 390), (600, 430), (910, 400), (910, 460), (600, 490), (300, 450), (-10, 480)]), (200, 222, 240), border=1.5, shadow=SMALL)
    for x in (100, 400, 700):
        flat(c, Thick(x, 440, x + 60, 436, 2), (240, 248, 252))
    # rime trees
    for k, (x, b, s) in enumerate(((60, 330, 1.2), (200, 310, 1.0), (330, 320, 1.1), (600, 310, 1.0), (730, 330, 1.2), (860, 316, 1.1))):
        rime_tree(c, x, b, s=s)
    # wooden bridge over the river + red pavilion
    piece(c, RRect(380, 410, 540, 424, 2), (150, 100, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(390, 396, 530, 396, 3)] + [Thick(400 + k * 20, 396, 400 + k * 20, 410, 2) for k in range(7)], (150, 100, 70) if "rail" not in d else (60, 120, 200))
    piece(c, [RRect(460, 230, 540, 300, 2)], (200, 60, 50), border=1.5, shadow=PROP)
    piece(c, Poly([(446, 234), (554, 234), (530, 206), (470, 206)]), (60, 70, 80), border=1.5, shadow=PROP)
    flat(c, Poly([(446, 234), (554, 234), (530, 214), (470, 214)]), SNOWC)
    flat(c, RRect(484, 250, 516, 300, 2), (255, 220, 140) if "door" not in d else (90, 140, 200))
    # walkers with red hats + photographer + snowman
    for k, (x, col) in enumerate(((240, (200, 60, 60)), (300, (60, 90, 150)), (680, (240, 200, 90)))):
        modern(c, x, 600, col, bottom=(40, 40, 50), hair=(40, 30, 30), h=2.2)
        hat = (220, 50, 50) if not (k == 2 and "hat" in d) else (90, 160, 220)
        flat(c, [Ell(x + 2, 600 - 46 * 2.2 - 8, 16, 10), Circ(x + 2, 600 - 46 * 2.2 - 20, 6)], hat)
    piece(c, [Circ(840, 570, 30), Circ(840, 526, 21), Circ(840, 494, 15)], SNOWC, border=1.5, border_col=(220, 226, 240), shadow=PROP)
    flat(c, Poly([(844, 494), (866, 498), (844, 502)]), (250, 140, 40))
    flat(c, [RRect(820, 510, 860, 524, 3), RRect(846, 516, 858, 546, 3)], (60, 120, 200) if "scarf" not in d else (220, 80, 80))


L596_ELEMENTS = [
    E("drop%d" % i, (lambda x, y: lambda c, m: flat(c, Circ(x, y, 3), (250, 252, 255)))(x, y),
      anim=dict(driftVelocity=(0, -30), driftLength=100, driftFade=True, phase=i / 3)) for i, (x, y) in enumerate(((40, 220), (330, 210), (740, 230)))
] + [
    cloud("cloudA", 200, 40, 1.2, (210, 216, 230), W_(SNOW)),
    cloud("cloudB", 680, 30, 1.3, (210, 216, 230), W_(SNOW)),
    snow_layer("snow", 596, 70, 2.0, 4.0, 40),
    bird_el("crow", 500, 120, s=9, speed=-16, col=(40, 40, 50)),
]

L596_DIFFS = [
    ("rail", 460, 400, 0),
    ("door", 500, 275, 0),
    ("hat", 682, 470, 0),
    ("scarf", 840, 520, 0),
]


# =================================================================== Level 597 rapeseed fields (rain showers)
STEPS597 = [(CLEAR, 12), (OVERCAST, 4), (RAIN, 10), (OVERCAST, 4)]


def l597_bg(c, d):
    sky(c, (130, 190, 236), (232, 236, 236), 260)
    far_ridge(c, 150, 60, (150, 180, 170), 5971)
    # terraced yellow fields
    for k, (top, col) in enumerate(((220, (250, 220, 70)), (290, (240, 210, 60)), (370, (250, 226, 80)), (460, (246, 214, 70)))):
        pts = [(x, top + 16 * math.sin(x / 90 + k)) for x in range(-10, 920, 20)] + [(910, 612), (-10, 612)]
        piece(c, Poly(pts), col, shadow=LAYER)
        rnd = random.Random(5972 + k)
        for _ in range(40):
            x = rnd.uniform(0, 900)
            flat(c, Circ(x, top + 16 * math.sin(x / 90 + k) + rnd.uniform(8, 40), 3), lit(col, 1.08))
    # white-walled farmhouses
    for k, (x, b) in enumerate(((150, 260), (700, 300))):
        piece(c, RRect(x - 50, b - 60, x + 50, b, 2), (250, 250, 246), border=1.5, shadow=PROP)
        piece(c, Poly([(x - 60, b - 56), (x + 60, b - 56), (x, b - 96)]), (60, 60, 70) if not (k == 1 and "roof" in d) else (190, 70, 60), border=1.5, shadow=PROP)
        flat(c, [RRect(x - 30, b - 40, x - 10, b - 20, 2), RRect(x + 10, b - 40, x + 30, b - 20, 2)], (150, 190, 220) if not (k == 0 and "window" in d)
             else (250, 200, 110))
    # path + bee boxes
    piece(c, Poly([(380, 612), (520, 612), (470, 400), (450, 400)]), (200, 170, 120), shadow=SMALL)
    for k, x in enumerate((560, 620, 680)):
        piece(c, [RRect(x - 22, 420, x + 22, 460, 2), RRect(x - 26, 412, x + 26, 422, 2)], (90, 150, 210) if not (k == 1 and "hive" in d) else (240, 120, 60),
              border=1, shadow=PROP)
    # cyclists parked + photographer + umbrella
    for wx in (180, 260):
        c.ellipse_ring(wx, 580, 26, 26, 4, (40, 40, 46))
    flat(c, [Thick(180, 580, 210, 540, 4), Thick(210, 540, 250, 540, 4), Thick(250, 540, 260, 580, 4), Thick(210, 540, 220, 580, 4), Thick(220, 580, 180, 580, 4)],
         (60, 160, 200) if "bike" not in d else (220, 80, 120))
    modern(c, 330, 600, (240, 120, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.2, style="long")
    modern(c, 820, 600, (90, 150, 110) if "shirt" not in d else (240, 120, 160), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.3)
    piece(c, RRect(838, 506, 868, 528, 4), (40, 40, 46), border=1, shadow=SMALL)


L597_ELEMENTS = [
    E("bee%d" % i, (lambda x, y: lambda c, m: (flat(c, Ell(x, y, 5, 4), (250, 200, 50)), flat(c, [Ell(x - 2, y - 5, 4, 3), Ell(x + 3, y - 5, 4, 3)], (240, 250, 255))))(x, y),
      pivot=(x, y), anim=dict(bobAmplitude=(30, 14), bobSpeed=0.4 + i * 0.1, phase=i / 3), weather=W_(CLEAR, OVERCAST)) for i, (x, y) in enumerate(((560, 380), (660, 390)))
] + [
    paper_sun("sun", 780, 60, r=30),
    cloud("cloudA", 200, 50, 1.2, (176, 182, 196), W_(OVERCAST, RAIN)),
    cloud("cloudB", 560, 40, 1.4, (168, 174, 190), W_(OVERCAST, RAIN)),
    puddles("puddles", [Ell(460, 560, 30, 5)], mask=W_(RAIN)),
    rain_layer("rain", 597, 70, 24, 1.3, 0.6, 260, mask=W_(RAIN)),
]

L597_DIFFS = [
    ("roof", 700, 226, 0),
    ("hive", 620, 436, 0),
    ("bike", 220, 560, 0),
    ("shirt", 821, 540, 0),
    ("window", 150, 230, 0),
]


# =================================================================== Level 598 limestone cave
def l598_bg(c, d):
    c.rect(0, 0, W, H, (40, 36, 46))
    # cave walls with layered bands
    for k, col in enumerate(((70, 60, 70), (90, 76, 80), (110, 92, 90))):
        pts = [(x, 20 + k * 30 + 20 * math.sin(x / 60 + k)) for x in range(-10, 920, 20)] + [(910, -10), (-10, -10)]
        piece(c, Poly(pts), col, border=1, border_col=(130, 116, 120), shadow=PROP)
    # stalactites
    rnd = random.Random(5981)
    for k in range(18):
        x = 20 + k * 50 + rnd.uniform(-10, 10)
        h = rnd.uniform(40, 140)
        col = (200, 186, 170) if not (k == 12 and "stalactite" in d) else (120, 200, 230)
        piece(c, Poly([(x - 12, 70), (x + 12, 70), (x, 70 + h)]), col, border=1, border_col=(130, 116, 120), shadow=SMALL)
    # back wall + coloured lights
    piece(c, RRect(-10, 200, 910, 400, 0), (70, 60, 76), shadow=LAYER)
    for k, (x, col) in enumerate(((150, (90, 180, 230)), (450, (220, 90, 160)), (750, (120, 220, 140)))):
        soft_union(c, [Ell(x, 300, 120, 80)], col, 0.25, spread=40)
    # stalagmites
    for k, (x, h) in enumerate(((80, 120), (230, 90), (640, 140), (820, 100))):
        col = (190, 176, 160) if not (k == 2 and "stalagmite" in d) else (230, 160, 90)
        piece(c, Poly([(x - 24, 420), (x + 24, 420), (x + 6, 420 - h), (x - 6, 420 - h)]), col, border=1, border_col=(130, 116, 120), shadow=PROP)
    # underground pool
    piece(c, Ell(450, 470, 400, 60), (40, 110, 140), border=1.5, border_col=(130, 116, 120), shadow=SMALL)
    flat(c, Ell(450, 460, 300, 30), (60, 140, 170))
    # walkway with railings + visitors
    piece(c, RRect(-10, 520, 910, 540, 2), (150, 110, 80), border=1.2, border_col=(130, 116, 120), shadow=PROP)
    flat(c, [Thick(-10, 490, 910, 490, 3)] + [Thick(x, 490, x, 520, 2) for x in range(10, 900, 40)], (120, 90, 70))
    c.rect(0, 540, W, H, (60, 52, 58))
    for k, (x, col) in enumerate(((200, (240, 200, 90)), (300, (90, 150, 220)), (620, (220, 110, 150)))):
        modern(c, x, 520, col if not (k == 2 and "visitor" in d) else (250, 250, 250), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0, style="long" if k == 2 else "short")
    # guide with a flashlight
    modern(c, 760, 520, (60, 120, 90) if "guide" not in d else (200, 120, 60), bottom=(40, 40, 50), hair=(130, 130, 140), h=2.0)
    piece(c, RRect(776, 450, 800, 462, 3), (250, 200, 60), shadow=SMALL)
    # bat on the ceiling
    piece(c, [Ell(300, 150, 10, 13), Poly([(290, 142), (262, 132), (270, 154)]), Poly([(310, 142), (338, 132), (330, 154)])],
          (30, 26, 34) if "bat" not in d else (170, 120, 90), shadow=None)


L598_ELEMENTS = [
    E("drip%d" % i, (lambda x: lambda c, m: flat(c, Ell(x, 160, 2.4, 4), (180, 220, 240)))(x),
      anim=dict(driftVelocity=(0, -120), driftLength=300, driftFade=True, phase=i / 3)) for i, x in enumerate((170, 420, 720))
] + [
    E("beam", lambda c, m: soft_union(c, [Poly([(800, 456), (806, 450), (900, 400), (900, 520)])], (255, 250, 210), 0.25, spread=10), daynight="untinted",
      anim=dict(swingAngle=4, swingSpeed=0.4)),
    E("ripple", lambda c, m: c.ellipse_ring(420, 470, 30, 8, 2, (120, 190, 214)), pivot=(420, 470), anim=dict(pulse=0.4, scaleSpeed=0.6, twinkle=0.5)),
    E("glowpulse", lambda c, m: soft_union(c, [Ell(450, 300, 120, 80)], (220, 90, 160), 0.15, spread=40), daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=0.4)),
]

L598_DIFFS = [
    ("stalactite", 640, 110, 0),
    ("stalagmite", 640, 350, 0),
    ("visitor", 621, 474, 0),
    ("guide", 761, 476, 0),
    ("bat", 300, 146, 0),
]


# =================================================================== Level 599 puffin cliffs
def puffin(c, x, base, s=1.0, beak=(250, 120, 50)):
    piece(c, [Ell(x, base - 18 * s, 12 * s, 18 * s), Circ(x + 2 * s, base - 38 * s, 10 * s)], (30, 30, 36), border=1, shadow=SMALL)
    flat(c, [Ell(x + 2 * s, base - 16 * s, 8 * s, 14 * s), Ell(x + 4 * s, base - 38 * s, 7 * s, 6 * s)], (250, 250, 250))
    flat(c, Poly([(x + 10 * s, base - 42 * s), (x + 22 * s, base - 36 * s), (x + 10 * s, base - 30 * s)]), beak)
    flat(c, Circ(x + 5 * s, base - 40 * s, 1.6 * s), INK)
    flat(c, [Ell(x - 4 * s, base, 5 * s, 2 * s), Ell(x + 6 * s, base, 5 * s, 2 * s)], (250, 120, 50))


def l599_bg(c, d):
    sky(c, (120, 180, 230), (230, 236, 240), 260)
    cloud_bank(c, 110, (250, 250, 246), 5991, k=0.6)
    sea(c, 230, seed=5992, n=14)
    # sea stacks
    for k, (x, w, h) in enumerate(((620, 60, 180), (720, 40, 120), (820, 70, 210))):
        piece(c, Poly([(x - w / 2, 420), (x - w / 2 + 8, 420 - h), (x + w / 2 - 8, 420 - h), (x + w / 2, 420)]), (150, 136, 126) if not (k == 1 and "stack" in d)
              else (200, 170, 120), border=1.5, shadow=PROP)
        flat(c, Thick(x - w / 2 + 8, 420 - h, x + w / 2 - 8, 420 - h, 6), (120, 170, 100))
    # cliff top (left) grassy, with burrows
    piece(c, Poly([(-10, 300), (520, 330), (560, 420), (520, 612), (-10, 612)]), (140, 120, 110), shadow=LAYER)
    piece(c, Poly([(-10, 300), (520, 330), (530, 360), (-10, 340)]), (110, 170, 90), shadow=SMALL)
    piece(c, Poly([(-10, 340), (530, 360), (520, 612), (-10, 612)]), (120, 176, 96), shadow=SMALL)
    for x, y in ((120, 420), (260, 400), (380, 450), (200, 520)):
        flat(c, Ell(x, y, 16, 9), (60, 50, 50))
    # puffins
    for k, (x, b, s) in enumerate(((140, 420, 1.3), (300, 404, 1.2), (400, 456, 1.4), (230, 524, 1.5), (90, 500, 1.2))):
        if k == 2 and "beak" in d:
            continue
        puffin(c, x, b, s=s)
    # birdwatchers + telescope + sign
    modern(c, 520, 600, (90, 150, 110), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.2, glasses=True)
    flat(c, [Thick(470, 600, 480, 540, 3), Thick(490, 600, 480, 540, 3)], (60, 60, 70))
    piece(c, Thick(470, 530, 506, 516, 10), (60, 60, 70) if "scope" not in d else (220, 80, 70), border=1, shadow=SMALL)
    modern(c, 360, 600, (240, 200, 90) if "kid" not in d else (200, 110, 200), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.6, style="twin")
    flat(c, Thick(40, 600, 40, 540, 4), (120, 90, 60))
    piece(c, RRect(10, 500, 90, 544, 3), (240, 236, 220) if "sign" not in d else (240, 200, 120), border=1.2, shadow=PROP)
    puffin(c, 50, 538, s=0.8)


L599_ELEMENTS = [
    E("fly%d" % i, (lambda x, y: lambda c, m: (piece(c, Ell(x, y, 10, 6), (30, 30, 36), shadow=None), flat(c, [Thick(x - 12, y - 4, x, y, 3), Thick(x, y, x + 12, y - 4, 3)],
                                                                                                         (30, 30, 36)),
                                              flat(c, Poly([(x + 9, y - 2), (x + 16, y), (x + 9, y + 2)]), (250, 120, 50))))(x, y),
      anim=dict(drift_across(x - 16, x + 16, 40 + i * 10, start=i * 300), bobAmplitude=(0, 8), bobSpeed=0.4)) for i, (x, y) in enumerate(((0, 200), (0, 260)))
] + [
    E("waves", lambda c, m: flat(c, [Ell(600 + k * 110, 424, 40, 5) for k in range(3)], (250, 252, 255, 0.85)), anim=dict(bobAmplitude=(0, 5), bobSpeed=0.3)),
    E("peek", lambda c, m: puffin(c, 260, 404, s=1.2), pivot=(260, 404), anim=dict(swingAngle=5, swingSpeed=0.6)),
]

L599_DIFFS = [
    ("stack", 720, 360, 0),
    ("beak", 404, 428, 0),
    ("scope", 488, 523, 0),
    ("sign", 50, 522, 0),
    ("kid", 361, 562, 0),
]


LEVELS = [
    ("Level590", "冰川徒步", l590_bg, L590_ELEMENTS, L590_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS590, blend=3.0), anim_seconds=20.0, frames=80)),
    ("Level591", "草莓田", l591_bg, L591_ELEMENTS, L591_DIFFS, 60, OPTS),
    ("Level592", "蝴蝶谷", l592_bg, L592_ELEMENTS, L592_DIFFS, 60, OPTS),
    ("Level593", "礁石潮池", l593_bg, L593_ELEMENTS, L593_DIFFS, 60, OPTS),
    ("Level594", "火山口湖", l594_bg, L594_ELEMENTS, L594_DIFFS, 60, OPTS),
    ("Level595", "骆驼商队", l595_bg, L595_ELEMENTS, L595_DIFFS, 60, dict(OPTS, day_night=DN595, anim_seconds=40.0, frames=80)),
    ("Level596", "雾凇森林", l596_bg, L596_ELEMENTS, L596_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS596, blend=3.0), anim_seconds=24.0, frames=80)),
    ("Level597", "油菜花田", l597_bg, L597_ELEMENTS, L597_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS597, blend=3.0), anim_seconds=30.0, frames=80)),
    ("Level598", "溶洞", l598_bg, L598_ELEMENTS, L598_DIFFS, 60, OPTS),
    ("Level599", "海鹦悬崖", l599_bg, L599_ELEMENTS, L599_DIFFS, 60, OPTS),
]
