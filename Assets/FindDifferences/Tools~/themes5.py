# -*- coding: utf-8 -*-
"""Theme levels 53-59: wizard tower, magic academy, dark fantasy, inverted city, sky city (worm's-eye),
toy city (isometric), miniature world (top-down tilt-shift)."""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, THUNDER, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, animal, barrel, bird_el, bubbles_el, bush, cloud_bg, cloud_el, crate, crystal, dead_tree,
                 drift_across, gy, house, lamp_post, layer, mushroom, person, rock, sign, sky, smoke_el, spin_el, stars_bg, sun_bg,
                 tiltshift_post, tower, tree_pine, tree_round)
from levels_views import ISO_SH, P, THICK, iso_box, iso_cyl, iso_quad, iso_tree
from stylekit import celestial, day_night, flame, moon_element, star_field, sun_element, window_glow
from weather import cloud, flash, fog_layer, lightning, rain_layer


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=36.0, frames=72)
    o.update(kw)
    return o


# =================================================================== 53 wizard tower (cut-away, night)
FLOORS = [(250, 440, 560), (250, 300, 430), (250, 150, 290)]   # (x0, y_top, y_bottom) inner rooms; x0..x1 = 250..650


def l53_bg(c, d):
    sky(c, (20, 24, 60), (60, 50, 110))
    fill_levels.back_Level53(c, d)
    stars_bg(c, 53, 90, 600)
    soft_union(c, [Circ(120, 110, 40)], (255, 250, 220), 0.35, spread=30)
    piece(c, Circ(120, 110, 36), (250, 244, 220), shadow=None)
    # tower shell
    piece(c, RRect(220, 120, 680, 600, 4), (120, 110, 130), border=3, shadow=PROP)
    piece(c, Poly([(200, 124), (700, 124), (450, 20)]), (70, 60, 130), border=3, shadow=PROP)
    for x0, y0, y1 in FLOORS:
        flat(c, RRect(x0, y0, 650, y1, 4), (210, 190, 160))
        for y in range(int(y0) + 20, int(y1), 26):
            flat(c, Thick(x0, y, 650, y, 1), (196, 176, 146))
        piece(c, RRect(236, y1, 664, y1 + 10, 2), (130, 90, 60), shadow=PROP)
    # top floor: telescope base, star map (constellation differs)
    piece(c, RRect(560, 250, 600, 290, 4), (130, 100, 70), border=1.5, shadow=PROP)
    piece(c, RRect(280, 170, 400, 250, 3), (40, 50, 90), border=3, border_col=(200, 170, 100), shadow=PROP)
    stars = [(300, 200), (330, 186), (360, 210), (380, 230)] + ([(345, 236)] if "starmap" not in d else [(300, 236)])
    flat(c, [Thick(stars[i][0], stars[i][1], stars[i + 1][0], stars[i + 1][1], 1.4) for i in range(len(stars) - 1)], (200, 210, 255))
    for x, y in stars:
        flat(c, Poly(star_pts(x, y, 5, 2)), (255, 240, 170))
    # middle floor: wizard at a desk, crystal ball, cat (missing in B)
    piece(c, [RRect(420, 380, 600, 392, 2), RRect(430, 392, 440, 430, 1), RRect(580, 392, 590, 430, 1)], (140, 96, 64), border=1.5, shadow=PROP)
    hat = (70, 160, 110) if "hat" in d else (110, 70, 170)
    hx, hy = person(c, 360, 430, (110, 70, 170), h=1.6)
    piece(c, Poly([(hx - 16, hy - 6), (hx + 16, hy - 6), (hx + 4, hy - 46)]), hat, border=1.5, shadow=SMALL)
    flat(c, Poly([(hx - 6, hy + 4), (hx + 8, hy + 4), (hx + 1, hy + 26)]), (240, 240, 245))
    if "cat" not in d:
        animal(c, "cat", 520, 380, (40, 40, 50), h=0.8)
    potion = (90, 220, 120) if "potion" in d else (230, 80, 160)
    piece(c, [Ell(600, 366, 10, 12), RRect(596, 346, 604, 356, 2)], (230, 236, 240), border=1.2, shadow=SMALL)
    flat(c, Ell(600, 370, 8, 7), potion)
    # bottom floor: library + spiral stairs
    for k in range(3):
        y = 470 + k * 30
        flat(c, Thick(270, y + 24, 420, y + 24, 3), (110, 76, 56))
        for j in range(8):
            flat(c, RRect(274 + j * 18, y + 2 + (j % 3) * 3, 288 + j * 18, y + 24, 2), [(170, 60, 60), (60, 100, 160), (80, 140, 90), (200, 160, 80)][(j + k) % 4])
    for k in range(8):
        flat(c, RRect(500 + k * 14, 550 - k * 13, 560 + k * 14, 560 - k * 13, 1), (150, 110, 80))
    # windows with an owl (missing in B)
    for y in (200, 360, 500):
        piece(c, [RRect(670, y - 20, 692, y + 20, 0), Circ(681, y - 20, 11)], (40, 40, 80), border=1.5, shadow=None)
    if "owl" not in d:
        animal(c, "owl", 700, 380, (150, 120, 90), h=0.8)


def l53_telescope(c, m):
    piece(c, [Thick(580, 252, 650, 190, 12), Thick(650, 190, 662, 180, 16)], (190, 150, 80), border=1.5, shadow=SMALL)


def l53_book(x, y, col):
    def d(c, m):
        piece(c, [Poly([(x - 16, y), (x, y + 4), (x + 16, y), (x + 16, y - 16), (x, y - 12), (x - 16, y - 16)])], col, border=1.2, shadow=SMALL)
        flat(c, Thick(x, y + 4, x, y - 12, 1.2), (250, 245, 230))
    return d


L53_EL = [
    E("telescope", l53_telescope, pivot=(580, 252), anim=dict(swingAngle=10, swingSpeed=0.12), animB={}),
    E("book1", l53_book(470, 500, (200, 70, 70)), pivot=(470, 494), anim=dict(bobAmplitude=(8, 12), bobSpeed=0.25, swingAngle=10, swingSpeed=0.3)),
    E("book2", l53_book(440, 470, (70, 110, 200)), show="A", pivot=(440, 464),
      anim=dict(bobAmplitude=(6, 10), bobSpeed=0.2, swingAngle=12, swingSpeed=0.25, phase=0.4)),
    E("ball", lambda c, m: (soft_union(c, [Circ(500, 362, 18)], (140, 200, 255), 0.5, spread=20), piece(c, Circ(500, 362, 16), (160, 210, 255), border=1.2,
                                                                                                      shadow=None)),
      daynight="untinted", anim=dict(twinkle=0.25, twinkleSpeed=0.7)),
] + flame("candle", 440, 372, 0.7, glow_night=False) + [
    E("spark%d" % i, (lambda x, y: lambda c, m: flat(c, Poly(star_pts(x, y, 5, 1.4, points=4, rot=0)), (255, 240, 180)))(x, y), pivot=(x, y),
      daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=0.6 + i * 0.15, orbitRadius=(14, 8), orbitSpeed=0.2, phase=i * 0.3))
    for i, (x, y) in enumerate(((400, 330), (480, 200), (300, 480), (620, 460)))
]
L53_DIFFS = [("telescope", 620, 220, 54), ("book", 440, 462, 40), ("hat", 368, 330, 0), ("cat", 520, 350, 0), ("potion", 600, 368, 0),
             ("starmap", 330, 220, 0), ("owl", 700, 350, 0)]


# =================================================================== 54 magic academy (side, day/night)
DN54 = day_night(40.0, tint=(0.32, 0.30, 0.58))
SUN54, MOON54 = celestial((450, 140), (420, 100), 40.0)
G54 = (380, [(30, 0.006, 0.5), (12, 0.02, 1.2)])


def l54_bg(c, d):
    sky(c, (120, 170, 230), (236, 226, 236))
    fill_levels.back_Level54(c, d)
    piece(c, Poly([(-20, 380), (120, 280), (300, 330), (520, 260), (720, 320), (920, 270), (920, 420), (-20, 420)]), (120, 130, 170), shadow=LAYER)
    layer(c, *G54, (110, 160, 110))
    # castle
    stone = (186, 180, 190)
    piece(c, RRect(300, 240, 640, 380, 2), stone, border=2, shadow=PROP)
    for x in range(300, 640, 20):
        piece(c, RRect(x, 230, x + 10, 242, 1), stone, shadow=SMALL)
    towers = [(300, 50, 220, (90, 80, 160)), (420, 44, 290, (90, 80, 160)), (520, 56, 260, (160, 60, 70)), (640, 48, 210, (90, 80, 160))]
    for i, (x, w, h, roof) in enumerate(towers):
        if i == 2 and "spire" in d:
            piece(c, RRect(x - w / 2, 380 - h, x + w / 2, 380, 2), stone, border=2, shadow=PROP)
            continue
        tower(c, x, 380, w, h, stone, roof, wins=3)
    banner = (60, 150, 90) if "banner" in d else (200, 60, 60)
    for x in (360, 580):
        piece(c, Poly([(x - 14, 260), (x + 14, 260), (x + 14, 310), (x, 300), (x - 14, 310)]), banner if x == 360 else (230, 190, 70),
              border=1.2, shadow=SMALL)
    # greenhouse
    gh = (150, 220, 240) if "greenhouse" not in d else (240, 200, 150)
    pts = [(780 + 60 * math.cos(math.radians(a)), 400 - 40 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    piece(c, Poly(pts), gh, border=2, border_col=(240, 240, 240), shadow=PROP)
    for k in range(-2, 3):
        flat(c, Thick(780 + k * 22, 400, 780 + k * 18, 362 + abs(k) * 6, 1.5), (240, 240, 240))
    # quidditch hoops (3 in A, 2 in B)
    hoops = [(100, 300), (140, 270), (180, 300)] if "hoops" not in d else [(100, 300), (180, 300)]
    for x, y in hoops:
        flat(c, Thick(x, y + 16, x, 390, 2.5), (200, 170, 90))
        c.ellipse_ring(x, y, 14, 16, 3, (230, 200, 90))
    # lake + boat
    c.rect(0, 470, W, 660, (60, 100, 150))
    piece(c, Poly([(-20, 470), (920, 460), (920, 480), (-20, 490)]), (90, 140, 100), shadow=SMALL)
    if "boat" not in d:
        piece(c, Poly([(400, 520), (480, 520), (470, 536), (410, 536)]), (160, 110, 70), border=1.5, shadow=SMALL)
        flat(c, [Thick(440, 520, 440, 496, 2)], INK)
        soft_union(c, [Circ(440, 492, 4)], (255, 220, 140), 0.6, spread=8)


def l54_broom(x, y, robe):
    def d(c, m):
        flat(c, Thick(x - 26, y + 6, x + 22, y - 2, 2.5), (150, 110, 70))
        flat(c, Poly([(x - 26, y + 6), (x - 40, y), (x - 40, y + 14)]), (200, 170, 90))
        person(c, x, y + 4, robe, h=0.6)
    return d


def l54_tentacle(c, m):
    pts = [(700 + 14 * math.sin(k * 0.7), 560 - k * 16) for k in range(7)]
    piece(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 14 - k * 1.6) for k in range(6)], (120, 80, 140), shadow=PROP)


L54_EL = [
    star_field("stars", 54, 60, 260),
    moon_element("moon", (450, 140), MOON54),
    sun_element("sun", (450, 140), SUN54, r=24),
    E("broom1", l54_broom(200, 160, (160, 50, 60)), anim=dict(drift_across(160, 230, 34), bobAmplitude=(0, 12), bobSpeed=0.3)),
    E("broom2", l54_broom(600, 120, (60, 70, 160)), anim=dict(drift_across(560, 630, -26), bobAmplitude=(0, 10), bobSpeed=0.25)),
    E("tentacle", l54_tentacle, show="A", pivot=(700, 560), anim=dict(swingAngle=12, swingSpeed=0.25, bobAmplitude=(0, 16), bobSpeed=0.12)),
    window_glow("windows", [(294, 196, 306, 212), (414, 128, 426, 144), (414, 200, 426, 216), (634, 210, 646, 226), (514, 160, 526, 176),
                            (514, 240, 526, 256), (360, 330, 380, 350), (560, 330, 580, 350)]),
    bird_el("owl", 760, 200, 10, col=(130, 100, 80), speed=16),
]
L54_DIFFS = [("banner", 360, 282, 0), ("spire", 520, 100, 0), ("greenhouse", 780, 380, 0), ("hoops", 140, 270, 0), ("boat", 440, 516, 0),
             ("tentacle", 700, 520, 70), ("door", 470, 360, 0)]


def _l54_bg(c, d):
    l54_bg(c, d)
    door = (90, 150, 210) if "door" in d else (110, 70, 50)
    flat(c, [RRect(452, 340, 488, 380, 0), Circ(470, 340, 18)], door)
    fill_levels.front_Level54(c, d)


# =================================================================== 55 dark fantasy castle (side, storm)
STEPS55 = [(OVERCAST, 8), (THUNDER, 10), (FOG, 8)]


def l55_bg(c, d):
    sky(c, (40, 34, 60), (110, 70, 90))
    fill_levels.back_Level55(c, d)
    soft_union(c, [Circ(700, 110, 46)], (255, 80, 60), 0.4, spread=40)
    piece(c, Circ(700, 110, 42), (220, 70, 60), shadow=None)
    # cliff + gothic castle
    piece(c, Poly([(380, 610), (420, 330), (520, 300), (700, 320), (760, 610)]), (50, 44, 56), shadow=LAYER)
    dark = (70, 64, 80)
    piece(c, RRect(450, 220, 700, 330, 2), dark, border=2, border_col=(110, 100, 120), shadow=PROP)
    spires = [(470, 30, 230), (540, 26, 300), (620, 34, 260), (690, 26, 220)]
    for i, (x, w, h) in enumerate(spires):
        if i == 1 and "spire" in d:
            continue
        piece(c, [RRect(x - w / 2, 330 - h, x + w / 2, 330, 1), Poly([(x - w / 2 - 6, 330 - h + 2), (x + w / 2 + 6, 330 - h + 2), (x, 330 - h - 60)])],
              dark, border=2, border_col=(110, 100, 120), shadow=PROP)
    win = (90, 220, 160) if "window" in d else (255, 80, 60)
    for x, y in ((470, 140), (620, 120), (560, 260), (660, 270)):
        soft_union(c, [RRect(x - 5, y, x + 5, y + 18, 3)], win, 0.5, spread=8)
        flat(c, RRect(x - 5, y, x + 5, y + 18, 3), win)
    gate_open = "gate" in d
    flat(c, [RRect(560, 290, 600, 330, 0), Circ(580, 290, 20)], (20, 16, 24) if gate_open else (90, 60, 50))
    if not gate_open:
        for x in range(566, 600, 8):
            flat(c, Thick(x, 276, x, 330, 2), (60, 40, 36))
    # graveyard
    layer(c, 470, [(10, 0.01, 0.3), (5, 0.03, 1.0)], (50, 56, 50))
    tombs = [(80, 1.0), (150, 0.9), (220, 1.1), (300, 0.8)] + ([] if "tomb" in d else [(800, 1.0)])
    for x, s in tombs:
        b = gy(470, [(10, 0.01, 0.3), (5, 0.03, 1.0)], x) + 12
        piece(c, [RRect(x - 16 * s, b - 40 * s, x + 16 * s, b, 4), Circ(x, b - 40 * s, 16 * s)], (120, 120, 130), shadow=PROP)
        if x == 150 and "cross" not in d:
            flat(c, [Thick(x, b - 52, x, b - 20, 3), Thick(x - 8, b - 42, x + 8, b - 42, 3)], (80, 80, 90))
    dead_tree(c, 380, 520, 1.4)
    if "raven" not in d:
        piece(c, [Ell(334, 404, 9, 6), Circ(342, 398, 4.5), Poly([(346, 398), (354, 400), (346, 402)])], (20, 20, 26), shadow=SMALL)
    fill_levels.front_Level55(c, d)


def l55_ghost(c, m):
    pts = [(160, 300), (150, 340), (160, 336), (170, 344), (180, 336), (190, 344), (200, 336), (190, 300)]
    soft_union(c, [Circ(175, 300, 22), Poly(pts)], (220, 230, 255), 0.6, spread=10)
    flat(c, [Circ(168, 298, 3), Circ(182, 298, 3), Ell(175, 310, 4, 5)], (40, 40, 60))


L55_EL = [
    E("ghost", l55_ghost, show="A", pivot=(175, 320), daynight="untinted", anim=dict(bobAmplitude=(20, 14), bobSpeed=0.12, twinkle=0.35, twinkleSpeed=0.4)),
    lightning("bolt", 300, 60, 330, interval=4.0, phase=0.3, seed=55),
    lightning("bolt2", 820, 40, 300, interval=6.3, phase=0.7, seed=56),
] + [
    E("bat%d" % i, (lambda x, y: lambda c, m: piece(c, [Poly([(x, y), (x - 12, y - 6), (x - 8, y), (x - 14, y + 2)]),
                                                     Poly([(x, y), (x + 12, y - 6), (x + 8, y), (x + 14, y + 2)]), Ell(x, y, 3, 4)], (20, 16, 26), shadow=None))(x, y),
      pivot=(x, y), anim=dict(orbitRadius=(30, 14), orbitSpeed=0.25 * (1 if i % 2 else -1), stretch=(0, 0.5), scaleSpeed=3, phase=i * 0.3))
    for i, (x, y) in enumerate(((520, 160), (620, 200), (740, 230)))
] + [
    bird_el("raven_fly", 200, 120, 11, col=(20, 20, 26), speed=18),
    rain_layer("rain", 55, 80, 30, 1.3, 0.6, 300, mask=W_(THUNDER), col=(200, 200, 230)),
    flash("flash", 4.0, 0.3, alpha=0.35),
    fog_layer("fog1", 55, 300, 480, 0.55, 9, 1, col=(150, 150, 170)),
    fog_layer("fog2", 56, 450, 600, 0.6, 12, -1, col=(150, 150, 170)),
]
L55_DIFFS = [("spire", 540, 100, 0), ("window", 560, 270, 0), ("gate", 580, 300, 0), ("tomb", 800, 470, 0), ("cross", 150, 452, 0),
             ("raven", 342, 400, 0), ("ghost", 175, 320, 50)]


# =================================================================== 56 inverted city
def l56_bg(c, d):
    sky(c, (160, 210, 240), (200, 230, 250))
    # top: upside-down city hanging from the "ground" at the top
    piece(c, RRect(-10, -10, 910, 40, 0), (110, 150, 100), shadow=PROP)
    piece(c, RRect(-10, 40, 910, 62, 0), (90, 90, 100), shadow=SMALL)
    tops = [(60, 140, 150, (220, 200, 180)), (180, 120, 200, (190, 200, 220)), (330, 160, 130, (230, 190, 170)), (530, 120, 220, (200, 210, 190)),
            (690, 140, 160, (220, 210, 230)), (840, 110, 190, (210, 190, 170))]
    for i, (x, w, h, col) in enumerate(tops):
        piece(c, RRect(x - w / 2, 62, x + w / 2, 62 + h, 2), col, border=2, shadow=PROP)
        piece(c, Poly([(x - w / 2 - 6, 60 + h), (x + w / 2 + 6, 60 + h), (x, 60 + h + w * 0.35)]), lit(col, 0.7), border=2, shadow=PROP)
        for y in range(80, int(62 + h) - 10, 30):
            for xx in range(int(x - w / 2) + 12, int(x + w / 2) - 16, 26):
                col_w = (255, 210, 120) if (i == 3 and y == 110 and "window" in d) else (130, 160, 200)
                flat(c, RRect(xx, y, xx + 14, y + 16, 2), col_w)
    if "clock" not in d:
        piece(c, Circ(330, 170, 18), (250, 250, 240), border=2, shadow=SMALL)
        flat(c, [Thick(330, 170, 330, 182, 2), Thick(330, 170, 322, 166, 2)], INK)
    # bottom: normal city
    piece(c, RRect(-10, 540, 910, 610, 0), (110, 150, 100), shadow=PROP)
    piece(c, RRect(-10, 518, 910, 540, 0), (90, 90, 100), shadow=SMALL)
    bots = [(100, 150, 140, (210, 190, 170)), (280, 130, 180, (200, 214, 230)), (460, 150, 120, (230, 200, 180)), (640, 120, 200, (210, 220, 200)),
            (800, 150, 150, (226, 210, 236))]
    for i, (x, w, h, col) in enumerate(bots):
        piece(c, RRect(x - w / 2, 518 - h, x + w / 2, 518, 2), col, border=2, shadow=PROP)
        roof = (90, 150, 210) if (i == 2 and "roof" in d) else lit(col, 0.7)
        piece(c, Poly([(x - w / 2 - 6, 520 - h), (x + w / 2 + 6, 520 - h), (x, 520 - h - w * 0.35)]), roof, border=2, shadow=PROP)
        for y in range(int(518 - h) + 14, 500, 30):
            for xx in range(int(x - w / 2) + 12, int(x + w / 2) - 16, 26):
                flat(c, RRect(xx, y, xx + 14, y + 16, 2), (130, 160, 200))
    for x in (40, 200, 380, 560, 880):
        if x == 380 and "tree" in d:
            continue
        tree_round(c, x, 540, 0.6)
    lamp_post(c, 720, 520, 60) if "lamp" not in d else None
    piece(c, [RRect(560, 62, 640, 90, 3)], (240, 190, 70) if "board" not in d else (90, 170, 120), border=2, shadow=PROP)


def l56_car(y, col, flip, speed):
    def d(c, m):
        s = -1 if flip else 1
        piece(c, [RRect(100, y - 10 * s - 6, 160, y - 10 * s + 6, 5), RRect(112, y - 22 * s - 6, 148, y - 22 * s + 4, 4)], col, border=1.5, shadow=SMALL)
        flat(c, [Circ(114, y, 6), Circ(146, y, 6)], (50, 45, 50))
    return E("car%d" % y, d, anim=drift_across(98, 162, speed))


def l56_balloon(c, m):
    col = (90, 170, 230) if m else (230, 80, 90)
    flat(c, Thick(450, 300, 450, 340, 1.2), INK)
    piece(c, Ell(450, 286, 18, 22), col, border=1.5, shadow=SMALL)


L56_EL = [
    cloud_el("cloud1", 200, 290, 0.8, 8),
    cloud_el("cloud2", 700, 320, 0.7, -6),
    l56_car(56, (230, 80, 80), True, -50),
    l56_car(530, (80, 140, 220), False, 60),
    E("balloon", l56_balloon, variant=True, pivot=(450, 310), anim=dict(bobAmplitude=(0, 60), bobSpeed=0.08, swingAngle=6, swingSpeed=0.3)),
    bird_el("bird", 300, 380, 9, speed=18),
    E("bird_up", lambda c, m: piece(c, [Thick(600, 240, 612, 244, 2.5), Thick(612, 244, 624, 240, 2.5)], (80, 85, 100), shadow=None), pivot=(612, 242),
      anim=dict(drift_across(598, 626, -20), stretch=(0, 0.5), scaleSpeed=2.4)),
]
L56_DIFFS = [("window", 545, 118, 0), ("clock", 330, 170, 0), ("roof", 460, 380, 0), ("tree", 380, 500, 0), ("lamp", 726, 480, 0),
             ("board", 600, 76, 0), ("balloon", 450, 286, 80)]


# =================================================================== 57 sky city (worm's-eye)
VP57 = (450, 300)


def l57_bg(c, d):
    for r, col in ((520, (150, 200, 245)), (380, (126, 182, 240)), (260, (104, 164, 234)), (150, (90, 150, 228))):
        flat(c, Circ(*VP57, r), col)
    sun_bg(c, 760, 100, 34, col=(255, 240, 190))
    # underside of the floating rock city (seen from below)
    rockp = [(200, 190), (330, 140), (500, 130), (680, 160), (760, 230), (700, 330), (560, 380), (380, 370), (240, 310)]
    piece(c, Poly(rockp), (140, 110, 100), shadow=(0, 10, 18, 0.35))
    flat(c, Poly([(450, 370), (560, 380), (700, 330), (760, 230), (600, 300)]), (120, 92, 86))
    # towers on the rim, foreshortened (pointing outward from the centre)
    for i, (a, ln, col) in enumerate(((200, 120, (220, 214, 230)), (240, 150, (230, 220, 200)), (300, 140, (220, 214, 230)), (340, 110, (210, 220, 236)))):
        rx, ry = VP57[0] + 230 * math.cos(math.radians(a)), VP57[1] + 120 * math.sin(math.radians(a))
        tx, ty = VP57[0] + (230 + ln) * math.cos(math.radians(a)), VP57[1] + (120 + ln) * math.sin(math.radians(a))
        ux, uy = (tx - rx) / ln, (ty - ry) / ln
        vx, vy = -uy, ux
        body = Poly([(rx + vx * 24, ry + vy * 24), (tx + vx * 16, ty + vy * 16), (tx - vx * 16, ty - vy * 16), (rx - vx * 24, ry - vy * 24)])
        piece(c, body, col, border=2, shadow=SMALL)
        flat(c, Poly([(rx + vx * 24, ry + vy * 24), (tx + vx * 16, ty + vy * 16), (tx + vx * 4, ty + vy * 4), (rx + vx * 6, ry + vy * 6)]),
             lit(col, 0.82))
        for t in (0.3, 0.6):
            wx, wy = rx + (tx - rx) * t, ry + (ty - ry) * t
            flat(c, Circ(wx, wy, 5), (90, 110, 160))
        apex = (tx + ux * 34, ty + uy * 34)
        piece(c, Poly([(tx + vx * 22, ty + vy * 22), apex, (tx - vx * 22, ty - vy * 22)]), (110, 120, 200), border=2, shadow=SMALL)
        if not (i == 2 and "flag" in d):
            piece(c, Poly([apex, (apex[0] + ux * 4 + vx * 16, apex[1] + uy * 4 + vy * 16), (apex[0] + ux * 12, apex[1] + uy * 12)]),
                  (230, 70, 70), shadow=None)
    # hanging roots and crystals
    roots = [(300, 300), (380, 360), (520, 370), (640, 320)]
    for i, (x, y) in enumerate(roots):
        if i == 2 and "root" in d:
            continue
        flat(c, [Thick(x, y, x + (x - 450) * 0.2, y + 40, 3), Thick(x + (x - 450) * 0.2, y + 40, x + (x - 450) * 0.3, y + 70, 2)], (110, 80, 60))
    crystal_col = (120, 230, 160) if "crystal" in d else (160, 120, 255)
    for x, y in ((450, 390), (600, 360)):
        piece(c, Poly([(x - 12, y - 10), (x + 12, y - 10), (x, y + 30)]), crystal_col, shadow=SMALL)
    if "window" not in d:
        piece(c, [RRect(410, 196, 430, 220, 2)], (255, 222, 140), border=1.5, shadow=None)
    if "balcony" not in d:
        piece(c, RRect(330, 190, 380, 206, 3), (230, 220, 200), border=1.5, shadow=SMALL)
    fill_levels.front_Level57(c, d)


def l57_airship(c, m):
    col = (90, 170, 120) if m else (240, 150, 70)
    piece(c, Ell(170, 460, 50, 18), col, border=1.5, shadow=SMALL)
    piece(c, RRect(150, 480, 190, 490, 3), (140, 100, 70), shadow=SMALL)


def l57_drop(a):
    def d(c, m):
        x, y = VP57[0] + 200 * math.cos(math.radians(a)), VP57[1] + 100 * math.sin(math.radians(a))
        flat(c, [Circ(x, y, 3), Poly([(x - 2.5, y - 1), (x + 2.5, y - 1), (x, y - 7)])], (200, 230, 255))
    return d


L57_EL = [
    E("airship", l57_airship, variant=True, pivot=(170, 470), anim=dict(bobAmplitude=(14, 6), bobSpeed=0.08)),
    cloud_el("cloud1", 150, 120, 0.9, 8),
    cloud_el("cloud2", 700, 520, 1.0, -6),
] + [
    E("bird%d" % i, (lambda x, y: lambda c, m: piece(c, [Thick(x - 9, y - 4, x, y, 2.4), Thick(x, y, x + 9, y - 4, 2.4)], (70, 75, 90), shadow=None))(x, y),
      pivot=VP57, anim=dict(orbitRadius=(330, 220), orbitSpeed=0.04, phase=i * 0.05, stretch=(0, 0.5), scaleSpeed=2.4))
    for i, (x, y) in enumerate(((450, 300), (450, 300), (450, 300)))
] + [
    E("fall%d" % i, l57_drop(a), pivot=(VP57[0] + 200 * math.cos(math.radians(a)), VP57[1] + 100 * math.sin(math.radians(a))), show="A" if a == 70 else "both",
      daynight="untinted", anim=dict(driftVelocity=(math.cos(math.radians(a)) * 80, -math.sin(math.radians(a)) * 80), driftLength=160, driftFade=True,
                                     driftGrow=2.5, phase=i * 0.37 % 1))
    for i, a in enumerate((70, 100, 130, 30))
]
L57_DIFFS = [("flag", 660, 42, 0), ("root", 520, 400, 0), ("crystal", 525, 380, 0), ("balcony", 355, 198, 0), ("airship", 170, 470, 0),
             ("window", 420, 210, 0), ("waterfall", 548, 470, 110)]


# =================================================================== 58 toy city (isometric, god's-eye 1 of 3)
def toy_block(c, X, Y, dx, dy, dz, col, letter=None):
    top, left, right = iso_box(c, X, Y, 0, dx, dy, dz, col, border=2)
    if letter:
        cx = (P(X + dx / 2, Y + dy, dz / 2))
        flat(c, Circ(cx[0], cx[1], 14), (255, 255, 255))
        flat(c, [Thick(cx[0] - 7, cx[1] + 8, cx[0], cx[1] - 8, 3.4), Thick(cx[0], cx[1] - 8, cx[0] + 7, cx[1] + 8, 3.4),
                 Thick(cx[0] - 4, cx[1] + 2, cx[0] + 4, cx[1] + 2, 3)], letter)


def l58_decor(c, X, Y, r):
    x, y = P(X, Y)
    cols = [(230, 80, 80), (90, 160, 230), (250, 200, 60), (120, 200, 120), (170, 110, 220)]
    col = cols[int(r * 50) % 5]
    if r < 0.45:
        toy_block(c, X, Y, 0.7, 0.7, 0.7, col, letter=col if r < 0.2 else None)
    elif r < 0.6:
        iso_cyl(c, X, Y, 0, 0.2, 0.12, col, border=1.2)
        a, b = P(X, Y, 0.1), P(X + 1.2, Y, 0.1)
        piece(c, Thick(a[0], a[1], b[0], b[1], 7), col, border=1.2, shadow=ISO_SH)
    elif r < 0.75:
        piece(c, Circ(x, y - 14, 15), col, border=2, shadow=ISO_SH)
        flat(c, [Thick(x - 15, y - 14, x + 15, y - 14, 2)], (255, 255, 255))
    elif r < 0.9:
        iso_box(c, X, Y, 0, 0.9, 0.5, 0.3, col, border=1.5)
        for wx in (X + 0.15, X + 0.7):
            a = P(wx, Y + 0.5, 0.1)
            piece(c, Circ(a[0], a[1], 5), (60, 60, 70), shadow=None)
    else:
        piece(c, [Circ(x, y - 30, 14), Circ(x, y - 12, 18), Circ(x - 10, y - 42, 6), Circ(x + 10, y - 42, 6)], (190, 140, 90), border=1.5,
              shadow=ISO_SH)
        flat(c, [Circ(x - 4, y - 32, 2), Circ(x + 4, y - 32, 2)], INK)


def _l58_surround():
    from fill_iso import surround_points
    return surround_points(58, step=80, keep=0.5)


L58_SURROUND = _l58_surround()


def l58_bg(c, d):
    # play mat on a wooden playroom floor, toys scattered all around
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (214, 176, 130), None)
    for k in range(-24, 34):
        a, b = P(k, -24), P(k, 34)
        flat(c, Thick(a[0], a[1], b[0], b[1], 1.6), (190, 150, 108))
    top = iso_quad(0, 0, 10, 10)
    piece(c, top, (110, 190, 220), border=3, shadow=(2, 4, 6, 0.3))
    draw_surround(c, L58_SURROUND, l58_decor, "back")
    # printed roads on the play mat
    for q in (iso_quad(4.3, 0, 5.7, 10), iso_quad(0, 4.3, 10, 5.7)):
        flat(c, q, (90, 90, 100))
    for k in range(10):
        a, b = P(5.0, k + 0.2), P(5.0, k + 0.6)
        flat(c, Thick(a[0], a[1], b[0], b[1], 2), (250, 250, 250))
    # train track (oval)
    cx, cy = P(7.4, 7.4)
    c.ellipse_ring(cx, cy, 90, 45, 6, (150, 110, 80))
    # block buildings
    toy_block(c, 1.0, 1.0, 1.4, 1.4, 1.6, (230, 80, 80), letter=(230, 80, 80))
    toy_block(c, 1.2, 1.2, 1.0, 1.0, 1.0 + 1.6, (250, 200, 60))
    toy_block(c, 7.0, 1.0, 1.6, 1.2, 1.2, (90, 160, 230) if "block" not in d else (120, 200, 120), letter=(60, 120, 200))
    piece(c, Poly([P(7.0, 1.0, 1.2), P(8.6, 1.0, 1.2), P(7.8, 1.6, 2.2)]), (240, 140, 60), border=2, shadow=ISO_SH)
    toy_block(c, 1.2, 7.2, 1.2, 1.2, 1.2, (170, 110, 220), letter=(170, 110, 220) if "letter" not in d else (230, 80, 80))
    toy_block(c, 2.6, 7.4, 0.8, 0.8, 0.8, (250, 160, 190))
    # toy trees (one missing in B)
    for X, Y in ((3.0, 2.6), (8.6, 4.0), (3.2, 8.8)):
        if (X, Y) == (8.6, 4.0) and "tree" in d:
            continue
        x, y = P(X, Y)
        piece(c, [RRect(x - 4, y - 30, x + 4, y, 2), Circ(x, y - 40, 16)], (80, 190, 110), border=2, shadow=ISO_SH)
    # toy soldier
    x, y = P(3.6, 6.2)
    hat = (60, 60, 70) if "soldier" not in d else (230, 60, 60)
    piece(c, [RRect(x - 7, y - 34, x + 7, y, 3), Circ(x, y - 40, 7)], (200, 50, 60), border=1.5, shadow=ISO_SH)
    piece(c, RRect(x - 7, y - 60, x + 7, y - 44, 3), hat, shadow=None)
    # crane base
    x, y = P(6.4, 2.6)
    piece(c, [RRect(x - 8, y - 90, x + 8, y, 2)], (250, 200, 60), border=2, shadow=ISO_SH)
    from fill_iso import draw_surround
    draw_surround(c, L58_SURROUND, l58_decor, "front")


def l58_crane(c, m):
    x, y = P(6.4, 2.6)
    piece(c, [Thick(x - 50, y - 92, x + 70, y - 92, 6)], (250, 200, 60), border=1.5, shadow=SMALL)
    flat(c, Thick(x + 60, y - 92, x + 60, y - 60, 1.2), INK)
    piece(c, RRect(x + 52, y - 60, x + 68, y - 48, 2), (230, 80, 80), shadow=SMALL)


def l58_train(i):
    cx, cy = P(7.4, 7.4)
    col = [(230, 80, 80), (90, 160, 230), (250, 200, 60)][i]

    def d(c, m):
        piece(c, [RRect(cx - 14, cy - 18, cx + 14, cy + 2, 4), Circ(cx - 8, cy + 4, 4), Circ(cx + 8, cy + 4, 4)], col, border=1.5, shadow=SMALL)
    return E("train%d" % i, d, pivot=(cx, cy), anim=dict(orbitRadius=(90, 45), orbitSpeed=0.08, orbitDepth=0.15, phase=-i * 0.07),
             animB=dict(orbitRadius=(90, 45), orbitSpeed=-0.08, orbitDepth=0.15, phase=i * 0.07))


def l58_car(c, m):
    a = P(5.4, 1.0)
    piece(c, [RRect(a[0] - 14, a[1] - 12, a[0] + 14, a[1] + 2, 5), Circ(a[0] - 8, a[1] + 4, 4), Circ(a[0] + 8, a[1] + 4, 4)], (240, 130, 60), border=1.5,
          shadow=SMALL)


def l58_balloon(c, m):
    col = (120, 200, 120) if m else (230, 80, 90)
    piece(c, Ell(200, 120, 28, 34), col, border=2, shadow=PROP)
    flat(c, [Ell(200, 120, 9, 34)], (255, 230, 120))
    piece(c, RRect(190, 160, 210, 172, 2), (180, 120, 70), shadow=SMALL)


_ca, _cb = P(5.4, 1.0), P(5.4, 9.0)
L58_EL = [
    E("balloon", l58_balloon, variant=True, pivot=(200, 140), anim=dict(bobAmplitude=(6, 10), bobSpeed=0.12)),
    E("crane", l58_crane, pivot=(P(6.4, 2.6)[0], P(6.4, 2.6)[1] - 92), anim=dict(swingAngle=14, swingSpeed=0.1),
      animB=dict(swingAngle=-14, swingSpeed=0.1)),
    E("car", l58_car, anim=dict(driftVelocity=((_cb[0] - _ca[0]) / 8 * 0.6, -(_cb[1] - _ca[1]) / 8 * 0.6), driftLength=math.hypot(_cb[0] - _ca[0], _cb[1] - _ca[1]),
                                 driftFade=True)),
] + [l58_train(i) for i in range(3)]
L58_DIFFS = [("block", int(P(7.8, 1.6, 0.8)[0]), int(P(7.8, 1.6, 0.8)[1]), 0), ("letter", int(P(1.8, 8.4, 0.6)[0]), int(P(1.8, 8.4, 0.6)[1]), 0),
             ("tree", int(P(8.6, 4.0)[0]), int(P(8.6, 4.0)[1] - 30), 0), ("soldier", int(P(3.6, 6.2)[0]), int(P(3.6, 6.2)[1] - 50), 0),
             ("balloon", 200, 130, 0), ("crane", int(P(6.4, 2.6)[0] + 10), int(P(6.4, 2.6)[1] - 80), 70),
             ("train", int(P(7.4, 7.4)[0]), int(P(7.4, 7.4)[1]), 100)]


# =================================================================== 59 miniature world (top-down, tilt-shift; god's-eye 2 of 3)
def l59_bg(c, d):
    c.rect(0, 0, W, 660, (120, 180, 100))
    for r in ((0, 280, 900, 330), (420, 0, 480, 600)):
        piece(c, RRect(*r, 0), (100, 100, 110), shadow=SMALL)
    for x in range(0, 900, 40):
        flat(c, RRect(x, 303, x + 20, 307, 1), (250, 250, 250))
    for y in range(0, 600, 40):
        flat(c, RRect(448, y, 452, y + 20, 1), (250, 250, 250))
    # houses (roofs from above)
    houses = [(80, 80, (200, 80, 70)), (200, 70, (90, 130, 200)), (320, 90, (230, 180, 70)), (600, 70, (150, 90, 160)), (740, 100, (200, 80, 70)),
              (80, 420, (110, 160, 110)), (220, 440, (230, 120, 80)), (620, 420, (90, 130, 200))]
    for i, (x, y, col) in enumerate(houses):
        if i == 3 and "roof" in d:
            col = (240, 200, 70)
        piece(c, RRect(x - 34, y - 26, x + 34, y + 26, 2), col, border=2, shadow=(5, 8, 6, 0.45))
        flat(c, RRect(x - 34, y - 26, x + 34, y, 2), lit(col, 1.15))
    # park with pond + trees, pool
    piece(c, Ell(760, 470, 110, 70), (100, 170, 90), shadow=SMALL)
    piece(c, Ell(760, 480, 50, 26), (90, 160, 210), border=2, shadow=None)
    for x, y in ((690, 420), (840, 430), (700, 520), (830, 530), (760, 400)):
        if (x, y) == (840, 430) and "tree" in d:
            continue
        piece(c, Circ(x, y, 14), (60, 130, 70), shadow=(4, 6, 5, 0.45))
    piece(c, RRect(260, 170, 360, 230, 6), (240, 236, 226), shadow=SMALL)
    flat(c, RRect(270, 180, 350, 220, 5), (110, 200, 230))
    if "umbrella" not in d:
        piece(c, Circ(372, 186, 12), (230, 80, 80), shadow=(4, 6, 4, 0.4))
    # parked cars
    for i, x in enumerate((520, 560, 600)):
        col = [(230, 80, 80), (250, 250, 250), (90, 140, 220)][i]
        if i == 1 and "car" in d:
            col = (60, 60, 70)
        piece(c, RRect(x - 10, 352, x + 10, 380, 4), col, border=1, shadow=(2, 3, 3, 0.4))
    # crowd in the square (5 vs 4 people)
    people = [(156, 248), (174, 260), (192, 246), (146, 266)] + ([] if "people" in d else [(204, 266)])
    for x, y in people:
        piece(c, Circ(x, y, 6), (230, 120, 80), shadow=(2, 3, 2, 0.4))


def l59_car(y, col, speed):
    def d(c, m):
        piece(c, RRect(100, y - 9, 130, y + 9, 4), col, border=1, shadow=(2, 3, 3, 0.4))
    return E("car%d" % y, d, anim=drift_across(98, 132, speed))


def l59_boat(c, m):
    piece(c, Ell(760, 480, 9, 4), (250, 250, 250), border=1, shadow=None)


L59_EL = [
    l59_car(294, (230, 80, 80), 60),
    l59_car(316, (90, 140, 220), -50),
    E("carv", lambda c, m: piece(c, RRect(432, 100, 446, 128, 4), (250, 200, 60), border=1, shadow=(2, 3, 3, 0.4)),
      anim=dict(driftVelocity=(0, -50), driftLength=700, driftStart=-140, phase=140 / 700)),
    E("boat", l59_boat, show="A", pivot=(760, 480), anim=dict(orbitRadius=(30, 12), orbitSpeed=0.08, orbitAlign=True)),
] + [
    E("walker%d" % i, (lambda x, y: lambda c, m: piece(c, Circ(x, y, 3.5), (250, 220, 120), shadow=(2, 3, 2, 0.4)))(x, y), pivot=(x, y),
      anim=dict(bobAmplitude=(30, 0), bobSpeed=0.05 + i * 0.01, phase=i * 0.3))
    for i, (x, y) in enumerate(((520, 260), (640, 340), (300, 340)))
]
L59_DIFFS = [("roof", 600, 70, 0), ("tree", 840, 430, 0), ("umbrella", 372, 186, 0), ("car", 560, 366, 0), ("people", 204, 266, 0),
             ("boat", 760, 480, 40), ("bench", 300, 468, 0)]


def _l59_bg(c, d):
    l59_bg(c, d)
    if "bench" not in d:
        piece(c, RRect(280, 462, 320, 474, 2), (150, 100, 60), shadow=(3, 4, 3, 0.4))
    fill_levels.front_Level59(c, d)


LEVELS = [
    ("Level53", "巫师塔", l53_bg, L53_EL, L53_DIFFS, 140, opts()),
    ("Level54", "魔法学院", _l54_bg, L54_EL, L54_DIFFS, 140, opts(day_night=DN54, anim_seconds=40.0, frames=80)),
    ("Level55", "暗黑城堡", l55_bg, L55_EL, L55_DIFFS, 140,
     opts(weather=dict(steps=STEPS55, blend=3.0, tints={FOG: (0.8, 0.8, 0.86)}), anim_seconds=26.0, frames=52)),
    ("Level56", "倒置城市", l56_bg, L56_EL, L56_DIFFS, 140, opts()),
    ("Level57", "天空之城", l57_bg, L57_EL, L57_DIFFS, 140, opts()),
    ("Level58", "玩具城市", l58_bg, L58_EL, L58_DIFFS, 140, opts()),
    ("Level59", "微缩世界", _l59_bg, L59_EL, L59_DIFFS, 140, opts(post=tiltshift_post)),
]
