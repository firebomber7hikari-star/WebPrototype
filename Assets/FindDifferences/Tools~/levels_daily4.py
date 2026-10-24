# -*- coding: utf-8 -*-
"""Everyday-town themes, part 4: the city outdoors (paper-craft side views, full-bleed, no real brands or logos):
  Level530 公交总站   - a bus terminal: shelters, parked buses, departures board, waiting passengers
  Level531 喷泉广场   - a city square: fountain with jets, clock tower, pigeons, flower beds, benches
  Level532 摩天楼擦窗 - window cleaners on a skyscraper: glass grid facade, swinging gondola, neighbouring towers
  Level533 立交桥     - a highway interchange: two deck levels with moving traffic, pillars, road signs, city behind
  Level534 停车场     - a cut-away parking garage: three decks of cars, ramp, ticket booth with barrier
  Level535 渡轮码头   - a ferry terminal: ferry at the pier, gangway, terminal building, passengers, gulls
  Level536 骑楼老街   - an arcade shophouse street: colonnades, hanging signs, scooters, laundry poles
  Level537 社区菜园   - a community garden: raised beds, bean poles, shed, wheelbarrow, gardeners; rain showers
  Level538 街头艺人   - a pedestrian street with performers: juggler, guitarist, living statue, onlookers
  Level539 雪夜车站   - a bus stop on a snowy night: shelter, lamp posts, lit windows, waiting people; snow
"""
import math
import random

from fdcore import CLEAR, E, H, OVERCAST, RAIN, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_modern import car_side
from levels_daily2 import umbrella
from levels_daily3 import plant
from weather import cloud, paper_sun, puddles, rain_layer, snow_layer, splash_rings

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
NIGHT_EDGE = (110, 110, 140)


def bus_side(c, x, base, col, s=1.0, stripe=(250, 250, 250), face_right=True):
    """City bus seen from the side (x = centre)."""
    k = 1 if face_right else -1
    piece(c, RRect(x - 120 * s, base - 90 * s, x + 120 * s, base - 14 * s, 12 * s), col, border=1.5, shadow=PROP)
    flat(c, RRect(x - 120 * s, base - 36 * s, x + 120 * s, base - 28 * s, 1), stripe)
    for i in range(6):
        wx = x - 100 * s + i * 34 * s
        flat(c, RRect(wx, base - 80 * s, wx + 28 * s, base - 50 * s, 3), (60, 80, 110))
    flat(c, RRect(x + k * 96 * s - 12 * s, base - 82 * s, x + k * 96 * s + 12 * s, base - 16 * s, 3), (60, 80, 110))
    piece(c, RRect(x + k * 80 * s - 30 * s, base - 104 * s, x + k * 80 * s + 30 * s, base - 88 * s, 3), (40, 40, 50), shadow=SMALL)
    for wx in (x - 76 * s, x + 76 * s):
        piece(c, Circ(wx, base - 12 * s, 14 * s), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(wx, base - 12 * s, 6 * s), (190, 190, 200))


def dpiece(c, shapes, col, border=1.5, shadow=PROP):
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


# =================================================================== Level 530 bus terminal
def l530_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 240)
    cloud_bank(c, 110, (250, 250, 246), 5301, k=0.7)
    far_skyline(c, 236, 40, 150, (186, 196, 214), 5302, win=(206, 214, 230))
    # canopy over the bays
    piece(c, Poly([(-10, 150), (910, 150), (910, 176), (-10, 190)]), (240, 240, 244), border=1.5, shadow=PROP)
    for x in (60, 330, 600, 860):
        piece(c, RRect(x - 6, 176, x + 6, 470, 2), (90, 100, 120), shadow=PROP)
    # route signs hanging from the canopy
    for k, x in enumerate((180, 460, 740)):
        flat(c, Thick(x, 186, x, 200, 2), (90, 100, 120))
        col = [(220, 70, 70), (60, 120, 210), (90, 170, 110)][k]
        if k == 1 and "route" in d:
            col = (250, 180, 50)
        piece(c, RRect(x - 34, 200, x + 34, 236, 4), col, border=1.2, shadow=SMALL)
        sign_box(c, x - 22, 208, x + 22, 228, (250, 250, 250), 5303 + k, vertical=False)
    # parked buses
    bus_side(c, 230, 400, (90, 160, 90), s=1.4)
    bus_side(c, 660, 410, (240, 190, 60) if "bus" not in d else (220, 90, 140), s=1.4, face_right=False)
    # platform
    piece(c, RRect(-10, 420, 910, 612, 0), (200, 200, 196), shadow=LAYER)
    flat(c, RRect(-10, 420, 910, 432, 0), (250, 220, 60))
    for y in range(452, H, 30):
        flat(c, Thick(0, y, W, y, 1.2), (186, 186, 182))
    # departures board
    piece(c, [RRect(426, 300, 434, 520, 2)], (90, 100, 120), shadow=PROP)
    piece(c, RRect(380, 440, 520, 512, 4), (40, 44, 56), border=1.5, shadow=PROP)
    for k in range(3):
        y = 452 + k * 18
        flat(c, RRect(390, y, 412, y + 12, 2), [(220, 70, 70), (60, 120, 210), (90, 170, 110)][k])
        sign_box(c, 418, y, 480, y + 12, (220, 226, 240), 5306 + k, vertical=False)
        flat(c, RRect(486, y, 510, y + 12, 2), (250, 200, 60) if not (k == 2 and "board" in d) else (240, 90, 80))
    # shelter with an ad panel and a bench
    piece(c, [RRect(560, 460, 880, 470, 2), RRect(570, 470, 578, 590, 2), RRect(862, 470, 870, 590, 2)], (90, 100, 120), shadow=PROP)
    flat(c, RRect(578, 470, 862, 580, 0), (200, 226, 240, 0.5))
    piece(c, RRect(800, 480, 856, 570, 3), (240, 120, 160) if "ad" not in d else (110, 200, 230), border=1.2, shadow=SMALL)
    flat(c, [Circ(828, 510, 12), RRect(812, 536, 844, 546, 2)], (250, 250, 250))
    piece(c, [RRect(600, 540, 780, 552, 3), RRect(606, 552, 614, 590, 2), RRect(766, 552, 774, 590, 2)], (150, 110, 80) if "bench" not in d else (90, 150, 200),
          border=1.2, shadow=PROP)
    # passengers
    modern(c, 650, 548, (200, 90, 90), bottom=(40, 40, 50), hair=(130, 130, 140), h=2.0, glasses=True)
    modern(c, 730, 548, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.9, style="long")
    modern(c, 120, 596, (60, 110, 180), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3, bag=(150, 100, 60))
    modern(c, 220, 600, (120, 190, 160), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.2, style="long")
    modern(c, 300, 600, (250, 160, 90), bottom=(60, 70, 110), hair=(40, 30, 30), h=1.5, style="twin")
    # bin
    piece(c, RRect(30, 520, 62, 570, 4), (90, 150, 110), border=1.2, shadow=PROP)


L530_ELEMENTS = [
    E("banner", lambda c, m: (flat(c, Thick(330, 190, 330, 210, 2), (90, 100, 120)),
                              piece(c, Poly([(318, 210), (342, 210), (342, 270), (330, 260), (318, 270)]), (240, 140, 60), border=1, shadow=SMALL)),
      pivot=(330, 190), anim=dict(swingAngle=6, swingSpeed=0.4)),
    E("pigeon", lambda c, m: piece(c, [Ell(470, 590, 10, 6), Circ(478, 582, 5)], (150, 150, 170), border=1, shadow=SMALL), pivot=(470, 596),
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.2, stretch=(0, 0.08), scaleSpeed=1.6)),
    bird_el("bird", 300, 60, s=8, speed=20),
]

L530_DIFFS = [
    ("route", 460, 218, 0),
    ("bus", 660, 350, 0),
    ("board", 498, 494, 0),
    ("ad", 828, 525, 0),
    ("bench", 690, 546, 0),
]


# =================================================================== Level 531 fountain square
def l531_bg(c, d):
    sky(c, (130, 194, 240), (222, 236, 246), 340)
    cloud_bg(c, 140, 60, 0.7)
    cloud_bg(c, 760, 50, 0.6)
    # buildings around the square
    for k, (x, w, h, col) in enumerate(((-10, 200, 230, (236, 214, 180)), (190, 140, 190, (210, 170, 150)), (560, 160, 200, (220, 200, 170)),
                                        (720, 200, 240, (190, 170, 160)))):
        piece(c, RRect(x, 330 - h, x + w, 330, 2), col, border=1.5, shadow=PROP)
        for wy in range(330 - h + 24, 310, 50):
            for wx in range(int(x) + 20, int(x + w) - 30, 44):
                flat(c, RRect(wx, wy, wx + 24, wy + 30, 2), (150, 190, 220))
    # clock tower (centre back)
    piece(c, RRect(400, 40, 500, 330, 2), (230, 210, 180), border=2, shadow=PROP)
    piece(c, Poly([(390, 44), (510, 44), (450, -10)]), (90, 120, 160) if "roof" not in d else (200, 90, 70), border=2, shadow=PROP)
    piece(c, Circ(450, 110, 34), (250, 250, 252), border=1.5, shadow=SMALL)
    c.ellipse_ring(450, 110, 34, 34, 3, (90, 70, 60))
    flat(c, [Thick(450, 110, 450, 88, 3), Thick(450, 110, 468, 118, 3)], (60, 50, 50))
    flat(c, RRect(430, 230, 470, 330, 18), (120, 80, 60))
    # cafe awning on the right building
    piece(c, Poly([(570, 270), (710, 270), (720, 300), (560, 300)]), (220, 70, 70) if "awning" not in d else (60, 140, 110), border=1.2, shadow=PROP)
    for x in range(576, 710, 24):
        flat(c, Poly([(x, 270), (x + 12, 270), (x + 13, 300), (x + 1, 300)]), (250, 250, 250))
    # square paving
    piece(c, RRect(-10, 330, 910, 612, 0), (220, 206, 186), shadow=LAYER)
    for y in range(350, H, 26):
        flat(c, Thick(0, y, W, y, 1.2), (206, 192, 172))
    for x in range(-200, 1100, 60):
        flat(c, Thick(x, 330, x + (x - 450) * 0.6, H, 1.2), (206, 192, 172))
    # fountain
    piece(c, Ell(450, 470, 200, 46), (190, 186, 180), border=2, shadow=PROP)
    flat(c, Ell(450, 466, 180, 36), (120, 180, 220))
    piece(c, [RRect(436, 380, 464, 466, 4), Ell(450, 380, 60, 14)], (200, 196, 190), border=1.5, shadow=SMALL)
    flat(c, Ell(450, 378, 50, 9), (120, 180, 220))
    # flower beds
    for k, x in enumerate((90, 810)):
        piece(c, Ell(x, 420, 80, 22), (120, 170, 90), shadow=PROP)
        for j in range(9):
            col = (240, 90, 110) if (j % 2) else (250, 200, 70)
            if k == 1 and j % 2 and "flowers" in d:
                col = (150, 110, 230)
            flat(c, Circ(x - 64 + j * 16, 414 - (j % 3) * 4, 6), col)
    # benches + people
    for k, x in enumerate((140, 760)):
        piece(c, [RRect(x - 70, 520, x + 70, 532, 3), RRect(x - 70, 500, x + 70, 510, 3), RRect(x - 62, 532, x - 54, 570, 2),
                  RRect(x + 54, 532, x + 62, 570, 2)], (60, 110, 80) if not (k == 1 and "bench" in d) else (190, 120, 70), border=1.2, shadow=PROP)
    modern(c, 120, 530, (200, 110, 150), bottom=(60, 60, 80), hair=(130, 130, 140), h=1.9, glasses=True)
    modern(c, 780, 530, (90, 150, 220), bottom=(50, 60, 90), hair=(40, 30, 30), h=1.9)
    modern(c, 300, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.2, style="long", skirt=True)
    modern(c, 610, 600, (120, 190, 120), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.3, bag=(240, 120, 60))
    # balloon on the kid's hand
    modern(c, 360, 600, (250, 120, 120), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.5, style="twin")
    flat(c, Thick(372, 556, 380, 490, 1.2), (90, 90, 100))
    piece(c, Ell(380, 478, 14, 17), (90, 170, 240) if "balloon" not in d else (250, 200, 60), border=1, shadow=SMALL)
    # lamp posts
    for x in (250, 650):
        piece(c, [RRect(x - 3, 360, x + 3, 520, 2), Ell(x, 352, 14, 10)], (50, 56, 70), shadow=PROP)


def jets(c, m):
    for k, (dx, h) in enumerate(((-40, 50), (0, 80), (40, 50))):
        x = 450 + dx
        flat(c, [Thick(x, 378, x + dx * 0.3, 378 - h, 4)], (210, 236, 250, 0.85))
        soft_union(c, [Circ(x + dx * 0.3, 378 - h, 6)], (230, 246, 255), 0.7, spread=6)


L531_ELEMENTS = [
    E("jets", jets, pivot=(450, 378), anim=dict(stretch=(0, 0.1), scaleSpeed=2.0)),
    E("ripple", lambda c, m: c.ellipse_ring(450, 470, 120, 22, 2, (200, 230, 250, 0.8)), pivot=(450, 470), anim=dict(pulse=0.15, scaleSpeed=0.8)),
] + [
    E("pigeon%d" % i, (lambda x, y: lambda c, m: (piece(c, [Ell(x, y, 10, 6), Circ(x + 8, y - 7, 5)], (150, 150, 170), border=1, shadow=SMALL),
                                                flat(c, Poly([(x + 12, y - 8), (x + 17, y - 6), (x + 12, y - 5)]), (230, 160, 60))))(x, y),
      pivot=(x, y + 6), anim=dict(bobAmplitude=(8, 0), bobSpeed=0.25, stretch=(0, 0.1), scaleSpeed=1.6, phase=i / 3))
    for i, (x, y) in enumerate(((500, 560), (540, 572), (200, 470)))
] + [bird_el("bird", 600, 120, s=8, speed=-20)]

L531_DIFFS = [
    ("roof", 450, 20, 0),
    ("awning", 640, 285, 0),
    ("flowers", 810, 412, 0),
    ("bench", 760, 516, 0),
    ("balloon", 380, 478, 0),
]


# =================================================================== Level 532 skyscraper window cleaners
def l532_bg(c, d):
    sky(c, (110, 170, 230), (210, 230, 246), 600)
    cloud_bg(c, 760, 120, 1.0)
    cloud_bg(c, 820, 420, 0.8)
    # neighbouring tower (right, further away)
    piece(c, RRect(700, 60, 910, 620, 2), (170, 186, 210), border=1.5, shadow=LAYER)
    for y in range(80, 600, 40):
        for x in range(716, 900, 36):
            flat(c, RRect(x, y, x + 26, y + 28, 1), (196, 214, 234))
    # main glass tower (fills most of the frame)
    piece(c, RRect(60, -10, 640, 620, 0), (80, 110, 150), shadow=LAYER)
    rnd = random.Random(5321)
    for r in range(12):
        for i in range(7):
            x, y = 76 + i * 80, 10 + r * 52
            col = (150, 196, 230) if (r + i) % 3 else (176, 214, 240)
            if r == 3 and i == 5 and "pane" in d:
                col = (250, 200, 120)
            flat(c, RRect(x, y, x + 72, y + 46, 1), col)
            flat(c, Poly([(x + 6, y + 40), (x + 20, y + 40), (x + 40, y + 6), (x + 26, y + 6)]), (220, 238, 250, 0.6))
    # balcony with plants + flag on a pole
    piece(c, RRect(60, 470, 280, 482, 2), (220, 220, 230), border=1.2, shadow=PROP)
    flat(c, [Thick(70 + k * 20, 482, 70 + k * 20, 520, 2) for k in range(11)], (220, 220, 230))
    flat(c, Thick(60, 520, 280, 520, 3), (220, 220, 230))
    plant(c, 110, 470, s=0.9)
    plant(c, 230, 470, s=0.9, pot=(90, 150, 210) if "pot" not in d else (240, 200, 60))
    flat(c, Thick(640, 300, 690, 300, 3), (200, 200, 210))
    piece(c, Poly([(690, 286), (740, 296), (690, 314)]),
          (220, 70, 70) if "flag" not in d else (60, 160, 110), border=1, shadow=SMALL)
    # a nest on a ledge + a blind behind a window
    piece(c, RRect(520, 360, 640, 372, 2), (200, 200, 210), shadow=SMALL)
    if "nest" not in d:
        piece(c, Ell(590, 356, 22, 8), (150, 110, 70), border=1, shadow=SMALL)
        flat(c, [Circ(582, 350, 4), Circ(594, 348, 4)], (250, 246, 236))
    flat(c, RRect(156, 166, 228, 196, 1), (250, 236, 200))
    for y in range(168, 196, 5):
        flat(c, Thick(156, y, 228, y, 1), (230, 210, 170))


def gondola(c, m):
    flat(c, [Thick(250, -10, 250, 260, 1.4), Thick(470, -10, 470, 260, 1.4)], (60, 60, 70))
    piece(c, [RRect(230, 260, 490, 274, 2), RRect(230, 230, 490, 236, 2)], (220, 220, 230), border=1.2, shadow=PROP)
    flat(c, [Thick(236 + k * 26, 236, 236 + k * 26, 260, 2) for k in range(11)], (220, 220, 230))
    modern(c, 300, 260, (250, 160, 40), bottom=(60, 70, 100), hair=(40, 30, 30), h=1.6)
    modern(c, 420, 260, (250, 160, 40), bottom=(60, 70, 100), hair=(90, 60, 40), h=1.6)
    piece(c, [Ell(304, 204, 9, 6)], (250, 220, 60), shadow=None)
    piece(c, [Ell(424, 204, 9, 6)], (250, 220, 60), shadow=None)
    flat(c, [Thick(440, 222, 470, 200, 3), Thick(466, 190, 466, 214, 4)], (60, 60, 70))
    piece(c, Poly([(350, 260), (380, 260), (376, 238), (354, 238)]), (60, 140, 220), border=1, shadow=SMALL)


L532_ELEMENTS = [
    E("gondola", gondola, pivot=(360, -10), anim=dict(swingAngle=1.5, swingSpeed=0.3)),
    E("squeegee", lambda c, m: flat(c, Thick(300, 226, 330, 196, 3), (60, 60, 70)), pivot=(300, 226), anim=dict(swingAngle=20, swingSpeed=1.0)),
    bird_el("bird1", 680, 200, s=9, speed=-20),
    cloud_el("cloud", 780, 40, 0.6, 6),
    E("glint", lambda c, m: flat(c, Poly(star_pts(560, 520, 14, 4, points=4)), (255, 255, 255)), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=0.5)),
]

L532_DIFFS = [
    ("pane", 512, 189, 0),
    ("pot", 230, 452, 0),
    ("flag", 710, 300, 0),
    ("nest", 590, 354, 0),
]


# =================================================================== Level 533 highway interchange
def l533_bg(c, d):
    sky(c, (130, 190, 236), (232, 230, 230), 300)
    cloud_bank(c, 100, (250, 250, 246), 5331, k=0.6)
    far_skyline(c, 300, 60, 200, (176, 190, 214), 5332, win=(200, 210, 230))
    far_round_trees(c, 320, 20, (110, 160, 120), 5333)
    # ground road
    piece(c, RRect(-10, 470, 910, 612, 0), (110, 110, 118), shadow=LAYER)
    flat(c, RRect(-10, 462, 910, 474, 0), (200, 200, 196))
    for x in range(0, 900, 90):
        flat(c, Thick(x, 540, x + 50, 540, 4), (250, 250, 240))
    # pillars
    for k, x in enumerate((140, 450, 760)):
        piece(c, RRect(x - 22, 300, x + 22, 470, 3), (200, 196, 190) if not (k == 1 and "pillar" in d) else (240, 190, 120), border=1.5, shadow=PROP)
    # upper deck
    piece(c, RRect(-10, 250, 910, 300, 2), (190, 190, 196), border=1.5, shadow=PROP)
    flat(c, RRect(-10, 290, 910, 300, 0), (160, 160, 168))
    flat(c, [Thick(-10, 250, 910, 250, 4)], (220, 220, 226))
    for x in range(0, 900, 30):
        flat(c, Thick(x, 236, x, 250, 2), (220, 220, 226))
    flat(c, Thick(-10, 236, 910, 236, 3), (220, 220, 226))
    # overhead sign gantry over the upper deck
    flat(c, [Thick(560, 250, 560, 150, 5), Thick(860, 250, 860, 150, 5), Thick(560, 150, 860, 150, 5)], (150, 150, 160))
    for k, x in enumerate((590, 730)):
        piece(c, RRect(x, 156, x + 110, 206, 3), (40, 130, 80) if not (k == 1 and "sign" in d) else (50, 90, 190), border=1.5, shadow=SMALL)
        sign_box(c, x + 12, 164, x + 98, 180, (250, 250, 250), 5334 + k, vertical=False)
        flat(c, Poly([(x + 50, 184), (x + 66, 194), (x + 50, 202)]), (250, 250, 250))
    # billboard (left)
    flat(c, [Thick(130, 236, 130, 170, 4), Thick(230, 236, 230, 170, 4)], (90, 96, 110))
    piece(c, RRect(80, 80, 280, 176, 4), (250, 200, 60) if "billboard" not in d else (220, 110, 170), border=1.5, shadow=PROP)
    flat(c, [Circ(130, 128, 26), RRect(170, 110, 260, 124, 3), RRect(170, 134, 240, 146, 3)], (250, 250, 250))
    # verge with bushes + lamp posts
    for x in (40, 300, 600, 860):
        bush(c, x, 470, s=1.1)
    for k, x in enumerate((300, 620)):
        piece(c, [RRect(x - 3, 480, x + 3, 600, 2), Thick(x, 480, x + 30, 476, 3)], (90, 96, 110), shadow=PROP)
        piece(c, RRect(x + 14, 470, x + 46, 486, 5), (90, 96, 110) if not (k == 1 and "lamp" in d) else (220, 80, 80), shadow=SMALL)
        flat(c, Ell(x + 30, 484, 12, 4), (255, 236, 160))
    # cyclist on the pavement
    piece(c, RRect(-10, 590, 910, 612, 0), (190, 190, 186), shadow=SMALL)


def car_el(eid, col, base, speed, start, s=1.0):
    return E(eid, lambda c, m: car_side(c, 0, base, col, s=s), anim=dict(drift_across(-62 * s, 62 * s, speed, start=start)))


L533_ELEMENTS = [
    car_el("c1", (220, 70, 70), 236, 90, 100, 0.8),
    car_el("c2", (60, 120, 210), 236, 90, 600, 0.8),
    car_el("c3", (250, 250, 250), 520, -110, 300, 1.2),
    car_el("c4", (250, 190, 60), 520, -110, 800, 1.2),
    car_el("c5", (90, 170, 120), 580, 130, 500, 1.3),
    bird_el("bird", 400, 50, s=8, speed=-18),
]

L533_DIFFS = [
    ("pillar", 450, 385, 0),
    ("sign", 785, 180, 0),
    ("billboard", 180, 128, 0),
    ("lamp", 650, 480, 0),
]


# =================================================================== Level 534 parking garage
def l534_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 620)
    far_skyline(c, 120, 30, 100, (186, 196, 214), 5341)
    # three decks
    for k, y in enumerate((120, 270, 420)):
        c.rect(30, y, 870, y + 150, (120, 124, 134))
        flat(c, RRect(30, y + 140, 870, y + 150, 0), (100, 104, 114))
        for x in range(60, 860, 110):
            flat(c, Thick(x, y + 140, x + 20, y + 120, 2), (250, 250, 240))
    for y in (120, 270, 420, 570):
        piece(c, RRect(10, y - 12, 890, y, 2), (210, 210, 214), border=1.5, shadow=PROP)
    for x in (30, 450, 870):
        piece(c, RRect(x - 14, 110, x + 14, 600, 2), (210, 210, 214), border=1.2, shadow=PROP)
    # deck numbers
    for k, y in enumerate((150, 300, 450)):
        col = [(60, 120, 210), (220, 70, 70), (90, 170, 110)][k]
        if k == 1 and "level" in d:
            col = (250, 190, 50)
        piece(c, Circ(450, y, 20), col, border=1.2, shadow=SMALL)
        flat(c, Thick(450, y - 10, 450, y + 10, 4), (250, 250, 250))
    # parked cars
    cars = [((130, 258), (220, 70, 70)), ((330, 258), (250, 250, 250)), ((600, 258), (60, 120, 210)), ((780, 258), (40, 40, 50)),
            ((140, 408), (250, 190, 60)), ((560, 408), (120, 120, 130)), ((760, 408), (90, 170, 120)),
            ((300, 558), (200, 110, 160)), ((620, 558), (250, 250, 250))]
    for k, ((x, b), col) in enumerate(cars):
        if k == 5 and "car" in d:
            col = (240, 130, 50)
        if k == 2 and "gone" in d:
            continue
        car_side(c, x, b, col, s=1.2)
    # ramp on the middle deck
    flat(c, Poly([(250, 408), (400, 300), (420, 300), (270, 408)]), (150, 154, 164))
    # entrance booth with barrier (front right)
    c.rect(870, 0, W, H, (196, 206, 220))
    piece(c, RRect(760, 486, 840, 560, 4), (240, 236, 226), border=1.5, shadow=PROP)
    flat(c, RRect(770, 496, 830, 530, 2), (170, 210, 236))
    piece(c, RRect(750, 474, 850, 490, 3), (60, 120, 210) if "booth" not in d else (220, 80, 80), border=1.2, shadow=SMALL)
    modern(c, 800, 540, (60, 90, 150), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.3)
    # extinguisher + sign on a pillar
    piece(c, RRect(40, 340, 60, 380, 5), (220, 50, 50), border=1, shadow=SMALL)
    piece(c, RRect(462, 190, 520, 230, 3), (250, 250, 250), border=1.2, shadow=SMALL)
    flat(c, Poly([(474, 210), (494, 198), (494, 204), (508, 204), (508, 216), (494, 216), (494, 222)]), (60, 160, 90))
    # people walking to their cars
    modern(c, 240, 404, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.4, bag=(200, 70, 70))
    modern(c, 680, 554, (120, 170, 120), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.4)


L534_ELEMENTS = [
    E("barrier", lambda c, m: (piece(c, RRect(740, 528, 756, 560, 3), (250, 200, 60), shadow=SMALL),
                               piece(c, RRect(620, 524, 748, 532, 3), (250, 250, 250), border=1, shadow=SMALL),
                               flat(c, [RRect(630 + k * 30, 524, 644 + k * 30, 532, 1) for k in range(4)], (220, 60, 60))),
      pivot=(748, 528), anim=dict(swingAngle=25, swingSpeed=0.15)),
    spin_el("vent", lambda c, m: (piece(c, Circ(240, 196, 22), (200, 204, 214), border=1, shadow=SMALL),
                                  flat(c, [Thick(240 - 18 * math.cos(a), 196 - 18 * math.sin(a), 240 + 18 * math.cos(a), 196 + 18 * math.sin(a), 6)
                                           for a in (0.2, 1.25, 2.3)], (110, 116, 130))), (240, 196), 200),
    E("blink", lambda c, m: soft_union(c, [Circ(812, 480, 6)], (255, 200, 80), 0.8, spread=8), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.5)),
]

L534_DIFFS = [
    ("level", 450, 300, 0),
    ("car", 560, 380, 0),
    ("gone", 600, 230, 0),
    ("booth", 800, 482, 0),
]


# =================================================================== Level 535 ferry terminal
def ferry(c, x, base, s=1.0, hull=(250, 250, 250), band=(60, 120, 210), funnel=(220, 70, 70)):
    piece(c, Poly([(x - 230 * s, base - 70 * s), (x + 260 * s, base - 70 * s), (x + 220 * s, base), (x - 210 * s, base)]), hull, border=1.5, shadow=PROP)
    flat(c, RRect(x - 226 * s, base - 40 * s, x + 250 * s, base - 30 * s, 1), band)
    piece(c, RRect(x - 170 * s, base - 130 * s, x + 170 * s, base - 70 * s, 6), hull, border=1.5, shadow=PROP)
    piece(c, RRect(x - 110 * s, base - 176 * s, x + 110 * s, base - 130 * s, 6), hull, border=1.5, shadow=PROP)
    for k in range(10):
        flat(c, RRect(x - 156 * s + k * 32 * s, base - 116 * s, x - 136 * s + k * 32 * s, base - 96 * s, 3), (60, 90, 130))
    for k in range(6):
        flat(c, RRect(x - 96 * s + k * 32 * s, base - 166 * s, x - 76 * s + k * 32 * s, base - 146 * s, 3), (60, 90, 130))
    piece(c, Poly([(x + 20 * s, base - 176 * s), (x + 70 * s, base - 176 * s), (x + 64 * s, base - 226 * s), (x + 28 * s, base - 226 * s)]), funnel,
          border=1.5, shadow=PROP)
    flat(c, RRect(x + 26 * s, base - 206 * s, x + 66 * s, base - 196 * s, 1), (250, 250, 250))


def l535_bg(c, d):
    sky(c, (120, 184, 236), (232, 230, 220), 300)
    cloud_bank(c, 120, (250, 250, 246), 5351, k=0.7)
    far_ridge(c, 230, 40, (150, 180, 200), 5352)
    far_skyline(c, 240, 20, 80, (180, 196, 214), 5353, x0=500, x1=920)
    c.gradient(240, H, (90, 160, 210), (50, 110, 170))
    for k in range(16):
        rnd = random.Random(5354 + k)
        x, y = rnd.uniform(0, 900), rnd.uniform(260, 560)
        flat(c, Thick(x, y, x + rnd.uniform(20, 60), y, 2), (140, 196, 230))
    # ferry at the pier
    ferry(c, 440, 420, s=1.0, funnel=(220, 70, 70) if "funnel" not in d else (250, 190, 50))
    # lifebuoys on the rail
    for k, x in enumerate((300, 560)):
        c.ellipse_ring(x, 376, 17, 17, 9, (250, 120, 50) if not (k == 1 and "buoy" in d) else (60, 200, 150))
    # pier + terminal (right)
    piece(c, RRect(640, 420, 910, 470, 2), (170, 120, 80), border=1.5, shadow=PROP)
    for x in range(650, 910, 40):
        flat(c, RRect(x, 470, x + 10, 600, 1), (130, 90, 60))
    piece(c, RRect(700, 250, 910, 420, 3), (240, 236, 226), border=1.5, shadow=PROP)
    piece(c, Poly([(690, 256), (920, 256), (920, 224), (740, 210)]), (60, 120, 180), border=1.5, shadow=PROP)
    for x in (720, 790, 860):
        flat(c, RRect(x, 290, x + 40, 340, 3), (150, 196, 226))
    flat(c, RRect(760, 360, 820, 420, 3), (90, 70, 60))
    piece(c, RRect(730, 228, 860, 250, 3), (250, 250, 250), border=1, shadow=SMALL)
    sign_box(c, 740, 232, 850, 246, (60, 120, 180), 5355, vertical=False)
    # gangway
    piece(c, Poly([(600, 420), (640, 420), (700, 440), (690, 448), (600, 430)]), (200, 200, 210), border=1.2, shadow=SMALL)
    # passengers on the pier + queue
    modern(c, 680, 420, (220, 90, 90), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.6, bag=(150, 100, 60))
    modern(c, 740, 420, (90, 150, 220) if "coat" not in d else (250, 200, 90), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.6, style="long")
    modern(c, 820, 420, (120, 190, 120), bottom=(50, 50, 60), hair=(130, 130, 140), h=1.6, glasses=True)
    # bollards + rope
    for x in (660, 880):
        piece(c, [RRect(x - 8, 404, x + 8, 420, 3), Ell(x, 404, 11, 4)], (60, 60, 70), shadow=SMALL)
    flat(c, Thick(660, 410, 610, 400, 2), (200, 180, 140))
    # small boat in the foreground (left)
    piece(c, Poly([(20, 530), (190, 530), (170, 566), (40, 566)]), (240, 120, 80) if "boat" not in d else (90, 170, 220), border=1.5, shadow=PROP)
    flat(c, Thick(100, 530, 100, 470, 3), (120, 90, 70))
    piece(c, Poly([(104, 474), (104, 526), (150, 526)]), (250, 250, 246), border=1, shadow=SMALL)
    modern(c, 70, 540, (250, 220, 70), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.2)


L535_ELEMENTS = [
    E("smoke", lambda c, m: soft_union(c, [Circ(500, 186, 12)], (230, 230, 236), 0.8, spread=10),
      anim=dict(driftVelocity=(-10, 18), driftLength=70, driftFade=True, driftGrow=1.8)),
    E("smoke2", lambda c, m: soft_union(c, [Circ(500, 186, 12)], (230, 230, 236), 0.8, spread=10),
      anim=dict(driftVelocity=(-10, 18), driftLength=70, driftFade=True, driftGrow=1.8, phase=0.5)),
    E("bob", lambda c, m: (piece(c, Poly([(260, 600), (340, 600), (330, 612), (270, 612)]), (250, 200, 60), border=1, shadow=SMALL)), pivot=(300, 606),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.5, swingAngle=4, swingSpeed=0.4)),
    bird_el("gull1", 200, 160, s=9, speed=-22),
    bird_el("gull2", 600, 140, s=8, speed=26),
]

L535_DIFFS = [
    ("funnel", 486, 220, 0),
    ("buoy", 560, 376, 0),
    ("coat", 741, 365, 0),
    ("boat", 105, 548, 0),
]


# =================================================================== Level 536 arcade shophouse street
def l536_bg(c, d):
    sky(c, (140, 196, 236), (230, 236, 240), 160)
    # shophouse row (three buildings) with upper floors
    cols = [(240, 214, 170), (200, 220, 200), (240, 200, 190)]
    for k, x0 in enumerate((-10, 300, 610)):
        col = cols[k]
        piece(c, RRect(x0, 30, x0 + 310, 400, 2), col, border=1.5, shadow=PROP)
        piece(c, RRect(x0 - 4, 24, x0 + 314, 40, 3), lit(col, 0.85), border=1, shadow=SMALL)
        for i in range(3):
            wx = x0 + 30 + i * 96
            flat(c, RRect(wx, 70, wx + 60, 150, 26), (150, 190, 220))
            flat(c, [Thick(wx + 30, 70, wx + 30, 150, 2), Thick(wx, 110, wx + 60, 110, 2)], lit(col, 0.85))
            shut = (90, 150, 110) if not (k == 1 and i == 0 and "shutter" in d) else (220, 120, 90)
            flat(c, [RRect(wx - 14, 70, wx, 150, 2), RRect(wx + 60, 70, wx + 74, 150, 2)], shut)
        # colonnade
        for i in range(5):
            piece(c, RRect(x0 + 10 + i * 72, 240, x0 + 28 + i * 72, 470, 2), lit(col, 0.95), border=1, shadow=PROP)
        flat(c, RRect(x0, 236, x0 + 310, 252, 0), lit(col, 0.85))
        flat(c, RRect(x0, 252, x0 + 310, 470, 0), lit(col, 0.6))
        for i in range(4):
            sx = x0 + 34 + i * 72
            flat(c, RRect(sx, 300, sx + 42, 420, 2), (250, 230, 180))
    # laundry poles between the upper windows
    for x0 in (60, 390, 680):
        flat(c, Thick(x0, 180, x0 + 160, 180, 2), (150, 120, 90))
        for k, col in enumerate(((250, 250, 250), (220, 90, 90), (90, 150, 220), (250, 210, 80))):
            if x0 == 390 and k == 1 and "laundry" in d:
                col = (120, 200, 120)
            flat(c, RRect(x0 + 10 + k * 38, 182, x0 + 40 + k * 38, 216, 2), col)
    # vertical hanging signs
    for k, (x, col) in enumerate(((255, (200, 50, 50)), (565, (40, 90, 160)), (856, (220, 160, 40)))):
        if k == 2 and "sign" in d:
            col = (120, 70, 160)
        piece(c, RRect(x, 160, x + 40, 300, 3), col, border=1.5, shadow=PROP)
        sign_box(c, x + 8, 172, x + 32, 288, (250, 240, 200), 5361 + k)
    # street
    piece(c, RRect(-10, 470, 910, 612, 0), (160, 156, 150), shadow=LAYER)
    flat(c, RRect(-10, 470, 910, 486, 0), (200, 196, 186))
    # scooters + people
    for k, (x, col) in enumerate(((240, (220, 70, 70)), (600, (60, 140, 200)))):
        if k == 1 and "scooter" in d:
            col = (250, 200, 60)
        piece(c, [Poly([(x - 40, 560), (x + 20, 560), (x + 40, 530), (x + 10, 520), (x - 30, 530)]), Thick(x + 30, 530, x + 40, 490, 4)], col,
              border=1.2, shadow=PROP)
        flat(c, Thick(x + 30, 490, x + 52, 486, 4), (40, 40, 46))
        for wx in (x - 34, x + 34):
            piece(c, Circ(wx, 566, 14), (40, 40, 46), shadow=SMALL)
            flat(c, Circ(wx, 566, 5), (190, 190, 200))
    modern(c, 380, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.2, bag=(200, 70, 70))
    modern(c, 470, 600, (120, 190, 160), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.1, style="long")
    modern(c, 820, 600, (150, 120, 180), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.3, glasses=True)
    # fruit stall at the corner
    piece(c, RRect(30, 500, 140, 560, 3), (170, 120, 80), border=1.2, shadow=PROP)
    flat(c, [Circ(46 + k * 16, 494, 8) for k in range(6)], (250, 160, 40))


L536_ELEMENTS = [
    E("fan", lambda c, m: (flat(c, Thick(500, 252, 500, 268, 2), (90, 90, 100)),
                           flat(c, [Thick(500 - 40 * math.cos(a), 272 - 4 * math.sin(a), 500 + 40 * math.cos(a), 272 + 4 * math.sin(a), 5) for a in (0.3, 1.9)],
                                (170, 130, 90))), pivot=(500, 272), anim=dict(stretch=(0.8, 0), scaleSpeed=3.0)),
    E("cat", lambda c, m: piece(c, [Ell(870, 466, 20, 9), Circ(850, 458, 8), Poly([(844, 454), (846, 444), (850, 452)]),
                                    Poly([(852, 452), (856, 444), (858, 456)])], (240, 170, 90), border=1, shadow=SMALL),
      pivot=(870, 474), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
    E("bike", lambda c, m: (piece(c, [Circ(-20, 592, 12), Circ(20, 592, 12)], (40, 40, 46), shadow=SMALL),
                            flat(c, [Thick(-20, 592, 0, 566, 3), Thick(0, 566, 20, 592, 3)], (60, 120, 200)),
                            modern(c, 0, 576, (250, 250, 250), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.2)),
      anim=dict(drift_across(-30, 30, 40, start=100))),
    bird_el("bird", 300, 10, s=7, speed=18),
]

L536_DIFFS = [
    ("shutter", 323, 110, 0),
    ("laundry", 467, 199, 0),
    ("sign", 876, 230, 0),
    ("scooter", 600, 540, 0),
]


# =================================================================== Level 537 community garden (rain showers)
STEPS537 = [(CLEAR, 12), (OVERCAST, 4), (RAIN, 10), (OVERCAST, 4)]


def raised_bed(c, x0, x1, base, crop, col_crop, seed):
    piece(c, RRect(x0, base - 30, x1, base, 2), (170, 120, 80), border=1.5, shadow=PROP)
    flat(c, RRect(x0 + 6, base - 30, x1 - 6, base - 22, 1), (110, 80, 60))
    rnd = random.Random(seed)
    x = x0 + 20
    while x < x1 - 14:
        if crop == "cabbage":
            piece(c, [Circ(x, base - 40, 13), Circ(x - 8, base - 36, 9), Circ(x + 8, base - 36, 9)], col_crop, shadow=SMALL)
        elif crop == "carrot":
            flat(c, [Thick(x, base - 30, x - 6, base - 56, 3), Thick(x, base - 30, x + 6, base - 58, 3), Thick(x, base - 30, x, base - 60, 3)], col_crop)
        elif crop == "tomato":
            flat(c, Thick(x, base - 30, x, base - 100, 3), (130, 100, 70))
            flat(c, [Ell(x - 8, base - 70, 9, 6), Ell(x + 8, base - 86, 9, 6), Ell(x - 6, base - 50, 9, 6)], (80, 150, 80))
            flat(c, [Circ(x + 6, base - 62, 6), Circ(x - 6, base - 82, 6)], col_crop)
        x += 30 + rnd.uniform(-4, 4)


def l537_bg(c, d):
    sky(c, (140, 196, 236), (224, 236, 240), 230)
    far_skyline(c, 200, 50, 160, (190, 200, 216), 5371, win=(210, 218, 232))
    far_round_trees(c, 236, 26, (110, 170, 120), 5372)
    piece(c, RRect(-10, 236, 910, 612, 0), (140, 110, 80), shadow=LAYER)
    for y in range(260, 600, 40):
        flat(c, Thick(0, y, W, y + 6, 3), (126, 98, 70))
    # shed (left) with tools
    piece(c, RRect(20, 150, 200, 330, 2), (90, 140, 120), border=2, shadow=PROP)
    piece(c, Poly([(6, 156), (214, 156), (110, 100)]), (170, 80, 70) if "shed" not in d else (60, 90, 170), border=2, shadow=PROP)
    flat(c, RRect(80, 220, 140, 330, 2), (70, 110, 96))
    flat(c, [Thick(156, 210, 156, 320, 4), Thick(176, 210, 176, 320, 4)], (150, 110, 70))
    flat(c, [Poly([(148, 320), (164, 320), (162, 336), (150, 336)]), Ell(176, 324, 8, 10)], (150, 150, 160))
    # raised beds
    raised_bed(c, 240, 520, 330, "tomato", (220, 50, 50) if "tomato" not in d else (250, 200, 60), 5373)
    raised_bed(c, 560, 880, 330, "cabbage", (140, 200, 110), 5374)
    raised_bed(c, 40, 360, 470, "carrot", (90, 170, 80), 5375)
    raised_bed(c, 420, 760, 470, "cabbage", (140, 200, 110) if "cabbage" not in d else (170, 110, 190), 5376)
    # bean poles teepee
    flat(c, [Thick(800, 470, 830, 360, 3), Thick(860, 470, 830, 360, 3), Thick(830, 470, 830, 360, 3)], (150, 110, 70))
    flat(c, [Ell(820 + (k % 2) * 18, 380 + k * 18, 8, 5) for k in range(5)], (90, 160, 90))
    # wheelbarrow + watering can + gardeners
    piece(c, [Poly([(60, 520), (170, 520), (150, 560), (80, 560)]), Thick(170, 524, 210, 540, 4)], (60, 120, 200) if "barrow" not in d else (220, 90, 80),
          border=1.5, shadow=PROP)
    piece(c, Circ(70, 566, 12), (40, 40, 46), shadow=SMALL)
    flat(c, Ell(116, 518, 46, 8), (110, 80, 60))
    modern(c, 300, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(130, 130, 140), h=2.3, glasses=True)
    piece(c, Ell(301, 486, 24, 6), (230, 200, 120), shadow=None)                      # straw hat brim
    modern(c, 560, 600, (120, 190, 120), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.2, style="long")
    piece(c, [RRect(590, 540, 630, 574, 6), Thick(628, 548, 656, 530, 4)], (250, 190, 60), border=1.2, shadow=PROP)
    # compost bins + sunflowers (right)
    piece(c, RRect(780, 510, 880, 590, 3), (90, 70, 60), border=1.5, shadow=PROP)
    for x in range(784, 880, 12):
        flat(c, Thick(x, 514, x, 586, 2), (110, 86, 70))
    for x, y in ((700, 360), (740, 380)):
        flat(c, Thick(x, 470, x, y, 4), (80, 140, 80))
        flat(c, [Circ(x + 14 * math.cos(a), y + 14 * math.sin(a), 8) for a in [j * math.pi / 4 for j in range(8)]], (250, 200, 50))
        flat(c, Circ(x, y, 9), (120, 80, 40))


L537_ELEMENTS = [
    E("bee", lambda c, m: (flat(c, Ell(0, 0, 5, 4), (250, 200, 50)), flat(c, [Ell(-2, -5, 4, 3), Ell(3, -5, 4, 3)], (240, 250, 255))),
      anim=dict(drift_across(-6, 6, 18, start=600), driftVelocity=(18, 0), bobAmplitude=(0, 26), bobSpeed=0.4)),
    E("spray", lambda c, m: [soft_union(c, [Circ(660 + k * 10, 536 + k * k * 1.6, 3)], (170, 210, 250), 0.8, spread=3) for k in range(5)],
      anim=dict(twinkle=0.4, twinkleSpeed=1.4)),
    paper_sun("sun", 760, 60, r=30),
    cloud("cloudA", 200, 50, 1.2, (176, 182, 196), W_(OVERCAST, RAIN)),
    cloud("cloudB", 600, 40, 1.4, (168, 174, 190), W_(OVERCAST, RAIN)),
    puddles("puddles", [Ell(400, 540, 40, 6), Ell(720, 590, 30, 5)], mask=W_(RAIN)),
    rain_layer("rain", 537, 70, 24, 1.3, 0.6, 260, mask=W_(RAIN)),
] + splash_rings("splash", [(380, 540, 7), (700, 590, 6)], mask=W_(RAIN))

L537_DIFFS = [
    ("shed", 110, 130, 0),
    ("tomato", 380, 260, 0),
    ("cabbage", 590, 430, 0),
    ("barrow", 120, 540, 0),
]


# =================================================================== Level 538 street performers
def l538_bg(c, d):
    sky(c, (140, 196, 236), (230, 236, 240), 200)
    # shop fronts
    for k, (x0, col, aw) in enumerate(((-10, (236, 214, 180), (220, 80, 80)), (300, (190, 210, 220), (60, 120, 200)), (600, (230, 200, 200), (90, 160, 110)))):
        piece(c, RRect(x0, 20, x0 + 310, 360, 2), col, border=1.5, shadow=PROP)
        for i in range(3):
            flat(c, RRect(x0 + 30 + i * 96, 60, x0 + 86 + i * 96, 140, 3), (150, 190, 220))
        if k == 1 and "awning" in d:
            aw = (250, 180, 60)
        piece(c, Poly([(x0 + 10, 190), (x0 + 300, 190), (x0 + 310, 230), (x0, 230)]), aw, border=1.2, shadow=PROP)
        for x in range(x0 + 16, x0 + 300, 30):
            flat(c, Poly([(x, 190), (x + 15, 190), (x + 16, 230), (x + 1, 230)]), (250, 250, 250))
        flat(c, RRect(x0 + 20, 250, x0 + 290, 360, 2), (250, 230, 180))
    # street
    piece(c, RRect(-10, 360, 910, 612, 0), (200, 186, 166), shadow=LAYER)
    for y in range(380, H, 26):
        off = 0 if (y // 26) % 2 else 30
        for x in range(-60 + off, W, 60):
            flat(c, Thick(x, y, x, y + 26, 1.2), (186, 172, 152))
        flat(c, Thick(0, y, W, y, 1.2), (186, 172, 152))
    # living statue on a crate (left)
    piece(c, RRect(60, 470, 160, 520, 3), (180, 180, 186), border=1.5, shadow=PROP)
    modern(c, 110, 470, (190, 200, 196), bottom=(190, 200, 196), hair=(190, 200, 196), h=2.4)
    flat(c, Thick(118, 370, 150, 340, 4), (190, 200, 196))
    piece(c, Ell(110, 550, 24, 8), (200, 160, 80) if "hat" not in d else (90, 150, 220), border=1, shadow=SMALL)
    # guitarist with an open case (centre)
    modern(c, 450, 500, (90, 60, 120), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.4)
    piece(c, [Ell(446, 444, 18, 14), Thick(458, 440, 500, 410, 5)], (220, 140, 60), border=1, shadow=SMALL)
    piece(c, RRect(390, 520, 520, 556, 8), (40, 40, 50), border=1.2, shadow=PROP)
    flat(c, RRect(398, 526, 512, 550, 6), (200, 60, 70) if "case" not in d else (60, 160, 120))
    flat(c, [Circ(420 + k * 18, 538, 4) for k in range(4)], (250, 210, 80))
    # mic stand + small amp
    flat(c, Thick(380, 500, 380, 420, 2.4), (150, 150, 160))
    piece(c, RRect(340, 470, 372, 500, 3), (40, 40, 46), shadow=SMALL)
    # onlookers
    for k, (x, col, hair, st) in enumerate(((250, (240, 200, 90), (90, 60, 40), "long"), (300, (60, 110, 180), (40, 30, 30), "short"),
                                           (620, (120, 190, 120), (220, 180, 90), "twin"), (680, (220, 110, 150), (40, 30, 30), "long"),
                                           (860, (150, 150, 170), (130, 130, 140), "short"))):
        if k == 3 and "shirt" in d:
            col = (250, 200, 60)
        modern(c, x, 600, col, bottom=(60, 60, 80), hair=hair, h=2.2 if k != 2 else 1.5, style=st)
    # cafe chairs (right)
    piece(c, [Ell(800, 440, 40, 8), RRect(796, 440, 804, 500, 2)], (250, 250, 250), border=1.2, shadow=PROP)
    piece(c, [RRect(746, 450, 770, 500, 3), RRect(830, 450, 854, 500, 3)], (60, 120, 90), border=1, shadow=SMALL)


def juggler(c, m):
    modern(c, 760, 600, (250, 200, 60), bottom=(200, 50, 60), hair=(220, 80, 40), h=2.2, style="twin")


L538_ELEMENTS = [
    E("juggler", juggler, pivot=(760, 600), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.9)),
    E("balls", lambda c, m: [piece(c, Circ(760 + 30 * math.cos(a), 420 + 30 * math.sin(a), 7), col, shadow=SMALL)
                             for a, col in ((0, (240, 80, 80)), (2.1, (80, 200, 120)), (4.2, (80, 140, 240)))],
      pivot=(760, 420), anim=dict(rotateSpeed=160)),
    E("notes", lambda c, m: [flat(c, [Circ(520 + k * 22, 420 - k * 14, 5), Thick(524 + k * 22, 420 - k * 14, 524 + k * 22, 400 - k * 14, 2)], (90, 60, 120))
                             for k in range(3)], anim=dict(driftVelocity=(10, 20), driftLength=50, driftFade=True)),
    E("bubble", lambda c, m: piece(c, Circ(200, 300, 14), (240, 240, 255), border=1, shadow=SMALL),
      anim=dict(driftVelocity=(8, 20), driftLength=120, driftFade=True, phase=0.2)),
]

L538_DIFFS = [
    ("awning", 455, 210, 0),
    ("hat", 110, 550, 0),
    ("case", 455, 538, 0),
    ("shirt", 681, 553, 0),
]


# =================================================================== Level 539 snowy-night bus stop
STEPS539 = [(CLEAR, 8), (SNOW, 16)]
NIGHT = (30, 36, 70)


def l539_bg(c, d):
    c.gradient(0, 360, (20, 26, 60), (60, 60, 100))
    # stars + moon
    rnd = random.Random(5391)
    for _ in range(40):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 200), rnd.choice((1.2, 1.8))), (250, 246, 220))
    piece(c, Circ(780, 70, 26), (250, 244, 220), border=1.5, border_col=NIGHT_EDGE, shadow=None)
    # houses with lit windows
    for k, (x, w, h, col, roof) in enumerate(((-10, 200, 170, (90, 70, 80), (60, 50, 60)), (200, 180, 200, (70, 80, 100), (50, 60, 80)),
                                             (580, 170, 180, (100, 80, 70), (70, 50, 50)), (760, 160, 150, (80, 90, 90), (50, 60, 60)))):
        dpiece(c, RRect(x, 360 - h, x + w, 360, 2), col)
        dpiece(c, Poly([(x - 10, 360 - h + 4), (x + w + 10, 360 - h + 4), (x + w / 2, 360 - h - 50)]), roof if not (k == 3 and "roof" in d) else (150, 60, 60))
        flat(c, Poly([(x - 10, 360 - h + 4), (x + w + 10, 360 - h + 4), (x + w * 0.8, 360 - h - 16), (x + w / 2, 360 - h - 50), (x + w * 0.2, 360 - h - 16)]),
             (230, 236, 250))
        for wx in range(int(x) + 24, int(x + w) - 30, 56):
            win = (255, 210, 120)
            if k == 1 and wx < 260 and "window" in d:
                win = (60, 60, 90)
            flat(c, RRect(wx, 360 - h + 40, wx + 30, 360 - h + 80, 2), win)
    # snow ground
    c.rect(0, 360, W, H, (220, 228, 244))
    for x, y in ((150, 420), (420, 460), (700, 430), (300, 560), (760, 560)):
        flat(c, Ell(x, y, 100, 8), (200, 210, 234))
    # bus stop shelter
    dpiece(c, [RRect(380, 300, 700, 316, 3), RRect(390, 316, 398, 520, 2), RRect(682, 316, 690, 520, 2)], (70, 80, 110))
    flat(c, RRect(398, 316, 682, 500, 0), (120, 150, 200, 0.35))
    flat(c, RRect(380, 292, 700, 302, 4), (240, 244, 252))
    dpiece(c, RRect(620, 340, 676, 440, 3), (240, 120, 160) if "ad" not in d else (110, 200, 220), border=1.2, shadow=SMALL)
    dpiece(c, [RRect(420, 470, 600, 480, 3), RRect(428, 480, 436, 510, 2), RRect(584, 480, 592, 510, 2)], (150, 110, 80))
    # stop sign pole
    dpiece(c, [RRect(316, 300, 324, 520, 2), Circ(320, 290, 24)], (60, 70, 100))
    flat(c, Circ(320, 290, 18), (60, 140, 220) if "stop" not in d else (220, 70, 70))
    flat(c, RRect(310, 284, 330, 296, 2), (250, 250, 250))
    # waiting people
    modern(c, 470, 480, (200, 70, 70), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0)
    flat(c, RRect(456, 380, 488, 386, 2), (250, 250, 250))
    modern(c, 560, 500, (90, 140, 200) if "coat" not in d else (240, 200, 70), bottom=(40, 40, 50), hair=(90, 60, 40), h=2.2, style="long")
    modern(c, 780, 596, (120, 170, 120), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.3, glasses=True)
    piece(c, Ell(130, 560, 30, 22), (240, 244, 252), border=1.5, border_col=NIGHT_EDGE, shadow=PROP)          # snowman base
    piece(c, Circ(130, 524, 18), (240, 244, 252), border=1.5, border_col=NIGHT_EDGE, shadow=PROP)
    flat(c, [RRect(116, 486, 144, 508, 2), RRect(110, 504, 150, 510, 2)], (40, 40, 50) if "hat" not in d else (200, 60, 70))
    flat(c, Poly([(132, 524), (148, 528), (132, 530)]), (250, 140, 40))


L539_ELEMENTS = [
    E("glow1", lambda c, m: soft_union(c, [Circ(240, 386, 10)], (255, 220, 140), 0.55, spread=40), daynight="untinted",
      anim=dict(twinkle=0.1, twinkleSpeed=1.0)),
    E("lamp1", lambda c, m: (piece(c, [RRect(237, 400, 243, 600, 2), Ell(240, 392, 12, 8)], (50, 56, 80), border=1, border_col=NIGHT_EDGE, shadow=SMALL),
                             flat(c, Ell(240, 398, 8, 4), (255, 236, 160))), daynight="untinted"),
    E("glow2", lambda c, m: soft_union(c, [Circ(860, 386, 10)], (255, 220, 140), 0.55, spread=40), daynight="untinted",
      anim=dict(twinkle=0.1, twinkleSpeed=1.0, phase=0.5)),
    E("lamp2", lambda c, m: (piece(c, [RRect(857, 400, 863, 600, 2), Ell(860, 392, 12, 8)], (50, 56, 80), border=1, border_col=NIGHT_EDGE, shadow=SMALL),
                             flat(c, Ell(860, 398, 8, 4), (255, 236, 160))), daynight="untinted"),
    E("bus", lambda c, m: (bus_side(c, 0, 600, (60, 120, 200), s=1.1), soft_union(c, [Circ(130, 584, 8)], (255, 240, 180), 0.8, spread=20)),
      anim=dict(drift_across(-150, 150, 60, start=-500))),
    cloud("cloudA", 200, 40, 1.2, (110, 116, 150), W_(SNOW)),
    cloud("cloudB", 560, 30, 1.3, (110, 116, 150), W_(SNOW)),
    snow_layer("snow", 539, 70, 2.0, 4.0, 40),
]

L539_DIFFS = [
    ("window", 240, 220, 0),
    ("ad", 648, 390, 0),
    ("stop", 320, 290, 0),
    ("coat", 561, 428, 0),
    ("roof", 840, 200, 0),
    ("hat", 130, 498, 0),
]


LEVELS = [
    ("Level530", "公交总站", l530_bg, L530_ELEMENTS, L530_DIFFS, 60, OPTS),
    ("Level531", "喷泉广场", l531_bg, L531_ELEMENTS, L531_DIFFS, 60, OPTS),
    ("Level532", "摩天楼擦窗", l532_bg, L532_ELEMENTS, L532_DIFFS, 60, OPTS),
    ("Level533", "立交桥", l533_bg, L533_ELEMENTS, L533_DIFFS, 60, OPTS),
    ("Level534", "停车场", l534_bg, L534_ELEMENTS, L534_DIFFS, 60, OPTS),
    ("Level535", "渡轮码头", l535_bg, L535_ELEMENTS, L535_DIFFS, 60, OPTS),
    ("Level536", "骑楼老街", l536_bg, L536_ELEMENTS, L536_DIFFS, 60, OPTS),
    ("Level537", "社区菜园", l537_bg, L537_ELEMENTS, L537_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS537, blend=3.0), anim_seconds=30.0, frames=80)),
    ("Level538", "街头艺人", l538_bg, L538_ELEMENTS, L538_DIFFS, 60, OPTS),
    ("Level539", "雪夜车站", l539_bg, L539_ELEMENTS, L539_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS539, blend=3.0), anim_seconds=24.0, frames=80)),
]
