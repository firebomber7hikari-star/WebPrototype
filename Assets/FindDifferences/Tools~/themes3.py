# -*- coding: utf-8 -*-
"""Theme levels 41-46: lost temple, shipwreck (porthole view), pirate ship, desert oasis, western town, harbour pub."""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, HEAT, OVERCAST, RAIN, THUNDER, W, W_, lit, on
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts, wave_strip
from kit import (INK, LAYER, PROP, SMALL, animal, barrel, bird_el, bubble, bubbles_el, bush, cactus, cloud_bg, cloud_el, crate,
                 drift_across, fish, gy, house, lamp_post, layer, palm, person, rock, sign, sky, smoke_el, spin_el, sun_bg, tree_round)
from stylekit import celestial, day_night, flame, moon_element, star_field, sun_element, window_glow
from weather import WET, cloud, flash, fog_layer, heat_haze, lightning, rain_layer, splash_rings, sun_glare


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=36.0, frames=72)
    o.update(kw)
    return o


# =================================================================== 41 lost temple (side, day/night)
DN41 = day_night(40.0, tint=(0.30, 0.34, 0.58))
SUN41, MOON41 = celestial((450, 160), (420, 120), 40.0)
STONE41 = (176, 166, 136)


def l41_bg(c, d):
    sky(c, (150, 200, 220), (240, 236, 200))
    fill_levels.back_Level41(c, d)
    layer(c, 300, [(26, 0.01, 0.4), (10, 0.03, 1.2)], (90, 150, 110))
    # step pyramid
    steps = 6 if "steps" not in d else 5
    for k in range(steps):
        w = 360 - k * 50
        y = 470 - k * 40
        piece(c, RRect(450 - w / 2, y - 40, 450 + w / 2, y, 2), lit(STONE41, 1 - k * 0.03), border=1.5, shadow=PROP)
        for xx in range(int(450 - w / 2) + 10, int(450 + w / 2) - 10, 30):
            flat(c, Thick(xx, y - 38, xx, y - 2, 1), lit(STONE41, 0.85))
    top = 470 - steps * 40
    piece(c, RRect(400, top - 60, 500, top, 2), lit(STONE41, 0.95), border=1.5, shadow=PROP)
    flat(c, [RRect(434, top - 46, 466, top, 3)], (40, 34, 40))
    glyph = (90, 200, 160) if "glyph" in d else (230, 120, 60)
    flat(c, [RRect(410, top - 40, 424, top - 26, 2), RRect(476, top - 40, 490, top - 26, 2)], glyph)
    flat(c, RRect(430, 470 - 40 * 5, 470, 470, 0), lit(STONE41, 0.8))   # stairway
    for y in range(470 - 40 * 5, 470, 8):
        flat(c, Thick(430, y, 470, y, 1.2), lit(STONE41, 0.7))
    # vines on the pyramid
    for x in (300, 360, 560, 600):
        flat(c, [Thick(x, 300, x + 6, 440, 3)], (70, 140, 80))
        for k in range(4):
            flat(c, Ell(x + 3 + (k % 2) * 6, 320 + k * 30, 6, 3), (90, 170, 90))
    # stone head (eyes closed in B)
    piece(c, RRect(90, 360, 190, 480, 20), (150, 146, 130), border=2, shadow=PROP)
    if "head" in d:
        flat(c, [Thick(110, 400, 132, 400, 3), Thick(148, 400, 170, 400, 3)], INK)
    else:
        flat(c, [Ell(121, 400, 10, 6), Ell(159, 400, 10, 6)], (70, 64, 60))
    flat(c, [RRect(130, 410, 150, 440, 4), Thick(116, 456, 164, 456, 4)], lit((150, 146, 130), 0.8))
    # columns (one broken in B), jaguar statue (missing in B)
    for i, x in enumerate((680, 760, 840)):
        h = 160 if not (i == 1 and "column" in d) else 80
        piece(c, [RRect(x - 16, 480 - h, x + 16, 480, 2), RRect(x - 22, 480 - h - 10, x + 22, 480 - h, 2)], (190, 182, 160), shadow=PROP)
    if "jaguar" not in d:
        piece(c, [Ell(250, 456, 32, 14), Circ(282, 440, 12), RRect(226, 456, 236, 476, 3), RRect(266, 456, 276, 476, 3),
                  RRect(220, 476, 290, 484, 2)], (200, 180, 120), border=1.5, shadow=PROP)
    layer(c, 480, [(8, 0.015, 0.3), (4, 0.04, 1.0)], (70, 130, 80))
    for x in (40, 330, 580, 880):
        bush(c, x, 500, 1.2, (80, 150, 85))
    fill_levels.front_Level41(c, d)


def l41_disk(c, m):
    piece(c, Circ(450, 142, 26), (230, 190, 80), border=2, shadow=None)
    for k in range(8):
        a = math.radians(k * 45)
        flat(c, Thick(450 + 10 * math.cos(a), 142 + 10 * math.sin(a), 450 + 22 * math.cos(a), 142 + 22 * math.sin(a), 3), (200, 150, 60))
    flat(c, Circ(450, 142, 6), (180, 120, 50))


def l41_macaw(c, m):
    col = (60, 120, 230) if m else (230, 60, 50)
    piece(c, [Ell(650, 160, 14, 7), Poly([(636, 160), (610, 166), (636, 166)]), Poly([(648, 156), (640, 136), (660, 156)])], col, border=1.2, shadow=SMALL)
    flat(c, Poly([(664, 158), (672, 160), (664, 163)]), INK)


L41_EL = [
    star_field("stars", 41, 60, 260),
    moon_element("moon", (450, 160), MOON41),
    sun_element("sun", (450, 160), SUN41, r=24),
    E("disk", l41_disk, pivot=(450, 142), anim=dict(rotateSpeed=20), animB={}),
    E("macaw", l41_macaw, variant=True, pivot=(650, 160), anim=dict(orbitRadius=(60, 24), orbitSpeed=0.07, stretch=(0, 0.4), scaleSpeed=2.4)),
    E("door_glow", lambda c, m: soft_union(c, [RRect(434, 250 - 46, 466, 250, 3)], (255, 200, 110), 0.6, spread=20), daynight="night",
      anim=dict(twinkle=0.2, twinkleSpeed=0.8)),
] + flame("torch1", 392, 236, 1.0) + flame("torch2", 508, 236, 1.0) + [bird_el("bird", 250, 110, 9, speed=18)]
L41_DIFFS = [("steps", 450, 230, 0), ("glyph", 450, 240, 0), ("head", 140, 400, 0), ("column", 760, 360, 0), ("jaguar", 255, 460, 0),
             ("disk", 450, 142, 34), ("macaw", 670, 160, 92)]


# =================================================================== 42 shipwreck seen through a porthole (first person)
PORT = (450, 290, 230)


def l42_bg(c, d):
    sky(c, (60, 140, 180), (20, 60, 100))
    # light rays
    for x in (300, 420, 560):
        c.polygon([(x, -10), (x + 40, -10), (x + 120, 460), (x + 40, 460)], (220, 250, 255, 0.10))
    piece(c, Poly([(-20, 470), (200, 440), (500, 460), (920, 430), (920, 610), (-20, 610)]), (200, 180, 130), shadow=LAYER)
    # wrecked galleon (tilted)
    hull = [(250, 470), (290, 380), (640, 350), (700, 420), (660, 470)]
    piece(c, Poly(hull), (120, 86, 64), border=2, border_col=(90, 64, 50), shadow=PROP)
    for k in range(4):
        flat(c, Thick(270 + k * 10, 440 - k * 22, 680 - k * 6, 430 - k * 22, 2), (100, 70, 54))
    for x in (380, 450, 520, 590):
        flat(c, Circ(x, 420 - (x - 380) * 0.07, 7), (40, 30, 30))
    piece(c, [Thick(420, 370, 380, 200, 7), Thick(560, 362, 600, 240, 6)], (110, 80, 60), shadow=PROP)
    sail = (200, 120, 110) if "sail" in d else (220, 210, 180)
    piece(c, Poly([(392, 230), (452, 250), (420, 330), (380, 300)]), sail, border=1.5, shadow=SMALL)
    # treasure, anchor, octopus, seaweed
    cx, cy = 372, 468          # inside the porthole's view
    piece(c, RRect(cx - 26, cy - 22, cx + 26, cy, 3), (150, 92, 55), border=2, border_col=(230, 190, 90), shadow=SMALL)
    if "chest" in d:
        piece(c, RRect(cx - 28, cy - 32, cx + 28, cy - 20, 5), (165, 102, 62), border=2, border_col=(230, 190, 90), shadow=SMALL)
    else:
        piece(c, Poly([(cx - 26, cy - 22), (cx + 26, cy - 22), (cx + 30, cy - 44), (cx - 22, cy - 46)]), (165, 102, 62), border=2,
              border_col=(230, 190, 90), shadow=SMALL)
        for k in range(4):
            piece(c, Circ(cx - 14 + k * 9, cy - 24, 5), (250, 210, 70), shadow=None)
    if "anchor" not in d:
        piece(c, [Thick(470, 380, 470, 450, 5), Thick(450, 440, 490, 440, 4), Thick(450, 440, 446, 426, 4), Thick(490, 440, 494, 426, 4),
                  Circ(470, 376, 7)], (90, 96, 110), shadow=SMALL)
    octo = (120, 180, 230) if "octopus" in d else (220, 110, 160)
    piece(c, [Ell(600, 330, 20, 16)] + [Thick(590 + k * 7, 340, 580 + k * 10, 362, 4) for k in range(4)], octo, border=1.2, shadow=SMALL)
    flat(c, [Circ(594, 328, 2.4), Circ(606, 328, 2.4)], INK)


def l42_seaweed(x, h, col):
    def d(c, m):
        pts = [(x + 8 * math.sin(k * 0.8), 470 - k * h / 6) for k in range(7)]
        piece(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 6 - k * 0.6) for k in range(6)], col, shadow=SMALL)
    return d


def l42_frame(c, m):
    x, y, r = PORT
    wall = (120, 126, 136)
    shapes = [RRect(-10, -10, W + 10, y - r + 20, 0), RRect(-10, y + r - 20, W + 10, H + 10, 0), RRect(-10, -10, x - r + 20, H + 10, 0),
              RRect(x + r - 20, -10, W + 10, H + 10, 0)]
    flat(c, shapes, wall)
    # fill the corners between the circle and the square cut-out
    for a0 in range(0, 360, 4):
        a, b = math.radians(a0), math.radians(a0 + 4)
        flat(c, Poly([(x + r * math.cos(a), y + r * math.sin(a)), (x + (r + 90) * math.cos(a), y + (r + 90) * math.sin(a)),
                       (x + (r + 90) * math.cos(b), y + (r + 90) * math.sin(b)), (x + r * math.cos(b), y + r * math.sin(b))]), wall)
    c.ellipse_ring(x, y, r + 22, r + 22, 26, (190, 150, 80))
    c.ellipse_ring(x, y, r + 2, r + 2, 6, (120, 90, 50))
    bolts = 11 if on("bolts", m) else 12
    for k in range(bolts):
        a = math.radians(k * 30)
        flat(c, Circ(x + (r + 11) * math.cos(a), y + (r + 11) * math.sin(a), 5), (230, 200, 120))
    for yy in range(20, 600, 60):
        for xx in (20, 60, 840, 880):
            flat(c, Circ(xx, yy, 3), (90, 96, 106))
    # gauges
    for gx, gy_ in ((90, 120), (810, 120)):
        piece(c, Circ(gx, gy_, 34), (240, 236, 220), border=4, border_col=(190, 150, 80), shadow=PROP)
        for k in range(7):
            a = math.radians(150 + k * 40)
            flat(c, Thick(gx + 24 * math.cos(a), gy_ + 24 * math.sin(a), gx + 30 * math.cos(a), gy_ + 30 * math.sin(a), 2), INK)
    pipe_col = (170, 120, 70)
    piece(c, [Thick(0, 480, 120, 480, 12), Thick(120, 480, 120, 600, 12)], pipe_col, shadow=PROP)
    piece(c, [Thick(900, 470, 780, 470, 12), Thick(780, 470, 780, 600, 12)], pipe_col, shadow=PROP)
    fill_levels.frame_Level42(c, m)


def l42_needle(gx, gy_):
    def d(c, m):
        flat(c, [Thick(gx, gy_, gx + 20, gy_ - 16, 2.5), Circ(gx, gy_, 4)], (200, 50, 50))
    return d


L42_EL = [
    E("rays", lambda c, m: [c.polygon([(x, -10), (x + 30, -10), (x + 110, 460), (x + 50, 460)], (240, 255, 255, 0.10)) for x in (340, 500)],
      daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.2)),
    E("weed1", l42_seaweed(320, 120, (60, 150, 90)), pivot=(320, 470), anim=dict(swingAngle=8, swingSpeed=0.3)),
    E("weed2", l42_seaweed(560, 100, (80, 160, 100)), pivot=(560, 470), show="A", anim=dict(swingAngle=8, swingSpeed=0.25, phase=0.4)),
    E("fish1", lambda c, m: fish(c, 300, 200, 1.2, (250, 200, 80), fin=(250, 150, 60)), pivot=(300, 200), anim=drift_across(270, 320, 30)),
    E("fish2", lambda c, m: fish(c, 600, 260, 1.0, (120, 200, 240), right=False), pivot=(600, 260), anim=drift_across(570, 620, -24)),
] + bubbles_el("bub", 460, 300, n=4, r=4, length=160) + [
    E("frame", l42_frame, variant=True),
    E("needle1", l42_needle(90, 120), pivot=(90, 120), anim=dict(swingAngle=30, swingSpeed=0.4), animB={}),
    E("needle2", l42_needle(810, 120), pivot=(810, 120), anim=dict(swingAngle=6, swingSpeed=1.4)),
    E("lamp", lambda c, m: (soft_union(c, [Circ(450, 30, 10)], (255, 220, 140), 0.6, spread=20), flat(c, Circ(450, 30, 8), (255, 236, 170))),
      daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=1.2)),
]
L42_DIFFS = [("sail", 418, 280, 0), ("chest", 372, 450, 0), ("anchor", 470, 412, 0), ("octopus", 600, 340, 0), ("bolts", 659, 169, 0),
             ("needle", 96, 112, 34), ("seaweed", 560, 420, 0), ("chart", 90, 350, 0), ("plaque", 825, 230, 0)]


# =================================================================== 43 pirate ship (side, storm)
STEPS43 = [(CLEAR, 10), (OVERCAST, 6), (THUNDER, 10), (RAIN, 6)]
SEA43 = 430


def l43_bg(c, d):
    sky(c, (120, 180, 230), (230, 236, 240))
    fill_levels.back_Level43(c, d)
    piece(c, Poly([(700, SEA43), (760, 380), (830, 370), (900, SEA43)]), (200, 180, 120), shadow=SMALL)
    if "island" not in d:
        palm(c, 790, 378, 70, 10)
    c.rect(0, SEA43 - 10, W, 660, (50, 110, 160))
    fill_levels.front_Level43(c, d)


def l43_ship(c, m):
    hull = [(160, 400), (680, 400), (640, 470), (210, 470)]
    piece(c, [Poly(hull), Poly([(600, 400), (690, 380), (680, 400)]), RRect(160, 360, 260, 402, 3)], (120, 76, 50), border=2, shadow=PROP)
    flat(c, Thick(170, 420, 660, 420, 4), (230, 190, 90))
    ports = 4 if on("ports", m) else 5
    for k in range(ports):
        flat(c, RRect(260 + k * 70, 432, 282 + k * 70, 448, 2), (40, 30, 30))
    for x, h in ((300, 260), (440, 300), (580, 240)):
        piece(c, Thick(x, 400, x, 400 - h, 7), (100, 70, 50), shadow=SMALL)
    for x, h in ((300, 260), (440, 300), (580, 240)):
        for k in range(2):
            y0 = 400 - h + 30 + k * (h - 60) / 2
            piece(c, Poly([(x - 56 + k * 6, y0), (x + 56 - k * 6, y0), (x + 50 - k * 6, y0 + (h - 80) / 2), (x - 50 + k * 6, y0 + (h - 80) / 2)]),
                  (240, 232, 206), border=1.5, shadow=SMALL)
    patch = (200, 70, 70) if on("patch", m) else (210, 190, 150)
    flat(c, RRect(420, 210, 446, 236, 2), patch)
    if not on("lookout", m):
        piece(c, [RRect(424, 108, 456, 120, 3)], (110, 80, 60), shadow=SMALL)
        person(c, 440, 108, (200, 60, 60), h=0.6)
    piece(c, Poly([(680, 400), (720, 372), (712, 392)]), (230, 190, 90), shadow=SMALL)


def l43_flag(c, m):
    piece(c, Poly([(441, 102), (486, 110), (441, 130)]), (30, 30, 36), border=1.2, shadow=SMALL)
    bones = (230, 60, 60) if m else (250, 250, 250)
    flat(c, [Circ(458, 114, 5), Thick(450, 122, 466, 108, 2), Thick(450, 108, 466, 122, 2)], bones)


def l43_waves(top, amp, period, col, dx):
    def d(c, m):
        piece(c, wave_strip(top, amp, period, 0.2, x0=-100, x1=1000, bottom=660), col, border=2, shadow=(1, 3, 8, 0.3))
    return E("wave%d" % top, d, anim=dict(bobAmplitude=(dx, 0), bobSpeed=0.1))


def l43_tentacle(c, m):
    pts = [(780 + 20 * math.sin(k * 0.7), 520 - k * 22) for k in range(8)]
    piece(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 18 - k * 2) for k in range(7)], (140, 80, 140), shadow=PROP)
    for k in range(1, 6):
        flat(c, Circ(pts[k][0] + 4, pts[k][1], 3), (220, 170, 210))


SHIP_ANIM = dict(swingAngle=3, swingSpeed=0.18, bobAmplitude=(0, 6), bobSpeed=0.18)
L43_EL = [
    cloud_el("cloud_w", 200, 80, 0.8, 7, weather=W_(CLEAR)),
    cloud("cloud_g1", 160, 60, 1.4, (150, 156, 172), W_(OVERCAST, RAIN, THUNDER)),
    cloud("cloud_g2", 480, 40, 1.6, (150, 156, 172), W_(OVERCAST, RAIN, THUNDER)),
    cloud("cloud_g3", 800, 70, 1.4, (150, 156, 172), W_(OVERCAST, RAIN, THUNDER)),
    lightning("bolt", 760, 110, SEA43 - 10, interval=4.4, phase=0.2, seed=43),
    l43_waves(SEA43 + 10, 10, 60, (70, 130, 180), 16),
    E("ship", l43_ship, variant=True, pivot=(420, 460), anim=SHIP_ANIM),
    E("flag", l43_flag, variant=True, pivot=(441, 116), anim=dict(SHIP_ANIM, stretch=(0.2, 0), scaleSpeed=1.4)),
    E("tentacle", l43_tentacle, show="A", pivot=(780, 520), anim=dict(swingAngle=10, swingSpeed=0.3, bobAmplitude=(0, 20), bobSpeed=0.15)),
] + smoke_el("cannon", 200, 440, n=3, col=(230, 230, 230), r=12, rise=(-30, 8), length=70, show="A") + [
    l43_waves(SEA43 + 50, 13, 80, (55, 110, 165), -18),
    bird_el("gull", 600, 140, 10, speed=20, weather=W_(CLEAR, OVERCAST)),
] + splash_rings("ripple", [(100, 540, 12), (400, 560, 12), (700, 530, 11)]) + [
    rain_layer("rain", 43, 90, 28, 1.4, 0.7, 280),
    flash("flash", 4.4, 0.2),
]
L43_DIFFS = [("ports", 535, 440, 0), ("patch", 433, 223, 0), ("lookout", 440, 92, 0), ("flag", 462, 116, 0), ("tentacle", 780, 440, 90),
             ("cannon", 176, 430, 50), ("island", 790, 340, 0)]


# =================================================================== 44 desert oasis (side, day/night + heat / sandstorm)
DN44 = day_night(40.0, tint=(0.32, 0.32, 0.58))
SUN44, MOON44 = celestial((450, 160), (420, 120), 40.0)
STEPS44 = [(HEAT, 14), (CLEAR, 10), (FOG, 8)]


def l44_bg(c, d):
    sky(c, (240, 190, 120), (255, 232, 180))
    fill_levels.back_Level44(c, d)
    for top, col in ((300, (236, 190, 120)), (360, (226, 170, 100)), (430, (240, 196, 124))):
        layer(c, top, [(24, 0.007, top * 0.02), (10, 0.02, 1.0)], col)
        if top == 300:
            for x, s in ((140, 1.0), (240, 0.7)):
                b = gy(300, [(24, 0.007, 6.0), (10, 0.02, 1.0)], x) + 10
                piece(c, Poly([(x - 70 * s, b), (x, b - 70 * s), (x + 70 * s, b)]), (220, 180, 120), shadow=SMALL)
                flat(c, Poly([(x, b - 70 * s), (x + 70 * s, b), (x + 10 * s, b)]), (196, 156, 100))
                if x == 140 and "capstone" not in d:
                    flat(c, Poly([(x - 10 * s, b - 60 * s), (x, b - 70 * s), (x + 10 * s, b - 60 * s)]), (250, 210, 80))
    # oasis
    piece(c, Ell(560, 470, 130, 22), (90, 170, 200), border=3, border_col=(210, 190, 140), shadow=SMALL)
    for x, lean in ((470, -16), (650, 18)):
        palm(c, x, 470, 150, lean)
    if "coconut" not in d:
        for k in range(3):
            piece(c, Circ(668 + k * 8, 330 + (k % 2) * 6, 6), (130, 90, 50), shadow=None)
    # tents
    tent = (90, 140, 200) if "tent" in d else (200, 80, 70)
    for x, col in ((200, tent), (320, (230, 220, 190))):
        piece(c, Poly([(x - 60, 500), (x, 430), (x + 60, 500)]), col, border=2, shadow=PROP)
        flat(c, Poly([(x - 10, 500), (x, 470), (x + 10, 500)]), lit(col, 0.6))
    # well with bucket, water jugs
    piece(c, [RRect(760, 470, 820, 500, 4)], (190, 170, 140), border=2, shadow=PROP)
    piece(c, [Thick(764, 470, 764, 420, 3), Thick(816, 470, 816, 420, 3), Thick(760, 420, 820, 420, 3)], (140, 100, 70), shadow=SMALL)
    if "bucket" not in d:
        piece(c, [Thick(790, 420, 790, 440, 1.2), RRect(782, 440, 798, 454, 2)], (120, 110, 100), shadow=SMALL)
    jugs = 3 if "jugs" not in d else 2
    for k in range(jugs):
        piece(c, [Ell(390 + k * 22, 502, 9, 11), RRect(386 + k * 22, 486, 394 + k * 22, 494, 2)], (200, 120, 80), border=1.2, shadow=SMALL)
    fill_levels.front_Level44(c, d)


def l44_camels(c, m):
    for k in range(3):
        x = 120 + k * 90
        b = 300
        piece(c, [Ell(x, b - 24, 26, 12), Circ(x - 6, b - 36, 9), Thick(x + 20, b - 26, x + 34, b - 44, 6), Circ(x + 36, b - 46, 5),
                  Thick(x - 16, b - 14, x - 18, b, 3), Thick(x + 14, b - 14, x + 16, b, 3)], (190, 150, 100), shadow=SMALL)
        flat(c, RRect(x - 14, b - 40, x + 4, b - 30, 2), (200, 60, 60))


def l44_fish(c, m):
    piece(c, [Ell(560, 466, 10, 5), Poly([(552, 466), (544, 460), (544, 472)])], (250, 160, 60), border=1, shadow=None)


L44_EL = [
    star_field("stars", 44, 70, 260),
    moon_element("moon", (450, 160), MOON44),
    sun_element("sun", (450, 160), SUN44, r=26),
    sun_glare("glare", 450, 40, 220),
    E("camels", l44_camels, pivot=(210, 300), anim=drift_across(90, 380, 10)),
    E("fish", l44_fish, show="A", pivot=(560, 466), anim=dict(bobAmplitude=(10, 36), bobSpeed=0.25, bounce=True, rotateSpeed=-120)),
    E("flag", lambda c, m: (flat(c, Thick(320, 430, 320, 404, 2), INK), piece(c, Poly([(321, 404), (344, 410), (321, 416)]), (60, 150, 90), shadow=SMALL)),
      pivot=(321, 410), anim=dict(stretch=(0.25, 0), scaleSpeed=1.5, swingAngle=4, swingSpeed=1.0), animB={}),
    E("lantern", lambda c, m: soft_union(c, [Circ(260, 470, 10)], (255, 200, 110), 0.6, spread=26), daynight="night",
      anim=dict(twinkle=0.2, twinkleSpeed=1.2)),
] + [heat_haze("haze%d" % i, y, phase=i * 0.3) for i, y in enumerate((330, 440))] + [
    fog_layer("sand1", 44, 240, 400, 0.55, 20, 1, col=(236, 200, 150)),
    fog_layer("sand2", 45, 400, 580, 0.6, 26, 1, col=(236, 200, 150)),
]
L44_DIFFS = [("tent", 200, 470, 0), ("coconut", 676, 334, 0), ("capstone", 140, 236, 0), ("bucket", 790, 440, 0), ("jugs", 434, 498, 0),
             ("fish", 565, 445, 44), ("flag", 332, 412, 26)]


# =================================================================== 45 western town (side, day/night)
DN45 = day_night(40.0, tint=(0.36, 0.30, 0.52))
SUN45, MOON45 = celestial((450, 150), (420, 110), 40.0)
WOOD = (176, 120, 80)


def l45_bg(c, d):
    sky(c, (130, 186, 236), (250, 220, 170))
    fill_levels.back_Level45(c, d)
    piece(c, Poly([(-20, 330), (100, 260), (180, 270), (260, 330)]), (196, 120, 80), shadow=LAYER)
    piece(c, Poly([(620, 330), (700, 250), (820, 260), (920, 330)]), (186, 110, 76), shadow=LAYER)
    layer(c, 330, [(0, 0, 0)], (226, 186, 130))
    # buildings with false fronts
    fronts = [(30, 200, 210, (190, 130, 90), "SALOON"), (220, 360, 180, (160, 120, 100), "SHERIFF"), (380, 520, 190, (200, 170, 120), "BANK"),
              (540, 700, 170, (170, 110, 80), "STORE")]
    for i, (x0, x1, h, col, _) in enumerate(fronts):
        top = 470 - h
        piece(c, Poly([(x0, 470), (x0, top + 20), (x0 + 20, top), (x1 - 20, top), (x1, top + 20), (x1, 470)]), col, border=2, shadow=PROP)
        for y in range(top + 20, 470, 12):
            flat(c, Thick(x0 + 2, y, x1 - 2, y, 1), lit(col, 0.88))
        sign_col = (60, 140, 90) if (i == 0 and "sign" in d) else (240, 220, 160)
        piece(c, RRect(x0 + 20, top + 10, x1 - 20, top + 36, 3), sign_col, border=1.5, shadow=SMALL)
        flat(c, [Thick(x0 + 34, top + 23, x1 - 34, top + 23, 3)], (90, 60, 50))
        flat(c, [RRect(x0 + 18, top + 60, x0 + 50, top + 96, 2), RRect(x1 - 50, top + 60, x1 - 18, top + 96, 2)], (255, 222, 150))
        piece(c, RRect(x0 - 6, 400, x1 + 6, 410, 1), lit(col, 0.7), shadow=SMALL)
        for x in (x0, x1):
            flat(c, Thick(x, 410, x, 470, 3), lit(col, 0.6))
    if "poster" not in d:
        piece(c, RRect(300, 420, 326, 452, 1), (240, 226, 190), border=1, shadow=SMALL)
        flat(c, [Circ(313, 432, 6), Thick(304, 446, 322, 446, 2)], (120, 90, 70))
    # water tower, windmill pump
    tower = (90, 140, 190) if "tower" in d else (170, 110, 80)
    piece(c, [Thick(740, 470, 750, 300, 4), Thick(810, 470, 800, 300, 4), RRect(730, 240, 820, 300, 6)], tower, border=2, shadow=PROP)
    flat(c, [Thick(732, 256, 818, 256, 2), Thick(732, 284, 818, 284, 2)], lit(tower, 0.7))
    piece(c, [Thick(860, 470, 868, 300, 3), Thick(890, 470, 882, 300, 3)], (120, 100, 90), shadow=PROP)
    # street, horse, barrels, cactus
    piece(c, RRect(-10, 470, 910, 610, 0), (214, 170, 116), shadow=LAYER)
    horse = (60, 50, 50) if "horse" in d else (150, 90, 60)
    piece(c, [Ell(640, 520, 40, 20), Thick(670, 512, 690, 486, 12), Ell(698, 482, 14, 9), RRect(608, 530, 616, 562, 3), RRect(664, 530, 672, 562, 3)],
          horse, border=1.5, shadow=PROP)
    flat(c, Thick(560, 520, 600, 520, 3), WOOD)
    barrels = 3 if "barrels" not in d else 2
    for k in range(barrels):
        barrel(c, 120 + k * 28, 560)
    cactus(c, 470, 570, 0.8)
    fill_levels.front_Level45(c, d)


def l45_doors(c, m):
    flat(c, [RRect(96, 430, 114, 460, 1), RRect(116, 430, 134, 460, 1)], (150, 100, 60))


def l45_pump(c, m):
    for k in range(10):
        a = math.radians(k * 36)
        flat(c, Poly([(875, 300), (875 + 30 * math.cos(a), 300 + 30 * math.sin(a)), (875 + 30 * math.cos(a + 0.3), 300 + 30 * math.sin(a + 0.3))]),
             (220, 210, 200))


def l45_weed(c, m):
    for r in (14, 10, 6):
        c.ellipse_ring(0, 560, r, r, 1.6, (160, 120, 80))


def l45_tail(c, m):
    flat(c, [Thick(600, 512, 590, 540, 5)], (60, 40, 40))


L45_EL = [
    star_field("stars", 45, 60, 250),
    moon_element("moon", (450, 150), MOON45),
    sun_element("sun", (450, 150), SUN45, r=26),
    E("doors", l45_doors, pivot=(115, 430), anim=dict(stretch=(0.3, 0), scaleSpeed=0.6), animB={}),
    spin_el("pump", l45_pump, (875, 300), -70, speed_b=70),
    E("weed", l45_weed, pivot=(0, 560), anim=dict(drift_across(-16, 16, 50), rotateSpeed=-220, bobAmplitude=(0, 12), bobSpeed=0.5, bounce=True)),
    E("tail", l45_tail, pivot=(600, 512), anim=dict(swingAngle=14, swingSpeed=0.5)),
    window_glow("windows", [(48, 320, 80, 356), (150, 320, 182, 356), (238, 350, 270, 386), (398, 340, 430, 376), (558, 360, 590, 396)]),
] + flame("lamp1", 210, 400, 0.8)
L45_DIFFS = [("sign", 115, 283, 0), ("poster", 313, 436, 0), ("tower", 775, 270, 0), ("horse", 650, 515, 0), ("barrels", 176, 545, 0),
             ("doors", 115, 445, 30), ("pump", 875, 300, 40)]


# =================================================================== 46 harbour pub (interior)
DN46 = day_night(40.0, tint=(0.40, 0.36, 0.50))


def l46_bg(c, d):
    c.rect(0, 0, W, 660, (150, 200, 230))
    wall = (170, 120, 80)
    shapes = [RRect(-10, -10, W + 10, 120, 0), RRect(-10, 220, W + 10, 610, 0), RRect(-10, 120, 140, 220, 0), RRect(240, 120, 660, 220, 0),
              RRect(760, 120, W + 10, 220, 0)]
    flat(c, shapes, wall)
    for x in range(0, 900, 36):
        flat(c, Thick(x, 0, x, 470, 1.4), lit(wall, 0.88))
    for cx in (190, 710):
        c.ellipse_ring(cx, 170, 58, 58, 10, (200, 170, 90))
        # cover square corners of the window opening
        for a0 in range(0, 360, 6):
            a, b = math.radians(a0), math.radians(a0 + 6)
            flat(c, Poly([(cx + 50 * math.cos(a), 170 + 50 * math.sin(a)), (cx + 75 * math.cos(a), 170 + 75 * math.sin(a)),
                          (cx + 75 * math.cos(b), 170 + 75 * math.sin(b)), (cx + 50 * math.cos(b), 170 + 50 * math.sin(b))]), wall)
        c.ellipse_ring(cx, 170, 58, 58, 10, (200, 170, 90))
        c.ellipse(cx, 190, 50, 8, (80, 140, 190, 0.8))
    # ship wheel (static), lifebuoy, swordfish, anchor
    piece(c, Circ(450, 160, 44), (150, 100, 60), border=0, shadow=PROP)
    flat(c, Circ(450, 160, 34), wall)
    for k in range(8):
        a = math.radians(k * 45)
        piece(c, Thick(450 + 10 * math.cos(a), 160 + 10 * math.sin(a), 450 + 56 * math.cos(a), 160 + 56 * math.sin(a), 5), (150, 100, 60), shadow=None)
    flat(c, Circ(450, 160, 10), (150, 100, 60))
    buoy = (60, 140, 210) if "buoy" in d else (230, 70, 60)
    piece(c, Circ(330, 170, 28), buoy, border=1.5, shadow=PROP)
    flat(c, Circ(330, 170, 14), wall)
    for k in range(4):
        a = math.radians(45 + k * 90)
        flat(c, Thick(330 + 15 * math.cos(a), 170 + 15 * math.sin(a), 330 + 27 * math.cos(a), 170 + 27 * math.sin(a), 6), (250, 250, 250))
    if "swordfish" not in d:
        piece(c, [Ell(570, 160, 50, 14), Thick(520, 160, 470 + 50, 160, 1), Poly([(616, 160), (640, 144), (640, 176)]),
                  Thick(520, 158, 486, 156, 3)], (90, 120, 170), border=1.5, shadow=PROP)
    if "anchor" not in d:
        piece(c, [Thick(830, 250, 830, 320, 5), Thick(810, 310, 850, 310, 4), Circ(830, 246, 7)], (90, 96, 110), shadow=PROP)
    # bar counter + shelves
    piece(c, RRect(560, 380, 900, 480, 3), (130, 86, 56), border=2, shadow=PROP)
    piece(c, RRect(550, 370, 910, 386, 3), (160, 110, 70), shadow=PROP)
    flat(c, Thick(580, 300, 880, 300, 4), (120, 80, 54))
    for k in range(8):
        piece(c, [RRect(590 + k * 36, 266, 604 + k * 36, 298, 3), RRect(594 + k * 36, 256, 600 + k * 36, 268, 1)],
              [(90, 150, 90), (160, 90, 60), (200, 180, 90)][k % 3], shadow=SMALL)
    # ship in a bottle (sail colour differs)
    piece(c, Ell(250, 360, 40, 16), (200, 230, 230), border=1.5, shadow=PROP)
    sail = (230, 90, 80) if "bottle" in d else (250, 250, 240)
    flat(c, [Poly([(236, 366), (264, 366), (258, 372), (242, 372)]), Poly([(250, 364), (250, 346), (262, 362)])], sail)
    # tables and patrons
    for x in (140, 360):
        piece(c, [RRect(x - 60, 440, x + 60, 452, 2), RRect(x - 6, 452, x + 6, 520, 1)], (150, 100, 66), border=1.5, shadow=PROP)
    person(c, 90, 520, (60, 90, 140), h=1.3, hat=None if "hat" in d else (40, 50, 80))
    person(c, 410, 520, (200, 200, 200), h=1.3)
    piece(c, RRect(-10, 520, 910, 610, 0), (120, 82, 54), shadow=(0, -3, 8, 0.3))
    fill_levels.front_Level46(c, d)


def l46_lantern(c, m):
    flat(c, Thick(600, 0, 600, 60, 1.5), INK)
    piece(c, RRect(588, 60, 612, 92, 4), (200, 160, 80), border=1.5, shadow=SMALL)
    flat(c, RRect(592, 66, 608, 86, 3), (255, 230, 150))


def l46_tank(c, m):
    piece(c, RRect(680, 320, 780, 370, 4), (170, 220, 230, 0.8), border=2, shadow=None)


def l46_fish(c, m):
    fish(c, 730, 345, 0.7, (250, 150, 60))


def l46_parrot(c, m):
    piece(c, [Ell(520, 330, 10, 16), Circ(522, 312, 8), Thick(500, 348, 540, 348, 3)], (60, 170, 90), border=1.2, shadow=SMALL)
    flat(c, Poly([(528, 312), (536, 316), (528, 320)]), (250, 200, 60))


L46_EL = [
    E("sea", lambda c, m: [c.ellipse(cx, 180, 46, 6, (60, 120, 170, 0.6)) for cx in (190, 710)], anim=dict(bobAmplitude=(0, 3), bobSpeed=0.3)),
    E("lantern", l46_lantern, pivot=(600, 0), anim=dict(swingAngle=10, swingSpeed=0.3), animB={}),
    E("lantern_glow", lambda c, m: soft_union(c, [Circ(600, 76, 12)], (255, 210, 130), 0.55, spread=36), daynight="night"),
    E("tank", l46_tank),
    E("fish", l46_fish, pivot=(730, 345), anim=dict(orbitRadius=(30, 6), orbitSpeed=0.12, orbitAlign=True),
      animB=dict(orbitRadius=(30, 6), orbitSpeed=-0.12, orbitAlign=True)),
    E("parrot", l46_parrot, pivot=(520, 348), anim=dict(swingAngle=6, swingSpeed=0.4)),
] + flame("candle1", 140, 438, 0.7) + flame("candle2", 360, 438, 0.7)
L46_DIFFS = [("buoy", 330, 170, 0), ("swordfish", 560, 160, 0), ("anchor", 830, 285, 0), ("bottle", 250, 360, 0), ("hat", 92, 452, 0),
             ("lantern", 600, 76, 34), ("fish", 730, 345, 40)]


LEVELS = [
    ("Level41", "失落神殿", l41_bg, L41_EL, L41_DIFFS, 140, opts(day_night=DN41, anim_seconds=40.0, frames=80)),
    ("Level42", "沉船", l42_bg, L42_EL, L42_DIFFS, 140, opts()),
    ("Level43", "海盗船", l43_bg, L43_EL, L43_DIFFS, 140,
     opts(weather=dict(steps=STEPS43, blend=3.0), anim_seconds=32.0, frames=64)),
    ("Level44", "沙漠绿洲", l44_bg, L44_EL, L44_DIFFS, 140,
     opts(day_night=DN44, weather=dict(steps=STEPS44, blend=3.0, tints={FOG: (0.98, 0.86, 0.68)}), anim_seconds=40.0, frames=80)),
    ("Level45", "西部小镇", l45_bg, L45_EL, L45_DIFFS, 140, opts(day_night=DN45, anim_seconds=40.0, frames=80)),
    ("Level46", "港口酒馆", l46_bg, L46_EL, L46_DIFFS, 140, opts(day_night=DN46, anim_seconds=40.0, frames=80)),
]
