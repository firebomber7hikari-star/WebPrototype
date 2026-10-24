# -*- coding: utf-8 -*-
"""Home interiors (paper-craft front views of rooms, full-bleed, no real brands or logos):
  Level136 现代公寓·客厅   - modern apartment living room: glass wall onto the city, grey sofa, wall TV, arc lamp, robot vacuum
  Level137 现代公寓·厨房   - modern open kitchen: island with bar stools, pendant lights, steel fridge, cook at the island
  Level138 现代公寓·卧室   - modern bedroom: big window onto the city; day / night (city lights, bedside lamps)
  Level139 美式老公寓·客厅 - old American apartment living room: striped wallpaper, radiator, fire escape, CRT TV, armchair
  Level140 美式老公寓·厨房 - old American apartment kitchen: checkered floor, rounded fridge, enamel stove, laundry line outside
  Level141 美式老公寓·浴室 - old American apartment bathroom: clawfoot tub, pedestal sink, high-tank toilet, subway tiles
  Level142 欧洲庄园·门厅   - European manor entrance hall: grand staircase, crystal chandelier, portraits, armour, long-case clock
  Level143 欧洲庄园·书房   - European manor study: marble fireplace, over-mantel painting, bookcases, chesterfield, sleeping dog
  Level144 欧洲庄园·宴会厅 - European manor dining hall: long table with candelabra, tall draped windows, diners and a butler
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from fills import far_round_trees, far_skyline, wallpaper_diamonds, wallpaper_stripes
from levels_akiba import modern
from levels_daily import bookcase, loaf
from levels_europe import lady
from levels_portrait import GOLD, GOLD_D, bust, frame
from stylekit import day_night, flame

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


# =================================================================== shared props
def planks(c, y0, col, line, step=26, seed=0, board=150):
    """Wooden floor from y0 to the bottom: horizontal boards with staggered joints."""
    c.rect(0, y0, W, H, col)
    rnd = random.Random(seed)
    for y in range(int(y0), H, step):
        flat(c, Thick(0, y, W, y, 1.2), line)
        off = rnd.uniform(0, board)
        for x in range(-board, W + board, board):
            flat(c, Thick(x + off, y, x + off, y + step, 1.2), line)


def monstera(c, x, base, s=1.0, pot=(236, 234, 228), leaf=(60, 130, 84)):
    for a, ln in ((-60, 70), (-25, 90), (10, 96), (40, 80), (75, 64)):
        r = math.radians(a - 90)
        tx, ty = x + math.cos(r) * ln * s, base - 40 * s + math.sin(r) * ln * s
        flat(c, Thick(x, base - 40 * s, tx, ty, 2 * s), lit(leaf, 0.8))
        piece(c, Ell(tx, ty, 22 * s, 15 * s), leaf, shadow=SMALL)
        flat(c, Thick(tx - 14 * s, ty, tx + 14 * s, ty, 1.2 * s), lit(leaf, 1.25))
    piece(c, Poly([(x - 22 * s, base - 44 * s), (x + 22 * s, base - 44 * s), (x + 16 * s, base), (x - 16 * s, base)]), pot, border=1.2, shadow=PROP)


def sofa(c, x0, x1, base, col, h=1.0):
    piece(c, [RRect(x0 + 18, base - 120 * h, x1 - 18, base - 50 * h, 12), RRect(x0, base - 80 * h, x0 + 40, base - 8, 10),
              RRect(x1 - 40, base - 80 * h, x1, base - 8, 10), RRect(x0 + 20, base - 60 * h, x1 - 20, base - 14, 6)], col, border=1.5, shadow=PROP)
    flat(c, Thick(x0 + 40, base - 58 * h, x1 - 40, base - 58 * h, 2), lit(col, 0.85))
    for k in range(1, 3):
        x = x0 + 20 + (x1 - x0 - 40) * k / 3
        flat(c, Thick(x, base - 58 * h, x, base - 16, 1.4), lit(col, 0.85))
    flat(c, [RRect(x0 + 8, base - 8, x0 + 16, base + 4, 1), RRect(x1 - 16, base - 8, x1 - 8, base + 4, 1)], (70, 54, 44))


def pendant(eid, x, y, shade, cord=(70, 70, 76), kind="dome", glow=None, **kw):
    """Ceiling pendant (element hanging from y = 0, swings a little)."""
    def d(c, m):
        flat(c, Thick(x, 0, x, y, 1.6), cord)
        if kind == "dome":
            piece(c, Poly(half_dome(x, y + 16, 26, 18)), shade, border=1, shadow=SMALL)
        elif kind == "cone":
            piece(c, Poly([(x - 6, y), (x + 6, y), (x + 22, y + 30), (x - 22, y + 30)]), shade, border=1, shadow=SMALL)
        elif kind == "globe":
            piece(c, Circ(x, y + 18, 18), shade, border=1, shadow=SMALL)
        if glow:
            soft_union(c, [Ell(x, y + 32, 16, 6)], glow, 0.6, spread=10)
    return E(eid, d, pivot=(x, 0), anim=dict(swingAngle=2.2, swingSpeed=0.25, phase=(x * 0.007) % 1), **kw)


def half_dome(cx, base, rx, ry, n=12):
    return [(cx + rx * math.cos(math.pi * k / n), base - ry * math.sin(math.pi * k / n)) for k in range(n + 1)]


def tabletop_lamp(c, x, base, shade, stem=(190, 160, 90)):
    piece(c, [Ell(x, base - 4, 14, 5), Thick(x, base - 4, x, base - 44, 3)], stem, border=1, shadow=SMALL)
    piece(c, Poly([(x - 24, base - 40), (x + 24, base - 40), (x + 14, base - 72), (x - 14, base - 72)]), shade, border=1.2, shadow=SMALL)


def framed(c, x0, y0, x1, y1, frame_col, art):
    """Thin modern frame with mat; art(c, rect) paints the picture."""
    piece(c, RRect(x0, y0, x1, y1, 1), frame_col, border=1.2, shadow=PROP)
    flat(c, RRect(x0 + 5, y0 + 5, x1 - 5, y1 - 5, 0), (248, 246, 240))
    art(c, (x0 + 14, y0 + 14, x1 - 14, y1 - 14))


def steam(prefix, x, y, n=3, r=6, rise=(2, -16), length=46):
    return [E("%s%d" % (prefix, i), (lambda: lambda c, m: soft_union(c, [Circ(x, y, r)], (250, 250, 250), 0.7, spread=r))(),
              anim=dict(driftVelocity=rise, driftLength=length, driftFade=True, driftGrow=1.7, phase=i / n), daynight="untinted")
            for i in range(n)]


def city_window(c, x0, y0, x1, y1, seed, sky=((168, 208, 238), (214, 232, 246)), far=(180, 196, 214), near=(140, 156, 178), win=(214, 228, 240)):
    """Sky + two rows of towers seen through a window opening (call before drawing the frame)."""
    mid = (y0 + y1) / 2
    flat(c, RRect(x0, y0, x1, mid, 0), sky[0])
    flat(c, RRect(x0, mid, x1, y1, 0), sky[1])
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w, h = rnd.randint(24, 50), rnd.randint(int((y1 - y0) * 0.25), int((y1 - y0) * 0.55))
        flat(c, RRect(x, y1 - h, min(x1, x + w), y1, 0), far)
        x += w + rnd.randint(2, 8)
    x = x0 - 10
    while x < x1:
        w, h = rnd.randint(40, 80), rnd.randint(int((y1 - y0) * 0.12), int((y1 - y0) * 0.32))
        xa, xb = max(x0, x), min(x1, x + w)
        if xb > xa:
            flat(c, RRect(xa, y1 - h, xb, y1, 0), near)
            for yy in range(int(y1 - h) + 8, int(y1) - 6, 14):
                for xx in range(int(xa) + 6, int(xb) - 8, 12):
                    flat(c, RRect(xx, yy, xx + 6, yy + 7, 0), win)
        x += w + rnd.randint(4, 14)


# =================================================================== Level 136 modern living room
WALL136 = (236, 234, 228)


def l136_bg(c, d):
    c.rect(0, 0, W, 470, WALL136)
    # glass wall onto the city
    city_window(c, 24, 36, 396, 470, 1361)
    if "blimp" not in d:
        piece(c, [Ell(210, 150, 40, 14), Poly([(170, 150), (158, 138), (158, 162)])], (236, 236, 240), shadow=SMALL)
        flat(c, [RRect(200, 162, 222, 170, 2), Thick(186, 150, 236, 150, 2)], (220, 90, 80))
    piece(c, [RRect(14, 26, 406, 40, 0), RRect(14, 26, 28, 470, 0), RRect(392, 26, 406, 470, 0), RRect(144, 26, 152, 470, 0),
              RRect(266, 26, 274, 470, 0), RRect(14, 300, 406, 306, 0)], (62, 66, 74), shadow=SMALL)
    # ceiling strip
    flat(c, RRect(0, 0, W, 14, 0), (246, 245, 242))
    flat(c, Thick(0, 14, W, 14, 2), (214, 210, 204))
    # wall clock + floating shelves on the strip between glass and TV wall
    clock = (40, 44, 52) if "clock" not in d else (220, 120, 70)
    piece(c, Circ(480, 96, 30), clock, border=1.5, shadow=PROP)
    flat(c, Circ(480, 96, 24), (246, 246, 244))
    flat(c, [Thick(480, 96, 480, 78, 2.4), Thick(480, 96, 494, 104, 2.4)], INK)
    for y in (200, 290):
        piece(c, RRect(416, y, 548, y + 8, 1), (176, 130, 90), shadow=SMALL)
    for k, (w, h, col) in enumerate(((10, 30, (60, 90, 140)), (9, 26, (200, 80, 70)), (12, 32, (230, 200, 120)), (8, 24, (80, 130, 100)))):
        x = 428 + k * 14
        flat(c, RRect(x, 200 - h, x + w, 200, 1), col)
    piece(c, [Ell(520, 186, 12, 14), RRect(514, 168, 526, 176, 2)], (90, 150, 140), shadow=SMALL)
    piece(c, Poly([(430, 290), (466, 290), (458, 262), (438, 262)]), (220, 214, 204), border=1, shadow=SMALL)
    flat(c, [Ell(448, 252, 6, 14), Ell(440, 258, 5, 10), Ell(456, 258, 5, 10)], (80, 150, 90))
    piece(c, [RRect(490, 266, 540, 290, 2)], (60, 64, 72), shadow=SMALL)
    flat(c, RRect(494, 270, 536, 286, 1), (190, 200, 210))
    # TV wall: two canvases, TV, low cabinet
    piece(c, RRect(590, 60, 700, 196, 1), (250, 250, 248), border=1.2, shadow=PROP)
    flat(c, [Circ(626, 110, 22), RRect(640, 130, 690, 186, 0)], (230, 170, 90))
    flat(c, Poly([(600, 186), (660, 120), (690, 186)]), (70, 100, 130))
    piece(c, RRect(730, 60, 840, 196, 1), (250, 250, 248), border=1.2, shadow=PROP)
    flat(c, RRect(740, 70, 830, 186, 0), (236, 226, 210))
    flat(c, Circ(785, 126, 34), (70, 120, 160) if "art" not in d else (220, 90, 90))
    flat(c, Ell(800, 160, 30, 12), (230, 170, 90))
    piece(c, RRect(588, 226, 852, 384, 3), (28, 30, 36), border=1.5, shadow=PROP)
    scr = (596, 234, 844, 376)
    flat(c, RRect(*scr, 1), (150, 200, 236))
    flat(c, Poly([(596, 376), (596, 310), (660, 260), (720, 316), (780, 270), (844, 320), (844, 376)]), (90, 130, 110))
    flat(c, Poly([(640, 296), (660, 260), (680, 290)]), (246, 246, 250))
    flat(c, RRect(596, 350, 844, 376, 0), (110, 160, 100))
    if "tv" in d:
        flat(c, Circ(740, 254, 20), (255, 210, 90))
    piece(c, [RRect(560, 400, 880, 452, 3)], (150, 106, 72), border=1.5, shadow=PROP)
    flat(c, [Thick(666, 404, 666, 448, 1.4), Thick(772, 404, 772, 448, 1.4)], (126, 88, 60))
    flat(c, [RRect(606, 424, 626, 428, 1), RRect(710, 424, 730, 428, 1), RRect(816, 424, 836, 428, 1)], (60, 50, 44))
    flat(c, [RRect(576, 452, 584, 468, 1), RRect(856, 452, 864, 468, 1)], (60, 50, 44))
    piece(c, [Ell(616, 392, 16, 8), RRect(604, 380, 628, 392, 3)], (230, 228, 222), shadow=SMALL)
    # floor + rug
    planks(c, 470, (210, 180, 140), (192, 162, 124), seed=136)
    piece(c, Ell(430, 570, 360, 34), (200, 196, 190), shadow=SMALL)
    c.ellipse_ring(430, 570, 340, 28, 3, (170, 166, 160))
    # arc floor lamp
    piece(c, [Ell(88, 588, 30, 8), Thick(88, 584, 88, 240, 4)], (180, 170, 150), shadow=PROP)
    c.ellipse_ring(176, 240, 88, 110, 4, (180, 170, 150), ymax=240)
    shade = (246, 244, 238) if "lamp" not in d else (230, 180, 60)
    piece(c, Poly(half_dome(264, 274, 32, 30)), shade, border=1.2, shadow=SMALL)
    # sofa with cushions
    sofa(c, 110, 530, 548, (150, 156, 166))
    for k, (x, col) in enumerate(((190, (230, 190, 90)), (320, (70, 140, 140)), (450, (240, 236, 228)))):
        if k == 1 and "cushion" in d:
            col = (230, 110, 100)
        piece(c, Poly([(x - 34, 468), (x + 34, 468), (x + 40, 428), (x - 40, 428)]), col, border=1.2, shadow=SMALL)
    # coffee table
    piece(c, [Ell(470, 556, 116, 14), RRect(400, 556, 408, 596, 1), RRect(532, 556, 540, 596, 1)], (40, 42, 48), border=1.5, shadow=PROP)
    piece(c, Poly([(416, 548), (444, 548), (440, 520), (420, 520)]), (246, 244, 236), border=1, shadow=SMALL)
    tul = (230, 70, 80) if "vase" not in d else (250, 210, 60)
    flat(c, [Thick(424, 520, 418, 486, 2), Thick(430, 520, 430, 480, 2), Thick(436, 520, 444, 488, 2)], (80, 140, 80))
    piece(c, [Ell(418, 482, 8, 10), Ell(430, 476, 8, 10), Ell(444, 484, 8, 10)], tul, shadow=SMALL)
    piece(c, [RRect(490, 536, 554, 546, 1), RRect(494, 526, 548, 536, 1)], (60, 100, 150), shadow=SMALL)
    flat(c, RRect(494, 526, 548, 536, 1), (230, 180, 90))
    # tall plant (right)
    monstera(c, 866, 596, 1.2)


def l136_cat(c, m):
    piece(c, [Ell(250, 462, 30, 13), Circ(276, 452, 11), Poly([(268, 446), (270, 432), (276, 444)]), Poly([(280, 444), (286, 432), (287, 448)])],
          (70, 66, 72), border=1.2, shadow=SMALL)
    flat(c, [Thick(270, 452, 275, 454, 1.4), Thick(279, 454, 284, 452, 1.4)], (220, 220, 210))


def l136_vacuum(c, m):
    piece(c, [Ell(0, 592, 26, 7)], (50, 52, 58), shadow=SMALL)
    flat(c, Ell(0, 588, 22, 4), (90, 94, 104))
    flat(c, Circ(8, 588, 2.4), (90, 220, 140))


L136_ELEMENTS = [
    E("cloud1", lambda c, m: piece(c, [Ell(90, 90, 34, 14), Circ(80, 82, 14), Circ(102, 80, 16)], (250, 250, 248), shadow=SMALL),
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.06)),
    E("cloud2", lambda c, m: piece(c, [Ell(320, 76, 30, 12), Circ(312, 70, 12), Circ(330, 68, 14)], (250, 250, 248), shadow=SMALL),
      anim=dict(bobAmplitude=(8, 0), bobSpeed=0.05, phase=0.5)),
    E("cat", l136_cat, pivot=(250, 470), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
    E("vacuum", l136_vacuum, anim=drift_across(-30, 30, 30, start=120)),
    E("leaf", lambda c, m: piece(c, Ell(820, 470, 18, 11), (70, 144, 94), shadow=SMALL), pivot=(850, 500), anim=dict(swingAngle=5, swingSpeed=0.3)),
    E("lampglow", lambda c, m: soft_union(c, [Ell(264, 276, 24, 8)], (255, 236, 170), 0.55, spread=14), anim=dict(twinkle=0.12, twinkleSpeed=0.5)),
]

L136_DIFFS = [
    ("blimp", 205, 150, 0),
    ("lamp", 264, 250, 0),
    ("cushion", 320, 448, 0),
    ("vase", 430, 488, 0),
    ("tv", 740, 254, 0),
    ("art", 785, 126, 0),
    ("clock", 480, 96, 0),
]


# =================================================================== Level 137 modern kitchen
CAB137 = (246, 246, 242)
LOWER137 = (150, 176, 160)
STEEL = (196, 200, 206)


def l137_bg(c, d):
    c.rect(0, 0, W, 450, (238, 236, 230))
    flat(c, RRect(0, 0, W, 12, 0), (246, 245, 242))
    # window over the sink
    flat(c, RRect(220, 60, 410, 160, 0), (176, 214, 238))
    flat(c, RRect(220, 160, 410, 236, 0), (206, 228, 240))
    far_round_trees(c, 236, 30, (130, 180, 120), 1371, spacing=36, x0=220, x1=410)
    flat(c, RRect(220, 236, 410, 300, 0), (238, 236, 230))
    piece(c, [RRect(212, 52, 418, 62, 0), RRect(212, 52, 222, 240, 0), RRect(408, 52, 418, 240, 0), RRect(312, 52, 318, 240, 0),
              RRect(206, 232, 424, 242, 1)], (60, 64, 70), shadow=SMALL)
    # backsplash (subway tiles)
    for x0, x1 in ((20, 212), (418, 650)):
        flat(c, RRect(x0, 170, x1, 300, 0), (232, 238, 240))
        for y in range(170, 300, 14):
            off = 0 if (y // 14) % 2 else 14
            flat(c, Thick(x0, y, x1, y, 1), (210, 218, 222))
            for x in range(x0 + off, x1, 28):
                flat(c, Thick(x, y, x, y + 14, 1), (210, 218, 222))
    flat(c, RRect(222, 242, 408, 300, 0), (232, 238, 240))
    # upper cabinets + range hood
    piece(c, [RRect(20, 40, 200, 160, 2)], CAB137, border=1.5, shadow=PROP)
    flat(c, [Thick(80, 44, 80, 156, 1.2), Thick(140, 44, 140, 156, 1.2)], (220, 220, 214))
    flat(c, [RRect(72, 140, 76, 154, 1), RRect(84, 140, 88, 154, 1), RRect(132, 140, 136, 154, 1), RRect(144, 140, 148, 154, 1)], (80, 80, 86))
    piece(c, [RRect(504, 12, 560, 90, 0), Poly([(450, 150), (614, 150), (580, 90), (484, 90)])], STEEL, border=1.5, shadow=PROP)
    flat(c, RRect(456, 144, 608, 150, 0), lit(STEEL, 0.85))
    # herbs on the sill
    for k, x in enumerate((246, 300, 360)):
        if k == 2 and "herb" in d:
            continue
        piece(c, RRect(x - 14, 208, x + 14, 232, 3), (200, 110, 80), shadow=SMALL)
        flat(c, [Ell(x - 6, 196, 7, 12), Ell(x + 6, 194, 7, 13), Ell(x, 188, 6, 12)], [(80, 150, 90), (110, 170, 90), (70, 130, 100)][k])
    # counter + lower cabinets
    piece(c, RRect(10, 296, 660, 310, 2), (244, 244, 240), border=1.2, shadow=PROP)
    piece(c, RRect(20, 310, 650, 450, 0), LOWER137, shadow=SMALL)
    for x in range(20, 651, 90):
        flat(c, Thick(x, 314, x, 446, 1.4), lit(LOWER137, 0.85))
        flat(c, RRect(x + 38, 324, x + 52, 328, 1), (80, 80, 86))
    flat(c, RRect(250, 296, 380, 304, 2), (170, 176, 184))
    piece(c, [Thick(316, 296, 316, 262, 4), Thick(316, 262, 340, 262, 4)], STEEL, shadow=SMALL)
    # coffee machine + knife block
    piece(c, [RRect(50, 230, 110, 296, 4)], (50, 52, 58), border=1.2, shadow=PROP)
    flat(c, [RRect(58, 246, 102, 256, 1), RRect(66, 270, 94, 292, 1)], (110, 114, 124))
    piece(c, Poly([(150, 296), (186, 296), (180, 260), (156, 260)]), (170, 120, 80), border=1, shadow=SMALL)
    flat(c, [Thick(162, 260, 160, 246, 3), Thick(170, 260, 170, 244, 3), Thick(178, 260, 180, 248, 3)], INK)
    # cooktop + kettle
    flat(c, RRect(456, 292, 610, 298, 1), (40, 40, 46))
    kettle = (230, 80, 70) if "kettle" not in d else (70, 140, 210)
    piece(c, [Ell(500, 276, 26, 18), RRect(486, 254, 514, 262, 3), Thick(524, 272, 544, 254, 4)], kettle, border=1.2, shadow=SMALL)
    piece(c, [RRect(560, 266, 604, 292, 4)], (70, 72, 80), border=1, shadow=SMALL)
    # wall clock
    clock = (246, 246, 244) if "clock" not in d else (250, 200, 70)
    piece(c, Circ(626, 70, 24), clock, border=1.5, shadow=PROP)
    c.ellipse_ring(626, 70, 24, 24, 3, (50, 52, 58))
    flat(c, [Thick(626, 70, 626, 56, 2), Thick(626, 70, 636, 76, 2)], INK)
    # steel fridge + pantry shelf
    piece(c, RRect(664, 50, 800, 450, 6), STEEL, border=1.5, shadow=PROP)
    flat(c, Thick(668, 190, 796, 190, 2), lit(STEEL, 0.8))
    flat(c, [RRect(676, 110, 682, 170, 2), RRect(676, 206, 682, 290, 2)], (150, 154, 162))
    note = (250, 236, 120) if "note" not in d else (150, 210, 240)
    piece(c, Poly([(716, 214), (764, 210), (768, 262), (720, 266)]), note, shadow=SMALL)
    flat(c, [Thick(724, 226, 756, 224, 1.4), Thick(724, 236, 758, 234, 1.4), Thick(726, 246, 750, 244, 1.4)], (90, 90, 110))
    flat(c, [Circ(740, 212, 4), Circ(780, 100, 6), Circ(700, 140, 6)], (220, 70, 70))
    piece(c, RRect(810, 20, 900, 450, 0), (204, 168, 128), shadow=SMALL)
    for y in (120, 220, 320, 420):
        flat(c, RRect(810, y, 900, y + 6, 0), (170, 130, 94))
    jars = [(240, 200, 120), (200, 120, 80), (240, 240, 230)]
    for k, col in enumerate(jars):
        if k == 1 and "jar" in d:
            continue
        x = 826 + k * 26
        piece(c, RRect(x, 84, x + 20, 120, 3), (226, 236, 240), shadow=SMALL)
        flat(c, RRect(x + 2, 96, x + 18, 118, 2), col)
        flat(c, RRect(x - 1, 80, x + 21, 86, 1), (150, 110, 80))
    for k in range(3):
        piece(c, Ell(836 + k * 22, 210, 11, 6), [(230, 230, 226), (180, 210, 230), (230, 200, 190)][k], shadow=SMALL)
    piece(c, [RRect(822, 270, 888, 320, 3)], (190, 160, 110), shadow=SMALL)
    flat(c, [Thick(822, 284, 888, 284, 1.4), Thick(822, 300, 888, 300, 1.4)], (160, 130, 90))
    for k in range(3):
        piece(c, [Ell(838 + k * 20, 414, 10, 6), Ell(838 + k * 20, 404, 8, 10)], [(230, 120, 60), (240, 200, 80), (130, 90, 170)][k], shadow=SMALL)
    # floor
    c.rect(0, 450, W, H, (200, 198, 194))
    for y in (450, 520):
        flat(c, Thick(0, y, W, y, 1.4), (182, 180, 176))
    for x in range(0, W, 140):
        flat(c, Thick(x, 450, x, 520, 1.4), (182, 180, 176))
        flat(c, Thick(x + 70, 520, x + 70, H, 1.4), (182, 180, 176))
    # cook behind the island
    modern(c, 420, 452, (240, 240, 236), bottom=(50, 60, 80), hair=(60, 40, 30), h=2.4)
    piece(c, RRect(400, 382, 444, 420, 3), (230, 140, 90), shadow=SMALL)
    # island
    piece(c, RRect(120, 426, 640, 440, 2), (244, 244, 240), border=1.5, shadow=PROP)
    piece(c, RRect(134, 440, 626, 560, 0), (56, 66, 90), shadow=PROP)
    for x in range(134, 627, 82):
        flat(c, Thick(x, 444, x, 556, 1.4), (46, 56, 78))
    # things on the island
    piece(c, Ell(250, 420, 40, 10), (240, 240, 236), border=1, shadow=SMALL)
    fruit = (250, 150, 50) if "fruit" not in d else (140, 200, 80)
    piece(c, [Circ(232, 410, 11), Circ(254, 406, 12), Circ(274, 412, 10), Circ(244, 396, 10)], fruit, shadow=SMALL)
    flat(c, [Thick(254, 394, 258, 388, 2)], (90, 120, 60))
    piece(c, RRect(370, 414, 470, 426, 3), (200, 160, 110), border=1, shadow=SMALL)
    flat(c, [Circ(392, 412, 8), Circ(410, 413, 7)], (230, 70, 60))
    flat(c, [Ell(440, 414, 14, 5)], (110, 170, 90))
    piece(c, [RRect(540, 404, 560, 426, 3), Thick(560, 410, 568, 418, 3)], (240, 240, 236), shadow=SMALL)
    # bar stools
    for k, x in enumerate((230, 380, 530)):
        seat = (230, 190, 80) if not (k == 2 and "stool" in d) else (60, 120, 190)
        piece(c, [Thick(x - 18, 600, x - 10, 488, 3), Thick(x + 18, 600, x + 10, 488, 3), Thick(x - 15, 560, x + 15, 560, 2.4)], (60, 60, 66), shadow=SMALL)
        piece(c, RRect(x - 28, 474, x + 28, 490, 6), seat, border=1.2, shadow=PROP)


L137_ELEMENTS = [
    pendant("pend1", 230, 300, (40, 44, 50), kind="cone", glow=(255, 230, 160)),
    pendant("pend2", 380, 310, (40, 44, 50), kind="cone", glow=(255, 230, 160)),
    pendant("pend3", 530, 300, (40, 44, 50), kind="cone", glow=(255, 230, 160)),
    E("knife", lambda c, m: flat(c, [Thick(430, 400, 452, 384, 3), Thick(452, 384, 466, 374, 2)], (210, 214, 220)), pivot=(430, 400),
      anim=dict(swingAngle=8, swingSpeed=1.2)),
] + steam("steam", 492, 256, n=3, r=5)

L137_DIFFS = [
    ("herb", 360, 212, 0),
    ("kettle", 506, 270, 0),
    ("clock", 626, 70, 0),
    ("note", 742, 238, 0),
    ("jar", 846, 104, 0),
    ("fruit", 254, 406, 0),
    ("stool", 530, 482, 0),
]


# =================================================================== Level 138 modern bedroom (day / night)
DN138 = day_night(40.0, tint=(0.34, 0.36, 0.58))
WALL138 = (206, 214, 222)
WIN138 = (300, 40, 640, 290)


def l138_bg(c, d):
    c.rect(0, 0, W, 480, WALL138)
    flat(c, RRect(0, 0, W, 12, 0), (226, 232, 238))
    # window onto the city
    city_window(c, *WIN138, 1381)
    x0, y0, x1, y1 = WIN138
    piece(c, [RRect(x0 - 10, y0 - 10, x1 + 10, y0, 0), RRect(x0 - 10, y0 - 10, x0, y1 + 10, 0), RRect(x1, y0 - 10, x1 + 10, y1 + 10, 0),
              RRect(x0 - 10, y1, x1 + 10, y1 + 10, 0), RRect(468, y0, 474, y1, 0)], (244, 244, 242), shadow=SMALL)
    flat(c, Thick(270, 26, 670, 26, 3), (90, 90, 96))
    # wardrobe (left)
    piece(c, RRect(-10, 40, 120, 480, 2), (236, 232, 224), border=1.5, shadow=PROP)
    door = (176, 196, 210) if "wardrobe" not in d else (190, 150, 110)
    flat(c, RRect(10, 70, 46, 200, 2), door)
    flat(c, RRect(10, 320, 46, 450, 2), (176, 196, 210))
    flat(c, Thick(56, 50, 56, 470, 1.4), (210, 206, 198))
    flat(c, [RRect(44, 230, 48, 290, 1), RRect(64, 230, 68, 290, 1)], (120, 120, 126))
    # framed print (right) + wall shelf (left of window)
    def art(c, r):
        flat(c, RRect(*r, 0), (240, 214, 190))
        flat(c, Poly([(r[0], r[3]), ((r[0] + r[2]) / 2, r[1] + 20), (r[2], r[3])]), (90, 120, 150) if "print" not in d else (200, 110, 90))
        flat(c, Circ(r[2] - 18, r[1] + 18, 10), (250, 250, 240))
    framed(c, 700, 80, 820, 230, (60, 60, 66), art)
    piece(c, RRect(150, 170, 270, 178, 1), (176, 136, 100), shadow=SMALL)
    piece(c, [RRect(160, 140, 172, 170, 1), RRect(174, 146, 184, 170, 1), RRect(186, 136, 198, 170, 1)], (110, 150, 180), shadow=SMALL)
    piece(c, [Ell(236, 156, 14, 14), RRect(228, 156, 244, 170, 2)], (240, 240, 234), shadow=SMALL)
    flat(c, [Ell(232, 136, 5, 12), Ell(242, 138, 5, 10)], (90, 150, 100))
    # floor + rug
    planks(c, 480, (196, 170, 136), (178, 152, 120), seed=138)
    piece(c, RRect(170, 530, 780, 594, 4), (226, 220, 210), shadow=SMALL)
    for x in range(184, 770, 16):
        flat(c, Thick(x, 594, x, 600, 1.2), (226, 220, 210))
    # bed
    piece(c, RRect(250, 300, 700, 420, 14), (120, 130, 150), border=2, shadow=PROP)
    for x in range(290, 700, 50):
        flat(c, Thick(x, 314, x, 410, 1.4), (108, 118, 138))
    piece(c, RRect(230, 400, 720, 470, 6), (250, 250, 248), border=1.5, shadow=PROP)
    for k, x in enumerate((340, 470, 600)):
        col = (240, 236, 228) if k != 1 else ((230, 200, 140) if "pillow" not in d else (150, 200, 170))
        piece(c, RRect(x - 56, 360, x + 56, 410, 16), col, border=1.2, shadow=SMALL)
    piece(c, RRect(230, 420, 720, 520, 8), (200, 214, 230), border=1.5, shadow=PROP)
    flat(c, RRect(230, 420, 720, 440, 6), (240, 240, 236))
    throw = (200, 110, 80) if "blanket" not in d else (90, 110, 170)
    piece(c, RRect(560, 432, 716, 520, 4), throw, shadow=SMALL)
    flat(c, [Thick(570, 510, 706, 510, 2)], lit(throw, 0.85))
    flat(c, [RRect(240, 520, 252, 536, 1), RRect(698, 520, 710, 536, 1)], (90, 70, 56))
    # nightstands + lamps
    for x in (150, 790):
        piece(c, RRect(x - 50, 410, x + 50, 500, 3), (176, 136, 100), border=1.5, shadow=PROP)
        flat(c, Thick(x - 46, 452, x + 46, 452, 1.4), (150, 112, 80))
        flat(c, RRect(x - 10, 430, x + 10, 434, 1), (80, 70, 60))
        tabletop_lamp(c, x - 18, 410, (240, 232, 214))
    alarm = (240, 240, 236) if "clock" not in d else (240, 120, 90)
    piece(c, [RRect(812, 384, 846, 410, 6)], alarm, border=1, shadow=SMALL)
    flat(c, RRect(818, 390, 840, 402, 2), (40, 44, 52))
    flat(c, [Thick(822, 396, 828, 396, 1.4), Thick(832, 396, 836, 396, 1.4)], (120, 220, 160))
    piece(c, [RRect(126, 396, 176, 410, 1)], (90, 120, 170), shadow=SMALL)
    sl = (240, 170, 180) if "slippers" not in d else (120, 170, 220)
    piece(c, [Ell(300, 566, 22, 9), Ell(340, 572, 22, 9)], sl, border=1, shadow=SMALL)
    # plant (right corner)
    monstera(c, 866, 590, 1.0, pot=(60, 64, 72), leaf=(70, 140, 96))


def l138_night(c, m):
    x0, y0, x1, y1 = WIN138
    flat(c, RRect(x0, y0, x1, y1, 0), (24, 30, 64))
    rnd = random.Random(1381)
    x = x0
    while x < x1:
        w, h = rnd.randint(24, 50), rnd.randint(int((y1 - y0) * 0.25), int((y1 - y0) * 0.55))
        flat(c, RRect(x, y1 - h, min(x1, x + w), y1, 0), (40, 46, 82))
        x += w + rnd.randint(2, 8)
    rnd = random.Random(1382)
    for _ in range(26):
        sx, sy = rnd.uniform(x0 + 6, x1 - 6), rnd.uniform(y0 + 6, y0 + 90)
        flat(c, Poly(star_pts(sx, sy, 3, 1, points=4, rot=0)), (255, 248, 210))
    piece(c, Circ(590, 82, 18), (252, 246, 220), shadow=None)
    for xx in range(x0 + 6, x1 - 6, 12):
        for yy in range(int(y1 - 70), int(y1) - 6, 14):
            if rnd.random() < 0.35:
                flat(c, RRect(xx, yy, xx + 6, yy + 7, 0), (255, 214, 120))
    flat(c, RRect(468, y0, 474, y1, 0), (60, 62, 76))


def l138_glow(x):
    return lambda c, m: soft_union(c, [Ell(x, 360, 34, 30)], (255, 220, 140), 0.55, spread=30)


L138_ELEMENTS = [
    E("night", l138_night, daynight="night"),
    E("glowL", l138_glow(132), daynight="night", anim=dict(twinkle=0.08, twinkleSpeed=0.5)),
    E("glowR", l138_glow(772), daynight="night", anim=dict(twinkle=0.08, twinkleSpeed=0.5, phase=0.5)),
    E("curtainL", lambda c, m: piece(c, [Poly([(276, 26), (318, 26), (324, 300), (270, 306)])], (246, 244, 236, 0.85), shadow=SMALL),
      pivot=(296, 26), anim=dict(swingAngle=1.5, swingSpeed=0.2)),
    E("curtainR", lambda c, m: piece(c, [Poly([(622, 26), (664, 26), (670, 306), (616, 300)])], (246, 244, 236, 0.85), shadow=SMALL),
      pivot=(644, 26), anim=dict(swingAngle=1.5, swingSpeed=0.2, phase=0.5)),
    E("plane", lambda c, m: flat(c, [Ell(0, 80, 10, 2.4), Thick(-2, 80, -6, 74, 2), Thick(-6, 80, -2, 86, 2)], (250, 250, 252)),
      daynight="day", anim=dict(driftVelocity=(16, 0), driftLength=380, driftStart=290, phase=0.3)),
]

L138_DIFFS = [
    ("pillow", 470, 385, 0),
    ("print", 760, 160, 0),
    ("slippers", 320, 568, 0),
    ("clock", 829, 397, 0),
    ("wardrobe", 28, 135, 0),
    ("blanket", 638, 476, 0),
]


# =================================================================== Level 139 old American apartment: living room
PAPER139 = ((196, 200, 160), (212, 214, 178))
WOOD139 = (120, 78, 54)


def brick_facade(c, x0, y0, x1, y1, col=(170, 96, 76), mortar=(150, 82, 66), seed=0):
    flat(c, RRect(x0, y0, x1, y1, 0), col)
    for y in range(int(y0), int(y1), 10):
        flat(c, Thick(x0, y, x1, y, 1), mortar)
        off = 0 if (y // 10) % 2 else 11
        for x in range(int(x0) + off, int(x1), 22):
            flat(c, Thick(x, y, x, y + 10, 1), mortar)


def l139_bg(c, d):
    wallpaper_stripes(c, (0, 0, W, 380), *PAPER139, w=30)
    soft_union(c, [Ell(820, 20, 90, 40)], (170, 150, 110), 0.35, spread=20)       # old water stain
    soft_union(c, [Ell(40, 300, 40, 70)], (180, 170, 130), 0.25, spread=20)
    flat(c, RRect(0, 0, W, 12, 0), (232, 226, 206))
    flat(c, Thick(0, 46, W, 46, 4), WOOD139)                                          # picture rail
    # window: brick building opposite + fire escape
    wx0, wy0, wx1, wy1 = 230, 70, 420, 350
    flat(c, RRect(wx0, wy0, wx1, wy0 + 40, 0), (180, 206, 226))
    brick_facade(c, wx0, wy0 + 30, wx1, wy1)
    for x in (250, 340):
        for y in (130, 230):
            flat(c, RRect(x, y, x + 50, y + 60, 1), (240, 232, 214))
            flat(c, RRect(x + 4, y + 4, x + 46, y + 56, 0), (70, 80, 96))
            flat(c, Thick(x + 4, y + 30, x + 46, y + 30, 2), (240, 232, 214))
    for y in (200, 300):
        flat(c, Thick(wx0, y, wx1, y, 3), (40, 40, 46))
        for x in range(wx0, wx1, 10):
            flat(c, Thick(x, y - 22, x, y, 1.4), (40, 40, 46))
        flat(c, Thick(wx0, y - 22, wx1, y - 22, 2), (40, 40, 46))
    flat(c, [Thick(392, 200, 360, 300, 3)] + [Thick(392 - k * 6.4, 200 + k * 20, 402 - k * 6.4, 200 + k * 20, 2) for k in range(5)], (40, 40, 46))
    piece(c, [RRect(wx0 - 12, wy0 - 12, wx1 + 12, wy0, 0), RRect(wx0 - 12, wy0 - 12, wx0, wy1 + 8, 0), RRect(wx1, wy0 - 12, wx1 + 12, wy1 + 8, 0),
              RRect(wx0, 206, wx1, 216, 0), RRect(wx0 - 20, wy1, wx1 + 20, wy1 + 12, 1)], (236, 230, 214), shadow=SMALL)
    for k, (x0, x1) in enumerate(((wx0 - 26, wx0 + 30), (wx1 - 30, wx1 + 26))):
        lace = (250, 248, 240) if not (k == 1 and "curtain" in d) else (240, 190, 200)
        piece(c, Poly([(x0, 58), (x1, 58), (x1 - 6, 300), (x0 + 6, 300)]), lace, shadow=SMALL)
        for y in range(78, 300, 22):
            flat(c, Thick(x0 + 8, y, x1 - 8, y, 1.2), lit(lace, 0.9))
    flat(c, Thick(wx0 - 34, 58, wx1 + 34, 58, 4), (150, 120, 70))
    # wainscot + radiator
    piece(c, RRect(-10, 380, 910, 470, 0), WOOD139, shadow=SMALL)
    flat(c, Thick(0, 384, W, 384, 3), lit(WOOD139, 1.2))
    for x in range(0, W, 90):
        flat(c, RRect(x + 10, 396, x + 80, 460, 2), lit(WOOD139, 0.9))
    piece(c, [RRect(236, 370, 414, 452, 4)], (198, 200, 204), border=1.5, shadow=PROP)
    for x in range(246, 410, 14):
        flat(c, RRect(x, 374, x + 8, 448, 4), (176, 178, 184))
    flat(c, [RRect(250, 452, 258, 470, 1), RRect(392, 452, 400, 470, 1)], (150, 152, 160))
    # family photos (right)
    for k, (x, y, w, h) in enumerate(((600, 90, 70, 90), (690, 76, 60, 76), (770, 100, 80, 64))):
        if k == 1 and "photo" in d:
            flat(c, RRect(x + 4, y + 4, x + w - 4, y + h - 4, 1), lit(PAPER139[1], 1.04))
            continue
        piece(c, RRect(x, y, x + w, y + h, 2), (90, 60, 40), border=1.2, shadow=PROP)
        flat(c, RRect(x + 6, y + 6, x + w - 6, y + h - 6, 1), (220, 206, 176))
        flat(c, [Circ(x + w / 2, y + h * 0.42, w * 0.16), Ell(x + w / 2, y + h - 10, w * 0.28, h * 0.18)], (130, 100, 80))
    # wall clock (left)
    clock = (240, 232, 210) if "clock" not in d else (120, 170, 210)
    piece(c, [RRect(100, 90, 150, 220, 6)], (110, 70, 46), border=1.5, shadow=PROP)
    piece(c, Circ(125, 124, 20), clock, shadow=SMALL)
    flat(c, [Thick(125, 124, 125, 110, 2), Thick(125, 124, 134, 130, 2)], INK)
    # floor + braided rug
    planks(c, 470, (150, 104, 70), (128, 88, 60), seed=139)
    for k, col in enumerate(((150, 70, 60), (200, 170, 120), (90, 110, 130), (180, 110, 80))):
        piece(c, Ell(460, 556, 300 - k * 50, 40 - k * 7), col, shadow=SMALL if k == 0 else None)
    # floor lamp with fringe
    piece(c, [Ell(540, 470, 24, 6), Thick(540, 466, 540, 210, 3)], (170, 140, 80), shadow=PROP)
    shade = (236, 206, 150) if "shade" not in d else (170, 80, 90)
    piece(c, Poly([(506, 220), (574, 220), (560, 168), (520, 168)]), shade, border=1.2, shadow=SMALL)
    flat(c, [Thick(x, 220, x, 230, 1.4) for x in range(508, 574, 5)], lit(shade, 0.85))
    # old TV set on legs
    piece(c, [RRect(612, 290, 812, 446, 8)], (126, 86, 56), border=1.5, shadow=PROP)
    flat(c, [Thick(636, 446, 628, 476, 4), Thick(788, 446, 796, 476, 4)], (90, 60, 40))
    flat(c, RRect(628, 306, 752, 430, 18), (40, 40, 44))
    bars = [(230, 230, 220), (230, 220, 90), (90, 200, 210), (90, 190, 90), (200, 80, 200), (210, 70, 70), (60, 70, 190)]
    if "tv" in d:
        bars[2], bars[5] = (250, 150, 60), (90, 200, 210)
    for k, col in enumerate(bars):
        flat(c, RRect(642 + k * 14, 320, 656 + k * 14, 400, 0), col)
    flat(c, RRect(642, 400, 740, 416, 0), (30, 30, 34))
    for y in (330, 372):
        piece(c, Circ(782, y, 11), (200, 196, 186), shadow=SMALL)
    flat(c, [Thick(770 + k * 6, 404, 770 + k * 6, 428, 1.4) for k in range(5)], (90, 60, 40))
    piece(c, [Ell(712, 290, 22, 7)], (60, 58, 62), shadow=SMALL)
    flat(c, [Thick(706, 286, 670, 216, 2.4), Thick(718, 286, 760, 220, 2.4)], (200, 200, 206))
    # armchair (left front)
    chair = (176, 90, 80)
    piece(c, [RRect(40, 380, 200, 500, 30), RRect(20, 440, 70, 560, 18), RRect(170, 440, 220, 560, 18), RRect(54, 470, 186, 556, 8)],
          chair, border=1.5, shadow=PROP)
    rnd = random.Random(1391)
    for _ in range(22):
        flat(c, Circ(rnd.uniform(56, 184), rnd.uniform(396, 548), 4), lit(chair, 1.25))
    flat(c, [Thick(34, 560, 34, 580, 4), Thick(206, 560, 206, 580, 4)], (90, 60, 40))
    piece(c, RRect(30, 426, 90, 446, 4), (240, 232, 214), shadow=SMALL)                # doily
    pillow = (230, 200, 120) if "pillow" not in d else (110, 160, 120)
    piece(c, Poly([(96, 478), (164, 478), (170, 432), (90, 432)]), pillow, border=1.2, shadow=SMALL)
    flat(c, Circ(130, 455, 5), lit(pillow, 0.8))
    # side table + rotary phone
    piece(c, [Ell(274, 482, 40, 9), Thick(274, 482, 274, 570, 5), Ell(274, 572, 24, 6)], (110, 70, 46), border=1.2, shadow=PROP)
    phone = (40, 40, 44) if "phone" not in d else (200, 60, 60)
    piece(c, [Poly([(252, 478), (296, 478), (288, 456), (260, 456)]), RRect(248, 446, 300, 456, 5)], phone, border=1, shadow=SMALL)
    flat(c, Circ(274, 468, 8), (230, 230, 226))


L139_ELEMENTS = [
    E("bulb", lambda c, m: (flat(c, Thick(450, 0, 450, 70, 1.4), (60, 56, 50)), piece(c, Ell(450, 80, 14, 10), (255, 240, 190), shadow=SMALL),
                            soft_union(c, [Circ(450, 80, 12)], (255, 236, 160), 0.5, spread=16)),
      pivot=(450, 0), anim=dict(swingAngle=3, swingSpeed=0.25)),
    E("pendulum", lambda c, m: piece(c, [Thick(125, 150, 125, 196, 2), Circ(125, 200, 8)], (210, 170, 80), shadow=SMALL), pivot=(125, 150),
      anim=dict(swingAngle=14, swingSpeed=0.5)),
    E("cat", lambda c, m: (piece(c, [Ell(470, 540, 34, 13), Circ(500, 530, 12), Poly([(492, 523), (494, 508), (500, 520)]),
                                     Poly([(504, 520), (510, 508), (511, 525)])], (230, 150, 70), border=1.2, shadow=SMALL),
                           flat(c, [Thick(494, 530, 499, 532, 1.4), Thick(503, 532, 508, 530, 1.4)], INK)),
      pivot=(470, 550), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.4)),
    E("tail", lambda c, m: flat(c, Thick(438, 546, 418, 536, 4), (230, 150, 70)), pivot=(438, 546), anim=dict(swingAngle=14, swingSpeed=0.6)),
    E("pigeon", lambda c, m: (piece(c, [Ell(300, 290, 12, 8), Circ(290, 284, 6)], (150, 150, 166), shadow=SMALL),
                              flat(c, Poly([(284, 284), (278, 286), (284, 288)]), (220, 160, 60))),
      pivot=(300, 298), anim=dict(bobAmplitude=(0, 2), bobSpeed=1.0)),
]

L139_DIFFS = [
    ("curtain", 410, 180, 0),
    ("clock", 125, 124, 0),
    ("photo", 720, 114, 0),
    ("shade", 540, 196, 0),
    ("tv", 690, 360, 0),
    ("pillow", 130, 455, 0),
    ("phone", 274, 462, 0),
]


# =================================================================== Level 140 old American apartment: kitchen
YELLOW140 = (240, 226, 170)
GINGHAM = (200, 60, 60)


def gingham(c, x0, y0, x1, y1, col=GINGHAM, s=10):
    flat(c, RRect(x0, y0, x1, y1, 0), (250, 246, 240))
    for x in range(int(x0), int(x1), s * 2):
        flat(c, RRect(x, y0, min(x1, x + s), y1, 0), lit(col, 1.35) if col[0] > 100 else col)
    for y in range(int(y0), int(y1), s * 2):
        flat(c, RRect(x0, y, x1, min(y1, y + s), 0), lit(col, 1.35) if col[0] > 100 else col)
    for x in range(int(x0), int(x1), s * 2):
        for y in range(int(y0), int(y1), s * 2):
            flat(c, RRect(x, y, min(x1, x + s), min(y1, y + s), 0), col)


def l140_bg(c, d):
    c.rect(0, 0, W, 450, YELLOW140)
    flat(c, RRect(0, 0, W, 12, 0), (250, 244, 220))
    # mint tiles (wainscot)
    flat(c, RRect(0, 240, W, 450, 0), (190, 222, 204))
    for y in range(240, 450, 20):
        flat(c, Thick(0, y, W, y, 1.2), (170, 204, 186))
    for x in range(0, W, 20):
        flat(c, Thick(x, 240, x, 450, 1.2), (170, 204, 186))
    flat(c, Thick(0, 240, W, 240, 4), (60, 60, 66))
    # window + outside (brick wall, sky)
    flat(c, RRect(270, 60, 450, 230, 0), (176, 210, 236))
    brick_facade(c, 380, 60, 450, 230, seed=1401)
    brick_facade(c, 270, 150, 380, 230, col=(190, 140, 110), mortar=(170, 120, 96))
    piece(c, [RRect(262, 52, 458, 62, 0), RRect(262, 52, 272, 236, 0), RRect(448, 52, 458, 236, 0), RRect(272, 140, 448, 146, 0),
              RRect(254, 226, 466, 238, 1)], (250, 248, 240), shadow=SMALL)
    flat(c, Thick(270, 96, 450, 84, 1.2), (80, 80, 86))                                  # laundry line
    valance = GINGHAM if "curtain" not in d else (60, 120, 190)
    gingham(c, 250, 44, 470, 84, valance)
    piece(c, [Poly([(250, 84)] + [(250 + k * 22 + 11, 92 if k % 2 == 0 else 84) for k in range(10)] + [(470, 84)])], lit(valance, 1.35), shadow=SMALL)
    # wall phone + calendar
    piece(c, [RRect(214, 140, 246, 200, 6)], (240, 210, 80), border=1.2, shadow=PROP)
    flat(c, [RRect(220, 150, 240, 162, 3)], (210, 180, 60))
    piece(c, RRect(740, 70, 830, 210, 1), (250, 248, 240), border=1.2, shadow=PROP)
    flat(c, RRect(748, 78, 822, 132, 0), (110, 170, 210) if "calendar" not in d else (240, 150, 80))
    flat(c, Poly([(748, 132), (775, 100), (800, 120), (822, 96), (822, 132)]), (90, 140, 90))
    for r in range(4):
        for k in range(6):
            flat(c, RRect(750 + k * 12, 142 + r * 16, 758 + k * 12, 152 + r * 16, 0), (220, 214, 200))
    # rounded fridge
    piece(c, [RRect(36, 110, 200, 450, 30), RRect(36, 160, 200, 450, 6)], (246, 240, 222), border=1.5, shadow=PROP)
    flat(c, Thick(40, 230, 196, 230, 2), (210, 204, 186))
    flat(c, [RRect(178, 180, 188, 220, 3), RRect(178, 244, 188, 300, 3)], (200, 204, 212))
    flat(c, RRect(80, 140, 156, 156, 3), (200, 204, 212))
    mag = [(220, 70, 70), (70, 140, 210), (240, 190, 50)]
    if "magnet" in d:
        mag[1] = (120, 190, 90)
    for k, (x, y) in enumerate(((80, 270), (120, 296), (150, 268))):
        piece(c, Circ(x, y, 14), mag[k], shadow=SMALL)
    piece(c, RRect(66, 282, 110, 330, 1), (250, 250, 246), shadow=SMALL)
    flat(c, [Thick(72, 296, 104, 296, 1.2), Thick(72, 306, 100, 306, 1.2), Thick(72, 316, 96, 316, 1.2)], (120, 120, 140))
    # sink on legs with curtain skirt
    piece(c, [RRect(244, 248, 476, 300, 6)], (246, 246, 242), border=1.5, shadow=PROP)
    flat(c, RRect(300, 254, 420, 270, 4), (210, 214, 216))
    piece(c, [Thick(360, 252, 360, 232, 3), Thick(360, 232, 376, 232, 3)], (190, 196, 204), shadow=SMALL)
    gingham(c, 250, 300, 470, 450, GINGHAM)
    flat(c, Thick(360, 300, 360, 450, 2), (150, 40, 40))
    # stove with backguard + kettle + pans
    piece(c, [RRect(520, 216, 700, 270, 4), RRect(520, 270, 700, 450, 4)], (246, 244, 236), border=1.5, shadow=PROP)
    flat(c, RRect(530, 226, 690, 244, 3), (200, 200, 196))
    flat(c, Circ(610, 235, 7), (240, 240, 236))
    flat(c, [Circ(546 + k * 22, 286, 6) for k in range(4)] + [Circ(640 + k * 20, 286, 6) for k in range(3)], (60, 60, 66))
    flat(c, RRect(540, 306, 680, 430, 4), (226, 224, 216))
    flat(c, RRect(568, 330, 652, 390, 4), (60, 60, 66))
    flat(c, RRect(560, 312, 660, 320, 3), (190, 196, 204))
    kettle = (90, 170, 160) if "kettle" not in d else (230, 120, 60)
    piece(c, [Ell(580, 252, 26, 18), RRect(568, 228, 592, 236, 3), Thick(552, 248, 540, 236, 4)], kettle, border=1.2, shadow=SMALL)
    piece(c, [Thick(568, 232, 592, 232, 4)], (40, 40, 46), shadow=None)
    piece(c, [RRect(630, 246, 680, 268, 4), Thick(680, 254, 700, 254, 4)], (60, 60, 66), shadow=SMALL)
    flat(c, Thick(520, 120, 700, 120, 4), (150, 150, 158))
    for k, x in enumerate((548, 610, 670)):
        if k == 1 and "pan" in d:
            continue
        flat(c, Thick(x, 120, x, 140, 1.6), (90, 90, 96))
        piece(c, [Thick(x, 140, x, 160, 5), Circ(x, 180, 22 - k * 3)], (200, 120, 70), border=1, shadow=SMALL)
    # floor: black / white checks
    c.rect(0, 450, W, H, (246, 244, 236))
    for r, y in enumerate(range(450, H, 30)):
        for k, x in enumerate(range(0, W, 30)):
            if (r + k) % 2:
                flat(c, RRect(x, y, x + 30, y + 30, 0), (50, 50, 56))
    flat(c, Thick(0, 450, W, 450, 3), (60, 60, 66))
    # formica table + chrome chair
    piece(c, RRect(700, 420, 900, 436, 4), (230, 90, 90), border=1.5, shadow=PROP)
    flat(c, Thick(704, 432, 896, 432, 2), (200, 204, 212))
    flat(c, [Thick(722, 436, 722, 600, 4), Thick(880, 436, 880, 600, 4)], (200, 204, 212))
    toaster = (200, 204, 212) if "toaster" not in d else (240, 200, 80)
    piece(c, RRect(830, 380, 884, 420, 8), toaster, border=1.2, shadow=SMALL)
    flat(c, [RRect(842, 380, 852, 386, 1), RRect(862, 380, 872, 386, 1)], (60, 60, 66))
    loaf(c, 752, 410, "round")
    piece(c, [Ell(794, 414, 14, 5), RRect(784, 396, 804, 414, 3)], (250, 250, 246), shadow=SMALL)
    seat = (230, 90, 90) if "chair" not in d else (90, 170, 120)
    piece(c, [Thick(760, 600, 764, 500, 3), Thick(820, 600, 816, 500, 3), Thick(816, 500, 820, 430, 3)], (200, 204, 212), shadow=SMALL)
    piece(c, [RRect(746, 486, 834, 504, 6), RRect(800, 408, 840, 440, 8)], seat, border=1.2, shadow=PROP)
    # grandma at the sink
    modern(c, 360, 540, (130, 160, 200), bottom=(130, 160, 200), hair=(220, 220, 226), h=3.0, skirt=True, glasses=True)
    piece(c, RRect(336, 436, 384, 482, 3), (250, 250, 246), shadow=SMALL)


def l140_shirt(x, col, ph):
    def d(c, m):
        y = 96 - (x - 270) * 12 / 180
        piece(c, [Poly([(x - 14, y), (x + 14, y), (x + 18, y + 10), (x + 10, y + 12), (x + 10, y + 36), (x - 10, y + 36), (x - 10, y + 12),
                        (x - 18, y + 10)])], col, shadow=SMALL)
    return E("shirt%d" % x, d, pivot=(x, 96 - (x - 270) * 12 / 180), anim=dict(swingAngle=6, swingSpeed=0.4, phase=ph))


L140_ELEMENTS = [
    l140_shirt(300, (240, 240, 236), 0.0),
    l140_shirt(350, (120, 160, 220), 0.3),
    l140_shirt(404, (240, 190, 90), 0.6),
    E("cord", lambda c, m: flat(c, [Thick(230, 200, 226 + (k % 2) * 8, 210 + k * 8, 1.6) for k in range(10)], (220, 190, 70)), pivot=(230, 200),
      anim=dict(swingAngle=4, swingSpeed=0.3)),
    E("lamp", lambda c, m: (piece(c, Ell(450, 14, 50, 16), (250, 248, 236), shadow=SMALL),
                            soft_union(c, [Ell(450, 30, 50, 10)], (255, 240, 190), 0.4, spread=14)), anim=dict(twinkle=0.06, twinkleSpeed=0.4)),
] + steam("steam", 556, 230, n=3, r=5, rise=(-6, -16))

L140_DIFFS = [
    ("curtain", 360, 64, 0),
    ("magnet", 120, 296, 0),
    ("pan", 610, 168, 0),
    ("kettle", 580, 250, 0),
    ("calendar", 785, 105, 0),
    ("chair", 790, 470, 0),
    ("toaster", 857, 400, 0),
]


# =================================================================== Level 141 old American apartment: bathroom
PINK141 = (236, 200, 200)


def l141_bg(c, d):
    c.rect(0, 0, W, 470, PINK141)
    flat(c, RRect(0, 0, W, 12, 0), (246, 220, 220))
    # subway tiles + black trim
    flat(c, RRect(0, 250, W, 470, 0), (246, 246, 242))
    for y in range(250, 470, 16):
        off = 0 if (y // 16) % 2 else 16
        flat(c, Thick(0, y, W, y, 1), (214, 214, 210))
        for x in range(off, W, 32):
            flat(c, Thick(x, y, x, y + 16, 1), (214, 214, 210))
    flat(c, RRect(0, 244, W, 254, 0), (40, 40, 46))
    flat(c, RRect(0, 458, W, 470, 0), (40, 40, 46))
    # frosted window (right)
    piece(c, RRect(770, 70, 880, 220, 2), (250, 248, 240), border=1.5, shadow=PROP)
    flat(c, RRect(780, 80, 870, 210, 0), (210, 228, 236))
    flat(c, Thick(825, 80, 825, 210, 4), (250, 248, 240))
    flat(c, [Thick(784, 90 + k * 14, 866, 84 + k * 14, 1.2) for k in range(9)], (226, 238, 244))
    # medicine cabinet mirror + sconces + pedestal sink
    piece(c, RRect(116, 90, 244, 236, 4), (240, 236, 226), border=1.5, shadow=PROP)
    flat(c, RRect(126, 100, 234, 226, 2), (196, 214, 222))
    flat(c, [Thick(140, 200, 176, 120, 6), Thick(170, 212, 210, 126, 3)], (224, 236, 240))
    for x in (96, 264):
        piece(c, [RRect(x - 4, 130, x + 4, 160, 1), Ell(x, 122, 10, 14)], (200, 170, 90), border=1, shadow=SMALL)
        flat(c, Ell(x, 120, 7, 10), (255, 246, 210))
    piece(c, [RRect(110, 280, 250, 318, 12), Poly([(160, 316), (200, 316), (192, 450), (168, 450)]), Ell(180, 452, 30, 8)], (250, 250, 248),
          border=1.5, shadow=PROP)
    flat(c, RRect(140, 284, 220, 296, 5), (220, 226, 230))
    piece(c, [Thick(180, 284, 180, 266, 3), Thick(180, 266, 196, 266, 3)], (200, 200, 206), shadow=SMALL)
    cup = (120, 170, 220) if "cup" not in d else (240, 180, 60)
    piece(c, Poly([(222, 280), (244, 280), (241, 254), (225, 254)]), cup, border=1, shadow=SMALL)
    flat(c, [Thick(230, 254, 228, 236, 2.4), Thick(236, 254, 240, 238, 2.4)], (230, 80, 80))
    piece(c, Ell(130, 276, 12, 5), (250, 240, 200), shadow=SMALL)
    # high-tank toilet with pull chain
    piece(c, RRect(292, 100, 368, 150, 4), (250, 250, 248), border=1.5, shadow=PROP)
    flat(c, Thick(330, 150, 330, 380, 5), (200, 200, 206))
    piece(c, [Ell(330, 392, 46, 14), Poly([(296, 392), (364, 392), (352, 450), (308, 450)]), RRect(304, 450, 356, 470, 3)], (250, 250, 248),
          border=1.5, shadow=PROP)
    piece(c, RRect(286, 372, 374, 384, 5), (130, 90, 60), shadow=SMALL)
    # shower curtain (pulled aside) + rod
    c.ellipse_ring(600, 70, 190, 16, 3, (200, 200, 206), ymin=70)
    flat(c, Thick(600, 12, 600, 58, 2), (200, 200, 206))
    stripe = (90, 160, 200) if "curtain" not in d else (230, 140, 170)
    piece(c, Poly([(410, 72), (470, 76), (466, 400), (420, 420)]), (250, 250, 248), shadow=PROP)
    for k in range(4):
        x = 418 + k * 14
        flat(c, Poly([(x, 74), (x + 7, 74), (x + 6.6, 250), (x + 0.4, 250)]), (90, 160, 200))
        flat(c, Poly([(x + 0.4, 250), (x + 6.6, 250), (x + 6, 410), (x - 1, 412)]), stripe)
    # clawfoot tub
    piece(c, [Poly([(470, 370), (780, 370), (770, 470), (750, 500), (500, 500), (480, 470)]), Ell(625, 372, 160, 12)], (80, 140, 132),
          border=1.5, shadow=PROP)
    flat(c, [Ell(625, 372, 160, 12), RRect(468, 370, 782, 382, 4)], (250, 250, 248))
    flat(c, Ell(625, 372, 150, 8), (220, 228, 232))
    soft_union(c, [Ell(560, 368, 50, 10), Ell(640, 366, 60, 12), Ell(700, 368, 40, 9)], (255, 255, 255), 0.9, spread=4)
    for x in (500, 750):
        piece(c, [Poly([(x - 14, 496), (x + 14, 496), (x + 10, 516), (x + 18, 524), (x - 18, 524), (x - 10, 516)])], (210, 170, 80), shadow=SMALL)
    piece(c, [Thick(770, 372, 770, 330, 4), Thick(770, 330, 744, 330, 4)], (210, 170, 80), shadow=SMALL)
    if "duck" not in d:
        piece(c, [Ell(700, 360, 14, 9), Circ(712, 348, 7)], (250, 210, 50), border=1, shadow=SMALL)
        flat(c, Poly([(718, 348), (726, 350), (718, 352)]), (240, 130, 40))
    # towel rack + towel (right wall)
    flat(c, Thick(790, 270, 880, 270, 4), (210, 170, 80))
    towel = (120, 190, 170) if "towel" not in d else (240, 160, 120)
    piece(c, RRect(800, 266, 870, 380, 4), towel, border=1, shadow=PROP)
    flat(c, [Thick(800, 350, 870, 350, 3), Thick(800, 358, 870, 358, 3)], lit(towel, 1.2))
    # floor: tiny hex tiles
    c.rect(0, 470, W, H, (246, 246, 242))
    for r, y in enumerate(range(474, H, 12)):
        for x in range((r % 2) * 7, W, 14):
            flat(c, Circ(x, y, 1.6), (210, 210, 206))
    for y in (490, 498):
        flat(c, Thick(0, y, W, y, 4), (50, 50, 56))
    for x in range(14, W, 56):
        flat(c, Poly([(x, 520), (x + 8, 528), (x, 536), (x - 8, 528)]), (50, 50, 56))
    mat = (110, 150, 200) if "mat" not in d else (230, 190, 90)
    piece(c, RRect(530, 540, 720, 586, 10), mat, shadow=SMALL)
    flat(c, [Thick(x, 586, x, 594, 1.6) for x in range(540, 716, 8)], mat)
    flat(c, [Thick(x, 532, x, 540, 1.6) for x in range(540, 716, 8)], mat)
    # slippers + scale
    piece(c, [RRect(70, 530, 160, 556, 6)], (220, 220, 226), border=1, shadow=SMALL)
    flat(c, Circ(115, 543, 8), (250, 250, 248))


def l141_drop(c, m):
    piece(c, Ell(746, 340, 3, 4.5), (170, 210, 240), shadow=None)


L141_ELEMENTS = [
    E("chain", lambda c, m: (flat(c, Thick(362, 150, 362, 230, 1.4), (190, 196, 204)), piece(c, RRect(356, 230, 368, 246, 3), (250, 250, 248),
                                                                                             shadow=SMALL)),
      pivot=(362, 150), anim=dict(swingAngle=5, swingSpeed=0.3)),
    E("drop", l141_drop, anim=dict(driftVelocity=(0, 30), driftLength=28, driftFade=True)),
    E("bulb", lambda c, m: (flat(c, Thick(500, 0, 500, 40, 1.4), (60, 56, 50)), piece(c, Ell(500, 50, 22, 12), (250, 240, 230), shadow=SMALL)),
      pivot=(500, 0), anim=dict(swingAngle=2, swingSpeed=0.2)),
] + [E("bubble%d" % i, (lambda i=i: lambda c, m: piece(c, Circ(540 + i * 50, 360, 5), (236, 246, 252), border=1, shadow=None))(),
       anim=dict(driftVelocity=(2, -14), driftLength=60, driftFade=True, phase=i / 4)) for i in range(4)] \
  + steam("steam", 620, 344, n=4, r=10, rise=(2, -18), length=90)

L141_DIFFS = [
    ("cup", 233, 262, 0),
    ("curtain", 440, 330, 0),
    ("duck", 710, 354, 0),
    ("towel", 835, 320, 0),
    ("mat", 625, 563, 0),
]


# =================================================================== Level 142 European manor: entrance hall
STONE142 = (232, 220, 196)
CARPET = (170, 40, 50)


def baluster_row(c, x0, x1, y0, y1, col, step=12):
    flat(c, [RRect(x - 2.5, y0, x + 2.5, y1, 2) for x in range(int(x0), int(x1), step)], col)


def l142_bg(c, d):
    c.rect(0, 0, W, 470, STONE142)
    for x in (40, 860):
        flat(c, RRect(x - 18, 0, x + 18, 470, 0), lit(STONE142, 1.04))
    flat(c, RRect(0, 0, W, 20, 0), (240, 230, 210))
    flat(c, Thick(0, 22, W, 22, 4), (210, 186, 130))
    # tall arched window on the landing
    pts = [(360, 270)] + [(450 + 90 * math.cos(math.radians(a)), 120 - 80 * math.sin(math.radians(a))) for a in range(180, -1, -10)] + [(540, 270)]
    piece(c, Poly(pts), (240, 230, 210), border=1.5, shadow=PROP)
    inner = [(372, 266)] + [(450 + 78 * math.cos(math.radians(a)), 120 - 68 * math.sin(math.radians(a))) for a in range(180, -1, -10)] + [(528, 266)]
    flat(c, Poly(inner), (180, 210, 236))
    far_round_trees(c, 266, 24, (120, 170, 110), 1421, spacing=26, x0=372, x1=528)
    flat(c, [Thick(450, 52, 450, 266, 3), Thick(372, 150, 528, 150, 3), Thick(372, 210, 528, 210, 3)], (240, 230, 210))
    for side in (-1, 1):
        drape = (150, 40, 60) if not (side == 1 and "drape" in d) else (60, 110, 80)
        x = 450 + side * 96
        piece(c, Poly([(x - 22, 30), (x + 22, 30), (x + 18 - side * 8, 270), (x - 18 - side * 8, 276)]), drape, border=1.5, shadow=PROP)
        piece(c, Ell(x - side * 4, 190, 10, 6), (220, 180, 80), shadow=SMALL)
    flat(c, Thick(340, 30, 560, 30, 5), (210, 176, 92))
    # upper galleries left / right
    for x0, x1 in ((-10, 230), (670, 910)):
        piece(c, RRect(x0, 130, x1, 146, 0), (240, 230, 210), shadow=PROP)
        baluster_row(c, x0 + 8, x1, 92, 130, (240, 230, 210))
        piece(c, RRect(x0, 86, x1, 94, 1), (150, 100, 60), shadow=SMALL)
    # side flights up to the galleries
    for side in (-1, 1):
        a, b = (340, 230) if side < 0 else (560, 670)
        piece(c, Poly([(a, 286), (b, 146), (b, 170), (a, 310)]), (240, 230, 210), shadow=PROP)
        flat(c, Poly([(a, 290), (b, 150), (b, 160), (a, 300)]), CARPET)
        flat(c, [Thick(a + (b - a) * t, 248 - 140 * t + 38, a + (b - a) * t, 248 - 140 * t, 2.4) for t in [k / 10 for k in range(11)]],
             (240, 230, 210))
        piece(c, Thick(a, 248, b, 108, 5), (150, 100, 60), shadow=SMALL)
    # landing + central flight
    piece(c, RRect(320, 270, 580, 290, 0), (240, 230, 210), shadow=PROP)
    for k in range(10):
        y = 290 + k * 18
        x0, x1 = 330 - k * 6, 570 + k * 6
        flat(c, RRect(x0, y, x1, y + 18, 0), (226, 214, 190))
        flat(c, RRect(x0, y, x1, y + 5, 0), (246, 238, 222))
    flat(c, Poly([(400, 290), (500, 290), (520, 470), (380, 470)]), CARPET)
    for k in range(10):
        flat(c, Thick(400 - k * 2.2, 292 + k * 18, 500 + k * 2.2, 292 + k * 18, 2), (210, 176, 92))
    for side in (-1, 1):
        xa, xb = (320, 266) if side < 0 else (580, 634)
        flat(c, [Thick(xa + (xb - xa) * t, 270 + 200 * t, xa + (xb - xa) * t, 230 + 200 * t, 2.4) for t in [k / 12 for k in range(13)]],
             (240, 230, 210))
        piece(c, Thick(xa, 230, xb, 430, 6), (150, 100, 60), shadow=SMALL)
        piece(c, [RRect(xb - 10, 420, xb + 10, 474, 2), Circ(xb, 414, 9)], (150, 100, 60), border=1.2, shadow=PROP)
    # portraits under the galleries
    for k, (x0, dress) in enumerate(((70, (60, 80, 130)), (720, (130, 60, 70)))):
        if k == 1 and "portrait" in d:
            dress = (70, 120, 80)
        r = frame(c, x0, 180, x0 + 110, 330, (70, 64, 60), k=10)
        bust(c, (r[0] + r[2]) / 2, r[3], 0.62, dress, hair=(90, 60, 40) if k == 0 else (60, 44, 36), hair_style="long" if k else "short",
             collar="ruff" if k == 0 else "pearls")
    # long-case clock (right)
    piece(c, [RRect(632, 300, 680, 470, 3), RRect(626, 230, 686, 306, 6), Poly([(626, 232), (656, 210), (686, 232)])], (110, 66, 40), border=1.5,
          shadow=PROP)
    face = (246, 240, 220) if "clock" not in d else (90, 130, 190)
    flat(c, Circ(656, 266, 22), face)
    flat(c, [Thick(656, 266, 656, 250, 2), Thick(656, 266, 668, 272, 2)], INK)
    flat(c, RRect(642, 320, 670, 440, 4), (70, 40, 26))
    # suit of armour (left)
    m = (176, 182, 196)
    piece(c, [RRect(222, 460, 260, 470, 2), Thick(234, 460, 234, 420, 7), Thick(248, 460, 248, 420, 7), RRect(226, 360, 256, 424, 8),
              Thick(226, 366, 216, 416, 6), Thick(256, 366, 266, 416, 6), RRect(230, 330, 252, 360, 6)], m, border=1.5, shadow=PROP)
    flat(c, [Thick(234, 344, 248, 344, 2), Thick(241, 360, 241, 410, 1.6)], lit(m, 0.7))
    plume = (190, 40, 50) if "plume" not in d else (60, 90, 190)
    piece(c, Poly([(236, 332), (240, 296), (274, 300), (284, 322), (252, 334)]), plume, shadow=SMALL)
    flat(c, Thick(276, 470, 276, 310, 2.4), (110, 90, 70))
    flat(c, Poly([(272, 310), (280, 310), (276, 292)]), m)
    # marble floor
    c.rect(0, 470, W, H, (238, 234, 228))
    for r, y in enumerate(range(470, H, 32)):
        for k, x in enumerate(range(-32, W + 32, 64)):
            xx = x + (r % 2) * 32
            flat(c, Poly([(xx, y + 16), (xx + 32, y), (xx + 64, y + 16), (xx + 32, y + 32)]), (90, 86, 96) if (k + r) % 3 == 0 else (214, 210, 204))
    flat(c, Poly([(380, 470), (520, 470), (560, H), (340, H)]), CARPET)
    flat(c, [Thick(380, 470, 340, H, 3), Thick(520, 470, 560, H, 3)], (210, 176, 92))
    # urns with flowers on pedestals
    for k, x in enumerate((120, 790)):
        piece(c, [RRect(x - 24, 500, x + 24, 590, 2), RRect(x - 30, 496, x + 30, 506, 2), RRect(x - 30, 584, x + 30, 594, 2)], (226, 220, 210),
              border=1.5, shadow=PROP)
        piece(c, [Ell(x, 474, 24, 22), RRect(x - 10, 490, x + 10, 498, 2)], (60, 90, 140), border=1.2, shadow=SMALL)
        fl = [(240, 160, 180), (250, 250, 246), (240, 200, 90)]
        if k == 1 and "flowers" in d:
            fl = [(180, 120, 220), (120, 160, 230), (180, 120, 220)]
        flat(c, [Thick(x, 460, x - 30, 420, 2), Thick(x, 460, x, 410, 2), Thick(x, 460, x + 30, 420, 2)], (80, 130, 80))
        for j, (dx, dy) in enumerate(((-30, 418), (-14, 406), (0, 400), (14, 406), (30, 418), (-20, 430), (20, 430))):
            piece(c, Circ(x + dx, dy, 9), fl[j % 3], shadow=SMALL)
    # butler with a tray (right front) + lady on the stairs
    modern(c, 700, 580, (40, 40, 48), bottom=(40, 40, 48), hair=(150, 150, 156), h=2.0)
    flat(c, Poly([(694, 516), (706, 516), (700, 534)]), (250, 250, 248))
    piece(c, [Ell(730, 520, 26, 5), Thick(712, 528, 724, 520, 4)], (220, 220, 226), shadow=SMALL)
    piece(c, [RRect(722, 504, 728, 518, 1), RRect(736, 506, 742, 518, 1)], (240, 230, 200), shadow=SMALL)
    lady(c, 450, 362, (90, 130, 190), hair=(200, 150, 80), h=1.6, wide=1.3)


def l142_chandelier(c, m):
    flat(c, Thick(450, 0, 450, 40, 2), (180, 150, 80))
    c.ellipse_ring(450, 60, 70, 14, 4, GOLD)
    c.ellipse_ring(450, 40, 40, 8, 3, GOLD)
    for k in range(9):
        x = 386 + k * 16
        yy = 60 + 13 * math.sqrt(max(0, 1 - ((x - 450) / 70) ** 2))
        flat(c, Thick(x, yy, x, yy + 14, 1), (230, 240, 250))
        flat(c, Poly([(x - 3, yy + 14), (x + 3, yy + 14), (x, yy + 22)]), (220, 236, 250))
    for dx in (-56, -28, 0, 28, 56):
        yy = 60 + 13 * math.sqrt(max(0, 1 - (dx / 70) ** 2)) - 12
        flat(c, RRect(450 + dx - 2.4, yy - 12, 450 + dx + 2.4, yy, 1), (246, 240, 226))
        flat(c, Poly([(450 + dx - 3, yy - 12), (450 + dx + 3, yy - 12), (450 + dx, yy - 22)]), (255, 190, 80))


L142_ELEMENTS = [
    E("chandelier", l142_chandelier, pivot=(450, 0), daynight="untinted", anim=dict(swingAngle=1.5, swingSpeed=0.15)),
    E("glow", lambda c, m: soft_union(c, [Ell(450, 60, 80, 24)], (255, 236, 170), 0.35, spread=30), anim=dict(twinkle=0.15, twinkleSpeed=0.6)),
    E("pendulum", lambda c, m: piece(c, [Thick(656, 320, 656, 412, 2), Circ(656, 418, 11)], (210, 176, 92), shadow=SMALL), pivot=(656, 320),
      anim=dict(swingAngle=10, swingSpeed=0.5)),
    E("bird", lambda c, m: flat(c, [Thick(380, 110, 386, 106, 1.6), Thick(386, 106, 392, 110, 1.6)], (60, 60, 70)),
      anim=dict(driftVelocity=(16, -2), driftLength=120, driftFade=True)),
]

L142_DIFFS = [
    ("drape", 550, 150, 0),
    ("portrait", 775, 255, 0),
    ("clock", 656, 266, 0),
    ("plume", 252, 318, 0),
    ("flowers", 790, 414, 0),
]


# =================================================================== Level 143 European manor: study
PANEL = (120, 78, 52)
DAMASK = ((60, 90, 70), (70, 104, 80))


def l143_bg(c, d):
    wallpaper_diamonds(c, (0, 0, W, 300), *DAMASK, s=28)
    flat(c, RRect(0, 0, W, 18, 0), (150, 104, 70))
    flat(c, Thick(0, 20, W, 20, 3), (200, 160, 90))
    piece(c, RRect(-10, 300, 910, 470, 0), PANEL, shadow=SMALL)
    flat(c, Thick(0, 304, W, 304, 3), lit(PANEL, 1.2))
    for x in range(250, 660, 100):
        flat(c, RRect(x + 8, 320, x + 92, 456, 2), lit(PANEL, 0.88))
    # bookcases left / right
    bookcase(c, 0, 230, 30, 470, 1431, rows=6)
    bookcase(c, 670, 900, 30, 470, 1432, rows=6, swap=(1, 3, 8, (240, 230, 200)) if "books" in d else None)
    # over-mantel painting
    r = frame(c, 340, 50, 560, 210, (150, 190, 220), k=12)
    if "painting" in d:
        flat(c, RRect(r[0], r[1], r[2], (r[1] + r[3]) / 2, 0), (240, 170, 120))
    flat(c, Poly([(r[0], r[3]), (r[0], r[3] - 50), (r[0] + 60, r[3] - 80), (r[0] + 120, r[3] - 56), (r[2], r[3] - 90), (r[2], r[3])]), (100, 140, 100))
    flat(c, Poly([(r[0], r[3]), (r[0] + 90, r[3] - 30), (r[2], r[3] - 20), (r[2], r[3])]), (130, 160, 90))
    flat(c, Circ(r[2] - 40, r[1] + 30, 12), (250, 240, 200))
    # marble fireplace
    piece(c, [RRect(316, 240, 584, 256, 2), RRect(330, 256, 570, 470, 0)], (232, 226, 214), border=1.5, shadow=PROP)
    flat(c, [RRect(330, 256, 570, 270, 0)], (220, 212, 198))
    flat(c, RRect(370, 300, 530, 470, 0), (40, 30, 30))
    flat(c, Poly([(370, 300), (530, 300), (530, 330), (450, 314), (370, 330)]), (232, 226, 214))
    piece(c, [Thick(396, 456, 504, 446, 9), Thick(400, 446, 500, 458, 9)], (110, 70, 46), shadow=SMALL)
    flat(c, [RRect(380, 462, 396, 470, 1), RRect(504, 462, 520, 470, 1)], (60, 56, 60))
    # mantel ornaments: clock, candlesticks, vase
    piece(c, [RRect(426, 196, 474, 240, 10), RRect(420, 234, 480, 240, 2)], (210, 176, 92), border=1.2, shadow=SMALL)
    flat(c, Circ(450, 214, 12), (246, 240, 220))
    flat(c, [Thick(450, 214, 450, 206, 1.6), Thick(450, 214, 456, 218, 1.6)], INK)
    for x in (344, 556):
        piece(c, [Ell(x, 238, 8, 3), Thick(x, 238, x, 210, 3)], (210, 176, 92), shadow=SMALL)
        flat(c, RRect(x - 3, 192, x + 3, 210, 1), (246, 240, 226))
    vase = (60, 90, 160) if "vase" not in d else (200, 80, 60)
    piece(c, [Ell(520, 226, 12, 14), RRect(514, 206, 526, 214, 2)], vase, border=1, shadow=SMALL)
    piece(c, [Ell(384, 230, 16, 10)], (240, 236, 226), border=1, shadow=SMALL)
    # floor + rug
    planks(c, 470, (110, 70, 48), (92, 58, 40), seed=143, step=22)
    piece(c, RRect(90, 500, 810, 596, 4), (150, 50, 50), shadow=SMALL)
    flat(c, RRect(104, 510, 796, 586, 2), (60, 70, 110))
    flat(c, RRect(120, 522, 780, 574, 2), (170, 120, 70))
    for k in range(6):
        flat(c, Poly(star_pts(180 + k * 108, 548, 18, 8, points=8)), (150, 50, 50))
    # chesterfield sofa (left front)
    leather = (130, 60, 40)
    piece(c, [RRect(30, 400, 300, 470, 14), RRect(10, 430, 60, 560, 16), RRect(270, 430, 320, 560, 16), RRect(40, 470, 290, 556, 6)],
          leather, border=1.5, shadow=PROP)
    for x in range(50, 290, 22):
        for y in (416, 440):
            flat(c, Circ(x + (y % 3) * 4, y, 2), lit(leather, 0.75))
    cushion = (220, 190, 120) if "cushion" not in d else (90, 140, 170)
    piece(c, Poly([(70, 476), (130, 476), (136, 432), (64, 432)]), cushion, border=1.2, shadow=SMALL)
    flat(c, [Thick(20, 560, 20, 576, 5), Thick(300, 560, 300, 576, 5)], (60, 40, 30))
    # wing chair (right front) + chess table
    green = (60, 110, 80)
    piece(c, [RRect(680, 380, 800, 480, 24), RRect(664, 440, 700, 560, 14), RRect(780, 440, 816, 560, 14), RRect(690, 470, 790, 552, 6)],
          green, border=1.5, shadow=PROP)
    flat(c, [Thick(680, 560, 680, 576, 5), Thick(800, 560, 800, 576, 5)], (60, 40, 30))
    piece(c, [RRect(560, 486, 640, 496, 2), Thick(600, 496, 600, 570, 5), Ell(600, 572, 24, 6)], (110, 70, 46), border=1.2, shadow=PROP)
    for i in range(4):
        for j in range(2):
            flat(c, RRect(564 + i * 18, 482 + j * 2, 573 + i * 18, 484 + j * 2, 0), (240, 230, 210) if (i + j) % 2 else (40, 30, 30))
    piece(c, [RRect(570, 466, 578, 484, 2), Circ(574, 462, 5)], (250, 246, 236), border=1, shadow=SMALL)
    piece(c, [RRect(588, 470, 596, 484, 2), Circ(592, 466, 4)], (40, 30, 30), border=1, shadow=SMALL)
    dec = (200, 130, 50) if "decanter" not in d else (90, 150, 80)
    piece(c, [Ell(624, 466, 14, 16), RRect(619, 436, 629, 456, 2), Circ(624, 432, 6)], (230, 236, 240), border=1, shadow=SMALL)
    flat(c, Ell(624, 469, 13, 13), dec)
    # brass reading lamp on a side table (by the sofa)
    piece(c, [Ell(330, 404, 22, 5), Thick(330, 404, 330, 480, 4), Ell(330, 482, 16, 4)], (90, 60, 40), shadow=PROP)
    lampshade = (60, 120, 80) if "lamp" not in d else (200, 160, 60)
    flat(c, Thick(330, 400, 330, 370, 2.4), (210, 176, 92))
    piece(c, Poly([(306, 372), (354, 372), (344, 352), (316, 352)]), lampshade, border=1.2, shadow=SMALL)


def l143_dog(c, m):
    piece(c, [Ell(450, 520, 52, 18), Circ(498, 512, 16), Ell(512, 520, 10, 6), Ell(488, 500, 7, 14)], (170, 120, 70), border=1.2, shadow=SMALL)
    flat(c, [Thick(494, 512, 500, 514, 1.6)], INK)
    flat(c, Circ(520, 518, 3), INK)


L143_ELEMENTS = flame("fire", 450, 450, 2.6, glow_night=False) + flame("fire2", 420, 452, 1.8, glow_night=False) \
    + flame("fire3", 484, 452, 2.0, glow_night=False) + flame("candleL", 344, 192, 0.6, glow_night=False) \
    + flame("candleR", 556, 192, 0.6, glow_night=False) + [
    E("fireglow", lambda c, m: soft_union(c, [Ell(450, 430, 70, 40)], (255, 170, 80), 0.3, spread=40), daynight="untinted",
      anim=dict(twinkle=0.25, twinkleSpeed=2.0)),
    E("dog", l143_dog, pivot=(450, 538), anim=dict(stretch=(0.02, 0.05), scaleSpeed=0.35)),
    E("dogtail", lambda c, m: flat(c, Thick(400, 526, 380, 534, 5), (170, 120, 70)), pivot=(400, 526), anim=dict(swingAngle=10, swingSpeed=0.5)),
    E("lampglow", lambda c, m: soft_union(c, [Ell(330, 378, 24, 8)], (255, 230, 150), 0.5, spread=14), anim=dict(twinkle=0.1, twinkleSpeed=0.5)),
]

L143_DIFFS = [
    ("painting", 450, 100, 0),
    ("books", 760, 110, 0),
    ("vase", 520, 222, 0),
    ("cushion", 100, 454, 0),
    ("decanter", 624, 462, 0),
    ("lamp", 330, 362, 0),
]


# =================================================================== Level 144 European manor: dining hall
BLUE144 = (190, 206, 214)


def l144_bg(c, d):
    c.rect(0, 0, W, 470, BLUE144)
    flat(c, RRect(0, 0, W, 22, 0), (240, 236, 226))
    flat(c, Thick(0, 24, W, 24, 4), GOLD)
    # three tall windows with drapes onto the garden
    for k, x in enumerate((150, 450, 750)):
        x0, x1 = x - 66, x + 66
        top = [(x0, 120)] + [(x + 66 * math.cos(math.radians(a)), 120 - 56 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(x1, 120)]
        piece(c, Poly(top + [(x1, 360), (x0, 360)]), (246, 242, 232), border=1.2, shadow=PROP)
        inner = [(x0 + 10, 120)] + [(x + 56 * math.cos(math.radians(a)), 120 - 46 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [
            (x1 - 10, 120)]
        flat(c, Poly(inner + [(x1 - 10, 350), (x0 + 10, 350)]), (176, 210, 236))
        far_round_trees(c, 300, 22, (110, 160, 100), 1441 + k, spacing=22, x0=x0 + 10, x1=x1 - 10)
        flat(c, RRect(x0 + 10, 300, x1 - 10, 350, 0), (140, 190, 110))
        flat(c, [Thick(x, 70, x, 350, 3), Thick(x0 + 10, 180, x1 - 10, 180, 3), Thick(x0 + 10, 260, x1 - 10, 260, 3)], (246, 242, 232))
        for side in (-1, 1):
            drape = (180, 150, 60)
            xx = x + side * 74
            piece(c, Poly([(xx - 18, 40), (xx + 18, 40), (xx + 14 - side * 6, 380), (xx - 14 - side * 6, 384)]), drape, border=1.5, shadow=PROP)
            for j in range(3):
                flat(c, Thick(xx - 10 + j * 10, 50, xx - 10 + j * 10 - side * 4, 376, 1.4), lit(drape, 0.86))
        valance = (180, 150, 60) if not (k == 2 and "valance" in d) else (150, 50, 70)
        piece(c, RRect(x - 100, 32, x + 100, 52, 3), valance, border=1.2, shadow=PROP)
    # portraits between the windows
    for k, x in enumerate((300, 600)):
        r = frame(c, x - 50, 120, x + 50, 250, (60, 54, 52), k=9)
        dress = [(120, 50, 60), (60, 70, 110)][k]
        if k == 0 and "portrait" in d:
            dress = (200, 160, 60)
        bust(c, x, r[3], 0.55, dress, hair=(70, 50, 40), hair_style="long" if k == 0 else "short", collar="pearls" if k == 0 else "ruff")
    # wainscot
    piece(c, RRect(-10, 380, 910, 470, 0), (246, 242, 232), shadow=SMALL)
    for x in range(0, W, 90):
        flat(c, RRect(x + 10, 394, x + 80, 458, 2), (234, 228, 214))
    # parquet floor
    c.rect(0, 470, W, H, (170, 120, 80))
    for r, y in enumerate(range(470, H, 20)):
        for x in range(-40 + (r % 2) * 20, W, 40):
            flat(c, Poly([(x, y), (x + 20, y), (x + 40, y + 20), (x + 20, y + 20)]), (150, 104, 70))
    # chairs behind the table
    for k, x in enumerate((210, 330, 570, 690)):
        col = (150, 50, 60) if not (k == 3 and "chair" in d) else (60, 110, 160)
        piece(c, [RRect(x - 26, 300, x + 26, 420, 18)], (120, 80, 50), border=1.5, shadow=PROP)
        flat(c, RRect(x - 18, 312, x + 18, 400, 14), col)
    # diners (behind the table)
    lady(c, 330, 470, (90, 140, 120), hair=(140, 90, 50), h=2.4, wide=1.0)
    modern(c, 570, 470, (50, 50, 70), bottom=(50, 50, 70), hair=(200, 200, 206), h=2.6)
    flat(c, Poly([(564, 372), (580, 372), (572, 396)]), (250, 250, 248))
    # long table with cloth
    piece(c, [RRect(110, 420, 790, 436, 2), RRect(110, 436, 790, 490, 0)], (250, 250, 246), border=1.5, shadow=PROP)
    for x in range(130, 790, 40):
        flat(c, Thick(x, 440, x, 490, 1.2), (230, 230, 226))
    flat(c, [RRect(130, 490, 150, 560, 2), RRect(750, 490, 770, 560, 2)], (110, 70, 46))
    # table setting: plates, glasses, centrepiece
    for x in (210, 330, 570, 690):
        piece(c, Ell(x, 426, 22, 5), (246, 246, 242), border=1, shadow=SMALL)
        flat(c, Ell(x, 425, 12, 3), (210, 176, 92))
        flat(c, [Poly([(x + 28, 410), (x + 36, 410), (x + 33, 420), (x + 31, 420)]), Thick(x + 32, 420, x + 32, 426, 1.4)], (230, 236, 244))
    piece(c, [Ell(450, 420, 50, 8), Thick(450, 420, 450, 404, 5), Ell(450, 402, 40, 7)], (210, 176, 92), border=1, shadow=SMALL)
    fruit = [(200, 60, 70), (240, 180, 60), (120, 60, 120)]
    if "fruit" in d:
        fruit = [(120, 180, 70), (120, 180, 70), (240, 180, 60)]
    for j, (dx, dy) in enumerate(((-24, 394), (0, 392), (24, 394), (-12, 380), (12, 380), (0, 368))):
        piece(c, Circ(450 + dx, dy, 11), fruit[j % 3], shadow=SMALL)
    # roast on a platter (left) + bottle (right)
    piece(c, Ell(250, 420, 30, 6), (230, 230, 226), border=1, shadow=SMALL)
    roast = (190, 110, 60) if "roast" not in d else (240, 240, 230)
    piece(c, [Ell(250, 408, 22, 13)], roast, shadow=SMALL)
    piece(c, [RRect(632, 380, 648, 420, 3), RRect(636, 364, 644, 382, 2)], (60, 90, 60), shadow=SMALL)
    # candelabra bases
    for x in (390, 510):
        piece(c, [Ell(x, 420, 12, 4), Thick(x, 420, x, 362, 3), Thick(x - 18, 372, x + 18, 372, 2.4), Thick(x - 18, 372, x - 18, 364, 2.4),
                  Thick(x + 18, 372, x + 18, 364, 2.4)], (210, 176, 92), shadow=SMALL)
        flat(c, [RRect(x - 2.4, 348, x + 2.4, 362, 1), RRect(x - 20.4, 352, x - 15.6, 364, 1), RRect(x + 15.6, 352, x + 20.4, 364, 1)],
             (246, 240, 226))
    # chairs in front (backs towards us, low) + butler
    for x in (240, 660):
        piece(c, [RRect(x - 30, 470, x + 30, 560, 14), Thick(x - 24, 560, x - 26, 590, 4), Thick(x + 24, 560, x + 26, 590, 4)], (120, 80, 50),
              border=1.5, shadow=PROP)
        flat(c, RRect(x - 22, 480, x + 22, 548, 10), (150, 50, 60))
    modern(c, 840, 590, (40, 40, 48), bottom=(40, 40, 48), hair=(90, 70, 50), h=2.4)
    flat(c, Poly([(834, 512), (848, 512), (841, 534)]), (250, 250, 248))
    bottle = (60, 90, 60) if "bottle" not in d else (150, 40, 60)
    piece(c, [RRect(862, 480, 878, 524, 4), RRect(866, 462, 874, 482, 2)], bottle, shadow=SMALL)
    piece(c, [Ell(60, 560, 30, 10), RRect(40, 470, 80, 560, 4)], (226, 220, 210), border=1.2, shadow=PROP)       # plant stand
    piece(c, [Ell(60, 440, 30, 30), Ell(40, 420, 14, 20), Ell(80, 420, 14, 20)], (70, 130, 80), shadow=SMALL)


def l144_chandelier(x):
    def d(c, m):
        flat(c, Thick(x, 0, x, 40, 2), (180, 150, 80))
        c.ellipse_ring(x, 56, 50, 10, 3.4, GOLD)
        for k in range(7):
            xx = x - 45 + k * 15
            yy = 56 + 9 * math.sqrt(max(0, 1 - ((xx - x) / 50) ** 2))
            flat(c, Poly([(xx - 3, yy), (xx + 3, yy), (xx, yy + 12)]), (220, 236, 250))
        for dx in (-36, -12, 12, 36):
            yy = 56 + 9 * math.sqrt(max(0, 1 - (dx / 50) ** 2)) - 8
            flat(c, RRect(x + dx - 2.4, yy - 10, x + dx + 2.4, yy, 1), (246, 240, 226))
            flat(c, Poly([(x + dx - 2.6, yy - 10), (x + dx + 2.6, yy - 10), (x + dx, yy - 19)]), (255, 190, 80))
    return d


L144_ELEMENTS = [
    E("chandL", l144_chandelier(300), pivot=(300, 0), daynight="untinted", anim=dict(swingAngle=1.5, swingSpeed=0.15)),
    E("chandR", l144_chandelier(600), pivot=(600, 0), daynight="untinted", anim=dict(swingAngle=1.5, swingSpeed=0.15, phase=0.5)),
] + flame("cl0", 390, 348, 0.6, glow_night=False) + flame("cl1", 372, 352, 0.6, glow_night=False) + flame("cl2", 408, 352, 0.6, glow_night=False) \
  + flame("cr0", 510, 348, 0.6, glow_night=False) + flame("cr1", 492, 352, 0.6, glow_night=False) + flame("cr2", 528, 352, 0.6, glow_night=False)   + steam("steam", 250, 396, n=3, r=5)

L144_DIFFS = [
    ("valance", 750, 42, 0),
    ("bottle", 870, 494, 0),
    ("portrait", 300, 185, 0),
    ("fruit", 450, 385, 0),
    ("chair", 690, 356, 0),
    ("roast", 250, 408, 0),
]


LEVELS = [
    ("Level136", "现代公寓·客厅", l136_bg, L136_ELEMENTS, L136_DIFFS, 60, OPTS),
    ("Level137", "现代公寓·厨房", l137_bg, L137_ELEMENTS, L137_DIFFS, 60, OPTS),
    ("Level138", "现代公寓·卧室", l138_bg, L138_ELEMENTS, L138_DIFFS, 60, dict(OPTS, day_night=DN138, anim_seconds=40.0, frames=80)),
    ("Level139", "美式老公寓·客厅", l139_bg, L139_ELEMENTS, L139_DIFFS, 60, OPTS),
    ("Level140", "美式老公寓·厨房", l140_bg, L140_ELEMENTS, L140_DIFFS, 60, OPTS),
    ("Level141", "美式老公寓·浴室", l141_bg, L141_ELEMENTS, L141_DIFFS, 60, OPTS),
    ("Level142", "欧洲庄园·门厅", l142_bg, L142_ELEMENTS, L142_DIFFS, 60, OPTS),
    ("Level143", "欧洲庄园·书房", l143_bg, L143_ELEMENTS, L143_DIFFS, 60, OPTS),
    ("Level144", "欧洲庄园·宴会厅", l144_bg, L144_ELEMENTS, L144_DIFFS, 60, OPTS),
]
