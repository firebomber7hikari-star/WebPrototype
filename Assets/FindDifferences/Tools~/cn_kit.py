# -*- coding: utf-8 -*-
"""Chinese prop library for the Three Kingdoms / Tang / Song levels (paper-craft, scene coordinates, base = ground y)."""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL
from levels_europe import ellipse_top, arch

RED = (186, 52, 42)
GOLDEN = (232, 186, 70)
GLAZE = (226, 170, 50)        # imperial yellow tiles
GREY_TILE = (78, 84, 96)
GREEN_TILE = (60, 120, 100)
BRACKET = (60, 130, 140)
SKIN = (248, 224, 198)
HAIR = (24, 22, 26)


# ------------------------------------------------------------------- architecture
def cn_roof(c, x0, x1, base, h, col=GREY_TILE, curl=16, ornaments=True):
    """Curved roof with swept-up eaves (hip-and-gable silhouette)."""
    w = x1 - x0
    o = 18 + w * 0.04
    pts = [(x0 - o, base - curl), (x0 - o + 10, base + 3)]
    for k in range(1, 6):
        t = k / 6
        pts.append((x0 - o + 10 + (w * 0.24 + o - 10) * t, base + 3 - h * (t ** 1.7)))
    pts.append((x1 - w * 0.24, base - h))
    for k in range(5, 0, -1):
        t = k / 6
        pts.append((x1 + o - 10 - (w * 0.24 + o - 10) * t, base + 3 - h * (t ** 1.7)))
    pts += [(x1 + o - 10, base + 3), (x1 + o, base - curl), (x1 + o - 6, base + 8), (x0 - o + 6, base + 8)]
    piece(c, Poly(pts), col, border=1.5, shadow=PROP)
    for k in range(1, int(w // 9)):
        x = x0 + k * 9
        flat(c, Thick(x, base + 4, x + (x - (x0 + x1) / 2) * 0.1, base - h * 0.55, 0.8), lit(col, 0.84))
    flat(c, Thick(x0 + w * 0.24 - 4, base - h, x1 - w * 0.24 + 4, base - h, 4), lit(col, 0.7))
    if ornaments:
        for sx, k in ((x0 + w * 0.24 - 4, -1), (x1 - w * 0.24 + 4, 1)):
            flat(c, Poly([(sx, base - h + 2), (sx + 6 * k, base - h - 4), (sx + 4 * k, base - h - 12), (sx - 2 * k, base - h - 6)]), lit(col, 0.6))


def bracket_band(c, x0, x1, y, h=8):
    flat(c, RRect(x0, y, x1, y + h, 0), BRACKET)
    for x in range(int(x0 + 4), int(x1 - 4), 12):
        flat(c, RRect(x, y + 2, x + 6, y + h - 2, 1), GOLDEN)


def cn_hall(c, x0, x1, base, top, roof_h, roof=GREY_TILE, pillar=RED, wall=(200, 70, 56), bays=5, terrace=10, doors=True):
    """Hall on a stone terrace: red pillars, lattice doors, bracket band, curved roof."""
    piece(c, RRect(x0 - 16, base - terrace, x1 + 16, base, 1), (206, 200, 186), border=1.5, shadow=PROP)
    piece(c, RRect(x0, top, x1, base - terrace, 0), wall, border=1.5, shadow=PROP)
    bw = (x1 - x0) / bays
    for k in range(bays):
        bx = x0 + k * bw
        if doors:
            flat(c, RRect(bx + 5, top + 12, bx + bw - 5, base - terrace - 2, 1), lit(wall, 0.82))
            for gx in range(int(bx + 9), int(bx + bw - 6), 6):
                flat(c, Thick(gx, top + 16, gx, top + (base - terrace - top) * 0.55, 1), (240, 210, 150))
            for gy in range(int(top + 18), int(top + (base - terrace - top) * 0.55), 6):
                flat(c, Thick(bx + 8, gy, bx + bw - 8, gy, 1), (240, 210, 150))
    for k in range(bays + 1):
        px = x0 + k * bw
        piece(c, RRect(px - 3.5, top, px + 3.5, base - terrace, 1), pillar, shadow=SMALL)
    bracket_band(c, x0 - 4, x1 + 4, top - 8)
    cn_roof(c, x0, x1, top - 8, roof_h, roof)


def pagoda(c, x, base, w0, tiers, tier_h, wall=(236, 226, 200), roof=GREY_TILE, shrink=0.12, finial=True):
    top = base
    for k in range(tiers):
        w = w0 * (1 - shrink * k)
        piece(c, RRect(x - w / 2, top - tier_h, x + w / 2, top, 1), wall, border=1.2, shadow=PROP)
        flat(c, arch(x - 5, x + 5, top - tier_h + 6, top - 4), (70, 56, 50))
        cn_roof(c, x - w / 2, x + w / 2, top - tier_h, 10, roof, curl=8, ornaments=False)
        top -= tier_h + 6
    if finial:
        flat(c, [Thick(x, top + 6, x, top - 26, 2.5)] + [Circ(x, top - 4 - k * 7, 4 - k * 0.6) for k in range(4)], GOLDEN)
    return top


def city_wall(c, x0, x1, top, base, col=(150, 142, 130)):
    piece(c, RRect(x0, top, x1, base, 0), col, border=1.5, shadow=PROP)
    for y in range(int(top + 10), int(base), 12):
        off = ((y - top) // 12 % 2) * 12
        for x in range(int(x0 + off), int(x1), 24):
            flat(c, Thick(x, y, x, y + 12, 0.8), lit(col, 0.86))
        flat(c, Thick(x0, y, x1, y, 0.8), lit(col, 0.86))
    for x in range(int(x0), int(x1) - 8, 18):
        piece(c, RRect(x, top - 10, x + 10, top + 1, 0), col, shadow=None)


def gate_tower(c, x, wall_top, w=160, h=60, roof=GREY_TILE, gate=True, gate_base=None):
    if gate and gate_base:
        flat(c, arch(x - 24, x + 24, wall_top + 30, gate_base), (40, 34, 30))
    cn_hall(c, x - w / 2, x + w / 2, wall_top, wall_top - h, 26, roof, bays=5, terrace=6)
    cn_roof(c, x - w * 0.38, x + w * 0.38, wall_top - h - 30, 22, roof)


def arch_bridge(c, x0, x1, base, top, col=(200, 196, 184)):
    n = 20
    arc = [(x0 + (x1 - x0) * k / n, base - (base - top) * math.sin(math.pi * k / n)) for k in range(n + 1)]
    piece(c, Poly(arc + [(x1, base + 10), (x0, base + 10)]), col, border=1.5, shadow=PROP)
    cx = (x0 + x1) / 2
    flat(c, ellipse_top(cx, base + 10, (x1 - x0) * 0.22, (base - top) * 0.8), (60, 90, 110))
    rail = [(x, y - 12) for x, y in arc]
    flat(c, [Thick(rail[i][0], rail[i][1], rail[i + 1][0], rail[i + 1][1], 2.5) for i in range(n)], lit(col, 0.85))
    for i in range(0, n + 1, 2):
        flat(c, Thick(arc[i][0], arc[i][1], rail[i][0], rail[i][1] - 3, 2.5), lit(col, 0.85))


def lantern_cn(c, x, y, col=(220, 50, 40), r=10):
    flat(c, Thick(x, y - r - 6, x, y - r, 1.2), (60, 50, 50))
    piece(c, Ell(x, y, r * 1.1, r), col, border=1, shadow=SMALL)
    flat(c, [RRect(x - r * 0.45, y - r - 1, x + r * 0.45, y - r + 2, 1), RRect(x - r * 0.45, y + r - 2, x + r * 0.45, y + r + 1, 1)], GOLDEN)
    flat(c, [Thick(x, y + r + 1, x, y + r + 10, 1.4)], GOLDEN)
    for k in (-0.5, 0, 0.5):
        flat(c, Thick(x + r * k, y - r * 0.9, x + r * k, y + r * 0.9, 0.6), lit(col, 0.8))


def bamboo(c, x0, x1, top, base, seed, col=(110, 160, 100)):
    rnd = random.Random(seed)
    for _ in range(int((x1 - x0) // 14)):
        x = rnd.uniform(x0, x1)
        cc = lit(col, rnd.uniform(0.85, 1.1))
        flat(c, Thick(x, base, x, top + rnd.uniform(0, 40), rnd.uniform(4, 7)), cc)
        for y in range(int(top + 40), int(base), 34):
            flat(c, Thick(x - 4, y, x + 4, y, 1.4), lit(cc, 0.8))
        for k in range(3):
            y = top + rnd.uniform(20, base - top - 20)
            flat(c, Poly([(x, y), (x + rnd.choice((-1, 1)) * 18, y - 5), (x, y - 3)]), lit(cc, 1.1))


def lotus_pond(c, items, pad=(90, 150, 90), flower=(240, 150, 180)):
    for x, y, f in items:
        flat(c, Ell(x, y, 20, 6), pad)
        if f:
            piece(c, Poly([(x - 7, y - 2), (x + 7, y - 2), (x + 9, y - 10), (x + 4, y - 6), (x, y - 16), (x - 4, y - 6), (x - 9, y - 10)]),
                  f if isinstance(f, tuple) else flower, shadow=SMALL)


# ------------------------------------------------------------------- people
def hanfu(c, x, base, robe, h=1.0, hat="futou", beard=None, hat_col=(30, 28, 32), sash=(230, 200, 120)):
    """Figure in a long robe with wide sleeves. hat: futou / guan / lady / tang_lady / straw / none. Returns head."""
    piece(c, [Poly([(x - 12 * h, base), (x + 12 * h, base), (x + 8 * h, base - 32 * h), (x - 8 * h, base - 32 * h)]),
              Poly([(x - 8 * h, base - 30 * h), (x - 20 * h, base - 12 * h), (x - 10 * h, base - 8 * h)]),
              Poly([(x + 8 * h, base - 30 * h), (x + 20 * h, base - 12 * h), (x + 10 * h, base - 8 * h)])], robe, border=1.5, shadow=PROP)
    flat(c, RRect(x - 8.5 * h, base - 20 * h, x + 8.5 * h, base - 16 * h, 1), sash)
    flat(c, Poly([(x - 3 * h, base - 32 * h), (x + 3 * h, base - 32 * h), (x, base - 22 * h)]), (240, 236, 226))
    hx, hy = x + 1 * h, base - 40 * h
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    if beard:
        flat(c, Poly([(hx - 3 * h, hy + 3 * h), (hx + 5 * h, hy + 3 * h), (hx + 1 * h, hy + 16 * h)]), beard)
    if hat == "futou":
        flat(c, [ellipse_top(hx, hy - 4 * h, 7 * h, 8 * h), Thick(hx - 6 * h, hy - 6 * h, hx - 16 * h, hy - 2 * h, 1.6 * h)], hat_col)
    elif hat == "wing":          # Song official hat with long side wings
        flat(c, [RRect(hx - 6 * h, hy - 13 * h, hx + 6 * h, hy - 4 * h, 1), Thick(hx - 24 * h, hy - 8 * h, hx + 24 * h, hy - 8 * h, 1.6 * h)], hat_col)
    elif hat == "guan":
        flat(c, [Ell(hx - 1 * h, hy - 6 * h, 7 * h, 3 * h), RRect(hx - 3 * h, hy - 14 * h, hx + 3 * h, hy - 6 * h, 1)], hat_col)
        flat(c, Thick(hx - 6 * h, hy - 11 * h, hx + 6 * h, hy - 11 * h, 1.2), GOLDEN)
    elif hat == "lady":
        flat(c, [Ell(hx - 2 * h, hy - 5 * h, 8 * h, 4 * h), Circ(hx - 3 * h, hy - 12 * h, 5 * h)], HAIR)
        flat(c, Thick(hx - 8 * h, hy - 14 * h, hx + 4 * h, hy - 16 * h, 1.2), GOLDEN)
    elif hat == "tang_lady":
        flat(c, [Ell(hx - 2 * h, hy - 5 * h, 8 * h, 4 * h), Ell(hx - 2 * h, hy - 14 * h, 7 * h, 7 * h), Circ(hx + 4 * h, hy - 18 * h, 4 * h)], HAIR)
        flat(c, Circ(hx + 6 * h, hy - 12 * h, 2.4 * h), (230, 60, 90))
    elif hat == "straw":
        flat(c, Poly([(hx - 15 * h, hy - 3 * h), (hx + 15 * h, hy - 3 * h), (hx, hy - 13 * h)]), hat_col)
    elif hat == "bun":
        flat(c, [Ell(hx - 2 * h, hy - 5 * h, 7 * h, 3 * h), Circ(hx - 1 * h, hy - 10 * h, 3.5 * h)], HAIR)
    return hx, hy


def warrior(c, x, base, armor, h=1.0, helmet=(110, 110, 120), plume=(200, 40, 40), face=SKIN, beard=None, weapon=None, weapon_col=(200, 200, 210)):
    """Armoured general; weapon: spear / blade (crescent glaive) / snake (serpent spear) / sword / None."""
    piece(c, [Poly([(x - 13 * h, base - 10 * h), (x + 13 * h, base - 10 * h), (x + 9 * h, base - 34 * h), (x - 9 * h, base - 34 * h)]),
              RRect(x - 7 * h, base - 12 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 12 * h, x + 7 * h, base, 1),
              Poly([(x - 9 * h, base - 34 * h), (x - 16 * h, base - 28 * h), (x - 9 * h, base - 26 * h)]),
              Poly([(x + 9 * h, base - 34 * h), (x + 16 * h, base - 28 * h), (x + 9 * h, base - 26 * h)])], armor, border=1.5, shadow=PROP)
    for k in range(4):
        for j in range(4):
            flat(c, Circ(x - 7 * h + j * 4.6 * h, base - 30 * h + k * 5 * h, 1.4 * h), lit(armor, 1.2))
    hx, hy = x + 1 * h, base - 41 * h
    flat(c, Circ(hx, hy, 6.5 * h), face)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    if beard:
        flat(c, Poly([(hx - 4 * h, hy + 2 * h), (hx + 6 * h, hy + 2 * h), (hx + 1 * h, hy + 18 * h)]), beard)
    piece(c, [ellipse_top(hx, hy - 3 * h, 8 * h, 9 * h), RRect(hx - 9 * h, hy - 4 * h, hx + 9 * h, hy - 1 * h, 1)], helmet, shadow=None)
    if plume:
        flat(c, [Thick(hx, hy - 11 * h, hx - 4 * h, hy - 24 * h, 3 * h)], plume)
    if weapon:
        flat(c, Thick(x + 14 * h, base, x + 18 * h, base - 120 * h, 2.2), (110, 80, 60))
        tx, ty = x + 18 * h, base - 120 * h
        if weapon == "spear":
            flat(c, Poly([(tx - 2.5 * h, ty), (tx + 2.5 * h, ty), (tx, ty - 16 * h)]), weapon_col)
        elif weapon == "blade":
            flat(c, Poly([(tx - 2 * h, ty + 6 * h), (tx + 14 * h, ty - 4 * h), (tx + 10 * h, ty - 22 * h), (tx, ty - 26 * h), (tx + 2 * h, ty - 6 * h)]),
                 weapon_col)
        elif weapon == "snake":
            pts = [(tx + 3 * h * math.sin(k * 1.4), ty - k * 5 * h) for k in range(5)]
            flat(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 2.6 * h) for k in range(4)], weapon_col)
        elif weapon == "sword":
            flat(c, Thick(tx - 10 * h, ty + 70 * h, tx - 2 * h, ty + 40 * h, 2.6 * h), weapon_col)
    return hx, hy


def horse_cn(c, x, base, col, flip=False, mane=(40, 34, 34), saddle=(160, 40, 40)):
    s = -1 if flip else 1
    for lx in (-22, -12, 14, 24):
        flat(c, RRect(x + lx * s - 3, base - 32, x + lx * s + 3, base, 1), lit(col, 0.8))
    piece(c, [Ell(x, base - 38, 34, 15), Poly([(x + 28 * s, base - 44), (x + 42 * s, base - 76), (x + 52 * s, base - 72), (x + 40 * s, base - 40)]),
              Ell(x + 52 * s, base - 74, 12, 7)], col, border=1.5, shadow=PROP)
    flat(c, [Thick(x + 32 * s, base - 50, x + 42 * s, base - 78, 4), Thick(x - 32 * s, base - 42, x - 42 * s, base - 22, 4)], mane)
    flat(c, RRect(x - 12, base - 54, x + 12, base - 44, 3), saddle)
    flat(c, Circ(x + 54 * s, base - 76, 1.4), INK)


def camel(c, x, base, col=(200, 160, 110), flip=False, load=(150, 60, 50)):
    s = -1 if flip else 1
    for lx in (-20, -10, 12, 22):
        flat(c, RRect(x + lx * s - 3, base - 36, x + lx * s + 3, base, 1), lit(col, 0.8))
    piece(c, [Ell(x, base - 44, 32, 14), Ell(x - 8 * s, base - 58, 10, 10), Ell(x + 10 * s, base - 58, 10, 10),
              Poly([(x + 26 * s, base - 46), (x + 40 * s, base - 70), (x + 48 * s, base - 66), (x + 34 * s, base - 40)]), Ell(x + 50 * s, base - 70, 10, 6)],
          col, border=1.5, shadow=PROP)
    flat(c, RRect(x - 18, base - 66, x + 18, base - 50, 3), load)
    flat(c, Circ(x + 52 * s, base - 72, 1.4), INK)


def junk(c, x, base, length=180, hull=(120, 80, 56), sail=(200, 150, 100), masts=2, roof=None):
    piece(c, Poly([(x, base - 30), (x + length, base - 34), (x + length - 20, base), (x + 16, base)]), hull, border=1.5, shadow=PROP)
    flat(c, Thick(x + 6, base - 26, x + length - 8, base - 30, 2.5), lit(hull, 0.7))
    if roof:
        piece(c, RRect(x + length * 0.3, base - 56, x + length * 0.62, base - 30, 3), roof, border=1.2, shadow=SMALL)
    for k in range(masts):
        mx = x + length * (0.3 + 0.38 * k)
        mh = 120 if k == 0 else 92
        flat(c, Thick(mx, base - 30, mx, base - 30 - mh, 3), (110, 80, 60))
        if sail:
            piece(c, Poly([(mx - 4, base - 30 - mh + 6), (mx + 46, base - 30 - mh + 14), (mx + 40, base - 46), (mx - 4, base - 44)]), sail,
                  border=1.2, shadow=SMALL)
            for j in range(1, 6):
                y0 = base - 30 - mh + 6 + j * (mh - 20) / 6
                flat(c, Thick(mx - 4, y0, mx + 44 - j * 0.8, y0 + 6, 1), lit(sail, 0.75))
