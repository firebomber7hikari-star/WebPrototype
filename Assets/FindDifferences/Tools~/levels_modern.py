# -*- coding: utf-8 -*-
"""Modern life themes (paper-craft side views, full-bleed, no real brands or logos):
  Level130 体育比赛 - a football match: stands full of fans, scoreboard, floodlights, players on the pitch
  Level131 演唱会   - a night concert: truss and spotlights, LED wall, the band, a crowd with glow sticks
  Level132 大型展览 - an expo hall: steel roof, a concept car on a turntable, robot arm demo, giant globe, booths
  Level133 加油站   - a roadside gas station with canopy, pumps, price pylon and shop; day / night
  Level134 商场     - a shopping-mall atrium: three floors of shops, escalators, glass roof, fountain
  Level135 未来世界 - a future city: domed towers, maglev, flying cars, hologram, robots in a garden plaza
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_bg, cloud_el, drift_across, sky, spin_el
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from stylekit import day_night, star_field, window_glow
from levels_akiba import modern, sign_box, HAIRS
from levels_misc import seg_text

NIGHT_EDGE = (120, 110, 140)
OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def dpiece(c, shapes, col, border=1.5, shadow=PROP):
    """Paper piece for dark scenes: cut edge in a muted tone instead of glowing white."""
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


def crowd(c, x0, x1, y, rows, seed, step=13, dy=16, cols=None, body=None):
    """Rows of spectators seen from the front: shoulders + heads."""
    rnd = random.Random(seed)
    cols = cols or [(220, 60, 60), (60, 110, 200), (250, 250, 250), (250, 200, 60), (60, 160, 90), (40, 40, 50)]
    for r in range(rows):
        yy = y + r * dy
        off = (r % 2) * step / 2
        x = x0 + off
        while x < x1:
            col = body or rnd.choice(cols)
            flat(c, Ell(x, yy + 7, 6, 6), col)
            flat(c, Circ(x, yy - 1, 4.2), (246, 214, 186) if rnd.random() < 0.8 else (170, 120, 90))
            if rnd.random() < 0.35:
                flat(c, Ell(x, yy - 4, 4.4, 2.4), rnd.choice(HAIRS[:3]))
            x += step * rnd.uniform(0.85, 1.15)


def player(c, x, base, shirt, shorts=(250, 250, 250), socks=None, h=1.0, number=None, hair=(40, 30, 30), skin=(246, 214, 186)):
    """Footballer, standing / running pose."""
    socks = socks or shirt
    flat(c, [RRect(x - 6 * h, base - 22 * h, x - 1 * h, base - 2 * h, 1), RRect(x + 1 * h, base - 22 * h, x + 6 * h, base - 2 * h, 1)], skin)
    piece(c, [RRect(x - 6 * h, base - 12 * h, x - 1 * h, base - 2 * h, 1), RRect(x + 1 * h, base - 12 * h, x + 6 * h, base - 2 * h, 1)], socks, shadow=SMALL)
    flat(c, [Ell(x - 4 * h, base - 1 * h, 5 * h, 2.4 * h), Ell(x + 5 * h, base - 1 * h, 5 * h, 2.4 * h)], (30, 30, 36))
    piece(c, RRect(x - 8 * h, base - 28 * h, x + 8 * h, base - 19 * h, 2), shorts, border=1.2, shadow=SMALL)
    piece(c, [RRect(x - 9 * h, base - 46 * h, x + 9 * h, base - 27 * h, 3), RRect(x - 13 * h, base - 45 * h, x - 7 * h, base - 36 * h, 2),
              RRect(x + 7 * h, base - 45 * h, x + 13 * h, base - 36 * h, 2)], shirt, border=1.5, shadow=PROP)
    if number:
        seg_text(c, x - 3 * h, base - 42 * h, 9 * h, number, (250, 250, 250) if sum(shirt) < 450 else (40, 40, 50), width=1.6 * h)
    hx, hy = x + 1 * h, base - 53 * h
    flat(c, Circ(hx, hy, 7 * h), skin)
    flat(c, Ell(hx - 1 * h, hy - 5 * h, 8 * h, 4 * h), hair)
    flat(c, Circ(hx + 3 * h, hy, 1.1 * h), INK)
    return hx, hy


# =================================================================== Level 130 football match
TEAM_A, TEAM_B = (220, 50, 60), (60, 110, 210)


def l130_bg(c, d):
    sky(c, (120, 180, 236), (210, 230, 246), 140)
    # far stand roof + floodlight towers
    piece(c, Poly([(-10, 40), (910, 40), (910, 62), (-10, 62)]), (200, 204, 214), border=1.5, shadow=PROP)
    for x in range(10, 900, 40):
        flat(c, Thick(x, 40, x + 20, 62, 1.6), (170, 174, 186))
    for tx in (70, 830):
        piece(c, [RRect(tx - 5, 0, tx + 5, 60, 1)], (150, 154, 166), shadow=SMALL)
        piece(c, RRect(tx - 34, 2, tx + 34, 34, 3), (60, 64, 76), border=1.5, shadow=PROP)
        for j in range(4):
            for i in range(2):
                lamp = (250, 250, 230)
                if tx == 830 and "lamp" in d and j < 2:
                    lamp = (80, 84, 96)
                flat(c, RRect(tx - 30 + j * 15, 6 + i * 14, tx - 18 + j * 15, 16 + i * 14, 2), lamp)
    # stands: tiers with the crowd
    piece(c, RRect(-10, 62, 910, 252, 0), (130, 136, 150), shadow=LAYER)
    for k, y in enumerate(range(66, 250, 16)):
        flat(c, RRect(-10, y, 910, y + 15, 0), (150, 156, 170) if k % 2 else (140, 146, 160))
    crowd(c, -6, 906, 72, 11, 130)
    # stairways and exits
    for x in (230, 680):
        flat(c, RRect(x - 10, 62, x + 10, 252, 0), (170, 172, 180))
        for y in range(66, 250, 8):
            flat(c, Thick(x - 10, y, x + 10, y, 1), (150, 152, 160))
    # scoreboard
    piece(c, RRect(340, 70, 560, 150, 4), (40, 42, 52), border=2, shadow=PROP)
    flat(c, RRect(350, 80, 550, 140, 2), (24, 26, 34))
    flat(c, [RRect(362, 94, 400, 126, 3)], TEAM_A)
    flat(c, [RRect(500, 94, 538, 126, 3)], (60, 190, 110) if "score" in d else TEAM_B)
    seg_text(c, 418, 92, 34, "2", (255, 200, 60), width=4)
    flat(c, [Circ(450, 102, 3), Circ(450, 118, 3)], (255, 200, 60))
    seg_text(c, 462, 92, 34, "1", (255, 200, 60), width=4)
    # fan banners in the stands
    piece(c, RRect(60, 150, 190, 186, 2), TEAM_A, border=1.2, shadow=SMALL)
    flat(c, [Thick(76, 168, 174, 168, 6)], (250, 250, 250))
    piece(c, RRect(730, 160, 860, 196, 2), (250, 210, 60) if "banner" in d else TEAM_B, border=1.2, shadow=SMALL)
    flat(c, [Poly(star_pts(760 + k * 34, 178, 10, 4)) for k in range(3)], (250, 250, 250))
    # advertising boards (abstract glyphs, no brands)
    for i, x in enumerate(range(-10, 910, 150)):
        col = [(240, 120, 40), (40, 170, 120), (60, 90, 200), (220, 60, 110), (250, 200, 60), (120, 80, 200), (60, 160, 220)][i % 7]
        piece(c, RRect(x + 2, 252, x + 148, 280, 1), col, border=1, shadow=SMALL)
        sign_box(c, x + 20, 258, x + 130, 274, lit(col, 0.8), 1300 + i, vertical=False)
    # pitch
    c.rect(0, 280, W, H, (90, 170, 80))
    for k, x in enumerate(range(-60, 960, 90)):
        if k % 2:
            flat(c, Poly([(x, 280), (x + 90, 280), (x + 120, 600), (x + 30, 600)]), (100, 182, 88))
    flat(c, [Thick(0, 296, W, 296, 3)], (245, 250, 240))
    c.ellipse_ring(560, 420, 120, 46, 3, (245, 250, 240))
    flat(c, Thick(560, 296, 560, 600, 3), (245, 250, 240))
    flat(c, [Thick(0, 330, 210, 330, 3), Thick(210, 330, 250, 560, 3), Thick(250, 560, 0, 560, 3)], (245, 250, 240))
    # goal (left)
    piece(c, [RRect(14, 300, 22, 420, 1), RRect(14, 300, 150, 308, 1), RRect(142, 300, 150, 420, 1)], (250, 250, 250), border=0, shadow=PROP)
    for x in range(26, 140, 10):
        flat(c, Thick(x, 308, x, 418, 1), (230, 236, 236, 0.7))
    for y in range(316, 418, 10):
        flat(c, Thick(22, y, 142, y, 1), (230, 236, 236, 0.7))
    # goalkeeper
    player(c, 84, 452, (60, 200, 220) if "keeper" in d else (250, 220, 40), shorts=(40, 40, 50), h=1.8, hair=(70, 50, 30))
    flat(c, [Circ(58, 378, 7), Circ(112, 378, 7)], (240, 240, 240))                     # gloves
    # players
    player(c, 300, 520, TEAM_A, h=2.1, number="9")
    player(c, 420, 470, TEAM_B, h=1.9, number="4", hair=(200, 160, 90))
    player(c, 640, 560, TEAM_A, h=2.3, number="7", hair=(90, 60, 40))
    player(c, 740, 440, TEAM_B, h=1.7, number="2")
    # referee
    player(c, 520, 380, (230, 120, 170) if "ref" in d else (30, 30, 36), shorts=(30, 30, 36), h=1.6)
    piece(c, RRect(530, 278, 544, 296, 1), (250, 220, 40), shadow=SMALL)                 # card raised high
    flat(c, Thick(529, 302, 536, 292, 3), (246, 214, 186))
    # ball at the striker's feet
    if "ball" not in d:
        piece(c, Circ(338, 514, 13), (250, 250, 250), border=0, shadow=SMALL)
        flat(c, [Poly([(334, 506), (342, 506), (345, 514), (338, 520), (331, 514)])], (40, 40, 46))
    # corner flag (right)
    flat(c, Thick(860, 600, 860, 506, 3), (240, 240, 240))
    piece(c, Poly([(861, 506), (898, 522), (861, 542)]), (60, 200, 90) if "flag" in d else (250, 120, 30), shadow=SMALL)


L130_ELEMENTS = [
    E("fanflag1", lambda c, m: (flat(c, Thick(300, 200, 300, 140, 2.4), (80, 70, 60)),
                               piece(c, Poly([(301, 140), (346, 148), (301, 162)]), TEAM_A, border=1, shadow=SMALL)),
      pivot=(300, 200), anim=dict(swingAngle=14, swingSpeed=0.7)),
    E("fanflag2", lambda c, m: (flat(c, Thick(620, 210, 620, 150, 2.4), (80, 70, 60)),
                               piece(c, Poly([(621, 150), (666, 158), (621, 172)]), TEAM_B, border=1, shadow=SMALL)),
      pivot=(620, 210), anim=dict(swingAngle=14, swingSpeed=0.6, phase=0.4)),
    E("juggle", lambda c, m: (piece(c, Circ(790, 360, 10), (250, 250, 250), shadow=SMALL),
                             flat(c, Circ(787, 357, 3.6), (40, 40, 46))),
      pivot=(790, 370), anim=dict(bobAmplitude=(0, 26), bobSpeed=1.1, bounce=True)),
    bird_el("gull", 450, 24, s=8, speed=28),
]

L130_DIFFS = [
    ("score", 519, 110, 0),
    ("banner", 795, 178, 0),
    ("keeper", 84, 400, 0),
    ("ref", 520, 350, 0),
    ("ball", 338, 514, 0),
    ("flag", 878, 524, 0),
    ("lamp", 818, 18, 0),
]


# =================================================================== Level 131 concert (night)
STAGE_Y = 400


def l131_bg(c, d):
    c.gradient(0, H, (18, 16, 40), (40, 26, 60))
    far_skyline(c, 300, 40, 140, (34, 30, 56), 1311, win=(90, 80, 120))
    # truss frame
    for x in (40, 860):
        dpiece(c, [RRect(x - 12, 30, x + 12, STAGE_Y, 1)], (110, 110, 124))
        for y in range(36, STAGE_Y, 22):
            flat(c, [Thick(x - 10, y, x + 10, y + 20, 1.6), Thick(x + 10, y, x - 10, y + 20, 1.6)], (80, 80, 92))
    dpiece(c, RRect(28, 26, 872, 52, 1), (110, 110, 124))
    for x in range(30, 870, 22):
        flat(c, [Thick(x, 28, x + 20, 50, 1.6), Thick(x + 20, 28, x, 50, 1.6)], (80, 80, 92))
    # lamps on the truss
    for i, x in enumerate(range(110, 820, 90)):
        dpiece(c, [RRect(x - 10, 52, x + 10, 70, 3)], (50, 50, 60), border=1)
        col = [(255, 80, 120), (80, 200, 255), (255, 220, 80), (160, 100, 255)][i % 4]
        if i == 6 and "lamp" in d:
            col = (80, 255, 120)
        flat(c, Circ(x, 72, 9), col)
    # LED wall
    dpiece(c, RRect(250, 90, 650, 290, 3), (30, 30, 40))
    scr = (60, 30, 120)
    flat(c, RRect(258, 98, 642, 282, 2), scr)
    for k in range(7):          # concentric glow rings that stay inside the panel
        flat(c, Ell(450, 190, 186 - k * 26, 88 - k * 12), [(90, 40, 170), (140, 60, 200), (200, 80, 210), (250, 130, 210)][k % 4])
    for k in range(12):         # light rays
        a = math.radians(k * 30 + 15)
        flat(c, Thick(450 + math.cos(a) * 70, 190 + math.sin(a) * 34, 450 + math.cos(a) * 180, 190 + math.sin(a) * 84, 3), (255, 200, 240, 0.6))
    if "screen" in d:
        flat(c, Circ(450, 190, 52), (255, 220, 90))
        flat(c, Circ(450, 190, 40), (255, 240, 170))
    else:
        flat(c, [Ell(450, 190, 60, 24)], (255, 180, 240))
        flat(c, [Ell(450, 190, 24, 60)], (255, 180, 240))
    # speaker stacks
    for x0 in (66, 742):
        for k in range(3):
            y = 180 + k * 72
            dpiece(c, RRect(x0, y, x0 + 92, y + 68, 3), (36, 36, 44))
            flat(c, [Circ(x0 + 46, y + 40, 20), Circ(x0 + 46, y + 14, 8)], (60, 60, 70))
            flat(c, [Circ(x0 + 46, y + 40, 8)], (26, 26, 32))
    if "speaker" in d:
        flat(c, RRect(742, 180, 834, 248, 3), (40, 26, 60))          # top-right speaker removed (wall shows)
    # stage floor and front
    dpiece(c, RRect(-10, STAGE_Y, 910, STAGE_Y + 30, 0), (50, 46, 66))
    flat(c, RRect(-10, STAGE_Y + 30, 910, STAGE_Y + 70, 0), (30, 28, 42))
    for x in range(0, 900, 60):
        flat(c, RRect(x + 4, STAGE_Y + 36, x + 50, STAGE_Y + 44, 2), (255, 220, 120, 0.6))
    # drum riser (right of centre): drummer behind the kit
    dpiece(c, RRect(480, 352, 640, STAGE_Y, 2), (60, 56, 80))
    for x in range(486, 640, 22):
        flat(c, RRect(x, 360, x + 14, 366, 1), (255, 220, 120, 0.5))
    modern(c, 560, 352, (40, 40, 50), h=1.4, hair=(200, 60, 60))
    dpiece(c, [Ell(560, 360, 30, 20)], (250, 250, 252))
    flat(c, Ell(560, 360, 23, 15), (200, 40, 70) if "drum" in d else (40, 40, 60))
    for x in (510, 610):
        dpiece(c, [Ell(x, 334, 16, 9), RRect(x - 16, 334, x + 16, 354, 2)], (200, 200, 210))
        flat(c, Thick(x, 306, x, 318, 2), (180, 180, 190))
        flat(c, Ell(x + (-12 if x < 560 else 12), 304, 20, 4), (230, 200, 80))
    # singer (front, left of centre) with mic stand
    flat(c, Thick(392, STAGE_Y, 392, 330, 2.5), (180, 180, 190))
    flat(c, Ell(392, 330, 4, 6), (60, 60, 70))
    modern(c, 370, STAGE_Y, (250, 250, 250) if "outfit" in d else (200, 30, 80), bottom=(30, 30, 40), hair=(250, 220, 120), h=2.0, style="long")
    # guitarist (left) and bassist (right)
    modern(c, 200, STAGE_Y, (40, 40, 50), hair=(30, 30, 30), h=1.9)
    guitar = (60, 180, 240) if "guitar" in d else (230, 120, 40)
    piece(c, [Ell(196, STAGE_Y - 44, 15, 11), Thick(206, STAGE_Y - 48, 244, STAGE_Y - 74, 4)], guitar, border=1, border_col=NIGHT_EDGE, shadow=SMALL)
    modern(c, 700, STAGE_Y, (90, 40, 120), hair=(220, 220, 230), h=1.9)
    piece(c, [Ell(704, STAGE_Y - 44, 15, 11), Thick(694, STAGE_Y - 48, 656, STAGE_Y - 76, 4)], (30, 30, 40), border=1, border_col=NIGHT_EDGE,
          shadow=SMALL)
    # crowd silhouettes in the foreground
    rnd = random.Random(1310)
    shapes = []
    x = -20
    while x < 920:
        hh = rnd.uniform(0.9, 1.3)
        shapes += [Circ(x, 520 - 28 * hh, 14 * hh), RRect(x - 22 * hh, 520 - 16 * hh, x + 22 * hh, 620, 10 * hh)]
        x += rnd.uniform(34, 50)
    flat(c, shapes, (14, 12, 26))
    rnd = random.Random(1312)
    shapes = []
    x = 0
    while x < 920:
        hh = rnd.uniform(1.1, 1.5)
        shapes += [Circ(x, 580 - 28 * hh, 15 * hh), RRect(x - 24 * hh, 580 - 16 * hh, x + 24 * hh, 640, 10 * hh)]
        x += rnd.uniform(40, 60)
    flat(c, shapes, (8, 6, 16))
    # a fan's banner held up (static)
    dpiece(c, RRect(560, 470, 650, 500, 2), (255, 120, 180) if "sign" not in d else (120, 255, 160), border=1)
    flat(c, [Thick(574, 485, 636, 485, 4)], (250, 250, 250))
    flat(c, [Thick(570, 500, 566, 530, 3), Thick(640, 500, 644, 530, 3)], (14, 12, 26))


def beam(x, y, ang, length, col, width=40):
    a = math.radians(ang)
    dx, dy = math.sin(a), math.cos(a)
    ex, ey = x + dx * length, y + dy * length
    px, py = dy * width, -dx * width
    return lambda c, m: soft_union(c, [Poly([(x - 3, y), (x + 3, y), (ex + px, ey + py), (ex - px, ey - py)])], col, 0.18, spread=10)


L131_ELEMENTS = [
    # beams from the outer truss columns, swinging outwards only (they never cross the stage or the speaker stacks)
    E("beam1", beam(40, 56, -16, 340, (255, 80, 120), width=26), pivot=(40, 56), daynight="untinted", anim=dict(swingAngle=8, swingSpeed=0.25)),
    E("beam2", beam(860, 56, 16, 340, (80, 200, 255), width=26), pivot=(860, 56), daynight="untinted",
      anim=dict(swingAngle=8, swingSpeed=0.25, phase=0.5)),
    E("glow", lambda c, m: soft_union(c, [RRect(258, 98, 642, 282, 4)], (200, 120, 255), 0.25, spread=26), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=1.0)),
] + [
    E("stick%d" % i, (lambda x, y, col: lambda c, m: (flat(c, Thick(x, y, x + 4, y - 30, 4), col),
                                                     soft_union(c, [Thick(x, y, x + 4, y - 30, 4)], col, 0.5, spread=8)))(x, y, col),
      pivot=(x, y), daynight="untinted", anim=dict(swingAngle=18, swingSpeed=0.9, phase=i / 7))
    for i, (x, y, col) in enumerate(((60, 500, (120, 255, 160)), (180, 490, (255, 120, 200)), (320, 505, (120, 200, 255)),
                                     (420, 500, (255, 230, 90)), (760, 495, (255, 120, 200)), (860, 505, (120, 255, 160))))
] + [
    E("confetti%d" % i, (lambda x, col: lambda c, m: flat(c, RRect(x, 60, x + 6, 70, 1), col))(x, col),
      daynight="untinted", anim=dict(driftVelocity=(6, -40), driftLength=160, driftFade=True, spinSpeed=0.8, phase=i / 6))
    for i, (x, col) in enumerate(((150, (255, 220, 90)), (300, (255, 120, 200)), (620, (120, 200, 255)), (720, (255, 220, 90)),
                                  (820, (120, 255, 160)), (40, (255, 255, 255))))
]

L131_DIFFS = [
    ("screen", 450, 190, 0),
    ("lamp", 650, 72, 0),
    ("speaker", 788, 214, 0),
    ("drum", 560, 360, 0),
    ("outfit", 371, 365, 0),
    ("guitar", 210, 350, 0),
    ("sign", 605, 485, 0),
]


# =================================================================== Level 132 expo hall
def l132_bg(c, d):
    # roof: steel trusses with skylights
    c.rect(0, 0, W, 330, (214, 222, 232))
    for x in range(-40, 940, 120):
        flat(c, Poly([(x, 0), (x + 100, 0), (x + 90, 60), (x + 10, 60)]), (190, 222, 246))
    for y in (60, 66):
        flat(c, Thick(0, y, W, y, 4), (150, 156, 170))
    for x in range(0, 900, 30):
        flat(c, [Thick(x, 66, x + 30, 92, 2), Thick(x + 30, 66, x, 92, 2)], (160, 166, 180))
    flat(c, Thick(0, 92, W, 92, 4), (150, 156, 170))
    # hanging banners
    for i, x in enumerate((90, 250, 650, 810)):
        flat(c, Thick(x, 92, x, 110, 1.4), (120, 120, 130))
        col = [(240, 120, 40), (60, 140, 220), (60, 180, 120), (220, 70, 120)][i]
        if i == 3 and "banner" in d:
            col = (250, 210, 60)
        piece(c, Poly([(x - 30, 110), (x + 30, 110), (x + 30, 196), (x, 182), (x - 30, 196)]), col, border=1.5, shadow=PROP)
        flat(c, [Circ(x, 140, 14)], (250, 250, 250))
        flat(c, [Thick(x - 18, 166, x + 18, 166, 3)], (250, 250, 250))
    # hanging model airship over the hall
    for x in (400, 500):
        flat(c, Thick(x, 92, x, 128, 1.4), (120, 120, 130))
    piece(c, [Ell(450, 150, 96, 26)], (236, 236, 244), border=2, shadow=PROP)
    for k in range(-3, 4):
        flat(c, Thick(450 + k * 24, 126, 450 + k * 24, 174, 1.2), (210, 212, 224))
    piece(c, Poly([(540, 150), (566, 128), (572, 132), (556, 150), (572, 168), (566, 172)]), (90, 140, 220), border=1.2, shadow=SMALL)
    piece(c, RRect(424, 172, 476, 186, 4), (90, 140, 220), border=1.2, shadow=SMALL)
    # spot lamps along the truss
    for x in range(30, 900, 60):
        flat(c, [RRect(x - 5, 92, x + 5, 104, 2)], (60, 64, 76))
        soft_union(c, [Poly([(x - 4, 104), (x + 4, 104), (x + 22, 220), (x - 22, 220)])], (255, 250, 220), 0.14, spread=6)
    # back wall of booths
    c.rect(0, 230, W, 380, (232, 230, 226))
    # centre: the expo's big LED wall (abstract skyline + sun)
    piece(c, RRect(336, 236, 564, 372, 3), (40, 44, 56), border=2, shadow=PROP)
    flat(c, RRect(344, 244, 556, 364, 2), (60, 110, 190))
    flat(c, RRect(344, 300, 556, 364, 2), (90, 150, 220))
    flat(c, Circ(500, 290, 26), (255, 210, 120))
    for i, (x0, x1, top) in enumerate(((350, 380, 300), (384, 410, 274), (414, 446, 310), (450, 476, 262), (480, 520, 296), (524, 552, 282))):
        flat(c, RRect(x0, top, x1, 364, 1), (40, 70, 130))
    flat(c, RRect(344, 344, 556, 364, 0), (30, 50, 100))
    for i, (x0, x1, col) in enumerate(((-10, 170, (70, 90, 130)), (170, 330, (240, 160, 60)), (570, 730, (90, 160, 120)), (730, 910, (150, 90, 160)))):
        piece(c, RRect(x0, 240, x1, 380, 2), col, border=1.5, shadow=PROP)
        flat(c, RRect(x0 + 16, 256, x1 - 16, 330, 2), lit(col, 1.25))
        sign_box(c, x0 + 26, 268, x1 - 26, 290, lit(col, 0.75), 1320 + i, vertical=False)
        flat(c, RRect(x0 + 30, 300, x1 - 30, 320, 2), (250, 250, 250))
    # screen on the left booth
    dpiece_ = piece
    dpiece_(c, RRect(30, 296, 130, 360, 2), (30, 30, 40), border=1.5, shadow=SMALL)
    flat(c, RRect(36, 302, 124, 354, 1), (80, 170, 230) if "tv" not in d else (240, 100, 120))
    flat(c, [Ell(80, 334, 26, 10)], (250, 250, 250))
    # floor
    piece(c, RRect(-10, 380, 910, 612, 0), (196, 196, 204), shadow=LAYER)
    for y in range(380, 600, 28):
        flat(c, Thick(0, y, W, y, 1), (182, 182, 192))
    for x in range(0, 900, 56):
        flat(c, Thick(x, 380, x - 30, 600, 1), (182, 182, 192))
    # centre: concept car on a turntable
    piece(c, Ell(450, 470, 170, 34), (60, 64, 76), border=2, shadow=PROP)
    flat(c, Ell(450, 466, 160, 28), (90, 96, 110))
    car = (60, 200, 210) if "car" in d else (230, 60, 60)
    piece(c, [Poly([(330, 450), (350, 418), (410, 396), (500, 394), (560, 420), (580, 450)])], car, border=2, shadow=PROP)
    flat(c, Poly([(380, 418), (414, 402), (494, 400), (532, 420)]), (180, 220, 240))
    for x in (375, 530):
        piece(c, Circ(x, 452, 17), (30, 30, 36), shadow=SMALL)
        flat(c, Circ(x, 452, 8), (190, 190, 200))
    flat(c, Ell(570, 436, 6, 4), (255, 240, 180))
    # stanchions around it
    for x in (250, 650):
        piece(c, [RRect(x - 3, 430, x + 3, 500, 1), Ell(x, 502, 10, 4)], (200, 180, 90), shadow=SMALL)
    # left: robot arm demo on a plinth
    piece(c, RRect(150, 470, 250, 540, 3), (240, 240, 244), border=1.5, shadow=PROP)
    flat(c, RRect(160, 490, 240, 500, 1), (60, 140, 220))
    # right: giant globe on a stand
    piece(c, [Poly([(740, 560), (820, 560), (800, 530), (760, 530)])], (90, 90, 100) if "stand" not in d else (220, 170, 60), border=1.5, shadow=PROP)
    flat(c, Thick(780, 530, 780, 500, 6), (150, 150, 160))
    # info desk + visitors
    piece(c, [RRect(560, 520, 690, 590, 4)], (250, 250, 252), border=1.5, shadow=PROP)
    flat(c, RRect(560, 520, 690, 532, 2), (60, 140, 220))
    modern(c, 630, 520, (60, 140, 220), hair=(40, 30, 30), h=1.4, style="long")
    # display pedestals with small exhibits
    piece(c, RRect(684, 520, 724, 590, 2), (250, 250, 252), border=1.5, shadow=PROP)
    piece(c, [Ell(704, 504, 14, 18), RRect(698, 486, 710, 494, 2)], (230, 120, 60) if "vase" in d else (90, 170, 200), border=1.2, shadow=SMALL)
    piece(c, RRect(250, 540, 290, 600, 2), (250, 250, 252), border=1.5, shadow=PROP)
    piece(c, [RRect(256, 516, 284, 540, 4), Circ(270, 508, 10)], (200, 200, 210), border=1.2, shadow=SMALL)
    flat(c, RRect(262, 504, 278, 510, 2), (60, 200, 240))
    rnd = random.Random(132)
    for i, (x, b, h) in enumerate(((60, 600, 2.2), (190, 604, 2.1), (330, 590, 2.0), (420, 604, 2.2), (870, 600, 2.2), (520, 600, 1.9),
                                   (640, 608, 2.3))):
        top = rnd.choice(((60, 80, 140), (200, 60, 70), (240, 240, 240), (90, 140, 90), (230, 170, 60)))
        modern(c, x, b, top, hair=rnd.choice(HAIRS[:4]), h=h, bag=(60, 60, 70) if i == 1 else None, glasses=(i == 3))
        flat(c, [Thick(x - 4 * h, b - 37 * h, x + 1 * h, b - 28 * h, 1), Thick(x + 6 * h, b - 37 * h, x + 1 * h, b - 28 * h, 1)], (60, 140, 220))
        flat(c, RRect(x - 2 * h, b - 29 * h, x + 4 * h, b - 22 * h, 0.5), (250, 250, 250))
    # a potted plant
    if "plant" not in d:
        piece(c, [Circ(46, 400, 22), Circ(70, 390, 24), Circ(92, 404, 20)], (70, 150, 80), shadow=PROP)
        piece(c, RRect(52, 410, 88, 450, 4), (180, 120, 80), border=1.2, shadow=SMALL)


def robot_arm(c, m):
    col = (250, 160, 40)
    piece(c, [Circ(200, 470, 14), Thick(200, 470, 230, 410, 12)], col, border=1.5, shadow=PROP)
    piece(c, [Circ(230, 410, 10), Thick(230, 410, 280, 400, 9)], col, border=1.5, shadow=PROP)
    flat(c, [Thick(280, 400, 292, 392, 3), Thick(280, 400, 292, 410, 3)], (80, 80, 90))


def globe(c, m):
    piece(c, Circ(780, 450, 54), (80, 150, 220), border=2, shadow=PROP)
    for (x, y, rx, ry) in ((760, 430, 18, 14), (796, 440, 14, 20), (770, 474, 16, 9), (812, 470, 8, 6)):
        flat(c, Ell(x, y, rx, ry), (110, 190, 100))
    c.ellipse_ring(780, 450, 54, 54, 2, (220, 220, 230))


L132_ELEMENTS = [
    E("arm", robot_arm, pivot=(200, 470), anim=dict(swingAngle=14, swingSpeed=0.35)),
    E("globe", globe, pivot=(780, 450), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.4)),
    E("drone", lambda c, m: (piece(c, [RRect(424, 300, 476, 312, 4)], (60, 60, 70), border=1, shadow=SMALL),
                             flat(c, [Ell(424, 298, 14, 3), Ell(476, 298, 14, 3)], (200, 200, 210)),
                             flat(c, Circ(450, 314, 4), (90, 220, 120))),
      pivot=(450, 306), anim=dict(bobAmplitude=(12, 8), bobSpeed=0.3)),
    E("skyglow", lambda c, m: soft_union(c, [RRect(0, 0, W, 50, 0)], (255, 255, 240), 0.2, spread=24), daynight="untinted",
      anim=dict(twinkle=0.25, twinkleSpeed=0.2)),
]

L132_DIFFS = [
    ("banner", 810, 150, 0),
    ("tv", 80, 328, 0),
    ("car", 455, 425, 0),
    ("stand", 780, 545, 0),
    ("plant", 70, 410, 0),
    ("vase", 704, 500, 0),
]


# =================================================================== Level 133 gas station (day / night)
DN133 = day_night(40.0, tint=(0.26, 0.28, 0.50))
CANOPY = (120, 120, 780, 160)


def car_side(c, x, base, col, s=1.0):
    piece(c, [Poly([(x - 60 * s, base - 14 * s), (x - 58 * s, base - 34 * s), (x - 30 * s, base - 36 * s),
                    (x - 14 * s, base - 58 * s), (x + 30 * s, base - 58 * s), (x + 46 * s, base - 36 * s), (x + 62 * s, base - 32 * s),
                    (x + 62 * s, base - 14 * s)])], col, border=1.5, shadow=PROP)
    flat(c, [Poly([(x - 8 * s, base - 54 * s), (x + 10 * s, base - 54 * s), (x + 10 * s, base - 38 * s), (x - 22 * s, base - 38 * s)]),
             Poly([(x + 14 * s, base - 54 * s), (x + 28 * s, base - 54 * s), (x + 40 * s, base - 38 * s), (x + 14 * s, base - 38 * s)])], (180, 220, 240))
    for wx in (x - 34 * s, x + 36 * s):
        piece(c, Circ(wx, base - 12 * s, 12 * s), (30, 30, 36), shadow=SMALL)
        flat(c, Circ(wx, base - 12 * s, 5 * s), (190, 190, 200))


def pump(c, x, base, col, screen=(140, 220, 160)):
    piece(c, [RRect(x - 22, base - 96, x + 22, base, 4)], col, border=1.5, shadow=PROP)
    flat(c, RRect(x - 14, base - 86, x + 14, base - 64, 2), (40, 44, 50))
    flat(c, RRect(x - 10, base - 82, x + 10, base - 68, 1), screen)
    flat(c, RRect(x - 16, base - 56, x + 16, base - 40, 2), lit(col, 1.2))
    flat(c, Thick(x + 22, base - 50, x + 30, base - 50, 3), (40, 40, 46))
    piece(c, RRect(x - 30, base - 6, x + 30, base + 4, 2), (200, 200, 206), shadow=SMALL)


def l133_bg(c, d):
    sky(c, (130, 190, 240), (240, 220, 200), 300)
    cloud_bank(c, 150, (246, 240, 236), 1334, k=0.8)
    far_ridge(c, 210, 70, (150, 170, 196), 1331)
    for x, b in ((180, 190), (512, 194)):         # wind turbine towers (blades are elements)
        piece(c, Poly([(x - 3, b - 110), (x + 3, b - 110), (x + 5, b), (x - 5, b)]), (240, 240, 244), shadow=SMALL)
    far_round_trees(c, 280, 22, (100, 150, 110), 1332)
    # highway billboard behind the canopy
    for x in (300, 400):
        piece(c, RRect(x - 4, 92, x + 4, 140, 1), (150, 150, 160), shadow=SMALL)
    piece(c, RRect(250, 20, 450, 96, 3), (250, 250, 250), border=2, shadow=PROP)
    flat(c, RRect(258, 28, 442, 88, 2), (250, 200, 80))
    flat(c, [Circ(300, 58, 22)], (250, 250, 250))
    flat(c, [Thick(336, 46, 428, 46, 6), Thick(336, 64, 410, 64, 6)], (220, 90, 40))
    # shop (right)
    piece(c, RRect(560, 170, 900, 400, 2), (240, 236, 226), border=1.5, shadow=PROP)
    awning = (230, 70, 60)
    piece(c, Poly([(560, 196), (900, 196), (900, 222), (560, 222)]), awning, border=1.2, shadow=SMALL)
    for x in range(560, 900, 34):
        flat(c, RRect(x, 196, x + 17, 222, 0), lit(awning, 1.25))
    for x0 in (590, 680, 790):
        piece(c, RRect(x0, 240, x0 + 72, 330, 2), (180, 210, 230), border=1.2, shadow=SMALL)
        flat(c, Thick(x0 + 36, 240, x0 + 36, 330, 2), (240, 240, 240))
    piece(c, RRect(820, 300, 870, 400, 2), (240, 190, 90) if "door" in d else (150, 190, 210), border=1.2, shadow=SMALL)
    sign_box(c, 600, 178, 860, 194, (40, 120, 80), 1333, vertical=False)
    # price pylon (left)
    piece(c, RRect(28, 70, 108, 330, 3), (250, 250, 250), border=1.5, shadow=PROP)
    piece(c, RRect(34, 76, 102, 130, 3), (60, 130, 90) if "pylon" in d else (240, 120, 40), shadow=SMALL)
    flat(c, Circ(68, 103, 18), (250, 250, 250))
    for k, price in enumerate(("68", "73", "79")):
        flat(c, RRect(36, 140 + k * 56, 100, 186 + k * 56, 2), (30, 70, 140) if (k == 1 and "price" in d) else (30, 30, 36))
        seg_text(c, 50, 148 + k * 56, 30, price, (255, 90, 70), width=3)
    piece(c, RRect(60, 330, 76, 410, 1), (150, 150, 160), shadow=SMALL)
    # canopy + columns
    x0, y0, x1, y1 = CANOPY
    for x in (180, 450):
        piece(c, RRect(x - 9, y1, x + 9, 420, 1), (220, 220, 226), border=1.2, shadow=PROP)
    piece(c, RRect(x0, y0, x1 - 260, y1, 3), (250, 250, 250), border=2, shadow=PROP)
    flat(c, RRect(x0, y0 + 26, x1 - 260, y0 + 40, 0), (240, 120, 40))
    for x in range(x0 + 30, x1 - 270, 70):
        flat(c, RRect(x, y1 - 6, x + 30, y1, 1), (255, 250, 220))
    # forecourt and road
    piece(c, RRect(-10, 400, 910, 520, 0), (186, 186, 190), shadow=LAYER)
    for x in range(0, 900, 90):
        flat(c, Thick(x, 400, x - 40, 520, 1), (170, 170, 176))
    piece(c, RRect(-10, 520, 910, 612, 0), (90, 92, 100), shadow=LAYER)
    for x in range(0, 900, 80):
        flat(c, RRect(x, 562, x + 40, 568, 1), (250, 240, 200))
    # pumps
    pump(c, 230, 420, (60, 140, 220))
    pump(c, 400, 420, (250, 200, 60) if "pump" in d else (60, 140, 220))
    # car being filled + driver
    car_side(c, 320, 470, (60, 170, 120) if "car" in d else (230, 230, 236), s=1.3)
    flat(c, [Thick(408, 370, 404, 404, 3), Thick(404, 404, 384, 412, 3)], (40, 40, 46))
    modern(c, 480, 470, (230, 120, 40), bottom=(50, 60, 90), h=1.7)
    # air / water stand, bin and tyres
    piece(c, RRect(500, 330, 530, 410, 3), (240, 240, 244), border=1.2, shadow=SMALL)
    flat(c, RRect(504, 338, 526, 352, 1), (60, 140, 220))
    if "bin" not in d:
        piece(c, RRect(140, 360, 170, 410, 3), (70, 150, 90), border=1.2, shadow=SMALL)
        flat(c, RRect(136, 356, 174, 364, 2), (50, 120, 70))
    for k in range(3):
        piece(c, Ell(890 - k * 4, 410 - k * 14, 20, 8), (40, 40, 46), shadow=SMALL)
    # second car parked by the shop, motorbike and an ice chest
    car_side(c, 720, 486, (70, 110, 200), s=1.2)
    piece(c, RRect(560, 360, 610, 404, 3), (250, 250, 252), border=1.2, shadow=SMALL)
    flat(c, RRect(566, 368, 604, 380, 2), (90, 170, 220))
    for wx in (836, 880):
        piece(c, Circ(wx, 500, 12), (30, 30, 36), shadow=SMALL)
    piece(c, [Poly([(830, 492), (850, 470), (876, 470), (888, 492)])], (220, 60, 60), border=1.2, shadow=SMALL)


def blades(x, y):
    return lambda c, m: (piece(c, [Thick(x, y, x + 34 * math.cos(math.radians(a)), y + 34 * math.sin(math.radians(a)), 4) for a in (-90, 30, 150)],
                               (246, 246, 250), shadow=SMALL), flat(c, Circ(x, y, 4), (200, 200, 210)))


L133_ELEMENTS = [
    spin_el("blade1", blades(180, 80), (180, 80), 0.25),
    spin_el("blade2", blades(512, 84), (512, 84), 0.2),
    cloud_el("cloud0", 300, 40, 0.6, 6, daynight="day"),
    star_field("stars", 133, 26, 120, avoid=[(20, 60, 120, 340)]),
    E("moon", lambda c, m: piece(c, Circ(480, 44, 18), (250, 244, 220), border=2, shadow=SMALL), daynight="night"),
    E("canopy_glow", lambda c, m: soft_union(c, [RRect(CANOPY[0] + 20, CANOPY[3], CANOPY[2] - 280, 420, 6)], (255, 245, 200), 0.22, spread=30),
      daynight="night"),
    window_glow("windows", [(590, 240, 662, 330), (680, 240, 752, 330), (790, 240, 862, 330)]),
    E("pylon_glow", lambda c, m: soft_union(c, [RRect(36, 140, 100, 298, 2)], (255, 120, 90), 0.3, spread=12), daynight="night"),
    E("truck", lambda c, m: (piece(c, RRect(0, 520, 150, 580, 4), (230, 230, 236), border=1.5, shadow=PROP),
                            piece(c, [RRect(150, 536, 196, 580, 6)], (60, 110, 200), border=1.5, shadow=PROP),
                            [piece(c, Circ(x, 586, 13), (30, 30, 36), shadow=SMALL) for x in (30, 120, 172)]),
      anim=dict(drift_across(0, 196, 70, start=-400))),
]

L133_DIFFS = [
    ("door", 845, 350, 0),
    ("pylon", 68, 103, 0),
    ("price", 68, 225, 0),
    ("pump", 400, 370, 0),
    ("car", 320, 440, 0),
    ("bin", 155, 384, 0),
]


# =================================================================== Level 134 shopping mall atrium
FLOORS = (60, 200, 340)   # top edge of each storey's shop band
SHOP_COLS = [(230, 90, 90), (90, 160, 220), (250, 190, 70), (120, 190, 120), (200, 110, 200), (90, 200, 200)]


def l134_bg(c, d):
    # glass roof
    c.gradient(0, 60, (170, 210, 240), (220, 236, 248))
    for x in range(-60, 960, 60):
        flat(c, Thick(x, 0, x + 30, 60, 2), (150, 160, 176))
    flat(c, Thick(0, 58, W, 58, 4), (150, 160, 176))
    # storeys
    for fi, y in enumerate(FLOORS):
        flat(c, RRect(0, y, W, y + 140, 0), (238, 232, 222))
        for si, x in enumerate(range(-10, 910, 150)):
            col = SHOP_COLS[(si + fi * 2) % len(SHOP_COLS)]
            if fi == 0 and si == 4 and "shop" in d:
                col = (60, 60, 70)
            piece(c, RRect(x + 8, y + 10, x + 142, y + 34, 2), col, border=1.2, shadow=SMALL)
            sign_box(c, x + 24, y + 14, x + 126, y + 30, lit(col, 0.7), 1340 + fi * 10 + si, vertical=False)
            flat(c, RRect(x + 14, y + 40, x + 136, y + 118, 2), (200, 226, 240))
            flat(c, Thick(x + 75, y + 40, x + 75, y + 118, 2), (250, 250, 250))
        # floor slab + glass railing
        piece(c, RRect(-10, y + 118, 910, y + 140, 0), (210, 206, 200), border=1.2, shadow=PROP)
        if fi < 2:
            flat(c, RRect(0, y + 96, W, y + 118, 0), (200, 230, 240, 0.45))
            flat(c, Thick(0, y + 96, W, y + 96, 3), (180, 186, 196))
    # mannequins in a window (2nd floor, left)
    for k, x in enumerate((44, 92)):
        dress = (250, 200, 60) if (k == 1 and "dress" in d) else [(220, 80, 120), (60, 90, 160)][k]
        piece(c, Poly([(x - 14, 316), (x + 14, 316), (x + 7, 270), (x - 7, 270)]), dress, border=1, shadow=SMALL)
        flat(c, Circ(x, 260, 8), (236, 230, 222))
        flat(c, Thick(x, 316, x, 330, 2), (150, 150, 160))
    # ground floor
    piece(c, RRect(-10, 480, 910, 612, 0), (226, 220, 210), shadow=LAYER)
    for x in range(0, 900, 60):
        for y in range(480, 600, 30):
            if (x // 60 + y // 30) % 2:
                flat(c, RRect(x, y, x + 60, y + 30, 0), (214, 208, 198))
    # escalators (crossing between storeys)
    for (xa, ya, xb, yb) in ((560, 480, 760, 340), (300, 340, 120, 200)):
        # side truss (the slanted body under the steps), glass balustrade, handrail and steps
        piece(c, Poly([(xa, ya), (xb, yb), (xb, yb + 22), (xa, ya + 22)]), (190, 194, 204), border=1.5, shadow=PROP)
        flat(c, Poly([(xa, ya - 30), (xb, yb - 30), (xb, yb), (xa, ya)]), (210, 236, 246, 0.55))
        flat(c, [Thick(xa, ya - 30, xb, yb - 30, 5)], (50, 54, 66))
        flat(c, [Thick(xa, ya, xb, yb, 3)], (150, 156, 170))
        for k in range(1, 12):
            t = k / 12
            x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
            flat(c, Thick(x, y, x, y - 30, 1), (180, 200, 214))
    # fountain + planters
    piece(c, Ell(450, 540, 110, 26), (200, 200, 210), border=2, shadow=PROP)
    flat(c, Ell(450, 536, 96, 18), (120, 190, 230))
    if "planter" not in d:
        piece(c, RRect(250, 520, 300, 560, 4), (180, 130, 90), border=1.2, shadow=SMALL)
        piece(c, [Circ(262, 508, 16), Circ(282, 500, 18), Circ(296, 512, 14)], (70, 150, 80), shadow=SMALL)
    piece(c, RRect(620, 520, 670, 560, 4), (180, 130, 90), border=1.2, shadow=SMALL)
    piece(c, [Circ(632, 508, 16), Circ(652, 500, 18), Circ(666, 512, 14)], (70, 150, 80), shadow=SMALL)
    # hanging clock over the atrium
    flat(c, Thick(450, 58, 450, 90, 2), (120, 120, 130))
    piece(c, Circ(450, 110, 24), (250, 210, 90) if "clock" in d else (250, 250, 250), border=2, shadow=PROP)
    flat(c, [Thick(450, 110, 450, 96, 2.4), Thick(450, 110, 462, 116, 2.4)], INK)
    # shoppers
    rnd = random.Random(134)
    for i, (x, b, h) in enumerate(((60, 600, 2.2), (180, 590, 2.0), (360, 598, 2.1), (560, 592, 2.0), (760, 600, 2.3), (860, 590, 2.0))):
        top = rnd.choice(((60, 80, 140), (200, 60, 70), (240, 240, 240), (90, 140, 90), (230, 170, 60)))
        bag = (250, 120, 160) if i == 4 else rnd.choice(((240, 200, 60), (120, 180, 220), (250, 250, 250)))
        if i == 4 and "bag" in d:
            bag = (60, 180, 120)
        modern(c, x, b, top, hair=rnd.choice(HAIRS[:4]), h=h, bag=bag, skirt=(i % 3 == 1), style="long" if i % 2 else "short")
    for i, (x, b) in enumerate(((330, 470), (520, 470), (720, 330), (820, 332))):
        modern(c, x, b, rnd.choice(((60, 80, 140), (200, 60, 70), (90, 140, 90))), hair=rnd.choice(HAIRS[:3]), h=1.2)


L134_ELEMENTS = [
    # riders on the escalators (anim velocity is y-up): along each escalator, looping
    E("rider1", lambda c, m: modern(c, 580, 470, (220, 80, 80), h=1.2, hair=(40, 30, 30)),
      anim=dict(driftVelocity=(26, 18.2), driftLength=230, phase=0.0)),
    E("rider2", lambda c, m: modern(c, 290, 330, (80, 120, 200), h=1.2, hair=(90, 60, 40)),
      anim=dict(driftVelocity=(-26, 18.2), driftLength=230, phase=0.5)),
    E("balloon", lambda c, m: (flat(c, Thick(800, 140, 802, 190, 1), (120, 120, 130)),
                              piece(c, Ell(800, 128, 14, 18), (250, 120, 160), border=1, shadow=SMALL)),
      pivot=(802, 190), anim=dict(swingAngle=8, swingSpeed=0.4)),
    E("water", lambda c, m: (flat(c, [Thick(450, 530, 450, 470, 6)], (200, 236, 250, 0.9)),
                            soft_union(c, [Ell(450, 470, 18, 10)], (220, 240, 255), 0.6, spread=6)),
      pivot=(450, 530), anim=dict(stretch=(0.0, 0.12), scaleSpeed=1.6)),
    E("banner", lambda c, m: (flat(c, Thick(150, 60, 150, 80, 1), (120, 120, 130)),
                             piece(c, Poly([(126, 80), (174, 80), (174, 150), (150, 140), (126, 150)]), (240, 120, 60), border=1.2, shadow=SMALL)),
      pivot=(150, 60), anim=dict(swingAngle=4, swingSpeed=0.3)),
]

L134_DIFFS = [
    ("shop", 675, 82, 0),
    ("dress", 92, 290, 0),
    ("clock", 450, 112, 0),
    ("planter", 276, 530, 0),
    ("bag", 734, 540, 0),
]


# =================================================================== Level 135 future world
def l135_bg(c, d):
    sky(c, (90, 120, 220), (250, 200, 220), H + 60)
    # a pale ringed planet low in the sky
    soft_union(c, [Circ(600, 70, 40)], (255, 230, 250), 0.35, spread=24)
    piece(c, Circ(600, 70, 34), (240, 210, 236), shadow=None)
    flat(c, [Ell(588, 60, 12, 6), Ell(612, 82, 8, 4)], (226, 194, 226))
    c.ellipse_ring(600, 74, 62, 12, 3, (250, 236, 250))
    # floating island far away
    piece(c, [Ell(160, 120, 70, 16), Poly([(100, 124), (220, 124), (170, 170), (150, 180)])], (190, 170, 210), shadow=LAYER)
    flat(c, [Circ(140, 104, 14), Circ(166, 98, 18), Circ(190, 106, 12)], (150, 200, 170))
    # skyline of domed towers
    far_skyline(c, 330, 80, 220, (170, 160, 210), 1351)
    towers = ((280, 70, 160, (230, 236, 250)), (450, 60, 220, (210, 220, 245)), (640, 90, 120, (236, 230, 250)), (790, 60, 180, (220, 236, 246)))
    for i, (x, w, top, col) in enumerate(towers):
        piece(c, [RRect(x - w / 2, top, x + w / 2, 420, 6)], col, border=2, shadow=PROP)
        for y in range(int(top) + 30, 400, 26):
            flat(c, RRect(x - w / 2 + 8, y, x + w / 2 - 8, y + 8, 3), (150, 200, 240))
        dome = (120, 220, 200) if (i == 2 and "dome" in d) else (200, 140, 230) if i % 2 else (140, 190, 250)
        piece(c, [Ell(x, top, w / 2 + 6, w / 2.4)], dome, border=2, shadow=PROP)
        flat(c, Ell(x - w / 6, top - w / 8, w / 8, w / 12), (250, 250, 255))
    # antenna on the tall tower
    if "antenna" not in d:
        flat(c, Thick(450, 196, 450, 130, 4), (180, 180, 200))
        flat(c, [Thick(436, 158, 464, 158, 3), Thick(440, 144, 460, 144, 3)], (180, 180, 200))
        piece(c, Circ(450, 126, 9), (255, 90, 120), shadow=SMALL)
    # sky bridge between the two left towers
    piece(c, RRect(310, 262, 424, 280, 8), (240, 244, 252), border=1.5, shadow=PROP)
    flat(c, RRect(318, 266, 416, 274, 4), (150, 200, 240))
    # ring structure around the right tower
    c.ellipse_ring(790, 250, 70, 16, 5, (250, 200, 90) if "ring" not in d else (90, 230, 160))
    # maglev track
    piece(c, RRect(-10, 330, 910, 344, 3), (240, 240, 250), border=1.5, shadow=PROP)
    for x in range(40, 900, 120):
        piece(c, Poly([(x - 8, 344), (x + 8, 344), (x + 4, 420), (x - 4, 420)]), (220, 220, 236), shadow=SMALL)
    # garden plaza
    piece(c, RRect(-10, 420, 910, 612, 0), (200, 214, 230), shadow=LAYER)
    for x in range(0, 900, 50):
        flat(c, Thick(x, 420, x - 60, 600, 1), (186, 200, 220))
    for x, col in ((90, (90, 200, 140)), (340, (120, 210, 180)), (620, (90, 200, 140))):
        piece(c, Ell(x, 470, 46, 14), (240, 240, 250), border=1.5, shadow=PROP)
        piece(c, [Circ(x - 14, 440, 20), Circ(x + 10, 430, 24), Circ(x + 24, 446, 16)], col, shadow=SMALL)
        flat(c, Thick(x, 456, x, 470, 4), (150, 120, 100))
    # robots
    for i, (x, b, s) in enumerate(((210, 560, 1.4), (520, 580, 1.6), (800, 560, 1.3))):
        col = (240, 240, 250)
        if i == 1 and "robot" in d:
            col = (250, 190, 70)
        piece(c, [RRect(x - 16 * s, b - 50 * s, x + 16 * s, b - 14 * s, 8 * s), Circ(x, b - 62 * s, 13 * s)], col, border=1.5, shadow=PROP)
        flat(c, RRect(x - 9 * s, b - 66 * s, x + 9 * s, b - 58 * s, 4 * s), (60, 200, 240))
        piece(c, Ell(x, b - 6 * s, 16 * s, 8 * s), (120, 126, 150), shadow=SMALL)
    # people
    modern(c, 300, 590, (220, 220, 240), bottom=(120, 120, 160), hair=(240, 240, 250), h=2.0)
    modern(c, 680, 594, (120, 200, 230), bottom=(60, 60, 90), hair=(230, 120, 160), h=2.0, style="long")
    # light poles along the plaza
    for x in (40, 262, 870):
        piece(c, [RRect(x - 3, 470, x + 3, 600, 2)], (230, 232, 244), shadow=SMALL)
        piece(c, Ell(x, 468, 16, 6), (240, 244, 252), shadow=SMALL)
        soft_union(c, [Ell(x, 474, 12, 4)], (160, 230, 255), 0.6, spread=6)
    # bench (hover pad)
    piece(c, [RRect(380, 520, 470, 536, 6)], (250, 120, 160) if "bench" in d else (120, 160, 250), border=1.5, shadow=PROP)
    soft_union(c, [Ell(425, 548, 40, 6)], (150, 220, 255), 0.5, spread=8)


def flying_car(col, y):
    def d(c, m):
        piece(c, [Ell(0, y, 34, 11), Ell(4, y - 9, 16, 9)], col, border=1.5, shadow=SMALL)
        flat(c, Ell(6, y - 10, 10, 5), (200, 236, 250))
        soft_union(c, [Ell(-34, y + 2, 10, 4)], (120, 220, 255), 0.6, spread=6)
    return d


L135_ELEMENTS = [
    E("car1", flying_car((250, 120, 90), 40), anim=dict(drift_across(-34, 34, 60, start=200))),
    E("car2", flying_car((120, 220, 180), 66), anim=dict(drift_across(-34, 34, -44, start=700))),
    E("train", lambda c, m: (piece(c, [RRect(0, 300, 320, 330, 14)], (250, 250, 255), border=1.5, shadow=PROP),
                             flat(c, RRect(20, 308, 300, 318, 4), (90, 160, 230)),
                             flat(c, RRect(0, 324, 320, 328, 2), (255, 120, 160))),
      anim=dict(drift_across(0, 320, 220, start=-600))),
    E("holo", lambda c, m: (soft_union(c, [Poly([(560, 500), (600, 380), (640, 500)])], (120, 230, 255), 0.25, spread=8),
                           flat(c, Poly(star_pts(600, 410, 22, 9)), (160, 240, 255, 0.85))),
      daynight="untinted", anim=dict(twinkle=0.35, twinkleSpeed=1.2)),
    E("drone", lambda c, m: (piece(c, Ell(860, 160, 16, 6), (240, 240, 250), shadow=SMALL), flat(c, Circ(860, 166, 3), (255, 90, 120))),
      pivot=(860, 160), anim=dict(bobAmplitude=(10, 14), bobSpeed=0.25)),
]

L135_DIFFS = [
    ("dome", 640, 90, 0),
    ("antenna", 450, 160, 0),
    ("ring", 790, 250, 0),
    ("robot", 520, 520, 0),
    ("bench", 425, 528, 0),
]


LEVELS = [
    ("Level130", "体育比赛", l130_bg, L130_ELEMENTS, L130_DIFFS, 60, OPTS),
    ("Level131", "演唱会", l131_bg, L131_ELEMENTS, L131_DIFFS, 60, OPTS),
    ("Level132", "大型展览", l132_bg, L132_ELEMENTS, L132_DIFFS, 60, OPTS),
    ("Level133", "加油站", l133_bg, L133_ELEMENTS, L133_DIFFS, 60, dict(OPTS, day_night=DN133, anim_seconds=40.0, frames=80)),
    ("Level134", "商场", l134_bg, L134_ELEMENTS, L134_DIFFS, 60, OPTS),
    ("Level135", "未来世界", l135_bg, L135_ELEMENTS, L135_DIFFS, 60, OPTS),
]
