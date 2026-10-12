# -*- coding: utf-8 -*-
"""
Shared helpers for the themed level packs (medieval / cyberpunk / anime):
  * sky: sun & moon on a shared orbit for the day/night cycle, star fields
  * small props: smoke puffs, torch flames, window glows, stand-up figures
  * neon: glowing tubes and signs (soft halo + bright core)
  * cel: anime-style cel shading (ink outline, base colour, shade band) instead of paper borders
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, grain, piece, soft_union, star_pts

INK = (45, 38, 58)
PROP = (2, 4, 7, 0.42)
SMALL = (1, 2, 3, 0.3)
LAYER = (1, 3, 11, 0.36)


def drift_across(x_left, x_right, speed, start=0.0):
    """Looping horizontal drift (negative speed = right to left)."""
    if speed >= 0:
        s_min = -(x_right + 10)
        length = W + 10 - x_left - s_min
        return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min,
                    phase=((start - s_min) / length) % 1.0)
    s_min = -(W + 10 - x_left)
    length = x_right + 10 - s_min
    return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min, phase=((start - s_min) / length) % 1.0)


def day_night(period=40.0, tint=(0.30, 0.34, 0.60), phase=0.0):
    return dict(period=period, phase=phase, tint=tint)


# ------------------------------------------------------------------- sky
def celestial(centre, radii, period):
    """Sun (top at t = 0) and moon share one orbit; returns (sun_anim, moon_anim)."""
    base = dict(orbitRadius=radii, orbitSpeed=1.0 / period)
    return dict(base, phase=0.25), dict(base, phase=0.75)


def sun_element(eid, centre, anim, r=30, cel_style=False, mask=0):
    x, y = centre

    def d(c, m):
        if cel_style:
            soft_union(c, [Circ(x, y, r)], (255, 250, 220), 0.6, spread=r * 1.4)
            flat(c, Circ(x, y, r), (255, 252, 235))
        else:
            piece(c, Poly(star_pts(x, y, r * 1.6, r * 1.2, points=12)), (255, 190, 80), shadow=PROP)
            piece(c, Circ(x, y, r), (255, 222, 95), border=2.5, shadow=PROP)
    return E(eid, d, pivot=centre, anim=anim, daynight="day", weather=mask)


def moon_element(eid, centre, anim, r=24, col=(252, 246, 220), mask=0):
    x, y = centre

    def d(c, m):
        soft_union(c, [Circ(x, y, r + 6)], (255, 250, 220), 0.35, spread=r * 0.7)
        piece(c, Circ(x, y, r), col, border=2, shadow=PROP)
        flat(c, [Circ(x - r * 0.3, y - r * 0.25, r * 0.22), Circ(x + r * 0.35, y + r * 0.3, r * 0.16)], lit(col, 0.9))
    return E(eid, d, pivot=centre, anim=anim, daynight="night", weather=mask)


def star_field(eid, seed, n, y_max, avoid=(), col=(255, 248, 210), mask=0):
    def d(c, m):
        rnd = random.Random(seed)
        for _ in range(n):
            x, y = rnd.uniform(8, W - 8), rnd.uniform(8, y_max)
            if any(x0 < x < x1 and y0 < y < y1 for x0, y0, x1, y1 in avoid):
                continue
            r = rnd.choice((2.2, 3, 4.4))
            flat(c, Poly(star_pts(x, y, r, r * 0.35, points=4, rot=0)), col)
    return E(eid, d, daynight="night", weather=mask, anim=dict(twinkle=0.25, twinkleSpeed=0.6))


# ------------------------------------------------------------------- small props
def smoke(prefix, x, y, n=3, col=(240, 236, 232), r=7, show="both", rise=(5, 20), length=60):
    return [E("%s%d" % (prefix, i), (lambda: lambda c, m: piece(c, Circ(x, y, r), col, shadow=SMALL))(), show=show,
              anim=dict(driftVelocity=rise, driftLength=length, driftFade=True, driftGrow=1.2, phase=i / n))
            for i in range(n)]


def flame(eid, x, y, s=1.0, show="both", glow_night=True):
    """Torch / candle flame (always flickering, not darkened at night) + optional night glow element."""
    def d(c, m):
        flat(c, Poly([(x - 6 * s, y), (x + 6 * s, y), (x + 4 * s, y - 8 * s), (x, y - 18 * s), (x - 4 * s, y - 8 * s)]), (255, 150, 50))
        flat(c, Poly([(x - 3 * s, y), (x + 3 * s, y), (x, y - 10 * s)]), (255, 235, 140))
    out = [E(eid, d, pivot=(x, y), show=show, daynight="untinted",
             anim=dict(stretch=(0.1, 0.3), scaleSpeed=4 + (x % 3), twinkle=0.15, twinkleSpeed=3, phase=(x * 0.013) % 1))]
    if glow_night:
        def g(c, m):
            soft_union(c, [Circ(x, y - 8 * s, 6 * s)], (255, 190, 90), 0.55, spread=26 * s)
        out.append(E(eid + "_glow", g, show=show, daynight="night", anim=dict(pulse=0.08, scaleSpeed=1.3, phase=(x * 0.01) % 1)))
    return out


def window_glow(eid, rects, col=(255, 214, 120), show="both", spread=14, mode="night"):
    def d(c, m):
        shapes = [RRect(*r, 1.5) for r in rects]
        soft_union(c, shapes, col, 0.5, spread=spread)
        flat(c, shapes, lit(col, 1.08))
    return E(eid, d, show=show, daynight=mode, anim=dict(twinkle=0.12, twinkleSpeed=0.7))


def figure(c, x, base, body, head=(250, 214, 185), h=1.0, hat=None, border=1.5, shadow=PROP):
    """Simple paper stand-up person facing right; returns head centre."""
    hx, hy = x + 1 * h, base - 40 * h
    piece(c, [Poly([(x - 9 * h, base), (x + 9 * h, base), (x + 6 * h, base - 30 * h), (x - 6 * h, base - 30 * h)]),
              Circ(hx, hy, 7.5 * h)], body, border=border, shadow=shadow)
    flat(c, Circ(hx, hy, 6.2 * h), head)
    flat(c, Circ(hx + 3 * h, hy - 1 * h, 1.1 * h), INK)
    if hat:
        flat(c, Poly([(hx - 9 * h, hy - 4 * h), (hx + 9 * h, hy - 4 * h), (hx, hy - 16 * h)]), hat)
    return hx, hy


# ------------------------------------------------------------------- neon
def neon(c, shapes, col, glow_alpha=0.55, spread=12, core=(255, 255, 255), core_mix=0.55):
    """Glowing tube: wide soft halo, saturated tube, whitish core."""
    soft_union(c, shapes, col, glow_alpha, spread=spread)
    flat(c, shapes, col)
    inner = tuple(int(col[i] + (core[i] - col[i]) * core_mix) for i in range(3))
    for s in shapes:
        s.draw(c, inner, -1.2)


def neon_glyphs(x, y, w, h, n, seed, width=3.0):
    """Abstract sign 'characters' made of strokes (no font needed)."""
    rnd = random.Random(seed)
    out = []
    cw = w / n
    for k in range(n):
        x0 = x + k * cw + cw * 0.15
        x1 = x + (k + 1) * cw - cw * 0.15
        ym = y + h / 2
        kind = rnd.randint(0, 4)
        if kind == 0:
            out += [Thick(x0, y, x1, y, width), Thick((x0 + x1) / 2, y, (x0 + x1) / 2, y + h, width), Thick(x0, y + h, x1, y + h, width)]
        elif kind == 1:
            out += [Thick(x0, y, x0, y + h, width), Thick(x0, ym, x1, ym, width), Thick(x1, y, x1, y + h, width)]
        elif kind == 2:
            out += [Thick(x0, y, x1, y + h, width), Thick(x1, y, x0, y + h, width)]
        elif kind == 3:
            out += [Thick(x0, y, x1, y, width), Thick(x1, y, x1, y + h, width), Thick(x0, ym, x1, ym, width), Thick(x0, y + h, x1, y + h, width)]
        else:
            out += [Thick(x0, y + h, (x0 + x1) / 2, y, width), Thick((x0 + x1) / 2, y, x1, y + h, width), Thick(x0, ym, x1, ym, width)]
    return out


def neon_post(rows, w, h, ox, oy, has_alpha):
    grain(rows, w, h, ox, oy, has_alpha, strength=0.6, vignette=not has_alpha)


# ------------------------------------------------------------------- anime cel shading
def cel(c, shapes, col, shade=None, ink=INK, w=2.2, shade_off=(3.0, 3.5), highlight=None):
    """Ink outline + flat base + a shade band on the lower-right edge (light from the upper left)."""
    if not isinstance(shapes, (list, tuple)):
        shapes = [shapes]
    shade = shade or lit(col, 0.78)
    for s in shapes:
        s.draw(c, ink, w)
    for s in shapes:
        s.draw(c, shade)
    for s in shapes:
        s.draw(c, col, -shade_off[0] * 0.5, -shade_off[0], -shade_off[1])
    if highlight:
        for s in shapes:
            s.draw(c, highlight, -min(6.0, shade_off[0] * 2.2), -shade_off[0] * 2, -shade_off[1] * 2)


def cel_flat(c, shapes, col, ink=INK, w=2.0):
    if not isinstance(shapes, (list, tuple)):
        shapes = [shapes]
    for s in shapes:
        s.draw(c, ink, w)
    for s in shapes:
        s.draw(c, col)


def cumulus(c, x, y, k, base=(255, 255, 255), shade=(196, 210, 236), ink=None):
    """Anime cumulus: big rounded puffs, flat white top, blue-grey shaded underside."""
    puffs = [(0, 0, 60), (-70, 30, 44), (72, 26, 50), (-30, -40, 42), (36, -48, 46), (120, 50, 36), (-118, 56, 30)]
    shapes = [Circ(x + dx * k, y + dy * k, r * k) for dx, dy, r in puffs]
    shapes.append(RRect(x - 140 * k, y + 30 * k, x + 150 * k, y + 80 * k, 24 * k))
    if ink:
        for s in shapes:
            s.draw(c, ink, 2)
    for s in shapes:
        s.draw(c, shade)
    for s in shapes:
        s.draw(c, base, -6 * k, -8 * k, -14 * k)


def anime_post(rows, w, h, ox, oy, has_alpha):
    grain(rows, w, h, ox, oy, has_alpha, strength=0.3, vignette=False)
