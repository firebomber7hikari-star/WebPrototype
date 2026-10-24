# -*- coding: utf-8 -*-
"""Mixed themes part 3 (paper-craft side views / interiors, full-bleed, original designs, no brands):
  Level255 古希腊神庙 - a hilltop temple by the sea: columns, pediment, statue, olive trees, thinkers, amphorae
  Level256 丛林遗迹   - overgrown jungle ruins: stepped pyramid, carved stone face, vines, macaws, explorer
  Level257 葡萄园     - a vineyard harvest: rolling vine rows, farmhouse with tower, cypresses, pickers
  Level258 奶牛牧场   - a dairy farm: silo and barn, wind pump, cows, milk churns, hay, chickens, farmer
  Level259 渔村       - a fishing village: stilt houses, boats, drying nets, crates of fish, fisherman, cat
  Level260 冰淇淋店   - an ice-cream parlour: tubs in the counter, cone display, menu board, stools
  Level261 花店       - a flower shop: buckets of flowers, hanging plants, florist wrapping a bouquet
  Level262 天文台     - an observatory at night: dome with open slit, telescope, star chart, astronomers
  Level263 音乐教室   - a music classroom: piano, drum kit, xylophone, guitars on the wall, notes on the board
  Level264 雪夜小木屋 - a snowy night cabin in the woods: lit windows, chimney smoke, snowman, sled, deer
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, layer, palm, rock, sky, smoke_el, stars_bg, tree_pine,
                 tree_round)
from fills import far_forest, far_ridge, far_round_trees
from stylekit import figure
from levels_akiba import modern, sign_box
from levels_festival import npiece
from levels_homes import planks, steam
from levels_mix1 import balloon
from levels_mix2 import wheel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def column(c, x, base, top, w, col):
    piece(c, [RRect(x - w / 2, top + 10, x + w / 2, base - 8, 1), RRect(x - w / 2 - 6, top, x + w / 2 + 6, top + 12, 2), RRect(x - w / 2 - 6, base - 10, x + w / 2 + 6, base, 2)],
          col, border=1.2, shadow=PROP)
    for k in (-1, 0, 1):
        flat(c, Thick(x + k * w / 4, top + 14, x + k * w / 4, base - 12, 1.2), lit(col, 0.88))


def toga(c, x, base, h, cloth, skin=SKIN, hair=(120, 90, 70), beard=None):
    hx, hy = figure(c, x, base, cloth, head=skin, h=h)
    flat(c, Thick(x - 7 * h, base - 28 * h, x + 7 * h, base - 6 * h, 3 * h), lit(cloth, 0.86))
    flat(c, Ell(hx - 1 * h, hy - 5 * h, 7 * h, 3.4 * h), hair)
    if beard:
        flat(c, Ell(hx + 1 * h, hy + 5 * h, 5 * h, 4 * h), beard)
    return hx, hy


def amphora(c, x, base, s, col, band=(40, 30, 30)):
    piece(c, [Ell(x, base - 24 * s, 16 * s, 22 * s), RRect(x - 6 * s, base - 54 * s, x + 6 * s, base - 40 * s, 2), Ell(x, base - 54 * s, 10 * s, 3 * s),
              Poly([(x - 6 * s, base - 4 * s), (x + 6 * s, base - 4 * s), (x, base + 2 * s)])], col, border=1.2, shadow=PROP)
    flat(c, [Thick(x - 6 * s, base - 50 * s, x - 14 * s, base - 36 * s, 2.4 * s), Thick(x + 6 * s, base - 50 * s, x + 14 * s, base - 36 * s, 2.4 * s)], col)
    flat(c, Thick(x - 15 * s, base - 26 * s, x + 15 * s, base - 26 * s, 3 * s), band)


def olive_tree(c, x, base, s):
    piece(c, [Thick(x, base, x - 6 * s, base - 40 * s, 7 * s), Thick(x - 6 * s, base - 40 * s, x + 10 * s, base - 70 * s, 5 * s)], (130, 110, 90), shadow=PROP)
    piece(c, [Ell(x, base - 76 * s, 40 * s, 22 * s), Ell(x - 30 * s, base - 62 * s, 24 * s, 14 * s), Ell(x + 30 * s, base - 64 * s, 24 * s, 14 * s)], (130, 160, 110),
          shadow=PROP)


def goat(c, x, base, s, col=(240, 236, 226), face=1):
    for lx in (-12, -4, 8, 14):
        flat(c, RRect(x + lx * s * face - 2 * s, base - 18 * s, x + lx * s * face + 2 * s, base, 1), lit(col, 0.8))
    piece(c, [Ell(x, base - 22 * s, 18 * s, 9 * s), Ell(x + 20 * s * face, base - 32 * s, 8 * s, 6 * s)], col, border=1.2, shadow=SMALL)
    flat(c, [Thick(x + 18 * s * face, base - 38 * s, x + 12 * s * face, base - 46 * s, 2 * s), Thick(x + 24 * s * face, base - 26 * s, x + 24 * s * face, base - 20 * s, 2 * s)],
         (120, 100, 80))
    flat(c, Circ(x + 22 * s * face, base - 33 * s, 1.2 * s), INK)


# =================================================================== Level 255 Greek temple
def l255_bg(c, d):
    sky(c, (110, 170, 230), (210, 230, 246), H)
    cloud_bg(c, 680, 60, 0.6)
    # sea + trireme
    c.rect(0, 190, W, 260, (60, 130, 190))
    for k in range(7):
        flat(c, Thick(30 + k * 130, 210 + (k % 2) * 20, 80 + k * 130, 210 + (k % 2) * 20, 1.6), (120, 180, 220))
    piece(c, Poly([(60, 210), (180, 210), (166, 226), (74, 226)]), (120, 80, 60), border=1.2, shadow=SMALL)
    for k in range(6):
        flat(c, Thick(80 + k * 16, 226, 74 + k * 16, 240, 1.4), (120, 80, 60))
    flat(c, Thick(120, 210, 120, 140, 2), (100, 70, 50))
    sail = (250, 246, 236) if "sail" not in d else (220, 90, 70)
    piece(c, RRect(92, 146, 148, 196, 2), sail, border=1, shadow=SMALL)
    flat(c, Thick(92, 170, 148, 170, 4), (200, 70, 60))
    # hill
    piece(c, hill_strip(240, [(30, 0.006, 0.2), (12, 0.02, 1.0)]), (170, 170, 110), shadow=LAYER)
    piece(c, hill_strip(320, [(14, 0.01, 1.2), (6, 0.03, 0.6)]), (190, 180, 120), shadow=LAYER)
    # temple
    piece(c, RRect(270, 300, 630, 330, 2), (236, 230, 216), border=1.5, shadow=PROP)
    piece(c, RRect(260, 330, 640, 346, 2), (226, 220, 206), border=1.5, shadow=PROP)
    for x in range(300, 620, 50):
        column(c, x, 300, 150, 26, (240, 236, 224))
    piece(c, RRect(270, 130, 630, 152, 2), (236, 230, 216), border=1.5, shadow=PROP)
    piece(c, Poly([(262, 132), (638, 132), (450, 70)]), (236, 230, 216), border=1.5, shadow=PROP)
    flat(c, Poly([(300, 124), (600, 124), (450, 82)]), (110, 150, 200))
    disc = (220, 170, 60) if "disc" not in d else (200, 80, 80)
    piece(c, Circ(450, 108, 14), disc, border=1, shadow=None)
    for x in range(280, 630, 30):
        flat(c, RRect(x, 136, x + 14, 148, 1), (200, 90, 70))
    # statue on a plinth (right)
    piece(c, RRect(760, 300, 840, 340, 2), (226, 220, 206), border=1.5, shadow=PROP)
    statue = (246, 244, 236) if "statue" not in d else (190, 140, 80)
    hx, hy = toga(c, 800, 300, 2.0, statue, skin=statue, hair=lit(statue, 0.9))
    flat(c, Thick(812, 236, 836, 200, 4), statue)
    # ground
    c.rect(0, 346, W, H, (210, 196, 150))
    for k in range(9):
        flat(c, Thick(20 + k * 100, 380 + (k % 3) * 60, 60 + k * 100, 380 + (k % 3) * 60, 2), (190, 176, 130))
    # olive trees
    olive_tree(c, 120, 420, 1.3)
    olive_tree(c, 700, 410, 1.0)
    # thinkers in togas
    toga(c, 290, 470, 2.0, (250, 246, 236) if "toga" not in d else (90, 140, 200), beard=(200, 200, 200))
    toga(c, 350, 466, 1.9, (200, 120, 90), beard=(90, 70, 50))
    # amphorae
    amphora(c, 620, 450, 1.4, (200, 110, 60) if "amphora" not in d else (60, 110, 160))
    amphora(c, 660, 456, 1.1, (190, 120, 70))
    # lyre player (centre front)
    hx, hy = toga(c, 450, 580, 2.3, (240, 200, 90) if "cloak" not in d else (150, 200, 120))
    piece(c, [Thick(470, 520, 476, 470, 3), Thick(496, 520, 490, 470, 3), Thick(474, 470, 492, 470, 3), Ell(483, 524, 16, 8)], (200, 160, 80), shadow=SMALL)
    # goats (left front)
    if "goat" not in d:
        goat(c, 110, 570, 2.0)
    goat(c, 200, 590, 1.6, col=(160, 120, 90), face=-1)
    # bread basket (right front)
    piece(c, Poly([(750, 540), (840, 540), (830, 580), (760, 580)]), (190, 140, 80), border=1.5, shadow=PROP)
    bread = (220, 160, 80) if "bread" not in d else (150, 90, 60)
    flat(c, [Ell(770 + k * 22, 534, 13, 9) for k in range(4)], bread)


L255_ELEMENTS = [
    bird_el("gull", 520, 40, s=9, speed=-16),
    E("wave", lambda c, m: [flat(c, Thick(x, 240, x + 40, 240, 1.6), (160, 210, 240)) for x in (220, 560, 760)], daynight="untinted",
      anim=dict(bobAmplitude=(14, 0), bobSpeed=0.3)),
    E("leaves", lambda c, m: piece(c, Ell(150, 300, 6, 3), (130, 160, 110), shadow=None), pivot=(150, 300),
      anim=dict(driftVelocity=(20, 30), driftLength=100, driftFade=True, swingAngle=40, swingSpeed=1.0)),
    E("tail", lambda c, m: flat(c, Thick(178, 562, 186, 552, 2), (160, 120, 90)), pivot=(178, 562), anim=dict(swingAngle=30, swingSpeed=2.0)),
]

L255_DIFFS = [
    ("sail", 120, 172, 0),
    ("disc", 450, 108, 0),
    ("statue", 800, 240, 0),
    ("toga", 290, 430, 0),
    ("amphora", 620, 420, 0),
    ("goat", 112, 545, 0),
    ("cloak", 450, 530, 0),
    ("bread", 800, 536, 0),
]


# =================================================================== Level 256 jungle ruins
STONE = (150, 150, 130)


def l256_bg(c, d):
    sky(c, (170, 210, 190), (220, 236, 220), H)
    far_forest(c, 180, 80, (110, 160, 120), 2561)
    # stepped pyramid
    for k in range(6):
        w = 420 - k * 60
        y = 340 - k * 40
        piece(c, RRect(450 - w / 2, y - 40, 450 + w / 2, y, 1), lit(STONE, 1 - k * 0.02), border=1.5, shadow=PROP)
        for j in range(int(w // 30)):
            flat(c, Thick(450 - w / 2 + j * 30, y - 40, 450 - w / 2 + j * 30, y, 1), lit(STONE, 0.88))
    flat(c, Poly([(420, 340), (480, 340), (470, 100), (430, 100)]), lit(STONE, 0.92))
    for y in range(110, 340, 12):
        flat(c, Thick(430 - (y - 100) * 0.04, y, 470 + (y - 100) * 0.04, y, 1.4), lit(STONE, 0.78))
    piece(c, RRect(400, 40, 500, 100, 2), STONE, border=1.5, shadow=PROP)
    door = (40, 40, 40) if "shrine" not in d else (220, 170, 60)
    flat(c, RRect(436, 60, 464, 100, 2), door)
    # vines hanging over the pyramid
    for x, l in ((300, 120), (360, 90), (560, 110), (600, 140)):
        flat(c, Thick(x, 180, x + 6, 180 + l, 3), (70, 140, 70))
        for k in range(0, l, 20):
            flat(c, Ell(x + 4, 186 + k, 6, 3), (90, 160, 80))
    vf = (240, 90, 140) if "vine" not in d else (250, 200, 60)
    flat(c, [Circ(606, 240, 7), Circ(596, 270, 6)], vf)
    # sun disc carving (left wall ruin)
    piece(c, RRect(40, 160, 220, 360, 2), STONE, border=1.5, shadow=PROP)
    carve = lit(STONE, 0.8) if "carve" not in d else (200, 150, 60)
    c.ellipse_ring(130, 230, 44, 44, 6, carve)
    flat(c, Circ(130, 230, 18), carve)
    for k in range(8):
        a = k * math.pi / 4
        flat(c, Thick(130 + 26 * math.cos(a), 230 + 26 * math.sin(a), 130 + 36 * math.cos(a), 230 + 36 * math.sin(a), 4), carve)
    # macaw on a branch (right top)
    piece(c, Thick(700, 120, 900, 100, 8), (120, 90, 60), shadow=PROP)
    mac = (220, 50, 50) if "macaw" not in d else (60, 140, 230)
    piece(c, [Ell(790, 140, 14, 22), Circ(794, 114, 10), Poly([(782, 156), (798, 156), (792, 200)])], mac, border=1.2, shadow=SMALL)
    flat(c, Ell(788, 144, 6, 12), (250, 200, 60))
    flat(c, Poly([(802, 112), (812, 118), (802, 122)]), (240, 230, 210))
    # ground
    c.rect(0, 360, W, H, (110, 150, 90))
    piece(c, hill_strip(380, [(8, 0.02, 0.4), (5, 0.05, 1.1)]), (100, 140, 80), shadow=LAYER)
    # carved stone head (left middle)
    piece(c, [RRect(220, 330, 340, 450, 10)], STONE, border=1.5, shadow=PROP)
    flat(c, [RRect(236, 360, 270, 376, 3), RRect(290, 360, 324, 376, 3)], lit(STONE, 0.7))
    eye = (40, 40, 40) if "eye" not in d else (90, 200, 120)
    flat(c, [Circ(253, 368, 6), Circ(307, 368, 6)], eye)
    flat(c, [RRect(270, 390, 290, 420, 3), RRect(250, 428, 310, 438, 2)], lit(STONE, 0.75))
    # broken columns + steps (right)
    for x, h in ((640, 80), (700, 120), (760, 60)):
        piece(c, RRect(x - 16, 440 - h, x + 16, 440, 2), STONE, border=1.5, shadow=PROP)
    # jaguar statue (right foreground)
    jag = (170, 160, 130) if "jaguar" not in d else (90, 100, 110)
    piece(c, [RRect(740, 540, 860, 560, 2)], STONE, shadow=PROP)
    piece(c, [Ell(800, 520, 44, 20), Circ(842, 500, 16), Poly([(832, 488), (836, 476), (842, 486)]), Poly([(846, 486), (852, 476), (854, 488)]),
              Thick(756, 520, 740, 490, 6)], jag, border=1.5, shadow=PROP)
    flat(c, [Circ(848, 498, 2.4)], INK)
    # golden idol on a stone (centre)
    piece(c, RRect(410, 520, 490, 560, 3), STONE, border=1.5, shadow=PROP)
    idol = (240, 200, 60) if "idol" not in d else (120, 200, 220)
    piece(c, [RRect(434, 470, 466, 520, 6), Circ(450, 462, 14)], idol, border=1.2, shadow=SMALL)
    flat(c, [Circ(445, 460, 2), Circ(455, 460, 2)], INK)
    # explorer (left foreground)
    hx, hy = modern(c, 120, 590, (200, 180, 120), bottom=(120, 110, 80), hair=(90, 60, 40), h=2.3)
    pack = (90, 120, 80) if "pack" not in d else (200, 80, 70)
    piece(c, RRect(84, 500, 108, 550, 6), pack, border=1.2, shadow=SMALL)
    piece(c, [Ell(hx, hy - 8, 20, 5), Ell(hx, hy - 14, 12, 8)], (220, 200, 140), shadow=SMALL)
    # foreground ferns / leaves
    for x, a in ((-10, -40), (900, -140), (600, -70)):
        piece(c, Poly([(x, 600), (x + 120 * math.cos(math.radians(a)) - 20, 600 + 120 * math.sin(math.radians(a))), (x + 120 * math.cos(math.radians(a)) + 20,
                                                                                                                   600 + 120 * math.sin(math.radians(a)))]),
              (70, 140, 70), shadow=SMALL)


L256_ELEMENTS = [
    E("bfly", lambda c, m: piece(c, [Ell(560, 300, 7, 10), Ell(572, 300, 7, 10)], (90, 170, 240), shadow=None), pivot=(566, 300),
      anim=dict(orbitRadius=(50, 24), orbitSpeed=0.15, stretch=(0.6, 0), scaleSpeed=5)),
    E("torch", lambda c, m: flat(c, Poly([(390, 30), (400, 30), (395, 12)]), (255, 180, 60)), pivot=(395, 30), daynight="untinted", anim=dict(stretch=(0.2, 0.4), scaleSpeed=4)),
    E("vine2", lambda c, m: flat(c, Thick(880, 104, 884, 220, 2.4), (70, 140, 70)), pivot=(880, 104), anim=dict(swingAngle=6, swingSpeed=0.4)),
    bird_el("bird", 300, 60, s=9, speed=14),
]

L256_DIFFS = [
    ("carve", 130, 230, 0),
    ("shrine", 450, 80, 0),
    ("macaw", 792, 140, 0),
    ("eye", 280, 368, 0),
    ("vine", 601, 255, 0),
    ("pack", 96, 525, 0),
    ("idol", 450, 490, 0),
    ("jaguar", 800, 512, 0),
]


# =================================================================== Level 257 vineyard
def grape_vine_row(c, y, x0, x1, col=(80, 140, 70), grapes=(120, 60, 140), seed=0, swap=None):
    flat(c, Thick(x0, y, x1, y, 1.2), (140, 120, 100))
    rnd = random.Random(seed)
    x = x0
    k = 0
    while x < x1:
        piece(c, [Circ(x, y - 8, 12), Circ(x + 12, y - 12, 10)], col, shadow=SMALL)
        g = grapes if not (swap and swap[0] <= x <= swap[1]) else swap[2]
        if rnd.random() < 0.6:
            flat(c, [Circ(x + 4 + dx, y + 4 + dy, 3) for dx, dy in ((0, 0), (5, 0), (2.5, 5), (-2.5, 5), (0, 10))], g)
        x += 26
        k += 1


def l257_bg(c, d):
    sky(c, (140, 196, 240), (240, 230, 200), H)
    cloud_bg(c, 600, 60, 0.6)
    # balloon in the sky (centre)
    balloon(c, 450, 60, 26, [(240, 120, 60), (250, 230, 120)] if "balloon" not in d else [(90, 160, 220), (250, 230, 120)])
    far_ridge(c, 170, 30, (170, 190, 170), 2571)
    # farmhouse with tower on the hill (left)
    piece(c, hill_strip(230, [(16, 0.01, 0.6), (8, 0.03, 0.2)]), (160, 180, 100), shadow=LAYER)
    roof = (200, 100, 70) if "roof" not in d else (90, 120, 180)
    piece(c, [RRect(60, 160, 200, 230, 2), RRect(170, 120, 210, 230, 2)], (240, 220, 180), border=1.5, shadow=PROP)
    piece(c, [Poly([(50, 162), (210, 162), (180, 136), (80, 136)]), Poly([(164, 122), (216, 122), (190, 100)])], roof, border=1.5, shadow=PROP)
    flat(c, [RRect(90, 180, 110, 200, 2), RRect(140, 180, 160, 200, 2), RRect(182, 140, 198, 160, 2)], (120, 90, 70))
    # cypress trees (right)
    for k, x in enumerate((720, 760, 800)):
        if k == 2 and "cypress" in d:
            continue
        piece(c, [Ell(x, 160, 14, 60), RRect(x - 3, 200, x + 3, 230, 1)], (60, 110, 70), shadow=PROP)
    # vine rows on the slopes
    c.rect(0, 230, W, H, (170, 150, 100))
    for k, y in enumerate(range(260, 600, 44)):
        swap = (560, 680, (150, 200, 80)) if (k == 2 and "grapes" in d) else None
        grape_vine_row(c, y, -10, 910, seed=2572 + k, swap=swap)
    # picker with hat + basket on the back (middle left)
    hx, hy = modern(c, 300, 400, (240, 240, 230), bottom=(70, 80, 110), hair=(90, 60, 40), h=1.8)
    hat = (230, 200, 120) if "hat" not in d else (220, 80, 80)
    piece(c, [Ell(hx, hy - 8, 20, 5), Ell(hx, hy - 14, 11, 8)], hat, shadow=SMALL)
    piece(c, RRect(270, 336, 292, 372, 4), (190, 140, 80), shadow=SMALL)
    # picker 2 (right middle)
    modern(c, 620, 400, (220, 90, 90), bottom=(70, 80, 110), hair=(40, 30, 30), h=1.7, style="long")
    # barrels (left front)
    for k, x in enumerate((60, 140)):
        band = (90, 90, 100) if not (k == 0 and "barrel" in d) else (220, 180, 60)
        piece(c, Ell(x, 540, 34, 44), (150, 100, 60), border=1.5, shadow=PROP)
        flat(c, [Thick(x - 32, 520, x + 32, 520, 4), Thick(x - 32, 560, x + 32, 560, 4)], band)
    # crate of grapes (centre front)
    piece(c, RRect(400, 520, 500, 570, 3), (190, 150, 100), border=1.5, shadow=PROP)
    gc = (120, 60, 140) if "crate" not in d else (150, 200, 80)
    flat(c, [Circ(410 + (k % 9) * 10, 516 - (k // 9) * 8, 6) for k in range(18)], gc)
    # small cart (right front)
    cart = (60, 120, 180) if "cart" not in d else (200, 90, 70)
    piece(c, RRect(720, 500, 860, 550, 4), cart, border=1.5, shadow=PROP)
    flat(c, Thick(720, 520, 680, 540, 4), (120, 90, 60))
    for x in (750, 830):
        wheel(c, x, 560, 16, tyre=(110, 80, 60), hub=(200, 170, 120))


L257_ELEMENTS = [
    bird_el("bird", 300, 80, s=9, speed=16),
    E("cloud", lambda c, m: cloud_bg(c, 250, 110, 0.4), anim=drift_across(220, 280, 8)),
    E("bee", lambda c, m: piece(c, Ell(520, 330, 6, 4), (250, 210, 60), shadow=None), pivot=(520, 330), anim=dict(orbitRadius=(40, 16), orbitSpeed=0.25)),
]

L257_DIFFS = [
    ("roof", 140, 140, 0),
    ("balloon", 450, 70, 0),
    ("cypress", 800, 160, 0),
    ("hat", 300, 300, 0),
    ("grapes", 620, 360, 0),
    ("barrel", 60, 540, 0),
    ("crate", 450, 512, 0),
    ("cart", 790, 525, 0),
]


# =================================================================== Level 258 dairy farm
def cow(c, x, base, s, spots=(40, 40, 46), body=(250, 250, 246), face=1):
    for lx in (-22, -10, 14, 24):
        flat(c, RRect(x + lx * s * face - 4 * s, base - 28 * s, x + lx * s * face + 4 * s, base, 2), lit(body, 0.9))
    piece(c, [Ell(x, base - 38 * s, 34 * s, 16 * s), Ell(x + 38 * s * face, base - 42 * s, 13 * s, 11 * s)], body, border=1.5, shadow=PROP)
    flat(c, [Ell(x - 10 * s, base - 42 * s, 10 * s, 7 * s), Ell(x + 14 * s, base - 34 * s, 8 * s, 6 * s), Ell(x - 24 * s, base - 30 * s, 6 * s, 5 * s)], spots)
    flat(c, Ell(x + 46 * s * face, base - 38 * s, 7 * s, 6 * s), (240, 180, 180))
    flat(c, [Thick(x + 32 * s * face, base - 52 * s, x + 28 * s * face, base - 58 * s, 2.4 * s)], (240, 230, 200))
    flat(c, Circ(x + 40 * s * face, base - 46 * s, 1.6 * s), INK)
    flat(c, Ell(x - 4 * s, base - 22 * s, 6 * s, 4 * s), (240, 180, 180))


def churn(c, x, base, s, col):
    piece(c, [RRect(x - 12 * s, base - 40 * s, x + 12 * s, base, 3), Poly([(x - 12 * s, base - 40 * s), (x + 12 * s, base - 40 * s), (x + 6 * s, base - 50 * s),
                                                                         (x - 6 * s, base - 50 * s)]), RRect(x - 7 * s, base - 56 * s, x + 7 * s, base - 50 * s, 2)],
          col, border=1.2, shadow=SMALL)
    flat(c, Thick(x - 12 * s, base - 20 * s, x + 12 * s, base - 20 * s, 2), lit(col, 0.8))


def chicken(c, x, base, s, col):
    piece(c, [Ell(x, base - 10 * s, 12 * s, 9 * s), Circ(x + 9 * s, base - 18 * s, 6 * s)], col, border=1, shadow=SMALL)
    flat(c, [Poly([(x + 14 * s, base - 18 * s), (x + 20 * s, base - 16 * s), (x + 14 * s, base - 14 * s)])], (240, 160, 40))
    flat(c, Ell(x + 9 * s, base - 25 * s, 3 * s, 3 * s), (220, 50, 50))
    flat(c, [Thick(x - 2 * s, base - 2 * s, x - 2 * s, base + 2 * s, 1.4), Thick(x + 3 * s, base - 2 * s, x + 3 * s, base + 2 * s, 1.4)], (240, 160, 40))


def l258_bg(c, d):
    sky(c, (120, 186, 240), (220, 236, 248), H)
    cloud_bg(c, 300, 60, 0.6)
    far_ridge(c, 200, 40, (170, 200, 160), 2581)
    layer(c, 230, [(14, 0.01, 0.2), (8, 0.03, 1.0)], (130, 190, 100))
    # silo + barn (left)
    silo = (200, 200, 210)
    piece(c, RRect(100, 90, 170, 300, 6), silo, border=1.5, shadow=PROP)
    top = (60, 110, 180) if "silo" not in d else (220, 90, 70)
    piece(c, Poly([(100 + 35 + 35 * math.cos(math.pi * k / 10), 92 - 30 * math.sin(math.pi * k / 10)) for k in range(11)]), top, border=1.5, shadow=PROP)
    for y in range(110, 300, 24):
        flat(c, Thick(100, y, 170, y, 1.2), lit(silo, 0.88))
    piece(c, [RRect(170, 180, 330, 300, 2), Poly([(160, 182), (340, 182), (310, 140), (190, 140)])], (220, 80, 70), border=1.5, shadow=PROP)
    flat(c, Poly([(160, 182), (340, 182), (310, 140), (190, 140)]), (90, 80, 80))
    flat(c, RRect(220, 220, 280, 300, 1), (250, 246, 236))
    flat(c, [Thick(220, 220, 280, 300, 3), Thick(280, 220, 220, 300, 3)], (220, 80, 70))
    # wind pump (centre)
    piece(c, [Thick(430, 300, 446, 120, 3), Thick(470, 300, 454, 120, 3), Thick(436, 240, 464, 240, 2), Thick(440, 180, 460, 180, 2)], (150, 150, 160), shadow=PROP)
    vane = (220, 80, 70) if "vane" not in d else (250, 200, 60)
    piece(c, Poly([(470, 104), (520, 92), (520, 116)]), vane, border=1, shadow=SMALL)
    # farmhouse (right)
    hroof = (60, 120, 90) if "house" not in d else (180, 80, 160)
    piece(c, RRect(700, 170, 860, 280, 2), (250, 240, 220), border=1.5, shadow=PROP)
    piece(c, Poly([(690, 172), (870, 172), (780, 110)]), hroof, border=1.5, shadow=PROP)
    flat(c, [RRect(720, 200, 750, 230, 2), RRect(810, 200, 840, 230, 2), RRect(766, 230, 794, 280, 2)], (140, 100, 80))
    piece(c, RRect(820, 110, 840, 150, 1), (160, 90, 70), shadow=SMALL)
    # pasture
    c.rect(0, 300, W, H, (120, 186, 90))
    for k in range(8):
        flat(c, Poly([(0, 316 + k * 36), (W, 306 + k * 36), (W, 316 + k * 36), (0, 326 + k * 36)]), (128, 194, 98))
    for x in range(0, W, 50):
        flat(c, RRect(x, 330, x + 6, 370, 1), (240, 230, 210))
    flat(c, [Thick(0, 340, W, 340, 4), Thick(0, 358, W, 358, 4)], (240, 230, 210))
    # cows
    cow(c, 280, 470, 1.6, spots=(40, 40, 46) if "spots" not in d else (150, 90, 50))
    cow(c, 560, 440, 1.2, face=-1)
    cow(c, 700, 480, 1.0, spots=(150, 90, 50))
    # milk churns
    for k, x in enumerate((600, 640)):
        churn(c, x, 520, 1.4, (200, 206, 216) if not (k == 0 and "churn" in d) else (90, 150, 220))
    # chickens (left front)
    for k, x in enumerate((60, 120, 170)):
        chicken(c, x, 560 + (k % 2) * 10, 1.6, (240, 236, 226) if not (k == 1 and "chick" in d) else (200, 120, 60))
    # hay bales (centre front)
    if "hay" not in d:
        for x in (420, 490):
            piece(c, RRect(x - 34, 520, x + 34, 570, 6), (230, 200, 110), border=1.5, shadow=PROP)
            flat(c, [Thick(x - 34, 536, x + 34, 536, 2), Thick(x - 34, 554, x + 34, 554, 2)], (200, 160, 70))
    # farmer (right front)
    hx, hy = modern(c, 810, 600, (220, 80, 70) if "farmer" not in d else (90, 150, 220), bottom=(60, 90, 160), hair=(130, 130, 140), h=2.2)
    piece(c, [Ell(hx, hy - 8, 20, 5), Ell(hx, hy - 14, 11, 8)], (230, 200, 120), shadow=SMALL)
    flat(c, Thick(840, 470, 846, 600, 3), (150, 110, 70))


L258_ELEMENTS = [
    E("blades", lambda c, m: [flat(c, Thick(450, 110, 450 + 34 * math.cos(a), 110 + 34 * math.sin(a), 3), (200, 200, 210)) for a in [k * 0.785 for k in range(8)]],
      pivot=(450, 110), anim=dict(rotateSpeed=50)),
    E("tail", lambda c, m: flat(c, Thick(226, 418, 214, 450, 2.4), (250, 250, 246)), pivot=(226, 418), anim=dict(swingAngle=20, swingSpeed=1.4)),
    E("smoke", lambda c, m: piece(c, Circ(830, 100, 8), (240, 236, 230), shadow=None), pivot=(830, 100),
      anim=dict(driftVelocity=(6, -20), driftLength=50, driftFade=True, driftGrow=1.5)),
    E("peck", lambda c, m: chicken(c, 220, 590, 1.4, (200, 120, 60)), pivot=(220, 590), anim=dict(swingAngle=12, swingSpeed=1.6)),
    bird_el("bird", 600, 70, s=9, speed=-16),
]

L258_DIFFS = [
    ("silo", 135, 80, 0),
    ("vane", 495, 104, 0),
    ("house", 780, 140, 0),
    ("spots", 270, 412, 0),
    ("churn", 600, 490, 0),
    ("chick", 120, 554, 0),
    ("hay", 455, 545, 0),
    ("farmer", 810, 520, 0),
]


# =================================================================== Level 259 fishing village
def boat(c, x, base, s, hull, stripe=(250, 250, 246), sail=None):
    piece(c, Poly([(x - 50 * s, base - 22 * s), (x + 56 * s, base - 26 * s), (x + 40 * s, base), (x - 40 * s, base)]), hull, border=1.5, shadow=PROP)
    flat(c, Thick(x - 46 * s, base - 16 * s, x + 50 * s, base - 19 * s, 3 * s), stripe)
    if sail:
        flat(c, Thick(x, base - 22 * s, x, base - 90 * s, 2), (110, 80, 60))
        piece(c, Poly([(x + 2, base - 88 * s), (x + 2, base - 28 * s), (x + 40 * s, base - 28 * s)]), sail, border=1.2, shadow=SMALL)


def stilt_house(c, x0, x1, base, top, wall, roof):
    for x in range(int(x0) + 6, int(x1), 26):
        piece(c, RRect(x, base, x + 6, base + 60, 1), (110, 80, 60), shadow=SMALL)
    piece(c, RRect(x0, top, x1, base, 2), wall, border=1.5, shadow=PROP)
    for x in range(int(x0) + 8, int(x1), 14):
        flat(c, Thick(x, top + 4, x, base - 4, 1), lit(wall, 0.9))
    piece(c, Poly([(x0 - 10, top + 2), (x1 + 10, top + 2), ((x0 + x1) / 2, top - 40)]), roof, border=1.5, shadow=PROP)
    flat(c, RRect(x0 + 16, top + 16, x0 + 40, top + 40, 2), (250, 230, 160))


def l259_bg(c, d):
    sky(c, (140, 190, 236), (230, 236, 240), H)
    cloud_bg(c, 680, 50, 0.6)
    far_ridge(c, 160, 50, (150, 180, 160), 2591)
    far_round_trees(c, 190, 22, (100, 150, 100), 2592)
    # sea
    c.rect(0, 200, W, 470, (70, 140, 180))
    for k in range(10):
        flat(c, Thick(20 + k * 90, 230 + (k % 4) * 50, 70 + k * 90, 230 + (k % 4) * 50, 1.6), (120, 180, 210))
    # far sailboat (centre)
    boat(c, 450, 200, 0.7, (200, 80, 60), sail=(250, 246, 236) if "sail" not in d else (240, 180, 60))
    # stilt houses (left)
    stilt_house(c, 30, 180, 240, 160, (180, 140, 100), (200, 80, 70) if "roof" not in d else (60, 130, 190))
    stilt_house(c, 200, 320, 250, 180, (150, 170, 190), (90, 90, 110))
    # buoys + jetty (right)
    piece(c, RRect(600, 300, 910, 316, 2), (150, 110, 80), shadow=PROP)
    for x in range(610, 910, 40):
        piece(c, RRect(x, 316, x + 8, 380, 1), (120, 90, 64), shadow=SMALL)
    buoy = (240, 120, 40) if "buoy" not in d else (90, 200, 120)
    piece(c, [Circ(800, 250, 14), Thick(800, 236, 800, 216, 2)], buoy, border=1.2, shadow=SMALL)
    flat(c, Thick(786, 250, 814, 250, 4), (250, 250, 246))
    # boats in the harbour
    boat(c, 280, 380, 1.3, (60, 120, 200) if "hull" not in d else (220, 90, 70))
    boat(c, 740, 290, 1.0, (240, 200, 60))
    # drying nets on poles (right middle)
    for x in (560, 680):
        flat(c, Thick(x, 260, x, 390, 3), (120, 90, 64))
    net = (90, 140, 120) if "net" not in d else (200, 120, 60)
    flat(c, Poly([(560, 268), (680, 268), (670, 360), (570, 360)]), lit(net, 1.1))
    for k in range(0, 120, 12):
        flat(c, Thick(560 + k, 268, 570 + k * 0.85, 360, 1.2), net)
    for y in range(276, 360, 12):
        flat(c, Thick(562, y, 678, y, 1.2), net)
    # quay
    c.rect(0, 470, W, H, (190, 180, 160))
    for x in range(0, W, 60):
        flat(c, RRect(x + 2, 470, x + 58, 534, 2), (200, 190, 170))
        flat(c, RRect(x + 30, 536, x + 88, 600, 2), (200, 190, 170))
    # fish crates (left front)
    crate = (150, 110, 70) if "crate" not in d else (70, 130, 170)
    for k in range(2):
        piece(c, RRect(40 + k * 90, 520, 120 + k * 90, 560, 3), crate if k == 0 else (150, 110, 70), border=1.5, shadow=PROP)
        for j in range(4):
            piece(c, Ell(56 + k * 90 + j * 16, 516, 10, 5), (170, 180, 200), shadow=None)
    # fisherman with a hat (centre front)
    hx, hy = modern(c, 450, 590, (250, 200, 60), bottom=(60, 80, 120), hair=(130, 130, 140), h=2.2)
    hat = (250, 220, 60) if "hat" not in d else (220, 80, 80)
    piece(c, [Poly([(hx - 20, hy - 6), (hx + 20, hy - 6), (hx + 12, hy - 20), (hx - 12, hy - 20)])], hat, border=1, shadow=SMALL)
    flat(c, Thick(480, 520, 560, 420, 3), (120, 90, 64))
    # cat (right front)
    if "cat" not in d:
        piece(c, [Ell(790, 570, 26, 14), Circ(816, 552, 12), Poly([(808, 544), (810, 530), (816, 542)]), Poly([(818, 542), (824, 530), (826, 544)])], (240, 160, 70),
              border=1.2, shadow=SMALL)
        flat(c, [Circ(820, 552, 1.8)], INK)
    # rope coil + bollard
    c.ellipse_ring(660, 560, 30, 12, 6, (220, 200, 160))
    piece(c, [RRect(580, 540, 600, 580, 4), Ell(590, 538, 14, 5)], (60, 60, 70), shadow=SMALL)


L259_ELEMENTS = [
    bird_el("gull", 300, 80, s=10, speed=16),
    bird_el("gull2", 620, 120, s=9, speed=-18),
    E("bob", lambda c, m: boat(c, 600, 430, 0.8, (250, 250, 246), stripe=(220, 80, 70)), pivot=(600, 430), anim=dict(bobAmplitude=(0, 4), bobSpeed=0.5, swingAngle=3, swingSpeed=0.5)),
    E("tail", lambda c, m: flat(c, Thick(766, 568, 750, 548, 4), (240, 160, 70)), pivot=(766, 568), anim=dict(swingAngle=20, swingSpeed=1.2)),
]

L259_DIFFS = [
    ("roof", 105, 140, 0),
    ("sail", 470, 160, 0),
    ("buoy", 800, 244, 0),
    ("hull", 285, 360, 0),
    ("net", 620, 314, 0),
    ("crate", 80, 534, 0),
    ("hat", 451, 470, 0),
    ("cat", 806, 560, 0),
]


# =================================================================== Level 260 ice-cream parlour
SCOOPS = [(250, 200, 210), (250, 240, 200), (140, 90, 60), (170, 220, 170), (250, 180, 120), (200, 170, 230), (250, 250, 246), (240, 120, 130)]


def cone(c, x, base, s, scoops):
    piece(c, Poly([(x - 12 * s, base - 30 * s), (x + 12 * s, base - 30 * s), (x, base)]), (220, 170, 100), border=1.2, shadow=SMALL)
    flat(c, [Thick(x - 8 * s, base - 26 * s, x + 4 * s, base - 8 * s, 1), Thick(x + 8 * s, base - 26 * s, x - 4 * s, base - 8 * s, 1)], (190, 140, 80))
    for k, col in enumerate(scoops):
        piece(c, Circ(x, base - 38 * s - k * 16 * s, 13 * s), col, border=1, shadow=None)


def l260_bg(c, d):
    # pastel wall with stripes
    for k, x in enumerate(range(0, W, 50)):
        flat(c, RRect(x, 0, x + 50, 360, 0), (250, 226, 230) if k % 2 else (250, 240, 236))
    # menu board (left top)
    piece(c, RRect(30, 40, 250, 200, 4), (60, 70, 70), border=2, shadow=PROP)
    head = (250, 200, 210) if "menu" not in d else (170, 220, 170)
    flat(c, RRect(46, 54, 234, 82, 3), head)
    for k in range(4):
        flat(c, Circ(60, 104 + k * 24, 7), SCOOPS[k])
        flat(c, Thick(76, 104 + k * 24, 180, 104 + k * 24, 2), (230, 230, 220))
        flat(c, Thick(200, 104 + k * 24, 230, 104 + k * 24, 2), (250, 220, 120))
    # neon cone sign (centre top)
    neon = (240, 120, 180) if "neon" not in d else (90, 220, 230)
    soft_union(c, [Poly([(430, 140), (470, 140), (450, 190)]), Circ(450, 120, 22)], neon, 0.4, spread=14)
    flat(c, [Thick(430, 140, 450, 190, 4), Thick(470, 140, 450, 190, 4), Thick(430, 140, 470, 140, 4)], lit(neon, 1.25))
    c.ellipse_ring(450, 120, 22, 22, 4, lit(neon, 1.25))
    # pendant lamps
    for k, x in enumerate((640, 790)):
        flat(c, Thick(x, 0, x, 60, 2), (90, 90, 100))
        col = (250, 200, 60) if not (k == 1 and "lamp" in d) else (90, 170, 220)
        piece(c, Poly([(x - 30, 90), (x + 30, 90), (x + 14, 60), (x - 14, 60)]), col, border=1.2, shadow=SMALL)
    # cone display shelf (right)
    piece(c, RRect(560, 200, 880, 214, 2), (220, 190, 150), shadow=PROP)
    for k, x in enumerate(range(590, 880, 50)):
        sc = [SCOOPS[k % 8], SCOOPS[(k + 3) % 8]]
        if k == 1 and "scoop" in d:
            sc = [(90, 200, 220), SCOOPS[(k + 3) % 8]]
        cone(c, x, 200, 1.0, sc)
    # counter with glass case of tubs
    piece(c, RRect(0, 300, W, 330, 2), (250, 250, 246), border=1.5, shadow=PROP)
    piece(c, RRect(0, 330, W, 460, 0), (240, 150, 170), shadow=LAYER)
    flat(c, RRect(30, 340, 870, 400, 3), (220, 236, 244))
    for k, x in enumerate(range(50, 860, 100)):
        col = SCOOPS[k % 8]
        if k == 2 and "tub" in d:
            col = (120, 200, 220)
        flat(c, RRect(x, 350, x + 80, 396, 4), (250, 250, 250))
        flat(c, Ell(x + 40, 356, 36, 12), col)
        flat(c, RRect(x + 4, 356, x + 76, 390, 3), col)
    # floor
    c.rect(0, 460, W, H, (240, 236, 230))
    for x in range(0, W, 40):
        for y in range(460, H, 40):
            if (x // 40 + y // 40) % 2:
                flat(c, RRect(x, y, x + 40, y + 40, 0), (60, 60, 70))
    # stools (left front)
    for k, x in enumerate((90, 200)):
        col = (240, 120, 160) if not (k == 0 and "stool" in d) else (90, 170, 220)
        piece(c, [Ell(x, 500, 34, 10), RRect(x - 5, 500, x + 5, 580, 2), Ell(x, 584, 26, 6)], col, shadow=PROP)
    # customer with a cone (centre)
    hx, hy = modern(c, 450, 600, (90, 160, 220), bottom=(60, 70, 100), hair=(200, 150, 80), h=2.2, style="twin")
    cone(c, 486, 520, 1.1, [(250, 200, 210) if "cone" not in d else (140, 90, 60), (250, 240, 200)])
    # sundae glass on a small table (right front)
    piece(c, [Ell(790, 520, 60, 12), RRect(784, 520, 796, 590, 2)], (250, 250, 246), shadow=PROP)
    sundae = (240, 120, 130) if "sundae" not in d else (170, 220, 170)
    piece(c, [Poly([(770, 510), (810, 510), (800, 470), (780, 470)]), Circ(790, 462, 18)], sundae, border=1.2, shadow=SMALL)
    flat(c, Circ(790, 442, 6), (200, 30, 50))


L260_ELEMENTS = [
    E("glow", lambda c, m: soft_union(c, [Circ(450, 140, 40)], (255, 220, 240), 0.2, spread=30), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=1.0)),
    E("drip", lambda c, m: piece(c, Ell(474, 470, 3, 5), (250, 200, 210), shadow=None), pivot=(474, 470), anim=dict(driftVelocity=(0, 30), driftLength=40, driftFade=True)),
    E("cashier", lambda c, m: modern(c, 330, 300, (250, 250, 246), bottom=(60, 70, 100), hair=(40, 30, 30), h=1.6), pivot=(330, 300),
      anim=dict(bobAmplitude=(20, 0), bobSpeed=0.12)),
]

L260_DIFFS = [
    ("menu", 140, 68, 0),
    ("neon", 450, 150, 0),
    ("lamp", 790, 76, 0),
    ("tub", 290, 372, 0),
    ("scoop", 640, 162, 0),
    ("stool", 90, 540, 0),
    ("cone", 486, 470, 0),
    ("sundae", 790, 480, 0),
]


# =================================================================== Level 261 flower shop
def bucket_flowers(c, x, base, s, bucket, bloom, kind="round"):
    piece(c, Poly([(x - 24 * s, base - 40 * s), (x + 24 * s, base - 40 * s), (x + 18 * s, base), (x - 18 * s, base)]), bucket, border=1.2, shadow=PROP)
    rnd = random.Random(int(x * 3 + base))
    for _ in range(7):
        fx, fy = x + rnd.uniform(-22, 22) * s, base - 40 * s - rnd.uniform(14, 46) * s
        flat(c, Thick(x + (fx - x) * 0.3, base - 40 * s, fx, fy, 1.4), (80, 140, 70))
        if kind == "round":
            piece(c, Circ(fx, fy, 8 * s), bloom, shadow=None)
            flat(c, Circ(fx, fy, 3 * s), lit(bloom, 0.8))
        else:
            piece(c, Poly([(fx - 6 * s, fy), (fx + 6 * s, fy), (fx + 4 * s, fy - 14 * s), (fx, fy - 8 * s), (fx - 4 * s, fy - 14 * s)]), bloom, shadow=None)


def l261_bg(c, d):
    c.rect(0, 0, W, 420, (220, 236, 220))
    planks(c, 420, (190, 150, 110), (170, 130, 94), seed=2611)
    # shop window with street view (right)
    piece(c, RRect(560, 40, 880, 260, 3), (250, 250, 246), border=1.5, shadow=PROP)
    flat(c, RRect(574, 54, 866, 246, 2), (190, 220, 240))
    flat(c, RRect(574, 180, 866, 246, 0), (200, 196, 190))
    for x in (620, 700, 780):
        flat(c, RRect(x, 110, x + 60, 180, 2), (230, 200, 170))
    flat(c, Thick(720, 54, 720, 246, 4), (250, 250, 246))
    box = (200, 80, 90) if "box" not in d else (90, 150, 220)
    piece(c, RRect(580, 260, 860, 286, 3), box, border=1.2, shadow=PROP)
    for k in range(10):
        flat(c, Circ(596 + k * 28, 254, 8), [(250, 200, 60), (250, 250, 246), (240, 120, 160)][k % 3])
    # wall clock / sign (centre top)
    sign = (90, 140, 100) if "sign" not in d else (200, 120, 60)
    piece(c, RRect(330, 30, 530, 90, 8), sign, border=1.5, shadow=PROP)
    sign_box(c, 350, 44, 510, 76, sign, 2612, vertical=False)
    # hanging pots (left top)
    for k, x in enumerate((90, 210)):
        flat(c, Thick(x, 0, x, 70, 1.4), (90, 80, 70))
        pot = (220, 130, 90) if not (k == 0 and "pot" in d) else (90, 150, 210)
        piece(c, Poly([(x - 24, 70), (x + 24, 70), (x + 18, 100), (x - 18, 100)]), pot, border=1.2, shadow=SMALL)
        for j in range(5):
            piece(c, Ell(x - 24 + j * 12, 112 + (j % 2) * 16, 6, 16), (80, 150, 80), shadow=None)
    # shelf of small pots (left middle)
    piece(c, RRect(20, 230, 300, 244, 2), (190, 150, 110), shadow=PROP)
    for k, x in enumerate(range(40, 300, 50)):
        piece(c, Poly([(x - 14, 206), (x + 14, 206), (x + 10, 230), (x - 10, 230)]), (240, 240, 236), border=1, shadow=None)
        flat(c, [Circ(x - 6, 198, 9), Circ(x + 6, 196, 9), Circ(x, 188, 9)], (80, 150, 80))
    # buckets of flowers along the floor
    bucket_flowers(c, 280, 420, 1.6, (150, 160, 176), (240, 90, 120) if "bucket" not in d else (250, 210, 60))
    bucket_flowers(c, 380, 430, 1.3, (150, 160, 176), (250, 250, 246), kind="tulip")
    bucket_flowers(c, 160, 440, 1.4, (150, 160, 176), (200, 140, 230), kind="tulip")
    # counter + florist wrapping a bouquet (right middle)
    piece(c, RRect(520, 380, 900, 470, 3), (200, 160, 120), border=1.5, shadow=PROP)
    flat(c, RRect(520, 380, 900, 392, 2), (170, 130, 94))
    hx, hy = modern(c, 700, 380, (250, 246, 236), bottom=(60, 70, 100), hair=(90, 60, 40), h=1.8, style="long")
    wrap = (250, 200, 210) if "wrap" not in d else (150, 210, 230)
    piece(c, Poly([(600, 380), (660, 380), (680, 320), (580, 320)]), wrap, border=1.2, shadow=SMALL)
    flat(c, [Circ(600 + k * 14, 316 - (k % 2) * 8, 9) for k in range(6)], (240, 90, 120))
    # register (counter right)
    piece(c, [RRect(800, 340, 870, 380, 3), RRect(810, 320, 860, 344, 2)], (90, 90, 100), shadow=SMALL)
    # ribbon rolls (centre front)
    for k, x in enumerate((420, 470, 520)):
        col = [(240, 90, 120), (250, 200, 60), (90, 160, 220)][k]
        if k == 1 and "ribbon" in d:
            col = (120, 200, 120)
        piece(c, Ell(x, 540, 20, 20), col, border=1.2, shadow=SMALL)
        flat(c, Circ(x, 540, 6), lit(col, 0.7))
    # watering can (left front)
    can = (90, 170, 160) if "can" not in d else (240, 140, 60)
    piece(c, [RRect(50, 520, 130, 580, 8), Thick(130, 540, 174, 510, 6), Thick(60, 520, 100, 500, 4)], can, border=1.5, shadow=PROP)
    # cat sleeping on a cushion (right front)
    piece(c, Ell(790, 570, 60, 14), (200, 80, 90), shadow=PROP)
    if "cat" not in d:
        piece(c, [Ell(790, 552, 36, 16), Circ(820, 546, 12), Poly([(812, 538), (814, 526), (820, 536)]), Poly([(822, 536), (828, 526), (830, 538)])], (130, 130, 140),
              border=1.2, shadow=SMALL)


L261_ELEMENTS = [
    E("petal", lambda c, m: piece(c, Ell(300, 300, 5, 3), (240, 90, 120), shadow=None), pivot=(300, 300),
      anim=dict(driftVelocity=(10, 30), driftLength=100, driftFade=True, swingAngle=40, swingSpeed=1.0)),
    E("leaf", lambda c, m: piece(c, Ell(210, 130, 6, 16), (80, 150, 80), shadow=None), pivot=(210, 112), anim=dict(swingAngle=10, swingSpeed=0.6)),
    E("walker", lambda c, m: modern(c, 650, 230, (220, 80, 80), bottom=(60, 70, 100), hair=(40, 30, 30), h=1.0), pivot=(650, 230), anim=drift_across(570, 870, 18)),
]

L261_DIFFS = [
    ("pot", 90, 86, 0),
    ("sign", 430, 60, 0),
    ("box", 720, 270, 0),
    ("bucket", 280, 340, 0),
    ("wrap", 630, 340, 0),
    ("can", 100, 545, 0),
    ("ribbon", 470, 540, 0),
    ("cat", 800, 548, 0),
]


# =================================================================== Level 262 observatory at night
NE = (110, 100, 130)


def l262_bg(c, d):
    c.gradient(0, H, (16, 20, 50), (50, 50, 100))
    rnd = random.Random(2621)
    for _ in range(160):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 420), rnd.choice((0.8, 1.2, 1.8))), (240, 240, 255))
    soft_union(c, [Poly([(0, 300), (300, 80), (500, 0), (600, 0), (380, 120), (0, 360)])], (120, 110, 200), 0.18, spread=40)
    # moon (left)
    moon = (250, 240, 200) if "moon" not in d else (250, 180, 140)
    npiece(c, Circ(120, 90, 36), moon, shadow=None)
    soft_union(c, [Circ(120, 90, 36)], (255, 250, 220), 0.3, spread=30)
    flat(c, [Circ(110, 80, 7), Circ(132, 102, 5)], lit(moon, 0.9))
    # bright constellation (centre top)
    star = (255, 240, 180) if "star" not in d else (150, 220, 255)
    pts = [(400, 60), (440, 40), (480, 70), (520, 50), (470, 110)]
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 1), (180, 180, 220))
    for x, y in pts:
        flat(c, Poly(star_pts(x, y, 9, 3, points=4, rot=0)), star)
    # ringed planet (right)
    planet = (230, 190, 130) if "planet" not in d else (140, 200, 160)
    npiece(c, Circ(790, 110, 24), planet, shadow=None)
    c.ellipse_ring(790, 110, 42, 10, 3, (240, 220, 190))
    # hills
    piece(c, hill_strip(400, [(20, 0.008, 0.4), (10, 0.03, 1.2)]), (30, 40, 70), border=1.5, border_col=NE, shadow=LAYER)
    # observatory building with dome (left middle)
    npiece(c, RRect(160, 300, 400, 460, 2), (200, 200, 216))
    dome = Poly([(280 + 120 * math.cos(math.pi * k / 16), 300 - 110 * math.sin(math.pi * k / 16)) for k in range(17)])
    npiece(c, dome, (220, 224, 236))
    flat(c, Poly([(266, 190), (300, 190), (300, 300), (266, 300)]), (20, 24, 50))
    for k in range(1, 4):
        flat(c, Thick(160 + 30 * k, 300 - 30 * k * 0.9, 160 + 30 * k, 300, 1.2), (190, 196, 210))
    flag = (220, 70, 70) if "flag" not in d else (250, 200, 60)
    flat(c, Thick(380, 300, 380, 250, 2), (200, 200, 210))
    npiece(c, Poly([(382, 250), (414, 258), (382, 268)]), flag, shadow=None)
    flat(c, [RRect(200, 340, 230, 380, 2), RRect(330, 340, 360, 380, 2)], (250, 220, 130))
    npiece(c, RRect(260, 390, 300, 460, 2), (90, 70, 70))
    # big telescope peeking out
    npiece(c, [Thick(284, 250, 340, 150, 18)], (90, 96, 120))
    # ground platform
    c.rect(0, 460, W, H, (40, 46, 70))
    for x in range(0, W, 60):
        flat(c, Thick(x, 460, x - 30, 600, 1), (50, 56, 82))
    # small telescope on a tripod (right middle)
    tel = (240, 240, 246) if "scope" not in d else (220, 120, 60)
    npiece(c, [Thick(600, 440, 660, 330, 14)], tel)
    flat(c, [Thick(620, 400, 590, 460, 3), Thick(620, 400, 650, 460, 3), Thick(620, 400, 620, 460, 3)], (160, 160, 180))
    hx, hy = modern(c, 700, 460, (90, 110, 170), bottom=(50, 50, 70), hair=(40, 30, 30), h=1.9)
    # star chart board (left front)
    npiece(c, [RRect(40, 470, 220, 580, 3), Thick(80, 580, 70, 600, 3), Thick(180, 580, 190, 600, 3)], (240, 236, 220))
    chart = (40, 50, 100) if "chart" not in d else (100, 40, 90)
    flat(c, RRect(50, 480, 210, 570, 2), chart)
    for x, y in ((80, 500), (120, 520), (150, 500), (180, 540), (100, 550)):
        flat(c, Circ(x, y, 3), (250, 240, 180))
    flat(c, [Thick(80, 500, 120, 520, 1), Thick(120, 520, 150, 500, 1), Thick(120, 520, 180, 540, 1)], (200, 200, 230))
    # laptop on a folding table (centre front)
    npiece(c, [RRect(380, 520, 520, 532, 2), Thick(392, 532, 380, 600, 3), Thick(508, 532, 520, 600, 3)], (150, 120, 90))
    npiece(c, [Poly([(410, 520), (490, 520), (484, 470), (416, 470)])], (60, 60, 70))
    scr = (120, 180, 240) if "laptop" not in d else (240, 140, 200)
    flat(c, Poly([(420, 514), (480, 514), (476, 476), (424, 476)]), scr)
    # thermos + mug (right front)
    therm = (220, 80, 70) if "thermos" not in d else (90, 170, 120)
    npiece(c, [RRect(780, 500, 810, 580, 6), RRect(784, 490, 806, 502, 2)], therm)
    npiece(c, [RRect(830, 540, 860, 580, 4)], (240, 240, 236))
    modern(c, 500, 600, (60, 70, 90), bottom=(40, 40, 50), hair=(200, 150, 80), h=2.0, style="long")


L262_ELEMENTS = [
    E("meteor", lambda c, m: [soft_union(c, [Poly([(620, 40), (700, 20), (624, 46)])], (230, 240, 255), 0.6, spread=6), flat(c, Circ(620, 44, 3), (255, 255, 255))],
      pivot=(620, 44), daynight="untinted", anim=dict(driftVelocity=(-120, 40), driftLength=200, driftFade=True)),
    E("twinkle", lambda c, m: [flat(c, Poly(star_pts(x, y, 8, 2, points=4, rot=0)), (255, 255, 255)) for x, y in ((40, 200), (600, 160), (860, 260), (300, 30))],
      daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
    E("steam", lambda c, m: piece(c, Circ(845, 530, 6), (220, 220, 240), shadow=None), pivot=(845, 530),
      anim=dict(driftVelocity=(2, -16), driftLength=40, driftFade=True, driftGrow=1.4)),
    E("glow", lambda c, m: soft_union(c, [Poly([(420, 514), (480, 514), (476, 476), (424, 476)])], (150, 200, 255), 0.3, spread=16), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=0.8)),
]

L262_DIFFS = [
    ("moon", 120, 90, 0),
    ("star", 460, 70, 0),
    ("planet", 790, 110, 0),
    ("flag", 398, 260, 0),
    ("scope", 630, 384, 0),
    ("chart", 130, 525, 0),
    ("laptop", 450, 495, 0),
    ("thermos", 795, 540, 0),
]


# =================================================================== Level 263 music classroom
def note(c, x, y, s, col):
    flat(c, Ell(x, y, 8 * s, 6 * s), col)
    flat(c, Thick(x + 7 * s, y, x + 7 * s, y - 30 * s, 2.4 * s), col)
    flat(c, Thick(x + 7 * s, y - 30 * s, x + 16 * s, y - 22 * s, 2.4 * s), col)


def guitar(c, x, y, s, body):
    piece(c, [Ell(x, y + 30 * s, 22 * s, 24 * s), Ell(x, y - 2 * s, 16 * s, 18 * s), RRect(x - 4 * s, y - 80 * s, x + 4 * s, y, 1), RRect(x - 7 * s, y - 96 * s, x + 7 * s, y - 80 * s, 2)],
          body, border=1.5, shadow=PROP)
    flat(c, Circ(x, y + 10 * s, 7 * s), (60, 40, 30))
    flat(c, RRect(x - 4 * s, y - 80 * s, x + 4 * s, y + 4 * s, 1), (80, 60, 40))


def l263_bg(c, d):
    c.rect(0, 0, W, 420, (236, 230, 210))
    # chalkboard with staff lines and notes (left)
    piece(c, RRect(20, 40, 300, 200, 4), (150, 110, 70), border=1.5, shadow=PROP)
    flat(c, RRect(32, 52, 288, 188, 3), (50, 80, 70))
    for k in range(5):
        flat(c, Thick(44, 90 + k * 12, 276, 90 + k * 12, 1.4), (220, 230, 220))
    for k, x in enumerate((70, 120, 170, 220, 260)):
        col = (240, 240, 230) if not (k == 1 and "note" in d) else (250, 200, 60)
        note(c, x, 126 - (k % 3) * 12, 1.2, col)
    # poster (centre top)
    poster = (240, 120, 90) if "poster" not in d else (90, 160, 220)
    piece(c, RRect(380, 40, 520, 180, 2), poster, border=1.5, shadow=PROP)
    piece(c, [Circ(450, 100, 30)], (250, 240, 200), shadow=None)
    note(c, 444, 112, 1.4, (60, 50, 60))
    # wall clock (right top)
    clock = (250, 250, 246) if "clock" not in d else (250, 220, 120)
    piece(c, Circ(790, 90, 40), (120, 90, 70), border=1.5, shadow=PROP)
    flat(c, Circ(790, 90, 32), clock)
    flat(c, [Thick(790, 90, 790, 66, 3), Thick(790, 90, 808, 98, 3)], (40, 40, 50))
    # guitars on the wall (right)
    guitar(c, 640, 250, 1.0, (210, 140, 70))
    guitar(c, 720, 260, 1.0, (180, 60, 60))
    # floor
    c.rect(0, 420, W, H, (190, 150, 110))
    for y in range(420, H, 22):
        flat(c, Thick(0, y, W, y, 1.2), (174, 136, 98))
    # piano (left)
    piece(c, RRect(20, 260, 260, 470, 4), (40, 36, 40), border=1.5, shadow=PROP)
    flat(c, RRect(30, 380, 250, 404, 2), (250, 250, 246))
    for k in range(16):
        flat(c, Thick(30 + k * 14, 380, 30 + k * 14, 404, 1), (180, 180, 180))
        if k % 7 not in (2, 6):
            flat(c, RRect(38 + k * 14, 380, 46 + k * 14, 394, 1), (30, 30, 34))
    piece(c, RRect(60, 280, 220, 340, 2), (230, 220, 190), shadow=SMALL)
    for k in range(4):
        flat(c, Thick(70, 296 + k * 12, 210, 296 + k * 12, 1), (150, 140, 120))
    # piano bench
    bench = (40, 36, 40) if "bench" not in d else (180, 60, 60)
    piece(c, [RRect(80, 500, 220, 520, 3), RRect(90, 520, 100, 580, 1), RRect(200, 520, 210, 580, 1)], bench, shadow=PROP)
    # drum kit (centre)
    drum = (200, 50, 60) if "drum" not in d else (60, 120, 210)
    piece(c, [Ell(400, 420, 50, 44)], drum, border=1.5, shadow=PROP)
    flat(c, Ell(400, 420, 30, 28), (250, 246, 236))
    for x, y, r in ((330, 360, 22), (470, 360, 22)):
        piece(c, Ell(x, y, r, 14), drum, border=1.2, shadow=SMALL)
        flat(c, Ell(x, y - 6, r, 6), (250, 246, 236))
    for x in (300, 520):
        flat(c, Thick(x, 470, x, 300, 2), (190, 190, 200))
        piece(c, Ell(x, 300, 30, 6), (230, 190, 70), shadow=SMALL)
    # xylophone (right middle)
    piece(c, [Poly([(560, 420), (760, 410), (760, 430), (560, 446)])], (130, 90, 60), shadow=PROP)
    for k in range(8):
        col = [(240, 90, 90), (250, 160, 60), (250, 220, 70), (120, 200, 100), (90, 180, 220), (100, 120, 220), (170, 110, 220), (240, 120, 180)][k]
        if k == 3 and "xylo" in d:
            col = (250, 250, 246)
        piece(c, RRect(568 + k * 24, 380 + k * 2, 588 + k * 24, 430 - k, 2), col, shadow=None)
    # kids
    modern(c, 140, 500, (90, 160, 220), bottom=(60, 70, 100), hair=(40, 30, 30), h=1.6)
    modern(c, 680, 560, (240, 200, 60), bottom=(60, 70, 100), hair=(200, 150, 80), h=2.0, style="twin")
    # trumpet case + music stand (right front)
    case = (60, 60, 70) if "case" not in d else (200, 120, 60)
    piece(c, [RRect(760, 540, 880, 590, 10)], case, border=1.5, shadow=PROP)
    flat(c, RRect(810, 530, 830, 542, 2), (200, 200, 210))
    flat(c, [Thick(520, 600, 520, 500, 3)], (60, 60, 70))
    piece(c, Poly([(480, 500), (560, 500), (556, 460), (484, 460)]), (60, 60, 70), shadow=SMALL)
    flat(c, RRect(490, 466, 550, 496, 1), (250, 250, 246))


L263_ELEMENTS = [
    E("note1", lambda c, m: note(c, 360, 280, 1.4, (60, 50, 60)), pivot=(360, 280), anim=dict(driftVelocity=(10, -30), driftLength=80, driftFade=True)),
    E("note2", lambda c, m: note(c, 200, 240, 1.2, (60, 50, 60)), pivot=(200, 240), anim=dict(driftVelocity=(-8, -30), driftLength=70, driftFade=True, phase=0.5)),
    E("stick", lambda c, m: flat(c, Thick(440, 330, 470, 300, 3), (220, 190, 140)), pivot=(440, 330), anim=dict(swingAngle=20, swingSpeed=1.4)),
    E("pendulum", lambda c, m: flat(c, Thick(80, 250, 80, 210, 2), (200, 160, 60)), pivot=(80, 250), anim=dict(swingAngle=20, swingSpeed=0.8)),
]

L263_DIFFS = [
    ("note", 124, 110, 0),
    ("poster", 450, 110, 0),
    ("clock", 790, 90, 0),
    ("drum", 400, 400, 0),
    ("xylo", 652, 412, 0),
    ("bench", 150, 520, 0),
    ("case", 820, 565, 0),
]


# =================================================================== Level 264 snowy night cabin
def l264_bg(c, d):
    c.gradient(0, H, (20, 30, 70), (70, 80, 130))
    stars_bg(c, 2641, 90, 300)
    moon = (250, 246, 220) if "moon" not in d else (250, 200, 150)
    npiece(c, Circ(130, 90, 34), moon, shadow=None)
    soft_union(c, [Circ(130, 90, 34)], (255, 250, 230), 0.3, spread=30)
    big = (255, 250, 210) if "star" not in d else (160, 220, 255)
    flat(c, Poly(star_pts(450, 70, 16, 5, points=4, rot=0)), big)
    soft_union(c, [Circ(450, 70, 6)], big, 0.4, spread=14)
    # snowy hills + far pines
    piece(c, hill_strip(280, [(20, 0.008, 0.4), (10, 0.03, 1.0)]), (170, 180, 210), border=1.5, border_col=(110, 110, 140), shadow=LAYER)
    for x in range(-20, W + 20, 40):
        tree_pine(c, x, 300 + (x % 3) * 6, h=60 + (x % 5) * 6, col=(40, 70, 70), snow=(220, 230, 246))
    c.rect(0, 330, W, H, (220, 228, 244))
    piece(c, hill_strip(330, [(8, 0.02, 0.4), (5, 0.05, 1.2)]), (226, 232, 246), border=1.5, border_col=(170, 176, 200), shadow=LAYER)
    # cabin (right)
    npiece(c, RRect(560, 250, 860, 420, 2), (120, 80, 60))
    for y in range(262, 420, 16):
        flat(c, Thick(560, y, 860, y, 2), (100, 66, 50))
    npiece(c, Poly([(540, 254), (880, 254), (710, 160)]), (90, 60, 50))
    flat(c, Poly([(540, 254), (880, 254), (710, 160), (710, 176), (566, 250)]), (236, 240, 250))
    chim = (150, 90, 80) if "chimney" not in d else (90, 100, 130)
    npiece(c, RRect(790, 150, 830, 230, 2), chim)
    flat(c, RRect(786, 146, 834, 156, 2), (236, 240, 250))
    win = (250, 210, 110) if "window" not in d else (150, 210, 250)
    for x in (590, 760):
        flat(c, RRect(x, 290, x + 70, 350, 3), win)
        flat(c, [Thick(x + 35, 290, x + 35, 350, 3), Thick(x, 320, x + 70, 320, 3)], (90, 60, 50))
    npiece(c, RRect(680, 320, 740, 420, 3), (70, 50, 40))
    flat(c, Circ(730, 370, 3), (240, 200, 90))
    # snowman (left middle)
    piece(c, [Circ(260, 440, 40), Circ(260, 380, 30), Circ(260, 334, 22)], (246, 248, 252), border=1.5, border_col=(170, 176, 200), shadow=PROP)
    scarf = (220, 60, 70) if "scarf" not in d else (90, 170, 120)
    flat(c, [RRect(238, 350, 282, 360, 3), RRect(268, 356, 280, 386, 3)], scarf)
    flat(c, [Circ(252, 330, 2.6), Circ(268, 330, 2.6), Circ(260, 376, 3), Circ(260, 392, 3)], INK)
    flat(c, Poly([(262, 336), (284, 340), (262, 342)]), (250, 140, 40))
    npiece(c, [RRect(244, 296, 276, 316, 2), RRect(236, 314, 284, 318, 1)], (40, 40, 50))
    flat(c, [Thick(232, 380, 196, 360, 3), Thick(288, 380, 320, 356, 3)], (110, 80, 60))
    # sled (left front)
    sled = (200, 60, 60) if "sled" not in d else (60, 120, 200)
    npiece(c, [RRect(60, 520, 200, 536, 4), Thick(60, 552, 216, 552, 3), Thick(80, 536, 80, 552, 3), Thick(180, 536, 180, 552, 3), Thick(200, 552, 220, 540, 3)], sled)
    # lantern on a post (centre front)
    flat(c, Thick(450, 600, 450, 480, 4), (60, 50, 50))
    lan = (250, 200, 90) if "lantern" not in d else (120, 220, 240)
    npiece(c, [RRect(434, 486, 466, 520, 4), Poly([(430, 488), (470, 488), (450, 472)])], (40, 40, 50))
    flat(c, RRect(440, 492, 460, 516, 2), lan)
    # deer (right front)
    if "deer" not in d:
        npiece(c, [Ell(790, 530, 36, 16), Ell(824, 504, 10, 12), Poly([(812, 518), (828, 490), (836, 500), (824, 526)]), RRect(764, 536, 770, 580, 1), RRect(780, 538, 786, 580, 1),
                   RRect(800, 538, 806, 580, 1), RRect(814, 536, 820, 580, 1)], (170, 120, 80), shadow=PROP)
        flat(c, [Thick(828, 494, 840, 470, 2), Thick(834, 482, 846, 476, 2), Thick(822, 494, 814, 470, 2)], (120, 90, 60))
        flat(c, Circ(828, 502, 1.8), INK)
    # footprints
    for k in range(6):
        flat(c, Ell(330 + k * 40, 560 - (k % 2) * 10, 7, 4), (196, 204, 226))


L264_ELEMENTS = smoke_el("smk", 810, 140, n=3, col=(200, 200, 220), r=12, rise=(10, -26), length=80) + [
    E("snow1", lambda c, m: [flat(c, Circ(x, y, 2.6), (250, 252, 255)) for x, y in ((60, 120), (240, 60), (380, 200), (520, 140), (660, 40), (880, 220), (320, 300), (720, 460))],
      daynight="untinted", anim=dict(driftVelocity=(-6, 40), driftLength=120, driftFade=True)),
    E("snow2", lambda c, m: [flat(c, Circ(x, y, 2), (250, 252, 255)) for x, y in ((140, 220), (300, 140), (460, 300), (600, 220), (780, 100), (860, 400), (200, 460))],
      daynight="untinted", anim=dict(driftVelocity=(8, 36), driftLength=120, driftFade=True, phase=0.5)),
    E("glow", lambda c, m: soft_union(c, [RRect(590, 290, 660, 350, 3), RRect(760, 290, 830, 350, 3), RRect(440, 492, 460, 516, 2)], (255, 210, 120), 0.3, spread=20),
      daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.8)),
]

L264_DIFFS = [
    ("moon", 130, 90, 0),
    ("star", 450, 70, 0),
    ("chimney", 810, 190, 0),
    ("scarf", 266, 365, 0),
    ("window", 625, 320, 0),
    ("sled", 140, 536, 0),
    ("lantern", 450, 504, 0),
    ("deer", 800, 530, 0),
]


LEVELS = [
    ("Level255", "古希腊神庙", l255_bg, L255_ELEMENTS, L255_DIFFS, 60, OPTS),
    ("Level256", "丛林遗迹", l256_bg, L256_ELEMENTS, L256_DIFFS, 60, OPTS),
    ("Level257", "葡萄园", l257_bg, L257_ELEMENTS, L257_DIFFS, 60, OPTS),
    ("Level258", "奶牛牧场", l258_bg, L258_ELEMENTS, L258_DIFFS, 60, OPTS),
    ("Level259", "渔村", l259_bg, L259_ELEMENTS, L259_DIFFS, 60, OPTS),
    ("Level260", "冰淇淋店", l260_bg, L260_ELEMENTS, L260_DIFFS, 60, OPTS),
    ("Level261", "花店", l261_bg, L261_ELEMENTS, L261_DIFFS, 60, OPTS),
    ("Level262", "天文台", l262_bg, L262_ELEMENTS, L262_DIFFS, 60, OPTS),
    ("Level263", "音乐教室", l263_bg, L263_ELEMENTS, L263_DIFFS, 60, OPTS),
    ("Level264", "雪夜小木屋", l264_bg, L264_ELEMENTS, L264_DIFFS, 60, OPTS),
]
