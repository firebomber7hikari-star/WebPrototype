# -*- coding: utf-8 -*-
"""Realistic open-world crime-city levels (sun-drenched coastal metropolis mood; every car, sign and building is an
original design - no real brands, logos, readable text, landmarks or violence):
  Level1595 日落大道   - a palm-lined boulevard into the sunset: cars, billboard, traffic lights
  Level1596 公路加油站 - a desert highway gas station: canopy, pumps, store, pickup truck, mountains
  Level1597 高速追逐   - a night freeway chase: sports car, police cruisers, helicopter searchlight
  Level1598 海滨栈桥   - a beach pier at sunset: Ferris wheel, lifeguard tower, umbrellas, surfers
  Level1599 霓虹夜街   - a rainy neon strip: wet reflections, glowing signs, taxi, fire escapes
  Level1600 改装车库   - a custom garage: car on a lift, tool wall, tyre stacks, neon tubes
  Level1601 港口货柜   - container docks at dusk: gantry crane, cargo ship, forklift
  Level1602 沙漠拖车   - a desert trailer camp at dusk: trailer, old car, dish, cacti, power poles
  Level1603 豪宅泳池   - a hillside villa with an infinity pool above the city at sunset
  Level1604 城市夜景   - a hilltop overlook of the downtown skyline at dusk, a sports car parked
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (C, Box, Circ, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm, fbm1,
                  grain_tex, hgrad, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint, tex, vgrad)
from real_kit import cloud_layer, cumulus, figure, mist_el, ridge, sky, stars, sun, water, ripples_light, glint_el, bird_el
from levels_real3 import flat_bg
from levels_real2 import make_bg, moon_receive
from weather import rain_layer

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)
SUNSET = [(0, (40, 60, 120)), (150, (150, 110, 140)), (260, (250, 150, 100)), (330, (255, 200, 130))]


def rcv(f, x):
    return float(f(np.array([x], np.float32))[0])


# =================================================================== realistic city kit
def car(g, x, base, L, col, kind="sedan", face=1, lights=False, tail=False, police=False, seed=0, glass=None):
    """Side-view car with metallic paint, sky-reflecting glass, alloy wheels (no badges)."""
    f = face
    h = L * 0.3

    def P(pts):
        return Poly([(x + f * (px - x), py) for px, py in pts])
    if kind == "sport":
        body = P([(x - L / 2, base - h * 0.3), (x - L / 2 + 4, base - h * 0.8), (x - L * 0.14, base - h * 0.92), (x + L * 0.06, base - h * 1.3),
                  (x + L * 0.28, base - h * 1.28), (x + L / 2, base - h * 0.72), (x + L / 2, base - h * 0.3)])
        win = P([(x - L * 0.06, base - h * 0.96), (x + L * 0.08, base - h * 1.24), (x + L * 0.27, base - h * 1.22), (x + L * 0.34, base - h * 0.96)])
    elif kind == "pickup":
        body = Union([Box(x - L / 2, base - h * 1.0, x + L / 2, base - h * 0.3, 4),
                      P([(x + L * 0.0, base - h), (x + L * 0.05, base - h * 1.72), (x + L * 0.3, base - h * 1.72), (x + L * 0.38, base - h)])])
        win = P([(x + L * 0.08, base - h * 1.62), (x + L * 0.28, base - h * 1.62), (x + L * 0.33, base - h * 1.08), (x + L * 0.08, base - h * 1.08)])
    elif kind == "van":
        body = P([(x - L / 2, base - h * 0.3), (x - L / 2, base - h * 1.8), (x + L * 0.25, base - h * 1.8), (x + L / 2, base - h * 1.0), (x + L / 2, base - h * 0.3)])
        win = P([(x + L * 0.08, base - h * 1.66), (x + L * 0.24, base - h * 1.66), (x + L * 0.42, base - h * 1.1), (x + L * 0.08, base - h * 1.1)])
    else:
        body = P([(x - L / 2, base - h * 0.3), (x - L / 2 + 4, base - h * 0.95), (x - L * 0.22, base - h), (x - L * 0.1, base - h * 1.6),
                  (x + L * 0.2, base - h * 1.6), (x + L * 0.32, base - h * 1.0), (x + L / 2, base - h * 0.9), (x + L / 2, base - h * 0.3)])
        win = P([(x - L * 0.08, base - h * 1.5), (x + L * 0.18, base - h * 1.5), (x + L * 0.28, base - h * 1.04), (x - L * 0.17, base - h * 1.04)])
    g.mul(Ell(x, base + 1, L * 0.56, 6), 0.6, feather=6)
    top = base - h * 1.8

    def paint(X, Y):
        t = np.clip((Y - top) / (base - top), 0, 1)
        k = 1.25 - 0.6 * t + 0.35 * np.exp(-((t - 0.52) / 0.05) ** 2)
        return C(col) * (k * (0.97 + 0.06 * fbm(X, Y, 30, 6, 2, seed)))[..., None]
    g.fill(body, paint, feather=0.6)
    g.fill(win, glass or lgrad(0, top, 0, base - h, [(0, (190, 210, 230)), (0.6, (60, 70, 90)), (1, (30, 34, 44))]), feather=0.5)
    g.add(Seg(x - L * 0.42, base - h * 0.62, x + L * 0.42, base - h * 0.62, 0.8), (255, 255, 255), 0.15)
    if police:
        g.fill(Box(x - L / 2 + 3, base - h * 0.76, x + L / 2 - 3, base - h * 0.56), (240, 240, 240))
        g.fill(Box(x - L * 0.1, base - h * 1.78, x, base - h * 1.62, 2), (230, 40, 40))
        g.fill(Box(x, base - h * 1.78, x + L * 0.1, base - h * 1.62, 2), (40, 80, 240))
    hx = x + f * (L / 2 - 8)
    g.fill(Ell(hx, base - h * 0.66, 6, 4), (255, 245, 220))
    tx = x - f * (L / 2 - 5)
    g.fill(Ell(tx, base - h * 0.7, 4, 4), (200, 30, 30))
    if lights:
        g.glow(hx + f * 20, base - h * 0.6, 70, (255, 240, 210), 0.35)
    if tail:
        g.glow(tx, base - h * 0.7, 26, (255, 40, 40), 0.6)
    for wx in (x - L * 0.3, x + L * 0.3):
        g.fill(Circ(wx, base - h * 0.28, h * 0.34), (24, 24, 26))
        g.fill(Circ(wx, base - h * 0.28, h * 0.2), sphere_paint(wx - 2, base - h * 0.32, h * 0.2, (170, 172, 178), amb=0.4, spec=0.7))
        for a in range(5):
            aa = a * math.tau / 5
            g.fill(Seg(wx, base - h * 0.28, wx + math.cos(aa) * h * 0.18, base - h * 0.28 + math.sin(aa) * h * 0.18, 1.2), (90, 90, 96))
    return body


def asphalt(g, shape, base=(70, 70, 76), seed=0, wet=False):
    g.fill(shape, grain_tex(lambda X, Y: C(base) * (0.8 + 0.3 * fbm(X, Y, 3, 3, 3, seed) + 0.1 * fbm(X, Y, 60, 30, 2, seed + 1))[..., None], 0.08, seed + 2))


def palm(g, x, base, h, lean=0.12, seed=0, col=(40, 70, 40), trunk=(120, 96, 72), sil=False):
    """Tall fan palm (washingtonia-like): thin ringed trunk, ragged crown. sil=True draws a dark silhouette."""
    tx, ty = x + lean * h, base - h
    tpaint = trunk if sil else tex(light_x(trunk, x - 6, x + 6, 1.3, 0.6), 0.2, 1.5, 3, 3, seed)
    for i in range(14):
        t0, t1 = i / 14, (i + 1) / 14
        g.fill(Seg(x + lean * h * t0 ** 1.5, base - h * t0, x + lean * h * t1 ** 1.5, base - h * t1, h * 0.022 * (1.2 - t0 * 0.5) + 1), tpaint)
    rnd = random.Random(seed)
    leaves = []
    for k in range(16):
        a = -math.pi + k * math.pi / 15 + rnd.uniform(-0.1, 0.1)
        ln = h * rnd.uniform(0.16, 0.24)
        ex, ey = tx + math.cos(a) * ln, ty + math.sin(a) * ln * 0.55 + ln * 0.35
        leaves.append(Seg(tx, ty, ex, ey, h * 0.012 + 1.2, 0.6))
        for j in range(3):
            t = 0.4 + j * 0.2
            px, py = tx + (ex - tx) * t, ty + (ey - ty) * t
            leaves.append(Seg(px, py, px + math.cos(a + 0.6) * ln * 0.18, py + math.sin(a + 0.6) * ln * 0.18 + 3, 1.0, 0.4))
            leaves.append(Seg(px, py, px + math.cos(a - 0.6) * ln * 0.18, py + math.sin(a - 0.6) * ln * 0.18 + 3, 1.0, 0.4))
    crown = Union(leaves + [Ell(tx, ty + h * 0.04, h * 0.05, h * 0.07)])
    g.fill(crown, col if sil else lambda X, Y: C(col) * (0.7 + 0.6 * fbm(X, Y, 3, 3, 3, seed + 1))[..., None])


def tower(g, x0, x1, top, base, col, seed=0, glass=True, lit=None, lit_p=0.0, cols=None, rows=None, sky_top=(150, 170, 210), sky_bot=(250, 190, 140)):
    """Office tower: reflective glass curtain wall (window grid) or concrete with punched windows."""
    s = Box(x0, top, x1, base)
    rnd = random.Random(seed)
    if glass:
        g.fill(s, lambda X, Y: (C(sky_top) + (C(sky_bot) - C(sky_top)) * np.clip((Y - top) / max(1, base - top), 0, 1)[..., None]) * 0.55 + C(col) * 0.45)
        g.fill(s, (0, 0, 0), alpha=lambda X, Y: 0.25 * smooth(x0, x1, X))
        cw = (x1 - x0) / (cols or max(3, int((x1 - x0) / 9)))
        mull = [Box(x, top, x + 1.2, base) for x in np.arange(x0, x1, cw)] + [Box(x0, y, x1, y + 1.2) for y in np.arange(top, base, 8)]
        g.fill(Union(mull), mixc(col, (0, 0, 0), 0.5), alpha=0.7)
    else:
        g.fill(s, tex(light_x(col, x0, x1, 1.15, 0.7), 0.1, 6, 6, 3, seed))
    if lit is not None:
        wins = []
        for y in np.arange(top + 6, base - 6, 8):
            for x in np.arange(x0 + 3, x1 - 4, 6):
                if rnd.random() < lit_p:
                    wins.append(Box(x, y, x + 3.4, y + 4))
        if wins:
            g.fill(Union(wins), lit)
    return s


def stucco(g, x0, x1, top, base, col, seed=0, light=-1):
    s = Box(x0, top, x1, base)
    g.fill(s, tex(light_x(col, x0, x1, *((1.15, 0.75) if light < 0 else (0.75, 1.15))), 0.08, 4, 4, 3, seed))
    return s


def window(g, x0, y0, x1, y1, lit=None, frame=(240, 236, 228), glass=((170, 190, 210), (70, 80, 96))):
    g.fill(Box(x0 - 2, y0 - 2, x1 + 2, y1 + 2), frame)
    if lit:
        g.glow((x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) * 1.6, lit, 0.25)
        g.fill(Box(x0, y0, x1, y1), lit)
    else:
        g.fill(Box(x0, y0, x1, y1), lgrad(0, y0, 0, y1, [(0, glass[0]), (1, glass[1])]))


def neon(g, shape, col, k=1.0, on=True):
    """Glowing neon tube outline of a shape (abstract sign, no text)."""
    if not on:
        g.fill(Ring(shape, 1.6), mixc(col, (40, 40, 50), 0.75))
        return
    b = shape.bbox()
    g.glow((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, max(b[2] - b[0], b[3] - b[1]) * 0.9, col, 0.25 * k)
    g.fill(Ring(shape, 2.6), col, alpha=0.5)
    g.fill(Ring(shape, 1.2), mixc(col, (255, 255, 255), 0.6))


class Ring:
    """Outline band of width w around a shape boundary."""

    def __init__(self, s, w):
        self.s, self.w = s, w

    def bbox(self):
        b = self.s.bbox()
        return (b[0] - self.w, b[1] - self.w, b[2] + self.w, b[3] + self.w)

    def sdf(self, X, Y):
        return np.abs(self.s.sdf(X, Y)) - self.w


def billboard(g, x0, y0, x1, y1, art, seed=0, lit=False):
    """Roadside billboard on posts with an abstract graphic: art(g, x0, y0, x1, y1)."""
    for px in (x0 + (x1 - x0) * 0.25, x0 + (x1 - x0) * 0.75):
        g.fill(Box(px - 4, y1, px + 4, y1 + (y1 - y0) * 1.4), light_x((90, 90, 96), px - 4, px + 4, 1.3, 0.6))
    g.fill(Box(x0 - 4, y0 - 4, x1 + 4, y1 + 4), (60, 60, 66))
    art(g, x0, y0, x1, y1)
    g.fill(Box(x0, y1 + 6, x1, y1 + 9), (80, 80, 86))
    if lit:
        for lx in np.linspace(x0 + 20, x1 - 20, 3):
            g.glow(lx, y0 + 6, 30, (255, 240, 200), 0.3)


def art_sunset(g, x0, y0, x1, y1, a=(250, 130, 80), b=(80, 40, 140)):
    g.fill(Box(x0, y0, x1, y1), lgrad(0, y0, 0, y1, [(0, b), (1, a)]))
    g.fill(Inter(Circ((x0 + x1) / 2, y1, (y1 - y0) * 0.6), Box(x0, y0, x1, y1)), (255, 220, 120))
    for i in range(3):
        g.fill(Box(x0, y1 - (y1 - y0) * (0.12 + i * 0.1), x1, y1 - (y1 - y0) * (0.08 + i * 0.1)), b, alpha=0.6)


def art_bars(g, x0, y0, x1, y1, a=(40, 160, 220), b=(250, 250, 250)):
    g.fill(Box(x0, y0, x1, y1), a)
    for i in range(3):
        g.fill(Box(x0 + 14, y0 + 12 + i * 16, x0 + (x1 - x0) * (0.7 - i * 0.15), y0 + 20 + i * 16, 3), b)
    g.fill(Circ(x1 - (y1 - y0) * 0.45, (y0 + y1) / 2, (y1 - y0) * 0.32), (250, 210, 60))


def traffic_light(g, x, base, h, state="green", arm=0):
    g.fill(Box(x - 3, base - h, x + 3, base), light_x((70, 72, 78), x - 3, x + 3, 1.3, 0.6))
    hx = x + arm
    if arm:
        g.fill(Seg(x, base - h + 6, hx, base - h + 6, 2.4), (70, 72, 78))
    g.fill(Box(hx - 9, base - h - 4, hx + 9, base - h + 46, 3), (40, 40, 44))
    for i, (st, col) in enumerate((("red", (255, 50, 40)), ("amber", (255, 180, 40)), ("green", (60, 230, 120)))):
        cy = base - h + 6 + i * 14
        on = st == state
        g.fill(Circ(hx, cy, 5), col if on else mixc(col, (30, 30, 30), 0.8))
        if on:
            g.glow(hx, cy, 22, col, 0.5)


def street_light(g, x, base, h, face=1, lit=True, col=(255, 220, 160)):
    g.fill(Box(x - 3, base - h, x + 3, base), light_x((90, 92, 98), x - 3, x + 3, 1.3, 0.6))
    g.fill(Seg(x, base - h, x + face * 40, base - h - 6, 2.4), (90, 92, 98))
    g.fill(Ell(x + face * 42, base - h - 4, 12, 4), (60, 60, 64))
    if lit:
        g.glow(x + face * 42, base - h, 60, col, 0.4)
        g.fill(Ell(x + face * 42, base - h - 2, 9, 2.4), (255, 250, 230))


def hydrant(g, x, base, col=(200, 40, 40)):
    g.fill(Union([Box(x - 7, base - 30, x + 7, base, 3), Ell(x, base - 30, 8, 5), Box(x - 12, base - 22, x + 12, base - 16, 2)]),
           cyl_paint(x, 9, col, amb=0.35, spec=0.5))


def person(g, x, base, h, coat, seed=0, face_right=True, hat=None, skin=(200, 160, 130), hair=(40, 30, 26)):
    figure(g, x, base, h, coat, skin=skin, hair=hair, face_right=face_right, hat=hat)



# =================================================================== Level 1595 sunset boulevard
SUN95 = (450, 300, 26)


def l1595_scene(g, d):
    sky(g, SUNSET)
    cloud_layer(g, 60, 200, (255, 170, 140), (120, 80, 120), cover=0.4, sx=220, sy=16, seed=9501, alpha=0.7)
    sun(g, *SUN95, col=(255, 236, 190), halo=(255, 160, 90), k=0.9)
    ridge(g, 330, 40, 200, 9502, (120, 80, 110), ridged=False, light=False, haze=((250, 160, 120), 0.5, 0.3))
    # low commercial buildings along both sides (receding)
    for side in (-1, 1):
        for i in range(6):
            t0, t1 = i / 6, (i + 1) / 6
            xa = 450 + side * (460 - 400 * t0 ** 0.8)
            xb = 450 + side * (460 - 400 * t1 ** 0.8)
            hh = (220 - 180 * t0 ** 0.8)
            col = [(170, 120, 110), (140, 110, 130), (180, 140, 110), (120, 100, 110)][(i + (side > 0)) % 4]
            y0b, y1b = 330 + (280 - 280 * t0 ** 0.8) * 0.3 - hh * 0.6, 330 + (280 - 280 * t0 ** 0.8) * 0.75
            stucco(g, min(xa, xb), max(xa, xb), y0b, y1b, col, seed=9503 + i * 3 + side, light=side)
            ww = abs(xb - xa)
            for r_ in range(2):
                wy = y0b + (y1b - y0b) * (0.2 + r_ * 0.35)
                g.fill(Box(min(xa, xb) + ww * 0.15, wy, max(xa, xb) - ww * 0.15, wy + (y1b - y0b) * 0.18), (255, 200, 150) if (i + r_) % 3 == 0 else (60, 50, 70))
    # road, sidewalks, lane markings
    asphalt(g, Poly([(-20, 610), (920, 610), (470, 330), (430, 330)]), seed=9510)
    for side in (-1, 1):
        g.fill(Poly([(450 + side * 40 * 0.5, 330), (450 + side * 30, 330), (450 + side * 520, 610), (450 + side * 470, 610)]), (190, 180, 170))
    for k in range(9):
        t0, t1 = (k + 0.2) / 9, (k + 0.6) / 9
        y0, y1 = 330 + 280 * t0 ** 1.6, 330 + 280 * t1 ** 1.6
        g.fill(Poly([(449 - t0 ** 1.6 * 4, y0), (451 + t0 ** 1.6 * 4, y0), (451 + t1 ** 1.6 * 4, y1), (449 - t1 ** 1.6 * 4, y1)]), (240, 210, 90))
    g.add(Poly([(380, 610), (520, 610), (460, 330), (440, 330)]), (255, 190, 120), 0.18, feather=30)
    # palms along both kerbs, receding
    for side in (-1, 1):
        for i, t_ in enumerate((0.0, 0.3, 0.52, 0.68, 0.8)):
            if "palm" in d and side == 1 and i == 3:
                continue
            x = 450 + side * (430 - 400 * t_)
            base = 610 - 280 * t_ ** 0.9
            palm(g, x, base, 380 * (1 - t_ * 0.85), lean=0.06 * side, seed=9520 + i * 2 + side, col=(30, 40, 40), trunk=(60, 46, 50), sil=True)
    # billboard (left)
    billboard(g, 70, 150, 250, 230, (lambda g, *b: art_sunset(g, *b)) if "billboard" not in d else (lambda g, *b: art_bars(g, *b)), seed=9530)
    # traffic light (right) and street sign
    traffic_light(g, 700, 470, 200, state="green" if "light" not in d else "red", arm=-60)
    if "sign" not in d:
        g.fill(Box(560, 300, 620, 314, 2), (40, 120, 70))
        g.fill(Box(568, 305, 610, 309, 1), (230, 240, 230))
    # cars
    car(g, 520, 520, 170, (190, 30, 40), kind="sedan", face=-1, tail=True, seed=9540)
    car(g, 330, 450, 110, (40, 60, 120) if "car" not in d else (230, 230, 230), kind="sedan", face=1, lights=True, seed=9541)
    car(g, 470, 380, 60, (60, 60, 64), kind="van", face=-1, seed=9542)
    if "hydrant" not in d:
        hydrant(g, 800, 590)
    person(g, 120, 600, 120, (60, 110, 160), seed=9550)
    person(g, 160, 596, 112, (220, 90, 80), seed=9551, face_right=False)
    g.fog(260, 340, (250, 170, 130), 0.0, 0.2)


L1595_RAYS = [dict(lx=SUN95[0], ly=SUN95[1], col=(255, 190, 130), k=0.7, region=Box(-2, -2, W + 2, 330), threshold=170,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=moon_receive(*SUN95, floor=0.3))]
L1595_EL = [bird_el("b1", 300, 100, s=6, speed=18), bird_el("b2", 320, 110, s=5, speed=18, phase=0.05),
            glint_el("glint", [(520, 470), (600, 485)], col=(255, 240, 210), r=6, speed=0.4)]
L1595_DIFFS = [("billboard", 160, 190, 0), ("palm", 770, 200, 0), ("light", 640, 290, 0), ("sign", 590, 307, 0), ("car", 330, 430, 0),
               ("hydrant", 800, 570, 0)]


# =================================================================== Level 1596 desert gas station
def l1596_scene(g, d):
    sky(g, [(0, (80, 140, 210)), (250, (210, 200, 190)), (300, (250, 200, 150))])
    cloud_layer(g, 40, 140, (255, 240, 230), (190, 170, 170), cover=0.35, sx=200, sy=20, seed=9601, alpha=0.7)
    ridge(g, 300, 90, 220, 9602, (170, 120, 100), ridged=True, light=True, haze=((230, 190, 160), 0.5, 0.2))
    g.fill(Box(-2, 300, W + 2, H + 2), tex(vgrad([(300, (210, 180, 140)), (600, (180, 150, 110))]), 0.25, 6, 3, 4, 9603))
    asphalt(g, Box(-2, 520, W + 2, H + 2), seed=9604)
    for x in range(-20, 900, 90):
        g.fill(Box(x, 560, x + 50, 566), (240, 220, 120))
    g.fill(Box(-2, 360, W + 2, 520), (150, 146, 140))
    # store
    stucco(g, 560, 880, 230, 400, (230, 220, 200), seed=9605)
    for i, x in enumerate((580, 660, 740)):
        window(g, x, 300, x + 64, 380, lit=(255, 240, 200) if i != 1 else None)
    g.fill(Box(820, 300, 862, 400), (90, 80, 70))
    g.fill(Box(556, 224, 884, 236), (180, 50, 50))
    neon(g, Poly([(720 + math.cos(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9), 265 + math.sin(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9)) for k in range(10)]),
         (255, 90, 120), on="neon" not in d)
    # canopy over the pumps
    g.mul(Box(60, 380, 520, 420), 0.4, feather=14)
    for x in (90, 480):
        g.fill(Box(x - 8, 250, x + 8, 400), cyl_paint(x, 8, (220, 220, 225), amb=0.4, spec=0.2))
    g.fill(Box(40, 200, 540, 250), lgrad(0, 200, 0, 250, [(0, (245, 245, 245)), (1, (200, 200, 205))]))
    g.fill(Box(40, 232, 540, 246), (40, 110, 200))
    for x in range(80, 520, 70):
        g.fill(Box(x, 250, x + 30, 254), (255, 250, 230))
    # pumps
    for i, x in enumerate((170, 290, 410)):
        g.mul(Ell(x + 6, 402, 30, 5), 0.5, feather=5)
        g.fill(Box(x - 22, 300, x + 22, 400, 3), light_x((235, 235, 235), x - 22, x + 22, 1.15, 0.75))
        g.fill(Box(x - 16, 312, x + 16, 334, 2), (40, 60, 70))
        hose = (220, 60, 50) if not (i == 2 and "pump" in d) else (40, 140, 90)
        g.fill(Box(x - 22, 300, x + 22, 312), hose)
        g.fill(Box(x - 22, 380, x + 22, 392), hose)
        g.fill(Seg(x + 22, 340, x + 30, 380, 2.4), (30, 30, 30))
        g.fill(Box(x + 24, 336, x + 34, 352, 2), hose)
    # tall pole sign with an abstract mark
    g.fill(Box(26, 40, 34, 250), light_x((120, 120, 126), 26, 34, 1.3, 0.6))
    sg = Box(-6, 40, 66, 110, 6)
    g.fill(sg, lgrad(0, 40, 0, 110, [(0, (250, 250, 250)), (1, (220, 220, 225))]))
    g.fill(Circ(30, 75, 24), (240, 140, 40) if "pole" not in d else (60, 170, 90))
    g.fill(Poly([(14, 84), (30, 58), (46, 84)]), (255, 255, 255))
    # pickup truck at the pump and props
    car(g, 300, 470, 220, (120, 40, 30), kind="pickup", face=1, seed=9610)
    for k in range(4 if "tyres" not in d else 2):
        g.fill(Ell(640, 506 - k * 14, 30, 9), (30, 30, 32))
        g.fill(Ell(640, 504 - k * 14, 14, 4), (60, 60, 64))
    if "bin" not in d:
        g.fill(Box(500, 440, 530, 500, 3), cyl_paint(515, 15, (40, 90, 60), amb=0.35, spec=0.3))
    g.fill(Box(720, 440, 790, 500, 3), lgrad(720, 0, 790, 0, [(0, (250, 250, 255)), (1, (180, 190, 210))]))
    g.fill(Box(724, 446, 786, 470, 2), (120, 180, 230))
    person(g, 430, 500, 120, (200, 200, 190), hat=(150, 110, 70), seed=9611)


L1596_EL = [mist_el("heat", 450, 300, 500, 8, (240, 210, 180), alpha=0.25, length=60, seed=96),
            E("tumble", el(lambda g, m: g.fill(Rough(Circ(820, 560, 16), 3, 4, 9620), (150, 120, 80), alpha=0.8)), pivot=(820, 560),
              anim=dict(driftVelocity=(-60, 0), driftLength=1000, driftStart=-100, rotateSpeed=-200))]
L1596_DIFFS = [("neon", 720, 265, 0), ("pump", 410, 320, 0), ("pole", 30, 75, 0), ("tyres", 640, 470, 0),
               ("bin", 515, 470, 0)]


# =================================================================== Level 1597 night freeway chase
def l1597_scene(g, d):
    sky(g, [(0, (8, 10, 24)), (220, (30, 30, 60)), (320, (70, 50, 70))])
    stars(g, 40, 160, seed=9701)
    # skyline far away
    rnd = random.Random(9702)
    x = -10
    while x < 910:
        w = rnd.uniform(26, 60)
        h = rnd.uniform(60, 200)
        tower(g, x, x + w, 320 - h, 320, (30, 34, 50), seed=int(x) + 9703, glass=False, lit=(255, 214, 150), lit_p=0.18)
        x += w + rnd.uniform(2, 8)
    if "beacon" not in d:
        g.fill(Box(598, 60, 612, 140), (40, 44, 60))
        g.fill(Seg(605, 60, 605, 30, 1.6), (60, 64, 80))
        g.glow(605, 30, 16, (255, 60, 60), 0.9)
    g.fog(240, 330, (80, 60, 80), 0.0, 0.4)
    # elevated freeway deck
    asphalt(g, Box(-2, 380, W + 2, 520), seed=9704)
    g.fill(Box(-2, 360, W + 2, 384), lgrad(0, 360, 0, 384, [(0, (150, 150, 156)), (1, (90, 90, 96))]))
    g.fill(Box(-2, 520, W + 2, 540), (110, 110, 116))
    g.fill(Box(-2, 540, W + 2, H + 2), vgrad([(540, (30, 30, 40)), (600, (10, 10, 16))]))
    for x in range(40, 900, 220):
        g.fill(Box(x, 540, x + 40, H + 2), light_x((70, 70, 78), x, x + 40, 1.2, 0.6))
    for x in range(-20, 900, 80):
        g.fill(Box(x, 446, x + 40, 452), (220, 220, 200))
    for x in (120, 520):
        street_light(g, x, 362, 160, face=1)
    # overhead sign gantry with abstract arrows
    g.fill(Union([Box(700, 160, 708, 362), Box(890, 160, 898, 362), Box(696, 168, 902, 176)]), (120, 122, 130))
    g.fill(Box(716, 180, 884, 240, 4), (30, 110, 70))
    g.fill(Ring(Box(716, 180, 884, 240, 4), 1.2), (230, 240, 230))
    ax = 800
    if "arrow" not in d:
        g.fill(Union([Box(ax - 4, 200, ax + 4, 232), Poly([(ax - 14, 204), (ax, 186), (ax + 14, 204)])]), (240, 240, 240))
    else:
        g.fill(Union([Seg(ax - 2, 232, ax + 14, 196, 4), Poly([(ax + 4, 196), (ax + 20, 186), (ax + 22, 206)])]), (240, 240, 240))
    g.fill(Box(740, 196, 776, 204, 2), (240, 240, 240))
    # the getaway sports car and the police
    car(g, 640, 470, 200, (220, 30, 30), kind="sport", face=1, lights=True, tail=True, seed=9710)
    if "spoiler" not in d:
        g.fill(Union([Box(534, 410, 584, 420, 2), Seg(546, 420, 552, 436, 3), Seg(574, 420, 572, 436, 3)]), (30, 30, 34))
    for x, s in ((330, 9711), (120, 9712)):
        car(g, x, 476 if x == 330 else 430, 180 if x == 330 else 150, (20, 22, 30), kind="sedan", face=1, lights=True, police=True, seed=s)
    lx = 330 - 18 + 9
    g.glow(lx, 410, 60, (255, 40, 40) if "siren" not in d else (60, 90, 255), 0.6)
    g.glow(lx + 18, 410, 60, (40, 80, 255), 0.6)
    for k in range(5):
        g.add(Seg(420 - k * 30, 430 + k * 8, 480 - k * 30, 430 + k * 8, 1.2), (255, 255, 255), 0.25)
    # traffic cones knocked on the shoulder
    for i, x in enumerate((850, 880)):
        if "cone" in d and i == 1:
            continue
        g.fill(Poly([(x - 13, 532), (x, 490), (x + 13, 532)]), lgrad(x - 13, 0, x + 13, 0, [(0, (255, 140, 40)), (1, (200, 80, 20))]))
        g.fill(Box(x - 7, 508, x + 7, 514), (250, 250, 250))


def l1597_heli(g, m):
    hx, hy = 220, 120
    g.fill(Poly([(hx + 20, hy + 20), (hx + 140, hy + 330), (hx + 420, hy + 330), (hx + 40, hy + 18)]), (220, 230, 255), alpha=lambda X, Y: 0.14 * np.clip(1 - (Y - hy) / 360, 0, 1), feather=20)
    g.fill(Union([Ell(hx, hy, 36, 16), Seg(hx + 20, hy - 4, hx + 90, hy - 10, 6, 3), Box(hx + 82, hy - 24, hx + 92, hy - 8)]), (30, 32, 40))
    g.fill(Ell(hx - 14, hy - 2, 16, 10), (90, 120, 160))
    g.fill(Union([Seg(hx - 20, hy + 20, hx + 24, hy + 20, 1.6), Seg(hx - 12, hy + 14, hx - 12, hy + 20, 1.4), Seg(hx + 14, hy + 14, hx + 14, hy + 20, 1.4)]), (30, 32, 40))
    g.fill(Seg(hx - 70, hy - 20, hx + 70, hy - 22, 1.6), (60, 60, 70))
    g.glow(hx + 30, hy + 16, 20, (255, 255, 230), 0.8)


L1597_EL = [E("heli", el(l1597_heli), pivot=(220, 120), anim=dict(bobAmplitude=(10, 4), bobSpeed=0.12)),
            E("blink", el(lambda g, m: g.glow(312, 410, 30, (255, 255, 255), 0.6)), daynight="untinted", anim=dict(blinkInterval=0.8, blinkDuration=0.2)),
            glint_el("city", [(100, 260), (300, 230), (700, 250), (860, 270)], col=(255, 230, 180), r=4, speed=0.5)]
L1597_DIFFS = [("beacon", 605, 50, 0), ("arrow", 800, 210, 0), ("spoiler", 562, 426, 0), ("siren", 321, 410, 0), ("cone", 880, 515, 0)]


# =================================================================== Level 1598 beach pier at sunset
SUN98 = (300, 250, 24)


def l1598_scene(g, d):
    sky(g, [(0, (60, 80, 150)), (180, (220, 140, 140)), (280, (255, 190, 120))])
    cloud_layer(g, 60, 190, (255, 180, 150), (140, 90, 120), cover=0.4, sx=220, sy=18, seed=9801, alpha=0.7)
    sun(g, *SUN98, col=(255, 236, 190), halo=(255, 160, 90), k=0.5)
    water(g, 290, 440, (220, 150, 120), (60, 80, 120), seed=9802)
    ripples_light(g, 300, 440, (255, 200, 140), k=0.6, cx=300, spread=80, seed=9803)
    # pier (right) with a Ferris wheel and a roller-coaster silhouette
    deck = Box(420, 300, 920, 316)
    for x in range(430, 920, 30):
        g.fill(Box(x, 316, x + 5, 440), (50, 40, 50))
    g.fill(deck, light_y((90, 70, 70), 300, 316, 1.3, 0.7))
    cx, cy, r = 700, 190, 100
    g.fill(Diff(Circ(cx, cy, r), Circ(cx, cy, r - 4)), (50, 40, 60))
    for a in range(12):
        aa = a * math.tau / 12
        g.fill(Seg(cx, cy, cx + math.cos(aa) * r, cy + math.sin(aa) * r, 1.2), (50, 40, 60))
    g.fill(Union([Seg(cx - 60, 300, cx, cy, 4), Seg(cx + 60, 300, cx, cy, 4)]), (50, 40, 60))
    for i, x0 in enumerate(range(440, 600, 18)):
        h = 30 + 40 * abs(math.sin(i * 0.7))
        g.fill(Box(x0, 300 - h, x0 + 3, 300), (50, 40, 60))
    g.fill(Seg(436, 260, 610, 230, 2), (50, 40, 60))
    # beach
    g.fill(Under(lambda x: 440 + (fbm1(x, 120, 3, 9804) - 0.5) * 10, -20, W + 20, H + 20), tex(vgrad([(440, (230, 190, 150)), (600, (200, 160, 120))]), 0.2, 4, 3, 4, 9805))
    g.add(Box(-2, 436, W + 2, 452), (255, 255, 255), 0.25, feather=6)
    # lifeguard tower
    g.fill(Union([Seg(110, 560, 130, 470, 4), Seg(190, 560, 170, 470, 4), Seg(115, 520, 185, 520, 3)]), (230, 230, 230))
    g.fill(Box(100, 420, 200, 476, 3), light_x((60, 140, 200), 100, 200, 1.2, 0.7))
    g.fill(Poly([(90, 422), (150, 396), (210, 422)]), (230, 70, 60) if "roof" not in d else (240, 200, 60))
    g.fill(Box(120, 432, 180, 456), (40, 50, 60))
    g.fill(Seg(200, 400, 200, 360, 2), (200, 200, 200))
    if "flag" not in d:
        g.fill(Poly([(201, 360), (246, 372), (201, 386)]), (240, 50, 50))
    # umbrellas, towels, surfboard
    for x, col, key in ((330, (230, 70, 80), "umbrella"), (520, (250, 200, 60), None)):
        c = col if not (key and key in d) else (60, 160, 220)
        g.fill(Seg(x, 540, x + 4, 470, 2), (230, 230, 230))
        g.fill(Inter(Ell(x + 4, 470, 54, 26), Box(x - 54, 440, x + 60, 470)), lambda X, Y, c=c: C(c) * (0.85 + 0.25 * (np.sin((X - x) * 0.18) > 0))[..., None])
        g.mul(Ell(x + 20, 545, 50, 8), 0.4, feather=6)
    g.fill(Box(380, 540, 470, 560, 2), (60, 170, 160) if "towel" not in d else (230, 120, 170))
    if "ball" not in d:
        g.fill(Circ(560, 580, 14), sphere_paint(555, 575, 14, (250, 250, 250), amb=0.5, spec=0.4))
        g.fill(Inter(Circ(560, 580, 14), Box(546, 566, 560, 594)), (230, 60, 60), alpha=0.8)
    if "board" not in d:
        g.fill(Ell(760, 500, 14, 60), lgrad(746, 0, 774, 0, [(0, (250, 250, 250)), (1, (200, 210, 220))]))
        g.fill(Seg(760, 444, 760, 556, 1.4), (240, 90, 60))
    # volleyball net
    g.fill(Union([Box(600, 470, 604, 560), Box(880, 470, 884, 560)]), (240, 240, 240))
    g.fill(Box(604, 474, 880, 500), (40, 40, 40), alpha=lambda X, Y: 0.6 * ((np.abs(np.sin(X * 0.6)) > 0.9) | (np.abs(np.sin(Y * 0.6)) > 0.9)))
    g.fill(Box(604, 472, 880, 476), (240, 240, 240))
    person(g, 660, 580, 110, (230, 90, 70), seed=9810)
    person(g, 820, 586, 116, (60, 110, 170), seed=9811, face_right=False)
    person(g, 260, 590, 116, (240, 200, 70), seed=9812)


L1598_RAYS = [dict(lx=SUN98[0], ly=SUN98[1], col=(255, 190, 130), k=0.6, region=Box(-2, -2, W + 2, 290), threshold=170,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=lambda X, Y: moon_receive(*SUN98, floor=0.3)(X, Y) * smooth(460, 300, Y))]


def l1598_wheel(g, m):
    cx, cy, r = 700, 190, 100
    for a in range(12):
        aa = a * math.tau / 12
        px, py = cx + math.cos(aa) * r, cy + math.sin(aa) * r
        g.fill(Box(px - 7, py - 6, px + 7, py + 8, 3), (250, 210, 120))
        g.glow(px, py, 12, (255, 220, 150), 0.4)


L1598_EL = [E("wheel", el(l1598_wheel), pivot=(700, 190), anim=dict(rotateSpeed=-8)),
            bird_el("gull1", 200, 120, s=8, speed=20, col=(240, 240, 240)), bird_el("gull2", 500, 90, s=7, speed=-16, col=(240, 240, 240)),
            glint_el("glints", [(260, 340), (320, 380), (300, 410)], col=(255, 230, 180), r=6, speed=0.6)]
L1598_DIFFS = [("flag", 220, 372, 0), ("umbrella", 334, 456, 0), ("board", 760, 500, 0), ("roof", 150, 410, 0), ("towel", 425, 550, 0),
               ("ball", 560, 580, 0)]


# =================================================================== Level 1599 rainy neon strip
def l1599_upper(g, d):
    sky(g, [(0, (10, 10, 24)), (300, (40, 30, 60))])
    stucco(g, -20, 300, 40, 420, (60, 50, 60), seed=9901)
    stucco(g, 300, 600, 90, 420, (50, 50, 66), seed=9902)
    stucco(g, 600, 920, 20, 420, (66, 50, 54), seed=9903)
    rnd = random.Random(9904)
    for x0, x1, top in ((-20, 300, 40), (300, 600, 90), (600, 920, 20)):
        for y in range(top + 30, 300, 60):
            for x in range(x0 + 30, x1 - 40, 70):
                lit = rnd.random() < 0.4
                if (x0, y, x) == (600, 230, 840) and "window" in d:
                    lit = not lit
                window(g, x, y, x + 30, y + 36, lit=(255, 200, 140) if lit else None, frame=(40, 36, 40), glass=((60, 60, 80), (30, 30, 40)))
    # fire escape on the left building
    for y in (120, 200):
        g.fill(Union([Box(60, y, 220, y + 4), Box(60, y - 30, 220, y - 28)] + [Box(x, y - 30, x + 2, y) for x in range(60, 222, 12)]), (24, 22, 26))
    if "ladder" not in d:
        g.fill(Union([Box(200, 124, 203, 196), Box(214, 124, 217, 196)] + [Box(200, y, 217, y + 2) for y in range(130, 196, 10)]), (24, 22, 26))
    # neon signs (abstract shapes)
    neon(g, Union([Circ(420, 180, 20), Circ(450, 180, 20), Poly([(402, 188), (468, 188), (435, 226)])]), (255, 60, 140) if "heart" not in d else (60, 220, 255))
    neon(g, Poly([(700, 120), (760, 120), (730, 160)]), (90, 240, 220))
    neon(g, Box(714, 160, 746, 164), (90, 240, 220))
    neon(g, Box(150, 300, 260, 340, 8), (250, 200, 60), on="frame" not in d)
    neon(g, Union([Seg(640, 330, 860, 330, 1), Poly([(860, 318), (880, 330), (860, 342)])]), (255, 120, 60))
    # awnings and shop windows at street level
    for x0, x1, col in ((20, 280, (120, 30, 50)), (320, 580, (30, 70, 110)), (620, 880, (40, 90, 60))):
        g.fill(Poly([(x0, 350), (x1, 350), (x1 + 10, 380), (x0 - 10, 380)]), light_y(col, 350, 380, 1.3, 0.7))
        window(g, x0 + 20, 386, x1 - 20, 420, lit=(255, 220, 170), frame=(30, 30, 34))
    asphalt(g, Box(-2, 420, W + 2, 440), base=(60, 60, 66), seed=9905)


def l1599_scene(g, d):
    l1599_upper(g, set())
    g.snapshot("s")
    l1599_upper(g, d)
    asphalt(g, Box(-2, 440, W + 2, H + 2), base=(30, 30, 38), seed=9906)
    g.reflect(440, 440, 600, ripple=4, k=0.55, tint=(20, 20, 40), tint_k=0.3, streak=0.4)
    for x in range(-20, 900, 100):
        g.fill(Box(x, 520, x + 50, 524), (200, 200, 180), alpha=0.6)
    # taxi and people with umbrellas
    car(g, 520, 560, 220, (240, 190, 30), kind="sedan", face=-1, lights=True, seed=9910)
    if "taxi" not in d:
        g.fill(Box(500, 474, 540, 486, 3), (250, 250, 240))
        g.glow(520, 480, 20, (255, 250, 200), 0.4)
    if "hydrant" not in d:
        hydrant(g, 820, 470, col=(220, 50, 50))
    for x, col, key in ((180, (40, 40, 44), None), (300, (200, 40, 60), "umbrella")):
        c = col if not (key and key in d) else (60, 120, 200)
        person(g, x, 480, 120, (60, 60, 70), seed=x)
        g.fill(Seg(x + 4, 380, x + 4, 410, 1.4), (30, 30, 30))
        g.fill(Inter(Ell(x + 4, 384, 44, 24), Box(x - 44, 356, x + 52, 384)), light_x(c, x - 40, x + 48, 1.3, 0.6))


L1599_EL = [rain_layer("rain", 9920, 70, 30, 1.1, 0.35, 300, mask=0),
            E("flicker", el(lambda g, m: g.glow(730, 140, 40, (90, 240, 220), 0.4)), daynight="untinted", anim=dict(blinkInterval=3.0, blinkDuration=0.3)),
            glint_el("puddles", [(200, 520), (640, 540), (420, 580)], col=(255, 160, 200), r=5, speed=0.5)]
L1599_DIFFS = [("window", 855, 248, 0), ("ladder", 208, 160, 0), ("heart", 435, 196, 0), ("frame", 205, 320, 0), ("taxi", 520, 480, 0),
               ("hydrant", 820, 450, 0), ("umbrella", 304, 372, 0)]



# =================================================================== Level 1600 custom garage
def tyre(g, x, base, r=30, w=18):
    g.fill(Box(x - r, base - w, x + r, base, 4), light_y((40, 40, 44), base - w, base, 1.3, 0.7))
    g.fill(Ell(x, base - w, r, w * 0.35), (30, 30, 32))
    g.fill(Ell(x, base - w, r * 0.5, w * 0.18), (16, 16, 18))


def l1600_scene(g, d):
    g.fill(Box(-2, -2, W + 2, 440), tex(vgrad([(0, (70, 72, 80)), (440, (96, 98, 104))]), 0.12, 20, 20, 3, 10001))
    for x0 in (60, 520):
        g.fill(Box(x0, 40, x0 + 320, 50, 4), (240, 250, 255))
        g.glow(x0 + 160, 50, 220, (180, 220, 255), 0.25, ry=60)
    # pegboard with tools
    g.fill(Box(40, 120, 300, 300, 2), tex((150, 120, 90), 0.1, 3, 3, 2, 10002))
    g.fill(Box(40, 120, 300, 300), (60, 40, 30), alpha=lambda X, Y: 0.5 * ((np.abs(np.sin(X * 0.35)) > 0.97) & (np.abs(np.sin(Y * 0.35)) > 0.97)))
    if "wrench" not in d:
        g.fill(Union([Seg(80, 150, 80, 270, 4), Circ(80, 146, 10) - Circ(80, 140, 5), Circ(80, 274, 8)]), sphere_paint(76, 200, 30, (180, 182, 190), ry=80, amb=0.4, spec=0.7))
    g.fill(Union([Seg(130, 150, 130, 260, 4), Box(116, 140, 144, 160, 2)]), sphere_paint(126, 200, 30, (170, 172, 180), ry=80, amb=0.4, spec=0.7))
    g.fill(Seg(130, 220, 130, 260, 5), (200, 40, 40))
    g.fill(Union([Seg(180, 150, 200, 260, 3), Seg(220, 150, 200, 260, 3)]), (180, 182, 190))
    g.fill(Ell(260, 200, 22, 30), (230, 180, 40))
    # abstract racing poster
    g.fill(Box(360, 120, 470, 260, 2), (240, 240, 236))
    g.fill(Poly([(360, 220), (470, 160), (470, 200), (360, 260)]), (220, 40, 40) if "poster" not in d else (40, 120, 220))
    g.fill(Circ(415, 150, 16), (30, 30, 30))
    # floor (polished concrete with reflections)
    g.fill(Box(-2, 440, W + 2, H + 2), tex(vgrad([(440, (120, 122, 128)), (600, (80, 82, 88))]), 0.15, 30, 10, 3, 10003))
    g.add(Box(-2, 440, W + 2, 470), (180, 220, 255), 0.08, feather=10)
    g.mul(Ell(640, 520, 70, 16), 0.4, feather=20)
    # two-post lift with the car raised
    for x in (470, 830):
        g.fill(Box(x - 12, 150, x + 12, 450), light_x((220, 180, 40), x - 12, x + 12, 1.3, 0.6))
        g.fill(Box(x - 20, 440, x + 20, 452, 2), (60, 60, 64))
    g.fill(Union([Box(470, 300, 560, 308), Box(740, 300, 830, 308)]), (60, 60, 64))
    car(g, 650, 300, 330, (40, 150, 90), kind="sport", face=1, seed=10004)
    if "rim" in d:
        for wx in (650 + 330 * 0.3,):
            g.fill(Circ(wx, 300 - 99 * 0.28, 99 * 0.2), sphere_paint(wx - 2, 300 - 99 * 0.32, 99 * 0.2, (230, 180, 40), amb=0.4, spec=0.7))
    # tyre stacks
    for k in range(4 if "tyres" not in d else 3):
        tyre(g, 100, 560 - k * 18, 34, 18)
    tyre(g, 180, 560, 34, 18)
    tyre(g, 180, 542, 34, 18)
    # rolling toolbox
    tb = Box(320, 420, 440, 560, 4)
    g.mul(Ell(386, 562, 70, 8), 0.5, feather=6)
    g.fill(tb, light_x((200, 30, 30), 320, 440, 1.3, 0.7))
    for k in range(5):
        y = 432 + k * 24
        g.fill(Box(326, y, 434, y + 2), (120, 20, 20))
        if "drawer" in d and k == 2:
            g.fill(Box(326, y + 3, 434, y + 22), (40, 90, 200))
        g.fill(Box(360, y + 8, 400, y + 12, 2), (220, 220, 230))
    for x in (330, 430):
        g.fill(Circ(x, 566, 6), (30, 30, 30))
    # oil drum and can
    g.fill(Box(820, 480, 880, 580, 4), cyl_paint(850, 30, (40, 70, 140), amb=0.35, spec=0.4))
    for y in (500, 560):
        g.fill(Box(820, y, 880, y + 4), (30, 50, 100))
    if "can" not in d:
        g.fill(Union([Box(760, 540, 790, 580, 3), Seg(775, 540, 790, 528, 3)]), cyl_paint(775, 15, (230, 190, 40), amb=0.35, spec=0.5))
    person(g, 560, 590, 150, (40, 60, 100), seed=10005, hat=None)


L1600_EL = [E("flicker", el(lambda g, m: g.glow(680, 50, 120, (180, 220, 255), 0.25, ry=30)), daynight="untinted",
              anim=dict(blinkInterval=5.0, blinkDuration=0.3)),
            E("spark", el(lambda g, m: [g.glow(560 + k * 6, 400 - k * 4, 3, (255, 220, 120), 1.0) for k in range(4)]), daynight="untinted",
              anim=dict(twinkle=0.9, twinkleSpeed=2.0))]
L1600_DIFFS = [("wrench", 80, 210, 0), ("poster", 415, 210, 0), ("rim", 749, 272, 0), ("tyres", 100, 500, 0), ("drawer", 380, 490, 0),
               ("can", 775, 556, 0)]


# =================================================================== Level 1601 container docks at dusk
CONT = [(190, 60, 50), (40, 90, 160), (220, 150, 40), (50, 120, 80), (150, 150, 160), (120, 50, 90)]


def container(g, x0, y0, w, h, col, seed=0):
    s = Box(x0, y0, x0 + w, y0 + h, 1)
    g.fill(s, tex(light_y(col, y0, y0 + h, 1.15, 0.8), 0.08, 2, 8, 2, seed))
    g.fill(s, (0, 0, 0), alpha=lambda X, Y: 0.25 * (np.abs(np.sin((X - x0) * 0.9)) > 0.8))
    g.fill(Diff(s, Box(x0 + 2, y0 + 2, x0 + w - 2, y0 + h - 2)), mixc(col, (0, 0, 0), 0.4))


def l1601_scene(g, d):
    sky(g, [(0, (50, 50, 100)), (180, (170, 110, 130)), (280, (250, 170, 110))])
    cloud_layer(g, 40, 170, (250, 170, 140), (110, 80, 110), cover=0.45, sx=220, sy=16, seed=10101, alpha=0.7)
    water(g, 300, 420, (170, 120, 120), (50, 60, 90), seed=10102)
    # cargo ship (right)
    hull = Poly([(420, 340), (920, 340), (920, 410), (460, 410)])
    g.fill(hull, light_y((40, 50, 70), 340, 410, 1.2, 0.7))
    g.fill(Box(420, 396, 920, 410), (150, 40, 40))
    rnd = random.Random(10103)
    for row in range(3):
        for k in range(9):
            container(g, 470 + k * 44, 316 - row * 22, 42, 22, CONT[rnd.randrange(6)], seed=10104 + row * 9 + k)
    g.fill(Box(840, 200, 900, 340), light_x((230, 230, 225), 840, 900, 1.2, 0.7))
    for y in (220, 250, 280):
        g.fill(Box(846, y, 894, y + 10), (60, 80, 110))
    g.fill(Box(856, 160, 884, 200), light_x((40, 40, 46), 856, 884, 1.3, 0.6))
    g.fill(Box(856, 166, 884, 186), (220, 50, 50) if "funnel" not in d else (240, 200, 60))
    # quay
    g.fill(Box(-2, 410, W + 2, H + 2), tex(vgrad([(410, (110, 108, 106)), (600, (70, 68, 66))]), 0.2, 10, 4, 3, 10105))
    g.fill(Box(-2, 410, W + 2, 418), (220, 190, 60))
    # gantry crane
    cr = (210, 80, 40)
    g.fill(Union([Box(120, 90, 136, 420), Box(330, 90, 346, 420), Box(100, 80, 480, 100), Seg(136, 140, 330, 300, 3), Seg(330, 140, 136, 300, 3)]),
           light_x(cr, 100, 480, 1.2, 0.7))
    g.fill(Box(240, 100, 280, 120), (60, 60, 66))
    g.fill(Union([Seg(250, 120, 250, 190, 1), Seg(270, 120, 270, 190, 1)]), (40, 40, 44))
    container(g, 220, 190, 80, 30, (40, 90, 160) if "box" not in d else (220, 150, 40), seed=10106)
    if "lamp" not in d:
        g.glow(480, 80, 30, (255, 220, 150), 0.6)
        g.fill(Circ(478, 84, 5), (255, 240, 200))
    # container stacks in the yard (left foreground)
    for row in range(3):
        for k in range(3):
            if row == 2 and (k == 2 or (k == 1 and "stack" in d)):
                continue
            container(g, 20 + k * 90, 560 - (row + 1) * 40, 88, 40, CONT[(row * 3 + k) % 6], seed=10110 + row * 3 + k)
    # forklift
    if "forklift" not in d:
        fx = 520
        g.fill(Box(fx, 500, fx + 80, 560, 4), light_x((240, 190, 40), fx, fx + 80, 1.2, 0.7))
        g.fill(Box(fx + 10, 450, fx + 60, 500), (40, 40, 44), alpha=0.6)
        g.fill(Union([Box(fx - 10, 440, fx - 4, 570), Box(fx - 40, 560, fx - 4, 566)]), (60, 60, 64))
        for wx in (fx + 16, fx + 66):
            g.fill(Circ(wx, 564, 14), (30, 30, 30))
    # bollard with rope
    g.fill(Union([Box(780, 430, 800, 470, 4), Ell(790, 430, 14, 5)]), cyl_paint(790, 10, (50, 50, 56), amb=0.4, spec=0.4))
    g.fill(Seg(790, 440, 920, 360, 2), (200, 180, 140))
    person(g, 700, 560, 120, (240, 140, 40), seed=10107, hat=(250, 250, 250))


L1601_EL = [bird_el("g1", 600, 120, s=8, speed=-18, col=(240, 240, 240)), glint_el("sea", [(200, 360), (400, 380)], col=(255, 210, 170), r=5, speed=0.5),
            mist_el("haze", 450, 300, 450, 12, (240, 180, 150), alpha=0.25, length=60, seed=101)]
L1601_DIFFS = [("funnel", 870, 176, 0), ("box", 260, 205, 0), ("lamp", 478, 82, 0), ("forklift", 545, 510, 0), ("stack", 155, 460, 0)]


# =================================================================== Level 1602 desert trailer at dusk
def saguaro(g, x, base, h, arms=((0.45, -1), (0.6, 1)), seed=0):
    col = (60, 100, 70)
    w = h * 0.08
    parts = [Box(x - w, base - h, x + w, base, w)]
    for t_, sgn in arms:
        y = base - h * t_
        parts += [Box(x, y - w * 0.8, x + sgn * w * 3, y + w * 0.6, w * 0.6), Box(x + sgn * w * 2.2 - w * 0.8, y - h * 0.3, x + sgn * w * 2.2 + w * 0.8, y + w * 0.2, w * 0.8)]
    s = Union(parts)
    g.fill(s, tex(light_x(col, x - w * 4, x + w * 4, 1.2, 0.6), 0.2, 1.2, 8, 3, seed))


def l1602_scene(g, d):
    sky(g, [(0, (40, 40, 90)), (200, (170, 100, 120)), (300, (250, 160, 90))])
    stars(g, 30, 140, seed=10201)
    ridge(g, 320, 80, 220, 10202, (80, 50, 70), ridged=True, light=False, haze=((200, 120, 110), 0.4, 0.2))
    g.fill(Box(-2, 320, W + 2, H + 2), tex(vgrad([(320, (170, 120, 90)), (600, (110, 80, 60))]), 0.25, 6, 3, 4, 10203))
    # power poles
    for x in (60, 330, 600, 870):
        g.fill(Union([Box(x - 3, 180, x + 3, 330), Box(x - 24, 190, x + 24, 194)]), (60, 46, 40))
    for k in (-20, 20):
        for a, b in ((60, 330), (330, 600), (600, 870)):
            pts = [(a + k + (b - a) * t_, 190 + 18 * 4 * t_ * (1 - t_)) for t_ in np.linspace(0, 1, 12)]
            for p0, p1 in zip(pts[:-1], pts[1:]):
                g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 0.7), (40, 30, 30))
    # trailer
    tr = Box(360, 330, 700, 460, 30)
    g.mul(Ell(530, 470, 190, 12), 0.5, feather=8)
    g.fill(tr, lambda X, Y: C((200, 196, 190)) * (1.15 - 0.45 * np.clip((Y - 330) / 130, 0, 1) + 0.2 * np.exp(-((Y - 360) / 10) ** 2))[..., None])
    for x, key in ((400, None), (520, "window"), (620, None)):
        lit = not (key and key in d)
        window(g, x, 360, x + 50, 400, lit=(255, 190, 110) if lit else None, frame=(160, 156, 150))
    g.fill(Box(460, 380, 494, 460), (110, 90, 80))
    g.fill(Poly([(360, 330), (300, 360), (300, 366), (360, 340)]), (220, 80, 60))
    if "dish" not in d:
        g.fill(Seg(640, 330, 640, 300, 2), (150, 150, 150))
        g.fill(Ell(646, 292, 22, 14), sphere_paint(640, 288, 22, (220, 220, 220), ry=14, amb=0.4, spec=0.4))
    for wx in (430, 610):
        g.fill(Circ(wx, 464, 16), (30, 30, 30))
    # lawn chairs and a fire barrel
    for x, col, key in ((300, (60, 140, 200), "chair"), (220, (230, 200, 60), None)):
        c = col if not (key and key in d) else (220, 80, 80)
        g.fill(Union([Box(x - 20, 470, x + 20, 480, 2), Box(x - 20, 440, x - 14, 480, 2)]), light_x(c, x - 20, x + 20, 1.2, 0.7))
        g.fill(Union([Seg(x - 18, 480, x - 22, 500, 1.4), Seg(x + 18, 480, x + 22, 500, 1.4)]), (160, 160, 160))
    g.fill(Box(250, 490, 290, 540, 4), cyl_paint(270, 20, (90, 70, 60), amb=0.35, spec=0.2))
    g.glow(270, 480, 100, (255, 150, 60), 0.4)
    # rusty car on blocks
    car(g, 790, 520, 200, (150, 90, 60), kind="sedan", face=-1, seed=10204)
    g.fill(Box(700, 500, 880, 520), (120, 70, 50), alpha=lambda X, Y: 0.4 * (fbm(X, Y, 6, 4, 2, 10205) > 0.55))
    if "tyre" not in d:
        g.fill(Ell(120, 560, 34, 12), (30, 30, 32))
        g.fill(Ell(120, 556, 16, 5), (60, 60, 64))
    saguaro(g, 90, 470, 170, arms=((0.45, -1), (0.6, 1)) if "cactus" not in d else ((0.45, -1),), seed=10206)
    saguaro(g, 900, 420, 120, seed=10207)
    # mailbox
    g.fill(Union([Box(560, 500, 566, 560), Box(546, 486, 580, 504, 6)]), light_x((80, 80, 90), 546, 580, 1.2, 0.7))
    if "flag" not in d:
        g.fill(Union([Box(580, 470, 585, 500), Box(585, 470, 604, 484)]), (220, 40, 40))


L1602_EL = [E("fire", el(lambda g, m: g.fill(Union([Ell(270, 484, 14, 8), Poly([(258, 486), (270, 452), (282, 486)])]), (255, 170, 70))),
              pivot=(270, 490), daynight="untinted", anim=dict(stretch=(0.08, 0.3), scaleSpeed=2.0)),
            E("smoke", el(lambda g, m: g.glow(270, 440, 16, (120, 110, 110), 0.3)), anim=dict(driftVelocity=(8, 50), driftLength=120, driftFade=True, driftGrow=2.0)),
            glint_el("stars", [(150, 40), (500, 60), (760, 30)], col=(255, 250, 230), r=3, speed=0.5)]
L1602_DIFFS = [("window", 545, 380, 0), ("dish", 644, 296, 0), ("chair", 300, 470, 0), ("tyre", 120, 558, 0), ("cactus", 110, 380, 0),
               ("flag", 588, 486, 0)]


# =================================================================== Level 1603 hillside villa with an infinity pool
SUN03 = (720, 230, 22)


def l1603_upper(g, d):
    sky(g, [(0, (70, 90, 160)), (160, (230, 150, 140)), (260, (255, 190, 120))])
    sun(g, *SUN03, col=(255, 236, 190), halo=(255, 160, 90), k=0.6)
    # city far below
    rnd = random.Random(10301)
    x = -10
    while x < 910:
        w = rnd.uniform(12, 30)
        hh = rnd.uniform(10, 70)
        g.fill(Box(x, 290 - hh, x + w, 300), (110, 90, 120))
        x += w + rnd.uniform(1, 5)
    g.fog(220, 300, (250, 180, 140), 0.0, 0.5)


def l1603_scene(g, d):
    l1603_upper(g, d)
    g.snapshot("s")
    # infinity pool reflecting the sky
    g.fill(Box(-2, 300, W + 2, 400), (40, 120, 150))
    g.reflect(300, 300, 400, ripple=2, k=0.7, tint=(30, 110, 140), tint_k=0.35)
    g.fill(Box(-2, 296, W + 2, 302), (230, 230, 225))
    if "ring" not in d:
        g.fill(Ell(540, 360, 34, 12) - Ell(540, 360, 18, 6), lambda X, Y: C((250, 90, 90)) * (0.85 + 0.3 * (np.sin(np.arctan2(Y - 360, X - 540) * 4) > 0))[..., None])
    # deck
    g.fill(Box(-2, 400, W + 2, H + 2), tex(light_y((200, 180, 160), 400, 600, 1.1, 0.8), 0.1, 30, 4, 3, 10302))
    g.fill(Box(-2, 400, W + 2, 408), (240, 240, 236))
    # modern villa (left): white boxes and glass
    g.fill(Box(-2, 120, 330, 400), light_x((240, 236, 228), -2, 330, 1.1, 0.8))
    g.fill(Box(-2, 110, 360, 124), (220, 216, 210))
    for x0 in (20, 130, 240):
        window(g, x0, 150, x0 + 90, 260, lit=(255, 210, 160) if (x0 == 130 and "window" not in d) else None, frame=(60, 60, 64),
               glass=((180, 160, 170), (80, 80, 100)))
    window(g, 20, 290, 300, 390, lit=(255, 220, 170), frame=(60, 60, 64))
    # loungers with towels
    for x, key in ((420, "lounger"), (560, None)):
        c = (240, 240, 240) if not (key and key in d) else (40, 140, 200)
        g.mul(Ell(x + 50, 482, 70, 8), 0.4, feather=6)
        g.fill(Union([Poly([(x, 470), (x + 100, 470), (x + 100, 478), (x, 478)]), Poly([(x, 470), (x - 20, 432), (x - 12, 430), (x + 8, 470)])]), light_y(c, 430, 478, 1.1, 0.8))
        g.fill(Box(x + 30, 466, x + 80, 472), (250, 140, 60))
        for lx in (x + 4, x + 96):
            g.fill(Box(lx - 2, 478, lx + 2, 492), (120, 120, 126))
    # umbrella
    if "umbrella" not in d:
        g.fill(Seg(720, 500, 720, 390, 2.4), (200, 200, 200))
        g.fill(Inter(Ell(720, 394, 80, 30), Box(640, 360, 800, 394)), light_x((40, 50, 60), 640, 800, 1.2, 0.7))
    # potted plant and abstract sculpture
    g.fill(Box(830, 470, 880, 520, 6), light_x((60, 60, 64), 830, 880, 1.2, 0.7))
    g.fill(Rough(Ell(855, 440, 40, 40), 8, 10, 10303), tex((60, 110, 60), 0.4, 3, 3, 3, 10304))
    if "sculpture" not in d:
        g.fill(Union([Box(360, 520, 400, 530), Seg(380, 520, 360, 460, 6), Seg(360, 460, 400, 440, 6)]), sphere_paint(370, 470, 40, (200, 160, 80), ry=60, amb=0.4, spec=0.8))
    palm(g, 880, 400, 330, lean=-0.08, seed=10305)


L1603_EL = [glint_el("pool", [(500, 340), (650, 360), (800, 330)], col=(255, 240, 210), r=5, speed=0.6), bird_el("b", 500, 80, s=6, speed=16)]
L1603_DIFFS = [("ring", 540, 360, 0), ("window", 175, 205, 0), ("lounger", 450, 460, 0), ("umbrella", 720, 380, 0), ("sculpture", 378, 488, 0)]


# =================================================================== Level 1604 skyline overlook at dusk
def l1604_scene(g, d):
    sky(g, [(0, (20, 30, 70)), (200, (90, 70, 120)), (330, (240, 140, 90))])
    stars(g, 30, 140, seed=10401)
    ridge(g, 330, 60, 240, 10402, (50, 40, 70), ridged=False, light=False)
    rnd = random.Random(10403)
    # downtown skyline
    for x0, w, top, glass_ in ((260, 50, 160, True), (316, 40, 200, False), (360, 70, 100, True), (436, 46, 180, True), (488, 60, 140, False),
                               (552, 40, 210, True), (598, 80, 120, True), (684, 44, 190, False)):
        tower(g, x0, x0 + w, top, 340, (60, 70, 100), seed=int(x0), glass=glass_, lit=(255, 214, 150), lit_p=0.25,
              sky_top=(60, 60, 110), sky_bot=(240, 140, 100))
    if "spire" not in d:
        g.fill(Union([Poly([(388, 100), (395, 50), (402, 100)]), Box(386, 96, 404, 104)]), light_x((110, 110, 130), 386, 404, 1.3, 0.6))
        g.glow(395, 48, 14, (255, 60, 60), 0.9)
    # hills with house lights
    g.fill(Under(lambda x: 340 + 40 * np.sin(x / 140.0) + (fbm1(x, 60, 3, 10404) - 0.5) * 20, -20, W + 20, H + 20), (30, 30, 46))
    for _ in range(80):
        x, y = rnd.uniform(0, 900), rnd.uniform(380, 470)
        g.glow(x, y, 3, (255, 210, 140), 0.8)
    # overlook: road, railing, bench, coin telescope, lamp
    asphalt(g, Box(-2, 470, W + 2, H + 2), base=(50, 50, 56), seed=10405)
    g.fill(Union([Box(-2, 452, W + 2, 456), Box(-2, 468, W + 2, 472)] + [Box(x, 452, x + 4, 492) for x in range(0, 900, 40)]), (150, 150, 156))
    if "telescope" not in d:
        g.fill(Union([Box(706, 470, 714, 520), Box(694, 516, 726, 522), Seg(690, 448, 736, 438, 8)]), light_x((70, 110, 90), 690, 736, 1.3, 0.6))
    if "bench" not in d:
        g.fill(Union([Box(100, 486, 220, 494, 2), Box(100, 470, 220, 476, 2), Box(106, 494, 112, 520), Box(208, 494, 214, 520)]), (110, 80, 60))
    street_light(g, 40, 560, 180, face=1, lit="lamp" not in d)
    car(g, 470, 570, 280, (230, 230, 236), kind="sport", face=1, lights=True, seed=10406)
    g.fill(Box(470 - 140 + 10, 570 - 84 * 0.62, 470 + 140 - 10, 570 - 84 * 0.55), (220, 40, 40))
    g.fill(Circ(470, 500, 15), (250, 250, 250) if "roundel" not in d else (250, 210, 60))
    g.fill(Ring(Circ(470, 500, 15), 1.5), (30, 30, 30))
    person(g, 640, 590, 130, (40, 40, 50), seed=10407)


L1604_EL = [E("heli", el(lambda g, m: [g.fill(Union([Ell(820, 120, 18, 8), Seg(830, 118, 860, 114, 3)]), (20, 20, 30)), g.glow(812, 124, 8, (255, 60, 60), 0.9)]),
              pivot=(820, 120), anim=dict(bobAmplitude=(40, 6), bobSpeed=0.05)),
            glint_el("city", [(380, 200), (460, 250), (620, 180), (300, 260)], col=(255, 230, 180), r=4, speed=0.4),
            E("beacon", el(lambda g, m: g.glow(395, 58, 22, (255, 80, 80), 0.6)), daynight="untinted", anim=dict(blinkInterval=1.5, blinkDuration=0.5))]
L1604_DIFFS = [("spire", 395, 76, 0), ("telescope", 712, 470, 0), ("lamp", 82, 380, 0), ("roundel", 470, 500, 0), ("bench", 160, 490, 0)]

LEVELS = [
    ("Level1595", "日落大道", make_bg(l1595_scene, L1595_RAYS, bloom=(205, 16, 0.4), grade=dict(contrast=1.06, sat=1.05)), L1595_EL, L1595_DIFFS, 60, OPTS),
    ("Level1596", "公路加油站", flat_bg(l1596_scene, bloom=(215, 16, 0.3)), L1596_EL, L1596_DIFFS, 60, OPTS),
    ("Level1597", "高速追逐", flat_bg(l1597_scene, bloom=(180, 16, 0.5)), L1597_EL, L1597_DIFFS, 60, OPTS),
    ("Level1598", "海滨栈桥", make_bg(l1598_scene, L1598_RAYS, bloom=(205, 16, 0.4)), L1598_EL, L1598_DIFFS, 60, OPTS),
    ("Level1599", "霓虹夜街", flat_bg(l1599_scene, bloom=(170, 18, 0.55)), L1599_EL, L1599_DIFFS, 60, OPTS),
    ("Level1600", "改装车库", flat_bg(l1600_scene, bloom=(210, 16, 0.4)), L1600_EL, L1600_DIFFS, 60, OPTS),
    ("Level1601", "港口货柜", flat_bg(l1601_scene, bloom=(210, 16, 0.35)), L1601_EL, L1601_DIFFS, 60, OPTS),
    ("Level1602", "沙漠拖车", flat_bg(l1602_scene, bloom=(200, 16, 0.4)), L1602_EL, L1602_DIFFS, 60, OPTS),
    ("Level1603", "豪宅泳池", flat_bg(l1603_scene, bloom=(205, 16, 0.4)), L1603_EL, L1603_DIFFS, 60, OPTS),
    ("Level1604", "城市夜景", flat_bg(l1604_scene, bloom=(190, 16, 0.5)), L1604_EL, L1604_DIFFS, 60, OPTS),
]
