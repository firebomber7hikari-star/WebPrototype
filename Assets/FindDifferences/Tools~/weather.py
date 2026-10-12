# -*- coding: utf-8 -*-
"""
Paper-craft weather effects as animated elements. Each element carries a weather mask, the
runtime (WeatherCycle) fades it in/out with the level's weather sequence and tints the scene.

Masks: build with fdcore.W_(RAIN, THUNDER) etc. Common ones are defined below.
Weather layers are 'untinted' (they keep their own colours instead of darkening with the scene).
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, HEAT, OVERCAST, RAIN, SNOW, THUNDER, W, W_
from paper import Circ, Ell, Poly, RRect, Thick, flat, piece, soft_union, star_pts

WET = W_(RAIN, THUNDER)
CLOUDY = W_(OVERCAST, RAIN, THUNDER)
SUNNY = W_(CLEAR, HEAT)
STORM = W_(THUNDER)
PROP = (2, 4, 7, 0.42)


def _seamless(step, speed):
    sx, sy = step
    ln = math.hypot(sx, sy)
    return dict(driftVelocity=(sx / ln * speed, -sy / ln * speed), driftLength=ln)


# ------------------------------------------------------------------- precipitation
def rain_layer(eid, seed, n, length, width, alpha, speed, mask=WET, step=(48, 128), col=(225, 235, 250)):
    """Diagonal rain streaks; the pattern repeats every `step`, so drifting by one step loops seamlessly."""
    sx, sy = step
    k_range = range(-1, int(H / sy) + 2)

    def d(c, m):
        rnd = random.Random(seed)
        streaks = [(rnd.uniform(-200, W + 200), rnd.uniform(0, sy)) for _ in range(n)]
        for k in k_range:
            for x, y in streaks:
                x0, y0 = x + k * sx, y + k * sy
                flat(c, Thick(x0, y0, x0 + length * sx / sy, y0 + length, width), col + (alpha,))
    bbox = (-200 - sx - 10, -sy - 10, W + 200 + sx * (len(k_range)) + 10, sy * (len(k_range)) + length + 10)
    return E(eid, d, bbox=bbox, anim=_seamless(step, speed), daynight="untinted", weather=mask)


def snow_layer(eid, seed, n, rmin, rmax, speed, sway=8.0, mask=W_(SNOW), alpha=0.95):
    def d(c, m):
        rnd = random.Random(seed)
        flakes = [(rnd.uniform(0, W), rnd.uniform(0, 200), rnd.uniform(rmin, rmax)) for _ in range(n)]
        for k in range(-1, 4):
            for x, y, r in flakes:
                flat(c, Circ(x, y + 200 * k, r), (255, 255, 255, alpha))
    anim = dict(_seamless((0, 200), speed), bobAmplitude=(sway, 0), bobSpeed=0.2)
    return E(eid, d, bbox=(-2, -210, W + 2, 810), anim=anim, daynight="untinted", weather=mask)


def splash_rings(eid, points, mask=WET, col=(225, 238, 252)):
    out = []
    for i, (x, y, r) in enumerate(points):
        def d(c, m, x=x, y=y, r=r):
            c.ellipse_ring(x, y, r, r * 0.45, 1.4, col + (0.85,))
        out.append(E("%s%d" % (eid, i), d, daynight="untinted", weather=mask,
                     anim=dict(driftVelocity=(0, -0.5), driftLength=1.0, driftFade=True, driftGrow=2.2, phase=(i * 0.37) % 1)))
    return out


def puddles(eid, shapes, mask=WET, col=(120, 150, 190), alpha=0.55):
    def d(c, m):
        soft_union(c, shapes, col, alpha, spread=4)
    return E(eid, d, daynight="untinted", weather=mask)


# ------------------------------------------------------------------- sky
def paper_sun(eid, x, y, r=34, mask=SUNNY):
    def d(c, m):
        piece(c, Poly(star_pts(x, y, r * 1.6, r * 1.2, points=12)), (255, 190, 80), shadow=PROP)
        piece(c, Circ(x, y, r), (255, 222, 95), border=2.5, shadow=PROP)
    return E(eid, d, pivot=(x, y), anim=dict(rotateSpeed=-10), daynight="untinted", weather=mask)


def sun_glare(eid, x, y, r=230, mask=W_(HEAT)):
    def d(c, m):
        soft_union(c, [Circ(x, y, r * 0.35)], (255, 245, 200), 0.55, spread=r * 0.65)
    return E(eid, d, pivot=(x, y), anim=dict(pulse=0.06, scaleSpeed=0.25), daynight="untinted", weather=mask)


def cloud_shapes(x, y, k):
    return [Circ(x - 30 * k, y + 10 * k, 22 * k), Circ(x, y, 30 * k), Circ(x + 32 * k, y + 8 * k, 24 * k),
            Circ(x + 60 * k, y + 14 * k, 16 * k), RRect(x - 56 * k, y + 8 * k, x + 80 * k, y + 30 * k, 11 * k)]


def cloud(eid, x, y, k, col, mask, anim=None, shadow=PROP):
    def d(c, m):
        piece(c, cloud_shapes(x, y, k), col, shadow=shadow)
    return E(eid, d, anim=anim or dict(bobAmplitude=(18 * k, 0), bobSpeed=0.03), daynight="untinted", weather=mask)


def lightning(eid, x, y0, y1, interval, phase=0.0, mask=STORM, seed=1):
    rnd = random.Random(seed)
    pts = [(x, y0)]
    y = y0
    while y < y1:
        y += rnd.uniform(18, 34)
        pts.append((x + rnd.uniform(-22, 22), min(y, y1)))

    def d(c, m):
        segs = [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 4) for i in range(len(pts) - 1)]
        soft_union(c, segs, (255, 250, 200), 0.6, spread=10)
        flat(c, segs, (255, 252, 225))
    return E(eid, d, daynight="untinted", weather=mask,
             anim=dict(blinkInterval=interval, blinkDuration=0.35, phase=phase))


def flash(eid, interval, phase=0.0, mask=STORM, alpha=0.45):
    def d(c, m):
        c.rect(0, 0, W, H, (255, 255, 240, alpha))
    return E(eid, d, bbox=(0, 0, W, H), daynight="untinted", weather=mask,
             anim=dict(blinkInterval=interval, blinkDuration=0.35, phase=phase))


# ------------------------------------------------------------------- fog / heat
def fog_layer(eid, seed, y0, y1, alpha, speed, direction=1, mask=W_(FOG), col=(245, 247, 252)):
    step = 300

    def d(c, m):
        rnd = random.Random(seed)
        blobs = [(rnd.uniform(0, step), rnd.uniform(y0, y1), rnd.uniform(60, 120), rnd.uniform(22, 40)) for _ in range(5)]
        shapes = [Ell(x + k * step, y, rx, ry) for k in range(-1, 5) for x, y, rx, ry in blobs]
        soft_union(c, shapes, col, alpha, spread=30)
    return E(eid, d, bbox=(-step - 160, y0 - 90, 4 * step + 160, y1 + 90),
             anim=_seamless((step * direction, 0), speed), daynight="untinted", weather=mask)


def heat_haze(eid, y, amp=4.0, mask=W_(HEAT), alpha=0.22, phase=0.0):
    def d(c, m):
        pts = [(x, y + amp * math.sin(x * 0.05)) for x in range(-40, W + 60, 6)]
        segs = [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 2.2) for i in range(len(pts) - 1)]
        flat(c, segs, (255, 250, 235, alpha))
    return E(eid, d, daynight="untinted", weather=mask,
             anim=dict(bobAmplitude=(10, 3), bobSpeed=0.35, stretch=(0, 0.6), scaleSpeed=0.7, twinkle=0.5, twinkleSpeed=0.5,
                       phase=phase))


def sparkles(eid, points, mask=SUNNY):
    out = []
    for i, (x, y) in enumerate(points):
        def d(c, m, x=x, y=y):
            soft_union(c, [Circ(x, y, 3)], (255, 255, 230), 0.6, spread=5)
            flat(c, Poly(star_pts(x, y, 6, 1.6, points=4, rot=0)), (255, 255, 240))
        out.append(E("%s%d" % (eid, i), d, pivot=(x, y), daynight="untinted", weather=mask,
                     anim=dict(twinkle=0.95, twinkleSpeed=0.5 + (i % 4) * 0.2, pulse=0.3, scaleSpeed=0.6, phase=(i * 0.29) % 1)))
    return out
