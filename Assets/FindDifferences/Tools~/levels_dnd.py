# -*- coding: utf-8 -*-
"""American-comic (heavy inks, flat colour, halftone shadows) tabletop-fantasy adventure levels.
Generic sword-and-sorcery: adventurers, dragons, goblins, trolls, giant spiders - all original designs; no product-identity
monsters, no readable text, no gore.
  Level1605 冒险者酒馆 - a tavern: the party plans over a map and dice, fireplace, quest board, barkeep
  Level1606 地牢走廊   - a torch-lit dungeon corridor: pressure plate, chest, chains, portcullis
  Level1607 巨龙宝藏   - a dragon asleep on its hoard while a rogue sneaks in
  Level1608 哥布林营地 - a goblin camp at night: tents, campfire, totem, cage; heroes hiding behind rocks
  Level1609 法师塔书房 - a wizard's tower study: cauldron, crystal ball, star chart, owl
  Level1610 巨魔石桥   - a troll lurking under a stone bridge as the party crosses
  Level1611 蛛网洞窟   - a giant spider's cavern: webs, glowing crystals, a lantern-bearing adventurer
  Level1612 丛林遗迹   - a vine-covered jungle temple: stairs, guardian statues, golden idol
  Level1613 奇幻集市   - a fantasy market: potion stall, smithy, banners, townsfolk
  Level1614 巨人山口   - a stone giant blocking a snowy mountain pass, the party with shields raised
"""
import math
import random

import numpy as np

from fdcore import E, H, W
from real import Box, Circ, Ctx, Diff, Ell, Inter, Poly, Rough, Seg, Under, Union, el, fbm1, mixc, real_post, vgrad
from levels_remake import ComicS, POSTS
from levels_isostyle import halftone
from toon import cloud_shape
from styled_kit import (SKIN, banner, barrel, bush, castle, chest, coin_pile, crate, crystal, dragon, goblin, pine_tree, potion,
                        rock, round_tree, sh_shadow, sign_board, sparkle_el, torch, tower)

S = ComicS()
INK = S.ink
OPTS = dict(post=POSTS["comic"], anim_seconds=12.0, frames=60)


def make(scene):
    def bg(c, d):
        g = Ctx(c)
        scene(g, d)
        S.finish(g)
        g.commit()
    return bg


def wave(y, amp, period, seed):
    return lambda x: y + amp * np.sin(x / period + seed) + (fbm1(x, 60, 2, seed) - 0.5) * amp


# =================================================================== adventurers (original designs)
def adventurer(g, x, base, h, kind="fighter", face=1, seed=0, main=None, trim=None, skin=SKIN, hair=(90, 60, 40), weapon=True,
               shield=None, hood=None, beard=False):
    """Heroic-proportion adventurer (~7 heads). kind: fighter / wizard / rogue / cleric."""
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    main = main or {"fighter": (160, 40, 40), "wizard": (60, 60, 160), "rogue": (50, 70, 50), "cleric": (230, 220, 200)}[kind]
    trim = trim or {"fighter": (190, 190, 200), "wizard": (230, 190, 70), "rogue": (90, 60, 40), "cleric": (230, 190, 70)}[kind]
    sh_shadow(S, g, x, base, 46 * k, 7 * k)
    # cloak behind
    if kind in ("rogue", "wizard", "cleric"):
        S.obj(g, Poly([(sx(-30), sy(240)), (sx(26), sy(240)), (sx(-10), sy(20)), (sx(-60), sy(30))]), mixc(main, (0, 0, 0), 0.3), seed, "fabric")
    # legs
    if kind in ("wizard", "cleric"):
        S.obj(g, Poly([(sx(-34), sy(4)), (sx(34), sy(4)), (sx(24), sy(160)), (sx(-24), sy(160))]), main, seed + 1, "fabric")
    else:
        for dx, fx in ((-12, -18), (12, 16)):
            S.obj(g, Seg(sx(dx), sy(150), sx(fx), sy(14), 12 * k, 10 * k), (70, 60, 56) if kind == "rogue" else trim, seed + 2)
            S.obj(g, Ell(sx(fx + 6), sy(7), 15 * k, 7 * k), (80, 56, 40), seed + 3)
    # torso
    S.obj(g, Poly([(sx(-30), sy(250)), (sx(30), sy(250)), (sx(26), sy(140)), (sx(-26), sy(140))]), main if kind != "fighter" else trim, seed + 4, hi=kind == "fighter")
    if kind == "fighter":
        S.obj(g, Poly([(sx(-28), sy(160)), (sx(28), sy(160)), (sx(32), sy(100)), (sx(-32), sy(100))]), main, seed + 5, "fabric")
    S.obj(g, Box(sx(-28) if f > 0 else sx(28), sy(150), sx(28) if f > 0 else sx(-28), sy(140)), (100, 70, 40), seed + 6)
    # arms
    S.obj(g, Seg(sx(-30), sy(240), sx(-38), sy(160), 10 * k, 9 * k), main if kind != "fighter" else trim, seed + 7)
    S.obj(g, Seg(sx(30), sy(240), sx(44), sy(170), 10 * k, 9 * k), main if kind != "fighter" else trim, seed + 8)
    hand = (sx(46), sy(164))
    S.obj(g, Circ(hand[0], hand[1], 8 * k), skin, seed + 9)
    # weapon
    if weapon:
        if kind == "fighter":
            S.obj(g, Poly([(hand[0] - 3 * k, hand[1] - 8 * k), (hand[0] + 3 * k, hand[1] - 8 * k), (hand[0] + 4 * k, hand[1] - 150 * k), (hand[0], hand[1] - 162 * k),
                           (hand[0] - 4 * k, hand[1] - 150 * k)]), (220, 225, 235), seed + 10, hi=True)
            S.obj(g, Box(hand[0] - 16 * k, hand[1] - 12 * k, hand[0] + 16 * k, hand[1] - 6 * k), (200, 160, 60), seed + 11)
        elif kind == "wizard":
            S.obj(g, Seg(hand[0], sy(4), hand[0] + f * 6 * k, sy(300), 4 * k), (120, 80, 50), seed + 10)
            S.glow(g, hand[0] + f * 6 * k, sy(312), 34 * k, (150, 230, 255), 0.4)
            S.obj(g, Circ(hand[0] + f * 6 * k, sy(312), 12 * k), (150, 230, 255), seed + 11, hi=True)
        elif kind == "rogue":
            S.obj(g, Poly([(hand[0], hand[1]), (hand[0] + f * 50 * k, hand[1] - 20 * k), (hand[0] + f * 46 * k, hand[1] - 10 * k)]), (220, 225, 235), seed + 10)
        elif kind == "cleric":
            S.obj(g, Seg(hand[0], hand[1] + 10 * k, hand[0] + f * 4 * k, hand[1] - 70 * k, 3.5 * k), (130, 100, 60), seed + 10)
            S.obj(g, Union([Circ(hand[0] + f * 4 * k, hand[1] - 80 * k, 14 * k)] + [Seg(hand[0] + f * 4 * k, hand[1] - 80 * k, hand[0] + f * 4 * k + math.cos(a) * 20 * k,
                                                                                         hand[1] - 80 * k + math.sin(a) * 20 * k, 3 * k) for a in np.linspace(0, math.tau, 7)[:-1]]),
                  (200, 200, 210), seed + 11, hi=True)
    if shield is not None:
        cx, cy = sx(-40), sy(190)
        S.obj(g, Union([Box(cx - 30 * k, cy - 40 * k, cx + 30 * k, cy + 6 * k), Inter(Circ(cx - 30 * k, cy, 60 * k), Circ(cx + 30 * k, cy, 60 * k)) & Box(cx - 30 * k, cy, cx + 30 * k, cy + 60 * k)]),
              shield, seed + 12, hi=True)
        S.flat(g, Union([Box(cx - 4 * k, cy - 34 * k, cx + 4 * k, cy + 44 * k), Box(cx - 24 * k, cy - 8 * k, cx + 24 * k, cy)]), (240, 210, 90))
    # head
    hx, hy = sx(2), sy(272)
    S.obj(g, Ell(hx, hy, 17 * k, 20 * k), skin, seed + 13)
    S.flat(g, Circ(hx + f * 9 * k, hy - 2 * k, 2 * k), INK)
    if beard:
        S.obj(g, Poly([(hx - 14 * k, hy + 4 * k), (hx + 16 * k, hy + 4 * k), (hx + f * 6 * k, hy + 40 * k)]), (210, 210, 210), seed + 14)
    if kind == "wizard":
        S.obj(g, Union([Ell(hx, hy - 16 * k, 34 * k, 6 * k), Poly([(hx - 18 * k, hy - 16 * k), (hx - f * 30 * k, hy - 80 * k), (hx + 18 * k, hy - 16 * k)])]),
              hood or main, seed + 15)
    elif kind in ("rogue", "cleric") or hood:
        S.obj(g, Union([Ell(hx - f * 4 * k, hy - 6 * k, 22 * k, 26 * k) - Ell(hx + f * 6 * k, hy + 2 * k, 15 * k, 18 * k)]),
              hood or mixc(main, (0, 0, 0), 0.15), seed + 15)
    else:
        S.obj(g, Union([Ell(hx - f * 2 * k, hy - 12 * k, 18 * k, 12 * k), Box(hx - f * 18 * k - 4 * k, hy - 12 * k, hx - f * 8 * k, hy + 10 * k)]), hair, seed + 15)
    return hand


def troll(g, x, base, h, skin=(110, 140, 100), face=1, seed=0, club=True, eyes=(250, 220, 60), cloth=(120, 90, 60)):
    k = h / 300.0
    f = face
    sx = lambda v: x + f * v * k
    sy = lambda v: base - v * k
    sh_shadow(S, g, x, base, 90 * k, 10 * k)
    for dx in (-30, 30):
        S.obj(g, Seg(sx(dx), sy(130), sx(dx * 1.1), sy(10), 24 * k, 20 * k), skin, seed)
    S.obj(g, Ell(sx(0), sy(170), 80 * k, 80 * k), skin, seed + 1, hi=True)
    S.obj(g, Poly([(sx(-70), sy(120)), (sx(70), sy(120)), (sx(60), sy(80)), (sx(-60), sy(80))]), cloth, seed + 2, "fabric")
    S.obj(g, Seg(sx(-70), sy(220), sx(-100), sy(80), 18 * k, 16 * k), skin, seed + 3)
    S.obj(g, Seg(sx(70), sy(220), sx(110), sy(120), 18 * k, 16 * k), skin, seed + 4)
    if club:
        S.obj(g, Union([Seg(sx(110), sy(120), sx(150), sy(280), 10 * k, 22 * k)]), (130, 90, 60), seed + 5, "wood")
    hx, hy = sx(20), sy(260)
    S.obj(g, Union([Ell(hx, hy, 40 * k, 34 * k), Poly([(hx + f * 30 * k, hy), (hx + f * 54 * k, hy + 8 * k), (hx + f * 30 * k, hy + 16 * k)])]), skin, seed + 6, hi=True)
    for ex in (-8, 16):
        S.flat(g, Ell(hx + f * ex * k, hy - 6 * k, 6 * k, 4 * k), eyes)
        S.flat(g, Circ(hx + f * ex * k, hy - 6 * k, 2 * k), INK)
    S.flat(g, Seg(hx - 14 * k, hy + 18 * k, hx + f * 26 * k, hy + 18 * k, 3 * k), INK)
    for tx in (-6, 14):
        S.flat(g, Poly([(hx + f * tx * k, hy + 17 * k), (hx + f * (tx + 4) * k, hy + 8 * k), (hx + f * (tx + 8) * k, hy + 17 * k)]), (250, 250, 230))


def spider(g, x, y, s, col=(60, 50, 70), seed=0, eyes=(255, 60, 60), mark=(230, 60, 60)):
    for sgn in (-1, 1):
        for i in range(4):
            a = -0.9 + i * 0.5
            kx, ky = x + sgn * math.cos(a) * 70 * s, y - 40 * s + math.sin(a) * 30 * s
            S.obj(g, Union([Seg(x + sgn * 20 * s, y, kx, ky, 6 * s, 5 * s), Seg(kx, ky, kx + sgn * 30 * s, y + 70 * s, 5 * s, 2 * s)]), col, seed + i)
    S.obj(g, Ell(x, y + 30 * s, 50 * s, 40 * s), col, seed + 5, hi=True)
    S.flat(g, Union([Poly([(x - 14 * s, y + 14 * s), (x + 14 * s, y + 14 * s), (x, y + 32 * s)]), Poly([(x - 14 * s, y + 50 * s), (x + 14 * s, y + 50 * s), (x, y + 32 * s)])]), mark)
    S.obj(g, Ell(x, y - 10 * s, 28 * s, 22 * s), col, seed + 6, hi=True)
    for ex, ey in ((-10, -16), (10, -16), (-5, -8), (5, -8)):
        S.flat(g, Circ(x + ex * s, y + ey * s, 3.6 * s), eyes)


def web(g, cx, cy, r, quad=(1, 1), col=(240, 240, 250), n=7):
    sx, sy = quad
    angs = [i * (math.pi / 2) / (n - 1) for i in range(n)]
    for a in angs:
        g.fill(Seg(cx, cy, cx + sx * math.cos(a) * r, cy + sy * math.sin(a) * r, 1.0), col)
    for f in (0.3, 0.5, 0.7, 0.9):
        for a0, a1 in zip(angs[:-1], angs[1:]):
            g.fill(Seg(cx + sx * math.cos(a0) * r * f, cy + sy * math.sin(a0) * r * f, cx + sx * math.cos(a1) * r * f, cy + sy * math.sin(a1) * r * f, 0.8), col)


def burst(g, x, y, r, col=(255, 230, 80), n=12, seed=0):
    """Comic action starburst (no lettering)."""
    rnd = random.Random(seed)
    pts = []
    for i in range(n * 2):
        a = i * math.pi / n
        rr = r if i % 2 == 0 else r * rnd.uniform(0.45, 0.6)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    S.obj(g, Poly(pts), col, seed, line=True)


def d20(g, x, y, r, col):
    pts = [(x + math.cos(-math.pi / 2 + i * math.tau / 6) * r, y + math.sin(-math.pi / 2 + i * math.tau / 6) * r) for i in range(6)]
    S.obj(g, Poly(pts), col, 0, hi=True)
    tri = [(x, y - r * 0.55), (x + r * 0.5, y + r * 0.3), (x - r * 0.5, y + r * 0.3)]
    g.fill(Poly(tri), mixc(col, (255, 255, 255), 0.25))
    for p0, p1 in zip(tri, tri[1:] + tri[:1]):
        g.fill(Seg(p0[0], p0[1], p1[0], p1[1], 1.2), INK)
    for i in range(6):
        g.fill(Seg(pts[i][0], pts[i][1], tri[(i // 2) % 3][0], tri[(i // 2) % 3][1], 1.0), INK)


def stone_arch(g, x0, x1, ys, base, col, seed, depth=0.0):
    w = x1 - x0
    S.obj(g, Diff(Union([Box(x0 - 18, ys, x1 + 18, base), Inter(Ell((x0 + x1) / 2, ys, w / 2 + 18, w / 2 + 18), Box(x0 - 18, ys - w, x1 + 18, ys + 1))]),
                  Union([Box(x0, ys, x1, base + 2), Inter(Ell((x0 + x1) / 2, ys, w / 2, w / 2), Box(x0, ys - w, x1, ys + 1))])), col, seed, "stone", depth=depth)


# =================================================================== Level 1605 adventurers' tavern
def l1605(g, d):
    S.obj(g, Box(-2, -2, W + 2, 420), (150, 100, 60), 1, "wood", line=False)
    for x in range(0, 900, 60):
        S.flat(g, Box(x, -2, x + 3, 420), (110, 70, 40))
    S.obj(g, Box(-2, 40, W + 2, 60), (100, 60, 30), 2, "wood")
    # fireplace (right)
    S.obj(g, Box(640, 180, 860, 420), (150, 140, 130), 3, "stone")
    S.obj(g, Union([Box(680, 280, 820, 420), Circ(750, 280, 70) & Box(680, 210, 820, 280)]), (30, 20, 20), 4)
    S.glow(g, 750, 380, 120, (255, 150, 60), 0.5)
    S.obj(g, Union([Ell(750, 400, 60, 14)]), (110, 70, 40), 5, "wood")
    # trophy antlers above the fireplace
    if "antlers" not in d:
        S.obj(g, Ell(750, 140, 30, 22), (200, 170, 130), 6, hi=True)
        for sgn in (-1, 1):
            S.obj(g, Union([Seg(750 + sgn * 20, 126, 750 + sgn * 70, 80, 4), Seg(750 + sgn * 50, 98, 750 + sgn * 54, 70, 3), Seg(750 + sgn * 64, 86, 750 + sgn * 84, 70, 3)]),
                  (240, 230, 200), 7)
    # quest board (left) with notices (no text)
    S.obj(g, Box(40, 100, 220, 240, 3), (130, 90, 50), 8, "wood")
    for i, (x0, y0, c) in enumerate(((52, 112, (240, 230, 200)), (110, 120, (230, 220, 180)), (162, 110, (240, 230, 200)), (60, 172, (240, 220, 190)), (130, 176, (230, 210, 170)))):
        if "notice" in d and i == 4:
            continue
        S.obj(g, Box(x0, y0, x0 + 46, y0 + 52), c, 9 + i)
        for r in range(3):
            g.fill(Box(x0 + 6, y0 + 10 + r * 12, x0 + 40 - r * 6, y0 + 13 + r * 12), INK, alpha=0.6)
        S.flat(g, Circ(x0 + 23, y0 + 3, 3), (200, 40, 40))
    # hanging lanterns
    for i, x in enumerate((320, 520)):
        g.fill(Seg(x, 60, x, 110, 1.4), INK)
        lit = not ("lantern" in d and i == 1)
        if lit:
            S.glow(g, x, 126, 60, (255, 200, 100), 0.4)
        S.obj(g, Box(x - 12, 108, x + 12, 144, 3), (255, 210, 120) if lit else (90, 80, 70), 14 + i)
    # floor
    S.ground(g, Box(-2, 420, W + 2, H + 2), (120, 80, 50), "wood", 16)
    # bar counter with the barkeep and mugs
    adventurer(g, 120, 470, 200, kind="fighter", main=(240, 236, 220), trim=(120, 90, 60), face=1, seed=17, weapon=False, beard=True, hair=(200, 200, 200))
    S.obj(g, Box(-2, 380, 260, 470, 3), (140, 90, 50), 18, "wood")
    S.obj(g, Box(-2, 372, 270, 386, 3), (170, 110, 60), 19, "wood")
    for x in (60, 200):
        S.obj(g, Union([Box(x - 12, 344, x + 12, 374, 2), Seg(x + 12, 352, x + 20, 366, 3)]), (200, 170, 100), 20 + x)
    # the party's table with a map and dice
    S.obj(g, Ell(470, 470, 170, 40), (150, 100, 60), 22, "wood")
    S.obj(g, Union([Box(380, 476, 400, 580), Box(540, 476, 560, 580)]), (110, 70, 40), 23, "wood")
    S.obj(g, Poly([(400, 450), (540, 446), (550, 476), (396, 482)]), (240, 220, 170) if "map" not in d else (200, 230, 210), 24)
    g.fill(Seg(420, 466, 520, 456, 1.5), (200, 60, 60))
    g.fill(Circ(520, 456, 5), (200, 60, 60))
    d20(g, 580, 460, 14, (220, 40, 60) if "dice" not in d else (60, 90, 220))
    S.obj(g, Union([Box(350, 432, 374, 462, 2), Seg(374, 440, 382, 454, 3)]), (200, 170, 100), 25)
    adventurer(g, 320, 600, 230, kind="wizard", face=1, seed=26)
    adventurer(g, 640, 600, 240, kind="fighter", face=-1, seed=27, shield=(60, 90, 170))
    adventurer(g, 830, 600, 220, kind="rogue", face=-1, seed=28)


L1605_EL = [E("fire", el(lambda g, m: S.obj(g, Union([Ell(750, 384, 40, 14), Poly([(716, 386), (736, 330), (750, 360), (764, 320), (786, 386)])]), (255, 170, 60), 30, line=False)),
              pivot=(750, 396), daynight="untinted", anim=dict(stretch=(0.06, 0.25), scaleSpeed=2.2)),
            E("glowL", el(lambda g, m: g.glow(320, 126, 30, (255, 220, 140), 0.4)), daynight="untinted", anim=dict(pulse=0.1, scaleSpeed=1.4))]
L1605_DIFFS = [("antlers", 750, 110, 0), ("notice", 153, 202, 0), ("lantern", 520, 126, 0), ("map", 470, 464, 0), ("dice", 580, 460, 0)]


# =================================================================== Level 1606 dungeon corridor
def l1606(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (40, 36, 44), 1, line=False)
    for i in range(6):
        t = i / 5
        k = 1 - 0.8 * t
        cx, cy = 450, 300
        w, hh = 440 * k, 300 * k
        c = mixc((130, 120, 120), (40, 36, 44), t)
        stone_arch(g, cx - w * 0.75, cx + w * 0.75, cy - hh * 0.3, cy + hh * 0.95, c, 2 + i)
    S.obj(g, Box(390, 210, 510, 330), (20, 18, 22), 10)
    gate = Union([Box(x, 210, x + 4, 330) for x in range(396, 510, 14)] + [Box(390, 250, 510, 254), Box(390, 290, 510, 294)])
    g.fill(gate, (90, 90, 100) if "gate" not in d else (150, 110, 60))
    S.ground(g, Poly([(-20, 610), (920, 610), (520, 330), (380, 330)]), (90, 84, 90), "stone", 11)
    for k_ in range(6):
        y = 340 + 270 * (k_ / 5) ** 1.5
        g.fill(Seg(450 - (y - 330) * 1.6, y, 450 + (y - 330) * 1.6, y, 1.2), INK, alpha=0.6)
    # pressure plate trap
    S.obj(g, Poly([(400, 470), (500, 470), (514, 500), (388, 500)]), (120, 116, 120) if "plate" not in d else (150, 60, 60), 12)
    # torches on the walls
    for x, y in ((120, 200), (780, 200), (300, 250), (600, 250)):
        torch(S, g, x, y, lit=not ("torch" in d and x == 780))
    # chains hanging and a chest
    if "chain" not in d:
        for k_ in range(10):
            S.obj(g, Ell(200, 40 + k_ * 12, 4, 7) - Ell(200, 40 + k_ * 12, 1.6, 4), (130, 130, 140), 20 + k_)
    chest(S, g, 760, 560, 60, open_=False, seed=13)
    if "gold" not in d:
        coin_pile(S, g, 680, 572, 50, seed=14)
    adventurer(g, 300, 600, 240, kind="fighter", face=1, seed=15, shield=(60, 90, 170))
    adventurer(g, 180, 600, 220, kind="cleric", face=1, seed=16)


L1606_EL = [E("f%d" % i, el(lambda g, m, x=x, y=y: S.glow(g, x, y - 10, 30, (255, 190, 90), 0.5)), daynight="untinted",
              anim=dict(pulse=0.15, scaleSpeed=2.0 + i * 0.3)) for i, (x, y) in enumerate(((120, 200), (300, 250), (600, 250)))]
L1606_DIFFS = [("gate", 450, 270, 0), ("plate", 450, 485, 0), ("torch", 780, 190, 0), ("chain", 200, 100, 0), ("gold", 680, 560, 0)]



# =================================================================== Level 1607 dragon's hoard
def l1607(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (60, 44, 50), 1, "stone", line=False)
    S.obj(g, Poly([(-20, -2), (920, -2), (920, 120), (760, 80), (600, 140), (420, 70), (240, 130), (80, 60), (-20, 110)]), (40, 30, 36), 2, "stone")
    for x, h in ((120, 120), (330, 80), (800, 100)):
        S.obj(g, Poly([(x - 20, 100), (x, 100 + h), (x + 20, 100)]), (70, 56, 60), 3 + x, "stone")
    S.ground(g, Box(-2, 450, W + 2, H + 2), (90, 70, 60), "stone", 4)
    # the hoard
    S.obj(g, Ell(520, 470, 330, 90), (240, 196, 60), 5, hi=True)
    rnd = random.Random(1607)
    for _ in range(60):
        x, y = rnd.uniform(220, 820), rnd.uniform(400, 520)
        S.obj(g, Ell(x, y, 7, 3), (255, 220, 90), 6, line=False)
    for x, y, c in ((300, 470, (220, 40, 60)), (720, 440, (60, 160, 220)), (640, 500, (60, 200, 120))):
        S.obj(g, Poly([(x, y - 12), (x + 10, y), (x, y + 12), (x - 10, y)]), c, 7, hi=True)
    # crown, goblet, shield in the gold
    if "crown" not in d:
        S.obj(g, Poly([(260, 420), (260, 396), (272, 408), (282, 390), (292, 408), (304, 396), (304, 420)]), (250, 210, 60), 8, hi=True)
    S.obj(g, Union([Poly([(780, 470), (810, 470), (802, 500), (788, 500)]), Box(792, 500, 798, 520), Box(782, 518, 808, 524)]),
          (250, 210, 60) if "goblet" not in d else (190, 190, 200), 9, hi=True)
    S.obj(g, Union([Box(380, 500, 440, 530), Inter(Circ(380, 530, 60), Circ(440, 530, 60)) & Box(380, 530, 440, 580)]), (60, 90, 170), 10, hi=True)
    # the sleeping dragon on top
    dragon(S, g, 560, 330, 1.25, col=(150, 40, 40), belly=(240, 190, 110), face=-1, seed=11, wings_up=False)
    if "horns" in d:
        for hx in (96, 108):
            g.fill(Poly([(560 - 1.25 * hx, 330 - 1.25 * 84), (560 - 1.25 * (hx - 22), 330 - 1.25 * 116), (560 - 1.25 * (hx + 8), 330 - 1.25 * 88)]), (60, 50, 60))
    S.flat(g, Seg(560 - 1.25 * 128, 330 - 1.25 * 76, 560 - 1.25 * 116, 330 - 1.25 * 76, 2), INK)
    # the rogue sneaking in (left) and torch
    adventurer(g, 110, 600, 240, kind="rogue", face=1, seed=12, main=(50, 70, 50) if "cloak" not in d else (110, 40, 90))
    torch(S, g, 860, 240, lit=True)


L1607_EL = [E("zzz", el(lambda g, m: [g.fill(Union([Seg(330 + k * 14, 250 - k * 22, 344 + k * 14, 250 - k * 22, 2), Seg(344 + k * 14, 250 - k * 22, 330 + k * 14, 262 - k * 22, 2),
                                                          Seg(330 + k * 14, 262 - k * 22, 344 + k * 14, 262 - k * 22, 2)]), (250, 250, 250)) for k in range(3)]),
              daynight="untinted", anim=dict(driftVelocity=(4, 20), driftLength=40, driftFade=True)),
            sparkle_el("gleam", [(300, 470), (640, 500), (720, 440), (500, 420)], col=(255, 250, 200), r=6, speed=0.6),
            E("fl", el(lambda g, m: S.glow(g, 860, 230, 30, (255, 190, 90), 0.5)), daynight="untinted", anim=dict(pulse=0.15, scaleSpeed=2.0))]
L1607_DIFFS = [("crown", 282, 408, 0), ("goblet", 795, 494, 0), ("horns", 430, 210, 0), ("cloak", 90, 480, 0)]


# =================================================================== Level 1608 goblin camp at night
def l1608(g, d):
    S.sky(g, [(0, (20, 26, 60)), (300, (60, 50, 90))])
    S.obj(g, Circ(760, 90, 40), (250, 245, 210), 1, line=False)
    for x in range(-20, 920, 70):
        pine_tree(S, g, x, 330, 160 + (x * 7 % 40), col=(30, 50, 50), seed=x, depth=0.5)
    S.ground(g, Box(-2, 320, W + 2, H + 2), (70, 70, 60), "dirt", 2)
    # tents
    for x, c, key in ((170, (140, 110, 70), None), (650, (120, 90, 60), "tent")):
        cc = c if not (key and key in d) else (150, 60, 60)
        S.obj(g, Poly([(x - 90, 420), (x, 300), (x + 90, 420)]), cc, 3 + x, "fabric")
        S.obj(g, Poly([(x - 20, 420), (x, 360), (x + 20, 420)]), (40, 30, 30), 4 + x)
        S.line(g, x, 300, x, 284, 2, (110, 80, 50))
    # totem (original carved post)
    tx = 420
    S.obj(g, Box(tx - 20, 250, tx + 20, 420), (130, 90, 50), 5, "wood")
    for y, c in ((270, (200, 60, 50)), (320, (60, 140, 200)), (370, (230, 190, 60))):
        S.obj(g, Ell(tx, y, 24, 18), c, 6 + y, hi=True)
        S.flat(g, Circ(tx - 8, y - 4, 3), INK)
        S.flat(g, Circ(tx + 8, y - 4, 3), INK)
    if "wings" not in d:
        S.obj(g, Union([Poly([(tx - 20, 262), (tx - 70, 240), (tx - 20, 280)]), Poly([(tx + 20, 262), (tx + 70, 240), (tx + 20, 280)])]), (230, 190, 60), 9)
    # cage
    S.obj(g, Box(760, 380, 860, 470, 3), (60, 50, 50), 10)
    g.fill(Box(764, 384, 856, 466), (30, 24, 30))
    g.fill(Union([Box(x, 380, x + 3, 470) for x in range(766, 860, 14 if "cage" not in d else 24)]), (140, 140, 150))
    # campfire with goblins
    S.obj(g, Union([Seg(430, 520, 490, 500, 6), Seg(490, 520, 430, 500, 6)]), (110, 70, 40), 11, "wood")
    S.glow(g, 460, 480, 160, (255, 150, 60), 0.5)
    goblin(S, g, 330, 560, 120, face=1, seed=12)
    goblin(S, g, 590, 560, 130, face=-1, seed=13, cloth=(120, 90, 60) if "vest" not in d else (60, 90, 150))
    # heroes hiding behind rocks (left foreground)
    rock(S, g, 120, 600, 90, col=(110, 106, 110), seed=15)
    adventurer(g, 90, 520, 170, kind="fighter", face=1, seed=16, weapon=False)
    rock(S, g, 70, 610, 70, col=(100, 96, 100), seed=17)
    if "barrel" not in d:
        barrel(S, g, 720, 520, seed=18)


L1608_EL = [E("fire", el(lambda g, m: S.obj(g, Union([Ell(460, 502, 26, 10), Poly([(436, 504), (450, 450), (462, 476), (474, 440), (486, 504)])]), (255, 170, 60), 30, line=False)),
              pivot=(460, 510), daynight="untinted", anim=dict(stretch=(0.06, 0.25), scaleSpeed=2.2)),
            sparkle_el("stars", [(100, 60), (300, 40), (520, 80), (860, 50)], col=(255, 255, 230), r=4, speed=0.5),
            E("sparks", el(lambda g, m: [g.glow(460 + k * 8, 440 - k * 10, 2.4, (255, 200, 100), 1.0) for k in range(4)]), daynight="untinted",
              anim=dict(driftVelocity=(4, 60), driftLength=80, driftFade=True))]
L1608_DIFFS = [("tent", 650, 360, 0), ("wings", 420, 256, 0), ("cage", 810, 425, 0), ("vest", 590, 470, 0), ("barrel", 720, 500, 0)]


# =================================================================== Level 1609 wizard's tower study
def l1609(g, d):
    S.obj(g, Box(-2, -2, W + 2, 450), (110, 100, 120), 1, "stone", line=False)
    S.obj(g, Union([Box(340, 60, 560, 260), Circ(450, 60, 110) & Box(340, -60, 560, 60)]), (40, 50, 110), 2)
    for x, y, r in ((380, 110, 3), (420, 80, 2), (500, 120, 3), (470, 190, 2), (520, 70, 2), (400, 200, 3)):
        S.flat(g, Circ(x, y, r), (255, 250, 210))
    if "moon" not in d:
        S.obj(g, Circ(470, 140, 18), (240, 240, 220), 3, hi=True)
    g.fill(Union([Box(448, -50, 452, 260), Box(340, 158, 560, 162)]), (60, 50, 50))
    # bookshelves both sides
    rnd = random.Random(1609)
    for x0, x1 in ((20, 300), (600, 880)):
        S.obj(g, Box(x0, 60, x1, 440), (110, 70, 40), 4 + x0, "wood")
        for y in (90, 180, 270, 360):
            x = x0 + 12
            while x < x1 - 20:
                w = rnd.uniform(10, 18)
                S.obj(g, Box(x, y, x + w, y + 70), [(160, 40, 40), (40, 80, 140), (60, 120, 70), (200, 160, 60), (110, 60, 130)][rnd.randrange(5)], 5, line=True)
                x += w + 1
            S.obj(g, Box(x0, y + 70, x1, y + 80), (130, 90, 50), 6, "wood")
    # star chart on the wall (right shelf top)
    S.obj(g, Box(640, 4, 840, 52, 2), (230, 220, 180) if "chart" not in d else (200, 220, 240), 7)
    for x, y in ((670, 20), (700, 36), (740, 16), (780, 30), (810, 18)):
        S.flat(g, Circ(x, y, 3), INK)
    g.fill(Seg(670, 20, 700, 36, 1), INK)
    g.fill(Seg(700, 36, 740, 16, 1), INK)
    # floor and rug
    S.ground(g, Box(-2, 440, W + 2, H + 2), (100, 80, 70), "stone", 8)
    S.obj(g, Ell(450, 540, 300, 50), (130, 40, 60), 9, "fabric")
    S.flat(g, Diff(Ell(450, 540, 280, 42), Ell(450, 540, 270, 38)), (230, 190, 70))
    # cauldron
    S.obj(g, Union([Ell(250, 500, 70, 50), Box(186, 460, 314, 476)]), (40, 40, 46), 10, hi=True)
    S.obj(g, Ell(250, 466, 60, 12), (90, 220, 120) if "brew" not in d else (220, 90, 200), 11)
    S.glow(g, 250, 460, 80, (120, 250, 150) if "brew" not in d else (240, 120, 230), 0.3)
    # desk with crystal ball, candle, scroll
    S.obj(g, Box(540, 430, 820, 450, 3), (130, 90, 50), 12, "wood")
    for x in (560, 800):
        S.obj(g, Box(x - 8, 450, x + 8, 560), (110, 70, 40), 13, "wood")
    S.obj(g, Box(610, 410, 650, 430, 3), (200, 160, 60), 14)
    S.glow(g, 630, 380, 60, (180, 140, 255), 0.4)
    S.obj(g, Circ(630, 384, 28), (180, 140, 255), 15, hi=True)
    S.obj(g, Union([Box(740, 400, 760, 430), Ell(750, 400, 10, 3)]), (250, 245, 230), 16)
    if "scroll" not in d:
        S.obj(g, Box(680, 418, 724, 430, 5), (240, 220, 170), 17)
    # owl on the shelf top
    if "owl" not in d:
        S.obj(g, Union([Ell(150, 36, 22, 28), Poly([(132, 14), (138, 4), (146, 14)]), Poly([(154, 14), (162, 4), (168, 14)])]), (150, 110, 70), 18, hi=True)
        for ex in (142, 158):
            S.flat(g, Circ(ex, 28, 7), (255, 230, 90))
            S.flat(g, Circ(ex, 28, 3), INK)
    adventurer(g, 420, 600, 260, kind="wizard", face=1, seed=19, beard=True, main=(70, 50, 140))


L1609_EL = [E("bubbles", el(lambda g, m: [S.obj(g, Circ(230 + k * 18, 456 - k * 10, 5 - k), (120, 250, 160), 40 + k, line=True) for k in range(3)]),
              daynight="untinted", anim=dict(driftVelocity=(0, 40), driftLength=40, driftFade=True)),
            sparkle_el("magic", [(630, 360), (600, 400), (660, 370)], col=(220, 200, 255), r=5, speed=0.8),
            E("flame", el(lambda g, m: S.obj(g, Union([Ell(750, 394, 4, 5), Poly([(746, 394), (750, 380), (754, 394)])]), (255, 190, 80), 50, line=False)),
              pivot=(750, 398), daynight="untinted", anim=dict(stretch=(0.06, 0.25), scaleSpeed=2.0))]
L1609_DIFFS = [("moon", 470, 140, 0), ("chart", 740, 28, 0), ("brew", 250, 466, 0), ("scroll", 702, 424, 0), ("owl", 150, 30, 0)]


# =================================================================== Level 1610 troll under the bridge
def l1610(g, d):
    S.sky(g, [(0, (110, 170, 230)), (300, (220, 236, 250))])
    S.obj(g, cloud_shape(200, 80, 90, 24, 1), (255, 255, 255), 1, "cloud", line=False)
    for x in range(-20, 920, 60):
        round_tree(S, g, x, 260 + (x * 13 % 30), 140, col=(70, 140, 80), seed=x, depth=0.4)
    S.ground(g, Under(wave(250, 10, 90, 2), -20, W + 20), (110, 180, 90), "grass", 2)
    S.water(g, Box(-2, 420, W + 2, H + 2), (90, 160, 210), (50, 110, 180), 3)
    # banks
    S.ground(g, Poly([(-20, 300), (200, 300), (260, 440), (-20, 440)]), (120, 110, 90), "dirt", 4, line=True)
    S.ground(g, Poly([(920, 300), (700, 300), (640, 440), (920, 440)]), (120, 110, 90), "dirt", 5, line=True)
    # troll in the shadow under the arch
    g.fill(Box(240, 330, 660, 460), (30, 30, 40))
    troll(g, 420, 470, 200, face=1, seed=6, club="club" not in d, cloth=(120, 90, 60) if "belt" not in d else (60, 90, 160))
    # stone bridge
    S.obj(g, Diff(Box(180, 250, 720, 340), Union([Box(240, 330, 660, 400), Ell(450, 330, 210, 90) & Box(240, 240, 660, 330)])), (170, 160, 150), 7, "stone")
    S.obj(g, Box(170, 236, 730, 256, 3), (190, 180, 170), 8, "stone")
    for x in range(190, 720, 46):
        if "post" in d and x == 466:
            continue
        S.obj(g, Box(x, 206, x + 16, 240, 2), (180, 170, 160), 9 + x, "stone")
    # the party crossing
    adventurer(g, 330, 240, 150, kind="fighter", face=1, seed=10, shield=(60, 90, 170))
    adventurer(g, 420, 240, 140, kind="cleric", face=1, seed=11)
    adventurer(g, 520, 240, 146, kind="wizard", face=1, seed=12, main=(60, 60, 160) if "hat" not in d else (160, 60, 60))
    # reeds and a lily pad
    for x in (60, 80, 100, 820, 840):
        S.line(g, x, 470, x + 4, 400, 2, (80, 130, 60))
        S.obj(g, Ell(x + 4, 400, 4, 12), (130, 90, 50), x)
    if "frog" not in d:
        S.obj(g, Ell(740, 520, 30, 8), (90, 170, 80), 13)
        S.obj(g, Union([Ell(744, 508, 12, 9), Circ(738, 500, 4), Circ(750, 500, 4)]), (110, 200, 90), 14, hi=True)
    burst(g, 640, 120, 30, col=(255, 230, 80), seed=15)


L1610_EL = [sparkle_el("water", [(120, 520), (520, 560), (820, 500)], r=5, speed=0.6),
            E("cl", el(lambda g, m: S.obj(g, cloud_shape(620, 60, 70, 18, 3), (255, 255, 255), 3, "cloud", line=False)), anim=dict(bobAmplitude=(40, 0), bobSpeed=0.04))]
L1610_DIFFS = [("club", 520, 270, 0), ("belt", 420, 403, 0), ("post", 474, 222, 0), ("hat", 512, 52, 0), ("frog", 742, 508, 0)]


# =================================================================== Level 1611 spider cavern
def l1611(g, d):
    S.obj(g, Box(-2, -2, W + 2, H + 2), (40, 40, 60), 1, "stone", line=False)
    S.obj(g, Poly([(-20, -2), (920, -2), (920, 150), (700, 90), (520, 160), (300, 80), (100, 140), (-20, 90)]), (28, 28, 44), 2, "stone")
    S.ground(g, Under(wave(470, 14, 80, 3), -20, W + 20), (70, 66, 80), "stone", 3, line=True)
    # webs in the corners and across
    web(g, -2, -2, 220, (1, 1))
    web(g, 902, -2, 200, (-1, 1))
    if "web" not in d:
        web(g, 300, 470, 140, (1, -1))
    # glowing crystal clusters
    for x, base, col, key in ((120, 490, (120, 220, 255), None), (780, 480, (230, 120, 250), "crystal")):
        c = col if not (key and key in d) else (120, 250, 160)
        S.glow(g, x, base - 40, 90, c, 0.35)
        for k, (h, tl) in enumerate(((80, -0.3), (110, 0.0), (70, 0.35))):
            crystal(S, g, x + (k - 1) * 26, base, h, c, seed=x + k, tilt=tl)
    # web bundles hanging (just silk wrappings)
    for x, y, key in ((560, 120, None), (640, 90, "bundle")):
        if key and key in d:
            continue
        g.fill(Seg(x, 0, x, y - 30, 1), (240, 240, 250))
        S.obj(g, Ell(x, y, 18, 34), (230, 230, 236), x, hi=True)
        for k in range(4):
            g.fill(Seg(x - 18, y - 20 + k * 12, x + 18, y - 14 + k * 12, 1), (200, 200, 210))
    # the giant spider descending on its thread
    g.fill(Seg(430, 0, 430, 200, 1.4), (240, 240, 250))
    spider(g, 430, 240, 1.2, seed=4, mark=(230, 60, 60) if "mark" not in d else (250, 220, 60))
    # the adventurer with a lantern and shield
    adventurer(g, 620, 600, 240, kind="fighter", face=-1, seed=5, shield=(170, 50, 50) if "shield" not in d else (60, 90, 170))
    lx, ly = 690, 420
    S.glow(g, lx, ly, 120, (255, 210, 120), 0.4)
    S.obj(g, Box(lx - 12, ly - 16, lx + 12, ly + 16, 3), (255, 220, 140), 6)
    g.fill(Seg(lx, ly - 16, lx - 20, ly - 40, 1.6), INK)
    for x, y, r in ((240, 560, 40), (860, 580, 50)):
        rock(S, g, x, y, r, col=(90, 86, 100), seed=x)


L1611_EL = [sparkle_el("glim", [(120, 420), (780, 410), (300, 300), (850, 300)], col=(200, 230, 255), r=5, speed=0.6),
            E("drip", el(lambda g, m: S.obj(g, Ell(200, 160, 3, 6), (150, 200, 230), 1, line=False)),
                                                                   daynight="untinted", anim=dict(driftVelocity=(0, -140), driftLength=320, driftFade=True))]
L1611_DIFFS = [("web", 360, 410, 0), ("crystal", 780, 430, 0), ("bundle", 640, 90, 0), ("mark", 430, 279, 0), ("shield", 668, 410, 0)]


# =================================================================== Level 1612 jungle temple ruins
def l1612(g, d):
    S.sky(g, [(0, (120, 190, 220)), (300, (220, 240, 230))])
    for x in range(-20, 920, 50):
        round_tree(S, g, x, 280 + (x * 11 % 40), 180, col=(50, 120, 70), seed=x, depth=0.5)
    # stepped temple
    col = (160, 150, 120)
    for i in range(5):
        w = 520 - i * 90
        S.obj(g, Box(450 - w / 2, 420 - (i + 1) * 50, 450 + w / 2, 420 - i * 50), col, 2 + i, "stone")
    S.obj(g, Box(400, 120, 500, 170), col, 8, "stone")
    S.obj(g, Union([Box(424, 130, 476, 170), Circ(450, 130, 26) & Box(424, 100, 476, 130)]), (30, 26, 24), 9)
    # golden idol in the shrine
    if "idol" not in d:
        S.glow(g, 450, 146, 40, (255, 220, 100), 0.4)
        S.obj(g, Union([Ell(450, 140, 12, 14), Box(440, 150, 460, 168, 3)]), (250, 210, 60), 10, hi=True)
    # stairs up the middle
    for k in range(10):
        y = 420 - k * 25
        S.obj(g, Box(410 - k * 2, y - 25, 490 + k * 2, y), mixc(col, (255, 255, 255), 0.1), 11 + k, "stone")
    # vines
    for x, ln in ((250, 120), (330, 80), (620, 140), (700, 90)):
        S.obj(g, Seg(x, 230, x + 6, 230 + ln, 3), (60, 130, 60), x)
        for k in range(4):
            S.obj(g, Ell(x + (k % 2) * 8, 250 + k * ln / 4, 7, 4), (70, 150, 70), x + k)
    # guardian statues flanking
    for x, f in ((170, 1), (730, -1)):
        S.obj(g, Box(x - 40, 400, x + 40, 440), col, x, "stone")
        S.obj(g, Union([Ell(x, 360, 34, 40), Circ(x + f * 20, 310, 26), Poly([(x + f * 34, 300), (x + f * 70, 310), (x + f * 36, 320)])]), (140, 150, 120), x + 1, "stone")
        S.obj(g, Circ(x + f * 28, 304, 10), (60, 200, 120) if not (x == 730 and "gem" in d) else (230, 60, 60), x + 2, hi=True)
    S.ground(g, Box(-2, 440, W + 2, H + 2), (100, 140, 80), "grass", 12)
    # adventurers and a rope bridge post
    adventurer(g, 300, 600, 230, kind="rogue", face=1, seed=13)
    adventurer(g, 600, 600, 240, kind="cleric", face=-1, seed=14, main=(230, 220, 200) if "robe" not in d else (200, 220, 240))
    if "parrot" not in d:
        S.obj(g, Union([Ell(820, 120, 14, 20), Circ(826, 96, 10), Poly([(816, 136), (806, 170), (822, 140)])]), (230, 50, 50), 15, hi=True)
        S.flat(g, Poly([(834, 94), (846, 100), (834, 104)]), (250, 220, 60))
    bush(S, g, 80, 560, 60, (60, 140, 70), seed=16)


L1612_EL = [sparkle_el("idol", [(450, 140)], col=(255, 250, 200), r=8, speed=0.5),
            E("butterfly", el(lambda g, m: S.obj(g, Union([Ell(560, 300, 8, 6), Ell(572, 300, 8, 6)]), (90, 160, 250), 1, line=True)), pivot=(566, 300),
              anim=dict(stretch=(0.6, 0), scaleSpeed=3.0, bobAmplitude=(30, 20), bobSpeed=0.15))]
L1612_DIFFS = [("idol", 450, 150, 0), ("gem", 702, 304, 0), ("robe", 600, 480, 0), ("parrot", 822, 120, 0)]


# =================================================================== Level 1613 fantasy market
def stall(g, x0, x1, base, roof_col, seed, stripe=(250, 250, 240)):
    S.obj(g, Box(x0, base - 70, x1, base, 2), (150, 100, 60), seed, "wood")
    for x in (x0 + 4, x1 - 10):
        S.obj(g, Box(x, base - 170, x + 6, base - 70), (120, 80, 50), seed + 1, "wood")
    aw = Poly([(x0 - 10, base - 160), (x1 + 10, base - 160), (x1 + 20, base - 120), (x0 - 20, base - 120)])
    S.obj(g, aw, roof_col, seed + 2, "fabric")
    for k in range(int((x1 - x0) / 40)):
        g.fill(Inter(Box(x0 + k * 40, base - 170, x0 + k * 40 + 20, base - 110), aw), stripe)


def l1613(g, d):
    S.sky(g, [(0, (110, 180, 240)), (300, (230, 240, 250))])
    castle(S, g, 450, 220, 360, 200, (220, 210, 200), (90, 100, 170), seed=1, depth=0.4, flags=((200, 50, 60), (200, 50, 60)))
    for x0, x1, top, c in ((-20, 160, 120, (230, 210, 180)), (740, 920, 140, (220, 200, 170))):
        S.obj(g, Box(x0, top, x1, 330), c, x0, "stone")
        S.obj(g, Poly([(x0 - 10, top), ((x0 + x1) / 2, top - 70), (x1 + 10, top)]), (170, 80, 60), x0 + 1, "roof")
    S.obj(g, Union([Box(80, 250, 124, 330), Circ(102, 250, 22) & Box(80, 228, 124, 250)]), (110, 70, 40) if "door" not in d else (60, 110, 160), 40, "wood")
    S.ground(g, Box(-2, 320, W + 2, H + 2), (190, 170, 140), "dirt", 2)
    # potion stall (left)
    stall(g, 40, 300, 460, (60, 90, 170), 3)
    for k, c in enumerate(((220, 50, 60), (60, 200, 120), (90, 140, 240), (240, 200, 60), (200, 90, 200))):
        if "potion" in d and k == 2:
            continue
        potion(S, g, 70 + k * 50, 390, c, s=1.2, seed=4 + k)
    # weapon stall (right) with swords and shields
    stall(g, 600, 860, 460, (170, 50, 50), 10)
    for k in range(3):
        x = 640 + k * 60
        S.obj(g, Poly([(x - 3, 390), (x + 3, 390), (x + 3, 300), (x, 290), (x - 3, 300)]), (220, 225, 235), 11 + k, hi=True)
        S.obj(g, Box(x - 12, 384, x + 12, 390), (200, 160, 60), 14 + k)
    S.obj(g, Union([Box(800, 320, 840, 350), Inter(Circ(800, 350, 40), Circ(840, 350, 40)) & Box(800, 350, 840, 390)]),
          (60, 90, 170) if "shield" not in d else (60, 150, 80), 17, hi=True)
    # fruit cart in the middle
    S.obj(g, Box(380, 430, 520, 480, 3), (150, 100, 60), 18, "wood")
    for k in range(6):
        S.obj(g, Circ(396 + k * 22, 424, 11), (230, 60, 60) if k % 2 else (250, 180, 60), 19 + k, hi=True)
    S.obj(g, Circ(400, 500, 22), (110, 70, 40), 26, "wood")
    S.obj(g, Circ(500, 500, 22), (110, 70, 40), 27, "wood")
    banner(S, g, 450, 300, 50, 90, (200, 50, 60) if "banner" not in d else (60, 140, 90), emblem="star", seed=28)
    # townsfolk and adventurers
    adventurer(g, 150, 600, 220, kind="wizard", face=1, seed=29)
    adventurer(g, 340, 600, 210, kind="fighter", main=(120, 140, 70), trim=(200, 180, 140), face=1, seed=30, weapon=False)
    adventurer(g, 600, 600, 230, kind="rogue", face=-1, seed=31)
    adventurer(g, 780, 600, 220, kind="fighter", face=-1, seed=32, shield=(170, 50, 50))
    if "cat" not in d:
        S.obj(g, Union([Ell(470, 560, 22, 12), Circ(494, 548, 9), Poly([(488, 542), (490, 532), (496, 540)]), Poly([(498, 540), (502, 532), (504, 542)]),
                        Seg(448, 556, 436, 536, 3)]), (240, 150, 60), 33, hi=True)


L1613_EL = [E("birds", el(lambda g, m: [g.fill(Union([Seg(x - 7, y - 3, x, y, 1.6), Seg(x, y, x + 7, y - 3, 1.6)]), INK) for x, y in ((600, 60), (620, 54))]),
              anim=dict(bobAmplitude=(40, 6), bobSpeed=0.05))]
L1613_DIFFS = [("door", 102, 282, 0), ("potion", 170, 372, 0), ("shield", 820, 350, 0), ("banner", 450, 340, 0), ("cat", 474, 552, 0)]


# =================================================================== Level 1614 stone giant on a mountain pass
def l1614(g, d):
    S.sky(g, [(0, (110, 150, 210)), (300, (220, 230, 245))])
    for ax, ay, xl, xr in ((200, 60, -60, 460), (700, 40, 420, 980)):
        S.obj(g, Poly([(xl, 360), (ax, ay), (xr, 360)]), (150, 160, 190), ax, "stone", depth=0.3)
        S.flat(g, Poly([(ax - (ax - xl) * 0.25, ay + (360 - ay) * 0.25), (ax, ay), (ax + (xr - ax) * 0.25, ay + (360 - ay) * 0.25), (ax, ay + (360 - ay) * 0.32)]), (250, 252, 255))
    S.ground(g, Under(wave(380, 16, 90, 5), -20, W + 20), (230, 236, 248), "snow", 2, line=True)
    # the stone giant (right)
    gx, gb = 640, 500
    S.obj(g, Union([Box(gx - 70, gb - 200, gx + 70, gb - 60, 30), Box(gx - 60, gb - 70, gx - 10, gb, 10), Box(gx + 10, gb - 70, gx + 60, gb, 10)]), (130, 126, 120), 3, "stone", hi=True)
    S.obj(g, Union([Seg(gx - 70, gb - 180, gx - 120, gb - 80, 26), Seg(gx + 70, gb - 180, gx + 130, gb - 260, 26)]), (130, 126, 120), 4, "stone")
    S.obj(g, Rough(Ell(gx, gb - 240, 46, 40), 5, 10, 5), (140, 136, 130), 5, "stone", hi=True)
    for ex in (-16, 14):
        S.glow(g, gx + ex, gb - 244, 18, (120, 220, 255) if "eyes" not in d else (255, 140, 60), 0.6)
        S.obj(g, Ell(gx + ex, gb - 244, 11, 7), (200, 240, 255) if "eyes" not in d else (255, 190, 100), 20 + ex)
    if "moss" not in d:
        S.obj(g, Rough(Ell(gx - 20, gb - 196, 44, 12), 3, 6, 6), (90, 140, 70), 6, "foliage")
    if "boulder" not in d:
        rock(S, g, gx + 140, gb - 250, 40, col=(150, 146, 140), seed=7)
    # pine trees with snow
    for x in (60, 130, 860):
        pine_tree(S, g, x, 440, 150, seed=x, snow=(250, 252, 255))
    # the party with shields raised
    adventurer(g, 220, 600, 230, kind="fighter", face=1, seed=8, shield=(60, 90, 170), main=(160, 40, 40) if "cape" not in d else (60, 120, 90))
    adventurer(g, 330, 600, 220, kind="cleric", face=1, seed=9, shield=(220, 200, 80))
    adventurer(g, 110, 600, 210, kind="wizard", face=1, seed=10)
    burst(g, 470, 300, 36, col=(255, 230, 90), seed=11)


L1614_EL = [E("snow", el(lambda g, m: [S.obj(g, Circ(x, y, 3), (255, 255, 255), 1, line=False) for x, y in ((100, 40), (300, 80), (500, 30), (700, 100), (860, 60), (420, 160))]),
              anim=dict(driftVelocity=(-6, -40), driftLength=200, driftFade=True)),
            E("pebbles", el(lambda g, m: [S.obj(g, Circ(780 + k * 10, 200 + k * 14, 4), (140, 136, 130), 2) for k in range(3)]), anim=dict(driftVelocity=(10, -60), driftLength=80, driftFade=True))]
L1614_DIFFS = [("eyes", 640, 256, 0), ("moss", 620, 304, 0), ("boulder", 780, 228, 0), ("cape", 210, 410, 0)]

LEVELS = [
    ("Level1605", "冒险者酒馆", make(l1605), L1605_EL, L1605_DIFFS, 60, OPTS),
    ("Level1606", "地牢走廊", make(l1606), L1606_EL, L1606_DIFFS, 60, OPTS),
    ("Level1607", "巨龙宝藏", make(l1607), L1607_EL, L1607_DIFFS, 60, OPTS),
    ("Level1608", "哥布林营地", make(l1608), L1608_EL, L1608_DIFFS, 60, OPTS),
    ("Level1609", "法师塔书房", make(l1609), L1609_EL, L1609_DIFFS, 60, OPTS),
    ("Level1610", "巨魔石桥", make(l1610), L1610_EL, L1610_DIFFS, 60, OPTS),
    ("Level1611", "蛛网洞窟", make(l1611), L1611_EL, L1611_DIFFS, 60, OPTS),
    ("Level1612", "丛林遗迹", make(l1612), L1612_EL, L1612_DIFFS, 60, OPTS),
    ("Level1613", "奇幻集市", make(l1613), L1613_EL, L1613_DIFFS, 60, OPTS),
    ("Level1614", "巨人山口", make(l1614), L1614_EL, L1614_DIFFS, 60, OPTS),
]
