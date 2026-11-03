# -*- coding: utf-8 -*-
"""American-comic tabletop-fantasy interiors, set 2 - following the five-star favourites (tavern, dungeon corridor,
wizard's study). Original adventurers, no readable text, no gore.
  Level1640 矮人锻造坊 - a dwarven forge under the mountain: furnace, anvil, weapon racks, mine cart, smiths at work
  Level1641 盗贼密室   - a thieves' hideout: map table with dice, loot sacks, lock-picks, a trapdoor, a lookout
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Poly, Rough, Seg, Union, el, mixc
from levels_dnd import INK, OPTS, S, adventurer, burst, d20, make, stone_arch
from styled_kit import barrel, chest, coin_pile, crate, potion, sparkle_el, torch


# =================================================================== Level 1640 dwarven forge
def l1640(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (70, 56, 54), 1, "stone", line=False)
    stone_arch(g, 120, 780, 160, 470, (110, 96, 90), 2)
    # furnace (centre back) with glowing mouth
    S.obj(g, Union([Box(330, 150, 570, 440), Poly([(330, 152), (450, 80), (570, 152)])]), (130, 110, 100), 3, "stone")
    S.obj(g, Box(430, -2, 470, 90), (110, 92, 86), 4, "stone")
    S.glow(g, 450, 360, 160, (255, 140, 50), 0.6)
    S.obj(g, Union([Box(380, 300, 520, 440), Circ(450, 300, 70) & Box(380, 230, 520, 300)]), (255, 150, 50), 5)
    S.obj(g, Union([Box(400, 330, 500, 440), Circ(450, 330, 50) & Box(400, 280, 500, 330)]), (255, 220, 120), 6, line=False)
    # floor
    S.ground(g, Box(-2, 440, W + 2, H + 2), (90, 76, 70), "stone", 7, line=True)
    # anvil with a glowing blade
    S.obj(g, Union([Poly([(520, 500), (660, 500), (680, 484), (560, 480), (500, 486)]), Box(560, 500, 620, 540), Box(540, 540, 640, 556)]), (60, 60, 70), 8, hi=True)
    S.obj(g, Poly([(560, 478), (660, 472), (664, 478), (560, 484)]), (255, 160, 60) if "blade" not in d else (180, 190, 210), 9)
    # weapon rack (left)
    S.obj(g, Box(40, 200, 230, 216), (130, 90, 50), 10, "wood")
    S.obj(g, Box(40, 330, 230, 346), (130, 90, 50), 11, "wood")
    for i, x in enumerate((70, 120, 170, 210)):
        if "axe" in d and i == 1:
            continue
        S.obj(g, Seg(x, 190, x, 350, 3.5), (140, 100, 60), 12 + i)
        if i % 2 == 0:
            S.obj(g, Poly([(x, 200), (x + 26, 186), (x + 30, 226), (x, 222)]), (190, 196, 210), 16 + i, hi=True)
        else:
            S.obj(g, Union([Box(x - 14, 196, x + 14, 216, 3)]), (150, 150, 160), 16 + i, hi=True)
    # shield on the wall (right) and a hanging chain hoist
    S.obj(g, Union([Circ(780, 260, 46)]), (160, 50, 50) if "shield" not in d else (60, 110, 170), 20, hi=True)
    S.flat(g, Circ(780, 260, 14), (230, 190, 70))
    for k in range(12):
        S.obj(g, Ell(660, 20 + k * 14, 5, 8) - Ell(660, 20 + k * 14, 2, 5), (120, 120, 130), 21)
    S.obj(g, Poly([(648, 190), (672, 190), (660, 214)]), (120, 120, 130), 22)
    # mine cart with ore and crystals
    S.obj(g, Poly([(700, 470), (860, 470), (840, 540), (720, 540)]), (110, 90, 80), 23, hi=True)
    for wx in (740, 820):
        S.obj(g, Circ(wx, 548, 14), (60, 60, 66), 24)
    for k, (x, y, c) in enumerate(((730, 466, (90, 200, 230)), (770, 460, (230, 90, 160)), (810, 466, (90, 200, 230)))):
        if "gem" in d and k == 1:
            c = (250, 210, 60)
        S.obj(g, Poly([(x - 12, y + 8), (x, y - 22), (x + 12, y + 8)]), c, 25 + k, hi=True)
    # dwarves (fighter archetype, short and bearded) and a barrel
    adventurer(g, 320, 600, 190, kind="fighter", main=(140, 70, 40), trim=(150, 150, 160), face=1, seed=30, beard=True, hair=(170, 90, 40),
               weapon=False)
    S.obj(g, Seg(360, 470, 410, 420, 4), (140, 100, 60), 31)
    S.obj(g, Box(400, 404, 430, 426, 3), (110, 110, 120), 32)
    adventurer(g, 470, 600, 180, kind="fighter", main=(60, 90, 70), trim=(150, 150, 160), face=1, seed=33, beard=True,
               hair=(220, 220, 220) if "beard" not in d else (200, 80, 40), weapon=False)
    barrel(S, g, 120, 560, r=26, h=60, seed=34)
    if "bucket" not in d:
        S.obj(g, Union([Box(200, 520, 240, 560, 4), Seg(200, 520, 240, 520, 2)]), (120, 120, 130), 35, hi=True)
        S.flat(g, Ell(220, 522, 18, 4), (110, 160, 220))
    burst(g, 600, 462, 16, col=(255, 230, 90), seed=36)


L1640_EL = [
    E("sparks", el(lambda g, m: [g.glow(610 + k * 10, 460 - k * 12, 3, (255, 210, 100), 1.0) for k in range(5)]), daynight="untinted",
      anim=dict(driftVelocity=(10, 70), driftLength=80, driftFade=True)),
    E("fire", el(lambda g, m: S.obj(g, Union([Ell(450, 420, 50, 16), Poly([(404, 424), (424, 360), (450, 390), (474, 350), (496, 424)])]), (255, 190, 80), 40, line=False)),
      pivot=(450, 430), daynight="untinted", anim=dict(stretch=(0.06, 0.25), scaleSpeed=2.2)),
    E("hammer", el(lambda g, m: S.obj(g, Union([Seg(660, 360, 640, 430, 4), Box(626, 420, 660, 440, 3)]), (120, 120, 130), 41)), pivot=(660, 360),
      anim=dict(swingAngle=14, swingSpeed=0.8)),
]
L1640_DIFFS = [("blade", 612, 478, 0), ("axe", 125, 270, 0), ("shield", 780, 260, 0), ("gem", 770, 452, 0), ("beard", 472, 430, 0), ("bucket", 220, 540, 0)]


# =================================================================== Level 1641 thieves' hideout
def l1641(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (60, 50, 60), 1, "stone", line=False)
    for x in range(0, 900, 70):
        S.obj(g, Box(x, -2, x + 8, 430), (80, 60, 50), 2 + x, "wood")
    S.obj(g, Box(-2, 40, W + 2, 56), (90, 66, 50), 3, "wood")
    # wanted-style posters (no text: silhouettes) and a dartboard
    for i, (x, c) in enumerate(((90, (230, 210, 170)), (190, (220, 200, 160)))):
        S.obj(g, Box(x, 100, x + 70, 190), c, 10 + i)
        S.flat(g, Union([Circ(x + 35, 130, 14), Box(x + 18, 146, x + 52, 180, 6)]), (90, 70, 60) if not ("poster" in d and i == 1) else (160, 60, 60))
    S.obj(g, Circ(760, 150, 44), (40, 40, 50), 12)
    for r, c in ((36, (230, 220, 200)), (26, (200, 50, 50)), (16, (230, 220, 200)), (7, (200, 50, 50))):
        S.flat(g, Circ(760, 150, r), c)
    if "dart" not in d:
        S.obj(g, Seg(774, 140, 800, 120, 2), (60, 120, 200), 13)
    # floor and rug with a trapdoor
    S.ground(g, Box(-2, 430, W + 2, H + 2), (110, 80, 60), "wood", 14, line=True)
    S.obj(g, Poly([(560, 520), (720, 510), (760, 580), (540, 590)]), (130, 100, 70), 15, "wood")
    S.obj(g, Circ(660, 552, 6), (200, 170, 80) if "ring" not in d else (60, 60, 70), 16)
    # map table with dice, candle and dagger
    S.obj(g, Ell(390, 470, 190, 44), (130, 90, 56), 17, "wood")
    for x in (290, 490):
        S.obj(g, Box(x - 10, 480, x + 10, 580), (110, 74, 46), 18, "wood")
    S.obj(g, Poly([(290, 450), (470, 444), (480, 476), (286, 482)]), (240, 220, 170), 19)
    S.flat(g, Seg(310, 470, 450, 456, 1.6), (200, 60, 60))
    S.flat(g, Circ(452, 456, 5), (200, 60, 60))
    d20(g, 520, 460, 14, (60, 160, 90) if "dice" not in d else (220, 40, 60))
    S.obj(g, Poly([(230, 476), (300, 462), (304, 468), (234, 482)]), (210, 216, 226), 20, hi=True)
    S.obj(g, Box(330, 420, 340, 446), (250, 245, 230), 21)
    S.glow(g, 335, 410, 40, (255, 200, 110), 0.4)
    # loot: sacks, chest, coins, goblet
    for x, c in ((90, (170, 140, 90)), (150, (160, 130, 80))):
        S.obj(g, Union([Ell(x, 540, 34, 40), Poly([(x - 10, 500), (x, 486), (x + 10, 500)])]), c, 22, "fabric", hi=True)
    chest(S, g, 230, 580, 64, open_=True, seed=23)
    if "coins" not in d:
        coin_pile(S, g, 320, 590, 70, seed=24)
    S.obj(g, Union([Poly([(830, 470), (860, 470), (852, 500), (838, 500)]), Box(842, 500, 848, 516), Box(832, 514, 858, 520)]),
          (250, 210, 60) if "goblet" not in d else (190, 190, 200), 25, hi=True)
    # lock-pick roll on the shelf, lookout at the window
    S.obj(g, Box(560, 220, 700, 232), (110, 80, 56), 26, "wood")
    S.obj(g, Box(570, 196, 640, 220, 4), (120, 60, 50), 27)
    for k in range(5):
        S.flat(g, Seg(578 + k * 12, 200, 578 + k * 12, 216, 1.4), (200, 200, 210))
    S.obj(g, Box(400, 90, 520, 200, 4), (30, 30, 60), 28)
    S.flat(g, Circ(486, 120, 14), (240, 240, 210))
    S.flat(g, Union([Box(458, 90, 462, 200), Box(400, 143, 520, 147)]), (80, 60, 50))
    adventurer(g, 470, 420, 190, kind="rogue", face=1, seed=29, main=(50, 70, 50))
    adventurer(g, 720, 600, 230, kind="rogue", face=-1, seed=30, main=(90, 40, 60) if "cloak" not in d else (40, 80, 120))


L1641_EL = [E("flame", el(lambda g, m: S.obj(g, Union([Ell(335, 414, 5, 6), Poly([(330, 414), (335, 396), (340, 414)])]), (255, 190, 80), 40, line=False)),
              pivot=(335, 420), daynight="untinted", anim=dict(stretch=(0.06, 0.25), scaleSpeed=2.0)),
            sparkle_el("loot", [(230, 540), (320, 572), (845, 480)], col=(255, 250, 200), r=6, speed=0.6),
            E("cat", el(lambda g, m: S.obj(g, Union([Ell(620, 214, 18, 10), Circ(640, 204, 8)]), (60, 56, 60), 42)), pivot=(620, 220),
              anim=dict(bobAmplitude=(0, 2), bobSpeed=0.4))]
L1641_DIFFS = [("poster", 225, 160, 0), ("dart", 787, 130, 0), ("ring", 660, 552, 0), ("dice", 520, 460, 0), ("coins", 320, 578, 0),
               ("goblet", 845, 494, 0), ("cloak", 700, 470, 0)]


LEVELS = [
    ("Level1640", "矮人锻造坊", make(l1640), L1640_EL, L1640_DIFFS, 60, OPTS),
    ("Level1641", "盗贼密室", make(l1641), L1641_EL, L1641_DIFFS, 60, OPTS),
]
