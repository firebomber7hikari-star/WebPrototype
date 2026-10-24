# -*- coding: utf-8 -*-
"""Mixed themes part 7 (paper-craft side views / interiors, full-bleed, original designs, no brands):
  Level295 养蜂场     - an apiary meadow: row of hives, beekeeper in a veil hat, honey stall, shed, flowers
  Level296 茶园       - a tea plantation: rows of round tea bushes on hills, pickers with back baskets, pavilion
  Level297 城堡厨房   - a castle kitchen: stone hearth with cauldron, hanging pans and hams, table of food, cook
  Level298 潜水艇     - inside a submarine: portholes with fish, pipes and valve wheels, sonar, periscope, captain
  Level299 冰上钓鱼   - ice fishing on a frozen lake: fishing huts, anglers at holes, sled, dog, pines
  Level300 蘑菇村     - a mushroom village: mushroom houses, little forest folk, snails, a well, lanterns
  Level301 月球基地   - a moon base: domes, rover, astronauts, dish antenna, lander, the Earth in the black sky
  Level302 机器人工厂 - a robot factory: conveyor belt, robot arms, half-built robots, warning lights, control booth
  Level303 沙滩城堡   - a sandcastle beach: big sandcastle with flags, bucket and spade, kids, crab, shells
  Level304 海岛度假村 - an island resort at sunset: overwater bungalows, palms, hammock, dock, kayak, drinks
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bubbles_el, bush, cloud_bg, cloud_el, drift_across, fish, layer, palm, rock, sky, stars_bg, sun_bg,
                 tree_pine, tree_round)
from fills import far_forest, far_ridge, far_round_trees
from levels_akiba import modern, sign_box
from levels_festival import npiece
from levels_homes import steam
from levels_mix2 import wheel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def bee_el(eid, x, y, rx, ry, speed):
    def d(c, m):
        piece(c, Ell(x, y, 6, 4), (250, 210, 60), shadow=None)
        flat(c, Thick(x - 1, y - 4, x - 1, y + 4, 1.6), (40, 40, 46))
        flat(c, [Ell(x - 2, y - 6, 4, 3), Ell(x + 3, y - 6, 4, 3)], (240, 250, 255))
    return E(eid, d, pivot=(x, y), anim=dict(orbitRadius=(rx, ry), orbitSpeed=speed))


# =================================================================== Level 295 apiary
def hive(c, x, base, col, levels=3):
    for k in range(levels):
        piece(c, RRect(x - 34, base - 30 * (k + 1), x + 34, base - 30 * k, 2), col if k % 2 == 0 else lit(col, 0.92), border=1.2, shadow=PROP)
    piece(c, Poly([(x - 42, base - 30 * levels + 2), (x + 42, base - 30 * levels + 2), (x + 36, base - 30 * levels - 12), (x - 36, base - 30 * levels - 12)]),
          (200, 200, 206), border=1.2, shadow=SMALL)
    flat(c, RRect(x - 12, base - 8, x + 12, base - 2, 1), (60, 50, 40))


def l295_bg(c, d):
    sky(c, (140, 196, 240), (240, 240, 220), H)
    sun_bg(c, 780, 70, 28)
    cloud_bg(c, 300, 60, 0.6)
    far_ridge(c, 200, 40, (170, 196, 170), 2951)
    far_round_trees(c, 220, 24, (100, 160, 100), 2952)
    # shed (left back)
    piece(c, RRect(40, 150, 200, 260, 2), (190, 150, 100), border=1.5, shadow=PROP)
    for x in range(48, 200, 16):
        flat(c, Thick(x, 154, x, 258, 1.4), (170, 130, 86))
    roof = (90, 120, 90) if "roof" not in d else (200, 80, 70)
    piece(c, Poly([(26, 154), (214, 154), (180, 110), (60, 110)]), roof, border=1.5, shadow=PROP)
    flat(c, RRect(100, 196, 140, 260, 2), (110, 80, 60))
    # meadow
    c.rect(0, 250, W, H, (130, 190, 90))
    layer(c, 250, [(8, 0.01, 0.6), (4, 0.04, 1.0)], (136, 194, 96))
    # hives in a row
    for k, x in enumerate((300, 420, 540, 660)):
        col = [(240, 240, 230), (120, 170, 220), (250, 210, 100), (240, 240, 230)][k]
        if k == 2 and "hive" in d:
            col = (220, 120, 160)
        hive(c, x, 340, col)
    # flower bushes
    for k, x in enumerate((60, 820, 220)):
        bush(c, x, 360 if k < 2 else 420, 1.6, col=(90, 160, 90))
        col = (240, 120, 170) if not (k == 1 and "flower" in d) else (250, 250, 246)
        flat(c, [Circ(x - 14, 340 if k < 2 else 400, 5), Circ(x + 4, 332 if k < 2 else 392, 5), Circ(x + 16, 344 if k < 2 else 404, 5)], col)
    # beekeeper with veil hat (centre)
    hx, hy = modern(c, 470, 520, (250, 250, 246), bottom=(250, 250, 246), hair=(90, 60, 40), h=2.4)
    hat = (240, 230, 200) if "veil" not in d else (90, 110, 90)
    piece(c, [Ell(hx, hy - 12, 30, 6), Ell(hx, hy - 18, 14, 10)], hat, border=1, shadow=SMALL)
    flat(c, Poly([(hx - 24, hy - 10), (hx + 24, hy - 10), (hx + 18, hy + 16), (hx - 18, hy + 16)]), (60, 60, 70, 0.35))
    # smoker in hand
    if "smoker" not in d:
        piece(c, [RRect(500, 430, 526, 474, 4), Poly([(500, 432), (526, 432), (518, 416), (508, 416)])], (190, 190, 200), border=1.2, shadow=SMALL)
    # honey stall (right front)
    piece(c, [RRect(640, 500, 880, 520, 2), RRect(650, 520, 662, 596, 2), RRect(858, 520, 870, 596, 2)], (170, 120, 80), border=1.5, shadow=PROP)
    for k, x in enumerate(range(670, 870, 40)):
        lab = (250, 250, 246) if not (k == 2 and "jar" in d) else (220, 80, 70)
        piece(c, [RRect(x - 14, 464, x + 14, 500, 4), RRect(x - 12, 456, x + 12, 466, 2)], (240, 170, 50), border=1, shadow=SMALL)
        flat(c, RRect(x - 10, 474, x + 10, 490, 2), lab)
    sign = (250, 200, 60) if "sign" not in d else (120, 190, 230)
    piece(c, RRect(700, 410, 820, 450, 4), sign, border=1.2, shadow=SMALL)
    sign_box(c, 712, 418, 808, 442, sign, 2953, glyph=(90, 60, 30), vertical=False)
    # honeycomb frame leaning (left front)
    frame = (240, 180, 60) if "comb" not in d else (160, 110, 60)
    piece(c, RRect(60, 470, 180, 590, 3), (170, 120, 80), border=1.5, shadow=PROP)
    for r in range(5):
        for k in range(5):
            flat(c, Poly([(76 + k * 22 + (r % 2) * 11 + 9 * math.cos(a * math.pi / 3), 490 + r * 20 + 9 * math.sin(a * math.pi / 3)) for a in range(6)]), frame)


L295_ELEMENTS = [
    bee_el("bee1", 360, 260, 60, 20, 0.3),
    bee_el("bee2", 600, 250, 50, 24, -0.25),
    bee_el("bee3", 300, 460, 40, 20, 0.35),
    E("smoke", lambda c, m: piece(c, Circ(513, 412, 8), (236, 236, 236), shadow=None), pivot=(513, 412),
      anim=dict(driftVelocity=(10, -24), driftLength=70, driftFade=True, driftGrow=1.6)),
    bird_el("bird", 500, 70, s=9, speed=-14),
]

L295_DIFFS = [
    ("roof", 120, 130, 0),
    ("hive", 540, 290, 0),
    ("flower", 822, 338, 0),
    ("veil", 472, 395, 0),
    ("smoker", 513, 445, 0),
    ("jar", 750, 482, 0),
    ("sign", 760, 430, 0),
    ("comb", 120, 530, 0),
]


# =================================================================== Level 296 tea plantation
def tea_row(c, y, col, seed, swap=None):
    rnd = random.Random(seed)
    x = -20
    while x < W + 30:
        cc = col if not (swap and swap[0] <= x <= swap[1]) else swap[2]
        r = rnd.uniform(22, 30)
        piece(c, Ell(x, y, r * 1.3, r * 0.8), cc, border=1, shadow=SMALL)
        flat(c, Ell(x - 6, y - 6, r * 0.6, r * 0.3), lit(cc, 1.12))
        x += r * 2.2


def l296_bg(c, d):
    sky(c, (170, 210, 230), (236, 240, 230), H)
    far_ridge(c, 140, 60, (180, 200, 196), 2961)
    far_ridge(c, 190, 40, (150, 184, 170), 2962)
    # pavilion on the hilltop (centre back)
    piece(c, [RRect(424, 150, 430, 190, 1), RRect(470, 150, 476, 190, 1)], (150, 80, 60), shadow=SMALL)
    pav = (180, 60, 50) if "pavilion" not in d else (60, 110, 160)
    piece(c, [Poly([(404, 154), (496, 154), (480, 136), (450, 120), (420, 136)]), RRect(446, 110, 454, 122, 1)], pav, border=1.2, shadow=SMALL)
    layer(c, 190, [(10, 0.01, 0.4), (5, 0.03, 1.0)], (110, 160, 100))
    for k, y in enumerate(range(220, 600, 48)):
        swap = (560, 720, (210, 170, 70)) if (k == 3 and "bush" in d) else None
        tea_row(c, y, (70 + k * 4, 140 + k * 3, 80), 2963 + k, swap=swap)
    # pickers
    for x, base, top, key in ((200, 330, (200, 80, 90), "shirt"), (700, 420, (90, 130, 200), None), (380, 510, (240, 200, 90), None)):
        hx, hy = modern(c, x, base, top if not (key and key in d) else (120, 200, 120), bottom=(60, 60, 70), hair=(30, 30, 34), h=1.9)
        piece(c, Poly([(hx - 18, hy - 4), (hx + 18, hy - 4), (hx, hy - 18)]), (230, 200, 120), border=1, shadow=SMALL)
        bc = (190, 140, 80) if not (x == 700 and "basket" in d) else (90, 160, 200)
        piece(c, Poly([(x - 28, base - 70), (x - 8, base - 70), (x - 10, base - 34), (x - 26, base - 34)]), bc, border=1, shadow=SMALL)
        flat(c, Ell(x - 18, base - 72, 12, 5), (90, 150, 80))
    # parasol (left front)
    para = (240, 120, 90) if "parasol" not in d else (250, 250, 246)
    flat(c, Thick(90, 600, 100, 480, 3), (120, 90, 60))
    piece(c, Poly([(30, 494), (170, 484), (100, 440)]), para, border=1.5, shadow=PROP)
    # tea cart with sacks (right front)
    cart = (150, 110, 70) if "cart" not in d else (90, 120, 160)
    piece(c, RRect(700, 520, 860, 560, 3), cart, border=1.5, shadow=PROP)
    flat(c, Thick(860, 530, 900, 510, 4), (120, 90, 60))
    for x in (730, 780, 830):
        piece(c, [Ell(x, 510, 24, 18)], (230, 220, 190), border=1, shadow=SMALL)
    for x in (730, 830):
        wheel(c, x, 572, 16, tyre=(100, 76, 56), hub=(200, 170, 120))


L296_ELEMENTS = [
    cloud_el("mist", 200, 200, 0.6, 6, col=(240, 244, 240)),
    cloud_el("mist2", 640, 170, 0.5, -5, col=(240, 244, 240)),
    bird_el("bird", 300, 70, s=9, speed=14),
    E("bfly", lambda c, m: piece(c, [Ell(560, 300, 7, 10), Ell(572, 300, 7, 10)], (250, 200, 60), shadow=None), pivot=(566, 300),
      anim=dict(orbitRadius=(40, 20), orbitSpeed=0.15, stretch=(0.6, 0), scaleSpeed=5)),
]

L296_DIFFS = [
    ("pavilion", 450, 134, 0),
    ("shirt", 200, 290, 0),
    ("basket", 682, 368, 0),
    ("bush", 640, 364, 0),
    ("parasol", 100, 470, 0),
    ("cart", 780, 530, 0),
]


# =================================================================== Level 297 castle kitchen
STONE = (150, 140, 130)


def l297_bg(c, d):
    c.rect(0, 0, W, 460, STONE)
    rnd = random.Random(2971)
    for r, y in enumerate(range(0, 460, 30)):
        for x in range(-((r % 2) * 30), W, 60):
            flat(c, RRect(x + 2, y + 2, x + 58, y + 28, 4), lit(STONE, rnd.uniform(0.92, 1.06)))
    # window (left top)
    win = (170, 210, 236) if "window" not in d else (250, 200, 130)
    piece(c, Poly([(60, 200), (60, 80)] + [(110 + 50 * math.cos(math.pi * k / 10), 80 - 40 * math.sin(math.pi * k / 10)) for k in range(10, -1, -1)] + [(160, 200)]),
          (110, 100, 90), border=1.5, shadow=PROP)
    flat(c, Poly([(70, 196), (70, 84)] + [(110 + 40 * math.cos(math.pi * k / 10), 84 - 32 * math.sin(math.pi * k / 10)) for k in range(10, -1, -1)] + [(150, 196)]), win)
    flat(c, [Thick(110, 52, 110, 196, 3), Thick(70, 130, 150, 130, 3)], (110, 100, 90))
    # hearth (centre)
    piece(c, [RRect(300, 120, 600, 160, 2), RRect(300, 160, 340, 420, 2), RRect(560, 160, 600, 420, 2)], (120, 110, 100), border=1.5, shadow=PROP)
    flat(c, RRect(340, 160, 560, 420, 0), (40, 30, 30))
    for k in range(3):
        piece(c, Thick(380 + k * 40, 410, 420 + k * 40, 396, 8), (110, 70, 50), shadow=None)
    flat(c, Thick(450, 160, 450, 290, 3), (60, 60, 70))
    piece(c, [Ell(450, 320, 60, 40), Ell(450, 290, 62, 10)], (60, 60, 66), border=1.2, shadow=SMALL)
    flat(c, Ell(450, 290, 54, 7), (140, 170, 90))
    # hanging pans (right top)
    flat(c, Thick(640, 60, 880, 60, 4), (90, 70, 60))
    for k, x in enumerate((670, 740, 820)):
        col = (200, 120, 70) if not (k == 1 and "pan" in d) else (90, 90, 100)
        flat(c, Thick(x, 60, x, 90, 2), (60, 60, 70))
        piece(c, [Thick(x, 90, x, 110, 4), Circ(x, 136, 26)], col, border=1.2, shadow=SMALL)
    # hams + onions hanging (left middle)
    flat(c, Thick(180, 220, 280, 220, 3), (90, 70, 60))
    if "ham" not in d:
        piece(c, [Ell(210, 270, 18, 32), Thick(210, 222, 210, 240, 3)], (200, 110, 90), border=1.2, shadow=SMALL)
    piece(c, [Ell(254, 266, 16, 28), Thick(254, 222, 254, 240, 3)], (200, 110, 90), border=1.2, shadow=SMALL)
    onion = (230, 200, 140) if "onion" not in d else (160, 80, 140)
    for k in range(4):
        piece(c, Circ(700 + k * 6 * (k % 2), 220 + k * 20, 11), onion, border=1, shadow=None)
    flat(c, Thick(704, 200, 704, 290, 2), (150, 120, 80))
    # shelf with jars (right middle)
    piece(c, RRect(760, 300, 890, 312, 2), (130, 90, 60), shadow=PROP)
    for k, x in enumerate((780, 820, 860)):
        col = [(200, 120, 80), (120, 160, 120), (220, 200, 140)][k]
        if k == 1 and "jar" in d:
            col = (90, 120, 200)
        piece(c, [RRect(x - 14, 262, x + 14, 300, 4), RRect(x - 10, 254, x + 10, 264, 2)], col, border=1, shadow=SMALL)
    # floor
    c.rect(0, 460, W, H, (120, 100, 80))
    for x in range(0, W, 80):
        flat(c, Thick(x, 460, x - 40, H, 2), (110, 90, 70))
    # table with food (centre front)
    piece(c, [RRect(260, 470, 640, 490, 3), RRect(280, 490, 296, 590, 2), RRect(604, 490, 620, 590, 2)], (150, 100, 60), border=1.5, shadow=PROP)
    piece(c, Ell(330, 456, 40, 16), (220, 170, 90), border=1.2, shadow=SMALL)
    pie = (200, 120, 60) if "pie" not in d else (150, 60, 90)
    piece(c, [Ell(450, 462, 44, 10), Ell(450, 452, 40, 12)], pie, border=1.2, shadow=SMALL)
    flat(c, [Thick(420, 450, 480, 450, 2), Thick(430, 444, 470, 458, 2)], lit(pie, 1.2))
    piece(c, Poly([(540, 470), (600, 470), (590, 440)]), (250, 210, 90), border=1, shadow=SMALL)
    # cook
    hx, hy = modern(c, 720, 600, (200, 80, 70), bottom=(60, 50, 50), hair=(90, 60, 40), h=2.6)
    apron = (250, 250, 246) if "apron" not in d else (240, 200, 90)
    piece(c, Poly([(700, 520), (742, 520), (748, 590), (694, 590)]), apron, border=1, shadow=None)
    piece(c, [Ell(hx, hy - 14, 18, 10)], (250, 250, 246), shadow=SMALL)
    # barrels (left front)
    for k, x in enumerate((80, 170)):
        band = (80, 80, 90) if not (k == 0 and "barrel" in d) else (220, 180, 60)
        piece(c, Ell(x, 548, 40, 50), (150, 100, 60), border=1.5, shadow=PROP)
        flat(c, [Thick(x - 38, 524, x + 38, 524, 4), Thick(x - 38, 572, x + 38, 572, 4)], band)
    # cat by the hearth
    piece(c, [Ell(840, 580, 30, 12), Circ(866, 566, 11)], (60, 60, 70), border=1.2, shadow=SMALL)


L297_ELEMENTS = [
    E("fire", lambda c, m: [flat(c, Poly([(390, 400), (510, 400), (480, 340), (450, 360), (420, 336)]), (250, 140, 40)),
                            flat(c, Poly([(420, 400), (480, 400), (460, 360), (440, 370)]), (255, 220, 110))], pivot=(450, 400), daynight="untinted",
      anim=dict(stretch=(0.1, 0.3), scaleSpeed=4)),
    E("glow", lambda c, m: soft_union(c, [Circ(450, 380, 50)], (255, 160, 60), 0.3, spread=50), daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.2)),
    E("bubble", lambda c, m: flat(c, Circ(440, 288, 4), (190, 220, 140)), pivot=(440, 288), anim=dict(driftVelocity=(0, -16), driftLength=30, driftFade=True)),
] + steam("stm", 460, 280, n=3, r=8)

L297_DIFFS = [
    ("window", 110, 130, 0),
    ("pan", 740, 130, 0),
    ("ham", 210, 260, 0),
    ("onion", 706, 250, 0),
    ("jar", 820, 280, 0),
    ("pie", 450, 455, 0),
    ("apron", 721, 555, 0),
    ("barrel", 80, 548, 0),
]


# =================================================================== Level 298 submarine
METAL = (120, 130, 130)


def valve(c, x, y, r, col):
    piece(c, Circ(x, y, r), col, border=1.2, shadow=SMALL)
    flat(c, Circ(x, y, r * 0.7), (60, 60, 66))
    for k in range(4):
        a = k * math.pi / 4
        flat(c, Thick(x - r * 0.7 * math.cos(a), y - r * 0.7 * math.sin(a), x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a), 3), col)


def l298_bg(c, d):
    c.rect(0, 0, W, H, (70, 90, 90))
    for x in range(0, W, 120):
        flat(c, Thick(x, 0, x, H, 3), (60, 78, 78))
    for y in (40, 460):
        piece(c, RRect(0, y - 10, W, y + 10, 2), METAL, shadow=SMALL)
        for x in range(20, W, 40):
            flat(c, Circ(x, y, 3), lit(METAL, 0.8))
    # portholes
    for k, x in enumerate((160, 740)):
        fr = (200, 160, 70) if not (k == 1 and "porthole" in d) else (160, 170, 180)
        piece(c, Circ(x, 170, 78), fr, border=1.5, shadow=PROP)
        flat(c, Circ(x, 170, 62), (30, 90, 130))
        flat(c, Ell(x, 230, 60, 16), (40, 110, 110))
        for j in range(8):
            a = j * math.pi / 4
            flat(c, Circ(x + 70 * math.cos(a), 170 + 70 * math.sin(a), 4), lit(fr, 0.75))
    # pipes along the top
    for y, col in ((70, (190, 90, 60)), (90, (90, 130, 170))):
        flat(c, Thick(0, y, W, y, 10), col)
    flat(c, Thick(300, 70, 300, 300, 10), (190, 90, 60))
    # periscope (centre)
    piece(c, [RRect(430, 50, 470, 300, 4), RRect(400, 260, 500, 300, 6), RRect(400, 290, 420, 320, 3), RRect(480, 290, 500, 320, 3)], (90, 100, 104), border=1.5,
          shadow=PROP)
    # warning lamp (top right of centre)
    lamp = (220, 60, 50) if "lamp" not in d else (90, 200, 90)
    piece(c, [Ell(580, 120, 20, 16), RRect(564, 120, 596, 136, 2)], lamp, border=1.2, shadow=SMALL)
    # valve wheels
    valve(c, 340, 170, 30, (200, 60, 60) if "valve" not in d else (240, 200, 60))
    valve(c, 880, 330, 26, (200, 60, 60))
    # control panel
    piece(c, RRect(30, 300, 380, 460, 4), (90, 100, 100), border=1.5, shadow=PROP)
    sonar = (40, 160, 90) if "sonar" not in d else (60, 140, 200)
    flat(c, Circ(110, 380, 54), (20, 40, 30))
    c.ellipse_ring(110, 380, 50, 50, 4, sonar)
    c.ellipse_ring(110, 380, 30, 30, 3, sonar)
    flat(c, [Thick(60, 380, 160, 380, 2), Thick(110, 330, 110, 430, 2)], sonar)
    for k, x in enumerate((210, 270, 330)):
        col = (240, 236, 220) if not (k == 1 and "dial" in d) else (250, 180, 80)
        piece(c, Circ(x, 350, 22), col, border=1.2, shadow=SMALL)
        flat(c, Thick(x, 350, x + 12, 338, 2), INK)
    for k in range(5):
        flat(c, Circ(200 + k * 34, 420, 7), [(220, 60, 60), (250, 200, 60), (90, 200, 90)][k % 3])
    # chart table (right)
    piece(c, [RRect(600, 360, 860, 380, 2), RRect(620, 380, 632, 470, 2), RRect(828, 380, 840, 470, 2)], (130, 100, 70), border=1.5, shadow=PROP)
    chart = (230, 220, 180) if "map" not in d else (180, 210, 230)
    piece(c, Poly([(620, 362), (840, 362), (830, 330), (630, 330)]), chart, border=1, shadow=None)
    flat(c, [Thick(660, 350, 720, 340, 2), Thick(720, 340, 800, 352, 2)], (200, 80, 70))
    # floor
    c.rect(0, 470, W, H, (60, 66, 70))
    for x in range(0, W, 30):
        flat(c, Thick(x, 470, x, H, 1.4), (70, 76, 80))
    # captain + crew
    hx, hy = modern(c, 520, 600, (40, 60, 100), bottom=(40, 40, 50), hair=(200, 200, 200), h=2.7)
    cap = (40, 50, 80) if "cap" not in d else (250, 250, 246)
    piece(c, [Ell(hx, hy - 12, 20, 8), RRect(hx - 2, hy - 12, hx + 26, hy - 6, 2)], cap, shadow=SMALL)
    flat(c, Circ(hx, hy - 14, 4), (240, 200, 60))
    modern(c, 300, 600, (90, 110, 120), bottom=(40, 40, 50), hair=(60, 40, 30), h=2.5)
    # toolbox (right front)
    tb = (220, 60, 50) if "toolbox" not in d else (60, 120, 200)
    piece(c, [RRect(720, 530, 840, 590, 4), Thick(756, 530, 756, 514, 3), Thick(804, 530, 804, 514, 3), Thick(756, 514, 804, 514, 3)], tb, border=1.5, shadow=PROP)
    # life ring (left front)
    c.ellipse_ring(100, 540, 46, 46, 18, (250, 250, 246))
    for a in (0.6, 2.2, 3.8, 5.4):
        flat(c, Thick(100 + 38 * math.cos(a), 540 + 38 * math.sin(a), 100 + 38 * math.cos(a + 0.5), 540 + 38 * math.sin(a + 0.5), 18), (220, 60, 50))


def porthole_fish(eid, x, col, speed, y):
    return E(eid, lambda c, m: fish(c, x, y, 1.2, col, right=speed > 0), pivot=(x, y), anim=dict(bobAmplitude=(40, 6), bobSpeed=abs(speed)))


L298_ELEMENTS = [
    porthole_fish("f1", 160, (250, 200, 60), 0.2, 160),
    porthole_fish("f2", 740, (240, 120, 60), -0.25, 180),
    E("sweep", lambda c, m: flat(c, Thick(110, 380, 160, 380, 3), (120, 250, 160)), pivot=(110, 380), daynight="untinted", anim=dict(rotateSpeed=90)),
    E("blink", lambda c, m: soft_union(c, [Circ(580, 120, 16)], (255, 120, 100), 0.5, spread=16), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.0)),
] + bubbles_el("bub", 740, 220, n=3, r=4, rise=(1, -24), length=60)

L298_DIFFS = [
    ("porthole", 740, 170, 0),
    ("valve", 340, 170, 0),
    ("lamp", 580, 124, 0),
    ("sonar", 110, 380, 0),
    ("dial", 270, 350, 0),
    ("map", 730, 346, 0),
    ("cap", 530, 450, 0),
    ("toolbox", 780, 556, 0),
]


# =================================================================== Level 299 ice fishing
def fishing_hut(c, x, base, w, h, wall, roof):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), wall, border=1.5, shadow=PROP)
    for y in range(int(base - h) + 10, int(base), 12):
        flat(c, Thick(x - w / 2, y, x + w / 2, y, 1.2), lit(wall, 0.85))
    piece(c, Poly([(x - w / 2 - 8, base - h + 2), (x + w / 2 + 8, base - h + 2), (x, base - h - 30)]), roof, border=1.5, shadow=PROP)
    flat(c, RRect(x - 10, base - 40, x + 10, base, 2), (90, 70, 60))
    flat(c, Poly([(x - w / 2 - 6, base - h + 2), (x, base - h - 26), (x + w / 2 + 6, base - h + 2), (x, base - h - 18)]), (250, 252, 255))


def l299_bg(c, d):
    sky(c, (160, 200, 236), (236, 240, 248), H)
    sun_bg(c, 120, 70, 24, col=(250, 230, 170))
    far_ridge(c, 190, 50, (200, 210, 226), 2991)
    for x in range(-20, W + 20, 36):
        tree_pine(c, x, 230 + (x % 4) * 4, h=60 + (x % 5) * 8, col=(60, 90, 90), snow=(240, 246, 252))
    # frozen lake
    c.rect(0, 230, W, H, (210, 226, 240))
    for k in range(10):
        flat(c, Thick(30 + k * 90, 260 + (k % 4) * 80, 120 + k * 90, 250 + (k % 4) * 80, 1.4), (230, 240, 250))
    # huts
    fishing_hut(c, 160, 330, 100, 70, (200, 70, 60) if "hut" not in d else (240, 200, 60), (90, 80, 80))
    fishing_hut(c, 700, 300, 80, 56, (70, 120, 180), (90, 80, 80))
    # tip-up flags at holes (centre)
    for k, x in enumerate((420, 560)):
        flat(c, Ell(x, 360, 18, 6), (60, 90, 120))
        flat(c, Thick(x, 360, x, 310, 2), (90, 70, 60))
        col = (240, 90, 60) if not (k == 0 and "flag" in d) else (90, 200, 90)
        piece(c, Poly([(x, 310), (x + 24, 318), (x, 326)]), col, border=1, shadow=None)
    # angler on a bucket (left front)
    flat(c, Ell(250, 520, 24, 8), (60, 90, 120))
    buck = (220, 220, 226) if "bucket" not in d else (240, 140, 60)
    piece(c, Poly([(150, 560), (210, 560), (204, 500), (156, 500)]), buck, border=1.5, shadow=PROP)
    hx, hy = modern(c, 180, 500, (60, 110, 160), bottom=(50, 50, 60), hair=(60, 40, 30), h=2.0)
    hat = (220, 60, 70) if "hat" not in d else (90, 170, 120)
    piece(c, [Ell(hx, hy - 8, 15, 9), Circ(hx, hy - 18, 5)], hat, border=1, shadow=None)
    flat(c, [Thick(196, 440, 250, 470, 2), Thick(250, 470, 250, 516, 1)], (60, 60, 70))
    # fish on the ice
    fish(c, 320, 540, 1.6, (150, 170, 190) if "fish" not in d else (240, 160, 60), right=False)
    # sled with gear (right front)
    sled = (150, 100, 70) if "sled" not in d else (60, 120, 200)
    piece(c, [RRect(640, 530, 820, 548, 4), Thick(640, 566, 840, 566, 3), Thick(660, 548, 660, 566, 3), Thick(800, 548, 800, 566, 3), Thick(840, 566, 860, 550, 3)],
          sled, border=1.2, shadow=PROP)
    piece(c, [RRect(660, 494, 740, 530, 4)], (90, 120, 90), border=1.2, shadow=SMALL)
    piece(c, [RRect(750, 504, 800, 530, 4)], (200, 180, 120), border=1.2, shadow=SMALL)
    # dog (centre front)
    if "dog" not in d:
        piece(c, [Ell(470, 560, 30, 14), Circ(500, 540, 13), Ell(510, 544, 8, 6), Thick(442, 556, 430, 540, 4)], (140, 100, 70), border=1.2, shadow=SMALL)
        flat(c, [Circ(502, 536, 1.8), Circ(518, 544, 2.4)], INK)
        flat(c, Ell(494, 532, 4, 9), (110, 80, 56))
    # second angler (right middle)
    modern(c, 560, 420, (240, 180, 60), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.7)


L299_ELEMENTS = [
    E("snow1", lambda c, m: [flat(c, Circ(x, y, 2.4), (250, 252, 255)) for x, y in ((60, 80), (240, 40), (380, 160), (520, 100), (660, 30), (860, 180), (320, 260), (760, 400))],
      daynight="untinted", anim=dict(driftVelocity=(-6, 40), driftLength=120, driftFade=True)),
    E("snow2", lambda c, m: [flat(c, Circ(x, y, 2), (250, 252, 255)) for x, y in ((140, 180), (300, 100), (460, 260), (600, 180), (780, 60), (860, 360), (40, 400))],
      daynight="untinted", anim=dict(driftVelocity=(8, 36), driftLength=120, driftFade=True, phase=0.5)),
    E("smoke", lambda c, m: piece(c, Circ(720, 230, 8), (240, 240, 244), shadow=None), pivot=(720, 230),
      anim=dict(driftVelocity=(6, -22), driftLength=60, driftFade=True, driftGrow=1.6)),
    E("tail", lambda c, m: flat(c, Thick(442, 556, 426, 540, 4), (140, 100, 70)), pivot=(442, 556), anim=dict(swingAngle=24, swingSpeed=2.4)),
]

L299_DIFFS = [
    ("hut", 160, 300, 0),
    ("flag", 432, 318, 0),
    ("hat", 182, 400, 0),
    ("bucket", 180, 530, 0),
    ("fish", 316, 540, 0),
    ("dog", 486, 550, 0),
    ("sled", 750, 550, 0),
]


# =================================================================== Level 300 mushroom village
def mush_house(c, x, base, w, h, cap, stem=(246, 236, 210), door=(150, 100, 60), win=(250, 220, 140)):
    piece(c, RRect(x - w * 0.32, base - h, x + w * 0.32, base, 10), stem, border=1.5, shadow=PROP)
    pts = [(x + w / 2 * math.cos(math.pi * k / 14), base - h + 10 - h * 0.6 * math.sin(math.pi * k / 14)) for k in range(15)]
    piece(c, Poly(pts), cap, border=1.5, shadow=PROP)
    for k in range(4):
        flat(c, Circ(x - w * 0.3 + k * w * 0.2, base - h - h * 0.25 + (k % 2) * 10, w * 0.05), (250, 248, 240))
    flat(c, Poly([(x - w * 0.1, base), (x - w * 0.1, base - h * 0.4), (x, base - h * 0.48), (x + w * 0.1, base - h * 0.4), (x + w * 0.1, base)]), door)
    flat(c, Circ(x + w * 0.2, base - h * 0.6, w * 0.07), win)


def folk(c, x, base, s, cloth, hat):
    piece(c, Poly([(x - 10 * s, base), (x + 10 * s, base), (x + 6 * s, base - 22 * s), (x - 6 * s, base - 22 * s)]), cloth, border=1, shadow=SMALL)
    flat(c, Circ(x, base - 28 * s, 7 * s), SKIN)
    flat(c, Circ(x + 3 * s, base - 28 * s, 1.1 * s), INK)
    flat(c, Ell(x, base - 22 * s, 7 * s, 4 * s), (250, 250, 246))
    piece(c, Poly([(x - 10 * s, base - 32 * s), (x + 10 * s, base - 32 * s), (x + 2 * s, base - 54 * s)]), hat, border=1, shadow=None)


def l300_bg(c, d):
    sky(c, (190, 220, 210), (236, 236, 214), H)
    far_round_trees(c, 160, 40, (130, 170, 130), 3001)
    far_round_trees(c, 200, 34, (110, 156, 110), 3002)
    c.rect(0, 240, W, H, (130, 180, 100))
    layer(c, 240, [(10, 0.01, 0.6), (5, 0.04, 1.0)], (136, 186, 104))
    # winding path
    flat(c, Poly([(380, 600), (520, 600), (500, 470), (560, 380), (520, 290), (470, 290), (500, 380), (430, 470)]), (220, 200, 160))
    # mushroom houses
    mush_house(c, 180, 360, 220, 120, (220, 60, 50) if "cap" not in d else (90, 120, 200))
    mush_house(c, 720, 330, 180, 100, (240, 160, 50))
    mush_house(c, 450, 260, 130, 70, (200, 90, 140), door=(150, 100, 60) if "door" not in d else (60, 130, 90))
    # well (right middle)
    well = (150, 100, 70) if "well" not in d else (90, 110, 160)
    piece(c, [RRect(780, 420, 860, 470, 4)], (160, 156, 150), border=1.5, shadow=PROP)
    piece(c, [Thick(784, 420, 784, 370, 4), Thick(856, 420, 856, 370, 4), Poly([(770, 374), (870, 374), (820, 344)])], well, border=1.2, shadow=PROP)
    # lanterns on posts along the path
    for k, (x, y) in enumerate(((360, 420), (600, 330))):
        flat(c, Thick(x, y + 60, x, y, 3), (90, 70, 60))
        col = (250, 210, 100) if not (k == 0 and "lantern" in d) else (140, 220, 240)
        piece(c, [RRect(x - 10, y - 22, x + 10, y, 3)], col, border=1, shadow=SMALL)
    # flowers
    for k, (x, y) in enumerate(((60, 470), (100, 500), (640, 470), (680, 500), (300, 560), (860, 560))):
        col = (240, 120, 170) if not (k == 3 and "flower" in d) else (250, 250, 246)
        flat(c, Thick(x, y, x, y + 24, 2), (90, 140, 70))
        piece(c, [Circ(x + 6 * math.cos(a), y + 6 * math.sin(a), 5) for a in (0, 1.26, 2.5, 3.8, 5.0)], col, shadow=None)
        flat(c, Circ(x, y, 3), (250, 210, 60))
    # forest folk
    folk(c, 250, 470, 1.8, (90, 140, 200), (220, 60, 60) if "folk" not in d else (250, 200, 60))
    folk(c, 560, 560, 2.0, (200, 120, 60), (90, 160, 90))
    folk(c, 140, 580, 1.6, (150, 100, 180), (90, 130, 200))
    # snails (front)
    shell = (220, 160, 80) if "snail" not in d else (120, 160, 220)
    piece(c, [Ell(760, 580, 40, 10)], (200, 190, 150), border=1, shadow=SMALL)
    piece(c, Circ(752, 556, 22), shell, border=1.2, shadow=SMALL)
    c.ellipse_ring(752, 556, 12, 12, 3, lit(shell, 0.75))
    flat(c, [Thick(794, 574, 800, 556, 2), Thick(788, 574, 790, 556, 2)], (200, 190, 150))
    # small mushrooms
    for x, s in ((40, 1.0), (880, 1.2), (330, 0.8)):
        piece(c, [RRect(x - 4 * s, 600 - 20 * s, x + 4 * s, 600, 2), Ell(x, 600 - 20 * s, 14 * s, 8 * s)], (240, 120, 100), shadow=SMALL)


L300_ELEMENTS = [
    E("smoke", lambda c, m: piece(c, Circ(220, 210, 9), (240, 240, 240), shadow=None), pivot=(220, 210),
      anim=dict(driftVelocity=(6, -22), driftLength=60, driftFade=True, driftGrow=1.6)),
    E("bfly", lambda c, m: piece(c, [Ell(620, 220, 7, 10), Ell(632, 220, 7, 10)], (250, 200, 60), shadow=None), pivot=(626, 220),
      anim=dict(orbitRadius=(40, 20), orbitSpeed=0.15, stretch=(0.6, 0), scaleSpeed=5)),
    E("glow", lambda c, m: soft_union(c, [RRect(590, 308, 610, 330, 3)], (255, 220, 120), 0.4, spread=12), daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=1.0)),
    bird_el("bird", 400, 60, s=9, speed=14),
]

L300_DIFFS = [
    ("cap", 180, 260, 0),
    ("door", 450, 236, 0),
    ("well", 820, 380, 0),
    ("lantern", 360, 410, 0),
    ("flower", 680, 500, 0),
    ("folk", 252, 400, 0),
    ("snail", 752, 556, 0),
]


# =================================================================== Level 301 moon base
MOON = (170, 170, 176)


def l301_bg(c, d):
    c.rect(0, 0, W, H, (10, 12, 24))
    stars_bg(c, 3011, 140, 300)
    # Earth (right top)
    npiece(c, Circ(760, 100, 50), (60, 120, 210), shadow=None)
    land = (90, 170, 100) if "earth" not in d else (230, 200, 120)
    flat(c, [Ell(740, 84, 20, 14), Ell(782, 116, 18, 12), Ell(752, 128, 10, 6)], land)
    flat(c, [Ell(770, 70, 24, 5), Ell(744, 112, 20, 4)], (250, 250, 250))
    # far ridge
    npiece(c, hill_strip(260, [(24, 0.008, 0.4), (10, 0.03, 1.0)]), (120, 120, 128), shadow=LAYER)
    npiece(c, hill_strip(320, [(10, 0.01, 1.2), (6, 0.04, 0.4)]), MOON, shadow=LAYER)
    # craters
    for x, y, r in ((100, 400, 40), (620, 360, 28), (380, 560, 46), (820, 540, 34)):
        flat(c, Ell(x, y, r, r * 0.3), lit(MOON, 0.8))
        flat(c, Ell(x, y - 2, r * 0.8, r * 0.22), lit(MOON, 0.9))
    # domes (centre)
    dome = (230, 236, 240) if "dome" not in d else (240, 190, 120)
    for x, r, col in ((350, 80, dome), (500, 56, (230, 236, 240))):
        npiece(c, Poly([(x + r * math.cos(math.pi * k / 16), 330 - r * math.sin(math.pi * k / 16)) for k in range(17)]), col)
        for k in (5, 8, 11):
            a = math.pi * k / 16
            flat(c, Thick(x + r * math.cos(a), 330 - r * math.sin(a), x + r * math.cos(a) * 0.4, 330, 1.4), lit(col, 0.85))
    flat(c, RRect(330, 300, 370, 330, 4), (250, 220, 120))
    npiece(c, RRect(400, 310, 460, 330, 6), (200, 206, 210))
    # dish antenna (left)
    dish = (220, 224, 230) if "dish" not in d else (220, 120, 90)
    npiece(c, [Thick(140, 330, 150, 250, 5)], (150, 150, 160))
    npiece(c, [Poly([(100, 200), (200, 260), (170, 280), (110, 250)])], dish)
    flat(c, Thick(150, 240, 176, 220, 2), (150, 150, 160))
    # lander (right middle)
    lander = (240, 200, 90) if "lander" not in d else (200, 200, 210)
    npiece(c, [Thick(640, 340, 610, 390, 3), Thick(720, 340, 750, 390, 3)], (150, 150, 160))
    npiece(c, [RRect(630, 290, 730, 344, 4)], lander)
    npiece(c, [Poly([(650, 290), (710, 290), (696, 250), (664, 250)])], (220, 224, 230))
    flat(c, Circ(680, 270, 8), (60, 70, 100))
    # flag (generic stripes, no nation)
    flat(c, Thick(560, 420, 560, 340, 2), (200, 200, 210))
    flag = (240, 90, 80) if "flag" not in d else (90, 170, 230)
    npiece(c, RRect(560, 340, 610, 370, 1), flag, shadow=None)
    flat(c, Thick(560, 355, 610, 355, 6), (250, 250, 246))
    # rover (left front)
    rov = (240, 240, 236) if "rover" not in d else (240, 150, 60)
    npiece(c, [RRect(120, 470, 300, 510, 6), RRect(150, 440, 250, 472, 4)], rov)
    flat(c, RRect(160, 446, 240, 464, 2), (60, 70, 100))
    for x in (140, 210, 280):
        wheel(c, x, 520, 18, tyre=(60, 60, 66), hub=(170, 170, 176))
    # astronaut (centre front)
    hx, hy = modern(c, 520, 590, (240, 240, 236), bottom=(220, 220, 226), hair=(240, 240, 236), h=2.6)
    npiece(c, Circ(hx, hy, 20), (240, 240, 236), shadow=SMALL)
    visor = (240, 190, 70) if "visor" not in d else (90, 170, 230)
    flat(c, Ell(hx + 4, hy, 13, 10), visor)
    npiece(c, RRect(490, 500, 506, 540, 3), (200, 200, 206), shadow=None)
    # rock samples box (right front)
    npiece(c, RRect(700, 540, 820, 590, 4), (200, 200, 206))
    if "crater" not in d:
        for k in range(4):
            npiece(c, Circ(720 + k * 26, 534, 12), (120, 110, 100), shadow=None)


L301_ELEMENTS = [
    E("blink", lambda c, m: soft_union(c, [Circ(176, 220, 4)], (255, 90, 80), 0.8, spread=8), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.0)),
    E("float", lambda c, m: [npiece(c, Circ(820, 300, 12), (240, 240, 236), shadow=None), flat(c, Ell(824, 300, 7, 6), (240, 190, 70))], pivot=(820, 300),
      anim=dict(bobAmplitude=(10, 14), bobSpeed=0.2)),
    E("dust", lambda c, m: piece(c, Circ(300, 520, 8), (200, 200, 206), shadow=None), pivot=(300, 520),
      anim=dict(driftVelocity=(30, -10), driftLength=60, driftFade=True, driftGrow=1.6)),
    E("sat", lambda c, m: flat(c, [RRect(300, 60, 320, 70, 1), RRect(286, 62, 298, 68, 1), RRect(322, 62, 334, 68, 1)], (200, 210, 230)), daynight="untinted",
      anim=drift_across(286, 334, 14)),
]

L301_DIFFS = [
    ("earth", 760, 100, 0),
    ("dish", 150, 240, 0),
    ("dome", 350, 290, 0),
    ("lander", 680, 316, 0),
    ("flag", 585, 355, 0),
    ("rover", 210, 480, 0),
    ("visor", 525, 470, 0),
    ("crater", 760, 534, 0),
]


# =================================================================== Level 302 robot factory
def robot(c, x, base, s, body, head=True, eye=(90, 220, 240)):
    piece(c, [RRect(x - 18 * s, base - 30 * s, x - 6 * s, base, 3), RRect(x + 6 * s, base - 30 * s, x + 18 * s, base, 3)], (140, 150, 160), border=1, shadow=SMALL)
    piece(c, RRect(x - 26 * s, base - 76 * s, x + 26 * s, base - 28 * s, 6), body, border=1.5, shadow=PROP)
    flat(c, Circ(x, base - 52 * s, 8 * s), lit(body, 0.8))
    if head:
        piece(c, RRect(x - 18 * s, base - 108 * s, x + 18 * s, base - 78 * s, 6), lit(body, 1.1), border=1.2, shadow=SMALL)
        flat(c, RRect(x - 12 * s, base - 98 * s, x + 12 * s, base - 88 * s, 3), eye)
        flat(c, Thick(x, base - 108 * s, x, base - 118 * s, 2), (90, 90, 100))
        flat(c, Circ(x, base - 120 * s, 4 * s), (240, 90, 80))


def l302_bg(c, d):
    c.rect(0, 0, W, H, (180, 186, 196))
    for x in range(0, W, 100):
        flat(c, Thick(x, 0, x, 380, 4), (166, 172, 182))
    # roof beams + lamps
    flat(c, Thick(0, 40, W, 40, 12), (110, 116, 126))
    for k, x in enumerate((150, 450, 750)):
        flat(c, Thick(x, 40, x, 70, 2), (60, 60, 70))
        piece(c, Poly([(x - 34, 96), (x + 34, 96), (x + 18, 70), (x - 18, 70)]), (60, 70, 80), border=1.2, shadow=SMALL)
    # warning light (left top)
    light = (250, 160, 40) if "light" not in d else (90, 200, 240)
    piece(c, [RRect(40, 140, 80, 156, 2), Ell(60, 136, 18, 20)], light, border=1.2, shadow=SMALL)
    # control booth (right top)
    piece(c, RRect(640, 120, 880, 280, 4), (90, 100, 110), border=1.5, shadow=PROP)
    flat(c, RRect(656, 136, 864, 220, 3), (170, 210, 230))
    modern(c, 760, 222, (240, 200, 60), bottom=(60, 60, 70), hair=(40, 30, 30), h=1.6)
    scr = (60, 200, 140) if "screen" not in d else (220, 90, 140)
    piece(c, RRect(770, 230, 860, 270, 3), (40, 44, 50), shadow=None)
    flat(c, RRect(776, 236, 854, 264, 2), scr)
    flat(c, [Circ(690, 250, 7), Circ(716, 250, 7), Circ(742, 250, 7)], (220, 60, 60))
    # hazard stripes
    for x in range(0, W, 40):
        flat(c, Poly([(x, 380), (x + 20, 380), (x + 40, 400), (x + 20, 400)]), (250, 200, 40))
        flat(c, Poly([(x + 20, 380), (x + 40, 380), (x + 60, 400), (x + 40, 400)]), (40, 40, 46))
    # sign (centre top)
    sign = (240, 240, 236) if "sign" not in d else (250, 200, 60)
    piece(c, RRect(330, 120, 570, 170, 4), sign, border=1.5, shadow=PROP)
    sign_box(c, 346, 130, 554, 160, sign, 3021, glyph=(60, 60, 70), vertical=False)
    # conveyor belt
    piece(c, RRect(0, 330, W, 372, 4), (60, 64, 70), border=1.5, shadow=PROP)
    flat(c, RRect(0, 330, W, 340, 2), (90, 94, 100))
    # robots on the belt
    robot(c, 140, 330, 1.2, (90, 150, 220))
    robot(c, 330, 330, 1.2, (240, 120, 60) if "robot" not in d else (120, 200, 120))
    robot(c, 520, 330, 1.2, (200, 200, 210), head="head" not in d)
    # robot arm bases (arms are elements)
    for x in (225, 620):
        arm = (250, 180, 40) if not (x == 620 and "arm" in d) else (90, 120, 200)
        piece(c, [RRect(x - 30, 120, x + 30, 150, 4), Circ(x, 160, 18)], arm, border=1.5, shadow=PROP)
    # floor
    c.rect(0, 400, W, H, (120, 124, 130))
    for x in range(0, W, 60):
        for y in range(400, H, 60):
            flat(c, RRect(x + 2, y + 2, x + 58, y + 58, 2), (128, 132, 138))
    # crates + barrel (front)
    crate = (190, 150, 100) if "crate" not in d else (90, 160, 200)
    for x0, y0, col in ((40, 500, crate), (120, 520, (190, 150, 100)), (60, 440, (180, 140, 90))):
        piece(c, RRect(x0, y0, x0 + 80, y0 + 70, 2), col, border=1.5, shadow=PROP)
        flat(c, [Thick(x0, y0, x0 + 80, y0 + 70, 3), Thick(x0 + 80, y0, x0, y0 + 70, 3)], lit(col, 0.8))
    barrel = (60, 110, 160) if "barrel" not in d else (220, 70, 70)
    piece(c, [RRect(760, 470, 840, 590, 8)], barrel, border=1.5, shadow=PROP)
    flat(c, [Thick(760, 500, 840, 500, 4), Thick(760, 560, 840, 560, 4)], lit(barrel, 0.7))
    # engineer with a tablet (centre front)
    hx, hy = modern(c, 450, 600, (60, 110, 160), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.6)
    piece(c, [Ell(hx, hy - 10, 22, 12), RRect(hx - 22, hy - 10, hx + 22, hy - 4, 2)], (250, 200, 40), shadow=SMALL)
    piece(c, RRect(476, 500, 520, 530, 3), (40, 44, 50), shadow=SMALL)
    # finished robot waving (right front)
    robot(c, 640, 590, 1.4, (200, 90, 160))


def arm_el(eid, x, phase):
    def d(c, m):
        piece(c, [Thick(x, 160, x + 40, 230, 12), Thick(x + 40, 230, x + 10, 290, 10)], (250, 180, 40), border=1.2, shadow=SMALL)
        flat(c, [Circ(x + 40, 230, 8), Thick(x + 10, 290, x - 4, 306, 4), Thick(x + 10, 290, x + 24, 306, 4)], (90, 90, 100))
    return E(eid, d, pivot=(x, 160), anim=dict(swingAngle=16, swingSpeed=0.6, phase=phase))


L302_ELEMENTS = [
    arm_el("arm1", 225, 0.0), arm_el("arm2", 620, 0.5),
    E("belt", lambda c, m: [flat(c, Thick(x, 352, x + 14, 352, 3), (110, 114, 120)) for x in range(0, W, 40)], anim=dict(driftVelocity=(40, 0), driftLength=40)),
    E("beacon", lambda c, m: soft_union(c, [Circ(60, 136, 22)], (255, 180, 60), 0.5, spread=24), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.4)),
    E("spark", lambda c, m: [flat(c, Circ(x, y, 2.4), (255, 230, 120)) for x, y in ((235, 310), (247, 300), (225, 302))], pivot=(235, 306), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=3.0)),
    E("wave", lambda c, m: piece(c, Thick(676, 520, 700, 480, 8), (200, 90, 160), shadow=SMALL), pivot=(676, 520), anim=dict(swingAngle=20, swingSpeed=1.2)),
]

L302_DIFFS = [
    ("light", 60, 140, 0),
    ("sign", 450, 145, 0),
    ("screen", 815, 250, 0),
    ("robot", 330, 280, 0),
    ("head", 520, 210, 0),
    ("arm", 620, 140, 0),
    ("crate", 80, 535, 0),
    ("barrel", 800, 530, 0),
]


# =================================================================== Level 303 sandcastle beach
SAND = (236, 210, 150)


def l303_bg(c, d):
    sky(c, (100, 180, 240), (220, 238, 250), H)
    sun_bg(c, 120, 60, 28)
    cloud_bg(c, 640, 50, 0.6)
    # sea + far sailboat
    c.rect(0, 180, W, 300, (60, 150, 200))
    for k in range(10):
        flat(c, Thick(30 + k * 90, 210 + (k % 3) * 30, 80 + k * 90, 210 + (k % 3) * 30, 1.6), (130, 200, 230))
    sail = (250, 246, 236) if "sail" not in d else (240, 120, 120)
    piece(c, Poly([(700, 200), (760, 200), (750, 214), (710, 214)]), (200, 90, 60), border=1, shadow=None)
    piece(c, Poly([(728, 196), (728, 130), (768, 196)]), sail, border=1, shadow=None)
    # shore
    piece(c, hill_strip(290, [(6, 0.02, 0.6), (3, 0.06, 1.0)]), (150, 210, 220), shadow=None)
    piece(c, hill_strip(300, [(6, 0.02, 0.6), (3, 0.06, 1.0)]), SAND, shadow=LAYER)
    # sandcastle (centre)
    base_col = (220, 190, 130)
    piece(c, RRect(300, 380, 600, 460, 4), base_col, border=1.5, shadow=PROP)
    for x in range(300, 600, 30):
        piece(c, RRect(x + 4, 366, x + 22, 382, 1), base_col, shadow=None)
    towers = [(330, 300), (450, 260), (570, 300)]
    for k, (x, top) in enumerate(towers):
        if k == 2 and "tower" in d:
            continue
        piece(c, [RRect(x - 30, top, x + 30, 380, 3), Poly([(x - 36, top + 2), (x + 36, top + 2), (x, top - 40)])], base_col, border=1.5, shadow=PROP)
        flat(c, RRect(x - 8, top + 30, x + 8, top + 50, 6), (160, 130, 80))
    flat(c, Poly([(430, 460), (430, 420), (450, 404), (470, 420), (470, 460)]), (160, 130, 80))
    flag = (240, 80, 80) if "flag" not in d else (80, 160, 240)
    flat(c, Thick(450, 220, 450, 180, 2), (120, 90, 60))
    piece(c, Poly([(450, 180), (484, 190), (450, 200)]), flag, border=1, shadow=None)
    # moat
    flat(c, Ell(450, 480, 190, 20), (120, 190, 220))
    # bucket + spade (left)
    buck = (240, 200, 40) if "bucket" not in d else (240, 120, 160)
    piece(c, [Poly([(150, 470), (210, 470), (200, 400), (160, 400)])], buck, border=1.5, shadow=PROP)
    flat(c, Thick(160, 404, 200, 404, 4), lit(buck, 0.8))
    spade = (60, 140, 220) if "spade" not in d else (90, 200, 120)
    piece(c, [Thick(250, 470, 290, 400, 4), Poly([(240, 470), (264, 470), (258, 500), (234, 500)])], spade, border=1.2, shadow=SMALL)
    # kids
    modern(c, 110, 600, (240, 120, 60), bottom=(60, 120, 200), hair=(200, 160, 90), h=2.2, style="twin")
    modern(c, 680, 590, (90, 180, 140), bottom=(240, 200, 60), hair=(40, 30, 30), h=2.0)
    # umbrella (right)
    umb = (240, 90, 90) if "umbrella" not in d else (250, 200, 60)
    flat(c, Thick(810, 600, 820, 360, 3), (200, 200, 210))
    piece(c, Poly([(720, 380), (900, 370), (816, 316)]), umb, border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, Poly([(750 + k * 50, 378), (776 + k * 50, 376), (816, 318)]), (250, 250, 246))
    # shells
    shell = (250, 180, 170) if "shell" not in d else (150, 200, 240)
    piece(c, Poly([(560 + 22 * math.cos(math.pi * k / 8), 560 - 20 * math.sin(math.pi * k / 8)) for k in range(9)]), shell, border=1.2, shadow=SMALL)
    for k in range(1, 8):
        flat(c, Thick(560, 560, 560 + 20 * math.cos(math.pi * k / 8), 560 - 18 * math.sin(math.pi * k / 8), 1.4), lit(shell, 0.8))
    piece(c, Ell(300, 570, 14, 9), (250, 240, 220), border=1, shadow=SMALL)
    # crab
    if "crab" not in d:
        piece(c, [Ell(840, 566, 22, 12), Circ(820, 552, 7), Circ(860, 552, 7)], (230, 80, 50), border=1, shadow=SMALL)
        flat(c, [Thick(826, 574, 812, 584, 2), Thick(854, 574, 868, 584, 2), Circ(834, 556, 2), Circ(846, 556, 2)], (60, 30, 30))


L303_ELEMENTS = [
    bird_el("gull", 300, 90, s=10, speed=16),
    E("wave", lambda c, m: flat(c, hill_strip(296, [(6, 0.02, 0.6), (3, 0.06, 1.0)], bottom=306), (250, 252, 255)), anim=dict(bobAmplitude=(0, 4), bobSpeed=0.3)),
    E("bob", lambda c, m: piece(c, [Ell(250, 250, 26, 8), Circ(250, 236, 8)], (250, 200, 60), shadow=None), pivot=(250, 250),
      anim=dict(bobAmplitude=(6, 4), bobSpeed=0.4)),
    cloud_el("cloud", 380, 70, 0.4, 8),
]

L303_DIFFS = [
    ("sail", 740, 170, 0),
    ("flag", 466, 190, 0),
    ("tower", 570, 300, 0),
    ("bucket", 180, 436, 0),
    ("spade", 262, 460, 0),
    ("umbrella", 810, 350, 0),
    ("shell", 560, 548, 0),
    ("crab", 840, 562, 0),
]


# =================================================================== Level 304 island resort
def bungalow(c, x, base, w, wall, roof):
    for px in (x - w / 2 + 8, x, x + w / 2 - 8):
        flat(c, Thick(px, base, px, base + 50, 4), (110, 80, 60))
    piece(c, RRect(x - w / 2 - 10, base - 6, x + w / 2 + 10, base + 4, 2), (170, 120, 80), border=1.2, shadow=SMALL)
    piece(c, RRect(x - w / 2, base - w * 0.5, x + w / 2, base - 4, 2), wall, border=1.5, shadow=PROP)
    piece(c, Poly([(x - w / 2 - 14, base - w * 0.5 + 4), (x + w / 2 + 14, base - w * 0.5 + 4), (x, base - w * 1.0)]), roof, border=1.5, shadow=PROP)
    for k in range(4):
        flat(c, Thick(x - w / 2 + k * w / 3, base - w * 0.5 + 4, x, base - w * 1.0, 1.4), lit(roof, 0.85))
    flat(c, RRect(x - 10, base - w * 0.36, x + 10, base - 4, 2), (90, 70, 60))


def l304_bg(c, d):
    sky(c, (250, 150, 110), (250, 220, 170), 330)
    sun = (250, 200, 90) if "sun" not in d else (240, 110, 110)
    sun_bg(c, 450, 230, 50, col=sun, glow=(255, 220, 160))
    cloud_bg(c, 160, 80, 0.7, col=(250, 200, 190))
    cloud_bg(c, 760, 60, 0.6, col=(250, 200, 190))
    # lagoon
    c.rect(0, 270, W, H, (70, 170, 190))
    for k in range(10):
        flat(c, Thick(20 + k * 90, 300 + (k % 4) * 50, 70 + k * 90, 300 + (k % 4) * 50, 1.6), (250, 200, 160))
    flat(c, Poly([(400, 270), (500, 270), (520, 400), (380, 400)]), (250, 200, 140))
    # overwater bungalows + walkway
    flat(c, Thick(0, 330, 640, 330, 8), (170, 120, 80))
    bungalow(c, 90, 320, 90, (240, 226, 196), (180, 140, 80))
    bungalow(c, 250, 320, 90, (240, 226, 196), (180, 140, 80) if "roof" not in d else (90, 130, 170))
    bungalow(c, 600, 320, 80, (240, 226, 196), (180, 140, 80))
    # sailboat far (right)
    sail = (250, 246, 236) if "boat" not in d else (90, 170, 220)
    piece(c, Poly([(760, 290), (840, 290), (826, 304), (774, 304)]), (90, 70, 60), border=1, shadow=None)
    piece(c, Poly([(800, 286), (800, 200), (850, 286)]), sail, border=1, shadow=None)
    # beach (front)
    piece(c, hill_strip(440, [(10, 0.01, 0.6), (5, 0.04, 1.0)]), (240, 220, 170), shadow=LAYER)
    # palms + hammock (right front)
    palm(c, 700, 560, h=200, lean=-30)
    palm(c, 880, 560, h=220, lean=24)
    ham = (240, 120, 80) if "hammock" not in d else (90, 170, 160)
    piece(c, Poly([(690, 470)] + [(780 + 90 * math.cos(math.pi * k / 10), 470 + 40 * math.sin(math.pi * k / 10)) for k in range(10, -1, -1)] + [(870, 470),
                                                                                                                                          (780, 480)]), ham, border=1.2,
          shadow=SMALL)
    # kayak on the beach (left)
    kay = (250, 200, 40) if "kayak" not in d else (220, 70, 90)
    piece(c, Poly([(40, 520), (220, 510), (200, 534), (60, 540)]), kay, border=1.2, shadow=SMALL)
    # lounger + drink table (centre front)
    lounger = (250, 250, 246) if "lounger" not in d else (90, 170, 230)
    piece(c, Poly([(300, 560), (480, 556), (500, 520), (474, 520), (464, 540), (300, 544)]), lounger, border=1.5, shadow=PROP)
    flat(c, [Thick(310, 560, 306, 590, 3), Thick(470, 558, 474, 590, 3)], (150, 120, 90))
    modern(c, 380, 546, (90, 160, 210), bottom=(90, 160, 210), hair=(40, 30, 30), h=1.6)
    piece(c, [Ell(560, 530, 30, 8), RRect(556, 530, 564, 590, 2)], (190, 150, 100), border=1.2, shadow=SMALL)
    drink = (240, 120, 60) if "drink" not in d else (90, 200, 120)
    piece(c, Poly([(546, 522), (574, 522), (568, 494), (552, 494)]), drink, border=1, shadow=None)
    flat(c, [Thick(566, 494, 578, 476, 2), Circ(546, 496, 6)], (250, 220, 60))
    # starfish (left front)
    if "starfish" not in d:
        piece(c, Poly(star_pts(120, 580, 22, 9)), (240, 130, 80), border=1.2, shadow=SMALL)


L304_ELEMENTS = [
    bird_el("gull", 300, 120, s=10, speed=14),
    bird_el("gull2", 620, 90, s=9, speed=-16),
    E("glint", lambda c, m: [flat(c, Thick(x, 360, x + 30, 360, 2), (255, 230, 180)) for x in (420, 470, 440)], daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.0)),
    E("swing", lambda c, m: flat(c, Thick(690, 470, 870, 470, 2), (120, 90, 60)), pivot=(780, 470), anim=dict(swingAngle=2, swingSpeed=0.5)),
]

L304_DIFFS = [
    ("sun", 450, 230, 0),
    ("roof", 250, 250, 0),
    ("boat", 815, 250, 0),
    ("hammock", 780, 490, 0),
    ("kayak", 130, 525, 0),
    ("lounger", 400, 545, 0),
    ("drink", 560, 506, 0),
    ("starfish", 120, 580, 0),
]


LEVELS = [
    ("Level295", "养蜂场", l295_bg, L295_ELEMENTS, L295_DIFFS, 60, OPTS),
    ("Level296", "茶园", l296_bg, L296_ELEMENTS, L296_DIFFS, 60, OPTS),
    ("Level297", "城堡厨房", l297_bg, L297_ELEMENTS, L297_DIFFS, 60, OPTS),
    ("Level298", "潜水艇", l298_bg, L298_ELEMENTS, L298_DIFFS, 60, OPTS),
    ("Level299", "冰上钓鱼", l299_bg, L299_ELEMENTS, L299_DIFFS, 60, OPTS),
    ("Level300", "蘑菇村", l300_bg, L300_ELEMENTS, L300_DIFFS, 60, OPTS),
    ("Level301", "月球基地", l301_bg, L301_ELEMENTS, L301_DIFFS, 60, OPTS),
    ("Level302", "机器人工厂", l302_bg, L302_ELEMENTS, L302_DIFFS, 60, OPTS),
    ("Level303", "沙滩城堡", l303_bg, L303_ELEMENTS, L303_DIFFS, 60, OPTS),
    ("Level304", "海岛度假村", l304_bg, L304_ELEMENTS, L304_DIFFS, 60, OPTS),
]
