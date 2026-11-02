# -*- coding: utf-8 -*-
"""Pencil-sketch levels (graphite on paper):
  45-degree 3D view (camera looks north, tilted down 45 deg - the project's "45° pseudo-3D top-down" view):
    Level1538 素描·老街       a village street: houses, market stalls, well, canal with a boat
    Level1539 素描·庭院       a formal courtyard garden: fountain, hedges, gazebo, statues, pond
  plain 2D view:
    Level1540 素描·火车站台   a side view of a station platform with a steam locomotive
    Level1541 素描·书房       a study corner: window, bookshelf, desk with lamp, globe, armchair

Rendering: warm paper with grain, smudged graphite tone + pencil hatching (cross-hatching in deep shade), wobbly
double-stroke outlines with overshoot, hatched cast shadows.  The 45-degree levels reuse the geometry kit of
levels_isostyle with an oblique camera (Obl) and the Sketch style; the 2D levels use sk() / outline() directly.
Greyscale only, so the differences are objects added / removed or changed in shape, not recoloured.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (F32, Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Shape, Union, el, fbm, real_post,
                  smooth)
from levels_inkiso import hatch
import levels_isostyle as K

PAPER = (244, 240, 230)
LEAD = (58, 58, 66)


# =================================================================== pencil primitives
class Outline(Shape):
    """Wobbly stroke along the boundary of a shape (sdf band)."""

    def __init__(self, s, w=1.1, wob=0.7, seed=0, off=0.0):
        self.s, self.w, self.wob, self.seed, self.off = s, w, wob, seed, off

    def bbox(self):
        b = self.s.bbox()
        p = self.w + self.wob + abs(self.off) + 1
        return (b[0] - p, b[1] - p, b[2] + p, b[3] + p)

    def sdf(self, X, Y):
        d = self.s.sdf(X, Y) + (fbm(X, Y, 16, 16, 2, self.seed) - 0.5) * 2 * self.wob + self.off
        return np.abs(d) - self.w / 2


def pressure(seed, lo=0.45, hi=0.95):
    return lambda X, Y: lo + (hi - lo) * fbm(X, Y, 40, 40, 2, seed)


def outline(g, shape, seed=0, w=1.1, k=1.0):
    g.fill(Outline(shape, w, 0.6, seed), LEAD, alpha=lambda X, Y: pressure(seed)(X, Y) * k)
    g.fill(Outline(shape, w * 0.6, 0.9, seed + 7, off=0.8), LEAD, alpha=lambda X, Y: pressure(seed + 1, 0.1, 0.5)(X, Y) * k)


def tone(g, shape, t, seed=0, ang=45, grad=None, cross=True, smudge=True):
    """Graphite tone t (0 white .. 1 black): smudge + hatching. grad=(x0, x1, dt) adds dt towards x1."""
    if t <= 0.02 and grad is None:
        return
    if grad is not None:
        x0, x1, dt = grad
        tf = lambda X, Y: np.clip(t + dt * smooth(x0, x1, X), 0, 1)
    else:
        tf = lambda X, Y: np.full(X.shape, t, F32)
    if smudge:
        g.fill(shape, LEAD, alpha=lambda X, Y: tf(X, Y) * 0.26 * (0.8 + 0.35 * fbm(X, Y, 40, 40, 3, seed)))
    h1 = hatch(ang, 3.2, w=0.18, seed=seed, brk=0.1, seg=46)
    g.fill(shape, LEAD, alpha=lambda X, Y: h1(X, Y) * smooth(0.18, 0.5, tf(X, Y)) * 0.7)
    if cross:
        h2 = hatch(ang - 70, 3.8, w=0.16, seed=seed + 3, brk=0.12, seg=46)
        g.fill(shape, LEAD, alpha=lambda X, Y: h2(X, Y) * smooth(0.5, 0.8, tf(X, Y)) * 0.6)


def sk(g, shape, t=0.2, seed=0, ang=45, grad=None, base=PAPER, line=True, w=1.1):
    """A sketched object: paper base, tone, outline."""
    g.fill(shape, base)
    tone(g, shape, t, seed, ang, grad)
    if line:
        outline(g, shape, seed + 11, w)


def line(g, x0, y0, x1, y1, seed=0, w=1.1, k=0.8, over=3.0):
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln
    rnd = random.Random(seed)
    j = lambda: rnd.uniform(-0.7, 0.7)
    g.fill(Seg(x0 - ux * over + j(), y0 - uy * over + j(), x1 + ux * over + j(), y1 + uy * over + j(), w, w * 0.7), LEAD, alpha=k)
    if ln > 20:
        o = rnd.uniform(-1.2, 1.2)
        g.fill(Seg(x0 - uy * o + ux * 4, y0 + ux * o + uy * 4, x1 - uy * o - ux * 6, y1 + ux * o - uy * 6, w * 0.6), LEAD, alpha=k * 0.4)


def paper(g, seed=0):
    g.fill(Box(-2, -2, W + 2, H + 2), lambda X, Y: np.broadcast_to(C(PAPER), X.shape + (3,)) *
           (0.965 + 0.05 * fbm(X, Y, 3, 3, 2, seed) + 0.02 * fbm(X, Y, 120, 90, 2, seed + 1))[..., None])


def finish(g):
    g.grade(contrast=1.04, sat=0.6)


def sketch_post(rows, w, h, ox, oy, has_alpha):
    real_post(rows, w, h, ox, oy, has_alpha, grain=3.0, vignette=0.14)


OPTS = dict(post=sketch_post, anim_seconds=12.0, frames=60)


# =================================================================== Sketch style for the 3D kit
class Sketch:
    name = "sketch"
    ink = LEAD

    def face(self, g, shp, col, v, kind, seed, ang=0.0, bot=None, top=False):
        lum = (0.3 * col[0] + 0.55 * col[1] + 0.15 * col[2]) / 255.0
        t = np.clip((1 - v) * 0.55 + (1 - lum) * 0.45, 0, 1)
        g.fill(shp, PAPER)
        a = 25 if top else 75
        tone(g, shp, float(t), seed, ang=a)
        ca, sa = math.cos(ang), math.sin(ang)
        if kind in ("roof", "wood"):
            sp = 4.5 if kind == "roof" else 3.6
            g.fill(shp, LEAD, alpha=lambda X, Y: smooth(0.1, 0.0, np.abs(((-X * sa + Y * ca) / sp) % 1.0 - 0.5) - 0.42) * 0.45)
        elif kind == "stone":
            g.fill(shp, LEAD, alpha=lambda X, Y: smooth(0.12, 0.0, np.abs(np.sin(fbm(X, Y, 7, 5, 2, seed) * 14))) * 0.45)
        elif kind == "foliage":
            h3 = hatch(130, 2.8, seed=seed + 5)
            g.fill(shp, LEAD, alpha=lambda X, Y: h3(X, Y) * 0.5 * smooth(0.4, 0.7, fbm(X, Y, 5, 5, 3, seed)))
        elif kind == "glass":
            g.fill(shp, LEAD, alpha=0.25)

    def edge(self, g, p0, p1, sil=True, w=1.0):
        line(g, p0[0], p0[1], p1[0], p1[1], seed=int(p0[0] * 7 + p1[1] * 3), w=(1.2 if sil else 0.8) * w, k=0.85 if sil else 0.55, over=2.5 if sil else 1.0)

    def shadow(self, g, shp, k=1.0):
        g.fill(shp, LEAD, alpha=lambda X, Y: 0.18 * k * (0.7 + 0.6 * fbm(X, Y, 20, 20, 2, 9)))
        h = hatch(40, 2.8, seed=5)
        g.fill(shp, LEAD, alpha=lambda X, Y: h(X, Y) * 0.6 * k)

    def ground(self, g, shp, col, kind, seed):
        if kind == "water":
            hf = hatch(-2, 6.0, w=0.12, seed=seed, brk=0.55, seg=10)
            g.fill(shp, LEAD, alpha=lambda X, Y: 0.1 + hf(X, Y) * 0.55)
            return
        if kind == "road":          # cobbles
            def cob(X, Y):
                n = fbm(X, Y, 5, 4, 2, seed)
                return smooth(0.1, 0.0, np.abs(np.sin(n * 22)) - 0.12) * 0.55
            g.fill(shp, LEAD, alpha=cob)
            g.fill(shp, LEAD, alpha=lambda X, Y: 0.08 * fbm(X, Y, 30, 30, 2, seed + 1))
            return
        if kind == "grass":
            rnd = random.Random(seed)
            b = shp.bbox()
            n = int((b[2] - b[0]) * (b[3] - b[1]) / 900)
            ticks = []
            for _ in range(min(n, 500)):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                ticks += [Seg(x, y, x - 1.5, y - 5, 0.8), Seg(x + 2, y, x + 2.5, y - 6, 0.8)]
            if ticks:
                g.fill(Inter(Union(ticks), shp), LEAD, alpha=0.55)
            g.fill(shp, LEAD, alpha=lambda X, Y: 0.06 * fbm(X, Y, 40, 40, 2, seed))
            return
        if kind == "dirt":           # gravel
            g.fill(shp, PAPER)
            g.fill(shp, LEAD, alpha=lambda X, Y: 0.1 + 0.35 * smooth(0.62, 0.7, fbm(X, Y, 1.6, 1.6, 2, seed)))
            return
        t = (1 - (0.3 * col[0] + 0.55 * col[1] + 0.15 * col[2]) / 255.0) * 0.6
        tone(g, shp, t, seed, ang=20, cross=False)

    def blob(self, g, cx, cy, rx, ry, col, seed, kind="foliage"):
        shape = Rough(Ell(cx, cy, rx, ry), rx * 0.14, rx * 0.3, seed, 3) if kind == "foliage" else Ell(cx, cy, rx, ry)
        g.fill(shape, PAPER)
        tone(g, shape, 0.25, seed, ang=60, grad=(cx - rx * 0.3, cx + rx, 0.55))
        if kind == "foliage":
            rnd = random.Random(seed)
            arcs = []
            for _ in range(int(rx * ry / 18)):
                a, r = rnd.uniform(0, math.tau), rnd.random() ** 0.6
                x, y = cx + math.cos(a) * rx * 0.85 * r, cy + math.sin(a) * ry * 0.85 * r
                arcs.append(Outline(Ell(x, y, 3.2, 2.4), 0.7, 0.2, seed) & Box(x - 4, y - 3, x + 4, y + 0.5))
            if arcs:
                g.fill(Inter(Union(arcs), shape), LEAD, alpha=0.6)
        outline(g, shape, seed + 3, 1.1)

    def finish(self, g):
        finish(g)


class Obl:
    """45-degree overhead camera: screen x = ox + x*u, screen y = oy - (y + z)*cos45*u (y points away from the viewer)."""
    view = np.array([0.0, -1.0, 1.0]) / math.sqrt(2)
    light = np.array([-0.5, -0.32, 0.85]) / np.linalg.norm([-0.5, -0.32, 0.85])
    shadow_dir = (0.5 / 0.85, 0.32 / 0.85)

    def __init__(self, ox, oy, u):
        self.ox, self.oy, self.u = ox, oy, u
        self.k = math.cos(math.radians(45))

    def p(self, x, y, z=0.0):
        return (self.ox + x * self.u, self.oy - (y + z) * self.k * self.u)

    def poly(self, pts3):
        return Poly([self.p(*q) for q in pts3])


def obl_depth(x, y):
    return -y + x * 1e-3


SK = Sketch()


def make_bg3d(scene):
    def bg(c, d):
        g = Ctx(c)
        paper(g, 3800)
        scene(g, SK, d)
        finish(g)
        g.commit()
    return bg


def make_bg2d(scene):
    def bg(c, d):
        g = Ctx(c)
        paper(g, 3801)
        scene(g, d)
        finish(g)
        g.commit()
    return bg


def sp_of(cam):
    return lambda x, y, z=0.0: tuple(int(round(v)) for v in cam.p(x, y, z))


# =================================================================== Level 1538 village street (45-degree)
C38 = Obl(0, 560, 22.0)


def l1538_scene(g, S, d):
    cam = C38
    dec = K.decal
    dec(g, S, cam, K.rect_ring(-5, 11.5, 50, 18.5), (150, 150, 150), "road", 3801)
    for y in (11.5, 18.5):
        a, b = cam.p(-5, y), cam.p(50, y)
        line(g, a[0], a[1], b[0], b[1], seed=int(y * 10), w=1.3)
    dec(g, S, cam, K.rect_ring(-5, -6, 50, 3.4), (200, 200, 200), "water", 3802)
    a, b = cam.p(-5, 3.4), cam.p(50, 3.4)
    line(g, a[0], a[1], b[0], b[1], seed=3803, w=1.4)
    sc = K.Scene(depth=obl_depth)
    shadows = []
    # back row: roofs and trees behind the street houses
    for k, (x0, w, wh) in enumerate(((-3, 9, 6.5), (7, 8, 7.5), (16, 10, 6.0), (27, 8, 8.0), (36, 9, 6.8))):
        sc.add(x0 + w / 2, 28, lambda x0=x0, w=w, wh=wh, k=k: K.gable(g, S, cam, x0, 28, x0 + w, 35, 0, wh, 2.8, (236, 232, 222), (196, 196, 196),
                                                                     3900 + k * 5, along_x=True, wall_kind="stone"))
    for k, (x, h) in enumerate(((5, 7), (16.5, 8), (26, 7.5), (43, 7))):
        sc.add(x, 27, lambda x=x, h=h, k=k: K.tree(g, S, cam, x, 27, h, (150, 150, 150), 3920 + k))
    # north row of houses (fronts face the street)
    houses = [(0, 19.5, 8, 6, 4.5, 2.6), (9, 19.5, 7, 6, 5.5, 2.4), (17, 19.5, 9, 6, 4.0, 3.0), (27, 19.5, 7, 6, 6.0, 2.2), (35, 19.5, 7, 6, 4.8, 2.6)]
    for k, (x0, y0, w, dp, wh, rh) in enumerate(houses):
        shadows.append((K.rect_ring(x0, y0, x0 + w, y0 + dp), wh + rh * 0.5))

        def house(x0=x0, y0=y0, w=w, dp=dp, wh=wh, rh=rh, k=k):
            K.gable(g, S, cam, x0, y0, x0 + w, y0 + dp, 0, wh, rh, (236, 232, 222), (196, 196, 196), 3810 + k * 7, along_x=True, wall_kind="stone")
            K.windows(g, S, cam, "y", y0, x0 + 0.5, x0 + w - 0.5, wh * 0.45, wh - 0.3, max(1, int(w / 2.6)), seed=3811 + k)
            dx = x0 + w * (0.25 if k % 2 else 0.7)
            S.face(g, K.quad_on(cam, "y", dx - 0.8, dx + 0.8, 0, 2.2, y0), (120, 100, 90), 0.2, "wood", 3812 + k, ang=0.0)
            if k == 1 and "chimney" not in d:
                K.box(g, S, cam, x0 + 4.5, y0 + 2.5, wh + 1.0, x0 + 5.4, y0 + 3.3, wh + rh + 1.4, (200, 200, 200), "stone", 3813)
            if k == 3:
                K.box(g, S, cam, x0 + 1, y0 + 2.5, wh + 0.8, x0 + 1.9, y0 + 3.3, wh + rh + 1.2, (200, 200, 200), "stone", 3814)
            if k == 2 and "sign" not in d:          # hanging shop sign
                p0 = cam.p(x0 + 1.5, y0, 3.2)
                line(g, p0[0], p0[1], p0[0] + 30, p0[1], seed=3815, w=1.4)
                for xx in (p0[0] + 12, p0[0] + 28):
                    line(g, xx, p0[1], xx, p0[1] + 8, seed=int(xx), w=0.8, over=0.5)
                sk(g, Ell(p0[0] + 20, p0[1] + 20, 13, 11), 0.15, 3816)
                sk(g, Circ(p0[0] + 20, p0[1] + 20, 5), 0.6, 3817, line=True)
            if k == 4 and "flowers" not in d:       # window box with flowers
                fx0, fx1 = x0 + 0.6, x0 + 3.0
                K.box(g, S, cam, fx0, y0 - 0.5, wh * 0.45 - 0.2, fx1, y0, wh * 0.45 + 0.3, (180, 160, 140), "wood", 3818)
                for j in range(5):
                    p = cam.p(fx0 + 0.3 + j * 0.5, y0 - 0.25, wh * 0.45 + 0.5)
                    S.blob(g, p[0], p[1], 5.5, 5, (200, 200, 200), 3819 + j, kind="body")
        sc.add(x0 + w / 2, y0, house)
    # laundry line across the street (difference)
    if "laundry" not in d:
        def laundry():
            a, b = cam.p(9.5, 19.5, 4.6), cam.p(16.5, 11.5, 4.2)
            pts = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + 14 * math.sin(t * math.pi)) for t in np.linspace(0, 1, 12)]
            for p0, p1 in zip(pts[:-1], pts[1:]):
                line(g, p0[0], p0[1], p1[0], p1[1], seed=int(p0[0]), w=0.8, over=0.2)
            for j, t in enumerate((0.25, 0.45, 0.65)):
                i = int(t * 11)
                px, py = pts[i]
                sk(g, Poly([(px - 9, py), (px + 9, py), (px + 8, py + 18 + j * 3), (px - 8, py + 18 + j * 3)]), 0.1 + 0.25 * j, 3825 + j)
        sc.add(13, 11, laundry)
    # south side: market stalls, barrels, crates, well, tree
    for k, x0 in enumerate((2, 12)):
        shadows.append((K.rect_ring(x0, 6, x0 + 6, 9.5), 3.2))

        def stall(x0=x0, k=k):
            K.box(g, S, cam, x0, 6, 0, x0 + 6, 9.5, 1.2, (210, 200, 190), "wood", 3830 + k)
            for (px, py) in ((x0 + 0.2, 6.2), (x0 + 5.8, 6.2)):
                K.box(g, S, cam, px - 0.12, py - 0.12, 1.2, px + 0.12, py + 0.12, 3.0, (150, 150, 150), "wood", 3832 + k)
            striped = not (k == 1 and "awning" in d)
            K.solid(g, S, cam, [(x0 - 0.3, 9.8, 3.4), (x0 + 6.3, 9.8, 3.4), (x0 + 6.3, 5.6, 2.8), (x0 - 0.3, 5.6, 2.8)],
                    [(x0 - 0.3, 9.8, 3.2), (x0 + 6.3, 9.8, 3.2), (x0 + 6.3, 5.6, 2.6), (x0 - 0.3, 5.6, 2.6)], (210, 210, 210), "plain", 3834 + k,
                    side_cols=[(210, 210, 210)])
            if striped:
                for j in range(4):
                    sx_ = x0 - 0.3 + j * 1.7
                    poly = cam.poly([(sx_, 9.8, 3.4), (sx_ + 0.85, 9.8, 3.4), (sx_ + 0.85, 5.6, 2.8), (sx_, 5.6, 2.8)])
                    tone(g, poly, 0.75, 3836 + j, ang=80)
            for j in range(4):           # produce
                p = cam.p(x0 + 0.8 + j * 1.4, 7.6, 1.2)
                S.blob(g, p[0], p[1] - 4, 9, 6, (210, 210, 210), 3840 + j + k * 5, kind="body")
        sc.add(x0 + 3, 6, stall)
    for k, (x, y) in enumerate(((20.5, 8), (21.8, 9.2), (21, 6.6))):
        if k == 1 and "barrel" in d:
            continue
        shadows.append(([(x + 0.7 * math.cos(t), y + 0.7 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 1.5))
        sc.add(x, y, lambda x=x, y=y, k=k: K.cyl(g, S, cam, x, y, 0, 1.5, 0.7, (170, 150, 130), "wood", 3850 + k))
    shadows.append(([(29 + 1.3 * math.cos(t), 8 + 1.3 * math.sin(t)) for t in np.linspace(0, math.tau, 10, endpoint=False)], 3.6))

    def well():
        K.cyl(g, S, cam, 29, 8, 0, 1.2, 1.3, (200, 200, 200), "stone", 3855)
        c_ = cam.p(29, 8, 1.2)
        g.fill(Ell(c_[0], c_[1], 1.1 * cam.u, 1.1 * cam.u * 0.7), LEAD, alpha=0.7)
        for x in (27.9, 30.1):
            K.box(g, S, cam, x - 0.12, 7.9, 1.2, x + 0.12, 8.1, 3.6, (160, 150, 140), "wood", 3856)
        K.gable(g, S, cam, 27.6, 7.0, 30.4, 9.0, 3.4, 0.2, 1.0, (200, 200, 200), (170, 170, 170), 3857, along_x=True)
    sc.add(29, 7, well)
    if "cat" not in d:
        def cat():
            cx, cy = cam.p(31.8, 6.2, 0.5)
            S.blob(g, cx, cy, 17, 10, (120, 120, 120), 3860, kind="body")
            S.blob(g, cx - 17, cy - 9, 8, 8, (120, 120, 120), 3861, kind="body")
            for e in (-1, 1):
                sk(g, Poly([(cx - 17 + e * 6, cy - 14), (cx - 17 + e * 7, cy - 22), (cx - 17 + e * 1, cy - 16)]), 0.4, 3862 + e)
            line(g, cx + 16, cy + 2, cx + 30, cy - 10, seed=3864, w=2.2, over=0.5)
        sc.add(31.5, 6, cat)
    shadows.append(("tree", 37, 8, 5.0))
    sc.add(37, 8, lambda: K.tree(g, S, cam, 37, 8, 5.0, (150, 150, 150), 3862))
    for k, (x, y) in enumerate(((24.5, 6.4), (25.8, 6.4))):
        sc.add(x, y, lambda x=x, y=y, k=k: K.box(g, S, cam, x - 0.6, y - 0.6, 0, x + 0.6, y + 0.6, 1.0 + 0.3 * k, (190, 180, 170), "wood", 3865 + k))
    # lamp posts, people
    for k, x in enumerate((6, 24, 40)):
        if k == 1 and "lamp" in d:
            continue
        sc.add(x, 18.8, lambda x=x, k=k: (K.cyl(g, S, cam, x, 18.8, 0, 3.6, 0.1, (120, 120, 120), "metal", 3870 + k, n=6),
                                         K.box(g, S, cam, x - 0.35, 18.45, 3.6, x + 0.35, 19.15, 4.4, (230, 230, 230), "glass", 3873 + k)))
    for k, (x, y) in enumerate(((5, 15), (14, 14), (22, 16.5), (33, 13.5))):
        sc.add(x, y, lambda x=x, y=y, k=k: K.person(g, S, cam, x, y, (180, 180, 180) if k % 2 else (90, 90, 90), 3880 + k))
    # canal: railing posts, a moored boat (difference), stone bridge steps at the right
    for x in range(0, 46, 3):
        sc.add(x, 3.6, lambda x=x: K.box(g, S, cam, x - 0.12, 3.4, 0, x + 0.12, 3.7, 1.0, (180, 180, 180), "stone", 3890 + x))
    a, b = cam.p(-2, 3.55, 1.0), cam.p(47, 3.55, 1.0)
    sc.add(22, 3.4, lambda: line(g, a[0], a[1], b[0], b[1], seed=3895, w=1.2), dz=-0.01)
    if "boat" not in d:
        def boat():
            K.solid(g, S, cam, [(8, 0.6, -0.3), (16, 0.6, -0.3), (17.6, 1.6, -0.2), (16, 2.6, -0.3), (8, 2.6, -0.3)],
                    [(8.5, 1.0, -1.2), (15.6, 1.0, -1.2), (16.8, 1.6, -1.2), (15.6, 2.2, -1.2), (8.5, 2.2, -1.2)], (150, 140, 130), "wood", 3896,
                    top_col=(220, 210, 200))
            for x in (10, 12.5):
                K.box(g, S, cam, x - 0.15, 0.8, -0.3, x + 0.15, 2.4, 0.0, (150, 140, 130), "wood", 3897)
        sc.add(12, 0.6, boat)
    for sh in shadows:
        if sh[0] == "tree":
            K.tree_shadow(g, S, cam, sh[1], sh[2], sh[3])
        else:
            K.shadow(g, S, cam, sh[0], 0, sh[1])
    sc.draw()


_s38 = sp_of(C38)
L1538_ELEMENTS = [
    E("smoke", el(lambda g, m: [outline(g, Circ(x, y, r), 3898, 0.9, 0.7) for x, y, r in ((_s38(31.45, 22.4, 8.6)[0], _s38(31.45, 22.4, 8.6)[1] - 8, 6),)]),
      anim=dict(driftVelocity=(8, 36), driftLength=60, driftFade=True, driftGrow=1.6)),
    E("birds", el(lambda g, m: [(line(g, x - 7, y - 2, x, y + 1, 1, 1.1, 0.8, 0), line(g, x, y + 1, x + 7, y - 2, 2, 1.1, 0.8, 0)) for x, y in ((400, 40), (424, 54))]),
      pivot=(412, 47), anim=dict(driftVelocity=(26, 0), driftLength=900, driftStart=-500, stretch=(0, 0.5), scaleSpeed=2.2)),
    E("ripple", el(lambda g, m: [line(g, x - 10, y, x + 10, y, 3, 1.0, 0.6, 0) for x, y in ((300, 600), (700, 590), (520, 608))]),
      anim=dict(twinkle=0.8, twinkleSpeed=0.5)),
]

L1538_DIFFS = [
    ("chimney", *_s38(13.95, 22.9, 8.4), 0),
    ("sign", _s38(18.5, 19.5, 3.2)[0] + 20, _s38(18.5, 19.5, 3.2)[1] + 18, 0),
    ("flowers", *_s38(36.8, 19.2, 3.0), 0),
    ("laundry", *_s38(13, 15.5, 4.0), 0),
    ("awning", *_s38(15, 7.7, 3.1), 0),
    ("barrel", *_s38(21.8, 9.2, 0.8), 0),
    ("cat", _s38(31.8, 6.2, 0.5)[0] - 4, _s38(31.8, 6.2, 0.5)[1] - 4, 0),
    ("lamp", *_s38(24, 18.8, 3.0), 0),
    ("boat", *_s38(12.5, 1.6, -0.5), 0),
]


# =================================================================== Level 1539 courtyard garden (45-degree)
C39 = Obl(0, 630, 22.0)


def l1539_scene(g, S, d):
    cam = C39
    dec = K.decal
    dec(g, S, cam, K.rect_ring(-5, -5, 50, 45), (200, 200, 200), "grass", 3901)
    dec(g, S, cam, K.rect_ring(-5, 13.5, 50, 18.5), (220, 220, 220), "dirt", 3902)
    dec(g, S, cam, K.rect_ring(18, -5, 23, 45), (220, 220, 220), "dirt", 3903)
    dec(g, S, cam, [(20.5 + 7 * math.cos(t), 16 + 7 * math.sin(t)) for t in np.linspace(0, math.tau, 24, endpoint=False)], (220, 220, 220), "dirt", 3904)
    for pts in (K.rect_ring(-5, 13.5, 50, 18.5), K.rect_ring(18, -5, 23, 45)):
        for i in range(4):
            a, b = cam.p(*pts[i]), cam.p(*pts[(i + 1) % 4])
            line(g, a[0], a[1], b[0], b[1], seed=3905 + i, w=0.9, k=0.5)
    sc = K.Scene(depth=obl_depth)
    shadows = []
    # back wall with a gate, trees beyond
    for k, (x, h) in enumerate(((3, 6), (11, 7), (30, 6.5), (40, 7))):
        sc.add(x, 37, lambda x=x, h=h, k=k: K.tree(g, S, cam, x, 37, h, (150, 150, 150), 3910 + k))
    for x0, x1 in ((-5, 18), (23, 50)):
        sc.add((x0 + x1) / 2, 34, lambda x0=x0, x1=x1: K.box(g, S, cam, x0, 34, 0, x1, 35, 3.0, (220, 216, 206), "stone", 3915 + int(x0)))
    for k, x in enumerate((17.2, 23.8)):
        def pillar(x=x, k=k):
            K.box(g, S, cam, x - 0.8, 33.8, 0, x + 0.8, 35.2, 3.8, (210, 206, 196), "stone", 3918 + k)
            if not (k == 1 and "urn" in d):
                K.cyl(g, S, cam, x, 34.5, 3.8, 4.4, 0.35, (200, 200, 200), "stone", 3920 + k, r1=0.6)
                K.cyl(g, S, cam, x, 34.5, 4.4, 5.2, 0.6, (200, 200, 200), "stone", 3922 + k, r1=0.45)
        sc.add(x, 33.8, pillar)
    # hedged parterres (low hedge rings) with flower beds
    for k, (x0, y0) in enumerate(((2, 21), (26, 21), (2, 2), (26, 2))):
        x1, y1 = x0 + 13, y0 + 10
        for (a0, b0, a1, b1) in ((x0, y0, x1, y0 + 0.8), (x0, y1 - 0.8, x1, y1), (x0, y0, x0 + 0.8, y1), (x1 - 0.8, y0, x1, y1)):
            sc.add((a0 + a1) / 2, b0, lambda a0=a0, b0=b0, a1=a1, b1=b1, k=k: K.box(g, S, cam, a0, b0, 0, a1, b1, 1.0, (170, 170, 170), "foliage", 3925 + k))
    # NE parterre: gazebo
    gx, gy = 32.5, 26
    shadows.append(([(gx + 2.8 * math.cos(t), gy + 2.8 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 5.0))

    def gazebo():
        K.cyl(g, S, cam, gx, gy, 0, 0.4, 2.6, (220, 220, 220), "stone", 3930, n=8)
        for t in np.linspace(0, math.tau, 8, endpoint=False):
            if math.sin(t) < 0.3:
                K.cyl(g, S, cam, gx + 2.3 * math.cos(t), gy + 2.3 * math.sin(t), 0.4, 3.2, 0.1, (200, 200, 200), "wood", 3931, n=6)
        K.cone(g, S, cam, gx, gy, 3.2, 5.6, 3.0, (190, 190, 190), "roof", 3932, n=8)
        p = cam.p(gx, gy, 5.6)
        line(g, p[0], p[1], p[0], p[1] - 14, seed=3933, w=1.4)
        sk(g, Circ(p[0], p[1] - 15, 3), 0.5, 3934)
    sc.add(gx, gy - 2.6, gazebo)
    # NW parterre: flower beds (blobs) + topiary
    for k, (x, y) in enumerate(((5, 25), (8, 28), (11, 24.5), (6, 23), (12.5, 28))):
        sc.add(x, y, lambda x=x, y=y, k=k: S.blob(g, *cam.p(x, y, 0.4), 13, 8, (200, 200, 200), 3940 + k, kind="foliage"))
    # SW parterre: topiary balls (difference: one) + birdbath with a bird (difference)
    for k, (x, y) in enumerate(((5, 5), (11.5, 5), (5, 9), (11.5, 9))):
        if k == 3 and "topiary" in d:
            continue
        shadows.append(([(x + 0.9 * math.cos(t), y + 0.9 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 2.4))
        sc.add(x, y, lambda x=x, y=y, k=k: (K.cyl(g, S, cam, x, y, 0, 0.8, 0.15, (150, 150, 150), "wood", 3950 + k, n=6),
                                           S.blob(g, *cam.p(x, y, 1.8), 19, 17, (170, 170, 170), 3955 + k)))

    def birdbath():
        K.cyl(g, S, cam, 8.2, 7, 0, 1.4, 0.3, (220, 220, 220), "stone", 3960, n=8)
        K.cyl(g, S, cam, 8.2, 7, 1.4, 1.8, 1.1, (220, 220, 220), "stone", 3961, r1=1.3)
        c_ = cam.p(8.2, 7, 1.8)
        g.fill(Ell(c_[0], c_[1], 22, 12), LEAD, alpha=0.2)
        if "bird" not in d:
            S.blob(g, c_[0] + 10, c_[1] - 14, 15, 9, (150, 150, 150), 3962, kind="body")
            S.blob(g, c_[0] - 2, c_[1] - 24, 7, 7, (150, 150, 150), 3963, kind="body")
            line(g, c_[0] - 8, c_[1] - 24, c_[0] - 17, c_[1] - 22, seed=3964, w=2.0, over=0)
            line(g, c_[0] + 24, c_[1] - 16, c_[0] + 36, c_[1] - 22, seed=3965, w=3.0, over=0)
    sc.add(8.2, 6, birdbath)
    # SE parterre: pond with lily pads and stepping stones (difference: one stone)
    pond = [(28, 4), (37, 3.5), (38.5, 8), (35, 11), (29, 10.5), (27.5, 7)]
    sc.add(33, 11, lambda: (dec(g, S, cam, pond, (200, 200, 200), "water", 3965, rough=3),
                            [outline(g, Ell(*cam.p(x, y), 9, 5), 3966 + int(x)) for x, y in ((30, 6), (35.5, 8.5), (33, 4.8))]), dz=-30)
    for k, (x, y) in enumerate(((29.5, 9.2), (31.5, 7.8), (33.6, 6.6), (35.8, 5.4))):
        if k == 2 and "stone" in d:
            continue
        sc.add(x, y, lambda x=x, y=y, k=k: K.cyl(g, S, cam, x, y, 0, 0.25, 0.75, (200, 200, 200), "stone", 3970 + k, n=10), dz=-29)
    # fountain in the middle
    shadows.append(([(20.5 + 3 * math.cos(t), 16 + 3 * math.sin(t)) for t in np.linspace(0, math.tau, 12, endpoint=False)], 1.0))

    def fountain():
        K.cyl(g, S, cam, 20.5, 16, 0, 0.8, 3.0, (220, 220, 220), "stone", 3975, n=20)
        c_ = cam.p(20.5, 16, 0.8)
        g.fill(Ell(c_[0], c_[1], 2.75 * cam.u, 2.75 * cam.u * 0.7), PAPER)
        hf = hatch(-2, 5.0, w=0.14, seed=3976, brk=0.5, seg=10)
        g.fill(Ell(c_[0], c_[1], 2.75 * cam.u, 2.75 * cam.u * 0.7), LEAD, alpha=lambda X, Y: 0.12 + hf(X, Y) * 0.5)
        K.cyl(g, S, cam, 20.5, 16, 0.8, 2.6, 0.4, (220, 220, 220), "stone", 3977, n=10)
        K.cyl(g, S, cam, 20.5, 16, 2.6, 3.0, 1.2, (220, 220, 220), "stone", 3978, n=14, r1=1.5)
    sc.add(20.5, 13, fountain)
    # statues on plinths at the plaza (difference: one), benches (difference), wheelbarrow (difference)
    for k, (x, y) in enumerate(((15.5, 20.5), (25.5, 20.5))):
        if k == 1 and "statue" in d:
            continue
        shadows.append((K.rect_ring(x - 0.7, y - 0.7, x + 0.7, y + 0.7), 4.6))
        sc.add(x, y - 0.7, lambda x=x, y=y, k=k: (K.box(g, S, cam, x - 0.7, y - 0.7, 0, x + 0.7, y + 0.7, 1.6, (220, 220, 220), "stone", 3980 + k),
                                                 K.person(g, S, cam, x, y, (226, 226, 226), 3982 + k, z=1.6, s=1.6)))
    for k, (x, y) in enumerate(((11, 12.8), (30, 12.8), (11, 19.2))):
        if k == 1 and "bench" in d:
            continue
        sc.add(x, y, lambda x=x, y=y, k=k: K.bench(g, S, cam, x, y, True, (190, 190, 190), 3985 + k))
    if "barrow" not in d:
        def barrow():
            K.solid(g, S, cam, [(39.5, 15, 1.4), (42.5, 15, 1.4), (42.5, 17, 1.4), (39.5, 17, 1.4)],
                    [(40, 15.4, 0.6), (42, 15.4, 0.6), (42, 16.6, 0.6), (40, 16.6, 0.6)], (180, 180, 180), "metal", 3990, top_col=(120, 120, 120))
            K.wheel(g, S, cam, 39.2, 15.8, 16.2, 0.5, 0.5, seed=3991)
            a, b = cam.p(42.5, 15.5, 1.2), cam.p(44.5, 15.2, 0.8)
            line(g, a[0], a[1], b[0], b[1], seed=3992, w=2)
            a, b = cam.p(42.5, 16.5, 1.2), cam.p(44.5, 16.8, 0.8)
            line(g, a[0], a[1], b[0], b[1], seed=3993, w=2)
        sc.add(41, 15, barrow)
    for k, (x, y) in enumerate(((21, 7), (19.5, 25))):
        sc.add(x, y, lambda x=x, y=y, k=k: K.person(g, S, cam, x, y, (120, 120, 120) if k else (200, 200, 200), 3995 + k))
    for sh in shadows:
        K.shadow(g, S, cam, sh[0], 0, sh[1])
    sc.draw()


_s39 = sp_of(C39)
L1539_ELEMENTS = [
    E("spout", el(lambda g, m: [outline(g, Ell(_s39(20.5, 16, 3.0)[0], _s39(20.5, 16, 3.0)[1] - 14, 4, 13), 3999, 0.9, 0.8)]),
      pivot=_s39(20.5, 16, 3.0), anim=dict(stretch=(0.05, 0.2), scaleSpeed=1.4)),
    E("butterfly", el(lambda g, m: [outline(g, Ell(x, y, 4, 3), 3998, 0.8, 0.8) for x, y in ((200, 300), (206, 300))]),
      pivot=(203, 300), anim=dict(orbitRadius=(60, 30), orbitSpeed=0.12, stretch=(0.5, 0), scaleSpeed=3)),
]

L1539_DIFFS = [
    ("urn", *_s39(23.8, 34.5, 4.6), 0),
    ("topiary", *_s39(11.5, 9, 1.6), 0),
    ("bird", _s39(8.2, 7, 1.8)[0] + 8, _s39(8.2, 7, 1.8)[1] - 16, 0),
    ("stone", *_s39(33.6, 6.6, 0.2), 0),
    ("statue", *_s39(25.5, 20.5, 3.0), 0),
    ("bench", *_s39(30, 12.8, 0.8), 0),
    ("barrow", *_s39(41.5, 16, 1.0), 0),
]


# =================================================================== Level 1540 station platform (2D side view)
def spoked_wheel(g, x, y, r, seed, spokes=10):
    sk(g, Circ(x, y, r) - Circ(x, y, r * 0.78), 0.6, seed)
    for k in range(spokes):
        a = k * math.tau / spokes
        line(g, x, y, x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8, seed=seed + k, w=1.4, over=0)
    sk(g, Circ(x, y, r * 0.2), 0.5, seed + 20)


def traveller(g, x, base, s=1.0, t=0.5, hat=True, seed=0, umbrella=False, sitting=False):
    h = 92 * s
    if sitting:
        sk(g, Poly([(x - 10 * s, base - 30 * s), (x + 22 * s, base - 30 * s), (x + 22 * s, base - 4 * s), (x + 16 * s, base - 4 * s), (x + 14 * s, base - 22 * s),
                    (x - 8 * s, base - 22 * s)]), t + 0.15, seed)
        body_top, body_bot = base - 76 * s, base - 26 * s
    else:
        for dx in (-5, 5):
            sk(g, Box(x + dx * s - 4 * s, base - 40 * s, x + dx * s + 4 * s, base, 2), t + 0.15, seed + dx)
        body_top, body_bot = base - h * 0.82, base - 36 * s
    coat = Poly([(x - 13 * s, body_bot), (x + 13 * s, body_bot), (x + 10 * s, body_top), (x - 10 * s, body_top)])
    sk(g, coat, t, seed + 3, ang=70, grad=(x - 13 * s, x + 13 * s, 0.25))
    sk(g, Circ(x, body_top - 10 * s, 8.5 * s), 0.08, seed + 4)
    if hat:
        sk(g, Union([Box(x - 17 * s, body_top - 17 * s, x + 17 * s, body_top - 13 * s), Box(x - 10 * s, body_top - 36 * s, x + 10 * s, body_top - 15 * s, 2)]), 0.8, seed + 5)
    if umbrella:
        line(g, x + 14 * s, body_top + 10 * s, x + 16 * s, body_top - 40 * s, seed=seed + 6, w=1.4)
        sk(g, Inter(Ell(x + 16 * s, body_top - 40 * s, 32 * s, 20 * s), Box(x - 30 * s, body_top - 64 * s, x + 60 * s, body_top - 40 * s)), 0.7, seed + 7, ang=80)


def l1540_scene(g, d):
    # station wall (brick courses), arched windows, clock
    wall = Box(-2, 60, W + 2, 300)
    sk(g, wall, 0.12, 4001, ang=80, line=False)
    for y in range(66, 300, 12):
        a, b = 0, W
        g.fill(Seg(a, y, b, y, 0.6), LEAD, alpha=0.18)
    for k, x in enumerate((90, 330, 570, 810)):
        win = Union([Box(x - 38, 130, x + 38, 260), Ell(x, 130, 38, 38)])
        sk(g, win, 0.5, 4002 + k, ang=60)
        for xx in (x - 13, x + 13):
            line(g, xx, 100, xx, 260, seed=4006 + int(xx), w=1.0, k=0.6, over=0)
        line(g, x - 38, 190, x + 38, 190, seed=4010 + k, w=1.0, k=0.6, over=0)
        outline(g, Union([Box(x - 44, 124, x + 44, 266), Ell(x, 124, 44, 44)]) - win, 4014 + k, 1.0, 0.7)
    cx, cy = 450, 150
    if "clock" not in d:
        sk(g, Circ(cx, cy, 34), 0.05, 4020)
        outline(g, Circ(cx, cy, 28), 4021, 0.9, 0.7)
        for k in range(12):
            a = k * math.tau / 12
            line(g, cx + math.cos(a) * 24, cy + math.sin(a) * 24, cx + math.cos(a) * 28, cy + math.sin(a) * 28, seed=4022 + k, w=1.6, over=0)
        line(g, cx, cy, cx + 12, cy - 14, seed=4040, w=2.4, over=0)
        line(g, cx, cy, cx - 2, cy - 24, seed=4041, w=1.6, over=0)
    else:
        sk(g, Box(cx - 30, cy - 30, cx + 30, cy + 30, 4), 0.05, 4020)
        outline(g, Box(cx - 24, cy - 24, cx + 24, cy + 24, 3), 4021, 0.9, 0.7)
        line(g, cx, cy, cx + 14, cy + 4, seed=4040, w=2.4, over=0)
        line(g, cx, cy, cx - 6, cy - 20, seed=4041, w=1.6, over=0)
    line(g, cx, 60, cx, cy - 34, seed=4042, w=1.6)
    # canopy roof with trusses and pigeons on a beam (difference)
    sk(g, Poly([(-2, 0), (W + 2, 0), (W + 2, 52), (-2, 72)]), 0.55, 4043, ang=10)
    for x in range(0, 900, 60):
        line(g, x, 62 - x * 0.02, x + 30, 30, seed=4044 + x, w=1.0, k=0.6, over=0)
        line(g, x + 30, 30, x + 60, 61 - (x + 60) * 0.02, seed=4045 + x, w=1.0, k=0.6, over=0)
    line(g, -2, 72, W + 2, 52, seed=4046, w=2.4)
    if "pigeons" not in d:
        for k, x in enumerate((640, 664, 688)):
            y = 70 - x * 0.02
            sk(g, Ell(x, y - 7, 10, 7), 0.35, 4047 + k)
            sk(g, Circ(x - 9, y - 13, 4.5), 0.35, 4050 + k)
    # far track with the train
    sk(g, Box(-2, 300, W + 2, 330), 0.4, 4053, ang=0, line=False)
    for y in (318, 326):
        line(g, -2, y, W + 2, y, seed=4054 + y, w=1.6)
    # carriage (right) and locomotive (left)
    sk(g, Box(560, 160, 910, 312, 6), 0.18, 4060, ang=80)
    for k, x in enumerate(range(580, 900, 52)):
        sk(g, Box(x, 184, x + 36, 230, 3), 0.55, 4061 + k, ang=60)
    sk(g, Box(556, 150, 914, 162, 4), 0.6, 4070)
    for x in (610, 860):
        spoked_wheel(g, x, 312, 16, 4071 + x, 8)
    boiler = Box(110, 196, 430, 280, 8)
    sk(g, boiler, 0.3, 4080, ang=0, grad=None)
    tone(g, boiler, 0.0, 4081, ang=0, grad=(196, 280, 0.0))
    g.fill(boiler, LEAD, alpha=lambda X, Y: 0.35 * smooth(220, 282, Y))
    for x in (180, 260, 340):
        line(g, x, 198, x, 278, seed=4082 + x, w=1.0, k=0.6, over=0)
    sk(g, Union([Box(140, 140, 168, 200), Box(132, 132, 176, 146, 3)]), 0.5, 4085)
    sk(g, Ell(260, 196, 22, 14) & Box(230, 180, 290, 198), 0.35, 4086)
    sk(g, Box(430, 150, 540, 290, 4), 0.28, 4087, ang=80)
    sk(g, Box(448, 170, 500, 218, 3), 0.65, 4088)
    sk(g, Box(424, 140, 548, 154, 3), 0.6, 4089)
    sk(g, Box(100, 276, 545, 296, 3), 0.55, 4090)
    for k, x in enumerate((200, 290, 380)):
        spoked_wheel(g, x, 300, 30, 4091 + k * 30)
    for x in (130, 500):
        spoked_wheel(g, x, 308, 14, 4095 + x, 8)
    line(g, 200, 304, 380, 304, seed=4099, w=3.4, over=0)
    # platform with edge stones
    sk(g, Box(-2, 330, W + 2, 470), 0.06, 4100, ang=5, line=False)
    for x in range(0, 900, 70):
        g.fill(Seg(x, 330, x - 40, 470, 0.7), LEAD, alpha=0.2)
    sk(g, Box(-2, 462, W + 2, 476), 0.35, 4101, ang=0)
    for x in range(0, 900, 36):
        line(g, x, 462, x, 476, seed=4102 + x, w=0.8, k=0.5, over=0)
    # near track
    sk(g, Box(-2, 476, W + 2, H + 2), 0.25, 4103, ang=0, line=False)
    for x in range(-20, 920, 34):
        sk(g, Poly([(x, 520), (x + 22, 520), (x + 26, 560), (x - 4, 560)]), 0.45, 4104 + x)
    for y in (512, 568):
        line(g, -2, y, W + 2, y, seed=4105 + y, w=3.2)
    # columns of the canopy
    for x in (210, 690):
        sk(g, Box(x - 7, 58, x + 7, 450), 0.35, 4110 + x, ang=88, grad=(x - 7, x + 7, 0.4))
        sk(g, Box(x - 13, 440, x + 13, 456, 2), 0.4, 4111 + x)
    # bench with a seated traveller (difference: his hat), luggage trolley (difference: top case), lamp, lady with umbrella, dog (difference)
    sk(g, Box(250, 392, 400, 402, 2), 0.4, 4120)
    sk(g, Box(250, 360, 400, 372, 2), 0.4, 4121)
    for x in (262, 388):
        line(g, x, 402, x, 440, seed=4122 + x, w=2.2)
    traveller(g, 300, 432, 0.9, 0.55, hat="hat" not in d, seed=4125, sitting=True)
    sk(g, Box(470, 410, 600, 420, 2), 0.45, 4130)
    for x in (480, 590):
        spoked_wheel(g, x, 432, 12, 4131 + x, 6)
    line(g, 600, 415, 630, 360, seed=4133, w=2.2)
    sk(g, Box(478, 370, 560, 410, 4), 0.35, 4134, ang=80)
    sk(g, Box(500, 380, 520, 386, 1), 0.7, 4135)
    if "case" not in d:
        sk(g, Box(490, 336, 548, 370, 4), 0.6, 4136, ang=40)
        sk(g, Box(510, 328, 528, 337, 2), 0.3, 4137)
    traveller(g, 770, 450, 1.0, 0.75, hat=False, seed=4140, umbrella=True)
    sk(g, Box(124, 220, 132, 460), 0.45, 4145, ang=88)
    if "lamp" not in d:
        sk(g, Poly([(112, 220), (144, 220), (138, 186), (118, 186)]), 0.1, 4146)
        sk(g, Poly([(110, 186), (128, 170), (146, 186)]), 0.6, 4147)
    if "dog" not in d:
        dx, db = 680, 456
        sk(g, Ell(dx, db - 22, 24, 12), 0.35, 4150, grad=(dx - 24, dx + 24, 0.3))
        sk(g, Circ(dx + 24, db - 34, 10), 0.35, 4151)
        sk(g, Ell(dx + 30, db - 30, 9, 5), 0.3, 4152)
        for lx in (-16, -8, 10, 18):
            line(g, dx + lx, db - 14, dx + lx, db, seed=4153 + lx, w=2.6, over=0)
        line(g, dx - 22, db - 26, dx - 36, db - 38, seed=4158, w=2.2, over=0)
    # sign board on two posts (bars instead of text)
    for x in (60, 200):
        line(g, x, 360, x, 460, seed=4160 + x, w=2.4)
    sk(g, Box(44, 330, 216, 370, 3), 0.08, 4162)
    for k in range(4):
        sk(g, Box(64 + k * 36, 342, 90 + k * 36, 358, 1), 0.7, 4163 + k, line=False)


L1540_ELEMENTS = [
    E("steam", el(lambda g, m: [outline(g, Circ(x, y, r), 4170 + int(x), 1.0, 0.8) for x, y, r in ((154, 112, 16), (170, 86, 22), (196, 58, 26))]),
      anim=dict(driftVelocity=(16, 40), driftLength=110, driftFade=True, driftGrow=1.5)),
    E("steam2", el(lambda g, m: [outline(g, Circ(x, y, r), 4180 + int(x), 1.0, 0.7) for x, y, r in ((150, 116, 12), (162, 96, 16))]),
      anim=dict(driftVelocity=(12, 36), driftLength=110, driftFade=True, driftGrow=1.6, phase=0.5)),
    E("pendulum", el(lambda g, m: line(g, 450, 186, 450, 214, 4190, 1.4, 0.8, 0)), pivot=(450, 186), anim=dict(swingAngle=10, swingSpeed=0.5)),
]

L1540_DIFFS = [
    ("clock", 450, 150, 0),
    ("pigeons", 664, 52, 0),
    ("hat", 300, 326, 0),
    ("case", 519, 350, 0),
    ("lamp", 128, 200, 0),
    ("dog", 690, 434, 0),
]


# =================================================================== Level 1541 study corner (2D)
def l1541_scene(g, d):
    # wall with faint stripes, wainscot, floor boards
    for x in range(0, 900, 18):
        g.fill(Seg(x, 0, x, 380, 0.6), LEAD, alpha=0.12)
    sk(g, Box(-2, 380, W + 2, 462), 0.18, 4201, ang=88, line=False)
    line(g, -2, 380, W + 2, 380, seed=4202, w=1.6)
    for x in range(40, 900, 120):
        outline(g, Box(x, 392, x + 96, 452, 2), 4203 + x, 0.9, 0.6)
    sk(g, Box(-2, 462, W + 2, H + 2), 0.22, 4204, ang=2, line=False)
    for k in range(-6, 14):
        line(g, 450 + k * 70, 462, 450 + k * 140, 600, seed=4205 + k, w=0.9, k=0.5, over=0)
    line(g, -2, 462, W + 2, 462, seed=4230, w=1.8)
    # window with curtains (left)
    sk(g, Box(50, 60, 260, 330), 0.04, 4231)
    for k, (x, h) in enumerate(((90, 90), (150, 120), (210, 80))):
        sk(g, Rough(Ell(x, 330 - h, 50, h * 0.6), 6, 18, 4232 + k), 0.2, 4235 + k, ang=60, line=True, w=0.8)
    for x in (155,):
        line(g, x, 60, x, 330, seed=4238, w=3.0, over=0)
    line(g, 50, 190, 260, 190, seed=4239, w=3.0, over=0)
    outline(g, Box(44, 54, 266, 336), 4240, 1.4)
    sk(g, Box(36, 330, 274, 344, 2), 0.25, 4241)
    for x0, x1 in ((20, 86), (226, 292)):
        cur = Poly([(x0, 40), (x1, 40), (x1 + (8 if x0 > 100 else -4), 360), (x0 + (4 if x0 > 100 else -8), 360)])
        g.fill(cur, PAPER)
        g.fill(cur, LEAD, alpha=lambda X, Y, x0=x0, x1=x1: 0.12 + 0.35 * np.abs(np.sin((X - x0) / (x1 - x0) * math.pi * 3)) ** 2)
        tone(g, cur, 0.3, 4242 + x0, ang=88)
        outline(g, cur, 4243 + x0)
    line(g, 10, 40, 300, 40, seed=4245, w=3.0)
    # bookshelf (right) with a vase (difference)
    sk(g, Box(630, 40, 890, 470, 3), 0.45, 4250, ang=88, grad=(630, 890, 0.2))
    rnd = random.Random(4251)
    for r_, y0 in enumerate((60, 160, 260, 360)):
        sk(g, Box(646, y0, 874, y0 + 92), 0.6, 4252 + r_, ang=88, line=True)
        x = 650
        while x < 860:
            if r_ == 1 and 760 < x < 830:
                x = 830
                continue
            bw = rnd.uniform(10, 22)
            bh = rnd.uniform(56, 86)
            if x + bw > 870:
                break
            lean = 0 if rnd.random() < 0.85 else 8
            sk(g, Poly([(x, y0 + 92), (x + bw, y0 + 92), (x + bw + lean, y0 + 92 - bh), (x + lean, y0 + 92 - bh)]), rnd.uniform(0.05, 0.6),
               4260 + int(x) + r_ * 900, ang=88)
            x += bw + rnd.uniform(0.5, 2)
        sk(g, Box(640, y0 + 92, 880, y0 + 100), 0.3, 4255 + r_)
    if "vase" not in d:
        vx, vy = 796, 252
        sk(g, Union([Ell(vx, vy - 26, 20, 26), Box(vx - 8, vy - 64, vx + 8, vy - 46)]), 0.15, 4256, grad=(vx - 20, vx + 20, 0.45))
        for k in range(3):
            line(g, vx, vy - 60, vx - 18 + k * 18, vy - 96, seed=4257 + k, w=1.2)
            sk(g, Circ(vx - 18 + k * 18, vy - 98, 6), 0.2, 4258 + k)
    # picture frame on the wall (difference: landscape becomes a portrait)
    sk(g, Box(330, 60, 470, 170, 2), 0.5, 4270)
    sk(g, Box(342, 72, 458, 158), 0.04, 4271)
    if "picture" not in d:
        sk(g, Poly([(342, 140), (380, 100), (410, 128), (436, 106), (458, 132), (458, 158), (342, 158)]), 0.35, 4272, ang=30)
        sk(g, Circ(430, 90, 8), 0.05, 4273)
    else:
        sk(g, Ell(400, 104, 14, 17), 0.1, 4272)
        sk(g, Inter(Ell(400, 160, 34, 34), Box(342, 124, 458, 158)), 0.5, 4273)
    # wall clock (pendulum is an element)
    sk(g, Box(530, 70, 586, 210, 6), 0.4, 4280, ang=88)
    sk(g, Circ(558, 104, 20), 0.02, 4281)
    line(g, 558, 104, 566, 92, seed=4282, w=1.8, over=0)
    line(g, 558, 104, 552, 116, seed=4283, w=1.4, over=0)
    sk(g, Box(540, 134, 576, 200, 3), 0.1, 4284)
    # rug
    rug = Ell(450, 540, 300, 44)
    sk(g, rug, 0.2, 4290, ang=0)
    outline(g, Ell(450, 540, 270, 34), 4291, 0.9, 0.7)
    # desk with drawers
    g.fill(Ell(450, 500, 200, 14), LEAD, alpha=0.18, feather=8)
    sk(g, Box(290, 372, 620, 388, 2), 0.35, 4300, ang=2)
    sk(g, Box(300, 388, 400, 490, 2), 0.3, 4301, ang=88, grad=(300, 400, 0.2))
    sk(g, Box(510, 388, 610, 490, 2), 0.3, 4302, ang=88, grad=(510, 610, 0.2))
    for y in (420, 455):
        for x0 in (300, 510):
            line(g, x0 + 4, y, x0 + 96, y, seed=4303 + y + x0, w=1.0, k=0.6, over=0)
            sk(g, Circ(x0 + 50, y - 16, 3), 0.7, 4305 + y + x0)
    # on the desk: lamp, book stack, open book, globe (difference), inkwell + quill (difference), cup (difference)
    sk(g, Ell(340, 370, 22, 6), 0.5, 4310)
    line(g, 340, 368, 352, 300, seed=4311, w=2.4)
    lampshade = Poly([(326, 300), (378, 300), (366, 266), (338, 266)])
    sk(g, lampshade, 0.2, 4312, ang=80)
    g.fill(Poly([(326, 300), (378, 300), (420, 372), (290, 372)]), (255, 255, 250), alpha=0.25, feather=10)
    for k, (w, h, t) in enumerate(((70, 12, 0.4), (64, 10, 0.2), (72, 14, 0.55))):
        sk(g, Box(392 - w / 2 + k * 3, 372 - 12 - sum(hh for _, hh, _ in ((70, 12, 0), (64, 10, 0), (72, 14, 0))[:k]) - h + 12,
                  392 + w / 2 + k * 3, 372 - sum(hh for _, hh, _ in ((70, 12, 0), (64, 10, 0), (72, 14, 0))[:k]), 2), t, 4313 + k, ang=5)
    sk(g, Poly([(430, 370), (470, 360), (510, 370), (510, 374), (430, 374)]), 0.05, 4320)
    line(g, 470, 360, 470, 372, seed=4321, w=1.0)
    for k in range(4):
        line(g, 438, 364 + k * 2.2, 462, 360 + k * 2.6, seed=4322 + k, w=0.6, k=0.5, over=0)
    if "globe" not in d:
        gx_, gy_ = 560, 316
        sk(g, Ell(gx_, 370, 20, 5), 0.6, 4330)
        line(g, gx_, 370, gx_, 350, seed=4331, w=2.4)
        sk(g, Circ(gx_, gy_, 32), 0.1, 4332, grad=(gx_ - 32, gx_ + 32, 0.5))
        sk(g, Rough(Ell(gx_ - 6, gy_ - 6, 16, 12), 4, 6, 4333), 0.45, 4334, line=False)
        sk(g, Rough(Ell(gx_ + 14, gy_ + 12, 10, 8), 3, 5, 4335), 0.45, 4336, line=False)
        outline(g, Circ(gx_, gy_, 38) - Circ(gx_, gy_, 35), 4337, 0.9)
    if "ink" not in d:
        sk(g, Union([Box(596, 352, 612, 370, 3), Box(600, 346, 608, 352)]), 0.75, 4340)
        line(g, 604, 348, 630, 300, seed=4341, w=1.4)
        sk(g, Poly([(630, 300), (640, 290), (632, 318), (620, 322)]), 0.1, 4342)
    if "cup" not in d:
        sk(g, Ell(476, 372, 18, 4), 0.2, 4350)
        sk(g, Union([Box(466, 350, 486, 370, 4)]), 0.1, 4351, grad=(466, 486, 0.35))
        outline(g, Ell(491, 360, 6, 6) - Ell(491, 360, 3, 3), 4352)
    # armchair with a sleeping cat (difference)
    ch = Union([Box(110, 360, 260, 470, 18), Box(96, 400, 130, 520, 10), Box(240, 400, 274, 520, 10)])
    sk(g, ch, 0.35, 4360, ang=70, grad=(96, 274, 0.25))
    sk(g, Box(126, 440, 248, 476, 6), 0.25, 4361, ang=5)
    for x in (110, 260):
        sk(g, Box(x - 6, 518, x + 6, 556, 2), 0.6, 4362 + x)
    if "cat" not in d:
        sk(g, Ell(190, 430, 46, 20), 0.3, 4365, grad=(150, 236, 0.4))
        sk(g, Circ(152, 420, 15), 0.3, 4366)
        for e in (-1, 1):
            sk(g, Poly([(152 + e * 8, 410), (152 + e * 11, 396), (152 + e * 2, 406)]), 0.35, 4367 + e)
        line(g, 232, 440, 252, 460, seed=4369, w=3.0, over=0)
        line(g, 145, 420, 151, 421, seed=4370, w=1.0, over=0)
    # potted plant (right floor)
    sk(g, Poly([(560, 560), (600, 560), (594, 510), (566, 510)]), 0.45, 4380, ang=88)
    for k in range(7):
        a = -2.6 + k * 0.36
        sk(g, Ell(580 + math.cos(a) * 34, 500 + math.sin(a) * 30, 16, 7), 0.25, 4381 + k, ang=30)


L1541_ELEMENTS = [
    E("pendulum", el(lambda g, m: (line(g, 558, 138, 558, 184, 4390, 1.2, 0.8, 0), sk(g, Circ(558, 188, 7), 0.4, 4391))), pivot=(558, 138),
      anim=dict(swingAngle=14, swingSpeed=0.5)),
    E("curtain", el(lambda g, m: outline(g, Poly([(226, 40), (292, 40), (300, 360), (230, 360)]), 4392, 0.8, 0.4)), pivot=(260, 40),
      anim=dict(swingAngle=1.5, swingSpeed=0.25)),
    E("dust", el(lambda g, m: [g.fill(Circ(x, y, 1.6), LEAD, alpha=0.4) for x, y in ((180, 160), (220, 220), (140, 260), (240, 120))]),
      anim=dict(driftVelocity=(4, -6), driftLength=24, driftFade=True)),
]

L1541_DIFFS = [
    ("vase", 796, 210, 0),
    ("picture", 400, 120, 0),
    ("globe", 560, 320, 0),
    ("ink", 612, 330, 0),
    ("cup", 478, 360, 0),
    ("cat", 190, 425, 0),
]


LEVELS = [
    ("Level1538", "素描·老街", make_bg3d(l1538_scene), L1538_ELEMENTS, L1538_DIFFS, 60, OPTS),
    ("Level1539", "素描·庭院", make_bg3d(l1539_scene), L1539_ELEMENTS, L1539_DIFFS, 60, OPTS),
    ("Level1540", "素描·火车站台", make_bg2d(l1540_scene), L1540_ELEMENTS, L1540_DIFFS, 60, OPTS),
    ("Level1541", "素描·书房", make_bg2d(l1541_scene), L1541_ELEMENTS, L1541_DIFFS, 60, OPTS),
]
