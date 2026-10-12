# -*- coding: utf-8 -*-
"""Perspective paper levels ("near is big, far is small"), full-bleed:
  Level63 欢乐游乐园 - plaza receding to the horizon: lamp rows, ferris wheel, carousel, roller coaster
  Level64 港口集市   - cobbled quay street running into the distance, houses in a receding row, boats near and far
  Level65 冬日雪村   - snowy village at dusk around a path to the mountains, near and far snow

Every object is drawn in its own coordinates and placed on the ground plane with persp.View (size = depth scale,
colours fade into the haze with distance); everything goes through paper25 so far pieces also get smaller,
lighter shadows. Ground decals (paths, sea, tiles) use an rgba colour so they lie flat without a shadow.
"""
import math
import random

from fdcore import H, W, WHITE, BLACK, E, cloud, bird_bbox, lit
from paper import paper_post
from paper25 import paper_level
from persp import View

OPTS = dict(post=paper_post, anim_seconds=8.0, frames=48)


def decal(col):
    """Flat ground paint (rgba with alpha 1 -> no paper shadow)."""
    return tuple(col[:3]) + (1.0,)


def stripes_cone(c, apex, x0, x1, y, n, cols):
    for k in range(n):
        a = x0 + (x1 - x0) * k / n
        b = x0 + (x1 - x0) * (k + 1) / n
        c.polygon([apex, (a, y), (b, y)], cols[k % len(cols)])


def scallops(c, x0, x1, y, r, cols):
    k = 0
    x = x0 + r
    while x <= x1 - r + 0.1:
        c.ellipse(x, y, r, r, cols[k % len(cols)], ymin=y)
        x += 2 * r
        k += 1


def person(c, x, y, shirt, skin=(250, 210, 170), hair=(90, 60, 40), s=1.0):
    c.line(x - 5 * s, y, x - 4 * s, y - 22 * s, 5 * s, (60, 70, 110))
    c.line(x + 5 * s, y, x + 4 * s, y - 22 * s, 5 * s, (60, 70, 110))
    c.round_rect(x - 11 * s, y - 50 * s, x + 11 * s, y - 20 * s, 6 * s, shirt)
    c.circle(x, y - 60 * s, 10 * s, skin)
    c.ellipse(x, y - 65 * s, 11 * s, 6 * s, hair, ymax=y - 63 * s)


def bush(c, x, y, s, col):
    for dx, dy, r in ((-18, 0, 16), (0, -10, 20), (18, 0, 15)):
        c.circle(x + dx * s, y + dy * s, r * s, col)
    c.circle(x - 4 * s, y - 14 * s, 7 * s, lit(col, 1.18))


def round_tree(c, x, y, h, col):
    c.rect(x - h * 0.06, y - h * 0.45, x + h * 0.06, y, (130, 90, 60))
    c.circle(x, y - h * 0.68, h * 0.32, col)
    c.circle(x - h * 0.08, y - h * 0.76, h * 0.12, lit(col, 1.15))


def pine(c, x, y, h, col, snow=None):
    c.rect(x - h * 0.05, y - h * 0.15, x + h * 0.05, y, (110, 75, 50))
    for k in range(3):
        top = y - h + k * h * 0.25
        w = h * (0.22 + k * 0.1)
        c.polygon([(x, top), (x - w, top + h * 0.4), (x + w, top + h * 0.4)], col)
        if snow:
            c.polygon([(x, top), (x - w * 0.45, top + h * 0.18), (x - w * 0.15, top + h * 0.15), (x + w * 0.1, top + h * 0.2),
                       (x + w * 0.45, top + h * 0.18)], snow)


def clouds_drift(prefix, items, speed=12):
    """Clouds: higher (closer to the viewer) ones are bigger and move faster."""
    out = []
    for i, (x, y, k) in enumerate(items):
        out.append(E("%s%d" % (prefix, i), (lambda x, y, k: lambda c, m: cloud(c, x, y, k))(x, y, k),
                     anim=dict(driftVelocity=(speed * k, 0), driftLength=1200, driftStart=-(x + 150), phase=(x + 150) / 1200)))
    return out


def birds_fly(prefix, items, col=BLACK):
    return [E("%s%d" % (prefix, i), (lambda x, y, s: lambda c, m: c.bird(x, y, s, col))(x, y, s), bird_bbox(x, y, s),
              pivot=(x, y - 2), anim=dict(stretch=(0, 0.6), scaleSpeed=2.2 + i * 0.3, bobAmplitude=(18 * s / 12, 6 * s / 12),
                                          bobSpeed=0.08 + i * 0.02, phase=i * 0.27))
            for i, (x, y, s) in enumerate(items)]


def draw_sorted(c, objs):
    """objs: (screen y of the foot, xf, fn(canvas, *args), args) - painted far to near."""
    for y, xf, fn, args in sorted(objs, key=lambda o: o[0]):
        fn(xf.canvas(c), *args)


# =================================================================== Level 63 amusement park
V63 = View(hz=292, vpx=450, yref=600, haze=(206, 230, 250), haze_k=0.45)
WHEEL = (210, 225, 160)
COASTER = [(470, 390), (515, 260), (560, 175), (620, 160), (672, 235), (720, 330), (772, 262), (826, 196), (880, 186), (930, 220)]

XF_COASTER = V63.at(690, 318, 7.35, anchor=(700, 430))
XF_WHEEL = V63.at(210, 405, 2.13, anchor=(210, 462))
XF_CAROUSEL = V63.at(652, 440, 1.75, anchor=(560, 452))
XF_BOOTH = V63.at(222, 488, 1.29, anchor=(370, 470))
XF_CART = V63.at(520, 585, 0.95, anchor=(500, 575))
XF_VENDOR = V63.at(800, 598, 1.0, anchor=(790, 590))
XF_SIGN = V63.at(70, 592, 1.0, anchor=(60, 580))
LAMPS63 = [(X, y) for y in (335, 380, 450, 540) for X in (-185, 185)]
LAMP_DIFF = (185, 450)
XF_LAMP_DIFF = V63.atX(*LAMP_DIFF)


def l63_coaster(c, d):
    for i, (px, py) in enumerate(COASTER):
        c.line(px, py + 4, px, 430, 5, (236, 236, 244))
        if i:
            qx, qy = COASTER[i - 1]
            c.line(qx, 430 - (430 - qy) * 0.4, px, py + 6, 3, (220, 220, 232))
    for i in range(len(COASTER) - 1):
        (ax, ay), (bx, by) = COASTER[i], COASTER[i + 1]
        c.line(ax, ay, bx, by, 9, (220, 60, 70))
        c.line(ax, ay - 4, bx, by - 4, 3, (255, 130, 130))
    car = (60, 170, 230) if "coaster" in d else (250, 200, 40)
    c.polygon([(578, 168), (612, 160), (614, 140), (580, 146)], car)
    c.polygon([(560, 172), (580, 168), (582, 150), (566, 152)], lit(car, 0.85))
    for px, py in ((570, 152), (596, 146)):
        c.circle(px, py - 6, 6, (250, 210, 170))


def l63_wheel_stand(c, d):
    cx, cy, r = WHEEL
    for bx in (140, 280):
        c.line(cx, cy, bx, 450, 12, (236, 236, 246))
    c.line(160, 380, 260, 380, 6, (236, 236, 246))
    c.round_rect(120, 444, 300, 462, 6, (150, 150, 170))


def l63_carousel(c, d):
    roof = [(240, 70, 80), (255, 245, 235)]
    for x in range(480, 660, 40):
        c.line(x, 300, x, 440, 4, (230, 190, 70))
    c.round_rect(450, 432, 670, 452, 8, (200, 60, 80))
    c.ellipse(560, 432, 110, 14, (250, 230, 200))
    stripes_cone(c, (560, 214), 448, 672, 300, 12, roof)
    scallops(c, 448, 672, 300, 9.33, roof[::-1])
    c.line(560, 214, 560, 186, 3, (120, 110, 110))
    flag = (70, 120, 230) if "flag" in d else (240, 70, 80)
    c.polygon([(561, 186), (590, 194), (561, 202)], flag)


def l63_booth(c, d):
    booth = (80, 170, 240) if "booth" in d else (240, 110, 70)
    c.rect(330, 380, 410, 470, (250, 240, 220))
    c.rect(342, 396, 398, 430, (150, 210, 240))
    c.rect(330, 446, 410, 470, lit(booth, 0.9))
    stripes_cone(c, (370, 346), 322, 418, 382, 6, [booth, WHITE])
    c.round_rect(344, 352, 396, 368, 4, (255, 240, 150))
    for k in range(4):
        c.rect(350 + k * 12, 357, 356 + k * 12, 363, (200, 80, 70))


def l63_lamp(c, d, missing):
    c.line(0, 0, 0, -110, 6, (70, 80, 100))
    c.line(-22, -104, 22, -104, 4, (70, 80, 100))
    c.circle(-22, -114, 10, (255, 244, 190))
    if not missing:
        c.circle(22, -114, 10, (255, 244, 190))
    c.round_rect(-10, -4, 10, 6, 3, (70, 80, 100))


def l63_sign(c, d):
    c.line(60, 580, 60, 470, 6, (140, 95, 60))
    pts = [(28, 480), (112, 480), (128, 494), (112, 508), (28, 508)]
    if "sign" in d:
        pts = [(148 - px, py) for px, py in pts]
    c.polygon(pts, (250, 220, 120))
    for k in range(3):
        c.line(48 + k * 18, 494, 58 + k * 18, 494, 3, (150, 100, 60))


def l63_cart(c, d):
    c.round_rect(430, 500, 570, 556, 10, (250, 200, 220))
    c.rect(430, 520, 570, 530, (240, 140, 180))
    for wx in (455, 545):
        c.circle(wx, 562, 13, (90, 90, 110))
        c.circle(wx, 562, 5, (220, 220, 230))
    c.line(560, 500, 560, 430, 3, (140, 140, 160))
    stripes_cone(c, (560, 410), 500, 620, 446, 6, [(120, 200, 240), WHITE])
    scoops = [(250, 150, 190), (130, 210, 140) if "cone" in d else (255, 240, 200), (150, 100, 70)]
    for k, col in enumerate(scoops):
        x = 452 + k * 28
        c.polygon([(x - 9, 494), (x + 9, 494), (x, 516)], (230, 180, 110))
        c.circle(x, 488, 11, col)


def l63_person(c, d, shirt, hair):
    person(c, 0, 0, shirt, hair=hair, s=1.25)


def l63_bush(c, d):
    bush(c, 0, 0, 1.6, (70, 160, 80))


def l63_flowerbed(c, d):
    rnd = random.Random(631)
    c.round_rect(-90, -26, 90, 30, 18, (100, 170, 80))
    for _ in range(9):
        fx, fy = rnd.uniform(-80, 80), rnd.uniform(-18, 6)
        c.circle(fx, fy, 7, rnd.choice(((255, 110, 150), (255, 220, 70), (250, 250, 250))))
        c.circle(fx, fy, 3, (255, 240, 170))


def l63_bg(c, d):
    v = V63
    c.gradient(0, v.hz + 2, (110, 190, 250), (218, 238, 252))
    # far city and tree line on the horizon (tiny and pale)
    rnd = random.Random(63)
    x = -10
    while x < 920:
        w, h = rnd.randint(14, 30), rnd.randint(14, 48)
        c.rect(x, v.hz - h, x + w, v.hz + 2, (190, 212, 234))
        x += w + rnd.randint(1, 5)
    c.ellipse(160, v.hz + 4, 300, 22, (176, 216, 168))
    c.ellipse(740, v.hz + 4, 320, 26, (166, 210, 156))
    for k in range(60):
        tx = k * 15 + rnd.uniform(-4, 4)
        c.circle(tx, v.hz - 2, rnd.uniform(5, 8), (140, 196, 136))
    # plaza: perspective tiles converging on the vanishing point, central path
    c.rect(0, v.hz, W, H + 10, (232, 220, 198))
    for X in range(-3000, 3001, 110):
        v.radial(c, X, (216, 202, 180), 1.2)
    for y in v.ground_rows(0.14):
        c.line(0, y, W, y, max(1.0, 2.2 * v.s(y)), (216, 202, 180))
    yb = H + 20
    c.polygon([(v.wx(-170, yb), yb), (v.wx(-170, v.hz + 1), v.hz + 1), (v.wx(170, v.hz + 1), v.hz + 1), (v.wx(170, yb), yb)],
              decal((244, 234, 212)))
    for X in (-170, 170):
        v.radial(c, X, (200, 184, 160), 3)
    # objects, far to near
    objs = [(318, XF_COASTER, l63_coaster, (d,)), (405, XF_WHEEL, l63_wheel_stand, (d,)), (440, XF_CAROUSEL, l63_carousel, (d,)),
            (488, XF_BOOTH, l63_booth, (d,)), (585, XF_CART, l63_cart, (d,)), (592, XF_SIGN, l63_sign, (d,))]
    for X, y in LAMPS63:
        objs.append((y, v.atX(X, y), l63_lamp, (d, (X, y) == LAMP_DIFF and "lamp" in d)))
    for X, y in ((-260, 310), (260, 312), (-270, 345), (270, 350), (-300, 400), (300, 410)):
        objs.append((y, v.atX(X, y), l63_bush, (d,)))
    people = [(-90, 352, (240, 120, 100), (60, 40, 30)), (70, 372, (110, 190, 120), (40, 30, 30)), (-120, 430, (90, 150, 220), (230, 190, 90)),
              (110, 480, (240, 180, 60), (40, 30, 30)), (-40, 530, (150, 110, 220), (90, 60, 40)), (330, 510, (240, 100, 120), (60, 40, 30)),
              (-310, 562, (110, 190, 120), (90, 60, 40))]
    for X, y, shirt, hair in people:
        objs.append((y, v.atX(X, y), l63_person, (d, shirt, hair)))
    objs.append((590, v.at(870, 590), l63_flowerbed, (d,)))
    objs.append((611, v.at(200, 614, 0.8), l63_flowerbed, (d,)))
    objs.append((599, XF_VENDOR, l63_person_vendor, (d,)))
    draw_sorted(c, objs)


def l63_person_vendor(c, d):
    person(c, 790, 590, (240, 120, 90), hair=(60, 40, 30), s=1.2)


def l63_wheel(c, m):
    cx, cy, r = WHEEL
    for k in range(16):
        a = math.radians(k * 22.5)
        c.line(cx, cy, cx + r * math.cos(a), cy - r * math.sin(a), 3, (250, 250, 255))
    c.ellipse_ring(cx, cy, r, r, 9, (240, 90, 130))
    c.ellipse_ring(cx, cy, r * 0.62, r * 0.62, 5, (255, 200, 80))
    for k in range(8):
        a = math.radians(k * 45)
        c.circle(cx + r * math.cos(a), cy - r * math.sin(a), 6, (255, 240, 160))
    c.circle(cx, cy, 16, (120, 120, 150))
    c.circle(cx, cy, 7, (230, 230, 240))


CABIN_COLS = [(250, 110, 110), (255, 200, 70), (110, 200, 240), (140, 210, 120), (200, 140, 230), (255, 150, 90), (90, 170, 220),
              (240, 120, 180)]


def l63_cabin(c, m, k):
    cx, cy, _ = WHEEL
    col = CABIN_COLS[k]
    c.line(cx, cy, cx, cy + 12, 3, (120, 120, 140))
    c.ellipse(cx, cy + 14, 20, 7, lit(col, 0.85), ymax=cy + 14)
    c.round_rect(cx - 17, cy + 12, cx + 17, cy + 40, 7, col)
    c.round_rect(cx - 12, cy + 17, cx + 12, cy + 27, 3, (210, 236, 250))


def l63_horse(c, m, x, col):
    y = 380
    c.line(x - 14, y + 8, x - 18, y + 28, 4, lit(col, 0.85))
    c.line(x + 12, y + 8, x + 18, y + 28, 4, lit(col, 0.85))
    c.ellipse(x, y, 22, 12, col)
    c.polygon([(x + 14, y - 6), (x + 26, y - 26), (x + 34, y - 22), (x + 24, y - 2)], col)
    c.ellipse(x + 34, y - 22, 9, 6, col)
    c.polygon([(x - 20, y - 4), (x - 32, y + 10), (x - 22, y + 4)], (255, 220, 120))
    c.polygon([(x + 18, y - 14), (x + 24, y - 28), (x + 20, y - 8)], (255, 220, 120))
    c.ellipse(x - 2, y - 10, 10, 5, (230, 70, 90))


def l63_balloons(c, m):
    hx, hy = 806, 520
    cols = [((760, 360), (240, 70, 80)), ((800, 340), (70, 170, 240)), ((840, 366), (255, 210, 60)),
            ((780, 400), (120, 200, 110)), ((826, 410), (200, 120, 230))]
    for i, ((bx, by), col) in enumerate(cols):
        if not (m and i == 2):
            c.line(hx, hy, bx, by + 22, 1.5, (110, 110, 120))
    for i, ((bx, by), col) in enumerate(cols):
        if m and i == 2:
            continue
        c.ellipse(bx, by, 18, 22, col)
        c.ellipse(bx - 6, by - 8, 5, 7, lit(col, 1.3))
        c.polygon([(bx - 4, by + 24), (bx + 4, by + 24), (bx, by + 19)], col)


def l63_loose_balloon(c, m):
    c.line(330, 230, 326, 256, 1.5, (110, 110, 120))
    c.ellipse(330, 214, 12, 15, (255, 120, 170))


def l63_bunting(c, m):
    """Overhead bunting - the nearest thing in the picture, so it is big and drawn over the clouds."""
    for x0, x1, y0, sag in ((-30, 470, -6, 40), (430, 930, -6, 40)):
        pts = [(x0 + (x1 - x0) * k / 8, y0 + sag * math.sin(math.pi * k / 8)) for k in range(9)]
        for k in range(8):
            c.line(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 3, (90, 80, 90))
            mx, my = (pts[k][0] + pts[k + 1][0]) / 2, (pts[k][1] + pts[k + 1][1]) / 2
            c.polygon([(mx - 20, my), (mx + 20, my), (mx, my + 36)], [(240, 80, 90), (255, 210, 60), (80, 170, 240), (110, 200, 110)][k % 4])


_WS = XF_WHEEL.s
_CS = XF_CAROUSEL.s
L63_ELEMENTS = clouds_drift("cloud", [(80, 60, 0.9), (430, 50, 1.1), (700, 80, 0.7), (300, 105, 0.45), (600, 118, 0.3)]) + [
    E("wheel", XF_WHEEL.draw(l63_wheel), pivot=XF_WHEEL.p(*WHEEL[:2]), anim=dict(rotateSpeed=10.8)),
] + [
    E("cabin%d" % k, XF_WHEEL.draw(l63_cabin, k), pivot=XF_WHEEL.p(*WHEEL[:2]),
      anim=dict(orbitRadius=(WHEEL[2] * _WS, WHEEL[2] * _WS), orbitSpeed=0.03, phase=k / 8)) for k in range(8)
] + [
    E("horse%d" % i, XF_CAROUSEL.draw(l63_horse, x, col), anim=dict(bobAmplitude=(0, 10 * _CS), bobSpeed=0.45, phase=i * 0.33))
    for i, (x, col) in enumerate(((500, (250, 250, 250)), (580, (250, 220, 170)), (632, (220, 230, 250))))
] + [
    E("balloons", XF_VENDOR.draw(l63_balloons), pivot=XF_VENDOR.p(806, 520), variant=True, anim=dict(swingAngle=3, swingSpeed=0.25)),
    E("loose_balloon", l63_loose_balloon, anim=dict(driftVelocity=(5, 26), driftLength=260, driftFade=True, driftGrow=-0.5)),
] + birds_fly("bird", [(420, 150, 12), (450, 136, 9), (760, 100, 10), (560, 240, 5), (575, 234, 4)]) + [
    E("bunting", l63_bunting),
]

L63_DIFFS = [
    ("coaster", *XF_COASTER.p(590, 156), 0),
    ("flag", *XF_CAROUSEL.p(575, 194), 0),
    ("booth", *XF_BOOTH.p(370, 365), 0),
    ("lamp", *XF_LAMP_DIFF.p(22, -114), 0),
    ("sign", *XF_SIGN.p(78, 494), 0),
    ("cone", *XF_CART.p(480, 488), 0),
    ("balloon", *XF_VENDOR.p(840, 366), 0),
]


# =================================================================== Level 64 harbour market
V64 = View(hz=262, vpx=520, yref=600, haze=(214, 232, 246), haze_k=0.5)
QUAY_X = 130                         # world x of the quay edge (sea to the right)
HOUSE_K = 1.2
XF_HOUSE = V64.at(V64.wx(-150, 600) - 70 * HOUSE_K, 600, HOUSE_K)      # near blue house (the one with differences)
XF_LIGHTHOUSE = V64.at(812, 271, 21.0, anchor=(830, 330))
XF_FISH = V64.at(V64.wx(-20, 455), 455, 1.35, anchor=(430, 520))
XF_FRUIT = V64.at(V64.wx(-40, 590), 590, 0.8, anchor=(710, 530))
BOATS = [(V64.wx(560, 296), 296, 3.0, (180, 90, 70), (250, 250, 245)), (V64.wx(440, 352), 352, 2.2, (60, 110, 160), (250, 200, 120)),
         (760, 430, 1.3, (90, 150, 110), (250, 250, 240)), (800, 575, 1.0, (230, 200, 80), (240, 110, 90))]


def l64_house(c, d, wall, roof, door, no_flowers=None, chimney=True):
    x0, x1, top = -70, 70, -350
    if chimney:
        c.rect(x1 - 36, top - 46, x1 - 20, top, (150, 80, 70))
    c.polygon([(x0 - 8, top + 4), (0, top - 50), (x1 + 8, top + 4)], roof)
    c.rect(x0, top, x1, 0, wall)
    for r in range(3):
        for i, wx in enumerate((x0 + 16, x1 - 46)):
            y = top + 20 + r * 70
            c.rect(wx - 3, y - 3, wx + 33, y + 43, WHITE)
            c.rect(wx, y, wx + 30, y + 40, (150, 205, 240))
            c.rect(wx + 13, y, wx + 17, y + 40, WHITE)
            if (r, i) != no_flowers:
                c.rect(wx - 4, y + 42, wx + 34, y + 50, (170, 110, 70))
                for k in range(4):
                    c.circle(wx + 2 + k * 9, y + 40, 5, [(240, 80, 100), (255, 220, 70)][k % 2])
    c.round_rect(-18, -50, 18, 0, 8, door)
    c.circle(10, -24, 3, (250, 220, 120))


def l64_lighthouse(c, d):
    for x, y, r in ((790, 330, 60), (850, 320, 50), (740, 345, 40), (900, 340, 40)):
        c.ellipse(x, y, r, r * 0.55, (120, 116, 120))
    top_band = (90, 170, 100) if "lighthouse" in d else (220, 60, 60)
    c.polygon([(806, 300), (854, 300), (846, 150), (814, 150)], WHITE)
    for k, (y0, y1) in enumerate(((150, 180), (210, 240), (270, 300))):
        f0, f1 = (y0 - 150) / 150, (y1 - 150) / 150
        c.polygon([(814 - 8 * f0, y0), (846 + 8 * f0, y0), (846 + 8 * f1, y1), (814 - 8 * f1, y1)], top_band if k == 0 else (220, 60, 60))
    c.rect(808, 132, 852, 150, (60, 70, 90))
    c.rect(814, 112, 846, 134, (255, 240, 160))
    c.polygon([(806, 114), (854, 114), (830, 90)], (60, 70, 90))


def l64_fish_stall(c, d):
    c.rect(330, 440, 530, 520, (170, 120, 80))
    c.rect(330, 430, 530, 446, (150, 100, 66))
    for x in (336, 520):
        c.rect(x, 330, x + 8, 520, (130, 90, 60))
    for k in range(8):
        c.rect(326 + k * 26, 320, 352 + k * 26, 350, [(60, 140, 220), WHITE][k % 2])
        c.ellipse(339 + k * 26, 350, 13, 10, [(60, 140, 220), WHITE][k % 2], ymin=350)
    c.rect(350, 410, 510, 432, (220, 236, 245))
    for k in range(5 if "fish" in d else 6):
        fx = 368 + k * 26
        c.ellipse(fx, 420, 11, 6, (150, 170, 190))
        c.polygon([(fx - 10, 420), (fx - 18, 413), (fx - 18, 427)], (130, 150, 170))
        c.circle(fx + 6, 418, 1.5, BLACK)


def l64_fruit_stall(c, d):
    awn = [(90, 180, 90) if "awning" in d else (240, 90, 90), (255, 245, 230)]
    c.rect(600, 450, 820, 530, (190, 140, 90))
    for x in (606, 806):
        c.rect(x, 340, x + 8, 530, (150, 105, 70))
    for k in range(8):
        c.rect(596 + k * 28.5, 330, 624.5 + k * 28.5, 362, awn[k % 2])
        c.ellipse(610 + k * 28.5, 362, 14.25, 10, awn[k % 2], ymin=362)
    for k, col in enumerate(((240, 60, 60), (255, 170, 40), (240, 220, 60), (120, 190, 80))):
        bx = 618 + k * 50
        c.rect(bx, 430, bx + 44, 452, (160, 110, 70))
        if k == 1 and "crate" in d:
            col = (150, 90, 200)
        for j in range(5):
            c.circle(bx + 6 + j * 8, 428 - (j % 2) * 4, 7, col)


def l64_bollard(c, d, buoy):
    c.round_rect(-9, -40, 9, 0, 4, (110, 80, 60))
    c.rect(-12, -44, 12, -36, (90, 64, 50))
    if buoy:
        c.ellipse_ring(0, -22, 20, 20, 8, (240, 80, 70))


def l64_barrels(c, d):
    for x in (-20, 20):
        c.round_rect(x - 18, -60, x + 18, 0, 8, (160, 110, 70))
        c.rect(x - 18, -46, x + 18, -42, (110, 80, 60))
        c.rect(x - 18, -16, x + 18, -12, (110, 80, 60))


def l64_crates(c, d):
    for x, y in ((-26, 0), (26, 0), (0, -40)):
        c.rect(x - 24, y - 40, x + 24, y, (190, 150, 100))
        c.line(x - 24, y - 40, x + 24, y, 3, (150, 110, 70))


def l64_person(c, d, shirt, hair):
    person(c, 0, 0, shirt, hair=hair, s=1.3)


def l64_boat(c, m, hull, sail):
    c.polygon([(-50, 0), (50, 0), (36, 20), (-36, 20)], hull)
    c.line(0, 0, 0, -90, 3, (110, 90, 70))
    c.polygon([(2, -88), (2, -6), (46, -6)], sail)
    c.polygon([(-2, -70), (-2, -6), (-34, -6)], lit(sail, 0.9))


def l64_bg(c, d):
    v = V64
    c.gradient(0, v.hz + 2, (120, 196, 245), (230, 242, 252))
    c.ellipse(700, v.hz + 2, 230, 26, (176, 206, 196), ymax=v.hz + 1)
    c.ellipse(900, v.hz + 2, 150, 16, (190, 214, 206), ymax=v.hz + 1)
    c.ellipse(180, v.hz + 2, 240, 30, (180, 206, 200), ymax=v.hz + 1)
    # quay street (cobbles in perspective)
    c.rect(0, v.hz, W, H + 10, (196, 186, 172))
    rows = [y for y in v.ground_rows(0.07) if y > v.hz + 3]
    rnd = random.Random(64)
    stones = ((214, 204, 190), (206, 196, 182), (222, 212, 198))
    for i in range(len(rows) - 1):
        y0, y1 = rows[i + 1], rows[i]
        s = v.s(y1)
        sw = 30 * s
        off = (i % 2) * sw / 2
        x = -off
        xe = v.wx(QUAY_X, y1)
        while x < xe:
            c.round_rect(x + 1.5 * s, y0 + 1.2 * s, min(xe, x + sw - 1.5 * s), y1 - 1.2 * s, 4 * s, decal(rnd.choice(stones)))
            x += sw
    # sea to the right of the quay edge (with perspective wave dashes)
    yb = H + 20
    c.polygon([(v.wx(QUAY_X, v.hz + 0.5), v.hz + 0.5), (W + 10, v.hz + 0.5), (W + 10, yb), (v.wx(QUAY_X, yb), yb)], decal((52, 130, 196)))
    c.polygon([(0, v.hz), (W, v.hz), (W, v.hz + 3), (0, v.hz + 3)], decal((70, 146, 206)))
    for y in v.ground_rows(0.09):
        s = v.s(y)
        for k in range(14):
            X = QUAY_X + 40 + k * 110 + (int(y) * 37 % 90)
            x = v.wx(X, y)
            if x < W:
                c.line(x, y, x + 34 * s, y, max(1.0, 3 * s), decal((110, 180, 230)))
    # quay kerb
    c.polygon([(v.wx(QUAY_X - 14, v.hz + 1), v.hz + 1), (v.wx(QUAY_X, v.hz + 1), v.hz + 1), (v.wx(QUAY_X, yb), yb), (v.wx(QUAY_X - 14, yb), yb)],
              decal((170, 160, 150)))
    objs = [(271, XF_LIGHTHOUSE, l64_lighthouse, (d,)), (455, XF_FISH, l64_fish_stall, (d,)), (590, XF_FRUIT, l64_fruit_stall, (d,))]
    # houses: rows at receding depths along the left side of the street
    walls = [((250, 210, 150), (200, 90, 70), (60, 120, 180)), ((240, 190, 200), (150, 80, 110), (90, 140, 90)),
             ((200, 226, 190), (90, 140, 100), (190, 90, 60)), ((250, 230, 170), (190, 110, 60), (80, 100, 170))]
    for j, y in enumerate((440, 370, 330, 305, 290, 280)):
        s = v.s(y) * HOUSE_K
        right = v.wx(-150, y)
        for n in range(4):
            cx = right - 70 * s - n * 140 * s
            if cx + 70 * s < 0:
                break
            wall, roof, door = walls[(j + n) % len(walls)]
            objs.append((y, v.at(cx, y, HOUSE_K), l64_house, (d, wall, roof, door)))
    objs.append((600, XF_HOUSE, l64_house, (d, (180, 210, 230), (90, 110, 160), (160, 80, 180) if "door" in d else (200, 70, 70),
                                            (1, 1) if "flowers" in d else None, "chimney" not in d)))
    objs.append((600, v.at(XF_HOUSE.x - 140 * XF_HOUSE.s, 600, HOUSE_K), l64_house, (d, (250, 210, 150), (200, 90, 70), (60, 120, 180))))
    objs.append((600, v.at(XF_HOUSE.x - 280 * XF_HOUSE.s, 600, HOUSE_K), l64_house, (d, (240, 190, 200), (150, 80, 110), (90, 140, 90))))
    for y in (300, 330, 380, 460):
        objs.append((y, v.atX(QUAY_X - 10, y), l64_bollard, (d, y == 460)))
    objs.append((500, v.atX(105, 500), l64_barrels, (d,)))
    objs.append((395, v.atX(70, 395, 1.0), l64_crates, (d,)))
    for X, y, shirt, hair in ((-60, 330, (240, 120, 100), (60, 40, 30)), (40, 352, (110, 190, 120), (40, 30, 30)),
                              (-110, 410, (90, 150, 220), (230, 190, 90)), (60, 470, (200, 100, 140), (230, 190, 90)),
                              (100, 566, (240, 170, 60), (40, 30, 30))):
        objs.append((y, v.atX(X, y), l64_person, (d, shirt, hair)))
    draw_sorted(c, objs)


def l64_cat(c, m):
    c.ellipse(-30, -398, 14, 10, (70, 70, 80))
    c.circle(-17, -409, 8, (70, 70, 80))
    c.polygon([(-23, -414), (-21, -423), (-17, -415)], (70, 70, 80))
    c.polygon([(-15, -415), (-11, -423), (-10, -413)], (70, 70, 80))


def l64_tail(c, m):
    c.line(-43, -395, -55, -407, 4, (70, 70, 80))
    c.line(-55, -407, -53, -421, 4, (70, 70, 80))


def l64_beam(c, m):
    c.polygon([(830, 123), (690, 100), (690, 146)], (255, 250, 200, 0.45))


L64_ELEMENTS = clouds_drift("cloud", [(360, 40, 1.0), (620, 30, 1.1), (520, 90, 0.5), (760, 105, 0.3)], speed=10) + [
    E("boat%d" % i, V64.at(x, y, k, anchor=(0, 20)).draw(l64_boat, hull, sail), pivot=V64.at(x, y, k, anchor=(0, 20)).p(0, 20),
      anim=dict(swingAngle=3, swingSpeed=0.22 + i * 0.03, bobAmplitude=(0, 3 * V64.s(y) * k), bobSpeed=0.3, phase=i * 0.3))
    for i, (x, y, k, hull, sail) in enumerate(BOATS)
] + [
    E("beam", XF_LIGHTHOUSE.draw(l64_beam), pivot=XF_LIGHTHOUSE.p(830, 123), anim=dict(swingAngle=12, swingSpeed=0.12)),
    E("cat", XF_HOUSE.draw(l64_cat)),
    E("tail", XF_HOUSE.draw(l64_tail), pivot=XF_HOUSE.p(-43, -395), anim=dict(swingAngle=18, swingSpeed=0.6)),
] + birds_fly("gull", [(420, 90, 16), (460, 70, 12), (700, 170, 9), (640, 220, 5)], col=(250, 250, 250))

L64_DIFFS = [
    ("lighthouse", *XF_LIGHTHOUSE.p(830, 165), 0),
    ("door", *XF_HOUSE.p(0, -25), 0),
    ("flowers", *XF_HOUSE.p(39, -220), 0),
    ("chimney", *XF_HOUSE.p(42, -373), 0),
    ("fish", *XF_FISH.p(498, 420), 0),
    ("awning", *XF_FRUIT.p(700, 345), 0),
    ("crate", *XF_FRUIT.p(690, 430), 0),
]


# =================================================================== Level 65 winter village at dusk
V65 = View(hz=318, vpx=450, yref=600, haze=(200, 184, 214), haze_k=0.55)
SNOW = (246, 248, 255)
SNOW_SH = (214, 222, 242)
WARM = (255, 214, 120)
XF_HOUSE65 = V65.atX(330, 440, 2.1)
XF_TREE = V65.atX(-40, 455, 1.8, anchor=(470, 462))
XF_SLED = V65.atX(230, 545, 1.0, anchor=(645, 546))
XF_SNOWMAN = V65.atX(375, 598, 1.0, anchor=(800, 590))
POND = (V65.wx(-330, 540), 540)


def snow_house(c, d, wall, roof, lit_wins=(True, True), wreath=False, chimney=True):
    x0, x1, base, h = -70, 70, 0, 100
    top = base - h
    if chimney:
        c.rect(x1 - 40, top - 52, x1 - 22, top - 10, (140, 80, 70))
        c.rect(x1 - 44, top - 58, x1 - 18, top - 48, SNOW)
    c.rect(x0, top, x1, base, wall)
    c.polygon([(x0 - 14, top + 4), (0, top - 52), (x1 + 14, top + 4)], roof)
    c.polygon([(x0 - 16, top + 6), (0, top - 56), (x1 + 16, top + 6), (x1 + 16, top - 2), (0, top - 62), (x0 - 16, top - 2)], SNOW)
    for k in range(int((x1 - x0) / 18)):
        ix = x0 - 10 + k * 18 + 9
        c.polygon([(ix - 4, top + 4), (ix + 4, top + 4), (ix, top + 14 + (k % 3) * 4)], (220, 236, 252))
    for i, wx in enumerate((x0 + 14, x1 - 44)):
        c.rect(wx - 3, top + 20, wx + 33, top + 56, (110, 80, 60))
        c.rect(wx, top + 23, wx + 30, top + 53, WARM if lit_wins[i] else (60, 70, 110))
        c.rect(wx + 13, top + 23, wx + 17, top + 53, (110, 80, 60))
        c.rect(wx - 4, top + 54, wx + 34, top + 60, SNOW)
    c.round_rect(-14, base - 44, 14, base, 6, (120, 70, 50))
    if wreath:
        c.ellipse_ring(0, base - 30, 9, 9, 5, (50, 130, 70))
        c.circle(0, base - 22, 3, (220, 40, 50))


def l65_tree(c, d):
    tx = 470
    c.rect(tx - 12, 420, tx + 12, 450, (110, 75, 50))
    for k in range(4):
        top = 150 + k * 62
        w = 50 + k * 26
        c.polygon([(tx, top), (tx - w, top + 90), (tx + w, top + 90)], (40, 110, 70))
        c.polygon([(tx, top), (tx - w * 0.5, top + 30), (tx - w * 0.2, top + 24), (tx + w * 0.1, top + 32), (tx + w * 0.5, top + 28)], SNOW)
    for k in range(3):
        y = 230 + k * 62
        c.line(tx - 40 - k * 22, y + 10, tx + 40 + k * 22, y + 30, 4, (230, 60, 70))
    c.star(tx, 142, 22, 9, (240, 240, 250) if "star" in d else (255, 210, 50))
    for k in range(5):
        gx, gy = tx - 70 + k * 34, 460 - (k % 2) * 6
        col = [(220, 60, 70), (70, 140, 220), (250, 200, 60), (150, 90, 200), (70, 170, 110)][k]
        c.rect(gx - 13, gy - 22, gx + 13, gy, col)
        c.rect(gx - 2, gy - 22, gx + 2, gy, (255, 240, 200))


def l65_lamp(c, d):
    c.ellipse(0, -96, 40, 40, (255, 230, 160, 0.22))
    c.line(0, 0, 0, -90, 5, (50, 60, 80))
    c.round_rect(-9, -102, 9, -82, 4, (255, 236, 170))
    c.polygon([(-12, -100), (12, -100), (0, -112)], (50, 60, 80))


def l65_sled(c, d):
    sled = (60, 130, 220) if "sled" in d else (220, 60, 60)
    c.round_rect(600, 520, 690, 536, 6, sled)
    c.line(596, 546, 690, 546, 4, (120, 80, 60))
    c.line(600, 536, 604, 546, 3, (120, 80, 60))
    c.line(684, 536, 680, 546, 3, (120, 80, 60))
    c.line(600, 546, 590, 534, 4, (120, 80, 60))


def l65_snowman(c, d):
    sx = 800
    c.ellipse(sx, 590, 70, 12, decal(SNOW_SH))
    for y, r in ((548, 44), (486, 32), (440, 24)):
        c.circle(sx, y, r + 2.5, (170, 184, 220))
        c.circle(sx, y, r, (226, 232, 250))
        c.circle(sx - r * 0.18, y - r * 0.18, r * 0.8, WHITE)
    scarf = (60, 160, 90) if "scarf" in d else (220, 50, 60)
    c.round_rect(sx - 26, 456, sx + 26, 468, 5, scarf)
    c.rect(sx + 8, 462, sx + 20, 500, scarf)
    c.rect(sx - 22, 400, sx + 22, 418, (40, 40, 50))
    c.rect(sx - 30, 414, sx + 30, 420, (40, 40, 50))
    for ex in (-8, 8):
        c.circle(sx + ex, 434, 3, BLACK)
    if "nose" not in d:
        c.polygon([(sx, 440), (sx + 26, 444), (sx, 448)], (255, 140, 40))
    for by in (480, 500, 540, 562):
        c.circle(sx, by, 3.5, BLACK)
    c.line(sx - 30, 480, sx - 70, 452, 3, (110, 75, 50))
    c.line(sx + 30, 480, sx + 68, 456, 3, (110, 75, 50))


def l65_pine(c, d):
    pine(c, 0, 0, 120, (40, 90, 80), snow=(230, 238, 252))


def l65_person(c, d, shirt, hat):
    person(c, 0, 0, shirt, hair=(60, 40, 30), s=1.2)
    c.ellipse(0, -79, 13, 8, hat, ymax=-77)


def l65_bg(c, d):
    v = V65
    c.gradient(0, v.hz + 2, (40, 50, 110), (250, 172, 152))
    c.circle(130, 80, 34, (250, 246, 230))
    # mountains and the forest band far away (small, hazy)
    c.polygon([(-20, 290), (120, 200), (230, 250), (360, 180), (520, 270), (660, 190), (800, 250), (920, 210), (920, v.hz + 2), (-20, v.hz + 2)],
              (170, 168, 206))
    for px, py in ((120, 200), (360, 180), (660, 190), (920, 210)):
        c.polygon([(px, py), (px - 26, py + 30), (px - 9, py + 22), (px + 5, py + 32), (px + 26, py + 27)], (236, 236, 250))
    rnd = random.Random(65)
    for k in range(70):
        x = k * 13 + rnd.uniform(-4, 4)
        pine(c, x, v.hz + 2, rnd.uniform(16, 30), (96, 110, 140), snow=(214, 214, 236))
    # snowy ground + path to the horizon with footprints
    c.rect(0, v.hz, W, H + 10, SNOW)
    yb = H + 20
    c.polygon([(v.wx(-120, yb), yb), (v.wx(-120, v.hz + 1), v.hz + 1), (v.wx(120, v.hz + 1), v.hz + 1), (v.wx(120, yb), yb)],
              decal((224, 230, 248)))
    for y in v.ground_rows(0.18):
        s = v.s(y)
        for X in (-26, 26):
            c.ellipse(v.wx(X + (8 if X > 0 else -8) * math.sin(y), y), y, 6 * s, 3 * s, decal((200, 208, 232)))
    for X, y, rx in ((-500, 380, 260), (520, 370, 300), (-150, 470, 120)):
        c.ellipse(v.wx(X, y), y, rx * v.s(y), 26 * v.s(y), decal((236, 240, 252)))
    # frozen pond (a flat ellipse in perspective)
    px, py = POND
    s = v.s(py)
    c.ellipse(px, py, 230 * s, 62 * s, decal((170, 210, 236)))
    c.ellipse(px - 20 * s, py - 8 * s, 150 * s, 32 * s, decal((196, 226, 246)))
    for dx, dy in ((-100, -6), (40, 22), (100, -10)):
        c.line(px + dx * s, py + dy * s, px + (dx + 40) * s, py + (dy - 4) * s, 2, decal(WHITE))
    objs = [(455, XF_TREE, l65_tree, (d,)), (545, XF_SLED, l65_sled, (d,)), (598, XF_SNOWMAN, l65_snowman, (d,)),
            (440, XF_HOUSE65, snow_house, (d, (230, 200, 150), (90, 70, 110), (True, "window" not in d), "wreath" not in d,
                                           "chimney" not in d))]
    houses = [(-300, 338, (200, 120, 90), (120, 60, 60)), (-330, 372, (240, 220, 190), (150, 70, 60)), (-360, 420, (150, 180, 210), (70, 90, 130)),
              (300, 340, (150, 180, 210), (70, 90, 130)), (330, 378, (200, 120, 90), (120, 60, 60)), (-600, 520, (230, 200, 150), (110, 70, 60))]
    for X, y, wall, roof in houses:
        objs.append((y, v.atX(X, y, 2.1), snow_house, (d, wall, roof, (True, X > 0), X < 0)))
    for X, y in ((-150, 345), (150, 345), (-160, 395), (160, 395), (-170, 520), (170, 520)):
        objs.append((y, v.atX(X, y, 1.3), l65_lamp, (d,)))
    for X, y in ((-220, 330), (230, 332), (-420, 350), (440, 352), (-520, 400), (560, 398), (600, 470), (-480, 610), (680, 590)):
        objs.append((y, v.atX(X, y, 2.0), l65_pine, (d,)))
    for X, y, shirt, hat in ((60, 360, (60, 120, 200), (220, 60, 70)), (-60, 400, (220, 90, 80), (60, 120, 200)),
                             (90, 505, (90, 170, 110), (240, 200, 60))):
        objs.append((y, v.atX(X, y), l65_person, (d, shirt, hat)))
    draw_sorted(c, objs)


def l65_skater(c, m):
    c.line(-4, 0, -8, -20, 4, (60, 60, 90))
    c.line(4, 0, 10, -20, 4, (60, 60, 90))
    c.round_rect(-9, -44, 9, -18, 5, (240, 120, 60))
    c.line(-9, -38, -24, -30, 3, (240, 120, 60))
    c.line(9, -38, 24, -30, 3, (240, 120, 60))
    c.circle(0, -52, 8, (250, 210, 170))
    c.ellipse(0, -56, 9, 6, (80, 140, 220), ymax=-55)
    c.line(-10, 2, -2, 2, 2, (200, 200, 220))
    c.line(4, 2, 12, 2, 2, (200, 200, 220))


def smoke_el(eid, xf, i, show="both"):
    x, y = xf.p(39, -160)
    s = xf.s
    return E(eid, lambda c, m: c.circle(x, y, 9 * s, (220, 222, 236)), show=show,
             anim=dict(driftVelocity=(6 * s, 18 * s), driftLength=80 * s, driftFade=True, driftGrow=1.2, phase=i / 3))


def l65_lights(k):
    rnd = random.Random(650 + k)
    pts = []
    for row in range(4):
        top = 150 + row * 62
        w = 50 + row * 26
        for j in range(3):
            t = rnd.uniform(0.35, 0.95)
            pts.append((470 + rnd.uniform(-w, w) * t, top + 90 * t))
    col = [(255, 230, 120), (255, 120, 140), (130, 210, 255)][k]

    def d(c, m):
        for x, y in pts:
            c.circle(x, y, 5, col)
            c.circle(x - 1.5, y - 1.5, 2, (255, 255, 240))
    return d


def snow_sheet(seed, n, r0, r1):
    rnd = random.Random(seed)
    flakes = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(r0, r1)) for _ in range(n)]

    def d(c, m):
        for x, y, r in flakes:
            c.circle(x, y, r, (255, 255, 255, 0.85))
    return d


STARS65 = [(40, 30), (220, 40), (300, 110), (420, 30), (560, 70), (640, 20), (760, 60), (870, 30), (520, 140), (840, 120)]
SMOKE_HOUSES = [V65.atX(-300, 338, 2.1), V65.atX(300, 340, 2.1), V65.atX(-360, 420, 2.1)]
_PS = V65.s(POND[1])

L65_ELEMENTS = [
    E("star%d" % i, (lambda x, y: lambda c, m: c.star(x, y, 4, 1.6, (255, 250, 220)))(x, y),
      anim=dict(twinkle=0.7, twinkleSpeed=0.4 + (i % 3) * 0.15, phase=i * 0.17)) for i, (x, y) in enumerate(STARS65)
] + [
    smoke_el("smoke%d_%d" % (h, i), xf, i) for h, xf in enumerate(SMOKE_HOUSES) for i in range(3)
] + [
    smoke_el("smokeB%d" % i, XF_HOUSE65, i, show="A") for i in range(3)
] + [
    E("lights%d" % k, XF_TREE.draw(lambda c, m, k=k: l65_lights(k)(c, m)), anim=dict(twinkle=0.8, twinkleSpeed=0.5, phase=k / 3))
    for k in range(3)
] + [
    E("skater", V65.at(POND[0], POND[1] + 4, 1.1).draw(l65_skater), pivot=(POND[0], POND[1] + 4),
      anim=dict(orbitRadius=(150 * _PS, 30 * _PS), orbitSpeed=0.08, orbitDepth=0.12)),
    # far flakes: small and slow; near flakes: big and fast (parallax)
    E("snowFarA", snow_sheet(651, 90, 0.8, 1.6), pivot=(450, 300), anim=dict(driftVelocity=(-3, -16), driftLength=1200, driftStart=-600)),
    E("snowFarB", snow_sheet(652, 90, 0.8, 1.6), pivot=(450, 300),
      anim=dict(driftVelocity=(-3, -16), driftLength=1200, driftStart=-600, phase=0.5)),
    E("snowNearA", snow_sheet(653, 26, 3.0, 5.0), pivot=(450, 300), anim=dict(driftVelocity=(-8, -55), driftLength=1200, driftStart=-600)),
    E("snowNearB", snow_sheet(654, 26, 3.0, 5.0), pivot=(450, 300),
      anim=dict(driftVelocity=(-8, -55), driftLength=1200, driftStart=-600, phase=0.5)),
]

L65_DIFFS = [
    ("star", *XF_TREE.p(470, 142), 0),
    ("window", *XF_HOUSE65.p(41, -62), 0),
    ("wreath", *XF_HOUSE65.p(0, -30), 0),
    ("chimney", *XF_HOUSE65.p(39, -140), 0),
    ("sled", *XF_SLED.p(645, 528), 0),
    ("scarf", *XF_SNOWMAN.p(810, 470), 0),
    ("nose", *XF_SNOWMAN.p(812, 444), 0),
]

LEVELS = [paper_level(lv) for lv in [
    ("Level63", "欢乐游乐园", l63_bg, L63_ELEMENTS, L63_DIFFS, 120, OPTS),
    ("Level64", "港口集市", l64_bg, L64_ELEMENTS, L64_DIFFS, 120, OPTS),
    ("Level65", "冬日雪村", l65_bg, L65_ELEMENTS, L65_DIFFS, 120, OPTS),
]]
