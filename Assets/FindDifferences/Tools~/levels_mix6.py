# -*- coding: utf-8 -*-
"""Mixed themes part 6 (paper-craft interiors / town scenes, full-bleed, original designs, no brands):
  Level285 邮局       - a post office: counter windows, wall of post boxes, parcel scale, mail sacks, letter box
  Level286 宠物医院   - a vet clinic: exam table with a dog, vet, X-ray light box, cabinet, cat carrier, rabbit
  Level287 滑板公园   - a skate park: half-pipe, ramps, rails, skaters, benches, skyline behind
  Level288 水上乐园   - a water park: twisting slides, pool with rings, lifeguard tower, umbrellas, palms
  Level289 露天电影院 - a drive-in cinema at night: big screen, cars, projector beam, snack stand with neon
  Level290 保龄球馆   - a bowling alley: lanes, pins, ball return, score screens, bowler, shoe rack
  Level291 健身房     - a gym: treadmills, dumbbell rack, punching bag, yoga mats, mirror wall, water cooler
  Level292 跳蚤市场   - an outdoor flea market: awnings, tables of old radios, vases, records, lamps, buyers
  Level293 屋顶花园   - a rooftop garden: planter beds, pergola with string lights, water tank, skyline
  Level294 地铁车厢   - inside a subway car: seats, straps, route map, posters, passengers, tunnel lights
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, layer, palm, sky, stars_bg, sun_bg, tree_round
from fills import far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_festival import npiece, string_lights, lights_el
from levels_homes import planks, steam
from levels_mix2 import pot_plant, teddy, wheel
from levels_modern import car_side

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def wall_poster(c, x0, y0, x1, y1, col, seed, art=None):
    piece(c, RRect(x0, y0, x1, y1, 3), col, border=1.5, shadow=PROP)
    if art:
        art(c)
    sign_box(c, x0 + 10, y1 - 30, x1 - 10, y1 - 10, col, seed, vertical=False)


# =================================================================== Level 285 post office
def l285_bg(c, d):
    c.rect(0, 0, W, 440, (236, 226, 200))
    flat(c, RRect(0, 300, W, 440, 0), (190, 160, 120))
    # wall of post boxes (left)
    piece(c, RRect(20, 40, 300, 280, 3), (180, 150, 90), border=1.5, shadow=PROP)
    for r in range(5):
        for k in range(6):
            x, y = 32 + k * 44, 52 + r * 44
            col = (200, 170, 100)
            if "box" in d and r in (1, 2) and k in (2, 3):
                col = (90, 140, 190)
            flat(c, RRect(x, y, x + 38, y + 38, 2), col)
            flat(c, [Circ(x + 30, y + 19, 3), RRect(x + 6, y + 6, x + 22, y + 12, 1)], (120, 100, 60))
    # clock (centre top)
    clock = (90, 60, 40) if "clock" not in d else (60, 110, 160)
    piece(c, Circ(450, 64, 36), clock, border=1.5, shadow=PROP)
    flat(c, Circ(450, 64, 28), (250, 246, 232))
    flat(c, [Thick(450, 64, 450, 44, 3), Thick(450, 64, 466, 70, 3)], INK)
    # stamp poster (right top)
    stamp = (220, 80, 70) if "stamp" not in d else (90, 160, 110)
    piece(c, RRect(700, 30, 870, 180, 3), (250, 248, 240), border=1.5, shadow=PROP)
    for k in range(10):
        flat(c, [Circ(720 + k * 15, 46, 4), Circ(720 + k * 15, 164, 4)], (236, 226, 200))
    flat(c, RRect(730, 60, 840, 150, 2), stamp)
    piece(c, [Ell(785, 110, 30, 24), Poly([(760, 100), (785, 76), (810, 100)])], (250, 248, 240), shadow=None)
    # counter windows
    for x in (380, 560):
        piece(c, RRect(x - 70, 120, x + 70, 300, 4), (130, 90, 60), border=1.5, shadow=PROP)
        flat(c, RRect(x - 60, 130, x + 60, 260, 2), (200, 220, 230))
        flat(c, RRect(x - 40, 260, x + 40, 300, 2), (90, 60, 40))
    hx, hy = modern(c, 380, 260, (90, 120, 160), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.2)
    piece(c, RRect(hx - 14, hy - 14, hx + 14, hy - 6, 2), (60, 70, 90), shadow=None)
    modern(c, 560, 260, (220, 220, 214), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.1, style="long")
    # scale with a parcel (counter right)
    piece(c, [RRect(660, 280, 760, 300, 2), RRect(700, 300, 720, 316, 1)], (170, 170, 180), border=1.2, shadow=SMALL)
    parcel = (200, 160, 100) if "parcel" not in d else (220, 90, 90)
    piece(c, RRect(670, 220, 750, 282, 3), parcel, border=1.2, shadow=SMALL)
    flat(c, [Thick(710, 220, 710, 282, 4), Thick(670, 250, 750, 250, 4)], (240, 230, 200))
    # counter front
    piece(c, RRect(260, 300, 800, 440, 0), (150, 110, 70), shadow=LAYER)
    for x in range(260, 800, 60):
        flat(c, RRect(x + 8, 316, x + 52, 424, 3), (140, 100, 64))
    # floor
    c.rect(0, 440, W, H, (200, 190, 170))
    for x in range(0, W, 50):
        for y in range(440, H, 50):
            if (x // 50 + y // 50) % 2:
                flat(c, RRect(x, y, x + 50, y + 50, 0), (186, 176, 156))
    # mail sacks (left front)
    for k, x in enumerate((70, 160)):
        if k == 1 and "sack" in d:
            continue
        piece(c, [Poly([(x - 40, 590), (x + 40, 590), (x + 34, 500), (x + 10, 486), (x - 10, 486), (x - 34, 500)])], (200, 190, 150), border=1.5, shadow=PROP)
        flat(c, Thick(x - 14, 494, x + 14, 494, 4), (150, 110, 70))
    # customer with letters (centre front)
    hx, hy = modern(c, 450, 600, (90, 150, 110), bottom=(60, 60, 80), hair=(200, 160, 90), h=2.5)
    if "letter" not in d:
        piece(c, [RRect(480, 490, 530, 524, 2), RRect(488, 480, 538, 514, 2)], (250, 250, 246), border=1, shadow=SMALL)
        flat(c, RRect(518, 484, 530, 496, 1), (220, 80, 70))
    # letter box (right front)
    lb = (210, 50, 50) if "mailbox" not in d else (60, 110, 170)
    piece(c, [RRect(760, 450, 860, 590, 10), Ell(810, 452, 50, 18)], lb, border=1.5, shadow=PROP)
    flat(c, [RRect(780, 480, 840, 490, 2)], (40, 40, 46))
    flat(c, RRect(790, 520, 830, 550, 2), (250, 240, 200))


L285_ELEMENTS = [
    E("fan", lambda c, m: [flat(c, Thick(600, 20, 600 + 50 * math.cos(a), 20 + 8 * math.sin(a), 6), (200, 190, 170)) for a in (0, 2.09, 4.19)], pivot=(600, 20),
      anim=dict(stretch=(0.6, 0), scaleSpeed=2.0)),
    E("stamp_hand", lambda c, m: piece(c, [RRect(420, 268, 436, 290, 2), Ell(428, 266, 10, 4)], (120, 80, 60), shadow=None), pivot=(428, 290),
      anim=dict(bobAmplitude=(0, 8), bobSpeed=1.2)),
    E("sway", lambda c, m: flat(c, Thick(600, 20, 600, 0, 2), (90, 90, 90)), pivot=(600, 0), anim=dict(swingAngle=2, swingSpeed=0.5)),
]

L285_DIFFS = [
    ("box", 166, 140, 0),
    ("clock", 450, 64, 0),
    ("stamp", 785, 105, 0),
    ("parcel", 710, 250, 0),
    ("sack", 160, 540, 0),
    ("letter", 510, 500, 0),
    ("mailbox", 810, 520, 0),
]


# =================================================================== Level 286 vet clinic
def dog(c, x, base, s, col, face=1, ear=None):
    for lx in (-18, -8, 12, 20):
        flat(c, RRect(x + lx * s * face - 3 * s, base - 18 * s, x + lx * s * face + 3 * s, base, 2), lit(col, 0.9))
    piece(c, [Ell(x, base - 24 * s, 26 * s, 11 * s), Circ(x + 28 * s * face, base - 36 * s, 11 * s), Ell(x + 38 * s * face, base - 32 * s, 7 * s, 5 * s)], col,
          border=1.2, shadow=SMALL)
    flat(c, Ell(x + 24 * s * face, base - 32 * s, 4 * s, 9 * s), ear or lit(col, 0.7))
    flat(c, [Circ(x + 32 * s * face, base - 38 * s, 1.6 * s), Circ(x + 44 * s * face, base - 33 * s, 2.2 * s)], INK)
    flat(c, Thick(x - 24 * s * face, base - 26 * s, x - 34 * s * face, base - 38 * s, 3 * s), col)


def l286_bg(c, d):
    c.rect(0, 0, W, 440, (214, 236, 236))
    flat(c, RRect(0, 290, W, 300, 0), (120, 190, 190))
    # X-ray light box (left top)
    xr = (220, 236, 250) if "xray" not in d else (250, 230, 160)
    piece(c, RRect(40, 40, 240, 180, 3), (200, 200, 210), border=1.5, shadow=PROP)
    flat(c, RRect(52, 52, 228, 168, 2), (40, 50, 70))
    flat(c, [Thick(80, 110, 200, 110, 6), Circ(76, 104, 9), Circ(76, 118, 9), Circ(204, 104, 9), Circ(204, 118, 9)], xr)
    for k in range(4):
        flat(c, Thick(100 + k * 26, 74, 100 + k * 26, 146, 3), lit(xr, 0.6))
    # cabinet with bottles (right top)
    piece(c, RRect(640, 30, 880, 200, 3), (250, 250, 246), border=1.5, shadow=PROP)
    for y in (90, 150):
        flat(c, Thick(650, y, 870, y, 3), (200, 200, 210))
    for r, y in enumerate((88, 148)):
        for k, x in enumerate(range(666, 870, 34)):
            col = [(120, 180, 230), (240, 160, 80), (140, 200, 140), (230, 120, 150), (200, 200, 120), (160, 140, 220)][(k + r * 2) % 6]
            if r == 0 and k == 2 and "bottle" in d:
                col = (220, 60, 60)
            piece(c, [RRect(x - 11, y - 40, x + 11, y, 4), RRect(x - 6, y - 48, x + 6, y - 38, 2)], col, border=1, shadow=None)
    # poster (centre top)
    poster = (250, 200, 120) if "poster" not in d else (160, 200, 250)
    wall_poster(c, 330, 40, 490, 200, poster, 2861, art=lambda c: [flat(c, [Circ(410, 100, 34)], (250, 250, 246)),
                                                                   flat(c, [Circ(398, 92, 5), Circ(422, 92, 5), Ell(410, 110, 10, 6)], (120, 90, 60))])
    # exam table + dog (centre)
    piece(c, [RRect(300, 360, 600, 380, 4), RRect(440, 380, 460, 470, 2), Ell(450, 474, 60, 8)], (170, 180, 196), border=1.5, shadow=PROP)
    dog(c, 430, 362, 2.2, (220, 170, 100) if "dog" not in d else (250, 250, 246), ear=(170, 120, 70))
    # vet
    hx, hy = modern(c, 620, 480, (250, 250, 250), bottom=(90, 140, 160), hair=(40, 30, 30), h=2.6, style="long")
    flat(c, [Thick(hx - 10, hy + 22, hx - 4, hy + 50, 2), Circ(hx - 4, hy + 52, 5)], (90, 90, 100))
    # floor
    c.rect(0, 440, W, H, (220, 226, 222))
    for x in range(0, W, 60):
        flat(c, Thick(x, 440, x - 30, H, 1.2), (206, 212, 208))
    # weighing scale (left)
    sc = (120, 190, 190) if "scale" not in d else (240, 140, 60)
    piece(c, [RRect(40, 520, 200, 560, 4), RRect(110, 440, 130, 520, 2), RRect(80, 420, 160, 450, 4)], sc, border=1.5, shadow=PROP)
    flat(c, RRect(92, 426, 148, 444, 2), (40, 50, 60))
    # cat carrier (centre left)
    car = (90, 120, 200) if "carrier" not in d else (240, 120, 160)
    piece(c, [RRect(240, 510, 360, 590, 10), Thick(270, 510, 300, 486, 4), Thick(330, 510, 300, 486, 4)], car, border=1.5, shadow=PROP)
    flat(c, RRect(258, 530, 300, 576, 4), (60, 60, 70))
    for x in range(264, 300, 8):
        flat(c, Thick(x, 530, x, 576, 1.4), (200, 200, 210))
    # owner with a rabbit (right front)
    modern(c, 800, 600, (200, 90, 90), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.4)
    if "rabbit" not in d:
        piece(c, [Ell(770, 520, 22, 16), Circ(790, 506, 11), Ell(786, 486, 4, 12), Ell(796, 486, 4, 12)], (250, 250, 246), border=1.2, shadow=SMALL)
        flat(c, Circ(794, 506, 1.8), INK)
    # plant (centre front)
    if "plant" not in d:
        pot_plant(c, 520, 596, 2.2, (240, 236, 226))


L286_ELEMENTS = [
    E("tail", lambda c, m: flat(c, Thick(380, 304, 360, 286, 6), (220, 170, 100)), pivot=(380, 304), anim=dict(swingAngle=26, swingSpeed=3.0)),
    E("glow", lambda c, m: soft_union(c, [RRect(52, 52, 228, 168, 2)], (220, 240, 255), 0.15, spread=16), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=0.6)),
    E("cateyes", lambda c, m: flat(c, [Circ(274, 552, 2.4), Circ(286, 552, 2.4)], (240, 220, 80)), pivot=(280, 552), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=0.4)),
]

L286_DIFFS = [
    ("xray", 140, 110, 0),
    ("poster", 410, 120, 0),
    ("bottle", 734, 64, 0),
    ("dog", 470, 300, 0),
    ("scale", 120, 490, 0),
    ("carrier", 300, 545, 0),
    ("rabbit", 780, 510, 0),
    ("plant", 520, 560, 0),
]


# =================================================================== Level 287 skate park
def skater(c, x, base, top, board, h=2.0, cap=None, lean=0):
    hx, hy = modern(c, x, base - 10, top, bottom=(60, 70, 100), hair=(60, 40, 30), h=h)
    flat(c, [Thick(x - 4 * h, base - 34 * h, x - 22 * h, base - 44 * h + lean, 3 * h), Thick(x + 6 * h, base - 34 * h, x + 24 * h, base - 40 * h - lean, 3 * h)], SKIN)
    piece(c, RRect(x - 24 * h, base - 10, x + 24 * h, base - 4, 3), board, border=1, shadow=SMALL)
    for wx in (x - 16 * h, x + 16 * h):
        flat(c, Circ(wx, base - 2, 3.4), (250, 250, 246))
    if cap:
        piece(c, [Ell(hx, hy - 6, 9 * h, 5 * h), RRect(hx, hy - 7 * h, hx + 12 * h, hy - 4 * h, 2)], cap, shadow=None)
    return hx, hy


def l287_bg(c, d):
    sky(c, (120, 180, 236), (240, 230, 220), H)
    sun_bg(c, 120, 70, 28)
    far_skyline(c, 220, 60, 160, (170, 186, 210), 2871, win=(200, 214, 230))
    far_round_trees(c, 230, 24, (100, 160, 100), 2872)
    # concrete ground
    c.rect(0, 250, W, H, (200, 200, 196))
    for x in range(0, W, 90):
        flat(c, Thick(x, 250, x - 60, H, 1.4), (186, 186, 182))
    # half-pipe (left)
    hp = (170, 180, 196)
    piece(c, Poly([(0, 400)] + [(160 + 150 * math.cos(math.pi * k / 16), 260 + 140 * math.sin(math.pi * k / 16)) for k in range(0, 17)] + [(320, 400), (320, 260),
                                                                                                                                        (340, 260), (340, 410), (-20, 410), (-20, 260), (0, 260)]),
          hp, border=1.5, shadow=PROP)
    flat(c, [Thick(-10, 258, 20, 258, 5), Thick(300, 258, 346, 258, 5)], (90, 90, 100))
    flat(c, Poly(star_pts(250, 370, 24, 10)), (240, 90, 90) if "ramp" not in d else (90, 200, 120))
    # wall with abstract murals (right back)
    piece(c, RRect(500, 160, 900, 260, 2), (230, 226, 214), border=1.5, shadow=PROP)
    mural = (240, 120, 160) if "mural" not in d else (120, 200, 230)
    flat(c, [Circ(570, 210, 34), Poly([(620, 250), (700, 170), (760, 250)])], mural)
    flat(c, [Circ(820, 200, 26), RRect(780, 230, 880, 246, 4)], (250, 200, 80))
    # grind rail (centre)
    rail = (240, 200, 60) if "rail" not in d else (90, 160, 220)
    piece(c, [Thick(380, 380, 600, 360, 5), Thick(400, 380, 400, 420, 4), Thick(580, 362, 580, 420, 4)], rail, border=1, shadow=PROP)
    # wedge ramp (right)
    piece(c, Poly([(640, 470), (860, 470), (860, 380)]), (180, 190, 204), border=1.5, shadow=PROP)
    # skaters
    skater(c, 490, 362, (220, 80, 70) if "shirt" not in d else (90, 180, 120), (60, 60, 70), h=1.8, lean=6)
    skater(c, 160, 360, (90, 120, 200), (240, 140, 60), h=1.7, cap=(250, 200, 60) if "cap" not in d else None)
    skater(c, 760, 430, (250, 250, 246), (200, 60, 200) if "board" not in d else (60, 200, 200), h=1.7)
    # bench + trash can (front)
    bench = (150, 100, 70) if "bench" not in d else (60, 110, 90)
    piece(c, [RRect(320, 540, 520, 556, 3), RRect(330, 556, 340, 596, 1), RRect(500, 556, 510, 596, 1), RRect(320, 506, 520, 520, 3)], bench, border=1.2, shadow=PROP)
    modern(c, 420, 556, (240, 200, 60), bottom=(60, 70, 100), hair=(30, 30, 34), h=1.8, style="long")
    can = (90, 140, 100) if "can" not in d else (220, 90, 70)
    piece(c, [RRect(620, 520, 680, 596, 4), Ell(650, 520, 32, 8)], can, border=1.5, shadow=PROP)
    # tree (right front)
    tree_round(c, 840, 600, 1.6, col=(90, 160, 90) if "tree" not in d else (230, 150, 60))
    # helmet on ground (left front)
    piece(c, Poly([(60 + 30 * math.cos(math.pi * k / 10), 590 - 26 * math.sin(math.pi * k / 10)) for k in range(11)]), (60, 60, 70), border=1.2, shadow=SMALL)


L287_ELEMENTS = [
    bird_el("bird", 600, 60, s=9, speed=-16),
    cloud_el("cloud", 420, 80, 0.5, 8),
    E("flyer", lambda c, m: skater(c, 340, 200, (240, 200, 60), (60, 60, 70), h=1.2), pivot=(340, 200), anim=dict(bobAmplitude=(30, 24), bobSpeed=0.25)),
]

L287_DIFFS = [
    ("ramp", 250, 370, 0),
    ("mural", 640, 210, 0),
    ("cap", 166, 270, 0),
    ("rail", 490, 380, 0),
    ("shirt", 492, 310, 0),
    ("board", 760, 424, 0),
    ("bench", 420, 540, 0),
    ("can", 650, 556, 0),
    ("tree", 840, 520, 0),
]


# =================================================================== Level 288 water park
def tube_slide(c, pts, col, w=26):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        piece(c, Thick(x0, y0, x1, y1, w), col, border=1.2, shadow=PROP)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        flat(c, Thick(x0, y0 - w * 0.25, x1, y1 - w * 0.25, w * 0.25), lit(col, 1.2))


def l288_bg(c, d):
    sky(c, (90, 180, 240), (220, 240, 250), H)
    sun_bg(c, 820, 60, 30)
    cloud_bg(c, 300, 50, 0.6)
    far_round_trees(c, 220, 26, (90, 170, 110), 2881)
    # slide tower + slides (left)
    piece(c, [RRect(60, 80, 200, 100, 2), Thick(70, 100, 70, 330, 6), Thick(190, 100, 190, 330, 6), Thick(70, 200, 190, 200, 4)], (240, 200, 60), border=1.2, shadow=PROP)
    piece(c, Poly([(50, 82), (210, 82), (130, 40)]), (220, 80, 70), border=1.5, shadow=PROP)
    tube_slide(c, [(200, 90), (300, 120), (330, 180), (260, 230), (300, 290), (380, 320)], (60, 140, 220) if "slide" not in d else (150, 210, 80))
    tube_slide(c, [(60, 100), (20, 160), (90, 220), (30, 280), (90, 330)], (240, 120, 60))
    # pool
    c.rect(0, 320, W, H, (240, 230, 210))
    piece(c, RRect(100, 340, 860, 520, 30), (80, 190, 230), border=2, shadow=LAYER)
    for k in range(8):
        flat(c, Thick(140 + k * 90, 370 + (k % 3) * 40, 190 + k * 90, 370 + (k % 3) * 40, 2), (170, 230, 250))
    # swim rings + swimmers
    ring = (240, 80, 80) if "ring" not in d else (250, 220, 60)
    c.ellipse_ring(560, 420, 30, 14, 10, ring)
    flat(c, Circ(560, 404, 10), SKIN)
    flat(c, Ell(558, 396, 10, 5), (60, 40, 30))
    c.ellipse_ring(700, 470, 26, 12, 9, (250, 200, 60))
    for x, y in ((300, 400), (420, 470)):
        flat(c, Circ(x, y, 10), SKIN)
        flat(c, Ell(x - 2, y - 8, 10, 5), (40, 30, 30))
    # rubber duck
    if "duck" not in d:
        piece(c, [Ell(220, 470, 24, 14), Circ(236, 452, 11), Poly([(244, 452), (256, 456), (244, 460)])], (250, 220, 60), border=1.2, shadow=SMALL)
        flat(c, Circ(238, 450, 2), INK)
    # lifeguard tower (right)
    tw = (250, 250, 246) if "tower" not in d else (240, 120, 60)
    piece(c, [Thick(760, 340, 790, 200, 5), Thick(860, 340, 830, 200, 5), RRect(770, 190, 850, 210, 2), RRect(780, 150, 840, 192, 2)], tw, border=1.5, shadow=PROP)
    flag = (220, 60, 50) if "flag" not in d else (60, 160, 90)
    flat(c, Thick(840, 150, 840, 100, 2), (90, 90, 100))
    piece(c, Poly([(840, 100), (876, 112), (840, 124)]), flag, border=1, shadow=None)
    modern(c, 810, 190, (220, 60, 50), bottom=(220, 60, 50), hair=(200, 160, 90), h=1.3)
    # palm (right back)
    palm(c, 660, 330, h=160, lean=-20)
    # umbrella + lounger (left front)
    umb = (240, 100, 120) if "umbrella" not in d else (90, 170, 230)
    flat(c, Thick(120, 600, 130, 520, 3), (150, 150, 160))
    piece(c, Poly([(40, 530), (220, 520), (130, 470)]), umb, border=1.5, shadow=PROP)
    piece(c, Poly([(60, 590), (220, 580), (236, 556), (210, 556)]), (250, 250, 246), border=1.2, shadow=SMALL)
    # towel + beach ball (front)
    towel = (90, 180, 200) if "towel" not in d else (240, 180, 60)
    piece(c, Poly([(380, 560), (560, 556), (570, 596), (370, 600)]), towel, border=1.2, shadow=SMALL)
    for k in range(4):
        flat(c, Thick(380 + k * 48, 560, 376 + k * 48, 598, 6), (250, 250, 246))
    if "ball" not in d:
        piece(c, Circ(700, 566, 24), (250, 250, 246), border=1.2, shadow=SMALL)
        flat(c, [Poly([(700, 566), (700, 542), (722, 556)]), Poly([(700, 566), (678, 576), (690, 588)])], (240, 80, 80))
        flat(c, [Poly([(700, 566), (722, 576), (712, 588)]), Poly([(700, 566), (678, 556), (690, 544)])], (60, 140, 230))
    modern(c, 820, 600, (250, 200, 60), bottom=(60, 120, 200), hair=(40, 30, 30), h=2.2)


L288_ELEMENTS = [
    E("rider", lambda c, m: [flat(c, Circ(380, 310, 9), SKIN), flat(c, Ell(380, 302, 9, 4), (60, 40, 30))], pivot=(380, 310), anim=dict(bobAmplitude=(0, 4), bobSpeed=0.8)),
    E("splash", lambda c, m: [flat(c, Circ(x, y, 4), (220, 246, 255)) for x, y in ((380, 334), (396, 330), (366, 330))], pivot=(380, 334), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.6)),
    E("wave", lambda c, m: [flat(c, Thick(x, 500, x + 40, 500, 2), (170, 230, 250)) for x in (180, 480, 760)], daynight="untinted",
      anim=dict(bobAmplitude=(14, 0), bobSpeed=0.3)),
    bird_el("gull", 500, 90, s=9, speed=14),
]

L288_DIFFS = [
    ("slide", 290, 200, 0),
    ("flag", 856, 112, 0),
    ("tower", 810, 220, 0),
    ("ring", 560, 420, 0),
    ("duck", 236, 462, 0),
    ("umbrella", 130, 505, 0),
    ("towel", 470, 578, 0),
    ("ball", 700, 566, 0),
]


# =================================================================== Level 289 drive-in cinema
def car_rear(c, x, base, col, s=1.0):
    npiece(c, [RRect(x - 60 * s, base - 50 * s, x + 60 * s, base - 10 * s, 10), Poly([(x - 44 * s, base - 50 * s), (x + 44 * s, base - 50 * s), (x + 34 * s, base - 80 * s),
                                                                                   (x - 34 * s, base - 80 * s)])], col)
    flat(c, Poly([(x - 36 * s, base - 54 * s), (x + 36 * s, base - 54 * s), (x + 28 * s, base - 76 * s), (x - 28 * s, base - 76 * s)]), (60, 70, 100))
    flat(c, [RRect(x - 56 * s, base - 40 * s, x - 36 * s, base - 30 * s, 2), RRect(x + 36 * s, base - 40 * s, x + 56 * s, base - 30 * s, 2)], (220, 60, 60))
    flat(c, [RRect(x - 52 * s, base - 12 * s, x - 34 * s, base, 3), RRect(x + 34 * s, base - 12 * s, x + 52 * s, base, 3)], (30, 30, 36))


def l289_bg(c, d):
    c.gradient(0, H, (14, 20, 54), (60, 50, 90))
    stars_bg(c, 2891, 90, 200)
    moon = (250, 240, 200)
    if "moon" not in d:
        npiece(c, Circ(820, 60, 24), moon, shadow=None)
        soft_union(c, [Circ(820, 60, 24)], (255, 250, 220), 0.25, spread=20)
    far_round_trees(c, 280, 26, (30, 44, 50), 2892)
    # big screen (centre)
    npiece(c, [RRect(240, 40, 660, 260, 2), Thick(300, 260, 300, 330, 6), Thick(600, 260, 600, 330, 6)], (180, 180, 190))
    flat(c, RRect(252, 52, 648, 248, 1), (120, 170, 220))
    flat(c, RRect(252, 180, 648, 248, 1), (60, 110, 170))
    ship = (220, 80, 60) if "ship" not in d else (240, 220, 80)
    flat(c, Poly([(380, 190), (520, 190), (500, 214), (400, 214)]), ship)
    flat(c, [Thick(450, 190, 450, 110, 3)], (90, 70, 60))
    flat(c, Poly([(454, 112), (454, 184), (510, 184)]), (250, 246, 236))
    flat(c, Poly([(446, 120), (446, 184), (400, 184)]), (250, 246, 236))
    flat(c, Circ(590, 90, 18), (250, 220, 120))
    # ground
    c.rect(0, 320, W, H, (40, 46, 56))
    for x in range(-100, W + 100, 120):
        flat(c, Thick(450, 320, x, H, 1.4), (56, 62, 74))
    # snack stand with neon (left)
    npiece(c, RRect(20, 260, 200, 400, 2), (200, 60, 60))
    stripe = (250, 250, 246) if "stand" not in d else (90, 160, 220)
    for x in range(20, 200, 30):
        flat(c, RRect(x, 260, x + 15, 290, 0), stripe)
    flat(c, RRect(40, 310, 180, 370, 2), (250, 220, 140))
    neon = (90, 230, 240) if "neon" not in d else (250, 120, 200)
    soft_union(c, [RRect(50, 214, 170, 246, 10)], neon, 0.5, spread=12)
    flat(c, RRect(54, 218, 166, 242, 10), lit(neon, 1.3))
    for k in range(4):
        flat(c, Circ(80 + k * 22, 230, 5), (40, 50, 60))
    # projector booth (right)
    npiece(c, RRect(760, 250, 880, 360, 2), (150, 140, 130))
    npiece(c, Poly([(750, 254), (890, 254), (870, 230), (770, 230)]), (90, 80, 80))
    flat(c, Circ(770, 290, 8), (255, 250, 220))
    # cars
    car_rear(c, 230, 470, (60, 120, 180), 1.2)
    car_rear(c, 450, 460, (230, 200, 70) if "car" not in d else (220, 90, 140), 1.2)
    car_rear(c, 680, 470, (200, 70, 60), 1.2)
    car_rear(c, 120, 590, (90, 160, 120), 1.4)
    car_rear(c, 560, 600, (180, 180, 196), 1.4)
    # speaker post (centre front)
    if "speaker" not in d:
        flat(c, Thick(350, 600, 350, 520, 4), (110, 110, 120))
        npiece(c, RRect(330, 500, 370, 530, 4), (80, 80, 90), shadow=SMALL)
        flat(c, Circ(350, 515, 8), (40, 40, 46))
    # popcorn box on a car roof
    pop = (250, 250, 246) if "popcorn" not in d else (240, 200, 60)
    npiece(c, Poly([(796, 500), (840, 500), (834, 540), (802, 540)]), (220, 60, 60), shadow=SMALL)
    flat(c, [Thick(808, 500, 806, 540, 4), Thick(828, 500, 830, 540, 4)], (250, 250, 246))
    flat(c, [Circ(804 + k * 8, 496 - (k % 2) * 4, 6) for k in range(5)], pop)
    npiece(c, RRect(760, 540, 880, 600, 6), (80, 80, 100))


L289_ELEMENTS = [
    E("beam", lambda c, m: soft_union(c, [Poly([(770, 286), (770, 294), (640, 250), (640, 60)])], (255, 250, 220), 0.12, spread=10), daynight="untinted",
      anim=dict(twinkle=0.5, twinkleSpeed=0.7)),
    E("wave", lambda c, m: [flat(c, Thick(x, 230, x + 40, 230, 2), (150, 200, 240)) for x in (270, 540)], daynight="untinted", anim=dict(bobAmplitude=(10, 0), bobSpeed=0.4)),
    E("bulbs", lambda c, m: [flat(c, Circ(x, 254, 4), (255, 220, 120)) for x in range(30, 200, 20)], daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.2)),
    E("glow", lambda c, m: soft_union(c, [RRect(252, 52, 648, 248, 1)], (180, 220, 255), 0.12, spread=24), daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.5)),
]

L289_DIFFS = [
    ("moon", 820, 60, 0),
    ("ship", 450, 200, 0),
    ("neon", 110, 230, 0),
    ("stand", 110, 275, 0),
    ("car", 450, 420, 0),
    ("speaker", 350, 530, 0),
    ("popcorn", 818, 510, 0),
]


# =================================================================== Level 290 bowling alley
def pin(c, x, base, s, col=(250, 250, 246), band=(220, 60, 60)):
    piece(c, [Ell(x, base - 10 * s, 7 * s, 10 * s), Ell(x, base - 28 * s, 4 * s, 6 * s), Circ(x, base - 36 * s, 4.4 * s)], col, border=1, shadow=None)
    flat(c, Thick(x - 4 * s, base - 24 * s, x + 4 * s, base - 24 * s, 2 * s), band)


def l290_bg(c, d):
    c.rect(0, 0, W, H, (40, 30, 70))
    # neon stars on the back wall
    for k, (x, y) in enumerate(((80, 60), (820, 60), (450, 30))):
        col = [(250, 120, 200), (90, 230, 240), (250, 220, 80)][k]
        if k == 1 and "neon" in d:
            col = (120, 250, 120)
        soft_union(c, [Poly(star_pts(x, y, 26, 11))], col, 0.4, spread=12)
        flat(c, Poly(star_pts(x, y, 22, 9)), lit(col, 1.2))
    # score screens
    for k, x in enumerate((250, 650)):
        npiece(c, RRect(x - 110, 70, x + 110, 160, 4), (30, 30, 40))
        col = (60, 120, 200) if not (k == 0 and "screen" in d) else (200, 80, 80)
        flat(c, RRect(x - 100, 80, x + 100, 150, 2), col)
        for j in range(6):
            flat(c, RRect(x - 94 + j * 32, 90, x - 70 + j * 32, 112, 1), (250, 250, 246))
            flat(c, RRect(x - 94 + j * 32, 120, x - 70 + j * 32, 140, 1), lit(col, 1.3))
    # lanes in perspective
    flat(c, RRect(0, 200, W, 230, 0), (20, 20, 30))
    for k in range(4):
        x0, x1 = 150 + k * 170, 30 + k * 280
        flat(c, Poly([(x0 - 70, 230), (x0 + 70, 230), (x1 + 120, H), (x1 - 120, H)]), (220, 180, 130))
        for j in range(-3, 4):
            flat(c, Thick(x0 + j * 20, 230, x1 + j * 34, H, 1), (200, 160, 112))
    for k in range(5):
        x0, x1 = 65 + k * 170, -110 + k * 280
        flat(c, Poly([(x0 - 15, 230), (x0 + 15, 230), (x1 + 20, H), (x1 - 20, H)]), (60, 50, 60))
    # pins at the lane ends
    for k in range(4):
        cx = 150 + k * 170
        if k == 2 and "pins" in d:
            continue
        for r, n in enumerate((4, 3, 2, 1)):
            for j in range(n):
                pin(c, cx + (j - (n - 1) / 2) * 16, 214 + r * 6, 1.0)
    # lane arrows
    arrow = (90, 60, 40) if "arrow" not in d else (240, 90, 60)
    for j in range(-2, 3):
        flat(c, Poly([(320 + j * 18, 400), (312 + j * 18, 420), (328 + j * 18, 420)]), arrow if j == 0 else (90, 60, 40))
    flat(c, Poly([(306, 404), (334, 404), (342, 430), (298, 430)]), arrow)
    # ball return (centre front)
    npiece(c, RRect(400, 470, 520, 540, 20), (60, 60, 80))
    for k, col in enumerate([(220, 60, 60), (60, 120, 220), (250, 200, 60)]):
        if k == 1 and "ball" in d:
            col = (120, 200, 120)
        npiece(c, Circ(420 + k * 40, 462, 18), col, shadow=SMALL)
        flat(c, [Circ(414 + k * 40, 456, 3), Circ(424 + k * 40, 454, 3), Circ(420 + k * 40, 464, 3)], (30, 30, 40))
    # bowler (lane 2)
    hx, hy = modern(c, 600, 520, (90, 180, 140) if "bowler" not in d else (240, 140, 60), bottom=(50, 50, 60), hair=(60, 40, 30), h=2.4)
    npiece(c, Circ(636, 490, 16), (200, 60, 200), shadow=SMALL)
    # shoe rack (left front)
    npiece(c, RRect(20, 470, 200, 600, 2), (120, 80, 60))
    for r in range(3):
        flat(c, Thick(20, 512 + r * 40, 200, 512 + r * 40, 3), (90, 60, 40))
        for k in range(4):
            col = [(220, 60, 60), (60, 120, 200), (250, 250, 246), (40, 40, 46)][(k + r) % 4]
            if r == 0 and k == 1 and "shoes" in d:
                col = (250, 200, 60)
            npiece(c, [Ell(44 + k * 44, 504 + r * 40, 18, 7)], col, shadow=None)
    # snack table (right front)
    npiece(c, [Ell(800, 540, 80, 14), RRect(794, 540, 806, 600, 2)], (200, 200, 210))
    npiece(c, Poly([(760, 532), (790, 532), (786, 500), (764, 500)]), (220, 60, 60), shadow=SMALL)
    cup = (250, 200, 60) if "cup" not in d else (90, 160, 220)
    npiece(c, RRect(810, 500, 840, 534, 3), cup, shadow=SMALL)


L290_ELEMENTS = [
    E("roll", lambda c, m: [piece(c, Circ(160, 420, 12), (60, 120, 220), shadow=None)], pivot=(160, 420),
      anim=dict(driftVelocity=(-4, -70), driftLength=170, driftFade=True, driftGrow=-0.6)),
    E("flash", lambda c, m: soft_union(c, [Circ(450, 30, 30)], (255, 230, 120), 0.3, spread=30), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.4)),
    E("disco", lambda c, m: [flat(c, Circ(x, y, 4), (255, 255, 255)) for x, y in ((200, 300), (700, 280), (420, 350))], daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=2.0, orbitRadius=(30, 10), orbitSpeed=0.2)),
]

L290_DIFFS = [
    ("neon", 820, 60, 0),
    ("screen", 250, 115, 0),
    ("pins", 490, 220, 0),
    ("arrow", 320, 415, 0),
    ("ball", 460, 462, 0),
    ("bowler", 602, 440, 0),
    ("shoes", 88, 504, 0),
    ("cup", 825, 517, 0),
]


# =================================================================== Level 291 gym
def l291_bg(c, d):
    c.rect(0, 0, W, 420, (220, 224, 230))
    # mirror wall
    flat(c, RRect(260, 60, 900, 300, 0), (200, 220, 230))
    for x in range(260, 900, 128):
        flat(c, Thick(x, 60, x, 300, 3), (180, 190, 200))
    for x in (300, 520, 760):
        flat(c, Thick(x, 80, x + 50, 140, 5), (226, 240, 246))
    # clock + poster (left top)
    clock = (60, 60, 70) if "clock" not in d else (220, 60, 60)
    piece(c, Circ(70, 70, 36), clock, border=1.5, shadow=PROP)
    flat(c, Circ(70, 70, 28), (250, 250, 246))
    flat(c, [Thick(70, 70, 70, 50, 3), Thick(70, 70, 86, 76, 3)], INK)
    poster = (250, 140, 60) if "poster" not in d else (90, 160, 220)
    wall_poster(c, 120, 40, 220, 200, poster, 2911, art=lambda c: [flat(c, [Thick(146, 120, 194, 120, 6), RRect(136, 104, 148, 136, 2), RRect(192, 104, 204, 136, 2)],
                                                                          (250, 250, 246))])
    # treadmills (back)
    for k, x in enumerate((360, 520)):
        piece(c, [Poly([(x - 70, 330), (x + 60, 330), (x + 70, 316), (x - 60, 316)]), Thick(x - 50, 316, x - 60, 230, 6), RRect(x - 80, 220, x - 40, 240, 4)],
              (70, 70, 80), border=1.2, shadow=PROP)
        flat(c, RRect(x - 76, 224, x - 44, 236, 2), (90, 200, 160))
    modern(c, 380, 318, (220, 80, 80), bottom=(40, 40, 50), hair=(200, 160, 90), h=1.8, style="long")
    # dumbbell rack (right)
    piece(c, [RRect(640, 300, 880, 316, 2), RRect(650, 316, 660, 400, 2), RRect(860, 316, 870, 400, 2), RRect(640, 360, 880, 372, 2)], (90, 90, 100), border=1.2,
          shadow=PROP)
    for r, y in enumerate((298, 358)):
        for k, x in enumerate(range(670, 860, 48)):
            col = [(220, 60, 60), (60, 120, 220), (250, 200, 60), (90, 180, 120)][k]
            if r == 0 and k == 2 and "dumbbell" in d:
                col = (200, 120, 220)
            piece(c, [RRect(x - 18, y - 16, x - 10, y, 2), RRect(x + 10, y - 16, x + 18, y, 2), Thick(x - 10, y - 8, x + 10, y - 8, 3)], col, border=1, shadow=None)
    # floor
    c.rect(0, 420, W, H, (90, 90, 100))
    for x in range(0, W, 60):
        for y in range(420, H, 60):
            if (x // 60 + y // 60) % 2:
                flat(c, RRect(x, y, x + 60, y + 60, 0), (100, 100, 110))
    flat(c, RRect(0, 410, W, 420, 0), (60, 60, 70))
    # yoga mats (left front)
    for k, y in enumerate((470, 530)):
        col = [(150, 100, 200), (90, 190, 180)][k]
        if k == 1 and "mat" in d:
            col = (240, 140, 60)
        piece(c, Poly([(30, y), (300, y - 6), (320, y + 30), (40, y + 36)]), col, border=1.2, shadow=SMALL)
    # kettlebell + water bottle on the mat
    if "kettle" not in d:
        piece(c, [Circ(260, 486, 18), Poly([(246, 470), (274, 470), (268, 454), (252, 454)])], (40, 40, 46), border=1.2, shadow=SMALL)
        flat(c, Ell(260, 460, 6, 5), (90, 90, 100))
    bottle = (90, 160, 230) if "bottle" not in d else (240, 90, 120)
    piece(c, [RRect(120, 500, 140, 540, 6), RRect(124, 490, 136, 502, 2)], bottle, border=1, shadow=SMALL)
    # weight bench (centre front)
    piece(c, [RRect(400, 520, 600, 540, 6), RRect(420, 540, 430, 590, 2), RRect(570, 540, 580, 590, 2)], (40, 40, 50), border=1.2, shadow=PROP)
    piece(c, [Thick(400, 470, 620, 470, 4), RRect(380, 440, 400, 500, 4), RRect(620, 440, 640, 500, 4), RRect(410, 470, 420, 520, 1), RRect(590, 470, 600, 520, 1)],
          (150, 150, 160), border=1.2, shadow=SMALL)
    towel = (250, 250, 246) if "towel" not in d else (240, 200, 60)
    piece(c, Poly([(460, 520), (520, 520), (526, 560), (454, 556)]), towel, border=1, shadow=SMALL)
    # water cooler (right front)
    piece(c, RRect(770, 460, 850, 590, 4), (230, 230, 236), border=1.5, shadow=PROP)
    water = (140, 200, 240) if "cooler" not in d else (240, 180, 120)
    piece(c, [RRect(780, 390, 840, 460, 14)], water, border=1.2, shadow=SMALL)
    flat(c, [Circ(790, 500, 5), Circ(830, 500, 5)], [(220, 60, 60), (60, 120, 220)][0])
    flat(c, Circ(830, 500, 5), (60, 120, 220))
    modern(c, 700, 600, (60, 70, 90), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.5)


L291_ELEMENTS = [
    E("bag", lambda c, m: [flat(c, Thick(256, 0, 256, 270, 2), (60, 60, 70)), piece(c, RRect(236, 270, 276, 380, 14), (200, 60, 60), border=1.2, shadow=PROP)],
      pivot=(256, 0), anim=dict(swingAngle=3, swingSpeed=0.7)),
    E("belt", lambda c, m: [flat(c, Thick(x, 326, x + 10, 326, 2), (110, 110, 120)) for x in range(300, 420, 24)], anim=dict(driftVelocity=(-24, 0), driftLength=24)),
    E("runner2", lambda c, m: modern(c, 540, 318, (90, 140, 200), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.8), pivot=(540, 318),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=2.0)),
]

L291_DIFFS = [
    ("clock", 70, 70, 0),
    ("poster", 170, 120, 0),
    ("dumbbell", 766, 290, 0),
    ("mat", 175, 545, 0),
    ("kettle", 260, 476, 0),
    ("bottle", 130, 516, 0),
    ("towel", 490, 540, 0),
    ("cooler", 810, 425, 0),
]


# =================================================================== Level 292 flea market
def awning(c, x0, x1, y, h, col, stripe=(250, 250, 246)):
    piece(c, RRect(x0, y, x1, y + h, 2), col, border=1.5, shadow=PROP)
    for x in range(int(x0), int(x1), 30):
        flat(c, RRect(x, y, x + 15, y + h, 0), stripe)
    for x in range(int(x0), int(x1), 30):
        piece(c, Poly([(x, y + h), (x + 30, y + h), (x + 15, y + h + 12)]), col, shadow=None)


def l292_bg(c, d):
    sky(c, (150, 200, 240), (240, 236, 220), H)
    cloud_bg(c, 450, 50, 0.6)
    far_skyline(c, 200, 40, 110, (200, 190, 180), 2921, win=(220, 214, 200))
    far_round_trees(c, 210, 26, (100, 160, 100), 2922)
    c.rect(0, 220, W, H, (200, 190, 170))
    for x in range(0, W, 40):
        flat(c, Thick(x, 220, x - 20, H, 1), (190, 180, 160))
    # stalls
    awning(c, 20, 290, 130, 40, (220, 80, 70) if "awning" not in d else (90, 150, 210))
    awning(c, 320, 580, 120, 40, (90, 150, 110))
    awning(c, 610, 880, 130, 40, (240, 180, 60))
    for x0, x1, top in ((30, 280, 170), (330, 570, 160), (620, 870, 170)):
        flat(c, [Thick(x0, top, x0, 360, 4), Thick(x1, top, x1, 360, 4)], (120, 90, 60))
        piece(c, RRect(x0 - 10, 300, x1 + 10, 360, 2), (240, 236, 226), border=1.5, shadow=PROP)
    # goods: vases + radio (left stall)
    vase = (90, 140, 200) if "vase" not in d else (220, 120, 60)
    piece(c, [Ell(70, 276, 18, 24), RRect(62, 236, 78, 256, 2)], vase, border=1.2, shadow=SMALL)
    piece(c, [Ell(110, 284, 14, 16), RRect(104, 254, 116, 272, 2)], (220, 200, 160), border=1.2, shadow=SMALL)
    radio = (150, 100, 60) if "radio" not in d else (90, 170, 160)
    piece(c, RRect(160, 230, 260, 300, 8), radio, border=1.5, shadow=SMALL)
    flat(c, [Circ(190, 266, 22), RRect(222, 246, 250, 284, 2)], (230, 210, 170))
    flat(c, Circ(190, 266, 16), lit(radio, 0.7))
    # records + books (middle stall)
    for k in range(4):
        col = (40, 40, 46)
        piece(c, Circ(370 + k * 34, 280, 22), col, border=1, shadow=None)
        lab = [(220, 60, 60), (250, 200, 60), (60, 120, 200), (120, 200, 120)][k]
        if k == 1 and "record" in d:
            lab = (250, 250, 246)
        flat(c, Circ(370 + k * 34, 280, 9), lab)
    for k in range(5):
        piece(c, RRect(500 + k * 14, 250, 512 + k * 14, 300, 1), [(160, 60, 60), (60, 90, 140), (200, 170, 90), (90, 120, 80), (120, 80, 120)][k], shadow=None)
    # lamps + chair (right stall)
    if "lamp" not in d:
        piece(c, [Ell(670, 296, 18, 5), Thick(670, 296, 670, 240, 3), Poly([(646, 240), (694, 240), (684, 210), (656, 210)])], (240, 200, 120), border=1.2, shadow=SMALL)
    teddy(c, 750, 300, 1.0, (200, 150, 90), (220, 60, 70))
    chair = (120, 170, 140) if "chair" not in d else (220, 120, 160)
    piece(c, [RRect(800, 230, 860, 244, 2), RRect(806, 180, 854, 232, 4), Thick(806, 244, 802, 298, 3), Thick(854, 244, 858, 298, 3)], chair, border=1.2, shadow=SMALL)
    # bunting
    for k in range(18):
        x = 10 + k * 50
        flat(c, Poly([(x, 30), (x + 40, 30), (x + 20, 54)]), [(220, 80, 70), (250, 200, 60), (90, 150, 210)][k % 3])
    flat(c, Thick(0, 30, W, 30, 1.4), (90, 80, 70))
    # buyers
    hx, hy = modern(c, 160, 560, (90, 150, 210), bottom=(60, 60, 80), hair=(200, 160, 90), h=2.6, style="long")
    hat = (230, 200, 120) if "hat" not in d else (220, 70, 80)
    piece(c, [Ell(hx, hy - 10, 26, 6), Ell(hx, hy - 16, 14, 9)], hat, shadow=SMALL)
    modern(c, 460, 580, (240, 200, 80), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.5)
    modern(c, 740, 590, (200, 90, 110), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.6)
    # crate of old toys (centre front)
    piece(c, RRect(540, 540, 640, 600, 3), (190, 150, 100), border=1.5, shadow=PROP)
    piece(c, [RRect(556, 520, 590, 544, 3)], (90, 160, 220), shadow=None)
    piece(c, Circ(612, 530, 14), (240, 90, 90), shadow=None)


L292_ELEMENTS = [
    bird_el("bird", 300, 80, s=9, speed=14),
    E("flap", lambda c, m: flat(c, Poly([(340, 160), (380, 160), (360, 176)]), (90, 150, 110)), pivot=(360, 160), anim=dict(swingAngle=8, swingSpeed=1.0)),
    E("balloon", lambda c, m: [flat(c, Thick(596, 300, 590, 220, 1), (90, 80, 70)), piece(c, Ell(590, 206, 14, 18), (240, 90, 140), shadow=SMALL)], pivot=(596, 300),
      anim=dict(swingAngle=6, swingSpeed=0.6)),
]

L292_DIFFS = [
    ("awning", 155, 150, 0),
    ("vase", 70, 260, 0),
    ("radio", 210, 265, 0),
    ("record", 404, 280, 0),
    ("lamp", 670, 252, 0),
    ("chair", 830, 236, 0),
    ("hat", 162, 420, 0),
]


# =================================================================== Level 293 rooftop garden
def planter(c, x0, x1, base, wood=(150, 110, 70)):
    piece(c, RRect(x0, base - 50, x1, base, 2), wood, border=1.5, shadow=PROP)
    for y in range(int(base) - 40, int(base), 16):
        flat(c, Thick(x0, y, x1, y, 1.4), lit(wood, 0.86))
    flat(c, RRect(x0 + 4, base - 56, x1 - 4, base - 48, 2), (110, 80, 60))


def l293_bg(c, d):
    sky(c, (130, 190, 240), (250, 220, 190), H)
    sun_bg(c, 450, 90, 30, col=(250, 200, 110))
    far_skyline(c, 300, 80, 220, (150, 170, 200), 2931, win=(190, 206, 226))
    far_skyline(c, 330, 50, 150, (120, 140, 170), 2932, win=(170, 186, 210))
    # water tank on stilts (left)
    tank = (150, 110, 80) if "tank" not in d else (90, 140, 190)
    piece(c, [Thick(60, 330, 70, 200, 4), Thick(160, 330, 150, 200, 4)], (90, 90, 100), shadow=PROP)
    piece(c, [RRect(50, 120, 170, 210, 4), Poly([(46, 122), (174, 122), (110, 80)])], tank, border=1.5, shadow=PROP)
    for y in (140, 170, 196):
        flat(c, Thick(50, y, 170, y, 2), lit(tank, 0.75))
    # solar panels (right)
    sol = (60, 80, 140) if "solar" not in d else (150, 160, 170)
    for x in (700, 800):
        piece(c, Poly([(x - 40, 330), (x + 40, 330), (x + 50, 280), (x - 30, 280)]), sol, border=1.5, shadow=PROP)
        flat(c, [Thick(x - 34, 305, x + 44, 305, 1.4), Thick(x + 5, 280, x, 330, 1.4)], lit(sol, 1.4))
    # roof deck
    c.rect(0, 330, W, H, (190, 160, 120))
    planks(c, 330, (190, 160, 120), (170, 140, 100), seed=2931)
    flat(c, RRect(0, 326, W, 334, 0), (120, 120, 130))
    # pergola with string lights (centre)
    piece(c, [Thick(320, 460, 320, 250, 6), Thick(600, 460, 600, 250, 6), Thick(300, 250, 620, 250, 6)], (160, 120, 80), shadow=PROP)
    string_lights(c, 320, 256, 600, 256, 10, [(250, 220, 120)], sag=26)
    # planter beds
    planter(c, 30, 280, 470)
    for k, x in enumerate(range(50, 270, 40)):
        flat(c, Thick(x, 414, x, 370, 2), (90, 140, 70))
        col = (220, 60, 50) if not (k in (1, 2) and "tomato" in d) else (250, 200, 60)
        flat(c, [Circ(x - 6, 380, 7), Circ(x + 6, 396, 7)], col)
        flat(c, [Ell(x - 8, 372, 8, 4), Ell(x + 8, 388, 8, 4)], (90, 150, 70))
    planter(c, 640, 880, 480)
    for x in range(660, 880, 34):
        piece(c, [Circ(x, 420, 14), Circ(x + 10, 410, 10)], (100, 170, 90), shadow=SMALL)
    # sunflower (right planter)
    flat(c, Thick(860, 430, 860, 340, 3), (90, 140, 60))
    sf = (250, 200, 40) if "sunflower" not in d else (220, 110, 160)
    piece(c, Circ(860, 340, 24), sf, shadow=SMALL)
    flat(c, Circ(860, 340, 10), (120, 80, 40))
    # deck chairs + umbrella (centre)
    umb = (240, 120, 100) if "umbrella" not in d else (90, 180, 170)
    flat(c, Thick(460, 470, 460, 330, 3), (200, 200, 210))
    piece(c, Poly([(380, 340), (540, 340), (460, 296)]), umb, border=1.5, shadow=PROP)
    chair = (90, 150, 210) if "chair" not in d else (250, 200, 60)
    piece(c, Poly([(380, 520), (460, 520), (470, 470), (440, 470)]), chair, border=1.2, shadow=PROP)
    flat(c, [Thick(384, 520, 380, 560, 3), Thick(456, 520, 462, 560, 3)], (150, 120, 90))
    modern(c, 530, 560, (250, 250, 246), bottom=(90, 120, 160), hair=(40, 30, 30), h=2.2, style="long")
    # birdhouse on a pole (left front)
    flat(c, Thick(120, 600, 120, 500, 4), (120, 90, 60))
    if "birdhouse" not in d:
        piece(c, [RRect(96, 470, 144, 510, 2), Poly([(90, 472), (150, 472), (120, 446)])], (220, 90, 70), border=1.2, shadow=SMALL)
        flat(c, Circ(120, 488, 7), (60, 40, 30))
    # watering can (right front)
    can = (90, 170, 160) if "can" not in d else (240, 140, 60)
    piece(c, [RRect(740, 540, 820, 590, 8), Thick(820, 554, 860, 524, 6), Thick(752, 540, 790, 520, 4)], can, border=1.5, shadow=PROP)


L293_ELEMENTS = [
    lights_el("lights", [(320 + k * 28, 256 + 26 * math.sin(math.pi * k / 10)) for k in range(11)], [(255, 220, 120)]),
    bird_el("bird", 300, 60, s=9, speed=14),
    E("bee", lambda c, m: piece(c, Ell(760, 380, 6, 4), (250, 210, 60), shadow=None), pivot=(760, 380), anim=dict(orbitRadius=(40, 16), orbitSpeed=0.3)),
    E("leaf", lambda c, m: flat(c, Ell(200, 360, 10, 4), (90, 150, 70)), pivot=(200, 370), anim=dict(swingAngle=10, swingSpeed=0.8)),
]

L293_DIFFS = [
    ("tank", 110, 150, 0),
    ("solar", 750, 305, 0),
    ("tomato", 110, 388, 0),
    ("umbrella", 460, 324, 0),
    ("sunflower", 860, 340, 0),
    ("chair", 440, 500, 0),
    ("birdhouse", 120, 480, 0),
    ("can", 790, 560, 0),
]


# =================================================================== Level 294 subway car
def seat_row(c, x0, x1, col):
    piece(c, [RRect(x0, 380, x1, 400, 4), RRect(x0, 300, x1, 384, 6)], col, border=1.5, shadow=PROP)
    for x in range(int(x0) + 60, int(x1), 60):
        flat(c, Thick(x, 306, x, 396, 2), lit(col, 0.8))


def l294_bg(c, d):
    c.rect(0, 0, W, H, (220, 224, 226))
    flat(c, RRect(0, 0, W, 40, 0), (240, 240, 236))
    # windows (tunnel)
    for x0 in (40, 330, 620):
        piece(c, RRect(x0, 120, x0 + 240, 280, 16), (180, 186, 190), border=1.5, shadow=PROP)
        flat(c, RRect(x0 + 10, 130, x0 + 230, 270, 12), (30, 34, 44))
    # route map + posters above windows
    mp = (250, 250, 246) if "map" not in d else (250, 220, 150)
    piece(c, RRect(60, 50, 440, 100, 3), mp, border=1.2, shadow=SMALL)
    flat(c, Thick(80, 76, 420, 76, 4), (60, 140, 90))
    for x in range(90, 420, 40):
        flat(c, Circ(x, 76, 6), (250, 250, 246))
        c.ellipse_ring(x, 76, 6, 6, 2, (60, 140, 90))
    ad = (240, 150, 60) if "ad" not in d else (120, 120, 220)
    piece(c, RRect(480, 48, 640, 104, 3), ad, border=1.2, shadow=SMALL)
    sign_box(c, 500, 60, 620, 92, ad, 2941, vertical=False)
    piece(c, RRect(680, 48, 860, 104, 3), (90, 160, 210), border=1.2, shadow=SMALL)
    flat(c, Circ(720, 76, 16), (250, 230, 120))
    # grab rail + straps
    flat(c, Thick(0, 30, W, 30, 4), (180, 180, 190))
    for k, x in enumerate(range(60, W, 80)):
        col = (250, 250, 246) if not (k == 5 and "strap" in d) else (240, 120, 60)
        flat(c, Thick(x, 30, x, 128, 4), (120, 120, 130))
        c.ellipse_ring(x, 144, 14, 16, 5, col)
    # seats
    seat_row(c, 20, 420, (60, 110, 160))
    seat_row(c, 480, 880, (60, 110, 160))
    if "seat" in d:
        piece(c, RRect(662, 302, 718, 398, 4), (200, 90, 80), shadow=None)
    flat(c, [Thick(450, 30, 450, 600, 6)], (190, 190, 200))
    # floor
    c.rect(0, 400, W, H, (150, 150, 156))
    for x in range(0, W, 30):
        flat(c, Thick(x, 400, x, H, 1), (140, 140, 146))
    # passengers seated
    hx, hy = modern(c, 100, 384, (220, 80, 80), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.0)
    if "beanie" not in d:
        piece(c, [Ell(hx, hy - 8, 17, 11), Circ(hx, hy - 21, 6)], (240, 200, 60), border=1, shadow=None)
        flat(c, Thick(hx - 16, hy - 4, hx + 16, hy - 4, 4), (220, 160, 40))
    hx, hy = modern(c, 250, 384, (90, 160, 110), bottom=(50, 50, 60), hair=(200, 160, 90), h=2.0, style="long")
    book = (200, 60, 60) if "book" not in d else (60, 110, 200)
    piece(c, RRect(236, 330, 276, 356, 2), book, border=1, shadow=SMALL)
    modern(c, 360, 384, (240, 220, 160), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.0)
    modern(c, 560, 384, (90, 90, 140), bottom=(50, 50, 60), hair=(30, 30, 34), h=2.0, glasses=True)
    modern(c, 820, 384, (250, 160, 60), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.0, style="twin")
    # standing passenger with a bag (centre front)
    hx, hy = modern(c, 680, 600, (60, 70, 90), bottom=(40, 40, 50), hair=(60, 40, 30), h=2.8)
    bag = (150, 100, 60) if "bag" not in d else (220, 60, 120)
    piece(c, [RRect(700, 500, 760, 560, 6), Thick(706, 500, 690, 460, 3)], bag, border=1.5, shadow=PROP)
    # umbrella leaning (left front)
    if "umbrella" not in d:
        piece(c, [Poly([(160, 590), (180, 590), (200, 470), (186, 466)]), Thick(166, 590, 160, 600, 3)], (40, 60, 120), border=1.2, shadow=SMALL)
        flat(c, Thick(196, 470, 210, 456, 3), (120, 80, 60))
    # suitcase (centre front)
    piece(c, [RRect(380, 480, 460, 590, 8), Thick(404, 480, 404, 456, 3), Thick(436, 480, 436, 456, 3), Thick(404, 456, 436, 456, 3)], (220, 200, 90), border=1.5,
          shadow=PROP)
    flat(c, [Circ(392, 594, 5), Circ(448, 594, 5)], (40, 40, 46))


def streak(eid, y, phase):
    return E(eid, lambda c, m: [soft_union(c, [RRect(x, y, x + 60, y + 4, 2)], (255, 230, 160), 0.8, spread=6) for x in (60, 350, 640)], daynight="untinted",
             anim=dict(driftVelocity=(-480, 0), driftLength=240, driftStart=-60, driftFade=True, phase=phase))


L294_ELEMENTS = [
    streak("s1", 170, 0.0), streak("s2", 220, 0.4), streak("s3", 250, 0.7),
    E("sway1", lambda c, m: [flat(c, Thick(140, 30, 140, 128, 4), (120, 120, 130)), c.ellipse_ring(140, 144, 14, 16, 5, (250, 250, 246))], pivot=(140, 30),
      anim=dict(swingAngle=4, swingSpeed=0.6)),
    E("rock", lambda c, m: flat(c, Thick(0, 596, W, 596, 4), (120, 120, 126)), anim=dict(bobAmplitude=(0, 1.5), bobSpeed=2.0)),
]

L294_DIFFS = [
    ("map", 250, 75, 0),
    ("ad", 560, 76, 0),
    ("strap", 460, 144, 0),
    ("beanie", 101, 280, 0),
    ("book", 256, 343, 0),
    ("seat", 690, 350, 0),
    ("bag", 728, 520, 0),
    ("umbrella", 182, 528, 0),
]


LEVELS = [
    ("Level285", "邮局", l285_bg, L285_ELEMENTS, L285_DIFFS, 60, OPTS),
    ("Level286", "宠物医院", l286_bg, L286_ELEMENTS, L286_DIFFS, 60, OPTS),
    ("Level287", "滑板公园", l287_bg, L287_ELEMENTS, L287_DIFFS, 60, OPTS),
    ("Level288", "水上乐园", l288_bg, L288_ELEMENTS, L288_DIFFS, 60, OPTS),
    ("Level289", "露天电影院", l289_bg, L289_ELEMENTS, L289_DIFFS, 60, OPTS),
    ("Level290", "保龄球馆", l290_bg, L290_ELEMENTS, L290_DIFFS, 60, OPTS),
    ("Level291", "健身房", l291_bg, L291_ELEMENTS, L291_DIFFS, 60, OPTS),
    ("Level292", "跳蚤市场", l292_bg, L292_ELEMENTS, L292_DIFFS, 60, OPTS),
    ("Level293", "屋顶花园", l293_bg, L293_ELEMENTS, L293_DIFFS, 60, OPTS),
    ("Level294", "地铁车厢", l294_bg, L294_ELEMENTS, L294_DIFFS, 60, OPTS),
]
