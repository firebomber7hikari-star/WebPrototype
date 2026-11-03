# -*- coding: utf-8 -*-
"""Toon-render (cel-shaded) levels, set 4 - assorted themes, original designs, no text:
  Level1649 卡通·海底小镇 - an undersea village: shell houses, coral, fish, a little submarine, bubbles
  Level1650 卡通·月面基地 - a moon base: domes, a rover, astronauts, the Earth in a starry sky
  Level1651 卡通·恐龙山谷 - a dinosaur valley: smoking volcano, long-neck and horned dinos, palms, a nest
  Level1652 卡通·面包房   - a bakery: bread shelves, cake counter, oven, baker, a customer
  Level1653 卡通·云上城堡 - a castle on the clouds: rainbow, hot-air balloons, winged horse, birds
  Level1654 卡通·灯笼夜市 - a night market under lanterns: food stalls, goldfish game, crowd
  Level1655 卡通·火车站台 - a little country station: steam train, clock, benches, luggage, flowers
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Poly, Rough, Seg, Under, Union, el, fbm1, mixc, vgrad
from levels_remake import ToonS
from toon import INK, bird_el, cel, cloud_el, cloud_shape, puff_el, shade_of, tint_of, toon_post
from styled_kit import (barrel, bush, castle, chest, crate, crystal, lamp_post, palm, person, potion, round_tree, sign_board,
                        sparkle_el, tower)
from levels_souls_toon import lantern, moon
from levels_toon3 import cat

S = ToonS()
OPTS = dict(post=toon_post, anim_seconds=12.0, frames=60)


def make(scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, d)
        S.finish(g)
        g.commit()
    return bg


def wave(y, amp, period, seed):
    return lambda x: y + amp * np.sin(x / period + seed) + (fbm1(x, 60, 2, seed) - 0.5) * amp


def fish(g, x, y, s, col, face=1, seed=0, stripe=None):
    S.obj(g, Union([Ell(x, y, 22 * s, 13 * s), Poly([(x - face * 18 * s, y), (x - face * 36 * s, y - 13 * s), (x - face * 36 * s, y + 13 * s)])]), col, seed, hi=True)
    if stripe:
        g.fill(Inter(Box(x - 4 * s, y - 14 * s, x + 4 * s, y + 14 * s), Ell(x, y, 22 * s, 13 * s)), stripe)
    g.fill(Circ(x + face * 12 * s, y - 3 * s, 3 * s), (30, 30, 50))


def bubble_el(eid, pts, phase=0.0):
    return E(eid, el(lambda g, m: [g.fill(Circ(x, y, r) - Circ(x, y, r * 0.75), (230, 250, 255)) for x, y, r in pts]), daynight="untinted",
             anim=dict(driftVelocity=(0, 70), driftLength=220, driftFade=True, phase=phase))


# =================================================================== Level 1649 undersea village
def l1649(g, d):
    S.sky(g, [(0, (60, 170, 220)), (600, (20, 70, 140))])
    for x in (150, 450, 750):
        g.fill(Poly([(x - 40, -2), (x + 40, -2), (x + 140, 600), (x - 60, 600)]), (180, 230, 250), alpha=0.12)
    S.ground(g, Under(wave(470, 14, 90, 2), -20, W + 20), (230, 210, 160), "dirt", 1, line=True)
    # shell and coral houses
    for i, (x, base, col, roof) in enumerate(((150, 470, (250, 190, 170), (240, 120, 120)), (420, 460, (250, 230, 170), (90, 170, 200)), (700, 470, (210, 190, 240), (240, 160, 80)))):
        S.obj(g, Union([Ell(x, base - 60, 70, 70), Box(x - 70, base - 60, x + 70, base)]), col, 10 + i, hi=True)
        for k in range(5):
            g.fill(Seg(x, base - 130, x - 60 + k * 30, base - 70, 2), shade_of(col, 0.85))
        S.obj(g, Poly([(x - 40, base - 120), (x, base - 175), (x + 40, base - 120)]), roof if not ("roof" in d and i == 1) else (120, 200, 120), 20 + i)
        S.obj(g, Union([Box(x - 16, base - 44, x + 16, base), Circ(x, base - 44, 16)]), (140, 90, 70), 30 + i)
        S.obj(g, Circ(x + 40, base - 70, 14), (170, 220, 240), 40 + i, hi=True)
    # corals and seaweed
    for i, (x, col) in enumerate(((40, (250, 110, 130)), (290, (250, 170, 80)), (560, (250, 110, 130)), (860, (170, 120, 230)))):
        if "coral" in d and i == 2:
            col = (110, 220, 160)
        parts = [Seg(x, 520, x + dx, 520 - h, 8, 5) for dx, h in ((-20, 60), (0, 80), (20, 56), (-8, 44))]
        S.obj(g, Union(parts), col, 50 + i)
    for x in (230, 520, 820):
        S.obj(g, Union([Seg(x + math.sin(k) * 8, 560 - k * 24, x + math.sin(k + 1) * 8, 560 - (k + 1) * 24, 6) for k in range(6)]), (80, 170, 100), 60 + x)
    # starfish, clam with a pearl, treasure chest
    S.obj(g, Poly([(340 + math.cos(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9), 560 + math.sin(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9)) for k in range(10)]),
          (250, 150, 80) if "star" not in d else (250, 220, 80), 70)
    S.obj(g, Union([Ell(620, 560, 34, 14)]), (230, 200, 220), 71)
    if "pearl" not in d:
        S.obj(g, Circ(620, 552, 9), (250, 250, 255), 72, hi=True)
    chest(S, g, 800, 580, 56, open_=True, seed=73)
    # a little submarine
    S.obj(g, Union([Ell(560, 180, 70, 32), Box(540, 130, 580, 152, 6), Seg(560, 130, 560, 110, 3)]), (250, 210, 70) if "sub" not in d else (240, 120, 100), 74, hi=True)
    for x in (530, 560, 590):
        S.obj(g, Circ(x, 180, 9), (170, 220, 250), 75, hi=True)
    S.obj(g, Union([Poly([(492, 170), (470, 150), (470, 210), (492, 190)])]), (220, 100, 80), 76)


L1649_EL = [E("fish1", el(lambda g, m: fish(g, 200, 130, 1.0, (250, 150, 60), stripe=(255, 255, 255))), pivot=(200, 130), anim=dict(bobAmplitude=(60, 10), bobSpeed=0.08)),
            E("fish2", el(lambda g, m: fish(g, 760, 260, 0.8, (90, 140, 240), face=-1)), pivot=(760, 260), anim=dict(bobAmplitude=(50, 12), bobSpeed=0.07, phase=0.5)),
            bubble_el("bub1", [(150, 380, 6), (170, 340, 4), (700, 380, 5)]), bubble_el("bub2", [(420, 360, 5), (440, 320, 3)], phase=0.5),
            E("prop", el(lambda g, m: S.obj(g, Union([Ell(470, 168, 4, 16), Ell(470, 192, 4, 16)]), (200, 200, 210), 1, line=False)), pivot=(470, 180),
              anim=dict(stretch=(0, 0.6), scaleSpeed=3.0))]
L1649_DIFFS = [("roof", 420, 312, 0), ("coral", 560, 470, 0), ("star", 340, 560, 0), ("pearl", 620, 552, 0), ("sub", 560, 170, 0)]


# =================================================================== Level 1650 moon base
def l1650(g, d):
    S.sky(g, [(0, (10, 14, 40)), (420, (40, 40, 80))])
    rnd = random.Random(1650)
    for _ in range(70):
        g.fill(Circ(rnd.uniform(0, 900), rnd.uniform(0, 380), rnd.uniform(0.8, 2.2)), (255, 255, 240))
    S.obj(g, Circ(720, 110, 60), (70, 140, 230), 1, hi=True)
    S.obj(g, Union([Rough(Ell(700, 90, 26, 18), 4, 6, 1), Rough(Ell(740, 130, 20, 14), 4, 6, 2)]), (100, 190, 110), 2, line=False)
    S.ground(g, Under(wave(390, 16, 120, 3), -20, W + 20), (200, 200, 210), "dirt", 3, line=True)
    for x, y, r in ((100, 470, 40), (420, 520, 30), (760, 450, 26), (300, 430, 18)):
        S.obj(g, Ell(x, y, r, r * 0.35), (170, 170, 184), 4 + x, line=False)
        S.obj(g, Ell(x, y - 3, r * 0.8, r * 0.25), (150, 150, 164), 5 + x, line=False)
    # domes and a tower
    for i, (x, r) in enumerate(((180, 90), (420, 70))):
        S.obj(g, Inter(Ell(x, 400, r, r), Box(x - r, 300, x + r, 400)), (220, 230, 240), 10 + i, hi=True)
        for k in range(3):
            S.obj(g, Circ(x - r * 0.5 + k * r * 0.5, 370, 13), (120, 200, 250) if not ("window" in d and i == 0 and k == 1) else (250, 210, 90), 12 + i * 3 + k)
    S.obj(g, Box(380, 330 - 120, 400, 330), (200, 210, 220), 20)
    S.obj(g, Ell(390, 206, 30, 10), (220, 230, 240), 21)
    if "dish" not in d:
        S.obj(g, Union([Ell(560, 300, 30, 18), Seg(560, 318, 560, 400, 4)]), (230, 230, 240), 22)
    # flag on a pole
    S.line(g, 300, 390, 300, 300, 2, (200, 200, 210))
    S.obj(g, Box(302, 300, 350, 330), (230, 80, 90) if "flag" not in d else (90, 170, 120), 23)
    # rover with antenna
    S.obj(g, Box(600, 420, 720, 460, 8), (250, 200, 70), 24)
    for wx in (620, 660, 700):
        S.obj(g, Circ(wx, 466, 14), (70, 70, 80), 25)
    S.line(g, 700, 420, 712, 392, 2, (90, 90, 100))
    S.obj(g, Circ(712, 386, 11), (230, 60, 60) if "light" not in d else (60, 200, 240), 26)
    # astronauts
    for i, (x, base) in enumerate(((240, 560), (820, 540))):
        S.obj(g, Union([Box(x - 22, base - 70, x + 22, base - 20, 10), Box(x - 18, base - 20, x - 4, base, 4), Box(x + 4, base - 20, x + 18, base, 4)]), (240, 240, 245), 30 + i)
        S.obj(g, Circ(x, base - 92, 24), (240, 240, 245), 32 + i)
        S.obj(g, Ell(x + 4, base - 92, 16, 13), (60, 80, 140), 34 + i, hi=True)
        S.obj(g, Box(x - 34, base - 66, x - 20, base - 30, 4), (230, 120, 80) if not ("pack" in d and i == 1) else (90, 150, 220), 36 + i)


L1650_EL = [sparkle_el("tw", [(100, 60), (300, 120), (520, 40), (840, 260)], col=(255, 255, 230), r=4, speed=0.6),
            E("rocket", el(lambda g, m: S.obj(g, Union([Ell(120, 180, 10, 26), Poly([(110, 196), (102, 212), (118, 202)]), Poly([(130, 196), (138, 212), (122, 202)])]), (240, 240, 250), 1)),
              pivot=(120, 180), anim=dict(driftVelocity=(10, 50), driftLength=260, driftFade=True)),
            E("bob", el(lambda g, m: S.obj(g, Circ(560, 300, 4), (255, 80, 80), 2, line=False)), daynight="untinted", anim=dict(blinkInterval=1.2, blinkDuration=0.4))]
L1650_DIFFS = [("window", 180, 370, 0), ("dish", 560, 320, 0), ("flag", 326, 314, 0), ("light", 712, 390, 0), ("pack", 793, 492, 0)]


# =================================================================== Level 1651 dinosaur valley
def l1651(g, d):
    S.sky(g, [(0, (250, 200, 140)), (300, (250, 230, 190))])
    S.obj(g, Poly([(480, 300), (620, 100), (660, 100), (820, 300)]), (150, 110, 100), 1)
    S.obj(g, Poly([(612, 112), (640, 90), (668, 112), (650, 140), (630, 140)]), (240, 110, 60), 2, line=False)
    S.ground(g, Under(wave(300, 10, 100, 3), -20, W + 20), (140, 190, 90), "grass", 3, line=True)
    S.water(g, Ell(450, 470, 160, 34), (110, 190, 220), (70, 150, 200), 4)
    for x, h, lean in ((60, 260, 0.1), (840, 280, -0.12), (300, 200, 0.05)):
        palm(S, g, x, 420 if x != 300 else 330, h, lean=lean, seed=x)
    # long-neck dino
    S.obj(g, Union([Ell(220, 420, 90, 46), Seg(280, 400, 340, 230, 16, 10), Ell(352, 224, 22, 12), Seg(140, 420, 60, 450, 16, 4),
                    Box(170, 440, 194, 500, 6), Box(240, 440, 264, 500, 6)]), (110, 180, 140), 10, hi=True)
    g.fill(Circ(360, 220, 3), INK)
    for k in range(5):
        S.obj(g, Poly([(180 + k * 22, 376), (190 + k * 22, 360), (200 + k * 22, 376)]), (250, 200, 80) if "spikes" not in d else (230, 90, 80), 11 + k)
    # horned dino
    hx = 640
    S.obj(g, Union([Ell(hx, 450, 70, 36), Ell(hx + 70, 430, 30, 24), Box(hx - 40, 470, hx - 20, 510, 6), Box(hx + 20, 470, hx + 40, 510, 6),
                    Poly([(hx - 60, 446), (hx - 110, 460), (hx - 60, 466)])]), (230, 150, 100), 20, hi=True)
    S.obj(g, Ell(hx + 56, 410, 24, 30), (250, 210, 150), 21)
    for dx in (78, 94):
        S.obj(g, Poly([(hx + dx - 4, 418), (hx + dx + 10, 390), (hx + dx + 4, 420)]), (250, 246, 230), 22)
    if "horn" not in d:
        S.obj(g, Poly([(hx + 94, 432), (hx + 130, 414), (hx + 98, 450)]), (250, 246, 230), 23)
    g.fill(Circ(hx + 84, 424, 3), INK)
    # nest with eggs, pterosaur on a rock
    S.obj(g, Ell(470, 560, 60, 16), (170, 130, 80), 30)
    for i, x in enumerate((448, 470, 492)):
        if "egg" in d and i == 2:
            continue
        S.obj(g, Ell(x, 548, 12, 16), (250, 240, 210), 31 + i, hi=True)
        g.fill(Circ(x - 3, 544, 2.5), (150, 200, 120))
    S.obj(g, Ell(820, 500, 60, 30), (170, 160, 150), 34)
    S.obj(g, Union([Ell(820, 450, 16, 22), Poly([(808, 440), (760, 430), (800, 460)]), Poly([(832, 440), (880, 430), (840, 460)]), Poly([(820, 430), (846, 418), (822, 440)])]),
          (200, 110, 120) if "ptero" not in d else (110, 140, 200), 35)
    bush(S, g, 120, 560, 40, (90, 150, 80), seed=36, flowers=(250, 120, 150) if "bush" not in d else None)


L1651_EL = [puff_el("smk%d" % i, 640, 96, r=14, rise=90, wind=8, phase=i / 3, col=(160, 150, 150)) for i in range(3)] + \
           [bird_el("p1", 300, 80, s=12, speed=20), sparkle_el("water", [(400, 470), (500, 480)], r=5, speed=0.5)]
L1651_DIFFS = [("spikes", 224, 368, 0), ("horn", 746, 434, 0), ("egg", 492, 548, 0), ("ptero", 820, 444, 0), ("bush", 120, 530, 0)]


# =================================================================== Level 1652 bakery
def l1652(g, d):
    S.obj(g, Box(-2, -2, W + 2, 430), (250, 230, 200), 1, line=False)
    for x in range(0, 900, 40):
        g.fill(Box(x, 300, x + 20, 430), (240, 216, 186))
    S.obj(g, Box(-2, 296, W + 2, 304), (200, 140, 100), 2)
    # bread shelves
    rnd = random.Random(1652)
    for y in (90, 180, 270):
        S.obj(g, Box(30, y, 380, y + 10), (170, 110, 70), 3 + y, "wood")
        for k in range(6):
            x = 50 + k * 56
            kind = (k + y // 90) % 3
            if "bread" in d and y == 180 and k == 2:
                continue
            if kind == 0:
                S.obj(g, Ell(x + 18, y - 14, 24, 14), (220, 160, 90), 4)
                for j in range(3):
                    g.fill(Seg(x + 6 + j * 10, y - 22, x + 12 + j * 10, y - 8, 1.6), (180, 110, 60))
            elif kind == 1:
                S.obj(g, Union([Ell(x + 18, y - 12, 22, 12), Ell(x + 18, y - 22, 16, 10)]), (230, 180, 110), 5)
            else:
                S.obj(g, Seg(x, y - 8, x + 40, y - 16, 7), (210, 150, 80), 6)
    # oven (right)
    S.obj(g, Union([Box(640, 120, 880, 430), Inter(Ell(760, 120, 120, 70), Box(640, 40, 880, 120))]), (200, 120, 90), 10, "brick")
    S.obj(g, Union([Box(700, 240, 820, 330), Inter(Circ(760, 240, 60), Box(700, 180, 820, 240))]), (60, 40, 40), 11)
    g.glow(760, 300, 90, (255, 160, 70), 0.4)
    S.obj(g, Ell(760, 320, 50, 12), (255, 170, 80), 12, line=False)
    S.ground(g, Box(-2, 430, W + 2, H + 2), (230, 200, 160), "plain", 22, line=True)
    person(S, g, 450, 430, 170, (250, 250, 250), pants=(70, 70, 90), face=1, seed=30, hat=(250, 250, 250))
    # counter with a cake stand, cookies and a till
    S.obj(g, Box(260, 380, 640, 460, 4), (240, 200, 160), 13, "wood")
    S.obj(g, Box(250, 370, 650, 384, 3), (250, 246, 236), 14)
    S.obj(g, Union([Box(330, 320, 410, 370, 4)]), (250, 220, 230), 15)
    S.obj(g, Box(330, 320, 410, 334, 4), (240, 120, 150) if "cake" not in d else (140, 200, 120), 16)
    g.fill(Circ(370, 314, 6), (220, 40, 50))
    for k in range(4):
        S.obj(g, Circ(450 + k * 26, 362, 10), (210, 160, 100), 17 + k)
    S.obj(g, Box(550, 330, 620, 370, 4), (120, 140, 160) if "till" not in d else (230, 190, 80), 21)

    for x in range(0, 900, 60):
        for y in (470, 530):
            g.fill(Box(x + (y % 120), y, x + 30 + (y % 120), y + 30), (210, 180, 140), alpha=0.6)
    # baker and customer
    person(S, g, 160, 590, 170, (90, 150, 210), skirt=True, hair_long=True, hair=(150, 90, 50), face=1, seed=31, bag=(220, 90, 90) if "bag" not in d else (90, 170, 120), arm_up=False)
    if "basket" not in d:
        S.obj(g, Union([Ell(240, 588, 26, 14), Box(214, 566, 266, 588)]), (210, 160, 90), 32, "wood")
    cat(g, 820, 580, 1.0, col=(240, 170, 90), face=-1)


L1652_EL = [puff_el("st%d" % i, 760, 230, r=10, rise=60, wind=4, phase=i / 3) for i in range(3)] + \
           [sparkle_el("sugar", [(350, 320), (480, 356)], col=(255, 255, 255), r=4, speed=0.6)]
L1652_DIFFS = [("bread", 160, 166, 0), ("cake", 370, 327, 0), ("till", 585, 350, 0), ("bag", 130, 480, 0), ("basket", 240, 578, 0)]


# =================================================================== Level 1653 castle on the clouds
def l1653(g, d):
    S.sky(g, [(0, (110, 170, 250)), (600, (230, 220, 250))])
    # rainbow
    for k, c in enumerate(((240, 90, 90), (250, 170, 70), (250, 230, 90), (110, 200, 120), (90, 150, 230), (150, 110, 220))):
        if "rainbow" in d and k == 3:
            c = (250, 250, 250)
        g.fill(Inter(Ell(250, 420, 260 - k * 14, 230 - k * 14) - Ell(250, 420, 246 - k * 14, 216 - k * 14), Box(-20, 0, 520, 420)), c, alpha=0.8)
    # cloud island with the castle
    S.obj(g, cloud_shape(560, 420, 300, 70, 3), (255, 255, 255), 1, "cloud")
    castle(S, g, 560, 400, 300, 260, (240, 230, 250), (200, 110, 170), seed=2, flags=((250, 210, 70), (250, 210, 70) if "flag" not in d else None))
    for x, y, r in ((560, 300, 12),):
        S.obj(g, Circ(x, y, r), (250, 220, 100) if "window" not in d else (120, 200, 240), 3, hi=True)
    # small clouds and floating islands
    for x, y, w, h, s in ((100, 120, 70, 20, 4), (830, 220, 60, 18, 5), (180, 520, 120, 30, 6), (820, 520, 110, 30, 7)):
        S.obj(g, cloud_shape(x, y, w, h, s), (255, 255, 255), s, "cloud")
    # hot-air balloons
    for i, (x, y, c) in enumerate(((150, 260, (240, 120, 90)), (820, 120, (120, 180, 230)))):
        if "balloon" in d and i == 1:
            c = (180, 120, 220)
        S.obj(g, Union([Circ(x, y, 34), Poly([(x - 28, y + 18), (x + 28, y + 18), (x + 10, y + 46), (x - 10, y + 46)])]), c, 10 + i, hi=True)
        S.obj(g, Box(x - 10, y + 54, x + 10, y + 68, 3), (170, 120, 70), 12 + i)
        g.fill(Union([Seg(x - 8, y + 46, x - 8, y + 54, 1), Seg(x + 8, y + 46, x + 8, y + 54, 1)]), INK)
    # winged horse on a cloud
    hx, hy = 220, 470
    S.obj(g, Union([Ell(hx, hy, 40, 20), Seg(hx + 30, hy - 10, hx + 50, hy - 40, 9), Ell(hx + 58, hy - 44, 16, 10), Box(hx - 26, hy + 10, hx - 18, hy + 40, 3),
                    Box(hx + 18, hy + 10, hx + 26, hy + 40, 3)]), (250, 250, 252), 20, hi=True)
    S.obj(g, Union([Poly([(hx - 10, hy - 14), (hx - 40, hy - 70), (hx + 10, hy - 30)])]), (220, 230, 250) if "wing" not in d else (250, 210, 120), 21)
    S.obj(g, Seg(hx + 40, hy - 40, hx + 30, hy - 20, 4), (250, 200, 220), 22)


L1653_EL = [cloud_el("c1", 400, 80, 60, 16, speed=6, seed=40), bird_el("b1", 700, 300, s=8, speed=-18), bird_el("b2", 730, 320, s=6, speed=-18),
            sparkle_el("sp", [(420, 160), (680, 200), (300, 350)], col=(255, 255, 240), r=5, speed=0.6)]
L1653_DIFFS = [("rainbow", 30, 220, 0), ("flag", 690, 80, 0), ("window", 560, 300, 0), ("balloon", 820, 140, 0), ("wing", 200, 430, 0)]


# =================================================================== Level 1654 lantern night market
def l1654(g, d):
    S.sky(g, [(0, (30, 30, 70)), (300, (90, 60, 110))])
    for x0, w, h in ((-20, 200, 240), (180, 160, 200), (520, 180, 260), (700, 220, 220)):
        S.obj(g, Union([Box(x0, 300 - h, x0 + w, 300), Poly([(x0 - 10, 300 - h), (x0 + w / 2, 300 - h - 40), (x0 + w + 10, 300 - h)])]), (60, 50, 80), x0, depth=0.4)
    S.ground(g, Box(-2, 300, W + 2, H + 2), (110, 90, 100), "plain", 1, line=True)
    # lantern strings
    for row, y in enumerate((60, 120)):
        g.fill(Seg(-10, y, 910, y + 20, 1.2), INK)
        for k in range(9):
            x = 40 + k * 100 + row * 50
            if "lantern" in d and row == 1 and k == 4:
                continue
            col = (240, 80, 70) if (k + row) % 2 else (250, 180, 70)
            g.glow(x, y + 30, 40, col, 0.3)
            S.obj(g, Ell(x, y + 30, 18, 22), col, 2 + k)
            g.fill(Union([Box(x - 10, y + 6, x + 10, y + 10), Box(x - 10, y + 50, x + 10, y + 54)]), (60, 40, 40))
    # stalls
    for i, (x0, col, stripe) in enumerate(((40, (230, 90, 80), (250, 240, 220)), (320, (80, 140, 200), (250, 240, 220)), (600, (250, 190, 70), (230, 90, 80)))):
        S.obj(g, Box(x0, 380, x0 + 240, 470, 3), (170, 110, 70), 20 + i, "wood")
        aw = Poly([(x0 - 10, 300), (x0 + 250, 300), (x0 + 240, 340), (x0, 340)])
        S.obj(g, aw, col if not ("awning" in d and i == 1) else (120, 190, 120), 23 + i)
        for k in range(6):
            g.fill(Inter(Box(x0 + k * 42, 290, x0 + k * 42 + 21, 350), aw), stripe, alpha=0.8)
        for x in (x0 + 4, x0 + 230):
            S.obj(g, Box(x, 340, x + 6, 380), (120, 80, 50), 26)
    # goods: skewers, goldfish tank, masks
    for k in range(5):
        S.obj(g, Seg(80 + k * 30, 380, 86 + k * 30, 340, 2), (200, 160, 100), 30 + k)
        S.obj(g, Ell(83 + k * 30, 352, 7, 9), (180, 90, 60), 35 + k)
    S.obj(g, Box(350, 340, 530, 380, 4), (150, 210, 240), 40)
    for k, x in enumerate((380, 430, 480)):
        if "fish" in d and k == 1:
            continue
        S.obj(g, Union([Ell(x, 360, 10, 6), Poly([(x - 8, 360), (x - 16, 354), (x - 16, 366)])]), (250, 120, 60), 41 + k)
    for k, x in enumerate((640, 700, 760)):
        S.obj(g, Ell(x, 360, 20, 24), [(250, 250, 250), (250, 200, 210), (200, 230, 250)][k] if not ("mask" in d and k == 2) else (250, 220, 90), 44 + k, hi=True)
        g.fill(Union([Ell(x - 7, 356, 3, 4), Ell(x + 7, 356, 3, 4)]), INK)
    # crowd
    for i, (x, c, sk) in enumerate(((180, (240, 150, 170), True), (420, (90, 140, 210), False), (560, (250, 210, 120), True), (780, (130, 190, 140), False))):
        person(S, g, x, 600, 170, c, skirt=sk, hair_long=sk, face=1 if i % 2 else -1, seed=50 + i)


L1654_EL = [E("glow", el(lambda g, m: [g.glow(40 + k * 100, 90, 30, (255, 200, 120), 0.25) for k in range(9)]), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.0)),
            sparkle_el("tank", [(400, 350), (470, 360)], col=(255, 255, 255), r=4, speed=0.7),
            E("smoke", el(lambda g, m: g.glow(130, 330, 20, (220, 220, 230), 0.4)), anim=dict(driftVelocity=(4, 40), driftLength=80, driftFade=True))]
L1654_DIFFS = [("lantern", 490, 150, 0), ("awning", 440, 320, 0), ("fish", 430, 360, 0), ("mask", 760, 360, 0)]


# =================================================================== Level 1655 country station
def l1655(g, d):
    S.sky(g, [(0, (130, 190, 240)), (300, (230, 240, 250))])
    S.obj(g, cloud_shape(200, 80, 80, 22, 1), (255, 255, 255), 1, "cloud", line=False)
    S.ground(g, Under(wave(260, 12, 100, 4), -20, W + 20), (140, 200, 110), "grass", 2, line=True)
    for x in (80, 760, 860):
        round_tree(S, g, x, 290, 120, seed=x, depth=0.3)
    # station building with a clock and roof
    S.obj(g, Box(80, 160, 420, 360), (240, 220, 190), 3)
    S.obj(g, Poly([(60, 164), (250, 90), (440, 164)]), (180, 80, 70), 4, "roof")
    S.obj(g, Circ(250, 140, 26), (250, 250, 246) if "clock" not in d else (250, 220, 120), 5)
    a = -math.pi / 2 + 0.9
    g.fill(Union([Seg(250, 140, 250 + math.cos(a) * 16, 140 + math.sin(a) * 16, 3), Seg(250, 140, 262, 148, 3)]), INK)
    for x in (110, 330):
        S.obj(g, Box(x, 220, x + 60, 280, 3), (150, 200, 240), 6 + x, hi=True)
    S.obj(g, Union([Box(220, 260, 280, 360), Circ(250, 260, 30) & Box(220, 230, 280, 260)]), (140, 90, 60) if "door" not in d else (80, 120, 180), 8, "wood")
    # platform, rails, train
    S.obj(g, Box(-2, 360, W + 2, 400), (200, 190, 180), 9)
    S.obj(g, Box(-2, 360, W + 2, 368), (250, 220, 90), 10)
    S.obj(g, Box(-2, 470, W + 2, 600), (150, 140, 130), 11)
    for x in range(0, 900, 40):
        g.fill(Box(x, 500, x + 24, 512), (120, 90, 70))
    g.fill(Union([Box(-2, 494, W + 2, 498), Box(-2, 516, W + 2, 520)]), (90, 90, 100))
    S.obj(g, Union([Box(460, 380, 860, 490, 12), Box(780, 330, 860, 400, 6)]), (60, 120, 90), 12, hi=True)
    S.obj(g, Box(440, 310, 470, 400, 3), (40, 40, 50), 13)
    for x in (520, 600, 680, 760):
        S.obj(g, Circ(x, 490, 22), (40, 40, 50), 14 + x)
        S.obj(g, Circ(x, 490, 9), (230, 60, 60), 15 + x)
    for x in (500, 580, 660):
        S.obj(g, Box(x, 400, x + 50, 440, 4), (250, 230, 150) if not ("window" in d and x == 580) else (150, 200, 240), 16 + x)
    # benches, luggage, flower tubs, a station master
    S.obj(g, Union([Box(80, 380, 200, 392, 2), Box(86, 392, 94, 420), Box(186, 392, 194, 420), Box(80, 360, 200, 370, 2)]), (150, 100, 60), 30, "wood")
    for i, (x, w, c) in enumerate(((240, 50, (180, 90, 60)), (296, 36, (90, 120, 170)))):
        if "case" in d and i == 1:
            c = (220, 180, 70)
        S.obj(g, Box(x, 420 - w * 0.7, x + w, 420, 4), c, 31 + i)
    for i, x in enumerate((40, 380)):
        S.obj(g, Box(x - 20, 420, x + 20, 452, 4), (170, 110, 70) if not ("flowers" in d and i == 1) else (80, 130, 190), 33 + i, "wood")
        bush(S, g, x, 424, 22, (90, 160, 80), seed=35 + i, flowers=(250, 120, 160))
    person(S, g, 360, 460, 140, (40, 60, 120), face=1, seed=40, hat=(40, 60, 120))
    S.obj(g, Union([Box(400, 360, 404, 400), Circ(402, 356, 8)]), (240, 60, 60), 41)


L1655_EL = [puff_el("st%d" % i, 455, 300, r=14, rise=90, wind=-10, phase=i / 3) for i in range(3)] + \
            [cloud_el("c2", 600, 70, 60, 16, speed=5, seed=50), bird_el("b", 300, 60, speed=18)]
L1655_DIFFS = [("clock", 250, 140, 0), ("door", 250, 300, 0), ("window", 605, 420, 0), ("case", 314, 406, 0), ("flowers", 380, 436, 0)]


LEVELS = [
    ("Level1649", "卡通·海底小镇", make(l1649), L1649_EL, L1649_DIFFS, 60, OPTS),
    ("Level1650", "卡通·月面基地", make(l1650), L1650_EL, L1650_DIFFS, 60, OPTS),
    ("Level1651", "卡通·恐龙山谷", make(l1651), L1651_EL, L1651_DIFFS, 60, OPTS),
    ("Level1652", "卡通·面包房", make(l1652), L1652_EL, L1652_DIFFS, 60, OPTS),
    ("Level1653", "卡通·云上城堡", make(l1653), L1653_EL, L1653_DIFFS, 60, OPTS),
    ("Level1654", "卡通·灯笼夜市", make(l1654), L1654_EL, L1654_DIFFS, 60, OPTS),
    ("Level1655", "卡通·火车站台", make(l1655), L1655_EL, L1655_DIFFS, 60, OPTS),
]
