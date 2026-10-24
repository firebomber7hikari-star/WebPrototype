# -*- coding: utf-8 -*-
"""Mixed themes part 8 (paper-craft side views of town and country, full-bleed, original designs, no brands):
  Level305 风筝节     - a kite festival on a grassy hill: kites of many shapes, families, picnic blankets
  Level306 江南水乡   - a canal water town: white walls and dark roofs, stone arch bridge, boats, lanterns
  Level307 麦田收割   - a wheat harvest: combine harvester, hay bales, farm truck, scarecrow, crows
  Level308 樱花河畔   - cherry blossoms along a river: rowing boats, picnic, lanterns, footbridge
  Level309 冰雪节     - a snow festival: ice castle, ice sculptures, skaters, food stall, lanterns
  Level310 南瓜农场   - a pumpkin patch: pumpkins, hay maze, red barn, tractor wagon, apple stand
  Level311 湿地观鸟   - a wetland: flamingos, storks, reeds, a bird hide, birdwatchers, a boardwalk
  Level312 渔港鱼市   - a harbour fish market: crates of fish on ice, scales, gulls, fishmongers, boats
  Level313 水车磨坊   - a watermill by a stream: wheel, millstones, sacks of flour, ducks, miller
  Level314 山间铁路   - a steam train crossing a stone viaduct in the mountains
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, fish, layer, rock, sky, smoke_el, sun_bg, tree_pine,
                 tree_round)
from fills import far_forest, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_festival import npiece
from levels_homes import steam
from levels_mix1 import lantern
from levels_mix2 import wheel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def blanket(c, x0, y0, x1, y1, a, b):
    piece(c, Poly([(x0, y0), (x1, y0 - 4), (x1 + 10, y1), (x0 - 10, y1 + 4)]), a, border=1.2, shadow=SMALL)
    for k in range(1, 4):
        t = k / 4
        flat(c, Thick(x0 + (x1 - x0) * t, y0 - 4 * t, x0 - 10 + (x1 + 20 - x0) * t, y1 + 4 - 4 * t, 4), b)


# =================================================================== Level 305 kite festival
def kite(c, x, y, s, a, b, kind="diamond"):
    if kind == "diamond":
        piece(c, Poly([(x, y - 30 * s), (x + 22 * s, y), (x, y + 34 * s), (x - 22 * s, y)]), a, border=1.2, shadow=SMALL)
        flat(c, Poly([(x, y - 30 * s), (x + 22 * s, y), (x, y)]), b)
        flat(c, Poly([(x, y + 34 * s), (x - 22 * s, y), (x, y)]), b)
    elif kind == "box":
        piece(c, [RRect(x - 16 * s, y - 30 * s, x + 16 * s, y - 8 * s, 2), RRect(x - 16 * s, y + 8 * s, x + 16 * s, y + 30 * s, 2)], a, border=1.2, shadow=SMALL)
        flat(c, [Thick(x - 16 * s, y - 30 * s, x - 16 * s, y + 30 * s, 2), Thick(x + 16 * s, y - 30 * s, x + 16 * s, y + 30 * s, 2)], b)
    else:  # fish kite
        piece(c, [Ell(x, y, 34 * s, 14 * s), Poly([(x - 30 * s, y), (x - 52 * s, y - 14 * s), (x - 52 * s, y + 14 * s)])], a, border=1.2, shadow=SMALL)
        flat(c, [Thick(x - 10 * s, y - 12 * s, x - 10 * s, y + 12 * s, 3), Thick(x + 6 * s, y - 13 * s, x + 6 * s, y + 13 * s, 3)], b)
        flat(c, Circ(x + 22 * s, y - 3 * s, 3 * s), INK)


def l305_bg(c, d):
    sky(c, (100, 176, 240), (220, 236, 250), H)
    cloud_bg(c, 760, 70, 0.6)
    cloud_bg(c, 140, 200, 0.5)
    # static kites high up (strings run to the flyers)
    kite(c, 150, 90, 1.3, (240, 90, 80) if "kite1" not in d else (90, 170, 230), (250, 210, 70))
    kite(c, 470, 70, 1.2, (90, 160, 90), (250, 250, 246), kind="box")
    kite(c, 700, 170, 1.1, (250, 160, 60) if "fishkite" not in d else (200, 110, 200), (220, 60, 50), kind="fish")
    for (kx, ky), (hx, hy) in (((150, 124), (230, 430)), ((470, 100), (430, 420)), ((650, 174), (720, 470))):
        flat(c, Thick(kx, ky, hx, hy, 1), (90, 90, 100))
    # hills
    far_round_trees(c, 260, 22, (100, 160, 100), 3051)
    layer(c, 280, [(20, 0.006, 0.2), (8, 0.03, 1.0)], (120, 186, 90))
    c.rect(0, 360, W, H, (124, 190, 94))
    layer(c, 350, [(10, 0.01, 1.2), (5, 0.04, 0.4)], (130, 196, 100))
    # flag tent (right)
    tent = (250, 250, 246) if "tent" not in d else (250, 210, 90)
    piece(c, Poly([(760, 330), (880, 330), (860, 270), (780, 270)]), tent, border=1.5, shadow=PROP)
    piece(c, Poly([(770, 272), (870, 272), (820, 236)]), (220, 70, 70), border=1.5, shadow=PROP)
    flat(c, Thick(820, 236, 820, 210, 2), (90, 80, 70))
    piece(c, Poly([(820, 210), (846, 218), (820, 226)]), (250, 210, 70), border=1, shadow=None)
    # flyers
    hx, hy = modern(c, 230, 440, (220, 80, 80), bottom=(60, 70, 100), hair=(40, 30, 30), h=1.9)
    modern(c, 430, 430, (240, 200, 60), bottom=(60, 70, 100), hair=(200, 160, 90), h=1.8, style="twin")
    hx, hy = modern(c, 720, 480, (90, 130, 200) if "flyer" not in d else (90, 190, 120), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.0)
    # picnic blankets
    blanket(c, 60, 520, 260, 560, (230, 80, 80) if "blanket" not in d else (90, 140, 220), (250, 250, 246))
    piece(c, Poly([(130, 516), (190, 516), (184, 494), (136, 494)]), (190, 140, 80), border=1.2, shadow=SMALL)
    blanket(c, 480, 540, 640, 576, (250, 200, 70), (240, 140, 60))
    # kite in the grass (centre front)
    kite(c, 370, 560, 1.0, (90, 200, 220) if "groundkite" not in d else (240, 120, 160), (250, 250, 246))
    flat(c, [Thick(370, 594, 330, 600, 2)], (90, 90, 100))
    # dog chasing (right front)
    if "dog" not in d:
        piece(c, [Ell(800, 560, 30, 13), Circ(830, 540, 12), Ell(840, 546, 8, 6)], (250, 250, 246), border=1.2, shadow=SMALL)
        flat(c, [Ell(796, 556, 10, 6), Ell(826, 534, 4, 8)], (60, 50, 50))
        for lx in (-20, -8, 10, 20):
            flat(c, RRect(800 + lx - 3, 568, 800 + lx + 3, 590, 1), (240, 240, 236))


def tail_el(eid, x, y, length, col, phase=0.0):
    return E(eid, lambda c, m: [flat(c, Thick(x, y + k * length / 5, x + (6 if k % 2 else -6), y + (k + 1) * length / 5, 2), col) for k in range(5)],
             pivot=(x, y), anim=dict(swingAngle=14, swingSpeed=0.9, phase=phase))


L305_ELEMENTS = [
    tail_el("tail1", 150, 124, 70, (250, 210, 70)),
    tail_el("tail2", 470, 100, 60, (220, 60, 50), 0.3),
    E("flyk", lambda c, m: kite(c, 330, 230, 0.9, (200, 90, 200), (250, 250, 246)), pivot=(330, 230), anim=dict(bobAmplitude=(20, 14), bobSpeed=0.2, swingAngle=10, swingSpeed=0.6)),
    bird_el("bird", 600, 50, s=9, speed=-14),
]

L305_DIFFS = [
    ("kite1", 150, 92, 0),
    ("fishkite", 690, 170, 0),
    ("tent", 820, 290, 0),
    ("flyer", 722, 430, 0),
    ("blanket", 160, 540, 0),
    ("groundkite", 370, 562, 0),
    ("dog", 816, 556, 0),
]


# =================================================================== Level 306 canal water town
def ww_house(c, x0, x1, base, h, roof=(60, 64, 72), wall=(246, 244, 236), win=(120, 90, 70)):
    piece(c, RRect(x0, base - h, x1, base, 1), wall, border=1.5, shadow=PROP)
    piece(c, Poly([(x0 - 10, base - h + 4), (x1 + 10, base - h + 4), (x1 - 4, base - h - 20), (x0 + 4, base - h - 20)]), roof, border=1.5, shadow=PROP)
    flat(c, [Thick(x0 - 12, base - h + 4, x0 - 2, base - h - 6, 3), Thick(x1 + 12, base - h + 4, x1 + 2, base - h - 6, 3)], roof)
    for k in range(int((x1 - x0) // 50)):
        flat(c, RRect(x0 + 16 + k * 50, base - h + 20, x0 + 40 + k * 50, base - h + 46, 2), win)


def l306_bg(c, d):
    sky(c, (190, 210, 220), (236, 236, 230), H)
    far_ridge(c, 150, 40, (190, 200, 206), 3061)
    far_round_trees(c, 180, 20, (130, 160, 140), 3062)
    # houses on both banks
    ww_house(c, 0, 200, 290, 120)
    ww_house(c, 210, 360, 290, 100, roof=(60, 64, 72) if "roof" not in d else (180, 70, 60))
    ww_house(c, 560, 720, 290, 110)
    ww_house(c, 730, 900, 290, 130)
    # canal
    c.rect(0, 290, W, 520, (110, 150, 150))
    for k in range(9):
        flat(c, Thick(20 + k * 100, 320 + (k % 3) * 60, 70 + k * 100, 320 + (k % 3) * 60, 1.6), (150, 186, 186))
    # reflections
    for x0, x1 in ((0, 200), (210, 360), (560, 720), (730, 900)):
        flat(c, RRect(x0, 292, x1, 330, 0), (150, 180, 180))
    # stone arch bridge (centre)
    br = (190, 186, 176)
    top = [(450 - 170 * math.cos(math.pi * k / 16), 330 - 110 * math.sin(math.pi * k / 16)) for k in range(17)]
    arch = [(450 - 80 * math.cos(math.pi * k / 16), 340 - 70 * math.sin(math.pi * k / 16)) for k in range(16, -1, -1)]
    piece(c, Poly([(260, 340)] + top + [(640, 340)] + arch), br, border=1.5, shadow=PROP)
    for k in range(2, 15, 2):
        x, y = top[k]
        flat(c, Thick(x, y, x, y - 18, 3), lit(br, 0.85))
    flat(c, Ell(450, 340, 80, 6), (90, 120, 120))
    plaque = (200, 60, 50) if "bridge" not in d else (60, 110, 160)
    piece(c, RRect(418, 236, 482, 262, 3), plaque, border=1.2, shadow=SMALL)
    modern(c, 470, 222, (200, 80, 90), bottom=(60, 60, 70), hair=(30, 30, 34), h=1.4, style="long")
    # red lanterns under eaves
    for k, x in enumerate((60, 140, 620, 800)):
        col = (220, 50, 40) if not (k == 3 and "lantern" in d) else (250, 210, 80)
        flat(c, Thick(x, 170 if x < 500 else 160, x, 186 if x < 500 else 176, 1.4), (60, 50, 50))
        lantern(c, x, 198 if x < 500 else 188, 1.0, col)
    # boats
    boat_col = (120, 80, 50)
    piece(c, Poly([(80, 420), (300, 416), (280, 444), (100, 446)]), boat_col, border=1.5, shadow=PROP)
    canopy = (60, 64, 72) if "canopy" not in d else (200, 120, 60)
    piece(c, Poly([(140, 418), (240, 416), (230, 384), (150, 386)]), canopy, border=1.2, shadow=SMALL)
    hx, hy = modern(c, 270, 420, (90, 120, 160), bottom=(50, 50, 60), hair=(30, 30, 34), h=1.4)
    piece(c, Poly([(hx - 16, hy - 4), (hx + 16, hy - 4), (hx, hy - 16)]), (230, 200, 120), border=1, shadow=None)
    flat(c, Thick(290, 400, 320, 470, 2), (120, 90, 60))
    piece(c, Poly([(560, 470), (760, 466), (740, 494), (580, 496)]), boat_col, border=1.5, shadow=PROP)
    cargo = (230, 210, 150) if "cargo" not in d else (120, 170, 120)
    for x in (610, 650, 690):
        piece(c, Ell(x, 462, 20, 14), cargo, border=1, shadow=SMALL)
    # stone quay (front)
    piece(c, RRect(0, 510, W, 600, 0), (170, 166, 156), shadow=LAYER)
    for x in range(0, W, 60):
        flat(c, RRect(x + 2, 512, x + 58, 552, 2), (180, 176, 166))
        flat(c, RRect(x + 32, 556, x + 90, 598, 2), (180, 176, 166))
    # willow (left front)
    piece(c, Thick(40, 600, 50, 470, 8), (110, 80, 60), shadow=PROP)
    for k in range(9):
        flat(c, Thick(50 + k * 8 - 30, 470, 40 + k * 8 - 30, 560, 3), (120, 170, 90))
    # umbrella vendor (right front)
    umb = (200, 60, 50) if "umbrella" not in d else (60, 120, 180)
    flat(c, Thick(820, 600, 820, 500, 3), (120, 90, 60))
    piece(c, Poly([(750, 510), (890, 510), (820, 470)]), umb, border=1.5, shadow=PROP)
    modern(c, 780, 600, (240, 236, 220), bottom=(60, 60, 70), hair=(30, 30, 34), h=2.2)


L306_ELEMENTS = [
    E("ripple", lambda c, m: [flat(c, Thick(x, 470, x + 30, 470, 1.6), (160, 196, 196)) for x in (380, 820)], daynight="untinted",
      anim=dict(bobAmplitude=(12, 0), bobSpeed=0.3)),
    bird_el("bird", 300, 70, s=9, speed=14),
    E("sway", lambda c, m: flat(c, Thick(30, 470, 24, 560, 3), (130, 180, 96)), pivot=(30, 470), anim=dict(swingAngle=6, swingSpeed=0.5)),
]

L306_DIFFS = [
    ("roof", 285, 182, 0),
    ("lantern", 800, 190, 0),
    ("bridge", 450, 249, 0),
    ("canopy", 190, 402, 0),
    ("cargo", 650, 462, 0),
    ("umbrella", 820, 494, 0),
]


# =================================================================== Level 307 wheat harvest
def combine(c, x, base, col):
    piece(c, [RRect(x - 70, base - 80, x + 60, base - 20, 6), RRect(x + 10, base - 130, x + 60, base - 80, 4)], col, border=1.5, shadow=PROP)
    flat(c, RRect(x + 18, base - 122, x + 52, base - 92, 3), (190, 220, 236))
    piece(c, [Poly([(x - 140, base - 10), (x - 70, base - 10), (x - 70, base - 60), (x - 140, base - 40)])], lit(col, 0.85), border=1.2, shadow=SMALL)
    for k in range(5):
        flat(c, Thick(x - 136 + k * 14, base - 40 + k * 4, x - 136 + k * 14, base - 12, 2), (60, 60, 60))
    flat(c, Thick(x - 40, base - 80, x - 80, base - 120, 8), lit(col, 0.9))
    for wx, r in ((x - 40, 26), (x + 40, 18)):
        wheel(c, wx, base - r + 4, r, tyre=(40, 40, 46), hub=(220, 200, 80))


def l307_bg(c, d):
    sky(c, (140, 190, 236), (250, 230, 190), H)
    sun_bg(c, 120, 70, 30)
    cloud_bg(c, 640, 60, 0.6)
    far_ridge(c, 190, 40, (170, 190, 170), 3071)
    far_round_trees(c, 210, 20, (110, 160, 100), 3072)
    # farmhouse + silo (right back)
    piece(c, RRect(700, 160, 820, 230, 2), (240, 230, 210), border=1.5, shadow=PROP)
    roof = (180, 70, 60) if "roof" not in d else (60, 110, 160)
    piece(c, Poly([(690, 162), (830, 162), (760, 120)]), roof, border=1.5, shadow=PROP)
    piece(c, [RRect(840, 110, 880, 230, 8)], (200, 200, 210), border=1.5, shadow=PROP)
    # wheat field
    c.rect(0, 230, W, H, (230, 190, 90))
    rnd = random.Random(3073)
    for y in range(240, 600, 18):
        for x in range(-10, W, 22):
            flat(c, Thick(x + rnd.uniform(-4, 4), y + 12, x + rnd.uniform(-4, 4), y, 2), (210, 170, 70))
    # harvested stripe (stubble)
    flat(c, Poly([(0, 330), (W, 310), (W, 380), (0, 400)]), (210, 190, 130))
    # combine (centre)
    combine(c, 520, 380, (90, 160, 80) if "combine" not in d else (220, 80, 60))
    # hay bales (round) on the stubble
    for k, x in enumerate((100, 200)):
        col = (220, 180, 90) if not (k == 1 and "bale" in d) else (150, 200, 120)
        piece(c, Circ(x, 360, 30), col, border=1.5, shadow=PROP)
        c.ellipse_ring(x, 360, 18, 18, 3, lit(col, 0.85))
    # scarecrow (left front)
    flat(c, [Thick(140, 600, 140, 440, 4), Thick(100, 480, 180, 480, 4)], (120, 90, 60))
    sc = (90, 120, 180) if "scarecrow" not in d else (200, 80, 90)
    piece(c, Poly([(116, 476), (164, 476), (170, 530), (110, 530)]), sc, border=1.2, shadow=SMALL)
    flat(c, Circ(140, 456, 16), (240, 220, 160))
    piece(c, [Ell(140, 442, 26, 6), Ell(140, 436, 14, 8)], (200, 170, 90), shadow=SMALL)
    # crow on the arm
    piece(c, [Ell(180, 470, 12, 8), Circ(190, 462, 6)], (40, 40, 46), border=1, shadow=None)
    # farm truck (right front)
    truck = (200, 60, 50) if "truck" not in d else (60, 120, 180)
    piece(c, [RRect(640, 470, 780, 530, 4), RRect(780, 490, 860, 530, 4), Poly([(780, 490), (820, 450), (850, 450), (860, 490)])], truck, border=1.5, shadow=PROP)
    flat(c, Poly([(788, 488), (822, 456), (846, 456), (852, 488)]), (190, 220, 236))
    for x in (680, 820):
        wheel(c, x, 536, 18, tyre=(40, 40, 46), hub=(200, 200, 210))
    piece(c, [Ell(680, 466, 24, 14), Ell(730, 466, 24, 14)], (230, 200, 110), shadow=SMALL)
    # farmer with pitchfork (centre front)
    hx, hy = modern(c, 400, 600, (240, 200, 70), bottom=(60, 90, 150), hair=(90, 60, 40), h=2.4)
    hat = (230, 200, 120) if "hat" not in d else (90, 90, 110)
    piece(c, [Ell(hx, hy - 8, 24, 6), Ell(hx, hy - 14, 13, 9)], hat, shadow=SMALL)
    flat(c, [Thick(440, 600, 470, 460, 3), Thick(462, 470, 482, 448, 2), Thick(470, 466, 486, 452, 2)], (120, 90, 60))
    # water jug + basket (left)
    jug = (90, 140, 200) if "jug" not in d else (240, 160, 60)
    piece(c, [RRect(240, 530, 280, 590, 8), RRect(250, 518, 270, 532, 2)], jug, border=1.2, shadow=SMALL)


L307_ELEMENTS = [
    bird_el("crow", 300, 120, s=10, col=(40, 40, 46), speed=16),
    bird_el("crow2", 560, 180, s=9, col=(40, 40, 46), speed=-12),
    E("chaff", lambda c, m: piece(c, Circ(420, 260, 8), (240, 220, 160), shadow=None), pivot=(420, 260),
      anim=dict(driftVelocity=(-30, -14), driftLength=90, driftFade=True, driftGrow=1.8)),
    E("reel", lambda c, m: [flat(c, Thick(390, 345, 390 + 26 * math.cos(a), 345 + 26 * math.sin(a), 3), (220, 200, 80)) for a in (0, 1.57, 3.14, 4.71)],
      pivot=(390, 345), anim=dict(rotateSpeed=90)),
]

L307_DIFFS = [
    ("roof", 760, 140, 0),
    ("combine", 540, 320, 0),
    ("bale", 200, 360, 0),
    ("scarecrow", 140, 500, 0),
    ("truck", 750, 500, 0),
    ("hat", 402, 470, 0),
    ("jug", 260, 556, 0),
]


# =================================================================== Level 308 cherry-blossom river
def blossom(c, x, base, s, col=(250, 196, 214)):
    piece(c, [Thick(x, base, x, base - 60 * s, 7 * s), Thick(x, base - 40 * s, x - 30 * s, base - 80 * s, 4 * s), Thick(x, base - 50 * s, x + 30 * s, base - 86 * s, 4 * s)],
          (110, 80, 70), shadow=PROP)
    piece(c, [Circ(x, base - 100 * s, 36 * s), Circ(x - 36 * s, base - 84 * s, 26 * s), Circ(x + 36 * s, base - 88 * s, 26 * s), Circ(x - 14 * s, base - 124 * s, 22 * s)],
          col, shadow=PROP)
    flat(c, [Circ(x - 14 * s, base - 108 * s, 10 * s), Circ(x + 20 * s, base - 96 * s, 8 * s)], lit(col, 1.06))


def l308_bg(c, d):
    sky(c, (170, 210, 240), (246, 236, 236), H)
    far_skyline(c, 200, 30, 90, (200, 200, 214), 3081, win=(220, 220, 230))
    # far bank with blossoms
    layer(c, 200, [(4, 0.02, 0.4)], (150, 190, 130))
    for x in range(-20, W + 40, 70):
        piece(c, Circ(x, 200, 34), (250, 210, 222), shadow=SMALL)
    # river
    c.rect(0, 230, W, 420, (110, 170, 210))
    for k in range(10):
        flat(c, Thick(30 + k * 90, 260 + (k % 3) * 50, 80 + k * 90, 260 + (k % 3) * 50, 1.6), (170, 210, 236))
    # footbridge (centre back)
    fb = (200, 60, 50) if "bridge" not in d else (90, 140, 190)
    piece(c, Poly([(320, 250), (580, 250), (560, 236), (340, 236)]), fb, border=1.2, shadow=SMALL)
    for x in range(330, 580, 30):
        flat(c, Thick(x, 236, x, 220, 2), fb)
    flat(c, Thick(330, 220, 570, 220, 2), fb)
    # rowing boats
    b1 = (250, 250, 246) if "boat" not in d else (250, 200, 70)
    piece(c, Poly([(120, 330), (280, 326), (262, 350), (136, 352)]), b1, border=1.2, shadow=SMALL)
    modern(c, 200, 334, (240, 120, 150), bottom=(60, 60, 70), hair=(30, 30, 34), h=1.4, style="long")
    piece(c, Poly([(600, 370), (760, 366), (742, 390), (616, 392)]), (90, 150, 200), border=1.2, shadow=SMALL)
    modern(c, 660, 374, (240, 200, 70), bottom=(60, 60, 70), hair=(90, 60, 40), h=1.4)
    modern(c, 710, 374, (90, 160, 110), bottom=(60, 60, 70), hair=(40, 30, 30), h=1.3)
    # near bank
    piece(c, hill_strip(420, [(8, 0.012, 0.6), (4, 0.05, 1.0)]), (140, 190, 110), shadow=LAYER)
    blossom(c, 90, 560, 1.4, col=(250, 196, 214) if "tree" not in d else (250, 250, 246))
    blossom(c, 820, 540, 1.3)
    # lantern string between trees
    flat(c, Thick(130, 380, 780, 380, 1.4), (90, 80, 70))
    for k, x in enumerate(range(180, 780, 70)):
        col = (250, 200, 210) if not (k == 4 and "lantern" in d) else (240, 100, 70)
        lantern(c, x, 396 + 6 * math.sin(k), 0.9, col)
    # picnic
    blanket(c, 300, 500, 520, 540, (90, 150, 210) if "blanket" not in d else (240, 140, 60), (250, 250, 246))
    piece(c, RRect(360, 480, 420, 506, 4), (220, 60, 60), border=1.2, shadow=SMALL)
    modern(c, 470, 520, (250, 200, 210), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.8, style="long")
    modern(c, 610, 560, (90, 110, 160), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.2)
    # bicycle (right front)
    bike = (60, 140, 120) if "bike" not in d else (220, 80, 120)
    for x in (640, 720):
        wheel(c, x, 576, 20, tyre=(40, 40, 46), hub=(200, 200, 210))
    flat(c, [Thick(640, 576, 680, 540, 4), Thick(680, 540, 720, 576, 4), Thick(680, 540, 710, 540, 4), Thick(660, 556, 700, 556, 4)], bike)


L308_ELEMENTS = [
    E("petal1", lambda c, m: flat(c, Ell(300, 120, 5, 3), (250, 196, 214)), pivot=(300, 120),
      anim=dict(driftVelocity=(20, 40), driftLength=180, driftFade=True, swingAngle=60, swingSpeed=1.2)),
    E("petal2", lambda c, m: flat(c, Ell(560, 100, 5, 3), (250, 196, 214)), pivot=(560, 100),
      anim=dict(driftVelocity=(-16, 44), driftLength=180, driftFade=True, swingAngle=60, swingSpeed=1.0, phase=0.4)),
    E("petal3", lambda c, m: flat(c, Ell(820, 360, 5, 3), (250, 196, 214)), pivot=(820, 360),
      anim=dict(driftVelocity=(-30, 30), driftLength=140, driftFade=True, swingAngle=60, swingSpeed=1.4, phase=0.7)),
    E("oar", lambda c, m: flat(c, Thick(170, 340, 230, 330, 2), (120, 90, 60)), pivot=(200, 335), anim=dict(swingAngle=18, swingSpeed=1.0)),
    bird_el("bird", 400, 60, s=9, speed=14),
]

L308_DIFFS = [
    ("bridge", 450, 236, 0),
    ("boat", 200, 340, 0),
    ("tree", 90, 440, 0),
    ("lantern", 460, 400, 0),
    ("blanket", 410, 520, 0),
    ("bike", 680, 560, 0),
]


# =================================================================== Level 309 snow festival
ICE = (190, 224, 240)


def l309_bg(c, d):
    c.gradient(0, H, (40, 50, 110), (140, 150, 200))
    rnd = random.Random(3091)
    for _ in range(60):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 200), rnd.choice((1.0, 1.6))), (250, 250, 230))
    far_ridge(c, 230, 40, (130, 150, 190), 3092)
    c.rect(0, 280, W, H, (226, 232, 246))
    # ice castle (centre)
    for x, top, w in ((360, 150, 60), (540, 150, 60), (450, 90, 80)):
        npiece(c, [RRect(x - w / 2, top, x + w / 2, 320, 2), Poly([(x - w / 2 - 6, top + 2), (x + w / 2 + 6, top + 2), (x, top - 50)])], ICE)
    npiece(c, RRect(320, 220, 580, 320, 2), ICE)
    flat(c, Poly([(420, 320), (420, 270), (450, 250), (480, 270), (480, 320)]), (120, 160, 200))
    glow = (250, 210, 120) if "castle" not in d else (180, 120, 240)
    for x, y in ((360, 190), (540, 190), (450, 140)):
        flat(c, RRect(x - 10, y, x + 10, y + 24, 6), glow)
    # ice sculpture: swan (left)
    if "swan" not in d:
        npiece(c, [Ell(140, 330, 50, 24), Thick(170, 320, 184, 260, 8), Ell(192, 256, 14, 8)], ICE)
        npiece(c, Poly([(100, 320), (60, 270), (130, 314)]), ICE)
    npiece(c, RRect(80, 350, 200, 370, 2), (200, 210, 230))
    # lantern posts
    for k, x in enumerate((260, 650)):
        flat(c, Thick(x, 360, x, 270, 3), (60, 60, 80))
        col = (250, 200, 90) if not (k == 1 and "lamp" in d) else (120, 220, 250)
        npiece(c, RRect(x - 12, 250, x + 12, 276, 3), col, shadow=None)
    # skating rink (right)
    flat(c, Ell(760, 400, 140, 34), (200, 226, 246))
    modern(c, 720, 400, (220, 60, 60), bottom=(40, 40, 60), hair=(200, 160, 90), h=1.6, style="long")
    modern(c, 800, 410, (60, 120, 200) if "skater" not in d else (250, 200, 60), bottom=(40, 40, 60), hair=(40, 30, 30), h=1.7)
    # food stall (left front)
    npiece(c, RRect(30, 460, 230, 580, 2), (190, 120, 80))
    stripe = (220, 60, 60) if "stall" not in d else (60, 140, 90)
    for x in range(30, 230, 40):
        flat(c, RRect(x, 440, x + 20, 470, 0), stripe)
        flat(c, RRect(x + 20, 440, x + 40, 470, 0), (250, 250, 246))
    flat(c, RRect(50, 490, 210, 540, 2), (250, 220, 150))
    # visitors with scarves
    for x, top, sc in ((380, (90, 90, 140), (220, 60, 60)), (520, (200, 120, 60), (60, 160, 120))):
        hx, hy = modern(c, x, 590, top, bottom=(40, 40, 60), hair=(60, 40, 30), h=2.3)
        col = sc if not (x == 520 and "scarf" in d) else (250, 200, 60)
        flat(c, [RRect(hx - 16, hy + 12, hx + 16, hy + 20, 3), RRect(hx + 4, hy + 16, hx + 12, hy + 40, 2)], col)
    # snowman with hat (right front)
    npiece(c, [Circ(800, 560, 34), Circ(800, 510, 24)], (246, 248, 252))
    hat = (40, 40, 50) if "hat" not in d else (200, 60, 60)
    npiece(c, [RRect(784, 470, 816, 490, 2), RRect(776, 488, 824, 492, 1)], hat, shadow=None)
    flat(c, [Circ(792, 506, 2.4), Circ(808, 506, 2.4)], INK)
    flat(c, Poly([(800, 512), (820, 516), (800, 518)]), (250, 140, 40))


L309_ELEMENTS = [
    E("snow1", lambda c, m: [flat(c, Circ(x, y, 2.4), (250, 252, 255)) for x, y in ((60, 80), (240, 40), (380, 160), (520, 100), (660, 30), (860, 180), (320, 260), (760, 300))],
      daynight="untinted", anim=dict(driftVelocity=(-6, 40), driftLength=120, driftFade=True)),
    E("glow", lambda c, m: soft_union(c, [RRect(320, 150, 580, 320, 4)], (150, 210, 255), 0.15, spread=24), daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=0.6)),
    E("fw", lambda c, m: [flat(c, Thick(150, 120, 150 + 20 * math.cos(a), 120 + 20 * math.sin(a), 2), (250, 200, 120)) for a in [k * 0.785 for k in range(8)]],
      pivot=(150, 120), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=0.5, stretch=(0.5, 0.5), scaleSpeed=0.5)),
] + steam("stm", 130, 470, n=3, r=8)

L309_DIFFS = [
    ("castle", 450, 170, 0),
    ("swan", 140, 300, 0),
    ("lamp", 650, 262, 0),
    ("skater", 800, 360, 0),
    ("stall", 130, 456, 0),
    ("scarf", 524, 520, 0),
    ("hat", 800, 482, 0),
]


# =================================================================== Level 310 pumpkin farm
def pumpkin(c, x, base, s, col=(240, 140, 40)):
    piece(c, [Ell(x - 10 * s, base - 16 * s, 14 * s, 16 * s), Ell(x + 10 * s, base - 16 * s, 14 * s, 16 * s), Ell(x, base - 16 * s, 14 * s, 17 * s)], col, border=1.2,
          shadow=SMALL)
    flat(c, Thick(x, base - 32 * s, x + 3 * s, base - 40 * s, 3 * s), (90, 120, 60))


def l310_bg(c, d):
    sky(c, (140, 190, 236), (250, 226, 190), H)
    cloud_bg(c, 300, 60, 0.6)
    far_round_trees(c, 200, 30, (220, 140, 70), 3101)
    # red barn (left back)
    barn = (190, 50, 40) if "barn" not in d else (60, 100, 150)
    piece(c, [RRect(40, 150, 220, 260, 2), Poly([(30, 152), (230, 152), (200, 110), (130, 90), (60, 110)])], barn, border=1.5, shadow=PROP)
    flat(c, [RRect(100, 190, 160, 260, 2)], (250, 250, 246))
    flat(c, [Thick(100, 190, 160, 260, 3), Thick(160, 190, 100, 260, 3)], barn)
    # hay maze (right back)
    for k in range(6):
        for j in range(3):
            if (k + j) % 4 == 1:
                continue
            piece(c, RRect(560 + k * 54, 180 + j * 30, 610 + k * 54, 206 + j * 30, 4), (230, 200, 110), border=1, shadow=SMALL)
    # field
    c.rect(0, 260, W, H, (140, 120, 80))
    for y in range(280, 600, 40):
        flat(c, Thick(0, y, W, y - 10, 3), (120, 104, 70))
    rnd = random.Random(3102)
    for _ in range(26):
        x, y = rnd.uniform(0, W), rnd.uniform(290, 420)
        pumpkin(c, x, y, rnd.uniform(0.7, 1.1))
    # tractor wagon with kids (centre)
    wag = (90, 140, 70) if "tractor" not in d else (220, 180, 50)
    piece(c, [RRect(260, 420, 440, 470, 3)], (200, 160, 100), border=1.5, shadow=PROP)
    piece(c, [RRect(450, 400, 550, 470, 6), RRect(500, 360, 545, 404, 3)], wag, border=1.5, shadow=PROP)
    flat(c, RRect(506, 368, 540, 396, 2), (190, 220, 236))
    for x, r in ((300, 16), (400, 16), (470, 18), (530, 26)):
        wheel(c, x, 478 - (r - 16), r, tyre=(40, 40, 46), hub=(220, 200, 80))
    for x, col in ((290, (220, 60, 60)), (340, (60, 120, 200)), (390, (250, 200, 60))):
        modern(c, x, 424, col, bottom=(60, 60, 70), hair=(90, 60, 40), h=1.2)
    # big pumpkin (left front)
    pumpkin(c, 120, 560, 3.0, col=(240, 140, 40) if "pumpkin" not in d else (240, 236, 220))
    # apple stand (right front)
    piece(c, [RRect(650, 500, 880, 520, 2), RRect(660, 520, 672, 596, 2), RRect(858, 520, 870, 596, 2)], (170, 120, 80), border=1.5, shadow=PROP)
    for k, x in enumerate(range(680, 870, 46)):
        col = (220, 50, 50) if not (k == 2 and "apples" in d) else (140, 200, 70)
        piece(c, Poly([(x - 20, 500), (x + 20, 500), (x + 16, 476), (x - 16, 476)]), (190, 140, 80), border=1, shadow=None)
        flat(c, [Circ(x - 8, 472, 8), Circ(x + 8, 472, 8), Circ(x, 464, 8)], col)
    sign = (250, 240, 200) if "sign" not in d else (240, 160, 70)
    piece(c, RRect(700, 420, 830, 456, 3), sign, border=1.2, shadow=SMALL)
    sign_box(c, 710, 426, 820, 450, sign, 3103, glyph=(150, 60, 40), vertical=False)
    # scarecrow-free: wheelbarrow (centre front)
    wb = (90, 120, 160) if "barrow" not in d else (200, 80, 110)
    piece(c, Poly([(360, 540), (500, 540), (480, 580), (380, 580)]), wb, border=1.5, shadow=PROP)
    wheel(c, 380, 590, 12, tyre=(40, 40, 46), hub=(200, 200, 210))
    flat(c, Thick(500, 544, 540, 570, 4), (120, 90, 60))
    pumpkin(c, 420, 542, 1.2)
    pumpkin(c, 456, 540, 1.0, col=(250, 200, 90))


L310_ELEMENTS = [
    bird_el("crow", 400, 70, s=10, col=(40, 40, 46), speed=14),
    E("leaf", lambda c, m: flat(c, Poly(star_pts(600, 120, 7, 3)), (230, 90, 50)), pivot=(600, 120),
      anim=dict(driftVelocity=(-12, 40), driftLength=120, driftFade=True, swingAngle=60, swingSpeed=1.2)),
    E("exhaust", lambda c, m: piece(c, Circ(546, 352, 7), (210, 210, 210), shadow=None), pivot=(546, 352),
      anim=dict(driftVelocity=(10, -20), driftLength=50, driftFade=True, driftGrow=1.5)),
]

L310_DIFFS = [
    ("barn", 130, 170, 0),
    ("tractor", 500, 400, 0),
    ("pumpkin", 120, 515, 0),
    ("apples", 772, 468, 0),
    ("sign", 765, 438, 0),
    ("barrow", 430, 560, 0),
]


# =================================================================== Level 311 wetland birdwatching
def flamingo(c, x, base, s, col=(246, 150, 160), face=1):
    flat(c, [Thick(x, base, x, base - 40 * s, 1.6 * s), Thick(x + 3 * s, base - 30 * s, x - 8 * s, base - 20 * s, 1.6 * s)], lit(col, 0.85))
    piece(c, Ell(x, base - 48 * s, 16 * s, 10 * s), col, border=1, shadow=SMALL)
    flat(c, [Thick(x + 10 * s * face, base - 52 * s, x + 14 * s * face, base - 80 * s, 2.6 * s), Thick(x + 14 * s * face, base - 80 * s, x + 6 * s * face, base - 88 * s, 2.6 * s)],
         col)
    flat(c, Circ(x + 6 * s * face, base - 88 * s, 4 * s), col)
    flat(c, Poly([(x + 8 * s * face, base - 88 * s), (x + 16 * s * face, base - 82 * s), (x + 10 * s * face, base - 84 * s)]), (40, 40, 46))


def l311_bg(c, d):
    sky(c, (170, 210, 236), (240, 236, 220), H)
    cloud_bg(c, 680, 60, 0.6)
    far_ridge(c, 190, 40, (170, 190, 190), 3111)
    far_round_trees(c, 220, 20, (110, 150, 110), 3112)
    c.rect(0, 230, W, H, (120, 170, 190))
    for k in range(10):
        flat(c, Thick(20 + k * 90, 260 + (k % 4) * 50, 70 + k * 90, 260 + (k % 4) * 50, 1.6), (170, 210, 226))
    # mud islands + reeds
    for x0, x1, y in ((60, 340, 330), (520, 860, 300)):
        flat(c, Ell((x0 + x1) / 2, y, (x1 - x0) / 2, 14), (160, 140, 100))
    rnd = random.Random(3113)
    for _ in range(40):
        x = rnd.choice([rnd.uniform(0, 140), rnd.uniform(760, 900)])
        y = rnd.uniform(380, 460)
        flat(c, Thick(x, y + 60, x + rnd.uniform(-6, 6), y, 2), (110, 140, 70))
        flat(c, Ell(x, y, 3, 9), (130, 100, 70))
    # flamingos (left island)
    for k, x in enumerate((110, 170, 230, 290)):
        col = (246, 150, 160) if not (k == 2 and "flamingo" in d) else (250, 250, 246)
        flamingo(c, x, 330, 1.2, col=col, face=1 if k % 2 else -1)
    # storks nest on pole (right)
    flat(c, Thick(700, 300, 700, 120, 5), (120, 90, 60))
    piece(c, Ell(700, 118, 40, 12), (160, 120, 80), border=1.2, shadow=SMALL)
    stork = (250, 250, 246) if "stork" not in d else (60, 60, 70)
    piece(c, [Ell(694, 98, 22, 12), Thick(712, 94, 720, 68, 4), Circ(722, 64, 7)], stork, border=1, shadow=SMALL)
    flat(c, [Thick(728, 64, 748, 68, 3)], (230, 80, 50))
    flat(c, Ell(684, 102, 14, 6), (40, 40, 46))
    # heron on right island
    piece(c, [Ell(600, 270, 18, 10), Thick(612, 262, 620, 230, 3), Ell(624, 228, 8, 5)], (150, 160, 180), border=1, shadow=SMALL)
    # bird hide (centre front)
    hide = (130, 100, 70) if "hide" not in d else (80, 120, 90)
    piece(c, [RRect(320, 380, 600, 500, 2), Poly([(306, 384), (614, 384), (590, 350), (330, 350)])], hide, border=1.5, shadow=PROP)
    flat(c, RRect(340, 410, 580, 440, 2), (50, 40, 34))
    for x in (380, 450, 520):
        flat(c, Circ(x, 426, 9), SKIN)
    # boardwalk
    piece(c, Poly([(0, 520), (W, 510), (W, 540), (0, 552)]), (180, 140, 100), border=1.2, shadow=PROP)
    for x in range(0, W, 30):
        flat(c, Thick(x, 552 - x * 0.013, x, 522 - x * 0.013, 1.4), (160, 120, 84))
    # birdwatchers on boardwalk
    hx, hy = modern(c, 200, 520, (90, 120, 90), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.2)
    bino = (40, 40, 46) if "binoculars" not in d else (220, 120, 50)
    piece(c, [RRect(hx + 4, hy - 4, hx + 22, hy + 8, 3)], bino, border=1, shadow=None)
    modern(c, 660, 516, (200, 90, 80), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.1, style="long")
    # tripod scope (right front)
    scope = (60, 60, 70) if "scope" not in d else (220, 220, 230)
    flat(c, [Thick(780, 516, 800, 460, 3), Thick(820, 516, 800, 460, 3), Thick(800, 516, 800, 460, 3)], (90, 90, 100))
    piece(c, [RRect(770, 440, 840, 462, 6)], scope, border=1.2, shadow=SMALL)
    # sign (left front)
    sg = (90, 130, 90) if "sign" not in d else (190, 120, 70)
    flat(c, Thick(80, 600, 80, 560, 4), (110, 80, 60))
    piece(c, RRect(30, 556, 140, 590, 3), sg, border=1.2, shadow=SMALL)


L311_ELEMENTS = [
    bird_el("goose1", 300, 80, s=11, speed=14),
    bird_el("goose2", 340, 100, s=10, speed=14),
    E("ripple", lambda c, m: c.ellipse_ring(450, 300, 24, 5, 1.6, (180, 220, 236)), pivot=(450, 300), anim=dict(stretch=(0.5, 0.5), scaleSpeed=1.0)),
    E("reed", lambda c, m: flat(c, Thick(880, 470, 884, 400, 2), (110, 140, 70)), pivot=(880, 470), anim=dict(swingAngle=6, swingSpeed=0.6)),
]

L311_DIFFS = [
    ("flamingo", 230, 290, 0),
    ("stork", 708, 90, 0),
    ("hide", 460, 380, 0),
    ("binoculars", 214, 420, 0),
    ("scope", 805, 450, 0),
    ("sign", 85, 573, 0),
]


# =================================================================== Level 312 harbour fish market
def l312_bg(c, d):
    sky(c, (160, 200, 230), (230, 236, 240), H)
    cloud_bg(c, 200, 60, 0.6)
    # sea + boats behind
    c.rect(0, 160, W, 260, (70, 130, 170))
    for x, col, key in ((180, (200, 70, 60), "boat"), (480, (60, 110, 170), None), (760, (240, 200, 70), None)):
        cc = col if not (key and key in d) else (90, 170, 120)
        piece(c, Poly([(x - 80, 230), (x + 90, 226), (x + 70, 256), (x - 66, 258)]), cc, border=1.5, shadow=PROP)
        piece(c, RRect(x - 10, 190, x + 40, 228, 2), (250, 250, 246), border=1.2, shadow=SMALL)
        flat(c, Thick(x - 40, 228, x - 40, 140, 3), (120, 90, 60))
    # market roof
    c.rect(0, 290, W, 600, (200, 196, 186))
    piece(c, RRect(0, 250, W, 290, 0), (90, 100, 110), shadow=PROP)
    roof = (220, 80, 60) if "awning" not in d else (60, 140, 120)
    for x in range(0, W, 60):
        piece(c, Poly([(x, 290), (x + 60, 290), (x + 30, 314)]), roof if 300 <= x < 540 else (220, 80, 60), shadow=None)
    # price board
    board = (60, 70, 70) if "board" not in d else (150, 80, 60)
    piece(c, RRect(620, 320, 860, 400, 3), board, border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, Thick(640, 342 + k * 22, 780, 342 + k * 22, 2), (240, 240, 230))
        flat(c, Thick(800, 342 + k * 22, 840, 342 + k * 22, 2), (250, 220, 120))
    # fishmonger behind counter
    hx, hy = modern(c, 420, 450, (250, 250, 246), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.2)
    apron = (60, 120, 180) if "apron" not in d else (220, 180, 60)
    piece(c, Poly([(400, 418), (440, 418), (446, 450), (394, 450)]), apron, border=1, shadow=None)
    # counter with ice and fish crates
    piece(c, RRect(0, 450, W, 600, 0), (150, 160, 170), shadow=LAYER)
    for k, x in enumerate(range(20, W, 180)):
        piece(c, RRect(x, 440, x + 160, 500, 3), (200, 160, 110), border=1.5, shadow=PROP)
        flat(c, RRect(x + 6, 440, x + 154, 456, 2), (230, 240, 248))
        col = [(170, 180, 200), (230, 120, 100), (200, 200, 210), (120, 140, 170), (240, 180, 160)][k]
        if k == 1 and "fish" in d:
            col = (250, 210, 80)
        for j in range(4):
            fish(c, x + 30 + j * 32, 444, 1.1, col, right=j % 2 == 0)
    # scale (left)
    piece(c, [RRect(60, 380, 140, 400, 2), RRect(94, 400, 106, 440, 2), Circ(100, 360, 22)], (200, 200, 210), border=1.2, shadow=SMALL)
    flat(c, Circ(100, 360, 16), (250, 250, 246))
    # octopus in a tub (front)
    piece(c, Poly([(380, 540), (520, 540), (500, 596), (400, 596)]), (90, 140, 190), border=1.5, shadow=PROP)
    octo = (200, 90, 120) if "octopus" not in d else (240, 160, 70)
    piece(c, [Ell(450, 524, 30, 22)] + [Thick(424 + k * 12, 536, 418 + k * 14, 560, 5) for k in range(5)], octo, border=1, shadow=SMALL)
    flat(c, [Circ(440, 520, 3), Circ(460, 520, 3)], INK)
    # customer with basket (left front)
    modern(c, 200, 600, (240, 200, 70), bottom=(60, 70, 100), hair=(200, 160, 90), h=2.4, style="long")
    bask = (190, 140, 80) if "basket" not in d else (220, 80, 80)
    piece(c, [Poly([(220, 560), (270, 560), (264, 590), (226, 590)]), Thick(226, 560, 264, 560, 2)], bask, border=1.2, shadow=SMALL)
    # crab bucket (right front)
    piece(c, Poly([(720, 596), (800, 596), (808, 540), (712, 540)]), (200, 200, 210), border=1.5, shadow=PROP)
    piece(c, [Ell(760, 534, 26, 12), Circ(738, 524, 7), Circ(782, 524, 7)], (230, 80, 50), border=1, shadow=None)


L312_ELEMENTS = [
    bird_el("gull", 300, 80, s=11, speed=16),
    bird_el("gull2", 640, 110, s=10, speed=-14),
    E("gullstand", lambda c, m: piece(c, [Ell(860, 430, 16, 9), Circ(872, 420, 6)], (250, 250, 246), shadow=None), pivot=(860, 438), anim=dict(swingAngle=6, swingSpeed=0.8)),
    E("drip", lambda c, m: flat(c, Circ(100, 460, 2.4), (200, 230, 250)), pivot=(100, 460), anim=dict(driftVelocity=(0, 40), driftLength=40, driftFade=True)),
]

L312_DIFFS = [
    ("boat", 180, 240, 0),
    ("awning", 420, 300, 0),
    ("board", 740, 360, 0),
    ("apron", 420, 434, 0),
    ("fish", 280, 444, 0),
    ("octopus", 450, 530, 0),
    ("basket", 245, 575, 0),
]


# =================================================================== Level 313 watermill
def l313_bg(c, d):
    sky(c, (150, 200, 236), (240, 236, 220), H)
    cloud_bg(c, 660, 60, 0.6)
    far_ridge(c, 180, 50, (170, 190, 180), 3131)
    far_forest(c, 230, 60, (90, 140, 100), 3132)
    # mill house (centre-left)
    piece(c, RRect(220, 150, 480, 380, 2), (230, 220, 196), border=1.5, shadow=PROP)
    for y in range(160, 380, 24):
        flat(c, Thick(220, y, 480, y, 1), (214, 204, 180))
    roof = (150, 80, 60) if "roof" not in d else (70, 100, 140)
    piece(c, Poly([(200, 154), (500, 154), (420, 80), (280, 80)]), roof, border=1.5, shadow=PROP)
    flat(c, [RRect(260, 200, 300, 240, 2), RRect(400, 200, 440, 240, 2)], (120, 90, 70))
    door = (120, 80, 50) if "door" not in d else (60, 130, 90)
    flat(c, RRect(320, 300, 370, 380, 3), door)
    # flower box
    piece(c, RRect(396, 240, 444, 252, 2), (150, 100, 60), shadow=None)
    flat(c, [Circ(404 + k * 10, 236, 5) for k in range(5)], (240, 90, 120))
    # stream
    c.rect(0, 380, W, H, (130, 170, 100))
    flat(c, Poly([(480, 380), (600, 380), (660, 470), (760, 600), (440, 600), (500, 470)]), (100, 160, 200))
    for k in range(5):
        flat(c, Thick(520 + k * 20, 420 + k * 36, 560 + k * 20, 420 + k * 36, 1.6), (170, 210, 236))
    # millrace chute
    piece(c, Poly([(480, 230), (720, 230), (720, 246), (480, 246)]), (150, 110, 70), border=1.2, shadow=PROP)
    flat(c, [Thick(700, 246, 700, 380, 4), Thick(620, 246, 620, 380, 4)], (130, 96, 64))
    # sacks of flour (left front)
    for k, x in enumerate((70, 140)):
        col = (240, 236, 220) if not (k == 1 and "sack" in d) else (220, 180, 120)
        piece(c, [Poly([(x - 34, 590), (x + 34, 590), (x + 28, 510), (x + 10, 496), (x - 10, 496), (x - 28, 510)])], col, border=1.5, shadow=PROP)
        flat(c, Thick(x - 12, 504, x + 12, 504, 4), (150, 110, 70))
    # millstone (left middle)
    ms = (170, 166, 160) if "millstone" not in d else (200, 150, 110)
    piece(c, [Ell(120, 430, 50, 16), RRect(70, 430, 170, 450, 3)], ms, border=1.5, shadow=PROP)
    flat(c, Circ(120, 430, 8), (110, 104, 100))
    # miller
    hx, hy = modern(c, 270, 520, (250, 250, 246), bottom=(90, 90, 110), hair=(200, 200, 200), h=2.3)
    cap = (200, 70, 60) if "cap" not in d else (60, 110, 170)
    piece(c, [Ell(hx, hy - 8, 16, 9)], cap, shadow=SMALL)
    # ducks
    for k, x in enumerate((560, 640)):
        col = (250, 250, 246) if not (k == 1 and "duck" in d) else (150, 110, 70)
        piece(c, [Ell(x, 540, 18, 10), Circ(x + 14, 526, 8)], col, border=1, shadow=SMALL)
        flat(c, Poly([(x + 20, 526), (x + 30, 528), (x + 20, 532)]), (240, 160, 40))
    # cart (right front)
    cart = (170, 120, 80) if "cart" not in d else (90, 140, 190)
    piece(c, RRect(760, 500, 880, 540, 3), cart, border=1.5, shadow=PROP)
    flat(c, Thick(760, 520, 720, 540, 4), (120, 90, 60))
    wheel(c, 820, 550, 22, tyre=(100, 76, 56), hub=(200, 170, 120))
    tree_round(c, 820, 420, 1.3)


L313_ELEMENTS = [
    E("wheel", lambda c, m: [c.ellipse_ring(560, 330, 66, 66, 8, (120, 86, 60))] + [piece(c, Thick(560, 330, 560 + 66 * math.cos(a), 330 + 66 * math.sin(a), 6), (140, 100, 70),
                                                                                           shadow=None) for a in [k * 0.524 for k in range(12)]],
      pivot=(560, 330), anim=dict(rotateSpeed=30)),
    E("splash", lambda c, m: [flat(c, Circ(x, 392, 4), (220, 240, 250)) for x in (520, 560, 600)], pivot=(560, 392), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.6)),
    E("fall", lambda c, m: [flat(c, Thick(x, 246, x, 300, 2), (200, 230, 250)) for x in (640, 660, 680)], daynight="untinted",
      anim=dict(driftVelocity=(0, 40), driftLength=20)),
    bird_el("bird", 400, 50, s=9, speed=14),
]

L313_DIFFS = [
    ("roof", 350, 110, 0),
    ("door", 345, 340, 0),
    ("millstone", 120, 436, 0),
    ("cap", 272, 400, 0),
    ("sack", 140, 545, 0),
    ("duck", 650, 534, 0),
    ("cart", 820, 520, 0),
]


# =================================================================== Level 314 mountain railway
def l314_bg(c, d):
    sky(c, (110, 170, 230), (226, 236, 246), H)
    cloud_bg(c, 160, 60, 0.6)
    peaks = [(-40, 300), (100, 110), (260, 220), (420, 80), (580, 200), (740, 100), (940, 260)]
    piece(c, Poly(peaks + [(940, 320), (-40, 320)]), (150, 166, 196), border=1.5, shadow=LAYER)
    for (x0, y0), (x1, y1), (x2, y2) in zip(peaks, peaks[1:], peaks[2:]):
        if y1 < y0 and y1 < y2:
            flat(c, Poly([(x1, y1), (x1 - 30, y1 + 44), (x1 - 8, y1 + 36), (x1 + 8, y1 + 50), (x1 + 30, y1 + 40)]), (250, 250, 252))
    far_forest(c, 330, 70, (60, 110, 90), 3141)
    # valley
    c.rect(0, 330, W, H, (110, 160, 100))
    flat(c, Poly([(380, 600), (420, 450), (480, 400), (540, 450), (560, 600)]), (100, 160, 200))
    # viaduct
    via = (190, 170, 150)
    piece(c, RRect(0, 300, W, 330, 2), via, border=1.5, shadow=PROP)
    for k in range(6):
        x = 70 + k * 150
        piece(c, Poly([(x - 60, 330), (x + 60, 330), (x + 60, 600), (x + 40, 600)] + [(x + 40 * math.cos(math.pi * j / 10), 480 - 60 * math.sin(math.pi * j / 10))
                                                                                  for j in range(11)] + [(x - 40, 600), (x - 60, 600)]),
              via if not (k == 4 and "viaduct" in d) else (200, 130, 110), border=1.5, shadow=PROP)
    # train
    flat(c, Thick(0, 298, W, 298, 3), (60, 60, 70))
    loco = (40, 50, 60)
    piece(c, [RRect(560, 230, 700, 290, 4), RRect(640, 200, 700, 232, 3), RRect(580, 206, 600, 232, 2)], loco, border=1.5, shadow=PROP)
    flat(c, RRect(648, 208, 692, 226, 2), (250, 220, 140))
    flat(c, Thick(560, 260, 700, 260, 3), (200, 60, 50) if "loco" not in d else (240, 200, 60))
    for x in (580, 620, 670):
        wheel(c, x, 292, 12, tyre=(30, 30, 36), hub=(200, 60, 50))
    for k, x0 in enumerate((240, 400)):
        col = (150, 50, 50) if not (k == 0 and "carriage" in d) else (60, 120, 90)
        piece(c, RRect(x0, 240, x0 + 150, 290, 4), col, border=1.5, shadow=PROP)
        for j in range(4):
            flat(c, RRect(x0 + 12 + j * 34, 250, x0 + 36 + j * 34, 270, 2), (250, 230, 170))
        for x in (x0 + 24, x0 + 126):
            wheel(c, x, 292, 9, tyre=(30, 30, 36), hub=(150, 150, 160))
    # hikers + signpost (front)
    hx, hy = modern(c, 250, 600, (240, 120, 60), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.2)
    pack = (60, 110, 80) if "pack" not in d else (90, 120, 200)
    piece(c, RRect(214, 506, 236, 554, 6), pack, border=1.2, shadow=SMALL)
    flat(c, Thick(800, 600, 800, 480, 4), (120, 90, 60))
    sp = (240, 220, 160) if "signpost" not in d else (220, 90, 70)
    piece(c, [Poly([(740, 484), (850, 484), (864, 498), (850, 512), (740, 512)]), Poly([(860, 520), (750, 520), (736, 534), (750, 548), (860, 548)])], sp, border=1.2,
          shadow=SMALL)
    # goats on the rocks (left middle)
    rock(c, 90, 600, 2.4, col=(150, 150, 140))
    goat_col = (250, 246, 236) if "goat" not in d else (120, 90, 70)
    piece(c, [Ell(90, 540, 22, 11), Ell(114, 528, 9, 7)], goat_col, border=1, shadow=SMALL)
    flat(c, [Thick(116, 522, 108, 510, 2), Thick(80, 550, 80, 560, 3), Thick(100, 550, 100, 560, 3)], (120, 100, 80))


L314_ELEMENTS = smoke_el("smk", 590, 196, n=4, col=(236, 236, 236), r=12, rise=(-30, -16), length=120) + [
    bird_el("eagle", 300, 70, s=12, speed=12),
    cloud_el("cloud", 500, 140, 0.5, 6),
]

L314_DIFFS = [
    ("loco", 630, 250, 0),
    ("carriage", 315, 265, 0),
    ("viaduct", 670, 500, 0),
    ("pack", 225, 530, 0),
    ("signpost", 800, 515, 0),
    ("goat", 100, 535, 0),
]


LEVELS = [
    ("Level305", "风筝节", l305_bg, L305_ELEMENTS, L305_DIFFS, 60, OPTS),
    ("Level306", "江南水乡", l306_bg, L306_ELEMENTS, L306_DIFFS, 60, OPTS),
    ("Level307", "麦田收割", l307_bg, L307_ELEMENTS, L307_DIFFS, 60, OPTS),
    ("Level308", "樱花河畔", l308_bg, L308_ELEMENTS, L308_DIFFS, 60, OPTS),
    ("Level309", "冰雪节", l309_bg, L309_ELEMENTS, L309_DIFFS, 60, OPTS),
    ("Level310", "南瓜农场", l310_bg, L310_ELEMENTS, L310_DIFFS, 60, OPTS),
    ("Level311", "湿地观鸟", l311_bg, L311_ELEMENTS, L311_DIFFS, 60, OPTS),
    ("Level312", "渔港鱼市", l312_bg, L312_ELEMENTS, L312_DIFFS, 60, OPTS),
    ("Level313", "水车磨坊", l313_bg, L313_ELEMENTS, L313_DIFFS, 60, OPTS),
    ("Level314", "山间铁路", l314_bg, L314_ELEMENTS, L314_DIFFS, 60, OPTS),
]
