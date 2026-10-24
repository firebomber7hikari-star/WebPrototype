# -*- coding: utf-8 -*-
"""Mixed themes part 5 (paper-craft side views of landscapes, full-bleed, original designs, no brands):
  Level275 郁金香风车 - striped tulip fields, windmills, a canal with a boat, cyclists
  Level276 高山牧场   - an alpine pasture: snowy peaks, chalets, cable car, cows with bells, a hiker
  Level277 梯田       - rice terraces on a hillside: farmers in straw hats, a water buffalo, a hut
  Level278 红岩峡谷   - a red-rock canyon: mesas, an arch, a river with a raft, cactus, a hawk
  Level279 枫叶溪谷   - an autumn maple valley: red bridge over a stream, waterfall, hikers, a deer
  Level280 萤火虫之夜 - a summer night meadow: tent, campfire, fireflies, moon over the pond, frogs
  Level281 红树林     - a mangrove channel: stilt roots, a heron, a kayak, crabs, a boardwalk
  Level282 薰衣草花田 - lavender rows to the horizon, a stone farmhouse, sunflowers, a painter, beehives
  Level283 树屋村     - a treehouse village in giant trees: rope bridges, ladders, lanterns, children
  Level284 峡湾       - a fjord: steep cliffs, waterfalls, a cruise ship, red cabins, a fishing boat
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bush, cactus, cloud_bg, cloud_el, drift_across, fish, layer, rock, sky, smoke_el, stars_bg, sun_bg,
                 tree_pine, tree_round)
from fills import far_forest, far_ridge, far_round_trees
from levels_akiba import modern
from levels_festival import npiece
from levels_mix2 import wheel
from levels_mix3 import cow

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def straw_hat(c, hx, hy, h, col=(230, 200, 120)):
    piece(c, Poly([(hx - 16 * h, hy - 4 * h), (hx + 16 * h, hy - 4 * h), (hx, hy - 16 * h)]), col, border=1, shadow=SMALL)


def windmill(c, x, base, s, body, cap):
    piece(c, Poly([(x - 24 * s, base), (x + 24 * s, base), (x + 14 * s, base - 90 * s), (x - 14 * s, base - 90 * s)]), body, border=1.5, shadow=PROP)
    piece(c, Poly([(x - 18 * s, base - 88 * s), (x + 18 * s, base - 88 * s), (x, base - 112 * s)]), cap, border=1.5, shadow=PROP)
    flat(c, RRect(x - 7 * s, base - 22 * s, x + 7 * s, base, 2), (90, 70, 60))
    flat(c, RRect(x - 6 * s, base - 64 * s, x + 6 * s, base - 52 * s, 2), (250, 230, 160))


def sails_el(eid, x, y, s, speed, col=(250, 246, 236)):
    def d(c, m):
        for k in range(4):
            a = k * math.pi / 2 + 0.3
            ex, ey = x + 60 * s * math.cos(a), y + 60 * s * math.sin(a)
            nx, ny = -math.sin(a) * 9 * s, math.cos(a) * 9 * s
            piece(c, Poly([(x, y), (ex, ey), (ex + nx, ey + ny), (x + nx * 0.3, y + ny * 0.3)]), col, border=1, shadow=SMALL)
        flat(c, Circ(x, y, 5 * s), (90, 70, 60))
    return E(eid, d, pivot=(x, y), anim=dict(rotateSpeed=speed))


# =================================================================== Level 275 tulip windmills
TULIPS = [(230, 60, 70), (250, 200, 60), (240, 130, 170), (250, 140, 50), (180, 90, 200)]


def l275_bg(c, d):
    sky(c, (120, 180, 240), (220, 236, 248), H)
    cloud_bg(c, 120, 60, 0.6)
    cloud_bg(c, 600, 40, 0.5)
    layer(c, 200, [(6, 0.01, 0.4), (3, 0.04, 1.0)], (150, 190, 120))
    far_round_trees(c, 206, 14, (110, 160, 100), 2751)
    # windmills (sails are elements)
    windmill(c, 140, 240, 1.0, (150, 110, 90), (90, 70, 60) if "cap" not in d else (60, 120, 190))
    windmill(c, 760, 230, 0.8, (160, 120, 100), (90, 70, 60))
    # farmhouse (centre back)
    piece(c, RRect(400, 170, 500, 230, 2), (200, 90, 70), border=1.5, shadow=PROP)
    roof = (60, 70, 80) if "roof" not in d else (230, 160, 60)
    piece(c, Poly([(390, 172), (510, 172), (450, 120)]), roof, border=1.5, shadow=PROP)
    flat(c, [RRect(416, 190, 436, 210, 2), RRect(464, 190, 484, 210, 2)], (250, 250, 236))
    # tulip stripes
    c.rect(0, 240, W, H, (110, 160, 90))
    for k in range(7):
        y0 = 250 + k * 30 + k * k * 1.5
        col = TULIPS[k % 5]
        flat(c, Poly([(0, y0), (W, y0 - 6), (W, y0 + 14 + k * 2), (0, y0 + 18 + k * 2)]), col)
        if k == 2 and "stripe" in d:
            flat(c, Poly([(600, y0 - 4), (840, y0 - 5.6), (840, y0 + 13.2 + k * 2), (600, y0 + 15 + k * 2)]), (250, 250, 246))
        flat(c, Thick(0, y0 + 20 + k * 2.4, W, y0 + 14 + k * 2.4, 4 + k), (100, 150, 80))
    # canal + boat (left middle)
    flat(c, Poly([(0, 400), (330, 380), (330, 410), (0, 440)]), (90, 150, 200))
    boat = (60, 110, 160) if "boat" not in d else (220, 80, 70)
    piece(c, Poly([(70, 404), (210, 396), (196, 418), (84, 424)]), boat, border=1.2, shadow=SMALL)
    modern(c, 150, 406, (240, 240, 230), bottom=(50, 50, 70), hair=(200, 160, 90), h=1.1)
    # cyclist (centre)
    modern(c, 470, 470, (90, 150, 220) if "cyclist" not in d else (250, 200, 60), bottom=(60, 60, 80), hair=(200, 160, 90), h=1.6)
    wheel(c, 446, 480, 16, tyre=(40, 40, 46), hub=(200, 200, 210))
    wheel(c, 500, 480, 16, tyre=(40, 40, 46), hub=(200, 200, 210))
    flat(c, [Thick(446, 480, 472, 456, 3), Thick(472, 456, 500, 480, 3)], (200, 60, 60))
    # basket of cut tulips (right front)
    piece(c, Poly([(720, 590), (840, 590), (856, 530), (704, 530)]), (190, 140, 80), border=1.5, shadow=PROP)
    bunch = (240, 130, 170) if "bunch" not in d else (250, 200, 60)
    for k in range(7):
        x = 720 + k * 20
        flat(c, Thick(x, 530, x + 4, 500, 2), (90, 140, 70))
        piece(c, Poly([(x - 6, 506), (x + 10, 506), (x + 10, 490), (x + 2, 496), (x - 6, 490)]), bunch, shadow=None)
    # wooden clogs (left front)
    clog = (250, 220, 120) if "clog" not in d else (90, 160, 220)
    for x in (80, 140):
        piece(c, [Ell(x, 580, 28, 12), Ell(x + 14, 572, 12, 10)], clog, border=1.2, shadow=SMALL)
    # sign post (centre right)
    sign = (240, 240, 230) if "sign" not in d else (240, 140, 60)
    flat(c, Thick(620, 600, 620, 500, 4), (120, 90, 60))
    piece(c, Poly([(580, 500), (670, 500), (684, 514), (670, 528), (580, 528)]), sign, border=1.2, shadow=SMALL)


L275_ELEMENTS = [
    sails_el("sails1", 140, 162, 1.0, 30),
    sails_el("sails2", 760, 168, 0.8, -40),
    bird_el("bird", 400, 70, s=9, speed=16),
    cloud_el("cloud", 300, 90, 0.4, 8),
]

L275_DIFFS = [
    ("cap", 140, 140, 0),
    ("roof", 450, 150, 0),
    ("stripe", 720, 320, 0),
    ("boat", 140, 410, 0),
    ("cyclist", 470, 420, 0),
    ("bunch", 780, 500, 0),
    ("clog", 110, 576, 0),
    ("sign", 630, 514, 0),
]


# =================================================================== Level 276 alpine pasture
def chalet(c, x, base, w, h, wall, roof, flowers=(230, 60, 70)):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), wall, border=1.5, shadow=PROP)
    for y in range(int(base - h) + 10, int(base), 12):
        flat(c, Thick(x - w / 2, y, x + w / 2, y, 1.2), lit(wall, 0.85))
    piece(c, Poly([(x - w / 2 - 16, base - h + 4), (x + w / 2 + 16, base - h + 4), (x, base - h - w * 0.4)]), roof, border=1.5, shadow=PROP)
    for k in (-1, 1):
        flat(c, RRect(x + k * w * 0.22 - 10, base - h * 0.7, x + k * w * 0.22 + 10, base - h * 0.4, 2), (250, 240, 200))
        flat(c, RRect(x + k * w * 0.22 - 14, base - h * 0.4, x + k * w * 0.22 + 14, base - h * 0.32, 2), flowers)


def l276_bg(c, d):
    sky(c, (100, 170, 240), (220, 236, 250), H)
    # snowy peaks
    peaks = [(-40, 260), (80, 90), (200, 200), (330, 60), (470, 210), (600, 80), (760, 190), (900, 70), (960, 260)]
    piece(c, Poly(peaks + [(960, 300), (-40, 300)]), (150, 170, 200), border=1.5, shadow=LAYER)
    for (x0, y0), (x1, y1), (x2, y2) in zip(peaks, peaks[1:], peaks[2:]):
        if y1 < y0 and y1 < y2:
            flat(c, Poly([(x1, y1), (x1 - 34, y1 + 50), (x1 - 10, y1 + 40), (x1 + 6, y1 + 56), (x1 + 34, y1 + 46)]), (250, 250, 252))
    flake = (250, 250, 252) if "peak" not in d else (150, 170, 200)
    flat(c, Poly([(600, 80), (566, 130), (590, 120), (606, 136), (634, 126)]), flake)
    far_forest(c, 260, 50, (70, 120, 90), 2761)
    # cable car line (right top)
    flat(c, Thick(640, 120, 900, 40, 2), (60, 60, 70))
    car = (220, 60, 60) if "cablecar" not in d else (250, 200, 60)
    flat(c, Thick(770, 80, 770, 104, 2), (60, 60, 70))
    piece(c, RRect(744, 102, 796, 140, 6), car, border=1.2, shadow=SMALL)
    flat(c, RRect(752, 108, 788, 122, 2), (200, 230, 246))
    # meadow
    layer(c, 280, [(16, 0.008, 0.4), (8, 0.03, 1.0)], (130, 190, 90))
    c.rect(0, 340, W, H, (120, 180, 84))
    layer(c, 330, [(10, 0.01, 1.4), (5, 0.04, 0.4)], (126, 186, 88))
    # chalets
    chalet(c, 160, 330, 120, 70, (190, 130, 80) if "flowers" not in d else (230, 220, 196), (90, 60, 50))
    chalet(c, 600, 300, 90, 54, (180, 120, 70), (80, 60, 50))
    # cows with bells
    cow(c, 330, 440, 1.3, spots=(150, 90, 50))
    bell = (230, 190, 60) if "bell" not in d else (120, 120, 140)
    flat(c, Thick(362, 396, 394, 392, 4), (200, 60, 50))
    piece(c, Poly([(370, 398), (388, 398), (396, 426), (362, 426)]), bell, border=1, shadow=None)
    cow(c, 760, 420, 1.0, spots=(150, 90, 50), face=-1)
    # wildflowers
    rnd = random.Random(2762)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(470, 600)
        if 380 < x < 540 and y > 500:
            continue
        flat(c, Circ(x, y, 3), rnd.choice([(250, 250, 246), (250, 210, 60), (200, 120, 220)]))
    # hiker with backpack (centre front)
    hx, hy = modern(c, 460, 590, (200, 80, 60), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.2)
    pack = (60, 120, 90) if "pack" not in d else (240, 180, 60)
    piece(c, RRect(424, 490, 446, 540, 6), pack, border=1.2, shadow=SMALL)
    flat(c, Thick(500, 600, 492, 500, 3), (120, 90, 60))
    # milk churn + fence (left front)
    for x in range(0, 280, 40):
        flat(c, Thick(x, 600, x, 540, 4), (150, 110, 70))
    flat(c, [Thick(0, 556, 280, 556, 3), Thick(0, 576, 280, 576, 3)], (150, 110, 70))
    # alphorn (right front)
    horn = (180, 120, 70) if "horn" not in d else (90, 90, 110)
    piece(c, [Thick(640, 520, 860, 580, 6), Ell(866, 582, 18, 12)], horn, border=1.2, shadow=SMALL)
    modern(c, 640, 600, (240, 240, 230), bottom=(60, 50, 50), hair=(200, 200, 200), h=2.0)


L276_ELEMENTS = [
    bird_el("eagle", 260, 60, s=12, speed=14),
    cloud_el("cloud", 450, 160, 0.5, 6),
    E("tail", lambda c, m: flat(c, Thick(286, 394, 274, 420, 2.4), (250, 250, 246)), pivot=(286, 394), anim=dict(swingAngle=20, swingSpeed=1.4)),
    E("smoke", lambda c, m: piece(c, Circ(190, 250, 8), (240, 240, 240), shadow=None), pivot=(190, 250),
      anim=dict(driftVelocity=(6, -20), driftLength=50, driftFade=True, driftGrow=1.5)),
]

L276_DIFFS = [
    ("peak", 600, 110, 0),
    ("cablecar", 770, 118, 0),
    ("flowers", 160, 292, 0),
    ("bell", 380, 412, 0),
    ("pack", 435, 515, 0),
    ("horn", 760, 552, 0),
]


# =================================================================== Level 277 rice terraces
def buffalo(c, x, base, s, col=(90, 90, 100)):
    for lx in (-20, -8, 14, 24):
        flat(c, RRect(x + lx * s - 4 * s, base - 22 * s, x + lx * s + 4 * s, base, 2), lit(col, 0.85))
    piece(c, [Ell(x, base - 32 * s, 32 * s, 14 * s), Ell(x + 36 * s, base - 30 * s, 12 * s, 10 * s)], col, border=1.2, shadow=PROP)
    flat(c, [Thick(x + 30 * s, base - 38 * s, x + 18 * s, base - 50 * s, 3 * s), Thick(x + 42 * s, base - 38 * s, x + 54 * s, base - 50 * s, 3 * s)], (220, 210, 190))
    flat(c, Circ(x + 40 * s, base - 32 * s, 1.6 * s), INK)


def l277_bg(c, d):
    sky(c, (160, 200, 230), (240, 236, 220), H)
    sun = (250, 210, 120) if "sun" not in d else (240, 140, 110)
    sun_bg(c, 760, 70, 30, col=sun)
    far_ridge(c, 150, 60, (170, 190, 190), 2771)
    far_ridge(c, 190, 40, (140, 170, 160), 2772)
    # terraces: stacked curved strips
    for k in range(9):
        top = 190 + k * 46
        g = (120 + k * 6, 180 + k * 3, 90)
        piece(c, hill_strip(top, [(10, 0.012, k * 0.7), (5, 0.03, k)]), g, border=1.2, shadow=(1, 3, 6, 0.3))
        flat(c, Poly([(x, hill_y_(top, k, x) + 6) for x in range(-60, 961, 20)] + [(960, hill_y_(top, k, 960) + 14), (-60, hill_y_(top, k, -60) + 14)]),
             (150, 200, 220) if k % 2 == 0 else lit(g, 1.1))
    # hut (left middle)
    piece(c, RRect(80, 220, 170, 270, 2), (190, 160, 110), border=1.5, shadow=PROP)
    hroof = (200, 170, 90) if "hut" not in d else (120, 80, 60)
    piece(c, Poly([(60, 224), (190, 224), (125, 180)]), hroof, border=1.5, shadow=PROP)
    flat(c, RRect(112, 240, 138, 270, 2), (90, 70, 60))
    # trees on the ridge (right)
    tree_round(c, 640, 240, 0.9, col=(90, 150, 90))
    tree_round(c, 860, 250, 1.1, col=(80, 140, 84))
    # buffalo with a farmer (centre)
    buffalo(c, 450, 380, 1.5, col=(90, 90, 100) if "buffalo" not in d else (170, 120, 80))
    # farmers planting (left front, right middle)
    for x, base, top, key in ((200, 500, (90, 120, 160), "shirt"), (720, 440, (200, 90, 80), None), (520, 560, (120, 160, 120), None)):
        hx, hy = modern(c, x, base, top if not (key and key in d) else (240, 200, 60), bottom=(60, 60, 70), hair=(30, 30, 34), h=1.8)
        straw_hat(c, hx, hy, 1.8, (230, 200, 120) if not (x == 720 and "hat" in d) else (220, 80, 80))
    # seedling basket (right front)
    bask = (190, 140, 80) if "basket" not in d else (90, 140, 190)
    piece(c, Poly([(780, 590), (880, 590), (890, 540), (770, 540)]), bask, border=1.5, shadow=PROP)
    for x in range(784, 880, 12):
        flat(c, Thick(x, 540, x + 3, 516, 2), (110, 180, 80))
    # egret (left front)
    if "egret" not in d:
        piece(c, [Ell(70, 560, 20, 10), Thick(84, 552, 96, 520, 3), Ell(100, 518, 8, 5)], (250, 250, 246), border=1, shadow=SMALL)
        flat(c, [Thick(106, 518, 120, 520, 2), Thick(66, 570, 64, 594, 1.6), Thick(74, 570, 76, 594, 1.6)], (240, 190, 60))


def hill_y_(top, k, x):
    from paper import hill_y
    return hill_y(top, [(10, 0.012, k * 0.7), (5, 0.03, k)], x)


L277_ELEMENTS = [
    bird_el("bird", 300, 80, s=9, speed=14),
    cloud_el("cloud", 480, 110, 0.5, 6),
    E("ripple", lambda c, m: c.ellipse_ring(330, 470, 20, 5, 1.6, (200, 230, 240)), pivot=(330, 470), anim=dict(stretch=(0.5, 0.5), scaleSpeed=1.0)),
    E("tail", lambda c, m: flat(c, Thick(404, 352, 396, 372, 2.4), (90, 90, 100)), pivot=(404, 352), anim=dict(swingAngle=20, swingSpeed=1.4)),
]

L277_DIFFS = [
    ("hut", 125, 205, 0),
    ("sun", 760, 70, 0),
    ("buffalo", 470, 340, 0),
    ("shirt", 200, 440, 0),
    ("hat", 722, 350, 0),
    ("basket", 830, 556, 0),
    ("egret", 88, 548, 0),
]


# =================================================================== Level 278 red canyon
ROCK = (200, 100, 70)


def mesa(c, x0, x1, top, base, col):
    piece(c, Poly([(x0, base), (x0 + 20, top + 20), (x0 + 30, top), (x1 - 30, top), (x1 - 20, top + 20), (x1, base)]), col, border=1.5, shadow=LAYER)
    for k in range(1, 4):
        y = top + (base - top) * k / 4
        flat(c, Thick(x0 + 10 + k * 2, y, x1 - 10 - k * 2, y, 2), lit(col, 0.86))


def l278_bg(c, d):
    sky(c, (90, 160, 230), (250, 220, 180), H)
    sun_bg(c, 120, 70, 28, col=(250, 220, 120))
    mesa(c, 180, 380, 120, 260, (220, 150, 120))
    mesa(c, 600, 860, 90, 260, (220, 150, 120))
    # stone arch (centre back)
    arch = (210, 120, 80) if "arch" not in d else (150, 140, 150)
    piece(c, [Poly([(400, 260), (420, 150), (520, 140), (540, 260), (510, 260), (500, 190), (450, 186), (430, 260)])], arch, border=1.5, shadow=PROP)
    # near canyon walls
    piece(c, Poly([(-20, 600), (-20, 200), (60, 210), (120, 300), (200, 330), (240, 420), (220, 600)]), ROCK, border=1.5, shadow=LAYER)
    piece(c, Poly([(920, 600), (920, 180), (840, 200), (780, 290), (700, 320), (660, 420), (680, 600)]), ROCK, border=1.5, shadow=LAYER)
    for k in range(5):
        flat(c, Thick(0, 260 + k * 60, 160 + k * 14, 300 + k * 60, 3), lit(ROCK, 0.84))
        flat(c, Thick(920, 240 + k * 60, 760 - k * 12, 290 + k * 60, 3), lit(ROCK, 0.84))
    # river
    flat(c, Poly([(240, 600), (300, 420), (380, 340), (520, 330), (620, 420), (680, 600)]), (220, 190, 150))
    flat(c, Poly([(300, 600), (340, 460), (400, 380), (500, 370), (570, 440), (620, 600)]), (90, 160, 190))
    for k in range(6):
        flat(c, Thick(360 + k * 30, 420 + k * 26, 400 + k * 30, 420 + k * 26, 1.6), (160, 210, 230))
    # raft with paddlers (centre)
    raft = (240, 200, 60) if "raft" not in d else (220, 60, 60)
    piece(c, [RRect(400, 470, 520, 500, 14)], raft, border=1.5, shadow=SMALL)
    for x, col in ((430, (220, 80, 70)), (490, (90, 140, 210))):
        hx, hy = modern(c, x, 480, col, bottom=(60, 60, 70), hair=(60, 40, 30), h=1.3)
        piece(c, Ell(hx, hy - 6, 9, 6), (250, 250, 246), shadow=None)
    # cactus (left wall ledge) + flower
    cactus(c, 100, 330, 1.1)
    flower = (240, 90, 140) if "bloom" not in d else (250, 220, 60)
    flat(c, [Circ(100, 252, 7)], flower)
    # hawk perched on the right wall
    hawk = (130, 90, 60) if "hawk" not in d else (60, 60, 70)
    piece(c, [Ell(800, 172, 14, 22), Circ(806, 146, 9), Poly([(794, 190), (806, 190), (800, 214)])], hawk, border=1, shadow=SMALL)
    flat(c, [Ell(802, 176, 7, 12), Poly([(812, 144), (820, 148), (812, 152)])], (240, 220, 180))
    # campsite on a sandbar (right front)
    tent = (60, 140, 120) if "tent" not in d else (240, 140, 50)
    piece(c, Poly([(700, 560), (820, 560), (760, 480)]), tent, border=1.5, shadow=PROP)
    flat(c, Poly([(752, 560), (768, 560), (760, 500)]), lit(tent, 0.6))
    # rocks + bones-free skull? no: boulders (left front)
    rock(c, 90, 590, 2.0, col=(170, 90, 60))
    rock(c, 170, 596, 1.2, col=(190, 110, 80))
    # lizard on the left boulder
    if "lizard" not in d:
        piece(c, [Ell(90, 546, 22, 6), Thick(70, 546, 46, 556, 3), Circ(114, 544, 6)], (90, 170, 90), border=1, shadow=None)


L278_ELEMENTS = [
    bird_el("vulture", 520, 60, s=12, speed=-12),
    E("splash", lambda c, m: [flat(c, Circ(x, 504, 3), (220, 240, 250)) for x in (396, 524)], pivot=(460, 504), daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=1.6)),
    E("raftbob", lambda c, m: flat(c, Thick(456, 470, 476, 510, 3), (150, 110, 70)), pivot=(466, 490), anim=dict(swingAngle=20, swingSpeed=1.2)),
    E("dust", lambda c, m: piece(c, Circ(300, 320, 6), (230, 200, 170), shadow=None), pivot=(300, 320),
      anim=dict(driftVelocity=(30, -6), driftLength=120, driftFade=True, driftGrow=2.0)),
]

L278_DIFFS = [
    ("arch", 470, 190, 0),
    ("bloom", 100, 252, 0),
    ("hawk", 804, 172, 0),
    ("raft", 460, 486, 0),
    ("tent", 760, 530, 0),
    ("lizard", 90, 548, 0),
]


# =================================================================== Level 279 maple valley
def maple(c, x, base, s, col, trunk=(110, 70, 50)):
    piece(c, [Thick(x, base, x, base - 50 * s, 6 * s), Thick(x, base - 40 * s, x - 20 * s, base - 70 * s, 3 * s), Thick(x, base - 40 * s, x + 24 * s, base - 72 * s, 3 * s)],
          trunk, shadow=PROP)
    piece(c, [Circ(x, base - 90 * s, 30 * s), Circ(x - 28 * s, base - 72 * s, 22 * s), Circ(x + 28 * s, base - 74 * s, 22 * s), Circ(x - 10 * s, base - 110 * s, 20 * s)], col,
          shadow=PROP)
    flat(c, Circ(x - 12 * s, base - 98 * s, 10 * s), lit(col, 1.12))


def l279_bg(c, d):
    sky(c, (150, 196, 236), (240, 230, 210), H)
    cloud_bg(c, 680, 60, 0.6)
    far_ridge(c, 160, 60, (190, 170, 170), 2791)
    far_round_trees(c, 200, 22, (220, 130, 90), 2792)
    # waterfall (centre back)
    piece(c, Poly([(380, 120), (520, 120), (540, 300), (360, 300)]), (150, 140, 140), border=1.5, shadow=LAYER)
    flat(c, Poly([(430, 120), (470, 120), (480, 300), (420, 300)]), (220, 236, 246))
    # pagoda roof on the hill (left top)
    pag = (180, 60, 50) if "pagoda" not in d else (60, 110, 160)
    piece(c, RRect(110, 150, 150, 200, 1), (240, 230, 210), border=1.2, shadow=SMALL)
    for k in range(3):
        piece(c, Poly([(90 + k * 8, 156 - k * 26), (170 - k * 8, 156 - k * 26), (150 - k * 8, 144 - k * 26), (110 + k * 8, 144 - k * 26)]), pag, border=1.2, shadow=SMALL)
    # valley slopes with maples
    layer(c, 260, [(16, 0.008, 0.2), (8, 0.03, 1.0)], (200, 150, 90))
    maple(c, 120, 330, 1.3, (220, 70, 50) if "maple" not in d else (250, 200, 60))
    maple(c, 270, 300, 1.0, (240, 140, 50))
    maple(c, 640, 300, 1.0, (230, 90, 60))
    maple(c, 800, 330, 1.3, (250, 180, 60))
    # stream
    c.rect(0, 330, W, H, (170, 140, 90))
    flat(c, Poly([(420, 300), (480, 300), (560, 400), (700, 500), (760, 600), (360, 600), (420, 480), (380, 380)]), (110, 170, 200))
    for k in range(5):
        flat(c, Thick(420 + k * 16, 360 + k * 50, 450 + k * 16, 360 + k * 50, 1.6), (180, 220, 236))
    # red arched bridge
    br = (210, 60, 50) if "bridge" not in d else (140, 100, 70)
    top = [(450 - 180 * math.cos(math.pi * k / 16), 440 - 56 * math.sin(math.pi * k / 16)) for k in range(17)]
    bot = [(450 - 150 * math.cos(math.pi * k / 16), 446 - 36 * math.sin(math.pi * k / 16)) for k in range(16, -1, -1)]
    piece(c, Poly(top + bot), br, border=1.5, shadow=PROP)
    for k in range(0, 17, 2):
        x, y = top[k]
        flat(c, Thick(x, y, x, y - 24, 3), br)
    flat(c, Poly([(x, y - 22) for x, y in top] + [(x, y - 18) for x, y in reversed(top)]), br)
    # hikers on the bridge
    modern(c, 420, 384, (90, 140, 200) if "hiker" not in d else (240, 200, 60), bottom=(60, 60, 70), hair=(60, 40, 30), h=1.5)
    modern(c, 470, 382, (220, 120, 140), bottom=(60, 60, 70), hair=(30, 30, 34), h=1.4, style="long")
    # shrubs + stream-bank rocks
    for x, base, col in ((280, 540, (220, 90, 60)), (640, 470, (240, 160, 60)), (700, 590, (210, 80, 60)), (40, 420, (240, 150, 60)), (860, 400, (220, 100, 60))):
        bush(c, x, base, 1.4, col=col)
    for x, base in ((360, 520), (560, 450), (330, 600)):
        rock(c, x, base, 0.9, col=(150, 140, 130))
    # deer (left front)
    if "deer" not in d:
        piece(c, [Ell(140, 530, 36, 16), Ell(176, 500, 10, 12), Poly([(160, 518), (176, 490), (186, 500), (174, 526)]), RRect(114, 536, 120, 580, 1),
                  RRect(130, 538, 136, 580, 1), RRect(150, 538, 156, 580, 1), RRect(164, 536, 170, 580, 1)], (180, 120, 70), shadow=PROP)
        flat(c, [Circ(130, 524, 3), Circ(146, 520, 3), Circ(118, 520, 3)], (250, 240, 220))
        flat(c, Circ(180, 498, 1.8), INK)
    # stone lantern + leaf pile (right front)
    lan = (180, 176, 166) if "lantern" not in d else (110, 110, 120)
    piece(c, [RRect(800, 560, 860, 576, 2), RRect(818, 520, 842, 560, 2), RRect(804, 496, 856, 522, 3), Poly([(792, 498), (868, 498), (830, 474)])], lan, border=1.2,
          shadow=PROP)
    flat(c, RRect(820, 502, 840, 516, 2), (250, 220, 140))
    for x, col in ((220, (230, 90, 60)), (250, (250, 180, 60)), (600, (230, 70, 50)), (720, (250, 180, 60))):
        flat(c, [Ell(x, 590, 18, 6), Ell(x + 20, 594, 14, 5)], col)


def falling_leaf(eid, x, y, col, phase):
    return E(eid, lambda c, m: flat(c, Poly(star_pts(x, y, 7, 3, points=5)), col), pivot=(x, y),
             anim=dict(driftVelocity=(-10, 40), driftLength=140, driftFade=True, swingAngle=60, swingSpeed=1.2, phase=phase))


L279_ELEMENTS = [
    falling_leaf("leaf1", 300, 160, (230, 80, 50), 0.0),
    falling_leaf("leaf2", 680, 150, (250, 180, 60), 0.4),
    falling_leaf("leaf3", 560, 300, (230, 90, 60), 0.7),
    E("fall", lambda c, m: [flat(c, Thick(x, 130, x, 290, 2), (250, 252, 255)) for x in (440, 452, 466)], daynight="untinted",
      anim=dict(driftVelocity=(0, 60), driftLength=20, driftFade=False)),
    bird_el("bird", 600, 60, s=9, speed=-14),
]

L279_DIFFS = [
    ("pagoda", 130, 140, 0),
    ("maple", 120, 230, 0),
    ("bridge", 300, 420, 0),
    ("hiker", 420, 350, 0),
    ("deer", 150, 530, 0),
    ("lantern", 830, 520, 0),
]


# =================================================================== Level 280 firefly night
def l280_bg(c, d):
    c.gradient(0, H, (16, 24, 60), (60, 70, 110))
    stars_bg(c, 2801, 100, 260)
    moon = (250, 240, 200) if "moon" not in d else (250, 190, 150)
    npiece(c, Circ(720, 90, 36), moon, shadow=None)
    soft_union(c, [Circ(720, 90, 36)], (255, 250, 220), 0.25, spread=30)
    far_forest(c, 260, 80, (30, 50, 60), 2802)
    # meadow + pond with moon reflection
    c.rect(0, 300, W, H, (40, 70, 60))
    npiece(c, hill_strip(300, [(10, 0.01, 0.6), (5, 0.04, 1.0)]), (40, 70, 60), shadow=LAYER)
    flat(c, Ell(700, 360, 180, 40), (40, 60, 100))
    flat(c, Ell(720, 360, 30, 8), lit(moon, 0.8))
    # tent with lit inside (left)
    tent = (220, 140, 60) if "tent" not in d else (90, 150, 200)
    npiece(c, Poly([(80, 420), (300, 420), (190, 300)]), tent)
    flat(c, Poly([(170, 420), (210, 420), (190, 340)]), (250, 220, 140))
    # campfire (centre) - flames are elements
    for a in (-30, 30, 0):
        npiece(c, Thick(420 + 30 * math.sin(math.radians(a)), 470, 480 - 30 * math.sin(math.radians(a)), 450, 6), (110, 70, 50), shadow=None)
    for k in range(8):
        a = k * math.pi / 4
        npiece(c, Circ(450 + 46 * math.cos(a), 470 + 14 * math.sin(a), 9), (110, 110, 120), shadow=None)
    # camper on a log (centre left) + guitar
    npiece(c, RRect(260, 500, 380, 524, 10), (110, 70, 50))
    hx, hy = modern(c, 320, 506, (200, 60, 70) if "camper" not in d else (240, 240, 230), bottom=(50, 50, 70), hair=(60, 40, 30), h=1.9)
    # lantern on a stump (right front)
    npiece(c, RRect(760, 540, 830, 590, 6), (110, 70, 50))
    lan = (250, 200, 90) if "lantern" not in d else (140, 220, 240)
    npiece(c, [RRect(778, 494, 812, 540, 4), Ell(795, 492, 18, 6)], (40, 40, 50))
    flat(c, RRect(784, 500, 806, 534, 2), lan)
    # frogs on lily pads (pond)
    for x in (620, 780):
        flat(c, Ell(x, 370, 26, 7), (60, 120, 70))
    frog = (100, 180, 80) if "frog" not in d else (200, 90, 160)
    npiece(c, [Ell(620, 362, 14, 9), Circ(612, 354, 5), Circ(628, 354, 5)], frog, shadow=None)
    # jar for fireflies (left front)
    jar = (200, 230, 240) if "jar" not in d else (240, 180, 90)
    npiece(c, [RRect(80, 520, 130, 590, 8), RRect(84, 510, 126, 522, 3)], jar, shadow=SMALL)
    flat(c, [Circ(96, 560, 4), Circ(114, 548, 4), Circ(104, 574, 4)], (250, 250, 160))
    # reeds
    for x in (540, 560, 870, 890):
        flat(c, Thick(x, 400, x + 4, 330, 2), (60, 90, 60))
        flat(c, Ell(x + 4, 330, 4, 12), (110, 80, 60))


def fireflies(eid, pts, phase):
    def d(c, m):
        for x, y in pts:
            soft_union(c, [Circ(x, y, 3)], (230, 255, 140), 0.7, spread=8)
            flat(c, Circ(x, y, 2), (250, 255, 200))
    return E(eid, d, daynight="untinted", pivot=pts[0], anim=dict(twinkle=1.0, twinkleSpeed=0.9, bobAmplitude=(6, 10), bobSpeed=0.3, phase=phase))


L280_ELEMENTS = [
    fireflies("ff1", [(180, 240), (300, 200), (560, 240), (860, 220)], 0.0),
    fireflies("ff2", [(250, 290), (420, 250), (600, 300), (520, 180)], 0.33),
    fireflies("ff3", [(60, 300), (380, 320), (660, 230), (840, 300)], 0.66),
    E("flame", lambda c, m: [flat(c, Poly([(430, 466), (470, 466), (450, 410)]), (250, 140, 40)), flat(c, Poly([(440, 466), (460, 466), (450, 430)]), (255, 230, 120))],
      pivot=(450, 466), daynight="untinted", anim=dict(stretch=(0.15, 0.35), scaleSpeed=4)),
    E("fglow", lambda c, m: soft_union(c, [Circ(450, 450, 30)], (255, 160, 60), 0.3, spread=40), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.4)),
    E("spark", lambda c, m: flat(c, Circ(450, 410, 2), (255, 200, 90)), pivot=(450, 410), daynight="untinted",
      anim=dict(driftVelocity=(4, -30), driftLength=80, driftFade=True)),
]

L280_DIFFS = [
    ("moon", 720, 90, 0),
    ("tent", 190, 380, 0),
    ("camper", 320, 450, 0),
    ("frog", 620, 358, 0),
    ("lantern", 795, 515, 0),
    ("jar", 105, 552, 0),
]


# =================================================================== Level 281 mangrove
def mangrove(c, x, base, s, col=(80, 130, 80), root=(110, 90, 70)):
    for k in range(-3, 4):
        flat(c, Thick(x + k * 4 * s, base - 70 * s, x + k * 16 * s, base, 3 * s), root)
    piece(c, Thick(x, base - 70 * s, x, base - 130 * s, 7 * s), root, shadow=SMALL)
    piece(c, [Ell(x, base - 150 * s, 60 * s, 30 * s), Ell(x - 40 * s, base - 130 * s, 36 * s, 20 * s), Ell(x + 40 * s, base - 132 * s, 36 * s, 20 * s)], col, shadow=PROP)


def l281_bg(c, d):
    sky(c, (150, 200, 220), (230, 236, 220), H)
    far_round_trees(c, 170, 30, (110, 150, 110), 2811)
    c.rect(0, 200, W, H, (90, 130, 120))
    for k in range(10):
        flat(c, Thick(20 + k * 90, 230 + (k % 4) * 60, 70 + k * 90, 230 + (k % 4) * 60, 1.6), (130, 170, 160))
    mangrove(c, 120, 330, 1.3)
    mangrove(c, 400, 280, 0.9, col=(90, 140, 86))
    mangrove(c, 780, 320, 1.4)
    # boardwalk (right middle)
    piece(c, RRect(560, 360, 910, 380, 2), (170, 130, 90), border=1.2, shadow=PROP)
    for x in range(570, 910, 40):
        piece(c, RRect(x, 380, x + 8, 430, 1), (130, 96, 64), shadow=SMALL)
    flat(c, Thick(560, 340, 910, 340, 3), (150, 110, 70))
    for x in range(570, 910, 60):
        flat(c, Thick(x, 340, x, 362, 3), (150, 110, 70))
    # visitor with binoculars on the boardwalk
    modern(c, 700, 362, (240, 200, 60) if "visitor" not in d else (90, 150, 210), bottom=(60, 70, 90), hair=(90, 60, 40), h=1.7)
    # heron (left middle)
    heron = (150, 170, 190) if "heron" not in d else (250, 250, 246)
    piece(c, [Ell(270, 360, 22, 12), Thick(288, 352, 300, 316, 3), Ell(304, 312, 9, 6)], heron, border=1, shadow=SMALL)
    flat(c, [Thick(312, 312, 330, 316, 2), Thick(264, 372, 262, 410, 1.6), Thick(274, 372, 276, 410, 1.6)], (220, 180, 60))
    # kayak with paddler (centre)
    kay = (240, 120, 40) if "kayak" not in d else (60, 160, 120)
    piece(c, Poly([(360, 470), (540, 466), (520, 486), (380, 488)]), kay, border=1.2, shadow=SMALL)
    modern(c, 450, 476, (90, 120, 160), bottom=(60, 60, 70), hair=(30, 30, 34), h=1.4)
    # mud bank with crabs (left front)
    piece(c, hill_strip(530, [(10, 0.02, 0.6), (5, 0.06, 1.0)], x0=-60, x1=380), (140, 110, 80), shadow=LAYER)
    crab = (220, 70, 50) if "crab" not in d else (90, 120, 200)
    for x in (90, 200):
        piece(c, [Ell(x, 566, 18, 10), Circ(x - 16, 554, 6), Circ(x + 16, 554, 6)], crab if x == 90 else (220, 70, 50), border=1, shadow=SMALL)
        flat(c, [Thick(x - 12, 572, x - 22, 580, 2), Thick(x + 12, 572, x + 22, 580, 2)], crab if x == 90 else (220, 70, 50))
    # sign on post (right front)
    sign = (90, 130, 90) if "sign" not in d else (190, 120, 70)
    flat(c, Thick(800, 600, 800, 500, 4), (110, 80, 60))
    piece(c, RRect(740, 490, 860, 540, 3), sign, border=1.2, shadow=SMALL)
    flat(c, [Thick(760, 506, 840, 506, 2), Thick(760, 522, 820, 522, 2)], (240, 240, 230))
    # mudskipper on the bank
    if "fish" not in d:
        fish(c, 300, 560, 1.4, (120, 110, 90), right=False)


L281_ELEMENTS = [
    bird_el("bird", 500, 60, s=10, speed=14),
    E("ripple", lambda c, m: c.ellipse_ring(560, 500, 26, 5, 1.6, (150, 190, 180)), pivot=(560, 500), anim=dict(stretch=(0.5, 0.5), scaleSpeed=1.0)),
    E("paddle", lambda c, m: flat(c, Thick(420, 480, 480, 440, 3), (60, 60, 70)), pivot=(450, 460), anim=dict(swingAngle=24, swingSpeed=1.2)),
    E("fly", lambda c, m: flat(c, [Ell(600, 250, 4, 2), Ell(606, 250, 4, 2)], (60, 60, 70)), pivot=(603, 250), anim=dict(orbitRadius=(30, 14), orbitSpeed=0.4)),
]

L281_DIFFS = [
    ("heron", 290, 350, 0),
    ("visitor", 702, 310, 0),
    ("kayak", 450, 476, 0),
    ("crab", 90, 562, 0),
    ("fish", 296, 560, 0),
    ("sign", 800, 515, 0),
]


# =================================================================== Level 282 lavender fields
def l282_bg(c, d):
    sky(c, (130, 180, 236), (250, 230, 210), H)
    sun_bg(c, 150, 70, 30, col=(250, 210, 110))
    cloud_bg(c, 620, 60, 0.6)
    far_ridge(c, 190, 40, (170, 180, 200), 2821)
    # stone farmhouse (right back)
    piece(c, RRect(620, 150, 800, 230, 2), (230, 210, 170), border=1.5, shadow=PROP)
    roof = (200, 110, 80) if "roof" not in d else (90, 110, 150)
    piece(c, Poly([(606, 154), (814, 154), (780, 120), (640, 120)]), roof, border=1.5, shadow=PROP)
    shut = (90, 140, 170) if "shutter" not in d else (200, 80, 70)
    for x in (650, 740):
        flat(c, RRect(x, 176, x + 30, 206, 2), (90, 80, 80))
        flat(c, [RRect(x - 12, 176, x, 206, 1), RRect(x + 30, 176, x + 42, 206, 1)], shut)
    # cypress (left back)
    for x in (300, 330):
        piece(c, [Ell(x, 160, 12, 50), RRect(x - 3, 200, x + 3, 228, 1)], (60, 100, 70), shadow=PROP)
    # lavender rows converging
    c.rect(0, 226, W, H, (130, 150, 90))
    for k in range(-8, 9):
        x0 = 450 + k * 26
        x1 = 450 + k * 160
        col = (150, 110, 200) if k % 2 else (130, 96, 180)
        flat(c, Poly([(x0 - 8, 230), (x0 + 8, 230), (x1 + 60, H), (x1 - 60, H)]), col)
        if k == 3 and "row" in d:
            def edge(y, side):
                t = (y - 230) / (H - 230)
                return x0 + (x1 - x0) * t + side * (8 + 52 * t)
            flat(c, Poly([(edge(330, -1), 330), (edge(330, 1), 330), (edge(470, 1), 470), (edge(470, -1), 470)]), (250, 230, 120))
    # sunflowers patch (left)
    for k, (x, y) in enumerate(((60, 380), (110, 360), (40, 440), (150, 420))):
        flat(c, Thick(x, y, x, y + 80, 3), (90, 140, 60))
        col = (250, 200, 40) if not (k == 1 and "sunflower" in d) else (240, 120, 50)
        piece(c, Circ(x, y, 20), col, shadow=SMALL)
        flat(c, Circ(x, y, 8), (120, 80, 40))
    # painter at an easel (centre)
    piece(c, [Thick(490, 470, 520, 380, 3), Thick(550, 470, 520, 380, 3)], (150, 110, 70), shadow=SMALL)
    canvas = (180, 150, 220) if "canvas" not in d else (120, 190, 230)
    piece(c, RRect(488, 360, 552, 420, 2), (250, 248, 240), border=1.2, shadow=SMALL)
    flat(c, RRect(494, 366, 546, 414, 1), canvas)
    hx, hy = modern(c, 440, 480, (250, 250, 246), bottom=(60, 70, 100), hair=(200, 160, 90), h=2.0, style="long")
    piece(c, [Ell(hx, hy - 8, 22, 5), Ell(hx, hy - 14, 12, 8)], (230, 200, 120), shadow=SMALL)
    # beehives (right front)
    for k, x in enumerate((720, 820)):
        col = (240, 240, 230) if not (k == 0 and "hive" in d) else (100, 160, 220)
        piece(c, [RRect(x - 36, 500, x + 36, 580, 2), RRect(x - 42, 490, x + 42, 504, 2)], col, border=1.5, shadow=PROP)
        flat(c, [Thick(x - 36, 526, x + 36, 526, 2), Thick(x - 36, 552, x + 36, 552, 2)], lit(col, 0.85))
    # basket of cut lavender (left front)
    bask = (190, 140, 80) if "basket" not in d else (220, 100, 100)
    piece(c, Poly([(220, 590), (330, 590), (340, 540), (210, 540)]), bask, border=1.5, shadow=PROP)
    for k in range(7):
        x = 226 + k * 16
        flat(c, Thick(x, 540, x - 6, 500, 2), (90, 130, 70))
        flat(c, Ell(x - 6, 502, 4, 10), (150, 110, 200))


L282_ELEMENTS = [
    E("bee1", lambda c, m: piece(c, Ell(620, 440, 6, 4), (250, 210, 60), shadow=None), pivot=(620, 440), anim=dict(orbitRadius=(50, 20), orbitSpeed=0.3)),
    E("bee2", lambda c, m: piece(c, Ell(380, 300, 6, 4), (250, 210, 60), shadow=None), pivot=(380, 300), anim=dict(orbitRadius=(40, 16), orbitSpeed=-0.25)),
    E("bfly", lambda c, m: piece(c, [Ell(250, 300, 7, 10), Ell(262, 300, 7, 10)], (250, 250, 246), shadow=None), pivot=(256, 300),
      anim=dict(orbitRadius=(40, 20), orbitSpeed=0.15, stretch=(0.6, 0), scaleSpeed=5)),
    bird_el("bird", 420, 60, s=9, speed=14),
]

L282_DIFFS = [
    ("roof", 710, 138, 0),
    ("shutter", 700, 190, 0),
    ("row", 620, 400, 0),
    ("sunflower", 110, 360, 0),
    ("canvas", 520, 390, 0),
    ("hive", 720, 535, 0),
    ("basket", 275, 545, 0),
]


# =================================================================== Level 283 treehouse village
def treehouse(c, x, y, w, h, wall, roof):
    piece(c, RRect(x - w / 2 - 10, y, x + w / 2 + 10, y + 12, 2), (150, 110, 70), border=1.2, shadow=PROP)
    piece(c, RRect(x - w / 2, y - h, x + w / 2, y, 2), wall, border=1.5, shadow=PROP)
    for yy in range(int(y - h) + 8, int(y), 10):
        flat(c, Thick(x - w / 2, yy, x + w / 2, yy, 1), lit(wall, 0.86))
    piece(c, Poly([(x - w / 2 - 12, y - h + 2), (x + w / 2 + 12, y - h + 2), (x, y - h - w * 0.5)]), roof, border=1.5, shadow=PROP)
    flat(c, RRect(x - 10, y - h * 0.7, x + 10, y - h * 0.3, 3), (250, 220, 140))


def l283_bg(c, d):
    sky(c, (170, 210, 220), (220, 236, 220), H)
    for k, x in enumerate(range(30, W, 75)):
        flat(c, RRect(x, 0, x + 22 + (k % 3) * 6, 520, 4), (120, 160, 130))
        flat(c, Circ(x + 12, 100 + (k % 4) * 40, 30), (110, 160, 110))
    # giant trunks
    for x, w in ((140, 70), (450, 60), (770, 80)):
        piece(c, Poly([(x - w / 2, 610), (x - w / 3, -10), (x + w / 3, -10), (x + w / 2, 610)]), (120, 86, 60), border=1.5, shadow=LAYER)
        for k in range(6):
            flat(c, Thick(x - w / 4 + k * 4, 40 + k * 90, x - w / 4 + k * 4, 100 + k * 90, 2), (100, 70, 50))
    # canopy
    for x in range(-40, W + 60, 90):
        piece(c, Circ(x, 20 + (x % 3) * 10, 70), (80, 140, 80), shadow=PROP)
    # treehouses
    treehouse(c, 140, 200, 110, 70, (200, 160, 110), (180, 70, 60) if "roof" not in d else (60, 110, 170))
    treehouse(c, 450, 300, 90, 60, (190, 150, 100), (80, 120, 80))
    treehouse(c, 770, 180, 120, 70, (210, 170, 120), (90, 90, 110))
    # rope bridges
    for (x0, y0), (x1, y1) in (((200, 206), (400, 306)), ((500, 306), (710, 186))):
        pts = [(x0 + (x1 - x0) * t / 10, y0 + (y1 - y0) * t / 10 + 18 * math.sin(math.pi * t / 10)) for t in range(11)]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            flat(c, Thick(ax, ay, bx, by, 4), (170, 130, 80))
            flat(c, Thick(ax, ay - 20, ax, ay, 1.4), (120, 90, 60))
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            flat(c, Thick(ax, ay - 20, bx, by - 20, 1.4), (120, 90, 60))
    # flag on the right treehouse
    flat(c, Thick(800, 120, 800, 80, 2), (90, 70, 60))
    flag = (240, 200, 60) if "flag" not in d else (220, 60, 70)
    piece(c, Poly([(800, 80), (840, 90), (800, 100)]), flag, border=1, shadow=None)
    # lanterns on a string (centre top)
    for k, x in enumerate(range(240, 420, 36)):
        col = (240, 120, 60) if not (k == 2 and "lantern" in d) else (120, 200, 230)
        flat(c, Thick(x, 120, x, 130, 1), (90, 70, 60))
        piece(c, Ell(x, 140, 9, 11), col, shadow=SMALL)
    flat(c, Thick(220, 118, 430, 118, 1.4), (90, 70, 60))
    # ladder (left trunk)
    for y in range(220, 600, 24):
        flat(c, Thick(176, y, 210, y, 3), (190, 150, 90))
    flat(c, [Thick(176, 212, 176, 600, 3), Thick(210, 212, 210, 600, 3)], (190, 150, 90))
    # ground
    c.rect(0, 520, W, H, (110, 150, 90))
    layer(c, 520, [(6, 0.02, 0.6), (3, 0.06, 1.0)], (120, 160, 96))
    # children
    modern(c, 450, 300, (240, 200, 60) if "kid" not in d else (200, 90, 200), bottom=(60, 70, 100), hair=(90, 60, 40), h=1.4)
    modern(c, 300, 590, (90, 160, 220), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.0, style="twin")
    # bucket on a pulley (right)
    flat(c, Thick(860, 190, 860, 420, 1.4), (90, 70, 60))
    bucket = (150, 160, 176) if "bucket" not in d else (220, 120, 60)
    piece(c, Poly([(842, 420), (878, 420), (872, 450), (848, 450)]), bucket, border=1.2, shadow=SMALL)
    # mushrooms + log (front)
    piece(c, RRect(560, 560, 720, 590, 14), (140, 100, 70), border=1.5, shadow=PROP)
    flat(c, Ell(720, 575, 10, 15), (200, 170, 120))
    shroom = (220, 60, 60) if "shroom" not in d else (250, 200, 60)
    for x in (600, 640):
        piece(c, [RRect(x - 4, 540, x + 4, 560, 2), Ell(x, 540, 16, 9)], shroom, border=1, shadow=SMALL)
        flat(c, RRect(x - 4, 542, x + 4, 560, 2), (250, 240, 220))


L283_ELEMENTS = [
    E("swing", lambda c, m: [flat(c, [Thick(560, 340, 560, 440, 1.4), Thick(600, 340, 600, 440, 1.4)], (90, 70, 60)),
                             piece(c, RRect(552, 440, 608, 448, 2), (190, 150, 90), shadow=SMALL)], pivot=(580, 340), anim=dict(swingAngle=14, swingSpeed=0.6)),
    E("leaf", lambda c, m: flat(c, Ell(300, 60, 6, 3), (100, 160, 90)), pivot=(300, 60),
      anim=dict(driftVelocity=(10, 40), driftLength=150, driftFade=True, swingAngle=40, swingSpeed=1.0)),
    E("squirrel", lambda c, m: piece(c, [Ell(470, 420, 10, 7), Circ(478, 414, 5), Ell(460, 410, 6, 10)], (180, 110, 60), shadow=None), pivot=(470, 420),
      anim=dict(bobAmplitude=(0, 30), bobSpeed=0.3)),
    E("glow", lambda c, m: soft_union(c, [Circ(x, 140, 8) for x in range(240, 420, 36)], (255, 200, 120), 0.3, spread=12), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=1.0)),
]

L283_DIFFS = [
    ("roof", 140, 110, 0),
    ("lantern", 312, 140, 0),
    ("flag", 815, 90, 0),
    ("kid", 452, 262, 0),
    ("bucket", 860, 435, 0),
    ("shroom", 620, 545, 0),
]


# =================================================================== Level 284 fjord
def l284_bg(c, d):
    sky(c, (120, 170, 220), (220, 230, 240), H)
    cloud_bg(c, 450, 50, 0.7)
    # cliffs
    piece(c, Poly([(-20, 420), (-20, 40), (80, 60), (160, 30), (260, 120), (330, 250), (360, 420)]), (100, 110, 120), border=1.5, shadow=LAYER)
    piece(c, Poly([(920, 420), (920, 60), (820, 30), (720, 90), (620, 220), (560, 420)]), (110, 116, 126), border=1.5, shadow=LAYER)
    flat(c, Poly([(80, 60), (160, 30), (200, 70), (150, 66), (110, 80)]), (250, 250, 252))
    flat(c, Poly([(820, 30), (720, 90), (760, 86), (800, 70), (860, 64)]), (250, 250, 252))
    for x0, x1 in ((40, 120), (700, 860)):
        for k in range(5):
            flat(c, Thick(x0 + k * 16, 100 + k * 50, x0 + k * 16 + 60, 140 + k * 50, 2), (90, 100, 110))
    far_forest(c, 420, 40, (60, 100, 80), 2841, x0=300, x1=620)
    # waterfalls
    wf = (230, 240, 250) if "fall" not in d else (110, 116, 126)
    flat(c, Poly([(230, 110), (250, 110), (300, 420), (270, 420)]), (230, 240, 250))
    flat(c, Poly([(680, 150), (700, 150), (660, 420), (636, 420)]), wf)
    # water
    c.rect(0, 410, W, H, (60, 110, 150))
    for k in range(10):
        flat(c, Thick(30 + k * 90, 440 + (k % 4) * 40, 80 + k * 90, 440 + (k % 4) * 40, 1.6), (110, 160, 200))
    # red cabins on the shore (left)
    piece(c, hill_strip(400, [(6, 0.03, 0.4)], x0=-60, x1=300, bottom=430), (90, 130, 80), shadow=LAYER)
    for k, x in enumerate((60, 150)):
        col = (180, 50, 40) if not (k == 1 and "cabin" in d) else (240, 200, 60)
        piece(c, RRect(x - 34, 360, x + 34, 410, 2), col, border=1.5, shadow=PROP)
        piece(c, Poly([(x - 42, 362), (x + 42, 362), (x, 330)]), (60, 60, 60), border=1.5, shadow=PROP)
        flat(c, [RRect(x - 22, 374, x - 8, 388, 1), RRect(x + 8, 374, x + 22, 388, 1)], (250, 250, 246))
    # cruise ship (centre)
    piece(c, Poly([(330, 470), (620, 470), (600, 500), (350, 500)]), (40, 50, 70), border=1.5, shadow=PROP)
    piece(c, [RRect(370, 430, 580, 472, 2), RRect(400, 400, 550, 432, 2)], (250, 250, 246), border=1.5, shadow=PROP)
    for x in range(380, 570, 18):
        flat(c, RRect(x, 444, x + 10, 452, 1), (90, 130, 170))
    funnel = (220, 60, 50) if "funnel" not in d else (60, 140, 120)
    piece(c, RRect(490, 370, 520, 402, 2), funnel, border=1.2, shadow=SMALL)
    # fishing boat (right front)
    boat = (60, 100, 170) if "boat" not in d else (220, 90, 70)
    piece(c, Poly([(660, 560), (850, 552), (830, 586), (680, 590)]), boat, border=1.5, shadow=PROP)
    piece(c, RRect(760, 510, 810, 556, 2), (250, 250, 246), border=1.2, shadow=SMALL)
    flat(c, Thick(720, 556, 720, 470, 3), (120, 90, 60))
    # kayaker (left front)
    kay = (250, 200, 60) if "kayak" not in d else (90, 200, 120)
    piece(c, Poly([(60, 556), (220, 552), (200, 568), (80, 570)]), kay, border=1.2, shadow=SMALL)
    modern(c, 140, 558, (200, 70, 70), bottom=(50, 50, 60), hair=(200, 160, 90), h=1.4)
    # puffin on a rock (centre front)
    rock(c, 450, 600, 1.8, col=(100, 100, 110))
    if "puffin" not in d:
        piece(c, [Ell(450, 560, 12, 16), Circ(452, 540, 9)], (40, 40, 46), border=1, shadow=SMALL)
        flat(c, [Ell(452, 566, 8, 10), Circ(454, 540, 5)], (250, 250, 246))
        flat(c, Poly([(460, 538), (472, 542), (460, 546)]), (240, 120, 40))


L284_ELEMENTS = [
    bird_el("gull", 300, 120, s=10, speed=14),
    bird_el("gull2", 600, 80, s=9, speed=-16),
    E("smoke", lambda c, m: piece(c, Circ(505, 362, 9), (220, 220, 226), shadow=None), pivot=(505, 362),
      anim=dict(driftVelocity=(16, -18), driftLength=70, driftFade=True, driftGrow=1.8)),
    E("fallmist", lambda c, m: soft_union(c, [Ell(280, 418, 30, 8)], (250, 252, 255), 0.5, spread=10), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.0)),
    E("paddle", lambda c, m: flat(c, Thick(110, 560, 170, 530, 3), (60, 60, 70)), pivot=(140, 545), anim=dict(swingAngle=24, swingSpeed=1.2)),
]

L284_DIFFS = [
    ("fall", 668, 290, 0),
    ("cabin", 150, 380, 0),
    ("funnel", 505, 386, 0),
    ("boat", 755, 560, 0),
    ("kayak", 140, 560, 0),
    ("puffin", 452, 552, 0),
]


LEVELS = [
    ("Level275", "郁金香风车", l275_bg, L275_ELEMENTS, L275_DIFFS, 60, OPTS),
    ("Level276", "高山牧场", l276_bg, L276_ELEMENTS, L276_DIFFS, 60, OPTS),
    ("Level277", "梯田", l277_bg, L277_ELEMENTS, L277_DIFFS, 60, OPTS),
    ("Level278", "红岩峡谷", l278_bg, L278_ELEMENTS, L278_DIFFS, 60, OPTS),
    ("Level279", "枫叶溪谷", l279_bg, L279_ELEMENTS, L279_DIFFS, 60, OPTS),
    ("Level280", "萤火虫之夜", l280_bg, L280_ELEMENTS, L280_DIFFS, 60, OPTS),
    ("Level281", "红树林", l281_bg, L281_ELEMENTS, L281_DIFFS, 60, OPTS),
    ("Level282", "薰衣草花田", l282_bg, L282_ELEMENTS, L282_DIFFS, 60, OPTS),
    ("Level283", "树屋村", l283_bg, L283_ELEMENTS, L283_DIFFS, 60, OPTS),
    ("Level284", "峡湾", l284_bg, L284_ELEMENTS, L284_DIFFS, 60, OPTS),
]
