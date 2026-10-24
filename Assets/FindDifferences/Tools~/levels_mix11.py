# -*- coding: utf-8 -*-
"""Mixed themes part 11 (paper-craft side views around the world, full-bleed, original designs, no brands):
  Level335 维京村庄   - a Norse fjord village: longhouses with turf roofs, a dragon-prow longship, shields
  Level336 草原毡房   - a grassland camp: felt yurts, horses, sheep, a rider, prayer-flag-free colour streamers
  Level337 白色崖城   - a whitewashed cliff village by the sea: blue domes, bell tower, stairways, bougainvillea
  Level338 温泉泻湖   - a geothermal lagoon: milky-blue pool, steam, lava rocks, bathers, a spa hut
  Level339 热带鸟园   - a walk-through aviary: parrots, toucans, hanging feeders, net dome, visitors
  Level340 清晨菜市场 - a morning farmers' market: vegetable crates, flower buckets, scales, shoppers
  Level341 赛车维修站 - a race pit stop: race car, crew changing tyres, pit wall, tyre stacks, lollipop sign
  Level342 马厩       - a horse stable: stalls with horses, hay loft, saddles, buckets, a stable hand
  Level343 竹筏漂流   - bamboo rafting on a river among karst peaks: rafts, boatman, water buffalo, village
  Level344 极光小镇   - a northern town at night under the aurora: wooden houses, lit windows, a sled dog team
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, fish, layer, palm, rock, sky, smoke_el, stars_bg, sun_bg,
                 tree_pine, tree_round)
from fills import far_forest, far_ridge, far_round_trees
from levels_akiba import modern, sign_box
from levels_festival import npiece
from levels_homes import planks
from levels_mix2 import wheel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def horse_side(c, x, base, s, col, mane=(60, 40, 30), face=1):
    for lx in (-22, -12, 14, 24):
        flat(c, RRect(x + lx * s * face - 3 * s, base - 34 * s, x + lx * s * face + 3 * s, base, 1), lit(col, 0.85))
    piece(c, [Ell(x, base - 40 * s, 32 * s, 13 * s), Thick(x + 24 * s * face, base - 46 * s, x + 36 * s * face, base - 70 * s, 9 * s),
              Ell(x + 44 * s * face, base - 70 * s, 13 * s, 7 * s)], col, border=1.2, shadow=PROP)
    flat(c, [Thick(x + 22 * s * face, base - 50 * s, x + 32 * s * face, base - 76 * s, 4 * s), Thick(x - 30 * s * face, base - 42 * s, x - 40 * s * face, base - 20 * s, 4 * s)], mane)
    flat(c, Circ(x + 42 * s * face, base - 73 * s, 1.6 * s), INK)


# =================================================================== Level 335 Viking village
def longhouse(c, x0, x1, base, h, wall=(140, 100, 70), turf=(110, 160, 90)):
    piece(c, RRect(x0, base - h, x1, base, 2), wall, border=1.5, shadow=PROP)
    for x in range(int(x0) + 10, int(x1), 14):
        flat(c, Thick(x, base - h + 4, x, base - 4, 1.4), lit(wall, 0.86))
    piece(c, Poly([(x0 - 14, base - h + 4), (x1 + 14, base - h + 4), (x1 - 20, base - h - 50), (x0 + 20, base - h - 50)]), turf, border=1.5, shadow=PROP)
    flat(c, [Thick(x0 + 20, base - h - 50, x0 + 4, base - h - 70, 4), Thick(x1 - 20, base - h - 50, x1 - 4, base - h - 70, 4)], (120, 80, 50))
    flat(c, RRect((x0 + x1) / 2 - 14, base - 40, (x0 + x1) / 2 + 14, base, 3), (70, 50, 40))


def l335_bg(c, d):
    sky(c, (150, 186, 220), (226, 230, 236), H)
    cloud_bg(c, 600, 60, 0.7)
    piece(c, Poly([(-20, 260), (-20, 80), (120, 60), (220, 160), (260, 260)]), (110, 120, 130), border=1.5, shadow=LAYER)
    piece(c, Poly([(920, 260), (920, 70), (800, 50), (700, 140), (640, 260)]), (120, 126, 136), border=1.5, shadow=LAYER)
    c.rect(0, 250, W, 360, (70, 110, 140))
    # longship (centre on the water)
    hull = (120, 80, 50)
    piece(c, Poly([(300, 300), (600, 300), (620, 270), (640, 230), (610, 250), (580, 330), (320, 330), (290, 250), (260, 230), (280, 270)]), hull, border=1.5, shadow=PROP)
    for k in range(7):
        shc = [(200, 60, 50), (250, 200, 60), (60, 110, 170)][k % 3]
        if k == 3 and "shield" in d:
            shc = (90, 160, 90)
        piece(c, Circ(330 + k * 40, 300, 13), shc, border=1, shadow=None)
        flat(c, Circ(330 + k * 40, 300, 4), (200, 200, 210))
    flat(c, Thick(450, 300, 450, 130, 4), (90, 60, 40))
    sail = (220, 60, 50) if "sail" not in d else (60, 110, 170)
    piece(c, RRect(380, 140, 520, 240, 3), sail, border=1.2, shadow=SMALL)
    for x in (400, 440, 480):
        flat(c, Thick(x, 140, x, 240, 8), (250, 246, 236))
    head = (200, 160, 70) if "prow" not in d else (90, 90, 100)
    piece(c, [Circ(640, 222, 12), Poly([(646, 216), (664, 220), (648, 228)])], head, border=1, shadow=None)
    # shore
    piece(c, hill_strip(360, [(8, 0.01, 0.6), (4, 0.04, 1.0)]), (130, 160, 100), shadow=LAYER)
    longhouse(c, 40, 280, 470, 70)
    longhouse(c, 620, 860, 460, 70, turf=(110, 160, 90) if "turf" not in d else (200, 170, 90))
    # people
    hx, hy = modern(c, 400, 560, (150, 110, 80), bottom=(80, 70, 60), hair=(220, 180, 100), h=2.4)
    helm = (170, 170, 180) if "helmet" not in d else (200, 160, 70)
    piece(c, Ell(hx, hy - 6, 16, 12), helm, border=1, shadow=None)
    flat(c, Thick(hx, hy - 6, hx, hy + 6, 3), helm)
    modern(c, 520, 570, (90, 120, 90), bottom=(80, 70, 60), hair=(200, 100, 60), h=2.2, style="long")
    # firewood + cauldron (right front)
    piece(c, [Ell(760, 560, 40, 30)], (50, 50, 56), border=1.2, shadow=PROP)
    flat(c, [Thick(720, 590, 800, 590, 6), Thick(730, 596, 790, 584, 6)], (120, 80, 50))
    # sheep (left front)
    sh = (240, 236, 226) if "sheep" not in d else (90, 80, 80)
    piece(c, [Circ(130 + k * 14, 560 + (k % 2) * 6, 14) for k in range(4)] + [Ell(190, 556, 9, 7)], sh, border=1, shadow=SMALL)
    flat(c, [Thick(140, 576, 140, 590, 3), Thick(170, 576, 170, 590, 3)], (60, 50, 50))


L335_ELEMENTS = smoke_el("smk", 160, 330, n=3, col=(220, 220, 226), r=10, rise=(8, -22), length=70) + [
    bird_el("raven", 300, 90, s=10, col=(40, 40, 46), speed=14),
    E("oars", lambda c, m: [flat(c, Thick(330 + k * 50, 320, 316 + k * 50, 352, 3), (150, 110, 70)) for k in range(6)], pivot=(450, 330),
      anim=dict(swingAngle=6, swingSpeed=0.8)),
    E("flame", lambda c, m: flat(c, Poly([(740, 532), (780, 532), (760, 500)]), (250, 160, 50)), pivot=(760, 532), daynight="untinted",
      anim=dict(stretch=(0.15, 0.3), scaleSpeed=4)),
]

L335_DIFFS = [
    ("sail", 450, 190, 0),
    ("shield", 450, 300, 0),
    ("prow", 650, 222, 0),
    ("turf", 740, 360, 0),
    ("helmet", 402, 444, 0),
    ("sheep", 160, 562, 0),
]


# =================================================================== Level 336 grassland yurts
def yurt(c, x, base, r, wall=(246, 240, 226), roof=(240, 236, 220), band=(200, 60, 60)):
    piece(c, RRect(x - r, base - r * 0.8, x + r, base, 2), wall, border=1.5, shadow=PROP)
    piece(c, Poly([(x - r - 6, base - r * 0.8 + 2), (x + r + 6, base - r * 0.8 + 2), (x + r * 0.2, base - r * 1.3), (x - r * 0.2, base - r * 1.3)]), roof, border=1.5,
          shadow=PROP)
    flat(c, [Thick(x - r, base - r * 0.5, x + r, base - r * 0.5, 4), Thick(x - r * 0.9, base - r * 0.9, x + r * 0.9, base - r * 0.9, 3)], band)
    flat(c, RRect(x - r * 0.2, base - r * 0.5, x + r * 0.2, base, 2), (200, 120, 60))


def l336_bg(c, d):
    sky(c, (90, 160, 236), (220, 236, 250), H)
    cloud_bg(c, 200, 70, 0.7)
    cloud_bg(c, 680, 50, 0.6)
    far_ridge(c, 200, 50, (150, 180, 170), 3361)
    c.rect(0, 230, W, H, (130, 190, 90))
    layer(c, 230, [(12, 0.006, 0.4), (5, 0.03, 1.0)], (136, 196, 96))
    yurt(c, 200, 340, 80, band=(200, 60, 60) if "band" not in d else (60, 110, 190))
    yurt(c, 440, 310, 60)
    yurt(c, 700, 330, 70, roof=(240, 236, 220) if "yurt" not in d else (200, 170, 120))
    # streamers on a pole
    flat(c, Thick(560, 340, 560, 200, 3), (120, 90, 60))
    for k in range(5):
        col = [(220, 60, 60), (250, 200, 60), (60, 140, 90), (60, 110, 190), (250, 250, 246)][k]
        if k == 1 and "streamer" in d:
            col = (200, 90, 200)
        piece(c, Poly([(560, 206 + k * 14), (600, 210 + k * 14), (560, 218 + k * 14)]), col, shadow=None)
    # horses
    horse_side(c, 300, 470, 1.4, (150, 100, 60))
    horse_side(c, 640, 460, 1.3, (240, 236, 226) if "horse" not in d else (60, 50, 50), face=-1)
    # rider on a horse (right front)
    horse_side(c, 800, 580, 1.6, (110, 70, 50), face=-1)
    hx, hy = modern(c, 790, 520, (60, 110, 170), bottom=(60, 60, 70), hair=(40, 30, 30), h=1.8)
    hat = (200, 150, 60) if "hat" not in d else (200, 60, 60)
    piece(c, [Ell(hx, hy - 8, 18, 6), Ell(hx, hy - 14, 10, 8)], hat, shadow=None)
    # sheep flock (left front)
    for k, (x, y) in enumerate(((80, 560), (140, 580), (200, 556), (260, 586), (120, 520))):
        col = (246, 242, 232) if not (k == 2 and "sheep" in d) else (60, 50, 50)
        piece(c, [Ell(x, y - 12, 22, 14), Circ(x + 22, y - 18, 8)], col, border=1, shadow=SMALL)
        flat(c, [Thick(x - 10, y - 2, x - 10, y + 6, 3), Thick(x + 10, y - 2, x + 10, y + 6, 3)], (60, 50, 50))
    # milk pail (centre front)
    pail = (200, 200, 210) if "pail" not in d else (240, 140, 60)
    piece(c, Poly([(440, 590), (500, 590), (506, 540), (434, 540)]), pail, border=1.5, shadow=PROP)
    c.ellipse_ring(470, 540, 30, 18, 2, (90, 90, 100), ymax=540)


L336_ELEMENTS = smoke_el("smk", 200, 236, n=3, col=(240, 240, 240), r=8, rise=(6, -22), length=60) + [
    bird_el("eagle", 450, 80, s=12, speed=12),
    E("tail", lambda c, m: flat(c, Thick(256, 430, 246, 460, 4), (60, 40, 30)), pivot=(256, 430), anim=dict(swingAngle=16, swingSpeed=1.2)),
    cloud_el("cloud", 420, 140, 0.4, 8),
]

L336_DIFFS = [
    ("band", 200, 300, 0),
    ("yurt", 700, 260, 0),
    ("streamer", 580, 226, 0),
    ("horse", 630, 420, 0),
    ("hat", 792, 446, 0),
    ("sheep", 210, 540, 0),
    ("pail", 470, 566, 0),
]


# =================================================================== Level 337 whitewashed cliff village
WHITE = (250, 250, 246)


def wh_house(c, x, base, w, h, dome=None, door=(60, 110, 180)):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 3), WHITE, border=1.5, border_col=(200, 200, 210), shadow=PROP)
    if dome:
        piece(c, Poly([(x + w * 0.4 * math.cos(math.pi * k / 12), base - h - w * 0.36 * math.sin(math.pi * k / 12)) for k in range(13)]), dome, border=1.2, shadow=SMALL)
    flat(c, RRect(x - 8, base - 30, x + 8, base, 3), door)
    flat(c, RRect(x + w * 0.2, base - h + 14, x + w * 0.2 + 14, base - h + 30, 2), door)


def l337_bg(c, d):
    sky(c, (80, 160, 236), (210, 236, 250), H)
    sun_bg(c, 820, 70, 26)
    c.rect(0, 250, W, H, (40, 110, 190))
    for k in range(10):
        flat(c, Thick(20 + k * 90, 290 + (k % 4) * 70, 70 + k * 90, 290 + (k % 4) * 70, 1.6), (120, 190, 240))
    # cliff
    piece(c, Poly([(-20, 600), (-20, 150), (200, 140), (420, 200), (560, 330), (600, 600)]), (170, 120, 100), border=1.5, shadow=LAYER)
    # houses stacked on the cliff
    wh_house(c, 60, 210, 90, 60)
    wh_house(c, 170, 200, 80, 56, dome=(40, 100, 190) if "dome" not in d else (220, 120, 60))
    wh_house(c, 290, 240, 90, 60)
    wh_house(c, 90, 320, 100, 70, door=(60, 110, 180) if "door" not in d else (220, 60, 60))
    wh_house(c, 230, 330, 90, 60)
    wh_house(c, 380, 360, 90, 60, dome=(40, 100, 190))
    wh_house(c, 150, 450, 110, 70)
    wh_house(c, 320, 470, 100, 66)
    # bell tower
    piece(c, [RRect(440, 230, 480, 320, 2), Poly([(436, 232), (484, 232), (460, 200)])], WHITE, border=1.5, border_col=(200, 200, 210), shadow=PROP)
    bell = (220, 180, 70) if "bell" not in d else (120, 120, 140)
    piece(c, Poly([(450, 270), (470, 270), (474, 290), (446, 290)]), bell, border=1, shadow=None)
    # bougainvillea
    bou = (220, 60, 140) if "flowers" not in d else (250, 180, 60)
    flat(c, [Circ(250 + k * 10, 290 - (k % 2) * 8, 9) for k in range(6)], bou)
    # stairway
    for k in range(8):
        flat(c, Thick(420 + k * 12, 400 + k * 22, 470 + k * 12, 400 + k * 22, 4), (230, 226, 216))
    # sailboat + windmill
    sail = WHITE if "sail" not in d else (240, 120, 120)
    piece(c, Poly([(700, 380), (800, 380), (790, 396), (710, 396)]), (60, 60, 70), border=1, shadow=None)
    piece(c, Poly([(750, 376), (750, 300), (796, 376)]), sail, border=1, shadow=None)
    # cafe terrace (right front)
    piece(c, RRect(600, 520, W, 600, 0), (230, 226, 216), shadow=LAYER)
    for x in (680, 820):
        piece(c, [Ell(x, 530, 40, 8), RRect(x - 4, 530, x + 4, 580, 1)], WHITE, border=1.2, shadow=SMALL)
    umb = (40, 100, 190) if "umbrella" not in d else (240, 200, 60)
    flat(c, Thick(750, 590, 750, 470, 3), (200, 200, 210))
    piece(c, Poly([(680, 476), (820, 476), (750, 440)]), umb, border=1.5, shadow=PROP)
    modern(c, 700, 590, (240, 120, 100), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.9, style="long")
    # cat on the steps
    piece(c, [Ell(520, 560, 22, 10), Circ(540, 548, 9)], (240, 160, 70), border=1, shadow=SMALL)


L337_ELEMENTS = [
    bird_el("gull", 600, 120, s=10, speed=-14),
    E("wave", lambda c, m: [flat(c, Thick(x, 470, x + 40, 470, 2), (150, 210, 246)) for x in (640, 820)], daynight="untinted", anim=dict(bobAmplitude=(14, 0), bobSpeed=0.3)),
    E("tail", lambda c, m: flat(c, Thick(500, 560, 486, 544, 3), (240, 160, 70)), pivot=(500, 560), anim=dict(swingAngle=20, swingSpeed=1.2)),
]

L337_DIFFS = [
    ("dome", 170, 134, 0),
    ("door", 90, 300, 0),
    ("flowers", 275, 286, 0),
    ("bell", 460, 280, 0),
    ("sail", 765, 340, 0),
    ("umbrella", 750, 462, 0),
]


# =================================================================== Level 338 geothermal lagoon
def l338_bg(c, d):
    sky(c, (150, 180, 210), (220, 226, 232), H)
    far_ridge(c, 200, 60, (120, 126, 140), 3381)
    far_ridge(c, 240, 30, (90, 96, 106), 3382)
    # lava field
    c.rect(0, 260, W, H, (70, 70, 76))
    rnd = random.Random(3383)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(270, 600)
        flat(c, Ell(x, y, rnd.uniform(10, 26), rnd.uniform(5, 10)), (90, 90, 96))
    # lagoon
    piece(c, Poly([(80, 360), (300, 320), (620, 330), (840, 380), (780, 480), (500, 500), (160, 480)]), (140, 210, 220), border=2, border_col=(220, 230, 230),
          shadow=LAYER)
    # bathers
    for x, y, col, key in ((300, 400, (90, 60, 40), "bather"), (460, 420, (200, 160, 90), None), (620, 400, (40, 30, 30), None)):
        flat(c, Circ(x, y, 12), SKIN)
        piece(c, Ell(x, y - 8, 14, 9), col if not (key and key in d) else (200, 60, 60), shadow=None)
        flat(c, Ell(x, y + 10, 18, 4), (170, 226, 232))
    # face mask on one bather
    ring = (240, 120, 60) if "mask" not in d else (120, 200, 120)
    c.ellipse_ring(460, 428, 28, 10, 8, ring)
    # spa hut (right)
    hut = (60, 64, 72) if "hut" not in d else (150, 100, 70)
    piece(c, [RRect(700, 220, 880, 320, 2), Poly([(690, 224), (890, 224), (790, 180)])], hut, border=1.5, shadow=PROP)
    flat(c, [RRect(720, 250, 860, 290, 2)], (250, 220, 150))
    # wooden deck with towels (front)
    piece(c, RRect(100, 520, 520, 560, 2), (170, 130, 90), border=1.2, shadow=PROP)
    for x in range(110, 520, 30):
        flat(c, Thick(x, 520, x, 560, 1.4), (150, 110, 74))
    for k, x in enumerate((160, 260, 360)):
        col = [(250, 250, 246), (90, 150, 200), (250, 250, 246)][k]
        if k == 1 and "towel" in d:
            col = (240, 180, 60)
        piece(c, RRect(x - 30, 506, x + 30, 524, 4), col, border=1, shadow=SMALL)
    # drinks bar at the water edge (right front)
    bar = (200, 160, 110) if "bar" not in d else (90, 140, 170)
    piece(c, RRect(640, 480, 840, 540, 3), bar, border=1.5, shadow=PROP)
    for x in (680, 730, 780):
        piece(c, Poly([(x - 10, 480), (x + 10, 480), (x + 6, 460), (x - 6, 460)]), (180, 220, 160), border=1, shadow=None)
    # moss on rocks
    for x, y in ((60, 580), (860, 590), (580, 580)):
        rock(c, x, y, 1.4, col=(80, 80, 86))
        flat(c, Ell(x, y - 20, 20, 6), (120, 160, 100))


L338_ELEMENTS = smoke_el("st1", 200, 360, n=3, col=(240, 244, 246), r=18, rise=(6, -30), length=140) + smoke_el("st2", 560, 340, n=3, col=(240, 244, 246), r=20,
                                                                                                                       rise=(-6, -30), length=140) + [
    bird_el("bird", 450, 80, s=10, speed=14),
]

L338_DIFFS = [
    ("hut", 790, 240, 0),
    ("bather", 300, 395, 0),
    ("mask", 462, 420, 0),
    ("towel", 260, 515, 0),
    ("bar", 740, 510, 0),
]


# =================================================================== Level 339 aviary
def parrot(c, x, y, s, body, wing, face=1):
    piece(c, [Ell(x, y, 12 * s, 20 * s), Circ(x + 4 * s * face, y - 22 * s, 10 * s), Poly([(x - 6 * s, y + 16 * s), (x + 6 * s, y + 16 * s), (x, y + 50 * s)])], body,
          border=1, shadow=SMALL)
    flat(c, Ell(x - 4 * s * face, y + 2 * s, 7 * s, 14 * s), wing)
    flat(c, Poly([(x + 12 * s * face, y - 24 * s), (x + 20 * s * face, y - 18 * s), (x + 10 * s * face, y - 16 * s)]), (40, 40, 46))
    flat(c, Circ(x + 6 * s * face, y - 24 * s, 2 * s), (250, 250, 246))


def l339_bg(c, d):
    sky(c, (190, 226, 220), (230, 240, 230), H)
    # net dome lines
    for k in range(-6, 7):
        flat(c, Thick(450 + k * 80, 0, 450 + k * 120, 600, 1), (160, 190, 180))
    for y in range(40, 400, 60):
        flat(c, Thick(0, y, W, y, 1), (160, 190, 180))
    far_round_trees(c, 260, 40, (90, 150, 100), 3391)
    # big tree branch across
    piece(c, [Thick(-20, 200, 520, 160, 14), Thick(300, 176, 380, 120, 8)], (120, 86, 60), shadow=PROP)
    piece(c, [Thick(920, 260, 560, 230, 12)], (120, 86, 60), shadow=PROP)
    for x, y in ((40, 170), (220, 150), (480, 130), (860, 220), (640, 200)):
        piece(c, [Circ(x, y, 30), Circ(x + 26, y + 10, 22)], (80, 150, 80), shadow=SMALL)
    # birds on branches
    parrot(c, 140, 170, 1.4, (220, 50, 50) if "macaw" not in d else (60, 140, 220), (60, 110, 200), face=1)
    parrot(c, 380, 140, 1.1, (60, 180, 90), (250, 200, 60), face=-1)
    # toucan (right branch)
    tou = (250, 170, 40) if "beak" not in d else (90, 200, 120)
    piece(c, [Ell(700, 210, 16, 24), Circ(706, 182, 12)], (40, 40, 46), border=1, shadow=SMALL)
    flat(c, Ell(708, 196, 9, 10), (250, 250, 220))
    piece(c, Poly([(714, 176), (760, 184), (716, 194)]), tou, border=1, shadow=None)
    # hanging feeder (centre)
    flat(c, Thick(560, 0, 560, 260, 1.4), (90, 80, 70))
    feeder = (220, 120, 60) if "feeder" not in d else (90, 150, 200)
    piece(c, [Poly([(530, 262), (590, 262), (560, 240)]), RRect(536, 262, 584, 300, 3), Ell(560, 304, 34, 6)], feeder, border=1.2, shadow=SMALL)
    # ground + path
    c.rect(0, 400, W, H, (140, 180, 110))
    flat(c, Poly([(300, 600), (600, 600), (520, 400), (420, 400)]), (220, 200, 160))
    # pond with a flamingo-free duck
    flat(c, Ell(150, 470, 110, 24), (130, 190, 210))
    duck = (250, 250, 246) if "duck" not in d else (120, 90, 60)
    piece(c, [Ell(160, 466, 18, 9), Circ(174, 454, 7)], duck, border=1, shadow=SMALL)
    # visitors
    hx, hy = modern(c, 460, 590, (240, 200, 70), bottom=(60, 70, 100), hair=(200, 160, 90), h=2.3, style="twin")
    hx, hy = modern(c, 560, 580, (90, 130, 200), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.4)
    cam = (40, 40, 46) if "camera" not in d else (220, 80, 80)
    piece(c, RRect(hx + 6, hy + 14, hx + 34, hy + 32, 3), cam, border=1, shadow=None)
    # info board (right front)
    board = (90, 130, 90) if "board" not in d else (190, 120, 70)
    flat(c, [Thick(760, 600, 760, 470, 4), Thick(860, 600, 860, 470, 4)], (110, 80, 60))
    piece(c, RRect(740, 450, 880, 530, 3), board, border=1.5, shadow=PROP)
    parrot(c, 790, 490, 0.7, (250, 250, 246), (250, 200, 60))
    for k in range(3):
        flat(c, Thick(820, 470 + k * 18, 866, 470 + k * 18, 2), (240, 240, 230))


L339_ELEMENTS = [
    E("flyer", lambda c, m: parrot(c, 300, 300, 0.9, (240, 140, 60), (250, 220, 90)), pivot=(300, 300), anim=dict(orbitRadius=(80, 30), orbitSpeed=0.12)),
    E("feedswing", lambda c, m: flat(c, Circ(560, 310, 3), (200, 160, 80)), pivot=(560, 304), anim=dict(driftVelocity=(0, 40), driftLength=60, driftFade=True)),
    E("leaf", lambda c, m: flat(c, Ell(620, 200, 8, 4), (90, 160, 90)), pivot=(620, 200), anim=dict(swingAngle=10, swingSpeed=0.6)),
]

L339_DIFFS = [
    ("macaw", 140, 175, 0),
    ("beak", 736, 186, 0),
    ("feeder", 560, 275, 0),
    ("duck", 164, 462, 0),
    ("camera", 588, 485, 0),
    ("board", 810, 490, 0),
]


# =================================================================== Level 340 morning market
def veg_crate(c, x, base, veg, kind):
    piece(c, RRect(x - 50, base - 40, x + 50, base, 3), (190, 150, 100), border=1.5, shadow=PROP)
    flat(c, Thick(x - 50, base - 20, x + 50, base - 20, 2), (160, 120, 80))
    for k in range(6):
        vx = x - 36 + (k % 3) * 36
        vy = base - 44 - (k // 3) * 12
        if kind == "round":
            piece(c, Circ(vx, vy, 12), veg, shadow=None)
        elif kind == "long":
            piece(c, Ell(vx, vy, 16, 7), veg, shadow=None)
        else:
            piece(c, [Circ(vx, vy, 12), Circ(vx + 6, vy - 6, 8)], veg, shadow=None)
        flat(c, Thick(vx, vy - 10, vx + 3, vy - 16, 2), (90, 150, 70))


def l340_bg(c, d):
    sky(c, (190, 216, 240), (250, 236, 216), H)
    sun_bg(c, 130, 80, 30, col=(250, 210, 140))
    # town backdrop
    for k, (x0, w, h, col) in enumerate(((0, 160, 200, (230, 200, 170)), (160, 140, 240, (200, 210, 220)), (300, 180, 190, (240, 220, 190)), (480, 150, 230, (210, 190, 200)),
                                        (630, 140, 200, (230, 210, 180)), (770, 140, 240, (200, 220, 210)))):
        piece(c, RRect(x0, 300 - h, x0 + w, 300, 1), col, border=1.5, shadow=PROP)
        for j in range(2):
            for i in range(int(w // 50)):
                flat(c, RRect(x0 + 16 + i * 50, 300 - h + 26 + j * 60, x0 + 36 + i * 50, 300 - h + 56 + j * 60, 2), (120, 140, 170))
    c.rect(0, 300, W, H, (200, 190, 170))
    # stall canopies
    for x0, x1, col, key in ((20, 300, (90, 150, 90), "canopy"), (330, 600, (240, 200, 90), None), (630, 880, (200, 90, 80), None)):
        cc = col if not (key and key in d) else (90, 120, 200)
        piece(c, Poly([(x0, 330), (x1, 330), (x1 - 20, 290), (x0 + 20, 290)]), cc, border=1.5, shadow=PROP)
        flat(c, [Thick(x0 + 10, 330, x0 + 10, 470, 3), Thick(x1 - 10, 330, x1 - 10, 470, 3)], (120, 90, 60))
        piece(c, RRect(x0 - 6, 420, x1 + 6, 470, 2), (240, 236, 226), border=1.2, shadow=PROP)
    veg_crate(c, 90, 420, (220, 60, 50), "round")
    veg_crate(c, 220, 420, (240, 140, 40) if "carrot" not in d else (150, 90, 160), "long")
    veg_crate(c, 410, 420, (120, 180, 70), "leafy")
    veg_crate(c, 530, 420, (150, 90, 160), "round")
    # flower buckets on the right stall
    for k, x in enumerate((680, 760, 840)):
        col = [(240, 90, 120), (250, 210, 60), (250, 250, 246)][k]
        if k == 1 and "flowers" in d:
            col = (120, 120, 230)
        piece(c, Poly([(x - 24, 420), (x + 24, 420), (x + 18, 380), (x - 18, 380)]), (150, 160, 176), border=1.2, shadow=SMALL)
        flat(c, [Circ(x - 12 + (j % 3) * 12, 370 - (j // 3) * 12, 7) for j in range(6)], col)
    # sellers
    modern(c, 160, 380, (250, 250, 246), bottom=(60, 60, 70), hair=(90, 60, 40), h=1.4)
    hx, hy = modern(c, 470, 380, (90, 140, 200), bottom=(60, 60, 70), hair=(200, 200, 200), h=1.4)
    # scale (middle stall)
    sc = (200, 60, 60) if "scale" not in d else (60, 140, 90)
    piece(c, [RRect(440, 400, 500, 420, 3), Ell(470, 396, 26, 6), Circ(470, 380, 12)], sc, border=1, shadow=SMALL)
    # shoppers
    hx, hy = modern(c, 300, 600, (220, 120, 150), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.5, style="long")
    bask = (190, 140, 80) if "basket" not in d else (90, 150, 200)
    piece(c, [Poly([(320, 540), (380, 540), (372, 580), (328, 580)]), Thick(328, 540, 372, 540, 2)], bask, border=1.2, shadow=SMALL)
    flat(c, [Circ(336, 536, 7), Circ(352, 532, 7)], (220, 60, 50))
    modern(c, 640, 600, (90, 160, 110), bottom=(60, 70, 100), hair=(90, 60, 40), h=2.4)
    # dog (right front)
    if "dog" not in d:
        piece(c, [Ell(800, 570, 28, 12), Circ(828, 552, 11), Ell(838, 556, 7, 5)], (200, 140, 80), border=1.2, shadow=SMALL)
        for lx in (-18, -8, 10, 18):
            flat(c, RRect(800 + lx - 3, 576, 800 + lx + 3, 596, 1), (180, 120, 70))
    # crate of bread (left front)
    piece(c, RRect(40, 540, 180, 590, 3), (190, 150, 100), border=1.5, shadow=PROP)
    for k in range(4):
        piece(c, Ell(64 + k * 32, 536, 18, 10), (220, 170, 90), shadow=None)


L340_ELEMENTS = [
    bird_el("pigeon", 400, 120, s=9, speed=14),
    E("sway", lambda c, m: flat(c, Poly([(330, 330), (360, 330), (345, 344)]), (240, 200, 90)), pivot=(345, 330), anim=dict(swingAngle=10, swingSpeed=0.8)),
    E("tail", lambda c, m: flat(c, Thick(774, 566, 760, 550, 3), (200, 140, 80)), pivot=(774, 566), anim=dict(swingAngle=24, swingSpeed=2.4)),
]

L340_DIFFS = [
    ("canopy", 160, 310, 0),
    ("carrot", 220, 384, 0),
    ("scale", 470, 395, 0),
    ("flowers", 760, 364, 0),
    ("basket", 350, 556, 0),
    ("dog", 812, 566, 0),
]


# =================================================================== Level 341 race pit stop
def race_car(c, x, base, col, num_col=(250, 250, 246)):
    piece(c, Poly([(x - 150, base - 20), (x - 140, base - 40), (x - 40, base - 46), (x - 10, base - 70), (x + 40, base - 70), (x + 60, base - 46), (x + 150, base - 40),
                   (x + 160, base - 20)]), col, border=1.5, shadow=PROP)
    piece(c, [RRect(x - 170, base - 74, x - 130, base - 64, 2), RRect(x - 156, base - 64, x - 148, base - 40, 1)], lit(col, 0.8), shadow=SMALL)
    flat(c, Poly([(x - 4, base - 66), (x + 36, base - 66), (x + 48, base - 48), (x - 8, base - 48)]), (40, 50, 70))
    flat(c, Circ(x - 80, base - 34, 14), num_col)
    for wx in (x - 110, x + 110):
        piece(c, Circ(wx, base - 16, 22), (30, 30, 36), shadow=SMALL)
        flat(c, Circ(wx, base - 16, 9), (180, 180, 190))


def l341_bg(c, d):
    c.rect(0, 0, W, 250, (200, 206, 216))
    # grandstand + sponsor-free banners
    for r in range(4):
        flat(c, RRect(0, 30 + r * 40, W, 66 + r * 40, 0), (170, 176, 190) if r % 2 else (180, 186, 200))
    rnd = random.Random(3411)
    for r in range(4):
        for x in range(10, W, 18):
            flat(c, Circ(x + (r % 2) * 9, 44 + r * 40, 5), rnd.choice([(220, 60, 60), (60, 110, 200), (250, 200, 60), (250, 250, 246), (40, 40, 46)]))
    ban = (220, 60, 60) if "banner" not in d else (60, 160, 120)
    piece(c, RRect(300, 196, 600, 236, 3), ban, border=1.5, shadow=PROP)
    sign_box(c, 316, 204, 584, 228, ban, 3412, vertical=False)
    # pit wall
    piece(c, RRect(0, 236, W, 290, 2), (240, 240, 236), border=1.5, shadow=PROP)
    for x in range(0, W, 60):
        flat(c, RRect(x, 270, x + 30, 290, 0), (220, 60, 60))
    # timing screen
    scr = (40, 44, 50)
    piece(c, RRect(700, 140, 860, 200, 3), scr, border=1.5, shadow=PROP)
    tcol = (90, 220, 120) if "screen" not in d else (250, 200, 60)
    for k in range(3):
        flat(c, Thick(716, 156 + k * 14, 840, 156 + k * 14, 4), tcol)
    # pit lane
    c.rect(0, 290, W, H, (90, 92, 100))
    flat(c, Thick(0, 470, W, 470, 3), (250, 250, 246))
    # car
    race_car(c, 450, 460, (40, 110, 200) if "car" not in d else (220, 60, 60))
    # crew
    for x, side in ((300, 1), (600, -1), (450, 0)):
        hx, hy = modern(c, x, 560, (240, 200, 60), bottom=(240, 200, 60), hair=(40, 30, 30), h=2.0)
        piece(c, Circ(hx, hy - 2, 14), (250, 250, 246), shadow=None)
        flat(c, Ell(hx + 4, hy, 9, 5), (60, 70, 100))
    # tyre stacks (left front)
    for k in range(3):
        col = (30, 30, 36)
        piece(c, Ell(100, 580 - k * 24, 42, 14), col, border=1.2, shadow=SMALL)
        flat(c, Thick(60, 580 - k * 24, 140, 580 - k * 24, 3), (250, 200, 60) if not (k == 1 and "tyre" in d) else (220, 60, 60))
    # lollipop sign (right)
    flat(c, Thick(760, 600, 760, 400, 4), (60, 60, 70))
    lol = (220, 60, 60) if "lollipop" not in d else (60, 180, 90)
    piece(c, Circ(760, 386, 34), lol, border=1.5, shadow=PROP)
    flat(c, RRect(744, 380, 776, 392, 2), (250, 250, 246))
    modern(c, 800, 600, (240, 200, 60), bottom=(240, 200, 60), hair=(40, 30, 30), h=2.2)
    # fuel rig / wheel gun (centre front)
    gun = (200, 200, 210) if "gun" not in d else (240, 140, 60)
    piece(c, [RRect(320, 520, 360, 540, 4), Thick(360, 530, 380, 530, 6)], gun, border=1, shadow=SMALL)


L341_ELEMENTS = [
    E("flash", lambda c, m: [flat(c, Circ(x, y, 3), (255, 255, 240)) for x, y in ((120, 60), (480, 100), (820, 50), (300, 140))], daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=2.0)),
    E("spin", lambda c, m: flat(c, Thick(340, 444, 340 + 14, 444, 3), (250, 250, 246)), pivot=(340, 444), anim=dict(rotateSpeed=300)),
    E("heat", lambda c, m: soft_union(c, [Ell(260, 430, 30, 10)], (255, 220, 200), 0.2, spread=10), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=2.0)),
]

L341_DIFFS = [
    ("banner", 450, 216, 0),
    ("screen", 780, 170, 0),
    ("car", 450, 420, 0),
    ("tyre", 100, 556, 0),
    ("lollipop", 760, 386, 0),
    ("gun", 350, 530, 0),
]


# =================================================================== Level 342 horse stable
def l342_bg(c, d):
    c.rect(0, 0, W, 440, (170, 120, 80))
    for x in range(0, W, 30):
        flat(c, Thick(x, 0, x, 440, 2), (156, 108, 72))
    # hay loft (top)
    piece(c, RRect(0, 60, W, 80, 0), (120, 80, 50), shadow=PROP)
    hay = (230, 200, 110) if "hay" not in d else (160, 200, 120)
    for x in range(20, W, 140):
        piece(c, RRect(x, 20, x + 110, 62, 6), hay if 300 <= x < 440 else (230, 200, 110), border=1.2, shadow=SMALL)
    # stalls with half doors
    for k, x0 in enumerate((40, 330, 620)):
        piece(c, RRect(x0, 120, x0 + 240, 440, 2), (110, 70, 44), border=1.5, shadow=PROP)
        flat(c, RRect(x0 + 10, 130, x0 + 230, 300, 2), (60, 40, 30))
        door = (140, 90, 60) if not (k == 2 and "door" in d) else (60, 110, 90)
        piece(c, RRect(x0, 300, x0 + 240, 440, 2), door, border=1.5, shadow=PROP)
        flat(c, [Thick(x0, 300, x0 + 240, 440, 4), Thick(x0 + 240, 300, x0, 440, 4)], lit(door, 0.8))
        plate = (240, 230, 200)
        piece(c, RRect(x0 + 90, 100, x0 + 150, 120, 2), plate, shadow=None)
    # horse heads over the doors
    for x, col, key in ((160, (150, 100, 60), "horse"), (450, (240, 236, 226), None), (740, (60, 50, 50), None)):
        cc = col if not (key and key in d) else (240, 236, 226)
        piece(c, [Thick(x, 300, x + 10, 220, 30), Ell(x + 24, 206, 30, 18)], cc, border=1.2, shadow=SMALL)
        flat(c, [Thick(x - 6, 300, x + 4, 216, 6)], (60, 40, 30) if col != (60, 50, 50) else (30, 24, 20))
        flat(c, Circ(x + 20, 200, 3), INK)
        flat(c, Poly([(x + 2, 196), (x + 8, 180), (x + 14, 196)]), cc)
    # blanket on the middle stall
    bl = (60, 100, 170) if "blanket" not in d else (200, 60, 60)
    piece(c, RRect(360, 300, 450, 360, 3), bl, border=1.2, shadow=SMALL)
    # floor (straw)
    c.rect(0, 440, W, H, (200, 170, 110))
    rnd = random.Random(3421)
    for _ in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(446, 600)
        a = rnd.uniform(0, 3.14)
        flat(c, Thick(x, y, x + 10 * math.cos(a), y + 4 * math.sin(a), 1.4), (230, 200, 130))
    # saddle on a stand (left front)
    flat(c, [Thick(100, 600, 120, 520, 4), Thick(160, 600, 140, 520, 4)], (110, 80, 60))
    sad = (120, 70, 40) if "saddle" not in d else (40, 40, 46)
    piece(c, Poly([(70, 520), (190, 520), (180, 494), (150, 500), (110, 500), (80, 490)]), sad, border=1.2, shadow=PROP)
    # buckets (centre front)
    for k, x in enumerate((400, 470)):
        col = (60, 110, 200) if not (k == 1 and "bucket" in d) else (240, 200, 60)
        piece(c, Poly([(x - 26, 590), (x + 26, 590), (x + 32, 540), (x - 32, 540)]), col, border=1.5, shadow=PROP)
    # stable hand with a pitchfork (right front)
    hx, hy = modern(c, 720, 600, (200, 80, 70), bottom=(60, 90, 150), hair=(90, 60, 40), h=2.4)
    cap = (60, 60, 70) if "cap" not in d else (250, 200, 60)
    piece(c, [Ell(hx, hy - 8, 16, 9), RRect(hx, hy - 9, hx + 20, hy - 4, 2)], cap, shadow=None)
    flat(c, [Thick(760, 600, 790, 470, 3), Thick(782, 476, 800, 456, 2), Thick(790, 474, 806, 460, 2)], (120, 90, 60))
    # cat on a hay bale
    piece(c, RRect(560, 540, 660, 590, 6), (230, 200, 110), border=1.2, shadow=PROP)
    piece(c, [Ell(600, 532, 22, 10), Circ(620, 522, 9)], (240, 240, 236), border=1, shadow=None)


L342_ELEMENTS = [
    E("nod", lambda c, m: flat(c, Ell(474, 210, 10, 6), (220, 216, 206)), pivot=(450, 300), anim=dict(swingAngle=3, swingSpeed=0.5)),
    E("dust", lambda c, m: soft_union(c, [Poly([(600, 0), (660, 0), (500, 440), (400, 440)])], (255, 240, 200), 0.1, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.5)),
    E("swallow", lambda c, m: piece(c, [Thick(300, 100, 310, 104, 3), Thick(310, 104, 320, 100, 3)], (40, 40, 60), shadow=None), pivot=(310, 102),
      anim=dict(orbitRadius=(120, 10), orbitSpeed=0.2)),
]

L342_DIFFS = [
    ("hay", 365, 42, 0),
    ("horse", 175, 240, 0),
    ("blanket", 405, 330, 0),
    ("door", 740, 370, 0),
    ("saddle", 130, 506, 0),
    ("bucket", 470, 565, 0),
    ("cap", 722, 476, 0),
]


# =================================================================== Level 343 bamboo rafting among karst peaks
def karst(c, x, base, w, h, col):
    piece(c, Poly([(x - w / 2, base), (x - w * 0.42, base - h * 0.6), (x - w * 0.3, base - h * 0.9), (x, base - h), (x + w * 0.3, base - h * 0.9), (x + w * 0.42, base - h * 0.6),
                   (x + w / 2, base)]), col, border=1.5, shadow=LAYER)


def l343_bg(c, d):
    sky(c, (190, 216, 226), (236, 240, 236), H)
    for x, w, h, col in ((80, 140, 220, (160, 190, 180)), (230, 120, 260, (150, 184, 170)), (420, 160, 200, (170, 196, 186)), (600, 120, 270, (150, 184, 170)),
                         (780, 160, 230, (160, 190, 180))):
        karst(c, x, 320, w, h, col)
    for x, w, h, col in ((150, 180, 160, (110, 160, 120)), (700, 200, 170, (100, 150, 110))):
        karst(c, x, 340, w, h, col)
    # pagoda on a peak
    pag = (180, 60, 50) if "pagoda" not in d else (60, 110, 160)
    piece(c, RRect(592, 60, 608, 80, 1), (240, 230, 210), shadow=None)
    for k in range(3):
        piece(c, Poly([(578 + k * 4, 62 - k * 14), (622 - k * 4, 62 - k * 14), (612 - k * 4, 54 - k * 14), (588 + k * 4, 54 - k * 14)]), pag, border=1, shadow=None)
    # river
    c.rect(0, 330, W, H, (120, 170, 160))
    for k in range(12):
        flat(c, Thick(20 + k * 80, 360 + (k % 4) * 60, 60 + k * 80, 360 + (k % 4) * 60, 1.6), (170, 210, 200))
    # village on the bank (left)
    for x, roof in ((40, (60, 64, 72)), (120, (60, 64, 72))):
        piece(c, RRect(x - 34, 300, x + 34, 340, 1), (240, 236, 226), border=1.2, shadow=SMALL)
        piece(c, Poly([(x - 42, 302), (x + 42, 302), (x, 280)]), roof, border=1.2, shadow=SMALL)
    # rafts
    for x, y, key in ((300, 420, "raft"), (640, 500, None)):
        col = (200, 190, 120) if not (key and key in d) else (150, 110, 70)
        piece(c, RRect(x - 110, y, x + 110, y + 20, 6), col, border=1.5, shadow=PROP)
        for k in range(10):
            flat(c, Thick(x - 104 + k * 22, y + 2, x - 104 + k * 22, y + 18, 1.6), lit(col, 0.8))
    # boatman with pole on raft 1
    hx, hy = modern(c, 360, 420, (90, 120, 160), bottom=(50, 50, 60), hair=(30, 30, 34), h=1.8)
    hat = (230, 200, 120) if "hat" not in d else (220, 80, 80)
    piece(c, Poly([(hx - 18, hy - 4), (hx + 18, hy - 4), (hx, hy - 18)]), hat, border=1, shadow=None)
    # tourists with parasol on raft 2
    modern(c, 600, 500, (240, 120, 140), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.7, style="long")
    para = (240, 200, 60) if "parasol" not in d else (90, 170, 220)
    flat(c, Thick(640, 500, 640, 420, 2), (120, 90, 60))
    piece(c, Poly([(590, 430), (690, 430), (640, 400)]), para, border=1.2, shadow=SMALL)
    # water buffalo bathing (right)
    buf = (90, 90, 100) if "buffalo" not in d else (170, 120, 80)
    piece(c, [Ell(800, 400, 44, 16), Ell(846, 392, 14, 12)], buf, border=1.2, shadow=SMALL)
    flat(c, [Thick(840, 384, 826, 372, 3), Thick(852, 384, 866, 372, 3)], (220, 210, 190))
    flat(c, Ell(800, 412, 52, 6), (150, 196, 190))
    # cormorant on a bamboo pole (front left)
    flat(c, Thick(100, 600, 140, 480, 4), (150, 170, 90))
    bird = (40, 40, 46) if "cormorant" not in d else (250, 250, 246)
    piece(c, [Ell(136, 470, 12, 18), Circ(142, 448, 7), Poly([(146, 446), (160, 450), (146, 452)])], bird, border=1, shadow=SMALL)


L343_ELEMENTS = [
    cloud_el("mist", 300, 240, 0.6, 5, col=(236, 240, 236)),
    cloud_el("mist2", 700, 200, 0.5, -4, col=(236, 240, 236)),
    E("pole", lambda c, m: flat(c, Thick(380, 330, 410, 460, 2), (150, 170, 90)), pivot=(395, 400), anim=dict(swingAngle=8, swingSpeed=0.6)),
    bird_el("bird", 450, 90, s=9, speed=14),
]

L343_DIFFS = [
    ("pagoda", 600, 50, 0),
    ("raft", 300, 430, 0),
    ("hat", 362, 334, 0),
    ("parasol", 640, 420, 0),
    ("buffalo", 820, 396, 0),
    ("cormorant", 140, 462, 0),
]


# =================================================================== Level 344 aurora town
def town_house(c, x, base, w, h, wall, roof, lit_win=(250, 210, 110)):
    npiece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), wall)
    npiece(c, Poly([(x - w / 2 - 8, base - h + 2), (x + w / 2 + 8, base - h + 2), (x, base - h - w * 0.5)]), roof)
    flat(c, Poly([(x - w / 2 - 6, base - h + 2), (x, base - h - w * 0.5 + 4), (x + w / 2 + 6, base - h + 2), (x, base - h - w * 0.4)]), (236, 240, 250))
    flat(c, [RRect(x - w * 0.3, base - h * 0.7, x - w * 0.1, base - h * 0.45, 2), RRect(x + w * 0.1, base - h * 0.7, x + w * 0.3, base - h * 0.45, 2)], lit_win)


def l344_bg(c, d):
    c.gradient(0, H, (10, 20, 50), (40, 60, 100))
    stars_bg(c, 3441, 120, 300)
    # aurora curtains (static base)
    for k, (col, y0) in enumerate((((90, 230, 160), 120), ((120, 200, 230), 160), ((180, 120, 220), 90))):
        pts = [(x, y0 + 30 * math.sin(x / 90 + k)) for x in range(-20, W + 40, 40)]
        soft_union(c, [Poly(pts + [(W + 20, y0 + 120), (-20, y0 + 120)])], col, 0.25, spread=20)
    if "moon" not in d:
        npiece(c, Circ(800, 70, 26), (250, 244, 220), shadow=None)
        flat(c, Circ(812, 62, 22), (14, 24, 56))
    far_forest(c, 330, 60, (20, 40, 50), 3442)
    c.rect(0, 330, W, H, (210, 220, 240))
    npiece(c, hill_strip(330, [(8, 0.01, 0.6), (4, 0.04, 1.0)]), (220, 228, 246), shadow=LAYER)
    # houses
    town_house(c, 120, 440, 120, 90, (180, 60, 50), (60, 50, 50))
    town_house(c, 300, 430, 100, 80, (60, 110, 160) if "house" not in d else (200, 160, 60), (60, 50, 50))
    town_house(c, 620, 440, 110, 90, (230, 200, 90), (60, 50, 50), lit_win=(250, 210, 110) if "window" not in d else (60, 70, 100))
    town_house(c, 790, 430, 110, 80, (90, 140, 110), (60, 50, 50))
    # church spire (centre back)
    npiece(c, [RRect(440, 300, 480, 420, 2), Poly([(436, 302), (484, 302), (460, 230)])], (240, 236, 226))
    flat(c, RRect(452, 330, 468, 356, 6), (250, 210, 110))
    # street lamp
    flat(c, Thick(520, 470, 520, 380, 3), (40, 40, 50))
    lamp = (250, 210, 110) if "lamp" not in d else (140, 220, 250)
    npiece(c, RRect(508, 364, 532, 384, 3), lamp, shadow=None)
    # sled dog team (front)
    sled = (150, 100, 60) if "sled" not in d else (60, 110, 160)
    npiece(c, [RRect(560, 540, 700, 556, 4), Thick(560, 572, 720, 572, 3), Thick(580, 556, 580, 572, 3), Thick(680, 556, 680, 572, 3), Thick(560, 520, 560, 556, 3)], sled)
    modern(c, 600, 540, (220, 60, 60), bottom=(40, 40, 60), hair=(90, 60, 40), h=1.8)
    for k, x in enumerate((760, 820)):
        col = (220, 226, 236) if not (k == 1 and "dog" in d) else (150, 100, 60)
        npiece(c, [Ell(x, 560, 22, 10), Circ(x + 20, 546, 9), Poly([(x + 16, 540), (x + 18, 528), (x + 24, 540)])], col, shadow=SMALL)
        flat(c, Thick(x + 4, 566, x + 4, 584, 3), lit(col, 0.85))
        flat(c, Thick(x + 16, 566, x + 16, 584, 3), lit(col, 0.85))
    flat(c, Thick(720, 560, 840, 556, 1.4), (60, 50, 50))
    # snowman with lantern (left front)
    npiece(c, [Circ(160, 560, 30), Circ(160, 516, 20)], (246, 248, 252))
    flat(c, [Circ(154, 512, 2), Circ(166, 512, 2)], INK)
    lan = (250, 200, 90) if "lantern" not in d else (240, 100, 120)
    npiece(c, RRect(196, 540, 220, 570, 3), lan, shadow=None)


L344_ELEMENTS = [
    E("aur1", lambda c, m: soft_union(c, [Poly([(x, 130 + 30 * math.sin(x / 70)) for x in range(-20, W + 40, 40)] + [(W + 20, 220), (-20, 220)])], (120, 250, 180), 0.2,
                                      spread=24), daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=0.4, bobAmplitude=(30, 0), bobSpeed=0.1)),
    E("glow", lambda c, m: soft_union(c, [RRect(508, 364, 532, 384, 3), RRect(452, 330, 468, 356, 6)], (255, 210, 120), 0.4, spread=16), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.8)),
    E("snow", lambda c, m: [flat(c, Circ(x, y, 2), (250, 252, 255)) for x, y in ((60, 260), (240, 220), (380, 300), (680, 250), (860, 280), (320, 380))],
      daynight="untinted", anim=dict(driftVelocity=(-6, 36), driftLength=100, driftFade=True)),
] + smoke_el("smk", 140, 360, n=3, col=(120, 130, 150), r=8, rise=(6, -20), length=60)

L344_DIFFS = [
    ("moon", 796, 70, 0),
    ("house", 300, 380, 0),
    ("window", 620, 386, 0),
    ("lamp", 520, 374, 0),
    ("sled", 640, 556, 0),
    ("dog", 830, 552, 0),
    ("lantern", 208, 555, 0),
]


LEVELS = [
    ("Level335", "维京村庄", l335_bg, L335_ELEMENTS, L335_DIFFS, 60, OPTS),
    ("Level336", "草原毡房", l336_bg, L336_ELEMENTS, L336_DIFFS, 60, OPTS),
    ("Level337", "白色崖城", l337_bg, L337_ELEMENTS, L337_DIFFS, 60, OPTS),
    ("Level338", "温泉泻湖", l338_bg, L338_ELEMENTS, L338_DIFFS, 60, OPTS),
    ("Level339", "热带鸟园", l339_bg, L339_ELEMENTS, L339_DIFFS, 60, OPTS),
    ("Level340", "清晨菜市场", l340_bg, L340_ELEMENTS, L340_DIFFS, 60, OPTS),
    ("Level341", "赛车维修站", l341_bg, L341_ELEMENTS, L341_DIFFS, 60, OPTS),
    ("Level342", "马厩", l342_bg, L342_ELEMENTS, L342_DIFFS, 60, OPTS),
    ("Level343", "竹筏漂流", l343_bg, L343_ELEMENTS, L343_DIFFS, 60, OPTS),
    ("Level344", "极光小镇", l344_bg, L344_ELEMENTS, L344_DIFFS, 60, OPTS),
]
