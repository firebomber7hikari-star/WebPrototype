# -*- coding: utf-8 -*-
"""Everyday-town themes (paper-craft side views, full-bleed, no real brands or logos):
  Level500 动物园   - a zoo: giraffe yard, elephant pool, lion rock, visitors, balloon seller, ice-cream cart
  Level501 机场     - an airport terminal: glass wall onto the apron, airliners, control tower, departures board, travellers
  Level502 超市     - a supermarket: shelf aisles, fruit stand, checkout, shoppers with a trolley
  Level503 学校操场 - a schoolyard: clock-tower school, swings, slide, sandbox, basketball hoop
  Level504 消防站   - a fire station: three bays, fire engine rolling out, hose tower, firefighters, station dog
  Level505 面包店   - a bakery: bread shelves, chalkboard menu, brick oven, cake case, cafe table
  Level506 湖畔公园 - a lakeside park: arched bridge, gazebo, blossom trees, rowing boat, ducks; rain showers
  Level507 滑雪场   - a ski resort: chairlift, lodge, slalom flags, snowman, skiers; snow and fog
  Level508 海边灯塔 - a seaside lighthouse: cliff, fishing village, pier, sailboat; day / night with the lighthouse beam
  Level509 图书馆   - a library: tall bookcases with a rolling ladder, arched window, reading table, globe, sleeping cat
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from fdcore import CLEAR, FOG, OVERCAST, RAIN, SNOW, W_
from kit import house, tree_pine
from stylekit import celestial, day_night, moon_element, star_field, sun_element, window_glow
from weather import cloud, fog_layer, paper_sun, puddles, rain_layer, snow_layer, splash_rings

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


# =================================================================== shared props
def balloon_bunch(x, y, cols, string_to=None):
    """Balloons on strings (drawn as one element so they bob together)."""
    def d(c, m):
        sx, sy = string_to or (x, y + 70)
        for k, col in enumerate(cols):
            bx, by = x + (k - (len(cols) - 1) / 2) * 16, y - abs(k - (len(cols) - 1) / 2) * 6
            flat(c, Thick(sx, sy, bx, by + 12, 1), (90, 90, 100))
            piece(c, [Ell(bx, by, 10, 12), Poly([(bx - 3, by + 13), (bx + 3, by + 13), (bx, by + 9)])], col, border=1, shadow=SMALL)
            flat(c, Ell(bx - 3, by - 4, 2.5, 4), lit(col, 1.35))
    return d


def path_tiles(c, y0, y1, col, line, step=60, seed=0):
    c.rect(0, y0, W, y1, col)
    rnd = random.Random(seed)
    for y in range(int(y0) + 18, int(y1), 26):
        off = rnd.uniform(0, step)
        for x in range(-int(step), W + int(step), step):
            flat(c, Thick(x + off, y, x + off + step * 0.55, y, 1.2), line)


# =================================================================== Level 500 zoo
def giraffe(c, x, base, s=1.0, body=(240, 190, 90), spots=(170, 100, 50), show_spots=True):
    legs = [RRect(x + dx * s - 3 * s, base - 50 * s, x + dx * s + 3 * s, base, 2) for dx in (-22, -12, 14, 24)]
    piece(c, legs, body, border=1.5, shadow=PROP)
    piece(c, [Ell(x, base - 58 * s, 34 * s, 16 * s), Poly([(x + 18 * s, base - 70 * s), (x + 30 * s, base - 62 * s),
                                                      (x + 52 * s, base - 150 * s), (x + 42 * s, base - 154 * s)]),
              Ell(x + 56 * s, base - 154 * s, 15 * s, 8 * s)], body, border=1.5, shadow=PROP)
    flat(c, [Thick(x + 44 * s, base - 160 * s, x + 42 * s, base - 172 * s, 2.4 * s), Thick(x + 52 * s, base - 160 * s, x + 52 * s, base - 172 * s, 2.4 * s)],
         spots)
    flat(c, [Circ(x + 42 * s, base - 172 * s, 3 * s), Circ(x + 52 * s, base - 172 * s, 3 * s)], spots)
    flat(c, Circ(x + 58 * s, base - 157 * s, 1.8 * s), INK)
    flat(c, Ell(x + 34 * s, base - 150 * s, 5 * s, 3 * s), body)                                  # ear
    if show_spots:
        rnd = random.Random(500)
        pts = [(x + rnd.uniform(-26, 26) * s, base - 58 * s + rnd.uniform(-9, 9) * s) for _ in range(9)]
        pts += [(x + (24 + t * 24) * s + rnd.uniform(-3, 3) * s, base - (78 + t * 64) * s) for t in (0.1, 0.35, 0.6, 0.85)]
        flat(c, [Ell(px, py, 5 * s, 4 * s) for px, py in pts], spots)
    flat(c, Thick(x - 34 * s, base - 60 * s, x - 42 * s, base - 36 * s, 2), spots)                # tail


def elephant(c, x, base, s=1.0, col=(160, 160, 176), ear=None, tusk=True):
    ear = ear or lit(col, 0.88)
    legs = [RRect(x + dx * s - 8 * s, base - 40 * s, x + dx * s + 8 * s, base, 4 * s) for dx in (-34, -16, 14, 32)]
    piece(c, legs, col, border=1.5, shadow=PROP)
    piece(c, [Ell(x, base - 52 * s, 52 * s, 32 * s), Circ(x + 50 * s, base - 66 * s, 24 * s),
              Thick(x + 66 * s, base - 60 * s, x + 78 * s, base - 30 * s, 11 * s), Thick(x + 78 * s, base - 30 * s, x + 88 * s, base - 22 * s, 8 * s)],
          col, border=1.5, shadow=PROP)
    piece(c, Ell(x + 36 * s, base - 62 * s, 16 * s, 22 * s), ear, border=1.2, shadow=SMALL)
    flat(c, Circ(x + 60 * s, base - 72 * s, 2 * s), INK)
    if tusk:
        flat(c, Poly([(x + 58 * s, base - 50 * s), (x + 64 * s, base - 50 * s), (x + 80 * s, base - 40 * s)]), (252, 248, 236))
    flat(c, Thick(x - 52 * s, base - 56 * s, x - 60 * s, base - 30 * s, 2.4), lit(col, 0.75))


def lion(c, x, base, s=1.0, body=(226, 176, 96), mane=(170, 96, 40)):
    piece(c, [RRect(x + dx * s - 5 * s, base - 26 * s, x + dx * s + 5 * s, base, 3 * s) for dx in (-26, -14, 16, 26)] +
          [Ell(x, base - 30 * s, 34 * s, 14 * s), Thick(x - 34 * s, base - 30 * s, x - 52 * s, base - 46 * s, 3 * s)], body, border=1.5, shadow=PROP)
    flat(c, Circ(x - 52 * s, base - 48 * s, 5 * s), mane)
    piece(c, [Circ(x + 34 * s, base - 46 * s, 20 * s)] + [Circ(x + 34 * s + 18 * s * math.cos(a), base - 46 * s + 18 * s * math.sin(a), 7 * s)
                                                         for a in [k * math.pi / 5 for k in range(10)]], mane, border=1.5, shadow=PROP)
    flat(c, Circ(x + 38 * s, base - 46 * s, 12 * s), body)
    flat(c, [Circ(x + 42 * s, base - 50 * s, 1.8 * s), Ell(x + 48 * s, base - 42 * s, 3 * s, 2 * s)], INK)


def l500_bg(c, d):
    sky(c, (126, 192, 238), (214, 234, 246), 260)
    cloud_bank(c, 112, (250, 250, 246), 5001, k=0.8)
    cloud_bg(c, 600, 60, 0.7)
    far_ridge(c, 200, 50, (160, 196, 186), 5002)
    far_round_trees(c, 236, 22, (110, 168, 120), 5003)
    # yards: grass with a moat-pool in the middle
    piece(c, Poly([(-10, 236), (910, 236), (910, 470), (-10, 470)]), (150, 196, 100), shadow=LAYER)
    for k, x in enumerate(range(-40, 940, 70)):
        flat(c, Ell(x, 300 + (k % 3) * 40, 40, 10), (140, 188, 94))
    # giraffe yard: acacia + feeding platform
    piece(c, [Thick(60, 400, 72, 250, 8), Thick(66, 300, 30, 260, 5), Thick(70, 280, 108, 236, 5)], (130, 92, 64), shadow=PROP)
    piece(c, [Ell(70, 236, 70, 18), Ell(30, 258, 40, 12), Ell(116, 232, 38, 12)], (96, 150, 80), shadow=PROP)
    piece(c, [RRect(250, 300, 262, 420, 2), RRect(232, 292, 300, 306, 2)], (170, 130, 90), shadow=PROP)
    piece(c, [Ell(266, 286, 30, 14)], (190, 200, 100), shadow=SMALL)                                  # hay on the platform
    giraffe(c, 170, 420, s=1.25, show_spots="spots" not in d)
    # elephant pool
    piece(c, Ell(470, 420, 150, 34), (110, 170, 210), border=2, shadow=SMALL)
    flat(c, [Ell(430, 414, 50, 6), Ell(520, 428, 40, 5)], (150, 200, 230))
    elephant(c, 450, 404, s=1.25, ear=(236, 150, 170) if "ear" in d else None)
    elephant(c, 580, 360, s=0.7)
    # lion rock
    piece(c, Poly([(650, 440), (680, 330), (760, 300), (860, 320), (910, 380), (910, 440)]), (190, 170, 150), border=2, shadow=PROP)
    flat(c, Poly([(760, 300), (860, 320), (910, 380), (910, 440), (800, 440)]), (170, 150, 132))
    lion(c, 770, 316, s=1.2, mane=(90, 60, 40) if "mane" in d else (170, 96, 40))
    # enclosure fences
    for x in range(-10, 920, 24):
        flat(c, Thick(x, 470, x, 436, 3), (120, 96, 72))
    flat(c, [Thick(-10, 444, 910, 444, 4), Thick(-10, 460, 910, 460, 4)], (140, 110, 80))
    # visitor path
    path_tiles(c, 470, H, (232, 214, 182), (210, 190, 160), seed=500)
    # info sign (giraffe icon) and signpost
    piece(c, [Thick(330, 470, 330, 400, 4), RRect(300, 360, 360, 404, 4)], (110, 80, 60), border=1.5, shadow=PROP)
    flat(c, RRect(306, 366, 354, 398, 3), (250, 220, 120) if "sign" not in d else (120, 200, 240))
    flat(c, [Thick(318, 392, 334, 374, 3), Circ(336, 372, 4)], (150, 100, 50))
    # bushes along the path
    for x, s in ((20, 1.3), (880, 1.2)):
        bush(c, x, 500, s=s, col=(90, 156, 90))
    # ice-cream cart
    piece(c, [RRect(560, 500, 660, 560, 6)], (250, 250, 252), border=1.5, shadow=PROP)
    flat(c, [RRect(560, 520, 660, 530, 0)], (240, 130, 160))
    piece(c, [Circ(578, 566, 10), Circ(642, 566, 10)], (60, 60, 70), shadow=SMALL)
    flat(c, Thick(610, 500, 610, 430, 3), (140, 140, 150))
    umb = (120, 200, 240) if "umbrella" in d else (240, 120, 150)
    piece(c, Poly([(552, 440), (668, 440), (610, 404)]), umb, border=1.5, shadow=PROP)
    flat(c, [Poly([(590, 440), (610, 404), (600, 440)]), Poly([(630, 440), (610, 404), (640, 440)])], (250, 250, 252))
    for k, col in enumerate(((250, 230, 170), (240, 160, 180), (170, 120, 90))):
        flat(c, [Circ(580 + k * 18, 498, 7)], col)
    modern(c, 690, 560, (250, 250, 252), bottom=(80, 90, 120), hair=(90, 60, 40), h=1.6)
    # visitors
    modern(c, 110, 572, (240, 120, 60), bottom=(60, 70, 110), hair=(40, 30, 30), h=1.9)
    modern(c, 150, 580, (90, 160, 220), bottom=(60, 60, 80), hair=(220, 180, 90), h=1.3, style="twin")
    modern(c, 260, 590, (120, 190, 120) if "shirt" not in d else (250, 210, 60), bottom=(80, 70, 60), hair=(40, 30, 30), h=1.8, style="long",
           skirt=True)
    modern(c, 450, 580, (200, 90, 120), bottom=(50, 60, 90), hair=(90, 60, 40), h=1.8, bag=(240, 200, 90))
    modern(c, 820, 586, (60, 80, 120), bottom=(40, 40, 50), hair=(240, 240, 246), h=1.9, glasses=True)
    # balloon seller's cart base
    piece(c, [RRect(354, 560, 400, 590, 4)], (250, 200, 80), border=1.5, shadow=PROP)
    modern(c, 380, 560, (250, 120, 100), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.3)
    # bin
    piece(c, [RRect(770, 520, 800, 566, 4)], (90, 150, 110) if "bin" not in d else (230, 120, 80), border=1.5, shadow=PROP)
    flat(c, RRect(766, 516, 804, 524, 2), (60, 100, 80))


L500_ELEMENTS = [
    E("balloons", balloon_bunch(386, 486, [(240, 80, 90), (250, 200, 60), (90, 170, 240), (130, 210, 120)], string_to=(388, 540)),
      pivot=(388, 540), anim=dict(swingAngle=6, swingSpeed=0.5)),
    E("flamingo", lambda c, m: (flat(c, [Thick(40, 436, 40, 406, 1.5)], (230, 120, 140)),
                                piece(c, [Ell(36, 398, 12, 7), Thick(44, 396, 48, 376, 2.4), Circ(48, 374, 4)], (240, 150, 170), shadow=SMALL)),
      pivot=(40, 436), anim=dict(swingAngle=4, swingSpeed=0.3)),
    E("trunk_spray", lambda c, m: soft_union(c, [Circ(570, 352, 6)], (190, 225, 250), 0.8, spread=6),
      anim=dict(driftVelocity=(14, -26), driftLength=40, driftFade=True, driftGrow=1.6)),
    bird_el("bird1", 300, 70, s=8, speed=24),
    cloud_el("cloud1", 240, 40, 0.6, 8),
]

L500_DIFFS = [
    ("spots", 180, 330, 0),
    ("ear", 495, 340, 0),
    ("mane", 812, 260, 0),
    ("sign", 330, 382, 0),
    ("umbrella", 610, 425, 0),
    ("shirt", 262, 545, 0),
    ("bin", 785, 540, 0),
]


# =================================================================== Level 501 airport terminal
def airliner(c, x, y, s, body=(250, 250, 252), tail=(60, 120, 210), stripe=None, face_right=True):
    d = 1 if face_right else -1
    stripe = stripe or tail
    piece(c, [RRect(x - 120 * s, y - 14 * s, x + 110 * s, y + 14 * s, 14 * s),
              Poly([(x + 96 * d * s, y - 14 * s), (x + 132 * d * s, y), (x + 96 * d * s, y + 14 * s)])], body, border=1.5, shadow=PROP)
    piece(c, Poly([(x - 100 * d * s, y - 12 * s), (x - 126 * d * s, y - 60 * s), (x - 108 * d * s, y - 60 * s), (x - 70 * d * s, y - 12 * s)]), tail,
          border=1.5, shadow=SMALL)
    piece(c, Poly([(x - 10 * d * s, y + 4 * s), (x - 50 * d * s, y + 30 * s), (x - 30 * d * s, y + 30 * s), (x + 30 * d * s, y + 4 * s)]),
          lit(body, 0.9), border=1.2, shadow=SMALL)
    flat(c, RRect(x - 110 * s, y + 2 * s, x + 120 * s, y + 6 * s, 2), stripe)
    for k in range(12):
        flat(c, Circ(x - 80 * s + k * 15 * s, y - 4 * s, 2.4 * s), (90, 140, 190))
    flat(c, Poly([(x + 112 * d * s, y - 8 * s), (x + 124 * d * s, y - 4 * s), (x + 112 * d * s, y - 2 * s)]), (60, 80, 110))
    piece(c, [Ell(x - 4 * d * s, y + 20 * s, 14 * s, 6 * s)], (200, 204, 214), shadow=SMALL)     # engine


def traveller(c, x, base, top, case, h=1.8, hair=(40, 30, 30), style="short", right=True):
    modern(c, x, base, top, bottom=(60, 64, 80), hair=hair, h=h, style=style)
    cx = x + (16 if right else -26) * h
    piece(c, [RRect(cx, base - 22 * h, cx + 12 * h, base - 2 * h, 2)], case, border=1.2, shadow=SMALL)
    flat(c, Thick(cx + 6 * h, base - 22 * h, cx + 6 * h, base - 32 * h, 1.4), (60, 60, 70))
    flat(c, [Circ(cx + 2 * h, base - 1 * h, 1.6 * h), Circ(cx + 10 * h, base - 1 * h, 1.6 * h)], (40, 40, 46))


def l501_bg(c, d):
    # outside through the glass: sky, city, apron
    sky(c, (120, 186, 240), (226, 238, 248), 330)
    cloud_bank(c, 130, (250, 250, 248), 5011, k=0.7)
    far_skyline(c, 236, 20, 70, (170, 186, 210), 5012)
    far_ridge(c, 240, 24, (150, 176, 200), 5013)
    c.rect(0, 240, W, 330, (170, 172, 180))
    for x in range(-40, 940, 90):
        flat(c, Thick(x, 286, x + 50, 286, 3), (250, 240, 170))
    # control tower
    piece(c, [Poly([(726, 240), (760, 240), (754, 120), (732, 120)])], (230, 232, 240), border=1.5, shadow=PROP)
    piece(c, [Poly([(712, 120), (774, 120), (766, 92), (720, 92)])], (90, 140, 180) if "cab" not in d else (240, 170, 70), border=1.5, shadow=PROP)
    piece(c, RRect(716, 84, 770, 94, 3), (230, 232, 240), shadow=SMALL)
    flat(c, Thick(743, 84, 743, 62, 2), (120, 120, 130))
    flat(c, Circ(743, 60, 4), (240, 80, 80))
    # parked airliners
    airliner(c, 200, 238, 0.9, tail=(60, 120, 210))
    airliner(c, 560, 262, 1.05, tail=(240, 120, 60) if "tail" not in d else (130, 90, 200), stripe=(240, 120, 60),
             face_right=False)
    # tug + baggage carts
    piece(c, RRect(330, 300, 370, 322, 4), (250, 200, 60), border=1.2, shadow=SMALL)
    for k in range(3):
        piece(c, RRect(380 + k * 40, 302, 414 + k * 40, 322, 3), (120, 130, 150), border=1.2, shadow=SMALL)
        flat(c, RRect(384 + k * 40, 296, 410 + k * 40, 304, 2), [(240, 120, 90), (90, 150, 220), (240, 200, 80)][k])
    # glass wall frame
    for x in range(0, 901, 150):
        piece(c, RRect(x - 6, 0, x + 6, 340, 1), (90, 96, 110), shadow=SMALL)
    piece(c, RRect(-10, 0, 910, 14, 0), (90, 96, 110), shadow=SMALL)
    for x in range(-10, 910, 150):
        flat(c, Poly([(x + 20, 20), (x + 60, 20), (x + 20, 120)]), (255, 255, 255, 0.18))
    # terminal floor and back wall strip
    piece(c, RRect(-10, 336, 910, 352, 0), (200, 204, 214), shadow=LAYER)
    c.rect(0, 352, W, H, (226, 222, 214))
    for y in range(372, H, 34):
        flat(c, Thick(0, y, W, y, 1.2), (210, 206, 198))
    for x in range(-200, 1100, 70):
        flat(c, Thick(x, 352, x - 160, H, 1.2), (210, 206, 198))
    # departures board (hanging)
    for x in (300, 600):
        flat(c, Thick(x, 14, x, 60, 2), (90, 96, 110))
    piece(c, RRect(260, 60, 640, 168, 6), (40, 44, 56), border=2, shadow=PROP)
    for k in range(5):
        y = 74 + k * 18
        flat(c, RRect(272, y, 300, y + 12, 2), (250, 200, 60))
        sign_box(c, 310, y, 520, y + 12, (220, 226, 240), 5014 + k, vertical=False)
        stat = (90, 220, 120) if k != 2 else (240, 90, 80)
        if k == 2 and "status" in d:
            stat = (90, 220, 120)
        flat(c, RRect(540, y, 626, y + 12, 2), stat)
    # check-in desk (left) with agent
    modern(c, 90, 420, (60, 90, 150), bottom=(40, 40, 60), hair=(90, 60, 40), h=1.8, style="long")
    piece(c, RRect(10, 400, 190, 470, 4), (240, 238, 232), border=1.5, shadow=PROP)
    flat(c, RRect(10, 400, 190, 412, 3), (60, 120, 200) if "desk" not in d else (230, 90, 110))
    piece(c, RRect(110, 380, 150, 402, 2), (60, 60, 70), shadow=SMALL)
    # conveyor with a suitcase
    flat(c, RRect(190, 440, 250, 470, 2), (90, 96, 110))
    piece(c, RRect(200, 418, 236, 444, 3), (240, 160, 60), border=1.2, shadow=SMALL)
    # potted plants
    for x in (300, 870):
        piece(c, Poly([(x - 18, 520), (x + 18, 520), (x + 14, 556), (x - 14, 556)]), (200, 120, 90), border=1.2, shadow=PROP)
        piece(c, [Ell(x, 500, 22, 28), Ell(x - 16, 486, 12, 20), Ell(x + 16, 488, 12, 20)], (80, 150, 90), shadow=SMALL)
    # seating row
    for k in range(4):
        x = 640 + k * 50
        piece(c, [RRect(x, 470, x + 44, 506, 6), RRect(x, 500, x + 44, 512, 3)], (70, 130, 190), border=1.2, shadow=PROP)
    flat(c, [Thick(650, 512, 650, 540, 3), Thick(820, 512, 820, 540, 3)], (120, 120, 130))
    modern(c, 720, 506, (230, 120, 60), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.4)
    # travellers
    traveller(c, 380, 560, (200, 70, 80), (60, 140, 210), h=2.0, hair=(220, 180, 90), style="long")
    traveller(c, 480, 590, (60, 160, 120), (240, 200, 60) if "case" not in d else (220, 80, 150), h=2.1)
    traveller(c, 590, 580, (240, 200, 90), (90, 90, 110), h=1.9, hair=(90, 60, 40), right=False)
    # wall clock
    piece(c, Circ(850, 400, 26), (250, 250, 252) if "clock" not in d else (250, 220, 110), border=1.5, shadow=PROP)
    c.ellipse_ring(850, 400, 26, 26, 3, (60, 60, 70))
    flat(c, [Thick(850, 400, 850, 382, 2.4), Thick(850, 400, 864, 404, 2.4)], (40, 40, 50))


def plane_takeoff(c, m):
    airliner(c, 0, 222, 0.45, tail=(90, 180, 120))


L501_ELEMENTS = [
    E("takeoff", plane_takeoff, anim=dict(drift_across(-60, 60, 40, start=300), driftVelocity=(40, -2))),
    bird_el("bird", 420, 40, s=7, speed=-22),
    E("cart", lambda c, m: (piece(c, RRect(0, 296, 36, 318, 4), (250, 250, 252), border=1.2, shadow=SMALL),
                            piece(c, [Circ(8, 320, 4), Circ(28, 320, 4)], (40, 40, 46), shadow=None)),
      anim=dict(drift_across(0, 36, 30, start=820))),
    E("windsock", lambda c, m: (flat(c, Thick(880, 240, 880, 196, 2), (200, 200, 210)),
                                piece(c, Poly([(881, 196), (910, 200), (910, 208), (881, 212)]), (250, 130, 50), border=1, shadow=SMALL)),
      pivot=(880, 204), anim=dict(swingAngle=8, swingSpeed=0.6)),
]

L501_DIFFS = [
    ("cab", 743, 106, 0),
    ("tail", 655, 228, 0),
    ("status", 583, 116, 0),
    ("desk", 100, 406, 0),
    ("case", 528, 568, 0),
    ("clock", 850, 400, 0),
]


# =================================================================== Level 502 supermarket
GOODS = [(230, 80, 80), (250, 200, 60), (90, 160, 230), (110, 190, 110), (240, 140, 60), (200, 120, 200), (250, 250, 250), (130, 90, 70)]


def shelf_unit(c, x0, x1, y0, y1, seed, rows=4, swap=None):
    """Tall store shelf with rows of boxes / bottles; swap=(row, i0, i1, col) recolours a run of items."""
    piece(c, RRect(x0, y0, x1, y1, 3), (200, 206, 216), border=2, shadow=PROP)
    flat(c, RRect(x0 + 6, y0 + 6, x1 - 6, y1 - 6, 2), (236, 238, 242))
    rnd = random.Random(seed)
    h = (y1 - y0 - 12) / rows
    for r in range(rows):
        base = y0 + 6 + (r + 1) * h
        flat(c, RRect(x0 + 2, base - 6, x1 - 2, base, 1), (170, 176, 190))
        x, i = x0 + 10, 0
        while x < x1 - 22:
            kind = rnd.random()
            col = rnd.choice(GOODS)
            run = rnd.randint(2, 4)
            for _ in range(run):
                if x > x1 - 22:
                    break
                cc = swap[3] if swap and swap[0] == r and swap[1] <= i <= swap[2] else col
                if kind < 0.5:
                    piece(c, RRect(x, base - h * 0.7, x + 14, base - 6, 1.5), cc, border=0.8, shadow=SMALL)
                    flat(c, RRect(x + 2, base - h * 0.5, x + 12, base - h * 0.36, 1), lit(cc, 1.3))
                else:
                    piece(c, [RRect(x + 2, base - h * 0.6, x + 12, base - 6, 3), RRect(x + 5, base - h * 0.78, x + 9, base - h * 0.55, 1)], cc,
                          border=0.8, shadow=SMALL)
                x += 16
                i += 1
            x += 4


def l502_bg(c, d):
    c.rect(0, 0, W, 420, (244, 238, 226))
    # ceiling with light strips
    c.rect(0, 0, W, 40, (226, 228, 234))
    for x in range(30, 900, 170):
        flat(c, RRect(x, 14, x + 110, 24, 4), (255, 252, 236))
        soft_union(c, [RRect(x, 14, x + 110, 24, 4)], (255, 250, 220), 0.4, spread=14)
    # aisle category boards
    for i, (x, col) in enumerate(((160, (230, 90, 80)), (450, (90, 160, 90)), (740, (70, 130, 210)))):
        flat(c, [Thick(x - 40, 40, x - 40, 58, 1.5), Thick(x + 40, 40, x + 40, 58, 1.5)], (130, 130, 140))
        cc = col if not (i == 1 and "board" in d) else (240, 170, 60)
        piece(c, RRect(x - 70, 58, x + 70, 92, 5), cc, border=1.5, shadow=PROP)
        sign_box(c, x - 52, 66, x + 52, 84, (250, 250, 250), 5020 + i, vertical=False)
    # three shelf units
    shelf_unit(c, 20, 300, 110, 400, 5021)
    shelf_unit(c, 310, 590, 110, 400, 5022, swap=(1, 3, 6, (240, 120, 200)) if "goods" in d else None)
    shelf_unit(c, 600, 880, 110, 400, 5023)
    # floor
    c.rect(0, 400, W, H, (226, 226, 222))
    for y in range(400, H, 40):
        for x in range(0, W, 40):
            if (x // 40 + y // 40) % 2:
                flat(c, RRect(x, y, x + 40, y + 40, 0), (214, 214, 212))
    # fruit stand (left)
    piece(c, Poly([(10, 470), (250, 470), (240, 560), (20, 560)]), (190, 140, 90), border=2, shadow=PROP)
    for k in range(3):
        flat(c, Thick(16 + k * 0, 500 + k * 22, 244, 500 + k * 22, 2), (160, 116, 76))
    rnd = random.Random(5024)
    apple = (120, 200, 80) if "apples" in d else (220, 50, 60)
    flat(c, [Circ(30 + i * 13 + (j % 2) * 6, 466 - j * 9, 7) for j in range(3) for i in range(6 - j)], apple)
    flat(c, [Circ(130 + i * 13 + (j % 2) * 6, 466 - j * 9, 7) for j in range(3) for i in range(6 - j)], (250, 150, 40))
    for k in range(4):
        flat(c, Thick(200 + k * 10, 456, 214 + k * 10, 436, 6), (250, 220, 70))
    flat(c, [Circ(204 + k * 10, 456, 2.4) for k in range(4)], (110, 90, 40))
    # checkout (right)
    piece(c, RRect(640, 440, 900, 540, 4), (90, 100, 120), border=2, shadow=PROP)
    flat(c, RRect(640, 440, 900, 452, 3), (60, 66, 80))
    modern(c, 820, 440, (230, 100, 90), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.8, style="long")
    piece(c, [RRect(700, 404, 752, 444, 3)], (60, 64, 76), border=1.2, shadow=SMALL)
    flat(c, RRect(706, 410, 746, 430, 2), (120, 220, 170) if "register" not in d else (250, 130, 90))
    piece(c, RRect(860, 360, 880, 440, 2), (60, 66, 80), shadow=SMALL)
    piece(c, Circ(870, 352, 12), (250, 80, 80) if "lamp" not in d else (80, 200, 120), border=1.2, shadow=SMALL)
    # shopper with a trolley (centre)
    modern(c, 360, 580, (90, 160, 220), bottom=(50, 60, 90), hair=(40, 30, 30), h=2.1)
    piece(c, [RRect(390, 480, 520, 540, 3)], (210, 214, 226), border=1.5, shadow=PROP)
    for x in range(398, 520, 14):
        flat(c, Thick(x, 486, x, 534, 1.4), (170, 176, 190))
    flat(c, Thick(370, 470, 392, 482, 3), (60, 60, 70))
    piece(c, [Circ(404, 560, 9), Circ(506, 560, 9)], (50, 50, 56), shadow=SMALL)
    flat(c, [Thick(400, 540, 404, 552, 2), Thick(510, 540, 506, 552, 2)], (150, 150, 160))
    piece(c, RRect(410, 462, 440, 486, 3), (110, 190, 110), border=1, shadow=SMALL)
    if "bread" not in d:
        piece(c, Ell(474, 476, 26, 11), (220, 170, 100), border=1, shadow=SMALL)
        flat(c, [Thick(462, 470, 466, 480, 1.6), Thick(476, 470, 480, 480, 1.6)], (190, 130, 70))
    # second shopper with basket
    modern(c, 580, 586, (250, 200, 80), bottom=(80, 70, 60), hair=(220, 180, 90), h=2.0, style="long", skirt=True)
    piece(c, RRect(590, 520, 626, 546, 3), (230, 60, 70), border=1.2, shadow=SMALL)
    flat(c, Thick(592, 522, 624, 522, 2), (150, 40, 50))
    # wet floor sign
    piece(c, Poly([(276, 600), (296, 540), (316, 600)]), (250, 210, 50), border=1.5, shadow=PROP)
    flat(c, Thick(296, 562, 296, 580, 3), (40, 40, 50))


L502_ELEMENTS = [
    E("promo1", lambda c, m: (flat(c, Thick(310, 40, 310, 100, 1), (130, 130, 140)),
                              piece(c, Poly(star_pts(310, 120, 22, 12, points=8)), (250, 90, 90), border=1.2, shadow=SMALL),
                              flat(c, Circ(310, 120, 9), (250, 250, 250))),
      pivot=(310, 40), anim=dict(swingAngle=6, swingSpeed=0.4)),
    E("promo2", lambda c, m: (flat(c, Thick(600, 40, 600, 100, 1), (130, 130, 140)),
                              piece(c, Poly(star_pts(600, 120, 22, 12, points=8)), (250, 200, 60), border=1.2, shadow=SMALL),
                              flat(c, Circ(600, 120, 9), (250, 250, 250))),
      pivot=(600, 40), anim=dict(swingAngle=6, swingSpeed=0.45, phase=0.5)),
    E("kid", lambda c, m: modern(c, 210, 590, (240, 120, 60), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.3), pivot=(210, 590),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=1.4, bounce=True)),
]

L502_DIFFS = [
    ("board", 450, 75, 0),
    ("goods", 380, 220, 0),
    ("apples", 55, 457, 0),
    ("register", 726, 420, 0),
    ("lamp", 870, 352, 0),
    ("bread", 474, 476, 0),
]


# =================================================================== Level 503 schoolyard
def l503_bg(c, d):
    sky(c, (130, 196, 240), (220, 238, 248), 220)
    cloud_bg(c, 120, 60, 0.8)
    cloud_bg(c, 780, 44, 0.7)
    far_round_trees(c, 200, 26, (120, 176, 120), 5031)
    # school building
    piece(c, RRect(140, 110, 760, 330, 3), (246, 226, 196), border=2, shadow=PROP)
    piece(c, RRect(130, 100, 770, 116, 3), (190, 90, 70), border=1.5, shadow=SMALL)
    for row, y in enumerate((136, 236)):
        for k in range(8):
            x = 160 + k * 74
            if 380 < x < 520:
                continue
            curtain = (250, 250, 250)
            if row == 0 and k == 1 and "curtain" in d:
                curtain = (250, 150, 170)
            flat(c, RRect(x, y, x + 52, y + 56, 2), (150, 200, 230))
            flat(c, [RRect(x, y, x + 12, y + 56, 2), RRect(x + 40, y, x + 52, y + 56, 2)], curtain)
            flat(c, Thick(x, y + 28, x + 52, y + 28, 2), (200, 180, 150))
    # clock tower + entrance
    piece(c, RRect(390, 30, 510, 330, 3), (240, 214, 180), border=2, shadow=PROP)
    piece(c, Poly([(380, 34), (520, 34), (450, -10)]), (190, 90, 70) if "roof" not in d else (70, 120, 190), border=2, shadow=PROP)
    piece(c, Circ(450, 84, 30), (250, 250, 252), border=1.5, shadow=SMALL)
    c.ellipse_ring(450, 84, 30, 30, 3, (90, 70, 60))
    flat(c, [Thick(450, 84, 450, 64, 3), Thick(450, 84, 466, 92, 3)], (60, 50, 50))
    piece(c, RRect(414, 250, 486, 330, 30), (150, 100, 70), border=1.5, shadow=SMALL)
    flat(c, Thick(450, 252, 450, 330, 2), (120, 80, 56))
    piece(c, RRect(400, 140, 500, 168, 3), (60, 130, 90), border=1.2, shadow=SMALL)
    sign_box(c, 412, 146, 488, 162, (250, 250, 250), 5032, vertical=False)
    # yard
    piece(c, RRect(-10, 330, 910, 612, 0), (214, 186, 140), shadow=LAYER)
    for k in range(30):
        rnd = random.Random(5033 + k)
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(350, 600), rnd.uniform(10, 30), 3), (204, 176, 130))
    # trees on both ends
    tree_round(c, 70, 340, s=1.6, col=(90, 160, 90))
    tree_round(c, 840, 340, s=1.6, col=(90, 160, 90) if "tree" not in d else (230, 150, 60))
    # running-track line
    c.ellipse_ring(450, 470, 420, 70, 3, (250, 250, 246))
    # swing frame (left)
    piece(c, [Thick(60, 520, 90, 390, 5), Thick(120, 520, 90, 390, 5), Thick(200, 520, 230, 390, 5), Thick(260, 520, 230, 390, 5),
              Thick(84, 392, 236, 392, 6)], (220, 80, 70), shadow=PROP)
    # slide (centre right)
    piece(c, [Thick(560, 520, 560, 420, 5), Thick(600, 520, 600, 420, 5)], (150, 150, 160), shadow=PROP)
    for y in range(430, 520, 16):
        flat(c, Thick(560, y, 600, y, 3), (150, 150, 160))
    piece(c, RRect(550, 412, 612, 424, 3), (150, 150, 160), shadow=SMALL)
    piece(c, Poly([(606, 414), (620, 414), (700, 510), (700, 524), (684, 524)]), (250, 200, 60) if "slide" not in d else (90, 190, 120),
          border=1.5, shadow=PROP)
    # sandbox with bucket
    piece(c, RRect(300, 520, 440, 560, 4), (180, 130, 90), border=1.5, shadow=PROP)
    flat(c, RRect(308, 524, 432, 552, 3), (240, 220, 160))
    if "bucket" not in d:
        piece(c, Poly([(400, 520), (424, 520), (420, 544), (404, 544)]), (60, 150, 230), border=1.2, shadow=SMALL)
        flat(c, Thick(402, 520, 422, 520, 2), (40, 110, 190))
    modern(c, 350, 544, (240, 120, 160), bottom=(70, 80, 120), hair=(90, 60, 40), h=1.2, style="twin")
    # basketball hoop (right)
    piece(c, [RRect(776, 380, 786, 560, 2)], (120, 120, 130), shadow=PROP)
    piece(c, RRect(734, 372, 794, 412, 3), (250, 250, 252), border=1.5, shadow=PROP)
    flat(c, RRect(752, 390, 776, 406, 1), (220, 80, 60))
    c.ellipse_ring(756, 416, 16, 4, 2.5, (230, 100, 50))
    # kids and a teacher
    modern(c, 480, 590, (90, 150, 220), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.6)
    modern(c, 660, 594, (250, 220, 90) if "shirt" not in d else (160, 100, 220), bottom=(60, 70, 110), hair=(220, 180, 90), h=1.6, style="long",
           skirt=True)
    modern(c, 260, 596, (120, 160, 120), bottom=(70, 60, 60), hair=(130, 130, 140), h=2.2, glasses=True)
    flat(c, Thick(276, 520, 296, 512, 2), (60, 60, 70))
    # schoolbags on the bench
    piece(c, [RRect(820, 540, 900, 552, 3), RRect(828, 552, 836, 576, 2), RRect(884, 552, 892, 576, 2)], (170, 120, 80), shadow=PROP)
    piece(c, RRect(830, 512, 856, 540, 5), (220, 60, 60), border=1.2, shadow=SMALL)
    piece(c, RRect(860, 516, 884, 540, 5), (60, 120, 210), border=1.2, shadow=SMALL)


def swing_seat(x, kid=None):
    def d(c, m):
        flat(c, [Thick(x - 14, 392, x - 14, 486, 1.5), Thick(x + 14, 392, x + 14, 486, 1.5)], (90, 90, 100))
        piece(c, RRect(x - 18, 484, x + 18, 492, 2), (240, 200, 60), border=1, shadow=SMALL)
        if kid:
            modern(c, x, 500, kid, bottom=(60, 70, 110), hair=(40, 30, 30), h=1.1)
    return d


L503_ELEMENTS = [
    E("swing1", swing_seat(130, kid=(240, 140, 60)), pivot=(130, 392), anim=dict(swingAngle=16, swingSpeed=0.5)),
    E("swing2", swing_seat(190), pivot=(190, 392), anim=dict(swingAngle=6, swingSpeed=0.5, phase=0.3)),
    E("flag", lambda c, m: (flat(c, Thick(620, 330, 620, 160, 3), (190, 190, 200)),
                            piece(c, Poly([(621, 162), (680, 172), (621, 196)]), (230, 70, 70), border=1.2, shadow=SMALL)),
      pivot=(620, 180), anim=dict(stretch=(0.12, 0), scaleSpeed=1.2)),
    E("ball", lambda c, m: (piece(c, Circ(520, 520, 10), (240, 130, 50), shadow=SMALL), flat(c, Thick(510, 520, 530, 520, 1.2), (120, 60, 30))),
      pivot=(520, 530), anim=dict(bobAmplitude=(0, 30), bobSpeed=1.2, bounce=True)),
    bird_el("bird", 300, 30, s=8, speed=18),
]

L503_DIFFS = [
    ("curtain", 260, 164, 0),
    ("roof", 450, 18, 0),
    ("tree", 840, 286, 0),
    ("slide", 650, 466, 0),
    ("bucket", 412, 532, 0),
    ("shirt", 661, 565, 0),
]


# =================================================================== Level 504 fire station
FIRE_RED = (210, 50, 50)


def fire_truck(c, x, base, s=1.0, ladder=True):
    piece(c, [RRect(x - 110 * s, base - 54 * s, x + 70 * s, base - 14 * s, 4), Poly([(x + 70 * s, base - 14 * s), (x + 70 * s, base - 64 * s),
                                                                                  (x + 100 * s, base - 64 * s), (x + 116 * s, base - 40 * s), (x + 116 * s, base - 14 * s)])],
          FIRE_RED, border=1.5, shadow=PROP)
    flat(c, Poly([(x + 78 * s, base - 58 * s), (x + 98 * s, base - 58 * s), (x + 110 * s, base - 40 * s), (x + 78 * s, base - 40 * s)]), (180, 220, 240))
    flat(c, RRect(x - 104 * s, base - 30 * s, x + 110 * s, base - 24 * s, 1), (250, 250, 250))
    for k in range(4):
        flat(c, RRect(x - 98 * s + k * 40 * s, base - 48 * s, x - 66 * s + k * 40 * s, base - 34 * s, 2), lit(FIRE_RED, 0.85))
    if ladder:
        piece(c, [Thick(x - 116 * s, base - 62 * s, x + 66 * s, base - 62 * s, 3), Thick(x - 116 * s, base - 72 * s, x + 66 * s, base - 72 * s, 3)],
              (220, 220, 230), shadow=SMALL)
        flat(c, [Thick(x - 110 * s + k * 16 * s, base - 72 * s, x - 110 * s + k * 16 * s, base - 62 * s, 2) for k in range(12)], (220, 220, 230))
    for wx in (x - 76 * s, x + 80 * s):
        piece(c, Circ(wx, base - 12 * s, 14 * s), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(wx, base - 12 * s, 6 * s), (200, 200, 210))


def firefighter(c, x, base, h=1.8, helmet=(250, 200, 50)):
    modern(c, x, base, (60, 60, 70), bottom=(60, 60, 70), hair=(40, 30, 30), h=h)
    flat(c, [RRect(x - 8 * h, base - 30 * h, x + 8 * h, base - 27 * h, 1), RRect(x - 8 * h, base - 8 * h, x + 8 * h, base - 5 * h, 1)], (250, 230, 90))
    hx, hy = x + 1 * h, base - 46 * h
    piece(c, [Ell(hx, hy - 5 * h, 9 * h, 6 * h), Ell(hx, hy - 1 * h, 12 * h, 2.4 * h)], helmet, border=1.2, shadow=SMALL)


def dalmatian(c, x, base, s=1.0, spots=True):
    piece(c, [RRect(x + dx * s - 3 * s, base - 22 * s, x + dx * s + 3 * s, base, 2) for dx in (-16, -8, 10, 18)] +
          [Ell(x, base - 24 * s, 22 * s, 9 * s), Circ(x + 24 * s, base - 36 * s, 9 * s), Ell(x + 32 * s, base - 33 * s, 6 * s, 4 * s),
           Thick(x - 22 * s, base - 26 * s, x - 32 * s, base - 38 * s, 2.4 * s)], (250, 250, 248), border=1.2, shadow=PROP)
    flat(c, Ell(x + 20 * s, base - 34 * s, 4 * s, 7 * s), (40, 40, 46))
    flat(c, [Circ(x + 27 * s, base - 38 * s, 1.5 * s), Circ(x + 38 * s, base - 33 * s, 2 * s)], INK)
    if spots:
        flat(c, [Circ(x + dx * s, base - 24 * s + dy * s, 4 * s) for dx, dy in ((-12, -3), (-3, 3), (6, -4), (14, 2), (-16, 5), (2, -6))],
             (40, 40, 46))
    flat(c, RRect(x + 16 * s, base - 30 * s, x + 22 * s, base - 26 * s, 1), FIRE_RED)


def l504_bg(c, d):
    sky(c, (130, 190, 236), (230, 236, 244), 260)
    cloud_bank(c, 120, (250, 250, 246), 5041, k=0.7)
    far_skyline(c, 236, 40, 130, (180, 190, 210), 5042, win=(206, 214, 230))
    # hose tower (right)
    piece(c, RRect(720, 40, 800, 330, 2), (190, 80, 70), border=2, shadow=PROP)
    piece(c, Poly([(710, 44), (810, 44), (760, 10)]), (90, 90, 100), border=2, shadow=PROP)
    for y in range(60, 320, 16):
        flat(c, Thick(720, y, 800, y, 1.2), (170, 70, 62))
    flat(c, [RRect(744, 70, 776, 110, 14), RRect(744, 150, 776, 190, 14)], (60, 60, 80))
    piece(c, Circ(760, 236, 16), (240, 200, 60) if "bell" not in d else (120, 180, 230), border=1.2, shadow=SMALL)
    flat(c, Circ(760, 250, 4), (120, 90, 40))
    # station building
    piece(c, RRect(60, 110, 720, 470, 2), (210, 96, 80), border=2, shadow=PROP)
    for y in range(126, 470, 18):
        off = 0 if (y // 18) % 2 else 20
        for x in range(60 + off, 720, 40):
            flat(c, Thick(x, y, x, y + 18, 1), (190, 84, 70))
        flat(c, Thick(60, y, 720, y, 1), (190, 84, 70))
    piece(c, RRect(50, 96, 730, 118, 2), (240, 236, 226), border=1.5, shadow=SMALL)
    piece(c, RRect(250, 130, 530, 172, 4), (240, 236, 226), border=1.5, shadow=SMALL)
    sign_box(c, 266, 140, 514, 162, FIRE_RED, 5043, vertical=False)
    # upper windows with flower boxes
    for k, x in enumerate((100, 200, 580, 660)):
        flat(c, RRect(x, 190, x + 50, 240, 2), (170, 210, 236))
        flat(c, Thick(x + 25, 190, x + 25, 240, 2), (240, 236, 226))
        piece(c, RRect(x - 4, 240, x + 54, 252, 2), (130, 90, 60), shadow=SMALL)
        fl = (250, 120, 160) if not (k == 3 and "flowers" in d) else (250, 220, 70)
        flat(c, [Circ(x + 5 + j * 10, 237, 6) for j in range(5)], fl)
    # three bays: left & right doors closed, centre open with the truck
    for k, x in enumerate((90, 290, 490)):
        piece(c, RRect(x, 280, x + 180, 470, 3), (240, 236, 226), border=1.5, shadow=SMALL)
        if k == 1:
            flat(c, RRect(x + 8, 288, x + 172, 470, 2), (60, 54, 60))
            continue
        door = (230, 226, 216)
        flat(c, RRect(x + 8, 288, x + 172, 470, 2), door)
        for y in range(304, 470, 22):
            flat(c, Thick(x + 8, y, x + 172, y, 1.5), lit(door, 0.85))
        flat(c, RRect(x + 30, 320, x + 150, 344, 2), (150, 190, 220) if not (k == 2 and "door" in d) else (250, 200, 80))
    # apron
    piece(c, RRect(-10, 470, 910, 612, 0), (180, 180, 186), shadow=LAYER)
    for x in range(110, 700, 200):
        flat(c, [Thick(x + 80, 480, x + 80, 600, 3)], (240, 220, 90))
    # trees and side buildings fill the edges
    piece(c, RRect(-10, 160, 56, 470, 2), (200, 190, 170), border=1.5, shadow=PROP)
    piece(c, RRect(810, 120, 910, 470, 2), (210, 200, 186), border=1.5, shadow=PROP)
    for y in (150, 230, 310, 390):
        flat(c, [RRect(830, y, 860, y + 40, 2), RRect(870, y, 900, y + 40, 2)], (170, 200, 226))
    # truck rolling out of the centre bay
    fire_truck(c, 380, 520, s=1.15, ladder="ladder" not in d)
    # hydrant
    hyd = (240, 200, 50) if "hydrant" not in d else (80, 170, 230)
    piece(c, [RRect(36, 520, 64, 572, 6), Ell(50, 520, 14, 8), RRect(26, 534, 74, 546, 3)], hyd, border=1.5, shadow=PROP)
    # firefighters and the station dog
    firefighter(c, 600, 590, h=2.0)
    firefighter(c, 680, 584, h=1.9, helmet=(250, 200, 50) if "helmet" not in d else (250, 250, 250))
    dalmatian(c, 150, 594, s=1.6, spots="spots" not in d)
    # traffic cones
    for x in (820, 870):
        piece(c, Poly([(x - 16, 580), (x + 16, 580), (x + 4, 534), (x - 4, 534)]), (250, 120, 40), border=1.2, shadow=PROP)
        flat(c, Thick(x - 10, 560, x + 10, 560, 4), (250, 250, 250))


L504_ELEMENTS = [
    E("siren", lambda c, m: (flat(c, RRect(472, 432, 492, 444, 3), (240, 60, 60)),
                             soft_union(c, [Circ(482, 438, 8)], (255, 90, 90), 0.6, spread=14)),
      daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=2.0)),
    E("spray", lambda c, m: [soft_union(c, [Circ(730 + k * 18, 500 - k * 10 + k * k * 2, 5)], (170, 210, 250), 0.8, spread=5) for k in range(5)],
      anim=dict(twinkle=0.3, twinkleSpeed=1.4)),
    E("hose", lambda c, m: flat(c, Thick(696, 520, 728, 500, 4), (230, 200, 120)), pivot=(696, 520), anim=dict(swingAngle=3, swingSpeed=0.8)),
    E("tail", lambda c, m: flat(c, Thick(120, 556, 108, 540, 3.6), (250, 250, 248)), pivot=(120, 556), anim=dict(swingAngle=20, swingSpeed=1.6)),
    cloud_el("cloud", 600, 50, 0.6, 7),
]

L504_DIFFS = [
    ("bell", 760, 238, 0),
    ("flowers", 685, 238, 0),
    ("door", 580, 332, 0),
    ("ladder", 330, 450, 0),
    ("hydrant", 50, 546, 0),
    ("helmet", 682, 492, 0),
    ("spots", 150, 556, 0),
]


# =================================================================== Level 505 bakery
WOOD = (176, 122, 80)


def loaf(c, x, y, kind, col=(214, 156, 86)):
    if kind == "round":
        piece(c, Ell(x, y, 18, 12), col, border=1, shadow=SMALL)
        flat(c, [Thick(x - 8, y - 6, x - 4, y + 4, 1.6), Thick(x + 2, y - 6, x + 6, y + 4, 1.6)], lit(col, 0.8))
    elif kind == "baguette":
        piece(c, Thick(x - 30, y, x + 30, y - 6, 11), col, border=1, shadow=SMALL)
        flat(c, [Thick(x - 18 + k * 14, y - 4, x - 12 + k * 14, y, 1.6) for k in range(4)], lit(col, 0.8))
    elif kind == "croissant":
        piece(c, [Ell(x, y, 10, 8), Ell(x - 12, y + 3, 8, 6), Ell(x + 12, y + 3, 8, 6), Ell(x - 20, y + 7, 5, 4), Ell(x + 20, y + 7, 5, 4)],
              (226, 160, 70), border=1, shadow=SMALL)
        flat(c, [Thick(x - 6, y - 6, x - 6, y + 6, 1.2), Thick(x + 6, y - 6, x + 6, y + 6, 1.2)], (190, 120, 50))


def cake(c, x, base, body, top, berry=(220, 50, 70)):
    piece(c, RRect(x - 24, base - 30, x + 24, base, 4), body, border=1.2, shadow=SMALL)
    flat(c, RRect(x - 24, base - 32, x + 24, base - 24, 4), top)
    flat(c, [Ell(x - 24 + k * 8, base - 24, 4, 3) for k in range(7)], top)
    flat(c, Circ(x, base - 36, 5), berry)


def l505_bg(c, d):
    c.rect(0, 0, W, 540, (246, 226, 196))
    for x in range(0, W, 36):
        flat(c, RRect(x, 0, x + 18, 540, 0), (240, 218, 186))
    # wooden shelves of bread (left)
    for k, y in enumerate((120, 200, 280)):
        piece(c, RRect(20, y, 340, y + 10, 2), WOOD, border=1.2, shadow=PROP)
        for i in range(5):
            x = 52 + i * 62
            if k == 0:
                loaf(c, x, y - 10, "round")
            elif k == 1:
                if not (i == 3 and "loaf" in d):
                    loaf(c, x, y - 8, "baguette")
            else:
                loaf(c, x, y - 10, "croissant")
    # chalkboard menu (centre top)
    piece(c, RRect(380, 40, 560, 170, 4), (130, 90, 60), border=1.5, shadow=PROP)
    flat(c, RRect(390, 50, 550, 160, 3), (50, 64, 58))
    sign_box(c, 400, 62, 540, 74, (240, 240, 230), 5051, vertical=False)
    for k in range(3):
        sign_box(c, 400, 92 + k * 20, 500, 102 + k * 20, (230, 230, 220), 5052 + k, vertical=False)
        flat(c, Circ(524, 97 + k * 20, 5), (250, 200, 80))
    chalk = (250, 160, 180) if "chalk" in d else (240, 240, 230)
    flat(c, [Circ(464, 136, 9), Circ(484, 136, 9), Poly([(456, 141), (492, 141), (474, 158)])], chalk)
    # brick oven (right)
    piece(c, Poly([(600, 430), (600, 160), (640, 100), (820, 100), (860, 160), (860, 430)]), (190, 100, 80), border=2, shadow=PROP)
    for y in range(116, 430, 18):
        off = 0 if (y // 18) % 2 else 18
        for x in range(600 + off, 860, 36):
            flat(c, Thick(x, y, x, y + 18, 1), (170, 86, 70))
        flat(c, Thick(600, y, 860, y, 1), (170, 86, 70))
    flat(c, RRect(660, 220, 800, 330, 60), (50, 30, 30))
    flat(c, RRect(660, 300, 800, 330, 4), (90, 60, 50))
    piece(c, RRect(700, 20, 760, 102, 2), (160, 90, 72), border=1.5, shadow=PROP)
    # peel leaning on the oven
    piece(c, [Thick(860, 420, 890, 180, 5), Ell(890, 170, 18, 26)], (200, 160, 110), border=1.2, shadow=PROP)
    # counter with display case
    piece(c, RRect(-10, 420, 620, 530, 3), WOOD, border=2, shadow=PROP)
    piece(c, RRect(20, 344, 580, 424, 4), (220, 236, 240), border=1.5, shadow=PROP)
    flat(c, RRect(28, 352, 572, 416, 3), (236, 246, 248))
    flat(c, Thick(28, 390, 572, 390, 2), (200, 214, 220))
    cake(c, 80, 388, (250, 240, 230), (250, 190, 210))
    cake(c, 170, 388, (130, 80, 60), (90, 50, 40), berry=(250, 250, 250))
    cake(c, 260, 388, (250, 240, 230), (250, 240, 200) if "cake" not in d else (150, 210, 130))
    for k in range(4):
        flat(c, Circ(340 + k * 18, 380, 8), [(250, 180, 200), (190, 230, 160), (250, 220, 130), (200, 170, 230)][k])
    for k in range(5):
        loaf(c, 90 + k * 80, 410, "croissant")
    for x in range(-10, 620, 60):
        flat(c, Thick(x, 440, x, 530, 1.4), lit(WOOD, 0.85))
    # baker behind the counter
    modern(c, 440, 400, (250, 250, 250), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.6)
    piece(c, [RRect(424, 250, 460, 270, 6), Circ(430, 250, 11), Circ(452, 248, 11)], (250, 250, 250), border=1.2, shadow=SMALL)
    flat(c, RRect(426, 306, 456, 344, 3), (90, 150, 220) if "apron" not in d else (230, 120, 80))
    # floor
    c.rect(0, 530, W, H, (190, 150, 110))
    for y in range(540, H, 20):
        flat(c, Thick(0, y, W, y, 1.2), (176, 136, 98))
    # customer + cafe table
    modern(c, 680, 596, (120, 170, 120), bottom=(70, 60, 60), hair=(220, 180, 90), h=2.1, style="long", skirt=True)
    piece(c, [Ell(800, 520, 60, 10), RRect(796, 520, 804, 590, 2), Ell(800, 590, 24, 6)], (240, 240, 236), border=1.5, shadow=PROP)
    piece(c, [RRect(778, 494, 800, 516, 4), Thick(800, 500, 808, 508, 3)], (240, 120, 90) if "cup" not in d else (90, 160, 230), border=1, shadow=SMALL)
    flat(c, Ell(822, 516, 14, 4), (250, 250, 250))
    loaf(c, 824, 506, "croissant")


L505_ELEMENTS = [
    E("fire", lambda c, m: (flat(c, Poly([(690, 300), (700, 260), (714, 282), (730, 240), (746, 280), (760, 258), (770, 300)]), (250, 140, 50)),
                            flat(c, Poly([(706, 300), (720, 276), (730, 290), (744, 270), (754, 300)]), (255, 220, 120))),
      pivot=(730, 300), daynight="untinted", anim=dict(stretch=(0.06, 0.2), scaleSpeed=3.0, twinkle=0.12, twinkleSpeed=2.5)),
    E("lamp1", lambda c, m: (flat(c, Thick(150, 0, 150, 40, 1.5), (90, 80, 70)),
                             piece(c, Poly([(130, 56), (170, 56), (162, 38), (138, 38)]), (90, 150, 120), border=1, shadow=SMALL),
                             soft_union(c, [Ell(150, 60, 14, 5)], (255, 230, 150), 0.6, spread=8)),
      pivot=(150, 0), anim=dict(swingAngle=3, swingSpeed=0.3)),
    E("lamp2", lambda c, m: (flat(c, Thick(320, 0, 320, 18, 1.5), (90, 80, 70)),
                             piece(c, Poly([(300, 34), (340, 34), (332, 16), (308, 16)]), (90, 150, 120), border=1, shadow=SMALL),
                             soft_union(c, [Ell(320, 38, 14, 5)], (255, 230, 150), 0.6, spread=8)),
      pivot=(320, 0), anim=dict(swingAngle=3, swingSpeed=0.3, phase=0.4)),
] + [E("steam%d" % i, (lambda: lambda c, m: soft_union(c, [Circ(790, 486, 5)], (250, 250, 250), 0.7, spread=5))(),
       anim=dict(driftVelocity=(2, -14), driftLength=40, driftFade=True, driftGrow=1.6, phase=i / 3)) for i in range(3)]

L505_DIFFS = [
    ("loaf", 238, 190, 0),
    ("chalk", 474, 144, 0),
    ("cake", 260, 372, 0),
    ("apron", 441, 325, 0),
    ("cup", 790, 505, 0),
]


# =================================================================== Level 506 lakeside park (rain showers)
STEPS506 = [(CLEAR, 12), (OVERCAST, 4), (RAIN, 10), (OVERCAST, 4)]
LAKE = (300, 430)


def blossom_tree(c, x, base, s=1.0, col=(246, 180, 200)):
    piece(c, [Thick(x, base, x, base - 50 * s, 8 * s), Thick(x, base - 40 * s, x - 22 * s, base - 64 * s, 4 * s),
              Thick(x, base - 44 * s, x + 24 * s, base - 70 * s, 4 * s)], (120, 84, 70), shadow=PROP)
    piece(c, [Circ(x - 24 * s, base - 74 * s, 22 * s), Circ(x, base - 88 * s, 28 * s), Circ(x + 26 * s, base - 76 * s, 22 * s),
              Circ(x - 6 * s, base - 64 * s, 20 * s)], col, shadow=PROP)
    flat(c, [Circ(x - 10 * s, base - 96 * s, 9 * s), Circ(x + 20 * s, base - 84 * s, 7 * s)], lit(col, 1.08))


def l506_bg(c, d):
    sky(c, (130, 194, 240), (220, 236, 246), 260)
    far_ridge(c, 170, 60, (170, 200, 200), 5061)
    far_round_trees(c, 236, 26, (110, 170, 120), 5062)
    piece(c, RRect(-10, 236, 910, 612, 0), (150, 200, 110), shadow=LAYER)
    # lake
    piece(c, Ell(450, 366, 440, 70), (110, 176, 214), border=2, shadow=SMALL)
    for x, y, w in ((240, 340, 60), (520, 352, 80), (700, 390, 50), (380, 400, 70)):
        flat(c, Thick(x, y, x + w, y, 2), (160, 206, 232))
    # reeds at the lake edge
    for x in (30, 52, 860, 878):
        flat(c, [Thick(x, 410, x - 3, 360, 2.4), Thick(x + 6, 410, x + 9, 370, 2.4)], (90, 140, 80))
        flat(c, [Ell(x - 3, 364, 3, 8), Ell(x + 9, 374, 3, 8)], (130, 90, 60))
    # arched bridge (left)
    rail = (200, 70, 60) if "bridge" not in d else (80, 140, 200)
    piece(c, Poly([(60, 386)] + [(160 + 100 * math.cos(math.radians(a)), 386 - 50 * math.sin(math.radians(a))) for a in range(180, -1, -15)] +
                  [(260, 386), (260, 396)] + [(160 + 92 * math.cos(math.radians(a)), 396 - 40 * math.sin(math.radians(a))) for a in range(0, 181, 15)] +
                  [(60, 396)]), (230, 210, 180), border=1.5, shadow=PROP)
    flat(c, [Thick(160 + 100 * math.cos(math.radians(a)), 362 - 50 * math.sin(math.radians(a)),
                   160 + 100 * math.cos(math.radians(a + 15)), 362 - 50 * math.sin(math.radians(a + 15)), 3) for a in range(0, 180, 15)], rail)
    flat(c, [Thick(160 + 100 * math.cos(math.radians(a)), 362 - 50 * math.sin(math.radians(a)),
                   160 + 100 * math.cos(math.radians(a)), 386 - 50 * math.sin(math.radians(a)), 2.4) for a in range(0, 181, 30)], rail)
    # gazebo (right, on the far bank)
    roof = (90, 150, 110) if "roof" not in d else (220, 110, 70)
    piece(c, [RRect(690, 230, 830, 244, 2)], (240, 236, 226), border=1.5, shadow=PROP)
    piece(c, [RRect(700, 190, 708, 236, 1), RRect(812, 190, 820, 236, 1), RRect(756, 190, 764, 236, 1)], (240, 236, 226), shadow=SMALL)
    piece(c, Poly([(680, 192), (840, 192), (760, 140)]), roof, border=1.5, shadow=PROP)
    flat(c, Circ(760, 138, 5), roof)
    # blossom trees
    blossom_tree(c, 340, 268, s=1.2)
    blossom_tree(c, 560, 262, s=1.0, col=(246, 180, 200) if "blossom" not in d else (250, 250, 250))
    tree_round(c, 880, 280, s=1.3, col=(90, 160, 90))
    # path along the near bank
    piece(c, Poly([(-10, 470), (910, 450), (910, 520), (-10, 540)]), (226, 206, 170), shadow=SMALL)
    # lamp posts
    for x in (250, 700):
        piece(c, [RRect(x - 3, 400, x + 3, 520, 2)], (60, 70, 80), shadow=PROP)
        piece(c, [RRect(x - 14, 378, x + 14, 406, 5), Poly([(x - 18, 380), (x + 18, 380), (x, 364)])],
              (60, 70, 80) if not (x == 700 and "lamp" in d) else (200, 80, 70), shadow=PROP)
        flat(c, RRect(x - 8, 384, x + 8, 400, 2), (255, 236, 160))
    # bench with a reader
    modern(c, 440, 510, (120, 120, 190), bottom=(60, 60, 80), hair=(130, 130, 140), h=1.6, glasses=True)
    bench = (170, 110, 70) if "bench" not in d else (70, 150, 110)
    piece(c, [RRect(390, 470, 500, 480, 2), RRect(390, 488, 500, 496, 2), RRect(396, 496, 402, 520, 1), RRect(488, 496, 494, 520, 1)], bench,
          shadow=PROP)
    piece(c, RRect(446, 466, 468, 480, 2), (250, 250, 240), shadow=SMALL)
    # flower beds in the foreground
    for x0, cols in ((20, ((240, 90, 110), (250, 200, 70))), (560, ((250, 150, 60), (200, 120, 220)))):
        piece(c, Ell(x0 + 140, 576, 150, 30), (120, 170, 90), shadow=PROP)
        rnd = random.Random(x0)
        for k in range(22):
            fx, fy = x0 + 20 + k * 12 + rnd.uniform(-4, 4), 566 + rnd.uniform(-10, 14)
            col = cols[k % 2]
            if x0 == 560 and k % 2 == 0 and "flowers" in d:
                col = (90, 170, 240)
            flat(c, Circ(fx, fy, 5), col)
    # people with an umbrella and a dog walker
    modern(c, 140, 540, (240, 200, 80), bottom=(70, 80, 110), hair=(90, 60, 40), h=1.8, style="long", skirt=True)
    piece(c, Poly([(100, 450), (180, 450), (140, 424)]), (230, 80, 100), border=1.2, shadow=SMALL)
    flat(c, Thick(140, 450, 142, 470, 2), (60, 60, 70))
    modern(c, 820, 530, (80, 130, 200), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.9)


L506_ELEMENTS = [
    E("boat", lambda c, m: (piece(c, Poly([(400, 372), (480, 372), (466, 390), (414, 390)]), (240, 236, 226), border=1.5, shadow=SMALL),
                            modern(c, 440, 380, (230, 120, 60), bottom=(60, 60, 80), hair=(40, 30, 30), h=0.9),
                            flat(c, Thick(420, 378, 396, 392, 2), (150, 110, 70))),
      pivot=(440, 390), anim=dict(bobAmplitude=(10, 2), bobSpeed=0.15, swingAngle=3, swingSpeed=0.4)),
] + [
    E("duck%d" % i, (lambda x, y: lambda c, m: (piece(c, [Ell(x, y, 10, 6), Circ(x + 8, y - 7, 5)], (250, 250, 246), border=1, shadow=SMALL),
                                              flat(c, Poly([(x + 12, y - 8), (x + 18, y - 6), (x + 12, y - 5)]), (250, 170, 50))))(x, y),
      pivot=(x, y), anim=dict(bobAmplitude=(6, 1.5), bobSpeed=0.25, phase=i / 3))
    for i, (x, y) in enumerate(((560, 330), (590, 342), (330, 410)))
] + [
    paper_sun("sun", 90, 70, r=30),
    cloud("cloudA", 200, 60, 1.2, (176, 182, 196), W_(OVERCAST, RAIN)),
    cloud("cloudB", 520, 50, 1.4, (168, 174, 190), W_(OVERCAST, RAIN)),
    cloud("cloudC", 800, 66, 1.2, (176, 182, 196), W_(OVERCAST, RAIN)),
    puddles("puddles", [Ell(300, 506, 36, 6), Ell(620, 496, 30, 5)], mask=W_(RAIN)),
    rain_layer("rain", 506, 70, 24, 1.3, 0.6, 260, mask=W_(RAIN)),
] + splash_rings("splash", [(260, 360, 8), (520, 400, 7), (660, 350, 7)], mask=W_(RAIN))

L506_DIFFS = [
    ("bridge", 160, 330, 0),
    ("roof", 760, 170, 0),
    ("blossom", 560, 180, 0),
    ("lamp", 700, 388, 0),
    ("bench", 445, 490, 0),
    ("flowers", 700, 566, 0),
]


# =================================================================== Level 507 ski resort (snow)
STEPS507 = [(CLEAR, 10), (SNOW, 12), (FOG, 6)]
SNOWC = (246, 248, 252)
CABLE = ((70, 470), (520, 90))


def skier(c, x, base, jacket, h=1.8, lean=0, hat=(230, 60, 70)):
    modern(c, x, base, jacket, bottom=(50, 60, 90), hair=(40, 30, 30), h=h)
    hx, hy = x + 1 * h, base - 46 * h
    flat(c, [Ell(hx, hy - 5 * h, 8 * h, 5 * h), Circ(hx, hy - 11 * h, 3 * h)], hat)
    flat(c, Thick(hx - 2 * h, hy - 1 * h, hx + 7 * h, hy - 1 * h, 3 * h), (60, 60, 80))
    flat(c, Thick(x - 22 * h, base + 1, x + 26 * h, base - 3 * h * lean, 2.6 * h), (60, 120, 210))
    flat(c, [Thick(x - 10 * h, base - 24 * h, x - 18 * h, base, 1.4), Thick(x + 10 * h, base - 24 * h, x + 16 * h, base, 1.4)], (120, 120, 130))


def snowman(c, x, base, s=1.0, hat=(50, 50, 60), nose=(250, 140, 40), scarf=(220, 60, 70)):
    piece(c, [Circ(x, base - 22 * s, 24 * s), Circ(x, base - 58 * s, 17 * s), Circ(x, base - 86 * s, 13 * s)], SNOWC, border=1.5, shadow=PROP)
    flat(c, [RRect(x - 10 * s, base - 116 * s, x + 10 * s, base - 96 * s, 2), RRect(x - 16 * s, base - 98 * s, x + 16 * s, base - 94 * s, 1)], hat)
    flat(c, Poly([(x + 2 * s, base - 88 * s), (x + 20 * s, base - 85 * s), (x + 2 * s, base - 82 * s)]), nose)
    flat(c, [Circ(x - 4 * s, base - 90 * s, 1.8 * s), Circ(x + 6 * s, base - 90 * s, 1.8 * s)], INK)
    flat(c, [RRect(x - 14 * s, base - 76 * s, x + 14 * s, base - 70 * s, 2), RRect(x + 4 * s, base - 72 * s, x + 10 * s, base - 56 * s, 2)], scarf)
    flat(c, [Circ(x, base - 60 * s, 2 * s), Circ(x, base - 50 * s, 2 * s)], INK)


def l507_bg(c, d):
    sky(c, (120, 176, 230), (220, 232, 246), 300)
    # mountains
    piece(c, Poly([(-10, 300), (120, 120), (220, 220), (360, 60), (520, 230), (640, 110), (800, 240), (910, 160), (910, 330), (-10, 330)]),
          (180, 196, 220), shadow=LAYER)
    for (px, py), w in (((120, 120), 40), ((360, 60), 60), ((640, 110), 46)):
        flat(c, Poly([(px - w, py + w * 1.1), (px, py), (px + w, py + w * 1.1), (px + w * 0.4, py + w * 0.8), (px, py + w), (px - w * 0.4, py + w * 0.8)]),
             SNOWC)
    far_ridge(c, 300, 40, (200, 214, 232), 5071)
    # snow slope
    piece(c, Poly([(-10, 330), (300, 300), (910, 360), (910, 612), (-10, 612)]), SNOWC, shadow=LAYER)
    for x, y in ((200, 380), (420, 420), (620, 470), (300, 520), (760, 540)):
        flat(c, Ell(x, y, 90, 8), (230, 236, 246))
    # pine forest on both edges
    for x, b, h in ((20, 360, 110), (60, 380, 90), (100, 352, 120), (820, 400, 110), (860, 392, 130), (900, 410, 100), (780, 420, 80)):
        if (x == 780) and "pine" in d:
            continue
        tree_pine(c, x, b, h=h, col=(60, 120, 90), snow=SNOWC)
    # chairlift towers + cable
    (x0, y0), (x1, y1) = CABLE
    for f in (0.15, 0.55, 0.92):
        tx, ty = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        piece(c, [RRect(tx - 4, ty, tx + 4, ty + 120 - f * 60, 1), RRect(tx - 18, ty - 4, tx + 18, ty + 4, 2)], (110, 116, 130), shadow=PROP)
    flat(c, Thick(x0, y0, x1, y1, 2), (70, 70, 80))
    # lodge (right)
    piece(c, RRect(560, 230, 760, 340, 2), (170, 110, 80), border=2, shadow=PROP)
    for y in range(240, 340, 14):
        flat(c, Thick(560, y, 760, y, 1.4), (150, 96, 70))
    piece(c, Poly([(540, 236), (780, 236), (660, 168)]), (120, 70, 60), border=2, shadow=PROP)
    flat(c, Poly([(540, 236), (780, 236), (760, 226), (660, 172), (560, 226)]), SNOWC)
    piece(c, RRect(714, 160, 734, 210, 2), (150, 100, 90), border=1.2, shadow=SMALL)
    flat(c, RRect(712, 156, 736, 164, 2), SNOWC)
    for x in (586, 696):
        flat(c, RRect(x, 262, x + 40, 300, 3), (255, 222, 140))
        flat(c, [Thick(x + 20, 262, x + 20, 300, 2), Thick(x, 281, x + 40, 281, 2)], (150, 96, 70))
    flat(c, RRect(640, 280, 680, 340, 3), (90, 60, 50) if "door" not in d else (70, 130, 200))
    piece(c, RRect(610, 196, 710, 222, 4), (240, 236, 226), border=1.2, shadow=SMALL)
    sign_box(c, 620, 202, 700, 216, (170, 60, 60), 5072, vertical=False)
    # slalom flags
    for k, (x, y) in enumerate(((330, 420), (440, 470), (520, 420))):
        col = (230, 60, 70) if k % 2 == 0 else (60, 110, 220)
        if k == 1 and "flag" in d:
            col = (250, 200, 50)
        flat(c, Thick(x, y, x, y - 58, 2.4), (90, 90, 100))
        piece(c, Poly([(x + 1, y - 58), (x + 40, y - 46), (x + 1, y - 30)]), col, border=1, shadow=SMALL)
    # snowman + skiers + ski rack
    snowman(c, 840, 590, s=1.3, hat=(50, 50, 60) if "hat" not in d else (60, 120, 220))
    skier(c, 300, 560, (240, 120, 50), h=2.0)
    piece(c, [RRect(440, 520, 520, 530, 4), Thick(518, 526, 530, 512, 3)], (200, 60, 60), border=1.2, shadow=PROP)
    modern(c, 474, 524, (250, 200, 60), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.1)
    skier(c, 640, 590, (80, 170, 220) if "jacket" not in d else (230, 90, 160), h=2.1, hat=(250, 200, 60))
    piece(c, [RRect(60, 540, 160, 548, 2), RRect(64, 548, 70, 590, 1), RRect(150, 548, 156, 590, 1)], (130, 90, 60), shadow=PROP)
    for k, col in enumerate(((230, 60, 70), (60, 110, 220), (250, 200, 60), (90, 170, 90))):
        flat(c, Thick(76 + k * 20, 590, 80 + k * 20, 516, 5), col)


def chair(f):
    (x0, y0), (x1, y1) = CABLE

    def d(c, m):
        x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        flat(c, Thick(x, y, x, y + 26, 2), (70, 70, 80))
        piece(c, [RRect(x - 16, y + 24, x + 16, y + 30, 2), RRect(x - 16, y + 12, x - 12, y + 30, 1)], (220, 70, 60), border=1, shadow=SMALL)
    return d


L507_ELEMENTS = [
    E("chair%d" % i, chair(0.04), anim=dict(driftVelocity=((CABLE[1][0] - CABLE[0][0]) / 18, -(CABLE[1][1] - CABLE[0][1]) / 18),
                                           driftLength=math.hypot(CABLE[1][0] - CABLE[0][0], CABLE[1][1] - CABLE[0][1]) * 0.9,
                                           driftFade=False, phase=i / 3))
    for i in range(3)
] + [
    E("smoke%d" % i, (lambda: lambda c, m: piece(c, Circ(724, 150, 7), (236, 236, 240), shadow=SMALL))(),
      anim=dict(driftVelocity=(6, 18), driftLength=60, driftFade=True, driftGrow=1.4, phase=i / 3)) for i in range(3)
] + [
    paper_sun("sun", 800, 60, r=28),
    cloud("cloudA", 240, 40, 1.2, (220, 226, 236), W_(SNOW, FOG)),
    cloud("cloudB", 560, 30, 1.3, (220, 226, 236), W_(SNOW, FOG)),
    snow_layer("snow", 507, 70, 2.0, 4.0, 40),
    fog_layer("fog", 507, 300, 460, 0.35, 12),
]

L507_DIFFS = [
    ("door", 660, 310, 0),
    ("pine", 780, 380, 0),
    ("flag", 460, 426, 0),
    ("hat", 840, 450, 0),
    ("jacket", 641, 525, 0),
]


# =================================================================== Level 508 seaside lighthouse (day / night)
DN508 = day_night(40.0, tint=(0.24, 0.28, 0.52))
SUN508, MOON508 = celestial((420, 260), (330, 210), 40.0)


def l508_bg(c, d):
    sky(c, (120, 184, 236), (236, 226, 214), 300)
    cloud_bank(c, 150, (250, 248, 244), 5081, k=0.7)
    # sea
    c.gradient(260, H, (90, 160, 210), (60, 120, 180))
    for k in range(14):
        rnd = random.Random(5082 + k)
        x, y = rnd.uniform(200, 700), rnd.uniform(280, 440)
        flat(c, Thick(x, y, x + rnd.uniform(20, 50), y, 2), (140, 196, 230))
    # village hill (left)
    piece(c, Poly([(-10, 250), (80, 230), (200, 250), (300, 300), (330, 380), (-10, 380)]), (130, 180, 110), shadow=LAYER)
    for k, (x, b, w, wall, roof) in enumerate(((40, 262, 60, (250, 246, 236), (60, 110, 190)), (120, 270, 66, (246, 226, 196), (200, 90, 70)),
                                               (210, 296, 56, (250, 246, 236), (60, 110, 190)), (60, 330, 70, (240, 220, 180), (200, 90, 70)),
                                               (170, 352, 64, (250, 246, 236), (90, 150, 110)))):
        if k == 1 and "roof" in d:
            roof = (240, 190, 60)
        house(c, x, b, w, w * 0.7, wall, roof, wins=1)
    # cliff + lighthouse (right)
    piece(c, Poly([(600, 600), (640, 300), (700, 250), (910, 230), (910, 600)]), (170, 150, 130), border=2, shadow=LAYER)
    flat(c, Poly([(700, 250), (910, 230), (910, 260), (700, 270)]), (120, 170, 100))
    stripe = (220, 60, 60) if "stripe" not in d else (60, 110, 200)
    piece(c, Poly([(752, 250), (848, 250), (836, 90), (764, 90)]), (250, 250, 250), border=2, shadow=PROP)
    for y0 in (108, 166, 224):
        flat(c, RRect(756 + (250 - y0) * 0.075, y0, 844 - (250 - y0) * 0.075, y0 + 22, 0), stripe)
    piece(c, RRect(756, 80, 844, 92, 2), (60, 60, 70), shadow=SMALL)
    piece(c, RRect(772, 46, 828, 80, 2), (250, 236, 170), border=1.5, shadow=SMALL)
    flat(c, [Thick(790, 46, 790, 80, 2), Thick(810, 46, 810, 80, 2)], (60, 60, 70))
    piece(c, Poly([(764, 48), (836, 48), (800, 20)]), (60, 60, 70), border=1.5, shadow=SMALL)
    flat(c, RRect(788, 196, 812, 250, 10), (90, 70, 60))
    # pier with lamp posts
    piece(c, RRect(260, 440, 640, 456, 2), (170, 120, 80), border=1.5, shadow=PROP)
    for x in range(270, 640, 50):
        flat(c, RRect(x, 456, x + 8, 520, 1), (130, 90, 60))
    for k, x in enumerate((300, 600)):
        piece(c, [RRect(x - 3, 380, x + 3, 440, 2)], (60, 60, 70), shadow=PROP)
        piece(c, [RRect(x - 13, 362, x + 13, 388, 4), Poly([(x - 16, 364), (x + 16, 364), (x, 350)])],
              (60, 60, 70) if not (k == 1 and "lamp" in d) else (60, 140, 110), shadow=PROP)
        flat(c, RRect(x - 7, 368, x + 7, 382, 2), (255, 236, 160))
    # moored sailboat
    piece(c, Poly([(380, 420), (500, 420), (486, 440), (394, 440)]), (240, 240, 236), border=1.5, shadow=PROP)
    flat(c, Thick(440, 420, 440, 320, 3), (120, 90, 70))
    sail = (250, 250, 246) if "sail" not in d else (250, 190, 90)
    piece(c, Poly([(444, 324), (444, 414), (500, 414)]), sail, border=1.5, shadow=SMALL)
    piece(c, Poly([(436, 340), (436, 414), (396, 414)]), (230, 90, 80), border=1.5, shadow=SMALL)
    # buoys + rocks in front
    piece(c, [Ell(140, 520, 18, 10), RRect(132, 492, 148, 516, 3)], (240, 80, 60) if "buoy" not in d else (250, 220, 70), border=1.2, shadow=SMALL)
    for x, s in ((40, 1.6), (500, 1.2), (900, 1.4)):
        piece(c, Poly([(x - 50 * s, 600), (x - 40 * s, 560), (x - 10 * s, 540), (x + 30 * s, 550), (x + 50 * s, 600)]), (120, 116, 120), shadow=PROP)
    # fisherman on the pier
    modern(c, 540, 440, (240, 200, 70), bottom=(60, 60, 80), hair=(130, 130, 140), h=1.6)
    flat(c, Thick(550, 400, 620, 360, 2), (120, 90, 70))
    flat(c, Thick(620, 360, 626, 470, 1), (200, 200, 210))


L508_ELEMENTS = [
    sun_element("sun", (420, 260), SUN508, r=26),
    moon_element("moon", (420, 260), MOON508, r=20),
    star_field("stars", 508, 30, 140, avoid=[(740, 0, 860, 260)]),
    E("beam", lambda c, m: soft_union(c, [Poly([(800, 63), (520, 20), (520, 106)])], (255, 246, 200), 0.35, spread=16), pivot=(800, 63),
      daynight="night", anim=dict(swingAngle=14, swingSpeed=0.25)),
    E("lantern", lambda c, m: soft_union(c, [Circ(800, 63, 14)], (255, 236, 160), 0.6, spread=18), daynight="night",
      anim=dict(pulse=0.1, scaleSpeed=1.0)),
    window_glow("windows", [(31, 230, 49, 248), (111, 236, 129, 254), (201, 265, 219, 283), (51, 285, 69, 303), (161, 312, 179, 330)]),
    E("boat2", lambda c, m: (piece(c, Poly([(0, 300), (60, 300), (50, 312), (10, 312)]), (240, 120, 80), border=1, shadow=SMALL),
                             flat(c, Thick(30, 300, 30, 270, 2), (120, 90, 70)), piece(c, Poly([(32, 272), (32, 298), (54, 298)]), (250, 250, 246), shadow=SMALL)),
      anim=dict(drift_across(0, 60, 14, start=330))),
    bird_el("gull1", 300, 200, s=8, speed=-20, daynight="day"),
    bird_el("gull2", 500, 230, s=7, speed=-26, daynight="day"),
    E("bob", lambda c, m: flat(c, Circ(626, 474, 4), (250, 80, 60)), pivot=(626, 474), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.8)),
]

L508_DIFFS = [
    ("roof", 120, 230, 0),
    ("stripe", 800, 180, 0),
    ("lamp", 600, 370, 0),
    ("sail", 470, 380, 0),
    ("buoy", 140, 508, 0),
]


# =================================================================== Level 509 library
SPINES = [(170, 60, 60), (60, 100, 160), (70, 130, 90), (200, 160, 70), (120, 80, 140), (150, 110, 80), (220, 210, 190), (60, 60, 70)]


def bookcase(c, x0, x1, y0, y1, seed, rows=5, swap=None):
    piece(c, RRect(x0, y0, x1, y1, 2), (130, 86, 58), border=2, shadow=PROP)
    rnd = random.Random(seed)
    h = (y1 - y0 - 12) / rows
    for r in range(rows):
        top, base = y0 + 6 + r * h, y0 + 6 + (r + 1) * h
        flat(c, RRect(x0 + 6, top, x1 - 6, base - 4, 1), (90, 58, 40))
        flat(c, RRect(x0 + 2, base - 6, x1 - 2, base, 1), (150, 100, 68))
        x, i = x0 + 8, 0
        while x < x1 - 14:
            w = rnd.choice((8, 9, 10, 12))
            bh = h * rnd.uniform(0.62, 0.86)
            col = rnd.choice(SPINES)
            if swap and swap[0] == r and swap[1] <= i <= swap[2]:
                col = swap[3]
            if rnd.random() < 0.07 and x < x1 - 30:
                flat(c, Poly([(x, base - 6), (x + 8, base - 6), (x + 24, base - 6 - bh * 0.9), (x + 16, base - 6 - bh * 0.94)]), col)
                x += 26
            else:
                flat(c, RRect(x, base - 6 - bh, x + w, base - 6, 1), col)
                flat(c, Thick(x + 2, base - 6 - bh * 0.7, x + w - 2, base - 6 - bh * 0.7, 1.2), lit(col, 1.35))
                x += w + 1
            i += 1


def l509_bg(c, d):
    c.rect(0, 0, W, 470, (214, 196, 170))
    for x in range(0, W, 30):
        flat(c, Thick(x, 0, x, 470, 1), (204, 186, 160))
    # tall bookcases
    bookcase(c, 10, 250, 30, 440, 5091)
    bookcase(c, 650, 890, 30, 440, 5092, swap=(2, 4, 9, (250, 200, 60)) if "books" in d else None)
    # arched window (centre)
    piece(c, Poly([(330, 300)] + [(450 + 120 * math.cos(math.radians(a)), 150 - 110 * math.sin(math.radians(a))) for a in range(180, -1, -10)] +
                  [(570, 300)]), (120, 86, 62), border=2, shadow=PROP)
    flat(c, Poly([(344, 290)] + [(450 + 106 * math.cos(math.radians(a)), 150 - 96 * math.sin(math.radians(a))) for a in range(180, -1, -10)] +
                 [(556, 290)]), (170, 210, 236))
    flat(c, [Circ(x, y, r) for x, y, r in ((360, 250, 24), (410, 240, 30), (470, 246, 26), (530, 240, 28))], (120, 176, 120))
    flat(c, RRect(344, 260, 556, 290, 0), (140, 186, 120))
    flat(c, [Thick(450, 56, 450, 290, 4), Thick(344, 170, 556, 170, 4)], (120, 86, 62))
    piece(c, Poly([(318, 40), (352, 40), (346, 300), (318, 310)]), (150, 40, 60) if "curtain" not in d else (60, 110, 160), border=1.5, shadow=PROP)
    piece(c, Poly([(582, 40), (548, 40), (554, 300), (582, 310)]), (150, 40, 60), border=1.5, shadow=PROP)
    flat(c, Thick(300, 40, 600, 40, 5), (180, 140, 60))
    # painting between window and right case
    piece(c, RRect(588, 330, 640, 400, 2), (190, 150, 70), border=1.5, shadow=PROP)
    flat(c, RRect(594, 336, 634, 394, 1), (110, 150, 170))
    flat(c, Poly([(594, 394), (614, 360), (634, 394)]), (90, 120, 90))
    # wainscot + floor
    piece(c, RRect(-10, 440, 910, 470, 0), (140, 96, 66), shadow=SMALL)
    c.rect(0, 470, W, H, (160, 112, 76))
    for y in range(476, H, 24):
        off = 0 if (y // 24) % 2 else 60
        for x in range(-60 + off, W, 120):
            flat(c, Thick(x, y, x, y + 24, 1.2), (144, 100, 68))
        flat(c, Thick(0, y, W, y, 1.2), (144, 100, 68))
    piece(c, Ell(450, 560, 330, 40), (150, 60, 60), shadow=SMALL)
    c.ellipse_ring(450, 560, 310, 34, 4, (220, 180, 90))
    # rolling ladder on the left case
    piece(c, [Thick(200, 470, 240, 30, 4), Thick(240, 470, 280, 30, 4)], (170, 120, 80), shadow=PROP)
    flat(c, [Thick(200 + k * 4, 470 - k * 44, 240 + k * 4, 470 - k * 44, 3) for k in range(10)], (170, 120, 80))
    # reading table with lamps
    piece(c, [RRect(300, 470, 600, 484, 3), RRect(316, 484, 328, 560, 2), RRect(572, 484, 584, 560, 2)], (120, 76, 50), border=1.5, shadow=PROP)
    for k, x in enumerate((360, 540)):
        flat(c, [Thick(x, 470, x, 440, 2.4)], (190, 150, 60))
        shade = (60, 140, 90) if not (k == 1 and "lamp" in d) else (200, 70, 70)
        piece(c, Poly([(x - 22, 444), (x + 22, 444), (x + 12, 424), (x - 12, 424)]), shade, border=1.2, shadow=SMALL)
    piece(c, [RRect(400, 456, 450, 470, 2)], (240, 236, 220), border=1, shadow=SMALL)
    flat(c, Thick(425, 457, 425, 469, 1), (200, 190, 170))
    piece(c, [RRect(460, 446, 500, 470, 2)], (60, 100, 160), border=1, shadow=SMALL)
    # readers
    modern(c, 300, 560, (120, 90, 150), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.0, glasses=True)
    modern(c, 610, 560, (230, 200, 120), bottom=(70, 70, 90), hair=(220, 180, 90), h=2.0, style="long")
    # globe on a stand (right front)
    piece(c, [RRect(776, 520, 784, 580, 2), Ell(780, 584, 26, 6)], (150, 100, 60), border=1.2, shadow=PROP)
    globe = (90, 150, 210) if "globe" not in d else (220, 170, 90)
    piece(c, Circ(780, 488, 34), globe, border=1.5, shadow=PROP)
    flat(c, [Ell(770, 476, 14, 10), Ell(792, 500, 12, 8)], (120, 180, 100))
    c.ellipse_ring(780, 488, 40, 40, 3, (190, 150, 60))
    # armchair with a cat
    chair = (150, 60, 60) if "chair" not in d else (70, 120, 90)
    piece(c, [RRect(40, 470, 150, 560, 16), RRect(30, 500, 60, 560, 10), RRect(130, 500, 160, 560, 10)], chair, border=1.5, shadow=PROP)
    flat(c, RRect(60, 520, 130, 540, 6), lit(chair, 1.12))
    # potted plant
    piece(c, Poly([(866, 560), (898, 560), (892, 600), (872, 600)]), (190, 110, 80), border=1.2, shadow=PROP)
    piece(c, [Ell(882, 532, 18, 30), Ell(866, 520, 10, 22), Ell(898, 524, 10, 22)], (80, 150, 90), shadow=SMALL)


def cat(c, m):
    piece(c, [Ell(96, 512, 26, 12), Circ(118, 500, 10), Poly([(110, 494), (112, 482), (118, 492)]), Poly([(122, 492), (128, 482), (128, 496)])],
          (240, 170, 90), border=1.2, shadow=SMALL)
    flat(c, [Thick(112, 500, 117, 502, 1.4), Thick(121, 502, 126, 500, 1.4)], INK)


L509_ELEMENTS = [
    E("cat", cat, pivot=(96, 520), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
    E("cat_tail", lambda c, m: flat(c, Thick(72, 516, 56, 500, 4), (240, 170, 90)), pivot=(72, 516), anim=dict(swingAngle=16, swingSpeed=0.6)),
    E("glow1", lambda c, m: soft_union(c, [Ell(360, 452, 20, 8)], (255, 236, 160), 0.6, spread=12), anim=dict(twinkle=0.15, twinkleSpeed=0.6)),
    E("glow2", lambda c, m: soft_union(c, [Ell(540, 452, 20, 8)], (255, 236, 160), 0.6, spread=12),
      anim=dict(twinkle=0.15, twinkleSpeed=0.6, phase=0.5)),
    E("page", lambda c, m: flat(c, Poly([(425, 457), (446, 452), (446, 468), (425, 469)]), (250, 248, 236)), pivot=(425, 463),
      anim=dict(stretch=(0.6, 0), scaleSpeed=0.5)),
    E("dust", lambda c, m: [flat(c, Circ(380 + k * 30, 120 + (k % 3) * 40, 2), (255, 250, 220, 0.8)) for k in range(6)],
      anim=dict(bobAmplitude=(4, 8), bobSpeed=0.1, twinkle=0.4, twinkleSpeed=0.5)),
]

L509_DIFFS = [
    ("books", 790, 200, 0),
    ("curtain", 330, 170, 0),
    ("lamp", 540, 434, 0),
    ("globe", 780, 488, 0),
    ("chair", 95, 500, 0),
]


LEVELS = [
    ("Level500", "动物园", l500_bg, L500_ELEMENTS, L500_DIFFS, 60, OPTS),
    ("Level501", "机场", l501_bg, L501_ELEMENTS, L501_DIFFS, 60, OPTS),
    ("Level502", "超市", l502_bg, L502_ELEMENTS, L502_DIFFS, 60, OPTS),
    ("Level503", "学校操场", l503_bg, L503_ELEMENTS, L503_DIFFS, 60, OPTS),
    ("Level504", "消防站", l504_bg, L504_ELEMENTS, L504_DIFFS, 60, OPTS),
    ("Level505", "面包店", l505_bg, L505_ELEMENTS, L505_DIFFS, 60, OPTS),
    ("Level506", "湖畔公园", l506_bg, L506_ELEMENTS, L506_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS506, blend=3.0), anim_seconds=30.0, frames=80)),
    ("Level507", "滑雪场", l507_bg, L507_ELEMENTS, L507_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS507, blend=3.0), anim_seconds=28.0, frames=80)),
    ("Level508", "海边灯塔", l508_bg, L508_ELEMENTS, L508_DIFFS, 60, dict(OPTS, day_night=DN508, anim_seconds=40.0, frames=80)),
    ("Level509", "图书馆", l509_bg, L509_ELEMENTS, L509_DIFFS, 60, OPTS),
]
