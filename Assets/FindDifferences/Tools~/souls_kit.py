# -*- coding: utf-8 -*-
"""Realistic dark-fantasy kit (real.py based) for the gothic-city and fallen-kingdom levels (Level1565-1584).

Everything here is an original design: gothic Victorian streets and cathedrals, hunters in long coats and
brimmed hats, armoured knights, beasts and dragons as dark silhouettes, campfires, torches, coffins, cages.
No gore: no blood, no corpses, no skulls.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (C, Box, Circ, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm, fbm1,
                  grain_tex, lgrad, light_x, light_y, mixc, rgrad, smooth, sphere_paint, tex, vgrad)
from levels_real2 import arch, ashlar, flame, rim, stains

MOON = (180, 196, 240)
FIRE = (255, 150, 60)
IRON = (26, 24, 28)


def n1(x, scale, seed=0):
    """Scalar 1-D noise in 0..1."""
    return float(fbm1(np.array([x], np.float32), scale, 2, seed)[0])


# =================================================================== architecture
def lancet(g, x0, x1, ys, y1, lit=None, frame=(30, 28, 32), mull=True, glass=(26, 30, 44)):
    """Pointed-arch window: dark glass or warm lit glass (lit = colour), with a mullion and transom."""
    shape = arch(x0, x1, ys, y1)
    if lit is not None:
        g.glow((x0 + x1) / 2, (ys + y1) / 2, (x1 - x0) * 2.2, lit, 0.22, power=1.8)
        g.fill(shape, lgrad(0, ys - (x1 - x0), 0, y1, [(0, mixc(lit, (255, 255, 255), 0.35)), (1, mixc(lit, (0, 0, 0), 0.25))]))
    else:
        g.fill(shape, vgrad([(ys - (x1 - x0), mixc(glass, (90, 100, 140), 0.25)), (y1, glass)]))
    if mull:
        bars = [Box((x0 + x1) / 2 - 1, ys - (x1 - x0) * 0.8, (x0 + x1) / 2 + 1, y1), Box(x0, (ys + y1) / 2 - 1, x1, (ys + y1) / 2 + 1)]
        g.fill(Inter(Union(bars), shape), frame)
    g.fill(Diff(arch(x0 - 3, x1 + 3, ys, y1 + 3), shape), frame)
    return shape


def stone(base, seed, bw=24, bh=11):
    return ashlar(base, bw, bh, seed)


def wall(g, shape, base, seed, x0, x1, light=-1, bw=24, bh=11, dark=(0.25, 0.55)):
    """Ashlar wall lit from one side (light = -1 left, 1 right)."""
    g.fill(shape, stone(base, seed, bw, bh))
    a0, a1 = dark if light < 0 else dark[::-1]
    g.fill(shape, (0, 0, 0), alpha=lambda X, Y: a0 + (a1 - a0) * smooth(x0, x1, X))


def spire(g, cx, base, w, h, col, seed=0, light=-1, crockets=True, finial=True):
    """Tall stone spire on a square drum: drum with lancet slots, needle with crockets and a cross-less finial."""
    drum_h = h * 0.32
    drum = Box(cx - w / 2, base - drum_h, cx + w / 2, base)
    wall(g, drum, col, seed, cx - w / 2, cx + w / 2, light, bw=12, bh=7)
    g.fill(arch(cx - w * 0.16, cx + w * 0.16, base - drum_h * 0.62, base - drum_h * 0.12), (14, 14, 20))
    for sg in (-1, 1):
        g.fill(Poly([(cx + sg * w * 0.5, base - drum_h), (cx + sg * w * 0.62, base - drum_h - w * 0.5), (cx + sg * w * 0.38, base - drum_h)]),
               mixc(col, (0, 0, 0), 0.35))
    needle = Poly([(cx - w * 0.42, base - drum_h), (cx, base - h), (cx + w * 0.42, base - drum_h)])
    g.fill(needle, tex(light_x(col, cx - w * 0.42, cx + w * 0.42, *((1.25, 0.5) if light < 0 else (0.5, 1.25))), 0.18, 3, 6, 3, seed))
    if crockets:
        n = int((h - drum_h) / 14)
        for i in range(1, n):
            t = i / n
            yy = base - drum_h - (h - drum_h) * t
            hw = w * 0.42 * (1 - t)
            for sg in (-1, 1):
                g.fill(Ell(cx + sg * (hw + 1.6), yy, 2.4, 1.6), mixc(col, (0, 0, 0), 0.15 if sg == light else 0.5))
    if finial:
        g.fill(Seg(cx, base - h, cx, base - h - 10, 1.2), mixc(col, (0, 0, 0), 0.3))
        g.fill(Circ(cx, base - h - 11, 2.2), mixc(col, (0, 0, 0), 0.3))
    return needle


def skyline(g, base, hmin, hmax, col, seed, x0=-20, x1=W + 20, spires=0.35, lit=None, lit_p=0.1, haze=None):
    """Distant gothic city: blocky roofs, pointed gables and needle spires as a hazy silhouette."""
    rnd = random.Random(seed)
    shapes, wins = [], []
    x = x0
    while x < x1:
        w = rnd.uniform(18, 46)
        h = rnd.uniform(hmin, hmax)
        shapes.append(Box(x, base - h, x + w, base + 2))
        r = rnd.random()
        if r < spires:
            sw = w * rnd.uniform(0.3, 0.6)
            sx = x + rnd.uniform(0.2, 0.8) * w
            shapes.append(Poly([(sx - sw / 2, base - h + 1), (sx, base - h - rnd.uniform(1.4, 3.2) * sw), (sx + sw / 2, base - h + 1)]))
        elif r < 0.75:
            shapes.append(Poly([(x, base - h + 1), (x + w / 2, base - h - w * 0.45), (x + w, base - h + 1)]))
        if lit is not None:
            for wy in np.arange(base - h + 8, base - 4, 9):
                for wx in np.arange(x + 4, x + w - 4, 7):
                    if rnd.random() < lit_p:
                        wins.append(Box(wx, wy, wx + 2.2, wy + 3.6))
        x += w * rnd.uniform(0.7, 1.05)
    g.fill(Union(shapes), col)
    if wins:
        g.fill(Union(wins), lit)
    if haze is not None:
        hc, a0, a1 = haze
        g.fog(base - hmax * 1.6, base, hc, a0, a1)


def buttress(g, x, base, w, h, col, seed=0, light=-1):
    s = Poly([(x - w / 2, base), (x - w / 2, base - h * 0.75), (x, base - h), (x + w / 2, base - h * 0.75), (x + w / 2, base)])
    wall(g, s, col, seed, x - w / 2, x + w / 2, light, bw=10, bh=8)
    return s


def railing(g, x0, x1, y, h, col=IRON, step=10, spikes=True):
    bars = [Box(x, y - h, x + 2, y) for x in np.arange(x0, x1, step)]
    tips = [Poly([(x - 1.6, y - h + 1), (x + 1, y - h - 7), (x + 3.6, y - h + 1)]) for x in np.arange(x0, x1, step)] if spikes else []
    g.fill(Union(bars + tips + [Box(x0 - 2, y - h + 4, x1 + 2, y - h + 7), Box(x0 - 2, y - 8, x1 + 2, y - 5)]), col)


def cobbles(paint_base, seed=0, sx=14, sy=7):
    """Wet cobblestone road paint (rounded setts with dark joints)."""
    base = C(paint_base)

    def f(X, Y):
        row = np.floor(Y / sy).astype(np.int64)
        xx = X + (row % 2) * sx * 0.5
        fx, fy = xx / sx - np.floor(xx / sx), Y / sy - row
        joint = smooth(0.0, 0.14, fx) * smooth(1.0, 0.86, fx) * smooth(0.0, 0.2, fy) * smooth(1.0, 0.8, fy)
        n = fbm(X, Y, 4, 3, 3, seed)
        return base * ((0.5 + 0.5 * joint) * (0.8 + 0.4 * n))[..., None]
    return f


# =================================================================== props
def gas_lamp(g, x, base, h, lit=True, col=IRON, light=(255, 196, 110)):
    """Victorian street lamp: fluted post, lantern head with a glowing mantle."""
    g.mul(Ell(x + 4, base + 1, 14, 3), 0.5, feather=3)
    g.fill(Box(x - 6, base - 12, x + 6, base, 2), col)
    g.fill(Seg(x, base - 10, x, base - h + 18, 3.2, 2.2), light_x(col, x - 4, x + 4, 1.6, 0.6))
    g.fill(Seg(x - 10, base - h + 22, x + 10, base - h + 22, 1.6), col)
    head = Poly([(x - 9, base - h + 18), (x - 12, base - h), (x + 12, base - h), (x + 9, base - h + 18)])
    if lit:
        g.glow(x, base - h + 9, 70, light, 0.3, power=2.0)
        g.fill(head, rgrad(x, base - h + 9, 14, [(0, (255, 248, 220)), (0.5, light), (1, mixc(light, (0, 0, 0), 0.3))]))
    else:
        g.fill(head, (40, 46, 58))
        g.add(Box(x - 8, base - h + 2, x - 5, base - h + 16), MOON, 0.18)
    g.fill(Union([Box(x - 1, base - h, x + 1, base - h + 18), Box(x - 12, base - h + 8, x + 12, base - h + 9.4)]), col)
    g.fill(Poly([(x - 15, base - h + 1), (x, base - h - 11), (x + 15, base - h + 1)]), col)
    g.fill(Circ(x, base - h - 13, 2.4), col)


def torch(g, x, y, lit=True, col=IRON):
    """Wall sconce torch (the flame itself is an animated element)."""
    g.fill(Seg(x, y + 26, x, y + 6, 2.2), col)
    g.fill(Seg(x - 6, y + 22, x, y + 26, 1.4), col)
    g.fill(Poly([(x - 6, y + 8), (x + 6, y + 8), (x + 4, y), (x - 4, y)]), (70, 50, 34))
    if lit:
        g.glow(x, y - 8, 90, FIRE, 0.28, power=1.8)


def fire_el(eid, x, y, s=1.0, phase=0.0):
    """A torch / campfire flame tongue that flickers."""
    def draw(g, m):
        g.glow(x, y - 6 * s, 16 * s, (255, 150, 60), 0.5)
        sh = Union([Ell(x, y - 5 * s, 6 * s, 7 * s), Poly([(x - 6 * s, y - 7 * s), (x - 1 * s, y - 30 * s), (x + 6 * s, y - 7 * s)])])
        g.fill(sh, lgrad(x, y - 30 * s, x, y, [(0, (255, 110, 30)), (0.5, (255, 190, 90)), (1, (255, 246, 210))]), feather=1.0)
    return E(eid, el(draw), pivot=(x, y), daynight="untinted", anim=dict(stretch=(0.08, 0.25), scaleSpeed=2.1 + phase, pulse=0.06, phase=phase))


def ember_el(eid, x, y, spread=20, n=5, rise=110, wind=8, col=(255, 170, 80), phase=0.0, seed=0):
    """Sparks rising from a fire (anim y points up)."""
    rnd = random.Random(seed)
    pts = [(x + rnd.uniform(-spread, spread), y + rnd.uniform(-10, 10)) for _ in range(n)]
    return E(eid, el(lambda g, m: [g.glow(px, py, 2.6, col, 1.0, power=1.2) for px, py in pts]), daynight="untinted",
             anim=dict(driftVelocity=(wind, rise), driftLength=rise * 0.9, driftFade=True, phase=phase))


def campfire(g, x, base, s=1.0, lit=True):
    """Log pile with ash and glowing coals (flames are elements)."""
    g.mul(Ell(x, base + 2, 46 * s, 10 * s), 0.5, feather=6)
    g.fill(Rough(Ell(x, base - 2, 40 * s, 9 * s), 2, 6, 3), tex((60, 56, 54), 0.4, 3, 2, 3, 5))
    for i, (a, b) in enumerate((((-34, 4), (22, -22)), ((30, 6), (-18, -24)), ((-10, 8), (34, -12)), ((-36, -6), (14, -6)))):
        g.fill(Seg(x + a[0] * s, base + a[1] * s, x + b[0] * s, base + b[1] * s, 6 * s, 5 * s),
               tex(light_y((90, 64, 44), base - 26 * s, base + 8 * s, 1.3, 0.5), 0.25, 1.5, 5, 3, 40 + i))
    if lit:
        g.glow(x, base - 10 * s, 160 * s, FIRE, 0.42, power=1.7)
        g.fill(Rough(Ell(x, base - 4 * s, 22 * s, 6 * s), 2, 4, 9), rgrad(x, base - 4 * s, 22 * s, [(0, (255, 220, 140)), (1, (200, 60, 20))]))


def coffin(g, x, base, w, h, col=(64, 44, 34), seed=0, lean=0.0, chain=True, lid_cross=True):
    """Standing hexagonal coffin, optionally bound with chains."""
    pts = [(x - w * 0.36, base), (x - w * 0.5, base - h * 0.72), (x - w * 0.3, base - h), (x + w * 0.3, base - h),
           (x + w * 0.5, base - h * 0.72), (x + w * 0.36, base)]
    if lean:
        pts = [(px + (base - py) * lean, py) for px, py in pts]
    s = Poly(pts)
    g.mul(Ell(x + 8, base + 2, w * 0.7, 4), 0.5, feather=4)
    g.fill(s, tex(light_x(col, x - w / 2, x + w / 2, 1.3, 0.6), 0.22, 1.5, 8, 3, seed))
    rim(g, s, -1.6, 0, k=0.25)
    if lid_cross:
        cx = x + (h * 0.62) * lean
        g.fill(Union([Box(cx - 2, base - h * 0.85, cx + 2, base - h * 0.35), Box(cx - 9, base - h * 0.72, cx + 9, base - h * 0.68)]),
               mixc(col, (0, 0, 0), 0.4))
    if chain:
        for t in (0.3, 0.62):
            yy = base - h * t
            dx = (h * t) * lean
            for k in range(int(w / 5) + 1):
                cx = x - w * 0.46 + dx + k * 5
                g.fill(Ell(cx, yy + (k % 2) * 0.6, 2.8, 1.8) - Ell(cx, yy + (k % 2) * 0.6, 1.4, 0.7), (90, 88, 92))
    return s


def cage(g, x, top, w, h, col=IRON, chain_len=60):
    """Hanging iron gibbet cage (empty)."""
    for k in range(int(chain_len / 6)):
        g.fill(Ell(x, top - chain_len + k * 6, 1.8 if k % 2 else 1.0, 3.2) - Ell(x, top - chain_len + k * 6, 0.6, 1.8), col)
    body = Union([Ell(x, top + 6, w / 2, 8), Box(x - w / 2, top + 6, x + w / 2, top + h - 8)])
    bars = [Seg(x + (i - 3) * w / 6, top + 4, x + (i - 3) * w / 6, top + h - 4, 1.4) for i in range(7)]
    rings = [Box(x - w / 2, top + 6, x + w / 2, top + 9), Box(x - w / 2, top + h * 0.5, x + w / 2, top + h * 0.5 + 2.5),
             Box(x - w / 2, top + h - 9, x + w / 2, top + h - 6)]
    g.fill(Union(bars + rings), col)
    g.fill(Ell(x, top + h - 7, w / 2, 4), col)
    g.add(Union([Seg(x - w / 2 + 1, top + 6, x - w / 2 + 1, top + h - 8, 0.8)]), MOON, 0.25)
    return body


def barrel(g, x, base, r, h, col=(96, 66, 42), seed=0):
    s = Box(x - r, base - h, x + r, base, r * 0.25)
    g.mul(Ell(x + 6, base + 1, r * 1.3, 4), 0.5, feather=4)
    g.fill(s, tex(cyl_paint(x, r, col, amb=0.35, spec=0.1), 0.18, 1.2, 9, 3, seed))
    for yy in (base - h * 0.18, base - h * 0.82):
        g.fill(Box(x - r, yy - 2, x + r, yy + 2), cyl_paint(x, r, (60, 58, 60), amb=0.35, spec=0.4))
    return s


def crate(g, x0, base, w, h, col=(110, 82, 54), seed=0):
    s = Box(x0, base - h, x0 + w, base, 1.5)
    g.mul(Ell(x0 + w * 0.6, base + 1, w * 0.7, 4), 0.5, feather=4)
    g.fill(s, tex(light_x(col, x0, x0 + w, 1.2, 0.7), 0.2, 1.2, 8, 3, seed))
    g.fill(Union([Seg(x0 + 3, base - 3, x0 + w - 3, base - h + 3, 2.2), Box(x0, base - h, x0 + w, base - h + 4), Box(x0, base - 4, x0 + w, base)]),
           mixc(col, (0, 0, 0), 0.35))
    return s


def banner(g, x, top, w, h, col, emblem=None, seed=0, tatter=True, pole=True):
    """Hanging cloth banner with a tattered hem; emblem(g, cx, cy, s) draws its device."""
    if pole:
        g.fill(Seg(x - w * 0.62, top, x + w * 0.62, top, 2.2), (60, 50, 40))
    pts = [(x - w / 2, top), (x + w / 2, top), (x + w / 2, top + h * 0.85)]
    n = 6
    for i in range(n + 1):
        t = 1 - i / n
        pts.append((x - w / 2 + w * t, top + h * (0.85 + (0.15 if i % 2 else 0.0)) + (n1(i * 7.0, 3, seed) - 0.5) * 8 * tatter))
    s = Poly(pts)

    def paint(X, Y):
        fold = 0.78 + 0.22 * np.sin((X - x) * 0.32)
        return C(col) * (fold * (0.85 + 0.3 * fbm(X, Y, 3, 8, 3, seed)))[..., None]
    g.fill(s, paint)
    g.fill(s, (0, 0, 0), alpha=lambda X, Y: 0.35 * smooth(top, top + h, Y))
    if emblem is not None:
        emblem(g, x, top + h * 0.42, w * 0.32)
    return s


def emblem_sun(g, cx, cy, s, col=(200, 160, 70)):
    g.fill(Circ(cx, cy, s * 0.5), col)
    for i in range(12):
        a = i * math.tau / 12
        g.fill(Seg(cx + math.cos(a) * s * 0.55, cy + math.sin(a) * s * 0.55, cx + math.cos(a) * s * 0.95, cy + math.sin(a) * s * 0.95, s * 0.09, 0.4),
               col)


def emblem_moon(g, cx, cy, s, col=(210, 210, 200)):
    g.fill(Circ(cx, cy, s * 0.7) - Circ(cx + s * 0.32, cy - s * 0.12, s * 0.6), col)


def emblem_tree(g, cx, cy, s, col=(200, 170, 90)):
    g.fill(Seg(cx, cy + s * 0.8, cx, cy - s * 0.1, s * 0.12, s * 0.08), col)
    for a in (-0.9, -0.4, 0.4, 0.9):
        g.fill(Seg(cx, cy + s * 0.1, cx + math.sin(a) * s * 0.8, cy - s * 0.6, s * 0.08, s * 0.03), col)


def chain(g, x0, y0, x1, y1, col=(70, 68, 72), sag=12, link=5.5):
    n = max(2, int(math.hypot(x1 - x0, y1 - y0) / link))
    for i in range(n + 1):
        t = i / n
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
        if i % 2:
            g.fill(Ell(px, py, 2.8, 1.6) - Ell(px, py, 1.4, 0.6), col)
        else:
            g.fill(Ell(px, py, 1.4, 2.6) - Ell(px, py, 0.5, 1.3), col)


def crow(g, x, y, s=1.0, col=(12, 10, 14), face=-1, eye=(200, 180, 120)):
    """Perched crow (feet at x, y)."""
    g.fill(Ell(x, y - 11 * s, 8 * s, 11.5 * s), col)
    g.fill(Circ(x + face * 5 * s, y - 24 * s, 6 * s), col)
    g.fill(Poly([(x + face * 10 * s, y - 26 * s), (x + face * 19 * s, y - 23 * s), (x + face * 10 * s, y - 21 * s)]), (34, 30, 32))
    g.fill(Poly([(x - face * 5 * s, y - 8 * s), (x - face * 19 * s, y - 1 * s), (x - face * 5 * s, y - 2 * s)]), col)
    g.fill(Circ(x + face * 7 * s, y - 25 * s, 1.3 * s), eye)
    g.fill(Union([Seg(x - 2 * s, y - 2 * s, x - 3 * s, y, 0.8 * s), Seg(x + 2 * s, y - 2 * s, x + 3 * s, y, 0.8 * s)]), col)


def statue(g, x, base, h, col=(118, 116, 112), seed=0, light=-1, hood=True, arms="pray", plinth=True):
    """Robed stone statue on a plinth (hooded, hands folded or holding a sword point-down)."""
    k = h / 200.0
    ph = 26 * k if plinth else 0
    if plinth:
        wall(g, Box(x - 34 * k, base - ph, x + 34 * k, base), col, seed, x - 34 * k, x + 34 * k, light, bw=16, bh=9)
        g.fill(Box(x - 38 * k, base - ph - 5 * k, x + 38 * k, base - ph), light_y(col, base - ph - 5 * k, base - ph, 1.2, 0.8))
    b = base - ph - 5 * k
    paint = tex(light_x(col, x - 30 * k, x + 30 * k, *((1.3, 0.55) if light < 0 else (0.55, 1.3))), 0.2, 3, 4, 4, seed)
    robe = Poly([(x - 30 * k, b), (x - 22 * k, b - 110 * k), (x - 18 * k, b - 150 * k), (x + 18 * k, b - 150 * k),
                 (x + 22 * k, b - 110 * k), (x + 30 * k, b)])
    g.fill(robe, paint)
    for f in (-12, -2, 9, 19):
        g.mul(Seg(x + f * k, b - 2, x + f * 0.7 * k, b - 120 * k, 1.6 * k, 0.6 * k), 0.35, feather=1.5)
    head = Union([Ell(x, b - 160 * k, 13 * k, 16 * k)])
    if hood:
        head = Union([head, Poly([(x - 20 * k, b - 146 * k), (x - 16 * k, b - 172 * k), (x, b - 182 * k), (x + 16 * k, b - 172 * k), (x + 20 * k, b - 146 * k)])])
    g.fill(head, paint)
    if hood:
        g.fill(Ell(x - light * 2 * k, b - 158 * k, 8 * k, 11 * k), mixc(col, (0, 0, 0), 0.65))
    if arms == "pray":
        g.fill(Poly([(x - 16 * k, b - 128 * k), (x, b - 104 * k), (x + 16 * k, b - 128 * k), (x + 8 * k, b - 96 * k), (x - 8 * k, b - 96 * k)]), paint)
        g.fill(Ell(x, b - 100 * k, 5 * k, 9 * k), paint)
    elif arms == "sword":
        g.fill(Seg(x, b - 104 * k, x, b - 4 * k, 4.5 * k, 2.5 * k), paint)
        g.fill(Box(x - 18 * k, b - 112 * k, x + 18 * k, b - 106 * k), paint)
        g.fill(Ell(x, b - 116 * k, 9 * k, 7 * k), paint)
    g.mul(robe, 0.4, alpha=lambda X, Y: smooth(b - 40 * k, b, Y))
    rim(g, robe, -light * 2, 0, k=0.25)
    return robe


# =================================================================== characters (original designs)
def hunter(g, x, base, h, coat=(46, 40, 38), trim=(70, 60, 52), skin=(200, 176, 156), face=1, weapon="axe",
           hat=(30, 28, 28), scarf=(90, 84, 76), rim_dx=-2.2, rim_col=MOON, rim_k=0.5, pistol=True, lantern=False):
    """Hunter in a long tattered greatcoat, brimmed hat and face scarf, facing `face` (1 right, -1 left).
    weapon: 'axe' (long-hafted axe over the shoulder), 'cane' (sword-cane), None."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    g.mul(Ell(x + 10 * k, base + 2, 60 * k, 8 * k), 0.5, feather=6 * k)
    # boots + legs
    for lx, fx in ((-14, -22), (12, 14)):
        g.fill(Seg(sx(lx), sy(126), sx(fx), sy(14), 13 * k, 11 * k), light_x((36, 34, 34), sx(lx) - 14 * k, sx(lx) + 14 * k, 1.2, 0.6))
        g.fill(Ell(sx(fx + 6), sy(7), 15 * k, 7 * k), sphere_paint(sx(fx + 2), sy(10), 15 * k, (28, 24, 22), ry=7 * k, spec=0.4))
    # greatcoat: tails flaring backwards, ragged hem
    hem = []
    for i in range(9):
        t = i / 8
        hem.append((sx(-58 + 108 * t), sy(40 + 22 * (i % 2) + (n1(i * 3.0, 2, 7) - 0.5) * 18)))
    cpts = [(sx(-32), sy(236)), (sx(30), sy(238)), (sx(40), sy(150)), (sx(50), sy(50))] + hem[::-1] + [(sx(-58), sy(42)), (sx(-44), sy(150))]
    cs = Poly(cpts)

    def coat_paint(X, Y):
        fold = 0.75 + 0.25 * np.sin((X - x) * 0.14 / k + (Y - base) * 0.012 / k)
        return C(coat) * (fold * (0.85 + 0.3 * fbm(X, Y, 4 * k, 18 * k, 3, 61)))[..., None]
    g.fill(cs, coat_paint)
    g.fill(cs, (0, 0, 0), alpha=lambda X, Y: 0.3 * smooth(sy(240), sy(40), Y))
    g.fill(Seg(sx(-30), sy(150), sx(36), sy(150), 5 * k), (40, 30, 24))
    g.fill(Box(sx(2) - 5 * k, sy(155), sx(2) + 5 * k, sy(145)), (150, 130, 90))
    rim(g, cs, rim_dx, 0, col=rim_col, k=rim_k * 0.6)
    # back arm (pistol)
    g.fill(Seg(sx(-28), sy(226), sx(-44), sy(150), 13 * k, 11 * k), coat_paint)
    if pistol:
        px_, py_ = sx(-46), sy(140)
        g.fill(Ell(px_, py_, 7 * k, 7 * k), (40, 36, 34))
        g.fill(Seg(px_, py_, sx(-50), sy(104), 4 * k, 3 * k), (70, 66, 64))
        g.fill(Seg(px_ - f * 2 * k, py_ + 2 * k, px_ + f * 4 * k, py_ + 14 * k, 4 * k), (80, 56, 36))
    # front arm
    g.fill(Seg(sx(26), sy(226), sx(44), sy(158), 13 * k, 11 * k), coat_paint)
    hand = (sx(48), sy(150))
    g.fill(Ell(hand[0], hand[1], 7 * k, 7 * k), (40, 34, 30))
    # shoulder cape / mantle
    mantle = Poly([(sx(-40), sy(232)), (sx(-34), sy(250)), (sx(0), sy(258)), (sx(34), sy(250)), (sx(42), sy(226)), (sx(30), sy(200)),
                   (sx(10), sy(214)), (sx(-12), sy(198)), (sx(-34), sy(208))])
    g.fill(mantle, light_x(trim, sx(-40), sx(42), *((1.3, 0.6) if rim_dx < 0 else (0.6, 1.3))))
    rim(g, mantle, rim_dx, 0, col=rim_col, k=rim_k * 0.6)
    # head: scarf over the lower face, brimmed hat
    hx, hy = sx(4), sy(272)
    g.fill(Ell(hx, hy, 15 * k, 18 * k), sphere_paint(hx - f * 3 * k, hy - 3 * k, 15 * k, skin, ry=18 * k, amb=0.4, spec=0.1))
    g.fill(Poly([(hx - 17 * k, hy - 1 * k), (hx + 17 * k, hy - 1 * k), (hx + 18 * k, hy + 20 * k), (hx - 16 * k, hy + 24 * k)]),
           tex(light_x(scarf, hx - 17 * k, hx + 17 * k, 1.2, 0.6), 0.2, 2, 3, 3, 62))
    g.fill(Seg(hx + f * 3 * k, hy - 5 * k, hx + f * 11 * k, hy - 5 * k, 1.6 * k), (30, 24, 24))
    brim = Ell(hx, hy - 15 * k, 34 * k, 7 * k)
    crown_s = Union([Box(hx - 16 * k, hy - 36 * k, hx + 16 * k, hy - 14 * k, 5 * k), Ell(hx, hy - 36 * k, 16 * k, 4 * k)])
    if hat is not None:
        g.fill(brim, light_x(hat, hx - 34 * k, hx + 34 * k, 1.3, 0.6))
        g.fill(crown_s, light_x(hat, hx - 16 * k, hx + 16 * k, 1.3, 0.6))
        g.fill(Box(hx - 16 * k, hy - 20 * k, hx + 16 * k, hy - 15 * k), (70, 56, 44))
        rim(g, Union([brim, crown_s]), rim_dx, 0.5, col=rim_col, k=rim_k)
    # weapon
    if weapon == "axe":
        g.fill(Seg(hand[0], hand[1], sx(-10), sy(330), 3.2 * k), tex(light_x((86, 62, 42), sx(-12), sx(50), 1.3, 0.7), 0.2, 1, 6))
        blade = Poly([(sx(-16), sy(318)), (sx(-52), sy(338)), (sx(-60), sy(300)), (sx(-38), sy(296)), (sx(-12), sy(306))])
        g.fill(blade, lgrad(sx(-60), sy(330), sx(-12), sy(300), [(0, (150, 152, 160)), (1, (64, 64, 70))]))
        g.add(Seg(sx(-56), sy(326), sx(-58), sy(304), 1.2 * k), (230, 236, 255), 0.5)
    elif weapon == "cane":
        g.fill(Seg(hand[0], hand[1], sx(120), sy(20), 2.6 * k, 1.8 * k), lgrad(hand[0], hand[1], sx(120), sy(20), [(0, (190, 194, 204)), (1, (110, 112, 122))]))
        g.fill(Seg(sx(40), sy(160), sx(56), sy(140), 3 * k), (150, 120, 60))
    if lantern:
        lx_, ly_ = sx(-34), sy(232)
        g.fill(Seg(lx_, ly_ - 8 * k, lx_, ly_ + 4 * k, 1 * k), (60, 50, 40))
        g.glow(lx_, ly_ + 14 * k, 60 * k, FIRE, 0.4)
        g.fill(Box(lx_ - 6 * k, ly_ + 4 * k, lx_ + 6 * k, ly_ + 22 * k, 1.5 * k), (255, 200, 120))
    return dict(head=(hx, hy), hand=hand, coat=cs)


def knight(g, x, base, h, steel=(120, 122, 130), cloth=(80, 30, 30), face=1, sword="up", shield=None, helm="great",
           rim_dx=-2.0, rim_col=MOON, rim_k=0.45, plume=None, kneel=False):
    """Armoured knight (original design): great helm or bascinet, surcoat, sword and optional heater shield.
    shield = (field colour, emblem fn or None)."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    metal = lambda x0, x1: tex(light_x(steel, x0, x1, *((1.45, 0.45) if rim_dx < 0 else (0.45, 1.45))), 0.12, 2, 3, 3, 71)
    g.mul(Ell(x + 10 * k, base + 2, 64 * k, 8 * k), 0.5, feather=6 * k)
    hip = 130 if not kneel else 70
    # legs (greaves + sabatons)
    if not kneel:
        legs = ((-16, -24), (14, 16))
        for lx, fx in legs:
            g.fill(Seg(sx(lx), sy(hip), sx(fx), sy(14), 14 * k, 11 * k), metal(sx(lx) - 15 * k, sx(lx) + 15 * k))
            g.fill(Ell(sx(lx * 0.6 + fx * 0.4), sy(70), 10 * k, 8 * k), metal(sx(lx) - 10 * k, sx(lx) + 10 * k))
            g.fill(Ell(sx(fx + 6), sy(7), 15 * k, 7 * k), metal(sx(fx) - 9 * k, sx(fx) + 21 * k))
    else:
        g.fill(Seg(sx(-14), sy(hip), sx(-40), sy(14), 14 * k, 11 * k), metal(sx(-50), sx(0)))
        g.fill(Seg(sx(14), sy(hip), sx(54), sy(66), 14 * k, 12 * k), metal(sx(0), sx(60)))
        g.fill(Seg(sx(54), sy(66), sx(54), sy(10), 12 * k, 10 * k), metal(sx(40), sx(66)))
        g.fill(Ell(sx(60), sy(7), 15 * k, 7 * k), metal(sx(46), sx(76)))
    # surcoat skirt
    top = hip + 110
    skirt = Poly([(sx(-34), sy(hip + 50)), (sx(34), sy(hip + 50)), (sx(44), sy(hip - 60)), (sx(14), sy(hip - 50)), (sx(0), sy(hip - 64)),
                  (sx(-16), sy(hip - 48)), (sx(-44), sy(hip - 58))])
    g.fill(skirt, tex(light_x(cloth, sx(-44), sx(44), 1.3, 0.55), 0.18, 2, 8, 3, 72))
    rim(g, skirt, rim_dx, 0, col=rim_col, k=rim_k * 0.5)
    # cuirass
    torso = Poly([(sx(-36), sy(top)), (sx(36), sy(top)), (sx(32), sy(hip + 40)), (sx(-32), sy(hip + 40))])
    g.fill(torso, metal(sx(-36), sx(36)))
    g.fill(Seg(sx(0), sy(top - 4), sx(0), sy(hip + 46), 2 * k), mixc(steel, (255, 255, 255), 0.25))
    g.fill(Box(sx(-34), sy(hip + 48), sx(34), sy(hip + 38)), (60, 44, 32))
    rim(g, torso, rim_dx, 0, col=rim_col, k=rim_k)
    # pauldrons
    for sg in (-1, 1):
        pa = Ell(sx(sg * 38), sy(top - 8), 20 * k, 15 * k)
        g.fill(pa, sphere_paint(sx(sg * 38 - 6), sy(top - 4), 20 * k, steel, ry=15 * k, amb=0.35, spec=0.6, shin=26))
        g.fill(Ell(sx(sg * 38), sy(top - 18), 20 * k, 4 * k), mixc(steel, (0, 0, 0), 0.4), alpha=0.5)
    # arms
    g.fill(Seg(sx(-40), sy(top - 14), sx(-46), sy(hip + 30), 12 * k, 10 * k), metal(sx(-58), sx(-34)))
    g.fill(Seg(sx(40), sy(top - 14), sx(46), sy(hip + 50), 12 * k, 10 * k), metal(sx(34), sx(58)))
    hand = (sx(46), sy(hip + 44))
    g.fill(Ell(hand[0], hand[1], 9 * k, 8 * k), metal(hand[0] - 9 * k, hand[0] + 9 * k))
    # sword
    if sword == "up":
        bl = Poly([(hand[0] - 4 * k, hand[1] - 10 * k), (hand[0] + 4 * k, hand[1] - 10 * k), (hand[0] + 3 * k, hand[1] - 190 * k), (hand[0], hand[1] - 204 * k),
                   (hand[0] - 3 * k, hand[1] - 190 * k)])
        g.fill(bl, lgrad(hand[0] - 4 * k, 0, hand[0] + 4 * k, 0, [(0, (210, 214, 224)), (1, (100, 104, 114))]))
        g.fill(Box(hand[0] - 20 * k, hand[1] - 12 * k, hand[0] + 20 * k, hand[1] - 7 * k), (130, 104, 60))
        g.fill(Circ(hand[0], hand[1] + 12 * k, 4 * k), (130, 104, 60))
    elif sword == "down":
        g.fill(Poly([(hand[0] - 4 * k, hand[1] + 10 * k), (hand[0] + 4 * k, hand[1] + 10 * k), (hand[0] + 2 * k, sy(4)), (hand[0] - 2 * k, sy(4))]),
               lgrad(hand[0] - 4 * k, 0, hand[0] + 4 * k, 0, [(0, (200, 204, 214)), (1, (96, 100, 110))]))
        g.fill(Box(hand[0] - 20 * k, hand[1] + 6 * k, hand[0] + 20 * k, hand[1] + 11 * k), (130, 104, 60))
    # shield on the back arm
    if shield is not None:
        field, device = shield
        cx, cy = sx(-50), sy(hip + 70)
        sh = Union([Box(cx - 34 * k, cy - 46 * k, cx + 34 * k, cy), Inter(Circ(cx - 34 * k, cy, 68 * k), Circ(cx + 34 * k, cy, 68 * k)) & Box(cx - 34 * k, cy, cx + 34 * k, cy + 70 * k)])
        g.mul(Moved(sh, 5 * k, 4 * k), 0.4, feather=4 * k)
        g.fill(sh, tex(light_x(field, cx - 34 * k, cx + 34 * k, 1.3, 0.6), 0.15, 2, 3, 3, 73))
        g.fill(Diff(sh, Union([Box(cx - 30 * k, cy - 42 * k, cx + 30 * k, cy), Inter(Circ(cx - 30 * k, cy, 62 * k), Circ(cx + 30 * k, cy, 62 * k)) & Box(cx - 30 * k, cy, cx + 30 * k, cy + 64 * k)])),
               metal(cx - 34 * k, cx + 34 * k))
        if device is not None:
            device(g, cx, cy, 40 * k)
        rim(g, sh, rim_dx, 0, col=rim_col, k=rim_k)
    # gorget + helm
    hx, hy = sx(2), sy(top + 34)
    g.fill(Ell(sx(0), sy(top + 4), 22 * k, 10 * k), metal(sx(-22), sx(22)))
    if helm == "great":
        hs = Union([Box(hx - 20 * k, hy - 26 * k, hx + 20 * k, hy + 24 * k, 4 * k), Ell(hx, hy - 26 * k, 20 * k, 8 * k)])
        g.fill(hs, metal(hx - 20 * k, hx + 20 * k))
        g.fill(Box(hx - 18 * k, hy - 6 * k, hx + 18 * k, hy - 1 * k), (10, 10, 12))
        g.fill(Box(hx - 2 * k, hy - 1 * k, hx + 2 * k, hy + 20 * k), mixc(steel, (0, 0, 0), 0.45))
        for i in range(3):
            g.fill(Circ(hx + f * 8 * k, hy + (6 + i * 5) * k, 1.4 * k), (10, 10, 12))
    else:     # bascinet with a pointed visor
        hs = Union([Ell(hx, hy - 6 * k, 20 * k, 28 * k), Poly([(hx - 4 * k, hy - 34 * k), (hx, hy - 46 * k), (hx + 4 * k, hy - 34 * k)])])
        g.fill(hs, metal(hx - 20 * k, hx + 20 * k))
        g.fill(Poly([(hx + f * 4 * k, hy - 12 * k), (hx + f * 30 * k, hy + 2 * k), (hx + f * 6 * k, hy + 14 * k)]), metal(hx - 10 * k, hx + 30 * k))
        g.fill(Seg(hx + f * 8 * k, hy - 4 * k, hx + f * 22 * k, hy + 2 * k, 1.4 * k), (10, 10, 12))
    rim(g, hs, rim_dx, 0.5, col=rim_col, k=rim_k)
    if plume is not None:
        g.fill(Rough(Poly([(hx, hy - 30 * k), (hx - f * 20 * k, hy - 60 * k), (hx - f * 60 * k, hy - 50 * k), (hx - f * 30 * k, hy - 30 * k)]), 2 * k, 4 * k, 74),
               light_x(plume, hx - 60 * k, hx + 20 * k, 0.7, 1.2))
    return dict(head=(hx, hy), hand=hand, torso=torso)


def beast(g, x, base, h, fur=(40, 34, 32), face=-1, eyes=(255, 200, 90), rim_dx=-2.0, rim_col=MOON, rim_k=0.5, seed=0):
    """Hulking wolf-like beast standing hunched on its hind legs (dark furry silhouette, glowing eyes)."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    g.mul(Ell(x, base + 2, 90 * k, 10 * k), 0.5, feather=8 * k)
    body = Union([
        Ell(sx(-10), sy(170), 62 * k, 80 * k),                             # chest / back
        Ell(sx(20), sy(230), 44 * k, 40 * k),                              # shoulders
        Poly([(sx(-40), sy(120)), (sx(-60), sy(60)), (sx(-40), sy(4)), (sx(-20), sy(4)), (sx(-24), sy(60)), (sx(0), sy(110))]),   # back leg
        Poly([(sx(10), sy(110)), (sx(30), sy(60)), (sx(16), sy(4)), (sx(38), sy(4)), (sx(46), sy(64)), (sx(34), sy(120))]),       # front leg
        Seg(sx(40), sy(220), sx(84), sy(130), 16 * k, 11 * k), Seg(sx(84), sy(130), sx(96), sy(70), 11 * k, 9 * k),              # long arm
        Seg(sx(-30), sy(210), sx(-70), sy(140), 15 * k, 10 * k), Seg(sx(-70), sy(140), sx(-74), sy(80), 10 * k, 8 * k),           # back arm
        Ell(sx(56), sy(258), 26 * k, 20 * k),                              # head
        Poly([(sx(66), sy(262)), (sx(108), sy(246)), (sx(108), sy(236)), (sx(66), sy(240))]),                                     # snout
        Poly([(sx(40), sy(270)), (sx(36), sy(304)), (sx(54), sy(276))]), Poly([(sx(56), sy(272)), (sx(60), sy(306)), (sx(70), sy(272))]),  # ears
    ])
    sh = Rough(body, 4 * k, 6 * k, seed, 3)

    def fur_paint(X, Y):
        strands = 0.75 + 0.35 * fbm(X, Y, 1.6 * k + 0.6, 9 * k + 2, 3, seed + 1)
        return C(fur) * strands[..., None]
    g.fill(sh, fur_paint)
    for cx_, cy_ in ((sx(96), sy(66)), (sx(-74), sy(76))):
        for i in range(3):
            g.fill(Seg(cx_ + (i - 1) * 5 * k, cy_, cx_ + (i - 1) * 7 * k + f * 4 * k, cy_ + 14 * k, 2 * k, 0.6 * k), (200, 196, 180))
    rim(g, sh, rim_dx, 0, col=rim_col, k=rim_k)
    ex, ey = sx(70), sy(258)
    g.glow(ex, ey, 14 * k, eyes, 0.8)
    g.fill(Ell(ex, ey, 4 * k, 2.4 * k), eyes)
    return sh


def dragon(g, x, y, s, col=(30, 26, 28), face=-1, rim_dx=0.0, rim_col=(255, 170, 90), rim_k=0.0, wings_up=True, seed=0):
    """Dragon silhouette (original): long neck, horned head, membrane wings, curling tail. (x, y) = body centre."""
    f = face
    sx = lambda v: x + f * v * s
    sy = lambda v: y - v * s
    parts = [Ell(sx(0), sy(0), 60 * s, 30 * s),
             Seg(sx(40), sy(10), sx(90), sy(60), 16 * s, 10 * s), Seg(sx(90), sy(60), sx(120), sy(70), 10 * s, 9 * s),
             Ell(sx(132), sy(68), 18 * s, 10 * s), Poly([(sx(140), sy(72)), (sx(166), sy(62)), (sx(140), sy(60))]),
             Poly([(sx(124), sy(76)), (sx(104), sy(98)), (sx(130), sy(78))]),
             Seg(sx(-50), sy(-4), sx(-120), sy(-20), 14 * s, 8 * s), Seg(sx(-120), sy(-20), sx(-170), sy(10), 8 * s, 3 * s),
             Poly([(sx(-170), sy(10)), (sx(-186), sy(22)), (sx(-176), sy(2))]),
             Seg(sx(20), sy(-20), sx(30), sy(-56), 9 * s, 6 * s), Seg(sx(-30), sy(-20), sx(-26), sy(-58), 10 * s, 6 * s)]
    if wings_up:
        wing = Poly([(sx(-10), sy(20)), (sx(-30), sy(110)), (sx(-90), sy(150)), (sx(-70), sy(110)), (sx(-130), sy(120)),
                     (sx(-100), sy(80)), (sx(-150), sy(70)), (sx(-90), sy(40)), (sx(-40), sy(10))])
    else:
        wing = Poly([(sx(-10), sy(20)), (sx(-60), sy(60)), (sx(-150), sy(40)), (sx(-120), sy(20)), (sx(-160), sy(0)),
                     (sx(-110), sy(-6)), (sx(-40), sy(4))])
    body = Union(parts + [wing])
    g.fill(body, lambda X, Y: C(col) * (0.85 + 0.3 * fbm(X, Y, 4 * s, 4 * s, 3, seed))[..., None])
    for a, b in (((-30, 110), (-10, 20)), ((-130, 120), (-40, 20)), ((-150, 70), (-40, 14))) if wings_up else ():
        g.fill(Seg(sx(a[0]), sy(a[1]), sx(b[0]), sy(b[1]), 2 * s, 1 * s), mixc(col, (0, 0, 0), 0.4))
    if rim_k:
        rim(g, body, rim_dx, 0, col=rim_col, k=rim_k)
    return body


def sword_in_ground(g, x, base, h, steel=(130, 132, 140), rust=0.4):
    """A greatsword driven into the ground at a slight angle."""
    k = h / 100.0
    tip = (x + 4 * k, base + 4)
    hilt = (x - 6 * k, base - 80 * k)
    g.fill(Seg(tip[0], tip[1], hilt[0], hilt[1], 2 * k, 5 * k), lgrad(x - 6 * k, 0, x + 6 * k, 0, [(0, mixc(steel, (120, 70, 40), rust)), (1, (60, 50, 46))]))
    g.fill(Seg(hilt[0] - 14 * k, hilt[1] + 1 * k, hilt[0] + 14 * k, hilt[1] - 1 * k, 2.6 * k), (90, 76, 56))
    g.fill(Seg(hilt[0], hilt[1], hilt[0] - 1.6 * k, hilt[1] - 18 * k, 2.4 * k), (60, 44, 32))
    g.fill(Circ(hilt[0] - 1.8 * k, hilt[1] - 20 * k, 3 * k), (110, 92, 60))
