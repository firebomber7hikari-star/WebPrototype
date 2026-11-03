# -*- coding: utf-8 -*-
"""Toon-render (cel-shaded) levels, set 3 - following the five-star toon favourites (windmill meadow, attic bedroom,
candy cottage, JRPG village / forest, toon gothic library / bridge). Original designs, no text.
  Level1631 卡通·魔女小屋 - a witch's cottage interior at night: cauldron, broom, shelves, black cat, moon window
  Level1632 卡通·幽灵船   - a ghost ship's deck under the moon: tattered sails, lanterns, a glowing wheel
  Level1633 卡通·旅店客房 - a cosy inn room: bed, the hero's gear, window over the village rooftops
  Level1634 卡通·花田风车 - a windmill above striped flower fields, a picnic and a kite
  Level1635 卡通·林间树屋 - a treehouse in a big oak: rope ladder, swing, lanterns, kids' treasures
  Level1636 卡通·南瓜田夜 - a pumpkin patch at night: jack-o'-lanterns, scarecrow, crows, harvest moon
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Poly, Rough, Seg, Under, Union, el, fbm1, mixc, vgrad
from levels_remake import ToonS
from levels_real2 import arch
from toon import INK, bird_el, cel, cloud_el, cloud_shape, puff_el, shade_of, tint_of, toon_post
from styled_kit import (barrel, bush, chest, crate, hero, mage, person, pine_tree, potion, round_tree, sparkle_el)
from levels_souls_toon import bat_el, candle, flame_el, lantern, moon, toon_tree
from levels_jrpg import cottage

S = ToonS()
OPTS = dict(post=toon_post, anim_seconds=12.0, frames=60)
FIRE = (255, 190, 90)


def make(scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, d)
        S.finish(g)
        g.commit()
    return bg


def wave(y, amp, period, seed):
    return lambda x: y + amp * np.sin(x / period + seed) + (fbm1(x, 60, 2, seed) - 0.5) * amp


def cat(g, x, base, s=1.0, col=(30, 26, 40), eyes=(250, 220, 80), face=1):
    S.obj(g, Union([Ell(x, base - 18 * s, 26 * s, 18 * s), Circ(x + face * 24 * s, base - 36 * s, 13 * s),
                    Poly([(x + face * 14 * s, base - 44 * s), (x + face * 16 * s, base - 62 * s), (x + face * 24 * s, base - 47 * s)]),
                    Poly([(x + face * 28 * s, base - 47 * s), (x + face * 36 * s, base - 62 * s), (x + face * 36 * s, base - 42 * s)]),
                    Seg(x - face * 24 * s, base - 16 * s, x - face * 40 * s, base - 50 * s, 4 * s, 2.5 * s)]), col, 1)
    for ex in (18, 30):
        S.flat(g, Ell(x + face * ex * s, base - 38 * s, 3 * s, 3.6 * s), eyes)


def pumpkin(g, x, base, r, col=(250, 140, 40), face=False, seed=0):
    S.obj(g, Union([Ell(x - r * 0.45, base - r * 0.75, r * 0.6, r * 0.75), Ell(x + r * 0.45, base - r * 0.75, r * 0.6, r * 0.75), Ell(x, base - r * 0.8, r * 0.6, r * 0.8)]),
          col, seed, hi=True)
    S.obj(g, Seg(x, base - r * 1.5, x + r * 0.15, base - r * 1.85, r * 0.12), (110, 140, 60), seed + 1)
    if face:
        g.glow(x, base - r * 0.7, r * 1.6, FIRE, 0.35)
        S.flat(g, Union([Poly([(x - r * 0.45, base - r * 0.95), (x - r * 0.2, base - r * 0.95), (x - r * 0.32, base - r * 1.2)]),
                         Poly([(x + r * 0.2, base - r * 0.95), (x + r * 0.45, base - r * 0.95), (x + r * 0.32, base - r * 1.2)]),
                         Poly([(x - r * 0.5, base - r * 0.6), (x + r * 0.5, base - r * 0.6), (x + r * 0.3, base - r * 0.35), (x, base - r * 0.48), (x - r * 0.3, base - r * 0.35)])]),
               (255, 230, 120))


# =================================================================== Level 1631 witch's cottage
def l1631(g, d):
    S.obj(g, Box(-2, -2, W + 2, 440), (110, 90, 120), 1, line=False)
    for x in range(0, 900, 60):
        S.flat(g, Box(x, -2, x + 3, 440), (90, 72, 100))
    S.obj(g, Box(-2, 30, W + 2, 50), (110, 76, 56), 2, "wood")
    # round moon window
    S.obj(g, Circ(450, 170, 92), (130, 110, 90), 3)
    g.fill(Circ(450, 170, 80), vgrad([(90, (40, 50, 110)), (250, (90, 100, 170))]))
    moon(g, 480, 140, 26)
    for x, y in ((400, 120), (420, 210), (510, 200)):
        S.flat(g, Circ(x, y, 2), (255, 250, 230))
    S.flat(g, Inter(Union([Box(447, 80, 453, 250), Box(370, 167, 530, 173)]), Circ(450, 170, 80)), (130, 110, 90))
    # shelves with potions and books (left)
    for y in (120, 210):
        S.obj(g, Box(30, y, 300, y + 10), (150, 100, 66), 4 + y, "wood")
    for i, (x, c) in enumerate(((60, (230, 70, 90)), (100, (90, 200, 120)), (140, (110, 140, 250)), (180, (250, 200, 70)), (220, (200, 110, 220)))):
        if "potion" in d and i == 2:
            c = (250, 140, 60)
        potion(S, g, x, 120, c, s=1.3, seed=10 + i)
    for i in range(6):
        S.obj(g, Box(40 + i * 18, 150, 56 + i * 18, 210), [(200, 70, 70), (70, 100, 170), (90, 150, 90), (220, 170, 80)][i % 4], 20 + i)
    if "skull" not in d:
        S.obj(g, Union([Ell(220, 186, 26, 20), Box(206, 196, 234, 210, 3)]), (250, 240, 210), 30, hi=True)
        for ex in (210, 230):
            S.flat(g, Ell(ex, 186, 6, 7), (60, 40, 70))
    # broom and hat on hooks (right)
    S.obj(g, Seg(760, 80, 800, 420, 4), (170, 120, 70), 31)
    S.obj(g, Poly([(786, 380), (814, 380), (830, 440), (770, 440)]), (220, 180, 90), 32)
    hatc = (60, 40, 90) if "hat" not in d else (40, 110, 80)
    S.obj(g, Union([Ell(650, 140, 50, 10), Poly([(620, 140), (660, 60), (690, 70), (676, 140)])]), hatc, 33)
    S.flat(g, Box(626, 128, 676, 138), (250, 200, 70))
    # floor, rug, cauldron on the hearth
    S.ground(g, Box(-2, 440, W + 2, H + 2), (140, 96, 70), "wood", 34, line=True)
    S.obj(g, Ell(450, 540, 260, 44), (170, 60, 90), 35)
    S.flat(g, Ell(450, 540, 220, 34) - Ell(450, 540, 210, 30), (250, 210, 90))
    S.glow(g, 450, 470, 140, (130, 250, 140), 0.3)
    S.obj(g, Union([Ell(450, 500, 90, 60), Box(366, 446, 534, 460)]), (50, 46, 60), 36, hi=True)
    S.obj(g, Ell(450, 452, 80, 14), (130, 240, 140) if "brew" not in d else (240, 120, 200), 37)
    for x in (380, 520):
        S.obj(g, Ell(x, 570, 12, 6), (70, 60, 70), 38)
    # candles and the black cat
    for x in (330, 570):
        candle(g, x, 440, 30, w=10)
    cat(g, 760, 560, 1.3, face=-1, eyes=(250, 220, 80) if "cat" not in d else (120, 230, 250))
    if "book" not in d:
        S.obj(g, Poly([(140, 520), (240, 510), (250, 530), (150, 540)]), (200, 60, 70), 39)
        S.obj(g, Poly([(146, 516), (238, 506), (240, 514), (148, 524)]), (250, 244, 226), 40)


L1631_EL = [flame_el("c1", 330, 404, 1.2, 0.1), flame_el("c2", 570, 404, 1.2, 0.5),
            puff_el("bub1", 420, 446, r=9, rise=60, wind=4, col=(170, 250, 180)), puff_el("bub2", 480, 446, r=7, rise=60, wind=-4, phase=0.5, col=(170, 250, 180)),
            sparkle_el("stars", [(400, 120), (420, 210), (510, 200)], col=(255, 250, 220), r=4, speed=0.5)]
L1631_DIFFS = [("potion", 140, 104, 0), ("skull", 220, 194, 0), ("hat", 655, 110, 0), ("brew", 450, 452, 0), ("cat", 790, 520, 0), ("book", 195, 525, 0)]


# =================================================================== Level 1632 ghost ship
def l1632(g, d):
    S.sky(g, [(0, (20, 30, 70)), (360, (70, 100, 140))])
    rnd = random.Random(1632)
    for _ in range(40):
        S.flat(g, Circ(rnd.uniform(0, 900), rnd.uniform(0, 260), rnd.uniform(0.8, 2)), (255, 250, 230))
    moon(g, 720, 110, 60)
    S.water(g, Box(-2, 380, W + 2, H + 2), (50, 80, 130), (20, 40, 80), 1)
    # hull and deck
    S.obj(g, Poly([(-20, 420), (920, 400), (900, 520), (-20, 540)]), (90, 70, 80), 2, "wood")
    S.obj(g, Box(-20, 396, 920, 420), (120, 96, 100), 3, "wood")
    for x in range(0, 900, 50):
        S.obj(g, Box(x, 370, x + 10, 400), (110, 90, 96), 4 + x)
    S.obj(g, Box(-20, 364, 920, 374), (120, 96, 100), 5)
    # masts with tattered sails
    for x, top, w in ((260, 40, 140), (620, 70, 120)):
        S.obj(g, Box(x - 7, top, x + 7, 400), (100, 80, 86), 6 + x, "wood")
        sail = Poly([(x - w, top + 30), (x + w, top + 30), (x + w * 0.8, top + 180), (x + w * 0.4, top + 160), (x + w * 0.1, top + 200),
                     (x - w * 0.3, top + 170), (x - w * 0.8, top + 190)])
        S.obj(g, sail, (200, 220, 230), 7 + x, "fabric")
        S.obj(g, Box(x - w - 10, top + 24, x + w + 10, top + 32), (100, 80, 86), 8 + x)
    S.obj(g, Poly([(261, 30), (320, 40) if "flag" not in d else (290, 34), (261, 50)]), (30, 30, 40), 9)
    if "patch" not in d:
        S.obj(g, Box(200, 120, 250, 160), (160, 190, 200), 10)
    # glowing wheel and lanterns
    S.glow(g, 450, 330, 70, (140, 255, 200), 0.3)
    S.obj(g, Box(444, 330, 456, 400), (100, 80, 86), 11)
    S.flat(g, Diff(Circ(450, 320, 34), Circ(450, 320, 26)), (140, 230, 190))
    for a in range(8):
        S.line(g, 450, 320, 450 + 40 * math.cos(a * math.pi / 4), 320 + 40 * math.sin(a * math.pi / 4), 2.4, (140, 230, 190))
    for i, x in enumerate((120, 800)):
        S.line(g, x, 300, x, 330, 2, (60, 50, 60))
        lantern(g, x, 330, 1.2, lit=not ("lantern" in d and i == 1), col=(170, 255, 200))
    # barrels, a chest and a ghost captain
    barrel(S, g, 130, 410, seed=12)
    barrel(S, g, 760, 400, seed=13)
    if "chest" not in d:
        chest(S, g, 560, 400, 50, open_=True, seed=14)
    gx, gy = 330, 300
    S.obj(g, Union([Ell(gx, gy, 30, 36), Poly([(gx - 30, gy), (gx + 30, gy), (gx + 34, gy + 80), (gx + 18, gy + 70), (gx, gy + 86), (gx - 18, gy + 70), (gx - 34, gy + 80)])]),
          (210, 250, 240), 15, hi=True)
    S.obj(g, Union([Ell(gx, gy - 30, 40, 8), Poly([(gx - 30, gy - 30), (gx, gy - 66), (gx + 30, gy - 30)])]), (40, 36, 50) if "captain" not in d else (170, 50, 60), 16)
    for ex in (-10, 10):
        S.flat(g, Ell(gx + ex, gy, 5, 8), (40, 60, 80))


L1632_EL = [bat_el("bat1", 150, 90, s=12, speed=26, phase=0.1), bat_el("bat2", 180, 110, s=8, speed=26, phase=0.12),
            sparkle_el("wisps", [(380, 260), (500, 280), (620, 250)], col=(180, 255, 220), r=5, speed=0.5),
            E("sea", el(lambda g, m: [S.flat(g, Seg(x, y, x + 40, y, 2), (160, 200, 240)) for x, y in ((80, 560), (300, 580), (520, 556), (740, 584))]),
              anim=dict(bobAmplitude=(20, 0), bobSpeed=0.2))]
L1632_DIFFS = [("flag", 290, 40, 0), ("patch", 225, 140, 0), ("lantern", 800, 340, 0), ("chest", 560, 384, 0), ("captain", 330, 252, 0)]


# =================================================================== Level 1633 cosy inn room
def l1633(g, d):
    S.obj(g, Box(-2, -2, W + 2, 430), (236, 214, 176), 1, line=False)
    S.obj(g, Box(-2, 300, W + 2, 430), (170, 120, 80), 2, "wood")
    S.obj(g, Box(-2, 294, W + 2, 304), (140, 96, 64), 3)
    # window over the village
    S.obj(g, Box(330, 60, 570, 260, 4), (150, 110, 70), 4, "wood")
    g.fill(Box(344, 74, 556, 246), vgrad([(74, (120, 190, 245)), (246, (220, 240, 250))]))
    S.obj(g, cloud_shape(420, 110, 40, 12, 3), (255, 255, 255), 5, "cloud", line=False)
    for x0, w, roof in ((350, 60, (200, 80, 70)), (420, 70, (80, 120, 190)), (500, 50, (110, 160, 90))):
        S.obj(g, Box(x0, 200, x0 + w, 246), (250, 236, 210), 6 + x0, depth=0.3)
        S.obj(g, Poly([(x0 - 6, 202), (x0 + w / 2, 176), (x0 + w + 6, 202)]), roof, 7 + x0, depth=0.3)
    S.flat(g, Union([Box(447, 74, 453, 246), Box(344, 158, 556, 164)]), (150, 110, 70))
    for x0, x1 in ((300, 344), (556, 600)):
        S.obj(g, Poly([(x0, 50), (x1, 50), (x1 - 6, 270), (x0 + 6, 270)]), (90, 140, 200) if not (x0 == 556 and "curtain" in d) else (220, 90, 110), 8 + x0, "fabric")
    S.ground(g, Box(-2, 430, W + 2, H + 2), (170, 120, 80), "wood", 14, line=True)
    # bed (left) with quilt
    S.obj(g, Box(30, 300, 70, 470), (150, 100, 66), 10, "wood")
    S.obj(g, Box(40, 380, 300, 440, 6), (250, 250, 246), 11)
    S.obj(g, Box(60, 410, 300, 470, 6), (210, 90, 100) if "quilt" not in d else (100, 170, 120), 12, "fabric")
    S.obj(g, Ell(90, 384, 40, 16), (250, 250, 250), 13, hi=True)
    S.obj(g, Ell(470, 540, 200, 36), (90, 140, 200), 15)
    # the hero's gear: sword on the wall, shield, backpack, boots
    S.obj(g, Poly([(700, 100), (706, 94), (712, 100), (712, 230), (700, 230)]), (220, 228, 240), 16, hi=True)
    S.obj(g, Box(690, 228, 722, 236), (200, 160, 60), 17)
    S.obj(g, Union([Box(750, 120, 830, 190), Inter(Circ(750, 190, 80), Circ(830, 190, 80)) & Box(750, 190, 830, 250)]),
          (60, 90, 180) if "shield" not in d else (200, 60, 70), 18, hi=True)
    S.flat(g, Circ(790, 180, 16), (250, 210, 80))
    if "pack" not in d:
        S.obj(g, Box(640, 400, 700, 470, 10), (150, 110, 60), 19)
        S.obj(g, Box(646, 420, 694, 440, 4), (130, 90, 50), 20)
    for x in (760, 790):
        S.obj(g, Union([Box(x, 430, x + 18, 470, 3), Box(x, 456, x + 30, 470, 3)]), (120, 80, 50), 21)
    # nightstand with a candle lamp and an apple
    S.obj(g, Box(330, 380, 410, 470, 3), (150, 100, 66), 22, "wood")
    candle(g, 350, 380, 28, w=10)
    if "apple" not in d:
        S.obj(g, Circ(390, 368, 12), (230, 60, 60), 23, hi=True)
    mage(S, g, 560, 590, 150, face=-1, seed=24)


L1633_EL = [flame_el("c", 350, 346, 1.2, 0.1), cloud_el("cl", 500, 100, 30, 10, speed=4, seed=30), bird_el("b", 380, 140, s=6, speed=12)]
L1633_DIFFS = [("curtain", 578, 160, 0), ("quilt", 180, 440, 0), ("shield", 790, 190, 0), ("pack", 670, 434, 0), ("apple", 390, 368, 0)]


# =================================================================== Level 1634 windmill flower fields
def l1634(g, d):
    S.sky(g, [(0, (110, 180, 245)), (300, (220, 238, 252))])
    for x, y, w, h, s in ((160, 80, 80, 22, 1), (620, 60, 100, 26, 2)):
        S.obj(g, cloud_shape(x, y, w, h, s), (255, 255, 255), s, "cloud", line=False)
    S.ground(g, Under(wave(290, 14, 110, 3), -20, W + 20), (140, 200, 110), "grass", 3, line=True)
    # windmill on the hill (sails are an element)
    S.obj(g, Poly([(600, 300), (620, 140), (680, 140), (700, 300)]), (240, 230, 214), 4)
    S.obj(g, Poly([(610, 146), (650, 100), (690, 146)]), (190, 90, 80), 5, "roof")
    S.obj(g, Union([Box(636, 250, 664, 300), Circ(650, 250, 14)]), (140, 96, 60), 6)
    S.obj(g, Box(636, 180, 664, 210, 2), (150, 210, 240) if "window" not in d else (250, 220, 120), 7)
    # striped flower fields in perspective
    cols = [(240, 90, 120), (250, 210, 70), (160, 110, 230), (250, 250, 250), (240, 120, 60)]
    for i in range(10):
        t0, t1 = i / 10, (i + 1) / 10
        y0, y1 = 300 + 300 * t0 ** 1.4, 300 + 300 * t1 ** 1.4
        c = cols[i % 5]
        if "stripe" in d and i == 6:
            c = (90, 200, 220)
        S.obj(g, Box(-20, y0, W + 20, y1 + 1), c, 8 + i, line=False)
        S.flat(g, Box(-20, y1 - 2, W + 20, y1 + 1), shade_of(c, 0.75))
    # picnic blanket, basket, a girl with a kite
    S.obj(g, Poly([(140, 520), (330, 510), (360, 570), (130, 586)]), (240, 240, 240), 20)
    for k in range(4):
        S.flat(g, Inter(Box(140 + k * 52, 500, 166 + k * 52, 600), Poly([(140, 520), (330, 510), (360, 570), (130, 586)])), (230, 70, 70))
    if "basket" not in d:
        S.obj(g, Union([Ell(250, 540, 34, 20), Box(216, 520, 284, 540)]), (200, 150, 80), 21, "wood")
        S.obj(g, Diff(Ell(250, 512, 26, 16), Ell(250, 512, 20, 10)) & Box(220, 494, 280, 514), (170, 120, 60), 22)
    person(S, g, 520, 590, 150, (250, 200, 60), skirt=True, hair_long=True, hair=(150, 90, 50), face=-1, seed=23, arm_up=True)
    S.line(g, 520 - 24, 590 - 146 * 0.98, 820, 220, 1.2, (60, 60, 60))
    S.obj(g, Poly([(820, 180), (850, 220), (820, 270), (790, 220)]), (230, 70, 80) if "kite" not in d else (80, 140, 230), 24)
    for k, (x, y) in enumerate(((820, 290), (812, 316), (826, 342))):
        S.flat(g, Poly([(x - 8, y - 5), (x + 8, y + 5), (x + 8, y - 5), (x - 8, y + 5)]), (250, 210, 70))
    round_tree(S, g, 90, 320, 150, seed=25)
    if "tree" not in d:
        round_tree(S, g, 520, 300, 100, col=(110, 180, 90), seed=26)


L1634_EL = [E("sails", el(lambda g, m: [S.obj(g, Poly([(650, 140), (650 + math.cos(a) * 110 - math.sin(a) * 14, 140 + math.sin(a) * 110 + math.cos(a) * 14),
                                                    (650 + math.cos(a) * 110 + math.sin(a) * 14, 140 + math.sin(a) * 110 - math.cos(a) * 14)]), (250, 246, 236), 30)
                                for a in (0.4, 0.4 + math.pi / 2, 0.4 + math.pi, 0.4 + 1.5 * math.pi)]), pivot=(650, 140), anim=dict(rotateSpeed=-30)),
            cloud_el("cl", 380, 110, 50, 16, speed=6, seed=31), bird_el("b", 300, 80, speed=20),
            E("butterfly", el(lambda g, m: S.obj(g, Union([Ell(420, 400, 8, 6), Ell(432, 400, 8, 6)]), (250, 160, 60), 1)), pivot=(426, 400),
              anim=dict(stretch=(0.6, 0), scaleSpeed=3.0, bobAmplitude=(40, 20), bobSpeed=0.15))]
L1634_DIFFS = [("window", 650, 195, 0), ("stripe", 450, 510, 0), ("basket", 250, 526, 0), ("kite", 820, 225, 0), ("tree", 520, 240, 0)]


# =================================================================== Level 1635 treehouse
def l1635(g, d):
    S.sky(g, [(0, (120, 190, 240)), (400, (220, 240, 230))])
    for x in range(-20, 920, 70):
        round_tree(S, g, x, 420, 200 + (x * 7 % 40), col=(90, 160, 100), seed=x, depth=0.5)
    S.ground(g, Box(-2, 420, W + 2, H + 2), (120, 190, 90), "grass", 1, line=True)
    # the big oak trunk and canopy
    S.obj(g, Poly([(380, 600), (420, 300), (480, 300), (530, 600)]), (150, 100, 66), 2, "wood")
    S.obj(g, Union([Circ(450, 40, 200), Circ(250, 90, 120), Circ(660, 90, 130)]), (80, 160, 80), 3, "foliage", hi=True)
    # platform and hut
    S.obj(g, Box(260, 320, 640, 340), (170, 120, 76), 4, "wood")
    S.obj(g, Box(320, 200, 560, 320), (210, 160, 100), 5, "wood")
    S.obj(g, Poly([(300, 204), (440, 130), (580, 204)]), (200, 80, 70) if "roof" not in d else (80, 120, 190), 6, "roof")
    S.obj(g, Union([Box(420, 250, 466, 320), Circ(443, 250, 23)]), (120, 80, 50), 7, "wood")
    S.obj(g, Box(340, 230, 390, 270, 3), (150, 210, 240), 8, hi=True)
    if "flag" not in d:
        S.line(g, 560, 204, 560, 150, 2, (110, 80, 50))
        S.obj(g, Poly([(561, 150), (600, 160), (561, 170)]), (250, 210, 60), 9)
    for x in range(270, 640, 30):
        S.obj(g, Box(x, 296, x + 6, 322), (190, 140, 90), 10)
    S.flat(g, Box(260, 296, 640, 302), (190, 140, 90))
    # rope ladder and swing
    for x in (290, 320):
        S.line(g, x, 340, x, 560, 2, (200, 170, 110))
    for k in range(7):
        if "rung" in d and k == 3:
            continue
        S.obj(g, Box(286, 360 + k * 30, 324, 366 + k * 30, 2), (170, 120, 76), 11)
    for x in (600, 660):
        S.line(g, x, 340, x, 500, 1.6, (200, 170, 110))
    S.obj(g, Box(590, 500, 670, 510, 2), (170, 120, 76) if "swing" not in d else (220, 80, 80), 12)
    # lanterns strung on the platform rail
    for i, x in enumerate((360, 450, 540)):
        S.line(g, x, 302, x, 316, 1, (60, 50, 50))
        lantern(g, x, 314, 0.8, lit=True)
    # kids' treasures: a telescope, a toy chest, a ball
    S.obj(g, Seg(600, 286, 640, 266, 6, 4), (200, 160, 70), 13, hi=True)
    if "chest" not in d:
        chest(S, g, 740, 560, 54, seed=14)
    S.obj(g, Circ(200, 572, 20), (230, 70, 70), 15, hi=True)
    S.flat(g, Seg(186, 560, 214, 584, 3), (250, 250, 250))
    person(S, g, 400, 320, 100, (90, 160, 220), face=1, seed=16)
    person(S, g, 820, 590, 140, (250, 140, 60), face=-1, seed=17, hat=(200, 60, 60))


L1635_EL = [bird_el("b1", 700, 120, s=7, speed=-16),
            E("leaves", el(lambda g, m: [S.obj(g, Ell(x, y, 6, 3), (110, 180, 90), 1) for x, y in ((300, 200), (560, 160), (700, 230))]),
              anim=dict(driftVelocity=(10, -60), driftLength=200, driftFade=True, swingAngle=20, swingSpeed=0.6)),
            sparkle_el("sun", [(150, 260), (760, 300)], col=(255, 250, 210), r=5, speed=0.4)]
L1635_DIFFS = [("roof", 440, 160, 0), ("flag", 580, 160, 0), ("rung", 305, 453, 0), ("swing", 630, 505, 0), ("chest", 740, 540, 0)]


# =================================================================== Level 1636 pumpkin patch at night
def l1636(g, d):
    S.sky(g, [(0, (30, 26, 70)), (330, (120, 80, 120))])
    moon(g, 650, 130, 80, col=(255, 220, 140))
    for x in range(-20, 920, 50):
        S.flat(g, Poly([(x - 30, 330), (x, 280 - (x * 13 % 30)), (x + 30, 330)]), (50, 40, 70))
    S.ground(g, Box(-2, 320, W + 2, H + 2), (70, 60, 70), "dirt", 1, line=True)
    toon_tree(g, 120, 360, 300, col=(40, 34, 50), lean=0.1, seed=2)
    # fence
    for x in range(200, 900, 50):
        S.obj(g, Box(x, 300, x + 14, 360, 2), (130, 100, 90), 3 + x)
    S.obj(g, Box(190, 318, 910, 326), (130, 100, 90), 4)
    # scarecrow
    sx, sb = 700, 430
    S.obj(g, Union([Box(sx - 4, sb - 200, sx + 4, sb), Box(sx - 70, sb - 160, sx + 70, sb - 152)]), (130, 100, 70), 5, "wood")
    S.obj(g, Poly([(sx - 40, sb - 164), (sx + 40, sb - 164), (sx + 30, sb - 80), (sx - 30, sb - 80)]), (200, 90, 70) if "shirt" not in d else (80, 120, 190), 6, "fabric")
    S.obj(g, Circ(sx, sb - 186, 22), (240, 210, 150), 7)
    S.obj(g, Union([Ell(sx, sb - 202, 40, 8), Poly([(sx - 20, sb - 202), (sx, sb - 240), (sx + 20, sb - 202)])]), (110, 80, 50), 8)
    for ex in (-8, 8):
        S.flat(g, Seg(sx + ex - 4, sb - 190, sx + ex + 4, sb - 182, 1.6), INK)
        S.flat(g, Seg(sx + ex - 4, sb - 182, sx + ex + 4, sb - 190, 1.6), INK)
    # pumpkins (some carved and glowing)
    for i, (x, base, r, face) in enumerate(((180, 500, 40, True), (320, 540, 54, True), (470, 500, 36, False), (560, 570, 46, True),
                                           (820, 540, 50, False), (90, 590, 34, False))):
        if "pumpkin" in d and i == 2:
            continue
        pumpkin(g, x, base, r, face=face and not ("glow" in d and i == 3), seed=10 + i)
    # crows on the fence and a lantern post
    if "crow" not in d:
        S.obj(g, Union([Ell(400, 290, 16, 11), Circ(412, 278, 8), Poly([(418, 276), (430, 280), (418, 284)])]), (30, 26, 40), 20)
    S.obj(g, Union([Ell(800, 290, 16, 11), Circ(788, 278, 8), Poly([(782, 276), (770, 280), (782, 284)])]), (30, 26, 40), 21)
    S.obj(g, Box(260, 380, 266, 470), (60, 50, 60), 22)
    lantern(g, 263, 366, 1.0, lit=True)
    cat(g, 640, 600, 1.0, face=1)


L1636_EL = [bat_el("bat1", 560, 80, s=12, speed=-24, phase=0.2), bat_el("bat2", 600, 100, s=8, speed=-24, phase=0.24),
            sparkle_el("fireflies", [(240, 420), (420, 460), (660, 480), (760, 420)], col=(255, 240, 150), r=4, speed=0.6),
            E("fog", el(lambda g, m: g.fill(Box(-60, 330, W + 60, 380, 25), (200, 180, 220), alpha=0.25, feather=20)), anim=dict(bobAmplitude=(40, 0), bobSpeed=0.05))]
L1636_DIFFS = [("shirt", 700, 310, 0), ("pumpkin", 470, 470, 0), ("glow", 560, 540, 0), ("crow", 408, 284, 0)]


LEVELS = [
    ("Level1631", "卡通·魔女小屋", make(l1631), L1631_EL, L1631_DIFFS, 60, OPTS),
    ("Level1632", "卡通·幽灵船", make(l1632), L1632_EL, L1632_DIFFS, 60, OPTS),
    ("Level1633", "卡通·旅店客房", make(l1633), L1633_EL, L1633_DIFFS, 60, OPTS),
    ("Level1634", "卡通·花田风车", make(l1634), L1634_EL, L1634_DIFFS, 60, OPTS),
    ("Level1635", "卡通·林间树屋", make(l1635), L1635_EL, L1635_DIFFS, 60, OPTS),
    ("Level1636", "卡通·南瓜田夜", make(l1636), L1636_EL, L1636_DIFFS, 60, OPTS),
]
