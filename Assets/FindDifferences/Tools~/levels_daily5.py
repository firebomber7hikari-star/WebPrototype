# -*- coding: utf-8 -*-
"""Everyday-town themes, part 5: nature trips (paper-craft side views, full-bleed):
  Level540 峡谷瀑布 - a canyon waterfall: cliffs, falling water, plunge pool, rainbow, viewing deck with hikers
  Level541 海狮海湾 - a sea-lion cove: rocks with sea lions, tour boat, cliffs, gulls
  Level542 林间小鹿 - a forest glade: deer family, birches, brook, mushrooms, rabbit
  Level543 雪原狐狸 - a snowy meadow: foxes, pines, distant cabin, tracks; snow
  Level544 雪猴温泉 - a mountain hot spring: macaques bathing, steam, snowy rocks; snow
  Level545 荷塘     - a lotus pond: lotus pads and flowers, pavilion, picker's boat, frogs, dragonflies
  Level546 向日葵田 - a sunflower field: rows of sunflowers, farmhouse, water tower, cyclist
  Level547 仙人掌荒野 - a cactus desert: mesas, saguaros, road sign, coyote; day / night with a campfire
  Level548 海龟沙滩 - a turtle beach: hatchlings heading to the sea, volunteers, palms; day / night
  Level549 秋日山径 - an autumn mountain trail: maples, signpost, footbridge, hikers; rain showers
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cactus, cloud_bg, cloud_el, drift_across, palm, rock, sky, tree_pine, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern
from stylekit import celestial, day_night, moon_element, star_field, sun_element, window_glow
from weather import cloud, fog_layer, paper_sun, puddles, rain_layer, snow_layer, splash_rings

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SNOWC = (246, 248, 252)


def hiker(c, x, base, top, pack, h=1.9, hair=(40, 30, 30), style="short", right=True):
    k = -1 if right else 1
    piece(c, RRect(x + k * 6 * h - 7 * h, base - 40 * h, x + k * 6 * h + 7 * h, base - 18 * h, 4), pack, border=1.2, shadow=SMALL)
    modern(c, x, base, top, bottom=(70, 70, 80), hair=hair, h=h, style=style)
    flat(c, Thick(x - k * 10 * h, base - 20 * h, x - k * 16 * h, base, 1.6), (120, 90, 60))


# =================================================================== Level 540 canyon waterfall
def l540_bg(c, d):
    sky(c, (120, 184, 236), (220, 234, 246), 300)
    cloud_bg(c, 450, 50, 0.8)
    far_ridge(c, 160, 50, (160, 186, 196), 5401)
    # cliffs (left and right) leaving a gap for the fall
    for pts, col in (([(-10, 60), (120, 40), (300, 70), (380, 100), (360, 500), (-10, 520)], (190, 130, 100)),
                     ([(520, 100), (620, 60), (780, 40), (910, 70), (910, 520), (540, 500)], (180, 124, 96))):
        piece(c, Poly(pts), col, border=1.5, shadow=LAYER)
    for y in range(120, 480, 40):
        flat(c, [Thick(0, y, 350, y + 10, 3), Thick(550, y + 6, 900, y - 4, 3)], (166, 110, 84))
    # trees on the cliff tops
    for x, s, col in ((60, 1.0, (90, 150, 90)), (190, 1.2, (80, 140, 80)), (700, 1.1, (90, 150, 90)), (830, 1.0, (80, 140, 80))):
        tree_round(c, x, 70 if x < 400 else 60, s=s, col=col if not (x == 830 and "tree" in d) else (230, 150, 60))
    # water column (static base colour)
    flat(c, RRect(380, 96, 520, 470, 0), (150, 206, 240))
    # rainbow over the pool
    for k, col in enumerate(((240, 90, 90), (250, 170, 70), (250, 230, 90), (120, 200, 110), (90, 150, 230), (150, 110, 210))):
        c.ellipse_ring(450, 470, 200 - k * 10, 160 - k * 10, 6, col + (0.55,), ymax=470)
    # plunge pool + river
    piece(c, Ell(450, 480, 260, 40), (90, 160, 210), border=2, shadow=SMALL)
    piece(c, Poly([(200, 500), (700, 500), (900, 612), (0, 612)]), (100, 170, 214), shadow=SMALL)
    for x, y, w in ((300, 540, 60), (500, 570, 80), (650, 530, 50), (180, 590, 70)):
        flat(c, Thick(x, y, x + w, y, 2), (160, 210, 236))
    # viewing deck (left) with hikers
    piece(c, RRect(30, 380, 250, 396, 2), (150, 110, 80), border=1.5, shadow=PROP)
    rail = (150, 110, 80) if "rail" not in d else (60, 140, 200)
    flat(c, [Thick(30, 340, 250, 340, 4)] + [Thick(40 + k * 30, 340, 40 + k * 30, 380, 3) for k in range(8)], rail)
    flat(c, [Thick(60, 396, 60, 520, 5), Thick(220, 396, 220, 520, 5)], (130, 90, 60))
    hiker(c, 100, 380, (240, 120, 60), (60, 110, 180) if "pack" not in d else (240, 200, 60), h=1.8)
    hiker(c, 170, 380, (90, 160, 110), (200, 70, 70), h=1.7, hair=(220, 180, 90), style="long")
    # mossy rocks + ferns in front
    rock(c, 760, 600, s=2.2, col=(140, 140, 150) if "rock" not in d else (190, 150, 110))
    rock(c, 90, 612, s=2.0)
    for x in (620, 860):
        flat(c, [Thick(x, 600, x - 20, 560, 3), Thick(x, 600, x, 554, 3), Thick(x, 600, x + 20, 560, 3)], (80, 150, 80))
    # flower patch on the right cliff
    flat(c, [Circ(600 + k * 14, 300 - (k % 2) * 6, 6) for k in range(6)], (250, 200, 60) if "flowers" not in d else (230, 100, 160))


def fall(c, m):
    rnd = random.Random(5402)
    for k in range(14):
        x = 386 + k * 10
        for j in range(4):
            y = 100 + j * 100 + rnd.uniform(0, 60)
            flat(c, Thick(x, y, x, y + 50, 3), (230, 244, 252, 0.85))


L540_ELEMENTS = [
    E("fall", fall, bbox=(370, 90, 530, 560), anim=dict(driftVelocity=(0, -120), driftLength=100)),
    E("mist", lambda c, m: soft_union(c, [Ell(450, 470, 120, 20)], (250, 252, 255), 0.6, spread=20), anim=dict(pulse=0.1, scaleSpeed=0.6)),
    bird_el("bird1", 300, 30, s=8, speed=20),
    bird_el("bird2", 600, 20, s=7, speed=-16),
]

L540_DIFFS = [
    ("tree", 830, 10, 0),
    ("rail", 140, 340, 0),
    ("pack", 106, 334, 0),
    ("rock", 760, 580, 0),
    ("flowers", 636, 298, 0),
]


# =================================================================== Level 541 sea-lion cove
def sea_lion(c, x, base, s=1.0, col=(120, 90, 70), face_right=True, up=False):
    k = 1 if face_right else -1
    if up:
        piece(c, [Ell(x, base - 20 * s, 30 * s, 20 * s), Poly([(x - k * 4 * s, base - 30 * s), (x + k * 26 * s, base - 26 * s), (x + k * 22 * s, base - 64 * s),
                                                               (x + k * 2 * s, base - 68 * s)]),
                  Ell(x + k * 16 * s, base - 72 * s, 14 * s, 11 * s), Ell(x + k * 30 * s, base - 70 * s, 8 * s, 6 * s)], col, border=1.2, shadow=PROP)
        flat(c, Circ(x + k * 20 * s, base - 76 * s, 2 * s), INK)
        flat(c, Ell(x + k * 36 * s, base - 70 * s, 3 * s, 2 * s), (60, 40, 30))
        flat(c, Ell(x + k * 22 * s, base - 8 * s, 10 * s, 4 * s), lit(col, 0.8))
    else:
        piece(c, [Ell(x, base - 14 * s, 46 * s, 14 * s), Circ(x + k * 40 * s, base - 22 * s, 12 * s), Poly([(x - k * 40 * s, base - 10 * s),
                                                                                                         (x - k * 66 * s, base - 22 * s), (x - k * 66 * s, base)])],
              col, border=1.2, shadow=PROP)
        flat(c, Circ(x + k * 44 * s, base - 26 * s, 1.8 * s), INK)
    flat(c, Ell(x + k * 6 * s, base - 4 * s, 12 * s, 4 * s), lit(col, 0.8))


def l541_bg(c, d):
    sky(c, (120, 186, 236), (230, 236, 240), 300)
    cloud_bank(c, 120, (250, 250, 246), 5411, k=0.7)
    c.gradient(220, H, (80, 160, 200), (40, 100, 150))
    # cliffs on both sides with grass tops
    piece(c, Poly([(-10, 120), (140, 110), (240, 160), (260, 340), (-10, 360)]), (170, 150, 130), border=1.5, shadow=LAYER)
    flat(c, Poly([(-10, 120), (140, 110), (240, 160), (220, 170), (-10, 140)]), (120, 170, 100))
    piece(c, Poly([(700, 160), (820, 110), (910, 120), (910, 330), (680, 330)]), (170, 150, 130), border=1.5, shadow=LAYER)
    flat(c, Poly([(700, 160), (820, 110), (910, 120), (910, 140), (720, 170)]), (120, 170, 100))
    # little viewing hut on the right cliff
    piece(c, RRect(790, 70, 870, 120, 2), (250, 246, 236), border=1.5, shadow=PROP)
    piece(c, Poly([(780, 74), (880, 74), (830, 40)]), (220, 80, 70) if "roof" not in d else (60, 120, 200), border=1.5, shadow=PROP)
    # waves
    for k in range(18):
        rnd = random.Random(5412 + k)
        x, y = rnd.uniform(0, 900), rnd.uniform(240, 580)
        flat(c, Thick(x, y, x + rnd.uniform(20, 60), y, 2), (130, 196, 230))
    # rocks with sea lions
    piece(c, Poly([(140, 470), (190, 400), (300, 380), (380, 410), (420, 470)]), (110, 106, 110), border=1.5, shadow=PROP)
    piece(c, Poly([(500, 520), (540, 450), (650, 430), (740, 460), (780, 520)]), (110, 106, 110), border=1.5, shadow=PROP)
    flat(c, [Ell(220, 420, 30, 6), Ell(600, 452, 40, 6)], (240, 240, 236))                  # guano patches
    sea_lion(c, 250, 404, s=1.2)
    sea_lion(c, 350, 418, s=1.0, col=(150, 110, 80), face_right=False, up=True)
    sea_lion(c, 600, 454, s=1.3, col=(120, 90, 70) if "pup" not in d else (220, 200, 170))
    sea_lion(c, 700, 470, s=1.0, col=(150, 110, 80), up=True)
    piece(c, Poly(star_pts(420, 462, 14, 6)), (250, 120, 70) if "star" not in d else (160, 110, 220), border=1, shadow=SMALL)
    # buoy
    piece(c, [Ell(860, 420, 16, 8), RRect(852, 390, 868, 418, 3)], (250, 200, 60) if "buoy" not in d else (220, 70, 70), border=1.2, shadow=SMALL)
    # tour boat (front)
    piece(c, Poly([(60, 540), (420, 540), (390, 590), (90, 590)]), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(64, 556, 416, 564, 1), (60, 120, 200))
    flat(c, Thick(390, 490, 390, 440, 3), (120, 120, 130))
    piece(c, Poly([(391, 440), (430, 450), (391, 462)]), (220, 70, 70) if "flag" not in d else (90, 180, 110), border=1, shadow=SMALL)
    piece(c, [RRect(120, 490, 360, 500, 2)], (220, 220, 230), shadow=SMALL)
    flat(c, [Thick(130 + k * 46, 500, 130 + k * 46, 540, 3) for k in range(6)], (220, 220, 230))
    for k, (x, col) in enumerate(((160, (240, 120, 60)), (220, (90, 150, 220)), (290, (240, 200, 90)), (340, (120, 190, 120)))):
        modern(c, x, 540, col, bottom=(60, 60, 80), hair=[(40, 30, 30), (90, 60, 40), (220, 180, 90), (130, 130, 140)][k], h=1.3)


L541_ELEMENTS = [
    E("swim", lambda c, m: (piece(c, Ell(0, 360, 18, 6), (120, 90, 70), shadow=SMALL), flat(c, Circ(14, 356, 1.5), INK)),
      anim=dict(drift_across(-20, 20, 24, start=500), bobAmplitude=(0, 3), bobSpeed=0.4)),
    E("bark", lambda c, m: sea_lion(c, 350, 418, s=1.0, col=(150, 110, 80), face_right=False, up=True), pivot=(350, 418),
      anim=dict(swingAngle=5, swingSpeed=0.6)),
    bird_el("gull1", 300, 200, s=9, speed=-20),
    bird_el("gull2", 600, 180, s=8, speed=24),
    E("splash", lambda c, m: c.ellipse_ring(480, 500, 16, 5, 2, (220, 240, 250)), pivot=(480, 500), anim=dict(pulse=0.4, scaleSpeed=0.8, twinkle=0.5)),
]

L541_DIFFS = [
    ("roof", 830, 60, 0),
    ("pup", 600, 434, 0),
    ("star", 420, 462, 0),
    ("buoy", 860, 408, 0),
    ("flag", 406, 450, 0),
]


# =================================================================== Level 542 forest glade with deer
def deer(c, x, base, s=1.0, col=(190, 130, 80), face_right=True, antlers=False, fawn=False):
    k = 1 if face_right else -1
    legs = [RRect(x + dx * s - 3 * s, base - 40 * s, x + dx * s + 3 * s, base, 2) for dx in (-22, -14, 14, 22)]
    piece(c, legs + [Ell(x, base - 46 * s, 32 * s, 15 * s), Poly([(x + k * 20 * s, base - 54 * s), (x + k * 30 * s, base - 50 * s),
                                                                     (x + k * 40 * s, base - 86 * s), (x + k * 30 * s, base - 90 * s)]),
                     Ell(x + k * 40 * s, base - 90 * s, 12 * s, 8 * s)], col, border=1.2, shadow=PROP)
    flat(c, [Ell(x + k * 30 * s, base - 100 * s, 4 * s, 7 * s)], col)
    flat(c, Circ(x + k * 42 * s, base - 92 * s, 1.8 * s), INK)
    flat(c, Ell(x + k * 50 * s, base - 88 * s, 3 * s, 2 * s), INK)
    flat(c, Ell(x - k * 30 * s, base - 50 * s, 5 * s, 6 * s), (250, 246, 236))
    if fawn:
        flat(c, [Circ(x + dx * s, base - 48 * s + dy * s, 2.4 * s) for dx, dy in ((-14, -4), (-4, -6), (6, -4), (14, -6), (-8, 2), (8, 2))], (250, 246, 236))
    if antlers:
        ax, ay = x + k * 36 * s, base - 98 * s
        flat(c, [Thick(ax, ay, ax - k * 6 * s, ay - 26 * s, 2.4 * s), Thick(ax - k * 4 * s, ay - 14 * s, ax - k * 16 * s, ay - 22 * s, 2 * s),
                 Thick(ax + k * 6 * s, ay, ax + k * 14 * s, ay - 24 * s, 2.4 * s), Thick(ax + k * 10 * s, ay - 12 * s, ax + k * 22 * s, ay - 16 * s, 2 * s)],
             (220, 200, 160))


def birch(c, x, base, h=300, w=16):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 3), (246, 244, 236), border=1, shadow=PROP)
    rnd = random.Random(x)
    for _ in range(int(h / 26)):
        y = base - rnd.uniform(10, h - 10)
        flat(c, Thick(x - w / 2, y, x - w / 2 + rnd.uniform(4, w), y, 2.4), (60, 60, 66))


def l542_bg(c, d):
    sky(c, (150, 200, 230), (226, 236, 222), 300)
    far_round_trees(c, 160, 40, (130, 180, 140), 5421)
    far_round_trees(c, 220, 34, (100, 160, 110), 5422)
    piece(c, RRect(-10, 300, 910, 612, 0), (130, 180, 100), shadow=LAYER)
    for k in range(20):
        rnd = random.Random(5423 + k)
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(320, 600), rnd.uniform(20, 50), 5), (120, 170, 92))
    # birches + canopy
    for x, h in ((40, 420), (130, 380), (760, 400), (860, 440)):
        birch(c, x, 420 if x < 400 else 430, h=h)
    for x, y, r in ((60, 40, 70), (150, 60, 60), (780, 40, 70), (880, 60, 60)):
        piece(c, [Circ(x, y, r), Circ(x + 40, y + 20, r * 0.7)], (110, 170, 90) if not (x == 880 and "canopy" in d) else (220, 160, 60), shadow=PROP)
    # brook across the glade
    piece(c, Poly([(-10, 470), (300, 440), (600, 470), (910, 450), (910, 500), (600, 520), (300, 490), (-10, 520)]), (120, 186, 220), border=1.5,
          shadow=SMALL)
    for x in (100, 400, 700):
        flat(c, Thick(x, 476, x + 50, 474, 2), (180, 220, 240))
    # stepping stones
    for x in (430, 470, 510):
        piece(c, Ell(x, 480, 16, 7), (170, 166, 170), shadow=SMALL)
    # deer family
    deer(c, 300, 420, s=1.6, antlers=True)
    deer(c, 560, 430, s=1.4, col=(200, 140, 90), face_right=False)
    deer(c, 470, 440, s=0.9, col=(210, 150, 100) if "fawn" not in d else (150, 100, 70), fawn=True, face_right=False)
    # mushrooms + flowers + rabbit
    for k, (x, col) in enumerate(((200, (220, 70, 70)), (230, (220, 70, 70)), (100, (240, 170, 70)))):
        if k == 2 and "mushroom" in d:
            col = (150, 120, 220)
        piece(c, [RRect(x - 3, 560, x + 3, 580, 2)], (246, 238, 220), shadow=SMALL)
        piece(c, Ell(x, 560, 14, 8), col, border=1, shadow=SMALL)
        flat(c, [Circ(x - 5, 558, 2), Circ(x + 4, 556, 2)], (250, 246, 236))
    flat(c, [Circ(340 + k * 16, 580 - (k % 2) * 6, 5) for k in range(6)], (250, 220, 90) if "flowers" not in d else (240, 120, 170))
    piece(c, [Ell(820, 580, 16, 11), Circ(834, 568, 8), Ell(830, 554, 3, 9), Ell(838, 554, 3, 9)], (200, 180, 160) if "rabbit" not in d else (250, 250, 250),
          border=1, shadow=SMALL)
    flat(c, Circ(838, 568, 1.4), INK)
    # fallen log
    piece(c, RRect(560, 556, 760, 584, 14), (130, 90, 60) if "log" not in d else (100, 120, 90), border=1.5, shadow=PROP)
    flat(c, [Ell(560, 570, 8, 14)], (190, 150, 100))
    c.ellipse_ring(560, 570, 5, 9, 1.4, (150, 110, 70))


L542_ELEMENTS = [
    E("tailA", lambda c, m: flat(c, Ell(250, 340, 5, 8), (250, 246, 236)), pivot=(252, 336), anim=dict(swingAngle=20, swingSpeed=1.2)),
    E("butterfly", lambda c, m: (flat(c, [Ell(-6, 0, 6, 4), Ell(6, 0, 6, 4)], (250, 160, 200)), flat(c, Thick(0, -4, 0, 4, 1.5), INK)),
      anim=dict(drift_across(-12, 12, 22, start=300), driftVelocity=(22, 0), bobAmplitude=(0, 14), bobSpeed=0.6, stretch=(0.5, 0), scaleSpeed=3)),
    E("leaf", lambda c, m: flat(c, Ell(420, 100, 6, 3), (220, 160, 60)), anim=dict(driftVelocity=(8, -20), driftLength=300, driftFade=True, spinSpeed=0.6)),
    E("ears", lambda c, m: flat(c, Ell(838, 554, 3, 9), (200, 180, 160)), pivot=(838, 562), anim=dict(swingAngle=14, swingSpeed=0.8)),
    bird_el("bird", 450, 120, s=8, speed=18),
]

L542_DIFFS = [
    ("fawn", 470, 400, 0),
    ("mushroom", 100, 556, 0),
    ("canopy", 890, 60, 0),
    ("rabbit", 830, 566, 0),
    ("flowers", 380, 578, 0),
    ("log", 660, 570, 0),
]


# =================================================================== Level 543 snowy meadow with foxes (snow)
STEPS543 = [(CLEAR, 10), (SNOW, 14)]


def fox(c, x, base, s=1.0, col=(230, 120, 50), face_right=True, sit=False):
    k = 1 if face_right else -1
    if sit:
        piece(c, [Ell(x, base - 24 * s, 18 * s, 24 * s), Circ(x + k * 6 * s, base - 54 * s, 13 * s),
                  Poly([(x + k * 12 * s, base - 54 * s), (x + k * 30 * s, base - 50 * s), (x + k * 14 * s, base - 46 * s)]),
                  Poly([(x - 2 * s, base - 62 * s), (x, base - 78 * s), (x + 8 * s, base - 64 * s)]),
                  Poly([(x + 8 * s, base - 64 * s), (x + 14 * s, base - 78 * s), (x + 16 * s, base - 60 * s)]),
                  Ell(x - k * 24 * s, base - 6 * s, 24 * s, 9 * s)], col, border=1.2, shadow=PROP)
        flat(c, Ell(x + k * 4 * s, base - 30 * s, 9 * s, 16 * s), (250, 246, 240))
    else:
        piece(c, [Ell(x, base - 24 * s, 28 * s, 11 * s), Circ(x + k * 30 * s, base - 32 * s, 11 * s),
                  Poly([(x + k * 36 * s, base - 34 * s), (x + k * 52 * s, base - 28 * s), (x + k * 36 * s, base - 24 * s)]),
                  Poly([(x + k * 24 * s, base - 40 * s), (x + k * 26 * s, base - 54 * s), (x + k * 32 * s, base - 42 * s)]),
                  Ell(x - k * 40 * s, base - 26 * s, 24 * s, 9 * s)] +
              [RRect(x + dx * s - 2.4 * s, base - 16 * s, x + dx * s + 2.4 * s, base, 1) for dx in (-16, -8, 10, 18)], col, border=1.2, shadow=PROP)
        flat(c, Ell(x - k * 56 * s, base - 26 * s, 8 * s, 6 * s), (250, 246, 240))
    flat(c, Circ(x + k * (32 if not sit else 10) * s, base - (34 if not sit else 56) * s, 1.8 * s), INK)


def l543_bg(c, d):
    sky(c, (140, 180, 220), (226, 232, 244), 300)
    far_ridge(c, 180, 60, (200, 212, 232), 5431)
    piece(c, Poly([(-10, 240), (300, 210), (600, 230), (910, 210), (910, 612), (-10, 612)]), SNOWC, shadow=LAYER)
    # pine forest band
    for k, x in enumerate(range(-10, 920, 46)):
        h = 90 + (k * 37) % 50
        if 330 < x < 460:
            continue
        tree_pine(c, x, 260 + (k % 3) * 8, h=h, col=(60, 110, 90), snow=SNOWC)
    # distant cabin
    piece(c, RRect(360, 200, 440, 250, 2), (150, 100, 70) if "cabin" not in d else (80, 110, 150), border=1.5, shadow=PROP)
    piece(c, Poly([(350, 204), (450, 204), (400, 170)]), (240, 244, 252), border=1.5, shadow=SMALL)
    flat(c, RRect(390, 220, 410, 236, 2), (255, 220, 140))
    flat(c, RRect(424, 160, 436, 190, 1), (120, 90, 80))
    # snow drifts + tracks
    for x, y in ((150, 360), (500, 400), (760, 350), (300, 520), (700, 540)):
        flat(c, Ell(x, y, 120, 10), (226, 234, 248))
    for k in range(10):
        flat(c, [Ell(80 + k * 40, 470 + (k % 2) * 8, 4, 3)], (200, 210, 230))
    # foxes
    fox(c, 300, 430, s=1.6)
    fox(c, 620, 470, s=1.4, face_right=False, sit=True, col=(230, 120, 50) if "fox" not in d else (240, 244, 250))
    fox(c, 780, 400, s=1.0, col=(220, 110, 50), face_right=False)
    # fence posts + bird box + scarf on a post
    for x in (60, 140, 220):
        piece(c, RRect(x - 5, 520, x + 5, 600, 2), (120, 90, 70), shadow=PROP)
        flat(c, Ell(x, 520, 8, 4), SNOWC)
    flat(c, [Thick(60, 540, 220, 536, 3)], (120, 90, 70))
    piece(c, [RRect(126, 470, 154, 506, 3), Poly([(120, 474), (160, 474), (140, 458)])], (170, 120, 80) if "box" not in d else (60, 140, 200),
          border=1, shadow=SMALL)
    flat(c, Circ(140, 488, 5), (60, 40, 30))
    piece(c, [RRect(126, 506, 154, 512, 1)], (120, 90, 70), shadow=None)
    # berry bush
    piece(c, [Circ(860, 580, 30), Circ(830, 590, 22), Circ(890, 592, 22)], (70, 110, 80), shadow=PROP)
    flat(c, [Circ(838 + k * 12, 568 + (k % 2) * 12, 6) for k in range(6)], (220, 50, 60) if "berries" not in d else (120, 90, 200))


L543_ELEMENTS = [
    E("tail", lambda c, m: piece(c, Ell(236, 384, 24, 9), (230, 120, 50), border=1.2, shadow=SMALL), pivot=(256, 386), anim=dict(swingAngle=10, swingSpeed=0.8)),
    E("hare", lambda c, m: (piece(c, [Ell(0, 560, 14, 9), Circ(12, 550, 7), Ell(10, 538, 3, 9), Ell(16, 538, 3, 9)], (250, 250, 252), border=1, shadow=SMALL)),
      anim=dict(drift_across(-14, 18, 40, start=500), bobAmplitude=(0, 10), bobSpeed=1.2, bounce=True)),
    E("smoke", lambda c, m: soft_union(c, [Circ(430, 156, 6)], (240, 240, 244), 0.7, spread=6), anim=dict(driftVelocity=(4, 14), driftLength=40, driftFade=True)),
    cloud("cloudA", 200, 50, 1.2, (210, 216, 230), W_(SNOW)),
    cloud("cloudB", 680, 40, 1.3, (210, 216, 230), W_(SNOW)),
    snow_layer("snow", 543, 70, 2.0, 4.0, 40),
]

L543_DIFFS = [
    ("cabin", 400, 228, 0),
    ("fox", 620, 430, 0),
    ("box", 140, 484, 0),
    ("berries", 868, 580, 0),
]


# =================================================================== Level 544 snow-monkey hot spring (snow)
STEPS544 = [(CLEAR, 10), (SNOW, 14)]


def macaque(c, x, base, s=1.0, fur=(170, 150, 130), face=(230, 120, 120), bathing=True):
    if bathing:
        piece(c, [Ell(x, base - 10 * s, 26 * s, 14 * s), Circ(x, base - 34 * s, 18 * s)], fur, border=1.2, shadow=SMALL)
    else:
        piece(c, [Ell(x, base - 24 * s, 22 * s, 26 * s), Circ(x, base - 58 * s, 18 * s)] +
              [RRect(x + dx * s - 5 * s, base - 14 * s, x + dx * s + 5 * s, base, 3) for dx in (-12, 12)], fur, border=1.2, shadow=PROP)
        base -= 24 * s
    flat(c, Ell(x, base - 32 * s, 11 * s, 10 * s), face)
    flat(c, [Circ(x - 4 * s, base - 34 * s, 1.8 * s), Circ(x + 4 * s, base - 34 * s, 1.8 * s)], INK)


def l544_bg(c, d):
    sky(c, (150, 180, 214), (226, 232, 244), 300)
    far_ridge(c, 120, 80, (210, 220, 236), 5441)
    # snowy slopes + pines
    piece(c, Poly([(-10, 220), (300, 170), (600, 200), (910, 160), (910, 612), (-10, 612)]), SNOWC, shadow=LAYER)
    for x, b, h in ((30, 260, 120), (100, 240, 140), (180, 250, 100), (720, 230, 130), (800, 220, 150), (880, 240, 120)):
        tree_pine(c, x, b, h=h, col=(60, 110, 90), snow=SNOWC)
    # wooden bath house
    piece(c, RRect(300, 110, 520, 230, 2), (150, 100, 70), border=1.5, shadow=PROP)
    piece(c, Poly([(286, 114), (534, 114), (410, 60)]), (90, 70, 70), border=1.5, shadow=PROP)
    flat(c, Poly([(286, 114), (534, 114), (480, 90), (410, 60), (340, 90)]), (240, 244, 252))
    for x in (330, 440):
        flat(c, RRect(x, 140, x + 50, 190, 2), (255, 220, 140))
    piece(c, RRect(360, 92, 460, 108, 3), (200, 60, 60) if "banner" not in d else (60, 110, 190), border=1, shadow=SMALL)
    # rock-rimmed pool
    piece(c, Ell(450, 430, 420, 110), (130, 126, 130), border=2, shadow=LAYER)
    flat(c, Ell(450, 430, 380, 90), (120, 190, 200))
    for x in range(70, 840, 60):
        piece(c, Ell(x, 340 + abs(x - 450) * 0.08, 34, 18), (150, 146, 150), shadow=SMALL)
        flat(c, Ell(x, 330 + abs(x - 450) * 0.08, 26, 7), SNOWC)
    # bathing macaques
    for k, (x, y) in enumerate(((250, 440), (380, 470), (520, 450), (650, 430))):
        macaque(c, x, y, s=1.3, fur=(170, 150, 130) if not (k == 2 and "fur" in d) else (110, 100, 96))
    flat(c, [Ell(250 + k * 130, 450 + (k % 2) * 20, 30, 6) for k in range(4)], (150, 210, 220))
    # monkey on a rock with a towel
    macaque(c, 800, 350, s=1.2, bathing=False)
    piece(c, RRect(780, 300, 820, 312, 3), (250, 250, 250) if "towel" not in d else (240, 120, 160), border=1, shadow=SMALL)
    # wooden bucket + ladle on the edge
    piece(c, [RRect(120, 520, 170, 566, 5)], (190, 140, 90) if "bucket" not in d else (90, 160, 210), border=1.2, shadow=PROP)
    flat(c, [Thick(120, 532, 170, 532, 2), Thick(120, 554, 170, 554, 2)], (150, 100, 60))
    flat(c, [Thick(166, 520, 196, 488, 3), Ell(198, 486, 8, 5)], (170, 120, 80))
    # snow ground front
    c.rect(0, 560, W, H, SNOWC)
    flat(c, [Ell(300, 580, 90, 6), Ell(700, 586, 80, 6)], (226, 234, 248))
    tree_pine(c, 860, 610, h=150, col=(60, 110, 90), snow=SNOWC)


L544_ELEMENTS = [
    E("steam%d" % i, (lambda x: lambda c, m: soft_union(c, [Circ(x, 400, 16)], (250, 252, 255), 0.6, spread=18))(x),
      anim=dict(driftVelocity=(4, 26), driftLength=110, driftFade=True, driftGrow=1.6, phase=i / 4))
    for i, x in enumerate((180, 330, 600, 720))
] + [
    E("dip", lambda c, m: macaque(c, 380, 470, s=1.3), pivot=(380, 470), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.3)),
    cloud("cloudA", 200, 40, 1.2, (210, 216, 230), W_(SNOW)),
    cloud("cloudB", 680, 30, 1.3, (210, 216, 230), W_(SNOW)),
    snow_layer("snow", 544, 70, 2.0, 4.0, 40),
]

L544_DIFFS = [
    ("banner", 410, 100, 0),
    ("fur", 520, 430, 0),
    ("towel", 800, 306, 0),
    ("bucket", 145, 543, 0),
]


# =================================================================== Level 545 lotus pond
def lotus(c, x, y, s=1.0, col=(246, 150, 180)):
    for a in (-50, -25, 0, 25, 50):
        r = math.radians(a - 90)
        cx, cy = x + 12 * s * math.cos(r), y + 12 * s * math.sin(r) + 6 * s
        piece(c, Ell(cx, cy, 7 * s, 14 * s), col, border=0.8, shadow=None)
    flat(c, Circ(x, y + 6 * s, 5 * s), (250, 220, 90))


def lily_pad(c, x, y, r, col=(90, 160, 90)):
    piece(c, Poly([(x, y)] + [(x + r * math.cos(math.radians(a)), y + r * 0.45 * math.sin(math.radians(a))) for a in range(20, 360, 20)]), col,
          border=1, shadow=SMALL)
    flat(c, Thick(x, y, x + r * 0.7, y - r * 0.2, 1.2), lit(col, 0.8))


def l545_bg(c, d):
    sky(c, (150, 200, 236), (232, 240, 236), 250)
    far_ridge(c, 150, 50, (180, 206, 200), 5451)
    far_round_trees(c, 210, 30, (120, 170, 130), 5452)
    # pond
    c.gradient(220, H, (130, 186, 190), (90, 150, 170))
    for k in range(12):
        rnd = random.Random(5453 + k)
        x, y = rnd.uniform(0, 900), rnd.uniform(240, 580)
        flat(c, Thick(x, y, x + rnd.uniform(30, 70), y, 2), (170, 214, 220))
    # pavilion on the right bank
    piece(c, Poly([(640, 260), (910, 240), (910, 300), (640, 300)]), (140, 170, 110), shadow=LAYER)
    piece(c, RRect(680, 260, 860, 272, 2), (190, 60, 50), shadow=SMALL)
    for x in (690, 760, 840):
        piece(c, RRect(x, 170, x + 10, 262, 1), (190, 60, 50), shadow=SMALL)
    piece(c, Poly([(660, 176), (880, 176), (850, 150), (770, 120), (690, 150)]), (60, 70, 80) if "roof" not in d else (60, 120, 90), border=1.5, shadow=PROP)
    flat(c, [Poly([(650, 180), (666, 166), (674, 178)]), Poly([(890, 180), (874, 166), (866, 178)])], (60, 70, 80) if "roof" not in d else (60, 120, 90))
    # zigzag bridge (left)
    piece(c, Poly([(-10, 300), (120, 300), (180, 330), (300, 330), (300, 344), (176, 344), (116, 314), (-10, 314)]), (200, 180, 150), border=1.5, shadow=PROP)
    flat(c, [Thick(0 + k * 30, 300, 0 + k * 30, 284, 2) for k in range(5)], (200, 180, 150))
    # lily pads + lotus flowers
    rnd = random.Random(5454)
    pads = [(100, 400, 40), (220, 430, 34), (380, 380, 44), (520, 420, 38), (660, 380, 40), (800, 420, 44), (160, 520, 50), (420, 540, 46),
            (640, 520, 50), (860, 540, 40), (300, 480, 30)]
    for x, y, r in pads:
        lily_pad(c, x, y, r, col=(90, 160, 90) if rnd.random() < 0.6 else (110, 176, 100))
    for k, (x, y) in enumerate(((120, 340), (390, 320), (680, 320), (820, 360), (440, 470))):
        flat(c, Thick(x, y + 40, x, y + 10, 3), (90, 150, 90))
        lotus(c, x, y, s=1.3, col=(246, 150, 180) if not (k == 2 and "lotus" in d) else (250, 250, 250))
    # seed pod + frog
    flat(c, Thick(560, 400, 560, 340, 3), (90, 150, 90))
    piece(c, Ell(560, 336, 14, 9), (150, 190, 110), border=1, shadow=SMALL)
    piece(c, [Ell(520, 412, 14, 9), Circ(512, 404, 5), Circ(526, 404, 5)], (110, 180, 90) if "frog" not in d else (220, 170, 60), border=1, shadow=SMALL)
    flat(c, [Circ(512, 403, 1.8), Circ(526, 403, 1.8)], INK)
    # picker's boat (front)
    piece(c, Poly([(200, 580), (480, 580), (450, 612), (230, 612)]), (150, 110, 70), border=1.5, shadow=PROP)
    modern(c, 300, 590, (90, 140, 200), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.8)
    piece(c, Ell(302, 504, 26, 8), (230, 200, 120), shadow=None)
    piece(c, Poly([(380, 580), (440, 580), (446, 540), (374, 540)]), (200, 160, 100) if "basket" not in d else (90, 150, 200), border=1.2, shadow=SMALL)
    lotus(c, 410, 526, s=0.9)


L545_ELEMENTS = [
    E("dfly%d" % i, (lambda x, y, col: lambda c, m: (flat(c, Thick(x - 10, y, x + 10, y, 2.4), col),
                                                    flat(c, [Ell(x - 2, y - 5, 4, 7), Ell(x + 4, y - 5, 4, 7)], (230, 240, 250, 0.8))))(x, y, col),
      pivot=(x, y), anim=dict(bobAmplitude=(30, 10), bobSpeed=0.25 + i * 0.05, phase=i / 3))
    for i, (x, y, col) in enumerate(((250, 300, (60, 120, 220)), (600, 280, (220, 70, 70)), (760, 470, (60, 160, 120))))
] + [
    E("ripple", lambda c, m: c.ellipse_ring(560, 470, 30, 8, 2, (200, 230, 236)), pivot=(560, 470), anim=dict(pulse=0.4, scaleSpeed=0.6, twinkle=0.5)),
    E("pole", lambda c, m: flat(c, Thick(330, 520, 380, 420, 3), (150, 110, 70)), pivot=(330, 520), anim=dict(swingAngle=4, swingSpeed=0.3)),
    bird_el("egret", 400, 80, s=12, speed=-14, col=(250, 250, 250)),
]

L545_DIFFS = [
    ("roof", 770, 150, 0),
    ("lotus", 680, 330, 0),
    ("frog", 520, 408, 0),
    ("basket", 410, 554, 0),
]


# =================================================================== Level 546 sunflower field
def sunflower(c, x, y, s=1.0, petal=(250, 200, 50), centre=(120, 80, 40)):
    flat(c, Thick(x, y, x, y + 140 * s, 4 * s), (80, 140, 80))
    flat(c, [Ell(x - 12 * s, y + 50 * s, 12 * s, 6 * s), Ell(x + 12 * s, y + 80 * s, 12 * s, 6 * s)], (80, 150, 80))
    piece(c, [Circ(x + 16 * s * math.cos(a), y + 16 * s * math.sin(a), 8 * s) for a in [j * math.pi / 6 for j in range(12)]], petal, border=0.6, shadow=None)
    flat(c, Circ(x, y, 11 * s), centre)


def l546_bg(c, d):
    sky(c, (110, 180, 236), (220, 236, 246), 300)
    cloud_bg(c, 200, 70, 0.9)
    cloud_bg(c, 680, 50, 0.7)
    far_ridge(c, 210, 40, (160, 196, 160), 5461)
    # farmhouse + water tower
    piece(c, RRect(600, 160, 760, 250, 2), (250, 246, 236), border=1.5, shadow=PROP)
    piece(c, Poly([(590, 164), (770, 164), (680, 110)]), (200, 70, 60) if "roof" not in d else (60, 120, 190), border=1.5, shadow=PROP)
    for x in (620, 700):
        flat(c, RRect(x, 186, x + 30, 216, 2), (150, 196, 226))
    flat(c, [Thick(800, 250, 820, 140, 3), Thick(860, 250, 840, 140, 3)], (150, 120, 90))
    piece(c, [RRect(800, 110, 860, 150, 6), Poly([(796, 112), (864, 112), (830, 90)])], (180, 180, 190), border=1.5, shadow=PROP)
    # field ground + rows of sunflowers (back to front)
    piece(c, RRect(-10, 240, 910, 612, 0), (130, 170, 80), shadow=LAYER)
    rnd = random.Random(5462)
    for row, (y, s) in enumerate(((240, 0.6), (290, 0.8), (360, 1.0))):
        x = -10 + row * 20
        while x < 920:
            sunflower(c, x + rnd.uniform(-6, 6), y + rnd.uniform(-6, 6), s=s)
            x += 44 * s + 6
    # dirt path + cyclist parked + girl with hat
    piece(c, Poly([(380, 612), (520, 612), (470, 470), (430, 470)]), (200, 170, 120), shadow=SMALL)
    for wx in (560, 640):
        c.ellipse_ring(wx, 580, 26, 26, 4, (40, 40, 46))
    flat(c, [Thick(560, 580, 590, 540, 4), Thick(590, 540, 630, 540, 4), Thick(630, 540, 640, 580, 4), Thick(590, 540, 600, 580, 4),
             Thick(600, 580, 560, 580, 4)], (220, 70, 70) if "bike" not in d else (60, 140, 200))
    piece(c, RRect(620, 524, 656, 540, 3), (200, 160, 100), border=1, shadow=SMALL)
    modern(c, 300, 600, (250, 250, 250), bottom=(90, 150, 220), hair=(90, 60, 40), h=2.3, style="long", skirt=True)
    piece(c, [Ell(302, 494, 30, 8), Ell(302, 486, 14, 10)], (240, 220, 160) if "hat" not in d else (240, 150, 170), shadow=SMALL)
    flat(c, RRect(290, 488, 314, 494, 2), (220, 70, 90))
    # big sunflowers in the very front
    sunflower(c, 80, 470, s=1.4)
    sunflower(c, 820, 460, s=1.5, petal=(250, 200, 50) if "petals" not in d else (250, 140, 60))
    sunflower(c, 160, 500, s=1.2)


L546_ELEMENTS = [
    E("bee%d" % i, (lambda x, y: lambda c, m: (flat(c, Ell(x, y, 5, 4), (250, 200, 50)), flat(c, Thick(x - 1, y - 4, x - 1, y + 4, 1.4), INK),
                                              flat(c, [Ell(x - 2, y - 6, 4, 3), Ell(x + 3, y - 6, 4, 3)], (240, 250, 255))))(x, y),
      pivot=(x, y), anim=dict(bobAmplitude=(24, 12), bobSpeed=0.4 + i * 0.1, phase=i / 3))
    for i, (x, y) in enumerate(((200, 360), (520, 330), (720, 420)))
] + [
    E("sway", lambda c, m: sunflower(c, 80, 470, s=1.4), pivot=(80, 612), anim=dict(swingAngle=2, swingSpeed=0.3)),
    cloud_el("cloud", 450, 40, 0.6, 7),
    bird_el("bird", 300, 120, s=8, speed=20),
]

L546_DIFFS = [
    ("roof", 680, 140, 0),
    ("bike", 600, 560, 0),
    ("hat", 302, 490, 0),
    ("petals", 820, 460, 0),
]


# =================================================================== Level 547 cactus desert (day / night)
DN547 = day_night(40.0, tint=(0.28, 0.24, 0.48))
SUN547, MOON547 = celestial((450, 320), (380, 260), 40.0)


def l547_bg(c, d):
    sky(c, (120, 180, 236), (250, 216, 170), 320)
    # mesas
    for pts, col in (([(-10, 300), (40, 160), (240, 160), (290, 300)], (200, 110, 80)), ([(560, 300), (620, 190), (760, 190), (820, 300)], (210, 120, 86)),
                     ([(800, 300), (840, 220), (910, 220), (910, 300)], (190, 104, 78))):
        piece(c, Poly(pts), col, border=1.5, shadow=LAYER)
        flat(c, Thick(pts[1][0], pts[1][1] + 30, pts[2][0], pts[2][1] + 30, 4), lit(col, 0.88))
    # desert floor
    piece(c, RRect(-10, 290, 910, 612, 0), (236, 196, 140), shadow=LAYER)
    for k in range(20):
        rnd = random.Random(5471 + k)
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(310, 600), rnd.uniform(20, 50), 4), (222, 182, 126))
    # road
    piece(c, Poly([(380, 612), (560, 612), (480, 300), (460, 300)]), (120, 116, 120), shadow=SMALL)
    flat(c, [Thick(470 + (y - 300) * 0.08, y, 470 + (y - 300) * 0.08, y + 18, 3) for y in range(320, 600, 40)], (250, 220, 90))
    # saguaros
    cactus(c, 140, 470, s=2.0)
    cactus(c, 700, 440, s=1.6, col=(90, 160, 90) if "cactus" not in d else (150, 170, 80))
    cactus(c, 300, 360, s=0.9)
    cactus(c, 840, 520, s=1.3)
    # road sign + tumbleweed + skull
    flat(c, Thick(600, 520, 600, 430, 4), (120, 120, 130))
    piece(c, Poly([(600, 400), (632, 432), (600, 464), (568, 432)]), (250, 200, 50) if "sign" not in d else (90, 160, 220), border=1.5, shadow=PROP)
    flat(c, Thick(586, 432, 614, 432, 3), (40, 40, 50))
    piece(c, [Ell(250, 560, 20, 10), Circ(270, 552, 10)], (246, 240, 226), border=1, shadow=SMALL)
    flat(c, [Circ(268, 550, 2.4), Circ(276, 550, 2.4)], (60, 50, 50))
    # camp: tent + fire pit + coyote
    piece(c, Poly([(30, 600), (130, 600), (80, 520)]), (220, 80, 60) if "tent" not in d else (60, 140, 110), border=1.5, shadow=PROP)
    flat(c, Poly([(70, 600), (90, 600), (80, 540)]), (120, 50, 40))
    piece(c, Ell(200, 600, 30, 8), (120, 110, 110), shadow=SMALL)
    piece(c, [Ell(760, 600, 28, 10), Circ(790, 584, 10), Poly([(786, 576), (788, 562), (794, 574)]), Poly([(794, 574), (800, 562), (802, 578)]),
              Ell(728, 594, 18, 6)] + [RRect(x - 2.4, 594, x + 2.4, 612, 1) for x in (744, 752, 768, 776)],
          (190, 150, 110) if "coyote" not in d else (120, 110, 110), border=1, shadow=PROP)


L547_ELEMENTS = [
    sun_element("sun", (450, 320), SUN547, r=28),
    moon_element("moon", (450, 320), MOON547, r=22),
    star_field("stars", 547, 40, 200),
    E("fire", lambda c, m: (flat(c, Poly([(186, 600), (194, 576), (200, 590), (208, 568), (216, 600)]), (250, 150, 50)),
                            flat(c, Poly([(194, 600), (202, 584), (210, 600)]), (255, 230, 130))),
      pivot=(200, 600), daynight="untinted", anim=dict(stretch=(0.08, 0.2), scaleSpeed=3.0)),
    E("fireglow", lambda c, m: soft_union(c, [Circ(200, 586, 12)], (255, 170, 80), 0.6, spread=50), daynight="night", anim=dict(pulse=0.1, scaleSpeed=1.2)),
    E("tumble", lambda c, m: (c.ellipse_ring(0, 500, 14, 14, 3, (170, 130, 80)), flat(c, [Thick(-10, 492, 10, 508, 2), Thick(10, 492, -10, 508, 2)], (170, 130, 80))),
      pivot=(0, 500), anim=dict(drift_across(-14, 14, 30, start=300), rotateSpeed=120, bobAmplitude=(0, 6), bobSpeed=1.0, bounce=True)),
    bird_el("hawk", 650, 90, s=12, speed=-14, daynight="day"),
]

L547_DIFFS = [
    ("cactus", 700, 400, 0),
    ("sign", 600, 432, 0),
    ("tent", 80, 570, 0),
    ("coyote", 768, 594, 0),
]


# =================================================================== Level 548 turtle beach (day / night)
DN548 = day_night(40.0, tint=(0.24, 0.28, 0.52))
SUN548, MOON548 = celestial((450, 300), (360, 230), 40.0)


def turtle(c, x, y, s=1.0, shell=(110, 140, 90), face_right=False):
    k = 1 if face_right else -1
    piece(c, [Ell(x - 10 * s, y + 6 * s, 6 * s, 3 * s), Ell(x + 10 * s, y + 6 * s, 6 * s, 3 * s), Circ(x + k * 16 * s, y, 5 * s)], (150, 170, 130),
          border=0.8, shadow=None)
    piece(c, Ell(x, y, 13 * s, 9 * s), shell, border=1, shadow=SMALL)
    flat(c, [Thick(x - 6 * s, y - 6 * s, x - 6 * s, y + 6 * s, 1), Thick(x + 6 * s, y - 6 * s, x + 6 * s, y + 6 * s, 1)], lit(shell, 0.8))


def l548_bg(c, d):
    sky(c, (120, 184, 236), (240, 220, 200), 300)
    cloud_bank(c, 130, (250, 248, 244), 5481, k=0.6)
    # sea
    c.gradient(230, 400, (80, 150, 200), (60, 130, 190))
    for k in range(10):
        rnd = random.Random(5482 + k)
        x, y = rnd.uniform(0, 900), rnd.uniform(250, 380)
        flat(c, Thick(x, y, x + rnd.uniform(30, 60), y, 2), (140, 196, 230))
    flat(c, Poly([(-10, 390)] + [(x, 396 + 6 * math.sin(x / 40)) for x in range(0, 920, 20)] + [(910, 420), (-10, 420)]), (240, 246, 250))
    # beach
    piece(c, Poly([(-10, 410), (910, 400), (910, 612), (-10, 612)]), (240, 220, 170), shadow=LAYER)
    for k in range(20):
        rnd = random.Random(5483 + k)
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(430, 600), rnd.uniform(10, 30), 3), (226, 206, 156))
    # palms + dunes (right)
    piece(c, Ell(820, 470, 140, 50), (230, 210, 160), shadow=SMALL)
    palm(c, 780, 470, h=230, lean=-30)
    palm(c, 870, 480, h=190, lean=20, col=(70, 160, 85) if "palm" not in d else (200, 170, 70))
    # hatchlings heading to the sea
    for k, (x, y) in enumerate(((200, 470), (260, 500), (330, 460), (380, 520), (450, 480), (520, 510), (580, 470))):
        turtle(c, x, y, s=1.2, shell=(110, 140, 90) if not (k == 3 and "shell" in d) else (200, 160, 80))
    # nest marker fence with a sign
    for x in (60, 120, 180):
        flat(c, Thick(x, 600, x, 540, 3), (150, 110, 70))
    flat(c, [Thick(60, 552, 180, 552, 2), Thick(60, 576, 180, 576, 2)], (250, 120, 50) if "rope" not in d else (60, 120, 200))
    piece(c, [RRect(100, 500, 160, 536, 3)], (250, 250, 240), border=1.2, shadow=PROP)
    turtle(c, 130, 518, s=1.0)
    # volunteers with a bucket + lantern
    modern(c, 660, 600, (90, 160, 120), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.2, style="long")
    modern(c, 720, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.3)
    piece(c, Poly([(700, 600), (730, 600), (734, 572), (696, 572)]), (60, 140, 220) if "bucket" not in d else (240, 120, 60), border=1.2, shadow=PROP)
    piece(c, [RRect(624, 540, 640, 566, 3)], (60, 60, 70), shadow=SMALL)
    flat(c, RRect(627, 546, 637, 560, 2), (255, 220, 140))


L548_ELEMENTS = [
    sun_element("sun", (450, 300), SUN548, r=26),
    moon_element("moon", (450, 300), MOON548, r=22),
    star_field("stars", 548, 36, 200),
    E("wave", lambda c, m: flat(c, [Ell(200 + k * 160, 404, 60, 5) for k in range(5)], (250, 252, 255, 0.85)), anim=dict(bobAmplitude=(0, 6), bobSpeed=0.3)),
    E("crawl", lambda c, m: turtle(c, 0, 440, s=1.2), anim=dict(driftVelocity=(-14, 0), driftStart=420, driftLength=180)),
    E("lanternglow", lambda c, m: soft_union(c, [Circ(632, 552, 8)], (255, 220, 140), 0.6, spread=36), daynight="night", anim=dict(pulse=0.1, scaleSpeed=1.0)),
    bird_el("gull", 300, 160, s=9, speed=-20, daynight="day"),
]

L548_DIFFS = [
    ("shell", 380, 520, 0),
    ("rope", 120, 564, 0),
    ("bucket", 715, 586, 0),
    ("palm", 890, 290, 0),
]


# =================================================================== Level 549 autumn mountain trail (rain showers)
STEPS549 = [(CLEAR, 12), (OVERCAST, 4), (RAIN, 10), (OVERCAST, 4)]


def maple(c, x, base, s=1.0, col=(220, 90, 50)):
    piece(c, [Thick(x, base, x, base - 50 * s, 7 * s), Thick(x, base - 40 * s, x - 20 * s, base - 64 * s, 4 * s), Thick(x, base - 44 * s, x + 22 * s, base - 70 * s, 4 * s)],
          (110, 76, 60), shadow=PROP)
    piece(c, [Circ(x - 24 * s, base - 74 * s, 22 * s), Circ(x, base - 90 * s, 28 * s), Circ(x + 26 * s, base - 76 * s, 22 * s), Circ(x - 4 * s, base - 64 * s, 20 * s)],
          col, shadow=PROP)
    flat(c, [Circ(x - 10 * s, base - 98 * s, 9 * s), Circ(x + 20 * s, base - 84 * s, 7 * s)], lit(col, 1.1))


def l549_bg(c, d):
    sky(c, (140, 190, 230), (236, 230, 220), 300)
    far_ridge(c, 120, 80, (170, 170, 190), 5491)
    far_ridge(c, 190, 60, (190, 150, 130), 5492)
    piece(c, Poly([(-10, 260), (300, 230), (600, 250), (910, 220), (910, 612), (-10, 612)]), (180, 150, 90), shadow=LAYER)
    # maples
    for x, b, s, col in ((60, 300, 1.4, (220, 90, 50)), (200, 280, 1.1, (240, 160, 50)), (660, 280, 1.2, (230, 120, 50)), (820, 300, 1.5, (210, 70, 60))):
        maple(c, x, b, s=s, col=col if not (x == 660 and "maple" in d) else (120, 160, 80))
    # winding trail
    piece(c, Poly([(380, 612), (540, 612), (520, 520), (420, 440), (480, 330), (450, 260), (420, 260), (440, 330), (380, 440), (440, 520)]),
          (210, 186, 140), shadow=SMALL)
    # stream + footbridge
    piece(c, Poly([(-10, 470), (300, 440), (900, 500), (910, 540), (300, 480), (-10, 510)]), (120, 180, 210), border=1.5, shadow=SMALL)
    piece(c, RRect(360, 450, 560, 466, 3), (150, 110, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(370, 430, 550, 430, 3)] + [Thick(380 + k * 30, 430, 380 + k * 30, 450, 2) for k in range(7)],
         (150, 110, 70) if "bridge" not in d else (220, 70, 70))
    # signpost
    flat(c, Thick(620, 440, 620, 360, 5), (120, 90, 60))
    for k, (y, dx) in enumerate(((364, 1), (390, -1))):
        col = (230, 200, 120) if not (k == 1 and "sign" in d) else (110, 180, 210)
        pts = [(620, y), (620 + dx * 60, y), (620 + dx * 72, y + 10), (620 + dx * 60, y + 20), (620, y + 20)]
        piece(c, Poly(pts), col, border=1.2, shadow=SMALL)
    # hikers
    hiker(c, 260, 600, (60, 110, 180), (240, 120, 60), h=2.3)
    hiker(c, 330, 600, (220, 90, 120), (90, 150, 110) if "pack" not in d else (250, 210, 70), h=2.2, hair=(90, 60, 40), style="long")
    # bench + fallen leaves
    piece(c, [RRect(700, 560, 860, 572, 3), RRect(706, 572, 714, 606, 2), RRect(846, 572, 854, 606, 2), RRect(700, 540, 860, 550, 3)], (130, 90, 60),
          border=1.2, shadow=PROP)
    rnd = random.Random(5493)
    for _ in range(30):
        x, y = rnd.uniform(0, 900), rnd.uniform(520, 600)
        flat(c, Ell(x, y, 5, 3), rnd.choice([(220, 90, 50), (240, 160, 50), (200, 70, 60)]))
    rock(c, 120, 600, s=1.5)


L549_ELEMENTS = [
    E("leaf%d" % i, (lambda x: lambda c, m: flat(c, Ell(x, 120, 6, 3), (230, 120, 50)))(x),
      anim=dict(driftVelocity=(10, -24), driftLength=360, driftFade=True, spinSpeed=0.8, bobAmplitude=(10, 0), bobSpeed=0.5, phase=i / 3))
    for i, x in enumerate((100, 700, 820))
] + [
    paper_sun("sun", 760, 60, r=30),
    cloud("cloudA", 200, 50, 1.2, (176, 182, 196), W_(OVERCAST, RAIN)),
    cloud("cloudB", 560, 40, 1.4, (168, 174, 190), W_(OVERCAST, RAIN)),
    puddles("puddles", [Ell(470, 580, 30, 5), Ell(480, 400, 18, 4)], mask=W_(RAIN)),
    rain_layer("rain", 549, 70, 24, 1.3, 0.6, 260, mask=W_(RAIN)),
] + splash_rings("splash", [(200, 490, 7), (700, 520, 6)], mask=W_(RAIN))

L549_DIFFS = [
    ("maple", 660, 200, 0),
    ("bridge", 460, 440, 0),
    ("sign", 584, 400, 0),
    ("pack", 343, 528, 0),
]


LEVELS = [
    ("Level540", "峡谷瀑布", l540_bg, L540_ELEMENTS, L540_DIFFS, 60, OPTS),
    ("Level541", "海狮海湾", l541_bg, L541_ELEMENTS, L541_DIFFS, 60, OPTS),
    ("Level542", "林间小鹿", l542_bg, L542_ELEMENTS, L542_DIFFS, 60, OPTS),
    ("Level543", "雪原狐狸", l543_bg, L543_ELEMENTS, L543_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS543, blend=3.0), anim_seconds=24.0, frames=80)),
    ("Level544", "雪猴温泉", l544_bg, L544_ELEMENTS, L544_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS544, blend=3.0), anim_seconds=24.0, frames=80)),
    ("Level545", "荷塘", l545_bg, L545_ELEMENTS, L545_DIFFS, 60, OPTS),
    ("Level546", "向日葵田", l546_bg, L546_ELEMENTS, L546_DIFFS, 60, OPTS),
    ("Level547", "仙人掌荒野", l547_bg, L547_ELEMENTS, L547_DIFFS, 60, dict(OPTS, day_night=DN547, anim_seconds=40.0, frames=80)),
    ("Level548", "海龟沙滩", l548_bg, L548_ELEMENTS, L548_DIFFS, 60, dict(OPTS, day_night=DN548, anim_seconds=40.0, frames=80)),
    ("Level549", "秋日山径", l549_bg, L549_ELEMENTS, L549_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS549, blend=3.0), anim_seconds=30.0, frames=80)),
]
