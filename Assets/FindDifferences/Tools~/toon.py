# -*- coding: utf-8 -*-
"""Cel-shaded (toon-render) style on top of real.py's numpy painter.

Look: flat colour blocks, one hard-edged shadow tone (cool-shifted) on the side away from the light
(upper left), small hard highlight, dark ink outlines on near objects (thinner / none in the distance),
smooth gradient skies, stylised puffy clouds, dash-line water. No film grain.

    cel(g, shape, base)      ink outline + flat base + crescent shadow (shape minus itself shifted to the light)
    ink(g, shape, paint)     outline + fill
    Grow(shape, w)           shape dilated by w (outline / rim)
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from kit import drift_across
from real import (Box, C, Circ, Ctx, Diff, Ell, Moved, Poly, Rough, Seg, Shape, Under, Union, el, fbm, fbm1, mixc,
                  real_post, smooth, vgrad)

INK = (50, 40, 62)


class Grow(Shape):
    def __init__(self, s, w):
        self.s, self.w = s, w

    def bbox(self):
        b = self.s.bbox()
        return (b[0] - self.w, b[1] - self.w, b[2] + self.w, b[3] + self.w)

    def sdf(self, X, Y):
        return self.s.sdf(X, Y) - self.w


def shade_of(col, k=0.7):
    return mixc(tuple(v * k for v in col[:3]), (70, 60, 130), 0.22)


def tint_of(col, k=0.4):
    return mixc(col, (255, 252, 238), k)


def ink(g, shape, paint, w=2.0, col=INK):
    if w > 0:
        g.fill(Grow(shape, w), col)
    g.fill(shape, paint)


def cel(g, shape, base, w=2.0, shade=None, off=(-7, -8), hi=None, hi_off=(3, 4), col=INK):
    """Outline + base + hard shadow on the lower right + optional highlight rim on the upper left."""
    ink(g, shape, base, w, col)
    g.fill(Diff(shape, Moved(shape, off[0], off[1])), shade or shade_of(base))
    if hi:
        g.fill(Diff(shape, Moved(shape, hi_off[0], hi_off[1])), hi if isinstance(hi, tuple) else tint_of(base))


def face_x(base, split, shade=None):
    """Paint: base left of x=split, shade colour right of it (box / building side)."""
    b, s = C(base), C(shade or shade_of(base))

    def f(X, Y):
        return np.where((X < split)[..., None], b, s)
    return f


def toon_post(rows, w, h, ox, oy, has_alpha):
    real_post(rows, w, h, ox, oy, has_alpha, grain=1.2, vignette=0.12)


# ------------------------------------------------------------------- scenery
def cloud_shape(x, y, w, h, seed=0):
    rnd = random.Random(seed)
    parts = [Box(x - w, y - h * 0.35, x + w, y + h * 0.35, h * 0.35)]
    n = max(3, int(w / (h * 0.55)))
    for k in range(n):
        t = (k + 0.5) / n
        cx = x - w * 0.8 + w * 1.6 * t
        r = h * (0.45 + 0.55 * math.sin(t * math.pi)) * rnd.uniform(0.85, 1.15)
        parts.append(Circ(cx, y - h * 0.1 - r * 0.35, r))
    return Union(parts)


def toon_cloud(g, x, y, w, h, col=(255, 255, 255), shade=(196, 214, 244), line=(150, 172, 214), seed=0, lw=1.6):
    cel(g, cloud_shape(x, y, w, h, seed), col, w=lw, shade=shade, off=(-0.18 * h, -0.3 * h), col=line)


def hill(g, f, col, x0=-20, x1=W + 20, y1=H + 20, w=0.0, rim=8, shade_k=None, line=INK, tufts=0, seed=0):
    """Ground band below y = f(x): flat colour, lighter rim along the crest, optional grass tufts."""
    sh = Under(f, x0, x1, y1)
    ink(g, sh, col, w, line)
    if rim:
        g.fill(Diff(sh, Under(lambda x: f(x) + rim, x0, x1, y1)), tint_of(col, 0.3))
    if tufts:
        rnd = random.Random(seed)
        dark = shade_of(col, 0.82)
        for _ in range(tufts):
            x = rnd.uniform(x0, x1)
            top = float(f(np.array([x], np.float32))[0])
            y = rnd.uniform(top + rim + 6, min(H, top + 160))
            s = rnd.uniform(3, 6)
            for k in (-1, 0, 1):
                g.fill(Seg(x + k * s * 0.6, y, x + k * s * 1.1, y - s * (1.6 - abs(k) * 0.4), 1.6, 0.4), dark)
    return sh


def peak(g, xl, xr, ax, ay, base, col, snow=None, w=2.0, snow_k=0.32):
    """Triangular mountain split into lit (left) and shaded (right) halves, optional snow cap."""
    left = Poly([(xl, base), (ax, ay), (ax + (xr - ax) * 0.18, base)])
    right = Poly([(ax, ay), (xr, base), (ax + (xr - ax) * 0.18, base)])
    whole = Poly([(xl, base), (ax, ay), (xr, base)])
    if w:
        g.fill(Grow(whole, w), INK)
    g.fill(left, col)
    g.fill(right, shade_of(col))
    if snow:
        sy = ay + (base - ay) * snow_k
        lx, rx = ax + (xl - ax) * snow_k, ax + (xr - ax) * snow_k
        mid = ax + (xr - ax) * 0.18 * snow_k
        cap = Poly([(lx, sy), (ax, ay), (rx, sy), (rx - (rx - ax) * 0.3, sy - 10), (mid + 8, sy + 6),
                    (lx + (ax - lx) * 0.45, sy - 8)])
        g.fill(cap & left, snow)
        g.fill(cap & right, shade_of(snow, 0.85))


def toon_tree(g, x, base, h, col=(90, 170, 70), trunk=(130, 90, 60), seed=0, w=2.0, round_=True):
    rnd = random.Random(seed)
    tw = max(4, h * 0.1)
    cel(g, Box(x - tw / 2, base - h * 0.5, x + tw / 2, base, 2), trunk, w=w, off=(-tw * 0.4, 0))
    if round_:
        cy, r = base - h * 0.62, h * 0.32
        parts = [Circ(x, cy, r)] + [Circ(x + r * 0.7 * math.cos(a), cy + r * 0.55 * math.sin(a), r * rnd.uniform(0.55, 0.7))
                                     for a in np.linspace(0, math.tau, 6, endpoint=False)]
        cel(g, Union(parts), col, w=w, off=(-r * 0.3, -r * 0.35), hi=True, hi_off=(r * 0.12, r * 0.14))
    else:
        tiers = [Poly([(x - h * 0.3 * (1 - k * 0.22), base - h * (0.25 + k * 0.22)), (x, base - h * (0.62 + k * 0.2)),
                       (x + h * 0.3 * (1 - k * 0.22), base - h * (0.25 + k * 0.22))]) for k in range(3)]
        sh = Union(tiers)
        if w:
            g.fill(Grow(sh, w), INK)
        g.fill(sh, col)
        g.fill(sh & Box(x, 0, x + h, base), shade_of(col))


def toon_water(g, y0, y1, top, bottom, seed=0, x0=-2, x1=W + 2, dashes=60, line=(236, 248, 255)):
    g.fill(Box(x0, y0, x1, y1), vgrad([(y0, top), (y1, bottom)]))
    rnd = random.Random(seed)
    for _ in range(dashes):
        y = rnd.uniform(y0 + 4, y1 - 2)
        t = (y - y0) / max(1, y1 - y0)
        x = rnd.uniform(x0, x1)
        ln = 8 + 40 * t * rnd.uniform(0.5, 1.2)
        g.fill(Seg(x, y, x + ln, y, 1.2 + 2.2 * t), line, alpha=0.75)


def toon_window(g, x0, y0, x1, y1, glass=(150, 210, 245), frame=(250, 248, 240), lit=None, bars=True, w=1.6):
    ink(g, Box(x0 - 3, y0 - 3, x1 + 3, y1 + 3), frame, w)
    g.fill(Box(x0, y0, x1, y1), lit or glass)
    if not lit:
        g.fill(Poly([(x0 + (x1 - x0) * 0.2, y1), (x0 + (x1 - x0) * 0.42, y1), (x0 + (x1 - x0) * 0.8, y0), (x0 + (x1 - x0) * 0.58, y0)]),
               tint_of(glass, 0.55))
    if bars:
        g.fill(Box((x0 + x1) / 2 - 1.2, y0, (x0 + x1) / 2 + 1.2, y1), frame)
        g.fill(Box(x0, (y0 + y1) / 2 - 1.2, x1, (y0 + y1) / 2 + 1.2), frame)


def house(g, x0, base, w, h, wall, roof, side=0.0, roof_h=None, door=None, windows=2, w_ink=2.0, chimney=False):
    """Front-facing gabled house with optional shaded side wall; returns the roof peak."""
    x1 = x0 + w
    rh = roof_h or h * 0.7
    g.mul(Box(x0 + 4, base - 2, x1 + side + 10, base + 6), 0.4)
    if side:
        cel(g, Poly([(x1, base - h), (x1 + side, base - h - side * 0.3), (x1 + side, base - side * 0.3), (x1, base)]),
            shade_of(wall), w=w_ink, off=(0, 0))
    ink(g, Box(x0, base - h, x1, base), wall, w_ink)
    g.fill(Box(x0, base - h, x1, base - h + 6), shade_of(wall, 0.85))
    if chimney:
        cel(g, Box(x1 - w * 0.28, base - h - rh * 0.85, x1 - w * 0.14, base - h - rh * 0.3), (180, 120, 100), w=w_ink, off=(-3, 0))
    rf = Poly([(x0 - 6, base - h + 2), ((x0 + x1) / 2, base - h - rh), (x1 + 6, base - h + 2)])
    if side:
        rf = Union([rf, Poly([((x0 + x1) / 2, base - h - rh), ((x0 + x1) / 2 + side, base - h - rh - side * 0.3),
                              (x1 + side + 6, base - h + 2 - side * 0.3), (x1 + 6, base - h + 2)])])
    ink(g, rf, roof, w_ink)
    g.fill(rf & Box((x0 + x1) / 2, 0, W + 50, base), shade_of(roof))
    ww = w * 0.2
    for k in range(windows):
        cx = x0 + w * (k + 1) / (windows + 1)
        toon_window(g, cx - ww / 2, base - h * 0.72, cx + ww / 2, base - h * 0.72 + ww * 1.1, w=1.2)
    if door:
        dw = w * 0.2
        cel(g, Box((x0 + x1) / 2 - dw / 2, base - h * 0.45, (x0 + x1) / 2 + dw / 2, base, 2), door, w=1.4, off=(-2.5, 0))
    return ((x0 + x1) / 2, base - h - rh)


def figure(g, x, base, h, shirt, pants=(60, 70, 110), skin=(250, 210, 176), hair=(90, 60, 40), hat=None, w=1.6):
    k = h / 60.0
    for dx in (-4, 4):
        cel(g, Box(x + dx * k - 3 * k, base - 24 * k, x + dx * k + 3 * k, base, 2 * k), pants, w=w, off=(-2 * k, 0))
    cel(g, Box(x - 10 * k, base - 46 * k, x + 10 * k, base - 20 * k, 5 * k), shirt, w=w, off=(-4 * k, -2 * k))
    cel(g, Circ(x, base - 54 * k, 9 * k), skin, w=w, off=(-3 * k, -3 * k))
    g.fill(Ell(x - 1 * k, base - 60 * k, 9 * k, 5 * k), hair)
    if hat:
        cel(g, Ell(x, base - 62 * k, 13 * k, 3.5 * k), hat, w=w, off=(-3 * k, 0))
        cel(g, Box(x - 7 * k, base - 72 * k, x + 7 * k, base - 61 * k, 3 * k), hat, w=w, off=(-3 * k, 0))


# ------------------------------------------------------------------- animated elements
def cloud_el(eid, x, y, w, h, speed=6.0, seed=0, start=0.0, **kw):
    return E(eid, el(lambda g, m: toon_cloud(g, x, y, w, h, seed=seed)), pivot=(x, y),
             anim=drift_across(x - w - 4, x + w + 4, speed, start=start), **kw)


def puff_el(eid, x, y, r=8, rise=60, wind=-14, phase=0.0, col=(250, 250, 250)):
    return E(eid, el(lambda g, m: cel(g, Circ(x, y, r), col, w=1.4, shade=(206, 214, 236), off=(-r * 0.3, -r * 0.35), col=(150, 160, 190))),
             pivot=(x, y), anim=dict(driftVelocity=(wind, rise), driftLength=rise, driftFade=True, driftGrow=1.2, phase=phase))


def bird_el(eid, x, y, s=7, speed=20, col=INK, start=0.0):
    def d(g, m):
        g.fill(Seg(x - s, y - s * 0.45, x, y, 2.2, 1.6), col)
        g.fill(Seg(x, y, x + s, y - s * 0.45, 1.6, 2.2), col)
    return E(eid, el(d), pivot=(x, y), anim=dict(drift_across(x - s, x + s, speed, start=start), stretch=(0, 0.5),
                                                 scaleSpeed=2.2, bobAmplitude=(0, 5), bobSpeed=0.2))


def sparkle_el(eid, pts, col=(255, 255, 255), r=5, speed=0.7, phase=0.0, daynight="untinted"):
    def d(g, m):
        for x, y in pts:
            g.fill(Poly([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28), (x, y + r),
                         (x - r * 0.28, y + r * 0.28), (x - r, y), (x - r * 0.28, y - r * 0.28)]), col)
    return E(eid, el(d), daynight=daynight, anim=dict(twinkle=0.9, twinkleSpeed=speed, phase=phase))
