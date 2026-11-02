# -*- coding: utf-8 -*-
"""Realistic (painterly-photographic) renderer for the find-the-difference generator.

Unlike the paper-craft kit (white cut edges, flat pieces), this module paints with numpy on the
supersampled fdcore.Canvas:
  * shapes are signed-distance fields -> anti-aliased, optionally feathered (soft focus / depth of field)
  * paints are per-pixel fields: multi-stop gradients, coordinate-based fbm noise textures, sphere /
    cylinder lighting, so surfaces carry texture and soft light instead of flat colour
  * effects: soft multiplied shadows, additive glows, fog bands, water reflections with ripples,
    gaussian blur of a region, bloom of bright pixels, colour grading
  * real_post: film grain (hashed by scene coordinate, so A/B and sprites match) + lens vignette

Noise is a pure function of scene coordinates, so the same drawing renders identically on the full
background canvas, on a measuring canvas and on an element's bbox canvas.

Usage inside a level:
    def bg(c, d):
        g = Ctx(c)
        g.fill(Box(0, 0, W, H), vgrad([(0, SKY_TOP), (300, SKY_LOW)]))
        ...
        g.commit()
"""
import math
from collections import OrderedDict

import numpy as np

from fdcore import H, W

F32 = np.float32


# =================================================================== noise
_TABLES = {}


def _table(seed):
    t = _TABLES.get(seed)
    if t is None:
        t = np.random.default_rng(seed + 9173).random((256, 256)).astype(F32)
        _TABLES[seed] = t
    return t


def vnoise(x, y, seed=0):
    """Smooth value noise in [0, 1] on the integer lattice (x, y arrays of any matching shape)."""
    t = _table(seed)
    xf, yf = np.floor(x), np.floor(y)
    fx, fy = (x - xf).astype(F32), (y - yf).astype(F32)
    ix, iy = xf.astype(np.int64) & 255, yf.astype(np.int64) & 255
    ix1, iy1 = (ix + 1) & 255, (iy + 1) & 255
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = t[iy, ix] + (t[iy, ix1] - t[iy, ix]) * ux
    b = t[iy1, ix] + (t[iy1, ix1] - t[iy1, ix]) * ux
    return a + (b - a) * uy


_CACHE = OrderedDict()


def fbm(X, Y, sx, sy=None, octaves=4, seed=0, gain=0.5, lac=2.03, key=None):
    """Fractal noise in ~[0, 1]; feature size sx (horizontal) / sy (vertical) scene px."""
    sy = sx if sy is None else sy
    ck = None
    if key is not None:
        ck = (key, X.shape, float(X[0, 0]), float(Y[0, 0]), sx, sy, octaves, seed, gain)
        v = _CACHE.get(ck)
        if v is not None:
            _CACHE.move_to_end(ck)
            return v
    tot = np.zeros(X.shape, F32)
    amp, norm, f = 1.0, 0.0, 1.0
    for o in range(octaves):
        tot += amp * vnoise(X * (f / sx) + o * 17.3, Y * (f / sy) + o * 31.7, seed + o)
        norm += amp
        amp *= gain
        f *= lac
    tot /= norm
    if ck is not None:
        _CACHE[ck] = tot
        if len(_CACHE) > 48:
            _CACHE.popitem(last=False)
    return tot


def fbm1(x, scale, octaves=4, seed=0, gain=0.5):
    """1-D fractal noise along x (array) -> ~[0, 1]."""
    x = np.asarray(x, F32)
    return fbm(x[None, :], np.full((1, x.shape[0]), 0.5 + seed * 3.1, F32), scale, 1.0, octaves, seed, gain)[0]


def ridged1(x, scale, octaves=5, seed=0):
    """Sharp mountain-ridge noise (1-D) in ~[0, 1]."""
    x = np.asarray(x, F32)
    tot = np.zeros(x.shape, F32)
    amp, norm, f = 1.0, 0.0, 1.0
    for o in range(octaves):
        n = vnoise(x * (f / scale) + o * 7.1, np.full(x.shape, 3.3 + o * 5.0 + seed, F32), seed + 40 + o)
        tot += amp * (1 - np.abs(2 * n - 1)) ** 2
        norm += amp
        amp *= 0.5
        f *= 2.1
    return tot / norm


def hash2(X, Y, seed=0):
    """Per-pixel white noise in [0, 1) from integer-ish coordinates."""
    xi = np.floor(X * 2).astype(np.int64)
    yi = np.floor(Y * 2).astype(np.int64)
    h = (xi * 374761393 + yi * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF).astype(F32) / 65536.0


# =================================================================== colour helpers
def C(col):
    return np.array(col[:3], F32)


def mixc(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# =================================================================== shapes (signed distance, scene px)
class Shape:
    pad = 0.0

    def bbox(self):
        raise NotImplementedError

    def sdf(self, X, Y):
        raise NotImplementedError

    def __or__(self, o):
        return Union([self, o])

    def __sub__(self, o):
        return Diff(self, o)

    def __and__(self, o):
        return Inter(self, o)


class Box(Shape):
    def __init__(self, x0, y0, x1, y1, r=0.0):
        self.x0, self.y0, self.x1, self.y1, self.r = min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), r

    def bbox(self):
        return (self.x0, self.y0, self.x1, self.y1)

    def sdf(self, X, Y):
        cx, cy = (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2
        hx, hy = (self.x1 - self.x0) / 2 - self.r, (self.y1 - self.y0) / 2 - self.r
        qx, qy = np.abs(X - cx) - hx, np.abs(Y - cy) - hy
        out = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
        return out + np.minimum(np.maximum(qx, qy), 0) - self.r


class Ell(Shape):
    def __init__(self, cx, cy, rx, ry=None):
        self.cx, self.cy, self.rx, self.ry = cx, cy, rx, (rx if ry is None else ry)

    def bbox(self):
        return (self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry)

    def sdf(self, X, Y):
        px, py = X - self.cx, Y - self.cy
        k0 = np.hypot(px / self.rx, py / self.ry)
        k1 = np.hypot(px / (self.rx * self.rx), py / (self.ry * self.ry))
        return np.where(k1 > 1e-9, k0 * (k0 - 1) / np.maximum(k1, 1e-9), -min(self.rx, self.ry))


class Poly(Shape):
    def __init__(self, pts):
        self.p = np.array(pts, F32)

    def bbox(self):
        return (self.p[:, 0].min(), self.p[:, 1].min(), self.p[:, 0].max(), self.p[:, 1].max())

    def sdf(self, X, Y):
        p = self.p
        n = len(p)
        d = (X - p[0, 0]) ** 2 + (Y - p[0, 1]) ** 2
        s = np.ones(X.shape, F32)
        j = n - 1
        for i in range(n):
            ex, ey = p[j, 0] - p[i, 0], p[j, 1] - p[i, 1]
            wx, wy = X - p[i, 0], Y - p[i, 1]
            ee = ex * ex + ey * ey
            t = np.clip((wx * ex + wy * ey) / (ee if ee > 0 else 1), 0, 1)
            bx, by = wx - ex * t, wy - ey * t
            d = np.minimum(d, bx * bx + by * by)
            c1 = Y >= p[i, 1]
            c2 = Y < p[j, 1]
            c3 = ex * wy > ey * wx
            flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
            s = np.where(flip, -s, s)
            j = i
        return s * np.sqrt(d)


class Seg(Shape):
    """Tapered capsule from (x0, y0) width w0 to (x1, y1) width w1 (full widths)."""

    def __init__(self, x0, y0, x1, y1, w0, w1=None):
        self.a, self.b = (x0, y0), (x1, y1)
        self.r0, self.r1 = w0 / 2, (w0 if w1 is None else w1) / 2

    def bbox(self):
        r = max(self.r0, self.r1)
        return (min(self.a[0], self.b[0]) - r, min(self.a[1], self.b[1]) - r,
                max(self.a[0], self.b[0]) + r, max(self.a[1], self.b[1]) + r)

    def sdf(self, X, Y):
        ax, ay = self.a
        ex, ey = self.b[0] - ax, self.b[1] - ay
        ee = ex * ex + ey * ey or 1.0
        t = np.clip(((X - ax) * ex + (Y - ay) * ey) / ee, 0, 1)
        return np.hypot(X - ax - ex * t, Y - ay - ey * t) - (self.r0 + (self.r1 - self.r0) * t)


class Under(Shape):
    """Everything below the curve y = f(x) (f takes a 1-D x array), within x0..x1 and down to y1."""

    def __init__(self, f, x0=-20, x1=W + 20, y1=H + 20, top=None):
        self.f, self.x0, self.x1, self.y1 = f, x0, x1, y1
        xs = np.linspace(x0, x1, 600)
        self.top = float(np.min(f(xs))) - 2 if top is None else top

    def bbox(self):
        return (self.x0, self.top, self.x1, self.y1)

    def sdf(self, X, Y):
        fy = self.f(X[0])[None, :]
        return np.maximum(fy - Y, np.maximum(self.x0 - X, X - self.x1))


class Union(Shape):
    def __init__(self, shapes):
        self.s = list(shapes)

    def bbox(self):
        bs = [s.bbox() for s in self.s]
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))

    def sdf(self, X, Y):
        d = self.s[0].sdf(X, Y)
        for s in self.s[1:]:
            b = s.bbox()
            if b[2] < X[0, 0] - 4 or b[0] > X[0, -1] + 4 or b[3] < Y[0, 0] - 4 or b[1] > Y[-1, 0] + 4:
                continue
            d = np.minimum(d, s.sdf(X, Y))
        return d


class Diff(Shape):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def bbox(self):
        return self.a.bbox()

    def sdf(self, X, Y):
        return np.maximum(self.a.sdf(X, Y), -self.b.sdf(X, Y))


class Inter(Shape):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def bbox(self):
        p, q = self.a.bbox(), self.b.bbox()
        return (max(p[0], q[0]), max(p[1], q[1]), min(p[2], q[2]), min(p[3], q[3]))

    def sdf(self, X, Y):
        return np.maximum(self.a.sdf(X, Y), self.b.sdf(X, Y))


class Rough(Shape):
    """Perturb the outline of a shape with noise (foliage, rocks, snow drifts)."""

    def __init__(self, s, amp, scale, seed=0, octaves=3):
        self.s, self.amp, self.scale, self.seed, self.oct = s, amp, scale, seed, octaves

    def bbox(self):
        b = self.s.bbox()
        return (b[0] - self.amp, b[1] - self.amp, b[2] + self.amp, b[3] + self.amp)

    def sdf(self, X, Y):
        return self.s.sdf(X, Y) + (fbm(X, Y, self.scale, octaves=self.oct, seed=self.seed) - 0.5) * 2 * self.amp


class Moved(Shape):
    def __init__(self, s, dx, dy):
        self.s, self.dx, self.dy = s, dx, dy

    def bbox(self):
        b = self.s.bbox()
        return (b[0] + self.dx, b[1] + self.dy, b[2] + self.dx, b[3] + self.dy)

    def sdf(self, X, Y):
        return self.s.sdf(X - self.dx, Y - self.dy)


def Circ(cx, cy, r):
    return Ell(cx, cy, r, r)


# =================================================================== paints (callables (X, Y) -> rgb array)
def vgrad(stops):
    """Vertical multi-stop gradient: stops = [(y, rgb), ...]."""
    ys = np.array([s[0] for s in stops], F32)
    cs = np.array([s[1][:3] for s in stops], F32)

    def f(X, Y):
        yy = Y[:, 0]
        out = np.stack([np.interp(yy, ys, cs[:, i]) for i in range(3)], -1).astype(F32)
        return np.broadcast_to(out[:, None, :], X.shape + (3,)).copy()
    return f


def hgrad(stops):
    xs = np.array([s[0] for s in stops], F32)
    cs = np.array([s[1][:3] for s in stops], F32)

    def f(X, Y):
        xx = X[0]
        out = np.stack([np.interp(xx, xs, cs[:, i]) for i in range(3)], -1).astype(F32)
        return np.broadcast_to(out[None, :, :], X.shape + (3,)).copy()
    return f


def lgrad(x0, y0, x1, y1, stops):
    """Linear gradient along (x0,y0)->(x1,y1); stops = [(t, rgb), ...]."""
    ts = np.array([s[0] for s in stops], F32)
    cs = np.array([s[1][:3] for s in stops], F32)
    dx, dy = x1 - x0, y1 - y0
    dd = dx * dx + dy * dy or 1.0

    def f(X, Y):
        t = np.clip(((X - x0) * dx + (Y - y0) * dy) / dd, 0, 1)
        return np.stack([np.interp(t, ts, cs[:, i]) for i in range(3)], -1).astype(F32)
    return f


def rgrad(cx, cy, r, stops, ry=None):
    ts = np.array([s[0] for s in stops], F32)
    cs = np.array([s[1][:3] for s in stops], F32)
    ry = r if ry is None else ry

    def f(X, Y):
        t = np.clip(np.hypot((X - cx) / r, (Y - cy) / ry), 0, 1)
        return np.stack([np.interp(t, ts, cs[:, i]) for i in range(3)], -1).astype(F32)
    return f


def solid(col):
    c = C(col)
    return lambda X, Y: np.broadcast_to(c, X.shape + (3,)).copy()


def _as_paint(p):
    return p if callable(p) else solid(p)


def tex(paint, amp=0.12, sx=6, sy=None, octaves=3, seed=0):
    """Multiply a paint by (1 + amp * noise) - surface texture."""
    p = _as_paint(paint)

    def f(X, Y):
        n = fbm(X, Y, sx, sy, octaves, seed) - 0.5
        return p(X, Y) * (1 + 2 * amp * n)[..., None]
    return f


def grain_tex(paint, amp=0.06, seed=0):
    """Fine per-pixel speckle (stone, sand, asphalt)."""
    p = _as_paint(paint)

    def f(X, Y):
        return p(X, Y) * (1 + amp * (hash2(X, Y, seed) - 0.5) * 2)[..., None]
    return f


def light_x(paint, x0, x1, k0=1.15, k1=0.75, gamma=1.0):
    """Horizontal light falloff across an object (lit side x0 -> shadow side x1)."""
    p = _as_paint(paint)

    def f(X, Y):
        t = np.clip((X - x0) / (x1 - x0), 0, 1) ** gamma
        return p(X, Y) * (k0 + (k1 - k0) * t)[..., None]
    return f


def light_y(paint, y0, y1, k0=1.1, k1=0.8):
    p = _as_paint(paint)

    def f(X, Y):
        t = np.clip((Y - y0) / (y1 - y0), 0, 1)
        return p(X, Y) * (k0 + (k1 - k0) * t)[..., None]
    return f


LIGHT = np.array([-0.5, -0.62, 0.6], F32)
LIGHT /= np.linalg.norm(LIGHT)


def sphere_paint(cx, cy, rx, base, ry=None, light=None, amb=0.28, spec=0.35, shin=30, bounce=None, wrap=0.25, sss=None):
    """Lit ellipsoid: wrapped diffuse + specular + optional bounce light from below."""
    ry = rx if ry is None else ry
    L = LIGHT if light is None else np.array(light, F32) / np.linalg.norm(light)
    Hv = L + np.array([0, 0, 1], F32)
    Hv /= np.linalg.norm(Hv)
    base = C(base)

    def f(X, Y):
        nx, ny = (X - cx) / rx, (Y - cy) / ry
        d = np.clip(nx * nx + ny * ny, 0, 1)
        nz = np.sqrt(1 - d)
        dif = (nx * L[0] + ny * L[1] + nz * L[2] + wrap) / (1 + wrap)
        dif = np.clip(dif, 0, 1)
        col = base * (amb + (1 - amb) * dif)[..., None]
        if bounce is not None:
            b = np.clip(ny, 0, 1) ** 2 * (1 - nz) * 0.9
            col = col + C(bounce) * (b * 0.35)[..., None]
        if sss is not None:
            col = col + C(sss) * ((1 - dif) * (1 - nz) * 0.25)[..., None]
        h = np.clip(nx * Hv[0] + ny * Hv[1] + nz * Hv[2], 0, 1)
        col = col + (spec * 255 * h ** shin)[..., None]
        return col
    return f


def cyl_paint(cx, r, base, amb=0.32, spec=0.25, shin=18, horizontal=False):
    """Vertical (or horizontal) cylinder lit from the upper left."""
    base = C(base)
    L = LIGHT

    def f(X, Y):
        u = np.clip(((Y if horizontal else X) - cx) / r, -1, 1)
        nz = np.sqrt(1 - u * u)
        d = (u * (L[1] if horizontal else L[0]) + nz * L[2])
        d = np.clip((d + 0.2) / 1.2, 0, 1)
        col = base * (amb + (1 - amb) * d)[..., None]
        h = np.clip(1 - np.abs(u + 0.45) * 3, 0, 1) ** 2
        return col + (spec * 255 * h ** (shin / 10))[..., None]
    return f


# =================================================================== painting context
class Ctx:
    def __init__(self, c):
        self.c, self.s = c, c.ss
        self.alpha = c.ch == 4
        self.ox, self.oy = c.ox, c.oy
        self.hh, self.ww = c.h, c.w
        self.img = np.zeros((c.h, c.w, 3), F32)
        self.A = np.zeros((c.h, c.w), F32) if self.alpha else None
        self.snaps = {}

    # -- windows
    def win(self, bb, pad=2.0):
        s = self.s
        x0, y0, x1, y1 = bb
        i0 = max(0, int(math.floor((x0 - pad - self.ox) * s)))
        i1 = min(self.ww, int(math.ceil((x1 + pad - self.ox) * s)))
        j0 = max(0, int(math.floor((y0 - pad - self.oy) * s)))
        j1 = min(self.hh, int(math.ceil((y1 + pad - self.oy) * s)))
        if i1 <= i0 or j1 <= j0:
            return None
        xs = ((np.arange(i0, i1, dtype=F32) + 0.5) / s + self.ox).astype(F32)
        ys = ((np.arange(j0, j1, dtype=F32) + 0.5) / s + self.oy).astype(F32)
        X, Y = np.meshgrid(xs, ys)
        return (j0, j1, i0, i1), X, Y

    def full(self):
        return self.win((self.ox, self.oy, self.ox + self.ww / self.s, self.oy + self.hh / self.s), pad=0)

    def cover(self, shape, X, Y, feather=0.0):
        d = shape.sdf(X, Y)
        wdt = max(1.0 / self.s, feather)
        return np.clip(0.5 - d / wdt, 0, 1).astype(F32)

    # -- compositing
    def _over(self, w, col, m):
        j0, j1, i0, i1 = w
        sub = self.img[j0:j1, i0:i1]
        if not self.alpha:
            sub += (col - sub) * m[..., None]
        else:
            a = self.A[j0:j1, i0:i1]
            oa = m + a * (1 - m)
            k = np.where(oa > 1e-6, 1 / np.maximum(oa, 1e-6), 0)
            sub[:] = (col * m[..., None] + sub * (a * (1 - m))[..., None]) * k[..., None]
            self.A[j0:j1, i0:i1] = oa

    def fill(self, shape, paint, alpha=1.0, feather=0.0):
        r = self.win(shape.bbox(), pad=feather + 2)
        if r is None:
            return
        w, X, Y = r
        m = self.cover(shape, X, Y, feather)
        if callable(alpha):
            m = m * alpha(X, Y)
        elif alpha != 1.0:
            m = m * alpha
        if not m.any():
            return
        col = paint(X, Y) if callable(paint) else np.broadcast_to(C(paint), X.shape + (3,))
        self._over(w, col, m)

    def mul(self, shape, k, feather=0.0, alpha=1.0, tint=(0, 0, 0)):
        """Darken (multiply towards tint) - soft shadows, occlusion. k = strength 0..1."""
        r = self.win(shape.bbox(), pad=feather + 2)
        if r is None:
            return
        (j0, j1, i0, i1), X, Y = r
        m = self.cover(shape, X, Y, feather) * k
        if callable(alpha):
            m = m * alpha(X, Y)
        elif alpha != 1.0:
            m = m * alpha
        sub = self.img[j0:j1, i0:i1]
        sub += (sub * (C(tint) / 255.0) - sub) * m[..., None]   # only darkens what is already painted

    def shadow(self, shape, dx=6, dy=4, blur=8, k=0.45):
        self.mul(Moved(shape, dx, dy), k, feather=blur)

    def add(self, shape, col, k=1.0, feather=0.0, alpha=None):
        """Additive light (glows, sun shafts, sparkles)."""
        r = self.win(shape.bbox(), pad=feather + 2)
        if r is None:
            return
        (j0, j1, i0, i1), X, Y = r
        m = self.cover(shape, X, Y, feather) * k
        if alpha is not None:
            m = m * alpha(X, Y)
        self.img[j0:j1, i0:i1] += C(col) * m[..., None]
        if self.alpha:
            a = self.A[j0:j1, i0:i1]
            self.A[j0:j1, i0:i1] = np.maximum(a, np.clip(m, 0, 1))

    def glow(self, cx, cy, r, col, k=1.0, power=2.0, ry=None):
        ry = r if ry is None else ry
        rr = self.win((cx - r, cy - ry, cx + r, cy + ry))
        if rr is None:
            return
        (j0, j1, i0, i1), X, Y = rr
        d = np.clip(1 - np.hypot((X - cx) / r, (Y - cy) / ry), 0, 1) ** power * k
        self.img[j0:j1, i0:i1] += C(col) * d[..., None]
        if self.alpha:
            a = self.A[j0:j1, i0:i1]
            self.A[j0:j1, i0:i1] = np.maximum(a, np.clip(d, 0, 1))

    def fog(self, y0, y1, col, a0, a1, x0=None, x1=None, noise=0.0, sx=120, sy=30, seed=0):
        """Vertical fog / haze band (alpha a0 at y0 -> a1 at y1), optionally patchy."""
        x0 = self.ox if x0 is None else x0
        x1 = self.ox + self.ww / self.s if x1 is None else x1
        r = self.win((x0, y0, x1, y1), pad=0)
        if r is None:
            return
        w, X, Y = r
        t = np.clip((Y - y0) / max(1e-6, y1 - y0), 0, 1)
        a = a0 + (a1 - a0) * t
        if noise:
            a = a * (1 - noise + 2 * noise * fbm(X, Y, sx, sy, 4, seed))
        self._over(w, np.broadcast_to(C(col), X.shape + (3,)), np.clip(a, 0, 1).astype(F32))

    # -- whole-region operations
    def region(self, bb):
        r = self.win(bb, pad=0)
        return r

    def snapshot(self, key="s"):
        self.snaps[key] = self.img.copy()

    def reflect(self, y_line, y0, y1, x0=0, x1=W, ripple=3.0, rsx=160, rsy=2.2, k=0.75, tint=(40, 70, 90),
                tint_k=0.35, src="s", fade=0.6, seed=7, blur_k=0.0, streak=0.0):
        """Water reflection of the picture above y_line into rows y0..y1 (mirrored about y_line)."""
        r = self.win((x0, y0, x1, y1), pad=0)
        if r is None:
            return
        (j0, j1, i0, i1), X, Y = r
        srcimg = self.snaps.get(src, self.img)
        s = self.s
        n = fbm(X, Y, rsx, rsy, 3, seed) - 0.5
        n2 = fbm(X, Y, rsx * 0.25, rsy * 2.2, 2, seed + 5) - 0.5
        depth = np.clip((Y - y_line) / max(1, y1 - y_line), 0, 1)
        sx = X + n * ripple * 2 * (0.4 + depth * 1.6)
        sy = 2 * y_line - Y + n2 * ripple * 1.2 * (0.3 + depth)
        ii = np.clip(((sx - self.ox) * s).astype(np.int64), 0, self.ww - 1)
        jj = np.clip(((sy - self.oy) * s).astype(np.int64), 0, self.hh - 1)
        refl = srcimg[jj, ii]
        refl = refl * k + C(tint) * tint_k
        if streak:
            refl = refl * (1 + streak * (fbm(X, Y, 90, 1.4, 2, seed + 9) - 0.5))[..., None]
        a = (1 - depth * fade).astype(F32)
        sub = self.img[j0:j1, i0:i1]
        sub += (refl - sub) * a[..., None]

    def godrays(self, lx, ly, col=(190, 205, 240), k=0.6, src="s", threshold=110, soft=60, region=None,
                density=0.85, decay=0.965, samples=72, res=2.0, bb=None, receive=None, gamma=1.0):
        """Volumetric light shafts (crepuscular rays / moonbeams) from a light at scene (lx, ly).

        Screen-space radial blur: bright pixels of snapshot `src` (luminance above `threshold`, optionally
        limited to `region` - a Shape or (X, Y) -> 0..1 - e.g. only the sky or the window openings) are smeared
        along lines towards the light, so occluders (castle walls, branches, window tracery) cut dark gaps
        into the beams.  The light may be off-canvas (beams entering through a window from the moon outside).
        Computed on a coarse grid (`res` scene px) and added to the current image; `receive` (Shape or fn)
        scales where the rays are visible (e.g. keep them out of a foreground wall).
        The source is a snapshot of the unmodified scene, so A and B get identical rays."""
        s = self.s
        srcimg = self.snaps.get(src, self.img)
        x0w, y0w = self.ox, self.oy
        x1w, y1w = self.ox + self.ww / s, self.oy + self.hh / s
        gw, gh = int(math.ceil((x1w - x0w) / res)), int(math.ceil((y1w - y0w) / res))
        gx = (x0w + (np.arange(gw, dtype=F32) + 0.5) * res).astype(F32)
        gy = (y0w + (np.arange(gh, dtype=F32) + 0.5) * res).astype(F32)
        GX, GY = np.meshgrid(gx, gy)
        ii = np.clip(((GX - self.ox) * s).astype(np.int64), 0, self.ww - 1)
        jj = np.clip(((GY - self.oy) * s).astype(np.int64), 0, self.hh - 1)
        lum = srcimg[jj, ii] @ np.array([0.3, 0.5, 0.2], F32)
        mask = np.clip((lum - threshold) / max(1.0, soft), 0, 1) ** gamma
        if region is not None:
            mask = mask * (self.cover(region, GX, GY, 1.5) if isinstance(region, Shape) else region(GX, GY))
        # march every grid cell towards the light, accumulating the decaying mask
        acc = np.zeros_like(mask)
        dx, dy = (GX - lx) * (density / samples), (GY - ly) * (density / samples)
        px, py = GX.copy(), GY.copy()
        wsum, w = 0.0, 1.0
        for _ in range(samples):
            px -= dx
            py -= dy
            mi = np.floor((px - x0w) / res).astype(np.int64)
            mj = np.floor((py - y0w) / res).astype(np.int64)
            ok = (mi >= 0) & (mi < gw) & (mj >= 0) & (mj < gh)
            acc += np.where(ok, mask[np.clip(mj, 0, gh - 1), np.clip(mi, 0, gw - 1)], 0) * w
            wsum += w
            w *= decay
        acc /= wsum
        acc = _box(_box(acc, 1, 0), 1, 1)
        # bilinear up-sample to the canvas window and add
        r = self.win(bb or (x0w, y0w, x1w, y1w), pad=0)
        if r is None:
            return
        (j0, j1, i0, i1), X, Y = r
        fx = np.clip((X[0] - x0w) / res - 0.5, 0, gw - 1.001)
        fy = np.clip((Y[:, 0] - y0w) / res - 0.5, 0, gh - 1.001)
        xi, yi = fx.astype(np.int64), fy.astype(np.int64)
        tx, ty = (fx - xi)[None, :], (fy - yi)[:, None]
        a = acc[yi][:, xi] * (1 - tx) + acc[yi][:, xi + 1] * tx
        b = acc[yi + 1][:, xi] * (1 - tx) + acc[yi + 1][:, xi + 1] * tx
        v = (a * (1 - ty) + b * ty) * k
        if receive is not None:
            v = v * (self.cover(receive, X, Y, 6.0) if isinstance(receive, Shape) else receive(X, Y))
        self.img[j0:j1, i0:i1] += C(col) * v[..., None]

    def blur(self, bb, radius):
        """Gaussian-ish blur (3 box passes) of a region, radius in scene px."""
        r = self.win(bb, pad=0)
        if r is None:
            return
        (j0, j1, i0, i1), _, _ = r
        rad = max(1, int(round(radius * self.s / 1.7)))
        a = self.img[j0:j1, i0:i1]
        for _ in range(3):
            a = _box(_box(a, rad, 0), rad, 1)
        self.img[j0:j1, i0:i1] = a

    def bloom(self, threshold=200, radius=14, k=0.5, bb=None):
        bb = bb or (self.ox, self.oy, self.ox + self.ww / self.s, self.oy + self.hh / self.s)
        r = self.win(bb, pad=0)
        if r is None:
            return
        (j0, j1, i0, i1), _, _ = r
        a = self.img[j0:j1, i0:i1]
        lum = a.mean(-1, keepdims=True)
        b = a * np.clip((lum - threshold) / (255 - threshold + 1e-6), 0, 1)
        rad = max(1, int(round(radius * self.s / 1.7)))
        for _ in range(3):
            b = _box(_box(b, rad, 0), rad, 1)
        self.img[j0:j1, i0:i1] = a + b * k

    def grade(self, contrast=1.06, sat=1.05, lift=(0, 0, 0), gain=(1, 1, 1), warm=0.0):
        a = self.img
        mean = 128.0
        a = (a - mean) * contrast + mean
        g = a.mean(-1, keepdims=True)
        a = g + (a - g) * sat
        a = a * C(gain) / 255.0 * 255.0 + C(lift)
        if warm:
            a = a + np.array([warm, warm * 0.3, -warm], F32)
        self.img = a

    def commit(self):
        img = np.clip(self.img, 0, 255).astype(np.uint8)
        if self.alpha:
            out = np.concatenate([img, (np.clip(self.A, 0, 1) * 255 + 0.5).astype(np.uint8)[..., None]], -1)
            # keep anything the canvas already had underneath (other draw calls in the same element)
            old = np.frombuffer(b"".join(bytes(r) for r in self.c.rows), np.uint8).reshape(self.hh, self.ww, 4)
            if old[..., 3].any():
                oa = old[..., 3:4] / 255.0
                na = out[..., 3:4] / 255.0
                ra = na + oa * (1 - na)
                rgb = (out[..., :3] * na + old[..., :3] * oa * (1 - na)) / np.maximum(ra, 1e-6)
                out = np.concatenate([np.clip(rgb, 0, 255), ra * 255], -1).astype(np.uint8)
        else:
            out = img
        for j in range(self.hh):
            self.c.rows[j][:] = out[j].tobytes()


def _box(a, r, axis):
    """Box blur of radius r along axis (edge-clamped)."""
    n = a.shape[axis]
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    p = np.pad(a, pad, mode="edge")
    cs = np.cumsum(p, axis=axis, dtype=np.float32)
    hi = np.take(cs, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(cs, np.arange(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


# =================================================================== post (final resolution rows)
def real_post(rows, w, h, ox, oy, has_alpha, grain=4.5, vignette=0.22):
    ch = 4 if has_alpha else 3
    a = np.frombuffer(b"".join(bytes(r) for r in rows), np.uint8).reshape(h, w, ch).astype(F32)
    xs = np.arange(w, dtype=F32) + ox + 0.25
    ys = np.arange(h, dtype=F32) + oy + 0.25
    X, Y = np.meshgrid(xs, ys)
    n = (hash2(X, Y, 991) + hash2(X + 0.5, Y, 313) - 1.0) * grain
    rgb = a[..., :3] + n[..., None]
    if not has_alpha and vignette:
        d = ((X - W / 2) / (W * 0.62)) ** 2 + ((Y - H / 2) / (H * 0.70)) ** 2
        rgb = rgb * (1 - vignette * np.clip(d, 0, 1.6) ** 1.6 / 1.6 ** 1.6 * 1.0)[..., None]
    a[..., :3] = rgb
    out = np.clip(a, 0, 255).astype(np.uint8)
    for j in range(h):
        rows[j][:] = out[j].tobytes()


# =================================================================== element helper
def el(fn):
    """Wrap a painter fn(g, m) into an fdcore element draw(c, m)."""
    def draw(c, m):
        g = Ctx(c)
        fn(g, m)
        g.commit()
    return draw
