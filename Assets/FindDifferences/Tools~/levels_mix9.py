# -*- coding: utf-8 -*-
"""Mixed themes part 9 (paper-craft shop and workshop interiors, full-bleed, original designs, no brands):
  Level315 玩具店   - a toy shop: shelves of toys, rocking horse, train on a track, kite on the wall
  Level316 古董店   - an antique shop: gramophone, grandfather clock, old globe, paintings, a cluttered counter
  Level317 甜甜圈店 - a doughnut shop: glazed rings in the case, giant doughnut sign, coffee, customers
  Level318 披萨店   - a pizzeria: brick oven with fire, chef tossing dough, checked tables, menu board
  Level319 裁缝店   - a tailor's shop: dress forms, fabric rolls, sewing machine, mirror, measuring tape
  Level320 陶艺工坊 - a pottery studio: potter's wheel, kiln, shelves of pots, glaze jars
  Level321 木工坊   - a carpentry workshop: workbench, saw, tool wall, planks, sawdust, a chair in progress
  Level322 糖果店   - a sweet shop: jars of candy, lollipop stand, scale, striped awning inside
  Level323 帽子店   - a hat shop: hat stands, hat boxes, mirror, a customer trying on a hat
  Level324 茶馆     - a traditional tea house: lattice windows, tea tables, teapots, storyteller stage
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, drift_across
from levels_akiba import modern, sign_box
from levels_homes import planks, steam
from levels_mix1 import lantern
from levels_mix2 import pot_plant, teddy, wheel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def shelf_board(c, x0, x1, y, col=(160, 110, 70)):
    piece(c, RRect(x0, y, x1, y + 12, 2), col, shadow=PROP)


def room(c, wall, floor, line, seed, y=440):
    c.rect(0, 0, W, y, wall)
    planks(c, y, floor, line, seed=seed)


# =================================================================== Level 315 toy shop
def l315_bg(c, d):
    room(c, (240, 226, 200), (190, 150, 110), (170, 130, 94), 3151)
    for x in range(0, W, 40):
        flat(c, Thick(x, 0, x, 440, 1.4), (232, 216, 188))
    # kite on the wall (left top)
    kc = (240, 90, 80) if "kite" not in d else (90, 170, 230)
    piece(c, Poly([(100, 30), (150, 90), (100, 160), (50, 90)]), kc, border=1.5, shadow=PROP)
    flat(c, [Poly([(100, 30), (150, 90), (100, 90)]), Poly([(100, 160), (50, 90), (100, 90)])], (250, 210, 70))
    # shelves with toys
    for y in (130, 250):
        shelf_board(c, 260, 640, y)
    for k, x in enumerate(range(290, 640, 70)):
        col = [(220, 60, 60), (60, 120, 200), (250, 200, 60), (90, 170, 90), (200, 110, 200)][k]
        if k == 2 and "block" in d:
            col = (240, 140, 60)
        piece(c, [RRect(x - 20, 90, x + 20, 130, 3)], col, border=1.2, shadow=SMALL)
        flat(c, Poly(star_pts(x, 110, 10, 4)), (250, 250, 246))
    teddy(c, 320, 250, 1.1, (200, 150, 90), (220, 60, 70))
    piece(c, [Circ(430, 226, 22)], (240, 90, 80) if "ball" not in d else (90, 200, 120), border=1.2, shadow=SMALL)
    flat(c, Thick(410, 226, 450, 226, 4), (250, 250, 246))
    piece(c, [RRect(500, 200, 590, 240, 4), RRect(560, 180, 590, 202, 3)], (60, 140, 200), border=1.2, shadow=SMALL)
    for x in (515, 575):
        wheel(c, x, 244, 9, tyre=(40, 40, 46), hub=(200, 200, 210))
    # robot toy + rocket (right shelf)
    shelf_board(c, 690, 880, 200)
    rob = (180, 186, 196) if "robot" not in d else (250, 200, 60)
    piece(c, [RRect(710, 140, 760, 200, 4), RRect(718, 110, 752, 140, 4)], rob, border=1.2, shadow=SMALL)
    flat(c, [Circ(728, 124, 4), Circ(744, 124, 4)], (90, 200, 240))
    piece(c, [RRect(810, 120, 840, 196, 12), Poly([(810, 130), (840, 130), (825, 96)]), Poly([(800, 196), (812, 170), (812, 196)]), Poly([(850, 196), (838, 170), (838, 196)])],
          (240, 240, 236), border=1.2, shadow=SMALL)
    flat(c, Circ(825, 146, 7), (220, 60, 60))
    # counter + shopkeeper (right)
    modern(c, 790, 400, (220, 120, 160), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.0, style="long")
    piece(c, RRect(680, 380, 900, 470, 3), (200, 150, 100), border=1.5, shadow=PROP)
    piece(c, [RRect(700, 350, 760, 382, 4)], (60, 60, 70), border=1.2, shadow=SMALL)
    # rocking horse (left front)
    rh = (240, 240, 236) if "horse" not in d else (200, 140, 90)
    piece(c, [Poly([(40, 590)] + [(130 + 100 * math.cos(math.pi * k / 10), 560 + 26 * math.sin(math.pi * k / 10)) for k in range(11)] + [(230, 590)])], (180, 60, 60),
          border=1.2, shadow=PROP)
    piece(c, [Ell(130, 500, 60, 24), Poly([(176, 494), (210, 440), (230, 452), (196, 504)]), Ell(222, 446, 20, 12)], rh, border=1.5, shadow=PROP)
    flat(c, [Thick(90, 520, 80, 562, 6), Thick(170, 520, 180, 562, 6)], rh)
    flat(c, [Poly([(196, 446), (206, 420), (214, 450)])], (200, 140, 60))
    flat(c, Circ(226, 442, 2.4), INK)
    # train track (centre front)
    c.ellipse_ring(470, 560, 140, 30, 6, (150, 110, 70))
    train = (220, 60, 60) if "train" not in d else (60, 160, 120)
    piece(c, [RRect(420, 556, 500, 590, 4), RRect(470, 530, 500, 558, 3), RRect(426, 538, 440, 558, 2)], train, border=1.2, shadow=SMALL)
    for x in (436, 486):
        wheel(c, x, 592, 8, tyre=(40, 40, 46), hub=(250, 200, 60))
    # child (centre)
    modern(c, 600, 590, (90, 160, 220), bottom=(60, 60, 80), hair=(200, 160, 90), h=2.2, style="twin")


L315_ELEMENTS = [
    E("spin", lambda c, m: [piece(c, Poly([(380, 384), (420, 384), (400, 420)]), (250, 200, 60), shadow=None),
                            flat(c, Thick(400, 384, 400, 370, 3), (220, 60, 60))], pivot=(400, 402), anim=dict(stretch=(0.7, 0), scaleSpeed=3.0)),
    E("bob", lambda c, m: piece(c, Circ(880, 60, 16), (240, 120, 160), shadow=SMALL), pivot=(880, 100), anim=dict(swingAngle=8, swingSpeed=0.6)),
]

L315_DIFFS = [
    ("kite", 100, 95, 0),
    ("block", 430, 110, 0),
    ("ball", 430, 226, 0),
    ("robot", 735, 150, 0),
    ("horse", 160, 480, 0),
    ("train", 460, 565, 0),
]


# =================================================================== Level 316 antique shop
def l316_bg(c, d):
    room(c, (110, 80, 70), (120, 84, 60), (104, 70, 50), 3161)
    for x in range(0, W, 30):
        flat(c, Thick(x, 0, x, 440, 1.2), (102, 74, 64))
    # paintings
    for x0, y0, w, h, art, key in ((30, 40, 160, 110, (120, 160, 120), "painting"), (220, 60, 110, 80, (200, 170, 120), None), (640, 40, 130, 100, (120, 140, 190), None)):
        fr = (200, 160, 70)
        piece(c, RRect(x0, y0, x0 + w, y0 + h, 3), fr, border=1.5, shadow=PROP)
        a = art if not (key and key in d) else (200, 90, 90)
        flat(c, RRect(x0 + 10, y0 + 10, x0 + w - 10, y0 + h - 10, 2), a)
        flat(c, Circ(x0 + w * 0.65, y0 + h * 0.4, h * 0.14), lit(a, 1.3))
    # long-case clock (right)
    piece(c, [RRect(800, 60, 880, 120, 4), RRect(810, 120, 870, 420, 2), RRect(800, 410, 880, 440, 2)], (90, 56, 40), border=1.5, shadow=PROP)
    flat(c, Circ(840, 90, 22), (250, 246, 232))
    flat(c, RRect(822, 150, 858, 380, 4), (50, 34, 26))
    # globe on a stand (centre)
    gl = (120, 170, 200) if "globe" not in d else (220, 190, 120)
    flat(c, [Thick(450, 300, 450, 360, 4), Thick(420, 380, 480, 380, 5)], (150, 110, 70))
    piece(c, Circ(450, 250, 46), gl, border=1.5, shadow=PROP)
    flat(c, [Ell(436, 236, 18, 12), Ell(466, 270, 14, 9)], (150, 170, 110))
    c.ellipse_ring(450, 250, 52, 52, 3, (200, 160, 70), ymin=200)
    # gramophone (left middle)
    piece(c, RRect(60, 320, 180, 370, 3), (110, 70, 50), border=1.5, shadow=PROP)
    gr = (220, 180, 70) if "horn" not in d else (90, 140, 120)
    piece(c, [Poly([(130, 320), (140, 280), (220, 200), (240, 250), (150, 300)])], gr, border=1.5, shadow=PROP)
    flat(c, Ell(230, 226, 14, 28), lit(gr, 0.7))
    # counter with curios (front)
    piece(c, RRect(260, 460, 760, 560, 3), (100, 66, 48), border=1.5, shadow=PROP)
    flat(c, RRect(270, 470, 750, 500, 2), (200, 220, 220))
    piece(c, Poly([(300, 460), (340, 460), (330, 420), (310, 420)]), (90, 140, 120), border=1, shadow=SMALL)
    vase = (240, 236, 226) if "vase" not in d else (60, 90, 180)
    piece(c, [Ell(400, 436, 20, 26), RRect(392, 400, 408, 414, 2)], vase, border=1.2, shadow=SMALL)
    flat(c, Thick(384, 436, 416, 436, 4), (60, 90, 160) if "vase" not in d else (240, 236, 226))
    piece(c, [Ell(540, 450, 30, 10), RRect(528, 420, 552, 452, 3)], (200, 200, 210), border=1.2, shadow=SMALL)
    cam = (40, 40, 46) if "camera" not in d else (150, 100, 60)
    piece(c, [RRect(620, 416, 690, 458, 4), RRect(640, 404, 670, 418, 2)], cam, border=1.2, shadow=SMALL)
    flat(c, Circ(655, 437, 12), (150, 150, 160))
    # shopkeeper with spectacles
    modern(c, 520, 460, (90, 110, 90), bottom=(50, 50, 60), hair=(200, 200, 200), h=1.6, glasses=True)
    # trunk (left front)
    tr = (60, 90, 120) if "trunk" not in d else (150, 60, 50)
    piece(c, [RRect(40, 500, 220, 590, 6)], tr, border=1.5, shadow=PROP)
    flat(c, [Thick(40, 530, 220, 530, 5), Thick(90, 500, 90, 590, 6), Thick(170, 500, 170, 590, 6)], (180, 150, 80))
    # cat on a chair (right front)
    piece(c, [RRect(780, 520, 880, 540, 3), RRect(784, 450, 876, 522, 6), Thick(790, 540, 786, 596, 4), Thick(870, 540, 874, 596, 4)], (140, 60, 60), border=1.2, shadow=PROP)
    piece(c, [Ell(830, 510, 30, 12), Circ(856, 498, 10)], (240, 160, 70), border=1, shadow=None)


L316_ELEMENTS = [
    E("pend", lambda c, m: [flat(c, Thick(840, 160, 840, 330, 2), (200, 170, 70)), piece(c, Circ(840, 340, 12), (220, 190, 80), shadow=None)], pivot=(840, 160),
      anim=dict(swingAngle=14, swingSpeed=0.8)),
    E("dust", lambda c, m: soft_union(c, [Poly([(560, 0), (620, 0), (500, 440), (380, 440)])], (255, 240, 200), 0.1, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.5)),
    E("spin", lambda c, m: c.ellipse_ring(110, 320, 34, 6, 3, (40, 40, 46)), pivot=(110, 320), anim=dict(stretch=(0.2, 0), scaleSpeed=2.0)),
]

L316_DIFFS = [
    ("painting", 110, 95, 0),
    ("globe", 450, 250, 0),
    ("horn", 190, 260, 0),
    ("vase", 400, 426, 0),
    ("camera", 655, 435, 0),
    ("trunk", 130, 545, 0),
]


# =================================================================== Level 317 doughnut shop
def donut(c, x, y, r, dough, icing, sprinkles=True):
    piece(c, Circ(x, y, r), dough, border=1, shadow=SMALL)
    flat(c, Circ(x, y - r * 0.1, r * 0.85), icing)
    flat(c, Circ(x, y - r * 0.1, r * 0.3), dough)
    if sprinkles:
        rnd = random.Random(int(x * 7 + y))
        for _ in range(6):
            a, rr = rnd.uniform(0, 6.28), rnd.uniform(r * 0.45, r * 0.75)
            flat(c, Thick(x + rr * math.cos(a), y + rr * math.sin(a), x + rr * math.cos(a) + 3, y + rr * math.sin(a) + 2, 1.6),
                 rnd.choice([(250, 250, 246), (90, 160, 230), (250, 210, 70)]))


def l317_bg(c, d):
    for k, x in enumerate(range(0, W, 45)):
        flat(c, RRect(x, 0, x + 45, 440, 0), (250, 230, 236) if k % 2 else (250, 244, 240))
    # giant doughnut sign (centre top)
    donut(c, 450, 110, 70, (220, 170, 100), (240, 120, 170) if "sign" not in d else (120, 90, 60))
    # menu (left top)
    piece(c, RRect(30, 40, 230, 200, 4), (60, 60, 70), border=1.5, shadow=PROP)
    for k in range(5):
        flat(c, Thick(50, 70 + k * 26, 170, 70 + k * 26, 2), (240, 240, 230))
        flat(c, Thick(186, 70 + k * 26, 214, 70 + k * 26, 2), (250, 200, 120))
    # coffee machine (right top)
    cm = (60, 60, 70) if "coffee" not in d else (200, 70, 60)
    piece(c, [RRect(700, 100, 840, 210, 6)], cm, border=1.5, shadow=PROP)
    flat(c, [RRect(720, 120, 820, 150, 3)], (200, 210, 220))
    piece(c, [RRect(740, 180, 770, 208, 3), RRect(780, 180, 810, 208, 3)], (250, 250, 246), shadow=None)
    # display case
    piece(c, RRect(60, 250, 840, 420, 4), (240, 244, 248), border=1.5, shadow=PROP)
    for y in (300, 370):
        flat(c, Thick(70, y + 30, 830, y + 30, 3), (200, 210, 220))
    cols = [(240, 120, 170), (120, 80, 50), (250, 250, 246), (250, 210, 80), (140, 200, 230), (180, 120, 200)]
    for r, y in enumerate((300, 370)):
        for k, x in enumerate(range(110, 820, 75)):
            ic = cols[(k + r * 3) % 6]
            if r == 0 and k == 3 and "glaze" in d:
                ic = (90, 200, 120)
            donut(c, x, y, 24, (220, 170, 100), ic, sprinkles=(k + r) % 2 == 0)
    # counter + floor
    piece(c, RRect(0, 420, W, 470, 0), (240, 140, 160), shadow=LAYER)
    c.rect(0, 470, W, H, (240, 236, 230))
    for x in range(0, W, 40):
        for y in range(470, H, 40):
            if (x // 40 + y // 40) % 2:
                flat(c, RRect(x, y, x + 40, y + 40, 0), (220, 120, 140))
    # customers
    hx, hy = modern(c, 200, 600, (90, 140, 200), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.5)
    box = (250, 220, 230) if "box" not in d else (150, 210, 240)
    piece(c, RRect(230, 500, 300, 540, 3), box, border=1.2, shadow=SMALL)
    flat(c, Thick(230, 520, 300, 520, 3), (240, 120, 170))
    modern(c, 500, 600, (250, 200, 70), bottom=(60, 70, 100), hair=(200, 160, 90), h=2.3, style="twin")
    # table with coffee cups (right front)
    piece(c, [Ell(760, 520, 80, 14), RRect(754, 520, 766, 596, 2)], (250, 250, 246), border=1.2, shadow=PROP)
    cup = (250, 250, 246) if "cup" not in d else (90, 160, 220)
    piece(c, [RRect(720, 486, 752, 514, 4), Ell(736, 516, 22, 4)], cup, border=1, shadow=SMALL)
    donut(c, 800, 500, 18, (220, 170, 100), (120, 80, 50), sprinkles=False)
    # balloon (left front)
    if "balloon" not in d:
        flat(c, Thick(60, 600, 70, 480, 1.2), (90, 90, 100))
        piece(c, Ell(70, 460, 24, 30), (240, 120, 170), border=1.2, shadow=SMALL)


L317_ELEMENTS = steam("stm", 736, 480, n=3) + [
    E("twirl", lambda c, m: flat(c, Poly(star_pts(450, 30, 10, 4)), (255, 250, 220)), pivot=(450, 30), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.0)),
    E("cashier", lambda c, m: modern(c, 600, 250, (250, 250, 246), bottom=(60, 60, 70), hair=(90, 60, 40), h=1.6), pivot=(600, 250),
      anim=dict(bobAmplitude=(30, 0), bobSpeed=0.12)),
]

L317_DIFFS = [
    ("sign", 450, 110, 0),
    ("coffee", 770, 150, 0),
    ("glaze", 335, 300, 0),
    ("box", 265, 520, 0),
    ("cup", 736, 500, 0),
    ("balloon", 70, 470, 0),
]


# =================================================================== Level 318 pizzeria
def l318_bg(c, d):
    room(c, (240, 230, 210), (170, 120, 80), (150, 104, 70), 3181)
    flat(c, RRect(0, 300, W, 440, 0), (230, 220, 200))
    for x in range(0, W, 30):
        for y in range(300, 440, 30):
            if (x // 30 + y // 30) % 2:
                flat(c, RRect(x, y, x + 30, y + 30, 0), (60, 130, 90))
    # brick oven (left)
    piece(c, [RRect(30, 100, 330, 440, 4)], (190, 90, 60), border=1.5, shadow=PROP)
    for r, y in enumerate(range(110, 440, 22)):
        for x in range(30 + (r % 2) * 20, 300, 40):
            flat(c, RRect(x + 2, y + 2, x + 38, y + 20, 2), (200, 100, 70))
    flat(c, Poly([(90, 330)] + [(180 + 90 * math.cos(math.pi * k / 12), 330 - 90 * math.sin(math.pi * k / 12)) for k in range(12, -1, -1)] + [(270, 330)]), (40, 30, 30))
    piece(c, RRect(60, 330, 300, 350, 2), (160, 160, 166), shadow=SMALL)
    flat(c, [Thick(130, 40, 130, 100, 30), RRect(110, 30, 150, 44, 2)], (150, 150, 160))
    # menu board (centre top)
    mb = (60, 60, 70) if "menu" not in d else (130, 70, 50)
    piece(c, RRect(380, 40, 620, 200, 4), mb, border=1.5, shadow=PROP)
    flat(c, Circ(430, 90, 26), (240, 190, 90))
    flat(c, [Circ(422, 84, 5), Circ(440, 96, 5), Circ(428, 100, 4)], (200, 60, 50))
    for k in range(4):
        flat(c, Thick(480, 70 + k * 30, 600, 70 + k * 30, 2), (240, 240, 230))
    # hanging garlic + herbs (right top)
    flat(c, Thick(680, 40, 880, 40, 3), (110, 80, 60))
    for k, x in enumerate((700, 760, 820, 870)):
        col = [(250, 246, 230), (90, 150, 80), (200, 60, 50), (90, 150, 80)][k]
        if k == 2 and "pepper" in d:
            col = (250, 200, 60)
        flat(c, Thick(x, 40, x, 70, 2), (110, 80, 60))
        piece(c, [Ell(x, 90, 14, 22)], col, border=1, shadow=SMALL)
    # chef tossing dough (centre)
    hx, hy = modern(c, 520, 430, (250, 250, 246), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.4)
    hat = (250, 250, 246) if "hat" not in d else (220, 60, 50)
    piece(c, [RRect(hx - 14, hy - 22, hx + 14, hy - 8, 3), Circ(hx - 8, hy - 26, 9), Circ(hx + 8, hy - 26, 9), Circ(hx, hy - 30, 9)], hat, border=1, shadow=SMALL)
    piece(c, RRect(380, 410, 700, 440, 2), (200, 170, 130), border=1.2, shadow=PROP)
    # tables with checked cloths (front)
    for x0, key in ((60, "cloth"), (600, None)):
        cc = (220, 60, 60) if not (key and key in d) else (60, 110, 190)
        piece(c, Poly([(x0, 500), (x0 + 240, 500), (x0 + 250, 560), (x0 - 10, 560)]), (250, 250, 246), border=1.2, shadow=PROP)
        for k in range(6):
            flat(c, Thick(x0 + 20 + k * 40, 502, x0 + 16 + k * 42, 558, 8), cc)
        flat(c, [RRect(x0 + 10, 560, x0 + 20, 600, 2), RRect(x0 + 220, 560, x0 + 230, 600, 2)], (110, 80, 60))
    # pizza on table
    pz = (240, 190, 90)
    piece(c, Circ(180, 486, 34), pz, border=1.2, shadow=SMALL)
    top = (200, 60, 50) if "pizza" not in d else (90, 150, 80)
    flat(c, [Circ(168, 478, 6), Circ(192, 482, 6), Circ(176, 498, 6), Circ(196, 498, 5)], top)
    # bottle + glasses on right table
    bot = (60, 120, 70) if "bottle" not in d else (150, 60, 90)
    piece(c, [RRect(700, 446, 726, 498, 6), RRect(706, 430, 720, 448, 2)], bot, border=1.2, shadow=SMALL)
    modern(c, 860, 600, (90, 120, 160), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.4)


L318_ELEMENTS = [
    E("fire", lambda c, m: [flat(c, Poly([(120, 330), (240, 330), (210, 270), (180, 290), (150, 264)]), (250, 140, 40)),
                            flat(c, Poly([(150, 330), (210, 330), (190, 290), (170, 300)]), (255, 220, 110))], pivot=(180, 330), daynight="untinted",
      anim=dict(stretch=(0.1, 0.3), scaleSpeed=4)),
    E("dough", lambda c, m: piece(c, Ell(610, 236, 34, 10), (250, 236, 200), shadow=SMALL), pivot=(610, 236), anim=dict(bobAmplitude=(0, 18), bobSpeed=0.8)),
] + steam("stm", 180, 450, n=3, r=7)

L318_DIFFS = [
    ("menu", 500, 120, 0),
    ("pepper", 820, 90, 0),
    ("hat", 522, 296, 0),
    ("cloth", 180, 530, 0),
    ("pizza", 182, 488, 0),
    ("bottle", 713, 466, 0),
]


# =================================================================== Level 319 tailor's shop
def dress_form(c, x, base, s, col):
    flat(c, [Thick(x, base, x, base - 50 * s, 3), Thick(x - 20 * s, base, x + 20 * s, base, 3)], (120, 90, 60))
    piece(c, Poly([(x - 22 * s, base - 50 * s), (x + 22 * s, base - 50 * s), (x + 30 * s, base - 70 * s), (x + 18 * s, base - 110 * s), (x + 24 * s, base - 140 * s),
                   (x - 24 * s, base - 140 * s), (x - 18 * s, base - 110 * s), (x - 30 * s, base - 70 * s)]), col, border=1.5, shadow=PROP)
    flat(c, RRect(x - 6 * s, base - 152 * s, x + 6 * s, base - 140 * s, 2), (120, 90, 60))


def l319_bg(c, d):
    room(c, (230, 220, 236), (180, 140, 100), (160, 120, 84), 3191)
    for x in range(0, W, 50):
        flat(c, [Thick(x, 0, x, 440, 6)], (224, 212, 230))
    # fabric rolls on wall shelves (left)
    for y in (140, 260):
        shelf_board(c, 20, 330, y)
    for r, y in enumerate((140, 260)):
        for k, x in enumerate(range(45, 330, 48)):
            col = [(200, 60, 80), (60, 110, 180), (250, 200, 70), (90, 160, 110), (220, 160, 200), (120, 90, 70)][(k + r * 2) % 6]
            if r == 1 and k == 2 and "fabric" in d:
                col = (250, 250, 246)
            piece(c, RRect(x - 20, y - 70, x + 20, y, 4), col, border=1.2, shadow=SMALL)
            flat(c, Thick(x - 20, y - 60, x + 20, y - 60, 2), lit(col, 0.8))
    # mirror (right)
    fr = (200, 160, 70) if "mirror" not in d else (60, 60, 70)
    piece(c, Ell(780, 220, 80, 150), fr, border=1.5, shadow=PROP)
    flat(c, Ell(780, 220, 66, 136), (210, 226, 236))
    flat(c, [Thick(740, 140, 770, 190, 6)], (236, 244, 250))
    # dress forms (centre)
    dress_form(c, 440, 440, 1.6, (200, 80, 100) if "dress" not in d else (90, 160, 200))
    dress_form(c, 580, 440, 1.4, (240, 236, 226))
    flat(c, Thick(424, 260, 466, 300, 3), (250, 200, 60))
    # tape measure over the form
    tape = (250, 210, 70) if "tape" not in d else (90, 200, 120)
    flat(c, [Thick(560, 260, 580, 340, 5), Thick(600, 260, 580, 340, 5)], tape)
    # sewing table (left front)
    piece(c, [RRect(40, 470, 300, 490, 3), RRect(50, 490, 62, 596, 2), RRect(278, 490, 290, 596, 2)], (150, 100, 70), border=1.5, shadow=PROP)
    mach = (40, 40, 46) if "machine" not in d else (200, 70, 60)
    piece(c, [RRect(90, 430, 250, 470, 6), RRect(210, 380, 250, 440, 6), RRect(90, 380, 250, 400, 6), RRect(100, 400, 116, 440, 3)], mach, border=1.5, shadow=PROP)
    flat(c, [Thick(110, 388, 230, 388, 2)], (220, 200, 120))
    piece(c, Circ(250, 410, 14), (200, 200, 210), shadow=None)
    # tailor
    hx, hy = modern(c, 340, 600, (90, 90, 120), bottom=(40, 40, 50), hair=(200, 200, 200), h=2.5, glasses=True)
    # pin cushion + scissors (right front)
    piece(c, [RRect(640, 500, 880, 516, 3), RRect(650, 516, 662, 596, 2), RRect(858, 516, 870, 596, 2)], (150, 100, 70), border=1.5, shadow=PROP)
    pc = (220, 60, 60) if "cushion" not in d else (90, 140, 220)
    piece(c, Circ(700, 486, 18), pc, border=1.2, shadow=SMALL)
    for a in (-0.8, -0.3, 0.3, 0.8):
        flat(c, Thick(700, 486, 700 + 20 * math.sin(a), 466, 1.4), (200, 200, 210))
    flat(c, [Thick(760, 494, 820, 470, 3), Thick(760, 478, 820, 494, 3)], (180, 180, 190))
    c.ellipse_ring(756, 478, 7, 7, 3, (40, 40, 46))
    c.ellipse_ring(756, 496, 7, 7, 3, (40, 40, 46))
    # buttons jar
    piece(c, RRect(830, 466, 870, 500, 6), (210, 230, 240), border=1, shadow=SMALL)
    flat(c, [Circ(840, 486, 4), Circ(852, 480, 4), Circ(858, 492, 4)], (220, 90, 90))


L319_ELEMENTS = [
    E("thread", lambda c, m: flat(c, Thick(108, 400, 108, 440, 1.4), (220, 60, 80)), pivot=(108, 400), anim=dict(bobAmplitude=(0, 4), bobSpeed=3.0)),
    E("wheel", lambda c, m: flat(c, Thick(238, 410, 262, 410, 3), (90, 90, 100)), pivot=(250, 410), anim=dict(rotateSpeed=180)),
    E("glint", lambda c, m: flat(c, Thick(800, 260, 820, 300, 4), (240, 250, 255)), pivot=(810, 280), anim=dict(twinkle=0.8, twinkleSpeed=0.6)),
]

L319_DIFFS = [
    ("fabric", 141, 225, 0),
    ("mirror", 780, 220, 0),
    ("dress", 440, 330, 0),
    ("tape", 580, 300, 0),
    ("machine", 170, 420, 0),
    ("cushion", 700, 482, 0),
]


# =================================================================== Level 320 pottery studio
def pot(c, x, base, s, col, kind=0):
    if kind == 0:
        piece(c, [Ell(x, base - 20 * s, 20 * s, 20 * s), RRect(x - 8 * s, base - 48 * s, x + 8 * s, base - 34 * s, 2)], col, border=1.2, shadow=SMALL)
    elif kind == 1:
        piece(c, Poly([(x - 22 * s, base - 36 * s), (x + 22 * s, base - 36 * s), (x + 14 * s, base), (x - 14 * s, base)]), col, border=1.2, shadow=SMALL)
    else:
        piece(c, [RRect(x - 16 * s, base - 40 * s, x + 16 * s, base, 6 * s)], col, border=1.2, shadow=SMALL)


def l320_bg(c, d):
    c.rect(0, 0, W, 440, (226, 216, 200))
    c.rect(0, 440, W, H, (170, 150, 130))
    for x in range(0, W, 70):
        flat(c, Thick(x, 440, x - 40, H, 1.4), (160, 140, 120))
    # window (centre top)
    piece(c, RRect(330, 30, 570, 190, 3), (250, 250, 246), border=1.5, shadow=PROP)
    flat(c, RRect(342, 42, 558, 178, 2), (180, 214, 236))
    flat(c, [Thick(450, 42, 450, 178, 4), Thick(342, 110, 558, 110, 4)], (250, 250, 246))
    pot_plant(c, 520, 186, 1.2, (200, 120, 80) if "plant" not in d else (90, 140, 210))
    # shelves of pots (left)
    for y in (130, 250, 370):
        shelf_board(c, 20, 290, y)
    rnd = random.Random(3201)
    for r, y in enumerate((130, 250, 370)):
        for k, x in enumerate(range(50, 290, 56)):
            col = rnd.choice([(200, 120, 80), (90, 140, 170), (220, 200, 160), (150, 170, 120), (180, 90, 90)])
            if r == 1 and k == 2 and "vase" in d:
                col = (250, 210, 70)
            pot(c, x, y, 1.0, col, kind=(k + r) % 3)
    # kiln (right)
    kiln = (150, 150, 160) if "kiln" not in d else (200, 120, 90)
    piece(c, [RRect(680, 200, 870, 440, 6)], kiln, border=1.5, shadow=PROP)
    flat(c, [RRect(700, 240, 850, 400, 4)], lit(kiln, 0.85))
    flat(c, [Circ(820, 220, 8), RRect(840, 216, 860, 226, 2)], (40, 40, 46))
    flat(c, Thick(840, 300, 840, 340, 6), (60, 60, 66))
    # glaze jars on a bench (right middle)
    shelf_board(c, 600, 680, 300)
    for k, x in enumerate((616, 642, 666)):
        col = [(60, 110, 180), (90, 170, 130), (200, 80, 80)][k]
        if k == 0 and "glaze" in d:
            col = (240, 200, 60)
        piece(c, RRect(x - 10, 270, x + 10, 300, 3), col, border=1, shadow=None)
    # potter at the wheel (centre)
    piece(c, [RRect(380, 470, 520, 520, 6), RRect(440, 420, 460, 470, 2)], (90, 100, 110), border=1.5, shadow=PROP)
    hx, hy = modern(c, 330, 520, (200, 160, 120), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.3, style="long")
    apron = (60, 110, 150) if "apron" not in d else (200, 80, 90)
    piece(c, Poly([(310, 440), (350, 440), (356, 520), (304, 520)]), apron, border=1, shadow=None)
    # buckets of clay (front)
    for k, x in enumerate((640, 740)):
        col = (200, 200, 210) if not (k == 1 and "bucket" in d) else (240, 140, 60)
        piece(c, Poly([(x - 34, 590), (x + 34, 590), (x + 40, 520), (x - 40, 520)]), col, border=1.5, shadow=PROP)
        flat(c, Ell(x, 522, 38, 8), (170, 120, 90))
    # stool (left front)
    piece(c, [Ell(140, 520, 40, 10), RRect(134, 520, 146, 596, 2)], (150, 100, 70), shadow=PROP)


L320_ELEMENTS = [
    E("clay", lambda c, m: [piece(c, Poly([(426, 418), (474, 418), (466, 360), (450, 350), (434, 360)]), (200, 140, 100), border=1, shadow=None),
                            flat(c, [Thick(430, 400, 470, 396, 2), Thick(436, 380, 466, 378, 2)], (180, 120, 86))], pivot=(450, 390),
      anim=dict(stretch=(0.06, 0), scaleSpeed=3.0)),
    E("disc", lambda c, m: flat(c, Ell(450, 420, 50, 8), (120, 130, 140)), pivot=(450, 420), anim=dict(stretch=(0.04, 0), scaleSpeed=4.0)),
    E("heat", lambda c, m: soft_union(c, [RRect(700, 240, 850, 400, 4)], (255, 160, 80), 0.12, spread=16), daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.5)),
]

L320_DIFFS = [
    ("plant", 520, 160, 0),
    ("vase", 162, 226, 0),
    ("kiln", 775, 320, 0),
    ("glaze", 616, 285, 0),
    ("apron", 330, 480, 0),
    ("bucket", 740, 555, 0),
]


# =================================================================== Level 321 carpentry workshop
def l321_bg(c, d):
    c.rect(0, 0, W, 440, (200, 170, 130))
    for x in range(0, W, 36):
        flat(c, Thick(x, 0, x, 440, 2), (186, 156, 118))
    # tool wall (pegboard, left)
    piece(c, RRect(30, 40, 360, 240, 3), (220, 200, 160), border=1.5, shadow=PROP)
    for x in range(44, 350, 20):
        for y in range(54, 230, 20):
            flat(c, Circ(x, y, 2), (180, 160, 120))
    saw = (200, 200, 210) if "saw" not in d else (220, 160, 70)
    piece(c, [Poly([(60, 80), (180, 80), (180, 120), (60, 100)]), RRect(176, 74, 210, 126, 6)], saw, border=1.2, shadow=SMALL)
    flat(c, RRect(176, 74, 210, 126, 6), (180, 70, 50))
    ham = (200, 60, 50) if "hammer" not in d else (60, 110, 180)
    piece(c, [RRect(240, 70, 252, 160, 3), RRect(220, 60, 276, 82, 3)], ham, border=1.2, shadow=SMALL)
    flat(c, RRect(220, 60, 276, 82, 3), (120, 120, 130))
    for k, x in enumerate((300, 330)):
        piece(c, [RRect(x - 5, 80, x + 5, 160, 2)], [(250, 200, 60), (60, 140, 90)][k], shadow=SMALL)
        flat(c, Thick(x, 160, x, 200, 3), (170, 170, 180))
    piece(c, [RRect(60, 170, 200, 186, 2)], (200, 170, 90), shadow=SMALL)
    # window (right top)
    piece(c, RRect(620, 40, 860, 200, 3), (150, 110, 70), border=1.5, shadow=PROP)
    flat(c, RRect(632, 52, 848, 188, 2), (180, 214, 236))
    flat(c, [Thick(740, 52, 740, 188, 4), Thick(632, 120, 848, 120, 4)], (150, 110, 70))
    # clamp rack (centre)
    for k, x in enumerate((420, 470, 520)):
        col = (60, 110, 180) if not (k == 1 and "clamp" in d) else (240, 140, 50)
        piece(c, [RRect(x - 4, 60, x + 4, 200, 2), RRect(x - 16, 60, x + 4, 72, 2), RRect(x - 16, 150, x + 4, 162, 2)], col, border=1, shadow=SMALL)
    # planks leaning (right)
    for k, x in enumerate((640, 680, 720, 760)):
        col = [(220, 180, 120), (200, 150, 100), (230, 196, 140), (190, 140, 90)][k]
        piece(c, Poly([(x, 440), (x + 26, 440), (x + 60, 230), (x + 34, 230)]), col, border=1.2, shadow=PROP)
    # floor
    c.rect(0, 440, W, H, (160, 130, 96))
    rnd = random.Random(3211)
    for _ in range(50):
        x, y = rnd.uniform(0, W), rnd.uniform(450, 600)
        flat(c, Ell(x, y, 4, 2), (230, 210, 160))
    # workbench (centre)
    piece(c, [RRect(220, 420, 620, 446, 3), RRect(240, 446, 258, 590, 2), RRect(582, 446, 600, 590, 2), RRect(240, 520, 600, 532, 2)], (180, 130, 80), border=1.5,
          shadow=PROP)
    piece(c, RRect(300, 400, 520, 422, 2), (230, 200, 150), border=1.2, shadow=SMALL)
    plane = (200, 70, 50) if "plane" not in d else (90, 150, 90)
    piece(c, [RRect(460, 380, 520, 402, 4), Ell(500, 378, 10, 8)], plane, border=1.2, shadow=SMALL)
    # carpenter
    hx, hy = modern(c, 420, 420, (90, 120, 160), bottom=(60, 60, 70), hair=(90, 60, 40), h=2.0)
    flat(c, Thick(hx + 4, hy - 8, hx + 20, hy - 14, 3), (240, 200, 60))
    # chair in progress (left front)
    ch = (200, 150, 100) if "chair" not in d else (120, 160, 190)
    piece(c, [RRect(60, 500, 180, 516, 3), Thick(66, 516, 62, 596, 5), Thick(174, 516, 178, 596, 5), Thick(66, 500, 66, 410, 5), Thick(174, 500, 174, 410, 5),
              RRect(66, 420, 174, 436, 2)], ch, border=1.2, shadow=PROP)
    # toolbox (right front)
    tb = (220, 60, 50) if "toolbox" not in d else (250, 200, 60)
    piece(c, [RRect(700, 520, 840, 590, 4), Thick(740, 520, 740, 500, 3), Thick(800, 520, 800, 500, 3), Thick(740, 500, 800, 500, 3)], tb, border=1.5, shadow=PROP)


L321_ELEMENTS = [
    E("dust", lambda c, m: soft_union(c, [Poly([(632, 120), (740, 120), (560, 440), (420, 440)])], (255, 246, 220), 0.12, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.5)),
    E("shaving", lambda c, m: flat(c, Ell(530, 396, 6, 3), (240, 220, 170)), pivot=(530, 396), anim=dict(driftVelocity=(16, 30), driftLength=60, driftFade=True)),
    E("sway", lambda c, m: flat(c, Thick(860, 0, 860, 90, 1.4), (90, 80, 70)), pivot=(860, 0), anim=dict(swingAngle=4, swingSpeed=0.5)),
]

L321_DIFFS = [
    ("saw", 130, 98, 0),
    ("hammer", 246, 110, 0),
    ("clamp", 466, 130, 0),
    ("plane", 490, 390, 0),
    ("chair", 120, 500, 0),
    ("toolbox", 770, 550, 0),
]


# =================================================================== Level 322 sweet shop
def candy_jar(c, x, base, s, candy, lid=(220, 60, 60)):
    piece(c, [RRect(x - 22 * s, base - 60 * s, x + 22 * s, base, 8 * s)], (226, 240, 246), border=1.2, shadow=SMALL)
    piece(c, RRect(x - 16 * s, base - 70 * s, x + 16 * s, base - 58 * s, 3), lid, shadow=None)
    rnd = random.Random(int(x * 3 + base))
    for _ in range(9):
        flat(c, Circ(x + rnd.uniform(-14, 14) * s, base - rnd.uniform(8, 46) * s, 5 * s), candy if rnd.random() < 0.7 else lit(candy, 1.2))


def l322_bg(c, d):
    room(c, (250, 236, 220), (220, 190, 160), (200, 170, 140), 3221)
    # striped awning inside (top)
    aw = (240, 120, 160) if "awning" not in d else (90, 180, 170)
    for k, x in enumerate(range(0, W, 50)):
        col = (240, 120, 160) if not (600 <= x < 800) else aw
        flat(c, RRect(x, 0, x + 50, 50, 0), col if k % 2 else (250, 250, 246))
        piece(c, Poly([(x, 50), (x + 50, 50), (x + 25, 66)]), col if k % 2 else (250, 250, 246), shadow=None)
    # jar shelves
    for y in (180, 300, 420):
        shelf_board(c, 20, 420, y)
    cands = [(240, 80, 80), (250, 200, 60), (90, 180, 120), (120, 120, 230), (240, 140, 200), (250, 150, 60)]
    for r, y in enumerate((180, 300, 420)):
        for k, x in enumerate(range(60, 420, 75)):
            cd = cands[(k + r * 2) % 6]
            if r == 1 and k == 3 and "jar" in d:
                cd = (60, 60, 70)
            candy_jar(c, x, y, 1.0, cd)
    # lollipop stand (right)
    piece(c, [RRect(740, 300, 760, 440, 3), Ell(750, 440, 40, 8)], (200, 170, 120), border=1.2, shadow=PROP)
    for k, (x, y) in enumerate(((710, 260), (790, 250), (750, 210), (700, 320), (800, 320))):
        col = cands[k]
        if k == 2 and "lolly" in d:
            col = (250, 250, 246)
        flat(c, Thick(x, y, 750, 300, 2), (250, 250, 246))
        piece(c, Circ(x, y, 22), col, border=1.2, shadow=SMALL)
        c.ellipse_ring(x, y, 12, 12, 3, (250, 250, 246))
    # counter + scale
    piece(c, RRect(460, 440, 900, 500, 3), (240, 160, 180), border=1.5, shadow=PROP)
    sc = (200, 60, 60) if "scale" not in d else (60, 120, 200)
    piece(c, [RRect(500, 410, 600, 440, 4), Ell(550, 404, 44, 8)], sc, border=1.2, shadow=SMALL)
    flat(c, Circ(550, 424, 10), (250, 250, 246))
    # shopkeeper
    hx, hy = modern(c, 680, 440, (250, 250, 246), bottom=(60, 60, 70), hair=(200, 120, 70), h=1.9, style="long")
    # children (front)
    modern(c, 300, 600, (250, 200, 70), bottom=(60, 120, 200), hair=(40, 30, 30), h=2.1, style="twin")
    hx, hy = modern(c, 520, 600, (90, 170, 120), bottom=(60, 60, 80), hair=(200, 160, 90), h=2.2)
    bag = (240, 120, 160) if "bag" not in d else (250, 220, 90)
    piece(c, Poly([(540, 520), (580, 520), (576, 566), (544, 566)]), bag, border=1.2, shadow=SMALL)
    # gumball machine (left front)
    gm = (220, 50, 50) if "gumball" not in d else (60, 120, 200)
    piece(c, [Poly([(80, 600), (160, 600), (150, 520), (90, 520)]), RRect(96, 500, 144, 522, 3)], gm, border=1.5, shadow=PROP)
    piece(c, Circ(120, 460, 42), (226, 240, 246), border=1.5, shadow=SMALL)
    rnd = random.Random(3222)
    for _ in range(14):
        a, r = rnd.uniform(0, 6.28), rnd.uniform(0, 30)
        flat(c, Circ(120 + r * math.cos(a), 466 + r * math.sin(a) * 0.8, 6), rnd.choice(cands))


L322_ELEMENTS = [
    E("bell", lambda c, m: [flat(c, Thick(880, 66, 880, 96, 1.4), (90, 80, 70)), piece(c, Poly([(870, 110), (890, 110), (880, 94)]), (240, 200, 60), shadow=None)],
      pivot=(880, 66), anim=dict(swingAngle=12, swingSpeed=1.4)),
    E("sparkle", lambda c, m: flat(c, Poly(star_pts(760, 380, 8, 3)), (255, 255, 230)), pivot=(760, 380), daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=1.2)),
]

L322_DIFFS = [
    ("awning", 700, 33, 0),
    ("jar", 285, 260, 0),
    ("lolly", 750, 210, 0),
    ("scale", 550, 422, 0),
    ("bag", 560, 543, 0),
    ("gumball", 120, 560, 0),
]


# =================================================================== Level 323 hat shop
def hat_on_stand(c, x, base, kind, col, band=(40, 40, 46)):
    flat(c, [Thick(x, base, x, base - 60, 3), Thick(x - 18, base, x + 18, base, 4)], (150, 110, 70))
    hy = base - 64
    if kind == "top":
        piece(c, [RRect(x - 18, hy - 44, x + 18, hy, 2), Ell(x, hy, 32, 6)], col, border=1.2, shadow=SMALL)
        flat(c, RRect(x - 18, hy - 12, x + 18, hy - 4, 1), band)
    elif kind == "sun":
        piece(c, [Ell(x, hy, 46, 10), Ell(x, hy - 12, 22, 16)], col, border=1.2, shadow=SMALL)
        flat(c, Thick(x - 22, hy - 6, x + 22, hy - 6, 5), band)
    elif kind == "cap":
        piece(c, [Ell(x, hy - 8, 22, 18), RRect(x, hy - 8, x + 36, hy, 3)], col, border=1.2, shadow=SMALL)
    else:  # bowler
        piece(c, [Ell(x, hy - 14, 20, 18), Ell(x, hy, 30, 6)], col, border=1.2, shadow=SMALL)
        flat(c, RRect(x - 20, hy - 8, x + 20, hy - 2, 1), band)


def l323_bg(c, d):
    room(c, (220, 236, 230), (160, 120, 90), (140, 104, 76), 3231)
    for x in range(0, W, 60):
        flat(c, Thick(x, 0, x, 440, 3), (210, 228, 222))
    # wall shelves with hats
    for y in (150, 290):
        shelf_board(c, 20, 400, y)
    kinds = ["top", "sun", "bowler", "cap"]
    cols = [(40, 40, 46), (230, 200, 120), (120, 80, 60), (200, 60, 60), (60, 110, 160), (240, 236, 226), (150, 90, 160), (90, 140, 90)]
    for r, y in enumerate((150, 290)):
        for k, x in enumerate(range(70, 400, 90)):
            col = cols[(k + r * 4) % 8]
            if r == 0 and k == 1 and "sunhat" in d:
                col = (240, 120, 160)
            hat_on_stand(c, x, y, kinds[(k + r) % 4], col, band=(200, 60, 60) if (k + r) % 2 else (40, 40, 46))
    # mirror + customer trying a hat (centre)
    fr = (200, 160, 70) if "mirror" not in d else (60, 60, 70)
    piece(c, RRect(480, 60, 620, 400, 10), fr, border=1.5, shadow=PROP)
    flat(c, RRect(492, 72, 608, 388, 8), (210, 226, 236))
    hx, hy = modern(c, 680, 440, (200, 90, 110), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.6, style="long")
    nh = (250, 200, 70) if "newhat" not in d else (90, 160, 220)
    piece(c, [Ell(hx, hy - 10, 30, 7), Ell(hx, hy - 20, 16, 12)], nh, border=1.2, shadow=SMALL)
    flat(c, Thick(hx - 16, hy - 14, hx + 16, hy - 14, 4), (200, 60, 60))
    # hat boxes (right)
    for k, (x, y, r) in enumerate(((820, 440, 50), (810, 360, 42), (826, 290, 34))):
        col = [(240, 140, 160), (120, 180, 200), (250, 220, 120)][k]
        if k == 1 and "box" in d:
            col = (150, 110, 190)
        piece(c, [RRect(x - r, y - r * 1.4, x + r, y, 4), Ell(x, y - r * 1.4, r, 8)], col, border=1.5, shadow=PROP)
        flat(c, Thick(x - r, y - r * 0.7, x + r, y - r * 0.7, 4), (250, 250, 246))
    # counter + shopkeeper (left front)
    piece(c, RRect(40, 470, 360, 560, 3), (150, 110, 80), border=1.5, shadow=PROP)
    hx, hy = modern(c, 200, 470, (90, 90, 120), bottom=(40, 40, 50), hair=(200, 200, 200), h=1.8, glasses=True)
    tape = (250, 210, 70) if "tape" not in d else (220, 80, 80)
    flat(c, [Thick(186, 410, 194, 450, 4), Thick(214, 410, 206, 450, 4)], tape)
    # umbrella stand (centre front)
    piece(c, [RRect(440, 520, 500, 596, 4)], (90, 90, 110), border=1.5, shadow=PROP)
    um = (60, 60, 70) if "umbrella" not in d else (220, 80, 60)
    piece(c, [Thick(456, 520, 444, 440, 3), Poly([(440, 520), (470, 520), (452, 460)])], um, border=1, shadow=SMALL)
    piece(c, [Thick(486, 520, 500, 450, 3)], (200, 60, 60), shadow=SMALL)


L323_ELEMENTS = [
    E("glint", lambda c, m: flat(c, Thick(520, 120, 560, 180, 5), (236, 244, 250)), pivot=(540, 150), anim=dict(twinkle=0.8, twinkleSpeed=0.6)),
    E("feather", lambda c, m: flat(c, Ell(712, 370, 4, 14), (240, 240, 236)), pivot=(712, 384), anim=dict(swingAngle=14, swingSpeed=1.0)),
    E("fan", lambda c, m: [flat(c, Thick(450, 20, 450 + 50 * math.cos(a), 20 + 8 * math.sin(a), 6), (200, 210, 206)) for a in (0, 2.09, 4.19)], pivot=(450, 20),
      anim=dict(stretch=(0.6, 0), scaleSpeed=2.0)),
]

L323_DIFFS = [
    ("sunhat", 160, 80, 0),
    ("mirror", 550, 230, 0),
    ("newhat", 682, 300, 0),
    ("box", 810, 330, 0),
    ("tape", 200, 430, 0),
    ("umbrella", 455, 490, 0),
]


# =================================================================== Level 324 tea house
def teapot(c, x, base, s, col):
    piece(c, [Ell(x, base - 16 * s, 22 * s, 16 * s), Thick(x + 20 * s, base - 18 * s, x + 34 * s, base - 30 * s, 4 * s), RRect(x - 6 * s, base - 36 * s, x + 6 * s, base - 30 * s, 2)],
          col, border=1.2, shadow=SMALL)
    c.ellipse_ring(x - 22 * s, base - 18 * s, 7 * s, 9 * s, 3 * s, col)


def l324_bg(c, d):
    c.rect(0, 0, W, 440, (200, 170, 130))
    flat(c, RRect(0, 0, W, 40, 0), (120, 70, 50))
    # lattice windows
    for x0 in (40, 640):
        piece(c, RRect(x0, 70, x0 + 220, 280, 3), (130, 80, 50), border=1.5, shadow=PROP)
        flat(c, RRect(x0 + 10, 80, x0 + 210, 270, 2), (240, 230, 200))
        for k in range(1, 6):
            flat(c, Thick(x0 + 10 + k * 33, 80, x0 + 10 + k * 33, 270, 3), (130, 80, 50))
            flat(c, Thick(x0 + 10, 80 + k * 32, x0 + 210, 80 + k * 32, 3), (130, 80, 50))
    # storyteller's stage (centre)
    piece(c, RRect(330, 280, 570, 330, 2), (150, 90, 60), border=1.5, shadow=PROP)
    scroll = (240, 230, 200) if "scroll" not in d else (220, 120, 90)
    piece(c, RRect(390, 60, 510, 220, 2), scroll, border=1.2, shadow=PROP)
    for k in range(4):
        flat(c, Thick(420 + k * 20, 80, 420 + k * 20, 200, 3), (60, 50, 50))
    flat(c, [RRect(384, 54, 516, 62, 2), RRect(384, 218, 516, 226, 2)], (120, 70, 50))
    hx, hy = modern(c, 450, 290, (90, 60, 120), bottom=(60, 50, 60), hair=(200, 200, 200), h=1.8)
    fan = (250, 240, 200) if "fan" not in d else (220, 80, 80)
    piece(c, Poly([(474, 240), (510, 210), (520, 240)]), fan, border=1, shadow=None)
    piece(c, RRect(400, 260, 500, 282, 2), (200, 60, 50), shadow=SMALL)
    # red lanterns
    for k, x in enumerate((300, 600)):
        col = (220, 50, 40) if not (k == 1 and "lantern" in d) else (250, 210, 80)
        flat(c, Thick(x, 40, x, 70, 1.4), (60, 50, 50))
        lantern(c, x, 92, 1.6, col)
    # floor
    c.rect(0, 440, W, H, (150, 110, 80))
    planks(c, 440, (150, 110, 80), (130, 94, 66), seed=3241)
    flat(c, RRect(0, 330, W, 440, 0), (190, 160, 120))
    # tea tables with guests
    for x0, pcol, key in ((120, (90, 140, 120), "teapot"), (450, (180, 90, 60), None), (780, (230, 230, 220), None)):
        piece(c, [RRect(x0 - 90, 420, x0 + 90, 440, 3), RRect(x0 - 80, 440, x0 - 68, 520, 2), RRect(x0 + 68, 440, x0 + 80, 520, 2)], (110, 60, 40), border=1.5, shadow=PROP)
        teapot(c, x0, 420, 1.2, pcol if not (key and key in d) else (90, 120, 200))
        for k in (-1, 1):
            piece(c, RRect(x0 + k * 50 - 10, 404, x0 + k * 50 + 10, 420, 3), (250, 250, 246), border=1, shadow=None)
    modern(c, 40, 470, (90, 120, 160), bottom=(50, 50, 60), hair=(40, 30, 30), h=1.8)
    modern(c, 860, 470, (200, 90, 90), bottom=(50, 50, 60), hair=(30, 30, 34), h=1.8, style="long")
    # waiter with a long-spout kettle (front)
    hx, hy = modern(c, 300, 600, (250, 250, 246), bottom=(40, 40, 50), hair=(30, 30, 34), h=2.4)
    ket = (200, 160, 70) if "kettle" not in d else (150, 150, 160)
    piece(c, [Ell(340, 500, 20, 16), Thick(356, 494, 420, 456, 3)], ket, border=1.2, shadow=SMALL)
    # bird cage (right front)
    flat(c, Thick(650, 440, 650, 470, 2), (90, 80, 70))
    for k in range(-3, 4):
        flat(c, Thick(650 + k * 10, 476 + abs(k) * 3, 650 + k * 11, 560, 1.4), (200, 170, 80))
    piece(c, Ell(650, 562, 44, 8), (200, 170, 80), shadow=SMALL)
    bird = (250, 210, 60) if "bird" not in d else (90, 170, 230)
    piece(c, [Ell(650, 530, 12, 9), Circ(660, 520, 6)], bird, border=1, shadow=None)


L324_ELEMENTS = steam("stm1", 160, 392, n=2) + steam("stm2", 500, 392, n=2) + steam("stm3", 820, 392, n=2) + [
    E("pour", lambda c, m: flat(c, Thick(420, 456, 420, 470, 2), (200, 160, 90)), pivot=(420, 456), anim=dict(stretch=(0, 0.4), scaleSpeed=2.0)),
    E("tassel", lambda c, m: flat(c, Thick(300, 116, 300, 134, 3), (250, 200, 60)), pivot=(300, 116), anim=dict(swingAngle=14, swingSpeed=0.8)),
]

L324_DIFFS = [
    ("scroll", 450, 140, 0),
    ("lantern", 600, 92, 0),
    ("fan", 498, 230, 0),
    ("teapot", 120, 400, 0),
    ("kettle", 360, 490, 0),
    ("bird", 652, 526, 0),
]


LEVELS = [
    ("Level315", "玩具店", l315_bg, L315_ELEMENTS, L315_DIFFS, 60, OPTS),
    ("Level316", "古董店", l316_bg, L316_ELEMENTS, L316_DIFFS, 60, OPTS),
    ("Level317", "甜甜圈店", l317_bg, L317_ELEMENTS, L317_DIFFS, 60, OPTS),
    ("Level318", "披萨店", l318_bg, L318_ELEMENTS, L318_DIFFS, 60, OPTS),
    ("Level319", "裁缝店", l319_bg, L319_ELEMENTS, L319_DIFFS, 60, OPTS),
    ("Level320", "陶艺工坊", l320_bg, L320_ELEMENTS, L320_DIFFS, 60, OPTS),
    ("Level321", "木工坊", l321_bg, L321_ELEMENTS, L321_DIFFS, 60, OPTS),
    ("Level322", "糖果店", l322_bg, L322_ELEMENTS, L322_DIFFS, 60, OPTS),
    ("Level323", "帽子店", l323_bg, L323_ELEMENTS, L323_DIFFS, 60, OPTS),
    ("Level324", "茶馆", l324_bg, L324_ELEMENTS, L324_DIFFS, 60, OPTS),
]
