# -*- coding: utf-8 -*-
"""Theme levels 29-34: steampunk, sci-fi, shelter, wasteland, quarantine zone (top-down), laboratory."""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, HEAT, OVERCAST, RAIN, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, barrel, bird_el, bubbles_el, cactus, cloud_bg, cloud_el, crate, drift_across, fence,
                 gear, gear_shapes, glow_el, gy, house, lamp_post, layer, person, pipe, rock, sign, sky, smoke_el, spin_el, stars_bg,
                 sun_bg)
from stylekit import celestial, day_night, moon_element, neon, star_field, sun_element, window_glow
from weather import WET, fog_layer, rain_layer, sun_glare, heat_haze, splash_rings

SUN_CENTRE = (450, 190)


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=36.0, frames=72)
    o.update(kw)
    return o


# =================================================================== 29 steampunk workshop (side, smog weather)
BRASS, COPPER, BRICK = (200, 160, 80), (190, 110, 70), (150, 92, 72)
G29 = [(462, [(6, 0.01, 0.3)])]


def l29_bg(c, d):
    sky(c, (226, 196, 150), (250, 228, 186))
    fill_levels.back_Level29(c, d)
    rnd = random.Random(29)
    x = -20
    while x < 920:
        w, h = rnd.randint(50, 90), rnd.randint(120, 260)
        piece(c, RRect(x, 420 - h, x + w, 440, 1), (170, 130, 100), shadow=None)
        if rnd.random() < 0.5:
            piece(c, RRect(x + w * 0.4, 420 - h - 40, x + w * 0.4 + 12, 420 - h, 1), (150, 112, 88), shadow=None)
        x += w + rnd.randint(2, 10)
    # clock tower
    piece(c, RRect(400, 120, 500, 470, 2), BRICK, border=2, shadow=PROP)
    for y in range(130, 470, 14):
        flat(c, Thick(402, y, 498, y, 1), lit(BRICK, 0.85))
    piece(c, Poly([(390, 124), (510, 124), (450, 60)]), (90, 110, 100), border=2, shadow=PROP)
    face = (180, 220, 200) if "clock" in d else (250, 238, 210)
    piece(c, Circ(450, 190, 34), face, border=3, border_col=BRASS, shadow=PROP)
    for k in range(12):
        a = math.radians(k * 30)
        flat(c, Thick(450 + 27 * math.cos(a), 190 + 27 * math.sin(a), 450 + 31 * math.cos(a), 190 + 31 * math.sin(a), 2), INK)
    # left workshop with gear wall, right factory
    piece(c, RRect(60, 250, 330, 470, 2), (176, 140, 110), border=2, shadow=PROP)
    piece(c, RRect(560, 230, 860, 470, 2), (160, 120, 96), border=2, shadow=PROP)
    for i, x in enumerate((600, 660, 720, 780)):
        if i == 2 and "window" in d:
            flat(c, RRect(x, 290, x + 36, 340, 3), lit((160, 120, 96), 0.85))
            for y in range(294, 340, 8):
                flat(c, Thick(x, y, x + 36, y, 1), lit((160, 120, 96), 0.7))
            continue
        piece(c, RRect(x, 290, x + 36, 340, 3), (255, 226, 150), border=2, border_col=BRASS, shadow=None)
        flat(c, Thick(x + 18, 290, x + 18, 340, 2), BRASS)
    for x in (620, 760):
        piece(c, RRect(x, 140, x + 26, 232, 2), BRICK, border=2, shadow=PROP)
    # pipes with a valve wheel
    pipe(c, [(330, 300), (370, 300), (370, 420), (400, 420)], 12, COPPER)
    pipe(c, [(500, 360), (540, 360), (540, 260), (560, 260)], 12, COPPER)
    valve = (90, 140, 210) if "valve" in d else (210, 60, 60)
    piece(c, Circ(540, 310, 14), valve, border=1.5, shadow=SMALL)
    flat(c, [Thick(526, 310, 554, 310, 2.5), Thick(540, 296, 540, 324, 2.5)], lit(valve, 0.6))
    # street
    piece(c, RRect(-10, 462, 910, 610, 0), (128, 108, 94), shadow=LAYER)
    for x in range(0, 900, 30):
        for y in (480, 510, 540, 570):
            flat(c, RRect(x + (y // 30 % 2) * 15, y, x + (y // 30 % 2) * 15 + 26, y + 24, 3), (140, 120, 104))
    for x in (150, 700):
        if x == 700 and "lamp" in d:
            continue
        lamp_post(c, x, 466, 90, col=(70, 60, 50), light=(255, 220, 140))
    sign(c, 250, 466, col=BRASS)
    fill_levels.front_Level29(c, d)


def l29_gear(x, y, r, col):
    return lambda c, m: gear(c, x, y, r, col, teeth=max(8, int(r / 4)))


def l29_hands(c, m):
    flat(c, [Thick(450, 190, 450, 166, 3), Circ(450, 190, 3)], INK)


def l29_hand_short(c, m):
    flat(c, Thick(450, 190, 466, 190, 3.5), INK)


def l29_airship(c, m):
    bal = (90, 150, 120) if m else (190, 90, 70)
    piece(c, Ell(210, 90, 90, 32), bal, border=2, shadow=PROP)
    for k in (-1, 0, 1):
        flat(c, Thick(130, 90 + k * 14, 290, 90 + k * 14, 1.5), lit(bal, 0.8))
    piece(c, [RRect(170, 132, 250, 152, 6), Poly([(296, 90), (318, 74), (318, 106)])], (140, 100, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(180, 120, 186, 132, 1.5), Thick(240, 120, 234, 132, 1.5)], INK)


def l29_prop(c, m):
    flat(c, [Ell(160, 142, 3, 14), Ell(160, 142, 14, 3)], (90, 80, 70))


L29_EL = [
    sun_element("sun", SUN_CENTRE, celestial(SUN_CENTRE, (420, 150), 36.0)[0], r=24),
    E("airship", l29_airship, variant=True, pivot=(210, 110), anim=dict(bobAmplitude=(14, 6), bobSpeed=0.08, swingAngle=2, swingSpeed=0.1)),
    spin_el("prop", l29_prop, (160, 142), 400),
    spin_el("gear1", l29_gear(130, 340, 42, BRASS), (130, 340), 30),
    spin_el("gear2", l29_gear(199, 388, 30, COPPER), (199, 388), -42),
    spin_el("gear3", l29_gear(270, 330, 36, BRASS), (270, 330), 35, speed_b=-35),
    spin_el("hand_long", l29_hands, (450, 190), 6),
    spin_el("hand_short", l29_hand_short, (450, 190), 0.5),
] + smoke_el("smoke", 633, 132, col=(200, 190, 180), r=11, show="A", length=90) + smoke_el("smoke_b", 773, 132, col=(200, 190, 180), r=11, length=90) + [
    E("tram", lambda c, m: (piece(c, [RRect(560, 490, 680, 540, 8), RRect(580, 470, 660, 494, 4)], (110, 130, 120), border=2, shadow=PROP),
                            flat(c, [Circ(585, 542, 8), Circ(655, 542, 8)], (60, 55, 50))), anim=drift_across(560, 680, 30)),
    fog_layer("smog1", 29, 200, 360, 0.5, 10, 1, col=(220, 200, 170)),
    fog_layer("smog2", 30, 360, 520, 0.55, 14, -1, col=(220, 200, 170)),
]
L29_DIFFS = [("gear", 270, 330, 52), ("airship", 220, 100, 0), ("smoke", 640, 90, 50), ("clock", 450, 190, 0), ("valve", 540, 310, 0),
             ("window", 678, 315, 0), ("lamp", 710, 420, 0)]


# =================================================================== 30 sci-fi spaceport (side, day/night)
DN30 = day_night(40.0, tint=(0.36, 0.30, 0.62))
SUN30, MOON30 = celestial((450, 180), (420, 140), 40.0)
G30 = (470, [(10, 0.009, 1.0), (5, 0.03, 0.2)])


def l30_bg(c, d):
    sky(c, (90, 70, 160), (255, 170, 160))
    fill_levels.back_Level30(c, d)
    # ringed planet
    soft_union(c, [Circ(720, 120, 70)], (255, 200, 220), 0.3, spread=40)
    c.ellipse_ring(720, 120, 120, 26, 6, (250, 220, 200), ymax=120)
    piece(c, Circ(720, 120, 70), (220, 130, 170), shadow=None)
    flat(c, [Ell(720, 100, 66, 6), Ell(716, 140, 60, 5)], (240, 160, 190))
    c.ellipse_ring(720, 120, 120, 26, 6, (250, 220, 200), ymin=120)
    layer(c, 360, [(30, 0.006, 0.4), (12, 0.02, 1.5)], (110, 90, 150))
    layer(c, 410, [(20, 0.008, 2.0), (8, 0.025, 0.4)], (90, 75, 130))
    layer(c, *G30, (70, 64, 110))
    # domes & towers
    for x, r, col in ((140, 60, (180, 220, 240)), (320, 44, (190, 230, 220)), (600, 52, (200, 210, 250))):
        if x == 320 and "dome" in d:
            col = (250, 200, 140)
        b = gy(*G30, x) + 8
        pts = [(x + r * math.cos(math.radians(a)), b - r * math.sin(math.radians(a))) for a in range(0, 181, 10)]
        piece(c, Poly(pts), col, border=2, shadow=PROP)
        flat(c, [Thick(x - r * 0.7, b - r * 0.45, x + r * 0.7, b - r * 0.45, 1.5), Thick(x, b - r, x, b, 1.5)], lit(col, 0.8))
    for x, h in ((460, 200), (800, 240)):
        b = gy(*G30, x) + 8
        piece(c, [RRect(x - 18, b - h, x + 18, b, 4), Poly([(x - 26, b - h), (x + 26, b - h), (x, b - h - 30)])], (200, 205, 220), border=2,
              shadow=PROP)
        for k in range(6):
            y = b - h + 20 + k * (h - 30) / 6
            on = (k % 2 == 0) if not ("lights" in d and x == 800) else (k % 3 == 0)
            flat(c, RRect(x - 10, y, x + 10, y + 8, 2), (120, 240, 255) if on else (80, 90, 120))
        if not (x == 460 and "antenna" in d):
            piece(c, Thick(x, b - h - 30, x, b - h - 66, 2.5), (200, 205, 220), shadow=None)
    # landing pad
    piece(c, RRect(560, gy(*G30, 650) - 6, 740, gy(*G30, 650) + 8, 3), (150, 150, 170), border=2, shadow=PROP)
    flat(c, [Thick(600, gy(*G30, 650), 700, gy(*G30, 650), 2)], (255, 220, 80))
    # rail
    flat(c, Thick(0, 300, 900, 300, 4), (210, 210, 230))
    fill_levels.front_Level30(c, d)


def l30_ship(c, m):
    col = (240, 140, 80) if m else (120, 200, 240)
    x, y = 650, 380
    piece(c, [Ell(x, y, 54, 16), Poly([(x - 20, y - 10), (x + 20, y - 10), (x + 8, y - 30), (x - 8, y - 30)])], col, border=2, shadow=PROP)
    flat(c, Ell(x, y - 18, 10, 6), (220, 250, 255))
    soft_union(c, [Ell(x, y + 18, 26, 6)], (150, 220, 255), 0.5, spread=10)


def l30_dish(c, m):
    piece(c, [Ell(230, 380, 22, 26), Thick(230, 380, 248, 376, 2)], (230, 232, 240), border=1.5, shadow=SMALL)


def l30_robot(c, m):
    x, b = 380, gy(*G30, 380) + 6
    piece(c, [RRect(x - 10, b - 34, x + 10, b - 8, 4), Circ(x, b - 42, 9), Thick(x - 6, b - 8, x - 6, b, 3), Thick(x + 6, b - 8, x + 6, b, 3)],
          (200, 205, 215), border=1.5, shadow=PROP)
    flat(c, Circ(x + 4, b - 43, 2.6), (255, 80, 80) if m else (80, 220, 255))


def l30_train(c, m):
    piece(c, [RRect(100, 284, 260, 300, 8), Poly([(260, 284), (284, 292), (260, 300)])], (240, 240, 250), border=1.5, shadow=SMALL)
    for x in range(115, 250, 22):
        flat(c, RRect(x, 288, x + 14, 294, 2), (120, 200, 255))


L30_EL = [
    star_field("stars", 30, 60, 300),
    moon_element("moon", (450, 180), MOON30, col=(220, 240, 255)),
    sun_element("sun", (450, 180), SUN30, r=22),
    E("train", l30_train, anim=drift_across(100, 284, 70)),
    E("ship", l30_ship, variant=True, pivot=(650, 380), anim=dict(bobAmplitude=(0, 8), bobSpeed=0.3)),
    E("dish", l30_dish, pivot=(230, 380), anim=dict(spinSpeed=0.15, spinShade=0.3), animB={}),
    E("robot", l30_robot, variant=True, pivot=(380, gy(*G30, 380)), anim=dict(bobAmplitude=(50, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85)),
    E("beacon", lambda c, m: (soft_union(c, [Circ(800, gy(*G30, 800) - 312, 4)], (255, 60, 60), 0.8, spread=12),
                              flat(c, Circ(800, gy(*G30, 800) - 312, 3.5), (255, 140, 140))),
      show="A", daynight="untinted", anim=dict(blinkInterval=1.2, blinkDuration=0.5)),
    window_glow("windows", [(130, gy(*G30, 140) - 20, 150, gy(*G30, 140) - 8), (590, gy(*G30, 600) - 18, 610, gy(*G30, 600) - 6)],
                col=(150, 230, 255)),
]
L30_DIFFS = [("ship", 650, 375, 0), ("dish", 230, 380, 34), ("beacon", 800, int(gy(*G30, 800) - 312), 26), ("dome", 320, 440, 0),
             ("antenna", 460, 250, 0), ("robot", 382, 430, 0), ("lights", 800, 330, 0)]


# =================================================================== 31 shelter cross-section
SURF = 140
ROOMS = [(40, 170, 300, 300), (310, 170, 590, 300), (600, 170, 860, 300), (40, 310, 300, 440), (310, 310, 590, 440), (600, 310, 860, 440),
         (40, 450, 450, 580), (460, 450, 860, 580)]


def l31_bg(c, d):
    sky(c, (170, 180, 175), (200, 200, 190))
    piece(c, RRect(-10, SURF, 910, 610, 0), (120, 100, 85), shadow=LAYER)
    piece(c, RRect(-10, SURF - 8, 910, SURF + 6, 0), (140, 130, 100), shadow=None)
    for x in range(10, 900, 40):
        flat(c, Poly([(x - 4, SURF - 6), (x - 1, SURF - 18), (x + 2, SURF - 6)]), (150, 140, 96))
    dead = (100, 90, 80)
    piece(c, [Thick(120, SURF - 4, 120, 60, 5), Thick(120, 90, 96, 66, 3), Thick(120, 100, 146, 74, 3)], dead, shadow=PROP)
    # hatch
    piece(c, RRect(430, SURF - 22, 520, SURF - 4, 4), (110, 120, 110), border=2, shadow=PROP)
    hatch = (220, 200, 60) if "hatch" in d else (200, 60, 60)
    piece(c, Circ(475, SURF - 30, 12), hatch, border=1.5, shadow=SMALL)
    # concrete rooms
    for i, (x0, y0, x1, y1) in enumerate(ROOMS):
        piece(c, RRect(x0, y0, x1, y1, 2), (200, 198, 188), border=0, shadow=(0, 2, 6, 0.35))
        flat(c, RRect(x0, y1 - 10, x1, y1, 0), (170, 168, 160))
    flat(c, RRect(455, 170, 470, 580, 0), (90, 85, 80))    # elevator shaft line
    # room contents
    # 0 generator
    piece(c, RRect(60, 230, 160, 290, 6), (110, 130, 110), border=2, shadow=PROP)
    piece(c, Circ(110, 250, 22), (80, 90, 80), border=1.5, shadow=None)
    piece(c, RRect(190, 220, 280, 290, 4), (160, 120, 80), border=2, shadow=PROP)
    # 1 dormitory bunks
    for x in (330, 450):
        piece(c, [RRect(x, 200, x + 110, 210, 2), RRect(x, 250, x + 110, 260, 2), RRect(x, 190, x + 6, 290, 1), RRect(x + 104, 190, x + 110, 290, 1)],
              (110, 110, 120), shadow=PROP)
        bl = (90, 150, 210) if (x == 450 and "blanket" in d) else (200, 80, 80)
        flat(c, [RRect(x + 8, 192, x + 102, 202, 3), RRect(x + 8, 242, x + 102, 252, 3)], bl)
    # 2 hydroponics
    plants = range(6) if "plants" not in d else range(5)
    for k in plants:
        x = 620 + k * 40
        piece(c, RRect(x, 270, x + 30, 290, 3), (140, 100, 80), shadow=SMALL)
        piece(c, [Circ(x + 15, 258, 12), Circ(x + 7, 264, 8), Circ(x + 23, 264, 8)], (90, 170, 90), shadow=SMALL)
    # 3 storage shelves with cans
    for row, y in enumerate((350, 390, 430)):
        flat(c, Thick(60, y, 280, y, 4), (120, 110, 100))
        n = 8 if not (row == 1 and "cans" in d) else 5
        for k in range(n):
            piece(c, RRect(66 + k * 26, y - 22, 84 + k * 26, y - 2, 3), [(220, 80, 70), (90, 140, 210), (240, 200, 80)][(k + row) % 3], shadow=SMALL)
    # 4 control room (screens are elements), desk
    piece(c, RRect(330, 400, 570, 430, 3), (120, 120, 130), border=2, shadow=PROP)
    # 5 water tank
    piece(c, RRect(640, 330, 720, 430, 12), (120, 160, 190), border=2, shadow=PROP)
    pipe(c, [(720, 360), (780, 360), (780, 430)], 8, (150, 150, 160))
    # 6 / 7 lower floor: mess hall + workshop
    piece(c, [RRect(80, 540, 300, 552, 2), RRect(96, 552, 104, 580, 1), RRect(276, 552, 284, 580, 1)], (160, 120, 80), border=2, shadow=PROP)
    piece(c, RRect(520, 520, 640, 580, 4), (130, 130, 140), border=2, shadow=PROP)
    piece(c, RRect(700, 500, 820, 580, 4), (160, 140, 90), border=2, shadow=PROP)
    # people
    person(c, 220, 300, (90, 120, 150))
    person(c, 400, 440, (150, 110, 80), hat=None if "hat" in d else (210, 190, 60))
    person(c, 200, 580, (110, 140, 100))
    person(c, 760, 580, (180, 110, 110))


def l31_fan(c, m):
    for k in range(4):
        a = math.radians(k * 90)
        flat(c, Poly([(110, 250), (110 + 20 * math.cos(a), 250 + 20 * math.sin(a)), (110 + 20 * math.cos(a + 0.7), 250 + 20 * math.sin(a + 0.7))]),
             (200, 205, 200))


def l31_screens(c, m):
    for k, x in enumerate((350, 420, 490)):
        col = (120, 255, 140) if not (m and k == 1) else (255, 170, 60)
        soft_union(c, [RRect(x, 350, x + 56, 390, 3)], col, 0.35, spread=8)
        piece(c, RRect(x, 350, x + 56, 390, 3), (30, 40, 40), border=2, border_col=(90, 90, 100), shadow=SMALL)
        for j in range(4):
            flat(c, Thick(x + 6, 360 + j * 8, x + 20 + (j * 13 + k * 7) % 30, 360 + j * 8, 2), col)


def l31_elevator(c, m):
    piece(c, RRect(448, 180, 478, 222, 3), (210, 190, 90), border=1.5, shadow=SMALL)
    flat(c, RRect(452, 186, 474, 210, 2), (255, 236, 160))


def l31_light(c, m):
    soft_union(c, [Circ(570, 180, 5)], (255, 80, 60), 0.8, spread=14)
    flat(c, Circ(570, 180, 5), (255, 120, 100))


L31_EL = [
    spin_el("fan", l31_fan, (110, 250), 300, speed_b=-300),
    E("screens", l31_screens, variant=True, daynight="untinted", anim=dict(twinkle=0.15, twinkleSpeed=2.0)),
    E("elevator", l31_elevator, pivot=(463, 200), anim=dict(bobAmplitude=(0, -180), bobSpeed=0.06, bounce=True)),
    E("alarm", l31_light, show="A", daynight="untinted", anim=dict(blinkInterval=1.0, blinkDuration=0.5)),
    E("uv", lambda c, m: soft_union(c, [RRect(612, 180, 852, 200, 4)], (240, 120, 255), 0.35, spread=18), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.5)),
] + smoke_el("steam", 230, 216, col=(230, 230, 232), r=6, length=34)
L31_DIFFS = [("fan", 110, 250, 30), ("screens", 448, 370, 0), ("alarm", 570, 180, 22), ("blanket", 505, 220, 0), ("cans", 200, 380, 0),
             ("hatch", 475, SURF - 30, 0), ("hat", 401, 395, 0)]


# =================================================================== 32 wasteland road (side, heat / dust)
STEPS32 = [(HEAT, 12), (CLEAR, 6), (FOG, 10), (CLEAR, 6)]
G32 = (440, [(6, 0.01, 0.4), (3, 0.03, 1.0)])


def l32_bg(c, d):
    sky(c, (250, 196, 130), (255, 232, 186))
    fill_levels.back_Level32(c, d)
    sun_bg(c, 150, 110, 40, col=(255, 236, 170))
    layer(c, 330, [(0, 0, 0)], (214, 150, 100))
    for x0, x1, top, col in ((-40, 230, 230, (190, 110, 70)), (520, 760, 250, (176, 96, 64)), (780, 960, 280, (196, 120, 80))):
        piece(c, Poly([(x0, 340), (x0 + 30, top), (x1 - 30, top), (x1, 340)]), col, shadow=LAYER)
        for k in range(3):
            y = top + 20 + k * 24
            flat(c, Thick(x0 + 24 + k * 6, y, x1 - 24 - k * 6, y, 2), lit(col, 0.85))
    layer(c, *G32, (230, 186, 130))
    # road
    piece(c, Poly([(-10, 520), (910, 500), (910, 560), (-10, 580)]), (90, 86, 92), shadow=PROP)
    for x in range(0, 900, 80):
        flat(c, Thick(x, 548 - x * 0.022, x + 40, 547 - (x + 40) * 0.022, 3), (240, 210, 90))
    # gas station
    b = gy(*G32, 640) + 6
    piece(c, [RRect(560, b - 90, 720, b - 76, 2), RRect(570, b - 76, 578, b, 1), RRect(702, b - 76, 710, b, 1)], (220, 220, 210), border=2,
          shadow=PROP)
    house(c, 800, b, 120, 70, (226, 212, 186), (150, 80, 60), roof="flat", wins=2)
    piece(c, RRect(620, b - 46, 646, b, 4), (200, 60, 60), border=1.5, shadow=PROP)
    sign_col = (90, 160, 210) if "sign" in d else (250, 200, 70)
    piece(c, [Thick(520, b, 520, b - 120, 4), RRect(480, b - 150, 560, b - 116, 5)], sign_col, border=2, shadow=PROP)
    flat(c, [Thick(492, b - 134, 548, b - 134, 3)], lit(sign_col, 0.5))
    # windmill pump tower (blades are an element)
    piece(c, [Thick(330, gy(*G32, 330) + 6, 344, gy(*G32, 330) - 150, 3), Thick(370, gy(*G32, 370) + 6, 356, gy(*G32, 370) - 150, 3)],
          (120, 100, 90), shadow=PROP)
    # rusty car
    car = (90, 140, 170) if "car" in d else (180, 90, 60)
    cb = 520
    piece(c, [RRect(140, cb - 40, 290, cb - 10, 10), Poly([(170, cb - 40), (260, cb - 40), (240, cb - 64), (190, cb - 64)])], car, border=2,
          shadow=PROP)
    flat(c, [Circ(170, cb - 8, 14), Circ(260, cb - 8, 14)], (50, 45, 48))
    flat(c, [Poly([(196, cb - 60), (236, cb - 60), (250, cb - 42), (182, cb - 42)])], (150, 190, 200))
    # props
    cactus(c, 430, gy(*G32, 430) + 8, 1.0)
    if "cactus" not in d:
        cactus(c, 470, gy(*G32, 470) + 10, 0.7)
    for i, x in enumerate((740, 766)):
        barrel(c, x, 600, col=(60, 120, 180) if (i == 1 and "barrel" in d) else (200, 80, 60))
    tires = 3 if "tires" not in d else 2
    for k in range(tires):
        piece(c, Ell(90, 596 - k * 12, 26, 8), (50, 48, 52), border=1, shadow=SMALL)
    rock(c, 860, 600, 1.0, (170, 120, 90))
    fill_levels.front_Level32(c, d)


def l32_blades(c, m):
    for k in range(8):
        a = math.radians(k * 45)
        flat(c, Poly([(350, 280), (350 + 34 * math.cos(a), 280 + 34 * math.sin(a)), (350 + 34 * math.cos(a + 0.3), 280 + 34 * math.sin(a + 0.3))]),
             (210, 200, 190))
    piece(c, Circ(350, 280, 5), (110, 90, 80), shadow=None)


def l32_weed(c, m):
    for r in (14, 10, 6):
        c.ellipse_ring(0, 500, r, r, 1.6, (160, 120, 80))
    flat(c, [Thick(-14, 500, 14, 500, 1.2), Thick(0, 486, 0, 514, 1.2)], (150, 110, 70))


def l32_vulture(c, m):
    piece(c, [Poly([(700, 110), (676, 102), (688, 112)]), Poly([(700, 110), (724, 102), (712, 112)]), Ell(700, 112, 4, 5)], (60, 50, 50),
          shadow=None)


L32_EL = [
    sun_glare("glare", 150, 110, 240),
    spin_el("pump", l32_blades, (350, 280), -60, speed_b=60),
    E("weed", l32_weed, pivot=(0, 500), anim=dict(drift_across(-16, 16, 60), rotateSpeed=-260, bobAmplitude=(0, 14), bobSpeed=0.5, bounce=True)),
    E("vulture", l32_vulture, show="A", pivot=(700, 110), anim=dict(orbitRadius=(60, 22), orbitSpeed=0.08, orbitAlign=False, swingAngle=8, swingSpeed=0.3)),
    E("vulture2", lambda c, m: l32_vulture(c, m), pivot=(700, 110),
      anim=dict(orbitRadius=(80, 30), orbitSpeed=-0.06, phase=0.4)),
    E("sign_glow", lambda c, m: soft_union(c, [RRect(480, gy(*G32, 640) + 6 - 150, 560, gy(*G32, 640) + 6 - 116, 5)], (255, 230, 150), 0.3, spread=8),
      daynight="untinted", anim=dict(blinkInterval=2.6, blinkDuration=1.8)),
] + [heat_haze("haze%d" % i, y, phase=i * 0.3) for i, y in enumerate((360, 470))] + [
    fog_layer("dust1", 32, 260, 420, 0.5, 18, 1, col=(236, 200, 150)),
    fog_layer("dust2", 33, 420, 590, 0.55, 24, 1, col=(236, 200, 150)),
]
L32_DIFFS = [("car", 215, 480, 0), ("sign", 520, 300, 0), ("pump", 350, 280, 44), ("cactus", 470, 420, 0), ("barrel", 766, 585, 0),
             ("vulture", 700, 110, 80), ("tires", 90, 572, 0)]


# =================================================================== 33 quarantine zone (top-down)
STEPS33 = [(OVERCAST, 8), (RAIN, 12), (FOG, 8), (OVERCAST, 6)]


def l33_bg(c, d):
    c.rect(0, 0, W, 660, (120, 130, 105))
    rnd = random.Random(33)
    for _ in range(120):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1, 3)), (105, 115, 92))
    # roads
    piece(c, RRect(-10, 260, 910, 330, 0), (90, 90, 95), shadow=SMALL)
    piece(c, RRect(400, -10, 470, 610, 0), (90, 90, 95), shadow=SMALL)
    for x in range(0, 900, 50):
        flat(c, RRect(x, 293, x + 24, 297, 1), (230, 220, 120))
    # chain-link fence around the inner zone
    for (x0, y0, x1, y1) in ((480, 30, 880, 30), (880, 30, 880, 250), (480, 340, 880, 340), (880, 340, 880, 580)):
        flat(c, Thick(x0, y0, x1, y1, 3), (190, 190, 200))
        n = int(max(abs(x1 - x0), abs(y1 - y0)) / 20)
        for k in range(n + 1):
            t = k / max(1, n)
            piece(c, Circ(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 3), (150, 150, 160), shadow=(2, 3, 2, 0.4))
    # hazard stripes at the gate
    for k in range(8):
        flat(c, Poly([(480 + k * 12, 250), (488 + k * 12, 250), (480 + k * 12 + 8, 262), (472 + k * 12, 262)]), (240, 200, 40) if k % 2 else (40, 40, 40))
    # tents (top-down), containers
    for i, (x, y) in enumerate(((540, 80), (660, 80), (780, 80), (540, 170), (660, 170))):
        col = (200, 210, 220) if not (i == 3 and "tent" in d) else (220, 120, 110)
        piece(c, RRect(x - 40, y - 30, x + 40, y + 30, 3), col, border=1.5, shadow=(4, 6, 6, 0.4))
        flat(c, RRect(x - 40, y - 30, x + 40, y, 3), lit(col, 1.1))
        flat(c, Thick(x - 38, y, x + 38, y, 2), lit(col, 0.7))
        flat(c, Poly([(x - 8, y - 4), (x + 8, y - 4), (x + 8, y + 4), (x - 8, y + 4)]), (220, 60, 60))
        flat(c, [Thick(x - 6, y, x + 6, y, 2.4), Thick(x, y - 6, x, y + 6, 2.4)], (255, 255, 255))
    for i, (x, y) in enumerate(((560, 420), (560, 490), (700, 420))):
        col = (200, 90, 60) if not (i == 2 and "container" in d) else (60, 140, 90)
        piece(c, RRect(x - 50, y - 24, x + 50, y + 24, 2), col, border=1.5, shadow=(5, 8, 6, 0.45))
        for k in range(1, 8):
            flat(c, Thick(x - 50 + k * 12.5, y - 22, x - 50 + k * 12.5, y + 22, 1.5), lit(col, 0.8))
    # trucks
    trucks = [(150, 290, (220, 220, 210)), (300, 300, (110, 130, 90))]
    if "truck" in d:
        trucks = trucks[:1]
    for x, y, col in trucks:
        piece(c, [RRect(x - 40, y - 15, x + 20, y + 15, 3), RRect(x + 22, y - 13, x + 44, y + 13, 4)], col, border=1.5, shadow=(4, 6, 5, 0.45))
        flat(c, RRect(x + 28, y - 10, x + 36, y + 10, 2), (70, 90, 110))
    # guard tower (top view: square roof)
    piece(c, RRect(820, 290, 860, 330, 2), (130, 110, 90), border=2, shadow=(10, 14, 8, 0.45))
    # barrels and a warning sign
    for k, (x, y) in enumerate(((120, 420), (150, 440), (130, 470))):
        col = (240, 200, 40) if not (k == 2 and "barrel" in d) else (60, 120, 200)
        piece(c, Circ(x, y, 14), col, border=1.5, shadow=(3, 4, 4, 0.4))
        flat(c, Circ(x, y, 6), lit(col, 0.7))
    if "sign" not in d:
        piece(c, Poly([(300, 420), (330, 470), (270, 470)]), (240, 200, 40), border=2, shadow=(3, 4, 4, 0.4))
        flat(c, [Thick(300, 436, 300, 456, 3), Circ(300, 462, 2)], INK)
    # helipad
    c.ellipse_ring(160, 130, 60, 60, 4, (230, 230, 230))
    flat(c, [Thick(140, 105, 140, 155, 6), Thick(180, 105, 180, 155, 6), Thick(140, 130, 180, 130, 6)], (230, 230, 230))
    fill_levels.front_Level33(c, d)


def l33_beam(c, m):
    c.polygon([(840, 310), (640, 220), (660, 380)], (255, 250, 210, 0.22))
    flat(c, Circ(840, 310, 6), (255, 250, 200))


def l33_drone(c, m):
    piece(c, [RRect(372, 452, 388, 468, 3)] + [Circ(380 + sx * 12, 460 + sy * 12, 6) for sx in (-1, 1) for sy in (-1, 1)], (80, 85, 100),
          border=1, shadow=(12, 18, 4, 0.3))


L33_EL = [
    E("beam", l33_beam, pivot=(840, 310), daynight="untinted", anim=dict(swingAngle=25, swingSpeed=0.12), animB=dict(swingAngle=-25, swingSpeed=0.12)),
    E("drone", l33_drone, show="A", pivot=(380, 460), anim=dict(orbitRadius=(40, 30), orbitSpeed=0.1)),
    E("ambulance", lambda c, m: (piece(c, [RRect(0, 288, 70, 312, 4)], (250, 250, 250), border=1.5, shadow=(4, 6, 5, 0.45)),
                                 soft_union(c, [Circ(60, 300, 4)], (80, 140, 255), 0.8, spread=10)),
      anim=drift_across(0, 70, 50)),
] + splash_rings("ripple", [(200, 200, 8), (620, 300, 9), (430, 500, 8), (760, 380, 8), (250, 540, 9)]) + [
    rain_layer("rain", 33, 110, 10, 1.4, 0.7, 170, step=(24, 64)),
    fog_layer("fog1", 33, 60, 300, 0.5, 9, 1, col=(220, 224, 220)),
    fog_layer("fog2", 34, 300, 560, 0.55, 12, -1, col=(220, 224, 220)),
]
L33_DIFFS = [("tent", 540, 170, 0), ("container", 700, 420, 0), ("truck", 310, 300, 0), ("beam", 740, 300, 110), ("sign", 300, 448, 0),
             ("barrel", 130, 470, 0), ("drone", 404, 468, 74)]


# =================================================================== 34 laboratory (front cut-away)
def l34_bg(c, d):
    c.rect(0, 0, W, 660, (226, 236, 236))
    fill_levels.back_Level34(c, d)
    for x in range(0, 900, 60):
        flat(c, Thick(x, 0, x, 470, 1), (210, 222, 224))
    piece(c, RRect(-10, 470, 910, 610, 0), (190, 196, 204), shadow=(0, -3, 8, 0.3))
    for x in range(0, 900, 50):
        flat(c, Thick(x, 470, x - 20, 600, 1), (176, 182, 190))
    # windows / poster
    piece(c, RRect(60, 60, 240, 200, 4), (170, 210, 240), border=4, border_col=(250, 250, 250), shadow=PROP)
    poster = (250, 200, 120) if "poster" in d else (150, 210, 160)
    piece(c, RRect(300, 70, 380, 180, 2), poster, border=2, shadow=PROP)
    flat(c, [Circ(340, 110, 18), Thick(316, 150, 364, 150, 3), Thick(316, 164, 350, 164, 3)], lit(poster, 0.75))
    # benches
    for x0, x1 in ((40, 380), (480, 860)):
        piece(c, [RRect(x0, 380, x1, 396, 2), RRect(x0 + 10, 396, x0 + 22, 470, 1), RRect(x1 - 22, 396, x1 - 10, 470, 1)], (230, 232, 236),
              border=2, shadow=PROP)
        flat(c, RRect(x0 + 30, 410, x1 - 30, 460, 3), (205, 210, 216))
    # flasks (liquid colour differs on one)
    for i, (x, col) in enumerate(((90, (120, 220, 140)), (150, (240, 120, 160)), (210, (120, 180, 250)))):
        if i == 1 and "flask" in d:
            col = (250, 220, 90)
        piece(c, Poly([(x - 6, 330), (x + 6, 330), (x + 6, 346), (x + 20, 378), (x - 20, 378), (x - 6, 346)]), (235, 245, 250), border=1.5,
              shadow=SMALL)
        flat(c, Poly([(x - 14, 364), (x + 14, 364), (x + 19, 377), (x - 19, 377)]), col)
    # microscope (missing in B)
    if "microscope" not in d:
        piece(c, [RRect(290, 360, 340, 380, 3), Thick(306, 360, 306, 300, 6), Thick(306, 306, 330, 290, 8), Thick(330, 290, 336, 340, 5)],
              (60, 64, 80), border=1.5, shadow=PROP)
    # specimen tank
    spec = (250, 140, 90) if "specimen" in d else (120, 230, 170)
    piece(c, RRect(560, 220, 660, 380, 10), (170, 230, 230), border=3, border_col=(150, 160, 170), shadow=PROP)
    piece(c, [Ell(610, 300, 22, 30), Circ(610, 262, 14)], spec, shadow=None)
    flat(c, [Circ(604, 260, 3), Circ(616, 260, 3)], INK)
    # centrifuge housing (rotor is an element)
    piece(c, RRect(750, 384, 830, 440, 8), (210, 214, 222), border=2, shadow=PROP)
    flat(c, Ell(790, 400, 26, 12), (90, 96, 110))
    # computer
    piece(c, RRect(700, 280, 820, 360, 4), (60, 64, 80), border=2, shadow=PROP)
    piece(c, RRect(744, 360, 776, 380, 1), (90, 94, 110), shadow=None)
    # scientists
    person(c, 440, 470, (250, 250, 250), h=1.4)
    person(c, 690, 470, (250, 250, 250), h=1.3, hat=None)


def l34_screen(c, m):
    col = (255, 160, 80) if m else (100, 230, 255)
    soft_union(c, [RRect(708, 288, 812, 352, 3)], col, 0.3, spread=6)
    flat(c, RRect(708, 288, 812, 352, 3), (20, 30, 40))
    pts = [(712 + k * 10, 330 - 18 * math.sin(k * 0.8)) for k in range(10)]
    flat(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 2) for k in range(9)], col)


def l34_arm(c, m):
    piece(c, [Thick(520, 380, 520, 330, 10), Thick(520, 330, 470, 300, 8), Thick(470, 300, 460, 320, 5)], (240, 160, 60), border=1.5, shadow=PROP)
    flat(c, [Circ(520, 330, 6), Circ(470, 300, 5)], (90, 90, 100))


def l34_centrifuge(c, m):
    for k in range(6):
        a = math.radians(k * 60)
        piece(c, Circ(790 + 18 * math.cos(a), 400 + 8 * math.sin(a), 4), (200, 80, 120) if k % 2 else (80, 140, 220), shadow=None)


L34_EL = [
    E("screen", l34_screen, variant=True, daynight="untinted", anim=dict(twinkle=0.15, twinkleSpeed=1.5)),
    E("arm", l34_arm, pivot=(520, 380), anim=dict(swingAngle=18, swingSpeed=0.25), animB={}),
    spin_el("centrifuge", l34_centrifuge, (790, 400), 360, speed_b=-360),
] + bubbles_el("bubbles_a", 90, 366, n=3, r=3, length=50) + bubbles_el("bubbles_b", 150, 366, n=3, r=3, length=50) \
  + bubbles_el("bubbles_c", 210, 366, n=3, r=3, length=50) + bubbles_el("tank", 600, 360, n=4, r=4, length=120)
L34_DIFFS = [("flask", 150, 360, 0), ("screen", 760, 320, 0), ("arm", 495, 330, 50), ("centrifuge", 790, 400, 30), ("specimen", 610, 285, 0),
             ("microscope", 315, 335, 0), ("poster", 340, 125, 0)]


LEVELS = [
    ("Level29", "蒸汽工坊", l29_bg, L29_EL, L29_DIFFS, 140,
     opts(weather=dict(steps=[(CLEAR, 12), (FOG, 8), (OVERCAST, 6)], blend=3.0, tints={FOG: (0.95, 0.88, 0.78)}))),
    ("Level30", "星际港口", l30_bg, L30_EL, L30_DIFFS, 140, opts(day_night=DN30, anim_seconds=40.0, frames=80)),
    ("Level31", "地下避难所", l31_bg, L31_EL, L31_DIFFS, 140, opts()),
    ("Level32", "荒漠公路", l32_bg, L32_EL, L32_DIFFS, 140,
     opts(weather=dict(steps=STEPS32, blend=3.0, tints={FOG: (0.98, 0.86, 0.68)}), anim_seconds=34.0, frames=68)),
    ("Level33", "隔离区", l33_bg, L33_EL, L33_DIFFS, 140, opts(weather=dict(steps=STEPS33, blend=3.0), anim_seconds=34.0, frames=68)),
    ("Level34", "科研实验室", l34_bg, L34_EL, L34_DIFFS, 140, opts()),
]
