# -*- coding: utf-8 -*-
"""Realistic gothic moonlight levels, set 3 - following the five-star favourites (Level1516-1519, 1565-1573, 1582):
moonlit interiors and exteriors with volumetric god rays, rich props, original designs, no gore.
  Level1624 钟楼机芯   - inside a clock tower: the back-lit clock face throws moonbeams over giant gears
  Level1625 月下回廊   - a monastery cloister: moonbeams through the arcade onto a fountain garden
  Level1626 炼金地窖   - an alchemist's vaulted cellar: barred window moonbeam, glassware, cauldron
  Level1627 肖像长廊   - a portrait gallery: lancet windows lay stripes of moonlight across the floor
  Level1628 废弃舞厅   - an abandoned ballroom: tall windows, a fallen chandelier, a grand piano
  Level1629 断崖修道院 - a monastery on a sea cliff under the full moon, lantern path, a monk
  Level1630 雾夜车站   - a Victorian station: iron-and-glass roof, a steam locomotive, gas lamps
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (C, Box, Circ, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm, fbm1,
                  grain_tex, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint, tex, vgrad)
from real_kit import blades, cloud_layer, crown, glint_el, mist_el, planks, ridge, rock, sky, stars, water
from levels_real2 import (arch, ashlar, bat_el, beam_el, candle, cobweb, flame, flame_el, fog_band, make_bg, moon,
                          moon_receive, motes_el, persp_floor, rim, stains, stone_band)
from souls_kit import (FIRE, IRON, MOON, banner, barrel, chain, crate, crow, emblem_moon, gas_lamp, lancet, n1, spire,
                       statue, stone, wall)

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)
WARM = (255, 200, 130)


def gear(g, cx, cy, r, teeth, col=(120, 96, 60), seed=0, spokes=5, hub=None, skip_spoke=None):
    """Toothed brass gear with spokes."""
    tw = r * 0.16
    parts = [Circ(cx, cy, r)]
    for i in range(teeth):
        a = i * math.tau / teeth
        ca, sa = math.cos(a), math.sin(a)
        p = [(cx + ca * (r - 2) - sa * tw / 2, cy + sa * (r - 2) + ca * tw / 2), (cx + ca * (r + tw) - sa * tw * 0.35, cy + sa * (r + tw) + ca * tw * 0.35),
             (cx + ca * (r + tw) + sa * tw * 0.35, cy + sa * (r + tw) - ca * tw * 0.35), (cx + ca * (r - 2) + sa * tw / 2, cy + sa * (r - 2) - ca * tw / 2)]
        parts.append(Poly(p))
    rim_ring = Union(parts) - Circ(cx, cy, r * 0.78)
    paint = tex(sphere_paint(cx - r * 0.3, cy - r * 0.3, r * 1.2, col, amb=0.35, spec=0.5, shin=20), 0.15, 3, 3, 3, seed)
    g.fill(rim_ring, paint)
    sp = [Seg(cx, cy, cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8, r * 0.07) for k, a in
          enumerate(np.linspace(0, math.tau, spokes, endpoint=False) + 0.3) if k != skip_spoke]
    g.fill(Union(sp + [Circ(cx, cy, r * 0.2)]), paint)
    g.fill(Circ(cx, cy, r * 0.08), hub or (30, 26, 24))
    rim(g, rim_ring, -2, -1, col=MOON, k=0.35)


def floor_planks(g, y0, col=(70, 54, 42), seed=0):
    g.fill(Box(-2, y0, W + 2, H + 2), planks("h", col, seed=seed, width=16))
    g.fill(Box(-2, y0, W + 2, H + 2), (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.35 * smooth(H, y0, Y))


def light_pool(g, pts, col=(170, 186, 232), k=0.22):
    g.add(Poly(pts), col, k, feather=10)


# =================================================================== Level 1624 clock tower movement
FACE24 = (450, 230, 170)


def l1624_scene(g, d):
    cx, cy, r = FACE24
    g.fill(Box(-2, -2, W + 2, H + 2), ashlar((50, 46, 52), 28, 13, 2401))
    g.fill(Box(-2, -2, W + 2, H + 2), (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.4 * (np.hypot(X - cx, Y - cy) / 520) ** 1.2)
    # back-lit translucent clock face
    face = Circ(cx, cy, r)
    g.fill(face, rgrad(cx + 40, cy - 30, r * 1.1, [(0, (236, 236, 222)), (0.7, (190, 196, 214)), (1, (140, 148, 176))]))
    g.glow(cx + 60, cy - 50, 90, (255, 255, 240), 0.35)
    ring = Circ(cx, cy, r + 14) - Circ(cx, cy, r)
    g.fill(ring, tex(light_x((80, 70, 60), cx - r, cx + r, 1.2, 0.7), 0.2, 3, 3))
    marks = []
    for i in range(12):
        a = i * math.tau / 12 - math.pi / 2
        x0_, y0_ = cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78
        x1_, y1_ = cx + math.cos(a) * r * 0.94, cy + math.sin(a) * r * 0.94
        marks.append(Seg(x0_, y0_, x1_, y1_, 5 if i % 3 == 0 else 3))
    spokes = [Seg(cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r, 2.2) for a in np.linspace(0, math.tau, 8, endpoint=False)]
    g.fill(Union(marks + spokes + [Circ(cx, cy, r * 0.62) - Circ(cx, cy, r * 0.6)]), (34, 30, 30))
    ha = -math.pi / 2 + 1.1
    ma = -math.pi / 2 + (4.4 if "hand" not in d else 3.0)
    g.fill(Union([Seg(cx, cy, cx + math.cos(ha) * r * 0.5, cy + math.sin(ha) * r * 0.5, 8, 4), Seg(cx, cy, cx + math.cos(ma) * r * 0.82, cy + math.sin(ma) * r * 0.82, 6, 2.5),
                  Circ(cx, cy, 12)]), (30, 26, 26))
    # beams and floor
    g.fill(Box(-2, 70, W + 2, 92), tex(light_y((80, 62, 46), 70, 92, 1.2, 0.6), 0.2, 2, 6))
    floor_planks(g, 470, seed=2402)
    light_pool(g, [(330, 470), (570, 470), (720, 610), (180, 610)])
    # gears (foreground, left and right)
    gear(g, 140, 300, 120, 22, seed=2403, skip_spoke=2 if "spoke" in d else None)
    gear(g, 280, 470, 60, 14 if "teeth" not in d else 10, col=(110, 100, 90), seed=2404)
    gear(g, 790, 380, 100, 20, col=(100, 84, 56), seed=2405)
    g.fill(Seg(140, 300, 450, 230, 6), (60, 56, 54))
    # bell rope and ladder
    g.fill(Seg(640, 92, 640, 430, 2.4), (150, 120, 80))
    g.fill(Ell(640, 440, 7, 14), (180, 40, 40) if "rope" not in d else (230, 190, 70))
    for x in (690, 730):
        g.fill(Seg(x, 92, x + 10, 470, 3.6), tex(light_x((110, 82, 54), x - 4, x + 14, 1.2, 0.6), 0.2, 1, 6))
    for k in range(1, 12):
        y = 92 + k * 34
        g.fill(Seg(690 + (y - 92) / 378 * 10, y, 730 + (y - 92) / 378 * 10, y, 2.4), (120, 90, 60))
    # crow on the beam, lantern on the floor
    if "crow" not in d:
        crow(g, 330, 70, 1.3, face=1)
    lx, ly = 560, 520
    g.mul(Ell(lx + 6, ly + 2, 24, 5), 0.5, feather=5)
    if "lantern" not in d:
        g.glow(lx, ly - 18, 60, FIRE, 0.4)
    g.fill(Box(lx - 12, ly - 34, lx + 12, ly, 2), (255, 200, 120) if "lantern" not in d else (50, 54, 66))
    g.fill(Union([Box(lx - 13, ly - 34, lx - 10, ly), Box(lx + 10, ly - 34, lx + 13, ly), Poly([(lx - 15, ly - 34), (lx, ly - 46), (lx + 15, ly - 34)])]), IRON)
    cobweb(g, 900, 92, 80, (-1, 1))


L1624_RAYS = [dict(lx=FACE24[0] + 80, ly=FACE24[1] - 900, col=(190, 200, 236), k=1.4, region=Circ(*FACE24), threshold=110,
                   soft=60, density=0.92, decay=0.97, samples=70, receive=Box(-20, 230, W + 20, H + 20))]


def l1624_pendulum(g, m):
    g.fill(Seg(450, 400, 450, 560, 3), (90, 80, 60))
    g.fill(Circ(450, 570, 20), sphere_paint(444, 564, 20, (170, 140, 70), amb=0.4, spec=0.7))


L1624_ELEMENTS = [
    E("pendulum", el(l1624_pendulum), pivot=(450, 400), anim=dict(swingAngle=10, swingSpeed=0.5)),
    motes_el("dust", [(400, 400), (480, 450), (430, 360), (520, 420)], vx=2, vy=-4, length=24),
    bat_el("bat", 760, 160, s=9, speed=-24, phase=0.3),
    E("gearspin", el(lambda g, m: gear(g, 600, 160, 34, 10, col=(130, 110, 70), seed=2410)), pivot=(600, 160), anim=dict(rotateSpeed=20)),
]
L1624_DIFFS = [("hand", 520, 170, 0), ("spoke", 120, 240, 0), ("teeth", 280, 470, 0), ("rope", 640, 440, 0), ("crow", 336, 52, 0),
               ("lantern", 560, 500, 0)]


# =================================================================== Level 1625 moonlit cloister
M25 = (420, 150, 30)


def l1625_scene(g, d):
    mx, my, mr = M25
    sky(g, [(0, (8, 12, 30)), (200, (30, 40, 70)), (300, (50, 60, 90))])
    stars(g, 60, 220, seed=2501)
    moon(g, mx, my, mr, k=0.8, seed=2502)
    # far wall of the cloister with arches and the roof
    g.fill(Box(-2, 200, W + 2, 380), ashlar((80, 78, 86), 22, 11, 2503))
    g.fill(Box(-2, 200, W + 2, 380), (0, 0, 0), alpha=0.35)
    g.fill(Poly([(-2, 200), (W + 2, 200), (W + 2, 180), (-2, 180)]), (50, 44, 50))
    for x in range(30, 900, 110):
        g.fill(arch(x, x + 70, 290, 380, pointed=False), (16, 16, 24))
    # garden: lawn, path, fountain
    g.fill(Box(-2, 380, W + 2, H + 2), tex(vgrad([(380, (40, 56, 44)), (600, (22, 30, 24))]), 0.35, 4, 3, 4, 2504))
    g.fill(Poly([(410, 380), (490, 380), (560, 600), (340, 600)]), grain_tex(vgrad([(380, (90, 88, 96)), (600, (60, 58, 66))]), 0.15, 2505))
    fx, fy = 450, 470
    g.fill(Ell(fx, fy, 110, 26), light_y((120, 118, 126), fy - 26, fy + 26, 1.2, 0.7))
    water(g, fy - 10, fy + 10, (90, 110, 150), (50, 60, 90), seed=2506, x0=fx - 96, x1=fx + 96)
    g.fill(Box(fx - 10, fy - 90, fx + 10, fy - 10), cyl_paint(fx, 10, (130, 128, 136), amb=0.35, spec=0.2))
    g.fill(Ell(fx, fy - 90, 40, 10), light_y((140, 138, 146), fy - 100, fy - 80, 1.2, 0.7))
    if "angel" not in d:
        statue(g, fx, fy - 92, 70, col=(150, 148, 156), seed=2507, light=-1, arms="pray", plinth=False)
    # rose bushes and an urn
    for x, key in ((150, None), (750, "roses")):
        g.fill(Rough(Ell(x, 450, 70, 36), 6, 10, 2508 + x), tex((40, 70, 46), 0.4, 3, 3, 3, 2509))
        rc = (180, 30, 50) if not (key and key in d) else (240, 230, 220)
        for k in range(7):
            rx, ry = x - 50 + k * 16, 440 + (k % 3) * 8
            g.fill(Circ(rx, ry, 6), sphere_paint(rx - 2, ry - 2, 6, rc, amb=0.4, spec=0.2))
    if "urn" not in d:
        g.fill(Union([Ell(300, 420, 18, 20), Box(290, 438, 310, 456)]), sphere_paint(294, 414, 20, (140, 138, 146), ry=22, amb=0.4, spec=0.2))
    if "bench" not in d:
        g.fill(Box(560, 420, 660, 430, 2), (90, 70, 56))
        g.fill(Union([Box(566, 430, 572, 452), Box(648, 430, 654, 452), Box(560, 400, 660, 406)]), (80, 62, 50))
    # foreground arcade framing the view
    col = (110, 106, 114)
    for x0 in (-60, 260, 580):
        a = Diff(Box(x0 - 30, -2, x0 + 280, 600), arch(x0 + 30, x0 + 250, 130, 640, pointed=False))
        wall(g, a, col, 2510 + x0, x0, x0 + 280, light=1)
        rim(g, a, -2, 0, k=0.25)
    for x in (30, 250, 330, 570, 650, 870):
        g.fill(Box(x - 14, 300, x + 14, 600), cyl_paint(x, 14, (130, 126, 134), amb=0.35, spec=0.2))
    if "lantern" not in d:
        g.fill(Seg(620, 250, 620, 290, 1.4), IRON)
        g.glow(620, 304, 40, FIRE, 0.4)
        g.fill(Box(610, 290, 630, 318, 2), (255, 200, 120))
    if "crow" not in d:
        crow(g, 200, 120, 1.2, face=1)
    if "ivy" not in d:
        g.fill(Rough(Ell(860, 160, 36, 70), 8, 10, 2511), tex((40, 70, 40), 0.4, 3, 3, 3, 2512))


L1625_RAYS = [dict(lx=M25[0], ly=M25[1], col=(170, 186, 232), k=1.4, region=Box(-2, -2, W + 2, 200), threshold=80,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=moon_receive(*M25, floor=0.3))]
L1625_ELEMENTS = [
    E("spout", el(lambda g, m: [g.fill(Seg(450 + s * 4, 380, 450 + s * 30, 460, 1.2), (190, 210, 240), alpha=0.6) for s in (-1, 1)]), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=1.5)),
    glint_el("water", [(410, 468), (490, 472)], col=(220, 230, 255), r=4, speed=0.6),
    bat_el("bat", 300, 60, s=9, speed=26, phase=0.2),
    mist_el("mist", 450, 400, 400, 12, (110, 120, 150), alpha=0.35, length=70, seed=25),
]
L1625_DIFFS = [("angel", 450, 340, 0), ("roses", 750, 444, 0), ("urn", 300, 432, 0), ("bench", 610, 420, 0), ("lantern", 620, 300, 0),
               ("crow", 206, 104, 0), ("ivy", 860, 160, 0)]


# =================================================================== Level 1626 alchemist's cellar
WIN26 = (130, 60, 230, 150)


def flask(g, x, base, r, liquid, neck=24, seed=0):
    g.fill(Union([Circ(x, base - r, r), Box(x - r * 0.28, base - r * 2 - neck, x + r * 0.28, base - r * 1.6)]), (200, 220, 230), alpha=0.35)
    g.fill(Inter(Circ(x, base - r, r - 1.5), Box(x - r, base - r * 0.9, x + r, base)), liquid)
    g.glow(x, base - r * 0.6, r * 2.2, liquid, 0.25)
    g.add(Seg(x - r * 0.5, base - r * 1.5, x - r * 0.2, base - r * 1.75, 1.6), (255, 255, 255), 0.5)


def l1626_scene(g, d):
    g.fill(Box(-2, -2, W + 2, H + 2), ashlar((52, 48, 50), 28, 14, 2601))
    g.fill(Box(-2, -2, W + 2, H + 2), (0, 0, 0), alpha=lambda X, Y: 0.3 + 0.3 * smooth(0, 600, Y))
    for r0, r1, cy in ((300, 330, 330), (380, 420, 380)):
        band = stone_band(450, cy, r0, r1, cy)
        g.fill(band, ashlar((80, 74, 70), 18, 26, 2602))
        g.mul(Moved(band, 0, 8), 0.4, feather=8)
    # barred window high left with moonlight
    x0, y0, x1, y1 = WIN26
    win = arch(x0, x1, y0 + 30, y1, pointed=False)
    g.fill(win, vgrad([(y0, (110, 126, 176)), (y1, (150, 160, 200))]))
    g.fill(Inter(Union([Box(x, y0, x + 4, y1) for x in (156, 178, 200)] + [Box(x0, 104, x1, 108)]), win), (26, 24, 28))
    # floor
    g.fill(Box(-2, 470, W + 2, H + 2), persp_floor((450, 250), 470, (64, 60, 62), tile=44, seed=2603))
    light_pool(g, [(200, 470), (290, 470), (520, 600), (330, 600)], k=0.25)
    # workbench with glassware
    g.fill(Box(330, 380, 760, 404, 2), tex(light_x((110, 80, 54), 330, 760, 1.2, 0.8), 0.2, 2, 8))
    for lx in (350, 730):
        g.fill(Box(lx, 404, lx + 18, 560), tex(light_x((90, 64, 44), lx, lx + 18, 1.2, 0.6), 0.2, 1, 8))
    flask(g, 400, 380, 22, (90, 220, 130) if "flask" not in d else (230, 90, 200), seed=2604)
    flask(g, 470, 380, 14, (240, 180, 70), neck=30)
    g.fill(Union([Seg(470, 320, 560, 300, 2), Seg(560, 300, 600, 340, 2)]), (200, 220, 230), alpha=0.5)
    flask(g, 610, 380, 18, (120, 160, 240))
    # balance scale
    if "scale" not in d:
        g.fill(Union([Box(686, 320, 690, 380), Box(668, 376, 708, 380), Seg(660, 322, 716, 322, 2)]), (190, 160, 80))
        for sx in (662, 714):
            g.fill(Seg(sx, 322, sx, 340, 0.8), (190, 160, 80))
            g.fill(Inter(Ell(sx, 340, 12, 6), Box(sx - 12, 340, sx + 12, 348)), (190, 160, 80))
    # shelf with jars and books (right wall)
    g.fill(Box(620, 200, 880, 210), (80, 58, 40))
    for i, x in enumerate(range(636, 870, 34)):
        c = [(150, 60, 50), (60, 120, 90), (200, 170, 80), (90, 80, 150), (150, 60, 50), (60, 120, 90), (200, 170, 80)][i]
        if "jar" in d and i == 3:
            c = (230, 230, 220)
        g.fill(Box(x - 12, 160, x + 12, 200, 4), (210, 220, 230), alpha=0.35)
        g.fill(Box(x - 10, 172, x + 10, 198, 3), c)
        g.fill(Box(x - 13, 154, x + 13, 162, 2), (110, 80, 50))
    # hanging herbs
    for i, x in enumerate((300, 340, 380)):
        if "herbs" in d and i == 1:
            continue
        g.fill(Seg(x, 120, x, 150, 1), (120, 100, 70))
        g.fill(Rough(Ell(x, 170, 10, 22), 3, 4, 2605 + i), tex((70, 100, 50), 0.3, 2, 4))
    # cauldron with a green glow, candles, a cat
    g.glow(180, 480, 140, (100, 230, 120), 0.3)
    g.fill(Union([Ell(180, 520, 80, 56), Box(108, 468, 252, 482)]), sphere_paint(160, 500, 80, (40, 40, 46), ry=56, amb=0.35, spec=0.4))
    g.fill(Ell(180, 474, 70, 12), (110, 230, 130))
    for x in (380, 520):
        candle(g, x, 404 - 24, 20, w=7)
    if "cat" not in d:
        cx_, cy_ = 820, 560
        g.fill(Union([Ell(cx_, cy_ - 20, 30, 22), Circ(cx_ - 30, cy_ - 42, 14), Poly([(cx_ - 40, cy_ - 52), (cx_ - 38, cy_ - 68), (cx_ - 30, cy_ - 54)]),
                      Poly([(cx_ - 26, cy_ - 54), (cx_ - 20, cy_ - 68), (cx_ - 18, cy_ - 50)]), Seg(cx_ + 26, cy_ - 14, cx_ + 50, cy_ - 50, 4)]), (20, 18, 22))
        for ex in (-36, -26):
            g.fill(Ell(cx_ + ex, cy_ - 44, 2.6, 2), (220, 220, 80))
    cobweb(g, 0, 0, 70, (1, 1))


L1626_RAYS = [dict(lx=-400, ly=-600, col=(176, 190, 236), k=2.0, region=arch(WIN26[0], WIN26[2], WIN26[1] + 30, WIN26[3], pointed=False),
                   threshold=70, soft=60, density=0.92, decay=0.97, samples=70, receive=Box(-20, 120, W + 20, H + 20))]
L1626_ELEMENTS = [
    E("bubbles", el(lambda g, m: [g.fill(Circ(160 + k * 22, 466 - k * 8, 5 - k), (160, 250, 170), alpha=0.8) for k in range(3)]), daynight="untinted",
      anim=dict(driftVelocity=(0, 50), driftLength=50, driftFade=True)),
    flame_el("c1", 380, 356, 0.9, 0.1), flame_el("c2", 520, 356, 0.9, 0.5),
    motes_el("dust", [(240, 300), (300, 380), (270, 440)], vx=3, vy=-4, length=24),
]
L1626_DIFFS = [("flask", 400, 352, 0), ("scale", 688, 340, 0), ("jar", 738, 186, 0), ("herbs", 340, 160, 0), ("cat", 806, 530, 0)]


# =================================================================== Level 1627 portrait gallery
def portrait(g, x0, y0, x1, y1, bg, figure_col, seed, frame=(170, 130, 60)):
    g.mul(Box(x0 + 6, y0 + 8, x1 + 10, y1 + 12), 0.5, feather=6)
    g.fill(Box(x0 - 10, y0 - 10, x1 + 10, y1 + 10, 2), tex(sphere_paint((x0 + x1) / 2 - 20, y0, (x1 - x0), frame, ry=(y1 - y0), amb=0.4, spec=0.6), 0.15, 2, 2))
    g.fill(Box(x0, y0, x1, y1), tex(vgrad([(y0, bg), (y1, mixc(bg, (0, 0, 0), 0.5))]), 0.1, 6, 6, 3, seed))
    cx = (x0 + x1) / 2
    g.fill(Union([Ell(cx, y0 + (y1 - y0) * 0.38, (x1 - x0) * 0.17, (y1 - y0) * 0.16), Poly([(x0 + 8, y1), (cx - (x1 - x0) * 0.25, y0 + (y1 - y0) * 0.58),
                                                                                            (cx + (x1 - x0) * 0.25, y0 + (y1 - y0) * 0.58), (x1 - 8, y1)])]), figure_col)
    g.fill(Ell(cx, y0 + (y1 - y0) * 0.4, (x1 - x0) * 0.12, (y1 - y0) * 0.12), (200, 170, 150))


def l1627_scene(g, d):
    # right wall (portraits) in perspective-ish frontal view, floor, left window wall cut at the edge
    g.fill(Box(-2, -2, W + 2, 440), tex(vgrad([(0, (60, 30, 36)), (440, (40, 20, 26))]), 0.12, 20, 30, 3, 2701))
    g.fill(Box(-2, -2, W + 2, 440), (0, 0, 0), alpha=lambda X, Y: 0.15 * (np.abs(np.sin(X * 0.08)) > 0.85))
    g.fill(Box(-2, 360, W + 2, 440), planks("v", (70, 46, 34), seed=2702, width=30))
    g.fill(Box(-2, 352, W + 2, 362), (110, 80, 50))
    portrait(g, 70, 100, 190, 260, (60, 70, 90), (40, 30, 40) if "portrait" not in d else (120, 30, 40), 2703)
    portrait(g, 300, 80, 460, 280, (90, 70, 50), (30, 40, 70), 2704)
    portrait(g, 580, 110, 690, 250, (70, 90, 70), (70, 30, 30), 2705)
    portrait(g, 780, 90, 890, 270, (80, 60, 80), (40, 40, 50), 2706, frame=(170, 130, 60) if "frame" not in d else (120, 120, 130))
    floor_planks(g, 440, col=(80, 56, 40), seed=2707)
    g.fill(Box(-2, 470, W + 2, 540), tex((110, 24, 34), 0.15, 4, 4, 3, 2708))
    g.fill(Box(-2, 474, W + 2, 478), (200, 160, 70))
    g.fill(Box(-2, 532, W + 2, 536), (200, 160, 70))
    # moonlight stripes from the windows behind the camera
    for x in (100, 400, 700):
        light_pool(g, [(x, 440), (x + 90, 440), (x + 200, 600), (x + 60, 600)], k=0.18)
        light_pool(g, [(x + 40, 60), (x + 110, 60), (x + 130, 400), (x + 60, 400)], k=0.07)
    # armour stand and bust
    from souls_kit import knight
    knight(g, 520, 470, 200, steel=(110, 112, 120), cloth=(70, 30, 40), face=-1, sword="down", helm="great",
           plume=(180, 30, 40) if "plume" not in d else None, rim_dx=2, rim_k=0.4)
    g.fill(Box(220, 360, 270, 460), tex(light_x((140, 136, 130), 220, 270, 1.2, 0.7), 0.2, 3, 3))
    g.fill(Box(214, 354, 276, 362), (150, 146, 140))
    if "bust" not in d:
        g.fill(Union([Ell(245, 320, 16, 20), Poly([(220, 354), (230, 336), (260, 336), (270, 354)])]), sphere_paint(240, 314, 22, (200, 196, 190), ry=26, amb=0.4, spec=0.2))
    # candelabra on a side table
    g.fill(Box(720, 400, 820, 410, 2), (90, 60, 40))
    g.fill(Box(764, 410, 776, 470), (80, 56, 38))
    g.fill(Union([Seg(770, 400, 770, 360, 2), Seg(746, 372, 794, 372, 1.6)]), (190, 160, 80))
    for dx, key in ((-24, None), (0, None), (24, "candle")):
        candle(g, 770 + dx, 372 if dx else 362, 18, w=6, lit=not (key and key in d))
        if key and key not in d:
            flame(g, 770 + dx, 354, 0.9)
    if "vase" not in d:
        g.fill(Union([Ell(110, 420, 22, 28), Box(100, 384, 120, 394)]), sphere_paint(104, 412, 22, (60, 80, 140), ry=28, amb=0.4, spec=0.5))


L1627_ELEMENTS = [
    flame_el("c1", 746, 354, 0.9, 0.2), flame_el("c2", 770, 344, 0.9, 0.5),
    motes_el("dust", [(180, 300), (480, 260), (760, 200), (300, 380)], vx=2, vy=-3, length=22),
    beam_el("b1", 140, 60, 260, 600, 60, 140, k=0.07), beam_el("b2", 440, 60, 560, 600, 60, 140, k=0.07, phase=0.5),
]
L1627_DIFFS = [("portrait", 130, 200, 0), ("frame", 835, 180, 0), ("plume", 470, 196, 0), ("bust", 245, 330, 0), ("candle", 794, 350, 0),
               ("vase", 110, 410, 0)]


# =================================================================== Level 1628 abandoned ballroom
WINS28 = [(120, 60, 220, 340), (400, 40, 500, 330), (680, 60, 780, 340)]


def l1628_scene(g, d):
    g.fill(Box(-2, -2, W + 2, 420), tex(vgrad([(0, (70, 66, 80)), (420, (50, 46, 58))]), 0.12, 30, 30, 3, 2801))
    for x in range(40, 900, 140):
        g.fill(Box(x - 14, -2, x + 14, 420), cyl_paint(x, 14, (120, 114, 126), amb=0.35, spec=0.2))
    for (x0, y0, x1, y1) in WINS28:
        sh = arch(x0, x1, y0 + 50, y1)
        g.fill(sh, vgrad([(y0, (90, 110, 170)), (y1, (140, 150, 200))]))
        g.fill(Inter(Union([Box((x0 + x1) / 2 - 2, y0, (x0 + x1) / 2 + 2, y1), Box(x0, 200, x1, 204)]), sh), (40, 36, 44))
        g.fill(Diff(arch(x0 - 8, x1 + 8, y0 + 50, y1 + 6), sh), (130, 124, 136))
    moon(g, 470, 110, 16, k=0.25, seed=2802)
    # curtains with tie-backs
    for x0, x1 in ((90, 120), (220, 250), (650, 680), (780, 810)):
        g.fill(Poly([(x0, 40), (x1, 40), (x1 - 4, 340), (x0 + 4, 340)]), tex(light_x((120, 30, 40), x0, x1, 1.2, 0.6), 0.2, 2, 8))
    g.fill(Ell(812, 240, 10, 5), (200, 160, 70) if "tie" not in d else (60, 110, 190))
    # floor (parquet)
    g.fill(Box(-2, 420, W + 2, H + 2), persp_floor((450, 200), 420, (110, 80, 56), tile=50, seed=2803))
    for (x0, y0, x1, y1) in WINS28:
        light_pool(g, [(x0, 420), (x1, 420), (x1 + 40, 600), (x0 + 30, 600)], k=0.2)
    # fallen chandelier in the middle of the floor
    if "chandelier" not in d:
        g.fill(Ell(450, 520, 120, 22) - Ell(450, 516, 100, 14), sphere_paint(430, 512, 120, (190, 160, 80), ry=22, amb=0.4, spec=0.7))
        for k in range(9):
            x = 350 + k * 25
            g.fill(Poly([(x - 4, 510), (x, 528), (x + 4, 510)]), (220, 230, 240))
    g.fill(Seg(450, -2, 450, 120, 1.4), (60, 56, 50))
    # grand piano (left) with a candle
    g.mul(Ell(190, 560, 150, 14), 0.5, feather=8)
    g.fill(Poly([(60, 480), (300, 480), (320, 440), (200, 420), (80, 430)]), sphere_paint(150, 440, 150, (24, 22, 26), ry=40, amb=0.3, spec=0.7))
    g.fill(Box(60, 480, 300, 500), (20, 18, 22))
    for x in (80, 280):
        g.fill(Box(x - 5, 500, x + 5, 560), (24, 22, 26))
    if "lid" not in d:
        g.fill(Poly([(90, 430), (210, 420), (300, 330), (180, 360)]), sphere_paint(200, 380, 100, (26, 24, 30), ry=50, amb=0.3, spec=0.6))
    for k in range(16):
        g.fill(Box(70 + k * 9, 476, 77 + k * 9, 484), (240, 236, 226))
    candle(g, 250, 438, 22, w=7)
    # dust-sheeted chairs and a mirror (right)
    for x, key in ((640, None), (760, "sheet")):
        c = (220, 220, 214) if not (key and key in d) else (180, 150, 120)
        g.fill(Rough(Union([Box(x - 40, 430, x + 40, 540, 14), Ell(x, 430, 40, 30)]), 3, 8, 2804 + x), light_x(c, x - 40, x + 40, 1.1, 0.7))
    g.fill(Box(840, 120, 900, 320, 4), tex(sphere_paint(860, 140, 80, (190, 160, 80), ry=120, amb=0.4, spec=0.6), 0.1, 2, 2))
    g.fill(Box(848, 130, 900, 310), vgrad([(130, (120, 130, 160)), (310, (60, 64, 80))]))
    if "crack" not in d:
        g.fill(Union([Seg(860, 150, 880, 200, 1), Seg(880, 200, 870, 250, 1), Seg(880, 200, 896, 220, 1)]), (230, 236, 250))
    if "vase" not in d:
        g.fill(Union([Ell(560, 400, 18, 24), Box(552, 370, 568, 378)]), sphere_paint(554, 392, 18, (200, 200, 210), ry=24, amb=0.4, spec=0.5))
        for k, (fx, fy) in enumerate(((548, 362), (560, 354), (572, 362))):
            g.fill(Seg(560, 372, fx, fy, 1), (60, 70, 50))
            g.fill(Circ(fx, fy, 5), (110, 40, 50))


L1628_RAYS = [dict(lx=470, ly=-500, col=(176, 190, 236), k=1.0, region=Union([arch(w[0], w[2], w[1] + 50, w[3]) for w in WINS28]), threshold=120,
                   soft=60, density=0.92, decay=0.97, samples=70, receive=Box(-20, 120, W + 20, H + 20))]
L1628_ELEMENTS = [flame_el("pc", 250, 414, 1.0, 0.1), motes_el("dust", [(180, 300), (450, 260), (720, 300), (450, 380)], vx=2, vy=-3, length=24),
                  bat_el("bat", 600, 140, s=8, speed=-20, phase=0.4)]
L1628_DIFFS = [("tie", 812, 240, 0), ("chandelier", 450, 516, 0), ("lid", 200, 380, 0), ("sheet", 760, 480, 0), ("crack", 878, 200, 0),
               ("vase", 560, 380, 0)]


# =================================================================== Level 1629 cliff monastery
M29 = (680, 120, 46)


def l1629_upper(g, d):
    mx, my, mr = M29
    sky(g, [(0, (6, 10, 26)), (200, (26, 36, 66)), (330, (56, 66, 96))])
    stars(g, 80, 260, seed=2901)
    moon(g, mx, my, mr, k=0.9, seed=2902)
    cloud_layer(g, 160, 230, (120, 130, 170), (40, 46, 70), cover=0.3, sx=200, sy=10, seed=2903, alpha=0.5)


def l1629_scene(g, d):
    l1629_upper(g, set())
    g.snapshot("r")
    l1629_upper(g, d)
    water(g, 330, 600, (40, 50, 80), (14, 18, 30), seed=2904)
    g.reflect(330, 330, 600, ripple=4, k=0.55, src="r", tint=(20, 30, 60), tint_k=0.3, streak=0.4)
    g.add(Poly([(650, 330), (710, 330), (760, 600), (600, 600)]), (200, 210, 240), 0.18, feather=20)
    if "boat" not in d:
        g.fill(Poly([(560, 420), (620, 420), (610, 432), (570, 432)]), (20, 18, 24))
        g.fill(Seg(590, 420, 590, 390, 1.2), (20, 18, 24))
        g.fill(Poly([(591, 392), (612, 418), (591, 418)]), (60, 60, 80))
    # the cliff (left) with the monastery
    cliff = Poly([(-20, 610), (-20, 230), (60, 220), (180, 240), (330, 260), (380, 330), (420, 450), (470, 610)])
    from real_kit import rock_face
    g.fill(cliff, rock_face((70, 66, 74), seed=2905))
    g.fill(cliff, (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.35 * smooth(200, 450, X))
    col = (100, 98, 108)
    chap = Union([Box(60, 140, 260, 240), Poly([(52, 142), (160, 80), (268, 142)])])
    wall(g, chap, col, 2906, 60, 260, light=1)
    tower = Box(260, 60, 320, 260)
    wall(g, tower, col, 2907, 260, 320, light=1)
    spire(g, 290, 62, 60, 90, col, seed=2908, light=1, crockets=False)
    g.fill(arch(276, 304, 90, 130), (14, 14, 20))
    if "bell" not in d:
        g.fill(Union([Poly([(280, 126), (282, 104), (290, 98), (298, 104), (300, 126)]), Ell(290, 127, 12, 3)]), sphere_paint(286, 108, 14, (180, 140, 70), ry=18, amb=0.4, spec=0.7))
    for x, lit in ((90, True), (150, "window" not in d), (210, True)):
        lancet(g, x, x + 22, 180, 226, lit=WARM if lit else None)
    # lantern path down the cliff and a monk
    for i, (x, y) in enumerate(((330, 300), (370, 380), (400, 460))):
        if "lamp" in d and i == 1:
            continue
        g.fill(Seg(x, y, x, y - 40, 2), IRON)
        g.glow(x, y - 44, 40, FIRE, 0.4)
        g.fill(Box(x - 6, y - 52, x + 6, y - 38, 2), (255, 200, 120))
    from real_kit import figure
    figure(g, 220, 270, 50, (60, 50, 60), skin=(200, 170, 150), hair=(60, 50, 60), face_right=True, hat=None)
    g.fog(330, 380, (80, 90, 120), 0.4, 0.0)


L1629_RAYS = [dict(lx=M29[0], ly=M29[1], col=(170, 186, 232), k=1.4, region=Box(-2, -2, W + 2, 330), threshold=90,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=lambda X, Y: moon_receive(*M29, floor=0.3)(X, Y) * smooth(360, 220, Y))]
L1629_ELEMENTS = [glint_el("sea", [(660, 400), (700, 460), (640, 520), (720, 560)], col=(220, 230, 255), r=5, speed=0.6),
                  bat_el("b1", 500, 80, s=9, speed=-22, phase=0.3), mist_el("mist", 450, 360, 450, 14, (110, 120, 150), alpha=0.4, length=80, seed=29)]
L1629_DIFFS = [("boat", 590, 412, 0), ("bell", 290, 112, 0), ("window", 161, 204, 0), ("lamp", 370, 352, 0)]


# =================================================================== Level 1630 foggy Victorian station
def l1630_scene(g, d):
    sky(g, [(0, (14, 18, 34)), (300, (40, 46, 70))])
    moon(g, 640, 110, 30, k=0.7, seed=3001)
    # iron-and-glass roof: arched trusses
    for x0 in (-100, 300, 700):
        g.fill(Diff(Inter(Ell(x0 + 200, 330, 230, 300), Box(x0 - 40, 20, x0 + 440, 330)), Inter(Ell(x0 + 200, 330, 222, 292), Box(x0 - 40, 20, x0 + 440, 330))), (40, 40, 48))
        for a in np.linspace(math.pi, math.tau, 10):
            g.fill(Seg(x0 + 200, 330, x0 + 200 + math.cos(a) * 226, 330 + math.sin(a) * 296, 1.2), (40, 40, 48))
    g.fill(Box(-2, 320, W + 2, 340), light_y((80, 76, 84), 320, 340, 1.2, 0.7))
    for x in range(40, 900, 160):
        g.fill(Box(x - 8, 330, x + 8, 520), cyl_paint(x, 8, (70, 70, 80), amb=0.35, spec=0.4))
    # hanging clock
    g.fill(Seg(360, 330, 360, 352, 2), IRON)
    g.fill(Circ(360, 380, 28), (30, 30, 36))
    g.fill(Circ(360, 380, 24), (240, 236, 220))
    mh = -math.pi / 2 + (0.3 if "clock" not in d else 2.6)
    g.fill(Union([Seg(360, 380, 360 + math.cos(mh) * 20, 380 + math.sin(mh) * 20, 2), Seg(360, 380, 372, 386, 2.6)]), (20, 20, 24))
    # platform
    g.fill(Box(-2, 520, W + 2, H + 2), grain_tex(vgrad([(520, (110, 108, 112)), (600, (70, 68, 72))]), 0.12, 3001))
    g.fill(Box(-2, 516, W + 2, 524), (220, 200, 90))
    # steam locomotive (right) with a lamp
    loco = Union([Box(520, 400, 900, 500, 8), Box(520, 340, 620, 500, 4)])
    g.fill(loco, tex(light_y((30, 34, 40), 340, 500, 1.3, 0.6), 0.1, 6, 3))
    g.fill(Box(530, 352, 610, 390), (255, 200, 120) if "cab" not in d else (40, 44, 54))
    g.fill(Box(780, 360, 820, 400, 3), (36, 36, 42))
    for x in (600, 690, 780, 870):
        g.fill(Circ(x, 500, 30), (26, 26, 30))
        g.fill(Circ(x, 500, 22) - Circ(x, 500, 18), (150, 40, 40))
    g.fill(Box(520, 470, 900, 476), (150, 40, 40))
    if "lamp" not in d:
        g.glow(890, 440, 60, (255, 230, 160), 0.5)
        g.fill(Circ(890, 440, 10), (255, 240, 200))
    # gas lamps, bench, luggage cart, porter
    gas_lamp(g, 120, 520, 170, lit=True)
    gas_lamp(g, 440, 520, 170, lit="gas" not in d)
    g.fill(Union([Box(170, 474, 290, 482, 2), Box(170, 454, 290, 460, 2), Box(178, 482, 184, 512), Box(276, 482, 282, 512)]), (90, 60, 40))
    for i, (x, w, c) in enumerate(((330, 50, (120, 60, 40)), (338, 36, (60, 80, 110)))):
        if "case" in d and i == 1:
            c = (150, 40, 40)
        g.fill(Box(x, 500 - i * 22 - 22, x + w, 500 - i * 22, 3), light_y(c, 478 - i * 22, 500 - i * 22, 1.2, 0.7))
    g.fill(Union([Box(320, 500, 400, 506), Circ(330, 510, 6), Circ(392, 510, 6)]), (40, 40, 44))
    from real_kit import figure
    figure(g, 480, 520, 100, (40, 40, 70), skin=(200, 170, 150), hair=(40, 30, 30), face_right=False, hat=(30, 30, 40))
    g.fog(380, 560, (110, 116, 140), 0.0, 0.35, noise=0.5, seed=3002)


L1630_RAYS = [dict(lx=640, ly=110, col=(176, 190, 236), k=1.2, region=Box(-2, -2, W + 2, 320), threshold=40,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=lambda X, Y: moon_receive(640, 110, 30, floor=0.3)(X, Y) * smooth(560, 320, Y))]
L1630_ELEMENTS = [E("steam%d" % i, el(lambda g, m, i=i: g.glow(560, 320, 30, (220, 224, 236), 0.4)), anim=dict(driftVelocity=(-20, 60), driftLength=160, driftFade=True,
                                                                                                       driftGrow=2.0, phase=i / 3)) for i in range(3)] + \
                 [mist_el("fog", 450, 480, 420, 20, (130, 136, 160), alpha=0.35, length=90, seed=30)]
L1630_DIFFS = [("clock", 362, 378, 0), ("cab", 570, 370, 0), ("lamp", 890, 440, 0), ("gas", 440, 360, 0), ("case", 356, 466, 0)]


LEVELS = [
    ("Level1624", "钟楼机芯", make_bg(l1624_scene, L1624_RAYS, bloom=(200, 14, 0.35)), L1624_ELEMENTS, L1624_DIFFS, 60, OPTS),
    ("Level1625", "月下回廊", make_bg(l1625_scene, L1625_RAYS), L1625_ELEMENTS, L1625_DIFFS, 60, OPTS),
    ("Level1626", "炼金地窖", make_bg(l1626_scene, L1626_RAYS, bloom=(200, 14, 0.35)), L1626_ELEMENTS, L1626_DIFFS, 60, OPTS),
    ("Level1627", "肖像长廊", make_bg(l1627_scene, [], bloom=(200, 14, 0.35)), L1627_ELEMENTS, L1627_DIFFS, 60, OPTS),
    ("Level1628", "废弃舞厅", make_bg(l1628_scene, L1628_RAYS, bloom=(200, 14, 0.35)), L1628_ELEMENTS, L1628_DIFFS, 60, OPTS),
    ("Level1629", "断崖修道院", make_bg(l1629_scene, L1629_RAYS), L1629_ELEMENTS, L1629_DIFFS, 60, OPTS),
    ("Level1630", "雾夜车站", make_bg(l1630_scene, L1630_RAYS), L1630_ELEMENTS, L1630_DIFFS, 60, OPTS),
]
