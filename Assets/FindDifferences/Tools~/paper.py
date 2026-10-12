# -*- coding: utf-8 -*-
"""
Paper-craft drawing helpers.

A *piece* is a cut-out sheet of paper: a union of shapes drawn as
    soft layered shadow  ->  optional white cut border  ->  flat paper colour
and every finished image gets a paper-grain pass (fibres + fine grain, see `grain`).

Shapes know how to draw themselves grown by `e` pixels and shifted, which is what
borders and shadows need. Polygons are offset with mitred corners.
"""
import math
import re

from fdcore import Canvas, H, W

PAPER_WHITE = (252, 248, 238)
SHADOW = (45, 28, 35)
_NONZERO = re.compile(rb"[^\x00]+")


# ------------------------------------------------------------------- shapes
class Ell:
    def __init__(self, cx, cy, rx, ry=None):
        self.cx, self.cy, self.rx, self.ry = cx, cy, rx, ry if ry is not None else rx

    def draw(self, c, col, e=0.0, dx=0.0, dy=0.0):
        c.ellipse(self.cx + dx, self.cy + dy, self.rx + e, self.ry + e, col)

    def bbox(self):
        return (self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry)


def Circ(cx, cy, r):
    return Ell(cx, cy, r, r)


class RRect:
    def __init__(self, x0, y0, x1, y1, r=3.0):
        self.x0, self.y0, self.x1, self.y1, self.r = x0, y0, x1, y1, r

    def draw(self, c, col, e=0.0, dx=0.0, dy=0.0):
        r = min(self.r + e, (self.x1 - self.x0) / 2 + e, (self.y1 - self.y0) / 2 + e)
        c.round_rect(self.x0 - e + dx, self.y0 - e + dy, self.x1 + e + dx, self.y1 + e + dy, r, col)

    def bbox(self):
        return (self.x0, self.y0, self.x1, self.y1)


class Poly:
    def __init__(self, pts):
        self.pts = [tuple(p) for p in pts]
        area = 0.0
        n = len(self.pts)
        for i in range(n):
            x0, y0 = self.pts[i]
            x1, y1 = self.pts[(i + 1) % n]
            area += x0 * y1 - x1 * y0
        self.orient = 1.0 if area > 0 else -1.0
        self._cache = {}

    def offset(self, e):
        if e == 0:
            return self.pts
        key = round(e, 3)
        if key in self._cache:
            return self._cache[key]
        pts, n, out = self.pts, len(self.pts), []
        for i in range(n):
            px, py = pts[i - 1]
            vx, vy = pts[i]
            nx_, ny_ = pts[(i + 1) % n]
            n1 = self._normal(px, py, vx, vy)
            n2 = self._normal(vx, vy, nx_, ny_)
            mx, my = n1[0] + n2[0], n1[1] + n2[1]
            dot = 1 + n1[0] * n2[0] + n1[1] * n2[1]
            if dot < 0.6:           # sharp corner: limit the mitre so shadows don't grow spikes
                dot = 0.6
            out.append((vx + mx * e / dot, vy + my * e / dot))
        self._cache[key] = out
        return out

    def _normal(self, x0, y0, x1, y1):
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1.0
        # outward normal for either winding
        return (-dy / ln * self.orient * -1, dx / ln * self.orient * -1)

    def draw(self, c, col, e=0.0, dx=0.0, dy=0.0):
        pts = self.offset(e)
        if dx or dy:
            pts = [(x + dx, y + dy) for x, y in pts]
        c.polygon(pts, col)

    def bbox(self):
        xs = [p[0] for p in self.pts]
        ys = [p[1] for p in self.pts]
        return (min(xs), min(ys), max(xs), max(ys))


class Thick:
    """A stroke (stick, string, stem) as a shape."""

    def __init__(self, x0, y0, x1, y1, width):
        self.a, self.b, self.w = (x0, y0), (x1, y1), width

    def draw(self, c, col, e=0.0, dx=0.0, dy=0.0):
        c.line(self.a[0] + dx, self.a[1] + dy, self.b[0] + dx, self.b[1] + dy, self.w + 2 * e, col)

    def bbox(self):
        return (min(self.a[0], self.b[0]) - self.w, min(self.a[1], self.b[1]) - self.w,
                max(self.a[0], self.b[0]) + self.w, max(self.a[1], self.b[1]) + self.w)


# ------------------------------------------------------------------- mask for shadows
class _Mask(Canvas):
    """Single-channel coverage buffer with the same geometry as a target canvas."""

    def __init__(self, like):
        self.ss, self.ox, self.oy, self.w, self.h = like.ss, like.ox, like.oy, like.w, like.h
        self.ch = 1
        self.rows = [bytearray(self.w) for _ in range(self.h)]

    def _span(self, y, x0, x1, v):
        if y < 0 or y >= self.h:
            return
        a = max(0, int(round((x0 - self.ox) * self.ss)))
        b = min(self.w, int(round((x1 - self.ox) * self.ss)))
        if b > a:
            self.rows[y][a:b] = bytes((v,)) * (b - a)


def _shadow(c, shapes, grow, dx, dy, spread, alpha, col=SHADOW, steps=6, cutout=True):
    mask = _Mask(c)
    for k in range(steps):
        e = grow + spread * (1 - k / steps)
        v = max(1, int(255 * alpha * ((k + 1) / steps) ** 1.6))
        for s in shapes:
            s.draw(mask, v, e, dx, dy)
    for s in shapes:
        if cutout:                        # the piece itself hides the shadow under it
            s.draw(mask, 0, grow)
        else:
            s.draw(mask, max(1, int(255 * alpha)), grow, dx, dy)

    xs0, ys0, xs1, ys1 = _union_bbox(shapes)
    pad = grow + spread + max(abs(dx), abs(dy)) + 2
    y_from = max(0, int((ys0 - pad - c.oy) * c.ss))
    y_to = min(c.h, int((ys1 + pad - c.oy) * c.ss) + 1)
    sr, sg, sb = col
    ch = c.ch
    for y in range(y_from, y_to):
        mrow = mask.rows[y]
        row = c.rows[y]
        for m in _NONZERO.finditer(mrow):
            for i in range(m.start(), m.end()):
                a = mrow[i] / 255.0
                k = i * ch
                if ch == 3:
                    row[k] = int(row[k] + (sr - row[k]) * a)
                    row[k + 1] = int(row[k + 1] + (sg - row[k + 1]) * a)
                    row[k + 2] = int(row[k + 2] + (sb - row[k + 2]) * a)
                else:
                    da = row[k + 3] / 255.0
                    oa = a + da * (1 - a)
                    f = da * (1 - a)
                    row[k] = int((sr * a + row[k] * f) / oa)
                    row[k + 1] = int((sg * a + row[k + 1] * f) / oa)
                    row[k + 2] = int((sb * a + row[k + 2] * f) / oa)
                    row[k + 3] = int(oa * 255)


def _union_bbox(shapes):
    bs = [s.bbox() for s in shapes]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


# ------------------------------------------------------------------- pieces
def piece(c, shapes, col, border=0.0, border_col=PAPER_WHITE, shadow=(2, 4, 9, 0.38)):
    """Draw one paper cut-out. shadow = (dx, dy, spread, alpha) or None."""
    if not isinstance(shapes, (list, tuple)):
        shapes = [shapes]
    if shadow:
        dx, dy, spread, alpha = shadow
        _shadow(c, shapes, border, dx, dy, spread, alpha)
    if border:
        for s in shapes:
            s.draw(c, border_col, border)
    for s in shapes:
        s.draw(c, col)


def soft_union(c, shapes, col, alpha, spread=10.0):
    """Translucent soft-edged silhouette of a union of shapes (cloud shadows, puddles).
    Overlapping shapes do not darken each other."""
    _shadow(c, shapes, 0.0, 0.0, 0.0, spread, alpha, col=col, cutout=False)


def flat(c, shapes, col):
    """Paper detail glued on top of a piece (no shadow, no border)."""
    if not isinstance(shapes, (list, tuple)):
        shapes = [shapes]
    for s in shapes:
        s.draw(c, col)


# ------------------------------------------------------------------- outlines
def wave_strip(top, amp, period, phase=0.0, x0=-90, x1=990, bottom=660, step=6):
    """Scalloped paper wave: a row of rounded bumps along `top`."""
    pts = []
    x = x0
    while x <= x1:
        t = ((x - x0) / period + phase) % 1.0
        y = top - amp * math.sin(t * math.pi) ** 0.7
        pts.append((x, y))
        x += step
    pts += [(x1, bottom), (x0, bottom)]
    return Poly(pts)


def hill_strip(top, waves, x0=-60, x1=960, bottom=660, step=8):
    """Smooth hill line: top + sum(a * sin(x * f + p)) for (a, f, p) in waves."""
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, top + sum(a * math.sin(x * f + p) for a, f, p in waves)))
        x += step
    pts += [(x1, bottom), (x0, bottom)]
    return Poly(pts)


def hill_y(top, waves, x):
    return top + sum(a * math.sin(x * f + p) for a, f, p in waves)


def star_pts(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ngon(cx, cy, r, n, rot=0.0, ry=None):
    ry = ry or r
    return [(cx + r * math.cos(math.radians(rot + i * 360 / n)), cy + ry * math.sin(math.radians(rot + i * 360 / n)))
            for i in range(n)]


# ------------------------------------------------------------------- paper grain
def _hash(x, y):
    n = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def grain(rows, w, h, ox, oy, has_alpha, strength=1.0, vignette=False):
    """Multiply by a paper texture: soft blotches + horizontal fibres + fine grain.
    Uses scene coordinates so element sprites line up with the background."""
    ch = 4 if has_alpha else 3
    cell = 9
    for j in range(h):
        sy = j + oy
        gy, fy = divmod(sy, cell)
        fy /= cell
        fibre = (_hash(7, sy) - 0.5) * 0.022 + (_hash(11, sy // 3) - 0.5) * 0.018
        row = rows[j]
        for i in range(w):
            k = i * ch
            if has_alpha and row[k + 3] == 0:
                continue
            sx = i + ox
            gx, fx = divmod(sx, cell)
            fx /= cell
            a = _hash(gx, gy)
            b = _hash(gx + 1, gy)
            c2 = _hash(gx, gy + 1)
            d = _hash(gx + 1, gy + 1)
            blot = (a + (b - a) * fx) * (1 - fy) + (c2 + (d - c2) * fx) * fy
            f = 1 + strength * ((blot - 0.5) * 0.05 + fibre + (_hash(sx, sy) - 0.5) * 0.05)
            if vignette:
                vx, vy = (sx - W / 2) / (W / 2), (sy - H / 2) / (H / 2)
                f *= 1 - 0.13 * (vx * vx + vy * vy) ** 1.3
            for q in range(3):
                v = int(row[k + q] * f)
                row[k + q] = 255 if v > 255 else v


def paper_post(rows, w, h, ox, oy, has_alpha):
    grain(rows, w, h, ox, oy, has_alpha, vignette=not has_alpha)
