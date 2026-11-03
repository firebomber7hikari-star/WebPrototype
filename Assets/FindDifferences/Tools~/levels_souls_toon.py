# -*- coding: utf-8 -*-
"""Toon-render (cel-shaded) remakes of four realistic dark-fantasy levels from levels_souls - same compositions,
same difference ideas, redrawn with ink outlines, flat colour and one hard cool shadow:
  Level1620 卡通·禁林提灯   (Level1569) lantern-lit forbidden woods: cages, fenced path, hut, eyes in the dark
  Level1621 卡通·禁书库     (Level1571) forbidden library: shelves, ladder, chandelier, desk, hourglass, globe
  Level1622 卡通·桥上对峙   (Level1573) a hunter facing a beast on a stone bridge under the full moon
  Level1623 卡通·月光礼拜堂 (Level1574) a chapel: stained-glass beams, pews, altar, candelabra, censer
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, el, fbm1, mixc, smooth, vgrad
from levels_remake import ToonS
from levels_real2 import arch
from toon import INK, cel, cloud_shape, shade_of, tint_of, toon_post
from styled_kit import sparkle_el

S = ToonS()
OPTS = dict(post=toon_post, anim_seconds=12.0, frames=60)
FIRE = (255, 190, 90)
NIGHT = (90, 70, 160)


def make(scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, d)
        S.finish(g)
        g.commit()
    return bg


def lantern(g, x, y, s=1.0, lit=True, col=(255, 210, 120)):
    if lit:
        g.glow(x, y + 9 * s, 60 * s, FIRE, 0.4)
    S.obj(g, Box(x - 8 * s, y, x + 8 * s, y + 20 * s, 2 * s), col if lit else (60, 64, 80), 1)
    S.obj(g, Poly([(x - 11 * s, y), (x, y - 10 * s), (x + 11 * s, y)]), (40, 36, 50), 2)


def cage(g, x, top, w, h, chain_len=60, col=(50, 46, 60)):
    for k in range(int(chain_len / 8)):
        g.fill(Ell(x, top - chain_len + k * 8, 2.4, 4) - Ell(x, top - chain_len + k * 8, 1, 2.4), INK)
    bars = Union([Seg(x + (i - 3) * w / 6, top + 4, x + (i - 3) * w / 6, top + h - 4, 1.8) for i in range(7)] +
                 [Box(x - w / 2, top + 4, x + w / 2, top + 9), Box(x - w / 2, top + h * 0.5, x + w / 2, top + h * 0.5 + 3),
                  Box(x - w / 2, top + h - 9, x + w / 2, top + h - 4), Inter(Ell(x, top + 6, w / 2, 10), Box(x - w / 2, top - 6, x + w / 2, top + 6))])
    S.obj(g, bars, col, 3)


def flame_el(eid, x, y, s=1.0, phase=0.0):
    def d(g, m):
        g.glow(x, y - 6 * s, 18 * s, FIRE, 0.5)
        cel(g, Union([Ell(x, y - 4 * s, 4 * s, 5 * s), Poly([(x - 4 * s, y - 5 * s), (x, y - 16 * s), (x + 4 * s, y - 5 * s)])]), (255, 200, 90),
            w=1.2, shade=(255, 140, 50), off=(-1.5 * s, -1.5 * s))
    return E(eid, el(d), pivot=(x, y), daynight="untinted", anim=dict(stretch=(0.06, 0.24), scaleSpeed=1.8 + phase, phase=phase))


def bat_el(eid, x, y, s=10, speed=28, phase=0.0):
    from kit import drift_across

    def d(g, m):
        for sg in (-1, 1):
            g.fill(Poly([(x, y - 0.1 * s), (x + sg * 0.4 * s, y - 0.5 * s), (x + sg * s, y - 0.3 * s), (x + sg * 0.7 * s, y + 0.1 * s),
                         (x + sg * 0.45 * s, y), (x + sg * 0.2 * s, y + 0.12 * s)]), INK)
        g.fill(Ell(x, y, 0.16 * s, 0.24 * s), INK)
    return E(eid, el(d), pivot=(x, y), anim=dict(drift_across(x - s, x + s, speed, start=phase), stretch=(0, 0.5), scaleSpeed=3.0,
                                                  bobAmplitude=(0, 5), bobSpeed=0.3))


def mist_el(eid, y, h, col, alpha=0.35, speed=0.05):
    return E(eid, el(lambda g, m: g.fill(Box(-60, y - h / 2, W + 60, y + h / 2, h / 2), col, alpha=alpha, feather=h * 0.4)),
             anim=dict(bobAmplitude=(40, 0), bobSpeed=speed))


def toon_tree(g, x, base, h, col=(40, 44, 60), lean=0.0, seed=0, spread=1.0):
    """Gnarled leafless toon tree: tapered trunk and a few forked, ink-outlined branches."""
    rnd = random.Random(seed)
    parts = [Poly([(x - h * 0.07, base), (x - h * 0.03, base - h * 0.5), (x + h * 0.03, base - h * 0.5), (x + h * 0.08, base)])]
    tips = [(x + lean * h * 0.3, base - h * 0.5, math.pi / 2 + lean, h * 0.03)]
    for depth in range(3):
        new = []
        for px, py, a, w in tips:
            for sg in (-1, 1):
                aa = a + sg * rnd.uniform(0.35, 0.7) * spread
                ln = h * (0.32 - depth * 0.08) * rnd.uniform(0.8, 1.15)
                qx, qy = px + math.cos(aa) * ln, py - math.sin(aa) * ln
                parts.append(Seg(px, py, qx, qy, w, w * 0.6))
                new.append((qx, qy, aa, w * 0.6))
        tips = new
    S.obj(g, Union(parts), col, seed)
    return [(px, py) for px, py, _, _ in tips]


def hunter(g, x, base, h, face=1, coat=(60, 56, 70), scarf=(110, 100, 90), hat=(40, 36, 46), seed=0, weapon="axe"):
    """Toon hunter: long tattered coat, brimmed hat, face scarf, long-hafted axe (original design)."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    S.shadow(g, Ell(x + 10 * k, base, 60 * k, 8 * k))
    for lx, fx in ((-14, -22), (12, 14)):
        S.obj(g, Seg(sx(lx), sy(126), sx(fx), sy(14), 12 * k, 10 * k), (50, 46, 54), seed)
        S.obj(g, Ell(sx(fx + 6), sy(7), 15 * k, 7 * k), (36, 30, 34), seed + 1)
    hem = [(sx(-58 + 108 * i / 8), sy(40 + 22 * (i % 2))) for i in range(9)]
    S.obj(g, Poly([(sx(-32), sy(236)), (sx(30), sy(238)), (sx(40), sy(150)), (sx(50), sy(50))] + hem[::-1] + [(sx(-58), sy(42)), (sx(-44), sy(150))]),
          coat, seed + 2)
    S.flat(g, Seg(sx(-30), sy(150), sx(36), sy(150), 5 * k), (80, 56, 40))
    S.obj(g, Seg(sx(-28), sy(226), sx(-44), sy(150), 12 * k, 10 * k), coat, seed + 3)
    S.obj(g, Seg(sx(26), sy(226), sx(44), sy(158), 12 * k, 10 * k), coat, seed + 4)
    hand = (sx(48), sy(150))
    S.obj(g, Poly([(sx(-40), sy(232)), (sx(-34), sy(250)), (sx(0), sy(258)), (sx(34), sy(250)), (sx(42), sy(226)), (sx(10), sy(212)), (sx(-34), sy(208))]),
          tint_of(coat, 0.2), seed + 5)
    hx, hy = sx(4), sy(272)
    S.obj(g, Ell(hx, hy, 15 * k, 18 * k), (240, 214, 190), seed + 6)
    S.obj(g, Poly([(hx - 17 * k, hy - 1 * k), (hx + 17 * k, hy - 1 * k), (hx + 18 * k, hy + 20 * k), (hx - 16 * k, hy + 24 * k)]), scarf, seed + 7)
    S.flat(g, Seg(hx + f * 3 * k, hy - 5 * k, hx + f * 11 * k, hy - 5 * k, 1.8 * k), INK)
    S.obj(g, Union([Ell(hx, hy - 15 * k, 34 * k, 7 * k), Box(hx - 16 * k, hy - 36 * k, hx + 16 * k, hy - 14 * k, 5 * k)]), hat, seed + 8)
    if weapon == "axe":
        S.obj(g, Seg(hand[0], hand[1], sx(-10), sy(330), 3.6 * k), (140, 100, 60), seed + 9)
        S.obj(g, Poly([(sx(-16), sy(318)), (sx(-52), sy(338)), (sx(-60), sy(300)), (sx(-38), sy(296)), (sx(-12), sy(306))]), (200, 206, 220), seed + 10, hi=True)
    S.obj(g, Ell(hand[0], hand[1], 7 * k, 7 * k), (50, 44, 40), seed + 11)


def beast(g, x, base, h, face=-1, fur=(70, 60, 80), eyes=(255, 210, 90), seed=0):
    """Toon beast: hunched wolf-like silhouette with spiky fur edge and glowing eyes (original design)."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    S.shadow(g, Ell(x, base, 90 * k, 10 * k))
    body = Union([Ell(sx(-10), sy(170), 62 * k, 80 * k), Ell(sx(20), sy(230), 44 * k, 40 * k),
                  Poly([(sx(-40), sy(120)), (sx(-60), sy(60)), (sx(-40), sy(4)), (sx(-20), sy(4)), (sx(-24), sy(60)), (sx(0), sy(110))]),
                  Poly([(sx(10), sy(110)), (sx(30), sy(60)), (sx(16), sy(4)), (sx(38), sy(4)), (sx(46), sy(64)), (sx(34), sy(120))]),
                  Seg(sx(40), sy(220), sx(84), sy(130), 16 * k, 11 * k), Seg(sx(84), sy(130), sx(96), sy(70), 11 * k, 9 * k),
                  Seg(sx(-30), sy(210), sx(-70), sy(140), 15 * k, 10 * k), Seg(sx(-70), sy(140), sx(-74), sy(80), 10 * k, 8 * k),
                  Ell(sx(56), sy(258), 26 * k, 20 * k), Poly([(sx(66), sy(262)), (sx(108), sy(246)), (sx(108), sy(236)), (sx(66), sy(240))]),
                  Poly([(sx(40), sy(270)), (sx(36), sy(304)), (sx(54), sy(276))]), Poly([(sx(56), sy(272)), (sx(60), sy(306)), (sx(70), sy(272))])])
    spikes = Union([Poly([(sx(-60 + i * 12), sy(196 + 40 * math.sin(i * 0.4))), (sx(-66 + i * 12), sy(222 + 40 * math.sin(i * 0.4))),
                          (sx(-52 + i * 12), sy(200 + 40 * math.sin(i * 0.4)))]) for i in range(8)])
    S.obj(g, Union([body, spikes]), fur, seed, hi=True)
    for cx_, cy_ in ((sx(96), sy(66)), (sx(-74), sy(76))):
        for i in range(3):
            S.flat(g, Seg(cx_ + (i - 1) * 5 * k, cy_, cx_ + (i - 1) * 7 * k + f * 4 * k, cy_ + 14 * k, 2.4 * k, 0.6 * k), (240, 236, 220))
    ex, ey = sx(70), sy(258)
    g.glow(ex, ey, 22 * k, eyes, 0.8)
    S.obj(g, Ell(ex, ey, 7 * k, 4.5 * k), eyes, seed + 1, line=False)


def statue(g, x, base, h, col=(170, 170, 186), seed=0, sword=True):
    k = h / 200.0
    S.obj(g, Poly([(x - 30 * k, base), (x - 22 * k, base - 110 * k), (x - 18 * k, base - 150 * k), (x + 18 * k, base - 150 * k), (x + 22 * k, base - 110 * k), (x + 30 * k, base)]),
          col, seed)
    S.obj(g, Union([Ell(x, base - 160 * k, 13 * k, 16 * k), Poly([(x - 20 * k, base - 146 * k), (x, base - 182 * k), (x + 20 * k, base - 146 * k)])]), col, seed + 1)
    S.flat(g, Ell(x + 2 * k, base - 158 * k, 8 * k, 11 * k), shade_of(col, 0.45))
    if sword:
        S.obj(g, Union([Seg(x, base - 104 * k, x, base - 4 * k, 4.5 * k, 2.5 * k), Box(x - 18 * k, base - 112 * k, x + 18 * k, base - 106 * k)]), tint_of(col, 0.2), seed + 2)


def moon(g, x, y, r, col=(250, 246, 220)):
    g.glow(x, y, r * 3.2, (170, 180, 255), 0.4)
    S.obj(g, Circ(x, y, r), col, 7, line=False, hi=True)
    for cx, cy, cr in ((x - r * 0.3, y - r * 0.2, r * 0.18), (x + r * 0.25, y + r * 0.3, r * 0.12), (x + r * 0.35, y - r * 0.35, r * 0.08)):
        S.flat(g, Circ(cx, cy, cr), shade_of(col, 0.9))


def spire(g, cx, base, w, h, col):
    S.obj(g, Union([Box(cx - w / 2, base - h * 0.32, cx + w / 2, base), Poly([(cx - w * 0.42, base - h * 0.32), (cx, base - h), (cx + w * 0.42, base - h * 0.32)])]), col, 9)
    S.obj(g, Union([Box(cx - w * 0.15, base - h * 0.25, cx + w * 0.15, base - h * 0.08), Circ(cx, base - h * 0.25, w * 0.15)]), (255, 210, 130), 10)


def banner(g, x, top, w, h, col):
    S.line(g, x - w * 0.6, top, x + w * 0.6, top, 2, (90, 70, 50))
    S.obj(g, Poly([(x - w / 2, top), (x + w / 2, top), (x + w / 2, top + h), (x, top + h * 0.82), (x - w / 2, top + h)]), col, 11)
    S.flat(g, Circ(x, top + h * 0.4, w * 0.24) - Circ(x + w * 0.1, top + h * 0.36, w * 0.2), (240, 236, 210))


def candle(g, x, base, h, w=6, lit=True, static_flame=False):
    S.obj(g, Box(x - w / 2, base - h, x + w / 2, base, 1), (250, 244, 226), 12)
    if lit:
        g.glow(x, base - h - 6, 26, FIRE, 0.35)
        if static_flame:
            S.obj(g, Union([Ell(x, base - h - 4, 3.5, 4.5), Poly([(x - 3.5, base - h - 5), (x, base - h - 15), (x + 3.5, base - h - 5)])]), (255, 200, 90), 13, line=False)


# =================================================================== Level 1620 forbidden woods (toon of Level1569)
def l1620(g, d):
    S.sky(g, [(0, (24, 30, 60)), (300, (50, 70, 90)), (420, (70, 96, 110))])
    for i, (base, col) in enumerate(((360, (44, 60, 84)), (390, (34, 48, 70)))):
        rnd = random.Random(6901 + i)
        x = -20
        trees = []
        while x < 920:
            h = rnd.uniform(70, 120) - i * 20
            trees.append(Poly([(x - 16, base), (x, base - h), (x + 16, base)]))
            x += rnd.uniform(18, 30)
        S.obj(g, Union(trees + [Box(-20, base - 4, 920, base + 40)]), col, 6901 + i, depth=0.5 - i * 0.2, line=False)
    S.ground(g, Box(-2, 380, W + 2, H + 2), (50, 76, 66), "grass", 6903)
    S.ground(g, Poly([(380, 384), (470, 384), (700, 610), (160, 610)]), (120, 104, 90), "dirt", 6904, line=True)
    for x, h, s, lean in ((80, 600, 6906, 0.1), (840, 620, 6907, -0.12), (250, 420, 6908, 0.05), (640, 440, 6909, -0.05)):
        toon_tree(g, x, 420 if h < 500 else 600, h, col=(46, 42, 58), lean=lean, seed=s)
    # hut with a lit window
    hx = 520
    S.obj(g, Box(hx, 330, hx + 80, 386), (90, 76, 70), 6910)
    S.obj(g, Poly([(hx - 10, 334), (hx + 40, 296), (hx + 90, 334)]), (70, 56, 66), 6911)
    S.obj(g, Box(hx + 50, 300, hx + 60, 320), (90, 76, 70), 6912)
    if "hut" not in d:
        g.glow(hx + 22, 354, 44, FIRE, 0.35)
    S.obj(g, Box(hx + 12, 344, hx + 32, 364, 2), (255, 200, 120) if "hut" not in d else (40, 44, 60), 6913)
    # fence
    for x in range(170, 380, 30):
        t = (x - 170) / 210
        S.obj(g, Box(x - 4 + t * 1.6, 560 - 170 * t - (60 - 30 * t), x + 4 - t * 1.6, 560 - 170 * t), (150, 116, 80), 6914 + x)
    S.line(g, 170, 528, 380, 372, 2.4, (150, 116, 80))
    S.line(g, 170, 546, 380, 380, 2.0, (150, 116, 80))
    # lantern posts
    for x, y, hgt, key in ((260, 480, 140, "lamp"), (440, 396, 60, None)):
        s = hgt / 140
        S.obj(g, Union([Seg(x, y, x, y - hgt, 3.4 * s), Seg(x, y - hgt, x + 22 * s, y - hgt, 2.4 * s)]), (90, 70, 56), 6920 + x)
        lantern(g, x + 20 * s, y - hgt + 12 * s, s * 1.1, lit=not (key and key in d))
    # cages
    cage(g, 150, 150, 46, 80, chain_len=80)
    if "cage" not in d:
        cage(g, 760, 190, 44, 76, chain_len=110)
    # eyes in the dark
    for ex, ey, show in ((70, 470, True), (870, 440, "eyes" not in d)):
        if show:
            for dx in (-10, 10):
                g.glow(ex + dx, ey, 18, (255, 220, 90), 0.8)
                S.obj(g, Ell(ex + dx, ey, 6, 4), (255, 236, 150), 6930, line=False)
    # sign post
    S.obj(g, Box(676, 440, 684, 520, 2), (150, 116, 80), 6931)
    ang = 0.2 if "sign" not in d else -0.25
    S.obj(g, Poly([(680, 450), (744, 450 + 64 * ang), (758, 460 + 64 * ang), (744, 470 + 64 * ang), (680, 470)]), (200, 160, 110), 6932)
    # mushrooms
    mcol = (230, 70, 70) if "mush" not in d else (240, 220, 140)
    for mx_, s in ((262, 1.6), (292, 1.1), (236, 1.0)):
        S.obj(g, Box(mx_ - 2.4 * s, 568 - 14 * s, mx_ + 2.4 * s, 568), (240, 234, 220), 6933)
        S.obj(g, Inter(Ell(mx_, 568 - 14 * s, 12 * s, 10 * s), Box(mx_ - 14 * s, 552 - 14 * s, mx_ + 14 * s, 568 - 14 * s)), mcol, 6934, hi=True)
        S.flat(g, Circ(mx_ - 4 * s, 562 - 18 * s, 2 * s), (255, 250, 240))


L1620_EL = [mist_el("mist1", 420, 40, (150, 180, 190), alpha=0.3), mist_el("mist2", 560, 30, (120, 150, 160), alpha=0.25, speed=0.04),
            sparkle_el("flies", [(360, 330), (480, 440), (620, 360), (220, 420)], col=(210, 255, 150), r=4, speed=0.5)]
L1620_DIFFS = [("cage", 760, 225, 0), ("hut", 542, 354, 0), ("lamp", 282, 362, 0), ("eyes", 870, 440, 0), ("sign", 716, 460, 0),
               ("mush", 262, 548, 0)]


# =================================================================== Level 1621 forbidden library (toon of Level1571)
def bookshelf(g, x0, x1, y0, y1, seed, shelf=74, wood=(140, 96, 66)):
    rnd = random.Random(seed)
    S.obj(g, Box(x0, y0, x1, y1), wood, seed)
    cols = [(200, 70, 70), (70, 100, 170), (90, 150, 90), (220, 170, 80), (140, 90, 160), (80, 80, 96), (230, 210, 170)]
    y = y0 + 8
    while y + shelf <= y1 - 4:
        S.flat(g, Box(x0 + 6, y, x1 - 6, y + shelf - 8), shade_of(wood, 0.45))
        x = x0 + 8
        books = []
        while x < x1 - 14:
            bw = rnd.uniform(8, 15)
            bh = rnd.uniform(0.65, 0.95) * (shelf - 10)
            books.append((Box(x, y + shelf - 8 - bh, min(x + bw, x1 - 8), y + shelf - 8, 1), cols[rnd.randrange(len(cols))]))
            x += bw + 1
        for b, c in books:
            cel(g, b, c, w=1.2, off=(-2.5, 0))
        S.obj(g, Box(x0, y + shelf - 8, x1, y + shelf - 2), tint_of(wood, 0.15), seed + 1)
        y += shelf


def l1621(g, d):
    S.obj(g, Box(-2, -2, W + 2, 470), (70, 62, 86), 7100, line=False)
    x0, y0, x1, y1 = 380, 60, 520, 300
    w_shape = arch(x0, x1, y0 + 70, y1)
    S.obj(g, Diff(arch(x0 - 12, x1 + 12, y0 + 70, y1 + 8), w_shape), (130, 124, 140), 7101)
    g.fill(w_shape, vgrad([(y0, (40, 60, 130)), (y1, (100, 120, 190))]))
    moon(g, 470, 130, 22)
    S.obj(g, Inter(Union([Box(447, y0, 453, y1), Box(x0, 180, x1, 185), Box(x0, 240, x1, 245)]), w_shape), (70, 56, 60), 7102)
    bookshelf(g, -10, 360, 20, 460, 7104)
    bookshelf(g, 540, 910, 20, 460, 7105)
    for x0_, x1_ in ((-10, 360), (540, 910)):
        S.obj(g, Box(x0_, 236, x1_, 246), (110, 76, 52), 7106)
        S.obj(g, Union([Box(x, 214, x + 4, 236) for x in range(x0_ + 10, x1_, 22)] + [Box(x0_, 208, x1_, 214)]), (130, 90, 60), 7107)
    if "scroll" not in d:
        S.obj(g, Box(636, 354, 716, 370, 8), (246, 232, 196), 7108, hi=True)
        S.flat(g, Box(672, 352, 680, 372), (200, 60, 60))
    # ladder
    for sx_ in (0, 1):
        S.obj(g, Seg(180 + sx_ * 46, 470, 230 + sx_ * 46, 40, 4.5), (190, 140, 90), 7109 + sx_)
    for i in range(1, 12):
        if "rung" in d and i in (5, 6):
            continue
        t = i / 12
        S.obj(g, Seg(180 + 50 * t, 470 - 430 * t, 226 + 50 * t, 470 - 430 * t, 3), (210, 160, 100), 7111)
    S.ground(g, Box(-2, 460, W + 2, H + 2), (150, 100, 70), "wood", 7112, line=True)
    # chandelier
    S.line(g, 450, -2, 450, 70, 1.6, (90, 80, 70))
    S.obj(g, Ell(450, 90, 72, 11) - Ell(450, 88, 62, 6), (230, 190, 90), 7113)
    for i, cx in enumerate((390, 420, 450, 480, 510)):
        if "chand" in d and i == 3:
            continue
        candle(g, cx, 88, 20, w=7)
    # reading desk with an open book
    S.shadow(g, Ell(450, 560, 220, 20))
    S.obj(g, Box(250, 470, 650, 494, 2), (170, 120, 80), 7114, "wood")
    for lx in (270, 610):
        S.obj(g, Box(lx, 494, lx + 18, 580), (140, 96, 66), 7115, "wood")
    S.obj(g, Poly([(360, 470), (450, 462), (450, 440), (366, 446)]), (250, 244, 226), 7116)
    S.obj(g, Poly([(450, 462), (540, 470), (534, 446), (450, 440)]), (244, 236, 214), 7117)
    for k in range(4):
        S.flat(g, Seg(378, 452 + k * 4, 440, 448 + k * 4, 0.8), (160, 140, 120))
        S.flat(g, Seg(460, 448 + k * 4, 522, 452 + k * 4, 0.8), (160, 140, 120))
    if "ribbon" not in d:
        S.obj(g, Poly([(450, 462), (460, 462), (460, 500), (455, 492), (450, 500)]), (220, 50, 60), 7118)
    candle(g, 300, 470, 30, w=10)
    # hourglass
    hx, hy = 590, 470
    S.obj(g, Union([Box(hx - 17, hy - 8, hx + 17, hy), Box(hx - 17, hy - 66, hx + 17, hy - 58)]), (150, 110, 70), 7119)
    S.obj(g, Poly([(hx - 12, hy - 58), (hx + 12, hy - 58), (hx + 2, hy - 33), (hx + 12, hy - 8), (hx - 12, hy - 8), (hx - 2, hy - 33)]), (200, 230, 250), 7120, hi=True)
    sand = (250, 200, 110)
    if "sand" not in d:
        S.flat(g, Poly([(hx - 11, hy - 9), (hx + 11, hy - 9), (hx + 5, hy - 22), (hx - 5, hy - 22)]), sand)
        S.flat(g, Poly([(hx - 7, hy - 52), (hx + 7, hy - 52), (hx + 1, hy - 37), (hx - 1, hy - 37)]), sand)
    else:
        S.flat(g, Poly([(hx - 11, hy - 57), (hx + 11, hy - 57), (hx + 2, hy - 36), (hx - 2, hy - 36)]), sand)
    # globe
    gx, gy = 780, 400
    S.obj(g, Union([Seg(gx, gy + 40, gx, gy + 140, 4.5), Seg(gx - 40, gy + 160, gx, gy + 140, 4.5), Seg(gx + 40, gy + 160, gx, gy + 140, 4.5)]),
          (170, 120, 80) if "globe" not in d else (190, 196, 210), 7121)
    S.obj(g, Circ(gx, gy, 40), (110, 170, 220), 7122, hi=True)
    S.obj(g, Union([Rough(Ell(gx - 8, gy - 6, 18, 14), 4, 6, 7107), Rough(Ell(gx + 16, gy + 16, 10, 12), 3, 5, 7108)]), (120, 190, 110), 7123, line=False)
    S.obj(g, Circ(gx, gy, 46) - Circ(gx, gy, 42), (230, 190, 90), 7124)
    # stack of books
    for i, (c, w) in enumerate((((200, 70, 70), 70), ((70, 100, 170), 64), ((220, 170, 80), 58))):
        if "stack" in d and i == 2:
            continue
        y = 580 - i * 15
        S.obj(g, Box(90 - w / 2, y - 15, 90 + w / 2, y, 2), c, 7125 + i)
        S.flat(g, Box(90 - w / 2 + 3, y - 12, 90 + w / 2, y - 4), (250, 244, 226))


L1621_EL = [flame_el("deskc", 300, 440, 1.2, 0.1),
            E("beam", el(lambda g, m: g.fill(Poly([(400, 220), (500, 220), (600, 590), (300, 590)]), (200, 210, 255), alpha=0.12, feather=20)),
              daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.12)),
            sparkle_el("dust", [(420, 340), (480, 400), (450, 300), (500, 360)], col=(230, 236, 255), r=3, speed=0.5)] + \
           [flame_el("ch%d" % i, cx, 68, 0.8, i * 0.2) for i, cx in enumerate((390, 420, 450, 510))]
L1621_DIFFS = [("chand", 480, 64, 0), ("rung", 222, 262, 0), ("scroll", 676, 362, 0), ("ribbon", 455, 482, 0), ("sand", 590, 437, 0),
               ("globe", 780, 520, 0), ("stack", 90, 552, 0)]


# =================================================================== Level 1622 duel on the bridge (toon of Level1573)
def l1622(g, d):
    S.sky(g, [(0, (20, 26, 70)), (250, (60, 70, 130)), (400, (100, 110, 160))])
    rnd = random.Random(7301)
    for _ in range(50):
        S.flat(g, Circ(rnd.uniform(0, 900), rnd.uniform(0, 300), rnd.uniform(0.8, 2.0)), (255, 250, 230))
    moon(g, 450, 200, 110)
    S.obj(g, cloud_shape(250, 330, 140, 16, 3), (150, 160, 210), 3, "cloud", line=False)
    # city skyline silhouette
    x = -10
    parts, wins = [], []
    while x < 910:
        w = rnd.uniform(24, 50)
        h = rnd.uniform(60, 160)
        parts.append(Box(x, 420 - h, x + w, 430))
        if rnd.random() < 0.5:
            parts.append(Poly([(x + w * 0.2, 420 - h + 1), (x + w / 2, 420 - h - w * 1.2), (x + w * 0.8, 420 - h + 1)]))
        for wy in np.arange(420 - h + 10, 410, 16):
            if rnd.random() < 0.3:
                wins.append(Box(x + w * 0.4, wy, x + w * 0.4 + 5, wy + 7))
        x += w * rnd.uniform(0.8, 1.05)
    S.obj(g, Union(parts), (46, 52, 90), 7304, line=False)
    if wins:
        S.flat(g, Union(wins), (255, 210, 120))
    if "spire" not in d:
        spire(g, 740, 330, 34, 200, (56, 62, 100))
    # bridge
    S.obj(g, Box(-20, 470, W + 20, 520), (140, 136, 156), 7306, "stone")
    S.obj(g, Box(-20, 520, W + 20, H + 20), (60, 60, 84), 7307, line=False)
    for ax in range(-60, 960, 180):
        S.obj(g, arch(ax + 20, ax + 160, 560, 640, pointed=False), (24, 24, 40), 7308, line=False)
    S.obj(g, Box(-20, 430, W + 20, 444), (176, 172, 190), 7309)
    S.obj(g, Union([Box(x + 3, 444, x + 11, 470, 3) for x in range(-10, 910, 18)]), (160, 156, 176), 7310)
    for x, key in ((90, "lamp"), (810, None)):
        S.obj(g, Box(x - 14, 400, x + 14, 470), (150, 146, 166), 7311 + x, "stone")
        S.obj(g, Box(x - 3, 280, x + 3, 402), (50, 48, 60), 7312 + x)
        lantern(g, x, 260, 1.4, lit=not (key and key in d))
    if "statue" not in d:
        statue(g, 330, 432, 120)
    banner(g, 810, 300, 32, 72, (200, 50, 60) if "banner" not in d else (60, 100, 190))
    hunter(g, 230, 516, 230, face=1, scarf=(110, 100, 90) if "scarf" not in d else (210, 60, 70), seed=7313)
    beast(g, 640, 516, 300, face=-1, eyes=(255, 210, 90) if "eyes" not in d else (130, 230, 255), seed=7314)


L1622_EL = [bat_el("bat1", 200, 80, s=12, speed=28, phase=0.1), bat_el("bat2", 230, 100, s=8, speed=28, phase=0.13),
            mist_el("mist", 520, 40, (140, 150, 200), alpha=0.3),
            flame_el("lampR", 810, 286, 1.2, 0.3)]
L1622_DIFFS = [("spire", 740, 230, 0), ("lamp", 90, 276, 0), ("statue", 330, 380, 0), ("banner", 810, 330, 0), ("scarf", 234, 340, 0),
               ("eyes", 592, 290, 0)]


# =================================================================== Level 1623 moonlit chapel (toon of Level1574)
WINS = [(150, 70, 230, 330), (410, 40, 490, 300), (670, 70, 750, 330)]


def l1623(g, d):
    S.obj(g, Box(-2, -2, W + 2, 430), (84, 80, 104), 7400, "stone", line=False)
    for i, (x0, y0, x1, y1) in enumerate(WINS):
        sh = arch(x0, x1, y0 + (x1 - x0), y1)
        S.obj(g, Diff(arch(x0 - 12, x1 + 12, y0 + (x1 - x0), y1 + 8), sh), (150, 146, 168), 7401 + i)
        rnd = random.Random(7410 + i)
        cols = [(80, 120, 220), (220, 70, 80), (250, 210, 90), (90, 190, 130), (170, 110, 210)]
        for gx in np.arange(x0, x1, 16):
            for gy in np.arange(y0 - 10, y1, 20):
                c = rnd.choice(cols)
                if i == 0 and "glass" in d and 200 < gy < 270:
                    c = (250, 230, 120)
                S.flat(g, Inter(Box(gx, gy, gx + 16, gy + 20), sh), c)
        S.flat(g, Inter(Union([Box(x, y0 - 40, x + 1.6, y1) for x in np.arange(x0, x1, 16)] + [Box(x0, y, x1, y + 1.6) for y in np.arange(y0 - 10, y1, 20)]), sh), INK)
        if i == 1:
            S.obj(g, Circ(450, 150, 22), (250, 244, 210), 7420)
    # floor
    S.obj(g, Box(-2, 430, W + 2, H + 2), (110, 104, 130), 7421, line=False)
    for i in range(-12, 13):
        S.flat(g, Seg(450 + i * 12, 430, 450 + i * 90, 610, 1), (80, 76, 100))
    for y in (440, 456, 478, 506, 542, 590):
        S.flat(g, Seg(-2, y, W + 2, y, 1), (80, 76, 100))
    # altar and candelabra
    S.obj(g, Box(330, 340, 570, 350), (220, 212, 200), 7422)
    S.obj(g, Box(340, 350, 560, 430), (200, 192, 184), 7423, "stone")
    S.obj(g, Box(380, 360, 520, 420), (190, 40, 60), 7424)
    S.flat(g, Union([Box(446, 366, 454, 414), Box(420, 386, 480, 392)]), (250, 210, 90))
    for cx, lit in ((370, True), (530, "candle" not in d)):
        S.obj(g, Union([Seg(cx, 340, cx, 290, 3), Seg(cx - 18, 300, cx + 18, 300, 2), Box(cx - 10, 334, cx + 10, 340)]), (230, 190, 90), 7425)
        for dx in (-18, 0, 18):
            candle(g, cx + dx, 300 if dx else 292, 22, w=7, lit=lit, static_flame=(cx == 530))
    if "chalice" not in d:
        S.obj(g, Union([Poly([(436, 308), (464, 308), (457, 326), (443, 326)]), Box(447, 326, 453, 336), Box(440, 336, 460, 341)]), (250, 210, 90), 7426, hi=True)
    # pews
    for row in range(5):
        t = row / 4
        y = 450 + 150 * t ** 1.2
        hgt = 26 + 50 * t
        for side in (-1, 1):
            xa, xb = 450 + side * (60 + 40 * t), 450 + side * (220 + 300 * t)
            S.obj(g, Box(min(xa, xb), y - hgt, max(xa, xb), y - hgt * 0.4), (160, 106, 70), 7430 + row, "wood")
            S.obj(g, Box(min(xa, xb), y - hgt * 0.4, max(xa, xb), y), (110, 72, 50), 7435 + row)
            if row == 3 and side == 1 and "book" not in d:
                bx = (xa + xb) / 2
                S.obj(g, Box(bx - 24, y - hgt - 12, bx + 24, y - hgt, 2), (200, 50, 60), 7440)
    # flower vase
    S.obj(g, Box(250, 360, 290, 430), (200, 192, 184), 7441, "stone")
    S.obj(g, Union([Ell(270, 346, 12, 14), Box(264, 330, 276, 340)]), (220, 226, 240), 7442, hi=True)
    fc = (230, 60, 90) if "flowers" not in d else (250, 244, 230)
    for fx, fy in ((254, 314), (270, 304), (286, 314), (262, 324), (280, 324)):
        S.line(g, 270, 332, fx, fy, 1, (70, 130, 70))
        S.obj(g, Circ(fx, fy, 7), fc, 7443)
    # censer
    S.line(g, 640, 0, 640, 276, 1.2, (180, 150, 80))
    if "censer" not in d:
        S.obj(g, Union([Ell(640, 298, 16, 14), Poly([(626, 290), (640, 268), (654, 290)])]), (230, 190, 90), 7444, hi=True)


def beam(eid, x0, y0, x1, y1, w0, w1, col, phase=0.0):
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    pts = [(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)]
    return E(eid, el(lambda g, m: g.fill(Poly(pts), col, alpha=0.14, feather=14)), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.12, phase=phase))


L1623_EL = [beam("beamL", 190, 200, 260, 560, 60, 160, (220, 200, 255)), beam("beamC", 450, 180, 450, 560, 60, 180, (220, 220, 255), 0.4),
            beam("beamR", 710, 200, 640, 560, 60, 160, (255, 220, 220), 0.7),
            sparkle_el("dust", [(430, 380), (470, 420), (220, 400), (680, 420)], col=(240, 236, 255), r=3, speed=0.5),
            E("smoke", el(lambda g, m: S.obj(g, Circ(640, 272, 7), (230, 230, 240), 1, line=False)), daynight="untinted",
              anim=dict(driftVelocity=(3, 30), driftLength=60, driftFade=True, driftGrow=1.5))] + \
           [flame_el("c%d" % i, x, y, 0.8, i * 0.15) for i, (x, y) in enumerate(((352, 280), (370, 272), (388, 280)))]
L1623_DIFFS = [("glass", 190, 236, 0), ("candle", 530, 270, 0), ("chalice", 450, 324, 0), ("book", 775, 466, 0), ("flowers", 270, 314, 0),
               ("censer", 640, 290, 0)]


LEVELS = [
    ("Level1620", "卡通·禁林提灯", make(l1620), L1620_EL, L1620_DIFFS, 60, OPTS),
    ("Level1621", "卡通·禁书库", make(l1621), L1621_EL, L1621_DIFFS, 60, OPTS),
    ("Level1622", "卡通·桥上对峙", make(l1622), L1622_EL, L1622_DIFFS, 60, OPTS),
    ("Level1623", "卡通·月光礼拜堂", make(l1623), L1623_EL, L1623_DIFFS, 60, OPTS),
]
