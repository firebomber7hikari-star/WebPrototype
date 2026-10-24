# -*- coding: utf-8 -*-
"""Inside video games, part 2 (all designs original: no real games, characters, brands or logos):
  Level175 像素城堡探险 - a pixel side-scrolling castle: moonlit windows, platforms, candles, orb pedestal, HP / MP HUD
  Level176 回合制战斗   - a turn-based battle screen: slime king and mushroom monster vs. a chibi party, command menu
  Level177 农场模拟     - a cosy farm sim (top-down): crop plots, barn, pond, scarecrow, calendar and tool bar
  Level178 城市建造     - an isometric city builder: roads, tower, factory, park, houses, build menu
  Level179 节奏音游     - a rhythm game: four lanes of falling notes, idol singer, combo counter, speakers
  Level180 弹球台       - a pinball table: bumpers, ramps, drop targets, flippers, backglass score
  Level181 卡牌对战     - a card battle board: portraits, creature cards with gems, mana crystals, hand, end-turn button
  Level182 星际驾驶舱   - a spaceship cockpit: planet, station, asteroids outside; radar, screens, throttle inside
  Level183 推箱子       - a pixel box-pushing puzzle in a warehouse
  Level184 钓鱼游戏     - a fishing game: dock and boat above, underwater cross-section, tension gauge
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from levels_retro import block, digits, sprite
from levels_gamecontent import OUTLINE, glyph_line, rpg_house, toon

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 220, 190)


def rot_poly(cx, cy, w, h, ang):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return Poly([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))])


def chibi(c, x, base, s=1.0, hair=(150, 90, 40), outfit=(60, 110, 210), face=1, hat=None, skin=SKIN, weapon=None):
    """Big-headed cartoon game character."""
    if weapon == "sword":
        toon(c, Thick(x + 16 * s * face, base - 20 * s, x + 30 * s * face, base - 62 * s, 4 * s), (220, 226, 236), w=1.4, shadow=None)
    elif weapon == "staff":
        toon(c, [Thick(x + 18 * s * face, base, x + 18 * s * face, base - 70 * s, 3.4 * s), Circ(x + 18 * s * face, base - 74 * s, 7 * s)],
             (150, 100, 60), w=1.4, shadow=None)
        flat(c, Circ(x + 18 * s * face, base - 74 * s, 4.6 * s), (120, 220, 255))
    toon(c, RRect(x - 14 * s, base - 34 * s, x + 14 * s, base - 2 * s, 6 * s), outfit)
    flat(c, [RRect(x - 10 * s, base - 8 * s, x - 3 * s, base, 2), RRect(x + 3 * s, base - 8 * s, x + 10 * s, base, 2)], (70, 50, 40))
    toon(c, Circ(x, base - 54 * s, 22 * s), skin)
    toon(c, [Ell(x - 3 * s * face, base - 66 * s, 24 * s, 13 * s), Ell(x - 16 * s * face, base - 54 * s, 9 * s, 14 * s)], hair, w=1.6, shadow=None)
    for ex in (x + 1 * s * face, x + 13 * s * face):
        flat(c, Ell(ex, base - 50 * s, 3 * s, 4.6 * s), (40, 30, 50))
        flat(c, Circ(ex + 1 * s, base - 52 * s, 1.2 * s), (250, 250, 250))
    flat(c, Ell(x + 8 * s * face, base - 40 * s, 3 * s, 1.6 * s), (230, 120, 120))
    if hat:
        toon(c, [Ell(x, base - 70 * s, 28 * s, 6 * s), Poly([(x - 16 * s, base - 72 * s), (x + 16 * s, base - 72 * s), (x - 10 * s * face, base - 112 * s)])],
             hat, w=1.6, shadow=None)


def bar(c, x0, y0, x1, y1, frac, col, back=(40, 36, 56)):
    flat(c, RRect(x0 - 2, y0 - 2, x1 + 2, y1 + 2, 3), (250, 250, 250))
    flat(c, RRect(x0, y0, x1, y1, 2), back)
    flat(c, RRect(x0, y0, x0 + (x1 - x0) * frac, y1, 2), col)


# =================================================================== Level 175 pixel castle
def l175_bg(c, d):
    c.rect(0, 0, W, H, (54, 46, 76))
    for r, y in enumerate(range(40, 510, 20)):
        off = (r % 2) * 20
        for x in range(-off, W, 40):
            flat(c, RRect(x + 1, y + 1, x + 39, y + 19, 0), (62, 54, 86) if (x // 40 + r) % 3 else (58, 50, 80))
    # arched windows (pixel steps)
    for k, x in enumerate((130, 450, 770)):
        for j, w in enumerate((40, 60, 70, 76, 80)):
            flat(c, RRect(x - w / 2 - 8, 70 + j * 10 - 8, x + w / 2 + 8, 80 + j * 10, 0), (90, 84, 110))
        flat(c, RRect(x - 48, 110, x + 48, 250, 0), (90, 84, 110))
        for j, w in enumerate((40, 60, 70, 76, 80)):
            flat(c, RRect(x - w / 2, 70 + j * 10, x + w / 2, 80 + j * 10, 0), (24, 30, 70))
        flat(c, RRect(x - 40, 120, x + 40, 242, 0), (24, 30, 70))
        rnd = random.Random(1750 + k)
        for _ in range(8):
            sx, sy = rnd.randrange(int(x) - 36, int(x) + 32, 4), rnd.randrange(76, 236, 4)
            flat(c, RRect(sx, sy, sx + 4, sy + 4, 0), (250, 250, 220))
        if k == 1:
            sprite(c, x - 20, 120, ["..####..", ".######.", "########", "########", "########", ".######.", "..####.."],
                   {"#": (250, 240, 170) if "moon" not in d else (250, 140, 120)}, 5)
        flat(c, [RRect(x - 2, 70, x + 2, 242, 0), RRect(x - 40, 160, x + 40, 164, 0)], (90, 84, 110))
    # columns + banners
    for k, x in enumerate((290, 610)):
        flat(c, RRect(x - 20, 40, x + 20, 510, 0), (84, 76, 104))
        flat(c, RRect(x - 20, 40, x - 14, 510, 0), (100, 92, 120))
        col = (180, 40, 60) if not (k == 1 and "banner" in d) else (60, 140, 90)
        sprite(c, x - 20, 60, ["##########"] * 18 + ["####..####", "###....###", "##......##"], {"#": col}, 4)
        sprite(c, x - 8, 96, ["..##..", ".####.", "######", ".####.", "..##.."], {"#": (240, 200, 70)}, 4)
    # platforms, ladder, floor
    for x0, x1, y in ((30, 240, 390), (360, 540, 300), (660, 860, 400)):
        for x in range(x0, x1, 30):
            block(c, x, y, 30, (130, 124, 150), kind="stone")
    for y in range(330, 510, 18):
        flat(c, RRect(500, y, 530, y + 4, 0), (150, 100, 60))
    flat(c, [RRect(500, 330, 504, 510, 0), RRect(526, 330, 530, 510, 0)], (150, 100, 60))
    for x in range(0, W, 30):
        block(c, x, 510, 30, (120, 114, 140), kind="stone")
        block(c, x, 540, 30, (100, 94, 120), kind="stone")
        block(c, x, 570, 30, (90, 84, 110), kind="stone")
    # candle holders (flames are elements)
    for x, y in ((60, 390), (220, 390), (690, 400), (830, 400)):
        sprite(c, x - 8, y - 24, ["....", "####", ".##.", ".##.", "####"], {"#": (200, 170, 80)}, 4)
    # pedestal + orb
    sprite(c, 426, 252, ["..######..", "...####...", "...####...", "..######..", ".########."], {"#": (170, 160, 190)}, 5)
    sprite(c, 435, 218, ["..##..", ".####.", "######", "######", ".####.", "..##.."], {"#": (90, 220, 240) if "orb" not in d else (240, 90, 160)}, 5)
    # chest on the left platform
    ch = (170, 100, 50) if "chest" not in d else (90, 110, 200)
    sprite(c, 100, 362, [".######.", "########", "#yyyyyy#", "####y###", "########"], {"#": ch, "y": (250, 210, 70)}, 4)
    # door (right)
    door = (130, 80, 40) if "door" not in d else (70, 110, 150)
    sprite(c, 834, 430, ["..####..", ".######.", "########", "########", "########", "######y#", "########", "########", "########", "########"],
           {"#": door, "y": (250, 210, 70)}, 7)
    # HUD
    flat(c, RRect(0, 0, W, 40, 0), (20, 16, 30))
    bar(c, 20, 12, 220, 28, 0.85 if "hp" not in d else 0.45, (220, 50, 60))
    bar(c, 240, 12, 380, 28, 0.6, (60, 120, 230))
    flat(c, RRect(420, 2, 470, 38, 2), (250, 250, 250))
    flat(c, RRect(423, 5, 467, 35, 1), (40, 36, 56))
    icon = ["....##", "...##.", "#.##..", ".##...", "#.#..."] if "item" not in d else [".###..", "####..", ".###..", "..#...", "..#..."]
    sprite(c, 431, 8, icon, {"#": (220, 226, 236) if "item" not in d else (240, 170, 60)}, 5)
    digits(c, 700, 10, "003800", (250, 250, 250), 4)


def l175_hero(c, m):
    sprite(c, 180, 446, ["..hhh...", ".hhhhh..", ".hssss..", ".sesse..", "..ssss..", ".bbbbbb#", "sbbbbbb#", "sbbbbbb.", ".bbbbbb.", ".ll..ll.", ".kk..kk."],
           {"h": (150, 90, 40), "s": (250, 210, 170), "e": (30, 30, 40), "b": (60, 110, 210), "l": (60, 60, 80), "k": (90, 60, 40), "#": (220, 226, 236)}, 6)


def candle(x, y, ph):
    return E("cand%d" % x, lambda c, m: sprite(c, x - 4, y - 36, [".#.", "###", "#y#"], {"#": (250, 140, 40), "y": (255, 230, 120)}, 4),
             daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=3.0, phase=ph))


L175_ELEMENTS = [candle(x, y, i * 0.3) for i, (x, y) in enumerate(((60, 390), (220, 390), (690, 400), (830, 400)))] + [
    E("hero", l175_hero, anim=dict(bobAmplitude=(0, 3), bobSpeed=1.4, bounce=True)),
    E("ghost", lambda c, m: sprite(c, 700, 260, ["..####..", ".######.", "##o##o##", "########", "########", "#.##.##."], {"#": (230, 230, 250), "o": (40, 40, 70)}, 5),
      daynight="untinted", anim=dict(bobAmplitude=(20, 10), bobSpeed=0.3, twinkle=0.4, twinkleSpeed=0.5)),
    E("bat", lambda c, m: sprite(c, 340, 70, ["#.....#", "##.#.##", "#######", ".#.#.#."], {"#": (30, 20, 40)}, 4),
      anim=dict(orbitRadius=(40, 14), orbitSpeed=0.3)),
    E("orbglow", lambda c, m: soft_union(c, [Circ(450, 233, 16)], (150, 220, 255), 0.4, spread=24), daynight="untinted", anim=dict(pulse=0.2, scaleSpeed=0.8)),
]

L175_DIFFS = [
    ("moon", 450, 137, 0),
    ("banner", 610, 100, 0),
    ("orb", 450, 233, 0),
    ("chest", 116, 372, 0),
    ("door", 862, 465, 0),
    ("hp", 170, 20, 0),
    ("item", 445, 20, 0),
]


# =================================================================== Level 176 turn-based battle
def l176_bg(c, d):
    c.gradient(0, 260, (110, 170, 240), (220, 236, 250))
    sun = (250, 220, 90) if "sun" not in d else (250, 140, 90)
    toon(c, Circ(780, 70, 34), sun, w=1.6, shadow=None)
    for x, y, k in ((140, 60, 1.0), (470, 40, 0.8)):
        toon(c, [Circ(x, y, 22 * k), Circ(x + 26 * k, y + 6 * k, 18 * k), Circ(x - 26 * k, y + 6 * k, 16 * k)], (250, 250, 255), w=1.4, shadow=None)
    toon(c, Poly([(-20, 260), (120, 150), (260, 220), (380, 140), (560, 230), (700, 170), (920, 260)]), (130, 150, 200), w=1.6, shadow=None)
    toon(c, Poly([(-20, 260), (900 + 20, 260), (920, 420), (-20, 420)]), (110, 190, 100), w=1.6, shadow=None)
    flat(c, Poly([(380, 260), (520, 260), (700, 420), (200, 420)]), (200, 180, 130))
    # tree on the hill
    tree = (60, 150, 80) if "tree" not in d else (230, 140, 50)
    toon(c, RRect(42, 206, 54, 250, 3), (130, 90, 60), w=1.4, shadow=None)
    toon(c, [Circ(48, 186, 28), Circ(28, 204, 18), Circ(68, 204, 18)], tree, w=1.4)
    for x, y in ((250, 300), (560, 290), (860, 300), (130, 380)):
        flat(c, [Thick(x, y, x - 4, y - 10, 2), Thick(x, y, x + 4, y - 10, 2)], (80, 150, 70))
    # monsters (left)
    toon(c, [Ell(180, 340, 80, 14)], (90, 150, 80), shadow=None)
    toon(c, Poly([(100, 344), (260, 344), (250, 300), (220, 262), (180, 248), (140, 262), (110, 300)]), (90, 200, 240))
    flat(c, Ell(150, 286, 14, 10), (190, 240, 255))
    flat(c, [Ell(160, 300, 8, 11), Ell(205, 300, 8, 11)], (30, 30, 60))
    flat(c, Thick(166, 324, 200, 324, 3), (30, 30, 60))
    crown = (250, 200, 50) if "crown" not in d else (200, 200, 216)
    toon(c, Poly([(150, 252), (210, 252), (216, 214), (196, 232), (180, 206), (164, 232), (144, 214)]), crown, w=1.6)
    flat(c, Circ(180, 236, 5), (220, 40, 60))
    toon(c, [RRect(318, 290, 352, 334, 8)], (246, 236, 210))
    toon(c, Ell(335, 280, 44, 28), (220, 60, 60))
    for sx, sy in ((310, 272), (338, 262), (360, 280), (322, 292)):
        flat(c, Circ(sx, sy, 6), (250, 250, 250) if "spots" not in d else (250, 220, 60))
    flat(c, [Circ(328, 306, 3), Circ(344, 306, 3)], (40, 30, 50))
    # party (right)
    chibi(c, 600, 330, s=1.2, hair=(240, 200, 90), outfit=(220, 80, 120), face=-1, weapon="staff")
    chibi(c, 700, 370, s=1.35, hair=(150, 90, 40) if "hair" not in d else (60, 60, 70), outfit=(60, 110, 210), face=-1, weapon="sword")
    chibi(c, 810, 330, s=1.2, hair=(90, 60, 40), outfit=(110, 70, 170), face=-1, hat=(110, 70, 170) if "hat" not in d else (60, 160, 100), weapon="staff")
    # UI panels
    for x0, x1 in ((10, 330), (340, 890)):
        toon(c, RRect(x0, 420, x1, 592, 10), (250, 250, 250), w=2.5)
        flat(c, RRect(x0 + 6, 426, x1 - 6, 586, 8), (40, 50, 120))
    for k in range(4):
        glyph_line(c, 60, 250, 452 + k * 36, (250, 250, 250), 1760 + k, w=2.4, size=12)
    for r, (hp, mp) in enumerate(((0.8, 0.5), (0.95, 0.7), (0.4, 0.9))):
        y = 452 + r * 46
        glyph_line(c, 360, 470, y, (250, 250, 250), 1765 + r, w=2.2, size=11)
        bar(c, 490, y - 8, 680, y + 6, hp if not (r == 0 and "hpbar" in d) else 0.25, (90, 210, 110))
        bar(c, 700, y - 8, 860, y + 6, mp, (80, 150, 240))


L176_ELEMENTS = [
    E("cursor", lambda c, m: toon(c, Poly([(30, 442), (46, 452), (30, 462)]), (250, 250, 250), w=1.2, shadow=None), daynight="untinted",
      anim=dict(bobAmplitude=(5, 0), bobSpeed=1.5)),
    E("dmg", lambda c, m: digits(c, 196, 190, "128", (250, 250, 250), 5), daynight="untinted", anim=dict(blinkInterval=2.0, blinkDuration=1.0,
                                                                                                         bobAmplitude=(0, 10), bobSpeed=0.5)),
    E("bat", lambda c, m: toon(c, [Poly([(110, 150), (80, 136), (90, 158)]), Poly([(130, 150), (160, 136), (150, 158)]), Circ(120, 152, 10)], (110, 70, 140),
                               w=1.4, shadow=None), pivot=(120, 152), anim=dict(bobAmplitude=(10, 12), bobSpeed=0.6, stretch=(0.2, 0), scaleSpeed=3)),
    E("slash", lambda c, m: flat(c, Thick(150, 230, 230, 330, 4), (255, 255, 255)), daynight="untinted", anim=dict(blinkInterval=2.0, blinkDuration=0.3)),
]

L176_DIFFS = [
    ("sun", 780, 70, 0),
    ("tree", 48, 196, 0),
    ("crown", 180, 230, 0),
    ("spots", 335, 276, 0),
    ("hair", 700, 300, 0),
    ("hat", 810, 210, 0),
    ("hpbar", 585, 452, 0),
]


# =================================================================== Level 177 farm sim
def crop(c, x, y, kind):
    if kind == "carrot":
        flat(c, [Poly([(x - 4, y), (x + 4, y), (x, y + 10)])], (240, 130, 40))
        flat(c, [Thick(x, y, x - 5, y - 10, 2), Thick(x, y, x + 5, y - 10, 2), Thick(x, y, x, y - 12, 2)], (70, 170, 70))
    elif kind == "cabbage":
        toon(c, Circ(x, y, 9), (130, 210, 100), w=1.2, shadow=None)
        flat(c, Circ(x, y, 4), (180, 240, 150))
    elif kind == "wheat":
        flat(c, [Thick(x + k * 4, y + 8, x + k * 5, y - 10, 2) for k in (-1, 0, 1)], (230, 190, 70))
    else:      # pumpkin
        toon(c, Ell(x, y, 15, 11), (240, 140, 40), w=1.2, shadow=None)
        flat(c, [Thick(x - 5, y - 9, x - 5, y + 9, 1.4), Thick(x + 5, y - 9, x + 5, y + 9, 1.4)], (210, 110, 30))
        flat(c, Thick(x, y - 10, x + 3, y - 17, 3), (70, 130, 50))


def l177_bg(c, d):
    c.rect(0, 0, W, H, (130, 200, 100))
    rnd = random.Random(1770)
    for _ in range(30):
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(50, 560), rnd.uniform(20, 50), rnd.uniform(8, 16)), (140, 210, 110))
    # paths
    flat(c, [RRect(0, 230, W, 270, 6), RRect(420, 270, 460, 600, 6)], (220, 196, 140))
    # farmhouse + barn
    rpg_house(c, 40, 50, 230, (90, 120, 190), roof_h=80, wall_h=70, door_x=135)
    rpg_house(c, 640, 40, 860, (200, 60, 50) if "barn" not in d else (120, 120, 140), wall=(200, 80, 70), roof_h=90, wall_h=90, door_x=750)
    flat(c, [Thick(722, 186, 778, 216, 4), Thick(778, 186, 722, 216, 4)], (250, 240, 220))
    # trees with fruit
    for x, y in ((320, 80), (520, 70)):
        toon(c, RRect(x - 6, y + 30, x + 6, y + 60, 2), (130, 90, 60), shadow=None)
        toon(c, [Circ(x, y, 34), Circ(x - 24, y + 18, 22), Circ(x + 24, y + 18, 22)], (70, 160, 80))
        fruit = (220, 50, 60) if not (x == 520 and "fruit" in d) else (250, 200, 50)
        flat(c, [Circ(x - 14, y - 6, 6), Circ(x + 12, y + 4, 6), Circ(x - 2, y + 20, 6)], fruit)
    # crop plots
    plots = [((40, 300, 380, 420), "carrot"), ((40, 440, 380, 560), "cabbage"), ((500, 300, 680, 420), "wheat")]
    for (x0, y0, x1, y1), kind in plots:
        toon(c, RRect(x0, y0, x1, y1, 6), (150, 106, 70), w=1.6, shadow=None)
        for y in range(y0 + 20, y1 - 10, 30):
            flat(c, RRect(x0 + 8, y - 6, x1 - 8, y + 8, 4), (130, 90, 58))
            for x in range(x0 + 24, x1 - 14, 34):
                k = kind
                if kind == "cabbage" and "crop" in d and (x, y) == (200, 520):
                    k = "pumpkin"
                crop(c, x, y, k)
    # scarecrow in the wheat
    flat(c, [Thick(590, 420, 590, 330, 4), Thick(560, 360, 620, 360, 4)], (140, 100, 60))
    toon(c, RRect(576, 346, 604, 386, 4), (200, 80, 80), w=1.4, shadow=None)
    toon(c, Circ(590, 334, 13), (240, 220, 160), w=1.4, shadow=None)
    hat = (190, 150, 80) if "hat" not in d else (70, 100, 190)
    toon(c, [Ell(590, 324, 22, 5), Poly([(578, 324), (602, 324), (596, 306), (584, 306)])], hat, w=1.4, shadow=None)
    # pond with lily pads + fence
    toon(c, Ell(760, 470, 120, 70), (90, 170, 230), w=2)
    flat(c, Ell(740, 456, 80, 40), (110, 190, 240))
    for x, y in ((700, 500), (800, 430), (820, 500)):
        flat(c, Circ(x, y, 12), (80, 170, 90))
    if "lily" not in d:
        flat(c, [Circ(800, 422, 8), Circ(808, 431, 8), Circ(792, 431, 8)], (250, 170, 200))
        flat(c, Circ(800, 428, 4), (250, 230, 120))
    for x in range(500, 690, 22):
        flat(c, RRect(x, 284, x + 6, 300, 1), (250, 240, 220))
    flat(c, RRect(500, 288, 690, 292, 0), (250, 240, 220))
    # chickens
    for x, y in ((520, 470), (560, 500)):
        toon(c, [Ell(x, y, 13, 10), Circ(x + 12, y - 8, 7)], (250, 250, 246), w=1.2, shadow=None)
        flat(c, Poly([(x + 18, y - 9), (x + 24, y - 7), (x + 18, y - 5)]), (250, 180, 40))
    # farmer
    chibi(c, 440, 300, s=1.0, hair=(90, 60, 40), outfit=(90, 140, 200), face=1, hat=None)
    toon(c, [Ell(441, 236, 30, 7), RRect(426, 222, 456, 238, 6)], (230, 200, 120), w=1.4, shadow=None)
    # HUD: calendar, coins, tool bar
    cal = (90, 180, 100) if "season" not in d else (230, 120, 160)
    toon(c, RRect(16, 12, 196, 44, 8), (250, 240, 220), w=1.8, shadow=None)
    flat(c, RRect(22, 18, 70, 38, 5), cal)
    digits(c, 84, 18, "12", (90, 70, 60), 4)
    glyph_line(c, 120, 190, 28, (120, 100, 90), 1771, w=2, size=10)
    toon(c, RRect(720, 548, 890, 590, 8), (250, 240, 220), w=1.8, shadow=None)
    flat(c, Circ(744, 569, 11), (250, 200, 60))
    digits(c, 764, 560, "4820", (90, 70, 60), 4)
    toon(c, RRect(120, 548, 690, 594, 8), (120, 90, 70), w=1.8, shadow=None)
    tools = [(170, 170, 180), (80, 150, 220), (200, 140, 80), (220, 70, 70), (250, 200, 60), (120, 200, 110), (170, 120, 200), (240, 240, 236)]
    if "tool" in d:
        tools[4] = (60, 200, 220)
    for k, col in enumerate(tools):
        x = 130 + k * 70
        flat(c, RRect(x, 554, x + 60, 588, 6), (250, 240, 220) if k else (250, 220, 120))
        toon(c, Circ(x + 30, 571, 11), col, w=1.2, shadow=None)


L177_ELEMENTS = [
    E("duck1", lambda c, m: toon(c, [Ell(700, 450, 14, 9), Circ(712, 442, 7)], (250, 250, 246), w=1.2, shadow=None), anim=dict(bobAmplitude=(30, 4), bobSpeed=0.15)),
    E("duck2", lambda c, m: toon(c, [Ell(780, 480, 12, 8), Circ(790, 473, 6)], (250, 220, 90), w=1.2, shadow=None), anim=dict(bobAmplitude=(-24, 4), bobSpeed=0.18)),
    E("butterfly", lambda c, m: toon(c, [Ell(300, 280, 6, 8), Ell(312, 280, 6, 8)], (250, 180, 220), w=1, shadow=None), pivot=(306, 280),
      anim=dict(orbitRadius=(60, 20), orbitSpeed=0.2, stretch=(0.6, 0), scaleSpeed=4)),
    E("sel", lambda c, m: c.ellipse_ring(160, 571, 34, 20, 3, (250, 250, 250)), daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=1.0)),
]

L177_DIFFS = [
    ("barn", 750, 85, 0),
    ("fruit", 520, 82, 0),
    ("crop", 200, 520, 0),
    ("hat", 590, 316, 0),
    ("lily", 800, 430, 0),
    ("season", 46, 28, 0),
    ("tool", 450, 571, 0),
]


# =================================================================== Level 178 isometric city builder
OX, OY, TW, TH = 450, -180, 30, 15


def P(i, j):
    return (OX + (i - j) * TW, OY + (i + j) * TH)


def iso_box(c, i, j, w, dd, h, top, left=None, right=None):
    left = left or lit(top, 0.82)
    right = right or lit(top, 0.66)
    a, b, cc, d = P(i, j), P(i + w, j), P(i + w, j + dd), P(i, j + dd)
    up = lambda p: (p[0], p[1] - h)
    toon(c, Poly([d, cc, up(cc), up(d)]), left, w=1.2, shadow=None)
    toon(c, Poly([cc, b, up(b), up(cc)]), right, w=1.2, shadow=None)
    toon(c, Poly([up(a), up(b), up(cc), up(d)]), top, w=1.2, shadow=None)
    return up(a), up(b), up(cc), up(d)


def iso_tile(c, i, j, w, dd, col):
    flat(c, Poly([P(i, j), P(i + w, j), P(i + w, j + dd), P(i, j + dd)]), col)


def iso_house(c, i, j, wall, roof):
    a, b, cc, d = iso_box(c, i, j, 1, 1, 22, wall)
    ridge = ((a[0] + d[0]) / 2, (a[1] + d[1]) / 2 - 16), ((b[0] + cc[0]) / 2, (b[1] + cc[1]) / 2 - 16)
    toon(c, Poly([d, cc, ridge[1], ridge[0]]), roof, w=1.2, shadow=None)
    toon(c, Poly([cc, b, ridge[1]]), lit(roof, 0.75), w=1.2, shadow=None)


def iso_tree(c, i, j, col=(70, 160, 80)):
    x, y = P(i + 0.5, j + 0.5)
    flat(c, Ell(x, y, 12, 6), (90, 150, 80))
    toon(c, RRect(x - 3, y - 14, x + 3, y, 1), (130, 90, 60), w=1, shadow=None)
    toon(c, Circ(x, y - 22, 13), col, w=1.2, shadow=None)


def l178_bg(c, d):
    c.rect(0, 0, W, H, (130, 200, 110))
    for k in range(-30, 80):
        flat(c, Thick(*P(k, -40), *P(k, 80), 1), (120, 188, 100))
        flat(c, Thick(*P(-40, k), *P(80, k), 1), (120, 188, 100))
    # river (bottom left)
    flat(c, Poly([P(0, 30), P(10, 30), P(10, 60), P(0, 60)]), (90, 170, 230))
    # roads
    iso_tile(c, 14, -20, 2, 90, (110, 110, 120))
    iso_tile(c, -20, 16, 90, 2, (110, 110, 120))
    for k in range(-20, 70, 2):
        flat(c, Thick(*P(15, k), *P(15, k + 0.8), 2), (250, 250, 240))
        flat(c, Thick(*P(k, 17), *P(k + 0.8, 17), 2), (250, 250, 240))
    objs = []
    # park (west)
    objs.append((30, lambda: iso_tile(c, 7, 19, 6, 6, (110, 190, 100))))
    objs.append((41, lambda: (toon(c, Ell(*P(10, 22), 34, 17), (200, 200, 210), w=1.2, shadow=None),
                              flat(c, Ell(*P(10, 22), 24, 12), (90, 180, 240) if "fountain" not in d else (240, 120, 160)))))
    for i, j in ((7, 19), (12, 19), (7, 24), (12, 24), (8, 21), (12, 22)):
        objs.append((i + j + 1, (lambda i, j: lambda: iso_tree(c, i, j, (70, 160, 80) if not ((i, j) == (12, 24) and "tree" in d) else (230, 140, 50)))(i, j)))
    # downtown tower + offices (north)
    objs.append((24, lambda: iso_box(c, 11, 11, 2, 2, 110, (110, 170, 230) if "tower" not in d else (240, 190, 80), (170, 190, 210), (130, 150, 180))))
    objs.append((22, lambda: iso_box(c, 8, 12, 2, 2, 70, (200, 200, 210))))
    objs.append((26, lambda: iso_box(c, 11, 14, 2, 1, 50, (230, 210, 170))))
    objs.append((20, lambda: iso_box(c, 9, 9, 2, 2, 50, (220, 150, 120))))
    # factory (east) with chimney
    objs.append((30, lambda: iso_box(c, 18, 9, 3, 3, 50, (190, 180, 160))))
    objs.append((32, lambda: (iso_box(c, 21, 10, 1, 1, 120, (170, 150, 140)),
                              flat(c, Poly([(P(21, 11)[0], P(21, 11)[1] - 94), (P(22, 11)[0], P(22, 11)[1] - 94),
                                            (P(22, 11)[0], P(22, 11)[1] - 118), (P(21, 11)[0], P(21, 11)[1] - 118)]),
                                   (220, 60, 60) if "chimney" not in d else (250, 250, 246)))))
    objs.append((32, lambda: iso_box(c, 18, 13, 2, 2, 30, (150, 140, 130))))
    # houses (south)
    roofs = [(200, 70, 60), (70, 120, 190), (90, 160, 90), (220, 160, 60), (160, 90, 160), (200, 70, 60)]
    for k, (i, j) in enumerate(((18, 19), (20, 19), (18, 21), (20, 21), (22, 20), (19, 23), (21, 23), (17, 25), (23, 22), (24, 19))):
        col = roofs[k % len(roofs)]
        if k == 3 and "roof" in d:
            col = (240, 240, 240)
        objs.append((i + j + 2, (lambda i, j, col: lambda: iso_house(c, i, j, (240, 230, 210), col))(i, j, col)))
    # houses (north-west) + trees fill
    for i, j in ((6, 14), (4, 12), (5, 9), (3, 15)):
        objs.append((i + j + 2, (lambda i, j: lambda: iso_house(c, i, j, (240, 220, 200), (190, 90, 70)))(i, j)))
    for i, j in ((24, 8), (25, 12), (26, 15), (3, 19), (2, 23), (14, 27), (25, 26), (19, 6), (6, 6), (27, 18), (12, 31), (20, 29)):
        objs.append((i + j + 1, (lambda i, j: lambda: iso_tree(c, i, j))(i, j)))
    # parked truck by the factory
    objs.append((36, lambda: iso_box(c, 18.4, 15.2, 1.2, 0.6, 14, (250, 200, 60) if "truck" not in d else (60, 160, 220))))
    for k, (i, j) in enumerate(((17, 28), (19, 27), (15, 29), (21, 28), (27, 20), (29, 19), (26, 22), (28, 22), (30, 21), (24, 25), (23, 27), (26, 25),
                                (16, 31), (25, 28), (29, 24))):
        objs.append((i + j + 2, (lambda i, j, col: lambda: iso_house(c, i, j, (240, 230, 210), col))(i, j, roofs[(k + 2) % len(roofs)])))
    for i, j in ((20, 31), (28, 27), (31, 18), (22, 30), (27, 30), (13, 33), (32, 23)):
        objs.append((i + j + 1, (lambda i, j: lambda: iso_tree(c, i, j))(i, j)))
    for _, f in sorted(objs, key=lambda o: o[0]):
        f()
    # HUD
    toon(c, RRect(10, 8, 890, 44, 10), (40, 50, 80), w=1.6, shadow=None)
    flat(c, Circ(34, 26, 10), (250, 200, 60))
    digits(c, 54, 18, "25800", (250, 250, 250), 3)
    flat(c, [Circ(250, 22, 6), RRect(242, 28, 258, 38, 3)], (180, 220, 250))
    digits(c, 270, 18, "1340", (250, 250, 250), 3)
    flat(c, Circ(450, 26, 11), (250, 220, 80))
    flat(c, [Circ(446, 23, 2), Circ(454, 23, 2)], (40, 40, 50))
    flat(c, Thick(445, 30, 455, 30, 1.6), (40, 40, 50))
    toon(c, RRect(830, 90, 888, 420, 12), (40, 50, 80), w=1.6, shadow=None)
    icons = [(220, 80, 70), (90, 150, 220), (240, 200, 70), (90, 180, 100), (170, 120, 200)]
    if "menu" in d:
        icons[2] = (240, 120, 180)
    for k, col in enumerate(icons):
        flat(c, RRect(838, 100 + k * 62, 880, 150 + k * 62, 8), (250, 240, 220))
        toon(c, RRect(848, 112 + k * 62, 870, 138 + k * 62, 4), col, w=1.2, shadow=None)


def car_el(k, col, ph):
    x, y = P(14.6, 0)

    def d(c, m):
        toon(c, Poly([(x - 10, y - 4), (x + 4, y - 11), (x + 14, y - 6), (x, y + 2)]), col, w=1, shadow=None)
    v = 1.0
    return E("car%d" % k, d, anim=dict(driftVelocity=(-TW * v, -TH * v), driftLength=math.hypot(TW, TH) * 40, phase=ph))


L178_ELEMENTS = [car_el(k, col, k * 0.33) for k, col in enumerate(((220, 60, 60), (60, 120, 220), (250, 250, 246)))] + [
    E("smoke%d" % k, (lambda k: lambda c, m: toon(c, Circ(P(21.5, 10.5)[0], P(21.5, 10.5)[1] - 126, 9), (230, 230, 236), w=1, shadow=None))(k),
      anim=dict(driftVelocity=(8, 24), driftLength=70, driftFade=True, driftGrow=1.4, phase=k / 3)) for k in range(3)] + [
    E("cloudshadow", lambda c, m: soft_union(c, [Ell(300, 400, 90, 30)], (40, 60, 40), 0.15, spread=20), anim=drift_across(210, 390, 10, start=300)),
]

L178_DIFFS = [
    ("tower", 450, 60, 0),
    ("chimney", 660, 170, 0),
    ("fountain", 90, 300, 0),
    ("tree", 90, 360, 0),
    ("roof", 450, 420, 0),
    ("truck", 474, 310, 0),
    ("menu", 859, 249, 0),
]


# =================================================================== Level 179 rhythm game
LANE_TOP, LANE_BOT, JUDGE = (60, 370, 530), (590, 210, 690), 500
NOTE_COLS = [(250, 80, 120), (250, 200, 60), (90, 220, 140), (80, 160, 250)]


def lane_x(k, y, frac=0.5):
    t = (y - LANE_TOP[0]) / (LANE_BOT[0] - LANE_TOP[0])
    x0 = LANE_TOP[1] + (LANE_BOT[1] - LANE_TOP[1]) * t
    x1 = LANE_TOP[2] + (LANE_BOT[2] - LANE_TOP[2]) * t
    return x0 + (x1 - x0) * (k + frac) / 4, (x1 - x0) / 4


def l179_bg(c, d):
    c.gradient(0, H, (40, 20, 70), (20, 30, 70))
    for k in range(9):
        a = math.radians(200 + k * 17)
        soft_union(c, [Poly([(450, 60), (450 + math.cos(a) * 900, 60 - math.sin(a) * 900), (450 + math.cos(a + 0.05) * 900, 60 - math.sin(a + 0.05) * 900)])],
                   (200, 120, 255), 0.08, spread=10)
    # light rig
    flat(c, RRect(0, 0, W, 18, 0), (60, 56, 80))
    lamps = [(250, 80, 120), (250, 200, 60), (90, 220, 140), (80, 160, 250)] * 3
    if "lamp" in d:
        lamps[8] = (250, 250, 250)
    for k, col in enumerate(lamps):
        x = 40 + k * 75
        toon(c, RRect(x - 16, 12, x + 16, 44, 6), (40, 40, 56), w=1.2, shadow=None)
        flat(c, Circ(x, 30, 12), col)
    # song progress
    flat(c, RRect(220, 50, 680, 58, 4), (60, 60, 90))
    flat(c, RRect(220, 50, 520 if "progress" not in d else 340, 58, 4), (250, 120, 200))
    # lanes
    flat(c, Poly([(LANE_TOP[1], LANE_TOP[0]), (LANE_TOP[2], LANE_TOP[0]), (LANE_BOT[2], LANE_BOT[0]), (LANE_BOT[1], LANE_BOT[0])]), (20, 16, 36))
    for k in range(5):
        xt = LANE_TOP[1] + (LANE_TOP[2] - LANE_TOP[1]) * k / 4
        xb = LANE_BOT[1] + (LANE_BOT[2] - LANE_BOT[1]) * k / 4
        flat(c, Thick(xt, LANE_TOP[0], xb, LANE_BOT[0], 2), (120, 100, 180))
    xl, _ = lane_x(0, JUDGE, 0)
    xr, _ = lane_x(3, JUDGE, 1)
    flat(c, Thick(xl, JUDGE, xr, JUDGE, 4), (250, 250, 250))
    for k in range(4):
        x, w = lane_x(k, JUDGE)
        col = NOTE_COLS[k] if not (k == 2 and "button" in d) else (250, 250, 250)
        toon(c, Ell(x, JUDGE, w * 0.4, w * 0.2), col, w=1.6, shadow=None)
    # static notes
    for k, y in ((0, 180), (3, 260), (1, 330), (2, 140)):
        x, w = lane_x(k, y)
        toon(c, RRect(x - w * 0.4, y - w * 0.1, x + w * 0.4, y + w * 0.1, 4), NOTE_COLS[k], w=1.2, shadow=None)
    # idol singer (left)
    hair = (120, 220, 240) if "hair" not in d else (250, 130, 180)
    toon(c, [Ell(100, 330, 28, 70), Ell(200, 330, 28, 70)], hair)
    toon(c, Poly([(110, 560), (190, 560), (176, 410), (124, 410)]), (250, 250, 250))
    flat(c, Poly([(110, 560), (190, 560), (184, 500), (116, 500)]), (250, 120, 200))
    toon(c, Circ(150, 360, 44), SKIN)
    toon(c, [Ell(150, 332, 48, 26)], hair, w=1.6, shadow=None)
    for ex in (134, 166):
        flat(c, Ell(ex, 366, 5, 8), (60, 40, 90))
        flat(c, Circ(ex + 1, 362, 2), (250, 250, 250))
    flat(c, Ell(150, 386, 6, 4), (230, 90, 110))
    toon(c, [Thick(176, 430, 200, 396, 5), Circ(204, 390, 9)], (60, 60, 70), w=1.2, shadow=None)
    # speakers
    for k, x in enumerate((40, 860)):
        col = (60, 56, 80) if not (k == 1 and "speaker" in d) else (200, 60, 90)
        toon(c, RRect(x - 34, 440, x + 34, 594, 6), col)
        for y, r in ((480, 18), (540, 26)):
            flat(c, Circ(x, y, r), (30, 30, 40))
            flat(c, Circ(x, y, r * 0.4), (90, 90, 110))
    # combo + score (right)
    glyph_line(c, 720, 840, 150, (250, 220, 120), 1791, w=3, size=14)
    digits(c, 726, 170, "128", (250, 250, 250) if "combo" not in d else (250, 200, 60), 9)
    toon(c, RRect(706, 300, 850, 340, 10), (250, 120, 200), w=1.6, shadow=None)
    glyph_line(c, 716, 846, 320, (250, 250, 250), 1792, w=3, size=14)
    digits(c, 720, 80, "0987650", (250, 250, 250), 3)
    for k in range(5):
        filled = k < 4 or "stars" in d
        toon(c, Poly(star_pts(730 + k * 26, 380, 11, 5)), (250, 210, 60) if filled else (90, 80, 120), w=1.2, shadow=None)


def note_el(k, ph):
    tx, tw = lane_x(k, LANE_TOP[0] + 4)
    bx, bw = lane_x(k, JUDGE)

    def d(c, m):
        toon(c, RRect(tx - tw * 0.4, LANE_TOP[0] + 4 - tw * 0.1, tx + tw * 0.4, LANE_TOP[0] + 4 + tw * 0.1, 3), NOTE_COLS[k], w=1, shadow=None)
    dx, dy = bx - tx, JUDGE - LANE_TOP[0]
    return E("note%d" % k, d, pivot=(tx, LANE_TOP[0] + 4), daynight="untinted",
             anim=dict(driftVelocity=(dx / 2.0, -dy / 2.0), driftLength=math.hypot(dx, dy), driftGrow=bw / tw - 1, driftFade=True, phase=ph))


L179_ELEMENTS = [note_el(k, ph) for k, ph in ((0, 0.0), (1, 0.4), (2, 0.7), (3, 0.2), (1, 0.85))] + [
    E("eq%d" % k, (lambda k: lambda c, m: flat(c, RRect(706 + k * 18, 420, 718 + k * 18, 470, 2), NOTE_COLS[k % 4]))(k), pivot=(712 + k * 18, 470),
      daynight="untinted", anim=dict(stretch=(0, 0.6), scaleSpeed=1.3 + k * 0.17, phase=k * 0.13)) for k in range(8)] + [
    E("spark", lambda c, m: [flat(c, Poly(star_pts(x, y, 9, 2, points=4, rot=0)), (255, 255, 255)) for x, y in ((240, 260), (90, 220), (230, 470))],
      daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=0.8)),
]

L179_DIFFS = [
    ("lamp", 640, 30, 0),
    ("progress", 430, 54, 0),
    ("button", lane_x(2, JUDGE)[0], JUDGE, 0),
    ("hair", 100, 330, 0),
    ("speaker", 860, 520, 0),
    ("combo", 780, 192, 0),
    ("stars", 834, 380, 0),
]


# =================================================================== Level 180 pinball table
def l180_bg(c, d):
    c.rect(0, 0, W, H, (60, 30, 50))
    for x in range(0, 150, 20):
        flat(c, Thick(x, 0, x, H, 1), (70, 36, 58))
    for x in range(760, 900, 20):
        flat(c, Thick(x, 0, x, H, 1), (70, 36, 58))
    # cabinet art: rocket (left), planet (right)
    toon(c, [Poly([(74, 200), (100, 260), (100, 360), (48, 360), (48, 260)])], (240, 240, 246))
    toon(c, Circ(74, 290, 12), (90, 180, 240), w=1.4, shadow=None)
    toon(c, [Poly([(48, 330), (26, 380), (48, 364)]), Poly([(100, 330), (122, 380), (100, 364)])], (220, 60, 70), w=1.4, shadow=None)
    toon(c, Poly([(56, 360), (92, 360), (74, 400)]), (250, 180, 60), w=1.2, shadow=None)
    planet = (240, 150, 80) if "planet" not in d else (120, 200, 120)
    toon(c, Circ(830, 300, 40), planet)
    c.ellipse_ring(830, 300, 62, 14, 4, (250, 220, 140))
    for x, y in ((40, 100), (110, 470), (800, 150), (870, 480), (60, 540), (840, 560)):
        flat(c, Poly(star_pts(x, y, 8, 3)), (250, 230, 160))
    # backglass
    toon(c, RRect(160, 6, 740, 70, 10), (30, 20, 40), w=2)
    digits(c, 300, 18, "02417300", (250, 120, 60) if "score" not in d else (90, 220, 240), 5)
    # table
    table = [RRect(150, 150, 750, 610, 0), Ell(450, 160, 300, 90)]
    toon(c, table, (40, 40, 60), w=3, shadow=None)
    flat(c, [RRect(166, 160, 734, 610, 0), Ell(450, 168, 284, 80)], (50, 90, 170))
    for k in range(5):
        flat(c, Poly([(450, 330), (166 + k * 120, 610), (226 + k * 120, 610)]), (56, 100, 184))
    # plunger lane
    flat(c, Thick(696, 200, 696, 610, 4), (230, 230, 240))
    toon(c, RRect(706, 540, 726, 600, 4), (220, 60, 60), w=1.4, shadow=None)
    # top lanes with lights
    for k, x in enumerate((370, 450, 530)):
        flat(c, Thick(x - 40, 110, x - 40, 160, 4), (230, 230, 240))
        lightc = (250, 220, 60) if not (k == 1 and "lane" in d) else (60, 60, 80)
        toon(c, Circ(x, 140, 14), lightc, w=1.4, shadow=None)
    flat(c, Thick(570, 110, 570, 160, 4), (230, 230, 240))
    # bumpers
    for k, (x, y) in enumerate(((360, 250), (460, 220), (540, 270))):
        toon(c, Circ(x, y, 32), (250, 250, 250))
        cap = (230, 60, 90) if not (k == 2 and "bumper" in d) else (90, 200, 120)
        toon(c, Circ(x, y, 22), cap, w=1.6, shadow=None)
        flat(c, Poly(star_pts(x, y, 12, 5)), (250, 250, 250))
    # left ramp
    ramp = (240, 200, 60) if "ramp" not in d else (200, 120, 230)
    pts = [(200 + 60 * math.sin(t / 10 * math.pi), 480 - t * 30) for t in range(11)]
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 14), ramp)
        flat(c, Thick(a[0], a[1], b[0], b[1], 6), lit(ramp, 0.75))
    # drop targets
    for k in range(3):
        col = (250, 140, 40) if not (k == 1 and "target" in d) else (250, 250, 250)
        toon(c, RRect(640, 300 + k * 30, 662, 324 + k * 30, 3), col, w=1.4, shadow=None)
    # centre insert (rocket arrow)
    insert = (240, 80, 80) if "insert" not in d else (80, 200, 240)
    toon(c, Poly([(450, 330), (480, 380), (464, 380), (464, 420), (436, 420), (436, 380), (420, 380)]), insert, w=1.6, shadow=None)
    for k, x in enumerate((390, 510)):
        toon(c, Circ(x, 400, 10), (250, 220, 60), w=1.2, shadow=None)
    # slingshots
    toon(c, Poly([(240, 440), (300, 520), (240, 520)]), (250, 250, 250))
    toon(c, Poly([(660, 440), (600, 520), (660, 520)]), (250, 250, 250))
    flat(c, [Poly([(246, 456), (286, 512), (246, 512)]), Poly([(654, 456), (614, 512), (654, 512)])], (240, 80, 80))
    # inlane guides + drain
    flat(c, [Thick(180, 500, 330, 560, 4), Thick(680, 500, 570, 560, 4)], (230, 230, 240))
    flat(c, RRect(410, 590, 490, 610, 0), (20, 20, 30))


L180_ELEMENTS = [
    E("flipL", lambda c, m: toon(c, Thick(330, 560, 410, 578, 12), (250, 250, 250), w=1.6, shadow=None), pivot=(330, 560),
      anim=dict(swingAngle=14, swingSpeed=0.6)),
    E("flipR", lambda c, m: toon(c, Thick(570, 560, 490, 578, 12), (250, 250, 250), w=1.6, shadow=None), pivot=(570, 560),
      anim=dict(swingAngle=14, swingSpeed=0.6, phase=0.5)),
    E("ball", lambda c, m: (piece(c, Circ(450, 300, 10), (220, 224, 236), shadow=SMALL), flat(c, Circ(446, 296, 3), (255, 255, 255))), pivot=(450, 300),
      anim=dict(orbitRadius=(150, 110), orbitSpeed=0.25)),
    E("blink1", lambda c, m: [flat(c, Circ(x, y, 7), (255, 255, 200)) for x, y in ((360, 250), (460, 220))], daynight="untinted",
      anim=dict(blinkInterval=0.8, blinkDuration=0.3)),
    E("glow", lambda c, m: soft_union(c, [RRect(160, 6, 740, 70, 10)], (250, 120, 60), 0.2, spread=16), daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=1.0)),
]

L180_DIFFS = [
    ("planet", 830, 300, 0),
    ("score", 450, 30, 0),
    ("lane", 450, 140, 0),
    ("bumper", 540, 270, 0),
    ("ramp", 230, 330, 0),
    ("target", 651, 342, 0),
    ("insert", 450, 380, 0),
]


# =================================================================== Level 181 card battle
def card(c, x, y, art, kind, atk, hp, frame=(240, 200, 90), atk_col=(250, 200, 60), w=110, h=150, ang=0):
    if ang:
        toon(c, rot_poly(x, y, w, h, ang), frame, w=2)
        toon(c, rot_poly(x, y, w - 14, h - 14, ang), (60, 50, 70), w=1, shadow=None)
        return
    toon(c, RRect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 10), frame, w=2)
    flat(c, RRect(x - w / 2 + 8, y - h / 2 + 8, x + w / 2 - 8, y + h / 2 - 8, 6), (250, 244, 228))
    flat(c, Ell(x, y - 18, w * 0.36, h * 0.26), art)
    if kind == "dragon":
        flat(c, [Poly([(x - 20, y - 4), (x - 6, y - 40), (x + 10, y - 26), (x + 24, y - 30), (x + 18, y - 4)])], lit(art, 0.6))
    elif kind == "knight":
        flat(c, [RRect(x - 14, y - 40, x + 14, y - 6, 6)], (200, 204, 216))
        flat(c, Thick(x - 8, y - 26, x + 8, y - 26, 3), (40, 40, 50))
    else:
        flat(c, [Ell(x - 10, y - 20, 8, 16), Ell(x + 10, y - 20, 8, 16), Circ(x, y - 30, 8)], lit(art, 0.6))
    glyph_line(c, x - 36, x + 40, y + 34, (120, 100, 90), int(x + y), w=1.6, size=8)
    toon(c, Circ(x - w / 2 + 8, y + h / 2 - 10, 16), atk_col, w=1.4, shadow=None)
    digits(c, x - w / 2 + 3, y + h / 2 - 17, str(atk), (60, 40, 30), 2)
    toon(c, Poly(ngon(x + w / 2 - 8, y + h / 2 - 10, 16, 6, rot=30)), (220, 60, 70), w=1.4, shadow=None)
    digits(c, x + w / 2 - 13, y + h / 2 - 17, str(hp), (250, 250, 250), 2)


def l181_bg(c, d):
    c.rect(0, 0, W, H, (90, 60, 40))
    for y in range(0, H, 24):
        flat(c, Thick(0, y, W, y, 1.4), (80, 52, 34))
    toon(c, RRect(40, 90, 760, 520, 26), (50, 110, 100), w=3)
    flat(c, RRect(54, 104, 746, 506, 20), (60, 126, 112))
    flat(c, Thick(70, 305, 730, 305, 3), (90, 160, 140))
    # opponent portrait (horned warlock) + player portrait
    toon(c, Circ(400, 50, 46), (240, 200, 90), w=2.5)
    flat(c, Circ(400, 50, 38), (120, 70, 140))
    horns = (240, 230, 200) if "horns" not in d else (220, 60, 60)
    toon(c, [Poly([(370, 30), (350, -4), (382, 22)]), Poly([(430, 30), (450, -4), (418, 22)])], horns, w=1.4, shadow=None)
    toon(c, Circ(400, 56, 20), (180, 220, 170), w=1.4, shadow=None)
    flat(c, [Circ(392, 52, 3), Circ(408, 52, 3)], (220, 40, 40))
    toon(c, Circ(400, 560, 46), (240, 200, 90), w=2.5)
    flat(c, Circ(400, 560, 38), (60, 110, 200))
    toon(c, Circ(400, 566, 20), SKIN, w=1.4, shadow=None)
    flat(c, Poly([(380, 556), (386, 536), (400, 530), (414, 536), (420, 556), (400, 548)]), (150, 90, 40))
    # opponent hand (card backs, top right) + deck
    for k in range(4):
        toon(c, rot_poly(560 + k * 34, 40, 50, 70, -10 + k * 7), (110, 60, 120), w=1.6, shadow=None)
        flat(c, Circ(560 + k * 34, 40, 10), (240, 200, 90))
    for k in range(6 if "deck" not in d else 3):
        toon(c, RRect(800, 230 - k * 5, 880, 340 - k * 5, 6), (110, 60, 120), w=1.4, shadow=None)
    # field cards
    card(c, 200, 200, (230, 120, 80), "dragon", 6, 5)
    card(c, 400, 200, (120, 170, 240) if "art" not in d else (250, 200, 80), "knight", 3, 4)
    card(c, 600, 200, (160, 210, 120), "plant", 2, 6)
    card(c, 200, 410, (160, 210, 120), "plant", 1, 3, atk_col=(250, 200, 60) if "atk" not in d else (90, 200, 240))
    card(c, 400, 410, (230, 120, 80), "dragon", 5, 5)
    card(c, 600, 410, (120, 170, 240), "knight", 4, 2)
    # hand (fanned, bottom left)
    for k in range(5):
        frame = (240, 200, 90) if not (k == 2 and "hand" in d) else (200, 204, 216)
        toon(c, rot_poly(80 + k * 50, 560, 70, 96, -24 + k * 12), frame, w=1.6)
        toon(c, rot_poly(80 + k * 50, 560, 56, 82, -24 + k * 12), (250, 244, 228), w=0, shadow=None)
        flat(c, Circ(80 + k * 50, 550, 14), [(230, 120, 80), (120, 170, 240), (160, 210, 120), (200, 120, 200), (250, 200, 80)][k])
    # mana crystals (bottom right)
    for k in range(10):
        on = k < (6 if "mana" not in d else 4)
        toon(c, Poly([(520 + k * 26, 548), (532 + k * 26, 562), (520 + k * 26, 576), (508 + k * 26, 562)]), (80, 160, 250) if on else (60, 60, 80), w=1.2, shadow=None)
    digits(c, 790, 552, "6", (250, 250, 250), 4)
    # end turn button
    toon(c, Ell(840, 420, 52, 30), (250, 200, 60) if "endturn" not in d else (90, 200, 120), w=2.4)
    glyph_line(c, 806, 878, 420, (90, 60, 30), 1811, w=2.4, size=10)


L181_ELEMENTS = [
    E("playable", lambda c, m: soft_union(c, [RRect(345, 335, 455, 485, 10)], (120, 250, 140), 0.5, spread=14), daynight="untinted",
      anim=dict(twinkle=0.6, twinkleSpeed=0.8)),
    E("fuse", lambda c, m: flat(c, Circ(770, 305, 6), (255, 200, 80)), daynight="untinted", anim=dict(bobAmplitude=(30, 0), bobSpeed=0.1, twinkle=0.4, twinkleSpeed=4)),
    E("spark", lambda c, m: flat(c, Poly(star_pts(400, 6, 10, 2, points=4, rot=0)), (255, 255, 230)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
]

L181_DIFFS = [
    ("horns", 400, 18, 0),
    ("deck", 840, 220, 0),
    ("art", 400, 182, 0),
    ("atk", 158, 475, 0),
    ("hand", 180, 560, 0),
    ("mana", 572, 562, 0),
    ("endturn", 840, 420, 0),
]


# =================================================================== Level 182 spaceship cockpit
def l182_bg(c, d):
    c.gradient(0, 400, (10, 10, 30), (30, 20, 60))
    rnd = random.Random(1820)
    for _ in range(120):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 400), rnd.choice((1, 1.4, 2))), (250, 250, 230))
    soft_union(c, [Ell(620, 120, 160, 60), Ell(700, 170, 120, 50)], (200, 90, 200), 0.3, spread=50)
    # planet with ring (left)
    flat(c, Circ(220, 210, 90), (90, 140, 210))
    flat(c, [Ell(200, 180, 70, 18), Ell(240, 240, 60, 14)], (120, 170, 230))
    ring = (230, 210, 150) if "ring" not in d else (240, 120, 160)
    c.ellipse_ring(220, 210, 150, 34, 8, ring, ymin=210)
    c.ellipse_ring(220, 210, 150, 34, 8, ring, ymax=184)
    # space station (right)
    flat(c, Thick(600, 260, 820, 260, 6), (170, 176, 190))
    flat(c, Circ(710, 260, 30), (200, 204, 216))
    flat(c, Circ(710, 260, 14), (120, 130, 150))
    panel = (60, 90, 170) if "panel" not in d else (220, 170, 60)
    for x in (600, 790):
        pc = panel if x == 790 else (60, 90, 170)
        flat(c, RRect(x - 30, 230, x + 30, 290, 2), pc)
        flat(c, [Thick(x - 30, 250, x + 30, 250, 1), Thick(x - 30, 270, x + 30, 270, 1), Thick(x, 230, x, 290, 1)], lit(pc, 1.4))
    # asteroids
    for k, (x, y, r) in enumerate(((430, 120, 26), (500, 300, 18), (380, 330, 14), (840, 90, 22))):
        if k == 0 and "asteroid" in d:
            continue
        flat(c, Poly(ngon(x, y, r, 7, rot=k * 20)), (130, 110, 100))
        flat(c, Circ(x - r * 0.3, y - r * 0.2, r * 0.25), (100, 86, 80))
    # HUD reticle
    c.ellipse_ring(450, 220, 40, 40, 2, (120, 250, 160))
    flat(c, [Thick(450, 160, 450, 186, 2), Thick(450, 254, 450, 280, 2), Thick(390, 220, 416, 220, 2), Thick(484, 220, 510, 220, 2)], (120, 250, 160))
    # cockpit frame
    toon(c, [Poly([(-10, -10), (910, -10), (910, 22), (-10, 22)]), Poly([(-10, -10), (60, -10), (20, 400), (-10, 400)]),
             Poly([(910, -10), (840, -10), (880, 400), (910, 400)]), Poly([(440, 22), (460, 22), (466, 400), (434, 400)])], (60, 64, 80), w=2)
    # dashboard
    toon(c, Poly([(-10, 600), (-10, 380), (200, 360), (450, 350), (700, 360), (910, 380), (910, 600)]), (70, 74, 92), w=2.5)
    flat(c, Poly([(-10, 600), (-10, 400), (200, 384), (450, 376), (700, 384), (910, 400), (910, 600)]), (54, 58, 74))
    # radar (left)
    toon(c, Circ(130, 480, 70), (20, 40, 30), w=2)
    for r in (24, 46, 66):
        c.ellipse_ring(130, 480, r, r, 1.6, (60, 160, 90))
    flat(c, [Thick(60, 480, 200, 480, 1.2), Thick(130, 410, 130, 550, 1.2)], (60, 160, 90))
    for x, y in ((160, 450), (100, 520)):
        flat(c, Circ(x, y, 6), (120, 250, 140))
    flat(c, Circ(110, 446, 12), (250, 80, 80) if "blip" not in d else (250, 220, 60))
    # centre screen with graph
    toon(c, RRect(330, 410, 570, 530, 8), (20, 30, 50), w=2)
    graph = (90, 200, 250) if "graph" not in d else (250, 140, 60)
    pts = [(344 + k * 22, 490 - 30 * math.sin(k * 0.8) - k * 3) for k in range(11)]
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 3), graph)
    for k in range(4):
        flat(c, RRect(344 + k * 54, 500, 380 + k * 54, 518, 2), (40, 60, 90))
    # right screen: ship schematic
    toon(c, RRect(640, 420, 800, 520, 8), (20, 30, 50), w=2)
    flat(c, Poly([(720, 434), (744, 500), (720, 488), (696, 500)]), (120, 200, 250))
    # button rows
    cols = [(240, 80, 80), (250, 200, 60), (90, 220, 120), (80, 160, 250)]
    for r in range(2):
        for k in range(6):
            col = cols[(k + r) % 4]
            if r == 1 and k < 3 and "buttons" in d:
                col = (250, 250, 250)
            toon(c, RRect(250 + k * 24 - 8, 548 + r * 24 - 8, 250 + k * 24 + 8, 548 + r * 24 + 8, 3), col, w=1.2, shadow=None)
    # throttle lever + yoke
    flat(c, RRect(830, 440, 850, 580, 6), (30, 30, 40))
    toon(c, Thick(840, 560, 860, 470, 8), (150, 150, 160), w=1.4, shadow=None)
    toon(c, Circ(862, 462, 16), (220, 60, 60) if "knob" not in d else (60, 160, 220), w=1.6)
    toon(c, [RRect(380, 560, 520, 580, 8), RRect(370, 540, 392, 600, 8), RRect(508, 540, 530, 600, 8)], (40, 40, 50), w=1.6)


L182_ELEMENTS = [
    E("sweep", lambda c, m: soft_union(c, [Poly([(130, 480), (196, 456), (200, 480)])], (120, 250, 140), 0.4, spread=4), pivot=(130, 480),
      daynight="untinted", anim=dict(rotateSpeed=-90)),
    E("blinks", lambda c, m: [flat(c, Circ(x, y, 4), (255, 240, 160)) for x, y in ((610, 395), (660, 395), (240, 395))], daynight="untinted",
      anim=dict(blinkInterval=1.2, blinkDuration=0.5)),
    E("stationlight", lambda c, m: flat(c, Circ(820, 254, 4), (255, 80, 80)), daynight="untinted", anim=dict(blinkInterval=1.6, blinkDuration=0.4)),
    E("streak", lambda c, m: flat(c, Thick(420, 60, 440, 64, 1.6), (220, 230, 255)), daynight="untinted",
      anim=dict(driftVelocity=(-200, 30), driftLength=300, driftFade=True)),
    E("scan", lambda c, m: flat(c, Thick(332, 470, 568, 470, 1.4), (120, 250, 200, 0.5)), daynight="untinted",
      anim=dict(bobAmplitude=(0, 50), bobSpeed=0.4)),
]

L182_DIFFS = [
    ("ring", 220, 240, 0),
    ("panel", 790, 260, 0),
    ("asteroid", 430, 120, 0),
    ("blip", 110, 446, 0),
    ("graph", 450, 470, 0),
    ("buttons", 250, 572, 0),
    ("knob", 862, 462, 0),
]


# =================================================================== Level 183 box-pushing puzzle
MAP183 = [
    "##################",
    "#......#.........#",
    "#.B..G.#..r...B..#",
    "#...#..#....##...#",
    "#.G.#.....*..#.G.#",
    "#...####..#..#...#",
    "#......#..#......#",
    "#.p.B.....#.B..p.#",
    "#......#..###.##.#",
    "#..*...#......G..#",
    "#..@...#..r......#",
    "##################",
]
S183 = 50
CRATE = ["########", "#yy##yy#", "#y#yy#y#", "##y##y##", "##y##y##", "#y#yy#y#", "#yy##yy#", "########"]


def l183_bg(c, d):
    for j, row in enumerate(MAP183):
        for i, ch in enumerate(row):
            x, y = i * S183, j * S183
            if (i, j) == (12, 3) and "wall" in d:
                ch = "."
            if ch == "#":
                block(c, x, y, S183, (150, 90, 70), kind="brick")
                continue
            flat(c, RRect(x, y, x + S183, y + S183, 0), (220, 200, 160) if (i + j) % 2 else (210, 190, 150))
            if ch == "G" and not ((i, j) == (5, 2) and "goal" in d):
                sprite(c, x + 11, y + 11, ["##...##", "###.###", ".#####.", "..###..", ".#####.", "###.###", "##...##"], {"#": (220, 60, 60)}, 4)
            if ch in "B*":
                col = (190, 130, 70) if ch == "B" else (120, 190, 90)
                if (i, j) == (14, 2) and "crate" in d:
                    col = (90, 120, 200)
                sprite(c, x + 5, y + 5, CRATE, {"#": lit(col, 0.7), "y": col}, 5)
            if ch == "r":
                col = (80, 110, 160) if not ((i, j) == (10, 2) and "barrel" in d) else (200, 80, 60)
                sprite(c, x + 10, y + 5, [".####.", "######", "#yyyy#", "######", "#yyyy#", "######", ".####."], {"#": col, "y": lit(col, 1.3)}, 5)
            if ch == "p" and not ((i, j) == (15, 7) and "plant" in d):
                sprite(c, x + 10, y + 2, ["..g...", ".ggg.g", "gggggg", ".gggg.", "..bb..", ".bbbb.", ".bbbb.", "..bb.."],
                       {"g": (80, 170, 80), "b": (190, 110, 70)}, 5)
            if ch == "@":
                cap = (220, 60, 60) if "cap" not in d else (60, 160, 90)
                sprite(c, x + 9, y + 2, [".cccc.", "cccccc", ".ssss.", ".sese.", ".ssss.", "bbbbbb", "sbbbbs", ".l..l.", ".k..k."],
                       {"c": cap, "s": (250, 210, 170), "e": (30, 30, 40), "b": (60, 110, 210) if "cap" not in d else (240, 200, 60), "l": (60, 60, 80), "k": (90, 60, 40)}, 5)
    # HUD over the top wall
    flat(c, RRect(560, 6, 890, 44, 6), (30, 26, 40, 0.85))
    glyph_line(c, 570, 640, 25, (250, 250, 250), 1831, w=2, size=10)
    digits(c, 650, 14, "042", (250, 250, 250) if "moves" not in d else (250, 200, 60), 4)
    glyph_line(c, 730, 800, 25, (250, 250, 250), 1832, w=2, size=10)
    digits(c, 810, 14, "07", (250, 250, 250), 4)
    flat(c, RRect(10, 6, 120, 44, 6), (30, 26, 40, 0.85))
    sprite(c, 20, 12, ["..#...", ".##...", "######", ".##..#", "..#..#", "....##"], {"#": (250, 250, 250)}, 4)
    sprite(c, 70, 12, ["######", "#....#", "#.##.#", "#.##.#", "#....#", "######"], {"#": (250, 250, 250)}, 4)


L183_ELEMENTS = [
    E("goalglow%d" % k, (lambda x, y: lambda c, m: soft_union(c, [RRect(x + 6, y + 6, x + 44, y + 44, 4)], (140, 250, 120), 0.35, spread=10))(x, y),
      daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.7, phase=k * 0.3)) for k, (x, y) in enumerate(((500, 200), (150, 450)))] + [
    E("hint", lambda c, m: sprite(c, 168, 470, ["..#..", ".###.", "#####"], {"#": (250, 250, 250)}, 4), daynight="untinted",
      anim=dict(bobAmplitude=(0, 5), bobSpeed=1.2)),
    E("dust", lambda c, m: [flat(c, RRect(x, y, x + 4, y + 4, 0), (240, 230, 200)) for x, y in ((300, 300), (720, 360), (420, 520))],
      anim=dict(driftVelocity=(10, 14), driftLength=40, driftFade=True)),
]

L183_DIFFS = [
    ("crate", 725, 125, 0),
    ("goal", 275, 125, 0),
    ("wall", 625, 175, 0),
    ("barrel", 525, 125, 0),
    ("plant", 775, 375, 0),
    ("cap", 175, 510, 0),
    ("moves", 674, 24, 0),
]


# =================================================================== Level 184 fishing game
SURF = 210


def l184_bg(c, d):
    c.gradient(0, SURF, (120, 190, 245), (230, 240, 250))
    for x, y, k in ((160, 50, 0.9), (620, 36, 0.7)):
        toon(c, [Circ(x, y, 20 * k), Circ(x + 24 * k, y + 6 * k, 16 * k), Circ(x - 24 * k, y + 6 * k, 15 * k)], (250, 250, 255), w=1.2, shadow=None)
    toon(c, Poly([(380, SURF), (520, 110), (620, 170), (720, 90), (920, SURF)]), (130, 160, 200), w=1.6, shadow=None)
    flat(c, Poly([(720, 90), (744, 112), (730, 110), (720, 120), (708, 110), (698, 112)]), (250, 250, 255))
    toon(c, Poly([(-20, SURF), (-20, 150), (120, 140), (260, 170), (340, SURF)]), (100, 170, 90), w=1.6, shadow=None)
    for x in (30, 90, 200):
        toon(c, [Poly([(x - 22, 160), (x + 22, 160), (x, 100)]), RRect(x - 4, 160, x + 4, 176, 1)], (60, 130, 80), w=1.4, shadow=None)
    # dock + angler
    toon(c, RRect(120, 190, 360, 206, 2), (170, 120, 80), w=1.6)
    for x in (140, 220, 300, 350):
        toon(c, RRect(x - 5, 206, x + 5, 280, 2), (140, 96, 60), w=1.2, shadow=None)
    chibi(c, 300, 192, s=0.9, hair=(90, 60, 40), outfit=(240, 120, 60), face=1)
    toon(c, [Ell(301, 136, 26, 6), RRect(286, 122, 316, 138, 6)], (240, 200, 90), w=1.2, shadow=None)
    piece(c, RRect(214, 168, 258, 192, 3), (90, 140, 200) if "box" not in d else (230, 90, 90), border=1.2, border_col=OUTLINE, shadow=None)
    # boat (right)
    boat = (220, 70, 60) if "boat" not in d else (250, 250, 246)
    toon(c, Poly([(600, SURF - 22), (760, SURF - 22), (740, SURF + 6), (620, SURF + 6)]), boat)
    flat(c, Thick(604, SURF - 14, 756, SURF - 14, 3), (250, 250, 250))
    flat(c, Thick(680, SURF - 22, 680, SURF - 100, 3), (140, 100, 60))
    toon(c, Poly([(684, SURF - 98), (730, SURF - 34), (684, SURF - 34)]), (250, 250, 246), w=1.4, shadow=None)
    # underwater
    c.gradient(SURF, H, (90, 170, 220), (30, 70, 130))
    for k in range(5):
        soft_union(c, [Poly([(100 + k * 180, SURF), (140 + k * 180, SURF), (100 + k * 180, H), (40 + k * 180, H)])], (200, 240, 255), 0.08, spread=10)
    flat(c, Thick(-10, SURF, 910, SURF, 4), (220, 240, 255))
    # sea floor, rocks, seaweed, coral, chest
    toon(c, Poly([(-20, 560), (200, 540), (420, 556), (640, 536), (920, 556), (920, 620), (-20, 620)]), (220, 200, 150), w=1.6, shadow=None)
    for x, y, r in ((80, 556, 30), (520, 548, 22), (860, 556, 34)):
        toon(c, Poly(ngon(x, y, r, 7, ry=r * 0.7)), (130, 130, 150), w=1.4, shadow=None)
    for k, x in enumerate((150, 360, 640, 780)):
        col = (60, 160, 90) if not (k == 2 and "weed" in d) else (200, 90, 160)
        pts = [(x + 10 * math.sin(t * 0.9), 560 - t * 18) for t in range(9)]
        toon(c, [Thick(a[0], a[1], b[0], b[1], 8) for a, b in zip(pts, pts[1:])], col, w=1.2, shadow=None)
    toon(c, [Thick(260, 550, 250, 500, 6), Thick(256, 520, 236, 500, 5), Thick(256, 516, 276, 494, 5)], (240, 120, 120) if "coral" not in d else (250, 220, 90),
         w=1.2, shadow=None)
    if "chest" not in d:
        toon(c, [RRect(440, 512, 500, 546, 4), RRect(440, 498, 500, 516, 8)], (160, 100, 50), w=1.4)
        flat(c, [RRect(466, 504, 474, 524, 1)], (250, 200, 60))
    # big fish near the hook
    fish = (240, 160, 60) if "fish" not in d else (120, 200, 240)
    toon(c, [Ell(470, 400, 50, 24), Poly([(514, 400), (550, 378), (550, 422)])], fish)
    flat(c, Circ(440, 394, 5), (40, 30, 50))
    flat(c, Poly([(470, 378), (490, 362), (496, 382)]), lit(fish, 0.8))
    # fishing line + hook
    flat(c, Thick(340, 80, 410, 410, 1.2), (250, 250, 250))
    flat(c, Thick(300, 160, 340, 80, 3), (130, 90, 60))
    c.ellipse_ring(406, 414, 6, 6, 2, (200, 200, 210), ymin=414)
    # UI: tension gauge + catch log + timer
    toon(c, RRect(840, 230, 880, 520, 10), (40, 40, 60), w=2)
    zone = (90, 220, 110) if "zone" not in d else (240, 140, 60)
    flat(c, RRect(846, 330, 874, 420, 4), zone)
    toon(c, RRect(16, 230, 130, 290, 8), (250, 240, 220), w=1.6, shadow=None)
    toon(c, [Ell(50, 260, 18, 9), Poly([(66, 260), (78, 250), (78, 270)])], (120, 180, 230), w=1.2, shadow=None)
    digits(c, 88, 250, "7", (90, 70, 60), 5)
    toon(c, RRect(780, 6, 890, 40, 8), (250, 240, 220), w=1.6, shadow=None)
    digits(c, 800, 14, "130", (90, 70, 60), 4)


L184_ELEMENTS = [
    E("marker", lambda c, m: toon(c, RRect(838, 370, 882, 380, 3), (250, 250, 250), w=1.2, shadow=None), daynight="untinted",
      anim=dict(bobAmplitude=(0, 50), bobSpeed=0.4)),
    E("fishA", lambda c, m: toon(c, [Ell(200, 330, 22, 10), Poly([(220, 330), (236, 320), (236, 340)])], (250, 220, 90), w=1.2, shadow=None),
      anim=dict(bobAmplitude=(50, 6), bobSpeed=0.12)),
    E("fishB", lambda c, m: toon(c, [Ell(680, 300, 18, 8), Poly([(664, 300), (650, 292), (650, 308)])], (200, 120, 220), w=1.2, shadow=None),
      anim=dict(bobAmplitude=(40, 6), bobSpeed=0.15, phase=0.4)),
    E("fishC", lambda c, m: toon(c, [Ell(580, 260, 16, 7), Poly([(564, 260), (552, 253), (552, 267)])], (240, 100, 100), w=1.2, shadow=None),
      anim=dict(bobAmplitude=(30, 4), bobSpeed=0.2, phase=0.7)),
] + [E("bub%d" % k, (lambda x: lambda c, m: toon(c, Circ(x, 520, 4), (220, 240, 255), w=1, shadow=None))(x),
       anim=dict(driftVelocity=(0, 40), driftLength=300, driftFade=True, phase=k / 3)) for k, x in enumerate((90, 300, 820))] + [
    E("bobber", lambda c, m: toon(c, Circ(358, SURF - 2, 6), (240, 60, 60), w=1, shadow=None), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.8)),
]

L184_DIFFS = [
    ("boat", 680, 180, 0),
    ("weed", 640, 520, 0),
    ("chest", 470, 522, 0),
    ("fish", 480, 400, 0),
    ("zone", 860, 375, 0),
    ("coral", 256, 520, 0),
    ("box", 236, 180, 0),
]


LEVELS = [
    ("Level175", "像素城堡探险", l175_bg, L175_ELEMENTS, L175_DIFFS, 60, OPTS),
    ("Level176", "回合制战斗", l176_bg, L176_ELEMENTS, L176_DIFFS, 60, OPTS),
    ("Level177", "农场模拟", l177_bg, L177_ELEMENTS, L177_DIFFS, 60, OPTS),
    ("Level178", "城市建造", l178_bg, L178_ELEMENTS, L178_DIFFS, 60, OPTS),
    ("Level179", "节奏音游", l179_bg, L179_ELEMENTS, L179_DIFFS, 60, OPTS),
    ("Level180", "弹球台", l180_bg, L180_ELEMENTS, L180_DIFFS, 60, OPTS),
    ("Level181", "卡牌对战", l181_bg, L181_ELEMENTS, L181_DIFFS, 60, OPTS),
    ("Level182", "星际驾驶舱", l182_bg, L182_ELEMENTS, L182_DIFFS, 60, OPTS),
    ("Level183", "推箱子", l183_bg, L183_ELEMENTS, L183_DIFFS, 60, OPTS),
    ("Level184", "钓鱼游戏", l184_bg, L184_ELEMENTS, L184_DIFFS, 60, OPTS),
]
