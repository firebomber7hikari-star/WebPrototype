# -*- coding: utf-8 -*-
"""Realistic-style night gothic levels (real.py + real_kit.py), all lit by moonlight with volumetric
god rays (Ctx.godrays: screen-space radial blur of the moonlit sky / window openings):
  Level1515 月下废堡   - a ruined castle on a crag, the full moon behind the broken keep, beams through its windows
  Level1516 废堡大厅   - the ruined great hall: moonbeams through tall lancet windows onto a dusty banquet
  Level1517 月夜墓地   - a graveyard in ground fog, moon behind a dead tree, chapel, mausoleum, iron fence
  Level1518 吸血鬼地穴 - a vaulted crypt: a vampire sits up in his coffin under a moonbeam from a barred window
  Level1519 吸血鬼伯爵 - the vampire count on a castle balcony, giant moon behind the bell tower, bats

Every background draws its scene twice when d is non-empty: first unmodified -> snapshot (the god-ray
source), then with the differences, so A and B get exactly the same beams.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from kit import drift_across
from real import (F32, Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el,
                  fbm, fbm1, grain_tex, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint,
                  tex, vgrad)
from real_kit import (bird_el, blades, bricks, crown, glint_el, mist_el, pine, planks, ridge, rock, rock_face, sky,
                      stars, treeline)

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)
MOONLIGHT = (180, 196, 240)


# =================================================================== shared helpers
def make_bg(scene, rays, bloom=(190, 16, 0.45), grade=None):
    """Background builder: unmodified pass -> snapshot (god-ray source) -> pass with differences -> rays."""
    def bg(c, d):
        g = Ctx(c)
        if d:
            scene(g, set())
            g.snapshot("s")
        scene(g, d)
        if not d:
            g.snapshot("s")
        for r in rays:
            g.godrays(**r)
        g.bloom(*bloom)
        g.grade(**(grade or dict(contrast=1.06, sat=1.0)))
        g.commit()
    return bg


def moon(g, x, y, r, col=(238, 238, 226), halo=(140, 160, 225), k=1.0, seed=7):
    g.glow(x, y, r * 9, halo, 0.22 * k, power=2.0)
    g.glow(x, y, r * 3.4, halo, 0.5 * k, power=1.6)
    sp = sphere_paint(x, y, r, col, amb=0.84, spec=0.0, wrap=0.8)

    def paint(X, Y):
        n = fbm(X, Y, r * 0.42, r * 0.36, 4, seed)
        m = smooth(0.5, 0.64, n)
        return sp(X, Y) * (1 - 0.2 * m)[..., None]
    g.fill(Circ(x, y, r), paint, feather=1.2)
    g.glow(x, y, r * 1.4, (225, 232, 255), 0.18 * k, power=1.3)


def arch(x0, x1, ys, y1, pointed=True):
    """Lancet (pointed) or round arch opening: springing line ys, bottom y1."""
    w = x1 - x0
    if pointed:
        top = Inter(Inter(Circ(x0, ys, w), Circ(x1, ys, w)), Box(x0, ys - w, x1, ys + 1))
    else:
        top = Inter(Ell((x0 + x1) / 2, ys, w / 2, w / 2), Box(x0, ys - w, x1, ys + 1))
    return Union([top, Box(x0, ys, x1, y1)])


def merlons(x0, x1, y, h, mw, gap):
    out, x = [], x0
    while x < x1 - 2:
        out.append(Box(x, y - h, min(x + mw, x1), y + 1))
        x += mw + gap
    return out


def ashlar(base, bw=26, bh=12, seed=0, mortar_k=0.55, vary=0.2):
    b = bricks(base, mortar=tuple(v * mortar_k for v in base[:3]), bw=bw, bh=bh, seed=seed, vary=vary)
    return tex(grain_tex(b, 0.08, seed), 0.16, 10, 8, 3, seed + 1)


def rim(g, shape, dx, dy, col=MOONLIGHT, k=0.55, feather=0.8):
    """Moonlit rim: the part of a shape not covered by itself shifted away from the light."""
    g.add(Diff(shape, Moved(shape, dx, dy)), col, k, feather=feather)


def stains(g, shape, k=0.35, sx=20, sy=60, seed=0):
    """Weathering streaks (darker vertical damp stains) inside a shape."""
    g.mul(shape, k, alpha=lambda X, Y: smooth(0.5, 0.75, fbm(X, Y, sx, sy, 3, seed)))


def bat(g, x, y, s, col=(16, 14, 20), up=0.0):
    """Flying bat silhouette (wingspan ~2s)."""
    for sg in (-1, 1):
        pts = [(x, y - 0.12 * s), (x + sg * 0.3 * s, y - (0.42 + up) * s), (x + sg * 0.62 * s, y - (0.5 + up) * s),
               (x + sg * 1.0 * s, y - (0.3 + up * 0.6) * s), (x + sg * 0.86 * s, y - 0.02 * s),
               (x + sg * 0.7 * s, y + 0.1 * s), (x + sg * 0.55 * s, y - 0.02 * s), (x + sg * 0.38 * s, y + 0.14 * s),
               (x + sg * 0.22 * s, y + 0.02 * s), (x, y + 0.14 * s)]
        g.fill(Poly(pts), col, feather=0.4)
    g.fill(Ell(x, y, 0.14 * s, 0.22 * s), col)
    for sg in (-1, 1):
        g.fill(Poly([(x + sg * 0.04 * s, y - 0.18 * s), (x + sg * 0.13 * s, y - 0.36 * s), (x + sg * 0.14 * s, y - 0.12 * s)]), col)


def bat_el(eid, x, y, s=10, speed=-26, phase=0.0, col=(16, 14, 20), bob=6):
    a = dict(drift_across(x - s, x + s, speed, start=phase), bobAmplitude=(0, bob), bobSpeed=0.35,
             stretch=(0, 0.55), scaleSpeed=3.2)
    return E(eid, el(lambda g, m: bat(g, x, y, s, col)), pivot=(x, y), daynight="tinted", anim=a)


def hanging_bat(g, x, y, s, col=(30, 24, 30), rim_col=None):
    """Bat hanging upside down from a rib at y: feet on top, wrapped wings, head with ears at the bottom."""
    for sg in (-1, 1):
        g.fill(Seg(x + sg * 0.08 * s, y, x + sg * 0.1 * s, y + 0.16 * s, 0.05 * s), col)
    wing = Poly([(x - 0.12 * s, y + 0.14 * s), (x + 0.12 * s, y + 0.14 * s), (x + 0.3 * s, y + 0.45 * s), (x + 0.26 * s, y + 0.62 * s),
                 (x + 0.3 * s, y + 0.74 * s), (x + 0.16 * s, y + 0.9 * s), (x - 0.16 * s, y + 0.9 * s), (x - 0.3 * s, y + 0.74 * s),
                 (x - 0.26 * s, y + 0.62 * s), (x - 0.3 * s, y + 0.45 * s)])
    g.fill(wing, sphere_paint(x - 0.06 * s, y + 0.5 * s, 0.32 * s, col, ry=0.45 * s, amb=0.45, spec=0.15, shin=10))
    for sg in (-1, 1):
        g.fill(Seg(x + sg * 0.04 * s, y + 0.2 * s, x + sg * 0.22 * s, y + 0.66 * s, 0.03 * s), mixc(col, (0, 0, 0), 0.5))
        g.fill(Seg(x + sg * 0.02 * s, y + 0.3 * s, x + sg * 0.12 * s, y + 0.86 * s, 0.025 * s), mixc(col, (0, 0, 0), 0.5))
    g.fill(Ell(x, y + 0.98 * s, 0.12 * s, 0.11 * s), mixc(col, (90, 70, 60), 0.25))
    for sg in (-1, 1):
        g.fill(Poly([(x + sg * 0.03 * s, y + 1.04 * s), (x + sg * 0.12 * s, y + 1.2 * s), (x + sg * 0.13 * s, y + 1.0 * s)]), col)
    g.fill(Circ(x - 0.05 * s, y + 0.98 * s, 0.022 * s), (230, 140, 90))
    g.fill(Circ(x + 0.05 * s, y + 0.98 * s, 0.022 * s), (230, 140, 90))
    if rim_col is not None:
        rim(g, wing, 0.05 * s, 0, col=rim_col, k=0.4)


def dead_tree(g, x, base, h, seed=0, col=(26, 22, 26), lean=0.0, spread=1.0, w=None, light_dir=None, depth=6,
              skip=()):
    """Gnarled leafless tree from recursive tapered segments; returns twig tip points."""
    rnd = random.Random(seed)
    w = w or h * 0.075
    tips = []
    paint = col if light_dir is None else None

    def seg(x0, y0, x1, y1, w0, w1):
        if paint is not None:
            g.fill(Seg(x0, y0, x1, y1, w0, w1), col)
        else:
            lo, hi = min(x0, x1) - w0, max(x0, x1) + w0
            g.fill(Seg(x0, y0, x1, y1, w0, w1), tex(light_x(col, lo, hi, *((1.5, 0.8) if light_dir < 0 else (0.8, 1.5))),
                                                   0.25, 1.5, 6, 3, seed))

    def branch(x0, y0, ang, ln, wd, dep, idx):
        n = 3
        px, py, a = x0, y0, ang
        for i in range(n):
            a += rnd.uniform(-0.28, 0.28)
            nx, ny = px + math.cos(a) * ln / n, py - math.sin(a) * ln / n
            w0 = wd * (1 - i / n * 0.35)
            seg(px, py, nx, ny, w0, w0 * 0.82)
            px, py = nx, ny
        if dep <= 0 or wd < 1.1:
            tips.append((px, py))
            return
        kids = 2 if rnd.random() < 0.65 else 3
        for k in range(kids):
            if (dep, idx, k) in skip:
                continue
            da = rnd.uniform(0.3, 0.75) * spread * (1 if k % 2 == 0 else -1) + rnd.uniform(-0.1, 0.1)
            branch(px, py, a + da, ln * rnd.uniform(0.62, 0.8), wd * rnd.uniform(0.55, 0.7), dep - 1, idx * 3 + k)
    # trunk with flared roots
    g.fill(Poly([(x - w * 1.9, base + 2), (x - w * 0.5, base - h * 0.12), (x + w * 0.5, base - h * 0.12), (x + w * 2.1, base + 2)]),
           col if light_dir is None else tex(light_x(col, x - w * 2, x + w * 2, 1.3, 0.8), 0.2, 2, 5))
    branch(x, base, math.pi / 2 + lean, h * 0.42, w, depth, 0)
    return tips


def tombstone(g, x, base, w, h, kind="round", col=(96, 98, 108), seed=0, lean=0.0, lit=-1, moss=True, shade=0.7):
    """Gravestone (round / cross / celtic / obelisk / slab), lit by the moon from side `lit` (-1 left, 1 right)."""
    hw = w / 2
    if kind == "round":
        s = Union([Box(x - hw, base - h + hw, x + hw, base), Inter(Circ(x, base - h + hw, hw), Box(x - hw, base - h - 1, x + hw, base - h + hw + 1))])
    elif kind == "cross":
        aw = w * 0.32
        s = Union([Box(x - aw / 2, base - h, x + aw / 2, base), Box(x - hw, base - h * 0.78, x + hw, base - h * 0.78 + aw)])
    elif kind == "celtic":
        aw = w * 0.28
        cy = base - h * 0.74
        s = Union([Box(x - aw / 2, base - h, x + aw / 2, base), Box(x - hw, cy - aw / 2, x + hw, cy + aw / 2),
                   Circ(x, cy, hw * 0.62) - Circ(x, cy, hw * 0.42), Box(x - hw * 0.62, base - h * 0.2, x + hw * 0.62, base)])
    elif kind == "obelisk":
        s = Union([Poly([(x - hw * 0.55, base - h * 0.2), (x - hw * 0.35, base - h + hw * 0.6), (x, base - h),
                         (x + hw * 0.35, base - h + hw * 0.6), (x + hw * 0.55, base - h * 0.2)]), Box(x - hw, base - h * 0.22, x + hw, base)])
    else:   # slab with a peaked top
        s = Poly([(x - hw, base), (x - hw, base - h * 0.82), (x, base - h), (x + hw, base - h * 0.82), (x + hw, base)])
    if lean:
        s = _sheared(s, x, base, lean)
    g.mul(Ell(x - lit * w * 0.5, base + 2, w * 1.0, 5 + w * 0.06), 0.55, feather=6)
    k0, k1 = (1.25, shade) if lit < 0 else (shade, 1.25)
    p = tex(grain_tex(light_x(col, x - hw, x + hw, k0, k1), 0.12, seed), 0.22, 4, 5, 4, seed + 1)
    if moss:
        mc = C((70, 84, 60))

        def p2(X, Y, p=p):
            out = p(X, Y)
            m = smooth(0.6, 0.72, fbm(X, Y, 3, 3, 3, seed + 3) + (Y - (base - h)) / h * 0.22)
            return out + (mc * (out.mean(-1, keepdims=True) / 120.0) - out) * (m * 0.38)[..., None]
        g.fill(s, p2)
    else:
        g.fill(s, p)
    rim(g, s, -lit * 2.2, 0.6, k=0.4)
    g.mul(s, 0.5, alpha=lambda X, Y: smooth(base - h * 0.25, base, Y))
    return s


class _sheared:
    """Shape sheared horizontally about the base line (leaning gravestone)."""

    def __init__(self, s, x, base, k):
        self.s, self.x, self.base, self.k = s, x, base, k

    def bbox(self):
        b = self.s.bbox()
        dx = (self.base - b[1]) * self.k
        return (b[0] + min(0, dx) - 2, b[1], b[2] + max(0, dx) + 2, b[3])

    def sdf(self, X, Y):
        return self.s.sdf(X - (self.base - Y) * self.k, Y)

    def __or__(self, o):
        return Union([self, o])

    def __sub__(self, o):
        return Diff(self, o)

    def __and__(self, o):
        return Inter(self, o)


def fog_band(g, y0, ym, y1, col, a, noise=0.5, sx=150, sy=14, seed=0):
    """Soft fog layer: rises from 0 at y0 to a at ym and fades back to 0 at y1 (no hard edges)."""
    g.fog(y0, ym, col, 0.0, a, noise=noise, sx=sx, sy=sy, seed=seed)
    g.fog(ym, y1, col, a, 0.0, noise=noise, sx=sx, sy=sy, seed=seed)


def twigs(g, pts, w0, w1, col, seed=0, n=2):
    """Hand-placed gnarled branch along a polyline (tapering), sprouting a few short twigs."""
    rnd = random.Random(seed)
    m = len(pts) - 1
    for i in range(m):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        wa, wb = w0 + (w1 - w0) * i / m, w0 + (w1 - w0) * (i + 1) / m
        g.fill(Seg(x0, y0, x1, y1, wa, wb), col)
        for _ in range(n):
            t = rnd.uniform(0.2, 0.9)
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            a = math.atan2(y1 - y0, x1 - x0) + rnd.choice((-1, 1)) * rnd.uniform(0.5, 1.1)
            ln = rnd.uniform(12, 30) * (0.5 + wa / max(w0, 1))
            qx, qy = px + math.cos(a) * ln, py + math.sin(a) * ln
            g.fill(Seg(px, py, qx, qy, max(1.0, wa * 0.45), 0.6), col)
            b = a + rnd.uniform(-0.6, 0.6)
            g.fill(Seg(qx, qy, qx + math.cos(b) * ln * 0.5, qy + math.sin(b) * ln * 0.5, 0.9, 0.4), col)


def moon_receive(mx, my, mr, floor=0.12):
    """Rays-receive mask that keeps the moon disc itself from blowing out."""
    return lambda X, Y: floor + (1 - floor) * smooth(mr * 0.7, mr * 2.8, np.hypot(X - mx, Y - my))


def candle(g, x, base, h, w=7, col=(232, 222, 196), lit=True):
    g.fill(Box(x - w / 2, base - h, x + w / 2, base, 1.2), cyl_paint(x, w / 2, col, amb=0.5, spec=0.12))
    g.fill(Ell(x + w * 0.3, base - h + 3, w * 0.22, 4), mixc(col, (255, 255, 255), 0.2))
    g.fill(Seg(x, base - h, x, base - h - 3, 1.0), (30, 26, 22))
    if lit:
        g.glow(x, base - h - 6, 26, (255, 160, 70), 0.35)


def flame(g, x, y, s=1.0):
    g.glow(x, y - 5 * s, 9 * s, (255, 170, 80), 0.6)
    sh = Union([Ell(x, y - 3 * s, 2.8 * s, 3.6 * s), Poly([(x - 2.7 * s, y - 4 * s), (x, y - 13 * s), (x + 2.7 * s, y - 4 * s)])])
    g.fill(sh, lgrad(x, y - 13 * s, x, y, [(0, (255, 140, 40)), (0.5, (255, 214, 120)), (1, (255, 250, 228))]), feather=0.7)


def flame_el(eid, x, y, s=1.0, phase=0.0):
    return E(eid, el(lambda g, m: flame(g, x, y, s)), pivot=(x, y), daynight="untinted",
             anim=dict(stretch=(0.06, 0.22), scaleSpeed=1.7 + phase, pulse=0.05, phase=phase))


def beam_el(eid, x0, y0, x1, y1, w0, w1, col=(196, 210, 250), k=0.16, speed=0.12, phase=0.0):
    """A soft moonbeam shaft that slowly breathes (normal-over fill so it only brightens)."""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    pts = [(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2),
           (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)]

    def alpha(X, Y):
        t = np.clip(((X - x0) * dx + (Y - y0) * dy) / (ln * ln), 0, 1)
        return k * (1 - t) ** 1.3 * smooth(0.0, 0.08, t)

    return E(eid, el(lambda g, m: g.fill(Poly(pts), col, alpha=alpha, feather=12)), daynight="untinted",
             anim=dict(twinkle=0.75, twinkleSpeed=speed, phase=phase))


def motes_el(eid, pts, col=(220, 230, 255), r=2.0, vx=3, vy=-5, length=22, phase=0.0):
    """Dust specks floating in a moonbeam."""
    return E(eid, el(lambda g, m: [g.glow(x, y, r, col, 0.9, power=1.1) for x, y in pts]), daynight="untinted",
             anim=dict(driftVelocity=(vx, vy), driftLength=length, driftFade=True, phase=phase))


def cobweb(g, x, y, r, quad=(1, 1), col=(200, 205, 220), k=0.35):
    """Corner cobweb: radial threads + sagging rings in the quadrant (sx, sy)."""
    sx, sy = quad
    angs = [i * (math.pi / 2) / 6 for i in range(7)]
    for a in angs:
        g.add(Seg(x, y, x + sx * math.cos(a) * r, y + sy * math.sin(a) * r, 0.7), col, k)
    for f in (0.3, 0.5, 0.7, 0.9):
        for a0, a1 in zip(angs[:-1], angs[1:]):
            p0 = (x + sx * math.cos(a0) * r * f, y + sy * math.sin(a0) * r * f)
            p1 = (x + sx * math.cos(a1) * r * f, y + sy * math.sin(a1) * r * f)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            mx -= sx * 2 * f
            my -= sy * 2 * f
            g.add(Seg(p0[0], p0[1], mx, my, 0.6), col, k * 0.8)
            g.add(Seg(mx, my, p1[0], p1[1], 0.6), col, k * 0.8)


def vampire(g, x, base, h, cape_in=(140, 18, 30), cape_out=(16, 14, 22), suit=(24, 22, 30), skin=(212, 212, 204),
            hair=(12, 10, 14), medal=(196, 26, 40), rose=None, rim_dx=2.4, wind=1.0, arm_up=True):
    """Original vampire count, 3/4 view facing left; moon rim light from the left. Returns key points."""
    k = h / 300.0
    sx = lambda v: x + v * k
    sy = lambda v: base - v * k
    # cape (back), flaring right with the wind
    cape = Poly([(sx(-34), sy(238)), (sx(40), sy(240)), (sx(70 + 40 * wind), sy(150)), (sx(108 + 60 * wind), sy(40)),
                 (sx(96 + 60 * wind), sy(4)), (sx(40), sy(0)), (sx(-20), sy(2)), (sx(-62), sy(6)), (sx(-58), sy(120)),
                 (sx(-46), sy(200))])

    def cape_paint(X, Y):
        fold = 0.72 + 0.28 * np.sin((X - x) * 0.11 / k + (Y - base) * 0.02 / k) * np.sin((X - x) * 0.05 / k)
        return C(cape_out) * (fold * (0.9 + 0.2 * fbm(X, Y, 6, 30, 3, 31)))[..., None]
    g.fill(cape, cape_paint)
    lining = Poly([(sx(-58), sy(8)), (sx(-62), sy(6)), (sx(-58), sy(120)), (sx(-46), sy(200)), (sx(-34), sy(238)),
                   (sx(-24), sy(232)), (sx(-36), sy(190)), (sx(-44), sy(110)), (sx(-42), sy(10))])
    g.fill(lining, light_x(cape_in, sx(-62), sx(-36), 1.15, 0.6))
    lining2 = Poly([(sx(96 + 60 * wind), sy(4)), (sx(108 + 60 * wind), sy(40)), (sx(112 + 60 * wind), sy(30)), (sx(104 + 60 * wind), sy(2))])
    g.fill(lining2, mixc(cape_in, (0, 0, 0), 0.35))
    rim(g, cape, rim_dx, 0, k=0.5)
    # legs and shoes
    for lx, fx in ((-14, -24), (12, 4)):
        g.fill(Seg(sx(lx), sy(118), sx(fx + 4), sy(10), 20 * k, 15 * k), light_x(suit, sx(lx - 12), sx(lx + 12), 1.2, 0.6))
        g.fill(Ell(sx(fx - 2), sy(6), 15 * k, 6 * k), sphere_paint(sx(fx - 6), sy(9), 15 * k, (20, 18, 22), ry=6 * k, spec=0.6, shin=30))
    # coat torso with tails
    coat = Poly([(sx(-30), sy(236)), (sx(30), sy(238)), (sx(34), sy(150)), (sx(30), sy(60)), (sx(10), sy(80)),
                 (sx(0), sy(124)), (sx(-12), sy(90)), (sx(-34), sy(64)), (sx(-36), sy(150))])
    g.fill(coat, tex(light_x(suit, sx(-36), sx(34), 1.35, 0.6), 0.08, 3, 6))
    g.fill(Poly([(sx(-10), sy(232)), (sx(10), sy(232)), (sx(8), sy(140)), (sx(-8), sy(140))]), light_x((120, 20, 30), sx(-10), sx(10), 1.1, 0.7))
    g.fill(Poly([(sx(-9), sy(240)), (sx(6), sy(240)), (sx(2), sy(206)), (sx(-6), sy(206))]), (226, 226, 220))
    g.fill(Rough(Ell(sx(-2), sy(214), 10 * k, 13 * k), 1.4 * k, 3 * k, 33), light_x((236, 236, 230), sx(-12), sx(8), 1.1, 0.75))
    rim(g, coat, rim_dx, 0, k=0.2)
    # medallion
    g.fill(Seg(sx(-14), sy(232), sx(-2), sy(186), 1.6 * k), (200, 170, 90))
    g.fill(Seg(sx(12), sy(232), sx(-2), sy(186), 1.6 * k), (170, 140, 70))
    g.fill(Circ(sx(-2), sy(178), 13 * k), sphere_paint(sx(-5), sy(181), 13 * k, (210, 176, 90), amb=0.4, spec=0.7))
    g.fill(Circ(sx(-2), sy(178), 9 * k), sphere_paint(sx(-5), sy(181), 9 * k, medal, amb=0.45, spec=0.9, shin=40))
    # front arm: raised to the chest (holding a rose) or down
    if arm_up:
        g.fill(Seg(sx(-28), sy(226), sx(-44), sy(170), 15 * k, 13 * k), light_x(suit, sx(-52), sx(-20), 1.4, 0.7))
        g.fill(Seg(sx(-44), sy(170), sx(-24), sy(150), 13 * k, 11 * k), light_x(suit, sx(-52), sx(-16), 1.4, 0.7))
        g.fill(Seg(sx(-24), sy(156), sx(-22), sy(146), 5 * k, 6 * k), (226, 222, 214))
        hand = (sx(-16), sy(150))
        g.fill(Ell(hand[0] + 4 * k, hand[1], 7 * k, 6 * k), light_x(skin, hand[0] - 4 * k, hand[0] + 12 * k, 1.15, 0.75))
        if rose is not None:
            g.fill(Seg(hand[0] + 4 * k, hand[1], hand[0] - 14 * k, hand[1] - 40 * k, 1.8 * k), (40, 80, 40))
            g.fill(Ell(hand[0] - 8 * k, hand[1] - 22 * k, 5 * k, 2.6 * k), (50, 96, 46))
            rx, ry = hand[0] - 15 * k, hand[1] - 46 * k
            g.fill(Rough(Circ(rx, ry, 11 * k), 2 * k, 3 * k, 35), sphere_paint(rx - 3 * k, ry - 3 * k, 11 * k, rose, amb=0.35, spec=0.2))
            for a in (0.4, 2.2, 4.0):
                g.fill(Seg(rx + math.cos(a) * 3 * k, ry + math.sin(a) * 3 * k, rx + math.cos(a + 1.4) * 7.5 * k,
                           ry + math.sin(a + 1.4) * 7.5 * k, 1.4 * k), mixc(rose, (0, 0, 0), 0.4))
    else:
        g.fill(Seg(sx(-28), sy(226), sx(-38), sy(140), 15 * k, 12 * k), light_x(suit, sx(-46), sx(-20), 1.4, 0.7))
        g.fill(Ell(sx(-39), sy(134), 6 * k, 8 * k), light_x(skin, sx(-46), sx(-32), 1.15, 0.75))
    # high collar behind the head
    for sg in (-1, 1):
        pts = [(sx(sg * 36), sy(234)), (sx(sg * 8), sy(240)), (sx(sg * 20), sy(268)), (sx(sg * 44), sy(326)), (sx(sg * 54), sy(282))]
        inn = [(sx(sg * 30), sy(240)), (sx(sg * 14), sy(244)), (sx(sg * 24), sy(268)), (sx(sg * 42), sy(312)), (sx(sg * 46), sy(282))]
        sh = Poly(pts)
        g.fill(sh, cape_out)
        g.fill(Poly(inn), light_y(cape_in, sy(320), sy(240), 1.1, 0.6))
        rim(g, sh, rim_dx, 0, k=0.4)
    # neck + head (3/4 to the left)
    g.fill(Box(sx(-7), sy(252), sx(7), sy(234), 3 * k), light_x(skin, sx(-7), sx(7), 1.0, 0.65))
    hx, hy = sx(-4), sy(274)
    head = Union([Ell(hx, hy, 16.5 * k, 21 * k), Poly([(hx - 14 * k, hy - 2 * k), (hx - 19 * k, hy + 4 * k), (hx - 13 * k, hy + 6 * k)])])
    g.fill(head, sphere_paint(hx - 5 * k, hy - 3 * k, 17 * k, skin, ry=20 * k, amb=0.42, spec=0.12, light=(-0.8, -0.3, 0.5)))
    g.fill(Seg(hx - 4 * k, hy + 12 * k, hx - 13 * k, hy + 14 * k, 2 * k), (150, 120, 120))
    for ex in (-10, -1):
        g.fill(Ell(hx + ex * k, hy - 2 * k, 2.6 * k, 1.5 * k), (110, 20, 26))
        g.fill(Circ(hx + ex * k - 0.6 * k, hy - 2 * k, 0.8 * k), (255, 90, 80))
    g.fill(Seg(hx - 14 * k, hy - 7 * k, hx - 6 * k, hy - 6 * k, 1.6 * k), hair)
    g.fill(Seg(hx - 3 * k, hy - 6 * k, hx + 4 * k, hy - 7 * k, 1.6 * k), hair)
    g.fill(Poly([(hx + 10 * k, hy - 4 * k), (hx + 20 * k, hy - 12 * k), (hx + 15 * k, hy + 4 * k)]), light_x(skin, hx + 10 * k, hx + 20 * k, 0.9, 0.6))
    hair_s = Poly([(hx - 14 * k, hy - 10 * k), (hx - 6 * k, hy - 8 * k), (hx - 3 * k, hy - 4 * k), (hx + 0 * k, hy - 9 * k),
                   (hx + 12 * k, hy - 6 * k), (hx + 16 * k, hy + 2 * k), (hx + 17 * k, hy - 12 * k), (hx + 8 * k, hy - 20 * k),
                   (hx - 6 * k, hy - 21 * k), (hx - 14 * k, hy - 16 * k)])
    g.fill(hair_s, tex(lambda X, Y: C(hair) * (1 + 0.6 * np.clip(np.sin((Y - hy) * 1.4 / k + (X - hx) * 0.3 / k), 0, 1))[..., None], 0.1, 2, 2))
    rim(g, head, rim_dx * 0.8, 0, k=0.35)
    rim(g, hair_s, rim_dx * 0.8, 1, k=0.45)
    return dict(head=(hx, hy), chest=(sx(-2), sy(180)))


# =================================================================== Level 1515 ruined castle under the moon
M15 = (600, 176, 46)


def l1515_crag(x):
    return 338 + ((x - 610) / 300.0) ** 2 * 70 + (fbm1(x, 36, 4, 1506) - 0.5) * 26


def l1515_scene(g, d):
    mx, my, mr = M15
    sky(g, [(0, (5, 8, 22)), (170, (16, 24, 54)), (320, (40, 50, 86)), (430, (58, 64, 96))])
    stars(g, 120, 300, seed=1501)
    moon(g, mx, my, mr)
    from real_kit import cloud_layer
    cloud_layer(g, 40, 140, (96, 108, 150), (34, 40, 66), cover=0.36, sx=210, sy=24, seed=1502, alpha=0.75)
    cloud_layer(g, 186, 236, (150, 160, 200), (60, 66, 100), cover=0.3, sx=150, sy=10, seed=1503, alpha=0.55)
    ridge(g, 410, 120, 260, 1504, (30, 36, 62), light=False, haze=((52, 60, 96), 0.55, 0.25), rock_tex=0.08)
    treeline(g, 432, 36, 10, 1505, (12, 16, 26), light=0.0, haze=((46, 54, 86), 0.45, 0.1))
    fog_band(g, 360, 420, 470, (70, 80, 120), 0.5, noise=0.45, sx=160, sy=18, seed=1509)
    # crag
    crag = Under(l1515_crag, 210, W + 20, H + 20)
    g.fill(crag, rock_face((44, 46, 60), seed=1507, sx=60, sy=30, bump=2.4))
    g.mul(crag, 0.45, alpha=lambda X, Y: smooth(330, 450, Y))
    rim(g, crag, 0, 3, k=0.12)
    # left curtain wall + broken gap, gate with portcullis
    wall = Union([Box(410, 268, 548, 372)] + merlons(410, 548, 268, 12, 12, 8))
    wall = Diff(wall, Poly([(446, 262), (486, 262), (476, 300), (462, 304)]))
    gate = arch(468, 512, 316, 372, pointed=False)
    g.fill(Box(468, 290, 512, 372), vgrad([(290, (90, 102, 140)), (372, (60, 66, 96))]))     # moonlit courtyard
    g.fog(320, 372, (130, 140, 180), 0.0, 0.5, x0=468, x1=512)
    wall = Diff(wall, gate)
    g.fill(wall, light_y(ashlar((60, 62, 78), 18, 9, 1510), 268, 372, 1.0, 0.7))
    stains(g, wall, 0.3, seed=1511)
    rim(g, wall, 0, 2.5, k=0.35)
    if "gate" not in d:
        bars = [Box(x, 318, x + 2.6, 372) for x in range(470, 511, 7)] + [Box(468, y, 512, y + 2.4) for y in range(326, 372, 9)]
        g.fill(Inter(Union(bars), gate), (24, 22, 26))
        g.add(Inter(Union([Box(x, 318, x + 1.0, 372) for x in range(470, 511, 7)]), gate), MOONLIGHT, 0.3)
    # left tower
    lt = Union([Box(356, 226, 424, 380)] + merlons(352, 428, 226, 13, 13, 8))
    lt = Diff(lt, Poly([(400, 214), (430, 214), (428, 244), (412, 236)]))
    g.fill(lt, ashlar((62, 64, 80), 18, 9, 1512))
    g.fill(lt, (0, 0, 0), alpha=lambda X, Y: 0.35 * smooth(356, 424, X))
    for wy in (262, 312):
        g.fill(arch(384, 396, wy, wy + 18), (10, 10, 16))
    stains(g, lt, 0.3, seed=1513)
    rim(g, lt, -1.5, 2, k=0.22)
    if "banner" not in d:
        g.fill(Seg(372, 214, 372, 168, 2.2), (40, 34, 30))
        flag = Rough(Poly([(373, 170), (408, 176), (402, 186), (410, 196), (373, 196)]), 1.6, 4, 1514)
        g.fill(flag, tex(light_y((120, 26, 34), 170, 196, 1.1, 0.7), 0.15, 3, 3))
        rim(g, flag, 0, 2, k=0.3)
    # keep (in front of the moon) with lancet windows and a breached corner
    keep = Union([Box(548, 108, 652, 352)] + merlons(544, 656, 108, 14, 15, 9))
    keep = Diff(keep, Poly([(626, 96), (662, 96), (662, 168), (648, 150), (640, 126)]))
    for x0 in (566, 610):
        keep = Diff(keep, arch(x0, x0 + 24, 160, 214))
    keep = Diff(keep, arch(590, 610, 262, 300))
    g.fill(keep, ashlar((58, 60, 76), 20, 10, 1515))
    g.fill(keep, (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.2 * smooth(548, 652, X))
    stains(g, keep, 0.35, sx=16, sy=70, seed=1516)
    rim(g, keep, 0, 2.5, k=0.55)
    g.fill(arch(590, 610, 262, 300), (90, 100, 140))       # sees through to the moonlit sky behind (opening)
    g.fill(Box(578, 214, 622, 220), (40, 40, 52))           # sill
    # right wall + round tower with the skeleton of a collapsed roof
    rw = Union([Box(652, 250, 762, 368)] + merlons(652, 762, 250, 11, 12, 8))
    rw = Diff(rw, Poly([(690, 244), (736, 244), (726, 286), (700, 280)]))
    g.fill(rw, light_y(ashlar((56, 58, 74), 18, 9, 1517), 250, 368, 1.0, 0.7))
    rim(g, rw, 0, 2.5, k=0.3)
    rt = Box(760, 200, 826, 396)
    g.fill(rt, tex(cyl_paint(793, 33, (66, 68, 86), amb=0.5, spec=0.05), 0.12, 8, 6, 3, 1518))
    g.fill(rt, lambda X, Y: ashlar((66, 68, 86), 16, 9, 1519)(X, Y) * (0.55 + 0.6 * np.sqrt(np.clip(1 - ((X - 805) / 40) ** 2, 0, 1)))[..., None])
    stains(g, rt, 0.3, seed=1520)
    for k in range(-3, 4):
        g.fill(Seg(793 + k * 10, 200, 793 + k * 3, 150 + abs(k) * 6, 2.4 - abs(k) * 0.2), (30, 26, 26))
    g.fill(Seg(760, 200, 826, 200, 3), (34, 30, 30))
    g.fill(Seg(774, 176, 812, 176, 2), (34, 30, 30))
    rim(g, rt, 0, 2, k=0.3)
    win = arch(784, 802, 256, 286)
    if "window" in d:
        g.fill(win, rgrad(793, 276, 22, [(0, (255, 214, 140)), (1, (210, 120, 50))]))
        g.glow(793, 274, 26, (255, 170, 80), 0.4)
    else:
        g.fill(win, (12, 12, 18))
    g.fill(arch(786, 800, 322, 344), (12, 12, 18))
    # foreground slope + path
    def fg(x):
        return 452 + 30 * np.sin(x * 0.008 + 0.6) + (fbm1(x, 50, 3, 1521) - 0.5) * 20
    gnd = Under(fg, -20, W + 20, H + 20)
    g.fill(gnd, tex(vgrad([(430, (46, 48, 58)), (600, (24, 24, 30))]), 0.3, 5, 4, 4, 1522))
    path = Rough(Poly([(380, H + 6), (560, H + 6), (520, 520), (530, 470), (500, 456), (480, 472), (460, 530)]), 5, 12, 1523)
    g.fill(path, grain_tex(vgrad([(456, (78, 80, 96)), (600, (54, 52, 60))]), 0.14, 1524), feather=1.5)
    blades(g, 470, 600, (70, 72, 80), n=220, seed=1525, hmax=22)
    for x, y, rx, ry, s in ((300, 560, 40, 20, 1526), (640, 520, 30, 16, 1527), (860, 580, 50, 24, 1528), (220, 470, 24, 12, 1529)):
        rock(g, x, y, rx, ry, (70, 72, 86), seed=s)
    # broken cart wheel leaning on the rock
    if "wheel" not in d:
        wx, wy, wr = 640, 492, 26
        g.fill(Circ(wx, wy, wr) - Circ(wx, wy, wr - 5), tex(light_x((92, 70, 54), wx - wr, wx + wr, 1.3, 0.6), 0.2, 2, 5))
        for a in range(0, 360, 45):
            if a == 135:
                continue
            g.fill(Seg(wx, wy, wx + math.cos(math.radians(a)) * (wr - 4), wy + math.sin(math.radians(a)) * (wr - 4), 3), (80, 60, 46))
        g.fill(Circ(wx, wy, 5), (60, 46, 36))
    # signpost (right)
    g.fill(Box(776, 430, 784, 560), tex(light_x((80, 64, 50), 776, 784, 1.3, 0.6), 0.2, 1.5, 6))
    g.mul(Ell(786, 560, 26, 5), 0.5, feather=5)
    g.fill(Poly([(724, 444), (796, 438), (798, 458), (726, 462)]), planks("h", (104, 82, 60), seed=1530, width=7, x_or_y0=438))
    if "sign" not in d:
        g.fill(Poly([(770, 474), (846, 482), (858, 492), (844, 500), (768, 494)]), planks("h", (98, 76, 56), seed=1531, width=7, x_or_y0=474))
    # lantern on a crooked post (left)
    g.fill(Seg(70, 600, 76, 410, 7, 6), tex(light_x((70, 56, 44), 66, 80, 1.3, 0.6), 0.2, 1.5, 6))
    g.fill(Seg(74, 416, 108, 412, 4), (60, 48, 40))
    if "lantern" not in d:
        lx, ly = 104, 440
        g.fill(Seg(lx, 412, lx, 422, 1.4), (30, 30, 30))
        g.glow(lx, ly, 70, (255, 170, 80), 0.35)
        g.fill(Box(lx - 9, ly - 16, lx + 9, ly + 12, 2), (255, 200, 120))
        g.fill(Box(lx - 11, ly - 20, lx + 11, ly - 16, 1.5), (40, 36, 34))
        g.fill(Box(lx - 11, ly + 12, lx + 11, ly + 16, 1.5), (40, 36, 34))
        for bx in (-10, 9):
            g.fill(Box(lx + bx, ly - 16, lx + bx + 1.6, ly + 12), (40, 36, 34))
    # dead tree with crows (left foreground, silhouetted against the sky)
    dead_tree(g, 160, 600, 470, seed=1532, col=(20, 18, 22), lean=0.08, spread=1.05, depth=5)
    g.fill(Seg(140, 186, 262, 176, 5, 2.5), (20, 18, 22))
    crows = [(166, 183), (206, 180), (244, 177)]
    for i, (cx, cy) in enumerate(crows):
        if i == 1 and "crow" in d:
            continue
        g.fill(Ell(cx, cy - 11, 8, 11.5), (14, 12, 16))
        g.fill(Circ(cx - 5, cy - 24, 6), (14, 12, 16))
        g.fill(Poly([(cx - 10, cy - 26), (cx - 19, cy - 23), (cx - 10, cy - 21)]), (34, 30, 32))
        g.fill(Poly([(cx + 5, cy - 8), (cx + 19, cy - 1), (cx + 5, cy - 2)]), (14, 12, 16))
        for lx in (-2, 2):
            g.fill(Seg(cx + lx, cy - 2, cx + lx, cy + 2, 1.2), (30, 26, 26))
        rim(g, Ell(cx, cy - 11, 8, 11.5), 0, 1.5, k=0.3)
    g.fog(440, 600, (60, 66, 96), 0.15, 0.0)


L1515_RAYS = [dict(lx=M15[0], ly=M15[1], col=(170, 186, 232), k=1.7, region=Box(-2, -2, W + 2, 330), threshold=92,
                   soft=70, density=0.92, decay=0.978, samples=80, receive=moon_receive(*M15, floor=0.5))]

L1515_ELEMENTS = [
    bat_el("bat1", 300, 96, s=11, speed=34),
    bat_el("bat2", 330, 112, s=8, speed=34, phase=0.05),
    bat_el("bat3", 700, 78, s=9, speed=-28, phase=0.4),
    mist_el("mist1", 300, 410, 140, 10, (90, 100, 140), alpha=0.45, length=60, seed=11),
    mist_el("mist2", 700, 420, 160, 10, (90, 100, 140), alpha=0.4, length=50, seed=12),
    beam_el("beam1", 578, 196, 470, 470, 18, 90, phase=0.0),
    beam_el("beam2", 622, 196, 700, 470, 18, 80, phase=0.5, speed=0.1),
    glint_el("twinkle", [(60, 40), (300, 30), (840, 60), (460, 110), (880, 150)], col=(240, 240, 255), r=3, speed=0.6),
]

L1515_DIFFS = [
    ("crow", 204, 170, 0),
    ("banner", 390, 186, 0),
    ("window", 793, 272, 0),
    ("gate", 490, 344, 0),
    ("lantern", 104, 440, 0),
    ("wheel", 640, 492, 0),
    ("sign", 812, 488, 0),
]


# =================================================================== Level 1516 ruined great hall
VP16 = (450, 230)
L16 = (100, -320)                   # the moon, high outside (upper left, behind the back wall)
WIN16 = (250, 450, 650)
WY16 = (150, 340)                   # springing line / sill of the lancet windows


def l16_wall_y(x, top=True):
    """Left / right side-wall top & bottom edge at screen x (converging to VP16)."""
    if x < 450:
        return 30 - (130 - x) * 200 / 320 if top else 400 + (130 - x) * 170 / 320
    return 30 - (x - 770) * 200 / 320 if top else 400 + (x - 770) * 170 / 320


def l16_window(c):
    return arch(c - 42, c + 42, WY16[0], WY16[1])


def l16_pool(pts):
    """Project points of a window opening onto the floor along the moonbeam (screen-space, from L16)."""
    out = []
    for px, py in pts:
        h = 400 - py
        fy = 400 + h * 0.42
        s = (fy - py) / (py - L16[1])
        out.append((px + (px - L16[0]) * s, fy))
    return out


def l16_outline(c):
    x0, x1, ys, yb = c - 42, c + 42, WY16[0], WY16[1]
    w = x1 - x0
    pts = [(x0, yb), (x0, ys)]
    for i in range(1, 12):                      # left arc (centre x1) up to the apex
        a = math.pi - i / 12 * (math.pi / 3)
        pts.append((x1 + w * math.cos(a), ys - w * math.sin(a)))
    pts.append((c, ys - w * math.sqrt(3) / 2))
    for i in range(11, 0, -1):
        a = i / 12 * (math.pi / 3)
        pts.append((x0 + w * math.cos(a), ys - w * math.sin(a)))
    pts += [(x1, ys), (x1, yb)]
    return pts


def persp_floor(vp, back_y, base, tile=46, depth=0.2, seed=0):
    """Flagstone floor paint in one-point perspective (vanishing point vp, floor meets back wall at back_y)."""
    def f(X, Y):
        z = (back_y - vp[1]) / np.maximum(Y - vp[1], 1)
        fx = (X - vp[0]) * z / tile
        fd = (1 / z) / depth
        ix, iy = np.floor(fx), np.floor(fd)
        jx, jy = fx - ix, fd - iy
        t = 0.82 + 0.3 * np.abs(np.sin(ix * 12.9898 + iy * 78.233) * 43758.5453 % 1.0)
        jw = 0.05 / np.maximum(z, 0.4)
        joint = smooth(0, jw, jx) * smooth(1, 1 - jw, jx) * smooth(0, jw * 1.4, jy) * smooth(1, 1 - jw * 1.4, jy)
        n = fbm(X, Y, 5, 3, 3, seed)
        k = t * (0.85 + 0.3 * n) * (0.45 + 0.55 * joint)
        return C(base) * k[..., None]
    return f


l16_floor = persp_floor(VP16, 400, (74, 74, 86), seed=1601)


def l1516_scene(g, d):
    # through the windows: moonlit cloudy sky and far hills
    g.fill(Box(130, 30, 770, 400), vgrad([(60, (86, 100, 146)), (300, (122, 132, 172)), (340, (100, 108, 146))]))
    from real_kit import cloud_layer
    cloud_layer(g, 60, 220, (176, 186, 220), (80, 90, 130), cover=0.45, sx=120, sy=26, seed=1602, alpha=0.8)
    ridge(g, 336, 40, 120, 1603, (40, 46, 70), light=False, rock_tex=0.05)
    treeline(g, 342, 18, 7, 1604, (22, 26, 40), light=0.0)
    # back wall with lancet window openings + deep reveals
    wall = Box(130, 30, 770, 400)
    for c in WIN16:
        wall = Diff(wall, l16_window(c))
    g.fill(wall, ashlar((78, 80, 96), 34, 16, 1605))
    g.mul(wall, 0.5, alpha=lambda X, Y: 0.3 + 0.7 * smooth(260, 30, Y) * 0.6 + 0.4 * (np.abs(X - 450) / 320) ** 2)
    stains(g, wall, 0.35, sx=26, sy=80, seed=1606)
    for c in WIN16:
        reveal = Diff(arch(c - 50, c + 50, WY16[0] - 4, WY16[1] + 6), l16_window(c))
        g.fill(reveal, light_x((60, 62, 78), c - 50, c + 50, 0.7, 1.15))
        g.fill(Box(c - 52, WY16[1], c + 52, WY16[1] + 10, 1), light_y((96, 96, 110), WY16[1], WY16[1] + 10, 1.2, 0.7))
        # tracery: mullion, transom, a quatrefoil oculus
        tr = Union([Box(c - 2.5, WY16[0] - 30, c + 2.5, WY16[1]), Box(c - 42, 252, c + 42, 257),
                    Circ(c, WY16[0] - 26, 15) - Circ(c, WY16[0] - 26, 11)])
        if c == 250:   # broken mullion in the left window
            tr = Diff(tr, Box(c - 4, 262, c + 4, 312))
        g.fill(Inter(tr, l16_window(c)), (44, 44, 56))
    # ivy creeping in through the left window
    rnd = random.Random(1607)
    for _ in range(46):
        x, y = 208 + rnd.uniform(-14, 30), 230 + rnd.uniform(0, 120)
        g.fill(Ell(x, y, 4, 2.6), (34 + rnd.randint(0, 16), 50 + rnd.randint(0, 20), 36))
    # side walls
    lw = Poly([(-2, l16_wall_y(-2)), (130, 30), (130, 400), (-2, l16_wall_y(-2, False))])
    rw = Poly([(770, 30), (902, l16_wall_y(902)), (902, l16_wall_y(902, False)), (770, 400)])
    g.fill(lw, ashlar((60, 60, 74), 30, 18, 1608))
    g.fill(lw, (0, 0, 0), alpha=lambda X, Y: 0.35 + 0.3 * smooth(130, 0, X))
    g.fill(rw, ashlar((60, 60, 74), 30, 18, 1609))
    g.fill(rw, (0, 0, 0), alpha=lambda X, Y: 0.45 + 0.25 * smooth(770, 900, X))
    stains(g, lw, 0.3, seed=1610)
    stains(g, rw, 0.3, seed=1611)
    g.fill(Poly([(-2, -60), (902, -60), (770, 30), (130, 30)]), (16, 14, 18))
    for x in range(150, 760, 70):
        g.fill(Poly([(x, 30), (x + 12, 30), ((x - 450) * 1.6 + 450 + 18, -60), ((x - 450) * 1.6 + 450, -60)]), (40, 32, 28))
    # floor
    floor = Poly([(130, 400), (770, 400), (902, l16_wall_y(902, False)), (902, 602), (-2, 602), (-2, l16_wall_y(-2, False))])
    g.fill(floor, l16_floor)
    g.mul(floor, 0.55, alpha=lambda X, Y: smooth(420, 600, Y) * 0.5 + (np.abs(X - 450) / 450) ** 2 * 0.5)
    g.mul(Box(120, 398, 780, 412), 0.5, feather=6)
    # moonlight pools on the floor (projected windows minus the mullion)
    for c in WIN16:
        pool = Poly(l16_pool(l16_outline(c)))
        mull = Poly(l16_pool([(c - 2.5, WY16[0] - 30), (c + 2.5, WY16[0] - 30), (c + 2.5, WY16[1]), (c - 2.5, WY16[1])]))
        g.add(Diff(pool, mull), (150, 164, 210), 0.42, feather=5)
    # tapestry on the left wall (perspective) - colour difference
    tc = (120, 26, 36)
    tx0, tx1 = 34, 104

    def wy(x, f):
        return l16_wall_y(x) + (l16_wall_y(x, False) - l16_wall_y(x)) * f
    tap = Rough(Poly([(tx0, wy(tx0, 0.2)), (tx1, wy(tx1, 0.2)), (tx1, wy(tx1, 0.62)), (tx0 + 34, wy(tx0 + 34, 0.68)), (tx0, wy(tx0, 0.64))]), 1.5, 4, 1612)
    g.fill(tap, lambda X, Y: C(tc) * (0.55 + 0.35 * np.sin(X * 0.5) ** 2 + 0.15 * fbm(X, Y, 3, 3, 3, 1613))[..., None])
    g.fill(Seg(tx0 - 4, wy(tx0, 0.2) - 2, tx1 + 4, wy(tx1, 0.2) - 2, 4), (70, 56, 40))
    g.fill(Inter(tap, Box(tx0, 0, tx1, 600)), (200, 170, 90), alpha=lambda X, Y: 0.6 * smooth(0.25, 0.22, np.abs(Y - wy(60, 0.58)) / 40))
    # crest on the tapestry - difference: a gold sun becomes a silver crescent
    ex, ey = 70, wy(70, 0.4)
    if "crest" not in d:
        g.fill(Circ(ex, ey, 13), sphere_paint(ex - 3, ey - 3, 13, (220, 180, 70), amb=0.5, spec=0.4))
        for k in range(8):
            a = k * math.tau / 8
            g.fill(Seg(ex + math.cos(a) * 14, ey + math.sin(a) * 14, ex + math.cos(a) * 22, ey + math.sin(a) * 22, 4, 1), (210, 170, 70))
    else:
        g.fill(Circ(ex, ey, 17) - Circ(ex + 8, ey - 4, 15), sphere_paint(ex - 3, ey - 3, 17, (200, 204, 214), amb=0.5, spec=0.4))
    # portrait frame on the right wall - missing in B (pale patch where it hung)
    fx0, fx1 = 796, 872
    ptop, pbot = (lambda x: l16_wall_y(x) + (l16_wall_y(x, False) - l16_wall_y(x)) * 0.24), (lambda x: l16_wall_y(x) + (l16_wall_y(x, False) - l16_wall_y(x)) * 0.58)
    frame = Poly([(fx0, ptop(fx0)), (fx1, ptop(fx1)), (fx1, pbot(fx1)), (fx0, pbot(fx0))])
    g.mul(Moved(frame, -5, 5), 0.5, feather=5)
    g.fill(frame, tex(light_x((150, 116, 56), fx0, fx1, 1.2, 0.6), 0.2, 2, 2))
    inner = Poly([(fx0 + 8, ptop(fx0 + 8) + 10), (fx1 - 8, ptop(fx1 - 8) + 10), (fx1 - 8, pbot(fx1 - 8) - 10), (fx0 + 8, pbot(fx0 + 8) - 10)])
    g.fill(inner, lambda X, Y: C((54, 40, 36)) * (0.8 + 0.3 * fbm(X, Y, 8, 8, 3, 1630))[..., None])
    cx, cy = (fx0 + fx1) / 2, (ptop((fx0 + fx1) / 2) + pbot((fx0 + fx1) / 2)) / 2
    if "portrait" not in d:          # B: the lady has vanished from her portrait
        g.fill(Ell(cx, cy + 22, 20, 18) - Box(cx - 30, cy + 34, cx + 30, cy + 60), (30, 24, 34))
        g.fill(Ell(cx, cy - 10, 10, 13), sphere_paint(cx - 3, cy - 12, 11, (190, 166, 146), ry=14, amb=0.4))
        g.fill(Ell(cx, cy - 18, 13, 8), (40, 26, 20))
        g.fill(Seg(cx + 9, cy - 16, cx + 12, cy + 10, 6, 4), (40, 26, 20))
    # suit of armour (left, by the wall) with a shield
    ax, ab = 176, 448
    g.mul(Ell(ax + 8, ab, 34, 6), 0.55, feather=6)
    steel = (150, 156, 170)
    for lx in (-8, 8):
        g.fill(Seg(ax + lx, ab - 4, ax + lx, ab - 56, 11, 12), cyl_paint(ax + lx, 6, steel, amb=0.35, spec=0.5))
    g.fill(Box(ax - 18, ab - 112, ax + 18, ab - 56, 8), sphere_paint(ax - 6, ab - 92, 26, steel, ry=34, amb=0.35, spec=0.6))
    for sx_ in (-1, 1):
        g.fill(Seg(ax + sx_ * 20, ab - 106, ax + sx_ * 24, ab - 60, 10, 9), cyl_paint(ax + sx_ * 22, 5, steel, amb=0.35, spec=0.5))
    g.fill(Ell(ax, ab - 128, 13, 16), sphere_paint(ax - 4, ab - 132, 14, steel, ry=17, amb=0.35, spec=0.7))
    g.fill(Box(ax - 10, ab - 130, ax + 10, ab - 127), (20, 20, 24))
    g.fill(Seg(ax + 28, ab - 150, ax + 28, ab, 2.5), (90, 80, 70))
    g.fill(Poly([(ax + 24, ab - 150), (ax + 28, ab - 166), (ax + 32, ab - 150)]), steel)
    sc = (40, 70, 140) if "shield" not in d else (150, 120, 40)
    sh = Poly([(ax - 26, ab - 104), (ax + 2, ab - 104), (ax + 2, ab - 80), (ax - 12, ab - 62), (ax - 26, ab - 80)])
    g.fill(sh, light_x(sc, ax - 26, ax + 2, 1.2, 0.7))
    g.fill(Seg(ax - 12, ab - 102, ax - 12, ab - 66, 3), (200, 190, 150))
    g.fill(Seg(ax - 24, ab - 92, ax, ab - 92, 3), (200, 190, 150))
    # banquet table with a tattered cloth
    g.mul(Ell(450, 548, 210, 16), 0.6, feather=14)
    for lx in (300, 600, 330, 570):
        g.fill(Box(lx - 5, 470, lx + 5, 548), cyl_paint(lx, 5, (70, 50, 38)))
    g.fill(Poly([(300, 436), (600, 436), (626, 462), (274, 462)]), planks("h", (92, 66, 48), seed=1615, width=6, x_or_y0=436))
    cloth = Rough(Poly([(286, 440), (614, 440), (628, 466), (626, 500), (560, 494), (520, 508), (450, 496), (380, 510), (320, 494), (276, 500), (274, 466)]), 2.5, 6, 1616)
    g.fill(cloth, lambda X, Y: C((150, 146, 136)) * (0.62 + 0.3 * np.sin(X * 0.13 + 0.002 * (Y - 460) ** 2) ** 2 * smooth(458, 476, Y)
                                                     + 0.25 * smooth(470, 440, Y) + 0.06 * fbm(X, Y, 3, 3, 2, 1631))[..., None])
    g.mul(cloth, 0.18, alpha=lambda X, Y: smooth(0.58, 0.8, fbm(X, Y, 22, 10, 3, 1617)))
    # tableware: plates, a toppled goblet, a candelabra (candles difference)
    for px in (320, 380, 520, 580):
        g.fill(Ell(px, 448, 16, 4), sphere_paint(px, 446, 16, (170, 170, 176), ry=4, amb=0.4, spec=0.5))
    g.fill(Seg(392, 444, 412, 448, 7, 4), cyl_paint(446, 3, (190, 160, 80), horizontal=True))
    g.fill(Ell(392, 444, 3, 4), (120, 20, 30))
    cx, cb = 450, 440
    g.fill(Box(cx - 9, cb - 4, cx + 9, cb + 2, 2), (150, 120, 60))
    g.fill(Box(cx - 2, cb - 46, cx + 2, cb - 4), cyl_paint(cx, 2, (170, 140, 70)))
    arms = [(-24, True), (0, True), (24, "candles" not in d)]
    g.fill(Seg(cx - 24, cb - 46, cx + 24, cb - 46, 3), (170, 140, 70))
    for ax_, on in arms:
        g.fill(Box(cx + ax_ - 4, cb - 52, cx + ax_ + 4, cb - 46, 1), (170, 140, 70))
        if on:
            candle(g, cx + ax_, cb - 52, 20 if ax_ else 26, w=6)
            if ax_ == 24:
                flame(g, cx + ax_, cb - 75, 0.9)
    # high-backed chairs at the table ends
    def chair(x, flip):
        cc = (70, 40, 34)
        back = Union([Box(x - 18, 372, x + 18, 468, 2), arch(x - 18, x + 18, 380, 400)])
        g.fill(back, tex(light_x(cc, x - 18, x + 18, 1.2, 0.6), 0.2, 2, 6))
        g.fill(Box(x - 12, 392, x + 12, 456, 2), light_x((110, 30, 40), x - 12, x + 12, 1.1, 0.6))
        g.fill(Box(x - 22, 466, x + 22, 476, 2), light_y(cc, 466, 476, 1.2, 0.7))
        for lx in (-18, 16):
            g.fill(Box(x + lx, 476, x + lx + 4, 532), cc)
    if "chair" not in d:
        chair(258, False)
    chair(642, True)
    # owl on the right window sill
    if "owl" not in d:
        ox, oy = 664, 322
        g.fill(Ell(ox, oy, 12, 17), tex(sphere_paint(ox - 3, oy - 3, 13, (130, 110, 90), ry=18, amb=0.5), 0.2, 1.4, 2))
        g.fill(Ell(ox, oy + 4, 7, 10), (180, 166, 146))
        for k in (-1, 1):
            g.fill(Circ(ox + k * 4.5, oy - 8, 4), (236, 200, 90))
            g.fill(Circ(ox + k * 4.5, oy - 8, 1.8), (16, 14, 14))
            g.fill(Poly([(ox + k * 3, oy - 15), (ox + k * 11, oy - 22), (ox + k * 9, oy - 12)]), (110, 90, 70))
        g.fill(Poly([(ox - 2, oy - 5), (ox + 2, oy - 5), (ox, oy)]), (190, 150, 60))
        rim(g, Ell(ox, oy, 12, 17), 2, 1, k=0.45)
    # fallen chandelier + rubble (front left)
    g.mul(Ell(206, 566, 70, 10), 0.55, feather=8)
    ring = Ell(206, 556, 62, 14) - Ell(206, 556, 54, 9)
    g.fill(ring, light_y((60, 56, 56), 542, 570, 1.3, 0.6))
    for k in range(6):
        a = k * math.tau / 6 + 0.3
        x, y = 206 + 58 * math.cos(a), 556 + 12 * math.sin(a)
        g.fill(Seg(x, y, x + 9 * math.cos(a + 1.2), y - 3, 4, 3), (214, 206, 186))
    g.fill(Seg(206, 556, 236, 470, 2), (50, 46, 46))
    for x, y, r, s in ((820, 470, 18, 1618), (850, 480, 12, 1619), (790, 486, 10, 1620), (90, 520, 16, 1621), (62, 540, 22, 1622)):
        rock(g, x, y, r, r * 0.6, (96, 96, 108), seed=s)
    # treasure chest (front right): closed in A, open with gold in B
    chx, chy = 770, 548
    g.mul(Ell(chx + 8, chy + 26, 60, 8), 0.6, feather=8)
    g.fill(Box(chx - 48, chy - 10, chx + 48, chy + 26, 3), planks("v", (96, 60, 36), seed=1623, width=12))
    for bx in (-36, 30):
        g.fill(Box(chx + bx, chy - 10, chx + bx + 6, chy + 26), (60, 56, 50))
    if "chest" not in d:
        g.fill(Union([Box(chx - 50, chy - 30, chx + 50, chy - 8, 2), Ell(chx, chy - 30, 50, 12) - Box(chx - 52, chy - 30, chx + 52, chy)]),
               light_y((110, 70, 42), chy - 42, chy - 8, 1.3, 0.7))
        g.fill(Box(chx - 6, chy - 18, chx + 6, chy - 4, 1), (150, 130, 70))
    else:
        g.fill(Poly([(chx - 50, chy - 12), (chx + 50, chy - 12), (chx + 46, chy - 58), (chx - 46, chy - 58)]), light_y((80, 50, 30), chy - 58, chy - 12, 1.1, 0.6))
        for k in range(14):
            gx, gy = chx - 40 + (k * 37) % 80, chy - 12 - (k % 3) * 3
            g.fill(Ell(gx, gy, 6, 3), sphere_paint(gx - 2, gy - 1, 6, (230, 180, 60), ry=3, amb=0.5, spec=0.8))
        g.glow(chx, chy - 14, 40, (255, 200, 90), 0.25)
    cobweb(g, 130, 30, 70, (1, 1))
    cobweb(g, 770, 30, 60, (-1, 1))
    cobweb(g, 302, 470, 26, (1, 1), k=0.25)


L1516_RAYS = [dict(lx=L16[0], ly=L16[1], col=(176, 190, 236), k=1.95, region=Union([l16_window(c) for c in WIN16]),
                   threshold=70, soft=80, density=0.9, decay=0.985, samples=80,
                   receive=lambda X, Y: 0.35 + 0.65 * smooth(600, 470, Y))]

L1516_ELEMENTS = [
    beam_el("beam1", 262, 250, 330, 480, 70, 90, k=0.14, phase=0.0),
    beam_el("beam2", 462, 250, 545, 470, 70, 90, k=0.12, phase=0.33, speed=0.1),
    beam_el("beam3", 662, 250, 740, 470, 70, 90, k=0.12, phase=0.66, speed=0.14),
    motes_el("motes1", [(300, 330), (330, 380), (280, 410), (500, 320), (530, 370), (700, 340), (720, 400)], phase=0.0),
    motes_el("motes2", [(310, 350), (510, 390), (480, 350), (690, 370), (730, 330), (270, 380)], phase=0.5, r=1.6, vx=-3),
    flame_el("f1", 426, 371, 0.9),
    flame_el("f2", 450, 365, 0.9, phase=0.3),
    bat_el("bat1", 450, 110, s=9, speed=40, phase=0.2),
]

L1516_DIFFS = [
    ("crest", 70, 196, 0),
    ("owl", 664, 316, 0),
    ("portrait", 834, 210, 0),
    ("shield", 164, 362, 0),
    ("candles", 474, 380, 0),
    ("chair", 258, 440, 0),
    ("chest", 770, 530, 0),
]


# =================================================================== Level 1517 moonlit graveyard
M17 = (430, 150, 40)


def l1517_scene(g, d):
    mx, my, mr = M17
    sky(g, [(0, (6, 10, 24)), (160, (20, 28, 58)), (300, (46, 56, 90)), (360, (60, 68, 100))])
    stars(g, 110, 300, seed=1701)
    moon(g, mx, my, mr, col=(226, 224, 214), k=0.7, seed=1702)
    from real_kit import cloud_layer
    cloud_layer(g, 120, 180, (150, 160, 200), (60, 66, 100), cover=0.32, sx=170, sy=9, seed=1703, alpha=0.6)
    cloud_layer(g, 20, 90, (90, 100, 140), (30, 36, 60), cover=0.4, sx=220, sy=22, seed=1704, alpha=0.7)
    ridge(g, 340, 60, 200, 1705, (34, 40, 66), ridged=False, light=False, rock_tex=0.05, haze=((54, 62, 96), 0.5, 0.3))
    treeline(g, 356, 26, 9, 1706, (16, 20, 32), light=0.0, haze=((50, 58, 90), 0.4, 0.15), conifer=False)
    # dead tree in front of the moon (trunk right of it, branches over the disc)
    dead_tree(g, 640, 470, 440, seed=1707, col=(18, 16, 20), lean=0.32, spread=1.0, w=26, depth=6)
    g.fill(Seg(668, 290, 600, 258, 12, 8), (18, 16, 20))
    g.fill(Seg(600, 258, 540, 232, 8, 5), (18, 16, 20))
    g.fill(Seg(540, 232, 470, 226, 5, 2.5), (18, 16, 20))
    g.fill(Seg(520, 230, 500, 206, 3, 1.5), (18, 16, 20))
    twigs(g, [(470, 226), (446, 196), (418, 178), (392, 150), (360, 136)], 5, 1.4, (18, 16, 20), seed=1750, n=3)
    twigs(g, [(584, 96), (530, 104), (480, 118), (446, 126), (404, 112), (370, 104)], 7, 1.4, (18, 16, 20), seed=1751, n=3)
    twigs(g, [(446, 126), (432, 150), (440, 176)], 3, 1.0, (18, 16, 20), seed=1752, n=1)
    g.fill(Seg(676, 300, 620, 170, 16, 10), (18, 16, 20))
    g.fill(Seg(620, 170, 584, 96, 10, 7), (18, 16, 20))
    if "crow" not in d:
        cx, cy = 506, 228
        g.fill(Ell(cx, cy - 11, 8, 11.5), (12, 10, 14))
        g.fill(Circ(cx - 5, cy - 24, 6), (12, 10, 14))
        g.fill(Poly([(cx - 10, cy - 26), (cx - 19, cy - 23), (cx - 10, cy - 21)]), (34, 30, 32))
        g.fill(Poly([(cx + 5, cy - 8), (cx + 19, cy - 1), (cx + 5, cy - 2)]), (12, 10, 14))
        g.fill(Circ(cx - 7, cy - 25, 1.3), (200, 180, 120))
    # chapel on a rise (left)
    def rise(x):
        return 352 - 22 * np.exp(-((x - 130) / 140.0) ** 2) + (fbm1(x, 40, 3, 1708) - 0.5) * 8
    g.fill(Under(rise, -20, 420, 420), (22, 26, 36))
    nave = Union([Box(40, 262, 196, 352), Poly([(32, 266), (118, 206), (204, 266)])])
    g.fill(nave, ashlar((58, 60, 76), 16, 8, 1709))
    g.fill(nave, (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.3 * smooth(40, 200, X))
    g.fill(Poly([(28, 268), (118, 202), (208, 268), (200, 268), (118, 210), (36, 268)]), (30, 28, 34))
    tower = Union([Box(190, 196, 246, 352), Poly([(184, 198), (218, 92), (252, 198)])])
    g.fill(tower, ashlar((62, 64, 80), 14, 8, 1710))
    g.fill(tower, (0, 0, 0), alpha=lambda X, Y: 0.2 + 0.35 * smooth(196, 246, X))
    g.fill(Union([Box(216, 62, 220, 94), Box(209, 70, 227, 74)]), (30, 28, 34))
    g.fill(arch(208, 228, 222, 250), (10, 10, 14))
    rim(g, tower, -2, 1.5, k=0.25)
    rim(g, nave, -2, 1.5, k=0.2)
    for wx in (62, 160):
        g.fill(arch(wx - 7, wx + 7, 300, 330), (16, 14, 20))
    rw = Circ(118, 286, 16)
    if "rose" not in d:
        g.fill(rw, rgrad(118, 286, 16, [(0, (255, 214, 140)), (0.7, (230, 140, 60)), (1, (140, 60, 40))]))
        g.glow(118, 286, 34, (255, 170, 80), 0.35)
    else:
        g.fill(rw, (16, 14, 20))
    g.fill(Union([Box(117, 270, 119, 302), Box(102, 285, 134, 287), Circ(118, 286, 5) - Circ(118, 286, 3)]), (40, 32, 30))
    g.fill(arch(106, 130, 324, 352, pointed=True), (14, 12, 16))
    # graveyard ground
    def gnd(x):
        return 366 + (fbm1(x, 70, 3, 1711) - 0.5) * 10
    g.fill(Under(gnd, -20, W + 20, H + 20), tex(vgrad([(366, (40, 46, 56)), (600, (22, 26, 30))]), 0.35, 4, 3, 4, 1712))
    blades(g, 380, 600, (60, 70, 74), n=320, seed=1713, hmax=18)
    fog_band(g, 330, 392, 440, (96, 106, 146), 0.55, seed=1714)
    # iron fence behind the graves
    bars = [Box(x, 344, x + 2.6, 398) for x in range(262, 900, 13)]
    tips = [Poly([(x - 2, 346), (x + 1.3, 336), (x + 4.6, 346)]) for x in range(262, 900, 13)]
    rails = [Box(258, 352, 902, 355), Box(258, 386, 902, 389)]
    fence = Union(bars + tips + rails)
    g.fill(fence, (16, 16, 20))
    g.add(Union([Box(x + 1.6, 336, x + 2.6, 398) for x in range(262, 900, 13)]), MOONLIGHT, 0.12)
    g.fill(Box(250, 336, 266, 404, 2), ashlar((70, 72, 88), 8, 8, 1715))
    # mausoleum (right)
    mb = 440
    g.mul(Ell(790, mb + 4, 120, 10), 0.55, feather=10)
    for i, (y0, y1, ext) in enumerate(((mb - 14, mb, 16), (mb - 26, mb - 14, 8))):
        g.fill(Box(690 - ext, y0, 880 + ext, y1), light_y((90, 92, 104), y0, y1, 1.2, 0.8))
    g.fill(Box(700, 326, 870, mb - 26), ashlar((80, 82, 96), 22, 11, 1716))
    g.fill(Box(700, 326, 870, mb - 26), (0, 0, 0), alpha=lambda X, Y: 0.3 + 0.25 * smooth(700, 870, X))
    g.fill(arch(764, 806, 372, mb - 26, pointed=False), (8, 8, 12))
    gate_bars = Union([Box(x, 352, x + 2, mb - 26) for x in range(768, 804, 7)] + [Box(764, 392, 806, 394)])
    g.fill(Inter(gate_bars, arch(764, 806, 372, mb - 26, pointed=False)), (60, 60, 70))
    for cx_ in (716, 744, 826, 854):
        g.fill(Box(cx_ - 7, 330, cx_ + 7, mb - 26), cyl_paint(cx_, 7, (120, 122, 134), amb=0.4, spec=0.15))
        g.fill(Box(cx_ - 10, 326, cx_ + 10, 332), (100, 102, 114))
    g.fill(Box(692, 312, 878, 326), light_y((104, 106, 120), 312, 326, 1.2, 0.8))
    ped = Poly([(690, 314), (785, 270), (880, 314)])
    g.fill(ped, tex(light_y((96, 98, 112), 270, 314, 1.3, 0.8), 0.15, 5, 4))
    g.fill(Poly([(712, 310), (785, 280), (858, 310)]), (64, 66, 78))
    rim(g, ped, 0, 2, k=0.3)
    stains(g, Box(700, 326, 870, mb - 26), 0.18, sx=30, sy=40, seed=1717)
    if "urn" not in d:
        g.fill(Union([Ell(785, 252, 12, 13), Box(779, 262, 791, 272), Box(774, 268, 796, 273)]),
               sphere_paint(781, 248, 13, (120, 122, 134), ry=14, amb=0.4, spec=0.2))
        g.fill(Box(778, 236, 792, 241, 1), (104, 106, 118))
        g.fill(Rough(Ell(785, 232, 8, 7), 2, 3, 1718), (48, 70, 46))
    # middle row of headstones
    for x, base, w, h, kind, s in ((300, 440, 30, 50, "round", 1720), (372, 446, 30, 64, "cross", 1721),
                                   (548, 444, 26, 74, "obelisk", 1723), (626, 452, 40, 44, "slab", 1724)):
        tombstone(g, x, base, w, h, kind, seed=s, lit=-1 if x > 430 else 1, lean=0.06 if s == 1724 else 0.0)
    tombstone(g, 470, 456, 40, 78, "celtic" if "celtic" not in d else "round", seed=1722, lit=-1)
    fog_band(g, 400, 450, 500, (96, 106, 146), 0.35, noise=0.6, sx=120, sy=10, seed=1725)
    # path of flagstones towards the chapel
    path = Rough(Poly([(120, H + 6), (300, H + 6), (220, 480), (150, 400), (128, 354), (110, 354), (124, 400), (150, 480)]), 3, 10, 1726)
    g.fill(path, grain_tex(vgrad([(380, (58, 62, 76)), (600, (44, 44, 52))]), 0.15, 1727), feather=1.5)
    # foreground headstone with a wreath
    tombstone(g, 300, 584, 76, 120, "round", col=(98, 100, 110), seed=1728, lit=1)
    g.fill(Box(276, 498, 324, 502), (60, 60, 70), alpha=0.6)
    for yy in (510, 518, 526):
        g.fill(Box(280, yy, 320, yy + 2), (60, 60, 70), alpha=0.5)
    wc = (150, 30, 40) if "wreath" not in d else (220, 210, 190)
    wr = Rough(Circ(300, 554, 20) - Circ(300, 554, 11), 2.2, 3, 1729)
    g.fill(Rough(Circ(300, 554, 20) - Circ(300, 554, 11), 1.6, 4, 1730), (34, 60, 36))
    for k in range(9):
        a = k * math.tau / 9
        bx, by = 300 + 15.5 * math.cos(a), 554 + 15.5 * math.sin(a)
        g.fill(Rough(Circ(bx, by, 5), 1.2, 2, 1731 + k), sphere_paint(bx - 1, by - 1, 5, wc, amb=0.4, spec=0.2))
    # leaning slab and a cross in the foreground
    tombstone(g, 520, 590, 58, 96, "slab", col=(92, 94, 104), seed=1740, lit=-1, lean=-0.1)
    tombstone(g, 880, 600, 44, 120, "cross", col=(88, 90, 100), seed=1741, lit=-1)
    # fresh grave mound with a shovel
    g.fill(Rough(Ell(720, 562, 74, 16), 4, 8, 1742), tex(sphere_paint(710, 556, 74, (66, 54, 46), ry=18, amb=0.4, spec=0.0), 0.3, 3, 2, 3, 1743))
    if "shovel" not in d:
        g.fill(Seg(746, 556, 774, 470, 5, 4), tex(light_x((110, 84, 56), 744, 776, 1.3, 0.6), 0.2, 1.5, 6))
        g.fill(Seg(768, 474, 784, 474, 4), (100, 76, 50))
        g.fill(Poly([(736, 552), (756, 556), (754, 578), (744, 584), (734, 576)]), sphere_paint(744, 560, 20, (130, 134, 144), amb=0.4, spec=0.5))
    # ground lantern (left)
    lx, ly = 80, 536
    g.mul(Ell(lx + 6, ly + 22, 26, 5), 0.55, feather=5)
    g.fill(Box(lx - 14, ly + 14, lx + 14, ly + 22, 2), (36, 34, 34))
    if "lantern" not in d:
        g.glow(lx, ly, 46, (255, 170, 80), 0.35)
        g.fill(Box(lx - 11, ly - 22, lx + 11, ly + 14, 2), (255, 200, 120))
        g.fill(Ell(lx, ly - 2, 5, 9), (255, 246, 210))
    else:
        g.fill(Box(lx - 11, ly - 22, lx + 11, ly + 14, 2), (40, 46, 56))
        g.add(Box(lx - 9, ly - 20, lx - 5, ly + 12), MOONLIGHT, 0.2)
    for bx in (-12, 10):
        g.fill(Box(lx + bx, ly - 22, lx + bx + 2.4, ly + 14), (30, 28, 28))
    g.fill(Poly([(lx - 16, ly - 22), (lx, ly - 36), (lx + 16, ly - 22)]), (30, 28, 28))
    g.fill(Ell(lx, ly - 40, 5, 5) - Ell(lx, ly - 40, 2.5, 2.5), (30, 28, 28))
    g.fog(470, 600, (80, 90, 126), 0.12, 0.0, noise=0.5, sx=160, sy=12, seed=1744)


L1517_RAYS = [dict(lx=M17[0], ly=M17[1], col=(170, 186, 232), k=2.0, region=Box(-2, -2, W + 2, 345), threshold=88,
                   soft=70, density=0.94, decay=0.98, samples=80, receive=moon_receive(*M17, floor=0.35))]

L1517_ELEMENTS = [
    bat_el("bat1", 250, 70, s=10, speed=30, phase=0.1),
    bat_el("bat2", 280, 88, s=7, speed=30, phase=0.15),
    mist_el("mist1", 220, 372, 160, 10, (110, 120, 160), alpha=0.45, length=60, seed=21),
    mist_el("mist2", 640, 484, 200, 9, (110, 120, 160), alpha=0.4, length=70, seed=22),
    beam_el("beam1", 430, 160, 250, 470, 30, 160, k=0.1, phase=0.0),
    beam_el("beam2", 440, 160, 610, 480, 30, 140, k=0.09, phase=0.5, speed=0.1),
    glint_el("wisp", [(400, 500), (610, 410), (170, 450)], col=(150, 220, 255), r=5, speed=0.3, phase=0.2),
    glint_el("twinkle", [(60, 40), (700, 60), (860, 120), (300, 30), (560, 40)], col=(240, 240, 255), r=3, speed=0.6),
]

L1517_DIFFS = [
    ("rose", 118, 286, 0),
    ("crow", 506, 214, 0),
    ("urn", 785, 252, 0),
    ("celtic", 470, 410, 0),
    ("wreath", 300, 554, 0),
    ("shovel", 760, 520, 0),
    ("lantern", 80, 520, 0),
]


# =================================================================== Level 1518 the vampire's crypt
L18 = (860, -250)                     # moon outside, upper right
WIN18 = (530, 96, 600, 176)           # barred window high in the back wall
VP18 = (450, 250)


def l18_window():
    return arch(WIN18[0], WIN18[2], WIN18[1] + 14, WIN18[3], pointed=False)


def stone_band(cx, cy, r0, r1, y_cut):
    """Semicircular vault rib (ring between radii r0 < r1, above y_cut)."""
    return Inter(Circ(cx, cy, r1) - Circ(cx, cy, r0), Box(cx - r1, cy - r1, cx + r1, y_cut))


def l1518_scene(g, d):
    # vault: dark stone everywhere, lighter back wall under the last arch
    g.fill(Box(-2, -2, W + 2, H + 2), ashlar((44, 42, 52), 30, 15, 1801))
    g.fill(Box(-2, -2, W + 2, H + 2), (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.35 * (np.abs(X - 450) / 450) ** 1.5)
    # through the window: moonlit sky with the moon's edge
    win = l18_window()
    g.fill(win, vgrad([(WIN18[1], (120, 136, 186)), (WIN18[3], (160, 170, 210))]))
    g.glow(612, 100, 60, (200, 214, 255), 0.6)
    g.fill(Inter(Circ(612, 100, 30), win), (236, 238, 230))
    back = Union([Box(262, 220, 638, 422), Inter(Circ(450, 220, 188), Box(262, 30, 638, 221))])
    g.fill(Diff(back, win), ashlar((70, 68, 80), 26, 13, 1802))
    g.fill(Diff(back, win), (0, 0, 0), alpha=lambda X, Y: 0.15 + 0.3 * smooth(300, 60, Y))
    stains(g, back, 0.3, sx=24, sy=70, seed=1803)
    g.fill(Diff(arch(WIN18[0] - 8, WIN18[2] + 8, WIN18[1] + 10, WIN18[3] + 8, pointed=False), win),
           light_x((56, 54, 64), WIN18[0] - 8, WIN18[2] + 8, 0.7, 1.2))
    bars = Union([Box(x - 2, WIN18[1], x + 2, WIN18[3]) for x in (548, 565, 582)] + [Box(WIN18[0], 140, WIN18[2], 144)])
    g.fill(Inter(bars, win), (26, 24, 28))
    # ribs of the vault
    for r0, r1, cy, yc, col in ((190, 210, 220, 222, (84, 82, 94)), (250, 276, 236, 240, (74, 72, 84)), (330, 366, 262, 270, (62, 60, 72))):
        band = stone_band(450, cy, r0, r1, yc)
        g.fill(band, lambda X, Y, col=col, cy=cy: ashlar(col, 18, 30, 1804)(X, Y) * (0.7 + 0.4 * np.clip((Y - cy + 300) / 300, 0, 1))[..., None])
        rim(g, band, 0, 2.5, col=(130, 120, 110), k=0.25)
        g.mul(Moved(band, 0, 8), 0.4, feather=8)
    # floor
    floor = Poly([(262, 422), (638, 422), (902, 520), (902, 602), (-2, 602), (-2, 520)])
    fpaint = persp_floor(VP18, 422, (66, 64, 74), tile=40, seed=1805)
    g.fill(floor, fpaint)
    g.mul(floor, 0.55, alpha=lambda X, Y: 0.25 + 0.6 * (np.abs(X - 450) / 450) ** 1.5)
    # side walls between ribs and pillars
    for sgn in (-1, 1):
        sw = Poly([(450 + sgn * 188, 220), (450 + sgn * 330, 262), (450 + sgn * 330, 560), (450 + sgn * 188, 422)])
        g.fill(sw, ashlar((50, 48, 58), 22, 14, 1806 + sgn))
        g.fill(sw, (0, 0, 0), alpha=0.35)
    # moonbeam pool on the floor / dais (bars cast stripes)
    pool = Poly([(330, 470), (430, 452), (470, 500), (360, 524)])
    stripes = Union([Seg(355 + i * 24, 466 - i * 4, 388 + i * 24, 516 - i * 4, 5) for i in range(3)])
    g.add(Diff(pool, stripes), (150, 164, 210), 0.35, feather=8)
    # chain hanging from the vault (difference)
    if "chain" not in d:
        for i in range(9):
            y = 40 + i * 13
            sh = (Ell(392, y, 4, 7.5) - Ell(392, y, 1.8, 5)) if i % 2 == 0 else Box(390.5, y - 7, 393.5, y + 7, 1.4)
            g.fill(sh, light_x((96, 90, 86), 386, 398, 1.3, 0.6))
        g.fill(Ell(392, 166, 13, 9) - Ell(392, 166, 9, 5.5), light_x((110, 104, 98), 378, 406, 1.3, 0.6))
    # hanging bats on the left rib (difference: one missing)
    for i, (bx, by) in enumerate(((146, 150), (184, 122), (224, 98))):
        if i == 1 and "bats" in d:
            continue
        hanging_bat(g, bx, by, 44, rim_col=(255, 170, 100))
    # front pillars
    for x0, x1 in ((20, 110), (790, 880)):
        pil = Box(x0, -2, x1, 602)
        g.fill(pil, lambda X, Y, x0=x0, x1=x1: ashlar((86, 82, 92), 45, 30, 1808)(X, Y) * (0.5 + 0.7 * np.sqrt(np.clip(1 - ((X - (x0 + x1) / 2) / ((x1 - x0) / 2 + 2)) ** 2, 0, 1)))[..., None])
        g.fill(Box(x0 - 12, 280, x1 + 12, 304, 2), light_y((96, 92, 102), 280, 304, 1.25, 0.7))
        g.fill(Box(x0 - 8, 304, x1 + 8, 314), (60, 58, 66))
        g.fill(Box(x0 - 14, 560, x1 + 14, 602, 2), light_y((90, 86, 96), 560, 602, 1.2, 0.7))
        stains(g, pil, 0.3, sx=20, sy=60, seed=x0)
    # crest on the right pillar: bat shield (colour difference)
    cc = (130, 20, 30) if "crest" not in d else (40, 60, 120)
    sh = Poly([(806, 196), (864, 196), (864, 236), (835, 264), (806, 236)])
    g.mul(Moved(sh, 4, 4), 0.5, feather=4)
    g.fill(sh, light_x(cc, 806, 864, 1.3, 0.7))
    g.fill(Diff(sh, Moved(Poly([(810, 200), (860, 200), (860, 234), (835, 258), (810, 234)]), 0, 0)), (190, 160, 80))
    bat(g, 835, 226, 20, col=(20, 16, 20))
    # chains / shackles on the left pillar
    for i in range(6):
        y = 340 + i * 12
        g.fill((Ell(64, y, 4, 7) - Ell(64, y, 1.8, 4.6)) if i % 2 == 0 else Box(62.5, y - 6, 65.5, y + 6, 1.2), (90, 84, 80))
    g.fill(Ell(64, 418, 12, 8) - Ell(64, 418, 8, 5), (96, 90, 86))
    # dais
    g.mul(Ell(450, 520, 230, 16), 0.6, feather=12)
    g.fill(Poly([(250, 470), (650, 470), (676, 486), (224, 486)]), light_y((96, 92, 104), 470, 486, 1.3, 0.85))
    g.fill(Box(224, 486, 676, 516), ashlar((82, 78, 90), 40, 15, 1809))
    g.fill(Box(224, 486, 676, 516), (0, 0, 0), alpha=0.2)
    # coffin: interior + rim, the vampire rising, then the front panel
    rim_top = [(276, 430), (322, 410), (586, 410), (626, 430), (586, 450), (322, 450)]
    g.fill(Poly(rim_top), tex(light_y((70, 40, 32), 410, 450, 1.2, 0.8), 0.1, 6, 2))
    inner = Poly([(290, 430), (328, 415), (580, 415), (612, 430), (580, 445), (328, 445)])
    g.fill(inner, lambda X, Y: C((130, 20, 34)) * (0.55 + 0.35 * np.abs(np.sin((X - 290) * 0.12)) * smooth(445, 418, Y) + 0.1)[..., None])
    for x in range(330, 580, 28):
        g.fill(Circ(x, 430, 1.8), (200, 170, 90))
    g.fill(Ell(312, 430, 18, 9), sphere_paint(306, 426, 18, (160, 30, 44), ry=9, amb=0.4))     # pillow
    before = g.img.copy()
    vampire(g, 352, 566, 300, medal=(196, 26, 40) if "medal" not in d else (40, 170, 90), rim_dx=-2.2, wind=0.0, arm_up=True)
    r = g.win((0, 446, W, H), pad=0)
    if r is not None:
        (j0, j1, i0, i1), _, _ = r
        g.img[j0:j1, i0:i1] = before[j0:j1, i0:i1]
    front = Poly([(276, 430), (322, 450), (586, 450), (626, 430), (626, 452), (586, 476), (322, 476), (276, 452)])
    g.fill(front, planks("h", (74, 44, 34), seed=1810, width=9, x_or_y0=450))
    g.fill(Poly([(276, 430), (322, 450), (322, 476), (276, 452)]), (0, 0, 0), alpha=0.35)
    for x in (340, 450, 560):
        g.fill(Box(x - 9, 455, x + 9, 470, 2), light_x((170, 140, 70), x - 9, x + 9, 1.3, 0.6))
    rim(g, Poly(rim_top), 0, 1.5, col=(255, 190, 120), k=0.2)
    # coffin lid leaning against the dais (left) with a rose on it (colour difference)
    lid = Poly([(170, 560), (200, 404), (250, 400), (262, 432), (236, 566)])
    g.mul(Moved(lid, 10, 6), 0.5, feather=8)
    g.fill(lid, tex(light_x((80, 48, 36), 170, 262, 1.25, 0.6), 0.12, 20, 2, 3, 1811))
    g.fill(Seg(205, 470, 230, 452, 2), (40, 70, 40))
    rc = (190, 20, 36) if "rose" not in d else (236, 232, 220)
    g.fill(Rough(Circ(234, 448, 13), 2.2, 3.2, 1812), sphere_paint(230, 444, 13, rc, amb=0.35, spec=0.2))
    for a in (0.4, 2.2, 4.0):
        g.fill(Seg(234 + math.cos(a) * 3, 448 + math.sin(a) * 3, 234 + math.cos(a + 1.4) * 9, 448 + math.sin(a + 1.4) * 9, 1.5), mixc(rc, (0, 0, 0), 0.4))
    g.fill(Ell(214, 462, 6, 3), (44, 84, 44))
    # standing candelabra (left; difference: a candle missing) and (right; flames animated)
    for cx_, base_, diffc in ((128, 560, True), (726, 548, False)):
        g.mul(Ell(cx_ + 8, base_, 34, 6), 0.55, feather=6)
        g.fill(Poly([(cx_ - 22, base_), (cx_, base_ - 20), (cx_ + 22, base_)]), (36, 32, 30))
        g.fill(Box(cx_ - 3, base_ - 210, cx_ + 3, base_ - 10), cyl_paint(cx_, 3, (110, 90, 60), spec=0.4))
        g.fill(Ell(cx_, base_ - 210, 34, 6) - Ell(cx_, base_ - 214, 30, 5), (110, 90, 60))
        for ax_, hh in ((-30, 26), (0, 34), (30, 26)):
            if diffc and ax_ == 30 and "candles" in d:
                continue
            candle(g, cx_ + ax_, base_ - 214, hh, w=8)
            if diffc:
                flame(g, cx_ + ax_, base_ - 214 - hh - 1, 1.1)
        g.glow(cx_, base_ - 250, 110, (255, 150, 60), 0.18)
    # side table with an hourglass (difference) and a goblet
    tx = 800
    g.mul(Ell(tx + 6, 560, 60, 6), 0.55, feather=6)
    g.fill(Box(tx - 52, 492, tx + 52, 502, 2), light_y((90, 60, 40), 492, 502, 1.2, 0.7))
    for lx in (-44, 40):
        g.fill(Box(tx + lx, 502, tx + lx + 5, 560), (70, 46, 32))
    g.fill(Union([Ell(tx + 30, 466, 9, 10) - Box(tx + 18, 444, tx + 42, 462), Box(tx + 28.5, 470, tx + 31.5, 488), Ell(tx + 30, 490, 8, 2.5)]),
           sphere_paint(tx + 27, 470, 10, (190, 160, 80), amb=0.4, spec=0.7))
    g.fill(Ell(tx + 30, 463, 8, 2.2), (110, 10, 24))
    if "hourglass" not in d:
        hx, hb = tx - 16, 492
        g.fill(Box(hx - 14, hb - 6, hx + 14, hb, 1), (80, 54, 36))
        g.fill(Box(hx - 14, hb - 52, hx + 14, hb - 46, 1), (80, 54, 36))
        for px in (-12, 10):
            g.fill(Box(hx + px, hb - 46, hx + px + 2.4, hb - 6), (80, 54, 36))
        glass = Union([Ell(hx, hb - 36, 9, 11), Ell(hx, hb - 16, 9, 11)])
        g.fill(glass, (150, 160, 180), alpha=0.35)
        g.fill(Poly([(hx - 7, hb - 8), (hx + 7, hb - 8), (hx + 3, hb - 16), (hx - 3, hb - 16)]), (210, 180, 120))
        g.fill(Seg(hx, hb - 26, hx, hb - 16, 1), (210, 180, 120))
        g.add(Seg(hx - 5, hb - 42, hx - 4, hb - 30, 1.2), (255, 255, 255), 0.4)
    # old book on the floor (left front)
    g.fill(Poly([(30, 590), (110, 580), (118, 596), (36, 604)]), light_y((80, 30, 30), 580, 604, 1.2, 0.7))
    g.fill(Poly([(34, 586), (112, 576), (110, 582), (32, 591)]), (210, 200, 170))
    cobweb(g, 110, 0, 80, (1, 1))
    cobweb(g, 790, 0, 70, (-1, 1))


L1518_RAYS = [dict(lx=L18[0], ly=L18[1], col=(176, 190, 236), k=2.4, region=l18_window(), threshold=80, soft=80,
                   density=0.92, decay=0.985, samples=80)]

L1518_ELEMENTS = [
    beam_el("beam1", 565, 150, 400, 480, 60, 130, k=0.13),
    motes_el("motes1", [(520, 220), (480, 260), (450, 320), (505, 300), (470, 380), (430, 360)], phase=0.0),
    motes_el("motes2", [(500, 240), (460, 300), (520, 270), (440, 400), (490, 340)], phase=0.5, r=1.6, vx=-3),
    flame_el("f1", 696, 307, 1.1, phase=0.0),
    flame_el("f2", 726, 299, 1.1, phase=0.3),
    flame_el("f3", 756, 307, 1.1, phase=0.6),
    E("flicker", el(lambda g, m: g.glow(726, 300, 120, (255, 160, 70), 0.18)), daynight="untinted",
      anim=dict(twinkle=0.6, twinkleSpeed=1.4)),
    bat_el("bat1", 450, 60, s=9, speed=36, phase=0.6),
]

L1518_DIFFS = [
    ("bats", 184, 146, 0),
    ("chain", 392, 100, 0),
    ("crest", 835, 228, 0),
    ("candles", 158, 320, 0),
    ("medal", 350, 388, 0),
    ("rose", 234, 450, 0),
    ("hourglass", 784, 466, 0),
]


# =================================================================== Level 1519 the vampire count on the balcony
M19 = (300, 214, 104)


def l1519_scene(g, d):
    mx, my, mr = M19
    sky(g, [(0, (6, 8, 22)), (200, (22, 26, 58)), (360, (50, 52, 88))])
    stars(g, 140, 330, seed=1901)
    moon(g, mx, my, mr, col=(226, 222, 210), halo=(150, 160, 225), k=0.6, seed=1902)
    from real_kit import cloud_layer
    cloud_layer(g, 250, 290, (150, 156, 196), (60, 62, 96), cover=0.32, sx=180, sy=8, seed=1903, alpha=0.55)
    cloud_layer(g, 30, 110, (80, 86, 124), (30, 32, 56), cover=0.38, sx=220, sy=20, seed=1904, alpha=0.7)
    ridge(g, 380, 110, 240, 1905, (30, 34, 60), light=False, haze=((50, 56, 92), 0.5, 0.25), rock_tex=0.06)
    fog_band(g, 320, 370, 420, (70, 76, 116), 0.5, seed=1906)
    # castle roofline below the balcony level
    roof = []
    rnd = random.Random(1907)
    x = -10
    while x < W + 10:
        w = rnd.uniform(60, 110)
        top = rnd.uniform(350, 390)
        roof.append(Union([Box(x, top, x + w, 460), Poly([(x - 6, top + 2), (x + w / 2, top - w * 0.42), (x + w + 6, top + 2)])]))
        x += w + rnd.uniform(-10, 10)
    rf = Union(roof)
    g.fill(rf, tex(vgrad([(300, (30, 32, 48)), (460, (18, 18, 28))]), 0.15, 6, 4))
    rim(g, rf, 0, 2, k=0.25)
    rnd = random.Random(1908)
    for _ in range(12):
        wx, wy = rnd.uniform(20, 880), rnd.uniform(395, 430)
        g.fill(Box(wx, wy, wx + 5, wy + 8, 1), (255, 190, 110))
        g.glow(wx + 2.5, wy + 4, 12, (255, 160, 70), 0.25)
    # bell tower in front of the moon
    tw = Union([Box(232, 160, 368, 460), Box(222, 150, 378, 164), Poly([(226, 152), (300, 28), (374, 152)])])
    belfry = [arch(248, 292, 196, 262, pointed=False), arch(308, 352, 196, 262, pointed=False)]
    tw_open = Diff(tw, Union(belfry))
    g.fill(tw_open, ashlar((50, 50, 66), 16, 9, 1909))
    g.fill(tw_open, (0, 0, 0), alpha=lambda X, Y: 0.35 + 0.15 * smooth(232, 368, X))
    g.fill(Poly([(226, 152), (300, 28), (374, 152)]), tex(light_y((40, 40, 56), 28, 152, 1.0, 0.7), 0.2, 3, 8, 3, 1910))
    for i in range(1, 9):
        y = 28 + i * 14
        hw = (y - 28) / 124 * 74
        g.fill(Seg(300 - hw, y, 300 + hw, y, 1), (24, 24, 34))
    g.fill(Union([Box(298, 4, 302, 30), Box(291, 12, 309, 16)]), (30, 30, 40))
    rim(g, tw_open, 0, 2, k=0.6)
    g.fill(Box(248, 262, 352, 270), (40, 40, 52))
    # bats crossing the moon / the belfry openings (they cut the beams)
    for bx, by, bs in ((214, 226, 15), (330, 228, 11), (392, 286, 10), (226, 296, 8)):
        bat(g, bx, by, bs, up=0.15 if bs > 10 else -0.1)
    # the bell (left arch) + its yoke
    g.fill(Box(250, 200, 290, 204), (30, 28, 30))
    bell = Union([Poly([(258, 246), (262, 220), (270, 210), (280, 210), (288, 220), (292, 246)]), Ell(275, 246, 19, 4)])
    g.fill(bell, (30, 26, 24))
    rim(g, bell, -2, 0, col=(220, 200, 160), k=0.4)
    # gargoyle on the tower corner (difference)
    if "gargoyle" not in d:
        gx, gy = 384, 150
        gs = Union([Ell(gx, gy, 14, 9), Circ(gx + 14, gy - 6, 7), Poly([(gx + 16, gy - 12), (gx + 20, gy - 22), (gx + 21, gy - 10)]),
                    Poly([(gx - 6, gy - 6), (gx - 18, gy - 26), (gx + 4, gy - 8)]), Seg(gx + 18, gy - 4, gx + 26, gy - 1, 3, 2),
                    Seg(gx + 6, gy + 6, gx + 8, gy + 14, 4), Seg(gx - 8, gy + 6, gx - 10, gy + 14, 4)])
        g.fill(gs, (36, 36, 46))
        rim(g, gs, -2, 1, k=0.55)
    # castle tower (middle) with a lit window (difference)
    t2 = Union([Box(520, 150, 600, 460), Poly([(510, 154), (560, 52), (610, 154)])])
    g.fill(t2, ashlar((48, 48, 64), 14, 9, 1911))
    g.fill(Poly([(510, 154), (560, 52), (610, 154)]), tex(light_x((44, 40, 56), 510, 610, 1.3, 0.6), 0.2, 3, 8, 3, 1912))
    g.fill(Box(520, 150, 600, 460), (0, 0, 0), alpha=lambda X, Y: 0.2 + 0.4 * smooth(520, 600, X))
    rim(g, t2, 2, 1, k=0.4)
    w2 = arch(550, 570, 200, 230)
    if "window" not in d:
        g.fill(w2, rgrad(560, 220, 20, [(0, (255, 214, 140)), (1, (210, 120, 50))]))
        g.glow(560, 216, 26, (255, 170, 80), 0.35)
    else:
        g.fill(w2, (12, 12, 18))
    g.fill(arch(552, 568, 290, 312), (255, 190, 110))
    # far right spire with a pennant (difference)
    t3 = Union([Box(764, 160, 820, 460), Poly([(756, 164), (792, 60), (828, 164)])])
    g.fill(t3, ashlar((44, 44, 60), 12, 8, 1913))
    g.fill(t3, (0, 0, 0), alpha=0.35)
    rim(g, t3, 2, 1, k=0.3)
    g.fill(Seg(792, 62, 792, 22, 2), (40, 36, 40))
    if "flag" not in d:
        flag = Rough(Poly([(793, 24), (836, 30), (826, 38), (838, 46), (793, 46)]), 1.4, 4, 1914)
        g.fill(flag, light_y((150, 20, 34), 24, 46, 1.2, 0.7))
    g.fill(arch(786, 798, 260, 284), (255, 190, 110))
    # balcony: rail, balusters, plinth, floor
    g.fill(Box(-2, 540, W + 2, H + 2), persp_floor((450, 300), 540, (70, 68, 80), tile=50, depth=0.25, seed=1915))
    g.mul(Box(-2, 540, W + 2, H + 2), 0.4, alpha=lambda X, Y: smooth(540, 600, Y))
    for x in range(10, 900, 34):
        bal = Union([Ell(x + 12, 486, 9, 16), Box(x + 7, 464, x + 17, 532), Ell(x + 12, 468, 7, 4)])
        g.fill(bal, light_x((92, 90, 104), x + 2, x + 22, 1.35, 0.55))
    g.fill(Box(-2, 526, W + 2, 546), ashlar((88, 86, 100), 60, 20, 1916))
    g.fill(Box(-2, 444, W + 2, 462, 2), light_y((110, 108, 122), 444, 462, 1.25, 0.7))
    g.mul(Box(-2, 462, W + 2, 470), 0.5, feather=4)
    g.add(Box(-2, 444, W + 2, 447), MOONLIGHT, 0.3)
    # stone post with a lantern (left; difference)
    g.fill(Box(30, 400, 96, 546), ashlar((96, 94, 108), 33, 24, 1917))
    g.fill(Box(30, 400, 96, 546), (0, 0, 0), alpha=lambda X, Y: 0.1 + 0.4 * smooth(30, 96, X))
    g.fill(Box(24, 392, 102, 404, 2), light_y((116, 114, 128), 392, 404, 1.2, 0.7))
    if "lantern" not in d:
        lx, ly = 63, 360
        g.glow(lx, ly, 60, (255, 170, 80), 0.38)
        g.fill(Box(lx - 12, ly - 22, lx + 12, ly + 26, 2), (255, 200, 120))
        g.fill(Ell(lx, ly + 2, 5, 10), (255, 246, 210))
        for bx in (-13, 11):
            g.fill(Box(lx + bx, ly - 22, lx + bx + 2.4, ly + 26), (30, 28, 28))
        g.fill(Box(lx - 15, ly + 26, lx + 15, ly + 32, 1.5), (30, 28, 28))
        g.fill(Poly([(lx - 17, ly - 22), (lx, ly - 38), (lx + 17, ly - 22)]), (30, 28, 28))
        g.fill(Ell(lx, ly - 42, 5, 5) - Ell(lx, ly - 42, 2.5, 2.5), (30, 28, 28))
    # goblet + candle on the rail (goblet = difference) and an urn (difference) on the right
    if "goblet" not in d:
        gx = 420
        g.fill(Union([Ell(gx, 412, 13, 15) - Box(gx - 15, 380, gx + 15, 404), Box(gx - 2, 424, gx + 2, 442), Ell(gx, 443, 10, 3)]),
               sphere_paint(gx - 4, 416, 14, (196, 166, 86), amb=0.4, spec=0.8))
        g.fill(Ell(gx, 405, 12, 3), (120, 8, 24))
    candle(g, 476, 444, 30, w=8)
    if "urn" not in d:
        ux = 866
        g.fill(Union([Ell(ux, 418, 18, 18), Box(ux - 10, 432, ux + 10, 444), Box(ux - 14, 398, ux + 14, 404)]),
               sphere_paint(ux - 6, 414, 19, (110, 108, 122), amb=0.4, spec=0.2))
        g.fill(Rough(Ell(ux, 392, 14, 10), 2.5, 4, 1918), (40, 64, 42))
        for k in range(4):
            g.fill(Seg(ux - 8 + k * 6, 394, ux - 14 + k * 9, 420 + (k % 2) * 8, 1.4), (40, 64, 42))
    # the count himself, rose in hand (difference: rose colour), cape in the wind
    vampire(g, 650, 592, 340, rose=(190, 20, 36) if "rose" not in d else (236, 232, 220), rim_dx=2.6, wind=1.0)


L1519_RAYS = [dict(lx=M19[0], ly=M19[1], col=(170, 182, 232), k=1.6, region=Box(-2, -2, W + 2, 330), threshold=96,
                   soft=70, density=0.94, decay=0.982, samples=84, receive=moon_receive(*M19, floor=0.12))]

L1519_ELEMENTS = [
    bat_el("bat1", 420, 250, s=12, speed=-30, phase=0.0, bob=10),
    bat_el("bat2", 450, 272, s=9, speed=-30, phase=0.04, bob=8),
    bat_el("bat3", 160, 110, s=10, speed=26, phase=0.5),
    mist_el("mist1", 450, 380, 200, 10, (90, 96, 136), alpha=0.4, length=70, seed=31),
    beam_el("beam1", 330, 260, 500, 560, 40, 150, k=0.08, phase=0.2),
    beam_el("beam2", 280, 270, 160, 560, 40, 130, k=0.07, phase=0.7, speed=0.1),
    flame_el("f1", 476, 413, 1.1),
    glint_el("twinkle", [(60, 40), (480, 30), (700, 90), (880, 200), (140, 250), (660, 30)], col=(240, 240, 255), r=3, speed=0.6),
]

L1519_DIFFS = [
    ("gargoyle", 384, 144, 0),
    ("window", 560, 216, 0),
    ("flag", 814, 36, 0),
    ("lantern", 63, 360, 0),
    ("goblet", 420, 420, 0),
    ("rose", 598, 372, 0),
    ("urn", 866, 416, 0),
]


LEVELS = [
    ("Level1515", "月下废堡", make_bg(l1515_scene, L1515_RAYS), L1515_ELEMENTS, L1515_DIFFS, 60, OPTS),
    ("Level1516", "废堡大厅", make_bg(l1516_scene, L1516_RAYS), L1516_ELEMENTS, L1516_DIFFS, 60, OPTS),
    ("Level1517", "月夜墓地", make_bg(l1517_scene, L1517_RAYS), L1517_ELEMENTS, L1517_DIFFS, 60, OPTS),
    ("Level1518", "吸血鬼地穴", make_bg(l1518_scene, L1518_RAYS), L1518_ELEMENTS, L1518_DIFFS, 60, OPTS),
    ("Level1519", "吸血鬼伯爵", make_bg(l1519_scene, L1519_RAYS), L1519_ELEMENTS, L1519_DIFFS, 60, OPTS),
]
