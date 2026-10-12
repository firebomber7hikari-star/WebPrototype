# -*- coding: utf-8 -*-
"""
Simple one-point perspective for side-view scenes ("near is big, far is small").

  View(hz, vpx, yref)      horizon line, vanishing point x, reference ground line (scale 1 there)
  view.s(y)                depth scale of the ground at screen row y (0 at the horizon, 1 at yref)
  view.wx(X, y)            screen x of world position X (0 = vanishing point) on ground row y
  view.at(x, y, k, anchor) placement of an object drawn in its own coordinates: the anchor point of the drawing
                           (usually its foot) lands at screen (x, y); size = k * s(y); colours fade into the haze
  xf.canvas(c)             canvas proxy that applies the placement to every drawing call
  xf.p(x, y)               transformed point (for pivots and difference centres)

Distance cues: scale, haze (atmospheric perspective) and - through paper25.PaperCanvas.cur_scale -
smaller / lighter shadows and thinner paper edges on far pieces.
"""
import math

from fdcore import mix


class Xf:
    def __init__(self, x, y, s, anchor=(0.0, 0.0), haze=None, t=0.0):
        self.x, self.y, self.s, self.anchor, self.haze, self.t = x, y, s, anchor, haze, t

    def p(self, lx, ly):
        return (self.x + (lx - self.anchor[0]) * self.s, self.y + (ly - self.anchor[1]) * self.s)

    def col(self, col):
        if self.haze is None or self.t <= 0 or callable(col):
            return col
        m = mix(col, self.haze, self.t)
        return m + tuple(col[3:])

    def canvas(self, c):
        return XCanvas(c, self)

    def draw(self, fn, *args):
        """Return a draw(c, m) function for an element painted by fn(canvas, m, *args) under this placement."""
        def d(c, m):
            fn(XCanvas(c, self), m, *args)
        return d


class XCanvas:
    def __init__(self, c, xf):
        self.c, self.xf = c, xf

    def _pre(self):
        if hasattr(self.c, "cur_scale"):
            self.c.cur_scale = round(self.xf.s, 3)

    def rect(self, x0, y0, x1, y1, col):
        self._pre()
        (a, b), (e, f) = self.xf.p(x0, y0), self.xf.p(x1, y1)
        self.c.rect(a, b, e, f, self.xf.col(col))

    def round_rect(self, x0, y0, x1, y1, r, col):
        self._pre()
        (a, b), (e, f) = self.xf.p(x0, y0), self.xf.p(x1, y1)
        self.c.round_rect(a, b, e, f, r * self.xf.s, self.xf.col(col))

    def circle(self, cx, cy, r, col):
        self._pre()
        x, y = self.xf.p(cx, cy)
        self.c.circle(x, y, r * self.xf.s, self.xf.col(col))

    def ellipse(self, cx, cy, rx, ry, col, ymin=None, ymax=None):
        self._pre()
        x, y = self.xf.p(cx, cy)
        s = self.xf.s
        ymin = None if ymin is None else self.xf.p(0, ymin)[1]
        ymax = None if ymax is None else self.xf.p(0, ymax)[1]
        self.c.ellipse(x, y, rx * s, ry * s, self.xf.col(col), ymin=ymin, ymax=ymax)

    def polygon(self, pts, col):
        self._pre()
        self.c.polygon([self.xf.p(x, y) for x, y in pts], self.xf.col(col))

    def line(self, x0, y0, x1, y1, width, col, caps=True):
        self._pre()
        (a, b), (e, f) = self.xf.p(x0, y0), self.xf.p(x1, y1)
        self.c.line(a, b, e, f, max(0.8, width * self.xf.s), self.xf.col(col), caps=caps)

    def star(self, cx, cy, r_out, r_in, col, points=5, rot=-90):
        self._pre()
        x, y = self.xf.p(cx, cy)
        self.c.star(x, y, r_out * self.xf.s, r_in * self.xf.s, self.xf.col(col), points, rot)

    def ellipse_ring(self, cx, cy, rx, ry, thick, col, ymin=None, ymax=None):
        self._pre()
        x, y = self.xf.p(cx, cy)
        s = self.xf.s
        ymin = None if ymin is None else self.xf.p(0, ymin)[1]
        ymax = None if ymax is None else self.xf.p(0, ymax)[1]
        self.c.ellipse_ring(x, y, rx * s, ry * s, max(1.0, thick * s), self.xf.col(col), ymin=ymin, ymax=ymax)

    def bird(self, x, y, size, col):
        self._pre()
        px, py = self.xf.p(x, y)
        self.c.bird(px, py, size * self.xf.s, self.xf.col(col))


class View:
    def __init__(self, hz, vpx=450.0, yref=600.0, haze=None, haze_k=0.55):
        self.hz, self.vpx, self.yref, self.haze, self.haze_k = hz, vpx, yref, haze, haze_k

    def s(self, y):
        return max(0.01, (y - self.hz) / (self.yref - self.hz))

    def wx(self, X, y):
        return self.vpx + X * self.s(y)

    def y_of(self, s):
        return self.hz + s * (self.yref - self.hz)

    def haze_t(self, y):
        return self.haze_k * max(0.0, 1.0 - self.s(y)) ** 2.2

    def at(self, x, y, k=1.0, anchor=(0.0, 0.0), haze_y=None):
        return Xf(x, y, k * self.s(y), anchor, self.haze, self.haze_t(y if haze_y is None else haze_y))

    def atX(self, X, y, k=1.0, anchor=(0.0, 0.0)):
        return self.at(self.wx(X, y), y, k, anchor)

    # ---------------------------------------------------------------- ground helpers
    def ground_rows(self, depth_step=0.12, near=1.0, far=0.03):
        """Screen rows of evenly spaced ground lines (equal world spacing -> 1/z on screen)."""
        rows = []
        z = 1.0 / near
        while True:
            s = 1.0 / z
            if s < far:
                break
            rows.append(self.y_of(s))
            z += depth_step
        return rows

    def radial(self, c, X, col, width=1.5, y0=None, y1=None):
        y0 = self.hz + 1 if y0 is None else y0
        y1 = self.yref + 40 if y1 is None else y1
        c.line(self.wx(X, y0), y0, self.wx(X, y1), y1, width, col)


# =================================================================== 3D camera for interiors
class Cam:
    """Pinhole camera looking down +Z. World units are metres, Y is height relative to the eye (up = +).
    Distance fades colours into `dark` (fog / gloom between fog[0] and fog[1] metres)."""

    def __init__(self, vpx=450.0, vpy=300.0, f=300.0, dark=(20, 18, 24), fog=(1.5, 16.0), fog_k=0.8):
        self.vpx, self.vpy, self.f, self.dark, self.fog, self.fog_k = vpx, vpy, f, dark, fog, fog_k

    def p(self, X, Y, Z):
        return (self.vpx + X * self.f / Z, self.vpy - Y * self.f / Z)

    def s(self, Z):
        """Pixels per metre at depth Z."""
        return self.f / Z

    def t(self, Z):
        u = max(0.0, min(1.0, (Z - self.fog[0]) / (self.fog[1] - self.fog[0])))
        return self.fog_k * u ** 0.85

    def col(self, col, Z):
        if callable(col):
            return col
        return mix(col, self.dark, self.t(Z)) + tuple(col[3:])

    def _depth(self, c, z):
        if hasattr(c, "cur_scale"):                     # paper shadows shrink with distance
            c.cur_scale = round(min(1.4, max(0.2, self.f / z / 220.0)), 2)

    def poly(self, c, pts3, col, flat=False, glow=False):
        z = sum(q[2] for q in pts3) / len(pts3)
        self._depth(c, z)
        cc = col if glow else self.col(col, z)
        if flat and len(cc) == 3:
            cc = tuple(cc) + (1.0,)
        c.polygon([self.p(*q) for q in pts3], cc)

    def line(self, c, a, b, width_m, col, flat=True, glow=False):
        z = (a[2] + b[2]) / 2
        self._depth(c, z)
        cc = col if glow else self.col(col, z)
        if flat and len(cc) == 3:
            cc = tuple(cc) + (1.0,)
        (x0, y0), (x1, y1) = self.p(*a), self.p(*b)
        c.line(x0, y0, x1, y1, max(0.8, width_m * self.f / z), cc)

    def at(self, X, Y, Z, k=1.0, anchor=(0.0, 0.0)):
        """Front-facing object drawn in centimetres (anchor = its foot) standing at (X, Y, Z)."""
        x, y = self.p(X, Y, Z)
        return Xf(x, y, k * self.f / Z / 100.0, anchor, self.dark, self.t(Z))

    # ---------------------------------------------------------------- planes
    def wall_pt(self, X, z, y):
        """Point on a side wall (plane X = const), u = depth z, v = height y."""
        return (X, y, z)

    def wall_poly(self, c, X, pts_zy, col, flat=False, glow=False):
        self.poly(c, [(X, y, z) for z, y in pts_zy], col, flat, glow)

    def wall_rect(self, c, X, z0, z1, y0, y1, col, flat=False, glow=False):
        self.wall_poly(c, X, [(z0, y0), (z1, y0), (z1, y1), (z0, y1)], col, flat, glow)

    def wall_ellipse(self, c, X, zc, yc, rz, ry, col, n=28, flat=False, glow=False):
        self.poly(c, [(X, yc + ry * math.sin(2 * math.pi * k / n), zc + rz * math.cos(2 * math.pi * k / n)) for k in range(n)], col, flat,
                  glow)

    def floor_poly(self, c, Y, pts_xz, col, flat=True, glow=False):
        self.poly(c, [(x, Y, z) for x, z in pts_xz], col, flat, glow)

    def floor_rect(self, c, Y, x0, x1, z0, z1, col, flat=True, glow=False):
        self.floor_poly(c, Y, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], col, flat, glow)

    def floor_ellipse(self, c, Y, xc, zc, rx, rz, col, n=32, flat=True, glow=False):
        self.poly(c, [(xc + rx * math.cos(2 * math.pi * k / n), Y, zc + rz * math.sin(2 * math.pi * k / n)) for k in range(n)], col, flat,
                  glow)

    def back_poly(self, c, Z, pts_xy, col, flat=False, glow=False):
        self.poly(c, [(x, y, Z) for x, y in pts_xy], col, flat, glow)

    def back_rect(self, c, Z, x0, x1, y0, y1, col, flat=False, glow=False):
        self.back_poly(c, Z, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, flat, glow)

    def back_ellipse(self, c, Z, xc, yc, rx, ry, col, n=28, flat=False, glow=False):
        self.back_poly(c, Z, [(xc + rx * math.cos(2 * math.pi * k / n), yc + ry * math.sin(2 * math.pi * k / n)) for k in range(n)], col,
                       flat, glow)

    def depth_strips(self, c, quad_fn, z0, z1, col, n=24):
        """A long plane drawn as strips that darken with distance. quad_fn(za, zb) -> 4 world points."""
        zs = [z0 * (z1 / z0) ** (k / n) for k in range(n + 1)]
        for a, b in zip(zs, zs[1:]):
            self.poly(c, quad_fn(a, b * 1.002), col, flat=True)


SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg",
       "9": "abcdfg"}


def seven_seg(c, cam, X, z0, y0, h, text, col, width_m=0.012):
    """Digits written on a side wall (plane X), starting at depth z0, baseline y0, height h (metres)."""
    w = h * 0.5
    sgn = 1 if X < 0 else -1          # reading direction: left wall runs away from the viewer, right wall towards
    for i, ch in enumerate(text):
        zl = z0 + sgn * i * w * 1.5
        zr = zl + sgn * w
        P = {"tl": (zl, y0 + h), "tr": (zr, y0 + h), "ml": (zl, y0 + h / 2), "mr": (zr, y0 + h / 2), "bl": (zl, y0), "br": (zr, y0)}
        segs = {"a": ("tl", "tr"), "b": ("tr", "mr"), "c": ("mr", "br"), "d": ("bl", "br"), "e": ("ml", "bl"), "f": ("tl", "ml"),
                "g": ("ml", "mr")}
        for sname in SEG.get(ch, ""):
            (za, ya), (zb, yb) = P[segs[sname][0]], P[segs[sname][1]]
            cam.line(c, (X, ya, za), (X, yb, zb), width_m, col)
