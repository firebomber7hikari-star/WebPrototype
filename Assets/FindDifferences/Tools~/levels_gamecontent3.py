# -*- coding: utf-8 -*-
"""Inside video games, part 3 (all designs original: no real games, characters, brands or logos):
  Level185 无尽跑酷   - an endless runner over sunset rooftops: coins, water towers, billboard, distance HUD
  Level186 点击冒险   - a point-and-click attic study: locked box, tilted painting, clock, inventory bar
  Level187 宠物养成   - a virtual pet room: round pet on a cushion, food bowl, toys, status bars, action buttons
  Level188 迷你高尔夫 - a top-down mini-golf hole: windmill, water, bunker, bridge, flag, stroke HUD
  Level189 荒岛求生   - a desert-island survival camp: shelter, campfire, raft, crab, survival bars, hotbar
  Level190 料理游戏   - a cooking game kitchen: stoves, cutting board, ingredient bins, order tickets, chef
  Level191 战棋策略   - a hex-grid strategy map: terrain, castle, village, two armies, unit panel
  Level192 视觉小说   - a visual novel scene: school rooftop at sunset, heroine sprite, dialogue box, menu
  Level193 水管谜题   - a pipe-connecting puzzle board with source tank and drain
  Level194 世界地图   - an open-world map screen: continent, towns, quest markers, compass, legend
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from stylekit import flame
from levels_retro import digits, sprite
from levels_gamecontent import OUTLINE, glyph_line, toon
from levels_gamecontent2 import bar, chibi, rot_poly

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 220, 190)


def panel(c, x0, y0, x1, y1, col=(250, 240, 220), r=8, w=1.8):
    toon(c, RRect(x0, y0, x1, y1, r), col, w=w, shadow=None)


def heart(c, x, y, s, col):
    flat(c, [Circ(x - 5 * s, y - 3 * s, 5.5 * s), Circ(x + 5 * s, y - 3 * s, 5.5 * s), Poly([(x - 10.5 * s, y - 1 * s), (x + 10.5 * s, y - 1 * s), (x, y + 11 * s)])], col)


# =================================================================== Level 185 endless runner
def roof_block(c, x0, x1, top, col):
    toon(c, RRect(x0, top, x1, 640, 2), col, w=2, shadow=None)
    flat(c, RRect(x0, top, x1, top + 10, 1), lit(col, 0.8))
    for y in range(int(top) + 30, 600, 44):
        for x in range(int(x0) + 14, int(x1) - 30, 46):
            flat(c, RRect(x, y, x + 26, y + 22, 2), lit(col, 0.7))


def l185_bg(c, d):
    c.gradient(0, 420, (250, 150, 120), (250, 220, 160))
    sun = (250, 230, 120) if "sun" not in d else (250, 120, 150)
    flat(c, Circ(700, 150, 60), sun)
    for k in range(5):
        flat(c, RRect(620, 160 + k * 10, 780, 164 + k * 10, 0), (250, 190, 150))
    rnd = random.Random(1850)
    x = -20
    while x < W:
        w, h = rnd.randint(40, 80), rnd.randint(80, 200)
        flat(c, RRect(x, 330 - h, x + w, 420, 0), (200, 120, 130))
        x += w + rnd.randint(0, 8)
    x = -20
    while x < W:
        w, h = rnd.randint(50, 90), rnd.randint(40, 140)
        flat(c, RRect(x, 380 - h, x + w, 440, 0), (160, 90, 120))
        for wy in range(int(380 - h) + 10, 430, 18):
            for wx in range(x + 6, x + w - 8, 14):
                if rnd.random() < 0.3:
                    flat(c, RRect(wx, wy, wx + 6, wy + 8, 0), (250, 210, 140))
        x += w + rnd.randint(0, 6)
    # rooftops (with gaps)
    roof_block(c, -20, 260, 420, (120, 110, 140))
    roof_block(c, 330, 600, 380, (110, 120, 150))
    roof_block(c, 670, 920, 440, (130, 104, 130))
    # water tower, AC units, antenna, chimney
    wt = (170, 110, 80) if "tower" not in d else (90, 140, 190)
    toon(c, [Thick(80, 420, 90, 340, 4), Thick(150, 420, 140, 340, 4)], (90, 80, 90), w=1.4, shadow=None)
    toon(c, [RRect(70, 270, 160, 344, 6), Poly([(64, 274), (166, 274), (115, 236)])], wt, w=1.8)
    flat(c, [Thick(70, 296, 160, 296, 2), Thick(70, 320, 160, 320, 2)], lit(wt, 0.75))
    if "ac" not in d:
        toon(c, RRect(200, 386, 250, 420, 3), (200, 204, 214), w=1.6, shadow=None)
        flat(c, Circ(225, 403, 11), (150, 154, 166))
    toon(c, RRect(540, 344, 580, 380, 3), (200, 204, 214), w=1.6, shadow=None)
    ant = (200, 60, 60) if "antenna" not in d else (250, 250, 250)
    flat(c, [Thick(470, 380, 470, 290, 3), Thick(450, 310, 490, 310, 2), Thick(456, 330, 484, 330, 2)], (90, 80, 90))
    flat(c, Circ(470, 288, 6), ant)
    toon(c, RRect(820, 380, 856, 440, 2), (180, 100, 80) if "chimney" not in d else (90, 90, 110), w=1.6, shadow=None)
    # billboard on the middle roof
    toon(c, [Thick(370, 380, 370, 320, 4), Thick(450, 380, 450, 320, 4)], (90, 80, 90), w=1.2, shadow=None)
    bb = (90, 190, 220) if "billboard" not in d else (240, 200, 70)
    toon(c, RRect(340, 250, 480, 324, 4), bb, w=2)
    glyph_line(c, 356, 470, 286, (250, 250, 250), 1851, w=3, size=14)
    # barrier obstacle on the right roof
    toon(c, [RRect(720, 410, 790, 424, 2), RRect(726, 424, 734, 440, 1), RRect(776, 424, 784, 440, 1)], (250, 200, 60), w=1.4, shadow=None)
    for k in range(3):
        flat(c, Poly([(728 + k * 22, 410), (740 + k * 22, 410), (732 + k * 22, 424), (720 + k * 22, 424)]), (40, 40, 50))
    # HUD
    panel(c, 14, 12, 220, 50, (40, 40, 60))
    digits(c, 26, 20, "01284", (250, 250, 250), 5)
    glyph_line(c, 170, 214, 31, (250, 250, 250), 1852, w=2, size=10)
    panel(c, 240, 12, 370, 50, (40, 40, 60))
    flat(c, Circ(262, 31, 11), (250, 200, 60))
    digits(c, 284, 20, "236", (250, 250, 250), 5)
    pu = (230, 70, 80) if "power" not in d else (90, 200, 120)
    panel(c, 790, 8, 846, 58, (250, 240, 220), w=1.4)
    toon(c, [Thick(800, 18, 800, 44, 8), Thick(836, 18, 836, 44, 8), Thick(800, 44, 836, 44, 8)], pu, w=1.2, shadow=None)
    flat(c, [RRect(856, 18, 864, 46, 2), RRect(872, 18, 880, 46, 2)], (250, 250, 250))


def coin_el(x, y, ph):
    return E("coin%d" % x, lambda c, m: (toon(c, Circ(x, y, 10), (250, 200, 60), w=1.2, shadow=None), flat(c, RRect(x - 2, y - 6, x + 2, y + 6, 1), (250, 230, 140))),
             pivot=(x, y), daynight="untinted", anim=dict(spinSpeed=1.0, phase=ph))


L185_ELEMENTS = [coin_el(x, y, i * 0.15) for i, (x, y) in enumerate(((280, 330), (310, 310), (340, 300), (610, 320), (640, 330)))] + [
    E("runner", lambda c, m: chibi(c, 300, 400, s=0.9, hair=(240, 120, 60), outfit=(60, 110, 210), face=1), pivot=(300, 400),
      anim=dict(bobAmplitude=(0, 40), bobSpeed=0.5, bounce=True)),
    E("drone", lambda c, m: toon(c, [RRect(560, 196, 600, 212, 4), Thick(552, 192, 608, 192, 2)], (60, 60, 70), w=1.2, shadow=None),
      anim=dict(bobAmplitude=(20, 8), bobSpeed=0.3)),
    E("trail", lambda c, m: [flat(c, Thick(240, 340 + k * 10, 270, 340 + k * 10, 2), (250, 250, 250)) for k in range(3)], daynight="untinted",
      anim=dict(twinkle=0.7, twinkleSpeed=2.0)),
    E("bird", lambda c, m: flat(c, [Thick(140, 100, 150, 106, 2), Thick(150, 106, 160, 100, 2)], (90, 60, 80)), anim=drift_across(140, 160, -25, start=150)),
]

L185_DIFFS = [
    ("sun", 700, 150, 0),
    ("tower", 115, 290, 0),
    ("ac", 225, 403, 0),
    ("antenna", 470, 288, 0),
    ("billboard", 410, 287, 0),
    ("chimney", 838, 410, 0),
    ("power", 818, 34, 0),
]


# =================================================================== Level 186 point-and-click attic study
def l186_bg(c, d):
    c.rect(0, 0, W, 440, (150, 110, 120))
    for x in range(0, W, 40):
        flat(c, RRect(x, 0, x + 20, 440, 0), (160, 118, 128))
    flat(c, Poly([(0, 0), (260, 0), (0, 160)]), (110, 76, 90))
    flat(c, Poly([(900, 0), (640, 0), (900, 160)]), (110, 76, 90))
    # round window with moon + curtain
    toon(c, Circ(450, 140, 82), (110, 80, 60), w=2)
    flat(c, Circ(450, 140, 70), (30, 40, 90))
    flat(c, Circ(480, 116, 18), (250, 240, 190))
    flat(c, [Thick(380, 140, 520, 140, 4), Thick(450, 70, 450, 210, 4)], (110, 80, 60))
    cur = (180, 50, 70) if "curtain" not in d else (60, 120, 90)
    toon(c, Poly([(350, 60), (390, 60), (380, 230), (340, 236)]), cur, w=1.6, shadow=None)
    # bookshelf (left)
    toon(c, RRect(40, 150, 220, 440, 4), (120, 80, 56), w=2)
    rnd = random.Random(1860)
    for r, y in enumerate((230, 310, 390)):
        flat(c, RRect(48, y, 212, y + 8, 0), (90, 60, 40))
        x = 52
        while x < 204:
            w = rnd.randint(10, 18)
            col = rnd.choice([(170, 60, 60), (60, 100, 160), (70, 130, 90), (200, 160, 70), (120, 80, 140)])
            if r == 1 and 120 < x < 150 and "book" in d:
                col = (250, 250, 250)
            flat(c, RRect(x, y - rnd.randint(46, 64), x + w, y, 1), col)
            x += w + 2
    # tilted painting
    art = (90, 150, 200) if "painting" not in d else (230, 140, 70)
    toon(c, rot_poly(660, 170, 140, 100, 6), (200, 160, 70), w=2)
    toon(c, rot_poly(660, 170, 116, 78, 6), art, w=0, shadow=None)
    flat(c, [Poly([(608, 200), (640, 160), (672, 196)]), Circ(700, 150, 12)], (250, 240, 200))
    # wall clock
    toon(c, Circ(820, 260, 40), (200, 160, 70), w=2)
    flat(c, Circ(820, 260, 32), (250, 246, 230))
    hand = (40, 40, 50) if "clock" not in d else (220, 60, 60)
    flat(c, [Thick(820, 260, 820, 234, 5), Thick(820, 260, 842, 272, 5), Circ(820, 260, 5)], hand)
    # floor + rug
    c.rect(0, 440, W, H, (120, 84, 60))
    for y in range(440, H, 26):
        flat(c, Thick(0, y, W, y, 1.4), (104, 72, 50))
    toon(c, Ell(450, 540, 260, 52), (70, 110, 150), w=2, shadow=None)
    c.ellipse_ring(450, 540, 210, 38, 6, (230, 200, 120))
    flat(c, Poly([(450, 510), (510, 530), (450, 550), (390, 530)]), (230, 200, 120) if "rug" not in d else (200, 80, 110))
    # desk with lamp + locked box
    toon(c, [RRect(300, 360, 620, 380, 3), RRect(316, 380, 336, 470, 2), RRect(584, 380, 604, 470, 2)], (140, 96, 66), w=2)
    lamp = (240, 200, 90) if "lamp" not in d else (120, 200, 230)
    toon(c, [Thick(350, 360, 360, 300, 3), Poly([(330, 300), (390, 300), (376, 270), (344, 270)])], lamp, w=1.6, shadow=None)
    box = (150, 90, 50) if "box" not in d else (90, 90, 120)
    toon(c, [RRect(470, 320, 560, 360, 4), RRect(470, 306, 560, 324, 8)], box, w=1.8)
    flat(c, RRect(506, 324, 524, 344, 2), (250, 200, 60))
    flat(c, [RRect(420, 340, 450, 360, 1)], (250, 246, 230))
    # chest + plant
    toon(c, [RRect(680, 430, 820, 500, 6), RRect(680, 410, 820, 440, 14)], (130, 80, 50), w=2)
    flat(c, [RRect(704, 410, 714, 500, 0), RRect(786, 410, 796, 500, 0)], (200, 160, 70))
    toon(c, Poly([(80, 500), (130, 500), (124, 460), (86, 460)]), (190, 110, 70), w=1.6, shadow=None)
    toon(c, [Ell(92, 430, 14, 30), Ell(118, 430, 14, 30), Ell(105, 420, 12, 36)], (80, 150, 90), w=1.4, shadow=None)
    # inventory bar
    panel(c, 150, 548, 750, 596, (60, 44, 40), r=10, w=2)
    items = [(250, 200, 60), (250, 246, 230), (90, 200, 220), None, None, None]
    if "item" in d:
        items[2] = (230, 80, 120)
    for k, col in enumerate(items):
        x = 170 + k * 96
        flat(c, RRect(x, 554, x + 80, 590, 6), (90, 66, 56))
        if col and k == 0:
            toon(c, [Circ(x + 26, 572, 8), Thick(x + 32, 572, x + 60, 572, 4)], col, w=1.2, shadow=None)
        elif col and k == 1:
            toon(c, rot_poly(x + 40, 572, 30, 24, -10), col, w=1.2, shadow=None)
        elif col:
            toon(c, Poly(ngon(x + 40, 572, 13, 6, rot=30)), col, w=1.2, shadow=None)
    toon(c, Circ(840, 572, 22), (250, 200, 60), w=1.8, shadow=None)
    flat(c, Thick(840, 562, 840, 576, 3), (60, 44, 40))
    flat(c, Circ(840, 582, 2), (60, 44, 40))


L186_ELEMENTS = [
    E("cursor", lambda c, m: toon(c, Poly([(600, 300), (600, 330), (608, 322), (614, 336), (620, 333), (614, 320), (624, 320)]), (250, 250, 250), w=1.4, shadow=None),
      daynight="untinted", anim=dict(bobAmplitude=(30, 14), bobSpeed=0.2)),
    E("lampglow", lambda c, m: soft_union(c, [Ell(360, 330, 60, 30)], (255, 230, 150), 0.35, spread=30), daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=0.5)),
    E("sparkle", lambda c, m: flat(c, Poly(star_pts(515, 300, 10, 2, points=4, rot=0)), (255, 255, 230)), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=0.7)),
    E("dust", lambda c, m: [flat(c, Circ(x, y, 2), (250, 240, 210)) for x, y in ((420, 120), (470, 170), (440, 200))], anim=dict(driftVelocity=(6, -10), driftLength=40, driftFade=True)),
]

L186_DIFFS = [
    ("curtain", 365, 150, 0),
    ("book", 135, 280, 0),
    ("painting", 660, 170, 0),
    ("clock", 826, 256, 0),
    ("rug", 450, 530, 0),
    ("lamp", 360, 286, 0),
    ("box", 515, 334, 0),
    ("item", 402, 572, 0),
]


# =================================================================== Level 187 virtual pet
def l187_bg(c, d):
    c.rect(0, 0, W, 420, (250, 220, 200))
    for y in range(80, 420, 40):
        for x in range((y // 40 % 2) * 40, W, 80):
            flat(c, Circ(x, y, 5), (250, 200, 190))
    # window
    toon(c, RRect(560, 90, 760, 260, 6), (250, 250, 250), w=2)
    flat(c, RRect(572, 102, 748, 248, 3), (150, 210, 250))
    flat(c, [Ell(620, 220, 50, 22), Ell(700, 230, 60, 24)], (120, 200, 120))
    flat(c, [Thick(660, 102, 660, 248, 4), Thick(572, 175, 748, 175, 4)], (250, 250, 250))
    cur = (250, 170, 190) if "curtain" not in d else (170, 210, 120)
    toon(c, Poly([(548, 80), (590, 80), (580, 270), (540, 276)]), cur, w=1.6, shadow=None)
    toon(c, Poly([(772, 80), (730, 80), (740, 270), (780, 276)]), (250, 170, 190), w=1.6, shadow=None)
    # wall frames
    toon(c, RRect(120, 100, 240, 200, 4), (200, 160, 110), w=2)
    flat(c, RRect(132, 112, 228, 188, 2), (190, 230, 250))
    heart(c, 180, 146, 2.0, (240, 100, 130) if "frame" not in d else (100, 140, 230))
    toon(c, RRect(300, 130, 380, 210, 4), (200, 160, 110), w=2)
    flat(c, RRect(310, 140, 370, 200, 2), (250, 240, 200))
    flat(c, Poly(star_pts(340, 170, 22, 9)), (250, 200, 70))
    # floor
    c.rect(0, 420, W, H, (220, 180, 140))
    for x in range(0, W, 60):
        flat(c, Thick(x, 420, x, H, 1.4), (206, 166, 126))
    # cushion + pet
    cush = (120, 160, 230) if "cushion" not in d else (240, 160, 80)
    toon(c, Ell(450, 470, 150, 40), cush, w=2.2)
    flat(c, Ell(450, 462, 120, 26), lit(cush, 1.15))
    toon(c, [Poly([(380, 320), (396, 260), (420, 316)]), Poly([(480, 316), (504, 260), (520, 320)])], (250, 230, 160), w=2, shadow=None)
    flat(c, [Poly([(388, 312), (398, 278), (412, 312)]), Poly([(488, 312), (502, 278), (512, 312)])], (250, 170, 180))
    toon(c, Ell(450, 380, 90, 80), (250, 230, 160), w=2.2)
    flat(c, Ell(450, 410, 52, 40), (250, 246, 220))
    for ex in (418, 482):
        flat(c, Ell(ex, 366, 9, 13), (50, 40, 60))
        flat(c, Circ(ex + 3, 360, 4), (250, 250, 250))
    flat(c, [Ell(398, 392, 12, 7), Ell(502, 392, 12, 7)], (250, 170, 180))
    flat(c, [Thick(442, 394, 450, 400, 2.4), Thick(450, 400, 458, 394, 2.4)], (50, 40, 60))
    # bowl, ball, bed, plant
    bowl = (230, 90, 90) if "bowl" not in d else (90, 170, 230)
    toon(c, Poly([(150, 500), (250, 500), (236, 530), (164, 530)]), bowl, w=2)
    flat(c, Ell(200, 500, 46, 9), (190, 130, 80))
    if "ball" not in d:
        toon(c, Circ(700, 500, 26), (250, 200, 60), w=2)
        flat(c, [Thick(676, 492, 724, 508, 3)], (230, 90, 90))
    toon(c, Poly([(780, 420), (860, 420), (850, 380), (790, 380)]), (190, 110, 70), w=1.6, shadow=None)
    toon(c, [Ell(806, 350, 16, 36), Ell(836, 350, 16, 36), Ell(820, 340, 14, 42)], (90, 170, 100), w=1.4, shadow=None)
    # status bars
    panel(c, 16, 14, 470, 60, (250, 250, 250))
    for k, (col, frac) in enumerate((((240, 90, 110), 0.8), ((250, 190, 60), 0.6 if "bar" not in d else 0.25), ((90, 180, 240), 0.45))):
        x = 30 + k * 148
        flat(c, Circ(x + 10, 37, 11), col)
        bar(c, x + 28, 30, x + 130, 44, frac, col)
    panel(c, 760, 14, 886, 60, (250, 250, 250))
    flat(c, Circ(784, 37, 12), (250, 200, 60))
    digits(c, 806, 26, "580", (90, 70, 60), 4)
    # action buttons
    icons = [(240, 120, 90), (90, 200, 120), (90, 170, 240), (170, 120, 220)]
    if "button" in d:
        icons[1] = (250, 200, 60)
    for k, col in enumerate(icons):
        x = 270 + k * 120
        toon(c, Circ(x, 566, 28), (250, 250, 250), w=2, shadow=None)
        toon(c, Circ(x, 566, 18), col, w=1.4, shadow=None)


L187_ELEMENTS = [
    E("heart%d" % k, (lambda k: lambda c, m: heart(c, 520 + k * 30, 300, 1.4, (250, 110, 140)))(k), daynight="untinted",
      anim=dict(driftVelocity=(4, 40), driftLength=80, driftFade=True, phase=k / 3)) for k in range(3)] + [
    E("tail", lambda c, m: toon(c, Ell(360, 430, 30, 12), (250, 230, 160), w=1.6, shadow=None), pivot=(380, 432), anim=dict(swingAngle=18, swingSpeed=1.0)),
    E("zzz", lambda c, m: flat(c, Poly(star_pts(300, 300, 8, 2, points=4, rot=0)), (255, 255, 230)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
    E("cloud", lambda c, m: flat(c, [Ell(620, 140, 30, 10), Ell(640, 132, 18, 10)], (250, 250, 255)), anim=dict(bobAmplitude=(30, 0), bobSpeed=0.08)),
]

L187_DIFFS = [
    ("curtain", 560, 180, 0),
    ("frame", 180, 150, 0),
    ("cushion", 450, 480, 0),
    ("bowl", 200, 515, 0),
    ("ball", 700, 500, 0),
    ("bar", 230, 37, 0),
    ("button", 390, 566, 0),
]


# =================================================================== Level 188 mini golf
def l188_bg(c, d):
    c.rect(0, 0, W, H, (90, 150, 80))
    rnd = random.Random(1880)
    for _ in range(50):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        flat(c, Circ(x, y, rnd.uniform(3, 6)), rnd.choice([(250, 240, 120), (250, 160, 190), (250, 250, 250)]))
    # course (wooden border + green)
    course = [RRect(80, 80, 820, 220, 40), RRect(680, 80, 820, 540, 40), RRect(80, 400, 820, 540, 40)]
    toon(c, course, (170, 120, 80), w=2, shadow=(0, 4, 6, 0.3))
    flat(c, [RRect(96, 96, 804, 204, 30), RRect(696, 96, 804, 524, 30), RRect(96, 416, 804, 524, 30)], (110, 200, 100))
    for x in range(110, 800, 40):
        flat(c, Thick(x, 100, x + 20, 200, 6), (120, 210, 110))
    # tee + hole + flag
    flat(c, RRect(110, 130, 160, 170, 6), (90, 180, 90))
    flat(c, Ell(180, 470, 14, 8), (30, 40, 30))
    flat(c, Thick(180, 470, 180, 400, 3), (250, 250, 250))
    flag = (230, 60, 60) if "flag" not in d else (250, 200, 60)
    toon(c, Poly([(180, 400), (220, 412), (180, 424)]), flag, w=1.2, shadow=None)
    # windmill on the top lane
    roof = (220, 80, 80) if "roof" not in d else (80, 120, 210)
    toon(c, Poly([(400, 220), (480, 220), (470, 120), (410, 120)]), (250, 240, 220), w=2)
    toon(c, Poly([(400, 124), (480, 124), (440, 80)]), roof, w=2)
    flat(c, RRect(426, 180, 454, 220, 6), (60, 50, 50))
    # water hazard on the right lane + bridge
    toon(c, Ell(750, 320, 50, 90), (90, 170, 230), w=1.6, shadow=None)
    br = (180, 120, 80) if "bridge" not in d else (240, 240, 240)
    toon(c, RRect(696, 300, 804, 340, 3), br, w=1.6, shadow=None)
    for x in range(706, 800, 16):
        flat(c, Thick(x, 300, x, 340, 2), lit(br, 0.8))
    # sand bunker on the bottom lane
    toon(c, Ell(500, 470, 70, 30), (240, 220, 160), w=1.4, shadow=None)
    if "rock" not in d:
        toon(c, Poly(ngon(340, 470, 22, 6, rot=10)), (150, 150, 160), w=1.6)
    # trees + flower beds around
    for x, y in ((40, 40), (860, 40), (40, 320), (300, 320), (520, 320), (860, 580), (40, 580), (600, 580)):
        col = (60, 140, 70) if not ((x, y) == (520, 320) and "tree" in d) else (230, 140, 50)
        toon(c, [Circ(x, y, 30), Circ(x - 20, y + 14, 20), Circ(x + 20, y + 14, 20)], col, w=1.6)
    bed = (250, 120, 160) if "flowers" not in d else (120, 160, 250)
    toon(c, Ell(420, 330, 70, 26), (120, 90, 60), w=1.4, shadow=None)
    for k in range(7):
        flat(c, Circ(370 + k * 16, 330 + (k % 2) * 6 - 3, 6), bed)
    # HUD
    panel(c, 14, 548, 250, 594, (40, 50, 80))
    glyph_line(c, 26, 80, 571, (250, 250, 250), 1881, w=2, size=10)
    digits(c, 88, 556, "3", (250, 250, 250) if "par" not in d else (250, 200, 60), 7)
    glyph_line(c, 140, 190, 571, (250, 250, 250), 1882, w=2, size=10)
    digits(c, 200, 560, "2", (250, 250, 250), 6)
    panel(c, 850, 380, 886, 540, (40, 50, 80))
    flat(c, RRect(856, 440, 880, 534, 4), (250, 180, 60))
    flat(c, RRect(856, 480, 880, 534, 4), (90, 210, 110))


L188_ELEMENTS = [
    E("blades", lambda c, m: toon(c, [Thick(440, 70, 440, 170, 10), Thick(390, 120, 490, 120, 10)], (200, 160, 110), w=1.4, shadow=None), pivot=(440, 120),
      anim=dict(rotateSpeed=60)),
    E("ball", lambda c, m: toon(c, Circ(140, 150, 8), (250, 250, 250), w=1.2, shadow=None)),
    E("aim", lambda c, m: [flat(c, Circ(160 + k * 18, 150, 3), (250, 250, 250)) for k in range(4)], daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=1.2)),
    E("ripple", lambda c, m: c.ellipse_ring(750, 380, 20, 10, 2, (180, 220, 250)), pivot=(750, 380), anim=dict(pulse=0.3, scaleSpeed=0.6, twinkle=0.6, twinkleSpeed=0.6)),
    E("flagwave", lambda c, m: flat(c, Poly([(180, 424), (210, 430), (180, 436)]), (250, 250, 250, 0.6)), pivot=(180, 430), anim=dict(stretch=(0.3, 0), scaleSpeed=1.2)),
]

L188_DIFFS = [
    ("flag", 196, 412, 0),
    ("roof", 440, 104, 0),
    ("bridge", 750, 320, 0),
    ("rock", 340, 470, 0),
    ("tree", 520, 330, 0),
    ("flowers", 418, 330, 0),
    ("par", 102, 571, 0),
]


# =================================================================== Level 189 island survival
SEA = 360


def l189_bg(c, d):
    c.gradient(0, SEA, (110, 190, 240), (220, 240, 250))
    toon(c, Circ(780, 80, 40), (250, 230, 110), w=1.6, shadow=None)
    for x, y in ((180, 70), (500, 50)):
        toon(c, [Circ(x, y, 22), Circ(x + 26, y + 6, 18), Circ(x - 26, y + 6, 16)], (250, 250, 255), w=1.2, shadow=None)
    flat(c, RRect(0, SEA - 120, W, SEA + 10, 0), (60, 150, 210))
    for y in range(SEA - 110, SEA, 18):
        for x in range((y // 18 % 2) * 30, W, 60):
            flat(c, Thick(x, y, x + 20, y, 2), (120, 190, 240))
    # beach
    toon(c, Poly([(-20, 600), (-20, 330), (200, 300), (500, 320), (780, 290), (920, 330), (920, 600)]), (240, 220, 160), w=2, shadow=None)
    flat(c, Poly([(-20, 340), (200, 310), (500, 330), (780, 300), (920, 340), (920, 350), (-20, 350)]), (250, 250, 250, 0.6))
    # palms
    for x, h, lean in ((80, 220, 30), (820, 200, -24)):
        pts = [(x + lean * (t / 6) ** 2, 400 - h * t / 6) for t in range(7)]
        toon(c, [Thick(a[0], a[1], b[0], b[1], 14 - i) for i, (a, b) in enumerate(zip(pts, pts[1:]))], (160, 110, 70), w=1.4, shadow=None)
        tx, ty = pts[-1]
        for a in (200, 240, 300, 340, 20, 150):
            r = math.radians(a)
            toon(c, Poly([(tx, ty), (tx + math.cos(r) * 90, ty + math.sin(r) * 40 + 24), (tx + math.cos(r) * 46, ty + math.sin(r) * 20 - 8)]), (70, 160, 80), w=1.2,
                 shadow=None)
        n = 3 if not (x == 820 and "coconut" in d) else 1
        for k in range(n):
            flat(c, Circ(tx - 12 + k * 12, ty + 12, 9), (130, 90, 50))
    # shelter (lean-to)
    cloth = (230, 120, 70) if "shelter" not in d else (90, 160, 210)
    toon(c, [Thick(230, 430, 290, 300, 5), Thick(390, 430, 330, 300, 5)], (140, 100, 60), w=1.4, shadow=None)
    toon(c, Poly([(280, 300), (340, 300), (420, 440), (200, 440)]), cloth, w=2)
    flat(c, Poly([(300, 330), (320, 330), (360, 440), (260, 440)]), (60, 40, 30))
    # campfire (flames are elements)
    for k in range(5):
        a = math.radians(k * 72)
        flat(c, Circ(520 + math.cos(a) * 26, 470 + math.sin(a) * 10, 9), (150, 150, 160))
    toon(c, [Thick(498, 476, 542, 466, 6), Thick(500, 466, 540, 478, 6)], (130, 90, 50), w=1.2, shadow=None)
    # raft at the shore
    toon(c, [RRect(600, 340, 760, 372, 4)], (180, 130, 80), w=1.6, shadow=None)
    for x in range(610, 760, 18):
        flat(c, Thick(x, 340, x, 372, 2), (150, 100, 60))
    flat(c, Thick(680, 340, 680, 230, 3), (140, 100, 60))
    sail = (250, 246, 230) if "sail" not in d else (230, 90, 90)
    toon(c, Poly([(684, 232), (740, 320), (684, 320)]), sail, w=1.6, shadow=None)
    # crate wreck + crab
    if "crate" not in d:
        toon(c, RRect(140, 470, 210, 530, 3), (170, 120, 70), w=1.8)
        flat(c, [Thick(140, 470, 210, 530, 3), Thick(210, 470, 140, 530, 3)], (130, 90, 50))
    crab = (230, 80, 60) if "crab" not in d else (120, 120, 220)
    toon(c, [Ell(700, 480, 22, 14), Circ(674, 468, 8), Circ(726, 468, 8)], crab, w=1.4, shadow=None)
    flat(c, [Circ(694, 472, 2.4), Circ(706, 472, 2.4)], (30, 30, 40))
    # UI
    panel(c, 14, 14, 250, 92, (40, 50, 70))
    for k, (col, frac) in enumerate((((240, 80, 90), 0.75), ((250, 170, 60), 0.5), ((80, 170, 240), 0.35))):
        flat(c, Circ(32, 30 + k * 24, 7), col)
        bar(c, 48, 25 + k * 24, 236, 35 + k * 24, frac, col)
    panel(c, 780, 548, 886, 594, (40, 50, 70))
    glyph_line(c, 790, 840, 571, (250, 250, 250), 1891, w=2, size=10)
    digits(c, 846, 560, "7" if "day" not in d else "8", (250, 250, 250), 5)
    panel(c, 220, 540, 680, 596, (60, 50, 50))
    items = [(150, 110, 70), (160, 160, 170), (90, 170, 90), (230, 90, 60), (250, 200, 60), None]
    if "slot" in d:
        items[2] = (200, 100, 200)
    for k, col in enumerate(items):
        x = 232 + k * 74
        flat(c, RRect(x, 548, x + 64, 588, 6), (90, 78, 74))
        if col:
            toon(c, Poly(ngon(x + 32, 568, 13, 5)), col, w=1.2, shadow=None)


L189_ELEMENTS = flame("fire", 520, 470, s=1.8, glow_night=False) + [
    E("smoke%d" % k, (lambda k: lambda c, m: toon(c, Circ(520, 420, 8), (220, 220, 226), w=1, shadow=None))(k), anim=dict(driftVelocity=(6, 30), driftLength=90,
                                                                                                                     driftFade=True, driftGrow=1.4, phase=k / 3))
    for k in range(3)] + [
    E("wave", lambda c, m: flat(c, Thick(0, 352, W, 352, 6), (250, 250, 250, 0.7)), anim=dict(bobAmplitude=(0, 4), bobSpeed=0.25)),
    E("gull", lambda c, m: flat(c, [Thick(400, 120, 412, 128, 2.4), Thick(412, 128, 424, 120, 2.4)], (70, 70, 90)), anim=drift_across(400, 424, 22, start=420)),
]

L189_DIFFS = [
    ("coconut", 806, 210, 0),
    ("shelter", 310, 380, 0),
    ("sail", 708, 290, 0),
    ("crate", 175, 500, 0),
    ("crab", 700, 476, 0),
    ("day", 856, 571, 0),
    ("slot", 410, 568, 0),
]


# =================================================================== Level 190 cooking game
def dish(c, x, y, kind, s=1.0):
    toon(c, Ell(x, y, 26 * s, 10 * s), (250, 250, 250), w=1.2, shadow=None)
    if kind == "burger":
        toon(c, [Ell(x, y - 6 * s, 16 * s, 8 * s)], (230, 160, 80), w=1, shadow=None)
        flat(c, RRect(x - 16 * s, y - 4 * s, x + 16 * s, y, 2), (120, 70, 40))
    elif kind == "salad":
        flat(c, [Circ(x - 8 * s, y - 4 * s, 7 * s), Circ(x + 6 * s, y - 6 * s, 7 * s), Circ(x, y - 2 * s, 6 * s)], (110, 200, 90))
        flat(c, Circ(x + 2 * s, y - 6 * s, 3 * s), (230, 60, 60))
    else:   # soup
        flat(c, Ell(x, y - 2 * s, 18 * s, 6 * s), (240, 140, 60))


def l190_bg(c, d):
    c.rect(0, 0, W, 340, (230, 236, 240))
    for y in range(120, 340, 30):
        for x in range((y // 30 % 2) * 30, W, 60):
            flat(c, RRect(x + 1, y + 1, x + 29, y + 29, 2), (240, 244, 248))
    # order tickets on a rail
    flat(c, RRect(0, 14, W, 22, 0), (160, 164, 176))
    orders = [("burger", 0.8), ("salad", 0.5), ("soup", 0.3), ("burger", 0.9)]
    if "order" in d:
        orders[2] = ("salad", 0.3)
    for k, (kind, t) in enumerate(orders):
        x = 120 + k * 200
        toon(c, RRect(x - 70, 22, x + 70, 104, 6), (250, 250, 236), w=1.8, shadow=None)
        dish(c, x - 22, 62, kind, 1.2)
        glyph_line(c, x + 14, x + 64, 56, (120, 110, 100), 1900 + k, w=1.6, size=8)
        bar(c, x - 60, 88, x + 60, 96, t, (90, 200, 110) if t > 0.4 else (240, 90, 80))
    # shelves with ingredient jars
    toon(c, RRect(40, 150, 360, 162, 2), (170, 120, 80), w=1.4, shadow=None)
    for k, col in enumerate(((230, 60, 60), (250, 200, 60), (110, 190, 90), (240, 140, 60), (170, 110, 200))):
        toon(c, RRect(54 + k * 62, 104 + 8, 94 + k * 62, 150, 6), col if not (k == 1 and "jar" in d) else (90, 170, 230), w=1.4, shadow=None)
    # range hood + stoves
    toon(c, Poly([(500, 120), (820, 120), (780, 170), (540, 170)]), (190, 194, 204), w=2)
    c.rect(0, 340, W, H, (200, 170, 130))
    toon(c, RRect(-10, 300, 910, 360, 4), (180, 184, 196), w=2, shadow=None)
    for k, x in enumerate((560, 700)):
        toon(c, RRect(x - 60, 260, x + 60, 300, 4), (60, 60, 70), w=1.6, shadow=None)
        pan = (60, 60, 70) if not (k == 0 and "pan" in d) else (210, 120, 60)
        toon(c, [Ell(x, 254, 50, 14), Thick(x + 50, 254, x + 100, 244, 6)], pan, w=1.6, shadow=None)
    flat(c, Ell(560, 250, 34, 8), (240, 140, 60))
    flat(c, [Ell(690, 250, 18, 6), Ell(714, 252, 16, 5)], (180, 100, 60))
    # cutting board + veg
    toon(c, RRect(120, 250, 300, 300, 6), (210, 170, 120), w=1.8, shadow=None)
    toon(c, Circ(170, 268, 18), (230, 60, 60) if "tomato" not in d else (250, 200, 60), w=1.4, shadow=None)
    flat(c, [Thick(230, 270, 290, 262, 4), Thick(222, 274, 240, 268, 6)], (200, 204, 214))
    # ingredient bins along the counter front
    for k, col in enumerate(((230, 60, 60), (110, 200, 90), (230, 160, 80), (250, 230, 120))):
        x = 100 + k * 120
        toon(c, RRect(x - 50, 370, x + 50, 440, 6), (150, 154, 166), w=1.8, shadow=None)
        for i in range(5):
            flat(c, Circ(x - 32 + i * 16, 392 + (i % 2) * 8, 9), col if not (k == 1 and "bin" in d) else (240, 140, 200))
    # plates waiting at the pass
    for k, kind in enumerate(("burger", "soup", "salad")):
        dish(c, 640 + k * 90, 400, kind if not (k == 2 and "plate" in d) else "burger", 1.2)
    # chef
    chibi(c, 450, 560, s=1.6, hair=(90, 60, 40), outfit=(250, 250, 250), face=1)
    hat = (250, 250, 250) if "hat" not in d else (240, 120, 120)
    toon(c, [RRect(426, 380, 474, 408, 4), Circ(436, 376, 14), Circ(464, 376, 14), Circ(450, 368, 16)], hat, w=1.6, shadow=None)
    # HUD
    panel(c, 14, 548, 200, 594, (60, 50, 50))
    flat(c, Circ(38, 571, 12), (250, 200, 60))
    digits(c, 60, 560, "1250", (250, 250, 250), 5)
    panel(c, 700, 548, 886, 594, (60, 50, 50))
    bar(c, 716, 564, 870, 578, 0.6, (240, 160, 60))


L190_ELEMENTS = flame("fl1", 540, 300, s=0.9, glow_night=False) + flame("fl2", 580, 300, s=0.9, glow_night=False) + [
    E("steam%d" % k, (lambda k: lambda c, m: toon(c, Circ(560, 236, 8), (240, 240, 246), w=1, shadow=None))(k), anim=dict(driftVelocity=(4, 30), driftLength=70,
                                                                                                                        driftFade=True, driftGrow=1.4, phase=k / 3))
    for k in range(3)] + [
    E("sizzle", lambda c, m: [flat(c, Circ(x, 246, 3), (255, 230, 150)) for x in (680, 700, 720)], daynight="untinted", anim=dict(bobAmplitude=(0, 6), bobSpeed=2.0, twinkle=0.6, twinkleSpeed=3)),
    E("knife", lambda c, m: toon(c, Thick(250, 240, 290, 226, 4), (200, 204, 214), w=1, shadow=None), pivot=(250, 240), anim=dict(swingAngle=12, swingSpeed=1.4)),
]

L190_DIFFS = [
    ("order", 498, 58, 0),
    ("jar", 136, 130, 0),
    ("pan", 560, 254, 0),
    ("tomato", 170, 268, 0),
    ("bin", 220, 400, 0),
    ("plate", 820, 395, 0),
    ("hat", 450, 380, 0),
]


# =================================================================== Level 191 hex strategy map
HR = 36
HX, HY = math.sqrt(3) * HR, 1.5 * HR


def hex_c(q, r):
    return 20 + q * HX + (r % 2) * HX / 2, 30 + r * HY


TERRAIN = [
    "ggfffggwwggmmg",
    "gffggggwwgmmmg",
    "ggggcggwggmmgg",
    "gggggggwgggggf",
    "wwgggvgbggggff",
    "wwwgggggggvgff",
    "wwggmmggggggfg",
    "wggmmmggfggcgg",
    "gggmmgggffgggg",
    "ggggggggfgggww",
    "fggggvggggggww",
]
TCOL = {"g": (130, 200, 100), "f": (70, 150, 80), "w": (80, 160, 220), "m": (160, 150, 140), "c": (130, 200, 100), "v": (130, 200, 100), "b": (80, 160, 220)}


def l191_bg(c, d):
    c.rect(0, 0, W, H, (130, 200, 100))
    for r, row in enumerate(TERRAIN):
        for q, ch in enumerate(row):
            x, y = hex_c(q, r)
            if (q, r) == (12, 4) and "forest" in d:
                ch = "g"
            if (q, r) == (4, 7) and "mount" in d:
                ch = "f"
            flat(c, Poly(ngon(x, y, HR - 1, 6, rot=30)), TCOL[ch])
            flat(c, Poly(ngon(x, y, HR - 6, 6, rot=30)), lit(TCOL[ch], 1.06))
            if ch == "f":
                for dx, dy in ((-10, 4), (8, -4), (2, 10)):
                    toon(c, Poly([(x + dx - 9, y + dy + 8), (x + dx + 9, y + dy + 8), (x + dx, y + dy - 14)]), (50, 120, 60), w=1, shadow=None)
            elif ch == "m":
                toon(c, Poly([(x - 22, y + 14), (x, y - 20), (x + 22, y + 14)]), (130, 120, 115), w=1.2, shadow=None)
                snow = (250, 250, 250) if not ((q, r) == (11, 1) and "snow" in d) else (130, 120, 115)
                flat(c, Poly([(x - 12, y - 2), (x, y - 20), (x + 12, y - 2)]), snow)
            elif ch == "w":
                flat(c, [Thick(x - 12, y - 4, x - 2, y - 4, 2), Thick(x + 2, y + 6, x + 12, y + 6, 2)], (150, 210, 250))
            elif ch == "b":
                toon(c, RRect(x - 26, y - 8, x + 26, y + 8, 2), (170, 120, 80) if "bridge" not in d else (200, 200, 210), w=1.2, shadow=None)
            elif ch == "c":
                flag = (220, 60, 60) if q > 6 else ((60, 110, 220) if "flag" not in d else (240, 200, 60))
                toon(c, [RRect(x - 22, y - 16, x + 22, y + 16, 2), RRect(x - 26, y - 26, x - 12, y + 16, 2), RRect(x + 12, y - 26, x + 26, y + 16, 2)], (200, 196, 206),
                     w=1.4, shadow=None)
                flat(c, Thick(x, y - 16, x, y - 46, 2), (90, 80, 70))
                toon(c, Poly([(x, y - 46), (x + 30, y - 38), (x, y - 28)]), flag, w=1, shadow=None)
            elif ch == "v":
                roof = (200, 80, 60) if not ((q, r) == (10, 5) and "village" in d) else (90, 120, 200)
                for dx in (-12, 10):
                    toon(c, [RRect(x + dx - 9, y - 2, x + dx + 9, y + 14, 1)], (240, 230, 210), w=1, shadow=None)
                    toon(c, Poly([(x + dx - 12, y), (x + dx + 12, y), (x + dx, y - 14)]), roof, w=1, shadow=None)
    # hex outlines
    for r in range(len(TERRAIN)):
        for q in range(len(TERRAIN[0])):
            x, y = hex_c(q, r)
            pts = ngon(x, y, HR, 6, rot=30)
            flat(c, [Thick(a[0], a[1], b[0], b[1], 1.2) for a, b in zip(pts, pts[1:] + pts[:1])], (70, 100, 70, 0.5))
    # units
    def unit(q, r, team, weapon, base=None):
        x, y = hex_c(q, r)
        bc = base or ((60, 110, 220) if team == 0 else (220, 60, 60))
        toon(c, Ell(x, y + 14, 22, 8), bc, w=1.4, shadow=None)
        chibi(c, x, y + 14, s=0.55, hair=(90, 60, 40) if team == 0 else (40, 40, 50), outfit=bc, face=1 if team == 0 else -1, weapon=weapon)
    unit(3, 3, 0, "sword")
    unit(4, 5, 0, "staff")
    unit(2, 6, 0, "sword", base=(60, 110, 220) if "unit" not in d else (90, 200, 120))
    unit(9, 3, 1, "sword")
    unit(10, 7, 1, "staff")
    unit(8, 6, 1, "sword")
    # UI
    panel(c, 14, 470, 300, 592, (40, 44, 60), w=2)
    toon(c, Circ(70, 530, 40), (60, 110, 220), w=1.6, shadow=None)
    chibi(c, 70, 566, s=0.75, hair=(90, 60, 40) if "portrait" not in d else (240, 200, 90), outfit=(60, 110, 220), face=1)
    for k in range(3):
        glyph_line(c, 124, 280 - k * 30, 498 + k * 26, (250, 250, 250), 1910 + k, w=2, size=10)
    bar(c, 124, 572, 284, 582, 0.7, (90, 210, 110))
    panel(c, 700, 6, 886, 46, (40, 44, 60))
    glyph_line(c, 712, 790, 26, (250, 250, 250), 1913, w=2, size=10)
    digits(c, 800, 15, "05", (250, 250, 250), 4)


L191_ELEMENTS = [
    E("move", lambda c, m: [flat(c, Poly(ngon(*hex_c(q, r), HR - 4, 6, rot=30)), (250, 250, 150, 0.35)) for q, r in ((4, 2), (2, 3), (4, 3), (3, 4), (2, 2))],
      daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.8)),
    E("select", lambda c, m: c.ellipse_ring(hex_c(3, 3)[0], hex_c(3, 3)[1] + 14, 26, 10, 2.4, (250, 250, 250)), daynight="untinted",
      anim=dict(pulse=0.15, scaleSpeed=1.2)),
    E("cloud", lambda c, m: soft_union(c, [Ell(500, 200, 80, 30)], (250, 250, 255), 0.35, spread=20), anim=drift_across(420, 580, 8, start=500)),
]

L191_DIFFS = [
    ("forest", hex_c(12, 4)[0], hex_c(12, 4)[1], 0),
    ("snow", hex_c(11, 1)[0], hex_c(11, 1)[1] - 10, 0),
    ("flag", hex_c(4, 2)[0] + 12, hex_c(4, 2)[1] - 38, 0),
    ("village", hex_c(10, 5)[0], hex_c(10, 5)[1], 0),
    ("unit", hex_c(2, 6)[0], hex_c(2, 6)[1] + 14, 0),
    ("portrait", 70, 520, 0),
    ("mount", hex_c(4, 7)[0], hex_c(4, 7)[1], 0),
    ("bridge", hex_c(7, 4)[0], hex_c(7, 4)[1], 0),
]


# =================================================================== Level 192 visual novel
def l192_bg(c, d):
    c.gradient(0, 380, (250, 150, 120), (250, 210, 160))
    clouds = [(160, 80, 1.0), (640, 60, 0.8)] + ([(420, 120, 0.7)] if "cloud" in d else [])
    for x, y, k in clouds:
        flat(c, [Ell(x, y, 70 * k, 18 * k), Ell(x + 30 * k, y - 12 * k, 40 * k, 16 * k)], (250, 200, 190))
    flat(c, Circ(760, 250, 50), (250, 230, 160))
    # town + school building
    rnd = random.Random(1920)
    x = -10
    while x < W:
        w, h = rnd.randint(40, 80), rnd.randint(30, 90)
        flat(c, RRect(x, 330 - h, x + w, 380, 0), (200, 130, 140))
        x += w + rnd.randint(0, 6)
    flat(c, RRect(560, 200, 900, 380, 0), (230, 200, 190))
    for r in range(3):
        for k in range(6):
            win = (250, 230, 170) if not (r == 1 and k == 3 and "window" in d) else (90, 110, 160)
            flat(c, RRect(580 + k * 52, 220 + r * 50, 618 + k * 52, 250 + r * 50, 2), win)
    # rooftop floor + fence
    c.rect(0, 380, W, H, (170, 170, 180))
    for y in range(380, H, 30):
        flat(c, Thick(0, y, W, y, 1.4), (150, 150, 160))
    flat(c, [Thick(0, 340, W, 340, 4), Thick(0, 384, W, 384, 4)], (90, 150, 110))
    for x in range(0, W, 24):
        flat(c, Thick(x, 340, x, 384, 2), (90, 150, 110))
    if "fence" in d:
        flat(c, [RRect(60, 352, 160, 372, 3)], (250, 250, 240))
        glyph_line(c, 66, 156, 362, (200, 80, 80), 1925, w=2, size=10)
    # heroine sprite
    hair = (60, 50, 70)
    toon(c, [Ell(390, 300, 70, 160), Ell(510, 300, 70, 160)], hair, w=2)
    toon(c, Poly([(340, 600), (560, 600), (530, 380), (370, 380)]), (60, 70, 110), w=2)
    toon(c, Poly([(400, 380), (500, 380), (470, 470), (430, 470)]), (250, 250, 250), w=1.6, shadow=None)
    ribbon = (220, 50, 70) if "ribbon" not in d else (60, 160, 220)
    toon(c, [Poly([(450, 400), (420, 384), (420, 420)]), Poly([(450, 400), (480, 384), (480, 420)])], ribbon, w=1.4, shadow=None)
    toon(c, Ell(450, 270, 74, 86), SKIN, w=2)
    toon(c, [Poly([(372, 250), (390, 180), (450, 160), (510, 180), (528, 250), (500, 210), (470, 230), (450, 200), (420, 230), (400, 210)])], hair, w=1.8, shadow=None)
    eye = (90, 60, 150) if "eyes" not in d else (60, 150, 90)
    for ex in (420, 480):
        flat(c, Ell(ex, 280, 13, 18), eye)
        flat(c, Ell(ex, 288, 9, 10), lit(eye, 0.6))
        flat(c, Circ(ex + 4, 274, 5), (250, 250, 250))
    flat(c, [Ell(400, 312, 12, 6), Ell(500, 312, 12, 6)], (250, 170, 170))
    flat(c, Thick(440, 322, 460, 322, 2.4), (180, 90, 100))
    clip = (250, 200, 60) if "clip" not in d else (240, 120, 200)
    toon(c, Poly(star_pts(510, 200, 14, 6)), clip, w=1.2, shadow=None)
    # dialogue box
    toon(c, RRect(20, 450, 880, 590, 14), (250, 250, 250, 0.92), w=2.5, shadow=None)
    tag = (220, 80, 120) if "tag" not in d else (90, 160, 220)
    toon(c, RRect(40, 426, 200, 466, 10), tag, w=2, shadow=None)
    glyph_line(c, 60, 190, 446, (250, 250, 250), 1921, w=2.6, size=12)
    for k in range(3):
        glyph_line(c, 50, 830 - k * 140, 494 + k * 30, (70, 60, 80), 1922 + k, w=2.4, size=12)
    for k in range(4):
        toon(c, RRect(560 + k * 78, 562, 630 + k * 78, 582, 8), (220, 220, 230) if not (k == 1 and "button" in d) else (250, 200, 80), w=1.2, shadow=None)


L192_ELEMENTS = [
    E("next", lambda c, m: toon(c, Poly([(844, 548), (864, 548), (854, 560)]), (220, 80, 120), w=1.2, shadow=None), daynight="untinted",
      anim=dict(bobAmplitude=(0, 5), bobSpeed=1.2)),
    E("petal%d" % 0, lambda c, m: flat(c, Ell(100, 100, 6, 3), (250, 190, 210)), anim=dict(driftVelocity=(40, -30), driftLength=300, driftFade=True)),
    E("petal%d" % 1, lambda c, m: flat(c, Ell(300, 60, 6, 3), (250, 190, 210)), anim=dict(driftVelocity=(40, -30), driftLength=300, driftFade=True, phase=0.5)),
    E("blink", lambda c, m: [flat(c, Ell(ex, 280, 14, 19), SKIN) for ex in (420, 480)], daynight="untinted", anim=dict(blinkInterval=3.0, blinkDuration=0.2, phase=0.5)),
]

L192_DIFFS = [
    ("cloud", 420, 120, 0),
    ("window", 754, 285, 0),
    ("fence", 110, 362, 0),
    ("ribbon", 450, 402, 0),
    ("eyes", 450, 282, 0),
    ("clip", 510, 200, 0),
    ("tag", 120, 446, 0),
    ("button", 673, 572, 0),
]


# =================================================================== Level 193 pipe puzzle
CELL193, BX193, BY193 = 80, 130, 80
# pipe tiles: openings N E S W as a 4-char mask
PIPES = [
    ["0110", "0101", "0011", "1100", "0101", "0011", "0110", "0011"],
    ["1010", "0110", "1001", "0110", "0101", "1001", "1010", "1010"],
    ["1100", "1001", "0110", "1001", "0110", "0101", "1001", "1010"],
    ["0110", "0101", "1001", "0110", "1001", "0110", "0101", "1001"],
    ["1010", "0011", "0110", "1001", "0110", "1001", "0011", "0110"],
    ["1100", "1001", "1100", "0101", "1001", "0101", "1100", "1001"],
]
FILLED = {(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (4, 3)}


def pipe_tile(c, i, j, mask, col, water=False):
    cx, cy = BX193 + i * CELL193 + CELL193 / 2, BY193 + j * CELL193 + CELL193 / 2
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    shapes = [Thick(cx, cy, cx + dx * CELL193 / 2, cy + dy * CELL193 / 2, 22) for (dx, dy), on in zip(dirs, mask) if on == "1"] + [Circ(cx, cy, 11)]
    toon(c, shapes, col, w=1.6, shadow=None)
    if water:
        flat(c, [Thick(cx, cy, cx + dx * CELL193 / 2, cy + dy * CELL193 / 2, 10) for (dx, dy), on in zip(dirs, mask) if on == "1"] + [Circ(cx, cy, 5)],
             (80, 180, 250))


def l193_bg(c, d):
    c.gradient(0, H, (60, 80, 110), (40, 50, 80))
    toon(c, RRect(BX193 - 14, BY193 - 14, BX193 + 8 * CELL193 + 14, BY193 + 6 * CELL193 + 14, 14), (90, 100, 120), w=2.5)
    for j in range(6):
        for i in range(8):
            flat(c, RRect(BX193 + i * CELL193 + 2, BY193 + j * CELL193 + 2, BX193 + (i + 1) * CELL193 - 2, BY193 + (j + 1) * CELL193 - 2, 6),
                 (110, 120, 140) if (i + j) % 2 else (100, 110, 130))
    for j, row in enumerate(PIPES):
        for i, mask in enumerate(row):
            if (i, j) == (5, 4) and "pipe" in d:
                mask = "1010"
            if (i, j) == (6, 1) and "rock" not in d:
                toon(c, Poly(ngon(BX193 + i * CELL193 + 40, BY193 + j * CELL193 + 40, 26, 7, rot=10)), (150, 140, 130), w=1.6)
                continue
            col = (190, 196, 206) if not ((i, j) == (1, 5) and "copper" in d) else (220, 140, 80)
            pipe_tile(c, i, j, mask, col, water=(i, j) in FILLED)
    # source tank (left) + drain (right)
    toon(c, [RRect(20, 60, 110, 180, 10), Thick(110, 120, 130, 120, 22)], (190, 196, 206), w=2)
    flat(c, RRect(28, 90, 102, 172, 8), (80, 180, 250))
    valve = (220, 60, 60) if "valve" not in d else (60, 180, 100)
    toon(c, [Circ(65, 50, 18), Thick(65, 50, 65, 66, 6)], valve, w=1.6, shadow=None)
    drain = (90, 100, 120) if "drain" not in d else (230, 190, 70)
    toon(c, [RRect(790, 440, 880, 560, 10), Thick(770, 520, 790, 520, 22)], drain, w=2)
    flat(c, Ell(835, 450, 34, 8), (40, 50, 60))
    # HUD
    panel(c, 300, 14, 600, 56, (250, 240, 220))
    for k in range(3):
        toon(c, Poly(star_pts(330 + k * 38, 35, 18, 8)), (250, 200, 60) if k < 2 or "star" in d else (190, 180, 190), w=1.2, shadow=None)
    digits(c, 450, 22, "023", (90, 70, 60), 5)
    panel(c, 20, 500, 110, 580, (250, 240, 220))
    toon(c, [Thick(42, 540, 88, 540, 6), Poly([(42, 526), (30, 540), (42, 554)])], (90, 140, 200), w=1.2, shadow=None)


L193_ELEMENTS = [
    E("flow", lambda c, m: [flat(c, Circ(BX193 + i * CELL193 + 40, BY193 + j * CELL193 + 40, 4), (220, 245, 255)) for i, j in FILLED], daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.4)),
    E("drip", lambda c, m: flat(c, Ell(835, 456, 4, 6), (80, 180, 250)), anim=dict(driftVelocity=(0, -40), driftLength=60, driftFade=True)),
    E("cursor", lambda c, m: c.ellipse_ring(BX193 + 4 * CELL193 + 40, BY193 + 4 * CELL193 + 40, 38, 38, 3, (250, 250, 150)), daynight="untinted",
      anim=dict(twinkle=0.6, twinkleSpeed=1.0)),
]

L193_DIFFS = [
    ("rock", BX193 + 6 * CELL193 + 40, BY193 + 1 * CELL193 + 40, 0),
    ("pipe", BX193 + 5 * CELL193 + 40, BY193 + 4 * CELL193 + 40, 0),
    ("copper", BX193 + 1 * CELL193 + 40, BY193 + 5 * CELL193 + 40, 0),
    ("valve", 65, 52, 0),
    ("drain", 835, 500, 0),
    ("star", 406, 35, 0),
]


# =================================================================== Level 194 open-world map
def l194_bg(c, d):
    c.rect(0, 0, W, H, (70, 130, 170))
    rnd = random.Random(1940)
    for _ in range(40):
        x, y = rnd.uniform(0, 700), rnd.uniform(40, 600)
        flat(c, Thick(x, y, x + 14, y, 1.6), (100, 160, 200))
    # continent
    land = Poly([(60, 140), (180, 70), (340, 90), (460, 60), (600, 110), (660, 220), (620, 330), (680, 420), (600, 540), (420, 560), (300, 520), (180, 560),
                 (90, 470), (120, 360), (50, 260)])
    toon(c, land, (220, 200, 150), w=3, shadow=(0, 4, 6, 0.3))
    flat(c, Poly([(120, 160), (300, 120), (420, 160), (380, 260), (220, 280), (140, 240)]), (150, 190, 110))
    flat(c, Poly([(300, 360), (460, 330), (560, 400), (500, 500), (340, 490)]), (170, 200, 120))
    # mountains
    for k, (x, y) in enumerate(((470, 180), (510, 200), (550, 170), (520, 240))):
        toon(c, Poly([(x - 30, y + 20), (x, y - 30), (x + 30, y + 20)]), (150, 130, 120), w=1.4, shadow=None)
        snow = (250, 250, 250) if not (k == 2 and "snow" in d) else (150, 130, 120)
        flat(c, Poly([(x - 11, y - 12), (x, y - 30), (x + 11, y - 12)]), snow)
    # forests
    for x, y in ((170, 180), (200, 200), (230, 170), (260, 210), (370, 400), (400, 420), (430, 390)):
        if (x, y) == (400, 420) and "forest" in d:
            continue
        toon(c, [Circ(x, y, 12), Circ(x + 10, y + 6, 10)], (70, 140, 80), w=1.2, shadow=None)
    # lake
    toon(c, Ell(250, 400, 50, 28) if "lake" not in d else Ell(250, 400, 34, 20), (90, 160, 210), w=1.4, shadow=None)
    # roads (dotted)
    route = [(130, 300), (240, 250), (340, 300), (430, 300), (540, 330), (600, 460)]
    for a, b in zip(route, route[1:]):
        for t in range(0, 10, 2):
            x0, y0 = a[0] + (b[0] - a[0]) * t / 10, a[1] + (b[1] - a[1]) * t / 10
            x1, y1 = a[0] + (b[0] - a[0]) * (t + 1) / 10, a[1] + (b[1] - a[1]) * (t + 1) / 10
            flat(c, Thick(x0, y0, x1, y1, 3), (150, 110, 70))
    # towns
    for k, (x, y) in enumerate(((130, 300), (340, 300), (540, 330), (600, 460))):
        roof = (200, 70, 60) if not (k == 2 and "town" in d) else (70, 120, 200)
        toon(c, [RRect(x - 14, y - 8, x + 14, y + 10, 2)], (250, 240, 220), w=1.2, shadow=None)
        toon(c, Poly([(x - 18, y - 6), (x + 18, y - 6), (x, y - 24)]), roof, w=1.2, shadow=None)
    # quest markers
    for k, (x, y, kind) in enumerate(((240, 160, "!"), (470, 440, "?"), (580, 230, "!"))):
        col = (250, 200, 60) if kind == "!" else (90, 200, 240)
        if k == 0 and "quest" in d:
            col = (230, 80, 120)
        toon(c, [Circ(x, y - 30, 16), Poly([(x - 8, y - 18), (x + 8, y - 18), (x, y - 4)])], col, w=1.6, shadow=None)
        if kind == "!":
            flat(c, [RRect(x - 2.5, y - 40, x + 2.5, y - 30, 1), Circ(x, y - 24, 2.6)], (60, 40, 30))
        else:
            c.ellipse_ring(x, y - 34, 5, 5, 2.4, (60, 40, 30), ymax=y - 32)
            flat(c, Circ(x, y - 23, 2.4), (60, 40, 30))
    # small islands
    toon(c, Ell(760, 120, 40, 20), (220, 200, 150), w=1.6, shadow=None)
    toon(c, Ell(740, 520, 30, 16), (220, 200, 150), w=1.6, shadow=None)
    # fog of war (top left)
    soft_union(c, [Ell(60, 60, 140, 90)], (230, 234, 240), 0.8, spread=40)
    # compass rose
    comp = (200, 60, 60) if "compass" not in d else (60, 160, 90)
    toon(c, Circ(110, 520, 40), (250, 240, 220), w=1.6, shadow=None)
    toon(c, Poly(star_pts(110, 520, 34, 8, points=4)), (90, 80, 70), w=1, shadow=None)
    flat(c, Poly([(110, 486), (118, 520), (102, 520)]), comp)
    # legend panel (right)
    panel(c, 720, 170, 886, 470, (250, 240, 220), r=12, w=2)
    glyph_line(c, 740, 860, 196, (90, 70, 60), 1941, w=2.4, size=12)
    icons = [(200, 70, 60), (250, 200, 60), (90, 200, 240), (70, 140, 80), (150, 130, 120)]
    if "legend" in d:
        icons[3] = (230, 140, 50)
    for k, col in enumerate(icons):
        y = 236 + k * 46
        toon(c, Circ(752, y, 13), col, w=1.2, shadow=None)
        glyph_line(c, 776, 870, y, (110, 90, 80), 1942 + k, w=2, size=10)
    # tabs
    for k in range(4):
        toon(c, RRect(200 + k * 130, 8, 316 + k * 130, 42, 10), (250, 240, 220) if k == 1 else (180, 170, 160), w=1.6, shadow=None)
        glyph_line(c, 220 + k * 130, 300 + k * 130, 25, (90, 70, 60), 1950 + k, w=2, size=10)


L194_ELEMENTS = [
    E("player", lambda c, m: toon(c, Poly([(340, 284), (352, 314), (340, 306), (328, 314)]), (250, 250, 250), w=1.4, shadow=None), pivot=(340, 300),
      daynight="untinted", anim=dict(pulse=0.15, scaleSpeed=1.0)),
    E("ping", lambda c, m: c.ellipse_ring(580, 230, 20, 8, 2, (250, 220, 120)), pivot=(580, 230), daynight="untinted",
      anim=dict(pulse=0.5, scaleSpeed=0.5, twinkle=0.8, twinkleSpeed=0.5)),
    E("ship", lambda c, m: toon(c, [Poly([(700, 300), (740, 300), (732, 312), (708, 312)]), Poly([(720, 298), (720, 274), (736, 296)])], (250, 250, 246), w=1.2, shadow=None),
      anim=dict(bobAmplitude=(14, 3), bobSpeed=0.15)),
]

L194_DIFFS = [
    ("snow", 550, 152, 0),
    ("forest", 405, 423, 0),
    ("lake", 250, 400, 0),
    ("town", 540, 320, 0),
    ("quest", 240, 136, 0),
    ("compass", 110, 500, 0),
    ("legend", 752, 374, 0),
]


LEVELS = [
    ("Level185", "无尽跑酷", l185_bg, L185_ELEMENTS, L185_DIFFS, 60, OPTS),
    ("Level186", "点击冒险", l186_bg, L186_ELEMENTS, L186_DIFFS, 60, OPTS),
    ("Level187", "宠物养成", l187_bg, L187_ELEMENTS, L187_DIFFS, 60, OPTS),
    ("Level188", "迷你高尔夫", l188_bg, L188_ELEMENTS, L188_DIFFS, 60, OPTS),
    ("Level189", "荒岛求生", l189_bg, L189_ELEMENTS, L189_DIFFS, 60, OPTS),
    ("Level190", "料理游戏", l190_bg, L190_ELEMENTS, L190_DIFFS, 60, OPTS),
    ("Level191", "战棋策略", l191_bg, L191_ELEMENTS, L191_DIFFS, 60, OPTS),
    ("Level192", "视觉小说", l192_bg, L192_ELEMENTS, L192_DIFFS, 60, OPTS),
    ("Level193", "水管谜题", l193_bg, L193_ELEMENTS, L193_DIFFS, 60, OPTS),
    ("Level194", "世界地图", l194_bg, L194_ELEMENTS, L194_DIFFS, 60, OPTS),
]
