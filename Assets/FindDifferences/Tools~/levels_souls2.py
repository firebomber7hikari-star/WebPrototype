# -*- coding: utf-8 -*-
"""Realistic dark-fantasy levels, part 2: a fallen medieval kingdom (inspired by the mood of dark-fantasy
action-RPGs; every knight, creature, emblem and building is an original design; no gore).
  Level1575 余烬神殿   - a ruined arcade at dusk, sun rays through broken arches, a resting knight by a campfire
  Level1576 要塞城门   - a fortress gatehouse: round towers, portcullis, drawbridge over the moat, banners, torches
  Level1577 龙踞城楼   - a dragon perched on a gate tower at the end of a long bridge, fiery sky, embers
  Level1578 黄昏神都   - a golden cathedral city at sunset across an abyss, giant guardian statues on a bridge
  Level1579 熔岩废城   - ruined towers in a lava field: glowing river, chains, fallen pillars, crystals
  Level1580 腐毒沼泽   - a poisonous swamp: stilt walkways, hanging lanterns, giant dead trees, green fog
  Level1581 地下墓窟   - catacombs: coffins in wall niches, candles, a knight's sarcophagus, iron gate
  Level1582 雪原圣堂   - a snowbound cathedral: snowfall, frozen statues, pines, bell tower, lanterns
  Level1583 王座大厅   - an abandoned throne hall: giant pillars, crown left on the throne, banners, light shafts
  Level1584 竞技场决战 - a knight facing a giant armoured warden in a ruined arena at sunset
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import (C, Box, Circ, Diff, Ell, Inter, Moved, Poly, Rough, Seg, Under, Union, cyl_paint, el, fbm, fbm1,
                  grain_tex, lgrad, light_x, light_y, mixc, real_post, rgrad, smooth, sphere_paint, tex, vgrad)
from real_kit import (blades, cloud_layer, crown, glint_el, mist_el, pine, planks, ridge, rock, rock_face, sky, stars,
                      sun, treeline)
from levels_real2 import (arch, ashlar, beam_el, candle, cobweb, dead_tree, flame, flame_el, fog_band, make_bg, merlons,
                          moon, moon_receive, motes_el, rim, stains, twigs)
from levels_real3 import flat_bg
from souls_kit import (FIRE, IRON, MOON, banner, barrel, buttress, cage, campfire, chain, coffin, crate, crow, dragon,
                       ember_el, emblem_moon, emblem_sun, emblem_tree, fire_el, knight, lancet, n1, skyline, spire,
                       statue, stone, torch, wall)
from weather import snow_layer

OPTS = dict(post=real_post, anim_seconds=12.0, frames=60)
SUNSET = (255, 196, 120)
EMBER = (255, 140, 60)


def sun_receive(sx, sy, r, floor=0.2):
    return moon_receive(sx, sy, r, floor=floor)


def round_tower(g, cx, base, w, h, col, seed, light=-1, cap="crenel", roof_col=(60, 50, 56)):
    """Round stone tower (cylinder shading) with crenellations or a conical roof."""
    body = Box(cx - w / 2, base - h, cx + w / 2, base)
    g.fill(body, tex(cyl_paint(cx - light * w * 0.2, w / 2, col, amb=0.3, spec=0.05), 0.0, 1))
    g.fill(body, ashlar(col, 22, 11, seed), alpha=0.55)
    g.fill(body, (0, 0, 0), alpha=lambda X, Y: 0.45 * smooth(-0.2, 1.0, (X - cx) / (w / 2) * -light))
    top = base - h
    if cap == "crenel":
        g.fill(Box(cx - w / 2 - 6, top - 8, cx + w / 2 + 6, top + 2), mixc(col, (0, 0, 0), 0.2))
        g.fill(Union(merlons(cx - w / 2 - 6, cx + w / 2 + 6, top - 8, 14, 12, 8)), mixc(col, (0, 0, 0), 0.15))
    else:
        cone = Poly([(cx - w / 2 - 8, top + 2), (cx, top - w * 1.2), (cx + w / 2 + 8, top + 2)])
        g.fill(cone, tex(light_x(roof_col, cx - w / 2, cx + w / 2, *((1.3, 0.5) if light < 0 else (0.5, 1.3))), 0.2, 3, 3, 3, seed + 1))
    return body


def ruin_arch(g, x0, x1, ys, base, thick, col, seed, broken=False, light=-1):
    """Round arch on two piers; broken=True leaves the right half of the arch missing."""
    w = x1 - x0
    outer = Union([Box(x0 - thick, ys, x0, base), Box(x1, ys, x1 + thick, base),
                   Inter(Ell((x0 + x1) / 2, ys, w / 2 + thick, w / 2 + thick) - Ell((x0 + x1) / 2, ys, w / 2, w / 2), Box(x0 - thick, ys - w, x1 + thick, ys + 1))])
    if broken:
        outer = Diff(outer, Poly([((x0 + x1) / 2 + 6, ys - w), (x1 + thick + 4, ys - w), (x1 + thick + 4, ys + 30), ((x0 + x1) / 2 + 24, ys - w * 0.2)]))
    wall(g, outer, col, seed, x0 - thick, x1 + thick, light, bw=20, bh=11)
    rim(g, outer, -light * 2, 1, col=SUNSET, k=0.25)
    return outer


def brazier(g, x, base, s=1.0, lit=True):
    g.fill(Union([Seg(x - 14 * s, base, x, base - 40 * s, 2.4 * s), Seg(x + 14 * s, base, x, base - 40 * s, 2.4 * s)]), IRON)
    g.fill(Poly([(x - 20 * s, base - 50 * s), (x + 20 * s, base - 50 * s), (x + 12 * s, base - 36 * s), (x - 12 * s, base - 36 * s)]),
           sphere_paint(x - 6 * s, base - 46 * s, 20 * s, (60, 56, 58), ry=8 * s, amb=0.4, spec=0.5))
    if lit:
        g.glow(x, base - 56 * s, 120 * s, FIRE, 0.4)
        g.fill(Rough(Ell(x, base - 52 * s, 16 * s, 4 * s), 1.5, 3, 5), (255, 200, 110))


# =================================================================== Level 1575 ruined shrine at dusk
SUN75 = (470, 318, 26)


def l1575_scene(g, d):
    sx_, sy_, sr = SUN75
    sky(g, [(0, (40, 44, 64)), (200, (150, 110, 100)), (300, (240, 170, 110)), (340, (250, 200, 140))])
    cloud_layer(g, 60, 200, (200, 150, 130), (80, 70, 90), cover=0.45, sx=220, sy=24, seed=7501, alpha=0.8)
    sun(g, sx_, sy_, sr, col=(255, 236, 200), halo=(255, 170, 100), k=0.8)
    ridge(g, 340, 70, 200, 7502, (80, 70, 90), ridged=True, light=False, rock_tex=0.06, haze=((200, 150, 130), 0.6, 0.3))
    g.fill(Box(-2, 400, W + 2, H + 2), tex(vgrad([(400, (90, 80, 70)), (600, (46, 40, 36))]), 0.35, 5, 3, 4, 7503))
    # ruined arcade across the middle
    col = (120, 110, 104)
    for i, x0 in enumerate((60, 260, 460, 660)):
        broken = (i == 2 and "arch" in d) or i == 3
        ruin_arch(g, x0 + 24, x0 + 176, 220, 420, 24, col, 7504 + i, broken=broken, light=1)
    g.fill(Box(-2, 410, W + 2, 430), light_y((110, 100, 94), 410, 430, 1.2, 0.7))
    # ivy on the arcade
    for x in (90, 330, 560):
        g.fill(Rough(Ell(x, 260, 22, 60), 6, 8, 7510 + x), tex((50, 70, 40), 0.4, 3, 3, 3, 7511))
    # tattered banner hanging in an arch
    banner(g, 650, 196, 40, 120, (120, 24, 30) if "banner" not in d else (40, 70, 120), emblem=emblem_tree, seed=7512)
    # bird on the broken pier top
    if "bird" not in d:
        crow(g, 846, 220, 1.2, face=-1)
    # rubble, a broken statue head, flowers
    for x, y, rx in ((120, 470, 30), (760, 480, 40), (320, 560, 22), (860, 570, 36)):
        rock(g, x, y, rx, rx * 0.6, col=(110, 100, 94), seed=7513 + x)
    hx, hy = 760, 470
    g.fill(Ell(hx, hy - 10, 34, 30), sphere_paint(hx - 10, hy - 18, 34, (130, 122, 116), ry=30, amb=0.35, spec=0.1))
    g.fill(Ell(hx - 10, hy - 14, 5, 3), (60, 54, 52))
    g.fill(Ell(hx + 12, hy - 14, 5, 3), (60, 54, 52))
    g.fill(Seg(hx - 4, hy - 4, hx + 8, hy - 2, 1.6), (70, 62, 60))
    if "flowers" not in d:
        for k, (fx, fy) in enumerate(((80, 540), (100, 530), (118, 544), (92, 552))):
            g.fill(Seg(fx, fy + 18, fx, fy, 1.2), (50, 90, 50))
            g.fill(Circ(fx, fy, 5), sphere_paint(fx - 1, fy - 1, 5, (230, 220, 200), amb=0.4, spec=0.2))
    blades(g, 430, 600, (80, 90, 60), n=220, seed=7514, hmax=18)
    # campfire in the foreground centre and a resting knight
    campfire(g, 470, 540, 1.1)
    knight(g, 280, 560, 230, steel=(110, 112, 118), cloth=(70, 60, 50), face=1, sword="down",
           shield=((150, 30, 30) if "shield" not in d else (40, 80, 140), emblem_sun), rim_dx=2.0, rim_col=FIRE, rim_k=0.45)
    if "pot" not in d:
        g.fill(Union([Ell(580, 540, 22, 18), Box(570, 518, 590, 526)]), sphere_paint(574, 534, 22, (110, 70, 50), ry=18, amb=0.35, spec=0.2))
    g.fog(330, 420, (200, 160, 140), 0.3, 0.0)


L1575_RAYS = [dict(lx=SUN75[0], ly=SUN75[1], col=(255, 200, 140), k=0.7, region=Box(-2, -2, W + 2, 400), threshold=170,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=sun_receive(*SUN75, floor=0.3))]
L1575_ELEMENTS = [
    fire_el("fireA", 462, 534, 1.4, 0.0), fire_el("fireB", 478, 536, 1.1, 0.5),
    ember_el("emb1", 470, 500, n=6, rise=120, seed=1), ember_el("emb2", 470, 500, n=5, rise=110, phase=0.5, seed=2),
    E("smoke", el(lambda g, m: g.glow(470, 470, 16, (120, 110, 110), 0.25)), anim=dict(driftVelocity=(6, 40), driftLength=120, driftFade=True, driftGrow=2.0)),
    mist_el("mist", 450, 420, 360, 14, (210, 170, 150), alpha=0.35, length=80, seed=40),
]
L1575_DIFFS = [("arch", 560, 160, 0), ("banner", 650, 250, 0), ("bird", 846, 200, 0), ("flowers", 98, 540, 0), ("shield", 230, 400, 0),
               ("pot", 580, 532, 0)]


# =================================================================== Level 1576 fortress gate
def l1576_scene(g, d):
    sky(g, [(0, (40, 46, 60)), (250, (120, 110, 110)), (330, (170, 140, 120))])
    cloud_layer(g, 0, 240, (150, 140, 140), (60, 60, 70), cover=0.6, sx=220, sy=30, seed=7601, alpha=0.9)
    ridge(g, 320, 100, 240, 7602, (70, 74, 86), ridged=True, light=False, haze=((150, 140, 140), 0.5, 0.2), snow=(260, (200, 200, 210)))
    # moat
    g.fill(Box(-2, 470, W + 2, H + 2), vgrad([(470, (40, 50, 50)), (600, (20, 28, 28))]))
    for y in range(480, 600, 10):
        g.add(Seg(0, y, W, y, 0.6), (150, 150, 150), 0.05)
    # curtain wall + gatehouse
    col = (110, 106, 104)
    g.fill(Box(-20, 250, W + 20, 470), stone(col, 7603, 26, 12))
    g.fill(Box(-20, 250, W + 20, 470), (0, 0, 0), alpha=0.25)
    g.fill(Union(merlons(-20, W + 20, 250, 16, 18, 10)), mixc(col, (0, 0, 0), 0.25))
    stains(g, Box(-20, 250, W + 20, 470), 0.25, seed=7604)
    for cx, side in ((280, -1), (620, 1)):
        round_tower(g, cx, 470, 130, 300, col, 7605 + cx, light=-1, cap="cone", roof_col=(60, 50, 60))
        for yy in (230, 330):
            lit = (cx == 620 and yy == 330 and "slit" not in d)
            g.fill(Box(cx - 4, yy, cx + 4, yy + 30, 1), (255, 190, 110) if lit else (20, 18, 22))
            if lit:
                g.glow(cx, yy + 15, 30, FIRE, 0.3)
    # banners hanging from the towers
    banner(g, 280, 196, 46, 110, (120, 24, 30) if "banner" not in d else (40, 80, 50), emblem=emblem_sun, seed=7606)
    banner(g, 620, 196, 46, 110, (120, 24, 30), emblem=emblem_sun, seed=7607)
    # gate arch + portcullis
    gate = arch(390, 510, 340, 470, pointed=True)
    g.fill(Diff(arch(374, 526, 340, 470), gate), stone((130, 124, 120), 7608, 14, 10))
    g.fill(gate, (14, 12, 14))
    g.glow(450, 440, 60, FIRE, 0.2)
    bars = [Box(x, 300, x + 4, 420) for x in range(396, 508, 14 if "bars" not in d else 22)] + [Box(390, y, 510, y + 4) for y in (320, 350, 380, 410)]
    g.fill(Inter(Union(bars), gate), (40, 38, 40))
    for y in (420,):
        g.fill(Union([Poly([(x, y), (x + 4, y), (x + 2, y + 10)]) for x in range(396, 508, 14 if "bars" not in d else 22)]), (40, 38, 40))
    # shield on the wall above the gate
    if "crest" not in d:
        sh = Union([Box(430, 262, 470, 288), Inter(Circ(430, 288, 40), Circ(470, 288, 40)) & Box(430, 288, 470, 320)])
        g.fill(sh, light_x((40, 70, 130), 430, 470, 1.3, 0.7))
        emblem_tree(g, 450, 288, 16)
    # drawbridge
    db = Poly([(390, 470), (510, 470), (560, 600), (340, 600)])
    g.fill(db, planks("v", (100, 74, 50), seed=7609, width=16))
    for sgn in (-1, 1):
        chain(g, 450 + sgn * 70, 400, 450 + sgn * 105, 600, sag=-6)
    # torches beside the gate
    torch(g, 360, 380, lit=True)
    torch(g, 540, 380, lit=True)
    # pennant on the right tower roof
    g.fill(Seg(780, 236, 780, 170, 1.8), IRON)
    if "pennant" not in d:
        g.fill(Poly([(781, 172), (836, 182), (781, 198)]), light_x((150, 30, 30), 781, 836, 1.2, 0.7))
    # crow on the chain post
    g.fill(Box(330, 560, 346, 600), (60, 50, 42))
    if "crow" not in d:
        crow(g, 338, 560, 1.2, face=1)
    g.fog(300, 470, (150, 140, 140), 0.0, 0.25, noise=0.5, seed=7610)


L1576_ELEMENTS = [
    fire_el("tL", 360, 382, 1.0, 0.1),
    fire_el("tR", 540, 382, 1.0, 0.4),
    glint_el("slit", [(280, 345)], col=(255, 200, 120), r=5, speed=0.3),
    mist_el("mist", 450, 480, 400, 14, (130, 130, 130), alpha=0.35, length=80, seed=41),
]
L1576_DIFFS = [("banner", 280, 250, 0), ("slit", 620, 345, 0), ("bars", 450, 380, 0), ("crest", 450, 290, 0), ("pennant", 806, 184, 0),
               ("crow", 338, 540, 0)]


# =================================================================== Level 1577 dragon on the gate tower
def l1577_scene(g, d):
    sky(g, [(0, (40, 10, 14)), (200, (130, 40, 26)), (380, (240, 130, 60)), (420, (250, 170, 90))])
    cloud_layer(g, 40, 260, (200, 90, 60), (60, 20, 24), cover=0.55, sx=200, sy=24, seed=7701, alpha=0.85)
    ridge(g, 400, 120, 220, 7702, (50, 24, 26), ridged=True, light=False, rock_tex=0.06, haze=((200, 90, 60), 0.4, 0.2))
    g.glow(450, 420, 520, (255, 120, 50), 0.35)
    # chasm below the bridge
    g.fill(Box(-2, 440, W + 2, H + 2), vgrad([(440, (60, 26, 22)), (600, (14, 8, 10))]))
    # long bridge to the gate tower
    col = (96, 80, 76)
    g.fill(Box(-20, 420, 680, 452), stone(col, 7703, 24, 12))
    for ax in range(-60, 680, 150):
        g.fill(arch(ax + 20, ax + 130, 490, 600, pointed=False), (12, 8, 10), alpha=0.85)
    g.fill(Box(-20, 452, 680, 520), stone(mixc(col, (0, 0, 0), 0.4), 7704, 24, 12))
    par = [Box(x, 396, x + 18, 422) for x in range(-20, 680, 30) if not ("gap" in d and 500 <= x <= 560)]
    g.fill(Union(par), light_y(col, 396, 422, 1.3, 0.7))
    rim(g, Union(par), 0, 1.5, col=EMBER, k=0.3)
    # gate tower on the right
    tw = Box(650, 150, 830, 452)
    wall(g, tw, (90, 76, 74), 7705, 650, 830, light=-1)
    g.fill(Union(merlons(640, 840, 150, 18, 20, 12)), (80, 66, 64))
    g.fill(arch(706, 774, 360, 452, pointed=True), (16, 10, 12))
    for wy in (230,):
        lit = "window" not in d
        g.fill(arch(726, 754, wy, wy + 50), (255, 170, 90) if lit else (20, 14, 16))
        if lit:
            g.glow(740, wy + 20, 50, FIRE, 0.35)
    banner(g, 740, 300, 44, 60, (40, 40, 60) if "banner" not in d else (130, 30, 30), emblem=emblem_moon, seed=7706, pole=False)
    # the dragon perched on the battlements, rim-lit by the fire sky
    dragon(g, 740, 100, 0.72, col=(30, 22, 24), face=-1, rim_dx=2.0, rim_col=(255, 150, 80), rim_k=0.5, wings_up=True, seed=7707)
    g.glow(640, 62, 12, (255, 200, 90), 0.9)
    # braziers on the bridge
    brazier(g, 120, 420, 1.0, lit=True)
    brazier(g, 420, 420, 1.0, lit="brazier" not in d)
    # a lone knight on the bridge
    knight(g, 270, 424, 120, steel=(100, 98, 104), cloth=(60, 50, 50), face=1, sword="down",
           shield=((150, 30, 30) if "shield" not in d else (60, 90, 140), None), rim_dx=-1.6, rim_col=EMBER, rim_k=0.5)
    g.fog(380, 470, (200, 100, 60), 0.0, 0.3, noise=0.5, seed=7708)


L1577_ELEMENTS = [
    fire_el("brz1", 120, 370, 1.1, 0.1),
    ember_el("emb1", 300, 420, spread=200, n=8, rise=160, wind=14, seed=3),
    ember_el("emb2", 600, 440, spread=200, n=8, rise=150, wind=10, phase=0.5, seed=4),
    E("breath", el(lambda g, m: g.glow(626, 66, 18, (255, 160, 80), 0.6)), daynight="untinted",
      anim=dict(driftVelocity=(-30, 10), driftLength=60, driftFade=True, driftGrow=2.0)),
]
L1577_DIFFS = [("window", 740, 250, 0), ("banner", 740, 330, 0), ("gap", 530, 410, 0), ("brazier", 420, 368, 0), ("shield", 248, 360, 0)]


# =================================================================== Level 1578 golden capital at sunset
SUN78 = (450, 300, 34)


def l1578_scene(g, d):
    sx_, sy_, sr = SUN78
    sky(g, [(0, (60, 70, 110)), (180, (200, 150, 120)), (300, (255, 200, 130)), (360, (255, 220, 160))])
    cloud_layer(g, 80, 200, (255, 200, 150), (150, 110, 110), cover=0.4, sx=240, sy=18, seed=7801, alpha=0.7)
    sun(g, sx_, sy_, sr, col=(255, 244, 210), halo=(255, 190, 110), k=0.9)
    gold = (150, 110, 70)
    skyline(g, 380, 60, 200, gold, 7802, x0=40, x1=860, spires=0.6, lit=(255, 230, 160), lit_p=0.05)
    # the great domed cathedral in the middle
    g.fill(Box(380, 220, 520, 380), stone((170, 130, 84), 7803, 16, 9))
    g.fill(Inter(Ell(450, 220, 66, 70), Box(380, 140, 520, 222)), sphere_paint(430, 190, 70, (220, 170, 80), ry=70, amb=0.4, spec=0.6))
    g.fill(Box(444, 120, 456, 152), (200, 160, 80))
    if "finial" not in d:
        g.fill(Union([Seg(450, 122, 450, 70, 3.4), Circ(450, 66, 8), Seg(438, 92, 462, 92, 3)]), sphere_paint(446, 70, 14, (240, 200, 110), ry=30, amb=0.5, spec=0.6))
    for x in (400, 450, 500):
        lancet(g, x - 8, x + 8, 290, 340, lit=(255, 220, 150))
    if "spire" not in d:
        spire(g, 700, 380, 36, 260, (150, 112, 74), seed=7804, light=-1)
    g.fog(300, 400, (230, 180, 140), 0.0, 0.5)
    # abyss and the bridge rising towards the city
    g.fill(Box(-2, 380, W + 2, H + 2), vgrad([(380, (120, 90, 80)), (600, (30, 24, 26))]))
    br = Poly([(260, 610), (640, 610), (480, 380), (420, 380)])
    g.fill(br, tex(light_y((170, 140, 110), 380, 600, 0.9, 1.2), 0.2, 6, 4, 3, 7805))
    for sgn in (-1, 1):
        g.fill(Poly([(450 + sgn * 30, 380), (450 + sgn * 34, 380), (450 + sgn * 200, 610), (450 + sgn * 190, 610)]), (120, 96, 80))
    # lamps along the bridge
    for t_, key in ((0.3, None), (0.65, "lamp")):
        y = 380 + 230 * t_
        for sgn in (-1, 1):
            x = 450 + sgn * (32 + 160 * t_)
            hgt = 30 + 90 * t_
            g.fill(Seg(x, y, x, y - hgt, 1 + 2 * t_), (60, 50, 44))
            lit = not (key and key in d and sgn == -1)
            if lit:
                g.glow(x, y - hgt, 30 * (0.5 + t_), FIRE, 0.5)
            g.fill(Circ(x, y - hgt, 3 + 5 * t_), (255, 210, 130) if lit else (60, 50, 44))
    # giant guardian statues (stone knights) on both sides
    stone_c = (150, 136, 120)
    knight(g, 120, 600, 480, steel=stone_c, cloth=(130, 120, 106), face=1, sword="down",
           shield=((140, 126, 110), emblem_sun if "emblem" not in d else emblem_tree), rim_dx=2.0, rim_col=SUNSET, rim_k=0.4)
    knight(g, 780, 600, 480, steel=stone_c, cloth=(130, 120, 106), face=-1, sword="down", helm="bascinet",
           plume=None if "plume" in d else (120, 40, 40), rim_dx=-2.0, rim_col=SUNSET, rim_k=0.4)
    g.fill(Box(-20, 590, W + 20, H + 20), (40, 34, 32))


L1578_RAYS = [dict(lx=SUN78[0], ly=SUN78[1], col=(255, 210, 150), k=0.6, region=Box(-2, -2, W + 2, 380), threshold=190,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=sun_receive(*SUN78, floor=0.3))]
L1578_ELEMENTS = [
    E("birds", el(lambda g, m: [g.fill(Union([Seg(x - 7, y - 3, x, y, 1.6), Seg(x, y, x + 7, y - 3, 1.6)]), (60, 40, 40))
                                for x, y in ((240, 120), (262, 110), (280, 126), (300, 114))]),
      anim=dict(bobAmplitude=(30, 6), bobSpeed=0.08)),
    mist_el("mist", 450, 400, 420, 14, (240, 200, 160), alpha=0.4, length=80, seed=42),
]
L1578_DIFFS = [("finial", 450, 84, 0), ("spire", 700, 220, 0), ("lamp", 312, 450, 0), ("emblem", 70, 330, 0), ("plume", 830, 160, 0)]


# =================================================================== Level 1579 lava ruins
def l1579_scene(g, d):
    sky(g, [(0, (14, 8, 10)), (220, (60, 20, 16)), (330, (140, 50, 24))])
    cloud_layer(g, 0, 260, (110, 50, 34), (30, 14, 14), cover=0.7, sx=200, sy=30, seed=7901, alpha=0.9)
    ridge(g, 330, 140, 260, 7902, (40, 20, 18), ridged=True, light=False, rock_tex=0.1)
    # glowing cracks on the far slopes
    g.add(Under(lambda x: 330 - 40 * np.exp(-((x - 520) / 40.0) ** 2), 440, 600, 335), (255, 120, 40), 0.35, feather=6)
    g.fill(Box(-2, 330, W + 2, H + 2), tex(vgrad([(330, (40, 26, 22)), (600, (20, 14, 12))]), 0.4, 6, 3, 4, 7903))
    # lava river winding to the front
    def river_x(y):
        return 450 + 120 * np.sin((y - 330) / 70.0)
    river = Poly([(river_x(y) - (10 + (y - 330) * 0.35), y) for y in range(330, 620, 10)] +
                 [(river_x(y) + (10 + (y - 330) * 0.35), y) for y in range(610, 320, -10)])

    def lava(X, Y):
        n = fbm(X, Y, 14, 6, 4, 7904)
        crust = smooth(0.55, 0.7, n)
        hot = C((255, 200, 90)) * (1 - crust)[..., None] + C((120, 30, 14)) * crust[..., None]
        return hot
    g.fill(river, lava, feather=2)
    g.add(river, (255, 120, 40), 0.25, feather=24)
    # ruined towers on either side
    col = (70, 54, 50)
    for cx, h, seed in ((160, 300, 7905), (740, 340, 7906)):
        body = round_tower(g, cx, 470, 120, h, col, seed, light=1, cap="crenel")
        g.add(body, (255, 110, 40), 0.12, alpha=lambda X, Y: smooth(330, 470, Y))
    for wy, key in ((300, "window"), (380, None)):
        lit = not (key and key in d)
        g.fill(arch(728, 752, wy, wy + 40), (255, 150, 60) if lit else (20, 12, 12))
        if lit:
            g.glow(740, wy + 18, 40, FIRE, 0.4)
    # chains slung between the towers
    chain(g, 210, 230, 690, 200, col=(60, 50, 50), sag=70, link=7)
    chain(g, 210, 290, 690, 270, col=(60, 50, 50), sag=60, link=7)
    if "cage" not in d:
        cage(g, 450, 300, 44, 70, col=(40, 30, 30), chain_len=4)
    # lava fall from the right tower base
    if "fall" not in d:
        fall = Poly([(820, 470), (850, 470), (856, 600), (812, 600)])
        g.fill(fall, lava, feather=2)
        g.add(fall, (255, 120, 40), 0.3, feather=20)
    # fallen pillar in the foreground
    if "pillar" not in d:
        g.fill(Seg(40, 560, 260, 520, 24), tex(light_y((90, 80, 76), 500, 584, 1.3, 0.55), 0.2, 3, 3, 3, 7907))
        for k in range(1, 6):
            g.mul(Seg(40 + k * 36, 560 - k * 6.5 - 22, 40 + k * 36, 560 - k * 6.5 + 22, 1.2), 0.4)
    # obsidian crystals (right foreground)
    cc = (60, 40, 70) if "crystal" not in d else (40, 90, 120)
    for k, (x, h, a) in enumerate(((640, 90, -0.2), (670, 120, 0.05), (700, 70, 0.3), (618, 60, -0.45))):
        tip = (x + math.sin(a) * h, 590 - math.cos(a) * h)
        g.fill(Poly([(x - 14, 590), tip, (x + 14, 590)]), lgrad(x - 14, 0, x + 14, 0, [(0, mixc(cc, (255, 255, 255), 0.35)), (1, mixc(cc, (0, 0, 0), 0.4))]))
        g.add(Seg(x - 4, 588, tip[0] - 2, tip[1] + 6, 1.2), (255, 140, 80), 0.4)
    for x, y, r in ((330, 470, 30), (560, 520, 40), (120, 440, 26)):
        rock(g, x, y, r, r * 0.6, col=(50, 38, 34), seed=7908 + x)
    g.fog(300, 400, (120, 50, 30), 0.0, 0.35, noise=0.5, seed=7909)


L1579_ELEMENTS = [
    ember_el("emb1", 450, 560, spread=120, n=8, rise=180, wind=6, seed=5),
    ember_el("emb2", 520, 480, spread=100, n=6, rise=160, wind=-6, phase=0.5, seed=6),
    E("smoke1", el(lambda g, m: g.glow(500, 300, 60, (40, 24, 22), 0.5)), anim=dict(driftVelocity=(10, 40), driftLength=120, driftFade=True, driftGrow=1.5)),
    glint_el("bubbles", [(470, 470), (400, 560), (520, 400)], col=(255, 230, 150), r=6, speed=0.5),
]
L1579_DIFFS = [("window", 740, 318, 0), ("cage", 450, 336, 0), ("fall", 834, 540, 0), ("pillar", 150, 540, 0), ("crystal", 660, 540, 0)]


# =================================================================== Level 1580 poison swamp
def l1580_scene(g, d):
    sky(g, [(0, (24, 34, 26)), (300, (70, 90, 60)), (360, (90, 110, 70))])
    g.glow(500, 280, 500, (150, 180, 100), 0.2)
    treeline(g, 340, 70, 16, 8001, (36, 50, 34), light=0.0, haze=((90, 110, 70), 0.6, 0.2), conifer=False)
    # murky water
    g.fill(Box(-2, 340, W + 2, H + 2), vgrad([(340, (60, 80, 50)), (600, (24, 34, 22))]))
    g.fill(Box(-2, 340, W + 2, H + 2), (120, 160, 60), alpha=lambda X, Y: 0.25 * fbm(X, Y, 60, 10, 3, 8002))
    # giant dead trees
    for x, base, h, s, lean in ((80, 600, 560, 8003, 0.08), (620, 360, 300, 8004, -0.06), (860, 500, 480, 8005, -0.1)):
        dead_tree(g, x, base, h, seed=s, col=(30, 32, 26), lean=lean, w=h * 0.05, depth=5)
    # walkway on stilts from the left foreground to the hut
    pts = [(120, 560), (300, 500), (480, 440), (640, 400)]
    for i in range(3):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        n = 7
        for k in range(n):
            if "plank" in d and i == 1 and k == 3:
                continue
            t0 = k / n
            px, py = x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0
            w = 30 - i * 6
            g.fill(Poly([(px - 4, py - w * 0.4), (px + 18, py - w * 0.4 - 4), (px + 22, py + w * 0.4 - 4), (px, py + w * 0.4)]),
                   tex(light_x((100, 84, 60), px - 4, px + 22, 1.2, 0.7), 0.2, 1, 4, 3, 8006 + i * 10 + k))
        for k in range(3):
            px, py = x0 + (x1 - x0) * k / 3, y0 + (y1 - y0) * k / 3
            g.fill(Seg(px, py, px + 2, py + 50 - i * 10, 3 - i * 0.6), (50, 40, 30))
    # stilt hut
    hx = 640
    g.fill(Union([Seg(hx + 10, 400, hx + 12, 450, 3), Seg(hx + 110, 400, hx + 112, 450, 3)]), (50, 40, 30))
    g.fill(Box(hx, 320, hx + 120, 400), planks("v", (80, 70, 54), seed=8010, width=12))
    g.fill(Poly([(hx - 14, 324), (hx + 60, 270), (hx + 134, 324)]), tex(light_y((90, 84, 50), 270, 324, 1.2, 0.7), 0.4, 3, 2, 3, 8011))
    lit = "hut" not in d
    g.fill(Box(hx + 70, 340, hx + 96, 364), (200, 230, 120) if lit else (20, 26, 20))
    if lit:
        g.glow(hx + 83, 352, 50, (180, 230, 100), 0.35)
    # lantern posts
    for x, y, key in ((200, 520, "lamp"), (420, 450, None)):
        hgt = 140 if x == 200 else 100
        g.fill(Seg(x, y, x, y - hgt, 3), (50, 40, 30))
        g.fill(Seg(x, y - hgt, x + 24, y - hgt, 2), (50, 40, 30))
        ok = not (key and key in d)
        lx, ly = x + 22, y - hgt + 10
        if ok:
            g.glow(lx, ly + 10, 70, (190, 240, 120), 0.45)
        g.fill(Box(lx - 8, ly, lx + 8, ly + 20, 2), (220, 250, 160) if ok else (40, 46, 36))
        g.fill(Poly([(lx - 10, ly), (lx, ly - 8), (lx + 10, ly)]), IRON)
    # warning sign
    g.fill(Seg(560, 470, 560, 400, 3), (60, 48, 34))
    if "sign" not in d:
        g.fill(Box(530, 396, 590, 428, 2), tex(light_x((110, 90, 60), 530, 590, 1.2, 0.7), 0.2, 1.5, 4))
        g.fill(Union([Seg(546, 404, 574, 420, 2.4), Seg(546, 420, 574, 404, 2.4)]), (60, 20, 20))
    # mushrooms on a log (left foreground)
    g.fill(Seg(20, 560, 160, 580, 16), tex(light_y((70, 56, 40), 548, 592, 1.3, 0.55), 0.3, 3, 3, 3, 8012))
    mc = (150, 200, 80) if "mush" not in d else (200, 90, 160)
    for k, (mx, s) in enumerate(((60, 1.2), (84, 0.9), (110, 1.0))):
        g.fill(Box(mx - 2 * s, 548 - 14 * s, mx + 2 * s, 552), (200, 200, 170))
        g.fill(Inter(Ell(mx, 548 - 14 * s, 12 * s, 9 * s), Box(mx - 13 * s, 536 - 14 * s, mx + 13 * s, 548 - 14 * s)), sphere_paint(mx - 3 * s, 544 - 18 * s, 12 * s, mc, amb=0.5, spec=0.3))
        g.glow(mx, 540 - 14 * s, 20 * s, mc, 0.2)
    # basket on the walkway
    if "basket" not in d:
        g.fill(Union([Ell(330, 486, 20, 14), Box(310, 470, 350, 486)]), tex(light_x((150, 120, 70), 310, 350, 1.2, 0.7), 0.3, 1.5, 1.5))
    g.fog(330, 420, (120, 150, 90), 0.0, 0.45, noise=0.5, seed=8013)
    g.fog(500, 610, (90, 120, 70), 0.0, 0.3, noise=0.6, seed=8014)


L1580_ELEMENTS = [
    mist_el("mist1", 450, 400, 400, 22, (140, 180, 100), alpha=0.45, length=90, seed=43),
    mist_el("mist2", 300, 560, 300, 18, (120, 160, 90), alpha=0.35, length=90, seed=44),
    glint_el("bubbles", [(300, 420), (520, 520), (760, 470), (180, 380)], col=(200, 240, 140), r=4, speed=0.4),
    glint_el("flies", [(640, 230), (300, 300)], col=(220, 255, 160), r=3, speed=0.7),
]
L1580_DIFFS = [("plank", 400, 466, 0), ("hut", 723, 352, 0), ("lamp", 222, 400, 0), ("sign", 560, 412, 0), ("mush", 84, 524, 0),
               ("basket", 330, 478, 0)]


# =================================================================== Level 1581 catacombs
def l1581_scene(g, d):
    g.fill(Box(-2, -2, W + 2, 470), stone((70, 64, 60), 8101, 28, 13))
    g.fill(Box(-2, -2, W + 2, 470), (0, 0, 0), alpha=lambda X, Y: 0.35 + 0.3 * smooth(0, 470, np.abs(Y - 300)))
    # vaulted ceiling ribs
    for x in (150, 450, 750):
        g.fill(Inter(Ell(x, 60, 170, 120) - Ell(x, 60, 156, 108), Box(x - 180, -60, x + 180, 60)), (90, 84, 78))
    # wall niches with coffins (two rows)
    for row, y0 in enumerate((110, 250)):
        for i, x0 in enumerate((40, 220, 580, 760)):
            niche = arch(x0, x0 + 110, y0 + 30, y0 + 110, pointed=False)
            g.fill(Diff(arch(x0 - 8, x0 + 118, y0 + 30, y0 + 116, pointed=False), niche), stone((96, 90, 84), 8102 + row * 4 + i, 12, 8))
            g.fill(niche, (18, 16, 16))
            cy = y0 + 110
            box_ = Box(x0 + 6, cy - 34, x0 + 104, cy - 2, 2)
            g.fill(box_, tex(light_y((80, 60, 44), cy - 34, cy, 1.3, 0.6), 0.2, 8, 2, 3, 8110 + row * 4 + i))
            if row == 0 and i == 1 and "lid" in d:
                g.fill(Poly([(x0 + 4, cy - 34), (x0 + 106, cy - 50), (x0 + 108, cy - 42), (x0 + 6, cy - 28)]), tex((96, 72, 52), 0.2, 8, 2))
            else:
                g.fill(Box(x0 + 2, cy - 38, x0 + 108, cy - 32, 2), (96, 72, 52))
    # central arch to a dark corridor with a gate
    g.fill(arch(380, 520, 230, 470, pointed=True), (10, 9, 10))
    g.fill(Diff(arch(366, 534, 230, 470), arch(380, 520, 230, 470)), stone((100, 94, 88), 8120, 12, 8))
    gate = Union([Box(x, 200, x + 3, 470) for x in range(388, 516, 12)] + [Box(380, 300, 520, 304), Box(380, 400, 520, 404)])
    g.fill(Inter(gate, arch(380, 520, 230, 470)), (40, 38, 40))
    if "chain" not in d:
        chain(g, 400, 350, 500, 350, col=(110, 104, 100), sag=14, link=6)
        g.fill(Box(442, 356, 458, 376, 3), (100, 90, 70))
    # plaque above the arch
    if "plaque" not in d:
        g.fill(Box(410, 120, 490, 160, 3), sphere_paint(440, 130, 60, (130, 110, 70), ry=30, amb=0.4, spec=0.5))
        g.fill(Union([Box(422, 130 + k * 9, 478, 132 + k * 9) for k in range(3)]), (70, 56, 36))
    # floor
    g.fill(Box(-2, 470, W + 2, H + 2), tex(vgrad([(470, (60, 54, 50)), (600, (34, 30, 28))]), 0.3, 8, 4, 3, 8121))
    # knight's sarcophagus with an effigy (foreground)
    g.mul(Ell(450, 590, 260, 16), 0.5, feather=10)
    g.fill(Box(210, 500, 690, 590, 3), stone((120, 114, 108), 8122, 30, 14))
    g.fill(Box(200, 490, 700, 504, 3), light_y((140, 134, 128), 490, 504, 1.3, 0.7))
    eff = (150, 144, 136)
    g.fill(Union([Ell(450, 474, 170, 18), Ell(280, 472, 16, 14)]), sphere_paint(400, 466, 180, eff, ry=20, amb=0.4, spec=0.1))
    g.fill(Union([Ell(620, 470, 10, 16), Ell(600, 470, 10, 16)]), eff)
    if "sword" not in d:
        g.fill(Seg(320, 466, 580, 466, 3, 2), (170, 166, 160))
        g.fill(Seg(330, 456, 330, 476, 3), (170, 166, 160))
    # urns and candles
    if "urn" not in d:
        g.fill(Union([Ell(760, 440, 20, 24), Box(750, 410, 770, 420)]), sphere_paint(752, 432, 20, (110, 80, 60), ry=24, amb=0.35, spec=0.3))
    g.fill(Ell(140, 460, 18, 22), sphere_paint(134, 452, 18, (90, 86, 84), ry=22, amb=0.35, spec=0.3))
    for x, y, key in ((60, 230, None), (870, 230, None), (300, 360, "candle"), (690, 360, None)):
        lit = not (key and key in d)
        candle(g, x, y, 24, w=8, lit=lit)
        if lit and key:
            flame(g, x, y - 24, 1.0)
    g.fog(380, 600, (60, 56, 60), 0.0, 0.25, noise=0.4, seed=8123)
    cobweb(g, 0, 0, 80, (1, 1))
    cobweb(g, 900, 0, 70, (-1, 1))


L1581_ELEMENTS = [
    flame_el("c1", 60, 206, 1.0, 0.1), flame_el("c2", 870, 206, 1.0, 0.3), flame_el("c4", 690, 336, 1.0, 0.6),
    motes_el("dust", [(300, 300), (600, 280), (450, 420)], vx=2, vy=-3, length=20),
    mist_el("mist", 450, 520, 300, 14, (80, 76, 80), alpha=0.3, length=60, seed=45),
]
L1581_DIFFS = [("lid", 275, 196, 0), ("chain", 450, 360, 0), ("plaque", 450, 140, 0), ("sword", 450, 466, 0), ("urn", 760, 430, 0),
               ("candle", 300, 330, 0)]


# =================================================================== Level 1582 snowbound cathedral
M82 = (160, 90, 30)
WARMW = (255, 200, 130)


def l1582_scene(g, d):
    mx, my, mr = M82
    sky(g, [(0, (20, 30, 54)), (260, (80, 100, 140)), (360, (130, 146, 176))])
    stars(g, 70, 240, seed=8201)
    moon(g, mx, my, mr, k=0.8, seed=8202)
    ridge(g, 340, 90, 220, 8203, (120, 130, 160), ridged=True, light=False, snow=(300, (220, 226, 240)), haze=((130, 146, 176), 0.5, 0.2))
    treeline(g, 370, 50, 12, 8204, (40, 56, 66), light=0.0, haze=((130, 146, 176), 0.4, 0.1))
    # cathedral (right of centre)
    col = (120, 122, 134)
    front = Union([Box(420, 200, 760, 450), Poly([(420, 202), (590, 110), (760, 202)])])
    wall(g, front, col, 8205, 420, 760, light=-1)
    g.fill(Poly([(410, 204), (590, 104), (770, 204), (760, 210), (590, 116), (420, 210)]), (236, 240, 248))
    for x0 in (450, 690):
        lancet(g, x0, x0 + 40, 280, 380, lit=WARMW if not (x0 == 450 and "window" in d) else None)
    g.fill(arch(550, 630, 340, 450), (20, 18, 24))
    g.glow(590, 420, 60, FIRE, 0.25)
    g.fill(Circ(590, 230, 34), (255, 200, 130))
    g.fill(Union([Circ(590, 230, 34) - Circ(590, 230, 31)] + [Seg(590, 230, 590 + 34 * math.cos(a), 230 + 34 * math.sin(a), 1.4) for a in np.linspace(0, math.tau, 9)[:-1]]), (40, 36, 40))
    # bell tower with a bell
    tw = Box(780, 120, 880, 450)
    wall(g, tw, col, 8206, 780, 880, light=-1)
    g.fill(arch(806, 854, 170, 240), (14, 14, 20))
    if "bell" not in d:
        g.fill(Union([Poly([(814, 230), (818, 196), (830, 186), (842, 196), (846, 230)]), Ell(830, 232, 18, 4)]),
               sphere_paint(824, 204, 22, (170, 130, 60), ry=26, amb=0.4, spec=0.7))
    spire(g, 830, 122, 96, 110, col, seed=8207, light=-1, crockets=False)
    g.fill(Poly([(780, 124), (830, 18), (880, 124), (868, 124), (830, 40), (792, 124)]), (230, 236, 246), alpha=0.6)
    # icicles along the eaves
    g.fill(Box(420, 268, 760, 274), (236, 240, 248))
    if "icicles" not in d:
        for x in range(430, 560, 12):
            hgt = 12 + (x * 7 % 13)
            g.fill(Poly([(x - 3, 274), (x + 3, 274), (x, 274 + hgt)]), (220, 236, 250))
    # snowy ground and path
    g.fill(Under(lambda x: 440 + (fbm1(x, 120, 3, 8208) - 0.5) * 20, -20, W + 20, H + 20), vgrad([(440, (220, 228, 244)), (600, (180, 190, 214))]))
    g.fill(Poly([(560, 452), (620, 452), (700, 610), (430, 610)]), (170, 176, 196), alpha=0.6)
    # pines on the left
    for x, h, key in ((60, 300, None), (170, 220, None), (300, 160, "pine")):
        if key and key in d:
            continue
        pine(g, x, 470 + (300 - h) * 0.2, h, col=(40, 60, 54), seed=8209 + x, snow=(230, 236, 250))
    # frozen statues lining the path
    statue(g, 380, 520, 170, col=(170, 180, 196), seed=8212, light=-1, arms="pray", hood="statue" not in d)
    statue(g, 800, 560, 190, col=(170, 180, 196), seed=8213, light=-1, arms="sword")
    # lantern on a post
    lx, ly = 500, 520
    g.fill(Seg(lx, 600, lx, ly, 3), IRON)
    lit = "lantern" not in d
    if lit:
        g.glow(lx, ly - 12, 70, FIRE, 0.4)
    g.fill(Box(lx - 10, ly - 26, lx + 10, ly, 2), (255, 200, 120) if lit else (60, 66, 80))
    g.fill(Poly([(lx - 13, ly - 26), (lx, ly - 38), (lx + 13, ly - 26)]), IRON)
    g.fill(Ell(lx, ly - 38, 14, 4), (236, 240, 250))
    g.fog(330, 460, (150, 166, 196), 0.0, 0.35, noise=0.5, seed=8214)


L1582_RAYS = [dict(lx=M82[0], ly=M82[1], col=(180, 196, 240), k=1.2, region=Box(-2, -2, W + 2, 330), threshold=110,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=moon_receive(*M82, floor=0.3))]
L1582_ELEMENTS = [
    snow_layer("snow", 8220, 80, 1.2, 2.6, 40, mask=0),
    mist_el("mist", 450, 460, 400, 14, (200, 210, 230), alpha=0.35, length=80, seed=46),
    flame_el("door", 590, 430, 1.2, 0.2),
]
L1582_DIFFS = [("bell", 830, 210, 0), ("window", 470, 330, 0), ("icicles", 494, 282, 0), ("pine", 300, 470, 0), ("statue", 380, 360, 0),
               ("lantern", 500, 500, 0)]


# =================================================================== Level 1583 throne hall
L83 = (450, -500)
WINS83 = [(120, 30, 190, 170), (710, 30, 780, 170)]


def l1583_scene(g, d):
    g.fill(Box(-2, -2, W + 2, H + 2), (24, 20, 22))
    # back wall with high windows
    g.fill(Box(-2, -2, W + 2, 420), stone((70, 62, 60), 8301, 30, 14))
    g.fill(Box(-2, -2, W + 2, 420), (0, 0, 0), alpha=lambda X, Y: 0.25 + 0.35 * smooth(0, 420, Y))
    for w in WINS83:
        x0, y0, x1, y1 = w
        sh = arch(x0, x1, y0 + 40, y1)
        g.fill(sh, vgrad([(y0, (200, 210, 230)), (y1, (150, 160, 190))]))
        g.fill(Inter(Union([Box((x0 + x1) / 2 - 2, y0, (x0 + x1) / 2 + 2, y1), Box(x0, 100, x1, 104)]), sh), (30, 26, 26))
    # floor with perspective
    g.fill(Box(-2, 420, W + 2, H + 2), vgrad([(420, (70, 64, 60)), (600, (40, 36, 34))]))
    for i in range(-14, 15):
        g.fill(Seg(450 + i * 20, 420, 450 + i * 110, 610, 0.8), (36, 32, 30))
    for y in (430, 446, 470, 506, 556):
        g.fill(Seg(-2, y, W + 2, y, 0.8), (36, 32, 30))
    # red carpet to the dais
    carpet = Poly([(400, 610), (500, 610), (466, 420), (434, 420)])
    g.fill(carpet, tex(light_y((120, 24, 30), 420, 600, 0.8, 1.2), 0.2, 4, 4, 3, 8302))
    trim = (200, 160, 70) if "trim" not in d else (60, 110, 170)
    for sgn in (-1, 1):
        g.fill(Poly([(450 + sgn * 46, 610), (450 + sgn * 50, 610), (450 + sgn * 17, 420), (450 + sgn * 15, 420)]), trim)
    # dais and throne
    g.fill(Box(340, 400, 560, 424), light_y((110, 100, 96), 400, 424, 1.3, 0.7))
    g.fill(Box(360, 384, 540, 402), light_y((120, 110, 104), 384, 402, 1.3, 0.7))
    th = Union([Box(400, 220, 500, 384, 4), Poly([(400, 222), (420, 170), (450, 150), (480, 170), (500, 222)])])
    g.fill(th, tex(light_x((90, 70, 50), 400, 500, 1.3, 0.6), 0.2, 2, 6, 3, 8303))
    g.fill(Box(414, 236, 486, 330, 3), (110, 24, 30))
    g.fill(Box(392, 320, 508, 344, 3), light_y((110, 86, 60), 320, 344, 1.3, 0.7))
    for x in (396, 504):
        g.fill(Seg(x, 300, x, 384, 6), (90, 70, 50))
        g.fill(Circ(x, 300, 8), sphere_paint(x - 2, 298, 8, (200, 160, 70), amb=0.4, spec=0.6))
    if "crown" not in d:
        cw = Poly([(430, 320), (430, 300), (438, 308), (444, 294), (450, 306), (456, 294), (462, 308), (470, 300), (470, 320)])
        g.fill(cw, sphere_paint(442, 304, 30, (230, 190, 80), ry=16, amb=0.4, spec=0.8))
        g.fill(Circ(450, 314, 3), (180, 30, 40))
    # pillars receding on both sides with banners
    for i, t_ in enumerate((0.0, 0.45, 0.75)):
        for sgn in (-1, 1):
            x = 450 + sgn * (400 - 250 * t_)
            w = 70 - 46 * t_
            base = 610 - 180 * t_
            col_s = Box(x - w / 2, -10, x + w / 2, base)
            g.fill(col_s, tex(cyl_paint(x - sgn * w * 0.1, w / 2, (110, 102, 96), amb=0.3, spec=0.1), 0.15, 3, 10, 3, 8304 + i))
            g.mul(col_s, 0.25 + 0.3 * t_)
            if i < 2:
                bw = w * 0.9
                key = "banner" if (i == 0 and sgn == -1) else None
                banner(g, x, 120 + 30 * t_, bw, 160 - 60 * t_, (110, 24, 30), seed=8310 + i * 2 + sgn,
                       emblem=(emblem_sun if not (key and key in d) else emblem_moon), pole=False)
    # shield hung on the right near pillar
    if "shield" not in d:
        sx0, sy0 = 850, 330
        sh = Union([Box(sx0 - 26, sy0 - 30, sx0 + 26, sy0), Inter(Circ(sx0 - 26, sy0, 52), Circ(sx0 + 26, sy0, 52)) & Box(sx0 - 26, sy0, sx0 + 26, sy0 + 50)])
        g.fill(sh, light_x((40, 70, 120), sx0 - 26, sx0 + 26, 1.3, 0.6))
        emblem_tree(g, sx0, sy0, 22)
    # braziers flanking the throne
    brazier(g, 300, 420, 1.0, lit=True)
    brazier(g, 600, 420, 1.0, lit="brazier" not in d)
    # armour stand on the left
    knight(g, 210, 520, 170, steel=(110, 112, 118), cloth=(60, 50, 60), face=1, sword=None, helm="great" if "helm" not in d else "bascinet",
           rim_dx=-1.6, rim_col=(200, 210, 230), rim_k=0.4)
    g.fog(300, 600, (60, 56, 60), 0.0, 0.25, noise=0.4, seed=8320)


L1583_RAYS = [dict(lx=L83[0], ly=L83[1], col=(200, 210, 236), k=1.6, region=Union([arch(w[0], w[2], w[1] + 40, w[3]) for w in WINS83]), threshold=100,
                   soft=60, density=0.92, decay=0.97, samples=70, receive=Box(-20, 100, W + 20, H + 20))]
L1583_ELEMENTS = [
    fire_el("brz", 300, 370, 1.2, 0.2),
    beam_el("beamL", 155, 110, 320, 560, 50, 150, col=(210, 220, 240), k=0.09),
    beam_el("beamR", 745, 110, 580, 560, 50, 150, col=(210, 220, 240), k=0.09, phase=0.5),
    motes_el("dust", [(240, 300), (660, 320), (450, 260)], vx=2, vy=-3, length=20),
]
L1583_DIFFS = [("crown", 450, 308, 0), ("trim", 476, 560, 0), ("banner", 50, 190, 0), ("shield", 850, 340, 0), ("brazier", 600, 368, 0),
               ("helm", 212, 340, 0)]


# =================================================================== Level 1584 arena duel
SUN84 = (470, 230, 30)


def l1584_scene(g, d):
    sx_, sy_, sr = SUN84
    sky(g, [(0, (50, 50, 80)), (180, (190, 120, 100)), (300, (250, 180, 110))])
    cloud_layer(g, 40, 190, (230, 150, 120), (90, 70, 90), cover=0.45, sx=220, sy=20, seed=8401, alpha=0.8)
    sun(g, sx_, sy_, sr, col=(255, 236, 200), halo=(255, 170, 100), k=0.9)
    # curved two-tier arena wall with a broken gap where the sun shows
    col = (150, 120, 100)

    def wall_top(x):
        return 230 + 60 * ((x - 450) / 450.0) ** 2 + (fbm1(x, 40, 3, 8402) - 0.5) * 10
    arena = Diff(Under(wall_top, -20, W + 20, 470), Poly([(400, 200), (540, 200), (520, 300), (420, 300)]))
    g.fill(arena, stone(col, 8403, 24, 12))
    g.fill(arena, (0, 0, 0), alpha=lambda X, Y: 0.3 + 0.2 * smooth(230, 470, Y))
    for tier, (ys, yb, h) in enumerate(((300, 360, 40), (400, 462, 44))):
        for x in range(-40, 940, 70):
            if tier == 0 and 400 < x + 35 < 540:
                continue
            gy = ys + 30 * ((x - 450) / 450.0) ** 2
            g.fill(arch(x + 10, x + 54, gy, gy + h + 10, pointed=False), (40, 26, 26))
    rim(g, arena, 0, 2, col=SUNSET, k=0.3)
    # pennants on the wall
    for x, key in ((110, "pennant"), (790, None)):
        top = float(wall_top(np.array([x], np.float32))[0])
        g.fill(Seg(x, top, x, top - 70, 1.8), IRON)
        if not (key and key in d):
            g.fill(Poly([(x + 1, top - 68), (x + 50, top - 58), (x + 1, top - 46)]), light_x((140, 30, 30), x, x + 50, 1.2, 0.7))
    # sand floor
    g.fill(Box(-2, 460, W + 2, H + 2), tex(vgrad([(460, (200, 160, 110)), (600, (150, 110, 76))]), 0.3, 6, 3, 4, 8404))
    # broken columns
    for x, h, key in ((70, 160, None), (840, 120, "column")):
        if key and key in d:
            h = 60
        g.fill(Box(x - 20, 540 - h, x + 20, 540), tex(cyl_paint(x - 6, 20, (180, 170, 156), amb=0.35, spec=0.1), 0.2, 3, 8, 3, 8405 + x))
        g.fill(Poly([(x - 22, 540 - h), (x - 8, 540 - h - 14), (x + 6, 540 - h - 4), (x + 22, 540 - h - 18), (x + 22, 540 - h + 4), (x - 22, 540 - h + 4)]), (170, 160, 146))
        g.fill(Box(x - 28, 530, x + 28, 548), (160, 150, 136))
    # a sword stuck in the sand
    if "sword" not in d:
        g.fill(Seg(590, 560, 600, 480, 2, 4), lgrad(586, 0, 604, 0, [(0, (200, 204, 214)), (1, (100, 100, 110))]))
        g.fill(Seg(586, 482, 616, 476, 2.6), (120, 96, 60))
        g.fill(Seg(601, 478, 604, 458, 2.6), (70, 50, 36))
    # the giant armoured warden (right) and the knight (left)
    knight(g, 690, 580, 420, steel=(80, 78, 84), cloth=(60, 40, 40), face=-1, sword="up", helm="bascinet", rim_dx=-2.4, rim_col=SUNSET, rim_k=0.55)
    knight(g, 260, 580, 230, steel=(130, 132, 140), cloth=(40, 60, 100), face=1, sword="up",
           shield=((150, 30, 30), emblem_sun if "shield" not in d else emblem_tree), helm="great",
           plume=(220, 220, 210) if "plume" not in d else None, rim_dx=2.2, rim_col=SUNSET, rim_k=0.5)
    g.fog(420, 520, (230, 180, 140), 0.0, 0.25, noise=0.5, seed=8406)


def l1584_receive(X, Y):
    return sun_receive(*SUN84, floor=0.3)(X, Y) * (0.25 + 0.75 * smooth(420, 260, Y))


L1584_RAYS = [dict(lx=SUN84[0], ly=SUN84[1], col=(255, 200, 140), k=0.7, region=Box(-2, -2, W + 2, 300), threshold=180,
                   soft=60, density=0.9, decay=0.97, samples=64, receive=l1584_receive)]
L1584_ELEMENTS = [
    mist_el("dust1", 450, 540, 400, 16, (230, 190, 140), alpha=0.35, length=90, seed=47),
    E("birds", el(lambda g, m: [g.fill(Union([Seg(x - 7, y - 3, x, y, 1.6), Seg(x, y, x + 7, y - 3, 1.6)]), (40, 30, 34))
                                for x, y in ((620, 90), (640, 82), (660, 96))]),
      anim=dict(bobAmplitude=(40, 8), bobSpeed=0.06)),
]
L1584_DIFFS = [("pennant", 136, 200, 0), ("column", 840, 400, 0), ("sword", 598, 520, 0), ("shield", 200, 360, 0), ("plume", 230, 230, 0)]


LEVELS = [
    ("Level1575", "余烬神殿", make_bg(l1575_scene, L1575_RAYS), L1575_ELEMENTS, L1575_DIFFS, 60, OPTS),
    ("Level1576", "要塞城门", flat_bg(l1576_scene, bloom=(200, 16, 0.35)), L1576_ELEMENTS, L1576_DIFFS, 60, OPTS),
    ("Level1577", "龙踞城楼", flat_bg(l1577_scene, bloom=(190, 18, 0.45)), L1577_ELEMENTS, L1577_DIFFS, 60, OPTS),
    ("Level1578", "黄昏神都", make_bg(l1578_scene, L1578_RAYS), L1578_ELEMENTS, L1578_DIFFS, 60, OPTS),
    ("Level1579", "熔岩废城", flat_bg(l1579_scene, bloom=(180, 18, 0.5)), L1579_ELEMENTS, L1579_DIFFS, 60, OPTS),
    ("Level1580", "腐毒沼泽", flat_bg(l1580_scene, bloom=(190, 16, 0.4)), L1580_ELEMENTS, L1580_DIFFS, 60, OPTS),
    ("Level1581", "地下墓窟", flat_bg(l1581_scene, bloom=(200, 14, 0.4)), L1581_ELEMENTS, L1581_DIFFS, 60, OPTS),
    ("Level1582", "雪原圣堂", make_bg(l1582_scene, L1582_RAYS), L1582_ELEMENTS, L1582_DIFFS, 60, OPTS),
    ("Level1583", "王座大厅", make_bg(l1583_scene, L1583_RAYS, bloom=(200, 14, 0.35)), L1583_ELEMENTS, L1583_DIFFS, 60, OPTS),
    ("Level1584", "竞技场决战", make_bg(l1584_scene, L1584_RAYS), L1584_ELEMENTS, L1584_DIFFS, 60, OPTS),
]
