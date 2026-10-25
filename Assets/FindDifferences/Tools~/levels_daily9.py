# -*- coding: utf-8 -*-
"""Everyday-town themes, part 9: more shops (paper-craft, full-bleed, no real brands or logos):
  Level580 蔬果店   - a greengrocer: crates of fruit and veg on tiers, scales, awning, shoppers
  Level581 香料铺   - a spice shop: sacks of coloured spices, jars on shelves, hanging chillies and garlic
  Level582 毛线店   - a yarn shop: wall of yarn balls, knitting armchair, mannequin in a sweater
  Level583 气球店   - a party balloon shop: balloon bunches, helium tank, party supplies
  Level584 五金店   - a hardware store: tool wall, paint cans, ladders, key-cutting counter
  Level585 香水店   - a perfume boutique: glass shelves of bottles, mirror, tester counter
  Level586 家电维修铺 - an electronics repair shop: old TVs and radios, workbench, technician
  Level587 蜡烛店   - a candle shop: shelves of candles with flickering flames, warm light
  Level588 布艺店   - a fabric store: rolls of cloth, cutting table, sewing machine, buttons
  Level589 灯具店   - a lighting store: pendant lamps, chandelier, floor and table lamps, all glowing
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, sky
from fills import far_skyline
from levels_akiba import modern, sign_box
from levels_daily3 import counter, plant, room, wall_shelf
from levels_daily8 import box

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def crate_of(c, x, base, fruit, r=8, w=90, col=(190, 150, 100)):
    piece(c, RRect(x - w / 2, base - 34, x + w / 2, base, 2), col, border=1.2, shadow=PROP)
    flat(c, [Thick(x - w / 2, base - 20, x + w / 2, base - 20, 2)], lit(col, 0.85))
    n = int(w / (r * 2))
    flat(c, [Circ(x - w / 2 + r + 2 + i * r * 2 + (j % 2) * r, base - 36 - j * r * 1.4, r) for j in range(2) for i in range(n - j)], fruit)


def jar(c, x, base, fill, h=46, w=28):
    piece(c, [RRect(x - w / 2, base - h, x + w / 2, base, 6), RRect(x - w / 2 + 3, base - h - 8, x + w / 2 - 3, base - h + 2, 2)], (230, 240, 244), border=1,
          shadow=SMALL)
    flat(c, RRect(x - w / 2 + 3, base - h * 0.7, x + w / 2 - 3, base - 3, 4), fill)


def lamp_glow(eid, x, y, r=14, col=(255, 230, 150), phase=0.0):
    return E(eid, lambda c, m: soft_union(c, [Circ(x, y, r)], col, 0.5, spread=r * 2.2), daynight="untinted", anim=dict(twinkle=0.12, twinkleSpeed=0.8, phase=phase))


# =================================================================== Level 580 greengrocer
def l580_bg(c, d):
    sky(c, (140, 196, 236), (232, 238, 236), 200)
    far_skyline(c, 200, 40, 150, (196, 200, 216), 5801)
    # shop front + awning
    piece(c, RRect(-10, 60, 910, 470, 2), (240, 230, 210), border=1.5, shadow=PROP)
    aw = (60, 140, 90)
    piece(c, Poly([(-10, 60), (910, 60), (910, 120), (-10, 120)]), aw, border=1.5, shadow=PROP)
    for x in range(-10, 910, 50):
        flat(c, Poly([(x, 60), (x + 25, 60), (x + 25, 120), (x, 120)]), (250, 250, 246))
    flat(c, [Circ(x + 12, 120, 12) for x in range(-10, 910, 25)], aw)
    piece(c, RRect(330, 130, 570, 170, 4), (250, 250, 246), border=1.2, shadow=SMALL)
    sign_box(c, 350, 138, 550, 162, (60, 140, 90), 5801, vertical=False)
    flat(c, RRect(330, 200, 570, 470, 3), (90, 70, 60))
    # tiered crates (left + right)
    fruits = [((240, 70, 70), 9), ((250, 160, 40), 9), ((250, 220, 70), 8), ((120, 190, 80), 9), ((160, 80, 160), 7), ((90, 160, 70), 10)]
    for side, x0 in ((0, 70), (1, 640)):
        for r, base in enumerate((280, 360, 440)):
            for k in range(2):
                fr, rad = fruits[(r * 2 + k + side * 3) % len(fruits)]
                if side == 1 and r == 1 and k == 0 and "apples" in d:
                    fr = (120, 200, 90)
                crate_of(c, x0 + k * 110, base, fr, r=rad)
            piece(c, RRect(x0 - 60, base, x0 + 170, base + 10, 2), (170, 130, 90), shadow=SMALL)
    # pavement
    c.rect(0, 470, W, H, (210, 206, 200))
    for y in range(486, H, 26):
        flat(c, Thick(0, y, W, y, 1.2), (200, 196, 190))
    # leafy greens + pumpkins in front
    crate_of(c, 120, 560, (90, 170, 80), r=12, w=110)
    for k, x in enumerate((700, 760, 820)):
        piece(c, [Ell(x, 560, 26, 20)], (240, 140, 50) if not (k == 1 and "pumpkin" in d) else (120, 160, 90), border=1.2, shadow=PROP)
        flat(c, Thick(x, 542, x + 4, 530, 4), (100, 120, 60))
    # scales on a stand + grocer + shoppers
    piece(c, [RRect(430, 470, 470, 560, 3), RRect(410, 450, 490, 470, 3)], (190, 190, 200), border=1.2, shadow=PROP)
    piece(c, Ell(450, 440, 34, 8), (220, 220, 230) if "scale" not in d else (240, 190, 60), border=1, shadow=SMALL)
    modern(c, 450, 420, (250, 250, 250), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.0)
    flat(c, RRect(436, 340, 466, 400, 3), (60, 140, 90) if "apron" not in d else (230, 120, 60))
    modern(c, 300, 600, (90, 150, 220), bottom=(50, 60, 90), hair=(130, 130, 140), h=2.3, bag=(200, 160, 100))
    modern(c, 580, 600, (240, 160, 180), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.2, style="long")
    piece(c, [Poly([(612, 540), (650, 540), (644, 576), (618, 576)])], (200, 70, 70) if "basket" not in d else (90, 140, 200), border=1, shadow=SMALL)
    flat(c, [Circ(622, 536, 7), Circ(638, 534, 7)], (250, 160, 40))


L580_ELEMENTS = [
    E("bee", lambda c, m: (flat(c, Ell(0, 250, 5, 4), (250, 200, 50)), flat(c, [Ell(-2, 245, 4, 3), Ell(3, 245, 4, 3)], (240, 250, 255))),
      anim=dict(driftVelocity=(18, 0), driftStart=60, driftLength=200, bobAmplitude=(0, 16), bobSpeed=0.6)),
    E("sway", lambda c, m: (flat(c, Thick(450, 300, 450, 330, 1.2), (90, 90, 100)), piece(c, Poly([(430, 330), (470, 330), (450, 350)]), (250, 200, 60),
                                                                                         border=1, shadow=SMALL)),
      pivot=(450, 300), anim=dict(swingAngle=6, swingSpeed=0.5)),
    bird_el("pigeon", 300, 30, s=8, speed=-16),
]

L580_DIFFS = [
    ("apron", 451, 370, 0),
    ("apples", 640, 320, 0),
    ("pumpkin", 760, 560, 0),
    ("scale", 450, 440, 0),
    ("basket", 631, 558, 0),
]


# =================================================================== Level 581 spice shop
def sack(c, x, base, spice, col=(210, 180, 130)):
    piece(c, Poly([(x - 34, base), (x + 34, base), (x + 30, base - 50), (x + 36, base - 60), (x - 36, base - 60), (x - 30, base - 50)]), col, border=1.2, shadow=PROP)
    piece(c, Ell(x, base - 58, 32, 10), spice, border=0.6, shadow=None)
    flat(c, Poly([(x - 14, base - 62), (x + 14, base - 62), (x, base - 76)]), spice)


def l581_bg(c, d):
    room(c, (236, 210, 170), (230, 202, 160), (170, 120, 80), (154, 106, 70), floor_y=470)
    # arched alcove shelves with jars
    for k, x0 in enumerate((30, 640)):
        piece(c, Poly([(x0, 420), (x0, 120)] + [(x0 + 115 + 115 * math.cos(math.radians(a)), 120 - 60 * math.sin(math.radians(a))) for a in range(180, -1, -15)]
                      + [(x0 + 230, 420)]), (180, 130, 90), border=1.5, shadow=PROP)
        flat(c, RRect(x0 + 10, 120, x0 + 220, 410, 0), (150, 100, 70))
        for r, y in enumerate((200, 290, 380)):
            flat(c, RRect(x0 + 6, y, x0 + 224, y + 8, 1), (120, 80, 56))
            for i in range(5):
                fill = [(230, 160, 40), (200, 70, 50), (120, 150, 60), (240, 200, 90), (150, 90, 60)][(i + r + k) % 5]
                if k == 1 and r == 1 and i == 2 and "jar" in d:
                    fill = (90, 140, 210)
                jar(c, x0 + 30 + i * 42, y, fill)
    # hanging chillies + garlic
    for k, x in enumerate((330, 400, 500, 570)):
        flat(c, Thick(x, 0, x, 40, 1.4), (120, 100, 80))
        if k % 2 == 0:
            flat(c, [Poly([(x - 6 + (j % 2) * 8, 44 + j * 16), (x + 2 + (j % 2) * 8, 44 + j * 16), (x - 2 + (j % 2) * 8, 64 + j * 16)]) for j in range(6)],
                 (220, 50, 40) if not (k == 2 and "chilli" in d) else (90, 170, 80))
        else:
            flat(c, [Circ(x + (j % 2) * 10 - 5, 52 + j * 18, 9) for j in range(5)], (246, 240, 226))
    # counter with brass scale
    counter(c, 300, 600, 330, 450, (150, 100, 70))
    piece(c, [RRect(440, 270, 460, 330, 2), Thick(390, 270, 510, 270, 3)], (200, 160, 60), shadow=SMALL)
    for x in (390, 510):
        flat(c, Thick(x, 270, x, 300, 1), (200, 160, 60))
        piece(c, Ell(x, 302, 24, 6), (200, 160, 60) if not (x == 510 and "pan" in d) else (150, 150, 160), shadow=SMALL)
    modern(c, 360, 330, (200, 70, 60), bottom=(60, 60, 70), hair=(40, 30, 30), h=1.6)
    # sacks of spices on the floor
    for k, (x, sp) in enumerate(((80, (230, 150, 40)), (170, (200, 60, 40)), (260, (240, 210, 80)), (640, (120, 140, 50)), (730, (160, 90, 50)),
                                 (820, (220, 120, 60)))):
        if k == 4 and "spice" in d:
            sp = (240, 240, 230)
        sack(c, x, 560, sp)
    # customer + rug
    piece(c, Ell(450, 580, 160, 16), (180, 60, 60), shadow=SMALL)
    c.ellipse_ring(450, 580, 140, 12, 3, (230, 190, 70))
    modern(c, 470, 600, (90, 140, 200), bottom=(50, 50, 60), hair=(220, 180, 90), h=2.3, style="long", bag=(200, 160, 100) if "bag" not in d else (90, 170, 110))


L581_ELEMENTS = [
    E("lamp", lambda c, m: (flat(c, Thick(450, 0, 450, 120, 1.4), (120, 100, 80)), piece(c, Poly([(430, 150), (470, 150), (460, 120), (440, 120)]), (200, 150, 60),
                                                                                            border=1, shadow=SMALL),
                            soft_union(c, [Circ(450, 156, 10)], (255, 220, 140), 0.6, spread=24)), pivot=(450, 0), daynight="untinted",
      anim=dict(swingAngle=3, swingSpeed=0.3)),
    E("incense", lambda c, m: soft_union(c, [Circ(560, 300, 4)], (230, 230, 236), 0.7, spread=4), anim=dict(driftVelocity=(4, 20), driftLength=80, driftFade=True,
                                                                                                           driftGrow=2.0)),
    E("cat", lambda c, m: piece(c, [Ell(880, 600, 20, 9), Circ(860, 592, 8), Poly([(854, 588), (856, 578), (860, 586)]), Poly([(862, 586), (866, 578), (868, 590)])],
                                (90, 80, 80), border=1, shadow=SMALL), pivot=(880, 608), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
]

L581_DIFFS = [
    ("jar", 755, 268, 0),
    ("chilli", 504, 90, 0),
    ("pan", 510, 302, 0),
    ("spice", 730, 520, 0),
    ("bag", 447, 534, 0),
]


# =================================================================== Level 582 yarn shop
def yarn(c, x, y, col, r=16):
    piece(c, Circ(x, y, r), col, border=1, shadow=SMALL)
    flat(c, [Thick(x - r * 0.8, y - r * 0.3, x + r * 0.6, y + r * 0.7, 1.4), Thick(x - r * 0.6, y - r * 0.7, x + r * 0.8, y + r * 0.3, 1.4)], lit(col, 0.85))


def l582_bg(c, d):
    room(c, (244, 232, 236), (238, 224, 230), (190, 160, 130), (176, 146, 116), floor_y=480)
    # yarn wall (cubbies)
    piece(c, RRect(20, 40, 520, 420, 3), (210, 180, 140), border=1.5, shadow=PROP)
    pal = [(240, 100, 110), (250, 170, 60), (250, 220, 90), (120, 190, 110), (90, 160, 230), (170, 120, 210), (250, 250, 250), (90, 70, 60)]
    for r in range(5):
        for k in range(6):
            x, y = 34 + k * 80, 52 + r * 72
            flat(c, RRect(x, y, x + 72, y + 64, 3), (180, 150, 110))
            col = pal[(k + r * 3) % len(pal)]
            if r == 2 and k == 4 and "yarn" in d:
                col = (40, 40, 50)
            for j, (dx, dy) in enumerate(((20, 44), (50, 44), (35, 20))):
                yarn(c, x + dx, y + dy, col, r=14)
    # mannequin in a knitted sweater
    flat(c, Thick(650, 480, 650, 380, 4), (90, 90, 100))
    piece(c, Ell(650, 480, 30, 6), (90, 90, 100), shadow=SMALL)
    piece(c, [Poly([(612, 260), (688, 260), (700, 380), (600, 380)]), Ell(650, 240, 22, 26)], (230, 210, 190), border=1.2, shadow=PROP)
    sweater = (200, 80, 90) if "sweater" not in d else (90, 160, 120)
    piece(c, Poly([(608, 270), (692, 270), (720, 330), (702, 336), (696, 380), (604, 380), (598, 336), (580, 330)]), sweater, border=1.2, shadow=PROP)
    for y in range(290, 380, 16):
        flat(c, Thick(606, y, 694, y, 2), lit(sweater, 1.2))
    # armchair knitter + basket
    piece(c, [RRect(740, 400, 880, 540, 18), RRect(726, 450, 760, 550, 10), RRect(860, 450, 894, 550, 10)], (120, 150, 190), border=1.5, shadow=PROP)
    modern(c, 810, 520, (240, 200, 90), bottom=(60, 60, 80), hair=(240, 240, 246), h=2.0, glasses=True)
    flat(c, [Thick(790, 440, 830, 410, 2), Thick(796, 412, 834, 440, 2)], (190, 160, 90))
    piece(c, RRect(796, 430, 830, 450, 3), (240, 140, 170) if "scarf" not in d else (90, 170, 230), border=0.8, shadow=None)
    piece(c, [Poly([(560, 600), (640, 600), (650, 540), (550, 540)])], (200, 160, 100), border=1.2, shadow=PROP)
    for k, col in enumerate(((240, 100, 110), (90, 160, 230), (250, 220, 90))):
        yarn(c, 574 + k * 26, 536, col if not (k == 1 and "ball" in d) else (250, 160, 60), r=13)
    # counter + shop cat
    counter(c, 60, 360, 470, 560, (190, 150, 110))
    piece(c, [RRect(110, 440, 170, 470, 3)], (60, 64, 76), border=1, shadow=SMALL)
    modern(c, 250, 470, (150, 120, 180), bottom=(150, 120, 180), hair=(90, 60, 40), h=1.2, style="long")
    modern(c, 420, 600, (120, 190, 160), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.3)


L582_ELEMENTS = [
    E("kitten", lambda c, m: (piece(c, [Ell(470, 590, 18, 9), Circ(488, 582, 8)], (240, 170, 90), border=1, shadow=SMALL),
                              yarn(c, 520, 592, (90, 160, 230), r=9)), pivot=(500, 598), anim=dict(bobAmplitude=(10, 0), bobSpeed=0.5)),
    E("needles", lambda c, m: flat(c, [Thick(790, 440, 830, 410, 2), Thick(796, 412, 834, 440, 2)], (190, 160, 90)), pivot=(812, 426),
      anim=dict(swingAngle=8, swingSpeed=1.6)),
    E("bell", lambda c, m: (flat(c, Thick(860, 0, 860, 40, 1.2), (120, 100, 80)), piece(c, Poly([(850, 56), (870, 56), (866, 40), (854, 40)]), (220, 180, 70),
                                                                                         shadow=SMALL)), pivot=(860, 0), anim=dict(swingAngle=10, swingSpeed=0.6)),
]

L582_DIFFS = [
    ("yarn", 389, 232, 0),
    ("sweater", 650, 320, 0),
    ("scarf", 813, 440, 0),
    ("ball", 600, 536, 0),
]


# =================================================================== Level 583 party balloon shop
def l583_bg(c, d):
    room(c, (250, 240, 246), (244, 232, 240), (200, 200, 210), (186, 186, 196), floor_y=480)
    # confetti-patterned wall dots
    rnd = random.Random(5831)
    for _ in range(60):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 470), 3), rnd.choice([(250, 200, 220), (200, 230, 250), (250, 240, 180)]))
    # shelves of party supplies (left)
    for r, y in enumerate((150, 250, 350)):
        wall_shelf(c, 20, 300, y)
        for i in range(5):
            x = 44 + i * 54
            col = [(240, 90, 120), (90, 170, 230), (250, 200, 60), (120, 200, 120), (200, 120, 220)][(i + r) % 5]
            if r == 1 and i == 3 and "hat" in d:
                col = (60, 60, 70)
            if r == 0:
                piece(c, Poly([(x - 16, y), (x + 16, y), (x, y - 44)]), col, border=1, shadow=SMALL)              # party hats
                flat(c, Circ(x, y - 44, 4), (250, 250, 250))
            elif r == 1:
                piece(c, Poly([(x - 16, y), (x + 16, y), (x, y - 44)]), col, border=1, shadow=SMALL)
                flat(c, [Thick(x - 10, y - 14, x + 10, y - 14, 3)], (250, 250, 250))
            else:
                piece(c, RRect(x - 20, y - 40, x + 20, y, 3), col, border=1, shadow=SMALL)                          # gift boxes
                flat(c, [Thick(x, y - 40, x, y, 3), Thick(x - 20, y - 20, x + 20, y - 20, 3)], (250, 250, 250))
    # counter with helium tank
    counter(c, 520, 880, 380, 480, (240, 120, 160))
    piece(c, [RRect(560, 250, 610, 380, 20), RRect(576, 230, 594, 254, 3)], (150, 160, 180) if "tank" not in d else (90, 170, 120), border=1.5, shadow=PROP)
    flat(c, Thick(594, 240, 630, 230, 3), (60, 60, 70))
    modern(c, 760, 380, (90, 170, 230), bottom=(60, 60, 70), hair=(220, 180, 90), h=2.0, style="long")
    # big number balloons on the wall
    for k, (x, col) in enumerate(((680, (250, 200, 60)), (760, (240, 120, 160)))):
        if k == 1 and "number" in d:
            col = (120, 200, 230)
        piece(c, [Circ(x, 110, 34), RRect(x - 12, 120, x + 12, 200, 10)], col, border=1.5, shadow=PROP)
        flat(c, Ell(x - 10, 96, 8, 12), lit(col, 1.25))
    # customers + floor balloons
    modern(c, 420, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.6, style="twin")
    modern(c, 340, 600, (200, 110, 150), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.3, style="long")
    for k, (x, y, col) in enumerate(((120, 560, (240, 90, 120)), (180, 576, (90, 170, 230)), (840, 570, (250, 200, 60)))):
        if k == 2 and "floor" in d:
            col = (150, 120, 220)
        piece(c, Ell(x, y, 26, 30), col, border=1.2, shadow=PROP)
        flat(c, Ell(x - 8, y - 12, 6, 10), lit(col, 1.25))


def bunch(eid, x, y, cols, sx, sy, phase=0.0):
    def d(c, m):
        for k, col in enumerate(cols):
            bx, by = x + (k - (len(cols) - 1) / 2) * 30, y - abs(k - (len(cols) - 1) / 2) * 14
            flat(c, Thick(sx, sy, bx, by + 22, 1.2), (90, 90, 100))
            piece(c, [Ell(bx, by, 18, 22), Poly([(bx - 4, by + 23), (bx + 4, by + 23), (bx, by + 18)])], col, border=1, shadow=SMALL)
            flat(c, Ell(bx - 6, by - 8, 4, 7), lit(col, 1.3))
    return E(eid, d, pivot=(sx, sy), anim=dict(swingAngle=5, swingSpeed=0.4, phase=phase))


L583_ELEMENTS = [
    bunch("b1", 420, 120, [(240, 90, 120), (250, 200, 60), (90, 170, 230), (120, 200, 120)], 420, 300),
    bunch("b2", 820, 280, [(200, 120, 220), (250, 250, 250), (240, 140, 60)], 810, 380, phase=0.4),
    E("float", lambda c, m: (flat(c, Thick(420, 520, 424, 470, 1), (90, 90, 100)), piece(c, Ell(424, 456, 14, 17), (240, 90, 120), border=1, shadow=SMALL)),
      pivot=(420, 520), anim=dict(swingAngle=8, swingSpeed=0.5)),
]

L583_DIFFS = [
    ("hat", 206, 220, 0),
    ("tank", 585, 310, 0),
    ("number", 760, 140, 0),
    ("floor", 840, 570, 0),
]


# =================================================================== Level 584 hardware store
def can(c, x, base, col, w=36, h=44):
    piece(c, [RRect(x - w / 2, base - h, x + w / 2, base, 3)], (190, 190, 200), border=1, shadow=SMALL)
    flat(c, RRect(x - w / 2, base - h * 0.75, x + w / 2, base - h * 0.25, 1), col)


def l584_bg(c, d):
    room(c, (220, 214, 200), (212, 206, 192), (160, 156, 150), (146, 142, 136), floor_y=480)
    # tool wall (pegboard)
    piece(c, RRect(20, 40, 460, 280, 3), (200, 160, 110), border=1.5, shadow=PROP)
    for x in range(30, 460, 16):
        for y in range(50, 276, 16):
            flat(c, Circ(x, y, 1.4), (176, 136, 90))
    tools = [("hammer", 60), ("saw", 130), ("wrench", 210), ("pliers", 270), ("screwdriver", 330), ("level", 400)]
    for k, (kind, x) in enumerate(tools):
        col = [(220, 70, 60), (60, 110, 200), (250, 190, 60), (90, 160, 110), (220, 70, 60), (250, 190, 60)][k]
        if kind == "wrench" and "tool" in d:
            col = (150, 90, 200)
        if kind == "hammer":
            flat(c, [Thick(x, 100, x, 220, 6), RRect(x - 22, 90, x + 22, 108, 3)], col)
        elif kind == "saw":
            flat(c, [Poly([(x - 10, 90), (x + 26, 90), (x + 30, 220), (x - 6, 220)]), RRect(x - 18, 80, x + 10, 110, 6)], col)
        elif kind == "wrench":
            flat(c, [Thick(x, 100, x, 220, 7), Circ(x, 96, 13), Circ(x, 224, 11)], col)
        elif kind == "pliers":
            flat(c, [Thick(x - 6, 100, x + 6, 220, 5), Thick(x + 6, 100, x - 6, 220, 5)], col)
        elif kind == "screwdriver":
            flat(c, [RRect(x - 7, 90, x + 7, 150, 5), Thick(x, 150, x, 230, 3)], col)
        else:
            flat(c, [RRect(x - 40, 140, x + 40, 160, 3), Circ(x, 150, 5)], col)
    # paint can shelves (right)
    for r, y in enumerate((150, 250, 350)):
        wall_shelf(c, 540, 890, y)
        for i in range(7):
            col = [(220, 70, 60), (250, 200, 60), (90, 160, 220), (120, 190, 110), (250, 250, 250), (150, 120, 200), (240, 140, 60)][(i + r * 2) % 7]
            if r == 0 and i == 5 and "paint" in d:
                col = (40, 40, 50)
            can(c, 566 + i * 48, y, col)
    # ladders leaning
    for k, x in enumerate((480, 515)):
        col = (200, 200, 210) if not (k == 1 and "ladder" in d) else (240, 180, 60)
        flat(c, [Thick(x, 470, x + 20, 250, 4), Thick(x + 30, 470, x + 50, 250, 4)] + [Thick(x + 4 + j * 2, 450 - j * 28, x + 34 + j * 2, 450 - j * 28, 3) for j in range(8)],
             col)
    # key cutting counter + clerk + customer
    counter(c, 40, 380, 380, 480, (200, 70, 60))
    piece(c, [RRect(80, 340, 160, 380, 4)], (90, 96, 110), border=1, shadow=SMALL)
    flat(c, [Circ(100, 350, 6), Circ(140, 350, 6)], (200, 200, 210))
    modern(c, 260, 380, (60, 120, 180), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.0, glasses=True)
    flat(c, RRect(246, 300, 276, 360, 3), (200, 70, 60))
    modern(c, 600, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(40, 30, 30), h=2.3)
    # boxes + bucket of brooms + wheelbarrow
    box(c, 760, 600, 80, 56)
    box(c, 840, 600, 70, 70, col=(200, 160, 110) if "box" not in d else (120, 170, 220))
    piece(c, Poly([(420, 600), (470, 600), (476, 560), (414, 560)]), (90, 150, 210), border=1.2, shadow=PROP)
    flat(c, [Thick(430 + k * 10, 560, 426 + k * 12, 500, 3) for k in range(4)], (190, 150, 90))


L584_ELEMENTS = [
    E("sign", lambda c, m: (flat(c, [Thick(640, 0, 640, 40, 1.2), Thick(780, 0, 780, 40, 1.2)], (100, 100, 110)),
                            piece(c, RRect(620, 40, 800, 80, 4), (250, 200, 60), border=1.2, shadow=SMALL),
                            sign_box(c, 640, 48, 780, 72, (60, 60, 70), 5841, vertical=False)), pivot=(710, 0), anim=dict(swingAngle=2, swingSpeed=0.4)),
    E("key", lambda c, m: (c.ellipse_ring(140, 330, 6, 6, 2, (230, 200, 90)), flat(c, Thick(146, 330, 166, 330, 3), (230, 200, 90))), pivot=(140, 324),
      anim=dict(swingAngle=14, swingSpeed=1.0)),
    E("sparks", lambda c, m: [flat(c, Thick(120, 336, 120 + 10 * math.cos(a), 336 - 10 * math.sin(a), 1.4), (255, 220, 120)) for a in (0.4, 1.2, 2.0, 2.8)],
      daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=3.0)),
]

L584_DIFFS = [
    ("tool", 210, 160, 0),
    ("paint", 806, 128, 0),
    ("ladder", 540, 360, 0),
    ("box", 840, 565, 0),
]


# =================================================================== Level 585 perfume boutique
def bottle(c, x, base, liquid, shape=0, s=1.0):
    if shape == 0:
        piece(c, [RRect(x - 12 * s, base - 34 * s, x + 12 * s, base, 6 * s), RRect(x - 4 * s, base - 42 * s, x + 4 * s, base - 32 * s, 1)], (236, 244, 250), border=1, shadow=SMALL)
    elif shape == 1:
        piece(c, [Ell(x, base - 16 * s, 16 * s, 16 * s), RRect(x - 4 * s, base - 40 * s, x + 4 * s, base - 28 * s, 1)], (236, 244, 250), border=1, shadow=SMALL)
    else:
        piece(c, [Poly([(x - 14 * s, base), (x + 14 * s, base), (x + 6 * s, base - 36 * s), (x - 6 * s, base - 36 * s)]),
                  RRect(x - 4 * s, base - 44 * s, x + 4 * s, base - 34 * s, 1)], (236, 244, 250), border=1, shadow=SMALL)
    flat(c, Ell(x, base - 12 * s, 9 * s, 9 * s) if shape == 1 else RRect(x - 8 * s, base - 24 * s, x + 8 * s, base - 4 * s, 3), liquid)
    flat(c, RRect(x - 5 * s, base - 50 * s, x + 5 * s, base - 42 * s, 2), (200, 170, 80))


def l585_bg(c, d):
    room(c, (240, 230, 232), (234, 222, 226), (230, 226, 222), (216, 212, 208), floor_y=480)
    # glass shelves (left + right walls)
    pal = [(250, 180, 200), (200, 170, 240), (250, 220, 140), (170, 220, 240), (240, 140, 120), (180, 230, 190)]
    for k, x0 in enumerate((30, 620)):
        piece(c, RRect(x0, 40, x0 + 250, 420, 4), (250, 248, 246), border=1.5, shadow=PROP)
        for r, y in enumerate((140, 240, 340)):
            flat(c, RRect(x0 + 8, y, x0 + 242, y + 6, 1), (210, 228, 236))
            for i in range(5):
                liq = pal[(i + r + k * 2) % len(pal)]
                if k == 0 and r == 2 and i == 1 and "bottle" in d:
                    liq = (60, 60, 80)
                bottle(c, x0 + 32 + i * 46, y, liq, shape=(i + r) % 3, s=1.4 if (k == 0 and r == 2 and i == 1) else 1.0)
    # mirror + logo arch (centre)
    piece(c, Poly([(350, 360), (350, 140)] + [(450 + 100 * math.cos(math.radians(a)), 140 - 90 * math.sin(math.radians(a))) for a in range(180, -1, -12)]
                  + [(550, 360)]), (200, 170, 90), border=1.5, shadow=PROP)
    flat(c, Poly([(362, 352), (362, 144)] + [(450 + 88 * math.cos(math.radians(a)), 144 - 80 * math.sin(math.radians(a))) for a in range(180, -1, -12)]
                 + [(538, 352)]), (214, 230, 238))
    flat(c, Poly([(390, 120), (420, 110), (380, 260), (366, 240)]), (240, 248, 252))
    # tester counter with a big display bottle + flowers
    counter(c, 300, 600, 400, 480, (250, 250, 250), top=(220, 200, 150))
    bottle(c, 450, 400, (250, 160, 190) if "display" not in d else (120, 200, 230), shape=1, s=2.2)
    piece(c, [RRect(360, 370, 390, 400, 4)], (250, 250, 250), border=1, shadow=SMALL)
    flat(c, [Circ(368, 362, 7), Circ(382, 360, 7)], (250, 140, 170))
    for k in range(3):
        piece(c, RRect(500 + k * 26, 384, 518 + k * 26, 400, 2), (250, 248, 240), border=0.6, shadow=None)
    # assistant + shoppers + chandelier stand-in (rug)
    modern(c, 220, 600, (40, 40, 50), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.4, style="long")
    modern(c, 700, 600, (240, 200, 210) if "coat" not in d else (120, 160, 210), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.4, style="long", bag=(200, 80, 90))
    piece(c, Ell(450, 560, 180, 20), (230, 200, 210), shadow=SMALL)
    piece(c, [Ell(880, 560, 22, 14), RRect(866, 470, 894, 560, 6)], (250, 250, 250), border=1.2, shadow=PROP)
    flat(c, [Circ(872, 460, 10), Circ(888, 456, 10), Circ(880, 444, 10)], (250, 180, 200) if "vase" not in d else (250, 220, 90))


L585_ELEMENTS = [
    E("mist", lambda c, m: [soft_union(c, [Circ(520 + k * 14, 360 - k * 10, 4)], (250, 240, 250), 0.6, spread=6) for k in range(3)],
      anim=dict(driftVelocity=(10, 10), driftLength=30, driftFade=True)),
    E("glint", lambda c, m: flat(c, Poly(star_pts(420, 200, 12, 3, points=4)), (255, 255, 255)), daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=0.5)),
    E("chand", lambda c, m: (flat(c, Thick(450, 0, 450, 30, 1.4), (200, 170, 90)), flat(c, Thick(410, 30, 490, 30, 3), (200, 170, 90)),
                             [flat(c, Ell(x, 44, 5, 10), (250, 240, 250)) for x in range(410, 491, 20)]), pivot=(450, 0), anim=dict(swingAngle=2, swingSpeed=0.3)),
]

L585_DIFFS = [
    ("bottle", 108, 324, 0),
    ("display", 450, 370, 0),
    ("coat", 701, 522, 0),
    ("vase", 880, 456, 0),
]


# =================================================================== Level 586 electronics repair shop
def crt_tv(c, x, base, w, h, screen, body=(150, 110, 80)):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 6), body, border=1.5, shadow=PROP)
    flat(c, RRect(x - w / 2 + 10, base - h + 10, x + w / 2 - 34, base - 10, 10), screen)
    flat(c, [Circ(x + w / 2 - 20, base - h + 26, 6), Circ(x + w / 2 - 20, base - h + 48, 6)], lit(body, 0.7))


def l586_bg(c, d):
    room(c, (200, 206, 196), (194, 200, 190), (150, 140, 130), (136, 126, 116), floor_y=480)
    # shelves stacked with TVs and radios
    for r, y in enumerate((170, 300)):
        wall_shelf(c, 20, 520, y)
        for k in range(4):
            x = 80 + k * 120
            if r == 0:
                crt_tv(c, x, y, 100, 80, [(60, 60, 70), (120, 200, 220), (60, 60, 70), (200, 220, 160)][k] if not (k == 2 and "screen" in d) else (240, 180, 90))
            else:
                piece(c, RRect(x - 46, y - 56, x + 46, y, 8), [(200, 70, 60), (90, 150, 200), (220, 190, 120), (90, 160, 110)][k], border=1.2, shadow=PROP)
                flat(c, [RRect(x - 38, y - 46, x + 6, y - 10, 4)], (230, 220, 200))
                flat(c, [Circ(x + 24, y - 30, 12)], (60, 60, 70))
                flat(c, [Thick(x - 34 + j * 8, y - 46, x - 34 + j * 8, y - 10, 1) for j in range(5)], (190, 180, 160))
    # clock + certificate
    piece(c, Circ(640, 90, 32), (250, 250, 252), border=1.5, shadow=PROP)
    c.ellipse_ring(640, 90, 32, 32, 3, (60, 60, 70))
    flat(c, [Thick(640, 90, 640, 66, 2.4), Thick(640, 90, 660, 98, 2.4)], (40, 40, 50))
    piece(c, RRect(720, 50, 860, 140, 3), (190, 150, 80) if "frame" not in d else (60, 60, 70), border=1.5, shadow=PROP)
    flat(c, RRect(730, 60, 850, 130, 2), (250, 246, 230))
    sign_box(c, 744, 74, 836, 112, (120, 100, 80), 5861, vertical=False)
    # workbench + technician + lamp
    counter(c, 560, 900, 360, 480, (120, 90, 70))
    modern(c, 740, 360, (90, 150, 200), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.9, glasses=True)
    crt_tv(c, 640, 360, 110, 90, (60, 60, 70), body=(220, 200, 160))
    flat(c, RRect(626, 290, 660, 300, 2), (90, 180, 110))
    piece(c, [Thick(860, 360, 840, 290, 3), Thick(840, 290, 800, 280, 3), Poly([(790, 270), (820, 270), (812, 292), (798, 292)])],
          (60, 60, 70) if "lamp" not in d else (220, 80, 80), border=1, shadow=SMALL)
    flat(c, [Thick(780, 360, 800, 344, 3), Thick(810, 360, 830, 350, 2)], (150, 150, 160))
    # boxes of parts + customer with a radio
    box(c, 90, 600, 90, 60)
    box(c, 180, 600, 70, 46, col=(200, 160, 110) if "box" not in d else (90, 170, 120))
    modern(c, 380, 600, (240, 160, 90), bottom=(60, 70, 110), hair=(130, 130, 140), h=2.3)
    piece(c, RRect(396, 506, 450, 540, 6), (90, 150, 200), border=1, shadow=SMALL)
    flat(c, [Circ(430, 523, 8)], (60, 60, 70))


L586_ELEMENTS = [
    E("static", lambda c, m: [flat(c, Thick(46 + j * 8, 104 + (j * 13) % 40, 54 + j * 8, 104 + (j * 13) % 40, 2), (230, 230, 230)) for j in range(6)],
      daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=4.0)),
    E("solder", lambda c, m: soft_union(c, [Circ(800, 346, 4)], (230, 230, 236), 0.7, spread=4), anim=dict(driftVelocity=(2, 16), driftLength=40, driftFade=True)),
    E("needle", lambda c, m: flat(c, Thick(430, 530, 432, 516, 2), (220, 60, 60)), pivot=(430, 530), anim=dict(swingAngle=30, swingSpeed=0.6)),
]

L586_DIFFS = [
    ("screen", 320, 125, 0),
    ("frame", 790, 95, 0),
    ("lamp", 805, 281, 0),
    ("box", 180, 577, 0),
]


# =================================================================== Level 587 candle shop
def candle(c, x, base, col, w=20, h=50):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 4), col, border=1, shadow=SMALL)
    flat(c, Ell(x, base - h, w / 2, 3), lit(col, 0.9))
    flat(c, Thick(x, base - h, x, base - h - 6, 1.4), (60, 50, 50))


def l587_bg(c, d):
    room(c, (90, 60, 60), (98, 66, 66), (110, 80, 60), (100, 72, 54), floor_y=480)
    # shelves with candles of many sizes
    pal = [(250, 240, 220), (240, 160, 170), (200, 180, 240), (250, 210, 120), (170, 220, 200), (220, 100, 90)]
    rnd = random.Random(5871)
    for r, y in enumerate((150, 260, 370)):
        wall_shelf(c, 20, 880, y, col=(150, 100, 70))
        x = 40
        i = 0
        while x < 860:
            w = rnd.choice((16, 20, 26))
            h = rnd.choice((30, 44, 60))
            col = pal[(i + r) % len(pal)]
            if r == 1 and i == 9 and "candle" in d:
                col = (60, 60, 80)
            candle(c, x + w / 2, y, col, w=w, h=h)
            x += w + 18
            i += 1
    # table with a large pillar candle display
    piece(c, [Ell(450, 470, 150, 20), RRect(440, 470, 460, 560, 3), Ell(450, 560, 50, 8)], (150, 100, 70), border=1.5, shadow=PROP)
    for k, (x, h, col) in enumerate(((380, 70, (250, 240, 220)), (450, 100, (240, 160, 170)), (520, 60, (200, 180, 240)))):
        if k == 1 and "pillar" in d:
            col = (120, 200, 160)
        candle(c, x, 466, col, w=40, h=h)
    # lanterns on the floor + customer + shop owner
    for k, x in enumerate((90, 820)):
        piece(c, [RRect(x - 22, 520, x + 22, 590, 4), Poly([(x - 26, 522), (x + 26, 522), (x, 500)])], (60, 60, 70) if not (k == 1 and "lantern" in d) else (190, 150, 70),
              border=1, shadow=PROP)
        flat(c, RRect(x - 14, 530, x + 14, 582, 2), (250, 210, 140))
    modern(c, 250, 600, (150, 120, 180), bottom=(50, 50, 60), hair=(220, 180, 90), h=2.3, style="long", bag=(200, 160, 100))
    modern(c, 680, 600, (240, 200, 150) if "shirt" not in d else (120, 170, 220), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.3)


def flames(c, m):
    rnd = random.Random(5871)
    pos = []
    for r, y in enumerate((150, 260, 370)):
        x = 40
        while x < 860:
            w = rnd.choice((16, 20, 26))
            h = rnd.choice((30, 44, 60))
            pos.append((x + w / 2, y - h - 6))
            x += w + 18
    for k, (x, y) in enumerate(pos):
        if k % 2 == 0:
            flat(c, Poly([(x - 3, y), (x + 3, y), (x, y - 10)]), (255, 190, 80))
    for x, h in ((380, 70), (450, 100), (520, 60)):
        flat(c, Poly([(x - 5, 466 - h - 6), (x + 5, 466 - h - 6), (x, 466 - h - 22)]), (255, 190, 80))


L587_ELEMENTS = [
    E("flames", flames, daynight="untinted", anim=dict(stretch=(0.04, 0.2), scaleSpeed=3.0, twinkle=0.15, twinkleSpeed=2.5)),
    E("warm", lambda c, m: soft_union(c, [Ell(450, 370, 140, 60)], (255, 200, 120), 0.18, spread=40), daynight="untinted", anim=dict(pulse=0.04, scaleSpeed=0.5)),
    E("lglow", lambda c, m: [soft_union(c, [Circ(x, 556, 10)], (255, 200, 120), 0.5, spread=24) for x in (90, 820)], daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=1.5)),
]

L587_DIFFS = [
    ("candle", 440, 220, 0),
    ("pillar", 450, 416, 0),
    ("lantern", 820, 545, 0),
    ("shirt", 681, 544, 0),
]


# =================================================================== Level 588 fabric store
def bolt(c, x, base, col, h=150, w=26):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 6), col, border=1, shadow=SMALL)
    flat(c, Ell(x, base - h, w / 2, 4), lit(col, 0.85))


def l588_bg(c, d):
    room(c, (236, 230, 220), (230, 222, 210), (180, 150, 120), (166, 136, 106), floor_y=480)
    # rolls of fabric standing in racks (left wall)
    pal = [(220, 70, 70), (250, 200, 80), (90, 150, 220), (120, 190, 120), (240, 160, 190), (150, 110, 190), (250, 250, 246), (60, 60, 80)]
    piece(c, RRect(20, 240, 420, 470, 2), (190, 150, 110), border=1.5, shadow=PROP)
    for k in range(13):
        col = pal[k % len(pal)]
        if k == 5 and "roll" in d:
            col = (250, 150, 60)
        bolt(c, 40 + k * 29, 460, col, h=170 + (k % 3) * 20)
    # stripes / patterns on a few rolls
    for k in (2, 7, 10):
        flat(c, [Thick(40 + k * 29 - 13, 460 - j * 30, 40 + k * 29 + 13, 460 - j * 30, 3) for j in range(1, 5)], (250, 250, 250))
    # shelves of folded fabric (right wall)
    for r, y in enumerate((150, 250, 350)):
        wall_shelf(c, 500, 880, y)
        for i in range(6):
            col = pal[(i + r * 3) % len(pal)]
            if r == 2 and i == 4 and "stack" in d:
                col = (40, 40, 50)
            for j in range(3):
                piece(c, RRect(514 + i * 60, y - 14 - j * 14, 562 + i * 60, y - j * 14, 2), lit(col, 1 - j * 0.06), border=0.6, shadow=None)
    # cutting table with sewing machine + scissors + tape
    counter(c, 340, 760, 470, 560, (150, 110, 80))
    piece(c, [RRect(380, 400, 480, 470, 6), RRect(380, 400, 400, 470, 4), RRect(380, 400, 480, 420, 6)], (60, 60, 70) if "machine" not in d else (220, 80, 90),
          border=1.2, shadow=PROP)
    flat(c, Circ(470, 430, 8), (200, 200, 210))
    piece(c, RRect(520, 450, 700, 470, 2), (200, 120, 160), border=0.8, shadow=None)
    flat(c, [Thick(600, 456, 640, 440, 3), Thick(600, 440, 640, 456, 3)], (150, 150, 160))
    flat(c, [Circ(600, 456, 5), Circ(600, 440, 5)], (220, 60, 60))
    # button jars on the counter
    piece(c, RRect(700, 420, 740, 470, 6), (230, 240, 244), border=1, shadow=SMALL)
    flat(c, [Circ(708 + (j % 3) * 10, 456 - (j // 3) * 10, 4) for j in range(9)], (250, 200, 60))
    # mannequin + shoppers
    piece(c, [Poly([(110, 120), (170, 120), (180, 220), (100, 220)]), Ell(140, 104, 18, 20)], (230, 210, 190), border=1.2, shadow=PROP)
    piece(c, Poly([(104, 130), (176, 130), (200, 236), (80, 236)]), (90, 160, 200) if "dress" not in d else (240, 140, 170), border=1.2, shadow=PROP)
    flat(c, Thick(140, 236, 140, 240, 4), (90, 90, 100))
    modern(c, 250, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.4, style="long")
    modern(c, 840, 600, (120, 170, 140), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.4, glasses=True)


L588_ELEMENTS = [
    E("needle", lambda c, m: flat(c, Thick(440, 470, 440, 482, 2), (200, 200, 210)), pivot=(440, 470), anim=dict(bobAmplitude=(0, 4), bobSpeed=3.0)),
    E("ribbon", lambda c, m: (flat(c, Thick(600, 0, 600, 40, 1.2), (100, 100, 110)), piece(c, Poly([(590, 40), (610, 40), (612, 110), (600, 100), (588, 110)]),
                                                                                         (240, 90, 120), border=1, shadow=SMALL)), pivot=(600, 0),
      anim=dict(swingAngle=6, swingSpeed=0.4)),
    E("cat", lambda c, m: piece(c, [Ell(70, 590, 22, 10), Circ(92, 580, 9), Poly([(86, 576), (88, 564), (92, 574)]), Poly([(94, 574), (98, 564), (100, 578)])],
                                (250, 250, 250), border=1, shadow=SMALL), pivot=(70, 600), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
]

L588_DIFFS = [
    ("roll", 185, 340, 0),
    ("stack", 784, 330, 0),
    ("machine", 430, 436, 0),
    ("dress", 140, 190, 0),
]


# =================================================================== Level 589 lighting store
def l589_bg(c, d):
    room(c, (60, 60, 76), (66, 66, 84), (120, 110, 100), (108, 98, 90), floor_y=480)
    # floor lamps + table lamps on plinths
    for k, (x, shade) in enumerate(((80, (250, 240, 220)), (220, (240, 200, 160)), (680, (250, 230, 200)), (830, (230, 220, 250)))):
        if k == 2 and "shade" in d:
            shade = (120, 200, 160)
        flat(c, Thick(x, 600, x, 380, 4), (200, 170, 90))
        piece(c, Ell(x, 600, 30, 6), (200, 170, 90), shadow=SMALL)
        piece(c, Poly([(x - 40, 380), (x + 40, 380), (x + 26, 330), (x - 26, 330)]), shade, border=1, border_col=(110, 110, 130), shadow=SMALL)
    for k, x in enumerate((380, 520)):
        piece(c, RRect(x - 50, 500, x + 50, 600, 3), (220, 220, 226) if not (k == 0 and "plinth" in d) else (230, 200, 120), border=1.2,
              border_col=(110, 110, 130), shadow=PROP)
        piece(c, [Ell(x, 490, 22, 12), RRect(x - 4, 450, x + 4, 490, 2)], (60, 110, 180) if not (k == 1 and "base" in d) else (220, 120, 60), border=1,
              border_col=(110, 110, 130), shadow=SMALL)
        piece(c, Poly([(x - 30, 450), (x + 30, 450), (x + 20, 416), (x - 20, 416)]), (250, 240, 220), border=1, border_col=(110, 110, 130), shadow=SMALL)
    # wall sconces
    for k, x in enumerate((140, 760)):
        piece(c, [RRect(x - 6, 200, x + 6, 250, 2), Poly([(x - 24, 200), (x + 24, 200), (x + 16, 170), (x - 16, 170)])], (200, 170, 90) if not (k == 1 and "sconce" in d)
              else (150, 150, 170), border=1, border_col=(110, 110, 130), shadow=SMALL)
    # price tags + counter
    counter(c, 300, 600, 300, 380, (40, 40, 50), top=(90, 90, 100))
    modern(c, 450, 300, (200, 60, 70), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.6, style="long")
    modern(c, 620, 600, (90, 150, 200) if "coat" not in d else (230, 120, 150), bottom=(40, 40, 50), hair=(220, 180, 90), h=2.4)


def pendant(eid, x, y, shade, phase):
    def d(c, m):
        flat(c, Thick(x, 0, x, y, 1.4), (150, 150, 160))
        piece(c, Poly([(x - 30, y + 30), (x + 30, y + 30), (x + 14, y), (x - 14, y)]), shade, border=1, border_col=(110, 110, 130), shadow=SMALL)
        flat(c, Ell(x, y + 32, 10, 4), (255, 240, 180))
    return E(eid, d, pivot=(x, 0), anim=dict(swingAngle=3, swingSpeed=0.3, phase=phase))


L589_ELEMENTS = [
    pendant("p1", 260, 80, (240, 120, 80), 0.0), pendant("p2", 640, 90, (90, 160, 140), 0.4),
    E("chand", lambda c, m: (flat(c, Thick(450, 0, 450, 60, 2), (200, 170, 90)), c.ellipse_ring(450, 90, 70, 18, 4, (200, 170, 90)),
                             [flat(c, Ell(450 + 70 * math.cos(a), 90 + 18 * math.sin(a) - 10, 5, 10), (255, 240, 190)) for a in [k * math.pi / 4 for k in range(8)]]),
      pivot=(450, 0), anim=dict(swingAngle=1.5, swingSpeed=0.25)),
] + [lamp_glow("g%d" % i, x, y, r, phase=i / 9) for i, (x, y, r) in enumerate(((80, 360, 22), (220, 360, 22), (680, 360, 22), (830, 360, 22), (380, 436, 16),
                                                                           (520, 436, 16), (140, 190, 14), (760, 190, 14), (450, 90, 30)))]

L589_DIFFS = [
    ("shade", 680, 356, 0),
    ("base", 520, 480, 0),
    ("sconce", 760, 200, 0),
    ("plinth", 380, 550, 0),
    ("coat", 621, 535, 0),
]


LEVELS = [
    ("Level580", "蔬果店", l580_bg, L580_ELEMENTS, L580_DIFFS, 60, OPTS),
    ("Level581", "香料铺", l581_bg, L581_ELEMENTS, L581_DIFFS, 60, OPTS),
    ("Level582", "毛线店", l582_bg, L582_ELEMENTS, L582_DIFFS, 60, OPTS),
    ("Level583", "气球店", l583_bg, L583_ELEMENTS, L583_DIFFS, 60, OPTS),
    ("Level584", "五金店", l584_bg, L584_ELEMENTS, L584_DIFFS, 60, OPTS),
    ("Level585", "香水店", l585_bg, L585_ELEMENTS, L585_DIFFS, 60, OPTS),
    ("Level586", "家电维修铺", l586_bg, L586_ELEMENTS, L586_DIFFS, 60, OPTS),
    ("Level587", "蜡烛店", l587_bg, L587_ELEMENTS, L587_DIFFS, 60, OPTS),
    ("Level588", "布艺店", l588_bg, L588_ELEMENTS, L588_DIFFS, 60, OPTS),
    ("Level589", "灯具店", l589_bg, L589_ELEMENTS, L589_DIFFS, 60, OPTS),
]
