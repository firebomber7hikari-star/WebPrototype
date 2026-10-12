# -*- coding: utf-8 -*-
"""Three Kingdoms China (184-280), paper-craft side views, full-bleed:
  Level94 桃园结义 - the oath in the peach garden: altar, incense, Liu Bei / Guan Yu / Zhang Fei
  Level95 赤壁之战 - the chained fleet burning below the red cliff, fire ships, Zhou Yu's flagship; day / night
  Level96 空城计   - Zhuge Liang plays the qin on the wall above an open gate while Sima Yi's cavalry hesitates
  Level97 三顾茅庐 - the third visit to the thatched cottage in the snow; snow weather cycle
  Level98 草船借箭 - straw boats collecting arrows in the fog before Cao Cao's water fortress; fog cycle
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_el, drift_across, gy, layer, sky, smoke_el
from stylekit import day_night, star_field, window_glow
from weather import CLOUDY, cloud, fog_layer, snow_layer
from levels_heian import blossom_tree, pine_jp
from levels_heian2 import snow_cap_pine
from cn_kit import (GOLDEN, GREY_TILE, RED, SKIN, arch, bamboo, lantern_cn, cn_hall, cn_roof, city_wall, ellipse_top, gate_tower, hanfu, horse_cn, junk, warrior)

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
GUAN_FACE = (190, 70, 60)
ZHANG_FACE = (120, 90, 80)


def flame(c, x, y, s=1.0):
    soft_union(c, [Circ(x, y - 10 * s, 14 * s)], (255, 160, 60), 0.5, spread=18 * s)
    flat(c, Poly([(x - 10 * s, y), (x + 10 * s, y), (x + 7 * s, y - 14 * s), (x, y - 30 * s), (x - 7 * s, y - 14 * s)]), (255, 140, 40))
    flat(c, Poly([(x - 5 * s, y), (x + 5 * s, y), (x, y - 16 * s)]), (255, 230, 130))


def flame_el(eid, x, y, s=1.0, show="both", phase=0.0):
    return E(eid, lambda c, m: flame(c, x, y, s), pivot=(x, y), show=show, daynight="untinted",
             anim=dict(stretch=(0.12, 0.25), scaleSpeed=2.4 + phase, twinkle=0.15, twinkleSpeed=3.0, phase=phase))


def pennant(eid, x, base, h, col, variant_col=None, phase=0.0):
    def d(c, m):
        cc = variant_col if (m and variant_col) else col
        flat(c, Thick(x, base, x, base - h, 2.5), (110, 80, 60))
        piece(c, Poly([(x + 1, base - h), (x + 34, base - h + 6), (x + 30, base - h + 20), (x + 34, base - h + 34), (x + 1, base - h + 40)]), cc,
              shadow=SMALL)
    return E(eid, d, pivot=(x, base - h + 20), variant=bool(variant_col),
             anim=dict(stretch=(0.12, 0), scaleSpeed=1.2 + phase, swingAngle=3, swingSpeed=0.7, phase=phase))


def thatched(c, x0, x1, base, h, wall=(196, 170, 120), roof=(176, 150, 96), window=True, open_win=True):
    piece(c, RRect(x0, base - h, x1, base, 1), wall, border=1.5, shadow=PROP)
    w = x1 - x0
    piece(c, Poly([(x0 - 18, base - h + 6), (x1 + 18, base - h + 6), (x1 - w * 0.2, base - h - w * 0.36), (x0 + w * 0.2, base - h - w * 0.36)]), roof,
          border=1.5, shadow=PROP)
    for k in range(int(w // 10)):
        flat(c, Thick(x0 - 14 + k * 11, base - h + 4, x0 + w * 0.2 + k * 7, base - h - w * 0.34, 1), lit(roof, 0.85))
    flat(c, RRect(x0 + w * 0.12, base - h * 0.62, x0 + w * 0.3, base, 1), (90, 70, 56))
    if window:
        flat(c, RRect(x0 + w * 0.5, base - h * 0.75, x0 + w * 0.82, base - h * 0.35, 1), (60, 50, 44) if open_win else (150, 120, 80))
        if not open_win:
            for k in range(1, 4):
                flat(c, Thick(x0 + w * (0.5 + 0.08 * k), base - h * 0.75, x0 + w * (0.5 + 0.08 * k), base - h * 0.35, 1.2), (110, 84, 60))
    return (x0 + w * 0.66, base - h * 0.55)


# =================================================================== Level 94 oath in the peach garden
def l94_bg(c, d):
    sky(c, (180, 214, 240), (250, 236, 222), 360)
    layer(c, 240, [(22, 0.007, 0.4), (8, 0.02, 1.2)], (160, 186, 170))
    layer(c, 286, [(12, 0.012, 1.0)], (140, 174, 130))
    for x, s in ((90, 1.0), (240, 0.9), (640, 0.9), (800, 1.1)):
        blossom_tree(c, x, 330, s, (246, 196, 210), 940 + x)
    thatched(c, 30, 200, 400, 80)
    if "pennant" not in d:
        flat(c, Thick(180, 320, 180, 270, 2), (110, 80, 60))
        flat(c, Poly([(181, 270), (204, 276), (181, 284)]), (220, 60, 50))
    piece(c, hill_strip(400, [(4, 0.01, 0.4), (2, 0.04, 1.0)]), (150, 182, 112), shadow=LAYER)
    for x in range(0, 900, 30):
        flat(c, Thick(x, 410, x + 16, 440, 2), (130, 160, 96))
    # altar with offerings and incense
    piece(c, RRect(330, 440, 570, 454, 1), (120, 60, 40), border=1.2, shadow=PROP)
    piece(c, RRect(338, 454, 562, 506, 1), (200, 50, 40), shadow=SMALL)
    flat(c, RRect(338, 470, 562, 476, 0), GOLDEN)
    for lx in (346, 554):
        flat(c, RRect(lx - 3, 454, lx + 3, 510, 1), (100, 50, 34))
    piece(c, [Ell(380, 422, 22, 18), RRect(370, 400, 390, 406, 1)], (60, 110, 180) if "jar" in d else (150, 90, 50), border=1.2, shadow=SMALL)
    piece(c, [Circ(510, 430, 9), Circ(526, 432, 9), Circ(518, 418, 9)], (240, 150, 160), shadow=None)
    if "incense" not in d:
        piece(c, [Ell(450, 430, 20, 10), RRect(438, 420, 462, 432, 2), RRect(436, 432, 442, 440, 1), RRect(458, 432, 464, 440, 1)], (170, 140, 80),
              border=1, shadow=SMALL)
        for dx in (-6, 0, 6):
            flat(c, Thick(450 + dx, 420, 450 + dx, 396, 1.2), (200, 60, 50))
    # the three brothers
    for x in range(60, 860, 46):
        flat(c, [Thick(x, 600, x - 4, 586, 2), Thick(x + 4, 600, x + 6, 584, 2)], (110, 150, 90))
    for x, y in ((150, 560), (760, 566)):
        piece(c, [Ell(x, y, 26, 8), RRect(x - 16, y, x + 16, y + 24, 3)], (170, 166, 156), border=1.2, shadow=PROP)
    for x in (110, 220, 690, 800):
        piece(c, [Circ(x - 10, 594, 10), Circ(x + 4, 588, 12), Circ(x + 16, 596, 9)], (90, 150, 90), shadow=PROP)
        flat(c, [Circ(x - 8, 588, 4), Circ(x + 6, 582, 4), Circ(x + 16, 590, 3.5)], (240, 120, 160))
    warrior(c, 330, 596, (60, 140, 90) if "robe" not in d else (60, 90, 170), h=1.7, face=GUAN_FACE, beard=(20, 20, 24), helmet=(60, 140, 90),
            plume=None, weapon="blade")
    hanfu(c, 450, 598, (230, 200, 120), h=1.7, hat="guan", hat_col=(150, 60, 180) if "hat" in d else (30, 28, 32), beard=None)
    warrior(c, 570, 596, (60, 60, 70), h=1.7, face=ZHANG_FACE, beard=(20, 20, 24), helmet=(40, 40, 46), plume=None,
            weapon="spear" if "spear" in d else "snake")
    blossom_tree(c, 20, 612, 1.8, (246, 196, 210), 941)
    blossom_tree(c, 880, 612, 1.7, (250, 250, 250) if "peach" in d else (246, 196, 210), 942)


def petal(i, x, y):
    def d(c, m):
        flat(c, Ell(x, y, 3.2, 2.2), (250, 196, 210))
    return E("petal%d" % i, d, pivot=(x, y), anim=dict(driftVelocity=(14, -22), driftLength=380, driftFade=True, rotateSpeed=90 + i * 13,
                                                       spinSpeed=0.6 + 0.07 * i, spinShade=0.3, bobAmplitude=(10, 0), bobSpeed=0.4,
                                                       phase=(i * 0.137) % 1))


L94_ELEMENTS = smoke_el("incense_smoke", 450, 392, n=3, col=(236, 236, 240), r=5, rise=(4, 20), length=70, show="A") + [
    bird_el("bird0", 520, 120, 8, speed=16), bird_el("bird1", 546, 110, 6, speed=16),
] + [petal(i, x, y) for i, (x, y) in enumerate(((60, 420), (120, 380), (840, 420), (880, 380), (260, 300), (640, 300), (800, 280), (40, 360)))]

L94_DIFFS = [
    ("robe", 330, 560, 0),
    ("hat", 452, 510, 0),
    ("spear", 602, 380, 0),
    ("jar", 380, 420, 0),
    ("incense", 450, 420, 0),
    ("pennant", 192, 276, 0),
    ("peach", 880, 480, 0),
]


# =================================================================== Level 95 Red Cliffs (day / night)
DN95 = day_night(40.0, tint=(0.30, 0.26, 0.48))
FLEET95 = [(30, 380), (220, 384), (410, 380)]
FLAG95 = (640, 360)


def l95_bg(c, d):
    sky(c, (190, 180, 200), (250, 200, 160), 330)
    layer(c, 250, [(16, 0.008, 0.6)], (150, 140, 150))
    # red cliff on the right
    piece(c, Poly([(700, 330), (720, 160), (780, 120), (860, 110), (920, 130), (920, 340)]), (176, 70, 50), shadow=LAYER)
    for y in range(150, 330, 20):
        flat(c, Thick(720 + (330 - y) * 0.02, y, 910, y + 6, 2), (150, 56, 40))
    if "pine" not in d:
        pine_jp(c, 800, 130, 0.8)
    c.rect(0, 320, W, H, (80, 110, 130))
    for y in range(332, 600, 14):
        for x in range((y * 13) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (110, 140, 160))
    # Cao Cao's chained fleet
    for i, (x, b) in enumerate(FLEET95):
        sail = ((90, 140, 90) if "sail" in d else (200, 180, 140)) if i == 1 else (200, 180, 140)
        junk(c, x, b, 170, hull=(90, 70, 60), sail=sail, roof=(60, 70, 110))
    for i in range(len(FLEET95) - 1):
        if i == 1 and "chain" in d:
            continue
        x0 = FLEET95[i][0] + 160
        x1 = FLEET95[i + 1][0] + 10
        for k in range(6):
            t = k / 5
            flat(c, Ell(x0 + (x1 - x0) * t, 362 + 6 * math.sin(math.pi * t), 4, 2.5), (60, 60, 66))
    # Zhou Yu's flagship (foreground right)
    junk(c, 560, 560, 300, hull=(120, 50, 40), sail=None, roof=None)
    piece(c, RRect(620, 470, 780, 528, 3), (150, 50, 40), border=1.5, shadow=PROP)
    cn_roof(c, 620, 780, 470, 20, (60, 60, 70))
    flat(c, Thick(FLAG95[0], 528, FLAG95[0], 300, 3), (110, 80, 60))
    piece(c, Poly([(FLAG95[0] + 1, 300), (FLAG95[0] + 56, 306), (FLAG95[0] + 50, 330), (FLAG95[0] + 56, 352), (FLAG95[0] + 1, 356)]),
          (40, 80, 160) if "banner" in d else (200, 40, 40), border=1.2, shadow=SMALL)
    flat(c, Circ(FLAG95[0] + 26, 328, 10), (240, 220, 160))
    if "drum" not in d:
        piece(c, [Ell(820, 512, 20, 16), Thick(808, 528, 804, 540, 3), Thick(832, 528, 836, 540, 3)], (180, 60, 40), border=1.2, shadow=SMALL)
        flat(c, Ell(820, 510, 14, 11), (230, 214, 180))
    warrior(c, 700, 528, (200, 50, 40), helmet=(110, 120, 140) if "plume" in d else (200, 160, 60), plume=(240, 240, 240), weapon="sword")
    flat(c, Thick(860, 528, 860, 470, 2), (110, 80, 60))
    lantern_cn(c, 860, 486, (60, 160, 90) if "lantern" in d else (220, 50, 40), r=9)
    for x in (600, 760, 790):
        warrior(c, x, 528, (90, 40, 40), h=0.8, helmet=(110, 110, 120), plume=(200, 40, 40), weapon="spear")


def fireship(x, y, k=1.0):
    def d(c, m):
        piece(c, Poly([(x - 40 * k, y - 10 * k), (x + 40 * k, y - 12 * k), (x + 32 * k, y), (x - 34 * k, y)]), (100, 70, 50), border=1.2, shadow=SMALL)
        piece(c, Ell(x, y - 18 * k, 26 * k, 10 * k), (200, 170, 100), shadow=None)
        flame(c, x - 8 * k, y - 22 * k, 0.9 * k)
        flame(c, x + 12 * k, y - 20 * k, 0.7 * k)
    return d


L95_ELEMENTS = [
    E("sun", lambda c, m: piece(c, Circ(160, 110, 30), (255, 200, 120), border=2, shadow=PROP), daynight="day"),
    E("moon", lambda c, m: (soft_union(c, [Circ(160, 110, 30)], (255, 250, 220), 0.35, spread=18),
                            piece(c, Circ(160, 110, 24), (252, 246, 220), border=2, shadow=PROP)), daynight="night"),
    star_field("stars", 95, 30, 160, avoid=[(110, 60, 210, 160)]),
] + [flame_el("fire%d" % i, x, y, s, phase=i * 0.17) for i, (x, y, s) in enumerate(((70, 352, 1.2), (130, 340, 1.0), (240, 352, 0.9), (440, 352, 1.3),
                                                                                     (500, 346, 1.0)))] + \
    smoke_el("smoke", 260, 300, n=4, col=(90, 80, 80), r=14, rise=(-20, 26), length=120) + [
    E("fireship0", fireship(560, 420, 0.8), pivot=(560, 420), anim=dict(drift_across(520, 600, -6), bobAmplitude=(0, 2), bobSpeed=0.3)),
    E("fireship1", fireship(700, 440, 0.9), pivot=(700, 440), anim=dict(drift_across(660, 740, -7, 300), bobAmplitude=(0, 2), bobSpeed=0.33)),
    pennant("wind", 560, 528, 160, (240, 236, 226), phase=0.3),
]

L95_DIFFS = [
    ("banner", FLAG95[0] + 28, 328, 0),
    ("plume", 701, 482, 0),
    ("drum", 820, 512, 0),
    ("lantern", 860, 486, 0),
    ("chain", 400, 364, 0),
    ("sail", 300, 300, 0),
    ("pine", 800, 90, 0),
]


# =================================================================== Level 96 the empty city
def l96_bg(c, d):
    sky(c, (190, 210, 230), (246, 232, 210), 330)
    layer(c, 230, [(24, 0.006, 0.3), (10, 0.02, 1.1)], (150, 160, 176))
    city_wall(c, -10, 910, 300, 470)
    flat(c, arch(410, 490, 360, 470), (40, 34, 30))
    gate_tower(c, 450, 300, w=200, h=64)
    # Zhuge Liang playing the qin on the tower terrace, two boys, incense
    piece(c, RRect(400, 280, 500, 288, 1), (120, 70, 50), shadow=SMALL)
    piece(c, RRect(410, 270, 490, 280, 2), (90, 60, 44), border=1, shadow=SMALL)
    hanfu(c, 450, 300, (236, 236, 240), hat="guan", hat_col=(30, 28, 32), beard=(30, 30, 34))
    piece(c, Poly([(478, 262), (494, 240), (500, 256)]), (240, 240, 246) if "fan" not in d else (90, 140, 200), border=1, shadow=SMALL)
    hanfu(c, 390, 300, (100, 160, 120) if "boy" in d else (200, 90, 80), hat="bun", h=0.7)
    hanfu(c, 520, 300, (90, 120, 180), hat="bun", h=0.7)
    if "incense" not in d:
        piece(c, [Ell(420, 268, 8, 5), RRect(414, 262, 426, 268, 1)], (170, 140, 80), shadow=None)
    # lowered banners on the wall (one leaning flag in A)
    if "flag" not in d:
        flat(c, Thick(250, 290, 290, 240, 2.5), (110, 80, 60))
        piece(c, Poly([(290, 240), (300, 268), (280, 276), (272, 252)]), (220, 60, 50), shadow=SMALL)
    # road with old sweepers
    piece(c, RRect(-10, 468, 910, 612, 0), (206, 190, 150), shadow=LAYER)
    for x in (400, 500):
        hanfu(c, x, 520, (120, 110, 90), hat="straw", hat_col=(200, 176, 120), h=0.85)
    # Sima Yi's cavalry on both sides
    for x in (60, 170):
        horse_cn(c, x, 590, (230, 226, 216) if (x == 60 and "horse2" in d) else (60, 50, 50), saddle=(40, 60, 120))
        warrior(c, x - 2, 554, (40, 50, 90), h=0.9, helmet=(90, 90, 100), plume=(40, 60, 160), weapon="spear")
    horse_cn(c, 780, 590, (130, 90, 60) if "horse" in d else (230, 226, 216), flip=True, saddle=(40, 60, 120))
    warrior(c, 782, 554, (40, 50, 90), h=0.95, helmet=(90, 90, 100), plume=(40, 60, 160))
    horse_cn(c, 880, 596, (90, 70, 60), flip=True, saddle=(40, 60, 120))
    flat(c, Thick(700, 596, 700, 470, 3), (110, 80, 60))
    piece(c, Poly([(701, 470), (746, 476), (742, 500), (746, 524), (701, 530)]), (90, 140, 90) if "sima" in d else (40, 60, 140), border=1.2,
          shadow=SMALL)
    flat(c, Circ(722, 500, 9), (240, 220, 160))


def sweeper(x, i):
    def d(c, m):
        flat(c, Thick(x + 6, 500, x - 12, 524, 2), (150, 120, 80))
        piece(c, Poly([(x - 20, 522), (x - 6, 520), (x - 8, 528), (x - 22, 528)]), (200, 176, 110), shadow=None)
    return E("broom%d" % i, d, pivot=(x + 6, 500), show="A" if i == 1 else "both", anim=dict(swingAngle=14, swingSpeed=0.5 + i * 0.1))


L96_ELEMENTS = [
    cloud_el("cloud0", 200, 60, 0.7, 6), cloud_el("cloud1", 640, 80, 0.5, 5),
    sweeper(400, 0), sweeper(500, 1),
] + smoke_el("incense_smoke", 420, 260, n=3, col=(236, 236, 240), r=4, rise=(4, 16), length=50, show="A") + [
    pennant("banner_l", 110, 470, 150, (40, 60, 140), phase=0.1), pennant("banner_r", 840, 470, 150, (40, 60, 140), phase=0.5),
    bird_el("crow0", 300, 150, 9, col=(40, 40, 46), speed=14), bird_el("crow1", 330, 138, 7, col=(40, 40, 46), speed=14),
]

L96_DIFFS = [
    ("fan", 490, 252, 0),
    ("boy", 390, 284, 0),
    ("incense", 420, 266, 0),
    ("flag", 280, 260, 0),
    ("horse", 780, 554, 0),
    ("sima", 722, 500, 0),
    ("broom", 486, 524, 0),
    ("horse2", 60, 560, 0),
]


# =================================================================== Level 97 third visit to the thatched cottage (snow)
STEPS97 = [(SNOW, 10), (OVERCAST, 6), (CLEAR, 8)]
WEATHER97 = dict(steps=STEPS97, blend=3.0, tints={SNOW: (0.9, 0.92, 0.98), OVERCAST: (0.88, 0.9, 0.94)})


def l97_bg(c, d):
    sky(c, (200, 210, 226), (238, 240, 246), 380)
    layer(c, 230, [(26, 0.007, 0.4), (10, 0.02, 1.2)], (220, 226, 238))
    layer(c, 280, [(12, 0.012, 1.0)], (206, 214, 230))
    bamboo(c, 560, 900, 140, 420, 971, col=(110, 150, 110))
    for x in range(570, 900, 30):
        flat(c, Ell(x, 150 + (x % 5) * 6, 14, 4), (248, 250, 255))
    if "pavilion" not in d:                         # a small pavilion on the far snowy hill
        piece(c, [RRect(112, 246, 168, 290, 1)], (170, 120, 90), border=1.5, shadow=SMALL)
        flat(c, [RRect(122, 258, 134, 290, 1), RRect(146, 258, 158, 290, 1)], (90, 60, 50))
        piece(c, Poly([(96, 250), (184, 250), (162, 226), (118, 226)]), (90, 80, 100), border=1.5, shadow=SMALL)
        flat(c, Poly([(100, 248), (180, 248), (160, 230), (120, 230)]), (248, 250, 255))
    piece(c, hill_strip(420, [(4, 0.01, 0.4)]), (240, 244, 250), shadow=LAYER)
    # cottage with wattle fence and gate
    thatched(c, 600, 820, 440, 96, open_win="window" not in d)
    flat(c, [Ell(710, 312, 120, 10)], (250, 252, 255))
    for x in range(560, 900, 14):
        flat(c, Thick(x, 470, x, 440, 3), (150, 120, 80))
    flat(c, [Thick(560, 452, 900, 452, 2), Thick(560, 462, 900, 462, 2)], (130, 100, 70))
    if "gate" in d:
        piece(c, RRect(620, 440, 660, 472, 1), (140, 110, 74), shadow=SMALL)
    hanfu(c, 700, 478, (200, 90, 80) if "boy" in d else (120, 160, 120), hat="bun", h=0.75)
    if "window" not in d:
        hanfu(c, 700, 380, (236, 236, 240), hat="guan", h=0.6)
    blossom_tree(c, 520, 470, 1.0, (246, 244, 250) if "plum" in d else (210, 50, 80), 971, trunk=(70, 56, 54))
    # the three brothers waiting with their horses
    piece(c, hill_strip(470, [(3, 0.012, 0.4)]), (244, 247, 252), shadow=LAYER)
    horse_cn(c, 90, 586, (230, 226, 216))
    horse_cn(c, 200, 590, (130, 90, 60) if "horse" in d else (40, 36, 40))
    hanfu(c, 300, 590, (200, 60, 50) if "cloak" not in d else (90, 110, 170), hat="guan", beard=(30, 30, 34))
    warrior(c, 370, 588, (60, 140, 90), face=GUAN_FACE, beard=(20, 20, 24), helmet=(60, 140, 90), plume=None,
            weapon="blade" if "blade" not in d else "spear")
    warrior(c, 440, 590, (60, 60, 70), face=ZHANG_FACE, beard=(20, 20, 24), helmet=(40, 40, 46), plume=None, weapon="snake")
    pine_jp(c, 40, 612, 1.5)
    snow_cap_pine(c, 40, 612, 1.5)
    rnd = random.Random(97)
    for k in range(20):
        flat(c, Ell(470 + k * 8, 520 + 6 * math.sin(k), 3, 2), (214, 222, 238))


L97_ELEMENTS = [
    E("sun", lambda c, m: piece(c, Circ(200, 80, 24), (255, 236, 180), border=2, shadow=PROP), weather=W_(CLEAR)),
    cloud("cloudA", 300, 70, 0.9, (226, 230, 238), W_(SNOW, OVERCAST), anim=dict(bobAmplitude=(26, 0), bobSpeed=0.02)),
    cloud("cloudB", 700, 50, 1.0, (214, 220, 230), W_(SNOW, OVERCAST), anim=dict(bobAmplitude=(-22, 0), bobSpeed=0.025)),
    snow_layer("snowFar", 971, 50, 1.4, 2.6, 26),
    snow_layer("snowNear", 972, 26, 3.0, 4.6, 46, sway=12),
] + smoke_el("chimney", 790, 330, n=3, col=(230, 230, 236), r=6, rise=(4, 18), length=60) + [
    E("horse_tail", lambda c, m: flat(c, Thick(58, 548, 50, 570, 3), (40, 34, 34)), pivot=(58, 548), anim=dict(swingAngle=12, swingSpeed=0.4)),
]

L97_DIFFS = [
    ("window", 760, 386, 0),
    ("gate", 640, 456, 0),
    ("plum", 520, 400, 0),
    ("horse", 200, 552, 0),
    ("cloak", 300, 570, 0),
    ("blade", 392, 450, 0),
    ("boy", 700, 456, 0),
    ("pavilion", 140, 258, 0),
]


# =================================================================== Level 98 borrowing arrows with straw boats (fog)
STEPS98 = [(FOG, 10), (OVERCAST, 8)]
WEATHER98 = dict(steps=STEPS98, blend=3.0, tints={FOG: (0.86, 0.87, 0.9), OVERCAST: (0.86, 0.87, 0.9)})
BOATS98 = [(470, 440), (650, 480), (300, 520)]


def straw_boat(c, x, y, arrows=True, hat=(200, 176, 120), k=1.0):
    junk(c, x - 100 * k, y, 200 * k, hull=(100, 76, 56), sail=None)
    for i in range(6):
        bx = x - 80 * k + i * 30 * k
        piece(c, [Poly([(bx - 9 * k, y - 30 * k), (bx + 9 * k, y - 30 * k), (bx + 6 * k, y - 70 * k), (bx - 6 * k, y - 70 * k)]), Circ(bx, y - 76 * k, 6 * k)],
              (206, 180, 110), shadow=SMALL)
        flat(c, Poly([(bx - 11 * k, y - 78 * k), (bx + 11 * k, y - 78 * k), (bx, y - 88 * k)]), hat)
        if arrows:
            for j in range(4):
                ay = y - 40 * k - j * 8 * k
                flat(c, Thick(bx - 4 * k, ay, bx - 22 * k, ay - 3 * k, 1.2), (110, 80, 60))
                flat(c, Poly([(bx - 22 * k, ay - 5 * k), (bx - 26 * k, ay - 3 * k), (bx - 22 * k, ay - 1 * k)]), (220, 220, 220))


def l98_bg(c, d):
    sky(c, (190, 196, 206), (226, 226, 222), 320)
    layer(c, 240, [(18, 0.008, 0.6)], (176, 182, 190))
    c.rect(0, 300, W, H, (100, 120, 130))
    for y in range(312, 600, 14):
        for x in range((y * 13) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (130, 146, 154))
    # Cao Cao's water fortress on the left
    for x in range(-10, 250, 12):
        piece(c, Poly([(x, 420), (x + 10, 420), (x + 10, 340), (x + 5, 330), (x, 340)]), (130, 100, 70), shadow=None)
    for tx in (40, 190):
        piece(c, [RRect(tx - 24, 230, tx + 24, 330, 1)], (120, 92, 66), border=1.2, shadow=PROP)
        cn_roof(c, tx - 26, tx + 26, 230, 18, (70, 70, 80))
        for k in range(3):
            warrior(c, tx - 14 + k * 14, 330, (40, 50, 90), h=0.55, helmet=(90, 90, 100), plume=None)
    flat(c, Thick(190, 210, 190, 150, 2), (110, 80, 60))
    piece(c, Poly([(191, 150), (226, 156), (191, 166)]), (90, 140, 90) if "tower_flag" in d else (40, 60, 140), shadow=SMALL)
    # straw boats (the nearest one carries Zhuge Liang and Lu Su)
    straw_boat(c, *BOATS98[0], arrows=True, k=0.8)
    straw_boat(c, *BOATS98[1], arrows="arrows" not in d, hat=(110, 110, 120) if "strawhat" in d else (200, 176, 110), k=0.9)
    x, y = BOATS98[2]
    junk(c, x - 150, y + 60, 300, hull=(110, 80, 56), sail=None)
    piece(c, RRect(x - 70, y - 4, x + 70, y + 30, 3), (130, 96, 64), border=1.2, shadow=PROP)
    cn_roof(c, x - 74, x + 74, y - 4, 16, (90, 80, 70))
    hanfu(c, x - 30, y + 30, (236, 236, 240), hat="guan", beard=(30, 30, 34))
    hanfu(c, x + 30, y + 30, (90, 120, 170) if "lusu" in d else (160, 80, 60), hat="guan")
    piece(c, [Ell(x, y + 22, 8, 7), RRect(x - 3, y + 12, x + 3, y + 16, 1)], (60, 110, 180) if "jar" in d else (150, 90, 50), shadow=SMALL)
    for bx in (x + 110, x + 140):
        piece(c, [Ell(bx, y + 50, 14, 12)], (200, 60, 40) if not ("drum" in d and bx == x + 110) else (60, 110, 60), border=1, shadow=SMALL)
        flat(c, Ell(bx, y + 46, 10, 8), (230, 214, 180))
    flat(c, Thick(x + 180, y + 60, x + 180, y - 90, 3), (110, 80, 60))
    lantern_cn(c, x + 180, y - 60, (60, 160, 90) if "lantern" in d else (220, 50, 40), r=9)


def arrow_el(i, x, y):
    def d(c, m):
        flat(c, Thick(x, y, x + 36, y + 4, 1.4), (90, 70, 56))
        flat(c, Poly([(x + 36, y + 1), (x + 44, y + 5), (x + 36, y + 7)]), (200, 200, 210))
    return E("arrow%d" % i, d, pivot=(x, y), anim=dict(driftVelocity=(220, -24), driftLength=420, driftFade=True, phase=(i * 0.29) % 1))


L98_ELEMENTS = [arrow_el(i, x, y) for i, (x, y) in enumerate(((200, 300), (220, 330), (180, 360), (240, 280), (200, 390), (230, 350)))] + [
    fog_layer("fog0", 981, 250, 320, 0.42, 14), fog_layer("fog1", 982, 330, 380, 0.3, 20, direction=-1),
    fog_layer("fog2", 983, 600, 650, 0.25, 26),
    E("drummer", lambda c, m: flat(c, Thick(BOATS98[2][0] + 96, BOATS98[2][1] + 30, BOATS98[2][0] + 108, BOATS98[2][1] + 40, 2.4), (110, 80, 60)),
      pivot=(BOATS98[2][0] + 96, BOATS98[2][1] + 30), anim=dict(swingAngle=20, swingSpeed=1.2)),
]

L98_DIFFS = [
    ("tower_flag", 206, 158, 0),
    ("arrows", BOATS98[1][0] - 60, BOATS98[1][1] - 50, 0),
    ("strawhat", BOATS98[1][0] + 30, BOATS98[1][1] - 76, 0),
    ("lusu", BOATS98[2][0] + 30, BOATS98[2][1] + 10, 0),
    ("jar", BOATS98[2][0], BOATS98[2][1] + 20, 0),
    ("drum", BOATS98[2][0] + 110, BOATS98[2][1] + 48, 0),
    ("lantern", BOATS98[2][0] + 180, BOATS98[2][1] - 60, 0),
]

LEVELS = [
    ("Level94", "桃园结义", l94_bg, L94_ELEMENTS, L94_DIFFS, 140, OPTS),
    ("Level95", "赤壁之战", l95_bg, L95_ELEMENTS, L95_DIFFS, 140, dict(OPTS, day_night=DN95, anim_seconds=40.0, frames=80)),
    ("Level96", "空城计", l96_bg, L96_ELEMENTS, L96_DIFFS, 140, OPTS),
    ("Level97", "三顾茅庐", l97_bg, L97_ELEMENTS, L97_DIFFS, 140, dict(OPTS, weather=WEATHER97, anim_seconds=24.0, frames=48)),
    ("Level98", "草船借箭", l98_bg, L98_ELEMENTS, L98_DIFFS, 140, dict(OPTS, weather=WEATHER98, anim_seconds=18.0, frames=36)),
]
