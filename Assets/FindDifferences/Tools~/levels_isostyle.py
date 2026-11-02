# -*- coding: utf-8 -*-
"""High-angle axonometric levels (same camera as levels_inkiso) in three render styles:
  realistic  Level1532 湖畔小镇   Level1533 城市街角
  toon       Level1534 卡通农场   Level1535 卡通游乐园
  comic      Level1536 屋顶之夜   Level1537 公路餐厅      (American comic: black inks, flat colour, halftone)

One geometry kit, three Style classes. Everything is modelled in world units, projected with
levels_inkiso.Iso (azimuth 35 deg, ~33 deg elevation), back faces culled, faces shaded by the same light:
  Style.face(g, shape, col, v, kind, seed, ang, bot)   v = Lambert term 0..1, ang = screen angle of the face's
                                                       base edge (roof rows / planks follow it), bot = base edge
  Style.edge(g, p0, p1, silhouette)                    outlines (none for realistic)
  Style.shadow(g, shape)                               cast shadows on the ground
  Style.ground(g, shape, col, kind, seed)              ground decals: grass, road, water, field, sand ...
  Style.blob(g, cx, cy, rx, ry, col, seed)             tree crowns, bushes, animals' bodies
Scene.add(x, y, fn) collects drawables and paints them back-to-front by depth x*sin35 + y*cos35.
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (F32, Box, C, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Union, el, fbm, grain_tex,
                  lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint, tex, vgrad, vnoise)
from levels_inkiso import CA, LIGHT, SA, SHADOW_DIR, VIEW, Iso, _hull, _normal, rect_ring
from toon import INK as TINK, shade_of, tint_of


def iso_at(cx, cy, u):
    """Camera centred on world point (cx, cy) at scale u px / unit."""
    return Iso(450 - (cx * CA - cy * SA) * u, 300 - (cx * SA + cy * CA) * 0.55 * u, u)


def to_world(iso, sx, sy):
    """Screen point -> world (x, y) on the ground plane z = 0."""
    a, b = (sx - iso.ox) / iso.u, (sy - iso.oy) / (iso.u * 0.55)
    # a = x*CA - y*SA ; b = x*SA + y*CA
    return a * CA + b * SA, -a * SA + b * CA


# =================================================================== styles
class Real:
    name = "real"
    sky = (150, 180, 220)

    def __init__(self, warm=0.0):
        self.warm = warm

    def face(self, g, shp, col, v, kind, seed, ang=0.0, bot=None, top=False):
        k = 0.38 + 0.72 * v
        base = C(col) * k
        if top:
            base = base * 0.96 + C(self.sky) * 0.06
        ca, sa = math.cos(ang), math.sin(ang)

        def paint(X, Y):
            out = np.broadcast_to(base, X.shape + (3,)).copy()
            n = fbm(X, Y, 6, 6, 3, seed)
            if kind == "roof":
                u = (-X * sa + Y * ca) / 3.4
                rows = 0.82 + 0.18 * smooth(0.0, 0.25, np.abs(u - np.floor(u) - 0.5))
                out *= (rows * (0.88 + 0.24 * fbm(X, Y, 3, 3, 2, seed + 1)))[..., None]
            elif kind == "wood":
                u = (-X * sa + Y * ca) / 3.0
                out *= (0.86 + 0.14 * smooth(0.0, 0.2, np.abs(u - np.floor(u) - 0.5)) + 0.1 * (fbm(X * 0.3, Y, 12, 1.5, 2, seed) - 0.5))[..., None]
            elif kind == "stone":
                st = smooth(0.42, 0.52, np.abs(np.sin(fbm(X, Y, 7, 5, 2, seed) * 14)))
                out *= (0.72 + 0.22 * st + 0.16 * n)[..., None]
            elif kind in ("grass", "foliage"):
                out *= (0.7 + 0.55 * fbm(X, Y, 2.5, 2.5, 3, seed))[..., None]
            elif kind == "metal":
                out = out + C((255, 255, 255)) * (0.25 * v ** 6)
                out *= (0.95 + 0.1 * n)[..., None]
            elif kind == "glass":
                out = out * 0.6 + C(self.sky) * (0.25 + 0.2 * smooth(0.3, 0.7, fbm(X, Y, 20, 20, 2, seed)))[..., None]
            else:
                out *= (0.92 + 0.14 * n)[..., None]
            return out
        g.fill(shp, grain_tex(paint, 0.05, seed + 7))
        if bot is not None:                 # ambient occlusion near the ground
            (x0, y0), (x1, y1) = bot
            if abs(x1 - x0) > 0.5:
                def ao(X, Y, x0=x0, y0=y0, x1=x1, y1=y1):
                    yb = y0 + (y1 - y0) * np.clip((X - x0) / (x1 - x0), 0, 1)
                    return smooth(yb - 16, yb + 1, Y) * 0.4
                g.mul(shp, 1.0, alpha=ao, tint=(40, 46, 60))

    def edge(self, g, p0, p1, sil=True, w=1.0):
        if sil:
            g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 0.7), (30, 32, 40), alpha=0.25)

    def shadow(self, g, shp, k=1.0):
        g.mul(shp, 0.48 * k, feather=3.5, tint=(30, 40, 80))

    def ground(self, g, shp, col, kind, seed):
        c = C(col)

        def paint(X, Y):
            if kind == "grass":
                n = fbm(X, Y, 3, 3, 4, seed)
                n2 = fbm(X, Y, 60, 40, 3, seed + 1)
                out = c * (0.72 + 0.4 * n)[..., None] * (0.88 + 0.24 * n2)[..., None]
                dry = smooth(0.6, 0.78, fbm(X, Y, 50, 40, 3, seed + 2))
                return out + (C((176, 160, 90)) * (0.8 + 0.3 * n)[..., None] - out) * (dry * 0.45)[..., None]
            if kind == "water":
                n = fbm(X, Y, 40, 6, 4, seed)
                out = c * (0.85 + 0.25 * n)[..., None]
                gl = smooth(0.66, 0.8, fbm(X, Y, 14, 2.4, 3, seed + 1))
                return out + C((230, 244, 250)) * (gl * 0.35)[..., None]
            if kind == "road":
                return c * (0.88 + 0.14 * fbm(X, Y, 30, 30, 3, seed))[..., None]
            if kind == "dirt":
                return c * (0.8 + 0.3 * fbm(X, Y, 5, 5, 4, seed))[..., None]
            return c * (0.9 + 0.15 * fbm(X, Y, 8, 8, 3, seed))[..., None]
        g.fill(shp, grain_tex(paint, 0.08 if kind in ("road", "dirt", "sand") else 0.04, seed + 3))

    def blob(self, g, cx, cy, rx, ry, col, seed, kind="foliage"):
        shape = Rough(Ell(cx, cy, rx, ry), max(2, rx * 0.14), max(3, rx * 0.3), seed, 3)
        sp = sphere_paint(cx, cy, rx * 1.05, col, ry=ry * 1.1, light=(-0.6, -0.7, 0.5), amb=0.35, spec=0.05, wrap=0.3)
        if kind == "foliage":
            g.fill(shape, lambda X, Y: sp(X, Y) * (0.62 + 0.62 * fbm(X, Y, max(2, rx * 0.2), max(2, ry * 0.2), 4, seed + 1))[..., None])
        else:
            g.fill(shape, grain_tex(sp, 0.06, seed))

    def finish(self, g):
        g.bloom(225, 12, 0.25)
        g.grade(contrast=1.06, sat=1.06, warm=self.warm)


class Toon:
    name = "toon"
    ink = TINK

    def face(self, g, shp, col, v, kind, seed, ang=0.0, bot=None, top=False):
        c = tint_of(col, 0.12) if v > 0.75 else (col if v > 0.42 else shade_of(col, 0.72))
        g.fill(shp, c)
        if kind in ("roof", "wood"):
            ca, sa = math.cos(ang), math.sin(ang)
            sp = 6.0 if kind == "roof" else 5.0
            g.fill(shp, shade_of(c, 0.8), alpha=lambda X, Y: smooth(0.1, 0.0, np.abs(((-X * sa + Y * ca) / sp) % 1.0 - 0.5) - 0.42) * 0.8)

    def edge(self, g, p0, p1, sil=True, w=1.0):
        g.fill(Seg(p0[0], p0[1], p1[0], p1[1], (2.0 if sil else 1.2) * w), self.ink)

    def shadow(self, g, shp, k=1.0):
        g.mul(shp, 0.3 * k, tint=(70, 40, 150))

    def ground(self, g, shp, col, kind, seed):
        g.fill(shp, col)
        if kind == "grass":
            rnd = random.Random(seed)
            b = shp.bbox()
            for _ in range(60):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                g.fill(Inter(Union([Seg(x - 3, y, x - 4, y - 5, 1.4), Seg(x, y, x, y - 7, 1.4), Seg(x + 3, y, x + 4, y - 5, 1.4)]), shp), shade_of(col, 0.8))
        if kind == "water":
            rnd = random.Random(seed)
            b = shp.bbox()
            for _ in range(40):
                x, y = rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3])
                g.fill(Inter(Seg(x - 8, y, x + 8, y, 1.6), shp), (236, 248, 255))

    def blob(self, g, cx, cy, rx, ry, col, seed, kind="foliage"):
        shape = Union([Ell(cx, cy, rx, ry)] + [Ell(cx + rx * 0.7 * math.cos(a), cy + ry * 0.6 * math.sin(a), rx * 0.42, ry * 0.42)
                                                for a in np.linspace(0, math.tau, 7, endpoint=False)]) if kind == "foliage" else Ell(cx, cy, rx, ry)
        g.fill(Moved(shape, 0, 0), self.ink, feather=0)
        inner = Ell(cx, cy, rx - 1.6, ry - 1.6) if kind != "foliage" else Union([Ell(cx, cy, rx - 1.6, ry - 1.6)] + [
            Ell(cx + rx * 0.7 * math.cos(a), cy + ry * 0.6 * math.sin(a), rx * 0.42 - 1.6, ry * 0.42 - 1.6) for a in np.linspace(0, math.tau, 7, endpoint=False)])
        g.fill(inner, col)
        g.fill(Inter(inner, Moved(Ell(cx, cy, rx * 1.1, ry * 1.1), rx * 0.45, ry * 0.5)), shade_of(col, 0.75))
        g.fill(Ell(cx - rx * 0.35, cy - ry * 0.4, rx * 0.22, ry * 0.14), tint_of(col, 0.45))

    def finish(self, g):
        g.grade(contrast=1.03, sat=1.08)


def halftone(amt, cell=5.0, ang=45):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)

    def f(X, Y):
        u, v = (X * ca + Y * sa) / cell, (-X * sa + Y * ca) / cell
        d = np.hypot(u - np.round(u), v - np.round(v))
        r = 0.5 * np.sqrt(np.clip(amt(X, Y) if callable(amt) else amt, 0, 1)) * 1.1
        return smooth(r, r - 0.12, d)
    return f


class Comic:
    name = "comic"
    ink = (16, 14, 22)

    def __init__(self, night=False):
        self.night = night

    def face(self, g, shp, col, v, kind, seed, ang=0.0, bot=None, top=False):
        if v > 0.6:
            g.fill(shp, col)
        elif v > 0.22:
            g.fill(shp, tuple(c * 0.78 for c in col))
            g.fill(shp, self.ink, alpha=halftone(0.32, 4.6))
        else:
            g.fill(shp, mixc(col, self.ink, 0.72))
        if kind in ("roof", "wood"):
            ca, sa = math.cos(ang), math.sin(ang)
            g.fill(shp, self.ink, alpha=lambda X, Y: smooth(0.08, 0.0, np.abs(((-X * sa + Y * ca) / 7.0) % 1.0 - 0.5) - 0.44) * 0.85)

    def edge(self, g, p0, p1, sil=True, w=1.0):
        g.fill(Seg(p0[0], p0[1], p1[0], p1[1], (2.6 if sil else 1.3) * w, (2.0 if sil else 1.1) * w), self.ink)

    def shadow(self, g, shp, k=1.0):
        g.fill(shp, self.ink, alpha=0.55 * k)

    def ground(self, g, shp, col, kind, seed):
        g.fill(shp, col)
        if kind in ("sand", "grass", "dirt", "roof"):
            g.fill(shp, self.ink, alpha=lambda X, Y: halftone(lambda X, Y: 0.18 * smooth(0.45, 0.7, fbm(X, Y, 80, 60, 2, seed)), 5.5)(X, Y))
        if kind == "road":
            g.fill(shp, self.ink, alpha=halftone(0.1, 5.0))

    def blob(self, g, cx, cy, rx, ry, col, seed, kind="foliage"):
        shape = Rough(Ell(cx, cy, rx, ry), rx * 0.12, rx * 0.35, seed, 2) if kind == "foliage" else Ell(cx, cy, rx, ry)
        g.fill(shape, self.ink)
        inner = Rough(Ell(cx, cy, rx - 2.2, ry - 2.2), rx * 0.12, rx * 0.35, seed, 2) if kind == "foliage" else Ell(cx, cy, rx - 2.2, ry - 2.2)
        g.fill(inner, col)
        sh = Inter(inner, Moved(Ell(cx, cy, rx, ry), rx * 0.5, ry * 0.55))
        g.fill(sh, tuple(c * 0.75 for c in col))
        g.fill(sh, self.ink, alpha=halftone(0.35, 4.4))
        g.fill(Ell(cx - rx * 0.35, cy - ry * 0.42, rx * 0.2, ry * 0.12), (255, 255, 255), alpha=0.8)

    def finish(self, g):
        g.grade(contrast=1.06, sat=1.12)


# =================================================================== geometry kit
def solid(g, S, iso, top, bot, col, kind="plain", seed=0, top_col=None, top_kind=None, smooth_sides=False, edges=True, w=1.0, side_cols=None):
    n = len(top)
    cen = np.mean(np.array(top + bot, float), axis=0)
    faces = [("top", list(top))] + [("s%d" % i, [bot[i], bot[(i + 1) % n], top[(i + 1) % n], top[i]]) for i in range(n)]
    vis = {}
    view, light = getattr(iso, "view", VIEW), getattr(iso, "light", LIGHT)
    for name, pts in faces:
        nn = _normal(pts)
        if np.linalg.norm(nn) < 1e-9:
            continue
        if np.dot(nn, np.mean(np.array(pts, float), axis=0) - cen) < 0:
            nn = -nn
        if np.dot(nn, view) > 1e-3:
            vis[name] = (pts, nn)
    for name, (pts, nn) in sorted(vis.items(), key=lambda kv: np.dot(np.mean(np.array(kv[1][0], float), axis=0), view)):
        sp = [iso.p(*q) for q in pts]
        v = max(0.0, float(np.dot(nn, light)))
        if name == "top":
            S.face(g, Poly(sp), top_col or col, v, top_kind or kind, seed, ang=math.atan2(sp[1][1] - sp[0][1], sp[1][0] - sp[0][0]), top=True)
        else:
            vertical = abs(nn[2]) < 0.2
            S.face(g, Poly(sp), side_cols[int(name[1:]) % len(side_cols)] if side_cols else col, v, kind, seed + int(name[1:]), ang=math.atan2(sp[1][1] - sp[0][1], sp[1][0] - sp[0][0]),
                   bot=(sp[0], sp[1]) if vertical else None)
    if not edges:
        return
    if "top" in vis:
        for i in range(n):
            S.edge(g, iso.p(*top[i]), iso.p(*top[(i + 1) % n]), sil=("s%d" % i) not in vis, w=w)
    for i in range(n):
        if ("s%d" % i) in vis:
            S.edge(g, iso.p(*bot[i]), iso.p(*bot[(i + 1) % n]), sil=True, w=w)
        a_vis, b_vis = ("s%d" % ((i - 1) % n)) in vis, ("s%d" % i) in vis
        if a_vis != b_vis or (a_vis and b_vis and not smooth_sides):
            S.edge(g, iso.p(*bot[i]), iso.p(*top[i]), sil=(a_vis != b_vis), w=w)


def box(g, S, iso, x0, y0, z0, x1, y1, z1, col, kind="plain", seed=0, **kw):
    solid(g, S, iso, [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
          [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], col, kind, seed, **kw)


def cyl(g, S, iso, x, y, z0, z1, r, col, kind="plain", seed=0, r1=None, n=18, **kw):
    r1 = r if r1 is None else r1
    ts = np.linspace(0, math.tau, n, endpoint=False)
    solid(g, S, iso, [(x + r1 * math.cos(t), y + r1 * math.sin(t), z1) for t in ts],
          [(x + r * math.cos(t), y + r * math.sin(t), z0) for t in ts], col, kind, seed, smooth_sides=True, **kw)


def cone(g, S, iso, x, y, z0, z1, r, col, kind="plain", seed=0, n=18, **kw):
    ts = np.linspace(0, math.tau, n, endpoint=False)
    solid(g, S, iso, [(x, y, z1)] * n, [(x + r * math.cos(t), y + r * math.sin(t), z0) for t in ts], col, kind, seed,
          smooth_sides=True, **kw)


def gable(g, S, iso, x0, y0, x1, y1, z0, wall_h, roof_h, wall, roof, seed=0, along_x=True, over=0.4, wall_kind="plain"):
    box(g, S, iso, x0, y0, z0, x1, y1, z0 + wall_h, wall, wall_kind, seed)
    zt = z0 + wall_h
    if along_x:
        ym = (y0 + y1) / 2
        top = [(x0 - over, ym, zt + roof_h), (x1 + over, ym, zt + roof_h), (x1 + over, ym, zt + roof_h), (x0 - over, ym, zt + roof_h)]
    else:
        xm = (x0 + x1) / 2
        top = [(xm, y0 - over, zt + roof_h), (xm, y0 - over, zt + roof_h), (xm, y1 + over, zt + roof_h), (xm, y1 + over, zt + roof_h)]
    bot = [(x0 - over, y0 - over, zt), (x1 + over, y0 - over, zt), (x1 + over, y1 + over, zt), (x0 - over, y1 + over, zt)]
    solid(g, S, iso, top, bot, roof, "roof", seed + 1)
    # gable-end triangles (wall colour) on the ends that face the camera
    view, light = getattr(iso, "view", VIEW), getattr(iso, "light", LIGHT)
    if along_x:
        ends = [([(x1, y0, zt), (x1, y1, zt), (x1, (y0 + y1) / 2, zt + roof_h * 0.92)], (1, 0, 0)),
                ([(x0, y0, zt), (x0, y1, zt), (x0, (y0 + y1) / 2, zt + roof_h * 0.92)], (-1, 0, 0))]
    else:
        ends = [([(x0, y1, zt), (x1, y1, zt), ((x0 + x1) / 2, y1, zt + roof_h * 0.92)], (0, 1, 0)),
                ([(x0, y0, zt), (x1, y0, zt), ((x0 + x1) / 2, y0, zt + roof_h * 0.92)], (0, -1, 0))]
    for tri, nn in ends:
        if np.dot(nn, view) <= 1e-3:
            continue
        sp = [iso.p(*q) for q in tri]
        S.face(g, Poly(sp), wall, max(0.0, float(np.dot(nn, light))), wall_kind, seed + 3, ang=math.atan2(sp[1][1] - sp[0][1], sp[1][0] - sp[0][0]))
        for i in range(3):
            S.edge(g, sp[i], sp[(i + 1) % 3], sil=(i != 0))


def quad_on(iso, face, a0, a1, z0, z1, at):
    """A rectangle on a vertical wall: face 'x' (x = at, spanning y a0..a1) or 'y' (y = at, spanning x a0..a1)."""
    if face == "x":
        return Poly([iso.p(at, a0, z0), iso.p(at, a1, z0), iso.p(at, a1, z1), iso.p(at, a0, z1)])
    return Poly([iso.p(a0, at, z0), iso.p(a1, at, z0), iso.p(a1, at, z1), iso.p(a0, at, z1)])


def windows(g, S, iso, face, at, a0, a1, z0, z1, n, glass=(110, 140, 170), frame=(240, 236, 226), lit=None, rows=1, gap=0.6, seed=0):
    span = (a1 - a0) / n
    hz = (z1 - z0) / rows
    for r in range(rows):
        for k in range(n):
            u0, u1 = a0 + k * span + span * 0.22, a0 + (k + 1) * span - span * 0.22
            v0, v1 = z0 + r * hz + hz * 0.2, z0 + (r + 1) * hz - hz * 0.15
            fr = quad_on(iso, face, u0 - 0.08, u1 + 0.08, v0 - 0.08, v1 + 0.08, at)
            gl = quad_on(iso, face, u0, u1, v0, v1, at)
            g.fill(fr, frame)
            col = lit if (lit is not None and (k + r + seed) % 3 == 0) else glass
            S.face(g, gl, col, 0.6, "glass", seed + k + r * 7)
            if S.name != "real":
                for i in range(4):
                    S.edge(g, gl.p[i], gl.p[(i + 1) % 4], sil=False, w=0.7)


def shadow(g, S, iso, ring, z, h, k=1.0, clip=None):
    sx, sy = getattr(iso, "shadow_dir", SHADOW_DIR)
    pts = [(x, y) for x, y in ring] + [(x + sx * h, y + sy * h) for x, y in ring]
    hull = _hull([(round(a, 4), round(b, 4)) for a, b in pts])
    shp = Poly([iso.p(x, y, z) for x, y in hull])
    if clip is not None:
        shp = Inter(shp, clip)
    S.shadow(g, shp, k)


def decal(g, S, iso, pts, col, kind="plain", seed=0, z=0.0, outline=False, rough=0.0):
    shp = Poly([iso.p(x, y, z) for x, y in pts])
    if rough:
        shp = Rough(shp, rough, rough * 4, seed, 3)
    S.ground(g, shp, col, kind, seed)
    if outline and S.name != "real":
        for i in range(len(pts)):
            S.edge(g, iso.p(*pts[i], z), iso.p(*pts[(i + 1) % len(pts)], z), sil=False)
    return shp


def strip(iso, pts, w, z=0.0):
    """Ground polygon for a path / road of width w along a world polyline."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == len(pts) - 1:
            dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln * w / 2, dx / ln * w / 2
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    return left + right[::-1]


def tree(g, S, iso, x, y, h, col=(70, 110, 50), seed=0, kind="round", trunk=(100, 74, 52)):
    if kind == "pine":
        cyl(g, S, iso, x, y, 0, h * 0.25, 0.18, trunk, "wood", seed, n=8)
        for t in range(3):
            z0 = h * (0.2 + t * 0.24)
            cone(g, S, iso, x, y, z0, z0 + h * 0.42, 1.2 * (1 - t * 0.25) * h / 5, col, "foliage", seed + t, n=12)
        return
    cyl(g, S, iso, x, y, 0, h * 0.5, 0.2 * h / 4, trunk, "wood", seed, n=8)
    cx, cy = iso.p(x, y, h * 0.68)
    r = 0.38 * h * iso.u * 0.62
    S.blob(g, cx, cy, r * 1.05, r * 0.92, col, seed)


def tree_shadow(g, S, iso, x, y, h, k=0.9):
    r = 0.33 * h * 0.62 / 0.82
    shadow(g, S, iso, [(x + r * math.cos(t), y + r * math.sin(t)) for t in np.linspace(0, math.tau, 10, endpoint=False)], 0, h * 0.62, k=k)


def car(g, S, iso, x, y, col, along_x=True, seed=0, z=0.0, L=3.6, Wd=1.7):
    if along_x:
        x0, x1, y0, y1 = x - L / 2, x + L / 2, y - Wd / 2, y + Wd / 2
    else:
        x0, x1, y0, y1 = x - Wd / 2, x + Wd / 2, y - L / 2, y + L / 2
    for (wx, wy) in ((x0 + 0.6, y0), (x1 - 0.6, y0), (x0 + 0.6, y1), (x1 - 0.6, y1)) if along_x else ((x0, y0 + 0.6), (x1, y0 + 0.6), (x0, y1 - 0.6), (x1, y1 - 0.6)):
        cyl(g, S, iso, wx, wy, z, z + 0.55, 0.32, (30, 30, 34), "plain", seed, n=8, edges=False)
    box(g, S, iso, x0, y0, z + 0.25, x1, y1, z + 0.85, col, "metal", seed)
    if along_x:
        cx0, cx1 = x0 + L * 0.25, x1 - L * 0.22
        box(g, S, iso, cx0, y0 + 0.12, z + 0.85, cx1, y1 - 0.12, z + 1.45, mixc(col, (40, 50, 70), 0.55), "glass", seed + 1, top_col=col)
    else:
        cy0, cy1 = y0 + L * 0.25, y1 - L * 0.22
        box(g, S, iso, x0 + 0.12, cy0, z + 0.85, x1 - 0.12, cy1, z + 1.45, mixc(col, (40, 50, 70), 0.55), "glass", seed + 1, top_col=col)


def person(g, S, iso, x, y, col, seed=0, z=0.0, hat=None, s=1.0):
    cyl(g, S, iso, x, y, z, z + 0.75 * s, 0.22 * s, (50, 54, 70), "plain", seed, n=8, w=0.7)
    cyl(g, S, iso, x, y, z + 0.75 * s, z + 1.45 * s, 0.3 * s, col, "plain", seed + 1, n=10, w=0.7)
    hx, hy = iso.p(x, y, z + 1.7 * s)
    r = 0.24 * s * iso.u
    S.blob(g, hx, hy, r, r, (236, 196, 160), seed + 2, kind="body")
    if hat is not None:
        g.fill(Ell(hx, hy - r * 0.55, r * 1.05, r * 0.55), hat)


def fence(g, S, iso, pts, col=(150, 120, 90), h=1.0, step=1.6, seed=0):
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        ln = math.hypot(xb - xa, yb - ya)
        n = max(1, int(ln / step))
        for k in range(n + 1):
            px, py = xa + (xb - xa) * k / n, ya + (yb - ya) * k / n
            box(g, S, iso, px - 0.1, py - 0.1, 0, px + 0.1, py + 0.1, h, col, "wood", seed + k, w=0.7)
        for z in (h * 0.45, h * 0.85):
            a, b = iso.p(xa, ya, z), iso.p(xb, yb, z)
            if S.name == "real":
                g.fill(Seg(a[0], a[1], b[0], b[1], 2.0), mixc(col, (0, 0, 0), 0.15))
            else:
                g.fill(Seg(a[0], a[1], b[0], b[1], 3.6), S.ink)
                g.fill(Seg(a[0], a[1], b[0], b[1], 1.6), col)


class Scene:
    def __init__(self, depth=None):
        self.items = []
        self.depth = depth or (lambda x, y: x * SA + y * CA)

    def add(self, x, y, fn, dz=0.0, on=None):
        """on=(x1, y1) of the building a prop stands on: sort right after that building."""
        if on is not None:
            x, y, dz = on[0], on[1], 0.001 + dz * 1e-4
        self.items.append((self.depth(x, y) + dz, len(self.items), fn))

    def draw(self):
        for _, _, fn in sorted(self.items, key=lambda t: (t[0], t[1])):
            fn()


def make_bg(S, scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, S, d)
        S.finish(g)
        g.commit()
    return bg


def toon_post(rows, w, h, ox, oy, has_alpha):
    real_post(rows, w, h, ox, oy, has_alpha, grain=1.2, vignette=0.12)


def comic_post(rows, w, h, ox, oy, has_alpha):
    real_post(rows, w, h, ox, oy, has_alpha, grain=1.6, vignette=0.14)


OPTS_REAL = dict(post=real_post, anim_seconds=12.0, frames=60)
OPTS_TOON = dict(post=toon_post, anim_seconds=12.0, frames=60)
OPTS_COMIC = dict(post=comic_post, anim_seconds=12.0, frames=60)


def sp_of(iso):
    return lambda x, y, z=0.0: tuple(int(round(v)) for v in iso.p(x, y, z))


# =================================================================== Level 1532 lakeside village (realistic)
I32 = iso_at(16, 13, 24.0)
R32 = Real(warm=3)


def l1532_scene(g, S, d):
    iso = I32
    decal(g, S, iso, [(-60, -60), (90, -60), (90, 90), (-60, 90)], (96, 130, 62), "grass", 3201)
    lake = [(30, 10), (38, 4), (52, 6), (60, 20), (56, 36), (40, 40), (28, 34), (24, 22)]
    decal(g, S, iso, [(x + 0.8, y + 0.8) for x, y in lake], (196, 186, 150), "sand", 3202, rough=10)
    lk = decal(g, S, iso, lake, (60, 110, 130), "water", 3203, rough=10)
    decal(g, S, iso, strip(iso, [(-14, 18), (0, 14), (10, 10), (18, 12), (24, 18)], 2.2), (160, 136, 100), "dirt", 3204)
    decal(g, S, iso, strip(iso, [(10, 10), (12, 0), (16, -10), (18, -24)], 2.0), (160, 136, 100), "dirt", 3205)
    for k, (gx, gy) in enumerate(((-12, 0), (8, 22))):
        decal(g, S, iso, rect_ring(gx, gy, gx + 5, gy + 4), (120, 90, 60), "dirt", 3206 + k)
        for r in range(4):
            decal(g, S, iso, rect_ring(gx + 0.3, gy + 0.4 + r, gx + 4.7, gy + 0.75 + r), (70, 120, 50), "grass", 3208 + r)
    sc = Scene()
    shadows = []
    for k, (x, y) in enumerate(((-6, 10), (7, 3), (24, -4), (-3, 14), (30, 2))):
        sc.add(x, y, lambda x=x, y=y, k=k: S.blob(g, *iso.p(x, y, 0.5), 16, 11, (70, 104, 46), 3300 + k))
    # houses (stone walls, slate / red roofs); one roof colour is a difference
    houses = [(0, -4, 6, 4.5, 3.0, (196, 186, 170), (80, 86, 100), True, "h1"),
              (-6, 4, 4.5, 4, 2.6, (210, 196, 172), (150, 70, 50), False, "h2"),
              (18, -2, 5, 4, 2.8, (200, 190, 176), (80, 86, 100), True, "h3"),
              (4, 18, 5, 4, 2.6, (216, 204, 180), (150, 70, 50), False, "h4")]
    for (x0, y0, w, dp, wh, wall, roof, ax, hid) in houses:
        if hid == "h3" and "roof" in d:
            roof = (60, 110, 80)

        def draw(x0=x0, y0=y0, w=w, dp=dp, wh=wh, wall=wall, roof=roof, ax=ax, seed=hash(hid) % 1000):
            gable(g, S, iso, x0, y0, x0 + w, y0 + dp, 0, wh, 1.8, wall, roof, seed, along_x=ax, wall_kind="stone")
            windows(g, S, iso, "y", y0 + dp, x0 + 0.4, x0 + w - 0.4, 0.8, wh - 0.3, 2, seed=seed)
            windows(g, S, iso, "x", x0 + w, y0 + 0.3, y0 + dp - 0.3, 0.8, wh - 0.3, 1, seed=seed + 5)
            door = quad_on(iso, "y", x0 + w * 0.42, x0 + w * 0.58, 0, 1.8, y0 + dp)
            S.face(g, door, (110, 70, 44), 0.5, "wood", seed + 9, ang=0.6)
        shadows.append((rect_ring(x0, y0, x0 + w, y0 + dp), wh + 1.0))
        sc.add(x0 + w, y0 + dp, draw)
    # chimney on h1 (static) - smoke element
    sc.add(5.5, 0.6, lambda: box(g, S, iso, 4.6, -3.0, 3.6, 5.3, -2.3, 5.4, (150, 140, 130), "stone", 3210), dz=0.01)
    # dock + boats on the lake
    sc.add(30, 26, lambda: box(g, S, iso, 24, 23.5, -0.3, 33, 25.5, 0.25, (150, 116, 80), "wood", 3220))
    for k, px in enumerate(range(25, 33, 2)):
        sc.add(px, 25.6, lambda px=px: cyl(g, S, iso, px, 25.5, -0.6, 0.25, 0.15, (110, 84, 60), "wood", 3221, n=8), dz=-0.01)
    boats = [(37, 18, (180, 60, 46), "boat1"), (32, 24, (60, 90, 140), "boat2")]
    for bx, by, col, bid in boats:
        if bid == "boat2" and "boat" in d:
            continue

        def draw(bx=bx, by=by, col=col):
            top = [(bx - 1.6, by - 0.6, 0.35), (bx + 1.2, by - 0.6, 0.3), (bx + 2.0, by, 0.4), (bx + 1.2, by + 0.6, 0.3), (bx - 1.6, by + 0.6, 0.35)]
            bot = [(bx - 1.3, by - 0.3, -0.2), (bx + 1.0, by - 0.3, -0.2), (bx + 1.5, by, -0.2), (bx + 1.0, by + 0.3, -0.2), (bx - 1.3, by + 0.3, -0.2)]
            solid(g, S, iso, top, bot, col, "wood", 3230, top_col=(150, 116, 80))
        sc.add(bx + 2, by, draw)
    # trees: pines behind, broadleaf around (one is a difference)
    trees = [(-12, -6, 5.5, "pine"), (-8, -10, 6, "pine"), (8, -12, 5, "pine"), (26, -8, 5.5, "pine"), (30, -2, 4.5, "round"),
             (-10, 12, 4.5, "round"), (14, 8, 4.2, "round"), (22, 6, 4.6, "round"), (-2, 26, 4.8, "round"), (14, 30, 4.4, "pine"),
             (20, 36, 5, "round")]
    for k, (x, y, h, kind) in enumerate(trees):
        if k == 6 and "tree" in d:
            continue
        shadows.append(("tree", x, y, h))
        col = (54, 86, 50) if kind == "pine" else ((80, 118, 50) if k % 2 else (96, 124, 52))
        sc.add(x, y, lambda x=x, y=y, h=h, kind=kind, col=col, k=k: tree(g, S, iso, x, y, h, col, 3240 + k, kind))
    # haystacks (one difference), fence, well, cart, people, dog
    for k, (x, y) in enumerate(((-4, 22), (-1, 24), (2, 28))):
        if k == 1 and "hay" in d:
            continue
        shadows.append(([(x + 0.9 * math.cos(t), y + 0.9 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 1.6))
        sc.add(x, y, lambda x=x, y=y, k=k: (cyl(g, S, iso, x, y, 0, 0.9, 1.0, (206, 176, 96), "grass", 3250 + k, r1=0.95),
                                           cone(g, S, iso, x, y, 0.9, 1.9, 0.98, (214, 184, 100), "grass", 3255 + k)))
    sc.add(-6, 30, lambda: fence(g, S, iso, [(-8, 18), (-8, 30), (6, 33)], seed=3260))
    shadows.append(([(10 + 0.8 * math.cos(t), 2 + 0.8 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 1.0))
    sc.add(10, 2, lambda: cyl(g, S, iso, 10, 2, 0, 0.9, 0.8, (150, 146, 140), "stone", 3270))
    if "cart" not in d:
        shadows.append((rect_ring(19, 13, 22, 15), 1.2))
        sc.add(22, 15, lambda: (box(g, S, iso, 19, 13, 0.5, 22, 15, 1.2, (150, 110, 70), "wood", 3280),
                                box(g, S, iso, 19.4, 13.4, 1.2, 21.6, 14.6, 1.7, (210, 180, 100), "grass", 3281),
                                cyl(g, S, iso, 20.5, 15.05, 0, 1.0, 0.5, (90, 70, 50), "wood", 3282, n=10)))
    for k, (x, y, col) in enumerate(((12, 13, (60, 100, 160)), (26, 24, (180, 60, 50)), (2, 9, (200, 170, 60)))):
        sc.add(x, y, lambda x=x, y=y, col=col, k=k: person(g, S, iso, x, y, col, 3290 + k))
    if "dog" not in d:
        sc.add(14, 14, lambda: (box(g, S, iso, 13.2, 13.6, 0.35, 14.4, 14.1, 0.8, (170, 120, 70), "plain", 3295),
                                box(g, S, iso, 14.2, 13.65, 0.6, 14.7, 14.05, 1.05, (170, 120, 70), "plain", 3296)))
    if "wash" not in d:      # laundry line between h4 and a pole
        def lines():
            for x in (11, 15):
                a, b = iso.p(x, 21, 0), iso.p(x, 21, 2.2)
                g.fill(Seg(a[0], a[1], b[0], b[1], 1.6), (90, 70, 50))
            a, b = iso.p(11, 21, 2.1), iso.p(15, 21, 2.1)
            g.fill(Seg(a[0], a[1], b[0], b[1], 0.8), (60, 60, 60))
            for k, col in enumerate(((230, 230, 224), (180, 60, 60), (70, 110, 170))):
                p = iso.p(11.6 + k * 1.2, 21, 2.1)
                S.face(g, Poly([(p[0] - 7, p[1]), (p[0] + 7, p[1]), (p[0] + 7, p[1] + 16), (p[0] - 7, p[1] + 16)]), col, 0.7, "plain", 3297 + k)
        sc.add(15, 21, lines)
    # cast shadows first, then everything back to front
    for sh in shadows:
        if sh[0] == "tree":
            tree_shadow(g, S, iso, sh[1], sh[2], sh[3])
        else:
            shadow(g, S, iso, sh[0], 0, sh[1])
    sc.draw()


L1532_ELEMENTS = [
    E("smoke", el(lambda g, m: [g.fill(Circ(x, y, r), (230, 230, 232), alpha=0.5, feather=4) for x, y, r in
                                ((I32.p(4.95, -2.65, 5.6)[0], I32.p(4.95, -2.65, 5.6)[1] - 6, 6),)]),
      anim=dict(driftVelocity=(10, 40), driftLength=70, driftFade=True, driftGrow=1.8)),
    E("glint", el(lambda g, m: [g.glow(x, y, 4, (255, 255, 240), 1.0) for x, y in (I32.p(40, 14), I32.p(48, 30), I32.p(34, 30))]),
      daynight="untinted", anim=dict(twinkle=0.85, twinkleSpeed=0.6)),
]

_s32 = sp_of(I32)
L1532_DIFFS = [
    ("roof", *_s32(20.5, 0, 3.8), 0),
    ("boat", *_s32(32.4, 24, 0.2), 0),
    ("tree", *_s32(14, 8, 3.0), 0),
    ("hay", *_s32(-1, 24, 1.0), 0),
    ("cart", *_s32(20.5, 14, 1.2), 0),
    ("dog", *_s32(14, 13.9, 0.7), 0),
    ("wash", *_s32(13, 21, 1.8), 0),
]


# =================================================================== more kit
def awning(g, S, iso, x0, x1, y, z, depth, cols, seed=0):
    n = len(cols) * 3
    for k in range(n):
        a0, a1 = x0 + (x1 - x0) * k / n, x0 + (x1 - x0) * (k + 1) / n
        shp = Poly([iso.p(a0, y, z), iso.p(a1, y, z), iso.p(a1, y + depth, z - 0.7), iso.p(a0, y + depth, z - 0.7)])
        S.face(g, shp, cols[k % len(cols)], 0.8, "plain", seed + k)
    for a, b in (((x0, y, z), (x1, y, z)), ((x0, y + depth, z - 0.7), (x1, y + depth, z - 0.7)), ((x0, y, z), (x0, y + depth, z - 0.7)),
                 ((x1, y, z), (x1, y + depth, z - 0.7))):
        S.edge(g, iso.p(*a), iso.p(*b), sil=True, w=0.8)


def umbrella(g, S, iso, x, y, h, r, cols, seed=0):
    cyl(g, S, iso, x, y, 0, h, 0.06, (220, 220, 220), "metal", seed, n=6, edges=False)
    ts = np.linspace(0, math.tau, 12, endpoint=False)
    solid(g, S, iso, [(x, y, h + 0.5)] * 12, [(x + r * math.cos(t), y + r * math.sin(t), h - 0.2) for t in ts], cols[0], "plain", seed,
          smooth_sides=False, side_cols=cols)


def lamp_post(g, S, iso, x, y, h=3.2, seed=0, lit=False):
    cyl(g, S, iso, x, y, 0, h, 0.08, (60, 64, 70), "metal", seed, n=6, w=0.7)
    box(g, S, iso, x - 0.25, y - 0.25, h, x + 0.25, y + 0.25, h + 0.35, (250, 236, 180) if lit else (70, 74, 80), "metal", seed + 1, w=0.7)
    if lit:
        px, py = iso.p(x, y, h)
        g.glow(px, py, 40, (255, 210, 120), 0.45)


def bench(g, S, iso, x, y, along_x=True, col=(140, 96, 60), seed=0):
    if along_x:
        box(g, S, iso, x - 1.0, y - 0.3, 0.45, x + 1.0, y + 0.3, 0.6, col, "wood", seed, w=0.8)
        box(g, S, iso, x - 1.0, y - 0.35, 0.6, x + 1.0, y - 0.22, 1.2, col, "wood", seed + 1, w=0.8)
    else:
        box(g, S, iso, x - 0.3, y - 1.0, 0.45, x + 0.3, y + 1.0, 0.6, col, "wood", seed, w=0.8)
        box(g, S, iso, x - 0.35, y - 1.0, 0.6, x - 0.22, y + 1.0, 1.2, col, "wood", seed + 1, w=0.8)


def wheel(g, S, iso, x, y0, y1, z, r, col=(40, 40, 44), seed=0):
    ts = np.linspace(0, math.tau, 14, endpoint=False)
    solid(g, S, iso, [(x + r * math.cos(t), y1, z + r * math.sin(t)) for t in ts], [(x + r * math.cos(t), y0, z + r * math.sin(t)) for t in ts],
          col, "plain", seed, smooth_sides=True)


def cow(g, S, iso, x, y, seed=0, col=(250, 250, 246), spots=(40, 36, 40)):
    for (lx, ly) in ((-0.8, -0.35), (0.8, -0.35), (-0.8, 0.35), (0.8, 0.35)):
        box(g, S, iso, x + lx - 0.12, y + ly - 0.12, 0, x + lx + 0.12, y + ly + 0.12, 0.7, col, "plain", seed, w=0.6)
    box(g, S, iso, x - 1.1, y - 0.5, 0.7, x + 1.1, y + 0.5, 1.5, col, "plain", seed + 1, w=0.8)
    box(g, S, iso, x + 1.0, y - 0.35, 1.0, x + 1.6, y + 0.35, 1.7, col, "plain", seed + 2, w=0.8)
    for (sx_, sy_, sz) in ((-0.4, 0.5, 1.1), (0.4, 0.5, 1.25), (1.1, 0.0, 1.5)):
        px, py = iso.p(x + sx_, y + sy_, sz)
        g.fill(Ell(px, py, 4.5, 3.4), spots)


def sheep(g, S, iso, x, y, seed=0):
    for (lx, ly) in ((-0.4, -0.2), (0.4, -0.2), (-0.4, 0.2), (0.4, 0.2)):
        box(g, S, iso, x + lx - 0.08, y + ly - 0.08, 0, x + lx + 0.08, y + ly + 0.08, 0.5, (50, 46, 50), "plain", seed, w=0.5)
    px, py = iso.p(x, y, 0.85)
    S.blob(g, px, py, 15, 11, (246, 244, 236), seed + 1)
    hx, hy = iso.p(x + 0.8, y, 0.95)
    S.blob(g, hx, hy, 5, 5, (60, 54, 56), seed + 2, kind="body")


def chicken(g, S, iso, x, y, seed=0):
    px, py = iso.p(x, y, 0.35)
    S.blob(g, px, py, 9, 7, (250, 248, 240), seed, kind="body")
    S.blob(g, px + 6, py - 9, 4.5, 4.5, (250, 248, 240), seed + 1, kind="body")
    g.fill(Ell(px + 6, py - 14, 2.6, 2), (220, 40, 40))
    g.fill(Poly([(px + 10, py - 10), (px + 15, py - 8), (px + 10, py - 7)]), (240, 170, 40))


def water_tower(g, S, iso, x, y, z0, col, seed=0, legs=2.0):
    for (lx, ly) in ((-0.9, -0.9), (0.9, -0.9), (-0.9, 0.9), (0.9, 0.9)):
        box(g, S, iso, x + lx - 0.1, y + ly - 0.1, z0, x + lx + 0.1, y + ly + 0.1, z0 + legs, (70, 60, 56), "wood", seed, w=0.7)
    cyl(g, S, iso, x, y, z0 + legs, z0 + legs + 2.4, 1.3, col, "wood", seed + 1)
    cone(g, S, iso, x, y, z0 + legs + 2.4, z0 + legs + 3.3, 1.45, mixc(col, (40, 40, 50), 0.35), "roof", seed + 2)


def cactus(g, S, iso, x, y, h, seed=0, col=(70, 140, 70), arms=True):
    cyl(g, S, iso, x, y, 0, h, 0.32, col, "plain", seed, n=10, r1=0.28)
    if arms:
        for sgn, z in ((1, h * 0.45), (-1, h * 0.6)):
            ax = x + sgn * 0.75
            cyl(g, S, iso, ax, y, z, z + h * 0.32, 0.2, col, "plain", seed + 3, n=8)
            box(g, S, iso, min(x, ax), y - 0.18, z - 0.18, max(x, ax), y + 0.18, z + 0.18, col, "plain", seed + 4, w=0.7)


def parapet(g, S, iso, x0, y0, x1, y1, z, col, seed=0, t=0.3, h=0.6):
    for (a0, b0, a1, b1) in ((x0, y0, x1, y0 + t), (x0, y0, x0 + t, y1), (x1 - t, y0, x1, y1), (x0, y1 - t, x1, y1)):
        box(g, S, iso, a0, b0, z, a1, b1, z + h, col, "plain", seed, w=0.8)


def building(g, S, iso, x0, y0, x1, y1, h, col, roof_col, seed=0, rows=None, glass=(110, 140, 170), lit=None, roof_kind="road"):
    box(g, S, iso, x0, y0, 0, x1, y1, h, col, "plain", seed, top_col=roof_col, top_kind=roof_kind)
    rows = rows or max(1, int(h / 2.6))
    windows(g, S, iso, "y", y1, x0 + 0.4, x1 - 0.4, 0.6, h - 0.5, max(1, int((x1 - x0) / 2.2)), glass=glass, rows=rows, lit=lit, seed=seed)
    windows(g, S, iso, "x", x1, y0 + 0.4, y1 - 0.4, 0.6, h - 0.5, max(1, int((y1 - y0) / 2.2)), glass=glass, rows=rows, lit=lit, seed=seed + 3)


# =================================================================== Level 1533 city street corner (realistic)
I33 = iso_at(13, 17, 22.0)
R33 = Real(warm=2)


def l1533_scene(g, S, d):
    iso = I33
    decal(g, S, iso, [(-60, -60), (90, -60), (90, 90), (-60, 90)], (190, 186, 178), "plain", 3301)
    for k in range(-30, 60, 3):              # paving joints
        a, b = iso.p(k, -40), iso.p(k, 60)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.6), (150, 146, 140), alpha=0.5)
        a, b = iso.p(-40, k), iso.p(60, k)
        g.fill(Seg(a[0], a[1], b[0], b[1], 0.6), (150, 146, 140), alpha=0.5)
    decal(g, S, iso, rect_ring(-60, 10, 90, 16), (66, 68, 72), "road", 3302)
    decal(g, S, iso, rect_ring(13, -60, 19, 90), (66, 68, 72), "road", 3303)
    for x in range(-30, 60, 4):
        if not (10 <= x <= 21):
            decal(g, S, iso, rect_ring(x, 12.9, x + 2, 13.1), (236, 230, 200), "plain", 3304)
    for y in range(-30, 60, 4):
        if not (7 <= y <= 18):
            decal(g, S, iso, rect_ring(15.9, y, 16.1, y + 2), (236, 230, 200), "plain", 3305)
    for k in range(7):
        decal(g, S, iso, rect_ring(10.6, 10.3 + k * 0.8, 12.6, 10.7 + k * 0.8), (236, 236, 230), "plain", 3306)
        decal(g, S, iso, rect_ring(13.3 + k * 0.8, 16.6, 13.7 + k * 0.8, 18.6), (236, 236, 230), "plain", 3307)
    for (a, b, c_, d_) in ((-60, 9.8, 13, 10), (19, 9.8, 90, 10), (-60, 16, 13, 16.2), (19, 16, 90, 16.2), (12.8, -60, 13, 10), (19, -60, 19.2, 10),
                           (12.8, 16, 13, 90), (19, 16, 19.2, 90)):
        decal(g, S, iso, rect_ring(a, b, c_, d_), (150, 148, 144), "plain", 3308)
    # park (SW block) and plaza (SE)
    decal(g, S, iso, rect_ring(-20, 18.5, 10.5, 50), (96, 140, 66), "grass", 3309)
    decal(g, S, iso, strip(iso, [(-12, 30), (0, 26), (10.5, 22)], 1.8), (200, 186, 156), "dirt", 3310)
    sc = Scene()
    shadows = []
    # buildings
    blds = [(-6, -14, 10.5, 7.5, 9.0, (176, 160, 140), (110, 110, 116), 3320), (21.5, -8, 34, 7.5, 5.0, (196, 120, 96), (120, 116, 112), 3321),
            (26, 23, 36, 34, 4.0, (210, 200, 176), (124, 120, 116), 3322)]
    for (x0, y0, x1, y1, h, col, rc, sd) in blds:
        shadows.append((rect_ring(x0, y0, x1, y1), h))
        sc.add(x1, y1, lambda x0=x0, y0=y0, x1=x1, y1=y1, h=h, col=col, rc=rc, sd=sd: building(g, S, iso, x0, y0, x1, y1, h, col, rc, sd))
    # cafe awning on building B (difference: colour) + tables with umbrellas (difference: one umbrella)
    awc = [(40, 110, 70), (240, 236, 226)] if "awning" not in d else [(200, 60, 50), (240, 236, 226)]
    sc.add(34, 9.0, lambda: awning(g, S, iso, 22.5, 33, 7.5, 2.6, 1.4, awc, 3330), on=(34, 7.5), dz=9)
    for k, (x, y, cols) in enumerate(((24, 20, [(230, 80, 60), (250, 246, 236)]), (20.8, 21.5, [(60, 120, 180), (250, 246, 236)]))):
        if k == 1 and "umbrella" in d:
            continue
        shadows.append(([(x + 1.3 * math.cos(t), y + 1.3 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 2.4))
        sc.add(x, y, lambda x=x, y=y, cols=cols, k=k: (cyl(g, S, iso, x, y, 0, 0.75, 0.6, (240, 240, 240), "metal", 3335 + k),
                                                       umbrella(g, S, iso, x, y, 2.2, 1.4, cols, 3337 + k)))
    # rooftop: AC units (difference) and a water tank on A
    for k, (x, y) in enumerate(((24, -5), (28, -3), (31, -6))):
        if k == 1 and "ac" in d:
            continue
        sc.add(x, y, lambda x=x, y=y, k=k: box(g, S, iso, x, y, 5.0, x + 1.6, y + 1.2, 6.0, (200, 200, 204), "metal", 3340 + k), dz=k, on=(34, 7.5))
    sc.add(2, -6, lambda: (cyl(g, S, iso, 2, -6, 9.0, 11.0, 1.2, (150, 120, 90), "wood", 3345),
                           cone(g, S, iso, 2, -6, 11.0, 11.8, 1.3, (90, 80, 76), "roof", 3346)), on=(10.5, 7.5))
    # cars (difference: colour of one)
    cars = [(2, 11.5, (190, 40, 40), True), (29, 14.5, (40, 80, 160), True),
            (44, 11.5, (230, 230, 230), True), (14.5, -6, (240, 200, 40) if "car" not in d else (60, 160, 220), False), (17.5, 30, (60, 120, 80), False)]
    for k, (x, y, col, ax) in enumerate(cars):
        r_ = rect_ring(x - 1.8, y - 0.85, x + 1.8, y + 0.85) if ax else rect_ring(x - 0.85, y - 1.8, x + 0.85, y + 1.8)
        shadows.append((r_, 1.2))
        sc.add(x + (1.8 if ax else 0.85), y + (0.85 if ax else 1.8), lambda x=x, y=y, col=col, ax=ax, k=k: car(g, S, iso, x, y, col, ax, 3350 + k))
    # street trees, lamp posts, traffic lights
    for k, (x, y) in enumerate(((4, 8.6), (24, 8.6), (6, 17.4), (30, 17.4), (20.4, 26), (11.6, -4))):
        decal(g, S, iso, [(x + 0.8 * math.cos(t), y + 0.8 * math.sin(t)) for t in np.linspace(0, math.tau, 10, endpoint=False)], (90, 70, 50), "dirt", 3360 + k)
        shadows.append(("tree", x, y, 4.2))
        sc.add(x, y, lambda x=x, y=y, k=k: tree(g, S, iso, x, y, 4.2, (74, 116, 50), 3365 + k))
    for k, (x, y) in enumerate(((12.4, 9.4), (19.6, 16.6))):
        sc.add(x, y, lambda x=x, y=y, k=k: (cyl(g, S, iso, x, y, 0, 3.4, 0.1, (60, 64, 70), "metal", 3370 + k, n=6),
                                           box(g, S, iso, x - 0.25, y - 0.25, 3.4, x + 0.25, y + 0.25, 4.6, (40, 44, 50), "metal", 3372 + k)))
    for k, (x, y) in enumerate(((-2, 8.8), (34, 8.8), (12.2, 26), (19.8, -2))):
        sc.add(x, y, lambda x=x, y=y, k=k: lamp_post(g, S, iso, x, y, 3.4, 3375 + k))
    # park: fountain, trees (difference), benches (difference)
    shadows.append(([(2 + 2.2 * math.cos(t), 30 + 2.2 * math.sin(t)) for t in np.linspace(0, math.tau, 12, endpoint=False)], 0.6))
    def fountain():
        cyl(g, S, iso, 2, 30, 0, 0.6, 2.2, (200, 196, 186), "stone", 3380)
        cx, cy = iso.p(2, 30, 0.6)
        g.fill(Ell(cx, cy, 2.0 * iso.u * 0.86, 2.0 * iso.u * 0.48), (80, 140, 170))
        cyl(g, S, iso, 2, 30, 0.6, 1.6, 0.35, (200, 196, 186), "stone", 3381)
    sc.add(4.2, 32.2, fountain)
    for k, (x, y, h) in enumerate(((-8, 22, 5.0), (6, 22, 4.4), (-4, 36, 5.2), (8, 38, 4.6))):
        if k == 0 and "tree" in d:
            continue
        shadows.append(("tree", x, y, h))
        sc.add(x, y, lambda x=x, y=y, h=h, k=k: tree(g, S, iso, x, y, h, (70, 116, 48), 3385 + k))
    for k, (x, y) in enumerate(((-2, 27), (6.5, 33))):
        if k == 1 and "bench" in d:
            continue
        sc.add(x, y, lambda x=x, y=y, k=k: bench(g, S, iso, x, y, True, seed=3390 + k))
    # bicycle (difference) leaning by building B, people
    if "bike" not in d:
        def bike():
            for wx in (1.2, 2.8):
                p = iso.p(wx, 8.9, 0.5)
                g.fill(Ell(p[0], p[1], 9, 9) - Ell(p[0], p[1], 7.5, 7.5), (30, 30, 34))
            a, b = iso.p(1.2, 8.9, 0.5), iso.p(2.8, 8.9, 0.5)
            c_ = iso.p(2.0, 8.9, 1.1)
            for p0, p1 in ((a, c_), (c_, b), (a, b)):
                g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 2.2), (40, 120, 180))
        sc.add(3, 9.0, bike)
    for k, (x, y) in enumerate(((8, 9), (26, 9.2), (11.5, 18), (-6, 28), (22, 18.2), (20.4, 4))):
        pc = ((60, 100, 160), (190, 70, 60), (60, 60, 64), (200, 170, 60), (110, 70, 140), (240, 240, 236))[k]
        sc.add(x, y, lambda x=x, y=y, pc=pc, k=k: person(g, S, iso, x, y, pc, 3395 + k))
    for sh in shadows:
        if sh[0] == "tree":
            tree_shadow(g, S, iso, sh[1], sh[2], sh[3])
        else:
            shadow(g, S, iso, sh[0], 0, sh[1])
    sc.draw()


_s33 = sp_of(I33)
L1533_ELEMENTS = [
    E("pigeons", el(lambda g, m: [g.fill(Seg(x - 5, y - 1, x + 5, y - 1, 1.6), (70, 70, 80)) for x, y in ((520, 60), (536, 70))]),
      anim=dict(driftVelocity=(30, 6), driftLength=500, driftStart=-300, stretch=(0, 0.5), scaleSpeed=2.2)),
    E("water", el(lambda g, m: g.fill(Ell(*_s33(2, 30, 1.9), 6, 10), (220, 240, 250), alpha=0.7, feather=2)), anim=dict(stretch=(0.05, 0.2), scaleSpeed=1.5)),
]

L1533_DIFFS = [
    ("awning", *_s33(27.7, 8.2, 2.3), 0),
    ("umbrella", *_s33(20.8, 21.5, 2.4), 0),
    ("ac", *_s33(28.8, -2.4, 5.5), 0),
    ("car", *_s33(14.5, -6, 0.8), 0),
    ("tree", *_s33(-8, 22, 3.2), 0),
    ("bench", *_s33(6.5, 33, 0.8), 0),
    ("bike", *_s33(2, 8.9, 0.6), 0),
]


# =================================================================== Level 1534 toon farm
I34 = iso_at(13, 7, 22.0)
T34 = Toon()


def l1534_scene(g, S, d):
    iso = I34
    decal(g, S, iso, [(-60, -60), (90, -60), (90, 90), (-60, 90)], (130, 196, 90), "grass", 3401)
    decal(g, S, iso, strip(iso, [(-20, 6), (0, 6), (12, 4), (16, -2), (18, -14)], 2.2), (220, 180, 120), "dirt", 3402, outline=True)
    decal(g, S, iso, strip(iso, [(12, 4), (16, 10), (16, 40)], 2.0), (220, 180, 120), "dirt", 3403, outline=True)
    for k in range(9):                      # crop field rows
        decal(g, S, iso, rect_ring(19, 8 + k * 2, 40, 9 + k * 2), (170, 110, 70), "dirt", 3404 + k, outline=False)
        decal(g, S, iso, rect_ring(19, 9 + k * 2, 40, 10 + k * 2), (110, 180, 70) if k % 3 else (240, 206, 90), "grass", 3420 + k, outline=False)
    decal(g, S, iso, rect_ring(3, 28, 11, 36), (170, 110, 70), "dirt", 3430, outline=True)
    decal(g, S, iso, [(-10, 26), (-4, 23), (1, 26), (0, 32), (-6, 34), (-11, 31)], (110, 180, 230), "water", 3431, outline=True, rough=4)
    sc = Scene()
    shadows = []
    # barn + silo + farmhouse
    shadows.append((rect_ring(0, -5, 7, 3), 6.5))
    def barn():
        gable(g, S, iso, 0, -5, 7, 3, 0, 3.8, 3.0, (206, 62, 52), (120, 76, 66), 3440, along_x=False)
        door = quad_on(iso, "y", 2.2, 4.8, 0, 2.8, 3)
        S.face(g, door, (240, 236, 226), 0.8, "plain", 3441)
        dc = (150, 50, 44) if "door" not in d else (60, 110, 170)
        S.face(g, quad_on(iso, "y", 2.45, 4.55, 0, 2.6, 3), dc, 0.8, "wood", 3442, ang=-0.4)
        for p0, p1 in ((iso.p(2.45, 3, 0), iso.p(4.55, 3, 2.6)), (iso.p(4.55, 3, 0), iso.p(2.45, 3, 2.6))):
            g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 3), (240, 236, 226))
        S.face(g, quad_on(iso, "y", 3.0, 4.0, 4.3, 5.2, 3.0), (240, 236, 226), 0.8, "plain", 3443)
        if "vane" not in d:
            p = iso.p(3.5, -1, 6.8)
            g.fill(Seg(p[0], p[1], p[0], p[1] - 22, 2), S.ink)
            g.fill(Poly([(p[0] - 10, p[1] - 22), (p[0] + 8, p[1] - 26), (p[0] + 10, p[1] - 20)]), S.ink)
    sc.add(7, 3, barn)
    shadows.append(([(9.8 + 1.8 * math.cos(t), -4 + 1.8 * math.sin(t)) for t in np.linspace(0, math.tau, 10, endpoint=False)], 8.5))
    sc.add(9.8, -4, lambda: (cyl(g, S, iso, 9.8, -4, 0, 7.5, 1.8, (200, 206, 216), "metal", 3445),
                             cone(g, S, iso, 9.8, -4, 7.5, 8.8, 1.9, (90, 130, 190), "plain", 3446)))
    shadows.append((rect_ring(16, -14, 23, -8), 5.0))
    def house():
        gable(g, S, iso, 16, -14, 23, -8, 0, 3.0, 2.0, (250, 244, 226), (80, 120, 190), 3447, along_x=True)
        windows(g, S, iso, "y", -8, 16.4, 22.6, 0.7, 2.7, 3, glass=(160, 210, 240), seed=3448)
        box(g, S, iso, 21, -12, 4.0, 21.8, -11.2, 5.6, (200, 80, 70), "plain", 3449)
    sc.add(23, -8, house)
    # windmill tower (blades are an element)
    shadows.append(([(30 + 1.2 * math.cos(t), 0 + 1.2 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 7))
    sc.add(30, 0, lambda: (cyl(g, S, iso, 30, 0, 0, 6.5, 1.4, (240, 230, 210), "plain", 3450, r1=0.9, n=10),
                           cone(g, S, iso, 30, 0, 6.5, 7.8, 1.1, (170, 70, 60), "plain", 3451, n=10)))
    # paddock with cows (difference: one) and sheep
    sc.add(-8, 20, lambda: fence(g, S, iso, [(-10, 8), (8, 8), (8, 20), (-10, 20)], (240, 236, 226), seed=3455), dz=-30)
    sc.add(8, 20, lambda: fence(g, S, iso, [(8, 8), (8, 20), (-10, 20)], (240, 236, 226), seed=3456))
    for k, (x, y) in enumerate(((-4, 12), (2, 15))):
        if k == 1 and "cow" in d:
            continue
        shadows.append((rect_ring(x - 1.1, y - 0.5, x + 1.6, y + 0.5), 1.6))
        sc.add(x + 1.6, y + 0.5, lambda x=x, y=y, k=k: cow(g, S, iso, x, y, 3460 + k))
    for k, (x, y) in enumerate(((-6, 17), (-1, 18), (4, 11))):
        shadows.append(([(x + 0.6 * math.cos(t), y + 0.6 * math.sin(t)) for t in np.linspace(0, math.tau, 8, endpoint=False)], 1.0))
        sc.add(x + 0.8, y, lambda x=x, y=y, k=k: sheep(g, S, iso, x, y, 3465 + k))
    sc.add(-7, 10, lambda: box(g, S, iso, -8, 9.5, 0, -5, 10.4, 0.7, (150, 110, 70), "wood", 3469))
    # tractor (difference: colour)
    tc = (80, 170, 70) if "tractor" not in d else (230, 90, 50)
    shadows.append((rect_ring(33, 4, 37, 6.4), 2.4))
    def tractor():
        wheel(g, S, iso, 33.6, 3.9, 4.4, 0.75, 0.75, seed=3470)
        wheel(g, S, iso, 36.2, 4.1, 4.5, 0.5, 0.5, seed=3471)
        box(g, S, iso, 33, 4.4, 0.6, 37, 6.0, 1.4, tc, "plain", 3472)
        box(g, S, iso, 33.1, 4.5, 1.4, 34.8, 5.9, 2.7, (200, 230, 250), "glass", 3473, top_col=tc)
        box(g, S, iso, 36.0, 5.0, 1.4, 36.3, 5.3, 2.2, (60, 60, 60), "metal", 3474)
        wheel(g, S, iso, 33.6, 6.0, 6.5, 0.75, 0.75, seed=3475)
        wheel(g, S, iso, 36.2, 5.9, 6.3, 0.5, 0.5, seed=3476)
    sc.add(37, 6.5, tractor)
    # pumpkins (difference: one), scarecrow (difference), haystacks, chickens (difference), mailbox, trees
    for k, (x, y) in enumerate(((5, 30), (7.5, 31), (9, 33.5), (5.5, 34), (8, 29))):
        if k == 2 and "pumpkin" in d:
            continue
        sc.add(x, y, lambda x=x, y=y, k=k: S.blob(g, *iso.p(x, y, 0.5), 15, 12, (250, 140, 40), 3480 + k, kind="body"))
    if "scarecrow" not in d:
        def scare():
            box(g, S, iso, 28.9, 15.9, 0, 29.1, 16.1, 3.2, (130, 90, 60), "wood", 3486)
            box(g, S, iso, 28.0, 15.9, 2.2, 30.0, 16.1, 2.4, (130, 90, 60), "wood", 3487)
            box(g, S, iso, 28.6, 15.7, 1.4, 29.4, 16.3, 2.6, (90, 120, 200), "plain", 3488)
            p = iso.p(29, 16, 3.2)
            S.blob(g, p[0], p[1], 7, 7, (240, 210, 140), 3489, kind="body")
            g.fill(Ell(p[0], p[1] - 6, 12, 4), (220, 180, 80))
        sc.add(29.1, 16.1, scare)
    for k, (x, y) in enumerate(((10, 6), (12, 1))):
        sc.add(x, y, lambda x=x, y=y, k=k: (cyl(g, S, iso, x, y, 0, 1.0, 1.0, (240, 210, 110), "plain", 3490 + k),
                                           cone(g, S, iso, x, y, 1.0, 1.8, 1.0, (240, 210, 110), "plain", 3492 + k)))
    for k, (x, y) in enumerate(((24, -4.5), (24.8, -3.3), (25.6, -5.1), (25.8, -3.7))):
        if k in (1, 3) and "chicken" in d:
            continue
        sc.add(x, y, lambda x=x, y=y, k=k: chicken(g, S, iso, x, y, 3495 + k))
    for k, (x, y, h) in enumerate(((-8, -6, 5), (-12, 2, 4.5), (26, -10, 4.6), (36, 28, 5), (-2, 36, 4.4))):
        shadows.append(("tree", x, y, h))
        sc.add(x, y, lambda x=x, y=y, h=h, k=k: tree(g, S, iso, x, y, h, (90, 170, 70), 3500 + k))
    sc.add(14, 9, lambda: (box(g, S, iso, 13.9, 8.9, 0, 14.1, 9.1, 1.2, (130, 90, 60), "wood", 3510),
                           box(g, S, iso, 13.6, 8.7, 1.2, 14.4, 9.3, 1.7, (60, 110, 190), "metal", 3511)))
    for sh in shadows:
        if sh[0] == "tree":
            tree_shadow(g, S, iso, sh[1], sh[2], sh[3])
        else:
            shadow(g, S, iso, sh[0], 0, sh[1])
    sc.draw()


_s34 = sp_of(I34)


def l1534_blades(g, m):
    hx, hy = _s34(30.95, 0.6, 6.2)
    for k in range(4):
        a = k * math.pi / 2 + 0.3
        ex, ey = hx + math.cos(a) * 56, hy + math.sin(a) * 56
        nx, ny = -math.sin(a) * 9, math.cos(a) * 9
        blade = Poly([(hx + nx * 0.3, hy + ny * 0.3), (ex + nx, ey + ny), (ex - nx * 0.2, ey - ny * 0.2), (hx - nx * 0.3, hy - ny * 0.3)])
        g.fill(blade, TINK)
        g.fill(Poly([(hx + nx * 0.3 + math.cos(a) * 6, hy + ny * 0.3 + math.sin(a) * 6), (ex + nx * 0.8 - math.cos(a) * 2, ey + ny * 0.8 - math.sin(a) * 2),
                     (ex - math.cos(a) * 2, ey - math.sin(a) * 2), (hx + math.cos(a) * 6, hy + math.sin(a) * 6)]), (250, 244, 226))
    g.fill(Circ(hx, hy, 6), TINK)
    g.fill(Circ(hx, hy, 4), (200, 80, 70))


L1534_ELEMENTS = [
    E("blades", el(l1534_blades), pivot=_s34(30.95, 0.6, 6.2), anim=dict(rotateSpeed=-40)),
    E("smoke", el(lambda g, m: [g.fill(Circ(x, y, r), TINK) or g.fill(Circ(x, y, r - 1.6), (250, 250, 250)) for x, y, r in ((_s34(21.4, -11.6, 5.8)[0], _s34(21.4, -11.6, 5.8)[1] - 10, 7),)]),
      anim=dict(driftVelocity=(8, 40), driftLength=60, driftFade=True, driftGrow=1.6)),
    E("cloudshadow", el(lambda g, m: g.fill(Ell(300, 420, 120, 50), (60, 40, 140), alpha=0.08, feather=30)), anim=dict(driftVelocity=(20, 0), driftLength=900, driftStart=-500)),
]

L1534_DIFFS = [
    ("door", *_s34(3.5, 3, 1.3), 0),
    ("vane", _s34(3.5, -1, 6.8)[0], _s34(3.5, -1, 6.8)[1] - 20, 0),
    ("cow", *_s34(2.3, 15, 1.1), 0),
    ("tractor", *_s34(35, 5.2, 1.3), 0),
    ("pumpkin", *_s34(9, 33.5, 0.5), 0),
    ("scarecrow", *_s34(29, 16, 2.4), 0),
    ("chicken", *_s34(25.3, -3.9, 0.5), 0),
]


# =================================================================== Level 1535 toon amusement park
I35 = iso_at(16, 11, 21.0)
T35 = Toon()
STRIPE_R = [(230, 70, 70), (250, 246, 236)]
STRIPE_B = [(70, 130, 220), (250, 246, 236)]
STRIPE_Y = [(250, 200, 60), (230, 90, 60)]


def l1535_scene(g, S, d):
    iso = I35
    decal(g, S, iso, [(-60, -60), (90, -60), (90, 90), (-60, 90)], (130, 200, 100), "grass", 3501)
    decal(g, S, iso, strip(iso, [(-20, 12), (6, 12), (14, 12), (40, 12)], 4.0), (240, 220, 180), "plain", 3502, outline=True)
    decal(g, S, iso, strip(iso, [(14, -20), (14, 12), (14, 40)], 4.0), (240, 220, 180), "plain", 3503, outline=True)
    decal(g, S, iso, [(14 + 7 * math.cos(t), 12 + 7 * math.sin(t)) for t in np.linspace(0, math.tau, 20, endpoint=False)], (240, 220, 180), "plain", 3504, outline=True)
    decal(g, S, iso, [(14 + 2.5 * math.cos(t), 12 + 2.5 * math.sin(t)) for t in np.linspace(0, math.tau, 16, endpoint=False)], (110, 190, 240), "water", 3505, outline=True)
    sc = Scene()
    shadows = []
    # carousel (difference: flag colour)
    cx, cy = 4, 2
    shadows.append(([(cx + 4 * math.cos(t), cy + 4 * math.sin(t)) for t in np.linspace(0, math.tau, 12, endpoint=False)], 5.0))
    def carousel():
        cyl(g, S, iso, cx, cy, 0, 0.6, 3.6, (250, 236, 200), "plain", 3510, n=20)
        cyl(g, S, iso, cx, cy, 0.6, 3.6, 0.5, (240, 200, 80), "plain", 3511, n=10)
        for k in range(8):
            a = k * math.tau / 8
            px, py = cx + 2.7 * math.cos(a), cy + 2.7 * math.sin(a)
            cyl(g, S, iso, px, py, 0.6, 3.4, 0.07, (240, 210, 90), "metal", 3512, n=6, edges=False)
            hc = ((250, 250, 250), (240, 160, 180), (160, 200, 250), (250, 220, 120))[k % 4]
            box(g, S, iso, px - 0.45, py - 0.2, 1.4, px + 0.45, py + 0.2, 2.0, hc, "plain", 3513 + k, w=0.7)
        ts = np.linspace(0, math.tau, 16, endpoint=False)
        solid(g, S, iso, [(cx, cy, 5.6)] * 16, [(cx + 3.9 * math.cos(t), cy + 3.9 * math.sin(t), 3.4) for t in ts], STRIPE_R[0], "plain", 3520,
              side_cols=STRIPE_R)
        p = iso.p(cx, cy, 5.6)
        g.fill(Seg(p[0], p[1], p[0], p[1] - 30, 2.2), S.ink)
        fc = (250, 200, 60) if "flag" not in d else (70, 130, 220)
        fl = Poly([(p[0] + 1, p[1] - 30), (p[0] + 30, p[1] - 22), (p[0] + 1, p[1] - 13)])
        g.fill(fl, fc)
        for i in range(3):
            S.edge(g, fl.p[i], fl.p[(i + 1) % 3], sil=False)
    sc.add(cx + 3.6, cy + 3.6, carousel)
    # ferris wheel in the plane x = 30 (difference: one cabin colour)
    fx, fy, fz, R = 30, 4, 8.0, 6.0
    def ferris():
        for sgn in (-1, 1):
            a, b = iso.p(fx, fy + sgn * 3.5, 0), iso.p(fx, fy, fz)
            g.fill(Seg(a[0], a[1], b[0], b[1], 6), S.ink)
            g.fill(Seg(a[0], a[1], b[0], b[1], 3.6), (250, 250, 250))
        pts = [iso.p(fx, fy + R * math.cos(t), fz + R * math.sin(t)) for t in np.linspace(0, math.tau, 40)]
        for p0, p1 in zip(pts[:-1], pts[1:]):
            g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 5), S.ink)
            g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 2.6), (230, 80, 80))
        c0 = iso.p(fx, fy, fz)
        for k in range(10):
            t = k * math.tau / 10
            p = iso.p(fx, fy + R * math.cos(t), fz + R * math.sin(t))
            g.fill(Seg(c0[0], c0[1], p[0], p[1], 1.6), S.ink)
        g.fill(Circ(c0[0], c0[1], 6), S.ink)
        g.fill(Circ(c0[0], c0[1], 4), (250, 200, 60))
        for k in range(10):
            t = k * math.tau / 10 + 0.31
            ey, ez = fy + R * math.cos(t), fz + R * math.sin(t)
            col = ((240, 100, 100), (100, 180, 240), (250, 210, 80), (140, 210, 120), (220, 140, 220))[k % 5]
            if k == 3 and "cabin" in d:
                col = (120, 90, 200)
            box(g, S, iso, fx - 0.45, ey - 0.5, ez - 1.3, fx + 0.45, ey + 0.5, ez - 0.4, col, "plain", 3530 + k, w=0.8)
    shadows.append((rect_ring(fx - 0.5, fy - 6, fx + 0.5, fy + 6), 9))
    sc.add(fx + 1, fy + 6, ferris)
    # circus tent (difference: top flag) and food stalls (difference: awning colour)
    tx, ty = 2, 22
    shadows.append(([(tx + 4 * math.cos(t), ty + 4 * math.sin(t)) for t in np.linspace(0, math.tau, 12, endpoint=False)], 6))
    def tent():
        cyl(g, S, iso, tx, ty, 0, 2.4, 3.8, STRIPE_B[0], "plain", 3540, n=16, side_cols=STRIPE_B)
        ts = np.linspace(0, math.tau, 16, endpoint=False)
        solid(g, S, iso, [(tx, ty, 6.2)] * 16, [(tx + 4.1 * math.cos(t), ty + 4.1 * math.sin(t), 2.3) for t in ts], STRIPE_B[0], "plain", 3541,
              side_cols=STRIPE_B)
        S.face(g, quad_on(iso, "y", tx - 0.8, tx + 0.8, 0, 2.0, ty + 3.75), (60, 40, 70), 0.3, "plain", 3542)
        if "tentflag" not in d:
            p = iso.p(tx, ty, 6.2)
            g.fill(Seg(p[0], p[1], p[0], p[1] - 32, 2.2), S.ink)
            fl = Poly([(p[0] + 1, p[1] - 32), (p[0] + 30, p[1] - 24), (p[0] + 1, p[1] - 15)])
            g.fill(fl, (250, 90, 90))
            for i in range(3):
                S.edge(g, fl.p[i], fl.p[(i + 1) % 3], sil=False)
    sc.add(tx + 4, ty + 4, tent)
    for k, (x0, y0, cols) in enumerate(((19, 17, STRIPE_Y), (24, 17, STRIPE_R if "stall" not in d else STRIPE_B))):
        shadows.append((rect_ring(x0, y0, x0 + 3.2, y0 + 2.4), 3.0))
        def stall(x0=x0, y0=y0, cols=cols, k=k):
            box(g, S, iso, x0, y0, 0, x0 + 3.2, y0 + 2.4, 1.2, (250, 240, 220), "plain", 3550 + k)
            for (px, py) in ((x0 + 0.1, y0 + 2.3), (x0 + 3.1, y0 + 2.3)):
                box(g, S, iso, px - 0.08, py - 0.08, 1.2, px + 0.08, py + 0.08, 2.4, (220, 220, 220), "metal", 3552 + k, w=0.6)
            solid(g, S, iso, [(x0 - 0.2, y0 - 0.2, 2.9), (x0 + 3.4, y0 - 0.2, 2.9), (x0 + 3.4, y0 + 2.8, 2.4), (x0 - 0.2, y0 + 2.8, 2.4)],
                  [(x0 - 0.2, y0 - 0.2, 2.6), (x0 + 3.4, y0 - 0.2, 2.6), (x0 + 3.4, y0 + 2.8, 2.1), (x0 - 0.2, y0 + 2.8, 2.1)], cols[0], "plain", 3554 + k,
                  side_cols=cols)
        sc.add(x0 + 3.2, y0 + 2.4, stall)
    # balloon seller (difference: balloon colours), ice cream cart (difference), benches, trees, lamps, people
    bcols = [(240, 80, 80), (80, 160, 240), (250, 210, 60), (150, 210, 110)] if "balloons" not in d else [(200, 120, 220)] * 4
    def balloons():
        person(g, S, iso, 18, 6, (240, 140, 60), 3560)
        hx, hy = iso.p(18.3, 6, 1.4)
        for k, (dx, dy) in enumerate(((-12, -46), (2, -54), (14, -44), (-2, -38))):
            g.fill(Seg(hx, hy, hx + dx, hy + dy + 8, 0.8), S.ink)
            S.blob(g, hx + dx, hy + dy, 7, 8.5, bcols[k], 3561 + k, kind="body")
    sc.add(18.5, 6.3, balloons)
    if "icecream" not in d:
        sc.add(9.5, 14.5, lambda: (box(g, S, iso, 8, 13.6, 0.4, 10, 14.6, 1.4, (250, 200, 220), "plain", 3570),
                                   wheel(g, S, iso, 8.6, 14.6, 14.8, 0.4, 0.4, seed=3571),
                                   umbrella(g, S, iso, 9, 14.1, 2.4, 1.2, [(250, 140, 180), (250, 246, 236)], 3572)))
    for k, (x, y, ax) in enumerate(((22, 9.5, True), (6, 15, True), (11, 25, False))):
        sc.add(x, y, lambda x=x, y=y, ax=ax, k=k: bench(g, S, iso, x, y, ax, (220, 110, 60), 3575 + k))
    for k, (x, y, h) in enumerate(((-6, -6, 4.6), (22, -6, 4.2), (-8, 14, 4.8), (34, 20, 5), (16, 30, 4.4), (26, 28, 4.6))):
        shadows.append(("tree", x, y, h))
        sc.add(x, y, lambda x=x, y=y, h=h, k=k: tree(g, S, iso, x, y, h, (90, 176, 80), 3580 + k))
    for k, (x, y) in enumerate(((10, 9.6), (18, 14.4), (10, 19))):
        sc.add(x, y, lambda x=x, y=y, k=k: lamp_post(g, S, iso, x, y, 3.0, 3586 + k))
    for k, (x, y, col) in enumerate(((12, 16, (80, 140, 220)), (15.5, 9, (240, 200, 60)), (6, 11.5, (200, 90, 160)), (24, 13, (90, 180, 120)), (20.5, 21, (240, 120, 80)))):
        sc.add(x, y, lambda x=x, y=y, col=col, k=k: person(g, S, iso, x, y, col, 3590 + k))
    for sh in shadows:
        if sh[0] == "tree":
            tree_shadow(g, S, iso, sh[1], sh[2], sh[3])
        else:
            shadow(g, S, iso, sh[0], 0, sh[1])
    sc.draw()


_s35 = sp_of(I35)


def l1535_spout(g, m):
    x, y = _s35(14, 12, 0.3)
    g.fill(Ell(x, y - 18, 5, 18), TINK)
    g.fill(Ell(x, y - 18, 3.4, 16.4), (220, 244, 255))


L1535_ELEMENTS = [
    E("spout", el(l1535_spout), pivot=_s35(14, 12, 0.3), anim=dict(stretch=(0.04, 0.18), scaleSpeed=1.4)),
    E("loose", el(lambda g, m: (g.fill(Seg(300, 210, 302, 228, 0.8), TINK), g.fill(Ell(300, 200, 8, 10), TINK), g.fill(Ell(300, 200, 6.4, 8.4), (250, 120, 160)))),
      anim=dict(driftVelocity=(6, 30), driftLength=260, driftFade=True)),
    E("confetti", el(lambda g, m: [g.fill(Box(x, y, x + 4, y + 2), c) for x, y, c in ((100, 80, (240, 80, 80)), (240, 40, (80, 160, 240)), (620, 60, (250, 210, 60)), (780, 120, (140, 210, 120)))]),
      anim=dict(driftVelocity=(4, -30), driftLength=200, driftFade=True, swingAngle=30, swingSpeed=0.8)),
]

L1535_DIFFS = [
    ("flag", _s35(4, 2, 5.6)[0] + 12, _s35(4, 2, 5.6)[1] - 22, 0),
    ("cabin", *_s35(30, 4 + 6 * math.cos(3 * math.tau / 10 + 0.31), 8 + 6 * math.sin(3 * math.tau / 10 + 0.31) - 0.9), 0),
    ("tentflag", _s35(2, 22, 6.2)[0] + 12, _s35(2, 22, 6.2)[1] - 24, 0),
    ("stall", *_s35(25.6, 18.2, 2.6), 0),
    ("balloons", _s35(18.3, 6, 1.4)[0], _s35(18.3, 6, 1.4)[1] - 46, 0),
    ("icecream", *_s35(9, 14.1, 1.6), 0),
]


# =================================================================== Level 1536 comic rooftops at night
I36 = iso_at(14, 4, 20.0)
C36 = Comic(night=True)
NIGHT_LIT = (255, 220, 90)


def l1536_scene(g, S, d):
    iso = I36
    decal(g, S, iso, [(-60, -60), (90, -60), (90, 90), (-60, 90)], (34, 38, 74), "road", 3601)
    for k in range(-20, 50, 4):
        decal(g, S, iso, rect_ring(k, 6.9, k + 2, 7.1), (240, 200, 60), "plain", 3602)
        decal(g, S, iso, rect_ring(25.9, k, 26.1, k + 2), (240, 200, 60), "plain", 3603)
    sc = Scene()
    shadows = []
    blds = [(-10, -12, 4, 4, 10, (70, 80, 130), (120, 126, 160), 3610), (6, -10, 18, 4, 7, (110, 70, 110), (140, 120, 150), 3611),
            (20, -14, 30, 4, 12, (60, 100, 120), (110, 140, 160), 3612), (-8, 9, 6, 22, 6, (120, 90, 80), (150, 130, 120), 3613),
            (8, 9, 20, 22, 8, (80, 70, 120), (130, 120, 160), 3614), (28, 9, 40, 20, 5, (90, 110, 90), (130, 150, 130), 3615)]
    for (x0, y0, x1, y1, h, col, rc, sd) in blds:
        shadows.append((rect_ring(x0, y0, x1, y1), h))
        def draw(x0=x0, y0=y0, x1=x1, y1=y1, h=h, col=col, rc=rc, sd=sd):
            building(g, S, iso, x0, y0, x1, y1, h, col, rc, sd, glass=(40, 50, 90), lit=NIGHT_LIT, roof_kind="roof")
            parapet(g, S, iso, x0, y0, x1, y1, h, mixc(col, (200, 200, 220), 0.25), sd + 1)
        sc.add(x1, y1, draw)
    # roof props (each at its building's roof height)
    if True:
        wcol = (170, 110, 70) if "tower" not in d else (90, 140, 170)
        sc.add(0, 0, lambda: water_tower(g, S, iso, -3, -4, 10, wcol, 3620), on=(4, 4))
    # billboard on B2 facing +y (difference: picture)
    def billboard():
        for x in (8, 15):
            box(g, S, iso, x - 0.1, -3.1, 7, x + 0.1, -2.9, 8.5, (60, 60, 70), "metal", 3625, w=0.7)
        box(g, S, iso, 7, -3.2, 8.5, 16, -2.8, 12, (240, 236, 220), "plain", 3626)
        pic = quad_on(iso, "y", 7.4, 15.6, 8.9, 11.6, -2.8)
        g.fill(pic, (250, 90, 60))
        if "billboard" not in d:
            c_ = iso.p(10, -2.8, 10.2)
            g.fill(Circ(c_[0], c_[1], 18), (250, 220, 60))
            g.fill(Circ(c_[0], c_[1], 18) - Circ(c_[0], c_[1], 15.5), S.ink)
        for x in (12.5, 14.5):
            a, b = iso.p(x, -2.8, 9.6), iso.p(x + 0.8, -2.8, 9.6)
            g.fill(Seg(a[0], a[1], b[0] + 14, b[1], 5), (250, 250, 240))
        for i in range(4):
            S.edge(g, pic.p[i], pic.p[(i + 1) % 4], sil=False)
        for k in range(3):
            lamp_p = iso.p(8.5 + k * 3, -2.4, 8.6)
            g.glow(lamp_p[0], lamp_p[1] - 30, 40, (255, 230, 150), 0.2)
    sc.add(16, -2.8, billboard, on=(18, 4))
    # antenna on the tall block (difference)
    if "antenna" not in d:
        def antenna():
            box(g, S, iso, 24.8, -6.2, 12, 25.2, -5.8, 18, (200, 200, 210), "metal", 3630, w=0.8)
            for z in (14, 15.5, 17):
                a, b = iso.p(24, -6, z), iso.p(26, -6, z)
                S.edge(g, a, b, sil=True)
            p = iso.p(25, -6, 18)
            g.fill(Circ(p[0], p[1], 4), (250, 60, 60))
        sc.add(25, -6, antenna, on=(30, 4))
    # AC units (difference: one) + stair housing on B4
    for k, (x, y) in enumerate(((-6, 12), (-3, 12), (-6, 16))):
        if k == 2 and "ac" in d:
            continue
        def ac(x=x, y=y, k=k):
            box(g, S, iso, x, y, 6, x + 2, y + 1.6, 7.2, (170, 176, 190), "metal", 3635 + k)
            c_ = iso.p(x + 1, y + 0.8, 7.2)
            g.fill(Ell(c_[0], c_[1], 11, 6), S.ink)
            g.fill(Ell(c_[0], c_[1], 9, 4.8), (90, 96, 120))
        sc.add(x + 2, y + 1.6, ac, on=(6, 22), dz=k)
    sc.add(4, 20, lambda: box(g, S, iso, 1, 17, 6, 4, 20, 8.4, (130, 100, 90), "plain", 3638), on=(6, 22), dz=5)
    # skylight on B5 (difference: lit) + hero crouching on the parapet corner (difference: cape colour)
    sc.add(14, 15, lambda: box(g, S, iso, 11, 12, 8, 15, 15, 8.8, (60, 70, 120), "glass", 3640,
                                top_col=NIGHT_LIT if "skylight" not in d else (50, 60, 110)), on=(20, 22))
    def hero():
        bx, by = iso.p(19.6, 21.6, 8.6)
        cape = (200, 30, 40) if "cape" not in d else (60, 160, 90)
        cp = Poly([(bx - 9, by - 51), (bx + 9, by - 51), (bx + 33, by + 6), (bx - 6, by + 3)])
        g.fill(cp, S.ink)
        g.fill(Poly([(bx - 6, by - 47), (bx + 7, by - 47), (bx + 28, by + 2), (bx - 3, by)]), cape)
        S.blob(g, bx, by - 21, 13, 21, (60, 70, 130), 3645, kind="body")
        S.blob(g, bx - 1, by - 51, 10, 10.5, (60, 70, 130), 3646, kind="body")
        g.fill(Box(bx - 9, by - 54, bx + 6, by - 49), (250, 250, 250))
        g.fill(Poly([(bx - 6, by - 27), (bx, by - 33), (bx + 6, by - 27), (bx, by - 21)]), (250, 220, 60))
    sc.add(20, 22, hero, on=(20, 22), dz=9)
    # laundry line + satellite dish on B6, pigeons (difference)
    def b6():
        for x in (30, 36):
            box(g, S, iso, x - 0.08, 12, 5, x + 0.08, 12.16, 7, (200, 200, 210), "metal", 3650, w=0.6)
        a, b = iso.p(30, 12, 6.8), iso.p(36, 12, 6.8)
        g.fill(Seg(a[0], a[1], b[0], b[1], 1), S.ink)
        for k, col in enumerate(((250, 250, 240), (240, 90, 90), (90, 160, 240))):
            p = iso.p(31 + k * 1.8, 12, 6.8)
            sh = Poly([(p[0] - 8, p[1]), (p[0] + 8, p[1] - 1), (p[0] + 8, p[1] + 16), (p[0] - 8, p[1] + 17)])
            g.fill(sh, col)
            for i in range(4):
                S.edge(g, sh.p[i], sh.p[(i + 1) % 4], sil=False, w=0.7)
        cyl(g, S, iso, 38, 17, 5, 5.8, 0.2, (200, 200, 210), "metal", 3652, n=6)
        p = iso.p(38, 17, 6.4)
        g.fill(Ell(p[0], p[1], 15, 11), S.ink)
        g.fill(Ell(p[0], p[1], 12.6, 8.6), (220, 224, 236))
    sc.add(40, 20, b6, on=(40, 20))
    if "pigeons" not in d:
        def pigeons():
            for k in range(3):
                p = iso.p(9 + k * 1.2, 22.2, 8.6)
                S.blob(g, p[0], p[1] - 4, 6, 4.5, (150, 150, 170), 3655 + k, kind="body")
                g.fill(Circ(p[0] + 5, p[1] - 8, 2.6), (150, 150, 170))
        sc.add(12, 22.4, pigeons, on=(20, 22), dz=8)
    # street level: cars with headlights
    for k, (x, y, ax, col) in enumerate(((-4, 6, True, (230, 200, 60)), (16, 7.8, True, (200, 60, 60)), (25, 0, False, (80, 160, 220)), (27, 26, False, (240, 240, 240)))):
        sc.add(x, y, lambda x=x, y=y, ax=ax, col=col, k=k: car(g, S, iso, x, y, col, ax, 3660 + k), dz=-40)
    for (x0, y0, x1, y1, h, col, rc, sd) in blds:
        pass
    for sh in shadows:
        shadow(g, S, iso, sh[0], 0, sh[1], k=0.6)
    sc.draw()


_s36 = sp_of(I36)
L1536_ELEMENTS = [
    E("search", el(lambda g, m: g.fill(Poly([(820, 600), (860, 600), (560, -10), (470, -10)]), (255, 250, 200), alpha=0.12, feather=10)),
      daynight="untinted", anim=dict(swingAngle=6, swingSpeed=0.12), pivot=(840, 600)),
    E("windows", el(lambda g, m: [g.glow(x, y, 14, NIGHT_LIT, 0.5) for x, y in (_s36(4, 2, 5), _s36(30, -4, 7), _s36(20, 14, 4))]),
      daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=0.4)),
    E("bat", el(lambda g, m: [g.fill(Seg(x - 8, y - 2, x, y + 2, 2.2), C36.ink) for x, y in ((300, 60),)] + [g.fill(Seg(300, 62, 308, 58, 2.2), C36.ink)]),
      anim=dict(driftVelocity=(-30, 4), driftLength=500, driftStart=-400, stretch=(0, 0.6), scaleSpeed=3)),
]

L1536_DIFFS = [
    ("tower", *_s36(-3, -4, 13.5), 0),
    ("billboard", *_s36(10, -2.8, 10.2), 0),
    ("antenna", *_s36(25, -6, 15.5), 0),
    ("ac", *_s36(-5, 16.8, 6.6), 0),
    ("skylight", *_s36(13, 13.5, 8.8), 0),
    ("cape", _s36(19.6, 21.6, 8.6)[0] + 12, _s36(19.6, 21.6, 8.6)[1] - 22, 0),
    ("pigeons", *_s36(10.2, 22.2, 8.9), 0),
]


# =================================================================== Level 1537 comic roadside diner (desert)
I37 = iso_at(14, 10, 22.0)
C37 = Comic()


def l1537_scene(g, S, d):
    iso = I37
    decal(g, S, iso, [(-60, -60), (90, -60), (90, 90), (-60, 90)], (240, 186, 110), "sand", 3701)
    decal(g, S, iso, rect_ring(16, -60, 22, 90), (70, 70, 84), "road", 3702)
    for y in range(-30, 60, 4):
        decal(g, S, iso, rect_ring(18.9, y, 19.1, y + 2), (250, 210, 60), "plain", 3703)
    decal(g, S, iso, rect_ring(-4, 4, 16, 14), (110, 110, 122), "road", 3704)
    for x in range(-2, 15, 3):
        decal(g, S, iso, rect_ring(x, 9.8, x + 0.15, 13.6), (250, 250, 240), "plain", 3705)
    decal(g, S, iso, rect_ring(22, -6, 34, 8), (150, 146, 150), "road", 3706)
    sc = Scene()
    shadows = []
    # diner
    shadows.append((rect_ring(-4, -6, 10, 2.5), 3.4))
    def diner():
        box(g, S, iso, -4, -6, 0, 10, 2.5, 3.0, (236, 236, 240), "metal", 3710, top_col=(200, 200, 210))
        band = quad_on(iso, "y", -4, 10, 2.0, 2.6, 2.5)
        g.fill(band, (220, 50, 60))
        S.face(g, quad_on(iso, "x", -6, 2.5, 2.0, 2.6, 10), (220, 50, 60), 0.4, "plain", 3711)
        windows(g, S, iso, "y", 2.5, -3.6, 9.6, 0.6, 1.9, 5, glass=(120, 200, 230), seed=3712)
        S.face(g, quad_on(iso, "y", 3.4, 4.6, 0, 1.9, 2.5), (40, 120, 160), 0.8, "glass", 3713)
        box(g, S, iso, 0, -1, 3.0, 6, -0.6, 4.6, (220, 50, 60), "plain", 3714)
        for k in range(4):
            p = iso.p(0.8 + k * 1.4, -0.6, 3.8)
            g.fill(Circ(p[0], p[1], 5), (250, 230, 120))
            g.fill(Circ(p[0], p[1], 5) - Circ(p[0], p[1], 3.8), S.ink)
    sc.add(10, 2.5, diner)
    # pole sign (difference: star colour)
    shadows.append((rect_ring(13.6, 2.6, 14.0, 3.0), 9))
    def pole():
        cyl(g, S, iso, 13.8, 2.8, 0, 7.6, 0.18, (200, 200, 210), "metal", 3720, n=8)
        box(g, S, iso, 11.6, 2.6, 7.6, 16.0, 3.0, 11.0, (60, 140, 200), "plain", 3721)
        c_ = iso.p(13.8, 3.0, 9.3)
        sc_ = (250, 220, 60) if "star" not in d else (250, 120, 200)
        pts = [(c_[0] + (22 if i % 2 == 0 else 9) * math.cos(-math.pi / 2 + i * math.pi / 5), c_[1] + (22 if i % 2 == 0 else 9) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        g.fill(Poly(pts), S.ink)
        pts2 = [(c_[0] + (19 if i % 2 == 0 else 7.4) * math.cos(-math.pi / 2 + i * math.pi / 5), c_[1] + (19 if i % 2 == 0 else 7.4) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        g.fill(Poly(pts2), sc_)
    sc.add(15.4, 3.0, pole)
    # gas station canopy + pumps (difference: one pump colour) + kiosk
    shadows.append((rect_ring(23, -4, 33, 4), 4.4))
    def station():
        for (x, y) in ((24, -3), (32, -3), (24, 3), (32, 3)):
            box(g, S, iso, x - 0.2, y - 0.2, 0, x + 0.2, y + 0.2, 3.6, (240, 240, 240), "metal", 3730, w=0.8)
        for k, y in enumerate((-1.2, 1.4)):
            pc = (220, 50, 60) if not (k == 1 and "pump" in d) else (60, 120, 220)
            box(g, S, iso, 27.4, y - 0.4, 0, 28.4, y + 0.4, 1.8, pc, "plain", 3731 + k)
            p = iso.p(28.4, y, 1.4)
            g.fill(Circ(p[0], p[1], 3.4), (250, 250, 240))
        box(g, S, iso, 23, -4, 3.6, 33, 4, 4.3, (250, 250, 250), "plain", 3735)
        S.face(g, quad_on(iso, "y", 23, 33, 3.6, 4.3, 4), (220, 50, 60), 0.7, "plain", 3736)
        S.face(g, quad_on(iso, "x", -4, 4, 3.6, 4.3, 33), (220, 50, 60), 0.3, "plain", 3737)
    sc.add(33, 4, station)
    shadows.append((rect_ring(26, -12, 32, -7), 3))
    sc.add(32, -7, lambda: (box(g, S, iso, 26, -12, 0, 32, -7, 2.6, (240, 230, 200), "plain", 3738),
                            windows(g, S, iso, "y", -7, 26.4, 31.6, 0.5, 2.2, 2, glass=(120, 200, 230), seed=3739)))
    # cars (difference: the one on the road)
    for k, (x, y, ax, col) in enumerate(((1, 11.8, False, (240, 140, 170)), (7, 11.8, False, (60, 190, 180)),
                                         (11, 11.8, False, (250, 220, 90) if "car" not in d else (150, 90, 220)),
                                         (17.5, 20, False, (220, 50, 60)), (20.5, -6, False, (90, 120, 220)))):
        r_ = rect_ring(x - 0.85, y - 1.8, x + 0.85, y + 1.8)
        shadows.append((r_, 1.2))
        sc.add(x + 0.85, y + 1.8, lambda x=x, y=y, ax=ax, col=col, k=k: car(g, S, iso, x, y, col, ax, 3740 + k))
    # cacti (difference: one), rocks, water tower, motel row, oil drums (difference), dog (difference), umbrella table
    for k, (x, y, h) in enumerate(((-8, 18, 3.6), (4, 22, 3.0), (28, 16, 3.8), (36, 4, 3.2), (-10, -2, 3.4), (30, 28, 3.0))):
        if k == 5 and "cactus" in d:
            continue
        shadows.append((rect_ring(x - 0.4, y - 0.4, x + 0.4, y + 0.4), h))
        sc.add(x, y, lambda x=x, y=y, h=h, k=k: cactus(g, S, iso, x, y, h, 3750 + k))
    shadows.append((rect_ring(-12, -14, -8, -10), 6.5))
    sc.add(-9, -11, lambda: water_tower(g, S, iso, -10, -12, 0, (200, 200, 210), 3760, legs=3.2))
    shadows.append((rect_ring(-6, 18, 10, 22), 2.6))
    def motel():
        box(g, S, iso, -6, 18, 0, 10, 22, 2.4, (90, 190, 190), "plain", 3765, top_col=(220, 120, 80))
        for k in range(6):
            S.face(g, quad_on(iso, "y", -5 + k * 2.6, -4 + k * 2.6, 0, 1.8, 22), (250, 230, 120) if k % 2 else (230, 90, 70), 0.8, "plain", 3766 + k)
    sc.add(10, 22, motel)
    if "drums" not in d:
        for k, (x, y) in enumerate(((34, -9), (35, -8.2))):
            sc.add(x, y, lambda x=x, y=y, k=k: cyl(g, S, iso, x, y, 0, 1.3, 0.45, (60, 120, 200), "metal", 3770 + k))
    if "dog" not in d:
        sc.add(-2.4, 15.2, lambda: (box(g, S, iso, -3.6, 14.75, 0.35, -2.4, 15.25, 0.8, (180, 130, 80), "plain", 3775),
                                    box(g, S, iso, -2.6, 14.8, 0.6, -2.1, 15.2, 1.05, (180, 130, 80), "plain", 3776)))
    sc.add(-2, 3.8, lambda: (cyl(g, S, iso, -2, 3.6, 0, 0.75, 0.5, (240, 240, 240), "metal", 3778),
                             umbrella(g, S, iso, -2, 3.6, 2.2, 1.3, [(250, 210, 60), (230, 70, 70)], 3779)))
    for k, (x, y, col) in enumerate(((3, 3.8, (230, 90, 70)), (26, 0, (60, 120, 200)), (9, 6, (250, 220, 120)))):
        sc.add(x, y, lambda x=x, y=y, col=col, k=k: person(g, S, iso, x, y, col, 3785 + k))
    for k, (x, y, sx_, sy_) in enumerate(((38, -14, 3, 2), (-14, 28, 2.4, 2), (40, 26, 2, 1.6))):
        sc.add(x, y, lambda x=x, y=y, sx_=sx_, sy_=sy_, k=k: box(g, S, iso, x - sx_, y - sy_, 0, x + sx_, y + sy_, 2.2, (200, 110, 70), "plain", 3790 + k))
    for sh in shadows:
        shadow(g, S, iso, sh[0], 0, sh[1])
    sc.draw()


_s37 = sp_of(I37)


def l1537_weed(g, m):
    x, y = 120, 470
    g.fill(Circ(x, y, 13), C37.ink)
    g.fill(Circ(x, y, 10.5), (200, 160, 90))
    for k in range(5):
        a = k * 1.3
        g.fill(Seg(x + math.cos(a) * 9, y + math.sin(a) * 9, x - math.cos(a) * 9, y - math.sin(a) * 9, 1.4), C37.ink)


L1537_ELEMENTS = [
    E("weed", el(l1537_weed), pivot=(120, 470), anim=dict(driftVelocity=(50, 6), driftLength=500, driftStart=-200, rotateSpeed=200, bobAmplitude=(0, 4), bobSpeed=1.0)),
    E("vulture", el(lambda g, m: (g.fill(Seg(600, 60, 612, 66, 2.6), C37.ink), g.fill(Seg(612, 66, 624, 60, 2.6), C37.ink))),
      pivot=(612, 64), anim=dict(orbitRadius=(60, 20), orbitSpeed=0.08)),
    E("heat", el(lambda g, m: g.fill(Box(-2, 200, 902, 240), (255, 240, 200), alpha=0.1)), anim=dict(twinkle=0.8, twinkleSpeed=0.3)),
]

L1537_DIFFS = [
    ("star", *_s37(13.8, 3.0, 9.3), 0),
    ("pump", *_s37(27.9, 1.4, 1.0), 0),
    ("car", *_s37(11, 11.8, 0.8), 0),
    ("cactus", *_s37(30, 28, 1.6), 0),
    ("drums", *_s37(34.5, -8.6, 0.7), 0),
    ("dog", *_s37(-2.9, 15, 0.7), 0),
]


LEVELS = [
    ("Level1532", "湖畔小镇", make_bg(R32, l1532_scene), L1532_ELEMENTS, L1532_DIFFS, 60, OPTS_REAL),
    ("Level1533", "城市街角", make_bg(R33, l1533_scene), L1533_ELEMENTS, L1533_DIFFS, 60, OPTS_REAL),
    ("Level1534", "卡通农场", make_bg(T34, l1534_scene), L1534_ELEMENTS, L1534_DIFFS, 60, OPTS_TOON),
    ("Level1535", "卡通游乐园", make_bg(T35, l1535_scene), L1535_ELEMENTS, L1535_DIFFS, 60, OPTS_TOON),
    ("Level1536", "屋顶之夜", make_bg(C36, l1536_scene), L1536_ELEMENTS, L1536_DIFFS, 60, OPTS_COMIC),
    ("Level1537", "公路餐厅", make_bg(C37, l1537_scene), L1537_ELEMENTS, L1537_DIFFS, 60, OPTS_COMIC),
]
