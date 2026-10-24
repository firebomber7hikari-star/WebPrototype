# -*- coding: utf-8 -*-
"""Everyday-town themes, part 6: events and leisure (paper-craft, full-bleed, no real brands or logos):
  Level550 花园婚礼 - a garden wedding: flower arch, couple, rows of guests, cake table, falling petals
  Level551 毕业典礼 - a graduation: stage with podium and banner, gowned graduates, caps tossed, families
  Level552 科技展   - a school science fair: booths with a volcano model, robot, planet mobile, posters
  Level553 草地音乐节 - a daytime lawn music festival: stage, flags, food tents, crowd, ferris wheel
  Level554 时装秀   - a fashion show: runway, models, front row, photographers' flashes
  Level555 魔术表演 - a magic show: red curtains, magician, rabbit in a hat, doves, audience
  Level556 木偶剧场 - a park puppet theatre: booth with puppets, children on the lawn, balloon seller
  Level557 芭蕾舞室 - a ballet studio: mirror wall, barre, dancers, piano, tall windows
  Level558 烹饪课   - a cooking class: teaching kitchen, chef, students at stations, oven
  Level559 公园象棋 - chess in the park: stone tables, players, onlookers, birdcages on a branch
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_modern import crowd
from levels_daily import balloon_bunch
from levels_daily3 import counter, plant, room, steam_el, wall_shelf

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def chair_row(c, x0, n, base, col, step=56):
    for k in range(n):
        x = x0 + k * step
        piece(c, [RRect(x - 18, base - 60, x + 18, base - 54, 2), RRect(x - 18, base - 30, x + 18, base - 24, 2), RRect(x - 16, base - 60, x - 12, base, 1),
                  RRect(x + 12, base - 60, x + 16, base, 1)], col, border=1, shadow=SMALL)


def seated(c, x, base, top, hair=(40, 30, 30), h=1.6, style="short"):
    """Guest seen from behind/side sitting on a chair (only the upper body shows above the backrest)."""
    modern(c, x, base - 12 * h, top, bottom=top, hair=hair, h=h, style=style)


def flash_el(eid, x, y, period_phase):
    return E(eid, lambda c, m: (soft_union(c, [Circ(x, y, 6)], (255, 255, 240), 0.9, spread=24), flat(c, Poly(star_pts(x, y, 14, 3, points=4)), (255, 255, 255))),
             daynight="untinted", anim=dict(twinkle=1.0, twinkleSpeed=0.5, phase=period_phase))


# =================================================================== Level 550 garden wedding
def l550_bg(c, d):
    sky(c, (140, 200, 240), (236, 240, 236), 300)
    far_round_trees(c, 180, 40, (120, 170, 120), 5501)
    far_round_trees(c, 240, 34, (100, 160, 100), 5502)
    piece(c, RRect(-10, 260, 910, 612, 0), (150, 200, 110), shadow=LAYER)
    # flower arch (centre back)
    for x in (380, 520):
        piece(c, RRect(x - 6, 140, x + 6, 380, 2), (250, 250, 246), shadow=PROP)
    c.ellipse_ring(450, 150, 76, 70, 12, (250, 250, 246), ymax=150)
    rnd = random.Random(5503)
    for k in range(28):
        a = math.pi * k / 27
        x, y = 450 - 76 * math.cos(a), 150 - 70 * math.sin(a)
        col = rnd.choice([(250, 180, 200), (250, 250, 250), (240, 140, 170)])
        if "roses" in d and k < 9:
            col = (250, 200, 80)
        flat(c, Circ(x, y, 9), col)
    for y in range(160, 370, 26):
        flat(c, [Circ(380, y, 8), Circ(520, y, 8)], (250, 200, 220))
    # couple
    modern(c, 420, 380, (40, 40, 50), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3)
    flat(c, RRect(418, 300, 424, 330, 1), (250, 250, 250))
    piece(c, Poly([(460, 380), (520, 380), (500, 316), (480, 316)]), (250, 250, 252), border=1.2, shadow=PROP)
    modern(c, 490, 330, (250, 250, 252), bottom=(250, 250, 252), hair=(220, 180, 90), h=1.6, style="long")
    flat(c, Poly([(476, 262), (508, 262), (520, 320), (464, 320)]), (250, 250, 255, 0.7))
    flat(c, [Circ(466 + k * 8, 330 - (k % 2) * 6, 8) for k in range(4)], (250, 120, 160) if "bouquet" not in d else (120, 180, 240))
    # aisle runner + chairs with guests
    piece(c, Poly([(420, 380), (480, 380), (560, 612), (340, 612)]), (250, 250, 250), shadow=SMALL)
    for side, x0 in ((0, 40), (1, 600)):
        for r, base in enumerate((440, 520, 600)):
            chair_row(c, x0 + (0 if side else -r * 10), 5, base, (250, 250, 246))
    guests = [(60, 440, (90, 150, 220)), (172, 440, (240, 180, 90)), (284, 440, (200, 110, 150)), (40, 520, (120, 190, 120)),
              (208, 520, (60, 60, 70)), (656, 440, (240, 120, 90)), (768, 440, (150, 120, 190)), (712, 520, (90, 160, 140)),
              (824, 520, (240, 200, 90)), (600, 600, (200, 90, 90))]
    for k, (x, b, col) in enumerate(guests):
        if k == 6 and "guest" in d:
            col = (250, 200, 60)
        seated(c, x, b, col, hair=[(40, 30, 30), (90, 60, 40), (220, 180, 90), (130, 130, 140)][k % 4], h=1.9, style="long" if k % 3 == 1 else "short")
    # cake table (right back)
    piece(c, [RRect(740, 330, 880, 344, 3), RRect(750, 344, 870, 400, 2)], (250, 250, 250), border=1.5, shadow=PROP)
    piece(c, [RRect(780, 300, 840, 330, 3), RRect(798, 256, 822, 276, 3)], (250, 246, 236), border=1.2, shadow=SMALL)
    piece(c, RRect(788, 276, 832, 300, 3), (250, 246, 236) if "cake" not in d else (240, 180, 200), border=1.2, shadow=SMALL)
    flat(c, [Circ(810, 250, 6)], (240, 120, 150))
    # string lights between the trees
    for k in range(18):
        x = 20 + k * 20
        y = 110 + 20 * math.sin(k / 17 * math.pi)
        flat(c, Circ(x, y, 3.4), (255, 230, 140))
    flat(c, [Thick(20 + k * 20, 110 + 20 * math.sin(k / 17 * math.pi), 40 + k * 20, 110 + 20 * math.sin((k + 1) / 17 * math.pi), 1) for k in range(17)],
         (120, 110, 100))
    # welcome sign on an easel (left back)
    flat(c, [Thick(120, 380, 140, 300, 3), Thick(180, 380, 160, 300, 3)], (150, 110, 80))
    piece(c, RRect(110, 270, 190, 340, 3), (250, 246, 236), border=1.2, shadow=PROP)
    flat(c, [Circ(150, 296, 12)], (240, 150, 170) if "sign" not in d else (150, 200, 120))
    flat(c, Thick(126, 322, 174, 322, 3), (150, 120, 100))


L550_ELEMENTS = [
    E("petal%d" % i, (lambda x: lambda c, m: flat(c, Ell(x, 120, 5, 3), (250, 190, 210)))(x),
      anim=dict(driftVelocity=(8, -30), driftLength=260, driftFade=True, spinSpeed=0.8, bobAmplitude=(8, 0), bobSpeed=0.5, phase=i / 4))
    for i, x in enumerate((400, 440, 480, 520))
] + [
    E("lights", lambda c, m: [soft_union(c, [Circ(20 + k * 20, 110 + 20 * math.sin(k / 17 * math.pi), 3)], (255, 230, 140), 0.6, spread=8) for k in range(18)],
      daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=1.2)),
    bird_el("dove", 600, 60, s=10, speed=-18, col=(250, 250, 250)),
]

L550_DIFFS = [
    ("roses", 410, 110, 0),
    ("bouquet", 479, 330, 0),
    ("guest", 769, 357, 0),
    ("cake", 810, 288, 0),
    ("sign", 150, 296, 0),
]


# =================================================================== Level 551 graduation
GOWN = (40, 40, 60)


def graduate(c, x, base, h=1.8, hair=(40, 30, 30), style="short", gown=GOWN, sash=(250, 200, 60), cap=True):
    modern(c, x, base, gown, bottom=gown, hair=hair, h=h, style=style)
    piece(c, Poly([(x - 10 * h, base - 2 * h), (x + 10 * h, base - 2 * h), (x + 8 * h, base - 36 * h), (x - 8 * h, base - 36 * h)]), gown, border=1.2,
          shadow=SMALL)
    flat(c, [Thick(x - 6 * h, base - 36 * h, x - 4 * h, base - 20 * h, 3 * h), Thick(x + 6 * h, base - 36 * h, x + 4 * h, base - 20 * h, 3 * h)], sash)
    if cap:
        hx, hy = x + 1 * h, base - 46 * h
        flat(c, [Poly([(hx - 12 * h, hy - 8 * h), (hx, hy - 13 * h), (hx + 12 * h, hy - 8 * h), (hx, hy - 3 * h)]), RRect(hx - 6 * h, hy - 8 * h, hx + 6 * h, hy - 4 * h, 1)],
             (30, 30, 40))
        flat(c, Thick(hx + 8 * h, hy - 8 * h, hx + 10 * h, hy, 1.2), sash)


def l551_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 420)
    cloud_bg(c, 760, 60, 0.7)
    # school hall behind the stage
    piece(c, RRect(120, 40, 780, 300, 2), (230, 210, 180), border=2, shadow=PROP)
    piece(c, Poly([(100, 46), (800, 46), (450, 0)]), (170, 80, 70), border=2, shadow=PROP)
    for k in range(6):
        x = 160 + k * 104
        flat(c, RRect(x, 90, x + 60, 170, 28), (150, 190, 220) if not (k == 0 and "window" in d) else (250, 210, 120))
    tree_round(c, 60, 300, s=1.6)
    tree_round(c, 850, 300, s=1.7)
    # banner over the stage
    piece(c, RRect(220, 190, 680, 236, 4), (60, 90, 160), border=1.5, shadow=PROP)
    sign_box(c, 250, 200, 650, 226, (250, 230, 150), 5511, vertical=False)
    # stage
    piece(c, RRect(140, 300, 760, 360, 3), (150, 110, 80), border=1.5, shadow=PROP)
    flat(c, RRect(140, 300, 760, 312, 2), (130, 94, 68))
    for x in range(160, 760, 60):
        flat(c, Thick(x, 316, x, 356, 1.2), (130, 94, 68))
    # podium + principal
    modern(c, 450, 300, (90, 60, 50), bottom=(40, 40, 50), hair=(130, 130, 140), h=2.0, glasses=True)
    piece(c, Poly([(410, 300), (490, 300), (484, 240), (416, 240)]), (120, 80, 60), border=1.5, shadow=PROP)
    flat(c, Circ(450, 266, 12), (250, 200, 60))
    # potted flowers on the stage edge
    for k, x in enumerate((180, 720)):
        piece(c, Poly([(x - 18, 300), (x + 18, 300), (x + 14, 270), (x - 14, 270)]), (200, 120, 90), border=1, shadow=SMALL)
        flat(c, [Circ(x - 12 + j * 8, 262 - (j % 2) * 6, 6) for j in range(4)], (250, 120, 160) if not (k == 1 and "flowers" in d) else (250, 220, 70))
    # graduates on the stage
    for k, x in enumerate((240, 310, 590, 660)):
        graduate(c, x, 300, h=1.6, hair=[(40, 30, 30), (220, 180, 90), (90, 60, 40), (40, 30, 30)][k], style="long" if k % 2 else "short",
                 sash=(250, 200, 60) if not (k == 2 and "sash" in d) else (220, 70, 70))
    # lawn + families
    piece(c, RRect(-10, 360, 910, 612, 0), (140, 190, 100), shadow=LAYER)
    chair_row(c, 60, 15, 470, (250, 250, 246))
    for k, x in enumerate(range(60, 900, 112)):
        graduate(c, x, 458, h=1.5, hair=[(40, 30, 30), (90, 60, 40), (220, 180, 90)][k % 3], style="long" if k % 2 else "short")
    for k, (x, col) in enumerate(((120, (240, 120, 90)), (220, (90, 150, 220)), (520, (120, 190, 120)), (640, (220, 110, 150)), (780, (240, 200, 90)))):
        modern(c, x, 600, col, bottom=(60, 60, 80), hair=[(40, 30, 30), (130, 130, 140), (90, 60, 40)][k % 3], h=2.2, style="long" if k % 2 else "short")
    # camera on a tripod
    flat(c, [Thick(360, 600, 380, 540, 3), Thick(400, 600, 380, 540, 3)], (40, 40, 46))
    piece(c, RRect(360, 516, 404, 542, 4), (40, 40, 46) if "camera" not in d else (200, 60, 70), border=1, border_col=(120, 120, 130), shadow=SMALL)
    flat(c, Circ(364, 528, 8), (120, 160, 200))


L551_ELEMENTS = [
    E("cap%d" % i, (lambda x: lambda c, m: flat(c, [Poly([(x - 14, 120), (x, 112), (x + 14, 120), (x, 128)])], (30, 30, 40)))(x),
      pivot=(x, 120), anim=dict(bobAmplitude=(0, 40), bobSpeed=0.4, bounce=True, rotateSpeed=60, phase=i / 3))
    for i, x in enumerate((300, 560, 640))
] + [
    E("confetti%d" % i, (lambda x, col: lambda c, m: flat(c, RRect(x, 40, x + 6, 50, 1), col))(x, col),
      anim=dict(driftVelocity=(6, -40), driftLength=200, driftFade=True, spinSpeed=0.8, phase=i / 5))
    for i, (x, col) in enumerate(((200, (250, 200, 60)), (330, (240, 120, 160)), (500, (90, 170, 240)), (620, (250, 200, 60)), (760, (120, 200, 120))))
]

L551_DIFFS = [
    ("window", 190, 130, 0),
    ("flowers", 720, 262, 0),
    ("sash", 590, 260, 0),
    ("camera", 382, 528, 0),
]


# =================================================================== Level 552 science fair
def volcano(c, x, base, col=(150, 110, 80), lava=(240, 90, 50)):
    piece(c, Poly([(x - 60, base), (x + 60, base), (x + 14, base - 80), (x - 14, base - 80)]), col, border=1.5, shadow=PROP)
    flat(c, Poly([(x - 14, base - 80), (x + 14, base - 80), (x + 20, base - 56), (x + 6, base - 64), (x - 4, base - 50), (x - 16, base - 60)]), lava)


def booth(c, x0, x1, top, base, cloth, board):
    piece(c, RRect(x0, top, x1, top + 120, 4), board, border=1.5, shadow=PROP)
    piece(c, [RRect(x0 - 10, base - 70, x1 + 10, base - 56, 3)], cloth, border=1.2, shadow=PROP)
    flat(c, RRect(x0 - 10, base - 56, x1 + 10, base, 2), lit(cloth, 0.9))


def l552_bg(c, d):
    room(c, (226, 230, 236), (220, 224, 232), (190, 186, 180), (176, 172, 166), floor_y=480)
    # bunting across the gym
    for x in range(0, 900, 36):
        flat(c, Poly([(x, 40), (x + 30, 40), (x + 15, 64)]), [(240, 120, 90), (90, 160, 230), (250, 210, 80), (120, 200, 120)][(x // 36) % 4])
    flat(c, Thick(0, 40, W, 40, 2), (120, 110, 100))
    # three booths
    booth(c, 40, 260, 120, 480, (60, 120, 200), (250, 250, 246))
    booth(c, 340, 560, 120, 480, (220, 80, 80), (250, 250, 246))
    booth(c, 640, 860, 120, 480, (90, 170, 110), (250, 250, 246))
    # posters on the boards
    for k, (x0, cols) in enumerate(((40, ((240, 160, 90), (150, 200, 230))), (340, ((90, 160, 230), (240, 200, 90))), (640, ((120, 200, 140), (230, 130, 170))))):
        for j in range(2):
            col = cols[j]
            if k == 2 and j == 1 and "poster" in d:
                col = (90, 90, 110)
            flat(c, RRect(x0 + 20 + j * 104, 140, x0 + 96 + j * 104, 220, 3), col)
            flat(c, [Thick(x0 + 30 + j * 104, 160 + i * 16, x0 + 86 + j * 104, 160 + i * 16, 3) for i in range(3)], (250, 250, 250))
    # volcano model (left booth)
    volcano(c, 150, 410, lava=(240, 90, 50) if "lava" not in d else (90, 200, 120))
    # robot (middle booth)
    rob = (200, 206, 220) if "robot" not in d else (250, 190, 70)
    piece(c, [RRect(420, 330, 480, 400, 8), RRect(430, 296, 470, 330, 6), RRect(426, 400, 440, 410, 2), RRect(460, 400, 474, 410, 2)], rob, border=1.5,
          shadow=PROP)
    flat(c, [Circ(442, 312, 5), Circ(458, 312, 5)], (90, 200, 240))
    flat(c, Thick(450, 296, 450, 282, 2), (90, 90, 100))
    flat(c, Circ(450, 280, 4), (240, 80, 80))
    # plant growth experiment (right booth)
    for k in range(3):
        x = 700 + k * 50
        piece(c, Poly([(x - 14, 410), (x + 14, 410), (x + 10, 384), (x - 10, 384)]), (200, 120, 90), border=1, shadow=SMALL)
        flat(c, Thick(x, 384, x, 384 - 20 * (k + 1), 3), (80, 150, 80))
        flat(c, [Ell(x - 8, 384 - 20 * (k + 1), 8, 4), Ell(x + 8, 384 - 20 * (k + 1) + 6, 8, 4)], (90, 170, 90))
    piece(c, [RRect(820, 360, 850, 410, 3)], (180, 220, 240), border=1, shadow=SMALL)
    # students presenting + visitors
    modern(c, 270, 560, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.0, style="long")
    modern(c, 580, 560, (120, 190, 160), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.0, glasses=True)
    modern(c, 880, 560, (220, 110, 150), bottom=(60, 70, 110), hair=(40, 30, 30), h=1.9, style="twin")
    modern(c, 120, 600, (90, 140, 200), bottom=(40, 40, 50), hair=(130, 130, 140), h=2.4)
    modern(c, 420, 600, (240, 140, 90), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.3, style="long", bag=(150, 100, 60))
    modern(c, 720, 600, (150, 150, 170), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.3)
    # prize ribbon on the middle booth
    piece(c, [Circ(530, 150, 16), Poly([(522, 160), (530, 160), (524, 190), (516, 186)]), Poly([(530, 160), (538, 160), (544, 186), (536, 190)])],
          (60, 110, 200) if "ribbon" not in d else (250, 190, 50), border=1, shadow=SMALL)


def planets(c, m):
    flat(c, Thick(760, 60, 760, 90, 1.2), (100, 100, 110))
    piece(c, Circ(760, 100, 14), (250, 200, 60), border=1, shadow=SMALL)
    for r, col, a in ((40, (90, 160, 230), 0.4), (60, (220, 100, 80), 2.6), (80, (180, 140, 220), 4.6)):
        x, y = 760 + r * math.cos(a), 100 + r * 0.35 * math.sin(a)
        flat(c, Thick(760, 100, x, y, 1), (160, 160, 170))
        piece(c, Circ(x, y, 7), col, border=1, shadow=SMALL)


L552_ELEMENTS = [
    E("planets", planets, pivot=(760, 100), anim=dict(stretch=(0.3, 0), scaleSpeed=0.3)),
    E("smoke", lambda c, m: soft_union(c, [Circ(150, 320, 8)], (220, 220, 226), 0.8, spread=8),
      anim=dict(driftVelocity=(2, 20), driftLength=60, driftFade=True, driftGrow=1.6)),
    E("wave", lambda c, m: flat(c, Thick(474, 350, 500, 324, 6), (200, 206, 220)), pivot=(474, 350), anim=dict(swingAngle=20, swingSpeed=0.8)),
]

L552_DIFFS = [
    ("poster", 798, 180, 0),
    ("lava", 150, 340, 0),
    ("robot", 450, 350, 0),
    ("ribbon", 530, 165, 0),
]


# =================================================================== Level 553 lawn music festival
def l553_bg(c, d):
    sky(c, (120, 186, 240), (226, 238, 246), 300)
    cloud_bg(c, 120, 60, 0.8)
    cloud_bg(c, 820, 40, 0.6)
    far_ridge(c, 200, 40, (160, 196, 170), 5531)
    # ferris wheel (left back)
    c.ellipse_ring(150, 170, 110, 110, 5, (240, 240, 246))
    flat(c, [Thick(150 - 110 * math.cos(a), 170 - 110 * math.sin(a), 150 + 110 * math.cos(a), 170 + 110 * math.sin(a), 2) for a in
             [k * math.pi / 6 for k in range(6)]], (240, 240, 246))
    flat(c, [Thick(150, 170, 100, 290, 5), Thick(150, 170, 200, 290, 5)], (220, 220, 230))
    for k in range(12):
        a = k * math.pi / 6
        col = [(240, 90, 90), (90, 160, 230), (250, 200, 60)][k % 3]
        if k == 4 and "gondola" in d:
            col = (120, 200, 120)
        piece(c, RRect(150 + 110 * math.cos(a) - 14, 170 + 110 * math.sin(a) - 6, 150 + 110 * math.cos(a) + 14, 170 + 110 * math.sin(a) + 18, 3), col,
              border=1, shadow=SMALL)
    # stage (right)
    piece(c, RRect(420, 70, 880, 300, 4), (40, 40, 50), border=2, shadow=PROP)
    piece(c, Poly([(400, 76), (900, 76), (860, 30), (440, 30)]), (250, 250, 250), border=1.5, shadow=PROP)
    flat(c, RRect(440, 90, 860, 290, 2), (60, 50, 80))
    for k in range(5):
        flat(c, Circ(480 + k * 90, 100, 10), [(255, 120, 150), (120, 200, 255), (255, 230, 120)][k % 3])
    piece(c, RRect(400, 290, 900, 320, 2), (90, 90, 100), shadow=PROP)
    modern(c, 560, 290, (250, 200, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0)
    modern(c, 660, 290, (200, 60, 90) if "singer" not in d else (90, 190, 220), bottom=(30, 30, 40), hair=(220, 180, 90), h=2.1, style="long")
    modern(c, 760, 290, (90, 150, 220), bottom=(40, 40, 50), hair=(90, 60, 40), h=2.0)
    piece(c, [Ell(556, 252, 13, 10), Thick(566, 248, 596, 228, 4)], (230, 120, 50), border=1, shadow=SMALL)
    # speaker towers
    for x in (410, 870):
        piece(c, RRect(x - 24, 180, x + 24, 300, 3), (40, 40, 46), border=1.2, border_col=(120, 120, 130), shadow=PROP)
        flat(c, [Circ(x, 210, 12), Circ(x, 260, 16)], (70, 70, 80))
    # lawn
    piece(c, RRect(-10, 300, 910, 612, 0), (130, 190, 100), shadow=LAYER)
    # food tents (left)
    for k, (x, col) in enumerate(((60, (240, 120, 90)), (200, (90, 170, 220)))):
        if k == 1 and "tent" in d:
            col = (240, 200, 70)
        piece(c, Poly([(x - 60, 380), (x + 60, 380), (x + 40, 330), (x - 40, 330)]), col, border=1.5, shadow=PROP)
        flat(c, [Poly([(x - 60 + j * 30, 380), (x - 45 + j * 30, 380), (x - 34 + j * 26, 330), (x - 40 + j * 26, 330)]) for j in range(4)], lit(col, 1.15))
        piece(c, RRect(x - 52, 380, x + 52, 430, 2), (250, 246, 236), border=1, shadow=SMALL)
    # crowd from behind + picnic blanket
    crowd(c, 300, 900, 360, 4, 5532, step=16, dy=20)
    piece(c, Poly([(40, 520), (240, 500), (280, 580), (60, 600)]), (220, 70, 70) if "blanket" not in d else (90, 140, 220), border=1.2, shadow=SMALL)
    for k in range(4):
        flat(c, Thick(50 + k * 50, 520 - k * 5, 70 + k * 50, 596 - k * 5, 6), (250, 250, 250))
    modern(c, 140, 560, (250, 220, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.8, style="long")
    modern(c, 420, 600, (90, 150, 110), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.3)
    modern(c, 760, 600, (240, 160, 180), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.2, style="twin")


L553_ELEMENTS = [
    E("flag%d" % i, (lambda x, col: lambda c, m: (flat(c, Thick(x, 470, x, 360, 3), (150, 150, 160)),
                                                 piece(c, Poly([(x + 1, 360), (x + 40, 370), (x + 1, 384)]), col, border=1, shadow=SMALL)))(x, col),
      pivot=(x, 372), anim=dict(stretch=(0.15, 0), scaleSpeed=1.2, phase=i / 3))
    for i, (x, col) in enumerate(((330, (240, 90, 90)), (520, (90, 160, 230)), (840, (250, 200, 60))))
] + [
    E("notes", lambda c, m: [flat(c, [Circ(620 + k * 26, 220 - k * 16, 5), Thick(624 + k * 26, 220 - k * 16, 624 + k * 26, 200 - k * 16, 2)], (255, 230, 140))
                             for k in range(3)], daynight="untinted", anim=dict(driftVelocity=(10, 20), driftLength=60, driftFade=True)),
    E("beach_ball", lambda c, m: (piece(c, Circ(600, 340, 14), (250, 250, 250), shadow=SMALL), flat(c, [Poly([(600, 326), (612, 340), (600, 354)])], (240, 90, 90))),
      pivot=(600, 340), anim=dict(bobAmplitude=(30, 40), bobSpeed=0.4, bounce=True)),
    cloud_el("cloud", 400, 40, 0.6, 6),
]

L553_DIFFS = [
    ("gondola", 70, 280, 0),
    ("singer", 661, 248, 0),
    ("tent", 200, 355, 0),
    ("blanket", 150, 550, 0),
]


# =================================================================== Level 554 fashion show
def model(c, x, base, top, bottom, h=2.2, hair=(40, 30, 30), style="long", skirt=True):
    modern(c, x, base, top, bottom=bottom, hair=hair, h=h, style=style, skirt=skirt)


def l554_bg(c, d):
    c.rect(0, 0, W, H, (30, 28, 40))
    # backdrop with light panels
    piece(c, RRect(200, 20, 700, 300, 4), (50, 48, 64), border=1.5, border_col=(90, 90, 110), shadow=PROP)
    for k in range(8):
        flat(c, RRect(220 + k * 60, 40, 260 + k * 60, 280, 3), (80, 76, 100))
    flat(c, RRect(360, 220, 540, 300, 0), (20, 18, 28))                     # entrance
    piece(c, RRect(330, 60, 570, 110, 5), (250, 250, 250) if "logo" not in d else (240, 190, 60), border=1.2, border_col=(90, 90, 110), shadow=SMALL)
    sign_box(c, 350, 72, 550, 98, (30, 28, 40), 5541, vertical=False)
    # runway (perspective)
    piece(c, Poly([(380, 300), (520, 300), (640, 612), (260, 612)]), (240, 240, 246), border=1.5, border_col=(90, 90, 110), shadow=SMALL)
    for y in range(320, 612, 40):
        t = (y - 300) / 312
        flat(c, Thick(380 - 120 * t, y, 520 + 120 * t, y, 1), (220, 220, 228))
    # models
    model(c, 450, 320, (250, 250, 250), (30, 30, 40), h=1.6, hair=(220, 180, 90))
    model(c, 430, 470, (200, 40, 70) if "dress" not in d else (60, 160, 200), (200, 40, 70) if "dress" not in d else (60, 160, 200), h=2.4, hair=(40, 30, 30))
    # front-row audience on both sides
    for side in (0, 1):
        for r, base in enumerate((400, 480, 560, 640)):
            for k in range(3):
                x = (240 - k * 70 - r * 30) if side == 0 else (660 + k * 70 + r * 30)
                col = [(60, 60, 80), (150, 120, 180), (240, 200, 90), (90, 150, 140), (200, 100, 110)][(k + r * 2 + side) % 5]
                if side == 1 and r == 1 and k == 1 and "coat" in d:
                    col = (250, 120, 40)
                seated(c, x, base, col, hair=[(40, 30, 30), (220, 180, 90), (90, 60, 40)][(k + r) % 3], h=1.6 + r * 0.15,
                       style="long" if (k + r) % 2 else "short")
    # photographers' pit (front centre)
    for k, x in enumerate((380, 520)):
        modern(c, x, 612, (40, 40, 50), bottom=(30, 30, 40), hair=(40, 30, 30), h=2.0)
        piece(c, RRect(x - 18, 500, x + 18, 524, 4), (60, 60, 70) if not (k == 1 and "camera" in d) else (220, 70, 70), border=1, border_col=(120, 120, 130),
              shadow=SMALL)
        flat(c, Circ(x - 18, 512, 7), (120, 160, 200))
    # flower arrangement at the runway head
    piece(c, Poly([(600, 300), (640, 300), (636, 270), (604, 270)]), (250, 250, 250), border=1, border_col=(90, 90, 110), shadow=SMALL)
    flat(c, [Circ(608 + k * 8, 262 - (k % 2) * 6, 7) for k in range(4)], (250, 120, 170))


L554_ELEMENTS = [
    flash_el("f1", 380, 504, 0.0), flash_el("f2", 520, 504, 0.5), flash_el("f3", 120, 360, 0.25), flash_el("f4", 800, 380, 0.75),
    E("spot", lambda c, m: soft_union(c, [Poly([(440, 0), (460, 0), (520, 480), (360, 480)])], (255, 250, 230), 0.15, spread=20), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.4)),
    E("walk", lambda c, m: model(c, 450, 320, (250, 250, 250), (30, 30, 40), h=1.6, hair=(220, 180, 90)), pivot=(450, 320),
      anim=dict(bobAmplitude=(0, 2), bobSpeed=1.2)),
]

L554_DIFFS = [
    ("logo", 450, 85, 0),
    ("dress", 431, 410, 0),
    ("coat", 770, 438, 0),
    ("camera", 520, 512, 0),
]


# =================================================================== Level 555 magic show
def l555_bg(c, d):
    c.rect(0, 0, W, H, (40, 20, 30))
    # stage curtains
    piece(c, RRect(-10, 0, 910, 60, 0), (170, 30, 40), shadow=PROP)
    for x in range(-10, 910, 40):
        flat(c, Poly([(x, 60), (x + 40, 60), (x + 20, 84)]), (170, 30, 40))
    flat(c, [Thick(-10, 60, 910, 60, 4)], (230, 190, 70))
    for side, x0 in ((0, -10), (1, 760)):
        piece(c, Poly([(x0, 60), (x0 + 150, 60), (x0 + 110 if side == 0 else x0 + 40, 440), (x0 if side == 0 else x0 + 150, 440)]), (190, 40, 50), shadow=PROP)
        for k in range(5):
            xx = x0 + 15 + k * 28
            flat(c, Thick(xx, 70, xx + (-20 if side == 0 else 20) * k / 4, 430, 3), (150, 26, 36))
    flat(c, RRect(140, 84, 760, 440, 0), (60, 30, 50))
    # star backdrop
    for k in range(10):
        rnd = random.Random(5551 + k)
        flat(c, Poly(star_pts(rnd.uniform(180, 720), rnd.uniform(110, 300), 10, 4)), (230, 190, 70))
    # stage floor
    piece(c, RRect(-10, 440, 910, 480, 0), (120, 70, 50), shadow=PROP)
    flat(c, RRect(-10, 440, 910, 448, 0), (150, 90, 60))
    # magician with top hat on the table
    modern(c, 360, 440, (30, 30, 40), bottom=(30, 30, 40), hair=(40, 30, 30), h=2.6)
    flat(c, [Poly([(344, 330), (362, 330), (360, 352), (346, 352)])], (180, 30, 40))
    flat(c, Thick(380, 360, 430, 330, 3), (30, 30, 40))
    flat(c, [Thick(430, 330, 460, 310, 3)], (250, 250, 250))
    piece(c, [RRect(470, 380, 590, 392, 3), RRect(524, 392, 536, 440, 2)], (200, 160, 80), border=1.2, shadow=PROP)
    flat(c, Poly([(470, 392), (590, 392), (580, 420), (480, 420)]), (180, 30, 40))
    # magic trunk (left) + curtain tassel (right)
    piece(c, [RRect(170, 380, 270, 440, 6)], (60, 90, 160) if "trunk" not in d else (150, 90, 60), border=1.5, border_col=(110, 90, 100), shadow=PROP)
    flat(c, [Thick(170, 396, 270, 396, 3), RRect(212, 386, 228, 406, 2)], (230, 190, 70))
    piece(c, [Ell(820, 300, 20, 12), Poly([(806, 306), (834, 306), (842, 350), (798, 350)])], (230, 190, 70) if "tassel" not in d else (90, 180, 230),
          border=1, border_col=(110, 90, 100), shadow=SMALL)
    piece(c, [RRect(500, 330, 560, 380, 3), RRect(488, 372, 572, 382, 3)], (30, 30, 40), border=1, border_col=(110, 90, 100), shadow=SMALL)
    flat(c, RRect(500, 362, 560, 370, 1), (180, 30, 40))
    # rabbit popping out
    piece(c, [Circ(530, 320, 14), Ell(522, 296, 4, 14), Ell(538, 296, 4, 14)], (250, 250, 250) if "rabbit" not in d else (170, 140, 120), border=1, shadow=SMALL)
    flat(c, [Circ(526, 318, 1.8), Circ(536, 318, 1.8)], INK)
    # assistant with a hoop
    modern(c, 660, 440, (240, 200, 60), bottom=(240, 200, 60), hair=(90, 60, 40), h=2.2, style="long", skirt=True)
    c.ellipse_ring(700, 330, 34, 34, 5, (230, 190, 70) if "hoop" not in d else (90, 200, 220))
    # audience silhouettes
    rnd = random.Random(5552)
    for row, (y, hh) in enumerate(((540, 1.0), (600, 1.3))):
        x = -20 + row * 20
        shapes = []
        while x < 920:
            s = hh * rnd.uniform(0.9, 1.1)
            shapes += [Circ(x, y - 28 * s, 14 * s), RRect(x - 22 * s, y - 16 * s, x + 22 * s, 640, 10 * s)]
            x += rnd.uniform(40, 56)
        flat(c, shapes, (20, 10, 18) if row == 0 else (12, 6, 12))
    # footlights
    for x in range(40, 900, 80):
        flat(c, Ell(x, 450, 12, 4), (255, 230, 140))
    piece(c, Poly(star_pts(230, 150, 30, 13)), (240, 200, 70) if "star" not in d else (200, 200, 220), border=1, border_col=(110, 90, 100), shadow=SMALL)


L555_ELEMENTS = [
    E("dove%d" % i, (lambda x, y: lambda c, m: piece(c, [Ell(x, y, 12, 7), Circ(x + 10, y - 4, 5), Poly([(x - 2, y - 2), (x - 14, y - 16), (x + 4, y - 6)])],
                                                    (250, 250, 250), border=1, shadow=SMALL))(x, y),
      anim=dict(driftVelocity=(30, 30), driftLength=200, driftFade=True, phase=i / 2))
    for i, (x, y) in enumerate(((540, 300), (520, 310)))
] + [
    E("sparkle", lambda c, m: [flat(c, Poly(star_pts(460 + 20 * math.cos(a), 300 + 20 * math.sin(a), 6, 2, points=4)), (255, 240, 160)) for a in (0, 2.1, 4.2)],
      pivot=(460, 300), daynight="untinted", anim=dict(rotateSpeed=90, twinkle=0.4, twinkleSpeed=2.0)),
    E("spot", lambda c, m: soft_union(c, [Poly([(440, 0), (460, 0), (620, 440), (300, 440)])], (255, 250, 220), 0.14, spread=20), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.4)),
]

L555_DIFFS = [
    ("trunk", 220, 410, 0),
    ("tassel", 820, 322, 0),
    ("rabbit", 530, 312, 0),
    ("hoop", 700, 330, 0),
    ("star", 230, 150, 0),
]


# =================================================================== Level 556 puppet theatre in the park
def l556_bg(c, d):
    sky(c, (140, 200, 240), (232, 240, 236), 300)
    cloud_bg(c, 160, 60, 0.7)
    far_round_trees(c, 200, 40, (120, 176, 120), 5561)
    piece(c, RRect(-10, 240, 910, 612, 0), (140, 196, 100), shadow=LAYER)
    tree_round(c, 70, 300, s=1.9)
    tree_round(c, 830, 290, s=2.0, col=(90, 160, 90) if "tree" not in d else (230, 150, 60))
    # puppet booth
    piece(c, RRect(300, 120, 600, 420, 4), (200, 60, 70), border=2, shadow=PROP)
    for x in range(310, 600, 30):
        flat(c, RRect(x, 120, x + 15, 420, 0), (220, 80, 90))
    piece(c, Poly([(280, 126), (620, 126), (590, 70), (310, 70)]), (250, 200, 60) if "roof" not in d else (90, 160, 220), border=1.5, shadow=PROP)
    flat(c, RRect(340, 170, 560, 300, 3), (60, 40, 60))
    piece(c, [Poly([(332, 170), (380, 170), (350, 300), (332, 300)]), Poly([(568, 170), (520, 170), (550, 300), (568, 300)])], (60, 110, 200),
          border=1, shadow=SMALL)
    flat(c, RRect(330, 300, 570, 312, 2), (250, 200, 60))
    piece(c, RRect(380, 330, 520, 370, 4), (250, 246, 236), border=1, shadow=SMALL)
    sign_box(c, 396, 340, 504, 360, (200, 60, 70), 5562, vertical=False)
    # children sitting on the grass
    for k, (x, b, col, hair) in enumerate(((180, 500, (240, 120, 90), (40, 30, 30)), (260, 520, (90, 160, 230), (220, 180, 90)), (360, 510, (250, 210, 80), (90, 60, 40)),
                                           (460, 520, (120, 200, 140), (40, 30, 30)), (560, 510, (220, 110, 160), (90, 60, 40)), (640, 500, (150, 130, 200), (40, 30, 30)),
                                           (300, 590, (250, 160, 80), (90, 60, 40)), (520, 600, (90, 190, 200), (220, 180, 90)))):
        if k == 4 and "kid" in d:
            col = (250, 250, 250)
        seated(c, x, b, col, hair=hair, h=1.3, style="twin" if k % 3 == 1 else "short")
    # picnic basket + balloon seller (right)
    piece(c, [RRect(100, 560, 170, 600, 4), Thick(110, 562, 160, 562, 3)], (200, 150, 90) if "basket" not in d else (90, 150, 210), border=1.2, shadow=PROP)
    c.ellipse_ring(135, 556, 24, 18, 3, (170, 120, 70), ymax=556)
    modern(c, 760, 600, (240, 200, 90), bottom=(60, 60, 80), hair=(130, 130, 140), h=2.3, glasses=True)
    flat(c, Thick(774, 520, 780, 470, 1.2), (90, 90, 100))
    # bench + parents
    piece(c, [RRect(640, 420, 820, 432, 3), RRect(648, 432, 656, 470, 2), RRect(804, 432, 812, 470, 2), RRect(640, 400, 820, 410, 3)], (130, 90, 60),
          border=1.2, shadow=PROP)
    modern(c, 700, 430, (60, 110, 180), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.7)
    modern(c, 760, 430, (220, 120, 140), bottom=(60, 60, 80), hair=(90, 60, 40), h=1.7, style="long")


def puppet(x, col, hat):
    def d(c, m):
        piece(c, [RRect(x - 16, 250, x + 16, 300, 6), Circ(x, 236, 16)], col, border=1.2, shadow=SMALL)
        flat(c, Circ(x, 238, 12), (246, 214, 186))
        flat(c, [Circ(x - 4, 236, 2), Circ(x + 4, 236, 2)], INK)
        flat(c, Ell(x, 246, 5, 3), (220, 70, 70))
        flat(c, Poly([(x - 16, 226), (x + 16, 226), (x, 196)]), hat)
    return d


L556_ELEMENTS = [
    E("pupA", puppet(410, (90, 160, 90), (220, 70, 70)), pivot=(410, 300), anim=dict(swingAngle=10, swingSpeed=0.7, bobAmplitude=(0, 8), bobSpeed=0.9)),
    E("pupB", puppet(490, (200, 120, 200), (60, 110, 200)), pivot=(490, 300), anim=dict(swingAngle=10, swingSpeed=0.6, phase=0.5, bobAmplitude=(0, 8), bobSpeed=0.8)),
    E("balloons", balloon_bunch(780, 440, [(240, 80, 90), (90, 170, 240), (250, 200, 60), (130, 210, 120)], string_to=(780, 470)), pivot=(780, 470),
      anim=dict(swingAngle=6, swingSpeed=0.5)),
    bird_el("bird", 500, 40, s=8, speed=-18),
]

L556_DIFFS = [
    ("tree", 830, 200, 0),
    ("roof", 450, 96, 0),
    ("kid", 560, 470, 0),
    ("basket", 135, 576, 0),
]


# =================================================================== Level 557 ballet studio
def dancer(c, x, base, top, h=2.0, hair=(40, 30, 30), arms_up=False, tutu=(250, 200, 220)):
    modern(c, x, base, top, bottom=(246, 214, 186), hair=hair, h=h, style="short")
    flat(c, [RRect(x - 5 * h, base - 20 * h, x - 2 * h, base, 1), RRect(x + 2 * h, base - 20 * h, x + 5 * h, base, 1)], (250, 210, 210))
    piece(c, Ell(x, base - 20 * h, 18 * h, 5 * h), tutu, border=1, shadow=SMALL)
    hx, hy = x + 1 * h, base - 46 * h
    flat(c, Circ(hx - 2 * h, hy - 8 * h, 4 * h), hair)
    if arms_up:
        flat(c, [Thick(x - 8 * h, base - 36 * h, x - 4 * h, base - 60 * h, 2 * h), Thick(x + 8 * h, base - 36 * h, x + 4 * h, base - 60 * h, 2 * h)], (246, 214, 186))


def l557_bg(c, d):
    room(c, (238, 230, 236), (232, 224, 230), (190, 150, 110), (176, 136, 98), floor_y=460)
    # tall windows (left)
    for k, x in enumerate((30, 170)):
        piece(c, RRect(x, 40, x + 110, 380, 50), (250, 250, 250), border=1.5, shadow=PROP)
        flat(c, RRect(x + 10, 50, x + 100, 370, 44), (190, 220, 240))
        flat(c, [Thick(x + 55, 50, x + 55, 370, 3), Thick(x + 10, 200, x + 100, 200, 3)], (250, 250, 250))
        curtain = (240, 180, 200)
        flat(c, [Poly([(x - 6, 40), (x + 14, 40), (x + 4, 380), (x - 10, 380)]), Poly([(x + 116, 40), (x + 96, 40), (x + 106, 380), (x + 120, 380)])], curtain)
    # mirror wall + barre (right)
    piece(c, RRect(320, 60, 900, 440, 2), (220, 232, 238), border=1.5, shadow=PROP)
    for x in range(320, 900, 145):
        flat(c, Thick(x, 60, x, 440, 2), (200, 214, 222))
    for k in range(6):
        flat(c, Poly([(360 + k * 90, 80), (380 + k * 90, 80), (340 + k * 90, 200), (320 + k * 90, 200)]), (240, 248, 252, 0.7))
    flat(c, Thick(320, 330, 900, 330, 6), (190, 150, 90))
    for x in (360, 620, 860):
        flat(c, Thick(x, 330, x, 440, 4), (170, 130, 80))
    # reflections in the mirror (pale)
    for x in (480, 680):
        dancer(c, x, 430, (230, 200, 220), h=1.6, hair=(150, 130, 130), tutu=(240, 220, 236))
    # piano (front left)
    piece(c, RRect(30, 420, 230, 560, 6), (40, 30, 30), border=2, border_col=(120, 100, 90), shadow=PROP)
    flat(c, RRect(30, 470, 230, 486, 2), (60, 50, 50))
    for k in range(14):
        flat(c, RRect(36 + k * 13.6, 488, 47 + k * 13.6, 520, 1), (250, 250, 246))
    modern(c, 140, 600, (150, 120, 180), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.2, glasses=True)
    piece(c, RRect(60, 430, 140, 466, 2), (250, 248, 236) if "sheet" not in d else (240, 200, 90), border=1, shadow=SMALL)
    # dancers
    dancer(c, 380, 560, (60, 60, 80), h=2.2, hair=(40, 30, 30), arms_up=True)
    dancer(c, 520, 580, (220, 110, 150) if "leotard" not in d else (90, 170, 120), h=2.3, hair=(220, 180, 90))
    dancer(c, 660, 560, (60, 60, 80), h=2.2, hair=(90, 60, 40), arms_up=True)
    dancer(c, 800, 590, (120, 150, 220), h=2.4, hair=(40, 30, 30), tutu=(250, 200, 220) if "tutu" not in d else (250, 230, 120))
    # water bottles + bag on the floor
    piece(c, RRect(270, 560, 330, 596, 8), (240, 120, 90) if "bag" not in d else (90, 140, 210), border=1.2, shadow=PROP)
    for k, x in enumerate((880, 868)):
        piece(c, RRect(x - 6, 500, x + 6, 540, 3), (90, 170, 230), border=1, shadow=SMALL)


L557_ELEMENTS = [
    E("twirl", lambda c, m: dancer(c, 380, 560, (60, 60, 80), h=2.2, hair=(40, 30, 30), arms_up=True), pivot=(380, 560),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.0)),
    E("notes", lambda c, m: [flat(c, [Circ(220 + k * 22, 420 - k * 14, 5), Thick(224 + k * 22, 420 - k * 14, 224 + k * 22, 400 - k * 14, 2)], (90, 60, 120))
                             for k in range(3)], anim=dict(driftVelocity=(10, 20), driftLength=50, driftFade=True)),
    E("sun", lambda c, m: soft_union(c, [Poly([(60, 60), (120, 60), (300, 460), (200, 460)])], (255, 250, 220), 0.12, spread=20), anim=dict(twinkle=0.2, twinkleSpeed=0.3)),
]

L557_DIFFS = [
    ("bag", 300, 578, 0),
    ("sheet", 100, 448, 0),
    ("leotard", 522, 506, 0),
    ("tutu", 800, 542, 0),
]


# =================================================================== Level 558 cooking class
def l558_bg(c, d):
    room(c, (236, 240, 236), (228, 234, 228), (200, 200, 200), (186, 186, 186), floor_y=480)
    # tiled splashback + shelves with jars
    for y in range(40, 280, 24):
        for x in range(0, W, 24):
            flat(c, RRect(x + 1, y + 1, x + 23, y + 23, 2), (226, 236, 240))
    wall_shelf(c, 30, 400, 110)
    for k in range(8):
        col = [(240, 120, 90), (250, 200, 70), (120, 190, 110), (200, 120, 200)][k % 4]
        if k == 5 and "jar" in d:
            col = (90, 150, 230)
        piece(c, [RRect(44 + k * 44, 70, 76 + k * 44, 110, 5), RRect(48 + k * 44, 62, 72 + k * 44, 72, 2)], col, border=1, shadow=SMALL)
    # hanging pots rack
    flat(c, Thick(500, 60, 860, 60, 4), (120, 120, 130))
    for k, x in enumerate((540, 620, 700, 780, 840)):
        flat(c, Thick(x, 60, x, 80, 2), (120, 120, 130))
        piece(c, [Ell(x, 96, 24, 16), Thick(x, 80, x, 86, 3)], (190, 120, 70) if not (k == 2 and "pot" in d) else (90, 140, 200), border=1, shadow=SMALL)
    # teacher's counter + oven (back)
    counter(c, 40, 420, 280, 400, (250, 250, 250), top=(200, 200, 210))
    piece(c, RRect(480, 200, 640, 400, 4), (200, 204, 214), border=1.5, shadow=PROP)
    flat(c, RRect(500, 280, 620, 380, 4), (60, 60, 70))
    flat(c, RRect(510, 290, 610, 370, 3), (250, 180, 90))
    flat(c, [Circ(520 + k * 26, 230, 7) for k in range(4)], (60, 60, 70))
    # chef behind the counter
    modern(c, 220, 400, (250, 250, 250), bottom=(60, 60, 70), hair=(40, 30, 30), h=2.8)
    piece(c, [RRect(202, 244, 242, 266, 6), Circ(210, 246, 11), Circ(232, 244, 11)], (250, 250, 250) if "hat" not in d else (240, 120, 120), border=1,
          shadow=SMALL)
    piece(c, [Ell(140, 270, 34, 10)], (200, 200, 210), border=1, shadow=SMALL)
    flat(c, [Circ(130, 264, 6), Circ(146, 266, 6)], (240, 90, 60))
    # fridge (right)
    piece(c, RRect(700, 150, 870, 420, 8), (240, 242, 246), border=1.5, shadow=PROP)
    flat(c, [Thick(700, 260, 870, 260, 2), Thick(850, 180, 850, 240, 4), Thick(850, 280, 850, 380, 4)], (180, 186, 196))
    flat(c, [RRect(720, 170, 760, 200, 2)], (250, 200, 80) if "note" not in d else (120, 200, 230))
    # students' stations (front)
    for k, x in enumerate((170, 450, 730)):
        piece(c, [RRect(x - 120, 500, x + 120, 516, 3), RRect(x - 110, 516, x + 110, 600, 3)], (250, 250, 250), border=1.5, shadow=PROP)
        flat(c, RRect(x - 110, 520, x + 110, 532, 1), (90, 160, 200) if not (k == 2 and "station" in d) else (240, 160, 80))
    for k, (x, col, hair, st) in enumerate(((120, (240, 120, 90), (40, 30, 30), "short"), (230, (120, 190, 160), (220, 180, 90), "long"),
                                           (400, (90, 150, 220), (90, 60, 40), "short"), (500, (250, 210, 80), (40, 30, 30), "twin"),
                                           (690, (200, 110, 160), (90, 60, 40), "long"), (790, (150, 150, 170), (130, 130, 140), "short"))):
        modern(c, x, 560, col, bottom=(60, 60, 80), hair=hair, h=2.0, style=st)
    for x in (170, 450, 730):
        piece(c, Ell(x, 494, 26, 10), (250, 250, 250), border=1, shadow=SMALL)
        flat(c, Ell(x, 490, 20, 6), (250, 230, 170))


L558_ELEMENTS = steam_el("st", 150, 254, n=3, r=7, rise=16, length=50) + [
    E("whisk", lambda c, m: (flat(c, Thick(450, 490, 470, 450, 3), (150, 150, 160)), c.ellipse_ring(452, 486, 6, 9, 1.4, (150, 150, 160))),
      pivot=(460, 470), anim=dict(swingAngle=16, swingSpeed=1.6)),
    E("glow", lambda c, m: soft_union(c, [RRect(510, 290, 610, 370, 3)], (255, 200, 120), 0.4, spread=16), daynight="untinted", anim=dict(twinkle=0.2, twinkleSpeed=0.8)),
    E("timer", lambda c, m: (piece(c, Circ(380, 260, 14), (250, 120, 90), border=1, shadow=SMALL), flat(c, Thick(380, 260, 380, 250, 2), INK)), pivot=(380, 274),
      anim=dict(swingAngle=6, swingSpeed=2.0)),
]

L558_DIFFS = [
    ("jar", 280, 86, 0),
    ("pot", 700, 92, 0),
    ("hat", 222, 254, 0),
    ("note", 740, 185, 0),
    ("station", 730, 526, 0),
]


# =================================================================== Level 559 chess in the park
def l559_bg(c, d):
    sky(c, (140, 200, 240), (232, 240, 236), 300)
    far_round_trees(c, 190, 40, (120, 176, 120), 5591)
    piece(c, RRect(-10, 250, 910, 612, 0), (200, 186, 160), shadow=LAYER)
    for y in range(270, H, 30):
        off = 0 if (y // 30) % 2 else 40
        for x in range(-80 + off, W, 80):
            flat(c, Thick(x, y, x, y + 30, 1.2), (186, 172, 146))
        flat(c, Thick(0, y, W, y, 1.2), (186, 172, 146))
    # big tree with birdcages on a branch
    piece(c, [Thick(140, 520, 150, 200, 22), Thick(150, 260, 320, 150, 10), Thick(150, 240, 40, 160, 9)], (120, 84, 60), shadow=PROP)
    piece(c, [Circ(80, 120, 70), Circ(180, 90, 80), Circ(300, 110, 70), Circ(30, 170, 50)], (90, 160, 90), shadow=PROP)
    for k, x in enumerate((220, 290)):
        flat(c, Thick(x, 196 - (x - 150) * 0.6 + 20, x, 240, 1.4), (90, 90, 100))
        for j in range(6):
            flat(c, Thick(x - 15 + j * 6, 240, x - 15 + j * 6, 284, 1.4), (190, 160, 90))
        piece(c, Poly([(x - 18, 242), (x + 18, 242), (x, 226)]), (190, 160, 90), shadow=SMALL)
        flat(c, Thick(x - 18, 284, x + 18, 284, 3), (190, 160, 90))
        piece(c, [Ell(x, 268, 10, 12), Circ(x + 5, 254, 7)], (250, 200, 60) if not (k == 1 and "bird" in d) else (90, 170, 220), border=1, shadow=None)
    # pavilion (right back)
    piece(c, RRect(600, 160, 890, 176, 2), (190, 60, 50), shadow=SMALL)
    for x in (620, 740, 860):
        piece(c, RRect(x, 170, x + 12, 300, 1), (190, 60, 50), shadow=SMALL)
    piece(c, Poly([(580, 166), (910, 166), (880, 130), (750, 100), (620, 130)]), (60, 110, 90) if "roof" not in d else (150, 90, 60), border=1.5, shadow=PROP)
    # stone chess tables
    for k, x in enumerate((420, 720)):
        piece(c, [Ell(x, 420, 90, 22), RRect(x - 16, 420, x + 16, 500, 3), Ell(x, 500, 34, 8)], (190, 190, 196), border=1.5, shadow=PROP)
        flat(c, Ell(x, 418, 70, 16), (230, 210, 160))
        for i in range(5):
            flat(c, Thick(x - 60 + i * 30, 404, x - 56 + i * 30, 432, 1), (150, 120, 80))
        rnd = random.Random(5592 + k)
        for _ in range(8):
            px, py = x + rnd.uniform(-56, 56), 418 + rnd.uniform(-10, 10)
            piece(c, Ell(px, py, 7, 4), (250, 246, 236) if rnd.random() < 0.5 else (200, 60, 60), border=0.6, shadow=None)
        for sx in (x - 110, x + 110):
            piece(c, [Ell(sx, 470, 26, 8), RRect(sx - 12, 470, sx + 12, 510, 3)], (190, 190, 196), border=1.2, shadow=PROP)
    # players + onlookers
    modern(c, 310, 480, (250, 250, 250), bottom=(60, 60, 80), hair=(240, 240, 246), h=2.0, glasses=True)
    modern(c, 530, 480, (90, 120, 160) if "jacket" not in d else (200, 90, 70), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.0)
    modern(c, 610, 480, (200, 180, 150), bottom=(60, 60, 70), hair=(240, 240, 246), h=2.0)
    modern(c, 830, 480, (120, 140, 120), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.0, glasses=True)
    for k, (x, col) in enumerate(((390, (180, 160, 140)), (460, (110, 130, 170)), (700, (150, 110, 90)), (760, (200, 200, 210)))):
        modern(c, x, 600, col, bottom=(50, 50, 60), hair=[(240, 240, 246), (130, 130, 140)][k % 2], h=2.3)
    # thermos + teacup on the second table
    piece(c, [RRect(680, 380, 700, 416, 5)], (220, 70, 70) if "thermos" not in d else (90, 170, 120), border=1, shadow=SMALL)
    # bench + pigeons area
    piece(c, [RRect(20, 560, 160, 572, 3), RRect(28, 572, 36, 606, 2), RRect(144, 572, 152, 606, 2)], (130, 90, 60), shadow=PROP)


L559_ELEMENTS = [
    E("pig%d" % i, (lambda x, y: lambda c, m: (piece(c, [Ell(x, y, 10, 6), Circ(x + 8, y - 7, 5)], (150, 150, 170), border=1, shadow=SMALL),
                                              flat(c, Poly([(x + 12, y - 8), (x + 17, y - 6), (x + 12, y - 5)]), (230, 160, 60))))(x, y),
      pivot=(x, y + 6), anim=dict(bobAmplitude=(8, 0), bobSpeed=0.25, stretch=(0, 0.1), scaleSpeed=1.6, phase=i / 3))
    for i, (x, y) in enumerate(((220, 580), (260, 590), (560, 590)))
] + [
    E("fan", lambda c, m: (piece(c, Poly([(312, 440), (340, 420), (346, 440)]), (240, 240, 230), border=1, shadow=SMALL)), pivot=(312, 440),
      anim=dict(swingAngle=20, swingSpeed=1.2)),
    E("tea", lambda c, m: soft_union(c, [Circ(690, 374, 4)], (250, 250, 250), 0.7, spread=4),
      anim=dict(driftVelocity=(2, 12), driftLength=26, driftFade=True, driftGrow=1.6)),
    bird_el("bird", 500, 60, s=8, speed=-18),
]

L559_DIFFS = [
    ("bird", 290, 262, 0),
    ("roof", 750, 140, 0),
    ("jacket", 531, 435, 0),
    ("thermos", 690, 398, 0),
]


LEVELS = [
    ("Level550", "花园婚礼", l550_bg, L550_ELEMENTS, L550_DIFFS, 60, OPTS),
    ("Level551", "毕业典礼", l551_bg, L551_ELEMENTS, L551_DIFFS, 60, OPTS),
    ("Level552", "科技展", l552_bg, L552_ELEMENTS, L552_DIFFS, 60, OPTS),
    ("Level553", "草地音乐节", l553_bg, L553_ELEMENTS, L553_DIFFS, 60, OPTS),
    ("Level554", "时装秀", l554_bg, L554_ELEMENTS, L554_DIFFS, 60, OPTS),
    ("Level555", "魔术表演", l555_bg, L555_ELEMENTS, L555_DIFFS, 60, OPTS),
    ("Level556", "木偶剧场", l556_bg, L556_ELEMENTS, L556_DIFFS, 60, OPTS),
    ("Level557", "芭蕾舞室", l557_bg, L557_ELEMENTS, L557_DIFFS, 60, OPTS),
    ("Level558", "烹饪课", l558_bg, L558_ELEMENTS, L558_DIFFS, 60, OPTS),
    ("Level559", "公园象棋", l559_bg, L559_ELEMENTS, L559_DIFFS, 60, OPTS),
]
