# -*- coding: utf-8 -*-
"""Mixed themes part 4 (paper-craft side views / interiors, full-bleed, original designs, no brands):
  Level265 竹林熊猫   - a misty bamboo grove: pandas munching, a cub on a rock, pavilion on the ridge, koi stream
  Level266 水族馆     - an aquarium hall: big tank with a ray, turtle, shark, fish school, visitors in front
  Level267 自然博物馆 - a museum hall: dinosaur skeleton, hanging flying-reptile, banners, display cases, visitors
  Level268 画室       - an art studio: easels, painter in a beret, still-life table, plaster bust, big window
  Level269 寿司店     - a sushi bar: chef behind the counter, fish case, menu tags, lanterns, customers
  Level270 宠物店     - a pet shop: fish tanks, parrot cage, puppy pen, kitten basket, hamster, food bags
  Level271 理发店     - a barber shop: mirrors, barber chairs, striped pole, waiting bench, towels
  Level272 咖啡馆     - a cafe: espresso machine, chalk menu, pastry case, pendant lamps, tables
  Level273 洗衣房     - a laundromat: a row of washers with tumbling clothes, folding table, baskets
  Level274 钟表店     - a clock shop: walls of clocks, cuckoo clock, long-case clock, watchmaker's bench
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bubbles_el, bush, cloud_bg, cloud_el, drift_across, fish, layer, rock, sky, sun_bg,
                 tree_round)
from fills import far_ridge, far_round_trees
from levels_akiba import modern, sign_box
from levels_homes import planks, steam
from levels_mix2 import pot_plant

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)
WOOD = (170, 120, 80)


def bamboo(c, x, base, top, w, col=(110, 170, 90), seed=0, leaves=3):
    piece(c, RRect(x - w / 2, top, x + w / 2, base, w / 2), col, border=1.2, shadow=SMALL)
    for y in range(int(top) + 30, int(base), 40):
        flat(c, Thick(x - w / 2, y, x + w / 2, y, 2), lit(col, 0.72))
    rnd = random.Random(seed)
    for _ in range(leaves):
        y = top + rnd.uniform(20, (base - top) * 0.6)
        s = rnd.choice((-1, 1))
        flat(c, [Poly([(x, y), (x + s * 40, y - 10), (x + s * 50, y), (x + s * 20, y + 6)]),
                 Poly([(x, y + 8), (x + s * 34, y + 6), (x + s * 42, y + 16), (x + s * 16, y + 14)])], lit(col, 0.9))


def panda(c, x, base, s, black=(40, 40, 46), white=(248, 248, 244), face=1):
    piece(c, [Ell(x - 16 * s, base - 8 * s, 13 * s, 9 * s), Ell(x + 16 * s, base - 8 * s, 13 * s, 9 * s)], black, border=1.2, shadow=SMALL)
    piece(c, Ell(x, base - 32 * s, 26 * s, 26 * s), white, border=1.2, shadow=PROP)
    flat(c, [Thick(x - 20 * s, base - 46 * s, x - 24 * s, base - 22 * s, 9 * s), Thick(x + 20 * s, base - 46 * s, x + 24 * s, base - 22 * s, 9 * s),
             Ell(x, base - 50 * s, 24 * s, 7 * s)], black)
    hx, hy = x + 3 * s * face, base - 66 * s
    piece(c, [Circ(hx - 15 * s, hy - 15 * s, 7 * s), Circ(hx + 15 * s, hy - 15 * s, 7 * s)], black, border=1.2, shadow=SMALL)
    piece(c, Ell(hx, hy, 21 * s, 18 * s), white, border=1.2, shadow=SMALL)
    flat(c, [Ell(hx - 8 * s, hy - 1 * s, 5.4 * s, 7 * s), Ell(hx + 8 * s, hy - 1 * s, 5.4 * s, 7 * s), Ell(hx + 1 * s * face, hy + 8 * s, 3.4 * s, 2.4 * s)], black)
    flat(c, [Circ(hx - 7 * s, hy - 2 * s, 1.6 * s), Circ(hx + 9 * s, hy - 2 * s, 1.6 * s)], (250, 250, 250))
    return hx, hy


# =================================================================== Level 265 bamboo grove
def l265_bg(c, d):
    sky(c, (196, 224, 200), (238, 240, 222), H)
    sun_bg(c, 790, 80, 30, col=(250, 200, 120) if "sun" not in d else (240, 120, 120))
    far_ridge(c, 200, 70, (176, 200, 180), 2651)
    # pavilion on the far ridge (left)
    piece(c, [RRect(110, 150, 116, 196, 1), RRect(184, 150, 190, 196, 1), RRect(104, 194, 196, 202, 1)], (150, 80, 60), shadow=SMALL)
    roof = (170, 60, 50) if "roof" not in d else (60, 110, 170)
    piece(c, [Poly([(84, 156), (216, 156), (196, 136), (150, 120), (104, 136)]), RRect(144, 108, 156, 122, 2)], roof, border=1.2, shadow=SMALL)
    far_ridge(c, 250, 50, (150, 186, 156), 2652)
    # crane flying (centre top)
    if "crane" not in d:
        piece(c, [Ell(450, 90, 30, 10), Poly([(424, 88), (370, 70), (378, 92)]), Poly([(470, 88), (520, 60), (510, 92)])], (250, 250, 246), border=1, shadow=SMALL)
        flat(c, [Thick(476, 86, 500, 78, 3), Thick(420, 92, 400, 100, 2)], (40, 40, 46))
        flat(c, Circ(502, 77, 3), (220, 50, 50))
    # bamboo walls left and right
    for k, x in enumerate((20, 70, 120, 790, 840, 890)):
        bamboo(c, x, 420, -10, 16 + (k % 2) * 4, col=(130, 180, 100), seed=2653 + k)
    for k, x in enumerate((45, 860, 330, 590)):
        bamboo(c, x, 420, 60 if k < 2 else 180, 20, col=(100, 160, 84), seed=2660 + k)
    # ground
    c.rect(0, 380, W, H, (150, 186, 110))
    layer(c, 390, [(8, 0.02, 0.6), (4, 0.06, 1.0)], (140, 178, 104))
    # stream with koi (bottom centre)
    flat(c, Ell(470, 530, 200, 46), (120, 176, 196))
    flat(c, [Thick(330, 520, 380, 520, 1.6), Thick(520, 545, 580, 545, 1.6), Thick(600, 512, 640, 512, 1.6)], (170, 210, 226))
    fish(c, 420, 528, 1.6, (240, 120, 50) if "koi" not in d else (250, 246, 236), fin=(250, 250, 246))
    fish(c, 560, 520, 1.3, (250, 246, 236), right=False, fin=(240, 120, 50))
    # big panda munching (left middle)
    panda(c, 240, 480, 1.6)
    if "leaf" not in d:
        flat(c, Thick(262, 420, 300, 360, 4), (110, 160, 80))
        flat(c, [Poly([(296, 366), (336, 352), (344, 362), (310, 370)]), Poly([(290, 376), (324, 380), (328, 392), (296, 386)]),
                 Poly([(300, 360), (316, 330), (326, 334), (310, 362)])], (120, 180, 90))
    # cub on a rock (right middle)
    rock(c, 690, 480, 2.4, col=(160, 160, 150))
    if "cub" not in d:
        panda(c, 690, 434, 0.95, face=-1)
    # stone lantern (left front)
    stone = (176, 176, 166) if "stone" not in d else (200, 140, 96)
    piece(c, [RRect(56, 560, 116, 576, 2), RRect(74, 520, 98, 560, 2), RRect(60, 496, 112, 522, 3), Poly([(48, 498), (124, 498), (86, 474)])], stone,
          border=1.2, shadow=PROP)
    flat(c, RRect(76, 502, 96, 516, 2), (250, 220, 140))
    # bamboo shoots (right front)
    if "shoot" not in d:
        for x, h in ((790, 60), (826, 44), (858, 70)):
            piece(c, Poly([(x - 14, 590), (x + 14, 590), (x, 590 - h)]), (190, 160, 90), border=1.2, shadow=SMALL)
            flat(c, [Thick(x - 9, 576, x + 9, 572, 2), Thick(x - 5, 590 - h * 0.5, x + 5, 590 - h * 0.55, 2)], (150, 120, 60))
    # grass tufts
    for x in (180, 380, 640, 730):
        flat(c, [Poly([(x, 596), (x + 4, 570), (x + 8, 596)]), Poly([(x + 6, 596), (x + 14, 576), (x + 14, 596)])], (110, 160, 84))


L265_ELEMENTS = [
    bird_el("bird", 300, 36, s=8, speed=14),
    cloud_el("mist", 330, 236, 0.5, 6, col=(240, 244, 236)),
    E("leaf1", lambda c, m: flat(c, Poly([(580, 190), (600, 186), (604, 192), (586, 196)]), (140, 190, 100)), pivot=(592, 191),
      anim=dict(driftVelocity=(-8, 34), driftLength=110, driftFade=True, swingAngle=40, swingSpeed=1.2)),
    E("leaf2", lambda c, m: flat(c, Poly([(380, 230), (400, 226), (404, 232), (386, 236)]), (140, 190, 100)), pivot=(392, 231),
      anim=dict(driftVelocity=(6, 30), driftLength=100, driftFade=True, swingAngle=40, swingSpeed=1.0, phase=0.5)),
    E("ripple", lambda c, m: c.ellipse_ring(510, 560, 22, 5, 1.6, (180, 220, 234)), pivot=(510, 560), anim=dict(stretch=(0.5, 0.5), scaleSpeed=1.2)),
]

L265_DIFFS = [
    ("roof", 150, 136, 0),
    ("crane", 450, 86, 0),
    ("sun", 790, 80, 0),
    ("leaf", 312, 370, 0),
    ("cub", 690, 380, 0),
    ("stone", 86, 525, 0),
    ("koi", 418, 528, 0),
    ("shoot", 826, 560, 0),
]


# =================================================================== Level 266 aquarium
WATER = (40, 110, 160)


def l266_bg(c, d):
    c.rect(0, 0, W, H, (30, 40, 70))
    # tank
    c.gradient(20, 430, (60, 150, 200), (30, 80, 130))
    for x in (40, 230, 560, 760):
        soft_union(c, [Poly([(x, 20), (x + 60, 20), (x + 140, 430), (x + 40, 430)])], (160, 220, 240), 0.12, spread=20)
    # sand and rocks
    piece(c, hill_strip(380, [(10, 0.02, 0.6), (6, 0.05, 1.0)], bottom=430), (220, 200, 150), shadow=LAYER)
    for x, s in ((60, 2.0), (520, 1.6), (850, 2.2)):
        rock(c, x, 420, s, col=(110, 120, 130))
    # kelp
    for x in (30, 250, 600, 880):
        for k in range(3):
            flat(c, Thick(x + k * 10, 430, x + k * 10 + 14 * math.sin(k), 260 - k * 30, 5), (60, 140, 90))
    # coral (left)
    coral = (240, 120, 120) if "coral" not in d else (240, 200, 90)
    piece(c, [Thick(120, 410, 120, 340, 8), Thick(120, 370, 90, 330, 6), Thick(120, 360, 150, 320, 6), Thick(150, 320, 160, 300, 5), Thick(90, 330, 80, 312, 5)],
          coral, border=1, shadow=SMALL)
    # treasure chest (centre bottom of the tank)
    piece(c, RRect(410, 370, 490, 410, 3), (140, 90, 50), border=1.2, shadow=SMALL)
    lid = (180, 120, 60) if "chest" not in d else (60, 160, 160)
    piece(c, Poly([(406, 372), (494, 372), (486, 350), (414, 350)]), lid, border=1.2, shadow=SMALL)
    flat(c, RRect(444, 368, 456, 384, 2), (240, 200, 80))
    # manta ray (left top)
    ray = (90, 110, 150) if "ray" not in d else (170, 100, 150)
    piece(c, [Poly([(110, 110), (180, 80), (250, 110), (180, 140)]), Thick(180, 136, 196, 190, 2)], ray, border=1, shadow=SMALL)
    flat(c, [Circ(160, 104, 2), Circ(200, 104, 2)], (230, 240, 250))
    # shark (centre top)
    piece(c, [Ell(450, 150, 80, 22), Poly([(376, 150), (330, 124), (340, 150), (330, 176)]), Poly([(440, 130), (462, 96), (474, 132)]),
              Poly([(440, 166), (420, 190), (460, 170)])], (140, 156, 170), border=1, shadow=SMALL)
    flat(c, Ell(456, 160, 60, 10), (220, 230, 236))
    flat(c, Circ(506, 144, 3), INK)
    # turtle (right top)
    if "turtle" not in d:
        piece(c, [Ell(760, 120, 44, 26), Ell(810, 112, 12, 9), Ell(730, 140, 16, 6), Ell(780, 144, 16, 6), Ell(744, 98, 16, 6)], (120, 160, 90), border=1, shadow=SMALL)
        flat(c, [Ell(760, 120, 34, 20)], (90, 120, 70))
        flat(c, [Circ(750, 112, 6), Circ(770, 114, 6), Circ(760, 128, 6)], (130, 160, 90))
    # school of yellow fish (right middle)
    sch = (250, 210, 60) if "school" not in d else (240, 110, 160)
    for x, y in ((640, 250), (680, 240), (670, 280), (710, 266), (630, 290)):
        fish(c, x, y, 1.2, sch, right=False)
    fish(c, 300, 260, 1.3, (240, 140, 60), fin=(250, 250, 250))
    # window frame + rail
    for x in (0, 300, 600, 900):
        piece(c, RRect(x - 8, 10, x + 8, 440, 2), (60, 70, 90), shadow=PROP)
    piece(c, RRect(0, 6, W, 22, 2), (60, 70, 90), shadow=PROP)
    piece(c, RRect(0, 430, W, 452, 2), (70, 80, 100), shadow=PROP)
    # floor
    c.rect(0, 452, W, H, (40, 50, 80))
    for x in range(0, W, 60):
        flat(c, Thick(x, 452, x - 40, H, 1.4), (50, 62, 96))
    # info plaque (centre)
    plaque = (220, 200, 140) if "sign" not in d else (120, 200, 160)
    piece(c, [RRect(400, 470, 500, 510, 3), RRect(446, 510, 454, 560, 1)], plaque, border=1.2, shadow=SMALL)
    sign_box(c, 410, 478, 490, 502, plaque, 2661, glyph=(80, 70, 60), vertical=False)
    # visitors (silhouettes lit from the tank)
    modern(c, 300, 600, (90, 140, 210) if "child" not in d else (230, 90, 80), bottom=(50, 50, 70), hair=(60, 40, 30), h=2.0, style="twin")
    modern(c, 200, 600, (70, 90, 120), bottom=(40, 40, 60), hair=(30, 30, 34), h=2.6)
    modern(c, 610, 600, (120, 90, 140), bottom=(40, 40, 60), hair=(80, 60, 40), h=2.5, style="long")
    # bench (right)
    bench = (140, 100, 70) if "bench" not in d else (60, 130, 170)
    piece(c, [RRect(700, 540, 880, 556, 3), RRect(710, 556, 720, 590, 1), RRect(860, 556, 870, 590, 1)], bench, border=1.2, shadow=PROP)


L266_ELEMENTS = bubbles_el("bub", 530, 400, n=4, r=5, rise=(2, -30), length=150) + [
    E("swim", lambda c, m: fish(c, 300, 205, 1.0, (120, 200, 230), right=True), anim=drift_across(280, 320, 30)),
    E("glow", lambda c, m: soft_union(c, [Ell(450, 30, 300, 10)], (200, 240, 255), 0.25, spread=20), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=0.6)),
    E("kelp", lambda c, m: flat(c, Thick(880, 430, 870, 300, 4), (80, 160, 100)), pivot=(880, 430), anim=dict(swingAngle=6, swingSpeed=0.6)),
]

L266_DIFFS = [
    ("ray", 180, 112, 0),
    ("turtle", 765, 120, 0),
    ("coral", 120, 360, 0),
    ("chest", 450, 362, 0),
    ("school", 670, 266, 0),
    ("sign", 450, 495, 0),
    ("child", 300, 540, 0),
    ("bench", 790, 556, 0),
]


# =================================================================== Level 267 natural history museum
BONE = (236, 226, 200)


def l267_bg(c, d):
    c.rect(0, 0, W, H, (226, 214, 190))
    # arched skylight (centre top)
    sky_col = (170, 210, 240) if "window" not in d else (250, 200, 140)
    piece(c, Poly([(540, 130)] + [(450 + 90 * math.cos(math.pi * k / 12), 60 - 50 * math.sin(math.pi * k / 12)) for k in range(13)] + [(360, 130)]), (200, 186, 160),
          border=1.5, shadow=PROP)
    flat(c, Poly([(528, 126)] + [(450 + 78 * math.cos(math.pi * k / 12), 62 - 42 * math.sin(math.pi * k / 12)) for k in range(13)] + [(372, 126)]), sky_col)
    flat(c, [Thick(450, 20, 450, 126, 3), Thick(372, 80, 528, 80, 3)], (200, 186, 160))
    # columns
    for x in (40, 300, 600, 860):
        piece(c, [RRect(x - 22, 40, x + 22, 470, 2), RRect(x - 30, 30, x + 30, 46, 2), RRect(x - 30, 456, x + 30, 472, 2)], (240, 232, 214), border=1.5, shadow=PROP)
        for k in (-10, 0, 10):
            flat(c, Thick(x + k, 50, x + k, 450, 1.2), (220, 210, 190))
    # banners (left)
    for k, x in enumerate((110, 200)):
        col = [(170, 60, 60), (60, 100, 150)][k]
        if k == 0 and "banner" in d:
            col = (90, 150, 80)
        piece(c, Poly([(x - 30, 60), (x + 30, 60), (x + 30, 200), (x, 180), (x - 30, 200)]), col, border=1.2, shadow=SMALL)
        flat(c, Circ(x, 110, 14), lit(col, 1.3))
    # hanging flying reptile skeleton (right top)
    flat(c, [Thick(720, 0, 730, 90, 1), Thick(800, 0, 790, 90, 1)], (90, 90, 100))
    if "ptero" not in d:
        piece(c, [Poly([(650, 130), (700, 96), (760, 92), (740, 112)]), Poly([(870, 130), (820, 96), (760, 92), (780, 112)]), Ell(760, 104, 18, 9),
                  Poly([(772, 98), (830, 80), (836, 88), (790, 106)]), Poly([(760, 84), (744, 64), (770, 86)])], BONE, border=1, shadow=SMALL)
        for k in range(4):
            flat(c, [Thick(676 + k * 18, 118 - k * 6, 690 + k * 18, 104 - k * 5, 2), Thick(844 - k * 18, 118 - k * 6, 830 - k * 18, 104 - k * 5, 2)], lit(BONE, 0.8))
        flat(c, Circ(796, 92, 3), (120, 110, 100))
    # dinosaur skeleton (centre)
    piece(c, RRect(250, 430, 720, 456, 3), (120, 110, 100), border=1.5, shadow=PROP)
    spine = [(260, 420), (320, 330), (380, 290), (450, 270), (520, 280), (580, 250), (620, 220)]
    for (x0, y0), (x1, y1) in zip(spine, spine[1:]):
        piece(c, Thick(x0, y0, x1, y1, 7), BONE, border=1, shadow=SMALL)
    for x, y in ((400, 284), (430, 276), (460, 272), (490, 274)):
        flat(c, [Thick(x, y, x - 6, y + 50, 3)], lit(BONE, 0.9))
    for x0, y0 in ((410, 284), (500, 278)):
        piece(c, [Thick(x0, y0, x0 - 10, y0 + 80, 7), Thick(x0 - 10, y0 + 80, x0, 430, 6)], BONE, border=1, shadow=SMALL)
    skull = BONE if "skull" not in d else (200, 150, 90)
    piece(c, [Poly([(606, 206), (660, 200), (690, 220), (676, 240), (620, 240)]), Poly([(630, 240), (680, 240), (670, 254), (636, 252)])], skull, border=1.2,
          shadow=SMALL)
    flat(c, Circ(640, 218, 7), (120, 110, 100))
    for k in range(5):
        flat(c, Thick(640 + k * 8, 240, 640 + k * 8, 248, 2), (250, 250, 240))
    # floor
    c.rect(0, 472, W, H, (190, 170, 140))
    for x in range(0, W, 60):
        for y in range(472, H, 40):
            if (x // 60 + y // 40) % 2:
                flat(c, RRect(x, y, x + 60, y + 40, 0), (200, 180, 150))
    # display case with a gem (left middle)
    piece(c, RRect(80, 360, 200, 470, 2), (130, 100, 70), border=1.5, shadow=PROP)
    flat(c, RRect(90, 300, 190, 362, 2), (220, 236, 240))
    gem = (90, 160, 220) if "gem" not in d else (220, 80, 120)
    piece(c, Poly([(120, 340), (140, 316), (160, 316), (180, 340), (150, 356)]), gem, border=1, shadow=None)
    # case with a fossil (right middle)
    piece(c, RRect(720, 380, 840, 470, 2), (130, 100, 70), border=1.5, shadow=PROP)
    flat(c, RRect(730, 320, 830, 382, 2), (220, 236, 240))
    c.ellipse_ring(780, 352, 22, 22, 6, (180, 150, 110))
    flat(c, Circ(780, 352, 8), (180, 150, 110))
    # stanchions + rope
    for x in (290, 680):
        piece(c, [RRect(x - 4, 480, x + 4, 540, 1), Ell(x, 542, 14, 4)], (200, 170, 80), shadow=SMALL)
    flat(c, Thick(290, 490, 680, 490, 3), (170, 50, 60))
    # visitors
    modern(c, 300, 600, (240, 200, 60) if "kid" not in d else (90, 160, 220), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.1)
    hx, hy = modern(c, 760, 600, (60, 110, 90), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.6, glasses=True)
    if "cap" not in d:
        piece(c, [Ell(hx, hy - 10, 18, 7), RRect(hx - 4, hy - 12, hx + 24, hy - 6, 2)], (200, 80, 60), shadow=SMALL)
    modern(c, 460, 600, (200, 120, 150), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.4, style="long")


L267_ELEMENTS = [
    E("sway", lambda c, m: flat(c, Thick(110, 200, 110, 230, 3), (220, 200, 120)), pivot=(110, 200), anim=dict(swingAngle=8, swingSpeed=0.6)),
    E("dust", lambda c, m: soft_union(c, [Poly([(400, 130), (500, 130), (560, 420), (340, 420)])], (255, 250, 230), 0.12, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.5)),
    E("guide", lambda c, m: modern(c, 560, 600, (60, 90, 140), bottom=(40, 40, 50), hair=(60, 40, 30), h=2.3), pivot=(560, 600),
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.12)),
]

L267_DIFFS = [
    ("banner", 110, 130, 0),
    ("window", 450, 80, 0),
    ("ptero", 760, 100, 0),
    ("skull", 650, 226, 0),
    ("gem", 150, 336, 0),
    ("kid", 300, 540, 0),
    ("cap", 770, 485, 0),
]


# =================================================================== Level 268 art studio
def easel(c, x, base, w, h, art):
    piece(c, [Thick(x - w * 0.4, base, x, base - h - 40, 4), Thick(x + w * 0.4, base, x, base - h - 40, 4), Thick(x, base - h - 30, x + 6, base, 3)],
          (160, 110, 70), shadow=PROP)
    piece(c, RRect(x - w / 2 - 6, base - h - 30, x + w / 2 + 6, base - 46, 2), (250, 248, 240), border=1.5, shadow=PROP)
    art(c, x - w / 2, base - h - 24, x + w / 2, base - 52)
    piece(c, RRect(x - w / 2 - 10, base - 50, x + w / 2 + 10, base - 42, 2), (160, 110, 70), shadow=SMALL)


def l268_bg(c, d):
    c.rect(0, 0, W, 440, (238, 230, 214))
    planks(c, 440, (180, 140, 100), (160, 120, 84), seed=2681)
    # big window (centre top)
    piece(c, RRect(300, 30, 600, 250, 3), (250, 250, 246), border=1.5, shadow=PROP)
    flat(c, RRect(312, 42, 588, 238, 2), (180, 214, 236))
    flat(c, Poly([(312, 238), (312, 200), (400, 186), (500, 196), (588, 184), (588, 238)]), (150, 196, 140))
    tree_round(c, 360, 230, 1.0)
    flat(c, [Thick(450, 42, 450, 238, 4), Thick(312, 140, 588, 140, 4)], (250, 250, 246))
    piece(c, RRect(290, 246, 610, 260, 2), (250, 250, 246), shadow=PROP)
    pot_plant(c, 540, 248, 1.2, (220, 120, 80) if "pot" not in d else (90, 140, 210), bloom=(240, 90, 120))
    # framed painting on wall (left)
    fr = (200, 160, 70) if "frame" not in d else (80, 80, 90)
    piece(c, RRect(40, 50, 220, 180, 3), fr, border=1.5, shadow=PROP)
    flat(c, RRect(54, 64, 206, 166, 2), (120, 170, 210))
    flat(c, Poly([(54, 166), (120, 100), (170, 150), (206, 120), (206, 166)]), (100, 140, 90))
    # pinned sketches (left middle)
    for k, (x, y) in enumerate(((50, 220), (130, 210), (210, 226))):
        piece(c, RRect(x, y, x + 64, y + 80, 1), (250, 248, 240), border=1, shadow=SMALL)
        flat(c, Circ(x + 32, y + 4, 4), [(220, 70, 70), (60, 120, 200), (250, 200, 60)][k])
        flat(c, [Thick(x + 12, y + 60, x + 30, y + 26, 1.6), Thick(x + 30, y + 26, x + 52, y + 56, 1.6), Ell(x + 32, y + 44, 10, 8)], (120, 110, 100))
    # shelf of paint jars (right)
    piece(c, RRect(660, 150, 880, 164, 2), (160, 110, 70), shadow=PROP)
    for k, x in enumerate(range(680, 880, 40)):
        col = [(220, 70, 70), (250, 200, 60), (60, 120, 200), (90, 170, 90), (200, 120, 200)][k]
        if k == 2 and "jar" in d:
            col = (250, 140, 40)
        piece(c, [RRect(x - 14, 110, x + 14, 150, 4), RRect(x - 12, 102, x + 12, 112, 2)], col, border=1, shadow=SMALL)
    # plaster bust on a stand (right middle)
    piece(c, RRect(740, 330, 820, 450, 2), (220, 214, 200), border=1.5, shadow=PROP)
    bust = (246, 244, 236) if "bust" not in d else (200, 150, 110)
    piece(c, [Ell(780, 316, 34, 16), RRect(770, 286, 790, 310, 3), Ell(782, 268, 18, 22)], bust, border=1.2, shadow=SMALL)
    flat(c, Ell(778, 252, 18, 10), lit(bust, 0.9))
    # easel with the painting in progress (centre)

    def art(c, x0, y0, x1, y1):
        flat(c, RRect(x0, y0, x1, y1, 0), (190, 220, 240))
        flat(c, Poly([(x0, y1), (x0 + 60, y0 + 60), (x0 + 110, y1 - 30), (x1, y0 + 80), (x1, y1)]), (120, 160, 110))
        flat(c, Circ(x1 - 34, y0 + 30, 16), (250, 200, 80) if "canvas" not in d else (230, 90, 80))
    easel(c, 450, 520, 150, 150, art)
    # small easel with a portrait (left)

    def art2(c, x0, y0, x1, y1):
        flat(c, RRect(x0, y0, x1, y1, 0), (200, 170, 140))
        flat(c, [Ell((x0 + x1) / 2, y0 + 50, 20, 26), Ell((x0 + x1) / 2, y1 + 4, 34, 22)], (240, 210, 180))
    easel(c, 160, 480, 100, 120, art2)
    # painter with beret
    hx, hy = modern(c, 300, 590, (90, 120, 160), bottom=(60, 60, 70), hair=(60, 40, 30), h=2.4)
    beret = (180, 40, 60) if "beret" not in d else (40, 40, 50)
    piece(c, [Ell(hx, hy - 12, 20, 8), Circ(hx + 4, hy - 20, 3)], beret, shadow=SMALL)
    piece(c, Ell(250, 500, 30, 18), (220, 190, 140), border=1, shadow=SMALL)
    for k, col in enumerate([(220, 70, 70), (250, 200, 60), (60, 120, 200), (250, 250, 250)]):
        flat(c, Circ(236 + k * 10, 494 + (k % 2) * 8, 4), col)
    # still-life table (right front)
    piece(c, [RRect(620, 500, 880, 516, 3), RRect(640, 516, 652, 596, 2), RRect(848, 516, 860, 596, 2)], (150, 100, 70), border=1.2, shadow=PROP)
    piece(c, Poly([(600, 502), (900, 502), (890, 560), (610, 560)]), (240, 236, 226), shadow=SMALL)
    piece(c, Ell(700, 490, 44, 14), (240, 240, 236), border=1, shadow=SMALL)
    fruit = (220, 60, 60) if "fruit" not in d else (140, 200, 70)
    flat(c, [Circ(686, 478, 14), Circ(712, 480, 13)], fruit)
    flat(c, Circ(700, 466, 12), (250, 200, 60))
    piece(c, [Ell(820, 470, 18, 26), RRect(814, 430, 826, 450, 2)], (90, 140, 120), border=1, shadow=SMALL)
    # rags + bucket of brushes (left front)
    piece(c, Poly([(60, 590), (100, 590), (106, 540), (54, 540)]), (150, 160, 170), border=1.2, shadow=SMALL)
    for k in range(4):
        flat(c, Thick(70 + k * 8, 540, 66 + k * 10, 510, 2), (160, 110, 70))


L268_ELEMENTS = [
    E("curtain", lambda c, m: flat(c, Poly([(300, 30), (330, 30), (322, 250), (296, 250)]), (220, 120, 100)), pivot=(315, 30), anim=dict(swingAngle=2, swingSpeed=0.4)),
    E("brush", lambda c, m: flat(c, Thick(330, 470, 376, 430, 3), (160, 110, 70)), pivot=(330, 470), anim=dict(swingAngle=10, swingSpeed=1.0)),
    E("sun", lambda c, m: soft_union(c, [Poly([(320, 240), (580, 240), (660, 440), (260, 440)])], (255, 246, 220), 0.12, spread=20), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=0.4)),
]

L268_DIFFS = [
    ("frame", 130, 115, 0),
    ("pot", 540, 230, 0),
    ("jar", 760, 128, 0),
    ("bust", 780, 290, 0),
    ("canvas", 491, 376, 0),
    ("beret", 302, 460, 0),
    ("fruit", 700, 478, 0),
]


# =================================================================== Level 269 sushi bar
def l269_bg(c, d):
    c.rect(0, 0, W, 400, (226, 206, 170))
    for x in range(0, W, 60):
        flat(c, Thick(x, 0, x, 400, 2), (200, 176, 140))
    # beam + noren curtain (left top)
    piece(c, RRect(0, 0, W, 24, 0), (120, 80, 50), shadow=PROP)
    noren = (40, 60, 110) if "noren" not in d else (170, 50, 50)
    for k in range(3):
        piece(c, RRect(30 + k * 64, 24, 88 + k * 64, 130, 2), noren, border=1.2, shadow=SMALL)
    flat(c, Circ(126, 76, 18), (250, 250, 246))
    # menu tags on the wall (centre)
    for k, x in enumerate(range(300, 620, 40)):
        col = (250, 246, 230)
        if k == 3 and "tag" in d:
            col = (240, 120, 120)
        piece(c, RRect(x, 50, x + 30, 150, 2), col, border=1, shadow=SMALL)
        for j in range(4):
            flat(c, Thick(x + 15, 62 + j * 20, x + 15, 74 + j * 20, 3), (60, 50, 50))
    # red lanterns (right)
    for k, x in enumerate((700, 820)):
        col = (220, 60, 50) if not (k == 1 and "lantern" in d) else (250, 246, 236)
        flat(c, Thick(x, 24, x, 50, 2), (60, 50, 50))
        piece(c, [Ell(x, 90, 34, 40), RRect(x - 18, 46, x + 18, 54, 2), RRect(x - 18, 126, x + 18, 134, 2)], col, border=1.2, shadow=SMALL)
        for j in range(-2, 3):
            flat(c, Thick(x - 32, 90 + j * 14, x + 32, 90 + j * 14, 1), lit(col, 0.8))
    # back shelf with sake bottles and plates
    piece(c, RRect(260, 200, 660, 212, 2), (150, 100, 60), shadow=PROP)
    for k, x in enumerate(range(280, 660, 46)):
        piece(c, [RRect(x - 10, 160, x + 10, 200, 4), RRect(x - 4, 146, x + 4, 162, 2)], [(240, 236, 220), (90, 120, 90), (70, 60, 90)][k % 3], border=1, shadow=SMALL)
    # chef behind the counter (centre)
    hx, hy = modern(c, 450, 360, (250, 250, 246), bottom=(60, 60, 70), hair=(30, 30, 34), h=2.4)
    band = (60, 80, 140) if "chef" not in d else (220, 60, 50)
    piece(c, [RRect(hx - 20, hy - 22, hx + 20, hy - 8, 3), Poly([(hx - 20, hy - 18), (hx - 34, hy - 26), (hx - 32, hy - 10)])], band, shadow=SMALL)
    # counter with a glass fish case
    piece(c, RRect(0, 330, W, 360, 2), (210, 170, 120), border=1.5, shadow=PROP)
    flat(c, RRect(140, 290, 760, 332, 3), (220, 236, 240))
    for k, x in enumerate(range(170, 740, 80)):
        col = [(230, 90, 80), (250, 160, 120), (240, 240, 230), (200, 80, 90)][k % 4]
        if k == 5 and "fish" in d:
            col = (250, 210, 80)
        flat(c, Poly([(x - 30, 326), (x + 30, 326), (x + 24, 306), (x - 24, 306)]), col)
        flat(c, Thick(x - 20, 316, x + 20, 316, 1.4), lit(col, 1.2))
    piece(c, RRect(0, 360, W, 470, 0), (150, 100, 60), shadow=LAYER)
    for x in range(0, W, 90):
        flat(c, Thick(x, 360, x, 470, 2), (130, 86, 50))
    # plates on the counter top
    piece(c, Ell(250, 346, 46, 10), (250, 250, 246), border=1, shadow=SMALL)
    sushi = (230, 80, 70) if "plate" not in d else (250, 210, 70)
    for x in (230, 270):
        piece(c, [RRect(x - 14, 330, x + 14, 344, 4)], (250, 250, 246), shadow=None)
        flat(c, RRect(x - 16, 324, x + 16, 334, 4), sushi)
    piece(c, Ell(650, 346, 40, 10), (40, 40, 46), border=1, shadow=SMALL)
    for x in (634, 664):
        piece(c, Circ(x, 336, 10), (40, 50, 40), shadow=None)
        flat(c, Circ(x, 336, 5), (240, 120, 80))
    # floor
    c.rect(0, 470, W, H, (180, 160, 130))
    for x in range(0, W, 40):
        flat(c, Thick(x, 470, x, H, 1), (166, 146, 118))
    # stools + customers
    for k, x in enumerate((140, 450, 760)):
        col = (90, 60, 40) if not (k == 2 and "stool" in d) else (200, 60, 60)
        piece(c, [Ell(x, 530, 40, 10), RRect(x - 6, 530, x + 6, 596, 2), Ell(x, 596, 30, 6)], col, shadow=PROP)
    modern(c, 290, 600, (200, 120, 90), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.6)
    modern(c, 600, 600, (90, 150, 120), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.5, style="long")
    # tea cup (right)
    tea = (110, 150, 90) if "tea" not in d else (60, 110, 170)
    piece(c, RRect(830, 300, 862, 332, 4), tea, border=1.2, shadow=SMALL)


L269_ELEMENTS = steam("stm", 846, 296, n=3) + [
    E("knife", lambda c, m: flat(c, Thick(470, 320, 510, 306, 3), (210, 214, 220)), pivot=(470, 320), anim=dict(swingAngle=10, swingSpeed=1.6)),
    E("sway", lambda c, m: flat(c, Thick(700, 134, 700, 160, 3), (250, 200, 60)), pivot=(700, 134), anim=dict(swingAngle=14, swingSpeed=0.8)),
]

L269_DIFFS = [
    ("noren", 110, 78, 0),
    ("tag", 435, 100, 0),
    ("lantern", 820, 90, 0),
    ("chef", 452, 236, 0),
    ("fish", 570, 316, 0),
    ("plate", 250, 330, 0),
    ("stool", 760, 560, 0),
    ("tea", 846, 316, 0),
]


# =================================================================== Level 270 pet shop
def l270_bg(c, d):
    c.rect(0, 0, W, 430, (220, 236, 230))
    planks(c, 430, (200, 170, 130), (180, 150, 114), seed=2701)
    # paw sign (centre top)
    sign = (240, 160, 60) if "sign" not in d else (120, 170, 230)
    piece(c, RRect(360, 20, 540, 80, 10), sign, border=1.5, shadow=PROP)
    flat(c, [Circ(400, 56, 12), Circ(386, 38, 5), Circ(398, 32, 5), Circ(412, 36, 5)], (250, 250, 246))
    sign_box(c, 430, 36, 520, 64, sign, 2702, vertical=False)
    # fish tanks on a shelf (left)
    piece(c, RRect(20, 210, 300, 226, 2), (160, 120, 80), shadow=PROP)
    for k, x in enumerate((30, 160)):
        piece(c, RRect(x, 110, x + 120, 210, 3), (90, 100, 110), border=1.2, shadow=PROP)
        flat(c, RRect(x + 6, 116, x + 114, 204, 2), (140, 200, 230))
        flat(c, RRect(x + 6, 190, x + 114, 204, 0), (220, 200, 150))
        col = [(240, 120, 50), (90, 200, 220)][k]
        if k == 0 and "tank" in d:
            col = (220, 70, 160)
        fish(c, x + 50, 150, 1.4, col)
        fish(c, x + 80, 172, 1.0, col, right=False)
    # hanging leashes (right top)
    piece(c, RRect(640, 40, 880, 52, 2), (150, 150, 160), shadow=SMALL)
    for k, x in enumerate(range(660, 880, 40)):
        col = [(220, 70, 70), (60, 120, 200), (250, 200, 60), (90, 170, 90), (200, 120, 200), (240, 140, 60)][k]
        if k == 2 and "leash" in d:
            col = (60, 60, 70)
        flat(c, Thick(x, 52, x, 170, 5), col)
        c.ellipse_ring(x, 180, 12, 12, 5, col)
    # parrot cage (centre)
    flat(c, Thick(450, 80, 450, 110, 2), (90, 90, 100))
    piece(c, Ell(450, 112, 14, 6), (200, 170, 80), shadow=None)
    for k in range(-4, 5):
        flat(c, Thick(450 + k * 12, 120 + abs(k) * 4, 450 + k * 13, 250, 1.4), (200, 170, 80))
    piece(c, Ell(450, 252, 60, 10), (200, 170, 80), shadow=SMALL)
    flat(c, Thick(420, 210, 480, 210, 3), (150, 110, 70))
    par = (60, 180, 90) if "parrot" not in d else (240, 90, 60)
    piece(c, [Ell(450, 186, 14, 22), Circ(454, 162, 11), Poly([(442, 204), (458, 204), (450, 240)])], par, border=1, shadow=None)
    flat(c, [Poly([(462, 160), (472, 166), (462, 170)])], (250, 200, 60))
    flat(c, Circ(457, 159, 2), INK)
    # cat tree (left middle)
    piece(c, [RRect(222, 270, 238, 430, 2)], (220, 200, 160), shadow=PROP)
    for y, w in ((270, 50), (340, 40), (420, 60)):
        piece(c, RRect(230 - w, y - 10, 230 + w, y + 4, 4), (180, 130, 100), border=1.2, shadow=SMALL)
    piece(c, Circ(190, 380, 10), (240, 90, 90), shadow=SMALL)
    flat(c, Thick(190, 344, 190, 370, 1.4), (90, 90, 100))
    # dog poster (right middle)
    piece(c, RRect(680, 214, 860, 310, 3), (250, 246, 236), border=1.5, shadow=PROP)
    flat(c, RRect(690, 224, 850, 300, 2), (250, 220, 150))
    piece(c, [Ell(760, 280, 36, 18), Circ(792, 258, 16), Ell(804, 248, 6, 12)], (200, 140, 80), shadow=None)
    flat(c, Circ(796, 256, 2), INK)
    # pet food bags (right middle)
    for k, x in enumerate((660, 740, 820)):
        col = [(220, 90, 80), (90, 140, 200), (250, 200, 80)][k]
        if k == 0 and "bag" in d:
            col = (120, 180, 100)
        piece(c, Poly([(x - 34, 420), (x + 34, 420), (x + 30, 330), (x - 30, 330)]), col, border=1.5, shadow=PROP)
        flat(c, Circ(x, 370, 14), (250, 250, 246))
    # counter + shopkeeper (centre middle)
    hx, hy = modern(c, 450, 380, (120, 170, 120), bottom=(60, 70, 100), hair=(90, 60, 40), h=1.9, style="long")
    piece(c, RRect(330, 360, 570, 440, 3), (190, 140, 90), border=1.5, shadow=PROP)
    # hamster cage on the counter
    piece(c, RRect(360, 310, 440, 362, 3), (240, 240, 236), border=1.2, shadow=SMALL)
    for x in range(366, 440, 10):
        flat(c, Thick(x, 314, x, 360, 1), (180, 180, 190))
    if "hamster" not in d:
        piece(c, [Ell(378, 350, 14, 9), Circ(391, 344, 7)], (230, 170, 90), border=1, shadow=None)
        flat(c, Circ(395, 342, 1.6), INK)
    # puppy pen (left front)
    piece(c, RRect(30, 500, 300, 580, 3), (230, 220, 200), border=1.2, shadow=PROP)
    for x in range(40, 300, 22):
        flat(c, Thick(x, 470, x, 520, 3), (200, 180, 140))
    flat(c, Thick(30, 470, 300, 470, 4), (200, 180, 140))
    if "puppy" not in d:
        piece(c, [Ell(130, 530, 34, 18), Circ(170, 510, 16), Ell(182, 500, 6, 12), Ell(158, 500, 6, 12)], (220, 180, 120), border=1.2, shadow=SMALL)
        flat(c, [Circ(176, 510, 2), Circ(186, 516, 3)], INK)
    piece(c, [Ell(240, 540, 30, 14), Circ(266, 526, 12)], (250, 250, 246), border=1.2, shadow=SMALL)
    flat(c, [Ell(240, 534, 10, 6)], (60, 60, 70))
    # kitten basket (right front)
    piece(c, Poly([(700, 590), (860, 590), (880, 530), (680, 530)]), (190, 140, 80), border=1.5, shadow=PROP)
    for x in range(690, 880, 16):
        flat(c, Thick(x, 534, x + 4, 588, 1.4), (160, 110, 60))
    kit_col = (240, 160, 70) if "kitten" not in d else (90, 90, 100)
    piece(c, [Ell(780, 524, 36, 14), Circ(810, 506, 14), Poly([(800, 498), (802, 484), (810, 496)]), Poly([(814, 496), (820, 484), (824, 498)])], kit_col, border=1.2,
          shadow=SMALL)
    flat(c, [Circ(814, 504, 1.8)], INK)


L270_ELEMENTS = bubbles_el("bub", 220, 196, n=3, r=3, rise=(1, -20), length=70) + [
    E("tail", lambda c, m: flat(c, Thick(96, 528, 70, 510, 4), (220, 180, 120)), pivot=(96, 528), anim=dict(swingAngle=24, swingSpeed=2.4)),
    E("wheel", lambda c, m: [c.ellipse_ring(424, 336, 14, 14, 2, (200, 80, 80)), flat(c, [Thick(410, 336, 438, 336, 1.4), Thick(424, 322, 424, 350, 1.4)], (200, 80, 80))],
      pivot=(424, 336), anim=dict(rotateSpeed=90)),
    E("swing", lambda c, m: flat(c, Thick(450, 112, 450, 128, 2), (90, 90, 100)), pivot=(450, 112), anim=dict(swingAngle=4, swingSpeed=0.6)),
]

L270_DIFFS = [
    ("tank", 92, 160, 0),
    ("sign", 450, 50, 0),
    ("leash", 740, 130, 0),
    ("parrot", 450, 196, 0),
    ("bag", 660, 376, 0),
    ("hamster", 382, 346, 0),
    ("puppy", 150, 520, 0),
    ("kitten", 800, 510, 0),
]


# =================================================================== Level 271 barber shop
def barber_chair(c, x, base, seat):
    piece(c, [RRect(x - 10, base - 40, x + 10, base, 2), Ell(x, base, 34, 6)], (170, 170, 180), shadow=PROP)
    piece(c, [RRect(x - 34, base - 70, x + 34, base - 40, 6), RRect(x - 30, base - 150, x + 30, base - 66, 8)], seat, border=1.5, shadow=PROP)
    flat(c, [RRect(x - 40, base - 84, x - 30, base - 52, 2), RRect(x + 30, base - 84, x + 40, base - 52, 2)], (200, 200, 210))


def l271_bg(c, d):
    c.rect(0, 0, W, 300, (236, 236, 230))
    for x in range(0, W, 30):
        for y in range(300, 440, 30):
            flat(c, RRect(x, y, x + 30, y + 30, 0), (250, 250, 246) if (x // 30 + y // 30) % 2 else (60, 70, 90))
    flat(c, Thick(0, 300, W, 300, 4), (180, 60, 60))
    # clock (left top)
    clock = (60, 70, 90) if "clock" not in d else (200, 140, 60)
    piece(c, Circ(80, 80, 40), clock, border=1.5, shadow=PROP)
    flat(c, Circ(80, 80, 32), (250, 250, 246))
    flat(c, [Thick(80, 80, 80, 58, 3), Thick(80, 80, 96, 86, 3)], INK)
    # mirrors
    for k, x in enumerate((300, 600)):
        fr = (200, 160, 70) if not (k == 1 and "mirror" in d) else (60, 60, 70)
        piece(c, RRect(x - 90, 40, x + 90, 230, 10), fr, border=1.5, shadow=PROP)
        flat(c, RRect(x - 78, 52, x + 78, 218, 8), (200, 226, 236))
        flat(c, [Thick(x - 50, 70, x - 20, 110, 6), Thick(x + 20, 160, x + 50, 200, 6)], (230, 244, 250))
    # counter shelves under the mirrors
    piece(c, RRect(190, 240, 710, 260, 2), (250, 250, 246), border=1.2, shadow=PROP)
    for x, col in ((220, (90, 160, 220)), (250, (220, 90, 90)), (650, (90, 180, 120)), (680, (250, 200, 60))):
        piece(c, [RRect(x - 8, 210, x + 8, 240, 3), RRect(x - 3, 202, x + 3, 212, 1)], col, border=1, shadow=SMALL)
    # striped pole (right)
    piece(c, [RRect(820, 40, 860, 240, 18)], (250, 250, 246), border=1.5, shadow=PROP)
    stripe = (210, 50, 50) if "pole" not in d else (60, 110, 200)
    for y in range(50, 230, 30):
        flat(c, Poly([(822, y + 20), (858, y), (858, y + 10), (822, y + 30)]), stripe)
    piece(c, [Ell(840, 34, 22, 10), Ell(840, 246, 22, 10)], (200, 200, 210), shadow=SMALL)
    # towel stack (left middle)
    piece(c, RRect(30, 200, 150, 214, 2), (160, 120, 80), shadow=PROP)
    tw = (250, 250, 246) if "towel" not in d else (240, 180, 70)
    for k in range(3):
        piece(c, RRect(46, 170 - k * 22, 134, 196 - k * 22, 6), tw if k != 1 else (120, 190, 200), border=1, shadow=SMALL)
    # floor
    c.rect(0, 440, W, H, (200, 190, 176))
    # chairs + customer with a cape
    barber_chair(c, 300, 500, (180, 40, 50))
    barber_chair(c, 600, 500, (180, 40, 50) if "chair" not in d else (60, 60, 70))
    cape = (90, 140, 200) if "cape" not in d else (250, 250, 246)
    piece(c, Poly([(266, 440), (334, 440), (346, 360), (254, 360)]), cape, border=1.2, shadow=SMALL)
    flat(c, Circ(300, 346, 18), SKIN)
    flat(c, Ell(298, 334, 18, 8), (90, 60, 40))
    # barber
    modern(c, 380, 520, (250, 250, 246), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.6)
    flat(c, [Thick(344, 400, 330, 370, 4)], SKIN)
    # waiting bench + magazine (right front)
    piece(c, [RRect(680, 540, 890, 556, 3), RRect(690, 556, 700, 596, 1), RRect(870, 556, 880, 596, 1)], (140, 100, 70), border=1.2, shadow=PROP)
    mag = (240, 120, 160) if "magazine" not in d else (120, 200, 120)
    piece(c, RRect(820, 526, 870, 542, 2), mag, border=1, shadow=SMALL)
    modern(c, 740, 540, (200, 160, 90), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.0)
    # plant (left front)
    if "plant" not in d:
        pot_plant(c, 90, 590, 2.4, (220, 120, 80))
    # hair clippings on floor
    for x in (260, 300, 330):
        flat(c, Thick(x, 536, x + 8, 530, 1.6), (90, 60, 40))


L271_ELEMENTS = [
    E("scissors", lambda c, m: flat(c, [Thick(330, 370, 316, 352, 2), Thick(330, 370, 312, 362, 2)], (180, 180, 190)), pivot=(330, 370),
      anim=dict(swingAngle=12, swingSpeed=3.0)),
    E("fan", lambda c, m: [flat(c, Thick(450, 20, 450 + 50 * math.cos(a), 20 + 8 * math.sin(a), 6), (200, 200, 210)) for a in (0, 2.09, 4.19)], pivot=(450, 20),
      anim=dict(stretch=(0.6, 0), scaleSpeed=2.0)),
    E("glint", lambda c, m: flat(c, Thick(560, 80, 590, 120, 4), (240, 250, 255)), pivot=(575, 100), anim=dict(twinkle=0.8, twinkleSpeed=0.6)),
]

L271_DIFFS = [
    ("clock", 80, 80, 0),
    ("towel", 90, 160, 0),
    ("mirror", 600, 135, 0),
    ("pole", 840, 140, 0),
    ("cape", 300, 400, 0),
    ("chair", 600, 420, 0),
    ("magazine", 845, 534, 0),
    ("plant", 90, 540, 0),
]


# =================================================================== Level 272 cafe
def l272_bg(c, d):
    c.rect(0, 0, W, 420, (90, 120, 110))
    for y in range(0, 420, 24):
        for x in range((y // 24 % 2) * 30, W, 60):
            flat(c, RRect(x + 1, y + 1, x + 59, y + 23, 2), (100, 132, 120))
    # chalk menu (left top)
    piece(c, RRect(30, 30, 260, 200, 4), (150, 110, 70), border=1.5, shadow=PROP)
    flat(c, RRect(40, 40, 250, 190, 2), (50, 56, 56))
    chalk = (250, 250, 246) if "menu" not in d else (250, 160, 180)
    piece(c, [RRect(70, 70, 110, 110, 6), Thick(110, 82, 122, 96, 4)], chalk, shadow=None)
    for k in range(4):
        flat(c, Thick(140, 70 + k * 30, 230, 70 + k * 30, 2), (220, 220, 214))
    flat(c, [Thick(60, 140, 120, 140, 2), Thick(60, 170, 110, 170, 2)], (220, 220, 214))
    # pendant lamps
    for k, x in enumerate((360, 540, 720)):
        flat(c, Thick(x, 0, x, 60, 2), (40, 40, 46))
        col = (250, 190, 70) if not (k == 1 and "lamp" in d) else (90, 170, 220)
        piece(c, Poly([(x - 30, 96), (x + 30, 96), (x + 16, 60), (x - 16, 60)]), col, border=1.2, shadow=SMALL)
    # shelf of cups + plant (right top)
    piece(c, RRect(640, 170, 880, 182, 2), (170, 120, 80), shadow=PROP)
    for x in (660, 700, 740):
        piece(c, RRect(x - 14, 144, x + 14, 170, 4), (250, 250, 246), border=1, shadow=SMALL)
    if "plant" not in d:
        pot_plant(c, 830, 170, 1.6, (240, 236, 226), kind="bush")
    # espresso machine on the counter (centre)
    mach = (200, 70, 60) if "machine" not in d else (80, 140, 190)
    piece(c, [RRect(380, 200, 520, 290, 6), RRect(390, 186, 510, 206, 3)], mach, border=1.5, shadow=PROP)
    flat(c, [RRect(400, 216, 500, 240, 3)], (220, 220, 226))
    flat(c, [RRect(410, 250, 430, 270, 2), RRect(470, 250, 490, 270, 2)], (60, 60, 70))
    # pastry case (right)
    piece(c, RRect(580, 230, 860, 300, 3), (240, 244, 246), border=1.5, shadow=PROP)
    for k, x in enumerate(range(610, 850, 60)):
        col = [(220, 160, 90), (250, 220, 180), (140, 90, 60), (240, 150, 170)][k]
        if k == 2 and "cake" in d:
            col = (150, 210, 150)
        piece(c, [RRect(x - 20, 262, x + 20, 292, 4)], col, shadow=None)
        flat(c, Ell(x, 262, 20, 5), lit(col, 1.15))
    # counter
    piece(c, RRect(0, 290, W, 420, 0), (170, 120, 80), shadow=LAYER)
    piece(c, RRect(0, 288, W, 304, 2), (220, 190, 150), shadow=SMALL)
    for x in range(0, W, 45):
        flat(c, Thick(x, 304, x, 420, 1.4), (150, 104, 70))
    # barista
    modern(c, 220, 290, (250, 250, 246), bottom=(40, 40, 50), hair=(60, 40, 30), h=1.8, style="long")
    # floor
    c.rect(0, 420, W, H, (200, 170, 130))
    planks(c, 420, (200, 170, 130), (180, 150, 112), seed=2721)
    # tables with customers
    for x0 in (180, 640):
        piece(c, [Ell(x0, 500, 90, 14), RRect(x0 - 6, 500, x0 + 6, 590, 2), Ell(x0, 592, 40, 6)], (240, 236, 226), border=1.2, shadow=PROP)
    modern(c, 80, 590, (200, 90, 90), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.4)
    modern(c, 760, 590, (90, 120, 180), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.4, style="long")
    cup = (250, 250, 246) if "cup" not in d else (240, 140, 60)
    piece(c, [RRect(150, 470, 180, 494, 4), Ell(165, 496, 20, 4)], cup, border=1, shadow=SMALL)
    lap = (180, 180, 190) if "laptop" not in d else (60, 60, 70)
    piece(c, [Poly([(600, 492), (680, 492), (670, 450), (610, 450)])], lap, border=1.2, shadow=SMALL)
    flat(c, Circ(640, 470, 5), (250, 250, 250))
    # bag on the floor (centre front)
    bag = (90, 130, 90) if "bag" not in d else (220, 180, 60)
    piece(c, [RRect(410, 540, 490, 590, 6), Thick(420, 540, 450, 510, 3), Thick(480, 540, 450, 510, 3)], bag, border=1.5, shadow=PROP)


L272_ELEMENTS = steam("stm", 165, 466, n=3) + steam("mach", 440, 182, n=2, r=8) + [
    E("swing", lambda c, m: flat(c, Thick(720, 96, 720, 104, 4), (255, 230, 150)), pivot=(720, 60), daynight="untinted", anim=dict(swingAngle=3, swingSpeed=0.5)),
    E("glow", lambda c, m: soft_union(c, [Circ(360, 100, 26), Circ(720, 100, 26)], (255, 230, 160), 0.3, spread=24), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=0.6)),
]

L272_DIFFS = [
    ("menu", 95, 92, 0),
    ("lamp", 540, 80, 0),
    ("plant", 830, 140, 0),
    ("machine", 450, 240, 0),
    ("cake", 730, 278, 0),
    ("cup", 165, 482, 0),
    ("laptop", 640, 472, 0),
    ("bag", 450, 555, 0),
]


# =================================================================== Level 273 laundromat
WASH_X = (90, 250, 410, 570, 730)


def l273_bg(c, d):
    c.rect(0, 0, W, 440, (210, 230, 240))
    for y in range(0, 440, 40):
        flat(c, Thick(0, y, W, y, 1), (196, 218, 230))
    # posters (left top)
    post = (250, 200, 80) if "poster" not in d else (240, 120, 160)
    piece(c, RRect(40, 30, 160, 140, 3), post, border=1.5, shadow=PROP)
    flat(c, [Circ(100, 74, 26)], (250, 250, 246))
    flat(c, Circ(100, 74, 14), (120, 180, 220))
    for k in range(2):
        flat(c, Thick(60, 112 + k * 12, 140, 112 + k * 12, 3), lit(post, 0.7))
    piece(c, RRect(200, 40, 300, 120, 3), (120, 200, 170), border=1.5, shadow=PROP)
    sign_box(c, 214, 54, 286, 106, (120, 200, 170), 2731, vertical=False)
    # clock (centre top)
    clock = (240, 90, 80) if "clock" not in d else (90, 90, 100)
    piece(c, Circ(450, 70, 34), clock, border=1.5, shadow=PROP)
    flat(c, Circ(450, 70, 26), (250, 250, 246))
    flat(c, [Thick(450, 70, 450, 52, 3), Thick(450, 70, 464, 76, 3)], INK)
    # shelf with detergent (right top)
    piece(c, RRect(620, 140, 880, 152, 2), (160, 120, 80), shadow=PROP)
    for k, x in enumerate(range(650, 880, 50)):
        col = [(90, 160, 230), (240, 140, 60), (120, 200, 120), (200, 100, 200), (250, 220, 80)][k]
        if k == 1 and "bottle" in d:
            col = (220, 60, 70)
        piece(c, [RRect(x - 16, 90, x + 16, 140, 6), RRect(x - 6, 80, x + 6, 92, 2)], col, border=1, shadow=SMALL)
        flat(c, RRect(x - 10, 106, x + 10, 124, 2), (250, 250, 246))
    # washers
    for k, x in enumerate(WASH_X):
        body = (246, 248, 250) if not (k == 4 and "machine" in d) else (250, 200, 210)
        piece(c, RRect(x - 70, 220, x + 70, 420, 6), body, border=1.5, shadow=PROP)
        flat(c, RRect(x - 70, 220, x + 70, 250, 6), (200, 210, 220))
        flat(c, [Circ(x - 46, 235, 6), RRect(x + 10, 230, x + 54, 240, 2)], (90, 100, 120))
        piece(c, Circ(x, 330, 50), (170, 180, 196), shadow=None)
        flat(c, Circ(x, 330, 40), (60, 70, 90))
    piece(c, RRect(818, 230, 890, 420, 4), (90, 100, 120), border=1.5, shadow=PROP)
    flat(c, [RRect(830, 250, 878, 290, 2), RRect(840, 310, 868, 330, 2)], (200, 220, 230))
    flat(c, RRect(836, 370, 872, 386, 2), (40, 40, 50))
    # floor
    c.rect(0, 440, W, H, (220, 214, 200))
    for x in range(0, W, 50):
        for y in range(440, H, 50):
            if (x // 50 + y // 50) % 2:
                flat(c, RRect(x, y, x + 50, y + 50, 0), (200, 194, 180))
    # folding table + shirt (centre front)
    piece(c, [RRect(320, 480, 600, 496, 3), RRect(330, 496, 340, 590, 2), RRect(580, 496, 590, 590, 2)], (190, 150, 110), border=1.2, shadow=PROP)
    shirt = (90, 140, 210) if "shirt" not in d else (240, 120, 60)
    piece(c, Poly([(380, 478), (450, 478), (460, 452), (440, 440), (390, 440), (370, 452)]), shirt, border=1, shadow=SMALL)
    piece(c, RRect(500, 456, 570, 478, 3), (250, 250, 246), border=1, shadow=SMALL)
    piece(c, RRect(504, 436, 566, 458, 3), (240, 200, 200), border=1, shadow=SMALL)
    modern(c, 470, 600, (200, 90, 120), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.0, style="long")
    # basket (left front)
    bk = (90, 160, 210) if "basket" not in d else (240, 200, 60)
    piece(c, Poly([(60, 590), (200, 590), (214, 500), (46, 500)]), bk, border=1.5, shadow=PROP)
    for x in range(62, 200, 18):
        flat(c, Thick(x, 510, x + 2, 580, 3), lit(bk, 0.8))
    flat(c, [Ell(100, 498, 30, 12), Ell(150, 494, 28, 10)], (250, 236, 220))
    # dropped sock (centre left floor)
    if "sock" not in d:
        piece(c, Poly([(250, 560), (270, 560), (270, 584), (298, 584), (298, 596), (250, 596)]), (240, 90, 90), border=1, shadow=SMALL)
    # plastic chair (right front)
    chair = (240, 160, 60) if "chair" not in d else (120, 120, 200)
    piece(c, [RRect(740, 480, 840, 500, 4), RRect(744, 420, 836, 482, 6), Thick(750, 500, 744, 590, 4), Thick(830, 500, 836, 590, 4)], chair, border=1.5, shadow=PROP)


def drum_el(k, x):
    cols = [(240, 120, 120), (120, 180, 230), (250, 220, 120), (150, 210, 150), (220, 160, 220)]

    def d(c, m):
        for j in range(3):
            a = j * 2.09 + k
            flat(c, Ell(x + 20 * math.cos(a), 330 + 20 * math.sin(a), 14, 9), cols[(k + j) % 5])
    return E("drum%d" % k, d, pivot=(x, 330), anim=dict(rotateSpeed=120 + k * 20))


L273_ELEMENTS = [drum_el(k, x) for k, x in enumerate(WASH_X)] + [
    E("glare", lambda c, m: [flat(c, Thick(x - 24, 300, x - 10, 290, 3), (230, 240, 250)) for x in WASH_X], daynight="untinted",
      anim=dict(twinkle=0.5, twinkleSpeed=0.5)),
    E("sway", lambda c, m: flat(c, Thick(460, 520, 470, 560, 3), SKIN), pivot=(460, 520), anim=dict(swingAngle=10, swingSpeed=0.8)),
]

L273_DIFFS = [
    ("poster", 100, 85, 0),
    ("clock", 450, 70, 0),
    ("bottle", 700, 112, 0),
    ("machine", 730, 300, 0),
    ("shirt", 415, 460, 0),
    ("basket", 130, 545, 0),
    ("sock", 274, 580, 0),
    ("chair", 790, 480, 0),
]


# =================================================================== Level 274 clock shop
def wall_clock(c, x, y, r, frame, face=(250, 246, 232)):
    piece(c, Circ(x, y, r), frame, border=1.5, shadow=PROP)
    flat(c, Circ(x, y, r * 0.8), face)
    for k in range(12):
        a = k * math.pi / 6
        flat(c, Circ(x + r * 0.66 * math.cos(a), y + r * 0.66 * math.sin(a), max(1.2, r * 0.05)), INK)


def hands_el(eid, x, y, r, speed):
    return E(eid, lambda c, m: flat(c, [Thick(x, y, x, y - r * 0.55, max(1.6, r * 0.08)), Thick(x, y, x + r * 0.4, y, max(1.6, r * 0.08))], INK), pivot=(x, y),
             anim=dict(rotateSpeed=speed))


def l274_bg(c, d):
    c.rect(0, 0, W, 440, (120, 70, 60))
    for x in range(0, W, 40):
        flat(c, Thick(x, 0, x, 440, 1.4), (110, 62, 54))
    # wall clocks
    wall_clock(c, 90, 90, 50, (200, 160, 70) if "round" not in d else (90, 140, 200))
    wall_clock(c, 230, 70, 34, (60, 60, 70))
    wall_clock(c, 230, 190, 30, (170, 120, 80))
    wall_clock(c, 600, 80, 40, (240, 236, 226))
    wall_clock(c, 720, 200, 30, (200, 90, 80))
    # square clock (right top)
    piece(c, RRect(790, 40, 880, 130, 6), (90, 60, 40), border=1.5, shadow=PROP)
    flat(c, Circ(835, 85, 34), (250, 246, 232))
    # cuckoo clock (centre top)
    roof = (90, 60, 40) if "cuckoo" not in d else (180, 60, 50)
    piece(c, [RRect(400, 70, 500, 180, 3)], (170, 120, 80), border=1.5, shadow=PROP)
    piece(c, Poly([(384, 76), (516, 76), (450, 24)]), roof, border=1.5, shadow=PROP)
    flat(c, RRect(436, 84, 464, 108, 4), (60, 40, 30))
    flat(c, Circ(450, 140, 26), (250, 246, 232))
    flat(c, [Ell(400, 190, 6, 12), Ell(500, 200, 6, 12)], (200, 170, 70))
    flat(c, [Thick(400, 180, 400, 190, 1), Thick(500, 180, 500, 200, 1)], (200, 170, 70))
    # long-case clock (left middle)
    wood = (130, 80, 50)
    piece(c, [RRect(20, 180, 140, 250, 4), RRect(36, 250, 124, 430, 2), RRect(26, 420, 134, 440, 2)], wood, border=1.5, shadow=PROP)
    flat(c, Circ(80, 214, 28), (250, 246, 232))
    flat(c, RRect(52, 270, 108, 400, 4), (60, 40, 30))
    # workbench (centre)
    piece(c, RRect(260, 360, 640, 380, 2), (160, 110, 70), border=1.5, shadow=PROP)
    piece(c, RRect(270, 380, 630, 440, 0), (140, 94, 60), shadow=LAYER)
    hx, hy = modern(c, 450, 362, (90, 110, 90), bottom=(50, 50, 60), hair=(200, 200, 200), h=2.0, glasses=True)
    flat(c, Circ(hx + 8, hy, 6), (120, 200, 230))
    # desk lamp (bench left)
    lamp = (60, 120, 90) if "lamp" not in d else (220, 140, 50)
    piece(c, [Ell(320, 358, 22, 5), Thick(320, 356, 300, 300, 3), Thick(300, 300, 340, 270, 3), Poly([(326, 274), (360, 260), (370, 290)])], lamp, border=1.2,
          shadow=SMALL)
    # watch parts tray (bench right)
    piece(c, RRect(520, 340, 610, 360, 3), (60, 60, 80), shadow=SMALL)
    for k in range(4):
        flat(c, Circ(536 + k * 20, 350, 6), [(200, 170, 70), (200, 200, 210)][k % 2])
    # big decorative gear (right middle)
    if "gear" not in d:
        pts = []
        for k in range(24):
            a = k * math.pi / 12
            r = 46 if k % 2 else 36
            pts.append((780 + r * math.cos(a), 330 + r * math.sin(a)))
        piece(c, Poly(pts), (200, 170, 70), border=1.5, shadow=PROP)
        flat(c, Circ(780, 330, 12), (120, 70, 60))
    # floor
    c.rect(0, 440, W, H, (90, 60, 50))
    planks(c, 440, (110, 74, 54), (96, 62, 46), seed=2741)
    # watch display case (right front)
    piece(c, RRect(620, 480, 880, 580, 3), (90, 60, 40), border=1.5, shadow=PROP)
    flat(c, RRect(630, 490, 870, 540, 2), (60, 70, 90))
    for k, x in enumerate(range(660, 870, 50)):
        col = (200, 170, 70) if not (k == 2 and "watch" in d) else (200, 200, 220)
        face = (250, 246, 232) if not (k == 2 and "watch" in d) else (60, 110, 180)
        flat(c, [RRect(x - 6, 494, x + 6, 536, 2)], (110, 70, 50) if not (k == 2 and "watch" in d) else (60, 60, 70))
        c.ellipse_ring(x, 515, 14, 14, 5, col)
        flat(c, Circ(x, 515, 10), face)
    # sleeping cat on a stool (left front)
    piece(c, [Ell(150, 530, 50, 12), RRect(144, 530, 156, 596, 2)], (160, 110, 70), shadow=PROP)
    if "cat" not in d:
        piece(c, [Ell(150, 512, 40, 16), Circ(184, 506, 13), Poly([(176, 498), (178, 486), (184, 496)]), Poly([(188, 496), (194, 486), (196, 498)])], (60, 60, 70),
              border=1.2, shadow=SMALL)
    # customer
    modern(c, 420, 600, (200, 150, 90), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.3)


L274_ELEMENTS = [
    hands_el("h1", 90, 90, 50, 30), hands_el("h2", 230, 70, 34, -40), hands_el("h3", 600, 80, 40, 20), hands_el("h4", 835, 85, 34, 50),
    hands_el("h5", 450, 140, 26, 36), hands_el("h6", 80, 214, 28, 24),
    E("pend", lambda c, m: [flat(c, Thick(80, 270, 80, 360, 2), (200, 170, 70)), piece(c, Circ(80, 368, 12), (220, 190, 80), shadow=None)], pivot=(80, 270),
      anim=dict(swingAngle=16, swingSpeed=0.8)),
    E("glow", lambda c, m: soft_union(c, [Poly([(330, 280), (380, 270), (420, 360), (300, 360)])], (255, 230, 160), 0.25, spread=16), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=0.6)),
]

L274_DIFFS = [
    ("round", 90, 90, 0),
    ("cuckoo", 450, 55, 0),
    ("lamp", 330, 300, 0),
    ("gear", 780, 330, 0),
    ("watch", 760, 515, 0),
    ("cat", 160, 506, 0),
]


LEVELS = [
    ("Level265", "竹林熊猫", l265_bg, L265_ELEMENTS, L265_DIFFS, 60, OPTS),
    ("Level266", "水族馆", l266_bg, L266_ELEMENTS, L266_DIFFS, 60, OPTS),
    ("Level267", "自然博物馆", l267_bg, L267_ELEMENTS, L267_DIFFS, 60, OPTS),
    ("Level268", "画室", l268_bg, L268_ELEMENTS, L268_DIFFS, 60, OPTS),
    ("Level269", "寿司店", l269_bg, L269_ELEMENTS, L269_DIFFS, 60, OPTS),
    ("Level270", "宠物店", l270_bg, L270_ELEMENTS, L270_DIFFS, 60, OPTS),
    ("Level271", "理发店", l271_bg, L271_ELEMENTS, L271_DIFFS, 60, OPTS),
    ("Level272", "咖啡馆", l272_bg, L272_ELEMENTS, L272_DIFFS, 60, OPTS),
    ("Level273", "洗衣房", l273_bg, L273_ELEMENTS, L273_DIFFS, 60, OPTS),
    ("Level274", "钟表店", l274_bg, L274_ELEMENTS, L274_DIFFS, 60, OPTS),
]
