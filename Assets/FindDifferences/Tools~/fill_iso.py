# -*- coding: utf-8 -*-
"""
Full-bleed helpers for the isometric levels: instead of a paper base floating on an empty backdrop,
the ground covers the whole picture and the surroundings are filled with scattered scenery.

  iso_ground(c, col, grid)          - ground over the whole frame (+ faint iso grid)
  surround_points(seed, ...)        - jittered screen positions outside the playable diamond
  draw_surround(c, pts, draw, part) - draws decor behind ('back') or in front ('front') of the diamond
"""
import math
import random

from fdcore import H, W
from paper import Thick, flat
from levels_views import P, T, OX, OY


def to_iso(x, y):
    a, b = (x - OX) / T, (y - OY) / (T / 2)
    return (a + b) / 2, (b - a) / 2


def iso_ground(c, col, grid=None, extent=(-24, 34)):
    c.rect(-10, -10, W + 10, H + 70, col)
    if grid:
        lo, hi = extent
        for k in range(lo, hi):
            for a, b in ((P(k, lo), P(k, hi)), (P(lo, k), P(hi, k))):
                flat(c, Thick(a[0], a[1], b[0], b[1], 1), grid)


def surround_points(seed, step=58, margin=0.45, jitter=0.4, keep=0.8, inside=(0, 10)):
    rnd = random.Random(seed)
    lo, hi = inside
    pts = []
    for y in range(-30, H + 60, int(step * 0.6)):
        for x in range(-20, W + 40, step):
            xx = x + rnd.uniform(-step * jitter, step * jitter)
            yy = y + rnd.uniform(-step * jitter * 0.6, step * jitter * 0.6)
            X, Y = to_iso(xx, yy)
            if lo - margin <= X <= hi + margin and lo - margin <= Y <= hi + margin:
                continue
            if rnd.random() > keep:
                continue
            pts.append((X, Y, rnd.random()))
    return pts


def draw_surround(c, pts, draw, part):
    """part 'back' = everything farther away than the diamond's centre line, 'front' = the rest."""
    for X, Y, r in sorted(pts, key=lambda p: p[0] + p[1]):
        is_back = X + Y < 10
        if (part == "back") == is_back:
            draw(c, X, Y, r)
