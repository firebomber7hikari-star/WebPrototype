# -*- coding: utf-8 -*-
"""Journey to the West, paper-craft side views, full-bleed:
  Level109 花果山   - the Water Curtain Cave on Flower-Fruit Mountain: waterfall, peach trees, the monkey troop
  Level110 大闹天宫 - the Southern Heavenly Gate above the clouds, the immortal peach garden, Wukong on his cloud
  Level111 三打白骨精 - the pilgrims on a mountain road meet a 'village girl' (the White Bone Demon in disguise)
  Level112 火焰山   - the Flaming Mountain and Princess Iron Fan with her palm-leaf fan
  Level113 通天河   - the great white turtle carries the pilgrims across the River that Reaches Heaven
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_bg, drift_across, fish, gy, layer, sky, smoke_el
from levels_heian import blossom_tree, pine_jp
from cn_kit import GLAZE, GOLDEN, GREY_TILE, RED, SKIN, arch, cn_hall, cn_roof, ellipse_top, hanfu, horse_cn, lantern_cn, warrior

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
FUR = (150, 100, 60)
TIGER = (230, 150, 50)


# ------------------------------------------------------------------- the pilgrims
def wukong(c, x, base, h=1.0, cloak=(200, 50, 40), staff=True, plumes=False, staff_up=False):
    piece(c, [Poly([(x - 10 * h, base - 12 * h), (x + 10 * h, base - 12 * h), (x + 8 * h, base - 32 * h), (x - 8 * h, base - 32 * h)]),
              RRect(x - 7 * h, base - 12 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 12 * h, x + 7 * h, base, 1)], cloak, border=1.5, shadow=PROP)
    flat(c, Poly([(x - 10 * h, base - 12 * h), (x + 10 * h, base - 12 * h), (x + 8 * h, base - 20 * h), (x - 8 * h, base - 20 * h)]), TIGER)
    for k in range(3):
        flat(c, Thick(x - 6 * h + k * 6 * h, base - 13 * h, x - 4 * h + k * 6 * h, base - 19 * h, 1.4), (40, 30, 30))
    hx, hy = x + 1 * h, base - 40 * h
    flat(c, Circ(hx, hy, 8 * h), FUR)
    flat(c, Ell(hx + 2 * h, hy + 2 * h, 5.5 * h, 5 * h), (240, 200, 160))
    flat(c, [Circ(hx + 4 * h, hy - 1 * h, 1.2 * h), Circ(hx - 1 * h, hy - 1 * h, 1.2 * h)], INK)
    flat(c, Thick(hx - 8 * h, hy - 5 * h, hx + 8 * h, hy - 5 * h, 2 * h), GOLDEN)
    if plumes:
        flat(c, [Thick(hx - 3 * h, hy - 6 * h, hx - 14 * h, hy - 34 * h, 1.8 * h), Thick(hx + 3 * h, hy - 6 * h, hx + 14 * h, hy - 34 * h, 1.8 * h)],
             (200, 60, 50))
    if staff:
        if staff_up:
            flat(c, Thick(x + 12 * h, base - 20 * h, x + 22 * h, base - 110 * h, 3 * h), (200, 50, 40))
            flat(c, [Thick(x + 12 * h, base - 20 * h, x + 13 * h, base - 28 * h, 3.4 * h), Thick(x + 21 * h, base - 102 * h, x + 22 * h, base - 110 * h, 3.4 * h)],
                 GOLDEN)
        else:
            flat(c, Thick(x - 30 * h, base - 24 * h, x + 34 * h, base - 30 * h, 3 * h), (200, 50, 40))
            flat(c, [Thick(x - 30 * h, base - 24 * h, x - 24 * h, base - 24.5 * h, 3.4 * h), Thick(x + 28 * h, base - 29.5 * h, x + 34 * h, base - 30 * h, 3.4 * h)],
                 GOLDEN)
    return hx, hy


def tangseng(c, x, base, h=1.0, kasaya=(200, 60, 50), hat=GOLDEN):
    hx, hy = hanfu(c, x, base, (246, 240, 226), h=h, hat="none", sash=kasaya)
    flat(c, Poly([(x - 10 * h, base - 30 * h), (x + 8 * h, base - 30 * h), (x + 12 * h, base - 4 * h), (x - 2 * h, base - 2 * h)]), kasaya)
    flat(c, [Poly([(hx - 9 * h, hy - 4 * h), (hx + 9 * h, hy - 4 * h), (hx + 7 * h, hy - 12 * h), (hx + 3 * h, hy - 9 * h), (hx, hy - 14 * h),
                   (hx - 3 * h, hy - 9 * h), (hx - 7 * h, hy - 12 * h)])], hat)
    return hx, hy


def bajie(c, x, base, h=1.0, robe=(40, 40, 46), rake=(200, 200, 210)):
    piece(c, [Ell(x, base - 18 * h, 15 * h, 18 * h), RRect(x - 8 * h, base - 6 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 6 * h, x + 8 * h, base, 1)],
          robe, border=1.5, shadow=PROP)
    flat(c, Ell(x + 2 * h, base - 16 * h, 9 * h, 10 * h), (250, 200, 200))
    hx, hy = x + 1 * h, base - 42 * h
    piece(c, [Circ(hx, hy, 10 * h), Ell(hx - 9 * h, hy - 4 * h, 6 * h, 9 * h)], (250, 190, 190), shadow=None)
    flat(c, Ell(hx + 8 * h, hy + 2 * h, 5 * h, 4 * h), (240, 160, 170))
    flat(c, [Circ(hx + 7 * h, hy + 2 * h, 1 * h), Circ(hx + 10 * h, hy + 2 * h, 1 * h), Circ(hx + 3 * h, hy - 4 * h, 1.2 * h)], INK)
    flat(c, Thick(x + 14 * h, base, x + 20 * h, base - 70 * h, 2.2 * h), (130, 96, 60))
    flat(c, [RRect(x + 12 * h, base - 76 * h, x + 30 * h, base - 70 * h, 1)] + [Thick(x + 13 * h + k * 4 * h, base - 70 * h, x + 13 * h + k * 4 * h,
                                                                                        base - 62 * h, 1.4 * h) for k in range(5)], rake)


def shaseng(c, x, base, h=1.0, robe=(90, 120, 160), luggage=(200, 140, 60)):
    hx, hy = hanfu(c, x, base, robe, h=h, hat="none", beard=(150, 60, 40))
    flat(c, Circ(hx, hy - 1 * h, 7.4 * h), (120, 140, 150))
    flat(c, Circ(hx + 3 * h, hy - 2 * h, 1.2 * h), INK)
    for k in range(7):
        a = math.pi * 0.15 + k * math.pi * 0.1
        flat(c, Circ(x + 9 * h * math.cos(a), base - 28 * h + 6 * h * math.sin(a), 2 * h), (110, 80, 60))
    flat(c, Thick(x - 34 * h, base - 34 * h, x + 34 * h, base - 34 * h, 2.4 * h), (130, 96, 60))
    for px in (x - 30 * h, x + 30 * h):
        piece(c, RRect(px - 10 * h, base - 34 * h, px + 10 * h, base - 14 * h, 3), luggage, border=1, shadow=SMALL)


def white_horse(c, x, base, saddle=(200, 50, 40)):
    horse_cn(c, x, base, (246, 244, 238), saddle=saddle)


def stylised_cloud(c, x, y, k, col=(250, 250, 252)):
    piece(c, [Circ(x - 26 * k, y, 16 * k), Circ(x, y - 8 * k, 20 * k), Circ(x + 26 * k, y, 16 * k), RRect(x - 40 * k, y, x + 40 * k, y + 12 * k, 6 * k)], col,
          shadow=SMALL)
    for dx in (-26, 0, 26):
        c.ellipse_ring(x + dx * k, y - (8 if dx == 0 else 0) * k, 8 * k, 8 * k, 1.6, lit(col, 0.85))


# =================================================================== Level 109 Flower-Fruit Mountain
def l109_bg(c, d):
    sky(c, (170, 214, 236), (246, 240, 214), 360)
    layer(c, 220, [(26, 0.007, 0.4), (10, 0.02, 1.2)], (140, 176, 150))
    piece(c, Poly([(200, 600), (220, 260), (300, 160), (420, 120), (520, 130), (620, 190), (700, 280), (720, 600)]), (130, 120, 110), shadow=LAYER)
    flat(c, RRect(400, 170, 520, 470, 0), (40, 34, 40))
    if "rainbow" not in d:
        for k, col in enumerate(((240, 100, 100), (250, 200, 90), (120, 200, 120), (120, 160, 230))):
            c.ellipse_ring(460, 380, 150 - k * 7, 120 - k * 7, 5, col + (0.55,), ymax=380)
    for x, s in ((120, 1.0), (790, 1.1), (300, 0.7), (640, 0.7)):
        blossom_tree(c, x, 300 if s < 1 else 420, s, (246, 196, 210), 1090 + x)
    for i, (x, y) in enumerate(((780, 330), (810, 344), (760, 350), (120, 320), (140, 334))):
        col = (230, 120, 60) if (i == 1 and "peach" in d) else (250, 160, 170)
        piece(c, Circ(x, y, 7), col, shadow=None)
    # pool and rocks
    piece(c, Ell(460, 500, 200, 40), (110, 170, 200), shadow=SMALL)
    piece(c, hill_strip(510, [(8, 0.012, 0.4), (3, 0.04, 1.0)]), (120, 160, 100), shadow=LAYER)
    for x, s in ((90, 1.2), (220, 0.9), (720, 1.1), (850, 1.3)):
        piece(c, Ell(x, 520, 40 * s, 22 * s), (150, 146, 140), border=1.2, shadow=PROP)
    # Wukong on his stone throne, monkeys around
    piece(c, [RRect(560, 470, 640, 520, 6), RRect(570, 430, 630, 476, 6)], (160, 150, 140), border=1.5, shadow=PROP)
    wukong(c, 600, 470, h=1.2, plumes="plume" not in d, staff=False)
    flat(c, Thick(546, 520, 546, 420, 2.5), (110, 80, 60))
    piece(c, Poly([(547, 420), (590, 426), (586, 444), (590, 462), (547, 466)]), (60, 130, 200) if "flag" in d else (230, 190, 60), border=1.2,
          shadow=SMALL)
    rnd = random.Random(109)
    for i, (x, b) in enumerate(((120, 560), (190, 590), (300, 576), (380, 598), (690, 590), (760, 566), (840, 596))):
        col = (90, 90, 96) if (i == 4 and "monkey" in d) else FUR
        piece(c, [Ell(x, b - 12, 11, 12), Circ(x + 3, b - 28, 8)], col, border=1, shadow=SMALL)
        flat(c, Ell(x + 5, b - 26, 5, 4.5), (240, 200, 160))
        flat(c, Circ(x + 6, b - 28, 1.2), INK)
        flat(c, Thick(x - 10, b - 8, x - 20, b - 20, 2), col)
    if "banana" not in d:
        for k in range(3):
            flat(c, Thick(388 + k * 4, 570, 400 + k * 4, 556, 3), (250, 220, 60))
    if "stool" not in d:
        piece(c, [Ell(480, 580, 22, 8), RRect(466, 580, 494, 598, 3)], (160, 150, 140), border=1.2, shadow=PROP)


def waterfall_el(i):
    def d(c, m):
        for k in range(6):
            x = 412 + k * 18 + (i * 7) % 12
            flat(c, Thick(x, 170, x, 260, 3), (220, 236, 250, 0.85))
    return E("fall%d" % i, d, anim=dict(driftVelocity=(0, -120), driftLength=300, driftStart=-40, driftFade=True, phase=i / 4))


L109_ELEMENTS = [waterfall_el(i) for i in range(4)] + [
    E("mist", lambda c, m: soft_union(c, [Ell(460, 480, 90, 16)], (250, 250, 252), 0.5, spread=16), anim=dict(twinkle=0.3, twinkleSpeed=0.4)),
    bird_el("bird0", 700, 120, 8, speed=14), bird_el("bird1", 724, 108, 6, speed=14),
    E("monkey_swing", lambda c, m: (flat(c, Thick(300, 240, 300, 296, 1.6), (90, 140, 70)),
                                    piece(c, [Ell(300, 304, 9, 10), Circ(302, 290, 7)], FUR, shadow=SMALL)), pivot=(300, 240),
      anim=dict(swingAngle=20, swingSpeed=0.35)),
]

L109_DIFFS = [
    ("rainbow", 460, 262, 0),
    ("peach", 810, 344, 0),
    ("plume", 601, 386, 0),
    ("flag", 570, 444, 0),
    ("monkey", 690, 574, 0),
    ("banana", 400, 562, 0),
    ("stool", 480, 586, 0),
]


# =================================================================== Level 110 havoc in heaven
def l110_bg(c, d):
    sky(c, (200, 180, 230), (250, 226, 200), 600)
    for x, y, k in ((100, 120, 1.4), (420, 80, 1.6), (760, 130, 1.4), (240, 260, 1.2), (620, 260, 1.3)):
        stylised_cloud(c, x, y, k, (246, 240, 250))
    # Lingxiao palace far behind, the Southern Heavenly Gate on the left
    cn_hall(c, 400, 640, 300, 220, 40, roof=GLAZE, bays=6)
    for x in (160, 300):
        piece(c, RRect(x - 16, 260, x + 16, 470, 2), RED, border=1.5, shadow=PROP)
        for k in range(6):
            flat(c, Ell(x, 280 + k * 32, 14, 6), (60, 160, 120) if ("pillar" in d and x == 300) else (230, 190, 60))
    piece(c, RRect(130, 230, 330, 262, 2), RED, border=1.5, shadow=PROP)
    cn_roof(c, 120, 340, 230, 34, (60, 140, 120) if "gate" in d else GLAZE)
    piece(c, RRect(206, 238, 254, 256, 1), (40, 60, 130), border=1, border_col=GOLDEN, shadow=SMALL)
    # cloud floor
    for x in range(-40, 960, 80):
        stylised_cloud(c, x, 470 + (x % 3) * 8, 1.4, (250, 250, 252))
    piece(c, RRect(-10, 490, 910, 612, 0), (244, 242, 250), shadow=LAYER)
    # heavenly soldiers, a crane, the peach tree
    for x in (120, 200, 280):
        warrior(c, x, 540, (230, 190, 60), h=1.0, helmet=(230, 190, 60), plume=(200, 40, 40), weapon="spear")
    flat(c, Thick(340, 540, 340, 420, 2.5), (110, 80, 60))
    piece(c, Poly([(341, 420), (380, 426), (376, 446), (380, 464), (341, 470)]), (60, 130, 200) if "banner" in d else (200, 40, 40), border=1.2,
          shadow=SMALL)
    piece(c, [Thick(760, 540, 754, 420, 12), Thick(754, 440, 700, 400, 6), Thick(754, 430, 820, 390, 6)], (110, 80, 60), shadow=SMALL)
    piece(c, [Circ(x, y, 34) for x, y in ((700, 380), (760, 360), (820, 380), (740, 400))], (110, 170, 100), border=1.2, shadow=PROP)
    peaches = [(690, 392), (730, 368), (770, 390), (812, 374), (750, 412)]
    for i, (x, y) in enumerate(peaches):
        if i == 3 and "peach" in d:
            continue
        piece(c, [Circ(x, y, 10)], (250, 170, 170), border=1, shadow=SMALL)
        flat(c, Ell(x - 3, y - 3, 4, 3), (255, 220, 220))
    if "crane" not in d:
        piece(c, [Ell(560, 560, 22, 10), Thick(576, 554, 590, 524, 3), Ell(592, 522, 6, 4)], (250, 250, 252), border=1.2, shadow=SMALL)
        flat(c, [Circ(592, 518, 3), Thick(596, 522, 606, 524, 1.6), Thick(552, 568, 548, 590, 1.6), Thick(560, 568, 558, 590, 1.6)],
             (220, 40, 40))
    lantern_cn(c, 460, 360, (60, 160, 90) if "lantern" in d else (220, 50, 40), r=10)


def l110_wukong(c, m):
    stylised_cloud(c, 460, 470, 1.1, (250, 230, 120) if m else (250, 250, 252))
    wukong(c, 456, 462, h=1.3, plumes=True, staff_up=True)


L110_ELEMENTS = [
    E("wukong", l110_wukong, pivot=(460, 470), variant=True, anim=dict(bobAmplitude=(6, 10), bobSpeed=0.25, swingAngle=4, swingSpeed=0.2)),
    E("cloud_drift", lambda c, m: stylised_cloud(c, 200, 180, 0.8, (250, 246, 252)), anim=drift_across(140, 260, 8)),
]

L110_DIFFS = [
    ("gate", 230, 200, 0),
    ("pillar", 300, 360, 0),
    ("banner", 360, 444, 0),
    ("peach", 812, 374, 0),
    ("crane", 576, 548, 0),
    ("lantern", 460, 360, 0),
    ("cloud", 460, 476, 0),
]


# =================================================================== Level 111 the White Bone Demon
def l111_bg(c, d):
    sky(c, (190, 200, 220), (240, 226, 210), 360)
    layer(c, 220, [(30, 0.006, 0.4), (14, 0.02, 1.1)], (140, 150, 170))
    layer(c, 276, [(20, 0.01, 1.0)], (120, 140, 120))
    for x, col in ((90, (200, 90, 50) if "tree2" not in d else (120, 160, 90)), (260, (220, 160, 60)), (700, (190, 70, 50) if "tree" not in d else (90, 140, 80)), (840, (230, 140, 60))):
        blossom_tree(c, x, 380, 1.0, col, 1110 + x, trunk=(90, 70, 60))
    piece(c, hill_strip(380, [(6, 0.01, 0.3)]), (150, 160, 110), shadow=LAYER)
    piece(c, Poly([(-10, 612), (-10, 470), (300, 430), (600, 440), (910, 470), (910, 612)]), (200, 180, 140), shadow=LAYER)
    for x, s in ((40, 1.3), (880, 1.1), (560, 0.8)):
        piece(c, Ell(x, 470, 40 * s, 26 * s), (150, 146, 140), border=1.2, shadow=PROP)
    # the pilgrims
    wukong(c, 160, 560, h=1.2, staff_up=True)
    white_horse(c, 300, 570, saddle=(60, 110, 170) if "saddle" in d else (200, 50, 40))
    tangseng(c, 302, 520, h=1.0, hat=(200, 200, 210) if "hat" in d else GOLDEN)
    bajie(c, 420, 576, h=1.15, rake=(200, 170, 60) if "rake" in d else (200, 200, 210))
    shaseng(c, 520, 578, h=1.1, luggage=(90, 140, 90) if "luggage" in d else (200, 140, 60))
    # the 'village girl' with her basket
    hx, hy = hanfu(c, 720, 586, (240, 170, 190) if "dress" not in d else (170, 200, 240), hat="lady", h=1.1)
    piece(c, [ellipse_top(760, 560, 16, 10), RRect(744, 560, 776, 574, 3)], (170, 130, 80), border=1.2, shadow=SMALL)
    flat(c, [Circ(752, 554, 4), Circ(762, 552, 4), Circ(770, 556, 4)], (240, 200, 60) if "basket" in d else (220, 60, 60))


L111_ELEMENTS = [
    E("wisp", lambda c, m: soft_union(c, [Ell(870, 440, 16, 30), Circ(870, 410, 12)], (240, 240, 250), 0.5, spread=12),
      anim=dict(twinkle=0.95, twinkleSpeed=0.1, bobAmplitude=(0, 10), bobSpeed=0.2)),
    bird_el("crow0", 500, 120, 9, col=(40, 40, 46), speed=14), bird_el("crow1", 526, 108, 7, col=(40, 40, 46), speed=14),
] + [E("leaf%d" % i, (lambda x, y: lambda c, m: flat(c, Poly(star_pts(x, y, 6, 2.6, points=5)), (220, 120, 50)))(x, y), pivot=(x, y),
       anim=dict(driftVelocity=(12, -22), driftLength=300, driftFade=True, rotateSpeed=80, phase=i * 0.2)) for i, (x, y) in
     enumerate(((90, 320), (260, 320), (840, 330), (700, 300), (180, 300)))]

L111_DIFFS = [
    ("tree", 700, 320, 0),
    ("saddle", 300, 520, 0),
    ("hat", 303, 474, 0),
    ("rake", 452, 498, 0),
    ("luggage", 520, 538, 0),
    ("dress", 720, 560, 0),
    ("basket", 762, 554, 0),
    ("tree2", 90, 320, 0),
]


# =================================================================== Level 112 the Flaming Mountain
def l112_bg(c, d):
    sky(c, (250, 190, 130), (255, 230, 170), 360)
    piece(c, Circ(160, 90, 34), (255, 150, 90) if "sun" in d else (255, 236, 160), border=2, shadow=PROP)
    for top, col in ((220, (200, 90, 50)), (280, (220, 110, 60)), (340, (190, 70, 40))):
        layer(c, top, [(30, 0.008, top * 0.01), (12, 0.03, 1.0)], col)
    # Princess Iron Fan on a ledge with her fan
    piece(c, Poly([(640, 420), (680, 300), (800, 280), (900, 300), (910, 420)]), (150, 70, 50), shadow=LAYER)
    flat(c, arch(740, 800, 330, 420), (40, 24, 20))
    if "door" not in d:
        piece(c, RRect(744, 352, 796, 420, 2), (110, 60, 40), shadow=SMALL)
        flat(c, Thick(770, 352, 770, 420, 2), (60, 34, 24))
    hx, hy = hanfu(c, 700, 300, (60, 160, 120) if "princess" in d else (180, 60, 140), hat="lady", h=1.1)
    flat(c, Thick(hx + 10, hy + 14, hx + 30, hy - 30, 2.4), (110, 80, 60))
    piece(c, Ell(hx + 40, hy - 52, 26, 34), (90, 150, 70) if "fan" not in d else (230, 190, 60), border=1.5, shadow=PROP)
    for k in range(5):
        flat(c, Thick(hx + 30, hy - 26, hx + 22 + k * 10, hy - 82 + abs(k - 2) * 6, 1), (60, 110, 50))
    # scorched plain with a dead tree and the pilgrims
    piece(c, hill_strip(440, [(5, 0.012, 0.4), (2, 0.04, 1.0)]), (200, 140, 90), shadow=LAYER)
    if "deadtree" not in d:
        flat(c, [Thick(560, 470, 556, 380, 6), Thick(556, 410, 530, 384, 3), Thick(556, 400, 584, 370, 3)], (90, 60, 50))
    wukong(c, 140, 580, h=1.2, staff_up="staff" not in d, staff=True)
    white_horse(c, 280, 586)
    tangseng(c, 282, 536, h=1.0)
    bajie(c, 400, 590, h=1.1)
    piece(c, [Ell(452, 560, 8, 10), Circ(452, 546, 5)], (90, 140, 200) if "gourd" in d else (200, 160, 80), border=1, shadow=SMALL)
    shaseng(c, 520, 592, h=1.05)
    for x in range(600, 900, 60):
        flat(c, Thick(x, 600, x + 30, 560, 2), (180, 110, 70))


L112_ELEMENTS = [E("flame%d" % i, (lambda x, y, s: lambda c, m: (soft_union(c, [Circ(x, y - 12 * s, 16 * s)], (255, 150, 50), 0.5, spread=18 * s),
                                                                   flat(c, Poly([(x - 14 * s, y), (x + 14 * s, y), (x + 9 * s, y - 20 * s), (x, y - 44 * s),
                                                                                 (x - 9 * s, y - 20 * s)]), (255, 120, 40)),
                                                                   flat(c, Poly([(x - 6 * s, y), (x + 6 * s, y), (x, y - 22 * s)]), (255, 220, 120))))(x, y, s),
                   pivot=(x, y), daynight="untinted", anim=dict(stretch=(0.12, 0.25), scaleSpeed=2.2 + i * 0.3, twinkle=0.15, twinkleSpeed=2.8,
                                                                phase=i * 0.17))
                 for i, (x, y, s) in enumerate(((60, 230, 1.4), (200, 240, 1.2), (330, 230, 1.5), (460, 250, 1.3), (580, 240, 1.2), (120, 300, 1.0),
                                                (400, 300, 1.1)))] + [
    E("haze", lambda c, m: soft_union(c, [Ell(450, 420, 400, 14)], (255, 230, 200), 0.3, spread=10), anim=dict(bobAmplitude=(0, 4), bobSpeed=0.5)),
    bird_el("bird0", 500, 120, 8, col=(90, 50, 40), speed=12),
]

L112_DIFFS = [
    ("door", 770, 386, 0),
    ("princess", 700, 274, 0),
    ("fan", 750, 200, 0),
    ("deadtree", 556, 410, 0),
    ("staff", 166, 520, 0),
    ("gourd", 452, 554, 0),
    ("sun", 160, 90, 0),
]


# =================================================================== Level 113 crossing the River that Reaches Heaven
TURTLE = (460, 450)


def l113_bg(c, d):
    sky(c, (180, 214, 236), (246, 238, 214), 320)
    layer(c, 230, [(20, 0.008, 0.4)], (150, 176, 170))
    for x0 in (20, 130, 760):
        piece(c, RRect(x0, 260, x0 + 90, 310, 1), (230, 220, 200), border=1.2, shadow=PROP)
        roof = (60, 120, 100) if (x0 == 760 and "roof" in d) else (150, 70, 60) if (x0 == 20 and "roof2" in d) else GREY_TILE
        cn_roof(c, x0, x0 + 90, 260, 16, roof, curl=8, ornaments=False)
    lantern_cn(c, 175, 296, (60, 160, 90) if "lantern" in d else (220, 50, 40), r=8)
    c.rect(0, 310, W, H, (90, 150, 180))
    for y in range(320, 600, 14):
        for x in range((y * 13) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (130, 184, 206))
    if "boat" not in d:
        piece(c, Poly([(700, 360), (800, 360), (790, 372), (710, 372)]), (110, 80, 56), border=1.2, shadow=SMALL)
        hanfu(c, 770, 362, (90, 90, 110), hat="straw", hat_col=(200, 176, 120), h=0.6)
    # the great white turtle with the pilgrims and scriptures
    x, y = TURTLE
    piece(c, [Ell(x, y, 190, 40), Ell(x + 200, y - 6, 30, 22), Ell(x - 160, y + 26, 30, 12), Ell(x + 150, y + 30, 30, 12)], (236, 236, 228), border=2,
          shadow=PROP)
    shell = (120, 170, 140) if "shell" in d else (200, 190, 160)
    for k in range(-3, 4):
        flat(c, Poly(star_pts(x + k * 46, y - 6, 18, 14, points=6)), shell)
    flat(c, [Circ(x + 210, y - 12, 3)], INK)
    wukong(c, x - 120, y - 20, h=1.0, staff=True)
    white_horse(c, x - 20, y - 18)
    tangseng(c, x - 18, y - 64, h=0.9, kasaya=(230, 180, 50) if "kasaya" in d else (200, 60, 50))
    bajie(c, x + 80, y - 18, h=0.95)
    shaseng(c, x + 150, y - 20, h=0.95)
    for k in range(3 if "sutra" not in d else 2):
        piece(c, RRect(x - 70 + k * 16, y - 36, x - 56 + k * 16, y - 20, 2), (200, 60, 50) if k != 1 else (230, 190, 60), border=1, shadow=SMALL)
    # near shore with reeds
    piece(c, hill_strip(560, [(4, 0.012, 0.3)]), (130, 170, 100), shadow=LAYER)
    for xx in range(10, 900, 18):
        flat(c, Thick(xx, 610, xx + 4, 540 + (xx % 30), 2.2), (90, 140, 80))


def jumping_fish(c, m):
    fish(c, 760, 470, 1.2, (250, 150, 60) if m else (200, 200, 210))


L113_ELEMENTS = [
    E("turtle_bob", lambda c, m: flat(c, Thick(TURTLE[0] - 200, TURTLE[1] + 40, TURTLE[0] + 220, TURTLE[1] + 40, 3), (220, 240, 250)),
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.3)),
    E("fish", jumping_fish, pivot=(760, 470), variant=True, anim=dict(bobAmplitude=(0, 30), bobSpeed=0.4, bounce=True, swingAngle=20, swingSpeed=0.4)),
    bird_el("bird0", 600, 120, 8, speed=14), bird_el("bird1", 626, 110, 6, speed=14),
]

L113_DIFFS = [
    ("lantern", 175, 296, 0),
    ("boat", 750, 360, 0),
    ("shell", TURTLE[0], TURTLE[1] - 6, 0),
    ("sutra", TURTLE[0] - 30, TURTLE[1] - 28, 0),
    ("fish", 760, 466, 0),
    ("roof", 805, 252, 0),
    ("kasaya", TURTLE[0] - 18, TURTLE[1] - 82, 0),
    ("roof2", 65, 252, 0),
]

LEVELS = [
    ("Level109", "花果山", l109_bg, L109_ELEMENTS, L109_DIFFS, 140, OPTS),
    ("Level110", "大闹天宫", l110_bg, L110_ELEMENTS, L110_DIFFS, 140, OPTS),
    ("Level111", "三打白骨精", l111_bg, L111_ELEMENTS, L111_DIFFS, 140, OPTS),
    ("Level112", "火焰山", l112_bg, L112_ELEMENTS, L112_DIFFS, 140, OPTS),
    ("Level113", "通天河", l113_bg, L113_ELEMENTS, L113_DIFFS, 140, OPTS),
]
