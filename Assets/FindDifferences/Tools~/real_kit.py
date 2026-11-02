# -*- coding: utf-8 -*-
"""Realistic-style building blocks (on top of real.py): sky, clouds, mountains, forests, trees, rocks,
water, grass, timber / brick / stone surfaces, simple buildings and props, plus animated elements."""
import math
import random

import numpy as np

from fdcore import E, H, W
from kit import drift_across
from real import (F32, Box, C, Circ, Ctx, Ell, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm,
                  fbm1, grain_tex, hash2, hgrad, lgrad, light_x, light_y, mixc, rgrad, ridged1, smooth,
                  solid, sphere_paint, tex, vgrad)


# =================================================================== sky
def sky(g, stops, y1=H):
    g.fill(Box(-2, -2, W + 2, y1), vgrad(stops))


def sun(g, x, y, r=18, col=(255, 236, 200), halo=(255, 190, 120), k=1.0):
    g.glow(x, y, r * 16, halo, 0.35 * k, power=2.2)
    g.glow(x, y, r * 5, halo, 0.55 * k, power=1.6)
    g.fill(Circ(x, y, r), col, feather=1.5)
    g.glow(x, y, r * 1.6, (255, 255, 240), 0.8 * k, power=1.2)


def cloud_layer(g, y0, y1, col_lit, col_shade, cover=0.55, sx=160, sy=40, seed=1, alpha=0.9, x0=-2, x1=W + 2,
                light_dir=-1.0, soft=0.12):
    """Field of fbm clouds between y0 and y1 (lit on top / towards light_dir)."""
    r = g.win((x0, y0, x1, y1), pad=0)
    if r is None:
        return
    w, X, Y = r
    n = fbm(X, Y, sx, sy, 5, seed)
    t = np.clip((Y - y0) / max(1, y1 - y0), 0, 1)
    env = np.sin(t * math.pi) ** 0.7
    dens = smooth(1 - cover, 1 - cover + soft + 0.12, n * env + (1 - env) * 0.0)
    n2 = fbm(X, Y - 6, sx, sy, 5, seed)
    shade = np.clip((n2 - n) * 6 + 0.5, 0, 1)        # lower part of the puff darker
    col = C(col_lit) + (C(col_shade) - C(col_lit)) * shade[..., None]
    col = col * (1 + 0.06 * (fbm(X, Y, 14, 10, 2, seed + 3) - 0.5))[..., None]
    g._over(w, col, (dens * alpha).astype(F32))


def stars(g, n, y1, seed=3, bright=(255, 250, 235)):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, y1)
        b = rnd.random() ** 3
        g.glow(x, y, 1.2 + 2.8 * b, bright, 0.4 + 0.6 * b, power=1.5)


# =================================================================== terrain
def ridge(g, base, height, scale, seed, paint, x0=-20, x1=W + 20, ridged=True, octaves=5, snow=None, haze=None,
          rock_tex=0.16, feather=0.0, light=True):
    """Mountain range: y = base - height * noise(x). snow=(line_y, col), haze=(col, a_top, a_bottom)."""
    def f(x):
        n = ridged1(x, scale, octaves, seed) if ridged else fbm1(x, scale, octaves, seed)
        return base - height * n
    shape = Under(f, x0, x1, H + 20)
    p = tex(paint, rock_tex, 9, 5, 4, seed + 1)

    def shaded(X, Y):
        col = p(X, Y)
        if light:
            # broad slope light from the (low-frequency) ridge profile + 2-D bump-mapped rock relief
            xs = X[0]
            sl = (f(xs + 24) - f(xs - 24)) / 48.0
            hf = lambda dx, dy: fbm(X + dx, Y + dy, 34, 26, 6, seed + 7)
            bump = (hf(-2.5, -2.5) - hf(2.5, 2.5)) * 9.0
            gul = fbm(X, Y, 7, 34, 3, seed + 8) - 0.5
            k = np.clip(0.95 + sl[None, :] * 0.6 + bump * 0.9 + gul * 0.35, 0.45, 1.45)
            col = col * k[..., None]
        if snow is not None:
            line, scol = snow
            n3 = fbm(X, Y, 26, 10, 4, seed + 11)
            gs = fbm(X, Y, 5, 26, 3, seed + 12)
            s = smooth(line + 6, line - 6, Y + (n3 - 0.5) * 18 + (gs - 0.5) * 50)
            col = col + (C(scol) * (0.85 + 0.3 * (fbm(X, Y, 30, 12, 3, seed + 5) - 0.5))[..., None] - col) * s[..., None]
        if haze is not None:
            hc, a0, a1 = haze
            t = np.clip((Y - (base - height)) / max(1, height + 40), 0, 1)
            a = a0 + (a1 - a0) * t
            col = col + (C(hc) - col) * a[..., None]
        return col
    g.fill(shape, shaded, feather=feather)
    return f


def treeline(g, base, h, spacing, seed, col, x0=-20, x1=W + 20, jitter=0.5, haze=None, feather=0.0, light=0.25,
             conifer=True):
    """Distant forest edge made of many tree tops (conifer spikes or round crowns)."""
    rnd = random.Random(seed)
    xs, hs, ws = [], [], []
    x = x0
    while x < x1:
        xs.append(x)
        hs.append(h * (1 - jitter + jitter * 2 * rnd.random()))
        ws.append(spacing * (0.7 + 0.6 * rnd.random()))
        x += spacing * (0.5 + 0.7 * rnd.random())
    xs, hs, ws = np.array(xs, F32), np.array(hs, F32), np.array(ws, F32)

    def f(x):
        d = np.abs(x[:, None] - xs[None, :])
        if conifer:
            prof = hs[None, :] * (1 - d / (ws[None, :] * 0.55))
            prof = prof + (fbm1(x, 3.0, 2, seed)[:, None] - 0.5) * 6
        else:
            u = np.clip(1 - (d / (ws[None, :] * 0.6)) ** 2, 0, 1)
            prof = hs[None, :] * np.sqrt(u) + (fbm1(x, 6.0, 3, seed)[:, None] - 0.5) * 10 * (u > 0)
        return base - np.maximum(prof.max(1), 0) + (fbm1(x, 40, 2, seed + 1) - 0.5) * 6
    shape = Under(f, x0, x1, base + 60)
    c = C(col)

    def paint(X, Y):
        n = fbm(X, Y, 5 if conifer else 9, 9 if conifer else 7, 4, seed + 2)
        k = 1 + (n - 0.5) * 0.7 + light * (np.sin(X * 0.21 + n * 4) * 0.5)
        out = c * k[..., None]
        if haze is not None:
            hc, a0, a1 = haze
            t = np.clip((Y - (base - h)) / max(1, h + 40), 0, 1)
            a = a0 + (a1 - a0) * t
            out = out + (C(hc) - out) * a[..., None]
        return out
    g.fill(shape, paint, feather=feather)
    return f


def pine(g, x, base, h, col=(40, 70, 48), seed=0, w=None, light=(1.25, 0.6), snow=None, trunk=(70, 50, 36)):
    """Single conifer: jagged tiers, lit on the left."""
    w = w or h * 0.36
    rnd = random.Random(seed)
    g.fill(Seg(x, base, x, base - h * 0.3, max(2, w * 0.1), max(1.5, w * 0.06)), light_x(trunk, x - w * 0.05, x + w * 0.05))
    tiers = []
    n = max(4, int(h / 14))
    for i in range(n):
        t = i / (n - 1)
        y = base - h * 0.12 - (h * 0.88) * t
        hw = w * (1 - t) ** 0.95 * (0.85 + 0.3 * rnd.random()) + 1.5
        tiers.append(Poly([(x - hw, y + h * 0.02), (x + hw, y + h * 0.02 + rnd.uniform(-2, 2)),
                           (x + hw * 0.2, y - h * 0.13), (x, y - h * 0.18), (x - hw * 0.25, y - h * 0.12)]))
    shape = Rough(Union(tiers), max(1.0, w * 0.05), max(2.0, w * 0.08), seed + 3, 2)
    c = C(col)

    def paint(X, Y):
        t = np.clip((X - (x - w)) / (2 * w), 0, 1)
        k = light[0] + (light[1] - light[0]) * t
        n = fbm(X, Y, max(1.5, w * 0.12), max(1.5, w * 0.1), 3, seed + 5)
        out = c * (k * (0.75 + 0.5 * n))[..., None]
        if snow is not None:
            sn = smooth(0.62, 0.72, n + (1 - t) * 0.12)
            out = out + (C(snow) - out) * sn[..., None]
        return out
    g.fill(shape, paint)


def crown(g, cx, cy, rx, ry, col, seed=0, rough=None, light=(1.25, 0.55), clumps=None, edge=None):
    """Broad-leaf tree crown: rough blob, sphere-like lighting, leaf-clump texture."""
    rough = rough or max(3, rx * 0.16)
    shape = Rough(Ell(cx, cy, rx, ry), rough, max(4, rx * 0.22), seed, 3)
    c = C(col)
    cl = clumps or max(3, rx * 0.18)

    def paint(X, Y):
        nx, ny = (X - cx) / rx, (Y - cy) / ry
        d = np.clip(-0.55 * nx - 0.7 * ny + 0.35, -1, 1)
        k = light[1] + (light[0] - light[1]) * (d * 0.5 + 0.5)
        n = fbm(X, Y, cl, cl, 4, seed + 1)
        n2 = fbm(X, Y, cl * 0.35, cl * 0.35, 2, seed + 2)
        k = k * (0.62 + 0.62 * n + 0.18 * (n2 - 0.5))
        return c * k[..., None]
    g.fill(shape, paint)
    return shape


def trunk(g, x0, y0, x1, y1, w0, w1, col=(86, 66, 50), seed=0):
    s = Seg(x0, y0, x1, y1, w0, w1)
    g.fill(s, tex(light_x(col, min(x0, x1) - w0 / 2, max(x0, x1) + w0 / 2, 1.2, 0.55), 0.18, 1.5, 9, 3, seed))


def broadleaf(g, x, base, h, col=(70, 110, 50), seed=0, trunk_col=(86, 66, 50), lean=0.0):
    rnd = random.Random(seed)
    trunk(g, x, base, x + lean * h, base - h * 0.55, h * 0.09, h * 0.05, trunk_col, seed)
    trunk(g, x + lean * h * 0.6, base - h * 0.42, x + lean * h - h * 0.16, base - h * 0.7, h * 0.04, h * 0.025, trunk_col, seed + 1)
    trunk(g, x + lean * h * 0.6, base - h * 0.45, x + lean * h + h * 0.18, base - h * 0.72, h * 0.04, h * 0.025, trunk_col, seed + 2)
    cx, cy = x + lean * h, base - h * 0.7
    crown(g, cx, cy, h * 0.36, h * 0.3, col, seed + 3)
    for i in range(3):
        a = rnd.uniform(0, math.tau)
        crown(g, cx + math.cos(a) * h * 0.18, cy + math.sin(a) * h * 0.12 - h * 0.04, h * 0.2, h * 0.17,
              mixc(col, (255, 240, 180), 0.08), seed + 10 + i)


def rock(g, cx, cy, rx, ry, col=(120, 116, 108), seed=0, moss=None, shadow=True, wet=False):
    shape = Rough(Ell(cx, cy, rx, ry), max(2, rx * 0.12), max(4, rx * 0.35), seed, 3)
    if shadow:
        g.mul(Ell(cx + rx * 0.25, cy + ry * 0.75, rx * 1.15, ry * 0.35), 0.45, feather=max(4, ry * 0.4))
    sp = sphere_paint(cx, cy, rx * 1.05, col, ry=ry * 1.1, amb=0.35, spec=0.12 if not wet else 0.4, shin=12, wrap=0.4)
    t = tex(sp, 0.22, max(3, rx * 0.18), max(3, ry * 0.2), 4, seed + 2)
    p = grain_tex(t, 0.08, seed)
    if moss:
        mc = C(moss)

        def p2(X, Y, p=p):
            out = p(X, Y)
            m = smooth(0.52, 0.66, fbm(X, Y, max(4, rx * 0.25), max(3, ry * 0.25), 3, seed + 9) + (cy - Y) / (ry * 3))
            return out + (mc * (out.mean(-1, keepdims=True) / 140.0) - out) * m[..., None]
        g.fill(shape, p2)
    else:
        g.fill(shape, p)
    return shape


# =================================================================== ground / water
def grass_field(g, y0, y1, near, far, seed=0, x0=-2, x1=W + 2, blades=True, dry=None):
    g.fill(Box(x0, y0, x1, y1 + 2), vgrad([(y0, far), (y1, near)]))
    r = g.win((x0, y0, x1, y1), pad=0)
    if r is None:
        return
    w, X, Y = r
    t = np.clip((Y - y0) / max(1, y1 - y0), 0, 1)
    sc = 1 + t * 5
    n = fbm(X, Y, 2.0 * sc, 7 * sc, 4, seed)
    n2 = fbm(X, Y, 60, 30, 3, seed + 1)
    k = (0.78 + 0.45 * n) * (0.88 + 0.24 * n2)
    sub = g.img[w[0]:w[1], w[2]:w[3]]
    sub *= k[..., None]
    if dry is not None:
        m = smooth(0.55, 0.75, fbm(X, Y, 80, 40, 3, seed + 4))
        sub += (C(dry) * k[..., None] - sub) * (m * 0.6)[..., None]


def blades(g, y0, y1, col, n=300, seed=0, x0=0, x1=W, hmin=8, hmax=26, lean=4):
    """Foreground grass blades (thin tapered strokes)."""
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        y = rnd.uniform(y0, y1)
        hh = rnd.uniform(hmin, hmax) * (0.6 + 0.6 * (y - y0) / max(1, y1 - y0))
        k = rnd.uniform(0.7, 1.3)
        cc = tuple(min(255, v * k) for v in col)
        g.fill(Seg(x, y, x + rnd.uniform(-lean, lean), y - hh, rnd.uniform(1.2, 2.4), 0.3), cc)


def water(g, y0, y1, top, bottom, seed=0, x0=-2, x1=W + 2, streak=0.12):
    g.fill(Box(x0, y0, x1, y1), vgrad([(y0, top), (y1, bottom)]))
    r = g.win((x0, y0, x1, y1), pad=0)
    if r is None:
        return
    w, X, Y = r
    t = np.clip((Y - y0) / max(1, y1 - y0), 0, 1)
    n = fbm(X, Y, 30 + 120 * t, 1.2 + 6 * t, 4, seed)
    g.img[w[0]:w[1], w[2]:w[3]] *= (1 + streak * (n - 0.5) * 2)[..., None]


def ripples_light(g, y0, y1, col, k=0.5, x0=0, x1=W, seed=5, cx=None, spread=120):
    """Glints on water (sun path when cx given)."""
    r = g.win((x0, y0, x1, y1), pad=0)
    if r is None:
        return
    (j0, j1, i0, i1), X, Y = r
    t = np.clip((Y - y0) / max(1, y1 - y0), 0, 1)
    n = fbm(X, Y, 14 + 50 * t, 1 + 3 * t, 3, seed)
    m = smooth(0.62, 0.8, n)
    if cx is not None:
        m = m * np.exp(-((X - cx) / (spread * (0.5 + t))) ** 2)
    g.img[j0:j1, i0:i1] += C(col) * (m * k)[..., None]


# =================================================================== surfaces
def planks(direction, base, seed=0, width=14, gap_col=(40, 30, 24), grain=0.18, x_or_y0=0, vary=0.12):
    """Wood planks paint: direction 'h' (boards run horizontally) or 'v'."""
    base = C(base)
    rnd = np.random.default_rng(seed)
    tints = (1 + (rnd.random(512) - 0.5) * 2 * vary).astype(F32)

    def f(X, Y):
        u = (Y if direction == "h" else X) - x_or_y0
        v = X if direction == "h" else Y
        idx = np.floor(u / width).astype(np.int64)
        fu = u / width - idx
        k = tints[idx % 512]
        gr = fbm(v + idx[...] * 37.0, u * 1.0, 40, 1.6, 4, seed + 1) if direction == "h" else fbm(u * 1.0, v + idx * 37.0, 1.6, 40, 4, seed + 1)
        col = base * (k * (1 + grain * (gr - 0.5) * 2))[..., None]
        edge = smooth(0.0, 0.08, fu) * smooth(1.0, 0.92, fu)
        col = col * (0.55 + 0.45 * edge)[..., None]
        return col
    return f


def bricks(base, mortar=(170, 160, 150), bw=26, bh=10, seed=0, vary=0.14, ox=0, oy=0):
    base, mortar = C(base), C(mortar)
    rnd = np.random.default_rng(seed)
    tints = (1 + (rnd.random((64, 64)) - 0.5) * 2 * vary).astype(F32)

    def f(X, Y):
        row = np.floor((Y - oy) / bh).astype(np.int64)
        xx = X - ox + (row % 2) * bw * 0.5
        col_i = np.floor(xx / bw).astype(np.int64)
        fx, fy = xx / bw - col_i, (Y - oy) / bh - row
        k = tints[row % 64, col_i % 64]
        n = fbm(X, Y, 3, 3, 3, seed + 2)
        out = base * (k * (0.85 + 0.3 * n))[..., None]
        m = (smooth(0.0, 0.06, fx) * smooth(1.0, 0.94, fx) * smooth(0.0, 0.12, fy) * smooth(1.0, 0.88, fy))
        return mortar * (0.9 + 0.2 * n)[..., None] + (out - mortar) * m[..., None]
    return f


def stone_wall(base, seed=0, sx=22, sy=14):
    """Irregular fieldstone: voronoi-ish cells via noise thresholds."""
    base = C(base)

    def f(X, Y):
        n = fbm(X, Y, sx, sy, 2, seed)
        n2 = fbm(X, Y, sx * 0.5, sy * 0.5, 3, seed + 1)
        cell = np.abs(np.sin(n * 18.0))
        k = 0.75 + 0.35 * n2
        joint = smooth(0.05, 0.22, cell)
        return base * (k * (0.45 + 0.55 * joint))[..., None]
    return f


def rock_face(base, seed=0, sx=70, sy=26, strata=0.16, bump=3.0):
    """Cliff / rock surface: bump-mapped relief, sedimentary banding and dark cracks."""
    base = C(base)

    def f(X, Y):
        hf = lambda dx, dy: fbm(X + dx, Y + dy, sx, sy, 6, seed)
        b = (hf(-2, -2) - hf(2, 2)) * bump
        st = 1 + strata * np.sin(Y * 0.22 + fbm(X, Y, 70, 24, 3, seed + 1) * 9)
        cr = smooth(0.3, 0.18, fbm(X, Y, 3, 40, 3, seed + 2)) * smooth(0.45, 0.6, fbm(X, Y, 50, 50, 2, seed + 4))
        k = np.clip(st * (0.9 + 0.3 * (fbm(X, Y, 12, 7, 4, seed + 3) - 0.5)) + b, 0.55, 1.35) * (1 - 0.4 * cr)
        return base * k[..., None]
    return f


def window_glass(g, x0, y0, x1, y1, sky_top=(170, 200, 225), sky_bot=(90, 110, 130), lit=None, frame=(235, 232, 225),
                 bars=True, fw=2.2):
    """Window with reflected sky gradient (or warm interior light when lit), frame and muntins."""
    g.fill(Box(x0 - fw, y0 - fw, x1 + fw, y1 + fw), light_y(frame, y0, y1, 1.05, 0.85))
    if lit:
        g.fill(Box(x0, y0, x1, y1), rgrad((x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) * 0.8,
                                         [(0, lit), (1, mixc(lit, (60, 30, 10), 0.5))]))
    else:
        g.fill(Box(x0, y0, x1, y1), lgrad(x0, y0, x1, y1, [(0, sky_top), (1, sky_bot)]))
        g.add(Poly([(x0 + (x1 - x0) * 0.15, y1), (x0 + (x1 - x0) * 0.45, y1), (x0 + (x1 - x0) * 0.85, y0),
                    (x0 + (x1 - x0) * 0.55, y0)]), (255, 255, 255), 0.12)
    if bars:
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        g.fill(Box(mx - fw * 0.5, y0, mx + fw * 0.5, y1), frame)
        g.fill(Box(x0, my - fw * 0.5, x1, my + fw * 0.5), frame)
    g.mul(Box(x0, y0, x1, y0 + 2.5), 0.4, feather=2)


def gable_house(g, x0, base, w, wall_h, roof_h, wall, roof, seed=0, side=None, side_w=0.0, roof_paint=None,
                wall_paint=None):
    """Front-facing gable house (lit from the left), returns key coordinates."""
    x1 = x0 + w
    g.mul(Box(x0 + 6, base - 4, x1 + 26, base + 8), 0.45, feather=8)
    wp = wall_paint or tex(light_x(wall, x0, x1, 1.08, 0.86), 0.06, 5, 5, 3, seed)
    g.fill(Box(x0, base - wall_h, x1, base), wp)
    if side is not None:
        g.fill(Poly([(x1, base - wall_h), (x1 + side_w, base - wall_h - side_w * 0.35), (x1 + side_w, base - side_w * 0.35 + 4),
                     (x1, base)]), tex(light_x(side, x1, x1 + side_w, 0.8, 0.62), 0.06, 5, 5, 3, seed + 1))
    rp = roof_paint or tex(light_y(roof, base - wall_h - roof_h, base - wall_h, 1.15, 0.8), 0.14, 6, 2.5, 3, seed + 2)
    g.fill(Poly([(x0 - 8, base - wall_h + 2), ((x0 + x1) / 2, base - wall_h - roof_h), (x1 + 8, base - wall_h + 2)]), rp)
    g.mul(Box(x0, base - wall_h + 2, x1, base - wall_h + 10), 0.35, feather=6)
    return dict(x0=x0, x1=x1, top=base - wall_h, base=base)


# =================================================================== animated elements
def cumulus(g, x, y, rx, ry, col=(250, 248, 245), shade=(200, 205, 215), alpha=0.95, seed=1):
    """Puffy cloud: noise-eroded ellipse, lit top, grey flat base."""
    r = g.win((x - rx, y - ry, x + rx, y + ry), pad=0)
    if r is None:
        return
    w, X, Y = r
    d = np.clip(1 - ((X - x) / rx) ** 2 - ((Y - y) / ry) ** 2 * 1.4, 0, 1)
    d = d * smooth(y + ry * 0.55, y + ry * 0.25, Y)          # flatter base
    n = fbm(X, Y, rx * 0.35, ry * 0.45, 5, seed)
    dens = smooth(0.35, 0.6, n * 0.7 + d * 0.7 - 0.2) * d ** 0.3
    n2 = fbm(X, Y - ry * 0.18, rx * 0.35, ry * 0.45, 5, seed)
    sh = np.clip((n2 - n) * 5 + (Y - y) / ry * 0.7 + 0.3, 0, 1)
    colr = C(col) + (C(shade) - C(col)) * sh[..., None]
    g._over(w, colr, (dens * alpha).astype(F32))


def cloud_el(eid, x, y, rx, ry, col=(250, 248, 245), shade=(200, 205, 215), speed=6.0, alpha=0.9,
             seed=1, daynight="tinted", phase=0.0):
    a = drift_across(x - rx, x + rx, speed, start=phase)
    return E(eid, el(lambda g, m: cumulus(g, x, y, rx, ry, col, shade, alpha, seed)), daynight=daynight, pivot=(x, y), anim=a)


def figure(g, x, base, h, coat, pants=(50, 52, 60), skin=(214, 170, 140), hair=(60, 44, 34), face_right=True,
           hat=None, sitting=False):
    """Small human figure (seen from a distance), softly lit from the left."""
    k = h / 60.0
    g.mul(Ell(x + 6 * k, base, 13 * k, 3 * k), 0.4, feather=3 * k)
    if not sitting:
        for dx in (-4, 4):
            g.fill(Seg(x + dx * k, base - 2 * k, x + dx * 0.7 * k, base - 26 * k, 6 * k, 7 * k), light_x(pants, x - 8 * k, x + 8 * k))
            g.fill(Ell(x + dx * k + 2 * k, base - 1.5 * k, 4.5 * k, 2.2 * k), (40, 36, 34))
    top = base - (26 if not sitting else 14) * k
    g.fill(Box(x - 9 * k, top - 22 * k, x + 9 * k, top + 2 * k, 5 * k), tex(light_x(coat, x - 9 * k, x + 9 * k, 1.2, 0.7), 0.08, 3, 3))
    for dx in (-10, 10):
        g.fill(Seg(x + dx * k, top - 19 * k, x + dx * 1.15 * k, top - 3 * k, 5 * k, 4.4 * k), light_x(coat, x - 12 * k, x + 12 * k, 1.15, 0.65))
    g.fill(Box(x - 2.5 * k, top - 26 * k, x + 2.5 * k, top - 20 * k), skin)
    g.fill(Ell(x, top - 31 * k, 6 * k, 7 * k), sphere_paint(x, top - 31 * k, 6 * k, skin, ry=7 * k, amb=0.5, spec=0.08))
    hx = -1.5 if face_right else 1.5
    g.fill(Ell(x + hx * k, top - 35 * k, 6.3 * k, 4.5 * k), hair)
    if hat is not None:
        g.fill(Ell(x, top - 36 * k, 9 * k, 2.2 * k), hat)
        g.fill(Box(x - 5.5 * k, top - 43 * k, x + 5.5 * k, top - 36 * k, 2 * k), hat)


def mist_el(eid, x, y, rx, ry, col=(235, 236, 240), alpha=0.5, speed=4.0, length=120, seed=4, daynight="tinted"):
    """Soft fog strip that slides back and forth (bob) - stays in its band."""
    def draw(g, m):
        r = g.win((x - rx, y - ry, x + rx, y + ry), pad=0)
        if r is None:
            return
        w, X, Y = r
        d = np.clip(1 - ((X - x) / rx) ** 2, 0, 1) * np.clip(1 - ((Y - y) / ry) ** 2, 0, 1)
        n = fbm(X, Y, rx * 0.25, ry * 0.6, 4, seed)
        g._over(w, np.broadcast_to(C(col), X.shape + (3,)), (d ** 1.2 * (0.4 + 0.9 * n) * alpha).astype(F32))
    return E(eid, el(draw), daynight=daynight, anim=dict(bobAmplitude=(length / 2, 0), bobSpeed=speed / max(1, length * 2)))


def bird_el(eid, x, y, s=6, col=(40, 40, 46), speed=-30, daynight="tinted", phase=0.0, flap=True):
    def draw(g, m):
        g.fill(Seg(x - s, y - s * 0.3, x, y + s * 0.15, s * 0.28, s * 0.18), col)
        g.fill(Seg(x, y + s * 0.15, x + s, y - s * 0.35, s * 0.18, s * 0.28), col)
        g.fill(Ell(x, y + s * 0.12, s * 0.26, s * 0.16), col)
    a = dict(drift_across(x - s, x + s, speed, start=phase), bobAmplitude=(0, 5), bobSpeed=0.2)
    if flap:
        a.update(stretch=(0, 0.5), scaleSpeed=2.2)
    return E(eid, el(draw), daynight=daynight, pivot=(x, y), anim=a)


def smoke_el(eid, x, y, r=7, col=(200, 200, 205), alpha=0.55, rise=60, wind=12, daynight="tinted", phase=0.0, seed=8):
    def draw(g, m):
        rr = g.win((x - r * 1.6, y - r * 1.6, x + r * 1.6, y + r * 1.6), pad=0)
        if rr is None:
            return
        w, X, Y = rr
        d = np.clip(1 - np.hypot(X - x, Y - y) / (r * 1.5), 0, 1)
        n = fbm(X, Y, r * 0.6, r * 0.6, 3, seed)
        g._over(w, np.broadcast_to(C(col), X.shape + (3,)), (smooth(0, 0.6, d) * (0.5 + 0.7 * n) * alpha).astype(F32))
    return E(eid, el(draw), daynight=daynight,
             anim=dict(driftVelocity=(wind, rise), driftLength=rise, driftFade=True, driftGrow=1.6, phase=phase))


def glint_el(eid, pts, col=(255, 250, 230), r=5, daynight="untinted", speed=0.8, phase=0.0):
    """Twinkling highlights (sun glints on water, stars, dew)."""
    def draw(g, m):
        for x, y in pts:
            g.glow(x, y, r, col, 1.0, power=1.4)
            g.add(Seg(x - r * 1.4, y, x + r * 1.4, y, 0.9), col, 0.7)
    return E(eid, el(draw), daynight=daynight, anim=dict(twinkle=0.85, twinkleSpeed=speed, phase=phase))


def fall_el(eid, x, y, draw_one, vx=10, vy=-60, length=300, phase=0.0, swing=0, daynight="tinted"):
    """Something falling (leaf / snowflake / petal) along a straight drift path (anim units: y up)."""
    a = dict(driftVelocity=(vx, vy), driftLength=length, driftFade=True, phase=phase)
    if swing:
        a.update(swingAngle=swing, swingSpeed=0.7)
    return E(eid, el(lambda g, m: draw_one(g, x, y)), daynight=daynight, anim=a)
