# -*- coding: utf-8 -*-
"""Everyday-town themes, part 2 (paper-craft side views, full-bleed, no real brands or logos):
  Level510 水族馆     - an aquarium hall: a huge tank with coral, fish, a sunken chest, visitors in front
  Level511 马戏团     - inside a circus tent: striped canvas, ring, trapeze, elephant on a drum, clown, ringmaster
  Level512 花店       - a flower shop: tiered flower buckets, hanging baskets, florist at the counter, shop window
  Level513 建筑工地   - a construction site: tower crane, steel frame, scaffolding, excavator, dump truck, workers
  Level514 火车站台   - a modern train platform: canopy, waiting train, timetable screen, clock, passengers
  Level515 恐龙博物馆 - a museum hall: T-rex skeleton on a plinth, banners, fossil cases, a school group
  Level516 雨天街角咖啡 - a street-corner cafe: striped awning, outdoor tables, bicycle, passers-by; rain showers
  Level517 南瓜农场   - an autumn farm: barn, silo, tractor, scarecrow, pumpkin patch; day / night with glowing lanterns
  Level518 露天溜冰场 - an outdoor ice rink in town: big decorated tree, skaters, cocoa stand, string lights; snow
  Level519 宠物店     - a pet shop: fish tank, birdcage, cat tree, puppy pen, food shelves, hamster wheel
"""
import math
import random

from fdcore import CLEAR, E, H, OVERCAST, RAIN, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bubbles_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_modern import crowd
from levels_daily import balloon_bunch, elephant
from stylekit import celestial, day_night, moon_element, star_field, sun_element, window_glow
from weather import cloud, paper_sun, puddles, rain_layer, snow_layer, splash_rings

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


# =================================================================== Level 510 aquarium
TANK = (30, 30, 870, 460)


def coral(c, x, base, s, col):
    piece(c, [Thick(x, base, x, base - 50 * s, 7 * s), Thick(x, base - 20 * s, x - 22 * s, base - 46 * s, 6 * s),
              Thick(x - 22 * s, base - 46 * s, x - 24 * s, base - 66 * s, 5 * s), Thick(x, base - 30 * s, x + 20 * s, base - 58 * s, 6 * s),
              Thick(x + 20 * s, base - 58 * s, x + 18 * s, base - 76 * s, 5 * s), Circ(x, base - 52 * s, 6 * s)], col, shadow=SMALL)


def big_fish(c, x, y, s, body, stripe=(250, 250, 250), right=True):
    d = 1 if right else -1
    piece(c, [Ell(x, y, 34 * s, 20 * s), Poly([(x - 28 * s * d, y), (x - 54 * s * d, y - 20 * s), (x - 54 * s * d, y + 20 * s)]),
              Poly([(x - 6 * s * d, y - 18 * s), (x + 10 * s * d, y - 34 * s), (x + 16 * s * d, y - 16 * s)])], body, border=1.5, shadow=SMALL)
    flat(c, [Thick(x - 4 * s * d, y - 18 * s, x - 4 * s * d, y + 18 * s, 6 * s), Thick(x + 14 * s * d, y - 14 * s, x + 14 * s * d, y + 14 * s, 5 * s)], stripe)
    flat(c, Circ(x + 22 * s * d, y - 5 * s, 3.4 * s), INK)


def l510_bg(c, d):
    c.rect(0, 0, W, H, (30, 40, 70))
    # tank water
    x0, y0, x1, y1 = TANK
    c.gradient(y0, y1, (60, 160, 210), (30, 90, 160))
    c.rect(0, 0, x0, H, (30, 40, 70))
    c.rect(x1, 0, W, H, (30, 40, 70))
    c.rect(0, 0, W, y0, (30, 40, 70))
    for k in range(6):                                      # light shafts
        flat(c, Poly([(80 + k * 150, y0), (130 + k * 150, y0), (90 + k * 150, 330), (40 + k * 150, 330)]), (140, 210, 240, 0.18))
    # rocks + sand
    piece(c, Poly([(x0, 380), (200, 360), (420, 372), (640, 356), (x1, 370), (x1, y1), (x0, y1)]), (230, 210, 160), shadow=SMALL)
    piece(c, Poly([(x0, 380), (x0, 230), (60, 200), (120, 240), (150, 380)]), (90, 100, 120), shadow=PROP)
    piece(c, Poly([(700, 370), (730, 260), (800, 230), (x1, 250), (x1, 372)]), (90, 100, 120), shadow=PROP)
    # coral garden
    coral(c, 200, 380, 1.4, (250, 120, 110) if "coral" not in d else (170, 120, 230))
    coral(c, 260, 376, 1.0, (250, 200, 90))
    coral(c, 520, 376, 1.2, (240, 120, 170))
    coral(c, 760, 360, 1.1, (250, 150, 80))
    for x in (110, 340, 450, 610, 850):
        flat(c, [Thick(x, 380, x - 6, 300, 5), Thick(x + 8, 380, x + 14, 316, 5)], (60, 150, 90))
    # sunken chest
    if "chest" not in d:
        piece(c, [RRect(600, 344, 666, 380, 4), Poly([(600, 346), (666, 346), (656, 326), (610, 326)])], (150, 100, 60), border=1.5, shadow=SMALL)
        flat(c, [Thick(600, 352, 666, 352, 3), RRect(626, 348, 640, 362, 2)], (230, 190, 80))
    # starfish + shells
    piece(c, Poly(star_pts(400, 380, 22, 9)), (250, 150, 60) if "star" not in d else (110, 200, 230), border=1, shadow=SMALL)
    flat(c, [Ell(470, 390, 8, 5), Ell(320, 392, 7, 4)], (250, 236, 220))
    # static big fish
    big_fish(c, 420, 230, 1.5, (250, 150, 50) if "fish" not in d else (120, 190, 240))
    big_fish(c, 690, 170, 1.0, (250, 220, 70), stripe=(40, 40, 60), right=False)
    big_fish(c, 160, 140, 0.9, (120, 190, 240))
    # tank frame
    for r in (TANK,):
        flat(c, [Thick(r[0], r[1], r[2], r[1], 10), Thick(r[0], r[3], r[2], r[3], 12), Thick(r[0], r[1], r[0], r[3], 10), Thick(r[2], r[1], r[2], r[3], 10)],
             (60, 66, 84))
    flat(c, Thick(450, 30, 450, 460, 6), (60, 66, 84))
    # floor
    c.rect(0, 466, W, H, (40, 50, 80))
    for y in range(480, H, 26):
        flat(c, Thick(0, y, W, y, 1.2), (50, 60, 92))
    # info plaque
    piece(c, [RRect(100, 480, 240, 536, 4), RRect(166, 536, 174, 590, 2)], (70, 80, 110), border=1.2, border_col=(110, 120, 150), shadow=SMALL)
    flat(c, Circ(130, 508, 16), (250, 150, 50) if "plaque" not in d else (250, 120, 160))
    sign_box(c, 154, 496, 228, 520, (220, 226, 240), 5101, vertical=False)
    # bench
    piece(c, [RRect(300, 540, 520, 554, 3), RRect(310, 554, 320, 590, 2), RRect(500, 554, 510, 590, 2)], (110, 90, 80), border=1.2,
          border_col=(150, 130, 120), shadow=SMALL)
    # visitors (backs to us, a little dimmed by the dark hall)
    modern(c, 380, 546, (200, 110, 110), bottom=(50, 50, 70), hair=(40, 30, 30), h=2.0)
    modern(c, 450, 546, (240, 200, 120), bottom=(50, 50, 70), hair=(90, 60, 40), h=1.9, style="long")
    modern(c, 600, 600, (90, 130, 190), bottom=(40, 40, 60), hair=(90, 60, 40), h=2.6)
    modern(c, 660, 600, (230, 200, 90) if "shirt" not in d else (120, 200, 120), bottom=(60, 60, 80), hair=(220, 180, 90), h=1.8, style="twin")
    flat(c, Thick(676, 540, 704, 500, 4), (246, 214, 186))
    modern(c, 820, 600, (150, 120, 180), bottom=(50, 50, 70), hair=(130, 130, 140), h=2.5, glasses=True)
    modern(c, 40, 600, (120, 170, 140), bottom=(50, 50, 70), hair=(40, 30, 30), h=2.4)


def swim(eid, x, y, s, col, speed, start):
    return E(eid, lambda c, m: big_fish(c, x, y, s, col, right=speed > 0), anim=dict(drift_across(x - 60 * s, x + 40 * s, speed, start=start),
                                                                                    bobAmplitude=(0, 4), bobSpeed=0.5))


L510_ELEMENTS = [
    swim("fishA", 0, 92, 0.5, (250, 230, 120), 30, 200),
    swim("fishB", 0, 110, 0.4, (250, 120, 150), -24, 600),
    E("jelly", lambda c, m: (piece(c, Poly([(570 + 22 * math.cos(math.radians(a)), 120 - 18 * math.sin(math.radians(a))) for a in range(0, 181, 15)]),
                                   (240, 200, 240), border=1, shadow=SMALL),
                             flat(c, [Thick(556 + k * 9, 120, 554 + k * 9, 160, 2) for k in range(4)], (240, 200, 240, 0.7))),
      pivot=(570, 130), anim=dict(bobAmplitude=(0, 14), bobSpeed=0.2, stretch=(0.05, 0.1), scaleSpeed=0.6)),
    E("weed", lambda c, m: flat(c, [Thick(780, 360, 790, 300, 6), Thick(800, 360, 812, 310, 5)], (70, 170, 100)), pivot=(795, 360),
      anim=dict(swingAngle=8, swingSpeed=0.35)),
] + bubbles_el("bub", 90, 360, n=4, r=5, rise=(2, 30), length=200)

L510_DIFFS = [
    ("coral", 200, 330, 0),
    ("chest", 633, 352, 0),
    ("star", 400, 380, 0),
    ("fish", 420, 230, 0),
    ("plaque", 130, 508, 0),
    ("shirt", 661, 543, 0),
]


# =================================================================== Level 511 circus tent
def l511_bg(c, d):
    # tent canvas: stripes radiating from the top centre
    c.rect(0, 0, W, H, (250, 244, 232))
    for k in range(-9, 10):
        a0, a1 = math.radians(90 + k * 10 - 5), math.radians(90 + k * 10)
        flat(c, Poly([(450, -40), (450 + 1200 * math.cos(a0), -40 + 1200 * math.sin(a0)), (450 + 1200 * math.cos(a1), -40 + 1200 * math.sin(a1))]),
             (210, 50, 60))
    # bunting
    for row, y in enumerate((70, 110)):
        for x in range(0, 900, 36):
            col = [(250, 200, 50), (60, 120, 210), (90, 180, 100)][(x // 36 + row) % 3]
            if row == 0 and x in (684, 720) and "pennant" in d:
                col = (240, 120, 200)
            flat(c, Poly([(x, y), (x + 30, y), (x + 15, y + 26)]), col)
        flat(c, Thick(0, y, W, y, 2), (120, 90, 70))
    # spotlight housings in the top corners
    for x, col in ((50, (60, 60, 70)), (850, (60, 60, 70) if "spot" not in d else (230, 190, 60))):
        piece(c, [RRect(x - 24, 10, x + 24, 44, 6), Thick(x, 0, x, 12, 4)], col, border=1.5, shadow=PROP)
        flat(c, Ell(x, 44, 16, 5), (255, 250, 220))
    # tent poles
    for x in (150, 750):
        piece(c, RRect(x - 7, 0, x + 7, 420, 2), (230, 200, 120), shadow=PROP)
    # audience stands (both sides)
    for x0, x1 in ((-10, 230), (670, 910)):
        piece(c, Poly([(x0, 300), (x1, 340), (x1, 470), (x0, 470)]), (110, 70, 80), shadow=LAYER)
        crowd(c, x0 + 12, x1 - 6, 322 if x0 < 0 else 330, 7, 5110 + x0, step=15, dy=19)
    # ring floor
    piece(c, Ell(450, 470, 330, 90), (220, 180, 120), shadow=LAYER)
    for k in range(40):
        rnd = random.Random(5112 + k)
        flat(c, Ell(450 + rnd.uniform(-280, 280), 470 + rnd.uniform(-60, 60), 8, 2), (206, 166, 108))
    c.ellipse_ring(450, 470, 330, 90, 14, (220, 50, 60))
    for k in range(16):
        a = 2 * math.pi * k / 16
        flat(c, Poly(star_pts(450 + 330 * math.cos(a), 470 + 90 * math.sin(a), 7, 3)), (250, 220, 80))
    # elephant on a drum (centre)
    piece(c, [RRect(380, 420, 520, 470, 6)], (60, 110, 210) if "drum" not in d else (250, 190, 60), border=1.5, shadow=PROP)
    flat(c, [Thick(380, 432, 520, 432, 4), Thick(380, 458, 520, 458, 4)], (250, 220, 80))
    flat(c, [Poly(star_pts(450, 445, 10, 4))], (250, 250, 250))
    elephant(c, 450, 422, s=1.3, col=(176, 176, 190))
    flat(c, [Poly([(420, 340), (480, 340), (450, 322)])], (220, 50, 60))                   # little hat
    flat(c, Circ(450, 320, 4), (250, 220, 80))
    # ringmaster (left)
    modern(c, 250, 560, (200, 40, 50), bottom=(30, 30, 40), hair=(60, 40, 30), h=2.3)
    hx, hy = 252, 560 - 46 * 2.3
    hat = (30, 30, 40) if "hat" not in d else (120, 50, 170)
    flat(c, [RRect(hx - 12, hy - 40, hx + 12, hy - 10, 2), RRect(hx - 18, hy - 12, hx + 18, hy - 7, 2)], hat)
    flat(c, RRect(hx - 12, hy - 18, hx + 12, hy - 13, 1), (250, 200, 50))
    flat(c, [Thick(270, 500, 300, 470, 3)], (40, 40, 50))
    # clown (right)
    modern(c, 640, 570, (250, 210, 60), bottom=(60, 130, 220), hair=(250, 120, 40) if "wig" not in d else (80, 170, 240), h=2.2, style="twin")
    flat(c, [Circ(640 - 4, 540 - 40, 5), Circ(640 + 4, 556 - 40, 5)], (220, 50, 60))
    flat(c, Circ(650, 570 - 46 * 2.2, 5), (240, 50, 60))
    flat(c, [Ell(624, 571, 14, 6), Ell(660, 571, 14, 6)], (220, 50, 60))
    # popcorn box in the front row
    piece(c, Poly([(820, 600), (860, 600), (866, 548), (814, 548)]), (250, 250, 250), border=1.2, shadow=SMALL)
    flat(c, [Thick(828, 548, 826, 600, 5), Thick(848, 548, 850, 600, 5)], (220, 50, 60) if "popcorn" not in d else (60, 120, 210))
    flat(c, [Circ(820 + k * 8, 546 - (k % 2) * 4, 6) for k in range(6)], (250, 240, 200))


def trapeze(c, m):
    flat(c, [Thick(410, 0, 420, 150, 1.5), Thick(490, 0, 480, 150, 1.5)], (90, 80, 70))
    piece(c, RRect(414, 148, 486, 156, 3), (230, 200, 120), shadow=SMALL)
    modern(c, 450, 214, (240, 120, 200), bottom=(240, 120, 200), hair=(40, 30, 30), h=1.4, style="long")
    flat(c, [Thick(440, 166, 438, 152, 3), Thick(462, 166, 464, 152, 3)], (246, 214, 186))


L511_ELEMENTS = [
    E("trapeze", trapeze, pivot=(450, 0), anim=dict(swingAngle=14, swingSpeed=0.35)),
    E("spotL", lambda c, m: soft_union(c, [Poly([(40, 30), (60, 30), (390, 470), (300, 480)])], (255, 250, 220), 0.18, spread=14),
      pivot=(50, 30), anim=dict(swingAngle=4, swingSpeed=0.2)),
    E("spotR", lambda c, m: soft_union(c, [Poly([(840, 30), (860, 30), (600, 480), (510, 470)])], (255, 250, 220), 0.18, spread=14),
      pivot=(850, 30), anim=dict(swingAngle=4, swingSpeed=0.2, phase=0.5)),
    E("balloons", balloon_bunch(690, 440, [(240, 80, 90), (90, 170, 240), (250, 200, 60)], string_to=(676, 500)), pivot=(676, 500),
      anim=dict(swingAngle=6, swingSpeed=0.5)),
    E("juggle", lambda c, m: [piece(c, Circ(600 + k * 18, 440 - (k % 2) * 16, 6), col, shadow=SMALL)
                              for k, col in enumerate(((250, 80, 80), (80, 200, 120), (80, 140, 240)))],
      pivot=(618, 440), anim=dict(rotateSpeed=90)),
]

L511_DIFFS = [
    ("pennant", 717, 80, 0),
    ("spot", 850, 28, 0),
    ("drum", 450, 452, 0),
    ("hat", 252, 420, 0),
    ("wig", 641, 470, 0),
    ("popcorn", 840, 574, 0),
]


# =================================================================== Level 512 flower shop
def bloom(c, x, y, col, r=7):
    flat(c, [Circ(x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a), r * 0.55) for a in [k * math.pi * 2 / 5 for k in range(5)]], col)
    flat(c, Circ(x, y, r * 0.35), (250, 220, 90))


def bucket(c, x, base, col, flowers, seed):
    rnd = random.Random(seed)
    for k in range(7):
        fx = x - 18 + k * 6 + rnd.uniform(-2, 2)
        fy = base - 70 - rnd.uniform(0, 26)
        flat(c, Thick(x - 8 + k * 2.6, base - 30, fx, fy, 1.6), (70, 140, 80))
        bloom(c, fx, fy, flowers)
    piece(c, Poly([(x - 22, base - 36), (x + 22, base - 36), (x + 16, base), (x - 16, base)]), col, border=1.2, shadow=SMALL)


def l512_bg(c, d):
    c.rect(0, 0, W, 470, (236, 244, 232))
    for x in range(0, W, 40):
        flat(c, RRect(x, 0, x + 20, 470, 0), (228, 238, 224))
    # big shop window (back), street outside
    piece(c, RRect(260, 40, 640, 250, 4), (250, 250, 246), border=2, shadow=PROP)
    flat(c, RRect(272, 52, 628, 238, 2), (190, 220, 240))
    far_skyline(c, 238, 30, 120, (200, 210, 226), 5121, win=(220, 228, 240), x0=272, x1=628)
    c.rect(272, 238, 628, 250, (250, 250, 246))
    flat(c, [Thick(450, 52, 450, 238, 4)], (250, 250, 246))
    piece(c, RRect(300, 14, 600, 40, 4), (90, 150, 110), border=1.5, shadow=SMALL)
    sign_box(c, 320, 20, 580, 34, (250, 250, 240), 5122, vertical=False)
    # wall shelves with potted plants (left)
    for k, y in enumerate((120, 220)):
        piece(c, RRect(20, y, 230, y + 10, 2), (190, 150, 110), border=1.2, shadow=PROP)
        for i in range(4):
            x = 46 + i * 52
            pot = (220, 120, 90) if not (k == 1 and i == 2 and "pot" in d) else (90, 150, 220)
            piece(c, [Ell(x, y - 30, 16, 18), Ell(x - 10, y - 38, 8, 12), Ell(x + 10, y - 40, 8, 12)], (80, 150, 90), shadow=SMALL)
            piece(c, Poly([(x - 14, y - 18), (x + 14, y - 18), (x + 10, y), (x - 10, y)]), pot, border=1, shadow=SMALL)
    # framed botanical prints (right)
    for k, (x, y) in enumerate(((690, 60), (790, 60), (690, 170), (790, 170))):
        piece(c, RRect(x, y, x + 80, y + 90, 2), (190, 150, 110), border=1.2, shadow=PROP)
        flat(c, RRect(x + 8, y + 8, x + 72, y + 82, 1), (250, 248, 236))
        flat(c, Thick(x + 40, y + 76, x + 40, y + 30, 2), (80, 140, 90))
        bloom(c, x + 40, y + 28, [(240, 110, 130), (250, 180, 60), (150, 120, 220), (90, 170, 230)][k], r=14)
    # tiered stand with buckets
    for k, (y, x0, x1) in enumerate(((330, 20, 600), (400, 0, 620), (470, -10, 640))):
        piece(c, RRect(x0, y, x1, y + 12, 2), (170, 130, 90), border=1.2, shadow=PROP)
    rows = [(330, range(60, 600, 90)), (400, range(40, 620, 90)), (470, range(20, 640, 90))]
    pal = [(240, 80, 100), (250, 200, 60), (250, 250, 250), (170, 120, 230), (250, 140, 60), (240, 150, 190), (90, 160, 230)]
    n = 0
    for y, xs in rows:
        for x in xs:
            fl = pal[n % len(pal)]
            if y == 400 and x == 310 and "tulips" in d:
                fl = (90, 200, 120)
            bucket(c, x, y, (180, 186, 200), fl, 5123 + n)
            n += 1
    # floor
    c.rect(0, 470, W, H, (200, 180, 160))
    for y in range(482, H, 22):
        flat(c, Thick(0, y, W, y, 1.2), (186, 166, 146))
    piece(c, RRect(-10, 482, 660, 520, 0), (170, 130, 90), shadow=SMALL)
    # counter + florist (right)
    piece(c, RRect(660, 380, 910, 560, 4), (190, 150, 110), border=2, shadow=PROP)
    modern(c, 790, 380, (250, 250, 250), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.0, style="long")
    flat(c, RRect(778, 320, 802, 372, 3), (90, 150, 110) if "apron" not in d else (230, 120, 150))
    flat(c, RRect(660, 380, 910, 392, 3), (160, 120, 84))
    # bouquet wrapped in paper on the counter
    piece(c, Poly([(700, 380), (740, 380), (760, 330), (680, 330)]), (250, 236, 210), border=1.2, shadow=SMALL)
    for k in range(5):
        bloom(c, 690 + k * 15, 326 - (k % 2) * 8, [(240, 80, 100), (250, 250, 250), (250, 200, 60)][k % 3], r=9)
    rib = (220, 60, 90) if "ribbon" not in d else (90, 140, 230)
    flat(c, [Poly([(720, 362), (696, 350), (696, 374)]), Poly([(720, 362), (744, 350), (744, 374)]), Circ(720, 362, 6),
             Thick(716, 366, 708, 384, 4), Thick(724, 366, 732, 384, 4)], rib)
    # crate of sunflowers on the floor
    piece(c, RRect(40, 540, 200, 596, 3), (190, 150, 100), border=1.5, shadow=PROP)
    flat(c, [Thick(40, 568, 200, 568, 2)], (160, 120, 80))
    for k in range(5):
        x = 60 + k * 32
        flat(c, Thick(x, 540, x + 4, 504, 3), (80, 140, 80))
        flat(c, [Circ(x + 4 + 10 * math.cos(a), 500 + 10 * math.sin(a), 6) for a in [j * math.pi / 4 for j in range(8)]], (250, 200, 50))
        flat(c, Circ(x + 4, 500, 7), (120, 80, 40))
    # watering can on the floor
    piece(c, [RRect(560, 540, 610, 580, 8), Thick(608, 554, 640, 532, 5)], (90, 170, 160) if "can" not in d else (250, 190, 60), border=1.2,
          shadow=PROP)
    c.ellipse_ring(574, 534, 16, 12, 3, (70, 130, 120))
    # customer
    modern(c, 480, 596, (240, 140, 90), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.1)
    piece(c, RRect(844, 520, 880, 560, 4), (250, 250, 250), border=1, shadow=SMALL)


def hanging_basket(x, col):
    def d(c, m):
        flat(c, [Thick(x, 0, x - 14, 60, 1.2), Thick(x, 0, x + 14, 60, 1.2)], (120, 100, 80))
        piece(c, Ell(x, 64, 22, 10), (170, 120, 80), shadow=SMALL)
        piece(c, [Ell(x - 14, 72, 8, 14), Ell(x + 14, 74, 8, 14), Ell(x, 78, 8, 16)], (80, 150, 90), shadow=SMALL)
        for k in range(5):
            bloom(c, x - 16 + k * 8, 58 - (k % 2) * 4, col, r=6)
    return d


L512_ELEMENTS = [
    E("basket1", hanging_basket(110, (240, 120, 160)), pivot=(110, 0), anim=dict(swingAngle=4, swingSpeed=0.3)),
    E("basket2", hanging_basket(740, (250, 200, 70)), pivot=(740, 0), anim=dict(swingAngle=4, swingSpeed=0.3, phase=0.5)),
    E("butterfly", lambda c, m: (flat(c, [Ell(-6, 0, 6, 4), Ell(6, 0, 6, 4)], (250, 200, 80)), flat(c, Thick(0, -4, 0, 4, 1.5), INK)),
      anim=dict(drift_across(-12, 12, 26, start=300), driftVelocity=(26, 0), bobAmplitude=(0, 10), bobSpeed=0.7, stretch=(0.5, 0), scaleSpeed=3)),
    E("cat", lambda c, m: (piece(c, [Ell(880, 470, 18, 9), Circ(864, 462, 8), Poly([(858, 458), (858, 448), (864, 456)]),
                                   Poly([(866, 456), (872, 448), (872, 458)])], (80, 80, 90), border=1, shadow=SMALL)),
      pivot=(880, 478), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
]

L512_DIFFS = [
    ("pot", 150, 210, 0),
    ("tulips", 310, 330, 0),
    ("apron", 790, 346, 0),
    ("ribbon", 720, 366, 0),
    ("can", 590, 556, 0),
]


# =================================================================== Level 513 construction site
STEEL = (220, 120, 60)
HARD = (250, 200, 50)


def worker(c, x, base, vest=(250, 140, 40), hat=HARD, h=1.9):
    modern(c, x, base, (90, 110, 150), bottom=(70, 80, 100), hair=(40, 30, 30), h=h)
    flat(c, RRect(x - 8 * h, base - 38 * h, x + 8 * h, base - 20 * h, 3), vest)
    flat(c, [Thick(x - 8 * h, base - 28 * h, x + 8 * h, base - 28 * h, 2 * h)], (240, 240, 200))
    hx, hy = x + 1 * h, base - 46 * h
    piece(c, [Ell(hx, hy - 4 * h, 9 * h, 6 * h), Ell(hx + 2 * h, hy - 1 * h, 12 * h, 2 * h)], hat, border=1, shadow=SMALL)


def l513_bg(c, d):
    sky(c, (130, 190, 236), (226, 234, 240), 300)
    cloud_bank(c, 140, (250, 250, 246), 5131, k=0.7)
    far_skyline(c, 300, 60, 180, (186, 196, 214), 5132, win=(206, 214, 230))
    # building frame under construction (centre)
    for k in range(5):
        y = 120 + k * 50
        piece(c, RRect(300, y, 640, y + 8, 1), STEEL, shadow=SMALL)
    for x in (300, 385, 470, 555, 632):
        piece(c, RRect(x, 120, x + 8, 380, 1), STEEL, shadow=SMALL)
    for k in range(4):
        y = 128 + k * 50
        for x in (308, 393, 478, 563):
            if k == 1 and x == 478 and "brace" in d:
                continue
            flat(c, [Thick(x, y, x + 77, y + 42, 3), Thick(x + 77, y, x, y + 42, 3)], lit(STEEL, 0.85))
    # finished floors with glass at the bottom
    piece(c, RRect(300, 320, 640, 380, 2), (210, 214, 224), border=1.5, shadow=PROP)
    for x in range(312, 630, 40):
        flat(c, RRect(x, 330, x + 30, 370, 2), (150, 196, 226) if not (x == 552 and "pane" in d) else (250, 200, 90))
    # scaffolding (left)
    for x in (150, 210, 270):
        flat(c, Thick(x, 180, x, 400, 4), (150, 150, 160))
    for y in range(190, 400, 50):
        piece(c, RRect(140, y, 280, y + 6, 1), (190, 150, 100), shadow=SMALL)
        flat(c, Thick(150, y, 210, y + 50, 2), (150, 150, 160))
    # tower crane (right)
    piece(c, RRect(756, 40, 776, 400, 1), (250, 200, 60), shadow=PROP)
    for y in range(44, 400, 20):
        flat(c, [Thick(756, y, 776, y + 20, 1.6), Thick(776, y, 756, y + 20, 1.6)], (220, 170, 40))
    piece(c, RRect(420, 36, 900, 50, 1), (250, 200, 60), shadow=PROP)
    for x in range(420, 900, 20):
        flat(c, Thick(x, 36, x + 20, 50, 1.6), (220, 170, 40))
    piece(c, RRect(800, 50, 860, 80, 2), (120, 120, 130), shadow=SMALL)                 # counterweight
    piece(c, RRect(740, 52, 790, 86, 3), (250, 200, 60), border=1.2, shadow=SMALL)       # cab
    flat(c, RRect(748, 58, 782, 76, 2), (170, 210, 236))
    # ground
    piece(c, RRect(-10, 400, 910, 612, 0), (196, 170, 130), shadow=LAYER)
    for k in range(30):
        rnd = random.Random(5133 + k)
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(420, 600), rnd.uniform(10, 26), 3), (180, 154, 116))
    # sand pile + barrier fence
    piece(c, Poly([(20, 470), (80, 410), (140, 400), (200, 470)]), (230, 200, 140), shadow=PROP)
    for x in range(0, 900, 60):
        piece(c, RRect(x + 2, 560, x + 56, 592, 3), (250, 250, 250), border=1, shadow=SMALL)
        for k in range(3):
            flat(c, Poly([(x + 6 + k * 18, 592), (x + 16 + k * 18, 592), (x + 24 + k * 18, 560), (x + 14 + k * 18, 560)]), (230, 70, 50))
    # excavator (left)
    exc = (250, 190, 50) if "digger" not in d else (90, 170, 120)
    piece(c, RRect(100, 500, 230, 520, 8), (60, 60, 66), shadow=PROP)
    piece(c, [RRect(110, 450, 210, 500, 4), RRect(170, 420, 214, 460, 4)], exc, border=1.5, shadow=PROP)
    flat(c, RRect(178, 428, 206, 450, 2), (170, 210, 236))
    piece(c, [Thick(214, 450, 280, 400, 10), Thick(280, 400, 300, 470, 8)], exc, border=1.2, shadow=SMALL)
    piece(c, Poly([(290, 470), (320, 466), (312, 492), (288, 486)]), (90, 90, 100), shadow=SMALL)
    # dump truck (right)
    piece(c, [RRect(560, 470, 720, 520, 4), Poly([(720, 520), (720, 474), (760, 474), (780, 496), (780, 520)])], (230, 90, 60), border=1.5,
          shadow=PROP)
    flat(c, Poly([(728, 480), (756, 480), (770, 496), (728, 496)]), (170, 210, 236))
    if "load" not in d:
        piece(c, Poly([(570, 472), (600, 444), (650, 436), (700, 450), (712, 472)]), (150, 120, 90), shadow=SMALL)
    for wx in (590, 690, 750):
        piece(c, Circ(wx, 524, 15), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(wx, 524, 6), (180, 180, 190))
    # workers + cones
    worker(c, 400, 540)
    worker(c, 470, 546, hat=HARD if "helmet" not in d else (250, 250, 250))
    worker(c, 840, 536, vest=(120, 220, 90))
    for x in (520, 820):
        piece(c, Poly([(x - 14, 556), (x + 14, 556), (x + 4, 516), (x - 4, 516)]), (250, 120, 40), border=1.2, shadow=PROP)
        flat(c, Thick(x - 9, 538, x + 9, 538, 4), (250, 250, 250))


def hook(c, m):
    flat(c, Thick(520, 50, 520, 200, 1.6), (60, 60, 70))
    piece(c, RRect(508, 196, 532, 212, 3), (250, 200, 60), shadow=SMALL)
    piece(c, [RRect(470, 230, 570, 242, 1)], STEEL, border=1, shadow=SMALL)
    flat(c, [Thick(520, 212, 474, 232, 1.2), Thick(520, 212, 566, 232, 1.2)], (60, 60, 70))


L513_ELEMENTS = [
    E("hook", hook, pivot=(520, 50), anim=dict(swingAngle=3, swingSpeed=0.25)),
    E("dust", lambda c, m: soft_union(c, [Circ(300, 486, 10)], (220, 200, 160), 0.6, spread=10),
      anim=dict(driftVelocity=(10, 12), driftLength=40, driftFade=True, driftGrow=1.8)),
    E("spark", lambda c, m: [flat(c, Thick(390, 220, 390 + 10 * math.cos(a), 220 + 10 * math.sin(a), 1.6), (255, 220, 120))
                             for a in [k * math.pi / 4 for k in range(8)]],
      daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=3.0)),
    bird_el("bird", 200, 90, s=8, speed=22),
    cloud_el("cloud", 640, 100, 0.6, 6),
]

L513_DIFFS = [
    ("brace", 516, 200, 0),
    ("pane", 567, 350, 0),
    ("digger", 160, 470, 0),
    ("load", 640, 456, 0),
    ("helmet", 472, 452, 0),
]


# =================================================================== Level 514 train platform
def train_car(c, x0, x1, base, body, stripe, door=(90, 96, 110), door2=None):
    piece(c, RRect(x0, base - 120, x1, base, 18), body, border=1.5, shadow=PROP)
    flat(c, RRect(x0, base - 42, x1, base - 30, 1), stripe)
    for x in range(int(x0) + 24, int(x1) - 40, 70):
        flat(c, RRect(x, base - 100, x + 50, base - 64, 6), (60, 80, 110))
        flat(c, Poly([(x + 6, base - 100), (x + 20, base - 100), (x + 6, base - 76)]), (120, 150, 190))
    for x, col in ((x0 + 140, door), (x1 - 180, door2 or door)):
        flat(c, RRect(x, base - 106, x + 40, base - 4, 3), col)
        flat(c, Thick(x + 20, base - 106, x + 20, base - 4, 2), lit(col, 0.8))


def l514_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 230)
    far_skyline(c, 220, 30, 110, (186, 196, 214), 5141, win=(206, 214, 230))
    # far track + overhead wires
    c.rect(0, 220, W, 250, (150, 146, 140))
    flat(c, [Thick(0, 236, W, 236, 2), Thick(0, 244, W, 244, 2)], (110, 110, 116))
    # canopy
    piece(c, Poly([(-10, 0), (910, 0), (910, 60), (-10, 90)]), (230, 232, 238), border=1.5, shadow=PROP)
    for x in range(40, 900, 200):
        piece(c, RRect(x - 6, 60, x + 6, 470, 2), (90, 100, 120), shadow=PROP)
    # train at the platform
    train_car(c, -40, 420, 420, (240, 242, 246), (60, 150, 90))
    train_car(c, 430, 940, 420, (240, 242, 246), (60, 150, 90), door2=(90, 96, 110) if "door" not in d else (230, 150, 60))
    piece(c, RRect(418, 330, 432, 400, 2), (60, 60, 70), shadow=SMALL)
    # platform edge + surface
    piece(c, RRect(-10, 420, 910, 612, 0), (200, 200, 196), shadow=LAYER)
    flat(c, RRect(-10, 420, 910, 432, 0), (250, 220, 60))
    for x in range(0, 900, 16):
        flat(c, Circ(x + 8, 426, 2), (230, 190, 40))
    for y in range(450, H, 30):
        flat(c, Thick(0, y, W, y, 1.2), (186, 186, 182))
    # hanging clock + timetable screen
    flat(c, Thick(160, 70, 160, 96, 2), (90, 100, 120))
    piece(c, Circ(160, 126, 30), (250, 250, 252) if "clock" not in d else (250, 220, 110), border=1.5, shadow=PROP)
    c.ellipse_ring(160, 126, 30, 30, 3, (60, 60, 70))
    flat(c, [Thick(160, 126, 160, 104, 2.4), Thick(160, 126, 176, 132, 2.4)], (40, 40, 50))
    flat(c, [Thick(560, 60, 560, 96, 2), Thick(740, 60, 740, 96, 2)], (90, 100, 120))
    piece(c, RRect(530, 96, 770, 170, 5), (40, 44, 56), border=1.5, shadow=PROP)
    for k in range(3):
        y = 108 + k * 18
        flat(c, RRect(542, y, 576, y + 12, 2), (250, 160, 60))
        sign_box(c, 586, y, 700, y + 12, (220, 226, 240), 5142 + k, vertical=False)
        flat(c, RRect(712, y, 758, y + 12, 2), (90, 220, 120) if not (k == 1 and "screen" in d) else (240, 90, 80))
    # station-name board
    piece(c, RRect(320, 80, 480, 112, 4), (250, 250, 250), border=1.5, shadow=SMALL)
    flat(c, RRect(320, 102, 480, 112, 2), (60, 150, 90))
    sign_box(c, 340, 86, 460, 100, (40, 40, 50), 5145, vertical=False)
    # vending machine (left)
    vm = (220, 70, 70) if "vending" not in d else (70, 130, 210)
    piece(c, RRect(20, 440, 110, 590, 4), vm, border=1.5, shadow=PROP)
    flat(c, RRect(30, 452, 100, 520, 2), (230, 240, 246))
    for k in range(3):
        for i in range(4):
            flat(c, RRect(34 + i * 16, 458 + k * 20, 46 + i * 16, 474 + k * 20, 2), [(250, 200, 60), (90, 170, 230), (120, 200, 120), (250, 140, 60)][i])
    flat(c, RRect(40, 548, 90, 566, 2), (40, 40, 50))
    # bench + passengers
    piece(c, [RRect(560, 520, 720, 532, 3), RRect(566, 532, 574, 566, 2), RRect(706, 532, 714, 566, 2)], (150, 110, 80), border=1.2, shadow=PROP)
    modern(c, 600, 530, (120, 100, 170), bottom=(50, 50, 70), hair=(130, 130, 140), h=1.6, glasses=True)
    modern(c, 220, 590, (60, 80, 130), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.2, bag=(150, 100, 60))
    modern(c, 380, 596, (240, 160, 90), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.1, style="long", skirt=True)
    piece(c, RRect(420, 548, 446, 586, 4), (90, 170, 220) if "case" not in d else (240, 120, 170), border=1.2, shadow=SMALL)
    flat(c, Thick(433, 548, 433, 530, 1.6), (60, 60, 70))
    modern(c, 820, 590, (90, 160, 110), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.2)
    # bin
    piece(c, RRect(480, 530, 510, 576, 4), (120, 130, 150), border=1.2, shadow=PROP)


def express(c, m):
    piece(c, RRect(0, 196, 520, 236, 14), (250, 250, 252), border=1.5, shadow=SMALL)
    flat(c, RRect(0, 220, 520, 226, 1), (60, 110, 210))
    for x in range(20, 500, 40):
        flat(c, RRect(x, 204, x + 26, 214, 3), (60, 80, 110))


L514_ELEMENTS = [
    E("express", express, anim=dict(drift_across(0, 520, 260, start=-900))),
    E("pigeon", lambda c, m: (piece(c, [Ell(300, 412, 10, 6), Circ(308, 404, 5)], (150, 150, 170), border=1, shadow=SMALL),
                              flat(c, Poly([(312, 404), (318, 406), (312, 407)]), (230, 160, 60))),
      pivot=(300, 418), anim=dict(bobAmplitude=(8, 0), bobSpeed=0.2, stretch=(0, 0.08), scaleSpeed=1.6)),
    E("pigeon2", lambda c, m: (piece(c, [Ell(760, 452, 10, 6), Circ(752, 444, 5)], (150, 150, 170), border=1, shadow=SMALL)),
      pivot=(760, 458), anim=dict(bobAmplitude=(6, 0), bobSpeed=0.25, phase=0.4)),
    bird_el("bird", 400, 180, s=8, speed=-18),
]

L514_DIFFS = [
    ("clock", 160, 126, 0),
    ("screen", 735, 132, 0),
    ("door", 780, 366, 0),
    ("vending", 65, 500, 0),
    ("case", 433, 566, 0),
]


# =================================================================== Level 515 dinosaur museum
BONE = (240, 230, 206)
BONE_D = (214, 200, 172)


def trex(c, x, base, s=1.0):
    """T-rex skeleton facing right: legs, pelvis, spine with ribs, tail, skull, small arms."""
    bones = [Thick(x - 10 * s, base - 120 * s, x - 30 * s, base - 60 * s, 8 * s), Thick(x - 30 * s, base - 60 * s, x - 14 * s, base, 7 * s),
             Thick(x + 20 * s, base - 120 * s, x + 30 * s, base - 60 * s, 8 * s), Thick(x + 30 * s, base - 60 * s, x + 50 * s, base, 7 * s),
             Ell(x, base - 128 * s, 26 * s, 14 * s)]
    spine = [(x - 230 * s, base - 40 * s), (x - 150 * s, base - 96 * s), (x - 60 * s, base - 130 * s), (x, base - 140 * s),
             (x + 60 * s, base - 150 * s), (x + 104 * s, base - 158 * s)]
    bones += [Thick(spine[i][0], spine[i][1], spine[i + 1][0], spine[i + 1][1], (4 + i) * s) for i in range(len(spine) - 1)]
    piece(c, bones, BONE, border=1.2, border_col=(250, 246, 236), shadow=PROP)
    for k in range(6):
        rx = x + 4 * s + k * 13 * s
        ry = base - 142 * s - k * 6 * s
        flat(c, Thick(rx, ry, rx - 6 * s, ry + 44 * s - k * 3 * s, 3 * s), BONE_D)
    for i in range(0, 4):
        px, py = spine[i]
        flat(c, Thick(px, py, px - 4 * s, py - 14 * s, 3 * s), BONE_D)
    hx, hy = x + 140 * s, base - 166 * s
    piece(c, [Poly([(hx - 30 * s, hy - 18 * s), (hx + 40 * s, hy - 14 * s), (hx + 50 * s, hy + 4 * s), (hx - 26 * s, hy + 10 * s)])],
          BONE, border=1.2, border_col=(250, 246, 236), shadow=PROP)
    flat(c, [Circ(hx - 6 * s, hy - 6 * s, 6 * s), Ell(hx + 16 * s, hy, 8 * s, 4 * s)], (90, 80, 70))
    flat(c, [Thick(hx - 10 * s + k * 9 * s, hy + 10 * s, hx - 10 * s + k * 9 * s, hy + 16 * s, 2 * s) for k in range(6)], (250, 250, 240))
    flat(c, [Thick(x + 70 * s, base - 146 * s, x + 86 * s, base - 126 * s, 3 * s), Thick(x + 86 * s, base - 126 * s, x + 94 * s, base - 132 * s, 2 * s)],
         BONE)


def l515_bg(c, d):
    c.rect(0, 0, W, 470, (226, 214, 196))
    # skylit vaulted ceiling
    for x in range(-40, 940, 110):
        flat(c, Poly([(x, 0), (x + 80, 0), (x + 70, 40), (x + 10, 40)]), (200, 226, 240))
    flat(c, Thick(0, 42, W, 42, 6), (180, 166, 150))
    for x in range(0, 900, 150):
        piece(c, RRect(x + 60, 42, x + 80, 470, 2), (210, 196, 176), border=1, shadow=PROP)
    # hanging banners
    for k, (x, col) in enumerate(((150, (60, 110, 160)), (750, (170, 90, 60)))):
        if k == 1 and "banner" in d:
            col = (90, 150, 90)
        flat(c, Thick(x, 42, x, 60, 1.4), (120, 110, 100))
        piece(c, Poly([(x - 40, 60), (x + 40, 60), (x + 40, 200), (x, 184), (x - 40, 200)]), col, border=1.5, shadow=PROP)
        flat(c, [Thick(x - 20, 140, x + 20, 100, 4), Circ(x + 22, 98, 6), Thick(x - 20, 140, x - 28, 160, 3)], (250, 240, 220))
    # big T-rex on a plinth (centre)
    piece(c, RRect(220, 430, 700, 470, 4), (150, 140, 130), border=1.5, shadow=PROP)
    trex(c, 470, 430, s=1.2)
    # long-neck skeleton silhouette in the back (left)
    flat(c, [Thick(30, 260, 120, 130, 6), Thick(120, 130, 130, 110, 5), Ell(136, 108, 12, 7)], BONE_D)
    flat(c, [Thick(-10, 290, 30, 260, 8), Thick(20, 270, 20, 340, 6), Thick(60, 266, 60, 340, 6)], BONE_D)
    # wall cases (right): ammonite + amber
    piece(c, RRect(760, 250, 880, 360, 4), (120, 90, 70), border=1.5, shadow=PROP)
    flat(c, RRect(768, 258, 872, 352, 2), (214, 230, 236))
    c.ellipse_ring(800, 304, 22, 22, 6, (180, 150, 110))
    c.ellipse_ring(800, 304, 10, 10, 5, (180, 150, 110))
    flat(c, Ell(848, 310, 14, 18), (240, 160, 50) if "amber" not in d else (120, 200, 230))
    flat(c, Circ(846, 306, 3), (90, 60, 30))
    # floor + rope barrier
    c.rect(0, 470, W, H, (196, 176, 150))
    for y in range(480, H, 30):
        flat(c, Thick(0, y, W, y, 1.2), (182, 162, 136))
    for x in (230, 400, 560, 700):
        piece(c, [RRect(x - 4, 470, x + 4, 520, 2), Circ(x, 468, 7), Ell(x, 520, 14, 4)], (190, 160, 70) if not (x == 560 and "post" in d) else (90, 100, 120),
              border=1, shadow=SMALL)
    for x0, x1 in ((230, 400), (400, 560), (560, 700)):
        flat(c, [Thick(x0, 474, (x0 + x1) / 2, 490, 3), Thick((x0 + x1) / 2, 490, x1, 474, 3)], (170, 40, 50))
    # fossil plaque
    piece(c, RRect(30, 380, 170, 450, 4), (90, 70, 60), border=1.5, shadow=PROP)
    flat(c, RRect(38, 388, 162, 442, 2), (230, 220, 196))
    flat(c, [Thick(46, 434, 70, 396, 6), Thick(70, 396, 94, 430, 6), Circ(70, 396, 7)], (150, 130, 100) if "plaque" not in d else (60, 120, 200))
    sign_box(c, 100, 398, 154, 432, (90, 80, 70), 5151, vertical=False)
    # guide + school group
    modern(c, 120, 590, (60, 120, 90) if "guide" not in d else (200, 80, 120), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.2, style="long")
    flat(c, Thick(140, 510, 170, 490, 3), (246, 214, 186))
    for k, (x, col, hair) in enumerate(((300, (240, 120, 60), (40, 30, 30)), (380, (90, 150, 220), (220, 180, 90)), (460, (250, 200, 70), (90, 60, 40)),
                                        (540, (200, 100, 160), (40, 30, 30)))):
        modern(c, x, 596, col, bottom=(60, 70, 110), hair=hair, h=1.5, style="twin" if k % 2 else "short")
    modern(c, 780, 594, (130, 130, 150), bottom=(50, 50, 60), hair=(240, 240, 246), h=2.1, glasses=True)
    flat(c, RRect(764, 506, 784, 520, 2), (40, 40, 50))


L515_ELEMENTS = [
    E("jaw", lambda c, m: (piece(c, Poly([(616, 244), (686, 242), (682, 256), (620, 258)]), BONE, border=1.2, border_col=(250, 246, 236), shadow=SMALL),
                           flat(c, [Thick(624 + k * 10, 244, 624 + k * 10, 238, 2.4) for k in range(6)], (250, 250, 240))),
      pivot=(618, 248), anim=dict(swingAngle=4, swingSpeed=0.3)),
    E("flash", lambda c, m: soft_union(c, [Circ(800, 470, 6)], (255, 255, 240), 0.8, spread=16), daynight="untinted",
      anim=dict(twinkle=0.9, twinkleSpeed=0.4)),
    E("kid", lambda c, m: modern(c, 620, 596, (120, 200, 120), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.5), pivot=(620, 596),
      anim=dict(bobAmplitude=(0, 6), bobSpeed=1.0, bounce=True)),
    E("dust", lambda c, m: [flat(c, Circ(330 + k * 50, 80 + (k % 3) * 30, 2), (255, 250, 230, 0.8)) for k in range(6)],
      anim=dict(bobAmplitude=(6, 8), bobSpeed=0.1, twinkle=0.4, twinkleSpeed=0.5)),
]

L515_DIFFS = [
    ("banner", 750, 130, 0),
    ("amber", 848, 310, 0),
    ("post", 560, 494, 0),
    ("plaque", 72, 416, 0),
    ("guide", 122, 528, 0),
]


# =================================================================== Level 516 rainy cafe corner
STEPS516 = [(OVERCAST, 4), (RAIN, 14), (OVERCAST, 4), (CLEAR, 8)]


def umbrella(c, x, y, col, r=34):
    piece(c, Poly([(x - r, y)] + [(x + r * math.cos(math.radians(a)), y - r * 0.7 * math.sin(math.radians(a))) for a in range(0, 181, 15)][::-1] +
                  [(x + r, y)]), col, border=1.2, shadow=SMALL)
    flat(c, [Thick(x, y - r * 0.7, x - r * 0.5, y, 1.2), Thick(x, y - r * 0.7, x + r * 0.5, y, 1.2)], lit(col, 0.8))


def l516_bg(c, d):
    sky(c, (150, 176, 206), (210, 220, 232), 200)
    far_skyline(c, 200, 40, 160, (176, 186, 206), 5161, win=(200, 208, 224))
    # left building: cafe on the ground floor
    piece(c, RRect(-10, 40, 520, 470, 2), (236, 214, 180), border=2, shadow=PROP)
    for k, x in enumerate((40, 160, 280, 400)):
        flat(c, RRect(x, 80, x + 70, 170, 3), (150, 186, 214))
        flat(c, Thick(x + 35, 80, x + 35, 170, 2), (236, 214, 180))
        piece(c, RRect(x - 4, 170, x + 74, 182, 2), (150, 110, 80), shadow=SMALL)
        fl = (240, 100, 120) if not (k == 2 and "flowers" in d) else (250, 220, 80)
        flat(c, [Circ(x + 6 + j * 12, 168, 6) for j in range(6)], fl)
    # cat on the second sill
    piece(c, [Ell(196, 164, 14, 8), Circ(184, 154, 8), Poly([(178, 150), (178, 140), (184, 148)]), Poly([(186, 148), (192, 140), (192, 150)])],
          (80, 80, 90) if "cat" not in d else (240, 170, 90), border=1, shadow=SMALL)
    # awning
    stripe = (60, 130, 90)
    piece(c, Poly([(10, 230), (510, 230), (530, 290), (-10, 290)]), (250, 248, 240), border=1.5, shadow=PROP)
    for k in range(10):
        x = 10 + k * 50
        flat(c, Poly([(x, 230), (x + 25, 230), (x + 27, 290), (x + 2, 290)]), stripe)
    flat(c, [Circ(-10 + k * 27, 290, 13) for k in range(21)], (250, 248, 240))
    # hanging cafe sign (cup)
    flat(c, Thick(500, 190, 540, 190, 4), (60, 60, 70))
    piece(c, Circ(540, 214, 22), (250, 248, 240) if "sign" not in d else (250, 200, 70), border=1.5, shadow=PROP)
    flat(c, [RRect(530, 206, 548, 224, 3)], (120, 80, 60))
    c.ellipse_ring(551, 214, 5, 5, 2.4, (120, 80, 60))
    # shop window + door
    flat(c, RRect(30, 310, 300, 440, 3), (120, 90, 70))
    flat(c, RRect(40, 320, 290, 430, 2), (250, 220, 150))
    for x in range(60, 290, 50):
        flat(c, [Circ(x, 400, 10), Ell(x, 380, 4, 10)], (190, 140, 90))
    flat(c, Thick(40, 400, 290, 400, 3), (150, 110, 80))
    flat(c, RRect(340, 310, 420, 470, 3), (90, 60, 50))
    flat(c, RRect(352, 324, 408, 400, 2), (250, 220, 150))
    # right building + lamp
    piece(c, RRect(560, 20, 910, 470, 2), (180, 190, 210), border=2, shadow=PROP)
    for y in (60, 160, 260, 360):
        for x in (600, 700, 800):
            flat(c, RRect(x, y, x + 60, y + 70, 3), (150, 176, 206))
    # street
    piece(c, RRect(-10, 470, 910, 612, 0), (150, 150, 160), shadow=LAYER)
    flat(c, RRect(-10, 470, 910, 492, 0), (190, 186, 182))
    # outdoor tables
    for k, x in enumerate((120, 300)):
        piece(c, [Ell(x, 520, 46, 8), RRect(x - 3, 520, x + 3, 576, 2), Ell(x, 576, 18, 4)], (250, 250, 246), border=1.2, shadow=PROP)
        piece(c, [RRect(x - 70, 530, x - 50, 576, 3), RRect(x + 50, 530, x + 70, 576, 3)], (60, 120, 90), border=1, shadow=SMALL)
        flat(c, Thick(x, 520, x, 430, 3), (90, 90, 100))
        umbrella(c, x, 440, (250, 248, 240) if not (k == 1 and "umbrella" in d) else (250, 200, 70), r=70)
        flat(c, [Thick(x - 70 + j * 28, 440, x - 56 + j * 28, 440, 6) for j in range(5)], (60, 130, 90))
    # cups on the first table
    piece(c, [RRect(104, 504, 120, 518, 3)], (250, 250, 250), border=1, shadow=SMALL)
    # menu board
    piece(c, Poly([(460, 576), (480, 500), (520, 500), (540, 576)]), (120, 90, 70), border=1.2, shadow=PROP)
    flat(c, Poly([(476, 566), (490, 510), (510, 510), (524, 566)]), (50, 64, 58))
    sign_box(c, 488, 520, 512, 556, (240, 240, 230), 5162)
    # bicycle by the lamp
    bike = (60, 110, 200) if "bike" not in d else (220, 80, 120)
    for wx in (620, 700):
        c.ellipse_ring(wx, 560, 26, 26, 4, (40, 40, 46))
    flat(c, [Thick(620, 560, 650, 520, 4), Thick(650, 520, 690, 520, 4), Thick(690, 520, 700, 560, 4), Thick(650, 520, 664, 560, 4),
             Thick(664, 560, 620, 560, 4), Thick(690, 520, 694, 506, 4)], bike)
    flat(c, [Thick(684, 506, 704, 506, 4), Ell(650, 514, 10, 4)], (40, 40, 46))
    piece(c, [RRect(776, 330, 784, 560, 2), Ell(780, 320, 16, 10)], (60, 64, 76), shadow=PROP)
    flat(c, Ell(780, 328, 10, 5), (255, 236, 160))
    # passer-by with an umbrella
    modern(c, 860, 590, (200, 90, 90), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.1)
    flat(c, Thick(856, 520, 858, 470, 2), (60, 60, 70))
    umbrella(c, 858, 476, (60, 60, 80), r=40)


L516_ELEMENTS = [
    E("walker", lambda c, m: (modern(c, 0, 600, (240, 200, 70), bottom=(50, 60, 90), hair=(90, 60, 40), h=1.9, style="long"),
                              flat(c, Thick(0, 520, 2, 476, 2), (60, 60, 70)), umbrella(c, 2, 480, (220, 70, 90), r=36)),
      anim=dict(drift_across(-40, 40, 26, start=520), bobAmplitude=(0, 2), bobSpeed=1.2)),
    E("steam", lambda c, m: soft_union(c, [Circ(112, 496, 4)], (250, 250, 250), 0.7, spread=4),
      anim=dict(driftVelocity=(2, 12), driftLength=24, driftFade=True, driftGrow=1.6)),
    paper_sun("sun", 840, 30, r=24),
    cloud("cloudA", 200, 30, 1.2, (170, 176, 192), W_(OVERCAST, RAIN)),
    cloud("cloudB", 700, 26, 1.3, (166, 172, 188), W_(OVERCAST, RAIN)),
    puddles("puddles", [Ell(220, 590, 40, 6), Ell(560, 596, 50, 6)], mask=W_(RAIN)),
    rain_layer("rain", 516, 70, 24, 1.3, 0.6, 260, mask=W_(RAIN)),
] + splash_rings("splash", [(200, 592, 7), (540, 596, 8), (740, 586, 6)], mask=W_(RAIN))

L516_DIFFS = [
    ("flowers", 310, 168, 0),
    ("cat", 188, 154, 0),
    ("sign", 540, 214, 0),
    ("umbrella", 300, 420, 0),
    ("bike", 660, 540, 0),
]


# =================================================================== Level 517 pumpkin farm (day / night)
DN517 = day_night(40.0, tint=(0.26, 0.24, 0.46))
SUN517, MOON517 = celestial((450, 300), (360, 230), 40.0)


def pumpkin(c, x, base, s=1.0, col=(240, 130, 40)):
    piece(c, [Ell(x - 10 * s, base - 14 * s, 12 * s, 14 * s), Ell(x + 10 * s, base - 14 * s, 12 * s, 14 * s), Ell(x, base - 15 * s, 13 * s, 15 * s)],
          col, border=1.2, shadow=SMALL)
    flat(c, [Thick(x - 4 * s, base - 28 * s, x - 4 * s, base - 4 * s, 1.4), Thick(x + 5 * s, base - 28 * s, x + 5 * s, base - 4 * s, 1.4)], lit(col, 0.82))
    flat(c, Thick(x, base - 29 * s, x + 3 * s, base - 37 * s, 3 * s), (100, 120, 60))


def l517_bg(c, d):
    sky(c, (140, 190, 230), (250, 220, 180), 300)
    far_ridge(c, 210, 50, (190, 160, 140), 5171)
    far_round_trees(c, 250, 24, (210, 140, 70), 5172)
    piece(c, RRect(-10, 250, 910, 612, 0), (180, 150, 90), shadow=LAYER)
    for y in range(290, 600, 40):
        flat(c, Thick(0, y, W, y + 10, 6), (166, 136, 80))
    # barn (left)
    piece(c, RRect(40, 150, 260, 330, 2), (190, 60, 50), border=2, shadow=PROP)
    piece(c, Poly([(26, 156), (274, 156), (240, 100), (150, 70), (60, 100)]), (90, 70, 70), border=2, shadow=PROP)
    door = (250, 240, 220) if "door" not in d else (90, 140, 200)
    flat(c, RRect(110, 220, 190, 330, 2), door)
    flat(c, [Thick(110, 220, 190, 330, 4), Thick(190, 220, 110, 330, 4)], (190, 60, 50))
    flat(c, RRect(134, 120, 166, 150, 2), (255, 220, 140))
    # silo
    piece(c, [RRect(270, 110, 320, 330, 4), Ell(295, 110, 25, 16)], (200, 204, 214), border=1.5, shadow=PROP)
    # autumn trees (right)
    tree_round(c, 820, 300, s=1.7, col=(230, 120, 50))
    tree_round(c, 700, 280, s=1.3, col=(240, 180, 60) if "tree" not in d else (90, 160, 90))
    # fence
    for x in range(330, 900, 40):
        flat(c, Thick(x, 340, x, 300, 4), (150, 110, 70))
    flat(c, [Thick(330, 310, 900, 310, 4), Thick(330, 328, 900, 328, 4)], (150, 110, 70))
    # hay bales
    for x, y in ((360, 380), (420, 370)):
        if x == 420 and "hay" in d:
            continue
        piece(c, Ell(x, y, 34, 26), (230, 200, 110), border=1.5, shadow=PROP)
        c.ellipse_ring(x, y, 20, 16, 2, (200, 170, 80))
    # tractor
    trac = (60, 140, 80) if "tractor" not in d else (60, 110, 200)
    piece(c, [RRect(540, 340, 640, 390, 4), RRect(600, 300, 640, 344, 3)], trac, border=1.5, shadow=PROP)
    flat(c, RRect(606, 306, 634, 330, 2), (180, 220, 236))
    piece(c, Circ(560, 396, 24), (40, 40, 46), shadow=SMALL)
    flat(c, Circ(560, 396, 10), (240, 200, 60))
    piece(c, Circ(630, 404, 16), (40, 40, 46), shadow=SMALL)
    flat(c, Circ(630, 404, 6), (240, 200, 60))
    flat(c, Thick(548, 340, 548, 316, 4), (60, 60, 66))
    # pumpkin patch
    rnd = random.Random(5173)
    for row, y in enumerate((440, 490, 545, 595)):
        x = 20 + row * 14
        while x < 880:
            s = rnd.uniform(0.9, 1.4)
            if not (row == 2 and 600 < x < 720):
                flat(c, Thick(x - 30, y - 6, x + 30, y - 2, 2), (90, 120, 60))
                pumpkin(c, x, y, s=s)
            x += rnd.uniform(70, 110)
        if row == 2:
            pumpkin(c, 660, 556, s=2.2, col=(240, 130, 40) if "pumpkin" not in d else (250, 236, 200))
    # scarecrow
    flat(c, [Thick(480, 470, 480, 330, 5), Thick(440, 380, 520, 380, 5)], (130, 90, 60))
    piece(c, Poly([(456, 372), (504, 372), (510, 440), (450, 440)]), (90, 120, 180), border=1.2, shadow=PROP)
    piece(c, Circ(480, 352, 18), (230, 200, 120), border=1.2, shadow=SMALL)
    flat(c, [Circ(474, 350, 2.4), Circ(486, 350, 2.4)], INK)
    hat = (150, 100, 60) if "hat" not in d else (200, 60, 60)
    flat(c, [Ell(480, 336, 30, 6), RRect(466, 314, 494, 336, 4)], hat)
    flat(c, [Thick(440, 380, 432, 392, 3), Thick(520, 380, 528, 392, 3)], (230, 200, 110))


def lantern(x, y):
    def d(c, m):
        flat(c, [Poly([(x - 6, y - 16), (x - 2, y - 22), (x + 2, y - 16)]), Poly([(x + 4, y - 16), (x + 8, y - 22), (x + 10, y - 16)])],
             (255, 220, 90))
        flat(c, Poly([(x - 8, y - 8), (x + 10, y - 8), (x + 4, y - 4), (x, y - 6), (x - 4, y - 4)]), (255, 220, 90))
        soft_union(c, [Circ(x, y - 14, 10)], (255, 180, 60), 0.5, spread=16)
    return E("lantern%d" % x, d, daynight="night", anim=dict(twinkle=0.2, twinkleSpeed=2.0, phase=(x % 7) / 7))


L517_ELEMENTS = [
    sun_element("sun", (450, 300), SUN517, r=26),
    moon_element("moon", (450, 300), MOON517, r=22),
    star_field("stars", 517, 26, 160, avoid=[(20, 60, 330, 340)]),
    window_glow("barnwin", [(134, 120, 166, 150)]),
    lantern(90, 490), lantern(280, 545), lantern(800, 595),
    E("crow", lambda c, m: (piece(c, [Ell(520, 372, 10, 7), Circ(530, 364, 6)], (40, 40, 50), border=1, shadow=SMALL),
                            flat(c, Poly([(535, 364), (544, 366), (535, 368)]), (240, 180, 60))),
      pivot=(520, 378), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.6, stretch=(0, 0.1), scaleSpeed=1.4)),
    bird_el("goose", 600, 160, s=9, speed=-16, daynight="day"),
]

L517_DIFFS = [
    ("door", 150, 276, 0),
    ("tree", 700, 210, 0),
    ("hay", 420, 370, 0),
    ("tractor", 590, 350, 0),
    ("pumpkin", 660, 530, 0),
    ("hat", 480, 326, 0),
]


# =================================================================== Level 518 outdoor ice rink (snow)
STEPS518 = [(CLEAR, 10), (SNOW, 14)]
ICE = (214, 234, 246)


def skater(c, x, base, top, scarf, h=1.8, hair=(40, 30, 30), style="short"):
    modern(c, x, base - 6 * h, top, bottom=(50, 60, 90), hair=hair, h=h, style=style)
    flat(c, RRect(x - 8 * h, base - 44 * h, x + 8 * h, base - 38 * h, 2), scarf)
    flat(c, RRect(x + 2 * h, base - 42 * h, x + 7 * h, base - 30 * h, 2), scarf)
    flat(c, [Thick(x - 8 * h, base - 2, x - 1 * h, base - 2, 2), Thick(x + 1 * h, base - 2, x + 9 * h, base - 2, 2)], (200, 200, 210))


def l518_bg(c, d):
    sky(c, (120, 160, 210), (220, 226, 240), 260)
    far_skyline(c, 220, 50, 150, (170, 180, 206), 5181, win=(250, 220, 150))
    # town buildings behind the rink with snowy roofs
    for k, (x, w, h, col) in enumerate(((-10, 170, 170, (200, 120, 100)), (170, 150, 140, (230, 210, 170)), (620, 150, 150, (150, 170, 200)),
                                        (780, 140, 180, (210, 180, 150)))):
        piece(c, RRect(x, 300 - h, x + w, 300, 2), col, border=1.5, shadow=PROP)
        flat(c, RRect(x - 4, 300 - h - 6, x + w + 4, 300 - h + 6, 4), (250, 252, 255))
        for wx in range(int(x) + 20, int(x + w) - 30, 44):
            flat(c, RRect(wx, 300 - h + 30, wx + 24, 300 - h + 62, 2), (255, 220, 140))
    # christmas tree (centre back)
    for k in range(4):
        w = 40 + k * 22
        piece(c, Poly([(450, 70 + k * 50), (450 - w, 150 + k * 50), (450 + w, 150 + k * 50)]), (50, 120, 80), border=1.5, shadow=PROP)
    flat(c, RRect(442, 300, 458, 320, 1), (120, 80, 60))
    for k, (x, y) in enumerate(((430, 140), (470, 180), (420, 230), (480, 260), (440, 290), (400, 290), (500, 220))):
        flat(c, Circ(x, y, 7), [(230, 60, 60), (250, 200, 60), (90, 150, 230)][k % 3])
    piece(c, Poly(star_pts(450, 66, 22, 9)), (250, 210, 60) if "star" not in d else (250, 250, 250), border=1.2, shadow=SMALL)
    # gift boxes under the tree
    piece(c, RRect(386, 296, 422, 324, 2), (200, 60, 70), border=1, shadow=SMALL)
    piece(c, RRect(478, 300, 510, 324, 2), (60, 110, 200) if "gift" not in d else (90, 180, 100), border=1, shadow=SMALL)
    flat(c, [Thick(404, 296, 404, 324, 3), Thick(494, 300, 494, 324, 3)], (250, 220, 90))
    # rink boards + ice
    piece(c, RRect(-10, 320, 910, 350, 2), (240, 240, 246), border=1.5, shadow=PROP)
    for x in range(20, 900, 120):
        flat(c, RRect(x, 326, x + 80, 344, 2), [(220, 70, 70), (60, 120, 210), (90, 170, 110)][(x // 120) % 3])
    c.rect(0, 350, W, 520, ICE)
    for k in range(18):
        rnd = random.Random(5182 + k)
        x, y = rnd.uniform(0, W), rnd.uniform(360, 510)
        flat(c, Thick(x, y, x + rnd.uniform(40, 90), y + rnd.uniform(-6, 6), 1.4), (240, 248, 252))
    flat(c, Thick(0, 520, W, 520, 6), (240, 240, 246))
    # skaters on the ice
    skater(c, 150, 460, (220, 80, 80), (250, 250, 250), h=1.9)
    skater(c, 330, 490, (90, 150, 220), (250, 200, 60) if "scarf" not in d else (90, 200, 120), h=1.8, hair=(220, 180, 90), style="long")
    skater(c, 600, 470, (250, 200, 80), (200, 60, 80), h=1.7)
    skater(c, 760, 500, (120, 100, 170), (250, 250, 250), h=2.0, hair=(90, 60, 40), style="long")
    # snowy path + hot chocolate stand (right) + bench (left)
    c.rect(0, 526, W, H, (246, 248, 252))
    piece(c, RRect(700, 520, 880, 600, 3), (150, 100, 70), border=1.5, shadow=PROP)
    piece(c, Poly([(690, 524), (890, 524), (870, 494), (710, 494)]), (220, 60, 60) if "awning" not in d else (60, 120, 210), border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, [RRect(730 + k * 40, 540, 750 + k * 40, 560, 3)], (250, 250, 250))
    modern(c, 820, 560, (60, 120, 90), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.2)
    piece(c, [RRect(60, 560, 220, 570, 2), RRect(68, 570, 76, 600, 1), RRect(204, 570, 212, 600, 1)], (130, 90, 60), shadow=PROP)
    modern(c, 140, 568, (240, 140, 80), bottom=(50, 60, 90), hair=(130, 130, 140), h=1.5)
    # lamp post with string lights
    piece(c, [RRect(576, 380, 584, 600, 2), Ell(580, 374, 14, 8)], (60, 64, 76), shadow=PROP)
    flat(c, Ell(580, 380, 9, 4), (255, 236, 160))


def string_lights(c, m):
    for y0, x0, x1 in ((240, 0, 900),):
        pts = [(x, y0 + 30 * math.sin((x - x0) / (x1 - x0) * math.pi * 3) ** 2) for x in range(x0, x1 + 1, 30)]
        flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(len(pts) - 1)], (60, 60, 70))
        for i, (x, y) in enumerate(pts):
            if 350 < x < 550:
                continue
            flat(c, Circ(x, y + 5, 4), [(255, 120, 120), (255, 230, 120), (140, 220, 255)][i % 3])


L518_ELEMENTS = [
    E("lights", string_lights, daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=1.2)),
    E("glider", lambda c, m: skater(c, 0, 515, (90, 200, 160), (240, 120, 160), h=1.5, hair=(90, 60, 40)),
      anim=dict(drift_across(-20, 20, 50, start=250), bobAmplitude=(0, 3), bobSpeed=0.6)),
    E("cocoa", lambda c, m: soft_union(c, [Circ(780, 532, 4)], (250, 250, 250), 0.7, spread=4),
      anim=dict(driftVelocity=(2, 12), driftLength=24, driftFade=True, driftGrow=1.6)),
    cloud("cloudA", 200, 40, 1.2, (210, 216, 230), W_(SNOW)),
    cloud("cloudB", 700, 30, 1.3, (210, 216, 230), W_(SNOW)),
    snow_layer("snow", 518, 70, 2.0, 4.0, 40),
]

L518_DIFFS = [
    ("star", 450, 66, 0),
    ("gift", 494, 312, 0),
    ("scarf", 336, 408, 0),
    ("awning", 790, 508, 0),
]


# =================================================================== Level 519 pet shop
def l519_bg(c, d):
    c.rect(0, 0, W, 460, (232, 240, 246))
    for y in range(0, 460, 40):
        flat(c, Thick(0, y, W, y, 1.2), (220, 230, 238))
    # fish tank wall (left)
    piece(c, RRect(20, 60, 300, 260, 4), (90, 100, 120), border=1.5, shadow=PROP)
    for k in range(18):
        y = 70 + k * 10
        f = k / 17
        flat(c, RRect(30, y, 290, y + 10, 0), (int(120 - 60 * f), int(200 - 60 * f), int(230 - 30 * f)))
    piece(c, RRect(20, 60, 300, 70, 2), (90, 100, 120), shadow=SMALL)
    piece(c, RRect(20, 250, 300, 260, 2), (90, 100, 120), shadow=SMALL)
    flat(c, Poly([(30, 250), (290, 250), (290, 230), (200, 224), (100, 232), (30, 226)]), (230, 210, 160))
    plant = (70, 170, 100) if "plant" not in d else (230, 110, 130)
    flat(c, [Thick(240, 236, 232, 150, 6), Thick(256, 236, 262, 160, 6), Thick(248, 236, 248, 140, 5)], plant)
    for x, y, col in ((90, 120, (250, 150, 50)), (170, 170, (250, 220, 70)), (110, 200, (240, 100, 150))):
        piece(c, [Ell(x, y, 14, 8), Poly([(x - 12, y), (x - 22, y - 7), (x - 22, y + 7)])], col, border=1, shadow=SMALL)
        flat(c, Circ(x + 8, y - 2, 1.6), INK)
    # cabinet under the tank
    piece(c, RRect(20, 262, 300, 440, 3), (170, 130, 90), border=1.5, shadow=PROP)
    flat(c, [Thick(160, 270, 160, 432, 2)], (150, 110, 76))
    # shelves of pet food (right)
    for k, y in enumerate((120, 210, 300)):
        piece(c, RRect(620, y, 890, y + 10, 2), (170, 130, 90), border=1.2, shadow=PROP)
        for i in range(5):
            x = 640 + i * 50
            col = [(240, 120, 60), (90, 150, 220), (120, 190, 110), (240, 200, 70), (200, 100, 160)][(i + k) % 5]
            if k == 1 and i == 2 and "bag" in d:
                col = (60, 60, 70)
            piece(c, [RRect(x, y - 54, x + 36, y, 4)], col, border=1, shadow=SMALL)
            flat(c, Circ(x + 18, y - 30, 9), (250, 250, 250))
            flat(c, Ell(x + 18, y - 30, 5, 4), lit(col, 0.8))
    # leashes on hooks
    for k, x in enumerate((380, 420, 460)):
        flat(c, Circ(x, 60, 4), (120, 120, 130))
        col = [(220, 60, 70), (60, 120, 210), (250, 190, 60)][k] if not (k == 2 and "leash" in d) else (130, 90, 200)
        flat(c, Thick(x, 60, x, 180, 4), col)
        c.ellipse_ring(x, 190, 10, 10, 3, col)
    # cat tree (centre)
    piece(c, [RRect(500, 200, 516, 460, 3)], (210, 190, 160), shadow=PROP)
    plat = (150, 110, 160) if "cattree" not in d else (90, 160, 140)
    piece(c, [RRect(460, 250, 560, 266, 4), RRect(470, 360, 570, 376, 4), Ell(508, 196, 34, 12)], plat, border=1.2, shadow=PROP)
    piece(c, [Ell(520, 236, 22, 12), Circ(538, 226, 10), Poly([(532, 220), (532, 208), (538, 218)]), Poly([(540, 218), (546, 208), (546, 220)])],
          (250, 250, 250), border=1, shadow=SMALL)
    flat(c, [Circ(540, 226, 1.6), Circ(546, 226, 1.6)], INK)
    # floor
    c.rect(0, 460, W, H, (210, 196, 176))
    for x in range(0, W, 60):
        flat(c, Thick(x, 460, x, H, 1.2), (196, 182, 162))
    # puppy pen (front left)
    piece(c, RRect(30, 500, 330, 600, 4), (240, 236, 226), border=1.5, shadow=PROP)
    flat(c, RRect(40, 510, 320, 590, 3), (230, 220, 200))
    for k, (x, col) in enumerate(((100, (220, 180, 120)), (200, (250, 250, 248) if "puppy" not in d else (110, 110, 120)), (270, (130, 90, 60)))):
        piece(c, [Ell(x, 570, 22, 12), Circ(x + 18, 552, 12), Ell(x + 8, 548, 6, 10)], col, border=1, shadow=SMALL)
        flat(c, Circ(x + 22, 550, 1.8), INK)
        flat(c, RRect(x + 8, 560, x + 26, 565, 2), (220, 60, 70))
    for x in range(40, 330, 20):
        flat(c, Thick(x, 500, x, 600, 2), (210, 206, 196))
    # counter + shopkeeper (right)
    piece(c, RRect(620, 420, 910, 560, 4), (170, 130, 90), border=1.5, shadow=PROP)
    modern(c, 760, 420, (90, 160, 140), bottom=(60, 60, 70), hair=(220, 180, 90), h=2.0, style="long")
    piece(c, [RRect(660, 392, 706, 422, 3)], (60, 64, 76), border=1, shadow=SMALL)
    # customer with a kid
    modern(c, 450, 600, (220, 120, 80), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.1)
    modern(c, 540, 600, (250, 210, 80), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.4, style="twin")


def birdcage(c, m):
    flat(c, Thick(380, 0, 380, 240, 1.4), (120, 120, 130))
    for k in range(7):
        x = 350 + k * 10
        flat(c, Thick(x, 260 - abs(k - 3) * 4, x, 330, 1.4), (200, 170, 80))
    piece(c, Poly([(346, 262), (414, 262), (380, 236)]), (200, 170, 80), shadow=SMALL)
    flat(c, [Thick(346, 330, 414, 330, 4), Thick(360, 300, 400, 300, 2)], (200, 170, 80))


def parrot(c, m):
    piece(c, [Ell(380, 288, 9, 14), Circ(384, 274, 8), Poly([(376, 298), (370, 318), (382, 300)])], (60, 180, 90), border=1, shadow=SMALL)
    flat(c, Poly([(390, 272), (398, 276), (390, 280)]), (250, 200, 60))
    flat(c, Circ(386, 272, 1.6), INK)


L519_ELEMENTS = [
    E("cage", birdcage, pivot=(380, 0), anim=dict(swingAngle=2, swingSpeed=0.3)),
    E("parrot", parrot, pivot=(380, 300), anim=dict(swingAngle=6, swingSpeed=0.6)),
    spin_el("wheel", lambda c, m: (c.ellipse_ring(860, 520, 26, 26, 3, (200, 200, 210)),
                                   flat(c, [Thick(860 + 26 * math.cos(a), 520 + 26 * math.sin(a), 860, 520, 1.6) for a in (0, 2.1, 4.2)], (200, 200, 210))),
            (860, 520), 90),
    E("wag", lambda c, m: flat(c, Thick(78, 566, 66, 552, 4), (220, 180, 120)), pivot=(78, 566), anim=dict(swingAngle=22, swingSpeed=1.8)),
] + bubbles_el("bub", 60, 240, n=3, r=4, rise=(1, 24), length=150)

L519_DIFFS = [
    ("plant", 248, 190, 0),
    ("leash", 460, 128, 0),
    ("bag", 758, 180, 0),
    ("cattree", 515, 368, 0),
    ("puppy", 210, 562, 0),
]


LEVELS = [
    ("Level510", "水族馆", l510_bg, L510_ELEMENTS, L510_DIFFS, 60, OPTS),
    ("Level511", "马戏团", l511_bg, L511_ELEMENTS, L511_DIFFS, 60, OPTS),
    ("Level512", "花店", l512_bg, L512_ELEMENTS, L512_DIFFS, 60, OPTS),
    ("Level513", "建筑工地", l513_bg, L513_ELEMENTS, L513_DIFFS, 60, OPTS),
    ("Level514", "火车站台", l514_bg, L514_ELEMENTS, L514_DIFFS, 60, OPTS),
    ("Level515", "恐龙博物馆", l515_bg, L515_ELEMENTS, L515_DIFFS, 60, OPTS),
    ("Level516", "雨天街角咖啡", l516_bg, L516_ELEMENTS, L516_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS516, blend=3.0), anim_seconds=30.0, frames=80)),
    ("Level517", "南瓜农场", l517_bg, L517_ELEMENTS, L517_DIFFS, 60, dict(OPTS, day_night=DN517, anim_seconds=40.0, frames=80)),
    ("Level518", "露天溜冰场", l518_bg, L518_ELEMENTS, L518_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS518, blend=3.0), anim_seconds=24.0, frames=80)),
    ("Level519", "宠物店", l519_bg, L519_ELEMENTS, L519_DIFFS, 60, OPTS),
]
