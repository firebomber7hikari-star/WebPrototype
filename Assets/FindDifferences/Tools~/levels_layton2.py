# -*- coding: utf-8 -*-
"""Storybook puzzle-adventure levels, set 2 (same watercolour LaytonS look as levels_layton; original places and characters):
  Level1656 雾港小镇   - a misty harbour: leaning warehouses, fishing boats, a lighthouse, gulls, crates
  Level1657 古董书店   - an antique bookshop: towering shelves, rolling ladder, curios, a shop cat
  Level1658 玻璃温室   - a glass greenhouse: potted palms, hanging baskets, watering cans, a fountain
  Level1659 博物馆大厅 - a museum hall: paintings, a vase on a plinth, an airship model, a suit of armour
  Level1660 山顶天文台 - an observatory at night: brass telescope under the open dome, star charts, orrery
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Diff, Ell, Inter, Poly, Rough, Seg, Under, Union, el, fbm1, vgrad
from levels_layton import INK, OPTS, S, apprentice, clock_face, crooked_house, lamp, make, professor
from styled_kit import sparkle_el


def wave(y, amp, period, seed):
    return lambda x: y + amp * np.sin(x / period + seed) + (fbm1(x, 60, 2, seed) - 0.5) * amp


def boat(g, x, base, w, hull, sail=None, seed=0):
    S.obj(g, Poly([(x - w / 2, base - 24), (x + w / 2, base - 24), (x + w / 2 - 16, base), (x - w / 2 + 16, base)]), hull, seed, "wood")
    if sail:
        S.line(g, x, base - 24, x, base - 24 - w * 0.9, 2, (90, 70, 50))
        S.obj(g, Poly([(x + 2, base - 28 - w * 0.85), (x + 2, base - 30), (x + w * 0.45, base - 30)]), sail, seed + 1)


# =================================================================== Level 1656 misty harbour
def l1656(g, d):
    S.sky(g, [(0, (190, 200, 210)), (300, (236, 220, 196))])
    S.water(g, Box(-2, 330, W + 2, H + 2), (150, 180, 190), (90, 120, 140), 1)
    # lighthouse on a rocky point (right)
    S.obj(g, Rough(Ell(800, 340, 120, 40), 6, 14, 2), (150, 140, 130), 2)
    S.obj(g, Poly([(778, 330), (822, 330), (812, 150), (788, 150)]), (246, 240, 226), 3)
    for y in (200, 270):
        S.obj(g, Poly([(780 + (330 - y) * 0.05, y), (820 - (330 - y) * 0.05, y), (820 - (330 - y - 20) * 0.05, y + 20), (780 + (330 - y - 20) * 0.05, y + 20)]),
              (200, 70, 60) if "stripe" not in d else (70, 110, 170), 4 + y)
    S.obj(g, Box(786, 128, 814, 150), (250, 220, 140), 6)
    S.obj(g, Poly([(780, 128), (800, 110), (820, 128)]), (90, 70, 60), 7)
    # quay with leaning warehouses
    S.obj(g, Box(-2, 330, 560, 380), (170, 150, 130), 8, "brick")
    for i, (x0, w, h, wall, roof, lean) in enumerate(((10, 110, 220, (220, 200, 170), (110, 120, 140), 0.03), (130, 100, 190, (200, 170, 150), (150, 80, 60), -0.04),
                                                      (240, 120, 240, (230, 216, 190), (90, 110, 100), 0.02), (370, 100, 180, (210, 190, 200), (140, 90, 80), -0.03))):
        crooked_house(g, x0, 330, w, h, wall, roof, 20 + i * 40, lean=lean, lit={(0, 1)} if i == 2 and "window" not in d else set(), chimney=i != 1)
    # boats
    boat(g, 300, 470, 160, (160, 80, 60), sail=(246, 236, 214), seed=60)
    boat(g, 600, 420, 120, (70, 110, 150) if "boat" not in d else (90, 150, 90), sail=(230, 200, 150), seed=62)
    # crates, barrels, a lamp and a gull on a post
    for i, (x, y) in enumerate(((440, 330), (470, 330), (455, 304))):
        if "crate" in d and i == 2:
            continue
        S.obj(g, Box(x - 14, y - 26, x + 14, y, 2), (180, 130, 80), 70 + i, "wood")
    lamp(g, 520, 330, 80)
    S.obj(g, Box(160, 380, 172, 470), (110, 80, 60), 75, "wood")
    if "gull" not in d:
        S.obj(g, Union([Ell(166, 372, 14, 8), Circ(176, 364, 6), Poly([(180, 362), (190, 365), (180, 368)])]), (246, 246, 250), 76)
    professor(g, 700, 590, 170, face=-1, seed=80)
    apprentice(g, 770, 594, 110, face=-1, seed=81)
    g.fill(Box(-2, 260, W + 2, 340), (240, 236, 226), alpha=0.25, feather=20)


L1656_EL = [E("gulls", el(lambda g, m: [g.fill(Union([Seg(x - 8, y - 3, x, y, 1.6), Seg(x, y, x + 8, y - 3, 1.6)]), INK) for x, y in ((500, 90), (530, 80), (560, 100))]),
              anim=dict(bobAmplitude=(60, 8), bobSpeed=0.05)),
            E("beam", el(lambda g, m: g.fill(Poly([(800, 138), (620, 100), (620, 170)]), (255, 240, 190), alpha=0.25, feather=10)), daynight="untinted",
              anim=dict(twinkle=0.8, twinkleSpeed=0.3)),
            sparkle_el("sea", [(200, 520), (480, 560), (700, 500)], col=(255, 250, 236), r=4, speed=0.5)]
L1656_DIFFS = [("stripe", 800, 230, 0), ("window", 290, 260, 0), ("boat", 600, 410, 0), ("crate", 455, 290, 0), ("gull", 172, 368, 0)]


# =================================================================== Level 1657 antique bookshop
def l1657(g, d):
    S.obj(g, Box(-2, -2, W + 2, 450), (170, 130, 100), 1, line=False)
    rnd = random.Random(1657)
    for x0, x1 in ((10, 320), (580, 890)):
        S.obj(g, Box(x0, 20, x1, 450), (120, 80, 56), 2 + x0, "wood")
        for y in (40, 140, 240, 340):
            x = x0 + 10
            while x < x1 - 16:
                w = rnd.uniform(10, 20)
                hh = rnd.uniform(56, 86)
                bc = [(160, 60, 50), (60, 90, 130), (90, 130, 80), (200, 160, 80), (130, 80, 120), (150, 120, 90)][rnd.randrange(6)]
                if "books" in d and x0 == 10 and y == 40 and 110 <= x <= 230:
                    bc = (70, 150, 150)
                S.obj(g, Box(x, y + 92 - hh, x + w, y + 92), bc, 5)
                x += w + 1.2
            S.obj(g, Box(x0, y + 92, x1, y + 100), (140, 96, 66), 6, "wood")
    # rolling ladder on a rail
    S.obj(g, Box(570, 26, 900, 32), (190, 150, 80), 7)
    for xa in (640, 680):
        S.obj(g, Seg(xa, 30, xa + 30, 450, 3.6), (150, 100, 66), 8)
    for k in range(1, 11):
        if "rung" in d and k in (5, 6):
            continue
        t = k / 11
        S.obj(g, Seg(640 + 30 * t, 30 + 420 * t, 680 + 30 * t, 30 + 420 * t, 2.6), (170, 120, 76), 9)
    # middle: shop window, bell, counter with curios
    S.obj(g, Box(360, 60, 540, 260, 4), (130, 90, 60), 10, "wood")
    g.fill(Box(372, 72, 528, 248), vgrad([(72, (210, 220, 220)), (248, (240, 220, 190))]))
    g.fill(Union([Box(447, 72, 453, 248), Box(372, 157, 528, 163)]), (130, 90, 60))
    S.obj(g, Union([Inter(Circ(450, 290, 14), Box(436, 276, 464, 292)), Box(448, 266, 452, 278)]), (210, 170, 80) if "bell" not in d else (150, 150, 160), 11)
    S.ground(g, Box(-2, 450, W + 2, H + 2), (150, 100, 70), "wood", 12, line=True)
    S.obj(g, Box(330, 400, 570, 470, 3), (140, 92, 62), 13, "wood")
    S.obj(g, Box(320, 392, 580, 406, 2), (160, 110, 76), 14)
    S.obj(g, Union([Ell(380, 368, 22, 26), Box(370, 340, 390, 350)]), (90, 130, 160) if "vase" not in d else (200, 100, 90), 15, hi=True)
    S.obj(g, Poly([(420, 392), (500, 384), (504, 392), (424, 400)]), (246, 236, 214), 16)
    clock_face(g, 540, 368, 20, seed=17)
    if "candle" not in d:
        S.obj(g, Box(474, 356, 482, 384), (246, 240, 226), 18)
        g.glow(478, 348, 20, (255, 210, 120), 0.4)
        S.obj(g, Ell(478, 350, 3, 6), (255, 200, 90), 19, line=False)
    # shop cat on a book pile, customer
    for k, c in enumerate(((160, 60, 50), (60, 90, 130), (200, 160, 80))):
        S.obj(g, Box(110 - k * 4, 560 - k * 16, 200 + k * 4, 576 - k * 16, 2), c, 20 + k)
    S.obj(g, Union([Ell(150, 500, 26, 14), Circ(174, 488, 11), Poly([(168, 480), (170, 468), (176, 478)]), Poly([(178, 478), (184, 468), (184, 482)])]),
          (70, 60, 70) if "cat" not in d else (240, 170, 90), 23)
    professor(g, 460, 600, 170, face=-1, seed=30)
    apprentice(g, 780, 600, 120, face=-1, seed=31)


L1657_EL = [sparkle_el("dust", [(420, 120), (500, 200), (460, 160)], col=(255, 246, 220), r=3, speed=0.5),
            E("flame", el(lambda g, m: g.glow(478, 348, 10, (255, 220, 140), 0.5)), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.4))]
L1657_DIFFS = [("rung", 662, 270, 0), ("books", 170, 90, 0), ("vase", 380, 362, 0), ("cat", 160, 492, 0)]


# =================================================================== Level 1658 glass greenhouse
def l1658(g, d):
    S.sky(g, [(0, (190, 220, 210)), (500, (240, 236, 210))])
    # glass roof frames
    for x in range(-40, 960, 80):
        S.line(g, x, 0, 450, -260, 2, (90, 110, 100))
    for k in range(8):
        y = 30 + k * 50
        S.line(g, -10, y, 910, y, 1.6, (90, 110, 100))
    for x in range(0, 900, 100):
        S.line(g, x, 0, x, 440, 2, (90, 110, 100))
    S.ground(g, Box(-2, 440, W + 2, H + 2), (180, 150, 120), "dirt", 1, line=True)
    for x in range(0, 900, 60):
        g.fill(Box(x + 4, 470, x + 52, 590), (200, 170, 140), alpha=0.4)
    # potted palms and plants
    for i, (x, h, pot) in enumerate(((90, 220, (190, 110, 80)), (330, 160, (180, 120, 90)), (760, 240, (190, 110, 80)))):
        S.obj(g, Poly([(x - 30, 440), (x + 30, 440), (x + 22, 490), (x - 22, 490)]), pot if not ("pot" in d and i == 1) else (80, 130, 170), 10 + i)
        S.obj(g, Seg(x, 440, x + 6, 440 - h, 5, 3), (130, 100, 70), 13 + i)
        fronds = [Poly([(x + 6, 440 - h), (x + 6 + math.cos(a) * 80, 440 - h + math.sin(a) * 30 + 30), (x + 6 + math.cos(a) * 40, 440 - h + math.sin(a) * 10 + 4)]) for a in np.linspace(-2.8, -0.3, 6)]
        S.obj(g, Union(fronds), (90, 150, 90), 16 + i)
    # hanging baskets
    for i, x in enumerate((220, 520, 640)):
        if "basket" in d and i == 0:
            continue
        S.line(g, x, 0, x, 130, 1, INK)
        S.obj(g, Inter(Ell(x, 140, 30, 22), Box(x - 30, 140, x + 30, 170)), (170, 120, 70), 20 + i, "wood")
        fc = [(230, 90, 120), (250, 200, 80), (160, 110, 220)][i]
        if "flowers" in d and i == 1:
            fc = (250, 250, 250)
        for k in range(5):
            S.obj(g, Circ(x - 24 + k * 12, 138 - (k % 2) * 6, 7), fc, 23 + i)
    # fountain, watering cans, bench
    S.obj(g, Ell(500, 470, 90, 22), (190, 190, 200), 30)
    S.water(g, Ell(500, 466, 78, 16), (150, 200, 220), (110, 170, 200), 31)
    S.obj(g, Box(492, 380, 508, 466, 3), (190, 190, 200), 32)
    S.obj(g, Ell(500, 380, 30, 8), (190, 190, 200), 33)
    if "frog" not in d:
        S.obj(g, Union([Ell(560, 456, 12, 8), Circ(554, 448, 4), Circ(566, 448, 4)]), (110, 170, 90), 34)
    for i, (x, c) in enumerate(((620, (90, 130, 110)), (680, (200, 90, 80)))):
        if "can" in d and i == 1:
            c = (230, 190, 80)
        S.obj(g, Union([Box(x - 18, 520, x + 18, 556, 4), Seg(x + 18, 530, x + 40, 514, 3), Seg(x - 12, 520, x + 12, 512, 2)]), c, 35 + i)
    S.obj(g, Union([Box(160, 520, 300, 532, 2), Box(166, 532, 172, 560), Box(288, 532, 294, 560), Box(160, 500, 300, 508, 2)]), (240, 240, 236), 40)
    apprentice(g, 400, 600, 130, face=1, seed=41)
    professor(g, 860, 600, 170, face=-1, seed=42)


L1658_EL = [E("spray", el(lambda g, m: [g.fill(Seg(500 + s * 4, 380, 500 + s * 34, 460, 1.2), (200, 230, 250), alpha=0.6) for s in (-1, 1)]), daynight="untinted",
              anim=dict(twinkle=0.3, twinkleSpeed=1.5)),
            E("butterfly", el(lambda g, m: S.obj(g, Union([Ell(300, 300, 7, 5), Ell(310, 300, 7, 5)]), (250, 180, 80), 1)), pivot=(305, 300),
              anim=dict(stretch=(0.6, 0), scaleSpeed=3.0, bobAmplitude=(40, 20), bobSpeed=0.12)),
            sparkle_el("light", [(150, 80), (450, 60), (750, 90)], col=(255, 250, 230), r=5, speed=0.4)]
L1658_DIFFS = [("pot", 330, 465, 0), ("flowers", 520, 136, 0), ("basket", 220, 120, 0), ("can", 690, 536, 0)]


# =================================================================== Level 1659 museum hall
def frame_art(g, x0, y0, x1, y1, art, frame=(190, 150, 80), seed=0):
    S.obj(g, Box(x0 - 10, y0 - 10, x1 + 10, y1 + 10, 2), frame, seed)
    g.fill(Box(x0, y0, x1, y1), vgrad([(y0, art[0]), (y1, art[1])]))
    g.fill(Ell((x0 + x1) / 2, (y0 + y1) * 0.55, (x1 - x0) * 0.25, (y1 - y0) * 0.2), art[2])


def l1659(g, d):
    S.obj(g, Box(-2, -2, W + 2, 420), (210, 190, 160), 1, line=False)
    for x in (120, 450, 780):
        S.obj(g, Box(x - 22, -2, x + 22, 420), (230, 214, 190), 2 + x)
    frame_art(g, 200, 90, 360, 220, ((150, 190, 220), (110, 150, 100), (240, 200, 90)), seed=10)
    frame_art(g, 540, 80, 700, 230, ((240, 200, 160), (200, 120, 90), (90, 70, 60) if "art" not in d else (70, 110, 170)), seed=11)
    frame_art(g, 20, 120, 90, 220, ((90, 90, 120), (60, 60, 80), (230, 220, 200)), frame=(170, 130, 70) if "frame" not in d else (120, 120, 130), seed=12)
    S.ground(g, Box(-2, 420, W + 2, H + 2), (180, 150, 120), "wood", 13, line=True)
    for x in range(-20, 900, 60):
        g.fill(Poly([(x, 420), (x + 30, 420), (x + 60, 600), (x + 30, 600)]), (200, 170, 140), alpha=0.5)
    # rope barrier
    for x in (240, 380):
        S.obj(g, Union([Box(x - 4, 380, x + 4, 460), Circ(x, 380, 8)]), (190, 150, 80), 14 + x)
    S.line(g, 240, 392, 380, 392, 2, (180, 40, 50))
    # vase on a plinth (centre)
    S.obj(g, Box(410, 340, 490, 470, 3), (236, 230, 220), 20)
    S.obj(g, Union([Ell(450, 300, 30, 36), Box(436, 256, 464, 268)]), (90, 130, 170) if "vase" not in d else (200, 120, 90), 21, hi=True)
    g.fill(Inter(Box(420, 290, 480, 300), Ell(450, 300, 30, 36)), (240, 220, 160))
    # airship model hanging
    S.line(g, 820, 0, 820, 60, 1, INK)
    S.obj(g, Ell(820, 90, 70, 26), (200, 180, 140), 22, hi=True)
    S.obj(g, Box(800, 116, 840, 132, 3), (150, 100, 66) if "gondola" not in d else (90, 140, 110), 23)
    S.obj(g, Poly([(752, 80), (736, 64), (744, 96)]), (170, 80, 60), 24)
    # suit of armour on a stand (left)
    S.obj(g, Union([Box(80, 330, 140, 420, 8), Ell(110, 310, 20, 24), Box(88, 420, 104, 500, 4), Box(116, 420, 132, 500, 4)]), (190, 196, 206), 25, hi=True)
    S.obj(g, Box(94, 304, 126, 312), (50, 50, 60), 26)
    if "plume" not in d:
        S.obj(g, Poly([(110, 286), (90, 250), (130, 260)]), (200, 60, 70), 27)
    S.obj(g, Box(70, 500, 150, 512, 2), (120, 80, 56), 28)
    # visitors
    professor(g, 600, 600, 180, face=-1, seed=30)
    apprentice(g, 330, 600, 120, face=1, coat=(80, 120, 170) if "coat" not in d else (90, 150, 90), seed=31)


L1659_EL = [sparkle_el("glint", [(450, 290), (820, 80)], col=(255, 255, 240), r=5, speed=0.5),
            E("prop", el(lambda g, m: S.obj(g, Union([Ell(748, 70, 3, 12), Ell(748, 94, 3, 12)]), (120, 110, 100), 1, line=False)), pivot=(748, 82),
              anim=dict(stretch=(0, 0.7), scaleSpeed=2.0))]
L1659_DIFFS = [("art", 620, 160, 0), ("frame", 55, 170, 0), ("vase", 450, 300, 0), ("gondola", 820, 124, 0), ("plume", 110, 266, 0), ("coat", 330, 530, 0)]


# =================================================================== Level 1660 hilltop observatory at night
def l1660(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (110, 90, 100), 1, line=False)
    # the dome with its slit open to the stars
    S.obj(g, Inter(Ell(450, 380, 470, 380), Box(-20, 0, 920, 380)), (130, 110, 120), 2, "roof")
    slit = Poly([(380, -2), (520, -2), (500, 380), (400, 380)])
    g.fill(slit, vgrad([(0, (20, 26, 60)), (380, (60, 60, 110))]))
    rnd = random.Random(1660)
    for _ in range(40):
        x, y = rnd.uniform(390, 510), rnd.uniform(0, 360)
        g.fill(Circ(x, y, rnd.uniform(0.8, 2)), (255, 250, 230))
    g.fill(Seg(420, 80, 470, 50, 2, 0.4), (255, 250, 220))
    g.fill(Circ(470, 50, 4), (255, 250, 230))
    S.ground(g, Box(-2, 420, W + 2, H + 2), (120, 80, 60), "wood", 3, line=True)
    S.obj(g, Box(-2, 380, W + 2, 424), (90, 70, 70), 4, "wood")
    # brass telescope on a stand
    S.obj(g, Union([Seg(330, 560, 450, 440, 6), Seg(570, 560, 450, 440, 6), Seg(450, 440, 450, 580, 6)]), (110, 80, 56), 10)
    S.obj(g, Seg(360, 480, 520, 200, 26, 16), (200, 160, 80), 11, hi=True)
    S.obj(g, Union([Box(360, 470, 400, 500, 4)]), (180, 140, 70), 12)
    S.obj(g, Ell(520, 200, 18, 10), (120, 90, 60) if "lens" not in d else (90, 140, 200), 13)
    # star charts on the wall, an orrery on the desk
    S.obj(g, Box(40, 120, 220, 300, 3), (230, 214, 180), 20)
    for x, y in ((80, 160), (130, 200), (180, 150), (110, 260), (170, 240)) if "chart" not in d else ():
        g.fill(Circ(x, y, 3), INK)
    if "chart" not in d:
        g.fill(Union([Seg(80, 160, 130, 200, 1), Seg(130, 200, 180, 150, 1), Seg(130, 200, 170, 240, 1)]), INK)
    else:
        S.obj(g, Circ(130, 210, 40) - Circ(150, 196, 34), (240, 180, 80), 26)
    S.obj(g, Box(680, 120, 860, 290, 3), (220, 200, 170), 21)
    g.fill(Circ(770, 205, 50) - Circ(770, 205, 48), INK)
    for a in range(8):
        g.fill(Seg(770, 205, 770 + math.cos(a * math.pi / 4) * 50, 205 + math.sin(a * math.pi / 4) * 50, 0.8), INK)
    S.obj(g, Box(640, 470, 880, 490, 3), (140, 92, 62), 22, "wood")
    for lx in (660, 850):
        S.obj(g, Box(lx, 490, lx + 16, 580), (120, 80, 54), 23, "wood")
    S.obj(g, Union([Box(756, 420, 764, 470), Box(730, 464, 790, 472)]), (190, 150, 80), 24)
    S.obj(g, Circ(760, 410, 16), (250, 200, 80), 25, hi=True)
    lamp(g, 680, 470, 30, lit="lamp" not in d)
    # scholar at the eyepiece, apprentice with a notebook
    professor(g, 300, 600, 180, face=1, seed=30)
    apprentice(g, 140, 600, 120, face=1, coat=(80, 120, 170) if "coat" not in d else (170, 80, 80), seed=31)
    S.obj(g, Box(160, 500, 186, 520, 2), (230, 220, 200), 32)


def l1660_orrery(g, m):
    for r, a, c in ((40, 0.4, (110, 160, 220)), (60, 2.4, (220, 110, 90)), (26, 4.4, (200, 200, 210))):
        g.fill(Ell(760, 410, r, r * 0.4) - Ell(760, 410, r - 1.2, r * 0.4 - 1.2), (150, 120, 70))
        S.obj(g, Circ(760 + math.cos(a) * r, 410 + math.sin(a) * r * 0.4, 6), c, 40)


L1660_EL = [E("orrery", el(l1660_orrery), pivot=(760, 410), anim=dict(stretch=(0.02, 0), scaleSpeed=0.2)),
            sparkle_el("stars", [(410, 100), (480, 220), (440, 300), (500, 140)], col=(255, 250, 230), r=4, speed=0.6),
            E("dome", el(lambda g, m: g.fill(Poly([(400, 380), (500, 380), (560, 600), (340, 600)]), (200, 210, 250), alpha=0.1, feather=20)), daynight="untinted",
              anim=dict(twinkle=0.5, twinkleSpeed=0.2))]
L1660_DIFFS = [("lens", 520, 200, 0), ("chart", 130, 210, 0), ("lamp", 680, 430, 0), ("coat", 140, 530, 0)]


LEVELS = [
    ("Level1656", "雾港小镇", make(l1656), L1656_EL, L1656_DIFFS, 60, OPTS),
    ("Level1657", "古董书店", make(l1657), L1657_EL, L1657_DIFFS, 60, OPTS),
    ("Level1658", "玻璃温室", make(l1658), L1658_EL, L1658_DIFFS, 60, OPTS),
    ("Level1659", "博物馆大厅", make(l1659), L1659_EL, L1659_DIFFS, 60, OPTS),
    ("Level1660", "山顶天文台", make(l1660), L1660_EL, L1660_DIFFS, 60, OPTS),
]
