# -*- coding: utf-8 -*-
"""Inside video games of today's genres (all designs original: no real games, characters, brands or logos):
  Level165 像素RPG村庄 - a 16-bit RPG overworld village (top-down tiles), hero, villagers, chest, dialogue box
  Level166 赛车游戏    - a pseudo-3D racing game: road to the horizon, rival cars, checkpoint arch, HUD with minimap
  Level167 塔防游戏    - a cartoon tower-defence map: winding path, towers, creeping slimes, castle, build bar
  Level168 宝石消除    - a match-3 puzzle board: gems, owl-wizard mascot, score / moves panels, boosters
  Level169 电竞赛场    - a real esports arena (paper-craft): giant screen, team booths, trophy, crowd with light sticks
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, drift_across
from levels_akiba import modern, sign_box
from levels_retro import digits, sprite
from levels_festival import confetti

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
NIGHT_EDGE = (120, 110, 140)
OUTLINE = (50, 40, 60)


def toon(c, shapes, col, w=2.0, shadow=(0, 3, 4, 0.25)):
    """Cartoon game art: dark outline + soft drop shadow."""
    piece(c, shapes, col, border=w, border_col=OUTLINE, shadow=shadow)


def dpiece(c, shapes, col, border=1.5, shadow=PROP):
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


def glyph_line(c, x0, x1, y, col, seed, w=2.0, size=10):
    """A line of made-up letters (UI text without real words)."""
    rnd = random.Random(seed)
    x = x0
    while x < x1 - size:
        for _ in range(2):
            flat(c, Thick(x + rnd.uniform(0, size), y + rnd.uniform(-size / 2, size / 2), x + rnd.uniform(0, size), y + rnd.uniform(-size / 2, size / 2), w), col)
        x += size + 4 + (6 if rnd.random() < 0.2 else 0)


# =================================================================== Level 165 16-bit RPG village
T = 30
GRASS, GRASS2 = (112, 190, 92), (104, 180, 86)
DIRT, DIRT2 = (214, 184, 120), (200, 168, 106)
CHAR = ["..hhhh..", ".hhhhhh.", ".hssssh.", ".sesses.", "..ssss..", ".bbbbbb.", "sbbbbbbs", "sbbbbbbs", ".bbbbbb.", ".ll..ll.", ".kk..kk."]
TREE = ["...gggg...", ".gggGGggg.", "ggGGggggGg", "gGgggggGgg", "ggggGgggGg", ".gGgggggg.", "..gggggg..", "....tt....", "....tt...."]


def npc(c, x, y, body, hair=(70, 50, 40), legs=(60, 60, 90), skin=(250, 210, 170), s=4):
    sprite(c, x, y, CHAR, {"h": hair, "s": skin, "e": (30, 30, 40), "b": body, "l": legs, "k": (60, 40, 30)}, s)


def tree_tile(c, x, y, col=(50, 140, 70), s=5):
    sprite(c, x, y, TREE, {"g": col, "G": lit(col, 1.3), "t": (120, 80, 50)}, s)


def rpg_house(c, x0, y0, x1, roof, wall=(236, 220, 186), roof_h=80, wall_h=70, door_x=None, sign=None):
    """JRPG house seen from above-front: striped roof block, wall with door and windows."""
    flat(c, RRect(x0 - 6, y0, x1 + 6, y0 + roof_h, 0), lit(roof, 0.75))
    flat(c, RRect(x0, y0 + 4, x1, y0 + roof_h - 4, 0), roof)
    for y in range(int(y0) + 14, int(y0 + roof_h) - 4, 12):
        flat(c, RRect(x0, y, x1, y + 3, 0), lit(roof, 0.85))
    flat(c, RRect(x0 - 6, y0 + roof_h - 6, x1 + 6, y0 + roof_h, 0), lit(roof, 0.6))
    wy = y0 + roof_h
    flat(c, RRect(x0, wy, x1, wy + wall_h, 0), wall)
    flat(c, RRect(x0, wy + wall_h - 6, x1, wy + wall_h, 0), lit(wall, 0.8))
    dx = door_x if door_x is not None else (x0 + x1) / 2
    flat(c, RRect(dx - 14, wy + wall_h - 44, dx + 14, wy + wall_h, 0), (140, 90, 50))
    flat(c, RRect(dx + 6, wy + wall_h - 24, dx + 10, wy + wall_h - 20, 0), (250, 220, 90))
    for wx in (x0 + 20, x1 - 44):
        if abs(wx + 12 - dx) > 30:
            flat(c, RRect(wx, wy + 14, wx + 24, wy + 36, 0), (90, 70, 50))
            flat(c, RRect(wx + 3, wy + 17, wx + 21, wy + 33, 0), (150, 210, 240))
            flat(c, Thick(wx + 12, wy + 17, wx + 12, wy + 33, 2), (90, 70, 50))
    if sign:
        flat(c, RRect(dx - 30, wy + 4, dx + 30, wy + 20, 0), (110, 70, 40))
        glyph_line(c, dx - 26, dx + 30, wy + 12, sign, 1651, w=2, size=8)


def l165_bg(c, d):
    for j in range(0, 20):
        for i in range(0, 30):
            flat(c, RRect(i * T, j * T, (i + 1) * T, (j + 1) * T, 0), GRASS if (i + j) % 2 else GRASS2)
    rnd = random.Random(1650)
    for _ in range(70):
        x, y = rnd.randrange(0, 900, 6), rnd.randrange(40, 500, 6)
        flat(c, RRect(x, y, x + 6, y + 6, 0), rnd.choice([(250, 250, 250), (250, 220, 80), (240, 120, 150), (90, 160, 70)]))
    # dirt paths
    for (x0, y0, x1, y1) in ((0, 270, 900, 330), (270, 330, 330, 500), (390, 210, 420, 270), (120, 220, 150, 270), (765, 250, 795, 270)):
        flat(c, RRect(x0, y0, x1, y1, 0), DIRT)
        for x in range(int(x0), int(x1), 12):
            for y in range(int(y0), int(y1), 12):
                if (x * 7 + y * 3) % 5 == 0:
                    flat(c, RRect(x, y, x + 6, y + 6, 0), DIRT2)
    # river + bridge
    flat(c, RRect(600, 0, 660, 500, 0), (70, 140, 220))
    flat(c, [RRect(600, 0, 606, 500, 0), RRect(654, 0, 660, 500, 0)], (230, 230, 210))
    for y in range(10, 500, 30):
        flat(c, RRect(616, y, 630, y + 4, 0), (150, 200, 250))
    plank = (160, 110, 60) if "bridge" not in d else (120, 120, 130)
    for x in range(594, 666, 12):
        flat(c, RRect(x, 262, x + 10, 338, 0), plank)
    flat(c, [RRect(590, 258, 670, 264, 0), RRect(590, 336, 670, 342, 0)], lit(plank, 0.7))
    # trees along the top edge and the corners
    for x in (-10, 180, 240, 530, 700, 860):
        tree_tile(c, x, 0)
    for x, y in ((520, 340), (540, 420), (860, 300), (870, 420), (-10, 300)):
        tree_tile(c, x, y, col=(50, 140, 70) if not (x == 540 and "tree" in d) else (220, 140, 50))
    # houses
    rpg_house(c, 50, 60, 210, (200, 70, 60), door_x=135)
    rpg_house(c, 330, 50, 500, (60, 110, 200) if "roof" not in d else (120, 70, 160), door_x=405, sign=(250, 230, 160))
    rpg_house(c, 700, 100, 860, (70, 150, 90), roof_h=70, wall_h=80, door_x=780, sign=(250, 230, 160))
    # treasure chest by the hero's house
    chest = (190, 120, 50) if "chest" not in d else (110, 110, 200)
    flat(c, RRect(222, 190, 262, 220, 0), lit(chest, 0.7))
    flat(c, [RRect(224, 192, 260, 204, 0), RRect(224, 206, 260, 218, 0)], chest)
    flat(c, [RRect(240, 200, 246, 212, 0)], (250, 220, 90))
    # village well
    flat(c, Circ(450, 400, 30), (150, 150, 160))
    flat(c, Circ(450, 400, 20), (40, 70, 120))
    flat(c, [RRect(420, 360, 426, 400, 0), RRect(474, 360, 480, 400, 0)], (110, 70, 40))
    well = (200, 70, 60) if "well" not in d else (60, 160, 160)
    flat(c, Poly([(410, 366), (490, 366), (470, 340), (430, 340)]), well)
    # crop field (left) with fence
    flat(c, RRect(30, 360, 230, 490, 0), (150, 110, 70))
    for y in range(372, 490, 22):
        flat(c, RRect(36, y, 224, y + 6, 0), (120, 86, 54))
        for x in range(44, 220, 26):
            flat(c, RRect(x, y - 8, x + 10, y, 0), (90, 180, 70))
    if "pumpkin" not in d:
        sprite(c, 150, 420, [".gg..", "ooooo", "oOooo", "ooooo", ".ooo."], {"g": (60, 130, 50), "o": (240, 140, 40), "O": (250, 190, 90)}, 6)
    for x in range(26, 236, 18):
        flat(c, RRect(x, 352, x + 6, 368, 0), (250, 240, 220))
    flat(c, RRect(26, 356, 236, 360, 0), (250, 240, 220))
    # sheep pen (right)
    for x in range(690, 860, 18):
        flat(c, RRect(x, 380, x + 6, 396, 0), (250, 240, 220))
    flat(c, RRect(690, 384, 856, 388, 0), (250, 240, 220))
    SHEEP = [".wwww...", "wwwwwwkk", "wwwwwwkk", "wwwwww..", ".k..k..."]
    for k, (x, y) in enumerate(((710, 410), (780, 440), (720, 460))):
        wool = (250, 250, 246) if not (k == 1 and "sheep" in d) else (70, 64, 72)
        sprite(c, x, y, SHEEP, {"w": wool, "k": (60, 50, 50)}, 5)
    # villagers
    npc(c, 470, 240, (120, 80, 160), hair=(220, 220, 220))                 # elder by the inn
    npc(c, 490, 420, (240, 200, 60), hair=(200, 120, 50))                 # kid at the well
    npc(c, 800, 250, (60, 150, 90) if "shopkeeper" not in d else (220, 80, 80), hair=(60, 40, 30))
    npc(c, 676, 330, (150, 150, 170), hair=(70, 70, 80), legs=(90, 90, 110))   # bridge guard
    flat(c, Thick(712, 300, 712, 350, 3), (200, 200, 210))
    # signpost
    flat(c, RRect(356, 340, 362, 380, 0), (110, 70, 40))
    flat(c, RRect(336, 330, 384, 348, 0), (180, 130, 80))
    # HUD: hearts + coins
    flat(c, RRect(8, 6, 152, 40, 4), (20, 24, 50, 0.8))
    for k in range(4 if "hearts" not in d else 3):
        sprite(c, 16 + k * 34, 12, [".#.#.", "#####", "#####", ".###.", "..#.."], {"#": (240, 60, 80)}, 5)
    flat(c, RRect(748, 6, 892, 40, 4), (20, 24, 50, 0.8))
    sprite(c, 758, 12, [".###.", "#####", "#####", "#####", ".###."], {"#": (250, 210, 60)}, 5)
    digits(c, 800, 14, "1250", (250, 250, 250), 4)
    # dialogue box
    flat(c, RRect(10, 500, 890, 594, 8), (250, 250, 250))
    flat(c, RRect(16, 506, 884, 588, 6), (30, 40, 110))
    flat(c, RRect(28, 514, 104, 580, 4), (60, 80, 160))
    hair = (200, 120, 50) if "portrait" not in d else (60, 50, 50)
    sprite(c, 38, 516, ["..hhhhh..", ".hhhhhhh.", "hhsssssh.", "hsesssesh", ".sssssss.", "..ssmss..", "..bbbbb..", ".bbbbbbb."],
           {"h": hair, "s": (250, 210, 170), "e": (30, 30, 40), "m": (200, 90, 90), "b": (240, 200, 60)}, 7)
    for k in range(3):
        glyph_line(c, 124, 760 - k * 120, 528 + k * 22, (250, 250, 250), 1652 + k, w=2.2, size=12)


def l165_hero(c, m):
    npc(c, 286, 262, (60, 110, 220), hair=(150, 90, 40), legs=(60, 60, 80))
    flat(c, [RRect(320, 290, 324, 314, 0)], (220, 220, 230))
    flat(c, RRect(316, 312, 328, 316, 0), (200, 160, 60))


L165_ELEMENTS = [
    E("hero", l165_hero, anim=dict(bobAmplitude=(0, 3), bobSpeed=1.5, bounce=True)),
    E("cursor", lambda c, m: sprite(c, 856, 566, ["#####", ".###.", "..#.."], {"#": (250, 250, 250)}, 4), daynight="untinted",
      anim=dict(bobAmplitude=(0, 4), bobSpeed=1.2)),
    E("ripple", lambda c, m: [flat(c, RRect(616, y, 640, y + 4, 0), (190, 230, 255)) for y in (40, 150, 400, 460)],
      anim=dict(driftVelocity=(0, 20), driftLength=40, driftFade=True)),
    E("bird", lambda c, m: sprite(c, 0, 60, ["#...#", ".#.#.", "..#.."], {"#": (60, 60, 80)}, 4), anim=drift_across(0, 20, 40, start=300)),
]

L165_DIFFS = [
    ("roof", 415, 90, 0),
    ("chest", 242, 205, 0),
    ("well", 450, 353, 0),
    ("pumpkin", 165, 435, 0),
    ("sheep", 800, 452, 0),
    ("shopkeeper", 816, 272, 0),
    ("hearts", 118, 22, 0),
    ("portrait", 66, 545, 0),
    ("bridge", 630, 300, 0),
    ("tree", 565, 440, 0),
]


# =================================================================== Level 166 pseudo-3D racing game
HZ, VX = 236, 450                  # horizon y, vanishing x


def road_hw(y):
    return 8 + (y - HZ) / (H - HZ) * 420


def depth_ys():
    ys, f = [], 1.0
    while f > 0.004:
        ys.append(HZ + (H - HZ) * f)
        f *= 0.8
    return ys + [HZ]


def car_rear(c, x, base, s, body, glass=(40, 50, 70), spoiler=None):
    w, h = 110 * s, 54 * s
    piece(c, [RRect(x - w / 2 + 6 * s, base - 14 * s, x - w / 2 + 26 * s, base, 3 * s), RRect(x + w / 2 - 26 * s, base - 14 * s, x + w / 2 - 6 * s, base, 3 * s)],
          (30, 30, 36), border=1.2, border_col=OUTLINE, shadow=(0, 2 * s, 4 * s, 0.35))
    toon(c, [RRect(x - w / 2, base - h * 0.62, x + w / 2, base - 8 * s, 8 * s), Poly([(x - w * 0.34, base - h * 0.6), (x + w * 0.34, base - h * 0.6),
                                                                                  (x + w * 0.24, base - h), (x - w * 0.24, base - h)])], body, w=1.5 * s)
    flat(c, Poly([(x - w * 0.28, base - h * 0.64), (x + w * 0.28, base - h * 0.64), (x + w * 0.2, base - h * 0.94), (x - w * 0.2, base - h * 0.94)]), glass)
    flat(c, [RRect(x - w / 2 + 6 * s, base - h * 0.5, x - w / 2 + 28 * s, base - h * 0.38, 2 * s),
             RRect(x + w / 2 - 28 * s, base - h * 0.5, x + w / 2 - 6 * s, base - h * 0.38, 2 * s)], (250, 60, 60))
    flat(c, RRect(x - 16 * s, base - h * 0.36, x + 16 * s, base - h * 0.22, 2 * s), (250, 250, 240))
    if spoiler:
        toon(c, [RRect(x - w * 0.5, base - h * 1.08, x + w * 0.5, base - h * 0.98, 2 * s), RRect(x - w * 0.3, base - h, x - w * 0.26, base - h * 0.9, 0),
                 RRect(x + w * 0.26, base - h, x + w * 0.3, base - h * 0.9, 0)], spoiler, w=1.2 * s, shadow=None)


def l166_bg(c, d):
    c.gradient(0, HZ, (90, 150, 240), (250, 200, 170))
    sun = (250, 230, 120) if "sun" not in d else (250, 150, 90)
    soft_union(c, [Circ(690, 130, 40)], (255, 240, 200), 0.5, spread=50)
    flat(c, Circ(690, 130, 40), sun)
    for k in range(4):
        flat(c, RRect(650, 140 + k * 8, 730, 143 + k * 8, 0), (250, 180, 150))
    # mountains (flat bands, game style)
    flat(c, Poly([(-20, HZ), (60, 150), (150, 200), (250, 110), (360, 190), (440, 150), (540, 200), (600, HZ)]), (110, 100, 170))
    if "snow" not in d:
        flat(c, Poly([(250, 110), (282, 140), (264, 136), (250, 146), (236, 134), (220, 140)]), (250, 250, 255))
    flat(c, Poly([(420, HZ), (560, 170), (650, 210), (760, 140), (920, HZ)]), (130, 120, 190))
    flat(c, Poly([(760, 140), (788, 166), (770, 162), (752, 168), (738, 160)]), (250, 250, 255))
    flat(c, Poly([(-20, HZ), (120, 206), (300, 222), (480, 200), (700, 216), (920, 204), (920, HZ)]), (90, 150, 120))
    # ground bands + road with rumble strips
    ys = depth_ys()
    for i, (ya, yb) in enumerate(zip(ys, ys[1:])):
        flat(c, RRect(-10, yb, 910, ya + 1, 0), (90, 180, 80) if i % 2 else (80, 166, 72))
        wa, wb = road_hw(ya), road_hw(yb)
        flat(c, Poly([(VX - wb, yb), (VX + wb, yb), (VX + wa, ya + 1), (VX - wa, ya + 1)]), (110, 110, 120) if i % 2 else (104, 104, 114))
        rs = (230, 50, 50) if i % 2 else (250, 250, 250)
        for side in (-1, 1):
            flat(c, Poly([(VX + side * wb, yb), (VX + side * wb * 1.12, yb), (VX + side * wa * 1.12, ya + 1), (VX + side * wa, ya + 1)]), rs)
    # roadside objects (scaled with depth)
    def at(f, side, off):
        y = HZ + (H - HZ) * f
        return VX + side * (road_hw(y) * 1.12 + off * f), y, f
    for f, side in ((0.22, -1), (0.34, 1), (0.5, -1), (0.12, 1)):
        x, y, s = at(f, side, 120)
        flat(c, Thick(x, y, x + side * 10 * s, y - 220 * s, 12 * s), (150, 110, 70))
        tx, ty = x + side * 10 * s, y - 220 * s
        cols = (60, 160, 80) if not (f == 0.5 and "palm" in d) else (220, 150, 50)
        for a in (200, 240, 290, 330, 20, 160):
            r = math.radians(a)
            flat(c, Poly([(tx, ty), (tx + math.cos(r) * 90 * s, ty + math.sin(r) * 50 * s + 30 * s), (tx + math.cos(r) * 50 * s, ty + math.sin(r) * 30 * s - 8 * s)]), cols)
    # chevron curve signs (right)
    for f in (0.62, 0.42):
        x, y, s = at(f, 1, 60)
        flat(c, [Thick(x, y, x, y - 70 * s, 4 * s)], (90, 90, 100))
        arrow = (250, 200, 40) if not (f == 0.62 and "sign" in d) else (60, 200, 230)
        toon(c, RRect(x - 50 * s, y - 130 * s, x + 50 * s, y - 70 * s, 4 * s), arrow, w=1.5, shadow=None)
        for k in range(2):
            ax = x - 28 * s + k * 34 * s
            flat(c, Poly([(ax, y - 122 * s), (ax + 16 * s, y - 122 * s), (ax + 34 * s, y - 100 * s), (ax + 16 * s, y - 78 * s), (ax, y - 78 * s),
                          (ax + 18 * s, y - 100 * s)]), (30, 30, 36))
    # checkpoint arch
    f = 0.3
    y = HZ + (H - HZ) * f
    hw = road_hw(y) * 1.3
    toon(c, [RRect(VX - hw - 14, y - 150, VX - hw, y, 2), RRect(VX + hw, y - 150, VX + hw + 14, y, 2)], (230, 230, 236), w=1.5, shadow=None)
    banner = (230, 60, 60) if "arch" not in d else (60, 160, 90)
    toon(c, RRect(VX - hw - 20, y - 176, VX + hw + 20, y - 140, 4), banner, w=1.5, shadow=None)
    for k in range(10):
        flat(c, RRect(VX - hw + k * hw / 5, y - 170, VX - hw + k * hw / 5 + 8, y - 164, 0), (250, 250, 250) if k % 2 else (30, 30, 36))
    glyph_line(c, VX - 60, VX + 70, y - 152, (250, 250, 250), 1661, w=2.4, size=12)
    # rivals
    car_rear(c, 400, HZ + (H - HZ) * 0.24, 0.4, (60, 120, 220))
    car_rear(c, 540, HZ + (H - HZ) * 0.42, 0.7, (250, 200, 50) if "rival" not in d else (160, 80, 200), spoiler=(40, 40, 50))
    # player's car
    car_rear(c, VX, 586, 2.1, (230, 50, 50), spoiler=(40, 40, 50) if "spoiler" not in d else (250, 250, 250))
    # HUD
    flat(c, RRect(16, 14, 210, 60, 6), (20, 20, 40, 0.75))
    digits(c, 28, 24, "0123", (250, 250, 250), 5)
    flat(c, RRect(140, 30, 146, 36, 0), (250, 250, 250))
    flat(c, RRect(380, 12, 520, 70, 8), (20, 20, 40, 0.75))
    digits(c, 400, 20, "2", (250, 210, 60), 9)
    glyph_line(c, 440, 512, 44, (250, 210, 60), 1662, w=3, size=14)
    # minimap
    flat(c, RRect(730, 14, 886, 136, 8), (20, 20, 40, 0.75))
    c.ellipse_ring(808, 75, 56, 40, 5, (220, 220, 230))
    flat(c, Circ(770, 46, 6), (230, 50, 50))
    flat(c, Circ(852, 90, 6), (250, 200, 50))
    flat(c, Circ(820, 116, 6), (60, 120, 220))
    # lap + nitro (bottom left)
    flat(c, RRect(16, 500, 210, 586, 8), (20, 20, 40, 0.75))
    digits(c, 30, 512, "2", (250, 250, 250), 6)
    flat(c, Thick(62, 538, 76, 512, 3), (250, 250, 250))
    digits(c, 84, 512, "3", (250, 250, 250), 6)
    flat(c, RRect(30, 556, 196, 574, 4), (60, 60, 80))
    flat(c, RRect(32, 558, 150 if "nitro" not in d else 90, 572, 3), (60, 200, 240))
    # speedometer (bottom right)
    flat(c, Circ(820, 530, 66), (20, 20, 40, 0.8))
    c.ellipse_ring(820, 530, 60, 60, 4, (220, 220, 230), ymax=545)
    for k in range(9):
        a = math.radians(160 + k * 27.5)
        flat(c, Thick(820 + math.cos(a) * 48, 530 + math.sin(a) * 48, 820 + math.cos(a) * 58, 530 + math.sin(a) * 58, 2.4),
             (250, 80, 80) if k > 6 else (250, 250, 250))
    digits(c, 788, 556, "248", (250, 210, 60), 4)


def dash(ph):
    return E("dash%d" % int(ph * 10), lambda c, m: flat(c, RRect(VX - 2, HZ + 6, VX + 2, HZ + 14, 0), (250, 250, 250)), pivot=(VX, HZ + 10),
             anim=dict(driftVelocity=(0, -120), driftLength=330, driftGrow=9, driftFade=True, phase=ph))


L166_ELEMENTS = [dash(k / 4) for k in range(4)] + [
    E("needle", lambda c, m: flat(c, Thick(820, 530, 866, 500, 3), (250, 80, 80)), pivot=(820, 530), anim=dict(swingAngle=6, swingSpeed=1.5)),
    E("exhaust", lambda c, m: [piece(c, Circ(x, 572, 9), (220, 220, 226), shadow=None) for x in (360, 540)],
      anim=dict(driftVelocity=(0, 30), driftLength=40, driftFade=True, driftGrow=1.5)),
    E("cloud", lambda c, m: flat(c, [Ell(140, 60, 50, 14), Ell(170, 50, 30, 14)], (250, 250, 255)), anim=drift_across(90, 200, 6, start=140)),
    E("cloud2", lambda c, m: flat(c, [Ell(500, 90, 44, 12), Ell(520, 80, 26, 12)], (250, 250, 255)), anim=drift_across(456, 546, 4, start=500)),
]

L166_DIFFS = [
    ("sun", 690, 130, 0),
    ("snow", 250, 130, 0),
    ("palm", 200, 280, 0),
    ("sign", 790, 400, 0),
    ("arch", 450, 322, 0),
    ("rival", 540, 380, 0),
    ("spoiler", 450, 466, 0),
    ("nitro", 120, 565, 0),
]


# =================================================================== Level 167 tower defence
PATH = [(-40, 140), (240, 140), (240, 430), (520, 430), (520, 230), (740, 230), (740, 400), (940, 400)]


def path_shapes(width):
    out = [Thick(a[0], a[1], b[0], b[1], width) for a, b in zip(PATH, PATH[1:])]
    out += [Circ(x, y, width / 2) for x, y in PATH[1:-1]]
    return out


def archer_tower(c, x, base, roof=(200, 70, 60), s=1.0):
    toon(c, [RRect(x - 26 * s, base - 70 * s, x + 26 * s, base, 6 * s)], (170, 166, 170))
    for y in range(int(base - 60 * s), int(base), int(14 * s)):
        flat(c, Thick(x - 24 * s, y, x + 24 * s, y, 1.4), (140, 136, 146))
    toon(c, RRect(x - 32 * s, base - 84 * s, x + 32 * s, base - 66 * s, 3 * s), (160, 110, 70))
    toon(c, Poly([(x - 36 * s, base - 82 * s), (x + 36 * s, base - 82 * s), (x, base - 130 * s)]), roof)
    flat(c, RRect(x - 6 * s, base - 54 * s, x + 6 * s, base - 36 * s, 3 * s), (60, 50, 60))


def cannon_tower(c, x, base, flag=(60, 120, 220), barrel=(60, 60, 70)):
    toon(c, RRect(x - 34, base - 60, x + 34, base, 4), (150, 146, 156))
    for i in range(4):
        toon(c, RRect(x - 34 + i * 18, base - 72, x - 22 + i * 18, base - 58, 2), (150, 146, 156), w=1.5, shadow=None)
    toon(c, [Thick(x - 4, base - 70, x + 30, base - 92, 14)], barrel)
    flat(c, Thick(x + 28, base - 70, x + 28, base - 120, 2), (90, 70, 50))
    toon(c, Poly([(x + 28, base - 120), (x + 56, base - 112), (x + 28, base - 102)]), flag, w=1.2, shadow=None)


def crystal_tower(c, x, base, crystal=(150, 100, 240)):
    toon(c, Poly([(x - 30, base), (x + 30, base), (x + 18, base - 70), (x - 18, base - 70)]), (120, 110, 150))
    toon(c, Poly([(x, base - 140), (x + 20, base - 104), (x, base - 70), (x - 20, base - 104)]), crystal)
    flat(c, Poly([(x, base - 136), (x + 8, base - 104), (x, base - 78)]), lit(crystal, 1.3))


def l167_bg(c, d):
    c.rect(0, 0, W, H, (120, 196, 100))
    rnd = random.Random(1670)
    for _ in range(26):
        x, y = rnd.uniform(0, W), rnd.uniform(40, 540)
        flat(c, Ell(x, y, rnd.uniform(30, 70), rnd.uniform(14, 26)), (130, 206, 108))
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(40, 540)
        flat(c, [Thick(x, y, x - 3, y - 7, 1.6), Thick(x, y, x + 3, y - 7, 1.6)], (90, 160, 80))
    # path
    piece(c, path_shapes(68), (170, 130, 80), shadow=None)
    flat(c, path_shapes(56), (226, 196, 140))
    for _ in range(50):
        t = rnd.randrange(len(PATH) - 1)
        (ax, ay), (bx, by) = PATH[t], PATH[t + 1]
        u = rnd.random()
        flat(c, Circ(ax + (bx - ax) * u + rnd.uniform(-18, 18) * (ay != by), ay + (by - ay) * u + rnd.uniform(-18, 18) * (ax != bx), 3), (206, 176, 120))
    # spawn cave (left) + castle (right)
    toon(c, [Ell(30, 150, 70, 70)], (130, 120, 130))
    flat(c, Ell(36, 160, 36, 40), (40, 30, 50))
    flat(c, [Circ(28, 150, 4), Circ(44, 150, 4)], (250, 80, 80))
    toon(c, [RRect(800, 300, 900, 470, 3)], (200, 196, 206))
    for i in range(6):
        toon(c, RRect(800 + i * 17, 284, 812 + i * 17, 304, 2), (200, 196, 206), w=1.5, shadow=None)
    toon(c, RRect(820, 360, 870, 420, 24), (110, 80, 60), w=1.5, shadow=None)
    flat(c, Thick(850, 284, 850, 220, 3), (90, 70, 50))
    toon(c, Poly([(850, 220), (896, 232), (850, 248)]), (60, 120, 220) if "flag" not in d else (240, 180, 40), w=1.2, shadow=None)
    # trees + rocks
    def tree(x, y, col=(60, 150, 80)):
        toon(c, [RRect(x - 6, y - 10, x + 6, y + 14, 2)], (130, 90, 60), shadow=None)
        toon(c, [Circ(x, y - 26, 24), Circ(x - 18, y - 12, 16), Circ(x + 18, y - 12, 16)], col)
    for x, y in ((90, 60), (370, 70), (470, 120), (860, 110), (100, 520), (380, 520), (640, 520), (30, 330), (870, 520)):
        tree(x, y, (60, 150, 80) if not (x == 470 and "tree" in d) else (230, 140, 50))
    for x, y in ((150, 470), (690, 330), (330, 250)):
        if (x, y) == (690, 330) and "rock" in d:
            continue
        toon(c, Poly([(x - 22, y + 10), (x - 14, y - 12), (x + 6, y - 18), (x + 22, y + 10)]), (160, 156, 166))
    # towers
    archer_tower(c, 150, 330, roof=(200, 70, 60) if "roof" not in d else (60, 120, 200))
    archer_tower(c, 620, 380)
    cannon_tower(c, 380, 360, barrel=(60, 60, 70) if "cannon" not in d else (210, 150, 60))
    crystal_tower(c, 640, 190, crystal=(150, 100, 240) if "crystal" not in d else (60, 200, 140))
    crystal_tower(c, 360, 200)
    # HUD top bar
    flat(c, RRect(0, 0, W, 38, 0), (40, 34, 60, 0.85))
    flat(c, Circ(26, 19, 12), (250, 200, 60))
    flat(c, Circ(26, 19, 6), (220, 160, 40))
    digits(c, 46, 9, "350", (250, 250, 250), 4)
    for k in range(5 if "lives" not in d else 4):
        sprite(c, 330 + k * 30, 7, [".#.#.", "#####", "#####", ".###.", "..#.."], {"#": (240, 60, 80)}, 5)
    digits(c, 700, 9, "3", (250, 250, 250), 4)
    flat(c, Thick(722, 30, 734, 8, 3), (250, 250, 250))
    digits(c, 742, 9, "10", (250, 250, 250), 4)
    flat(c, [RRect(858, 8, 866, 30, 1), RRect(874, 8, 882, 30, 1)], (250, 250, 250))
    # build bar (bottom)
    flat(c, RRect(170, 548, 730, 598, 10), (40, 34, 60, 0.85))
    icons = [(200, 70, 60), (60, 60, 70), (150, 100, 240), (240, 180, 40)]
    for k, col in enumerate(icons):
        x = 220 + k * 140
        flat(c, RRect(x - 34, 554, x + 34, 592, 8), (250, 220, 120) if k == 0 else ((250, 240, 220) if not (k == 3 and "slot" in d) else (170, 220, 250)))
        toon(c, Poly([(x - 14, 586), (x + 14, 586), (x, 560)]) if k != 1 else Circ(x - 10, 574, 12), col, w=1.5, shadow=None)
        digits(c, x + 6, 576, str(50 + k * 25), (60, 50, 60), 2)


def slime_el(eid, x, y, col, vx, length, ph):
    def d(c, m):
        toon(c, [Ell(x, y, 16, 13)], col, w=1.5, shadow=None)
        flat(c, [Circ(x - 5, y - 3, 3), Circ(x + 5, y - 3, 3)], (40, 30, 50))
    return E(eid, d, pivot=(x, y + 13), anim=dict(driftVelocity=(vx, 0), driftLength=length, phase=ph, stretch=(0.12, -0.12), scaleSpeed=2.0))


L167_ELEMENTS = [
    slime_el("slime1", 70, 140, (120, 200, 240), 30, 160, 0.0),
    slime_el("slime2", 70, 140, (240, 120, 160), 30, 160, 0.5),
    slime_el("slime3", 270, 430, (120, 220, 120), 30, 230, 0.2),
    slime_el("slime4", 545, 230, (250, 200, 80), 30, 170, 0.6),
    E("arrow", lambda c, m: flat(c, Thick(176, 200, 196, 186, 2), (90, 60, 40)), anim=dict(driftVelocity=(50, 40), driftLength=60, driftFade=True)),
    E("glowc", lambda c, m: soft_union(c, [Circ(360, 96, 14)], (200, 170, 255), 0.6, spread=24), daynight="untinted", anim=dict(pulse=0.2, scaleSpeed=1.0)),
    E("pointer", lambda c, m: toon(c, Poly([(220, 548), (210, 530), (230, 530)]), (250, 250, 250), w=1.2, shadow=None), daynight="untinted",
      anim=dict(bobAmplitude=(0, 5), bobSpeed=1.2)),
]

L167_DIFFS = [
    ("flag", 872, 234, 0),
    ("tree", 470, 100, 0),
    ("rock", 690, 326, 0),
    ("roof", 150, 222, 0),
    ("cannon", 393, 280, 0),
    ("crystal", 640, 84, 0),
    ("lives", 450, 19, 0),
    ("slot", 640, 574, 0),
]


# =================================================================== Level 168 match-3 puzzle
BX, BY, CELL, COLS, ROWS = 226, 136, 56, 8, 7
GEMS = ["ruby", "sapph", "emer", "topaz", "amet", "amber"]
GEM_COL = {"ruby": (230, 50, 70), "sapph": (50, 110, 230), "emer": (40, 180, 100), "topaz": (250, 200, 40), "amet": (170, 80, 220), "amber": (250, 140, 40)}


def gem(c, kind, cx, cy, r=21):
    col = GEM_COL[kind]
    if kind == "ruby":
        shapes = [Circ(cx, cy, r)]
    elif kind == "sapph":
        shapes = [Poly([(cx, cy - r), (cx + r * 0.8, cy + r * 0.2), (cx, cy + r), (cx - r * 0.8, cy + r * 0.2)])]
    elif kind == "emer":
        shapes = [RRect(cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85, 5)]
    elif kind == "topaz":
        shapes = [Poly(star_pts(cx, cy + 2, r * 1.1, r * 0.55))]
    elif kind == "amet":
        shapes = [Poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)])]
    else:
        shapes = [Poly(ngon(cx, cy, r, 6, rot=30))]
    toon(c, shapes, col, w=1.6, shadow=(0, 2, 3, 0.3))
    flat(c, Ell(cx - r * 0.3, cy - r * 0.35, r * 0.28, r * 0.18), lit(col, 1.6))


def board_layout():
    rnd = random.Random(1680)
    grid = [[None] * COLS for _ in range(ROWS)]
    for j in range(ROWS):
        for i in range(COLS):
            opts = [g for g in GEMS if not (i >= 2 and grid[j][i - 1] == grid[j][i - 2] == g) and not (j >= 2 and grid[j - 1][i] == grid[j - 2][i] == g)]
            grid[j][i] = rnd.choice(opts)
    return grid


GRID = board_layout()
SWAPS = {"gem1": (1, 1, "amber"), "gem2": (6, 2, "emer"), "gem3": (3, 5, "topaz"), "gem4": (7, 6, "sapph")}


def cell_c(i, j):
    return BX + i * CELL + CELL / 2, BY + j * CELL + CELL / 2


def l168_bg(c, d):
    c.gradient(0, H, (130, 90, 200), (250, 170, 200))
    rnd = random.Random(1681)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 300)
        flat(c, Poly(star_pts(x, y, 4, 1.5, points=4, rot=0)), (255, 240, 220))
    flat(c, [Ell(120, 560, 260, 110), Ell(780, 560, 260, 110)], (120, 80, 170))
    flat(c, [Ell(450, 620, 420, 120)], (140, 100, 190))
    # far castle silhouette
    flat(c, [RRect(380, 70, 520, 140, 0), RRect(360, 40, 392, 140, 0), RRect(508, 40, 540, 140, 0), RRect(436, 20, 464, 140, 0)], (160, 120, 210))
    flat(c, [Poly([(356, 40), (396, 40), (376, 10)]), Poly([(504, 40), (544, 40), (524, 10)]), Poly([(432, 20), (468, 20), (450, -10)])], (160, 120, 210))
    # top banner + star progress
    toon(c, RRect(300, 16, 600, 70, 20), (250, 240, 220))
    flat(c, RRect(320, 48, 580, 60, 6), (200, 180, 200))
    flat(c, RRect(320, 48, 500, 60, 6), (250, 120, 160))
    for k, x in enumerate((380, 460, 540)):
        filled = k < 2 or (k == 2 and "star" in d)
        toon(c, Poly(star_pts(x, 34, 19, 9)), (250, 200, 40) if filled else (200, 190, 200), w=1.4, shadow=None)
    # board
    toon(c, RRect(BX - 14, BY - 14, BX + COLS * CELL + 14, BY + ROWS * CELL + 14, 18), (70, 50, 110), w=2.5)
    for j in range(ROWS):
        for i in range(COLS):
            flat(c, RRect(BX + i * CELL + 2, BY + j * CELL + 2, BX + (i + 1) * CELL - 2, BY + (j + 1) * CELL - 2, 8),
                 (100, 80, 150) if (i + j) % 2 else (90, 70, 140))
    swaps = {(i, j): k for key, (i, j, k) in SWAPS.items() if key in d}
    for j in range(ROWS):
        for i in range(COLS):
            gem(c, swaps.get((i, j), GRID[j][i]), *cell_c(i, j))
    # left: mascot (owl wizard) on a pedestal
    toon(c, RRect(30, 470, 190, 520, 10), (200, 170, 120))
    toon(c, [Ell(110, 410, 56, 64)], (180, 130, 90))
    flat(c, Ell(110, 430, 36, 40), (240, 220, 190))
    for ex in (88, 132):
        toon(c, Circ(ex, 384, 16), (250, 250, 250), w=1.5, shadow=None)
        flat(c, Circ(ex + 3, 386, 7), (40, 30, 50))
    flat(c, Poly([(102, 400), (118, 400), (110, 414)]), (250, 160, 40))
    hat = (60, 90, 200) if "hat" not in d else (220, 60, 90)
    toon(c, [Poly([(50, 350), (170, 350), (120, 250)]), Ell(110, 352, 70, 12)], hat)
    flat(c, Poly(star_pts(116, 310, 12, 5)), (250, 220, 80))
    toon(c, [Thick(168, 470, 186, 330, 6)], (140, 90, 50), w=1.5, shadow=None)
    # speech bubble
    toon(c, [Ell(110, 180, 70, 44), Poly([(110, 210), (130, 210), (100, 250)])], (250, 250, 250))
    glyph_line(c, 66, 160, 172, (90, 70, 120), 1682, w=2.4, size=12)
    glyph_line(c, 76, 146, 194, (90, 70, 120), 1683, w=2.4, size=12)
    # right panels: score, moves, goals
    toon(c, RRect(706, 110, 880, 190, 14), (250, 240, 220))
    glyph_line(c, 720, 800, 130, (140, 110, 160), 1684, w=2, size=10)
    digits(c, 720, 150, "48250", (90, 60, 120), 5)
    toon(c, RRect(706, 210, 880, 330, 14), (250, 240, 220))
    glyph_line(c, 720, 800, 230, (140, 110, 160), 1685, w=2, size=10)
    digits(c, 748, 250, "18", (230, 60, 90) if "moves" not in d else (60, 140, 220), 12)
    toon(c, RRect(706, 350, 880, 520, 14), (250, 240, 220))
    for k, kind in enumerate(("ruby", "emer", "amet")):
        gem(c, kind if not (k == 2 and "goal" in d) else "sapph", 740, 390 + k * 46, r=16)
        digits(c, 780, 380 + k * 46, ("12", "7", "9")[k], (90, 60, 120), 5)
    # boosters (bottom)
    for k, (x, col) in enumerate(((330, (220, 120, 60)), (450, (60, 170, 220)), (570, (240, 70, 90)))):
        if k == 1 and "booster" in d:
            col = (120, 200, 90)
        toon(c, Circ(x, 568, 26), (250, 240, 220))
        toon(c, Circ(x, 568, 16), col, w=1.4, shadow=None)
    flat(c, [Thick(326, 576, 338, 556, 4)], (110, 70, 40))


def sparkle_el(eid, i, j, ph):
    x, y = cell_c(i, j)

    def d(c, m):
        flat(c, Poly(star_pts(x + 12, y - 12, 9, 2, points=4, rot=0)), (255, 255, 240))
    return E(eid, d, daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=0.7, phase=ph))


L168_ELEMENTS = [sparkle_el("sp%d" % k, i, j, k * 0.27) for k, (i, j) in enumerate(((4, 0), (0, 4), (5, 4), (2, 3)))] + [
    E("hand", lambda c, m: toon(c, [RRect(x, y, x + 20, y + 30, 8) for x, y in ((BX + 4 * CELL + 30, BY + 3 * CELL + 30),)] +
                             [RRect(BX + 4 * CELL + 30, BY + 3 * CELL + 10, BX + 4 * CELL + 38, BY + 3 * CELL + 36, 4)], (250, 226, 200), w=1.4),
      daynight="untinted", anim=dict(bobAmplitude=(-12, 12), bobSpeed=0.8)),
    E("mascot_wing", lambda c, m: toon(c, [Ell(160, 420, 14, 30)], (160, 110, 76), w=1.5, shadow=None), pivot=(160, 396),
      anim=dict(swingAngle=14, swingSpeed=0.8)),
    E("glint", lambda c, m: flat(c, Poly(star_pts(500, 34, 10, 2, points=4, rot=0)), (255, 255, 255)), daynight="untinted",
      anim=dict(blinkInterval=2.0, blinkDuration=0.5)),
]

L168_DIFFS = [
    ("gem1", 310, 220, 0),
    ("gem2", 590, 276, 0),
    ("gem3", 422, 444, 0),
    ("gem4", 646, 500, 0),
    ("star", 540, 34, 0),
    ("hat", 110, 306, 0),
    ("moves", 790, 280, 0),
    ("goal", 740, 482, 0),
    ("booster", 450, 568, 0),
]


# =================================================================== Level 169 esports arena (real world, paper-craft)
TEAM_A, TEAM_B = (60, 140, 240), (230, 60, 80)


def gamer(c, x, base, jersey, headset, flip=False, h=1.5):
    k = -1 if flip else 1
    dpiece(c, [RRect(x - 14 * h * k - 4, base - 46 * h, x - 14 * h * k + 4, base, 2)], (40, 40, 50), shadow=SMALL)         # chair back
    hx, hy = modern(c, x, base, jersey, bottom=(40, 40, 50), hair=(40, 30, 30), h=h)
    flat(c, [Thick(hx - 8 * h, hy - 7 * h, hx + 8 * h, hy - 7 * h, 3 * h), Thick(hx + 7 * h * k, hy + 2 * h, hx + 12 * h * k, hy + 6 * h, 1.6 * h)], headset)
    flat(c, [Ell(hx - 8 * h, hy, 4.4 * h, 5.6 * h), Ell(hx + 8 * h, hy, 4.4 * h, 5.6 * h)], headset)


def monitor(c, x, base, col=(120, 200, 255)):
    """Monitor seen from behind on the desk in front of a player (screen glow on its rim)."""
    soft_union(c, [RRect(x - 28, base - 58, x + 28, base - 26, 2)], col, 0.35, spread=8)
    dpiece(c, RRect(x - 28, base - 58, x + 28, base - 26, 2), (36, 36, 48), shadow=SMALL)
    flat(c, RRect(x - 5, base - 26, x + 5, base - 16, 0), (60, 60, 70))
    dpiece(c, RRect(x - 46, base - 18, x + 46, base - 10, 1), (70, 70, 90), shadow=SMALL)


def emblem(c, x, y, s, col, kind):
    if kind == "shield":
        dpiece(c, Poly([(x - 30 * s, y - 34 * s), (x + 30 * s, y - 34 * s), (x + 30 * s, y + 4 * s), (x, y + 36 * s), (x - 30 * s, y + 4 * s)]), col)
        flat(c, Poly([(x - 18 * s, y - 10 * s), (x, y + 8 * s), (x + 18 * s, y - 10 * s), (x + 18 * s, y + 4 * s), (x, y + 22 * s), (x - 18 * s, y + 4 * s)]),
             (250, 250, 250))
    else:
        dpiece(c, Circ(x, y, 34 * s), col)
        flat(c, Poly(star_pts(x, y + 2 * s, 24 * s, 10 * s)), (250, 250, 250))


def l169_bg(c, d):
    c.rect(0, 0, W, H, (30, 28, 46))
    # truss
    for x in range(0, W + 40, 40):
        flat(c, [Thick(x, 6, x + 20, 26, 2), Thick(x + 40, 6, x + 20, 26, 2)], (80, 80, 96))
    flat(c, [Thick(0, 6, W, 6, 3), Thick(0, 26, W, 26, 3)], (90, 90, 106))
    for x in (90, 250, 650, 810):
        dpiece(c, RRect(x - 12, 26, x + 12, 46, 3), (50, 50, 60), shadow=SMALL)
    # side screens with team emblems
    for x, col, kind, key in ((120, TEAM_A, "shield", "emblemA"), (780, TEAM_B, "star", None)):
        dpiece(c, RRect(x - 90, 60, x + 90, 200, 4), (20, 20, 30))
        flat(c, RRect(x - 82, 68, x + 82, 192, 2), lit(col, 0.45))
        emblem(c, x, 128, 1.3, col if not (key and key in d) else (250, 180, 40), kind)
    # main screen with the game map
    dpiece(c, RRect(240, 40, 660, 270, 6), (20, 20, 30))
    flat(c, RRect(250, 50, 650, 260, 3), (60, 120, 70))
    flat(c, Poly([(250, 230), (620, 50), (650, 50), (650, 80), (280, 260), (250, 260)]), (70, 140, 200))       # river
    flat(c, [Thick(290, 240, 290, 80, 10), Thick(290, 80, 610, 80, 10), Thick(290, 240, 610, 240, 10), Thick(610, 240, 610, 80, 10),
             Thick(300, 230, 600, 90, 10)], (200, 180, 130))
    flat(c, RRect(260, 214, 316, 256, 4), TEAM_A)
    flat(c, RRect(584, 54, 640, 96, 4), TEAM_B)
    for k, (x, y, col) in enumerate(((290, 180, TEAM_A), (350, 240, TEAM_A), (380, 175, TEAM_A), (610, 140, TEAM_B), (550, 80, TEAM_B), (520, 135, TEAM_B))):
        if k == 4 and "tower" in d:
            col = (250, 200, 40)
        flat(c, Circ(x, y, 13), col)
        flat(c, Circ(x, y, 5), (250, 250, 250))
    # HUD strip on the screen: kill score
    flat(c, RRect(390, 50, 510, 76, 0), (20, 20, 30))
    digits(c, 400, 56, "12", TEAM_A, 3)
    digits(c, 470, 56, "9", TEAM_B, 3)
    # team booths
    for x0, x1, col, flip, seed in ((20, 330, TEAM_A, False, 0), (570, 880, TEAM_B, True, 1)):
        dpiece(c, RRect(x0, 220, x1, 340, 6), (44, 46, 70))
        flat(c, RRect(x0 + 6, 226, x1 - 6, 334, 4), (60, 70, 100))
        strip = col if not (seed == 1 and "strip" in d) else (90, 220, 120)
        flat(c, RRect(x0, 334, x1, 344, 2), strip)
        sign_box(c, x0 + 90, 228, x1 - 90, 248, lit(col, 0.7), 1690 + seed, vertical=False)
        for k in range(3):
            gx = x0 + 60 + k * 95 if not flip else x1 - 60 - k * 95
            hs = (250, 250, 250)
            if seed == 0 and k == 1 and "headset" in d:
                hs = (250, 200, 40)
            gamer(c, gx, 330, col, hs, flip=flip, h=1.5)
            monitor(c, gx, 336)
    # stage + trophy
    dpiece(c, RRect(-10, 340, 910, 400, 2), (50, 50, 70), shadow=LAYER)
    flat(c, RRect(-10, 392, 910, 400, 0), (110, 110, 140))
    dpiece(c, RRect(410, 300, 490, 344, 3), (230, 230, 240))
    cup = (240, 196, 70) if "trophy" not in d else (200, 204, 216)
    dpiece(c, [Poly([(424, 240), (476, 240), (466, 276), (434, 276)]), RRect(440, 274, 460, 290, 1), RRect(428, 288, 472, 300, 2)], cup)
    flat(c, [Thick(424, 248, 412, 262, 4), Thick(476, 248, 488, 262, 4)], cup)
    # caster desk (front left)
    dpiece(c, RRect(30, 420, 230, 470, 4), (60, 60, 90))
    for x in (80, 170):
        modern(c, x, 440, (40, 40, 50), bottom=(40, 40, 50), hair=(60, 50, 50), h=1.3)
        flat(c, Thick(x + 10, 400, x + 18, 380, 2), (200, 200, 210))
    flat(c, RRect(30, 446, 230, 456, 0), TEAM_A)
    # camera crane (right)
    dpiece(c, [Thick(800, 520, 860, 410, 8), RRect(780, 510, 880, 530, 3)], (70, 70, 84))
    dpiece(c, RRect(700, 390, 760, 424, 3), (40, 40, 50))
    flat(c, Thick(760, 404, 860, 410, 6), (70, 70, 84))
    # crowd (foreground silhouettes)
    rnd = random.Random(1691)
    for row, base in enumerate((540, 600)):
        x = -10 + row * 18
        while x < 920:
            col = (40 + row * 10, 38 + row * 10, 60 + row * 10)
            flat(c, [Ell(x, base, 20, 30), Circ(x, base - 40, 13)], col)
            x += 38 * rnd.uniform(0.85, 1.15)
    # fan banner held up in the crowd
    banner = TEAM_B if "banner" not in d else (90, 220, 120)
    dpiece(c, RRect(520, 470, 640, 516, 2), banner, shadow=SMALL)
    glyph_line(c, 532, 636, 493, (250, 250, 250), 1692, w=3, size=12)
    flat(c, [Thick(530, 516, 530, 560, 3), Thick(630, 516, 630, 560, 3)], (60, 58, 80))


def stick_el(x, y, col, ph):
    def d(c, m):
        flat(c, Thick(x, y, x, y - 34, 4), col)
        soft_union(c, [Thick(x, y - 4, x, y - 34, 4)], col, 0.5, spread=8)
    return E("stick%d" % x, d, pivot=(x, y), daynight="untinted", anim=dict(swingAngle=22, swingSpeed=0.9, phase=ph))


def beam_el(eid, x, angle_ph):
    def d(c, m):
        soft_union(c, [Poly([(x - 8, 46), (x + 8, 46), (x + 80, 380), (x - 80, 380)])], (200, 210, 255), 0.18, spread=16)
    return E(eid, d, pivot=(x, 46), daynight="untinted", anim=dict(swingAngle=14, swingSpeed=0.15, phase=angle_ph, twinkle=0.4, twinkleSpeed=0.6))


L169_ELEMENTS = [beam_el("beam1", 250, 0.0), beam_el("beam2", 650, 0.5)] + [
    stick_el(x, y, col, i * 0.17) for i, (x, y, col) in enumerate(((60, 520, TEAM_A), (180, 510, TEAM_A), (300, 530, TEAM_A), (420, 520, TEAM_B),
                                                                    (700, 520, TEAM_B), (820, 530, TEAM_B)))] + [
    E("glow", lambda c, m: soft_union(c, [RRect(250, 50, 650, 260, 3)], (150, 220, 160), 0.18, spread=30), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.8)),
    E("tally", lambda c, m: flat(c, Circ(748, 398, 4), (250, 60, 60)), daynight="untinted", anim=dict(blinkInterval=1.0, blinkDuration=0.5)),
]

L169_DIFFS = [
    ("emblemA", 120, 128, 0),
    ("tower", 550, 80, 0),
    ("strip", 725, 339, 0),
    ("headset", 176, 260, 0),
    ("trophy", 450, 268, 0),
    ("banner", 580, 493, 0),
]


LEVELS = [
    ("Level165", "像素RPG村庄", l165_bg, L165_ELEMENTS, L165_DIFFS, 60, OPTS),
    ("Level166", "赛车游戏", l166_bg, L166_ELEMENTS, L166_DIFFS, 60, OPTS),
    ("Level167", "塔防游戏", l167_bg, L167_ELEMENTS, L167_DIFFS, 60, OPTS),
    ("Level168", "宝石消除", l168_bg, L168_ELEMENTS, L168_DIFFS, 60, OPTS),
    ("Level169", "电竞赛场", l169_bg, L169_ELEMENTS, L169_DIFFS, 60, OPTS),
]
