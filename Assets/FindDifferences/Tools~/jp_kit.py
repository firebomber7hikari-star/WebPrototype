# -*- coding: utf-8 -*-
"""Japanese prop library for the Heian / Sengoku / Meiji levels (paper-craft, scene coordinates, base = ground y)."""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL
from levels_heian import GOLD, VERMILION, ROOF, BLIND, HAIR, curved_roof
from levels_europe import ellipse_top, arch

TILE = (72, 78, 92)
PLASTER = (244, 240, 230)
SKIN = (250, 226, 200)


# ------------------------------------------------------------------- architecture
def tile_roof(c, x0, x1, base, h, col=TILE, flare=12, gable=False):
    """Hip roof with upturned eaves (castle / town style)."""
    w = x1 - x0
    o = flare + 8
    pts = [(x0 - o, base - 6), (x0 - o + 6, base + 2), (x0 + w * 0.2, base - h * 0.55), (x0 + w * 0.3, base - h), (x1 - w * 0.3, base - h),
           (x1 - w * 0.2, base - h * 0.55), (x1 + o - 6, base + 2), (x1 + o, base - 6), (x1 + o - 4, base + 6), (x0 - o + 4, base + 6)]
    piece(c, Poly(pts), col, border=1.5, shadow=PROP)
    for k in range(1, int(w // 10)):
        x = x0 + k * 10
        flat(c, Thick(x, base + 3, x + (x - (x0 + x1) / 2) * 0.12, base - h * 0.5, 0.8), lit(col, 0.85))
    flat(c, Thick(x0 + w * 0.3, base - h, x1 - w * 0.3, base - h, 3), lit(col, 0.7))
    if gable:
        cx = (x0 + x1) / 2
        piece(c, Poly([(cx - h * 0.9, base - h * 0.45), (cx + h * 0.9, base - h * 0.45), (cx, base - h * 1.2)]), col, border=1.2, shadow=SMALL)
        flat(c, Poly([(cx - h * 0.6, base - h * 0.5), (cx + h * 0.6, base - h * 0.5), (cx, base - h * 1.0)]), PLASTER)


def shachi(c, x, y, s=1.0, flip=False, col=GOLD):
    k = -1 if flip else 1
    piece(c, Poly([(x, y), (x + 6 * k * s, y - 4 * s), (x + 4 * k * s, y - 12 * s), (x + 10 * k * s, y - 20 * s), (x + 2 * k * s, y - 16 * s),
                   (x - 2 * k * s, y - 6 * s)]), col, border=1, shadow=SMALL)


def ishigaki(c, x0, x1, base, top, slope=18):
    piece(c, Poly([(x0, base), (x1, base), (x1 - slope, top), (x0 + slope, top)]), (170, 164, 150), border=1.5, shadow=PROP)
    rnd = random.Random(int(x0 * 7 + top))
    y = base - 8
    while y > top + 4:
        t = (base - y) / (base - top)
        xa, xb = x0 + slope * t, x1 - slope * t
        x = xa + rnd.uniform(0, 10)
        while x < xb - 10:
            w = rnd.uniform(14, 26)
            flat(c, RRect(x, y - 7, min(xb, x + w), y, 2), (154, 148, 134))
            x += w + 3
        y -= 9


def castle_keep(c, x, base, w0=150, tiers=4, tier_h=44, shachi_r=True, wall=PLASTER, roof=TILE):
    """Multi-storey keep on its stone base; returns the y of the top ridge."""
    top = base
    for k in range(tiers):
        w = w0 * (1 - 0.17 * k)
        y0 = top - tier_h
        piece(c, RRect(x - w / 2, y0, x + w / 2, top, 1), wall, border=1.5, shadow=PROP)
        flat(c, RRect(x - w / 2, top - tier_h * 0.35, x + w / 2, top, 0), (60, 56, 60))
        for wx in range(int(x - w / 2 + 10), int(x + w / 2 - 12), 20):
            flat(c, RRect(wx, y0 + 10, wx + 8, y0 + 20, 1), (60, 56, 60))
        tile_roof(c, x - w / 2, x + w / 2, y0, 20 if k < tiers - 1 else 30, roof, gable=(k % 2 == 1))
        top = y0 - (8 if k < tiers - 1 else 0)
    ridge = top - 30
    shachi(c, x - w0 * 0.12, ridge + 2, 1.0, flip=True)
    if shachi_r:
        shachi(c, x + w0 * 0.12, ridge + 2, 1.0)
    return ridge


def plaster_wall(c, x0, x1, top, base):
    piece(c, RRect(x0, top, x1, base, 0), PLASTER, border=1.5, shadow=PROP)
    flat(c, RRect(x0, top + (base - top) * 0.55, x1, base, 0), (60, 56, 60))
    for x in range(int(x0 + 14), int(x1 - 10), 40):
        flat(c, RRect(x, top + 10, x + 8, top + 16, 1), (60, 56, 60))
    piece(c, Poly([(x0 - 6, top + 2), (x1 + 6, top + 2), (x1, top - 10), (x0, top - 10)]), TILE, shadow=SMALL)


def machiya(c, x0, x1, base, h, wall=(150, 112, 80), noren=(40, 60, 110), sign=None, lantern=None):
    """Two-storey townhouse: lattice front, tiled roofs, noren curtain; returns door centre."""
    piece(c, RRect(x0, base - h, x1, base, 1), wall, border=1.5, shadow=PROP)
    tile_roof(c, x0 + 4, x1 - 4, base - h * 0.52, 10, flare=4)
    for x in range(int(x0 + 6), int(x1 - 4), 6):
        flat(c, Thick(x, base - h + 8, x, base - h * 0.58, 1.6), lit(wall, 0.7))
    tile_roof(c, x0 + 6, x1 - 6, base - h, 14, flare=6)
    cx = (x0 + x1) / 2
    flat(c, RRect(x0 + 8, base - h * 0.42, x1 - 8, base, 0), (70, 56, 46))
    piece(c, RRect(cx - 22, base - h * 0.42, cx + 22, base - h * 0.22, 1), noren, shadow=SMALL)
    flat(c, [Thick(cx - 7, base - h * 0.42, cx - 7, base - h * 0.22, 1), Thick(cx + 7, base - h * 0.42, cx + 7, base - h * 0.22, 1)], lit(noren, 0.7))
    flat(c, Circ(cx, base - h * 0.33, 4), (240, 236, 226))
    if sign:
        piece(c, RRect(x1 - 18, base - h * 0.5, x1 - 6, base - h * 0.5 + 34, 1), sign, border=1, shadow=SMALL)
    if lantern:
        chochin(c, x0 + 12, base - h * 0.4, lantern)
    return cx


def chochin(c, x, y, col=(220, 60, 50), s=1.0):
    flat(c, Thick(x, y - 6 * s, x, y, 1), (60, 50, 50))
    piece(c, [Ell(x, y + 10 * s, 7 * s, 10 * s)], col, border=1, shadow=SMALL)
    flat(c, [RRect(x - 4 * s, y - 1 * s, x + 4 * s, y + 2 * s, 1), RRect(x - 4 * s, y + 18 * s, x + 4 * s, y + 21 * s, 1)], (40, 34, 34))
    for k in (-4, 0, 4):
        flat(c, Thick(x - 6 * s, y + 10 * s + k * s, x + 6 * s, y + 10 * s + k * s, 0.6), lit(col, 0.8))


def torii(c, x, base, w=90, h=100, col=VERMILION):
    piece(c, [RRect(x - w / 2 + 6, base - h, x - w / 2 + 14, base, 1), RRect(x + w / 2 - 14, base - h, x + w / 2 - 6, base, 1),
              RRect(x - w / 2 - 4, base - h + 14, x + w / 2 + 4, base - h + 22, 1),
              Poly([(x - w / 2 - 14, base - h - 2), (x + w / 2 + 14, base - h - 2), (x + w / 2 + 8, base - h + 8), (x - w / 2 - 8, base - h + 8)])],
          col, border=1.5, shadow=PROP)
    flat(c, Thick(x - w / 2 - 14, base - h - 2, x + w / 2 + 14, base - h - 2, 3), (40, 34, 34))


# ------------------------------------------------------------------- people
def kimono(c, x, base, col, obi=(220, 190, 90), h=1.0, hair="man", hat=None, umbrella=None):
    """Townsperson in a kimono; hair 'man' (topknot) or 'woman' (bun); optional sedge hat / umbrella. Returns head."""
    piece(c, [Poly([(x - 10 * h, base), (x + 10 * h, base), (x + 8 * h, base - 32 * h), (x - 8 * h, base - 32 * h)]),
              Poly([(x - 8 * h, base - 30 * h), (x - 16 * h, base - 16 * h), (x - 8 * h, base - 14 * h)])], col, border=1.5, shadow=PROP)
    flat(c, RRect(x - 8.5 * h, base - 22 * h, x + 8.5 * h, base - 17 * h, 1), obi)
    flat(c, Poly([(x - 2 * h, base - 32 * h), (x + 2 * h, base - 32 * h), (x, base - 24 * h)]), (240, 236, 226))
    hx, hy = x + 1 * h, base - 40 * h
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    if hair == "woman":
        flat(c, [Ell(hx - 2 * h, hy - 5 * h, 8 * h, 4 * h), Ell(hx - 4 * h, hy - 10 * h, 6 * h, 4 * h)], HAIR)
        flat(c, Thick(hx - 10 * h, hy - 10 * h, hx + 4 * h, hy - 12 * h, 1.2), (220, 60, 80))
    else:
        flat(c, [Ell(hx - 3 * h, hy - 5 * h, 7 * h, 3 * h), RRect(hx - 2 * h, hy - 10 * h, hx + 4 * h, hy - 7 * h, 1)], HAIR)
    if hat:
        flat(c, Poly([(hx - 13 * h, hy - 3 * h), (hx + 13 * h, hy - 3 * h), (hx, hy - 12 * h)]), hat)
    if umbrella:
        flat(c, Thick(hx + 8 * h, hy + 8 * h, hx + 10 * h, hy - 22 * h, 1.4), (110, 80, 60))
        piece(c, ellipse_top(hx + 10 * h, hy - 20 * h, 24 * h, 12 * h), umbrella, border=1.2, shadow=SMALL)
        for k in range(5):
            a = math.pi * (k + 0.5) / 5
            flat(c, Thick(hx + 10 * h, hy - 20 * h, hx + 10 * h + 22 * h * math.cos(a), hy - 20 * h - 11 * h * math.sin(a), 0.6), lit(umbrella, 0.75))
    return hx, hy


def samurai(c, x, base, armor, h=1.0, crest=GOLD, sashimono=None, spear=False):
    """Armoured samurai (lamellar armour, kabuto with crest); optional back banner and spear."""
    if sashimono:
        flat(c, Thick(x - 6 * h, base - 30 * h, x - 6 * h, base - 76 * h, 1.6), (90, 70, 60))
        piece(c, RRect(x - 6 * h, base - 76 * h, x + 6 * h, base - 52 * h, 1), sashimono, shadow=SMALL)
    piece(c, [Poly([(x - 12 * h, base - 12 * h), (x + 12 * h, base - 12 * h), (x + 9 * h, base - 34 * h), (x - 9 * h, base - 34 * h)]),
              RRect(x - 7 * h, base - 12 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 12 * h, x + 7 * h, base, 1)], armor, border=1.5, shadow=PROP)
    for k in range(4):
        flat(c, Thick(x - 11 * h, base - 14 * h - k * 5 * h, x + 11 * h, base - 14 * h - k * 5 * h, 0.8), lit(armor, 0.7))
    hx, hy = x + 1 * h, base - 40 * h
    flat(c, Circ(hx, hy, 6 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    piece(c, [ellipse_top(hx, hy - 2 * h, 9 * h, 9 * h), RRect(hx - 12 * h, hy - 3 * h, hx + 12 * h, hy, 1)], lit(armor, 0.6), shadow=None)
    if crest:
        flat(c, [Thick(hx, hy - 9 * h, hx - 8 * h, hy - 22 * h, 2.2 * h), Thick(hx, hy - 9 * h, hx + 8 * h, hy - 22 * h, 2.2 * h)], crest)
    if spear:
        flat(c, Thick(x + 12 * h, base, x + 16 * h, base - 110 * h, 2), (110, 80, 60))
        flat(c, Poly([(x + 14.5 * h, base - 110 * h), (x + 17.5 * h, base - 110 * h), (x + 16.6 * h, base - 126 * h)]), (210, 210, 220))
    return hx, hy


def ashigaru(c, x, base, col, h=1.0, weapon="yari"):
    piece(c, [Poly([(x - 9 * h, base - 10 * h), (x + 9 * h, base - 10 * h), (x + 7 * h, base - 32 * h), (x - 7 * h, base - 32 * h)]),
              RRect(x - 6 * h, base - 10 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 10 * h, x + 6 * h, base, 1)], col, border=1.2, shadow=PROP)
    hx, hy = x + 1 * h, base - 38 * h
    flat(c, Circ(hx, hy, 6 * h), SKIN)
    flat(c, Poly([(hx - 12 * h, hy - 2 * h), (hx + 12 * h, hy - 2 * h), (hx, hy - 9 * h)]), (40, 36, 40))
    if weapon == "yari":
        flat(c, Thick(x + 8 * h, base, x + 8 * h, base - 140 * h, 1.8), (110, 80, 60))
        flat(c, Poly([(x + 6.5 * h, base - 140 * h), (x + 9.5 * h, base - 140 * h), (x + 8 * h, base - 154 * h)]), (210, 210, 220))
    elif weapon == "teppo":
        flat(c, Thick(x - 4 * h, base - 24 * h, x + 30 * h, base - 30 * h, 2.6), (70, 50, 40))
    return hx, hy


def westerner(c, x, base, coat, h=1.0, hat="top", hat_col=(30, 30, 34), trousers=(50, 50, 60)):
    piece(c, [RRect(x - 6 * h, base - 14 * h, x - 1.5 * h, base, 1), RRect(x + 1.5 * h, base - 14 * h, x + 6 * h, base, 1)], trousers, shadow=SMALL)
    piece(c, Poly([(x - 9 * h, base - 12 * h), (x + 9 * h, base - 12 * h), (x + 8 * h, base - 34 * h), (x - 8 * h, base - 34 * h)]), coat, border=1.5,
          shadow=PROP)
    flat(c, Poly([(x - 2 * h, base - 34 * h), (x + 2 * h, base - 34 * h), (x, base - 26 * h)]), (246, 244, 236))
    hx, hy = x + 1 * h, base - 41 * h
    flat(c, Circ(hx, hy, 6.5 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    if hat == "top":
        flat(c, [RRect(hx - 9 * h, hy - 6 * h, hx + 9 * h, hy - 4 * h, 1), RRect(hx - 6 * h, hy - 19 * h, hx + 6 * h, hy - 5 * h, 1)], hat_col)
    elif hat == "bowler":
        flat(c, [RRect(hx - 9 * h, hy - 6 * h, hx + 9 * h, hy - 4 * h, 1), ellipse_top(hx, hy - 5 * h, 6.5 * h, 8 * h)], hat_col)
    elif hat == "kepi":
        flat(c, [RRect(hx - 6 * h, hy - 13 * h, hx + 6 * h, hy - 4 * h, 1), RRect(hx - 2 * h, hy - 6 * h, hx + 10 * h, hy - 4 * h, 1)], hat_col)
    return hx, hy


def lady_west(c, x, base, dress, h=1.0, parasol=None, hat=(240, 230, 210)):
    piece(c, [Poly([(x - 18 * h, base), (x + 14 * h, base), (x + 7 * h, base - 26 * h), (x - 7 * h, base - 26 * h)]), Ell(x - 12 * h, base - 22 * h, 9 * h, 7 * h),
              RRect(x - 6 * h, base - 40 * h, x + 6 * h, base - 24 * h, 3)], dress, border=1.5, shadow=PROP)
    hx, hy = x + 1 * h, base - 47 * h
    flat(c, Circ(hx, hy, 6.4 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    flat(c, Ell(hx - 2 * h, hy - 4 * h, 7 * h, 4 * h), (90, 60, 40))
    if hat:
        flat(c, [Ell(hx, hy - 7 * h, 12 * h, 3 * h), Ell(hx, hy - 10 * h, 6 * h, 4 * h)], hat)
    if parasol:
        flat(c, Thick(x + 10 * h, base - 30 * h, x + 16 * h, base - 70 * h, 1.4), (110, 80, 60))
        piece(c, ellipse_top(x + 16 * h, base - 68 * h, 22 * h, 12 * h), parasol, border=1.2, shadow=SMALL)
    return hx, hy


# ------------------------------------------------------------------- vehicles
def rickshaw(c, x, base, hood=(40, 40, 50), wheel=(60, 50, 44), passenger=(150, 60, 80), puller=(50, 60, 100)):
    c.ellipse_ring(x, base - 26, 26, 26, 3, wheel)
    for k in range(8):
        a = math.pi * k / 4
        flat(c, Thick(x, base - 26, x + 24 * math.cos(a), base - 26 + 24 * math.sin(a), 1.2), wheel)
    piece(c, Poly([(x - 18, base - 34), (x + 20, base - 34), (x + 24, base - 58), (x - 14, base - 60)]), (150, 40, 40), border=1.2, shadow=PROP)
    kimono(c, x + 2, base - 34, passenger, h=0.7, hair="woman")
    piece(c, Poly([(x - 20, base - 34), (x - 22, base - 80), (x + 4, base - 84), (x - 4, base - 60)]), hood, border=1.2, shadow=SMALL)
    flat(c, Thick(x + 20, base - 36, x + 70, base - 30, 2.4), (110, 80, 60))
    ashigaru(c, x + 76, base, puller, h=0.95, weapon=None)


def locomotive(c, x, base, body=(36, 40, 48), trim=(200, 60, 50), wheel=(200, 60, 50), funnel="balloon"):
    """Early steam locomotive facing right, x = cab rear; returns funnel top."""
    piece(c, RRect(x, base - 80, x + 40, base - 28, 2), body, border=1.5, shadow=PROP)
    piece(c, RRect(x - 4, base - 86, x + 44, base - 78, 2), trim, shadow=None)
    flat(c, RRect(x + 8, base - 72, x + 30, base - 56, 2), (190, 210, 220))
    piece(c, [RRect(x + 40, base - 64, x + 150, base - 28, 16), RRect(x + 40, base - 30, x + 160, base - 22, 2)], body, border=1.5, shadow=PROP)
    flat(c, [Thick(x + 70, base - 64, x + 70, base - 28, 2), Thick(x + 110, base - 64, x + 110, base - 28, 2)], trim)
    piece(c, [RRect(x + 84, base - 76, x + 100, base - 62, 4)], (190, 150, 70), shadow=None)
    if funnel == "balloon":
        piece(c, [RRect(x + 128, base - 86, x + 138, base - 62, 1), Poly([(x + 120, base - 104), (x + 146, base - 104), (x + 138, base - 86), (x + 128, base - 86)])],
              body, border=1.2, shadow=SMALL)
        top = (x + 133, base - 106)
    else:
        piece(c, RRect(x + 126, base - 100, x + 140, base - 62, 1), body, border=1.2, shadow=SMALL)
        top = (x + 133, base - 102)
    piece(c, Poly([(x + 150, base - 22), (x + 172, base - 6), (x + 150, base - 6)]), trim, shadow=None)
    for wx, r in ((x + 20, 14), (x + 70, 22), (x + 120, 22)):
        c.ellipse_ring(wx, base - r, r, r, 3.5, wheel)
        flat(c, [Thick(wx - r, base - r, wx + r, base - r, 1.4), Thick(wx, base - 2 * r, wx, base, 1.4), Circ(wx, base - r, 4)], wheel)
    flat(c, Thick(x + 70, base - 22, x + 120, base - 22, 3), (170, 170, 180))
    return top


def steamship(c, x, base, hull=(36, 36, 44), funnel=(200, 60, 50), length=300, masts=2):
    piece(c, Poly([(x, base - 40), (x + length, base - 40), (x + length - 24, base), (x + 20, base)]), hull, border=1.5, shadow=PROP)
    flat(c, Thick(x + 6, base - 34, x + length - 6, base - 34, 3), (200, 60, 50))
    for k in range(int(length // 26) - 1):
        flat(c, Circ(x + 30 + k * 26, base - 24, 3), (220, 210, 170))
    piece(c, RRect(x + length * 0.3, base - 62, x + length * 0.7, base - 40, 2), (240, 236, 226), shadow=SMALL)
    fx = x + length * 0.5
    piece(c, RRect(fx - 10, base - 110, fx + 10, base - 62, 2), funnel, border=1.2, shadow=SMALL)
    flat(c, RRect(fx - 10, base - 110, fx + 10, base - 102, 1), (30, 30, 30))
    for k in range(masts):
        mx = x + length * (0.18 if k == 0 else 0.82)
        flat(c, [Thick(mx, base - 40, mx, base - 160, 3), Thick(mx - 30, base - 130, mx + 30, base - 130, 2)], (110, 80, 60))
    return (fx, base - 112)
