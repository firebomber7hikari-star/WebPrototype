# -*- coding: utf-8 -*-
"""Europe 15th-19th century, paper-craft side views (same look as Level06/07), full-bleed:
  Level69 文艺复兴佛罗伦萨 (15th c.)  - Duomo, campanile, Palazzo Vecchio, Arno with the Ponte Vecchio, a painter on the bank
  Level70 威尼斯狂欢节   (16th c.)  - campanile, Doge's palace, gondolas, masked revellers; day/night with lanterns and fireworks
  Level71 荷兰黄金时代   (17th c.)  - windmills, tulip fields, stepped-gable canal houses; clear -> overcast -> rain
  Level72 凡尔赛花园     (18th c.)  - palace front, topiary parterre, Apollo fountain, rococo courtiers, a Montgolfier balloon
  Level73 维多利亚伦敦   (19th c.)  - Big Ben, Tower Bridge, paddle steamer, gas lamps, hansom cab; day/night + fog and rain
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts, wave_strip
from kit import (INK, LAYER, PROP, SMALL, barrel, bird_el, bush, cloud_bg, cloud_el, crate, drift_across, gy, layer, person, sky,
                 smoke_el, sun_bg, tree_round)
from stylekit import day_night, star_field, window_glow
from weather import CLOUDY, SUNNY, WET, cloud, fog_layer, rain_layer

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def ellipse_top(cx, base, rx, ry, n=18):
    return Poly([(cx + rx * math.cos(math.pi * k / n), base - ry * math.sin(math.pi * k / n)) for k in range(n + 1)])


def arch(x0, x1, top, bottom):
    """Round-headed window / arch shape."""
    r = (x1 - x0) / 2
    return [RRect(x0, top + r, x1, bottom, 0), Circ((x0 + x1) / 2, top + r, r)]


def cypress(c, x, base, h, col=(52, 92, 62)):
    piece(c, [Ell(x, base - h * 0.48, h * 0.11, h * 0.5), Thick(x, base, x, base - h * 0.1, 3)], col, shadow=SMALL)
    flat(c, Ell(x - h * 0.03, base - h * 0.6, h * 0.04, h * 0.28), lit(col, 1.18))


def flag_el(eid, x, y, col, col2=None, w=26, h=16, **kw):
    def d(c, m):
        flat(c, Thick(x, y, x, y + h * 2.2, 2), (90, 80, 80))
        piece(c, Poly([(x + 1, y), (x + w, y + h * 0.15), (x + w, y + h * 0.85), (x + 1, y + h)]), col, shadow=SMALL)
        if col2:
            flat(c, Poly([(x + 1, y + h * 0.35), (x + w, y + h * 0.42), (x + w, y + h * 0.62), (x + 1, y + h * 0.65)]), col2)
    return E(eid, d, pivot=(x, y + h / 2), anim=dict(stretch=(0.18, 0.05), scaleSpeed=1.4, swingAngle=3, swingSpeed=0.9), **kw)


def hat_cap(c, hx, hy, h, col):
    """Renaissance soft cap."""
    flat(c, [Ell(hx, hy - 5 * h, 10 * h, 5 * h), RRect(hx - 8 * h, hy - 6 * h, hx + 8 * h, hy - 2 * h, 2)], col)


def tricorne(c, hx, hy, h, col):
    flat(c, Poly([(hx - 12 * h, hy - 4 * h), (hx + 12 * h, hy - 4 * h), (hx + 7 * h, hy - 12 * h), (hx, hy - 9 * h), (hx - 7 * h, hy - 12 * h)]),
         col)


def top_hat(c, hx, hy, h, col, band):
    flat(c, [RRect(hx - 11 * h, hy - 7 * h, hx + 11 * h, hy - 4 * h, 1), RRect(hx - 7 * h, hy - 22 * h, hx + 7 * h, hy - 6 * h, 1)], col)
    flat(c, RRect(hx - 7 * h, hy - 10 * h, hx + 7 * h, hy - 7 * h, 0), band)


def lady(c, x, base, dress, hair=(90, 60, 40), h=1.0, wide=1.0):
    """Long-dress figure (wide = panier width)."""
    piece(c, [Poly([(x - 18 * h * wide, base), (x + 18 * h * wide, base), (x + 7 * h, base - 30 * h), (x - 7 * h, base - 30 * h)]),
              RRect(x - 6 * h, base - 42 * h, x + 6 * h, base - 28 * h, 3), Circ(x + 1 * h, base - 49 * h, 7.5 * h)], dress, border=1.5,
          shadow=PROP)
    flat(c, Circ(x + 1 * h, base - 49 * h, 6.2 * h), (250, 214, 185))
    flat(c, Ell(x + 1 * h, base - 55 * h, 7 * h, 4 * h), hair)
    flat(c, Circ(x + 4 * h, base - 50 * h, 1.1 * h), INK)
    return x + 1 * h, base - 49 * h


# =================================================================== Level 69 Renaissance Florence
HILLS69 = [(18, 0.008, 0.3), (8, 0.025, 1.0)]
SHOPS69 = list(range(486, 900, 34))
SHOP_DIFF = 4
TERRA = (204, 104, 70)
OCHRES = [(232, 204, 150), (238, 216, 170), (222, 180, 130), (240, 226, 196), (214, 170, 120)]


def l69_houses(c, base, x0, x1, seed, hmin, hmax, wmin=40, wmax=66):
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w, h = rnd.randint(wmin, wmax), rnd.randint(hmin, hmax)
        wall = rnd.choice(OCHRES)
        piece(c, RRect(x, base - h, x + w, base, 1), wall, border=1.5, shadow=PROP)
        piece(c, Poly([(x - 4, base - h + 2), (x + w + 4, base - h + 2), (x + w * 0.5, base - h - w * 0.22)]), TERRA, border=1.5, shadow=SMALL)
        for k in range(int(h // 22)):
            for wx in range(int(x + 8), int(x + w - 10), 16):
                flat(c, [RRect(wx, base - h + 10 + k * 22, wx + 7, base - h + 20 + k * 22, 1)], (110, 80, 60))
        x += w + rnd.randint(-4, 2)


def l69_bg(c, d):
    sky(c, (140, 190, 236), (252, 230, 196), 420)
    sun_bg(c, 800, 70, 28)
    layer(c, 228, HILLS69, (190, 204, 162))
    for x in range(10, 900, 38):
        b = gy(228, HILLS69, x) + 8
        if x % 152 == 48:
            piece(c, [RRect(x - 12, b - 14, x + 12, b, 1)], (240, 228, 200), shadow=SMALL)
            flat(c, Poly([(x - 14, b - 13), (x + 14, b - 13), (x, b - 20)]), TERRA)
        else:
            cypress(c, x, b, 34 + (x * 7) % 18, (84, 120, 84))
    layer(c, 268, [(12, 0.01, 1.2), (5, 0.03, 0.4)], (164, 186, 130))
    l69_houses(c, 330, -10, 200, 691, 30, 56)
    l69_houses(c, 330, 720, 910, 692, 30, 56)
    # Duomo: nave, drum, dome, lantern (+ golden ball and cross in A)
    piece(c, RRect(190, 282, 470, 362, 1), (238, 228, 206), border=2, shadow=PROP)
    for x in range(200, 470, 22):
        flat(c, Thick(x, 286, x, 360, 2), (110, 150, 120))
    flat(c, [Thick(190, 300, 470, 300, 3), Thick(190, 330, 470, 330, 2)], (200, 130, 130))
    piece(c, RRect(270, 232, 390, 292, 1), (238, 228, 206), border=2, shadow=PROP)
    for x in (292, 330, 368):
        flat(c, Circ(x, 262, 7), (90, 80, 80))
    piece(c, ellipse_top(330, 236, 68, 84), (204, 94, 62), border=2, shadow=PROP)
    for xb in (276, 303, 357, 384):
        flat(c, Thick(330, 154, xb, 236, 2.5), (246, 236, 220))
    piece(c, RRect(320, 134, 340, 156, 2), (246, 240, 228), border=1.5, shadow=SMALL)
    piece(c, Poly([(317, 136), (343, 136), (330, 114)]), (214, 206, 190), border=1.5, shadow=SMALL)
    if "lantern" not in d:
        piece(c, Circ(330, 108, 6), (236, 192, 70), border=1.2, shadow=SMALL)
        flat(c, [Thick(330, 102, 330, 88, 2), Thick(324, 94, 336, 94, 2)], (236, 192, 70))
    # Giotto's campanile with coloured marble bands
    piece(c, RRect(472, 150, 506, 395, 1), (242, 234, 216), border=2, shadow=PROP)
    for k, y in enumerate(range(168, 384, 30)):
        col = ((120, 160, 220) if "campanile" in d else (222, 150, 150)) if k == 2 else [(222, 150, 150), (120, 160, 120)][k % 2]
        flat(c, RRect(474, y, 504, y + 10, 0), col)
    for x in range(468, 512, 8):
        piece(c, RRect(x, 138, x + 5, 150, 0), (242, 234, 216), shadow=None)
    # Palazzo Vecchio
    piece(c, RRect(560, 242, 730, 398, 1), (216, 182, 132), border=2, shadow=PROP)
    for x in range(556, 734, 14):
        piece(c, RRect(x, 232, x + 8, 244, 0), (216, 182, 132), shadow=None)
    for y in (270, 320):
        for x in range(578, 720, 28):
            flat(c, arch(x, x + 12, y, y + 24), (100, 80, 66))
    piece(c, RRect(628, 122, 662, 244, 1), (216, 182, 132), border=2, shadow=PROP)
    for x in range(624, 668, 9):
        piece(c, RRect(x, 112, x + 6, 124, 0), (216, 182, 132), shadow=None)
    piece(c, RRect(634, 80, 656, 112, 1), (216, 182, 132), border=1.5, shadow=SMALL)
    flat(c, arch(640, 650, 86, 104), (90, 70, 60))
    piece(c, Poly([(630, 82), (660, 82), (645, 62)]), (150, 100, 70), border=1.5, shadow=SMALL)
    piece(c, Circ(645, 172, 12), (246, 240, 224), border=1.5, shadow=SMALL)
    if "clock" in d:
        flat(c, [Thick(645, 172, 637, 172, 2.4), Thick(645, 172, 645, 182, 1.8)], INK)
    else:
        flat(c, [Thick(645, 172, 653, 172, 2.4), Thick(645, 172, 645, 162, 1.8)], INK)
    l69_houses(c, 402, -10, 470, 693, 40, 70, 44, 70)
    # Arno
    c.rect(0, 398, W, 480, (98, 158, 188))
    for y in range(410, 478, 14):
        for x in range((y * 13) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (130, 186, 210))
    # Ponte Vecchio with its shops (one shutter differs)
    piece(c, RRect(468, 392, 910, 412, 1), (214, 178, 128), border=2, shadow=PROP)
    for cx in (560, 700, 840):
        piece(c, [RRect(cx - 70, 410, cx - 52, 470, 0), RRect(cx + 52, 410, cx + 70, 470, 0)], (204, 168, 120), shadow=SMALL)
        flat(c, Ell(cx, 412, 52, 34), (80, 130, 160))
    for i, x in enumerate(SHOPS69):
        wall = OCHRES[i % len(OCHRES)]
        piece(c, RRect(x, 356, x + 32, 392, 1), wall, border=1.2, shadow=SMALL)
        piece(c, Poly([(x - 2, 358), (x + 34, 358), (x + 16, 348)]), TERRA, shadow=None)
        sh = ((200, 60, 60) if "shutter" in d else (90, 130, 80)) if i == SHOP_DIFF else (90, 130, 80) if i % 2 else (140, 96, 64)
        flat(c, [RRect(x + 6, 364, x + 14, 380, 1), RRect(x + 18, 364, x + 26, 380, 1)], sh)
    # embankment
    piece(c, RRect(-10, 470, 910, 612, 0), (206, 188, 152), shadow=LAYER)
    flat(c, RRect(-10, 470, 910, 480, 0), (226, 210, 178))
    for y in (510, 550, 590):
        flat(c, Thick(0, y, 900, y, 1.5), (188, 168, 134))
    # painter at the easel (portrait in A, the same portrait with a moustache in B)
    person(c, 112, 578, (120, 40, 60))
    hat_cap(c, 113, 538, 1.0, (40, 40, 70))
    flat(c, [Thick(166, 578, 182, 520, 3), Thick(214, 578, 198, 520, 3), Thick(190, 578, 190, 530, 3)], (130, 90, 60))
    piece(c, RRect(156, 464, 224, 532, 2), (246, 240, 226), border=2, shadow=PROP)
    flat(c, RRect(162, 470, 218, 526, 1), (120, 150, 120))
    flat(c, [Ell(190, 520, 20, 12), Ell(190, 494, 12, 15)], (110, 60, 50))
    flat(c, Ell(190, 496, 9, 12), (236, 200, 170))
    flat(c, [Circ(186, 494, 1.4), Circ(194, 494, 1.4)], INK)
    if "canvas" in d:
        flat(c, [Thick(184, 502, 190, 500, 2), Thick(190, 500, 196, 502, 2)], INK)
    else:
        flat(c, Thick(187, 503, 193, 503, 1.2), (160, 80, 70))
    # fruit cart
    for wx in (660, 750):
        piece(c, Circ(wx, 560, 16), (120, 84, 60), border=1.5, shadow=PROP)
        flat(c, Circ(wx, 560, 5), (80, 60, 50))
    piece(c, RRect(636, 516, 776, 548, 2), (170, 120, 80), border=1.5, shadow=PROP)
    fruits = [(658, (240, 150, 40)), (700, (120, 60, 130)), (742, (150, 200, 80) if "fruit" in d else (250, 220, 60))]
    for x, col in fruits:
        for k in range(6):
            piece(c, Circ(x - 12 + (k % 3) * 12, 512 - (k // 3) * 9, 6), col, shadow=None)
    # townsfolk
    hx, hy = person(c, 400, 580, (40, 70, 140))
    hat_cap(c, hx, hy, 1.0, (40, 120, 60) if "hat" in d else (160, 30, 44))
    lady(c, 440, 582, (150, 40, 60))
    hx, hy = person(c, 560, 584, (90, 110, 60))
    hat_cap(c, hx, hy, 1.0, (60, 50, 50))
    lady(c, 832, 588, (110, 80, 150), hair=(170, 110, 60))
    cypress(c, 18, 612, 230)
    cypress(c, 884, 612, 210)
    bush(c, 300, 600, 1.4, (90, 140, 80))


BOAT69 = (260, 440)


def l69_boat(c, m):
    x, y = BOAT69
    piece(c, Poly([(x - 40, y), (x + 40, y), (x + 30, y + 12), (x - 30, y + 12)]), (130, 84, 56), border=1.5, shadow=SMALL)
    person(c, x, y + 2, (200, 80, 60), h=0.7)
    flat(c, Thick(x - 30, y - 20, x + 22, y + 14, 2), (110, 80, 60))


def l69_pigeon(x, y):
    def d(c, m):
        piece(c, [Ell(x, y, 8, 5), Circ(x + 7, y - 4, 3.5)], (150, 150, 165), shadow=SMALL)
        flat(c, Poly([(x + 10, y - 4), (x + 14, y - 3), (x + 10, y - 2)]), (230, 170, 60))
    return d


L69_ELEMENTS = [
    cloud_el("cloud0", 120, 46, 0.6, 9), cloud_el("cloud1", 520, 34, 0.7, 7),
    flag_el("flag", 645, 40, (230, 230, 230), (200, 40, 50)),
    E("boat", l69_boat, pivot=(BOAT69[0], BOAT69[1] + 12),
      anim=dict(drift_across(BOAT69[0] - 42, BOAT69[0] + 42, 14), bobAmplitude=(0, 2), bobSpeed=0.4)),
    bird_el("bird0", 400, 70, 9, speed=18), bird_el("bird1", 430, 84, 7, speed=18),
] + [E("pigeon%d" % i, l69_pigeon(x, y), pivot=(x, y + 4), anim=dict(swingAngle=14, swingSpeed=0.9 + i * 0.2, phase=i * 0.3))
     for i, (x, y) in enumerate(((300, 590), (330, 596), (600, 596)))]


L69_DIFFS = [
    ("lantern", 330, 100, 0),
    ("campanile", 489, 233, 0),
    ("clock", 645, 172, 0),
    ("shutter", SHOPS69[SHOP_DIFF] + 16, 372, 0),
    ("canvas", 190, 500, 0),
    ("fruit", 742, 508, 0),
    ("hat", 401, 534, 0),
]


# =================================================================== Level 70 Venice carnival (16th c.), day / night
DN70 = day_night(40.0, tint=(0.34, 0.32, 0.62))
LANT70 = []
for _k in range(1, 10):
    _t = _k / 10
    LANT70.append((236 + 524 * _t, 130 + 40 * _t + 40 * math.sin(math.pi * _t)))
LANT_DIFF = 6
GONDOLA = (470, 446)
WIN70 = [(x + 6, y + 18, x + 34, y + 56) for y in (128, 208) for x in (24, 96, 168)] + \
        [(x + 4, y, x + 22, y + 30) for y in (190, 270, 350) for x in (780, 830, 880)]


def masked(c, x, base, body, mask, hat, plume=False, lady_=False, dress=None):
    if lady_:
        hx, hy = lady(c, x, base, dress)
    else:
        hx, hy = person(c, x, base, body)
    flat(c, Poly([(hx - 7, hy - 3), (hx + 8, hy - 3), (hx + 7, hy + 2), (hx + 1, hy + 1), (hx - 6, hy + 2)]), mask)
    flat(c, [Circ(hx - 2, hy - 1, 1.4), Circ(hx + 4, hy - 1, 1.4)], INK)
    if hat:
        tricorne(c, hx, hy, 1.0, hat)
    if plume:
        flat(c, [Thick(hx - 4, hy - 10, hx - 10, hy - 22, 3), Thick(hx - 10, hy - 22, hx - 6, hy - 30, 2.5)], (250, 250, 250))
        flat(c, Thick(hx - 2, hy - 10, hx + 2, hy - 24, 2), (230, 80, 120))
    return hx, hy


def l70_bg(c, d):
    sky(c, (110, 170, 230), (252, 214, 190), 360)
    # basilica domes
    piece(c, RRect(650, 252, 830, 334, 1), (228, 212, 192), border=2, shadow=PROP)
    for x in (680, 740, 800):
        piece(c, ellipse_top(x, 254, 24, 30), (170, 182, 190), border=1.5, shadow=SMALL)
        piece(c, RRect(x - 3, 214, x + 3, 226, 1), (220, 190, 90), shadow=None)
    for x in range(662, 824, 30):
        flat(c, arch(x, x + 18, 286, 334), (200, 168, 110))
    # Doge's palace
    piece(c, RRect(300, 226, 600, 334, 1), (238, 196, 186), border=2, shadow=PROP)
    for y in range(236, 296, 12):
        for x in range(306 + (y // 12 % 2) * 8, 596, 16):
            flat(c, Poly([(x, y - 4), (x + 4, y), (x, y + 4), (x - 4, y)]), (226, 178, 170))
    for x in range(316, 590, 34):
        flat(c, arch(x, x + 14, 244, 272), (110, 90, 90))
    for x in range(306, 596, 22):
        flat(c, arch(x, x + 16, 300, 334), (120, 100, 96))
    for x in range(300, 600, 12):
        piece(c, Poly([(x, 228), (x + 6, 216), (x + 12, 228)]), (250, 244, 236), shadow=None)
    # St Mark's campanile with the golden angel (A)
    piece(c, RRect(585, 108, 617, 334, 1), (196, 112, 90), border=2, shadow=PROP)
    for x in (593, 601, 609):
        flat(c, Thick(x, 112, x, 330, 1.5), (176, 98, 80))
    piece(c, RRect(582, 88, 620, 110, 1), (236, 226, 206), border=1.5, shadow=SMALL)
    for x in (586, 597, 608):
        flat(c, arch(x, x + 8, 92, 108), (90, 80, 80))
    piece(c, Poly([(579, 90), (623, 90), (601, 46)]), (110, 160, 130), border=1.5, shadow=SMALL)
    if "angel" not in d:
        piece(c, [Poly([(597, 46), (605, 46), (603, 32), (599, 32)]), Circ(601, 29, 3.2), Poly([(599, 36), (588, 30), (598, 40)]),
                  Poly([(603, 36), (614, 30), (604, 40)])], (232, 190, 70), border=1, shadow=SMALL)
    # lagoon
    c.rect(0, 334, W, 480, (64, 132, 164))
    for y in range(344, 478, 12):
        for x in range((y * 11) % 64, 900, 64):
            flat(c, Thick(x, y, x + 24, y, 2), (98, 162, 190))
    # palazzi
    piece(c, RRect(-10, 96, 236, 480, 1), (226, 150, 120), border=2, shadow=PROP)
    for y in (128, 208, 306):
        for x in (24, 96, 168):
            flat(c, [RRect(x + 3, y + 16, x + 37, y + 60, 1), Poly([(x + 3, y + 18), (x + 37, y + 18), (x + 20, y + 2)])], (246, 236, 220))
            flat(c, [RRect(x + 6, y + 18, x + 34, y + 56, 1), Poly([(x + 6, y + 20), (x + 34, y + 20), (x + 20, y + 6)])], (60, 52, 66))
    piece(c, RRect(66, 266, 186, 274, 1), (246, 240, 228), border=1.2, shadow=SMALL)
    for x in range(70, 186, 12):
        flat(c, RRect(x, 274, x + 5, 290, 1), (246, 240, 228))
    flat(c, RRect(66, 288, 186, 292, 0), (246, 240, 228))
    if "flowers" not in d:
        for x in range(72, 184, 9):
            piece(c, Circ(x, 260 - (x % 2) * 3, 5), (220, 50, 60) if x % 18 else (250, 140, 160), shadow=None)
            flat(c, Ell(x + 3, 265, 4, 2), (70, 140, 70))
    flat(c, arch(90, 146, 400, 480), (40, 40, 52))
    piece(c, RRect(760, 150, 910, 480, 1), (244, 222, 170), border=2, shadow=PROP)
    for y in (190, 270, 350):
        for x in (780, 830, 880):
            flat(c, arch(x, x + 26, y - 4, y + 34), (246, 240, 228))
            flat(c, arch(x + 4, x + 22, y, y + 30), (70, 60, 70))
    # mooring poles
    for i, x in enumerate((292, 318, 560)):
        stripe = ((60, 160, 90) if "pole" in d else (60, 120, 200)) if i == 1 else (200, 50, 60)
        piece(c, RRect(x - 5, 350, x + 5, 480, 2), (246, 242, 234), border=1.2, shadow=SMALL)
        for y in range(358, 472, 16):
            flat(c, Poly([(x - 5, y), (x + 5, y - 6), (x + 5, y + 2), (x - 5, y + 8)]), stripe)
        piece(c, Circ(x, 348, 6), (220, 186, 80), shadow=None)
    # lantern string
    pts = [(236 + 524 * t / 40, 130 + 40 * t / 40 + 40 * math.sin(math.pi * t / 40)) for t in range(41)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.5) for i in range(40)], (70, 60, 60))
    for k, (x, y) in enumerate(LANT70):
        col = ((70, 170, 90) if "lantern" in d else (220, 60, 50)) if k == LANT_DIFF else [(220, 60, 50), (240, 190, 60)][k % 2]
        flat(c, Thick(x, y, x, y + 6, 1.2), (70, 60, 60))
        piece(c, RRect(x - 6, y + 6, x + 6, y + 22, 4), col, border=1.2, shadow=SMALL)
        flat(c, [RRect(x - 4, y + 4, x + 4, y + 7, 1), RRect(x - 4, y + 21, x + 4, y + 24, 1)], (60, 50, 50))
    # quay and revellers
    piece(c, RRect(-10, 478, 910, 612, 0), (204, 188, 164), shadow=LAYER)
    flat(c, RRect(-10, 478, 910, 488, 0), (226, 214, 190))
    for x in range(0, 900, 60):
        flat(c, Thick(x, 488, x - 20, 600, 1.4), (186, 170, 146))
    masked(c, 170, 580, (130, 30, 60), (230, 190, 80), (40, 30, 50), plume="plume" not in d)
    masked(c, 252, 584, (40, 60, 130), (40, 40, 50) if "mask" in d else (246, 242, 236), (150, 30, 40))
    masked(c, 660, 584, None, (200, 60, 90), None, plume=True, lady_=True, dress=(90, 140, 120))
    piece(c, Poly([(722, 588), (758, 588), (748, 540), (732, 540)]), (30, 28, 34), border=1.5, shadow=PROP)
    masked(c, 740, 548, (30, 28, 34), (246, 242, 236), (30, 28, 34))
    hx, hy = person(c, 840, 588, (160, 120, 40))
    tricorne(c, hx, hy, 1.0, (90, 40, 40))
    piece(c, [Ell(824, 560, 12, 9), Thick(824, 556, 846, 534, 3)], (180, 130, 70), border=1.2, shadow=SMALL)
    for x in (40, 420, 520):
        piece(c, RRect(x - 14, 574, x + 14, 600, 3), (190, 110, 80), border=1.2, shadow=PROP)
        piece(c, [Circ(x - 8, 568, 8), Circ(x + 6, 566, 9), Circ(x, 560, 8)], (80, 150, 80), shadow=SMALL)
        flat(c, [Circ(x - 6, 564, 3), Circ(x + 5, 560, 3)], (230, 70, 90))


def gondola(x, y, k, cushion_a, cushion_b=None):
    def d(c, m):
        cush = cushion_b if (m and cushion_b) else cushion_a
        piece(c, Poly([(x - 92 * k, y - 18 * k), (x - 80 * k, y - 2 * k), (x - 40 * k, y + 6 * k), (x + 40 * k, y + 6 * k), (x + 82 * k, y - 4 * k),
                       (x + 98 * k, y - 28 * k), (x + 88 * k, y - 10 * k), (x + 40 * k, y - 4 * k), (x - 40 * k, y - 4 * k), (x - 84 * k, y - 8 * k)]),
              (30, 30, 36), border=1.5, shadow=SMALL)
        flat(c, [Poly([(x + 92 * k, y - 22 * k), (x + 104 * k, y - 34 * k), (x + 100 * k, y - 20 * k)])] +
             [Thick(x + 94 * k, y - 22 * k + i * 3 * k, x + 102 * k, y - 22 * k + i * 3 * k, 1.2 * k) for i in range(4)], (220, 220, 226))
        piece(c, RRect(x - 22 * k, y - 18 * k, x + 22 * k, y - 4 * k, 3 * k), cush, border=1.2, shadow=None)
        hx, hy = person(c, x - 62 * k, y - 4 * k, (246, 246, 246), h=k)
        for i in range(3):
            flat(c, Thick(x - 70 * k, y - 26 * k + i * 7 * k, x - 54 * k, y - 26 * k + i * 7 * k, 2 * k), (200, 40, 50))
        flat(c, [Ell(hx, hy - 6 * k, 11 * k, 3 * k), RRect(hx - 6 * k, hy - 11 * k, hx + 6 * k, hy - 6 * k, 1)], (236, 206, 120))
        flat(c, Thick(x - 48 * k, y - 46 * k, x - 76 * k, y + 10 * k, 2.4 * k), (130, 90, 60))
    return d


def firework(x, y, col, r=36):
    def d(c, m):
        for k in range(14):
            a = 2 * math.pi * k / 14
            flat(c, Thick(x + r * 0.3 * math.cos(a), y + r * 0.3 * math.sin(a), x + r * math.cos(a), y + r * math.sin(a), 2.2), col)
            flat(c, Circ(x + r * 1.08 * math.cos(a), y + r * 1.08 * math.sin(a), 2.4), (255, 250, 220))
        soft_union(c, [Circ(x, y, r * 0.5)], col, 0.4, spread=r * 0.6)
    return d


def lantern_glow(c, m):
    soft_union(c, [Circ(x, y + 14, 8) for x, y in LANT70], (255, 200, 110), 0.5, spread=16)


def l70_sun(c, m):
    piece(c, Poly(star_pts(420, 70, 40, 30, points=12)), (255, 190, 80), shadow=PROP)
    piece(c, Circ(420, 70, 26), (255, 222, 95), border=2, shadow=PROP)


def l70_moon(c, m):
    soft_union(c, [Circ(420, 70, 28)], (255, 250, 220), 0.35, spread=16)
    piece(c, Circ(420, 70, 22), (252, 246, 220), border=2, shadow=PROP)
    flat(c, [Circ(414, 64, 5), Circ(428, 76, 3.5)], (232, 224, 196))


L70_ELEMENTS = [
    E("sun", l70_sun, daynight="day", anim=dict(pulse=0.03, scaleSpeed=0.3)),
    E("moon", l70_moon, daynight="night"),
    star_field("stars", 70, 40, 200, avoid=[(560, 20, 640, 130), (380, 30, 460, 110)]),
    cloud_el("cloud0", 300, 40, 0.6, 8, daynight="day"),
    bird_el("gull0", 500, 120, 10, col=(246, 246, 246), speed=16, daynight="day"),
    bird_el("gull1", 530, 106, 8, col=(246, 246, 246), speed=16, daynight="day"),
    E("gondola_far", gondola(380, 372, 0.55, (180, 40, 50)), pivot=(380, 376), anim=dict(drift_across(320, 440, -12), bobAmplitude=(0, 1.5),
                                                                                          bobSpeed=0.3)),
    E("gondola", gondola(*GONDOLA, 1.0, (180, 40, 50), (50, 80, 170)), pivot=(GONDOLA[0], GONDOLA[1] + 4), variant=True,
      anim=dict(bobAmplitude=(0, 2), bobSpeed=0.3, swingAngle=1.2, swingSpeed=0.25)),
    E("lantern_glow", lantern_glow, daynight="night", anim=dict(twinkle=0.12, twinkleSpeed=0.8)),
    window_glow("windows", WIN70),
] + [E("firework%d" % i, firework(x, y, col), pivot=(x, y), daynight="night",
       anim=dict(blinkInterval=3.2, blinkDuration=1.2, phase=i * 0.33, pulse=0.15, scaleSpeed=0.8))
     for i, (x, y, col) in enumerate(((300, 70, (255, 120, 140)), (500, 56, (140, 220, 255)), (740, 90, (255, 220, 110))))]

L70_DIFFS = [
    ("angel", 601, 36, 0),
    ("flowers", 126, 258, 0),
    ("pole", 318, 410, 0),
    ("lantern", int(LANT70[LANT_DIFF][0]), int(LANT70[LANT_DIFF][1] + 14), 0),
    ("mask", 253, 541, 0),
    ("plume", 160, 520, 0),
    ("cushion", GONDOLA[0], GONDOLA[1] - 11, 0),
]


# =================================================================== Level 71 Dutch Golden Age (17th c.), weather
STEPS71 = [(CLEAR, 8), (OVERCAST, 5), (RAIN, 8), (OVERCAST, 5)]
WEATHER71 = dict(steps=STEPS71, blend=3.0, tints={OVERCAST: (0.86, 0.88, 0.92), RAIN: (0.74, 0.78, 0.86)})
BANDS71 = [(302, 308), (308, 316), (316, 326), (326, 338), (338, 352), (352, 368), (368, 386), (386, 406), (406, 428)]
GREEN71 = (110, 170, 90)
BAND_COLS = [(230, 60, 70), GREEN71, (250, 210, 60), GREEN71, (240, 140, 170), GREEN71, (250, 246, 236), GREEN71, (150, 90, 170)]
HOUSES71 = [(0, 80, (170, 80, 60), "step", 170), (80, 72, (60, 90, 80), "step", 150), (152, 84, (232, 220, 190), "diff", 182),
            (236, 80, (150, 60, 50), "neck", 160)]
MILL71 = (640, 266)
MILL71_SMALL = (830, 344)
BARGE = (420, 474)


def gable_pts(x0, x1, top, kind):
    w = x1 - x0
    cx = (x0 + x1) / 2
    if kind == "step":
        pts = [(x0, top)]
        for k in range(4):
            xl = x0 + (k + 1) * w * 0.1
            pts += [(x0 + k * w * 0.1, top - (k + 1) * 14), (xl, top - (k + 1) * 14)]
        pts += [(cx - w * 0.1, top - 66), (cx + w * 0.1, top - 66)]
        for k in range(3, -1, -1):
            pts += [(x1 - (k + 1) * w * 0.1, top - (k + 1) * 14), (x1 - k * w * 0.1, top - (k + 1) * 14)]
        pts.append((x1, top))
        return pts
    if kind == "bell":
        return [(x0, top), (x0 + w * 0.06, top - 20), (x0 + w * 0.2, top - 30), (x0 + w * 0.26, top - 44), (x0 + w * 0.24, top - 60),
                (cx - w * 0.12, top - 72), (cx, top - 76), (cx + w * 0.12, top - 72), (x1 - w * 0.24, top - 60), (x1 - w * 0.26, top - 44),
                (x1 - w * 0.2, top - 30), (x1 - w * 0.06, top - 20), (x1, top)]
    return [(x0, top), (x0 + w * 0.2, top - 20), (x0 + w * 0.28, top - 22), (x0 + w * 0.28, top - 70), (cx, top - 82), (x1 - w * 0.28, top - 70),
            (x1 - w * 0.28, top - 22), (x1 - w * 0.2, top - 20), (x1, top)]


def cow(c, x, base, body, spots, flip=False):
    s = -1 if flip else 1
    for lx in (-18, -8, 10, 20):
        flat(c, RRect(x + lx * s - 2.5, base - 20, x + lx * s + 2.5, base, 1), lit(body, 0.8))
    piece(c, [Ell(x, base - 30, 30, 15), Ell(x + 34 * s, base - 38, 10, 8)], body, border=1.5, shadow=PROP)
    flat(c, Ell(x + 40 * s, base - 34, 6, 4), (240, 190, 180))
    flat(c, [Poly([(x + 30 * s, base - 46), (x + 26 * s, base - 54), (x + 34 * s, base - 47)])], (230, 220, 200))
    flat(c, Circ(x + 34 * s, base - 40, 1.4), INK)
    flat(c, [Ell(x + dx * s, base - 30 + dy, rx, ry) for dx, dy, rx, ry in spots], INK if body[0] > 200 else (246, 242, 232))
    flat(c, Thick(x - 30 * s, base - 34, x - 36 * s, base - 14, 2), lit(body, 0.8))


def l71_bg(c, d):
    sky(c, (150, 200, 240), (234, 240, 246), 320)
    c.rect(0, 294, W, 304, (150, 180, 140))
    for x, s in ((90, 0.9), (200, 0.72), (760, 0.84)):
        piece(c, Poly([(x - 14 * s, 300), (x + 14 * s, 300), (x + 8 * s, 300 - 60 * s), (x - 8 * s, 300 - 60 * s)]), (150, 160, 170), shadow=None)
        for a in (0.4, 2.0):
            flat(c, Thick(x - 50 * s * math.cos(a), 300 - 64 * s + 50 * s * math.sin(a), x + 50 * s * math.cos(a), 300 - 64 * s - 50 * s * math.sin(a),
                          2), (150, 160, 170))
    piece(c, [RRect(500, 262, 520, 300, 0), Poly([(498, 264), (522, 264), (510, 226)])], (160, 166, 176), shadow=None)
    # tulip fields (one patch changes colour)
    for i, (y0, y1) in enumerate(BANDS71):
        col = BAND_COLS[i]
        flat(c, RRect(-10, y0, 910, y1 + 0.5, 0), col)
        if i == 6 and "tulips" in d:
            flat(c, RRect(604, y0, 910, y1 + 0.5, 0), (250, 150, 60))
        if col != GREEN71 and y1 - y0 >= 10:
            for x in range(4 + i * 3, 900, 9):
                fc = (250, 150, 60) if (i == 6 and "tulips" in d and x > 604) else col
                flat(c, Circ(x, y0 + 3, (y1 - y0) * 0.16), lit(fc, 1.1))
    for x in (300, 600):
        flat(c, Poly([(x - 1, 302), (x + 1, 302), (x + 4, 428), (x - 4, 428)]), (120, 170, 200))
    # canal houses
    for i, (x0, w, wall, kind, h) in enumerate(HOUSES71):
        top = 440 - h
        if kind == "diff":
            kind = "bell" if "gable" in d else "step"
        piece(c, [RRect(x0, top, x0 + w, 440, 0), Poly(gable_pts(x0, x0 + w, top + 1, kind))], wall, border=2, shadow=PROP)
        flat(c, Thick(x0 + w / 2, top - 48, x0 + w / 2, top - 38, 3), (90, 70, 60))
        for row in range(int((h - 50) // 40)):
            for wx in (x0 + 12, x0 + w - 32):
                y = top + 12 + row * 40
                flat(c, RRect(wx, y, wx + 20, y + 28, 1), (246, 244, 236))
                flat(c, [RRect(wx + 3, y + 3, wx + 9, y + 13, 0), RRect(wx + 11, y + 3, wx + 17, y + 13, 0), RRect(wx + 3, y + 15, wx + 9, y + 25, 0),
                         RRect(wx + 11, y + 15, wx + 17, y + 25, 0)], (90, 110, 130))
        flat(c, RRect(x0 + w / 2 - 9, 410, x0 + w / 2 + 9, 440, 2), (70, 50, 40))
    # dike + canal
    piece(c, RRect(-10, 426, 910, 444, 0), (120, 166, 92), shadow=LAYER)
    c.rect(0, 442, W, 490, (100, 150, 180))
    for y in range(452, 488, 12):
        for x in range((y * 7) % 60, 900, 60):
            flat(c, Thick(x, y, x + 22, y, 2), (130, 176, 204))
    # windmills
    mx, my = MILL71
    piece(c, Poly([(mx - 44, 442), (mx + 44, 442), (mx + 28, my + 10), (mx - 28, my + 10)]), (124, 104, 92), border=2, shadow=PROP)
    for y in range(my + 24, 440, 16):
        dx = (y - my) * 0.1
        flat(c, Thick(mx - 28 - dx, y, mx + 28 + dx, y, 1.4), (108, 90, 80))
    piece(c, RRect(mx - 56, 354, mx + 56, 362, 1), (150, 110, 70), border=1.2, shadow=SMALL)
    for x in range(mx - 52, mx + 56, 12):
        flat(c, Thick(x, 340, x, 356, 1.5), (150, 110, 70))
    flat(c, Thick(mx - 56, 342, mx + 56, 342, 1.5), (150, 110, 70))
    piece(c, RRect(mx - 12, 404, mx + 12, 442, 3), (180, 60, 50) if "door" in d else (60, 110, 70), border=1.2, shadow=SMALL)
    flat(c, RRect(mx - 6, 310, mx + 6, 324, 1), (70, 60, 60))
    piece(c, Poly([(mx - 34, my + 14), (mx + 34, my + 14), (mx + 24, my - 14), (mx - 24, my - 14)]), (90, 80, 74), border=1.5, shadow=SMALL)
    sx, sy = MILL71_SMALL
    piece(c, [Poly([(sx - 22, 436), (sx + 22, 436), (sx + 14, sy + 6), (sx - 14, sy + 6)]),
              Poly([(sx - 18, sy + 8), (sx + 18, sy + 8), (sx + 12, sy - 8), (sx - 12, sy - 8)])], (130, 112, 100), border=1.5, shadow=PROP)
    # meadow foreground
    piece(c, hill_strip(488, [(6, 0.01, 0.3), (3, 0.04, 1.0)]), (122, 182, 92), shadow=LAYER)
    for x in range(560, 910, 28):
        piece(c, Poly([(x - 3, 512), (x - 3, 486), (x + 3, 486), (x + 3, 512)]), (240, 232, 214), shadow=SMALL)
    flat(c, [Thick(556, 494, 904, 494, 2.5), Thick(556, 504, 904, 504, 2.5)], (226, 216, 196))
    cow(c, 380, 560, (246, 244, 238), [(-12, -4, 9, 6), (8, 2, 7, 5), (18, -6, 5, 4)] if "cow" not in d else [(-6, 0, 12, 8), (16, 3, 4, 3)])
    cow(c, 486, 548, (180, 120, 80), [(-4, -2, 8, 6), (14, 2, 5, 4)], flip=True)
    hx, hy = lady(c, 760, 586, (60, 90, 160), hair=(200, 160, 100))
    flat(c, [Ell(hx, hy - 6, 8, 4), RRect(hx - 8, hy - 7, hx + 8, hy - 3, 2)], (250, 250, 246))
    flat(c, RRect(752, 556, 768, 584, 2), (246, 244, 236))
    flat(c, Thick(728, 540, 792, 540, 3), (150, 110, 70))
    for px in ((730, 790) if "pail" not in d else (730,)):
        flat(c, Thick(px, 540, px, 556, 1.2), (110, 110, 120))
        piece(c, Poly([(px - 9, 556), (px + 9, 556), (px + 7, 574), (px - 7, 574)]), (190, 196, 206), border=1.2, shadow=SMALL)
    clog = (200, 50, 50) if "clogs" in d else (240, 200, 60)
    for x in (198, 222):
        piece(c, Poly([(x - 12, 590), (x + 10, 590), (x + 12, 582), (x + 2, 578), (x - 10, 580)]), clog, border=1.2, shadow=SMALL)
        flat(c, Ell(x - 5, 582, 4, 2), lit(clog, 0.7))
    for x, col in ((60, (230, 60, 70)), (100, (250, 210, 60)), (140, (240, 140, 170))):
        piece(c, Poly([(x - 14, 600), (x + 14, 600), (x + 11, 578), (x - 11, 578)]), (190, 110, 80), border=1.2, shadow=PROP)
        for k in range(3):
            fx = x - 8 + k * 8
            flat(c, Thick(fx, 578, fx, 560, 2), (80, 150, 80))
            piece(c, Poly([(fx - 4, 560), (fx + 4, 560), (fx + 4, 552), (fx, 555), (fx - 4, 552)]), col, shadow=None)
    tree_round(c, 880, 600, 1.4, (90, 150, 90))


def sails(cx, cy, r, col=(236, 230, 214)):
    def d(c, m):
        for k in range(4):
            a = math.radians(20 + k * 90)
            ux, uy = math.cos(a), math.sin(a)
            nx, ny = -uy, ux
            flat(c, Thick(cx, cy, cx + ux * r, cy + uy * r, 3), (110, 90, 70))
            p0, p1 = (cx + ux * r * 0.2, cy + uy * r * 0.2), (cx + ux * r, cy + uy * r)
            piece(c, Poly([p0, p1, (p1[0] + nx * r * 0.22, p1[1] + ny * r * 0.22), (p0[0] + nx * r * 0.22, p0[1] + ny * r * 0.22)]), col,
                  border=1.2, shadow=SMALL)
            for t in (0.4, 0.6, 0.8):
                q = (cx + ux * r * t, cy + uy * r * t)
                flat(c, Thick(q[0], q[1], q[0] + nx * r * 0.22, q[1] + ny * r * 0.22, 1), (150, 130, 110))
        piece(c, Circ(cx, cy, 6), (90, 80, 74), shadow=None)
    return d


def l71_barge(c, m):
    x, y = BARGE
    piece(c, Poly([(x - 70, y - 12), (x + 70, y - 12), (x + 58, y + 6), (x - 62, y + 6)]), (120, 84, 56), border=1.5, shadow=SMALL)
    piece(c, RRect(x - 50, y - 26, x - 14, y - 12, 2), (200, 180, 140), shadow=None)
    flat(c, Thick(x + 10, y - 12, x + 10, y - 96, 3), (110, 80, 60))
    piece(c, Poly([(x + 13, y - 92), (x + 13, y - 18), (x + 58, y - 18)]), (80, 120, 190) if m else (226, 204, 150), border=1.2,
          shadow=SMALL)
    person(c, x - 30, y - 12, (90, 60, 50), h=0.7)


def l71_duck(x, y):
    def d(c, m):
        piece(c, [Ell(x, y, 10, 5), Circ(x + 8, y - 6, 4)], (250, 250, 246), shadow=None)
        flat(c, Poly([(x + 11, y - 6), (x + 16, y - 5), (x + 11, y - 4)]), (240, 160, 50))
    return d


def l71_sun(c, m):
    piece(c, Poly(star_pts(800, 70, 42, 31, points=12)), (255, 190, 80), shadow=PROP)
    piece(c, Circ(800, 70, 27), (255, 222, 95), border=2, shadow=PROP)


L71_ELEMENTS = [
    E("sun", l71_sun, weather=SUNNY, anim=dict(pulse=0.03, scaleSpeed=0.3)),
    cloud("cloudA", 220, 70, 0.8, (252, 252, 248), W_(CLEAR, OVERCAST), anim=dict(bobAmplitude=(30, 0), bobSpeed=0.02)),
    cloud("cloudB", 520, 50, 1.0, (200, 206, 216), CLOUDY, anim=dict(bobAmplitude=(24, 0), bobSpeed=0.025)),
    cloud("cloudC", 760, 110, 0.9, (186, 192, 204), CLOUDY, anim=dict(bobAmplitude=(-20, 0), bobSpeed=0.03)),
    cloud("cloudD", 80, 120, 0.7, (196, 202, 212), CLOUDY),
    rain_layer("rain", 71, 46, 24, 1.8, 0.55, 300),
    E("sails", sails(*MILL71, 104), pivot=MILL71, anim=dict(rotateSpeed=-40)),
    E("sails_small", sails(*MILL71_SMALL, 52), pivot=MILL71_SMALL, anim=dict(rotateSpeed=-55)),
    E("barge", l71_barge, pivot=(BARGE[0], BARGE[1] + 6), variant=True,
      anim=dict(bobAmplitude=(0, 2), bobSpeed=0.3, swingAngle=1.5, swingSpeed=0.2)),
    bird_el("bird0", 380, 150, 9, speed=18, weather=SUNNY), bird_el("bird1", 410, 136, 7, speed=18, weather=SUNNY),
] + [E("duck%d" % i, l71_duck(x, 470), pivot=(x, 474),
       anim=dict(drift_across(x - 12, x + 18, 9 + i * 2, x), bobAmplitude=(0, 1.5), bobSpeed=0.5)) for i, x in enumerate((700, 730))]

L71_DIFFS = [
    ("door", MILL71[0], 422, 0),
    ("tulips", 750, 377, 0),
    ("gable", 194, 222, 0),
    ("cow", 380, 530, 0),
    ("pail", 790, 562, 0),
    ("clogs", 210, 584, 0),
    ("sail", BARGE[0] + 30, BARGE[1] - 46, 0),
]


# =================================================================== Level 72 Versailles garden (18th c.)
URNS72 = list(range(80, 840, 60))
URN_DIFF = 10
TOPIARY_DIFF = 750
BALLOON = (770, 104)


def l72_bg(c, d):
    sky(c, (130, 190, 240), (246, 240, 224), 320)
    for x in (10, 60, 840, 890):
        tree_round(c, x, 304, 1.3, (70, 130, 80))
    piece(c, RRect(40, 192, 860, 304, 1), (242, 230, 204), border=2, shadow=PROP)
    piece(c, Poly([(32, 194), (868, 194), (848, 160), (52, 160)]), (108, 118, 140), border=1.5, shadow=SMALL)
    flat(c, Thick(52, 160, 848, 160, 3), (226, 186, 80))
    for i, x in enumerate(URNS72):
        if i == URN_DIFF and "urn" in d:
            continue
        piece(c, [Poly([(x - 6, 158), (x + 6, 158), (x + 8, 146), (x + 4, 140), (x - 4, 140), (x - 8, 146)]), RRect(x - 3, 134, x + 3, 141, 1)],
              (226, 186, 80), border=1, shadow=SMALL)
    for y0, y1 in ((204, 240), (252, 296)):
        for x in range(54, 850, 30):
            if 384 < x < 510:
                continue
            flat(c, arch(x, x + 14, y0, y1), (246, 240, 226))
            flat(c, arch(x + 2, x + 12, y0 + 2, y1 - 2), (150, 174, 196))
    piece(c, RRect(390, 172, 510, 304, 1), (248, 238, 216), border=2, shadow=PROP)
    for x in range(398, 510, 16):
        flat(c, RRect(x, 186, x + 6, 304, 1), (234, 222, 196))
    for x in (414, 450, 486):
        flat(c, arch(x - 9, x + 9, 236, 304), (90, 96, 110))
    piece(c, Poly([(380, 174), (520, 174), (450, 128)]), (248, 238, 216), border=2, shadow=PROP)
    flat(c, [Thick(380, 174, 450, 128, 2.5), Thick(450, 128, 520, 174, 2.5)], (226, 186, 80))
    piece(c, Circ(450, 158, 10), (250, 248, 240), border=1.5, shadow=SMALL)
    if "clock" in d:
        flat(c, [Thick(450, 158, 444, 160, 2), Thick(450, 158, 450, 166, 1.6)], INK)
    else:
        flat(c, [Thick(450, 158, 456, 158, 2), Thick(450, 158, 450, 150, 1.6)], INK)
    # gardens
    c.rect(0, 304, W, H, (226, 214, 184))
    for x in range(30, 900, 46):
        piece(c, Poly([(x - 7, 322), (x + 7, 322), (x, 300)]), (70, 130, 80), shadow=SMALL)
    for x0, x1 in ((20, 390), (510, 880)):
        piece(c, RRect(x0, 334, x1, 422, 4), (112, 172, 92), shadow=SMALL)
        cx = (x0 + x1) / 2
        for k in range(3):
            c.ellipse_ring(cx - 110 + k * 110, 378, 40, 26, 3, (82, 140, 72))
            c.ellipse_ring(cx - 110 + k * 110, 378, 18, 12, 3, (82, 140, 72))
        flat(c, [Thick(x0 + 10, 378, x1 - 10, 378, 2.5)], (82, 140, 72))
    for x in (30, 150, 270, 630, 750, 870):
        if x == TOPIARY_DIFF and "topiary" in d:
            piece(c, [Thick(x, 456, x, 420, 5), Circ(x, 404, 22)], (60, 120, 74), border=1.5, shadow=PROP)
        else:
            piece(c, [Poly([(x - 18, 452), (x + 18, 452), (x, 382)]), RRect(x - 14, 452, x + 14, 462, 2)], (60, 120, 74), border=1.5,
                  shadow=PROP)
    # Apollo fountain
    piece(c, Ell(450, 470, 170, 32), (226, 220, 206), border=2, shadow=PROP)
    flat(c, Ell(450, 468, 156, 25), (120, 180, 220))
    piece(c, RRect(426, 398, 474, 464, 2), (226, 220, 206), border=1.5, shadow=PROP)
    statue = (240, 236, 226) if "statue" in d else (226, 184, 70)
    piece(c, [Poly([(438, 398), (462, 398), (458, 368), (442, 368)]), Circ(450, 358, 9), Thick(442, 372, 430, 350, 4),
              Thick(458, 372, 472, 354, 4), Poly(star_pts(450, 358, 16, 12, points=10))], statue, border=1.2, shadow=SMALL)
    for x in (330, 380, 520, 570):
        piece(c, Ell(x, 462, 9, 6), (226, 184, 70), shadow=None)
    # foreground lawns + courtiers
    piece(c, RRect(-10, 560, 260, 612, 3), (112, 172, 92), shadow=SMALL)
    piece(c, RRect(640, 560, 910, 612, 3), (112, 172, 92), shadow=SMALL)
    hx, hy = lady(c, 180, 588, (240, 170, 190), hair=(246, 246, 246), wide=1.8)
    flat(c, Ell(hx, hy - 12, 8, 11), (246, 246, 246))
    flat(c, Thick(190, 550, 200, 496, 2), (120, 90, 70))
    piece(c, ellipse_top(200, 498, 32, 18), (140, 210, 170) if "parasol" in d else (190, 150, 220), border=1.5, shadow=PROP)
    hx, hy = person(c, 250, 588, (180, 50, 60) if "coat" in d else (60, 90, 160))
    flat(c, [Circ(hx - 4, hy, 7), Circ(hx - 6, hy + 5, 4)], (246, 246, 246))
    tricorne(c, hx, hy, 1.0, (30, 30, 40))
    flat(c, Thick(262, 588, 266, 556, 2), (60, 40, 30))
    hx, hy = lady(c, 700, 590, (160, 200, 230), hair=(246, 246, 246), wide=1.7)
    flat(c, Ell(hx, hy - 12, 8, 11), (246, 246, 246))
    hx, hy = person(c, 752, 590, (120, 60, 90))
    tricorne(c, hx, hy, 1.0, (30, 30, 40))
    # sedan chair with bearers
    person(c, 486, 592, (200, 180, 120))
    person(c, 600, 592, (200, 180, 120))
    flat(c, Thick(480, 560, 610, 560, 3), (110, 80, 60))
    piece(c, RRect(514, 520, 574, 584, 4), (170, 40, 50), border=1.5, shadow=PROP)
    flat(c, [RRect(522, 530, 566, 556, 2)], (230, 220, 190))
    piece(c, ellipse_top(544, 522, 32, 12), (226, 184, 70), shadow=None)
    # peacock (fanned tail in A, folded in B)
    if "peacock" in d:
        piece(c, Poly([(842, 576), (900, 590), (900, 596), (840, 584)]), (40, 120, 110), border=1.2, shadow=SMALL)
    else:
        piece(c, ellipse_top(846, 584, 52, 54), (40, 120, 110), border=1.5, shadow=PROP)
        for k in range(9):
            a = math.pi * (k + 0.5) / 9
            flat(c, [Circ(846 + 40 * math.cos(a), 584 - 42 * math.sin(a), 5)], (230, 190, 60))
            flat(c, [Circ(846 + 40 * math.cos(a), 584 - 42 * math.sin(a), 2.5)], (30, 60, 120))
    piece(c, [Ell(846, 576, 11, 9), Thick(846, 570, 852, 548, 4), Circ(853, 546, 4.5)], (40, 90, 170), border=1.2, shadow=SMALL)
    flat(c, Poly([(856, 546), (862, 548), (856, 549)]), (220, 180, 80))


def l72_balloon(c, m):
    x, y = BALLOON
    piece(c, [Ell(x, y, 40, 46), Poly([(x - 34, y + 22), (x + 34, y + 22), (x + 12, y + 58), (x - 12, y + 58)])], (60, 90, 170), border=2,
          shadow=PROP)
    flat(c, [Thick(x - 40, y, x + 40, y, 4), Thick(x - 30, y + 26, x + 30, y + 26, 3)], (226, 186, 80))
    for k in range(5):
        flat(c, Poly(star_pts(x - 24 + k * 12, y - 18, 4, 1.6, points=4, rot=0)), (226, 186, 80))
    flat(c, [Thick(x - 10, y + 58, x - 14, y + 74, 1.2), Thick(x + 10, y + 58, x + 14, y + 74, 1.2)], (100, 80, 60))
    piece(c, RRect(x - 16, y + 72, x + 16, y + 82, 2), (150, 110, 70), shadow=SMALL)


def jet(i, x0, y0, vx, vy):
    def d(c, m):
        flat(c, Circ(x0, y0, 3), (220, 240, 255, 0.9))
    return E("jet%d" % i, d, anim=dict(driftVelocity=(vx, vy), driftLength=60, driftFade=True, driftGrow=-0.3, phase=(i * 0.137) % 1))


L72_ELEMENTS = [
    cloud_el("cloud0", 160, 50, 0.7, 8), cloud_el("cloud1", 560, 40, 0.6, 6),
    E("balloon", l72_balloon, pivot=BALLOON, anim=dict(bobAmplitude=(6, 10), bobSpeed=0.07, swingAngle=2, swingSpeed=0.1)),
    flag_el("flagL", 60, 110, (250, 250, 246), (226, 186, 80)), flag_el("flagR", 838, 110, (250, 250, 246), (226, 186, 80)),
    bird_el("bird0", 300, 90, 9, speed=18), bird_el("bird1", 330, 78, 7, speed=18),
    E("water", lambda c, m: soft_union(c, [Ell(450, 330, 5, 22)], (220, 240, 255), 0.6, spread=6), pivot=(450, 352),
      anim=dict(stretch=(0.1, 0.2), scaleSpeed=1.2)),
] + [jet(i, 450, 312, vx, vy) for i, (vx, vy) in enumerate(((-18, 10), (18, 10), (-10, 20), (10, 20), (-26, 4), (26, 4)))] + \
    [jet(10 + i, x, 458, 0, 16) for i, x in enumerate((330, 380, 520, 570))]

L72_DIFFS = [
    ("clock", 450, 158, 0),
    ("urn", URNS72[URN_DIFF], 146, 0),
    ("topiary", TOPIARY_DIFF, 420, 0),
    ("statue", 450, 376, 0),
    ("parasol", 200, 490, 0),
    ("coat", 250, 568, 0),
    ("peacock", 860, 560, 0),
]


# =================================================================== Level 73 Victorian London (19th c.), day / night + fog / rain
DN73 = day_night(40.0, tint=(0.36, 0.34, 0.56))
STEPS73 = [(OVERCAST, 8), (FOG, 10), (RAIN, 8)]
WEATHER73 = dict(steps=STEPS73, blend=3.0, tints={OVERCAST: (0.9, 0.9, 0.92), FOG: (0.86, 0.86, 0.88), RAIN: (0.76, 0.78, 0.84)})
POTS73 = [50, 68, 86, 104]
WIN73 = [(x, y, x + 30, y + 40) for y in (180, 250, 320) for x in (14, 70, 126)]
LAMPS73 = [(250, 560), (770, 560)]


def l73_bg(c, d):
    sky(c, (168, 178, 192), (226, 218, 202), 360)
    # Palace of Westminster + Big Ben
    piece(c, RRect(170, 254, 470, 328, 1), (196, 174, 134), border=2, shadow=PROP)
    for x in range(176, 466, 14):
        piece(c, Poly([(x - 3, 256), (x + 3, 256), (x, 238)]), (196, 174, 134), shadow=None)
        flat(c, Thick(x, 262, x, 324, 1.2), (176, 154, 116))
    for y in (270, 296):
        for x in range(182, 460, 14):
            flat(c, RRect(x, y, x + 6, y + 14, 1), (110, 100, 90))
    piece(c, RRect(184, 150, 222, 330, 1), (196, 174, 134), border=2, shadow=PROP)
    for x in (184, 196, 208, 220):
        piece(c, Poly([(x - 3, 152), (x + 3, 152), (x, 132)]), (196, 174, 134), shadow=None)
    flat(c, [Thick(203, 132, 203, 108, 1.5), Poly([(204, 108), (222, 112), (204, 118)])], (200, 50, 50))
    piece(c, RRect(424, 120, 456, 328, 1), (204, 182, 136), border=2, shadow=PROP)
    for x in (432, 440, 448):
        flat(c, Thick(x, 124, x, 324, 1.2), (186, 164, 120))
    piece(c, RRect(418, 80, 462, 122, 1), (204, 182, 136), border=1.5, shadow=SMALL)
    piece(c, Circ(440, 100, 15), (246, 240, 220), border=1.5, shadow=SMALL)
    if "clock" in d:
        flat(c, [Thick(440, 100, 448, 106, 2.4), Thick(440, 100, 440, 112, 1.8)], INK)
    else:
        flat(c, [Thick(440, 100, 432, 95, 2.4), Thick(440, 100, 448, 90, 1.8)], INK)
    piece(c, RRect(424, 60, 456, 82, 1), (204, 182, 136), border=1.5, shadow=SMALL)
    for x in (428, 440, 452):
        flat(c, arch(x - 4, x + 4, 64, 80), (90, 80, 70))
    piece(c, Poly([(420, 62), (460, 62), (440, 14)]), (70, 84, 90), border=1.5, shadow=SMALL)
    flat(c, Circ(440, 14, 2.5), (226, 186, 80))
    # Thames
    c.rect(0, 328, W, 424, (112, 124, 124))
    for y in range(338, 422, 12):
        for x in range((y * 9) % 70, 900, 70):
            flat(c, Thick(x, y, x + 26, y, 2), (136, 148, 146))
    # Tower Bridge
    flat(c, [Thick(560, 300, 620, 200, 4), Thick(860, 200, 910, 290, 4)], (90, 128, 160))
    piece(c, RRect(560, 330, 910, 344, 1), (90, 128, 160), border=1.5, shadow=SMALL)
    piece(c, RRect(660, 194, 820, 208, 1), (90, 128, 160), border=1.5, shadow=SMALL)
    for tx in (640, 840):
        piece(c, RRect(tx - 20, 172, tx + 20, 412, 1), (208, 198, 178), border=2, shadow=PROP)
        for dx in (-20, 20):
            piece(c, [RRect(tx + dx - 4, 156, tx + dx + 4, 176, 1), Poly([(tx + dx - 5, 158), (tx + dx + 5, 158), (tx + dx, 144)])],
                  (208, 198, 178), shadow=None)
        piece(c, Poly([(tx - 16, 174), (tx + 16, 174), (tx, 134)]), (80, 94, 110), border=1.2, shadow=SMALL)
        for y in (200, 250, 300, 360):
            flat(c, arch(tx - 6, tx + 6, y, y + 22), (80, 80, 90))
        flat(c, Thick(tx, 134, tx, 112, 1.5), (80, 80, 80))
        fcol = ((40, 70, 160) if "flag" in d else (200, 40, 50)) if tx == 840 else (200, 40, 50)
        flat(c, Poly([(tx + 1, 112), (tx + 18, 115), (tx + 18, 123), (tx + 1, 124)]), fcol)
    # embankment + street
    piece(c, RRect(-10, 420, 910, 442, 0), (150, 150, 154), shadow=LAYER)
    c.rect(0, 442, W, H, (120, 112, 104))
    rnd = random.Random(73)
    for y in range(446, 600, 12):
        for x in range(-(y // 12 % 2) * 10, 900, 20):
            flat(c, RRect(x + 1, y + 1, x + 19, y + 11, 3), rnd.choice(((130, 122, 114), (112, 104, 98), (124, 116, 108))))
    for x, y, rx in ((470, 590, 50), (690, 600, 40), (120, 600, 36)):
        flat(c, Ell(x, y, rx, 6), (96, 104, 112))
    # terrace house with shop
    piece(c, RRect(-10, 150, 172, 472, 1), (150, 80, 62), border=2, shadow=PROP)
    for y in range(160, 470, 10):
        flat(c, Thick(-10, y, 172, y, 0.8), (136, 70, 56))
    piece(c, Poly([(-14, 152), (176, 152), (160, 132), (-4, 132)]), (90, 90, 100), border=1.5, shadow=SMALL)
    piece(c, RRect(40, 98, 116, 136, 1), (150, 80, 62), border=1.5, shadow=SMALL)
    for i, x in enumerate(POTS73):
        if i == 3 and "pots" in d:
            continue
        piece(c, RRect(x - 5, 82, x + 5, 100, 1), (196, 112, 80), border=1, shadow=SMALL)
    for r in WIN73:
        flat(c, RRect(r[0] - 3, r[1] - 3, r[2] + 3, r[3] + 3, 1), (240, 236, 226))
        flat(c, RRect(*r, 0), (70, 80, 96))
        flat(c, Thick(r[0], (r[1] + r[3]) / 2, r[2], (r[1] + r[3]) / 2, 2), (240, 236, 226))
    piece(c, RRect(-10, 380, 172, 472, 1), (40, 80, 60), border=1.5, shadow=SMALL)
    flat(c, RRect(10, 396, 110, 456, 2), (190, 210, 220))
    for x in (30, 60, 90):
        flat(c, [Ell(x, 446, 8, 6), RRect(x - 6, 430, x + 6, 446, 2)], (120, 80, 60))
    flat(c, RRect(124, 400, 160, 472, 2), (30, 50, 40))
    flat(c, Thick(172, 300, 210, 300, 2.5), (40, 40, 44))
    piece(c, RRect(182, 302, 214, 332, 2), (160, 40, 40) if "sign" in d else (40, 40, 44), border=1.5, shadow=SMALL)
    flat(c, Poly([(190, 324), (204, 324), (206, 318), (198, 316), (198, 308), (192, 308)]), (226, 186, 80))
    # lamp posts
    for x, base in LAMPS73:
        piece(c, [Thick(x, base, x, base - 110, 4), RRect(x - 8, base - 6, x + 8, base, 2)], (40, 44, 50), shadow=PROP)
        piece(c, Poly([(x - 9, base - 110), (x + 9, base - 110), (x + 12, base - 132), (x - 12, base - 132)]), (40, 44, 50), shadow=SMALL)
        flat(c, Poly([(x - 6, base - 112), (x + 6, base - 112), (x + 8, base - 128), (x - 8, base - 128)]), (240, 226, 170))
        flat(c, Poly([(x - 14, base - 132), (x + 14, base - 132), (x, base - 142)]), (40, 44, 50))
    # pillar box
    box = (40, 110, 70) if "postbox" in d else (200, 40, 44)
    piece(c, [RRect(306, 514, 334, 566, 4), Ell(320, 514, 16, 8)], box, border=1.5, shadow=PROP)
    flat(c, [RRect(312, 526, 328, 529, 1), RRect(304, 562, 336, 568, 1)], (30, 30, 34))
    # hansom cab
    piece(c, [Ell(520, 540, 34, 16)], (130, 90, 60), border=1.5, shadow=PROP)
    for lx in (-24, -12, 14, 26):
        flat(c, RRect(520 + lx - 2.5, 548, 520 + lx + 2.5, 580, 1), (110, 76, 50))
    piece(c, [Poly([(490, 536), (476, 500), (468, 504), (478, 540)]), Ell(470, 500, 11, 8)], (130, 90, 60), border=1.2, shadow=SMALL)
    flat(c, Thick(552, 534, 600, 530, 2.5), (60, 50, 44))
    piece(c, Poly([(590, 570), (600, 500), (660, 480), (676, 500), (676, 560), (640, 570)]), (40, 40, 46), border=1.5, shadow=PROP)
    flat(c, RRect(612, 504, 650, 528, 3), (150, 170, 190))
    wheel = (180, 50, 50) if "wheel" in d else (220, 180, 60)
    c.ellipse_ring(630, 552, 28, 28, 4, wheel)
    for k in range(8):
        a = math.pi * k / 4
        flat(c, Thick(630, 552, 630 + 26 * math.cos(a), 552 + 26 * math.sin(a), 1.6), wheel)
    hx, hy = person(c, 668, 482, (40, 40, 46), h=0.8)
    top_hat(c, hx, hy, 0.8, (30, 30, 34), (30, 30, 34))
    # people
    hx, hy = person(c, 400, 588, (40, 40, 50))
    top_hat(c, hx, hy, 1.0, (130, 92, 60) if "hat" in d else (30, 30, 34), (180, 40, 50))
    flat(c, Thick(410, 588, 414, 556, 2), (60, 40, 30))
    hx, hy = person(c, 140, 590, (110, 100, 80))
    flat(c, [Ell(hx, hy - 6, 9, 4), RRect(hx - 2, hy - 7, hx + 12, hy - 4, 1)], (80, 70, 60))
    piece(c, RRect(148, 552, 168, 566, 1), (236, 232, 216), border=1, shadow=SMALL)
    hx, hy = lady(c, 840, 590, (110, 60, 110))
    flat(c, Thick(852, 548, 856, 500, 2), (60, 40, 30))
    piece(c, ellipse_top(856, 502, 30, 16), (60, 40, 70), border=1.5, shadow=PROP)


def l73_steamer(c, m):
    piece(c, Poly([(400, 384), (548, 384), (536, 404), (412, 404)]), (40, 40, 46), border=1.5, shadow=SMALL)
    piece(c, RRect(424, 366, 520, 384, 2), (236, 232, 222), shadow=None)
    piece(c, RRect(472, 340, 488, 368, 1), (200, 60, 50), shadow=None)
    flat(c, RRect(472, 340, 488, 346, 1), (30, 30, 30))
    piece(c, ellipse_top(450, 390, 18, 18), (60, 60, 70), shadow=None)
    for x in range(432, 518, 12):
        flat(c, Circ(x, 375, 2.4), (70, 80, 96))


def _tinted(e):
    """Fog that darkens with the night instead of glowing white."""
    e.daynight = "tinted"
    return e


def l73_lamp_glow(c, m):
    soft_union(c, [Circ(x, b - 120, 14) for x, b in LAMPS73], (255, 214, 130), 0.6, spread=40)


L73_ELEMENTS = [
    _tinted(cloud("cloud0", 120, 46, 0.8, (196, 200, 208), 0, anim=dict(bobAmplitude=(26, 0), bobSpeed=0.02))),
    _tinted(cloud("cloud1", 640, 40, 0.9, (186, 190, 200), 0, anim=dict(bobAmplitude=(-22, 0), bobSpeed=0.025))),
    E("steamer", l73_steamer, pivot=(474, 404), anim=dict(bobAmplitude=(0, 2), bobSpeed=0.3, swingAngle=1, swingSpeed=0.2)),
] + smoke_el("steam", 480, 334, n=4, col=(220, 220, 224), r=9, rise=(-8, 22), length=80) + \
    [e for i, x in enumerate(POTS73[:3]) for e in smoke_el("pot%d_" % i, x, 76, n=2, col=(200, 200, 206), r=6, rise=(6, 18), length=56)] + [
    window_glow("windows", WIN73 + [(x, 270, x + 6, 284) for x in range(182, 460, 28)]),
    E("lamp_glow", l73_lamp_glow, daynight="night", anim=dict(twinkle=0.12, twinkleSpeed=0.9)),
    _tinted(fog_layer("fog0", 731, 250, 330, 0.4, 18)),
    _tinted(fog_layer("fog1", 732, 360, 430, 0.34, 26, direction=-1)),
    rain_layer("rain", 73, 40, 24, 1.6, 0.5, 300),
    bird_el("pigeon0", 300, 160, 8, col=(110, 110, 120), speed=16, weather=W_(OVERCAST)),
]

L73_DIFFS = [
    ("clock", 440, 100, 0),
    ("flag", 849, 118, 0),
    ("pots", 104, 90, 0),
    ("sign", 198, 316, 0),
    ("postbox", 320, 540, 0),
    ("wheel", 630, 552, 0),
    ("hat", 401, 534, 0),
]

LEVELS = [
    ("Level69", "文艺复兴佛罗伦萨", l69_bg, L69_ELEMENTS, L69_DIFFS, 140, OPTS),
    ("Level70", "威尼斯狂欢节", l70_bg, L70_ELEMENTS, L70_DIFFS, 140, dict(OPTS, day_night=DN70, anim_seconds=40.0, frames=80)),
    ("Level71", "荷兰黄金时代", l71_bg, L71_ELEMENTS, L71_DIFFS, 140, dict(OPTS, weather=WEATHER71, anim_seconds=26.0, frames=52)),
    ("Level72", "凡尔赛花园", l72_bg, L72_ELEMENTS, L72_DIFFS, 140, OPTS),
    ("Level73", "维多利亚伦敦", l73_bg, L73_ELEMENTS, L73_DIFFS, 140,
     dict(OPTS, day_night=DN73, weather=WEATHER73, anim_seconds=40.0, frames=80)),
]
