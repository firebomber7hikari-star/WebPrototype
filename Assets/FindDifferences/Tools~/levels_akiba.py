# -*- coding: utf-8 -*-
"""Akihabara (generic shops and characters, no real brands), paper-craft side views, full-bleed:
  Level114 秋叶原电器街 - the electric town street: sign towers, big screen, the railway overpass, crowds; day / night
  Level115 女仆咖啡厅   - inside a maid cafe: pastel room, maids serving omurice and parfaits
  Level116 手办店       - a figure shop: glass cases of figures, model kits, a wall of capsule machines
  Level117 游戏中心     - an arcade at night: claw machines, drum game, fighting cabinets, photo booth
  Level118 步行者天国   - the Sunday pedestrian street: cosplayers, photographers, flyers
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_el, drift_across, sky
from stylekit import day_night, neon_glyphs, star_field, window_glow
from levels_europe import arch, ellipse_top

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 226, 204)
HAIRS = [(40, 30, 30), (90, 60, 40), (220, 180, 90), (230, 120, 160), (90, 140, 220), (240, 240, 246)]


def modern(c, x, base, top, bottom=(60, 70, 100), hair=(40, 30, 30), h=1.0, style="short", bag=None, glasses=False, ears=None, skirt=False):
    """Modern figure (t-shirt / jacket, trousers or skirt); returns head centre."""
    if skirt:
        piece(c, [Poly([(x - 11 * h, base - 12 * h), (x + 11 * h, base - 12 * h), (x + 6 * h, base - 22 * h), (x - 6 * h, base - 22 * h)])], bottom,
              shadow=SMALL)
        flat(c, [RRect(x - 5 * h, base - 12 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 12 * h, x + 5 * h, base, 1)], SKIN)
    else:
        piece(c, [RRect(x - 6 * h, base - 20 * h, x - 1 * h, base, 1), RRect(x + 1 * h, base - 20 * h, x + 6 * h, base, 1)], bottom, shadow=SMALL)
    piece(c, RRect(x - 8 * h, base - 38 * h, x + 8 * h, base - 18 * h, 3), top, border=1.5, shadow=PROP)
    if bag:
        piece(c, RRect(x - 14 * h, base - 36 * h, x - 6 * h, base - 22 * h, 2), bag, shadow=SMALL)
    hx, hy = x + 1 * h, base - 46 * h
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy, 1.1 * h), INK)
    if style == "long":
        flat(c, [Ell(hx - 3 * h, hy - 2 * h, 8 * h, 9 * h), Ell(hx, hy - 6 * h, 8 * h, 4 * h)], hair)
        flat(c, Circ(hx + 2 * h, hy + 1 * h, 5.6 * h), SKIN)
        flat(c, Circ(hx + 4 * h, hy, 1.1 * h), INK)
    elif style == "twin":
        flat(c, [Ell(hx, hy - 6 * h, 8 * h, 4 * h), Ell(hx - 10 * h, hy + 4 * h, 3.5 * h, 9 * h), Ell(hx + 10 * h, hy + 4 * h, 3.5 * h, 9 * h)], hair)
    else:
        flat(c, Ell(hx - 1 * h, hy - 5 * h, 8 * h, 4 * h), hair)
    if glasses:
        flat(c, [Thick(hx - 2 * h, hy, hx + 6 * h, hy, 1.4)], (40, 40, 50))
    if ears:
        flat(c, [Poly([(hx - 7 * h, hy - 6 * h), (hx - 4 * h, hy - 16 * h), (hx - 1 * h, hy - 8 * h)]),
                 Poly([(hx + 1 * h, hy - 8 * h), (hx + 5 * h, hy - 16 * h), (hx + 8 * h, hy - 6 * h)])], ears)
    return hx, hy


def maid(c, x, base, dress=(40, 40, 60), ribbon=(230, 80, 120), hair=(90, 60, 40), h=1.0, tray=None):
    piece(c, [Poly([(x - 14 * h, base - 10 * h), (x + 14 * h, base - 10 * h), (x + 7 * h, base - 34 * h), (x - 7 * h, base - 34 * h)])], dress, border=1.5,
          shadow=PROP)
    flat(c, [Poly([(x - 9 * h, base - 12 * h), (x + 9 * h, base - 12 * h), (x + 5 * h, base - 30 * h), (x - 5 * h, base - 30 * h)])], (250, 250, 252))
    flat(c, [Ell(x - 14 * h + k * 7 * h, base - 10 * h, 4 * h, 2.5 * h) for k in range(5)], (250, 250, 252))
    flat(c, [RRect(x - 5 * h, base - 10 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 10 * h, x + 5 * h, base, 1)], (30, 30, 36))
    flat(c, Poly([(x - 4 * h, base - 34 * h), (x + 4 * h, base - 34 * h), (x, base - 29 * h)]), ribbon)
    hx, hy = x + 1 * h, base - 42 * h
    flat(c, [Ell(hx - 2 * h, hy, 9 * h, 10 * h)], hair)
    flat(c, Circ(hx + 1 * h, hy + 1 * h, 6.4 * h), SKIN)
    flat(c, Circ(hx + 3 * h, hy, 1.1 * h), INK)
    flat(c, [RRect(hx - 7 * h, hy - 9 * h, hx + 7 * h, hy - 6 * h, 1)], (250, 250, 252))
    if tray:
        flat(c, Thick(x + 6 * h, base - 26 * h, x + 22 * h, base - 32 * h, 1.6), SKIN)
        flat(c, Ell(x + 26 * h, base - 34 * h, 12 * h, 3 * h), (200, 200, 210))
        tray(c, x + 26 * h, base - 36 * h, h)
    return hx, hy


def sign_box(c, x0, y0, x1, y1, col, seed, glyph=(250, 250, 250), vertical=True):
    piece(c, RRect(x0, y0, x1, y1, 2), col, border=1.2, shadow=SMALL)
    rnd = random.Random(seed)
    if vertical:
        y = y0 + 8
        while y < y1 - 14:
            gx = (x0 + x1) / 2
            for _ in range(3):
                a, b = rnd.uniform(-7, 7), rnd.uniform(0, 10)
                flat(c, Thick(gx + a, y + b, gx + rnd.uniform(-7, 7), y + rnd.uniform(0, 10), 2), glyph)
            y += 16
    else:
        x = x0 + 8
        while x < x1 - 14:
            cy = (y0 + y1) / 2
            for _ in range(3):
                flat(c, Thick(x + rnd.uniform(0, 10), cy + rnd.uniform(-7, 7), x + rnd.uniform(0, 10), cy + rnd.uniform(-7, 7), 2), glyph)
            x += 16


def chibi(c, x, base, hair, outfit, s=1.0):
    piece(c, [RRect(x - 6 * s, base - 16 * s, x + 6 * s, base, 2), Circ(x, base - 24 * s, 9 * s)], outfit, border=1, shadow=SMALL)
    flat(c, Circ(x, base - 23 * s, 7.4 * s), SKIN)
    flat(c, [Ell(x, base - 29 * s, 10 * s, 6 * s), Ell(x - 8 * s, base - 20 * s, 3 * s, 8 * s), Ell(x + 8 * s, base - 20 * s, 3 * s, 8 * s)], hair)
    flat(c, [Circ(x - 3 * s, base - 22 * s, 1.6 * s), Circ(x + 3 * s, base - 22 * s, 1.6 * s)], (60, 90, 200))
    flat(c, RRect(x - 8 * s, base - 2 * s, x + 8 * s, base + 2 * s, 1), (250, 250, 252))


# =================================================================== Level 114 the electric town street (day / night)
DN114 = day_night(40.0, tint=(0.28, 0.28, 0.52))
BUILD114 = [(-10, 140, 110, (170, 170, 180)), (140, 290, 70, (200, 190, 170)), (290, 470, 40, (150, 160, 180)), (470, 620, 90, (210, 200, 190)),
            (620, 780, 60, (160, 150, 170)), (780, 910, 100, (190, 180, 160))]
SIGNS114 = [(20, 140, 52, 330, (220, 50, 50)), (200, 90, 232, 300, (250, 200, 50)), (330, 70, 360, 260, (60, 120, 220)),
            (520, 120, 552, 330, (230, 80, 160)), (660, 80, 692, 300, (60, 180, 120)), (820, 130, 852, 330, (250, 140, 40))]
SIGN_DIFF = 3


def l114_bg(c, d):
    sky(c, (160, 200, 236), (240, 230, 220), 360)
    for x0, x1, top, col in BUILD114:
        piece(c, RRect(x0, top, x1, 420, 1), col, border=1.5, shadow=PROP)
        for y in range(top + 20, 400, 30):
            for x in range(x0 + 12, x1 - 16, 26):
                flat(c, RRect(x, y, x + 16, y + 16, 1), (190, 210, 230))
    for i, (x0, y0, x1, y1, col) in enumerate(SIGNS114):
        if i == SIGN_DIFF and "sign" in d:
            col = (60, 200, 220)
        sign_box(c, x0, y0, x1, y1, col, 1140 + i)
    sign_box(c, 300, 300, 460, 330, (40, 40, 60), 1149, glyph=(250, 220, 90), vertical=False)
    # big screen
    piece(c, RRect(560, 150, 760, 260, 3), (40, 40, 46), border=1.5, shadow=PROP)
    flat(c, RRect(568, 158, 752, 252, 1), (90, 180, 230) if "screen" not in d else (240, 120, 160))
    flat(c, Circ(620, 200, 26), (250, 240, 200))
    flat(c, [Ell(690, 230, 40, 14)], (250, 250, 250))
    # railway overpass
    piece(c, RRect(-10, 300, 910, 330, 0), (110, 110, 120), border=1.5, shadow=PROP)
    for x in range(40, 900, 140):
        piece(c, RRect(x - 10, 330, x + 10, 430, 1), (110, 110, 120), shadow=SMALL)
    for x in range(-10, 910, 20):
        flat(c, Thick(x, 300, x + 10, 330, 1.4), (90, 90, 100))
    # shopfronts and street
    for x0, x1, _, col in BUILD114:
        piece(c, RRect(x0 + 6, 430, x1 - 6, 480, 1), lit(col, 0.9), shadow=SMALL)
        flat(c, RRect(x0 + 14, 440, x1 - 14, 480, 0), (220, 230, 240))
    piece(c, RRect(-10, 480, 910, 612, 0), (150, 150, 156), shadow=LAYER)
    for x in range(0, 900, 60):
        flat(c, RRect(x, 540, x + 30, 548, 1), (240, 240, 240))
    piece(c, RRect(30, 420, 70, 480, 3), (220, 60, 60) if "vending" not in d else (60, 120, 200), border=1.2, shadow=PROP)
    for k in range(3):
        for j in range(3):
            flat(c, RRect(36 + j * 11, 428 + k * 12, 44 + j * 11, 436 + k * 12, 1), [(250, 220, 90), (120, 200, 230), (250, 250, 250)][(k + j) % 3])
    flat(c, Thick(860, 600, 860, 470, 4), (60, 60, 70))
    piece(c, RRect(846, 440, 874, 474, 3), (40, 40, 46), shadow=SMALL)
    lamp = (60, 220, 120) if "signal" in d else (230, 60, 50)
    flat(c, Circ(860, 450, 6), lamp)
    flat(c, Circ(860, 464, 6), (60, 70, 70))
    flat(c, Thick(780, 600, 780, 500, 2.5), (110, 110, 120))
    piece(c, Poly([(781, 500), (800, 500), (800, 560), (781, 560)]), (60, 160, 90) if "nobori" in d else (240, 200, 60), shadow=SMALL)
    rnd = random.Random(114)
    for i, x in enumerate(range(120, 760, 64)):
        top = rnd.choice(((60, 80, 140), (200, 60, 70), (240, 240, 240), (90, 140, 90), (50, 50, 56)))
        if i == 4 and "shirt" in d:
            top = (250, 200, 60)
        modern(c, x, 604 - (i % 2) * 10, top, hair=rnd.choice(HAIRS[:3]), bag=(60, 60, 70) if i % 3 == 0 else None, glasses=(i % 4 == 1),
               ears=(240, 180, 200) if (i == 7 and "ears" not in d) else None, h=1.5)


L114_ELEMENTS = [
    cloud_el("cloud0", 300, 50, 0.6, 5, daynight="day"),
    star_field("stars", 114, 20, 60),
    E("train", lambda c, m: (piece(c, RRect(100, 262, 480, 300, 6), (230, 232, 236), border=1.5, shadow=PROP),
                             flat(c, RRect(100, 284, 480, 290, 0), (150, 200, 60)),
                             [flat(c, RRect(x, 268, x + 26, 280, 2), (120, 160, 200)) for x in range(112, 470, 36)]),
      anim=dict(driftVelocity=(160, 0), driftLength=1400, driftStart=-900)),
    E("neon", lambda c, m: soft_union(c, [RRect(x0, y0, x1, y1, 2) for x0, y0, x1, y1, _ in SIGNS114], (255, 200, 150), 0.45, spread=14),
      daynight="night", anim=dict(twinkle=0.15, twinkleSpeed=1.4)),
    window_glow("windows", [(x, y, x + 16, y + 16) for x0, x1, top, _ in BUILD114 for y in range(top + 20, 300, 60) for x in range(x0 + 12, x1 - 16, 52)]),
    E("screen_glow", lambda c, m: soft_union(c, [RRect(568, 158, 752, 252, 2)], (150, 210, 250), 0.4, spread=20), daynight="night"),
]

L114_DIFFS = [
    ("sign", 536, 226, 0),
    ("screen", 660, 205, 0),
    ("vending", 50, 450, 0),
    ("signal", 860, 450, 0),
    ("nobori", 790, 530, 0),
    ("shirt", 376, 562, 0),
    ("ears", 570, 518, 0),
]


# =================================================================== Level 115 maid cafe
def omurice(heart):
    def t(c, x, y, h):
        piece(c, Ell(x, y, 10 * h, 5 * h), (250, 220, 90), shadow=None)
        flat(c, Poly([(x - 3 * h, y - 2 * h), (x + 3 * h, y - 2 * h), (x, y + 2 * h)]), heart)
    return t


def parfait(cherry):
    def t(c, x, y, h):
        piece(c, [Poly([(x - 6 * h, y), (x + 6 * h, y), (x + 4 * h, y - 16 * h), (x - 4 * h, y - 16 * h)])], (250, 230, 240), shadow=None)
        flat(c, [Circ(x - 2 * h, y - 18 * h, 4 * h), Circ(x + 3 * h, y - 19 * h, 4 * h)], (250, 250, 252))
        flat(c, Circ(x, y - 23 * h, 2.6 * h), cherry)
    return t


def l115_bg(c, d):
    c.rect(0, 0, W, H, (250, 220, 230))
    for x in range(0, 900, 30):
        flat(c, RRect(x, 0, x + 15, 420, 0), (252, 230, 238))
    piece(c, RRect(-10, 0, 910, 40, 0), (250, 250, 252), shadow=SMALL)
    for x in (120, 440):
        piece(c, RRect(x, 90, x + 160, 230, 4), (250, 250, 252), border=2, shadow=PROP)
        flat(c, RRect(x + 8, 98, x + 152, 222, 2), (180, 220, 240))
        flat(c, [Thick(x + 80, 98, x + 80, 222, 3), Thick(x + 8, 160, x + 152, 160, 3)], (250, 250, 252))
        piece(c, Poly([(x - 10, 84), (x + 40, 84), (x + 20, 240), (x - 6, 240)]), (240, 160, 190), shadow=SMALL)
        piece(c, Poly([(x + 170, 84), (x + 120, 84), (x + 140, 240), (x + 166, 240)]), (240, 160, 190), shadow=SMALL)
    piece(c, RRect(700, 70, 860, 230, 4), (120, 80, 60), border=2, shadow=PROP)
    flat(c, RRect(708, 78, 852, 222, 2), (50, 70, 60))
    for k in range(5):
        flat(c, Thick(720, 100 + k * 24, 800, 100 + k * 24, 2), (240, 240, 230))
        flat(c, Circ(830, 104 + k * 24, 6), [(250, 200, 90), (240, 120, 160), (120, 200, 230)][k % 3])
    if "menu" in d:
        flat(c, Circ(780, 200, 12), (240, 120, 160))
    piece(c, Circ(620, 60, 22), (250, 250, 252), border=2, shadow=PROP)
    flat(c, [Thick(620, 60, 620, 46, 2), Thick(620, 60, 630, 66, 2)] if "clock" not in d else [Thick(620, 60, 608, 60, 2), Thick(620, 60, 620, 74, 2)], INK)
    # counter and floor
    piece(c, RRect(-10, 420, 910, 612, 0), (200, 160, 130), shadow=LAYER)
    for x in range(0, 900, 60):
        for y in range(420, 600, 30):
            flat(c, RRect(x + ((y // 30) % 2) * 30, y, x + ((y // 30) % 2) * 30 + 30, y + 30, 0), (210, 172, 140))
    piece(c, RRect(-10, 300, 160, 420, 2), (250, 250, 252), border=1.5, shadow=PROP)
    flat(c, RRect(-10, 300, 160, 312, 0), (240, 160, 190))
    # tables with customers
    for i, tx in enumerate((300, 640)):
        piece(c, [Ell(tx, 470, 70, 14), RRect(tx - 6, 470, tx + 6, 540, 2)], (250, 250, 252), border=1.5, shadow=PROP)
        modern(c, tx - 96, 590, (60, 80, 140) if i == 0 else (90, 90, 96), hair=HAIRS[i], glasses=True,
               ears=(240, 180, 200) if (i == 1 and "ears" not in d) else None, h=1.8)
        modern(c, tx + 96, 590, (200, 200, 210), hair=HAIRS[1 + i], bag=(60, 60, 70), h=1.8)
        flat(c, Thick(tx, 456, tx, 430, 2.4), (90, 150, 80))
        piece(c, Circ(tx, 428, 10), (230, 80, 120) if not ("flower" in d and i == 0) else (250, 220, 80), shadow=SMALL)
    omurice((220, 40, 50) if "heart" not in d else (60, 140, 220))(c, 330, 462, 3.0)
    parfait((60, 120, 220) if "cherry" in d else (220, 30, 50))(c, 610, 466, 2.4)
    maid(c, 470, 596, dress=(130, 40, 70) if "ribbon" in d else (40, 40, 60), h=2.0, hair=(220, 180, 90))
    maid(c, 80, 424, h=1.6, hair=(40, 30, 30))
    maid(c, 830, 598, h=1.9, hair=(230, 120, 160))


L115_ELEMENTS = [E("heart%d" % i, (lambda x, y: lambda c, m: flat(c, [Circ(x - 5, y, 6), Circ(x + 5, y, 6), Poly([(x - 11, y + 2), (x + 11, y + 2), (x, y + 14)])],
                                                                  (250, 150, 190, 0.85)))(x, y),
                   anim=dict(driftVelocity=(4, 20), driftLength=60, driftFade=True, phase=i / 4)) for i, (x, y) in enumerate(((470, 500), (500, 490), (800, 500),
                                                                                                                             (830, 510)))] + [
    E("ribbon_bob", lambda c, m: flat(c, [Thick(560, 0, 560, 70, 1.4), Circ(560, 76, 10)], (250, 180, 200)), pivot=(560, 0),
      anim=dict(swingAngle=6, swingSpeed=0.3)),
]

L115_DIFFS = [
    ("menu", 780, 200, 0),
    ("clock", 620, 62, 0),
    ("ears", 546, 488, 0),
    ("flower", 300, 428, 0),
    ("heart", 330, 462, 0),
    ("cherry", 610, 411, 0),
    ("ribbon", 470, 560, 0),
]


# =================================================================== Level 116 figure shop
def l116_bg(c, d):
    c.rect(0, 0, W, H, (236, 236, 240))
    piece(c, RRect(-10, 0, 910, 30, 0), (250, 250, 252), shadow=SMALL)
    # glass cases with figures
    rnd = random.Random(116)
    for ci, (x0, x1) in enumerate(((20, 290), (310, 580))):
        piece(c, RRect(x0, 60, x1, 420, 3), (200, 210, 220), border=2, shadow=PROP)
        flat(c, RRect(x0 + 8, 68, x1 - 8, 412, 1), (230, 240, 248))
        for r, y in enumerate((150, 240, 330, 410)):
            flat(c, RRect(x0 + 8, y, x1 - 8, y + 4, 0), (180, 190, 200))
            for k in range(5):
                x = x0 + 34 + k * (x1 - x0 - 60) / 4
                hair = HAIRS[(ci * 7 + r * 3 + k) % len(HAIRS)]
                if ci == 0 and r == 1 and k == 2 and "figure" in d:
                    hair = (60, 200, 120)
                chibi(c, x, y, hair, rnd.choice(((240, 120, 160), (90, 120, 200), (250, 250, 250), (60, 60, 70))), s=1.2)
        flat(c, Thick(x0 + 20, 70, x0 + 60, 400, 3), (250, 250, 255, 0.5))
    # model kit boxes, a big robot statue
    for k in range(5):
        for j in range(3):
            col = [(60, 90, 160), (200, 60, 60), (240, 200, 60), (90, 150, 90)][(k + j) % 4]
            if k == 2 and j == 1 and "box" in d:
                col = (160, 90, 200)
            piece(c, RRect(610 + j * 92, 70 + k * 56, 694 + j * 92, 120 + k * 56, 2), col, border=1.2, shadow=SMALL)
            flat(c, RRect(620 + j * 92, 80 + k * 56, 660 + j * 92, 110 + k * 56, 1), (250, 250, 252))
    # capsule machines wall
    for k in range(6):
        x = 610 + k * 48
        piece(c, [RRect(x, 380, x + 40, 470, 3), Circ(x + 20, 360, 22)], (230, 230, 236), border=1.2, shadow=PROP)
        flat(c, Circ(x + 20, 360, 18), (250, 220, 236) if (k == 3 and "capsule" in d) else (220, 236, 250))
        for j in range(5):
            cap = [(240, 120, 160), (120, 200, 230), (250, 220, 90), (130, 210, 130)][(k + j) % 4]
            flat(c, Circ(x + 10 + (j % 3) * 10, 352 + (j // 3) * 12, 5), cap)
        flat(c, Circ(x + 20, 430, 6), (180, 180, 190))
    piece(c, RRect(-10, 470, 910, 612, 0), (200, 200, 210), shadow=LAYER)
    piece(c, [RRect(110, 470, 190, 490, 2), RRect(130, 400, 170, 470, 4), RRect(126, 360, 174, 404, 6), RRect(138, 334, 162, 362, 4)], (240, 240, 246),
          border=1.5, shadow=PROP)
    flat(c, [RRect(130, 370, 170, 380, 0), Circ(150, 346, 4)], (60, 100, 200))
    flat(c, [RRect(130, 370, 170, 380, 0)], (220, 60, 60) if "horn" in d else (60, 100, 200))
    flat(c, Poly([(142, 334), (150, 314), (158, 334)]), (240, 200, 60))
    hx, hy = modern(c, 400, 596, (60, 60, 70), hair=(40, 30, 30), bag=(200, 60, 60) if "backpack" not in d else (60, 140, 90), glasses=True, h=1.4)
    modern(c, 520, 598, (240, 180, 200), bottom=(220, 120, 160) if "skirt" in d else (60, 70, 100), hair=(220, 180, 90), style="twin", skirt=True, h=1.3)
    modern(c, 760, 600, (90, 140, 200), hair=(90, 60, 40), h=1.4)
    piece(c, RRect(820, 500, 880, 540, 2), (250, 230, 120) if "tag" in d else (250, 250, 252), border=1, shadow=SMALL)
    flat(c, Thick(830, 520, 870, 520, 2), (220, 50, 60))


L116_ELEMENTS = [
    E("sparkle%d" % i, (lambda x, y: lambda c, m: flat(c, Poly(star_pts(x, y, 6, 1.8, points=4, rot=0)), (255, 255, 255)))(x, y),
      anim=dict(twinkle=0.95, twinkleSpeed=0.6 + i * 0.1, phase=i * 0.2)) for i, (x, y) in enumerate(((60, 100), (300, 180), (420, 300), (560, 120),
                                                                                                         (240, 380)))]

L116_DIFFS = [
    ("figure", 155, 225, 0),
    ("box", 794, 208, 0),
    ("capsule", 774, 366, 0),
    ("horn", 150, 375, 0),
    ("backpack", 388, 552, 0),
    ("tag", 850, 520, 0),
    ("skirt", 520, 580, 0),
]


# =================================================================== Level 117 arcade at night
def plush(c, x, y, col, s=1.0):
    piece(c, [Circ(x, y, 10 * s), Circ(x - 7 * s, y - 8 * s, 4 * s), Circ(x + 7 * s, y - 8 * s, 4 * s)], col, shadow=None)
    flat(c, [Circ(x - 3 * s, y - 1 * s, 1.4 * s), Circ(x + 3 * s, y - 1 * s, 1.4 * s), Ell(x, y + 3 * s, 3 * s, 2 * s)], INK)


def cabinet(c, x0, x1, base, top, body, screen, marquee):
    piece(c, Poly([(x0, base), (x1, base), (x1, top + 40), (x1 - 10, top), (x0, top)]), body, border=1.5, shadow=PROP)
    flat(c, RRect(x0 + 8, top + 6, x1 - 18, top + 24, 2), marquee)
    flat(c, RRect(x0 + 10, top + 34, x1 - 16, top + 100, 2), screen)
    flat(c, RRect(x0 + 6, top + 106, x1 - 4, top + 124, 1), lit(body, 0.8))
    for k in range(4):
        flat(c, Circ(x0 + 18 + k * 12, top + 115, 3.5), [(230, 60, 60), (250, 220, 60), (60, 140, 230), (90, 200, 120)][k])


def l117_bg(c, d):
    c.rect(0, 0, W, H, (34, 28, 50))
    for y in (24, 40):
        flat(c, Thick(0, y, 900, y, 3), (60, 50, 80))
    for x0, y0, x1, y1, col in ((40, 60, 240, 90, (250, 80, 160)), (340, 60, 520, 90, (80, 220, 250)), (600, 60, 860, 90, (250, 200, 60))):
        if x0 == 340 and "neon" in d:
            col = (120, 250, 120)
        piece(c, RRect(x0, y0, x1, y1, 4), (40, 34, 60), shadow=None)
        neon_glyphs_box(c, x0, y0, x1, y1, col)
    # claw machines
    for k, x0 in enumerate((20, 160)):
        piece(c, RRect(x0, 160, x0 + 130, 470, 4), (240, 120, 170) if k == 0 else (110, 170, 240), border=1.5, shadow=PROP)
        flat(c, RRect(x0 + 10, 180, x0 + 120, 360, 2), (200, 220, 240))
        for j, (px, py) in enumerate(((30, 340), (56, 344), (84, 338), (108, 344), (44, 324), (96, 322), (70, 322))):
            col = [(250, 220, 120), (240, 170, 200), (180, 220, 250), (250, 250, 250)][(j + k) % 4]
            if k == 0 and j == 4 and "plush" in d:
                col = (120, 220, 140)
            plush(c, x0 + px, py, col)
        flat(c, RRect(x0 + 10, 360, x0 + 120, 380, 0), lit((240, 120, 170) if k == 0 else (110, 170, 240), 0.8))
        flat(c, [RRect(x0 + 30, 400, x0 + 100, 420, 3)], (40, 34, 50))
        flat(c, Circ(x0 + 50, 410, 6), (230, 60, 60))
    # drum game
    piece(c, RRect(330, 200, 500, 470, 4), (230, 120, 40), border=1.5, shadow=PROP)
    flat(c, RRect(345, 220, 485, 320, 2), (60, 200, 220) if "screen" not in d else (250, 120, 160))
    for x in (380, 450):
        piece(c, [Ell(x, 400, 30, 12), RRect(x - 30, 400, x + 30, 440, 4)], (200, 60, 50) if not ("drum" in d and x == 450) else (60, 120, 200),
              border=1.2, shadow=SMALL)
        flat(c, Ell(x, 400, 24, 8), (250, 240, 220))
    # fighting cabinets with players
    for x0 in (530, 630):
        cabinet(c, x0, x0 + 90, 470, 200, (40, 40, 60), (120, 90, 200), (250, 200, 60))
        flat(c, RRect(x0 + 20, 420, x0 + 70, 432, 2), (60, 60, 80))
    if "coins" not in d:
        for k in range(4):
            flat(c, Ell(610, 196 - k * 3, 8, 3), (240, 200, 60))
    # photo booth
    piece(c, RRect(730, 160, 900, 470, 4), (250, 230, 240), border=1.5, shadow=PROP)
    sign_box(c, 750, 170, 880, 200, (240, 120, 170), 1171, vertical=False)
    curtain = (120, 200, 160) if "curtain" in d else (230, 90, 140)
    for k in range(6):
        piece(c, RRect(752 + k * 21, 220, 772 + k * 21, 440, 2), curtain if k % 2 else lit(curtain, 1.1), shadow=None)
    piece(c, RRect(-10, 470, 910, 612, 0), (60, 50, 90), shadow=LAYER)
    rnd = random.Random(117)
    for _ in range(60):
        x, y = rnd.uniform(0, 900), rnd.uniform(480, 600)
        flat(c, Poly(star_pts(x, y, 5, 2, points=4, rot=0)), rnd.choice(((250, 120, 180), (100, 220, 250), (250, 220, 90))))
    hx, hy = modern(c, 575, 560, (200, 60, 70), hair=(40, 30, 30), h=1.6)
    flat(c, [Ell(hx, hy - 7, 12, 5), RRect(hx - 2, hy - 7, hx + 16, hy - 3, 1)], (60, 140, 220) if "cap" in d else (30, 30, 34))
    modern(c, 675, 560, (240, 240, 240), hair=(220, 180, 90), h=1.6, style="long")
    modern(c, 120, 596, (90, 90, 110), hair=(90, 60, 40), bag=(240, 120, 170), h=1.4)
    modern(c, 420, 598, (240, 180, 60), hair=(40, 30, 30), h=1.4, glasses=True)


def neon_glyphs_box(c, x0, y0, x1, y1, col):
    soft_union(c, [RRect(x0 + 4, y0 + 4, x1 - 4, y1 - 4, 3)], col, 0.4, spread=10)
    rnd = random.Random(int(x0 * 3 + y0))
    x = x0 + 12
    while x < x1 - 16:
        cy = (y0 + y1) / 2
        for _ in range(3):
            flat(c, Thick(x + rnd.uniform(0, 12), cy + rnd.uniform(-8, 8), x + rnd.uniform(0, 12), cy + rnd.uniform(-8, 8), 2.4), lit(col, 1.2))
        x += 18


def l117_claw(i, x):
    def d(c, m):
        flat(c, Thick(x, 180, x, 250, 1.4), (200, 200, 210))
        piece(c, [RRect(x - 8, 250, x + 8, 258, 2), Thick(x - 6, 258, x - 12, 272, 2), Thick(x + 6, 258, x + 12, 272, 2)], (210, 210, 220), shadow=None)
    return E("claw%d" % i, d, pivot=(x, 180), anim=dict(swingAngle=8, swingSpeed=0.25 + i * 0.05, bobAmplitude=(20, 0), bobSpeed=0.08))


L117_ELEMENTS = [l117_claw(0, 85), l117_claw(1, 225)] + [
    E("screen_flicker%d" % i, (lambda x0, x1: lambda c, m: flat(c, RRect(x0 + 10, 234, x1 - 16, 300, 2), (255, 255, 255, 0.25)))(x0, x0 + 90),
      anim=dict(twinkle=0.9, twinkleSpeed=1.6 + i * 0.4)) for i, x0 in enumerate((530, 630))] + [
    E("drummer", lambda c, m: flat(c, Thick(420, 520, 400, 470, 3), (250, 226, 204)), pivot=(420, 520), anim=dict(swingAngle=24, swingSpeed=1.4)),
    E("neon_pulse", lambda c, m: soft_union(c, [RRect(40, 60, 240, 90, 4), RRect(600, 60, 860, 90, 4)], (250, 120, 200), 0.3, spread=20),
      anim=dict(twinkle=0.6, twinkleSpeed=0.8)),
]

L117_DIFFS = [
    ("neon", 430, 75, 0),
    ("plush", 64, 324, 0),
    ("screen", 415, 270, 0),
    ("drum", 450, 412, 0),
    ("cap", 580, 476, 0),
    ("coins", 610, 190, 0),
    ("curtain", 815, 330, 0),
]


# =================================================================== Level 118 pedestrian paradise
SIGNS118 = [(30, 60, 62, 280, (60, 120, 220)), (170, 40, 202, 260, (230, 80, 160)), (420, 70, 452, 290, (250, 200, 50)), (640, 50, 672, 270, (220, 50, 50)),
            (800, 80, 832, 300, (60, 180, 120))]


def l118_bg(c, d):
    sky(c, (160, 204, 240), (240, 232, 220), 340)
    for x0, x1, top, col in ((-10, 150, 30, (190, 190, 200)), (150, 300, 10, (210, 200, 180)), (300, 560, 60, (170, 180, 200)),
                             (560, 760, 20, (200, 190, 200)), (760, 910, 50, (180, 170, 160))):
        piece(c, RRect(x0, top, x1, 430, 1), col, border=1.5, shadow=PROP)
        for y in range(top + 20, 400, 30):
            for x in range(x0 + 12, x1 - 16, 26):
                flat(c, RRect(x, y, x + 16, y + 16, 1), (190, 210, 230))
    for i, (x0, y0, x1, y1, col) in enumerate(SIGNS118):
        sign_box(c, x0, y0, x1, y1, (90, 200, 220) if (i == 2 and "sign" in d) else col, 1180 + i)
    piece(c, RRect(-10, 430, 910, 612, 0), (170, 170, 176), shadow=LAYER)
    for x in range(0, 900, 60):
        flat(c, RRect(x, 500, x + 30, 506, 1), (240, 240, 240))
    # cosplayers and the crowd
    hx, hy = modern(c, 120, 590, (250, 250, 252), bottom=(230, 120, 160), hair=(240, 240, 246), style="long", skirt=True, h=1.5)
    wing = (120, 200, 250) if "wings" in d else (250, 250, 252)
    piece(c, [Poly([(110, 540), (60, 500), (70, 540), (56, 566), (108, 556)]), Poly([(132, 540), (182, 500), (172, 540), (186, 566), (134, 556)])], wing,
          border=1.2, shadow=PROP)
    modern(c, 240, 592, (90, 90, 120), bottom=(60, 60, 80), hair=(40, 30, 30), h=1.5)
    if "sword" not in d:
        flat(c, Thick(256, 560, 290, 470, 4), (220, 226, 236))
        flat(c, Thick(250, 572, 262, 552, 5), (90, 60, 40))
    modern(c, 360, 594, (240, 180, 200), bottom=(40, 40, 60), hair=(90, 160, 230) if "wig" in d else (240, 120, 170), style="twin", skirt=True, h=1.5)
    hx, hy = modern(c, 470, 596, (60, 70, 60), hair=(40, 30, 30), h=1.5)
    flat(c, [Ell(hx, hy - 7, 12, 5), RRect(hx - 2, hy - 7, hx + 16, hy - 4, 1)], (200, 60, 60) if "cap" in d else (40, 40, 46))
    piece(c, RRect(hx + 8, hy + 10, hx + 26, hy + 24, 2), (40, 40, 46), shadow=SMALL)
    flat(c, Circ(hx + 22, hy + 17, 5), (120, 140, 170))
    maid(c, 600, 594, h=1.5, hair=(90, 60, 40))
    piece(c, RRect(630, 520, 652, 548, 1), (250, 220, 90) if "flyer" in d else (240, 140, 180), border=1, shadow=SMALL)
    rnd = random.Random(118)
    for x in range(700, 900, 40):
        modern(c, x, 600, rnd.choice(((60, 80, 140), (200, 60, 70), (240, 240, 240), (90, 140, 90))), hair=rnd.choice(HAIRS[:3]), h=1.3)
    flat(c, Thick(860, 560, 860, 470, 1.2), (110, 110, 120))
    piece(c, Ell(860, 456, 16, 20), (90, 160, 230) if "balloon" in d else (240, 80, 120), border=1.2, shadow=SMALL)


L118_ELEMENTS = [cloud_el("cloud0", 300, 40, 0.6, 5)] + [
    E("ball%d" % i, (lambda col: lambda c, m: piece(c, Circ(780, 470, 6), col, shadow=None))(col), pivot=(780, 470),
      anim=dict(orbitRadius=(16, 30), orbitSpeed=0.6, phase=i / 3)) for i, col in enumerate(((250, 80, 80), (80, 160, 250), (250, 220, 60)))] + [
    E("flash", lambda c, m: soft_union(c, [Circ(530, 512, 10)], (255, 255, 240), 0.8, spread=16), anim=dict(blinkInterval=3.0, blinkDuration=0.3)),
]

L118_DIFFS = [
    ("sign", 436, 180, 0),
    ("wings", 120, 530, 0),
    ("sword", 274, 500, 0),
    ("wig", 361, 520, 0),
    ("cap", 474, 520, 0),
    ("flyer", 641, 534, 0),
    ("balloon", 860, 456, 0),
]

LEVELS = [
    ("Level114", "秋叶原电器街", l114_bg, L114_ELEMENTS, L114_DIFFS, 140, dict(OPTS, day_night=DN114, anim_seconds=40.0, frames=80)),
    ("Level115", "女仆咖啡厅", l115_bg, L115_ELEMENTS, L115_DIFFS, 140, OPTS),
    ("Level116", "手办店", l116_bg, L116_ELEMENTS, L116_DIFFS, 140, OPTS),
    ("Level117", "游戏中心", l117_bg, L117_ELEMENTS, L117_DIFFS, 140, OPTS),
    ("Level118", "步行者天国", l118_bg, L118_ELEMENTS, L118_DIFFS, 140, OPTS),
]
