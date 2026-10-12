# -*- coding: utf-8 -*-
"""
Paper 2.5D adapter: runs ordinary Canvas drawing code (rect / circle / polygon / line ...) and turns every
primitive into a layered paper cut-out:

  * consecutive primitives with the same colour are glued into one piece (clouds, bushes, balloons ...)
  * the size of a piece decides its depth: wide layers cast a long soft shadow onto the scene behind,
    props get a white cut edge + drop shadow, small parts a thin contact shadow, fine details stay flat
  * larger pieces get a soft top-lit gradient, so the cut-outs read as slightly bent card

Use paperize(fn) on background / element draw functions and post=paper_post for the paper grain.
"""
import math

from fdcore import lit, linear, mix
from paper import PAPER_WHITE, Ell, Poly, RRect, Thick, piece, star_pts

LAYER = (1, 4, 12, 0.36)       # wide scenery layers
PROP = (2, 4, 8, 0.42)         # objects
SMALL = (1, 2, 3, 0.32)        # small parts
FLAT, SMALL_K, PROP_K, LAYER_K, BASE_K = 0, 1, 2, 3, 4


def _classify(shape):
    if isinstance(shape, Thick):
        w = shape.w
        if w >= 8:
            return PROP_K
        return SMALL_K if w >= 4 else FLAT
    x0, y0, x1, y1 = shape.bbox()
    w, h = x1 - x0, y1 - y0
    if w >= 880 and h >= 150:
        return BASE_K
    if w >= 480:
        return LAYER_K
    if min(w, h) >= 12 and w * h >= 400:
        return PROP_K
    if min(w, h) >= 5:
        return SMALL_K
    return FLAT


class PaperCanvas:
    def __init__(self, c, edge_mix=0.0):
        self.c = c
        self.edge_mix = edge_mix     # > 0: the cut edge takes on the piece colour (dark scenes: no glowing white rims)
        self.pending = None          # (colour, [shapes], depth scale)
        self.cur_scale = 1.0         # set by a perspective canvas (persp.XCanvas): shadows / borders shrink with distance

    def __getattr__(self, name):     # anything not overridden goes to the real canvas
        attr = getattr(self.c, name)
        if callable(attr):
            def call(*a, **kw):
                self.flush()
                return attr(*a, **kw)
            return call
        return attr

    # ---------------------------------------------------------------- grouping
    def _add(self, shape, col):
        if callable(col) or len(col) == 4:
            self.flush()
            shape.draw(self.c, col)
            return
        if self.pending and self.pending[0] == col and self.pending[2] == self.cur_scale:
            self.pending[1].append(shape)
        else:
            self.flush()
            self.pending = (col, [shape], self.cur_scale)

    def flush(self):
        if not self.pending:
            return
        col, shapes, ds = self.pending
        self.pending = None
        k_off = min(1.6, max(0.25, ds))
        k_a = min(1.0, 0.45 + 0.55 * ds)

        def sh(v):
            return (v[0] * k_off, v[1] * k_off, v[2] * k_off, v[3] * k_a)
        k = max(_classify(s) for s in shapes)
        c = self.c
        if k == BASE_K:
            for s in shapes:
                s.draw(c, col)
            return
        if k == FLAT:
            for s in shapes:
                s.draw(c, col)
            return
        fill = col
        bx = [s.bbox() for s in shapes]
        y0, y1 = min(b[1] for b in bx), max(b[3] for b in bx)
        area = sum((b[2] - b[0]) * (b[3] - b[1]) for b in bx)
        if k >= PROP_K and area >= 1500 and y1 - y0 >= 16:
            fill = linear(0, y0, 0, y1, lit(col, 1.07), lit(col, 0.9))
        if k == LAYER_K:
            piece(c, shapes, fill, shadow=sh(LAYER))
        elif k == PROP_K:
            edge = mix(PAPER_WHITE, col, self.edge_mix) if self.edge_mix else PAPER_WHITE
            piece(c, shapes, fill, border=1.5 * min(1.0, max(0.45, ds)), border_col=edge, shadow=sh(PROP))
        else:
            piece(c, shapes, fill, shadow=sh(SMALL))

    # ---------------------------------------------------------------- primitives
    def rect(self, x0, y0, x1, y1, col):
        self._add(RRect(x0, y0, x1, y1, 0), col)

    def round_rect(self, x0, y0, x1, y1, r, col):
        self._add(RRect(x0, y0, x1, y1, r), col)

    def circle(self, cx, cy, r, col):
        self._add(Ell(cx, cy, r, r), col)

    def ellipse(self, cx, cy, rx, ry, col, ymin=None, ymax=None):
        if ymin is not None or ymax is not None:
            self.flush()
            self.c.ellipse(cx, cy, rx, ry, col, ymin=ymin, ymax=ymax)
        else:
            self._add(Ell(cx, cy, rx, ry), col)

    def polygon(self, pts, col):
        self._add(Poly(pts), col)

    def line(self, x0, y0, x1, y1, width, col, caps=True):
        if width < 4 or not caps:
            self.flush()
            self.c.line(x0, y0, x1, y1, width, col, caps=caps)
        else:
            self._add(Thick(x0, y0, x1, y1, width), col)

    def star(self, cx, cy, r_out, r_in, col, points=5, rot=-90):
        if r_out < 8:
            self.flush()
            self.c.star(cx, cy, r_out, r_in, col, points, rot)
        else:
            self._add(Poly(star_pts(cx, cy, r_out, r_in, points, rot)), col)

    def ellipse_ring(self, cx, cy, rx, ry, thick, col, ymin=None, ymax=None):
        if thick < 5 or ymin is not None or ymax is not None:
            self.flush()
            self.c.ellipse_ring(cx, cy, rx, ry, thick, col, ymin=ymin, ymax=ymax)
            return
        n = 48
        r0, r1 = rx - thick / 2, ry - thick / 2
        pts = [(cx + r0 * math.cos(2 * math.pi * k / n), cy + r1 * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
        self.flush()
        piece(self.c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], thick) for k in range(n)], col, border=1.5, shadow=PROP)


def paperize(fn, edge_mix=0.0):
    def run(c, arg):
        pc = PaperCanvas(c, edge_mix)
        fn(pc, arg)
        pc.flush()
    return run


def paper_level(level, edge_mix=0.0):
    """Wrap a LEVELS tuple: background and every element draw through PaperCanvas."""
    name, title, bg, elements, diffs, time_limit, *opts = level
    for e in elements:
        e.draw = paperize(e.draw, edge_mix)
    return (name, title, paperize(bg, edge_mix), elements, diffs, time_limit, *opts)
