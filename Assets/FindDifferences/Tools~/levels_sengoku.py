# -*- coding: utf-8 -*-
"""Sengoku Japan (1467-1615), paper-craft side views, full-bleed:
  Level79 城下町   - a castle town under a white keep: townhouses, samurai, peddlers, a kite in the sky
  Level80 川中岛   - a battle across a river ford: camp curtains, a general with his war fan, cavalry, spearmen; fog cycle
  Level81 茶之汤   - a tea house in autumn, cut away: tokonoma, kettle, tea master and guest; the roji garden outside
  Level82 南蛮船   - a Portuguese carrack at Nagasaki: merchants, a Jesuit, goods on the pier, a church on the hill
  Level83 夜之城   - a castle by its moat; day / night: guards with lanterns, ninja appear on the roofs at night
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_el, drift_across, gy, layer, sky, smoke_el
from stylekit import day_night, star_field, window_glow
from weather import cloud, fog_layer
from levels_heian import GOLD, VERMILION, pine_jp, blossom_tree, stone_lantern, kasumi
from jp_kit import (PLASTER, SKIN, TILE, ashigaru, castle_keep, chochin, ellipse_top, ishigaki, kimono, machiya, plaster_wall, samurai,
                    shachi, tile_roof, westerner)

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def horse(c, x, base, col, flip=False, mane=(40, 34, 34)):
    s = -1 if flip else 1
    for lx in (-22, -12, 14, 24):
        flat(c, RRect(x + lx * s - 3, base - 32, x + lx * s + 3, base, 1), lit(col, 0.8))
    piece(c, [Ell(x, base - 38, 34, 15), Poly([(x + 28 * s, base - 44), (x + 42 * s, base - 76), (x + 52 * s, base - 72), (x + 40 * s, base - 40)]),
              Ell(x + 52 * s, base - 74, 12, 7)], col, border=1.5, shadow=PROP)
    flat(c, Thick(x + 32 * s, base - 50, x + 42 * s, base - 78, 4), mane)
    flat(c, Thick(x - 32 * s, base - 42, x - 42 * s, base - 22, 4), mane)
    flat(c, Circ(x + 54 * s, base - 76, 1.4), INK)


def nobori(eid, x, base, h, col, mon=None, variant_col=None, phase=0.0):
    def d(c, m):
        cc = variant_col if (m and variant_col) else col
        flat(c, Thick(x, base, x, base - h, 2.5), (90, 70, 60))
        flat(c, Thick(x, base - h + 4, x + 18, base - h + 4, 2), (90, 70, 60))
        piece(c, Poly([(x + 1, base - h + 4), (x + 18, base - h + 4), (x + 18, base - h * 0.35), (x + 1, base - h * 0.35)]), cc, shadow=SMALL)
        if mon:
            flat(c, Circ(x + 9.5, base - h * 0.78, 5), mon)
    return E(eid, d, pivot=(x, base - h * 0.6), variant=bool(variant_col),
             anim=dict(swingAngle=3, swingSpeed=0.5 + phase, stretch=(0.08, 0), scaleSpeed=1.1, phase=phase))


# =================================================================== Level 79 castle town
SHOPS79 = [(-10, 96, (150, 112, 80)), (86, 92, (176, 140, 100)), (178, 100, (140, 104, 76)), (278, 92, (166, 128, 92)),
           (370, 100, (150, 112, 80)), (470, 96, (176, 140, 100)), (566, 100, (140, 104, 76)), (666, 92, (166, 128, 92)), (758, 96, (150, 112, 80)),
           (854, 60, (176, 140, 100))]


def l79_bg(c, d):
    sky(c, (176, 206, 236), (246, 236, 214), 380)
    kasumi(c, 120, -20, 260, 16, col=(246, 240, 226))
    layer(c, 220, [(24, 0.006, 0.3), (10, 0.02, 1.1)], (160, 180, 190))
    layer(c, 268, [(12, 0.012, 1.4)], (132, 164, 140))
    piece(c, Poly([(380, 420), (460, 330), (560, 296), (740, 290), (860, 320), (920, 380), (920, 420)]), (118, 158, 108), shadow=LAYER)
    for x in (420, 470, 850, 890):
        pine_jp(c, x, 340 + (x % 3) * 8, 0.7)
    ishigaki(c, 560, 740, 304, 256)
    ridge = castle_keep(c, 650, 258, w0=150, tiers=4, tier_h=40, shachi_r="shachi" not in d)
    ishigaki(c, 440, 520, 336, 306, 10)
    castle_keep(c, 480, 308, w0=70, tiers=1, tier_h=30)
    plaster_wall(c, 520, 560, 300, 330)
    plaster_wall(c, 740, 860, 300, 330)
    # town
    for i, (x0, w, wall) in enumerate(SHOPS79):
        noren = ((200, 50, 50) if "noren" in d else (40, 60, 110)) if i == 2 else [(40, 60, 110), (120, 60, 40), (60, 90, 70)][i % 3]
        lantern = ((240, 236, 226) if "chochin" in d else (220, 60, 50)) if i == 6 else None
        machiya(c, x0, x0 + w, 452, 120, wall, noren, sign=(240, 230, 200) if i in (1, 5, 8) else None, lantern=lantern)
        if i == 4 and "sugidama" not in d:
            piece(c, Circ(x0 + 14, 360, 10), (90, 130, 70), border=1, shadow=SMALL)
            flat(c, Thick(x0 + 14, 340, x0 + 14, 350, 1.4), (90, 70, 60))
    # street + people
    piece(c, RRect(-10, 450, 910, 612, 0), (214, 196, 156), shadow=LAYER)
    for y in range(470, 600, 22):
        flat(c, Thick(0, y, 900, y, 1), (200, 180, 140))
    hx, hy = kimono(c, 160, 580, (60, 60, 80))
    piece(c, [Poly([(150, 552), (128, 548), (130, 556), (152, 562)]), Poly([(170, 552), (192, 548), (190, 556), (168, 562)])],
          (150, 200, 140) if "kamishimo" in d else (90, 110, 150), border=1, shadow=SMALL)
    flat(c, Thick(170, 560, 192, 548, 2), (40, 34, 34))
    kimono(c, 300, 584, (180, 160, 120), hat=(200, 176, 120))
    flat(c, Thick(270, 548, 330, 548, 2.5), (130, 96, 60))
    for px in (270, 330):
        flat(c, Thick(px, 548, px, 566, 1), (110, 90, 70))
        piece(c, Ell(px, 572, 12, 7), (170, 130, 80), border=1, shadow=SMALL)
    goods = (230, 120, 60) if "tenbin" in d else (240, 240, 230)
    for px in (270, 330):
        for k in range(3):
            flat(c, Ell(px - 6 + k * 6, 565, 3, 7), goods)
    kimono(c, 440, 586, (190, 60, 90), hair="woman", umbrella=(70, 130, 200) if "wagasa" in d else (230, 190, 60))
    horse(c, 620, 590, (150, 110, 80))
    piece(c, [RRect(596, 534, 644, 552, 3)], (200, 180, 140), border=1, shadow=SMALL)
    kimono(c, 690, 588, (90, 120, 90), hat=(200, 176, 120))
    kimono(c, 800, 590, (110, 70, 120), hair="woman")
    kimono(c, 840, 594, (220, 140, 60), h=0.7)
    for wx in (512, 576):
        c.ellipse_ring(wx, 584, 16, 16, 3, (110, 80, 56))
        flat(c, [Thick(wx - 14, 584, wx + 14, 584, 1.4), Thick(wx, 570, wx, 598, 1.4)], (110, 80, 56))
    piece(c, [RRect(494, 556, 600, 566, 1), Thick(494, 560, 470, 566, 3)], (150, 112, 76), shadow=PROP)
    for x in (514, 546, 578):
        piece(c, RRect(x - 13, 524, x + 13, 556, 5), (160, 110, 70), border=1.2, shadow=SMALL)
        flat(c, [Thick(x - 13, 532, x + 13, 532, 2), Thick(x - 13, 548, x + 13, 548, 2)], (110, 76, 50))
    for x in (40, 230, 390, 730):
        piece(c, RRect(x - 12, 466, x + 12, 490, 3), (130, 96, 70), border=1, shadow=PROP)
        piece(c, [Circ(x - 7, 460, 8), Circ(x + 6, 458, 9), Circ(x, 452, 8)], (80, 140, 80), shadow=SMALL)
    piece(c, [Ell(756, 590, 14, 8), Circ(770, 580, 6)], (200, 160, 110), shadow=SMALL)


def l79_kite(c, m):
    piece(c, Poly([(200, 120), (236, 128), (230, 166), (194, 160)]), (240, 230, 210), border=1.2, shadow=SMALL)
    flat(c, Circ(215, 143, 8), (210, 50, 50))
    flat(c, [Thick(212, 162, 218, 200, 1.2), Thick(218, 200, 210, 230, 1.2)], (200, 60, 60))


L79_ELEMENTS = [
    cloud_el("cloud0", 120, 60, 0.7, 8), cloud_el("cloud1", 440, 50, 0.6, 6),
    E("kite", l79_kite, pivot=(214, 160), anim=dict(bobAmplitude=(10, 8), bobSpeed=0.12, swingAngle=8, swingSpeed=0.3)),
    nobori("banner", 500, 276, 70, (240, 236, 226), mon=(40, 40, 46)),
    bird_el("bird0", 330, 110, 8, speed=16), bird_el("bird1", 356, 100, 6, speed=16),
]

L79_DIFFS = [
    ("shachi", 650 + 18, 32, 0),
    ("noren", SHOPS79[2][0] + 50, 409, 0),
    ("sugidama", SHOPS79[4][0] + 14, 360, 0),
    ("chochin", SHOPS79[6][0] + 12, 414, 0),
    ("kamishimo", 160, 552, 0),
    ("tenbin", 300, 566, 0),
    ("wagasa", 452, 504, 0),
]


# =================================================================== Level 80 battle at the river ford (fog)
STEPS80 = [(FOG, 9), (CLEAR, 9), (OVERCAST, 6)]
WEATHER80 = dict(steps=STEPS80, blend=3.0, tints={FOG: (0.86, 0.87, 0.9), OVERCAST: (0.88, 0.89, 0.92)})
NOBORI80 = [(70, (230, 60, 50)), (140, (240, 236, 226)), (230, (230, 60, 50)), (600, (40, 50, 90)), (690, (240, 236, 226)), (780, (40, 50, 90)),
            (860, (240, 236, 226))]
NOBORI_DIFF = 0


def bishi(c, x, y, r, col):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        cx, cy = x + dx * r * 0.55, y + dy * r * 0.55
        flat(c, Poly([(cx, cy - r * 0.45), (cx + r * 0.45, cy), (cx, cy + r * 0.45), (cx - r * 0.45, cy)]), col)


def l80_bg(c, d):
    sky(c, (190, 206, 220), (236, 232, 220), 380)
    layer(c, 214, [(30, 0.006, 0.4), (12, 0.02, 1.2)], (150, 164, 180))
    layer(c, 262, [(18, 0.01, 1.1)], (122, 146, 140))
    piece(c, hill_strip(340, [(6, 0.01, 0.4)]), (150, 170, 110), shadow=LAYER)
    c.rect(0, 360, W, 404, (120, 160, 180))
    for y in range(368, 402, 10):
        for x in range((y * 17) % 60, 900, 60):
            flat(c, Thick(x, y, x + 22, y, 2), (160, 196, 210))
    piece(c, hill_strip(402, [(5, 0.012, 0.3), (2, 0.04, 1.0)]), (156, 168, 108), shadow=LAYER)
    # camp curtains (maku) with the clan crest
    piece(c, RRect(14, 404, 320, 470, 0), (244, 240, 230), border=1.5, shadow=PROP)
    for y in (418, 440, 460):
        flat(c, Thick(14, y, 320, y, 5), (30, 30, 36))
    for x in (14, 120, 220, 320):
        flat(c, Thick(x, 396, x, 474, 3), (110, 80, 60))
    for cx in (66, 170, 270):
        flat(c, Circ(cx, 430, 14), (244, 240, 230))
        bishi(c, cx, 430, 14, (200, 40, 40) if ("maku" in d and cx == 170) else (30, 30, 36))
    # general on his stool with a war fan, drummer
    piece(c, [Thick(140, 520, 180, 500, 3), Thick(180, 520, 140, 500, 3)], (110, 80, 60), shadow=SMALL)
    samurai(c, 160, 516, (180, 40, 40), crest=GOLD)
    fan = (226, 186, 70) if "fan" in d else (30, 30, 36)
    flat(c, Thick(176, 490, 196, 464, 2), (110, 80, 60))
    piece(c, Poly([(186, 470), (212, 450), (214, 478), (196, 486)]), fan, border=1.2, shadow=SMALL)
    flat(c, Circ(200, 468, 5), (200, 40, 40) if fan[0] < 100 else (200, 40, 40))
    if "drum" not in d:
        piece(c, [RRect(244, 470, 300, 506, 6), Thick(250, 506, 246, 528, 3), Thick(294, 506, 298, 528, 3)], (160, 100, 60), border=1.2, shadow=PROP)
        flat(c, Ell(272, 488, 20, 14), (230, 214, 180))
    ashigaru(c, 330, 528, (60, 70, 90))
    # spearmen line
    for i, x in enumerate(range(380, 560, 30)):
        ashigaru(c, x, 560 + (i % 2) * 6, (60, 70, 90) if i % 2 else (80, 60, 50))
    # mounted samurai
    horse(c, 660, 552, (60, 50, 50) if "horse" in d else (240, 236, 226), flip=True)
    samurai(c, 664, 520, (40, 60, 120), crest=(200, 200, 210) if "crest" in d else GOLD,
            sashimono=(230, 190, 60) if "sashimono" in d else (230, 60, 50))
    horse(c, 760, 560, (130, 90, 60), flip=True)
    samurai(c, 764, 528, (60, 60, 70), crest=GOLD, sashimono=(240, 236, 226))
    # gunners kneeling
    for x in (720, 800, 870):
        ashigaru(c, x, 600, (70, 60, 50), h=0.9, weapon="teppo")


def smoke_puff(eid, x, y, phase):
    def d(c, m):
        piece(c, [Circ(x, y, 8), Circ(x + 8, y - 4, 7), Circ(x + 4, y + 4, 6)], (236, 236, 236), shadow=None)
    return E(eid, d, pivot=(x, y), anim=dict(driftVelocity=(-14, 10), driftLength=70, driftFade=True, driftGrow=1.4, phase=phase))


L80_ELEMENTS = [nobori("nobori%d" % i, x, 400 if x < 400 else 410, 120, col, mon=(30, 30, 36) if col[0] > 200 else (240, 236, 226),
                      variant_col=(90, 150, 90) if i == NOBORI_DIFF else None, phase=i * 0.13) for i, (x, col) in enumerate(NOBORI80)] + [
    smoke_puff("smoke%d" % i, x + 26, 568, (i * 0.3) % 1) for i, x in enumerate((720, 800, 870))] + [
    fog_layer("fog0", 801, 300, 380, 0.5, 16), fog_layer("fog1", 802, 430, 520, 0.4, 22, direction=-1),
    cloud("cloud0", 200, 70, 0.9, (226, 230, 236), W_(CLEAR, OVERCAST)), cloud("cloud1", 640, 50, 1.0, (210, 214, 222), W_(OVERCAST)),
    bird_el("crow0", 420, 130, 9, col=(40, 40, 46), speed=18), bird_el("crow1", 448, 118, 7, col=(40, 40, 46), speed=18),
]

L80_DIFFS = [
    ("maku", 170, 430, 0),
    ("fan", 200, 466, 0),
    ("drum", 272, 490, 0),
    ("sashimono", 658, 460, 0),
    ("horse", 660, 516, 0),
    ("crest", 664, 466, 0),
    ("nobori", NOBORI80[NOBORI_DIFF][0] + 9, 330, 0),
]


# =================================================================== Level 81 tea house in autumn
def l81_bg(c, d):
    sky(c, (206, 218, 230), (250, 236, 214), 380)
    rnd = random.Random(81)
    for k in range(40):
        x = rnd.uniform(-10, 910)
        col = rnd.choice(((110, 160, 100), (90, 140, 90), (130, 176, 110)))
        flat(c, Thick(x, 0, x, 400, rnd.uniform(5, 9)), col)
        for y in range(30, 400, 40):
            flat(c, Thick(x - 4, y, x + 4, y, 1.4), lit(col, 0.8))
    for x, s, col in ((60, 1.4, (214, 70, 50)), (300, 1.2, (236, 140, 50)), (420, 1.0, (200, 60, 50))):
        if x == 300 and "maple" in d:
            col = (120, 170, 80)
        blossom_tree(c, x, 400, s, col, 810 + x, trunk=(96, 70, 62))
    # bamboo fence
    for x in range(0, 470, 40):
        flat(c, Thick(x, 360, x, 430, 4), (180, 160, 110))
    for y in (370, 395, 420):
        flat(c, Thick(0, y, 470, y, 3), (190, 170, 120))
    # roji ground with stepping stones
    piece(c, hill_strip(428, [(4, 0.01, 0.3)]), (128, 150, 96), shadow=LAYER)
    for x, y in ((40, 560), (110, 540), (180, 520), (250, 500), (320, 486), (390, 470), (440, 456)):
        piece(c, Ell(x, y, 26, 9), (180, 176, 166), border=1, shadow=SMALL)
    if "geta" not in d:
        for dx in (-6, 6):
            piece(c, RRect(440 + dx - 4, 446, 440 + dx + 4, 452, 1), (150, 110, 70), shadow=None)
    if "sekimori" not in d:
        piece(c, Circ(250, 488, 9), (120, 110, 100), border=1, shadow=SMALL)
        flat(c, [Thick(242, 486, 258, 486, 2), Thick(250, 480, 250, 492, 2)], (40, 34, 34))
    stone_lantern(c, 150, 470, 0.8)
    # tsukubai
    piece(c, [Ell(330, 560, 34, 12), RRect(300, 530, 360, 560, 6)], (150, 146, 136), border=1.2, shadow=PROP)
    flat(c, Ell(330, 532, 22, 6), (90, 130, 150))
    flat(c, [Thick(370, 520, 344, 528, 4)], (150, 160, 90))
    if "ladle" not in d:
        flat(c, [Thick(306, 528, 352, 524, 1.6), RRect(298, 522, 310, 532, 2)], (200, 180, 120))
    # waiting bench with a guest
    piece(c, [RRect(20, 470, 120, 478, 1), RRect(26, 478, 32, 500, 1), RRect(108, 478, 114, 500, 1)], (150, 110, 70), shadow=PROP)
    kimono(c, 70, 474, (70, 70, 90), h=0.8)
    # tea house (cut away)
    piece(c, RRect(470, 250, 900, 440, 0), (200, 176, 136), border=1.5, shadow=PROP)
    flat(c, RRect(480, 262, 890, 420, 0), (222, 204, 166))
    piece(c, Poly([(440, 256), (930, 256), (880, 180), (500, 180)]), (176, 150, 100), border=1.5, shadow=PROP)
    for y in range(190, 254, 8):
        flat(c, Thick(500 - (y - 180) * 0.7, y, 880 + (y - 180) * 0.6, y, 1), (150, 126, 84))
    piece(c, RRect(470, 418, 900, 440, 0), (200, 186, 130), shadow=None)
    for x in range(470, 900, 60):
        flat(c, Thick(x, 420, x, 440, 1.2), (160, 146, 96))
    flat(c, RRect(470, 380, 490, 418, 1), (60, 50, 40))
    # tokonoma: scroll + camellia
    flat(c, RRect(490, 262, 590, 410, 0), (210, 190, 150))
    flat(c, RRect(488, 408, 592, 414, 0), (90, 60, 40))
    piece(c, RRect(518, 272, 562, 382, 1), (236, 230, 214), border=1, shadow=SMALL)
    if "scroll" in d:
        c.ellipse_ring(540, 320, 14, 14, 3, (40, 36, 36))
    else:
        flat(c, Poly([(522, 360), (534, 316), (544, 336), (552, 300), (560, 360)]), (90, 90, 96))
        flat(c, Poly([(522, 360), (540, 340), (560, 360)]), (140, 140, 146))
    flat(c, [RRect(516, 268, 564, 274, 1), RRect(516, 380, 564, 386, 1)], (90, 60, 40))
    piece(c, RRect(568, 370, 578, 408, 2), (150, 160, 90), shadow=SMALL)
    flat(c, Thick(573, 372, 584, 352, 1.4), (70, 110, 60))
    piece(c, Circ(586, 350, 6), (240, 236, 240) if "camellia" in d else (200, 30, 50), shadow=None)
    flat(c, Circ(586, 350, 2), (240, 200, 60))
    # hearth and kettle, host and guest
    flat(c, RRect(660, 416, 720, 422, 0), (60, 50, 44))
    piece(c, [Ell(690, 404, 22, 14), RRect(684, 386, 696, 392, 1)], (40, 36, 36), border=1.2, shadow=SMALL)
    kimono(c, 640, 418, (60, 50, 60))
    kimono(c, 820, 418, (120, 90, 70))
    piece(c, ellipse_top(760, 418, 12, 12), (200, 60, 50) if "chawan" in d else (30, 28, 30), border=1, shadow=SMALL)
    flat(c, Ell(760, 408, 8, 2), (120, 170, 80))


def l81_leaf(i, x, y):
    col = [(214, 70, 50), (236, 140, 50), (200, 60, 50)][i % 3]

    def d(c, m):
        flat(c, Poly(star_pts(x, y, 6, 2.6, points=5)), col)
    return E("leaf%d" % i, d, pivot=(x, y), anim=dict(driftVelocity=(14, -22), driftLength=400, driftFade=True, rotateSpeed=70 + i * 11,
                                                      spinSpeed=0.5 + 0.08 * i, spinShade=0.3, bobAmplitude=(14, 0), bobSpeed=0.3,
                                                      phase=(i * 0.173) % 1))


L81_ELEMENTS = smoke_el("steam", 690, 382, n=3, col=(246, 246, 246), r=5, rise=(2, 18), length=50) + [
    E("drip", lambda c, m: flat(c, Circ(346, 528, 2), (180, 220, 240, 0.9)), anim=dict(driftVelocity=(0, -20), driftLength=14, driftFade=True)),
    bird_el("bird0", 600, 120, 7, speed=12),
] + [l81_leaf(i, x, y) for i, (x, y) in enumerate(((60, 300), (120, 260), (300, 310), (360, 280), (420, 320), (20, 340), (260, 260)))]

L81_DIFFS = [
    ("scroll", 540, 326, 0),
    ("camellia", 586, 350, 0),
    ("chawan", 760, 410, 0),
    ("ladle", 320, 526, 0),
    ("sekimori", 250, 486, 0),
    ("maple", 300, 320, 0),
    ("geta", 440, 450, 0),
]


# =================================================================== Level 82 Nanban trade at Nagasaki
SHIP82 = (100, 444)


def l82_bg(c, d):
    sky(c, (150, 200, 240), (246, 236, 214), 320)
    layer(c, 214, [(26, 0.006, 0.5), (10, 0.02, 1.0)], (140, 170, 140))
    rnd = random.Random(82)
    for k in range(18):
        x = 520 + k * 22 + rnd.uniform(-4, 4)
        y = gy(214, [(26, 0.006, 0.5), (10, 0.02, 1.0)], x) + 30 + rnd.uniform(0, 30)
        piece(c, RRect(x - 9, y - 10, x + 9, y, 1), (230, 220, 200), shadow=None)
        flat(c, Poly([(x - 12, y - 9), (x + 12, y - 9), (x, y - 17)]), TILE)
    piece(c, [RRect(750, 216, 790, 250, 1), Poly([(744, 218), (796, 218), (770, 196)])], (240, 236, 226), border=1.2, shadow=SMALL)
    if "cross" not in d:
        flat(c, [Thick(770, 196, 770, 176, 2.5), Thick(762, 184, 778, 184, 2.5)], (226, 186, 80))
    c.rect(0, 290, W, 474, (70, 140, 180))
    for y in range(300, 472, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (110, 170, 204))
    # carrack
    x0, base = SHIP82
    for mx, top in ((x0 + 90, 150), (x0 + 210, 110), (x0 + 330, 160)):
        flat(c, Thick(mx, base - 50, mx, top, 4), (110, 80, 60))
    for mx, y0, y1, w in ((x0 + 90, 170, 240, 50), (x0 + 210, 130, 230, 66), (x0 + 210, 236, 300, 72), (x0 + 330, 180, 250, 46)):
        piece(c, Poly([(mx - w, y0), (mx + w, y0), (mx + w + 4, y1), (mx - w - 4, y1)]), (246, 240, 226), border=1.2, shadow=SMALL)
    crossc = (60, 90, 180) if "sail" in d else (200, 40, 40)
    flat(c, [Thick(x0 + 210, 246, x0 + 210, 292, 7), Thick(x0 + 188, 264, x0 + 232, 264, 7)], crossc)
    flat(c, Poly([(x0 + 211, 110), (x0 + 250, 116), (x0 + 211, 124)]), (60, 140, 80) if "flag" in d else (230, 60, 50))
    piece(c, Poly([(x0, base - 70), (x0 + 60, base - 60), (x0 + 360, base - 60), (x0 + 420, base - 92), (x0 + 430, base - 50), (x0 + 390, base),
                   (x0 + 40, base)]), (44, 36, 34), border=2, shadow=PROP)
    flat(c, [Thick(x0 + 10, base - 52, x0 + 410, base - 52, 3), Thick(x0 + 30, base - 20, x0 + 395, base - 20, 2)], (226, 186, 80))
    for k in range(9):
        flat(c, RRect(x0 + 80 + k * 32, base - 42, x0 + 90 + k * 32, base - 32, 1), (30, 26, 26))
    # tender boat between ship and pier is an element; pier and goods
    piece(c, RRect(-10, 470, 910, 612, 0), (170, 130, 90), shadow=LAYER)
    for x in range(0, 900, 36):
        flat(c, Thick(x, 470, x, 612, 1.4), (150, 112, 76))
    n = 3 if "crates" in d else 4
    for k in range(n):
        piece(c, RRect(60 + (k % 2) * 34, 556 - (k // 2) * 30, 92 + (k % 2) * 34, 586 - (k // 2) * 30, 2), (190, 150, 100), border=1.2, shadow=PROP)
    for x in (170, 200):
        piece(c, Ell(x, 576, 16, 12), (220, 210, 180), border=1.2, shadow=PROP)
        flat(c, Thick(x - 14, 574, x + 14, 574, 1.4), (160, 140, 110))
    # captain with parasol bearer, Jesuit, merchants
    hx, hy = westerner(c, 340, 588, (120, 40, 50), hat=None, trousers=(150, 120, 60))
    flat(c, [Ell(342, 568, 14, 9)], (150, 120, 60))
    flat(c, [Ell(hx, hy - 6, 12, 3), Ell(hx, hy - 9, 7, 4)], (30, 30, 34))
    flat(c, Thick(hx + 4, hy - 10, hx + 18, hy - 22, 2.4), (90, 160, 220) if "feather" in d else (240, 240, 240))
    flat(c, Circ(hx, hy + 6, 7), (246, 244, 236))
    kimono(c, 382, 590, (160, 140, 110))
    flat(c, Thick(380, 560, 360, 490, 2), (110, 80, 60))
    piece(c, ellipse_top(360, 494, 34, 16), (70, 130, 200) if "parasol" in d else (220, 60, 60), border=1.2, shadow=PROP)
    westerner(c, 470, 590, (30, 28, 32), hat=None, trousers=(30, 28, 32))
    flat(c, Thick(470, 556, 470, 572, 1.6), (226, 186, 80))
    for x, col in ((560, (60, 80, 120)), (610, (140, 90, 60)), (700, (90, 110, 80))):
        kimono(c, x, 590, col)
    samurai(c, 770, 590, (70, 60, 50), crest=None)
    # parrot in a cage
    piece(c, ellipse_top(250, 540, 22, 30), (150, 110, 60), shadow=PROP)
    piece(c, RRect(228, 540, 272, 548, 1), (150, 110, 60), shadow=None)
    for x in range(232, 270, 7):
        flat(c, Thick(x, 516, x, 540, 1), (120, 90, 50))
    parrot = (220, 50, 50) if "parrot" in d else (60, 170, 80)
    piece(c, [Ell(250, 526, 7, 10), Circ(252, 514, 5)], parrot, shadow=None)
    flat(c, Poly([(256, 514), (261, 516), (256, 518)]), (240, 200, 60))
    piece(c, RRect(236, 548, 264, 584, 1), (130, 96, 60), shadow=PROP)


def l82_tender(c, m):
    piece(c, Poly([(560, 452), (640, 452), (630, 464), (570, 464)]), (130, 90, 60), border=1.2, shadow=SMALL)
    piece(c, RRect(584, 438, 610, 452, 1), (190, 150, 100), shadow=None)
    kimono(c, 620, 454, (70, 80, 110), h=0.6)
    flat(c, Thick(632, 420, 618, 470, 1.6), (110, 80, 60))


L82_ELEMENTS = [
    cloud_el("cloud0", 640, 60, 0.7, 7), cloud_el("cloud1", 860, 100, 0.5, 5),
    E("tender", l82_tender, pivot=(600, 464), anim=dict(drift_across(556, 644, 10), bobAmplitude=(0, 1.5), bobSpeed=0.4)),
    E("pennant", lambda c, m: flat(c, Poly([(SHIP82[0] + 331, 160), (SHIP82[0] + 370, 164), (SHIP82[0] + 331, 168)]), (240, 236, 226)),
      pivot=(SHIP82[0] + 331, 164), anim=dict(stretch=(0.2, 0), scaleSpeed=1.3, swingAngle=4, swingSpeed=0.8)),
    bird_el("gull0", 520, 120, 10, col=(246, 246, 246), speed=16), bird_el("gull1", 548, 108, 8, col=(246, 246, 246), speed=16),
]

L82_DIFFS = [
    ("sail", SHIP82[0] + 210, 268, 0),
    ("flag", SHIP82[0] + 230, 116, 0),
    ("cross", 770, 186, 0),
    ("crates", 110, 530, 0),
    ("parrot", 250, 522, 0),
    ("feather", 352, 528, 0),
    ("parasol", 360, 486, 0),
]


# =================================================================== Level 83 castle at night (ninja)
DN83 = day_night(40.0, tint=(0.28, 0.30, 0.56))
TURRET_WIN = [(608 + k * 22, 352, 616 + k * 22, 364) for k in range(4)] + [(286 + k * 24, 196, 294 + k * 24, 206) for k in range(4)]


def l83_bg(c, d):
    sky(c, (160, 196, 230), (240, 224, 206), 380)
    layer(c, 230, [(20, 0.007, 0.4), (8, 0.02, 1.2)], (140, 160, 170))
    piece(c, Poly([(120, 420), (190, 300), (420, 290), (500, 420)]), (110, 140, 100), shadow=LAYER)
    ishigaki(c, 220, 400, 300, 262)
    ridge = castle_keep(c, 310, 264, w0=140, tiers=3, tier_h=40, shachi_r="shachi" not in d)
    # turret over the moat, walls and gate
    ishigaki(c, 560, 740, 440, 380)
    piece(c, RRect(584, 330, 716, 380, 1), PLASTER, border=1.5, shadow=PROP)
    flat(c, RRect(584, 360, 716, 380, 0), (60, 56, 60))
    tile_roof(c, 584, 716, 330, 26, gable=True)
    piece(c, RRect(590, 290, 710, 330, 1), PLASTER, border=1.5, shadow=PROP)
    tile_roof(c, 600, 700, 292, 22)
    piece(c, Circ(650, 346, 8), (40, 120, 70) if "mon" in d else (226, 186, 80), border=1, shadow=SMALL)
    flat(c, Poly(star_pts(650, 346, 6, 2.5, points=3)), (60, 56, 60))
    shachi(c, 628, 266, 0.8, flip=True)
    shachi(c, 672, 266, 0.8)
    plaster_wall(c, 380, 470, 380, 440)
    plaster_wall(c, 740, 920, 380, 440)
    piece(c, RRect(470, 360, 560, 440, 1), (60, 50, 44), border=1.5, shadow=PROP)
    tile_roof(c, 466, 564, 360, 18)
    if "gate" in d:
        flat(c, RRect(480, 376, 550, 440, 0), (24, 20, 20))
        piece(c, [RRect(470, 376, 480, 440, 0), RRect(550, 376, 560, 440, 0)], (110, 80, 56), shadow=SMALL)
    else:
        piece(c, RRect(480, 376, 550, 440, 0), (110, 80, 56), shadow=SMALL)
        flat(c, Thick(515, 376, 515, 440, 2), (60, 44, 34))
        for y in (392, 412, 432):
            for x in (490, 504, 526, 540):
                flat(c, Circ(x, y, 2), (226, 186, 80))
    flat(c, Thick(380, 300, 380, 380, 2.5), (90, 70, 60))
    flat(c, Poly([(381, 302), (398, 302), (398, 352), (381, 352)]), (60, 60, 120) if "banner" in d else (240, 236, 226))
    # moat
    c.rect(0, 440, W, 510, (60, 100, 120))
    for y in range(450, 508, 12):
        for x in range((y * 11) % 60, 900, 60):
            flat(c, Thick(x, y, x + 20, y, 2), (90, 130, 150))
    if "boat" not in d:
        piece(c, Poly([(150, 470), (250, 470), (236, 484), (164, 484)]), (110, 80, 56), border=1.2, shadow=SMALL)
        flat(c, Thick(170, 470, 140, 444, 1.4), (150, 120, 90))
    # near bank: pine, guards, well
    piece(c, hill_strip(508, [(5, 0.012, 0.4), (2, 0.04, 1.0)]), (110, 130, 90), shadow=LAYER)
    pine_jp(c, 60, 610, 1.8)
    kimono(c, 420, 590, (60, 60, 80))
    chochin(c, 436, 548, (240, 236, 226) if "lantern" in d else (220, 60, 50))
    kimono(c, 520, 592, (80, 60, 60))
    chochin(c, 536, 550, (220, 60, 50))
    piece(c, [RRect(760, 556, 820, 590, 2)], (150, 146, 136), border=1.2, shadow=PROP)
    piece(c, [Thick(764, 556, 764, 506, 3), Thick(816, 556, 816, 506, 3), Thick(756, 506, 824, 506, 4)], (110, 80, 56), shadow=SMALL)
    if "bucket" not in d:
        flat(c, Thick(790, 506, 790, 530, 1.2), (90, 70, 60))
        piece(c, RRect(782, 530, 798, 546, 2), (160, 120, 80), border=1, shadow=SMALL)
    stone_lantern(c, 660, 590, 0.9)
    for x, y in ((860, 596), (884, 596), (872, 570)):
        piece(c, Ell(x, y - 12, 16, 12), (200, 176, 110), border=1, shadow=PROP)
        flat(c, [Thick(x - 14, y - 16, x + 14, y - 16, 1.4), Thick(x - 14, y - 8, x + 14, y - 8, 1.4)], (150, 120, 70))
    for x in (260, 330, 600):
        piece(c, [Circ(x - 12, 600, 14), Circ(x + 6, 594, 17), Circ(x + 22, 602, 12)], (70, 110, 70), shadow=PROP)


def ninja(x, base, h=1.0, pose=0):
    def d(c, m):
        col = (24, 24, 30)
        piece(c, [Poly([(x - 8 * h, base - 8 * h), (x + 8 * h, base - 8 * h), (x + 6 * h, base - 28 * h), (x - 6 * h, base - 28 * h)]),
                  Circ(x + 1 * h, base - 34 * h, 6.5 * h), Thick(x - 4 * h, base - 8 * h, x - 10 * h + pose * 6 * h, base, 3 * h),
                  Thick(x + 4 * h, base - 8 * h, x + 8 * h, base, 3 * h)], col, shadow=SMALL)
        flat(c, RRect(x - 2 * h, base - 36 * h, x + 6 * h, base - 33 * h, 1), (240, 220, 190))
        flat(c, Thick(x - 6 * h, base - 26 * h, x + 10 * h, base - 38 * h, 1.6 * h), (90, 90, 100))
    return d


L83_ELEMENTS = [
    E("sun", lambda c, m: (piece(c, Poly(star_pts(780, 90, 40, 30, points=12)), (255, 190, 80), shadow=PROP),
                           piece(c, Circ(780, 90, 26), (255, 216, 100), border=2, shadow=PROP)), daynight="day"),
    E("moon", lambda c, m: (soft_union(c, [Circ(780, 90, 46)], (255, 250, 220), 0.4, spread=26),
                            piece(c, Circ(780, 90, 36), (252, 246, 220), border=2, shadow=PROP)), daynight="night"),
    star_field("stars", 83, 50, 220, avoid=[(720, 30, 840, 150)]),
    cloud_el("cloud0", 520, 60, 0.6, 6, daynight="day"),
    window_glow("windows", TURRET_WIN),
    E("lantern_glow", lambda c, m: soft_union(c, [Circ(436, 560, 8), Circ(536, 562, 8)], (255, 200, 110), 0.6, spread=22), daynight="night",
      anim=dict(twinkle=0.12, twinkleSpeed=1.1)),
    E("ninja0", ninja(340, 222, 0.9), daynight="night", anim=dict(bobAmplitude=(30, 0), bobSpeed=0.06)),
    E("ninja1", ninja(860, 368, 1.0, pose=1), daynight="night", anim=dict(bobAmplitude=(0, 6), bobSpeed=0.5, bounce=True)),
    E("ninja2", ninja(70, 490, 0.9), daynight="night", anim=dict(twinkle=0.9, twinkleSpeed=0.12)),
    E("owl", lambda c, m: (piece(c, [Ell(110, 440, 9, 12), Circ(110, 426, 8)], (120, 100, 80), shadow=SMALL),
                           flat(c, [Circ(107, 426, 2.4), Circ(114, 426, 2.4)], (255, 220, 90))), daynight="night"),
    bird_el("crow0", 460, 130, 9, col=(40, 40, 46), speed=16, daynight="day"),
]

L83_DIFFS = [
    ("shachi", 310 + 17, 40, 0),
    ("mon", 650, 346, 0),
    ("gate", 515, 408, 0),
    ("banner", 390, 326, 0),
    ("boat", 200, 476, 0),
    ("lantern", 436, 560, 0),
    ("bucket", 790, 530, 0),
]

LEVELS = [
    ("Level79", "城下町", l79_bg, L79_ELEMENTS, L79_DIFFS, 140, OPTS),
    ("Level80", "川中岛", l80_bg, L80_ELEMENTS, L80_DIFFS, 140, dict(OPTS, weather=WEATHER80, anim_seconds=24.0, frames=48)),
    ("Level81", "茶之汤", l81_bg, L81_ELEMENTS, L81_DIFFS, 140, OPTS),
    ("Level82", "南蛮船", l82_bg, L82_ELEMENTS, L82_DIFFS, 140, OPTS),
    ("Level83", "夜之城", l83_bg, L83_ELEMENTS, L83_DIFFS, 140, dict(OPTS, day_night=DN83, anim_seconds=40.0, frames=80)),
]
