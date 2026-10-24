# -*- coding: utf-8 -*-
"""Festivals around the year (paper-craft, full-bleed, no real brands or logos):
  Level145 年夜饭     - Spring Festival eve dinner: round table, couplets, red lanterns, fireworks through the window
  Level146 端午龙舟   - Dragon Boat Festival: two dragon boats on the river, drummers, crowd with umbrellas, zongzi stall
  Level147 中秋赏月   - Mid-Autumn night in a courtyard: full moon, osmanthus tree, mooncakes and tea, rabbit lanterns
  Level148 万圣节     - Halloween street at dusk: houses with jack-o'-lanterns, trick-or-treaters in costumes, bats
  Level149 圣诞夜     - Christmas Eve living room: decorated tree, fireplace with stockings, gifts, snow outside the window
  Level150 圣诞集市   - Christmas market square: timber-frame houses, striped stalls, big tree, shoppers; snow showers
  Level151 生日派对   - backyard birthday party: bunting, balloons, cake table, kids in party hats, bubbles, dog
  Level152 彩蛋寻宝   - spring egg hunt in a garden: painted eggs in the grass, kids with baskets, rabbits, blossom tree
  Level153 新年倒数   - New Year countdown on a city square at night: clock tower, giant screen, crowd, fireworks, confetti
  Level154 狂欢节游行 - carnival parade: a peacock float, feather dancers, drummers, balconies, streamers and confetti
"""
import math
import random

from fdcore import CLEAR, E, H, SNOW, W, W_, lit, on
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bush, cloud_bg, dead_tree, drift_across, house, layer, sky, tree_pine, tree_round
from fills import far_ridge, far_round_trees, far_skyline, wallpaper_stripes
from levels_akiba import modern, sign_box
from levels_daily import blossom_tree, cake
from levels_europe import firework, lady
from levels_gothic import pumpkin
from levels_homes import gingham, monstera, planks, steam
from cn_kit import cn_roof, lantern_cn, pagoda
from stylekit import flame
from weather import cloud, snow_layer

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)
NIGHT_EDGE = (120, 110, 140)
GOLDEN = (240, 196, 80)
CN_RED = (200, 40, 40)


# =================================================================== shared props
def npiece(c, shapes, col, border=1.5, shadow=PROP):
    """Paper piece for night scenes: muted cut edge instead of a glowing white one."""
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


def party_hat(c, hx, hy, h, col, dot=(250, 250, 250)):
    flat(c, Poly([(hx - 6 * h, hy - 5 * h), (hx + 6 * h, hy - 5 * h), (hx + 1 * h, hy - 20 * h)]), col)
    flat(c, Circ(hx + 1 * h, hy - 20 * h, 2.4 * h), dot)


def bunting(c, x0, y0, x1, y1, cols, n, sag=24, size=16, swap=None):
    """Pennant string from (x0, y0) to (x1, y1); swap = (index, colour)."""
    pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)) for t in [k / 20 for k in range(21)]]
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 1.4), (90, 80, 80))
    for k in range(n):
        t = (k + 0.5) / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
        col = swap[1] if swap and swap[0] == k else cols[k % len(cols)]
        piece(c, Poly([(x - size * 0.6, y), (x + size * 0.6, y), (x, y + size * 1.3)]), col, shadow=SMALL)


def string_lights(c, x0, y0, x1, y1, n, cols, sag=20, r=4):
    pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)) for t in [k / 20 for k in range(21)]]
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 1.2), (60, 60, 60))
    return [(x0 + (x1 - x0) * ((k + 0.5) / n), y0 + (y1 - y0) * ((k + 0.5) / n) + sag * 4 * ((k + 0.5) / n) * (1 - (k + 0.5) / n) + r)
            for k in range(n)]


def lights_el(eid, pts, cols, r=4, phase=0.0):
    def d(c, m):
        for k, (x, y) in enumerate(pts):
            soft_union(c, [Circ(x, y, r)], cols[k % len(cols)], 0.5, spread=r * 2)
            flat(c, Circ(x, y, r), lit(cols[k % len(cols)], 1.15))
    return E(eid, d, daynight="untinted", anim=dict(twinkle=0.35, twinkleSpeed=1.2, phase=phase))


def gift(c, x, base, w, h, col, ribbon=(250, 220, 90), edge=None):
    (npiece if edge else piece)(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), col, shadow=SMALL)
    flat(c, [RRect(x - 3, base - h, x + 3, base, 0), RRect(x - w / 2, base - h * 0.55 - 3, x + w / 2, base - h * 0.55 + 3, 0)], ribbon)
    flat(c, [Ell(x - 7, base - h - 4, 7, 4), Ell(x + 7, base - h - 4, 7, 4)], ribbon)


def fireworks(prefix, items, mode="untinted"):
    return [E("%s%d" % (prefix, i), firework(x, y, col, r), pivot=(x, y), daynight=mode,
              anim=dict(blinkInterval=2.4 + i * 0.35, blinkDuration=1.1, phase=i * 0.29, pulse=0.15, scaleSpeed=0.8))
            for i, (x, y, col, r) in enumerate(items)]


def confetti(prefix, seed, n, x0, x1, y0, cols, fall=(4, 30), length=160):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(x0, x1), y0 + rnd.uniform(0, 40)
        col, a = rnd.choice(cols), rnd.uniform(0, math.pi)
        out.append(E("%s%d" % (prefix, i), (lambda x=x, y=y, col=col, a=a: lambda c, m: flat(c, Thick(x - 4 * math.cos(a), y - 4 * math.sin(a), x + 4 * math.cos(a),
                                                                                                 y + 4 * math.sin(a), 3), col))(),
                     daynight="untinted", anim=dict(driftVelocity=fall, driftLength=length, driftFade=True, swingAngle=40, swingSpeed=1.5,
                                                    phase=rnd.random())))
    return out


def crowd_row(c, x0, x1, base, seed, h=1.6, tops=None, step=34, edge=False, hats=None):
    """A row of modern figures (back rows of crowds)."""
    rnd = random.Random(seed)
    tops = tops or [(220, 90, 80), (90, 140, 210), (240, 200, 80), (120, 180, 120), (200, 120, 200), (240, 240, 236), (70, 70, 90)]
    x = x0
    while x < x1:
        hx, hy = modern(c, x, base + rnd.uniform(-4, 4), rnd.choice(tops), bottom=rnd.choice([(60, 70, 100), (70, 60, 60), (50, 50, 60)]),
                        hair=rnd.choice([(40, 30, 30), (90, 60, 40), (200, 160, 90), (30, 30, 34)]), h=h * rnd.uniform(0.92, 1.08),
                        style=rnd.choice(["short", "long", "short"]))
        if hats and rnd.random() < 0.5:
            party_hat(c, hx, hy, h, rnd.choice(hats))
        x += step * rnd.uniform(0.8, 1.2)


# =================================================================== Level 145 Spring Festival eve dinner
WALL145 = (240, 224, 196)


def l145_bg(c, d):
    c.rect(0, 0, W, 430, WALL145)
    flat(c, RRect(0, 0, W, 12, 0), (246, 236, 214))
    # window with the night sky (fireworks are elements)
    flat(c, RRect(330, 60, 570, 250, 0), (30, 34, 74))
    far_skyline(c, 250, 30, 80, (50, 52, 90), 1451, win=(255, 210, 120), x0=330, x1=570)
    flat(c, RRect(300, 250, 600, 430, 0), WALL145)                               # skyline blocks run past the sill
    piece(c, [RRect(320, 50, 580, 60, 0), RRect(320, 50, 330, 260, 0), RRect(570, 50, 580, 260, 0), RRect(447, 60, 453, 250, 0),
              RRect(312, 250, 588, 262, 1)], (150, 60, 50), shadow=SMALL)
    # couplets + banner
    for x in (276, 594):
        piece(c, RRect(x, 70, x + 30, 330, 1), CN_RED, border=1.2, shadow=PROP)
        sign_box(c, x, 70, x + 30, 330, CN_RED, 1450 + x, glyph=(30, 24, 20))
    banner = CN_RED if "banner" not in d else (240, 180, 50)
    piece(c, RRect(330, 18, 570, 44, 1), banner, border=1.2, shadow=PROP)
    sign_box(c, 380, 18, 520, 44, banner, 1453, glyph=(30, 24, 20), vertical=False)
    # 福 diamond (left)
    fu = CN_RED if "fu" not in d else (240, 140, 40)
    piece(c, Poly([(160, 80), (220, 140), (160, 200), (100, 140)]), fu, border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, Thick(140 + k * 10, 118 + k * 6, 178 - k * 4, 160 - k * 8, 3), (30, 24, 20))
    # TV cabinet with the gala (left)
    piece(c, RRect(20, 330, 230, 430, 3), (140, 90, 60), border=1.5, shadow=PROP)
    piece(c, RRect(40, 220, 210, 324, 3), (30, 30, 36), border=1.2, shadow=PROP)
    scr = (230, 70, 80) if "tv" not in d else (60, 120, 200)
    flat(c, RRect(48, 228, 202, 316, 1), scr)
    flat(c, [Ell(125, 316, 70, 22)], lit(scr, 0.7))
    for k, x in enumerate((90, 125, 160)):
        flat(c, [Circ(x, 278, 7), RRect(x - 7, 286, x + 7, 312, 3)], [(250, 220, 90), (250, 250, 240), (250, 220, 90)][k])
    flat(c, Thick(125, 324, 125, 330, 6), (30, 30, 36))
    # floor + rug
    planks(c, 430, (160, 110, 70), (140, 94, 60), seed=145)
    piece(c, Ell(450, 560, 400, 40), (170, 40, 40), shadow=SMALL)
    c.ellipse_ring(450, 560, 380, 34, 4, GOLDEN)
    # kumquat tree (right)
    piece(c, Poly([(796, 500), (856, 500), (848, 560), (804, 560)]), (210, 60, 50) if "pot" not in d else (60, 110, 180), border=1.5, shadow=PROP)
    piece(c, [Circ(826, 420, 54), Circ(790, 448, 36), Circ(862, 448, 36), Circ(826, 380, 36)], (70, 140, 80), shadow=PROP)
    rnd = random.Random(1452)
    for _ in range(18):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(10, 54)
        flat(c, Circ(826 + r * math.cos(a), 420 + r * math.sin(a) * 0.9, 5), (250, 160, 40))
    flat(c, Thick(826, 470, 826, 500, 6), (110, 80, 50))
    # family behind the table
    for x, top, hair, h, style in ((300, (200, 60, 60), (220, 220, 226), 2.3, "short"), (390, (120, 60, 90), (200, 200, 206), 2.3, "long"),
                                   (510, (60, 90, 150), (40, 30, 30), 2.5, "short"), (600, (230, 120, 80), (40, 30, 30), 2.4, "long")):
        modern(c, x, 440, top, bottom=(60, 50, 50), hair=hair, h=h, style=style)
    # round table with dishes
    piece(c, [Ell(450, 420, 280, 34), RRect(170, 420, 730, 500, 0), Ell(450, 500, 280, 20)], (200, 40, 40), border=1.5, shadow=PROP)
    flat(c, Thick(176, 470, 724, 470, 3), GOLDEN)
    piece(c, Ell(450, 412, 60, 14), (246, 244, 236), border=1, shadow=SMALL)
    fish = (230, 140, 60) if "fish" not in d else (120, 160, 200)
    piece(c, [Ell(444, 406, 38, 10), Poly([(482, 406), (500, 396), (500, 416)])], fish, shadow=SMALL)
    flat(c, Circ(418, 404, 2), INK)
    piece(c, Ell(330, 414, 42, 11), (246, 244, 236), border=1, shadow=SMALL)
    for k in range(5):
        flat(c, Ell(310 + k * 10, 408, 8, 5), (250, 248, 236))
    piece(c, [Ell(580, 410, 34, 14), RRect(548, 396, 612, 410, 4)], (180, 120, 60), border=1, shadow=SMALL)
    flat(c, Ell(580, 398, 30, 5), (220, 110, 70))
    cup = (250, 240, 230) if "cup" not in d else (240, 200, 60)
    piece(c, Poly([(644, 414), (678, 414), (672, 378), (650, 378)]), cup, border=1, shadow=SMALL)
    flat(c, Ell(661, 382, 10, 3), (240, 140, 60))
    # child on a stool in front, holding a sparkler-free red envelope
    modern(c, 240, 590, (220, 60, 60), bottom=(60, 60, 80), hair=(30, 30, 34), h=2.0, style="twin")
    piece(c, RRect(256, 520, 276, 548, 2), CN_RED, shadow=SMALL)
    flat(c, RRect(262, 528, 270, 534, 1), GOLDEN)


L145_ELEMENTS = fireworks("fw", ((380, 110, (255, 120, 140), 30), (500, 96, (255, 220, 110), 34), (440, 170, (140, 220, 255), 22))) + [
    E("lanternL", lambda c, m: (flat(c, Thick(60, 0, 60, 60, 1.4), (60, 50, 50)), lantern_cn(c, 60, 86, r=22)), pivot=(60, 0), daynight="untinted",
      anim=dict(swingAngle=4, swingSpeed=0.3)),
    E("lanternR", lambda c, m: (flat(c, Thick(840, 0, 840, 60, 1.4), (60, 50, 50)), lantern_cn(c, 840, 86, r=22)), pivot=(840, 0), daynight="untinted",
      anim=dict(swingAngle=4, swingSpeed=0.3, phase=0.5)),
] + steam("steam", 580, 392, n=3, r=6)

L145_DIFFS = [
    ("banner", 450, 31, 0),
    ("fu", 160, 140, 0),
    ("tv", 125, 272, 0),
    ("pot", 826, 530, 0),
    ("fish", 450, 406, 0),
    ("cup", 661, 400, 0),
]


# =================================================================== Level 146 Dragon Boat Festival
RIVER = (300, 520)


def dragon_boat(c, x, y, hull, head, rowers, flip=False):
    s = -1 if flip else 1
    piece(c, [Poly([(x - 170 * s, y - 6), (x + 150 * s, y - 6), (x + 130 * s, y + 14), (x - 150 * s, y + 14)])], hull, border=1.5, shadow=PROP)
    flat(c, [Thick(x - 160 * s + k * 20 * s, y + 4, x - 150 * s + k * 20 * s, y + 4, 3) for k in range(15)], lit(hull, 1.3))
    piece(c, [Poly([(x + 146 * s, y - 6), (x + 176 * s, y - 50), (x + 196 * s, y - 46), (x + 184 * s, y - 30), (x + 160 * s, y + 4)])], head,
          border=1.5, shadow=PROP)
    flat(c, Circ(x + 182 * s, y - 42, 3), INK)
    piece(c, Poly([(x - 168 * s, y - 6), (x - 196 * s, y - 34), (x - 180 * s, y - 4)]), lit(hull, 1.2), border=1.2, shadow=SMALL)
    for k in range(rowers):
        rx = x - 120 * s + k * 34 * s
        modern(c, rx, y - 4, (250, 250, 246) if k % 2 else (230, 80, 70), bottom=(50, 50, 60), hair=(30, 30, 34), h=1.0)
    piece(c, [RRect(x - 4 - 140 * s, y - 34, x + 4 - 140 * s, y - 6, 2), Ell(x - 140 * s, y - 34, 12, 8)], (170, 60, 40), shadow=SMALL)


def l146_bg(c, d):
    sky(c, (150, 200, 240), (220, 236, 246))
    cloud_bg(c, 160, 70, 0.9)
    cloud_bg(c, 620, 50, 1.1)
    layer(c, 230, [(20, 0.01, 0.2), (8, 0.03, 1.1)], (160, 190, 176))
    layer(c, 270, [(14, 0.012, 1.0), (6, 0.04, 0.3)], (120, 170, 120))
    pagoda(c, 720, 280, 54, 5, 30, roof=(70, 80, 100) if "pagoda" not in d else (180, 60, 50))
    # arched stone bridge in the distance
    piece(c, Poly([(60, 300)] + [(170 + 110 * math.cos(math.radians(a)), 300 - 40 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(280, 300),
                   (280, 312), (60, 312)]), (200, 196, 184), shadow=PROP)
    flat(c, Poly([(110, 312)] + [(170 + 50 * math.cos(math.radians(a)), 312 - 24 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(220, 312)]),
         (150, 190, 200))
    # river
    c.rect(0, 300, W, 520, (110, 170, 200))
    for y in range(316, 520, 22):
        for x in range((y * 7) % 60, W, 90):
            flat(c, Thick(x, y, x + 34, y, 1.6), (150, 200, 226))
    flat(c, RRect(0, 300, W, 306, 0), (170, 200, 180))
    # boats (static; paddles are elements)
    dragon_boat(c, 300, 380, (220, 70, 50), (230, 170, 40) if "dragon" not in d else (60, 160, 100), 8)
    dragon_boat(c, 600, 460, (60, 120, 190), (230, 200, 60), 8, flip=True)
    # far bank flags
    for k, x in enumerate((420, 470, 520, 570)):
        flat(c, Thick(x, 300, x, 240, 2), (110, 90, 70))
        col = [(230, 70, 60), (240, 200, 60), (70, 140, 210), (110, 180, 110)][k]
        if k == 2 and "flag" in d:
            col = (200, 110, 200)
        piece(c, Poly([(x, 240), (x + 40, 250), (x, 268)]), col, shadow=SMALL)
    # near bank + crowd
    layer(c, 512, [(4, 0.02, 0.3)], (130, 170, 100))
    crowd_row(c, 300, 760, 596, 1462, h=1.9, step=40)
    for k, (x, col) in enumerate(((360, (240, 120, 160)), (520, (90, 160, 220)), (690, (240, 200, 70)))):
        if k == 1 and "umbrella" in d:
            col = (120, 190, 110)
        flat(c, Thick(x, 560, x, 500, 2), (70, 60, 60))
        piece(c, Poly([(x - 40, 506), (x, 478), (x + 40, 506)]), col, shadow=PROP)
    # zongzi stall (left)
    piece(c, [RRect(20, 470, 220, 560, 2)], (180, 130, 80), border=1.5, shadow=PROP)
    awning = (230, 80, 70) if "awning" not in d else (80, 120, 200)
    piece(c, Poly([(6, 470), (234, 470), (220, 430), (20, 430)]), awning, border=1.5, shadow=PROP)
    for x in range(30, 220, 40):
        flat(c, Poly([(x, 470), (x + 20, 470), (x + 10, 482)]), awning)
    for k in range(6):
        x = 50 + k * 26
        piece(c, Poly([(x - 10, 520), (x + 10, 520), (x, 498)]), (110, 160, 90), shadow=SMALL)
        flat(c, Thick(x - 8, 512, x + 8, 512, 1.4), (200, 170, 110))
    piece(c, [Ell(170, 512, 22, 6), RRect(150, 496, 190, 512, 3)], (190, 190, 196), shadow=SMALL)
    modern(c, 120, 596, (240, 240, 236), bottom=(70, 70, 90), hair=(220, 220, 226), h=1.8)
    # willow (right)
    piece(c, [Thick(850, 600, 846, 380, 10)], (110, 80, 60), shadow=PROP)
    willow = (120, 180, 90)
    for k in range(9):
        x = 790 + k * 16
        flat(c, Thick(846, 380, x, 500 + (k % 3) * 20, 3), willow)
    piece(c, [Ell(846, 380, 70, 30)], willow, shadow=PROP)
    # drum on the near bank
    piece(c, [Ell(260, 560, 28, 22), RRect(232, 560, 288, 590, 4)], (200, 60, 50) if "drum" not in d else (60, 110, 180), border=1.5, shadow=PROP)
    flat(c, Ell(260, 560, 24, 16), (240, 220, 180))


def l146_paddles(x, y, n, flip, ph):
    s = -1 if flip else 1

    def d(c, m):
        for k in range(n):
            rx = x - 120 * s + k * 34 * s
            flat(c, Thick(rx + 6 * s, y - 34, rx - 10 * s, y + 18, 2.4), (150, 110, 70))
    return E("pad%d" % x, d, pivot=(x, y - 10), anim=dict(swingAngle=3, swingSpeed=1.0, phase=ph))


L146_ELEMENTS = [
    l146_paddles(300, 380, 8, False, 0.0),
    l146_paddles(600, 460, 8, True, 0.5),
    E("boatA_bob", lambda c, m: flat(c, [Thick(130, 390, 160, 390, 1.6), Thick(460, 392, 490, 392, 1.6)], (220, 240, 250)),
      anim=dict(bobAmplitude=(6, 1), bobSpeed=0.5)),
    E("drumstick", lambda c, m: flat(c, Thick(282, 536, 298, 516, 3), (110, 80, 60)), pivot=(282, 536), anim=dict(swingAngle=18, swingSpeed=2.0)),
    E("willow", lambda c, m: flat(c, [Thick(846, 400, 800 + k * 18, 530, 2) for k in range(4)], (130, 190, 100)), pivot=(846, 400),
      anim=dict(swingAngle=3, swingSpeed=0.3)),
    E("cloud", lambda c, m: cloud_bg(c, 400, 40, 0.7), anim=dict(bobAmplitude=(20, 0), bobSpeed=0.04)),
]

L146_DIFFS = [
    ("pagoda", 720, 200, 0),
    ("dragon", 486, 344, 0),
    ("flag", 534, 252, 0),
    ("umbrella", 520, 494, 0),
    ("awning", 120, 450, 0),
    ("drum", 260, 572, 0),
]


# =================================================================== Level 147 Mid-Autumn moon in a courtyard
def l147_bg(c, d):
    sky(c, (20, 26, 64), (60, 60, 110))
    rnd = random.Random(1471)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 230)
        flat(c, Poly(star_pts(x, y, 3, 1, points=4, rot=0)), (255, 248, 210))
    soft_union(c, [Circ(640, 120, 70)], (255, 240, 190), 0.4, spread=60)
    piece(c, Circ(640, 120, 62), (252, 240, 200), shadow=None)
    flat(c, [Circ(620, 104, 10), Circ(664, 140, 8), Circ(650, 96, 5)], (238, 224, 184))
    # courtyard wall with a moon gate
    npiece(c, RRect(-10, 250, 910, 430, 0), (210, 206, 200), shadow=LAYER)
    cn_roof(c, -20, 920, 252, 22, col=(60, 66, 80), ornaments=False)
    flat(c, Circ(450, 340, 74), (40, 44, 70))
    c.ellipse_ring(450, 340, 80, 80, 8, (170, 166, 160))
    flat(c, [Circ(430, 380, 30), Circ(480, 370, 36)], (40, 70, 60))
    # pavilion eaves (top left)
    cn_roof(c, -40, 300, 120, 40, col=(50, 56, 70))
    flat(c, [RRect(10, 120, 26, 430, 0), RRect(250, 120, 266, 430, 0)], (150, 50, 46))
    for k, x in enumerate((70, 140, 210)):
        col = (220, 60, 50) if not (k == 1 and "lantern" in d) else (240, 200, 60)
        lantern_cn(c, x, 160, col=col, r=16)
    # osmanthus tree (right)
    piece(c, [Thick(800, 440, 790, 250, 12), Thick(794, 320, 740, 270, 6)], (90, 66, 56), shadow=PROP)
    osm = (60, 110, 70)
    piece(c, [Circ(790, 230, 70), Circ(730, 260, 50), Circ(856, 260, 50), Circ(790, 180, 48)], osm, border=1.2, border_col=NIGHT_EDGE, shadow=PROP)
    flower = (250, 210, 90) if "osmanthus" not in d else (250, 250, 240)
    rnd = random.Random(1472)
    for _ in range(40):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(10, 70)
        flat(c, Circ(790 + r * math.cos(a), 230 + r * math.sin(a) * 0.8, 3.4), flower)
    # stone floor
    c.rect(0, 430, W, H, (120, 118, 130))
    for y in range(430, H, 34):
        off = 0 if (y // 34) % 2 else 40
        flat(c, Thick(0, y, W, y, 1.4), (100, 98, 112))
        for x in range(off, W, 80):
            flat(c, Thick(x, y, x, y + 34, 1.4), (100, 98, 112))
    # family at the table
    for x, top, hair, h, style in ((330, (150, 60, 70), (220, 220, 226), 2.2, "long"), (580, (60, 80, 120), (30, 30, 34), 2.4, "short")):
        modern(c, x, 540, top, bottom=(50, 50, 60), hair=hair, h=h, style=style)
    npiece(c, [Ell(450, 470, 130, 18), RRect(436, 470, 464, 560, 3), Ell(450, 560, 40, 8)], (130, 80, 56))
    npiece(c, Ell(400, 462, 40, 9), (240, 236, 226), border=1, shadow=SMALL)
    cakes = (200, 140, 70) if "mooncake" not in d else (120, 160, 80)
    for k in range(3):
        npiece(c, [Ell(386 + k * 14, 452 - (k % 2) * 6, 14, 8)], cakes, border=1, shadow=SMALL)
    npiece(c, [Ell(500, 452, 18, 14), Thick(516, 448, 528, 440, 3), RRect(494, 436, 506, 440, 2)], (90, 150, 140), border=1, shadow=SMALL)
    for x in (470, 536):
        npiece(c, RRect(x - 7, 452, x + 7, 464, 2), (240, 236, 226), border=1, shadow=SMALL)
    # rabbit lanterns on the floor (static bodies, glows are elements)
    for k, x in enumerate((140, 700)):
        col = (250, 240, 236) if not (k == 1 and "rabbit" in d) else (250, 190, 210)
        npiece(c, [Ell(x, 540, 30, 18), Circ(x + 28, 524, 12), Ell(x + 22, 504, 4, 12), Ell(x + 32, 504, 4, 12)], col, border=1, shadow=SMALL)
        flat(c, Circ(x + 32, 522, 2.4), (220, 50, 60))
        flat(c, [RRect(x - 20, 560, x - 14, 572, 1), RRect(x + 14, 560, x + 20, 572, 1)], (60, 56, 60))
    # cat on the wall
    if "cat" not in d:
        npiece(c, [Ell(170, 244, 22, 10), Circ(190, 234, 9), Poly([(184, 228), (186, 218), (190, 228)]), Poly([(192, 228), (196, 218), (198, 230)])],
               (40, 36, 44), border=1, shadow=SMALL)


L147_ELEMENTS = [
    E("glowL", lambda c, m: soft_union(c, [Ell(140, 540, 30, 18)], (255, 230, 170), 0.55, spread=24), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.8)),
    E("glowR", lambda c, m: soft_union(c, [Ell(700, 540, 30, 18)], (255, 230, 170), 0.55, spread=24), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.8, phase=0.5)),
    E("lglow", lambda c, m: soft_union(c, [Circ(x, 160, 14) for x in (70, 140, 210)], (255, 170, 90), 0.4, spread=20), daynight="untinted",
      anim=dict(twinkle=0.15, twinkleSpeed=0.6)),
    E("cloud", lambda c, m: piece(c, [Ell(300, 80, 60, 12), Ell(330, 72, 40, 10)], (90, 90, 140), shadow=None), daynight="untinted",
      anim=dict(bobAmplitude=(60, 0), bobSpeed=0.03)),
    E("tea", lambda c, m: soft_union(c, [Circ(470, 444, 4)], (240, 240, 250), 0.5, spread=4), daynight="untinted",
      anim=dict(driftVelocity=(1, -10), driftLength=24, driftFade=True, driftGrow=1.6)),
]

L147_DIFFS = [
    ("lantern", 140, 160, 0),
    ("osmanthus", 790, 230, 0),
    ("mooncake", 400, 450, 0),
    ("rabbit", 712, 530, 0),
    ("cat", 182, 236, 0),
]


# =================================================================== Level 148 Halloween street at dusk
def l148_bg(c, d):
    sky(c, (70, 50, 110), (240, 140, 90))
    soft_union(c, [Circ(760, 90, 40)], (255, 240, 190), 0.4, spread=40)
    npiece(c, Circ(760, 90, 34), (252, 240, 200), shadow=None)
    far_skyline(c, 300, 40, 90, (90, 70, 110), 1481)
    for k, (x, w, h, wall, roof) in enumerate(((110, 180, 160, (120, 100, 130), (60, 50, 70)), (340, 200, 180, (150, 110, 90), (70, 50, 60)),
                                               (580, 180, 150, (100, 120, 130), (50, 56, 70)), (800, 180, 170, (140, 120, 110), (60, 50, 60)))):
        house(c, x, 450, w, h, wall, roof, door=None, win=(255, 210, 110), wins=2)
        door = (80, 50, 40) if not (k == 1 and "door" in d) else (60, 130, 90)
        npiece(c, RRect(x - 18, 400, x + 18, 452, 3), door, border=1, shadow=SMALL)
        flat(c, Circ(x + 10, 428, 2.4), (240, 200, 90))
    # porch pumpkins
    for k, (x, s) in enumerate(((60, 1.6), (300, 1.4), (390, 1.8), (630, 1.5), (850, 1.6))):
        pumpkin(c, x, 470, s, col=(226, 120, 40) if not (k == 2 and "pumpkin" in d) else (236, 230, 220), face=True)
    # bare tree + fence
    dead_tree(c, 470, 470, 1.6, col=(50, 40, 56))
    flat(c, Thick(0, 480, W, 480, 3), (60, 50, 66))
    for x in range(0, W, 24):
        flat(c, [Poly([(x - 4, 506), (x + 4, 506), (x + 4, 470), (x, 462), (x - 4, 470)])], (60, 50, 66))
    if "web" not in d:
        for k in range(5):
            a = math.radians(180 + k * 22)
            flat(c, Thick(860, 470, 860 + 40 * math.cos(a), 470 + 40 * math.sin(a) * -1, 1), (230, 230, 240))
        for r in (14, 26, 38):
            c.ellipse_ring(860, 470, r, r, 1, (230, 230, 240), ymin=430, ymax=470)
    # pavement
    c.rect(0, 506, W, H, (90, 80, 100))
    for x in range(0, W, 90):
        flat(c, Thick(x, 506, x - 20, H, 1.4), (76, 68, 86))
    flat(c, Thick(0, 506, W, 506, 3), (110, 100, 120))
    # trick-or-treaters
    # ghost
    npiece(c, [Poly([(130, 594), (180, 594), (176, 520), (155, 496), (134, 520)])], (246, 246, 250))
    flat(c, [Ell(148, 524, 4, 6), Ell(164, 524, 4, 6)], INK)
    # witch
    modern(c, 300, 596, (80, 40, 110), bottom=(40, 30, 50), hair=(200, 120, 60), h=2.0, style="long", skirt=True)
    hat = (40, 30, 50) if "hat" not in d else (60, 140, 90)
    npiece(c, [Ell(302, 506, 26, 5), Poly([(288, 506), (316, 506), (310, 470), (320, 456)])], hat, border=1, shadow=SMALL)
    flat(c, Thick(326, 596, 330, 520, 2), (110, 80, 60))
    # pumpkin costume kid
    modern(c, 470, 596, (240, 140, 40), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.0)
    npiece(c, Ell(470, 548, 26, 22), (240, 140, 40), border=1, shadow=SMALL)
    flat(c, [Poly([(460, 544), (466, 544), (463, 536)]), Poly([(474, 544), (480, 544), (477, 536)])], (60, 40, 30))
    # candy bucket
    bucket = (240, 140, 40) if "bucket" not in d else (120, 90, 200)
    npiece(c, [RRect(500, 554, 526, 580, 4)], bucket, border=1, shadow=SMALL)
    flat(c, Thick(500, 556, 526, 556, 2), (60, 40, 30))
    # adult with a lantern
    modern(c, 700, 596, (60, 90, 70), bottom=(50, 50, 60), hair=(60, 40, 30), h=2.3)
    flat(c, Thick(712, 520, 728, 506, 2), (40, 40, 46))
    npiece(c, [RRect(720, 504, 736, 528, 2)], (60, 56, 70), border=1, shadow=SMALL)
    flat(c, RRect(723, 508, 733, 524, 1), (255, 210, 120))
    # black cat on the fence
    npiece(c, [Ell(590, 456, 18, 9), Circ(606, 446, 8), Poly([(600, 440), (602, 430), (606, 440)]), Poly([(608, 440), (612, 430), (613, 444)])],
           (30, 26, 34), border=1, shadow=SMALL)
    flat(c, [Circ(604, 446, 1.6), Circ(610, 446, 1.6)], (250, 220, 80))


L148_ELEMENTS = [
    E("bat%d" % i, (lambda x, y: lambda c, m: flat(c, [Poly([(x, y), (x - 14, y - 6), (x - 10, y + 2), (x - 18, y + 4), (x, y + 6), (x + 18, y + 4),
                                                             (x + 10, y + 2), (x + 14, y - 6)])], (30, 24, 40)))(x, y),
      pivot=(x, y), daynight="untinted", anim=dict(orbitRadius=(30, 12), orbitSpeed=0.18, phase=i * 0.33))
    for i, (x, y) in enumerate(((200, 70), (500, 50), (640, 160)))
] + [
    E("glow%d" % i, (lambda x: lambda c, m: soft_union(c, [Circ(x, 456, 12)], (255, 170, 60), 0.5, spread=18))(x), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=2.0, phase=i * 0.2)) for i, x in enumerate((60, 300, 630, 850))
] + flame("lantern", 728, 520, 0.8, glow_night=False) + [
    E("tail", lambda c, m: flat(c, Thick(574, 458, 560, 440, 3), (30, 26, 34)), pivot=(574, 458), anim=dict(swingAngle=14, swingSpeed=0.6)),
]

L148_DIFFS = [
    ("door", 340, 426, 0),
    ("pumpkin", 390, 450, 0),
    ("web", 860, 450, 0),
    ("hat", 304, 486, 0),
    ("bucket", 513, 567, 0),
]


# =================================================================== Level 149 Christmas Eve living room
WALL149 = (200, 220, 200)


def l149_bg(c, d):
    wallpaper_stripes(c, (0, 0, W, 430), WALL149, (190, 212, 190), w=40)
    flat(c, RRect(0, 0, W, 14, 0), (240, 236, 220))
    flat(c, Thick(0, 16, W, 16, 4), (190, 60, 60))
    # snowy window
    flat(c, RRect(600, 60, 820, 270, 0), (40, 50, 90))
    piece(c, hill_strip(240, [(8, 0.03, 0.3)], x0=600, x1=820, bottom=270), (240, 244, 250), shadow=None)
    for x in (630, 700, 780):
        tree_pine(c, x, 250, 50, col=(40, 70, 70), snow=(240, 244, 250))
    piece(c, [RRect(590, 50, 830, 60, 0), RRect(590, 50, 600, 280, 0), RRect(820, 50, 830, 280, 0), RRect(707, 60, 713, 270, 0),
              RRect(582, 270, 838, 282, 1)], (246, 242, 230), shadow=SMALL)
    flat(c, [Ell(650, 270, 40, 6), Ell(780, 270, 40, 6)], (250, 250, 252))
    # wreath on the wall
    piece(c, Circ(450, 110, 44), (50, 110, 70), shadow=PROP)
    flat(c, Circ(450, 110, 24), WALL149)
    rnd = random.Random(1491)
    for _ in range(14):
        a = rnd.uniform(0, 2 * math.pi)
        flat(c, Circ(450 + 34 * math.cos(a), 110 + 34 * math.sin(a), 4), (220, 50, 50))
    bow = (220, 50, 50) if "bow" not in d else (240, 200, 60)
    piece(c, [Poly([(450, 150), (428, 138), (428, 162)]), Poly([(450, 150), (472, 138), (472, 162)]), Circ(450, 150, 6)], bow, shadow=SMALL)
    # fireplace with stockings
    piece(c, [RRect(320, 230, 580, 246, 2), RRect(334, 246, 566, 430, 0)], (180, 90, 70), border=1.5, shadow=PROP)
    for y in range(256, 430, 16):
        off = 0 if (y // 16) % 2 else 18
        flat(c, Thick(334, y, 566, y, 1), (160, 76, 60))
        for x in range(334 + off, 566, 36):
            flat(c, Thick(x, y, x, y + 16, 1), (160, 76, 60))
    flat(c, RRect(390, 300, 510, 430, 50), (40, 30, 30))
    piece(c, [Thick(410, 422, 490, 414, 9)], (110, 70, 46), shadow=SMALL)
    for k, x in enumerate((360, 450, 540)):
        col = [(220, 50, 50), (60, 130, 80), (220, 50, 50)][k]
        if k == 2 and "stocking" in d:
            col = (70, 110, 200)
        piece(c, [RRect(x - 10, 246, x + 10, 296, 2), Ell(x + 6, 296, 16, 10)], col, border=1.2, shadow=SMALL)
        flat(c, RRect(x - 12, 246, x + 12, 258, 2), (250, 250, 246))
    # candles + clock on the mantel
    for x in (340, 560):
        piece(c, RRect(x - 5, 204, x + 5, 230, 1), (246, 240, 226), shadow=SMALL)
    # floor + rug
    planks(c, 430, (150, 100, 66), (130, 86, 56), seed=149)
    piece(c, Ell(450, 540, 330, 40), (170, 50, 60), shadow=SMALL)
    c.ellipse_ring(450, 540, 310, 34, 4, (240, 220, 160))
    # Christmas tree (left)
    tcol = (50, 120, 80)
    piece(c, [Poly([(160, 60), (70, 220), (250, 220)]), Poly([(160, 140), (40, 340), (280, 340)]), Poly([(160, 240), (20, 450), (300, 450)])], tcol,
          border=1.5, shadow=PROP)
    piece(c, Poly([(110, 450), (210, 450), (200, 500), (120, 500)]), (180, 60, 50), border=1.5, shadow=PROP)
    flat(c, [Thick(80, 200, 240, 170, 3), Thick(60, 320, 270, 280, 3), Thick(40, 430, 290, 390, 3)], (240, 210, 90))
    rnd = random.Random(1492)
    for k, (x, y) in enumerate(((120, 180), (190, 196), (100, 300), (180, 260), (230, 320), (80, 410), (150, 380), (240, 430))):
        col = rnd.choice([(220, 50, 50), (70, 120, 210), (240, 200, 60), (230, 230, 240)])
        if k == 5 and "ornament" in d:
            col = (200, 110, 220)
        piece(c, Circ(x, y, 14), col, border=1, shadow=SMALL)
    # gifts under the tree
    gift(c, 60, 530, 70, 50, (60, 120, 200))
    gift(c, 150, 540, 60, 70, (220, 60, 60) if "gift" not in d else (240, 200, 60), ribbon=(250, 250, 246))
    gift(c, 240, 520, 56, 40, (120, 180, 110), ribbon=(220, 50, 50))
    gift(c, 300, 560, 64, 44, (240, 230, 210), ribbon=(60, 120, 80))
    # armchair + side table with cookies and milk
    piece(c, [RRect(680, 360, 830, 470, 26), RRect(660, 420, 704, 560, 16), RRect(806, 420, 850, 560, 16), RRect(690, 460, 820, 548, 8)],
          (120, 60, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(668, 560, 668, 576, 5), Thick(842, 560, 842, 576, 5)], (70, 50, 40))
    piece(c, [Ell(600, 470, 40, 8), Thick(600, 470, 600, 560, 5), Ell(600, 562, 22, 5)], (110, 70, 46), border=1.2, shadow=PROP)
    piece(c, Ell(588, 462, 24, 5), (246, 246, 242), border=1, shadow=SMALL)
    cookies = (200, 140, 80) if "cookies" not in d else (250, 250, 246)
    for k in range(3):
        piece(c, Circ(576 + k * 12, 454 - (k % 2) * 4, 8), cookies, shadow=SMALL)
    piece(c, RRect(612, 436, 628, 468, 2), (250, 250, 250), border=1, shadow=SMALL)
    # teddy bear in the armchair
    piece(c, [Ell(756, 450, 26, 24), Circ(756, 414, 18), Circ(742, 400, 7), Circ(770, 400, 7), Ell(736, 470, 9, 7), Ell(776, 470, 9, 7)],
          (200, 150, 100), border=1.2, shadow=SMALL)
    flat(c, [Circ(750, 412, 2), Circ(762, 412, 2), Circ(756, 420, 3)], INK)
    flat(c, Poly([(744, 432), (768, 432), (756, 440)]), (220, 50, 50))


L149_ELEMENTS = [
    E("star", lambda c, m: (soft_union(c, [Circ(160, 52, 18)], (255, 230, 140), 0.5, spread=16),
                            piece(c, Poly(star_pts(160, 52, 22, 9)), (250, 210, 60), border=1.2, shadow=SMALL)),
      pivot=(160, 52), daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=0.8, pulse=0.05, scaleSpeed=0.8)),
    E("cat", lambda c, m: (piece(c, [Ell(470, 470, 30, 12), Circ(498, 462, 11), Poly([(490, 456), (492, 442), (498, 454)]),
                                     Poly([(502, 454), (508, 442), (509, 458)])], (240, 240, 236), border=1.2, shadow=SMALL),
                           flat(c, [Thick(492, 462, 497, 464, 1.4), Thick(501, 464, 506, 462, 1.4)], INK)),
      pivot=(470, 480), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
] + flame("fire", 450, 414, 2.4, glow_night=False) + flame("fire2", 424, 416, 1.6, glow_night=False) \
  + flame("fire3", 478, 416, 1.8, glow_night=False) + flame("candleL", 340, 204, 0.6, glow_night=False) + flame("candleR", 560, 204, 0.6, glow_night=False) + [
    E("snow%d" % i, (lambda x: lambda c, m: flat(c, Circ(x, 70, 3), (250, 250, 252)))(x), daynight="untinted",
      anim=dict(driftVelocity=(3, 22), driftLength=180, driftFade=True, phase=i / 7)) for i, x in enumerate((612, 640, 668, 692, 730, 760, 796))
] + [
    E("lights", lambda c, m: [flat(c, Circ(x, y, 4), col) for x, y, col in
                              ((100, 192, (255, 120, 120)), (140, 184, (255, 230, 120)), (210, 176, (140, 220, 255)), (80, 314, (255, 230, 120)),
                               (130, 304, (140, 220, 255)), (200, 292, (255, 120, 120)), (250, 284, (255, 230, 120)), (60, 424, (255, 120, 120)),
                               (110, 416, (140, 220, 255)), (170, 406, (255, 230, 120)), (230, 398, (255, 120, 120)), (280, 392, (140, 220, 255)))],
      daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=1.5)),
]

L149_DIFFS = [
    ("bow", 450, 150, 0),
    ("stocking", 546, 280, 0),
    ("ornament", 80, 410, 0),
    ("gift", 150, 505, 0),
    ("cookies", 588, 452, 0),
]


# =================================================================== Level 150 Christmas market (snow showers)
STEPS150 = [(CLEAR, 10), (SNOW, 14)]


def timber_house(c, x0, x1, base, h, wall, beam, roof, seed, shutters=None):
    piece(c, RRect(x0, base - h, x1, base, 1), wall, border=1.5, shadow=PROP)
    piece(c, Poly([(x0 - 8, base - h + 2), (x1 + 8, base - h + 2), ((x0 + x1) / 2, base - h - (x1 - x0) * 0.55)]), roof, border=1.5, shadow=PROP)
    flat(c, [Poly([(x0 - 8, base - h + 2), (x1 + 8, base - h + 2), (x1 + 2, base - h - 4), (x0 - 2, base - h - 4)])], (246, 248, 252))
    flat(c, [Thick(x0, base - h * 0.5, x1, base - h * 0.5, 4), Thick(x0 + 4, base - h, x0 + 4, base, 4), Thick(x1 - 4, base - h, x1 - 4, base, 4)], beam)
    flat(c, [Thick(x0 + 4, base - h * 0.5, (x0 + x1) / 2, base - h, 3), Thick(x1 - 4, base - h * 0.5, (x0 + x1) / 2, base - h, 3)], beam)
    for k in range(2):
        wx = x0 + (x1 - x0) * (k + 1) / 3
        flat(c, RRect(wx - 10, base - h * 0.4, wx + 10, base - h * 0.4 + 24, 2), (255, 220, 140))
        sc = shutters or lit(roof, 1.1)
        flat(c, [RRect(wx - 18, base - h * 0.4, wx - 11, base - h * 0.4 + 24, 1), RRect(wx + 11, base - h * 0.4, wx + 18, base - h * 0.4 + 24, 1)], sc)


def stall(c, x, base, w, stripe, goods_col, seed, roof_h=40):
    x0, x1 = x - w / 2, x + w / 2
    piece(c, [RRect(x0, base - 70, x1, base, 2)], (170, 120, 76), border=1.5, shadow=PROP)
    flat(c, [Thick(x0 + 6, base - 70, x0 + 6, base - 130, 4), Thick(x1 - 6, base - 70, x1 - 6, base - 130, 4)], (130, 90, 60))
    pts = [(x0 - 10, base - 130), (x1 + 10, base - 130), (x, base - 130 - roof_h)]
    piece(c, Poly(pts), (250, 250, 246), border=1.5, shadow=PROP)
    n = 6
    for k in range(0, n, 2):
        a0, a1 = x0 - 10 + (w + 20) * k / n, x0 - 10 + (w + 20) * (k + 1) / n
        flat(c, Poly([(a0, base - 130), (a1, base - 130), (x, base - 130 - roof_h)]), stripe)
    flat(c, [Poly([(x0 - 10, base - 130), (x1 + 10, base - 130), (x1 + 6, base - 136), (x0 - 6, base - 136)])], (246, 248, 252))
    rnd = random.Random(seed)
    for k in range(int(w // 22)):
        flat(c, Circ(x0 + 14 + k * 22, base - 78, 8), goods_col if rnd.random() < 0.7 else lit(goods_col, 1.3))


def l150_bg(c, d):
    sky(c, (150, 170, 200), (220, 226, 236))
    far_skyline(c, 260, 40, 110, (180, 186, 204), 1501)
    for k, (x0, x1, h, wall, roof) in enumerate(((-10, 140, 190, (240, 226, 200), (150, 60, 50)), (140, 270, 220, (226, 200, 170), (80, 70, 80)),
                                                 (630, 770, 210, (236, 220, 196), (120, 60, 60)), (770, 910, 180, (220, 210, 190), (70, 80, 100)))):
        timber_house(c, x0, x1, 340, h, wall, (110, 70, 50), roof, 1500 + k,
                     shutters=(60, 120, 80) if (k == 2 and "shutter" in d) else None)
    # big tree in the middle
    piece(c, [Poly([(450, 60), (380, 170), (520, 170)]), Poly([(450, 120), (350, 260), (550, 260)]), Poly([(450, 200), (320, 350), (580, 350)])],
          (40, 100, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(392, 160, 508, 150, 2.4), Thick(366, 250, 534, 236, 2.4), Thick(336, 340, 564, 326, 2.4)], (240, 210, 90))
    flat(c, RRect(440, 350, 460, 380, 2), (110, 70, 50))
    # square cobbles
    c.rect(0, 340, W, H, (190, 186, 190))
    for y in range(350, H, 18):
        off = 0 if (y // 18) % 2 else 16
        for x in range(off, W, 32):
            flat(c, Ell(x, y, 13, 6), (176, 172, 178))
    flat(c, RRect(0, 340, W, 350, 0), (244, 246, 250))
    # stalls
    stall(c, 150, 480, 180, (200, 50, 50), (190, 120, 60), 1502)
    stall(c, 450, 470, 160, (60, 120, 80) if "stall" not in d else (70, 110, 200), (220, 60, 60), 1503)
    stall(c, 750, 480, 180, (200, 50, 50), (240, 200, 90), 1504)
    # gingerbread hearts on the left stall
    for k, x in enumerate((90, 130, 170, 210)):
        col = (170, 100, 50) if not (k == 2 and "heart" in d) else (230, 120, 160)
        flat(c, Thick(x, 350, x, 364, 1), (200, 50, 50))
        piece(c, [Circ(x - 6, 370, 8), Circ(x + 6, 370, 8), Poly([(x - 13, 373), (x + 13, 373), (x, 388)])], col, shadow=SMALL)
    # shoppers
    for x, top, hair, h, style in ((300, (60, 90, 150), (90, 60, 40), 2.2, "short"), (360, (200, 60, 60), (200, 160, 90), 2.0, "long"),
                                   (580, (90, 120, 80), (40, 30, 30), 2.3, "short"), (870, (150, 100, 160), (40, 30, 30), 2.1, "long")):
        hx, hy = modern(c, x, 590, top, bottom=(50, 50, 60), hair=hair, h=h, style=style)
        flat(c, RRect(hx - 9 * h, hy + 8 * h, hx + 9 * h, hy + 12 * h, 2), (240, 240, 236))
    scarf = (240, 200, 60) if "scarf" not in d else (90, 160, 220)
    flat(c, [RRect(348, 512, 378, 524, 3), RRect(366, 518, 376, 548, 2)], scarf)
    hx, hy = modern(c, 50, 594, (120, 60, 60), bottom=(50, 50, 60), hair=(220, 220, 226), h=2.4)
    piece(c, RRect(10, 520, 40, 550, 3), (200, 160, 100), shadow=SMALL)
    # lamp post with wreath
    flat(c, Thick(640, 600, 640, 380, 5), (50, 50, 60))
    piece(c, RRect(626, 360, 654, 386, 3), (50, 50, 60), shadow=SMALL)
    piece(c, Circ(640, 430, 16), (50, 110, 70), shadow=SMALL)
    flat(c, Circ(640, 430, 8), (50, 50, 60))
    flat(c, Poly([(640, 444), (630, 452), (650, 452)]), (220, 50, 50))


L150_ELEMENTS = [
    cloud("cloudA", 200, 40, 1.2, (220, 226, 236), W_(SNOW)),
    cloud("cloudB", 650, 30, 1.3, (220, 226, 236), W_(SNOW)),
    snow_layer("snow", 150, 70, 2.0, 4.0, 40),
    E("star", lambda c, m: piece(c, Poly(star_pts(450, 56, 18, 7)), (250, 210, 60), border=1.2, shadow=SMALL), pivot=(450, 56), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.8)),
    lights_el("treelights", [(400, 158), (440, 156), (480, 152), (380, 248), (420, 244), (460, 240), (500, 238), (360, 338), (400, 334), (440, 332),
                             (480, 330), (520, 328)], [(255, 120, 120), (255, 230, 120), (140, 220, 255)]),
    lights_el("lamp", [(640, 373)], [(255, 230, 150)], r=8),
] + steam("mulled", 760, 400, n=3, r=6)

L150_DIFFS = [
    ("shutter", 700, 254, 0),
    ("stall", 450, 360, 0),
    ("heart", 170, 376, 0),
    ("scarf", 363, 526, 0),
]


# =================================================================== Level 151 backyard birthday party
def l151_bg(c, d):
    sky(c, (140, 200, 240), (210, 234, 246))
    cloud_bg(c, 150, 60, 1.0)
    cloud_bg(c, 720, 80, 0.9)
    far_round_trees(c, 220, 40, (110, 170, 110), 1511)
    # house back with a door and window
    piece(c, RRect(560, 80, 920, 360, 2), (240, 220, 190), border=1.5, shadow=PROP)
    piece(c, Poly([(540, 90), (940, 90), (900, 40), (580, 40)]), (170, 90, 80), border=1.5, shadow=PROP)
    flat(c, RRect(620, 150, 720, 240, 2), (180, 210, 236))
    flat(c, [Thick(670, 150, 670, 240, 3), Thick(620, 195, 720, 195, 3)], (250, 250, 246))
    flat(c, RRect(780, 200, 850, 360, 3), (120, 80, 60))
    flat(c, Circ(838, 280, 4), (240, 200, 80))
    # picket fence
    for x in range(0, 560, 26):
        piece(c, Poly([(x, 360), (x + 18, 360), (x + 18, 280), (x + 9, 268), (x, 280)]), (250, 250, 246), shadow=SMALL)
    flat(c, [RRect(0, 296, 560, 304, 0), RRect(0, 336, 560, 344, 0)], (236, 236, 230))
    # lawn
    c.rect(0, 360, W, H, (120, 190, 100))
    rnd = random.Random(1512)
    for _ in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(370, 600)
        flat(c, Thick(x, y, x + 2, y - 6, 1.4), (100, 170, 86))
    # bunting
    cols = [(230, 80, 80), (250, 200, 60), (80, 160, 220), (120, 190, 110), (220, 120, 200)]
    bunting(c, 0, 120, 560, 100, cols, 12, sag=40, size=24, swap=(4, (250, 250, 246)) if "flag" in d else None)
    # banner on the house
    piece(c, RRect(600, 260, 760, 300, 2), (250, 200, 60) if "banner" not in d else (230, 120, 160), border=1.2, shadow=PROP)
    sign_box(c, 610, 260, 750, 300, (250, 200, 60) if "banner" not in d else (230, 120, 160), 1513, glyph=(200, 60, 60), vertical=False)
    # party table with cloth
    piece(c, [RRect(260, 400, 640, 414, 2), RRect(260, 414, 640, 470, 0)], (250, 250, 246), border=1.5, shadow=PROP)
    for x in range(270, 640, 30):
        flat(c, RRect(x, 414, x + 15, 470, 0), (230, 120, 140))
    flat(c, [RRect(276, 470, 288, 540, 2), RRect(612, 470, 624, 540, 2)], (200, 200, 206))
    cake(c, 450, 400, (250, 240, 230), (250, 170, 200) if "cake" not in d else (150, 100, 70))
    for k in range(4):
        x = 438 + k * 8
        col = [(120, 180, 230), (250, 200, 60), (230, 100, 120), (120, 190, 110)][k]
        flat(c, RRect(x - 1.6, 356, x + 1.6, 368, 1), col)
    gift(c, 330, 400, 50, 40, (90, 140, 220), ribbon=(250, 200, 60))
    gift(c, 560, 400, 44, 50, (240, 120, 80) if "gift" not in d else (120, 190, 110), ribbon=(250, 250, 246))
    piece(c, [RRect(610, 370, 630, 400, 3), Thick(630, 378, 638, 390, 3)], (180, 220, 240), border=1, shadow=SMALL)
    flat(c, RRect(612, 380, 628, 398, 2), (250, 170, 60))
    # kids with party hats
    for x, top, hair, hatc, style in ((180, (230, 90, 90), (90, 60, 40), (80, 160, 220), "short"), (380, (120, 180, 230), (200, 160, 90), (250, 200, 60), "long"),
                                      (520, (250, 200, 60), (40, 30, 30), (230, 90, 120), "twin"), (720, (120, 190, 110), (60, 40, 30), (200, 120, 220), "short")):
        if x == 720 and "shirt" in d:
            top = (250, 140, 40)
        hx, hy = modern(c, x, 590, top, bottom=(60, 70, 100), hair=hair, h=2.2, style=style)
        party_hat(c, hx, hy, 2.2, hatc)
    # dog
    piece(c, [Ell(830, 560, 30, 14), Circ(860, 544, 12), Ell(866, 536, 5, 9), RRect(808, 568, 814, 590, 2), RRect(846, 568, 852, 590, 2)],
          (220, 180, 120), border=1.2, shadow=SMALL)
    flat(c, Circ(866, 546, 2), INK)
    # bucket of water balloons / ball
    piece(c, Circ(90, 560, 20), (250, 250, 246), border=1, shadow=SMALL)
    flat(c, [Poly([(76, 548), (90, 540), (104, 548), (90, 560)])], (230, 80, 80))


def l151_balloons(x, y, cols, ph):
    def d(c, m):
        for k, col in enumerate(cols):
            bx = x + (k - (len(cols) - 1) / 2) * 22
            by = y - abs(k - (len(cols) - 1) / 2) * 8
            flat(c, Thick(x, y + 80, bx, by + 16, 1), (90, 90, 100))
            piece(c, [Ell(bx, by, 14, 17), Poly([(bx - 4, by + 18), (bx + 4, by + 18), (bx, by + 13)])], col, border=1, shadow=SMALL)
            flat(c, Ell(bx - 4, by - 6, 3, 5), lit(col, 1.35))
    return E("balloons%d" % x, d, pivot=(x, y + 80), anim=dict(swingAngle=4, swingSpeed=0.4, phase=ph))


L151_ELEMENTS = [
    l151_balloons(270, 300, [(230, 80, 80), (250, 200, 60), (80, 160, 220)], 0.0),
    l151_balloons(630, 300, [(120, 190, 110), (220, 120, 200), (250, 140, 60)], 0.5),
    E("flames", lambda c, m: [flat(c, Poly([(x - 2.4, 356), (x + 2.4, 356), (x, 346)]), (255, 190, 60))
                              for x in (438, 446, 454, 462)], daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=3.0)),
    E("tail", lambda c, m: flat(c, Thick(802, 556, 784, 540, 4), (220, 180, 120)), pivot=(802, 556), anim=dict(swingAngle=20, swingSpeed=1.5)),
] + [E("bubble%d" % i, (lambda x: lambda c, m: piece(c, Circ(x, 520, 7), (220, 236, 250, 0.7), border=1, shadow=None))(x), daynight="untinted",
       anim=dict(driftVelocity=(6, -26), driftLength=150, driftFade=True, bobAmplitude=(4, 0), bobSpeed=0.6, phase=i / 4))
     for i, x in enumerate((60, 76, 90, 104))]

L151_DIFFS = [
    ("flag", 212, 140, 0),
    ("banner", 680, 280, 0),
    ("cake", 450, 380, 0),
    ("gift", 560, 375, 0),
    ("shirt", 720, 528, 0),
]


# =================================================================== Level 152 spring egg hunt
def egg(c, x, y, col, band=None, s=1.0):
    piece(c, Ell(x, y, 10 * s, 13 * s), col, border=1, shadow=SMALL)
    flat(c, Thick(x - 9 * s, y, x + 9 * s, y, 2.6 * s), band or lit(col, 1.3))


def l152_bg(c, d):
    sky(c, (160, 210, 240), (226, 240, 246))
    cloud_bg(c, 200, 70, 1.0)
    layer(c, 230, [(20, 0.01, 0.3), (8, 0.03, 1.4)], (170, 210, 150))
    far_round_trees(c, 250, 30, (120, 180, 110), 1521)
    # cottage + picket fence + birdhouse
    house(c, 760, 330, 160, 120, (250, 240, 220), (120, 160, 200), win=(200, 226, 240))
    for x in range(560, 900, 24):
        piece(c, Poly([(x, 340), (x + 16, 340), (x + 16, 296), (x + 8, 286), (x, 296)]), (250, 250, 246), shadow=SMALL)
    flat(c, Thick(560, 312, 900, 312, 4), (236, 236, 230))
    flat(c, Thick(520, 340, 520, 230, 4), (130, 100, 70))
    bh = (200, 80, 70) if "birdhouse" not in d else (70, 120, 200)
    piece(c, [RRect(500, 190, 540, 232, 3)], (240, 210, 150), border=1.2, shadow=PROP)
    piece(c, Poly([(492, 194), (548, 194), (520, 168)]), bh, border=1.2, shadow=PROP)
    flat(c, Circ(520, 210, 7), (80, 60, 50))
    # meadow
    piece(c, hill_strip(330, [(8, 0.015, 0.4)]), (130, 196, 100), shadow=LAYER)
    rnd = random.Random(1522)
    for _ in range(90):
        x, y = rnd.uniform(0, W), rnd.uniform(350, 600)
        flat(c, Thick(x, y, x + 2, y - 7, 1.4), (110, 176, 86))
    # blossom tree (left)
    blossom_tree(c, 150, 400, 1.6)
    # tulip bed (front centre)
    for k, x in enumerate(range(330, 520, 24)):
        col = [(240, 90, 110), (250, 200, 60), (240, 90, 110), (220, 120, 200)][k % 4]
        if "tulips" in d and k in (2, 3, 4):
            col = (250, 250, 246)
        flat(c, Thick(x, 600, x, 556, 2), (80, 140, 70))
        piece(c, Poly([(x - 8, 556), (x + 8, 556), (x + 8, 542), (x + 4, 548), (x, 538), (x - 4, 548), (x - 8, 542)]), col, shadow=SMALL)
    # painted eggs hidden in the grass
    eggs = [(60, 470, (120, 180, 230)), (250, 420, (250, 200, 80)), (600, 520, (230, 120, 160)), (850, 560, (150, 200, 120))]
    for k, (x, y, col) in enumerate(eggs):
        if k == 2 and "egg" in d:
            continue
        egg(c, x, y, col, s=1.3)
        flat(c, [Thick(x - 12, y + 12, x - 8, y + 2, 2), Thick(x + 12, y + 12, x + 8, y + 2, 2)], (100, 170, 80))
    egg(c, 720, 400, (200, 150, 230) if "egg2" not in d else (250, 160, 60), s=1.4)
    # wheelbarrow with flowers
    wb = (200, 70, 60) if "barrow" not in d else (70, 140, 200)
    piece(c, [Poly([(40, 520), (150, 520), (130, 560), (60, 560)]), Thick(150, 524, 190, 548, 4)], wb, border=1.2, shadow=PROP)
    piece(c, Circ(70, 572, 14), (60, 60, 66), shadow=SMALL)
    for k in range(5):
        flat(c, Circ(60 + k * 18, 512, 8), [(250, 200, 60), (240, 120, 160), (250, 250, 246)][k % 3])
    # kids with baskets
    for x, top, hair, basket, style in ((300, (250, 200, 210), (200, 160, 90), (200, 160, 100), "twin"), (650, (150, 200, 240), (60, 40, 30), (180, 140, 90), "short")):
        hx, hy = modern(c, x, 590, top, bottom=(80, 110, 160), hair=hair, h=2.3, style=style)
        bcol = basket if not (x == 650 and "basket" in d) else (230, 120, 160)
        piece(c, [Poly([(x + 14, 530), (x + 50, 530), (x + 44, 556), (x + 20, 556)])], bcol, border=1.2, shadow=SMALL)
        c.ellipse_ring(x + 32, 530, 18, 22, 2.4, lit(bcol, 0.8), ymax=530)
        for k in range(3):
            egg(c, x + 22 + k * 10, 526, [(240, 120, 160), (120, 180, 230), (250, 200, 80)][k], s=0.6)


def l152_bunny(x, y, col, ph):
    def d(c, m):
        piece(c, [Ell(x, y, 22, 16), Circ(x + 20, y - 12, 11), Ell(x + 16, y - 32, 4, 13), Ell(x + 26, y - 32, 4, 13), Circ(x - 22, y - 2, 6)], col,
              border=1.2, shadow=SMALL)
        flat(c, Circ(x + 25, y - 13, 2), INK)
        flat(c, Circ(x + 31, y - 10, 2), (240, 140, 160))
    return E("bunny%d" % x, d, pivot=(x, y + 16), anim=dict(bobAmplitude=(0, 12), bobSpeed=0.8, bounce=True, phase=ph))


L152_ELEMENTS = [
    l152_bunny(470, 440, (250, 250, 246), 0.0),
    l152_bunny(820, 470, (200, 170, 140), 0.5),
    E("bird", lambda c, m: (piece(c, [Ell(540, 182, 10, 7), Circ(548, 176, 5)], (240, 120, 80), shadow=SMALL),
                            flat(c, Poly([(552, 176), (558, 178), (552, 180)]), (250, 200, 60))), pivot=(540, 190),
      anim=dict(bobAmplitude=(0, 2), bobSpeed=1.2)),
    E("butterfly", lambda c, m: flat(c, [Ell(360, 300, 6, 8), Ell(372, 300, 6, 8)], (250, 190, 60)), pivot=(366, 300),
      anim=dict(orbitRadius=(60, 20), orbitSpeed=0.12, stretch=(0.5, 0), scaleSpeed=3.0)),
    E("petals", lambda c, m: [flat(c, Ell(140 + k * 30, 290 + (k % 3) * 20, 3, 2), (250, 200, 220)) for k in range(5)],
      anim=dict(driftVelocity=(10, 20), driftLength=120, driftFade=True)),
]

L152_DIFFS = [
    ("birdhouse", 520, 198, 0),
    ("tulips", 414, 548, 0),
    ("egg", 600, 520, 0),
    ("egg2", 720, 400, 0),
    ("barrow", 110, 540, 0),
    ("basket", 682, 538, 0),
]


# =================================================================== Level 153 New Year countdown on a city square
def l153_bg(c, d):
    sky(c, (14, 18, 50), (50, 40, 90))
    rnd = random.Random(1531)
    for _ in range(30):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 160)
        flat(c, Circ(x, y, 1.6), (255, 248, 210))
    far_skyline(c, 360, 80, 200, (40, 44, 80), 1532, win=(255, 210, 120))
    # towers with lit tops
    for k, (x0, x1, top) in enumerate(((20, 150, 140), (700, 820, 120))):
        npiece(c, RRect(x0, top, x1, 400, 2), (60, 66, 100), shadow=LAYER)
        for y in range(top + 20, 390, 22):
            for x in range(x0 + 10, x1 - 10, 20):
                flat(c, RRect(x, y, x + 10, y + 12, 1), (255, 214, 120) if (x + y) % 3 else (90, 96, 130))
        crown = (120, 220, 255) if not (k == 1 and "tower" in d) else (255, 120, 180)
        flat(c, RRect(x0, top - 14, x1, top, 2), crown)
    # clock tower in the centre
    npiece(c, [RRect(390, 110, 510, 420, 2), Poly([(380, 112), (520, 112), (450, 30)])], (110, 96, 120))
    face = (250, 244, 220) if "clock" not in d else (180, 230, 250)
    npiece(c, Circ(450, 170, 40), face, shadow=SMALL)
    for k in range(12):
        a = math.radians(k * 30)
        flat(c, Circ(450 + 33 * math.cos(a), 170 + 33 * math.sin(a), 2), INK)
    flat(c, [Thick(450, 170, 450, 138, 3.4), Thick(450, 170, 446, 144, 2.4)], INK)
    for y in (250, 320):
        flat(c, RRect(420, y, 480, y + 40, 20), (255, 210, 120))
    # giant screen (right of the clock)
    npiece(c, RRect(540, 170, 680, 280, 3), (30, 30, 40))
    scr = (120, 60, 160) if "screen" not in d else (40, 140, 100)
    flat(c, RRect(548, 178, 672, 272, 2), scr)
    sign_box(c, 556, 196, 664, 254, scr, 1533, glyph=(255, 230, 120), vertical=False)
    # banner across the square
    flat(c, [Thick(150, 260, 390, 240, 2), Thick(150, 260, 150, 300, 2)], (90, 90, 100))
    ban = (220, 60, 70) if "banner" not in d else (60, 160, 200)
    npiece(c, Poly([(170, 262), (370, 246), (370, 280), (170, 296)]), ban, shadow=SMALL)
    sign_box(c, 190, 258, 350, 284, ban, 1534, glyph=(255, 230, 120), vertical=False)
    # plaza + crowd
    c.rect(0, 400, W, H, (60, 56, 80))
    for y in range(410, H, 24):
        flat(c, Thick(0, y, W, y, 1.4), (70, 66, 92))
    crowd_row(c, 10, 900, 520, 1535, h=1.7, step=36, hats=[(240, 200, 60), (230, 90, 120), (120, 200, 240)])
    crowd_row(c, 30, 880, 600, 1536, h=2.1, step=48, hats=[(240, 200, 60), (230, 90, 120), (120, 200, 240)])
    # hot-drink cart (right front)
    npiece(c, [RRect(760, 500, 880, 570, 3)], (200, 60, 60))
    umb = (250, 200, 60) if "umbrella" not in d else (120, 200, 120)
    npiece(c, Poly([(740, 470), (900, 470), (820, 430)]), umb, shadow=PROP)
    flat(c, Thick(820, 470, 820, 500, 3), (90, 90, 100))
    npiece(c, [Circ(780, 580, 12), Circ(860, 580, 12)], (40, 40, 46), shadow=SMALL)


L153_ELEMENTS = fireworks("fw", ((140, 80, (255, 120, 150), 40), (300, 60, (140, 220, 255), 34), (620, 70, (255, 220, 110), 44),
                                 (800, 60, (200, 150, 255), 34))) \
    + confetti("conf", 1537, 16, 40, 860, 300, [(255, 120, 150), (255, 220, 110), (140, 220, 255), (200, 150, 255)], fall=(4, 36), length=200) + [
    E("glow", lambda c, m: soft_union(c, [Circ(450, 170, 40)], (255, 240, 190), 0.35, spread=26), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.5)),
]

L153_DIFFS = [
    ("tower", 760, 113, 0),
    ("clock", 450, 170, 0),
    ("screen", 610, 225, 0),
    ("banner", 270, 271, 0),
    ("umbrella", 820, 455, 0),
]


# =================================================================== Level 154 carnival parade
def l154_bg(c, d):
    sky(c, (120, 200, 240), (210, 236, 246))
    # colourful row houses with balconies
    cols = [(240, 170, 90), (120, 190, 200), (240, 120, 120), (250, 210, 100), (150, 200, 140), (200, 150, 210)]
    for k, x0 in enumerate(range(-10, 910, 150)):
        wall = cols[k % len(cols)]
        piece(c, RRect(x0, 40, x0 + 150, 400, 0), wall, border=1.5, shadow=PROP)
        flat(c, RRect(x0, 30, x0 + 150, 46, 0), lit(wall, 0.8))
        for y in (80, 220):
            for wx in (x0 + 24, x0 + 90):
                flat(c, RRect(wx, y, wx + 36, y + 60, 3), (70, 80, 100))
                flat(c, [RRect(wx - 6, y, wx, y + 60, 1), RRect(wx + 36, y, wx + 42, y + 60, 1)], lit(wall, 0.7))
        piece(c, RRect(x0 + 16, 280, x0 + 134, 288, 1), (60, 60, 66), shadow=SMALL)
        flat(c, [Thick(x, 288, x, 316, 1.6) for x in range(x0 + 20, x0 + 132, 8)] + [Thick(x0 + 16, 316, x0 + 134, 316, 2)], (60, 60, 66))
        swap = k == 4 and "pot" in d
        piece(c, RRect(x0 + 56, 264, x0 + 94, 282, 2), (200, 80, 60) if not swap else (70, 120, 200), shadow=SMALL)
        flat(c, [Circ(x0 + 62, 258, 8), Circ(x0 + 75, 252, 8), Circ(x0 + 88, 258, 8)], (240, 90, 120) if not swap else (250, 220, 80))
    # balcony spectators
    for x, top in ((100, (250, 250, 246)), (400, (230, 90, 90)), (700, (90, 140, 210))):
        modern(c, x, 290, top, bottom=(60, 60, 80), hair=(40, 30, 30), h=1.4, style="long" if x == 400 else "short")
    # streamers between the houses
    bunting(c, 0, 50, 450, 60, [(250, 200, 60), (230, 80, 80), (80, 160, 220)], 9, sag=50, size=22)
    bunting(c, 450, 60, 900, 50, [(120, 190, 110), (220, 120, 200), (250, 140, 60)], 9, sag=50, size=22, swap=(6, (250, 250, 246)) if "flag" in d else None)
    # street
    c.rect(0, 400, W, H, (200, 190, 176))
    for y in range(410, H, 20):
        off = 0 if (y // 20) % 2 else 20
        for x in range(off, W, 40):
            flat(c, Thick(x, y, x, y + 20, 1.2), (184, 174, 160))
        flat(c, Thick(0, y, W, y, 1.2), (184, 174, 160))
    flat(c, RRect(0, 400, W, 410, 0), (170, 160, 150))
    # peacock float (centre)
    piece(c, [RRect(300, 470, 640, 540, 6)], (250, 200, 60), border=2, shadow=PROP)
    flat(c, [Circ(x, 506, 10) for x in range(320, 640, 30)], (230, 80, 80))
    for k in range(9):
        a = math.radians(200 + k * 17.5)
        tx, ty = 470 + 150 * math.cos(a), 470 + 150 * math.sin(a)
        flat(c, Thick(470, 470, tx, ty, 14), (40, 150, 120))
        tip = (250, 200, 60) if not (k == 6 and "feather" in d) else (230, 80, 80)
        piece(c, Circ(tx, ty, 18), tip, border=1, shadow=SMALL)
        flat(c, Circ(tx, ty, 10), (60, 90, 200))
    piece(c, [Ell(470, 440, 34, 40), Thick(470, 410, 484, 350, 14), Circ(488, 344, 16)], (50, 110, 200), border=1.5, shadow=PROP)
    flat(c, [Circ(494, 340, 3)], INK)
    flat(c, Poly([(502, 344), (516, 348), (502, 352)]), (250, 200, 60))
    piece(c, [Circ(320, 560, 22), Circ(620, 560, 22)], (60, 60, 66), shadow=SMALL)
    # drummers (left)
    for k, x in enumerate((80, 170)):
        modern(c, x, 596, (250, 250, 246), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.2)
        dcol = (230, 60, 60) if not (k == 1 and "drum" in d) else (60, 140, 220)
        piece(c, [Ell(x + 6, 520, 26, 8), RRect(x - 20, 520, x + 32, 556, 3), Ell(x + 6, 556, 26, 8)], dcol, border=1.5, shadow=PROP)
        flat(c, [Thick(x - 18, 524 + j * 10, x + 30, 532 + j * 10, 1.4) for j in range(3)], (250, 250, 246))
    # feather dancers (right)
    for k, (x, dress, plume) in enumerate(((720, (230, 60, 120), (250, 200, 60)), (830, (250, 160, 40), (60, 160, 220)))):
        if k == 1 and "plume" in d:
            plume = (120, 200, 90)
        for j in range(5):
            a = math.radians(220 + j * 25)
            piece(c, Ell(x + 1 + 30 * math.cos(a), 470 + 30 * math.sin(a), 8, 22), plume, shadow=SMALL)
        lady(c, x, 596, dress, hair=(40, 30, 30), h=2.2, wide=1.2)


L154_ELEMENTS = confetti("conf", 1541, 18, 20, 880, 80, [(255, 120, 150), (255, 220, 110), (140, 220, 255), (150, 220, 120)], fall=(6, 40), length=320) + [
    E("sticks", lambda c, m: flat(c, [Thick(96, 540, 120, 506, 3), Thick(186, 540, 210, 506, 3)], (120, 90, 60)), pivot=(140, 540),
      anim=dict(bobAmplitude=(0, 4), bobSpeed=2.4)),
    E("head", lambda c, m: (flat(c, [Thick(484, 330, 480, 312, 2), Thick(490, 330, 494, 312, 2)], (50, 110, 200)),
                            flat(c, [Circ(480, 310, 3), Circ(494, 310, 3)], (250, 200, 60))), pivot=(487, 330), anim=dict(swingAngle=10, swingSpeed=0.8)),
]

L154_DIFFS = [
    ("pot", 670, 268, 0),
    ("flag", 774, 106, 0),
    ("feather", 556, 346, 0),
    ("drum", 176, 538, 0),
    ("plume", 815, 450, 0),
]


LEVELS = [
    ("Level145", "年夜饭", l145_bg, L145_ELEMENTS, L145_DIFFS, 60, OPTS),
    ("Level146", "端午龙舟", l146_bg, L146_ELEMENTS, L146_DIFFS, 60, OPTS),
    ("Level147", "中秋赏月", l147_bg, L147_ELEMENTS, L147_DIFFS, 60, OPTS),
    ("Level148", "万圣节", l148_bg, L148_ELEMENTS, L148_DIFFS, 60, OPTS),
    ("Level149", "圣诞夜", l149_bg, L149_ELEMENTS, L149_DIFFS, 60, OPTS),
    ("Level150", "圣诞集市", l150_bg, L150_ELEMENTS, L150_DIFFS, 60, dict(OPTS, weather=dict(steps=STEPS150, blend=3.0), anim_seconds=24.0, frames=72)),
    ("Level151", "生日派对", l151_bg, L151_ELEMENTS, L151_DIFFS, 60, OPTS),
    ("Level152", "彩蛋寻宝", l152_bg, L152_ELEMENTS, L152_DIFFS, 60, OPTS),
    ("Level153", "新年倒数", l153_bg, L153_ELEMENTS, L153_DIFFS, 60, OPTS),
    ("Level154", "狂欢节游行", l154_bg, L154_ELEMENTS, L154_DIFFS, 60, OPTS),
]
