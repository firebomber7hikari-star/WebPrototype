# -*- coding: utf-8 -*-
"""Portrait paintings (paper-craft, front view of a gallery wall):
  Level129 肖像画廊 - a gallery of original old-master style portraits (a lady in a pearl-trimmed gown, a cavalier in a
  plumed hat, a girl with a lamb), a painter at work on his easel and visitors; 4 large differences >= 135 px apart
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, glow_el
from fills import wallpaper_diamonds
from stylekit import figure

SKIN = (246, 216, 190)
GOLD = (214, 176, 92)
GOLD_D = (172, 134, 62)


def frame(c, x0, y0, x1, y1, canvas_col, k=10):
    """Gilded frame with an inner bevel; returns the canvas rect."""
    piece(c, RRect(x0, y0, x1, y1, 3), GOLD, border=2, shadow=PROP)
    flat(c, [Thick(x0 + 4, y0 + 4, x1 - 4, y0 + 4, 2), Thick(x0 + 4, y0 + 4, x0 + 4, y1 - 4, 2)], lit(GOLD, 1.18))
    flat(c, [Thick(x0 + 4, y1 - 4, x1 - 4, y1 - 4, 2), Thick(x1 - 4, y0 + 4, x1 - 4, y1 - 4, 2)], GOLD_D)
    for cx, cy in ((x0 + 6, y0 + 6), (x1 - 6, y0 + 6), (x0 + 6, y1 - 6), (x1 - 6, y1 - 6)):
        flat(c, Circ(cx, cy, 4), lit(GOLD, 1.2))
    r = (x0 + k, y0 + k, x1 - k, y1 - k)
    flat(c, RRect(*r, 1), GOLD_D)
    r = (r[0] + 3, r[1] + 3, r[2] - 3, r[3] - 3)
    flat(c, RRect(*r, 1), canvas_col)
    return r


def bust(c, cx, base, s, dress, hair=(90, 60, 40), skin=SKIN, hair_style="long", collar=None):
    """Head-and-shoulders sitter, facing slightly left; base = bottom of the canvas."""
    flat(c, Poly([(cx - 62 * s, base), (cx + 62 * s, base), (cx + 50 * s, base - 46 * s), (cx + 22 * s, base - 62 * s), (cx - 22 * s, base - 62 * s),
                  (cx - 50 * s, base - 46 * s)]), dress)
    flat(c, Poly([(cx - 10 * s, base - 64 * s), (cx + 10 * s, base - 64 * s), (cx + 8 * s, base - 48 * s), (cx - 8 * s, base - 48 * s)]), skin)
    if hair_style == "long":
        flat(c, [Ell(cx, base - 92 * s, 30 * s, 36 * s), RRect(cx - 30 * s, base - 96 * s, cx + 30 * s, base - 50 * s, 10 * s)], hair)
    flat(c, Ell(cx - 2 * s, base - 90 * s, 22 * s, 28 * s), skin)
    if hair_style == "long":
        flat(c, Poly([(cx - 24 * s, base - 96 * s), (cx - 16 * s, base - 120 * s), (cx + 14 * s, base - 120 * s), (cx + 24 * s, base - 96 * s),
                      (cx + 6 * s, base - 108 * s), (cx - 8 * s, base - 104 * s)]), hair)
    elif hair_style == "short":
        flat(c, Poly([(cx - 24 * s, base - 92 * s), (cx - 20 * s, base - 116 * s), (cx + 18 * s, base - 118 * s), (cx + 22 * s, base - 92 * s),
                      (cx + 10 * s, base - 106 * s), (cx - 10 * s, base - 104 * s)]), hair)
    for ex in (-10, 6):
        flat(c, Ell(cx + ex * s, base - 92 * s, 3 * s, 2.2 * s), (250, 250, 250))
        flat(c, Circ(cx + ex * s - 1 * s, base - 92 * s, 1.6 * s), (60, 44, 40))
    flat(c, Thick(cx - 3 * s, base - 88 * s, cx - 5 * s, base - 80 * s, 1.4 * s), lit(skin, 0.86))
    flat(c, Thick(cx - 8 * s, base - 72 * s, cx + 2 * s, base - 72 * s, 2 * s), (200, 110, 110))
    flat(c, [Circ(cx - 14 * s, base - 78 * s, 4 * s), Circ(cx + 10 * s, base - 78 * s, 4 * s)], lit((240, 170, 160), 1.0))
    if collar == "ruff":
        flat(c, [Ell(cx - 2 * s, base - 60 * s, 32 * s, 9 * s)], (250, 248, 240))
        for k in range(-3, 4):
            flat(c, Thick(cx + k * 8 * s, base - 66 * s, cx + k * 8 * s, base - 54 * s, 1 * s), (220, 216, 206))
    elif collar == "pearls":
        for k in range(-5, 6):
            flat(c, Circ(cx + k * 5 * s, base - 56 * s + abs(k) * -1.4 * s, 2.4 * s), (250, 246, 236))


def l129_bg(c, d):
    # wall: damask wallpaper above a wooden wainscot
    c.rect(0, 0, W, 620, (150, 64, 66))
    wallpaper_diamonds(c, (0, 0, W, 400), (150, 64, 66), (136, 54, 58), s=30)
    piece(c, RRect(-10, 396, W + 10, 440, 0), (120, 78, 56), shadow=(0, 3, 6, 0.3))
    for x in range(-10, W, 60):
        flat(c, RRect(x + 6, 404, x + 54, 434, 2), lit((120, 78, 56), 1.1))
    flat(c, Thick(0, 18, W, 18, 6), GOLD_D)                       # picture rail
    # parquet floor
    piece(c, RRect(-10, 440, W + 10, 620, 0), (178, 132, 86), shadow=(0, -2, 6, 0.3))
    for i, y in enumerate(range(440, 620, 18)):
        flat(c, Thick(0, y, W, y, 1.2), (156, 112, 70))
        for x in range(-40 + (i % 2) * 30, W, 60):
            flat(c, Thick(x, y, x, y + 18, 1.2), (156, 112, 70))

    # 1) the lady in a gown (gown colour changes)
    r = frame(c, 40, 46, 210, 280, (54, 62, 56))
    soft_union(c, [Ell(125, 140, 60, 70)], (110, 120, 96), 0.5, spread=30)
    bust(c, 128, r[3], 1.18, (70, 120, 170) if "gown" in d else (150, 40, 60), hair=(90, 56, 36), collar="pearls")
    # 2) the cavalier in a plumed hat (hat missing in B)
    r = frame(c, 320, 30, 580, 300, (70, 60, 48), k=12)
    soft_union(c, [Ell(450, 150, 90, 90)], (126, 104, 74), 0.5, spread=40)
    bust(c, 452, r[3], 1.6, (40, 44, 60), hair=(70, 46, 30), hair_style="short", collar="ruff")
    flat(c, [Thick(426, r[3] - 54, 476, r[3] - 20, 7), Thick(476, r[3] - 54, 426, r[3] - 20, 7)], (190, 150, 70))     # sash
    if "hat" not in d:
        hy = r[3] - 1.6 * 116
        flat(c, Ell(452, hy + 6, 74, 14), (36, 30, 34))
        flat(c, [RRect(412, hy - 44, 494, hy + 6, 14)], (36, 30, 34))
        flat(c, Poly([(470, hy - 30), (540, hy - 70), (556, hy - 56), (500, hy - 18)]), (250, 244, 232))
        flat(c, Thick(472, hy - 32, 548, hy - 64, 1.6), (220, 210, 196))
    # 3) the girl with a lamb (the lamb is gone in B)
    r = frame(c, 690, 46, 860, 280, (80, 110, 150))
    flat(c, Poly([(r[0], r[3] - 30), (r[0] + 40, r[3] - 50), (r[0] + 90, r[3] - 38), (r[2], r[3] - 56), (r[2], r[3]), (r[0], r[3])]), (90, 120, 80))
    bust(c, 768, r[3], 1.1, (240, 236, 224), hair=(200, 160, 90), hair_style="long")
    if "lamb" not in d:
        flat(c, [Ell(812, r[3] - 30, 32, 22), Circ(820, r[3] - 54, 14), Circ(838, r[3] - 48, 12)], (250, 248, 240))
        flat(c, [Ell(842, r[3] - 48, 6, 4)], (236, 200, 190))
        flat(c, [Circ(836, r[3] - 52, 1.8)], INK)
    # small oval portraits between the big ones
    for x, col in ((265, (120, 150, 110)), (635, (150, 120, 160))):
        piece(c, Ell(x, 130, 34, 44), GOLD, border=2, shadow=PROP)
        flat(c, Ell(x, 130, 26, 36), col)
        flat(c, [Ell(x, 160, 20, 12), Ell(x, 126, 11, 14)], (60, 50, 60))
        flat(c, Ell(x, 126, 9, 12), SKIN)
    # brass name plates
    for x in (125, 450, 775):
        piece(c, RRect(x - 34, 306, x + 34, 322, 3), (220, 190, 110), border=1, shadow=SMALL)
        flat(c, [Thick(x - 24, 312, x + 24, 312, 1.4), Thick(x - 18, 317, x + 18, 317, 1.4)], (150, 120, 60))
    # 4) the painter's easel: his own portrait in progress (the sitter's cloak changes colour)
    for a, b in (((300, 600), (338, 360)), ((400, 600), (362, 360)), ((350, 610), (350, 380))):
        piece(c, Thick(a[0], a[1], b[0], b[1], 5), (140, 96, 60), shadow=SMALL)
    piece(c, RRect(270, 380, 430, 500, 2), (250, 246, 236), border=2, shadow=PROP)
    flat(c, RRect(276, 386, 424, 494, 1), (210, 196, 170))
    bust(c, 352, 494, 0.8, (200, 150, 50) if "cloak" in d else (60, 110, 80), hair=(70, 50, 40), hair_style="short")
    piece(c, RRect(266, 500, 434, 510, 2), (140, 96, 60), shadow=SMALL)
    # the painter himself (beret), palette in hand
    figure(c, 486, 600, (90, 90, 130), h=2.0, hat=None)
    flat(c, Ell(490, 504, 16, 7), (60, 50, 60))                          # beret
    piece(c, [Ell(452, 540, 22, 14)], (220, 190, 140), border=1.2, shadow=SMALL)
    for k, col in enumerate(((220, 60, 60), (60, 120, 210), (250, 210, 60), (70, 160, 90))):
        flat(c, Circ(442 + k * 8, 536 + (k % 2) * 6, 3.4), col)
    # visitors on the right
    figure(c, 700, 600, (120, 70, 120), h=2.1, hat=(60, 50, 60))
    figure(c, 790, 604, (70, 110, 90), h=2.3)
    piece(c, Thick(820, 520, 850, 600, 3), (60, 50, 50), shadow=SMALL)             # walking stick
    # velvet rope + stanchions in front of the wall
    for x in (40, 230):
        piece(c, [RRect(x - 4, 470, x + 4, 560, 2), Ell(x, 562, 14, 5), Circ(x, 466, 7)], (210, 180, 90), border=1.2, shadow=SMALL)
    pts = [(40 + k * 19, 476 + 20 * math.sin(math.pi * k / 10)) for k in range(11)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 5) for i in range(10)], (150, 30, 50))
    # bench
    piece(c, [RRect(560, 520, 660, 534, 3), RRect(566, 534, 576, 580, 2), RRect(644, 534, 654, 580, 2)], (110, 70, 50), border=1.5, shadow=PROP)


def l129_brush(c, m):
    piece(c, [Thick(470, 560, 440, 520, 3), Thick(440, 520, 432, 510, 4)], (140, 100, 60), border=1, shadow=SMALL)
    flat(c, Circ(431, 508, 3), (220, 60, 60))


def l129_lights(c, m):
    for x in (125, 450, 775):
        soft_union(c, [Ell(x, 40, 70, 18)], (255, 236, 190), 0.28, spread=30)


L129_ELEMENTS = [
    E("lights", l129_lights, daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=0.25)),
    E("brush", l129_brush, pivot=(470, 560), anim=dict(swingAngle=10, swingSpeed=0.8)),
    E("visitor", lambda c, m: figure(c, 610, 590, (200, 140, 70), h=1.6), pivot=(610, 590),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.6)),
]

L129_DIFFS = [
    ("gown", 128, 240, 0),
    ("hat", 470, 70, 0),
    ("lamb", 822, 230, 0),
    ("cloak", 352, 470, 0),
]

LEVELS = [
    ("Level129", "肖像画廊", l129_bg, L129_ELEMENTS, L129_DIFFS, 140, dict(post=paper_post, anim_seconds=12.0, frames=48)),
]
