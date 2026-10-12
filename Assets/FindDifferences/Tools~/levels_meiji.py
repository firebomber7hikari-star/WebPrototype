# -*- coding: utf-8 -*-
"""Meiji Japan (1868-1912), paper-craft side views, full-bleed:
  Level84 银座砖街 - Ginza brick street: colonnades, gas lamps, willows, horse tram, rickshaw; day / night
  Level85 新桥驿   - opening of the railway at Shinbashi: station, steam locomotive, crowds, bunting
  Level86 鹿鸣馆   - a ball at the Rokumeikan: lit arcades, dancing couples, carriages in the garden; day / night
  Level87 横滨港   - Yokohama harbour: steamship, brick warehouses, tea chests, Mt Fuji beyond; clear -> rain
  Level88 富冈制丝 - Tomioka silk mill in spring: long brick hall, chimney, mulberry fields, cherry trees
"""
import math
import random

from fdcore import CLEAR, E, H, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_el, drift_across, gy, layer, sky, smoke_el
from stylekit import day_night, star_field, window_glow
from weather import CLOUDY, SUNNY, WET, cloud, rain_layer
from levels_heian import blossom_tree, pine_jp, stone_lantern
from jp_kit import (SKIN, TILE, arch, ashigaru, ellipse_top, kimono, lady_west, locomotive, rickshaw, steamship, tile_roof, westerner)

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
BRICK = (178, 82, 62)
STONE = (226, 218, 200)


def brick_front(c, x0, x1, top, base, col=BRICK, wins=4, arcade=True):
    piece(c, RRect(x0, top, x1, base, 1), col, border=1.5, shadow=PROP)
    for y in range(int(top + 6), int(base), 8):
        flat(c, Thick(x0, y, x1, y, 0.7), lit(col, 0.88))
    w = (x1 - x0) / wins
    rects = []
    for k in range(wins):
        cx = x0 + w * (k + 0.5)
        flat(c, arch(cx - w * 0.22, cx + w * 0.22, top + 14, top + (base - top) * 0.42), (246, 240, 228))
        flat(c, arch(cx - w * 0.17, cx + w * 0.17, top + 18, top + (base - top) * 0.42 - 3), (70, 80, 100))
        rects.append((cx - w * 0.17, top + 24, cx + w * 0.17, top + (base - top) * 0.42 - 3))
    if arcade:
        my = top + (base - top) * 0.52
        piece(c, RRect(x0 - 4, my - 6, x1 + 4, my, 1), STONE, shadow=SMALL)
        for k in range(wins + 1):
            px = x0 + w * k
            piece(c, RRect(px - 4, my, px + 4, base, 1), STONE, shadow=SMALL)
        for k in range(wins):
            cx = x0 + w * (k + 0.5)
            flat(c, RRect(cx - w * 0.36, my + 8, cx + w * 0.36, base, 0), (60, 54, 54))
    piece(c, RRect(x0 - 6, top - 8, x1 + 6, top + 2, 1), STONE, shadow=SMALL)
    return rects


def gas_lamp(c, x, base, h=110):
    piece(c, [Thick(x, base, x, base - h, 4), RRect(x - 8, base - 6, x + 8, base, 2), Thick(x - 12, base - h + 20, x + 12, base - h + 20, 2)],
          (40, 50, 50), shadow=PROP)
    piece(c, Poly([(x - 9, base - h), (x + 9, base - h), (x + 12, base - h - 22), (x - 12, base - h - 22)]), (40, 50, 50), shadow=SMALL)
    flat(c, Poly([(x - 6, base - h - 2), (x + 6, base - h - 2), (x + 8, base - h - 18), (x - 8, base - h - 18)]), (240, 226, 170))
    flat(c, Poly([(x - 14, base - h - 22), (x + 14, base - h - 22), (x, base - h - 32)]), (40, 50, 50))
    return (x, base - h - 10)


def telegraph(c, xs, top, base):
    for x in xs:
        flat(c, Thick(x, base, x, top, 4), (110, 84, 64))
        flat(c, [Thick(x - 16, top + 8, x + 16, top + 8, 2.5), Thick(x - 12, top + 20, x + 12, top + 20, 2.5)], (110, 84, 64))
    for k in range(len(xs) - 1):
        for dy in (8, 20):
            a, b = xs[k], xs[k + 1]
            pts = [(a + (b - a) * t / 10, top + dy + 14 * math.sin(math.pi * t / 10)) for t in range(11)]
            flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1) for i in range(10)], (60, 60, 64))


def willow_el(eid, x, base, phase):
    def d(c, m):
        for k in range(9):
            sx = x - 40 + k * 10
            pts = [(sx + 4 * math.sin(j * 0.7 + k), base - 120 + j * 15) for j in range(7)]
            flat(c, [Thick(pts[j][0], pts[j][1], pts[j + 1][0], pts[j + 1][1], 1.4) for j in range(6)], (100, 150, 80))
            for j in range(1, 7):
                flat(c, Ell(pts[j][0] + 2, pts[j][1], 3, 1.6), (124, 178, 96))
    return E(eid, d, pivot=(x, base - 120), anim=dict(swingAngle=3, swingSpeed=0.18, phase=phase))


def willow_trunk(c, x, base):
    piece(c, [Thick(x, base, x - 4, base - 116, 8), Thick(x - 4, base - 96, x - 28, base - 124, 4), Thick(x, base - 106, x + 24, base - 128, 4)],
          (110, 90, 70), shadow=SMALL)


# =================================================================== Level 84 Ginza brick street (day / night)
DN84 = day_night(40.0, tint=(0.30, 0.32, 0.58))
FRONTS84 = [(-10, 150, BRICK), (150, 300, (196, 110, 80)), (300, 450, BRICK), (450, 600, (188, 96, 70)), (600, 750, BRICK), (750, 910, (196, 110, 80))]
LAMPS84 = [120, 380, 640, 880]
WILLOWS84 = [250, 760]


def l84_bg(c, d):
    sky(c, (160, 200, 236), (246, 232, 210), 300)
    for x0, x1, col in FRONTS84:
        brick_front(c, x0, x1, 210, 446, col, wins=4)
    # clock tower in the middle
    piece(c, RRect(500, 130, 550, 204, 1), STONE, border=1.5, shadow=PROP)
    piece(c, Poly([(494, 132), (556, 132), (525, 100)]), TILE, border=1.2, shadow=SMALL)
    piece(c, Circ(525, 164, 16), (250, 248, 240), border=1.5, shadow=SMALL)
    if "clock" in d:
        flat(c, [Thick(525, 164, 516, 170, 2.4), Thick(525, 164, 525, 176, 1.8)], INK)
    else:
        flat(c, [Thick(525, 164, 533, 158, 2.4), Thick(525, 164, 525, 151, 1.8)], INK)
    if "flag" not in d:
        flat(c, Thick(220, 204, 220, 150, 2), (90, 80, 80))
        piece(c, RRect(221, 150, 249, 168, 1), (250, 250, 246), shadow=SMALL)
        flat(c, Circ(235, 159, 5), (210, 40, 50))
    # shop signs
    for i, x in enumerate((40, 330, 620, 820)):
        col = ((60, 130, 80) if "sign" in d else (40, 40, 60)) if i == 2 else [(40, 40, 60), (150, 40, 40), None, (90, 70, 40)][i]
        piece(c, RRect(x, 330, x + 20, 380, 1), col, border=1.2, border_col=(226, 186, 80), shadow=SMALL)
        flat(c, [Thick(x + 10, 338, x + 10, 372, 2)], (240, 230, 200))
    # sidewalk, street, rails
    piece(c, RRect(-10, 446, 910, 470, 0), (200, 196, 186), shadow=SMALL)
    c.rect(0, 470, W, H, (176, 164, 140))
    for y in (536, 552):
        flat(c, Thick(0, y, 900, y, 3), (120, 120, 126))
    telegraph(c, [60, 480, 900], 170, 470)
    for x in LAMPS84:
        gas_lamp(c, x, 470)
    for x in WILLOWS84:
        willow_trunk(c, x, 470)
    # horse tram
    tram = (40, 110, 70) if "tram" in d else (170, 50, 50)
    piece(c, RRect(560, 470, 720, 538, 4), tram, border=1.5, shadow=PROP)
    piece(c, RRect(552, 462, 728, 472, 2), (240, 232, 214), shadow=SMALL)
    for k in range(5):
        flat(c, RRect(570 + k * 30, 480, 592 + k * 30, 502, 2), (220, 236, 244))
    for wx in (590, 690):
        c.ellipse_ring(wx, 540, 10, 10, 3, (50, 50, 56))
    flat(c, Thick(720, 520, 760, 520, 2.5), (90, 70, 60))
    for lx in (-20, -10, 12, 22):
        flat(c, RRect(790 + lx - 3, 530, 790 + lx + 3, 560, 1), (110, 76, 50))
    piece(c, [Ell(790, 524, 30, 13), Poly([(812, 520), (826, 492), (834, 496), (822, 524)]), Ell(834, 494, 10, 7)], (140, 96, 64), border=1.5,
          shadow=PROP)
    # people
    rickshaw(c, 150, 596, hood=(60, 110, 160) if "hood" in d else (40, 40, 50))
    westerner(c, 360, 598, (50, 50, 64), hat="bowler", hat_col=(120, 84, 56) if "bowler" in d else (30, 30, 34))
    lady_west(c, 430, 598, (160, 60, 90), parasol=None)
    hx, hy = kimono(c, 500, 598, (70, 90, 130), hair="woman")
    flat(c, Thick(508, 570, 514, 528, 1.4), (110, 80, 60))
    piece(c, ellipse_top(514, 530, 22, 12), (240, 170, 60) if "parasol" in d else (150, 80, 160), border=1.2, shadow=SMALL)
    westerner(c, 860, 600, (40, 50, 90), hat="kepi", hat_col=(40, 50, 90), trousers=(40, 50, 90))
    kimono(c, 600, 600, (130, 110, 80), h=0.75)
    kimono(c, 640, 600, (60, 60, 70))


L84_WIN = [(x0 + (x1 - x0) / 4 * (k + 0.5 - 0.17), 234, x0 + (x1 - x0) / 4 * (k + 0.5 + 0.17), 306) for x0, x1, _ in FRONTS84 for k in range(4)]

L84_ELEMENTS = [
    cloud_el("cloud0", 300, 60, 0.7, 7, daynight="day"),
    E("moon", lambda c, m: (soft_union(c, [Circ(760, 80, 30)], (255, 250, 220), 0.35, spread=18),
                            piece(c, Circ(760, 80, 24), (252, 246, 220), border=2, shadow=PROP)), daynight="night"),
    star_field("stars", 84, 30, 140, avoid=[(700, 30, 820, 130)]),
    window_glow("windows", L84_WIN),
    E("lamp_glow", lambda c, m: soft_union(c, [Circ(x, 350, 12) for x in LAMPS84], (255, 214, 130), 0.6, spread=36), daynight="night",
      anim=dict(twinkle=0.12, twinkleSpeed=0.9)),
] + [willow_el("willow%d" % i, x, 470, i * 0.4) for i, x in enumerate(WILLOWS84)] + [
    bird_el("bird0", 420, 120, 8, speed=16, daynight="day"),
    E("horse_head", lambda c, m: flat(c, Thick(840, 494, 848, 500, 3), (60, 40, 30)), pivot=(834, 494), anim=dict(swingAngle=6, swingSpeed=0.5)),
]

L84_DIFFS = [
    ("clock", 525, 164, 0),
    ("flag", 235, 159, 0),
    ("sign", 630, 355, 0),
    ("tram", 640, 504, 0),
    ("hood", 140, 540, 0),
    ("bowler", 361, 548, 0),
    ("parasol", 514, 524, 0),
]


# =================================================================== Level 85 Shinbashi station, opening day
LOCO85 = (540, 528)


def l85_bg(c, d):
    sky(c, (166, 204, 236), (246, 234, 214), 300)
    layer(c, 240, [(14, 0.01, 0.4)], (170, 186, 180))
    # station building
    piece(c, RRect(30, 250, 400, 440, 1), STONE, border=1.5, shadow=PROP)
    piece(c, Poly([(20, 252), (410, 252), (380, 214), (50, 214)]), (90, 96, 110), border=1.5, shadow=SMALL)
    for x in range(52, 392, 34):
        flat(c, arch(x, x + 16, 270, 318), (90, 100, 120))
        flat(c, arch(x, x + 16, 350, 410), (90, 100, 120))
    piece(c, RRect(170, 200, 260, 260, 1), STONE, border=1.5, shadow=PROP)
    piece(c, Poly([(162, 202), (268, 202), (215, 170)]), STONE, border=1.5, shadow=SMALL)
    piece(c, Circ(215, 228, 15), (250, 248, 240), border=1.5, shadow=SMALL)
    if "clock" in d:
        flat(c, [Thick(215, 228, 206, 232, 2.4), Thick(215, 228, 215, 240, 1.8)], INK)
    else:
        flat(c, [Thick(215, 228, 223, 222, 2.4), Thick(215, 228, 215, 215, 1.8)], INK)
    for x in (180, 200, 230, 250):
        piece(c, RRect(x - 4, 372, x + 4, 440, 1), (240, 236, 226), shadow=SMALL)
    # platform canopy and bunting
    piece(c, RRect(400, 250, 910, 262, 1), (110, 90, 80), border=1.2, shadow=PROP)
    for x in range(420, 910, 90):
        flat(c, Thick(x, 262, x, 450, 4), (90, 80, 76))
    pts = [(400 + k * 30, 270 + 10 * abs(math.sin(math.pi * k / 3))) for k in range(18)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(17)], (70, 60, 60))
    for i in range(17):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        col = ((60, 130, 200) if "bunting" in d else (220, 50, 50)) if i == 9 else [(220, 50, 50), (250, 250, 246)][i % 2]
        flat(c, Poly([(mx - 8, my), (mx + 8, my), (mx, my + 14)]), col)
    piece(c, RRect(390, 440, 910, 460, 0), (200, 192, 176), shadow=SMALL)
    # crowd on the platform
    rnd = random.Random(85)
    for x in range(420, 900, 26):
        col = rnd.choice(((60, 70, 110), (150, 60, 70), (90, 110, 80), (40, 40, 46), (200, 170, 110)))
        if rnd.random() < 0.4:
            westerner(c, x, 446, col, h=0.8, hat=rnd.choice(("top", "bowler")))
        else:
            kimono(c, x, 446, col, h=0.8, hair=rnd.choice(("man", "woman")))
    # tracks
    piece(c, RRect(-10, 524, 910, 612, 0), (150, 140, 124), shadow=LAYER)
    for x in range(-10, 910, 26):
        flat(c, RRect(x, 524, x + 14, 540, 1), (120, 92, 70))
    flat(c, [Thick(0, 526, 900, 526, 3), Thick(0, 538, 900, 538, 3)], (150, 150, 160))
    # train: coaches + locomotive
    for k, x in enumerate((60, 220, 380)):
        piece(c, RRect(x, 450, x + 150, 512, 3), (120, 60, 50) if k != 1 else (60, 80, 120), border=1.5, shadow=PROP)
        piece(c, Poly([(x - 4, 452), (x + 154, 452), (x + 146, 440), (x + 4, 440)]), (90, 90, 96), shadow=SMALL)
        for j in range(5):
            flat(c, RRect(x + 10 + j * 28, 462, x + 30 + j * 28, 484, 2), (220, 232, 240))
        for wx in (x + 30, x + 120):
            c.ellipse_ring(wx, 516, 10, 10, 3, (50, 50, 56))
    wheel = (60, 120, 180) if "wheel" in d else (200, 60, 50)
    locomotive(c, LOCO85[0], LOCO85[1], wheel=wheel, funnel="straight" if "funnel" in d else "balloon")
    # semaphore, stationmaster, luggage, onlookers
    flat(c, Thick(830, 524, 830, 380, 4), (90, 80, 76))
    a = math.radians(-40 if "semaphore" in d else 0)
    piece(c, Poly([(832, 392), (832 + 40 * math.cos(a), 392 + 40 * math.sin(a)), (832 + 40 * math.cos(a), 400 + 40 * math.sin(a)), (832, 400)]),
          (220, 50, 50), border=1.2, shadow=SMALL)
    piece(c, Circ(830, 384, 6), (240, 220, 140), shadow=None)
    westerner(c, 780, 600, (30, 40, 70), hat="kepi", hat_col=(200, 50, 50) if "cap" in d else (30, 40, 70), trousers=(30, 40, 70))
    n = 2 if "luggage" in d else 3
    for k in range(n):
        piece(c, RRect(860 + (k % 2) * 4 - 18, 584 - k * 16, 860 + (k % 2) * 4 + 18, 600 - k * 16, 2), (150, 100, 60), border=1.2, shadow=PROP)
    for x, col in ((60, (150, 60, 80)), (110, (60, 80, 120)), (170, (130, 110, 80))):
        kimono(c, x, 600, col, umbrella=(200, 60, 60) if x == 110 else None)


L85_ELEMENTS = [
    cloud_el("cloud0", 300, 70, 0.7, 7), cloud_el("cloud1", 700, 50, 0.6, 6),
] + smoke_el("smoke", LOCO85[0] + 133, LOCO85[1] - 110, n=5, col=(220, 220, 224), r=10, rise=(-30, 26), length=110) + \
    smoke_el("steam", LOCO85[0] + 160, LOCO85[1] - 10, n=3, col=(250, 250, 250), r=7, rise=(26, 6), length=50) + [
    bird_el("bird0", 560, 120, 8, speed=16)]

L85_DIFFS = [
    ("clock", 215, 228, 0),
    ("bunting", 685, 283, 0),
    ("wheel", LOCO85[0] + 70, LOCO85[1] - 22, 0),
    ("funnel", LOCO85[0] + 133, LOCO85[1] - 92, 0),
    ("semaphore", 850, 400, 0),
    ("cap", 781, 545, 0),
    ("luggage", 864, 560, 0),
]


# =================================================================== Level 86 Rokumeikan ball (day / night)
DN86 = day_night(40.0, tint=(0.28, 0.28, 0.52))
WIN86 = [(x, y, x + 50, y + 70) for y in (210, 320) for x in range(270, 880, 76)]


def couple(c, x, base, dress, coat=(30, 30, 40), h=0.9):
    westerner(c, x - 8 * h, base, coat, h=h, hat=None)
    lady_west(c, x + 8 * h, base, dress, h=h, hat=None)


def l86_bg(c, d):
    sky(c, (160, 196, 230), (240, 224, 206), 300)
    layer(c, 250, [(14, 0.01, 0.4)], (150, 170, 150))
    # building with two arcaded floors, cut open to show the ballroom
    piece(c, RRect(240, 170, 910, 420, 1), (240, 232, 214), border=2, shadow=PROP)
    piece(c, Poly([(230, 172), (920, 172), (900, 140), (250, 140)]), (100, 106, 120), border=1.5, shadow=SMALL)
    for i, (x, y, x1, y1) in enumerate(WIN86):
        flat(c, arch(x - 4, x1 + 4, y - 4, y1), (250, 246, 236))
        flat(c, arch(x, x1, y, y1), (120, 96, 80))
    flat(c, RRect(240, 300, 910, 310, 0), (226, 216, 196))
    # chandeliers (one has fewer candles in B)
    for i, cx in enumerate((345, 573, 801)):
        if i == 1 and "chandelier" in d:
            continue
        n = 5
        flat(c, Thick(cx, 210, cx, 228, 1.4), (200, 170, 90))
        piece(c, Ell(cx, 232, 22, 5), (226, 186, 80), shadow=None)
        for k in range(n):
            flat(c, Circ(cx - 16 + k * 32 / max(1, n - 1), 224, 2.6), (255, 236, 160))
    # dancing couples in the lower windows
    for i, (x, y, x1, y1) in enumerate(WIN86[8:]):
        dress = ((120, 200, 160) if "dress" in d else (230, 120, 150)) if i == 3 else [(230, 120, 150), (150, 170, 230), (240, 220, 150)][i % 3]
        couple(c, (x + x1) / 2, y1 - 4, dress, h=0.75)
    # entrance porch, flags, garden
    piece(c, RRect(160, 300, 240, 420, 1), (240, 232, 214), border=1.5, shadow=PROP)
    flat(c, arch(176, 224, 330, 420), (90, 70, 60))
    for x, flag in ((300, "jp"), (850, "flag")):
        flat(c, Thick(x, 140, x, 90, 2), (90, 80, 80))
        if flag == "jp":
            piece(c, RRect(301, 90, 333, 110, 1), (250, 250, 246), shadow=SMALL)
            flat(c, Circ(317, 100, 5.5), (210, 40, 50))
        else:
            col = (60, 130, 80) if "flag" in d else (200, 50, 50)
            piece(c, RRect(851, 90, 883, 110, 1), col, shadow=SMALL)
            flat(c, Poly(star_pts(867, 100, 6, 2.6)), (250, 230, 120))
    piece(c, RRect(-10, 420, 910, 612, 0), (140, 166, 110), shadow=LAYER)
    piece(c, Poly([(150, 612), (250, 420), (320, 420), (420, 612)]), (220, 210, 186), shadow=None)
    pine_jp(c, 60, 470, 1.4)
    stone_lantern(c, 130, 470, 0.7)
    if "lamp" not in d:
        gas_lamp(c, 450, 520, 90)
    # carriage with crest, horses, footman
    for wx in (560, 650):
        c.ellipse_ring(wx, 560, 24, 24, 3, (40, 36, 36))
    piece(c, Poly([(530, 550), (540, 486), (670, 486), (680, 550)]), (30, 30, 40), border=1.5, shadow=PROP)
    flat(c, RRect(560, 496, 600, 526, 3), (190, 210, 220))
    piece(c, Circ(630, 516, 8), (200, 200, 210) if "crest" in d else (226, 186, 80), shadow=None)
    for hx in (740, 790):
        for lx in (-18, -8, 12, 20):
            flat(c, RRect(hx + lx - 3, 540, hx + lx + 3, 576, 1), (60, 50, 50))
        piece(c, [Ell(hx, 534, 28, 12), Poly([(hx + 20, 530), (hx + 34, 500), (hx + 42, 504), (hx + 30, 534)]), Ell(hx + 42, 502, 10, 6)],
              (70, 56, 50), border=1.5, shadow=PROP)
    flat(c, Thick(680, 530, 770, 530, 2), (90, 70, 60))
    westerner(c, 500, 586, (40, 40, 56), hat="top", hat_col=(200, 190, 170) if "footman" in d else (30, 30, 34))
    lady_west(c, 440, 590, (200, 80, 110), hat=(240, 230, 210))
    westerner(c, 410, 590, (30, 30, 40), hat="top")
    if "palm" not in d:
        piece(c, RRect(860, 560, 890, 596, 3), (150, 100, 70), border=1.2, shadow=PROP)
        for a in (-60, -30, 0, 30, 60):
            r = math.radians(a - 90)
            flat(c, Thick(875, 560, 875 + 34 * math.cos(r), 560 + 34 * math.sin(r) + 10, 4), (70, 140, 80))


def l86_dancers(c, m):
    for i, (x, y, x1, y1) in enumerate(WIN86[:8]):
        if i % 2:
            couple(c, (x + x1) / 2, y1 - 4, [(150, 170, 230), (240, 220, 150)][i % 2 if i % 4 else 0], h=0.7)


L86_ELEMENTS = [
    cloud_el("cloud0", 140, 60, 0.6, 6, daynight="day"),
    E("moon", lambda c, m: (soft_union(c, [Circ(120, 90, 30)], (255, 250, 220), 0.35, spread=18),
                            piece(c, Circ(120, 90, 24), (252, 246, 220), border=2, shadow=PROP)), daynight="night"),
    star_field("stars", 86, 40, 130, avoid=[(80, 50, 160, 130)]),
    E("windows_glow", lambda c, m: soft_union(c, [RRect(x, y, x1, y1, 4) for x, y, x1, y1 in WIN86], (255, 214, 140), 0.45, spread=14),
      daynight="night", anim=dict(twinkle=0.1, twinkleSpeed=0.8)),
    E("dancers", l86_dancers, anim=dict(bobAmplitude=(8, 0), bobSpeed=0.25)),
    E("lamp_glow", lambda c, m: soft_union(c, [Circ(450, 420, 10)], (255, 214, 130), 0.6, spread=30), daynight="night", show="A"),
    bird_el("bird0", 600, 90, 8, speed=14, daynight="day"),
]

L86_DIFFS = [
    ("chandelier", 573, 226, 0),
    ("dress", (WIN86[11][0] + WIN86[11][2]) / 2, WIN86[11][3] - 20, 0),
    ("flag", 867, 100, 0),
    ("crest", 630, 516, 0),
    ("footman", 501, 534, 0),
    ("lamp", 450, 470, 0),
    ("palm", 875, 560, 0),
]


# =================================================================== Level 87 Yokohama harbour (clear -> rain)
STEPS87 = [(CLEAR, 9), (OVERCAST, 5), (RAIN, 9), (OVERCAST, 4)]
WEATHER87 = dict(steps=STEPS87, blend=3.0, tints={OVERCAST: (0.86, 0.88, 0.92), RAIN: (0.74, 0.78, 0.86)})


def l87_bg(c, d):
    sky(c, (160, 204, 236), (242, 234, 218), 300)
    piece(c, Poly([(-20, 300), (80, 250), (150, 150), (172, 146), (250, 250), (360, 300)]), (130, 150, 180), shadow=LAYER)
    if "fuji" not in d:
        flat(c, Poly([(122, 190), (150, 150), (172, 146), (198, 190), (184, 182), (170, 194), (156, 180), (140, 194)]), (250, 250, 252))
    layer(c, 286, [(8, 0.012, 0.6)], (140, 166, 150))
    # bluff with foreign houses
    piece(c, Poly([(600, 300), (660, 240), (900, 220), (920, 300)]), (130, 160, 110), shadow=LAYER)
    for x in (690, 790, 870):
        piece(c, RRect(x - 30, 216, x + 30, 252, 1), (246, 240, 226), border=1.2, shadow=SMALL)
        piece(c, Poly([(x - 36, 218), (x + 36, 218), (x, 196)]), (180, 80, 70), shadow=SMALL)
        flat(c, RRect(x - 30, 240, x + 30, 244, 0), (120, 140, 160))
    c.rect(0, 298, W, 470, (70, 130, 170))
    for y in range(310, 468, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (110, 166, 200))
    steamship(c, 360, 430, funnel=(60, 110, 170) if "funnel" in d else (200, 60, 50), length=300)
    flat(c, Thick(690, 268, 690, 240, 1.6), (90, 80, 80))
    piece(c, RRect(691, 240, 719, 258, 1), (60, 140, 80) if "flag" in d else (230, 60, 50), shadow=SMALL)
    # warehouses
    piece(c, RRect(-10, 300, 220, 470, 1), BRICK, border=1.5, shadow=PROP)
    piece(c, Poly([(-14, 302), (224, 302), (204, 276), (6, 276)]), (90, 90, 100), border=1.2, shadow=SMALL)
    for y in range(306, 470, 8):
        flat(c, Thick(-10, y, 220, y, 0.7), lit(BRICK, 0.88))
    for x in (30, 130):
        piece(c, RRect(x, 380, x + 50, 470, 2), (60, 100, 70) if ("door" in d and x == 130) else (70, 60, 56), border=1.2, shadow=SMALL)
        flat(c, Thick(x + 25, 380, x + 25, 470, 2), (40, 36, 34))
    for x in (30, 90, 150):
        flat(c, arch(x, x + 24, 320, 360), (60, 70, 86))
    piece(c, RRect(220, 330, 330, 470, 1), (246, 240, 230), border=1.5, shadow=PROP)
    tile_roof(c, 220, 330, 330, 24)
    flat(c, RRect(220, 430, 330, 470, 0), (60, 56, 60))
    # pier
    piece(c, RRect(-10, 468, 910, 612, 0), (180, 160, 130), shadow=LAYER)
    for x in range(0, 900, 40):
        flat(c, Thick(x, 470, x, 612, 1.2), (160, 140, 110))
    for k, (x, y) in enumerate(((300, 590), (334, 590), (317, 560), (368, 590))):
        piece(c, RRect(x - 16, y - 30, x + 16, y, 2), (170, 120, 70), border=1.2, shadow=PROP)
        lab = ((60, 110, 180) if "label" in d else (220, 60, 50)) if k == 2 else (220, 60, 50)
        flat(c, RRect(x - 8, y - 22, x + 8, y - 10, 1), lab)
    for x in (430, 460):
        piece(c, Ell(x, 580, 16, 14), (236, 232, 214), border=1.2, shadow=PROP)
    westerner(c, 540, 596, (30, 40, 80), hat="kepi", hat_col=(240, 240, 240) if "cap" in d else (30, 40, 80), trousers=(30, 40, 80))
    westerner(c, 590, 596, (240, 240, 236), hat="kepi", hat_col=(30, 40, 80), trousers=(30, 40, 80))
    kimono(c, 650, 598, (90, 80, 70), hat=(200, 176, 120))
    rickshaw(c, 740, 598, hood=(160, 50, 50) if "rickshaw" in d else (40, 40, 50))
    kimono(c, 80, 598, (60, 60, 90), umbrella=(70, 70, 90))
    kimono(c, 140, 598, (150, 70, 90), hair="woman")


L87_ELEMENTS = [
    E("sun", lambda c, m: (piece(c, Poly(star_pts(500, 80, 38, 28, points=12)), (255, 190, 80), shadow=PROP),
                           piece(c, Circ(500, 80, 24), (255, 222, 95), border=2, shadow=PROP)), weather=SUNNY),
    cloud("cloudA", 300, 70, 0.9, (252, 252, 248), W_(CLEAR, OVERCAST), anim=dict(bobAmplitude=(26, 0), bobSpeed=0.02)),
    cloud("cloudB", 560, 60, 1.0, (200, 206, 216), CLOUDY, anim=dict(bobAmplitude=(-22, 0), bobSpeed=0.025)),
    cloud("cloudC", 820, 110, 0.8, (190, 196, 208), CLOUDY),
    rain_layer("rain", 87, 44, 24, 1.8, 0.55, 300),
] + smoke_el("smoke", 510, 314, n=4, col=(90, 90, 96), r=10, rise=(-20, 24), length=90) + [
    E("sailboat", lambda c, m: (piece(c, Poly([(780, 380), (850, 380), (840, 392), (790, 392)]), (240, 236, 226), border=1, shadow=SMALL),
                                flat(c, Thick(815, 380, 815, 320, 2), (110, 80, 60)),
                                piece(c, Poly([(817, 324), (817, 376), (850, 376)]), (240, 236, 226), shadow=SMALL)),
      pivot=(815, 392), anim=dict(drift_across(776, 854, -8), bobAmplitude=(0, 2), bobSpeed=0.3)),
    bird_el("gull0", 600, 150, 10, col=(246, 246, 246), speed=16, weather=SUNNY),
]

L87_DIFFS = [
    ("funnel", 510, 342, 0),
    ("flag", 705, 249, 0),
    ("fuji", 160, 166, 0),
    ("door", 155, 424, 0),
    ("label", 317, 544, 0),
    ("cap", 541, 546, 0),
    ("rickshaw", 730, 530, 0),
]


# =================================================================== Level 88 Tomioka silk mill in spring
WIN88 = [(x, 340, x + 22, 372) for x in range(60, 740, 40)]
WIN_DIFF = 9


def l88_bg(c, d):
    sky(c, (166, 206, 236), (246, 236, 220), 320)
    piece(c, Poly([(-20, 300), (60, 240), (90, 260), (130, 200), (170, 236), (210, 214), (260, 270), (340, 300)]), (130, 140, 170), shadow=LAYER)
    layer(c, 286, [(10, 0.012, 0.4)], (150, 180, 140))
    for x, col in ((330, (246, 196, 210)), (460, (246, 196, 210)), (860, (246, 196, 210))):
        blossom_tree(c, x, 314, 0.8, (250, 250, 250) if ("cherry" in d and x == 460) else col, 880 + x)
    # long brick hall
    piece(c, RRect(40, 320, 760, 420, 1), BRICK, border=1.5, shadow=PROP)
    for y in range(326, 420, 7):
        flat(c, Thick(40, y, 760, y, 0.6), lit(BRICK, 0.88))
    for x in range(40, 760, 40):
        flat(c, Thick(x, 320, x, 420, 3), (236, 230, 216))
    for i, r in enumerate(WIN88):
        flat(c, RRect(r[0] - 2, r[1] - 2, r[2] + 2, r[3] + 2, 1), (246, 240, 228))
        if i == WIN_DIFF and "window" in d:
            flat(c, RRect(*r, 0), (40, 40, 46))
        else:
            flat(c, RRect(*r, 0), (160, 190, 210))
            flat(c, [Thick((r[0] + r[2]) / 2, r[1], (r[0] + r[2]) / 2, r[3], 1.2), Thick(r[0], (r[1] + r[3]) / 2, r[2], (r[1] + r[3]) / 2, 1.2)],
                 (246, 240, 228))
    piece(c, Poly([(30, 322), (770, 322), (740, 290), (60, 290)]), TILE, border=1.5, shadow=SMALL)
    # chimney
    piece(c, Poly([(800, 420), (840, 420), (832, 150), (808, 150)]), BRICK, border=1.5, shadow=PROP)
    for y in range(160, 420, 8):
        flat(c, Thick(806, y, 834, y, 0.6), lit(BRICK, 0.88))
    flat(c, RRect(808, 180, 832, 192, 0), (60, 130, 200) if "chimney" in d else (246, 240, 228))
    # gate with a flag
    piece(c, [RRect(560, 380, 572, 444, 1), RRect(640, 380, 652, 444, 1), RRect(552, 372, 660, 382, 1)], (90, 80, 76), shadow=PROP)
    flat(c, Thick(606, 372, 606, 330, 2), (90, 80, 80))
    if "flag" in d:
        piece(c, RRect(607, 330, 637, 348, 1), (250, 250, 246), shadow=SMALL)
        flat(c, Circ(622, 339, 5), (210, 40, 50))
    else:
        piece(c, [RRect(607, 330, 617, 348, 0)], (40, 70, 160), shadow=SMALL)
        piece(c, [RRect(617, 330, 627, 348, 0)], (250, 250, 246), shadow=None)
        piece(c, [RRect(627, 330, 637, 348, 0)], (210, 40, 50), shadow=None)
    # mulberry fields
    piece(c, hill_strip(440, [(4, 0.01, 0.4)]), (150, 180, 100), shadow=LAYER)
    for row, y in enumerate((470, 510, 552, 596)):
        for x in range(-10 + row * 20, 920, 60):
            piece(c, [Circ(x - 10, y - 12, 12), Circ(x + 6, y - 18, 14), Circ(x + 18, y - 10, 11)], (80, 140, 70), shadow=PROP)
    # people
    for x, basket in ((200, "basket"), (290, None), (420, None)):
        kimono(c, x, 560, (90, 110, 160), hair="woman", hat=(220, 200, 150))
        if basket:
            piece(c, Ell(x + 18, 540, 13, 9), (150, 110, 160) if "basket" in d else (190, 150, 90), border=1.2, shadow=SMALL)
        else:
            piece(c, Ell(x + 18, 540, 13, 9), (190, 150, 90), border=1.2, shadow=SMALL)
    hx, hy = westerner(c, 520, 600, (90, 80, 70), hat="bowler", hat_col=(60, 110, 160) if "hat" in d else (40, 36, 34))
    flat(c, Ell(hx + 1, hy + 6, 6, 4), (120, 90, 60))
    kimono(c, 600, 600, (200, 60, 70) if "hakama" in d else (70, 60, 120), hair="woman")
    flat(c, Poly([(590, 600), (612, 600), (608, 578), (594, 578)]), (110, 50, 70))
    kimono(c, 660, 600, (220, 160, 80), hair="woman")


def l88_petal(i, x, y):
    def d(c, m):
        flat(c, Ell(x, y, 3.2, 2.2), (250, 200, 214))
    return E("petal%d" % i, d, pivot=(x, y), anim=dict(driftVelocity=(14, -22), driftLength=380, driftFade=True, rotateSpeed=90 + i * 13,
                                                       spinSpeed=0.6 + 0.07 * i, spinShade=0.3, phase=(i * 0.137) % 1))


L88_ELEMENTS = [
    cloud_el("cloud0", 300, 70, 0.7, 7), cloud_el("cloud1", 620, 50, 0.6, 6),
] + smoke_el("smoke", 820, 140, n=5, col=(200, 200, 206), r=11, rise=(-24, 24), length=110) + [
    bird_el("bird0", 500, 120, 8, speed=16), bird_el("bird1", 526, 110, 6, speed=16),
] + [l88_petal(i, x, y) for i, (x, y) in enumerate(((330, 250), (460, 240), (860, 260), (400, 280), (880, 300)))]

L88_DIFFS = [
    ("chimney", 820, 186, 0),
    ("window", WIN88[WIN_DIFF][0] + 11, 356, 0),
    ("flag", 622, 339, 0),
    ("cherry", 460, 250, 0),
    ("basket", 218, 540, 0),
    ("hat", 521, 552, 0),
    ("hakama", 600, 580, 0),
]

LEVELS = [
    ("Level84", "银座砖街", l84_bg, L84_ELEMENTS, L84_DIFFS, 140, dict(OPTS, day_night=DN84, anim_seconds=40.0, frames=80)),
    ("Level85", "新桥驿", l85_bg, L85_ELEMENTS, L85_DIFFS, 140, OPTS),
    ("Level86", "鹿鸣馆", l86_bg, L86_ELEMENTS, L86_DIFFS, 140, dict(OPTS, day_night=DN86, anim_seconds=40.0, frames=80)),
    ("Level87", "横滨港", l87_bg, L87_ELEMENTS, L87_DIFFS, 140, dict(OPTS, weather=WEATHER87, anim_seconds=27.0, frames=54)),
    ("Level88", "富冈制丝", l88_bg, L88_ELEMENTS, L88_DIFFS, 140, OPTS),
]
