# -*- coding: utf-8 -*-
"""Mixed themes part 1 (paper-craft side views, full-bleed, original designs, no brands):
  Level235 海底世界 - a coral reef: light rays, sunken ship, treasure chest, turtle, fish shoals, diver
  Level236 热带雨林 - a rainforest gorge: waterfall, giant leaves, toucan, monkey, frog, explorer's canoe
  Level237 古埃及   - the Nile in ancient Egypt: pyramids, obelisk, temple columns, felucca, camels, builders
  Level238 极地冰原 - an Arctic bay: aurora, icebergs, research hut, polar bears, seals, dog sled
  Level239 秋日果园 - an autumn orchard: apple trees, barn, ladder picker, baskets, tractor, pumpkins
  Level240 夜市小吃街 - a night food market: lantern strings, stalls with steam, signs, tables, crowd
  Level241 太空站内部 - inside a space station module: Earth window, floating crew, hydroponics, screens
  Level242 糖果王国 - a candy kingdom: gumdrop castle, lollipop trees, chocolate river, gingerbread house
  Level243 恐龙时代 - the age of dinosaurs: volcano, ferns, long-necks, horned dinos, nest, pterosaurs
  Level244 热气球节 - a hot-air balloon festival: balloons over the meadow, crews, tents, spectators
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bubble, bubbles_el, bush, cloud_bg, cloud_el, drift_across, fish, layer, palm, rock, sky,
                 smoke_el, tree_pine, tree_round)
from fills import far_forest, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_festival import crowd_row, npiece, string_lights, lights_el
from levels_homes import steam

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def balloon(c, x, y, r, cols, basket=(150, 100, 60), stripes=6):
    """Hot-air balloon: envelope with vertical gores, ropes and basket (y = envelope centre)."""
    piece(c, [Ell(x, y, r, r * 1.1), Poly([(x - r * 0.62, y + r * 0.8), (x + r * 0.62, y + r * 0.8), (x + r * 0.22, y + r * 1.35), (x - r * 0.22, y + r * 1.35)])],
          cols[0], border=1.5, shadow=PROP)
    for k in range(1, stripes, 2):
        t = k / stripes
        rx = r * abs(math.cos(math.pi * t))
        cx = x + r * -math.cos(math.pi * t) * 0.5
        flat(c, Ell(cx, y, max(rx * 0.35, r * 0.12), r * 1.06), cols[1])
    flat(c, [Thick(x - r * 0.22, y + r * 1.35, x - r * 0.18, y + r * 1.6, 1.2), Thick(x + r * 0.22, y + r * 1.35, x + r * 0.18, y + r * 1.6, 1.2)], (90, 80, 70))
    piece(c, RRect(x - r * 0.22, y + r * 1.58, x + r * 0.22, y + r * 1.82, 2), basket, border=1, shadow=SMALL)


def lantern(c, x, y, s, col, tassel=(250, 200, 60), pk=None):
    (pk or piece)(c, [Ell(x, y, 14 * s, 11 * s), RRect(x - 7 * s, y - 14 * s, x + 7 * s, y - 9 * s, 1), RRect(x - 7 * s, y + 9 * s, x + 7 * s, y + 14 * s, 1)], col,
                  shadow=SMALL)
    flat(c, [Thick(x - 8 * s, y - 8 * s, x - 8 * s, y + 8 * s, 1.2), Thick(x + 8 * s, y - 8 * s, x + 8 * s, y + 8 * s, 1.2)], lit(col, 0.75))
    flat(c, Thick(x, y + 14 * s, x, y + 24 * s, 2 * s), tassel)


def fern(c, x, base, s, col):
    for a in (-60, -35, -12, 12, 35, 60):
        r = math.radians(a - 90)
        ex, ey = x + 60 * s * math.cos(r), base + 60 * s * math.sin(r) * 0.9
        piece(c, Poly([(x, base), (ex - 8 * s * math.sin(r), ey), (ex, ey), (x + 4 * s, base)]), col, shadow=SMALL)
        flat(c, Thick(x, base, ex, ey, 1.4), lit(col, 0.8))


def big_leaf(c, x, y, ang, length, col):
    a = math.radians(ang)
    ex, ey = x + math.cos(a) * length, y + math.sin(a) * length
    nx, ny = -math.sin(a) * length * 0.28, math.cos(a) * length * 0.28
    mx, my = (x + ex) / 2, (y + ey) / 2
    piece(c, Poly([(x, y), (mx + nx, my + ny), (ex, ey), (mx - nx, my - ny)]), col, shadow=PROP)
    flat(c, Thick(x, y, ex, ey, 1.6), lit(col, 1.2))


# =================================================================== Level 235 coral reef
def coral(c, x, base, s, col, kind="branch"):
    if kind == "branch":
        piece(c, [Thick(x, base, x, base - 50 * s, 6 * s), Thick(x, base - 20 * s, x - 22 * s, base - 50 * s, 5 * s), Thick(x, base - 30 * s, x + 20 * s, base - 64 * s, 5 * s),
                  Thick(x - 22 * s, base - 50 * s, x - 30 * s, base - 62 * s, 4 * s), Thick(x, base - 50 * s, x + 6 * s, base - 72 * s, 4 * s)], col, shadow=SMALL)
    elif kind == "fan":
        piece(c, [Ell(x, base - 34 * s, 32 * s, 30 * s), RRect(x - 3 * s, base - 10 * s, x + 3 * s, base, 1)], col, shadow=SMALL)
        for a in range(-60, 61, 20):
            r = math.radians(a - 90)
            flat(c, Thick(x, base - 6 * s, x + 28 * s * math.cos(r), base - 34 * s + 28 * s * math.sin(r), 1.2), lit(col, 0.8))
    else:   # brain
        piece(c, Ell(x, base - 16 * s, 30 * s, 18 * s), col, shadow=SMALL)
        for k in range(4):
            flat(c, Thick(x - 22 * s + k * 14 * s, base - 26 * s, x - 16 * s + k * 14 * s, base - 6 * s, 1.4), lit(col, 0.8))


def seaweed(c, x, base, h, col):
    pts = []
    for k in range(9):
        t = k / 8
        pts.append((x + 8 * math.sin(t * 6), base - h * t))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        piece(c, Thick(x0, y0, x1, y1, 7), col, shadow=None)


def l235_bg(c, d):
    c.gradient(0, H, (90, 180, 220), (30, 90, 150))
    # surface ripples + boat hull above
    flat(c, RRect(0, 0, W, 18, 0), (150, 210, 240))
    for x in range(0, W, 50):
        flat(c, Ell(x + 25, 18, 25, 5), (150, 210, 240))
    hull = (200, 70, 60) if "boat" not in d else (250, 200, 60)
    piece(c, Poly([(700, 0), (880, 0), (860, 34), (720, 34)]), hull, border=1.5, shadow=PROP)
    flat(c, Thick(796, 34, 796, 70, 1.4), (230, 230, 230))
    # light rays
    for k, x in enumerate((140, 330, 520, 690)):
        soft_union(c, [Poly([(x, 0), (x + 40, 0), (x + 120, 420), (x + 40, 420)])], (220, 246, 255), 0.12, spread=16)
    # distant reef silhouette
    piece(c, hill_strip(380, [(30, 0.01, 0.3), (14, 0.03, 2.0)]), (60, 120, 160), shadow=LAYER)
    # sunken ship (right)
    piece(c, Poly([(560, 470), (840, 440), (880, 380), (600, 400)]), (110, 80, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(600, 420, 860, 400, 3)], (90, 64, 56))
    for x in (640, 700, 760):
        flat(c, Circ(x, 430 - (x - 600) * 0.1, 7), (40, 60, 80))
    piece(c, [Thick(700, 400, 740, 220, 6), Thick(708, 300, 790, 286, 4)], (120, 90, 74), shadow=PROP)
    flag = (220, 60, 60) if "flag" not in d else (60, 200, 140)
    piece(c, Poly([(738, 226), (778, 236), (736, 252)]), flag, shadow=SMALL)
    # sand floor
    piece(c, hill_strip(470, [(16, 0.008, 1.0), (8, 0.03, 0.4)]), (230, 210, 160), shadow=LAYER)
    rnd = random.Random(2351)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(500, 600)
        flat(c, Circ(x, y, rnd.uniform(1.2, 2.4)), (210, 190, 140))
    # corals
    coral(c, 60, 540, 1.6, (240, 110, 130) if "coral" not in d else (250, 170, 60), "branch")
    coral(c, 180, 520, 1.3, (250, 180, 80), "fan")
    coral(c, 330, 560, 1.2, (170, 110, 200), "brain")
    coral(c, 560, 560, 1.4, (240, 120, 100), "fan")
    coral(c, 880, 580, 1.4, (250, 200, 110), "branch")
    for x, h in ((250, 140), (420, 110), (500, 160), (820, 120)):
        seaweed(c, x, 600, h, (70, 160, 90))
    # treasure chest
    chest = (170, 110, 60) if "chest" not in d else (110, 110, 190)
    piece(c, [RRect(410, 500, 490, 546, 3), Poly([(410, 502), (490, 502), (482, 480), (418, 480)])], chest, border=1.5, shadow=PROP)
    flat(c, [RRect(410, 498, 490, 504, 0), RRect(444, 496, 456, 516, 1)], (240, 200, 70))
    flat(c, [Circ(430 + k * 10, 478 - (k % 2) * 4, 5) for k in range(5)], (250, 210, 80))
    # starfish + clam
    if "star" not in d:
        piece(c, Poly(star_pts(760, 560, 22, 9)), (240, 120, 60), shadow=SMALL)
    piece(c, [Ell(660, 566, 24, 12)], (220, 200, 230), shadow=SMALL)
    # turtle (left middle)
    shell = (110, 150, 80) if "turtle" not in d else (190, 120, 70)
    piece(c, [Ell(270, 300, 50, 26), Ell(330, 296, 14, 10), Ell(234, 320, 18, 7), Ell(300, 324, 18, 7), Ell(236, 280, 16, 6), Ell(304, 276, 18, 7)],
          (140, 190, 120), border=1.5, shadow=PROP)
    piece(c, Ell(268, 296, 40, 22), shell, shadow=None)
    for k in range(3):
        flat(c, Ell(244 + k * 24, 296, 9, 11), lit(shell, 1.2))
    flat(c, Circ(336, 292, 2), INK)
    # shoal of little fish (top left)
    for k, (x, y) in enumerate(((80, 120), (110, 100), (140, 126), (100, 146), (150, 92), (70, 160), (130, 160))):
        fish(c, x, y, 0.9, (250, 200, 60) if "shoal" not in d else (240, 120, 180), right=True)
    # big fish (centre top)
    fish(c, 450, 150, 2.4, (90, 160, 230), right=False, fin=(250, 200, 60))
    flat(c, [Thick(436, 136, 436, 164, 4), Thick(456, 134, 456, 166, 4)], (250, 250, 246))


L235_ELEMENTS = [
    E("jelly", lambda c, m: [piece(c, Ell(620, 140, 26, 20), (240, 180, 230, 0.85), shadow=None)] +
      [flat(c, Thick(604 + k * 8, 156, 600 + k * 9, 200, 1.6), (240, 190, 230)) for k in range(5)], pivot=(620, 160),
      anim=dict(bobAmplitude=(0, 16), bobSpeed=0.3, stretch=(0.05, 0.12), scaleSpeed=1.2)),
    E("diver", lambda c, m: [piece(c, [RRect(140, 380, 210, 400, 6), Circ(216, 386, 10)], (40, 40, 56), border=1.2, shadow=SMALL),
                             flat(c, Circ(218, 384, 6), (170, 220, 240)), piece(c, RRect(148, 370, 186, 380, 4), (250, 200, 60), shadow=None),
                             flat(c, [Poly([(140, 386), (112, 376), (116, 396)]), Poly([(140, 394), (112, 404), (116, 410)])], (250, 200, 60))],
      pivot=(170, 390), anim=dict(bobAmplitude=(30, 8), bobSpeed=0.2)),
    *bubbles_el("bub", 226, 376, n=4, r=4, rise=(2, 30), length=140),
    E("fish2", lambda c, m: fish(c, 760, 320, 1.4, (250, 140, 80), right=False), pivot=(760, 320), anim=dict(drift_across(740, 780, -18), bobAmplitude=(0, 6), bobSpeed=0.4)),
    E("weed", lambda c, m: seaweed(c, 120, 600, 120, (60, 150, 90)), pivot=(120, 600), anim=dict(swingAngle=4, swingSpeed=0.4)),
]

L235_DIFFS = [
    ("boat", 790, 20, 0),
    ("shoal", 110, 128, 0),
    ("turtle", 280, 300, 0),
    ("flag", 756, 238, 0),
    ("coral", 60, 500, 0),
    ("chest", 450, 512, 0),
    ("star", 760, 560, 0),
]


# =================================================================== Level 236 rainforest gorge
def toucan(c, x, y, s, beak):
    piece(c, [Ell(x, y, 14 * s, 20 * s), Circ(x + 4 * s, y - 20 * s, 10 * s)], (40, 40, 46), border=1.2, shadow=SMALL)
    flat(c, Ell(x + 6 * s, y - 14 * s, 7 * s, 8 * s), (250, 240, 200))
    piece(c, Poly([(x + 10 * s, y - 26 * s), (x + 44 * s, y - 20 * s), (x + 10 * s, y - 12 * s)]), beak, border=1, shadow=None)
    flat(c, Circ(x + 8 * s, y - 22 * s, 2 * s), (70, 160, 220))


def monkey(c, x, y, s, fur=(140, 90, 60)):
    piece(c, [Ell(x, y + 14 * s, 13 * s, 16 * s), Circ(x, y - 8 * s, 12 * s), Circ(x - 12 * s, y - 10 * s, 5 * s), Circ(x + 12 * s, y - 10 * s, 5 * s)], fur,
          border=1.2, shadow=SMALL)
    flat(c, Ell(x, y - 4 * s, 8 * s, 7 * s), (230, 196, 160))
    flat(c, [Circ(x - 4 * s, y - 8 * s, 1.6 * s), Circ(x + 4 * s, y - 8 * s, 1.6 * s)], INK)
    flat(c, [Thick(x - 10 * s, y + 4 * s, x - 20 * s, y - 24 * s, 3.4 * s), Thick(x + 10 * s, y + 20 * s, x + 28 * s, y + 30 * s, 3 * s)], fur)


def frog(c, x, y, s, col):
    piece(c, [Ell(x, y, 16 * s, 10 * s), Circ(x - 7 * s, y - 9 * s, 5 * s), Circ(x + 7 * s, y - 9 * s, 5 * s)], col, border=1.2, shadow=SMALL)
    flat(c, [Circ(x - 7 * s, y - 9 * s, 2.4 * s), Circ(x + 7 * s, y - 9 * s, 2.4 * s)], INK)
    flat(c, Thick(x - 6 * s, y + 2 * s, x + 6 * s, y + 2 * s, 1.2), lit(col, 0.6))


def l236_bg(c, d):
    sky(c, (170, 220, 200), (220, 240, 220), 200)
    far_forest(c, 160, 70, (110, 170, 130), 2361)
    # cliffs + waterfall
    piece(c, Poly([(300, 80), (420, 60), (430, 360), (290, 360)]), (110, 120, 110), shadow=LAYER)
    piece(c, Poly([(480, 60), (600, 80), (610, 360), (470, 360)]), (110, 120, 110), shadow=LAYER)
    flat(c, Poly([(420, 60), (480, 60), (480, 360), (420, 360)]), (200, 230, 246))
    for x in range(424, 480, 10):
        flat(c, Thick(x, 60, x, 360, 2), (230, 246, 255))
    soft_union(c, [Ell(450, 360, 80, 22)], (250, 252, 255), 0.6, spread=14)
    far_round_trees(c, 240, 30, (70, 140, 90), 2362)
    # mid jungle canopy
    piece(c, hill_strip(300, [(20, 0.02, 0.5), (12, 0.05, 1.0)], x0=-60, x1=300), (60, 130, 80), shadow=LAYER)
    piece(c, hill_strip(300, [(20, 0.02, 2.5), (12, 0.05, 3.0)], x0=600, x1=960), (60, 130, 80), shadow=LAYER)
    # river
    c.rect(0, 420, W, H, (80, 150, 150))
    flat(c, Poly([(380, 360), (520, 360), (700, 430), (200, 430)]), (100, 170, 170))
    for k in range(10):
        y = 440 + k * 16
        flat(c, Thick(30 + k * 40, y, 160 + k * 40, y, 1.6), (140, 200, 200))
    # banks with plants
    piece(c, Poly([(-10, 340), (300, 360), (240, 470), (-10, 520)]), (70, 140, 80), shadow=LAYER)
    piece(c, Poly([(910, 330), (620, 360), (680, 470), (910, 520)]), (70, 140, 80), shadow=LAYER)
    # giant tree trunk + branch (left)
    piece(c, [RRect(40, 0, 100, 420, 10), Thick(90, 120, 280, 100, 18)], (120, 90, 70), shadow=PROP)
    flat(c, [Thick(60, 0, 64, 420, 2), Thick(80, 40, 84, 400, 2)], (100, 74, 58))
    for k, x in enumerate((140, 200, 250)):
        flat(c, Thick(x, 108 - k * 2, x + 4 * k, 200 + k * 30, 2.4), (70, 130, 70))
    toucan(c, 180, 92, 1.4, (250, 150, 40) if "beak" not in d else (90, 200, 110))
    # vines + right tree with monkey
    piece(c, [RRect(800, 0, 850, 380, 10), Thick(820, 90, 640, 70, 14)], (120, 90, 70), shadow=PROP)
    if "monkey" not in d:
        monkey(c, 700, 100, 1.4)
    # orchid flower (centre top on cliff)
    orch = (240, 120, 200) if "orchid" not in d else (250, 220, 90)
    for a in range(5):
        r = math.radians(a * 72)
        piece(c, Ell(360 + 12 * math.cos(r), 150 + 12 * math.sin(r), 10, 7), orch, shadow=SMALL)
    flat(c, Circ(360, 150, 6), (250, 240, 120))
    big_leaf(c, 300, 180, 200, 70, (70, 150, 80))
    # giant flowers on the right bank
    fl = (230, 70, 60) if "flower" not in d else (250, 160, 220)
    for a in range(5):
        r = math.radians(a * 72 - 90)
        piece(c, Ell(760 + 26 * math.cos(r), 420 + 18 * math.sin(r), 20, 14), fl, shadow=SMALL)
        flat(c, Circ(760 + 26 * math.cos(r), 420 + 18 * math.sin(r), 4), lit(fl, 1.4))
    flat(c, Circ(760, 420, 14), (250, 230, 200))
    # frog on a lily pad
    flat(c, Ell(200, 470, 40, 12), (90, 170, 90))
    frog(c, 200, 462, 1.5, (90, 200, 90) if "frog" not in d else (60, 140, 230))
    # foreground leaves
    for x, y, a, l, col in ((-20, 600, -50, 140, (60, 130, 70)), (40, 610, -80, 120, (80, 160, 90)), (880, 610, -120, 140, (60, 130, 70)),
                            (920, 560, -150, 120, (80, 160, 90))):
        big_leaf(c, x, y, a, l, col)
    # explorer in a canoe
    canoe = (180, 110, 60) if "canoe" not in d else (220, 70, 70)
    piece(c, Poly([(380, 540), (580, 540), (560, 566), (400, 566)]), canoe, border=1.5, shadow=PROP)
    modern(c, 470, 546, (200, 180, 120), bottom=(120, 110, 80), hair=(90, 60, 40), h=1.4)
    piece(c, [Ell(472, 480, 22, 6), Ell(472, 472, 13, 9)], (220, 200, 140) if "hat" not in d else (240, 120, 60), shadow=SMALL)
    flat(c, Thick(420, 500, 520, 590, 3), (150, 100, 60))
    # parrot (right bank)
    par = (230, 60, 60) if "parrot" not in d else (60, 160, 230)
    piece(c, [Ell(830, 520, 14, 22), Circ(834, 494, 10), Poly([(824, 536), (840, 536), (836, 580)])], par, border=1.2, shadow=SMALL)
    flat(c, Ell(826, 522, 6, 14), (250, 210, 60))
    flat(c, Poly([(842, 492), (854, 498), (842, 502)]), (250, 240, 200))


L236_ELEMENTS = [
    E("bfly", lambda c, m: [piece(c, [Ell(540, 220, 9, 12), Ell(556, 220, 9, 12)], (80, 160, 240), shadow=None), flat(c, Thick(548, 212, 548, 230, 2), (40, 40, 50))],
      pivot=(548, 220), anim=dict(orbitRadius=(60, 30), orbitSpeed=0.15, stretch=(0.6, 0), scaleSpeed=5)),
    E("mist", lambda c, m: soft_union(c, [Ell(450, 362, 60, 14)], (255, 255, 255), 0.5, spread=12), pivot=(450, 362), daynight="untinted",
      anim=dict(pulse=0.15, scaleSpeed=0.8)),
    E("vine", lambda c, m: piece(c, [Thick(600, 70, 604, 220, 2.4), Ell(604, 224, 8, 5)], (70, 140, 70), shadow=None), pivot=(600, 70),
      anim=dict(swingAngle=6, swingSpeed=0.4)),
    E("ripple", lambda c, m: [flat(c, Thick(x, 580, x + 40, 580, 2), (170, 220, 220)) for x in (120, 620, 740)], daynight="untinted",
      anim=dict(bobAmplitude=(12, 0), bobSpeed=0.3)),
]

L236_DIFFS = [
    ("beak", 220, 66, 0),
    ("orchid", 360, 150, 0),
    ("monkey", 700, 100, 0),
    ("frog", 200, 455, 0),
    ("flower", 760, 420, 0),
    ("canoe", 480, 553, 0),
    ("hat", 472, 477, 0),
    ("parrot", 832, 524, 0),
]


# =================================================================== Level 237 ancient Egypt
def pyramid(c, x, base, w, h, col, cap=None):
    piece(c, Poly([(x - w / 2, base), (x + w / 2, base), (x, base - h)]), col, shadow=LAYER)
    flat(c, Poly([(x, base - h), (x + w / 2, base), (x + w * 0.1, base)]), lit(col, 0.84))
    for k in range(1, 8):
        y = base - h * k / 8
        hw = w / 2 * (1 - k / 8)
        flat(c, Thick(x - hw, y, x + hw, y, 1), lit(col, 0.92))
    if cap:
        flat(c, Poly([(x, base - h), (x - w * 0.06, base - h * 0.88), (x + w * 0.06, base - h * 0.88)]), cap)


def worker(c, x, base, h, kilt=(250, 246, 230), skin=(200, 140, 90), hair=(30, 30, 34)):
    flat(c, [Thick(x - 3 * h, base, x - 2 * h, base - 20 * h, 3.4 * h), Thick(x + 3 * h, base, x + 2 * h, base - 20 * h, 3.4 * h)], skin)
    piece(c, Poly([(x - 9 * h, base - 12 * h), (x + 9 * h, base - 12 * h), (x + 6 * h, base - 24 * h), (x - 6 * h, base - 24 * h)]), kilt, border=1, shadow=SMALL)
    piece(c, RRect(x - 7 * h, base - 40 * h, x + 7 * h, base - 23 * h, 3), skin, shadow=SMALL)
    flat(c, [Thick(x + 6 * h, base - 36 * h, x + 18 * h, base - 30 * h, 3 * h)], skin)
    hx, hy = x + 1 * h, base - 47 * h
    flat(c, Circ(hx, hy, 7 * h), skin)
    flat(c, [Ell(hx - 2 * h, hy - 2 * h, 8 * h, 8 * h)], hair)
    flat(c, Circ(hx + 2 * h, hy + 1 * h, 5.4 * h), skin)
    flat(c, Circ(hx + 4 * h, hy, 1.1 * h), INK)


def camel(c, x, base, s, col=(210, 170, 110), blanket=(200, 60, 60), face=1):
    for lx in (-20, -10, 12, 22):
        flat(c, RRect(x + lx * s * face - 3 * s, base - 38 * s, x + lx * s * face + 3 * s, base, 1), lit(col, 0.82))
    piece(c, [Ell(x, base - 46 * s, 32 * s, 14 * s), Ell(x - 4 * s * face, base - 60 * s, 14 * s, 12 * s),
              Poly([(x + 26 * s * face, base - 48 * s), (x + 40 * s * face, base - 74 * s), (x + 50 * s * face, base - 70 * s), (x + 34 * s * face, base - 42 * s)]),
              Ell(x + 50 * s * face, base - 74 * s, 11 * s, 6 * s)], col, border=1.5, shadow=PROP)
    flat(c, Poly([(x - 18 * s, base - 58 * s), (x + 12 * s, base - 58 * s), (x + 16 * s, base - 38 * s), (x - 22 * s, base - 38 * s)]), blanket)
    flat(c, Circ(x + 52 * s * face, base - 76 * s, 1.4 * s), INK)


def l237_bg(c, d):
    sky(c, (240, 200, 140), (250, 230, 190), 360)
    sun = (250, 220, 90) if "sun" not in d else (250, 150, 80)
    piece(c, Circ(620, 70, 40), sun, border=2, shadow=None)
    soft_union(c, [Circ(620, 70, 40)], (255, 240, 180), 0.4, spread=40)
    # pyramids
    pyramid(c, 330, 250, 340, 190, (230, 196, 130), cap=(250, 210, 70) if "cap" not in d else (240, 240, 236))
    pyramid(c, 560, 250, 260, 140, (220, 186, 124))
    pyramid(c, 700, 250, 160, 90, (214, 180, 120))
    # dunes
    piece(c, hill_strip(240, [(10, 0.01, 0.4), (6, 0.03, 1.2)]), (236, 206, 150), shadow=LAYER)
    # temple columns (left)
    piece(c, RRect(0, 180, 200, 210, 2), (230, 210, 170), border=1.5, shadow=PROP)
    for k, x in enumerate((20, 80, 140)):
        piece(c, [RRect(x, 210, x + 36, 360, 3), Poly([(x - 8, 210), (x + 44, 210), (x + 36, 196), (x, 196)])], (236, 216, 176), border=1.5, shadow=PROP)
        for j in range(4):
            flat(c, RRect(x + 6, 224 + j * 32, x + 30, 244 + j * 32, 1), [(60, 120, 180), (200, 80, 60), (240, 190, 60), (60, 150, 120)][(k + j) % 4])
    # obelisk (right)
    piece(c, Poly([(780, 360), (820, 360), (812, 120), (788, 120)]), (220, 196, 150), border=1.5, shadow=PROP)
    piece(c, Poly([(788, 120), (812, 120), (800, 98)]), (250, 210, 70) if "obelisk" not in d else (90, 170, 210), border=1.5, shadow=SMALL)
    for j in range(7):
        flat(c, [Thick(796, 140 + j * 30, 804, 150 + j * 30, 2)], (170, 140, 100))
    # Nile
    c.rect(0, 360, W, 440, (70, 150, 180))
    for k in range(8):
        flat(c, Thick(40 + k * 110, 380 + (k % 3) * 18, 100 + k * 110, 380 + (k % 3) * 18, 1.6), (130, 200, 220))
    for x in range(0, W, 30):
        flat(c, [Thick(x, 360, x + 4, 340, 2), Thick(x + 10, 360, x + 6, 344, 2)], (100, 150, 80))
    # felucca
    piece(c, Poly([(640, 410), (780, 410), (760, 428), (660, 428)]), (140, 100, 70), border=1.5, shadow=PROP)
    flat(c, Thick(710, 410, 710, 290, 2.4), (110, 80, 60))
    sail = (250, 246, 230) if "sail" not in d else (240, 140, 60)
    piece(c, Poly([(712, 294), (770, 400), (680, 400)]), sail, border=1.2, shadow=SMALL)
    # near bank (sand)
    c.rect(0, 440, W, H, (232, 204, 150))
    rnd = random.Random(2371)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(450, 600)
        flat(c, Thick(x, y, x + rnd.uniform(10, 30), y, 1.2), (216, 188, 136))
    # palms
    palm(c, 880, 560, h=180, lean=-14)
    if "palm" not in d:
        palm(c, 820, 560, h=130, lean=10)
    # camel with blanket
    camel(c, 280, 470, 1.5, blanket=(200, 60, 60) if "camel" not in d else (60, 110, 200))
    worker(c, 380, 470, 1.4, kilt=(250, 246, 230))
    # stone block on rollers pulled by workers
    blk = (220, 190, 140) if "block" not in d else (170, 170, 180)
    piece(c, RRect(400, 500, 500, 560, 3), blk, border=1.5, shadow=PROP)
    for x in (414, 450, 486):
        piece(c, Circ(x, 570, 9), (150, 110, 70), shadow=SMALL)
    flat(c, [Thick(500, 520, 560, 506, 2), Thick(560, 506, 640, 500, 2)], (160, 130, 90))
    for x in (580, 640):
        worker(c, x, 560, 1.5)
    # jars (left foreground)
    jar = (180, 100, 70) if "jar" not in d else (60, 140, 160)
    for k, x in enumerate((60, 120)):
        piece(c, [Ell(x, 560, 26, 34), RRect(x - 12, 518, x + 12, 530, 3)], jar if k == 0 else (190, 120, 80), border=1.5, shadow=PROP)
        flat(c, Thick(x - 22, 556, x + 22, 556, 3), (240, 210, 140))


L237_ELEMENTS = [
    bird_el("ibis", 470, 70, s=10, speed=-18),
    E("heat", lambda c, m: flat(c, Thick(200, 300, 260, 300, 2), (255, 240, 210, 0.5)), daynight="untinted", anim=dict(bobAmplitude=(30, 0), bobSpeed=0.2)),
    E("fan", lambda c, m: [flat(c, Thick(150, 470, 150, 410, 2), (110, 80, 60)), piece(c, Ell(150, 400, 16, 22), (70, 140, 80), shadow=SMALL)], pivot=(150, 470),
      anim=dict(swingAngle=12, swingSpeed=0.6)),
    E("ripple", lambda c, m: [flat(c, Thick(x, 430, x + 30, 430, 1.6), (150, 210, 230)) for x in (120, 380, 760)], daynight="untinted",
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.3)),
]

L237_DIFFS = [
    ("sun", 620, 70, 0),
    ("cap", 330, 72, 0),
    ("obelisk", 800, 110, 0),
    ("camel", 270, 420, 0),
    ("sail", 720, 350, 0),
    ("jar", 60, 556, 0),
    ("block", 450, 530, 0),
    ("palm", 826, 470, 0),
]


# =================================================================== Level 238 Arctic bay
def polar_bear(c, x, base, s, col=(250, 250, 246), face=1):
    for lx in (-20, -8, 12, 24):
        flat(c, RRect(x + lx * s * face - 5 * s, base - 22 * s, x + lx * s * face + 5 * s, base, 3), lit(col, 0.9))
    piece(c, [Ell(x, base - 30 * s, 34 * s, 18 * s), Ell(x + 34 * s * face, base - 34 * s, 14 * s, 11 * s), Circ(x + 28 * s * face, base - 44 * s, 4 * s)],
          col, border=1.5, shadow=PROP)
    flat(c, [Circ(x + 46 * s * face, base - 34 * s, 2.4 * s), Circ(x + 38 * s * face, base - 38 * s, 1.4 * s)], INK)


def seal(c, x, base, s, col):
    piece(c, [Ell(x, base - 10 * s, 26 * s, 10 * s), Circ(x + 22 * s, base - 18 * s, 9 * s), Poly([(x - 24 * s, base - 8 * s), (x - 38 * s, base - 16 * s), (x - 36 * s, base)])],
          col, border=1.2, shadow=SMALL)
    flat(c, [Circ(x + 25 * s, base - 20 * s, 1.8 * s)], INK)


def l238_bg(c, d):
    sky(c, (30, 50, 100), (120, 150, 200), 230)
    for k, (col, y) in enumerate((((90, 230, 160), 40), ((120, 200, 240), 70), ((180, 120, 220), 100))):
        soft_union(c, [Poly([(-20, y + 40), (200, y), (420, y + 30), (640, y - 10), (920, y + 20), (920, y + 34), (640, y + 6), (420, y + 46), (200, y + 16),
                             (-20, y + 56)])], col, 0.35, spread=18)
    rnd = random.Random(2381)
    for _ in range(40):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 140), rnd.choice((1, 1.5))), (240, 240, 255))
    # mountains + icebergs
    far_ridge(c, 230, 60, (190, 206, 230), 2382)
    c.rect(0, 250, W, 400, (60, 110, 160))
    for k in range(7):
        flat(c, Thick(20 + k * 130, 280 + (k % 3) * 30, 90 + k * 130, 280 + (k % 3) * 30, 1.6), (110, 160, 200))
    for x, y, w, h in ((420, 290, 110, 60), (640, 300, 70, 40)):
        piece(c, Poly([(x - w / 2, y), (x - w * 0.3, y - h * 0.7), (x, y - h), (x + w * 0.2, y - h * 0.6), (x + w / 2, y)]), (236, 246, 252), border=1.5,
              shadow=SMALL)
        flat(c, Poly([(x, y - h), (x + w * 0.2, y - h * 0.6), (x + w / 2, y), (x + w * 0.1, y)]), (200, 220, 236))
    # whale tail
    if "whale" not in d:
        piece(c, [Poly([(540, 330), (552, 300), (520, 280), (548, 288), (560, 270), (566, 290), (592, 280), (568, 302), (560, 330)])], (70, 80, 100),
              border=1.2, shadow=SMALL)
    # ice shelf foreground
    piece(c, hill_strip(380, [(12, 0.01, 0.4), (6, 0.04, 1.4)]), (236, 244, 250), shadow=LAYER)
    c.rect(0, 420, W, H, (236, 244, 250))
    for k in range(10):
        flat(c, Thick(30 + k * 90, 450 + (k % 4) * 34, 80 + k * 90, 446 + (k % 4) * 34, 1.6), (210, 226, 240))
    # research hut (left) with flag
    roof = (220, 70, 60)
    piece(c, RRect(30, 300, 210, 380, 3), roof, border=1.5, shadow=PROP)
    piece(c, Poly([(20, 302), (220, 302), (200, 270), (40, 270)]), (240, 240, 236), border=1.5, shadow=PROP)
    flat(c, [RRect(60, 320, 100, 350, 2), RRect(130, 320, 170, 350, 2)], (250, 220, 130))
    flat(c, RRect(104, 340, 126, 380, 2), (120, 60, 50) if "hut" not in d else (240, 200, 60))
    flat(c, Thick(190, 270, 190, 210, 2), (200, 200, 210))
    piece(c, [Ell(200, 206, 10, 10), Thick(190, 206, 210, 206, 2)], (220, 220, 230), shadow=None)
    # igloo
    igloo = Poly([(320 + 60 * math.cos(math.pi * k / 12), 420 - 46 * math.sin(math.pi * k / 12)) for k in range(13)])
    piece(c, igloo, (246, 250, 255), border=1.5, shadow=PROP)
    for k in range(1, 4):
        flat(c, Thick(266, 420 - k * 12, 374, 420 - k * 12, 1.2), (200, 216, 236))
    flat(c, [Poly([(304, 420), (304, 398), (336, 398), (336, 420)]), Ell(320, 398, 16, 10)], (60, 70, 90) if "igloo" not in d else (230, 150, 60))
    # polar bears
    polar_bear(c, 640, 440, 1.6)
    if "cub" not in d:
        polar_bear(c, 750, 452, 0.9, face=-1)
    seal(c, 820, 330, 1.2, (150, 150, 170) if "seal" not in d else (190, 140, 110))
    # dog sled (bottom centre)
    sled = (170, 110, 70) if "sled" not in d else (60, 120, 210)
    piece(c, [RRect(380, 540, 520, 556, 3), Thick(380, 566, 540, 566, 3), Thick(510, 556, 520, 520, 3)], sled, shadow=PROP)
    piece(c, RRect(396, 512, 500, 540, 4), (200, 70, 60), border=1.2, shadow=SMALL)
    for k, x in enumerate((570, 640, 710)):
        piece(c, [Ell(x, 548, 22, 10), Circ(x + 20, 536, 8), Poly([(x + 16, 530), (x + 20, 520), (x + 24, 530)])], (160, 160, 176) if k % 2 else (90, 90, 100),
              border=1.2, shadow=SMALL)
        flat(c, [RRect(x - 14, 554, x - 10, 566, 1), RRect(x + 10, 554, x + 14, 566, 1)], (90, 90, 100))
    flat(c, Thick(520, 540, 730, 540, 1.2), (60, 60, 70))
    # researcher in a parka (right)
    hx, hy = modern(c, 850, 600, (240, 140, 40) if "parka" not in d else (90, 170, 220), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.1)
    piece(c, Ell(hx, hy - 2, 12, 12), (240, 230, 210), shadow=None)
    flat(c, Circ(hx + 2, hy, 6.4), SKIN)
    flat(c, Circ(hx + 4, hy - 1, 1.4), INK)
    # ice fishing hole (left foreground)
    flat(c, Ell(100, 540, 46, 16), (40, 90, 140))
    flat(c, Thick(140, 500, 104, 540, 2), (150, 110, 70))


L238_ELEMENTS = [
    E("aurora", lambda c, m: soft_union(c, [Poly([(100, 40), (500, 20), (800, 50), (800, 70), (500, 40), (100, 60)])], (120, 250, 180), 0.25, spread=20),
      daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.4)),
    E("snow", lambda c, m: [flat(c, Circ(x, y, 2.4), (250, 250, 255)) for x, y in ((80, 160), (260, 220), (480, 120), (700, 200), (860, 140), (380, 260))],
      daynight="untinted", anim=dict(driftVelocity=(-4, 24), driftLength=80, driftFade=True)),
    E("bob", lambda c, m: [flat(c, Thick(104, 540, 104, 520, 1), (60, 60, 70)), piece(c, Circ(104, 520, 4), (220, 60, 60), shadow=None)], pivot=(104, 540),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=1.0)),
    E("blow", lambda c, m: soft_union(c, [Ell(556, 252, 8, 14)], (240, 250, 255), 0.7, spread=8), pivot=(556, 262), daynight="untinted",
      anim=dict(blinkInterval=3, blinkDuration=0.8)),
]

L238_DIFFS = [
    ("hut", 115, 360, 0),
    ("whale", 556, 302, 0),
    ("seal", 826, 318, 0),
    ("igloo", 320, 406, 0),
    ("cub", 750, 430, 0),
    ("sled", 450, 540, 0),
    ("parka", 850, 540, 0),
]


# =================================================================== Level 239 autumn orchard
def apple_tree(c, x, base, s, fruit=(220, 50, 50), leaf=(200, 150, 60)):
    piece(c, [Thick(x, base, x, base - 50 * s, 9 * s), Thick(x, base - 40 * s, x - 22 * s, base - 64 * s, 5 * s), Thick(x, base - 44 * s, x + 24 * s, base - 70 * s, 5 * s)],
          (130, 90, 60), shadow=PROP)
    piece(c, [Circ(x, base - 86 * s, 36 * s), Circ(x - 32 * s, base - 70 * s, 26 * s), Circ(x + 32 * s, base - 72 * s, 26 * s)], leaf, shadow=PROP)
    rnd = random.Random(int(x * 7 + base))
    for _ in range(9):
        a, r = rnd.uniform(0, 6.28), rnd.uniform(0, 40 * s)
        flat(c, Circ(x + math.cos(a) * r, base - 80 * s + math.sin(a) * r * 0.6, 5 * s), fruit)


def pumpkin(c, x, base, s, col):
    piece(c, [Ell(x - 10 * s, base - 14 * s, 14 * s, 14 * s), Ell(x + 10 * s, base - 14 * s, 14 * s, 14 * s), Ell(x, base - 15 * s, 14 * s, 15 * s)], col, border=1.2,
          shadow=SMALL)
    flat(c, [Thick(x - 4 * s, base - 26 * s, x - 4 * s, base - 4 * s, 1.2), Thick(x + 4 * s, base - 26 * s, x + 4 * s, base - 4 * s, 1.2)], lit(col, 0.8))
    flat(c, Thick(x, base - 28 * s, x + 4 * s, base - 36 * s, 3 * s), (110, 90, 50))


def basket(c, x, base, s, fruit):
    piece(c, Poly([(x - 26 * s, base - 30 * s), (x + 26 * s, base - 30 * s), (x + 20 * s, base), (x - 20 * s, base)]), (190, 140, 80), border=1.2, shadow=PROP)
    for k in range(3):
        flat(c, Thick(x - 24 * s, base - 22 * s + k * 9 * s, x + 24 * s, base - 22 * s + k * 9 * s, 1.2), (160, 110, 60))
    flat(c, [Circ(x - 14 * s + k * 9 * s, base - 32 * s - (k % 2) * 4 * s, 6 * s) for k in range(4)], fruit)


def l239_bg(c, d):
    sky(c, (150, 200, 236), (240, 226, 200), 230)
    cloud_bg(c, 200, 60, 0.7)
    far_ridge(c, 170, 40, (200, 170, 150), 2391)
    layer(c, 200, [(14, 0.01, 0.4), (8, 0.03, 1.4)], (210, 170, 100))
    # windmill (centre top)
    piece(c, Poly([(430, 200), (470, 200), (462, 110), (438, 110)]), (240, 230, 210), border=1.5, shadow=PROP)
    piece(c, Poly([(430, 112), (470, 112), (450, 92)]), (150, 80, 60) if "mill" not in d else (60, 110, 200), border=1.5, shadow=SMALL)
    # barn (left)
    barn = (190, 60, 50)
    piece(c, [RRect(30, 150, 220, 270, 2), Poly([(20, 152), (230, 152), (200, 106), (50, 106)])], barn, border=1.5, shadow=PROP)
    flat(c, Poly([(20, 152), (230, 152), (200, 106), (50, 106)]), (120, 60, 50))
    door = (250, 246, 236) if "barn" not in d else (250, 200, 60)
    flat(c, RRect(90, 190, 160, 270, 1), lit(barn, 0.8))
    flat(c, [Thick(90, 190, 160, 270, 4), Thick(160, 190, 90, 270, 4), Thick(90, 190, 160, 190, 4), Thick(90, 270, 160, 270, 4)], door)
    flat(c, RRect(108, 124, 142, 146, 2), (250, 230, 160))
    # orchard ground
    c.rect(0, 260, W, H, (170, 170, 90))
    for k in range(6):
        flat(c, Poly([(0, 300 + k * 50), (W, 280 + k * 50), (W, 296 + k * 50), (0, 316 + k * 50)]), (180, 180, 100))
    # rows of apple trees
    for k, x in enumerate((300, 560, 820)):
        apple_tree(c, x, 300, 1.0, fruit=(220, 50, 50) if not (k == 2 and "apples" in d) else (150, 200, 60), leaf=[(200, 150, 60), (190, 120, 50), (210, 160, 70)][k])
    for k, x in enumerate((180, 440, 700)):
        apple_tree(c, x, 420, 1.3, leaf=[(210, 130, 50), (200, 160, 60), (190, 120, 50)][k])
    # picker on a ladder (tree at 440)
    ladder = (150, 110, 70) if "ladder" not in d else (90, 150, 220)
    piece(c, [Thick(360, 420, 380, 290, 4), Thick(390, 420, 410, 290, 4)] + [Thick(366 - k * 0, 400 - k * 24, 396, 400 - k * 24, 3) for k in range(5)], ladder,
          shadow=PROP)
    modern(c, 390, 344, (90, 130, 70), bottom=(60, 70, 100), hair=(200, 150, 80), h=1.3)
    # baskets + crate
    basket(c, 560, 470, 1.3, (220, 50, 50) if "basket" not in d else (240, 200, 60))
    basket(c, 640, 480, 1.1, (220, 50, 50))
    # fence
    for x in range(0, W, 46):
        flat(c, RRect(x, 470, x + 6, 510, 1), (240, 230, 210))
    flat(c, [Thick(0, 480, W, 480, 4), Thick(0, 498, W, 498, 4)], (240, 230, 210))
    # tractor with trailer
    trac = (60, 140, 80) if "tractor" not in d else (220, 120, 40)
    piece(c, [RRect(380, 520, 480, 566, 6), RRect(440, 490, 480, 524, 3)], trac, border=1.5, shadow=PROP)
    flat(c, RRect(446, 496, 474, 516, 2), (180, 220, 240))
    piece(c, RRect(200, 520, 370, 560, 3), (170, 120, 70), border=1.5, shadow=PROP)
    flat(c, [Circ(220 + k * 18, 516 - (k % 2) * 5, 8) for k in range(9)], (220, 60, 50))
    for x, r in ((400, 18), (466, 26), (240, 16), (330, 16)):
        piece(c, Circ(x, 572 - (r - 16), r), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(x, 572 - (r - 16), r * 0.4), (160, 160, 170))
    # pumpkins + scarecrow
    for k, (x, s) in enumerate(((60, 1.6), (120, 1.2), (850, 1.4))):
        pumpkin(c, x, 590, s, (240, 140, 40) if not (k == 0 and "pumpkin" in d) else (240, 220, 200))
    piece(c, [Thick(770, 600, 770, 500, 4), Thick(730, 530, 810, 530, 4)], (150, 110, 70), shadow=PROP)
    piece(c, Poly([(752, 520), (788, 520), (794, 570), (746, 570)]), (60, 110, 180), border=1.2, shadow=SMALL)
    flat(c, Circ(770, 500, 12), (240, 210, 140))
    flat(c, [Ell(770, 490, 22, 5), RRect(760, 474, 780, 490, 3)], (200, 160, 80))
    # dog
    if "dog" not in d:
        piece(c, [Ell(680, 584, 22, 11), Circ(700, 570, 9), Ell(706, 562, 4, 7)], (200, 150, 100), border=1.2, shadow=SMALL)
        flat(c, Circ(704, 568, 1.4), INK)


L239_ELEMENTS = [
    E("sails", lambda c, m: flat(c, [Poly([(450, 112), (446, 60), (456, 62)]), Poly([(450, 112), (502, 108), (500, 118)]), Poly([(450, 112), (454, 164), (444, 162)]),
                                     Poly([(450, 112), (398, 116), (400, 106)])], (240, 230, 210)), pivot=(450, 112), anim=dict(rotateSpeed=30)),
    E("leaf1", lambda c, m: piece(c, Ell(600, 200, 7, 4), (220, 120, 40), shadow=None), pivot=(600, 200),
      anim=dict(driftVelocity=(-12, 40), driftLength=120, driftFade=True, swingAngle=40, swingSpeed=1.2)),
    E("leaf2", lambda c, m: piece(c, Ell(260, 280, 7, 4), (200, 90, 40), shadow=None), pivot=(260, 280),
      anim=dict(driftVelocity=(10, 40), driftLength=110, driftFade=True, swingAngle=40, swingSpeed=1.0, phase=0.5)),
    bird_el("crow", 700, 80, s=9, speed=-16),
    E("tail", lambda c, m: flat(c, Thick(660, 580, 650, 566, 3), (200, 150, 100)), pivot=(660, 580), anim=dict(swingAngle=25, swingSpeed=2.0)),
]

L239_DIFFS = [
    ("barn", 125, 230, 0),
    ("mill", 450, 102, 0),
    ("apples", 820, 220, 0),
    ("ladder", 386, 355, 0),
    ("basket", 560, 430, 0),
    ("pumpkin", 60, 570, 0),
    ("tractor", 430, 520, 0),
    ("dog", 690, 576, 0),
]


# =================================================================== Level 240 night food market
NE = (110, 100, 130)


def stall(c, x0, x1, top, awn, cloth, seed, sign_col):
    npiece(c, RRect(x0, top + 40, x1, 520, 2), (90, 70, 60))
    npiece(c, RRect(x0 + 6, top + 50, x1 - 6, 460, 2), (60, 46, 44))
    for k in range(int((x1 - x0) // 24)):
        col = awn if k % 2 == 0 else (240, 236, 226)
        npiece(c, Poly([(x0 + k * 24, top + 20), (x0 + k * 24 + 24, top + 20), (x0 + k * 24 + 24, top + 48), (x0 + k * 24 + 12, top + 56), (x0 + k * 24, top + 48)]),
               col, shadow=SMALL)
    sign_box(c, x0 + 14, top - 10, x1 - 14, top + 18, sign_col, seed, vertical=False)
    npiece(c, RRect(x0 - 6, 460, x1 + 6, 520, 3), cloth)


def l240_bg(c, d):
    c.gradient(0, H, (30, 30, 70), (80, 60, 110))
    rnd = random.Random(2401)
    for _ in range(30):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 140), 1.2), (240, 240, 255))
    if "moon" not in d:
        piece(c, Circ(800, 60, 30), (250, 240, 200), border=2, border_col=NE, shadow=None)
        soft_union(c, [Circ(800, 60, 30)], (255, 250, 220), 0.3, spread=30)
    # building silhouettes with lit windows
    for k, x in enumerate(range(-20, W, 110)):
        h = 160 + (k * 47 % 80)
        npiece(c, RRect(x, 300 - h, x + 104, 330, 2), (60, 50, 80), shadow=None)
        for wy in range(int(310 - h), 300, 26):
            for wx in (x + 16, x + 46, x + 76):
                flat(c, RRect(wx, wy, wx + 14, wy + 14, 1), (250, 210, 120) if (wx + wy) % 3 else (80, 70, 100))
    # lantern strings
    for k, (x0, y0, x1, y1) in enumerate(((-10, 110, 460, 120), (440, 120, 910, 100))):
        pts = string_lights(c, x0, y0, x1, y1, 8, [(220, 60, 60)], sag=40, r=0)
        for j, (x, y) in enumerate(pts):
            col = (220, 60, 60) if j % 2 == 0 else (250, 170, 60)
            if k == 0 and j == 1 and "lantern" in d:
                col = (90, 160, 230)
            lantern(c, x, y + 14, 1.0, col, pk=npiece)
    # street
    c.rect(0, 330, W, H, (70, 64, 76))
    for k in range(6):
        flat(c, Thick(0, 520 + k * 16, W, 520 + k * 16, 1), (80, 74, 86))
    # stalls
    stall(c, 20, 270, 190, (220, 60, 60), (200, 170, 120), 2402, (250, 200, 60))
    stall(c, 330, 580, 180, (60, 140, 90) if "awning" not in d else (150, 90, 200), (220, 200, 160), 2403, (240, 240, 230))
    stall(c, 640, 890, 190, (250, 160, 40), (200, 170, 120), 2404, (220, 60, 60))
    # food on the counters: skewers, bun steamers, noodles
    for k in range(6):
        flat(c, Thick(50 + k * 18, 456, 60 + k * 18, 420, 2), (200, 170, 120))
        npiece(c, [Ell(56 + k * 18, 432, 6, 4), Ell(58 + k * 18, 442, 6, 4)], (180, 90, 50), shadow=None)
    steamer = (210, 170, 110) if "steamer" not in d else (90, 160, 200)
    for k in range(3):
        npiece(c, [Ell(400, 450 - k * 22, 46, 10), RRect(354, 430 - k * 22, 446, 450 - k * 22, 2)], steamer, shadow=SMALL)
    npiece(c, [Ell(520, 440, 34, 12)], (250, 246, 236), shadow=SMALL)
    flat(c, Ell(520, 436, 26, 7), (230, 180, 90))
    for k in range(3):
        npiece(c, Circ(690 + k * 40, 440, 14), (250, 220, 160), shadow=SMALL)
    npiece(c, RRect(810, 410, 870, 456, 4), (60, 60, 70))
    # vendors
    modern(c, 150, 400, (250, 246, 236), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.4)
    modern(c, 460, 390, (250, 246, 236), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.4)
    modern(c, 760, 400, (220, 60, 60), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.4)
    # balloon seller (between stalls)
    bcols = [(240, 80, 120), (90, 170, 230), (250, 210, 60)]
    if "balloon" in d:
        bcols[1] = (120, 210, 120)
    for k, col in enumerate(bcols):
        flat(c, Thick(610, 470, 590 + k * 20, 330, 1), (220, 220, 220))
        npiece(c, Ell(590 + k * 20, 320 - (k % 2) * 16, 14, 18), col, shadow=SMALL)
    modern(c, 610, 520, (90, 120, 200), bottom=(60, 60, 80), hair=(130, 130, 140), h=1.5)
    # tables + stools (front)
    for k, x in enumerate((140, 450, 760)):
        npiece(c, [RRect(x - 70, 540, x + 70, 556, 4), RRect(x - 6, 556, x + 6, 600, 2)], (200, 60, 60) if k != 1 else (60, 120, 200))
        for sx in (x - 100, x + 100):
            col = (250, 200, 60) if not (k == 0 and sx < x and "stool" in d) else (90, 200, 140)
            npiece(c, [Ell(sx, 570, 18, 6), RRect(sx - 4, 570, sx + 4, 600, 1)], col, shadow=SMALL)
    # bowls on the middle table
    for x in (420, 480):
        npiece(c, Ell(x, 536, 18, 8), (250, 246, 236), shadow=SMALL)
    plate = (240, 180, 80) if "plate" not in d else (120, 200, 120)
    npiece(c, Ell(450, 534, 14, 6), plate, shadow=None)
    # customers in the front
    crowd_row(c, 40, 880, 610, 2405, h=1.8, edge=True)
    modern(c, 800, 600, (250, 200, 60) if "kid" not in d else (240, 120, 180), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.4)


L240_ELEMENTS = steam("st", 400, 400, n=3, r=7) + steam("st2", 520, 420, n=2, r=6) + [
    lights_el("bulbs", [(x, 300) for x in range(30, W, 60)], [(255, 220, 140)], r=3),
    E("glow", lambda c, m: soft_union(c, [RRect(30, 250, 260, 460, 4), RRect(340, 240, 570, 460, 4), RRect(650, 250, 880, 460, 4)], (255, 200, 120), 0.12, spread=20),
      daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=0.6)),
    E("fan", lambda c, m: flat(c, Ell(150, 380, 14, 8), (240, 200, 120)), pivot=(150, 386), anim=dict(swingAngle=20, swingSpeed=1.4)),
]

L240_DIFFS = [
    ("lantern", 78, 150, 0),
    ("moon", 800, 60, 0),
    ("awning", 455, 225, 0),
    ("steamer", 400, 430, 0),
    ("balloon", 610, 304, 0),
    ("stool", 40, 580, 0),
    ("plate", 450, 534, 0),
    ("kid", 800, 560, 0),
]


# =================================================================== Level 241 inside a space station
def l241_bg(c, d):
    c.rect(0, 0, W, H, (200, 206, 216))
    # curved module walls: panels
    for x in range(0, W, 90):
        piece(c, RRect(x + 4, 20, x + 86, 90, 6), (220, 224, 232), border=1, shadow=SMALL)
        piece(c, RRect(x + 4, 500, x + 86, 580, 6), (214, 218, 228), border=1, shadow=SMALL)
    flat(c, [RRect(0, 0, W, 16, 0), RRect(0, 584, W, H, 0)], (150, 156, 170))
    flat(c, [Thick(0, 98, W, 98, 5), Thick(0, 494, W, 494, 5)], (240, 200, 60))
    c.rect(0, 104, W, 490, (180, 186, 200))
    # big window with Earth (left)
    piece(c, Circ(160, 290, 130), (90, 96, 110), border=2, shadow=PROP)
    flat(c, Circ(160, 290, 112), (10, 12, 30))
    rnd = random.Random(2411)
    for _ in range(30):
        a, r = rnd.uniform(0, 6.28), rnd.uniform(0, 108)
        flat(c, Circ(160 + math.cos(a) * r, 290 + math.sin(a) * r, 1), (240, 240, 255))
    c.ellipse(160, 420, 160, 110, (60, 120, 200), ymax=400)
    soft_union(c, [Ell(160, 420, 150, 100)], (140, 200, 255), 0.25, spread=10)
    for x, y, rx, ry in ((110, 340, 40, 14), (210, 360, 50, 16), (150, 380, 30, 10)):
        flat(c, Ell(x, y, rx, ry), (90, 170, 90))
    for x, y in ((80, 330), (190, 324), (240, 380)):
        flat(c, Ell(x, y, 30, 6), (250, 250, 250))
    if "moon" not in d:
        piece(c, Circ(220, 220, 16), (230, 230, 220), shadow=None)
    for k in range(8):
        a = k * math.pi / 4
        flat(c, Circ(160 + 121 * math.cos(a), 290 + 121 * math.sin(a), 5), (160, 166, 180))
    # screens (centre top)
    for k, x in enumerate((340, 470)):
        piece(c, RRect(x, 120, x + 110, 200, 4), (40, 44, 56), border=1.5, shadow=PROP)
        scr = (60, 150, 200) if not (k == 1 and "screen" in d) else (220, 120, 60)
        flat(c, RRect(x + 8, 128, x + 102, 192, 2), scr)
        flat(c, [Thick(x + 16, 176, x + 40, 150, 2), Thick(x + 40, 150, x + 64, 166, 2), Thick(x + 64, 166, x + 94, 136, 2)], lit(scr, 1.5))
    # hydroponic rack (right)
    piece(c, RRect(700, 110, 880, 300, 4), (230, 232, 238), border=1.5, shadow=PROP)
    for r in range(3):
        y = 150 + r * 50
        flat(c, RRect(710, y, 870, y + 8, 2), (150, 156, 170))
        soft_union(c, [RRect(710, y - 30, 870, y - 26, 2)], (240, 140, 240), 0.3, spread=8)
        for k in range(5):
            pot = (240, 140, 40) if not (r == 0 and k >= 3 and "pot" in d) else (90, 170, 220)
            piece(c, RRect(718 + k * 32, y - 12, 740 + k * 32, y, 2), pot, shadow=None)
            flat(c, [Ell(729 + k * 32, y - 20, 9, 7), Ell(723 + k * 32, y - 26, 5, 6)], (90, 180, 90))
    # handrails + cables
    for x in (300, 620):
        piece(c, [RRect(x, 220, x + 10, 470, 4)], (240, 200, 60), shadow=SMALL)
    flat(c, [Thick(300, 104, 340, 160, 3), Thick(560, 104, 600, 180, 3)], (90, 96, 110))
    # tool box (centre)
    tb = (220, 60, 60) if "toolbox" not in d else (60, 160, 110)
    piece(c, [RRect(560, 380, 660, 440, 4), Thick(586, 380, 634, 380, 6)], tb, border=1.5, shadow=PROP)
    flat(c, RRect(560, 400, 660, 406, 0), lit(tb, 0.7))
    # bunk with sleeping bag (bottom left)
    piece(c, RRect(30, 420, 270, 490, 6), (150, 156, 170), border=1.5, shadow=PROP)
    piece(c, RRect(44, 430, 256, 480, 20), (60, 110, 200), border=1, shadow=SMALL)
    piece(c, RRect(196, 436, 250, 474, 12), (250, 250, 246) if "bag" not in d else (240, 150, 60), border=1, shadow=None)
    flat(c, Circ(214, 455, 14), SKIN)
    # food packs on velcro wall (bottom centre)
    for k in range(4):
        col = [(240, 200, 60), (220, 90, 90), (90, 180, 110), (90, 150, 220)][k]
        if k == 2 and "food" in d:
            col = (200, 120, 220)
        piece(c, RRect(390 + k * 40, 520, 420 + k * 40, 560, 3), col, border=1, shadow=SMALL)
    # fire extinguisher + hatch (bottom right)
    if "ext" not in d:
        piece(c, [RRect(780, 500, 810, 570, 8), RRect(788, 490, 802, 502, 2)], (220, 60, 60), border=1.2, shadow=SMALL)
    piece(c, Circ(860, 400, 60), (150, 156, 170), border=1.5, shadow=PROP)
    flat(c, Circ(860, 400, 44), (120, 126, 140))
    flat(c, [Thick(830, 400, 890, 400, 5)], (240, 200, 60))


def astronaut(c, x, y, s, suit, stripe):
    piece(c, [RRect(x - 14 * s, y - 20 * s, x + 14 * s, y + 18 * s, 8 * s), Circ(x, y - 32 * s, 14 * s),
              Thick(x - 12 * s, y - 12 * s, x - 34 * s, y - 30 * s, 8 * s), Thick(x + 12 * s, y - 12 * s, x + 30 * s, y + 6 * s, 8 * s),
              Thick(x - 6 * s, y + 16 * s, x - 20 * s, y + 44 * s, 9 * s), Thick(x + 6 * s, y + 16 * s, x + 18 * s, y + 44 * s, 9 * s)], suit, border=1.5, shadow=PROP)
    flat(c, Circ(x + 2 * s, y - 32 * s, 9 * s), (60, 80, 110))
    flat(c, Ell(x - 2 * s, y - 36 * s, 4 * s, 3 * s), (200, 220, 240))
    flat(c, RRect(x - 14 * s, y - 2 * s, x + 14 * s, y + 4 * s, 1), stripe)


L241_ELEMENTS = [
    E("astro", lambda c, m: astronaut(c, 470, 330, 1.6, (250, 250, 246), (220, 60, 60)), pivot=(470, 330), anim=dict(bobAmplitude=(10, 14), bobSpeed=0.2, swingAngle=6, swingSpeed=0.2)),
    E("pen", lambda c, m: flat(c, Thick(380, 260, 400, 250, 3), (60, 60, 70)), pivot=(390, 255), anim=dict(rotateSpeed=30, bobAmplitude=(10, 8), bobSpeed=0.3)),
    E("drop", lambda c, m: piece(c, Circ(620, 250, 7), (150, 210, 250, 0.9), shadow=None), pivot=(620, 250), anim=dict(bobAmplitude=(14, 10), bobSpeed=0.25)),
    E("leds", lambda c, m: [flat(c, Circ(x, 60, 3), (90, 240, 120)) for x in range(40, W, 90)], daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=1.2)),
]

L241_DIFFS = [
    ("moon", 220, 220, 0),
    ("screen", 525, 160, 0),
    ("pot", 841, 138, 0),
    ("toolbox", 610, 410, 0),
    ("bag", 223, 455, 0),
    ("food", 490, 540, 0),
    ("ext", 795, 530, 0),
]


# =================================================================== Level 242 candy kingdom
def lollipop(c, x, base, r, col, swirl=(250, 250, 246)):
    flat(c, Thick(x, base, x, base - r * 2.6, 3), (250, 250, 246))
    piece(c, Circ(x, base - r * 2.6 - r, r), col, border=1.5, shadow=PROP)
    for k in range(1, 4):
        c.ellipse_ring(x, base - r * 3.6, r * k / 4, r * k / 4, 2, swirl)


def gumdrop(c, x, base, w, h, col):
    piece(c, Poly([(x - w / 2, base), (x - w * 0.42, base - h * 0.7), (x - w * 0.2, base - h * 0.96), (x, base - h), (x + w * 0.2, base - h * 0.96),
                   (x + w * 0.42, base - h * 0.7), (x + w / 2, base)]), col, border=1.5, shadow=PROP)
    rnd = random.Random(int(x + base))
    for _ in range(5):
        flat(c, Circ(x + rnd.uniform(-w * 0.3, w * 0.3), base - rnd.uniform(h * 0.15, h * 0.75), 2.4), (250, 250, 246))


def l242_bg(c, d):
    sky(c, (250, 200, 230), (200, 230, 250), H)
    for x, y, k in ((140, 60, 0.8), (700, 50, 0.7), (420, 120, 0.5)):
        cloud_bg(c, x, y, k, col=(250, 220, 240) if not (x == 140 and "cloud" in d) else (200, 230, 250))
    # cupcake hills
    for k, (x, w, col) in enumerate(((150, 320, (240, 170, 200)), (500, 360, (200, 230, 170)), (800, 300, (250, 210, 160)))):
        piece(c, Ell(x, 270, w / 2, 70), col, shadow=LAYER)
        for j in range(8):
            flat(c, Circ(x - w * 0.35 + j * w * 0.1, 230 + (j % 3) * 10, 4), [(240, 80, 120), (90, 170, 230), (250, 220, 60)][j % 3])
    # castle
    castle = (250, 220, 236)
    piece(c, RRect(380, 120, 520, 270, 4), castle, border=1.5, shadow=PROP)
    for x in (350, 550):
        piece(c, RRect(x - 26, 140, x + 26, 270, 4), castle, border=1.5, shadow=PROP)
    gumdrop(c, 350, 146, 70, 60, (240, 100, 140))
    gumdrop(c, 550, 146, 70, 60, (120, 200, 240) if "turret" not in d else (250, 200, 60))
    gumdrop(c, 450, 126, 100, 80, (180, 120, 230))
    flat(c, Thick(450, 46, 450, 20, 2), (250, 250, 246))
    piece(c, Poly([(452, 20), (484, 28), (452, 38)]), (240, 80, 120) if "flag" not in d else (90, 200, 120), shadow=SMALL)
    flat(c, [RRect(426, 200, 474, 270, 24)], (150, 90, 60))
    for x in (400, 500):
        flat(c, RRect(x - 10, 160, x + 10, 186, 10), (250, 246, 200))
    for k in range(10):
        flat(c, Circ(384 + k * 14, 120, 6), [(240, 80, 120), (250, 250, 246)][k % 2])
    # chocolate river
    c.rect(0, 300, W, 380, (130, 80, 50))
    for k in range(9):
        flat(c, Thick(20 + k * 100, 320 + (k % 3) * 18, 80 + k * 100, 320 + (k % 3) * 18, 2), (160, 100, 66))
    # ground (frosting)
    piece(c, hill_strip(370, [(10, 0.02, 0.4), (6, 0.05, 1.4)]), (250, 240, 236), shadow=LAYER)
    c.rect(0, 400, W, H, (250, 240, 236))
    rnd = random.Random(2421)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(400, 600)
        flat(c, RRect(x, y, x + 8, y + 3, 1.4), rnd.choice([(240, 80, 120), (90, 170, 230), (250, 210, 60), (120, 200, 120)]))
    # lollipop trees
    lollipop(c, 80, 420, 30, (240, 90, 140) if "lolly" not in d else (90, 200, 220))
    lollipop(c, 190, 440, 22, (250, 190, 60))
    lollipop(c, 870, 430, 26, (120, 200, 120))
    # gingerbread house (left)
    gb = (190, 120, 70)
    piece(c, RRect(160, 460, 320, 560, 4), gb, border=1.5, shadow=PROP)
    piece(c, Poly([(150, 462), (330, 462), (240, 400)]), (250, 246, 240), border=1.5, shadow=PROP)
    for k in range(6):
        flat(c, Circ(170 + k * 30, 462, 6), [(240, 80, 120), (120, 200, 120), (250, 210, 60)][k % 3])
    door = (240, 90, 140) if "door" not in d else (90, 170, 230)
    flat(c, RRect(220, 500, 260, 560, 16), door)
    flat(c, [RRect(176, 480, 206, 506, 4), RRect(274, 480, 304, 506, 4)], (250, 240, 200))
    # donut on a hill (centre right)
    don = (240, 160, 190) if "donut" not in d else (250, 220, 90)
    piece(c, Ell(640, 470, 60, 30), (220, 170, 110), border=1.5, shadow=PROP)
    flat(c, Ell(640, 466, 52, 24), don)
    flat(c, Ell(640, 466, 18, 8), (220, 170, 110))
    for k in range(10):
        a = k * 0.63
        flat(c, Thick(640 + 36 * math.cos(a), 466 + 16 * math.sin(a), 640 + 42 * math.cos(a), 466 + 18 * math.sin(a), 2), [(90, 170, 230), (250, 250, 246)][k % 2])
    # candy canes fence
    for k, x in enumerate((360, 420, 480)):
        if k == 1 and "cane" in d:
            continue
        flat(c, [Thick(x, 600, x, 500, 6)], (250, 250, 246))
        c.ellipse_ring(x - 12, 500, 12, 12, 6, (250, 250, 246), ymax=500)
        for j in range(5):
            flat(c, Thick(x - 3, 590 - j * 20, x + 3, 582 - j * 20, 4), (230, 60, 70))
    # gummy bears (right foreground)
    for k, x in enumerate((760, 830)):
        col = (240, 80, 80, 0.85) if k == 0 else (120, 200, 120, 0.85)
        if k == 0 and "bear" in d:
            col = (250, 200, 60, 0.85)
        piece(c, [Ell(x, 570, 20, 24), Circ(x, 536, 15), Circ(x - 11, 524, 6), Circ(x + 11, 524, 6), Ell(x - 18, 560, 7, 9), Ell(x + 18, 560, 7, 9)], col, shadow=SMALL)
        flat(c, [Circ(x - 5, 534, 2), Circ(x + 5, 534, 2)], (60, 40, 50))


L242_ELEMENTS = [
    E("cloud", lambda c, m: cloud_bg(c, 260, 160, 0.5, col=(250, 230, 246)), anim=drift_across(230, 290, 10)),
    E("sprinkle", lambda c, m: [flat(c, Poly(star_pts(x, y, 9, 3, points=4, rot=0)), (255, 255, 240)) for x, y in ((300, 90), (620, 150), (800, 380), (100, 300))],
      daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.7)),
    E("boat", lambda c, m: [piece(c, Poly([(660, 330), (740, 330), (730, 346), (670, 346)]), (250, 200, 60), shadow=SMALL), flat(c, Thick(700, 330, 700, 300, 2), (250, 250, 246)),
                            piece(c, Poly([(702, 300), (726, 322), (702, 322)]), (240, 90, 140), shadow=None)],
      pivot=(700, 340), anim=dict(drift_across(660, 740, -14), bobAmplitude=(0, 3), bobSpeed=0.6)),
]

L242_DIFFS = [
    ("cloud", 140, 66, 0),
    ("lolly", 80, 342, 0),
    ("flag", 466, 29, 0),
    ("turret", 550, 116, 0),
    ("door", 240, 530, 0),
    ("donut", 640, 466, 0),
    ("cane", 420, 550, 0),
    ("bear", 760, 550, 0),
]


# =================================================================== Level 243 age of dinosaurs
def longneck(c, x, base, s, col, face=1):
    for lx in (-26, -12, 14, 28):
        flat(c, RRect(x + lx * s * face - 6 * s, base - 30 * s, x + lx * s * face + 6 * s, base, 3), lit(col, 0.85))
    piece(c, [Ell(x, base - 40 * s, 44 * s, 22 * s), Poly([(x + 30 * s * face, base - 50 * s), (x + 60 * s * face, base - 120 * s), (x + 74 * s * face, base - 118 * s),
                                                           (x + 46 * s * face, base - 36 * s)]),
              Ell(x + 74 * s * face, base - 122 * s, 14 * s, 8 * s), Poly([(x - 36 * s * face, base - 46 * s), (x - 90 * s * face, base - 26 * s), (x - 40 * s * face, base - 28 * s)])],
          col, border=1.5, shadow=PROP)
    flat(c, Circ(x + 80 * s * face, base - 124 * s, 1.8 * s), INK)


def horned(c, x, base, s, col, frill, face=1):
    for lx in (-18, -6, 14, 24):
        flat(c, RRect(x + lx * s * face - 5 * s, base - 16 * s, x + lx * s * face + 5 * s, base, 2), lit(col, 0.85))
    piece(c, [Ell(x, base - 26 * s, 34 * s, 18 * s), Ell(x + 36 * s * face, base - 30 * s, 16 * s, 13 * s)], col, border=1.5, shadow=PROP)
    piece(c, Ell(x + 26 * s * face, base - 40 * s, 12 * s, 22 * s), frill, border=1.2, shadow=SMALL)
    flat(c, [Poly([(x + 42 * s * face, base - 38 * s), (x + 66 * s * face, base - 52 * s), (x + 46 * s * face, base - 32 * s)])], (250, 246, 230))
    flat(c, Circ(x + 40 * s * face, base - 32 * s, 1.8 * s), INK)


def l243_bg(c, d):
    sky(c, (240, 190, 140), (250, 226, 180), H)
    # volcano
    piece(c, Poly([(40, 250), (170, 90), (230, 90), (360, 250)]), (120, 90, 90), shadow=LAYER)
    lava = (240, 90, 40) if "lava" not in d else (250, 200, 60)
    flat(c, Poly([(170, 90), (230, 90), (214, 130), (200, 112), (186, 140)]), lava)
    flat(c, [Thick(196, 120, 176, 210, 5), Thick(206, 120, 230, 200, 4)], lava)
    far_ridge(c, 250, 40, (180, 160, 140), 2431, x0=320)
    # jungle layer
    far_forest(c, 280, 50, (90, 140, 90), 2432)
    piece(c, hill_strip(290, [(14, 0.01, 0.3), (8, 0.04, 1.2)]), (120, 160, 90), shadow=LAYER)
    # lake
    flat(c, Ell(620, 330, 220, 34), (90, 160, 190))
    for k in range(5):
        flat(c, Thick(480 + k * 60, 330, 520 + k * 60, 330, 1.4), (140, 200, 220))
    longneck(c, 600, 360, 1.3, (120, 150, 170) if "longneck" not in d else (190, 150, 110))
    longneck(c, 790, 340, 0.8, (130, 160, 176))
    # ground
    c.rect(0, 380, W, H, (150, 170, 100))
    for k in range(8):
        flat(c, Poly([(0, 400 + k * 28), (W, 390 + k * 28), (W, 400 + k * 28), (0, 410 + k * 28)]), (160, 180, 108))
    # pterosaur on a rock spire (centre top)
    piece(c, Poly([(410, 280), (440, 150), (470, 150), (490, 280)]), (150, 130, 120), shadow=PROP)
    ptero = (200, 120, 90) if "ptero" not in d else (100, 140, 200)
    piece(c, [Ell(456, 140, 12, 8), Poly([(456, 136), (420, 110), (436, 140)]), Poly([(456, 136), (494, 110), (476, 140)]),
              Poly([(462, 132), (490, 128), (464, 140)]), Poly([(450, 132), (440, 116), (452, 128)])], ptero, border=1.2, shadow=SMALL)
    # horned dinos (left)
    horned(c, 230, 470, 1.7, (150, 130, 90), (200, 110, 80) if "frill" not in d else (90, 160, 210))
    # nest with eggs (centre bottom)
    piece(c, Ell(470, 540, 70, 22), (160, 120, 80), border=1.5, shadow=PROP)
    for k in range(4):
        col = (240, 236, 220) if not (k == 2 and "egg" in d) else (150, 210, 150)
        piece(c, Ell(430 + k * 26, 520 - (k % 2) * 6, 13, 17), col, shadow=SMALL)
        flat(c, [Circ(426 + k * 26, 514, 2.4), Circ(434 + k * 26, 526, 2)], (200, 180, 150))
    # ferns + cycads
    fern(c, 60, 600, 1.4, (70, 140, 80))
    fern(c, 880, 600, 1.6, (80, 150, 80) if "fern" not in d else (200, 160, 60))
    for x in (700, 790):
        piece(c, [RRect(x - 8, 480, x + 8, 560, 4)], (140, 110, 80), shadow=PROP)
        for a in (-50, -20, 20, 50):
            r = math.radians(a - 90)
            piece(c, Thick(x, 480, x + 50 * math.cos(r), 480 + 40 * math.sin(r), 6), (80, 150, 80), shadow=SMALL)
    # small raptor-like dino (friendly) near the nest
    piece(c, [Ell(620, 560, 26, 12), Ell(646, 536, 12, 8), Poly([(598, 556), (560, 548), (598, 566)]), RRect(612, 566, 618, 590, 2), RRect(628, 566, 634, 590, 2)],
          (110, 160, 120), border=1.2, shadow=SMALL)
    flat(c, Circ(650, 532, 1.6), INK)
    # rocks
    rock(c, 330, 600, 1.4)
    rock(c, 540, 600, 0.9)


L243_ELEMENTS = smoke_el("smk", 200, 70, n=4, col=(110, 100, 100), r=14, rise=(6, -30), length=80) + [
    E("ptero2", lambda c, m: piece(c, [Ell(700, 90, 10, 6), Poly([(700, 88), (668, 70), (684, 92)]), Poly([(700, 88), (732, 70), (716, 92)])], (180, 110, 90), shadow=SMALL),
      pivot=(700, 90), anim=dict(drift_across(660, 740, -20), stretch=(0, 0.4), scaleSpeed=2.0)),
    bird_el("ptero3", 300, 60, s=12, col=(150, 90, 80), speed=14),
    E("tail", lambda c, m: flat(c, Thick(560, 548, 540, 540, 4), (110, 160, 120)), pivot=(560, 548), anim=dict(swingAngle=20, swingSpeed=1.5)),
]

L243_DIFFS = [
    ("lava", 200, 120, 0),
    ("ptero", 456, 126, 0),
    ("longneck", 640, 320, 0),
    ("frill", 270, 412, 0),
    ("egg", 482, 514, 0),
    ("fern", 880, 560, 0),
]


# =================================================================== Level 244 balloon festival
def l244_bg(c, d):
    sky(c, (120, 180, 240), (230, 236, 246), H)
    cloud_bg(c, 150, 220, 0.6)
    cloud_bg(c, 760, 240, 0.5)
    far_ridge(c, 330, 50, (170, 196, 214), 2441)
    layer(c, 350, [(16, 0.01, 0.6), (8, 0.03, 0.2)], (130, 180, 110))
    # static balloons in the sky
    balloon(c, 120, 90, 46, [(240, 80, 80), (250, 220, 70)] if "b1" not in d else [(90, 170, 230), (250, 220, 70)])
    balloon(c, 450, 70, 40, [(90, 170, 230), (250, 250, 246)] if "b2" not in d else [(90, 170, 230), (240, 120, 180)])
    balloon(c, 780, 110, 50, [(250, 190, 60), (230, 90, 150)])
    balloon(c, 300, 230, 26, [(120, 200, 120), (250, 250, 246)])
    balloon(c, 640, 250, 30, [(180, 120, 220), (250, 230, 90)] if "b3" not in d else [(240, 140, 60), (250, 230, 90)])
    # field
    c.rect(0, 380, W, H, (120, 180, 90))
    for k in range(8):
        flat(c, Poly([(0, 390 + k * 30), (W, 384 + k * 30), (W, 394 + k * 30), (0, 400 + k * 30)]), (128, 188, 98))
    # tents
    for k, (x, col) in enumerate(((100, (240, 90, 90)), (220, (250, 250, 246)), (800, (90, 150, 220)))):
        if k == 0 and "tent" in d:
            col = (250, 200, 60)
        piece(c, Poly([(x - 50, 430), (x + 50, 430), (x, 380)]), col, border=1.5, shadow=PROP)
        flat(c, Poly([(x - 12, 430), (x + 12, 430), (x, 404)]), lit(col, 0.7))
    # flags
    for k, x in enumerate((300, 360, 560, 620)):
        flat(c, Thick(x, 440, x, 380, 2), (220, 220, 226))
        col = [(220, 60, 60), (250, 200, 60), (60, 120, 220), (90, 180, 110)][k]
        if k == 0 and "flag" in d:
            col = (200, 120, 220)
        piece(c, Poly([(x, 380), (x + 30, 390), (x, 400)]), col, shadow=SMALL)
    # balloon being inflated on the ground (centre)
    piece(c, Ell(470, 470, 110, 50), (240, 160, 60), border=1.5, shadow=PROP)
    for k in range(5):
        flat(c, Ell(400 + k * 34, 470, 10, 48), (250, 230, 120))
    piece(c, RRect(580, 460, 620, 500, 3), (150, 100, 60), border=1.2, shadow=SMALL)
    modern(c, 640, 500, (240, 90, 60), bottom=(60, 70, 100), hair=(90, 60, 40), h=1.4)
    # spectators
    crowd_row(c, 0, 900, 560, 2442, h=1.6)
    # picnic blanket + basket (front centre)
    blk = (220, 70, 70) if "blanket" not in d else (90, 150, 220)
    piece(c, Poly([(300, 560), (460, 560), (480, 600), (280, 600)]), blk, border=1.5, shadow=SMALL)
    for k in range(4):
        flat(c, Thick(310 + k * 40, 560, 300 + k * 44, 600, 4), (250, 246, 236))
    piece(c, [RRect(380, 556, 430, 586, 4), Thick(386, 556, 424, 556, 3)], (190, 140, 80), border=1.2, shadow=SMALL)
    # dog (right front)
    if "dog" not in d:
        piece(c, [Ell(780, 586, 26, 12), Circ(804, 570, 10), Ell(810, 562, 4, 8)], (240, 236, 226), border=1.2, shadow=SMALL)
        flat(c, [Circ(808, 568, 1.4), Ell(770, 582, 8, 5)], INK)


L244_ELEMENTS = [
    E("bal1", lambda c, m: balloon(c, 560, 170, 36, [(240, 100, 140), (250, 250, 246)]), pivot=(560, 170), anim=dict(bobAmplitude=(10, 20), bobSpeed=0.2)),
    E("bal2", lambda c, m: balloon(c, 220, 330, 22, [(250, 150, 50), (90, 150, 220)]), pivot=(220, 330), anim=dict(bobAmplitude=(0, 40), bobSpeed=0.12)),
    E("flame", lambda c, m: flat(c, Poly([(600, 460), (590, 440), (600, 420), (610, 440)]), (255, 180, 60)), pivot=(600, 460), daynight="untinted",
      anim=dict(stretch=(0.2, 0.5), scaleSpeed=5)),
    bird_el("bird", 380, 160, s=8, speed=18),
    cloud_el("cloud", 400, 300, 0.4, 6),
]

L244_DIFFS = [
    ("b1", 120, 90, 0),
    ("b2", 450, 70, 0),
    ("b3", 640, 250, 0),
    ("tent", 100, 410, 0),
    ("flag", 315, 390, 0),
    ("blanket", 380, 580, 0),
    ("dog", 795, 578, 0),
]


LEVELS = [
    ("Level235", "海底世界", l235_bg, L235_ELEMENTS, L235_DIFFS, 60, OPTS),
    ("Level236", "热带雨林", l236_bg, L236_ELEMENTS, L236_DIFFS, 60, OPTS),
    ("Level237", "古埃及", l237_bg, L237_ELEMENTS, L237_DIFFS, 60, OPTS),
    ("Level238", "极地冰原", l238_bg, L238_ELEMENTS, L238_DIFFS, 60, OPTS),
    ("Level239", "秋日果园", l239_bg, L239_ELEMENTS, L239_DIFFS, 60, OPTS),
    ("Level240", "夜市小吃街", l240_bg, L240_ELEMENTS, L240_DIFFS, 60, OPTS),
    ("Level241", "太空站内部", l241_bg, L241_ELEMENTS, L241_DIFFS, 60, OPTS),
    ("Level242", "糖果王国", l242_bg, L242_ELEMENTS, L242_DIFFS, 60, OPTS),
    ("Level243", "恐龙时代", l243_bg, L243_ELEMENTS, L243_DIFFS, 60, OPTS),
    ("Level244", "热气球节", l244_bg, L244_ELEMENTS, L244_DIFFS, 60, OPTS),
]
