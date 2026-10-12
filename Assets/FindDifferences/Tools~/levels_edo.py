# -*- coding: utf-8 -*-
"""Edo Japan (1603-1868), paper-craft side views with an ukiyo-e flavour, full-bleed:
  Level89 日本桥     - Nihonbashi: a daimyo procession on the bridge, the fish market below, Fuji and the castle far off
  Level90 神奈川冲浪里 - the great wave curling over the boats, Fuji small in the trough
  Level91 歌舞伎小屋 - inside a kabuki theatre: stage, runway, musicians, audience boxes, paper lanterns
  Level92 两国花火   - fireworks over the Sumida at Ryogoku bridge; day / night
  Level93 东海道宿场 - a post town on the Tokaido with inns, travellers and a palanquin; clear -> rain
"""
import math
import random

from fdcore import CLEAR, E, H, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_el, drift_across, gy, layer, sky
from stylekit import day_night, star_field, window_glow
from weather import CLOUDY, SUNNY, WET, cloud, rain_layer
from levels_heian import GOLD, VERMILION, pine_jp, stone_lantern
from levels_europe import firework
from jp_kit import (HAIR, PLASTER, SKIN, TILE, ashigaru, castle_keep, chochin, ellipse_top, ishigaki, kimono, machiya, samurai, tile_roof)

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
PRUSSIAN = (40, 72, 120)


def fuji(c, x, base, w, h, snow=True, col=(90, 110, 150)):
    piece(c, Poly([(x - w, base), (x - w * 0.16, base - h), (x + w * 0.16, base - h), (x + w, base)]), col, shadow=LAYER)
    if snow:
        flat(c, Poly([(x - w * 0.16, base - h), (x + w * 0.16, base - h), (x + w * 0.36, base - h * 0.62), (x + w * 0.2, base - h * 0.7),
                       (x + w * 0.08, base - h * 0.58), (x - w * 0.06, base - h * 0.7), (x - w * 0.2, base - h * 0.6), (x - w * 0.36, base - h * 0.64)]),
             (250, 250, 252))


def kago(c, x, base, col=(150, 90, 60), bearer=(200, 170, 120)):
    flat(c, Thick(x - 70, base - 54, x + 70, base - 54, 4), (130, 100, 70))
    piece(c, [RRect(x - 26, base - 52, x + 26, base - 20, 4), Poly([(x - 30, base - 52), (x + 30, base - 52), (x, base - 64)])], col, border=1.2,
          shadow=PROP)
    flat(c, RRect(x - 18, base - 46, x + 18, base - 28, 2), lit(col, 0.7))
    for bx in (x - 58, x + 58):
        kimono(c, bx, base, bearer, h=0.95)


# =================================================================== Level 89 Nihonbashi
BRIDGE89 = (180, 720, 386, 300)


def l89_bg(c, d):
    sky(c, (170, 206, 236), (248, 236, 212), 300)
    fuji(c, 210, 270, 160, 140, snow="fuji" not in d)
    layer(c, 258, [(6, 0.01, 0.4)], (150, 176, 170))
    ishigaki(c, 720, 840, 262, 232, 10)
    castle_keep(c, 780, 234, w0=80, tiers=3, tier_h=22)
    rnd = random.Random(89)
    for row, y in enumerate((300, 330)):
        x = -20 + row * 30
        while x < 920:
            w = rnd.randint(50, 90)
            piece(c, RRect(x, y - 16, x + w, y + 12, 0), (196, 180, 150), shadow=None)
            tile_roof(c, x + 4, x + w - 4, y - 16, 10, flare=4)
            x += w + 6
    c.rect(0, 360, W, 480, (90, 140, 170))
    for y in range(372, 478, 12):
        for x in range((y * 11) % 64, 900, 64):
            flat(c, Thick(x, y, x + 24, y, 2), (120, 170, 196))
    # bridge with a daimyo procession
    x0, x1, base, top = BRIDGE89
    for x in range(x0 + 30, x1 - 20, 60):
        y = base - (base - top) * math.sin(math.pi * (x - x0) / (x1 - x0))
        flat(c, RRect(x - 4, y, x + 4, 440, 1), (110, 84, 64))
    n = 24
    arc = [(x0 + (x1 - x0) * k / n, base - (base - top) * math.sin(math.pi * k / n)) for k in range(n + 1)]
    piece(c, Poly(arc + [(x1, base + 10), (x0, base + 10)]), (170, 130, 90), border=1.5, shadow=PROP)
    rail = [(x, y - 16) for x, y in arc]
    flat(c, [Thick(rail[i][0], rail[i][1], rail[i + 1][0], rail[i + 1][1], 3) for i in range(n)], (150, 112, 76))
    for i, k in enumerate((2, 8, 16, 22)):
        x, y = rail[k]
        if not (i == 2 and "giboshi" in d):
            piece(c, [Circ(x, y - 5, 5), Poly([(x - 2, y - 8), (x + 2, y - 8), (x, y - 16)])], (196, 176, 110), shadow=None)
    for k in range(3, 22, 2):
        x, y = arc[k]
        if 10 <= k <= 13:
            continue
        ashigaru(c, x, y, (40, 50, 80), h=0.7, weapon="yari" if k % 4 == 1 else None)
        if k == 9:
            flat(c, [Ell(x + 6, y - 106, 6, 9)], (60, 120, 180) if "keyari" in d else (30, 30, 34))
    xm, ym = arc[12]
    flat(c, Thick(xm - 46, ym - 34, xm + 46, ym - 34, 4), (110, 80, 60))
    piece(c, [RRect(xm - 24, ym - 40, xm + 24, ym - 8, 3), Poly([(xm - 28, ym - 40), (xm + 28, ym - 40), (xm, ym - 52)])],
          (60, 90, 60) if "norimono" in d else (30, 26, 30), border=1.5, shadow=PROP)
    flat(c, Circ(xm, ym - 26, 5), GOLD)
    # fish market quay
    piece(c, RRect(-10, 470, 910, 612, 0), (196, 176, 140), shadow=LAYER)
    for x in range(0, 900, 44):
        flat(c, Thick(x, 470, x, 612, 1), (180, 160, 124))
    for i, x in enumerate((120, 330, 560, 780)):
        piece(c, RRect(x - 60, 500, x + 60, 536, 2), (150, 110, 70), border=1.2, shadow=PROP)
        flat(c, [Thick(x - 56, 536, x - 56, 560, 3), Thick(x + 56, 536, x + 56, 560, 3)], (110, 80, 56))
        nfish = 2 if (i == 1 and "tuna" in d) else 3
        for k in range(nfish):
            fx = x - 36 + k * 34
            piece(c, [Ell(fx, 496, 16, 6), Poly([(fx - 15, 496), (fx - 24, 489), (fx - 24, 503)])], (70, 90, 120), shadow=SMALL)
            flat(c, Ell(fx + 2, 498, 12, 2.5), (230, 230, 236))
    for x, band in ((230, (200, 50, 50)), (450, (240, 240, 240)), (680, (60, 90, 160))):
        hx, hy = kimono(c, x, 598, (150, 80, 50) if (x == 450 and "hachimaki" in d) else (60, 70, 100))
        flat(c, Thick(hx - 7, hy - 4, hx + 7, hy - 4, 2.5), band)
        flat(c, Thick(x - 30, 562, x + 30, 562, 2.5), (130, 96, 60))
        for px in (x - 30, x + 30):
            piece(c, Ell(px, 580, 12, 7), (170, 130, 80), border=1, shadow=SMALL)
    # a fishing boat unloading
    piece(c, Poly([(20, 448), (180, 448), (166, 466), (34, 466)]), (130, 96, 64), border=1.2, shadow=SMALL)
    if "boat" not in d:
        piece(c, ellipse_top(100, 450, 44, 16), (196, 176, 110), border=1, shadow=SMALL)
    kimono(c, 150, 450, (80, 90, 110), h=0.7)


L89_ELEMENTS = [
    cloud_el("cloud0", 440, 60, 0.7, 7), cloud_el("cloud1", 700, 90, 0.5, 5),
    bird_el("gull0", 500, 150, 9, col=(246, 246, 246), speed=16), bird_el("gull1", 528, 140, 7, col=(246, 246, 246), speed=16),
    E("flag", lambda c, m: (flat(c, Thick(700, 330, 700, 280, 2), (90, 70, 60)),
                            piece(c, Poly([(701, 282), (716, 282), (716, 314), (701, 314)]), (240, 236, 226), shadow=SMALL)),
      pivot=(700, 300), anim=dict(swingAngle=3, swingSpeed=0.6)),
]

L89_DIFFS = [
    ("fuji", 210, 150, 0),
    ("giboshi", 540, 290, 0),
    ("keyari", 388, 200, 0),
    ("norimono", 450, 280, 0),
    ("tuna", 364, 496, 0),
    ("hachimaki", 450, 580, 0),
    ("boat", 100, 440, 0),
]


# =================================================================== Level 90 the great wave
WAVE_C = (380, 200)


def great_wave(c):
    """Hokusai-like wave: a dark mound whose crest curls over to the right, foam claws on the lip."""
    mound = [(-20, 612), (-20, 330), (80, 262), (200, 218), (272, 204), (300, 262), (330, 336), (400, 424), (520, 500), (640, 560), (700, 612)]
    piece(c, Poly(mound), PRUSSIAN, border=2, border_col=(240, 236, 222), shadow=LAYER)
    cx, cy = WAVE_C
    outer = [(cx + 112 * math.cos(math.radians(a)), cy + 112 * math.sin(math.radians(a))) for a in range(180, 404, 8)]
    inner = [(cx + 64 * math.cos(math.radians(a)), cy + 60 * math.sin(math.radians(a))) for a in range(396, 176, -8)]
    piece(c, Poly(outer + inner), PRUSSIAN, border=2, border_col=(240, 236, 222), shadow=PROP)
    for a in range(200, 380, 22):
        r0, r1 = 74, 104
        flat(c, Thick(cx + r0 * math.cos(math.radians(a)), cy + r0 * math.sin(math.radians(a)), cx + r1 * math.cos(math.radians(a + 10)),
                      cy + r1 * math.sin(math.radians(a + 10)), 3), (80, 120, 170))
    for a in range(296, 404, 9):
        ra = math.radians(a)
        bx, by = cx + 112 * math.cos(ra), cy + 112 * math.sin(ra)
        tx, ty = cx + 132 * math.cos(ra + 0.08), cy + 132 * math.sin(ra + 0.08)
        flat(c, [Circ(bx, by, 6), Poly([(bx - 4 * math.sin(ra), by + 4 * math.cos(ra)), (bx + 4 * math.sin(ra), by - 4 * math.cos(ra)), (tx, ty)])],
             (246, 242, 230))
    for k in range(7):
        x = 40 + k * 60
        flat(c, Thick(x, 600, x + 60, 300 + k * 18, 3), (70, 110, 160))


def oshiokuri(x, y, hull, rowers, k=1.0):
    def d(c, m):
        hc = hull(m) if callable(hull) else hull
        n = rowers(m) if callable(rowers) else rowers
        piece(c, Poly([(x - 100 * k, y - 12 * k), (x + 100 * k, y - 20 * k), (x + 90 * k, y), (x - 90 * k, y + 2 * k)]), hc, border=1.5, shadow=SMALL)
        for i in range(n):
            px = x - 70 * k + i * 22 * k
            piece(c, [Ell(px, y - 16 * k, 7 * k, 6 * k), Circ(px + 4 * k, y - 22 * k, 4 * k)], (60, 70, 110), shadow=None)
            flat(c, Circ(px + 4 * k, y - 23 * k, 2.6 * k), SKIN)
    return d


def l90_bg(c, d):
    sky(c, (226, 218, 196), (236, 228, 206), 400)
    if "cloud" not in d:
        flat(c, Poly([(560, 120), (660, 90), (800, 96), (900, 120), (860, 140), (600, 140)]), (196, 190, 176))
    piece(c, RRect(30, 30, 110, 120, 1), (236, 226, 200), border=2, border_col=(90, 80, 70), shadow=SMALL)
    flat(c, RRect(40, 40, 100, 110, 0), (196, 184, 150) if "cartouche" in d else (150, 170, 196))
    for k in range(4):
        flat(c, Thick(56 + k * 10, 48, 56 + k * 10, 102, 1.4), INK)
    flat(c, RRect(118, 50, 136, 68, 1), (60, 130, 80) if "seal" in d else (200, 50, 50))
    c.rect(0, 396, W, H, (60, 100, 150))
    fuji(c, 610, 470, 76, 64, snow="fuji" not in d, col=(80, 100, 140))
    great_wave(c)
    piece(c, Poly([(640, 612), (680, 520), (740, 484), (800, 470), (860, 456), (920, 470), (920, 612)]), PRUSSIAN, border=2,
          border_col=(240, 236, 222), shadow=LAYER)
    if "foam" not in d:
        for x in range(720, 910, 20):
            flat(c, Circ(x, 476 - (x - 720) * 0.08 + (x % 3) * 4, 5), (246, 242, 230))
    for y in range(520, 600, 14):
        flat(c, Thick(0, y, 900, y + 3 * math.sin(y), 2.5), (90, 130, 176))


L90_ELEMENTS = [
    E("boat1", oshiokuri(330, 470, lambda m: (150, 150, 160) if m else (236, 200, 110), 7), pivot=(330, 470), variant=True,
      anim=dict(bobAmplitude=(0, 6), bobSpeed=0.25, swingAngle=6, swingSpeed=0.25)),
    E("boat2", oshiokuri(790, 470, (236, 200, 110), lambda m: 5 if m else 6, 0.9), pivot=(790, 470), variant=True,
      anim=dict(bobAmplitude=(0, 5), bobSpeed=0.22, swingAngle=-5, swingSpeed=0.22, phase=0.4)),
] + [E("spray%d" % i, (lambda x, y: lambda c, m: flat(c, Circ(x, y, 3.5), (250, 248, 240)))(x, y),
       anim=dict(driftVelocity=(10, 30), driftLength=60, driftFade=True, phase=i / 8)) for i, (x, y) in enumerate(
        ((470, 110), (490, 150), (500, 200), (440, 96), (510, 240), (420, 92), (480, 270), (500, 120)))] + [
    bird_el("bird0", 300, 50, 8, col=(80, 80, 90), speed=12)]

L90_DIFFS = [
    ("cloud", 730, 116, 0),
    ("cartouche", 70, 76, 0),
    ("seal", 127, 59, 0),
    ("fuji", 610, 420, 0),
    ("foam", 810, 466, 0),
    ("hull", 330, 460, 0),
    ("rowers", 826, 450, 0),
]


# =================================================================== Level 91 inside a kabuki theatre
LANT91 = list(range(40, 900, 70))
LANT_DIFF91 = 7


def l91_bg(c, d):
    c.rect(0, 0, W, H, (120, 90, 64))
    for x in range(0, 900, 40):
        flat(c, Thick(x, 0, x, 60, 2), (100, 74, 52))
    piece(c, RRect(-10, 50, 910, 66, 0), (90, 66, 46), shadow=SMALL)
    # stage with pine backdrop
    piece(c, RRect(360, 100, 910, 420, 0), (200, 160, 80), border=2, shadow=PROP)
    for y in range(110, 400, 30):
        flat(c, Thick(360, y, 910, y, 1), (186, 146, 70))
    piece(c, [Thick(640, 400, 630, 260, 14), Thick(630, 260, 600, 200, 9)] + ([] if "pine" in d else [Thick(630, 280, 720, 240, 7)]),
          (110, 80, 60), shadow=SMALL)
    pads = [(560, 200, 60), (650, 170, 70), (760, 220, 60)] + ([] if "pine" in d else [(740, 236, 50)])
    piece(c, [Ell(x, y, r, r * 0.38) for x, y, r in pads], (60, 120, 80), border=1.2, shadow=PROP)
    piece(c, RRect(360, 400, 910, 430, 0), (176, 136, 90), border=1.5, shadow=PROP)
    # musicians on the dais
    piece(c, RRect(700, 300, 900, 330, 1), (200, 60, 50), shadow=SMALL)
    for x in (720, 760, 800, 840, 880):
        kimono(c, x, 300, (40, 40, 50), h=0.7)
    # actors: aragoto hero (kumadori make-up) and an onnagata with a fan
    hx, hy = kimono(c, 480, 402, (200, 40, 40), h=1.4, obi=(240, 240, 240))
    flat(c, [Thick(hx - 8, hy - 2, hx + 8, hy - 2, 2), Thick(hx - 6, hy + 4, hx + 4, hy + 2, 2)], (60, 90, 200) if "kumadori" in d else (220, 40, 40))
    flat(c, [Circ(hx - 1, hy - 12, 9)], HAIR)
    flat(c, [Thick(470, 370, 440, 340, 4), Thick(492, 370, 528, 344, 4)], (200, 40, 40))
    hx, hy = kimono(c, 580, 404, (240, 170, 200), h=1.3, hair="woman", obi=(200, 60, 80))
    piece(c, Poly([(hx + 10, hy + 20), (hx + 34, hy - 4), (hx + 36, hy + 18)]), (80, 160, 220) if "fan" in d else (240, 200, 60), border=1,
          shadow=SMALL)
    # curtain (jo-shiki-maku) partly drawn at the left of the stage
    stripes = [(30, 30, 34), (200, 110, 50), (40, 90, 60)]
    for k in range(6):
        col = (200, 110, 50) if (k == 5 and "curtain" in d) else stripes[k % 3]
        piece(c, RRect(360 + k * 14, 100, 374 + k * 14, 420, 0), col, shadow=None)
    # theatre signboard (kanban) hanging on the left wall: the play's title in brush strokes
    flat(c, [Thick(80, 66, 80, 110, 2), Thick(160, 66, 160, 110, 2)], (60, 44, 34))
    board = (60, 110, 170) if "kanban" in d else (236, 226, 200)
    piece(c, RRect(50, 110, 190, 320, 3), board, border=2, shadow=PROP)
    flat(c, RRect(58, 118, 182, 312, 2), lit(board, 0.94))
    for k, x in enumerate((90, 120, 150)):
        for j in range(5):
            y = 134 + j * 34 + (k % 2) * 10
            flat(c, [Thick(x - 8, y, x + 8, y + 4, 3), Thick(x, y - 6, x - 2, y + 16, 3)], (40, 30, 30) if "kanban" not in d else (240, 236, 226))
    # runway (hanamichi) and audience boxes
    piece(c, RRect(-10, 430, 380, 452, 0), (176, 136, 90), border=1.2, shadow=PROP)
    kimono(c, 200, 432, (60, 60, 120), h=1.2)
    c.rect(0, 452, W, H, (150, 112, 76))
    rnd = random.Random(91)
    for row, y in enumerate((500, 552, 604)):
        for x in range(-20 + row * 20, 920, 120):
            flat(c, [Thick(x, y - 30, x + 110, y - 30, 3), Thick(x, y - 30, x, y, 3)], (110, 80, 56))
            for k in range(3):
                px = x + 22 + k * 32
                col = rnd.choice(((60, 70, 110), (150, 60, 80), (90, 120, 80), (200, 150, 80), (110, 70, 110)))
                piece(c, [Ell(px, y - 6, 12, 10), Circ(px, y - 20, 7)], col, shadow=SMALL)
                flat(c, Circ(px, y - 20, 6), SKIN)
                flat(c, Ell(px - 1, y - 24, 6, 3), HAIR)
    if "parasol" not in d:                                    # a spectator holding up a parasol (blocking the view)
        flat(c, Thick(770, 552, 776, 470, 2), (90, 70, 50))
        piece(c, Poly([(728, 486), (776, 452), (824, 486), (812, 492), (794, 486), (776, 492), (758, 486), (740, 492)]), (220, 80, 70),
              border=1.5, shadow=SMALL)
        for k in range(-2, 3):
            flat(c, Thick(776, 454, 776 + k * 22, 488, 1), (180, 60, 50))
    if "bento" not in d:
        piece(c, RRect(290, 540, 314, 552, 2), (200, 40, 40), border=1, shadow=SMALL)
        flat(c, [Circ(296, 544, 2), Circ(304, 544, 2)], (250, 250, 250))
    hx, hy = kimono(c, 880, 600, (40, 40, 50))
    if "hyoshigi" not in d:
        flat(c, [Thick(hx + 6, hy + 16, hx + 20, hy + 6, 3), Thick(hx + 8, hy + 20, hx + 22, hy + 10, 3)], (220, 190, 140))


L91_ELEMENTS = [
    E("lanterns", lambda c, m: [chochin(c, x, 70, (240, 236, 226), s=1.3) or flat(c, Circ(x, 83, 4),
                                                                                   ((60, 120, 200) if (m and i == LANT_DIFF91) else (200, 40, 40)))
                                for i, x in enumerate(LANT91)],
      pivot=(450, 64), variant=True, anim=dict(swingAngle=0.6, swingSpeed=0.3)),
    E("mie", lambda c, m: flat(c, Thick(500, 340, 528, 330, 3), (240, 236, 226)), pivot=(500, 340), anim=dict(swingAngle=10, swingSpeed=0.4)),
]

L91_DIFFS = [
    ("pine", 720, 240, 0),
    ("kumadori", 481, 360, 0),
    ("fan", 610, 362, 0),
    ("curtain", 437, 260, 0),
    ("bento", 302, 546, 0),
    ("hyoshigi", 900, 566, 0),
    ("mon", LANT91[LANT_DIFF91], 83, 0),
    ("kanban", 120, 215, 0),
    ("parasol", 776, 476, 0),
]


# =================================================================== Level 92 fireworks at Ryogoku (day / night)
DN92 = day_night(40.0, tint=(0.26, 0.28, 0.56))
BOATS92 = [(260, 470, (200, 60, 50)), (620, 500, (60, 80, 140))]


def yakatabune(x, y, roof, lant, k=1.0):
    def d(c, m):
        lc = lant(m) if callable(lant) else lant
        piece(c, Poly([(x - 90 * k, y - 10 * k), (x + 90 * k, y - 14 * k), (x + 78 * k, y + 6 * k), (x - 80 * k, y + 6 * k)]), (110, 76, 50), border=1.5,
              shadow=SMALL)
        for px in range(int(x - 60 * k), int(x + 66 * k), int(30 * k)):
            flat(c, Thick(px, y - 10 * k, px, y - 46 * k, 2), (90, 64, 44))
        piece(c, Poly([(x - 72 * k, y - 46 * k), (x + 72 * k, y - 46 * k), (x + 60 * k, y - 60 * k), (x - 60 * k, y - 60 * k)]), roof, border=1.2,
              shadow=SMALL)
        for i, px in enumerate(range(int(x - 50 * k), int(x + 60 * k), int(30 * k))):
            chochin(c, px, y - 46 * k, lc, s=0.7 * k)
        for px in (x - 40 * k, x, x + 40 * k):
            kimono(c, px, y - 10 * k, (60, 70, 110), h=0.6 * k, hair="woman" if px == x else "man")
    return d


def l92_bg(c, d):
    sky(c, (150, 186, 220), (240, 214, 190), 320)
    layer(c, 250, [(8, 0.01, 0.4)], (130, 150, 160))
    rnd = random.Random(92)
    x = -10
    while x < 920:
        w = rnd.randint(40, 80)
        piece(c, RRect(x, 262, x + w, 290, 0), (170, 160, 150), shadow=None)
        tile_roof(c, x + 4, x + w - 4, 262, 8, flare=3)
        x += w + 4
    c.rect(0, 290, W, 540, (60, 100, 130))
    for y in range(300, 538, 12):
        for xx in range((y * 13) % 66, 900, 66):
            flat(c, Thick(xx, y, xx + 24, y, 2), (90, 130, 160))
    # Ryogoku bridge with spectators
    for xx in range(-10, 920, 40):
        flat(c, Thick(xx, 330, xx, 380, 3), (100, 76, 56))
    piece(c, RRect(-10, 316, 910, 330, 0), (150, 114, 80), border=1.2, shadow=PROP)
    flat(c, Thick(-10, 306, 910, 306, 2.5), (130, 98, 70))
    for xx in range(0, 900, 14):
        col = rnd.choice(((60, 60, 90), (150, 60, 80), (90, 110, 80), (200, 160, 100)))
        piece(c, [Ell(xx, 312, 5, 7), Circ(xx, 302, 4)], col, shadow=None)
    if "lamp" not in d:
        chochin(c, 450, 296, (240, 236, 226), s=1.0)
    # teahouses on the left bank with noren
    piece(c, Poly([(-10, 600), (-10, 470), (230, 520), (260, 600)]), (130, 110, 80), shadow=LAYER)
    for i, x0 in enumerate((-10, 90)):
        machiya(c, x0, x0 + 100, 520 + i * 10, 110, (160, 120, 80), ((200, 60, 60) if "noren" in d else (40, 60, 110)) if i == 1 else (120, 60, 40),
                lantern=(220, 60, 50))
    piece(c, RRect(200, 470, 218, 520, 1), (240, 120, 80) if "sign" in d else (240, 230, 200), border=1, shadow=SMALL)
    flat(c, Thick(209, 476, 209, 512, 2), (40, 40, 60))
    # near bank with spectators
    piece(c, hill_strip(540, [(4, 0.012, 0.4)]), (120, 110, 84), shadow=LAYER)
    pine_jp(c, 860, 600, 1.4)
    for x, col in ((360, (60, 90, 160)), (420, (220, 120, 150)), (500, (60, 60, 70)), (560, (230, 200, 120)), (640, (120, 60, 100))):
        hx, hy = kimono(c, x, 598, (100, 160, 200) if ("yukata" in d and x == 420) else col, hair="woman" if x in (420, 560) else "man")
        if x == 560:
            piece(c, Circ(hx + 12, hy + 8, 7), (220, 60, 60) if "uchiwa" in d else (60, 120, 200), border=1, shadow=SMALL)
            flat(c, Thick(hx + 12, hy + 14, hx + 8, hy + 22, 1.5), (110, 80, 60))


L92_ELEMENTS = [
    E("moon", lambda c, m: (soft_union(c, [Circ(800, 70, 26)], (255, 250, 220), 0.35, spread=16),
                            piece(c, Circ(800, 70, 20), (252, 246, 220), border=2, shadow=PROP)), daynight="night"),
    star_field("stars", 92, 30, 160, avoid=[(760, 30, 840, 110)]),
    cloud_el("cloud0", 300, 60, 0.7, 6, daynight="day"),
    E("boatA", yakatabune(BOATS92[0][0], BOATS92[0][1], BOATS92[0][2], lambda m: (240, 236, 226) if m else (220, 60, 50)),
      pivot=(BOATS92[0][0], BOATS92[0][1]), variant=True, anim=dict(bobAmplitude=(0, 2), bobSpeed=0.3, swingAngle=1, swingSpeed=0.2)),
    E("boatB", yakatabune(BOATS92[1][0], BOATS92[1][1], BOATS92[1][2], (220, 60, 50), 0.9),
      pivot=(BOATS92[1][0], BOATS92[1][1]), anim=dict(bobAmplitude=(0, 2), bobSpeed=0.27, swingAngle=1, swingSpeed=0.18, phase=0.4)),
    E("boatC", lambda c, m: yakatabune(470, 420, (40, 40, 46) if m else (150, 110, 70), (220, 60, 50), 0.6)(c, m), pivot=(470, 420), variant=True,
      anim=dict(bobAmplitude=(0, 1.5), bobSpeed=0.33, phase=0.2)),
    E("lantern_glow", lambda c, m: soft_union(c, [Circ(x, 498, 5) for x in range(int(BOATS92[0][0] - 50), int(BOATS92[0][0] + 60), 30)] +
                                             [Circ(450, 306, 6)], (255, 200, 110), 0.55, spread=16), daynight="night"),
] + [E("firework%d" % i, firework(x, y, col, r), pivot=(x, y), daynight="night",
       anim=dict(blinkInterval=2.6 + i * 0.3, blinkDuration=1.1, phase=i * 0.27, pulse=0.15, scaleSpeed=0.8))
     for i, (x, y, col, r) in enumerate(((240, 90, (255, 130, 150), 40), (460, 60, (140, 220, 255), 52), (680, 120, (255, 220, 110), 38),
                                         (580, 180, (200, 150, 255), 30)))]

L92_DIFFS = [
    ("boatlant", BOATS92[0][0], BOATS92[0][1] - 36, 0),
    ("roof", 470, 386, 0),
    ("lamp", 450, 306, 0),
    ("noren", 140, 485, 0),
    ("sign", 209, 494, 0),
    ("yukata", 420, 576, 0),
    ("uchiwa", 573, 566, 0),
]


# =================================================================== Level 93 Tokaido post town (clear -> rain)
STEPS93 = [(CLEAR, 8), (OVERCAST, 5), (RAIN, 10)]
WEATHER93 = dict(steps=STEPS93, blend=3.0, tints={OVERCAST: (0.86, 0.88, 0.92), RAIN: (0.72, 0.76, 0.84)})


def mino_traveller(c, x, base, hat=(200, 176, 120), h=1.0):
    hx, hy = kimono(c, x, base, (90, 90, 110), h=h)
    piece(c, Poly([(x - 14 * h, base - 8 * h), (x + 14 * h, base - 8 * h), (x + 8 * h, base - 34 * h), (x - 8 * h, base - 34 * h)]), (176, 150, 90),
          shadow=SMALL)
    for k in range(5):
        flat(c, Thick(x - 12 * h + k * 6 * h, base - 10 * h, x - 7 * h + k * 4 * h, base - 32 * h, 1), (150, 126, 70))
    flat(c, Poly([(hx - 15 * h, hy - 2 * h), (hx + 15 * h, hy - 2 * h), (hx, hy - 13 * h)]), hat)
    flat(c, Thick(x + 12 * h, base, x + 16 * h, base - 50 * h, 1.6), (110, 80, 60))
    return hx, hy


def l93_bg(c, d):
    sky(c, (170, 204, 230), (240, 232, 214), 320)
    fuji(c, 650, 260, 150, 120)
    layer(c, 230, [(26, 0.007, 0.4), (10, 0.02, 1.2)], (130, 150, 150))
    layer(c, 270, [(14, 0.012, 1.0)], (110, 140, 110))
    for x in range(400, 920, 60):
        pine_jp(c, x, gy(270, [(14, 0.012, 1.0)], x) + 40, 0.6)
    # inns
    for i, (x0, w) in enumerate(((-10, 110), (100, 110), (210, 110), (320, 100))):
        lant = ((240, 236, 226) if "inn_lantern" in d else (220, 60, 50)) if i == 1 else (220, 60, 50)
        machiya(c, x0, x0 + w, 440, 140, (160, 120, 80), (60, 70, 110), sign=((60, 120, 80) if "sign" in d else (240, 230, 200)) if i == 2 else None,
                lantern=lant)
    piece(c, RRect(-10, 440, 910, 612, 0), (200, 180, 140), shadow=LAYER)
    for y in range(452, 600, 18):
        flat(c, Thick(0, y, 900, y, 1), (186, 164, 124))
    # inn maids calling, travellers, palanquin, packhorse
    kimono(c, 160, 470, (150, 60, 80), hair="woman")
    kimono(c, 270, 470, (60, 90, 140), hair="woman")
    kago(c, 470, 580, col=(60, 90, 140) if "kago" in d else (150, 90, 60))
    hx, hy = mino_traveller(c, 640, 586, hat=(110, 110, 120) if "hat" in d else (200, 176, 120))
    mino_traveller(c, 700, 590)
    for lx in (-22, -12, 14, 24):
        flat(c, RRect(820 + lx - 3, 560, 820 + lx + 3, 596, 1), (110, 76, 50))
    piece(c, [Ell(820, 552, 32, 14), Poly([(846, 548), (860, 518), (868, 522), (856, 552)]), Ell(868, 520, 11, 7)], (150, 110, 70), border=1.5,
          shadow=PROP)
    piece(c, [RRect(796, 520, 844, 540, 3)], (60, 100, 160) if "load" in d else (200, 180, 140), border=1, shadow=SMALL)
    kimono(c, 760, 596, (80, 70, 60), umbrella=(200, 60, 60) if "umbrella" in d else (70, 70, 90))
    pine_jp(c, 380, 450, 1.0)
    if "pine" not in d:
        pine_jp(c, 880, 450, 0.9)


L93_ELEMENTS = [
    E("sun", lambda c, m: (piece(c, Poly(star_pts(820, 70, 36, 27, points=12)), (255, 190, 80), shadow=PROP),
                           piece(c, Circ(820, 70, 22), (255, 222, 95), border=2, shadow=PROP)), weather=SUNNY),
    cloud("cloudA", 200, 70, 0.9, (252, 252, 248), W_(CLEAR, OVERCAST), anim=dict(bobAmplitude=(26, 0), bobSpeed=0.02)),
    cloud("cloudB", 480, 60, 1.0, (196, 202, 214), CLOUDY, anim=dict(bobAmplitude=(-22, 0), bobSpeed=0.025)),
    cloud("cloudC", 760, 110, 0.9, (186, 192, 206), CLOUDY),
    rain_layer("rain", 93, 46, 26, 1.8, 0.55, 300),
    bird_el("bird0", 300, 140, 8, speed=16, weather=SUNNY),
    E("horse_tail", lambda c, m: flat(c, Thick(788, 546, 782, 570, 3), (60, 44, 34)), pivot=(788, 546), anim=dict(swingAngle=14, swingSpeed=0.5)),
]

L93_DIFFS = [
    ("inn_lantern", 112, 382, 0),
    ("sign", 308, 386, 0),
    ("kago", 470, 544, 0),
    ("hat", 641, 534, 0),
    ("load", 820, 530, 0),
    ("umbrella", 771, 532, 0),
    ("pine", 880, 400, 0),
]

LEVELS = [
    ("Level89", "日本桥", l89_bg, L89_ELEMENTS, L89_DIFFS, 140, OPTS),
    ("Level90", "神奈川冲浪里", l90_bg, L90_ELEMENTS, L90_DIFFS, 140, OPTS),
    ("Level91", "歌舞伎小屋", l91_bg, L91_ELEMENTS, L91_DIFFS, 140, OPTS),
    ("Level92", "两国花火", l92_bg, L92_ELEMENTS, L92_DIFFS, 140, dict(OPTS, day_night=DN92, anim_seconds=40.0, frames=80)),
    ("Level93", "东海道宿场", l93_bg, L93_ELEMENTS, L93_DIFFS, 140, dict(OPTS, weather=WEATHER93, anim_seconds=23.0, frames=46)),
]
