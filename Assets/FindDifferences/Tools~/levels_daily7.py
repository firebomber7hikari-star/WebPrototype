# -*- coding: utf-8 -*-
"""Everyday-town themes, part 7: work and transport (paper-craft side views, full-bleed, no real brands or logos):
  Level560 剪羊毛农场 - a sheep station: shearing shed, fluffy sheep, shearer, wool bales, sheepdog
  Level561 伐木场     - a lumber yard: log piles, sawmill with a spinning blade, log truck, logs floating down the river
  Level562 盐田       - salt pans: shallow pans mirroring the sky, white salt cones, rakers, a wind pump
  Level563 帆船赛     - a sailing regatta: racing dinghies, course buoys, committee boat, harbour town
  Level564 直升机停机坪 - a rooftop helipad: helicopter with turning rotor, windsock, crew, city skyline
  Level565 邮轮甲板   - a cruise-ship deck: pool, loungers, funnel, lifeboats, passengers, open sea
  Level566 山间缆车   - a mountain gondola: cabins gliding on the cable, valley station, pines, hikers; mist
  Level567 游艇码头   - a marina: moored yachts on pontoons, clubhouse, fuel dock, gulls
  Level568 河畔自行车道 - a riverside bike path: cyclists, railings, trees, river barge, skyline across the water
  Level569 火箭发射场 - a rocket launch site: rocket on the pad, service tower, control building; day / night
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_pine, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from stylekit import celestial, day_night, moon_element, star_field, sun_element, window_glow
from weather import fog_layer
from levels_daily5 import hiker

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def sea(c, y0, top=(90, 160, 210), bottom=(50, 110, 170), seed=0, n=16):
    c.gradient(y0, H, top, bottom)
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(0, 900), rnd.uniform(y0 + 10, H - 10)
        flat(c, Thick(x, y, x + rnd.uniform(20, 60), y, 2), lit(top, 1.25))


def dinghy(c, x, base, sail, s=1.0, hull=(250, 250, 250), number=None):
    piece(c, Poly([(x - 40 * s, base - 14 * s), (x + 46 * s, base - 14 * s), (x + 34 * s, base), (x - 32 * s, base)]), hull, border=1.2, shadow=SMALL)
    flat(c, Thick(x, base - 14 * s, x, base - 120 * s, 2.4 * s), (120, 120, 130))
    piece(c, Poly([(x + 3 * s, base - 118 * s), (x + 3 * s, base - 20 * s), (x + 60 * s, base - 20 * s)]), sail, border=1.2, shadow=SMALL)
    piece(c, Poly([(x - 3 * s, base - 100 * s), (x - 3 * s, base - 20 * s), (x - 36 * s, base - 20 * s)]), lit(sail, 1.1), border=1, shadow=None)
    if number:
        flat(c, Circ(x + 24 * s, base - 54 * s, 9 * s), (250, 250, 250))
        flat(c, Thick(x + 24 * s, base - 60 * s, x + 24 * s, base - 48 * s, 2 * s), (40, 40, 50))


def yacht(c, x, base, hull=(250, 250, 250), stripe=(60, 110, 190), s=1.0, cab=None, pennant=None):
    piece(c, Poly([(x - 90 * s, base - 30 * s), (x + 100 * s, base - 30 * s), (x + 80 * s, base), (x - 80 * s, base)]), hull, border=1.5, shadow=PROP)
    flat(c, RRect(x - 88 * s, base - 20 * s, x + 96 * s, base - 14 * s, 1), stripe)
    piece(c, RRect(x - 50 * s, base - 54 * s, x + 40 * s, base - 30 * s, 6), cab or hull, border=1.2, shadow=SMALL)
    for k in range(4):
        flat(c, RRect(x - 42 * s + k * 20 * s, base - 48 * s, x - 30 * s + k * 20 * s, base - 38 * s, 2), (60, 90, 130))
    flat(c, Thick(x - 4 * s, base - 54 * s, x - 4 * s, base - 200 * s, 2.4 * s), (150, 150, 160))
    if pennant:
        piece(c, Poly([(x - 2 * s, base - 198 * s), (x + 40 * s, base - 186 * s), (x - 2 * s, base - 172 * s)]), pennant, border=1, shadow=None)


# =================================================================== Level 560 sheep station
def sheep(c, x, base, s=1.0, wool=(246, 244, 236), shorn=False):
    legs = [RRect(x + dx * s - 3 * s, base - 22 * s, x + dx * s + 3 * s, base, 2) for dx in (-16, -8, 10, 18)]
    piece(c, legs, (60, 56, 60), shadow=SMALL)
    if shorn:
        piece(c, Ell(x, base - 30 * s, 26 * s, 13 * s), (236, 220, 200), border=1.2, shadow=PROP)
    else:
        piece(c, [Circ(x + dx * s, base - 30 * s + dy * s, 11 * s) for dx, dy in ((-18, 0), (-8, -8), (4, -10), (16, -6), (20, 4), (0, 4), (-14, 6))],
              wool, border=1.2, shadow=PROP)
    piece(c, [Ell(x + 30 * s, base - 36 * s, 9 * s, 7 * s), Ell(x + 26 * s, base - 44 * s, 5 * s, 3 * s)], (60, 56, 60), shadow=SMALL)
    flat(c, Circ(x + 32 * s, base - 38 * s, 1.6 * s), (250, 250, 250))


def l560_bg(c, d):
    sky(c, (130, 194, 240), (226, 238, 244), 300)
    cloud_bg(c, 200, 60, 0.8)
    far_ridge(c, 180, 50, (160, 196, 150), 5601)
    far_ridge(c, 220, 40, (140, 186, 120), 5602)
    piece(c, RRect(-10, 250, 910, 612, 0), (150, 196, 100), shadow=LAYER)
    # shearing shed (left)
    piece(c, RRect(40, 120, 380, 360, 2), (200, 200, 206), border=2, shadow=PROP)
    piece(c, Poly([(20, 126), (400, 126), (210, 60)]), (150, 70, 60), border=2, shadow=PROP)
    piece(c, [RRect(190, 70, 232, 104, 3), Poly([(184, 74), (238, 74), (211, 54)])], (200, 200, 206) if "vent" not in d else (240, 190, 60), border=1.2, shadow=SMALL)
    flat(c, [Thick(196, 84 + k * 7, 226, 84 + k * 7, 2) for k in range(3)], (150, 150, 160))
    for x in range(50, 380, 18):
        flat(c, Thick(x, 130, x, 356, 1.2), (186, 186, 194))
    flat(c, RRect(140, 200, 280, 360, 2), (60, 50, 50))
    # shearer + sheep being shorn in the doorway
    sheep(c, 200, 360, s=1.4, shorn=True)
    modern(c, 250, 360, (90, 130, 190), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.0)
    flat(c, Thick(236, 304, 216, 318, 3), (150, 150, 160))
    # wool bales stacked by the shed
    for k, (x, y) in enumerate(((410, 360), (470, 360), (440, 320))):
        piece(c, RRect(x - 28, y - 38, x + 28, y, 3), (236, 226, 200) if not (k == 2 and "bale" in d) else (200, 220, 240), border=1.2, shadow=PROP)
        flat(c, [Thick(x - 28, y - 26, x + 28, y - 26, 2), Thick(x - 28, y - 12, x + 28, y - 12, 2)], (180, 150, 110))
    # pen fence + sheep
    for x in range(520, 900, 50):
        flat(c, Thick(x, 470, x, 410, 4), (150, 110, 70))
    flat(c, [Thick(520, 424, 900, 424, 3), Thick(520, 446, 900, 446, 3)], (150, 110, 70))
    for k, (x, b, s) in enumerate(((600, 400, 1.2), (720, 390, 1.1), (840, 404, 1.2), (660, 520, 1.6), (820, 560, 1.7))):
        sheep(c, x, b, s=s, wool=(246, 244, 236) if not (k == 3 and "black" in d) else (70, 66, 70))
    # sheepdog + farmer
    piece(c, [Ell(380, 560, 24, 10), Circ(404, 548, 10), Ell(408, 538, 4, 7), Thick(356, 556, 342, 544, 4)] +
          [RRect(x - 2.4, 560, x + 2.4, 580, 1) for x in (366, 374, 390, 398)], (40, 40, 46), border=1, shadow=PROP)
    flat(c, [Ell(398, 556, 8, 6), Ell(404, 552, 5, 4)], (250, 250, 250))
    modern(c, 140, 600, (200, 80, 70) if "shirt" not in d else (90, 170, 120), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.3)
    piece(c, [Ell(141, 488, 26, 6), RRect(128, 474, 154, 490, 4)], (170, 130, 80), shadow=SMALL)
    # water trough
    piece(c, RRect(480, 560, 600, 590, 4), (150, 150, 160), border=1.2, shadow=PROP)
    flat(c, RRect(488, 562, 592, 572, 2), (120, 180, 220))


L560_ELEMENTS = [
    E("graze", lambda c, m: sheep(c, 720, 390, s=1.1), pivot=(752, 360), anim=dict(swingAngle=3, swingSpeed=0.4)),
    E("tail", lambda c, m: flat(c, Thick(356, 556, 340, 540, 4), (40, 40, 46)), pivot=(356, 556), anim=dict(swingAngle=22, swingSpeed=1.6)),
    E("tuft", lambda c, m: flat(c, Circ(190, 330, 6), (246, 244, 236)), anim=dict(driftVelocity=(-10, 10), driftLength=60, driftFade=True)),
    cloud_el("cloud", 600, 50, 0.6, 6),
    bird_el("bird", 500, 100, s=8, speed=-18),
]

L560_DIFFS = [
    ("vent", 211, 82, 0),
    ("bale", 440, 300, 0),
    ("black", 660, 494, 0),
    ("shirt", 140, 540, 0),
]


# =================================================================== Level 561 lumber yard
def log_pile(c, x, base, rows, col=(170, 120, 80), end=(220, 180, 130)):
    for r in range(rows):
        for k in range(rows - r):
            lx, ly = x + k * 34 + r * 17, base - 16 - r * 30
            piece(c, Circ(lx, ly, 16), col, border=1, shadow=SMALL)
            flat(c, Circ(lx, ly, 12), end)
            c.ellipse_ring(lx, ly, 7, 7, 1.2, lit(end, 0.85))


def l561_bg(c, d):
    sky(c, (140, 196, 236), (230, 236, 236), 300)
    far_ridge(c, 150, 70, (150, 180, 170), 5611)
    for k, x in enumerate(range(-10, 920, 40)):
        tree_pine(c, x, 250 + (k % 3) * 6, h=100 + (k * 23) % 40, col=(60, 120, 90))
    piece(c, RRect(-10, 250, 910, 612, 0), (180, 160, 120), shadow=LAYER)
    # river with floating logs (right)
    piece(c, Poly([(560, 250), (640, 250), (900, 420), (910, 612), (780, 612), (600, 330)]), (110, 170, 200), border=1.5, shadow=SMALL)
    # sawmill shed
    piece(c, RRect(220, 140, 520, 360, 2), (170, 110, 80), border=2, shadow=PROP)
    for x in range(230, 520, 20):
        flat(c, Thick(x, 144, x, 356, 1.4), (150, 96, 70))
    piece(c, RRect(460, 70, 490, 130, 2), (160, 100, 80) if "chimney" not in d else (90, 110, 160), border=1.2, shadow=PROP)
    piece(c, Poly([(200, 146), (540, 146), (370, 80)]), (90, 90, 100), border=2, shadow=PROP)
    flat(c, RRect(290, 230, 450, 360, 2), (60, 46, 40))
    piece(c, RRect(270, 320, 470, 340, 2), (120, 120, 130), shadow=SMALL)
    piece(c, RRect(300, 300, 440, 320, 3), (200, 150, 100), border=1, shadow=SMALL)
    # sign on the shed
    piece(c, RRect(300, 160, 440, 196, 4), (250, 210, 80) if "sign" not in d else (120, 200, 230), border=1.2, shadow=SMALL)
    sign_box(c, 316, 168, 424, 188, (90, 60, 40), 5612, vertical=False)
    # log piles
    log_pile(c, 40, 470, 4)
    log_pile(c, 560, 600, 3, col=(150, 100, 70) if "pile" not in d else (200, 160, 110))
    # log truck
    piece(c, RRect(190, 470, 470, 500, 3), (60, 120, 90), border=1.5, shadow=PROP)
    piece(c, Poly([(470, 500), (470, 440), (520, 440), (540, 466), (540, 500)]), (60, 120, 90) if "truck" not in d else (220, 120, 60), border=1.5, shadow=PROP)
    flat(c, Poly([(478, 446), (516, 446), (530, 466), (478, 466)]), (170, 210, 236))
    for k in range(3):
        piece(c, RRect(196, 440 - k * 22, 466, 462 - k * 22, 10), (170, 120, 80), border=1, shadow=SMALL)
        flat(c, Circ(200, 451 - k * 22, 9), (220, 180, 130))
    flat(c, [Thick(230, 400, 230, 470, 4), Thick(430, 400, 430, 470, 4)], (60, 60, 70))
    for wx in (230, 300, 500):
        piece(c, Circ(wx, 506, 15), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(wx, 506, 6), (190, 190, 200))
    # workers with hard hats
    for k, (x, hat) in enumerate(((120, (250, 200, 50)), (340, (250, 120, 50)), (840, (250, 200, 50)))):
        if k == 2 and "helmet" in d:
            hat = (250, 250, 250)
        modern(c, x, 600, (200, 70, 70) if k != 1 else (60, 110, 180), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.2)
        hx, hy = x + 2.2, 600 - 46 * 2.2
        piece(c, [Ell(hx, hy - 9, 20, 13), Ell(hx + 4, hy - 2, 26, 4)], hat, border=1, shadow=SMALL)
    # axe stuck in a stump
    piece(c, [Ell(700, 560, 40, 12), RRect(660, 520, 740, 560, 6)], (150, 110, 70), border=1.2, shadow=PROP)
    flat(c, Ell(700, 520, 40, 10), (220, 180, 130))
    flat(c, [Thick(700, 520, 720, 470, 4), Poly([(714, 484), (734, 470), (738, 490)])], (120, 120, 130))


L561_ELEMENTS = [
    spin_el("saw", lambda c, m: (piece(c, Circ(370, 290, 28), (200, 204, 214), border=1, shadow=SMALL),
                                 flat(c, [Poly([(370 + 28 * math.cos(a), 290 + 28 * math.sin(a)), (370 + 34 * math.cos(a + 0.15), 290 + 34 * math.sin(a + 0.15)),
                                                (370 + 28 * math.cos(a + 0.3), 290 + 28 * math.sin(a + 0.3))]) for a in [k * math.pi / 8 for k in range(16)]],
                                      (170, 176, 190)),
                                 flat(c, Circ(370, 290, 6), (90, 90, 100))), (370, 290), 300),
    E("sawdust", lambda c, m: [flat(c, Circ(400 + k * 8, 300 - k * 4, 2.4), (230, 200, 150)) for k in range(4)],
      anim=dict(driftVelocity=(20, 10), driftLength=40, driftFade=True)),
    E("float1", lambda c, m: (piece(c, RRect(610, 290, 680, 306, 8), (160, 110, 70), shadow=SMALL), flat(c, Ell(610, 298, 5, 8), (220, 180, 130))),
      anim=dict(driftVelocity=(36, -24), driftLength=300, driftFade=True)),
    E("float2", lambda c, m: (piece(c, RRect(610, 290, 670, 306, 8), (150, 100, 70), shadow=SMALL), flat(c, Ell(610, 298, 5, 8), (220, 180, 130))),
      anim=dict(driftVelocity=(36, -24), driftLength=300, driftFade=True, phase=0.5)),
    bird_el("bird", 300, 50, s=8, speed=18),
]

L561_DIFFS = [
    ("chimney", 475, 90, 0),
    ("sign", 370, 178, 0),
    ("pile", 600, 560, 0),
    ("truck", 505, 470, 0),
    ("helmet", 842, 490, 0),
]


# =================================================================== Level 562 salt pans
def l562_bg(c, d):
    sky(c, (120, 180, 236), (240, 226, 210), 260)
    cloud_bank(c, 120, (250, 248, 244), 5621, k=0.6)
    sea(c, 220, seed=5622, n=8)
    flat(c, RRect(0, 220, W, 240, 0), (70, 140, 190))
    # pans grid (mirror the sky)
    piece(c, RRect(-10, 240, 910, 612, 0), (200, 186, 166), shadow=LAYER)
    for r, (y0, y1) in enumerate(((256, 330), (344, 440), (456, 600))):
        for k in range(4):
            x0, x1 = -10 + k * 230 + 8, -10 + (k + 1) * 230 - 8
            col = [(200, 220, 240), (230, 214, 226), (210, 226, 236)][(k + r) % 3]
            if r == 1 and k == 2 and "pan" in d:
                col = (240, 200, 200)
            flat(c, RRect(x0, y0, x1, y1, 2), col)
            flat(c, Poly([(x0 + 20, y0 + 10), (x0 + 60, y0 + 10), (x0 + 30, y1 - 10), (x0 - 10 + 20, y1 - 10)]), (250, 250, 252, 0.5))
    # salt cones
    for k, (x, b, s) in enumerate(((150, 330, 1.0), (330, 440, 1.3), (600, 330, 1.1), (780, 440, 1.4), (450, 600, 1.6))):
        piece(c, Poly([(x - 40 * s, b), (x + 40 * s, b), (x, b - 50 * s)]), (250, 250, 252) if not (k == 3 and "salt" in d) else (240, 210, 200),
              border=1.2, border_col=(220, 220, 228), shadow=PROP)
        flat(c, Poly([(x, b - 50 * s), (x + 40 * s, b), (x + 10 * s, b)]), (230, 232, 240))
    # wind pump (right)
    flat(c, [Thick(820, 330, 840, 180, 4), Thick(870, 330, 850, 180, 4), Thick(830, 260, 860, 260, 3)], (150, 120, 90))
    piece(c, Poly([(846, 176), (896, 158), (896, 194)]), (220, 70, 70) if "vane" not in d else (60, 140, 200), border=1, shadow=SMALL)
    # wooden boardwalk + rakers + wheelbarrow
    piece(c, RRect(-10, 440, 910, 456, 1), (170, 130, 90), border=1, shadow=SMALL)
    for x in range(0, 900, 30):
        flat(c, Thick(x, 440, x, 456, 1.2), (150, 110, 76))
    modern(c, 200, 440, (60, 110, 180), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.0)
    piece(c, [Ell(202, 334, 30, 8), Ell(202, 328, 14, 8)], (230, 200, 120), shadow=SMALL)
    flat(c, [Thick(220, 420, 270, 330, 3), Thick(256, 330, 286, 340, 4)], (150, 110, 70))
    modern(c, 680, 440, (220, 90, 80) if "shirt" not in d else (90, 180, 110), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.0)
    piece(c, [Ell(682, 334, 30, 8), Ell(682, 328, 14, 8)], (230, 200, 120), shadow=SMALL)
    flat(c, [Thick(660, 420, 610, 340, 3), Thick(596, 340, 626, 330, 4)], (150, 110, 70))
    piece(c, [Poly([(80, 560), (180, 560), (160, 590), (100, 590)]), Thick(180, 562, 220, 576, 4)], (90, 150, 210), border=1.2, shadow=PROP)
    flat(c, Ell(130, 556, 44, 10), (250, 250, 252))
    piece(c, Circ(96, 596, 10), (40, 40, 46), shadow=SMALL)


L562_ELEMENTS = [
    spin_el("pump", lambda c, m: flat(c, [Thick(845 - 26 * math.cos(a), 176 - 26 * math.sin(a), 845 + 26 * math.cos(a), 176 + 26 * math.sin(a), 5)
                                         for a in [k * math.pi / 4 for k in range(4)]], (220, 220, 226)), (845, 176), 120),
    E("shimmer", lambda c, m: [flat(c, Thick(60 + k * 220, 300, 110 + k * 220, 300, 2), (255, 255, 255, 0.8)) for k in range(4)],
      anim=dict(twinkle=0.6, twinkleSpeed=0.6)),
    bird_el("gull", 300, 160, s=8, speed=-20),
    bird_el("gull2", 600, 180, s=7, speed=24),
]

L562_DIFFS = [
    ("pan", 585, 392, 0),
    ("salt", 780, 405, 0),
    ("vane", 878, 176, 0),
    ("shirt", 680, 375, 0),
]


# =================================================================== Level 563 sailing regatta
def l563_bg(c, d):
    sky(c, (120, 186, 236), (226, 236, 244), 260)
    cloud_bg(c, 160, 60, 0.8)
    cloud_bg(c, 720, 40, 0.6)
    # harbour town on the far shore
    far_ridge(c, 200, 30, (150, 186, 170), 5631)
    for k in range(12):
        x = 20 + k * 75
        col = [(240, 200, 170), (250, 246, 236), (200, 216, 236), (240, 220, 180)][k % 4]
        piece(c, RRect(x, 196 - (k % 3) * 14, x + 60, 240, 2), col, border=1, shadow=SMALL)
        flat(c, Poly([(x - 4, 198 - (k % 3) * 14), (x + 64, 198 - (k % 3) * 14), (x + 30, 176 - (k % 3) * 14)]), (200, 90, 70))
    sea(c, 240, seed=5632, n=22)
    # course buoys
    for k, x in enumerate((120, 760)):
        piece(c, [Ell(x, 420, 18, 8), Poly([(x - 14, 420), (x + 14, 420), (x, 384)])], (250, 140, 40) if not (k == 1 and "buoy" in d) else (220, 60, 160),
              border=1.2, shadow=SMALL)
    # dinghies
    for k, (x, b, s, col) in enumerate(((240, 360, 1.0, (250, 250, 250)), (440, 330, 0.8, (220, 70, 70)), (620, 380, 1.1, (60, 120, 210)), (300, 520, 1.5, (250, 200, 60)),
                                        (700, 560, 1.6, (250, 250, 250)))):
        if k == 2 and "sail" in d:
            col = (120, 200, 120)
        dinghy(c, x, b, col, s=s, number=(k == 4))
    # committee boat with flags (right front)
    piece(c, Poly([(760, 600), (910, 600), (910, 560), (780, 560)]), (250, 250, 250), border=1.5, shadow=PROP)
    piece(c, RRect(800, 520, 880, 560, 4), (250, 250, 250), border=1.2, shadow=SMALL)
    flat(c, Thick(840, 520, 840, 420, 3), (150, 150, 160))
    for k, col in enumerate(((220, 60, 60), (250, 200, 60), (60, 110, 200))):
        if k == 1 and "flag" in d:
            col = (90, 180, 110)
        piece(c, RRect(842, 426 + k * 26, 878, 446 + k * 26, 1), col, border=0.8, shadow=None)
    modern(c, 820, 560, (60, 110, 180), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.4)
    # starting line marker boat (left front)
    piece(c, Poly([(10, 600), (150, 600), (140, 570), (20, 570)]), (220, 70, 70) if "boat" not in d else (90, 150, 210), border=1.5, shadow=PROP)
    modern(c, 80, 580, (250, 200, 60), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.3)


L563_ELEMENTS = [
    E("bob%d" % i, (lambda x, b, s, col: lambda c, m: dinghy(c, x, b, col, s=s))(x, b, s, col), pivot=(x, b), anim=dict(swingAngle=4, swingSpeed=0.4, phase=i / 2))
    for i, (x, b, s, col) in enumerate(((240, 360, 1.0, (250, 250, 250)), (440, 330, 0.8, (220, 70, 70))))
] + [
    E("racer", lambda c, m: dinghy(c, 0, 300, (240, 120, 160), s=0.7), anim=dict(drift_across(-30, 50, 26, start=600))),
    bird_el("gull", 500, 120, s=9, speed=-20),
    E("spray", lambda c, m: soft_union(c, [Ell(720, 560, 30, 6)], (240, 248, 252), 0.7, spread=8), anim=dict(pulse=0.2, scaleSpeed=0.8, twinkle=0.3)),
]

L563_DIFFS = [
    ("buoy", 760, 408, 0),
    ("sail", 650, 320, 0),
    ("flag", 860, 462, 0),
    ("boat", 80, 585, 0),
]


# =================================================================== Level 564 rooftop helipad
def helicopter(c, x, base, col=(220, 70, 70), s=1.0, fin=None):
    piece(c, [Ell(x, base - 40 * s, 70 * s, 34 * s), RRect(x + 50 * s, base - 50 * s, x + 170 * s, base - 36 * s, 6)], col, border=1.5, shadow=PROP)
    piece(c, Poly([(x + 150 * s, base - 50 * s), (x + 186 * s, base - 84 * s), (x + 184 * s, base - 36 * s), (x + 156 * s, base - 36 * s)]), fin or col,
          border=1.5, shadow=SMALL)
    flat(c, Poly([(x - 60 * s, base - 46 * s), (x - 30 * s, base - 70 * s), (x + 10 * s, base - 70 * s), (x + 10 * s, base - 40 * s), (x - 64 * s, base - 36 * s)]),
         (170, 210, 236))
    flat(c, RRect(x - 20 * s, base - 44 * s, x + 40 * s, base - 38 * s, 1), (250, 250, 250))
    flat(c, [Thick(x - 40 * s, base, x + 50 * s, base, 4 * s), Thick(x - 20 * s, base, x - 20 * s, base - 10 * s, 3 * s), Thick(x + 30 * s, base, x + 30 * s, base - 10 * s, 3 * s)],
         (60, 60, 70))
    flat(c, RRect(x - 6 * s, base - 84 * s, x + 6 * s, base - 72 * s, 2), (60, 60, 70))


def l564_bg(c, d):
    sky(c, (110, 170, 230), (226, 230, 240), 420)
    cloud_bank(c, 140, (250, 250, 246), 5641, k=0.6)
    far_skyline(c, 360, 80, 280, (170, 186, 214), 5642, win=(200, 210, 230))
    # neighbouring towers
    for k, (x, w, h, col) in enumerate(((-10, 150, 330, (150, 170, 200)), (760, 160, 300, (170, 180, 206)))):
        piece(c, RRect(x, 420 - h, x + w, 440, 2), col, border=1.5, shadow=PROP)
        for y in range(420 - h + 20, 420, 34):
            for wx in range(int(x) + 14, int(x + w) - 20, 30):
                lit_ = (250, 220, 140) if (wx + y) % 3 == 0 else (200, 216, 236)
                if k == 1 and y == 420 - h + 54 and wx < 820 and "window" in d:
                    lit_ = (240, 120, 120)
                flat(c, RRect(wx, y, wx + 20, y + 24, 1), lit_)
    # rooftop deck
    piece(c, RRect(-10, 440, 910, 612, 0), (110, 116, 126), shadow=LAYER)
    piece(c, Ell(450, 520, 300, 60), (90, 96, 106), border=1.5, shadow=SMALL)
    c.ellipse_ring(450, 520, 280, 54, 5, (250, 220, 60))
    flat(c, [Thick(400, 490, 400, 550, 10), Thick(500, 490, 500, 550, 10), Thick(400, 520, 500, 520, 10)], (250, 250, 250))
    # edge lights
    for x in range(30, 900, 60):
        flat(c, Circ(x, 446, 4), (90, 200, 120))
    # helicopter on the pad
    helicopter(c, 430, 520, col=(220, 70, 70), s=1.3, fin=(220, 70, 70) if "fin" not in d else (60, 110, 200))
    # crew + fuel cart
    modern(c, 160, 600, (250, 160, 40), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.2)
    piece(c, [Ell(162, 488, 13, 10)], (250, 250, 250), shadow=SMALL)
    flat(c, Thick(176, 520, 210, 500, 3), (250, 160, 40))
    modern(c, 760, 600, (60, 70, 90), bottom=(40, 40, 50), hair=(90, 60, 40), h=2.2)
    piece(c, RRect(790, 520, 880, 580, 4), (250, 200, 60) if "cart" not in d else (120, 200, 120), border=1.5, shadow=PROP)
    for wx in (806, 864):
        piece(c, Circ(wx, 586, 10), (40, 40, 46), shadow=SMALL)
    # stair-house + antenna (left)
    piece(c, RRect(20, 360, 120, 446, 2), (180, 186, 196), border=1.5, shadow=PROP)
    flat(c, RRect(46, 384, 94, 446, 2), (90, 96, 110) if "door" not in d else (200, 120, 60))
    flat(c, [Thick(70, 360, 70, 290, 3), Thick(56, 310, 84, 310, 2)], (120, 120, 130))


def rotor(c, m):
    flat(c, [Thick(430 - 150 * math.cos(a), 410 - 6 * math.sin(a), 430 + 150 * math.cos(a), 410 + 6 * math.sin(a), 5) for a in (0.0, 1.57)], (60, 60, 70))


L564_ELEMENTS = [
    E("rotor", rotor, pivot=(430, 410), anim=dict(stretch=(0.95, 0), scaleSpeed=6.0)),
    E("tailrotor", lambda c, m: flat(c, [Thick(668, 438, 668, 462, 3), Thick(656, 450, 680, 450, 3)], (60, 60, 70)), pivot=(668, 450), anim=dict(rotateSpeed=600)),
    E("sock", lambda c, m: (flat(c, Thick(880, 446, 880, 380, 3), (150, 150, 160)),
                            piece(c, Poly([(881, 380), (910, 386), (910, 396), (881, 400)]), (250, 130, 50), border=1, shadow=SMALL)),
      pivot=(880, 390), anim=dict(swingAngle=8, swingSpeed=0.6)),
    E("beacon", lambda c, m: soft_union(c, [Circ(70, 288, 4)], (255, 80, 80), 0.8, spread=10), daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=1.0)),
    bird_el("bird", 600, 80, s=8, speed=20),
]

L564_DIFFS = [
    ("window", 790, 174, 0),
    ("door", 70, 415, 0),
    ("fin", 655, 440, 0),
    ("cart", 835, 550, 0),
]


# =================================================================== Level 565 cruise-ship deck
def lounger(c, x, base, col):
    piece(c, [Poly([(x - 50, base - 16), (x + 30, base - 16), (x + 50, base - 40), (x + 40, base - 44), (x + 22, base - 22), (x - 50, base - 22)])], col, border=1,
          shadow=SMALL)
    flat(c, [Thick(x - 44, base - 16, x - 44, base, 2), Thick(x + 24, base - 16, x + 24, base, 2)], (150, 150, 160))


def l565_bg(c, d):
    sky(c, (110, 180, 236), (226, 236, 244), 240)
    cloud_bg(c, 140, 60, 0.8)
    sea(c, 200, seed=5651, n=10)
    # superstructure + funnel
    piece(c, RRect(500, 40, 910, 260, 3), (250, 250, 250), border=1.5, shadow=PROP)
    for r in range(3):
        for k in range(8):
            flat(c, RRect(520 + k * 48, 60 + r * 56, 554 + k * 48, 90 + r * 56, 4), (60, 90, 130))
    piece(c, Poly([(680, 40), (780, 40), (770, -10), (690, -10)]), (220, 60, 60) if "funnel" not in d else (60, 110, 200), border=1.5, shadow=PROP)
    flat(c, RRect(684, 10, 776, 20, 1), (40, 40, 50))
    # lifeboats hanging
    for k, x in enumerate((540, 660, 780)):
        piece(c, RRect(x, 230, x + 100, 256, 12), (250, 140, 40) if not (k == 1 and "lifeboat" in d) else (250, 220, 70), border=1.2, shadow=PROP)
    # railings + deck
    piece(c, RRect(-10, 300, 910, 612, 0), (200, 170, 130), shadow=LAYER)
    for x in range(0, 900, 36):
        flat(c, Thick(x, 300, x + 36, 300, 1.2), (180, 150, 112))
    for y in range(320, 612, 26):
        flat(c, Thick(0, y, W, y, 1.2), (186, 156, 118))
    flat(c, [Thick(0, 260, 500, 260, 4), Thick(0, 280, 500, 280, 2)] + [Thick(x, 260, x, 300, 2) for x in range(0, 500, 24)], (250, 250, 250))
    # pool
    piece(c, RRect(120, 360, 460, 470, 10), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(132, 372, 448, 458, 8), (90, 190, 230))
    for k in range(5):
        flat(c, Thick(150 + k * 60, 410, 190 + k * 60, 410, 2), (170, 226, 246))
    piece(c, Circ(240, 410, 14), (250, 90, 90) if "ring" not in d else (250, 220, 60), border=1, shadow=SMALL)
    flat(c, Circ(240, 410, 7), (90, 190, 230))
    modern(c, 360, 452, (240, 200, 90), bottom=(240, 200, 90), hair=(40, 30, 30), h=1.3)
    # loungers with sunbathers + parasol
    for k, x in enumerate((560, 700, 840)):
        lounger(c, x, 420, (250, 250, 250) if not (k == 1 and "lounger" in d) else (240, 120, 160))
    piece(c, Poly([(600, 330), (720, 330), (660, 300)]), (60, 140, 200), border=1.2, shadow=PROP)
    flat(c, Thick(660, 330, 660, 420, 3), (150, 150, 160))
    # passengers strolling
    modern(c, 120, 600, (90, 150, 220), bottom=(50, 60, 90), hair=(130, 130, 140), h=2.3, glasses=True)
    modern(c, 520, 600, (250, 250, 250), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.3, style="long")
    piece(c, [Ell(522, 490, 26, 7), Ell(522, 484, 12, 8)], (230, 200, 120), shadow=SMALL)
    modern(c, 760, 600, (60, 60, 70), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3)
    # deck bar
    piece(c, RRect(260, 500, 420, 560, 4), (150, 100, 70), border=1.5, shadow=PROP)
    flat(c, RRect(260, 500, 420, 510, 3), (120, 80, 56))
    for k in range(3):
        piece(c, [Poly([(290 + k * 50, 480), (310 + k * 50, 480), (302 + k * 50, 498), (298 + k * 50, 498)])], [(250, 160, 60), (90, 200, 230), (240, 120, 160)][k],
              border=0.8, shadow=None)


L565_ELEMENTS = [
    E("smoke", lambda c, m: soft_union(c, [Circ(730, -6, 12)], (230, 230, 236), 0.7, spread=10),
      anim=dict(driftVelocity=(-20, 10), driftLength=80, driftFade=True, driftGrow=1.6)),
    E("flag", lambda c, m: (flat(c, Thick(20, 260, 20, 200, 2), (150, 150, 160)), piece(c, Poly([(21, 200), (60, 208), (21, 220)]), (60, 110, 200), border=1, shadow=SMALL)),
      pivot=(20, 210), anim=dict(stretch=(0.15, 0), scaleSpeed=1.4)),
    E("ripple", lambda c, m: c.ellipse_ring(360, 448, 26, 6, 2, (200, 240, 250)), pivot=(360, 448), anim=dict(pulse=0.3, scaleSpeed=0.7, twinkle=0.4)),
    bird_el("gull", 300, 120, s=9, speed=-20),
    E("dolphin", lambda c, m: piece(c, Poly([(0, 230), (20, 214), (46, 220), (40, 230)]), (120, 140, 170), border=1, shadow=None),
      anim=dict(drift_across(0, 46, 30, start=200), bobAmplitude=(0, 8), bobSpeed=0.5)),
]

L565_DIFFS = [
    ("funnel", 730, 20, 0),
    ("lifeboat", 710, 243, 0),
    ("ring", 240, 410, 0),
    ("lounger", 700, 400, 0),
]


# =================================================================== Level 566 mountain gondola (mist)
STEPS566 = [(CLEAR, 12), (FOG, 8)]
CABLE566 = ((120, 470), (820, 90))


def cabin(c, x, y, col):
    flat(c, Thick(x, y, x, y + 26, 2), (70, 70, 80))
    piece(c, RRect(x - 22, y + 24, x + 22, y + 64, 8), col, border=1.2, shadow=SMALL)
    flat(c, RRect(x - 16, y + 30, x + 16, y + 46, 3), (170, 210, 236))


def l566_bg(c, d):
    sky(c, (120, 180, 236), (220, 232, 246), 300)
    # mountains
    piece(c, Poly([(-10, 320), (160, 120), (300, 240), (470, 60), (640, 220), (780, 100), (910, 200), (910, 340), (-10, 340)]), (170, 186, 210), shadow=LAYER)
    for (px, py), w in (((160, 120), 40), ((470, 60), 60), ((780, 100), 46)):
        flat(c, Poly([(px - w, py + w), (px, py), (px + w, py + w), (px, py + w * 0.8)]), (246, 248, 252))
    piece(c, Poly([(-10, 360), (300, 300), (600, 330), (910, 280), (910, 612), (-10, 612)]), (120, 170, 100), shadow=LAYER)
    for k, x in enumerate(range(-10, 920, 44)):
        if 360 < x < 480:
            continue
        tree_pine(c, x, 360 - (x * 0.05) + (k % 3) * 10, h=80 + (k * 17) % 40, col=(60, 120, 80))
    # cable + towers
    (x0, y0), (x1, y1) = CABLE566
    for f in (0.3, 0.65):
        tx, ty = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        piece(c, [RRect(tx - 6, ty, tx + 6, ty + 200, 1), RRect(tx - 24, ty - 4, tx + 24, ty + 4, 2)], (150, 150, 160) if not (f == 0.65 and "tower" in d)
              else (220, 120, 60), shadow=PROP)
    flat(c, Thick(x0, y0, x1, y1, 2), (60, 60, 70))
    # a parked cabin at the valley station
    piece(c, RRect(30, 420, 240, 560, 3), (200, 200, 206), border=1.5, shadow=PROP)
    piece(c, Poly([(20, 424), (250, 424), (200, 380), (70, 380)]), (90, 90, 100), border=1.5, shadow=PROP)
    flat(c, RRect(60, 460, 210, 560, 2), (60, 60, 70))
    cabin(c, 136, 444, (220, 70, 70) if "cabin" not in d else (250, 200, 60))
    piece(c, RRect(60, 392, 210, 416, 3), (250, 250, 250), border=1, shadow=SMALL)
    sign_box(c, 72, 398, 198, 410, (60, 110, 180), 5661, vertical=False)
    # meadow with hikers + bench + signpost
    hiker(c, 420, 600, (240, 120, 60), (60, 110, 180) if "pack" not in d else (250, 200, 60), h=2.3)
    hiker(c, 500, 600, (90, 160, 120), (200, 70, 70), h=2.2, hair=(220, 180, 90), style="long")
    piece(c, [RRect(640, 560, 800, 572, 3), RRect(648, 572, 656, 606, 2), RRect(784, 572, 792, 606, 2), RRect(640, 540, 800, 550, 3)], (130, 90, 60),
          border=1.2, shadow=PROP)
    flat(c, Thick(860, 600, 860, 500, 4), (120, 90, 60))
    piece(c, Poly([(860, 504), (900, 504), (910, 516), (900, 528), (860, 528)]), (230, 200, 120) if "sign" not in d else (110, 180, 210), border=1, shadow=SMALL)
    for k in range(12):
        rnd = random.Random(5662 + k)
        flat(c, Circ(rnd.uniform(560, 900), rnd.uniform(470, 600), 4), rnd.choice([(250, 220, 90), (250, 250, 250), (220, 120, 200)]))


def moving_cabin(i, col):
    (x0, y0), (x1, y1) = CABLE566
    L = math.hypot(x1 - x0, y1 - y0)
    return E("cab%d" % i, lambda c, m: cabin(c, x0, y0, col), anim=dict(driftVelocity=((x1 - x0) / L * 30, -(y1 - y0) / L * 30), driftLength=L * 0.98, phase=i / 3))


L566_ELEMENTS = [moving_cabin(i, col) for i, col in enumerate(((220, 70, 70), (60, 120, 210), (250, 200, 60)))] + [
    bird_el("eagle", 600, 60, s=12, speed=-14),
    fog_layer("fog", 566, 260, 420, 0.35, 12),
]

L566_DIFFS = [
    ("tower", 575, 290, 0),
    ("cabin", 136, 500, 0),
    ("pack", 427, 525, 0),
    ("sign", 885, 516, 0),
]


# =================================================================== Level 567 marina
def l567_bg(c, d):
    sky(c, (120, 186, 236), (230, 236, 240), 260)
    cloud_bank(c, 110, (250, 250, 246), 5671, k=0.6)
    far_ridge(c, 210, 40, (150, 186, 170), 5672)
    # clubhouse on the quay (right)
    piece(c, RRect(620, 120, 900, 260, 3), (250, 246, 236), border=1.5, shadow=PROP)
    piece(c, Poly([(600, 126), (920, 126), (880, 90), (640, 90)]), (60, 110, 160), border=1.5, shadow=PROP)
    for x in (640, 720, 800):
        flat(c, RRect(x, 150, x + 60, 210, 3), (150, 196, 226) if not (x == 800 and "window" in d) else (250, 210, 120))
    for x in range(620, 900, 30):
        flat(c, Thick(x, 230, x + 15, 230, 2), (60, 110, 160))
    piece(c, RRect(-10, 250, 910, 270, 1), (190, 186, 180), shadow=PROP)
    sea(c, 270, seed=5673, n=16)
    # pontoons
    for y in (360, 500):
        piece(c, RRect(-10, y, 910, y + 14, 1), (200, 170, 130), border=1, shadow=SMALL)
        for x in range(30, 900, 180):
            piece(c, RRect(x - 4, y + 14, x + 4, y + 50, 1), (150, 120, 90), shadow=None)
    # moored yachts (masts)
    yacht(c, 160, 360, stripe=(60, 110, 190))
    yacht(c, 500, 360, stripe=(220, 70, 70), pennant=(250, 200, 60) if "pennant" not in d else (220, 70, 160))
    yacht(c, 820, 360, stripe=(40, 40, 50), s=0.9)
    yacht(c, 320, 500, stripe=(250, 180, 60), s=1.1)
    yacht(c, 700, 500, stripe=(60, 110, 190), s=1.2, cab=(250, 250, 250) if "cab" not in d else (250, 200, 120))
    # fuel dock pump + life ring + people
    piece(c, RRect(30, 300, 70, 360, 4), (220, 60, 60) if "pump" not in d else (60, 160, 110), border=1.2, shadow=PROP)
    flat(c, RRect(38, 310, 62, 330, 2), (250, 250, 250))
    c.ellipse_ring(560, 540, 16, 16, 8, (250, 140, 40) if "ring" not in d else (90, 200, 220))
    modern(c, 600, 500, (60, 110, 180), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.8)
    modern(c, 880, 500, (250, 250, 250), bottom=(60, 60, 80), hair=(220, 180, 90), h=1.8, style="long")
    # crates + rope coil
    piece(c, RRect(400, 470, 440, 500, 2), (190, 150, 100), border=1, shadow=SMALL)
    c.ellipse_ring(470, 492, 14, 6, 4, (220, 200, 160))


L567_ELEMENTS = [
    E("rock%d" % i, (lambda x, b, s, st: lambda c, m: yacht(c, x, b, stripe=st, s=s))(x, b, s, st), pivot=(x, b), anim=dict(swingAngle=1.5, swingSpeed=0.3, phase=i / 2))
    for i, (x, b, s, st) in enumerate(((160, 360, 1.0, (60, 110, 190)), (820, 360, 0.9, (40, 40, 50))))
] + [
    bird_el("gull1", 300, 80, s=9, speed=-20),
    bird_el("gull2", 640, 300, s=8, speed=22),
    E("buoy", lambda c, m: piece(c, [Ell(260, 590, 14, 6), RRect(252, 566, 268, 588, 3)], (250, 200, 60), border=1, shadow=SMALL), pivot=(260, 590),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.5)),
]

L567_DIFFS = [
    ("window", 830, 180, 0),
    ("pennant", 512, 175, 0),
    ("cab", 694, 449, 0),
    ("pump", 50, 330, 0),
    ("ring", 560, 540, 0),
]


# =================================================================== Level 568 riverside bike path
def cyclist(c, x, base, top, frame, s=1.0, hair=(40, 30, 30), helmet=(250, 250, 250)):
    for wx in (x - 30 * s, x + 30 * s):
        c.ellipse_ring(wx, base - 20 * s, 20 * s, 20 * s, 3 * s, (40, 40, 46))
    flat(c, [Thick(x - 30 * s, base - 20 * s, x - 4 * s, base - 54 * s, 3 * s), Thick(x - 4 * s, base - 54 * s, x + 22 * s, base - 54 * s, 3 * s),
             Thick(x + 22 * s, base - 54 * s, x + 30 * s, base - 20 * s, 3 * s), Thick(x - 4 * s, base - 54 * s, x, base - 20 * s, 3 * s),
             Thick(x, base - 20 * s, x - 30 * s, base - 20 * s, 3 * s)], frame)
    modern(c, x - 2 * s, base - 30 * s, top, bottom=(40, 40, 50), hair=hair, h=1.2 * s)
    piece(c, Ell(x - 1 * s, base - 30 * s - 62 * s, 10 * s, 6 * s), helmet, border=1, shadow=None)


def l568_bg(c, d):
    sky(c, (130, 190, 236), (230, 236, 240), 260)
    cloud_bg(c, 200, 60, 0.7)
    far_skyline(c, 220, 60, 170, (176, 190, 214), 5681, win=(200, 210, 230))
    # river
    sea(c, 220, top=(110, 170, 200), bottom=(80, 140, 180), seed=5682, n=12)
    # arched bridge across the river (left)
    piece(c, Poly([(-10, 200), (330, 200), (330, 220), (-10, 220)]), (190, 180, 170), border=1.5, shadow=PROP)
    for x in (60, 200):
        piece(c, Poly([(x, 220), (x + 30, 220), (x + 26, 300), (x + 4, 300)]), (180, 170, 160), shadow=SMALL)
    # barge (static)
    piece(c, Poly([(500, 300), (760, 300), (740, 330), (520, 330)]), (120, 70, 60) if "barge" not in d else (60, 110, 160), border=1.5, shadow=PROP)
    piece(c, RRect(680, 270, 740, 300, 3), (250, 246, 236), border=1, shadow=SMALL)
    piece(c, RRect(530, 284, 660, 300, 2), (250, 200, 60), border=1, shadow=SMALL)
    # embankment + railing
    piece(c, RRect(-10, 360, 910, 612, 0), (150, 196, 110), shadow=LAYER)
    flat(c, RRect(-10, 360, 910, 376, 0), (200, 196, 186))
    flat(c, [Thick(0, 384, W, 384, 3)] + [Thick(x, 384, x, 410, 3) for x in range(10, 900, 40)], (90, 96, 110))
    # bike path
    piece(c, RRect(-10, 470, 910, 540, 0), (110, 116, 126), shadow=SMALL)
    flat(c, [Thick(x, 506, x + 40, 506, 3) for x in range(0, 900, 80)], (250, 250, 240))
    flat(c, [Poly([(440, 520), (460, 520), (466, 494), (434, 494)])], (250, 250, 240))
    # trees + benches + bin along the path
    for k, x in enumerate((80, 380, 700)):
        tree_round(c, x, 460, s=1.5, col=(90, 160, 90) if not (k == 1 and "tree" in d) else (230, 150, 60))
    piece(c, [RRect(520, 440, 640, 452, 3), RRect(528, 452, 536, 470, 2), RRect(624, 452, 632, 470, 2), RRect(520, 420, 640, 430, 3)], (60, 110, 80), shadow=PROP)
    modern(c, 580, 450, (240, 180, 90), bottom=(60, 60, 80), hair=(130, 130, 140), h=1.6, glasses=True)
    # parked cyclist + runner
    cyclist(c, 200, 600, (220, 70, 70), (60, 110, 200) if "bike" not in d else (250, 190, 50), s=1.2)
    modern(c, 820, 600, (90, 160, 220), bottom=(40, 40, 50), hair=(90, 60, 40), h=2.2, style="long")
    # path sign
    flat(c, Thick(300, 600, 300, 540, 3), (90, 96, 110))
    piece(c, Circ(300, 528, 16), (60, 120, 210) if "sign" not in d else (220, 70, 70), border=1.2, shadow=SMALL)
    flat(c, [Circ(294, 532, 5), Circ(308, 532, 5)], (250, 250, 250))


L568_ELEMENTS = [
    E("rider1", lambda c, m: cyclist(c, 0, 500, (250, 200, 60), (40, 40, 50), s=1.0), anim=dict(drift_across(-50, 50, 60, start=300))),
    E("rider2", lambda c, m: cyclist(c, 0, 530, (120, 200, 160), (220, 70, 70), s=1.1, hair=(220, 180, 90)), anim=dict(drift_across(-55, 55, -50, start=600))),
    E("boat", lambda c, m: (piece(c, Poly([(0, 260), (60, 260), (52, 272), (8, 272)]), (250, 250, 250), border=1, shadow=SMALL)),
      anim=dict(drift_across(0, 60, 16, start=100))),
    bird_el("bird", 600, 60, s=8, speed=-18),
]

L568_DIFFS = [
    ("barge", 630, 315, 0),
    ("tree", 380, 400, 0),
    ("bike", 196, 560, 0),
    ("sign", 300, 528, 0),
]


# =================================================================== Level 569 rocket launch site (day / night)
DN569 = day_night(40.0, tint=(0.24, 0.26, 0.50))
SUN569, MOON569 = celestial((230, 300), (170, 240), 40.0)


def l569_bg(c, d):
    sky(c, (120, 180, 236), (240, 220, 200), 340)
    far_ridge(c, 260, 40, (180, 170, 180), 5691)
    piece(c, RRect(-10, 330, 910, 612, 0), (210, 196, 166), shadow=LAYER)
    # launch pad
    piece(c, RRect(300, 420, 600, 450, 2), (150, 150, 160), border=1.5, shadow=PROP)
    flat(c, RRect(400, 450, 500, 480, 0), (90, 90, 100))
    # service tower
    piece(c, RRect(520, 90, 560, 420, 1), (220, 70, 60), shadow=PROP)
    for y in range(96, 420, 24):
        flat(c, [Thick(520, y, 560, y + 24, 2), Thick(560, y, 520, y + 24, 2)], (190, 56, 50))
    for y in (160, 260, 360):
        piece(c, RRect(484, y, 524, y + 16, 2), (220, 70, 60) if not (y == 260 and "arm" in d) else (60, 110, 200), shadow=SMALL)
    # rocket
    piece(c, [RRect(420, 140, 480, 420, 14), Poly([(420, 146), (480, 146), (450, 70)])], (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(420, 210, 480, 226, 1), (40, 40, 50))
    flat(c, RRect(420, 330, 480, 340, 1), (40, 40, 50) if "band" not in d else (220, 70, 70))
    piece(c, [Poly([(420, 360), (420, 420), (392, 430), (396, 390)]), Poly([(480, 360), (480, 420), (508, 430), (504, 390)])], (220, 70, 60) if "fins" not in d
          else (60, 110, 200), border=1.2, shadow=SMALL)
    flat(c, Circ(450, 260, 10), (60, 90, 130))
    flat(c, RRect(436, 170, 464, 200, 2), (60, 110, 200))
    # water tower + control building
    piece(c, [Ell(140, 200, 50, 30), RRect(90, 200, 190, 230, 4)], (230, 232, 240), border=1.5, shadow=PROP)
    flat(c, [Thick(110, 230, 100, 330, 4), Thick(170, 230, 180, 330, 4)], (150, 150, 160))
    piece(c, RRect(660, 280, 900, 380, 3), (240, 240, 244), border=1.5, shadow=PROP)
    for x in range(680, 890, 44):
        flat(c, RRect(x, 300, x + 30, 330, 2), (150, 196, 226))
    flat(c, [Thick(760, 280, 760, 220, 3)], (150, 150, 160))
    piece(c, Ell(760, 220, 30, 12), (250, 250, 250) if "dish" not in d else (250, 190, 60), border=1.2, shadow=SMALL)
    # crawler road + spectators bleacher
    piece(c, RRect(-10, 480, 910, 520, 0), (180, 170, 150), shadow=SMALL)
    piece(c, RRect(20, 520, 300, 600, 3), (190, 190, 196), border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, Thick(20, 540 + k * 20, 300, 540 + k * 20, 2), (170, 170, 176))
    for k, x in enumerate(range(50, 290, 46)):
        modern(c, x, 540 + (k % 2) * 20, [(240, 120, 90), (90, 150, 220), (250, 200, 80), (120, 190, 120), (200, 110, 150), (150, 150, 170)][k], bottom=(60, 60, 80),
               hair=[(40, 30, 30), (220, 180, 90), (90, 60, 40)][k % 3], h=1.4)
    # flags
    for k, x in enumerate((640, 700, 760)):
        flat(c, Thick(x, 600, x, 520, 3), (150, 150, 160))
        piece(c, Poly([(x + 1, 520), (x + 34, 528), (x + 1, 538)]), [(220, 60, 60), (60, 110, 200), (250, 250, 250)][k], border=1, shadow=SMALL)


L569_ELEMENTS = [
    sun_element("sun", (230, 300), SUN569, r=26),
    moon_element("moon", (230, 300), MOON569, r=22),
    star_field("stars", 569, 40, 200, avoid=[(380, 40, 600, 440)]),
] + [
    E("vent%d" % i, (lambda dx: lambda c, m: soft_union(c, [Circ(450 + dx, 456, 16)], (246, 246, 250), 0.8, spread=14))(dx),
      anim=dict(driftVelocity=((-1 if dx < 0 else 1) * 30, 6), driftLength=120, driftFade=True, driftGrow=1.8, phase=i / 4))
    for i, dx in enumerate((-40, 40, -20, 20))
] + [
    window_glow("winglow", [(680 + k * 44, 300, 710 + k * 44, 330) for k in range(5)]),
    E("floodL", lambda c, m: soft_union(c, [Poly([(250, 360), (262, 360), (440, 120), (400, 110)])], (255, 250, 220), 0.2, spread=14), daynight="night"),
    E("beacon", lambda c, m: soft_union(c, [Circ(540, 84, 4)], (255, 80, 80), 0.9, spread=10), daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=1.0)),
]

L569_DIFFS = [
    ("arm", 502, 264, 0),
    ("band", 450, 335, 0),
    ("fins", 450, 400, 0),
    ("dish", 760, 220, 0),
]


LEVELS = [
    ("Level560", "剪羊毛农场", l560_bg, L560_ELEMENTS, L560_DIFFS, 60, OPTS),
    ("Level561", "伐木场", l561_bg, L561_ELEMENTS, L561_DIFFS, 60, OPTS),
    ("Level562", "盐田", l562_bg, L562_ELEMENTS, L562_DIFFS, 60, OPTS),
    ("Level563", "帆船赛", l563_bg, L563_ELEMENTS, L563_DIFFS, 60, OPTS),
    ("Level564", "直升机停机坪", l564_bg, L564_ELEMENTS, L564_DIFFS, 60, OPTS),
    ("Level565", "邮轮甲板", l565_bg, L565_ELEMENTS, L565_DIFFS, 60, OPTS),
    ("Level566", "山间缆车", l566_bg, L566_ELEMENTS, L566_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS566, blend=3.0), anim_seconds=20.0, frames=80)),
    ("Level567", "游艇码头", l567_bg, L567_ELEMENTS, L567_DIFFS, 60, OPTS),
    ("Level568", "河畔自行车道", l568_bg, L568_ELEMENTS, L568_DIFFS, 60, OPTS),
    ("Level569", "火箭发射场", l569_bg, L569_ELEMENTS, L569_DIFFS, 60, dict(OPTS, day_night=DN569, anim_seconds=40.0, frames=80)),
]
