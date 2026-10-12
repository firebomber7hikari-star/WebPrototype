# -*- coding: utf-8 -*-
"""
Looking out of a vehicle window (first person, the vehicle moves to the right):
  Level60 火车窗外   - train compartment, countryside, day/night
  Level61 夜行出租车 - back seat of a taxi, city at night, rain
  Level62 飞机舷窗   - airliner window above the clouds, sunset -> night

The interior is a full-picture element in front of everything; outside, the far layer is static
(background) while mid/near layers are seamless tiles scrolling to the left at different speeds (parallax).
Differences live in the interior and in the static far layer, so they never scroll away.
"""
import math
import random
import fill_levels

from fdcore import CLEAR, E, H, RAIN, W, W_, lit, on
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, cloud_bg, house, sky, tree_pine, tree_round
from stylekit import celestial, day_night, moon_element, star_field, sun_element
from weather import WET


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=40.0, frames=80)
    o.update(kw)
    return o


def scroll(eid, unit, step, speed, y0, y1, ks=range(-1, 5), **kw):
    """Seamless horizontal tile scrolling left: unit(c, m, dx) draws one period starting at x = dx."""
    def d(c, m):
        for k in ks:
            unit(c, m, k * step)
    x0, x1 = min(ks) * step - 40, (max(ks) + 1) * step + 40
    return E(eid, d, bbox=(x0, y0, x1, y1), anim=dict(driftVelocity=(-speed, 0), driftLength=step), **kw)


def window_rain(prefix, n, area, slant, speed, mask=WET, length=60):
    """Drops on the glass, pushed backwards by the wind of the moving vehicle."""
    x0, y0, x1, y1 = area
    rnd = random.Random(len(prefix) * 31 + n)
    out = []
    for i in range(n):
        x, y = rnd.uniform(x0 + 20, x1 - 20), rnd.uniform(y0 + 10, y1 - 30)

        def d(c, m, x=x, y=y):
            piece(c, [Circ(x, y, 3.2)], (220, 236, 252), border=0.8, border_col=(250, 252, 255), shadow=None)
            flat(c, Thick(x, y, x + slant[0] * 0.25, y + slant[1] * 0.25, 1.2), (230, 240, 252, 0.5))
        out.append(E("%s%d" % (prefix, i), d, daynight="untinted", weather=mask,
                     anim=dict(driftVelocity=(slant[0] * speed, -slant[1] * speed), driftLength=length, driftFade=True, phase=(i * 0.37) % 1)))
    return out


# =================================================================== 60 train window (countryside, day/night)
DN60 = day_night(40.0, tint=(0.30, 0.32, 0.56))
SUN60, MOON60 = celestial((450, 150), (420, 100), 40.0)
WIN60 = (140, 50, 760, 370)


def l60_bg(c, d):
    sky(c, (120, 180, 236), (230, 238, 246))
    # far mountains with a hilltop castle (static)
    piece(c, Poly([(-20, 300), (120, 190), (230, 240), (360, 160), (500, 250), (640, 170), (780, 230), (920, 200), (920, 330), (-20, 330)]),
          (150, 170, 200), shadow=LAYER)
    for px, py in ((120, 190), (360, 160), (640, 170)):
        flat(c, Poly([(px, py), (px - 20, py + 22), (px - 6, py + 16), (px + 6, py + 24), (px + 20, py + 20)]), (250, 252, 255))
    piece(c, [RRect(486, 226, 520, 252, 1), RRect(482, 210, 494, 232, 1), RRect(512, 210, 524, 232, 1)], (210, 200, 196), shadow=SMALL)
    if "castle" not in d:
        piece(c, [Thick(518, 210, 518, 192, 1.6), Poly([(519, 192), (532, 196), (519, 200)])], (220, 60, 60), shadow=None)
    piece(c, Poly([(-20, 330), (920, 320), (920, 380), (-20, 380)]), (130, 180, 120), shadow=LAYER)
    # a lake in the distance (shape differs)
    if "lake" in d:
        piece(c, Ell(250, 334, 60, 6), (120, 180, 220), shadow=None)
    else:
        piece(c, Ell(250, 334, 90, 8), (120, 180, 220), shadow=None)


def l60_hills(c, m, dx):
    for k in range(2):
        x = dx + k * 225
        piece(c, Ell(x + 110, 360, 150, 40), (110, 170, 100), shadow=(1, 3, 6, 0.25))
    house(c, dx + 120, 352, 50, 30, (246, 236, 214), (200, 80, 70), wins=1)
    tree_round(c, dx + 330, 360, 0.6, (80, 150, 85))


def l60_near(c, m, dx):
    flat(c, Thick(dx + 40, 60, dx + 40, 380, 7), (110, 86, 70))
    flat(c, Thick(dx + 26, 90, dx + 54, 90, 4), (110, 86, 70))
    pts = [(dx + 40 + t * 30, 92 + 26 * math.sin(math.pi * t / 10)) for t in range(11)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.4) for i in range(10)], (60, 50, 50))
    flat(c, Poly([(dx, 380), (dx + 300, 380), (dx + 300, 360), (dx + 200, 352), (dx + 100, 362), (dx, 356)]), (80, 140, 70))


def l60_interior(c, m):
    x0, y0, x1, y1 = WIN60
    wall = (150, 108, 80)
    flat(c, [RRect(-10, -10, W + 10, y0 + 10, 0), RRect(-10, y1 - 10, W + 10, H + 10, 0), RRect(-10, -10, x0 + 10, H + 10, 0),
             RRect(x1 - 10, -10, W + 10, H + 10, 0)], wall)
    for x in range(0, 900, 30):
        if not (x0 < x < x1):
            flat(c, Thick(x, 0, x, 600, 1.2), lit(wall, 0.9))
    # rounded window frame
    piece(c, [RRect(x0 - 14, y0 - 14, x1 + 14, y0 + 6, 6), RRect(x0 - 14, y1 - 6, x1 + 14, y1 + 14, 6), RRect(x0 - 14, y0 - 14, x0 + 6, y1 + 14, 6),
              RRect(x1 - 6, y0 - 14, x1 + 14, y1 + 14, 6)], (200, 180, 140), shadow=PROP)
    flat(c, Thick(x0, (y0 + y1) / 2 - 40, x1, (y0 + y1) / 2 - 40, 4), (200, 180, 140))
    # curtains (left one changes colour)
    for cx0, cx1, col in ((x0 - 30, x0 + 40, (60, 140, 90) if on("curtain", m) else (180, 60, 70)), (x1 - 40, x1 + 30, (180, 60, 70))):
        piece(c, Poly([(cx0, y0 - 20), (cx1, y0 - 20), (cx1 - 10, y0 + 100), (cx1, y1 + 10), (cx0, y1 + 10)]), col, border=1.5, shadow=PROP)
        for k in range(3):
            xx = cx0 + 12 + k * 18
            flat(c, Thick(xx, y0 - 16, xx - 4, y1 + 6, 2), lit(col, 0.8))
    # luggage rack + bag
    flat(c, Thick(0, 30, 900, 30, 4), (180, 180, 190))
    piece(c, RRect(560, 0, 680, 28, 6), (90, 140, 210) if on("bag", m) else (230, 170, 60), border=1.5, shadow=SMALL)
    # table with a cup, book, orange and ticket
    piece(c, [RRect(200, 400, 700, 426, 4), RRect(430, 426, 470, 600, 2)], (190, 150, 110), border=2, shadow=PROP)
    piece(c, [RRect(300, 360, 330, 400, 5), Thick(330, 372, 340, 386, 3)], (250, 250, 250), border=1.5, shadow=SMALL)
    flat(c, Ell(315, 364, 13, 3), (150, 90, 50))
    book = (90, 120, 200) if on("book", m) else (200, 80, 70)
    piece(c, Poly([(400, 400), (520, 392), (522, 380), (402, 388)]), book, border=1.5, shadow=SMALL)
    if not on("orange", m):
        piece(c, Circ(580, 388, 13), (250, 160, 50), border=1.2, shadow=SMALL)
        flat(c, Ell(580, 376, 4, 2), (90, 150, 80))
    piece(c, RRect(620, 394, 670, 402, 1), (250, 236, 200), border=1, shadow=None)
    # seats
    piece(c, [RRect(20, 300, 120, 600, 20), RRect(780, 300, 880, 600, 20)], (60, 90, 140), border=2, shadow=PROP)
    flat(c, [RRect(30, 310, 110, 340, 8), RRect(790, 310, 870, 340, 8)], (250, 250, 250))


def l60_strap(c, m):
    flat(c, Thick(220, 30, 220, 80, 3), (90, 90, 100))
    c.ellipse_ring(220, 92, 12, 12, 3, (230, 230, 240))


def l60_steam(i):
    def d(c, m):
        piece(c, Circ(315, 352, 5), (250, 250, 252), shadow=None)
    return E("steam%d" % i, d, show="A", anim=dict(driftVelocity=(-6, 18), driftLength=40, driftFade=True, driftGrow=1.0, phase=i / 3))


L60_EL = [
    star_field("stars", 60, 60, 300),
    moon_element("moon", (450, 150), MOON60),
    sun_element("sun", (450, 150), SUN60, r=22),
    E("cloud1", lambda c, m: cloud_bg(c, 300, 90, 0.8), anim=dict(driftVelocity=(-6, 0), driftLength=1100, driftStart=-500, phase=500 / 1100)),
    scroll("hills", l60_hills, 450, 40, 300, 400, ks=range(-1, 3)),
    scroll("near", l60_near, 300, 260, 50, 390),
    E("lamp_glow", lambda c, m: soft_union(c, [Circ(450, 40, 30)], (255, 220, 150), 0.4, spread=50), daynight="night"),
    E("interior", l60_interior, variant=True),
    E("strap", l60_strap, pivot=(220, 30), anim=dict(swingAngle=8, swingSpeed=0.5)),
] + [l60_steam(i) for i in range(3)]
L60_DIFFS = [("curtain", 145, 170, 0), ("bag", 620, 14, 0), ("book", 460, 392, 0), ("orange", 600, 390, 0), ("castle", 524, 196, 0),
             ("lake", 250, 334, 0), ("steam", 312, 336, 30)]


# =================================================================== 61 night taxi (city, rain)
STEPS61 = [(CLEAR, 10), (RAIN, 16)]
WIN61 = [(120, 70), (800, 70), (830, 380), (90, 380)]


def l61_bg(c, d):
    c.gradient(0, 600, (14, 12, 40), (60, 30, 80))
    rnd = random.Random(61)
    x = -10
    while x < 920:
        w, h = rnd.randint(40, 80), rnd.randint(120, 260)
        piece(c, RRect(x, 380 - h, x + w, 400, 1), (40, 36, 80), shadow=None)
        for y in range(380 - h + 10, 380, 14):
            for xx in range(x + 6, x + w - 8, 12):
                if rnd.random() < 0.35:
                    flat(c, RRect(xx, y, xx + 6, y + 7, 1), rnd.choice(((255, 220, 120), (120, 220, 255))) + (0.8,))
        x += w + rnd.randint(2, 8)
    # big billboard on the skyline (colour differs)
    bb = (60, 220, 160) if "billboard" in d else (255, 70, 180)
    soft_union(c, [RRect(560, 110, 720, 170, 4)], bb, 0.45, spread=16)
    piece(c, RRect(560, 110, 720, 170, 4), lit(bb, 0.5), border=2, border_col=bb, shadow=None)
    for k in range(4):
        flat(c, Thick(576 + k * 36, 128, 596 + k * 36, 152, 4), bb)
    soft_union(c, [Circ(180, 90, 26)], (255, 250, 220), 0.3, spread=20)
    flat(c, Circ(180, 90, 22), (250, 246, 225))


def l61_mid(c, m, dx):
    cols = ((255, 80, 160), (80, 220, 255), (255, 210, 80))
    for k in range(3):
        x = dx + k * 140
        piece(c, RRect(x, 230, x + 120, 420, 1), (30, 26, 60), shadow=None)
        for y in range(244, 410, 18):
            flat(c, RRect(x + 10, y, x + 110, y + 8, 1), (255, 220, 140, 0.45))
        col = cols[k]
        soft_union(c, [RRect(x + 20, 260, x + 100, 280, 3)], col, 0.4, spread=10)
        flat(c, RRect(x + 20, 260, x + 100, 280, 3), col)


def l61_lights(c, m, dx):
    flat(c, Thick(dx + 60, 120, dx + 60, 400, 5), (70, 70, 90))
    flat(c, Thick(dx + 60, 124, dx + 100, 124, 4), (70, 70, 90))
    soft_union(c, [Circ(dx + 100, 130, 10)], (255, 220, 150), 0.6, spread=30)
    flat(c, Circ(dx + 100, 130, 8), (255, 236, 180))
    flat(c, Thick(dx, 396, dx + 300, 396, 30), (40, 40, 56))
    flat(c, Thick(dx + 30, 392, dx + 150, 392, 2.5), (250, 220, 120, 0.7))


def l61_interior(c, m):
    body = (30, 30, 40)
    win = Poly(WIN61)
    # door panel and roof around the trapezoid window
    flat(c, [RRect(-10, -10, W + 10, 70, 0), RRect(-10, 380, W + 10, H + 10, 0), Poly([(-10, -10), (120, 70), (90, 380), (-10, 380)]),
             Poly([(W + 10, -10), (800, 70), (830, 380), (W + 10, 380)])], body)
    piece(c, [Thick(120, 70, 800, 70, 8), Thick(800, 70, 830, 380, 8), Thick(90, 380, 830, 380, 10), Thick(120, 70, 90, 380, 8)], (60, 60, 72), shadow=PROP)
    flat(c, Thick(470, 70, 476, 380, 14), (40, 40, 50))     # B-pillar
    # door panel details
    piece(c, RRect(60, 420, 860, 600, 16), (70, 66, 80), shadow=PROP)
    handle = (200, 170, 90) if m else (190, 190, 200)
    piece(c, RRect(620, 450, 700, 470, 8), handle, border=1.5, shadow=SMALL)
    flat(c, [Circ(200, 520, 40)], (50, 48, 58))
    for k in range(5):
        flat(c, Thick(170, 504 + k * 8, 230, 504 + k * 8, 2), (80, 76, 90))
    # side mirror outside the window (reflection of headlights only in A)
    piece(c, Poly([(830, 300), (890, 284), (896, 340), (836, 350)]), (40, 40, 50), border=2, shadow=PROP)
    flat(c, Poly([(838, 306), (884, 294), (888, 334), (842, 342)]), (70, 80, 110))
    if not m:
        soft_union(c, [Circ(860, 318, 5), Circ(874, 316, 5)], (255, 250, 210), 0.8, spread=6)
    # sticker on the glass
    if not m:
        piece(c, Circ(780, 104, 14), (255, 220, 60), border=1.2, shadow=None)
        flat(c, [Circ(775, 100, 2), Circ(785, 100, 2), Thick(774, 110, 786, 110, 1.6)], INK)


def l61_freshener(c, m):
    col = (90, 170, 230) if m else (90, 200, 110)
    flat(c, Thick(300, 70, 300, 104, 1.2), (230, 230, 230))
    piece(c, Poly([(300, 104), (286, 140), (294, 140), (282, 160), (318, 160), (306, 140), (314, 140)]), col, border=1.2, shadow=SMALL)


def l61_phone(c, m):
    col = (255, 150, 60) if m else (90, 200, 255)
    soft_union(c, [RRect(360, 440, 410, 520, 6)], col, 0.4, spread=10)
    piece(c, RRect(360, 440, 410, 520, 6), (20, 20, 30), border=2, border_col=(90, 90, 100), shadow=SMALL)
    flat(c, RRect(366, 448, 404, 512, 4), col)


def l61_bobble(c, m):
    piece(c, [RRect(530, 560, 560, 590, 4), Circ(545, 540, 16)], (240, 200, 160), border=1.5, shadow=SMALL)
    flat(c, [Circ(539, 538, 2.4), Circ(551, 538, 2.4), Thick(538, 548, 552, 548, 2)], INK)


L61_EL = [
    scroll("mid", l61_mid, 420, 90, 220, 430, ks=range(-1, 3)),
    scroll("lights", l61_lights, 300, 320, 110, 420),
    E("interior", l61_interior, variant=True),
] + window_rain("drop", 12, (120, 70, 800, 380), (-1.0, 0.35), 110, length=140) + [
    E("freshener", l61_freshener, variant=True, pivot=(300, 70), anim=dict(swingAngle=12, swingSpeed=0.4)),
    E("phone", l61_phone, variant=True, daynight="untinted", anim=dict(twinkle=0.1, twinkleSpeed=1.0)),
    E("bobble", l61_bobble, pivot=(545, 556), anim=dict(swingAngle=14, swingSpeed=0.9), animB={}),
]
L61_DIFFS = [("billboard", 640, 140, 0), ("freshener", 300, 130, 0), ("phone", 385, 480, 0), ("handle", 660, 460, 0), ("mirror", 866, 318, 0),
             ("sticker", 780, 104, 0), ("bobble", 545, 545, 44)]


# =================================================================== 62 airliner window (sunset -> night)
DN62 = day_night(40.0, tint=(0.32, 0.28, 0.56), phase=0.1)
SUN62, MOON62 = celestial((450, 180), (420, 90), 40.0)
OVAL = (450, 250, 220, 180)


def l62_bg(c, d):
    sky(c, (90, 140, 220), (255, 196, 150))
    # ground far below (static); everything that differs sits inside the oval window
    piece(c, Poly([(-20, 290), (920, 290), (920, 620), (-20, 620)]), (130, 160, 110), shadow=None)
    rnd = random.Random(62)
    for _ in range(26):
        x, y = rnd.uniform(200, 700), rnd.uniform(296, 420)
        flat(c, Poly([(x, y), (x + 50, y + 4), (x + 46, y + 26), (x - 4, y + 22)]),
             rnd.choice(((150, 180, 110), (190, 180, 110), (120, 150, 100), (170, 190, 130))))
    field = (220, 120, 140) if "field" in d else (196, 186, 110)
    flat(c, Poly([(300, 380), (360, 384), (356, 410), (296, 406)]), field)
    pts = [(x, 318 + 14 * math.sin(x * 0.012)) for x in range(-20, 940, 20)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 5) for i in range(len(pts) - 1)], (110, 160, 210))
    if "lake" in d:
        flat(c, Ell(400, 352, 30, 10), (110, 160, 210))
    else:
        flat(c, [Ell(400, 352, 44, 14), Ell(432, 362, 22, 9)], (110, 160, 210))
    for k in range(12):
        flat(c, RRect(500 + (k % 4) * 12, 340 + (k // 4) * 10, 508 + (k % 4) * 12, 347 + (k // 4) * 10, 1), (200, 200, 210))


def l62_wing(c, m):
    """The wing is closer than any cloud, so it is an element drawn after the scrolling cloud layers."""
    piece(c, Poly([(900, 300), (500, 372), (490, 392), (900, 392)]), (226, 230, 238), border=2, shadow=PROP)
    flat(c, Poly([(900, 300), (500, 372), (540, 370), (900, 318)]), (250, 252, 255))
    flat(c, Circ(572, 382, 10), (90, 170, 120) if m else (220, 70, 80))
    piece(c, RRect(560, 392, 630, 416, 12), (190, 196, 206), border=1.5, shadow=SMALL)


def l62_cloud_unit(seed, y, k, col):
    def unit(c, m, dx):
        rnd = random.Random(seed)
        for _ in range(2):
            x = dx + rnd.uniform(0, 300)
            cloud_bg(c, x, y + rnd.uniform(-20, 20), k, col, shadow=(1, 3, 6, 0.2))
    return unit


def l62_interior(c, m):
    cx, cy, rx, ry = OVAL
    wall = (232, 232, 236)
    flat(c, [RRect(-10, -10, W + 10, cy - ry, 0), RRect(-10, cy + ry, W + 10, H + 10, 0), RRect(-10, -10, cx - rx, H + 10, 0),
             RRect(cx + rx, -10, W + 10, H + 10, 0)], wall)
    for a0 in range(0, 360, 3):      # fill between the oval opening and its bounding box
        a, b = math.radians(a0), math.radians(a0 + 3)
        flat(c, Poly([(cx + rx * math.cos(a), cy + ry * math.sin(a)), (cx + (rx + 110) * math.cos(a), cy + (ry + 110) * math.sin(a)),
                       (cx + (rx + 110) * math.cos(b), cy + (ry + 110) * math.sin(b)), (cx + rx * math.cos(b), cy + ry * math.sin(b))]), wall)
    c.ellipse_ring(cx, cy, rx + 24, ry + 24, 26, (210, 210, 216))
    c.ellipse_ring(cx, cy, rx + 3, ry + 3, 5, (180, 180, 190))
    # window shade (pulled lower in B)
    shade_y = cy - ry + (70 if on("shade", m) else 36)
    piece(c, RRect(cx - rx * 0.62, cy - ry - 4, cx + rx * 0.62, shade_y, 4), (246, 246, 248), border=1.5, shadow=SMALL)
    flat(c, RRect(cx - 16, shade_y - 8, cx + 16, shade_y - 2, 2), (180, 180, 190))
    # seat back + tray table with a drink and pretzels
    piece(c, RRect(-20, 460, 160, 620, 30), (150, 70, 70) if on("seat", m) else (60, 80, 130), border=2, shadow=PROP)
    piece(c, RRect(620, 470, 920, 500, 6), (210, 210, 216), border=2, shadow=PROP)
    drink = (90, 200, 120) if on("drink", m) else (230, 120, 60)
    piece(c, [Poly([(690, 470), (720, 470), (716, 430), (694, 430)])], (240, 244, 250), border=1.5, shadow=SMALL)
    flat(c, Poly([(692, 468), (718, 468), (715, 442), (695, 442)]), drink)
    if not on("pretzels", m):
        piece(c, RRect(760, 450, 820, 470, 4), (60, 120, 200), border=1.2, shadow=SMALL)
    fill_levels.interior_Level62(c)


L62_EL = [
    star_field("stars", 62, 60, 260),
    moon_element("moon", (450, 180), MOON62),
    sun_element("sun", (450, 180), SUN62, r=24),
    scroll("clouds_low", l62_cloud_unit(1, 296, 0.6, (250, 250, 255)), 300, 30, 240, 340),
    scroll("clouds_near", l62_cloud_unit(2, 180, 1.0, (246, 246, 252)), 300, 70, 110, 260),
    E("wing", l62_wing, variant=True),
    E("wing_light", lambda c, m: (soft_union(c, [Circ(496, 380, 5)], (255, 60, 60), 0.8, spread=14), flat(c, Circ(496, 380, 4.5), (255, 140, 140))),
      show="A", daynight="untinted", anim=dict(blinkInterval=1.3, blinkDuration=0.4)),
    E("interior", l62_interior, variant=True),
    E("reading_light", lambda c, m: soft_union(c, [Circ(820, 60, 20)], (255, 230, 170), 0.5, spread=60), daynight="night"),
]
L62_DIFFS = [("seat", 70, 540, 0), ("shade", 450, 104, 0), ("drink", 705, 452, 0), ("pretzels", 790, 460, 0), ("logo", 572, 382, 0), ("lake", 410, 356, 0),
             ("field", 328, 395, 0), ("light", 496, 380, 24)]


LEVELS = [
    ("Level60", "火车窗外", l60_bg, L60_EL, L60_DIFFS, 140, opts(day_night=DN60)),
    ("Level61", "夜行出租车", l61_bg, L61_EL, L61_DIFFS, 140,
     opts(weather=dict(steps=STEPS61, blend=3.0, tints={RAIN: (0.85, 0.85, 0.95)}), anim_seconds=26.0, frames=52)),
    ("Level62", "飞机舷窗", l62_bg, L62_EL, L62_DIFFS, 140, opts(day_night=DN62)),
]
