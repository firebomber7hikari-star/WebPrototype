# -*- coding: utf-8 -*-
"""Scrolling-background themes: a focus vehicle / person / animal holds still while the scenery loops past
(paper-craft, full-bleed, no real brands). Every scrolling layer repeats exactly every LOOP seconds
(speed = tile step / LOOP); the differences sit on the focus subject or on the static far background.
  Level1000 田野小火车   - a little steam train crossing farmland (horizontal)
  Level1001 海滨骑行     - a cyclist on a seaside promenade (horizontal)
  Level1002 荒野牛仔     - a cowboy galloping through the desert (horizontal)
  Level1003 热气球升空   - a hot-air balloon rising through the clouds (vertical, clouds sink)
  Level1004 深海潜航     - a submarine diving past a reef wall (vertical, scenery rises)
  Level1005 赛道飞驰     - a race car flying past the grandstand (horizontal)
  Level1006 沙漠驼队     - a camel and rider crossing dunes at sunset (horizontal)
  Level1007 跳伞         - a parachutist drifting down through the clouds (vertical, clouds rise)
  Level1008 公园小狗     - a puppy running along a park fence (horizontal)
  Level1009 云海飞行     - a biplane above a sea of clouds (horizontal)
"""
import math
import random

from fdcore import E, H, W, lit, on
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import LAYER, PROP, SMALL, bush, cloud_bg, rock, sky, spin_el, tree_pine, tree_round, palm
from fills import far_ridge, far_skyline

LOOP = 10.0
OPTS = dict(post=paper_post, anim_seconds=LOOP, frames=50)
INK = (60, 50, 55)


def hscroll(eid, unit, step, y0, y1, **kw):
    """Seamless tiles scrolling left, one loop every LOOP seconds: unit(c, m, dx) draws one period starting at x = dx."""
    ks = range(-1, int(math.ceil(W / step)) + 1)

    def d(c, m):
        for k in ks:
            unit(c, m, k * step)
    return E(eid, d, bbox=(-step - 40, y0, (max(ks) + 1) * step + 40, y1),
             anim=dict(driftVelocity=(-step / LOOP, 0), driftLength=step), **kw)


def vscroll(eid, unit, step, up=True, x0=-20, x1=W + 20, **kw):
    """Seamless tiles scrolling vertically (up or down), one loop every LOOP seconds: unit(c, m, dy) draws one period from y = dy."""
    ks = range(-1, int(math.ceil(H / step)) + 1)

    def d(c, m):
        for k in ks:
            unit(c, m, k * step)
    return E(eid, d, bbox=(x0, -step - 40, x1, (max(ks) + 1) * step + 40),
             anim=dict(driftVelocity=(0, -step / LOOP if up else step / LOOP), driftLength=step), **kw)


def focus(eid, draw, amp=(0, 3), speed=1.0, **kw):
    """The still subject: drawn above the scenery, holds the differences, only a gentle bob (loops with LOOP)."""
    return E(eid, draw, variant=True, anim=dict(bobAmplitude=amp, bobSpeed=speed), **kw)


def puff(eid, x, y, v, length, i, n=3, r=12, col=(240, 238, 236)):
    return E("%s%d" % (eid, i), lambda c, m: piece(c, Circ(x, y, r), col, shadow=SMALL),
             anim=dict(driftVelocity=v, driftLength=length, driftFade=True, driftGrow=1.4, phase=i / n))


def wheel(c, x, y, r, rim=(70, 60, 70), hub=(220, 200, 120), spokes=6):
    piece(c, Circ(x, y, r), rim, border=1.5, shadow=SMALL)
    flat(c, Circ(x, y, r * 0.72), lit(rim, 1.4))
    flat(c, [Thick(x + r * 0.7 * math.cos(a * math.pi / spokes), y + r * 0.7 * math.sin(a * math.pi / spokes),
                   x - r * 0.7 * math.cos(a * math.pi / spokes), y - r * 0.7 * math.sin(a * math.pi / spokes), 2) for a in range(spokes)], rim)
    flat(c, Circ(x, y, r * 0.25), hub)


# =================================================================== 1000 steam train through farmland
def l1000_bg(c, d):
    sky(c, (120, 184, 238), (226, 240, 248))
    if "sun" in d:
        piece(c, Circ(810, 80, 34), (250, 150, 80), border=2, shadow=PROP)
    else:
        piece(c, Poly(star_pts(810, 80, 54, 40, points=12)), (255, 196, 90), shadow=PROP)
        piece(c, Circ(810, 80, 34), (255, 224, 100), border=2, shadow=PROP)
    # a balloon hanging far away
    env = (90, 150, 220) if "balloon" in d else (230, 90, 80)
    piece(c, [Circ(140, 86, 34), Poly([(110, 100), (170, 100), (148, 136), (132, 136)])], env, border=2, shadow=PROP)
    flat(c, [Thick(134, 136, 134, 150, 1.4), Thick(146, 136, 146, 150, 1.4)], INK)
    piece(c, RRect(128, 148, 152, 166, 3), (170, 120, 80), border=1.5, shadow=SMALL)
    far_ridge(c, 290, 80, (150, 170, 205), seed=1000)
    # a windmill on the far ridge
    piece(c, RRect(462, 196, 486, 262, 2), (236, 228, 214), border=1.5, shadow=SMALL)
    piece(c, Poly([(458, 198), (474, 180), (490, 198)]), (190, 90, 80), shadow=None)
    blades = 4 if "mill" not in d else 3
    flat(c, [Thick(474, 196, 474 + 34 * math.cos(a * 2 * math.pi / blades + 0.4), 196 + 34 * math.sin(a * 2 * math.pi / blades + 0.4), 5)
             for a in range(blades)], (120, 100, 90))
    flat(c, RRect(-20, 420, W + 20, H + 20, 0), (140, 120, 96))
    flat(c, RRect(-20, 500, W + 20, H + 20, 0), (110, 170, 90))


def l1000_hills(c, m, dx):
    piece(c, Ell(dx + 120, 410, 200, 120), (120, 182, 100), shadow=LAYER)
    piece(c, Ell(dx + 340, 420, 160, 90), (100, 168, 90), shadow=LAYER)
    tree_round(c, dx + 60, 330, 0.7, (80, 150, 85))
    tree_round(c, dx + 300, 350, 0.6, (90, 160, 90))
    flat(c, [RRect(dx + 170, 330, dx + 230, 360, 3)], (230, 220, 190))
    flat(c, Poly([(dx + 164, 332), (dx + 200, 310), (dx + 236, 332)]), (180, 80, 70))


def l1000_near(c, m, dx):
    flat(c, [RRect(dx + x, 470, dx + x + 14, 484, 2) for x in range(0, 900, 36)], (100, 76, 60))
    for x in range(10, 900, 150):
        flat(c, [Thick(dx + x, 520, dx + x, 560, 5), Thick(dx + x - 20, 532, dx + x + 130, 532, 4)], (200, 170, 130))
    for x, col in ((70, (250, 210, 80)), (260, (240, 120, 150)), (480, (250, 250, 250)), (700, (250, 210, 80)), (820, (180, 140, 240))):
        flat(c, [Circ(dx + x + k * 14, 575 - (k % 2) * 8, 5) for k in range(3)], col)


def l1000_train(c, m):
    flat(c, Thick(-20, 468, W + 20, 468, 4), (90, 90, 100))
    # carriage 2 (rear) with passengers
    body2 = (70, 120, 190)
    piece(c, RRect(60, 360, 290, 450, 8), body2, border=2, shadow=PROP)
    piece(c, RRect(52, 348, 298, 364, 5), (110, 70, 60), border=1.5, shadow=None)
    for i, x in enumerate((80, 150, 220)):
        flat(c, RRect(x, 378, x + 50, 414, 5), (240, 240, 220))
        if not (i == 1 and on("rider", m)):
            piece(c, [Circ(x + 25, 398, 10), RRect(x + 12, 404, x + 38, 414, 4)], (250, 210, 170) if i != 1 else (230, 180, 140), shadow=None)
            if i == 1:
                flat(c, Ell(x + 25, 389, 12, 5), (220, 80, 70))
    # carriage 1
    body1 = (240, 190, 70) if on("car1", m) else (90, 160, 100)
    piece(c, RRect(320, 360, 540, 450, 8), body1, border=2, shadow=PROP)
    piece(c, RRect(312, 348, 548, 364, 5), (110, 70, 60), border=1.5, shadow=None)
    for x in (340, 410, 480):
        flat(c, RRect(x, 378, x + 46, 414, 5), (240, 240, 220))
    flat(c, Thick(290, 430, 320, 430, 5), (60, 50, 50))
    flat(c, Thick(540, 430, 570, 430, 5), (60, 50, 50))
    # locomotive
    piece(c, [RRect(570, 380, 820, 450, 10), RRect(570, 320, 660, 450, 6)], (200, 60, 60), border=2, shadow=PROP)
    piece(c, RRect(560, 310, 670, 326, 4), (60, 50, 60), border=1.5, shadow=None)
    flat(c, RRect(588, 336, 642, 370, 5), (250, 236, 180))
    piece(c, Ell(820, 414, 14, 26), (240, 200, 90), border=1.5, shadow=None)
    stack = (70, 70, 80)
    if on("chimney", m):
        piece(c, RRect(730, 330, 762, 382, 3), stack, border=1.5, shadow=SMALL)
    else:
        piece(c, [Poly([(722, 326), (770, 326), (756, 354), (736, 354)]), RRect(736, 350, 756, 382, 2)], stack, border=1.5, shadow=SMALL)
    piece(c, Circ(690, 376, 10), (240, 200, 90), border=1.2, shadow=None)
    for x in (100, 250, 360, 500):
        wheel(c, x, 450, 18)
    for x in (620, 700, 780):
        wheel(c, x, 446, 24, rim=(60, 60, 70), hub=(90, 150, 220) if (x == 620 and on("wheel", m)) else (240, 200, 90))
    flat(c, Thick(620, 446, 780, 446, 4), (180, 180, 190))


L1000_EL = [
    hscroll("hills", l1000_hills, 450, 260, 440),
    hscroll("near", l1000_near, 900, 460, 600),
] + [puff("smoke", 746, 316, (-70, -30), 200, i) for i in range(3)] + [
    focus("train", l1000_train, amp=(0, 1.5), speed=2.0),
]
L1000_DIFFS = [("sun", 810, 80, 0), ("balloon", 140, 100, 0), ("mill", 474, 196, 0), ("rider", 175, 396, 0),
               ("car1", 430, 400, 0), ("chimney", 746, 350, 0), ("wheel", 620, 446, 0)]


# =================================================================== 1001 seaside cyclist
def l1001_bg(c, d):
    sky(c, (110, 190, 240), (220, 240, 250))
    piece(c, Circ(700, 80, 32), (255, 224, 100) if "sun" not in d else (250, 160, 90), border=2, shadow=PROP)
    c.gradient(250, 340, (80, 170, 210), (60, 140, 190))
    flat(c, RRect(-20, 250, W + 20, 340, 0), (80, 160, 205))
    for y in (270, 300, 322):
        flat(c, [Thick(x, y, x + 40, y, 2) for x in range(-20 + y % 60, 900, 120)], (170, 220, 240))
    # far island with a lighthouse
    piece(c, Ell(130, 256, 110, 20), (120, 160, 120), shadow=LAYER)
    piece(c, Poly([(116, 250), (144, 250), (138, 170), (122, 170)]), (250, 250, 250), border=1.5, shadow=SMALL)
    band = (60, 120, 200) if "light" in d else (220, 70, 70)
    flat(c, [Poly([(120, 230), (140, 230), (139, 214), (121, 214)]), Poly([(122, 196), (138, 196), (137, 184), (123, 184)])], band)
    piece(c, Poly([(118, 170), (130, 156), (142, 170)]), band, shadow=None)
    # a far sailboat
    flat(c, Thick(800, 300, 800, 240, 2), INK)
    piece(c, Poly([(802, 244), (802, 296), (840, 296)]) if "sail" not in d else Poly([(802, 244), (802, 296), (830, 280)]),
          (250, 250, 250), border=1.2, shadow=SMALL)
    piece(c, Poly([(780, 298), (850, 298), (838, 312), (790, 312)]), (200, 90, 70), border=1.2, shadow=SMALL)
    flat(c, RRect(-20, 340, W + 20, 360, 0), (240, 220, 170))
    flat(c, RRect(-20, 430, W + 20, H + 20, 0), (110, 110, 120))
    flat(c, RRect(-20, 560, W + 20, H + 20, 0), (230, 210, 170))


def l1001_prom(c, m, dx):
    flat(c, RRect(dx - 2, 360, dx + 452, 430, 0), (220, 200, 160))
    flat(c, [Thick(dx + x, 360, dx + x, 340, 4) for x in range(0, 450, 45)] + [Thick(dx - 2, 344, dx + 452, 344, 4)], (250, 250, 250))
    palm(c, dx + 120, 420, h=180, lean=18)
    piece(c, [RRect(dx + 300, 352, dx + 312, 420, 2), Circ(dx + 306, 346, 12)], (80, 90, 110), shadow=SMALL)
    bush(c, dx + 380, 428, 0.8)


def l1001_road(c, m, dx):
    flat(c, [RRect(dx + x, 494, dx + x + 70, 502, 3) for x in (40, 340, 640)], (250, 250, 240))
    flat(c, [Circ(dx + x, 580, 4) for x in range(20, 900, 70)], (200, 180, 140))
    piece(c, Poly([(dx + 500, 590), (dx + 520, 574), (dx + 540, 590)]), (240, 140, 120), shadow=SMALL)


def l1001_cyclist(c, m):
    rim = (60, 60, 70)
    for x, hl in ((330, on("tyre", m)), (560, False)):
        c.ellipse_ring(x, 470, 62, 62, 7, (250, 150, 60) if hl else rim)
        flat(c, [Thick(x + 56 * math.cos(a * math.pi / 6), 470 + 56 * math.sin(a * math.pi / 6),
                       x - 56 * math.cos(a * math.pi / 6), 470 - 56 * math.sin(a * math.pi / 6), 1.2) for a in range(6)], (170, 170, 180))
        flat(c, Circ(x, 470, 7), (200, 200, 210))
    frame = (40, 150, 170)
    piece(c, [Thick(330, 470, 420, 470, 6), Thick(420, 470, 400, 380, 6), Thick(400, 380, 530, 390, 6), Thick(530, 390, 420, 470, 6),
              Thick(330, 470, 400, 380, 5), Thick(530, 390, 560, 470, 6), Thick(530, 390, 520, 350, 5)], frame, shadow=SMALL)
    flat(c, [Thick(500, 350, 540, 345, 5)], INK)
    piece(c, RRect(380, 368, 420, 380, 5), INK, shadow=None)
    # basket on the handlebar
    piece(c, Poly([(540, 352), (600, 352), (592, 392), (548, 392)]), (200, 160, 100), border=1.5, shadow=SMALL)
    flat(c, [Thick(548 + k * 10, 354, 552 + k * 9, 390, 1.2) for k in range(5)], (160, 120, 70))
    if on("basket", m):
        piece(c, [Circ(556, 344, 10), Circ(576, 340, 12)], (240, 120, 60), border=1.2, shadow=None)
    else:
        piece(c, Poly(star_pts(570, 334, 24, 10, points=6)), (240, 120, 160), border=1.2, shadow=None)
        flat(c, Thick(570, 334, 570, 352, 3), (80, 150, 80))
    # rider
    skin = (246, 206, 170)
    flat(c, [Thick(410, 360, 470, 420, 12), Thick(470, 420, 450, 470, 10)], (60, 80, 140))
    flat(c, [Thick(420, 360, 500, 430, 11), Thick(500, 430, 520, 470, 9)], (70, 90, 150))
    shirt = (250, 200, 70) if on("shirt", m) else (240, 90, 80)
    piece(c, Poly([(400, 368), (430, 290), (470, 280), (480, 310), (440, 372)]), shirt, border=1.5, shadow=SMALL)
    if not on("shirt", m):
        flat(c, [Thick(420 + k * 4, 340 - k * 18, 452 + k * 4, 336 - k * 16, 4) for k in range(3)], (250, 250, 250))
    piece(c, [Thick(460, 296, 520, 348, 9)], skin, shadow=None)
    piece(c, Circ(470, 250, 30), skin, border=1.5, shadow=SMALL)
    flat(c, Circ(482, 248, 3), INK)
    helmet = (90, 200, 120) if on("helmet", m) else (60, 120, 220)
    piece(c, Poly([(436, 248), (444, 220), (470, 210), (502, 222), (506, 244)]), helmet, border=1.5, shadow=None)
    flat(c, Thick(450, 222, 494, 226, 2.5), lit(helmet, 1.3))


L1001_EL = [
    hscroll("prom", l1001_prom, 450, 220, 440),
    hscroll("road", l1001_road, 900, 480, 600),
    focus("rider", l1001_cyclist, amp=(0, 2), speed=1.0),
]
L1001_DIFFS = [("sun", 700, 80, 0), ("light", 130, 200, 0), ("sail", 815, 270, 0), ("helmet", 470, 228, 0),
               ("basket", 570, 360, 0), ("tyre", 330, 470, 0), ("shirt", 440, 330, 0)]


# =================================================================== 1002 desert cowboy
def l1002_bg(c, d):
    sky(c, (100, 170, 230), (250, 226, 180))
    piece(c, Circ(160, 90, 36), (255, 226, 110), border=2, shadow=PROP)
    if "bird" not in d:
        flat(c, [Thick(770, 100, 794, 116, 5), Thick(794, 116, 818, 100, 5), Thick(812, 136, 830, 148, 5), Thick(830, 148, 848, 136, 5)], INK)
    # far mesas
    piece(c, Poly([(-20, 300), (40, 200), (240, 200), (300, 300)]), (200, 120, 90), shadow=LAYER)
    piece(c, Poly([(560, 300), (600, 230), (680, 230), (700, 300)]), (210, 130, 100), shadow=LAYER)
    if "arch" not in d:
        flat(c, Ell(130, 268, 34, 30), (240, 210, 180))
    piece(c, Poly([(700, 300), (760, 180), (880, 180), (920, 300)]), (190, 110, 80), shadow=LAYER)
    flat(c, [Thick(780, 190, 860, 190, 3), Thick(770, 220, 870, 220, 3)], (170, 96, 70))
    flat(c, RRect(-20, 300, W + 20, H + 20, 0), (232, 190, 130))
    flat(c, RRect(-20, 480, W + 20, H + 20, 0), (216, 170, 110))


def l1002_cacti(c, m, dx):
    col = (90, 150, 90)
    for x, h in ((60, 90), (300, 70)):
        piece(c, [RRect(dx + x, 400 - h, dx + x + 22, 400, 10), RRect(dx + x - 24, 400 - h * 0.7, dx + x - 10, 400 - h * 0.3, 7),
                  Thick(dx + x - 17, 400 - h * 0.35, dx + x, 400 - h * 0.35, 8), RRect(dx + x + 32, 400 - h * 0.85, dx + x + 46, 400 - h * 0.5, 7),
                  Thick(dx + x + 22, 400 - h * 0.55, dx + x + 39, 400 - h * 0.55, 8)], col, border=1.5, shadow=SMALL)
    rock(c, dx + 200, 404, 0.8, (190, 140, 110))


def l1002_near(c, m, dx):
    flat(c, [Thick(dx + x, 520 + (x % 3) * 20, dx + x + 30, 520 + (x % 3) * 20, 2) for x in range(0, 900, 70)], (190, 140, 90))
    rock(c, dx + 150, 590, 1.2, (170, 120, 100))
    piece(c, [Circ(dx + 520, 560, 18)], (180, 150, 100), shadow=SMALL)
    flat(c, [Thick(dx + 504, 552, dx + 536, 568, 1.5), Thick(dx + 504, 568, dx + 536, 552, 1.5)], (140, 110, 70))
    rock(c, dx + 760, 594, 0.9, (170, 120, 100))


def l1002_rider(c, m):
    horse = (150, 96, 64)
    dark = (90, 60, 50)
    # legs (gallop pose)
    flat(c, [Thick(310, 380, 270, 440, 12), Thick(270, 440, 250, 480, 9), Thick(350, 390, 360, 450, 12), Thick(360, 450, 340, 488, 9),
             Thick(540, 380, 600, 430, 12), Thick(600, 430, 640, 450, 9), Thick(510, 390, 520, 450, 12), Thick(520, 450, 550, 480, 9)], horse)
    tail = (240, 220, 180) if on("tail", m) else dark
    piece(c, Poly([(290, 330), (230, 350), (200, 400), (240, 380), (300, 350)]), tail, border=1.5, shadow=SMALL)
    piece(c, [Ell(420, 360, 130, 46), Poly([(520, 340), (600, 260), (630, 270), (570, 370)])], horse, border=2, shadow=PROP)
    piece(c, Poly([(590, 250), (660, 280), (670, 300), (650, 306), (600, 290)]), horse, border=2, shadow=None)
    flat(c, Circ(620, 270, 3), INK)
    if not on("blaze", m):
        flat(c, Poly([(626, 262), (664, 286), (660, 298), (622, 276)]), (250, 245, 235))
    flat(c, Poly([(596, 250), (608, 232), (612, 256)]), horse)
    flat(c, Poly([(530, 330), (590, 252), (570, 300), (540, 350)]), dark)
    # saddle blanket + saddle
    blanket = (70, 140, 200) if on("blanket", m) else (200, 60, 60)
    piece(c, RRect(380, 314, 470, 372, 6), blanket, border=1.5, shadow=None)
    flat(c, [Thick(384, 340 + k * 10, 466, 340 + k * 10, 2) for k in range(2)], (250, 230, 120))
    piece(c, Poly([(390, 316), (460, 316), (470, 300), (450, 310), (400, 310), (386, 296)]), (120, 76, 50), shadow=None)
    # rider
    flat(c, [Thick(430, 300, 470, 350, 12), Thick(470, 350, 460, 390, 10)], (60, 80, 130))
    piece(c, RRect(446, 376, 482, 404, 5), (40, 40, 50) if on("boot", m) else (120, 70, 40), shadow=None)
    piece(c, Poly([(410, 300), (420, 220), (460, 214), (470, 300)]), (230, 190, 120), border=1.5, shadow=SMALL)
    if not on("vest", m):
        flat(c, [Poly([(412, 296), (420, 224), (434, 220), (432, 296)]), Poly([(450, 296), (452, 218), (462, 216), (468, 296)])], (140, 90, 60))
    flat(c, [Thick(460, 230, 520, 250, 9)], (230, 190, 120))
    lasso = (240, 220, 160)
    c.ellipse_ring(540, 236, 26, 18, 3, lasso)
    piece(c, Circ(440, 188, 24), (240, 200, 160), border=1.5, shadow=SMALL)
    flat(c, Circ(452, 186, 2.5), INK)
    band = (60, 120, 210) if on("bandana", m) else (220, 60, 60)
    piece(c, Poly([(420, 206), (462, 206), (452, 226), (436, 230)]), band, shadow=None)
    hat = (230, 220, 200) if on("hat", m) else (120, 80, 50)
    piece(c, [Ell(440, 168, 50, 9), RRect(420, 134, 460, 168, 8)], hat, border=1.5, shadow=SMALL)
    flat(c, Thick(420, 160, 460, 160, 4), (60, 40, 30))


L1002_EL = [
    hscroll("cacti", l1002_cacti, 450, 280, 420),
    hscroll("near", l1002_near, 900, 500, 600),
    focus("cowboy", l1002_rider, amp=(0, 5), speed=2.0),
]
L1002_DIFFS = [("bird", 808, 124, 0), ("arch", 130, 268, 0), ("hat", 440, 160, 0), ("blaze", 644, 280, 0), ("boot", 464, 390, 0)]


# =================================================================== 1003 hot-air balloon rising (clouds sink)
def l1003_bg(c, d):
    c.gradient(0, H, (70, 130, 220), (190, 220, 245))


def l1003_clouds(c, m, dy):
    for x, y, k in ((90, 60, 1.0), (760, 140, 1.2), (200, 260, 0.8), (680, 330, 0.9), (120, 470, 1.1), (820, 520, 0.8)):
        cloud_bg(c, x, dy + y, k, shadow=SMALL)


def l1003_balloon(c, m):
    cols = [(230, 80, 80), (250, 200, 70), (230, 80, 80), (250, 200, 70), (230, 80, 80)]
    cx, cy, rx, ry = 450, 220, 170, 190
    piece(c, [Ell(cx, cy, rx, ry), Poly([(cx - 120, cy + 120), (cx + 120, cy + 120), (cx + 50, cy + 250), (cx - 50, cy + 250)])], cols[0], border=2.5, shadow=PROP)
    for i, col in enumerate(cols):
        xs = cx - rx + rx * 0.4 * i
        flat(c, Poly([(cx + (xs - cx) * 0.25, cy - ry + 8), (xs + 4, cy), (xs + rx * 0.4 - 4, cy), (cx + (xs + rx * 0.4 - cx) * 0.25, cy - ry + 8),
                      (cx + (xs + rx * 0.4 - cx) * 0.5, cy + 200), (cx + (xs - cx) * 0.5, cy + 200)]), col)
    flat(c, Thick(cx - 160, cy + 40, cx + 160, cy + 40, 10), (250, 250, 240))
    # emblem
    if on("emblem", m):
        piece(c, Circ(cx, cy - 60, 30), (90, 120, 220), border=2, shadow=None)
    else:
        piece(c, Poly(star_pts(cx, cy - 60, 36, 15)), (250, 250, 240), border=2, shadow=None)
    # ropes + basket
    flat(c, [Thick(cx - 48, cy + 250, cx - 40, cy + 300, 2), Thick(cx + 48, cy + 250, cx + 40, cy + 300, 2)], INK)
    piece(c, Circ(cx, cy + 266, 14), (255, 180, 80), shadow=None)
    piece(c, RRect(cx - 50, cy + 296, cx + 50, cy + 350, 6), (180, 130, 80), border=2, shadow=PROP)
    flat(c, [Thick(cx - 46, cy + 310 + k * 14, cx + 46, cy + 310 + k * 14, 1.5) for k in range(3)], (140, 96, 60))
    # passengers
    piece(c, Circ(cx - 20, cy + 282, 14), (246, 206, 170), border=1.2, shadow=None)
    flat(c, Ell(cx - 20, cy + 270, 15, 6), (80, 60, 50))
    piece(c, Circ(cx + 22, cy + 280, 14), (240, 200, 160), border=1.2, shadow=None)
    hat = (240, 120, 160) if on("hat", m) else (60, 120, 200)
    piece(c, [Ell(cx + 22, cy + 268, 22, 5), RRect(cx + 10, cy + 252, cx + 34, cy + 268, 5)], hat, shadow=None)
    # sandbags
    bags = [(cx - 60, cy + 352), (cx + 60, cy + 352)]
    for i, (x, y) in enumerate(bags):
        if i == 1 and on("sandbag", m):
            continue
        flat(c, Thick(x + (8 if i == 0 else -8), y - 30, x, y, 1.4), INK)
        piece(c, Ell(x, y + 8, 12, 14), (210, 190, 150), border=1.2, shadow=SMALL)


def l1003_small(c, m):
    col = (90, 170, 220) if on("small", m) else (160, 110, 220)
    piece(c, [Circ(770, 150, 44), Poly([(732, 172), (808, 172), (784, 214), (756, 214)])], col, border=2, shadow=PROP)
    flat(c, Thick(728, 150, 812, 150, 6), (250, 250, 240))
    piece(c, RRect(758, 224, 782, 244, 3), (180, 130, 80), border=1.2, shadow=SMALL)
    flat(c, [Thick(760, 214, 762, 224, 1.2), Thick(780, 214, 778, 224, 1.2)], INK)


def l1003_kite(c, m):
    piece(c, Poly([(130, 370), (168, 420), (130, 476), (92, 420)]), (90, 190, 220) if on("kite", m) else (250, 200, 70), border=1.5, shadow=SMALL)
    flat(c, [Thick(130, 380, 130, 470, 1.5), Thick(100, 420, 160, 420, 1.5)], INK)
    tail = [(130, 470), (120, 500), (140, 530), (124, 560)]
    flat(c, [Thick(tail[i][0], tail[i][1], tail[i + 1][0], tail[i + 1][1], 1.5) for i in range(3)], INK)
    bows = (220, 60, 60)
    flat(c, [Poly([(x - 8, y - 5), (x + 8, y + 5), (x + 8, y - 5), (x - 8, y + 5)]) for x, y in tail[1:]], bows)


L1003_EL = [
    vscroll("clouds", l1003_clouds, 600, up=False, x0=-80, x1=W + 80),
    focus("small", l1003_small, amp=(0, 3), speed=0.5),
    focus("kite", l1003_kite, amp=(3, 0), speed=0.5),
    focus("balloon", l1003_balloon, amp=(0, 3), speed=0.3),
]
L1003_DIFFS = [("emblem", 450, 160, 0), ("hat", 472, 480, 0), ("sandbag", 510, 572, 0), ("small", 770, 160, 0), ("kite", 130, 420, 0)]


# =================================================================== 1004 submarine diving (scenery rises)
def l1004_bg(c, d):
    c.gradient(0, H, (40, 110, 160), (14, 40, 80))


def l1004_wall(c, m, dy):
    for side in (0, 1):
        for i, (y, w, col) in enumerate(((0, 110, (60, 80, 100)), (100, 140, (70, 90, 110)), (200, 100, (55, 75, 95)))):
            x = -10 if side == 0 else W + 10
            k = 1 if side == 0 else -1
            piece(c, Poly([(x, dy + y - 10), (x + k * w, dy + y + 20), (x + k * (w - 20), dy + y + 90), (x, dy + y + 110)]), col, shadow=LAYER)
        sx = 60 if side == 0 else W - 60
        flat(c, [Thick(sx + (k * j * 10), dy + 300 - j * 20, sx + k * (j * 10 + 6), dy + 260 - j * 20, 4) for j in range(4)], (80, 160, 110))
    for x, y in ((180, 40), (700, 120), (240, 220), (650, 280)):
        c.ellipse_ring(x, dy + y, 6, 6, 1.5, (170, 220, 240))
        c.ellipse_ring(x + 10, dy + y + 16, 4, 4, 1.2, (170, 220, 240))


def l1004_fish(c, m, dy):
    for x, y, col in ((90, 120, (250, 170, 70)), (830, 250, (240, 120, 150))):
        piece(c, [Ell(x, dy + y, 18, 10), Poly([(x + 14, dy + y), (x + 30, dy + y - 10), (x + 30, dy + y + 10)])], col, shadow=SMALL)


def l1004_sub(c, m):
    hull = (250, 200, 60)
    soft_union(c, [Poly([(700, 300), (900, 230), (900, 400)])], (230, 240, 200), 0.3, spread=20)
    piece(c, [Ell(450, 320, 250, 90)], hull, border=2.5, shadow=PROP)
    peri = (90, 90, 100)
    piece(c, RRect(400, 210, 520, 250, 12), hull, border=2, shadow=None)
    piece(c, [RRect(436, 146, 454, 212, 3), RRect(436, 146, 484, 164, 4)], (220, 70, 60) if on("periscope", m) else peri, border=1.2, shadow=None)
    for i, x in enumerate((330, 430, 530)):
        glass = (250, 230, 120) if (i == 0 and on("port", m)) else (150, 210, 240)
        piece(c, Circ(x, 316, 26), (200, 200, 210), border=1.5, shadow=None)
        flat(c, Circ(x, 316, 18), glass)
        flat(c, Ell(x - 6, 310, 6, 4), lit(glass, 1.2))
    flat(c, Thick(220, 360, 660, 360, 4), lit(hull, 0.85))
    # tail fins + propeller
    fin = (220, 80, 70)
    piece(c, [Poly([(230, 300), (170, 250), (196, 300)]), Poly([(230, 340), (170, 390), (196, 340)])], fin, border=1.5, shadow=SMALL)
    piece(c, RRect(170, 308, 210, 332, 4), (150, 150, 160), shadow=None)
    piece(c, Circ(700, 316, 18), (250, 120, 90) if on("lamp", m) else (255, 250, 210), border=1.5, shadow=None)


def l1004_prop(c, m):
    flat(c, [Ell(160, 300, 7, 22), Ell(160, 340, 7, 22)], (140, 140, 150))


def l1004_jelly(c, m):
    col = (240, 170, 220) if not on("jelly", m) else (170, 230, 140)
    piece(c, Poly([(110, 470), (120, 444), (150, 436), (180, 444), (190, 470)]), col, border=1.2, shadow=SMALL)
    flat(c, [Thick(124 + k * 14, 470, 120 + k * 14 + (k % 2) * 8, 530, 2) for k in range(5)], col)


def l1004_angler(c, m):
    piece(c, [Ell(790, 480, 44, 30), Poly([(828, 480), (860, 456), (860, 504)])], (90, 70, 110), border=1.5, shadow=SMALL)
    flat(c, Poly([(752, 490), (790, 486), (760, 500)]), (250, 250, 250))
    flat(c, Circ(770, 470, 5), (250, 250, 240))
    flat(c, [Thick(780, 452, 770, 420, 2), Thick(770, 420, 750, 420, 2)], (90, 70, 110))
    piece(c, Circ(746, 422, 11), (120, 230, 140) if on("angler", m) else (255, 230, 110), shadow=None)


L1004_EL = [
    vscroll("wall", l1004_wall, 300, up=True),
    vscroll("fish", l1004_fish, 600, up=True),
    E("prop", l1004_prop, pivot=(160, 320), anim=dict(stretch=(0, 0.6), scaleSpeed=3.0)),
    focus("sub", l1004_sub, amp=(0, 4), speed=0.3),
    focus("jelly", l1004_jelly, amp=(0, 6), speed=0.5),
    focus("angler", l1004_angler, amp=(4, 0), speed=0.2),
]
L1004_DIFFS = [("periscope", 450, 170, 0), ("port", 330, 316, 0), ("lamp", 700, 316, 0), ("jelly", 150, 470, 0), ("angler", 790, 470, 0)]


# =================================================================== 1005 race car past the grandstand
def l1005_bg(c, d):
    sky(c, (110, 180, 236), (220, 236, 248))
    cloud_bg(c, 760, 70, 0.9, shadow=SMALL)
    piece(c, Circ(560, 62, 30), (250, 160, 90) if "sun" in d else (255, 224, 100), border=2, shadow=PROP)
    # a blimp hanging over the circuit
    piece(c, Ell(230, 76, 96, 34), (240, 240, 245), border=2, shadow=PROP)
    piece(c, [Poly([(140, 60), (118, 40), (128, 76)]), Poly([(140, 92), (118, 112), (128, 76)])], (200, 70, 70), shadow=None)
    stripe = (60, 120, 210) if "blimp" in d else (230, 80, 80)
    flat(c, RRect(170, 70, 290, 84, 6), stripe)
    piece(c, RRect(210, 108, 250, 122, 4), (90, 90, 100), shadow=None)
    flat(c, RRect(-20, 330, W + 20, H + 20, 0), (110, 110, 118))
    flat(c, RRect(-20, 540, W + 20, H + 20, 0), (110, 170, 90))


def l1005_stand(c, m, dx):
    piece(c, RRect(dx, 150, dx + 440, 300, 0), (200, 200, 210), shadow=LAYER)
    piece(c, Poly([(dx - 10, 150), (dx + 450, 150), (dx + 430, 130), (dx + 10, 130)]), (220, 80, 70), shadow=SMALL)
    rnd = random.Random(1005)
    cols = [(240, 90, 80), (60, 120, 210), (250, 200, 70), (90, 170, 100), (250, 250, 250), (180, 110, 200)]
    for row, y in enumerate((180, 220, 260)):
        for x in range(14 + row * 8, 440, 26):
            flat(c, [Circ(dx + x, y, 9), RRect(dx + x - 9, y + 8, dx + x + 9, y + 22, 4)], cols[rnd.randrange(6)])
    flat(c, RRect(dx - 2, 300, dx + 442, 330, 0), (90, 90, 100))
    flat(c, [Thick(dx + x, 300, dx + x + 20, 300, 4) for x in range(0, 440, 40)], (250, 250, 250))


def l1005_track(c, m, dx):
    for x in range(0, 900, 60):
        flat(c, RRect(dx + x, 520, dx + x + 30, 540, 0), (230, 60, 60))
        flat(c, RRect(dx + x + 30, 520, dx + x + 60, 540, 0), (250, 250, 250))
    flat(c, [RRect(dx + x, 424, dx + x + 90, 432, 2) for x in (60, 510)], (240, 240, 240))
    flat(c, [Circ(dx + x, 570, 3) for x in range(20, 900, 50)], (90, 140, 70))


def l1005_lines(c, m):
    flat(c, [Thick(60, y, 160 + (y % 3) * 20, y, 2) for y in (370, 400, 440)], (240, 240, 240))


def l1005_car(c, m):
    body = (220, 50, 50)
    soft_union(c, [Ell(470, 474, 250, 14)], (20, 20, 30), 0.35, spread=8)
    wing = (60, 60, 70)
    piece(c, [RRect(200, 360, 230, 440, 3), RRect(196, 350, 280, 370, 3)], (240, 200, 60) if on("wing", m) else wing, border=1.5, shadow=SMALL)
    piece(c, Poly([(220, 440), (230, 400), (360, 380), (430, 360), (560, 380), (700, 420), (720, 450), (230, 460)]), body, border=2.5, shadow=PROP)
    piece(c, RRect(680, 438, 764, 458, 3), (60, 140, 220) if on("nose", m) else wing, border=1.5, shadow=None)
    flat(c, Poly([(360, 410), (700, 430), (700, 440), (360, 430)]), (250, 250, 250))
    # number roundel
    piece(c, Circ(330, 420, 24), (250, 250, 250), border=1.5, shadow=None)
    num = (60, 120, 210) if on("number", m) else INK
    flat(c, [Thick(322, 410, 338, 410, 4), Thick(338, 410, 324, 432, 4)], num)
    # driver
    piece(c, Poly([(420, 384), (450, 356), (500, 356), (520, 384)]), (40, 40, 50), shadow=None)
    helmet = (90, 200, 120) if on("helmet", m) else (250, 210, 60)
    piece(c, Circ(466, 352, 24), helmet, border=2, shadow=SMALL)
    flat(c, RRect(468, 342, 492, 356, 5), (60, 80, 120))
    for x, hub in ((290, (250, 200, 60)), (630, (90, 170, 230) if on("rim", m) else (250, 200, 60))):
        piece(c, Circ(x, 452, 34), (40, 40, 45), border=1.5, shadow=SMALL)
        flat(c, Circ(x, 452, 16), hub)
    # mirror
    flat(c, Thick(540, 384, 560, 372, 3), INK)
    piece(c, RRect(552, 364, 572, 376, 3), body, shadow=None)


L1005_EL = [
    hscroll("stand", l1005_stand, 450, 120, 340),
    hscroll("track", l1005_track, 900, 410, 600),
    E("lines", l1005_lines, anim=dict(bobAmplitude=(12, 0), bobSpeed=2.0)),
    focus("car", l1005_car, amp=(0, 1.5), speed=3.0),
]
L1005_DIFFS = [("blimp", 230, 77, 0), ("sun", 560, 62, 0), ("wing", 236, 380, 0), ("helmet", 466, 350, 0), ("nose", 722, 448, 0),
               ("rim", 630, 452, 0)]


# =================================================================== 1006 camel at sunset
def l1006_bg(c, d):
    sky(c, (90, 80, 160), (250, 170, 110))
    sun = (255, 210, 110)
    soft_union(c, [Circ(700, 250, 70)], (255, 230, 170), 0.4, spread=60)
    piece(c, Circ(700, 250, 70), sun, shadow=None)
    piece(c, Poly([(-20, 300), (120, 260), (300, 290), (500, 250), (720, 290), (920, 260), (920, 330), (-20, 330)]), (210, 130, 100), shadow=LAYER)
    # far pyramids
    if "pyramid" not in d:
        piece(c, Poly([(10, 296), (60, 236), (110, 296)]), (200, 130, 100), border=1.5, shadow=SMALL)
    piece(c, Poly([(120, 296), (200, 200), (280, 296)]), (190, 120, 90), border=1.5, shadow=SMALL)
    flat(c, Poly([(200, 200), (280, 296), (210, 296)]), (160, 100, 80))
    if "star" not in d:
        piece(c, Poly(star_pts(180, 60, 22, 9)), (255, 240, 200), shadow=None)
    bird = (200, 70, 90) if "birds" in d else INK
    flat(c, [Thick(x - 14, y - 7, x, y, 4) for x, y in ((790, 110), (830, 136))] + [Thick(x, y, x + 14, y - 7, 4) for x, y in ((790, 110), (830, 136))], bird)
    flat(c, RRect(-20, 330, W + 20, H + 20, 0), (230, 170, 110))


def l1006_dunes(c, m, dx):
    piece(c, Ell(dx + 120, 420, 220, 70), (226, 160, 100), shadow=LAYER)
    piece(c, Ell(dx + 360, 430, 160, 50), (236, 176, 116), shadow=LAYER)
    flat(c, [Thick(dx + 60 + k * 30, 380 + k * 6, dx + 100 + k * 30, 376 + k * 6, 2) for k in range(4)], (250, 200, 140))


def l1006_near(c, m, dx):
    flat(c, RRect(dx - 2, 480, dx + 902, 600, 0), (220, 156, 100))
    for x in range(0, 900, 60):
        flat(c, Thick(dx + x, 520 + (x // 60 % 3) * 20, dx + x + 34, 516 + (x // 60 % 3) * 20, 2), (196, 130, 80))
    rock(c, dx + 200, 590, 0.9, (170, 110, 90))
    flat(c, [Thick(dx + 640, 580, dx + 650, 550, 3), Thick(dx + 650, 580, dx + 660, 556, 3), Thick(dx + 660, 580, dx + 672, 560, 3)], (140, 120, 70))


def l1006_camel(c, m):
    camel = (196, 150, 100)
    dark = lit(camel, 0.8)
    flat(c, [Thick(290, 360, 280, 470, 13), Thick(330, 360, 340, 470, 13), Thick(500, 360, 520, 470, 13), Thick(540, 360, 530, 470, 13)], dark)
    flat(c, [Thick(280, 470, 270, 486, 9), Thick(340, 470, 352, 486, 9), Thick(520, 470, 512, 486, 9), Thick(530, 470, 546, 486, 9)], (130, 96, 70))
    piece(c, [Ell(410, 330, 140, 50), Ell(360, 286, 60, 46), Ell(460, 286, 60, 46),
              Poly([(530, 320), (590, 250), (610, 200), (640, 210), (620, 270), (560, 350)])], camel, border=2, shadow=PROP)
    piece(c, Ell(650, 210, 40, 22), camel, border=2, shadow=None)
    flat(c, Circ(660, 202, 3), INK)
    flat(c, Thick(276, 320, 250, 370, 5), dark)
    # saddle rug
    rug = (60, 130, 190) if on("rug", m) else (200, 60, 70)
    piece(c, Poly([(350, 270), (470, 270), (480, 360), (340, 360)]), rug, border=1.5, shadow=None)
    flat(c, [Thick(346 + k * 22, 360, 346 + k * 22, 372, 3) for k in range(7)], (250, 210, 90))
    flat(c, Thick(346, 330, 476, 330, 4), (250, 210, 90))
    # bag on the hump
    bag = (110, 160, 90) if on("bag", m) else (150, 100, 70)
    piece(c, RRect(300, 300, 344, 352, 8), bag, border=1.5, shadow=SMALL)
    flat(c, Thick(300, 318, 344, 318, 3), lit(bag, 0.7))
    # lantern hanging from the neck
    flat(c, Thick(570, 290, 570, 320, 1.5), INK)
    if not on("lantern", m):
        piece(c, [RRect(560, 320, 580, 346, 4), Poly([(558, 322), (570, 312), (582, 322)])], (240, 190, 80), border=1.2, shadow=SMALL)
    # rider
    robe = (240, 236, 220)
    piece(c, Poly([(380, 280), (390, 180), (440, 176), (450, 280)]), robe, border=1.5, shadow=SMALL)
    flat(c, [Thick(420, 260, 430, 330, 11)], robe)
    piece(c, Circ(414, 160, 22), (200, 150, 110), border=1.5, shadow=SMALL)
    flat(c, Circ(426, 158, 2.5), INK)
    turban = (80, 120, 200) if on("turban", m) else (250, 250, 250)
    piece(c, [Ell(412, 142, 28, 16), Poly([(394, 150), (380, 210), (396, 210), (404, 150)])], turban, border=1.5, shadow=None)
    flat(c, [Thick(440, 200, 520, 250, 7), Thick(520, 250, 600, 220, 2)], (200, 150, 110))


L1006_EL = [
    hscroll("dunes", l1006_dunes, 450, 320, 490),
    hscroll("near", l1006_near, 900, 470, 600),
    focus("camel", l1006_camel, amp=(0, 3), speed=1.0),
]
L1006_DIFFS = [("pyramid", 60, 270, 0), ("star", 180, 60, 0), ("birds", 810, 122, 0), ("lantern", 570, 330, 0), ("turban", 412, 142, 0),
               ("bag", 322, 326, 0)]


# =================================================================== 1007 parachutist (clouds rise)
def l1007_bg(c, d):
    c.gradient(0, H, (90, 160, 230), (210, 232, 248))


def l1007_clouds(c, m, dy):
    for x, y, k in ((110, 80, 1.1), (800, 200, 1.0), (180, 380, 0.9), (760, 480, 1.2), (470, 560, 0.7)):
        cloud_bg(c, x, dy + y, k, shadow=SMALL)
    flat(c, [Thick(x, dy + y, x, dy + y + 50, 1.5) for x, y in ((300, 120), (620, 300), (90, 520))], (250, 250, 255))


def l1007_chute(c, m):
    cx = 450
    cols = [(240, 90, 80), (250, 250, 250), (250, 200, 70), (250, 250, 250), (60, 130, 210), (250, 250, 250), (240, 90, 80)]
    piece(c, Poly([(cx - 220, 200), (cx - 200, 120), (cx - 120, 64), (cx, 46), (cx + 120, 64), (cx + 200, 120), (cx + 220, 200)]),
          cols[0], border=2.5, shadow=PROP)
    for i, col in enumerate(cols):
        xa, xb = cx - 220 + i * 440 / 7, cx - 220 + (i + 1) * 440 / 7
        top = lambda x: 200 - 150 * math.sqrt(max(0.0, 1 - ((x - cx) / 222) ** 2))
        flat(c, Poly([(xa + 3, 198), (xa + 3, top(xa + 3) + 4), ((xa + xb) / 2, top((xa + xb) / 2) + 4), (xb - 3, top(xb - 3) + 4), (xb - 3, 198)]), col)
    if on("emblem", m):
        piece(c, Circ(326, 132, 20), (60, 130, 210), shadow=None)
    else:
        piece(c, Poly(star_pts(326, 132, 24, 10)), (250, 210, 60), shadow=None)
    flat(c, [Thick(cx - 220 + i * 440 / 7, 200, cx - 10, 360, 1.2) for i in range(8)], INK)
    # jumper
    suit = (240, 120, 50)
    flat(c, [Thick(cx - 10, 420, cx - 26, 490, 12), Thick(cx + 10, 420, cx + 30, 486, 12)], (60, 80, 140))
    shoe = (250, 250, 250) if on("shoes", m) else (60, 50, 50)
    piece(c, [Ell(cx - 30, 494, 14, 8), Ell(cx + 34, 490, 14, 8)], shoe, shadow=None)
    piece(c, RRect(cx - 30, 360, cx + 30, 430, 12), suit, border=1.5, shadow=SMALL)
    flat(c, [Thick(cx - 26, 372, cx - 46, 330, 9), Thick(cx + 26, 372, cx + 44, 330, 9)], suit)
    flat(c, [Thick(cx - 30, 396, cx + 30, 396, 6)], (60, 60, 70))
    piece(c, Circ(cx, 336, 22), (246, 206, 170), border=1.5, shadow=SMALL)
    helmet = (60, 180, 120) if on("helmet", m) else (250, 210, 60)
    piece(c, Poly([(cx - 24, 334), (cx - 20, 314), (cx, 306), (cx + 20, 314), (cx + 24, 334)]), helmet, shadow=None)
    flat(c, RRect(cx - 16, 334, cx + 16, 344, 4), (60, 90, 140))


def l1007_plane(c, m):
    body = (250, 250, 250)
    piece(c, [Ell(780, 80, 60, 14), Poly([(740, 80), (700, 54), (716, 82)])], body, border=1.5, shadow=SMALL)
    tail = (60, 120, 210) if on("plane", m) else (220, 70, 70)
    flat(c, RRect(734, 78, 834, 86, 4), tail)
    piece(c, Poly([(722, 76), (704, 52), (716, 50), (736, 74)]), tail, shadow=None)
    piece(c, Poly([(770, 84), (800, 112), (812, 112), (796, 84)]), lit(body, 0.92), shadow=None)
    flat(c, [Circ(790 + k * 12, 76, 2.5) for k in range(3)], (90, 140, 200))


def l1007_balloon(c, m):
    col = (90, 190, 120) if on("balloon", m) else (240, 140, 60)
    piece(c, [Circ(130, 470, 40), Poly([(96, 490), (164, 490), (140, 526), (120, 526)])], col, border=2, shadow=PROP)
    flat(c, Thick(92, 470, 168, 470, 5), (250, 250, 240))
    flat(c, [Thick(122, 526, 122, 538, 1.2), Thick(138, 526, 138, 538, 1.2)], INK)
    piece(c, RRect(118, 536, 142, 554, 3), (180, 130, 80), border=1.2, shadow=SMALL)


def l1007_buddy(c, m):
    col = (160, 110, 220) if on("buddy", m) else (90, 190, 200)
    piece(c, Poly([(650, 380), (670, 346), (720, 334), (770, 346), (790, 380)]), col, border=2, shadow=PROP)
    flat(c, [Thick(x, 380, 720, 440, 1) for x in (652, 690, 750, 788)], INK)
    piece(c, [RRect(710, 436, 730, 470, 6), Circ(720, 430, 9)], (240, 120, 50), border=1.2, shadow=SMALL)


L1007_EL = [
    vscroll("clouds", l1007_clouds, 600, up=True, x0=-80, x1=W + 80),
    focus("plane", l1007_plane, amp=(4, 0), speed=0.3),
    focus("balloon", l1007_balloon, amp=(0, 4), speed=0.3),
    focus("buddy", l1007_buddy, amp=(5, 3), speed=0.3, pivot=(720, 380)),
    focus("chute", l1007_chute, amp=(6, 0), speed=0.2, pivot=(450, 200)),
]
L1007_DIFFS = [("emblem", 326, 132, 0), ("helmet", 450, 318, 0), ("shoes", 452, 492, 0), ("plane", 770, 74, 0), ("balloon", 130, 490, 0),
               ("buddy", 720, 360, 0)]


# =================================================================== 1008 puppy running in the park
def l1008_bg(c, d):
    sky(c, (130, 196, 240), (230, 244, 250))
    piece(c, Circ(110, 80, 32), (255, 224, 100) if "sun" not in d else (250, 160, 90), border=2, shadow=PROP)
    far_skyline(c, 260, 60, 150, (170, 186, 214), seed=1008)
    # a clock tower in the skyline
    piece(c, [RRect(620, 110, 680, 260, 2), Poly([(612, 112), (650, 70), (688, 112)])], (190, 170, 160), border=1.5, shadow=SMALL)
    piece(c, Circ(650, 140, 20), (250, 250, 240) if "clock" not in d else (250, 210, 90), border=1.2, shadow=None)
    flat(c, [Thick(650, 140, 650, 128, 2), Thick(650, 140, 660, 146, 2)], INK)
    if "kite" not in d:
        piece(c, Poly([(390, 60), (416, 84), (390, 118), (364, 84)]), (240, 90, 150), border=1.5, shadow=SMALL)
        flat(c, [Thick(390, 118, 400, 160, 1.4)], INK)
    flat(c, RRect(-20, 260, W + 20, H + 20, 0), (130, 190, 100))
    flat(c, RRect(-20, 470, W + 20, H + 20, 0), (230, 210, 170))


def l1008_trees(c, m, dx):
    tree_round(c, dx + 80, 380, 1.0, (80, 150, 85))
    tree_pine(c, dx + 240, 380, h=110)
    tree_round(c, dx + 370, 384, 0.8, (100, 170, 90))
    piece(c, [RRect(dx + 150, 360, dx + 220, 368, 2), RRect(dx + 156, 368, dx + 162, 384, 1), RRect(dx + 208, 368, dx + 214, 384, 1)],
          (170, 120, 80), shadow=SMALL)


def l1008_fence(c, m, dx):
    flat(c, [RRect(dx + x, 400, dx + x + 14, 470, 3) for x in range(0, 900, 45)], (250, 250, 245))
    flat(c, [RRect(dx - 2, 418, dx + 902, 426, 0), RRect(dx - 2, 446, dx + 902, 454, 0)], (236, 236, 230))
    for x, col in ((60, (240, 90, 120)), (330, (250, 200, 60)), (610, (160, 120, 230)), (820, (250, 140, 60))):
        flat(c, [Circ(dx + x + k * 16, 478 - (k % 2) * 6, 6) for k in range(3)], col)
    flat(c, [Circ(dx + x, 560 + (x % 3) * 8, 3) for x in range(30, 900, 80)], (200, 180, 140))


def l1008_dog(c, m):
    fur = (230, 180, 120)
    dark = (150, 100, 70)
    flat(c, [Thick(360, 470, 320, 520, 13), Thick(400, 470, 420, 524, 13), Thick(560, 470, 610, 510, 13), Thick(530, 474, 520, 526, 13)], lit(fur, 0.88))
    tail = (250, 250, 250) if on("tail", m) else fur
    piece(c, Poly([(350, 430), (290, 390), (280, 400), (340, 450)]), tail, border=1.5, shadow=SMALL)
    piece(c, [Ell(460, 450, 120, 46)], fur, border=2, shadow=PROP)
    if not on("spot", m):
        flat(c, Ell(420, 430, 34, 20), dark)
    piece(c, Circ(600, 390, 50), fur, border=2, shadow=PROP)
    piece(c, Ell(650, 410, 30, 20), lit(fur, 1.08), shadow=None)
    flat(c, Circ(672, 400, 7), INK)
    flat(c, Circ(612, 378, 5), INK)
    flat(c, Ell(650, 430, 10, 6), (230, 100, 110))
    ear = (250, 230, 200) if on("ear", m) else dark
    piece(c, Poly([(570, 350), (540, 330), (550, 400), (575, 380)]), ear, border=1.5, shadow=SMALL)
    collar = (60, 140, 220) if on("collar", m) else (220, 50, 60)
    flat(c, Thick(560, 420, 580, 448, 9), collar)
    piece(c, Circ(574, 452, 7), (250, 210, 70), shadow=None)
    # stick in its mouth
    if not on("stick", m):
        piece(c, [Thick(640, 440, 730, 420, 6)], (150, 110, 70), shadow=SMALL)


def l1008_butterfly(i, x, y):
    def d(c, m):
        piece(c, [Ell(x - 8, y, 8, 10), Ell(x + 8, y, 8, 10)], (250, 170, 60), shadow=SMALL)
    return E("fly%d" % i, d, pivot=(x, y), anim=dict(stretch=(0.6, 0), scaleSpeed=2.0, bobAmplitude=(10, 6), bobSpeed=0.2))


L1008_EL = [
    hscroll("trees", l1008_trees, 450, 260, 400),
    hscroll("fence", l1008_fence, 900, 396, 600),
    l1008_butterfly(0, 800, 340),
    focus("dog", l1008_dog, amp=(0, 6), speed=2.0),
]
L1008_DIFFS = [("sun", 110, 80, 0), ("clock", 650, 140, 0), ("kite", 390, 90, 0), ("tail", 318, 418, 0), ("spot", 420, 430, 0),
               ("ear", 556, 362, 0), ("collar", 570, 436, 0), ("stick", 690, 430, 0)]


# =================================================================== 1009 biplane above a sea of clouds
def l1009_bg(c, d):
    sky(c, (70, 140, 220), (230, 230, 240))
    piece(c, Poly(star_pts(800, 90, 60, 44, points=12)), (255, 200, 100), shadow=PROP)
    piece(c, Circ(800, 90, 38), (255, 226, 110) if "sun" not in d else (250, 150, 90), border=2, shadow=PROP)
    # snowy peaks poking through the clouds
    piece(c, Poly([(20, 420), (140, 260), (260, 420)]), (140, 150, 190), shadow=LAYER)
    flat(c, Poly([(140, 260), (110, 300), (130, 294), (150, 306), (170, 300)]), (250, 250, 255))
    if "flag" not in d:
        flat(c, Thick(140, 262, 140, 212, 2.5), INK)
        flat(c, Poly([(141, 212), (178, 224), (141, 236)]), (230, 70, 70))
    piece(c, Poly([(600, 420), (720, 300), (860, 420)]), (150, 160, 196), shadow=LAYER)
    flat(c, Poly([(720, 300), (696, 324), (716, 320), (734, 330), (744, 324)]), (250, 250, 255))
    flat(c, RRect(-20, 400, W + 20, H + 20, 0), (236, 240, 248))


def l1009_far(c, m, dx):
    for k in range(3):
        piece(c, Circ(dx + 50 + k * 100, 400 + (k % 2) * 12, 50), (244, 246, 252), shadow=(1, 3, 6, 0.18))


def l1009_near(c, m, dx):
    for x, y, r in ((60, 520, 80), (220, 540, 70), (400, 510, 90), (580, 545, 70), (760, 520, 85)):
        piece(c, Circ(dx + x, y, r), (252, 252, 255), shadow=(1, 3, 8, 0.2))


def l1009_plane(c, m):
    body = (230, 70, 60)
    # lower wing
    piece(c, RRect(330, 330, 620, 352, 10), lit(body, 0.85), border=2, shadow=PROP)
    piece(c, [Ell(450, 300, 190, 40), Poly([(270, 290), (200, 250), (196, 300), (280, 320)])], body, border=2.5, shadow=PROP)
    fin = (250, 200, 70) if on("tail", m) else body
    piece(c, Poly([(214, 300), (190, 220), (222, 222), (250, 292)]), fin, border=2, shadow=None)
    flat(c, [Thick(390, 220, 400, 330, 4), Thick(540, 220, 530, 330, 4)], (90, 70, 60))
    # upper wing
    piece(c, RRect(330, 206, 620, 228, 10), lit(body, 1.1), border=2, shadow=PROP)
    roundel = (60, 120, 210) if on("roundel", m) else (250, 250, 250)
    piece(c, Circ(580, 217, 14), roundel, shadow=None)
    flat(c, Circ(580, 217, 6), (250, 200, 70))
    # pilot
    piece(c, Circ(430, 252, 20), (246, 206, 170), border=1.5, shadow=None)
    flat(c, Ell(428, 240, 21, 12), (120, 80, 50))
    flat(c, [Circ(426, 248, 6), Circ(442, 248, 6)], (150, 210, 240))
    scarf = (250, 250, 250) if not on("scarf", m) else (90, 190, 110)
    piece(c, Poly([(416, 270), (360, 262), (340, 276), (364, 284), (420, 280)]), scarf, shadow=None)
    piece(c, Poly([(400, 270), (470, 270), (460, 290), (410, 290)]), (90, 70, 60), shadow=None)
    # wheels
    flat(c, [Thick(470, 330, 456, 380, 4), Thick(510, 330, 520, 380, 4)], (90, 70, 60))
    for x in (456, 520):
        piece(c, Circ(x, 384, 16), (230, 120, 60) if (x == 456 and on("wheel", m)) else (50, 50, 55), border=1.2, shadow=None)
        flat(c, Circ(x, 384, 5), (250, 200, 70))
    piece(c, Ell(640, 300, 12, 22), (90, 90, 100), border=1.5, shadow=None)


def l1009_prop(c, m):
    flat(c, Ell(652, 300, 6, 56), (120, 110, 100))


L1009_EL = [
    hscroll("far", l1009_far, 300, 340, 470),
    hscroll("near", l1009_near, 900, 420, 640),
    focus("plane", l1009_plane, amp=(0, 6), speed=0.3),
    E("prop", l1009_prop, pivot=(652, 300), anim=dict(stretch=(0, 0.85), scaleSpeed=4.0, bobAmplitude=(0, 6), bobSpeed=0.3)),
]
L1009_DIFFS = [("sun", 800, 90, 0), ("flag", 156, 224, 0), ("tail", 216, 260, 0), ("roundel", 580, 217, 0), ("scarf", 380, 274, 0),
               ("wheel", 456, 384, 0)]


LEVELS = [
    ("Level1000", "田野小火车", l1000_bg, L1000_EL, L1000_DIFFS, 60, OPTS),
    ("Level1001", "海滨骑行", l1001_bg, L1001_EL, L1001_DIFFS, 60, OPTS),
    ("Level1002", "荒野牛仔", l1002_bg, L1002_EL, L1002_DIFFS, 60, OPTS),
    ("Level1003", "热气球升空", l1003_bg, L1003_EL, L1003_DIFFS, 60, OPTS),
    ("Level1004", "深海潜航", l1004_bg, L1004_EL, L1004_DIFFS, 60, OPTS),
    ("Level1005", "赛道飞驰", l1005_bg, L1005_EL, L1005_DIFFS, 60, OPTS),
    ("Level1006", "沙漠驼队", l1006_bg, L1006_EL, L1006_DIFFS, 60, OPTS),
    ("Level1007", "跳伞", l1007_bg, L1007_EL, L1007_DIFFS, 60, OPTS),
    ("Level1008", "公园小狗", l1008_bg, L1008_EL, L1008_DIFFS, 60, OPTS),
    ("Level1009", "云海飞行", l1009_bg, L1009_EL, L1009_DIFFS, 60, OPTS),
]
