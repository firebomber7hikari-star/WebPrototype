# -*- coding: utf-8 -*-
"""Inside video games, part 5 (all designs original: no real games, characters, brands or logos):
  Level205 银河城地图 - a pixel underground base cross-section: rooms, coloured doors, save station, elevator, room map
  Level206 浮岛平台   - isometric floating islands: bridges, springs, stars, windmill, chest, clouds below
  Level207 餐厅经营   - a restaurant sim front hall: tables with customers and wish bubbles, waiter, menu board
  Level208 医院经营   - a two-floor hospital sim: reception, waiting room, exam room, scanner, pharmacy, lift
  Level209 火星基地   - a Mars colony builder: greenhouse domes, habitat modules, rover, rocket pad, resource bars
  Level210 家居设计   - a top-down home-design game: room plan with furniture, catalog panel, tool bar
  Level211 卡车驾驶   - a truck-driving sim cab: highway through the windscreen, wheel, gauges, GPS, dashboard toy
  Level212 合成游戏   - a merge game board: item chains on a grid, order cards, energy, chests
  Level213 派对棋盘   - a party board game: island path of spaces, player pieces, dice, star shop, player panels
  Level214 文字冒险   - a retro text adventure on a green monochrome monitor, floppies and notes on the desk
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from stylekit import flame
from levels_retro import block, digits, sprite
from levels_gamecontent import OUTLINE, glyph_line, toon
from levels_gamecontent2 import P, bar, chibi, iso_box, iso_house, iso_tree, rot_poly
from levels_gamecontent3 import heart, panel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 220, 190)


# =================================================================== Level 205 metroidvania base
ROOMS = [(20, 60, 300, 230), (300, 60, 600, 230), (600, 60, 880, 230), (20, 230, 220, 420), (220, 230, 680, 420), (680, 230, 880, 420),
         (20, 420, 450, 580), (450, 420, 880, 580)]
TINTS = [(40, 50, 80), (50, 40, 70), (40, 60, 70), (60, 40, 60), (40, 50, 80), (50, 60, 50), (60, 50, 40), (40, 50, 70)]


def l205_bg(c, d):
    c.rect(0, 0, W, H, (20, 18, 30))
    for k, (x0, y0, x1, y1) in enumerate(ROOMS):
        col = TINTS[k]
        flat(c, RRect(x0 + 8, y0 + 8, x1 - 8, y1 - 8, 0), col)
        for x in range(int(x0) + 8, int(x1) - 8, 24):
            flat(c, Thick(x, y0 + 8, x, y1 - 8, 1), lit(col, 1.15))
    # walls/floors as pixel blocks
    for x0, y0, x1, y1 in ROOMS:
        for x in range(int(x0), int(x1), 20):
            block(c, x, y1 - 10, 20, (110, 104, 130), kind="stone")
    for x in range(0, W, 20):
        block(c, x, 40, 20, (110, 104, 130), kind="stone")
    # platforms
    for x0, x1, y in ((60, 180, 160), (380, 520, 150), (680, 800, 170), (260, 400, 350), (520, 640, 330), (100, 300, 510), (560, 760, 500)):
        for x in range(x0, x1, 20):
            block(c, x, y, 20, (140, 134, 160), kind="stone")
    # coloured doors between rooms
    for k, (x, y, col) in enumerate(((290, 160, (220, 60, 60)), (590, 160, (60, 120, 220)), (210, 350, (250, 200, 60)), (670, 350, (90, 200, 120)), (440, 510, (220, 60, 60)))):
        if k == 1 and "door" in d:
            col = (220, 120, 220)
        flat(c, RRect(x, y, x + 20, y + 60, 0), col)
        flat(c, RRect(x + 4, y + 6, x + 16, y + 54, 0), lit(col, 0.7))
    # save station
    save = (90, 220, 240) if "save" not in d else (250, 160, 60)
    sprite(c, 740, 362, ["..####..", ".#....#.", "#..##..#", "#.####.#", "#..##..#", ".#....#.", "########"], {"#": save}, 6)
    # elevator shaft
    flat(c, RRect(140, 240, 180, 410, 0), (30, 28, 44))
    flat(c, [Thick(140, 240, 140, 410, 2), Thick(180, 240, 180, 410, 2)], (150, 150, 170))
    flat(c, RRect(140, 330, 180, 346, 0), (200, 200, 216))
    # item orb + crystal plant
    sprite(c, 430, 100, ["..##..", ".####.", "######", "######", ".####.", "..##.."], {"#": (250, 120, 200) if "orb" not in d else (120, 250, 140)}, 6)
    crystal = (120, 200, 250) if "crystal" not in d else (250, 220, 90)
    for dx, h in ((-12, 30), (0, 46), (14, 26)):
        flat(c, Poly([(820 + dx - 6, 220), (820 + dx + 6, 220), (820 + dx, 220 - h)]), crystal)
    # pipes, hero
    flat(c, [Thick(240, 450, 240, 570, 6), Thick(240, 470, 420, 470, 6)], (90, 90, 110))
    sprite(c, 300, 460, ["..hhh...", ".hhhhh..", ".hssss..", ".sesse..", "..ssss..", ".bbbbbb.", "sbbbbbbs", ".bbbbbb.", ".ll..ll.", ".kk..kk."],
           {"h": (240, 120, 60), "s": (250, 210, 170), "e": (30, 30, 40), "b": (60, 110, 210), "l": (60, 60, 80), "k": (90, 60, 40)}, 5)
    # HUD + room map
    flat(c, RRect(0, 0, W, 40, 0), (14, 12, 22))
    bar(c, 20, 12, 220, 28, 0.7, (220, 60, 70))
    bar(c, 240, 12, 360, 28, 0.5, (60, 120, 230))
    for k, (x0, y0, x1, y1) in enumerate(ROOMS):
        col = (90, 200, 240) if k != 4 else (250, 250, 250)
        if k == 6 and "map" in d:
            col = (70, 70, 90)
        flat(c, RRect(700 + x0 / 6, 4 + y0 / 18, 700 + x1 / 6 - 2, 4 + y1 / 18 - 2, 1), col)


L205_ELEMENTS = [
    E("saveglow", lambda c, m: soft_union(c, [Circ(764, 384, 20)], (120, 220, 255), 0.4, spread=24), daynight="untinted", anim=dict(pulse=0.2, scaleSpeed=0.8)),
    E("lift", lambda c, m: flat(c, RRect(140, 320, 180, 330, 0), (250, 220, 90)), anim=dict(bobAmplitude=(0, 60), bobSpeed=0.15)),
    E("drip", lambda c, m: flat(c, RRect(620, 70, 624, 78, 0), (120, 180, 250)), anim=dict(driftVelocity=(0, -120), driftLength=150, driftFade=True)),
    E("bat", lambda c, m: sprite(c, 560, 260, ["#.....#", "##.#.##", "#######", ".#.#.#."], {"#": (90, 60, 120)}, 4), anim=dict(orbitRadius=(40, 16), orbitSpeed=0.3)),
]

L205_DIFFS = [
    ("door", 600, 190, 0),
    ("save", 764, 384, 0),
    ("orb", 448, 118, 0),
    ("crystal", 820, 200, 0),
    ("map", 736, 32, 0),
]


# =================================================================== Level 206 floating islands
def float_island(c, i, j, w, dd, grass=(110, 200, 90), rock=(150, 120, 100), depth=50):
    a, b, cc, dd_ = P(i, j), P(i + w, j), P(i + w, j + dd), P(i, j + dd)
    tip = ((a[0] + cc[0]) / 2, (a[1] + cc[1]) / 2 + depth + (w + dd) * 8)
    toon(c, Poly([dd_, cc, tip]), lit(rock, 0.85), w=1.4, shadow=None)
    toon(c, Poly([cc, b, tip]), lit(rock, 0.7), w=1.4, shadow=None)
    toon(c, Poly([a, b, cc, dd_]), grass, w=1.6, shadow=None)
    return ((a[0] + cc[0]) / 2, (a[1] + cc[1]) / 2)


def l206_bg(c, d):
    c.gradient(0, H, (140, 200, 250), (230, 240, 250))
    for x, y, k in ((120, 520, 1.2), (480, 560, 1.4), (800, 500, 1.1), (300, 440, 0.8)):
        flat(c, [Ell(x, y, 90 * k, 26 * k), Ell(x + 40 * k, y - 16 * k, 50 * k, 22 * k), Ell(x - 50 * k, y - 8 * k, 40 * k, 18 * k)], (250, 250, 255))
    islands = [(8, 10, 4, 4), (16, 8, 3, 3), (20, 15, 4, 3), (12, 18, 3, 3), (24, 22, 3, 4)]
    centres = [float_island(c, *isl) for isl in islands]
    # bridges
    for a, b in ((0, 1), (1, 2), (0, 3), (2, 4)):
        flat(c, Thick(*centres[a], *centres[b], 8), (180, 130, 80))
        flat(c, Thick(*centres[a], *centres[b], 3), (210, 160, 110))
    # windmill on island 0
    x, y = centres[0]
    toon(c, Poly([(x - 18, y), (x + 18, y), (x + 10, y - 70), (x - 10, y - 70)]), (240, 236, 220), w=1.6, shadow=None)
    toon(c, Poly([(x - 14, y - 66), (x + 14, y - 66), (x, y - 90)]), (200, 80, 70), w=1.4, shadow=None)
    # house on island 2
    iso_house(c, 21, 15.5, (250, 240, 220), (80, 130, 210) if "roof" not in d else (220, 140, 60))
    # trees
    for i, j in ((16.5, 8.5), (9, 12.5), (13, 19), (25, 23)):
        iso_tree(c, i, j, (70, 160, 80) if not ((i, j) == (9, 12.5) and "tree" in d) else (230, 140, 50))
    # spring + chest + crystal + flag
    x, y = centres[3]
    toon(c, [RRect(x + 6, y - 22, x + 44, y - 4, 5)], (250, 200, 60) if "spring" not in d else (220, 80, 200), w=1.4, shadow=None)
    for k in range(3):
        flat(c, Thick(x + 12, y - 6 + k * -4, x + 34, y - 6 + k * -4, 1.6), (90, 90, 100))
    x, y = centres[1]
    toon(c, [RRect(x - 20, y - 24, x + 20, y, 4), RRect(x - 20, y - 32, x + 20, y - 20, 8)], (170, 110, 50) if "chest" not in d else (110, 110, 200), w=1.4,
         shadow=None)
    flat(c, RRect(x - 4, y - 24, x + 4, y - 14, 1), (250, 200, 60))
    x, y = centres[4]
    flat(c, Thick(x, y, x, y - 70, 3), (220, 220, 230))
    toon(c, Poly([(x, y - 74), (x + 46, y - 60), (x, y - 44)]), (220, 60, 70) if "flag" not in d else (60, 160, 220), w=1.2, shadow=None)
    # character on island 0
    chibi(c, centres[0][0] + 50, centres[0][1] + 10, s=0.7, hair=(240, 120, 60), outfit=(220, 60, 70), face=1)
    # HUD
    panel(c, 14, 12, 190, 52, (40, 50, 80))
    toon(c, Poly(star_pts(38, 32, 13, 6)), (250, 210, 60), w=1.2, shadow=None)
    digits(c, 60, 20, "12", (250, 250, 250), 5)
    digits(c, 114, 20, "40", (180, 190, 220), 5)


def star_el(k, x, y):
    return E("star%d" % k, lambda c, m: toon(c, Poly(star_pts(x, y, 13, 6)), (250, 210, 60), w=1.2, shadow=None), pivot=(x, y), daynight="untinted",
             anim=dict(spinSpeed=0.8, phase=k * 0.2, bobAmplitude=(0, 4), bobSpeed=0.5))


L206_ELEMENTS = [star_el(k, x, y) for k, (x, y) in enumerate(((560, 200), (620, 250), (330, 330), (700, 400)))] + [
    E("blades", lambda c, m: toon(c, [Thick(P(10, 12)[0], P(10, 12)[1] - 120, P(10, 12)[0], P(10, 12)[1] - 40, 7),
                                      Thick(P(10, 12)[0] - 40, P(10, 12)[1] - 80, P(10, 12)[0] + 40, P(10, 12)[1] - 80, 7)], (200, 170, 120), w=1.2, shadow=None),
      pivot=(P(10, 12)[0], P(10, 12)[1] - 80), anim=dict(rotateSpeed=50)),
    E("platform", lambda c, m: (toon(c, Poly([P(17, 20), P(19, 20), P(19, 22), P(17, 22)]), (180, 140, 100), w=1.4, shadow=None),),
      anim=dict(bobAmplitude=(0, 30), bobSpeed=0.2)),
    E("cloud", lambda c, m: flat(c, [Ell(200, 70, 60, 16), Ell(230, 60, 34, 14)], (250, 250, 255, 0.9)), anim=drift_across(140, 260, 8, start=120)),
]

_c1 = ((P(16, 8)[0] + P(19, 11)[0]) / 2, (P(16, 8)[1] + P(19, 11)[1]) / 2)
_c3 = ((P(12, 18)[0] + P(15, 21)[0]) / 2, (P(12, 18)[1] + P(15, 21)[1]) / 2)
_c4 = ((P(24, 22)[0] + P(27, 26)[0]) / 2, (P(24, 22)[1] + P(27, 26)[1]) / 2)
L206_DIFFS = [
    ("roof", P(21.5, 16)[0], P(21.5, 16)[1] - 30, 0),
    ("tree", P(9.5, 13)[0], P(9.5, 13)[1] - 22, 0),
    ("spring", _c3[0] + 23, _c3[1] - 10, 0),
    ("chest", _c1[0], _c1[1] - 16, 0),
    ("flag", _c4[0] + 16, _c4[1] - 60, 0),
]


# =================================================================== Level 207 restaurant sim
def table(c, x, y, cloth):
    toon(c, Ell(x, y, 60, 18), cloth, w=1.6)
    flat(c, Ell(x, y - 2, 50, 12), lit(cloth, 1.12))
    flat(c, [Thick(x - 40, y + 10, x - 44, y + 50, 4), Thick(x + 40, y + 10, x + 44, y + 50, 4)], (120, 80, 50))


def wish(c, x, y, kind):
    toon(c, [Ell(x, y, 30, 22), Circ(x - 18, y + 26, 5)], (250, 250, 250), w=1.4, shadow=None)
    if kind == "cake":
        toon(c, [RRect(x - 12, y - 6, x + 12, y + 10, 3)], (250, 200, 220), w=1, shadow=None)
        flat(c, Circ(x, y - 8, 3), (230, 60, 60))
    elif kind == "noodle":
        toon(c, Ell(x, y + 4, 14, 8), (240, 240, 246), w=1, shadow=None)
        flat(c, [Thick(x - 8, y + 2, x + 8, y - 2, 2), Thick(x - 8, y + 6, x + 8, y + 2, 2)], (240, 200, 110))
    else:
        toon(c, [Thick(x, y + 10, x, y - 2, 4), Ell(x, y - 8, 10, 6)], (120, 80, 50), w=1, shadow=None)


def l207_bg(c, d):
    c.rect(0, 0, W, 380, (250, 230, 200))
    for x in range(0, W, 50):
        flat(c, RRect(x, 0, x + 25, 380, 0), (250, 222, 190))
    flat(c, RRect(0, 340, W, 380, 0), (180, 120, 80))
    # kitchen window + cashier counter (back)
    toon(c, RRect(560, 60, 860, 220, 6), (180, 130, 90), w=2)
    flat(c, RRect(574, 74, 846, 206, 4), (230, 236, 240))
    chibi(c, 700, 210, s=0.9, hair=(60, 50, 50), outfit=(250, 250, 250), face=-1)
    toon(c, RRect(560, 220, 860, 340, 4), (150, 100, 70), w=2)
    toon(c, RRect(780, 190, 840, 222, 4), (200, 200, 210), w=1.4, shadow=None)
    # menu board
    menu = (60, 70, 60) if "menu" not in d else (90, 60, 110)
    toon(c, RRect(60, 60, 260, 200, 6), menu, w=2)
    for k in range(4):
        glyph_line(c, 80, 240 - k * 20, 90 + k * 28, (250, 250, 240), 2070 + k, w=2, size=10)
    # lamps
    for k, x in enumerate((180, 450)):
        flat(c, Thick(x, 0, x, 40, 2), (90, 80, 70))
        toon(c, Poly([(x - 30, 70), (x + 30, 70), (x + 18, 40), (x - 18, 40)]), (240, 180, 70) if not (k == 1 and "lamp" in d) else (90, 170, 220), w=1.4, shadow=None)
    # door + plant
    toon(c, RRect(330, 120, 410, 340, 4), (150, 100, 70), w=2)
    flat(c, RRect(342, 136, 398, 230, 3), (180, 220, 240))
    plant = (80, 150, 90) if "plant" not in d else (220, 140, 60)
    toon(c, Poly([(470, 340), (520, 340), (512, 300), (478, 300)]), (190, 110, 70), w=1.4, shadow=None)
    toon(c, [Ell(482, 270, 14, 34), Ell(508, 270, 14, 34), Ell(495, 260, 12, 40)], plant, w=1.4, shadow=None)
    # floor
    c.rect(0, 380, W, H, (200, 160, 120))
    for y in range(380, H, 30):
        for x in range((y // 30 % 2) * 30, W, 60):
            flat(c, RRect(x, y, x + 30, y + 30, 0), (210, 172, 132))
    # tables with customers + wish bubbles
    for k, (x, cloth, kind) in enumerate(((150, (220, 80, 80), "cake"), (450, (80, 140, 210), "noodle"), (750, (90, 170, 110), "drink"))):
        if k == 0 and "cloth" in d:
            cloth = (250, 200, 60)
        chibi(c, x - 50, 470, s=0.8, hair=[(240, 200, 90), (60, 50, 50), (150, 90, 40)][k], outfit=[(200, 120, 200), (90, 180, 120), (240, 140, 60)][k], face=1)
        chibi(c, x + 50, 470, s=0.8, hair=[(90, 60, 40), (230, 120, 160), (40, 40, 50)][k], outfit=[(90, 140, 220), (250, 200, 80), (120, 120, 140)][k], face=-1)
        table(c, x, 490, cloth)
        wish(c, x + 70, 370, kind if not (k == 1 and "wish" in d) else "cake")
    # HUD
    panel(c, 14, 548, 200, 594, (60, 50, 50))
    flat(c, Circ(38, 571, 12), (250, 200, 60) if "coins" not in d else (90, 200, 240))
    digits(c, 60, 560, "3480", (250, 250, 250), 5)
    panel(c, 700, 548, 886, 594, (60, 50, 50))
    toon(c, Circ(724, 571, 13), (250, 210, 80), w=1.2, shadow=None)
    bar(c, 746, 564, 870, 578, 0.75, (90, 210, 110))


L207_ELEMENTS = [
    E("waiter", lambda c, m: (chibi(c, 300, 560, s=0.9, hair=(40, 40, 50), outfit=(40, 40, 56), face=1),
                              toon(c, Ell(330, 500, 30, 7), (220, 220, 230), w=1.2, shadow=None)), anim=dict(bobAmplitude=(40, 3), bobSpeed=0.15)),
    E("steam", lambda c, m: toon(c, Circ(810, 186, 6), (246, 246, 250), w=1, shadow=None), anim=dict(driftVelocity=(3, 24), driftLength=50, driftFade=True)),
    E("heart", lambda c, m: heart(c, 760, 330, 1.2, (250, 110, 140)), daynight="untinted", anim=dict(driftVelocity=(0, 30), driftLength=50, driftFade=True)),
    E("glow", lambda c, m: [soft_union(c, [Ell(x, 74, 30, 10)], (255, 230, 150), 0.4, spread=20) for x in (180, 450)], daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.4)),
]

L207_DIFFS = [
    ("menu", 160, 130, 0),
    ("lamp", 450, 56, 0),
    ("plant", 495, 270, 0),
    ("cloth", 150, 490, 0),
    ("wish", 520, 370, 0),
    ("coins", 38, 571, 0),
]


# =================================================================== Level 208 hospital sim
def l208_bg(c, d):
    c.rect(0, 0, W, H, (60, 70, 90))
    # two floors
    for y0, y1 in ((30, 290), (300, 560)):
        flat(c, RRect(20, y0, 880, y1, 0), (230, 240, 240))
        flat(c, RRect(20, y1 - 20, 880, y1, 0), (180, 200, 210))
    flat(c, RRect(0, 560, W, H, 0), (110, 120, 130))
    for x in (300, 600):
        flat(c, RRect(x, 30, x + 10, 290, 0), (180, 190, 200))
        flat(c, RRect(x, 300, x + 10, 560, 0), (180, 190, 200))
    # top floor: exam room, scanner, ward bed
    toon(c, [RRect(60, 210, 230, 236, 4), RRect(70, 236, 80, 270, 2), RRect(210, 236, 220, 270, 2)], (200, 200, 210), w=1.6, shadow=None)
    sheet = (150, 210, 240) if "sheet" not in d else (240, 170, 200)
    toon(c, RRect(66, 196, 224, 214, 5), sheet, w=1.2, shadow=None)
    toon(c, RRect(80, 70, 220, 160, 6), (40, 50, 60), w=1.8)
    xray = (150, 220, 250) if "xray" not in d else (250, 220, 120)
    flat(c, [Ell(150, 116, 30, 34), Thick(150, 84, 150, 150, 4)], xray)
    toon(c, [Ell(450, 220, 110, 46), RRect(340, 220, 560, 270, 8)], (230, 230, 240), w=2)
    flat(c, Ell(450, 220, 50, 30), (60, 70, 90))
    toon(c, RRect(400, 240, 520, 256, 4), (150, 210, 240), w=1.2, shadow=None)
    chibi(c, 260, 270, s=0.8, hair=(60, 50, 50), outfit=(250, 250, 250), face=-1)
    for k in range(2):
        toon(c, [RRect(640 + k * 120, 220, 740 + k * 120, 244, 4), RRect(640 + k * 120, 190, 668 + k * 120, 222, 4)], (250, 250, 250), w=1.4, shadow=None)
        toon(c, RRect(664 + k * 120, 200, 740 + k * 120, 224, 4), (150, 210, 240), w=1, shadow=None)
    chibi(c, 700, 210, s=0.6, hair=(240, 200, 90), outfit=(150, 210, 240), face=1)
    # plant + clock
    plant = (80, 150, 90) if "plant" not in d else (220, 140, 60)
    toon(c, Poly([(570, 270), (590, 270), (586, 250), (574, 250)]), (190, 110, 70), w=1.2, shadow=None)
    toon(c, [Ell(574, 232, 9, 20), Ell(588, 232, 9, 20)], plant, w=1.2, shadow=None)
    toon(c, Circ(780, 90, 26), (250, 250, 250), w=1.6, shadow=None)
    flat(c, [Thick(780, 90, 780, 72, 2.4), Thick(780, 90, 792, 96, 2.4)], (40, 40, 50))
    # bottom floor: reception, waiting chairs, pharmacy, lift
    toon(c, RRect(60, 460, 260, 540, 6), (120, 180, 200), w=2)
    chibi(c, 160, 460, s=0.8, hair=(150, 90, 40), outfit=(250, 250, 250), face=1)
    for k in range(4):
        col = (90, 160, 220) if not (k == 2 and "chair" in d) else (240, 140, 60)
        toon(c, [RRect(330 + k * 64, 486, 380 + k * 64, 510, 4), RRect(330 + k * 64, 456, 340 + k * 64, 490, 3)], col, w=1.2, shadow=None)
    for k, x in enumerate((360, 490)):
        chibi(c, x, 500, s=0.7, hair=[(40, 40, 50), (230, 120, 160)][k], outfit=[(240, 200, 90), (90, 180, 120)][k], face=1)
    toon(c, RRect(640, 440, 780, 540, 6), (230, 230, 240), w=2)
    for k in range(3):
        bottle = [(240, 90, 90), (90, 180, 240), (250, 200, 60)][k]
        if k == 1 and "pill" in d:
            bottle = (150, 220, 120)
        toon(c, [RRect(660 + k * 40, 340, 684 + k * 40, 380, 4), RRect(664 + k * 40, 330, 680 + k * 40, 342, 2)], bottle, w=1.2, shadow=None)
    flat(c, RRect(650, 390, 770, 398, 0), (180, 130, 90))
    toon(c, RRect(810, 330, 870, 540, 4), (190, 196, 206), w=2)
    flat(c, Thick(840, 330, 840, 540, 2), (150, 156, 166))
    flat(c, Poly([(836, 344), (844, 344), (840, 336)]), (250, 200, 60))
    # heart-pill hospital sign (no real emblems)
    toon(c, RRect(60, 330, 260, 390, 8), (250, 250, 250), w=1.6, shadow=None)
    heart(c, 100, 360, 1.6, (240, 80, 110))
    glyph_line(c, 130, 250, 360, (70, 120, 160), 2080, w=2.4, size=12)
    # HUD
    panel(c, 330, 4, 570, 26, (30, 34, 50), r=6, w=1.4)
    flat(c, Circ(346, 15, 7), (250, 200, 60))
    digits(c, 360, 9, "92400", (250, 250, 250), 2)
    for k in range(5):
        toon(c, Poly(star_pts(460 + k * 22, 15, 11, 5)), (250, 210, 60) if k < 3 or "stars" in d else (110, 110, 130), w=1, shadow=None)


L208_ELEMENTS = [
    E("monitor", lambda c, m: flat(c, [Thick(600 + k * 10, 120 + (k % 2) * 10, 610 + k * 10, 120 + ((k + 1) % 2) * 10, 2) for k in range(4)], (90, 230, 120)),
      daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=1.4)),
    E("liftlight", lambda c, m: flat(c, Circ(840, 320, 5), (250, 220, 90)), daynight="untinted", anim=dict(blinkInterval=1.4, blinkDuration=0.6)),
    E("nurse", lambda c, m: chibi(c, 560, 545, s=0.8, hair=(90, 60, 40), outfit=(240, 170, 200), face=-1), anim=dict(bobAmplitude=(30, 2), bobSpeed=0.12)),
    E("scanbeam", lambda c, m: soft_union(c, [RRect(420, 200, 480, 240, 6)], (150, 220, 255), 0.4, spread=10), daynight="untinted", anim=dict(bobAmplitude=(30, 0), bobSpeed=0.3)),
]

L208_DIFFS = [
    ("sheet", 145, 205, 0),
    ("xray", 150, 116, 0),
    ("plant", 580, 236, 0),
    ("chair", 483, 480, 0),
    ("pill", 712, 356, 0),
    ("stars", 526, 15, 0),
]


# =================================================================== Level 209 Mars base
def dome(c, x, base, r, plants):
    toon(c, Ell(x, base, r + 8, 10), (170, 170, 180), w=1.4, shadow=None)
    pts = [(x + r * math.cos(math.radians(a)), base - r * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    toon(c, Poly(pts), (180, 220, 240), w=1.6, shadow=None)
    for k in range(-2, 3):
        flat(c, Circ(x + k * r * 0.3, base - r * 0.25, r * 0.16), plants)
    flat(c, [Thick(x - r * 0.6, base - r * 0.8, x - r * 0.3, base - r * 0.95, 3)], (250, 250, 255))


def l209_bg(c, d):
    c.gradient(0, 300, (200, 130, 100), (240, 190, 150))
    flat(c, Circ(760, 80, 26), (250, 240, 220))
    flat(c, Circ(120, 60, 12), (200, 180, 170))
    toon(c, Poly([(-20, 300), (120, 200), (260, 260), (420, 180), (600, 260), (760, 210), (920, 280), (920, 320), (-20, 320)]), (190, 100, 70), w=1.6, shadow=None)
    toon(c, Poly([(-20, 600), (-20, 300), (920, 300), (920, 600)]), (210, 120, 80), w=1.6, shadow=None)
    rnd = random.Random(2090)
    for _ in range(40):
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(320, 600), rnd.uniform(6, 20), rnd.uniform(3, 8)), (190, 104, 70))
    # tubes connecting modules
    flat(c, [Thick(160, 420, 760, 420, 14)], (200, 200, 210))
    flat(c, [Thick(160, 420, 760, 420, 6)], (230, 230, 240))
    # domes + habitat modules
    dome(c, 160, 430, 90, (90, 200, 110) if "plants" not in d else (240, 160, 60))
    dome(c, 760, 430, 70, (90, 200, 110))
    for x in (330, 470):
        toon(c, [RRect(x - 50, 370, x + 50, 440, 30)], (230, 230, 240), w=1.8)
        for k in range(3):
            flat(c, Circ(x - 26 + k * 26, 400, 8), (120, 180, 230))
    toon(c, Circ(600, 400, 40), (230, 230, 240), w=1.8)
    flat(c, Circ(600, 400, 20), (120, 180, 230))
    # solar panels
    panel_col = (60, 90, 170) if "solar" not in d else (200, 160, 60)
    for k in range(3):
        x = 60 + k * 70
        flat(c, Thick(x, 560, x, 520, 3), (150, 150, 160))
        toon(c, rot_poly(x, 512, 60, 24, -12), panel_col, w=1.2, shadow=None)
    # satellite dish
    dish = (230, 230, 240) if "dish" not in d else (240, 120, 120)
    flat(c, Thick(860, 370, 860, 320, 3), (150, 150, 160))
    toon(c, rot_poly(860, 310, 60, 16, -30), dish, w=1.4, shadow=None)
    # rocket on its pad
    toon(c, Ell(650, 560, 70, 14), (150, 150, 160), w=1.4, shadow=None)
    toon(c, Poly([(630, 556), (670, 556), (670, 470), (650, 430), (630, 470)]), (240, 240, 246), w=1.8)
    stripe = (220, 60, 60) if "rocket" not in d else (60, 140, 220)
    flat(c, [RRect(630, 500, 670, 512, 0), Poly([(630, 520), (612, 556), (630, 556)]), Poly([(670, 520), (688, 556), (670, 556)])], stripe)
    # rover + astronauts
    rover = (240, 200, 90) if "rover" not in d else (90, 180, 230)
    toon(c, RRect(330, 500, 450, 536, 6), rover, w=1.8)
    for x in (348, 390, 432):
        toon(c, Circ(x, 542, 13), (60, 60, 70), w=1.2, shadow=None)
    flat(c, [Thick(430, 500, 440, 470, 2)], (150, 150, 160))
    for x, visor in ((260, (250, 200, 80)), (540, (250, 200, 80))):
        if x == 540 and "visor" in d:
            visor = (90, 200, 240)
        toon(c, [RRect(x - 14, 520, x + 14, 560, 6), Circ(x, 506, 14)], (250, 250, 250), w=1.4)
        flat(c, Ell(x + 2, 506, 11, 9), visor)
    # HUD
    panel(c, 14, 12, 300, 92, (30, 30, 44))
    for k, (col, frac) in enumerate((((120, 200, 250), 0.7), ((250, 200, 60), 0.5), ((90, 210, 160), 0.85 if "bar" not in d else 0.35))):
        flat(c, Circ(32, 30 + k * 24, 7), col)
        bar(c, 48, 25 + k * 24, 286, 35 + k * 24, frac, col)
    panel(c, 700, 548, 886, 594, (30, 30, 44))
    digits(c, 716, 560, "0342", (250, 250, 250), 5)


L209_ELEMENTS = [
    E("dust", lambda c, m: soft_union(c, [Ell(100, 360, 60, 14)], (240, 180, 140), 0.4, spread=20), anim=drift_across(40, 160, 20, start=100)),
    E("beacon", lambda c, m: flat(c, Circ(650, 428, 4), (255, 80, 80)), daynight="untinted", anim=dict(blinkInterval=1.2, blinkDuration=0.5)),
    E("drone", lambda c, m: toon(c, [RRect(480, 220, 510, 232, 4), Thick(470, 216, 520, 216, 2)], (220, 220, 230), w=1, shadow=None), anim=dict(bobAmplitude=(40, 10), bobSpeed=0.2)),
    E("glow", lambda c, m: soft_union(c, [Circ(600, 400, 20)], (150, 220, 255), 0.4, spread=16), daynight="untinted", anim=dict(pulse=0.2, scaleSpeed=0.6)),
]

L209_DIFFS = [
    ("plants", 160, 408, 0),
    ("solar", 130, 512, 0),
    ("dish", 860, 310, 0),
    ("rocket", 650, 530, 0),
    ("rover", 390, 518, 0),
    ("visor", 543, 506, 0),
    ("bar", 220, 78, 0),
]


# =================================================================== Level 210 home design (top-down)
def l210_bg(c, d):
    c.rect(0, 0, W, H, (220, 226, 236))
    for x in range(0, 680, 20):
        flat(c, Thick(x, 50, x, 600, 1), (210, 216, 226))
    for y in range(50, 600, 20):
        flat(c, Thick(0, y, 680, y, 1), (210, 216, 226))
    # room plan
    toon(c, RRect(30, 70, 650, 580, 2), (60, 60, 70), w=1, shadow=None)
    flat(c, RRect(42, 82, 638, 568, 0), (230, 210, 180))
    for y in range(82, 568, 24):
        flat(c, Thick(42, y, 638, y, 1), (214, 194, 164))
    flat(c, RRect(330, 82, 342, 340, 0), (60, 60, 70))
    flat(c, RRect(42, 330, 230, 342, 0), (60, 60, 70))
    flat(c, RRect(42, 82, 330, 330, 0), (200, 220, 230))
    for x in range(42, 330, 30):
        flat(c, Thick(x, 82, x, 330, 1), (186, 206, 218))
    # bedroom (left top): bed, nightstands, wardrobe
    blanket = (120, 160, 220) if "blanket" not in d else (240, 150, 170)
    toon(c, RRect(80, 110, 220, 290, 8), (250, 250, 250), w=1.6)
    toon(c, RRect(80, 160, 220, 290, 8), blanket, w=1.2, shadow=None)
    toon(c, [RRect(90, 118, 145, 150, 8), RRect(155, 118, 210, 150, 8)], (250, 250, 246), w=1, shadow=None)
    for x in (56, 228):
        toon(c, RRect(x, 112, x + 40, 150, 4), (170, 120, 80), w=1.4, shadow=None)
    lamp = (250, 220, 120) if "lamp" not in d else (120, 220, 200)
    toon(c, Circ(76, 131, 12), lamp, w=1.2, shadow=None)
    toon(c, RRect(250, 220, 320, 320, 4), (170, 120, 80), w=1.4, shadow=None)
    flat(c, Thick(285, 222, 285, 318, 2), (140, 96, 60))
    # living room (right): sofa, rug, coffee table, tv, plants
    rug = (200, 90, 90) if "rug" not in d else (90, 150, 200)
    toon(c, RRect(380, 180, 600, 330, 10), rug, w=1.4, shadow=None)
    flat(c, RRect(400, 200, 580, 310, 8), lit(rug, 1.15))
    sofa = (90, 110, 140) if "sofa" not in d else (150, 110, 70)
    toon(c, [RRect(400, 100, 600, 160, 10), RRect(390, 100, 420, 180, 8), RRect(580, 100, 610, 180, 8)], sofa, w=1.6)
    toon(c, RRect(440, 220, 560, 280, 6), (170, 120, 80) if "table" not in d else (240, 240, 246), w=1.6)
    toon(c, RRect(420, 380, 600, 400, 3), (40, 40, 50), w=1.4, shadow=None)
    for x, y in ((620, 110), (370, 540)):
        toon(c, [Circ(x, y, 18), Circ(x - 10, y + 8, 12), Circ(x + 10, y + 8, 12)], (80, 160, 90) if not (x == 370 and "plant" in d) else (240, 160, 60), w=1.4)
    # kitchen (bottom left): counter + fridge + dining table
    toon(c, RRect(50, 350, 90, 560, 4), (240, 240, 246), w=1.4, shadow=None)
    for y in (380, 440, 500):
        toon(c, Circ(70, y, 10), (60, 60, 70), w=1, shadow=None)
    toon(c, RRect(100, 500, 160, 560, 4), (220, 230, 240), w=1.4, shadow=None)
    toon(c, Circ(240, 450, 50), (200, 150, 100), w=1.6)
    for a in range(0, 360, 90):
        r = math.radians(a + 45)
        toon(c, Circ(240 + math.cos(r) * 66, 450 + math.sin(r) * 66, 14), (150, 110, 70), w=1.2, shadow=None)
    # catalog panel (right)
    panel(c, 690, 60, 890, 590, (250, 250, 250), r=12, w=2)
    glyph_line(c, 708, 860, 86, (90, 90, 110), 2100, w=2.4, size=12)
    cats = [(90, 110, 140), (200, 90, 90), (170, 120, 80), (80, 160, 90), (240, 200, 90), (120, 160, 220)]
    if "catalog" in d:
        cats[4] = (220, 100, 200)
    for k, col in enumerate(cats):
        x, y = 740 + (k % 2) * 92, 140 + (k // 2) * 110
        flat(c, RRect(x - 36, y - 34, x + 36, y + 40, 8), (236, 240, 246))
        toon(c, RRect(x - 22, y - 22, x + 22, y + 14, 5), col, w=1.2, shadow=None)
        flat(c, Circ(x - 18, y + 28, 5), (250, 200, 60))
        digits(c, x - 8, y + 23, str(120 + k * 40), (90, 80, 70), 2)
    # top toolbar
    panel(c, 30, 8, 650, 46, (40, 44, 60))
    for k in range(6):
        toon(c, RRect(44 + k * 52, 14, 84 + k * 52, 40, 5), [(90, 160, 230), (240, 200, 90), (220, 90, 90), (90, 200, 120), (170, 120, 220), (200, 200, 210)][k], w=1, shadow=None)


L210_ELEMENTS = [
    E("drag", lambda c, m: toon(c, RRect(440, 440, 520, 500, 6), (240, 200, 90), w=1.6, shadow=(0, 8, 8, 0.3)), anim=dict(bobAmplitude=(20, 10), bobSpeed=0.25)),
    E("cursor", lambda c, m: toon(c, Poly([(520, 500), (520, 530), (528, 522), (534, 536), (540, 533), (534, 520), (544, 520)]), (250, 250, 250), w=1.4, shadow=None),
      daynight="untinted", anim=dict(bobAmplitude=(20, 10), bobSpeed=0.25)),
    E("snap", lambda c, m: c.ellipse_ring(480, 470, 60, 40, 2, (90, 200, 250)), daynight="untinted", anim=dict(twinkle=0.7, twinkleSpeed=0.8)),
]

L210_DIFFS = [
    ("blanket", 150, 230, 0),
    ("lamp", 76, 131, 0),
    ("rug", 490, 300, 0),
    ("sofa", 500, 130, 0),
    ("table", 500, 250, 0),
    ("plant", 370, 544, 0),
    ("catalog", 740, 362, 0),
]


# =================================================================== Level 211 truck driving
def l211_bg(c, d):
    c.gradient(0, 330, (120, 180, 240), (230, 236, 246))
    sun = (250, 230, 120) if "sun" not in d else (250, 150, 110)
    flat(c, Circ(720, 90, 34), sun)
    toon(c, Poly([(-20, 260), (140, 140), (300, 230), (460, 150), (640, 240), (800, 160), (920, 240), (920, 330), (-20, 330)]), (130, 150, 190), w=1.6, shadow=None)
    flat(c, Poly([(-20, 330), (920, 330), (920, 400), (-20, 400)]), (120, 180, 100))
    # highway
    flat(c, Poly([(420, 240), (480, 240), (900, 400), (0, 400)]), (110, 110, 120))
    flat(c, [Thick(450, 250, 450, 400, 3)], (250, 250, 240))
    flat(c, [Thick(422, 242, 0, 400, 3), Thick(478, 242, 900, 400, 3)], (250, 250, 240))
    # truck ahead + road sign
    toon(c, [RRect(510, 270, 560, 300, 3)], (220, 80, 70), w=1.4, shadow=None)
    toon(c, RRect(560, 280, 574, 300, 2), (250, 250, 250), w=1, shadow=None)
    sign = (60, 140, 90) if "sign" not in d else (60, 100, 180)
    flat(c, [Thick(700, 330, 700, 260, 3), Thick(780, 330, 780, 260, 3)], (150, 150, 160))
    toon(c, RRect(680, 210, 800, 266, 4), sign, w=1.6, shadow=None)
    glyph_line(c, 694, 790, 238, (250, 250, 250), 2110, w=2.4, size=12)
    # cab frame
    toon(c, [Poly([(-10, -10), (910, -10), (910, 30), (-10, 30)]), Poly([(-10, -10), (60, -10), (20, 400), (-10, 400)]),
             Poly([(910, -10), (840, -10), (880, 400), (910, 400)])], (70, 74, 90), w=2)
    # side mirror
    toon(c, RRect(856, 156, 900, 244, 8), (60, 60, 70) if "mirror" not in d else (200, 70, 60), w=1.6, shadow=None)
    flat(c, RRect(864, 166, 894, 234, 6), (150, 190, 230))
    toon(c, RRect(872, 200, 888, 212, 2), (240, 200, 60), w=1, shadow=None)
    # dashboard
    toon(c, Poly([(-10, 600), (-10, 380), (450, 360), (910, 380), (910, 600)]), (60, 60, 72), w=2.5)
    for k, (x, col) in enumerate(((160, (250, 250, 250)), (280, (250, 250, 250)))):
        toon(c, Circ(x, 440, 46), (30, 30, 36), w=1.6, shadow=None)
        c.ellipse_ring(x, 440, 38, 38, 2, (200, 200, 210), ymax=448)
        needle = (250, 80, 60) if not (k == 1 and "needle" in d) else (90, 220, 120)
        flat(c, Thick(x, 440, x + 34 * (1 if k == 0 else -0.6), 408, 7), needle)
    # GPS
    toon(c, RRect(560, 400, 760, 520, 10), (30, 30, 40), w=2)
    flat(c, RRect(570, 410, 750, 510, 6), (200, 220, 200))
    route = (60, 140, 240) if "gps" not in d else (240, 100, 160)
    flat(c, [Thick(580, 500, 640, 450, 5), Thick(640, 450, 720, 460, 5), Thick(720, 460, 740, 420, 5)], route)
    toon(c, Poly([(640, 444), (650, 462), (630, 462)]), (240, 80, 70), w=1, shadow=None)
    # steering wheel
    toon(c, [Circ(360, 590, 110)], (40, 40, 46), w=2, shadow=None)
    flat(c, Circ(360, 590, 92), (60, 60, 72))
    toon(c, [Thick(270, 590, 450, 590, 18), Circ(360, 590, 30)], (40, 40, 46), w=1.6, shadow=None)
    # coffee cup + dashboard toy
    cup = (240, 240, 246) if "cup" not in d else (240, 160, 60)
    toon(c, [RRect(800, 440, 840, 500, 6), Thick(840, 460, 856, 470, 5)], cup, w=1.6)
    flat(c, RRect(800, 450, 840, 462, 0), (170, 110, 60))
    toy = (250, 200, 60) if "toy" not in d else (120, 200, 240)
    toon(c, [Circ(500, 370, 16), Ell(500, 394, 14, 10)], toy, w=1.4, shadow=None)
    flat(c, [Circ(494, 368, 3), Circ(506, 368, 3)], (40, 30, 40))
    # HUD
    panel(c, 330, 36, 570, 76, (30, 30, 40))
    digits(c, 350, 46, "088", (250, 250, 250), 5)
    digits(c, 450, 46, "1240", (250, 200, 80), 5)


L211_ELEMENTS = [
    E("dash", lambda c, m: flat(c, RRect(448, 252, 452, 262, 0), (250, 250, 240)), pivot=(450, 256), anim=dict(driftVelocity=(0, -60), driftLength=140, driftGrow=3, driftFade=True)),
    E("dash2", lambda c, m: flat(c, RRect(448, 252, 452, 262, 0), (250, 250, 240)), pivot=(450, 256),
      anim=dict(driftVelocity=(0, -60), driftLength=140, driftGrow=3, driftFade=True, phase=0.5)),
    E("toybob", lambda c, m: toon(c, Circ(500, 352, 6), (250, 120, 120), w=1, shadow=None), pivot=(500, 370), anim=dict(swingAngle=14, swingSpeed=1.0)),
    E("steam", lambda c, m: toon(c, Circ(820, 430, 6), (246, 246, 250), w=1, shadow=None), anim=dict(driftVelocity=(2, 24), driftLength=50, driftFade=True)),
    E("bird", lambda c, m: flat(c, [Thick(200, 90, 210, 96, 2), Thick(210, 96, 220, 90, 2)], (70, 70, 90)), anim=drift_across(200, 220, 15, start=210)),
]

L211_DIFFS = [
    ("sun", 720, 90, 0),
    ("sign", 740, 238, 0),
    ("mirror", 880, 206, 0),
    ("needle", 268, 426, 0),
    ("gps", 660, 456, 0),
    ("cup", 822, 470, 0),
    ("toy", 500, 380, 0),
]


# =================================================================== Level 212 merge game
GRID212 = [
    "fbBc.eE",
    "b.fFccr",
    "eEb.fbB",
    ".cCFb.e",
    "fbe.EcC",
    "Bf.bceF",
]
G212X, G212Y, G212S = 200, 140, 70


def merge_item(c, x, y, ch):
    if ch in "fF":     # flower (bud / bloom)
        r = 10 if ch == "f" else 16
        flat(c, Thick(x, y + 20, x, y, 3), (80, 160, 80))
        for a in range(0, 360, 72):
            flat(c, Circ(x + math.cos(math.radians(a)) * r * 0.7, y - 4 + math.sin(math.radians(a)) * r * 0.7, r * 0.55), (250, 140, 180))
        flat(c, Circ(x, y - 4, r * 0.35), (250, 220, 90))
    elif ch in "bB":   # berries / basket
        if ch == "b":
            flat(c, [Circ(x - 6, y, 8), Circ(x + 6, y + 2, 8), Circ(x, y - 8, 8)], (200, 60, 90))
        else:
            toon(c, [Ell(x, y + 6, 22, 14), Thick(x - 18, y, x + 18, y, 3)], (190, 140, 80), w=1.2, shadow=None)
            flat(c, [Circ(x - 8, y - 2, 6), Circ(x + 6, y - 4, 6)], (200, 60, 90))
    elif ch in "cC":   # coin / coin stack
        for k in range(1 if ch == "c" else 3):
            toon(c, Ell(x, y + 8 - k * 8, 16, 7), (250, 200, 60), w=1.2, shadow=None)
    elif ch in "eE":   # egg / chick
        toon(c, Ell(x, y, 13, 17), (250, 246, 230) if ch == "e" else (250, 220, 90), w=1.2, shadow=None)
        if ch == "E":
            flat(c, [Circ(x - 4, y - 4, 2), Circ(x + 4, y - 4, 2)], (40, 30, 40))
            flat(c, Poly([(x - 3, y + 2), (x + 3, y + 2), (x, y + 6)]), (250, 140, 40))
    elif ch == "r":    # rock (locked)
        toon(c, Poly(ngon(x, y, 20, 7)), (150, 146, 156), w=1.2, shadow=None)


def l212_bg(c, d):
    c.gradient(0, H, (150, 210, 130), (110, 180, 100))
    # order cards
    for k in range(3):
        x0 = 210 + k * 170
        toon(c, RRect(x0, 14, x0 + 150, 110, 10), (250, 250, 246), w=1.8, shadow=None)
        chibi(c, x0 + 36, 100, s=0.55, hair=[(240, 200, 90), (60, 50, 50), (230, 120, 160)][k] if not (k == 1 and "hair" in d) else (90, 160, 230),
              outfit=[(90, 140, 220), (240, 140, 60), (150, 110, 200)][k])
        merge_item(c, x0 + 100, 56, ["F", "B", "E"][k])
        glyph_line(c, x0 + 80, x0 + 140, 96, (120, 110, 100), 2120 + k, w=1.6, size=8)
    # board
    toon(c, RRect(G212X - 12, G212Y - 12, G212X + 7 * G212S + 12, G212Y + 6 * G212S + 12, 16), (200, 160, 110), w=2.4)
    for j, row in enumerate(GRID212):
        for i, ch in enumerate(row):
            x, y = G212X + i * G212S, G212Y + j * G212S
            flat(c, RRect(x + 3, y + 3, x + G212S - 3, y + G212S - 3, 10), (240, 230, 200) if (i + j) % 2 else (230, 220, 190))
            if (i, j) == (3, 3) and "item" in d:
                ch = "C"
            if (i, j) == (6, 1) and "lock" in d:
                ch = "."
            if ch != ".":
                merge_item(c, x + G212S / 2, y + G212S / 2, ch)
    # side: energy + chest + crate
    panel(c, 20, 140, 170, 200, (250, 250, 246))
    toon(c, Poly([(48, 150), (34, 172), (46, 172), (40, 192), (60, 166), (48, 166), (56, 150)]), (250, 200, 60), w=1.2, shadow=None)
    digits(c, 74, 156, "86", (90, 80, 70), 5)
    chest = (170, 110, 50) if "chest" not in d else (110, 110, 200)
    toon(c, [RRect(40, 300, 150, 370, 6), RRect(40, 280, 150, 306, 12)], chest, w=1.8)
    flat(c, RRect(88, 300, 102, 324, 2), (250, 200, 60))
    toon(c, RRect(730, 330, 860, 440, 6), (190, 140, 90) if "crate" not in d else (120, 160, 200), w=1.8)
    flat(c, [Thick(730, 330, 860, 440, 3), Thick(860, 330, 730, 440, 3)], (150, 100, 60))
    # bottom info bar
    panel(c, 200, 570, 700, 596, (250, 250, 246), r=8, w=1.4)
    glyph_line(c, 220, 680, 583, (120, 110, 100), 2125, w=1.6, size=9)
    # trees decoration
    for x, y in ((60, 520), (840, 540), (840, 180)):
        toon(c, [Circ(x, y, 34), Circ(x - 22, y + 16, 22), Circ(x + 22, y + 16, 22)], (70, 150, 80), w=1.6)


L212_ELEMENTS = [
    E("drag", lambda c, m: (toon(c, RRect(G212X + 3 * G212S + 6, G212Y + 1 * G212S + 6, G212X + 4 * G212S - 6, G212Y + 2 * G212S - 6, 10), (250, 250, 200, 0.6), w=1, shadow=None),
                            merge_item(c, G212X + 3.5 * G212S, G212Y + 1.5 * G212S, "f")), anim=dict(bobAmplitude=(10, 6), bobSpeed=0.4)),
    E("spark", lambda c, m: [flat(c, Poly(star_pts(x, y, 10, 2, points=4, rot=0)), (255, 255, 230)) for x, y in ((330, 330), (560, 260))], daynight="untinted",
      anim=dict(twinkle=1, twinkleSpeed=0.7)),
    E("glow", lambda c, m: soft_union(c, [RRect(40, 280, 150, 370, 10)], (255, 230, 140), 0.4, spread=16), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.6)),
    E("butterfly", lambda c, m: toon(c, [Ell(780, 260, 6, 8), Ell(792, 260, 6, 8)], (200, 160, 250), w=1, shadow=None), pivot=(786, 260),
      anim=dict(orbitRadius=(40, 20), orbitSpeed=0.2, stretch=(0.6, 0), scaleSpeed=4)),
]

L212_DIFFS = [
    ("hair", 380 + 36, 60, 0),
    ("item", G212X + 3.5 * G212S, G212Y + 3.5 * G212S, 0),
    ("lock", G212X + 6.5 * G212S, G212Y + 1.5 * G212S, 0),
    ("crate", 795, 385, 0),
    ("chest", 95, 325, 0),
]


# =================================================================== Level 213 party board game
SPACES = [(150, 470), (210, 420), (270, 380), (340, 360), (410, 380), (470, 430), (540, 460), (610, 440), (670, 390), (720, 330), (740, 260), (700, 200),
          (630, 170), (560, 180), (490, 210), (420, 220), (350, 200), (280, 170), (210, 180), (160, 230), (130, 300), (120, 380)]
SPACE_COLS = {"b": (70, 130, 230), "r": (230, 70, 80), "s": (250, 200, 60), "g": (90, 200, 120)}
SPACE_KIND = "bbrbsbbgbrbbsbrbbgbbrb"


def l213_bg(c, d):
    c.rect(0, 0, W, H, (70, 160, 220))
    toon(c, Ell(430, 320, 400, 250), (230, 210, 150), w=2.4, shadow=None)
    flat(c, Ell(430, 320, 370, 220), (120, 190, 100))
    # path
    for a, b in zip(SPACES, SPACES[1:] + SPACES[:1]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 14), (230, 210, 160))
    for k, (x, y) in enumerate(SPACES):
        col = SPACE_COLS[SPACE_KIND[k]]
        if k == 6 and "space" in d:
            col = SPACE_COLS["r"]
        toon(c, Ell(x, y, 22, 14), col, w=1.6, shadow=None)
    # star shop + minigame tent + bridge + boat
    roof = (200, 70, 120) if "shop" not in d else (70, 160, 200)
    toon(c, RRect(400, 270, 480, 330, 4), (250, 240, 220), w=1.6)
    toon(c, Poly([(390, 274), (490, 274), (440, 232)]), roof, w=1.6)
    toon(c, Poly(star_pts(440, 296, 14, 6)), (250, 210, 60), w=1.2, shadow=None)
    toon(c, Poly([(560, 330), (640, 330), (600, 270)]), (250, 120, 60), w=1.6)
    for k in range(3):
        flat(c, Poly([(570 + k * 24, 330), (582 + k * 24, 330), (600, 270)]), (250, 240, 220))
    toon(c, Poly([(820, 470), (880, 470), (870, 490), (830, 490)]), (220, 80, 70) if "boat" not in d else (250, 250, 246), w=1.4, shadow=None)
    flat(c, Thick(850, 470, 850, 430, 2), (140, 100, 60))
    toon(c, Poly([(852, 432), (876, 462), (852, 462)]), (250, 250, 246), w=1.2, shadow=None)
    # trees
    for x, y in ((250, 280), (300, 300), (580, 240), (520, 380), (680, 270), (200, 360)):
        toon(c, [Circ(x, y, 18), Circ(x + 10, y + 8, 12)], (60, 140, 70) if not ((x, y) == (520, 380) and "tree" in d) else (230, 140, 50), w=1.4)
    # player pieces
    for k, (sp, col) in enumerate(((3, (230, 80, 80)), (8, (80, 140, 230)), (14, (90, 200, 120)), (19, (250, 200, 60)))):
        x, y = SPACES[sp]
        chibi(c, x, y + 4, s=0.5, hair=(60, 50, 50), outfit=col, face=1)
    # player panels
    for k, (x0, y0, col) in enumerate(((10, 10, (230, 80, 80)), (690, 10, (80, 140, 230)), (10, 530, (90, 200, 120)), (690, 530, (250, 200, 60)))):
        if k == 3 and "panel" in d:
            col = (200, 120, 220)
        toon(c, RRect(x0, y0, x0 + 200, y0 + 60, 10), col, w=1.8, shadow=None)
        toon(c, Poly(star_pts(x0 + 40, y0 + 30, 14, 6)), (250, 230, 120), w=1, shadow=None)
        digits(c, x0 + 60, y0 + 20, str(2 + k % 2), (250, 250, 250), 4)
        flat(c, Circ(x0 + 120, y0 + 30, 10), (250, 210, 60))
        digits(c, x0 + 136, y0 + 20, ["24", "18", "31", "09"][k], (250, 250, 250), 4)


L213_ELEMENTS = [
    E("dice", lambda c, m: (toon(c, RRect(296, 240, 336, 280, 6), (250, 250, 250), w=1.6), [flat(c, Circ(x, y, 4), (40, 40, 50)) for x, y in ((306, 250), (316, 260), (326, 270))]),
      pivot=(316, 260), anim=dict(bobAmplitude=(0, 10), bobSpeed=1.0, bounce=True, swingAngle=12, swingSpeed=1.0)),
    E("wave", lambda c, m: c.ellipse_ring(430, 320, 410, 260, 3, (220, 240, 255)), pivot=(430, 320), anim=dict(pulse=0.01, scaleSpeed=0.3, twinkle=0.5, twinkleSpeed=0.3)),
    E("starglint", lambda c, m: flat(c, Poly(star_pts(440, 230, 10, 2, points=4, rot=0)), (255, 255, 230)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
]

L213_DIFFS = [
    ("space", SPACES[6][0], SPACES[6][1], 0),
    ("shop", 440, 254, 0),
    ("boat", 850, 470, 0),
    ("tree", 520, 384, 0),
    ("panel", 790, 560, 0),
]


# =================================================================== Level 214 retro text adventure (monochrome monitor)
GREEN = (90, 250, 120)


def l214_bg(c, d):
    c.rect(0, 0, W, 420, (120, 100, 110))
    for x in range(0, W, 40):
        flat(c, RRect(x, 0, x + 20, 420, 0), (126, 106, 116))
    # desk
    c.rect(0, 420, W, H, (150, 100, 70))
    flat(c, Thick(0, 420, W, 420, 4), (120, 80, 56))
    # monitor
    toon(c, RRect(200, 30, 700, 400, 20), (220, 210, 190), w=2.5)
    toon(c, RRect(230, 60, 670, 360, 16), (20, 30, 20), w=1.6, shadow=None)
    # text lines
    for k in range(5):
        glyph_line(c, 250, 470 - (k % 2) * 40, 84 + k * 22, GREEN, 2140 + k, w=2, size=10)
    flat(c, Thick(250, 196, 300, 196, 2), GREEN)
    # ASCII-ish map box
    flat(c, [Thick(500, 80, 650, 80, 2), Thick(500, 200, 650, 200, 2), Thick(500, 80, 500, 200, 2), Thick(650, 80, 650, 200, 2)], GREEN)
    rooms = [(520, 100), (580, 100), (580, 150), (620, 150), (520, 150)]
    for k, (x, y) in enumerate(rooms):
        if k == 3 and "room" in d:
            continue
        flat(c, [Thick(x, y, x + 26, y, 3.4), Thick(x, y + 26, x + 26, y + 26, 3.4), Thick(x, y, x, y + 26, 3.4), Thick(x + 26, y, x + 26, y + 26, 3.4)], GREEN)
    flat(c, Circ(592, 112, 4), GREEN)
    # pixel picture: castle
    sprite(c, 300, 220, ["....#..........", "....##.........", "....#..........", "...###...#.#.#.", "...###...#####.", "#.#####.######.",
                         "###############", "######...######", "######...######"], {"#": GREEN}, 8)
    if "flag" in d:
        flat(c, RRect(372, 244, 420, 272, 0), (20, 30, 20))
    flat(c, Thick(250, 340, 640, 340, 2), GREEN)
    # monitor stand + brand-less badge + power LED
    toon(c, [RRect(400, 400, 500, 430, 4), RRect(360, 426, 540, 444, 4)], (210, 200, 180), w=2)
    led = (90, 250, 120) if "led" not in d else (250, 80, 80)
    flat(c, Circ(640, 380, 10), led)
    # keyboard
    toon(c, Poly([(220, 470), (680, 470), (720, 560), (180, 560)]), (220, 210, 190), w=2)
    for r in range(4):
        for k in range(14):
            x = 214 + k * 34 - r * 6 + r * 10
            flat(c, RRect(x, 478 + r * 20, x + 26, 492 + r * 20, 3), (240, 232, 214))
    # floppy disks + sticky notes + mug + lamp
    for k, col in enumerate(((60, 60, 70), (60, 100, 180), (180, 60, 60))):
        if k == 1 and "floppy" in d:
            col = (240, 200, 60)
        toon(c, rot_poly(90 + k * 30, 500 - k * 10, 70, 70, -10 + k * 8), col, w=1.6)
        flat(c, rot_poly(90 + k * 30, 484 - k * 10, 36, 20, -10 + k * 8), (220, 220, 230))
    note = (250, 230, 110) if "note" not in d else (250, 160, 200)
    toon(c, rot_poly(740, 120, 70, 70, 6), note, w=1.4, shadow=None)
    glyph_line(c, 714, 770, 116, (90, 80, 60), 2150, w=2, size=8)
    toon(c, rot_poly(150, 120, 60, 60, -8), (160, 220, 250), w=1.4, shadow=None)
    mug = (220, 80, 70) if "mug" not in d else (80, 150, 220)
    toon(c, [RRect(780, 470, 840, 540, 8), Thick(840, 490, 862, 510, 7)], mug, w=1.8)
    flat(c, Ell(810, 474, 26, 6), (120, 70, 40))
    toon(c, [Thick(780, 420, 820, 300, 5), Thick(820, 300, 760, 250, 5), Poly([(730, 270), (790, 240), (800, 280)])], (60, 60, 70), w=1.4, shadow=None)


L214_ELEMENTS = [
    E("cursor", lambda c, m: flat(c, RRect(306, 188, 318, 200, 0), GREEN), daynight="untinted", anim=dict(blinkInterval=1.0, blinkDuration=0.5)),
    E("scan", lambda c, m: flat(c, RRect(232, 62, 668, 70, 0), (120, 250, 150, 0.15)), daynight="untinted", anim=dict(bobAmplitude=(0, 140), bobSpeed=0.2)),
    E("screenglow", lambda c, m: soft_union(c, [RRect(230, 60, 670, 360, 16)], (90, 250, 120), 0.12, spread=30), daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=2.0)),
    E("steam", lambda c, m: toon(c, Circ(810, 456, 6), (240, 240, 246), w=1, shadow=None), anim=dict(driftVelocity=(3, 24), driftLength=50, driftFade=True)),
]

L214_DIFFS = [
    ("room", 632, 162, 0),
    ("flag", 396, 258, 0),
    ("led", 640, 380, 0),
    ("floppy", 120, 490, 0),
    ("note", 740, 120, 0),
    ("mug", 812, 505, 0),
]


LEVELS = [
    ("Level205", "银河城地图", l205_bg, L205_ELEMENTS, L205_DIFFS, 60, OPTS),
    ("Level206", "浮岛平台", l206_bg, L206_ELEMENTS, L206_DIFFS, 60, OPTS),
    ("Level207", "餐厅经营", l207_bg, L207_ELEMENTS, L207_DIFFS, 60, OPTS),
    ("Level208", "医院经营", l208_bg, L208_ELEMENTS, L208_DIFFS, 60, OPTS),
    ("Level209", "火星基地", l209_bg, L209_ELEMENTS, L209_DIFFS, 60, OPTS),
    ("Level210", "家居设计", l210_bg, L210_ELEMENTS, L210_DIFFS, 60, OPTS),
    ("Level211", "卡车驾驶", l211_bg, L211_ELEMENTS, L211_DIFFS, 60, OPTS),
    ("Level212", "合成游戏", l212_bg, L212_ELEMENTS, L212_DIFFS, 60, OPTS),
    ("Level213", "派对棋盘", l213_bg, L213_ELEMENTS, L213_DIFFS, 60, OPTS),
    ("Level214", "文字冒险", l214_bg, L214_ELEMENTS, L214_DIFFS, 60, OPTS),
]
