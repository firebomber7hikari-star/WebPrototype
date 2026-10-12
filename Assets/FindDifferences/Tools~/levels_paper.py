# -*- coding: utf-8 -*-
"""
Paper-craft levels (cut paper diorama look):
  Level06 纸艺海港 (paper harbour: sliding paper waves, boat between wave layers)
  Level07 纸艺秋林 (paper autumn forest: layered hills, stand-up fox that flips around)

Every prop is a paper piece (white cut border + soft drop shadow); scenery layers cast a
soft halo onto the layer behind. All images get a paper-grain pass (paper.paper_post).
"""
import math

from fdcore import E, W
from paper import (Circ, Ell, Poly, RRect, Thick, flat, hill_strip, hill_y, paper_post, piece, soft_union,
                   star_pts, wave_strip, ngon)

OPTS = {"post": paper_post}
INK = (70, 55, 65)
PROP = (2, 4, 7, 0.42)        # shadow for props
LAYER = (1, 3, 11, 0.36)      # shadow for big scenery layers


def drift_across(x_left, x_right, speed, start_offset=0.0):
    s_min = -(x_right + 10)
    length = W + 10 - x_left - s_min
    return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min,
                phase=((start_offset - s_min) / length) % 1.0)


def arc(cx, cy, r, a0, a1, width, n=10):
    """A stroked arc as a list of Thick segments (angles in degrees, y down)."""
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], width) for i in range(n)]


def taper_band(xl0, xr0, y0, xl1, xr1, y1, ya, yb):
    """Horizontal band [ya, yb] of a trapezoid whose sides go from (xl0/xr0, y0) to (xl1/xr1, y1)."""
    def side(x0, x1, y):
        return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return Poly([(side(xl0, xl1, ya), ya), (side(xr0, xr1, ya), ya), (side(xr0, xr1, yb), yb), (side(xl0, xl1, yb), yb)])


# =================================================================== Level 06
HILL6 = [(16, 0.014, 0.8), (7, 0.035, 2.0)]


def l6_left_hill():
    pts = []
    for x in range(-60, 300, 8):
        pts.append((x, hill_y(232, HILL6, x)))
    pts += [(320, 270), (345, 330), (350, 660), (-60, 660)]
    return Poly(pts)


HOUSES6 = [(75, (240, 180, 120), (205, 80, 70)), (155, (150, 190, 230), None), (235, (250, 222, 150), (110, 160, 120))]
ROOF_A, ROOF_B = (90, 110, 200), (245, 190, 70)


def l6_house(c, x, wall, roof, w=50, h=40):
    base = hill_y(232, HILL6, x) + 10
    y0 = base - h
    piece(c, RRect(x - w / 2, y0, x + w / 2, base, 2), wall, border=2.5, shadow=PROP)
    flat(c, RRect(x - 8, base - 18, x + 4, base, 1.5), (110, 80, 85))
    flat(c, RRect(x + 9, y0 + 9, x + 19, y0 + 19, 1.5), (255, 235, 170))
    piece(c, Poly([(x - w / 2 - 7, y0 + 3), (x + w / 2 + 7, y0 + 3), (x, y0 - 30)]), roof, border=2.5, shadow=PROP)


def l6_background(c, d):
    """纸艺海港 - static part"""
    c.rect(0, 0, W, 660, (168, 216, 228))
    piece(c, hill_strip(262, [(10, 0.01, 0.3), (6, 0.03, 1.0)]), (195, 230, 232), shadow=LAYER)
    piece(c, Poly([(150, 340), (210, 288), (260, 275), (330, 262), (400, 285), (450, 340)]), (150, 205, 190), shadow=LAYER)
    piece(c, Poly([(520, 340), (580, 290), (640, 255), (700, 280), (740, 340)]), (140, 198, 188), shadow=LAYER)
    c.rect(0, 328, W, 660, (100, 178, 216))
    # left hill with a little paper village
    piece(c, l6_left_hill(), (150, 205, 120), shadow=LAYER)
    for x, wall, roof in HOUSES6:
        if roof is None:
            roof = ROOF_B if "roof" in d else ROOF_A
        l6_house(c, x, wall, roof)
    for x in (30, 115, 195, 280):
        y = hill_y(232, HILL6, x) + 12
        piece(c, [Circ(x, y - 22, 13), Thick(x, y - 12, x, y + 4, 4)], (90, 160, 95), border=2, shadow=PROP)
    # cliff with lighthouse
    cliff = Poly([(640, 660), (648, 430), (676, 330), (700, 262), (760, 248), (830, 254), (900, 240), (980, 240), (980, 660)])
    piece(c, cliff, (210, 172, 130), shadow=LAYER)
    flat(c, Poly([(660, 380), (980, 330), (980, 352), (664, 404)]), (190, 152, 115))
    flat(c, Poly([(650, 470), (980, 430), (980, 452), (652, 494)]), (190, 152, 115))
    piece(c, Poly([(690, 282), (700, 260), (760, 246), (830, 252), (900, 238), (980, 238), (980, 262), (900, 262),
                   (830, 274), (760, 270), (706, 290)]), (120, 185, 110), shadow=(1, 3, 6, 0.3))
    # lighthouse: white tapered tower with red bands (3 in A, 2 in B)
    tower = Poly([(770, 254), (810, 254), (802, 140), (778, 140)])
    piece(c, tower, (250, 247, 240), border=3, shadow=PROP)
    bands = [(214, 232), (178, 196), (146, 162)] if "stripes" not in d else [(214, 232), (146, 162)]
    for ya, yb in bands:
        flat(c, taper_band(770, 810, 254, 778, 802, 140, ya, yb), (222, 72, 70))
    flat(c, RRect(784, 236, 796, 254, 2), (95, 75, 85))
    piece(c, RRect(772, 128, 808, 141, 2), (75, 75, 95), border=2, shadow=PROP)
    piece(c, RRect(779, 108, 801, 128, 2), (255, 228, 130), border=2, shadow=None)
    flat(c, [Thick(784, 110, 784, 126, 1.5), Thick(796, 110, 796, 126, 1.5)], (75, 75, 95))
    piece(c, Poly([(774, 110), (806, 110), (790, 88)]), (222, 72, 70), border=2, shadow=PROP)


def l6_sun_rays(c, m):
    piece(c, Poly(star_pts(130, 85, 64, 47, points=12)), (255, 185, 80), shadow=PROP)


def l6_sun_face(c, m):
    piece(c, Circ(130, 85, 41), (255, 222, 95), border=3, shadow=PROP)
    flat(c, [Circ(118, 80, 4.5), Circ(142, 80, 4.5)], INK)
    flat(c, [Circ(110, 93, 6), Circ(150, 93, 6)], (255, 165, 140))
    if m:
        flat(c, Circ(130, 99, 5), INK)
    else:
        flat(c, arc(130, 88, 13, 25, 155, 3), INK)


def l6_cloud(xs, y, string_top, r):
    def d(c, m):
        flat(c, Thick(xs, string_top, xs, y - r * 0.8, 1.3), (120, 110, 115))
        piece(c, [Circ(xs - r * 1.05, y + r * 0.35, r * 0.8), Circ(xs, y, r), Circ(xs + r * 1.05, y + r * 0.35, r * 0.8),
                  RRect(xs - r * 1.6, y + r * 0.2, xs + r * 1.6, y + r * 1.0, r * 0.4)], (252, 252, 247), shadow=PROP)
    return d


def l6_plane(c, m):
    piece(c, [Poly([(500, 140), (460, 127), (474, 141)]), Poly([(500, 140), (462, 152), (476, 142)])], (250, 250, 246),
          shadow=PROP)
    flat(c, Poly([(500, 140), (462, 152), (476, 142)]), (226, 226, 222))
    flat(c, Poly([(500, 140), (474, 142), (470, 148)]), (200, 200, 198))


def l6_gull(x, y, s):
    def d(c, m):
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.25), Thick(x, y, x + s, y - s * 0.4, s * 0.25)], (95, 105, 120),
              shadow=(1, 3, 4, 0.3))
    return d


def l6_beam(c, m):
    c.polygon([(790, 118), (915, 70), (915, 160)], (255, 245, 185, 0.42))


def l6_wave(top, amp, period, phase, col):
    def d(c, m):
        piece(c, wave_strip(top, amp, period, phase), col, border=3, shadow=(1, 3, 9, 0.35))
    return d


def l6_boat(c, m):
    flat(c, Thick(452, 352, 452, 262, 3), (120, 80, 60))
    piece(c, Poly([(452, 262), (475, 268), (452, 275)]), (60, 170, 90) if m else (230, 60, 60), border=1.5, shadow=PROP)
    piece(c, Poly([(456, 270), (456, 344), (512, 344)]), (252, 250, 244), border=2, shadow=PROP)
    piece(c, Poly([(448, 280), (448, 344), (406, 344)]), (240, 218, 186), border=2, shadow=PROP)
    piece(c, Poly([(392, 350), (508, 350), (492, 384), (408, 384)]), (205, 92, 72), border=3, shadow=PROP)
    flat(c, Poly([(394, 355), (506, 355), (504, 361), (397, 361)]), (250, 230, 200))
    flat(c, [Circ(425, 370, 4), Circ(450, 370, 4), Circ(475, 370, 4)], (250, 230, 200))


def l6_fish(c, m):
    piece(c, [Ell(300, 455, 21, 11), Poly([(316, 455), (334, 443), (334, 467)])], (255, 150, 60), border=2, shadow=PROP)
    flat(c, Poly([(296, 446), (306, 446), (304, 464), (296, 464)]), (255, 205, 120))
    flat(c, Circ(287, 452, 2.6), INK)


def l6_buoy(c, m):
    flat(c, Thick(640, 462, 640, 446, 3), (80, 80, 95))
    piece(c, Circ(640, 443, 5), (255, 230, 120), border=1.5, shadow=None)
    piece(c, [Circ(640, 480, 16), RRect(628, 462, 652, 480, 4)], (245, 200, 60) if m else (225, 70, 70),
          border=2.5, shadow=PROP)
    flat(c, RRect(624, 472, 656, 479, 1), (252, 250, 244))


WAVE = dict(bobSpeed=0.1)
L6_ELEMENTS = [
    E("sun_rays", l6_sun_rays, pivot=(130, 85), anim=dict(rotateSpeed=10)),
    E("sun", l6_sun_face, pivot=(130, 85), variant=True, anim=dict(swingAngle=6, swingSpeed=0.25)),
    E("cloud1", l6_cloud(330, 72, -10, 26), pivot=(330, -5), anim=dict(swingAngle=5, swingSpeed=0.2)),
    E("cloud", l6_cloud(557, 52, -10, 22), pivot=(557, -5), show="A", anim=dict(swingAngle=6, swingSpeed=0.24, phase=0.4)),
    E("plane", l6_plane, pivot=(480, 140),
      anim=dict(drift_across(460, 502, 30), bobAmplitude=(0, 12), bobSpeed=0.3, swingAngle=7, swingSpeed=0.3)),
    E("gull1", l6_gull(270, 120, 15), pivot=(270, 117),
      anim=dict(stretch=(0, 0.5), scaleSpeed=2.0, bobAmplitude=(20, 6), bobSpeed=0.1)),
    E("gull2", l6_gull(650, 118, 12), pivot=(650, 116),
      anim=dict(stretch=(0, 0.5), scaleSpeed=2.4, bobAmplitude=(16, 5), bobSpeed=0.12, phase=0.5)),
    E("beam", l6_beam, pivot=(790, 118), anim=dict(swingAngle=22, swingSpeed=0.15, twinkle=0.3, twinkleSpeed=0.3)),
    E("wave1", l6_wave(340, 12, 60, 0.0, (118, 194, 226)), anim=dict(WAVE, bobAmplitude=(18, 0))),
    E("boat", l6_boat, pivot=(450, 380), variant=True,
      anim=dict(bobAmplitude=(0, 6), bobSpeed=0.3, swingAngle=4, swingSpeed=0.25)),
    E("wave2", l6_wave(390, 13, 70, 0.3, (92, 170, 214)), anim=dict(WAVE, bobAmplitude=(-20, 0), bobSpeed=0.12)),
    # the fish only leaps in the original; in the modified picture it stays hidden behind wave3
    E("fish", l6_fish, pivot=(300, 455),
      anim=dict(bobAmplitude=(0, 88), bobSpeed=0.22, bounce=True, swingAngle=20, swingSpeed=0.22, phase=0.1), animB={}),
    E("wave3", l6_wave(447, 14, 80, 0.6, (70, 148, 198)), anim=dict(WAVE, bobAmplitude=(16, 0), bobSpeed=0.09)),
    E("buoy", l6_buoy, pivot=(640, 500), variant=True,
      anim=dict(bobAmplitude=(0, 5), bobSpeed=0.35, swingAngle=8, swingSpeed=0.3)),
    E("wave4", l6_wave(514, 15, 90, 0.1, (50, 124, 178)), anim=dict(WAVE, bobAmplitude=(-14, 0), bobSpeed=0.11)),
]

L6_DIFFS = [
    ("sunface", 130, 92, 24),
    ("cloud", 557, 58, 42),
    ("roof", 155, int(hill_y(232, HILL6, 155) - 40), 30),
    ("flag", 462, 268, 20),
    ("stripes", 790, 186, 28),
    ("fish", 300, 400, 58),
    ("buoy", 640, 472, 26),
]


# =================================================================== Level 07
HILLS7 = [
    (300, [(25, 0.008, 0.3), (10, 0.02, 1.2)], (242, 170, 132)),
    (360, [(22, 0.01, 2.0), (9, 0.025, 0.4)], (218, 128, 106)),
    (420, [(20, 0.009, 4.0), (8, 0.03, 2.2)], (178, 98, 90)),
    (500, [(18, 0.011, 1.0), (7, 0.028, 3.0)], (122, 72, 78)),
]


def ground(layer, x):
    top, waves, _ = HILLS7[layer]
    return hill_y(top, waves, x)


def pine(c, x, base, h, col, trunk=(120, 75, 60)):
    flat(c, RRect(x - 3, base - 10, x + 3, base + 6, 1), trunk)
    tiers = [Poly([(x, base - h + k * h * 0.24), (x - h * (0.2 + k * 0.08), base - h * (0.5 - k * 0.2)),
                   (x + h * (0.2 + k * 0.08), base - h * (0.5 - k * 0.2))]) for k in range(3)]
    piece(c, tiers, col, shadow=PROP)


def round_tree(c, x, base, r, col, trunk=(125, 78, 62)):
    piece(c, [Thick(x, base + 4, x, base - r, 5), Circ(x, base - r * 1.6, r)], col, shadow=PROP)
    flat(c, Thick(x, base + 4, x, base - r * 0.8, 5), trunk)


PINE_DIFF_X = 400
HOUSE_X = 560
HOUSE_BASE = ground(2, HOUSE_X) + 8
MUSH_X = 120
MUSH_BASE = ground(3, MUSH_X) + 8
RABBIT_X = 330
RABBIT_BASE = ground(3, RABBIT_X) + 6
FOX_X = 640
FOX_BASE = ground(3, FOX_X) + 4
PINWHEEL = (500, HOUSE_BASE - 86)
CHIMNEY = (HOUSE_X + 26, HOUSE_BASE - 82)


def l7_background(c, d):
    """纸艺秋林 - static part"""
    c.rect(0, 0, W, 660, (255, 216, 172))
    # sun, moon and clouds are elements (they move with the day/night cycle)

    # hill layers with trees between them (each layer's halo falls on the one behind)
    for li, (top, waves, col) in enumerate(HILLS7):
        piece(c, hill_strip(top, waves), col, shadow=LAYER)
        if li == 0:
            for x in range(30, 900, 70):
                pine(c, x, ground(0, x) + 6, 46, (226, 150, 118))
        elif li == 1:
            for x, kind in ((60, 0), (150, 1), (250, 0), (PINE_DIFF_X, 0), (470, 1), (720, 0), (800, 1), (870, 0)):
                if x == PINE_DIFF_X and "pine" in d:
                    continue
                if kind == 0:
                    pine(c, x, ground(1, x) + 6, 70, (196, 104, 86))
                else:
                    round_tree(c, x, ground(1, x) + 6, 20, (240, 160, 84))
        elif li == 2:
            for x, kind in ((40, 1), (140, 0), (230, 1), (700, 0), (780, 1), (860, 0)):
                if kind == 0:
                    pine(c, x, ground(2, x) + 6, 90, (150, 72, 68))
                else:
                    round_tree(c, x, ground(2, x) + 6, 26, (232, 128, 60))
            # cottage, pinwheel pole
            b = HOUSE_BASE
            piece(c, RRect(CHIMNEY[0] - 7, b - 92, CHIMNEY[0] + 7, b - 50, 2), (160, 90, 80), border=2, shadow=PROP)
            piece(c, RRect(HOUSE_X - 34, b - 52, HOUSE_X + 34, b, 3), (250, 222, 170), border=3, shadow=PROP)
            piece(c, Poly([(HOUSE_X - 44, b - 48), (HOUSE_X + 44, b - 48), (HOUSE_X, b - 88)]), (190, 70, 64), border=3,
                  shadow=PROP)
            flat(c, RRect(HOUSE_X + 6, b - 30, HOUSE_X + 22, b, 2), (120, 75, 70))
            win = (90, 62, 75) if "window" in d else (255, 220, 120)
            flat(c, RRect(HOUSE_X - 24, b - 40, HOUSE_X - 6, b - 22, 2), win)
            flat(c, [Thick(HOUSE_X - 15, b - 40, HOUSE_X - 15, b - 22, 1.5), Thick(HOUSE_X - 24, b - 31, HOUSE_X - 6, b - 31, 1.5)],
                 (150, 95, 80))
            piece(c, Thick(PINWHEEL[0], b, PINWHEEL[0], PINWHEEL[1], 3.5), (150, 110, 90), border=1.5, shadow=PROP)
    # front layer details: mushroom (red in A / blue in B), bushes, grass
    b = MUSH_BASE
    piece(c, RRect(MUSH_X - 9, b - 34, MUSH_X + 9, b, 4), (250, 238, 215), border=2.5, shadow=PROP)
    cap = [(MUSH_X + 36 * math.cos(math.radians(a)), b - 30 - 28 * math.sin(math.radians(a))) for a in range(0, 181, 12)]
    piece(c, Poly(cap), (80, 120, 220) if "mushroom" in d else (225, 80, 70), border=3, shadow=PROP)
    flat(c, [Circ(MUSH_X - 16, b - 42, 5), Circ(MUSH_X + 6, b - 50, 6), Circ(MUSH_X + 22, b - 38, 4)], (255, 248, 236))
    for x, r in ((220, 20), (245, 15), (470, 18), (800, 22), (830, 16)):
        piece(c, [Circ(x, ground(3, x) + 2 - r * 0.6, r)], (95, 120, 80), shadow=PROP)
    for x in range(20, 900, 46):
        y = ground(3, x) + 26
        flat(c, Poly([(x - 8, y), (x - 4, y - 14), (x, y - 4), (x + 4, y - 16), (x + 8, y)]), (150, 92, 92))


def l7_balloon(c, m):
    stripe = (240, 110, 90) if m else (255, 240, 200)
    flat(c, [Thick(176, 195, 182, 213, 1.3), Thick(204, 195, 198, 213, 1.3)], (110, 85, 80))
    piece(c, RRect(180, 211, 200, 226, 2), (175, 112, 75), border=2, shadow=PROP)
    piece(c, [Circ(190, 160, 36), Poly([(158, 172), (222, 172), (204, 200), (176, 200)])], (110, 165, 215), border=3,
          shadow=PROP)
    flat(c, [Ell(190, 160, 12, 36), Poly([(184, 196), (196, 196), (200, 172), (180, 172)])], stripe)


def l7_bird(x, y, s):
    def d(c, m):
        piece(c, [Thick(x - s, y - s * 0.4, x, y, s * 0.25), Thick(x, y, x + s, y - s * 0.4, s * 0.25)], (120, 70, 80),
              shadow=(1, 3, 4, 0.25))
    return d


def l7_smoke(c, m):
    piece(c, Circ(CHIMNEY[0], CHIMNEY[1] - 12, 9), (250, 242, 232), shadow=(1, 3, 5, 0.25))


def l7_pinwheel(c, m):
    x, y = PINWHEEL
    cols = [(240, 90, 80), (255, 200, 80), (90, 170, 220), (120, 200, 120)]
    for k in range(4):
        a = math.radians(k * 90)
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        tri = Poly([(x, y), (x + ux * 28, y + uy * 28), (x + ux * 6 + vx * 22, y + uy * 6 + vy * 22)])
        piece(c, tri, cols[k], border=1.5, shadow=(1, 2, 4, 0.3))
    piece(c, Circ(x, y, 4), (250, 245, 235), shadow=None)


def l7_leaf(x, y, col):
    def d(c, m):
        piece(c, [Poly(star_pts(x, y, 11, 5, points=5)), Thick(x, y, x + 3, y + 10, 1.5)], col, border=1.5, shadow=PROP)
    return d


def l7_fox(c, m):
    x, b = FOX_X, FOX_BASE
    orange, cream, dark = (240, 130, 60), (255, 240, 220), (90, 60, 65)
    piece(c, [Thick(x - 14, b - 14, x - 16, b, 4), Thick(x + 10, b - 14, x + 12, b, 4)], dark, border=2, shadow=PROP)
    piece(c, Poly([(x - 20, b - 24), (x - 48, b - 46), (x - 56, b - 30), (x - 34, b - 16)]), orange, border=2.5, shadow=PROP)
    flat(c, Poly([(x - 48, b - 46), (x - 56, b - 30), (x - 50, b - 34)]), cream)
    piece(c, Ell(x - 2, b - 24, 22, 13), orange, border=2.5, shadow=PROP)
    flat(c, Ell(x + 2, b - 19, 12, 6), cream)
    piece(c, [Poly([(x + 12, b - 46), (x + 40, b - 34), (x + 14, b - 22)]),
              Poly([(x + 14, b - 44), (x + 16, b - 60), (x + 25, b - 42)])], orange, border=2.5, shadow=PROP)
    flat(c, Poly([(x + 22, b - 36), (x + 40, b - 34), (x + 20, b - 26)]), cream)
    flat(c, [Circ(x + 40, b - 34, 2.6), Circ(x + 24, b - 39, 2)], dark)


def l7_rabbit(c, m):
    x, b = RABBIT_X, RABBIT_BASE
    white, pink = (252, 250, 245), (250, 175, 185)
    piece(c, [Ell(x - 2, b - 14, 17, 14), Circ(x + 14, b - 30, 11), Ell(x + 9, b - 50, 4.5, 13), Ell(x + 19, b - 50, 4.5, 13),
              Circ(x - 19, b - 18, 6)], white, border=0, shadow=PROP)
    flat(c, [Ell(x + 9, b - 50, 2, 9), Ell(x + 19, b - 50, 2, 9)], pink)
    flat(c, [Circ(x + 18, b - 32, 2), Circ(x + 25, b - 28, 1.6)], INK)


LEAVES7 = [(120, 40, (235, 110, 60)), (300, 10, (250, 190, 70)), (480, 30, (220, 80, 70)),
           (640, 0, (245, 150, 60)), (820, 20, (250, 200, 90)), (60, 120, (230, 120, 70))]

# ---- day / night cycle --------------------------------------------------------
# One full day + night every 40 s. Sun and moon share one orbit half a turn apart:
# the sun is at the top at t = 0 (midday) and sets on the left while night falls.
DAY_NIGHT7 = dict(period=40.0, phase=0.0, tint=(0.30, 0.34, 0.60))
SKY_ORBIT = dict(orbitRadius=(400, 130), orbitSpeed=1 / 40.0)
ORBIT_CENTRE = (450, 200)      # low enough to set, high enough that the fading sun stays above the hills


def l7_sun(c, m):
    x, y = ORBIT_CENTRE
    for r, col in ((46, (255, 196, 148)), (35, (255, 172, 120)), (25, (255, 150, 100)), (15, (255, 128, 86))):
        piece(c, Circ(x, y, r), col, shadow=(1, 3, 8, 0.25))


def l7_moon(c, m):
    x, y = ORBIT_CENTRE
    soft_union(c, [Circ(x, y, 34)], (255, 250, 220), 0.35, spread=16)
    piece(c, Circ(x, y, 26), (252, 246, 220), border=2, shadow=PROP)
    flat(c, [Circ(x - 8, y - 6, 6), Circ(x + 9, y + 7, 4), Circ(x + 6, y - 10, 3)], (232, 224, 196))


def l7_stars(c, m):
    import random as _r
    rnd = _r.Random(70)
    for _ in range(46):
        x, y = rnd.uniform(10, 890), rnd.uniform(10, 235)
        if (130 < x < 262 and 70 < y < 130) or (748 < x < 852 and 38 < y < 92):
            continue
        r = rnd.choice((2.5, 3.5, 5))
        flat(c, Poly(star_pts(x, y, r, r * 0.35, points=4, rot=0)), (255, 248, 210))


def l7_firefly(x, y):
    def d(c, m):
        soft_union(c, [Circ(x, y, 5)], (230, 255, 150), 0.55, spread=7)
        flat(c, Circ(x, y, 2.2), (250, 255, 210))
    return d


def l7_window_glow(c, m):
    b = HOUSE_BASE
    soft_union(c, [RRect(HOUSE_X - 24, b - 40, HOUSE_X - 6, b - 22, 2)], (255, 210, 110), 0.55, spread=16)
    flat(c, RRect(HOUSE_X - 24, b - 40, HOUSE_X - 6, b - 22, 2), (255, 232, 150))
    flat(c, [Thick(HOUSE_X - 15, b - 40, HOUSE_X - 15, b - 22, 1.5), Thick(HOUSE_X - 24, b - 31, HOUSE_X - 6, b - 31, 1.5)],
         (190, 130, 80))


def l7_cloud(x, y, k):
    def d(c, m):
        piece(c, [Circ(x - 26 * k, y + 9 * k, 20 * k), Circ(x, y, 26 * k), Circ(x + 28 * k, y + 10 * k, 20 * k),
                  RRect(x - 56 * k, y + 8 * k, x + 56 * k, y + 26 * k, 9 * k)], (255, 238, 215), shadow=PROP)
    return d


FIREFLIES7 = [(90, 430), (250, 455), (420, 470), (600, 445), (760, 470), (860, 430), (330, 395), (690, 400)]

L7_ELEMENTS = [
    E("stars", l7_stars, daynight="night", anim=dict(twinkle=0.25, twinkleSpeed=0.6)),
    E("moon", l7_moon, pivot=ORBIT_CENTRE, daynight="night", anim=dict(SKY_ORBIT, phase=0.75)),
    E("sun", l7_sun, pivot=ORBIT_CENTRE, daynight="day", anim=dict(SKY_ORBIT, phase=0.25, pulse=0.03, scaleSpeed=0.3)),
    E("cloud1", l7_cloud(196, 100, 1.0), anim=dict(bobAmplitude=(30, 0), bobSpeed=0.02)),
    E("cloud2", l7_cloud(800, 66, 0.8), anim=dict(bobAmplitude=(-24, 0), bobSpeed=0.025, phase=0.3)),
    E("balloon", l7_balloon, pivot=(190, 165), variant=True,
      anim=dict(bobAmplitude=(0, 10), bobSpeed=0.15, swingAngle=3, swingSpeed=0.12)),
] + [
    E("bird%d" % i, l7_bird(x, y, s), pivot=(x, y - 2), daynight="day",
      anim=dict(drift_across(x - s, x + s, 22, 0), stretch=(0, 0.5), scaleSpeed=2.2 + 0.3 * i,
                bobAmplitude=(0, 6), bobSpeed=0.2))
    for i, (x, y, s) in enumerate(((330, 90, 12), (360, 105, 10), (300, 110, 9)))
] + [
    E("smoke%d" % i, l7_smoke, show="A",
      anim=dict(driftVelocity=(6, 22), driftLength=70, driftFade=True, driftGrow=1.2, phase=i / 3))
    for i in range(3)
] + [
    E("pinwheel", l7_pinwheel, pivot=PINWHEEL, anim=dict(rotateSpeed=-110), animB=dict(rotateSpeed=110)),
    # stand-up fox walking back and forth; it flips around (spinSnap) at the turning points
    E("fox", l7_fox, pivot=(FOX_X, FOX_BASE),
      anim=dict(bobAmplitude=(90, 0), bobSpeed=0.07, spinSpeed=0.07, spinSnap=0.85, spinShade=0.25,
                swingAngle=4, swingSpeed=1.3)),
    E("rabbit", l7_rabbit, pivot=(RABBIT_X, RABBIT_BASE),
      anim=dict(bobAmplitude=(0, 24), bobSpeed=0.55, bounce=True), animB={}),
] + [
    E("leaf%d" % i, l7_leaf(x, y, col),
      anim=dict(driftVelocity=(12, -26), driftLength=420, driftFade=True, rotateSpeed=60 + 15 * i,
                spinSpeed=0.5 + 0.1 * i, spinShade=0.3, bobAmplitude=(16, 0), bobSpeed=0.3, phase=i / len(LEAVES7)))
    for i, (x, y, col) in enumerate(LEAVES7)
] + [
    E("window_glow", l7_window_glow, show="A", daynight="night", anim=dict(twinkle=0.15, twinkleSpeed=1.1)),
] + [
    E("firefly%d" % i, l7_firefly(x, y), daynight="night",
      anim=dict(orbitRadius=(14 + i % 3 * 6, 9 + i % 2 * 5), orbitSpeed=(0.1 + i % 4 * 0.04) * (1 if i % 2 else -1),
                twinkle=0.8, twinkleSpeed=0.5 + i % 3 * 0.2, phase=i * 0.13))
    for i, (x, y) in enumerate(FIREFLIES7)
]

L7_DIFFS = [
    ("rabbit", RABBIT_X + 4, int(RABBIT_BASE - 32), 42),
    ("pinwheel", PINWHEEL[0], int(PINWHEEL[1]), 34),
    ("balloon", 190, 175, 46),
    ("window", HOUSE_X - 15, int(HOUSE_BASE - 31), 18),
    ("pine", PINE_DIFF_X, int(ground(1, PINE_DIFF_X) - 28), 32),
    ("mushroom", MUSH_X, int(MUSH_BASE - 40), 34),
    ("smoke", CHIMNEY[0] + 4, int(CHIMNEY[1] - 36), 32),
]


LEVELS = [
    ("Level06", "纸艺海港", l6_background, L6_ELEMENTS, L6_DIFFS, 130, OPTS),
    ("Level07", "纸艺秋林", l7_background, L7_ELEMENTS, L7_DIFFS, 140,
     dict(OPTS, day_night=DAY_NIGHT7, anim_seconds=40.0, frames=80)),
]
