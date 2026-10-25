# -*- coding: utf-8 -*-
"""Everyday-town themes, part 11: sports and hobbies (paper-craft, full-bleed, no real brands or logos):
  Level600 攀岩馆   - a climbing gym: wall with coloured holds, roped climbers, belayers, crash mats
  Level601 蹦床乐园 - a trampoline park: grid of trampolines, jumpers in the air, foam pit, dodgeball court
  Level602 卡丁车   - a go-kart track: kerbs, tyre walls, karts racing, start gantry, spectators
  Level603 城市马拉松 - a city marathon: runners on the avenue, water station, arch, cheering crowd
  Level604 皮划艇   - kayaking on a river gorge: kayaks, paddlers, rapids, pine banks
  Level605 滑翔伞   - paragliding over a valley: colourful wings, take-off slope, village far below
  Level606 飞盘狗   - frisbee dogs in the park: dogs leaping, owners throwing, agility hoops
  Level607 海边瑜伽 - sunrise yoga on the beach: mats, poses, palms, calm sea
  Level608 冲浪     - surfing: big waves, surfers on boards, lifeguard tower, boards in the sand
  Level609 冰壶     - a curling rink: house rings, stones sliding, sweepers, scoreboard
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, palm, rock, sky, tree_pine, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_modern import crowd
from levels_daily3 import room
from levels_daily6 import flash_el
from levels_daily7 import sea

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)


def hold(c, x, y, col, r=9):
    piece(c, Poly([(x - r, y + r * 0.5), (x - r * 0.3, y - r), (x + r, y - r * 0.4), (x + r * 0.6, y + r)]), col, border=0.8, shadow=None)


def kart(c, x, base, col, driver=(250, 250, 250), helmet=(220, 60, 60), s=1.0):
    piece(c, [Poly([(x - 40 * s, base - 10 * s), (x + 44 * s, base - 10 * s), (x + 40 * s, base - 24 * s), (x - 30 * s, base - 26 * s)])], col, border=1.2, shadow=PROP)
    for wx in (x - 28 * s, x + 30 * s):
        piece(c, Circ(wx, base - 8 * s, 9 * s), (40, 40, 46), shadow=SMALL)
    piece(c, [RRect(x - 10 * s, base - 46 * s, x + 6 * s, base - 22 * s, 4)], driver, border=1, shadow=None)
    piece(c, Circ(x - 2 * s, base - 54 * s, 9 * s), helmet, border=1, shadow=None)
    flat(c, RRect(x + 2 * s, base - 58 * s, x + 10 * s, base - 50 * s, 2), (60, 80, 110))


def runner(c, x, base, top, bib=(250, 250, 250), h=1.8, hair=(40, 30, 30), style="short"):
    modern(c, x, base, top, bottom=(40, 40, 50), hair=hair, h=h, style=style)
    flat(c, RRect(x - 5 * h, base - 34 * h, x + 5 * h, base - 26 * h, 1), bib)


def wing(c, x, y, cols, w=90):
    pts = [(x + w * math.cos(math.radians(a)), y - w * 0.35 * math.sin(math.radians(a))) for a in range(200, 341, 10)]
    n = len(pts) - 1
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        flat(c, Poly([(x0, y0), (x1, y1), (x1, y1 + 14), (x0, y0 + 14)]), cols[i % len(cols)])
    flat(c, [Thick(pts[0][0], pts[0][1] + 14, x - 4, y + 70, 1), Thick(pts[-1][0], pts[-1][1] + 14, x + 4, y + 70, 1), Thick(x, y - w * 0.35 + 14, x, y + 70, 1)],
         (90, 90, 100))


# =================================================================== Level 600 climbing gym
def l600_bg(c, d):
    room(c, (200, 206, 214), (194, 200, 210), (60, 120, 180), (50, 106, 166), floor_y=520)
    # climbing wall panels (angled)
    for k, (x0, x1, col) in enumerate(((20, 300, (230, 220, 200)), (300, 600, (200, 210, 230)), (600, 880, (230, 210, 220)))):
        piece(c, Poly([(x0, 40), (x1, 40), (x1 + (20 if k == 1 else 0), 520), (x0 - (20 if k == 1 else 0), 520)]), col, border=1.5, shadow=PROP)
    rnd = random.Random(6001)
    pal = [(240, 80, 80), (250, 200, 50), (90, 170, 90), (60, 120, 220), (200, 100, 210), (250, 140, 40)]
    for k in range(48):
        x, y = rnd.uniform(40, 860), rnd.uniform(60, 500)
        col = pal[k % 6]
        hold(c, x, y, col, r=rnd.choice((7, 9, 12)))
    # route tape + top anchors
    for x in (160, 460, 740):
        flat(c, Circ(x, 50, 6), (150, 150, 160))
    # crash mats
    piece(c, RRect(-10, 520, 910, 556, 6), (60, 60, 70), shadow=SMALL)
    # climbers on ropes
    for k, (x, y, col) in enumerate(((160, 260, (240, 120, 60)), (460, 200, (90, 160, 220)), (740, 320, (220, 90, 140)))):
        flat(c, Thick(x, 50, x, y - 80, 1.4), (240, 200, 60))
        if k == 1 and "climber" in d:
            col = (120, 200, 120)
        modern(c, x, y, col, bottom=(40, 40, 50), hair=(40, 30, 30), h=1.6, style="long" if k == 2 else "short")
        flat(c, [Thick(x - 10, y - 60, x - 20, y - 80, 3), Thick(x + 10, y - 60, x + 20, y - 76, 3)], (246, 214, 186))
    # belayers + chalk bag
    for k, (x, col) in enumerate(((210, (60, 60, 70)), (520, (150, 120, 180)))):
        modern(c, x, 600, col if not (k == 1 and "belayer" in d) else (90, 190, 160), bottom=(40, 40, 50), hair=[(90, 60, 40), (220, 180, 90)][k], h=2.2,
               style="long" if k else "short")
        flat(c, Thick(x - 10, 520, x - 50 if k == 0 else x - 60, 300, 1.4), (240, 200, 60))
    piece(c, [RRect(820, 560, 860, 600, 8)], (220, 70, 70) if "bag" not in d else (90, 160, 220), border=1.2, shadow=PROP)
    flat(c, Ell(840, 560, 18, 5), (250, 250, 250))
    # bench with shoes
    piece(c, [RRect(640, 570, 780, 582, 3), RRect(648, 582, 656, 610, 2), RRect(764, 582, 772, 610, 2)], (150, 110, 80), border=1.2, shadow=PROP)
    for k, col in enumerate(((250, 160, 40), (60, 60, 70))):
        piece(c, Poly([(674 + k * 50, 570), (716 + k * 50, 570), (720 + k * 50, 558), (688 + k * 50, 548)]), col if not (k == 0 and "shoe" in d) else (120, 190, 230),
              border=0.8, shadow=None)


L600_ELEMENTS = [
    E("swing", lambda c, m: (flat(c, Thick(740, 50, 740, 240, 1.4), (240, 200, 60)), modern(c, 740, 320, (220, 90, 140), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.6,
                                                                                          style="long")), pivot=(740, 50), anim=dict(swingAngle=2, swingSpeed=0.5)),
    E("chalk", lambda c, m: soft_union(c, [Circ(470, 150, 6)], (250, 250, 250), 0.7, spread=8), anim=dict(driftVelocity=(6, -10), driftLength=40, driftFade=True)),
]

L600_DIFFS = [
    ("climber", 461, 145, 0),
    ("belayer", 521, 545, 0),
    ("shoe", 697, 560, 0),
    ("bag", 840, 580, 0),
]


# =================================================================== Level 601 trampoline park
def l601_bg(c, d):
    room(c, (240, 236, 246), (232, 226, 240), (60, 60, 80), (50, 50, 70), floor_y=420)
    # angled wall trampolines
    for k in range(6):
        x = 20 + k * 150
        piece(c, Poly([(x, 140), (x + 140, 140), (x + 140, 420), (x, 420)]), [(60, 140, 220), (240, 90, 90), (250, 200, 60)][k % 3], border=1.5, shadow=PROP)
        flat(c, RRect(x + 10, 150, x + 130, 410, 4), (40, 40, 50))
    # grid of trampolines on the floor
    for r, y in enumerate((440, 510)):
        for k in range(5):
            x = 30 + k * 176
            pad = [(60, 140, 220), (240, 90, 90), (250, 200, 60)][(k + r) % 3]
            if r == 1 and k == 3 and "pad" in d:
                pad = (120, 200, 120)
            piece(c, RRect(x, y, x + 160, y + 60, 4), pad, border=1.2, shadow=SMALL)
            flat(c, RRect(x + 10, y + 8, x + 150, y + 52, 3), (40, 40, 50))
    # foam pit (right edge) + safety net + banner
    piece(c, RRect(700, 40, 890, 130, 3), (250, 250, 250) if "banner" not in d else (250, 220, 120), border=1.5, shadow=PROP)
    sign_box(c, 714, 60, 876, 110, (220, 70, 90), 6011, vertical=False)
    for x in range(20, 900, 30):
        flat(c, Thick(x, 140, x, 130, 1), (90, 90, 100))
    # spectators on a bench (left top)
    piece(c, [RRect(30, 100, 260, 112, 3)], (150, 110, 80), shadow=PROP)
    for k, (x, col) in enumerate(((60, (240, 200, 90)), (130, (90, 150, 110)), (200, (200, 110, 150)))):
        if k == 1 and "parent" in d:
            col = (250, 120, 60)
        modern(c, x, 110, col, bottom=(40, 40, 50), hair=(40, 30, 30), h=1.2)
    # dodgeball balls + cubbies with shoes
    for k, (x, y) in enumerate(((620, 590), (660, 596), (420, 600))):
        piece(c, Circ(x, y, 18 if k == 2 else 14), (240, 90, 90) if not (k == 2 and "ball" in d) else (90, 200, 220), border=1, shadow=SMALL)


def jumper(eid, x, base, col, h=1.6, phase=0.0, hair=(40, 30, 30)):
    return E(eid, lambda c, m: (modern(c, x, base, col, bottom=(40, 40, 50), hair=hair, h=h),
                                flat(c, [Thick(x - 8 * h, base - 34 * h, x - 16 * h, base - 54 * h, 2.4 * h), Thick(x + 8 * h, base - 34 * h, x + 16 * h, base - 54 * h, 2.4 * h)],
                                     (246, 214, 186))),
             pivot=(x, base), anim=dict(bobAmplitude=(0, 70), bobSpeed=0.7, bounce=True, phase=phase))


L601_ELEMENTS = [jumper("j1", 110, 490, (240, 120, 60)), jumper("j2", 460, 490, (90, 170, 230), phase=0.3, hair=(220, 180, 90)),
                 jumper("j3", 820, 560, (200, 110, 200), phase=0.6), jumper("j4", 290, 560, (120, 200, 120), h=1.4, phase=0.8)]

L601_DIFFS = [
    ("pad", 638, 540, 0),
    ("parent", 131, 76, 0),
    ("ball", 420, 600, 0),
    ("banner", 795, 85, 0),
]


# =================================================================== Level 602 go-kart track
def l602_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 240)
    cloud_bg(c, 160, 60, 0.7)
    far_round_trees(c, 220, 30, (110, 170, 120), 6021)
    # grandstand roof + spectators
    piece(c, RRect(560, 120, 910, 240, 2), (150, 156, 170), border=1.5, shadow=PROP)
    piece(c, Poly([(550, 124), (920, 124), (910, 96), (560, 96)]), (220, 70, 70) if "roof" not in d else (60, 120, 200), border=1.5, shadow=PROP)
    crowd(c, 580, 900, 150, 4, 6022, step=14, dy=20)
    piece(c, RRect(-10, 240, 910, 612, 0), (130, 180, 100), shadow=LAYER)
    # track asphalt loop with red-white kerbs
    piece(c, Poly([(-10, 300), (910, 300), (910, 380), (200, 380), (200, 460), (910, 460), (910, 560), (-10, 560)]), (90, 90, 100), shadow=SMALL)
    for x in range(-10, 910, 30):
        flat(c, RRect(x, 296, x + 15, 304, 0), (220, 60, 60))
        flat(c, RRect(x + 15, 296, x + 30, 304, 0), (250, 250, 250))
        flat(c, RRect(x, 556, x + 15, 564, 0), (220, 60, 60))
        flat(c, RRect(x + 15, 556, x + 30, 564, 0), (250, 250, 250))
    # tyre walls
    for k, x in enumerate((40, 80, 120)):
        piece(c, [Ell(x, 410, 20, 8), RRect(x - 20, 400, x + 20, 440, 2)], (40, 40, 46) if not (k == 1 and "tyre" in d) else (60, 110, 190), shadow=SMALL)
        flat(c, Thick(x - 20, 420, x + 20, 420, 3), (250, 250, 250))
    # start gantry with lights + chequered line
    flat(c, [Thick(300, 300, 300, 230, 4), Thick(500, 300, 500, 230, 4)], (90, 96, 110))
    piece(c, RRect(296, 220, 504, 246, 3), (40, 40, 50), border=1.2, shadow=SMALL)
    for k in range(5):
        flat(c, Circ(340 + k * 30, 233, 8), (220, 60, 60) if not (k == 4 and "light" in d) else (90, 220, 120))
    for k in range(10):
        flat(c, RRect(390 + (k % 2) * 8, 300 + k * 8, 398 + (k % 2) * 8, 308 + k * 8, 0), (250, 250, 250))
    # marshal with a flag + pit board
    modern(c, 860, 600, (250, 160, 40) if "marshal" not in d else (90, 180, 120), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.2)
    flat(c, Thick(870, 540, 890, 480, 3), (150, 150, 160))
    piece(c, RRect(880, 470, 910, 494, 1), (250, 250, 250), shadow=None)
    piece(c, [RRect(20, 580, 160, 606, 3)], (240, 240, 244) if "board" not in d else (250, 210, 90), border=1.2, shadow=PROP)
    sign_box(c, 30, 586, 150, 600, (60, 60, 70), 6023, vertical=False)


L602_ELEMENTS = [
    E("k1", lambda c, m: kart(c, 0, 360, (220, 60, 60), helmet=(250, 250, 250)), anim=dict(drift_across(-40, 44, 120, start=200))),
    E("k2", lambda c, m: kart(c, 0, 370, (60, 120, 210), helmet=(250, 200, 60)), anim=dict(drift_across(-40, 44, 120, start=650))),
    E("k3", lambda c, m: kart(c, 0, 530, (250, 190, 50), helmet=(60, 60, 70), s=1.2), anim=dict(drift_across(-48, 53, -140, start=400))),
    E("k4", lambda c, m: kart(c, 0, 540, (90, 170, 110), helmet=(220, 60, 60), s=1.2), anim=dict(drift_across(-48, 53, -140, start=850))),
    E("flag", lambda c, m: (piece(c, Poly([(890, 480), (910, 476), (910, 494), (890, 494)]), (60, 60, 70), shadow=None)), pivot=(890, 488),
      anim=dict(swingAngle=14, swingSpeed=1.2)),
]

L602_DIFFS = [
    ("roof", 735, 110, 0),
    ("tyre", 80, 420, 0),
    ("light", 460, 233, 0),
    ("marshal", 861, 545, 0),
    ("board", 90, 593, 0),
]


# =================================================================== Level 603 city marathon
def l603_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 240)
    far_skyline(c, 240, 80, 220, (176, 190, 214), 6031, win=(200, 210, 230))
    # inflatable finish arch
    piece(c, [RRect(600, 120, 640, 400, 16), RRect(260, 110, 640, 160, 22)], (240, 90, 60), border=1.5, shadow=PROP)
    piece(c, RRect(260, 120, 300, 400, 16), (240, 90, 60) if "arch" not in d else (60, 140, 210), border=1.5, shadow=PROP)
    piece(c, RRect(330, 120, 570, 150, 4), (250, 250, 250), border=1, shadow=None)
    sign_box(c, 350, 126, 550, 144, (240, 90, 60), 6032, vertical=False)
    # avenue
    piece(c, RRect(-10, 300, 910, 612, 0), (120, 120, 128), shadow=LAYER)
    flat(c, [Thick(x, 460, x + 40, 460, 4) for x in range(0, 900, 90)], (250, 250, 240))
    # barriers + crowd on the far side
    piece(c, RRect(-10, 300, 910, 320, 0), (200, 200, 206), shadow=SMALL)
    crowd(c, -6, 906, 270, 2, 6033, step=14, dy=16)
    for x in range(0, 900, 60):
        piece(c, RRect(x + 4, 304, x + 56, 330, 2), (250, 250, 250), border=1, shadow=SMALL)
        flat(c, RRect(x + 8, 312, x + 52, 320, 1), (60, 120, 200))
    # water station (right)
    piece(c, [RRect(720, 360, 900, 376, 3), RRect(730, 376, 738, 420, 2), RRect(882, 376, 890, 420, 2)], (240, 240, 244), border=1.2, shadow=PROP)
    for k in range(6):
        piece(c, RRect(730 + k * 26, 340, 748 + k * 26, 360, 3), (90, 170, 230), border=0.8, shadow=None)
    modern(c, 810, 420, (250, 200, 60) if "cup" not in d else (200, 110, 200), bottom=(40, 40, 50), hair=(90, 60, 40), h=1.6, style="long")
    # runners (static)
    for k, (x, b, col, hair, st) in enumerate(((80, 540, (220, 60, 60), (40, 30, 30), "short"), (200, 600, (60, 120, 210), (220, 180, 90), "long"),
                                               (380, 560, (250, 200, 60), (40, 30, 30), "short"), (520, 600, (120, 190, 120), (90, 60, 40), "short"),
                                               (660, 560, (200, 110, 200), (40, 30, 30), "long"))):
        if k == 2 and "vest" in d:
            col = (250, 250, 250)
        runner(c, x, b, col, h=2.0 if b > 580 else 1.8, hair=hair, style=st)
    # balloon cluster on the arch post
    for k, col in enumerate(((240, 90, 120), (250, 200, 60), (90, 170, 230))):
        piece(c, Ell(250 + k * 14, 96 - (k % 2) * 10, 12, 14), col if not (k == 1 and "balloon" in d) else (150, 110, 220), border=1, shadow=SMALL)


L603_ELEMENTS = [
    E("pass", lambda c, m: runner(c, 0, 420, (240, 140, 60), h=1.6), anim=dict(drift_across(-14, 14, 70, start=300), bobAmplitude=(0, 4), bobSpeed=2.0)),
    E("pass2", lambda c, m: runner(c, 0, 440, (90, 90, 110), h=1.7, hair=(220, 180, 90)), anim=dict(drift_across(-14, 14, 60, start=700), bobAmplitude=(0, 4), bobSpeed=2.0)),
    E("cheer", lambda c, m: [piece(c, Poly([(x, 266), (x + 16, 254), (x + 18, 266)]), col, border=0.6, shadow=None)
                             for x, col in ((120, (250, 200, 60)), (420, (240, 90, 120)), (760, (90, 170, 230)))], pivot=(450, 266),
      anim=dict(bobAmplitude=(0, 6), bobSpeed=1.4)),
    E("heli", lambda c, m: (piece(c, Ell(0, 60, 26, 12), (250, 250, 250), border=1, shadow=SMALL), flat(c, Thick(-30, 46, 30, 46, 2), (60, 60, 70))),
      anim=dict(drift_across(-30, 30, 20, start=100))),
]

L603_DIFFS = [
    ("arch", 280, 280, 0),
    ("cup", 811, 380, 0),
    ("vest", 381, 512, 0),
    ("balloon", 264, 86, 0),
]


# =================================================================== Level 604 kayaking in a gorge
def kayak(c, x, base, col, top, paddle=(250, 200, 60), s=1.0):
    piece(c, Poly([(x - 60 * s, base - 6 * s), (x - 20 * s, base - 14 * s), (x + 20 * s, base - 14 * s), (x + 64 * s, base - 6 * s), (x + 20 * s, base + 2 * s),
                   (x - 20 * s, base + 2 * s)]), col, border=1.2, shadow=SMALL)
    modern(c, x, base - 4 * s, top, bottom=top, hair=(40, 30, 30), h=1.1 * s)
    piece(c, Ell(x + 1 * s, base - 55 * s, 9 * s, 6 * s), (250, 250, 250), shadow=None)


def l604_bg(c, d):
    sky(c, (130, 190, 236), (226, 236, 244), 260)
    # gorge walls with pines
    piece(c, Poly([(-10, 60), (200, 100), (280, 300), (240, 420), (-10, 440)]), (170, 130, 100), border=1.5, shadow=LAYER)
    piece(c, Poly([(910, 40), (700, 90), (620, 300), (660, 420), (910, 440)]), (160, 124, 96), border=1.5, shadow=LAYER)
    for x, b in ((40, 90), (120, 100), (780, 80), (860, 70)):
        tree_pine(c, x, b, h=90, col=(60, 120, 80))
    far_ridge(c, 200, 40, (150, 186, 170), 6041, x0=240, x1=660)
    # river
    piece(c, Poly([(240, 260), (660, 260), (910, 420), (910, 612), (-10, 612), (-10, 420)]), (90, 160, 200), shadow=SMALL)
    for k in range(14):
        rnd = random.Random(6042 + k)
        x, y = rnd.uniform(100, 800), rnd.uniform(300, 600)
        flat(c, Thick(x, y, x + rnd.uniform(20, 50), y - 4, 3), (200, 230, 246))
    # boulders + rapids
    for k, (x, y, s) in enumerate(((330, 380, 1.2), (560, 440, 1.6), (180, 540, 1.4))):
        rock(c, x, y, s=s, col=(140, 136, 140) if not (k == 1 and "boulder" in d) else (190, 150, 110))
        flat(c, [Ell(x - 30 * s, y + 4, 16, 4), Ell(x + 30 * s, y + 4, 16, 4)], (240, 248, 252))
    # kayaks (static)
    kayak(c, 420, 350, (250, 190, 50), (220, 60, 60), s=0.9)
    kayak(c, 700, 520, (220, 70, 70) if "kayak" not in d else (90, 190, 120), (60, 120, 210), s=1.3)
    # guide on the bank with a throw bag + sign
    modern(c, 80, 450, (250, 160, 40) if "guide" not in d else (120, 120, 220), bottom=(40, 40, 50), hair=(90, 60, 40), h=1.6)
    piece(c, RRect(100, 404, 120, 424, 4), (220, 60, 60) if "throwbag" not in d else (60, 120, 200), border=1, shadow=SMALL)
    flat(c, Thick(800, 440, 800, 380, 3), (120, 90, 60))
    piece(c, RRect(770, 350, 830, 384, 3), (250, 200, 60) if "sign" not in d else (90, 170, 220), border=1.2, shadow=SMALL)


L604_ELEMENTS = [
    E("paddle1", lambda c, m: flat(c, [Thick(392, 320, 450, 300, 3), Ell(388, 322, 8, 4), Ell(454, 298, 8, 4)], (250, 200, 60)), pivot=(421, 310),
      anim=dict(swingAngle=24, swingSpeed=1.0)),
    E("paddle2", lambda c, m: flat(c, [Thick(660, 470, 740, 440, 4), Ell(654, 472, 10, 5), Ell(746, 438, 10, 5)], (250, 250, 250)), pivot=(700, 455),
      anim=dict(swingAngle=24, swingSpeed=1.0, phase=0.5)),
    E("rider", lambda c, m: kayak(c, 0, 580, (90, 170, 230), (250, 200, 60), s=1.2), anim=dict(drift_across(-72, 77, 40, start=200), bobAmplitude=(0, 3), bobSpeed=0.8)),
    E("spray", lambda c, m: soft_union(c, [Ell(560, 440, 40, 8)], (240, 248, 252), 0.7, spread=8), anim=dict(pulse=0.2, scaleSpeed=0.8, twinkle=0.3)),
    bird_el("bird", 450, 90, s=8, speed=-18),
]

L604_DIFFS = [
    ("boulder", 560, 410, 0),
    ("kayak", 700, 518, 0),
    ("throwbag", 110, 414, 0),
    ("guide", 81, 410, 0),
    ("sign", 800, 367, 0),
]


# =================================================================== Level 605 paragliding
def l605_bg(c, d):
    sky(c, (110, 176, 236), (226, 236, 246), 400)
    cloud_bg(c, 160, 70, 0.9)
    cloud_bg(c, 720, 50, 0.7)
    # valley far below
    far_ridge(c, 330, 60, (150, 186, 170), 6051)
    piece(c, Poly([(-10, 400), (910, 380), (910, 612), (-10, 612)]), (140, 186, 110), shadow=LAYER)
    for k in range(6):
        x = 300 + k * 70
        piece(c, RRect(x, 420 - (k % 2) * 6, x + 40, 446 - (k % 2) * 6, 2), [(250, 246, 236), (240, 220, 190)][k % 2], border=1, shadow=SMALL)
        flat(c, Poly([(x - 4, 422 - (k % 2) * 6), (x + 44, 422 - (k % 2) * 6), (x + 20, 406 - (k % 2) * 6)]), (200, 80, 70) if not (k == 3 and "roof" in d)
             else (60, 110, 190))
    flat(c, Poly([(500, 470), (560, 470), (700, 612), (600, 612)]), (110, 170, 210))
    tree_round(c, 780, 470, s=1.4, col=(90, 160, 90) if "tree" not in d else (230, 150, 60))
    piece(c, Poly([(598, 560), (650, 560), (642, 574), (606, 574)]), (220, 70, 60) if "boat" not in d else (250, 250, 250), border=1, shadow=SMALL)
    piece(c, [RRect(360, 470, 400, 520, 2), Poly([(356, 472), (404, 472), (380, 420)])], (250, 246, 236) if "church" not in d else (240, 200, 120), border=1.2,
          shadow=PROP)
    # take-off slope (left)
    piece(c, Poly([(-10, 260), (260, 360), (300, 612), (-10, 612)]), (120, 170, 90), shadow=LAYER)
    piece(c, Poly([(40, 330), (180, 370), (190, 400), (40, 370)]), (200, 200, 190) if "mat" not in d else (230, 160, 90), shadow=SMALL)
    flat(c, Thick(220, 360, 220, 300, 3), (150, 150, 160))
    piece(c, Poly([(221, 296), (270, 304), (270, 318), (221, 324)]), (250, 130, 50) if "sock" not in d else (90, 140, 220), border=1, shadow=SMALL)
    # pilot laying out a wing
    modern(c, 100, 360, (60, 120, 200) if "pilot" not in d else (250, 200, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.8)
    piece(c, Poly([(20, 400), (200, 420), (190, 440), (10, 430)]), (240, 90, 90) if "wing" not in d else (120, 200, 140), border=1, shadow=SMALL)
    # wind turbine on a far hill + birds
    flat(c, Thick(820, 380, 820, 300, 3), (240, 240, 244))


L605_ELEMENTS = [
    E("pg1", lambda c, m: (wing(c, 420, 120, [(240, 90, 90), (250, 200, 60), (240, 90, 90), (250, 200, 60)]), modern(c, 420, 220, (60, 60, 70), bottom=(40, 40, 50),
                                                                                                                   hair=(40, 30, 30), h=1.0)),
      pivot=(420, 120), anim=dict(bobAmplitude=(30, 14), bobSpeed=0.1)),
    E("pg2", lambda c, m: (wing(c, 700, 200, [(90, 170, 230), (250, 250, 250), (90, 170, 230), (250, 250, 250)], w=70),
                           modern(c, 700, 290, (220, 110, 150), bottom=(40, 40, 50), hair=(220, 180, 90), h=0.8)),
      pivot=(700, 200), anim=dict(bobAmplitude=(26, 12), bobSpeed=0.12, phase=0.5)),
    E("blades", lambda c, m: flat(c, [Thick(820 - 30 * math.cos(a), 300 - 30 * math.sin(a), 820, 300, 3) for a in (0.3, 2.4, 4.5)], (240, 240, 244)),
      pivot=(820, 300), anim=dict(rotateSpeed=90)),
    bird_el("hawk", 300, 250, s=11, speed=-16),
]

L605_DIFFS = [
    ("roof", 530, 410, 0),
    ("mat", 115, 365, 0),
    ("pilot", 101, 320, 0),
    ("sock", 245, 310, 0),
    ("tree", 780, 414, 0),
    ("boat", 624, 567, 0),
    ("church", 380, 480, 0),
]


# =================================================================== Level 606 frisbee dogs in the park
def dog(c, x, base, col, s=1.0, face_right=True, ears=(0, 0, 0)):
    k = 1 if face_right else -1
    piece(c, [Ell(x, base - 24 * s, 26 * s, 11 * s), Circ(x + k * 26 * s, base - 36 * s, 11 * s), Ell(x + k * 36 * s, base - 33 * s, 7 * s, 5 * s),
              Thick(x - k * 24 * s, base - 28 * s, x - k * 38 * s, base - 40 * s, 4 * s)] +
          [RRect(x + dx * s - 3 * s, base - 16 * s, x + dx * s + 3 * s, base, 1) for dx in (-16, -8, 10, 18)], col, border=1.2, shadow=PROP)
    flat(c, Ell(x + k * 20 * s, base - 40 * s, 5 * s, 8 * s), lit(col, 0.75))
    flat(c, [Circ(x + k * 30 * s, base - 39 * s, 1.8 * s), Circ(x + k * 42 * s, base - 34 * s, 2.2 * s)], INK)


def l606_bg(c, d):
    sky(c, (130, 196, 240), (230, 240, 236), 260)
    cloud_bg(c, 760, 60, 0.7)
    far_round_trees(c, 200, 40, (110, 170, 110), 6061)
    piece(c, RRect(-10, 240, 910, 612, 0), (140, 196, 100), shadow=LAYER)
    tree_round(c, 70, 300, s=1.8)
    tree_round(c, 840, 290, s=1.9, col=(90, 160, 90) if "tree" not in d else (230, 150, 60))
    # agility hoops + weave poles
    for k, x in enumerate((300, 600)):
        flat(c, [Thick(x - 40, 400, x - 40, 330, 3), Thick(x + 40, 400, x + 40, 330, 3)], (200, 200, 210))
        c.ellipse_ring(x, 330, 36, 36, 6, (240, 90, 90) if not (k == 1 and "hoop" in d) else (90, 170, 230))
    for k in range(6):
        flat(c, Thick(400 + k * 30, 470, 400 + k * 30, 420, 4), [(250, 200, 60), (250, 250, 250)][k % 2])
    # owners
    modern(c, 160, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.3, style="long")
    flat(c, Thick(176, 520, 210, 500, 3), (246, 214, 186))
    modern(c, 740, 600, (90, 150, 220) if "shirt" not in d else (220, 110, 150), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3)
    # resting dogs
    dog(c, 300, 590, (200, 160, 110), s=1.4)
    dog(c, 620, 580, (60, 60, 66) if "collar" not in d else (190, 130, 80), s=1.3, face_right=False)
    flat(c, RRect(568, 548, 586, 554, 2), (220, 60, 70))
    # water bowl + frisbee stack + blanket
    piece(c, Ell(420, 590, 24, 8), (60, 140, 220), border=1, shadow=SMALL)
    piece(c, Poly([(820, 540), (900, 530), (910, 590), (830, 600)]), (220, 70, 70) if "blanket" not in d else (90, 140, 200), border=1.2, shadow=SMALL)


L606_ELEMENTS = [
    E("leap", lambda c, m: dog(c, 450, 300, (240, 180, 90), s=1.4), pivot=(450, 300), anim=dict(bobAmplitude=(40, 50), bobSpeed=0.4, bounce=True)),
    E("disc", lambda c, m: piece(c, Ell(0, 220, 16, 5), (250, 200, 60), border=1, shadow=SMALL), anim=dict(drift_across(-16, 16, 70, start=200), bobAmplitude=(0, 20),
                                                                                                         bobSpeed=0.3)),
    E("wag", lambda c, m: flat(c, Thick(266, 552, 248, 536, 5), (200, 160, 110)), pivot=(266, 552), anim=dict(swingAngle=20, swingSpeed=1.6)),
    bird_el("bird", 400, 70, s=8, speed=-18),
]

L606_DIFFS = [
    ("tree", 840, 230, 0),
    ("hoop", 600, 330, 0),
    ("shirt", 741, 545, 0),
    ("collar", 610, 560, 0),
    ("blanket", 865, 565, 0),
]


# =================================================================== Level 607 sunrise beach yoga
def l607_bg(c, d):
    c.gradient(0, 300, (250, 190, 150), (250, 230, 190))
    piece(c, Circ(450, 270, 50), (255, 220, 140) if "sun" not in d else (250, 160, 120), border=1.5, shadow=None)
    soft_union(c, [Circ(450, 270, 50)], (255, 230, 160), 0.4, spread=40)
    sea(c, 280, top=(240, 190, 170), bottom=(120, 160, 200), seed=6071, n=10)
    flat(c, [Thick(380 + k * 12, 300 + k * 10, 520 - k * 12, 300 + k * 10, 3) for k in range(5)], (255, 230, 170, 0.7))
    # beach
    piece(c, Poly([(-10, 400), (910, 390), (910, 612), (-10, 612)]), (240, 220, 180), shadow=LAYER)
    palm(c, 60, 470, h=240, lean=30)
    palm(c, 860, 460, h=220, lean=-26)
    # mats + yogis
    pal = [(90, 170, 230), (240, 120, 160), (120, 200, 140), (250, 200, 70)]
    for k, (x, b) in enumerate(((200, 520), (380, 540), (560, 520), (740, 540))):
        col = pal[k]
        if k == 2 and "mat" in d:
            col = (150, 110, 220)
        piece(c, Poly([(x - 70, b), (x + 70, b - 6), (x + 76, b + 14), (x - 64, b + 20)]), col, border=1, shadow=SMALL)
    modern(c, 200, 520, (250, 250, 250), bottom=(60, 60, 80), hair=(40, 30, 30), h=2.0)
    flat(c, [Thick(186, 452, 166, 420, 3), Thick(216, 452, 236, 420, 3)], (246, 214, 186))
    modern(c, 380, 540, (220, 90, 120) if "top" not in d else (90, 170, 120), bottom=(40, 40, 60), hair=(90, 60, 40), h=2.0, style="long")
    flat(c, [Thick(362, 476, 330, 476, 3), Thick(398, 476, 430, 476, 3)], (246, 214, 186))
    modern(c, 740, 540, (60, 90, 150), bottom=(40, 40, 50), hair=(220, 180, 90), h=2.0, style="long")
    # instructor sitting + water bottles + towel
    modern(c, 560, 506, (250, 200, 80), bottom=(250, 200, 80), hair=(40, 30, 30), h=1.6)
    piece(c, RRect(820, 560, 900, 586, 3), (250, 250, 250) if "towel" not in d else (240, 140, 80), border=1, shadow=SMALL)
    for x in (280, 640):
        piece(c, RRect(x - 6, 540, x + 6, 570, 3), (120, 200, 230), border=1, shadow=SMALL)


L607_ELEMENTS = [
    E("waves", lambda c, m: flat(c, [Ell(100 + k * 180, 394, 70, 5) for k in range(5)], (250, 252, 255, 0.85)), anim=dict(bobAmplitude=(0, 5), bobSpeed=0.3)),
    E("breathe", lambda c, m: modern(c, 740, 540, (60, 90, 150), bottom=(40, 40, 50), hair=(220, 180, 90), h=2.0, style="long"), pivot=(740, 540),
      anim=dict(stretch=(0.02, 0.04), scaleSpeed=0.3)),
    bird_el("gull1", 300, 120, s=9, speed=-16),
    bird_el("gull2", 640, 160, s=8, speed=18),
]

L607_DIFFS = [
    ("sun", 450, 250, 0),
    ("mat", 560, 528, 0),
    ("top", 381, 485, 0),
    ("towel", 860, 573, 0),
]


# =================================================================== Level 608 surfing
def surfboard(c, x, y, col, ang=0.0, L=70):
    a = math.radians(ang)
    dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
    piece(c, [Thick(x - dx, y - dy, x + dx, y + dy, 12), Circ(x + dx, y + dy, 6)], col, border=1, shadow=SMALL)
    flat(c, Thick(x - dx * 0.8, y - dy * 0.8, x + dx * 0.8, y + dy * 0.8, 2), (250, 250, 250))


def l608_bg(c, d):
    sky(c, (110, 180, 236), (226, 238, 246), 260)
    cloud_bg(c, 160, 60, 0.8)
    sea(c, 200, top=(60, 150, 200), bottom=(40, 110, 170), seed=6081, n=8)
    # big curling wave
    piece(c, Poly([(200, 380), (360, 240), (480, 210), (580, 240), (540, 260), (500, 250), (460, 300), (440, 380)]), (60, 160, 200), border=1.5, shadow=PROP)
    flat(c, Poly([(480, 210), (580, 240), (540, 260), (500, 250)]), (240, 248, 252))
    flat(c, [Circ(560 + k * 10, 240 + k * 6, 10) for k in range(3)], (250, 252, 255))
    # surfer riding the wave (static)
    surfboard(c, 400, 330, (250, 190, 60) if "board" not in d else (220, 70, 120), ang=-20)
    modern(c, 400, 324, (40, 40, 50), bottom=(40, 40, 50), hair=(220, 180, 90), h=1.4)
    # beach
    piece(c, Poly([(-10, 420), (910, 400), (910, 612), (-10, 612)]), (240, 220, 180), shadow=LAYER)
    flat(c, Poly([(-10, 420)] + [(x, 416 + 6 * math.sin(x / 40)) for x in range(0, 920, 20)] + [(910, 410)]), (250, 252, 255))
    # lifeguard tower
    flat(c, [Thick(740, 560, 760, 440, 4), Thick(840, 560, 820, 440, 4)], (220, 220, 226))
    piece(c, RRect(730, 400, 850, 446, 3), (220, 70, 60) if "tower" not in d else (250, 200, 60), border=1.5, shadow=PROP)
    piece(c, Poly([(720, 404), (860, 404), (790, 370)]), (250, 250, 250), border=1, shadow=SMALL)
    modern(c, 790, 446, (250, 200, 60), bottom=(220, 60, 60), hair=(40, 30, 30), h=1.2)
    # boards stuck in the sand + surfers walking
    for k, (x, col) in enumerate(((120, (90, 170, 230)), (160, (250, 250, 250)), (200, (240, 120, 160)))):
        surfboard(c, x, 520, col if not (k == 2 and "stuck" in d) else (250, 200, 60), ang=-90, L=110)
    modern(c, 360, 600, (40, 40, 50), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3)
    surfboard(c, 400, 520, (120, 200, 140), ang=-70, L=110)
    modern(c, 560, 600, (250, 120, 90) if "rashie" not in d else (90, 170, 230), bottom=(60, 60, 80), hair=(220, 180, 90), h=2.2, style="long")
    piece(c, Poly([(620, 600), (700, 600), (660, 560)]), (250, 200, 60), border=1, shadow=SMALL)              # beach umbrella base
    flat(c, Thick(660, 600, 660, 500, 3), (150, 150, 160))
    piece(c, Poly([(600, 510), (720, 510), (660, 476)]), (60, 140, 200) if "umbrella" not in d else (240, 120, 160), border=1, shadow=SMALL)


L608_ELEMENTS = [
    E("paddler", lambda c, m: (surfboard(c, 0, 300, (250, 250, 250)), modern(c, 0, 302, (220, 60, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=0.9)),
      anim=dict(drift_across(-40, 40, 20, start=700), bobAmplitude=(0, 4), bobSpeed=0.4)),
    E("foam", lambda c, m: flat(c, [Ell(100 + k * 180, 412, 60, 5) for k in range(5)], (250, 252, 255, 0.85)), anim=dict(bobAmplitude=(0, 6), bobSpeed=0.3)),
    E("flag", lambda c, m: (flat(c, Thick(860, 404, 860, 360, 2), (150, 150, 160)), piece(c, Poly([(861, 360), (890, 366), (861, 376)]), (250, 200, 60), shadow=None)),
      pivot=(860, 368), anim=dict(stretch=(0.15, 0), scaleSpeed=1.4)),
    bird_el("gull", 300, 120, s=9, speed=-20),
]

L608_DIFFS = [
    ("board", 400, 330, 0),
    ("tower", 790, 423, 0),
    ("rashie", 561, 545, 0),
    ("umbrella", 660, 498, 0),
    ("stuck", 200, 520, 0),
]


# =================================================================== Level 609 curling rink
def stone(c, x, y, handle, s=1.0):
    piece(c, [Ell(x, y, 22 * s, 9 * s), RRect(x - 22 * s, y - 10 * s, x + 22 * s, y, 4)], (150, 150, 160), border=1, shadow=SMALL)
    flat(c, Ell(x, y - 10 * s, 22 * s, 7 * s), (180, 180, 190))
    flat(c, [RRect(x - 4 * s, y - 20 * s, x + 4 * s, y - 10 * s, 2), RRect(x - 4 * s, y - 20 * s, x + 14 * s, y - 14 * s, 2)], handle)


def l609_bg(c, d):
    room(c, (60, 80, 120), (66, 86, 128), (230, 240, 248), (216, 228, 240), floor_y=300)
    # banners + scoreboard
    piece(c, RRect(300, 40, 600, 140, 4), (30, 34, 44), border=1.5, shadow=PROP)
    for k in range(2):
        flat(c, RRect(320, 60 + k * 36, 360, 86 + k * 36, 3), [(220, 60, 60), (250, 200, 60)][k])
        for j in range(5):
            flat(c, RRect(380 + j * 40, 60 + k * 36, 406 + j * 40, 86 + k * 36, 2), (60, 64, 80))
        flat(c, RRect(560, 60 + k * 36, 586, 86 + k * 36, 2), (90, 220, 120) if not (k == 1 and "score" in d) else (240, 90, 80))
    for k, (x, col) in enumerate(((100, (220, 60, 60)), (800, (250, 200, 60)))):
        piece(c, Poly([(x - 50, 40), (x + 50, 40), (x + 50, 170), (x, 150), (x - 50, 170)]), col if not (k == 1 and "banner" in d) else (90, 170, 230), border=1.5, shadow=PROP)
        flat(c, Circ(x, 90, 20), (250, 250, 250))
    # spectators behind glass
    crowd(c, -6, 906, 230, 2, 6091, step=15, dy=18)
    piece(c, RRect(-10, 260, 910, 300, 0), (200, 220, 236), shadow=SMALL)
    # ice with the house (target rings)
    for r, col in ((130, (60, 120, 210)), (96, (250, 250, 250)), (62, (220, 60, 60)), (26, (250, 250, 250))):
        flat(c, Ell(650, 420, r * 1.4, r * 0.5), col)
    flat(c, [Thick(0, 420, W, 420, 2), Thick(650, 300, 650, 612, 2)], (220, 60, 60))
    flat(c, Thick(0, 520, W, 520, 3), (60, 120, 210))
    # stones at rest in the house
    stone(c, 610, 420, (220, 60, 60))
    if "stone" not in d:
        stone(c, 700, 440, (250, 200, 60))
    stone(c, 560, 396, (250, 200, 60))
    # skip in the house + players
    modern(c, 820, 470, (250, 200, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.8)
    flat(c, Thick(812, 400, 790, 470, 3), (90, 90, 100))
    modern(c, 120, 600, (220, 60, 60), bottom=(40, 40, 50), hair=(90, 60, 40), h=2.3)
    piece(c, RRect(40, 560, 70, 600, 6), (40, 40, 50) if "bag" not in d else (150, 110, 220), border=1, shadow=SMALL)


L609_ELEMENTS = [
    E("slide", lambda c, m: stone(c, 0, 500, (220, 60, 60), s=1.2), anim=dict(driftVelocity=(60, 2), driftStart=240, driftLength=260, phase=0.0)),
    E("sweep1", lambda c, m: (modern(c, 0, 560, (220, 60, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.9), flat(c, Thick(10, 480, 40, 540, 3), (90, 90, 100))),
      anim=dict(driftVelocity=(60, 2), driftStart=240, driftLength=260, phase=0.0, bobAmplitude=(6, 0), bobSpeed=2.0)),
    flash_el("flash", 200, 236, 0.3),
]

L609_DIFFS = [
    ("score", 573, 109, 0),
    ("banner", 800, 100, 0),
    ("stone", 700, 432, 0),
    ("bag", 55, 580, 0),
]


LEVELS = [
    ("Level600", "攀岩馆", l600_bg, L600_ELEMENTS, L600_DIFFS, 60, OPTS),
    ("Level601", "蹦床乐园", l601_bg, L601_ELEMENTS, L601_DIFFS, 60, OPTS),
    ("Level602", "卡丁车", l602_bg, L602_ELEMENTS, L602_DIFFS, 60, OPTS),
    ("Level603", "城市马拉松", l603_bg, L603_ELEMENTS, L603_DIFFS, 60, OPTS),
    ("Level604", "皮划艇", l604_bg, L604_ELEMENTS, L604_DIFFS, 60, OPTS),
    ("Level605", "滑翔伞", l605_bg, L605_ELEMENTS, L605_DIFFS, 60, OPTS),
    ("Level606", "飞盘狗", l606_bg, L606_ELEMENTS, L606_DIFFS, 60, OPTS),
    ("Level607", "海边瑜伽", l607_bg, L607_ELEMENTS, L607_DIFFS, 60, OPTS),
    ("Level608", "冲浪", l608_bg, L608_ELEMENTS, L608_DIFFS, 60, OPTS),
    ("Level609", "冰壶", l609_bg, L609_ELEMENTS, L609_DIFFS, 60, OPTS),
]
