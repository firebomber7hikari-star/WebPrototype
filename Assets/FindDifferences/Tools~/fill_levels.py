# -*- coding: utf-8 -*-
"""
Per-level filler that removes large empty areas (called from the level background / interior painters).
back_*  : drawn right after the sky / base wall, behind everything else
front_* : drawn last in the background, only in areas that hold no difference
"""
import math
import random

from fdcore import H, W, lit, on
from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union, star_pts
from fills import (birds, cloud_bank, corner_foliage, far_forest, far_ridge, far_round_trees, far_skyline, flowerlet, hanging_vines,
                   pebble, picture_frame, puffs, scatter, shelf, shrub, side_bushes, tuft, wall_tiles, wallpaper_diamonds,
                   wallpaper_stripes)

PROP = (2, 4, 7, 0.42)
SMALL = (1, 2, 3, 0.3)


def crate_(c, x, y, rnd):
    piece(c, RRect(x - 14, y - 26, x + 14, y, 2), (190, 150, 100), border=1.5, shadow=PROP)
    flat(c, [Thick(x - 14, y - 26, x + 14, y, 2), Thick(x + 14, y - 26, x - 14, y, 2)], (160, 120, 80))


def barrel_(c, x, y, rnd):
    piece(c, RRect(x - 11, y - 28, x + 11, y, 5), (160, 110, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(x - 11, y - 20, x + 11, y - 20, 2), Thick(x - 11, y - 8, x + 11, y - 8, 2)], (120, 80, 50))


# ------------------------------------------------------------------- 12 doll's house
def back_Level12(c, d):
    pass


# ------------------------------------------------------------------- 16 farm
def back_Level16(c, d):
    far_ridge(c, 300, 80, (176, 200, 216), 16)
    puffs(c, [(520, 130, 0.6), (760, 150, 0.5), (340, 190, 0.4)])
    birds(c, [(620, 80, 8), (640, 70, 6)])


def front_Level16(c, d):
    scatter(c, (0, 520, 900, 598), 40, 160, [(3, tuft((90, 150, 70))), (2, flowerlet([(255, 140, 180), (255, 220, 90), (250, 250, 245)]))],
            avoid=[(20, 490, 240, 570), (250, 460, 350, 540), (780, 535, 860, 600)])


# ------------------------------------------------------------------- 19 castle
def back_Level19(c, d):
    far_ridge(c, 320, 70, (186, 196, 222), 19)
    puffs(c, [(620, 160, 0.5), (90, 170, 0.45), (800, 200, 0.4)])
    birds(c, [(300, 90, 8), (320, 80, 6), (700, 120, 7)])


def front_Level19(c, d):
    far_forest(c, 340, 50, (100, 150, 110), 193, spacing=20, x0=-20, x1=150)
    far_forest(c, 340, 50, (100, 150, 110), 194, spacing=20, x0=770, x1=920)
    corner_foliage(c, "tr", (80, 140, 85), 191, 0.9)
    scatter(c, (0, 470, 900, 600), 30, 192, [(3, tuft((90, 150, 80))), (1, shrub((90, 160, 90))), (1, flowerlet([(255, 130, 170), (255, 230, 90)]))],
            avoid=[(20, 360, 270, 470), (400, 340, 660, 600), (470, 460, 650, 560)])


# ------------------------------------------------------------------- 21 tavern (upper walls)
def front_Level21(c, d):
    shelf(c, 80, 250, 130, (130, 90, 62), 211, [(220, 210, 190), (190, 80, 70), (90, 120, 170)])
    for x, y in ((100, 200), (150, 200), (200, 200)):
        piece(c, Circ(x, y, 18), (230, 225, 210), border=1.5, shadow=PROP)
        flat(c, Circ(x, y, 10), (210, 200, 180))
    picture_frame(c, 660, 80, 70, 56, (150, 110, 60), [(150, 190, 220), (100, 150, 90), (250, 220, 120)], 1)
    picture_frame(c, 750, 90, 60, 70, (150, 110, 60), [(220, 200, 160), (170, 110, 80)], 2)
    piece(c, [Thick(510, 300, 570, 300, 3)], (120, 80, 60), shadow=None)
    piece(c, RRect(-10, 590, 910, 610, 0), (110, 74, 50), shadow=None)
    piece(c, Ell(450, 560, 180, 26), (170, 60, 60), border=2, border_col=(230, 190, 90), shadow=SMALL)


# ------------------------------------------------------------------- 29 steampunk
def back_Level29(c, d):
    cloud_bank(c, 40, (236, 214, 180), 29, 1.2)
    far_skyline(c, 430, 170, 320, (186, 150, 120), 290)
    for x, y, k in ((620, 70, 0.5), (820, 120, 0.4)):
        piece(c, Ell(x, y, 50 * k * 2, 18 * k * 2), (176, 120, 90), shadow=SMALL)
        piece(c, RRect(x - 20 * k, y + 16 * k, x + 20 * k, y + 26 * k, 3), (120, 90, 70), shadow=None)


def front_Level29(c, d):
    for x, y in ((24, 600), (54, 600), (870, 600)):
        crate_(c, x, y, None)
    barrel_(c, 840, 600, None)


# ------------------------------------------------------------------- 30 sci-fi
def back_Level30(c, d):
    for (x, y, rx, ry, col) in ((200, 120, 260, 60, (200, 120, 220)), (650, 260, 300, 50, (120, 160, 240)), (300, 300, 200, 40, (250, 150, 180))):
        soft_union(c, [Ell(x, y, rx, ry)], col, 0.25, spread=60)
    rnd = random.Random(30)
    for _ in range(50):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 340), rnd.uniform(0.8, 1.8)), (255, 250, 230))
    far_skyline(c, 370, 60, 170, (120, 96, 170), 300, win=(150, 230, 255))


def front_Level30(c, d):
    def crystal_(c, x, y, rnd):
        col = rnd.choice(((150, 120, 255), (120, 230, 255)))
        piece(c, Poly([(x - 6, y), (x - 6, y - 16), (x, y - 26), (x + 6, y - 16), (x + 6, y)]), col, shadow=SMALL)
    scatter(c, (0, 500, 900, 598), 28, 301, [(2, pebble((110, 100, 140))), (1, crystal_)],
            avoid=[(80, 420, 200, 500), (280, 420, 470, 500), (540, 440, 760, 500)])


# ------------------------------------------------------------------- 32 wasteland
def back_Level32(c, d):
    far_ridge(c, 330, 40, (232, 176, 128), 32)
    puffs(c, [(380, 70, 0.6), (640, 110, 0.5)], col=(255, 244, 226))
    birds(c, [(520, 150, 7)])


def front_Level32(c, d):
    scatter(c, (0, 450, 900, 598), 30, 320, [(2, pebble((190, 150, 110))), (2, shrub((150, 150, 90))), (1, tuft((170, 150, 90)))],
            avoid=[(120, 440, 310, 540), (40, 560, 130, 600), (700, 540, 800, 600), (830, 560, 900, 600), (400, 380, 520, 460),
                   (-10, 500, 910, 585)])


# ------------------------------------------------------------------- 33 quarantine (top-down)
def front_Level33(c, d):
    def sandbags(c, x, y, rnd):
        for k in range(4):
            piece(c, Ell(x - 24 + k * 16, y, 10, 6), (190, 170, 120), border=1, shadow=(2, 3, 3, 0.4))

    def tree_(c, x, y, rnd):
        piece(c, Circ(x, y, rnd.uniform(14, 22)), (80, 120, 70), shadow=(6, 9, 6, 0.4))

    def puddle(c, x, y, rnd):
        flat(c, Ell(x, y, rnd.uniform(18, 30), rnd.uniform(8, 12)), (100, 120, 110))

    scatter(c, (10, 10, 390, 250), 16, 330, [(2, tree_), (2, sandbags), (1, puddle)], avoid=[(80, 50, 240, 210)])
    scatter(c, (10, 345, 390, 590), 16, 331, [(2, tree_), (2, sandbags), (1, puddle), (1, crate_)],
            avoid=[(90, 380, 180, 500), (250, 400, 350, 490), (340, 430, 430, 500)])


# ------------------------------------------------------------------- 34 laboratory
def back_Level34(c, d):
    wall_tiles(c, (0, 250, W, 470), (214, 228, 230), (196, 212, 214), 28)
    flat(c, Thick(0, 22, W, 22, 10), (170, 180, 190))
    flat(c, Thick(0, 40, W, 40, 6), (190, 200, 206))
    for x in (430, 880):
        flat(c, Thick(x, 22, x, 250, 6), (170, 180, 190))
    shelf(c, 420, 540, 140, (150, 160, 170), 341, [(120, 200, 240), (240, 140, 160), (160, 220, 140), (250, 220, 120)])
    shelf(c, 420, 540, 210, (150, 160, 170), 342, [(120, 200, 240), (240, 140, 160), (160, 220, 140)])
    shelf(c, 700, 880, 140, (150, 160, 170), 343, [(120, 200, 240), (240, 140, 160), (160, 220, 140), (250, 220, 120)])
    shelf(c, 700, 880, 210, (150, 160, 170), 344, [(120, 200, 240), (200, 200, 210)])
    piece(c, RRect(840, 280, 900, 470, 3), (200, 206, 214), border=1.5, shadow=PROP)
    flat(c, [Thick(842, 340, 898, 340, 2), Thick(842, 400, 898, 400, 2)], (170, 176, 186))
    soft_union(c, [RRect(70, 70, 230, 190, 2)], (255, 255, 255), 0.25, spread=8)


# ------------------------------------------------------------------- 36 rainforest
def front_Level36(c, d):
    corner_foliage(c, "tl", (50, 120, 70), 361, 1.0)
    corner_foliage(c, "bl", (60, 130, 75), 362, 0.9)
    corner_foliage(c, "br", (55, 125, 70), 363, 0.9)
    hanging_vines(c, (250, 470, 720), 120, (70, 150, 80), 364)


# ------------------------------------------------------------------- 37 polar
def back_Level37(c, d):
    cloud_bank(c, 120, (236, 244, 252), 37, 0.9)
    puffs(c, [(150, 60, 0.6), (760, 50, 0.5)], col=(250, 252, 255))


def front_Level37(c, d):
    def drift(c, x, y, rnd):
        piece(c, Ell(x, y, rnd.uniform(24, 40), rnd.uniform(6, 9)), (236, 244, 252), shadow=SMALL)

    def ice(c, x, y, rnd):
        s = rnd.uniform(0.6, 1.0)
        piece(c, Poly([(x - 14 * s, y), (x - 8 * s, y - 18 * s), (x + 6 * s, y - 22 * s), (x + 14 * s, y)]), (200, 226, 246), shadow=SMALL)
    scatter(c, (0, 540, 900, 598), 24, 370, [(2, drift), (1, ice)],
            avoid=[(120, 400, 280, 480), (300, 460, 420, 500), (440, 470, 600, 545), (360, 490, 470, 560), (680, 480, 900, 570)])


# ------------------------------------------------------------------- 38 volcano
def back_Level38(c, d):
    cloud_bank(c, 60, (210, 170, 150), 38, 1.0)
    birds(c, [(200, 140, 8), (220, 130, 6), (650, 200, 7)])


def front_Level38(c, d):
    corner_foliage(c, "tl", (70, 120, 80), 381, 0.8)
    corner_foliage(c, "br", (70, 130, 80), 382, 0.8)


# ------------------------------------------------------------------- 39 deep sea
def back_Level39(c, d):
    rnd = random.Random(390)
    for x in range(-20, 920, 46):
        h = rnd.uniform(140, 300)
        pts = [(x + 10 * math.sin(k * 0.9), 470 - k * h / 8) for k in range(9)]
        piece(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 9 - k * 0.6) for k in range(8)], (24, 60, 70), shadow=None)
    piece(c, Poly([(560, 470), (600, 330), (700, 300), (780, 340), (820, 470), (760, 470), (720, 380), (650, 380), (620, 470)]), (30, 44, 66),
          shadow=None)
    piece(c, [Ell(160, 90, 90, 22), Poly([(70, 90), (40, 70), (44, 110)])], (24, 44, 74), shadow=None)
    for x in (200, 420, 640):
        c.polygon([(x, -10), (x + 50, -10), (x + 150, 470), (x + 70, 470)], (120, 200, 230, 0.06))


def front_Level39(c, d):
    corner_foliage(c, "br", (60, 90, 110), 391, 0.8, leaf=(120, 220, 210))


# ------------------------------------------------------------------- 40 underground ruins
def front_Level40(c, d):
    rnd = random.Random(400)
    for x in range(20, 900, 46):
        if 440 < x < 560:
            continue
        h = rnd.uniform(20, 46)
        piece(c, Poly([(x - 9, 0), (x + 9, 0), (x, h)]), (110, 86, 70), shadow=SMALL)
    for x0, y0, x1, y1 in ((0, 300, 60, 360), (420, 300, 480, 360), (860, 300, 900, 600), (0, 560, 120, 600), (800, 560, 900, 600)):
        for y in range(int(y0), int(y1), 14):
            for x in range(int(x0) + (y // 14 % 2) * 12, int(x1), 24):
                flat(c, RRect(x, y, x + 20, y + 11, 1), (120, 96, 80))
    for x in (40, 860):
        flat(c, [Thick(x, 0, x + 10, 120, 3), Thick(x + 10, 120, x - 6, 200, 2)], (120, 90, 60))


# ------------------------------------------------------------------- 41 lost temple
def back_Level41(c, d):
    far_ridge(c, 300, 90, (150, 186, 190), 41)
    puffs(c, [(220, 90, 0.6), (700, 70, 0.5)])


def front_Level41(c, d):
    corner_foliage(c, "tl", (60, 130, 80), 411, 1.0)
    corner_foliage(c, "tr", (60, 130, 80), 412, 0.9)
    hanging_vines(c, (60, 140, 780, 860), 150, (70, 150, 80), 413)


# ------------------------------------------------------------------- 42 porthole (inside the frame element)
def frame_Level42(c, m=False):
    # pipes and valves, a chart and a hatch sign on the walls around the porthole
    for pts in (((0, 250), (170, 250), (170, 30)), ((900, 300), (740, 300), (740, 560)), ((0, 560), (300, 560), (300, 600))):
        piece(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 14) for i in range(len(pts) - 1)], (150, 120, 80), shadow=PROP)
    for x, y in ((170, 150), (740, 420)):
        piece(c, Circ(x, y, 16), (200, 60, 60), border=1.5, shadow=SMALL)
        flat(c, [Thick(x - 16, y, x + 16, y, 3), Thick(x, y - 16, x, y + 16, 3)], (150, 40, 40))
    piece(c, RRect(30, 300, 150, 400, 3), (190, 214, 236) if on("chart", m) else (230, 220, 190), border=2, shadow=PROP)
    for k in range(5):
        flat(c, Thick(40, 316 + k * 16, 140, 316 + k * 16, 1.2), (150, 140, 120))
    flat(c, Poly(star_pts(110, 360, 12, 4, points=4, rot=0)), (200, 80, 70))
    piece(c, RRect(770, 200, 880, 260, 4), (90, 190, 120) if on("plaque", m) else (250, 210, 60), border=2, shadow=PROP)
    flat(c, [Thick(790, 230, 860, 230, 4)], (60, 50, 50))
    piece(c, [RRect(806, 500, 866, 600, 10)], (210, 60, 50), border=2, shadow=PROP)


# ------------------------------------------------------------------- 43 pirate ship
def back_Level43(c, d):
    puffs(c, [(620, 70, 0.7), (860, 110, 0.5), (360, 140, 0.45)])
    birds(c, [(700, 160, 8), (720, 150, 6), (120, 120, 7), (140, 112, 5)])
    sea = 418
    piece(c, Poly([(-20, sea), (40, sea - 30), (120, sea - 44), (200, sea - 20), (260, sea)]), (150, 180, 160), shadow=None)
    piece(c, Poly([(540, sea), (590, sea - 24), (660, sea - 30), (700, sea)]), (160, 186, 170), shadow=None)
    puffs(c, [(80, 60, 0.8), (240, 100, 0.55), (460, 50, 0.5)])


def front_Level43(c, d):
    for x, k in ((60, 0.5), (240, 0.35)):
        y = 418
        piece(c, [Poly([(x - 30 * k * 2, y), (x + 30 * k * 2, y), (x + 22 * k * 2, y + 8), (x - 22 * k * 2, y + 8)]),
                  Thick(x, y, x, y - 60 * k * 2, 2), Poly([(x + 2, y - 56 * k * 2), (x + 2, y - 10), (x + 26 * k * 2, y - 10)])], (120, 140, 170),
              shadow=None)


# ------------------------------------------------------------------- 44 desert oasis
def back_Level44(c, d):
    puffs(c, [(620, 70, 0.6), (820, 110, 0.5), (90, 80, 0.7), (380, 120, 0.5)], col=(255, 246, 228))
    birds(c, [(470, 150, 8), (490, 140, 6), (760, 180, 7)])
    far_skyline(c, 300, 20, 60, (226, 186, 130), 440, x0=560, x1=760)


def front_Level44(c, d):
    scatter(c, (0, 505, 900, 598), 28, 441, [(2, pebble((210, 170, 110))), (1, shrub((150, 160, 90)))],
            avoid=[(130, 420, 390, 520), (370, 470, 460, 520), (420, 430, 700, 500), (740, 400, 840, 520)])
    for x in range(0, 900, 60):
        flat(c, Thick(x, 560 + (x % 120) * 0.1, x + 40, 556 + (x % 120) * 0.1, 2), (226, 180, 110))


# ------------------------------------------------------------------- 45 western town
def back_Level45(c, d):
    puffs(c, [(300, 60, 0.6), (620, 90, 0.5), (820, 50, 0.45)])
    birds(c, [(500, 120, 8)])


def front_Level45(c, d):
    scatter(c, (0, 480, 900, 598), 30, 451, [(2, pebble((190, 150, 110))), (2, tuft((170, 150, 90))), (1, shrub((150, 150, 90)))],
            avoid=[(90, 510, 200, 570), (420, 480, 520, 580), (580, 460, 730, 570), (-10, 535, 910, 575)])
    piece(c, [RRect(760, 480, 900, 488, 2), RRect(760, 500, 900, 508, 2)], (150, 110, 80), shadow=SMALL)
    for x in range(770, 900, 30):
        piece(c, RRect(x, 470, x + 8, 520, 2), (140, 100, 70), shadow=SMALL)


# ------------------------------------------------------------------- 46 harbour pub
def front_Level46(c, d):
    for k in range(9):
        x = 20 + k * 100
        pts = [(x, 6), (x + 50, 20), (x + 100, 6)]
        flat(c, [Thick(pts[0][0], pts[0][1], pts[1][0], pts[1][1], 1.4), Thick(pts[1][0], pts[1][1], pts[2][0], pts[2][1], 1.4)], (90, 70, 60))
        piece(c, Poly([(x + 40, 16), (x + 60, 16), (x + 50, 34)]), [(230, 80, 80), (250, 220, 90), (90, 150, 220)][k % 3], shadow=SMALL)
    for k in range(6):
        for j in range(5):
            flat(c, Circ(20 + k * 18, 60 + j * 26, 1.6), (220, 200, 150))
    for k in range(7):
        flat(c, [Thick(10 + k * 16, 50, 10 + k * 16, 180, 1), Thick(10, 50 + k * 20, 110, 50 + k * 20, 1)], (200, 180, 140))
    for x, y in ((30, 190), (80, 196)):
        piece(c, Circ(x, y, 9), (230, 90, 70), shadow=SMALL)
    picture_frame(c, 780, 40, 90, 70, (120, 80, 50), [(150, 200, 230), (90, 120, 160), (250, 240, 220)], 3)
    shelf(c, 470, 640, 300, (120, 80, 50), 461, [(90, 140, 90), (160, 90, 60), (220, 200, 150)])
    for x in (30, 75):
        barrel_(c, x, 600, None)


# ------------------------------------------------------------------- 49 animal town
def back_Level49(c, d):
    far_ridge(c, 300, 50, (180, 214, 170), 49)
    for x in (60, 240, 470, 690, 860):
        piece(c, [RRect(x - 18, 262, x + 18, 300, 1), Poly([(x - 22, 264), (x + 22, 264), (x, 244)])], (230, 220, 200), shadow=None)


def front_Level49(c, d):
    for (x0, x1) in ((0, 440), (460, 900)):
        pts = [(x0 + (x1 - x0) * t / 12, 40 + 26 * math.sin(math.pi * t / 12)) for t in range(13)]
        flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.4) for i in range(12)], (90, 80, 90))
        for i in range(12):
            mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
            piece(c, Poly([(mx - 8, my), (mx + 8, my), (mx, my + 16)]), [(230, 80, 80), (250, 210, 70), (90, 160, 220), (120, 200, 120)][i % 4],
                  shadow=None)


# ------------------------------------------------------------------- 50 alchemy lab
def front_Level50(c, d):
    for x in (350, 380):
        flat(c, Thick(x, 0, x, 60, 1.2), (90, 80, 70))
        piece(c, [Ell(x, 70, 10, 16), Thick(x, 56, x, 86, 2)], (120, 160, 90), shadow=SMALL)
    piece(c, RRect(640, 40, 760, 108, 2), (230, 214, 170), border=1.5, shadow=PROP)
    c.ellipse_ring(700, 74, 24, 24, 2, (150, 90, 60))
    flat(c, Poly(star_pts(700, 74, 18, 7)), (180, 110, 70, 0.6))
    piece(c, RRect(780, 50, 860, 104, 2), (226, 210, 166), border=1.5, shadow=PROP)
    for k in range(4):
        flat(c, Thick(790, 62 + k * 10, 850, 62 + k * 10, 1.2), (150, 110, 80))
    for x in (40, 860):
        flat(c, [Thick(x, 0, x, 300, 2)], (100, 90, 90))
    piece(c, [Ell(70, 560, 40, 14)], (110, 80, 120), border=1.5, shadow=SMALL)
    for x, y in ((60, 540), (80, 534), (100, 544)):
        piece(c, [Ell(x, y, 8, 10)], (90, 160, 110), shadow=SMALL)


# ------------------------------------------------------------------- 51 floating isles
def back_Level51(c, d):
    for x, y, w in ((60, 120, 40), (330, 90, 30), (640, 60, 36), (860, 180, 30), (300, 420, 34), (640, 440, 28)):
        piece(c, Poly([(x - w, y), (x + w, y), (x + w * 0.3, y + w * 0.9), (x - w * 0.3, y + w * 0.6)]), (196, 190, 214), shadow=None)
        flat(c, Ell(x, y, w + 3, 6), (186, 214, 196))
    cloud_bank(c, 470, (240, 242, 252), 51, 0.9)
    birds(c, [(720, 120, 7), (740, 110, 5)])


# ------------------------------------------------------------------- 52 fairy forest
def front_Level52(c, d):
    corner_foliage(c, "tl", (50, 110, 80), 521, 0.9)
    corner_foliage(c, "tr", (50, 110, 80), 522, 0.9)

    def mush(c, x, y, rnd):
        col = rnd.choice(((240, 200, 120), (230, 130, 170), (170, 140, 230)))
        piece(c, [RRect(x - 2, y - 10, x + 2, y, 1)], (245, 236, 220), shadow=None)
        piece(c, Ell(x, y - 10, 8, 5), col, shadow=SMALL)
    scatter(c, (0, 525, 900, 598), 26, 523, [(2, mush), (2, flowerlet([(255, 160, 220), (160, 220, 255)])), (1, tuft((60, 120, 70)))],
            avoid=[(380, 440, 470, 490), (700, 470, 860, 545), (240, 390, 290, 430)])


# ------------------------------------------------------------------- 53 wizard tower (outside the tower)
def back_Level53(c, d):
    far_ridge(c, 600, 200, (40, 44, 90), 53)
    far_ridge(c, 600, 120, (54, 54, 104), 530)
    for x, h in ((80, 220), (840, 260)):
        piece(c, [RRect(x - 16, 600 - h, x + 16, 600, 2), Poly([(x - 22, 600 - h), (x + 22, 600 - h), (x, 600 - h - 50)])], (60, 60, 110), shadow=None)
        flat(c, RRect(x - 4, 600 - h + 30, x + 4, 600 - h + 44, 2), (255, 220, 140))
    puffs(c, [(140, 260, 0.6), (780, 160, 0.6), (830, 330, 0.5)], col=(80, 80, 140), shadow=None)
    far_forest(c, 600, 120, (30, 36, 70), 531, spacing=18, x0=-20, x1=215)
    far_forest(c, 600, 120, (30, 36, 70), 532, spacing=18, x0=685, x1=920)
    for x, y in ((40, 520), (130, 500), (760, 520), (860, 490)):
        piece(c, [RRect(x - 18, y, x + 18, y + 40, 1), Poly([(x - 24, y + 2), (x + 24, y + 2), (x, y - 22)])], (50, 50, 90), shadow=None)
        flat(c, RRect(x - 6, y + 12, x + 6, y + 24, 1), (255, 210, 120))


# ------------------------------------------------------------------- 54 magic academy
def back_Level54(c, d):
    far_ridge(c, 330, 120, (160, 170, 210), 54)
    puffs(c, [(140, 70, 0.6), (780, 90, 0.5)])


def front_Level54(c, d):
    far_forest(c, 470, 40, (80, 130, 90), 541, spacing=22, x0=-20, x1=60)
    far_forest(c, 470, 40, (80, 130, 90), 542, spacing=22, x0=860, x1=920)
    corner_foliage(c, "br", (70, 130, 80), 543, 0.8)


# ------------------------------------------------------------------- 55 dark fantasy
def back_Level55(c, d):
    cloud_bank(c, 30, (70, 56, 80), 55, 1.2)
    far_ridge(c, 470, 110, (60, 50, 74), 550)
    for x, h in ((120, 160), (210, 120), (820, 150)):
        piece(c, [RRect(x - 10, 470 - h, x + 10, 470, 1), Poly([(x - 14, 470 - h), (x + 14, 470 - h), (x, 470 - h - 40)])], (50, 44, 62), shadow=None)


def front_Level55(c, d):
    for x, y, s_ in ((60, 470, 1.0), (250, 480, 0.8)):
        flat(c, [Thick(x, y, x, y - 110 * s_, 6 * s_), Thick(x, y - 70 * s_, x - 40 * s_, y - 110 * s_, 3 * s_),
                 Thick(x, y - 90 * s_, x + 36 * s_, y - 130 * s_, 3 * s_), Thick(x - 20 * s_, y - 90 * s_, x - 30 * s_, y - 130 * s_, 2)], (36, 30, 44))
    puffs(c, [(150, 230, 0.8), (320, 180, 0.6)], col=(80, 66, 92), shadow=None)
    birds(c, [(120, 160, 7), (200, 120, 6), (300, 260, 6)], col=(30, 24, 36))
    for x in range(10, 900, 24):
        if 330 < x < 450:
            continue
        flat(c, [Thick(x, 600, x, 556, 3), Poly([(x - 4, 556), (x, 548), (x + 4, 556)])], (40, 36, 46))
    flat(c, [Thick(0, 572, 330, 572, 2.5), Thick(450, 572, 900, 572, 2.5)], (40, 36, 46))


# ------------------------------------------------------------------- 57 sky city
def front_Level57(c, d):
    puffs(c, [(70, 70, 1.1), (860, 470, 1.0), (90, 330, 0.7), (820, 300, 0.6)], col=(250, 252, 255))
    birds(c, [(250, 560, 9), (275, 548, 7), (720, 80, 8)])


# ------------------------------------------------------------------- 59 miniature world (top-down)
def front_Level59(c, d):
    def house_(c, x, y, rnd):
        col = rnd.choice(((200, 80, 70), (90, 130, 200), (230, 180, 70), (150, 90, 160)))
        piece(c, RRect(x - 22, y - 16, x + 22, y + 16, 2), col, border=1.5, shadow=(4, 6, 5, 0.45))
        flat(c, RRect(x - 22, y - 16, x + 22, y, 2), lit(col, 1.15))

    def tree_(c, x, y, rnd):
        piece(c, Circ(x, y, rnd.uniform(9, 14)), (60, 130, 70), shadow=(4, 6, 5, 0.45))

    def field(c, x, y, rnd):
        col = rnd.choice(((190, 170, 90), (150, 190, 110)))
        flat(c, RRect(x - 30, y - 18, x + 30, y + 18, 2), col)
        for k in range(4):
            flat(c, Thick(x - 28, y - 12 + k * 8, x + 28, y - 12 + k * 8, 1.2), lit(col, 0.85))
    scatter(c, (10, 140, 410, 270), 7, 590, [(2, tree_), (1, house_)], avoid=[(240, 150, 400, 250), (130, 230, 230, 280)])
    scatter(c, (500, 130, 890, 270), 8, 591, [(2, tree_), (1, house_), (1, field)], avoid=[])
    scatter(c, (10, 480, 410, 590), 8, 592, [(2, tree_), (1, field)], avoid=[(260, 440, 340, 500)])
    scatter(c, (500, 520, 640, 590), 4, 593, [(2, tree_)], avoid=[])


# ------------------------------------------------------------------- vehicles (interior elements)
def interior_Level62(c):
    piece(c, RRect(-10, -10, W + 10, 40, 6), (214, 216, 222), border=1.5, shadow=PROP)
    for x in range(0, 900, 120):
        flat(c, Thick(x, 6, x, 38, 1.5), (196, 198, 206))
    piece(c, RRect(730, 80, 860, 130, 8), (60, 64, 76), border=1.5, shadow=SMALL)
    flat(c, [Circ(760, 105, 9), Circ(830, 105, 9)], (240, 240, 245))
    flat(c, [Thick(752, 105, 768, 105, 3), Thick(822, 97, 838, 113, 3)], (60, 64, 76))
    for y in range(160, 460, 60):
        flat(c, Thick(0, y, 210, y, 1.2), (220, 220, 226))
        flat(c, Thick(712, y, 900, y, 1.2), (220, 220, 226))
    piece(c, RRect(170, 520, 420, 620, 30), (60, 80, 130), border=2, shadow=PROP)
    flat(c, RRect(190, 530, 400, 560, 10), (250, 250, 250))
