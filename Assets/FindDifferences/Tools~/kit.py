# -*- coding: utf-8 -*-
"""
Prop library + post filters for the theme levels (Level29+), paper-craft style.

Everything draws in scene coordinates on an fdcore.Canvas. Props take a base (ground) y so they can stand
on hill_strip layers. Helpers that return E elements are suffixed with _el.
Post filters: paper (default grain), oil painting, pencil sketch, tilt-shift miniature.
"""
import math
import random

from fdcore import E, H, W, lit
from paper import (Circ, Ell, Poly, RRect, Thick, flat, grain, hill_strip, hill_y, paper_post, piece, soft_union,
                   star_pts)

INK = (60, 50, 62)
PROP = (2, 4, 7, 0.42)
SMALL = (1, 2, 3, 0.3)
LAYER = (1, 3, 11, 0.36)


# ------------------------------------------------------------------- landscape
def sky(c, top, bottom, y1=H + 60):
    c.gradient(0, y1, top, bottom)


def layer(c, top, waves, col, shadow=LAYER):
    piece(c, hill_strip(top, waves), col, shadow=shadow)


def gy(top, waves, x):
    return hill_y(top, waves, x)


def cloud_bg(c, x, y, k, col=(252, 252, 248), shadow=PROP):
    piece(c, [Circ(x - 26 * k, y + 9 * k, 20 * k), Circ(x, y, 26 * k), Circ(x + 28 * k, y + 10 * k, 20 * k),
              RRect(x - 56 * k, y + 8 * k, x + 56 * k, y + 26 * k, 9 * k)], col, shadow=shadow)


def sun_bg(c, x, y, r, col=(255, 222, 95), glow=(255, 240, 190)):
    soft_union(c, [Circ(x, y, r)], glow, 0.5, spread=r * 1.3)
    piece(c, Circ(x, y, r), col, shadow=None)


def moon_bg(c, x, y, r, col=(250, 244, 220)):
    soft_union(c, [Circ(x, y, r)], (255, 250, 220), 0.35, spread=r)
    piece(c, Circ(x, y, r), col, shadow=None)
    flat(c, [Circ(x - r * 0.3, y - r * 0.2, r * 0.2), Circ(x + r * 0.3, y + r * 0.3, r * 0.14)], lit(col, 0.9))


def stars_bg(c, seed, n, y_max, col=(255, 250, 220)):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, y_max), rnd.choice((1.0, 1.4, 2.0))
        flat(c, Circ(x, y, r), col)


# ------------------------------------------------------------------- vegetation & rocks
def tree_round(c, x, base, s=1.0, col=(86, 160, 90), trunk=(130, 88, 64)):
    piece(c, [Thick(x, base, x, base - 34 * s, 7 * s), Circ(x, base - 56 * s, 26 * s), Circ(x - 18 * s, base - 42 * s, 18 * s),
              Circ(x + 18 * s, base - 42 * s, 18 * s)], col, shadow=PROP)
    flat(c, Thick(x, base, x, base - 28 * s, 7 * s), trunk)
    flat(c, Circ(x - 8 * s, base - 62 * s, 10 * s), lit(col, 1.15))


def tree_pine(c, x, base, h=80, col=(60, 120, 80), trunk=(120, 80, 60), snow=None):
    tiers = [Poly([(x, base - h + k * h * 0.24), (x - h * (0.2 + k * 0.08), base - h * (0.5 - k * 0.2)),
                   (x + h * (0.2 + k * 0.08), base - h * (0.5 - k * 0.2))]) for k in range(3)]
    flat(c, RRect(x - 3, base - h * 0.15, x + 3, base, 1), trunk)
    piece(c, tiers, col, shadow=PROP)
    if snow:
        for k in range(3):
            top = base - h + k * h * 0.24
            w = h * (0.2 + k * 0.08) * 0.5
            flat(c, Poly([(x, top), (x - w, top + h * 0.12), (x, top + h * 0.08), (x + w, top + h * 0.12)]), snow)


def palm(c, x, base, h=150, lean=20, col=(70, 160, 85), trunk=(150, 110, 70)):
    tx, ty = x + lean, base - h
    segs = [Thick(x + lean * (k / 8) ** 2, base - h * k / 8, x + lean * ((k + 1) / 8) ** 2, base - h * (k + 1) / 8, 9 - k * 0.6)
            for k in range(8)]
    piece(c, segs, trunk, shadow=PROP)
    leaves = []
    for a, ln in ((200, 70), (235, 64), (290, 58), (330, 68), (10, 64), (160, 60)):
        r = math.radians(a)
        ex, ey = tx + ln * math.cos(r), ty + ln * math.sin(r) * 0.7 + 16
        mx, my = (tx + ex) / 2, (ty + ey) / 2 - 12
        leaves.append(Poly([(tx, ty), (mx, my - 7), (ex, ey), (mx, my + 8)]))
    piece(c, leaves, col, shadow=PROP)


def dead_tree(c, x, base, s=1.0, col=(70, 58, 62)):
    br = [Thick(x, base, x, base - 80 * s, 7 * s), Thick(x, base - 50 * s, x - 34 * s, base - 84 * s, 4 * s),
          Thick(x, base - 62 * s, x + 30 * s, base - 100 * s, 4 * s), Thick(x - 20 * s, base - 70 * s, x - 30 * s, base - 106 * s, 3 * s),
          Thick(x + 16 * s, base - 82 * s, x + 40 * s, base - 88 * s, 3 * s)]
    piece(c, br, col, shadow=PROP)


def bush(c, x, base, s=1.0, col=(80, 150, 85)):
    piece(c, [Circ(x - 14 * s, base - 10 * s, 13 * s), Circ(x, base - 16 * s, 16 * s), Circ(x + 15 * s, base - 10 * s, 12 * s)],
          col, shadow=PROP)


def mushroom(c, x, base, s=1.0, cap=(220, 70, 70), stem=(245, 236, 215), spots=True):
    piece(c, RRect(x - 6 * s, base - 30 * s, x + 6 * s, base, 3 * s), stem, shadow=PROP)
    pts = [(x + 26 * s * math.cos(math.radians(a)), base - 28 * s - 22 * s * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    piece(c, Poly(pts), cap, shadow=PROP)
    if spots:
        flat(c, [Circ(x - 10 * s, base - 38 * s, 4 * s), Circ(x + 6 * s, base - 44 * s, 4.5 * s), Circ(x + 15 * s, base - 33 * s, 3 * s)],
             (255, 248, 236))


def cactus(c, x, base, s=1.0, col=(90, 160, 90)):
    piece(c, [RRect(x - 9 * s, base - 70 * s, x + 9 * s, base, 9 * s), RRect(x - 30 * s, base - 46 * s, x - 20 * s, base - 22 * s, 5 * s),
              Thick(x - 25 * s, base - 26 * s, x - 6 * s, base - 26 * s, 9 * s), RRect(x + 20 * s, base - 56 * s, x + 30 * s, base - 30 * s, 5 * s),
              Thick(x + 25 * s, base - 34 * s, x + 6 * s, base - 34 * s, 9 * s)], col, shadow=PROP)
    flat(c, Thick(x - 2 * s, base - 64 * s, x - 2 * s, base - 6 * s, 1.4), lit(col, 0.8))


def rock(c, x, base, s=1.0, col=(150, 145, 150)):
    piece(c, Poly([(x - 30 * s, base), (x - 24 * s, base - 18 * s), (x - 6 * s, base - 28 * s), (x + 18 * s, base - 22 * s),
                   (x + 30 * s, base)]), col, shadow=PROP)
    flat(c, Poly([(x - 6 * s, base - 28 * s), (x + 18 * s, base - 22 * s), (x + 30 * s, base), (x + 6 * s, base)]), lit(col, 0.82))


def crystal(c, x, base, s=1.0, col=(150, 120, 255)):
    for dx, h, w in ((-10, 40, 9), (4, 58, 11), (16, 34, 8)):
        pts = [(x + dx * s - w * s, base), (x + dx * s - w * s, base - h * s * 0.7), (x + dx * s, base - h * s),
               (x + dx * s + w * s, base - h * s * 0.7), (x + dx * s + w * s, base)]
        piece(c, Poly(pts), col, shadow=PROP)
        flat(c, Poly([(x + dx * s, base - h * s), (x + dx * s + w * s, base - h * s * 0.7), (x + dx * s + w * s, base), (x + dx * s, base)]),
             lit(col, 0.75))


def grass_tufts(c, x0, x1, base_fn, col, step=34, seed=1):
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        y = base_fn(x) + rnd.uniform(4, 30)
        flat(c, Poly([(x - 6, y), (x - 3, y - 10), (x, y - 2), (x + 3, y - 12), (x + 6, y)]), col)
        x += step + rnd.uniform(-8, 8)


# ------------------------------------------------------------------- buildings
def house(c, x, base, w, h, wall, roof_col, roof="gable", door=(120, 80, 60), win=(255, 222, 140), wins=2, roof_h=None):
    """Returns dict with handy points: door, windows (rects), chimney (x, y)."""
    x0, x1 = x - w / 2, x + w / 2
    top = base - h
    piece(c, RRect(x0, top, x1, base, 2), wall, border=2, shadow=PROP)
    rh = roof_h or w * 0.42
    if roof == "gable":
        piece(c, Poly([(x0 - 8, top + 2), (x1 + 8, top + 2), (x, top - rh)]), roof_col, border=2, shadow=PROP)
    elif roof == "flat":
        piece(c, RRect(x0 - 6, top - 10, x1 + 6, top + 2, 2), roof_col, border=2, shadow=PROP)
    elif roof == "dome":
        pts = [(x + (w / 2 + 4) * math.cos(math.radians(a)), top + 2 - rh * math.sin(math.radians(a))) for a in range(0, 181, 12)]
        piece(c, Poly(pts), roof_col, border=2, shadow=PROP)
    elif roof == "spire":
        piece(c, Poly([(x0 - 4, top + 2), (x1 + 4, top + 2), (x, top - rh * 1.8)]), roof_col, border=2, shadow=PROP)
    rects = []
    for i in range(wins):
        wx = x0 + w * (i + 1) / (wins + 1)
        r = (wx - 9, top + h * 0.2, wx + 9, top + h * 0.2 + 18)
        rects.append(r)
        flat(c, RRect(*r, 2), win)
        flat(c, [Thick(wx, r[1], wx, r[3], 1.4), Thick(r[0], (r[1] + r[3]) / 2, r[2], (r[1] + r[3]) / 2, 1.4)], lit(wall, 0.75))
    dr = (x - 9, base - 26, x + 9, base)
    if door:
        flat(c, RRect(*dr, 3), door)
    return dict(door=dr, windows=rects, chimney=(x1 - w * 0.22, top - rh * 0.45))


def chimney(c, x, y, h=26, col=(160, 95, 80)):
    piece(c, RRect(x - 7, y - h, x + 7, y + 6, 1.5), col, border=1.5, shadow=PROP)
    return (x, y - h - 4)


def tower(c, x, base, w, h, wall, roof_col, roof_h=None, wins=3):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), wall, border=2, shadow=PROP)
    rh = roof_h or w * 1.1
    piece(c, Poly([(x - w / 2 - 8, base - h + 2), (x + w / 2 + 8, base - h + 2), (x, base - h - rh)]), roof_col, border=2, shadow=PROP)
    out = []
    for k in range(wins):
        y = base - h + 20 + k * (h - 40) / max(1, wins)
        r = (x - 6, y, x + 6, y + 16)
        flat(c, [RRect(*r, 0), Circ(x, y, 6)], (60, 52, 72))
        out.append(r)
    return out


def fence(c, x0, x1, base_fn, col=(240, 232, 214), step=28, h=30):
    x = x0
    while x <= x1:
        b = base_fn(x)
        piece(c, Poly([(x - 4, b + 6), (x - 4, b - h), (x, b - h - 5), (x + 4, b - h), (x + 4, b + 6)]), col, shadow=SMALL)
        x += step
    pts = [(xx, base_fn(xx) - h * 0.6) for xx in range(int(x0), int(x1) + 1, step)]
    if len(pts) > 1:
        flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 2.5) for i in range(len(pts) - 1)], lit(col, 0.9))


def lamp_post(c, x, base, h=70, col=(70, 70, 85), light=(255, 230, 150)):
    piece(c, [Thick(x, base, x, base - h, 3), Thick(x, base - h, x + 12, base - h, 3)], col, shadow=PROP)
    piece(c, Poly([(x + 6, base - h), (x + 18, base - h), (x + 15, base - h + 10), (x + 9, base - h + 10)]), light, border=1, shadow=None)
    return (x + 12, base - h + 6)


def barrel(c, x, base, s=1.0, col=(160, 110, 70)):
    piece(c, RRect(x - 12 * s, base - 30 * s, x + 12 * s, base, 6 * s), col, border=1.5, shadow=PROP)
    flat(c, [Thick(x - 12 * s, base - 22 * s, x + 12 * s, base - 22 * s, 2), Thick(x - 12 * s, base - 8 * s, x + 12 * s, base - 8 * s, 2)],
         lit(col, 0.7))


def crate(c, x, base, s=1.0, col=(190, 150, 100)):
    piece(c, RRect(x - 16 * s, base - 30 * s, x + 16 * s, base, 2), col, border=1.5, shadow=PROP)
    flat(c, [Thick(x - 16 * s, base - 30 * s, x + 16 * s, base, 2.4), Thick(x + 16 * s, base - 30 * s, x - 16 * s, base, 2.4)], lit(col, 0.8))


def sign(c, x, base, col=(180, 130, 80), text_col=(90, 60, 50)):
    piece(c, [Thick(x, base, x, base - 40, 3), RRect(x - 22, base - 56, x + 22, base - 36, 3)], col, border=1.5, shadow=PROP)
    flat(c, [Thick(x - 14, base - 46, x + 14, base - 46, 2)], text_col)


# ------------------------------------------------------------------- characters
def person(c, x, base, body, head=(250, 214, 185), h=1.0, hat=None):
    hx, hy = x + 1 * h, base - 40 * h
    piece(c, [Poly([(x - 9 * h, base), (x + 9 * h, base), (x + 6 * h, base - 30 * h), (x - 6 * h, base - 30 * h)]), Circ(hx, hy, 7.5 * h)],
          body, border=1.5, shadow=PROP)
    flat(c, Circ(hx, hy, 6.2 * h), head)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    if hat:
        flat(c, Poly([(hx - 9 * h, hy - 4 * h), (hx + 9 * h, hy - 4 * h), (hx, hy - 16 * h)]), hat)
    return hx, hy


ANIMALS = {
    "cat": ((240, 170, 90), "pointy"), "fox": ((240, 130, 60), "pointy"), "rabbit": ((245, 242, 236), "long"),
    "bear": ((150, 100, 70), "round"), "pig": ((250, 180, 190), "flop"), "dog": ((200, 160, 110), "flop"),
    "frog": ((110, 190, 100), "eyes"), "owl": ((150, 120, 90), "tufts"), "mouse": ((190, 190, 200), "big"),
}


def animal(c, kind, x, base, clothes, h=1.0, face_right=True):
    """Stand-up animal character wearing clothes; returns head centre."""
    fur, ears = ANIMALS[kind]
    s = 1 if face_right else -1
    hx, hy = x + 2 * h * s, base - 44 * h
    body = [Poly([(x - 10 * h, base), (x + 10 * h, base), (x + 7 * h, base - 32 * h), (x - 7 * h, base - 32 * h)])]
    piece(c, body, clothes, border=1.5, shadow=PROP)
    head = [Circ(hx, hy, 10 * h)]
    if ears == "pointy":
        head += [Poly([(hx - 9 * h, hy - 4 * h), (hx - 6 * h, hy - 18 * h), (hx - 1 * h, hy - 8 * h)]),
                 Poly([(hx + 9 * h, hy - 4 * h), (hx + 6 * h, hy - 18 * h), (hx + 1 * h, hy - 8 * h)])]
    elif ears == "long":
        head += [Ell(hx - 4 * h, hy - 18 * h, 3 * h, 10 * h), Ell(hx + 4 * h, hy - 18 * h, 3 * h, 10 * h)]
    elif ears == "round":
        head += [Circ(hx - 8 * h, hy - 8 * h, 4.5 * h), Circ(hx + 8 * h, hy - 8 * h, 4.5 * h)]
    elif ears == "flop":
        head += [Ell(hx - 10 * h, hy - 2 * h, 4 * h, 7 * h), Ell(hx + 10 * h, hy - 2 * h, 4 * h, 7 * h)]
    elif ears == "eyes":
        head += [Circ(hx - 5 * h, hy - 9 * h, 4.5 * h), Circ(hx + 5 * h, hy - 9 * h, 4.5 * h)]
    elif ears == "tufts":
        head += [Poly([(hx - 9 * h, hy - 5 * h), (hx - 10 * h, hy - 15 * h), (hx - 4 * h, hy - 8 * h)]),
                 Poly([(hx + 9 * h, hy - 5 * h), (hx + 10 * h, hy - 15 * h), (hx + 4 * h, hy - 8 * h)])]
    elif ears == "big":
        head += [Circ(hx - 9 * h, hy - 8 * h, 6 * h), Circ(hx + 9 * h, hy - 8 * h, 6 * h)]
    piece(c, head, fur, border=1.5, shadow=PROP)
    if kind == "pig":
        flat(c, Ell(hx + 6 * h * s, hy + 2 * h, 4 * h, 3 * h), lit(fur, 0.85))
    if kind in ("dog", "bear", "fox", "cat", "mouse", "rabbit"):
        flat(c, Ell(hx + 5 * h * s, hy + 3 * h, 4 * h, 3 * h), lit(fur, 1.15))
        flat(c, Circ(hx + 8 * h * s, hy + 2 * h, 1.6 * h), INK)
    eye = (hx + 3 * h * s, hy - 3 * h)
    if kind == "frog":
        flat(c, [Circ(hx - 5 * h, hy - 9 * h, 2 * h), Circ(hx + 5 * h, hy - 9 * h, 2 * h)], INK)
    elif kind == "owl":
        flat(c, [Circ(hx - 4 * h, hy - 1 * h, 3.4 * h), Circ(hx + 4 * h, hy - 1 * h, 3.4 * h)], (255, 220, 90))
        flat(c, [Circ(hx - 4 * h, hy - 1 * h, 1.5 * h), Circ(hx + 4 * h, hy - 1 * h, 1.5 * h)], INK)
    else:
        flat(c, Circ(*eye, 1.4 * h), INK)
    return hx, hy


# ------------------------------------------------------------------- machines
def gear_shapes(x, y, r, teeth=10, tooth=None, hole=True):
    tooth = tooth or r * 0.22
    shapes = [Circ(x, y, r)]
    for k in range(teeth):
        a = 2 * math.pi * k / teeth
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        w = r * 0.18
        shapes.append(Poly([(x + ux * r * 0.9 + vx * w, y + uy * r * 0.9 + vy * w), (x + ux * (r + tooth) + vx * w * 0.7, y + uy * (r + tooth) + vy * w * 0.7),
                            (x + ux * (r + tooth) - vx * w * 0.7, y + uy * (r + tooth) - vy * w * 0.7), (x + ux * r * 0.9 - vx * w, y + uy * r * 0.9 - vy * w)]))
    return shapes


def gear(c, x, y, r, col=(190, 150, 80), teeth=10):
    piece(c, gear_shapes(x, y, r, teeth), col, border=1.2, border_col=lit(col, 1.3), shadow=PROP)
    flat(c, Circ(x, y, r * 0.55), lit(col, 0.8))
    flat(c, Circ(x, y, r * 0.2), lit(col, 0.5))
    for k in range(4):
        a = math.pi / 2 * k + 0.4
        flat(c, Circ(x + math.cos(a) * r * 0.38, y + math.sin(a) * r * 0.38, r * 0.1), lit(col, 0.55))


def pipe(c, pts, w=10, col=(150, 110, 70)):
    segs = [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], w) for i in range(len(pts) - 1)]
    piece(c, segs, col, border=1.2, shadow=PROP)
    flat(c, [Thick(pts[i][0], pts[i][1] - w * 0.2, pts[i + 1][0], pts[i + 1][1] - w * 0.2, w * 0.25) for i in range(len(pts) - 1)],
         lit(col, 1.3))
    for x, y in pts[1:-1]:
        flat(c, Circ(x, y, w * 0.7), lit(col, 0.85))


def fish(c, x, y, s, col, right=True, fin=None):
    d = 1 if right else -1
    piece(c, [Ell(x, y, 14 * s, 7 * s), Poly([(x - 11 * s * d, y), (x - 22 * s * d, y - 7 * s), (x - 22 * s * d, y + 7 * s)])], col,
          border=1.2, shadow=SMALL)
    flat(c, Circ(x + 8 * s * d, y - 2 * s, 1.6 * s), INK)
    if fin:
        flat(c, Poly([(x - 2 * s * d, y - 6 * s), (x + 4 * s * d, y - 12 * s), (x + 6 * s * d, y - 5 * s)]), fin)


def bubble(c, x, y, r, col=(220, 240, 255)):
    c.ellipse_ring(x, y, r, r, max(1.0, r * 0.25), col + (0.85,))
    flat(c, Circ(x - r * 0.35, y - r * 0.35, r * 0.25), (255, 255, 255, 0.8))


# ------------------------------------------------------------------- element helpers
def spin_el(eid, draw, pivot, speed, speed_b=None, **kw):
    a = dict(rotateSpeed=speed)
    b = None if speed_b is None else dict(rotateSpeed=speed_b)
    return E(eid, draw, pivot=pivot, anim=a, animB=b, **kw)


def smoke_el(prefix, x, y, n=3, col=(238, 234, 230), r=8, show="both", rise=(5, 22), length=64, **kw):
    return [E("%s%d" % (prefix, i), (lambda: lambda c, m: piece(c, Circ(x, y, r), col, shadow=SMALL))(), show=show,
              anim=dict(driftVelocity=rise, driftLength=length, driftFade=True, driftGrow=1.3, phase=i / n), **kw) for i in range(n)]


def bubbles_el(prefix, x, y, n=4, r=4, rise=(2, 26), length=120, show="both", col=(220, 240, 255)):
    return [E("%s%d" % (prefix, i), (lambda: lambda c, m: bubble(c, x, y, r, col))(), show=show, daynight="untinted",
              anim=dict(driftVelocity=rise, driftLength=length, driftFade=True, driftGrow=0.6, bobAmplitude=(4, 0), bobSpeed=0.6,
                        phase=i / n)) for i in range(n)]


def drift_across(x_left, x_right, speed, start=0.0):
    if speed >= 0:
        s_min = -(x_right + 10)
        length = W + 10 - x_left - s_min
    else:
        s_min = -(W + 10 - x_left)
        length = x_right + 10 - s_min
    return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min, phase=((start - s_min) / length) % 1.0)


def bird_el(eid, x, y, s=9, col=(80, 85, 100), speed=20, **kw):
    def d(c, m):
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.25), Thick(x, y, x + s, y - s * 0.4, s * 0.25)], col, shadow=(1, 3, 4, 0.25))
    return E(eid, d, pivot=(x, y), anim=dict(drift_across(x - s, x + s, speed), stretch=(0, 0.5), scaleSpeed=2.4, bobAmplitude=(0, 6),
                                             bobSpeed=0.2), **kw)


def cloud_el(eid, x, y, k, speed, col=(252, 252, 248), **kw):
    return E(eid, lambda c, m: cloud_bg(c, x, y, k, col), anim=drift_across(x - 60 * k, x + 60 * k, speed), **kw)


def glow_el(eid, x, y, r, col, alpha=0.55, spread=None, **kw):
    def d(c, m):
        soft_union(c, [Circ(x, y, r)], col, alpha, spread=spread or r * 1.6)
    return E(eid, d, pivot=(x, y), **kw)


# ------------------------------------------------------------------- post filters
def oil_post(rows, w, h, ox, oy, has_alpha):
    """Oil painting: smear along a swirling stroke field, posterise lightly, canvas weave."""
    ch = 4 if has_alpha else 3
    src = [bytes(r) for r in rows]
    for j in range(h):
        sy = j + oy
        row = rows[j]
        for i in range(w):
            k = i * ch
            if has_alpha and src[j][k + 3] == 0:
                continue
            sx = i + ox
            a = math.sin(sx * 0.021 + math.sin(sy * 0.017) * 2.0) * 1.6 + math.cos(sy * 0.013) * 0.8
            dx, dy = math.cos(a), math.sin(a)
            acc = [0, 0, 0]
            n = 0
            for t in (-4, -2, 0, 2, 4):
                xx, yy = int(i + dx * t), int(j + dy * t)
                if 0 <= xx < w and 0 <= yy < h:
                    q = xx * ch
                    if has_alpha and src[yy][q + 3] == 0:
                        continue
                    acc[0] += src[yy][q]
                    acc[1] += src[yy][q + 1]
                    acc[2] += src[yy][q + 2]
                    n += 1
            if not n:
                continue
            weave = 1 + 0.035 * (((sx // 2) + (sy // 2)) % 2 - 0.5)
            for q in range(3):
                v = acc[q] / n
                v = round(v / 12) * 12            # gentle posterise -> visible paint patches
                v = int(v * weave)
                row[k + q] = 255 if v > 255 else (0 if v < 0 else v)
    grain(rows, w, h, ox, oy, has_alpha, strength=0.6, vignette=not has_alpha)


def sketch_post(rows, w, h, ox, oy, has_alpha):
    """Pencil sketch: grey paper, graphite outlines from colour edges, diagonal hatching for darker tones."""
    ch = 4 if has_alpha else 3
    lum = [[0.0] * w for _ in range(h)]
    for j in range(h):
        r = rows[j]
        lj = lum[j]
        for i in range(w):
            k = i * ch
            lj[i] = 0.3 * r[k] + 0.59 * r[k + 1] + 0.11 * r[k + 2]
    paper = (246, 242, 232)
    for j in range(h):
        sy = j + oy
        row = rows[j]
        for i in range(w):
            k = i * ch
            if has_alpha and row[k + 3] == 0:
                continue
            sx = i + ox
            L = lum[j][i]
            gx = lum[j][min(w - 1, i + 1)] - lum[j][max(0, i - 1)]
            gyv = lum[min(h - 1, j + 1)][i] - lum[max(0, j - 1)][i]
            edge = min(1.0, (abs(gx) + abs(gyv)) / 70.0)
            tone = 1.0
            if L < 200 and (sx + sy) % 7 == 0:
                tone -= 0.35
            if L < 140 and (sx - sy) % 6 == 0:
                tone -= 0.35
            if L < 80 and (sx + 2 * sy) % 5 == 0:
                tone -= 0.3
            tone *= 0.8 + 0.2 * (L / 255.0)
            v = tone * (1 - 0.85 * edge)
            for q in range(3):
                row[k + q] = int(paper[q] * v * (0.97 if q == 2 else 1.0))
    grain(rows, w, h, ox, oy, has_alpha, strength=0.5, vignette=not has_alpha)


def tiltshift_post(rows, w, h, ox, oy, has_alpha):
    """Miniature look: boost saturation and blur the top/bottom bands (background only)."""
    paper_post(rows, w, h, ox, oy, has_alpha)
    ch = 4 if has_alpha else 3
    for j in range(h):
        r = rows[j]
        for i in range(w):
            k = i * ch
            if has_alpha and r[k + 3] == 0:
                continue
            m = (r[k] + r[k + 1] + r[k + 2]) / 3
            for q in range(3):
                v = int(m + (r[k + q] - m) * 1.25)
                r[k + q] = 255 if v > 255 else (0 if v < 0 else v)
    if has_alpha:
        return
    src = [bytes(r) for r in rows]
    for j in range(h):
        sy = j + oy
        dist = max(0.0, abs(sy - H * 0.55) - H * 0.18) / (H * 0.3)
        rad = int(min(1.0, dist) * 6)
        if rad <= 0:
            continue
        row = rows[j]
        for i in range(w):
            acc = [0, 0, 0]
            n = 0
            for dy in (-rad, 0, rad):
                yy = min(h - 1, max(0, j + dy))
                for dx in (-rad, 0, rad):
                    xx = min(w - 1, max(0, i + dx))
                    q = xx * 3
                    acc[0] += src[yy][q]
                    acc[1] += src[yy][q + 1]
                    acc[2] += src[yy][q + 2]
                    n += 1
            row[i * 3:i * 3 + 3] = bytes(int(a / n) for a in acc)
