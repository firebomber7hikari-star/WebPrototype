# -*- coding: utf-8 -*-
"""Style-agnostic props and characters for the render-style series (Level1585-1619).

Everything draws through the small style interface of levels_remake (ToonS / RealS / ComicS / PersonaS):
    S.obj(g, shape, col, seed, kind, depth, line, hi)   S.flat(g, shape, col)   S.shadow(g, shape, k)
    S.line(g, x0, y0, x1, y1, w, col)                   S.glow(g, x, y, r, col, k)
so one scene description renders as cel-shaded JRPG, American comic or realistic.
All characters, monsters, vehicles and signs are original designs; signs carry no readable text or brands.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Union, el, mixc

SKIN = (250, 214, 180)


def sh_shadow(S, g, x, base, rx, ry=6, k=1.0):
    S.shadow(g, Ell(x, base, rx, ry), k)


# =================================================================== architecture
def building(S, g, x0, x1, top, base, col, seed=0, rows=3, cols=3, lit=(), win=(150, 190, 220), roof=None, depth=0.0,
             skip=(), lit_col=(255, 220, 140), door=True, ledge=True):
    """Box building with a grid of windows (lit = set of (r, c)), optional pitched roof colour."""
    S.obj(g, Box(x0, top, x1, base), col, seed, "stone" if depth < 0.3 else "plain", depth=depth)
    if roof is not None:
        S.obj(g, Poly([(x0 - 8, top + 2), ((x0 + x1) / 2, top - (x1 - x0) * 0.32), (x1 + 8, top + 2)]), roof, seed + 1, "roof", depth=depth)
    if ledge:
        S.flat(g, Box(x0 - 3, top - 2, x1 + 3, top + 4), mixc(col, (0, 0, 0), 0.3))
    ww = (x1 - x0) / (cols * 2 + 1)
    hh = (base - top - (40 if door else 10)) / (rows * 2 + 1)
    for r in range(rows):
        for c in range(cols):
            if (r, c) in skip:
                continue
            wx = x0 + ww * (1 + c * 2)
            wy = top + hh * (1 + r * 2)
            on = (r, c) in lit
            if on:
                S.glow(g, wx + ww / 2, wy + hh / 2, ww * 1.6, lit_col, 0.2)
            S.obj(g, Box(wx, wy, wx + ww, wy + hh, 1), lit_col if on else mixc(win, col, depth * 0.5), seed + 10 + r * 7 + c,
                  depth=depth, line=depth < 0.4, hi=not on)
    if door:
        dx = (x0 + x1) / 2
        S.obj(g, Box(dx - 12, base - 34, dx + 12, base, 2), mixc(col, (60, 40, 30), 0.6), seed + 2, "wood", depth=depth)


def tower(S, g, cx, base, w, h, col, roof, seed=0, depth=0.0, windows=2, flag=None, lit=False):
    S.obj(g, Box(cx - w / 2, base - h, cx + w / 2, base), col, seed, "stone", depth=depth)
    S.obj(g, Poly([(cx - w / 2 - 8, base - h + 2), (cx, base - h - w * 1.1), (cx + w / 2 + 8, base - h + 2)]), roof, seed + 1, "roof", depth=depth)
    for i in range(windows):
        y = base - h + 30 + i * 46
        c = (255, 220, 140) if lit and i == 0 else (60, 60, 90)
        S.obj(g, Union([Box(cx - 6, y, cx + 6, y + 22), Circ(cx, y, 6)]), c, seed + 2 + i, depth=depth)
    if flag is not None:
        top = base - h - w * 1.1
        S.line(g, cx, top, cx, top - 34, 1.6, (90, 80, 70))
        S.obj(g, Poly([(cx + 1, top - 34), (cx + 30, top - 27), (cx + 1, top - 20)]), flag, seed + 5, depth=depth)


def castle(S, g, cx, base, w, h, col, roof, seed=0, depth=0.0, flags=((200, 50, 60), (200, 50, 60)), gate=True):
    """Fairy-tale castle: curtain wall with crenels, keep, two flanking towers."""
    S.obj(g, Box(cx - w / 2, base - h * 0.45, cx + w / 2, base), col, seed, "stone", depth=depth)
    for x in np.arange(cx - w / 2, cx + w / 2 - 6, 16):
        S.obj(g, Box(x, base - h * 0.45 - 10, x + 10, base - h * 0.45 + 1), col, seed + 1, depth=depth, line=False)
    S.obj(g, Box(cx - w * 0.18, base - h * 0.8, cx + w * 0.18, base - h * 0.4), col, seed + 2, "stone", depth=depth)
    S.obj(g, Poly([(cx - w * 0.2, base - h * 0.8), (cx, base - h * 1.1), (cx + w * 0.2, base - h * 0.8)]), roof, seed + 3, "roof", depth=depth)
    for i, sx in enumerate((-1, 1)):
        tower(S, g, cx + sx * w * 0.42, base, w * 0.16, h * 0.7, col, roof, seed + 4 + i * 5, depth=depth, windows=1,
              flag=flags[i] if flags else None)
    if gate:
        S.obj(g, Union([Box(cx - w * 0.07, base - h * 0.22, cx + w * 0.07, base), Circ(cx, base - h * 0.22, w * 0.07)]), (50, 40, 50), seed + 9, depth=depth)


# =================================================================== nature
def round_tree(S, g, x, base, h, col=(90, 170, 70), trunk=(130, 90, 60), seed=0, depth=0.0):
    S.obj(g, Box(x - h * 0.05, base - h * 0.45, x + h * 0.05, base), trunk, seed, "wood", depth=depth)
    rnd = random.Random(seed)
    blobs = [Circ(x + rnd.uniform(-0.2, 0.2) * h, base - h * (0.55 + rnd.uniform(0, 0.3)), h * rnd.uniform(0.18, 0.26)) for _ in range(4)]
    S.obj(g, Union([Circ(x, base - h * 0.65, h * 0.32)] + blobs), col, seed + 1, "foliage", depth=depth, hi=True)


def pine_tree(S, g, x, base, h, col=(60, 120, 80), seed=0, depth=0.0, snow=None):
    S.obj(g, Box(x - h * 0.04, base - h * 0.2, x + h * 0.04, base), (110, 76, 50), seed, "wood", depth=depth)
    tiers = [Poly([(x - h * (0.36 - i * 0.09), base - h * (0.18 + i * 0.24)), (x, base - h * (0.52 + i * 0.24)),
                   (x + h * (0.36 - i * 0.09), base - h * (0.18 + i * 0.24))]) for i in range(3)]
    S.obj(g, Union(tiers), col, seed + 1, "foliage", depth=depth)
    if snow:
        for i in range(3):
            S.flat(g, Poly([(x - h * 0.12, base - h * (0.4 + i * 0.24)), (x, base - h * (0.52 + i * 0.24)), (x + h * 0.12, base - h * (0.4 + i * 0.24))]), snow)


def palm(S, g, x, base, h, lean=0.15, col=(70, 150, 70), trunk=(150, 115, 80), seed=0, depth=0.0):
    tx, ty = x + lean * h, base - h
    segs = []
    for i in range(10):
        t0, t1 = i / 10, (i + 1) / 10
        segs.append(Seg(x + lean * h * t0 ** 1.6, base - h * t0, x + lean * h * t1 ** 1.6, base - h * t1, h * 0.035 * (1 - t0 * 0.4) + 1))
    S.obj(g, Union(segs), trunk, seed, "wood", depth=depth)
    fronds = []
    for a in (-2.8, -2.2, -1.6, -0.9, -0.3, 0.3):
        ex, ey = tx + math.cos(a) * h * 0.42, ty + math.sin(a) * h * 0.18 + h * 0.16
        mx, my = tx + math.cos(a) * h * 0.22, ty - h * 0.06 + math.sin(a) * h * 0.1
        fronds.append(Poly([(tx, ty), (mx, my - h * 0.04), (ex, ey), (mx, my + h * 0.03)]))
    S.obj(g, Union(fronds), col, seed + 1, "foliage", depth=depth)


def rock(S, g, x, base, r, col=(140, 136, 130), seed=0, depth=0.0):
    S.obj(g, Rough(Ell(x, base - r * 0.55, r, r * 0.6), r * 0.12, r * 0.4, seed), col, seed, "stone", depth=depth, hi=True)


def bush(S, g, x, base, r, col=(80, 150, 70), seed=0, flowers=None):
    S.obj(g, Union([Circ(x - r * 0.6, base - r * 0.6, r * 0.65), Circ(x, base - r * 0.9, r * 0.8), Circ(x + r * 0.7, base - r * 0.6, r * 0.6)]),
          col, seed, "foliage", hi=True)
    if flowers:
        rnd = random.Random(seed)
        for _ in range(5):
            S.flat(g, Circ(x + rnd.uniform(-r, r), base - r * rnd.uniform(0.4, 1.3), r * 0.12), flowers)


# =================================================================== props
def chest(S, g, x, base, w=40, col=(150, 90, 40), trim=(230, 190, 70), open_=False, gold=True, seed=0):
    h = w * 0.6
    sh_shadow(S, g, x, base, w * 0.6, 5)
    S.obj(g, Box(x - w / 2, base - h, x + w / 2, base, 2), col, seed, "wood")
    if open_:
        S.obj(g, Poly([(x - w / 2, base - h), (x + w / 2, base - h), (x + w / 2 + 4, base - h * 1.9), (x - w / 2 + 4, base - h * 1.9)]), col, seed + 1, "wood")
        if gold:
            S.obj(g, Ell(x, base - h, w * 0.42, h * 0.3), (250, 210, 70), seed + 2, hi=True)
    else:
        S.obj(g, Union([Box(x - w / 2, base - h * 1.5, x + w / 2, base - h + 2), Ell(x, base - h * 1.5, w / 2, h * 0.3)]), col, seed + 1, "wood")
    S.flat(g, Box(x - w / 2, base - h * 0.62, x + w / 2, base - h * 0.5), trim)
    S.obj(g, Box(x - 4, base - h * 0.75, x + 4, base - h * 0.4, 1), trim, seed + 3)


def barrel(S, g, x, base, r=16, h=40, col=(140, 96, 56), seed=0):
    sh_shadow(S, g, x, base, r * 1.2, 4)
    S.obj(g, Box(x - r, base - h, x + r, base, r * 0.3), col, seed, "wood", hi=True)
    for yy in (base - h * 0.2, base - h * 0.8):
        S.flat(g, Box(x - r, yy - 2, x + r, yy + 2), (80, 76, 80))


def crate(S, g, x0, base, w=40, h=36, col=(170, 126, 76), seed=0):
    S.obj(g, Box(x0, base - h, x0 + w, base, 1), col, seed, "wood")
    S.line(g, x0 + 4, base - 4, x0 + w - 4, base - h + 4, 2, mixc(col, (0, 0, 0), 0.25))


def torch(S, g, x, y, lit=True):
    S.line(g, x, y + 30, x, y + 4, 3, (90, 70, 50))
    S.obj(g, Poly([(x - 7, y + 6), (x + 7, y + 6), (x + 5, y - 2), (x - 5, y - 2)]), (110, 80, 50), 1)
    if lit:
        S.glow(g, x, y - 10, 70, (255, 170, 80), 0.35)
        S.obj(g, Union([Ell(x, y - 6, 6, 7), Poly([(x - 6, y - 8), (x, y - 28), (x + 6, y - 8)])]), (255, 190, 80), 2, line=False)
        S.flat(g, Ell(x, y - 6, 3, 4), (255, 245, 200))


def lamp_post(S, g, x, base, h, lit=True, col=(50, 52, 60), light=(255, 220, 150)):
    S.obj(g, Box(x - 3, base - h, x + 3, base), col, 0)
    S.obj(g, Box(x - 8, base - 6, x + 8, base, 1), col, 1)
    if lit:
        S.glow(g, x, base - h - 6, 70, light, 0.35)
    S.obj(g, Union([Box(x - 9, base - h - 16, x + 9, base - h), Poly([(x - 12, base - h - 16), (x, base - h - 26), (x + 12, base - h - 16)])]),
          light if lit else (90, 100, 120), 2)


def banner(S, g, x, top, w, h, col, emblem_col=(250, 220, 90), emblem="star", seed=0):
    S.line(g, x - w * 0.6, top, x + w * 0.6, top, 2, (110, 80, 50))
    S.obj(g, Poly([(x - w / 2, top), (x + w / 2, top), (x + w / 2, top + h), (x, top + h * 0.82), (x - w / 2, top + h)]), col, seed, "fabric")
    cy = top + h * 0.4
    if emblem == "star":
        pts = [(x + math.cos(-math.pi / 2 + k * math.pi / 5) * (w * 0.22 if k % 2 == 0 else w * 0.09),
                cy + math.sin(-math.pi / 2 + k * math.pi / 5) * (w * 0.22 if k % 2 == 0 else w * 0.09)) for k in range(10)]
        S.flat(g, Poly(pts), emblem_col)
    elif emblem == "circle":
        S.flat(g, Circ(x, cy, w * 0.2), emblem_col)
    elif emblem == "cross":
        S.flat(g, Union([Box(x - w * 0.05, cy - w * 0.22, x + w * 0.05, cy + w * 0.22), Box(x - w * 0.18, cy - w * 0.05, x + w * 0.18, cy + w * 0.05)]), emblem_col)


def sign_board(S, g, x0, y0, x1, y1, col, mark_col=(250, 240, 220), seed=0, marks=3):
    """Blank shop sign with abstract stroke 'lettering' (no readable text)."""
    S.obj(g, Box(x0, y0, x1, y1, 3), col, seed)
    rnd = random.Random(seed)
    w = (x1 - x0 - 16) / marks
    for k in range(marks):
        cx = x0 + 8 + w * (k + 0.5)
        S.flat(g, Box(cx - w * 0.32, (y0 + y1) / 2 - (y1 - y0) * 0.2, cx + w * 0.32, (y0 + y1) / 2 + (y1 - y0) * 0.2, 2), mark_col)
        S.flat(g, Box(cx - w * 0.1, (y0 + y1) / 2 - (y1 - y0) * rnd.uniform(0.05, 0.15), cx + w * 0.1, (y0 + y1) / 2 + (y1 - y0) * 0.25), col)


def potion(S, g, x, base, col, s=1.0, seed=0):
    S.obj(g, Union([Circ(x, base - 10 * s, 10 * s), Box(x - 3 * s, base - 28 * s, x + 3 * s, base - 16 * s)]), col, seed, hi=True)
    S.obj(g, Box(x - 4 * s, base - 32 * s, x + 4 * s, base - 26 * s, 1), (150, 110, 70), seed + 1)


def crystal(S, g, x, base, h, col, seed=0, tilt=0.0):
    tip = (x + math.sin(tilt) * h, base - math.cos(tilt) * h)
    S.obj(g, Poly([(x - h * 0.16, base), (x - h * 0.2, base - h * 0.6), tip, (x + h * 0.2, base - h * 0.6), (x + h * 0.16, base)]), col, seed, hi=True)


def coin_pile(S, g, x, base, w, seed=0):
    S.obj(g, Ell(x, base - w * 0.12, w / 2, w * 0.16), (240, 196, 60), seed, hi=True)
    rnd = random.Random(seed)
    for _ in range(int(w / 6)):
        cx = x + rnd.uniform(-w * 0.4, w * 0.4)
        cy = base - w * rnd.uniform(0.12, 0.3)
        S.obj(g, Ell(cx, cy, 5, 2.4), (255, 220, 90), seed + 3, line=False)


# =================================================================== characters (original designs)
def person(S, g, x, base, h, shirt, pants=(60, 70, 110), skin=SKIN, hair=(80, 56, 40), face=1, seed=0, hat=None, skirt=False,
           arm_up=False, hair_long=False, bag=None):
    """Simple stylised human (~6.5 heads tall), facing `face`."""
    k = h / 200.0
    sh_shadow(S, g, x, base, 26 * k, 5 * k)
    if skirt:
        S.obj(g, Poly([(x - 24 * k, base - 70 * k), (x + 24 * k, base - 70 * k), (x + 16 * k, base - 112 * k), (x - 16 * k, base - 112 * k)]), pants, seed)
        for dx in (-9, 9):
            S.obj(g, Box(x + (dx - 4) * k, base - 72 * k, x + (dx + 4) * k, base - 4 * k, 3 * k), skin, seed + 1)
    else:
        for dx in (-9, 9):
            S.obj(g, Box(x + (dx - 6) * k, base - 100 * k, x + (dx + 6) * k, base - 4 * k, 3 * k), pants, seed + 1)
    for dx in (-9, 9):
        S.obj(g, Ell(x + (dx + face * 4) * k, base - 4 * k, 9 * k, 5 * k), (50, 44, 44), seed + 2)
    S.obj(g, Box(x - 18 * k, base - 160 * k, x + 18 * k, base - 96 * k, 8 * k), shirt, seed + 3)
    if arm_up:
        S.obj(g, Seg(x + face * 16 * k, base - 152 * k, x + face * 34 * k, base - 196 * k, 6 * k), shirt, seed + 4)
    else:
        S.obj(g, Seg(x + face * 18 * k, base - 152 * k, x + face * 22 * k, base - 104 * k, 6 * k), shirt, seed + 4)
    S.obj(g, Seg(x - face * 18 * k, base - 152 * k, x - face * 22 * k, base - 104 * k, 6 * k), shirt, seed + 5)
    if bag is not None:
        S.obj(g, Box(x - face * 30 * k, base - 120 * k, x - face * 12 * k, base - 96 * k, 3 * k), bag, seed + 6)
    S.obj(g, Box(x - 5 * k, base - 172 * k, x + 5 * k, base - 158 * k), skin, seed + 7, line=False)
    S.obj(g, Ell(x + face * 2 * k, base - 184 * k, 15 * k, 17 * k), skin, seed + 8)
    hs = Union([Ell(x - face * 2 * k, base - 192 * k, 16 * k, 12 * k)] + ([Box(x - face * 16 * k - 4 * k, base - 192 * k, x - face * 4 * k, base - 150 * k, 4 * k)] if hair_long else []))
    S.obj(g, hs, hair, seed + 9)
    S.flat(g, Circ(x + face * 9 * k, base - 184 * k, 1.8 * k), (40, 30, 30))
    if hat is not None:
        S.obj(g, Union([Ell(x, base - 196 * k, 22 * k, 5 * k), Box(x - 14 * k, base - 214 * k, x + 14 * k, base - 196 * k, 5 * k)]), hat, seed + 10)


def hero(S, g, x, base, h, tunic=(60, 110, 200), cape=(200, 50, 60), hair=(250, 200, 80), skin=SKIN, face=1, seed=0,
         sword=True, shield=None, armor=(200, 205, 215), cape_on=True, hair_spiky=True):
    """Chibi JRPG hero (~4 heads tall): spiky hair, cape, tunic, sword raised behind."""
    k = h / 200.0
    f = face
    sh_shadow(S, g, x, base, 34 * k, 6 * k)
    if cape_on:
        S.obj(g, Poly([(x - f * 6 * k, base - 120 * k), (x + f * 18 * k, base - 120 * k), (x - f * 10 * k, base - 20 * k), (x - f * 48 * k, base - 30 * k)]), cape, seed, "fabric")
    if sword:
        S.obj(g, Poly([(x - f * 30 * k, base - 92 * k), (x - f * 24 * k, base - 98 * k), (x - f * 66 * k, base - 196 * k), (x - f * 72 * k, base - 192 * k)]), (220, 230, 240), seed + 1, hi=True)
        S.obj(g, Seg(x - f * 18 * k, base - 92 * k, x - f * 38 * k, base - 102 * k, 4 * k), (200, 160, 60), seed + 2)
    for dx in (-10, 10):
        S.obj(g, Box(x + (dx - 7) * k, base - 50 * k, x + (dx + 7) * k, base - 4 * k, 3 * k), (70, 60, 60), seed + 3)
        S.obj(g, Ell(x + (dx + f * 4) * k, base - 6 * k, 11 * k, 6 * k), (110, 70, 40), seed + 4)
    S.obj(g, Poly([(x - 24 * k, base - 44 * k), (x + 24 * k, base - 44 * k), (x + 20 * k, base - 112 * k), (x - 20 * k, base - 112 * k)]), tunic, seed + 5)
    S.obj(g, Box(x - 22 * k, base - 62 * k, x + 22 * k, base - 54 * k), (120, 80, 50), seed + 6, line=False)
    S.obj(g, Ell(x - 18 * k, base - 108 * k, 12 * k, 9 * k), armor, seed + 7, hi=True)
    S.obj(g, Ell(x + 18 * k, base - 108 * k, 12 * k, 9 * k), armor, seed + 8, hi=True)
    S.obj(g, Seg(x + f * 22 * k, base - 104 * k, x + f * 28 * k, base - 70 * k, 7 * k), tunic, seed + 9)
    if shield is not None:
        S.obj(g, Union([Box(x + f * 20 * k, base - 96 * k, x + f * 50 * k, base - 60 * k), Circ(x + f * 35 * k, base - 60 * k, 15 * k)]), shield, seed + 10, hi=True)
        S.flat(g, Circ(x + f * 35 * k, base - 76 * k, 6 * k), (250, 220, 90))
    # big head
    hx, hy = x + f * 2 * k, base - 150 * k
    S.obj(g, Ell(hx, hy, 34 * k, 36 * k), skin, seed + 11)
    if hair_spiky:
        spikes = [Poly([(hx - 36 * k, hy - 6 * k), (hx - 50 * k, hy - 30 * k), (hx - 20 * k, hy - 30 * k)]),
                  Poly([(hx - 24 * k, hy - 26 * k), (hx - 30 * k, hy - 62 * k), (hx, hy - 36 * k)]),
                  Poly([(hx - 6 * k, hy - 34 * k), (hx + 8 * k, hy - 70 * k), (hx + 20 * k, hy - 32 * k)]),
                  Poly([(hx + 14 * k, hy - 28 * k), (hx + 44 * k, hy - 46 * k), (hx + 34 * k, hy - 8 * k)])]
        S.obj(g, Union([Ell(hx - f * 4 * k, hy - 16 * k, 36 * k, 24 * k)] + spikes), hair, seed + 12, hi=True)
    else:
        S.obj(g, Union([Ell(hx - f * 4 * k, hy - 16 * k, 37 * k, 26 * k), Box(hx - f * 36 * k, hy - 16 * k, hx - f * 22 * k, hy + 30 * k, 8 * k)]), hair, seed + 12, hi=True)
    for ex in (8, 22):
        S.flat(g, Ell(hx + f * ex * k, hy + 6 * k, 4 * k, 7 * k), (40, 40, 70))
        S.flat(g, Circ(hx + f * ex * k + 1 * k, hy + 3 * k, 1.6 * k), (255, 255, 255))
    return (hx, hy)


def mage(S, g, x, base, h, robe=(110, 70, 170), hat=(80, 50, 140), skin=SKIN, face=1, seed=0, orb=(120, 220, 255), staff=True):
    k = h / 200.0
    f = face
    sh_shadow(S, g, x, base, 34 * k, 6 * k)
    if staff:
        S.obj(g, Seg(x + f * 32 * k, base - 4 * k, x + f * 38 * k, base - 170 * k, 4 * k), (130, 90, 50), seed, "wood")
        S.glow(g, x + f * 38 * k, base - 180 * k, 30 * k, orb, 0.4)
        S.obj(g, Circ(x + f * 38 * k, base - 180 * k, 11 * k), orb, seed + 1, hi=True)
    S.obj(g, Poly([(x - 34 * k, base - 2 * k), (x + 34 * k, base - 2 * k), (x + 18 * k, base - 110 * k), (x - 18 * k, base - 110 * k)]), robe, seed + 2, "fabric")
    S.obj(g, Seg(x + f * 18 * k, base - 104 * k, x + f * 32 * k, base - 80 * k, 7 * k), robe, seed + 3)
    hx, hy = x + f * 2 * k, base - 140 * k
    S.obj(g, Ell(hx, hy, 30 * k, 32 * k), skin, seed + 4)
    S.obj(g, Union([Ell(hx, hy - 20 * k, 50 * k, 10 * k), Poly([(hx - 28 * k, hy - 22 * k), (hx - f * 20 * k, hy - 96 * k), (hx + 28 * k, hy - 22 * k)])]), hat, seed + 5)
    S.flat(g, Box(hx - 27 * k, hy - 30 * k, hx + 27 * k, hy - 22 * k), (250, 210, 80))
    for ex in (6, 20):
        S.flat(g, Ell(hx + f * ex * k, hy + 4 * k, 3.6 * k, 6 * k), (40, 40, 70))


def slime(S, g, x, base, r, col=(90, 170, 250), seed=0, face=1, crown=False):
    sh_shadow(S, g, x, base, r * 1.1, r * 0.2)
    body = Union([Ell(x, base - r * 0.6, r * 1.05, r * 0.62), Poly([(x - r * 0.7, base - r * 0.9), (x + face * r * 0.1, base - r * 1.9), (x + r * 0.7, base - r * 0.9)])])
    S.obj(g, body, col, seed, hi=True)
    for ex in (-0.32, 0.22):
        S.flat(g, Ell(x + (ex + face * 0.1) * r, base - r * 0.72, r * 0.1, r * 0.17), (30, 30, 50))
    S.flat(g, Ell(x + face * 0.05 * r, base - r * 0.42, r * 0.2, r * 0.08), (30, 30, 50))
    if crown:
        S.obj(g, Poly([(x - r * 0.35, base - r * 1.55), (x - r * 0.35, base - r * 1.85), (x - r * 0.15, base - r * 1.7), (x, base - r * 1.95),
                       (x + r * 0.15, base - r * 1.7), (x + r * 0.35, base - r * 1.85), (x + r * 0.35, base - r * 1.55)]), (250, 210, 60), seed + 1, hi=True)


def goblin(S, g, x, base, h, skin=(120, 170, 80), cloth=(120, 90, 60), face=1, seed=0, weapon=True):
    k = h / 200.0
    f = face
    sh_shadow(S, g, x, base, 34 * k, 6 * k)
    for dx in (-12, 12):
        S.obj(g, Box(x + (dx - 7) * k, base - 60 * k, x + (dx + 7) * k, base - 4 * k, 3 * k), skin, seed)
    S.obj(g, Poly([(x - 30 * k, base - 50 * k), (x + 30 * k, base - 50 * k), (x + 24 * k, base - 120 * k), (x - 24 * k, base - 120 * k)]), cloth, seed + 1, "fabric")
    if weapon:
        S.obj(g, Poly([(x + f * 30 * k, base - 80 * k), (x + f * 36 * k, base - 86 * k), (x + f * 70 * k, base - 150 * k), (x + f * 62 * k, base - 152 * k)]), (200, 205, 210), seed + 2)
    S.obj(g, Seg(x + f * 24 * k, base - 110 * k, x + f * 36 * k, base - 80 * k, 8 * k), skin, seed + 3)
    hx, hy = x + f * 6 * k, base - 152 * k
    S.obj(g, Union([Ell(hx, hy, 32 * k, 30 * k), Poly([(hx - 26 * k, hy - 8 * k), (hx - 66 * k, hy - 26 * k), (hx - 28 * k, hy + 8 * k)]),
                    Poly([(hx + 26 * k, hy - 8 * k), (hx + 66 * k, hy - 26 * k), (hx + 28 * k, hy + 8 * k)])]), skin, seed + 4, hi=True)
    S.obj(g, Ell(hx + f * 18 * k, hy + 6 * k, 9 * k, 7 * k), mixc(skin, (0, 0, 0), 0.15), seed + 5)
    for ex in (-6, 12):
        S.flat(g, Ell(hx + f * ex * k, hy - 6 * k, 5 * k, 4 * k), (250, 220, 60))
        S.flat(g, Circ(hx + f * ex * k, hy - 6 * k, 1.6 * k), (20, 20, 20))


def dragon(S, g, x, y, s, col=(190, 50, 50), belly=(240, 190, 110), face=-1, seed=0, wings_up=True, fire=False):
    """Original dragon (side view): horned head, wings, curling tail. (x, y) body centre."""
    f = face
    sx = lambda v: x + f * v * s
    sy = lambda v: y - v * s
    wing = Poly([(sx(-10), sy(20)), (sx(-30), sy(110)), (sx(-90), sy(150)), (sx(-70), sy(110)), (sx(-130), sy(120)), (sx(-100), sy(80)),
                 (sx(-150), sy(70)), (sx(-90), sy(40)), (sx(-40), sy(10))]) if wings_up else \
        Poly([(sx(-10), sy(20)), (sx(-60), sy(60)), (sx(-150), sy(40)), (sx(-120), sy(20)), (sx(-160), sy(0)), (sx(-110), sy(-6)), (sx(-40), sy(4))])
    S.obj(g, wing, mixc(col, (0, 0, 0), 0.25), seed, hi=False)
    tail = Union([Seg(sx(-50), sy(-4), sx(-120), sy(-20), 14 * s, 8 * s), Seg(sx(-120), sy(-20), sx(-170), sy(10), 8 * s, 3 * s),
                  Poly([(sx(-170), sy(10)), (sx(-190), sy(24)), (sx(-178), sy(-2))])])
    S.obj(g, tail, col, seed + 1)
    for lx in (20, -30):
        S.obj(g, Seg(sx(lx), sy(-18), sx(lx + 6), sy(-58), 10 * s, 7 * s), col, seed + 2)
    S.obj(g, Ell(sx(0), sy(0), 60 * s, 32 * s), col, seed + 3, hi=True)
    S.obj(g, Ell(sx(10), sy(-12), 44 * s, 16 * s), belly, seed + 4, line=False)
    S.obj(g, Seg(sx(40), sy(10), sx(92), sy(62), 17 * s, 11 * s), col, seed + 5)
    head = Union([Ell(sx(110), sy(72), 26 * s, 17 * s), Poly([(sx(124), sy(80), ), (sx(160), sy(66)), (sx(158), sy(56)), (sx(124), sy(58))])])
    S.obj(g, head, col, seed + 6, hi=True)
    for hx in (96, 108):
        S.obj(g, Poly([(sx(hx), sy(84)), (sx(hx - 22), sy(116)), (sx(hx + 8), sy(88))]), (240, 230, 200), seed + 7)
    S.flat(g, Ell(sx(122), sy(76), 4 * s, 3 * s), (255, 230, 60))
    S.flat(g, Circ(sx(123), sy(76), 1.6 * s), (20, 10, 10))
    if fire:
        S.glow(g, sx(200), sy(56), 80 * s, (255, 160, 60), 0.5)
        S.obj(g, Poly([(sx(158), sy(62)), (sx(230), sy(86)), (sx(260), sy(56)), (sx(230), sy(30))]), (255, 170, 60), seed + 8, line=False)
        S.flat(g, Poly([(sx(162), sy(60)), (sx(214), sy(72)), (sx(230), sy(56)), (sx(214), sy(44))]), (255, 240, 170))
    return head


def car(S, g, x, base, L, col, seed=0, face=1, kind="sedan", lights=False, police=False, glass=(120, 160, 190)):
    """Side-view modern car (sedan / sport / van / pickup), no badges."""
    f = face
    h = L * 0.3
    sh_shadow(S, g, x, base, L * 0.55, 6)

    def P(pts):        # authored facing right; mirrored about x when facing left
        return Poly([(x + f * (px - x), py) for px, py in pts])
    if kind == "sport":
        body = P([(x - L / 2, base - h * 0.35), (x - L / 2 + 6, base - h * 0.85), (x - L * 0.12, base - h * 0.95), (x + L * 0.08, base - h * 1.35),
                  (x + L * 0.3, base - h * 1.3), (x + L / 2, base - h * 0.75), (x + L / 2, base - h * 0.3)])
        win = P([(x - L * 0.06, base - h * 0.98), (x + L * 0.1, base - h * 1.28), (x + L * 0.28, base - h * 1.24), (x + L * 0.34, base - h * 0.98)])
    elif kind == "van":
        body = P([(x - L / 2, base - h * 0.3), (x - L / 2, base - h * 1.75), (x + L * 0.25, base - h * 1.75), (x + L / 2, base - h * 1.0), (x + L / 2, base - h * 0.3)])
        win = P([(x + L * 0.08, base - h * 1.6), (x + L * 0.24, base - h * 1.6), (x + L * 0.42, base - h * 1.08), (x + L * 0.08, base - h * 1.08)])
    elif kind == "pickup":
        body = Union([Box(x - L / 2, base - h * 1.0, x + L / 2, base - h * 0.3, 4),
                      P([(x + L * 0.02, base - h), (x + L * 0.06, base - h * 1.7), (x + L * 0.3, base - h * 1.7), (x + L * 0.38, base - h)])])
        win = P([(x + L * 0.08, base - h * 1.6), (x + L * 0.28, base - h * 1.6), (x + L * 0.33, base - h * 1.08), (x + L * 0.08, base - h * 1.08)])
    else:
        body = P([(x - L / 2, base - h * 0.3), (x - L / 2 + 4, base - h * 0.95), (x - L * 0.22, base - h), (x - L * 0.1, base - h * 1.6),
                  (x + L * 0.2, base - h * 1.6), (x + L * 0.32, base - h * 1.0), (x + L / 2, base - h * 0.9), (x + L / 2, base - h * 0.3)])
        win = P([(x - L * 0.08, base - h * 1.5), (x + L * 0.18, base - h * 1.5), (x + L * 0.28, base - h * 1.04), (x - L * 0.17, base - h * 1.04)])
    S.obj(g, body, col, seed, hi=True)
    S.obj(g, win, glass, seed + 1, hi=True)
    if police:
        S.flat(g, Box(x - L / 2 + 2, base - h * 0.75, x + L / 2 - 2, base - h * 0.55), (250, 250, 250))
        S.obj(g, Box(x - L * 0.08, base - h * 1.75, x + L * 0.08, base - h * 1.6, 2), (230, 40, 40), seed + 5)
        S.flat(g, Box(x, base - h * 1.75, x + L * 0.08, base - h * 1.6), (40, 90, 240))
    if lights:
        S.glow(g, x + f * L / 2, base - h * 0.6, 50, (255, 240, 200), 0.4)
    S.obj(g, Box(x + f * L / 2 - f * 10 - 5, base - h * 0.72, x + f * L / 2 - f * 10 + 5, base - h * 0.55, 2), (255, 240, 200), seed + 2, line=False)
    for wx in (x - L * 0.3, x + L * 0.3):
        S.obj(g, Circ(wx, base - h * 0.28, h * 0.34), (36, 36, 40), seed + 3)
        S.obj(g, Circ(wx, base - h * 0.28, h * 0.17), (180, 184, 190), seed + 4, hi=True)


# =================================================================== small animated helpers
def sparkle_el(eid, pts, col=(255, 255, 255), r=5, speed=0.7, phase=0.0):
    def draw(g, m):
        for x, y in pts:
            g.glow(x, y, r, col, 1.0, power=1.3)
            g.fill(Seg(x - r * 1.4, y, x + r * 1.4, y, 0.9), col)
            g.fill(Seg(x, y - r * 1.4, x, y + r * 1.4, 0.9), col)
    return E(eid, el(draw), daynight="untinted", anim=dict(twinkle=0.85, twinkleSpeed=speed, phase=phase))


def bob_el(eid, S, fn, pivot, amp=(0, 4), speed=0.5, **kw):
    """Wrap a style-drawn prop fn(S, g) as a bobbing element."""
    return E(eid, el(lambda g, m: fn(S, g)), pivot=pivot, anim=dict(bobAmplitude=amp, bobSpeed=speed), **kw)
