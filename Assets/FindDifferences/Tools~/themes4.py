# -*- coding: utf-8 -*-
"""Theme levels 47-52: oil painting, pencil sketch, animal town, alchemy lab, floating isles, fairy forest."""
import math
import random
import fill_levels

from fdcore import CLEAR, E, FOG, H, OVERCAST, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import (INK, LAYER, PROP, SMALL, animal, barrel, bird_el, bubble, bubbles_el, bush, cloud_bg, cloud_el, crate, crystal,
                 drift_across, fish, glow_el, gy, house, lamp_post, layer, mushroom, oil_post, palm, person, rock, sign, sketch_post, sky,
                 smoke_el, spin_el, sun_bg, tree_pine, tree_round)
from stylekit import celestial, day_night, flame, moon_element, star_field, sun_element, window_glow


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=36.0, frames=72)
    o.update(kw)
    return o


# =================================================================== 47 oil painting: wheat field under a swirling sky
G47 = (360, [(14, 0.008, 0.6), (6, 0.025, 1.4)])


def l47_bg(c, d):
    sky(c, (40, 80, 170), (120, 170, 220))
    # swirling strokes
    for cx, cy, r0 in ((300, 120, 70), (560, 90, 50), (740, 170, 40)):
        for k in range(4):
            r = r0 - k * 14
            pts = [(cx + r * math.cos(math.radians(a)), cy + r * 0.6 * math.sin(math.radians(a))) for a in range(0, 330, 15)]
            flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 6) for i in range(len(pts) - 1)],
                 [(150, 190, 240), (230, 230, 200), (90, 130, 210), (250, 240, 170)][k])
    for y in range(40, 300, 22):
        for x in range(-20, 920, 60):
            flat(c, Thick(x + (y % 44), y, x + 30 + (y % 44), y + 6, 4), (70, 120, 200, 0.6))
    # farmhouse + cypress
    layer(c, *G47, (190, 160, 70))
    b = gy(*G47, 640) + 8
    roof = (90, 130, 200) if "roof" in d else (200, 80, 50)
    house(c, 640, b, 110, 60, (240, 220, 170), roof, wins=2)
    for i, (x, h) in enumerate(((160, 230), (220, 170))):
        if i == 1 and "cypress" in d:
            continue
        bb = gy(*G47, x) + 10
        pts = [(x - 18, bb), (x - 26, bb - h * 0.4), (x - 14, bb - h * 0.75), (x, bb - h), (x + 14, bb - h * 0.75), (x + 26, bb - h * 0.4), (x + 18, bb)]
        piece(c, Poly(pts), (30, 70, 50), shadow=PROP)
        for k in range(5):
            flat(c, Thick(x - 10 + k * 5, bb - 10, x - 6 + k * 4, bb - h * 0.8, 3), (50, 100, 70))
    # wheat field with strokes, path, haystacks, poppies, cart
    layer(c, 430, [(10, 0.01, 0.2), (4, 0.03, 1.0)], (230, 190, 70))
    rnd = random.Random(47)
    for _ in range(260):
        x, y = rnd.uniform(0, W), rnd.uniform(430, 600)
        flat(c, Thick(x, y, x + rnd.uniform(-6, 6), y - 14, 3), rnd.choice(((250, 220, 90), (210, 160, 50), (240, 200, 70))))
    path = [(420, 600), (470, 440), (500, 440), (560, 600)] if "path" not in d else [(440, 600), (480, 440), (500, 440), (520, 600)]
    piece(c, Poly(path), (200, 160, 110), shadow=None)
    for i, x in enumerate((300, 760)):
        if i == 1 and "haystack" in d:
            continue
        piece(c, Poly([(x - 40, 500), (x - 30, 460), (x, 440), (x + 30, 460), (x + 40, 500)]), (220, 170, 60), shadow=PROP)
    if "poppies" not in d:
        for k in range(9):
            flat(c, Circ(80 + (k % 3) * 24, 520 + (k // 3) * 18, 7), (220, 50, 40))
    if "cart" not in d:
        piece(c, [RRect(820, 540, 880, 560, 3), Circ(832, 566, 10), Circ(868, 566, 10)], (150, 100, 60), shadow=PROP)


def l47_sun(c, m):
    soft_union(c, [Circ(780, 80, 36)], (255, 240, 140), 0.6, spread=40)
    flat(c, Circ(780, 80, 34), (255, 220, 80))
    for k in range(3):
        c.ellipse_ring(780, 80, 46 + k * 12, 46 + k * 12, 5, (250, 230, 120))


def l47_swirl(c, m):
    for k in range(3):
        r = 60 - k * 16
        pts = [(300 + r * math.cos(math.radians(a)), 120 + r * 0.6 * math.sin(math.radians(a))) for a in range(0, 300, 20)]
        flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 7) for i in range(len(pts) - 1)], (250, 250, 220))


def l47_wheat(c, m):
    for k in range(40):
        x = k * 23
        flat(c, Thick(x, 600, x + 4, 560, 4), (250, 210, 80))


L47_EL = [
    E("sun", l47_sun, pivot=(780, 80), anim=dict(pulse=0.04, scaleSpeed=0.3)),
    E("swirl", l47_swirl, pivot=(300, 120), anim=dict(rotateSpeed=14), animB=dict(rotateSpeed=-14)),
    E("wheat", l47_wheat, pivot=(450, 600), anim=dict(swingAngle=1.5, swingSpeed=0.3)),
    bird_el("crow1", 400, 200, 12, col=(30, 30, 40), speed=20),
    bird_el("crow2", 520, 240, 10, col=(30, 30, 40), speed=16),
]
L47_DIFFS = [("roof", 640, 300, 0), ("cypress", 220, 290, 0), ("path", 490, 520, 0), ("haystack", 760, 470, 0), ("poppies", 104, 538, 0),
             ("cart", 850, 552, 0), ("swirl", 300, 120, 80)]


# =================================================================== 48 pencil sketch: street corner cafe
def l48_bg(c, d):
    c.rect(0, 0, W, 660, (230, 236, 240))
    # buildings
    for x0, x1, top, col in ((0, 300, 60, (230, 210, 190)), (300, 600, 30, (210, 200, 190)), (600, 900, 80, (220, 214, 200))):
        piece(c, RRect(x0, top, x1, 470, 1), col, border=2, shadow=PROP)
        for row in range(4):
            y = top + 30 + row * 80
            if y > 400:
                break
            for xx in range(x0 + 30, x1 - 40, 70):
                piece(c, RRect(xx, y, xx + 34, y + 50, 2), (170, 190, 210), border=2, border_col=(250, 250, 250), shadow=None)
                shut = not ("shutter" in d and x0 == 600 and row == 1 and xx == x0 + 100)
                if shut:
                    flat(c, [RRect(xx - 10, y, xx - 2, y + 50, 1), RRect(xx + 36, y, xx + 44, y + 50, 1)], (120, 140, 120))
                if row == 1:
                    flat(c, Thick(xx - 6, y + 52, xx + 40, y + 52, 3), (90, 90, 100))
                    for k in range(6):
                        flat(c, Thick(xx - 4 + k * 8, y + 52, xx - 4 + k * 8, y + 66, 1.4), (90, 90, 100))
    # plant pots on balconies (one missing in B)
    for i, x in enumerate((70, 380, 650)):
        if i == 1 and "pot" in d:
            continue
        piece(c, [RRect(x, 220, x + 20, 236, 2), Circ(x + 10, 212, 12)], (90, 150, 90), shadow=SMALL)
    # clock on the middle building (missing in B)
    if "clock" not in d:
        piece(c, Circ(450, 70, 22), (250, 250, 245), border=3, border_col=(90, 90, 100), shadow=PROP)
        flat(c, [Thick(450, 70, 450, 56, 2.5), Thick(450, 70, 462, 74, 2.5)], INK)
    # cafe awning (6 or 5 stripes), tables and chairs
    stripes = 6 if "awning" not in d else 5
    piece(c, Poly([(320, 380), (580, 380), (600, 420), (300, 420)]), (250, 250, 250), border=2, shadow=PROP)
    for k in range(stripes):
        x0 = 320 + k * 260 / stripes
        flat(c, Poly([(x0, 380), (x0 + 260 / stripes / 2, 380), (x0 + 260 / stripes / 2 - 4, 420), (x0 - 4, 420)]), (190, 80, 80))
    piece(c, RRect(-10, 470, 910, 610, 0), (200, 196, 190), shadow=LAYER)
    for x in range(0, 900, 40):
        flat(c, Thick(x, 470, x - 30, 600, 1), (176, 172, 168))
    for tx in (370, 520):
        piece(c, [Circ(tx, 500, 26), RRect(tx - 3, 500, tx + 3, 550, 1), RRect(tx - 16, 548, tx + 16, 554, 2)], (240, 240, 240), border=2,
              border_col=(90, 90, 100), shadow=PROP)
        piece(c, RRect(tx - 6, 484, tx + 6, 496, 2), (250, 250, 250), border=1.5, border_col=(90, 90, 100), shadow=None)
    chairs = [(320, 1), (420, -1), (470, 1)] + ([] if "chair" in d else [(570, -1)])
    for x, s in chairs:
        piece(c, [RRect(x - 12, 520, x + 12, 526, 2), Thick(x + 10 * s, 526, x + 10 * s, 556, 2.5), Thick(x - 10 * s, 526, x - 10 * s, 556, 2.5),
                  Thick(x + 12 * s, 520, x + 14 * s, 490, 2.5)], (110, 110, 120), shadow=SMALL)
    lamp_post(c, 700, 560, 140, col=(80, 80, 90))
    if "pigeon" not in d:
        piece(c, [Ell(716, 416, 8, 6), Circ(722, 410, 4)], (150, 150, 160), shadow=SMALL)
    # bicycle (basket missing in B)
    for wx in (770, 830):
        c.ellipse_ring(wx, 548, 20, 20, 3, (60, 60, 70))
    flat(c, [Thick(770, 548, 800, 520, 3), Thick(800, 520, 830, 548, 3), Thick(770, 548, 806, 548, 3), Thick(800, 520, 796, 508, 3),
             Thick(826, 512, 830, 548, 3)], (60, 60, 70))
    piece(c, RRect(818, 498, 842, 514, 2), (170, 140, 100), shadow=None)
    person(c, 400, 560, (100, 120, 160), h=1.3)
    tree_round(c, 120, 560, 1.4, (100, 150, 100))


def l48_steam(i):
    def d(c, m):
        flat(c, Thick(520, 480, 524, 466, 2.5), (180, 180, 190))
    return E("steam%d" % i, d, show="A", anim=dict(driftVelocity=(2, 14), driftLength=30, driftFade=True, phase=i / 3))


L48_EL = [
    E("pigeon2", lambda c, m: piece(c, [Ell(620, 590, 9, 6), Circ(628, 584, 4)], (140, 140, 150), shadow=SMALL), pivot=(620, 594),
      anim=dict(swingAngle=16, swingSpeed=0.6)),
    E("leaves", lambda c, m: piece(c, [Circ(120 + dx, 470 + dy, 12) for dx, dy in ((-30, -10), (10, -30), (34, -6))], (110, 160, 110), shadow=SMALL),
      pivot=(120, 560), anim=dict(swingAngle=2, swingSpeed=0.3)),
] + [l48_steam(i) for i in range(3)]
L48_DIFFS = [("shutter", 720, 215, 0), ("pot", 390, 220, 0), ("clock", 450, 70, 0), ("awning", 450, 400, 0), ("chair", 570, 530, 0),
             ("pigeon", 720, 412, 0), ("steam", 522, 466, 26)]


# =================================================================== 49 animal town
def l49_bg(c, d):
    sky(c, (150, 210, 240), (230, 244, 250))
    fill_levels.back_Level49(c, d)
    cloud_bg(c, 180, 80, 0.9)
    cloud_bg(c, 720, 60, 0.7)
    layer(c, 300, [(14, 0.01, 0.4), (6, 0.03, 1.0)], (150, 200, 130))
    shops = [(110, 200, 170, (250, 220, 170), (200, 90, 80)), (330, 220, 150, (230, 240, 210), (120, 170, 110)),
             (560, 200, 190, (240, 214, 230), (170, 110, 160)), (780, 200, 160, (220, 230, 250), (90, 130, 200))]
    for i, (x, w, h, wall, roof) in enumerate(shops):
        if i == 2 and "roof" in d:
            roof = (230, 180, 70)
        info = house(c, x, 470, w, h, wall, roof, wins=2)
        aw = (90, 160, 210) if (i == 0 and "awning" in d) else roof
        piece(c, Poly([(x - w / 2 + 10, 470 - h * 0.45), (x + w / 2 - 10, 470 - h * 0.45), (x + w / 2, 470 - h * 0.3), (x - w / 2, 470 - h * 0.3)]),
              aw, border=1.5, shadow=SMALL)
        for k in range(5):
            xx = x - w / 2 + 10 + k * (w - 20) / 5
            flat(c, Poly([(xx, 470 - h * 0.45), (xx + (w - 20) / 10, 470 - h * 0.45), (xx + (w - 20) / 10 + 2, 470 - h * 0.3), (xx + 2, 470 - h * 0.3)]),
                 (255, 255, 255))
    # shop signs
    piece(c, Circ(110, 278, 18), (250, 200, 120) if "bread" not in d else (180, 120, 70), border=2, shadow=SMALL)
    # owl clock on the purple shop
    piece(c, Circ(560, 250, 18), (250, 250, 240), border=2, shadow=SMALL)
    if "owl" not in d:
        animal(c, "owl", 600, 286, (150, 120, 90), h=0.7)
    # cat in a window (missing in B), flower pots
    if "cat" not in d:
        animal(c, "cat", 812, 360, (240, 170, 90), h=0.7)
    pots = [(300, (230, 80, 90)), (360, (250, 200, 70))] + ([] if "pot" in d else [(420, (150, 120, 230))])
    for x, col in pots:
        piece(c, [Poly([(x - 10, 470), (x + 10, 470), (x + 8, 450), (x - 8, 450)]), Circ(x, 440, 10)], col, shadow=SMALL)
    piece(c, RRect(-10, 470, 910, 610, 0), (200, 190, 176), shadow=LAYER)
    for x in range(0, 900, 60):
        flat(c, Thick(x, 540, x + 30, 540, 3), (250, 250, 250))
    # shopkeepers / passers-by
    animal(c, "bear", 160, 470, (250, 250, 250), h=1.3)
    animal(c, "rabbit", 400, 470, (250, 180, 200), h=1.2)
    animal(c, "fox", 700, 470, (90, 120, 200) if "fox" in d else (120, 160, 90), h=1.3, face_right=False)
    fill_levels.front_Level49(c, d)


def l49_pig(c, m):
    animal(c, "pig", 500, 560, (240, 220, 120), h=1.3)
    col = (90, 170, 230) if m else (230, 70, 80)
    flat(c, Thick(512, 520, 520, 440, 1.2), INK)
    piece(c, Ell(520, 430, 14, 16), col, border=1.2, shadow=SMALL)


def l49_dog(c, m):
    animal(c, "dog", 250, 580, (200, 80, 80), h=1.2)


def l49_frog(c, m):
    animal(c, "frog", 820, 580, (250, 220, 120), h=1.1, face_right=False)


L49_EL = [
    E("pig", l49_pig, variant=True, pivot=(500, 560), anim=dict(swingAngle=3, swingSpeed=0.4)),
    E("dog", l49_dog, pivot=(250, 580), anim=dict(bobAmplitude=(60, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85),
      animB=dict(bobAmplitude=(-60, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85, phase=0.5)),
    E("frog", l49_frog, pivot=(820, 580), anim=dict(bobAmplitude=(0, 16), bobSpeed=0.5, bounce=True)),
    cloud_el("cloud", 450, 110, 0.6, 6),
    bird_el("bird", 300, 150, 9, speed=18),
]
L49_DIFFS = [("roof", 560, 260, 0), ("awning", 110, 380, 0), ("bread", 110, 278, 0), ("owl", 600, 250, 0), ("cat", 814, 330, 0),
             ("balloon", 520, 430, 0), ("dog", 250, 550, 80)]


# =================================================================== 50 alchemy lab (interior)
def l50_bg(c, d):
    c.rect(0, 0, W, 660, (90, 76, 70))
    for y in range(0, 500, 34):
        for x in range(-30, 920, 64):
            flat(c, RRect(x + (y // 34 % 2) * 32, y, x + (y // 34 % 2) * 32 + 60, y + 30, 3), (104, 90, 82))
    piece(c, RRect(-10, 500, 910, 610, 0), (70, 58, 54), shadow=(0, -3, 8, 0.3))
    # potion shelves
    for y in (150, 240):
        piece(c, RRect(40, y, 330, y + 10, 2), (130, 90, 60), shadow=PROP)
        for k in range(7):
            col = [(230, 70, 90), (90, 200, 120), (120, 140, 250), (250, 200, 70)][(k + y) % 4]
            if y == 150 and k == 3 and "potion" in d:
                col = (250, 120, 30)
            piece(c, [Ell(64 + k * 38, y - 14, 12, 14), RRect(60 + k * 38, y - 40, 68 + k * 38, y - 26, 2)], (230, 236, 240), border=1.2, shadow=SMALL)
            flat(c, Ell(64 + k * 38, y - 10, 10, 9), col)
    # books
    piece(c, RRect(600, 120, 860, 330, 2), (110, 76, 56), shadow=PROP)
    for row, y in enumerate((130, 200, 270)):
        flat(c, Thick(604, y + 58, 856, y + 58, 4), (90, 60, 44))
        for k in range(10):
            col = [(170, 60, 60), (60, 100, 160), (80, 140, 90), (200, 160, 80)][(k + row) % 4]
            if row == 1 and k == 4 and "book" in d:
                col = (230, 230, 230)
            flat(c, RRect(612 + k * 24, y + 10 + (k % 3) * 4, 630 + k * 24, y + 56, 2), col)
    # skull, hanging crocodile
    if "skull" not in d:
        piece(c, [Circ(380, 268, 16), RRect(372, 278, 388, 290, 3)], (240, 236, 220), shadow=SMALL)
        flat(c, [Circ(374, 266, 4), Circ(386, 266, 4)], (60, 50, 50))
    if "croc" not in d:
        flat(c, [Thick(420, 0, 420, 40, 1.2), Thick(560, 0, 560, 40, 1.2)], INK)
        piece(c, [Ell(490, 50, 80, 14), Poly([(410, 50), (380, 44), (380, 56)]), Poly([(570, 48), (600, 42), (600, 58)])], (90, 130, 80), shadow=PROP)
    # table with alembic, cauldron on the floor
    piece(c, [RRect(380, 380, 640, 396, 2), RRect(390, 396, 404, 500, 1), RRect(616, 396, 630, 500, 1)], (130, 90, 60), border=2, shadow=PROP)
    piece(c, [Circ(450, 352, 26), Thick(470, 336, 540, 300, 5), Ell(560, 360, 18, 20)], (220, 236, 240), border=1.5, shadow=SMALL)
    flat(c, Circ(450, 356, 18), (120, 230, 140))
    piece(c, Ell(200, 470, 70, 46), (60, 56, 62), border=2, shadow=PROP)
    flat(c, Ell(200, 432, 62, 12), (130, 230, 120))
    soft_union(c, [Ell(200, 520, 50, 10)], (255, 140, 60), 0.4, spread=14)
    fill_levels.front_Level50(c, d)


def l50_ball(c, m):
    col = (255, 120, 200) if m else (120, 200, 255)
    soft_union(c, [Circ(740, 440, 30)], col, 0.5, spread=26)
    piece(c, Circ(740, 440, 26), col, border=1.5, shadow=None)
    flat(c, Circ(732, 432, 7), (255, 255, 255, 0.8))
    piece(c, RRect(718, 464, 762, 476, 3), (120, 90, 60), shadow=SMALL)


def l50_circle(c, m):
    soft_union(c, [Ell(450, 560, 120, 30)], (240, 200, 120), 0.2, spread=10)
    c.ellipse_ring(450, 560, 120, 30, 3, (240, 200, 120))
    c.ellipse_ring(450, 560, 90, 22, 2, (240, 200, 120))


def l50_star(c, m):
    flat(c, Poly(star_pts(450, 560, 7, 2.8)), (255, 230, 150))


def l50_drop(i):
    def d(c, m):
        flat(c, Ell(560, 384, 2.4, 3.6), (120, 230, 140))
    return E("drop%d" % i, d, show="A", daynight="untinted", anim=dict(driftVelocity=(0, -40), driftLength=24, driftFade=True, phase=i / 2))


L50_EL = [
    E("ball", l50_ball, variant=True, daynight="untinted", anim=dict(twinkle=0.25, twinkleSpeed=0.6)),
    E("circle", l50_circle, daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=0.5)),
] + [
    # runes travelling round the circle; the other way round in B
    E("rune%d" % k, l50_star, pivot=(450, 560), daynight="untinted",
      anim=dict(orbitRadius=(104, 26), orbitSpeed=0.08, phase=k / 6), animB=dict(orbitRadius=(104, 26), orbitSpeed=-0.08, phase=k / 6))
    for k in range(6)
] + [l50_drop(i) for i in range(2)] + bubbles_el("cauldron", 200, 430, n=5, r=6, length=80, col=(160, 255, 150)) \
  + flame("fire", 200, 520, 1.6, glow_night=False) + flame("candle", 300, 370, 0.7, glow_night=False)
L50_DIFFS = [("potion", 178, 136, 0), ("book", 718, 236, 0), ("skull", 380, 276, 0), ("croc", 490, 50, 0), ("ball", 740, 440, 0),
             ("drip", 560, 396, 24), ("circle", 450, 560, 120)]


# =================================================================== 51 floating isles (side, day/night)
DN51 = day_night(40.0, tint=(0.34, 0.34, 0.62))
SUN51, MOON51 = celestial((450, 160), (420, 120), 40.0)
ISLES = [(170, 300, 120), (480, 220, 150), (770, 330, 110)]


def isle(c, x, y, w, grass=(110, 190, 100), rock_col=(150, 120, 100), crystal_col=None):
    piece(c, Poly([(x - w, y), (x + w, y), (x + w * 0.5, y + w * 0.6), (x + w * 0.1, y + w * 1.1), (x - w * 0.4, y + w * 0.7)]), rock_col, shadow=PROP)
    flat(c, Poly([(x + w * 0.1, y + w * 1.1), (x + w, y), (x + w * 0.5, y + w * 0.6)]), lit(rock_col, 0.8))
    piece(c, Ell(x, y, w + 6, 14), grass, shadow=None)
    if crystal_col:
        crystal(c, x + w * 0.1, y + w * 1.25, 0.8, crystal_col)


def l51_bg(c, d):
    sky(c, (120, 180, 240), (240, 236, 250))
    fill_levels.back_Level51(c, d)
    for i, (x, y, w) in enumerate(ISLES):
        isle(c, x, y, w, crystal_col=((120, 230, 160) if "crystal" in d else (160, 120, 255)) if i == 1 else None)
    # buildings / trees on the islands
    roof = (90, 160, 100) if "roof" in d else (200, 80, 70)
    house(c, 140, 294, 70, 50, (246, 236, 214), roof, wins=1)
    tree_round(c, 220, 296, 0.8)
    if "tree" not in d:
        tree_round(c, 540, 216, 0.9)
    house(c, 450, 216, 80, 70, (236, 230, 250), (110, 120, 200), roof="spire", wins=2)
    piece(c, [Thick(770, 326, 770, 240, 6)], (240, 236, 220), shadow=PROP)
    piece(c, Poly([(756, 244), (784, 244), (770, 220)]), (200, 80, 70), shadow=SMALL)
    # rope bridge (missing in B)
    if "bridge" not in d:
        pts = [(290 + k * 10, 300 - k * 4 + 8 * math.sin(math.pi * k / 7)) for k in range(8)]
        flat(c, [Thick(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 2) for k in range(7)], (140, 100, 70))
        for x, y in pts[1:-1]:
            flat(c, RRect(x - 3, y - 2, x + 3, y + 4, 1), (170, 120, 80))


def l51_cloudsea(seed, y, col, speed):
    def d(c, m):
        rnd = random.Random(seed)
        shapes = [Circ(x + k * 300, y + rnd.uniform(-10, 10), rnd.uniform(40, 70)) for k in range(-1, 5) for x in (0, 100, 200)]
        piece(c, shapes, col, shadow=(1, 3, 8, 0.2))
    sp = math.hypot(speed, 0)
    return E("cloudsea%d" % seed, d, bbox=(-380, y - 90, 1600, y + 90), anim=dict(driftVelocity=(speed, 0), driftLength=300))


def l51_stream(i, x, y0, show="both"):
    def d(c, m):
        flat(c, Thick(x + (i % 3) * 5, y0, x + (i % 3) * 5, y0 + 30, 3), (220, 240, 255, 0.85))
    return E("fall_%d_%d" % (x, i), d, show=show, daynight="untinted",
             anim=dict(driftVelocity=(0, -120), driftLength=150, driftFade=True, phase=i / 6))


def l51_ship(c, m):
    col = (90, 170, 230) if m else (240, 160, 80)
    piece(c, Ell(640, 90, 60, 22), col, border=2, shadow=PROP)
    piece(c, RRect(612, 120, 668, 136, 5), (140, 100, 70), border=1.5, shadow=SMALL)
    flat(c, [Thick(620, 110, 626, 120, 1.4), Thick(660, 110, 654, 120, 1.4)], INK)


def l51_mill(c, m):
    for k in range(4):
        a = math.radians(45 + k * 90)
        flat(c, Poly([(770, 240), (770 + 30 * math.cos(a), 240 + 30 * math.sin(a)), (770 + 30 * math.cos(a + 0.4), 240 + 30 * math.sin(a + 0.4))]),
             (250, 246, 236))


L51_EL = [
    star_field("stars", 51, 60, 300),
    moon_element("moon", (450, 160), MOON51),
    sun_element("sun", (450, 160), SUN51, r=24),
    l51_cloudsea(1, 560, (250, 250, 255), 14),
    E("ship", l51_ship, variant=True, pivot=(640, 110), anim=dict(bobAmplitude=(12, 6), bobSpeed=0.08)),
    spin_el("mill", l51_mill, (770, 240), -90, speed_b=90),
    bird_el("bird", 300, 120, 9, speed=20),
] + [l51_stream(i, 600, 230) for i in range(6)] + [l51_stream(i, 820, 340, show="A") for i in range(6)] + [
    window_glow("windows", [(440, 172, 452, 190), (128, 262, 140, 280)]),
    l51_cloudsea(2, 600, (236, 238, 250), 22),
]
L51_DIFFS = [("roof", 140, 254, 0), ("crystal", 495, 400, 0), ("tree", 540, 160, 0), ("bridge", 325, 300, 0), ("ship", 640, 100, 0),
             ("mill", 770, 240, 40), ("waterfall", 828, 420, 92)]


# =================================================================== 52 fairy forest (side, day/night)
DN52 = day_night(40.0, tint=(0.36, 0.30, 0.62))
SUN52, MOON52 = celestial((450, 150), (420, 110), 40.0)


def l52_bg(c, d):
    sky(c, (140, 200, 220), (230, 240, 220))
    for top, col in ((250, (90, 150, 120)), (320, (70, 130, 100))):
        layer(c, top, [(30, 0.01, top * 0.01), (12, 0.03, 1.0)], col)
        for x in range(30, 900, 80):
            tree_pine(c, x, gy(top, [(30, 0.01, top * 0.01), (12, 0.03, 1.0)], x) + 6, 80 if top == 250 else 110, lit(col, 0.85))
    layer(c, 430, [(10, 0.012, 0.3), (5, 0.04, 1.0)], (90, 160, 100))
    # mushroom houses (cap colour differs on the big one)
    cap = (90, 150, 230) if "cap" in d else (220, 70, 80)
    for x, s, col in ((200, 2.6, cap), (640, 2.0, (240, 160, 60))):
        mushroom(c, x, 470, s, cap=col)
        door = (90, 150, 210) if (x == 640 and "door" in d) else (130, 80, 60)
        flat(c, [RRect(x - 9, 470 - 22, x + 9, 470, 6)], door)
        flat(c, Circ(x + 8, 470 - 50 * s / 2.6, 6), (255, 222, 140))
    # lantern on a hook (missing in B), snail, mushroom ring
    if "lantern" not in d:
        flat(c, Thick(268, 430, 268, 400, 2), INK)
        piece(c, RRect(260, 400, 276, 418, 3), (250, 210, 120), border=1, shadow=SMALL)
    if "snail" not in d:
        piece(c, [Ell(420, 470, 18, 6), Circ(426, 458, 10), Thick(408, 462, 404, 450, 1.5)], (230, 180, 120), border=1.2, shadow=SMALL)
        c.ellipse_ring(426, 458, 6, 6, 2, (180, 120, 80))
    ring = 6 if "ring" in d else 7
    for k in range(ring):
        a = math.radians(k * 360 / 7)
        mushroom(c, 780 + 50 * math.cos(a), 520 + 14 * math.sin(a), 0.5, cap=(250, 240, 230), spots=False)
    piece(c, RRect(-10, 520, 910, 610, 0), (70, 130, 80), shadow=LAYER)
    fill_levels.front_Level52(c, d)


def l52_fairy(x, y, col, eid, **kw):
    def d(c, m):
        cc = kw.get("col_b", col) if m else col
        soft_union(c, [Circ(x, y, 6)], cc, 0.6, spread=16)
        flat(c, [Ell(x - 6, y - 4, 6, 4), Ell(x + 6, y - 4, 6, 4)], (230, 250, 255, 0.8))
        flat(c, Circ(x, y, 3.5), (255, 250, 230))
    return d


def l52_flowers(c, m):
    col = (120, 220, 255) if m else (255, 140, 220)
    for x in (100, 330, 520, 880):
        soft_union(c, [Circ(x, 500, 6)], col, 0.5, spread=12)
        flat(c, Circ(x, 500, 5), col)


L52_EL = [
    star_field("stars", 52, 50, 240),
    moon_element("moon", (450, 150), MOON52),
    sun_element("sun", (450, 150), SUN52, r=24),
    E("fairy1", l52_fairy(200, 330, (255, 200, 120), "f1", col_b=(140, 255, 160)), pivot=(200, 330), variant=True, daynight="untinted",
      anim=dict(orbitRadius=(80, 26), orbitSpeed=0.12, orbitDepth=0.3)),
    E("fairy2", l52_fairy(780, 470, (200, 160, 255), "f2"), pivot=(780, 470), daynight="untinted",
      anim=dict(orbitRadius=(56, 16), orbitSpeed=0.1, orbitDepth=0.3), animB=dict(orbitRadius=(56, 16), orbitSpeed=-0.1, orbitDepth=0.3)),
    E("flowers", l52_flowers, variant=True, daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.7)),
    window_glow("windows", [(194, 400, 214, 414), (640, 420, 656, 432)]),
    E("lantern_glow", lambda c, m: soft_union(c, [Circ(268, 410, 8)], (255, 210, 130), 0.6, spread=22), daynight="night"),
] + [
    E("firefly%d" % i, (lambda x, y: lambda c, m: (soft_union(c, [Circ(x, y, 3)], (220, 255, 150), 0.7, spread=8), flat(c, Circ(x, y, 1.8), (250, 255, 220))))(x, y),
      pivot=(x, y), daynight="night", anim=dict(orbitRadius=(16, 10), orbitSpeed=0.2 * (1 if i % 2 else -1), twinkle=0.8, twinkleSpeed=0.6, phase=i * 0.3))
    for i, (x, y) in enumerate(((320, 380), (480, 420), (560, 360), (700, 400), (860, 440), (120, 420)))
]
L52_DIFFS = [("cap", 200, 410, 0), ("door", 640, 459, 0), ("lantern", 268, 410, 0), ("snail", 420, 462, 0), ("fairy", 200, 330, 96),
             ("flowers", 330, 500, 0), ("ring", 780, 500, 0)]


LEVELS = [
    ("Level47", "油画·麦田", l47_bg, L47_EL, L47_DIFFS, 140, opts(post=oil_post)),
    ("Level48", "素描·街角", l48_bg, L48_EL, L48_DIFFS, 140, opts(post=sketch_post)),
    ("Level49", "动物小镇", l49_bg, L49_EL, L49_DIFFS, 140, opts()),
    ("Level50", "炼金工房", l50_bg, L50_EL, L50_DIFFS, 140, opts()),
    ("Level51", "浮空群岛", l51_bg, L51_EL, L51_DIFFS, 140, opts(day_night=DN51, anim_seconds=40.0, frames=80)),
    ("Level52", "妖精森林", l52_bg, L52_EL, L52_DIFFS, 140, opts(day_night=DN52, anim_seconds=40.0, frames=80)),
]
