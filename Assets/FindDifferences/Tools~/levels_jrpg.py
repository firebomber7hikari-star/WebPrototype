# -*- coding: utf-8 -*-
"""Cel-shaded (toon-render) JRPG levels (original characters, monsters and places; no text, no logos):
  Level1585 启程之村   - the hero's starting village: cottages, inn sign, well, windmill, river bridge
  Level1586 王城谒见   - the throne room: king and queen, guards, red carpet, stained glass, chandelier
  Level1587 史莱姆之战 - a turn-based battle on the plains: party vs slimes, command window and HP gauges
  Level1588 迷雾森林   - a misty forest: giant trees, glowing mushrooms, fairy lights, a hidden chest
  Level1589 飞空艇甲板 - an airship deck above the clouds: balloon, propellers, captain at the wheel
  Level1590 沙漠绿洲城 - a desert oasis town: domes, palms, pond, merchant stalls, ruins on the horizon
  Level1591 雪山村落   - a snowy mountain village: snow-roofed cottages, hot spring, snowman, pines
  Level1592 港口城镇   - a harbour town: sailing ship, lighthouse, tavern, crates, gulls
  Level1593 水晶神殿   - a crystal shrine in a cavern: floating crystal on an altar, glowing crystals, pool
  Level1594 魔王城     - the demon lord's castle: lightning sky, lava moat, bridge, the party at the gate
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Poly, Rough, Seg, Under, Union, el, fbm1, mixc, vgrad
from levels_remake import ToonS
from toon import bird_el, cloud_el, cloud_shape, puff_el, sparkle_el, toon_post
from styled_kit import (SKIN, banner, barrel, bush, castle, chest, coin_pile, crate, crystal, dragon, goblin, hero, lamp_post,
                        mage, palm, person, pine_tree, potion, rock, round_tree, sh_shadow, sign_board, slime, torch, tower,
                        building)

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


def cottage(g, x0, base, w, h, wall, roof, seed, lit=False, chimney=True, door=(140, 90, 50), snow=None):
    S.obj(g, Box(x0, base - h, x0 + w, base), wall, seed, "plain")
    rp = Poly([(x0 - 12, base - h + 4), (x0 + w / 2, base - h - w * 0.5), (x0 + w + 12, base - h + 4)])
    if chimney:
        S.obj(g, Box(x0 + w * 0.7, base - h - w * 0.45, x0 + w * 0.82, base - h - w * 0.1), (170, 110, 90), seed + 1)
    S.obj(g, rp, roof, seed + 2, "roof")
    if snow:
        S.flat(g, Poly([(x0 - 12, base - h + 4), (x0 + w / 2, base - h - w * 0.5), (x0 + w + 12, base - h + 4), (x0 + w + 6, base - h + 10),
                        (x0 + w / 2, base - h - w * 0.4), (x0 - 6, base - h + 10)]), snow)
    S.obj(g, Union([Box(x0 + w * 0.12, base - 36, x0 + w * 0.34, base), Circ(x0 + w * 0.23, base - 36, w * 0.11)]), door, seed + 3, "wood")
    wc = (255, 220, 120) if lit else (150, 200, 240)
    if lit:
        S.glow(g, x0 + w * 0.68, base - h * 0.55, 40, (255, 200, 110), 0.3)
    S.obj(g, Box(x0 + w * 0.55, base - h * 0.7, x0 + w * 0.82, base - h * 0.4, 2), wc, seed + 4, hi=not lit)
    S.flat(g, Box(x0 + w * 0.68 - 1, base - h * 0.7, x0 + w * 0.68 + 1, base - h * 0.4), (80, 60, 50))


def menu_window(g, x0, y0, x1, y1):
    S.obj(g, Box(x0, y0, x1, y1, 8), (40, 50, 130), 1)
    S.flat(g, Box(x0 + 4, y0 + 4, x1 - 4, y1 - 4, 6), (40, 50, 130))
    g.fill(Diff(Box(x0 + 4, y0 + 4, x1 - 4, y1 - 4, 6), Box(x0 + 7, y0 + 7, x1 - 7, y1 - 7, 5)), (240, 240, 255))


def gauge(g, x0, y, w, frac, col):
    g.fill(Box(x0 - 1, y - 1, x0 + w + 1, y + 7, 3), (20, 20, 40))
    g.fill(Box(x0, y, x0 + w * frac, y + 6, 3), col)


# =================================================================== Level 1585 starting village
def l1585(g, d):
    S.sky(g, [(0, (110, 180, 245)), (330, (210, 236, 252))])
    for x, y, w, h, s in ((140, 80, 70, 22, 1), (560, 60, 90, 26, 2)):
        S.obj(g, cloud_shape(x, y, w, h, s), (255, 255, 255), s, "cloud", line=False)
    S.ground(g, Under(wave(300, 12, 90, 1), -20, W + 20), (150, 210, 120), "grass", 1, line=True)
    for x in (60, 820):
        round_tree(S, g, x, 320, 120, (90, 170, 80), seed=x, depth=0.4)
    # windmill (sails are an element)
    S.obj(g, Poly([(700, 300), (716, 190), (744, 190), (760, 300)]), (240, 230, 210), 3)
    S.obj(g, Poly([(708, 194), (730, 166), (752, 194)]), (190, 90, 80), 4, "roof")
    # river and bridge
    river = Poly([(380, 330), (460, 330), (520, 610), (300, 610)])
    S.water(g, river, (110, 190, 240), (70, 150, 220), 5)
    S.obj(g, Union([Box(330, 420, 500, 436, 3)] + [Box(x, 400, x + 6, 436) for x in (336, 380, 424, 468, 490)]), (170, 120, 70), 6, "wood")
    S.ground(g, Poly([(-20, 610), (300, 610), (380, 330), (360, 330), (-20, 420)]), (130, 200, 100), "grass", 7)
    S.ground(g, Poly([(920, 610), (520, 610), (460, 330), (480, 330), (920, 380)]), (130, 200, 100), "grass", 8)
    # cottages and the inn
    cottage(g, 40, 400, 130, 100, (250, 236, 210), (200, 80, 70), 10, lit=False)
    cottage(g, 560, 380, 150, 110, (240, 226, 196), (80, 120, 190), 11, chimney="chimney" not in d)
    cottage(g, 740, 420, 130, 100, (250, 236, 210), (110, 160, 90), 12)
    S.line(g, 700, 330, 730, 330, 3, (100, 70, 50))
    sign_board(S, g, 690, 334, 744, 360, (190, 140, 80) if "sign" not in d else (120, 160, 210), seed=13, marks=2)
    # well
    S.obj(g, Ell(230, 470, 34, 12), (160, 160, 170), 14, "stone")
    S.obj(g, Box(196, 470, 264, 500, 4), (170, 170, 180), 15, "stone")
    S.line(g, 202, 470, 202, 420, 3, (130, 90, 60))
    S.line(g, 258, 470, 258, 420, 3, (130, 90, 60))
    S.obj(g, Poly([(190, 424), (230, 400), (270, 424)]), (190, 80, 70) if "well" not in d else (80, 130, 200), 16, "roof")
    if "bucket" not in d:
        S.obj(g, Box(216, 440, 244, 466, 3), (150, 110, 70), 17, "wood")
    # flowers and fence
    bush(S, g, 90, 560, 34, (90, 170, 80), seed=18)
    for k, (fx, fy) in enumerate(((66, 532), (90, 520), (112, 534), (80, 548), (104, 550))):
        S.obj(g, Circ(fx, fy, 6), (250, 120, 150) if "flowers" not in d else (250, 230, 90), 40 + k)
    for x in range(620, 900, 26):
        S.obj(g, Box(x, 470, x + 8, 506, 2), (240, 230, 210), 19 + x)
    S.flat(g, Box(616, 480, 900, 486), (220, 210, 190))
    # the party setting off
    hero(S, g, 640, 560, 120, face=1, seed=20, shield=(60, 90, 180))
    mage(S, g, 580, 566, 110, face=1, seed=21)
    person(S, g, 820, 580, 120, (120, 170, 90), skirt=True, hair_long=True, hair=(160, 90, 50), face=-1, seed=22,
           hat=None if "hat" not in d else (230, 210, 150))
    slime(S, g, 250, 590, 20, (120, 200, 250), seed=23)


L1585_EL = [
    E("sails", el(lambda g, m: [S.obj(g, Poly([(730, 200), (730 + math.cos(a) * 56 - math.sin(a) * 8, 200 + math.sin(a) * 56 + math.cos(a) * 8),
                                                   (730 + math.cos(a) * 56 + math.sin(a) * 8, 200 + math.sin(a) * 56 - math.cos(a) * 8)]), (250, 245, 230), 30)
                                for a in (0.3, 0.3 + math.pi / 2, 0.3 + math.pi, 0.3 + 1.5 * math.pi)]), pivot=(730, 200), anim=dict(rotateSpeed=-30)),
    cloud_el("cl1", 300, 110, 60, 18, speed=6, seed=31),
    puff_el("smoke1", 677, 300, r=8, rise=50, wind=-10),
    puff_el("smoke2", 677, 300, r=8, rise=50, wind=-10, phase=0.5),
    bird_el("bird1", 470, 90, speed=22),
]
L1585_DIFFS = [("chimney", 680, 296, 0), ("sign", 717, 347, 0), ("well", 230, 412, 0), ("bucket", 230, 454, 0), ("flowers", 90, 540, 0),
               ("hat", 820, 470, 0)]


# =================================================================== Level 1586 throne room
def l1586(g, d):
    S.obj(g, Box(-2, -2, W + 2, 430), (200, 190, 210), 1, "stone", line=False)
    for x in (80, 260, 640, 820):
        S.obj(g, Box(x - 26, -2, x + 26, 430), (230, 224, 236), 2 + x, "stone")
        S.obj(g, Box(x - 34, 400, x + 34, 430), (210, 200, 220), 3 + x, "stone")
    # stained glass window
    win = Union([Box(390, 60, 510, 220), Circ(450, 60, 60)])
    S.obj(g, win, (90, 140, 220), 4)
    for i, c in enumerate(((240, 80, 90), (250, 210, 80), (90, 200, 140), (240, 80, 90))):
        S.flat(g, Inter(Box(390 + i * 30, 0, 420 + i * 30, 220), win), mixc(c, (90, 140, 220), 0.35))
    S.flat(g, Inter(Union([Box(448, 0, 452, 220), Box(390, 120, 510, 124), Box(390, 170, 510, 174)]), win), (60, 50, 70))
    if "window" not in d:
        S.flat(g, Circ(450, 70, 22), (250, 220, 90))
    # banners
    for x, key in ((170, None), (730, "banner")):
        banner(S, g, x, 70, 60, 150, (190, 40, 60) if not (key and key in d) else (60, 90, 190), emblem="star", seed=5 + x)
    # floor + carpet + dais
    S.ground(g, Box(-2, 430, W + 2, H + 2), (220, 200, 170), "floor", 6, line=False)
    for x in range(-40, 960, 60):
        S.flat(g, Seg(x, 430, 450 + (x - 450) * 2.2, 610, 1.2), (190, 170, 140))
    S.obj(g, Box(330, 330, 570, 350, 3), (230, 210, 180), 7, "stone")
    S.obj(g, Box(300, 350, 600, 380, 3), (220, 200, 170), 8, "stone")
    S.obj(g, Poly([(400, 380), (500, 380), (590, 610), (310, 610)]), (200, 40, 50), 9, "fabric")
    S.flat(g, Poly([(410, 380), (418, 380), (330, 610), (318, 610)]), (250, 210, 80))
    S.flat(g, Poly([(482, 380), (490, 380), (582, 610), (570, 610)]), (250, 210, 80))
    # thrones with king and queen
    for x, col in ((400, (190, 40, 60)), (500, (60, 90, 190))):
        S.obj(g, Union([Box(x - 34, 220, x + 34, 340, 6), Circ(x, 220, 34)]), (240, 200, 80), 10 + x)
        S.obj(g, Box(x - 24, 236, x + 24, 330, 4), col, 11 + x, "fabric")
    person(S, g, 400, 350, 120, (190, 40, 60), pants=(150, 30, 50), hair=(240, 240, 240), face=1, seed=12)
    S.obj(g, Poly([(380, 228), (380, 212), (388, 220), (394, 206), (400, 218), (406, 206), (412, 220), (420, 212), (420, 228)]),
          (250, 210, 60), 13, hi=True)
    if "scepter" not in d:
        S.obj(g, Union([Box(430, 270, 436, 350, 2), Circ(433, 266, 7)]), (240, 200, 80), 14, hi=True)
    person(S, g, 500, 350, 116, (60, 90, 190), pants=(60, 90, 190), skirt=True, hair=(250, 210, 120), hair_long=True, face=-1, seed=15)
    S.obj(g, Union([Ell(500, 232, 20, 5), Poly([(482, 232), (488, 214), (494, 226), (500, 208), (506, 226), (512, 214), (518, 232)])]),
          (250, 210, 60) if "tiara" not in d else (200, 210, 240), 16, hi=True)
    # chandelier
    S.line(g, 450, -2, 450, 30, 2, (120, 100, 60))
    S.obj(g, Ell(450, 40, 80, 10), (230, 190, 80), 17)
    for i, x in enumerate(range(380, 530, 30)):
        if "candle" in d and i == 3:
            continue
        S.obj(g, Box(x - 3, 20, x + 3, 34), (250, 245, 230), 18 + i)
        S.glow(g, x, 14, 20, (255, 210, 120), 0.35)
        S.flat(g, Ell(x, 15, 3, 5), (255, 200, 80))
    # guards and the hero party
    for x, f in ((200, 1), (700, -1)):
        hero(S, g, x, 520, 140, tunic=(150, 150, 170), cape=(190, 40, 60), hair=(80, 70, 70), face=f, seed=20 + x, hair_spiky=False,
             shield=(190, 40, 60) if not (x == 700 and "shield" in d) else (60, 90, 190))
    hero(S, g, 450, 590, 130, face=1, seed=30, cape_on=True)
    mage(S, g, 380, 600, 110, seed=31)


L1586_EL = [sparkle_el("glint", [(450, 70), (250, 200), (650, 200)], r=6, speed=0.4)]
L1586_DIFFS = [("window", 450, 70, 0), ("banner", 730, 150, 0), ("scepter", 433, 325, 0), ("tiara", 500, 226, 0), ("candle", 470, 24, 0),
               ("shield", 670, 450, 0)]


# =================================================================== Level 1587 slime battle
def l1587(g, d):
    S.sky(g, [(0, (120, 190, 250)), (300, (220, 240, 252))])
    S.obj(g, cloud_shape(200, 90, 90, 24, 1), (255, 255, 255), 1, "cloud", line=False)
    S.obj(g, Poly([(500, 250), (620, 150), (760, 250)]), (150, 170, 200), 2, depth=0.6)
    S.obj(g, Poly([(620, 250), (760, 120), (920, 250)]), (140, 160, 196), 3, depth=0.6)
    S.ground(g, Under(wave(250, 6, 120, 2), -20, W + 20), (140, 210, 110), "grass", 4, line=True)
    S.ground(g, Ell(450, 380, 420, 70), (150, 220, 120), "grass", 5)
    # enemies (left)
    slime(S, g, 130, 380, 46, (90, 170, 250), seed=6, face=1, crown="king" not in d)
    slime(S, g, 340, 300, 30, (110, 220, 140) if "green" not in d else (250, 150, 90), seed=7, face=1)
    slime(S, g, 250, 440, 26, (90, 170, 250), seed=8, face=1)
    # party (right), facing left
    hero(S, g, 640, 420, 130, face=-1, seed=9, shield=(60, 90, 180))
    mage(S, g, 760, 400, 120, face=-1, seed=10, robe=(110, 70, 170) if "robe" not in d else (200, 70, 90))
    hero(S, g, 820, 470, 120, tunic=(240, 240, 240), cape=(90, 170, 220), hair=(170, 90, 60) if "hair" not in d else (90, 60, 160), face=-1, seed=11,
         sword=False, hair_spiky=False)
    # battle effects
    S.glow(g, 250, 420, 50, (255, 255, 200), 0.3)
    # command window + party status
    menu_window(g, 20, 470, 300, 590)
    for i in range(4):
        y = 492 + i * 24
        g.fill(Box(56, y, 56 + (110 - i * 18), y + 10, 3), (240, 240, 255))
    if "cursor" not in d:
        g.fill(Poly([(28, 486), (48, 497), (28, 508)]), (255, 230, 90))
    menu_window(g, 320, 470, 880, 590)
    for i, (frac, fr2) in enumerate(((0.9, 0.5), (0.6, 0.9), (0.75, 0.7))):
        x0 = 340 + i * 180
        g.fill(Box(x0, 488, x0 + 70, 498, 3), (240, 240, 255))
        gauge(g, x0, 512, 140, frac, (110, 230, 120) if not (i == 1 and "hp" in d) else (250, 150, 70))
        gauge(g, x0, 536, 140, fr2, (110, 170, 250))


L1587_EL = [
    sparkle_el("hit", [(250, 420)], col=(255, 250, 200), r=12, speed=1.2),
    cloud_el("cl", 520, 70, 50, 14, speed=5, seed=40),
]
L1587_DIFFS = [("king", 130, 306, 0), ("green", 340, 280, 0), ("robe", 760, 350, 0), ("hair", 820, 360, 0), ("hp", 590, 515, 0),
               ("cursor", 38, 497, 0)]


# =================================================================== Level 1588 misty forest
def l1588(g, d):
    S.sky(g, [(0, (60, 110, 110)), (400, (150, 200, 180))])
    for x, h in ((80, 380), (300, 340), (560, 360), (800, 400)):
        S.obj(g, Box(x - 40, 0, x + 40, 420), (90, 110, 120), x, "wood", depth=0.6)
    S.ground(g, Box(-2, 400, W + 2, H + 2), (90, 150, 100), "grass", 1, line=False)
    S.ground(g, Poly([(380, 400), (520, 400), (640, 610), (260, 610)]), (190, 170, 120), "dirt", 2)
    # giant trees framing
    for x, w, seed in ((40, 110, 3), (860, 120, 4)):
        S.obj(g, Union([Box(x - w / 2, -10, x + w / 2, 560), Poly([(x - w / 2 - 30, 560), (x - w / 2, 500), (x + w / 2, 500), (x + w / 2 + 30, 560)])]),
              (140, 100, 70), seed, "wood")
        S.obj(g, Union([Circ(x, -10, 160), Circ(x + (100 if x < 450 else -100), 40, 110)]), (60, 130, 80), seed + 1, "foliage", hi=True)
    # glowing mushrooms
    for x, base, r, key in ((200, 520, 26, "mush"), (240, 530, 16, None), (700, 500, 22, None), (730, 512, 14, None)):
        col = (240, 110, 170) if not (key and key in d) else (120, 200, 250)
        S.glow(g, x, base - r, r * 3, col, 0.25)
        S.obj(g, Box(x - r * 0.25, base - r, x + r * 0.25, base), (250, 240, 220), x)
        S.obj(g, Inter(Ell(x, base - r, r, r * 0.8), Box(x - r - 2, base - r * 1.9, x + r + 2, base - r)), col, x + 1, hi=True)
    # hidden treasure chest
    if "chest" not in d:
        chest(S, g, 590, 470, 48, seed=5)
    # sign post
    S.line(g, 330, 470, 330, 400, 4, (130, 90, 60))
    S.obj(g, Poly([(330, 404), (396, 404) if "arrow" not in d else (370, 404), (408 if "arrow" not in d else 382, 418), (396 if "arrow" not in d else 370, 432), (330, 432)]),
          (190, 150, 100), 6, "wood")
    # goblin peeking from a bush
    bush(S, g, 740, 470, 46, (70, 140, 80), seed=8)
    goblin(S, g, 690, 500, 110, face=-1, seed=7, weapon="dagger" not in d)
    rock(S, g, 140, 590, 40, seed=11)
    if "moss" not in d:
        S.obj(g, Ell(140, 556, 30, 9), (90, 170, 80), 12, "foliage")
    if "bird" not in d:
        S.obj(g, Union([Ell(250, 120, 16, 12), Circ(262, 108, 9)]), (230, 90, 70), 13, hi=True)
        S.flat(g, Poly([(270, 106), (282, 110), (270, 113)]), (250, 200, 60))
    # party walking in
    hero(S, g, 470, 580, 130, face=-1, seed=9)
    mage(S, g, 540, 590, 120, face=-1, seed=10)
    g.fill(Box(-2, 380, W + 2, 440), (200, 230, 220), alpha=0.3, feather=16)


L1588_EL = [
    sparkle_el("fairy1", [(150, 300), (420, 220), (650, 330), (300, 360)], col=(255, 250, 180), r=5, speed=0.6),
    sparkle_el("fairy2", [(250, 250), (520, 300), (720, 260)], col=(200, 255, 220), r=4, speed=0.5, phase=0.5),
    E("mist", el(lambda g, m: g.fill(Box(-20, 380, W + 20, 440), (220, 240, 235), alpha=0.35, feather=20)),
      anim=dict(bobAmplitude=(30, 0), bobSpeed=0.05)),
]
L1588_DIFFS = [("mush", 200, 498, 0), ("chest", 590, 446, 0), ("arrow", 380, 418, 0), ("dagger", 650, 410, 0), ("moss", 140, 556, 0),
               ("bird", 260, 112, 0)]


# =================================================================== Level 1589 airship deck
def l1589(g, d):
    S.sky(g, [(0, (90, 160, 240)), (600, (200, 230, 252))])
    for x, y, w, h, s in ((120, 470, 160, 40, 1), (500, 520, 220, 50, 2), (840, 480, 150, 36, 3)):
        S.obj(g, cloud_shape(x, y, w, h, s), (255, 255, 255), s, "cloud", line=False)
    # floating island in the distance
    if "island" not in d:
        S.obj(g, Poly([(700, 200), (820, 200), (790, 250), (760, 270), (730, 250)]), (150, 130, 110), 4, "stone", depth=0.4)
        S.obj(g, Ell(760, 200, 66, 14), (120, 190, 110), 5, "grass", depth=0.4)
        round_tree(S, g, 760, 200, 60, seed=6, depth=0.4)
    # balloon envelope and rigging
    env = Ell(360, 110, 300, 100)
    S.obj(g, env, (220, 70, 70), 7, "fabric", hi=True)
    for x in range(120, 620, 60):
        S.flat(g, Inter(Box(x, 0, x + 6, 220), env), (190, 50, 60))
    S.flat(g, Inter(Box(60, 120, 660, 132), env), (250, 210, 90))
    S.obj(g, Circ(360, 126, 30), (250, 210, 90) if "emblem" not in d else (90, 170, 230), 19, hi=True)
    for x in (160, 260, 460, 560):
        S.line(g, x, 190, x + (x - 360) * 0.2, 330, 1.6, (90, 70, 60))
    # deck
    S.obj(g, Poly([(-20, 330), (760, 330), (860, 380), (760, 430), (-20, 430)]), (170, 120, 70), 8, "wood")
    S.obj(g, Poly([(-20, 430), (760, 430), (840, 390), (860, 380), (860, 420), (760, 480), (-20, 480)]), (120, 80, 50), 9, "wood")
    for x in range(0, 760, 40):
        S.obj(g, Box(x, 300, x + 6, 332), (150, 100, 60), 10 + x)
    S.flat(g, Box(-20, 300, 760, 306), (150, 100, 60))
    # propeller hubs (blades are elements)
    for x, y in ((40, 456), (700, 456)):
        S.obj(g, Circ(x, y, 12), (160, 160, 170), 11 + x, hi=True)
    # captain's wheel
    S.obj(g, Box(608, 270, 620, 330), (130, 90, 50), 12, "wood")
    S.flat(g, Diff(Circ(614, 262, 26), Circ(614, 262, 20)), (150, 100, 50))
    for a in range(8):
        S.line(g, 614, 262, 614 + 32 * math.cos(a * math.pi / 4), 262 + 32 * math.sin(a * math.pi / 4), 2, (150, 100, 50))
    person(S, g, 660, 330, 120, (60, 70, 110) if "captain" not in d else (160, 50, 50), pants=(40, 40, 60), face=-1, seed=13, hat=(40, 40, 50),
           hair=(200, 200, 200))
    # crates, barrel, party
    crate(S, g, 60, 330, 46, 40, seed=14)
    if "crate" not in d:
        crate(S, g, 72, 290, 34, 30, seed=15)
    barrel(S, g, 140, 330, seed=16)
    hero(S, g, 300, 340, 110, face=1, seed=17)
    mage(S, g, 380, 340, 100, face=1, seed=18)


def l1589_prop(x, y):
    return E("prop%d" % x, el(lambda g, m: S.obj(g, Union([Ell(x, y - 26, 6, 24), Ell(x, y + 26, 6, 24)]), (200, 200, 210), 1, line=False)),
             pivot=(x, y), anim=dict(rotateSpeed=360))


L1589_EL = [l1589_prop(40, 456), l1589_prop(700, 456),
            cloud_el("cl1", 300, 560, 100, 24, speed=-30, seed=50), cloud_el("cl2", 700, 590, 90, 22, speed=-36, seed=51),
            bird_el("b1", 820, 160, speed=-20)]
L1589_DIFFS = [("island", 760, 220, 0), ("emblem", 360, 126, 0), ("captain", 660, 270, 0), ("crate", 89, 276, 0)]



# =================================================================== Level 1590 desert oasis town
def dome_house(g, x0, base, w, h, wall, dome, seed, lit=False):
    S.obj(g, Box(x0, base - h, x0 + w, base), wall, seed, "plain")
    S.obj(g, Inter(Ell(x0 + w / 2, base - h, w * 0.42, w * 0.42), Box(x0, base - h - w, x0 + w, base - h + 1)), dome, seed + 1, hi=True)
    S.obj(g, Union([Box(x0 + w * 0.4, base - 40, x0 + w * 0.6, base), Circ(x0 + w / 2, base - 40, w * 0.1)]), (120, 80, 50), seed + 2, "wood")
    S.obj(g, Union([Box(x0 + w * 0.15, base - h * 0.7, x0 + w * 0.3, base - h * 0.45), Circ(x0 + w * 0.225, base - h * 0.7, w * 0.075)]),
          (255, 220, 130) if lit else (70, 60, 80), seed + 3)


def l1590(g, d):
    S.sky(g, [(0, (110, 180, 240)), (300, (250, 230, 190))])
    S.glow(g, 780, 80, 90, (255, 250, 210), 0.5)
    S.obj(g, Circ(780, 80, 30), (255, 245, 200), 1, line=False)
    S.ground(g, Under(wave(280, 14, 120, 3), -20, W + 20), (240, 200, 130), "sand", 2, line=True)
    # far ruins
    for i, x in enumerate((100, 140, 180, 220)):
        if "ruin" in d and i == 2:
            continue
        S.obj(g, Box(x - 8, 220, x + 8, 286), (220, 190, 150), 3 + i, "stone", depth=0.4)
    S.obj(g, Box(90, 212, 200, 224), (220, 190, 150), 9, "stone", depth=0.4)
    # town
    dome_house(g, 420, 360, 120, 110, (240, 220, 190), (240, 190, 70) if "dome" not in d else (70, 150, 220), 10, lit=True)
    tower(S, g, 580, 360, 40, 180, (240, 220, 190), (240, 190, 70), seed=11, windows=2, flag=(200, 50, 60) if "flag" not in d else None)
    dome_house(g, 620, 380, 150, 120, (230, 210, 180), (90, 160, 210), 12)
    dome_house(g, 290, 380, 110, 90, (236, 214, 184), (200, 110, 80), 13)
    # oasis pond with palms
    pond = Ell(470, 500, 150, 36)
    S.water(g, pond, (90, 200, 220), (60, 160, 200), 14)
    if "lily" not in d:
        S.obj(g, Ell(520, 500, 20, 7), (90, 180, 90), 15)
        S.obj(g, Circ(526, 494, 6), (250, 140, 180), 16)
    palm(S, g, 330, 520, 170, lean=-0.15, seed=17)
    palm(S, g, 640, 510, 190, lean=0.18, seed=18)
    palm(S, g, 820, 470, 150, lean=0.1, seed=19)
    # market stall with a striped awning
    S.obj(g, Box(30, 420, 210, 500, 2), (170, 120, 70), 20, "wood")
    aw = Poly([(20, 420), (220, 420), (200, 380), (40, 380)])
    S.obj(g, aw, (250, 250, 240), 21)
    for k in range(5):
        x = 40 + k * 32
        S.flat(g, Inter(Box(x, 370, x + 16, 430), aw), (220, 60, 70) if "awning" not in d else (60, 120, 210))
    for k, c in enumerate(((240, 140, 60), (200, 70, 90), (250, 220, 90))):
        S.obj(g, Circ(60 + k * 22, 412, 9), c, 22 + k, hi=True)
    if "pot" not in d:
        S.obj(g, Union([Ell(250, 520, 22, 24), Box(240, 490, 260, 500)]), (200, 110, 70), 25, hi=True)
    person(S, g, 140, 560, 120, (240, 240, 230), pants=(200, 180, 140), face=1, seed=26, hat=(240, 240, 230), skin=(210, 160, 120))
    hero(S, g, 560, 590, 110, face=-1, seed=27)
    mage(S, g, 630, 596, 100, face=-1, seed=28)


L1590_EL = [sparkle_el("pond", [(420, 500), (500, 510), (560, 494)], r=5, speed=0.6), bird_el("b", 300, 120, speed=18)]
L1590_DIFFS = [("ruin", 180, 250, 0), ("dome", 480, 230, 0), ("flag", 595, 110, 0), ("lily", 520, 498, 0), ("awning", 120, 400, 0),
               ("pot", 250, 506, 0)]


# =================================================================== Level 1591 snowy mountain village
def l1591(g, d):
    S.sky(g, [(0, (130, 170, 230)), (300, (230, 240, 252))])
    for ax, ay, xl, xr in ((250, 80, 20, 480), (620, 50, 360, 900)):
        S.obj(g, Poly([(xl, 300), (ax, ay), (xr, 300)]), (150, 170, 210), ax, depth=0.4)
        S.flat(g, Poly([(ax - (ax - xl) * 0.3, ay + (300 - ay) * 0.3), (ax, ay), (ax + (xr - ax) * 0.3, ay + (300 - ay) * 0.3),
                        (ax + 10, ay + (300 - ay) * 0.36), (ax - 14, ay + (300 - ay) * 0.28)]), (250, 252, 255))
    S.ground(g, Under(wave(300, 10, 100, 4), -20, W + 20), (240, 246, 255), "snow", 2, line=True)
    for i, x in enumerate((40, 110, 820, 880)):
        if "pine" in d and i == 1:
            continue
        pine_tree(S, g, x, 360 + i * 10, 140, seed=3 + i, snow=(250, 252, 255))
    cottage(g, 180, 400, 140, 100, (200, 150, 110), (150, 70, 60), 10, lit="window" not in d, snow=(250, 252, 255))
    cottage(g, 600, 390, 150, 110, (190, 140, 100), (90, 100, 150), 11, lit=True, snow=(250, 252, 255))
    # hot spring
    S.obj(g, Rough(Ell(450, 470, 110, 30), 4, 10, 12), (170, 170, 180), 12, "stone")
    S.water(g, Ell(450, 470, 94, 22), (120, 200, 230), (90, 170, 210), 13)
    # snowman
    S.obj(g, Circ(780, 540, 40), (250, 252, 255), 14, hi=True)
    S.obj(g, Circ(780, 480, 28), (250, 252, 255), 15, hi=True)
    S.flat(g, Circ(770, 474, 3), (40, 40, 50))
    S.flat(g, Circ(790, 474, 3), (40, 40, 50))
    if "nose" not in d:
        S.obj(g, Poly([(780, 482), (808, 488), (780, 492)]), (250, 140, 50), 16)
    S.obj(g, Box(752, 498, 808, 510, 3), (220, 50, 60) if "scarf" not in d else (60, 160, 90), 17)
    S.obj(g, Union([Box(760, 444, 800, 456), Box(766, 420, 794, 446, 2)]), (40, 40, 50), 18)
    # sled
    S.obj(g, Box(80, 540, 200, 556, 3), (200, 60, 60) if "sled" not in d else (60, 120, 210), 19, "wood")
    S.line(g, 70, 572, 210, 572, 3, (120, 110, 120))
    S.line(g, 210, 572, 220, 560, 3, (120, 110, 120))
    for x in (100, 180):
        S.line(g, x, 556, x, 572, 2.4, (120, 110, 120))
    lamp_post(S, g, 400, 560, 110, lit="lamp" not in d)
    hero(S, g, 560, 590, 120, face=-1, seed=20, tunic=(60, 110, 200), cape=(200, 50, 60))
    mage(S, g, 640, 596, 108, face=-1, seed=21)


L1591_EL = [puff_el("st%d" % i, 420 + i * 30, 460, r=12, rise=70, wind=6, phase=i / 3, col=(250, 252, 255)) for i in range(3)] + \
           [puff_el("ch%d" % i, 717, 300, r=8, rise=50, wind=-8, phase=i / 2) for i in range(2)]
L1591_DIFFS = [("pine", 110, 300, 0), ("window", 290, 360, 0), ("nose", 794, 487, 0), ("scarf", 780, 504, 0), ("sled", 140, 548, 0),
               ("lamp", 400, 440, 0)]


# =================================================================== Level 1592 harbour town
def l1592(g, d):
    S.sky(g, [(0, (100, 170, 240)), (280, (220, 236, 250))])
    S.obj(g, cloud_shape(650, 70, 90, 24, 1), (255, 255, 255), 1, "cloud", line=False)
    S.water(g, Box(-2, 280, W + 2, H + 2), (90, 170, 230), (50, 120, 200), 2)
    # lighthouse on a far headland
    S.obj(g, Ell(820, 290, 110, 26), (130, 160, 110), 3, depth=0.3)
    S.obj(g, Poly([(806, 290), (834, 290), (828, 180), (812, 180)]), (250, 250, 250), 4, depth=0.3)
    for y in (200, 240):
        S.flat(g, Box(810, y, 830, y + 14), (220, 60, 60) if "light" not in d else (60, 100, 200))
    S.obj(g, Box(810, 166, 830, 182), (250, 230, 120), 5)
    S.obj(g, Poly([(806, 166), (820, 152), (834, 166)]), (220, 60, 60), 6)
    # sailing ship
    hull = Poly([(260, 380), (640, 380), (600, 450), (300, 450)])
    S.obj(g, hull, (140, 90, 50), 7, "wood")
    S.flat(g, Box(270, 392, 630, 400), (250, 220, 120))
    for x in (380, 520):
        S.obj(g, Box(x - 5, 120, x + 5, 380), (130, 90, 50), 8 + x, "wood")
    for x, top, w in ((380, 140, 90), (520, 160, 80)):
        sail = Poly([(x - w, top), (x + w, top), (x + w * 0.8, top + 180), (x - w * 0.8, top + 180)])
        S.obj(g, sail, (250, 246, 236), 10 + x, "fabric", hi=True)
    if "emblem" not in d:
        S.obj(g, Poly([(380 + math.cos(-math.pi / 2 + k * math.pi / 4) * (32 if k % 2 == 0 else 13),
                        230 + math.sin(-math.pi / 2 + k * math.pi / 4) * (32 if k % 2 == 0 else 13)) for k in range(8)]), (60, 110, 200), 12)
    S.obj(g, Poly([(521, 112), (560, 120) if "pennant" not in d else (540, 116), (521, 128)]), (60, 120, 210), 13)
    S.line(g, 520, 120, 520, 104, 2, (130, 90, 50))
    # pier and tavern
    S.obj(g, Box(-20, 460, 600, 490), (170, 120, 70), 14, "wood")
    for x in range(10, 600, 70):
        S.obj(g, Box(x, 490, x + 10, 600), (120, 80, 50), 15 + x, "wood")
    building(S, g, 640, 820, 330, 520, (230, 210, 180), seed=16, rows=2, cols=2, lit={(1, 0)}, roof=(150, 80, 60))
    S.line(g, 640, 430, 610, 430, 3, (100, 70, 50))
    sign_board(S, g, 584, 434, 636, 462, (190, 140, 80) if "sign" not in d else (120, 170, 120), seed=17, marks=2)
    S.ground(g, Box(600, 520, W + 2, H + 2), (200, 190, 170), "dirt", 18, line=True)
    for k in range(3 if "crate" not in d else 2):
        crate(S, g, 60 + k * 44, 460, 42, 36, seed=19 + k)
    barrel(S, g, 230, 460, seed=23)
    if "anchor" not in d:
        S.obj(g, Union([Box(860, 500, 866, 560), Ell(863, 560, 20, 8) - Ell(863, 556, 14, 6), Box(850, 508, 876, 513)]), (90, 90, 100), 24)
    hero(S, g, 380, 470, 100, face=1, seed=25)
    person(S, g, 700, 590, 120, (60, 100, 160), face=-1, seed=26, hat=(250, 250, 250))


L1592_EL = [bird_el("g1", 200, 120, s=9, speed=22, col=(250, 250, 250)), bird_el("g2", 700, 160, s=8, speed=-18, col=(250, 250, 250)),
            sparkle_el("waves", [(100, 330), (700, 360), (300, 560)], r=5, speed=0.5),
            cloud_el("cl", 300, 60, 70, 18, speed=5, seed=60)]
L1592_DIFFS = [("light", 820, 220, 0), ("emblem", 380, 230, 0), ("pennant", 540, 120, 0), ("sign", 610, 448, 0), ("crate", 150, 442, 0),
               ("anchor", 863, 530, 0)]


# =================================================================== Level 1593 crystal shrine
def l1593(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (40, 36, 80), 1, line=False)
    S.obj(g, Union([Poly([(-20, -2), (920, -2), (920, 80), (700, 140), (450, 90), (200, 150), (-20, 90)])]), (30, 26, 60), 2, "stone")
    # pillars
    for x, key in ((150, None), (300, None), (600, None), (750, "pillar")):
        top = 120 if not (key and key in d) else 260
        S.obj(g, Box(x - 26, top, x + 26, 470), (140, 140, 190), 3 + x, "stone")
        if top > 200:
            S.obj(g, Poly([(x - 26, top), (x - 10, top - 18), (x + 6, top - 4), (x + 26, top - 22), (x + 26, top + 4), (x - 26, top + 4)]), (140, 140, 190), 4 + x, "stone")
    S.ground(g, Box(-2, 460, W + 2, H + 2), (90, 90, 150), "stone", 5, line=True)
    # altar and floating crystal (the crystal bobs as an element)
    S.obj(g, Box(380, 380, 520, 470, 4), (170, 170, 210), 6, "stone")
    S.obj(g, Box(360, 370, 540, 386, 3), (190, 190, 230), 7, "stone")
    S.flat(g, Circ(450, 425, 22), (110, 110, 170))
    if "rune" not in d:
        S.flat(g, Diff(Circ(450, 425, 18), Circ(450, 425, 12)), (150, 230, 255))
        S.flat(g, Poly([(450, 410), (460, 432), (440, 432)]), (150, 230, 255))
    # glowing crystal clusters
    for x, base, hs, col, key in ((70, 470, (90, 60, 50), (120, 220, 255), None), (240, 470, (60, 44), (230, 120, 250), "cluster"),
                                  (660, 470, (70, 50), (120, 220, 255), None), (840, 470, (100, 70, 56), (140, 250, 200), None)):
        c = col if not (key and key in d) else (250, 200, 90)
        S.glow(g, x, base - 30, 90, c, 0.3)
        for k, h in enumerate(hs):
            crystal(S, g, x + (k - 1) * 22, base, h, c, seed=x + k, tilt=(k - 1) * 0.3)
    # pool
    S.water(g, Ell(170, 540, 130, 30), (80, 150, 230), (50, 100, 200), 8)
    torch(S, g, 560, 300, lit="torch" not in d)
    torch(S, g, 340, 300, lit=True)
    hero(S, g, 640, 590, 120, face=-1, seed=9)
    mage(S, g, 720, 596, 110, face=-1, seed=10)
    slime(S, g, 820, 590, 22, (230, 230, 120) if "slime" not in d else (230, 120, 160), seed=11, face=-1)


def l1593_crystal(g, m):
    S.glow(g, 450, 290, 120, (150, 230, 255), 0.45)
    crystal(S, g, 450, 330, 80, (150, 230, 255), seed=40)
    S.obj(g, Poly([(436, 330), (450, 352), (464, 330)]), (150, 230, 255), 41)


L1593_EL = [E("crystal", el(l1593_crystal), pivot=(450, 300), anim=dict(bobAmplitude=(0, 8), bobSpeed=0.3)),
            sparkle_el("sp1", [(100, 380), (250, 300), (670, 360), (830, 330), (450, 200)], col=(200, 240, 255), r=5, speed=0.6),
            E("fl1", el(lambda g, m: S.glow(g, 340, 286, 14, (255, 190, 90), 0.8)), anim=dict(pulse=0.15, scaleSpeed=2.0))]
L1593_DIFFS = [("pillar", 750, 190, 0), ("rune", 450, 425, 0), ("cluster", 240, 430, 0), ("torch", 560, 290, 0), ("slime", 820, 570, 0)]


# =================================================================== Level 1594 demon lord's castle
def l1594(g, d):
    S.sky(g, [(0, (30, 16, 50)), (300, (110, 40, 80))])
    S.glow(g, 160, 90, 80, (255, 120, 120), 0.4)
    S.obj(g, Circ(160, 90, 40), (230, 80, 90), 1, line=False)
    S.obj(g, Poly([(380, 330), (450, 260), (820, 250), (900, 330)]), (40, 30, 50), 2, "stone")
    castle(S, g, 640, 260, 300, 240, (80, 70, 100), (60, 30, 80), seed=3, flags=((150, 30, 40), (150, 30, 40) if "flag" not in d else None))
    for x, y, key in ((640, 120, "window"), (560, 200, None), (720, 200, None)):
        lit = not (key and key in d)
        S.obj(g, Union([Box(x - 8, y, x + 8, y + 24), Circ(x, y, 8)]), (255, 200, 90) if lit else (30, 20, 40), 4 + x)
        if lit:
            S.glow(g, x, y + 10, 30, (255, 170, 80), 0.3)
    # the dark lord on the balcony
    if "lord" not in d:
        S.obj(g, Union([Poly([(626, 180), (654, 180), (664, 230), (616, 230)]), Circ(640, 170, 12),
                        Poly([(630, 162), (622, 140), (636, 158)]), Poly([(650, 162), (658, 140), (644, 158)])]), (20, 10, 30), 5)
        S.flat(g, Circ(636, 170, 2), (255, 60, 60))
        S.flat(g, Circ(644, 170, 2), (255, 60, 60))
    # lava moat and bridge
    lava = Box(-2, 360, W + 2, 460)
    S.obj(g, lava, (240, 110, 40), 6, line=False)
    S.glow(g, 450, 400, 400, (255, 120, 40), 0.25)
    for x in range(20, 900, 90):
        S.flat(g, Ell(x, 400 + (x % 3) * 15, 26, 6), (255, 210, 90))
    if "rock" not in d:
        rock(S, g, 160, 430, 34, col=(70, 50, 60), seed=7)
    S.obj(g, Poly([(380, 340), (520, 340), (560, 470), (340, 470)]), (100, 90, 110), 8, "stone")
    S.ground(g, Box(-2, 460, W + 2, H + 2), (70, 60, 80), "stone", 9, line=True)
    torch(S, g, 360, 300, lit=True)
    torch(S, g, 540, 300, lit="torch" not in d)
    # the party at the gate
    hero(S, g, 420, 590, 130, face=1, seed=10, shield=(60, 90, 180))
    mage(S, g, 340, 596, 120, face=1, seed=11)
    hero(S, g, 520, 596, 120, tunic=(240, 240, 240), cape=(90, 170, 220), hair=(170, 90, 60), face=1, seed=12, sword=False, hair_spiky=False)
    goblin(S, g, 760, 590, 120, skin=(150, 120, 180), cloth=(60, 40, 70), face=-1, seed=13, weapon="axe" not in d)


L1594_EL = [E("flash", el(lambda g, m: g.fill(Poly([(820, -2), (790, 60), (810, 64), (770, 140), (840, 50), (818, 46), (850, -2)]), (255, 250, 220))),
              daynight="untinted", anim=dict(blinkInterval=4.0, blinkDuration=0.4)),
            sparkle_el("ember", [(200, 380), (600, 420), (760, 390)], col=(255, 220, 120), r=5, speed=0.8),
            E("f1", el(lambda g, m: S.glow(g, 360, 286, 14, (255, 190, 90), 0.8)), anim=dict(pulse=0.15, scaleSpeed=2.0))]
L1594_DIFFS = [("flag", 768, 50, 0), ("window", 640, 124, 0), ("lord", 640, 186, 0), ("rock", 160, 412, 0), ("torch", 540, 290, 0),
               ("axe", 790, 510, 0)]

LEVELS = [
    ("Level1585", "启程之村", make(l1585), L1585_EL, L1585_DIFFS, 60, OPTS),
    ("Level1586", "王城谒见", make(l1586), L1586_EL, L1586_DIFFS, 60, OPTS),
    ("Level1587", "史莱姆之战", make(l1587), L1587_EL, L1587_DIFFS, 60, OPTS),
    ("Level1588", "迷雾森林", make(l1588), L1588_EL, L1588_DIFFS, 60, OPTS),
    ("Level1589", "飞空艇甲板", make(l1589), L1589_EL, L1589_DIFFS, 60, OPTS),
    ("Level1590", "沙漠绿洲城", make(l1590), L1590_EL, L1590_DIFFS, 60, OPTS),
    ("Level1591", "雪山村落", make(l1591), L1591_EL, L1591_DIFFS, 60, OPTS),
    ("Level1592", "港口城镇", make(l1592), L1592_EL, L1592_DIFFS, 60, OPTS),
    ("Level1593", "水晶神殿", make(l1593), L1593_EL, L1593_DIFFS, 60, OPTS),
    ("Level1594", "魔王城", make(l1594), L1594_EL, L1594_DIFFS, 60, OPTS),
]
