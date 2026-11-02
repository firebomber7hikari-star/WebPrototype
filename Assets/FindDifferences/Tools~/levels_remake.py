# -*- coding: utf-8 -*-
"""Remakes of the first five levels (scene order 1-5: Level06 海港, Level07 秋林, Level08 野餐, Level09 小镇,
Level10 地下) in four render styles - 20 levels:
  Level1545-1549  卡通渲染 (toon: ink outlines, flat colour, one hard cool shadow)
  Level1550-1554  写实渲染 (realistic: textured, lit, soft shadows, grain, bloom)
  Level1555-1559  美漫渲染 (American comic: heavy black inks, flat colour, halftone shadow crescents)
  Level1560-1564  素描渲染 (pencil sketch: graphite tone + hatching on paper)

Each scene is written once against a small style interface and rendered by four Style classes:
  S.sky(g, stops, y1)                         S.obj(g, shape, col, seed, kind, depth, line, hi)
  S.flat(g, shape, col)  (details)            S.shadow(g, shape, k)
  S.water(g, shape, top, bottom, seed)        S.ground(g, shape, col, kind, seed)
  S.line(g, x0, y0, x1, y1, w, col)           S.glow(g, x, y, r, col, k)        S.finish(g)
The layouts and the differences follow the originals (same subjects, same difference ideas).
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from kit import drift_across
from real import (F32, Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, el, fbm, fbm1,
                  grain_tex, light_x, light_y, mixc, real_post, smooth, sphere_paint, tex, vgrad)
from toon import INK as TINK, Grow, cel, cloud_shape, shade_of, tint_of
from levels_isostyle import halftone
import levels_sketch as SKM


def _size(shape):
    b = shape.bbox()
    return b[2] - b[0], b[3] - b[1]


def _lum(col):
    return (0.3 * col[0] + 0.55 * col[1] + 0.15 * col[2]) / 255.0


# =================================================================== styles
class ToonS:
    name = "toon"
    haze = (210, 225, 245)

    def sky(self, g, stops, y1=H):
        g.fill(Box(-2, -2, W + 2, y1), vgrad(stops))

    def obj(self, g, shape, col, seed=0, kind="plain", depth=0.0, line=True, hi=False):
        w, h = _size(shape)
        o = -min(12, max(2, min(w, h) * 0.16))
        if depth:
            col = mixc(col, self.haze, depth * 0.45)
        lw = (2.0 * (1 - depth * 0.6)) if line else 0
        cel(g, shape, col, w=lw, off=(o, o), hi=hi, hi_off=(-o * 0.3, -o * 0.3))
        if kind == "wood":
            g.fill(shape, shade_of(col, 0.85), alpha=lambda X, Y: smooth(0.1, 0.0, np.abs((Y / 6.0) % 1.0 - 0.5) - 0.42) * 0.7)

    def flat(self, g, shape, col):
        g.fill(shape, col)

    def shadow(self, g, shape, k=1.0):
        g.mul(shape, 0.32 * k, tint=(70, 40, 150))

    def water(self, g, shape, top, bottom, seed=0, y0=None, y1=None):
        b = shape.bbox()
        g.fill(shape, vgrad([(b[1], top), (b[3], bottom)]))
        rnd = random.Random(seed)
        for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 2500)):
            x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
            g.fill(Inter(Seg(x, y, x + rnd.uniform(10, 34), y, 2), shape), (236, 248, 255), alpha=0.8)

    def ground(self, g, shape, col, kind="grass", seed=0, line=False):
        if line:
            g.fill(Grow(shape, 2), TINK)
        g.fill(shape, col)
        if kind == "grass":
            rnd = random.Random(seed)
            b = shape.bbox()
            ts = []
            for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 1800)):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                ts += [Seg(x - 3, y, x - 4, y - 6, 1.4), Seg(x, y, x, y - 8, 1.4), Seg(x + 3, y, x + 4, y - 6, 1.4)]
            if ts:
                g.fill(Inter(Union(ts), shape), shade_of(col, 0.82))
        elif kind == "dirt":
            rnd = random.Random(seed)
            b = shape.bbox()
            for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 2200)):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                g.fill(Inter(Ell(x, y, 3, 2), shape), shade_of(col, 0.8))

    def line(self, g, x0, y0, x1, y1, w=2.0, col=(80, 60, 50)):
        g.fill(Seg(x0, y0, x1, y1, w + 2.4), TINK)
        g.fill(Seg(x0, y0, x1, y1, w), col)

    def glow(self, g, x, y, r, col, k=0.4):
        g.glow(x, y, r, col, k)

    def finish(self, g):
        g.grade(contrast=1.03, sat=1.08)


class RealS:
    name = "real"
    haze = (200, 215, 235)

    def sky(self, g, stops, y1=H):
        g.fill(Box(-2, -2, W + 2, y1), vgrad(stops))

    def _paint(self, shape, col, kind, seed, round_):
        b = shape.bbox()
        x0, y0, x1, y1 = b
        if round_:
            sp = sphere_paint((x0 + x1) / 2 - (x1 - x0) * 0.05, (y0 + y1) / 2 - (y1 - y0) * 0.05, (x1 - x0) / 2 * 1.05, col,
                              ry=(y1 - y0) / 2 * 1.05, amb=0.38, spec=0.25 if kind != "foliage" else 0.05, wrap=0.3)
        else:
            lx = light_x(col, x0, x1, 1.12, 0.8)
            sp = lambda X, Y: lx(X, Y) * (1.08 - 0.16 * np.clip((Y - y0) / max(1, y1 - y0), 0, 1))[..., None]

        def p(X, Y):
            out = sp(X, Y)
            if kind == "wood":
                u = Y / 5.0
                out = out * (0.86 + 0.14 * smooth(0.0, 0.18, np.abs(u - np.floor(u) - 0.5)) + 0.12 * (fbm(X * 0.3, Y, 14, 1.4, 2, seed) - 0.5))[..., None]
            elif kind == "roof":
                u = Y / 4.0
                out = out * (0.82 + 0.18 * smooth(0.0, 0.25, np.abs(u - np.floor(u) - 0.5)))[..., None]
            elif kind == "stone":
                out = out * (0.8 + 0.3 * fbm(X, Y, 4, 4, 3, seed))[..., None]
            elif kind == "foliage":
                out = out * (0.6 + 0.65 * fbm(X, Y, 4, 4, 4, seed))[..., None]
            elif kind == "cloud":
                out = out * (0.95 + 0.1 * fbm(X, Y, 12, 8, 3, seed))[..., None]
            elif kind == "fabric":
                out = out * (0.93 + 0.1 * fbm(X, Y, 1.5, 1.5, 2, seed))[..., None]
            else:
                out = out * (0.94 + 0.1 * fbm(X, Y, 8, 8, 3, seed))[..., None]
            return out
        return grain_tex(p, 0.04, seed + 9)

    def obj(self, g, shape, col, seed=0, kind="plain", depth=0.0, line=True, hi=False):
        if depth:
            col = mixc(col, self.haze, depth * 0.5)
        g.fill(shape, self._paint(shape, col, kind, seed, hi), feather=0.6)
        if line and depth < 0.5:
            g.mul(Diff(shape, Grow(shape, -1.6)), 0.25, feather=0.8)

    def flat(self, g, shape, col):
        g.fill(shape, grain_tex(lambda X, Y: np.broadcast_to(C(col), X.shape + (3,)).copy(), 0.04, 5), feather=0.5)

    def shadow(self, g, shape, k=1.0):
        g.mul(shape, 0.45 * k, feather=6, tint=(30, 40, 70))

    def water(self, g, shape, top, bottom, seed=0):
        b = shape.bbox()

        def p(X, Y):
            t = np.clip((Y - b[1]) / max(1, b[3] - b[1]), 0, 1)
            base = C(top) + (C(bottom) - C(top)) * t[..., None]
            n = fbm(X, Y, 40 + 60 * t, 2 + 4 * t, 4, seed)
            out = base * (0.88 + 0.22 * n)[..., None]
            gl = smooth(0.66, 0.8, fbm(X, Y, 14, 2.2, 3, seed + 1))
            return out + C((235, 245, 250)) * (gl * 0.3)[..., None]
        g.fill(shape, p, feather=0.6)

    def ground(self, g, shape, col, kind="grass", seed=0, line=False):
        c = C(col)

        def p(X, Y):
            if kind == "grass":
                n = fbm(X, Y, 3, 3, 4, seed)
                return c * ((0.74 + 0.38 * n) * (0.9 + 0.2 * fbm(X, Y, 60, 40, 3, seed + 1)))[..., None]
            if kind == "dirt":
                n = fbm(X, Y, 4, 4, 4, seed)
                return c * (0.78 + 0.35 * n)[..., None]
            if kind == "road":
                return c * (0.88 + 0.14 * fbm(X, Y, 30, 30, 3, seed))[..., None]
            return c * (0.92 + 0.12 * fbm(X, Y, 10, 10, 3, seed))[..., None]
        g.fill(shape, grain_tex(p, 0.06 if kind in ("dirt", "road") else 0.04, seed + 3), feather=0.6)

    def line(self, g, x0, y0, x1, y1, w=2.0, col=(80, 60, 50)):
        g.fill(Seg(x0, y0, x1, y1, w), light_x(col, min(x0, x1) - w, max(x0, x1) + w, 1.15, 0.8))

    def glow(self, g, x, y, r, col, k=0.4):
        g.glow(x, y, r, col, k)

    def finish(self, g):
        g.bloom(225, 14, 0.3)
        g.grade(contrast=1.06, sat=1.05)


class ComicS:
    name = "comic"
    ink = (16, 14, 22)
    haze = (220, 230, 245)

    def sky(self, g, stops, y1=H):
        g.fill(Box(-2, -2, W + 2, y1), vgrad(stops))
        g.fill(Box(-2, -2, W + 2, y1), (255, 255, 255), alpha=lambda X, Y: halftone(lambda X, Y: 0.25 * smooth(y1 * 0.4, y1, Y), 6.0)(X, Y) * 0.6)

    def obj(self, g, shape, col, seed=0, kind="plain", depth=0.0, line=True, hi=False):
        w, h = _size(shape)
        o = -min(14, max(2, min(w, h) * 0.2))
        if depth:
            col = mixc(col, self.haze, depth * 0.5)
        if line:
            g.fill(Grow(shape, 2.8 * (1 - depth * 0.6)), self.ink)
        g.fill(shape, col)
        cres = Diff(shape, Moved(shape, o, o))
        g.fill(cres, tuple(c * 0.72 for c in col))
        g.fill(cres, self.ink, alpha=halftone(0.32, 4.6))
        if kind == "wood":
            g.fill(shape, self.ink, alpha=lambda X, Y: smooth(0.08, 0.0, np.abs((Y / 7.0) % 1.0 - 0.5) - 0.44) * 0.8)
        if hi and depth < 0.5:
            b = shape.bbox()
            g.fill(Ell(b[0] + w * 0.3, b[1] + h * 0.28, w * 0.12, h * 0.08), (255, 255, 255))

    def flat(self, g, shape, col):
        g.fill(shape, col)

    def shadow(self, g, shape, k=1.0):
        g.fill(shape, self.ink, alpha=0.5 * k)

    def water(self, g, shape, top, bottom, seed=0):
        b = shape.bbox()
        g.fill(shape, vgrad([(b[1], top), (b[3], bottom)]))
        g.fill(shape, self.ink, alpha=halftone(lambda X, Y: 0.22 * smooth(b[1], b[3], Y), 5.0))
        rnd = random.Random(seed)
        for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 3000)):
            x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
            g.fill(Inter(Seg(x, y, x + rnd.uniform(12, 30), y, 2.4), shape), (255, 255, 255))

    def ground(self, g, shape, col, kind="grass", seed=0, line=False):
        if line:
            g.fill(Grow(shape, 2.4), self.ink)
        g.fill(shape, col)
        g.fill(shape, self.ink, alpha=halftone(lambda X, Y: 0.2 * smooth(0.45, 0.7, fbm(X, Y, 70, 50, 2, seed)), 5.5))
        if kind == "grass":
            rnd = random.Random(seed)
            b = shape.bbox()
            ts = []
            for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 3000)):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                ts += [Seg(x - 3, y, x - 5, y - 7, 1.6), Seg(x + 2, y, x + 3, y - 8, 1.6)]
            if ts:
                g.fill(Inter(Union(ts), shape), self.ink)

    def line(self, g, x0, y0, x1, y1, w=2.0, col=(80, 60, 50)):
        g.fill(Seg(x0, y0, x1, y1, w + 3), self.ink)
        g.fill(Seg(x0, y0, x1, y1, w), col)

    def glow(self, g, x, y, r, col, k=0.4):
        g.fill(Circ(x, y, r * 0.55), col, alpha=0.35 * k / 0.4)
        g.fill(Circ(x, y, r * 0.55) - Circ(x, y, r * 0.5), self.ink, alpha=0.3)

    def finish(self, g):
        g.grade(contrast=1.06, sat=1.15)


class SketchS:
    name = "sketch"
    ink = SKM.LEAD

    def sky(self, g, stops, y1=H):
        SKM.paper(g, 4500)
        g.fill(Box(-2, -2, W + 2, y1), SKM.LEAD, alpha=lambda X, Y: 0.04 * smooth(y1, 0, Y))

    def obj(self, g, shape, col, seed=0, kind="plain", depth=0.0, line=True, hi=False):
        t = float(np.clip((1 - _lum(col)) * 0.8, 0.04, 0.85)) * (1 - depth * 0.6)
        b = shape.bbox()
        g.fill(shape, SKM.PAPER)
        SKM.tone(g, shape, t, seed, ang=50 if kind != "wood" else 2, grad=(b[0] + (b[2] - b[0]) * 0.3, b[2], 0.22 * (1 - depth)))
        if kind == "foliage":
            h3 = SKM.hatch(130, 2.8, seed=seed + 5)
            g.fill(shape, SKM.LEAD, alpha=lambda X, Y: h3(X, Y) * 0.4 * smooth(0.45, 0.7, fbm(X, Y, 6, 6, 3, seed)) * (1 - depth))
        if line:
            SKM.outline(g, shape, seed + 11, 1.1 * (1 - depth * 0.5), 1 - depth * 0.6)

    def flat(self, g, shape, col):
        t = float(np.clip((1 - _lum(col)) * 0.8, 0.0, 0.85))
        g.fill(shape, SKM.PAPER)
        SKM.tone(g, shape, t, 77, ang=30, cross=True)

    def shadow(self, g, shape, k=1.0):
        g.fill(shape, SKM.LEAD, alpha=0.12 * k)
        h = SKM.hatch(40, 2.8, seed=5)
        g.fill(shape, SKM.LEAD, alpha=lambda X, Y: h(X, Y) * 0.55 * k)

    def water(self, g, shape, top, bottom, seed=0):
        g.fill(shape, SKM.PAPER)
        hf = SKM.hatch(-2, 6.0, w=0.12, seed=seed, brk=0.5, seg=12)
        b = shape.bbox()
        g.fill(shape, SKM.LEAD, alpha=lambda X, Y: 0.08 + 0.12 * smooth(b[1], b[3], Y) + hf(X, Y) * 0.55)

    def ground(self, g, shape, col, kind="grass", seed=0, line=False):
        t = float(np.clip((1 - _lum(col)) * 0.6, 0.0, 0.7))
        g.fill(shape, SKM.PAPER)
        SKM.tone(g, shape, t, seed, ang=15, cross=False)
        if kind == "grass":
            rnd = random.Random(seed)
            b = shape.bbox()
            ts = []
            for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 1500)):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                ts += [Seg(x, y, x - 1.5, y - 6, 0.8), Seg(x + 2, y, x + 2.5, y - 7, 0.8)]
            if ts:
                g.fill(Inter(Union(ts), shape), SKM.LEAD, alpha=0.55)
        elif kind == "dirt":
            g.fill(shape, SKM.LEAD, alpha=lambda X, Y: 0.25 * smooth(0.62, 0.7, fbm(X, Y, 1.8, 1.8, 2, seed)))
        if line:
            SKM.outline(g, shape, seed + 3, 1.1, 0.8)

    def line(self, g, x0, y0, x1, y1, w=2.0, col=(80, 60, 50)):
        SKM.line(g, x0, y0, x1, y1, seed=int(x0 * 3 + y1), w=max(1.0, w * 0.6), k=0.85)

    def glow(self, g, x, y, r, col, k=0.4):
        for f in (0.45, 0.62):
            SKM.outline(g, Circ(x, y, r * f), int(x + y + f * 10), 0.8, 0.35)

    def finish(self, g):
        SKM.finish(g)


STYLES = [ToonS(), RealS(), ComicS(), SketchS()]
POSTS = {
    "toon": lambda rows, w, h, ox, oy, a: real_post(rows, w, h, ox, oy, a, grain=1.2, vignette=0.12),
    "real": lambda rows, w, h, ox, oy, a: real_post(rows, w, h, ox, oy, a, grain=4.0, vignette=0.2),
    "comic": lambda rows, w, h, ox, oy, a: real_post(rows, w, h, ox, oy, a, grain=1.6, vignette=0.14),
    "sketch": SKM.sketch_post,
}


# =================================================================== shared props
def cloud(S, g, x, y, w, h, seed=0):
    S.obj(g, cloud_shape(x, y, w, h, seed), (252, 252, 255), seed, kind="cloud")


def sun_rays(S, g, x, y, r, col=(255, 210, 70), face=False, seed=0):
    rays = Union([Poly([(x + math.cos(a - 0.12) * r * 1.1, y + math.sin(a - 0.12) * r * 1.1), (x + math.cos(a) * r * 1.6, y + math.sin(a) * r * 1.6),
                        (x + math.cos(a + 0.12) * r * 1.1, y + math.sin(a + 0.12) * r * 1.1)]) for a in np.linspace(0, math.tau, 12, endpoint=False)])
    S.obj(g, rays, (250, 180, 60), seed)
    S.glow(g, x, y, r * 3, (255, 230, 150), 0.3)
    S.obj(g, Circ(x, y, r), col, seed + 1, hi=True)
    if face:
        for e in (-1, 1):
            S.flat(g, Ell(x + e * r * 0.32, y - r * 0.1, r * 0.07, r * 0.12), (90, 60, 40))
        S.flat(g, Inter(Circ(x, y + r * 0.1, r * 0.4) - Circ(x, y + r * 0.02, r * 0.4), Box(x - r, y + r * 0.1, x + r, y + r)), (190, 80, 60))


def tree_round(S, g, x, base, h, col=(90, 160, 70), seed=0, trunk=(130, 90, 60), depth=0.0):
    S.obj(g, Box(x - h * 0.05, base - h * 0.5, x + h * 0.05, base, 2), trunk, seed, kind="wood", depth=depth)
    S.obj(g, Circ(x, base - h * 0.66, h * 0.3), col, seed + 1, kind="foliage", depth=depth, hi=True)


def pine(S, g, x, base, h, col=(70, 120, 70), seed=0, depth=0.0):
    S.obj(g, Box(x - h * 0.04, base - h * 0.2, x + h * 0.04, base), (120, 80, 60), seed, depth=depth)
    S.obj(g, Union([Poly([(x - h * 0.3 * (1 - k * 0.25), base - h * (0.15 + k * 0.25)), (x, base - h * (0.55 + k * 0.22)),
                          (x + h * 0.3 * (1 - k * 0.25), base - h * (0.15 + k * 0.25))]) for k in range(3)]), col, seed + 1, kind="foliage", depth=depth)


def treetop(S, g, x, y, r, col=(70, 140, 60), seed=0):
    """A tree seen from above: shadow to the lower right, layered crown."""
    S.shadow(g, Ell(x + r * 0.35, y + r * 0.35, r * 1.05, r), 0.8)
    S.obj(g, Union([Circ(x, y, r)] + [Circ(x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), r * 0.55) for a in np.linspace(0, math.tau, 6, endpoint=False)]),
          col, seed, kind="foliage", hi=True)
    S.obj(g, Circ(x - r * 0.15, y - r * 0.15, r * 0.45), tint_of(col, 0.2), seed + 1, kind="foliage", line=False)


# =================================================================== scene 1: harbour (Level06)
def harbour(g, S, d):
    S.sky(g, [(0, (110, 190, 242)), (300, (206, 234, 250))], 330)
    sun_rays(S, g, 112, 80, 36, face=True, seed=5001)
    for k, (x, y, w, h) in enumerate(((300, 70, 56, 20), (560, 46, 66, 22), (860, 120, 40, 14))):
        if k == 1 and "cloud" in d:
            continue
        cloud(S, g, x, y, w, h, 5002 + k)
    for x, y in ((260, 110), (290, 120), (630, 100)):
        S.line(g, x - 9, y - 4, x, y, 1.6, (60, 70, 90))
        S.line(g, x, y, x + 9, y - 4, 1.6, (60, 70, 90))
    # distant hills, left hill with houses, right cliff with lighthouse
    S.obj(g, Poly([(260, 330), (330, 250), (400, 270), (470, 236), (560, 260), (640, 240), (700, 330)]), (110, 170, 170), 5010, depth=0.6)
    S.obj(g, Poly([(-4, 340), (-4, 196), (60, 186), (240, 192), (300, 240), (360, 340)]), (110, 190, 90), 5011, kind="grass")
    houses = [(36, 190, (230, 210, 180), (220, 80, 70)), (118, 186, (240, 236, 220), (70, 120, 200) if "roof" not in d else (240, 180, 40)),
              (200, 176, (250, 230, 160), (80, 160, 90))]
    for k, (x, base, wall, roof) in enumerate(houses):
        S.shadow(g, Box(x + 6, base - 4, x + 58, base + 4), 0.6)
        S.obj(g, Box(x, base - 34, x + 46, base), wall, 5012 + k)
        S.obj(g, Poly([(x - 6, base - 32), (x + 23, base - 60), (x + 52, base - 32)]), roof, 5015 + k, kind="roof")
        S.obj(g, Box(x + 18, base - 18, x + 28, base), (130, 80, 60), 5018 + k, line=True)
        S.obj(g, Box(x + 6, base - 28, x + 15, base - 19), (150, 210, 240), 5021 + k, line=False)
    for k, x in enumerate((20, 100, 182, 270)):
        tree_round(S, g, x, 200 - (8 if k == 3 else 0), 40, (90, 170, 80), 5024 + k)
    cliff = Poly([(600, 340), (660, 250), (760, 244), (904, 236), (904, 340)])
    S.obj(g, cliff, (170, 130, 90), 5030, kind="stone")
    S.obj(g, Poly([(660, 252), (760, 244), (904, 236), (904, 254), (760, 262), (650, 266)]), (110, 190, 90), 5031, kind="grass")
    lx, lb, lt = 780, 250, 108
    tower = Poly([(lx - 20, lb), (lx + 20, lb), (lx + 13, lt), (lx - 13, lt)])
    S.obj(g, tower, (250, 248, 240), 5032)
    sc = (220, 50, 50) if "stripes" not in d else (30, 50, 110)
    for y0 in (130, 170, 210):
        t0, t1 = (y0 - lt) / (lb - lt), (y0 + 20 - lt) / (lb - lt)
        S.flat(g, Poly([(lx - 13 - 7 * t0, y0), (lx + 13 + 7 * t0, y0), (lx + 13 + 7 * t1, y0 + 20), (lx - 13 - 7 * t1, y0 + 20)]), sc)
    S.obj(g, Box(lx - 16, lt - 6, lx + 16, lt, 1), (60, 60, 70), 5033)
    S.obj(g, Box(lx - 10, lt - 26, lx + 10, lt - 6), (255, 236, 150), 5034, hi=True)
    S.obj(g, Poly([(lx - 15, lt - 26), (lx, lt - 44), (lx + 15, lt - 26)]), (220, 50, 50), 5035)
    S.glow(g, lx, lt - 16, 40, (255, 240, 180), 0.4)
    # sea bands (back -> boat -> mid -> fish / buoy -> front)
    def band(y0, amp, ph):
        return Under(lambda x: y0 - amp * np.abs(np.sin(x * 0.032 + ph)), -10, W + 10, H + 10)
    S.water(g, band(312, 10, 0.3), (120, 200, 236), (80, 170, 220), 5040)
    # sailboat (difference: sail colour)
    bx, by = 340, 336
    S.obj(g, Poly([(bx - 60, by - 22), (bx + 64, by - 22), (bx + 46, by + 4), (bx - 44, by + 4)]), (220, 60, 50), 5041)
    S.flat(g, Box(bx - 54, by - 16, bx + 58, by - 11), (255, 255, 255))
    S.line(g, bx, by - 22, bx, by - 130, 2.4, (120, 90, 60))
    S.obj(g, Poly([(bx + 3, by - 124), (bx + 3, by - 28), (bx + 58, by - 28)]), (250, 246, 230) if "sail" not in d else (250, 200, 60), 5042)
    S.obj(g, Poly([(bx - 3, by - 110), (bx - 3, by - 28), (bx - 44, by - 28)]), (250, 246, 230), 5043)
    S.obj(g, Poly([(bx, by - 130), (bx + 22, by - 124), (bx, by - 118)]), (230, 60, 60), 5044)
    S.water(g, band(380, 12, 1.4), (90, 180, 230), (60, 150, 214), 5045)
    if "fish" not in d:
        fx, fy = 310, 400
        S.obj(g, Poly([(fx + 22, fy - 2), (fx + 40, fy - 14), (fx + 36, fy + 8)]), (250, 140, 40), 5046)
        S.obj(g, Ell(fx, fy, 26, 14), (250, 150, 50), 5047, hi=True)
        S.flat(g, Circ(fx - 14, fy - 3, 3), (30, 30, 40))
    if "buoy" not in d:
        ux, uy = 640, 428
        S.obj(g, Union([Ell(ux, uy, 18, 20), Box(ux - 3, uy - 34, ux + 3, uy - 16)]), (230, 60, 60), 5048, hi=True)
        S.flat(g, Box(ux - 18, uy - 4, ux + 18, uy + 4), (255, 255, 255))
    S.water(g, band(458, 14, 2.2), (70, 160, 222), (40, 120, 196), 5049)
    S.water(g, band(540, 16, 0.8), (50, 130, 206), (30, 96, 176), 5050)


def harbour_elements(S):
    return [
        E("cloud_m", el(lambda g, m: cloud(S, g, 760, 60, 44, 15, 5060)), pivot=(760, 60), anim=drift_across(716, 804, -6, start=0.0)),
        E("gull", el(lambda g, m: (S.line(g, 461, 136, 470, 140, 1.6, (60, 70, 90)), S.line(g, 470, 140, 479, 136, 1.6, (60, 70, 90)))),
          pivot=(470, 140), anim=dict(drift_across(461, 479, 22), stretch=(0, 0.5), scaleSpeed=2.2)),
        E("beam", el(lambda g, m: S.glow(g, 840, 92, 70, (255, 246, 200), 0.5)), daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=0.4)),
        E("glint", el(lambda g, m: [S.glow(g, x, y, 6, (255, 255, 255), 0.8) for x, y in ((150, 420), (520, 500), (780, 430), (420, 560))]),
          daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=0.6)),
    ]


HARBOUR_DIFFS = [("cloud", 560, 40, 0), ("roof", 141, 140, 0), ("stripes", 780, 170, 0), ("sail", 370, 260, 0), ("fish", 314, 400, 0), ("buoy", 640, 420, 0)]


# =================================================================== scene 2: autumn forest (Level07)
def autumn(g, S, d):
    S.sky(g, [(0, (250, 226, 196)), (260, (240, 190, 160))], 300)
    for k in range(4):
        S.obj(g, Circ(500, 60, 44 - k * 10), ((250, 160, 110), (250, 130, 90), (240, 110, 80), (230, 90, 70))[k], 5101 + k, line=(k == 0))
    cloud(S, g, 160, 90, 50, 18, 5105)
    cloud(S, g, 820, 60, 50, 16, 5106)
    if "balloon" not in d:
        bx, by = 190, 150
        env = Union([Ell(bx, by, 28, 32), Poly([(bx - 20, by + 18), (bx + 20, by + 18), (bx + 7, by + 42), (bx - 7, by + 42)])])
        S.obj(g, env, (120, 170, 230), 5107, hi=True)
        S.flat(g, Inter(env, Box(bx - 30, by - 6, bx + 30, by + 4)), (250, 250, 240))
        S.line(g, bx - 7, by + 42, bx - 6, by + 52, 1.2, (90, 70, 50))
        S.line(g, bx + 7, by + 42, bx + 6, by + 52, 1.2, (90, 70, 50))
        S.obj(g, Box(bx - 8, by + 51, bx + 8, by + 62, 2), (170, 120, 70), 5108, kind="wood")
    for x, y in ((420, 110), (444, 98), (470, 112)):
        S.line(g, x - 8, y - 3, x, y, 1.6, (90, 60, 60))
        S.line(g, x, y, x + 8, y - 3, 1.6, (90, 60, 60))
    layers = [(230, 30, (226, 160, 140), 0.55, 5110), (286, 34, (206, 130, 110), 0.35, 5111), (350, 30, (180, 100, 90), 0.18, 5112),
              (430, 26, (150, 80, 76), 0.0, 5113)]
    for li, (base, amp, col, depth, sd) in enumerate(layers):
        f = (lambda base=base, amp=amp, sd=sd: (lambda x: base - amp * (0.5 + 0.5 * np.sin(x * 0.009 + sd)) - 10 * fbm1(x, 60, 2, sd)))()
        S.obj(g, Under(f, -10, W + 10, H + 10), col, sd, kind="grass", depth=depth)
        rnd = random.Random(sd)
        for k in range(9 - li):
            x = rnd.uniform(20, 880)
            top = float(f(np.array([x], F32))[0])
            if li == 1 and k == 3:
                x, top = 402, float(f(np.array([402.0], F32))[0])
                if "pine" in d:
                    continue
            if rnd.random() < 0.55 or (li == 1 and k == 3):
                pine(S, g, x, top + 6, 70 - li * 4, mixc((170, 70, 60), (90, 60, 50), li / 4), sd + 20 + k, depth=depth)
            else:
                tree_round(S, g, x, top + 6, 64 - li * 4, (240, 140, 50), sd + 40 + k, depth=depth)
    # cottage with window glow (difference) and pinwheel
    hx, hb = 730, 330
    S.shadow(g, Box(hx + 6, hb - 4, hx + 110, hb + 6), 0.6)
    S.obj(g, Box(hx, hb - 60, hx + 90, hb), (250, 230, 190), 5120)
    S.obj(g, Box(hx + 64, hb - 106, hx + 78, hb - 70), (170, 90, 70), 5121)
    S.obj(g, Poly([(hx - 10, hb - 56), (hx + 45, hb - 104), (hx + 100, hb - 56)]), (220, 70, 60), 5122, kind="roof")
    S.obj(g, Box(hx + 54, hb - 40, hx + 76, hb), (140, 90, 60), 5123, kind="wood")
    win = Box(hx + 12, hb - 44, hx + 40, hb - 20)
    if "window" not in d:
        S.glow(g, hx + 26, hb - 32, 40, (255, 200, 110), 0.45)
        S.obj(g, win, (255, 214, 120), 5124)
    else:
        S.obj(g, win, (90, 110, 140), 5124)
    S.line(g, hx + 26, hb - 44, hx + 26, hb - 20, 1.6, (140, 90, 60))
    S.line(g, hx + 12, hb - 32, hx + 40, hb - 32, 1.6, (140, 90, 60))
    if "pinwheel" not in d:
        px, py = 690, 270
        S.line(g, px, py, px, py + 64, 2.2, (150, 110, 70))
        for k, col in enumerate(((240, 80, 80), (80, 160, 240), (250, 210, 60), (90, 190, 110))):
            a = k * math.pi / 2
            S.obj(g, Poly([(px, py), (px + math.cos(a) * 24, py + math.sin(a) * 24), (px + math.cos(a + 0.9) * 18, py + math.sin(a + 0.9) * 18)]), col, 5125 + k)
    # foreground: mushroom (difference), rabbit (difference), bushes, fox
    if "mushroom" not in d:
        mx, my = 120, 480
        S.obj(g, Box(mx - 8, my - 4, mx + 8, my + 30, 3), (250, 240, 220), 5130)
        cap = Inter(Ell(mx, my, 34, 24), Box(mx - 36, my - 26, mx + 36, my + 2))
        S.obj(g, cap, (220, 50, 50), 5131, hi=True)
        for dx, dy in ((-16, -8), (6, -16), (18, -6)):
            S.flat(g, Ell(mx + dx, my + dy, 5, 3.6), (255, 255, 255))
    if "rabbit" not in d:
        rx, ry = 440, 468
        S.obj(g, Ell(rx, ry, 20, 15), (250, 250, 246), 5132, hi=True)
        S.obj(g, Circ(rx + 14, ry - 16, 10), (250, 250, 246), 5133)
        for e in (-4, 4):
            S.obj(g, Ell(rx + 14 + e, ry - 36, 4, 12), (250, 250, 246), 5134 + e)
        S.flat(g, Circ(rx + 18, ry - 17, 1.8), (30, 30, 40))
    for k, (x, y, r) in enumerate(((250, 500, 26), (600, 512, 30), (860, 500, 26))):
        S.obj(g, Union([Circ(x - r * 0.6, y, r * 0.8), Circ(x + r * 0.6, y, r * 0.8), Circ(x, y - r * 0.4, r)]), (80, 120, 70), 5136 + k, kind="foliage")
    fx, fy = 760, 520
    S.obj(g, Ell(fx, fy, 30, 13), (240, 120, 50), 5140)
    S.obj(g, Poly([(fx + 22, fy - 8), (fx + 50, fy - 16), (fx + 36, fy + 2)]), (240, 120, 50), 5141)
    S.obj(g, Poly([(fx - 28, fy - 4), (fx - 64, fy - 18), (fx - 50, fy + 8)]), (240, 120, 50), 5142)
    S.flat(g, Poly([(fx - 58, fy - 14), (fx - 64, fy - 18), (fx - 54, fy - 6)]), (255, 255, 255))
    for lx in (-16, 14):
        S.line(g, fx + lx, fy + 10, fx + lx, fy + 26, 2.6, (60, 40, 40))


def autumn_elements(S):
    return [
        E("smoke", el(lambda g, m: S.obj(g, Circ(801, 214, 9), (240, 236, 236), 5150, kind="cloud")),
          anim=dict(driftVelocity=(8, 40), driftLength=70, driftFade=True, driftGrow=1.6)),
        E("smoke2", el(lambda g, m: S.obj(g, Circ(801, 214, 7), (240, 236, 236), 5151, kind="cloud")),
          anim=dict(driftVelocity=(10, 40), driftLength=70, driftFade=True, driftGrow=1.6, phase=0.5)),
        E("leaf", el(lambda g, m: S.obj(g, Ell(560, 160, 7, 4), (230, 120, 40), 5152, line=False)),
          anim=dict(driftVelocity=(16, -50), driftLength=260, driftFade=True, swingAngle=40, swingSpeed=0.7)),
        E("leaf2", el(lambda g, m: S.obj(g, Ell(320, 200, 6, 3.4), (220, 80, 50), 5153, line=False)),
          anim=dict(driftVelocity=(-10, -44), driftLength=240, driftFade=True, swingAngle=50, swingSpeed=0.6, phase=0.4)),
    ]


AUTUMN_DIFFS = [("balloon", 190, 160, 0), ("pine", 402, 290, 0), ("window", 756, 298, 0), ("pinwheel", 690, 276, 0), ("mushroom", 120, 476, 0),
                ("rabbit", 446, 456, 0)]


# =================================================================== scene 3: picnic seen from above (Level08)
def _rot(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def picnic(g, S, d):
    S.ground(g, Box(-2, -2, W + 2, H + 2), (120, 196, 90), "grass", 5201)
    rnd = random.Random(5202)
    for _ in range(9):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        S.flat(g, Rough(Ell(x, y, rnd.uniform(60, 110), rnd.uniform(40, 70)), 8, 30, int(x)), (140, 206, 100))
    # pond with lily pads and koi (difference: one koi)
    S.obj(g, Ell(800, 110, 160, 96), (220, 210, 170), 5203, kind="stone")
    S.water(g, Ell(800, 110, 140, 80), (110, 190, 230), (60, 140, 200), 5204)
    for k, (x, y) in enumerate(((760, 70), (860, 150), (720, 150))):
        S.obj(g, Ell(x, y, 16, 11) - Poly([(x, y), (x + 20, y - 6), (x + 20, y + 2)]), (90, 170, 80), 5205 + k)
    for k, (x, y, a) in enumerate(((694, 128, 1.8), (870, 96, -0.4))):
        if k == 1 and "koi" in d:
            continue
        body = Poly(_rot([(x - 16, y), (x - 6, y - 7), (x + 10, y - 5), (x + 16, y), (x + 10, y + 5), (x - 6, y + 7)], x, y, a))
        S.obj(g, body, (250, 140, 50) if k else (250, 250, 246), 5208 + k, hi=True)
        S.obj(g, Poly(_rot([(x + 14, y), (x + 26, y - 7), (x + 26, y + 7)], x, y, a)), (250, 140, 50), 5210 + k)
        S.flat(g, Circ(*_rot([(x - 4, y)], x, y, a)[0], 3.5), (240, 80, 60))
    # trees in the corners
    for k, (x, y, r) in enumerate(((60, 60, 60), (250, 40, 48), (70, 300, 52), (880, 560, 64), (40, 560, 40), (600, 40, 34))):
        treetop(S, g, x, y, r, (60, 140, 60) if k % 2 else (70, 150, 66), 5220 + k)
    # picnic blanket (gingham)
    bc, ba = (650, 330), -0.18
    blank = Poly(_rot([(520, 230), (790, 230), (790, 430), (520, 430)], *bc, ba))
    S.shadow(g, Moved(blank, 8, 8), 0.6)
    S.obj(g, blank, (250, 248, 240), 5230, kind="fabric")
    for k in range(9):
        x = 520 + k * 30
        S.flat(g, Inter(blank, Poly(_rot([(x, 230), (x + 15, 230), (x + 15, 430), (x, 430)], *bc, ba))), (230, 70, 70))
    for k in range(7):
        y = 230 + k * 30
        S.flat(g, Inter(blank, Poly(_rot([(520, y), (790, y), (790, y + 15), (520, y + 15)], *bc, ba))), (236, 110, 110))
    # basket, sandwich plate (difference), strawberries, watermelon, cup
    S.shadow(g, Ell(572, 262, 50, 36), 0.7)
    S.obj(g, Ell(566, 256, 48, 34), (190, 140, 80), 5240, kind="wood", hi=True)
    S.obj(g, Ell(566, 252, 36, 24), (160, 110, 60), 5241, kind="wood")
    S.flat(g, Box(552, 240, 584, 262, 2), (250, 250, 250))
    for k, (x, y) in enumerate(((680, 236), (600, 340), (752, 330), (660, 376))):
        r = 30 if k < 3 else 14
        S.shadow(g, Circ(x + 5, y + 5, r), 0.6)
        S.obj(g, Circ(x, y, r), (250, 250, 250), 5245 + k, hi=True)
    if "sandwich" not in d:
        S.obj(g, Poly([(664, 250), (700, 248), (676, 218)]), (240, 210, 140), 5250)
        S.flat(g, Poly([(668, 246), (696, 244), (676, 224)]), (140, 190, 80))
    for dx, dy in ((-10, -6), (8, -8), (-2, 8), (12, 6)):
        S.obj(g, Circ(600 + dx, 340 + dy, 6), (230, 50, 60), 5251, hi=True)
    S.obj(g, Inter(Circ(752, 330, 22), Box(726, 330, 778, 356)), (230, 70, 80), 5252)
    S.flat(g, Inter(Circ(752, 330, 22) - Circ(752, 330, 18), Box(726, 330, 778, 356)), (90, 170, 80))
    S.obj(g, Circ(660, 376, 9), (130, 80, 50), 5253)
    # frisbee (difference), flower bed (difference: one flower), ants (difference)
    if "frisbee" not in d:
        S.shadow(g, Ell(448, 418, 30, 26), 0.6)
        S.obj(g, Circ(440, 410, 28), (250, 150, 40), 5260, hi=True)
        S.flat(g, Circ(440, 410, 20) - Circ(440, 410, 16), (255, 210, 120))
    bed = Box(40, 470, 230, 590, 16)
    S.obj(g, bed, (130, 90, 60), 5261, kind="dirt")
    for k, (x, y, col) in enumerate(((70, 500, (240, 90, 140)), (120, 520, (250, 210, 60)), (176, 556, (240, 120, 200)), (90, 566, (250, 140, 60)),
                                     (200, 500, (255, 255, 255)), (150, 488, (240, 90, 140)))):
        if k == 2 and "flower" in d:
            continue
        S.obj(g, Union([Circ(x + 9 * math.cos(a), y + 9 * math.sin(a), 7) for a in np.linspace(0, math.tau, 5, endpoint=False)]), col, 5262 + k)
        S.flat(g, Circ(x, y, 4.5), (250, 190, 60))
    if "ants" not in d:
        for k in range(8):
            x, y = 770 + math.sin(k * 0.8) * 8, 452 + k * 10
            S.obj(g, Union([Circ(x, y, 2.6), Circ(x, y + 4, 2.2), Circ(x, y - 4, 2.0)]), (40, 30, 30), 5270 + k, line=False)


def picnic_elements(S):
    def bfly(g, m, x=330, y=180, col=(250, 140, 200)):
        for e in (-1, 1):
            S.obj(g, Ell(x + e * 7, y, 7, 9), col, 5280, line=True)
        S.flat(g, Ell(x, y, 2, 7), (50, 40, 40))
    return [
        E("butterfly", el(bfly), pivot=(330, 180), anim=dict(orbitRadius=(80, 40), orbitSpeed=0.1, stretch=(0.6, 0), scaleSpeed=3.5)),
        E("butterfly2", el(lambda g, m: bfly(g, m, 330, 520, (250, 220, 80))), pivot=(330, 520), anim=dict(orbitRadius=(60, 30), orbitSpeed=-0.12, stretch=(0.6, 0), scaleSpeed=3.2)),
        E("ripple", el(lambda g, m: [S.flat(g, Circ(x, y, 9) - Circ(x, y, 7.5), (230, 245, 255)) for x, y in ((820, 90), (760, 130))]),
          anim=dict(pulse=0.3, twinkle=0.7, twinkleSpeed=0.5)),
    ]


PICNIC_DIFFS = [("koi", 874, 96, 0), ("sandwich", 682, 236, 0), ("frisbee", 440, 410, 0), ("flower", 176, 556, 0), ("ants", 772, 488, 0)]


# =================================================================== scene 4: little town seen from above (Level09)
def roof_top(S, g, x0, y0, x1, y1, col, seed, chimney=True):
    S.shadow(g, Box(x0 + 8, y0 + 8, x1 + 8, y1 + 8), 0.7)
    S.obj(g, Box(x0, y0, x1, y1, 2), col, seed, kind="roof")
    if (x1 - x0) > (y1 - y0):
        S.flat(g, Box(x0 + 4, (y0 + y1) / 2 - 1.5, x1 - 4, (y0 + y1) / 2 + 1.5), shade_of(col, 0.75))
    else:
        S.flat(g, Box((x0 + x1) / 2 - 1.5, y0 + 4, (x0 + x1) / 2 + 1.5, y1 - 4), shade_of(col, 0.75))
    if chimney:
        S.obj(g, Box(x1 - 22, y0 + 8, x1 - 10, y0 + 20), (150, 110, 100), seed + 1)


def car_top(S, g, x, y, col, vertical=False, seed=0):
    if vertical:
        S.shadow(g, Box(x - 7, y - 12, x + 11, y + 16, 3), 0.6)
        S.obj(g, Box(x - 9, y - 16, x + 9, y + 16, 5), col, seed, hi=True)
        S.flat(g, Box(x - 6, y - 8, x + 6, y + 2, 2), (150, 200, 230))
    else:
        S.shadow(g, Box(x - 12, y - 7, x + 16, y + 11, 3), 0.6)
        S.obj(g, Box(x - 16, y - 9, x + 16, y + 9, 5), col, seed, hi=True)
        S.flat(g, Box(x - 2, y - 6, x + 8, y + 6, 2), (150, 200, 230))


def town(g, S, d):
    S.ground(g, Box(-2, -2, W + 2, H + 2), (126, 196, 96), "grass", 5301)
    # river (right) and roads
    river = Poly([(640, -4), (720, -4), (700, 120), (730, 260), (700, 420), (740, 604), (650, 604), (620, 420), (650, 260), (622, 120)])
    S.obj(g, Grow(river, 8), (220, 210, 170), 5302, kind="stone", line=False)
    S.water(g, river, (110, 180, 230), (70, 150, 210), 5303)
    S.ground(g, Box(220, -4, 270, H + 4), (110, 110, 116), "road", 5304, line=True)
    S.ground(g, Box(-4, 270, W + 4, 320), (110, 110, 116), "road", 5305, line=True)
    S.ground(g, Box(220, 270, 270, 320), (110, 110, 116), "road", 5306)
    for y in range(0, 600, 40):
        if not 260 < y < 330:
            S.flat(g, Box(243, y, 247, y + 20), (250, 250, 240))
    for x in range(0, 900, 44):
        if not (210 < x < 280 or 600 < x < 760):
            S.flat(g, Box(x, 293, x + 22, 297), (250, 250, 240))
    for k in range(5):
        S.flat(g, Box(224 + k * 10, 250, 230 + k * 10, 266), (250, 250, 250))
        S.flat(g, Box(274, 274 + k * 10, 290, 280 + k * 10), (250, 250, 250))
    S.shadow(g, Box(620, 276, 760, 330), 0.6)
    S.obj(g, Box(612, 268, 752, 322, 3), (196, 190, 180), 5307, kind="stone")
    for y in (268, 316):
        S.flat(g, Box(612, y, 752, y + 6), (150, 146, 140))
    # buildings (roofs from above): difference = one roof colour
    roofs = [(20, 40, 100, 110, (220, 80, 70)), (130, 40, 200, 140, (220, 80, 70) if "roof" not in d else (250, 226, 130)),
             (40, 160, 150, 230, (240, 200, 70)), (300, 40, 400, 110, (90, 160, 100)), (430, 40, 500, 150, (230, 130, 190)),
             (310, 150, 420, 220, (90, 140, 220)), (40, 556, 200, 604, (190, 120, 90))]
    for k, (x0, y0, x1, y1, col) in enumerate(roofs):
        roof_top(S, g, x0, y0, x1, y1, col, 5310 + k * 3, chimney=k != 6)
    # fountain plaza (top right)
    S.obj(g, Circ(820, 130, 76), (220, 214, 200), 5330, kind="stone")
    S.obj(g, Circ(820, 130, 44), (200, 196, 190), 5331, kind="stone")
    S.water(g, Circ(820, 130, 38), (120, 200, 240), (80, 160, 220), 5332)
    S.obj(g, Circ(820, 130, 8), (220, 214, 200), 5333)
    # pool with lanes and a parasol (difference)
    S.obj(g, Box(40, 390, 230, 520, 4), (236, 236, 230), 5340, kind="stone")
    S.water(g, Box(54, 404, 216, 506), (110, 200, 240), (70, 170, 230), 5341)
    for y in (436, 470):
        S.flat(g, Box(56, y, 214, y + 2), (250, 120, 80))
    if "umbrella" not in d:
        ux, uy = 270, 410
        S.shadow(g, Circ(ux + 10, uy + 10, 34), 0.6)
        for k in range(8):
            a0, a1 = k * math.tau / 8, (k + 1) * math.tau / 8
            S.obj(g, Poly([(ux, uy), (ux + math.cos(a0) * 34, uy + math.sin(a0) * 34), (ux + math.cos(a1) * 34, uy + math.sin(a1) * 34)]),
                  (230, 60, 60) if k % 2 else (255, 255, 255), 5345 + k, line=k == 0)
        S.flat(g, Circ(ux, uy, 4), (150, 150, 150))
    # parking lot with cars (difference: one parked car)
    S.ground(g, Box(300, 390, 560, 594, 6), (100, 100, 106), "road", 5350, line=True)
    for x in range(310, 560, 40):
        S.flat(g, Box(x, 400, x + 3, 450), (250, 250, 240))
        S.flat(g, Box(x, 534, x + 3, 584), (250, 250, 240))
    for k, (x, y, col) in enumerate(((330, 426, (220, 60, 60)), (370, 426, (250, 250, 250)), (450, 426, (60, 120, 220)), (330, 560, (90, 170, 90)),
                                     (410, 560, (250, 210, 60)), (490, 560, (180, 180, 190)), (530, 560, (220, 110, 60)))):
        if k == 6 and "parkedcar" in d:
            continue
        car_top(S, g, x, y, col, vertical=True, seed=5355 + k)
    # trees, boat on the river (difference), bench (difference)
    for k, (x, y, r) in enumerate(((180, 190, 26), (300, 250, 22), (450, 200, 26), (560, 60, 30), (600, 210, 26), (20, 350, 24), (560, 360, 22),
                                   (870, 300, 30), (860, 470, 30), (800, 560, 30), (190, 340, 20))):
        if k == 10 and "tree" in d:
            continue
        treetop(S, g, x, y, r, (70, 150, 66), 5370 + k)
    if "boat" not in d:
        S.obj(g, Poly([(680, 500), (692, 520), (690, 560), (670, 560), (668, 520)]), (180, 120, 70), 5385, kind="wood", hi=True)
        S.flat(g, Box(672, 528, 688, 534), (130, 90, 50))
    if "bench" not in d:
        S.shadow(g, Box(568, 248, 610, 262), 0.6)
        S.obj(g, Box(560, 240, 604, 254, 2), (170, 120, 70), 5386, kind="wood")


def town_elements(S):
    return [
        E("car_h", el(lambda g, m: car_top(S, g, 100, 284, (230, 60, 60), False, 5390)), anim=dict(driftVelocity=(40, 0), driftLength=900, driftStart=-200)),
        E("car_h2", el(lambda g, m: car_top(S, g, 800, 306, (60, 120, 220), False, 5391)), anim=dict(driftVelocity=(-34, 0), driftLength=900, driftStart=-100)),
        E("car_v", el(lambda g, m: car_top(S, g, 232, 500, (250, 210, 60), True, 5392)), anim=dict(driftVelocity=(0, 30), driftLength=600, driftStart=-100)),
        E("swimmer", el(lambda g, m: (S.obj(g, Ell(110, 452, 16, 6), (230, 190, 160), 5393, line=True), S.obj(g, Circ(124, 452, 5), (240, 80, 70), 5394))),
          anim=dict(bobAmplitude=(40, 0), bobSpeed=0.1)),
        E("spray", el(lambda g, m: [S.flat(g, Circ(820 + 16 * math.cos(a), 130 + 16 * math.sin(a), 3), (240, 250, 255)) for a in np.linspace(0, math.tau, 8, endpoint=False)]),
          anim=dict(pulse=0.3, scaleSpeed=1.0, twinkle=0.5, twinkleSpeed=0.8), pivot=(820, 130)),
    ]


TOWN_DIFFS = [("roof", 165, 90, 0), ("umbrella", 270, 410, 0), ("parkedcar", 530, 560, 0), ("boat", 680, 530, 0), ("tree", 190, 340, 0), ("bench", 582, 247, 0)]


# =================================================================== scene 5: cross-section underground (Level10)
def underground(g, S, d):
    S.sky(g, [(0, (130, 200, 245)), (200, (210, 236, 250))], 212)
    cloud(S, g, 270, 50, 50, 18, 5401)
    cloud(S, g, 520, 76, 40, 14, 5402)
    sun_rays(S, g, 850, 64, 32, seed=5403)
    # soil layers
    def lay(y0, amp, sd):
        return lambda x: y0 + amp * np.sin(x * 0.01 + sd) + 8 * fbm1(x, 50, 2, sd)
    S.ground(g, Box(-4, 208, W + 4, H + 4), (160, 110, 70), "dirt", 5404)
    S.ground(g, Under(lay(330, 14, 1), -10, W + 10, H + 10), (140, 92, 56), "dirt", 5405)
    S.ground(g, Under(lay(450, 16, 2), -10, W + 10, H + 10), (116, 74, 46), "dirt", 5406)
    rnd = random.Random(5407)
    for _ in range(46):
        x, y = rnd.uniform(0, W), rnd.uniform(230, 595)
        S.obj(g, Ell(x, y, rnd.uniform(4, 9), rnd.uniform(3, 6)), (170, 166, 160), 5408, line=False)
    S.ground(g, Box(-4, 200, W + 4, 214), (100, 180, 80), "grass", 5409)
    # tree with roots (left)
    for k, (dx, dy) in enumerate(((-60, 120), (-20, 150), (30, 130), (70, 100), (-90, 70))):
        S.line(g, 96, 214, 96 + dx, 214 + dy, 6 - k * 0.6, (120, 84, 56))
        S.line(g, 96 + dx, 214 + dy, 96 + dx * 1.3, 214 + dy * 1.25, 3, (120, 84, 56))
    S.obj(g, Box(86, 110, 106, 214, 3), (130, 90, 60), 5410, kind="wood")
    S.obj(g, Circ(100, 80, 64), (90, 160, 70), 5411, kind="foliage", hi=True)
    # fence (right) and sunflowers
    for x in range(780, 900, 18):
        S.obj(g, Poly([(x, 204), (x, 166), (x + 6, 158), (x + 12, 166), (x + 12, 204)]), (250, 250, 246), 5412)
    S.flat(g, Box(778, 176, 902, 181), (250, 250, 246))
    for k, (x, h) in enumerate(((320, 90), (350, 74))):
        S.line(g, x, 204, x, 204 - h, 3, (80, 150, 60))
        S.obj(g, Union([Circ(x + 14 * math.cos(a), 204 - h + 14 * math.sin(a), 8) for a in np.linspace(0, math.tau, 10, endpoint=False)]), (250, 210, 50), 5413 + k)
        S.obj(g, Circ(x, 204 - h, 9), (120, 80, 40), 5415 + k)
    # carrots (difference: one) with tops
    for k, x in enumerate((476, 506, 536)):
        if k == 1 and "carrot" in d:
            continue
        S.obj(g, Poly([(x - 9, 214), (x + 9, 214), (x, 262)]), (250, 140, 40), 5420 + k)
        for a in (-0.4, 0, 0.4):
            S.line(g, x, 206, x + math.sin(a) * 14, 182, 2.4, (90, 170, 60))
    # molehill + ant tunnel and chambers (difference: ants in the tunnel)
    S.obj(g, Inter(Ell(298, 206, 30, 16), Box(268, 188, 328, 206)), (130, 90, 60), 5425, kind="dirt")
    tunnel = Union([Seg(300, 206, 262, 300, 12), Seg(262, 300, 236, 372, 12), Seg(262, 300, 320, 410, 12), Seg(236, 372, 220, 440, 10)])
    S.flat(g, tunnel, (70, 44, 30))
    for k, (x, y, rx, ry) in enumerate(((236, 372, 32, 18), (330, 418, 30, 16), (214, 452, 24, 13))):
        S.flat(g, Ell(x, y, rx, ry), (70, 44, 30))
    for k in range(4):
        S.obj(g, Ell(224 + k * 9, 378, 4.6, 3.4), (250, 248, 236), 5430 + k, line=False)
    for k in range(4):
        S.obj(g, Circ(320 + k * 8, 424, 3.4), (230, 200, 120), 5434 + k, line=False)
    if "ants" not in d:
        for k in range(5):
            t = k / 4
            x, y = 296 - 34 * t, 216 + 74 * t
            S.obj(g, Union([Circ(x, y, 4.2), Circ(x + 4.6, y - 4.6, 3.4), Circ(x - 4.6, y + 4.6, 3.8)]), (30, 20, 20), 5440 + k, line=False)
            S.line(g, x - 6, y - 2, x + 6, y + 2, 1.0, (30, 20, 20))
    # worm (difference)
    if "worm" not in d:
        pts = [(400 + k * 8, 286 + 5 * math.sin(k * 0.9)) for k in range(7)]
        for k, (x, y) in enumerate(pts):
            S.obj(g, Circ(x, y, 6), (240, 140, 160), 5445 + k, line=k in (0, 6))
        S.flat(g, Circ(450, 284, 1.6), (40, 30, 30))
    # rabbit burrow: tunnel to a chamber with sleeping rabbits and "Z"s (difference)
    S.flat(g, Union([Seg(700, 206, 740, 270, 26), Seg(740, 270, 760, 320, 26)]), (70, 44, 30))
    S.flat(g, Ell(790, 334, 76, 36), (70, 44, 30))
    S.obj(g, Ell(790, 350, 64, 14), (200, 170, 100), 5450, kind="grass", line=False)
    for k, x in enumerate((764, 812)):
        S.obj(g, Ell(x, 342, 22, 13), (250, 250, 246), 5451 + k, hi=True)
        S.obj(g, Ell(x - 14, 334, 9, 4), (250, 250, 246), 5453 + k)
    S.obj(g, Ell(714, 214, 10, 9), (250, 250, 246), 5455)
    for e in (-3, 3):
        S.obj(g, Ell(714 + e, 196, 3, 9), (250, 250, 246), 5456 + e)
    if "zzz" not in d:
        for k, (x, y, s) in enumerate(((770, 300, 7), (782, 286, 9), (796, 268, 11))):
            S.obj(g, Poly([(x - s, y - s), (x + s, y - s), (x + s, y - s + 2.4), (x - s + 3, y + s - 2.4), (x + s, y + s - 2.4), (x + s, y + s),
                           (x - s, y + s), (x - s, y + s - 2.4), (x + s - 3, y - s + 2.4), (x - s, y - s + 2.4)]), (250, 250, 250), 5460 + k)
    # mole tunnel with a mole and a treasure chest (difference), fossil fish (difference)
    S.flat(g, Union([Seg(470, 560, 640, 530, 34), Seg(640, 530, 900, 520, 34)]), (60, 38, 26))
    S.obj(g, Ell(560, 546, 22, 14), (60, 56, 66), 5465, hi=True)
    S.obj(g, Circ(540, 548, 4), (240, 150, 160), 5466)
    if "chest" not in d:
        cx, cy = 704, 534
        S.obj(g, Box(cx - 26, cy - 10, cx + 26, cy + 14, 2), (170, 110, 50), 5467, kind="wood")
        S.obj(g, Union([Box(cx - 28, cy - 22, cx + 28, cy - 10, 3)]), (150, 96, 44), 5468, kind="wood")
        S.flat(g, Box(cx - 4, cy - 14, cx + 4, cy - 2), (250, 210, 60))
        for k in range(5):
            S.obj(g, Circ(cx - 16 + k * 8, cy - 24, 4), (250, 210, 60), 5469 + k, line=False)
    if "fossil" not in d:
        fx, fy = 132, 560
        S.line(g, fx - 50, fy, fx + 40, fy, 2.6, (236, 230, 216))
        for k in range(7):
            x = fx - 36 + k * 11
            S.line(g, x, fy - 12 + abs(k - 3) * 1.4, x + 4, fy + 12 - abs(k - 3) * 1.4, 1.8, (236, 230, 216))
        S.obj(g, Poly([(fx + 38, fy - 10), (fx + 56, fy), (fx + 38, fy + 10)]), (236, 230, 216), 5475)
        S.obj(g, Poly([(fx - 50, fy), (fx - 66, fy - 12), (fx - 66, fy + 12)]), (236, 230, 216), 5476)


def underground_elements(S):
    return [
        E("cloud_u", el(lambda g, m: cloud(S, g, 680, 40, 36, 12, 5480)), pivot=(680, 40), anim=drift_across(644, 716, 6, start=0.3)),
        E("bee", el(lambda g, m: (S.obj(g, Ell(380, 120, 7, 5), (250, 210, 60), 5481), S.flat(g, Box(378, 115, 381, 125), (40, 30, 30)))),
          pivot=(380, 120), anim=dict(orbitRadius=(40, 20), orbitSpeed=0.2)),
        E("bird", el(lambda g, m: (S.line(g, 591, 120, 600, 124, 1.6, (60, 70, 90)), S.line(g, 600, 124, 609, 120, 1.6, (60, 70, 90)))),
          pivot=(600, 124), anim=dict(drift_across(591, 609, -24), stretch=(0, 0.5), scaleSpeed=2.2)),
    ]


UNDER_DIFFS = [("ants", 278, 252, 0), ("carrot", 506, 238, 0), ("worm", 424, 286, 0), ("zzz", 784, 282, 0), ("chest", 704, 526, 0), ("fossil", 128, 560, 0)]


# =================================================================== level list
SCENES = [
    ("海港", harbour, harbour_elements, HARBOUR_DIFFS),
    ("秋林", autumn, autumn_elements, AUTUMN_DIFFS),
    ("野餐", picnic, picnic_elements, PICNIC_DIFFS),
    ("小镇", town, town_elements, TOWN_DIFFS),
    ("地下", underground, underground_elements, UNDER_DIFFS),
]
STYLE_TITLES = {"toon": "卡通", "real": "写实", "comic": "美漫", "sketch": "素描"}


def _bg(S, scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, S, d)
        S.finish(g)
        g.commit()
    return bg


LEVELS = []
for si, S in enumerate(STYLES):
    for k, (title, scene, elems, diffs) in enumerate(SCENES):
        num = 1545 + si * 5 + k
        LEVELS.append(("Level%d" % num, "%s·%s" % (STYLE_TITLES[S.name], title), _bg(S, scene), elems(S), list(diffs), 60,
                       dict(post=POSTS[S.name], anim_seconds=12.0, frames=60)))
