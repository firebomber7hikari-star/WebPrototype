# -*- coding: utf-8 -*-
"""Everyday-town themes, part 3: shops and services (paper-craft, full-bleed, no real brands or logos):
  Level520 洗车场     - a car wash: tunnel with spinning brushes and foam, queue of cars, attendant drying a car
  Level521 眼镜店     - an optician: frame display wall, eye chart, mirror, optician and customer
  Level522 书店       - a bookshop: tall shelves, table stacks, reading armchair, small cafe corner
  Level523 文具店     - a stationery shop: pen racks, notebook wall, paper rolls, school bags, counter
  Level524 乐器行     - a music shop: guitar wall, upright piano, drum kit, brass on a shelf
  Level525 自行车修理铺 - a bicycle repair shop: bike on a stand, wheels on hooks, tool board, mechanic
  Level526 照相馆     - a photo studio: backdrop, softboxes, camera on a tripod, family posing
  Level527 早点铺     - a breakfast shop: bamboo steamer stacks, dumpling counter, soy-milk pot, diners
  Level528 火锅店     - a hot-pot restaurant: lanterns, tables with bubbling pots, diners, waiter
  Level529 鞋店       - a shoe shop: shoe wall, try-on bench, mirror, boxes, shoppers
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_modern import car_side
from levels_daily import bookcase

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


# =================================================================== shared helpers
def room(c, wall, stripe, floor, line, floor_y=470, step=40):
    """Back wall with soft vertical stripes and a plank floor."""
    c.rect(0, 0, W, H, wall)
    for x in range(0, W, step):
        flat(c, RRect(x, 0, x + step / 2, floor_y, 0), stripe)
    c.rect(0, floor_y, W, H, floor)
    for y in range(floor_y + 12, H, 22):
        flat(c, Thick(0, y, W, y, 1.2), line)
    piece(c, RRect(-10, floor_y - 10, 910, floor_y + 4, 0), lit(floor, 0.85), shadow=SMALL)


def wall_shelf(c, x0, x1, y, col=(170, 130, 90)):
    piece(c, RRect(x0, y, x1, y + 10, 2), col, border=1.2, shadow=PROP)


def counter(c, x0, x1, y0, y1, col, top=None):
    piece(c, RRect(x0, y0, x1, y1, 4), col, border=1.5, shadow=PROP)
    flat(c, RRect(x0, y0, x1, y0 + 12, 3), top or lit(col, 0.85))


def plant(c, x, base, s=1.0, pot=(200, 120, 90), leaf=(80, 150, 90)):
    piece(c, Poly([(x - 16 * s, base - 30 * s), (x + 16 * s, base - 30 * s), (x + 12 * s, base), (x - 12 * s, base)]), pot, border=1.2, shadow=PROP)
    piece(c, [Ell(x, base - 54 * s, 18 * s, 28 * s), Ell(x - 16 * s, base - 46 * s, 10 * s, 20 * s), Ell(x + 16 * s, base - 48 * s, 10 * s, 20 * s)],
          leaf, shadow=SMALL)


def steam_el(eid, x, y, n=3, r=6, rise=14, length=40):
    return [E("%s%d" % (eid, i), (lambda: lambda c, m: soft_union(c, [Circ(x, y, r)], (250, 250, 250), 0.7, spread=r))(),
              anim=dict(driftVelocity=(2, rise), driftLength=length, driftFade=True, driftGrow=1.6, phase=i / n)) for i in range(n)]


# =================================================================== Level 520 car wash
def l520_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 260)
    cloud_bank(c, 120, (250, 250, 246), 5201, k=0.7)
    far_skyline(c, 240, 30, 120, (186, 196, 214), 5202, win=(206, 214, 230))
    # wash building with the tunnel
    piece(c, RRect(260, 90, 760, 420, 4), (90, 150, 210), border=2, shadow=PROP)
    piece(c, RRect(250, 80, 770, 110, 4), (250, 250, 250), border=1.5, shadow=SMALL)
    for x in range(260, 760, 40):
        flat(c, Poly([(x, 110), (x + 20, 110), (x + 30, 124), (x + 10, 124)]), (250, 250, 250))
    flat(c, RRect(320, 170, 700, 420, 30), (40, 60, 90))
    flat(c, RRect(340, 186, 680, 420, 24), (70, 100, 140))
    piece(c, RRect(380, 120, 640, 156, 6), (250, 220, 60) if "sign" not in d else (240, 120, 160), border=1.5, shadow=SMALL)
    sign_box(c, 400, 128, 620, 148, (40, 60, 90), 5203, vertical=False)
    # stripes on the building side
    for k, x in enumerate((280, 720)):
        flat(c, [RRect(x, 180, x + 24, 400, 4)], (250, 250, 250) if not (k == 1 and "stripe" in d) else (250, 200, 60))
    # car in the tunnel under foam
    car_side(c, 510, 410, (220, 70, 70), s=1.5)
    flat(c, [Circ(450 + k * 22, 330 - (k % 3) * 12, 18) for k in range(8)], (250, 250, 255))
    flat(c, [Circ(470 + k * 30, 352, 12) for k in range(5)], (240, 246, 255))
    # forecourt
    piece(c, RRect(-10, 420, 910, 612, 0), (170, 170, 178), shadow=LAYER)
    for x in range(0, 900, 120):
        flat(c, Thick(x, 500, x + 60, 500, 3), (250, 250, 240))
    flat(c, [Ell(520, 440, 160, 10), Ell(300, 470, 60, 6)], (150, 170, 196))
    # queue of cars (left)
    car_side(c, 120, 560, (90, 150, 220) if "car" not in d else (250, 190, 60), s=1.4)
    # dried car + attendant (right)
    car_side(c, 760, 580, (250, 250, 250), s=1.5)
    modern(c, 860, 590, (60, 120, 200), bottom=(50, 50, 70), hair=(40, 30, 30), h=2.0)
    piece(c, RRect(838, 500, 866, 520, 3), (250, 220, 70), border=1, shadow=SMALL)
    # bucket + hose
    piece(c, Poly([(590, 600), (636, 600), (642, 556), (584, 556)]), (240, 120, 60) if "bucket" not in d else (90, 190, 120), border=1.2, shadow=PROP)
    c.ellipse_ring(613, 552, 26, 8, 3, (200, 90, 40))
    flat(c, [Thick(560, 520, 600, 560, 5), Thick(560, 520, 530, 470, 5)], (60, 140, 90))
    # price board on a pole (left)
    piece(c, [RRect(60, 330, 68, 470, 2), RRect(10, 250, 120, 336, 4)], (60, 64, 76), border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, RRect(22, 262 + k * 24, 108, 280 + k * 24, 2), [(250, 220, 60), (120, 200, 240), (240, 120, 160)][k] if not (k == 1 and "price" in d)
             else (250, 250, 250))
    # bushes along the edge
    bush(c, 200, 430, s=1.2)
    bush(c, 860, 430, s=1.3)


def brush(x):
    def d(c, m):
        flat(c, [Thick(x - 30 * math.cos(a), 300 - 30 * math.sin(a), x + 30 * math.cos(a), 300 + 30 * math.sin(a), 6) for a in
                 [k * math.pi / 6 for k in range(6)]], (60, 160, 230))
        flat(c, Circ(x, 300, 8), (40, 60, 90))
    return d


L520_ELEMENTS = [
    spin_el("brushL", brush(370), (370, 300), 160),
    spin_el("brushR", brush(650), (650, 300), -160),
    E("spray", lambda c, m: [soft_union(c, [Circ(420 + k * 34, 200, 4)], (200, 230, 255), 0.8, spread=6) for k in range(6)],
      anim=dict(bobAmplitude=(0, 6), bobSpeed=2.0, twinkle=0.3, twinkleSpeed=2.0)),
    E("drops", lambda c, m: [flat(c, Ell(430 + k * 40, 230, 2, 5), (200, 230, 255)) for k in range(5)],
      anim=dict(driftVelocity=(0, -40), driftLength=30, driftFade=True)),
    E("towel", lambda c, m: piece(c, RRect(820, 540, 852, 560, 3), (250, 120, 160), border=1, shadow=SMALL), pivot=(836, 550),
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.8)),
    bird_el("bird", 300, 40, s=8, speed=20),
]

L520_DIFFS = [
    ("sign", 510, 138, 0),
    ("stripe", 732, 290, 0),
    ("car", 120, 530, 0),
    ("bucket", 613, 578, 0),
    ("price", 65, 298, 0),
]


# =================================================================== Level 521 optician
def specs(c, x, y, col, s=1.0, lens=(200, 226, 240)):
    for dx in (-12 * s, 12 * s):
        flat(c, Circ(x + dx, y, 9 * s), lens)
        c.ellipse_ring(x + dx, y, 9 * s, 8 * s, 2.6 * s, col)
    flat(c, Thick(x - 3 * s, y - 2 * s, x + 3 * s, y - 2 * s, 2 * s), col)


def l521_bg(c, d):
    room(c, (238, 232, 222), (232, 226, 214), (200, 186, 170), (186, 172, 156))
    # frame display wall (left)
    piece(c, RRect(20, 40, 380, 420, 4), (250, 248, 242), border=2, shadow=PROP)
    cols = [(40, 40, 50), (170, 90, 60), (200, 60, 70), (60, 110, 190), (160, 120, 200), (90, 150, 110), (220, 170, 60)]
    for r in range(6):
        y = 80 + r * 56
        flat(c, Thick(30, y + 18, 370, y + 18, 3), (220, 214, 204))
        for i in range(5):
            col = cols[(r * 2 + i) % len(cols)]
            if r == 2 and i == 1 and "frame" in d:
                continue
            specs(c, 70 + i * 66, y, col)
    # eye chart (centre)
    piece(c, RRect(430, 60, 560, 260, 3), (250, 250, 250), border=1.5, shadow=PROP)
    for k in range(6):
        w = 46 - k * 6
        flat(c, RRect(495 - w, 80 + k * 28, 495 + w, 96 + k * 28 - k * 1.5, 1), (40, 40, 50) if not (k == 2 and "chart" in d) else (220, 60, 60))
    # mirror (right)
    piece(c, Ell(720, 190, 70, 110), (190, 150, 80) if "mirror" not in d else (90, 160, 200), border=2, shadow=PROP)
    flat(c, Ell(720, 190, 58, 96), (210, 230, 238))
    flat(c, Poly([(690, 120), (710, 110), (680, 220), (666, 210)]), (240, 248, 252))
    # optician behind the counter with display case
    modern(c, 640, 460, (250, 250, 250), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.6, glasses=True)
    counter(c, 420, 900, 360, 470, (190, 150, 110))
    flat(c, RRect(440, 380, 880, 440, 3), (220, 236, 240))
    for k in range(5):
        specs(c, 480 + k * 84, 410, cols[k], s=1.1)
    # waiting bench with a reader + rotating display stand
    piece(c, [RRect(560, 540, 760, 556, 4), RRect(570, 556, 580, 596, 2), RRect(740, 556, 750, 596, 2)], (110, 140, 170), border=1.2, shadow=PROP)
    modern(c, 640, 550, (200, 110, 110), bottom=(50, 50, 70), hair=(130, 130, 140), h=2.0)
    piece(c, RRect(650, 470, 680, 494, 2), (240, 220, 160), border=1, shadow=SMALL)
    piece(c, [RRect(316, 450, 330, 590, 3), Ell(323, 592, 30, 6), RRect(290, 440, 356, 456, 3)], (220, 214, 204), border=1.2, shadow=PROP)
    for k in range(3):
        specs(c, 323, 478 + k * 34, cols[k + 3], s=0.9)
    # customer on a stool trying glasses
    piece(c, [Ell(200, 520, 40, 10), RRect(194, 520, 206, 590, 2), Ell(200, 590, 26, 6)], (200, 60, 60) if "stool" not in d else (60, 120, 200),
          border=1.2, shadow=PROP)
    modern(c, 200, 520, (120, 170, 120) if "shirt" not in d else (240, 150, 90), bottom=(60, 70, 110), hair=(220, 180, 90), h=2.2, style="long")
    specs(c, 205, 418, (40, 40, 50), s=0.6)
    # hand mirror on the counter
    piece(c, [Thick(800, 360, 800, 330, 4), Circ(800, 314, 18)], (220, 200, 120), border=1, shadow=SMALL)
    flat(c, Circ(800, 314, 13), (210, 230, 238))
    plant(c, 860, 600, s=1.3)
    plant(c, 470, 600, s=1.0, pot=(90, 150, 210))


L521_ELEMENTS = [
    E("glint", lambda c, m: flat(c, Poly(star_pts(740, 140, 14, 4, points=4)), (255, 255, 255)), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=0.5)),
    E("fan", lambda c, m: (flat(c, Thick(450, 0, 450, 20, 2), (90, 90, 100)),
                           flat(c, [Thick(450 - 50 * math.cos(a), 24 - 6 * math.sin(a), 450 + 50 * math.cos(a), 24 + 6 * math.sin(a), 6) for a in (0.3, 1.9)],
                                (170, 130, 90))), pivot=(450, 24), anim=dict(stretch=(0.8, 0), scaleSpeed=3.0)),
    E("tilt", lambda c, m: specs(c, 800, 500, (200, 60, 70), s=1.0), pivot=(800, 500), anim=dict(swingAngle=6, swingSpeed=0.5)),
]

L521_DIFFS = [
    ("frame", 136, 192, 0),
    ("chart", 495, 144, 0),
    ("mirror", 720, 190, 0),
    ("stool", 200, 556, 0),
    ("shirt", 200, 462, 0),
]


# =================================================================== Level 522 bookshop
def l522_bg(c, d):
    room(c, (232, 220, 200), (226, 212, 190), (170, 120, 84), (150, 104, 72))
    bookcase(c, 10, 250, 30, 460, 5221)
    bookcase(c, 650, 890, 30, 460, 5222, swap=(3, 3, 8, (250, 120, 180)) if "books" in d else None)
    # poster + window between the cases
    piece(c, RRect(300, 50, 600, 250, 4), (130, 90, 60), border=2, shadow=PROP)
    flat(c, RRect(312, 62, 588, 238, 2), (190, 220, 240))
    far_skyline(c, 236, 30, 120, (210, 216, 230), 5223, x0=312, x1=588)
    flat(c, [Thick(450, 62, 450, 238, 4), Thick(312, 150, 588, 150, 4)], (130, 90, 60))
    piece(c, RRect(320, 270, 420, 350, 3), (240, 200, 90) if "poster" not in d else (110, 190, 220), border=1.5, shadow=PROP)
    flat(c, [Circ(370, 300, 16), RRect(340, 326, 400, 336, 2)], (250, 250, 240))
    # table display with stacks
    piece(c, [RRect(280, 440, 620, 456, 3), RRect(296, 456, 308, 540, 2), RRect(592, 456, 604, 540, 2)], (120, 80, 56), border=1.5, shadow=PROP)
    rnd = random.Random(5224)
    for k, x in enumerate(range(300, 600, 60)):
        y = 440
        for j in range(rnd.randint(3, 5)):
            col = rnd.choice([(200, 70, 70), (60, 110, 180), (90, 160, 110), (230, 190, 70), (160, 110, 190)])
            if k == 2 and "stack" in d:
                col = (250, 250, 250)
            piece(c, RRect(x - 22 + rnd.uniform(-3, 3), y - 12, x + 22 + rnd.uniform(-3, 3), y, 1), col, border=0.8, shadow=SMALL)
            y -= 12
    # cafe corner (right front): mug on a small table, armchair reader
    piece(c, [Ell(560, 556, 36, 8), RRect(556, 556, 564, 600, 2)], (240, 236, 226), border=1.2, shadow=PROP)
    piece(c, [RRect(540, 530, 560, 554, 4), Thick(560, 536, 568, 544, 3)], (240, 120, 90) if "mug" not in d else (90, 170, 230), border=1, shadow=SMALL)
    chair = (90, 120, 160) if "chair" not in d else (200, 120, 60)
    piece(c, [RRect(640, 480, 780, 580, 18), RRect(626, 520, 662, 590, 12), RRect(760, 520, 796, 590, 12)], chair, border=1.5, shadow=PROP)
    modern(c, 712, 556, (230, 190, 90), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.9, style="long")
    piece(c, RRect(712, 446, 742, 470, 2), (200, 70, 70), border=1, shadow=SMALL)
    # browsing customers
    modern(c, 150, 596, (90, 150, 110), bottom=(50, 50, 70), hair=(40, 30, 30), h=2.3)
    modern(c, 380, 596, (200, 110, 150), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.1, style="twin")
    plant(c, 870, 600, s=1.2)


def lamp_el(eid, x, y0, y1, col=(90, 140, 110)):
    def d(c, m):
        flat(c, Thick(x, y0, x, y1, 1.5), (90, 80, 70))
        piece(c, Poly([(x - 22, y1 + 18), (x + 22, y1 + 18), (x + 12, y1), (x - 12, y1)]), col, border=1, shadow=SMALL)
        soft_union(c, [Ell(x, y1 + 22, 16, 6)], (255, 236, 160), 0.6, spread=10)
    return E(eid, d, pivot=(x, y0), anim=dict(swingAngle=3, swingSpeed=0.3, phase=(x % 9) / 9))


L522_ELEMENTS = [
    lamp_el("lamp1", 360, 0, 20),
    lamp_el("lamp2", 540, 0, 20),
    E("cat", lambda c, m: piece(c, [Ell(470, 428, 20, 9), Circ(490, 420, 8), Poly([(484, 416), (486, 406), (490, 414)]),
                                    Poly([(492, 414), (496, 406), (498, 418)])], (240, 170, 90), border=1, shadow=SMALL),
      pivot=(470, 436), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
] + steam_el("steam", 550, 524, r=4, rise=12, length=26)

L522_DIFFS = [
    ("books", 780, 330, 0),
    ("poster", 370, 310, 0),
    ("stack", 420, 410, 0),
    ("mug", 552, 542, 0),
    ("chair", 710, 530, 0),
]


# =================================================================== Level 523 stationery shop
def l523_bg(c, d):
    room(c, (240, 236, 226), (234, 230, 218), (210, 196, 176), (196, 182, 162))
    # notebook wall (left): grid of covers
    piece(c, RRect(20, 40, 340, 400, 4), (250, 250, 248), border=2, shadow=PROP)
    pal = [(240, 120, 120), (120, 180, 240), (250, 210, 90), (140, 200, 140), (200, 150, 220), (250, 160, 90)]
    for r in range(5):
        for i in range(5):
            col = pal[(r + i * 2) % len(pal)]
            if r == 1 and i == 3 and "note" in d:
                col = (60, 60, 70)
            x, y = 36 + i * 60, 54 + r * 68
            piece(c, RRect(x, y, x + 46, y + 58, 2), col, border=0.8, shadow=SMALL)
            flat(c, RRect(x + 8, y + 10, x + 38, y + 20, 1), (250, 250, 250))
    # pen racks (centre)
    piece(c, RRect(380, 60, 560, 300, 4), (190, 150, 110), border=1.5, shadow=PROP)
    for r in range(4):
        y = 80 + r * 56
        flat(c, RRect(390, y + 34, 550, y + 42, 1), (160, 120, 84))
        for i in range(12):
            col = pal[(i + r) % len(pal)]
            flat(c, [RRect(396 + i * 13, y, 404 + i * 13, y + 36, 2)], col)
            flat(c, Poly([(396 + i * 13, y), (404 + i * 13, y), (400 + i * 13, y - 8)]), (60, 60, 70))
    # paper rolls on the right wall
    for k in range(5):
        col = [(240, 120, 120), (120, 180, 240), (250, 210, 90), (140, 200, 140), (200, 150, 220)][k]
        if k == 3 and "roll" in d:
            col = (250, 140, 60)
        piece(c, [RRect(620 + k * 46, 60, 652 + k * 46, 250, 12)], col, border=1, shadow=SMALL)
        flat(c, Ell(636 + k * 46, 64, 14, 5), lit(col, 0.8))
    # school bags on hooks
    for k, x in enumerate((640, 740, 840)):
        flat(c, Circ(x, 280, 4), (120, 120, 130))
        col = [(220, 60, 70), (60, 110, 200), (250, 190, 60)][k] if not (k == 1 and "bag" in d) else (120, 190, 110)
        piece(c, [RRect(x - 30, 290, x + 30, 370, 12)], col, border=1.5, shadow=PROP)
        flat(c, RRect(x - 20, 330, x + 20, 360, 6), lit(col, 0.85))
        flat(c, Thick(x - 20, 290, x, 280, 3), lit(col, 0.7))
    # counter + shopkeeper
    counter(c, 360, 640, 400, 500, (120, 170, 200))
    modern(c, 500, 400, (240, 200, 90), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.0, style="long")
    piece(c, RRect(400, 384, 440, 404, 3), (60, 64, 76), border=1, shadow=SMALL)
    piece(c, [RRect(580, 370, 610, 400, 3)], (240, 120, 90) if "cup" not in d else (120, 120, 220), border=1, shadow=SMALL)
    flat(c, [Thick(586 + k * 6, 370, 584 + k * 7, 346, 3) for k in range(4)], (60, 60, 70))
    # shoppers + a desk globe
    modern(c, 170, 596, (90, 150, 220), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.2, bag=(240, 120, 60))
    modern(c, 260, 600, (240, 160, 180), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.5, style="twin")
    modern(c, 780, 596, (130, 130, 150), bottom=(50, 50, 60), hair=(240, 240, 246), h=2.2, glasses=True)
    piece(c, [Circ(870, 520, 24), RRect(866, 544, 874, 580, 2), Ell(870, 582, 18, 5)], (90, 160, 220) if "globe" not in d else (240, 170, 80),
          border=1.2, shadow=PROP)
    flat(c, [Ell(862, 512, 10, 7), Ell(878, 530, 8, 5)], (120, 190, 110))


L523_ELEMENTS = [
    E("mobile", lambda c, m: (flat(c, Thick(300, 0, 300, 30, 1.2), (100, 100, 110)),
                              flat(c, Thick(250, 30, 350, 30, 2), (100, 100, 110)),
                              [piece(c, Poly(star_pts(x, 52, 12, 5)), col, border=1, shadow=SMALL) for x, col in
                               ((250, (250, 200, 60)), (300, (240, 120, 160)), (350, (120, 200, 240)))]),
      pivot=(300, 0), anim=dict(swingAngle=6, swingSpeed=0.3)),
    E("plane", lambda c, m: piece(c, Poly([(0, 20), (30, 26), (0, 32), (6, 26)]), (250, 250, 250), border=1, shadow=SMALL),
      anim=dict(drift_across(0, 30, 50, start=100), bobAmplitude=(0, 10), bobSpeed=0.5)),
    E("pencil", lambda c, m: (flat(c, Thick(230, 480, 230, 440, 4), (250, 200, 60)), flat(c, Poly([(228, 480), (232, 480), (230, 488)]), (60, 60, 70))),
      pivot=(230, 470), anim=dict(swingAngle=10, swingSpeed=1.0)),
]

L523_DIFFS = [
    ("note", 239, 150, 0),
    ("roll", 774, 156, 0),
    ("bag", 740, 330, 0),
    ("cup", 595, 385, 0),
    ("globe", 870, 520, 0),
]


# =================================================================== Level 524 music shop
def guitar(c, x, y, col, s=1.0, neck=(120, 80, 50)):
    piece(c, [Thick(x, y, x, y - 110 * s, 7 * s), RRect(x - 8 * s, y - 130 * s, x + 8 * s, y - 108 * s, 3)], neck, border=1, shadow=SMALL)
    piece(c, [Ell(x, y + 34 * s, 30 * s, 26 * s), Ell(x, y - 4 * s, 22 * s, 20 * s)], col, border=1.2, shadow=PROP)
    flat(c, Circ(x, y + 14 * s, 8 * s), (40, 30, 30))
    flat(c, RRect(x - 12 * s, y + 44 * s, x + 12 * s, y + 50 * s, 2), (40, 30, 30))


def l524_bg(c, d):
    room(c, (60, 70, 90), (66, 76, 98), (150, 110, 80), (134, 96, 68))
    # guitar wall
    for k, (x, col) in enumerate(((80, (220, 120, 50)), (170, (40, 40, 50)), (260, (200, 60, 70)), (350, (240, 220, 180)), (440, (60, 120, 200)))):
        if k == 2 and "guitar" in d:
            col = (120, 200, 120)
        flat(c, Circ(x, 54, 4), (200, 200, 210))
        guitar(c, x, 190, col)
    # upright piano (right)
    piece(c, RRect(560, 230, 860, 460, 6), (40, 30, 30), border=2, border_col=(120, 100, 90), shadow=PROP)
    flat(c, RRect(560, 330, 860, 350, 2), (60, 50, 50))
    for k in range(22):
        flat(c, RRect(566 + k * 13.4, 352, 577 + k * 13.4, 400, 1), (250, 250, 246))
    for k in range(21):
        if k % 7 not in (2, 6):
            flat(c, RRect(575 + k * 13.4, 352, 582 + k * 13.4, 382, 1), (30, 30, 34))
    piece(c, [RRect(640, 470, 780, 486, 3), RRect(650, 486, 660, 540, 2), RRect(760, 486, 770, 540, 2)],
          (40, 30, 30) if "bench" not in d else (180, 60, 60), border=1.2, border_col=(120, 100, 90), shadow=PROP)
    # sheet music + metronome on the piano
    piece(c, RRect(660, 254, 760, 320, 2), (250, 248, 236), border=1, shadow=SMALL)
    for k in range(4):
        flat(c, Thick(670, 270 + k * 12, 750, 270 + k * 12, 1), (90, 90, 100))
    piece(c, Poly([(800, 330), (840, 330), (828, 270), (812, 270)]), (150, 100, 60), border=1, shadow=SMALL)
    # brass shelf
    wall_shelf(c, 560, 860, 150)
    if "trumpet" not in d:
        piece(c, [Thick(590, 136, 660, 136, 6), Poly([(656, 120), (690, 112), (690, 160), (656, 152)]), RRect(606, 124, 640, 132, 2)],
              (240, 200, 70), border=1, shadow=SMALL)
    piece(c, [Ell(770, 120, 20, 30), Thick(770, 90, 770, 60, 4)], (180, 110, 60), border=1, shadow=SMALL)       # violin
    flat(c, Thick(800, 140, 830, 60, 2), (120, 90, 60))
    # drum kit (front left)
    piece(c, [Ell(160, 520, 60, 46)], (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, Ell(160, 520, 50, 38), (60, 110, 200) if "drum" not in d else (220, 60, 70))
    for x in (90, 236):
        piece(c, [Ell(x, 470, 30, 10), RRect(x - 30, 470, x + 30, 500, 3)], (250, 250, 250), border=1.2, shadow=PROP)
        flat(c, Thick(x, 500, x, 590, 3), (180, 180, 190))
    flat(c, [Thick(60, 400, 60, 590, 3)], (180, 180, 190))
    flat(c, Ell(60, 400, 40, 6), (230, 200, 80))
    # record shelf under the guitars
    wall_shelf(c, 30, 520, 360)
    rnd = random.Random(5241)
    for k in range(14):
        x = 40 + k * 34
        col = rnd.choice([(220, 70, 70), (60, 110, 200), (240, 200, 70), (40, 40, 50), (240, 240, 230), (120, 180, 120)])
        piece(c, RRect(x, 316, x + 30, 360, 1), col, border=0.8, shadow=SMALL)
        flat(c, Circ(x + 15, 338, 9), lit(col, 0.7))
    # amp + shopkeeper + customer
    piece(c, RRect(420, 480, 520, 580, 4), (40, 40, 46), border=1.5, border_col=(120, 120, 130), shadow=PROP)
    flat(c, RRect(430, 500, 510, 570, 3), (70, 70, 80))
    flat(c, [Circ(440 + k * 12, 490, 3) for k in range(6)], (250, 220, 120))
    modern(c, 340, 596, (200, 90, 90), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3)
    guitar(c, 352, 470, (240, 220, 180), s=0.8)
    modern(c, 850, 596, (90, 150, 110), bottom=(50, 50, 60), hair=(220, 180, 90), h=2.2, style="long")
    # poster
    piece(c, RRect(480, 70, 540, 160, 2), (250, 200, 60) if "poster" not in d else (240, 120, 200), border=1.2, shadow=PROP)
    flat(c, [Circ(510, 100, 14), Thick(510, 114, 510, 146, 3)], (40, 40, 50))


L524_ELEMENTS = [
    E("notes", lambda c, m: [flat(c, [Circ(460 + k * 22, 450 - k * 14, 5), Thick(464 + k * 22, 450 - k * 14, 464 + k * 22, 430 - k * 14, 2)], (250, 220, 120))
                             for k in range(3)],
      daynight="untinted", anim=dict(driftVelocity=(10, 20), driftLength=50, driftFade=True)),
    E("pend", lambda c, m: flat(c, Thick(820, 326, 820, 280, 2), (240, 220, 160)), pivot=(820, 326), anim=dict(swingAngle=20, swingSpeed=1.2)),
    E("spot", lambda c, m: soft_union(c, [Ell(260, 230, 200, 40)], (255, 240, 200), 0.18, spread=24), anim=dict(twinkle=0.2, twinkleSpeed=0.4)),
]

L524_DIFFS = [
    ("guitar", 260, 200, 0),
    ("bench", 710, 500, 0),
    ("trumpet", 640, 136, 0),
    ("drum", 160, 520, 0),
    ("poster", 510, 115, 0),
]


# =================================================================== Level 525 bicycle repair shop
def bike(c, x, base, col, s=1.0):
    for wx in (x - 40 * s, x + 40 * s):
        c.ellipse_ring(wx, base - 26 * s, 26 * s, 26 * s, 4 * s, (40, 40, 46))
        flat(c, [Thick(wx - 24 * s, base - 26 * s, wx + 24 * s, base - 26 * s, 1), Thick(wx, base - 50 * s, wx, base - 2 * s, 1)], (170, 170, 180))
    flat(c, [Thick(x - 40 * s, base - 26 * s, x - 6 * s, base - 70 * s, 4 * s), Thick(x - 6 * s, base - 70 * s, x + 30 * s, base - 70 * s, 4 * s),
             Thick(x + 30 * s, base - 70 * s, x + 40 * s, base - 26 * s, 4 * s), Thick(x - 6 * s, base - 70 * s, x, base - 26 * s, 4 * s),
             Thick(x, base - 26 * s, x - 40 * s, base - 26 * s, 4 * s), Thick(x + 30 * s, base - 70 * s, x + 32 * s, base - 82 * s, 4 * s)], col)
    flat(c, [Thick(x + 24 * s, base - 82 * s, x + 42 * s, base - 82 * s, 4 * s), Ell(x - 6 * s, base - 76 * s, 10 * s, 4 * s)], (40, 40, 46))


def l525_bg(c, d):
    room(c, (220, 214, 200), (212, 206, 192), (150, 150, 156), (136, 136, 142))
    # roller door frame + street outside (right)
    piece(c, RRect(560, 40, 900, 470, 2), (90, 96, 110), shadow=PROP)
    flat(c, RRect(574, 54, 900, 470, 0), (180, 210, 236))
    far_skyline(c, 360, 60, 200, (200, 208, 224), 5251, x0=574, x1=900)
    c.rect(574, 360, 900, 470, (180, 180, 186))
    tree_round(c, 700, 380, s=1.4)
    for y in range(54, 110, 12):
        flat(c, Thick(574, y, 900, y, 2), (120, 126, 140))
    # tool board (left)
    piece(c, RRect(30, 60, 330, 260, 3), (210, 170, 120), border=1.5, shadow=PROP)
    for x in range(40, 330, 16):
        for y in range(70, 256, 16):
            flat(c, Circ(x, y, 1.6), (180, 140, 96))
    tools = [(70, (150, 150, 160)), (110, (220, 60, 60)), (150, (150, 150, 160)), (190, (60, 110, 200)), (230, (150, 150, 160)), (270, (250, 190, 60))]
    for k, (x, col) in enumerate(tools):
        if k == 3 and "tool" in d:
            col = (90, 180, 110)
        flat(c, [Thick(x, 90, x, 200, 6), Circ(x, 86, 9)], col)
        flat(c, Circ(x, 86, 4), (210, 170, 120))
    # wheels on hooks
    for k, x in enumerate((380, 470)):
        if k == 1 and "wheel" in d:
            continue
        flat(c, Circ(x, 60, 4), (120, 120, 130))
        c.ellipse_ring(x, 120, 44, 44, 6, (40, 40, 46))
        flat(c, [Thick(x - 40 * math.cos(a), 120 - 40 * math.sin(a), x + 40 * math.cos(a), 120 + 40 * math.sin(a), 1) for a in
                 [j * math.pi / 6 for j in range(6)]], (170, 170, 180))
    # bike on the repair stand (centre)
    flat(c, [Thick(300, 470, 330, 340, 5), Thick(360, 470, 330, 340, 5), Thick(330, 340, 350, 320, 5)], (90, 96, 110))
    bike(c, 380, 400, (230, 70, 70) if "frame" not in d else (60, 160, 200), s=1.4)
    # mechanic + tire pump + helmet
    modern(c, 210, 500, (60, 100, 150), bottom=(60, 70, 90), hair=(40, 30, 30), h=2.2)
    flat(c, RRect(194, 420, 228, 470, 3), (90, 130, 170))
    piece(c, [RRect(110, 470, 124, 590, 3), RRect(90, 586, 144, 596, 2), Thick(110, 480, 80, 470, 3)], (230, 190, 60), border=1, shadow=PROP)
    piece(c, [Ell(500, 560, 34, 22), RRect(466, 560, 534, 568, 2)], (250, 120, 50) if "helmet" not in d else (120, 120, 220), border=1.2, shadow=PROP)
    flat(c, [Thick(484, 546, 516, 546, 3)], (250, 250, 250))
    # parked bikes for sale
    bike(c, 680, 590, (60, 120, 200), s=1.2)
    bike(c, 830, 594, (250, 200, 60), s=1.2)
    # oil can on a stool
    piece(c, [RRect(560, 540, 610, 552, 3), RRect(566, 552, 574, 600, 2), RRect(596, 552, 604, 600, 2)], (150, 110, 80), shadow=PROP)
    piece(c, [RRect(570, 508, 600, 540, 4), Thick(598, 516, 616, 500, 3)], (220, 60, 60), border=1, shadow=SMALL)
    # sign over the door
    piece(c, RRect(620, 8, 860, 36, 4), (250, 200, 60) if "sign" not in d else (120, 200, 240), border=1.5, shadow=SMALL)
    sign_box(c, 640, 14, 840, 30, (60, 60, 70), 5252, vertical=False)


L525_ELEMENTS = [
    spin_el("spin", lambda c, m: (c.ellipse_ring(436, 374, 37, 37, 5, (40, 40, 46)),
                                  flat(c, [Thick(436 - 34 * math.cos(a), 374 - 34 * math.sin(a), 436 + 34 * math.cos(a), 374 + 34 * math.sin(a), 1.2)
                                           for a in [j * math.pi / 6 for j in range(6)]], (200, 200, 210))), (436, 374), 120),
    E("rider", lambda c, m: (bike(c, 0, 450, (240, 120, 160), s=0.9), modern(c, 2, 400, (250, 250, 250), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.2)),
      anim=dict(driftVelocity=(40, 0), driftStart=610, driftLength=340)),
    bird_el("bird", 760, 120, s=7, speed=-16),
]

L525_DIFFS = [
    ("tool", 190, 140, 0),
    ("wheel", 470, 120, 0),
    ("frame", 380, 350, 0),
    ("helmet", 500, 556, 0),
    ("sign", 740, 22, 0),
]


# =================================================================== Level 526 photo studio
def softbox(c, x, base, col=(250, 250, 250), frame=(60, 60, 70)):
    flat(c, [Thick(x, base, x, base - 150, 3), Thick(x - 24, base, x, base - 40, 3), Thick(x + 24, base, x, base - 40, 3)], frame)
    piece(c, Poly([(x - 40, base - 220), (x + 40, base - 220), (x + 24, base - 150), (x - 24, base - 150)]), frame, border=1.2, shadow=PROP)
    flat(c, Poly([(x - 34, base - 214), (x + 34, base - 214), (x + 20, base - 156), (x - 20, base - 156)]), col)


def l526_bg(c, d):
    room(c, (200, 196, 190), (194, 190, 184), (110, 100, 96), (100, 90, 86))
    # paper backdrop roll
    piece(c, RRect(180, 20, 720, 40, 8), (90, 90, 100), shadow=PROP)
    back = (150, 190, 220)
    piece(c, Poly([(200, 40), (700, 40), (700, 470), (720, 540), (180, 540), (200, 470)]), back, shadow=LAYER)
    # posing family on a bench
    piece(c, [RRect(300, 460, 600, 480, 4), RRect(310, 480, 322, 530, 2), RRect(578, 480, 590, 530, 2)], (150, 110, 80), border=1.2, shadow=PROP)
    modern(c, 350, 470, (60, 90, 150), bottom=(40, 40, 60), hair=(40, 30, 30), h=2.4)
    modern(c, 450, 470, (230, 120, 140) if "dress" not in d else (120, 200, 160), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.3, style="long")
    modern(c, 540, 476, (250, 210, 80), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.6, style="twin")
    modern(c, 400, 530, (120, 190, 120), bottom=(60, 70, 110), hair=(40, 30, 30), h=1.4)
    piece(c, [Circ(500, 356, 20), Poly([(488, 372), (512, 372), (500, 396)])], (250, 120, 160) if "balloon" not in d else (250, 210, 70), border=1,
          shadow=SMALL)      # balloon prop
    flat(c, Thick(500, 396, 476, 430, 1.2), (90, 90, 100))
    # softboxes
    softbox(c, 110, 560)
    softbox(c, 790, 560, frame=(60, 60, 70) if "light" not in d else (200, 60, 70))
    # camera on a tripod (front centre)
    flat(c, [Thick(640, 600, 680, 520, 4), Thick(720, 600, 680, 520, 4), Thick(680, 600, 680, 520, 4)], (40, 40, 46))
    piece(c, [RRect(650, 480, 716, 522, 6), RRect(664, 470, 690, 482, 3)], (40, 40, 46), border=1.2, border_col=(120, 120, 130), shadow=PROP)
    flat(c, Circ(650, 500, 14), (90, 90, 100))
    flat(c, Circ(650, 500, 8), (140, 180, 220))
    modern(c, 760, 600, (230, 200, 160), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.2, glasses=True)
    # framed sample photos on the side walls
    for k, (x, y) in enumerate(((20, 60), (20, 200), (760, 40))):
        piece(c, RRect(x, y, x + 120, y + 100, 3), (190, 150, 80) if not (k == 1 and "frame" in d) else (60, 60, 70), border=1.5, shadow=PROP)
        flat(c, RRect(x + 8, y + 8, x + 112, y + 92, 2), [(200, 220, 236), (240, 220, 200), (210, 230, 210)][k])
        flat(c, [Circ(x + 40, y + 50, 12), Circ(x + 74, y + 54, 12)], (150, 110, 90))
    # props basket
    piece(c, Poly([(40, 600), (130, 600), (140, 540), (30, 540)]), (200, 160, 100), border=1.2, shadow=PROP)
    flat(c, [Circ(60, 534, 12), Circ(90, 528, 14), Circ(118, 536, 10)], (250, 200, 60) if "props" not in d else (200, 120, 220))


L526_ELEMENTS = [
    E("flash", lambda c, m: soft_union(c, [Circ(650, 500, 10)], (255, 255, 240), 0.9, spread=40), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=0.25)),
    E("bubble", lambda c, m: (piece(c, Circ(560, 380, 10), (240, 200, 240), border=1, shadow=SMALL)), pivot=(560, 380),
      anim=dict(bobAmplitude=(8, 12), bobSpeed=0.3)),
    E("fan", lambda c, m: (piece(c, Circ(850, 470, 30), (220, 226, 236), border=1.2, shadow=SMALL),
                           flat(c, [Thick(850 - 26 * math.cos(a), 470 - 26 * math.sin(a), 850 + 26 * math.cos(a), 470 + 26 * math.sin(a), 8)
                                    for a in (0.2, 1.25, 2.3)], (150, 160, 180))), pivot=(850, 470), anim=dict(rotateSpeed=300)),
]

L526_DIFFS = [
    ("balloon", 500, 360, 0),
    ("dress", 452, 400, 0),
    ("light", 790, 380, 0),
    ("frame", 80, 250, 0),
    ("props", 89, 530, 0),
]


# =================================================================== Level 527 breakfast shop
def steamer(c, x, base, n=3, col=(220, 190, 130)):
    for k in range(n):
        y = base - k * 26
        piece(c, RRect(x - 40, y - 26, x + 40, y, 6), col, border=1.2, shadow=SMALL)
        flat(c, Thick(x - 40, y - 13, x + 40, y - 13, 1.6), lit(col, 0.85))
    piece(c, Poly([(x - 40, base - n * 26), (x + 40, base - n * 26), (x + 26, base - n * 26 - 16), (x - 26, base - n * 26 - 16)]), lit(col, 0.92),
          border=1.2, shadow=SMALL)


def l527_bg(c, d):
    room(c, (246, 236, 214), (240, 228, 204), (180, 150, 120), (166, 136, 108))
    # menu boards across the top
    for k in range(4):
        x = 40 + k * 215
        col = (200, 50, 50) if not (k == 2 and "menu" in d) else (60, 110, 180)
        piece(c, RRect(x, 30, x + 190, 110, 4), col, border=1.5, shadow=PROP)
        for j in range(3):
            sign_box(c, x + 16, 42 + j * 22, x + 140, 56 + j * 22, (250, 240, 200), 5271 + k * 3 + j, vertical=False)
            flat(c, RRect(x + 150, 42 + j * 22, x + 176, 56 + j * 22, 2), (250, 220, 90))
    # cook making dumplings (behind the counter)
    modern(c, 520, 396, (250, 250, 250), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.8)
    piece(c, [RRect(502, 238, 542, 258, 6), Circ(510, 240, 11), Circ(532, 238, 11)], (250, 250, 250), border=1, shadow=SMALL)
    # kitchen counter with steamers + soy milk pot
    counter(c, 20, 560, 300, 420, (200, 200, 206), top=(170, 170, 180))
    steamer(c, 90, 300, 4)
    steamer(c, 190, 300, 3)
    steamer(c, 290, 300, 5 if "stack" not in d else 3)
    piece(c, [RRect(380, 230, 470, 300, 8), Ell(425, 230, 45, 10)], (180, 180, 190), border=1.5, shadow=PROP)
    flat(c, Ell(425, 232, 38, 7), (250, 246, 232))
    flat(c, Thick(470, 250, 494, 240, 4), (60, 60, 70))
    # tray of dumplings on the counter
    piece(c, RRect(470, 286, 560, 300, 3), (150, 110, 80), shadow=SMALL)
    flat(c, [Ell(482 + k * 14, 282, 7, 5) for k in range(6)], (250, 246, 232))
    # lanterns on the wall
    for k, x in enumerate((640, 760, 860)):
        flat(c, Thick(x, 120, x, 140, 1.4), (90, 80, 70))
        piece(c, Ell(x, 166, 26, 28), (220, 50, 50) if not (k == 1 and "lantern" in d) else (250, 200, 60), border=1.2, shadow=PROP)
        flat(c, [RRect(x - 18, 136, x + 18, 142, 2), RRect(x - 18, 190, x + 18, 196, 2)], (240, 200, 80))
    # tables with diners
    for k, x in enumerate((640, 820)):
        piece(c, [RRect(x - 70, 420, x + 70, 434, 3), RRect(x - 60, 434, x - 52, 520, 2), RRect(x + 52, 434, x + 60, 520, 2)], (180, 130, 90),
              border=1.2, shadow=PROP)
        piece(c, [Ell(x - 20, 412, 18, 6), RRect(x - 36, 400, x - 4, 414, 4)], (250, 250, 250), border=1, shadow=SMALL)
        piece(c, RRect(x + 10, 388, x + 34, 418, 4), (250, 250, 240) if not (k == 0 and "cup" in d) else (90, 170, 230), border=1, shadow=SMALL)
    modern(c, 600, 540, (90, 150, 220), bottom=(50, 60, 90), hair=(40, 30, 30), h=2.0)
    modern(c, 860, 540, (240, 160, 90) if "diner" not in d else (150, 110, 200), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.0, style="long")
    # stools + customers queueing
    for x in (150, 260):
        piece(c, [Ell(x, 520, 24, 6), RRect(x - 4, 520, x + 4, 580, 2)], (200, 60, 60) if not (x == 260 and "stool" in d) else (60, 120, 200),
              border=1, shadow=PROP)
    modern(c, 120, 600, (120, 170, 120), bottom=(60, 60, 80), hair=(130, 130, 140), h=2.3, glasses=True)
    modern(c, 340, 600, (200, 110, 150), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.1, bag=(240, 200, 90))


L527_ELEMENTS = steam_el("st1", 90, 180, n=3, r=8, rise=18, length=60) + steam_el("st2", 290, 150, n=3, r=8, rise=18, length=60) + [
    E("ladle", lambda c, m: (flat(c, Thick(425, 210, 440, 160, 3), (150, 150, 160)), piece(c, Ell(424, 214, 10, 5), (150, 150, 160), shadow=None)),
      pivot=(440, 160), anim=dict(swingAngle=14, swingSpeed=0.6)),
    E("cat", lambda c, m: piece(c, [Ell(420, 590, 22, 10), Circ(442, 580, 9), Poly([(436, 574), (438, 564), (442, 572)]),
                                    Poly([(444, 572), (448, 564), (450, 576)])], (90, 80, 80), border=1, shadow=SMALL),
      pivot=(420, 598), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
]

L527_DIFFS = [
    ("menu", 525, 70, 0),
    ("stack", 290, 220, 0),
    ("lantern", 760, 166, 0),
    ("cup", 662, 404, 0),
    ("stool", 260, 540, 0),
    ("diner", 861, 497, 0),
]


# =================================================================== Level 528 hot-pot restaurant
def hotpot(c, x, y, broth=(220, 60, 40), half=None):
    piece(c, [Ell(x, y, 54, 16), RRect(x - 54, y, x + 54, y + 22, 8)], (190, 190, 200), border=1.5, shadow=PROP)
    flat(c, Ell(x, y, 46, 12), broth)
    if half:
        flat(c, Poly([(x, y - 12), (x + 46, y - 4), (x + 46, y + 4), (x, y + 12)]), half)
        flat(c, Thick(x, y - 12, x, y + 12, 3), (190, 190, 200))
    flat(c, [Circ(x - 20, y - 2, 4), Circ(x + 10, y + 4, 3), Circ(x - 6, y - 6, 3)], (250, 220, 120))


def l528_bg(c, d):
    room(c, (120, 40, 40), (130, 46, 46), (90, 60, 50), (80, 52, 44))
    # wooden lattice windows
    for k, x in enumerate((60, 340, 620)):
        piece(c, RRect(x, 50, x + 220, 200, 4), (150, 100, 60), border=1.5, shadow=PROP)
        flat(c, RRect(x + 10, 60, x + 210, 190, 2), (250, 220, 160) if not (k == 0 and "window" in d) else (170, 220, 200))
        for gx in range(x + 30, x + 210, 30):
            flat(c, Thick(gx, 60, gx, 190, 3), (150, 100, 60))
        for gy in range(80, 190, 30):
            flat(c, Thick(x + 10, gy, x + 210, gy, 3), (150, 100, 60))
    # calligraphy scroll
    piece(c, RRect(296, 210, 330, 330, 2), (240, 230, 200) if "scroll" not in d else (250, 200, 90), border=1, shadow=PROP)
    for k in range(4):
        flat(c, Thick(306, 226 + k * 26, 320, 238 + k * 26, 3), (40, 30, 30))
    # tables with hot pots
    for k, (x, y) in enumerate(((180, 380), (720, 380))):
        piece(c, [RRect(x - 130, y + 20, x + 130, y + 36, 3), RRect(x - 120, y + 36, x - 108, y + 140, 2), RRect(x + 108, y + 36, x + 120, y + 140, 2)],
              (60, 40, 36), border=1.2, border_col=(110, 80, 70), shadow=PROP)
        hotpot(c, x, y, half=(250, 230, 200) if k == 0 else None, broth=(220, 60, 40) if not (k == 1 and "broth" in d) else (230, 200, 120))
        for j, dx in enumerate((-100, -70, 70, 100)):
            col = [(120, 190, 90), (240, 160, 160), (250, 220, 120), (200, 100, 80)][j]
            if k == 1 and j == 2 and "plate" in d:
                col = (90, 160, 230)
            piece(c, Ell(x + dx, y + 16, 14, 5), (250, 250, 250), border=1, shadow=SMALL)
            flat(c, Ell(x + dx, y + 13, 10, 4), col)
    # diners
    for x, col, hair, style in ((80, (60, 110, 180), (40, 30, 30), "short"), (290, (240, 200, 90) if "shirt" not in d else (120, 200, 230), (90, 60, 40), "long"),
                                (620, (200, 90, 140), (40, 30, 30), "long"), (830, (90, 150, 110), (130, 130, 140), "short")):
        modern(c, x, 520, col, bottom=(40, 40, 50), hair=hair, h=2.3, style=style)
    flat(c, [Thick(110, 400, 160, 372, 2), Thick(112, 404, 162, 378, 2)], (220, 200, 160))         # chopsticks
    # waiter with a tray (centre)
    modern(c, 450, 600, (250, 250, 250), bottom=(30, 30, 40), hair=(40, 30, 30), h=2.4)
    flat(c, RRect(436, 520, 466, 560, 2), (40, 40, 50))
    piece(c, Ell(490, 470, 40, 8), (180, 180, 190), border=1, shadow=SMALL)
    flat(c, [Ell(476, 462, 10, 6), Ell(504, 462, 10, 6)], (240, 160, 160))
    # floor tiles + a wine jar
    piece(c, [Ell(870, 560, 30, 36), RRect(850, 516, 890, 528, 4)], (150, 100, 60) if "jar" not in d else (60, 110, 160), border=1.2, shadow=PROP)
    flat(c, RRect(856, 540, 884, 566, 2), (220, 60, 50))


def lantern(eid, x, y, s=1.0, col=(220, 50, 50)):
    def d(c, m):
        flat(c, Thick(x, 0, x, y - 30 * s, 1.4), (90, 80, 70))
        piece(c, Ell(x, y, 30 * s, 32 * s), col, border=1.2, shadow=SMALL)
        flat(c, [RRect(x - 20 * s, y - 36 * s, x + 20 * s, y - 28 * s, 2), RRect(x - 20 * s, y + 28 * s, x + 20 * s, y + 36 * s, 2)], (240, 200, 80))
        flat(c, [Thick(x - 6 * s, y + 36 * s, x - 6 * s, y + 56 * s, 2), Thick(x + 6 * s, y + 36 * s, x + 6 * s, y + 56 * s, 2)], (240, 200, 80))
        soft_union(c, [Circ(x, y, 22 * s)], (255, 200, 120), 0.25, spread=20)
    return E(eid, d, pivot=(x, 0), daynight="untinted", anim=dict(swingAngle=3, swingSpeed=0.3, phase=(x % 7) / 7))


L528_ELEMENTS = [lantern("lan1", 230, 250), lantern("lan2", 450, 260, s=1.2), lantern("lan3", 680, 250)] + \
    steam_el("s1", 160, 360, n=3, r=10, rise=20, length=70) + steam_el("s2", 740, 360, n=3, r=10, rise=20, length=70)

L528_DIFFS = [
    ("window", 170, 125, 0),
    ("scroll", 313, 270, 0),
    ("shirt", 291, 470, 0),
    ("broth", 720, 380, 0),
    ("plate", 790, 393, 0),
    ("jar", 870, 552, 0),
]


# =================================================================== Level 529 shoe shop
def shoe(c, x, y, col, s=1.0, sole=(250, 250, 250)):
    piece(c, [Poly([(x - 22 * s, y), (x - 22 * s, y - 16 * s), (x - 8 * s, y - 20 * s), (x + 4 * s, y - 10 * s), (x + 22 * s, y - 6 * s), (x + 24 * s, y)])],
          col, border=1, shadow=SMALL)
    flat(c, RRect(x - 23 * s, y - 3 * s, x + 25 * s, y + 1 * s, 1), sole)


def l529_bg(c, d):
    room(c, (234, 226, 236), (228, 220, 232), (190, 170, 150), (176, 156, 136))
    # shoe wall (left & centre)
    rnd = random.Random(5291)
    pal = [(220, 70, 70), (60, 110, 200), (40, 40, 50), (250, 200, 60), (250, 250, 250), (150, 100, 70), (240, 140, 180), (90, 170, 120)]
    for r in range(5):
        y = 100 + r * 64
        wall_shelf(c, 20, 560, y)
        for i in range(8):
            col = rnd.choice(pal)
            if r == 2 and i == 5 and "shoe" in d:
                col = (160, 110, 230)
            shoe(c, 54 + i * 66, y, col)
    # mirror (right) + poster
    piece(c, RRect(620, 60, 720, 360, 6), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(630, 70, 710, 350, 4), (210, 230, 238))
    flat(c, Poly([(650, 90), (670, 90), (640, 200), (636, 180)]), (240, 248, 252))
    piece(c, RRect(760, 80, 880, 240, 3), (240, 120, 90) if "poster" not in d else (110, 180, 230), border=1.5, shadow=PROP)
    shoe(c, 820, 180, (250, 250, 250), s=2.0, sole=(60, 60, 70))
    # try-on bench + customer
    modern(c, 640, 520, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.2, style="long")
    piece(c, [RRect(560, 470, 820, 500, 6), RRect(570, 500, 580, 560, 2), RRect(800, 500, 810, 560, 2)], (90, 140, 160) if "bench" not in d else (200, 100, 120),
          border=1.5, shadow=PROP)
    shoe(c, 700, 560, (220, 70, 70), s=1.2)
    shoe(c, 746, 560, (220, 70, 70), s=1.2)
    # boxes stacked
    for k, (x, y, col) in enumerate(((80, 600, (240, 200, 160)), (80, 566, (90, 150, 220)), (160, 600, (240, 120, 120)), (120, 532, (250, 250, 250)))):
        if k == 1 and "box" in d:
            col = (250, 200, 60)
        piece(c, RRect(x - 36, y - 34, x + 36, y, 2), col, border=1.2, shadow=PROP)
        flat(c, RRect(x - 36, y - 34, x + 36, y - 26, 1), lit(col, 0.85))
    # shop assistant + shopper
    modern(c, 320, 600, (60, 60, 70), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3)
    piece(c, RRect(330, 540, 370, 566, 2), (240, 200, 160), border=1, shadow=SMALL)
    modern(c, 470, 600, (120, 190, 160), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.2, bag=(240, 120, 160))
    # plant + rug
    piece(c, Ell(690, 590, 160, 14), (200, 170, 200) if "rug" not in d else (150, 200, 170), shadow=SMALL)
    plant(c, 870, 600, s=1.3)


L529_ELEMENTS = [
    E("ceilingfan", lambda c, m: (flat(c, Thick(450, 0, 450, 22, 2), (90, 90, 100)),
                                  flat(c, [Thick(450 - 60 * math.cos(a), 26 - 6 * math.sin(a), 450 + 60 * math.cos(a), 26 + 6 * math.sin(a), 6) for a in (0.3, 1.9)],
                                       (170, 130, 90))), pivot=(450, 26), anim=dict(stretch=(0.8, 0), scaleSpeed=3.0)),
    E("tap", lambda c, m: shoe(c, 700, 560, (220, 70, 70), s=1.2), pivot=(680, 560), anim=dict(swingAngle=6, swingSpeed=1.0)),
    E("glint", lambda c, m: flat(c, Poly(star_pts(690, 110, 12, 3, points=4)), (255, 255, 255)), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=0.5)),
]

L529_DIFFS = [
    ("shoe", 384, 220, 0),
    ("poster", 820, 160, 0),
    ("bench", 690, 485, 0),
    ("box", 80, 549, 0),
    ("rug", 690, 590, 0),
]


LEVELS = [
    ("Level520", "洗车场", l520_bg, L520_ELEMENTS, L520_DIFFS, 60, OPTS),
    ("Level521", "眼镜店", l521_bg, L521_ELEMENTS, L521_DIFFS, 60, OPTS),
    ("Level522", "书店", l522_bg, L522_ELEMENTS, L522_DIFFS, 60, OPTS),
    ("Level523", "文具店", l523_bg, L523_ELEMENTS, L523_DIFFS, 60, OPTS),
    ("Level524", "乐器行", l524_bg, L524_ELEMENTS, L524_DIFFS, 60, OPTS),
    ("Level525", "自行车修理铺", l525_bg, L525_ELEMENTS, L525_DIFFS, 60, OPTS),
    ("Level526", "照相馆", l526_bg, L526_ELEMENTS, L526_DIFFS, 60, OPTS),
    ("Level527", "早点铺", l527_bg, L527_ELEMENTS, L527_DIFFS, 60, OPTS),
    ("Level528", "火锅店", l528_bg, L528_ELEMENTS, L528_DIFFS, 60, OPTS),
    ("Level529", "鞋店", l529_bg, L529_ELEMENTS, L529_DIFFS, 60, OPTS),
]
