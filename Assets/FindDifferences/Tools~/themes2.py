# -*- coding: utf-8 -*-
"""Theme levels 35-40: flooded city, rainforest, polar, volcano, deep sea, underground ruins."""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, SNOW, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts, wave_strip
from kit import (INK, LAYER, PROP, SMALL, animal, barrel, bird_el, bubble, bubbles_el, bush, cloud_bg, cloud_el, crate, crystal,
                 dead_tree, drift_across, fish, glow_el, gy, house, layer, palm, person, rock, sky, smoke_el, spin_el, sun_bg,
                 tree_pine, tree_round)
from stylekit import celestial, day_night, flame, moon_element, star_field, sun_element
from weather import WET, cloud, fog_layer, rain_layer, snow_layer, splash_rings


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=36.0, frames=72)
    o.update(kw)
    return o


# =================================================================== 35 flooded city (side, rain)
WATER = 390
STEPS35 = [(OVERCAST, 8), (RAIN, 14), (CLEAR, 8)]


def l35_bg(c, d):
    sky(c, (150, 170, 196), (214, 222, 230))
    rnd = random.Random(35)
    x = -10
    while x < 920:
        w, h = rnd.randint(40, 70), rnd.randint(100, 220)
        piece(c, RRect(x, WATER - h, x + w, WATER + 40, 1), (150, 160, 180), shadow=None)
        x += w + rnd.randint(4, 12)
    # front buildings standing in the water
    blds = [(60, 170, 150, (200, 190, 176)), (200, 300, 230, (176, 186, 200)), (330, 450, 120, (210, 180, 160)), (500, 610, 260, (190, 196, 210)),
            (650, 760, 170, (214, 200, 176)), (790, 900, 210, (186, 176, 190))]
    for i, (x0, x1, h, col) in enumerate(blds):
        top = WATER - h
        piece(c, RRect(x0, top, x1, WATER + 120, 2), col, border=2, shadow=PROP)
        for y in range(top + 16, WATER - 10, 30):
            for xx in range(x0 + 10, x1 - 16, 26):
                lit_win = (i == 3 and y == top + 46 and xx == x0 + 36 and "window" in d)
                flat(c, RRect(xx, y, xx + 14, y + 18, 2), (255, 222, 140) if lit_win else (110, 130, 160))
    # rooftop details
    if "antenna" not in d:
        piece(c, [Thick(555, WATER - 260, 555, WATER - 320, 3), Thick(540, WATER - 300, 570, WATER - 300, 2)], (90, 90, 100), shadow=SMALL)
    banner = (90, 160, 220) if "banner" in d else (240, 240, 235)
    piece(c, RRect(214, WATER - 250, 290, WATER - 230, 2), banner, border=1.5, shadow=SMALL)
    flat(c, [Thick(222, WATER - 240, 282, WATER - 240, 3)], (220, 60, 60))
    board = (240, 190, 60) if "billboard" in d else (230, 90, 120)
    piece(c, [RRect(660, WATER - 230, 750, WATER - 186, 3), Thick(680, WATER - 186, 680, WATER - 170, 3), Thick(730, WATER - 186, 730, WATER - 170, 3)],
          board, border=2, shadow=PROP)
    person(c, 380, WATER - 120, (200, 80, 80))
    person(c, 410, WATER - 120, (80, 130, 200), h=0.8)
    # water body (buildings show faintly below the surface)
    c.rect(0, WATER, W, 660, (70, 120, 150, 0.82))
    for k in range(8):
        y = WATER + 20 + k * 26
        for x in range(-20, 920, 70):
            flat(c, Ell(x + (k % 2) * 35, y, 22, 2.4), (150, 190, 210, 0.6))


def l35_waves(c, m):
    piece(c, wave_strip(WATER - 2, 5, 46, 0.0, x0=-100, x1=1000, bottom=WATER + 14), (110, 160, 190), border=1.5, shadow=None)


def l35_boat(c, m):
    col = (90, 170, 120) if m else (220, 120, 60)
    piece(c, Poly([(250, WATER + 8), (350, WATER + 8), (336, WATER + 26), (264, WATER + 26)]), col, border=2, shadow=SMALL)
    person(c, 300, WATER + 10, (90, 110, 150), h=0.9)
    flat(c, [Thick(280, WATER - 4, 330, WATER + 30, 2.5)], (140, 100, 70))


def l35_debris(x, kind):
    def d(c, m):
        if kind == "barrel":
            piece(c, RRect(x - 14, WATER - 6, x + 14, WATER + 12, 6), (200, 80, 60), border=1.5, shadow=SMALL)
        else:
            piece(c, RRect(x - 30, WATER - 2, x + 30, WATER + 8, 2), (170, 120, 80), border=1.5, shadow=SMALL)
    return d


def l35_duck(c, m):
    piece(c, [Ell(820, WATER + 2, 12, 7), Circ(830, WATER - 8, 5)], (250, 220, 80), border=1.2, shadow=SMALL)
    flat(c, Poly([(835, WATER - 8), (842, WATER - 6), (835, WATER - 4)]), (240, 140, 50))


L35_EL = [
    cloud("cloud_g1", 160, 60, 1.3, (170, 176, 192), W_(OVERCAST, RAIN)),
    cloud("cloud_g2", 520, 40, 1.5, (170, 176, 192), W_(OVERCAST, RAIN)),
    cloud("cloud_g3", 820, 70, 1.2, (170, 176, 192), W_(OVERCAST, RAIN)),
    cloud_el("cloud_w", 300, 80, 0.8, 6, weather=W_(CLEAR)),
    E("waves", l35_waves, anim=dict(bobAmplitude=(20, 0), bobSpeed=0.1)),
    E("boat", l35_boat, variant=True, pivot=(300, WATER + 20), anim=dict(bobAmplitude=(30, 3), bobSpeed=0.06, swingAngle=4, swingSpeed=0.3)),
    E("barrel", l35_debris(150, "barrel"), show="A", pivot=(150, WATER), anim=dict(bobAmplitude=(6, 3), bobSpeed=0.25, swingAngle=10, swingSpeed=0.3)),
    E("plank", l35_debris(620, "plank"), pivot=(620, WATER), anim=dict(bobAmplitude=(8, 2), bobSpeed=0.2, swingAngle=4, swingSpeed=0.25)),
    E("duck", l35_duck, pivot=(820, WATER), anim=dict(bobAmplitude=(40, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85),
      animB=dict(bobAmplitude=(-40, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85, phase=0.5)),
    bird_el("gull", 600, 120, 10, speed=22),
] + splash_rings("ripple", [(120, 470, 12), (300, 520, 12), (460, 450, 10), (640, 500, 12), (800, 470, 11), (220, 560, 10)]) + [
    rain_layer("rain", 35, 90, 26, 1.3, 0.7, 250),
]
L35_DIFFS = [("boat", 300, WATER + 6, 64), ("barrel", 150, WATER + 3, 0), ("banner", 252, WATER - 240, 0), ("billboard", 705, WATER - 208, 0),
             ("antenna", 555, WATER - 290, 0), ("window", 543, WATER - 205, 0), ("duck", 820, WATER, 60)]


# =================================================================== 36 rainforest (side, rain / mist)
STEPS36 = [(CLEAR, 10), (OVERCAST, 5), (RAIN, 14), (FOG, 6)]


def l36_bg(c, d):
    sky(c, (150, 200, 180), (210, 236, 210))
    for top, col in ((180, (90, 150, 110)), (250, (70, 130, 90)), (330, (56, 112, 78))):
        layer(c, top, [(30, 0.012, top * 0.01), (14, 0.03, 1.2)], col)
        rnd = random.Random(top)
        for _ in range(9):
            x = rnd.uniform(0, W)
            r = rnd.uniform(26, 44)
            piece(c, [Circ(x, gy(top, [(30, 0.012, top * 0.01), (14, 0.03, 1.2)], x) - r * 0.4, r)], lit(col, 1.08), shadow=SMALL)
    # waterfall cliff
    piece(c, Poly([(560, 120), (700, 100), (720, 420), (540, 430)]), (110, 120, 110), shadow=LAYER)
    flat(c, RRect(600, 110, 660, 430, 6), (180, 225, 240))
    piece(c, Ell(630, 440, 110, 26), (130, 190, 210), border=2, shadow=SMALL)
    # big trees with vines
    for x, s in ((120, 1.4), (360, 1.1), (820, 1.5)):
        b = 520
        piece(c, [RRect(x - 16 * s, 160, x + 16 * s, b, 4), Poly([(x - 16 * s, b - 30), (x - 40 * s, b), (x + 40 * s, b), (x + 16 * s, b - 30)])],
              (110, 80, 60), border=1.5, shadow=PROP)
        piece(c, [Circ(x, 150, 70 * s), Circ(x - 60 * s, 180, 46 * s), Circ(x + 60 * s, 180, 46 * s)], (60, 140, 80), shadow=PROP)
        for k in range(3):
            vx = x - 40 * s + k * 40 * s
            flat(c, Thick(vx, 200, vx + 6, 330 + k * 20, 2.5), (70, 130, 70))
    # toucan on the left tree (beak colour differs)
    piece(c, [Ell(160, 260, 12, 16), Circ(164, 244, 9)], (40, 40, 50), border=1.2, shadow=SMALL)
    flat(c, Ell(162, 254, 6, 8), (255, 240, 200))
    beak = (90, 200, 120) if "beak" in d else (255, 150, 40)
    flat(c, Poly([(170, 240), (196, 246), (170, 250)]), beak)
    flat(c, Thick(130, 276, 200, 276, 4), (110, 80, 60))
    # front ground + plants
    layer(c, 500, [(10, 0.015, 0.3), (5, 0.04, 1.0)], (60, 110, 70))
    for x in (40, 230, 470, 700, 880):
        if x == 700 and "plant" in d:
            continue
        piece(c, [Ell(x - 24, 500, 30, 10), Ell(x + 24, 496, 30, 10), Ell(x, 486, 12, 30)], (80, 160, 90), shadow=SMALL)
    # flowers, fruit, frog
    flower = (255, 220, 70) if "flower" in d else (240, 70, 120)
    for x, y in ((300, 470), (520, 480)):
        piece(c, [Circ(x + 7 * math.cos(math.radians(a)), y + 7 * math.sin(math.radians(a)), 6) for a in range(0, 360, 72)], flower,
              shadow=SMALL)
        flat(c, Circ(x, y, 3.5), (255, 240, 150))
    fruits = 3 if "fruit" in d else 4
    for k in range(fruits):
        piece(c, Circ(780 + k * 20, 210 + (k % 2) * 10, 8), (250, 170, 50), shadow=SMALL)
    if "frog" not in d:
        piece(c, [Ell(470, 504, 12, 8), Circ(464, 496, 4.5), Circ(476, 496, 4.5)], (90, 200, 90), border=1.2, shadow=SMALL)
        flat(c, [Circ(464, 496, 2), Circ(476, 496, 2)], INK)
    fill_levels.front_Level36(c, d)


def l36_stream(i):
    x = 606 + (i * 7) % 48

    def d(c, m):
        flat(c, Thick(x, 130, x, 170, 2.5), (240, 250, 255, 0.8))
    return E("fall%d" % i, d, daynight="untinted", anim=dict(driftVelocity=(0, -160), driftLength=270, driftFade=True, phase=i / 8))


def l36_parrot(c, m):
    body = (60, 140, 230) if m else (230, 50, 50)
    piece(c, [Ell(300, 120, 14, 8), Poly([(286, 120), (264, 116), (286, 126)])], body, border=1.2, shadow=SMALL)
    piece(c, [Poly([(298, 116), (290, 96), (308, 114)]), Poly([(298, 124), (290, 144), (308, 126)])], (250, 210, 60), shadow=SMALL)
    flat(c, Poly([(312, 118), (320, 121), (312, 124)]), INK)


def l36_monkey(c, m):
    flat(c, Thick(360, 200, 360, 300, 2), (70, 130, 70))
    piece(c, [Circ(360, 316, 13), Circ(360, 300, 9), Thick(360, 320, 372, 336, 4)], (130, 90, 60), border=1.2, shadow=SMALL)
    flat(c, Circ(361, 302, 6), (230, 190, 150))


L36_EL = [
    cloud_el("cloud_w", 200, 70, 0.8, 6, weather=W_(CLEAR)),
    cloud("cloud_g1", 300, 40, 1.4, (170, 180, 176), W_(OVERCAST, RAIN, FOG)),
    cloud("cloud_g2", 700, 50, 1.3, (170, 180, 176), W_(OVERCAST, RAIN, FOG)),
] + [l36_stream(i) for i in range(8)] + [
    E("parrot", l36_parrot, variant=True, pivot=(300, 120),
      anim=dict(orbitRadius=(70, 30), orbitSpeed=0.08, stretch=(0, 0.4), scaleSpeed=3)),
    E("monkey", l36_monkey, pivot=(360, 200), anim=dict(swingAngle=22, swingSpeed=0.3), animB={}),
    E("butterfly", lambda c, m: (piece(c, [Ell(540, 400, 7, 6), Ell(552, 400, 7, 6)], (120, 200, 255), shadow=SMALL),
                                 flat(c, Ell(546, 402, 2, 7), INK)), pivot=(546, 400),
      anim=dict(orbitRadius=(40, 24), orbitSpeed=0.15, stretch=(0.5, 0), scaleSpeed=4)),
] + splash_rings("splash", [(600, 444, 14), (660, 440, 12), (300, 520, 9), (780, 530, 9)]) + [
    rain_layer("rain", 36, 90, 26, 1.3, 0.65, 250),
    fog_layer("mist1", 36, 200, 380, 0.5, 8, 1, col=(225, 240, 228)),
    fog_layer("mist2", 37, 380, 560, 0.55, 11, -1, col=(225, 240, 228)),
]
L36_DIFFS = [("beak", 183, 245, 0), ("flower", 300, 470, 0), ("fruit", 840, 216, 0), ("frog", 470, 500, 0), ("parrot", 300, 120, 90),
             ("monkey", 360, 300, 50), ("plant", 700, 488, 0)]


# =================================================================== 37 polar (side, day/night + snow, aurora)
DN37 = day_night(40.0, tint=(0.34, 0.38, 0.62))
SUN37, MOON37 = celestial((450, 170), (420, 130), 40.0)
STEPS37 = [(CLEAR, 14), (SNOW, 12), (CLEAR, 14)]


def l37_bg(c, d):
    sky(c, (150, 196, 236), (226, 240, 250))
    fill_levels.back_Level37(c, d)
    for pts, col in (([(-20, 300), (120, 200), (240, 260), (360, 180), (520, 280), (700, 190), (920, 300), (920, 360), (-20, 360)], (214, 230, 246)),
                     ([(-20, 340), (200, 270), (420, 330), (620, 260), (920, 340), (920, 380), (-20, 380)], (196, 216, 238))):
        piece(c, Poly(pts), col, shadow=LAYER)
    # sea and ice floes
    c.rect(0, 380, W, 660, (60, 100, 150))
    berg = [(600, 380), (640, 300), (690, 290), (730, 380)] if "berg" not in d else [(600, 380), (630, 330), (700, 320), (730, 380)]
    piece(c, Poly(berg), (236, 246, 255), shadow=PROP)
    flat(c, Poly([(665, 295) if "berg" not in d else (665, 325), (730, 380), (690, 380)]), (200, 222, 244))
    if "flag" not in d:
        piece(c, [Thick(690, 292, 690, 250, 2), Poly([(691, 250), (712, 256), (691, 262)])], (230, 70, 70), shadow=SMALL)
    piece(c, Poly([(-20, 420), (380, 410), (420, 440), (-20, 460)]), (240, 248, 255), shadow=PROP)
    piece(c, Poly([(-20, 460), (920, 450), (920, 610), (-20, 610)]), (246, 250, 255), shadow=LAYER)
    # igloo (door shape differs)
    pts = [(200 + 70 * math.cos(math.radians(a)), 470 - 56 * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    piece(c, Poly(pts), (236, 244, 252), border=2, shadow=PROP)
    for k in range(1, 4):
        flat(c, Thick(200 - 70 + k * 6, 470 - k * 14, 200 + 70 - k * 6, 470 - k * 14, 1.5), (200, 214, 232))
    if "igloo" in d:
        flat(c, RRect(236, 444, 262, 470, 2), (90, 110, 140))
    else:
        flat(c, [RRect(236, 452, 262, 470, 0), Circ(249, 452, 13)], (90, 110, 140))
    # sled
    sled = (90, 150, 210) if "sled" in d else (200, 90, 60)
    piece(c, [RRect(320, 470, 400, 480, 3), Thick(316, 486, 404, 486, 3)], sled, border=1.5, shadow=SMALL)
    # penguin group (one fewer in B)
    group = [(480, 520), (510, 528), (540, 518)] + ([] if "penguins" in d else [(570, 526)])
    for x, b in group:
        piece(c, [Ell(x, b - 18, 11, 18), Circ(x, b - 38, 8)], (40, 44, 56), border=1.2, shadow=SMALL)
        flat(c, Ell(x + 2, b - 16, 7, 13), (250, 250, 250))
        flat(c, Poly([(x + 7, b - 39), (x + 13, b - 37), (x + 7, b - 35)]), (250, 170, 50))
    fill_levels.front_Level37(c, d)


def l37_aurora(c, m):
    for k, col in enumerate(((120, 255, 180), (160, 120, 255))):
        pts = [(x, 90 + k * 40 + 26 * math.sin(x * 0.012 + k)) for x in range(-20, 940, 20)]
        shapes = [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 18) for i in range(len(pts) - 1)]
        soft_union(c, shapes, col, 0.35, spread=24)


def l37_bear(c, m):
    x, b = 780, 540
    piece(c, [Ell(x, b - 26, 40, 22), Circ(x + 38, b - 36, 15), Circ(x + 30, b - 50, 5), RRect(x - 30, b - 14, x - 18, b, 4),
              RRect(x + 16, b - 14, x + 28, b, 4)], (250, 248, 240), border=1.5, shadow=PROP)
    flat(c, [Circ(x + 50, b - 34, 3), Circ(x + 40, b - 40, 1.6)], INK)


def l37_seal(c, m):
    piece(c, [Ell(120, 412, 26, 10), Circ(144, 404, 8), Poly([(96, 412), (86, 404), (88, 418)])], (130, 130, 140), border=1.2, shadow=SMALL)
    flat(c, Circ(147, 402, 1.5), INK)


def l37_spout(c, m):
    for k in range(3):
        flat(c, Thick(860, 420, 860 + (k - 1) * 12, 380, 3), (220, 236, 250))
    piece(c, Ell(860, 428, 30, 8), (60, 70, 90), shadow=None)


L37_EL = [
    star_field("stars", 37, 60, 300),
    E("aurora", l37_aurora, daynight="night", anim=dict(twinkle=0.4, twinkleSpeed=0.25, bobAmplitude=(20, 4), bobSpeed=0.05)),
    moon_element("moon", (450, 170), MOON37),
    sun_element("sun", (450, 170), SUN37, r=24),
    E("bear", l37_bear, pivot=(780, 540), anim=dict(bobAmplitude=(60, 0), bobSpeed=0.04, spinSpeed=0.04, spinSnap=0.85, swingAngle=2, swingSpeed=1.0)),
    E("seal", l37_seal, show="A", pivot=(120, 412), anim=dict(swingAngle=6, swingSpeed=0.3)),
    E("spout", l37_spout, pivot=(860, 428), anim=dict(stretch=(0, 0.4), scaleSpeed=0.8, twinkle=0.6, twinkleSpeed=0.4)),
    E("walker", lambda c, m: (piece(c, [Ell(420, 532, 10, 16), Circ(420, 512, 7)], (40, 44, 56), border=1.2, shadow=SMALL),
                              flat(c, Ell(422, 534, 6, 11), (250, 250, 250))), pivot=(420, 548),
      anim=dict(swingAngle=8, swingSpeed=1.2, bobAmplitude=(30, 0), bobSpeed=0.06), animB=dict(swingAngle=8, swingSpeed=1.2, bobAmplitude=(-30, 0), bobSpeed=0.06)),
    snow_layer("snow_far", 37, 70, 1.0, 2.0, 16),
    snow_layer("snow_near", 38, 30, 2.4, 3.8, 30),
]
L37_DIFFS = [("berg", 665, 320, 0), ("flag", 700, 256, 0), ("igloo", 249, 456, 0), ("sled", 360, 478, 0), ("penguins", 570, 510, 0),
             ("seal", 118, 410, 0), ("walker", 420, 520, 50)]


# =================================================================== 38 volcano island (side, ash fog)
STEPS38 = [(CLEAR, 12), (FOG, 10), (CLEAR, 8)]


def l38_bg(c, d):
    sky(c, (230, 150, 110), (255, 210, 160))
    fill_levels.back_Level38(c, d)
    sun_bg(c, 780, 120, 30, col=(255, 230, 170))
    piece(c, Poly([(120, 470), (330, 190), (380, 170), (440, 172), (490, 200), (720, 470)]), (110, 70, 66), shadow=LAYER)
    flat(c, Poly([(380, 170), (440, 172), (490, 200), (720, 470), (600, 470)]), (90, 56, 56))
    soft_union(c, [Ell(410, 176, 34, 8)], (255, 140, 50), 0.8, spread=16)
    flows = [[(400, 180), (380, 260), (350, 330), (300, 420)], [(430, 182), (470, 270), (520, 360), (560, 450)]]
    if "lava" not in d:
        flows.append([(412, 180), (420, 280), (410, 380), (430, 460)])
    for pts in flows:
        segs = [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 9) for i in range(len(pts) - 1)]
        soft_union(c, segs, (255, 120, 40), 0.55, spread=12)
        flat(c, segs, (255, 170, 60))
    # sea, beach, jungle
    c.rect(0, 470, W, 660, (60, 120, 160))
    piece(c, Poly([(-20, 500), (300, 470), (620, 480), (920, 500), (920, 610), (-20, 610)]), (230, 200, 140), shadow=LAYER)
    for x in (60, 180, 760, 860):
        if x == 760 and "tree" in d:
            dead_tree(c, x, 500, 0.9)
        else:
            palm(c, x, 500, 120, 16)
    # rock pillar, hut, boulder
    if "pillar" not in d:
        piece(c, Poly([(640, 520), (650, 440), (672, 430), (684, 520)]), (100, 90, 96), shadow=PROP)
    hut = (120, 170, 210) if "hut" in d else (210, 150, 90)
    house(c, 280, 560, 90, 50, hut, (190, 160, 100), roof="gable", wins=1)
    rock(c, 520, 580, 1.2, (90, 80, 90))
    piece(c, Ell(150, 560, 50, 12), (255, 120, 50), border=2, border_col=(90, 60, 50), shadow=SMALL)
    fill_levels.front_Level38(c, d)


def l38_bomb(i):
    x0 = 410 + (i - 1) * 16

    def d(c, m):
        soft_union(c, [Circ(x0, 170, 5)], (255, 120, 40), 0.7, spread=10)
        piece(c, Circ(x0, 170, 6), (80, 50, 50), shadow=None)
    return E("bomb%d" % i, d, pivot=(x0, 170), daynight="untinted",
             anim=dict(bobAmplitude=((i - 1) * 40, 80), bobSpeed=0.25 + 0.05 * i, bounce=True, rotateSpeed=200, phase=i * 0.3))


def l38_ptero(c, m):
    col = (150, 110, 160) if m else (120, 150, 110)
    piece(c, [Poly([(600, 100), (560, 86), (540, 96), (596, 106)]), Poly([(620, 100), (660, 86), (680, 96), (624, 106)]), Ell(610, 102, 12, 5),
              Poly([(620, 98), (640, 92), (624, 104)])], col, border=1.2, shadow=SMALL)


L38_EL = [
    E("ptero", l38_ptero, variant=True, pivot=(610, 100), anim=dict(orbitRadius=(60, 20), orbitSpeed=0.06, stretch=(0, 0.35), scaleSpeed=1.4)),
] + smoke_el("plume", 410, 150, n=5, col=(90, 80, 84), r=22, rise=(10, 30), length=150) + [l38_bomb(i) for i in range(3)] \
  + smoke_el("vent", 560, 450, n=3, col=(240, 236, 236), r=8, show="A", length=60) + [
    E("lava_glow", lambda c, m: soft_union(c, [Ell(150, 560, 50, 12)], (255, 160, 60), 0.5, spread=16), daynight="untinted",
      anim=dict(pulse=0.08, scaleSpeed=0.6, twinkle=0.3, twinkleSpeed=0.6)),
] + bubbles_el("lava_b", 150, 556, n=3, r=4, rise=(0, 12), length=16, show="A", col=(255, 200, 120)) + [
    fog_layer("ash1", 38, 120, 330, 0.55, 10, 1, col=(150, 130, 130)),
    fog_layer("ash2", 39, 330, 520, 0.55, 14, -1, col=(150, 130, 130)),
]
L38_DIFFS = [("lava", 420, 320, 0), ("tree", 760, 440, 0), ("pillar", 662, 475, 0), ("hut", 280, 540, 0), ("ptero", 630, 100, 118),
             ("vent", 560, 420, 40), ("bubbles", 150, 548, 30)]


# =================================================================== 39 deep sea (side)
def l39_bg(c, d):
    sky(c, (14, 30, 60), (6, 14, 30))
    fill_levels.back_Level39(c, d)
    rnd = random.Random(39)
    for _ in range(80):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 500), rnd.uniform(0.6, 1.6)), (150, 200, 230, 0.5))
    piece(c, Poly([(-20, 470), (160, 440), (320, 470), (520, 430), (700, 460), (920, 440), (920, 610), (-20, 610)]), (40, 50, 70), shadow=LAYER)
    for x, s in ((90, 1.2), (420, 0.9), (820, 1.3)):
        rock(c, x, 520, s, (60, 70, 90))
    # bioluminescent corals (one colour differs)
    for i, (x, col) in enumerate(((240, (255, 90, 200)), (560, (90, 255, 220)), (700, (180, 120, 255)))):
        if i == 1 and "coral" in d:
            col = (255, 200, 80)
        b = 470
        shapes = [Thick(x, b, x, b - 50, 4), Thick(x, b - 20, x - 18, b - 46, 3), Thick(x, b - 30, x + 20, b - 56, 3)]
        soft_union(c, shapes, col, 0.35, spread=10)
        flat(c, shapes, col)
    # tube worms
    for k in range(5):
        x = 330 + k * 12
        piece(c, RRect(x - 3, 430 - k % 2 * 10, x + 3, 470, 3), (220, 220, 230), shadow=None)
        flat(c, Circ(x, 430 - k % 2 * 10, 5), (230, 60, 60))
    if "starfish" not in d:
        piece(c, Poly(star_pts(640, 478, 12, 5)), (255, 120, 90), shadow=SMALL)
    if "crab" not in d:
        piece(c, [Ell(470, 478, 14, 8), Circ(458, 470, 4), Circ(482, 470, 4)], (200, 80, 60), border=1.2, shadow=SMALL)
    # hydrothermal vent
    piece(c, Poly([(120, 470), (132, 400), (150, 400), (162, 470)]), (70, 60, 70), shadow=PROP)
    fill_levels.front_Level39(c, d)


def l39_sub(c, m):
    col = (90, 200, 120) if m else (240, 200, 60)
    c.polygon([(660, 180), (520, 120), (520, 250)], (220, 240, 255, 0.15))
    piece(c, [Ell(720, 180, 60, 26), RRect(704, 140, 740, 162, 6), Poly([(780, 180), (800, 164), (800, 196)])], col, border=2, shadow=None)
    for x in (690, 720, 750):
        flat(c, Circ(x, 180, 7), (150, 220, 255))


def l39_angler(c, m):
    lure = (120, 255, 160) if m else (255, 240, 140)
    piece(c, [Ell(300, 330, 34, 24), Poly([(330, 330), (350, 316), (350, 344)])], (50, 50, 70), border=1.5, border_col=(80, 90, 110), shadow=None)
    flat(c, [Poly([(270, 334), (290, 344), (270, 352)])], (240, 240, 240))
    flat(c, Thick(282, 310, 262, 284, 2), (90, 90, 110))
    soft_union(c, [Circ(260, 282, 5)], lure, 0.8, spread=16)
    flat(c, Circ(260, 282, 5), lure)
    flat(c, Circ(286, 322, 3), (255, 255, 200))


def l39_jelly(x, y, col):
    def d(c, m):
        pts = [(x + 22 * math.cos(math.radians(a)), y - 18 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
        soft_union(c, [Poly(pts)], col, 0.3, spread=12)
        flat(c, Poly(pts), col + (0.7,))
        for k in range(4):
            xx = x - 15 + k * 10
            flat(c, Thick(xx, y, xx + 3, y + 30, 1.4), col + (0.6,))
    return d


def l39_school(c, m):
    for k in range(6):
        fish(c, 560 + (k % 3) * 22, 300 + (k // 3) * 16 + (k % 2) * 6, 0.6, (150, 200, 230), right=True)


L39_EL = [
    E("sub", l39_sub, variant=True, pivot=(720, 180), daynight="untinted", anim=dict(bobAmplitude=(10, 6), bobSpeed=0.1, swingAngle=2, swingSpeed=0.1)),
    E("angler", l39_angler, variant=True, pivot=(300, 330), daynight="untinted", anim=dict(bobAmplitude=(30, 10), bobSpeed=0.06)),
    E("jelly1", l39_jelly(160, 200, (255, 140, 220)), pivot=(160, 210), daynight="untinted",
      anim=dict(bobAmplitude=(0, 30), bobSpeed=0.12, stretch=(0.1, -0.12), scaleSpeed=0.7)),
    E("jelly2", l39_jelly(450, 140, (140, 220, 255)), show="A", pivot=(450, 150), daynight="untinted",
      anim=dict(bobAmplitude=(0, 26), bobSpeed=0.1, stretch=(0.1, -0.12), scaleSpeed=0.6, phase=0.4)),
    E("school", l39_school, pivot=(590, 310), anim=dict(drift_across(540, 640, 30))),
] + bubbles_el("vent", 141, 396, n=5, r=5, length=200, show="A") + bubbles_el("sub_b", 790, 180, n=3, r=3, length=90)
L39_DIFFS = [("sub", 720, 175, 0), ("lure", 262, 290, 52), ("jelly", 450, 150, 50), ("coral", 560, 440, 0), ("crab", 470, 475, 0),
             ("vent", 141, 300, 104), ("starfish", 640, 478, 0)]


# =================================================================== 40 underground ruins (cross-section)
def l40_bg(c, d):
    c.rect(0, 0, W, 660, (90, 70, 60))
    for top, col in ((0, (110, 86, 70)), (150, (96, 74, 62)), (330, (84, 64, 56))):
        layer(c, top, [(14, 0.01, top * 0.01), (6, 0.03, 1.0)], col)
    # carved chambers
    for x0, y0, x1, y1 in ((60, 120, 420, 300), (480, 100, 860, 300), (120, 360, 800, 560)):
        flat(c, RRect(x0, y0, x1, y1, 30), (50, 38, 36))
        for s in (RRect(x0, y0, x1, y1, 30),):
            s.draw(c, (66, 52, 48), -6, 0, 6)
    # light shaft from the surface
    c.polygon([(560, 0), (620, 0), (700, 300), (580, 300)], (255, 240, 200, 0.18))
    # pillars and statue (head missing in B)
    for x in (120, 360):
        piece(c, [RRect(x - 16, 140, x + 16, 300, 2), RRect(x - 24, 130, x + 24, 146, 2), RRect(x - 24, 290, x + 24, 300, 2)], (190, 170, 140), shadow=PROP)
    piece(c, RRect(220, 250, 280, 300, 2), (170, 150, 120), shadow=PROP)
    piece(c, [RRect(232, 190, 268, 250, 6)], (180, 160, 130), shadow=PROP)
    if "statue" not in d:
        piece(c, Circ(250, 176, 16), (180, 160, 130), shadow=PROP)
    # treasure chest (open in A, closed in B), gems
    cx, cy = 700, 300
    piece(c, RRect(cx - 34, cy - 30, cx + 34, cy, 3), (150, 92, 55), border=2, border_col=(230, 190, 90), shadow=PROP)
    if "chest" in d:
        piece(c, RRect(cx - 36, cy - 44, cx + 36, cy - 28, 6), (165, 102, 62), border=2, border_col=(230, 190, 90), shadow=PROP)
    else:
        piece(c, Poly([(cx - 34, cy - 30), (cx + 34, cy - 30), (cx + 40, cy - 58), (cx - 28, cy - 62)]), (165, 102, 62), border=2,
              border_col=(230, 190, 90), shadow=PROP)
        for k in range(5):
            piece(c, Circ(cx - 20 + k * 10, cy - 34 + (k % 2) * 4, 6), (250, 210, 70), shadow=SMALL)
    gem = (90, 220, 120) if "gem" in d else (230, 60, 90)
    crystal(c, 560, 300, 0.9, gem)
    # minecart track on the lower level
    flat(c, Thick(120, 548, 800, 548, 3), (150, 130, 110))
    for x in range(130, 800, 30):
        flat(c, Thick(x, 544, x, 556, 4), (110, 80, 60))
    # spider web (missing in B), hanging bats (3 vs 2), lever
    if "web" not in d:
        for k in range(5):
            a = math.radians(k * 22)
            flat(c, Thick(480, 100, 480 + 70 * math.cos(a), 100 + 70 * math.sin(a), 1), (230, 230, 230, 0.8))
        for r in (20, 40, 60):
            pts = [(480 + r * math.cos(math.radians(a)), 100 + r * math.sin(math.radians(a))) for a in range(0, 91, 22)]
            flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1) for i in range(len(pts) - 1)], (230, 230, 230, 0.8))
    bats = [(300, 368), (340, 372), (380, 366)] if "bats" not in d else [(300, 368), (380, 366)]
    for x, y in bats:
        piece(c, [Ell(x, y + 10, 6, 10), Poly([(x - 6, y + 4), (x - 12, y + 16), (x - 4, y + 18)]), Poly([(x + 6, y + 4), (x + 12, y + 16), (x + 4, y + 18)])],
              (40, 34, 40), shadow=SMALL)
    lever_a = (-30 if "lever" in d else 30)
    piece(c, [RRect(760, 520, 790, 548, 3), Thick(775, 524, 775 + 30 * math.sin(math.radians(lever_a)), 524 - 30 * math.cos(math.radians(lever_a)), 4)],
          (120, 110, 100), shadow=SMALL)
    fill_levels.front_Level40(c, d)


def l40_cart(c, m):
    piece(c, [Poly([(150, 516), (220, 516), (212, 542), (158, 542)])], (130, 120, 110), border=1.5, shadow=SMALL)
    flat(c, [Circ(166, 546, 6), Circ(204, 546, 6)], (50, 45, 48))
    for k in range(3):
        piece(c, Circ(170 + k * 14, 512, 7), (250, 210, 70), shadow=None)


def l40_drip(i, x):
    def d(c, m):
        flat(c, Ell(x, 130, 2.4, 4), (170, 210, 240))
    return E("drip%d" % i, d, daynight="untinted", anim=dict(driftVelocity=(0, -120), driftLength=160, driftFade=True, phase=i * 0.37))


L40_EL = [
    E("cart", l40_cart, anim=dict(bobAmplitude=(260, 0), bobSpeed=0.04)),
] + flame("torch1", 80, 230, 1.2) + flame("torch2", 440, 230, 1.2, show="A") + flame("torch3", 160, 440, 1.2) + [
    l40_drip(i, x) for i, x in enumerate((180, 640, 520))
] + [
    E("bat_fly", lambda c, m: piece(c, [Poly([(600, 420), (586, 412), (590, 422)]), Poly([(600, 420), (614, 412), (610, 422)]), Ell(600, 421, 3, 4)],
                                    (40, 34, 40), shadow=None), pivot=(600, 420),
      anim=dict(orbitRadius=(60, 24), orbitSpeed=0.2, stretch=(0, 0.6), scaleSpeed=3)),
]
L40_DIFFS = [("statue", 250, 176, 0), ("chest", 700, 270, 0), ("torch", 440, 214, 26), ("gem", 560, 270, 0), ("web", 510, 130, 0),
             ("bats", 340, 382, 0), ("lever", 775, 510, 0)]


LEVELS = [
    ("Level35", "水没都市", l35_bg, L35_EL, L35_DIFFS, 140,
     opts(weather=dict(steps=STEPS35, blend=3.0), anim_seconds=30.0, frames=60)),
    ("Level36", "热带雨林", l36_bg, L36_EL, L36_DIFFS, 140,
     opts(weather=dict(steps=STEPS36, blend=3.0, tints={FOG: (0.92, 0.96, 0.92)}), anim_seconds=35.0, frames=70)),
    ("Level37", "极地冰原", l37_bg, L37_EL, L37_DIFFS, 140,
     opts(day_night=DN37, weather=dict(steps=STEPS37, blend=3.0), anim_seconds=40.0, frames=80)),
    ("Level38", "火山岛", l38_bg, L38_EL, L38_DIFFS, 140,
     opts(weather=dict(steps=STEPS38, blend=3.0, tints={FOG: (0.72, 0.66, 0.66)}), anim_seconds=30.0, frames=60)),
    ("Level39", "深海", l39_bg, L39_EL, L39_DIFFS, 140, opts()),
    ("Level40", "地下遗迹", l40_bg, L40_EL, L40_DIFFS, 140, opts()),
]
