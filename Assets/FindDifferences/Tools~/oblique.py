# -*- coding: utf-8 -*-
"""
45-degree overhead ("3/4 top-down") projection for paper scenes, with a directional light that casts shadows.

World: X to the right, Y away from the viewer (up the screen), Z up. The camera looks north, tilted down 45 deg:
    screen x = X,  screen y = GY - (Y + Z) * K      (K = cos 45)
so every object shows its top and its south (front) face.

The sun shines from the upper left behind the scene; a point at height Z throws its shadow to
    (X + Z * SX, Y + Z * SY, 0)
Shadows of all objects are gathered first and painted onto the ground (soft, translucent), then the objects
are painted far to near as paper pieces (lit top, darker front, lit / shaded roof slopes).
"""
import math

from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union
from fdcore import lit

K = math.cos(math.radians(45))
GY = 640.0
SX, SY = 0.75, -0.55               # shadow offset per unit of height (to the right, towards the viewer)
SHADOW_COL = (40, 50, 50)
EDGE = 1.2


def p(X, Y, Z=0.0):
    return (X, GY - (Y + Z) * K)


def shadow_pt(X, Y, Z):
    return (X + Z * SX, Y + Z * SY)


def hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for q in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    return lower[:-1] + upper[:-1]


class Scene:
    """Collects shadow casters and drawables; paint() draws shadows first, then objects far -> near."""

    def __init__(self):
        self.shadows = []          # lists of 3D points (their ground shadows are hulled)
        self.items = []            # (sort key, fn)

    def cast(self, pts3):
        self.shadows.append(pts3)

    def add(self, y_sort, fn):
        self.items.append((y_sort, fn))

    def paint_shadows(self, c, alpha=0.32, spread=5.0):
        shapes = []
        for pts3 in self.shadows:
            ground = [shadow_pt(*q) for q in pts3]
            h = hull(ground)
            if len(h) >= 3:
                shapes.append(Poly([p(x, y) for x, y in h]))
        if shapes:
            soft_union(c, shapes, SHADOW_COL, alpha, spread=spread)

    def paint(self, c):
        self.paint_shadows(c)
        for _, fn in sorted(self.items, key=lambda it: -it[0]):
            fn(c)


# ------------------------------------------------------------------- ground
def ground_poly(c, pts_xy, col):
    flat(c, Poly([p(x, y) for x, y in pts_xy]), col)


def ground_ellipse(c, X, Y, rx, ry, col, n=36):
    flat(c, Poly([p(X + rx * math.cos(2 * math.pi * k / n), Y + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]), col)


# ------------------------------------------------------------------- solids (each registers its shadow and drawing)
def box(sc, X0, Y0, X1, Y1, h, col, z0=0.0, top=None, front=None, detail=None, sort_y=None):
    """Axis-aligned box from (X0, Y0) to (X1, Y1), Y0 = front face."""
    corners = [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)]
    sc.cast([(x, y, z0) for x, y in corners] + [(x, y, z0 + h) for x, y in corners])

    def d(c):
        piece(c, Poly([p(X0, Y0, z0), p(X1, Y0, z0), p(X1, Y0, z0 + h), p(X0, Y0, z0 + h)]), front or lit(col, 0.84), border=EDGE, shadow=None)
        piece(c, Poly([p(x, y, z0 + h) for x, y in corners]), top or lit(col, 1.08), border=EDGE, shadow=None)
        if detail:
            detail(c)
    sc.add(Y0 if sort_y is None else sort_y, d)


def cylinder(sc, X, Y, r, h, col, z0=0.0, top=None, detail=None, sort_y=None):
    sc.cast([(X + r * math.cos(a), Y + r * math.sin(a), z) for a in [k * math.pi / 8 for k in range(16)] for z in (z0, z0 + h)])

    def d(c):
        x, yb = p(X, Y, z0)
        _, yt = p(X, Y, z0 + h)
        piece(c, [RRect(x - r, yt, x + r, yb, 0), Ell(x, yb, r, r * K)], lit(col, 0.86), border=EDGE, shadow=None)
        flat(c, RRect(x - r * 0.8, yt, x - r * 0.45, yb, 0), lit(col, 1.0))
        piece(c, Ell(x, yt, r, r * K), top or lit(col, 1.08), border=EDGE, shadow=None)
        if detail:
            detail(c)
    sc.add(Y - r if sort_y is None else sort_y, d)


def ball(sc, X, Y, Z, r, col, sort_y=None):
    sc.cast([(X + r * math.cos(a), Y + r * math.sin(a), Z + dz) for a in [k * math.pi / 6 for k in range(12)] for dz in (-r * 0.6, 0, r * 0.6)])

    def d(c):
        x, y = p(X, Y, Z)
        piece(c, Circ(x, y, r), col, border=EDGE, shadow=None)
        flat(c, Circ(x + r * 0.25, y + r * 0.25, r * 0.78), lit(col, 0.86))
        flat(c, Circ(x - r * 0.12, y - r * 0.12, r * 0.72), col)
        flat(c, Circ(x - r * 0.35, y - r * 0.38, r * 0.25), lit(col, 1.18))
    sc.add(sort_y if sort_y is not None else Y - r, d)


def cone(sc, X, Y, r, h, col, z0=0.0, sort_y=None):
    sc.cast([(X + r * math.cos(a), Y + r * math.sin(a), z0) for a in [k * math.pi / 8 for k in range(16)]] + [(X, Y, z0 + h)])

    def d(c):
        x, yb = p(X, Y, z0)
        _, yt = p(X, Y, z0 + h)
        piece(c, [Poly([(x - r, yb), (x + r, yb), (x, yt)]), Ell(x, yb, r, r * K)], lit(col, 0.86), border=EDGE, shadow=None)
        flat(c, Poly([(x - r * 0.95, yb), (x - r * 0.1, yb + r * K * 0.6), (x, yt)]), lit(col, 1.08))
    sc.add(Y - r if sort_y is None else sort_y, d)


def tent(sc, X, Y, w, dpt, h, col, door=(60, 50, 50)):
    """A-frame tent, ridge running away from the viewer, entrance on the front."""
    X0, X1, Y0, Y1 = X - w / 2, X + w / 2, Y, Y + dpt
    sc.cast([(X0, Y0, 0), (X1, Y0, 0), (X1, Y1, 0), (X0, Y1, 0), (X, Y0, h), (X, Y1, h)])

    def d(c):
        piece(c, Poly([p(X0, Y0), p(X0, Y1), p(X, Y1, h), p(X, Y0, h)]), lit(col, 1.12), border=EDGE, shadow=None)
        piece(c, Poly([p(X1, Y0), p(X1, Y1), p(X, Y1, h), p(X, Y0, h)]), lit(col, 0.8), border=EDGE, shadow=None)
        piece(c, Poly([p(X0, Y0), p(X1, Y0), p(X, Y0, h)]), lit(col, 0.94), border=EDGE, shadow=None)
        flat(c, Poly([p(X - w * 0.18, Y0), p(X + w * 0.18, Y0), p(X, Y0, h * 0.7)]), door)
        flat(c, Thick(*p(X, Y0, h), *p(X, Y1, h), 2), lit(col, 0.6))
    sc.add(Y0, d)


def figure(sc, X, Y, body, head=(250, 222, 196), hair=(70, 50, 40), s=1.0):
    """Little paper person: cylinder body + ball head."""
    cylinder(sc, X, Y, 7 * s, 22 * s, body)
    ball(sc, X, Y, 30 * s, 7 * s, head, sort_y=Y - 7 * s - 0.01)

    def hair_d(c):
        x, y = p(X, Y, 30 * s)
        flat(c, Ell(x - 1 * s, y - 4 * s, 6.5 * s, 3.4 * s), hair)
    sc.add(Y - 7 * s - 0.02, hair_d)


def tree_round(sc, X, Y, s=1.0, col=(80, 150, 80)):
    cylinder(sc, X, Y, 6 * s, 40 * s, (130, 90, 60))
    ball(sc, X, Y, 66 * s, 30 * s, col, sort_y=Y - 6 * s - 0.01)


def tree_pine(sc, X, Y, s=1.0, col=(50, 120, 80)):
    cylinder(sc, X, Y, 5 * s, 16 * s, (120, 84, 60))
    cone(sc, X, Y, 26 * s, 50 * s, col, z0=14 * s, sort_y=Y - 5 * s - 0.01)
    cone(sc, X, Y, 19 * s, 40 * s, lit(col, 1.08), z0=40 * s, sort_y=Y - 5 * s - 0.02)
