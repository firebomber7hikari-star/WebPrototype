# -*- coding: utf-8 -*-
"""Realistic dark-fantasy levels, part 1: a gothic Victorian hunters' city by night (inspired by the mood of
gothic action-RPGs; every building, character and creature is an original design; no gore).
  Level1565 雾夜长街   - a foggy gothic street receding to a cathedral, gas lamps, chained coffins, a hunter
  Level1566 大教堂石阶 - a great cathedral facade above a long flight of steps, statues, moon behind the tower
  Level1567 猎人工坊   - a hunter's workshop: workbench, weapons on the wall, vials, candles, moonlit window
  Level1568 血月屋顶   - rooftops under a huge red moon: clock tower, chimneys, gargoyle, crows, a hunter
  Level1569 禁林提灯   - lantern-lit forbidden woods: hanging cages, a fenced path, a hut, eyes in the dark
  Level1570 雨中渔村   - a rotting fishing village in the rain: stilt huts, boats, nets, a distant lighthouse
  Level1571 禁书库     - a forbidden library: towering shelves, ladder, chandelier, reading desk, globe
  Level1572 地下水道   - a brick sewer tunnel: water channel, light shaft through a grate, lanterns, gates
  Level1573 桥上对峙   - a hunter facing a beast on a stone bridge under the full moon
  Level1574 月光礼拜堂 - a chapel interior: stained-glass moonbeams, pews, altar, candelabra
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (C, Box, Circ, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm, fbm1,
                  grain_tex, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint, tex, vgrad)
from real_kit import blades, cloud_layer, crown, glint_el, mist_el, planks, ridge, rock, sky, stars, treeline
from levels_real2 import (arch, ashlar, bat, bat_el, beam_el, candle, cobweb, dead_tree, flame, flame_el, fog_band,
                          make_bg, moon, moon_receive, motes_el, rim, stains, twigs)
from levels_real3 import flat_bg
from souls_kit import (FIRE, IRON, MOON, banner, barrel, beast, buttress, cage, chain, cobbles, coffin, crate, crow,
                       emblem_moon, ember_el, fire_el, gas_lamp, hunter, lancet, n1, railing, skyline, spire, statue,
                       stone, torch, wall)
from weather import rain_layer

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)
WARM = (255, 196, 120)


def quad(p0, p1, p2, p3):
    return Poly([p0, p1, p2, p3])


class Facade:
    """A street facade in one-point perspective: depth s (0 near .. 1 far), height v (0 base .. 1 top)."""

    def __init__(self, x_near, x_far, base_near, base_far, top_near, top_far):
        self.xn, self.xf, self.bn, self.bf, self.tn, self.tf = x_near, x_far, base_near, base_far, top_near, top_far

    def p(self, s, v):
        x = self.xn + (self.xf - self.xn) * s
        b = self.bn + (self.bf - self.bn) * s
        t = self.tn + (self.tf - self.tn) * s
        return (x, b + (t - b) * v)

    def rect(self, s0, s1, v0, v1):
        return quad(self.p(s0, v0), self.p(s1, v0), self.p(s1, v1), self.p(s0, v1))

    def shape(self):
        return self.rect(0, 1, 0, 1)


def persp_window(g, fa, s0, s1, v0, v1, lit=None, frame=(26, 24, 28)):
    outer = fa.rect(s0, s1, v0, v1)
    g.fill(fa.rect(s0 - 0.006, s1 + 0.006, v0 - 0.012, v1 + 0.02), frame)
    if lit is not None:
        x, y = fa.p((s0 + s1) / 2, (v0 + v1) / 2)
        g.glow(x, y, 40 * (1 - (s0 + s1) / 2 * 0.7), lit, 0.18)
        g.fill(outer, lit)
    else:
        g.fill(outer, (24, 28, 40))
        g.add(fa.rect(s0, s0 + (s1 - s0) * 0.3, v0, v1), MOON, 0.08)
    sm, vm = (s0 + s1) / 2, (v0 + v1) * 0.55
    g.fill(Union([quad(fa.p(sm - 0.003, v0), fa.p(sm + 0.003, v0), fa.p(sm + 0.003, v1), fa.p(sm - 0.003, v1)),
                  fa.rect(s0, s1, vm - 0.006, vm + 0.006)]), frame)


# =================================================================== Level 1565 foggy street
M65 = (470, 92, 30)
LF65 = Facade(-20, 330, 572, 352, -30, 196)
RF65 = Facade(920, 570, 572, 352, -30, 206)
S65 = (0.0, 0.2, 0.37, 0.5, 0.61, 0.7, 0.78, 0.85)


def l1565_scene(g, d):
    mx, my, mr = M65
    sky(g, [(0, (8, 12, 22)), (150, (24, 34, 52)), (300, (52, 62, 80)), (360, (70, 78, 92))])
    stars(g, 60, 220, seed=6501)
    moon(g, mx, my, mr, col=(232, 230, 214), k=0.8, seed=6502)
    cloud_layer(g, 60, 130, (120, 130, 160), (50, 56, 80), cover=0.3, sx=140, sy=10, seed=6503, alpha=0.55)
    # distant cathedral closing the street
    skyline(g, 356, 40, 110, (30, 36, 50), 6504, x0=300, x1=600, spires=0.6)
    g.fill(Box(380, 210, 520, 356), stone((44, 48, 62), 6505, 14, 8))
    spire(g, 450, 230, 46, 180, (50, 54, 70), seed=6506, crockets=True)
    for sx_ in (400, 500):
        spire(g, sx_, 250, 26, 110, (46, 50, 66), seed=6507 + sx_, crockets=False)
    if "turret" not in d:
        spire(g, 352, 330, 22, 100, (46, 50, 66), seed=6509, crockets=False)
    g.fill(Circ(450, 290, 20), (255, 200, 130))
    g.glow(450, 290, 40, (255, 170, 90), 0.3)
    g.fog(180, 360, (70, 80, 100), 0.0, 0.55, x0=300, x1=600)
    # street
    road = Poly([(-20, 610), (920, 610), (570, 352), (330, 352)])
    g.fill(road, cobbles((70, 70, 76), 6510, 16, 8))
    g.fill(road, (0, 0, 0), alpha=lambda X, Y: 0.3 + 0.4 * smooth(380, 352, Y))
    g.add(Poly([(380, 600), (520, 600), (470, 360), (430, 360)]), (150, 160, 190), 0.18, feather=30)
    for fa, side in ((LF65, -1), (RF65, 1)):
        walk = Poly([fa.p(0, 0), fa.p(1, 0), (fa.xf + side * -14, fa.bf + 2), (fa.xn - side * 160, fa.bn + 40)])
        g.fill(walk, cobbles((86, 84, 88), 6511, 10, 10))
    # facades
    for fa, base, seed, lsign in ((LF65, (66, 62, 64), 6512, 1), (RF65, (60, 58, 62), 6513, -1)):
        sh = fa.shape()
        g.fill(sh, stone(base, seed, 22, 11))
        g.fill(sh, (0, 0, 0), alpha=lambda X, Y, fa=fa: 0.25 + 0.5 * smooth(abs(fa.xn - 450), abs(fa.xf - 450), np.abs(X - 450)))
        stains(g, sh, 0.22, sx=30, sy=70, seed=seed + 1)
        for s0, s1 in zip(S65[:-1], S65[1:]):
            g.fill(fa.rect(s0, s0 + 0.012, 0, 1), (30, 28, 32), alpha=0.6)
        g.fill(fa.rect(0, 1, 0.9, 0.94), mixc(base, (0, 0, 0), 0.35))
        g.fill(fa.rect(0, 1, 0.35, 0.37), mixc(base, (0, 0, 0), 0.3))
    lit_l = {(1, 1), (3, 2), (5, 0)}
    lit_r = {(2, 1), (4, 2), (0, 2), (6, 1)}
    for fa, lits, key in ((LF65, lit_l, "L"), (RF65, lit_r, "R")):
        for i, (s0, s1) in enumerate(zip(S65[:-1], S65[1:])):
            w = (s1 - s0)
            for j, (v0, v1) in enumerate(((0.44, 0.62), (0.68, 0.84))):
                lit = WARM if (i, j + 1) in lits else None
                if key == "R" and (i, j) == (0, 1):
                    lit = None if "window" in d else WARM
                persp_window(g, fa, s0 + w * 0.25, s1 - w * 0.25, v0, v1, lit)
            # ground floor: doors / shopfronts
            persp_window(g, fa, s0 + w * 0.2, s1 - w * 0.2, 0.0, 0.26, WARM if (i, 0) in lits else (40, 34, 30))
    # hanging shop sign on the left facade
    bx, by = LF65.p(0.3, 0.6)
    g.fill(Seg(bx, by, bx + 70, by - 4, 2.4), IRON)
    g.fill(Seg(bx + 10, by + 6, bx + 40, by - 2, 1.4), IRON)
    for hx in (bx + 30, bx + 62):
        g.fill(Seg(hx, by - 3, hx, by + 10, 1.0), IRON)
    if "sign" not in d:
        sign = Box(bx + 22, by + 10, bx + 72, by + 46, 4)
        g.fill(sign, tex(light_x((80, 56, 40), bx + 22, bx + 72, 1.3, 0.7), 0.2, 1.5, 6))
        emblem_moon(g, bx + 47, by + 28, 14, col=(200, 170, 100))
    # gas lamps along the kerbs
    for s, side in ((0.12, -1), (0.45, -1), (0.72, -1), (0.3, 1), (0.62, 1)):
        fa = LF65 if side < 0 else RF65
        x, y = fa.p(s, 0)
        x += -side * (60 - 50 * s)
        y += 26 * (1 - s)
        gas_lamp(g, x, y, 200 * (1 - s * 0.78), lit=True)
    # chained coffins by the near left door
    if "coffin" not in d:
        coffin(g, 116, 566, 54, 128, seed=6520, lean=0.06)
    coffin(g, 60, 572, 50, 120, seed=6521, lean=-0.04, chain=True)
    # crates and a ground lantern
    crate(g, 300, 520, 44, 40, seed=6522)
    lx, ly = 344, 512
    g.fill(Box(lx - 9, ly - 22, lx + 9, ly, 2), (255, 200, 120) if "lantern" not in d else (40, 44, 54))
    if "lantern" not in d:
        g.glow(lx, ly - 10, 50, FIRE, 0.4)
    g.fill(Union([Box(lx - 10, ly - 22, lx - 8, ly), Box(lx + 8, ly - 22, lx + 10, ly), Poly([(lx - 12, ly - 22), (lx, ly - 32), (lx + 12, ly - 22)])]), IRON)
    fog_band(g, 330, 400, 470, (90, 100, 124), 0.5, seed=6523)
    # the hunter in the foreground, lit from the moon on the left
    hunter(g, 742, 590, 300, face=-1, weapon="cane", rim_dx=2.2, scarf=(120, 30, 34) if "scarf" in d else (70, 64, 58),
           coat=(40, 36, 36), trim=(64, 56, 50))
    g.fog(470, 610, (60, 66, 84), 0.0, 0.3, noise=0.5, sx=160, sy=14, seed=6524)


L1565_RAYS = [dict(lx=M65[0], ly=M65[1], col=(170, 186, 232), k=1.4, region=Box(260, -2, 640, 230), threshold=90,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=moon_receive(*M65, floor=0.3))]
L1565_ELEMENTS = [
    mist_el("mist1", 450, 380, 260, 16, (110, 120, 150), alpha=0.5, length=80, seed=31),
    mist_el("mist2", 300, 520, 300, 14, (90, 100, 126), alpha=0.35, length=90, seed=32),
    bat_el("bat1", 560, 60, s=9, speed=-28, phase=0.3),
    bat_el("bat2", 590, 76, s=6, speed=-28, phase=0.35),
    beam_el("beam", 470, 100, 450, 420, 40, 160, k=0.07),
    glint_el("lamps", [(LF65.p(0.12, 0)[0] + 54, 400), (452, 290)], col=(255, 220, 160), r=6, speed=0.5),
]
L1565_DIFFS = [("turret", 352, 280, 0), ("window", 840, 180, 0), ("sign", 160, 250, 0), ("coffin", 120, 510, 0),
               ("lantern", 344, 500, 0), ("scarf", 746, 300, 0)]


# =================================================================== Level 1566 cathedral steps
M66 = (700, 120, 46)


def l1566_scene(g, d):
    mx, my, mr = M66
    sky(g, [(0, (6, 10, 22)), (200, (30, 38, 62)), (360, (64, 70, 96))])
    stars(g, 90, 260, seed=6601)
    moon(g, mx, my, mr, col=(236, 232, 214), k=0.9, seed=6602)
    cloud_layer(g, 160, 230, (130, 140, 170), (50, 56, 84), cover=0.35, sx=180, sy=12, seed=6603, alpha=0.5)
    skyline(g, 330, 30, 80, (26, 30, 44), 6604, spires=0.4)
    # cathedral: nave front, rose window, twin towers (right tower in front of the moon)
    col = (78, 78, 88)
    front = Union([Box(300, 150, 600, 360), Poly([(300, 152), (450, 40), (600, 152)])])
    wall(g, front, col, 6605, 300, 600, light=1)
    g.fill(Poly([(318, 152), (450, 58), (582, 152), (568, 152), (450, 70), (332, 152)]), (40, 40, 48))
    rw = Circ(450, 160, 44)
    g.fill(Circ(450, 160, 50), (40, 40, 48))
    glass = (60, 120, 200) if "rose" in d else (200, 60, 70)
    for i in range(12):
        a0 = i * math.tau / 12
        seg_col = glass if i % 2 else (230, 180, 80)
        g.fill(Poly([(450, 160), (450 + 44 * math.cos(a0), 160 + 44 * math.sin(a0)), (450 + 44 * math.cos(a0 + math.tau / 12), 160 + 44 * math.sin(a0 + math.tau / 12))]),
               mixc(seg_col, (0, 0, 0), 0.25))
    g.glow(450, 160, 60, (255, 150, 90), 0.25)
    g.fill(Union([Circ(450, 160, 44) - Circ(450, 160, 41)] + [Seg(450, 160, 450 + 44 * math.cos(i * math.tau / 12), 160 + 44 * math.sin(i * math.tau / 12), 1.4) for i in range(12)] + [Circ(450, 160, 9)]), (30, 28, 32))
    g.fill(arch(400, 500, 280, 360), (20, 16, 18))
    g.fill(arch(408, 492, 284, 360), lgrad(0, 220, 0, 360, [(0, (110, 70, 40)), (1, (60, 40, 26))]))
    g.fill(Union([Box(449, 236, 451, 360)] + [Box(410, y, 490, y + 2) for y in (300, 324, 348)]), (40, 30, 24))
    for x0 in (330, 530):
        lancet(g, x0, x0 + 40, 230, 320)
    for tx, w in ((220, 120), (680, 120)):
        tower = Box(tx - w / 2, 90, tx + w / 2, 360)
        wall(g, tower, col, 6606 + tx, tx - w / 2, tx + w / 2, light=1)
        for yy in (130, 220):
            lancet(g, tx - 16, tx + 16, yy, yy + 60, lit=WARM if (tx == 220 and yy == 220 and "window" not in d) else None)
        spire(g, tx, 92, w * 0.9, 150, col, seed=6607 + tx, light=1)
        buttress(g, tx - w / 2 - 8, 360, 22, 230, col, seed=tx, light=1)
        buttress(g, tx + w / 2 + 8, 360, 22, 230, col, seed=tx + 1, light=1)
    # gargoyle on the right tower corner
    gx, gy = 742, 98
    if "gargoyle" not in d:
        g.fill(Union([Ell(gx + 12, gy - 6, 14, 9), Circ(gx + 26, gy - 14, 7), Poly([(gx + 2, gy - 10), (gx - 14, gy - 34), (gx + 10, gy - 16)]),
                      Seg(gx + 18, gy, gx + 22, gy + 6, 3)]), tex(light_x((70, 70, 80), gx - 14, gx + 34, 0.6, 1.3), 0.2, 2, 2))
    # long flight of steps widening to the foreground
    for i in range(12):
        t = i / 11
        y0 = 360 + 240 * t ** 1.3
        y1 = 360 + 240 * ((i + 1) / 11) ** 1.3 if i < 11 else 610
        hw = 120 + 380 * t
        g.fill(Box(450 - hw, y0, 450 + hw, y1 + 1), light_y((96, 94, 100), y0, y1, 1.25, 0.55))
        g.fill(Box(450 - hw, y0, 450 + hw, y0 + 2), (130, 128, 136))
    g.fill(Poly([(330, 360), (-20, 610), (-20, 360)]), (40, 42, 52))
    g.fill(Poly([(570, 360), (920, 610), (920, 360)]), (40, 42, 52))
    # statues flanking the stairs
    statue(g, 150, 470, 230, col=(112, 112, 116), seed=6610, light=1, arms="pray")
    statue(g, 750, 470, 230, col=(112, 112, 116), seed=6611, light=1, arms="pray", hood="statue" not in d)
    # lamps on the stair landings
    gas_lamp(g, 300, 430, 120, lit="lamp" not in d)
    gas_lamp(g, 600, 430, 120, lit=True)
    # a banner hanging over the door
    if "banner" not in d:
        banner(g, 450, 236, 40, 40, (120, 20, 30), emblem=None, seed=6612, pole=False)
    # crow on the stairs, hunter climbing
    if "crow" not in d:
        crow(g, 610, 540, 1.3, face=-1)
    if "lantern" not in d:
        lx, ly = 230, 566
        g.glow(lx, ly - 12, 60, FIRE, 0.35)
        g.fill(Box(lx - 10, ly - 26, lx + 10, ly, 2), (255, 200, 120))
        g.fill(Union([Box(lx - 11, ly - 26, lx - 9, ly), Box(lx + 9, ly - 26, lx + 11, ly), Poly([(lx - 13, ly - 26), (lx, ly - 36), (lx + 13, ly - 26)])]), IRON)
    hunter(g, 430, 556, 150, face=1, weapon="axe", rim_dx=-1.6)
    fog_band(g, 300, 360, 420, (80, 90, 120), 0.45, seed=6613)


L1566_RAYS = [dict(lx=M66[0], ly=M66[1], col=(170, 186, 232), k=1.6, region=Box(-2, -2, W + 2, 330), threshold=90,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=moon_receive(*M66, floor=0.3))]
L1566_ELEMENTS = [
    bat_el("bat1", 300, 60, s=10, speed=30, phase=0.1),
    bat_el("bat2", 330, 80, s=7, speed=30, phase=0.12),
    mist_el("mist", 450, 380, 300, 18, (110, 120, 150), alpha=0.45, length=90, seed=33),
    beam_el("beam", 700, 120, 520, 460, 40, 180, k=0.08),
    flame_el("lampL", 300, 318, 0.9, 0.1),
    flame_el("lampR", 600, 318, 0.9, 0.4),
]
L1566_DIFFS = [("rose", 450, 160, 0), ("window", 220, 250, 0), ("statue", 750, 250, 0), ("crow", 610, 524, 0),
               ("lantern", 230, 550, 0), ("gargoyle", 752, 82, 0)]


# =================================================================== Level 1567 hunter's workshop
L67 = (1100, -200)


def l1567_scene(g, d):
    # back wall (wood panelling below, plaster above), window right with moonlight
    g.fill(Box(-2, -2, W + 2, 420), tex(vgrad([(0, (54, 46, 42)), (420, (40, 34, 30))]), 0.12, 20, 30, 3, 6701))
    g.fill(Box(-2, 300, W + 2, 420), planks("v", (70, 50, 36), seed=6702, width=26))
    g.fill(Box(-2, 296, W + 2, 304), (44, 32, 24))
    win = Box(640, 70, 820, 260, 2)
    g.fill(win, vgrad([(70, (40, 56, 90)), (260, (70, 84, 120))]))
    moon(g, 760, 120, 18, col=(230, 230, 214), k=0.6, seed=6703)
    g.fill(Union([Box(640, 70, 820, 76), Box(640, 254, 820, 260), Box(640, 70, 646, 260), Box(814, 70, 820, 260), Box(727, 70, 733, 260), Box(640, 162, 820, 168)]),
           (50, 38, 30))
    # floor
    g.fill(Box(-2, 420, W + 2, H + 2), planks("h", (86, 62, 44), seed=6704, width=18))
    g.fill(Box(-2, 420, W + 2, H + 2), (0, 0, 0), alpha=lambda X, Y: 0.45 * smooth(600, 420, Y))
    # weapon rack on the wall: axe, cane sword, saw-toothed cleaver (original), pistol
    g.fill(Box(60, 80, 380, 96, 2), planks("h", (90, 66, 46), seed=6705, width=8))
    g.fill(Box(60, 230, 380, 246, 2), planks("h", (90, 66, 46), seed=6706, width=8))
    g.fill(Seg(110, 60, 110, 270, 4), tex(light_x((96, 70, 46), 104, 116, 1.3, 0.6), 0.2, 1, 6))
    if "axe" not in d:
        g.fill(Poly([(112, 70), (156, 56), (164, 100), (140, 104), (112, 96)]), lgrad(112, 0, 164, 0, [(0, (90, 92, 100)), (1, (170, 172, 180))]))
    g.fill(Seg(200, 70, 200, 280, 2.6), lgrad(196, 0, 204, 0, [(0, (190, 194, 204)), (1, (100, 102, 112))]))
    g.fill(Seg(200, 250, 200, 286, 4), (60, 40, 30))
    g.fill(Seg(186, 248, 214, 248, 2), (150, 120, 60))
    cle = Poly([(270, 70), (300, 70), (306, 210), (286, 226), (266, 210)])
    g.fill(cle, lgrad(266, 0, 306, 0, [(0, (110, 112, 120)), (1, (180, 182, 190))]))
    g.fill(Union([Poly([(304, 80 + i * 14), (312, 86 + i * 14), (304, 92 + i * 14)]) for i in range(9)]), (150, 152, 160))
    g.fill(Seg(286, 226, 286, 290, 4), (60, 40, 30))
    if "pistol" not in d:
        g.fill(Union([Ell(350, 160, 22, 10), Seg(338, 162, 330, 194, 6)]), sphere_paint(344, 156, 22, (70, 60, 56), ry=10, amb=0.4, spec=0.4))
        g.fill(Seg(352, 157, 384, 157, 4), cyl_paint(157, 4, (110, 110, 118), horizontal=True))
    # shelf with vials and books (left)
    g.fill(Box(420, 120, 600, 128, 1), (80, 58, 40))
    g.fill(Box(420, 210, 600, 218, 1), (80, 58, 40))
    vial_cols = [(170, 40, 50), (60, 130, 90), (170, 40, 50), (200, 180, 90), (80, 110, 190), (170, 40, 50)]
    if "vial" in d:
        vial_cols[3], vial_cols[4] = (90, 200, 220), (230, 120, 40)
    for i, vc in enumerate(vial_cols):
        x = 436 + i * 26
        g.fill(Union([Ell(x, 106, 9, 12), Box(x - 3, 86, x + 3, 98)]), sphere_paint(x - 3, 102, 9, vc, ry=12, amb=0.35, spec=0.7, shin=40))
        g.fill(Box(x - 4, 82, x + 4, 88, 1), (110, 84, 60))
    for i in range(7):
        x0 = 430 + i * 22
        hgt = 60 + (i * 7) % 18
        col = [(90, 40, 36), (50, 60, 80), (70, 70, 46), (100, 70, 40), (40, 50, 40), (80, 30, 50), (60, 50, 40)][i]
        g.fill(Box(x0, 210 - hgt, x0 + 18, 210, 1), tex(light_x(col, x0, x0 + 18, 1.3, 0.6), 0.15, 2, 6))
    if "book" not in d:
        g.fill(Poly([(586, 210), (594, 150), (614, 154), (606, 210)]), light_x((140, 110, 60), 586, 614, 1.2, 0.6))
    # workbench
    bench = Box(80, 380, 620, 404, 2)
    g.mul(Box(80, 404, 620, 470), 0.5, feather=10)
    g.fill(bench, tex(light_x((110, 80, 54), 80, 620, 1.2, 0.8), 0.2, 2, 8))
    for lx in (100, 590):
        g.fill(Box(lx, 404, lx + 20, 560), tex(light_x((90, 64, 44), lx, lx + 20, 1.2, 0.6), 0.2, 1.5, 8))
    g.fill(Box(100, 500, 610, 512), (80, 58, 40))
    # bench items: vice, gear, map with pins, candle, hat
    g.fill(Union([Box(130, 350, 170, 380, 2), Box(140, 340, 160, 352), Seg(126, 344, 174, 344, 2)]), cyl_paint(150, 20, (80, 82, 90), amb=0.35, spec=0.5))
    gx, gy = 230, 360
    teeth = 12
    tips = [(gx + 21 * math.cos(i * math.tau / teeth), gy + 21 * math.sin(i * math.tau / teeth)) for i in range(teeth)]
    gear = Union([Circ(gx, gy, 18)] + [Box(tx - 3.5, ty - 3.5, tx + 3.5, ty + 3.5, 1) for tx, ty in tips])
    g.fill(Diff(gear, Circ(gx, gy, 6)), sphere_paint(gx - 6, gy - 6, 24, (150, 120, 60) if "gear" not in d else (110, 116, 126), amb=0.4, spec=0.6))
    mp = Poly([(300, 372), (450, 366), (456, 380), (304, 384)])
    g.fill(mp, (196, 180, 140))
    g.fill(Union([Seg(320, 374, 360, 372, 0.8), Seg(360, 372, 400, 378, 0.8), Seg(380, 370, 430, 374, 0.8)]), (120, 90, 60))
    g.fill(Circ(410, 374, 2.6), (200, 40, 40))
    candle(g, 500, 380, 34, w=10, lit=True)
    # hat on a peg by the door (left wall edge)
    g.fill(Seg(30, 150, 50, 150, 3), (80, 58, 40))
    hatc = (36, 32, 30) if "hat" not in d else (90, 60, 40)
    g.fill(Ell(44, 166, 34, 6), light_x(hatc, 10, 78, 1.3, 0.6))
    g.fill(Box(30, 136, 58, 164, 5), light_x(hatc, 30, 58, 1.3, 0.6))
    # long coat hanging under it
    g.fill(Poly([(24, 172), (64, 172), (78, 360), (10, 360)]), tex(light_x((50, 44, 40), 10, 78, 1.2, 0.6), 0.15, 3, 12))
    # anvil and barrel on the floor (right)
    g.fill(Union([Poly([(680, 430), (800, 430), (820, 410), (700, 410), (660, 420)]), Box(712, 430, 770, 480), Box(696, 480, 786, 494)]),
           sphere_paint(720, 418, 80, (70, 72, 80), ry=40, amb=0.35, spec=0.6))
    barrel(g, 860, 560, 36, 100, seed=6707)
    if "tongs" not in d:
        g.fill(Union([Seg(700, 404, 780, 396, 3), Seg(700, 404, 776, 408, 3), Seg(690, 402, 706, 406, 5)]), (40, 40, 44))
    # moonlight pool on the floor
    g.add(Poly([(560, 440), (720, 440), (700, 600), (500, 600)]), (150, 166, 210), 0.12, feather=20)
    cobweb(g, 0, 0, 70, (1, 1))


L1567_RAYS = [dict(lx=L67[0], ly=L67[1], col=(170, 186, 232), k=1.6, region=Box(646, 76, 814, 254), threshold=60,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=Box(380, 60, W + 20, H + 20))]
L1567_ELEMENTS = [
    flame_el("candle", 500, 343, 1.0, 0.1),
    motes_el("dust", [(600, 330), (660, 380), (620, 460), (700, 300)], vx=3, vy=-4, length=24),
    beam_el("beam", 740, 160, 600, 560, 60, 180, k=0.08),
]
L1567_DIFFS = [("axe", 138, 80, 0), ("vial", 527, 104, 0), ("book", 600, 180, 0), ("gear", 230, 360, 0), ("pistol", 352, 168, 0),
               ("hat", 44, 152, 0), ("tongs", 740, 402, 0)]


# =================================================================== Level 1568 rooftops under a red moon
M68 = (330, 210, 120)


def l1568_scene(g, d):
    mx, my, mr = M68
    sky(g, [(0, (30, 8, 12)), (220, (90, 30, 30)), (360, (120, 60, 50))])
    stars(g, 40, 200, seed=6801, bright=(255, 220, 200))
    moon(g, mx, my, mr, col=(220, 80, 60), halo=(200, 60, 50), k=1.0, seed=6802)
    cloud_layer(g, 240, 300, (180, 80, 70), (60, 20, 24), cover=0.32, sx=200, sy=10, seed=6803, alpha=0.6)
    skyline(g, 360, 40, 140, (40, 14, 18), 6804, spires=0.5, lit=(255, 170, 100), lit_p=0.06)
    # clock tower crossing the moon (left of centre)
    tw = Box(380, 110, 460, 470)
    wall(g, tw, (50, 30, 32), 6805, 380, 460, light=-1)
    spire(g, 420, 112, 90, 120, (46, 26, 30), seed=6806, light=-1)
    g.fill(Circ(420, 180, 30), (230, 210, 170) if "clock" not in d else (120, 90, 80))
    g.fill(Circ(420, 180, 30) - Circ(420, 180, 27), (40, 24, 24))
    for i in range(12):
        a = i * math.tau / 12
        g.fill(Seg(420 + 23 * math.cos(a), 180 + 23 * math.sin(a), 420 + 26 * math.cos(a), 180 + 26 * math.sin(a), 1.2), (40, 24, 24))
    ha = -math.pi / 2 + 0.9
    g.fill(Seg(420, 180, 420 + 15 * math.cos(ha), 180 + 15 * math.sin(ha), 2), (30, 20, 20))
    g.fill(Seg(420, 180, 420 + 22 * math.cos(-math.pi / 2 + 4.2), 180 + 22 * math.sin(-math.pi / 2 + 4.2), 1.4), (30, 20, 20))
    for yy in (250, 340):
        lancet(g, 406, 434, yy, yy + 50, lit=(255, 170, 100) if yy == 340 else None)
    # weathervane on a far gable (right)
    g.fill(Poly([(640, 330), (700, 260), (760, 330)]), (44, 16, 20))
    g.fill(Seg(700, 260, 700, 220, 1.6), (30, 12, 14))
    k = 1 if "vane" not in d else -1
    g.fill(Union([Seg(700 - 30 * k, 226, 700 + 26 * k, 226, 2.4), Poly([(700 + 22 * k, 218), (700 + 40 * k, 226), (700 + 22 * k, 234)]),
                  Poly([(700 - 26 * k, 226), (700 - 40 * k, 212), (700 - 32 * k, 226), (700 - 40 * k, 240)]),
                  Ell(700 + 2 * k, 212, 12, 9), Circ(700 + 12 * k, 202, 5), Poly([(700 - 8 * k, 208), (700 - 20 * k, 194), (700 - 10 * k, 214)])]), (30, 12, 14))
    # near rooftops: slate roofs with chimneys
    def roof(x0, x1, ridge_y, eave_y, col, seed):
        sh = Poly([(x0, eave_y), (x0 + 30, ridge_y), (x1 - 30, ridge_y), (x1, eave_y), (x1, H + 10), (x0, H + 10)])

        def slate(X, Y):
            row = np.floor((Y - ridge_y) / 9).astype(np.int64)
            fx = (X + (row % 2) * 7) / 14 - np.floor((X + (row % 2) * 7) / 14)
            n = fbm(X, Y, 3, 3, 3, seed)
            return C(col) * ((0.7 + 0.3 * smooth(0.0, 0.12, fx)) * (0.8 + 0.4 * n) * (0.75 + 0.25 * smooth(0, 0.3, (Y - ridge_y) / 9 - row)))[..., None]
        g.fill(sh, slate)
        g.add(Seg(x0 + 30, ridge_y, x1 - 30, ridge_y, 1.6), (255, 120, 90), 0.25)
        return sh
    g.fill(Box(330, 440, 500, H + 10), stone((40, 22, 26), 6814, 18, 9))
    g.fill(Box(330, 440, 500, H + 10), (0, 0, 0), alpha=lambda X, Y: 0.3 + 0.5 * smooth(440, 600, Y))
    for wy in (500, 560):
        lancet(g, 400, 428, wy, wy + 30, lit=(255, 170, 100) if wy == 560 else None)
    roof(-40, 360, 420, 470, (52, 40, 44), 6807)
    roof(480, 960, 400, 450, (48, 38, 42), 6808)
    for cx, top, pots in ((120, 340, 3), (300, 360, 2), (620, 330, 2), (820, 320, 3)):
        n = pots if not (cx == 820 and "pots" in d) else 1
        ch = Box(cx - 26, top, cx + 26, 470)
        wall(g, ch, (90, 50, 44), 6809 + cx, cx - 26, cx + 26, light=-1, bw=12, bh=6)
        g.fill(Box(cx - 30, top - 8, cx + 30, top), (60, 36, 34))
        for i in range(n):
            px = cx - (n - 1) * 12 + i * 24
            g.fill(Box(px - 7, top - 30, px + 7, top - 8, 2), cyl_paint(px, 7, (150, 80, 60), amb=0.35, spec=0.2))
    # gargoyle on the near left parapet
    gx, gy = 220, 418
    g.fill(Box(170, 418, 260, 470), stone((70, 46, 46), 6810, 14, 8))
    g.fill(Union([Ell(gx, gy - 18, 20, 18), Circ(gx + 22, gy - 34, 11), Poly([(gx + 28, gy - 30), (gx + 46, gy - 24), (gx + 30, gy - 22)]),
                  Poly([(gx - 8, gy - 30), (gx - 40, gy - 70), (gx - 30, gy - 36)] if "wing" not in d else [(gx - 8, gy - 30), (gx - 46, gy - 40), (gx - 20, gy - 20)]),
                  Poly([(gx + 18, gy - 44), (gx + 14, gy - 58), (gx + 26, gy - 44)])]),
           tex(light_x((70, 50, 52), gx - 40, gx + 46, 1.3, 0.6), 0.25, 2, 2, 3, 6811))
    g.fill(Circ(gx + 26, gy - 36, 2), (255, 120, 80))
    # hunter on the right roof ridge, rim-lit by the moon
    hunter(g, 560, 404, 180, face=-1, weapon="axe", rim_dx=2.0, rim_col=(255, 120, 90), rim_k=0.7, coat=(26, 20, 22), trim=(40, 30, 30))
    # crows on the ridge
    crow(g, 760, 400, 1.2, face=-1)
    if "crow" not in d:
        crow(g, 806, 400, 1.4, face=1)
    g.fog(360, 470, (110, 40, 40), 0.25, 0.0, noise=0.5, seed=6812)


L1568_RAYS = [dict(lx=M68[0], ly=M68[1], col=(230, 110, 90), k=1.3, region=Box(-2, -2, W + 2, 360), threshold=70,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=moon_receive(*M68, floor=0.25))]
L1568_ELEMENTS = [
    bat_el("bat1", 600, 120, s=12, speed=-30, phase=0.2, col=(20, 6, 8)),
    bat_el("bat2", 630, 140, s=8, speed=-30, phase=0.24, col=(20, 6, 8)),
    bat_el("bat3", 150, 80, s=9, speed=24, phase=0.6, col=(20, 6, 8)),
    mist_el("mist", 450, 470, 400, 14, (120, 50, 50), alpha=0.35, length=80, seed=34),
]
L1568_DIFFS = [("clock", 420, 180, 0), ("vane", 700, 214, 0), ("pots", 820, 304, 0), ("wing", 190, 380, 0), ("crow", 800, 386, 0)]


# =================================================================== Level 1569 lantern-lit forbidden woods
def l1569_scene(g, d):
    sky(g, [(0, (10, 16, 18)), (300, (30, 44, 44)), (420, (40, 54, 52))])
    g.glow(450, 300, 500, (80, 110, 100), 0.25)
    for i, (base, col, a) in enumerate(((360, (30, 42, 42), 0.5), (390, (22, 32, 32), 0.3))):
        treeline(g, base, 110 - i * 20, 14, 6901 + i, col, light=0.0, haze=((60, 80, 78), a, 0.1), conifer=True)
    g.fill(Box(-2, 380, W + 2, H + 2), tex(vgrad([(380, (34, 40, 34)), (600, (18, 22, 18))]), 0.35, 4, 3, 4, 6903))
    path = Rough(Poly([(380, 384), (470, 384), (700, 610), (160, 610)]), 4, 14, 6904)
    g.fill(path, grain_tex(vgrad([(384, (60, 58, 50)), (600, (40, 36, 30))]), 0.2, 6905), feather=2)
    # big gnarled trees framing
    for x, h, s, lean in ((80, 600, 6906, 0.1), (840, 620, 6907, -0.12), (250, 420, 6908, 0.05), (640, 440, 6909, -0.05)):
        dead_tree(g, x, 420 if h < 500 else 600, h, seed=s, col=(22, 22, 20), lean=lean, w=h * 0.05, depth=5)
    # hut with a lit window in the distance
    hx = 520
    g.fill(Union([Box(hx, 330, hx + 80, 386), Poly([(hx - 10, 334), (hx + 40, 296), (hx + 90, 334)])]), (30, 30, 28))
    g.fill(Box(hx + 14, 346, hx + 30, 362), (255, 190, 110) if "hut" not in d else (30, 34, 40))
    if "hut" not in d:
        g.glow(hx + 22, 354, 40, FIRE, 0.25)
    g.fill(Box(hx + 50, 300, hx + 60, 320), (30, 30, 28))
    # wooden fence along the path
    for x in range(170, 380, 30):
        t = (x - 170) / 210
        y = 560 - 170 * t
        hgt = 60 - 30 * t
        g.fill(Seg(x, y, x, y - hgt, 3.4 - t * 1.6), tex(light_x((80, 64, 46), x - 4, x + 4, 1.3, 0.6), 0.2, 1, 4))
    g.fill(Seg(170, 528, 380, 372, 2.4), (76, 60, 44))
    g.fill(Seg(170, 546, 380, 380, 2.0), (76, 60, 44))
    # lantern posts along the path
    for x, y, hgt, key in ((260, 480, 140, "lamp"), (440, 396, 60, None)):
        g.fill(Seg(x, y, x, y - hgt, 3 * hgt / 140), (40, 32, 26))
        g.fill(Seg(x, y - hgt, x + 20 * hgt / 140, y - hgt, 2 * hgt / 140), (40, 32, 26))
        lx, ly = x + 18 * hgt / 140, y - hgt + 10 * hgt / 140
        s = hgt / 140
        lit = not (key and key in d)
        if lit:
            g.glow(lx, ly + 8 * s, 70 * s, FIRE, 0.4)
        g.fill(Box(lx - 7 * s, ly, lx + 7 * s, ly + 18 * s, 2 * s), (255, 200, 120) if lit else (36, 40, 40))
        g.fill(Poly([(lx - 9 * s, ly), (lx, ly - 8 * s), (lx + 9 * s, ly)]), IRON)
    # hanging cages from the big trees
    cage(g, 150, 150, 46, 80, chain_len=80)
    if "cage" not in d:
        cage(g, 760, 190, 40, 70, chain_len=110)
    # eyes in the dark
    for ex, ey, pair in ((70, 470, True), (870, 440, "eyes" not in d)):
        if pair:
            for dx in (-8, 8):
                g.glow(ex + dx, ey, 14, (255, 210, 90), 0.9)
                g.fill(Ell(ex + dx, ey, 4.5, 2.8), (255, 230, 140))
    # signpost
    g.fill(Seg(680, 520, 680, 440, 3.4), (70, 56, 40))
    ang = 0.2 if "sign" not in d else -0.25
    pts = [(680, 452), (740, 452 + 60 * ang), (752, 460 + 60 * ang), (740, 468 + 60 * ang), (680, 468)]
    g.fill(Poly(pts), tex(light_x((100, 80, 56), 680, 752, 1.2, 0.7), 0.2, 1.5, 4))
    # mushrooms
    mcol = (200, 60, 50) if "mush" not in d else (200, 180, 120)
    for mx_, s in ((262, 1.5), (290, 1.0), (238, 0.9)):
        g.fill(Box(mx_ - 2 * s, 568 - 14 * s, mx_ + 2 * s, 568), (220, 210, 190))
        g.fill(Inter(Ell(mx_, 568 - 14 * s, 11 * s, 9 * s), Box(mx_ - 12 * s, 556 - 14 * s, mx_ + 12 * s, 568 - 14 * s)), sphere_paint(mx_ - 3 * s, 564 - 18 * s, 11 * s, mcol, amb=0.4, spec=0.3))
    blades(g, 420, 600, (40, 52, 40), n=260, seed=6910, hmax=22)
    fog_band(g, 340, 400, 470, (80, 100, 96), 0.5, seed=6911)


L1569_ELEMENTS = [
    mist_el("mist1", 450, 420, 320, 20, (100, 120, 116), alpha=0.5, length=80, seed=35),
    mist_el("mist2", 300, 560, 300, 16, (80, 96, 92), alpha=0.35, length=100, seed=36),
    glint_el("flies", [(360, 330), (480, 440), (620, 360), (220, 420)], col=(200, 255, 150), r=3, speed=0.5),
]
L1569_DIFFS = [("cage", 760, 220, 0), ("hut", 542, 354, 0), ("lamp", 278, 350, 0), ("eyes", 870, 440, 0), ("sign", 716, 460, 0),
               ("mush", 262, 550, 0)]



# =================================================================== Level 1570 rotting fishing village in the rain
def stilt_hut(g, x0, x1, floor_y, roof_y, water_y, col, seed, lit=None, light=-1):
    for px in np.linspace(x0 + 6, x1 - 6, 4):
        g.fill(Seg(px, floor_y, px + 2, water_y + 30, 4), tex(light_x((50, 42, 34), px - 4, px + 4, 1.2, 0.6), 0.2, 1, 6))
    g.fill(Box(x0 - 8, floor_y - 6, x1 + 8, floor_y + 4), planks("h", (66, 54, 42), seed=seed, width=5))
    body = Box(x0, roof_y + 20, x1, floor_y - 6)
    g.fill(body, planks("v", col, seed=seed + 1, width=12))
    g.fill(body, (0, 0, 0), alpha=lambda X, Y: 0.15 + 0.35 * smooth(x0, x1, X) if light < 0 else 0.5 - 0.35 * smooth(x0, x1, X))
    roof_s = Poly([(x0 - 16, roof_y + 24), ((x0 + x1) / 2, roof_y - 14), (x1 + 16, roof_y + 24)])
    g.fill(roof_s, tex(light_y((56, 50, 46), roof_y - 14, roof_y + 24, 1.2, 0.7), 0.3, 3, 2, 3, seed + 2))
    wx = (x0 + x1) / 2
    win = Box(wx - 12, roof_y + 40, wx + 12, roof_y + 62, 1)
    if lit:
        g.glow(wx, roof_y + 51, 50, FIRE, 0.3)
        g.fill(win, (255, 190, 110))
    else:
        g.fill(win, (24, 28, 34))
    g.fill(Union([Box(wx - 1, roof_y + 40, wx + 1, roof_y + 62), Box(wx - 12, roof_y + 50, wx + 12, roof_y + 52)]), (40, 32, 26))
    return body


def rowboat(g, x, y, L, col, seed=0, face=1):
    hull = Poly([(x - L / 2, y - 14), (x + L / 2, y - 14), (x + L / 2 - 14, y + 6), (x - L / 2 + 20, y + 8)])
    g.mul(Ell(x, y + 10, L * 0.55, 6), 0.5, feather=5)
    g.fill(hull, tex(light_y(col, y - 14, y + 8, 1.25, 0.6), 0.2, 2, 6, 3, seed))
    g.fill(Seg(x - L / 2, y - 14, x + L / 2, y - 14, 2.2), (60, 48, 38))
    for k in (-0.25, 0.1):
        g.fill(Seg(x + L * k, y - 12, x + L * k, y + 4, 1.4), mixc(col, (0, 0, 0), 0.35))
    return hull


def l1570_scene(g, d):
    sky(g, [(0, (30, 36, 40)), (220, (60, 68, 70)), (280, (72, 80, 82))])
    cloud_layer(g, 0, 200, (90, 98, 104), (40, 46, 52), cover=0.7, sx=200, sy=30, seed=7001, alpha=0.9)
    # sea and far headland with a lighthouse
    g.fill(Box(-2, 280, W + 2, 420), vgrad([(280, (50, 60, 64)), (420, (30, 38, 42))]))
    g.fill(Under(lambda x: 280 - 40 * np.exp(-((x - 760) / 120.0) ** 2) + (fbm1(x, 30, 3, 7002) - 0.5) * 8, 560, 960, 300), (34, 40, 42))
    lh = Poly([(766, 244), (794, 244), (788, 170), (772, 170)])
    g.fill(lh, light_x((200, 196, 186), 766, 794, 1.2, 0.6))
    g.fill(Union([Box(768, 214, 792, 222), Box(770, 186, 790, 194)]), (150, 40, 40))
    g.fill(Box(770, 152, 790, 170), (40, 40, 44))
    if "light" not in d:
        g.glow(780, 160, 60, (255, 230, 160), 0.6)
        g.fill(Box(773, 155, 787, 168), (255, 240, 200))
    g.fill(Poly([(766, 152), (780, 140), (794, 152)]), (40, 40, 44))
    for y in range(300, 420, 9):
        g.add(Seg(0, y, W, y, 0.6), (120, 130, 140), 0.06)
    # stilt huts on the left over the water
    stilt_hut(g, 40, 170, 300, 170, 420, (78, 66, 56), 7003, lit="hut" not in d)
    stilt_hut(g, 210, 300, 330, 230, 420, (70, 62, 54), 7004, lit=None)
    # pier running out to the right
    g.fill(Poly([(330, 390), (900, 372), (900, 384), (330, 400)]), planks("v", (72, 60, 48), seed=7005, width=9))
    for px in range(350, 900, 70):
        y = 400 - (px - 330) * 0.03
        g.fill(Seg(px, y - 26, px, y + 30, 4), tex(light_x((56, 46, 36), px - 4, px + 4, 1.2, 0.6), 0.2, 1, 6))
    # net drying poles with floats
    g.fill(Seg(560, 380, 560, 280, 3), (60, 50, 40))
    g.fill(Seg(700, 376, 700, 276, 3), (60, 50, 40))
    net = Poly([(560, 284), (700, 280), (690, 350), (570, 356)])
    g.fill(net, (40, 40, 38), alpha=lambda X, Y: 0.55 * (smooth(0.75, 0.9, np.abs(np.sin(X * 0.6))) + smooth(0.75, 0.9, np.abs(np.sin(Y * 0.6)))).clip(0, 1))
    for i, fx in enumerate(range(574, 690, 22)):
        fc = (220, 120, 50) if not ("float" in d and i in (2, 3)) else (90, 150, 210)
        g.fill(Circ(fx, 284 + (fx - 560) * -0.03, 5), sphere_paint(fx - 1, 282, 5, fc, amb=0.4, spec=0.4))
    # shore (mud and shingle)
    g.fill(Under(lambda x: 430 + (fbm1(x, 80, 3, 7006) - 0.5) * 16, -20, W + 20, H + 20),
           tex(vgrad([(420, (64, 58, 50)), (600, (38, 34, 30))]), 0.4, 5, 3, 4, 7007))
    g.add(Box(-2, 420, W + 2, 470), (120, 130, 140), 0.06, feather=10)
    # beached boats
    rowboat(g, 420, 500, 170, (60, 90, 100) if "boat" not in d else (130, 60, 50), seed=7008)
    rowboat(g, 160, 560, 200, (110, 96, 76), seed=7009)
    g.fill(Seg(330, 480, 370, 520, 2.4), (90, 70, 50))
    # fish drying rack
    g.fill(Union([Seg(610, 560, 620, 460, 3), Seg(760, 560, 750, 460, 3), Seg(606, 470, 764, 470, 3)]), (70, 56, 42))
    for i, fx in enumerate(range(626, 750, 18)):
        g.fill(Seg(fx, 470, fx, 478, 0.8), (40, 34, 30))
        g.fill(Ell(fx, 494, 5, 15), sphere_paint(fx - 2, 490, 5, (150, 150, 140), ry=15, amb=0.4, spec=0.5))
    # barrels and a crow on a mooring post
    barrel(g, 840, 560, 30, 76, seed=7010)
    if "barrel" not in d:
        barrel(g, 870, 590, 26, 64, seed=7011)
    g.fill(Seg(520, 460, 520, 380, 6), tex(light_x((60, 50, 40), 514, 526, 1.2, 0.6), 0.2, 1, 6))
    if "crow" not in d:
        crow(g, 520, 380, 1.3, face=1)
    g.fog(260, 330, (90, 98, 104), 0.5, 0.0)
    g.fog(380, 460, (70, 78, 84), 0.0, 0.25, noise=0.5, seed=7012)
    g.mul(Box(-2, -2, W + 2, H + 2), 0.15)


L1570_ELEMENTS = [
    rain_layer("rain", 7020, 60, 26, 1.1, 0.35, 260, mask=0),
    mist_el("mist", 450, 300, 400, 16, (100, 108, 112), alpha=0.4, length=90, seed=37),
    glint_el("beam", [(780, 160)], col=(255, 240, 200), r=14, speed=0.25),
]
L1570_DIFFS = [("light", 780, 160, 0), ("hut", 105, 220, 0), ("float", 630, 282, 0), ("boat", 420, 494, 0), ("barrel", 870, 560, 0),
               ("crow", 520, 362, 0)]


# =================================================================== Level 1571 forbidden library
L71 = (450, -400)
WIN71 = (380, 60, 520, 300)


def bookshelf(g, x0, x1, y0, y1, seed, shelf=74, wood=(70, 48, 34)):
    rnd = random.Random(seed)
    g.fill(Box(x0, y0, x1, y1), tex(light_y(wood, y0, y1, 1.1, 0.7), 0.2, 2, 8, 3, seed))
    cols = [(110, 30, 30), (40, 60, 90), (60, 80, 50), (120, 90, 50), (70, 40, 70), (40, 40, 44), (130, 110, 80)]
    y = y0 + 8
    while y + shelf <= y1 - 4:
        g.fill(Box(x0 + 6, y, x1 - 6, y + shelf - 8), (22, 16, 14))
        x = x0 + 8
        while x < x1 - 12:
            bw = rnd.uniform(6, 13)
            bh = rnd.uniform(0.62, 0.95) * (shelf - 10)
            c = cols[rnd.randrange(len(cols))]
            if rnd.random() < 0.08:
                g.fill(Seg(x + 2, y + shelf - 9, x + bh * 0.6, y + shelf - 9 - bh * 0.75, bw * 0.5), light_x(c, x, x + bh, 1.2, 0.7))
                x += bh * 0.62
                continue
            g.fill(Box(x, y + shelf - 8 - bh, min(x + bw, x1 - 8), y + shelf - 8, 1), light_x(c, x, x + bw, 1.3, 0.6))
            g.fill(Box(x, y + shelf - 8 - bh * 0.85, min(x + bw, x1 - 8), y + shelf - 8 - bh * 0.8), (200, 170, 90), alpha=0.5)
            x += bw + 0.6
        g.fill(Box(x0, y + shelf - 8, x1, y + shelf - 2), light_y(wood, y + shelf - 8, y + shelf - 2, 1.3, 0.7))
        y += shelf


def l1571_scene(g, d):
    g.fill(Box(-2, -2, W + 2, 470), tex(vgrad([(0, (40, 34, 34)), (470, (30, 26, 26))]), 0.15, 30, 30, 3, 7101))
    # tall window in the middle
    x0, y0, x1, y1 = WIN71
    w_shape = arch(x0, x1, y0 + 70, y1)
    g.fill(w_shape, vgrad([(y0, (40, 54, 90)), (y1, (90, 104, 140))]))
    moon(g, 470, 130, 22, k=0.5, seed=7102)
    g.fill(Inter(Union([Box(447, y0, 453, y1), Box(x0, 180, x1, 185), Box(x0, 240, x1, 245)]), w_shape), (36, 28, 26))
    g.fill(Diff(arch(x0 - 10, x1 + 10, y0 + 70, y1 + 8), w_shape), stone((70, 64, 60), 7103, 16, 10))
    # bookshelves left and right, two storeys with a gallery rail
    bookshelf(g, -10, 360, 20, 460, 7104)
    bookshelf(g, 540, 910, 20, 460, 7105)
    g.fill(Box(-10, 236, 360, 246), (60, 42, 30))
    g.fill(Box(540, 236, 910, 246), (60, 42, 30))
    for x in range(0, 360, 22):
        g.fill(Box(x, 214, x + 3, 236), (54, 38, 28))
    for x in range(546, 910, 22):
        g.fill(Box(x, 214, x + 3, 236), (54, 38, 28))
    g.fill(Box(-10, 210, 360, 216), (64, 46, 32))
    g.fill(Box(540, 210, 910, 216), (64, 46, 32))
    # a scroll lying on the right shelf
    if "scroll" not in d:
        g.fill(Seg(640, 362, 712, 362, 7), cyl_paint(362, 7, (220, 206, 170), horizontal=True))
        g.fill(Box(672, 355, 678, 369), (150, 40, 40))
    # ladder leaning on the left shelves
    for sx_ in (0, 1):
        g.fill(Seg(180 + sx_ * 46, 470, 230 + sx_ * 46, 40, 4), tex(light_x((110, 80, 50), 170, 290, 1.3, 0.6), 0.2, 1, 8))
    for i in range(1, 12):
        if "rung" in d and i == 5:
            continue
        t = i / 12
        g.fill(Seg(180 + 50 * t, 470 - 430 * t, 226 + 50 * t, 470 - 430 * t, 2.6), (120, 88, 56))
    # floor
    g.fill(Box(-2, 460, W + 2, H + 2), planks("h", (80, 56, 38), seed=7106, width=20))
    g.fill(Box(-2, 460, W + 2, H + 2), (0, 0, 0), alpha=lambda X, Y: 0.5 * smooth(600, 460, Y))
    g.fill(Box(-2, 456, W + 2, 464), (50, 36, 26))
    # chandelier
    g.fill(Seg(450, -2, 450, 70, 1.6), (40, 34, 30))
    g.fill(Ell(450, 90, 70, 10) - Ell(450, 88, 62, 6), (110, 90, 50))
    for i, cx in enumerate((390, 420, 450, 480, 510)):
        if "chand" in d and i == 3:
            continue
        candle(g, cx, 88, 18, w=6, lit=True)
    # reading desk with an open book and candle
    g.mul(Ell(450, 560, 220, 20), 0.5, feather=14)
    g.fill(Box(250, 470, 650, 494, 2), tex(light_x((100, 70, 46), 250, 650, 1.2, 0.8), 0.2, 2, 8))
    for lx in (270, 610):
        g.fill(Box(lx, 494, lx + 18, 580), tex(light_x((80, 56, 38), lx, lx + 18, 1.2, 0.6), 0.2, 1, 8))
    g.fill(Poly([(360, 470), (450, 462), (450, 440), (366, 446)]), (226, 214, 186))
    g.fill(Poly([(450, 462), (540, 470), (534, 446), (450, 440)]), (214, 202, 174))
    for k in range(5):
        g.fill(Seg(376, 450 + k * 4, 440, 446 + k * 4, 0.6), (120, 100, 80))
        g.fill(Seg(460, 446 + k * 4, 524, 450 + k * 4, 0.6), (120, 100, 80))
    if "ribbon" not in d:
        g.fill(Poly([(452, 462), (458, 462), (458, 492), (455, 486), (452, 492)]), (170, 30, 40))
    candle(g, 300, 470, 30, w=9)
    # hourglass
    hx, hy = 590, 470
    g.fill(Union([Box(hx - 14, hy - 6, hx + 14, hy), Box(hx - 14, hy - 56, hx + 14, hy - 50)]), (90, 66, 40))
    g.fill(Union([Seg(hx - 12, hy - 6, hx - 12, hy - 50, 1.4), Seg(hx + 12, hy - 6, hx + 12, hy - 50, 1.4)]), (90, 66, 40))
    g.fill(Poly([(hx - 10, hy - 50), (hx + 10, hy - 50), (hx + 1.5, hy - 28), (hx + 10, hy - 6), (hx - 10, hy - 6), (hx - 1.5, hy - 28)]), (200, 220, 230), alpha=0.35)
    sand = (220, 180, 110)
    if "sand" not in d:
        g.fill(Poly([(hx - 9, hy - 7), (hx + 9, hy - 7), (hx + 4, hy - 18), (hx - 4, hy - 18)]), sand)
        g.fill(Poly([(hx - 5, hy - 44), (hx + 5, hy - 44), (hx + 1, hy - 32), (hx - 1, hy - 32)]), sand)
    else:
        g.fill(Poly([(hx - 9, hy - 49), (hx + 9, hy - 49), (hx + 2, hy - 32), (hx - 2, hy - 32)]), sand)
    # globe on a stand (right)
    gx, gy = 780, 400
    g.fill(Union([Seg(gx, gy + 40, gx, gy + 140, 4), Seg(gx - 40, gy + 160, gx, gy + 140, 4), Seg(gx + 40, gy + 160, gx, gy + 140, 4)]),
           (110, 80, 50) if "globe" not in d else (150, 150, 160))
    g.fill(Circ(gx, gy, 40), sphere_paint(gx - 12, gy - 12, 40, (170, 150, 100), amb=0.4, spec=0.3))
    g.fill(Rough(Ell(gx - 8, gy - 6, 18, 14), 4, 6, 7107), (110, 120, 70))
    g.fill(Rough(Ell(gx + 16, gy + 16, 10, 12), 3, 5, 7108), (110, 120, 70))
    g.fill(Circ(gx, gy, 46) - Circ(gx, gy, 42), (150, 120, 60))
    # stack of books on the floor
    for i, (c, w) in enumerate((((90, 40, 36), 70), ((40, 60, 90), 64), ((110, 90, 50), 58))):
        if "stack" in d and i == 2:
            continue
        y = 580 - i * 14
        g.fill(Box(90 - w / 2, y - 14, 90 + w / 2, y, 2), light_y(c, y - 14, y, 1.3, 0.7))
        g.fill(Box(90 - w / 2 + 3, y - 12, 90 + w / 2, y - 3), (220, 210, 180))
    cobweb(g, 910, 0, 60, (-1, 1))


L1571_RAYS = [dict(lx=L71[0], ly=L71[1], col=(170, 186, 232), k=1.6, region=Box(WIN71[0], WIN71[1], WIN71[2], WIN71[3]), threshold=70,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=Box(-20, 160, W + 20, H + 20))]
L1571_ELEMENTS = [
    flame_el("deskc", 300, 437, 1.1, 0.1),
    beam_el("beam", 450, 220, 450, 580, 120, 300, k=0.08),
    motes_el("dust", [(420, 340), (480, 400), (450, 300), (500, 360)], vx=2, vy=-4, length=24),
] + [flame_el("ch%d" % i, cx, 67, 0.7, i * 0.2) for i, cx in enumerate((390, 420, 450, 510))]
L1571_DIFFS = [("chand", 480, 76, 0), ("rung", 220, 260, 0), ("scroll", 676, 362, 0), ("ribbon", 455, 478, 0), ("sand", 590, 440, 0),
               ("globe", 780, 520, 0), ("stack", 90, 552, 0)]


# =================================================================== Level 1572 sewer tunnel
VP72 = (450, 300)
G72 = (420, 30, 480, 60)        # ceiling grate opening (light from above)


def l1572_scene(g, d):
    g.fill(Box(-2, -2, W + 2, H + 2), (14, 14, 16))
    # receding brick arches (near to far)
    rings = 9
    for i in range(rings):
        t = i / (rings - 1)
        k = 1 - 0.86 * t ** 0.7
        cx, cy = VP72
        w, h = 460 * k, 330 * k
        outer = Union([Ell(cx, cy - h * 0.2, w, h * 0.8) & Box(cx - w, cy - h, cx + w, cy - h * 0.2), Box(cx - w, cy - h * 0.2, cx + w, cy + h * 0.9)])
        c = mixc((96, 70, 56), (20, 18, 18), t ** 0.6)
        g.fill(outer, ashlar(c, max(6, 30 * k), max(3, 12 * k), 7201 + i))
        g.mul(outer, 0.15 + 0.2 * t)
    g.fill(Box(VP72[0] - 50, VP72[1] - 40, VP72[0] + 50, VP72[1] + 50), (10, 10, 12))
    # far gate with a warm light behind it
    g.glow(450, 300, 70, (255, 170, 90), 0.35)
    gate = Union([Box(x, 262, x + 2.4, 346) for x in range(410, 492, 9)] + [Box(406, 270, 494, 274), Box(406, 320, 494, 324)])
    g.fill(gate, (20, 18, 18))
    # walkways and water channel
    g.fill(Poly([(-20, 600), (300, 600), (430, 340), (400, 340)]), tex(light_x((70, 62, 56), -20, 430, 1.1, 0.6), 0.3, 6, 4, 3, 7210))
    g.fill(Poly([(920, 600), (600, 600), (470, 340), (500, 340)]), tex(light_x((70, 62, 56), 470, 920, 0.6, 1.1), 0.3, 6, 4, 3, 7211))
    water = Poly([(300, 600), (600, 600), (470, 340), (430, 340)])
    g.fill(water, vgrad([(340, (40, 44, 40)), (600, (20, 30, 28))]))
    g.add(Poly([(420, 600), (480, 600), (456, 340), (446, 340)]), (255, 170, 90), 0.08, feather=16)
    for y in range(360, 600, 12):
        hw = (y - 340) / 260 * 150 + 20
        g.add(Seg(450 - hw * 0.6, y, 450 + hw * 0.5, y, 0.7), (120, 140, 130), 0.1)
    # pipes and a valve wheel on the right wall
    g.fill(Seg(920, 210, 520, 290, 10, 3), (80, 64, 50))
    g.fill(Seg(920, 236, 530, 300, 8, 2.4), (70, 60, 52))
    vx, vy = 800, 250
    vc = (160, 40, 40) if "valve" not in d else (60, 130, 90)
    g.fill(Circ(vx, vy, 22) - Circ(vx, vy, 17), vc)
    g.fill(Union([Seg(vx - 20, vy, vx + 20, vy, 2.4), Seg(vx, vy - 20, vx, vy + 20, 2.4), Circ(vx, vy, 5)]), vc)
    # wall lanterns
    for x, y, key in ((110, 250, "lamp"), (300, 290, None), (640, 296, None)):
        s = 1.0 if x in (110,) else 0.6
        lit = not (key and key in d)
        g.fill(Seg(x, y + 26 * s, x, y + 6 * s, 2 * s), IRON)
        if lit:
            g.glow(x, y + 12 * s, 90 * s, FIRE, 0.4)
        g.fill(Box(x - 9 * s, y - 8 * s, x + 9 * s, y + 14 * s, 2 * s), (255, 200, 120) if lit else (40, 40, 42))
        g.fill(Poly([(x - 11 * s, y - 8 * s), (x, y - 18 * s), (x + 11 * s, y - 8 * s)]), IRON)
    # plaque on the left wall
    if "plaque" not in d:
        g.fill(Box(200, 170, 260, 206, 2), sphere_paint(222, 182, 40, (130, 110, 70), ry=24, amb=0.4, spec=0.5))
        g.fill(Union([Box(210, 180 + k * 7, 250, 182 + k * 7) for k in range(3)]), (70, 56, 36))
    # hanging chain from the vault
    if "chain" not in d:
        chain(g, 640, 60, 640, 160, sag=0)
    # floating crate and a barrel on the walkway
    if "crate" not in d:
        crate(g, 400, 520, 46, 34, seed=7212)
    barrel(g, 820, 560, 30, 78, seed=7213)
    g.fill(Box(G72[0], 0, G72[2], 6), (10, 10, 12))
    g.fog(300, 600, (60, 60, 56), 0.0, 0.2, noise=0.5, sx=100, sy=10, seed=7214)


L1572_ELEMENTS = [
    mist_el("mist", 450, 470, 180, 12, (90, 96, 90), alpha=0.35, length=60, seed=38),
    glint_el("drips", [(430, 420), (470, 480), (450, 560)], col=(200, 220, 210), r=4, speed=0.4),
    E("drip", el(lambda g, m: g.fill(Ell(640, 170, 2, 4), (170, 190, 190))), daynight="untinted",
      anim=dict(driftVelocity=(0, -120), driftLength=330, driftFade=True)),
    beam_el("shaft", 450, 0, 450, 520, 40, 160, col=(200, 210, 230), k=0.12),
]
L1572_DIFFS = [("valve", 800, 250, 0), ("lamp", 110, 252, 0), ("plaque", 230, 188, 0), ("chain", 640, 110, 0), ("crate", 423, 503, 0)]


# =================================================================== Level 1573 duel on the bridge
M73 = (450, 200, 110)


def l1573_scene(g, d):
    mx, my, mr = M73
    sky(g, [(0, (6, 10, 22)), (250, (34, 44, 70)), (400, (60, 70, 96))])
    stars(g, 80, 300, seed=7301)
    moon(g, mx, my, mr, col=(236, 234, 220), k=1.0, seed=7302)
    cloud_layer(g, 280, 340, (140, 150, 180), (50, 56, 84), cover=0.3, sx=200, sy=10, seed=7303, alpha=0.5)
    skyline(g, 420, 60, 160, (24, 28, 42), 7304, spires=0.55, lit=(255, 190, 110), lit_p=0.05)
    if "spire" not in d:
        spire(g, 740, 330, 34, 200, (30, 34, 50), seed=7305, crockets=False)
    g.fog(300, 430, (70, 80, 110), 0.0, 0.5)
    # bridge deck and balustrade
    deck = Box(-20, 470, W + 20, 520)
    g.fill(deck, stone((90, 88, 96), 7306, 26, 12))
    g.fill(Box(-20, 520, W + 20, H + 20), vgrad([(520, (40, 40, 48)), (600, (16, 16, 20))]))
    for ax in range(-60, 960, 180):
        g.fill(arch(ax + 20, ax + 160, 560, 640, pointed=False), (8, 8, 12))
    bal = Box(-20, 430, W + 20, 444)
    g.fill(bal, light_y((110, 108, 116), 430, 444, 1.3, 0.7))
    for x in range(-10, 910, 18):
        g.fill(Union([Box(x + 3, 444, x + 11, 470)]), cyl_paint(x + 7, 4, (100, 98, 106), amb=0.4, spec=0.2))
    g.fill(Box(-20, 466, W + 20, 472), (70, 68, 76))
    # lamp posts on the parapet
    for x, key in ((90, "lamp"), (810, None)):
        g.fill(Box(x - 14, 400, x + 14, 470), stone((100, 98, 106), 7307 + x, 10, 8))
        gas_lamp(g, x, 402, 150, lit=not (key and key in d))
    # statue on a pier (centre-left)
    if "statue" not in d:
        statue(g, 330, 432, 120, col=(100, 100, 108), seed=7309, light=-1, arms="sword", plinth=False)
    # banner on the right lamp post
    banner(g, 810, 290, 30, 70, (110, 24, 30) if "banner" not in d else (40, 70, 120), emblem=emblem_moon, seed=7310)
    # the hunter (left) facing the beast (right)
    hunter(g, 230, 516, 230, face=1, weapon="axe", rim_dx=-2.2, scarf=(70, 64, 58) if "scarf" not in d else (130, 30, 36))
    beast(g, 640, 516, 300, face=-1, eyes=(255, 200, 90) if "eyes" not in d else (130, 220, 255), rim_dx=2.2, seed=7311)
    fog_band(g, 470, 520, 580, (80, 90, 120), 0.4, seed=7312)


def l1573_receive(X, Y):
    return moon_receive(*M73, floor=0.3)(X, Y) * smooth(470, 330, Y)


L1573_RAYS = [dict(lx=M73[0], ly=M73[1], col=(170, 186, 232), k=1.3, region=Box(-2, -2, W + 2, 420), threshold=90,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=l1573_receive)]
L1573_ELEMENTS = [
    bat_el("bat1", 200, 80, s=10, speed=28, phase=0.1),
    bat_el("bat2", 230, 100, s=7, speed=28, phase=0.13),
    mist_el("mist", 450, 500, 420, 16, (100, 110, 140), alpha=0.4, length=90, seed=39),
    flame_el("lampR", 810, 260, 1.0, 0.3),
]
L1573_DIFFS = [("spire", 740, 230, 0), ("lamp", 90, 260, 0), ("statue", 330, 380, 0), ("banner", 810, 320, 0), ("scarf", 234, 340, 0),
               ("eyes", 592, 290, 0)]


# =================================================================== Level 1574 moonlit chapel
L74 = (450, -600)
WINS74 = [(150, 70, 230, 330), (410, 40, 490, 300), (670, 70, 750, 330)]


def l1574_window_shape(w):
    x0, y0, x1, y1 = w
    return arch(x0, x1, y0 + (x1 - x0), y1)


def l1574_scene(g, d):
    g.fill(Box(-2, -2, W + 2, 430), tex(vgrad([(0, (40, 40, 48)), (430, (30, 30, 36))]), 0.12, 30, 30, 3, 7401))
    g.fill(Box(-2, -2, W + 2, 430), stone((56, 54, 62), 7402, 30, 14), alpha=0.6)
    # stained glass windows
    for i, w in enumerate(WINS74):
        x0, y0, x1, y1 = w
        sh = l1574_window_shape(w)
        g.fill(Diff(arch(x0 - 10, x1 + 10, y0 + (x1 - x0), y1 + 8), sh), stone((80, 78, 88), 7403 + i, 12, 8))
        rnd = random.Random(7410 + i)
        cols = [(60, 90, 170), (170, 40, 50), (200, 170, 70), (60, 130, 90), (120, 70, 150)]

        def glass(X, Y, rnd_cols=[rnd.choice(cols) for _ in range(64)], x0=x0, i=i):
            ci = (np.floor((X - x0) / 13).astype(np.int64) * 7 + np.floor(Y / 17).astype(np.int64) * 3) % 64
            out = np.array(rnd_cols, np.float32)[ci]
            if i == 0 and "glass" in d:
                out = np.where(((Y > 200) & (Y < 270))[..., None], np.array([230, 200, 90], np.float32), out)
            return out * (0.7 + 0.5 * fbm(X, Y, 6, 6, 2, 7420))[..., None]
        g.fill(sh, glass)
        lead = Union([Box(x, y0, x + 1.2, y1) for x in np.arange(x0, x1, 13)] + [Box(x0, y, x1, y + 1.2) for y in np.arange(y0, y1, 17)])
        g.fill(Inter(lead, sh), (20, 18, 22))
        if i == 1:
            g.fill(Circ(450, 150, 22), (230, 220, 180))
            g.fill(Circ(450, 150, 22) - Circ(450, 150, 19), (20, 18, 22))
    # floor with perspective tiles
    g.fill(Box(-2, 430, W + 2, H + 2), vgrad([(430, (60, 58, 64)), (600, (40, 38, 44))]))
    for i in range(-12, 13):
        g.fill(Seg(450 + i * 12, 430, 450 + i * 90, 610, 0.8), (30, 28, 34))
    for y in (440, 456, 478, 506, 542, 590):
        g.fill(Seg(-2, y, W + 2, y, 0.8), (30, 28, 34))
    # altar with candelabra
    g.fill(Box(330, 340, 570, 350), (160, 150, 140))
    g.fill(Box(340, 350, 560, 430), stone((150, 142, 134), 7430, 20, 10))
    g.fill(Box(380, 360, 520, 420), (110, 20, 30))
    g.fill(Union([Box(380, 360, 520, 366), Box(380, 414, 520, 420), Box(446, 366, 454, 414), Box(420, 386, 480, 392)]), (200, 170, 90))
    for cx, lit in ((370, True), (530, "candle" not in d)):
        g.fill(Union([Seg(cx, 340, cx, 290, 2.4), Seg(cx - 18, 300, cx + 18, 300, 1.6), Box(cx - 10, 334, cx + 10, 340)]), (170, 140, 70))
        for dx in (-18, 0, 18):
            candle(g, cx + dx, 300 if dx else 292, 20, w=6, lit=lit)
    if "chalice" not in d:
        g.fill(Union([Poly([(440, 312), (460, 312), (455, 326), (445, 326)]), Box(448, 326, 452, 336), Box(442, 336, 458, 340)]),
               sphere_paint(446, 316, 14, (210, 176, 90), amb=0.4, spec=0.8))
    # pews in perspective (left and right blocks)
    for row in range(5):
        t = row / 4
        y = 450 + 150 * t ** 1.2
        hgt = 26 + 50 * t
        for side in (-1, 1):
            xa = 450 + side * (60 + 40 * t)
            xb = 450 + side * (220 + 300 * t)
            g.fill(Box(min(xa, xb), y - hgt, max(xa, xb), y - hgt * 0.4), tex(light_y((90, 60, 40), y - hgt, y, 1.2, 0.6), 0.2, 3, 6, 3, 7440 + row))
            g.fill(Box(min(xa, xb), y - hgt * 0.4, max(xa, xb), y), (50, 34, 24))
            if row == 3 and side == 1 and "book" not in d:
                bx = (xa + xb) / 2
                g.fill(Box(bx - 18, y - hgt - 8, bx + 18, y - hgt, 1), (120, 30, 30))
    # flower vase on the left pedestal
    g.fill(Box(250, 360, 290, 430), stone((140, 132, 124), 7450, 12, 8))
    g.fill(Union([Ell(270, 346, 12, 14), Box(264, 330, 276, 340)]), sphere_paint(266, 342, 12, (200, 200, 210), ry=14, amb=0.4, spec=0.5))
    fc = (200, 40, 60) if "flowers" not in d else (240, 240, 230)
    for k, (fx, fy) in enumerate(((256, 314), (270, 306), (284, 314), (264, 322), (278, 322))):
        g.fill(Seg(270, 332, fx, fy, 1), (50, 90, 50))
        g.fill(Circ(fx, fy, 6), sphere_paint(fx - 2, fy - 2, 6, fc, amb=0.4, spec=0.2))
    # hanging censer (right)
    g.fill(Seg(640, 0, 640, 280, 1.2), (110, 90, 50))
    if "censer" not in d:
        g.fill(Union([Ell(640, 296, 14, 12), Poly([(628, 288), (640, 270), (652, 288)])]), sphere_paint(636, 290, 14, (180, 150, 80), ry=14, amb=0.4, spec=0.7))
    g.fog(380, 600, (50, 50, 64), 0.0, 0.25, noise=0.4, seed=7451)


L1574_RAYS = [dict(lx=L74[0], ly=L74[1], col=(200, 190, 240), k=1.8, region=Union([l1574_window_shape(w) for w in WINS74]), threshold=40,
                   soft=60, density=0.92, decay=0.97, samples=70, receive=Box(-20, 100, W + 20, H + 20))]
L1574_ELEMENTS = [
    beam_el("beamL", 190, 200, 260, 560, 60, 160, col=(200, 180, 240), k=0.08),
    beam_el("beamC", 450, 180, 450, 560, 60, 180, col=(200, 200, 250), k=0.09, phase=0.4),
    beam_el("beamR", 710, 200, 640, 560, 60, 160, col=(240, 200, 200), k=0.08, phase=0.7),
    motes_el("dust", [(430, 380), (470, 420), (220, 400), (680, 420)], vx=2, vy=-4, length=24),
    E("smoke", el(lambda g, m: g.glow(640, 280, 10, (200, 200, 210), 0.4)), daynight="untinted",
      anim=dict(driftVelocity=(3, 30), driftLength=60, driftFade=True, driftGrow=1.5)),
] + [flame_el("c%d" % i, x, y, 0.6, i * 0.15) for i, (x, y) in enumerate(((352, 280), (370, 272), (388, 280)))]
L1574_DIFFS = [("glass", 190, 236, 0), ("candle", 530, 280, 0), ("chalice", 450, 326, 0), ("book", 775, 470, 0), ("flowers", 270, 316, 0),
               ("censer", 640, 290, 0)]

LEVELS = [
    ("Level1565", "雾夜长街", make_bg(l1565_scene, L1565_RAYS), L1565_ELEMENTS, L1565_DIFFS, 60, OPTS),
    ("Level1566", "大教堂石阶", make_bg(l1566_scene, L1566_RAYS), L1566_ELEMENTS, L1566_DIFFS, 60, OPTS),
    ("Level1567", "猎人工坊", make_bg(l1567_scene, L1567_RAYS, bloom=(200, 14, 0.35)), L1567_ELEMENTS, L1567_DIFFS, 60, OPTS),
    ("Level1568", "血月屋顶", make_bg(l1568_scene, L1568_RAYS), L1568_ELEMENTS, L1568_DIFFS, 60, OPTS),
    ("Level1569", "禁林提灯", flat_bg(l1569_scene, bloom=(200, 16, 0.4)), L1569_ELEMENTS, L1569_DIFFS, 60, OPTS),
    ("Level1570", "雨中渔村", flat_bg(l1570_scene, bloom=(200, 16, 0.35)), L1570_ELEMENTS, L1570_DIFFS, 60, OPTS),
    ("Level1571", "禁书库", make_bg(l1571_scene, L1571_RAYS, bloom=(200, 14, 0.35)), L1571_ELEMENTS, L1571_DIFFS, 60, OPTS),
    ("Level1572", "地下水道", flat_bg(l1572_scene, bloom=(190, 16, 0.4)), L1572_ELEMENTS, L1572_DIFFS, 60, OPTS),
    ("Level1573", "桥上对峙", make_bg(l1573_scene, L1573_RAYS), L1573_ELEMENTS, L1573_DIFFS, 60, OPTS),
    ("Level1574", "月光礼拜堂", make_bg(l1574_scene, L1574_RAYS, bloom=(200, 14, 0.35)), L1574_ELEMENTS, L1574_DIFFS, 60, OPTS),
]
