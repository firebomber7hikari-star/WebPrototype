# -*- coding: utf-8 -*-
"""Street-fighting-game style stages (original fighters, no franchise characters) and the Age of Discovery, paper-craft side views:
  Level119 夜市擂台 - a night-market stage: crowd behind the rope, lanterns, bicycles, chickens; two fighters and a HUD
  Level120 黄昏码头 - a dockside stage at sunset: cargo ship, crane, crates; a wrestler against a karateka
  Level121 里斯本出航 - caravels leaving Lisbon: the river tower, navigators with astrolabe and globe, the royal banner
  Level122 新大陆登陆 - landing on a tropical shore: the ship at anchor, the longboat, a flag planted on the beach
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, barrel, bird_el, cloud_el, crate, drift_across, palm, person, sky, smoke_el
from levels_europe import arch, ellipse_top, lady, tricorne
from cn_kit import lantern_cn
from levels_akiba import modern, sign_box

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)
TAN = (210, 160, 120)
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg",
       "K": "fegbc", "O": "abcdef"}


def seg_text(c, x, y, h, text, col, width=3.0):
    w = h * 0.5
    for i, ch in enumerate(text):
        x0 = x + i * w * 1.5
        P = {"tl": (x0, y), "tr": (x0 + w, y), "ml": (x0, y + h / 2), "mr": (x0 + w, y + h / 2), "bl": (x0, y + h), "br": (x0 + w, y + h)}
        segs = {"a": ("tl", "tr"), "b": ("tr", "mr"), "c": ("mr", "br"), "d": ("bl", "br"), "e": ("ml", "bl"), "f": ("tl", "ml"), "g": ("ml", "mr")}
        for sname in SEG.get(ch, ""):
            (ax, ay), (bx, by) = P[segs[sname][0]], P[segs[sname][1]]
            flat(c, Thick(ax, ay, bx, by, width), col)


def hud(c, left_hp=1.0, right_hp=1.0, timer="99", bar=(250, 210, 50)):
    for x0, x1, hp, flip in ((30, 400, left_hp, False), (500, 870, right_hp, True)):
        piece(c, RRect(x0 - 3, 22, x1 + 3, 46, 3), (40, 30, 40), shadow=SMALL)
        flat(c, RRect(x0, 25, x1, 43, 2), (200, 40, 40))
        if flip:
            flat(c, RRect(x1 - (x1 - x0) * hp, 25, x1, 43, 2), bar)
        else:
            flat(c, RRect(x0, 25, x0 + (x1 - x0) * hp, 43, 2), bar)
    piece(c, RRect(420, 14, 480, 60, 4), (40, 30, 40), border=1.5, shadow=SMALL)
    seg_text(c, 432, 22, 30, timer, (250, 220, 90), 3.4)


def fighter_gi(c, x, base, gi=(250, 250, 248), belt=(30, 30, 34), band=(220, 40, 40), hair=(40, 30, 30), skin=SKIN, h=1.0, flip=False):
    """Karate-gi fighter in a stance (original design)."""
    k = -1 if flip else 1
    piece(c, [Poly([(x - 16 * h * k, base), (x - 8 * h * k, base), (x - 2 * h * k, base - 34 * h), (x - 12 * h * k, base - 34 * h)]),
              Poly([(x + 18 * h * k, base), (x + 26 * h * k, base), (x + 12 * h * k, base - 34 * h), (x + 2 * h * k, base - 34 * h)])], gi, border=1.5,
          shadow=PROP)
    piece(c, [Poly([(x - 14 * h, base - 34 * h), (x + 14 * h, base - 34 * h), (x + 12 * h, base - 70 * h), (x - 12 * h, base - 70 * h)])], gi, border=1.5,
          shadow=PROP)
    flat(c, Poly([(x - 6 * h, base - 70 * h), (x + 6 * h, base - 70 * h), (x, base - 56 * h)]), skin)
    flat(c, RRect(x - 14 * h, base - 40 * h, x + 14 * h, base - 34 * h, 1), belt)
    flat(c, [Thick(x + 6 * h * k, base - 37 * h, x + 14 * h * k, base - 26 * h, 2.4 * h)], belt)
    piece(c, [Thick(x + 10 * h * k, base - 64 * h, x + 30 * h * k, base - 56 * h, 7 * h), Circ(x + 32 * h * k, base - 56 * h, 6 * h)], skin, shadow=SMALL)
    piece(c, [Thick(x - 10 * h * k, base - 64 * h, x - 2 * h * k, base - 48 * h, 7 * h), Circ(x - 1 * h * k, base - 46 * h, 6 * h)], skin, shadow=SMALL)
    hx, hy = x + 2 * h * k, base - 82 * h
    flat(c, Circ(hx, hy, 10 * h), skin)
    flat(c, [Ell(hx - 1 * h * k, hy - 7 * h, 10 * h, 5 * h)], hair)
    flat(c, RRect(hx - 10 * h, hy - 5 * h, hx + 10 * h, hy - 1 * h, 1), band)
    flat(c, [Thick(hx - 10 * h * k, hy - 3 * h, hx - 22 * h * k, hy + 4 * h, 2.4 * h), Thick(hx - 10 * h * k, hy - 3 * h, hx - 20 * h * k, hy + 10 * h, 2.4 * h)], band)
    flat(c, Circ(hx + 4 * h * k, hy, 1.4 * h), INK)


def fighter_kungfu(c, x, base, top=(40, 80, 170), trim=(240, 200, 60), buns=(250, 250, 250), h=1.0, flip=True):
    k = -1 if flip else 1
    piece(c, [Thick(x - 6 * h, base - 34 * h, x - 18 * h * k, base, 8 * h), Thick(x + 6 * h, base - 34 * h, x + 22 * h * k, base - 6 * h, 8 * h)], SKIN,
          shadow=SMALL)
    flat(c, [RRect(x - 22 * h * k - 6 * h, base - 6 * h, x - 22 * h * k + 6 * h, base, 2), RRect(x + 22 * h * k - 6 * h, base - 10 * h, x + 22 * h * k + 6 * h,
                                                                                                  base - 4 * h, 2)], (250, 250, 250))
    piece(c, [Poly([(x - 16 * h, base - 30 * h), (x + 16 * h, base - 30 * h), (x + 12 * h, base - 70 * h), (x - 12 * h, base - 70 * h)])], top, border=1.5,
          shadow=PROP)
    flat(c, [Thick(x - 14 * h, base - 30 * h, x + 14 * h, base - 30 * h, 3 * h), Thick(x, base - 70 * h, x + 8 * h, base - 50 * h, 2 * h)], trim)
    piece(c, [Thick(x + 10 * h * k, base - 64 * h, x + 34 * h * k, base - 70 * h, 7 * h), Circ(x + 36 * h * k, base - 70 * h, 6 * h)], SKIN, shadow=SMALL)
    flat(c, [RRect(x + 22 * h * k - 6 * h, base - 72 * h, x + 22 * h * k + 6 * h, base - 64 * h, 2)], trim)
    hx, hy = x + 2 * h * k, base - 82 * h
    flat(c, Circ(hx, hy, 10 * h), SKIN)
    flat(c, [Ell(hx, hy - 6 * h, 10 * h, 5 * h), Circ(hx - 12 * h, hy - 8 * h, 6 * h), Circ(hx + 12 * h, hy - 8 * h, 6 * h)], (40, 30, 30))
    flat(c, [Circ(hx - 12 * h, hy - 8 * h, 4.6 * h), Circ(hx + 12 * h, hy - 8 * h, 4.6 * h)], buns)
    flat(c, Circ(hx + 4 * h * k, hy, 1.4 * h), INK)


def chicken(c, x, base, col=(250, 246, 236)):
    piece(c, [Ell(x, base - 10, 12, 9), Circ(x + 10, base - 20, 6), Poly([(x - 10, base - 14), (x - 18, base - 24), (x - 14, base - 8)])], col, border=1,
          shadow=SMALL)
    flat(c, [Poly([(x + 8, base - 26), (x + 11, base - 30), (x + 14, base - 26)]), Poly([(x + 16, base - 20), (x + 21, base - 19), (x + 16, base - 17)])],
         (220, 50, 50))
    flat(c, [Thick(x - 2, base - 2, x - 4, base + 4, 1.4), Thick(x + 4, base - 2, x + 4, base + 4, 1.4)], (230, 160, 50))


def bicycle(c, x, base, col):
    for wx in (x - 22, x + 22):
        c.ellipse_ring(wx, base - 16, 15, 15, 2.4, (40, 40, 46))
    flat(c, [Thick(x - 22, base - 16, x, base - 16, 2.4), Thick(x, base - 16, x + 12, base - 34, 2.4), Thick(x - 22, base - 16, x - 8, base - 34, 2.4),
             Thick(x - 8, base - 34, x + 12, base - 34, 2.4), Thick(x + 12, base - 34, x + 22, base - 16, 2.4)], col)
    flat(c, [Thick(x - 12, base - 38, x - 4, base - 38, 3), Thick(x + 12, base - 34, x + 14, base - 42, 2)], (40, 40, 46))


# =================================================================== Level 119 night market stage
def l119_bg(c, d):
    c.gradient(0, 400, (30, 30, 70), (90, 60, 100))
    rnd = random.Random(119)
    for x0, x1, top in ((-10, 150, 90), (150, 330, 130), (330, 560, 70), (560, 740, 120), (740, 910, 100)):
        piece(c, RRect(x0, top, x1, 400, 1), (60, 56, 80), border=1.5, shadow=PROP)
        for y in range(top + 16, 380, 28):
            for x in range(x0 + 12, x1 - 14, 24):
                if rnd.random() < 0.5:
                    flat(c, RRect(x, y, x + 12, y + 14, 1), (250, 210, 130))
    for i, (x0, y0, x1, y1, col) in enumerate(((60, 120, 92, 300, (220, 50, 50)), (250, 150, 282, 320, (250, 200, 60)), (620, 140, 652, 310, (60, 180, 220)),
                                               (800, 120, 832, 300, (230, 80, 160)))):
        sign_box(c, x0, y0, x1, y1, ((90, 200, 120) if "sign" in d else col) if i == 2 else col, 1190 + i)
    # string lights and lanterns
    pts = [(k * 60, 100 + 20 * math.sin(math.pi * k / 7.5)) for k in range(16)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(15)], (40, 40, 50))
    for i, (x, y) in enumerate(pts[1:-1]):
        lantern_cn(c, x, y + 16, ((90, 160, 220) if "lantern" in d else (220, 50, 40)) if i == 6 else (220, 50, 40), r=8)
    # stalls and crowd behind a rope
    for x0, col in ((0, (200, 60, 50)), (220, (60, 120, 180)), (640, (230, 170, 60))):
        piece(c, RRect(x0, 330, x0 + 180, 420, 2), (150, 110, 70), border=1.2, shadow=PROP)
        piece(c, Poly([(x0 - 10, 330), (x0 + 190, 330), (x0 + 170, 300), (x0 + 10, 300)]), col, border=1.2, shadow=SMALL)
    for x in range(10, 900, 24):
        col = rnd.choice(((60, 70, 110), (150, 60, 70), (90, 110, 80), (200, 160, 100), (110, 70, 110), (240, 240, 240)))
        piece(c, [Ell(x, 440, 11, 16), Circ(x, 418, 8)], col, shadow=SMALL)
        flat(c, Circ(x, 418, 6.6), SKIN)
        flat(c, Ell(x, 413, 7, 3.4), (40, 30, 30))
    flat(c, [Thick(0, 452, 900, 452, 3)], (200, 40, 40))
    for x in range(0, 900, 90):
        flat(c, RRect(x - 3, 446, x + 3, 470, 1), (220, 200, 160))
    # ground
    piece(c, RRect(-10, 466, 910, 612, 0), (130, 120, 110), shadow=LAYER)
    for x in range(0, 900, 50):
        flat(c, Thick(x, 466, x - 30, 612, 1.2), (116, 106, 98))
    bicycle(c, 80, 560, (60, 160, 90) if "bicycle" in d else (220, 60, 60))
    bicycle(c, 820, 566, (60, 110, 200))
    if "chicken" not in d:
        chicken(c, 180, 590)
    chicken(c, 740, 596, (190, 120, 60))
    hud(c, left_hp=0.62 if "hp" in d else 0.86, right_hp=0.7)


L119_ELEMENTS = [
    E("fighterA", lambda c, m: fighter_gi(c, 330, 566, band=(60, 120, 220) if m else (220, 40, 40), h=1.3), pivot=(330, 566), variant=True,
      anim=dict(bobAmplitude=(0, 3), bobSpeed=1.0, stretch=(0, 0.02), scaleSpeed=1.0)),
    E("fighterB", lambda c, m: fighter_kungfu(c, 580, 566, buns=(220, 60, 60) if m else (250, 250, 250), h=1.3), pivot=(580, 566), variant=True,
      anim=dict(bobAmplitude=(0, 4), bobSpeed=1.2, phase=0.5)),
    E("crowd", lambda c, m: [flat(c, Thick(x, 430, x + 6, 404, 3), SKIN) for x in range(40, 900, 96)], anim=dict(bobAmplitude=(0, 6), bobSpeed=0.9)),
] + smoke_el("steam", 300, 300, n=3, col=(240, 240, 246), r=7, rise=(4, 18), length=60)

L119_DIFFS = [
    ("sign", 636, 226, 0),
    ("lantern", int(7 * 60), 130, 0),
    ("bicycle", 80, 534, 0),
    ("chicken", 184, 578, 0),
    ("hp", 300, 34, 0),
    ("band", 334, 457, 0),
    ("buns", 582, 456, 0),
]


# =================================================================== Level 120 dockside at sunset
def wrestler(c, x, base, trunks=(200, 40, 40), h=1.0, flip=False):
    k = -1 if flip else 1
    piece(c, [Thick(x - 8 * h, base - 34 * h, x - 18 * h * k, base, 11 * h), Thick(x + 8 * h, base - 34 * h, x + 18 * h * k, base, 11 * h)], TAN,
          shadow=SMALL)
    flat(c, [RRect(x - 18 * h * k - 8 * h, base - 12 * h, x - 18 * h * k + 8 * h, base, 2), RRect(x + 18 * h * k - 8 * h, base - 12 * h,
                                                                                                    x + 18 * h * k + 8 * h, base, 2)], (40, 40, 46))
    piece(c, Ell(x, base - 62 * h, 24 * h, 30 * h), TAN, border=1.5, shadow=PROP)
    piece(c, RRect(x - 18 * h, base - 42 * h, x + 18 * h, base - 28 * h, 4), trunks, shadow=None)
    piece(c, [Thick(x + 18 * h * k, base - 80 * h, x + 40 * h * k, base - 60 * h, 11 * h), Thick(x - 18 * h * k, base - 80 * h, x - 34 * h * k, base - 52 * h,
                                                                                                    11 * h)], TAN, shadow=SMALL)
    hx, hy = x + 2 * h * k, base - 100 * h
    flat(c, Circ(hx, hy, 11 * h), TAN)
    flat(c, Ell(hx, hy - 8 * h, 11 * h, 4 * h), (40, 30, 30))
    flat(c, Circ(hx + 4 * h * k, hy, 1.4 * h), INK)


def l120_bg(c, d):
    sky(c, (250, 150, 90), (255, 220, 160), 380)
    piece(c, Circ(450, 300, 70), (255, 200, 120), shadow=None)
    c.rect(0, 340, W, 420, (200, 110, 90))
    for y in range(350, 418, 10):
        flat(c, Thick(380, y, 520, y, 2), (255, 190, 130))
    # cargo ship and crane
    piece(c, Poly([(560, 400), (900, 390), (910, 300), (600, 300)]), (60, 50, 60), border=1.5, shadow=PROP)
    flat(c, Thick(600, 320, 910, 316, 4), (200, 60, 50))
    piece(c, RRect(760, 220, 860, 300, 2), (236, 230, 220), border=1.2, shadow=SMALL)
    flat(c, Thick(840, 220, 840, 180, 2), (60, 60, 70))
    flat(c, Poly([(841, 180), (870, 186), (841, 194)]), (60, 160, 90) if "flag" in d else (230, 60, 50))
    piece(c, [Thick(120, 420, 120, 140, 10), Thick(120, 150, 380, 120, 8), Thick(120, 150, 70, 170, 8)], (240, 180, 50), shadow=PROP)
    flat(c, Thick(340, 124, 340, 230, 1.4), (60, 60, 70))
    piece(c, RRect(318, 230, 362, 262, 2), (90, 130, 170), border=1.2, shadow=SMALL)
    # dock
    piece(c, RRect(-10, 420, 910, 612, 0), (150, 130, 110), shadow=LAYER)
    for x in range(0, 900, 40):
        flat(c, Thick(x, 420, x, 612, 1.2), (134, 114, 96))
    n = 3 if "crates" in d else 4
    for k in range(n):
        crate(c, 70 + (k % 2) * 34, 600 - (k // 2) * 30, 1.0)
    for x in (780, 820):
        piece(c, RRect(x - 16, 540, x + 16, 600, 6), (60, 120, 180) if ("drum" in d and x == 820) else (200, 80, 50), border=1.2, shadow=PROP)
        flat(c, [Thick(x - 16, 556, x + 16, 556, 2), Thick(x - 16, 584, x + 16, 584, 2)], (40, 40, 46))
    rnd = random.Random(120)
    for x in range(180, 740, 40):
        if 300 < x < 640:
            continue
        modern(c, x, 470, rnd.choice(((60, 80, 140), (200, 140, 60), (240, 240, 240), (90, 110, 80))), hair=(40, 30, 30), h=1.2)
    hud(c, left_hp=0.5, right_hp=0.9, timer="60" if "timer" in d else "99")
    if "gull" not in d:
        piece(c, [Ell(600, 290, 10, 6), Circ(608, 284, 4)], (250, 250, 250), shadow=SMALL)
        flat(c, Poly([(612, 284), (617, 285), (612, 286)]), (240, 180, 60))


L120_ELEMENTS = [
    E("wrestler", lambda c, m: wrestler(c, 340, 566, trunks=(60, 120, 200) if m else (200, 40, 40), h=1.3), pivot=(340, 566), variant=True,
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.9)),
    E("karateka", lambda c, m: fighter_gi(c, 580, 566, gi=(240, 150, 60), belt=(250, 250, 250) if m else (30, 30, 34), band=(250, 250, 250), h=1.3, flip=True),
      pivot=(580, 566), variant=True, anim=dict(bobAmplitude=(0, 4), bobSpeed=1.1, phase=0.5)),
    bird_el("gull0", 300, 80, 10, col=(250, 250, 250), speed=14), bird_el("gull1", 330, 70, 8, col=(250, 250, 250), speed=14),
    E("hook", lambda c, m: (flat(c, Thick(340, 262, 340, 290, 1.4), (60, 60, 70)), flat(c, Circ(340, 294, 4), (60, 60, 70))), pivot=(340, 124),
      anim=dict(swingAngle=3, swingSpeed=0.3)),
]

L120_DIFFS = [
    ("flag", 855, 187, 0),
    ("crates", 104, 560, 0),
    ("drum", 820, 570, 0),
    ("timer", 455, 37, 0),
    ("gull", 606, 288, 0),
    ("trunks", 340, 518, 0),
    ("belt", 580, 512, 0),
]


# =================================================================== Level 121 caravels leaving Lisbon
def caravel(c, x, base, k=1.0, cross=(200, 40, 40), hull=(110, 74, 50), pennant=(220, 50, 50)):
    piece(c, Poly([(x - 70 * k, base - 30 * k), (x + 70 * k, base - 34 * k), (x + 56 * k, base), (x - 56 * k, base)]), hull, border=1.5, shadow=PROP)
    piece(c, RRect(x - 70 * k, base - 46 * k, x - 40 * k, base - 30 * k, 2), hull, shadow=SMALL)
    for mx, h in ((x - 20 * k, 120), (x + 30 * k, 96)):
        flat(c, Thick(mx, base - 30 * k, mx, base - 30 * k - h * k, 3), (100, 70, 50))
        piece(c, Poly([(mx - 4 * k, base - 30 * k - h * k), (mx + 46 * k, base - 40 * k), (mx - 4 * k, base - 40 * k)]), (246, 240, 226), border=1.2,
              shadow=SMALL)
        flat(c, [Thick(mx + 8 * k, base - 52 * k - h * 0.25 * k, mx + 8 * k, base - 52 * k, 4 * k), Thick(mx, base - 46 * k - h * 0.12 * k,
                                                                                                         mx + 18 * k, base - 46 * k - h * 0.12 * k, 4 * k)],
             cross)
    flat(c, Poly([(x - 20 * k, base - 150 * k), (x + 6 * k, base - 146 * k), (x - 20 * k, base - 140 * k)]), pennant)


def l121_bg(c, d):
    sky(c, (160, 204, 240), (246, 236, 214), 340)
    piece(c, hill_strip(300, [(20, 0.008, 0.4)]), (160, 180, 150), shadow=LAYER)
    c.rect(0, 320, W, 480, (80, 150, 190))
    for y in range(330, 478, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (120, 186, 216))
    # river tower
    piece(c, RRect(60, 180, 200, 400, 1), (230, 220, 196), border=2, shadow=PROP)
    piece(c, RRect(90, 120, 170, 182, 1), (230, 220, 196), border=1.5, shadow=PROP)
    for x in range(60, 200, 16):
        piece(c, RRect(x, 170, x + 10, 182, 0), (230, 220, 196), shadow=None)
    for x in range(90, 170, 14):
        piece(c, RRect(x, 110, x + 8, 122, 0), (230, 220, 196), shadow=None)
    for x in (66, 194):
        piece(c, [RRect(x - 8, 170, x + 8, 200, 1), ellipse_top(x, 172, 10, 14)], (230, 220, 196), border=1, shadow=SMALL)
    for x in (100, 140):
        flat(c, arch(x, x + 20, 220, 270), (90, 90, 100))
    flat(c, Thick(130, 110, 130, 70, 2), (90, 80, 80))
    flat(c, Poly([(131, 70), (160, 76), (131, 82)]), (60, 140, 80) if "towerflag" in d else (230, 60, 50))
    caravel(c, 420, 420, 1.0, cross=(60, 90, 180) if "cross" in d else (200, 40, 40))
    caravel(c, 680, 380, 0.7)
    # quay with navigators
    piece(c, RRect(-10, 470, 910, 612, 0), (200, 186, 160), shadow=LAYER)
    for x in range(0, 900, 48):
        flat(c, Thick(x, 470, x, 612, 1.2), (184, 170, 144))
    piece(c, RRect(260, 530, 400, 548, 2), (130, 90, 60), border=1.2, shadow=PROP)
    flat(c, [RRect(268, 548, 276, 590, 1), RRect(384, 548, 392, 590, 1)], (110, 76, 50))
    piece(c, RRect(276, 520, 340, 532, 1), (236, 226, 196), shadow=SMALL)
    piece(c, Circ(370, 512, 14), (60, 140, 90) if "globe" in d else (90, 140, 200), border=1.2, shadow=SMALL)
    flat(c, [Thick(356, 512, 384, 512, 1), Thick(370, 498, 370, 526, 1)], (250, 240, 200))
    hx, hy = person(c, 220, 590, (60, 40, 70))
    flat(c, [Ell(hx, hy - 6, 11, 3), Ell(hx, hy - 9, 6, 4)], (150, 40, 50) if "hat" in d else (30, 30, 34))
    if "astrolabe" not in d:
        c.ellipse_ring(240, 540, 9, 9, 2, (230, 190, 70))
        flat(c, Thick(232, 540, 248, 540, 1.4), (230, 190, 70))
    person(c, 450, 592, (30, 28, 32))
    flat(c, [Thick(450, 560, 450, 540, 1.4), Thick(444, 548, 456, 548, 1.4)], (230, 190, 70))
    for k in range(4 if "barrels" not in d else 3):
        barrel(c, 560 + k * 26, 600, 1.0)
    person(c, 690, 594, (200, 180, 140))
    flat(c, Thick(820, 600, 820, 470, 3), (110, 80, 60))
    piece(c, Poly([(821, 470), (870, 474), (866, 498), (870, 522), (821, 526)]), (220, 220, 230), border=1.2, shadow=SMALL)
    c.ellipse_ring(845, 498, 12, 12, 2.4, (60, 90, 180) if "banner" in d else (230, 190, 70))


L121_ELEMENTS = [
    cloud_el("cloud0", 360, 60, 0.7, 6), cloud_el("cloud1", 700, 90, 0.5, 5),
    bird_el("gull0", 520, 150, 10, col=(250, 250, 250), speed=14), bird_el("gull1", 548, 140, 8, col=(250, 250, 250), speed=14),
    E("pennant", lambda c, m: flat(c, Poly([(400, 270), (434, 276), (400, 282)]), (240, 236, 226)), pivot=(400, 276),
      anim=dict(stretch=(0.2, 0), scaleSpeed=1.3, swingAngle=4, swingSpeed=0.8)),
    E("far_ship", lambda c, m: caravel(c, 860, 350, 0.4), pivot=(860, 350), anim=dict(drift_across(830, 890, 6), bobAmplitude=(0, 1.5), bobSpeed=0.3)),
]

L121_DIFFS = [
    ("towerflag", 145, 76, 0),
    ("cross", 406, 300, 0),
    ("globe", 370, 512, 0),
    ("astrolabe", 240, 540, 0),
    ("barrels", 638, 586, 0),
    ("banner", 845, 498, 0),
    ("hat", 221, 542, 0),
]


# =================================================================== Level 122 landing on a tropical shore
def l122_bg(c, d):
    sky(c, (120, 200, 240), (240, 240, 220), 320)
    piece(c, Circ(780, 80, 30), (255, 230, 120), border=2, shadow=PROP)
    c.rect(0, 300, W, 470, (50, 170, 190))
    for y in range(310, 468, 12):
        for x in range((y * 13) % 66, 900, 66):
            flat(c, Thick(x, y, x + 24, y, 2), (110, 210, 220))
    # ship at anchor
    piece(c, Poly([(120, 330), (380, 330), (360, 360), (140, 360)]), (90, 60, 44), border=1.5, shadow=PROP)
    for mx, top in ((180, 200), (260, 170), (330, 210)):
        flat(c, Thick(mx, 330, mx, top, 3), (100, 70, 50))
        piece(c, Poly([(mx - 28, top + 14), (mx + 28, top + 14), (mx + 24, top + 70), (mx - 24, top + 70)]), (246, 240, 226), border=1.2, shadow=SMALL)
    flat(c, [Thick(260, 200, 260, 238, 6), Thick(246, 214, 274, 214, 6)], (200, 40, 40))
    # island with palms
    piece(c, hill_strip(300, [(26, 0.01, 0.5)], x0=500, x1=960), (90, 150, 90), shadow=LAYER)
    piece(c, hill_strip(440, [(8, 0.012, 0.4), (3, 0.04, 1.0)]), (240, 220, 170), shadow=LAYER)
    for i, (x, h, lean) in enumerate(((560, 170, 20), (660, 200, -16), (800, 180, 24), (40, 190, 18))):
        if i == 2 and "palm" in d:
            continue
        palm(c, x, 470, h, lean)
    if "monkey" not in d:
        piece(c, [Ell(664, 330, 9, 10), Circ(668, 316, 7)], (130, 90, 60), shadow=SMALL)
        flat(c, Ell(670, 318, 4, 4), (230, 200, 160))
    # longboat and explorers
    piece(c, Poly([(200, 470), (360, 470), (344, 492), (216, 492)]), (130, 90, 60), border=1.5, shadow=PROP)
    for x in (240, 290):
        person(c, x, 472, (60, 70, 110), h=0.8)
    hx, hy = person(c, 470, 580, (90, 40, 50))
    flat(c, [Ell(hx, hy - 6, 11, 3), Ell(hx, hy - 9, 6, 4)], (60, 140, 90) if "hat" in d else (30, 30, 34))
    flat(c, Thick(500, 590, 504, 460, 3), (110, 80, 60))
    piece(c, Poly([(505, 460), (556, 466), (552, 490), (556, 514), (505, 520)]), (60, 90, 180) if "flag" in d else (230, 220, 200), border=1.2, shadow=SMALL)
    flat(c, [Thick(530, 466, 530, 516, 5), Thick(508, 490, 552, 490, 5)], (200, 40, 40))
    person(c, 400, 584, (120, 100, 70))
    piece(c, RRect(410, 548, 436, 566, 1), (220, 200, 150), border=1, shadow=SMALL)
    # treasure chest, crab, parrot, turtle
    piece(c, RRect(620, 548, 690, 590, 3), (150, 100, 60), border=1.5, shadow=PROP)
    if "chest" in d:
        piece(c, ellipse_top(655, 550, 35, 12), (150, 100, 60), border=1.2, shadow=SMALL)
    else:
        piece(c, Poly([(620, 548), (690, 548), (700, 520), (630, 520)]), (150, 100, 60), border=1.2, shadow=SMALL)
        flat(c, [Circ(640, 544, 6), Circ(656, 542, 6), Circ(672, 544, 6)], (250, 220, 90))
    if "crab" not in d:
        piece(c, [Ell(160, 590, 14, 8)], (230, 80, 50), shadow=SMALL)
        flat(c, [Thick(148, 588, 140, 578, 2), Thick(172, 588, 180, 578, 2)], (230, 80, 50))
    parrot = (60, 160, 230) if "parrot" in d else (220, 50, 50)
    piece(c, [Ell(70, 330, 8, 12), Circ(72, 316, 6), Poly([(66, 340), (62, 360), (72, 344)])], parrot, border=1, shadow=SMALL)
    flat(c, Poly([(76, 316), (82, 318), (76, 320)]), (240, 200, 60))
    piece(c, [Ell(760, 598, 26, 10), Circ(788, 594, 6)], (110, 140, 90), border=1, shadow=SMALL)


L122_ELEMENTS = [
    cloud_el("cloud0", 200, 60, 0.7, 6), cloud_el("cloud1", 520, 90, 0.5, 5),
    E("waves", lambda c, m: flat(c, [Thick(0, 440, 900, 440, 3)], (250, 250, 250)), anim=dict(bobAmplitude=(0, 4), bobSpeed=0.3)),
    E("ship_bob", lambda c, m: flat(c, Poly([(261, 170), (292, 176), (261, 182)]), (240, 236, 226)), pivot=(261, 176),
      anim=dict(stretch=(0.2, 0), scaleSpeed=1.3, swingAngle=4, swingSpeed=0.8)),
    bird_el("gull0", 420, 120, 10, col=(250, 250, 250), speed=14),
]

L122_DIFFS = [
    ("palm", 820, 360, 0),
    ("monkey", 666, 322, 0),
    ("hat", 471, 532, 0),
    ("flag", 530, 490, 0),
    ("chest", 655, 536, 0),
    ("crab", 160, 586, 0),
    ("parrot", 70, 330, 0),
]

LEVELS = [
    ("Level119", "夜市擂台", l119_bg, L119_ELEMENTS, L119_DIFFS, 140, OPTS),
    ("Level120", "黄昏码头", l120_bg, L120_ELEMENTS, L120_DIFFS, 140, OPTS),
    ("Level121", "里斯本出航", l121_bg, L121_ELEMENTS, L121_DIFFS, 140, OPTS),
    ("Level122", "新大陆登陆", l122_bg, L122_ELEMENTS, L122_DIFFS, 140, OPTS),
]
