# -*- coding: utf-8 -*-
"""Mixed themes part 10 (paper-craft fantasy / adventure / misc, full-bleed, original designs, no brands):
  Level325 海底宫殿   - an undersea palace: shell domes, coral towers, sea-folk, seahorses, a pearl throne
  Level326 彩虹山谷   - a rainbow valley: rainbow over a waterfall, pastel hills, winged ponies, flowers
  Level327 雪人村     - a snowman village: snow-block huts, snowmen families, a sled hill, ice slide
  Level328 企鹅聚居地 - a penguin colony on the ice: penguins, chicks, an iceberg, a research boat, seals
  Level329 海盗港湾   - a pirate cove town: wooden docks, a moored ship, tavern, treasure crates, parrot
  Level330 外星花园   - an alien garden planet: two moons, strange glowing plants, round creatures, a saucer
  Level331 巧克力工厂 - a chocolate factory: melting vats, chocolate river, pipes, conveyor of bars, workers
  Level332 气象站     - a mountain weather station: anemometer, radar dome, balloon launch, instruments
  Level333 赛艇湖     - a rowing regatta on a lake: rowing boats, boathouse, spectators, finish buoys
  Level334 古罗马广场 - a Roman forum market: columns, arches, fountain, stalls, citizens in togas, a chariot
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bubbles_el, bush, cloud_bg, cloud_el, drift_across, fish, layer, palm, rock, sky, smoke_el, stars_bg,
                 sun_bg, tree_pine, tree_round)
from fills import far_forest, far_ridge, far_round_trees
from levels_akiba import modern, sign_box
from levels_festival import npiece, bunting
from levels_mix1 import lantern
from levels_mix2 import wheel
from levels_mix3 import column, toga, amphora

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


# =================================================================== Level 325 undersea palace
def l325_bg(c, d):
    c.gradient(0, H, (50, 140, 190), (20, 60, 110))
    for x in (60, 300, 620, 820):
        soft_union(c, [Poly([(x, 0), (x + 50, 0), (x + 130, 600), (x + 40, 600)])], (170, 230, 250), 0.1, spread=20)
    # palace
    pal = (240, 220, 210)
    piece(c, RRect(260, 200, 640, 420, 4), pal, border=1.5, shadow=PROP)
    dome = (240, 170, 190) if "dome" not in d else (150, 210, 200)
    piece(c, Poly([(450 + 110 * math.cos(math.pi * k / 16), 200 - 110 * math.sin(math.pi * k / 16)) for k in range(17)]), dome, border=1.5, shadow=PROP)
    for k in (4, 8, 12):
        a = math.pi * k / 16
        flat(c, Thick(450 + 110 * math.cos(a), 200 - 110 * math.sin(a), 450, 200, 2), lit(dome, 0.85))
    for x in (230, 670):
        piece(c, [RRect(x - 30, 160, x + 30, 420, 4), Poly([(x - 36, 162), (x + 36, 162), (x, 90)])], pal, border=1.5, shadow=PROP)
        flat(c, RRect(x - 10, 200, x + 10, 240, 8), (60, 110, 150))
    flat(c, Poly([(410, 420), (410, 330), (450, 300), (490, 330), (490, 420)]), (60, 100, 140))
    for x in (320, 580):
        flat(c, RRect(x - 18, 260, x + 18, 320, 10), (60, 110, 150))
    # pearl on the dome top
    pearl = (250, 250, 246) if "pearl" not in d else (240, 200, 90)
    piece(c, Circ(450, 80, 16), pearl, border=1.2, shadow=SMALL)
    # sea floor
    piece(c, hill_strip(420, [(10, 0.02, 0.6), (6, 0.05, 1.0)]), (220, 200, 150), shadow=LAYER)
    # coral towers
    for x, col, key in ((80, (240, 110, 120), "coral"), (820, (250, 170, 80), None)):
        cc = col if not (key and key in d) else (150, 120, 220)
        piece(c, [Thick(x, 480, x, 330, 10), Thick(x, 400, x - 40, 340, 7), Thick(x, 380, x + 40, 320, 7), Thick(x - 40, 340, x - 46, 300, 6), Thick(x + 40, 320, x + 46, 280, 6)],
              cc, border=1, shadow=SMALL)
    # seahorse (left middle)
    sh = (250, 200, 70) if "seahorse" not in d else (240, 120, 160)
    piece(c, [Ell(170, 300, 14, 26), Circ(176, 266, 11), Poly([(184, 264), (204, 260), (186, 272)]), Thick(166, 324, 176, 350, 6), Thick(176, 350, 164, 356, 5)], sh,
          border=1, shadow=SMALL)
    flat(c, Circ(178, 264, 2), INK)
    # sea-folk king on throne (front centre)
    piece(c, [RRect(390, 470, 510, 560, 10), Poly([(380, 470)] + [(450 + 70 * math.cos(math.pi * k / 10), 470 - 60 * math.sin(math.pi * k / 10)) for k in range(11)] + [(520, 470)])],
          (240, 180, 200), border=1.5, shadow=PROP)
    hx, hy = modern(c, 450, 540, (60, 140, 160), bottom=(60, 140, 160), hair=(250, 250, 246), h=2.0)
    crown = (250, 200, 60) if "crown" not in d else (200, 200, 220)
    piece(c, Poly([(hx - 14, hy - 8), (hx + 14, hy - 8), (hx + 14, hy - 24), (hx + 6, hy - 14), (hx, hy - 26), (hx - 6, hy - 14), (hx - 14, hy - 24)]), crown, border=1,
          shadow=None)
    flat(c, Thick(480, 540, 492, 440, 3), (250, 200, 60))
    # treasure chest + clam (left front)
    chest = (170, 110, 60) if "chest" not in d else (90, 140, 160)
    piece(c, [RRect(100, 530, 200, 580, 3), Poly([(96, 532), (204, 532), (196, 506), (104, 506)])], chest, border=1.5, shadow=PROP)
    flat(c, RRect(144, 528, 156, 546, 2), (250, 200, 60))
    piece(c, [Ell(760, 570, 50, 16), Poly([(710, 566)] + [(760 + 50 * math.cos(math.pi * k / 10), 560 - 40 * math.sin(math.pi * k / 10)) for k in range(11)])],
          (230, 210, 230), border=1.2, shadow=SMALL)
    fish(c, 300, 140, 1.5, (250, 200, 60), fin=(250, 250, 246))


L325_ELEMENTS = bubbles_el("bub", 600, 440, n=4, r=5, rise=(2, -40), length=200) + [
    E("swim1", lambda c, m: fish(c, 700, 120, 1.3, (120, 200, 240), right=False), anim=drift_across(680, 720, -26)),
    E("jelly", lambda c, m: [piece(c, Ell(820, 160, 20, 14), (250, 200, 240), shadow=None)] + [flat(c, Thick(810 + k * 6, 170, 808 + k * 6, 200, 1.6), (250, 200, 240))
                                                                                                for k in range(4)], pivot=(820, 160), anim=dict(bobAmplitude=(0, 20), bobSpeed=0.3)),
    E("kelp", lambda c, m: flat(c, Thick(880, 600, 870, 440, 5), (60, 140, 90)), pivot=(880, 600), anim=dict(swingAngle=6, swingSpeed=0.5)),
]

L325_DIFFS = [
    ("pearl", 450, 80, 0),
    ("dome", 450, 150, 0),
    ("seahorse", 180, 300, 0),
    ("coral", 80, 380, 0),
    ("crown", 452, 430, 0),
    ("chest", 150, 545, 0),
]


# =================================================================== Level 326 rainbow valley
def pony(c, x, base, s, body, mane, face=1, wings=True):
    for lx in (-14, -6, 8, 14):
        flat(c, RRect(x + lx * s * face - 2.5 * s, base - 22 * s, x + lx * s * face + 2.5 * s, base, 1), lit(body, 0.9))
    if wings:
        piece(c, Poly([(x - 4 * s, base - 34 * s), (x - 20 * s * face, base - 64 * s), (x + 8 * s * face, base - 40 * s)]), (250, 250, 246), border=1, shadow=None)
    piece(c, [Ell(x, base - 28 * s, 22 * s, 11 * s), Thick(x + 16 * s * face, base - 32 * s, x + 24 * s * face, base - 48 * s, 7 * s), Ell(x + 30 * s * face, base - 50 * s, 10 * s, 7 * s)],
          body, border=1.2, shadow=SMALL)
    flat(c, [Thick(x + 14 * s * face, base - 36 * s, x + 22 * s * face, base - 56 * s, 4 * s), Thick(x - 20 * s * face, base - 30 * s, x - 30 * s * face, base - 14 * s, 4 * s)], mane)
    flat(c, Circ(x + 32 * s * face, base - 52 * s, 1.6 * s), INK)


RAINBOW = [(240, 90, 90), (250, 160, 70), (250, 220, 90), (120, 200, 110), (90, 160, 230), (160, 120, 220)]


def l326_bg(c, d):
    sky(c, (160, 210, 246), (250, 236, 240), H)
    # rainbow
    for k, col in enumerate(RAINBOW):
        c.ellipse_ring(450, 330, 330 - k * 16, 260 - k * 16, 16, col, ymax=330)
    if "rainbow" in d:
        cloud_bg(c, 560, 86, 0.6)
    cloud_bg(c, 130, 310, 0.8)
    cloud_bg(c, 770, 300, 0.8)
    # pastel hills
    layer(c, 300, [(30, 0.006, 0.2), (12, 0.02, 1.0)], (180, 220, 200))
    layer(c, 360, [(16, 0.01, 1.2), (6, 0.04, 0.4)], (160, 210, 170))
    # waterfall + pond (centre)
    flat(c, Poly([(420, 300), (480, 300), (490, 420), (410, 420)]), (220, 240, 250))
    flat(c, Ell(450, 440, 120, 26), (150, 200, 240))
    # mushroom cottage (left)
    piece(c, RRect(80, 330, 160, 400, 10), (250, 246, 230), border=1.5, shadow=PROP)
    cap = (240, 140, 180) if "cottage" not in d else (120, 200, 200)
    piece(c, Poly([(120 + 70 * math.cos(math.pi * k / 12), 340 - 50 * math.sin(math.pi * k / 12)) for k in range(13)]), cap, border=1.5, shadow=PROP)
    flat(c, RRect(110, 366, 130, 400, 6), (180, 120, 90))
    # ponies
    pony(c, 300, 500, 1.8, (250, 250, 246), (240, 120, 180) if "mane" not in d else (90, 160, 230))
    pony(c, 640, 490, 1.6, (250, 210, 230), (160, 120, 220), face=-1)
    pony(c, 700, 200, 1.0, (200, 220, 250), (250, 200, 90), wings=True)
    # flowers
    rnd = random.Random(3261)
    for _ in range(30):
        x, y = rnd.uniform(0, W), rnd.uniform(500, 600)
        piece(c, Circ(x, y, 6), rnd.choice(RAINBOW), shadow=None)
    # giant lollipop flower (right front)
    flat(c, Thick(820, 600, 820, 470, 4), (90, 160, 90))
    fl = (250, 200, 90) if "flower" not in d else (240, 90, 120)
    piece(c, [Circ(820 + 22 * math.cos(a), 450 + 22 * math.sin(a), 14) for a in [k * 1.047 for k in range(6)]], fl, border=1, shadow=SMALL)
    flat(c, Circ(820, 450, 12), (250, 250, 246))
    # crystal (left front)
    cr = (190, 160, 250) if "crystal" not in d else (120, 220, 200)
    piece(c, [Poly([(70, 590), (90, 520), (110, 590)]), Poly([(100, 590), (124, 500), (148, 590)]), Poly([(140, 590), (156, 540), (172, 590)])], cr, border=1.2, shadow=PROP)


L326_ELEMENTS = [
    E("sparkle1", lambda c, m: flat(c, Poly(star_pts(260, 160, 9, 3)), (255, 255, 230)), pivot=(260, 160), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.0)),
    E("sparkle2", lambda c, m: flat(c, Poly(star_pts(330, 60, 9, 3)), (255, 255, 230)), pivot=(330, 60), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=1.3, phase=0.5)),
    E("fall", lambda c, m: [flat(c, Thick(x, 300, x, 420, 2), (250, 252, 255)) for x in (430, 450, 470)], daynight="untinted", anim=dict(driftVelocity=(0, 40), driftLength=20)),
    E("bfly", lambda c, m: piece(c, [Ell(500, 520, 7, 10), Ell(512, 520, 7, 10)], (240, 120, 180), shadow=None), pivot=(506, 520),
      anim=dict(orbitRadius=(40, 20), orbitSpeed=0.15, stretch=(0.6, 0), scaleSpeed=5)),
]

L326_DIFFS = [
    ("rainbow", 560, 92, 0),
    ("cottage", 120, 318, 0),
    ("mane", 340, 440, 0),
    ("flower", 820, 450, 0),
    ("crystal", 120, 560, 0),
]


# =================================================================== Level 327 snowman village
def snowman(c, x, base, s, scarf, hat=(40, 40, 50)):
    piece(c, [Circ(x, base - 30 * s, 30 * s), Circ(x, base - 76 * s, 22 * s), Circ(x, base - 110 * s, 16 * s)], (246, 248, 252), border=1.5,
          border_col=(170, 176, 200), shadow=PROP)
    flat(c, [RRect(x - 18 * s, base - 96 * s, x + 18 * s, base - 88 * s, 3), RRect(x + 6 * s, base - 92 * s, x + 14 * s, base - 70 * s, 2)], scarf)
    flat(c, [Circ(x - 6 * s, base - 114 * s, 2 * s), Circ(x + 6 * s, base - 114 * s, 2 * s), Circ(x, base - 76 * s, 2.4 * s), Circ(x, base - 64 * s, 2.4 * s)], INK)
    flat(c, Poly([(x, base - 110 * s), (x + 16 * s, base - 107 * s), (x, base - 104 * s)]), (250, 140, 40))
    if hat:
        piece(c, [RRect(x - 12 * s, base - 144 * s, x + 12 * s, base - 124 * s, 2), RRect(x - 18 * s, base - 126 * s, x + 18 * s, base - 122 * s, 1)], hat, shadow=None)


def l327_bg(c, d):
    sky(c, (170, 200, 236), (236, 240, 250), H)
    far_ridge(c, 190, 50, (210, 220, 240), 3271)
    for x in range(-20, W + 20, 40):
        tree_pine(c, x, 250 + (x % 3) * 6, h=60 + (x % 5) * 8, col=(70, 110, 110), snow=(240, 246, 252))
    c.rect(0, 260, W, H, (230, 236, 248))
    # snow hill with sled track (left back)
    piece(c, Poly([(0, 380), (0, 240), (120, 250), (300, 380)]), (240, 244, 252), border=1.5, border_col=(190, 196, 220), shadow=LAYER)
    sled = (200, 60, 60) if "sled" not in d else (60, 120, 200)
    piece(c, [RRect(110, 270, 170, 282, 3), Thick(104, 290, 176, 296, 2)], sled, shadow=SMALL)
    # snow-block huts
    for x, r, key in ((420, 70, "igloo"), (720, 60, None)):
        col = (240, 244, 252) if not (key and key in d) else (200, 226, 250)
        piece(c, Poly([(x + r * math.cos(math.pi * k / 16), 360 - r * math.sin(math.pi * k / 16)) for k in range(17)]), col, border=1.5, border_col=(170, 180, 210),
              shadow=PROP)
        for j in range(1, 4):
            flat(c, Thick(x - r * math.cos(math.asin(j / 4)), 360 - r * j / 4, x + r * math.cos(math.asin(j / 4)), 360 - r * j / 4, 1.4), (200, 206, 226))
        flat(c, Poly([(x - 18, 360), (x - 18, 330)] + [(x + 18 * math.cos(math.pi * k / 8), 330 - 18 * math.sin(math.pi * k / 8)) for k in range(8, -1, -1)] + [(x + 18, 360)]),
             (90, 110, 150))
    # chimney flag on big igloo
    flat(c, Thick(440, 296, 440, 260, 2), (90, 80, 70))
    flag = (250, 200, 60) if "flag" not in d else (220, 80, 120)
    piece(c, Poly([(440, 260), (470, 268), (440, 276)]), flag, border=1, shadow=None)
    # snowman family
    snowman(c, 160, 560, 1.3, (220, 60, 60))
    snowman(c, 260, 570, 0.9, (60, 140, 220) if "scarf" not in d else (250, 200, 60), hat=None)
    snowman(c, 600, 560, 1.2, (90, 170, 110), hat=(40, 40, 50) if "tophat" not in d else (200, 60, 60))
    # ice slide (right)
    slide = (180, 220, 246) if "slide" not in d else (240, 180, 210)
    piece(c, Poly([(760, 600), (900, 420), (900, 450), (800, 600)]), slide, border=1.5, shadow=PROP)
    piece(c, RRect(860, 400, 900, 600, 2), (210, 230, 246), border=1.5, shadow=PROP)
    # snowball pile (centre front)
    for x, y in ((400, 590), (430, 590), (415, 568), (460, 594)):
        piece(c, Circ(x, y, 14), (246, 248, 252), border=1.2, border_col=(170, 176, 200), shadow=SMALL)
    # kid with mittens
    hx, hy = modern(c, 500, 600, (240, 140, 60), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.0)
    hat = (220, 60, 70) if "beanie" not in d else (90, 170, 120)
    piece(c, [Ell(hx, hy - 8, 15, 10), Circ(hx, hy - 20, 5)], hat, border=1, shadow=None)


L327_ELEMENTS = [
    E("snow1", lambda c, m: [flat(c, Circ(x, y, 2.4), (250, 252, 255)) for x, y in ((60, 80), (240, 40), (380, 160), (520, 100), (660, 30), (860, 180), (320, 260), (760, 300))],
      daynight="untinted", anim=dict(driftVelocity=(-6, 40), driftLength=120, driftFade=True)),
    E("snow2", lambda c, m: [flat(c, Circ(x, y, 2), (250, 252, 255)) for x, y in ((140, 180), (300, 100), (460, 230), (600, 180), (780, 60), (860, 330), (40, 300))],
      daynight="untinted", anim=dict(driftVelocity=(8, 36), driftLength=120, driftFade=True, phase=0.5)),
    E("slider", lambda c, m: modern(c, 870, 420, (90, 140, 220), bottom=(60, 60, 70), hair=(40, 30, 30), h=1.2), pivot=(870, 420),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=1.0)),
]

L327_DIFFS = [
    ("sled", 140, 282, 0),
    ("igloo", 420, 320, 0),
    ("flag", 452, 268, 0),
    ("scarf", 266, 482, 0),
    ("tophat", 600, 400, 0),
    ("slide", 830, 510, 0),
    ("beanie", 502, 488, 0),
]


# =================================================================== Level 328 penguin colony
def penguin(c, x, base, s, belly=(250, 250, 246), face=1):
    piece(c, [Ell(x, base - 24 * s, 14 * s, 24 * s), Circ(x + 2 * s * face, base - 50 * s, 10 * s)], (40, 44, 56), border=1, shadow=SMALL)
    flat(c, [Ell(x + 3 * s * face, base - 20 * s, 9 * s, 18 * s), Circ(x + 5 * s * face, base - 50 * s, 6 * s)], belly)
    flat(c, Poly([(x + 10 * s * face, base - 50 * s), (x + 18 * s * face, base - 48 * s), (x + 10 * s * face, base - 46 * s)]), (240, 160, 40))
    flat(c, [Ell(x - 4 * s, base + 1, 5 * s, 2 * s), Ell(x + 6 * s, base + 1, 5 * s, 2 * s)], (240, 160, 40))
    flat(c, Circ(x + 6 * s * face, base - 52 * s, 1.4 * s), INK)


def l328_bg(c, d):
    sky(c, (150, 200, 240), (230, 240, 250), H)
    cloud_bg(c, 200, 60, 0.6)
    # sea + iceberg + research boat
    c.rect(0, 200, W, 300, (70, 130, 180))
    berg = (240, 248, 252) if "iceberg" not in d else (180, 220, 240)
    piece(c, Poly([(560, 260), (600, 150), (640, 170), (680, 110), (740, 180), (780, 260)]), berg, border=1.5, border_col=(170, 190, 220), shadow=PROP)
    flat(c, Poly([(640, 170), (680, 110), (700, 260), (660, 260)]), (210, 228, 244))
    boat = (220, 70, 50) if "boat" not in d else (240, 200, 60)
    piece(c, Poly([(120, 240), (320, 236), (300, 262), (140, 264)]), boat, border=1.5, shadow=PROP)
    piece(c, [RRect(180, 200, 270, 238, 2), RRect(200, 180, 240, 202, 2)], (250, 250, 246), border=1.2, shadow=SMALL)
    # ice shelf
    piece(c, hill_strip(290, [(8, 0.01, 0.6), (4, 0.04, 1.0)]), (236, 242, 250), border=1.5, border_col=(180, 196, 220), shadow=LAYER)
    # penguins
    rnd = random.Random(3281)
    for k in range(9):
        x = 80 + k * 90 + rnd.uniform(-20, 20)
        y = 380 + (k % 3) * 40
        if k == 4 and "penguin" in d:
            continue
        penguin(c, x, y, 1.3 + (k % 2) * 0.2, face=1 if k % 2 else -1)
    # chick (fluffy grey) at front
    chick = (170, 170, 180) if "chick" not in d else (120, 90, 70)
    piece(c, [Ell(330, 560, 18, 22), Circ(334, 532, 12)], chick, border=1, shadow=SMALL)
    flat(c, [Circ(340, 530, 2), Poly([(346, 532), (354, 534), (346, 536)])], INK)
    penguin(c, 380, 580, 1.8, face=-1)
    # seal on a floe (right front)
    flat(c, Ell(760, 570, 110, 24), (210, 226, 240))
    seal = (130, 130, 140) if "seal" not in d else (190, 160, 120)
    piece(c, [Ell(760, 550, 60, 18), Circ(818, 538, 14), Poly([(700, 550), (680, 540), (684, 562)])], seal, border=1.2, shadow=SMALL)
    flat(c, [Circ(824, 534, 2), Circ(830, 542, 2)], INK)
    # scientist with clipboard (left front)
    hx, hy = modern(c, 120, 600, (220, 60, 50), bottom=(40, 40, 60), hair=(90, 60, 40), h=2.3)
    cb = (250, 250, 246) if "clipboard" not in d else (250, 200, 60)
    piece(c, RRect(140, 508, 176, 550, 2), cb, border=1.2, shadow=SMALL)
    flag = (240, 120, 40) if "flag" not in d else (90, 160, 220)
    flat(c, Thick(560, 600, 560, 480, 3), (90, 90, 100))
    piece(c, RRect(560, 480, 610, 510, 1), flag, border=1, shadow=None)


L328_ELEMENTS = [
    E("waddle", lambda c, m: penguin(c, 480, 470, 1.2), pivot=(480, 470), anim=dict(swingAngle=6, swingSpeed=1.6)),
    bird_el("gull", 400, 80, s=10, speed=14),
    E("splash", lambda c, m: [flat(c, Circ(x, 286, 3), (220, 240, 250)) for x in (440, 456)], pivot=(448, 286), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.2)),
]

L328_DIFFS = [
    ("boat", 220, 230, 0),
    ("iceberg", 670, 200, 0),
    ("penguin", 440, 360, 0),
    ("chick", 332, 548, 0),
    ("seal", 760, 548, 0),
    ("clipboard", 158, 530, 0),
    ("flag", 585, 495, 0),
]


# =================================================================== Level 329 pirate cove
def l329_bg(c, d):
    sky(c, (250, 190, 140), (250, 230, 190), H)
    sun_bg(c, 760, 120, 36, col=(250, 200, 100))
    # cliffs + sea
    piece(c, Poly([(-20, 300), (-20, 60), (80, 80), (160, 160), (200, 300)]), (150, 120, 100), border=1.5, shadow=LAYER)
    c.rect(0, 280, W, 460, (60, 120, 160))
    for k in range(8):
        flat(c, Thick(220 + k * 80, 300 + (k % 3) * 40, 260 + k * 80, 300 + (k % 3) * 40, 1.6), (250, 200, 160))
    # moored ship (right back)
    hull = (110, 70, 50)
    piece(c, Poly([(560, 330), (860, 330), (830, 380), (590, 380)]), hull, border=1.5, shadow=PROP)
    flat(c, Thick(570, 346, 850, 346, 4), (200, 160, 70))
    for x in (640, 760):
        flat(c, Thick(x, 330, x, 150, 4), (90, 60, 40))
        piece(c, RRect(x - 50, 170, x + 50, 270, 4), (240, 230, 210), border=1.2, shadow=SMALL)
    fl = (40, 40, 46) if "flag" not in d else (200, 60, 60)
    piece(c, Poly([(760, 150), (800, 158), (760, 168)]), fl, border=1, shadow=None)
    flat(c, Circ(774, 158, 3), (250, 250, 246))
    # tavern on the dock (left)
    piece(c, RRect(60, 220, 280, 380, 2), (170, 120, 80), border=1.5, shadow=PROP)
    for y in range(230, 380, 14):
        flat(c, Thick(60, y, 280, y, 1.2), (150, 104, 70))
    piece(c, Poly([(44, 224), (296, 224), (230, 170), (110, 170)]), (90, 70, 60), border=1.5, shadow=PROP)
    sign = (200, 160, 70) if "sign" not in d else (90, 140, 200)
    flat(c, Thick(290, 240, 330, 240, 3), (60, 50, 40))
    piece(c, RRect(296, 244, 336, 284, 3), sign, border=1.2, shadow=SMALL)
    win = (250, 210, 120)
    flat(c, [RRect(90, 260, 130, 300, 2), RRect(210, 260, 250, 300, 2)], win)
    flat(c, RRect(150, 310, 190, 380, 3), (80, 50, 40))
    # dock
    piece(c, RRect(0, 380, W, 410, 2), (150, 110, 70), border=1.2, shadow=PROP)
    for x in range(10, W, 50):
        piece(c, RRect(x, 410, x + 10, 470, 1), (120, 86, 56), shadow=SMALL)
    c.rect(0, 470, W, H, (220, 200, 150))
    # pirates
    hx, hy = modern(c, 400, 384, (200, 60, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0)
    hat = (40, 40, 46) if "hat" not in d else (120, 80, 50)
    piece(c, Poly([(hx - 22, hy - 6), (hx + 22, hy - 6), (hx + 12, hy - 20), (hx, hy - 14), (hx - 12, hy - 20)]), hat, border=1, shadow=None)
    parrot = (60, 180, 90) if "parrot" not in d else (240, 90, 60)
    piece(c, [Ell(hx - 18, hy + 16, 7, 11), Circ(hx - 16, hy + 4, 6)], parrot, border=1, shadow=None)
    modern(c, 520, 384, (240, 236, 220), bottom=(60, 60, 80), hair=(150, 90, 50), h=1.9)
    # treasure crates + barrels (front)
    for x0 in (60, 160):
        piece(c, RRect(x0, 520, x0 + 90, 590, 2), (170, 120, 70), border=1.5, shadow=PROP)
        flat(c, [Thick(x0, 520, x0 + 90, 590, 3), Thick(x0 + 90, 520, x0, 590, 3)], (140, 96, 56))
    gold = (250, 200, 60) if "gold" not in d else (200, 200, 220)
    piece(c, [RRect(380, 540, 500, 590, 3), Poly([(376, 542), (504, 542), (494, 516), (386, 516)])], (130, 80, 50), border=1.5, shadow=PROP)
    flat(c, [Circ(400 + k * 14, 512 - (k % 2) * 6, 8) for k in range(7)], gold)
    for k, x in enumerate((640, 720)):
        band = (60, 60, 70) if not (k == 1 and "barrel" in d) else (220, 180, 60)
        piece(c, Ell(x, 548, 36, 46), (150, 100, 60), border=1.5, shadow=PROP)
        flat(c, [Thick(x - 34, 526, x + 34, 526, 4), Thick(x - 34, 570, x + 34, 570, 4)], band)
    # anchor (right front)
    anc = (90, 90, 100) if "anchor" not in d else (200, 120, 60)
    piece(c, [Thick(840, 470, 840, 580, 6), Thick(806, 490, 874, 490, 5), Thick(800, 560, 840, 590, 6), Thick(880, 560, 840, 590, 6)], anc, border=1, shadow=PROP)
    c.ellipse_ring(840, 462, 10, 10, 4, anc)


L329_ELEMENTS = [
    bird_el("gull", 400, 100, s=10, speed=14),
    E("lamp", lambda c, m: soft_union(c, [RRect(90, 260, 130, 300, 2), RRect(210, 260, 250, 300, 2)], (255, 210, 120), 0.3, spread=16), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=1.0)),
    E("bobship", lambda c, m: flat(c, Thick(560, 384, 860, 384, 3), (250, 210, 170)), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.5)),
    E("signswing", lambda c, m: flat(c, Thick(300, 240, 300, 244, 2), (60, 50, 40)), pivot=(300, 240), anim=dict(swingAngle=6, swingSpeed=0.6)),
]

L329_DIFFS = [
    ("flag", 778, 158, 0),
    ("sign", 316, 264, 0),
    ("hat", 402, 270, 0),
    ("parrot", 386, 300, 0),
    ("gold", 440, 512, 0),
    ("barrel", 720, 548, 0),
    ("anchor", 840, 520, 0),
]


# =================================================================== Level 330 alien garden
def l330_bg(c, d):
    c.gradient(0, H, (40, 20, 80), (160, 80, 140))
    stars_bg(c, 3301, 80, 250)
    m1 = (240, 200, 120) if "moon" not in d else (140, 220, 200)
    npiece(c, Circ(160, 100, 40), m1, shadow=None)
    npiece(c, Circ(250, 70, 18), (200, 170, 240), shadow=None)
    # saucer (right top)
    sau = (180, 190, 210) if "saucer" not in d else (240, 160, 90)
    npiece(c, [Ell(720, 130, 80, 18), Ell(720, 116, 36, 22)], sau)
    flat(c, Ell(720, 110, 26, 14), (160, 230, 240))
    for x in (670, 700, 740, 770):
        flat(c, Circ(x, 134, 4), (250, 250, 150))
    # purple ground
    npiece(c, hill_strip(320, [(20, 0.008, 0.4), (8, 0.03, 1.0)]), (90, 50, 110), shadow=LAYER)
    npiece(c, hill_strip(400, [(10, 0.01, 1.2), (5, 0.04, 0.4)]), (110, 60, 130), shadow=LAYER)
    # strange plants
    for x, h, col, key in ((80, 200, (90, 220, 180), "stalk"), (300, 150, (240, 120, 200), None), (560, 180, (120, 200, 250), None), (840, 220, (250, 200, 90), None)):
        cc = col if not (key and key in d) else (250, 110, 90)
        npiece(c, Thick(x, 420, x + 10, 420 - h, 6), (60, 120, 100), shadow=SMALL)
        npiece(c, [Circ(x + 10, 420 - h, 26), Circ(x - 14, 420 - h + 20, 14), Circ(x + 34, 420 - h + 16, 14)], cc, shadow=SMALL)
        flat(c, Circ(x + 4, 420 - h - 6, 8), lit(cc, 1.25))
    # spiral plant (centre)
    sp = (120, 240, 160) if "spiral" not in d else (240, 240, 120)
    for k in range(30):
        a = k * 0.5
        r = 4 + k * 1.3
        flat(c, Circ(440 + r * math.cos(a), 340 + r * math.sin(a), 4), sp)
    flat(c, Thick(440, 420, 440, 380, 5), (60, 120, 100))
    # round creatures
    for x, y, col, key in ((220, 520, (120, 220, 120), "creature"), (620, 540, (250, 160, 90), None)):
        cc = col if not (key and key in d) else (120, 160, 250)
        npiece(c, [Ell(x, y, 40, 32), Thick(x - 10, y - 30, x - 18, y - 56, 3), Thick(x + 10, y - 30, x + 18, y - 56, 3)], cc)
        flat(c, [Circ(x - 18, y - 58, 5), Circ(x + 18, y - 58, 5)], lit(cc, 1.2))
        flat(c, Circ(x, y - 6, 12), (250, 250, 246))
        flat(c, Circ(x + 2, y - 6, 6), INK)
    # glowing mushrooms (front)
    for k, x in enumerate((420, 470, 760, 810)):
        col = (120, 230, 250) if not (k == 2 and "shroom" in d) else (250, 120, 180)
        npiece(c, [RRect(x - 4, 570, x + 4, 600, 2), Ell(x, 570, 18, 10)], col, shadow=SMALL)
    # crashed rover (left front)
    npiece(c, [RRect(40, 560, 140, 590, 4)], (170, 170, 180))
    for x in (60, 120):
        wheel(c, x, 596, 10, tyre=(50, 50, 60), hub=(170, 170, 180))


L330_ELEMENTS = [
    E("beam", lambda c, m: soft_union(c, [Poly([(700, 140), (740, 140), (790, 320), (650, 320)])], (200, 250, 220), 0.2, spread=10), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=0.6)),
    E("glow", lambda c, m: soft_union(c, [Circ(x, 570, 14) for x in (420, 470, 760, 810)], (150, 240, 250), 0.3, spread=14), daynight="untinted",
      anim=dict(twinkle=0.6, twinkleSpeed=1.0)),
    E("spore1", lambda c, m: flat(c, Circ(320, 300, 3), (250, 200, 250)), pivot=(320, 300), daynight="untinted",
      anim=dict(driftVelocity=(10, -30), driftLength=120, driftFade=True)),
    E("spore2", lambda c, m: flat(c, Circ(580, 280, 3), (200, 250, 250)), pivot=(580, 280), daynight="untinted",
      anim=dict(driftVelocity=(-8, -26), driftLength=120, driftFade=True, phase=0.5)),
    E("hover", lambda c, m: npiece(c, [Ell(500, 200, 20, 10), Circ(500, 192, 8)], (150, 240, 200), shadow=None), pivot=(500, 200),
      anim=dict(bobAmplitude=(30, 10), bobSpeed=0.25)),
]

L330_DIFFS = [
    ("moon", 160, 100, 0),
    ("saucer", 720, 124, 0),
    ("stalk", 90, 230, 0),
    ("spiral", 440, 340, 0),
    ("creature", 220, 510, 0),
    ("shroom", 760, 576, 0),
]


# =================================================================== Level 331 chocolate factory
CHOC = (110, 64, 40)


def l331_bg(c, d):
    c.rect(0, 0, W, H, (240, 220, 200))
    for x in range(0, W, 80):
        flat(c, Thick(x, 0, x, 400, 3), (230, 208, 186))
    # pipes along the top
    for y, col in ((40, (200, 200, 210)), (64, (240, 140, 160))):
        flat(c, Thick(0, y, W, y, 12), col)
    # melting vats (back)
    for k, x in enumerate((160, 450, 740)):
        vat = (200, 200, 210) if not (k == 1 and "vat" in d) else (240, 180, 90)
        piece(c, [RRect(x - 90, 120, x + 90, 280, 10), Thick(x, 64, x, 120, 8)], vat, border=1.5, shadow=PROP)
        flat(c, Ell(x, 130, 80, 12), CHOC if k != 2 else (250, 240, 220))
        flat(c, [Circ(x - 50, 220, 10), Circ(x + 50, 220, 10)], (90, 90, 100))
        gauge = (250, 250, 246)
        flat(c, Circ(x, 200, 22), gauge)
        flat(c, Thick(x, 200, x + 14, 190, 2), INK)
    # chocolate river with a waterfall (middle)
    flat(c, Poly([(0, 330), (W, 320), (W, 400), (0, 410)]), CHOC)
    for k in range(8):
        flat(c, Thick(30 + k * 110, 360 + (k % 2) * 16, 80 + k * 110, 360 + (k % 2) * 16, 2), lit(CHOC, 1.3))
    flat(c, Poly([(600, 280), (640, 280), (650, 330), (590, 330)]), lit(CHOC, 1.1))
    # candy-cane bridge
    piece(c, Poly([(200, 330), (400, 330), (390, 300), (210, 300)]), (250, 250, 246), border=1.2, shadow=PROP)
    for x in range(210, 400, 24):
        flat(c, Thick(x, 300, x + 12, 330, 6), (220, 60, 60))
    # conveyor with bars (front)
    piece(c, RRect(0, 460, W, 490, 4), (90, 90, 100), border=1.5, shadow=PROP)
    for k, x in enumerate(range(40, W, 110)):
        wrap = [(220, 60, 60), (60, 120, 200), (250, 200, 60)][k % 3]
        if k == 4 and "bar" in d:
            wrap = (90, 180, 110)
        piece(c, RRect(x, 436, x + 70, 462, 3), CHOC, border=1, shadow=SMALL)
        flat(c, RRect(x + 20, 436, x + 50, 462, 2), wrap)
    # workers
    for x, top, key in ((300, (250, 250, 246), "worker"), (620, (250, 250, 246), None)):
        hx, hy = modern(c, x, 600, top, bottom=(60, 60, 80), hair=(60, 40, 30), h=2.3)
        cap = (240, 140, 160) if not (key and key in d) else (90, 160, 220)
        piece(c, Ell(hx, hy - 10, 16, 9), cap, shadow=None)
    # stack of boxes (left front)
    box = (240, 200, 210) if "box" not in d else (180, 220, 160)
    for k, (x0, y0) in enumerate(((40, 540), (120, 540), (80, 490))):
        piece(c, RRect(x0, y0, x0 + 80, y0 + 50, 3), box if k == 0 else (240, 200, 210), border=1.5, shadow=PROP)
        flat(c, Thick(x0 + 40, y0, x0 + 40, y0 + 50, 4), (220, 60, 60))
    # tasting table (right front)
    piece(c, [Ell(800, 540, 80, 14), RRect(794, 540, 806, 600, 2)], (250, 250, 246), border=1.2, shadow=PROP)
    truf = CHOC if "truffle" not in d else (250, 240, 220)
    flat(c, [Circ(770 + k * 20, 528 - (k % 2) * 6, 9) for k in range(4)], truf)


L331_ELEMENTS = [
    E("pour", lambda c, m: flat(c, Thick(450, 280, 450, 330, 10), CHOC), pivot=(450, 280), anim=dict(stretch=(0, 0.2), scaleSpeed=2.0)),
    E("belt", lambda c, m: [flat(c, Thick(x, 480, x + 14, 480, 3), (130, 130, 140)) for x in range(0, W, 40)], anim=dict(driftVelocity=(40, 0), driftLength=40)),
    E("stir", lambda c, m: flat(c, Thick(160, 130, 200, 100, 4), (150, 110, 70)), pivot=(160, 130), anim=dict(swingAngle=20, swingSpeed=0.8)),
    E("bubble", lambda c, m: flat(c, Circ(600, 370, 6), lit(CHOC, 1.3)), pivot=(600, 370), anim=dict(stretch=(0.5, 0.5), scaleSpeed=1.0)),
]

L331_DIFFS = [
    ("vat", 450, 200, 0),
    ("bar", 515, 449, 0),
    ("worker", 302, 480, 0),
    ("box", 80, 565, 0),
    ("truffle", 800, 526, 0),
]


# =================================================================== Level 332 weather station
def l332_bg(c, d):
    sky(c, (110, 170, 230), (220, 236, 248), H)
    cloud_bg(c, 150, 120, 0.7)
    peaks = [(-40, 340), (120, 200), (300, 300), (500, 160), (700, 280), (940, 200)]
    piece(c, Poly(peaks + [(940, 400), (-40, 400)]), (160, 176, 200), border=1.5, shadow=LAYER)
    c.rect(0, 360, W, H, (200, 196, 180))
    piece(c, hill_strip(360, [(10, 0.01, 0.6), (5, 0.04, 1.0)]), (190, 190, 170), shadow=LAYER)
    # station building (left)
    piece(c, RRect(60, 280, 300, 440, 2), (240, 240, 236), border=1.5, shadow=PROP)
    roof = (200, 70, 60) if "roof" not in d else (60, 120, 170)
    piece(c, Poly([(44, 284), (316, 284), (280, 244), (80, 244)]), roof, border=1.5, shadow=PROP)
    flat(c, [RRect(90, 320, 150, 370, 2), RRect(200, 320, 260, 370, 2)], (170, 210, 236))
    flat(c, RRect(160, 380, 196, 440, 2), (90, 80, 80))
    # radar dome (centre)
    dome = (250, 250, 246) if "radar" not in d else (240, 200, 90)
    piece(c, [RRect(430, 300, 470, 440, 2)], (200, 200, 210), border=1.5, shadow=PROP)
    piece(c, Circ(450, 270, 50), dome, border=1.5, shadow=PROP)
    for k in range(-2, 3):
        flat(c, Thick(450 + k * 18, 224 + abs(k) * 4, 450 + k * 18, 316 - abs(k) * 4, 1.2), lit(dome, 0.9))
    # mast with anemometer (cups are an element) + wind vane
    flat(c, Thick(640, 440, 640, 160, 4), (150, 150, 160))
    vane = (220, 60, 50) if "vane" not in d else (90, 160, 90)
    piece(c, Poly([(640, 200), (700, 192), (700, 208)]), vane, border=1, shadow=None)
    piece(c, Poly([(640, 200), (610, 190), (616, 200), (610, 210)]), vane, border=1, shadow=None)
    # instrument box on legs (right)
    box = (250, 250, 246) if "box" not in d else (200, 220, 160)
    piece(c, [RRect(740, 330, 860, 400, 2), Thick(756, 400, 756, 460, 3), Thick(844, 400, 844, 460, 3)], box, border=1.5, shadow=PROP)
    for y in range(340, 400, 10):
        flat(c, Thick(744, y, 856, y, 1.4), (210, 210, 214))
    # meteorologist releasing a balloon (front)
    hx, hy = modern(c, 300, 590, (240, 140, 50), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.4)
    flat(c, Thick(hx + 10, hy + 30, 360, 480, 1.2), (90, 90, 100))
    # solar panel (right front)
    sol = (60, 80, 140) if "solar" not in d else (150, 160, 170)
    piece(c, Poly([(720, 560), (860, 560), (880, 500), (740, 500)]), sol, border=1.5, shadow=PROP)
    flat(c, [Thick(790, 500, 790, 560, 2), Thick(730, 530, 870, 530, 2)], lit(sol, 1.4))
    flat(c, Thick(800, 560, 800, 600, 4), (150, 150, 160))
    # rain gauge (left front)
    rg = (90, 140, 200) if "gauge" not in d else (220, 120, 60)
    piece(c, [RRect(100, 520, 130, 590, 3), Poly([(90, 520), (140, 520), (130, 506), (100, 506)])], rg, border=1.2, shadow=SMALL)
    # flag on the building
    flat(c, Thick(280, 244, 280, 200, 2), (90, 90, 100))
    piece(c, Poly([(280, 200), (316, 208), (280, 216)]), (250, 200, 60), border=1, shadow=None)


L332_ELEMENTS = [
    E("cups", lambda c, m: [flat(c, Thick(640, 160, 640 + 30 * math.cos(a), 160 + 8 * math.sin(a), 2), (90, 90, 100)) for a in (0, 2.09, 4.19)] +
      [piece(c, Circ(640 + 30 * math.cos(a), 160 + 8 * math.sin(a), 6), (250, 250, 246), shadow=None) for a in (0, 2.09, 4.19)],
      pivot=(640, 160), anim=dict(stretch=(0.8, 0), scaleSpeed=3.0)),
    E("balloon", lambda c, m: [flat(c, Thick(360, 480, 380, 420, 1.2), (90, 90, 100)), piece(c, Circ(380, 400, 24), (250, 250, 246), shadow=SMALL)], pivot=(380, 400),
      anim=dict(driftVelocity=(10, -60), driftLength=260, driftFade=True, driftGrow=-0.3)),
    E("sweep", lambda c, m: soft_union(c, [Circ(450, 270, 50)], (200, 240, 255), 0.2, spread=10), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.8)),
    cloud_el("cloud", 700, 90, 0.5, -6),
]

L332_DIFFS = [
    ("roof", 180, 260, 0),
    ("radar", 450, 270, 0),
    ("vane", 660, 200, 0),
    ("box", 800, 365, 0),
    ("solar", 800, 530, 0),
    ("gauge", 115, 545, 0),
]


# =================================================================== Level 333 rowing regatta
def rowing_boat(c, x, y, col, rowers=4, kit=(250, 250, 246)):
    piece(c, Poly([(x - 140, y), (x + 150, y - 2), (x + 130, y + 12), (x - 120, y + 14)]), col, border=1.2, shadow=SMALL)
    for k in range(rowers):
        rx = x - 90 + k * 56
        flat(c, Circ(rx, y - 22, 8), SKIN)
        flat(c, RRect(rx - 8, y - 14, rx + 8, y + 2, 3), kit)


def l333_bg(c, d):
    sky(c, (130, 190, 240), (230, 240, 250), H)
    cloud_bg(c, 680, 60, 0.6)
    far_ridge(c, 170, 40, (170, 190, 200), 3331)
    far_round_trees(c, 200, 24, (100, 150, 100), 3332)
    # boathouse (left back)
    piece(c, RRect(40, 150, 260, 230, 2), (240, 236, 226), border=1.5, shadow=PROP)
    roof = (60, 110, 160) if "boathouse" not in d else (200, 80, 60)
    piece(c, Poly([(26, 154), (274, 154), (150, 110)]), roof, border=1.5, shadow=PROP)
    for x in (80, 150, 220):
        flat(c, Poly([(x - 24, 230), (x - 24, 190), (x, 176), (x + 24, 190), (x + 24, 230)]), (90, 80, 80))
    # spectators stand (right back)
    piece(c, RRect(560, 150, 880, 220, 2), (200, 200, 210), border=1.5, shadow=PROP)
    rnd = random.Random(3333)
    for r in range(2):
        for x in range(580, 870, 22):
            flat(c, Circ(x + r * 11, 168 + r * 24, 7), SKIN)
            flat(c, RRect(x + r * 11 - 7, 174 + r * 24, x + r * 11 + 7, 186 + r * 24, 3), rnd.choice([(220, 60, 60), (60, 110, 200), (250, 200, 60), (250, 250, 246)]))
    bunting(c, 560, 140, 880, 140, [(220, 60, 60), (250, 250, 246), (60, 110, 200)], 9, sag=10, size=12)
    # lake
    c.rect(0, 230, W, H, (70, 140, 190))
    for k in range(12):
        flat(c, Thick(20 + k * 80, 260 + (k % 4) * 80, 60 + k * 80, 260 + (k % 4) * 80, 1.6), (130, 190, 226))
    # lane buoys
    for y in (300, 400, 500):
        for x in range(20, W, 50):
            flat(c, Circ(x, y, 4), (250, 200, 60))
    # boats
    rowing_boat(c, 300, 280, (250, 250, 246), kit=(220, 60, 60))
    rowing_boat(c, 520, 380, (240, 200, 70) if "boat" not in d else (60, 160, 120), kit=(60, 110, 200))
    rowing_boat(c, 380, 480, (250, 250, 246), kit=(250, 200, 60) if "kit" not in d else (200, 90, 200))
    # finish buoy + judge boat (right)
    fb = (220, 60, 50) if "finish" not in d else (60, 180, 90)
    piece(c, [Circ(820, 330, 16), Thick(820, 314, 820, 280, 2), Poly([(820, 280), (850, 288), (820, 296)])], fb, border=1.2, shadow=SMALL)
    piece(c, Poly([(700, 560), (880, 556), (860, 586), (720, 590)]), (250, 250, 246), border=1.5, shadow=PROP)
    hx, hy = modern(c, 790, 564, (240, 200, 60), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.8)
    mega = (240, 120, 40) if "megaphone" not in d else (90, 160, 220)
    piece(c, Poly([(hx + 6, hy + 4), (hx + 30, hy - 8), (hx + 30, hy + 18)]), mega, border=1, shadow=None)
    # swan (left front)
    if "swan" not in d:
        piece(c, [Ell(100, 560, 34, 14), Thick(124, 552, 128, 516, 5), Ell(132, 512, 9, 6)], (250, 250, 246), border=1.2, shadow=SMALL)
        flat(c, Poly([(140, 512), (150, 514), (140, 516)]), (240, 140, 40))


def oar_el(eid, x, y, n, phase):
    return E(eid, lambda c, m: [flat(c, Thick(x - 90 + k * 56, y - 6, x - 110 + k * 56, y + 26, 2.4), (120, 90, 60)) for k in range(n)], pivot=(x, y + 4),
             anim=dict(swingAngle=10, swingSpeed=1.2, phase=phase))


L333_ELEMENTS = [
    oar_el("oar1", 300, 280, 4, 0.0),
    oar_el("oar2", 520, 380, 4, 0.3),
    oar_el("oar3", 380, 480, 4, 0.6),
    bird_el("bird", 450, 80, s=9, speed=14),
]

L333_DIFFS = [
    ("boathouse", 150, 135, 0),
    ("boat", 525, 385, 0),
    ("kit", 360, 472, 0),
    ("finish", 828, 310, 0),
    ("megaphone", 812, 474, 0),
    ("swan", 112, 545, 0),
]


# =================================================================== Level 334 Roman forum
def l334_bg(c, d):
    sky(c, (120, 180, 236), (240, 230, 210), H)
    cloud_bg(c, 680, 50, 0.6)
    far_ridge(c, 190, 30, (190, 196, 190), 3341)
    # temple front (centre back)
    piece(c, RRect(300, 250, 600, 270, 2), (236, 230, 216), border=1.5, shadow=PROP)
    for x in range(330, 600, 45):
        column(c, x, 250, 120, 22, (240, 236, 224))
    piece(c, RRect(300, 104, 600, 122, 2), (236, 230, 216), border=1.5, shadow=PROP)
    ped = (110, 150, 200) if "pediment" not in d else (200, 120, 90)
    piece(c, Poly([(292, 106), (608, 106), (450, 56)]), (236, 230, 216), border=1.5, shadow=PROP)
    flat(c, Poly([(330, 100), (570, 100), (450, 66)]), ped)
    # triumphal arch (left)
    piece(c, [RRect(40, 120, 240, 280, 2)], (220, 200, 170), border=1.5, shadow=PROP)
    flat(c, Poly([(100, 280), (100, 200)] + [(140 + 40 * math.cos(math.pi * k / 10), 200 - 40 * math.sin(math.pi * k / 10)) for k in range(10, -1, -1)] + [(180, 280)]), (120, 170, 220))
    arch_top = (200, 160, 80) if "arch" not in d else (150, 150, 160)
    piece(c, RRect(30, 100, 250, 126, 2), arch_top, border=1.2, shadow=SMALL)
    # aqueduct (right back)
    for k in range(4):
        x = 680 + k * 60
        piece(c, Poly([(x, 270), (x, 150), (x + 60, 150), (x + 60, 270), (x + 50, 270)] + [(x + 30 + 20 * math.cos(math.pi * j / 8), 220 - 20 * math.sin(math.pi * j / 8))
                                                                                       for j in range(9)] + [(x + 10, 270)]), (210, 180, 150), border=1.2, shadow=PROP)
    # paved square
    c.rect(0, 270, W, H, (220, 206, 176))
    for y in range(290, H, 30):
        for x in range(-((y // 30) % 2) * 30, W, 60):
            flat(c, RRect(x + 2, y + 2, x + 58, y + 28, 3), (226, 212, 184))
    # fountain (centre)
    piece(c, [Ell(450, 390, 110, 24), RRect(340, 390, 560, 420, 6)], (200, 196, 186), border=1.5, shadow=PROP)
    flat(c, Ell(450, 392, 96, 18), (120, 180, 220))
    statue = (240, 236, 226) if "statue" not in d else (200, 150, 90)
    piece(c, [RRect(436, 330, 464, 390, 3)], (200, 196, 186), border=1.2, shadow=SMALL)
    toga(c, 450, 330, 1.4, statue, skin=statue, hair=lit(statue, 0.9))
    # stalls (left middle)
    aw = (200, 70, 60) if "awning" not in d else (60, 120, 170)
    piece(c, [Poly([(40, 330), (250, 330), (240, 300), (50, 300)])], aw, border=1.5, shadow=PROP)
    flat(c, [Thick(60, 330, 60, 400, 3), Thick(230, 330, 230, 400, 3)], (120, 90, 60))
    piece(c, RRect(50, 380, 240, 410, 2), (170, 120, 80), border=1.2, shadow=SMALL)
    amphora(c, 90, 380, 0.7, (200, 110, 60))
    amphora(c, 130, 380, 0.6, (190, 120, 70))
    flat(c, [Circ(180 + k * 14, 372, 7) for k in range(4)], (130, 90, 150))
    # citizens
    toga(c, 300, 540, 2.0, (250, 246, 236), beard=(120, 100, 80))
    toga(c, 620, 520, 1.9, (200, 120, 90) if "toga" not in d else (90, 140, 200))
    # chariot (right front)
    ch = (200, 160, 70) if "chariot" not in d else (150, 80, 60)
    piece(c, [Poly([(700, 560), (790, 560), (780, 500), (710, 510)])], ch, border=1.5, shadow=PROP)
    wheel(c, 745, 572, 26, tyre=(110, 80, 60), hub=(200, 170, 120))
    piece(c, [Ell(840, 520, 40, 18), Thick(866, 510, 880, 476, 10), Ell(884, 470, 12, 9)], (190, 140, 100), border=1.2, shadow=PROP)
    for lx in (820, 836, 856, 868):
        flat(c, RRect(lx - 3, 530, lx + 3, 580, 1), (170, 120, 86))
    # pigeon (left front)
    piece(c, [Ell(120, 580, 16, 9), Circ(134, 572, 6)], (150, 156, 170), border=1, shadow=SMALL)


L334_ELEMENTS = [
    E("water", lambda c, m: [flat(c, Thick(450 + dx, 330, 450 + dx * 2.6, 384, 2), (200, 230, 250)) for dx in (-30, -15, 15, 30)], daynight="untinted",
      anim=dict(twinkle=0.5, twinkleSpeed=1.4)),
    E("pigeon", lambda c, m: piece(c, [Ell(300, 140, 10, 5), Circ(308, 138, 4)], (150, 156, 170), shadow=None), pivot=(300, 140),
      anim=dict(orbitRadius=(60, 16), orbitSpeed=0.12)),
    E("peck", lambda c, m: piece(c, Circ(148, 590, 4), (150, 156, 170), shadow=None), pivot=(134, 580), anim=dict(swingAngle=20, swingSpeed=1.6)),
]

L334_DIFFS = [
    ("pediment", 450, 86, 0),
    ("arch", 140, 113, 0),
    ("awning", 145, 315, 0),
    ("statue", 452, 300, 0),
    ("toga", 620, 480, 0),
    ("chariot", 745, 545, 0),
]


LEVELS = [
    ("Level325", "海底宫殿", l325_bg, L325_ELEMENTS, L325_DIFFS, 60, OPTS),
    ("Level326", "彩虹山谷", l326_bg, L326_ELEMENTS, L326_DIFFS, 60, OPTS),
    ("Level327", "雪人村", l327_bg, L327_ELEMENTS, L327_DIFFS, 60, OPTS),
    ("Level328", "企鹅聚居地", l328_bg, L328_ELEMENTS, L328_DIFFS, 60, OPTS),
    ("Level329", "海盗港湾", l329_bg, L329_ELEMENTS, L329_DIFFS, 60, OPTS),
    ("Level330", "外星花园", l330_bg, L330_ELEMENTS, L330_DIFFS, 60, OPTS),
    ("Level331", "巧克力工厂", l331_bg, L331_ELEMENTS, L331_DIFFS, 60, OPTS),
    ("Level332", "气象站", l332_bg, L332_ELEMENTS, L332_DIFFS, 60, OPTS),
    ("Level333", "赛艇湖", l333_bg, L333_ELEMENTS, L333_DIFFS, 60, OPTS),
    ("Level334", "古罗马广场", l334_bg, L334_ELEMENTS, L334_DIFFS, 60, OPTS),
]
