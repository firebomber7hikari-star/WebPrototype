# -*- coding: utf-8 -*-
"""Inside video games, part 7 - following the five-star favourites (pixel RPG village, tower defence, match-3,
turn-based battle, farm sim). All designs original: no real games, characters, brands or readable text.
  Level1637 像素地牢     - a 16-bit top-down dungeon: stone tiles, torches, chests, keys, slimes, hero, HUD
  Level1638 雪原回合战斗 - a turn-based battle on a snowfield: ice golem and frost wolves vs. a chibi party
  Level1639 农场秋收     - a cosy farm sim in autumn (top-down): orchard, pumpkin and wheat plots, barn, pond
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import drift_across
from levels_retro import digits, sprite
from levels_gamecontent import glyph_line, npc, rpg_house, toon, tree_tile
from levels_gamecontent2 import bar, chibi, crop

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
KEY = [".##....", "#..#...", "#..####", "#..#.#.", ".##..#."]
SLIME = ["..ggg..", ".gGggg.", "gggggg.", "gegggeg", "ggggggg", ".ggggg."]


# =================================================================== Level 1637 pixel dungeon
T = 30
STONE, STONE2 = (90, 90, 110), (82, 82, 100)


def wall_tile(c, x, y, col=(110, 104, 120)):
    flat(c, RRect(x, y, x + T, y + T, 0), col)
    flat(c, [RRect(x, y + 14, x + T, y + 16, 0), RRect(x + 14, y, x + 16, y + 14, 0), RRect(x + 6, y + 16, x + 8, y + T, 0)], lit(col, 0.7))
    flat(c, RRect(x, y, x + T, y + 3, 0), lit(col, 1.25))


def l1637_bg(c, d):
    for j in range(20):
        for i in range(30):
            flat(c, RRect(i * T, j * T, (i + 1) * T, (j + 1) * T, 0), STONE if (i + j) % 2 else STONE2)
    rnd = random.Random(1637)
    for _ in range(60):
        x, y = rnd.randrange(0, 900, 6), rnd.randrange(60, 500, 6)
        flat(c, RRect(x, y, x + 6, y + 6, 0), (70, 70, 88))
    # walls: outer frame + inner rooms
    for i in range(30):
        wall_tile(c, i * T, 30)
    for j in range(2, 17):
        wall_tile(c, 0, j * T)
        wall_tile(c, 870, j * T)
    for i in range(1, 12):
        if i not in (5, 6):
            wall_tile(c, i * T, 240)
    for i in range(17, 29):
        if i not in (22, 23):
            wall_tile(c, i * T, 300)
    for j in range(3, 8):
        wall_tile(c, 360, j * T)
    for j in range(10, 17):
        if j not in (12, 13):
            wall_tile(c, 480, j * T)
    # water channel with a bridge
    flat(c, RRect(560, 60, 620, 300, 0), (60, 110, 200))
    for y in range(70, 300, 26):
        flat(c, RRect(574, y, 590, y + 4, 0), (140, 190, 250))
    for x in range(556, 626, 10):
        flat(c, RRect(x, 150, x + 8, 200, 0), (150, 100, 60))
    # torches
    for x, y in ((90, 64), (300, 64), (660, 64), (840, 64), (420, 270), (720, 330)):
        flat(c, RRect(x + 8, y, x + 14, y + 20, 0), (110, 70, 40))
        sprite(c, x + 4, y - 14, ["..y..", ".yoy.", "yoroy", ".yoy."], {"y": (250, 220, 80), "o": (250, 150, 40), "r": (230, 70, 40)}, 3)
    # chests
    for k, (x, y, key) in enumerate(((60, 90, None), (420, 90, "chest"), (780, 360, None))):
        col = (190, 120, 50) if not (key and key in d) else (110, 110, 200)
        flat(c, RRect(x, y, x + 40, y + 30, 0), lit(col, 0.7))
        flat(c, [RRect(x + 2, y + 2, x + 38, y + 13, 0), RRect(x + 2, y + 16, x + 38, y + 28, 0)], col)
        flat(c, RRect(x + 17, y + 10, x + 23, y + 20, 0), (250, 220, 90))
    # locked door, key, spikes, slimes, stairs down
    door = (150, 100, 60) if "door" not in d else (120, 120, 140)
    flat(c, RRect(660, 300, 720, 330, 0), door)
    flat(c, RRect(684, 308, 696, 322, 0), (250, 220, 90))
    if "key" not in d:
        sprite(c, 200, 380, KEY, {"#": (250, 210, 60)}, 5)
    for k in range(4):
        sprite(c, 560 + k * 26, 420, ["..#..", ".###.", "#####"], {"#": (200, 200, 210)}, 5)
    for k, (x, y) in enumerate(((150, 160), (250, 440), (760, 180))):
        col = (90, 200, 120) if not ("slime" in d and k == 2) else (230, 90, 160)
        sprite(c, x, y, SLIME, {"g": col, "G": lit(col, 1.4), "e": (30, 30, 40)}, 5)
    for k in range(4):
        flat(c, RRect(790 + k * 6, 470 + k * 10, 850, 476 + k * 10, 0), (60, 60, 76) if k % 2 else (130, 126, 140))
    # pots
    for k, (x, y) in enumerate(((260, 90), (290, 90), (60, 500))):
        if "pot" in d and k == 1:
            continue
        toon(c, [Ell(x + 12, y + 16, 12, 14), RRect(x + 6, y, x + 18, y + 6, 2)], (200, 120, 70), w=1.4, shadow=None)
    # HUD: hearts, keys count, mini-map
    flat(c, RRect(0, 0, 900, 30, 0), (20, 20, 36))
    for k in range(5 if "hearts" not in d else 4):
        sprite(c, 10 + k * 30, 5, HEART, {"#": (240, 60, 80)}, 4)
    sprite(c, 200, 6, KEY, {"#": (250, 210, 60)}, 3)
    digits(c, 230, 8, "3", (250, 250, 250), 3)
    flat(c, RRect(780, 4, 890, 26, 2), (40, 40, 60))
    for i, j in ((0, 0), (1, 0), (2, 0), (1, 1), (2, 1), (3, 1)):
        flat(c, RRect(784 + i * 18, 6 + j * 10, 798 + i * 18, 14 + j * 10, 1), (120, 120, 160))
    flat(c, RRect(784 + 18 * 2, 16, 798 + 18 * 2, 24, 1), (250, 220, 90))


def l1637_hero(c, m):
    npc(c, 470, 180, (60, 110, 220), hair=(150, 90, 40), legs=(60, 60, 80))
    flat(c, RRect(504, 196, 508, 222, 0), (220, 220, 230))


L1637_ELEMENTS = [
    E("hero", l1637_hero, pivot=(486, 200), anim=dict(bobAmplitude=(0, 3), bobSpeed=1.0, bounce=True)),
    E("flicker", lambda c, m: [soft_union(c, [Circ(x + 11, y - 6, 16)], (255, 200, 90), 0.3, spread=12) for x, y in ((90, 64), (300, 64), (660, 64), (840, 64))],
      daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.6)),
    E("bat", lambda c, m: sprite(c, 330, 380, ["#...#", "##.##", ".###.", "..#.."], {"#": (120, 80, 150)}, 5), pivot=(342, 390),
      anim=dict(bobAmplitude=(40, 12), bobSpeed=0.3)),
]
L1637_DIFFS = [("chest", 440, 104, 0), ("door", 690, 315, 0), ("key", 216, 392, 0), ("slime", 776, 194, 0), ("pot", 302, 106, 0),
               ("hearts", 136, 14, 0)]


# =================================================================== Level 1638 snowfield turn-based battle
def l1638_bg(c, d):
    c.gradient(0, 260, (150, 190, 240), (230, 240, 252))
    toon(c, Poly([(-20, 260), (120, 120), (260, 210), (400, 100), (560, 220), (720, 130), (920, 260)]), (190, 210, 240), w=1.6, shadow=None)
    for ax, ay in ((120, 120), (400, 100), (720, 130)):
        flat(c, Poly([(ax - 30, ay + 36), (ax, ay), (ax + 30, ay + 36)]), (250, 252, 255))
    toon(c, Poly([(-20, 260), (920, 260), (920, 420), (-20, 420)]), (236, 242, 252), w=1.6, shadow=None)
    for x, y in ((80, 300), (300, 380), (520, 300), (840, 380)):
        flat(c, Ell(x, y, 30, 6), (210, 222, 240))
    # pine trees with snow
    for x, key in ((40, None), (860, "pine")):
        if key and key in d:
            continue
        toon(c, RRect(x - 5, 230, x + 5, 262, 2), (130, 90, 60), w=1.2, shadow=None)
        toon(c, [Poly([(x - 34, 236), (x, 160), (x + 34, 236)]), Poly([(x - 26, 200), (x, 140), (x + 26, 200)])], (60, 120, 90), w=1.4, shadow=None)
        flat(c, Poly([(x - 10, 166), (x, 140), (x + 10, 166)]), (250, 252, 255))
    # ice golem (left)
    toon(c, [RRect(110, 240, 250, 350, 20)], (150, 200, 240))
    toon(c, [RRect(140, 190, 220, 246, 14)], (170, 214, 248))
    for x0 in (80, 252):
        toon(c, RRect(x0, 260, x0 + 34, 340, 12), (140, 190, 236))
    flat(c, [Ell(166, 216, 7, 9), Ell(196, 216, 7, 9)], (30, 60, 120) if "eyes" not in d else (230, 60, 60))
    for k, (x, y) in enumerate(((130, 230), (180, 180), (226, 236))):
        toon(c, Poly([(x - 8, y), (x, y - 26), (x + 8, y)]), (220, 240, 255), w=1.2, shadow=None)
    # frost wolves
    for k, (x, base) in enumerate(((330, 360), (380, 300))):
        col = (200, 210, 230) if not ("wolf" in d and k == 0) else (120, 120, 150)
        toon(c, [Ell(x, base - 20, 34, 18), Circ(x + 34, base - 34, 15), Poly([(x + 28, base - 46), (x + 30, base - 62), (x + 38, base - 46)]),
                 Poly([(x + 40, base - 46), (x + 46, base - 62), (x + 48, base - 44)]), RRect(x - 24, base - 10, x - 16, base, 2), RRect(x + 14, base - 10, x + 22, base, 2)],
             col, w=1.6)
        flat(c, Circ(x + 40, base - 36, 2.4), (40, 120, 220))
    # party (right)
    chibi(c, 620, 330, s=1.2, hair=(240, 200, 90), outfit=(220, 80, 120), face=-1, weapon="staff")
    chibi(c, 720, 370, s=1.35, hair=(150, 90, 40), outfit=(60, 110, 210) if "coat" not in d else (90, 170, 90), face=-1, weapon="sword")
    chibi(c, 820, 330, s=1.2, hair=(90, 60, 40), outfit=(110, 70, 170), face=-1, hat=(110, 70, 170), weapon="staff")
    # UI
    for x0, x1 in ((10, 330), (340, 890)):
        toon(c, RRect(x0, 420, x1, 592, 10), (250, 250, 250), w=2.5)
        flat(c, RRect(x0 + 6, 426, x1 - 6, 586, 8), (40, 50, 120))
    for k in range(4):
        glyph_line(c, 60, 250, 452 + k * 36, (250, 250, 250), 3810 + k, w=2.4, size=12)
    for r, (hp, mp) in enumerate(((0.7, 0.6), (0.9, 0.4), (0.55, 0.85))):
        y = 452 + r * 46
        glyph_line(c, 360, 470, y, (250, 250, 250), 3815 + r, w=2.2, size=11)
        bar(c, 490, y - 8, 680, y + 6, hp, (90, 210, 110) if not (r == 2 and "hpbar" in d) else (240, 150, 60))
        bar(c, 700, y - 8, 860, y + 6, mp, (80, 150, 240))
    if "icon" not in d:
        sprite(c, 280, 444, [".#.#.", "#####", ".###.", "#####", ".#.#."], {"#": (150, 220, 255)}, 5)


L1638_ELEMENTS = [
    E("cursor", lambda c, m: toon(c, Poly([(30, 442), (46, 452), (30, 462)]), (250, 250, 250), w=1.2, shadow=None), daynight="untinted",
      anim=dict(bobAmplitude=(5, 0), bobSpeed=1.5)),
    E("snow", lambda c, m: [flat(c, Circ(x, y, 3), (255, 255, 255)) for x, y in ((100, 40), (260, 90), (480, 30), (640, 120), (820, 70), (380, 160))],
      bbox=(80, 20, 840, 180), anim=dict(driftVelocity=(-6, -40), driftLength=200, driftFade=True)),
    E("dmg", lambda c, m: digits(c, 160, 150, "245", (250, 250, 250), 5), daynight="untinted", anim=dict(blinkInterval=2.0, blinkDuration=1.0,
                                                                                                        bobAmplitude=(0, 10), bobSpeed=0.5)),
]
L1638_DIFFS = [("pine", 860, 200, 0), ("eyes", 181, 216, 0), ("wolf", 340, 334, 0), ("coat", 720, 340, 0), ("hpbar", 585, 544, 0),
               ("icon", 292, 456, 0)]


# =================================================================== Level 1639 autumn farm sim
def l1639_bg(c, d):
    c.rect(0, 0, W, H, (150, 190, 90))
    rnd = random.Random(1639)
    for _ in range(80):
        x, y = rnd.randrange(0, 900, 6), rnd.randrange(30, 520, 6)
        flat(c, RRect(x, y, x + 6, y + 6, 0), rnd.choice([(170, 200, 100), (230, 160, 70), (210, 110, 60)]))
    # dirt path
    flat(c, RRect(0, 290, 900, 330, 0), (214, 184, 120))
    flat(c, RRect(430, 330, 470, 520, 0), (214, 184, 120))
    # barn and house
    rpg_house(c, 40, 40, 230, (190, 60, 50), roof_h=90, wall_h=90, door_x=135)
    rpg_house(c, 640, 50, 800, (90, 120, 190) if "roof" not in d else (120, 70, 160), door_x=720)
    # orchard trees with apples (autumn colours)
    for k, (x, y) in enumerate(((290, 40), (360, 70), (430, 40), (500, 70))):
        col = [(230, 140, 50), (210, 90, 50), (240, 180, 60), (200, 120, 40)][k]
        tree_tile(c, x, y, col=col)
        if not ("apples" in d and k == 1):
            for ax, ay in ((x + 14, y + 14), (x + 30, y + 22), (x + 22, y + 34)):
                flat(c, Circ(ax, ay, 4), (220, 40, 40))
    # crop plots: pumpkins, wheat, carrots
    for py, kind in ((360, "pumpkin"), (420, "wheat"), (480, "carrot")):
        flat(c, RRect(40, py - 22, 400, py + 22, 2), (130, 90, 60))
        for k, x in enumerate(range(70, 390, 40)):
            if kind == "pumpkin" and "pumpkin" in d and k == 4:
                continue
            crop(c, x, py, kind)
    # pond with a duck and lily pads
    flat(c, Ell(690, 430, 150, 70), (80, 150, 220))
    flat(c, Ell(690, 430, 140, 60), (110, 180, 240))
    for x, y in ((620, 420), (760, 450)):
        flat(c, Ell(x, y, 16, 8), (90, 170, 80))
    if "duck" not in d:
        sprite(c, 680, 400, ["..yy..", ".yyyo.", "wwwww.", "wwwww."], {"y": (250, 220, 60), "o": (240, 140, 40), "w": (250, 250, 250)}, 5)
    # chickens, scarecrow, hay bales
    for k, (x, y) in enumerate(((520, 360), (560, 380), (540, 420))):
        col = (250, 250, 246) if not ("chick" in d and k == 1) else (150, 100, 60)
        sprite(c, x, y, [".rr..", "wwww.", "wwwwo", ".ww..", ".y.y."], {"r": (230, 50, 50), "w": col, "o": (240, 160, 40), "y": (240, 180, 50)}, 5)
    flat(c, RRect(206, 250, 214, 300, 0), (120, 80, 50))
    flat(c, RRect(186, 262, 234, 268, 0), (120, 80, 50))
    flat(c, Circ(210, 246, 10), (240, 210, 150))
    flat(c, Poly([(194, 240), (226, 240), (210, 222)]), (110, 80, 50) if "hat" not in d else (60, 120, 200))
    for x in (820, 860):
        flat(c, RRect(x, 300, x + 34, 330, 4), (230, 200, 100))
        flat(c, [RRect(x, 310, x + 34, 313, 0), RRect(x, 320, x + 34, 323, 0)], (200, 170, 70))
    # HUD: calendar + tool bar
    flat(c, RRect(800, 6, 892, 70, 6), (250, 240, 220))
    flat(c, RRect(800, 6, 892, 22, 6), (220, 80, 60))
    digits(c, 828, 32, "12", (60, 50, 50), 5)
    flat(c, RRect(260, 534, 640, 592, 8), (90, 60, 40))
    for k in range(6):
        x = 270 + k * 62
        flat(c, RRect(x, 542, x + 52, 584, 4), (250, 230, 190) if k != 2 else (250, 210, 90))
    toon(c, [Thick(285, 576, 305, 552, 4)], (150, 100, 60), w=1, shadow=None)
    toon(c, RRect(346, 552, 372, 572, 3), (100, 160, 230), w=1, shadow=None)
    if "seed" not in d:
        toon(c, RRect(408, 552, 434, 576, 4), (230, 180, 90), w=1, shadow=None)
    npc(c, 446, 200, (60, 150, 90), hair=(150, 90, 40), legs=(70, 70, 100))


L1639_ELEMENTS = [
    E("leaf1", lambda c, m: flat(c, Ell(320, 120, 5, 3), (230, 140, 50)), pivot=(320, 120),
      anim=dict(driftVelocity=(10, -50), driftLength=200, driftFade=True, swingAngle=30, swingSpeed=0.8)),
    E("leaf2", lambda c, m: flat(c, Ell(460, 110, 5, 3), (210, 90, 50)), pivot=(460, 110),
      anim=dict(driftVelocity=(-8, -50), driftLength=200, driftFade=True, swingAngle=30, swingSpeed=0.8, phase=0.5)),
    E("ripple", lambda c, m: flat(c, Ell(690, 460, 30, 4), (180, 220, 250)), anim=dict(twinkle=0.6, twinkleSpeed=0.6, pulse=0.2)),
]
L1639_DIFFS = [("roof", 720, 90, 0), ("apples", 382, 98, 0), ("pumpkin", 230, 360, 0), ("duck", 694, 410, 0), ("chick", 572, 392, 0),
               ("hat", 210, 234, 0), ("seed", 421, 564, 0)]


LEVELS = [
    ("Level1637", "像素地牢", l1637_bg, L1637_ELEMENTS, L1637_DIFFS, 60, OPTS),
    ("Level1638", "雪原回合战斗", l1638_bg, L1638_ELEMENTS, L1638_DIFFS, 60, OPTS),
    ("Level1639", "农场秋收", l1639_bg, L1639_ELEMENTS, L1639_DIFFS, 60, OPTS),
]
