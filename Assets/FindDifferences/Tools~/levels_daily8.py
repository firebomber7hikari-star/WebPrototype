# -*- coding: utf-8 -*-
"""Everyday-town themes, part 8: neighbourhood life (paper-craft, full-bleed, no real brands or logos):
  Level570 花鸟市场   - a flower-and-bird market: stalls of potted plants, birdcages, goldfish tanks, shoppers
  Level571 天台晾晒   - a rooftop on laundry day: washing lines, water tanks, potted plants, city around
  Level572 搬家日     - moving day: a van with the ramp down, boxes, sofa carried out, neighbours waving
  Level573 快递驿站   - a parcel pick-up station: shelves of parcels, scanner counter, delivery tricycle
  Level574 广场舞     - square dancing at dusk: dancers in rows, speaker cart, lamp posts, apartment blocks
  Level575 幼儿园     - a kindergarten classroom: low tables, cubbies, alphabet frieze, toys, teacher
  Level576 宠物美容   - a pet grooming salon: bathing tub, grooming table, dryer, dogs waiting
  Level577 路边烧烤摊 - a roadside barbecue stall: grill with smoke, folding tables, string bulbs; day / night
  Level578 雨天公交车厢 - inside a city bus on a rainy day: seats, grab handles, passengers, rainy street outside
  Level579 车库乐队   - a garage band: drum kit, amps, guitarists, posters, bikes and tools on the walls
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_daily3 import counter, plant, room, steam_el, wall_shelf, guitar
from stylekit import day_night, star_field, window_glow

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def box(c, x, base, w, h, col=(200, 160, 110), tape=(220, 190, 140)):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), col, border=1.2, shadow=PROP)
    flat(c, RRect(x - 4, base - h, x + 4, base - h * 0.4, 1), tape)
    flat(c, Thick(x - w / 2, base - h + 2, x + w / 2, base - h + 2, 1.4), lit(col, 0.85))


def birdcage(c, x, y, col=(200, 170, 80), bird=(250, 200, 60)):
    for j in range(7):
        flat(c, Thick(x - 18 + j * 6, y - 4 - abs(j - 3) * 3, x - 18 + j * 6, y + 40, 1.4), col)
    piece(c, Poly([(x - 20, y - 2), (x + 20, y - 2), (x, y - 20)]), col, shadow=SMALL)
    flat(c, Thick(x - 20, y + 40, x + 20, y + 40, 3), col)
    piece(c, [Ell(x, y + 22, 7, 9), Circ(x + 4, y + 12, 5)], bird, border=0.8, shadow=None)


# =================================================================== Level 570 flower-and-bird market
def l570_bg(c, d):
    sky(c, (140, 196, 236), (232, 238, 236), 240)
    far_skyline(c, 220, 40, 140, (190, 196, 214), 5701, win=(210, 216, 230))
    # market canopy roofs
    for k, (x0, col) in enumerate(((-10, (200, 70, 70)), (300, (60, 120, 190)), (610, (90, 160, 110)))):
        if k == 1 and "awning" in d:
            col = (240, 180, 60)
        piece(c, Poly([(x0, 140), (x0 + 310, 140), (x0 + 300, 190), (x0 + 10, 190)]), col, border=1.5, shadow=PROP)
        for x in range(x0 + 14, x0 + 300, 34):
            flat(c, Poly([(x, 140), (x + 17, 140), (x + 17, 190), (x, 190)]), lit(col, 1.15))
        flat(c, [Thick(x0 + 20, 190, x0 + 20, 470, 4), Thick(x0 + 290, 190, x0 + 290, 470, 4)], (120, 110, 100))
    # ground
    piece(c, RRect(-10, 470, 910, 612, 0), (200, 190, 176), shadow=LAYER)
    for y in range(490, H, 28):
        flat(c, Thick(0, y, W, y, 1.2), (186, 176, 162))
    # stall 1: potted plants on tiers
    for r, y in enumerate((300, 370, 440)):
        piece(c, RRect(20, y, 280, y + 10, 2), (170, 130, 90), shadow=SMALL)
        for i in range(5):
            x = 44 + i * 52
            pot = (200, 120, 90) if not (r == 1 and i == 3 and "pot" in d) else (90, 150, 220)
            leaf = [(90, 160, 90), (240, 120, 150), (250, 200, 70), (200, 120, 220), (80, 150, 100)][(i + r) % 5]
            piece(c, [Circ(x, y - 30, 14), Circ(x - 10, y - 24, 10), Circ(x + 10, y - 24, 10)], leaf, shadow=SMALL)
            piece(c, Poly([(x - 13, y - 18), (x + 13, y - 18), (x + 9, y), (x - 9, y)]), pot, border=1, shadow=SMALL)
    # stall 2: birdcages hanging + on the table
    for k, x in enumerate((360, 450, 540)):
        flat(c, Thick(x, 190, x, 214, 1.4), (90, 90, 100))
        birdcage(c, x, 234, bird=[(250, 200, 60), (90, 180, 220), (240, 120, 120)][k] if not (k == 2 and "bird" in d) else (120, 200, 120))
    piece(c, RRect(330, 400, 580, 470, 3), (170, 130, 90), border=1.5, shadow=PROP)
    for k, x in enumerate((370, 450, 530)):
        birdcage(c, x, 350, col=(170, 140, 90), bird=[(250, 250, 250), (250, 160, 60), (120, 190, 240)][k])
    # stall 3: goldfish tanks
    piece(c, RRect(630, 380, 890, 470, 3), (170, 130, 90), border=1.5, shadow=PROP)
    for k, x in enumerate((680, 760, 840)):
        piece(c, RRect(x - 34, 300, x + 34, 380, 4), (190, 226, 240), border=1.2, shadow=SMALL)
        flat(c, RRect(x - 30, 314, x + 30, 376, 3), (140, 200, 230))
        for j in range(3):
            fx, fy = x - 16 + j * 14, 330 + (j % 2) * 18
            col = (250, 120, 50) if not (k == 1 and "fish" in d) else (250, 250, 250)
            piece(c, [Ell(fx, fy, 9, 6), Poly([(fx - 7, fy), (fx - 15, fy - 6), (fx - 15, fy + 6)])], col, border=0.6, shadow=None)
    # shoppers
    modern(c, 140, 600, (90, 150, 220), bottom=(50, 60, 90), hair=(130, 130, 140), h=2.3, glasses=True)
    modern(c, 300, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.2, style="long", bag=(200, 70, 70))
    modern(c, 600, 600, (120, 190, 120), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.3)
    modern(c, 820, 600, (220, 110, 150) if "shirt" not in d else (250, 250, 250), bottom=(60, 70, 110), hair=(220, 180, 90), h=2.2, style="twin")
    piece(c, [Ell(450, 590, 20, 8), RRect(436, 560, 464, 590, 4)], (200, 160, 100), border=1, shadow=SMALL)       # flower basket
    flat(c, [Circ(442, 556, 6), Circ(456, 552, 6)], (250, 120, 160))


L570_ELEMENTS = [
    E("hop%d" % i, (lambda x, col: lambda c, m: piece(c, [Ell(x, 256, 7, 9), Circ(x + 4, 246, 5)], col, border=0.8, shadow=None))(x, col),
      pivot=(x, 264), anim=dict(bobAmplitude=(0, 4), bobSpeed=1.2, bounce=True, phase=i / 2))
    for i, (x, col) in enumerate(((360, (250, 200, 60)), (450, (90, 180, 220))))
] + [
    E("bubble", lambda c, m: c.ellipse_ring(700, 360, 3, 3, 1.2, (230, 246, 255)), anim=dict(driftVelocity=(0, 18), driftLength=40, driftFade=True)),
    E("butterfly", lambda c, m: (flat(c, [Ell(-6, 0, 6, 4), Ell(6, 0, 6, 4)], (250, 200, 220)), flat(c, Thick(0, -4, 0, 4, 1.5), INK)),
      anim=dict(drift_across(-12, 12, 22, start=200), driftVelocity=(22, 0), bobAmplitude=(0, 14), bobSpeed=0.6, stretch=(0.5, 0), scaleSpeed=3)),
    bird_el("pigeon", 500, 60, s=8, speed=-18),
]

L570_DIFFS = [
    ("awning", 455, 165, 0),
    ("pot", 200, 352, 0),
    ("bird", 540, 256, 0),
    ("fish", 760, 340, 0),
    ("shirt", 821, 543, 0),
]


# =================================================================== Level 571 rooftop laundry day
def l571_bg(c, d):
    sky(c, (120, 186, 240), (226, 238, 246), 420)
    cloud_bg(c, 160, 60, 0.9)
    cloud_bg(c, 720, 40, 0.7)
    far_skyline(c, 300, 80, 240, (176, 190, 214), 5711, win=(200, 210, 230))
    # neighbouring rooftops
    for x, w, h, col in ((-10, 180, 120, (200, 170, 150)), (720, 200, 150, (180, 186, 200))):
        piece(c, RRect(x, 330 - h + 120, x + w, 360, 2), col, border=1.5, shadow=PROP)
    # roof deck + parapet
    piece(c, RRect(-10, 360, 910, 612, 0), (170, 166, 160), shadow=LAYER)
    for x in range(0, 900, 60):
        flat(c, Thick(x, 360, x, 612, 1.2), (156, 152, 146))
    piece(c, RRect(-10, 350, 910, 372, 2), (210, 206, 200), border=1, shadow=SMALL)
    # water tanks (left) + stair hut (right)
    for k, x in enumerate((90, 200)):
        flat(c, [Thick(x - 30, 350, x - 30, 290, 4), Thick(x + 30, 350, x + 30, 290, 4)], (120, 120, 130))
        piece(c, [RRect(x - 40, 210, x + 40, 290, 10), Ell(x, 210, 40, 10)], (90, 150, 210) if not (k == 1 and "tank" in d) else (230, 120, 70), border=1.5,
              shadow=PROP)
    piece(c, RRect(740, 230, 880, 360, 2), (220, 216, 206), border=1.5, shadow=PROP)
    flat(c, RRect(780, 270, 840, 360, 2), (110, 90, 80) if "door" not in d else (60, 120, 180))
    # washing lines with clothes (static)
    for y in (170, 220):
        flat(c, Thick(260, y, 720, y + 10, 1.6), (90, 90, 100))
    flat(c, [Thick(260, 150, 260, 360, 4), Thick(720, 150, 720, 360, 4)], (150, 150, 160))
    items = [(300, 170, (250, 250, 250), "shirt"), (380, 172, (90, 150, 220), "towel"), (460, 174, (240, 200, 90), "dress"), (540, 176, (220, 90, 90), "shirt"),
             (620, 178, (120, 190, 160), "towel"), (330, 222, (240, 150, 180), "sock"), (420, 224, (60, 80, 130), "trousers"), (520, 226, (250, 250, 250), "sheet")]
    for k, (x, y, col, kind) in enumerate(items):
        if k == 3 and "shirt" in d:
            col = (250, 200, 60)
        if kind == "shirt":
            piece(c, [Poly([(x - 22, y), (x + 22, y), (x + 30, y + 14), (x + 18, y + 18), (x + 18, y + 50), (x - 18, y + 50), (x - 18, y + 18), (x - 30, y + 14)])],
                  col, border=1, shadow=SMALL)
        elif kind == "towel":
            piece(c, RRect(x - 24, y, x + 24, y + 56, 2), col, border=1, shadow=SMALL)
            flat(c, Thick(x - 24, y + 46, x + 24, y + 46, 3), lit(col, 0.8))
        elif kind == "dress":
            piece(c, Poly([(x - 14, y), (x + 14, y), (x + 30, y + 64), (x - 30, y + 64)]), col, border=1, shadow=SMALL)
        elif kind == "sock":
            piece(c, [Poly([(x - 6, y), (x + 6, y), (x + 6, y + 30), (x + 16, y + 34), (x + 14, y + 42), (x - 6, y + 38)])], col, border=1, shadow=SMALL)
        elif kind == "trousers":
            piece(c, [Poly([(x - 20, y), (x + 20, y), (x + 22, y + 70), (x + 6, y + 70), (x, y + 24), (x - 6, y + 70), (x - 22, y + 70)])], col, border=1, shadow=SMALL)
        else:
            piece(c, RRect(x - 50, y, x + 50, y + 80, 2), col, border=1, shadow=SMALL)
    for k, (x, y, *_r) in enumerate(items):
        flat(c, [Thick(x - 8, y - 4, x - 8, y + 4, 3), Thick(x + 8, y - 4, x + 8, y + 4, 3)], (240, 120, 60))
    # basket + resident + plants
    piece(c, [Ell(320, 560, 46, 12), RRect(274, 520, 366, 560, 6)], (90, 170, 210) if "basket" not in d else (240, 140, 60), border=1.2, shadow=PROP)
    flat(c, [Circ(300, 514, 12), Circ(330, 510, 12)], (250, 250, 250))
    modern(c, 420, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.4, style="long")
    for x, pot in ((560, (200, 120, 90)), (640, (90, 150, 210)), (840, (200, 120, 90))):
        plant(c, x, 600, s=1.2, pot=pot)
    piece(c, [RRect(60, 520, 200, 532, 3), RRect(66, 532, 74, 570, 2), RRect(186, 532, 194, 570, 2)], (150, 110, 80), shadow=PROP)


L571_ELEMENTS = [
    E("sheet", lambda c, m: (piece(c, RRect(570, 226, 690, 316, 2), (240, 240, 250), border=1, shadow=SMALL),
                             flat(c, [Thick(590, 222, 590, 230, 3), Thick(670, 222, 670, 230, 3)], (240, 120, 60))), pivot=(630, 226),
      anim=dict(stretch=(0.06, 0.04), scaleSpeed=0.8, swingAngle=3, swingSpeed=0.6)),
    E("cat", lambda c, m: piece(c, [Ell(130, 512, 20, 9), Circ(150, 504, 8), Poly([(144, 500), (146, 490), (150, 498)]), Poly([(152, 498), (156, 490), (158, 502)])],
                                (240, 170, 90), border=1, shadow=SMALL), pivot=(130, 520), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
    bird_el("bird1", 300, 90, s=8, speed=20),
    bird_el("bird2", 640, 110, s=7, speed=-16),
]

L571_DIFFS = [
    ("tank", 200, 250, 0),
    ("door", 810, 315, 0),
    ("shirt", 540, 200, 0),
    ("basket", 320, 540, 0),
]


# =================================================================== Level 572 moving day
def l572_bg(c, d):
    sky(c, (130, 194, 240), (226, 238, 244), 440)
    cloud_bg(c, 760, 60, 0.7)
    # apartment block
    piece(c, RRect(400, 40, 900, 420, 2), (236, 220, 196), border=2, shadow=PROP)
    for r in range(4):
        for k in range(5):
            x, y = 430 + k * 92, 70 + r * 84
            flat(c, RRect(x, y, x + 56, y + 56, 3), (150, 190, 220))
            flat(c, Thick(x + 28, y, x + 28, y + 56, 2), (236, 220, 196))
    piece(c, RRect(600, 330, 680, 420, 3), (120, 90, 70), border=1.2, shadow=SMALL)
    flat(c, RRect(608, 340, 672, 420, 2), (60, 50, 50))
    # neighbour waving from a window
    modern(c, 520, 210, (200, 90, 120) if "neighbour" not in d else (90, 170, 120), bottom=(200, 90, 120), hair=(90, 60, 40), h=1.3, style="long")
    flat(c, Thick(536, 184, 548, 164, 3), (246, 214, 186))
    flat(c, RRect(512, 210, 580, 216, 1), (236, 220, 196))
    piece(c, Poly([(880, 140), (900, 140), (900, 160), (880, 160)]), (220, 70, 70), shadow=None)
    # street + pavement
    piece(c, RRect(-10, 420, 910, 612, 0), (150, 150, 158), shadow=LAYER)
    flat(c, RRect(-10, 420, 910, 440, 0), (200, 196, 186))
    # moving van (left) with the ramp down
    van = (250, 250, 250)
    piece(c, [RRect(20, 300, 280, 520, 6), Poly([(280, 520), (280, 360), (340, 360), (370, 420), (370, 520)])], van, border=1.5, shadow=PROP)
    flat(c, Poly([(290, 370), (334, 370), (358, 416), (290, 416)]), (170, 210, 236))
    piece(c, RRect(40, 340, 260, 380, 4), (60, 140, 200) if "van" not in d else (230, 120, 60), border=1, shadow=SMALL)
    sign_box(c, 60, 348, 240, 372, (250, 250, 250), 5721, vertical=False)
    flat(c, RRect(30, 390, 270, 510, 2), (90, 80, 70))
    for wx in (80, 220, 330):
        piece(c, Circ(wx, 528, 22), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(wx, 528, 9), (190, 190, 200))
    piece(c, Poly([(270, 510), (290, 510), (400, 590), (380, 600)]), (190, 190, 196), border=1, shadow=SMALL)
    # boxes stacked inside and on the pavement
    for x, b, w, h in ((60, 510, 60, 50), (130, 510, 70, 60), (90, 460, 54, 46), (200, 510, 50, 44)):
        box(c, x, b, w, h)
    for k, (x, b, w, h) in enumerate(((440, 600, 70, 60), (520, 600, 60, 50), (480, 540, 56, 46), (840, 600, 80, 64))):
        box(c, x, b, w, h, col=(200, 160, 110) if not (k == 2 and "box" in d) else (120, 170, 220))
    # movers carrying a sofa
    modern(c, 650, 600, (60, 110, 180), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.3)
    modern(c, 790, 600, (60, 110, 180), bottom=(50, 50, 60), hair=(90, 60, 40), h=2.3)
    piece(c, [RRect(630, 500, 810, 540, 10), RRect(630, 470, 660, 540, 8), RRect(780, 470, 810, 540, 8)], (200, 80, 80) if "sofa" not in d else (90, 160, 120),
          border=1.5, shadow=PROP)
    # lamp + plant + kid with a teddy
    piece(c, [Thick(560, 600, 560, 500, 3), Poly([(536, 500), (584, 500), (574, 470), (546, 470)])], (240, 200, 90) if "lamp" not in d else (120, 190, 230),
          border=1, shadow=SMALL)
    modern(c, 360, 600, (250, 210, 80), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.5, style="twin")
    piece(c, [Circ(380, 548, 10), Circ(374, 538, 4), Circ(386, 538, 4)], (190, 140, 90), border=1, shadow=SMALL)


L572_ELEMENTS = [
    E("wave", lambda c, m: flat(c, Thick(536, 184, 548, 164, 3), (246, 214, 186)), pivot=(536, 184), anim=dict(swingAngle=24, swingSpeed=1.4)),
    E("balloon", lambda c, m: (flat(c, Thick(366, 556, 372, 500, 1), (90, 90, 100)), piece(c, Ell(372, 488, 12, 14), (240, 90, 120), border=1, shadow=SMALL)),
      pivot=(366, 556), anim=dict(swingAngle=8, swingSpeed=0.5)),
    E("car", lambda c, m: (piece(c, RRect(0, 560, 110, 596, 10), (90, 170, 220), border=1.5, shadow=PROP),
                           piece(c, [Circ(24, 600, 12), Circ(86, 600, 12)], (40, 40, 46), shadow=SMALL)),
      anim=dict(drift_across(0, 110, -50, start=-200))),
    bird_el("bird", 300, 60, s=8, speed=18),
]

L572_DIFFS = [
    ("van", 150, 360, 0),
    ("box", 480, 517, 0),
    ("sofa", 720, 505, 0),
    ("lamp", 560, 486, 0),
    ("neighbour", 521, 190, 0),
]


# =================================================================== Level 573 parcel pick-up station
def parcel(c, x, base, w, h, col):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), col, border=1, shadow=SMALL)
    flat(c, RRect(x - w / 4, base - h / 2 - 4, x + w / 4, base - h / 2 + 4, 1), (250, 250, 250))


def l573_bg(c, d):
    room(c, (230, 234, 238), (224, 228, 234), (190, 190, 190), (176, 176, 176), floor_y=480)
    # parcel shelves
    rnd = random.Random(5731)
    for k, x0 in enumerate((20, 260)):
        piece(c, RRect(x0, 60, x0 + 220, 470, 2), (150, 154, 166), border=1.5, shadow=PROP)
        for r, y in enumerate((150, 240, 330, 420)):
            flat(c, RRect(x0 + 6, y, x0 + 214, y + 8, 1), (120, 124, 136))
            x = x0 + 16
            i = 0
            while x < x0 + 190:
                w, h = rnd.choice(((40, 50), (50, 36), (34, 60), (60, 44)))
                col = rnd.choice([(200, 160, 110), (220, 190, 140), (190, 150, 100), (250, 250, 250)])
                if k == 1 and r == 1 and i == 1 and "parcel" in d:
                    col = (240, 120, 160)
                parcel(c, x + w / 2, y, w, h, col)
                x += w + 6
                i += 1
    # shelf number signs
    for k, x in enumerate((130, 370)):
        piece(c, RRect(x - 24, 30, x + 24, 56, 3), (250, 200, 60) if not (k == 1 and "label" in d) else (90, 170, 230), border=1, shadow=SMALL)
        flat(c, Thick(x, 36, x, 50, 4), (40, 40, 50))
    # counter with scanner + clerk
    modern(c, 680, 400, (60, 140, 90), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.4)
    counter(c, 540, 900, 380, 480, (60, 140, 90))
    piece(c, [RRect(580, 340, 640, 380, 4)], (40, 44, 56), border=1, shadow=SMALL)
    flat(c, RRect(588, 348, 632, 370, 2), (120, 220, 170))
    flat(c, [Thick(760, 380, 790, 340, 4), RRect(784, 330, 806, 346, 3)], (60, 60, 70))
    piece(c, [RRect(820, 300, 880, 380, 4)], (250, 250, 250), border=1, shadow=SMALL)       # weighing scale
    flat(c, RRect(828, 310, 872, 330, 2), (90, 200, 120))
    # wall clock + notice board
    piece(c, Circ(700, 120, 30), (250, 250, 252) if "clock" not in d else (250, 220, 110), border=1.5, shadow=PROP)
    c.ellipse_ring(700, 120, 30, 30, 3, (60, 60, 70))
    flat(c, [Thick(700, 120, 700, 98, 2.4), Thick(700, 120, 716, 126, 2.4)], (40, 40, 50))
    piece(c, RRect(560, 180, 680, 280, 3), (190, 150, 100), border=1.2, shadow=PROP)
    for k, (x, y, col) in enumerate(((572, 192, (250, 240, 150)), (620, 196, (240, 200, 220)), (590, 236, (200, 230, 250)))):
        flat(c, RRect(x, y, x + 44, y + 34, 1), col)
    # customers + delivery tricycle at the door
    modern(c, 500, 600, (240, 120, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.3, style="long")
    parcel(c, 480, 556, 40, 36, (200, 160, 110))
    modern(c, 380, 600, (90, 150, 220), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.3, glasses=True)
    piece(c, [RRect(40, 520, 200, 580, 4)], (250, 190, 60) if "trike" not in d else (90, 170, 120), border=1.5, shadow=PROP)
    for wx in (60, 180, 250):
        c.ellipse_ring(wx, 590, 16, 16, 4, (40, 40, 46))
    flat(c, [Thick(200, 560, 240, 520, 4), Thick(240, 520, 250, 590, 4), Thick(234, 520, 250, 510, 4)], (60, 60, 70))
    parcel(c, 90, 520, 60, 40, (200, 160, 110))
    parcel(c, 150, 520, 50, 30, (220, 190, 140))


L573_ELEMENTS = [
    E("beep", lambda c, m: soft_union(c, [RRect(588, 348, 632, 370, 2)], (150, 255, 200), 0.5, spread=10), daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.0)),
    E("tape", lambda c, m: (piece(c, Circ(860, 470, 10), (220, 190, 140), shadow=SMALL), flat(c, Circ(860, 470, 4), (150, 120, 90))), pivot=(860, 470),
      anim=dict(rotateSpeed=120)),
    E("fan", lambda c, m: (flat(c, Thick(450, 0, 450, 18, 2), (90, 90, 100)),
                           flat(c, [Thick(450 - 60 * math.cos(a), 22 - 6 * math.sin(a), 450 + 60 * math.cos(a), 22 + 6 * math.sin(a), 6) for a in (0.3, 1.9)],
                                (170, 130, 90))), pivot=(450, 22), anim=dict(stretch=(0.8, 0), scaleSpeed=3.0)),
]

L573_DIFFS = [
    ("parcel", 330, 226, 0),
    ("label", 370, 43, 0),
    ("clock", 700, 120, 0),
    ("trike", 120, 550, 0),
]


# =================================================================== Level 574 square dancing at dusk
def l574_bg(c, d):
    c.gradient(0, 330, (90, 110, 170), (240, 170, 140))
    piece(c, Circ(500, 70, 30), (250, 220, 170) if "moon" not in d else (250, 170, 120), border=1.5, shadow=None)
    # apartment blocks with lit windows
    for k, (x, w, h, col) in enumerate(((-10, 220, 260, (170, 150, 150)), (210, 180, 220, (150, 150, 170)), (600, 160, 240, (160, 150, 150)),
                                        (760, 160, 280, (150, 146, 166)))):
        piece(c, RRect(x, 330 - h, x + w, 330, 2), col, border=1.5, shadow=PROP)
        rnd = random.Random(5741 + k)
        for y in range(330 - h + 20, 320, 34):
            for wx in range(int(x) + 14, int(x + w) - 20, 32):
                lit_ = (255, 220, 140) if rnd.random() < 0.5 else (110, 110, 140)
                if k == 2 and y == 330 - h + 54 and wx < x + 50 and "window" in d:
                    lit_ = (120, 220, 255)
                flat(c, RRect(wx, y, wx + 20, y + 22, 1), lit_)
    # plaza
    piece(c, RRect(-10, 330, 910, 612, 0), (190, 176, 160), shadow=LAYER)
    for y in range(350, H, 26):
        flat(c, Thick(0, y, W, y, 1.2), (176, 162, 146))
    # lamp posts
    for k, x in enumerate((60, 840)):
        piece(c, [RRect(x - 4, 340, x + 4, 560, 2)], (50, 56, 70), shadow=PROP)
        piece(c, Ell(x, 334, 18, 12), (50, 56, 70) if not (k == 1 and "lamp" in d) else (200, 80, 60), shadow=SMALL)
        flat(c, Ell(x, 340, 10, 5), (255, 236, 160))
    # speaker cart
    piece(c, [RRect(110, 470, 200, 560, 6)], (60, 60, 70) if "speaker" not in d else (200, 70, 90), border=1.5, shadow=PROP)
    flat(c, [Circ(155, 498, 16), Circ(155, 538, 10)], (90, 90, 100))
    piece(c, [Circ(124, 566, 8), Circ(186, 566, 8)], (40, 40, 46), shadow=SMALL)
    flat(c, Thick(200, 480, 226, 450, 3), (60, 60, 70))
    # dancers in rows (fans in hand)
    cols = [(220, 60, 80), (250, 200, 70), (90, 160, 220), (230, 120, 170), (120, 190, 120)]
    for r, (base, h) in enumerate(((420, 1.6), (500, 1.9), (590, 2.2))):
        for k in range(5):
            x = 300 + k * 110 + (r % 2) * 40
            col = cols[(k + r) % 5]
            if r == 1 and k == 3 and "dancer" in d:
                col = (250, 250, 250)
            modern(c, x, base, col, bottom=(40, 40, 50), hair=[(40, 30, 30), (130, 130, 140), (90, 60, 40)][(k + r) % 3], h=h, style="long" if (k + r) % 2 else "short")
    # bench with a watcher + bicycle
    piece(c, [RRect(20, 590, 120, 600, 2)], (130, 90, 60), shadow=SMALL)


L574_ELEMENTS = [
    E("fans", lambda c, m: [piece(c, Poly([(x, y), (x + 20, y - 18), (x + 24, y - 4)]), (250, 80, 100), border=0.8, shadow=None)
                            for x, y in ((316, 360), (426, 360), (536, 360), (646, 360), (756, 360))],
      pivot=(530, 360), anim=dict(bobAmplitude=(6, 6), bobSpeed=0.8)),
    E("sway", lambda c, m: modern(c, 340, 590, (220, 60, 80), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.2), pivot=(340, 590), anim=dict(swingAngle=4, swingSpeed=0.8)),
    E("notes", lambda c, m: [flat(c, [Circ(220 + k * 22, 450 - k * 14, 5), Thick(224 + k * 22, 450 - k * 14, 224 + k * 22, 430 - k * 14, 2)], (255, 230, 140))
                             for k in range(3)], daynight="untinted", anim=dict(driftVelocity=(10, 20), driftLength=50, driftFade=True)),
    E("glow1", lambda c, m: soft_union(c, [Circ(60, 340, 8)], (255, 220, 140), 0.55, spread=34), daynight="untinted", anim=dict(twinkle=0.1, twinkleSpeed=1.0)),
    E("glow2", lambda c, m: soft_union(c, [Circ(840, 340, 8)], (255, 220, 140), 0.55, spread=34), daynight="untinted", anim=dict(twinkle=0.1, twinkleSpeed=1.0, phase=0.5)),
]

L574_DIFFS = [
    ("window", 630, 115, 0),
    ("speaker", 155, 515, 0),
    ("dancer", 670, 450, 0),
    ("moon", 500, 70, 0),
    ("lamp", 840, 334, 0),
]


# =================================================================== Level 575 kindergarten classroom
def l575_bg(c, d):
    room(c, (250, 236, 210), (246, 230, 200), (180, 210, 170), (166, 196, 156), floor_y=470)
    # alphabet frieze
    pal = [(240, 100, 100), (250, 190, 70), (110, 190, 110), (90, 150, 230), (200, 120, 220)]
    for k in range(16):
        col = pal[k % 5]
        if k == 6 and "letter" in d:
            col = (60, 60, 70)
        piece(c, RRect(20 + k * 54, 20, 64 + k * 54, 64, 6), col, border=1, shadow=SMALL)
        flat(c, Thick(34 + k * 54, 54, 42 + k * 54, 30, 4), (250, 250, 250))
        flat(c, Thick(42 + k * 54, 30, 50 + k * 54, 54, 4), (250, 250, 250))
    # window with sun drawing + paintings
    piece(c, RRect(330, 90, 570, 270, 4), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(340, 100, 560, 260, 3), (180, 220, 240))
    tree_round(c, 400, 260, s=1.1)
    flat(c, Thick(450, 100, 450, 260, 3), (250, 250, 250))
    for k, (x, col) in enumerate(((620, (250, 210, 80)), (740, (120, 200, 230)))):
        piece(c, RRect(x, 100, x + 100, 190, 2), (250, 250, 250), border=1.2, shadow=PROP)
        flat(c, Circ(x + 50, 140, 26), col if not (k == 1 and "drawing" in d) else (240, 120, 160))
        flat(c, Thick(x + 20, 176, x + 80, 176, 3), (90, 160, 90))
    # cubbies (left)
    piece(c, RRect(20, 110, 280, 330, 3), (230, 190, 140), border=1.5, shadow=PROP)
    for r in range(3):
        for k in range(4):
            x, y = 30 + k * 62, 120 + r * 70
            flat(c, RRect(x, y, x + 54, y + 60, 3), (200, 160, 110))
            col = pal[(k + r * 2) % 5]
            if r == 1 and k == 2 and "bag" in d:
                col = (60, 60, 70)
            piece(c, RRect(x + 10, y + 20, x + 44, y + 58, 6), col, border=0.8, shadow=None)
    # low tables + tiny chairs + kids
    for k, (x, tcol) in enumerate(((240, (250, 200, 70)), (600, (90, 170, 230)))):
        if k == 1 and "table" in d:
            tcol = (240, 120, 120)
        piece(c, [RRect(x - 110, 470, x + 110, 484, 5), RRect(x - 100, 484, x - 92, 540, 2), RRect(x + 92, 484, x + 100, 540, 2)], tcol, border=1.2, shadow=PROP)
    for k, (x, col, hair, st) in enumerate(((160, (240, 120, 120), (40, 30, 30), "twin"), (240, (120, 190, 120), (90, 60, 40), "short"),
                                           (320, (250, 200, 70), (220, 180, 90), "short"), (540, (200, 120, 220), (40, 30, 30), "twin"),
                                           (660, (90, 150, 230), (90, 60, 40), "short"))):
        modern(c, x, 560, col, bottom=(60, 70, 110), hair=hair, h=1.4, style=st)
    # crayons and paper on tables
    for x in (200, 280, 560, 640):
        piece(c, RRect(x - 22, 460, x + 22, 470, 1), (250, 250, 250), border=0.8, shadow=None)
        flat(c, [Thick(x - 10 + j * 6, 466, x - 4 + j * 6, 458, 3) for j in range(3)], pal[(x // 40) % 5])
    # teacher + toy box + rocking horse
    modern(c, 820, 600, (120, 170, 200), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.6, style="long")
    piece(c, RRect(20, 540, 130, 600, 6), (240, 120, 90), border=1.5, shadow=PROP)
    flat(c, [Circ(46, 534, 12), RRect(80, 520, 110, 542, 3)], (90, 170, 230))
    piece(c, [Ell(440, 560, 40, 18), Circ(470, 528, 14), Thick(470, 520, 486, 500, 6)], (200, 140, 90), border=1.2, shadow=PROP)
    c.ellipse_ring(440, 590, 50, 10, 5, (170, 110, 70), ymin=590)


L575_ELEMENTS = [
    E("rock", lambda c, m: (piece(c, [Ell(440, 560, 40, 18), Circ(470, 528, 14)], (200, 140, 90), border=1.2, shadow=PROP)), pivot=(440, 590),
      anim=dict(swingAngle=6, swingSpeed=0.6)),
    E("mobile", lambda c, m: (flat(c, Thick(220, 66, 220, 86, 1.2), (100, 100, 110)), flat(c, Thick(180, 86, 260, 86, 2), (100, 100, 110)),
                              [piece(c, Poly(star_pts(x, 104, 12, 5)), col, border=1, shadow=SMALL) for x, col in ((180, (250, 200, 60)), (260, (240, 120, 160)))]),
      pivot=(220, 66), anim=dict(swingAngle=8, swingSpeed=0.3)),
    E("ball", lambda c, m: (piece(c, Circ(740, 580, 14), (240, 90, 90), shadow=SMALL), flat(c, Thick(728, 580, 752, 580, 2), (250, 250, 250))),
      pivot=(740, 594), anim=dict(bobAmplitude=(0, 24), bobSpeed=1.0, bounce=True)),
]

L575_DIFFS = [
    ("letter", 362, 42, 0),
    ("drawing", 790, 140, 0),
    ("bag", 181, 209, 0),
    ("table", 600, 477, 0),
]


# =================================================================== Level 576 pet grooming salon
def poodle(c, x, base, col=(250, 250, 250), s=1.0):
    piece(c, [Circ(x - 18 * s, base - 30 * s, 13 * s), Circ(x, base - 34 * s, 14 * s), Circ(x + 16 * s, base - 30 * s, 12 * s), Circ(x + 26 * s, base - 54 * s, 14 * s),
              Circ(x + 30 * s, base - 68 * s, 9 * s), Circ(x - 32 * s, base - 40 * s, 8 * s)] +
          [RRect(x + dx * s - 3 * s, base - 22 * s, x + dx * s + 3 * s, base, 1) for dx in (-16, -6, 10, 18)], col, border=1.2, shadow=PROP)
    flat(c, Ell(x + 18 * s, base - 54 * s, 6 * s, 10 * s), lit(col, 0.85))
    flat(c, [Circ(x + 30 * s, base - 56 * s, 1.8 * s), Circ(x + 38 * s, base - 52 * s, 2.4 * s)], INK)


def l576_bg(c, d):
    room(c, (220, 236, 240), (214, 230, 236), (200, 200, 210), (186, 186, 196), floor_y=480)
    # tiled wall section + mirror
    for y in range(200, 470, 24):
        for x in range(20, 420, 24):
            flat(c, RRect(x + 1, y + 1, x + 23, y + 23, 2), (240, 246, 250))
    piece(c, RRect(500, 60, 660, 240, 6), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(510, 70, 650, 230, 4), (210, 230, 238))
    # bathing tub with a dog in suds
    piece(c, [RRect(40, 330, 300, 440, 12), RRect(60, 440, 80, 480, 2), RRect(260, 440, 280, 480, 2)], (250, 250, 250), border=1.5, shadow=PROP)
    poodle(c, 160, 400, col=(200, 160, 110) if "dog" not in d else (90, 90, 100), s=1.4)
    flat(c, [Circ(80 + k * 22, 334 - (k % 3) * 8, 14) for k in range(10)], (250, 252, 255))
    flat(c, [Thick(290, 320, 290, 200, 4), Thick(290, 200, 230, 200, 4)], (150, 150, 160))
    piece(c, Ell(226, 212, 14, 8), (150, 150, 160), shadow=SMALL)
    # grooming table + groomer + white poodle
    piece(c, [RRect(440, 400, 700, 416, 3), RRect(460, 416, 470, 480, 2), RRect(670, 416, 680, 480, 2)], (90, 150, 200), border=1.2, shadow=PROP)
    flat(c, [Thick(570, 400, 570, 280, 3), Thick(570, 280, 620, 280, 3)], (150, 150, 160))
    poodle(c, 560, 400, s=1.5)
    flat(c, [Poly([(597, 319), (580, 308), (580, 330)]), Poly([(597, 319), (614, 308), (614, 330)]), Circ(597, 319, 5)],
         (240, 90, 140) if "bow" not in d else (90, 170, 230))
    modern(c, 750, 600, (240, 140, 160), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.5, style="long")
    flat(c, [Thick(722, 470, 690, 440, 3)], (150, 150, 160))
    # dryer stand
    flat(c, Thick(390, 480, 390, 340, 4), (120, 120, 130))
    piece(c, [RRect(370, 310, 430, 350, 8), Thick(430, 330, 460, 350, 8)], (250, 200, 60) if "dryer" not in d else (120, 200, 150), border=1, shadow=SMALL)
    # waiting area: dogs on leashes, shelf of shampoos
    wall_shelf(c, 720, 890, 150)
    for k in range(5):
        piece(c, [RRect(734 + k * 32, 104, 756 + k * 32, 150, 4), RRect(740 + k * 32, 96, 750 + k * 32, 106, 1)],
              [(120, 200, 230), (250, 180, 200), (190, 230, 160), (250, 220, 120), (200, 180, 240)][k], border=0.8, shadow=None)
    piece(c, [Ell(120, 560, 30, 14), Circ(150, 540, 13), Ell(146, 528, 6, 10), Thick(90, 556, 76, 540, 5)] +
          [RRect(x - 3, 560, x + 3, 590, 1) for x in (100, 110, 132, 142)], (240, 180, 90) if "collar" not in d else (150, 150, 160), border=1.2, shadow=PROP)
    flat(c, Circ(156, 538, 2), INK)
    flat(c, RRect(140, 546, 158, 552, 2), (220, 60, 70))
    piece(c, [Ell(300, 580, 26, 12), Circ(326, 564, 12)] + [RRect(x - 3, 580, x + 3, 600, 1) for x in (284, 294, 310, 318)], (60, 60, 66), border=1.2, shadow=PROP)
    flat(c, Circ(332, 562, 2), (250, 250, 250))


L576_ELEMENTS = [
    E("bubbles%d" % i, (lambda x: lambda c, m: c.ellipse_ring(x, 300, 6, 6, 1.6, (220, 240, 255)))(x),
      anim=dict(driftVelocity=(4, 30), driftLength=120, driftFade=True, phase=i / 3)) for i, x in enumerate((110, 170, 230))
] + [
    E("wag", lambda c, m: flat(c, Thick(90, 556, 74, 538, 5), (240, 180, 90)), pivot=(90, 556), anim=dict(swingAngle=24, swingSpeed=1.8)),
    E("air", lambda c, m: [soft_union(c, [Circ(470 + k * 16, 352 + k * 6, 4)], (230, 240, 250), 0.6, spread=4) for k in range(3)],
      anim=dict(twinkle=0.5, twinkleSpeed=2.0)),
]

L576_DIFFS = [
    ("dog", 160, 360, 0),
    ("bow", 597, 319, 0),
    ("dryer", 400, 330, 0),
    ("collar", 125, 556, 0),
]


# =================================================================== Level 577 roadside barbecue stall (day / night)
DN577 = day_night(40.0, tint=(0.30, 0.28, 0.52))


def l577_bg(c, d):
    sky(c, (120, 180, 230), (240, 210, 190), 260)
    far_skyline(c, 240, 50, 170, (170, 176, 200), 5771, win=(255, 220, 140))
    # shop row
    piece(c, RRect(-10, 120, 910, 360, 2), (200, 176, 150), border=1.5, shadow=PROP)
    for k, x in enumerate((30, 250, 470, 690)):
        flat(c, RRect(x, 200, x + 180, 340, 3), (250, 220, 160))
        col = [(200, 60, 60), (60, 110, 180), (240, 180, 60), (90, 160, 110)][k]
        if k == 2 and "sign" in d:
            col = (150, 90, 200)
        piece(c, RRect(x, 140, x + 180, 186, 4), col, border=1.2, shadow=SMALL)
        sign_box(c, x + 16, 150, x + 164, 176, (250, 240, 200), 5772 + k, vertical=False)
    # pavement + road edge
    piece(c, RRect(-10, 360, 910, 612, 0), (170, 166, 160), shadow=LAYER)
    for y in range(380, H, 30):
        flat(c, Thick(0, y, W, y, 1.2), (156, 152, 146))
    # grill cart
    piece(c, [RRect(320, 380, 580, 470, 4)], (180, 180, 190), border=1.5, shadow=PROP)
    flat(c, RRect(330, 372, 570, 384, 2), (60, 60, 66))
    for k in range(8):
        x = 344 + k * 28
        flat(c, Thick(x, 360, x, 386, 2), (200, 180, 140))
        flat(c, [RRect(x - 5, 362, x + 5, 380, 3)], (190, 110, 60))
    piece(c, [Circ(350, 480, 12), Circ(550, 480, 12)], (40, 40, 46), shadow=SMALL)
    modern(c, 450, 360, (250, 250, 250), bottom=(60, 60, 70), hair=(40, 30, 30), h=1.2)
    # griller standing behind
    modern(c, 620, 470, (220, 70, 70) if "apron" not in d else (60, 130, 200), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.4)
    # folding tables + stools + diners
    for k, x in enumerate((140, 760)):
        piece(c, [RRect(x - 90, 500, x + 90, 512, 2), RRect(x - 80, 512, x - 74, 570, 2), RRect(x + 74, 512, x + 80, 570, 2)], (240, 240, 244), border=1.2, shadow=PROP)
        for j in range(3):
            piece(c, RRect(x - 50 + j * 40, 470, x - 34 + j * 40, 500, 4), (250, 210, 90), border=0.8, shadow=None)       # cups
        for sx in (x - 100, x + 100):
            piece(c, [RRect(sx - 16, 560, sx + 16, 568, 2), RRect(sx - 12, 568, sx - 8, 600, 1), RRect(sx + 8, 568, sx + 12, 600, 1)],
                  (60, 110, 200) if not (k == 1 and sx > x and "stool" in d) else (220, 80, 80), shadow=SMALL)
    for x, col in ((40, (90, 150, 110)), (240, (240, 200, 90)), (660, (150, 120, 180)), (860, (200, 110, 110))):
        modern(c, x, 560, col, bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0)
    # crate of drinks
    piece(c, RRect(300, 560, 380, 600, 2), (220, 70, 70) if "crate" not in d else (60, 120, 200), border=1.2, shadow=PROP)
    flat(c, [RRect(306 + k * 18, 546, 318 + k * 18, 562, 2) for k in range(4)], (120, 180, 120))


def bulbs(c, m):
    pts = [(x, 200 + 18 * math.sin((x / 900) * math.pi * 2) ** 2 + 4) for x in range(0, 920, 40)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(len(pts) - 1)], (60, 60, 70))
    for x, y in pts:
        flat(c, Circ(x, y + 6, 5), (255, 220, 140))


L577_ELEMENTS = [
    E("bulbs", bulbs, daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=1.0)),
    E("bulbglow", lambda c, m: [soft_union(c, [Circ(x, 210 + 18 * math.sin((x / 900) * math.pi * 2) ** 2, 4)], (255, 210, 120), 0.5, spread=16)
                                for x in range(0, 920, 40)], daynight="night"),
    window_glow("shops", [(30 + k * 220, 200, 210 + k * 220, 340) for k in range(4)]),
] + [
    E("smoke%d" % i, (lambda: lambda c, m: soft_union(c, [Circ(450, 350, 14)], (230, 230, 236), 0.7, spread=14))(),
      anim=dict(driftVelocity=(-6, 26), driftLength=110, driftFade=True, driftGrow=1.8, phase=i / 3)) for i in range(3)
] + [
    E("ember", lambda c, m: [flat(c, Circ(400 + k * 30, 372, 2.4), (255, 160, 60)) for k in range(5)], daynight="untinted",
      anim=dict(twinkle=0.7, twinkleSpeed=2.0)),
]

L577_DIFFS = [
    ("sign", 560, 163, 0),
    ("crate", 340, 576, 0),
    ("apron", 621, 401, 0),
    ("stool", 860, 564, 0),
]


# =================================================================== Level 578 inside a city bus on a rainy day
def l578_bg(c, d):
    # outside through the windows: rainy street
    c.gradient(0, 300, (150, 160, 180), (190, 196, 206))
    far_skyline(c, 300, 60, 220, (140, 150, 170), 5781, win=(230, 220, 170))
    c.rect(0, 260, W, 300, (110, 110, 118))
    for x, col in ((120, (220, 70, 90)), (420, (60, 60, 80)), (700, (250, 200, 60))):
        piece(c, Poly([(x - 40, 250), (x + 40, 250), (x, 226)]), col, border=1, shadow=SMALL)
        flat(c, Thick(x, 250, x, 280, 2), (40, 40, 50))
    # bus body: window frames + interior
    c.rect(0, 300, W, H, (220, 222, 228))
    piece(c, RRect(-10, 0, 910, 36, 0), (210, 212, 218), shadow=SMALL)
    for x in range(0, 901, 180):
        piece(c, RRect(x - 10, 30, x + 10, 310, 2), (200, 202, 210), shadow=SMALL)
    piece(c, RRect(-10, 296, 910, 330, 0), (190, 192, 200), shadow=SMALL)
    for x in range(0, 900, 180):
        flat(c, Poly([(x + 30, 50), (x + 70, 50), (x + 30, 140)]), (255, 255, 255, 0.16))
    # grab rail + handles (static parts)
    flat(c, Thick(0, 54, W, 54, 5), (170, 174, 184))
    # stop button + route display
    piece(c, RRect(360, 6, 540, 30, 3), (40, 44, 56), border=1, shadow=SMALL)
    sign_box(c, 376, 10, 524, 26, (250, 160, 60) if "display" not in d else (90, 220, 120), 5782, vertical=False)
    # seats
    for k, x in enumerate((60, 220, 640, 800)):
        seat = (60, 110, 180) if not (k == 2 and "seat" in d) else (220, 80, 80)
        piece(c, [RRect(x - 50, 380, x + 50, 470, 10), RRect(x - 56, 460, x + 56, 490, 8)], seat, border=1.5, shadow=PROP)
        flat(c, RRect(x - 40, 392, x + 40, 452, 6), lit(seat, 1.1))
    # floor
    c.rect(0, 500, W, H, (110, 116, 126))
    for x in range(0, 900, 30):
        flat(c, Thick(x, 500, x - 20, H, 1.2), (100, 106, 116))
    # pole + passengers
    flat(c, [Thick(450, 36, 450, 600, 6)], (250, 200, 60))
    piece(c, Circ(452, 260, 15), (220, 60, 60) if "button" not in d else (60, 180, 110), border=1, shadow=SMALL)
    modern(c, 60, 470, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.8, style="long")
    modern(c, 220, 470, (90, 150, 110), bottom=(50, 50, 60), hair=(130, 130, 140), h=1.8, glasses=True)
    piece(c, RRect(232, 414, 262, 436, 2), (240, 230, 200), border=1, shadow=SMALL)
    modern(c, 800, 470, (200, 110, 150), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.8)
    modern(c, 520, 600, (60, 80, 120), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.4, bag=(150, 100, 60))
    modern(c, 380, 600, (240, 140, 90), bottom=(60, 70, 110), hair=(220, 180, 90), h=2.3, style="long")
    # wet umbrella on the floor
    piece(c, [Thick(640, 600, 690, 520, 6), Poly([(684, 520), (704, 524), (698, 540)])], (60, 150, 200) if "umbrella" not in d else (240, 120, 160), border=1,
          shadow=SMALL)
    flat(c, [Ell(660, 600, 20, 4)], (150, 170, 196))


def rain_streaks(c, m):
    rnd = random.Random(5783)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(40, 290)
        flat(c, Thick(x, y, x + 3, y + 16, 1.2), (230, 236, 250, 0.7))


L578_ELEMENTS = [
    E("rain", rain_streaks, bbox=(-10, 0, 920, 320), anim=dict(driftVelocity=(0, -60), driftLength=20)),
] + [
    E("handle%d" % i, (lambda x: lambda c, m: (flat(c, Thick(x, 54, x, 90, 2), (170, 174, 184)), c.ellipse_ring(x, 100, 10, 10, 3, (250, 250, 250))))(x),
      pivot=(x, 54), anim=dict(swingAngle=10, swingSpeed=0.6, phase=i / 5)) for i, x in enumerate((100, 300, 600, 760, 860))
] + [
    E("drops", lambda c, m: [flat(c, Ell(90 + k * 180, 200 + (k % 2) * 40, 3, 5), (230, 240, 250)) for k in range(5)],
      anim=dict(driftVelocity=(0, -14), driftLength=40, driftFade=True)),
    E("car", lambda c, m: (piece(c, RRect(0, 266, 120, 296, 10), (220, 70, 70), border=1, shadow=SMALL),
                           soft_union(c, [Circ(118, 282, 6)], (255, 240, 180), 0.8, spread=12)), anim=dict(drift_across(0, 120, -60, start=300))),
]

L578_DIFFS = [
    ("display", 450, 18, 0),
    ("seat", 640, 430, 0),
    ("button", 452, 260, 0),
    ("umbrella", 672, 556, 0),
]


# =================================================================== Level 579 garage band
def l579_bg(c, d):
    room(c, (170, 170, 176), (162, 162, 170), (120, 120, 126), (110, 110, 116), floor_y=470)
    # roll-up door frame (back) half open
    piece(c, RRect(260, 30, 640, 300, 2), (190, 194, 204), border=1.5, shadow=PROP)
    for y in range(40, 200, 14):
        flat(c, Thick(270, y, 630, y, 3), (170, 174, 186))
    c.rect(270, 200, 630, 300, (130, 186, 230))
    flat(c, RRect(270, 270, 630, 300, 0), (120, 170, 100))
    tree_round(c, 340, 290, s=1.0)
    # pegboard with tools (left) + posters (right)
    piece(c, RRect(20, 60, 230, 240, 3), (210, 170, 120), border=1.2, shadow=PROP)
    for k, (x, col) in enumerate(((50, (150, 150, 160)), (90, (220, 60, 60)), (130, (150, 150, 160)), (170, (60, 110, 200)), (200, (250, 190, 60)))):
        flat(c, [Thick(x, 90, x, 190, 6), Circ(x, 86, 9)], col)
    for k, (x, y, col) in enumerate(((680, 60, (240, 80, 120)), (790, 80, (250, 200, 60)), (700, 190, (90, 160, 230)))):
        if k == 1 and "poster" in d:
            col = (120, 200, 120)
        piece(c, RRect(x, y, x + 90, y + 110, 2), col, border=1.2, shadow=PROP)
        flat(c, [Circ(x + 45, y + 44, 20), RRect(x + 16, y + 80, x + 74, y + 92, 2)], (40, 40, 50))
    # bike hanging on the wall
    for wx in (760, 860):
        c.ellipse_ring(wx, 360, 30, 30, 4, (40, 40, 46))
    flat(c, [Thick(760, 360, 790, 320, 4), Thick(790, 320, 840, 320, 4), Thick(840, 320, 860, 360, 4), Thick(790, 320, 800, 360, 4)],
         (60, 160, 120) if "bike" not in d else (220, 80, 80))
    # amps + drum kit + band
    for k, x in enumerate((60, 590)):
        piece(c, RRect(x, 380, x + 110, 480, 4), (40, 40, 46) if not (k == 1 and "amp" in d) else (150, 60, 50), border=1.5, border_col=(120, 120, 130), shadow=PROP)
        flat(c, RRect(x + 10, 400, x + 100, 470, 3), (70, 70, 80))
        flat(c, [Circ(x + 18 + j * 12, 390, 3) for j in range(7)], (250, 220, 120))
    piece(c, Ell(450, 470, 56, 42), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, Ell(450, 470, 46, 34), (200, 50, 60))
    for x in (380, 520):
        piece(c, [Ell(x, 420, 26, 9), RRect(x - 26, 420, x + 26, 446, 3)], (250, 250, 250), border=1.2, shadow=PROP)
        flat(c, Thick(x, 446, x, 520, 3), (180, 180, 190))
    flat(c, Thick(560, 340, 560, 520, 3), (180, 180, 190))
    flat(c, Ell(560, 340, 34, 6), (230, 200, 80))
    modern(c, 450, 430, (40, 40, 50), bottom=(40, 40, 50), hair=(220, 120, 60), h=1.6)
    modern(c, 200, 600, (220, 60, 90), bottom=(40, 40, 60), hair=(40, 30, 30), h=2.4)
    guitar(c, 210, 490, (60, 110, 200), s=0.9)
    modern(c, 680, 600, (90, 160, 120), bottom=(40, 40, 60), hair=(220, 180, 90), h=2.4, style="long")
    guitar(c, 690, 490, (240, 200, 60), s=0.9)
    # paint cans + old sofa
    piece(c, [RRect(820, 520, 870, 570, 4)], (240, 120, 60) if "can" not in d else (120, 120, 220), border=1.2, shadow=PROP)
    piece(c, [RRect(320, 540, 380, 600, 4)], (90, 150, 210), border=1.2, shadow=PROP)
    piece(c, [RRect(20, 510, 140, 600, 10)], (150, 110, 80) if "sofa" not in d else (90, 140, 110), border=1.5, shadow=PROP)


L579_ELEMENTS = [
    E("notes", lambda c, m: [flat(c, [Circ(260 + k * 24, 360 - k * 14, 5), Thick(264 + k * 24, 360 - k * 14, 264 + k * 24, 340 - k * 14, 2)], (255, 230, 140))
                             for k in range(3)], daynight="untinted", anim=dict(driftVelocity=(10, 20), driftLength=60, driftFade=True)),
    E("cymbal", lambda c, m: flat(c, Ell(560, 340, 34, 6), (230, 200, 80)), pivot=(560, 340), anim=dict(swingAngle=6, swingSpeed=2.0)),
    E("bulb", lambda c, m: (flat(c, Thick(450, 0, 450, 24, 1.4), (90, 90, 100)), piece(c, Circ(450, 32, 9), (255, 236, 160), shadow=None),
                            soft_union(c, [Circ(450, 32, 9)], (255, 230, 150), 0.5, spread=20)), pivot=(450, 0), daynight="untinted",
      anim=dict(swingAngle=5, swingSpeed=0.4)),
    E("dog", lambda c, m: piece(c, [Ell(260, 590, 22, 10), Circ(282, 578, 10), Ell(278, 568, 4, 8)], (200, 160, 110), border=1, shadow=SMALL), pivot=(260, 598),
      anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
]

L579_DIFFS = [
    ("poster", 835, 135, 0),
    ("bike", 810, 340, 0),
    ("amp", 645, 430, 0),
    ("can", 845, 545, 0),
    ("sofa", 80, 555, 0),
]


LEVELS = [
    ("Level570", "花鸟市场", l570_bg, L570_ELEMENTS, L570_DIFFS, 60, OPTS),
    ("Level571", "天台晾晒", l571_bg, L571_ELEMENTS, L571_DIFFS, 60, OPTS),
    ("Level572", "搬家日", l572_bg, L572_ELEMENTS, L572_DIFFS, 60, OPTS),
    ("Level573", "快递驿站", l573_bg, L573_ELEMENTS, L573_DIFFS, 60, OPTS),
    ("Level574", "广场舞", l574_bg, L574_ELEMENTS, L574_DIFFS, 60, OPTS),
    ("Level575", "幼儿园", l575_bg, L575_ELEMENTS, L575_DIFFS, 60, OPTS),
    ("Level576", "宠物美容", l576_bg, L576_ELEMENTS, L576_DIFFS, 60, OPTS),
    ("Level577", "路边烧烤摊", l577_bg, L577_ELEMENTS, L577_DIFFS, 60, dict(OPTS, day_night=DN577, anim_seconds=40.0, frames=80)),
    ("Level578", "雨天公交车厢", l578_bg, L578_ELEMENTS, L578_DIFFS, 60, OPTS),
    ("Level579", "车库乐队", l579_bg, L579_ELEMENTS, L579_DIFFS, 60, OPTS),
]
