# -*- coding: utf-8 -*-
"""Ink-sketch axonometric levels: a high-angle camera looking down on blocky terrain, drawn like a ballpoint pen
sketch on paper (blue ink hatching whose density follows the light, cross-hatched cast shadows, wobbly outlines,
a few red-ink / blue-wash accents). Original scenes:
  Level1530 墨线崖庭 - a clifftop stone courtyard: terrace with a pavilion, stairs, water channel and bridge, pines
  Level1531 墨线渔港 - a fishing harbour: quay, warehouses, crane, piers, boats, breakwater lighthouse

Renderer (on top of real.Ctx):
  Iso.p(x, y, z)          world -> screen (azimuth 35 deg, elevation ~33 deg, orthographic)
  solid(g, iso, top, bot) convex solid from a top ring and a bottom ring (boxes, frusta, cylinders, hulls, roofs);
                          back faces culled, faces hatched by Lambert shade, outlines drawn as ink strokes
  shadow(...)             cast shadow of a prism on a plane (convex hull of footprint + shifted top), cross-hatched
Noise / jitter depend only on scene coordinates, so A / B and the measuring canvases render identically.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (F32, Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Union, el, fbm, real_post,
                  smooth, vnoise)

AZ = math.radians(35)
SA, CA = math.sin(AZ), math.cos(AZ)
KY, KZ = 0.55, 0.9
VIEW = np.array([KZ * SA, KZ * CA, KY])
VIEW /= np.linalg.norm(VIEW)
LIGHT = np.array([-0.9, 0.6, 0.9])
LIGHT /= np.linalg.norm(LIGHT)
SHADOW_DIR = (-LIGHT[0] / LIGHT[2], -LIGHT[1] / LIGHT[2])      # ground offset per unit of height

PAPER = (246, 245, 240)
INK = (34, 44, 140)
RED = (206, 56, 66)
WASH = (176, 210, 238)


def ink_post(rows, w, h, ox, oy, has_alpha):
    real_post(rows, w, h, ox, oy, has_alpha, grain=2.5, vignette=0.1)


OPTS = dict(post=ink_post, anim_seconds=12.0, frames=60)


class Iso:
    def __init__(self, ox, oy, u=20.0):
        self.ox, self.oy, self.u = ox, oy, u

    def p(self, x, y, z=0.0):
        return (self.ox + (x * CA - y * SA) * self.u, self.oy + (x * SA + y * CA) * KY * self.u - z * KZ * self.u)

    def poly(self, pts3):
        return Poly([self.p(*q) for q in pts3])


# =================================================================== ink primitives
def hatch(ang_deg, sp, w=0.2, seed=0, brk=0.22, jit=0.22, seg=16.0):
    """Alpha field of broken, slightly wavy parallel pen strokes."""
    a = math.radians(ang_deg)
    ca, sa = math.cos(a), math.sin(a)

    def f(X, Y):
        u = (X * ca + Y * sa) / sp
        v = (-X * sa + Y * ca)
        u = u + (fbm(X, Y, 26, 26, 2, seed) - 0.5) * jit * 2
        fr = np.abs(u - np.floor(u) - 0.5)
        line = smooth(w, w * 0.3, fr)
        n = vnoise(np.floor(u) * 3.17 + 0.5, v / seg, seed + 3)
        keep = smooth(brk, brk + 0.14, n)
        return line * keep * (0.72 + 0.28 * n)
    return f


def _jit(x, y, seed, amp):
    h = math.sin(x * 12.9898 + y * 78.233 + seed * 37.719) * 43758.5453
    return (h - math.floor(h) - 0.5) * 2 * amp


def ink_line(g, p0, p1, w=1.3, col=INK, seed=0, over=2.0, double=True):
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1.0
    ux, uy = dx / ln, dy / ln
    a = (x0 - ux * over + _jit(x0, y0, seed, 0.6), y0 - uy * over + _jit(y0, x0, seed, 0.6))
    b = (x1 + ux * over + _jit(x1, y1, seed + 1, 0.6), y1 + uy * over + _jit(y1, x1, seed + 1, 0.6))
    g.fill(Seg(a[0], a[1], b[0], b[1], w, w * 0.8), col)
    if double and ln > 18:
        o = _jit(x0 + x1, y0 + y1, seed + 2, 0.9)
        g.fill(Seg(a[0] - uy * o + ux * 3, a[1] + ux * o + uy * 3, b[0] - uy * o - ux * 5, b[1] + ux * o - uy * 5, w * 0.6), col,
               alpha=0.45)


def shade_fill(g, shape, dark, seed, vertical=True, base=PAPER, ang=None):
    """Paper (or base colour) + pen hatching whose density follows `dark` (0 lit .. 1 deep shade)."""
    g.fill(shape, base)
    if dark > 0.28:
        a0 = ang if ang is not None else ((96 + (seed % 7) - 3) if vertical else 28)
        sp = 5.6 if dark < 0.48 else (3.5 if dark < 0.72 else 2.9)
        hf = hatch(a0, sp, seed=seed)
        g.fill(shape, INK, alpha=lambda X, Y: hf(X, Y) * 0.85)
    if dark > 0.72:
        hf2 = hatch(38, 4.4, seed=seed + 11)
        g.fill(shape, INK, alpha=lambda X, Y: hf2(X, Y) * 0.6)


def _normal(pts):
    p = np.array(pts, float)
    n = np.zeros(3)
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        n += np.cross(a, b)
    ln = np.linalg.norm(n)
    return n / ln if ln > 1e-9 else n


def solid(g, iso, top, bot, seed=0, smooth_sides=False, top_base=PAPER, side_base=PAPER, top_dark=None,
          edges=True, w=1.3, extra_dark=0.0, top_paint=None):
    """Convex solid between ring `top` and ring `bot` (same vertex count, both counter-clockwise seen from above)."""
    n = len(top)
    cen = np.mean(np.array(top + bot, float), axis=0)
    faces = [("top", list(top))]
    for i in range(n):
        j = (i + 1) % n
        faces.append(("side%d" % i, [bot[i], bot[j], top[j], top[i]]))
    vis = {}
    for name, pts in faces:
        nn = _normal(pts)
        fc = np.mean(np.array(pts, float), axis=0)
        if np.dot(nn, fc - cen) < 0:
            nn = -nn
        if np.dot(nn, VIEW) > 1e-3:
            vis[name] = (pts, nn)
    order = sorted(vis.items(), key=lambda kv: np.dot(np.mean(np.array(kv[1][0], float), axis=0), VIEW))
    for name, (pts, nn) in order:
        shp = iso.poly(pts)
        dark = 1 - max(0.0, float(np.dot(nn, LIGHT))) + extra_dark
        if name == "top":
            if top_paint is not None:
                top_paint(g, shp)
                continue
            shade_fill(g, shp, (0.15 if dark < 0.45 else dark) if top_dark is None else top_dark, seed, vertical=False, base=top_base)
        else:
            shade_fill(g, shp, min(1.0, dark), seed + int(name[4:]) * 5, vertical=True, base=side_base)
    if not edges:
        return
    if "top" in vis:
        for i in range(n):
            ink_line(g, iso.p(*top[i]), iso.p(*top[(i + 1) % n]), w=w, seed=seed + i)
    for i in range(n):
        j = (i + 1) % n
        if ("side%d" % i) in vis:
            ink_line(g, iso.p(*bot[i]), iso.p(*bot[j]), w=w, seed=seed + 40 + i)
    for i in range(n):
        a_vis = ("side%d" % ((i - 1) % n)) in vis
        b_vis = ("side%d" % i) in vis
        if (a_vis != b_vis) or (a_vis and b_vis and not smooth_sides):
            ink_line(g, iso.p(*bot[i]), iso.p(*top[i]), w=w, seed=seed + 80 + i)


def box(g, iso, x0, y0, z0, x1, y1, z1, **kw):
    top = [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    bot = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]
    solid(g, iso, top, bot, **kw)


def cyl(g, iso, x, y, z0, z1, r, n=16, r1=None, **kw):
    r1 = r if r1 is None else r1
    top = [(x + r1 * math.cos(t), y + r1 * math.sin(t), z1) for t in np.linspace(0, math.tau, n, endpoint=False)]
    bot = [(x + r * math.cos(t), y + r * math.sin(t), z0) for t in np.linspace(0, math.tau, n, endpoint=False)]
    solid(g, iso, top, bot, smooth_sides=True, **kw)


def rockblock(g, iso, x, y, z0, sx, sy, h, seed, cham=0.25):
    """Chunky chamfered rock: octagonal top slightly smaller than the base."""
    rnd = random.Random(seed)
    c = cham
    ring = [(-1 + c, -1), (1 - c, -1), (1, -1 + c), (1, 1 - c), (1 - c, 1), (-1 + c, 1), (-1, 1 - c), (-1, -1 + c)]
    jt = [(rnd.uniform(-0.08, 0.08), rnd.uniform(-0.08, 0.08)) for _ in ring]
    bot = [(x + (u + a) * sx, y + (v + b) * sy, z0) for (u, v), (a, b) in zip(ring, jt)]
    top = [(x + (u * 0.86 + a) * sx, y + (v * 0.86 + b) * sy, z0 + h * rnd.uniform(0.92, 1.08)) for (u, v), (a, b) in zip(ring, jt)]
    solid(g, iso, top, bot, seed=seed)
    # a few crack strokes on the top
    for k in range(3):
        px, py = x + rnd.uniform(-0.5, 0.5) * sx, y + rnd.uniform(-0.5, 0.5) * sy
        a = iso.p(px, py, z0 + h)
        b = iso.p(px + rnd.uniform(-0.4, 0.4) * sx, py + rnd.uniform(-0.4, 0.4) * sy, z0 + h)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.9, 0.4), INK, alpha=0.7)


def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def shadow(g, iso, ring_xy, z_base, h, seed=0, clip=None, k=1.0):
    sx, sy = SHADOW_DIR
    pts = [(x, y) for x, y in ring_xy] + [(x + sx * h, y + sy * h) for x, y in ring_xy]
    hull = _hull([(round(a, 4), round(b, 4)) for a, b in pts])
    shp = Poly([iso.p(x, y, z_base) for x, y in hull])
    if clip is not None:
        shp = Inter(shp, clip)
    g.fill(shp, WASH, alpha=0.3 * k)
    h1, h2 = hatch(42, 3.0, seed=seed + 5), hatch(-18, 4.6, seed=seed + 6)
    g.fill(shp, INK, alpha=lambda X, Y: h1(X, Y) * 0.75 * k)
    g.fill(shp, INK, alpha=lambda X, Y: h2(X, Y) * 0.4 * k)


def rect_ring(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def water_fill(g, shape, seed=0):
    g.fill(shape, lambda X, Y: np.broadcast_to(C(WASH), X.shape + (3,)) * (0.9 + 0.14 * fbm(X, Y, 90, 50, 3, seed))[..., None])
    hf = hatch(-8, 7.0, w=0.12, seed=seed + 1, brk=0.55, seg=10)
    g.fill(shape, (70, 110, 190), alpha=lambda X, Y: hf(X, Y) * 0.55)


def pine(g, iso, x, y, z, h, seed=0, shadow_on=True, clip=None):
    bx, by = iso.p(x, y, z)
    s = h * KZ * iso.u
    if shadow_on:
        shadow(g, iso, [(x - 0.5, y - 0.5), (x + 0.5, y - 0.5), (x + 0.5, y + 0.5), (x - 0.5, y + 0.5)], z, h * 0.8, seed=seed, clip=clip, k=0.8)
    g.fill(Seg(bx, by, bx, by - s * 0.3, 4, 3), PAPER)
    ink_line(g, (bx - 2, by), (bx - 1.5, by - s * 0.3), w=1.1, seed=seed, double=False)
    ink_line(g, (bx + 2, by), (bx + 1.5, by - s * 0.3), w=1.1, seed=seed + 1, double=False)
    rnd = random.Random(seed)
    for t in range(4):
        y0 = by - s * (0.22 + t * 0.19)
        hw = s * (0.32 - t * 0.065)
        pts = [(bx - hw, y0)]
        for k in range(1, 6):
            pts.append((bx - hw + 2 * hw * k / 6, y0 + rnd.uniform(-3, 3) + (3 if k % 2 else 0)))
        pts += [(bx + hw, y0), (bx + hw * 0.15, y0 - s * 0.24), (bx, y0 - s * 0.27), (bx - hw * 0.15, y0 - s * 0.24)]
        shp = Poly(pts)
        g.fill(shp, PAPER)
        hf = hatch(60, 3.2, seed=seed + t)
        g.fill(shp, INK, alpha=lambda X, Y, bx=bx, hw=hw: hf(X, Y) * 0.85 * smooth(bx - hw * 0.4, bx + hw * 0.7, X))
        for i in range(len(pts)):
            ink_line(g, pts[i], pts[(i + 1) % len(pts)], w=1.1, seed=seed + t * 10 + i, over=1.0, double=False)


def figure(g, x, y, s=1.0, coat=PAPER, accent=None, pack=None, stick=False, seed=0, face=1):
    """Small original ink figure standing at screen point (x, y) (feet)."""
    h = 40 * s
    sh = Ell(x + 12 * s, y, 12 * s, 3 * s)
    g.fill(sh, INK, alpha=lambda X, Y: hatch(40, 2.6, seed=seed)(X, Y) * 0.8)
    for dx in (-3, 3):
        g.fill(Seg(x + dx * s, y, x + dx * s, y - h * 0.32, 2.6 * s), INK)
    body = Poly([(x - 7 * s, y - h * 0.3), (x + 7 * s, y - h * 0.3), (x + 6 * s, y - h * 0.72), (x - 6 * s, y - h * 0.72)])
    g.fill(body, coat)
    hf = hatch(95, 2.8, seed=seed + 1)
    g.fill(body, INK, alpha=lambda X, Y: hf(X, Y) * 0.8 * smooth(x - 2 * s, x + 6 * s, X))
    for i, (a, b) in enumerate(((0, 1), (1, 2), (2, 3), (3, 0))):
        ink_line(g, body.p[a], body.p[b], w=1.1, seed=seed + i, over=0.5, double=False)
    if pack is not None:
        pk = Box(x - face * 12 * s, y - h * 0.7, x - face * 5 * s, y - h * 0.38, 2)
        g.fill(pk, pack)
        g.fill(pk, INK, alpha=lambda X, Y: hatch(100, 3.0, seed=seed + 2)(X, Y) * 0.6)
        ink_line(g, (x - face * 12 * s, y - h * 0.7), (x - face * 12 * s, y - h * 0.38), w=1, seed=seed + 7, double=False)
    if accent is not None:
        g.fill(Box(x - 6 * s, y - h * 0.74, x + 6 * s, y - h * 0.66, 1.5), accent)
    g.fill(Circ(x, y - h * 0.82, 5.2 * s), PAPER)
    g.fill(Circ(x, y - h * 0.82, 5.2 * s) - Circ(x - 1.5 * s, y - h * 0.84, 4.6 * s), INK)
    g.fill(Ell(x, y - h * 0.92, 5.6 * s, 2.6 * s), INK)
    if stick:
        g.fill(Seg(x + face * 9 * s, y + 1, x + face * 8 * s, y - h * 0.8, 1.4), INK)


def bird_el(eid, x, y, s=7, speed=24, phase=0.0):
    from kit import drift_across

    def draw(g, m):
        g.fill(Seg(x - s, y - s * 0.3, x, y + s * 0.1, 1.4, 1.0), INK)
        g.fill(Seg(x, y + s * 0.1, x + s, y - s * 0.35, 1.0, 1.4), INK)
    return E(eid, el(draw), pivot=(x, y), anim=dict(drift_across(x - s, x + s, speed, start=phase), stretch=(0, 0.5), scaleSpeed=2.2,
                                                     bobAmplitude=(0, 5), bobSpeed=0.2))


def shimmer_el(eid, pts, phase=0.0):
    def draw(g, m):
        for x, y in pts:
            g.fill(Seg(x - 8, y, x + 8, y - 1, 1.4), (255, 255, 255))
            g.fill(Seg(x - 3, y + 4, x + 5, y + 3, 1.0), (255, 255, 255))
    return E(eid, el(draw), daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=0.5, phase=phase))


# =================================================================== Level 1530 clifftop stone courtyard
I30 = Iso(300, 70, 20.0)
X30, Y30, Z30 = 44, 30, -7


def l1530_bg(c, d):
    g = Ctx(c)
    iso = I30
    # water far below, then the plateau block with its two visible cliff faces
    water_fill(g, Box(-2, -2, W + 2, H + 2), seed=3001)
    plateau_top = iso.poly([(-30, -30, 0), (X30, -30, 0), (X30, Y30, 0), (-30, Y30, 0)])
    for name, pts in (("y", [(-30, Y30, 0), (X30, Y30, 0), (X30, Y30, Z30), (-30, Y30, Z30)]),
                      ("x", [(X30, -30, 0), (X30, Y30, 0), (X30, Y30, Z30), (X30, -30, Z30)])):
        shp = iso.poly(pts)
        shade_fill(g, shp, 0.62 if name == "y" else 0.95, 3002 if name == "y" else 3003)
        # vertical rock seams
        rnd = random.Random(3004 if name == "y" else 3005)
        for _ in range(60):
            t = rnd.random()
            if name == "y":
                px, py = -30 + t * (X30 + 30), Y30
                a, b = iso.p(px, py, -0.2), iso.p(px, py, Z30 * rnd.uniform(0.3, 0.9))
            else:
                px, py = X30, -30 + t * (Y30 + 30)
                a, b = iso.p(px, py, -0.2), iso.p(px, py, Z30 * rnd.uniform(0.3, 0.9))
            g.fill(Seg(a[0], a[1], b[0] + rnd.uniform(-2, 2), b[1], 1.0, 0.5), INK, alpha=0.8)
    g.fill(plateau_top, PAPER)
    ink_line(g, iso.p(-30, Y30, 0), iso.p(X30, Y30, 0), w=1.6, seed=3006)
    ink_line(g, iso.p(X30, -30, 0), iso.p(X30, Y30, 0), w=1.6, seed=3007)
    ink_line(g, iso.p(X30, Y30, 0), iso.p(X30, Y30, Z30), w=1.6, seed=3008)
    for (a, b) in ((iso.p(-30, Y30, Z30), iso.p(X30, Y30, Z30)), (iso.p(X30, -30, Z30), iso.p(X30, Y30, Z30))):
        g.fill(Seg(a[0], a[1] + 3, b[0], b[1] + 3, 3), (255, 255, 255), alpha=0.8)
    # boat on the water (bottom left; difference)
    if "boat" not in d:
        bx, by = 120, 556
        hull = Poly([(bx - 40, by - 8), (bx + 44, by - 14), (bx + 30, by + 4), (bx - 30, by + 8)])
        g.fill(hull, PAPER)
        g.fill(hull, INK, alpha=lambda X, Y: hatch(95, 3.0, seed=3010)(X, Y) * 0.8 * smooth(by - 10, by + 6, Y))
        for i in range(4):
            ink_line(g, hull.p[i], hull.p[(i + 1) % 4], w=1.2, seed=3011 + i, over=1, double=False)
        g.fill(Seg(bx + 2, by - 10, bx + 2, by - 66, 1.6), INK)
        sail = Poly([(bx + 4, by - 64), (bx + 40, by - 18), (bx + 4, by - 16)])
        g.fill(sail, RED, alpha=0.85)
        ink_line(g, (bx + 4, by - 64), (bx + 40, by - 18), w=1.0, seed=3015, double=False)
        g.fill(Seg(bx - 40, by + 12, bx + 40, by + 4, 1.2), (70, 110, 190), alpha=0.6)
    # rock outcrop (top left)
    for k, (x, y, sx, sy, h) in enumerate(((-9, 3, 2.6, 2.2, 3.4), (-5, -1, 2.4, 2.4, 5.0), (-4.5, 7.5, 2.2, 1.8, 2.2),
                                            (-1, 2.5, 1.8, 2.0, 2.8), (-8, 10, 1.6, 1.6, 1.6), (1, -3, 1.6, 1.4, 1.8))):
        if k == 3 and "rock" in d:
            continue
        shadow(g, iso, rect_ring(x - sx, y - sy, x + sx, y + sy), 0, h, seed=3020 + k)
        rockblock(g, iso, x, y, 0, sx, sy, h, seed=3030 + k)
    # pine behind the terrace (top right; difference)
    if "pine" not in d:
        pine(g, iso, 28, -6, 0, 5.0, seed=3040)
    pine(g, iso, 33, -1, 0, 4.0, seed=3041)
    # terrace with its shadow
    tx0, ty0, tx1, ty1, th = 4, -4, 22, 6, 3
    shadow(g, iso, rect_ring(tx0, ty0, tx1, ty1), 0, th, seed=3050)
    box(g, iso, tx0, ty0, 0, tx1, ty1, th, seed=3051, w=1.5)
    # flagstone joints on the terrace top
    for k in range(1, 6):
        a, b = iso.p(tx0 + k * 3, ty0, th), iso.p(tx0 + k * 3, ty1, th)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.8), INK, alpha=0.35)
    for k in range(1, 4):
        a, b = iso.p(tx0, ty0 + k * 2.5, th), iso.p(tx1, ty0 + k * 2.5, th)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.8), INK, alpha=0.35)
    # pavilion on the terrace: posts, roof, red paper lantern (difference)
    px0, py0, px1, py1 = 14, 0.5, 19, 4.5
    shadow(g, iso, rect_ring(px0, py0, px1, py1), th, 4.5, seed=3060,
           clip=iso.poly([(tx0, ty0, th), (tx1, ty0, th), (tx1, ty1, th), (tx0, ty1, th)]))
    box(g, iso, px0 - 0.3, py0 - 0.3, th, px1 + 0.3, py1 + 0.3, th + 0.4, seed=3061)
    for (x, y) in ((px0, py0), (px1, py0), (px1, py1), (px0, py1)):
        box(g, iso, x - 0.25, y - 0.25, th + 0.4, x + 0.25, y + 0.25, th + 3.2, seed=3062 + int(x * 3 + y), w=1.1)
    eave = 1.3
    rt = [((px0 + px1) / 2, (py0 + py1) / 2, th + 6.0)] * 4
    rb = [(px0 - eave, py0 - eave, th + 3.2), (px1 + eave, py0 - eave, th + 3.2), (px1 + eave, py1 + eave, th + 3.2), (px0 - eave, py1 + eave, th + 3.2)]
    solid(g, iso, rt, rb, seed=3066, w=1.4)
    tip = iso.p((px0 + px1) / 2, (py0 + py1) / 2, th + 6.0)
    g.fill(Seg(tip[0], tip[1], tip[0], tip[1] - 12, 1.6), INK)
    g.fill(Circ(tip[0], tip[1] - 13, 2.6), INK)
    if "lamp" not in d:
        lx, ly = iso.p(px1 + eave, py1 + eave, th + 3.2)
        g.fill(Seg(lx, ly, lx, ly + 8, 1.2), INK)
        g.fill(Ell(lx, ly + 22, 10, 14), RED)
        g.fill(Ell(lx, ly + 22, 10, 14) - Ell(lx - 2.5, ly + 21, 9, 13.5), INK)
        for yy in (ly + 14, ly + 22, ly + 30):
            g.fill(Seg(lx - 8, yy, lx + 8, yy, 0.8), INK, alpha=0.6)
        g.fill(Box(lx - 5, ly + 7, lx + 5, ly + 10), INK)
    # stairs down from the terrace front
    for k in range(3):
        box(g, iso, 8, ty1 + k * 1.0, 0, 12, ty1 + (k + 1) * 1.0, th * (3 - k) / 4, seed=3070 + k, w=1.1)
    # stone lanterns at the foot of the stairs (difference: left one)
    for k, (x, y) in enumerate(((6.5, 9.5), (13.5, 9.5))):
        if k == 0 and "lantern" in d:
            continue
        shadow(g, iso, rect_ring(x - 0.5, y - 0.5, x + 0.5, y + 0.5), 0, 2.6, seed=3080 + k)
        box(g, iso, x - 0.6, y - 0.6, 0, x + 0.6, y + 0.6, 0.4, seed=3081 + k, w=1.0)
        box(g, iso, x - 0.25, y - 0.25, 0.4, x + 0.25, y + 0.25, 1.6, seed=3082 + k, w=1.0)
        box(g, iso, x - 0.55, y - 0.55, 1.6, x + 0.55, y + 0.55, 2.3, seed=3083 + k, w=1.0)
        solid(g, iso, [(x, y, 3.0)] * 4, [(x - 0.8, y - 0.8, 2.3), (x + 0.8, y - 0.8, 2.3), (x + 0.8, y + 0.8, 2.3), (x - 0.8, y + 0.8, 2.3)], seed=3084 + k, w=1.0)
    # red banner on a pole (difference)
    if "banner" not in d:
        bx, by = iso.p(25, 8, 0)
        g.fill(Seg(bx, by, bx, by - 112, 2.2), INK)
        flag = Poly([(bx + 1, by - 108), (bx + 30, by - 104), (bx + 26, by - 66), (bx + 1, by - 70)])
        g.fill(flag, RED, alpha=0.9)
        for i in range(4):
            ink_line(g, flag.p[i], flag.p[(i + 1) % 4], w=1.0, seed=3091 + i, over=0.5, double=False)
    # water channel cut into the plateau, with a stone bridge
    cx0, cy0, cx1, cy1, cd = 0, 12.5, 36, 18, 1.6
    rim_ = iso.poly([(cx0, cy0, 0), (cx1, cy0, 0), (cx1, cy1, 0), (cx0, cy1, 0)])
    water_fill(g, Inter(iso.poly([(cx0, cy0, -cd), (cx1, cy0, -cd), (cx1, cy1, -cd), (cx0, cy1, -cd)]), rim_), seed=3100)
    wy = iso.poly([(cx0, cy0, 0), (cx1, cy0, 0), (cx1, cy0, -cd), (cx0, cy0, -cd)])
    shade_fill(g, Inter(wy, rim_), 0.6, 3101)
    wx = iso.poly([(cx0, cy0, 0), (cx0, cy1, 0), (cx0, cy1, -cd), (cx0, cy0, -cd)])
    shade_fill(g, Inter(wx, rim_), 0.95, 3102)
    sh_ = iso.poly([(cx0, cy0, -cd), (cx0 + cd * SHADOW_DIR[0], cy0, -cd), (cx0 + cd * SHADOW_DIR[0], cy1, -cd), (cx0, cy1, -cd)])
    g.fill(Inter(sh_, rim_), INK, alpha=lambda X, Y: hatch(42, 3.0, seed=3109)(X, Y) * 0.7)
    wl = -0.9
    water_fill(g, Inter(iso.poly([(cx0, cy0, wl), (cx1, cy0, wl), (cx1, cy1, wl), (cx0, cy1, wl)]), rim_), seed=3108)
    a_, b_ = iso.p(cx0, cy0, wl), iso.p(cx1, cy0, wl)
    g.fill(Seg(a_[0], a_[1], b_[0], b_[1], 1.0), (60, 100, 180), alpha=0.8)
    for a, b in (((cx0, cy0, 0), (cx1, cy0, 0)), ((cx1, cy0, 0), (cx1, cy1, 0)), ((cx1, cy1, 0), (cx0, cy1, 0)),
                 ((cx0, cy0, -cd), (cx1, cy0, -cd)), ((cx0, cy0, 0), (cx0, cy0, -cd)), ((cx0, cy1, 0), (cx0, cy0, 0))):
        ink_line(g, iso.p(*a), iso.p(*b), w=1.4, seed=int(a[0] * 7 + b[1] * 3))
    box(g, iso, 16, cy0 - 0.6, -0.6, 19, cy1 + 0.6, 0.2, seed=3104, w=1.3)
    for x in (16.2, 18.8):
        box(g, iso, x - 0.15, cy0 - 0.4, 0.2, x + 0.15, cy1 + 0.4, 0.9, seed=3105 + int(x), w=0.9)
    # well with a little roof (difference: roof)
    shadow(g, iso, rect_ring(24, 23, 26, 25), 0, 1.4, seed=3110)
    cyl(g, iso, 25, 24, 0, 1.2, 1.0, seed=3111, w=1.2)
    cx, cy = iso.p(25, 24, 1.2)
    g.fill(Ell(cx, cy, 13, 7), (50, 70, 140))
    if "well" not in d:
        for (x, y) in ((24.1, 23.1), (25.9, 24.9)):
            box(g, iso, x - 0.12, y - 0.12, 1.2, x + 0.12, y + 0.12, 3.2, seed=3112 + int(x), w=0.9)
        solid(g, iso, [(24.0, 24, 4.0), (26.0, 24, 4.0), (26.0, 24, 4.0), (24.0, 24, 4.0)],
              [(23.6, 22.6, 3.2), (26.4, 22.6, 3.2), (26.4, 25.4, 3.2), (23.6, 25.4, 3.2)], seed=3114, w=1.1)
    # traveller near the bridge (difference: red scarf -> plain)
    fx, fy = iso.p(17, 22, 0)
    figure(g, fx, fy, 1.1, accent=RED, pack=(236, 232, 220), stick=True, seed=3120)
    # handcart with a red cloth (difference)
    if "cart" not in d:
        shadow(g, iso, rect_ring(25, 9.5, 28, 11.5), 0, 1.4, seed=3150)
        box(g, iso, 25, 9.5, 0.6, 28, 11.5, 1.4, seed=3151, w=1.1)
        box(g, iso, 25.4, 9.9, 1.4, 27.6, 11.1, 2.0, seed=3152, w=1.0, top_base=RED, side_base=RED, top_dark=0.0)
        for wy_ in (9.4, 11.6):
            cx_, cy_ = iso.p(26.5, wy_, 0.6)
            g.fill(Ell(cx_, cy_, 8, 6), PAPER)
            g.fill(Ell(cx_, cy_, 8, 6) - Ell(cx_, cy_, 6.5, 4.6), INK)
        a_, b_ = iso.p(28, 10.5, 1.0), iso.p(30.5, 10.5, 0.7)
        g.fill(Seg(a_[0], a_[1], b_[0], b_[1], 1.6), INK)
    # hut near the cliff (bottom right) and a fence along the cliff edge
    shadow(g, iso, rect_ring(34, 19, 40, 25), 0, 5.0, seed=3160)
    box(g, iso, 34, 19, 0, 40, 25, 3.0, seed=3161, w=1.3)
    solid(g, iso, [(33.4, 22, 5.2), (40.6, 22, 5.2), (40.6, 22, 5.2), (33.4, 22, 5.2)],
          [(33.4, 18.4, 2.9), (40.6, 18.4, 2.9), (40.6, 25.6, 2.9), (33.4, 25.6, 2.9)], seed=3162, w=1.3)
    dx_, dy_ = iso.p(37, 25, 0)
    door = iso.poly([(36.2, 25, 0), (37.8, 25, 0), (37.8, 25, 2.0), (36.2, 25, 2.0)])
    g.fill(door, (60, 70, 140))
    for k in range(0, 17):
        x = 1 + k * 2.4
        box(g, iso, x - 0.12, 29.2, 0, x + 0.12, 29.45, 1.2, seed=3170 + k, w=0.8, edges=False)
        a_, b_ = iso.p(x, 29.3, 1.2), iso.p(x, 29.3, 0)
        ink_line(g, a_, b_, w=0.9, seed=3190 + k, over=0.5, double=False)
    for z in (0.5, 1.0):
        a_, b_ = iso.p(1, 29.3, z), iso.p(39.4, 29.3, z)
        ink_line(g, a_, b_, w=1.0, seed=3200 + int(z * 10))
    figure(g, *iso.p(10, 2, th), 0.85, seed=3121, face=-1)
    # pines (left / right) and scattered stones
    pine(g, iso, -2, 20, 0, 4.4, seed=3130)
    pine(g, iso, 37, 7, 0, 4.6, seed=3131)
    for k, (x, y) in enumerate(((26, 26), (12, 23), (34, 12), (3, 10))):
        rockblock(g, iso, x, y, 0, 0.6, 0.5, 0.6, seed=3140 + k)
    g.commit()


L1530_ELEMENTS = [
    bird_el("bird1", 600, 40, s=7, speed=-22),
    bird_el("bird2", 630, 54, s=6, speed=-22),
    shimmer_el("shimmer", [(80, 470), (220, 520), (40, 560), (860, 560), (300, 590), (430, 330)]),
]

def _sp(x, y, z=0.0):
    return tuple(round(v) for v in I30.p(x, y, z))


L1530_DIFFS = [
    ("rock", *_sp(-1, 2.5, 1.4), 0),
    ("pine", *_sp(28, -6, 2.6), 0),
    ("lamp", _sp(20.3, 5.8, 6.2)[0], _sp(20.3, 5.8, 6.2)[1] + 22, 0),
    ("lantern", *_sp(6.5, 9.5, 1.5), 0),
    ("banner", *_sp(25.6, 8, 4.4), 0),
    ("well", *_sp(25, 24, 3.0), 0),
    ("cart", *_sp(26.5, 10.5, 1.2), 0),
    ("boat", 130, 530, 0),
]


# =================================================================== Level 1531 fishing harbour
I31 = Iso(330, 60, 20.0)
QX = 22          # quay edge (x) - water beyond
QY = 34          # land ends at y = QY (bottom-left)
QZ = -3          # water level relative to the quay top


def gable(g, iso, x0, y0, x1, y1, z0, wall_h, roof_h, seed, along_x=True, over=0.5):
    box(g, iso, x0, y0, z0, x1, y1, z0 + wall_h, seed=seed, w=1.3)
    zt = z0 + wall_h
    if along_x:
        ym = (y0 + y1) / 2
        top = [(x0 - over, ym, zt + roof_h), (x1 + over, ym, zt + roof_h), (x1 + over, ym, zt + roof_h), (x0 - over, ym, zt + roof_h)]
    else:
        xm = (x0 + x1) / 2
        top = [(xm, y0 - over, zt + roof_h), (xm, y0 - over, zt + roof_h), (xm, y1 + over, zt + roof_h), (xm, y1 + over, zt + roof_h)]
    bot = [(x0 - over, y0 - over, zt), (x1 + over, y0 - over, zt), (x1 + over, y1 + over, zt), (x0 - over, y1 + over, zt)]
    solid(g, iso, top, bot, seed=seed + 1, w=1.3)


def pier(g, iso, x0, y0, x1, y1, seed):
    zt, zb = 0.0, -0.6
    shadow(g, iso, rect_ring(x0, y0, x1, y1), QZ, -QZ - 0.3, seed=seed, k=0.7)
    for x in np.arange(x0 + 1.0, x1, 3.0):
        for y in (y0 + 0.3, y1 - 0.3):
            cyl(g, iso, x, y, QZ, zb, 0.25, n=8, seed=seed + int(x * 3 + y), w=0.9)
    box(g, iso, x0, y0, zb, x1, y1, zt, seed=seed + 1, w=1.2)
    for k in range(1, int((x1 - x0) / 0.8)):
        a, b = iso.p(x0 + k * 0.8, y0, zt), iso.p(x0 + k * 0.8, y1, zt)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.7), INK, alpha=0.45)


def hull(g, iso, x0, y0, x1, y1, seed, deck=0.4, keel=-0.7, bow=1.8, col=PAPER):
    ym = (y0 + y1) / 2
    top = [(x0, y0, QZ + deck + 0.4), (x1, y0, QZ + deck), (x1 + bow, ym, QZ + deck + 0.5), (x1, y1, QZ + deck), (x0, y1, QZ + deck + 0.4)]
    bot = [(x0 + 0.4, y0 + 0.4, QZ + keel), (x1, y0 + 0.4, QZ + keel), (x1 + bow * 0.6, ym, QZ + keel), (x1, y1 - 0.4, QZ + keel), (x0 + 0.4, y1 - 0.4, QZ + keel)]
    shadow(g, iso, [(x0, y0), (x1, y0), (x1 + bow, ym), (x1, y1), (x0, y1)], QZ, 0.8, seed=seed, k=0.6)
    solid(g, iso, top, bot, seed=seed + 1, side_base=col, w=1.3)


def l1531_bg(c, d):
    g = Ctx(c)
    iso = I31
    water_fill(g, Box(-2, -2, W + 2, H + 2), seed=3201)
    # land block with the quay wall (+x face) and the shore wall (+y face)
    for name, pts, dk in (("y", [(-40, QY, 0), (QX, QY, 0), (QX, QY, QZ), (-40, QY, QZ)], 0.62),
                          ("x", [(QX, -40, 0), (QX, QY, 0), (QX, QY, QZ), (QX, -40, QZ)], 0.95)):
        shp = iso.poly(pts)
        shade_fill(g, shp, dk, 3202 if name == "y" else 3203)
        rnd = random.Random(3204 if name == "y" else 3205)
        for k in range(70):               # ashlar joints of the quay wall
            t = rnd.random()
            zz = rnd.choice((-1.0, -2.0))
            if name == "x":
                a, b = iso.p(QX, -40 + t * 74, zz), iso.p(QX, -40 + t * 74 + 2.2, zz)
                c_, d_ = iso.p(QX, -40 + t * 74, zz), iso.p(QX, -40 + t * 74, zz + 1)
            else:
                a, b = iso.p(-40 + t * 62, QY, zz), iso.p(-40 + t * 62 + 2.2, QY, zz)
                c_, d_ = iso.p(-40 + t * 62, QY, zz), iso.p(-40 + t * 62, QY, zz + 1)
            g.fill(Seg(a[0], a[1], b[0], b[1], 0.8), INK, alpha=0.6)
            g.fill(Seg(c_[0], c_[1], d_[0], d_[1], 0.8), INK, alpha=0.6)
    g.fill(iso.poly([(-40, -40, 0), (QX, -40, 0), (QX, QY, 0), (-40, QY, 0)]), PAPER)
    for a, b in (((QX, -40, 0), (QX, QY, 0)), ((-40, QY, 0), (QX, QY, 0)), ((QX, QY, 0), (QX, QY, QZ))):
        ink_line(g, iso.p(*a), iso.p(*b), w=1.6, seed=int(a[1] + b[0]))
    # cobble joints on the quay
    for k in range(-6, 12):
        a, b = iso.p(QX - 1.2, k * 3, 0), iso.p(QX - 1.2, k * 3 + 2.6, 0)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.8), INK, alpha=0.4)
    # piers
    pier(g, iso, QX, 3.5, 31, 6.5, 3220)
    pier(g, iso, QX, 18, 30, 21, 3221)
    # fishing boat beside pier 1 with a cabin (difference: red roof -> plain)
    hull(g, iso, 23.5, 8.0, 30.5, 11.5, 3230)
    box(g, iso, 24.5, 8.7, QZ + 0.8, 27.0, 10.8, QZ + 2.6, seed=3232, w=1.1)
    rc = RED if "cabin" not in d else PAPER
    box(g, iso, 24.2, 8.4, QZ + 2.6, 27.3, 11.1, QZ + 2.95, seed=3233, w=1.1, top_base=rc, side_base=rc, top_dark=0.0 if rc == RED else None)
    a, b = iso.p(28.5, 9.75, QZ + 0.8), iso.p(28.5, 9.75, QZ + 6.5)
    g.fill(Seg(a[0], a[1], b[0], b[1], 1.6), INK)
    c_ = iso.p(31.8, 9.75, QZ + 1.0)
    g.fill(Seg(b[0], b[1], c_[0], c_[1], 0.8), INK)
    # rowboat by pier 2 (difference)
    if "rowboat" not in d:
        hull(g, iso, 24.0, 22.6, 27.4, 24.4, 3240, deck=0.3, keel=-0.4, bow=1.0)
        a, b = iso.p(24.6, 23.0, QZ + 0.5), iso.p(27.6, 25.6, QZ + 0.2)
        g.fill(Seg(a[0], a[1], b[0], b[1], 1.3), INK)
    # breakwater with a lighthouse (red flag = difference)
    bw = (34, 5, 37, 34)
    shadow(g, iso, rect_ring(*bw), QZ, 0.6 - QZ, seed=3210, k=0.6)
    box(g, iso, bw[0], bw[1], QZ, bw[2], bw[3], 0.6, seed=3211, w=1.3)
    for k in range(1, 10):
        a, b = iso.p(bw[0], bw[1] + k * 3, 0.6), iso.p(bw[2], bw[1] + k * 3, 0.6)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.8), INK, alpha=0.4)
    lx, ly = 35.5, 7.0
    shadow(g, iso, rect_ring(lx - 1, ly - 1, lx + 1, ly + 1), 0.6, 7.5, seed=3212,
           clip=iso.poly([(bw[0], bw[1], 0.6), (bw[2], bw[1], 0.6), (bw[2], bw[3], 0.6), (bw[0], bw[3], 0.6)]))
    cyl(g, iso, lx, ly, 0.6, 7.0, 1.2, r1=0.85, seed=3213, w=1.3)
    for zb in (2.4, 4.6):
        rr = 1.2 - (zb / 7.0) * 0.35
        cyl(g, iso, lx, ly, zb, zb + 0.8, rr, r1=rr - 0.04, seed=3218 + int(zb), w=1.0, side_base=RED, top_dark=0.0, edges=True)
    cyl(g, iso, lx, ly, 7.0, 8.2, 0.75, seed=3214, w=1.1, top_dark=0.0)
    solid(g, iso, [(lx, ly, 9.4)] * 4, [(lx - 1.1, ly - 1.1, 8.2), (lx + 1.1, ly - 1.1, 8.2), (lx + 1.1, ly + 1.1, 8.2), (lx - 1.1, ly + 1.1, 8.2)], seed=3215, w=1.1)
    tip = iso.p(lx, ly, 9.4)
    g.fill(Seg(tip[0], tip[1], tip[0], tip[1] - 28, 1.6), INK)
    if "flag" not in d:
        fl = Poly([(tip[0] + 1, tip[1] - 26), (tip[0] + 34, tip[1] - 19), (tip[0] + 1, tip[1] - 6)])
        g.fill(fl, RED, alpha=0.9)
        ink_line(g, fl.p[0], fl.p[1], w=0.9, seed=3216, over=0.5, double=False)
        ink_line(g, fl.p[1], fl.p[2], w=0.9, seed=3217, over=0.5, double=False)
    # warehouses
    shadow(g, iso, rect_ring(2, -14, 13, -5), 0, 6.5, seed=3250)
    gable(g, iso, 2, -14, 13, -5, 0, 4.0, 2.6, 3251, along_x=True)
    a, b = iso.p(7.5, -5, 0), iso.p(7.5, -5, 2.6)
    g.fill(iso.poly([(6, -5, 0), (9, -5, 0), (9, -5, 2.6), (6, -5, 2.6)]), (60, 70, 140))
    shadow(g, iso, rect_ring(1, 3, 9, 11), 0, 5.5, seed=3252)
    gable(g, iso, 1, 3, 9, 11, 0, 3.4, 2.2, 3253, along_x=False)
    for wy in (5, 8.5):
        g.fill(iso.poly([(9, wy, 1.4), (9, wy + 1.4, 1.4), (9, wy + 1.4, 2.5), (9, wy, 2.5)]), (60, 70, 140))
    # crane on the quay (difference: hanging crate)
    shadow(g, iso, rect_ring(17.5, -3, 20, -0.5), 0, 8, seed=3260)
    box(g, iso, 17.5, -3, 0, 20, -0.5, 1.4, seed=3261, w=1.2)
    box(g, iso, 18.4, -2.1, 1.4, 19.1, -1.4, 8.5, seed=3262, w=1.1)
    tipc, endc = iso.p(18.75, -1.75, 8.5), iso.p(25.5, -1.75, 7.8)
    g.fill(Seg(tipc[0], tipc[1], endc[0], endc[1], 4), PAPER)
    ink_line(g, (tipc[0], tipc[1] - 2), (endc[0], endc[1] - 2), w=1.2, seed=3263)
    ink_line(g, (tipc[0], tipc[1] + 2), (endc[0], endc[1] + 2), w=1.2, seed=3264)
    g.fill(Seg(endc[0], endc[1], endc[0], endc[1] + 70, 1.0), INK)
    if "cargo" not in d:
        box(g, iso, 24.6, -2.6, 3.0, 26.4, -0.9, 4.4, seed=3265, w=1.1)
    # crate stack (difference: top crate), barrels, red nets (difference: colour), lamp posts (difference)
    for k, (x, y, z) in enumerate(((14, 8, 0), (16, 8, 0), (14, 10, 0), (16, 10, 0), (15, 9, 1.6))):
        if k == 4 and "crate" in d:
            continue
        if k == 0:
            shadow(g, iso, rect_ring(14, 8, 18, 12), 0, 3.2, seed=3270)
        box(g, iso, x, y, z, x + 1.9, y + 1.9, z + 1.6, seed=3271 + k, w=1.1)
    for k, (x, y) in enumerate(((15, 15), (16.4, 15.4), (15.5, 16.8))):
        shadow(g, iso, rect_ring(x - 0.6, y - 0.6, x + 0.6, y + 0.6), 0, 1.6, seed=3280 + k)
        cyl(g, iso, x, y, 0, 1.6, 0.6, seed=3283 + k, w=1.0)
    nc = RED if "net" not in d else (70, 120, 200)
    nx_, ny_ = iso.p(10, 22, 0)
    netp = Rough(Ell(nx_, ny_ - 6, 34, 14) - Box(nx_ - 40, ny_, nx_ + 40, ny_ + 20), 3, 6, 3290)
    g.fill(netp, nc, alpha=0.85)
    g.fill(netp, INK, alpha=lambda X, Y: np.clip(hatch(45, 4, seed=3291)(X, Y) + hatch(-45, 4, seed=3292)(X, Y), 0, 1) * 0.7)
    g.fill(Diff(netp, Moved(netp, -1.2, 1.2)), INK)
    # small house, market stall with a striped awning, fish-drying racks (fill the open quay)
    shadow(g, iso, rect_ring(-9, -3, -3, 3), 0, 5.0, seed=3320)
    gable(g, iso, -9, -3, -3, 3, 0, 3.0, 2.0, 3321, along_x=False)
    g.fill(iso.poly([(-3, -1, 0), (-3, 0.6, 0), (-3, 0.6, 2.0), (-3, -1, 2.0)]), (60, 70, 140))
    shadow(g, iso, rect_ring(-4, 13, 1, 16), 0, 2.6, seed=3322)
    box(g, iso, -4, 13, 0, 1, 16, 1.2, seed=3323, w=1.2)
    for (x, y) in ((-4, 13), (1, 13), (1, 16), (-4, 16)):
        a, b = iso.p(x, y, 1.2), iso.p(x, y, 3.0)
        g.fill(Seg(a[0], a[1], b[0], b[1], 1.4), INK)
    aw = [(-4.4, 12.6, 3.0), (1.4, 12.6, 3.0), (1.4, 16.4, 2.6), (-4.4, 16.4, 2.6)]
    g.fill(iso.poly(aw), PAPER)
    for k in range(6):
        if k % 2 == 0:
            x0_ = -4.4 + k * 0.97
            g.fill(iso.poly([(x0_, 12.6, 3.0), (x0_ + 0.97, 12.6, 3.0), (x0_ + 0.97, 16.4, 2.6), (x0_, 16.4, 2.6)]), RED, alpha=0.85)
    for i in range(4):
        ink_line(g, iso.p(*aw[i]), iso.p(*aw[(i + 1) % 4]), w=1.2, seed=3324 + i)
    for k, x in enumerate((-2.8, -1.4, 0.0)):
        cx_, cy_ = iso.p(x, 14.5, 1.2)
        g.fill(Ell(cx_, cy_ - 2, 7, 3), (200, 210, 230))
        g.fill(Ell(cx_, cy_ - 2, 7, 3) - Ell(cx_, cy_ - 3, 6, 2.5), INK)
    for k, y in enumerate((24, 28)):
        for x in (-6, 2):
            a, b = iso.p(x, y, 0), iso.p(x, y, 2.6)
            g.fill(Seg(a[0], a[1], b[0], b[1], 1.6), INK)
        a, b = iso.p(-6, y, 2.4), iso.p(2, y, 2.4)
        ink_line(g, a, b, w=1.0, seed=3330 + k)
        for j in range(9):
            fx_ = -5.4 + j * 0.85
            p = iso.p(fx_, y, 2.4)
            g.fill(Ell(p[0], p[1] + 8, 2.6, 7), PAPER)
            g.fill(Ell(p[0], p[1] + 8, 2.6, 7) - Ell(p[0] - 0.8, p[1] + 7.5, 2.0, 6.2), INK)
            g.fill(Poly([(p[0] - 3, p[1] + 16), (p[0], p[1] + 13), (p[0] + 3, p[1] + 16)]), INK)
        shadow(g, iso, [(-6, y - 0.05), (2, y - 0.05), (2, y + 0.05), (-6, y + 0.05)], 0, 2.4, seed=3335 + k, k=0.5)
    for k, y in enumerate((-13, 6, 24)):
        if k == 1 and "lamp" in d:
            continue
        x = QX - 0.6
        shadow(g, iso, rect_ring(x - 0.1, y - 0.1, x + 0.1, y + 0.1), 0, 4.5, seed=3295 + k, k=0.6)
        a, b = iso.p(x, y, 0), iso.p(x, y, 4.5)
        g.fill(Seg(a[0], a[1], b[0], b[1], 2.0), INK)
        g.fill(Poly([(b[0] - 5, b[1]), (b[0] + 5, b[1]), (b[0] + 3, b[1] - 9), (b[0] - 3, b[1] - 9)]), (250, 240, 200))
        for i, (p0, p1) in enumerate((((b[0] - 5, b[1]), (b[0] - 3, b[1] - 9)), ((b[0] + 5, b[1]), (b[0] + 3, b[1] - 9)))):
            ink_line(g, p0, p1, w=1.0, seed=3297 + k * 3 + i, over=0.5, double=False)
        g.fill(Poly([(b[0] - 6, b[1] - 9), (b[0], b[1] - 14), (b[0] + 6, b[1] - 9)]), INK)
    # people: fisherman mending nets, a worker by the crates
    figure(g, *iso.p(13, 19, 0), 1.0, seed=3300, face=-1)
    figure(g, *iso.p(19, 13, 0), 1.0, accent=RED, seed=3301)
    figure(g, *iso.p(28, 5, 0), 0.9, seed=3302)
    # bollards on the quay edge
    for y in (1, 14, 28):
        cyl(g, iso, QX - 0.5, y, 0, 0.7, 0.3, n=10, seed=3310 + y, w=0.9)
    g.commit()


def _sp31(x, y, z=0.0):
    return tuple(round(v) for v in I31.p(x, y, z))


L1531_ELEMENTS = [
    bird_el("gull1", 500, 60, s=8, speed=24),
    bird_el("gull2", 540, 80, s=6, speed=24),
    shimmer_el("shimmer", [(760, 260), (640, 470), (860, 420), (480, 560), (700, 330), (80, 560)]),
    E("smoke", el(lambda g, m: [g.fill(Circ(x, y, r) - Circ(x - 1, y - 1, r - 1.4), INK, alpha=0.7) for x, y, r in
                                ((150, 40, 6), (160, 30, 8), (174, 18, 9))]),
      anim=dict(driftVelocity=(8, 30), driftLength=60, driftFade=True)),
]

L1531_DIFFS = [
    ("flag", _sp31(35.5, 7, 9.4)[0] + 11, _sp31(35.5, 7, 9.4)[1] - 15, 0),
    ("cabin", *_sp31(25.75, 9.75, QZ + 2.8), 0),
    ("rowboat", *_sp31(25.7, 23.5, QZ), 0),
    ("cargo", *_sp31(25.5, -1.75, 3.7), 0),
    ("crate", *_sp31(16, 10, 2.4), 0),
    ("net", _sp31(10, 22)[0], _sp31(10, 22)[1] - 8, 0),
    ("lamp", *_sp31(QX - 0.6, 6, 4.0), 0),
]


LEVELS = [
    ("Level1530", "墨线崖庭", l1530_bg, L1530_ELEMENTS, L1530_DIFFS, 60, OPTS),
    ("Level1531", "墨线渔港", l1531_bg, L1531_ELEMENTS, L1531_DIFFS, 60, OPTS),
]
