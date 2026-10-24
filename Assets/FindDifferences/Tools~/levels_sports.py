# -*- coding: utf-8 -*-
"""Sports & competition themes (paper-craft, full-bleed, no real teams, leagues, brands or logos):
  Level160 篮球馆 - an indoor arena: crowded stands, hanging scoreboard, championship banners, hoop, players, bench
  Level161 网球场 - a tennis final seen from behind the baseline: windscreen fence, stands, net, umpire chair, players
  Level162 游泳馆 - a swimming hall: arched glass roof, bleachers, lane ropes, swimmers, diving tower, lifeguard
  Level163 田径场 - an athletics stadium: stands, big screen, cauldron, high jump, hurdles, sprinters, finish line
  Level164 棒球场 - a ballpark seen from behind home plate: outfield wall, scoreboard, diamond, pitcher, batter, umpire
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_bg, cloud_el, drift_across, sky, tree_round
from fills import far_round_trees, far_skyline
from stylekit import flame
from levels_akiba import modern, sign_box
from levels_misc import seg_text
from levels_modern import crowd, player
from levels_festival import bunting

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
NIGHT_EDGE = (120, 110, 140)
SKIN = (246, 214, 186)
HOME, AWAY = (214, 56, 60), (56, 108, 206)


def dpiece(c, shapes, col, border=1.5, shadow=PROP):
    """Paper piece for darker indoor scenes: cut edge in a muted tone instead of glowing white."""
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


def ad_boards(c, y0, y1, seed, x0=-10, x1=910, w=150):
    cols = [(240, 120, 40), (40, 170, 120), (60, 90, 200), (220, 60, 110), (250, 200, 60), (120, 80, 200), (60, 160, 220)]
    for i, x in enumerate(range(x0, x1, w)):
        col = cols[(i + seed) % len(cols)]
        piece(c, RRect(x + 2, y0, x + w - 2, y1, 1), col, border=1, shadow=SMALL)
        sign_box(c, x + 20, y0 + 5, x + w - 20, y1 - 5, lit(col, 0.8), seed * 10 + i, vertical=False)


def stands(c, y0, y1, seed, col=(130, 136, 150), step=16, edge=None):
    (dpiece if edge else piece)(c, RRect(-10, y0, 910, y1, 0), col, shadow=LAYER)
    for k, y in enumerate(range(y0 + 4, y1 - 2, step)):
        flat(c, RRect(-10, y, 910, y + step - 1, 0), lit(col, 1.08) if k % 2 else lit(col, 1.02))
    crowd(c, -6, 906, y0 + 10, int((y1 - y0 - 10) / step), seed, dy=step)


def flash_el(eid, pts, phase=0.0, interval=1.6):
    """Camera flashes popping in the crowd."""
    def d(c, m):
        for x, y in pts:
            flat(c, Poly(star_pts(x, y, 7, 2, points=4, rot=0)), (255, 255, 240))
    return E(eid, d, daynight="untinted", anim=dict(blinkInterval=interval, blinkDuration=0.25, phase=phase))


def racket(c, x0, y0, x1, y1, col=(60, 60, 70), head=(230, 70, 60)):
    """Racket from the grip (x0, y0) to the head centre (x1, y1)."""
    a = math.atan2(y1 - y0, x1 - x0)
    hx, hy = x1 + math.cos(a) * 4, y1 + math.sin(a) * 4
    piece(c, Thick(x0, y0, x1, y1, 3), col, shadow=SMALL)
    piece(c, Ell(hx, hy, 13, 13), head, shadow=SMALL)
    flat(c, Ell(hx, hy, 10, 10), (236, 236, 226))
    for k in (-5, 0, 5):
        flat(c, [Thick(hx + k, hy - 9, hx + k, hy + 9, 0.8), Thick(hx - 9, hy + k, hx + 9, hy + k, 0.8)], (180, 180, 170))


# =================================================================== Level 160 basketball arena
def l160_bg(c, d):
    c.rect(0, 0, W, 270, (40, 46, 70))
    for x in range(0, W + 60, 60):
        flat(c, [Thick(x, 0, x + 30, 34, 2), Thick(x + 60, 0, x + 30, 34, 2)], (70, 76, 102))
    flat(c, Thick(0, 34, W, 34, 3), (84, 90, 116))
    stands(c, 56, 238, 1601, col=(70, 76, 104), edge=True)
    # championship banners
    for k, x in enumerate((56, 130, 770, 844)):
        col = [(200, 50, 60), (240, 190, 60), (60, 110, 200), (246, 246, 240)][k]
        if k == 1 and "banner" in d:
            col = (90, 180, 110)
        dpiece(c, Poly([(x - 26, 36), (x + 26, 36), (x + 26, 124), (x, 140), (x - 26, 124)]), col, shadow=PROP)
        flat(c, Poly(star_pts(x, 72, 13, 5)), (246, 246, 240) if k != 3 else (200, 50, 60))
        flat(c, [Thick(x - 16, 104, x + 16, 104, 3), Thick(x - 12, 112, x + 12, 112, 3)], lit(col, 0.72))
    # hanging scoreboard
    flat(c, [Thick(380, 0, 380, 30, 3), Thick(520, 0, 520, 30, 3)], (100, 106, 130))
    dpiece(c, RRect(330, 26, 570, 132, 6), (30, 32, 44), shadow=PROP)
    flat(c, RRect(342, 38, 558, 120, 3), (16, 18, 26))
    flat(c, RRect(352, 48, 408, 110, 3), HOME)
    flat(c, RRect(492, 48, 548, 110, 3), AWAY if "jumbo" not in d else (250, 170, 40))
    seg_text(c, 366, 58, 40, "8", (250, 250, 250), width=4)
    seg_text(c, 506, 58, 40, "6", (250, 250, 250), width=4)
    seg_text(c, 428, 64, 28, "12", (255, 200, 60), width=3)
    for x in (340, 560):
        flat(c, RRect(x - 6, 130, x + 6, 150, 2), (60, 64, 80))
    # ad boards
    ad_boards(c, 238, 266, 3)
    # court
    c.rect(0, 266, W, H, (222, 176, 120))
    rnd = random.Random(1602)
    for y in range(266, H, 14):
        flat(c, Thick(0, y, W, y, 1), (206, 160, 106))
        off = rnd.uniform(0, 180)
        for x in range(-180, W + 180, 180):
            flat(c, Thick(x + off, y, x + off, y + 14, 1), (206, 160, 106))
    paint = (180, 60, 60)
    flat(c, Poly([(660, 292), (910, 292), (910, 452), (610, 452)]), paint)
    lines = (250, 250, 246)
    flat(c, [Thick(0, 292, W, 292, 3), Thick(660, 292, 610, 452, 3), Thick(610, 452, 910, 452, 3)], lines)
    c.ellipse_ring(610, 372, 34, 80, 3, lines, ymin=292)
    flat(c, Thick(300, 292, 262, 600, 3), lines)
    c.ellipse_ring(282, 440, 96, 40, 3, lines)
    flat(c, Ell(282, 440, 28, 12), HOME)
    # hoop (right)
    piece(c, RRect(826, 400, 904, 484, 4), (40, 70, 140), border=1.5, shadow=PROP)
    piece(c, [Thick(866, 404, 846, 232, 9), Thick(846, 236, 800, 240, 7)], (90, 96, 110), shadow=PROP)
    piece(c, RRect(700, 180, 820, 262, 3), (232, 242, 248), border=1.5, shadow=PROP)
    flat(c, RRect(706, 186, 814, 256, 2), (206, 226, 238))
    sq = (220, 60, 60) if "backboard" not in d else (40, 40, 50)
    flat(c, [RRect(738, 214, 782, 250, 1)], sq)
    flat(c, RRect(744, 220, 776, 250, 0), (206, 226, 238))
    # bench + coach (left foreground)
    piece(c, [RRect(-10, 520, 250, 536, 3), RRect(10, 536, 20, 580, 2), RRect(220, 536, 230, 580, 2)], (60, 64, 80), shadow=PROP)
    if "towel" not in d:
        piece(c, Poly([(120, 518), (166, 518), (170, 552), (116, 552)]), (250, 250, 246), border=1, shadow=SMALL)
        flat(c, Thick(118, 540, 168, 540, 3), HOME)
    cooler = (240, 140, 40) if "cooler" not in d else (70, 170, 110)
    piece(c, [RRect(180, 454, 236, 518, 8), RRect(176, 446, 240, 460, 4)], cooler, border=1.5, shadow=PROP)
    flat(c, RRect(200, 490, 216, 500, 2), (250, 250, 246))
    for k in range(3):
        piece(c, Poly([(30 + k * 22, 518), (46 + k * 22, 518), (44 + k * 22, 500), (32 + k * 22, 500)]), (250, 250, 246), shadow=SMALL)
    modern(c, 70, 600, (50, 50, 64), bottom=(40, 40, 50), hair=(60, 50, 50), h=2.2, glasses=True)
    piece(c, RRect(84, 520, 110, 554, 2), (250, 250, 246), border=1, shadow=SMALL)
    # players
    player(c, 480, 520, AWAY, h=2.0, number="5", hair=(30, 26, 30), skin=(170, 120, 90))
    player(c, 380, 560, HOME, h=2.2, number="3")
    player(c, 640, 500, HOME if "shirt" not in d else (90, 180, 110), h=1.9, number="7", hair=(90, 60, 40))
    player(c, 760, 580, AWAY, h=2.3, number="9", skin=(170, 120, 90))
    # referee (striped)
    player(c, 540, 420, (246, 246, 240), shorts=(30, 30, 36), h=1.5)
    flat(c, [Thick(530 + k * 7, 354, 530 + k * 7, 383, 2.4) for k in range(4)], (30, 30, 36))


def l160_ball(c, m):
    piece(c, Circ(414, 528, 11), (230, 110, 40), shadow=SMALL)
    flat(c, [Thick(403, 528, 425, 528, 1.2), Thick(414, 517, 414, 539, 1.2)], (120, 56, 30))


def l160_net(c, m):
    c.ellipse_ring(760, 266, 22, 5, 2.5, (230, 100, 40))
    flat(c, [Thick(740 + k * 8, 268, 746 + k * 5, 298, 1.2) for k in range(6)], (250, 250, 250))
    flat(c, [Thick(742, 280, 778, 280, 1), Thick(745, 290, 774, 290, 1)], (250, 250, 250))


L160_ELEMENTS = [
    E("ball", l160_ball, pivot=(414, 539), anim=dict(bobAmplitude=(0, 34), bobSpeed=1.2, bounce=True)),
    E("net", l160_net, pivot=(760, 266), anim=dict(swingAngle=3, swingSpeed=0.6)),
    flash_el("flash1", [(120, 180), (520, 200), (700, 96)], phase=0.0),
    flash_el("flash2", [(300, 120), (620, 160), (860, 210)], phase=0.5, interval=2.1),
    E("glow", lambda c, m: soft_union(c, [RRect(342, 38, 558, 120, 3)], (180, 200, 255), 0.2, spread=20), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=1.2)),
]

L160_DIFFS = [
    ("banner", 130, 88, 0),
    ("jumbo", 520, 79, 0),
    ("backboard", 760, 232, 0),
    ("shirt", 640, 470, 0),
    ("cooler", 208, 484, 0),
    ("towel", 143, 535, 0),
]


# =================================================================== Level 161 tennis court
def l161_bg(c, d):
    sky(c, (120, 184, 238), (210, 232, 248), 140)
    cloud_bg(c, 140, 40, 0.6)
    cloud_bg(c, 760, 30, 0.5)
    far_round_trees(c, 110, 22, (110, 170, 110), 1611)
    # stands on both sides of the umpire's box
    stands(c, 80, 180, 1612, col=(150, 156, 170))
    piece(c, RRect(390, 70, 510, 180, 2), (60, 110, 80), border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, RRect(402 + k * 36, 84, 430 + k * 36, 110, 2), (200, 220, 230))
    flat(c, RRect(400, 120, 500, 170, 2), (40, 80, 60))
    # windscreen fence + scoreboard
    piece(c, RRect(-10, 180, 910, 250, 0), (40, 110, 80), shadow=LAYER)
    for i, x in enumerate(range(30, 900, 170)):
        if 300 < x < 520:
            continue
        sign_box(c, x, 196, x + 110, 220, (250, 250, 246) if i != 4 or "sign" not in d else (250, 200, 60), 1613 + i, glyph=(40, 110, 80),
                 vertical=False)
    piece(c, RRect(350, 186, 550, 246, 3), (30, 36, 44), border=1.5, shadow=PROP)
    for r, (col, pts) in enumerate((((250, 250, 246), "64"), ((250, 220, 60), "37"))):
        flat(c, Circ(370, 202 + r * 26, 5), (250, 220, 60) if r == 0 else (30, 36, 44))
        flat(c, Thick(384, 202 + r * 26, 440, 202 + r * 26, 4), (190, 196, 206))
        seg_text(c, 470, 192 + r * 26, 20, pts, col, width=2.6)
    # court surround + court (trapezoid seen from behind the baseline)
    c.rect(0, 250, W, H, (90, 150, 110))
    flat(c, Poly([(250, 262), (650, 262), (860, 610), (40, 610)]), (60, 110, 180))
    ln = (250, 250, 246)
    flat(c, [Thick(250, 262, 40, 610, 3), Thick(650, 262, 860, 610, 3), Thick(250, 262, 650, 262, 3),
             Thick(290, 262, 116, 610, 2), Thick(610, 262, 784, 610, 2), Thick(450, 300, 450, 520, 2),
             Thick(222, 320, 678, 320, 2), Thick(160, 520, 740, 520, 2)], ln)
    # net
    piece(c, [RRect(150, 362, 158, 410, 1), RRect(742, 362, 750, 410, 1)], (60, 64, 70), shadow=SMALL)
    for x in range(160, 742, 8):
        flat(c, Thick(x, 370, x, 408, 0.8), (30, 30, 36))
    for y in range(372, 408, 8):
        flat(c, Thick(158, y, 742, y, 0.8), (30, 30, 36))
    flat(c, RRect(154, 362, 746, 370, 1), (250, 250, 246))
    flat(c, RRect(436, 364, 464, 408, 0), (250, 250, 246) if "strap" not in d else (220, 60, 60))
    # far player
    player(c, 560, 322, (250, 250, 246), shorts=(40, 60, 120), h=1.0, hair=(90, 60, 40))
    racket(c, 572, 290, 584, 276, head=(60, 60, 70))
    # umpire chair (right of the net)
    piece(c, [Thick(800, 470, 812, 330, 4), Thick(860, 470, 848, 330, 4), Thick(806, 420, 856, 420, 3)], (240, 240, 236), shadow=PROP)
    piece(c, RRect(796, 310, 864, 334, 3), (40, 110, 80), border=1.2, shadow=SMALL)
    modern(c, 830, 314, (40, 60, 110), bottom=(40, 60, 110), hair=(130, 130, 140), h=1.4)
    cap = (250, 250, 246) if "cap" not in d else (220, 60, 60)
    flat(c, [Ell(831, 244, 10, 5), RRect(831, 244, 846, 248, 2)], cap)
    piece(c, [Poly([(786, 236), (876, 236), (831, 214)])], (250, 250, 246), shadow=SMALL)
    flat(c, Thick(831, 236, 831, 250, 2), (220, 220, 220))
    # players' bench + parasol (left)
    piece(c, [RRect(10, 430, 110, 444, 3), RRect(18, 444, 26, 480, 2), RRect(94, 444, 102, 480, 2)], (40, 110, 80), shadow=PROP)
    flat(c, Thick(60, 432, 60, 330, 3), (220, 220, 220))
    para = (250, 200, 60) if "parasol" not in d else (230, 90, 150)
    piece(c, [Poly([(0, 350), (120, 350), (60, 310)])], para, border=1.5, shadow=PROP)
    flat(c, [Poly([(40, 350), (80, 350), (60, 310)])], (250, 250, 246))
    piece(c, RRect(24, 400, 50, 430, 3), (60, 140, 220), shadow=SMALL)
    # ball boy kneeling by the net post
    modern(c, 120, 440, (60, 110, 80), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.3)
    # ball basket (near left)
    if "basket" not in d:
        piece(c, [Poly([(176, 560), (240, 560), (232, 600), (184, 600)])], (90, 90, 100), border=1.2, shadow=PROP)
        for k in range(5):
            flat(c, Circ(186 + k * 11, 556, 6), (210, 230, 70))
    # near player (big, back view, ready to serve)
    player(c, 470, 610, (240, 120, 160) if "shirt" not in d else (110, 200, 220), shorts=(250, 250, 246), h=2.4, hair=(200, 150, 80))
    racket(c, 500, 520, 540, 470, head=(230, 70, 60))


L161_ELEMENTS = [
    E("ball", lambda c, m: piece(c, Circ(444, 470, 6), (220, 240, 70), shadow=SMALL), pivot=(444, 470),
      anim=dict(bobAmplitude=(0, 60), bobSpeed=0.5, bounce=True)),
    cloud_el("cloud", 420, 40, 0.5, 8),
    bird_el("bird", 600, 60, s=8, speed=-22),
    flash_el("flash", [(80, 120), (640, 100), (300, 150)], interval=2.4),
]

L161_DIFFS = [
    ("sign", 734, 208, 0),
    ("strap", 450, 386, 0),
    ("cap", 836, 246, 0),
    ("parasol", 60, 336, 0),
    ("basket", 208, 575, 0),
    ("shirt", 470, 532, 0),
]


# =================================================================== Level 162 swimming hall
WATER = (90, 170, 220)
ROPES = [300, 336, 376, 422, 474]
LANES = [318, 356, 399, 448, 490]
SWIMMERS = [(260, 318), (540, 356), (380, 399), (660, 448), (440, 490)]


def l162_bg(c, d):
    # arched glass roof
    c.rect(0, 0, W, 130, (196, 222, 240))
    for x in range(-40, W + 40, 90):
        flat(c, Thick(x, 0, x + 45, 130, 3), (150, 170, 190))
        flat(c, Thick(x + 90, 0, x + 45, 130, 3), (150, 170, 190))
    flat(c, [Thick(0, 60, W, 60, 3), Thick(0, 128, W, 128, 6)], (150, 170, 190))
    # bleachers with crowd
    stands(c, 130, 250, 1621, col=(160, 170, 186))
    # scoreboard + lap clock
    piece(c, RRect(340, 18, 560, 116, 4), (30, 40, 60), border=1.5, shadow=PROP)
    for r in range(4):
        col = (250, 220, 60)
        flat(c, Circ(360, 34 + r * 22, 6), [(220, 60, 60), (250, 250, 246), (60, 120, 220), (250, 200, 60)][r])
        flat(c, Thick(376, 34 + r * 22, 450, 34 + r * 22, 4), (180, 196, 214))
        seg_text(c, 480, 26 + r * 22, 16, "5%d" % (r * 2 + 1), col, width=2)
    piece(c, Circ(110, 66, 40), (250, 250, 246), border=1.5, shadow=PROP)
    c.ellipse_ring(110, 66, 40, 40, 4, (220, 60, 60) if "clock" not in d else (60, 120, 220))
    flat(c, [Thick(110, 66, 110, 36, 3), Thick(110, 66, 132, 76, 3)], (40, 40, 50))
    # flags string across the hall
    bunting(c, -10, 140, 910, 140, [(220, 60, 60), (250, 250, 246), (60, 120, 220), (250, 200, 60), (90, 180, 110)], 18, sag=30, size=14,
            swap=(12, (200, 120, 220)) if "flag" in d else None)
    # deck + pool
    c.rect(0, 250, W, H, (230, 236, 240))
    for x in range(0, W, 30):
        flat(c, Thick(x, 250, x, 290, 1), (210, 218, 226))
    flat(c, RRect(0, 290, W, 506, 0), WATER)
    rnd = random.Random(1622)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(296, 500)
        flat(c, Thick(x, y, x + rnd.uniform(16, 40), y, 1.6), (150, 210, 240))
    flat(c, RRect(0, 286, W, 294, 1), (250, 250, 250))
    # lane ropes (perspective: further = thinner)
    for k, y in enumerate(ROPES):
        r = 2.5 + k * 0.7
        for i, x in enumerate(range(0, W, int(10 + k * 2))):
            a, b = (220, 60, 60), (250, 250, 246)
            if k == 2 and "rope" in d and 520 < x < 700:
                a = b = (250, 200, 60)
            flat(c, Circ(x, y, r), a if (i // 3) % 2 else b)
    flat(c, RRect(0, 502, W, 512, 1), (250, 250, 250))
    for x in range(0, W, 46):
        flat(c, Thick(x, 512, x - 14, 600, 1.2), (210, 218, 226))
    for y in (544, 580):
        flat(c, Thick(0, y, W, y, 1.2), (210, 218, 226))
    # starting blocks (left end)
    for k, y in enumerate(LANES):
        s = 0.8 + k * 0.15
        piece(c, Poly([(6, y - 4 * s), (6 + 30 * s, y - 12 * s), (6 + 30 * s, y + 4 * s), (6, y + 8 * s)]), (240, 240, 246), shadow=SMALL)
        flat(c, Thick(6, y, 6 + 26 * s, y - 8 * s, 2 * s), (60, 120, 220))
    # swimmers (heads + wake) in lanes
    caps = [(250, 200, 60), (220, 60, 60), (250, 250, 246), (40, 40, 50), (90, 180, 110)]
    for k, (x, y) in enumerate(SWIMMERS):
        s = 1.1 + k * 0.18
        cap = caps[k] if not (k == 2 and "cap" in d) else (230, 120, 200)
        flat(c, Ell(x - 22 * s, y + 4 * s, 30 * s, 5 * s), (160, 214, 240))
        piece(c, Circ(x, y, 8 * s), cap, shadow=None)
        flat(c, RRect(x + 2 * s, y - 2 * s, x + 9 * s, y + 2 * s, 1), (30, 30, 40))
    # coach with a stopwatch + towel bench (near deck)
    piece(c, [RRect(300, 556, 520, 568, 3), RRect(312, 568, 320, 600, 2), RRect(500, 568, 508, 600, 2)], (90, 140, 200), shadow=PROP)
    for k, col in enumerate(((250, 250, 246), (250, 200, 60), (220, 60, 60))):
        piece(c, RRect(330 + k * 60, 540, 380 + k * 60, 558, 4), col, border=1, shadow=SMALL)
    modern(c, 600, 600, (40, 60, 110), bottom=(40, 40, 50), hair=(130, 130, 140), h=2.0)
    flat(c, Circ(624, 540, 7), (250, 200, 60))
    # diving tower (right)
    piece(c, [RRect(780, 120, 800, 290, 1), RRect(860, 150, 880, 290, 1)], (220, 224, 230), border=1.5, shadow=PROP)
    piece(c, RRect(700, 110, 820, 124, 2), (60, 120, 200), border=1.2, shadow=SMALL)
    diving = (250, 200, 60) if "dive" not in d else (220, 60, 60)
    piece(c, RRect(730, 180, 880, 192, 2), diving, border=1.2, shadow=SMALL)
    for y in range(140, 290, 14):
        flat(c, Thick(860, y, 880, y, 2), (160, 166, 176))
    modern(c, 720, 110, (40, 60, 110), bottom=(40, 60, 110), hair=(40, 30, 30), h=1.2)
    # lifeguard chair (left foreground)
    piece(c, [Thick(110, 600, 130, 500, 5), Thick(210, 600, 190, 500, 5), Thick(120, 560, 200, 560, 4)], (240, 240, 236), shadow=PROP)
    piece(c, RRect(104, 486, 216, 504, 3), (220, 60, 60), border=1.2, shadow=SMALL)
    modern(c, 160, 492, (220, 60, 60), bottom=(220, 60, 60), hair=(200, 150, 80), h=1.6)
    flat(c, Thick(200, 492, 200, 360, 2.4), (200, 200, 210))
    umb = (250, 250, 246) if "umbrella" not in d else (250, 200, 60)
    piece(c, Poly([(140, 370), (260, 370), (200, 334)]), umb, border=1.5, shadow=PROP)
    flat(c, Poly([(180, 370), (220, 370), (200, 334)]), (220, 60, 60))
    # kickboards + ring (right foreground)
    kb = [(250, 200, 60), (60, 120, 220), (220, 60, 60), (90, 180, 110)]
    if "kick" in d:
        kb[1] = (240, 140, 200)
    for k, col in enumerate(kb):
        piece(c, RRect(720 + k * 6, 570 - k * 12, 800 + k * 6, 600 - k * 12, 8), col, border=1.2, shadow=SMALL)
    piece(c, Ell(850, 586, 40, 14), (250, 140, 40), border=1.2, shadow=PROP)
    flat(c, Ell(850, 586, 20, 6), (230, 236, 240))


def swimmer_splash(x, y, s, ph):
    def d(c, m):
        flat(c, [Thick(x - 20 * s, y + 2 * s, x - 6 * s, y - 14 * s, 4 * s)], SKIN)
        piece(c, Circ(x - 28 * s, y + 4 * s, 6 * s), (220, 240, 250, 0.8), shadow=None)
    return E("arm%d" % x, d, pivot=(x - 8 * s, y + 2 * s), anim=dict(swingAngle=40, swingSpeed=0.7, phase=ph))


L162_ELEMENTS = [swimmer_splash(x, y, 1.1 + k * 0.18, k * 0.23) for k, (x, y) in enumerate(SWIMMERS) if k != 2] + [
    E("hand", lambda c, m: flat(c, Thick(110, 66, 100, 32, 2), (220, 60, 60)), pivot=(110, 66), anim=dict(rotateSpeed=-30)),
    E("diver", lambda c, m: modern(c, 840, 180, (220, 60, 60), bottom=(220, 60, 60), hair=(40, 30, 30), h=1.2), pivot=(840, 180),
      anim=dict(bobAmplitude=(0, 6), bobSpeed=0.8, bounce=True)),
    E("shine", lambda c, m: [flat(c, Thick(x, y, x + 30, y, 2), (220, 244, 255)) for x, y in ((90, 310), (420, 350), (760, 400), (300, 480))],
      daynight="untinted", anim=dict(twinkle=0.7, twinkleSpeed=0.9)),
]

L162_DIFFS = [
    ("clock", 110, 66, 0),
    ("flag", 680, 170, 0),
    ("rope", 610, 376, 0),
    ("dive", 810, 186, 0),
    ("cap", 380, 399, 0),
    ("umbrella", 200, 356, 0),
    ("kick", 770, 570, 0),
]


# =================================================================== Level 163 athletics stadium
TRACK = (200, 86, 64)


def hurdle(c, x, y, s, col):
    piece(c, [RRect(x - 2 * s, y - 30 * s, x + 2 * s, y, 1), RRect(x + 30 * s, y - 30 * s, x + 34 * s, y, 1)], (240, 240, 240), shadow=SMALL)
    piece(c, RRect(x - 4 * s, y - 34 * s, x + 36 * s, y - 24 * s, 1), col, shadow=SMALL)
    flat(c, RRect(x + 8 * s, y - 34 * s, x + 16 * s, y - 24 * s, 0), (250, 250, 250))


def runner(c, x, base, top, h=1.6, bib=None, hair=(40, 30, 30), skin=SKIN, stride=1.0):
    """Sprinter in mid-stride, facing right."""
    flat(c, [Thick(x - 2 * h, base - 22 * h, x - 14 * h * stride, base - 4 * h, 4 * h), Thick(x + 2 * h, base - 22 * h, x + 12 * h * stride, base - 10 * h, 4 * h),
             Thick(x + 12 * h * stride, base - 10 * h, x + 10 * h * stride, base, 3.6 * h)], skin)
    flat(c, [Ell(x - 16 * h * stride, base - 3 * h, 5 * h, 2.4 * h), Ell(x + 13 * h * stride, base - 1 * h, 5 * h, 2.4 * h)], (250, 250, 250))
    piece(c, RRect(x - 7 * h, base - 28 * h, x + 7 * h, base - 19 * h, 2), (40, 40, 50), shadow=SMALL)
    piece(c, RRect(x - 7 * h, base - 46 * h, x + 7 * h, base - 27 * h, 3), top, border=1.4, shadow=PROP)
    if bib:
        flat(c, RRect(x - 5 * h, base - 42 * h, x + 5 * h, base - 34 * h, 1), bib)
    flat(c, [Thick(x - 4 * h, base - 42 * h, x - 16 * h, base - 32 * h, 3 * h), Thick(x + 4 * h, base - 42 * h, x + 14 * h, base - 50 * h, 3 * h)], skin)
    hx, hy = x + 3 * h, base - 53 * h
    flat(c, Circ(hx, hy, 7 * h), skin)
    flat(c, Ell(hx - 1 * h, hy - 5 * h, 8 * h, 4 * h), hair)
    flat(c, Circ(hx + 3 * h, hy, 1.1 * h), INK)


def l163_bg(c, d):
    sky(c, (110, 176, 236), (206, 228, 246), 120)
    cloud_bg(c, 120, 30, 0.5)
    # stadium bowl
    piece(c, Poly([(-10, 40), (910, 40), (910, 64), (-10, 64)]), (220, 224, 232), border=1.5, shadow=PROP)
    stands(c, 64, 214, 1631, col=(150, 156, 172))
    # big screen
    piece(c, RRect(320, 50, 580, 170, 4), (30, 34, 44), border=2, shadow=PROP)
    scr = (40, 120, 70)
    flat(c, RRect(332, 62, 568, 158, 2), scr)
    flat(c, [RRect(342, 72 + k * 22, 450, 86 + k * 22, 2) for k in range(4)], lit(scr, 1.4))
    seg_text(c, 470, 74, 34, "98", (250, 250, 246) if "screen" not in d else (250, 200, 60), width=3.6)
    # cauldron on a tower (flame is an element)
    piece(c, [RRect(820, 70, 840, 214, 1)], (190, 190, 200), border=1.5, shadow=PROP)
    piece(c, Poly([(796, 70), (864, 70), (850, 92), (810, 92)]), (220, 180, 70), border=1.5, shadow=PROP)
    # flag poles (left)
    for k, x in enumerate((40, 80, 120)):
        flat(c, Thick(x, 214, x, 90, 2), (220, 220, 226))
        col = [(220, 60, 60), (60, 120, 220), (250, 200, 60)][k]
        if k == 1 and "flag" in d:
            col = (90, 180, 110)
        piece(c, Poly([(x, 90), (x + 36, 100), (x, 118)]), col, shadow=SMALL)
    ad_boards(c, 214, 236, 5)
    # infield
    c.rect(0, 236, W, 330, (100, 176, 90))
    for x in range(-60, 960, 120):
        flat(c, Poly([(x, 236), (x + 60, 236), (x + 70, 330), (x + 10, 330)]), (110, 186, 98))
    # long-jump sand pit with a rake
    piece(c, RRect(330, 288, 490, 320, 4), (240, 236, 230), shadow=SMALL)
    flat(c, RRect(336, 292, 484, 316, 3), (230, 206, 150))
    flat(c, [Thick(300, 304, 336, 304, 4)], (250, 250, 246))
    flat(c, [Thick(470, 296, 500, 262, 2), Thick(462, 290, 478, 302, 3)], (150, 110, 70))
    # high jump: standards, bar, mat
    mat = (60, 110, 200) if "mat" not in d else (220, 100, 60)
    piece(c, RRect(540, 280, 700, 322, 6), mat, border=1.5, shadow=PROP)
    flat(c, RRect(548, 286, 692, 296, 3), lit(mat, 1.2))
    piece(c, [RRect(560, 230, 566, 300, 1), RRect(674, 230, 680, 300, 1)], (240, 240, 240), shadow=SMALL)
    flat(c, Thick(560, 244, 680, 244, 3), (250, 200, 60))
    # javelin thrower (left infield)
    runner(c, 240, 316, (250, 250, 246), h=1.2, stride=0.6, hair=(90, 60, 40))
    flat(c, Thick(210, 248, 300, 226, 2), (220, 220, 226))
    # track
    flat(c, RRect(0, 330, W, 600, 0), TRACK)
    for k, y in enumerate((330, 372, 420, 474, 534, 600)):
        flat(c, Thick(0, y, W, y, 2 + k * 0.4), (250, 246, 240))
    for k, y in enumerate((360, 408, 462, 522, 590)):
        seg_text(c, 40, y - 22 - k * 3, 16 + k * 3, str(k + 1), (250, 246, 240), width=2)
    # hurdles in the far lanes
    for k, (x, y) in enumerate(((420, 368), (420, 416), (640, 368), (640, 416))):
        hurdle(c, x, y, 0.9, (250, 250, 250) if not (k == 1 and "hurdle" in d) else (250, 200, 60))
    # finish line + timing post (right)
    flat(c, RRect(800, 330, 812, 600, 0), (250, 250, 246))
    for y in range(330, 600, 12):
        flat(c, RRect(800 + (y // 12 % 2) * 6, y, 806 + (y // 12 % 2) * 6, y + 6, 0), (40, 40, 50))
    piece(c, [RRect(850, 250, 858, 470, 1)], (90, 96, 110), shadow=PROP)
    piece(c, RRect(820, 220, 890, 256, 3), (30, 34, 44) if "clock" not in d else (40, 90, 160), border=1.5, shadow=PROP)
    seg_text(c, 828, 228, 20, "102", (250, 80, 60), width=2.4)
    # official with a flag on a stand (near right)
    piece(c, RRect(860, 540, 900, 600, 2), (240, 240, 236), shadow=PROP)
    # sprinters (near lanes)
    runner(c, 330, 472, (60, 120, 220), h=1.4, bib=(250, 250, 246))
    runner(c, 500, 532, (220, 60, 60) if "runner" not in d else (250, 200, 60), h=1.6, bib=(250, 250, 246), skin=(170, 120, 90))
    runner(c, 640, 596, (90, 180, 110), h=1.8, bib=(250, 250, 246), hair=(200, 150, 80))


L163_ELEMENTS = flame("cauldron", 830, 72, s=2.4, glow_night=False) + [
    E("tape", lambda c, m: piece(c, Poly([(806, 500), (840, 492), (840, 500), (806, 508)]), (250, 250, 246), shadow=SMALL), pivot=(806, 504),
      anim=dict(swingAngle=6, swingSpeed=0.5)),
    E("official", lambda c, m: modern(c, 880, 540, (250, 250, 246), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.6), pivot=(880, 540),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.5)),
    flash_el("flash", [(100, 150), (700, 120), (280, 90), (600, 190)], interval=1.8),
    bird_el("bird", 700, 26, s=7, speed=18),
]

L163_DIFFS = [
    ("screen", 505, 92, 0),
    ("flag", 95, 100, 0),
    ("mat", 620, 300, 0),
    ("hurdle", 435, 398, 0),
    ("clock", 855, 238, 0),
    ("runner", 500, 490, 0),
]


# =================================================================== Level 164 ballpark
def l164_bg(c, d):
    sky(c, (120, 186, 238), (214, 234, 248), 120)
    cloud_bg(c, 760, 36, 0.6)
    far_skyline(c, 80, 20, 60, (176, 196, 216), 1641)
    # upper stands
    stands(c, 70, 170, 1642, col=(60, 100, 150))
    # scoreboard (centre)
    piece(c, RRect(300, 20, 600, 150, 4), (30, 60, 50), border=2, shadow=PROP)
    for r in range(2):
        flat(c, RRect(310, 34 + r * 30, 360, 58 + r * 30, 2), [HOME, AWAY if "score" not in d else (90, 180, 110)][r])
        for k in range(9):
            v = "0" if (r + k) % 3 else "1"
            col = (250, 250, 246)
            seg_text(c, 372 + k * 22, 36 + r * 30, 18, v, col, width=2)
    flat(c, [Circ(330 + k * 22, 120, 9) for k in range(3)], (250, 200, 60))
    flat(c, [Circ(410 + k * 22, 120, 9) for k in range(3)], (90, 220, 110) if "lights" not in d else (220, 60, 60))
    sign_box(c, 500, 108, 590, 132, (30, 60, 50), 1643, glyph=(250, 250, 246), vertical=False)
    # foul poles
    for x in (30, 870):
        piece(c, RRect(x - 4, 60, x + 4, 210, 1), (250, 200, 60) if not (x == 870 and "pole" in d) else (250, 250, 246), shadow=SMALL)
    # outfield wall with ads
    piece(c, RRect(-10, 170, 910, 214, 0), (40, 110, 70), shadow=LAYER)
    for i, x in enumerate(range(60, 860, 160)):
        col = [(250, 200, 60), (250, 250, 246), (220, 60, 60), (250, 250, 246), (60, 160, 220)][i]
        if i == 1 and "ad" in d:
            col = (240, 140, 200)
        sign_box(c, x, 178, x + 110, 204, col, 1644 + i, glyph=(40, 110, 70), vertical=False)
    # outfield grass (mowed stripes)
    c.rect(0, 214, W, H, (90, 170, 80))
    for k, x in enumerate(range(-200, 1100, 80)):
        if k % 2:
            flat(c, Poly([(x, 214), (x + 80, 214), (450 + (x + 80 - 450) * 2.4, 600), (450 + (x - 450) * 2.4, 600)]), (100, 182, 90))
    # infield dirt + grass diamond
    flat(c, Poly([(450, 250), (760, 380), (450, 610), (140, 380)]), (200, 150, 100))
    flat(c, Poly([(450, 290), (680, 384), (450, 540), (220, 384)]), (100, 182, 90))
    flat(c, [Thick(450, 560, 0, 300, 3), Thick(450, 560, 900, 300, 3)], (250, 250, 246))
    # pitcher's mound + bases
    flat(c, Ell(450, 400, 50, 16), (200, 150, 100))
    flat(c, RRect(438, 396, 462, 400, 1), (250, 250, 246))
    for x, y in ((450, 268), (230, 384)):
        piece(c, Poly([(x - 16, y), (x, y - 8), (x + 16, y), (x, y + 8)]), (250, 250, 246), shadow=SMALL)
    if "base" not in d:
        piece(c, Poly([(654, 384), (670, 376), (686, 384), (670, 392)]), (250, 250, 246), shadow=SMALL)
    # fielders
    for x, y in ((180, 250), (720, 250), (450, 246), (300, 330), (600, 330)):
        modern(c, x, y, (250, 250, 246), bottom=(250, 250, 246), hair=AWAY, h=0.8)
    modern(c, 700, 372, (250, 250, 246), bottom=(250, 250, 246), hair=AWAY, h=0.9)
    # pitcher
    modern(c, 450, 398, (250, 250, 246) if "cap" not in d else (250, 200, 60), bottom=(250, 250, 246), hair=AWAY, h=1.3)
    piece(c, Circ(436, 360, 5), (110, 70, 40), shadow=None)
    # home plate area (near)
    flat(c, Ell(450, 580, 160, 40), (200, 150, 100))
    piece(c, Poly([(436, 566), (464, 566), (464, 574), (450, 582), (436, 574)]), (250, 250, 246), shadow=SMALL)
    flat(c, [RRect(360, 556, 420, 596, 0), RRect(480, 556, 540, 596, 0)], (184, 136, 90))
    flat(c, [Thick(360, 556, 420, 556, 2), Thick(480, 556, 540, 556, 2)], (250, 250, 246))
    # batter (right box)
    hx, hy = modern(c, 510, 590, HOME, bottom=(250, 250, 246), hair=(40, 30, 30), h=2.2)
    helm = HOME if "helmet" not in d else (40, 40, 50)
    piece(c, [Ell(hx - 1, hy - 6, 17, 12)], helm, border=1.2, shadow=SMALL)
    flat(c, RRect(hx - 16, hy - 2, hx + 18, hy, 0), helm)
    flat(c, Circ(hx + 3, hy + 2, 1.6), INK)
    # catcher + umpire (crouching, foreground)
    piece(c, [Ell(450, 600, 34, 26)], (40, 40, 56), border=1.2, shadow=PROP)
    piece(c, Circ(450, 566, 16), (30, 30, 40), shadow=SMALL)
    flat(c, [Thick(436, 562, 464, 562, 1.4), Thick(436, 570, 464, 570, 1.4)], (150, 150, 160))
    piece(c, Ell(424, 584, 14, 12), (150, 90, 50), shadow=SMALL)
    # dugout (left) with players + bucket of balls
    piece(c, RRect(-10, 450, 160, 520, 4), (50, 60, 80), border=1.5, shadow=PROP)
    flat(c, RRect(0, 462, 150, 516, 2), (30, 34, 46))
    for x in (30, 70, 110):
        modern(c, x, 516, HOME, bottom=(250, 250, 246), hair=(40, 30, 30), h=1.2)
    piece(c, RRect(-10, 440, 170, 456, 2), (60, 120, 200), shadow=SMALL)
    # vendor (right)
    modern(c, 820, 600, (250, 200, 60) if "vendor" not in d else (90, 180, 110), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.2)
    piece(c, RRect(780, 540, 862, 566, 3), (250, 250, 246), border=1.2, shadow=SMALL)
    for k in range(3):
        flat(c, RRect(788 + k * 24, 532, 806 + k * 24, 544, 4), (220, 140, 80))
    # on-deck batter (left)
    modern(c, 250, 596, HOME, bottom=(250, 250, 246), hair=(40, 30, 30), h=1.8)
    piece(c, Thick(268, 540, 300, 470, 4), (200, 160, 110), shadow=SMALL)
    c.ellipse_ring(250, 594, 40, 10, 2, (250, 250, 246))


def l164_bat(c, m):
    piece(c, Thick(522, 500, 552, 440, 5), (200, 160, 110), shadow=SMALL)
    flat(c, Circ(522, 502, 5), (40, 40, 50))


L164_ELEMENTS = [
    E("bat", l164_bat, pivot=(522, 502), anim=dict(swingAngle=6, swingSpeed=0.4)),
    E("pitch", lambda c, m: piece(c, Circ(440, 380, 4), (250, 250, 246), shadow=None), pivot=(440, 380),
      anim=dict(driftVelocity=(10, -150), driftLength=180, driftFade=True, driftGrow=1.4)),
    E("flagL", lambda c, m: piece(c, Poly([(34, 60), (64, 66), (34, 80)]), HOME, shadow=SMALL), pivot=(34, 70), anim=dict(stretch=(0.15, 0), scaleSpeed=1.4)),
    bird_el("gull", 200, 40, s=9, speed=24),
    flash_el("flash", [(140, 100), (640, 140), (860, 110)], interval=2.0),
]

L164_DIFFS = [
    ("score", 335, 76, 0),
    ("lights", 432, 120, 0),
    ("pole", 870, 135, 0),
    ("ad", 275, 191, 0),
    ("base", 670, 384, 0),
    ("cap", 450, 362, 0),
    ("helmet", 510, 474, 0),
    ("vendor", 821, 520, 0),
]


LEVELS = [
    ("Level160", "篮球馆", l160_bg, L160_ELEMENTS, L160_DIFFS, 60, OPTS),
    ("Level161", "网球场", l161_bg, L161_ELEMENTS, L161_DIFFS, 60, OPTS),
    ("Level162", "游泳馆", l162_bg, L162_ELEMENTS, L162_DIFFS, 60, OPTS),
    ("Level163", "田径场", l163_bg, L163_ELEMENTS, L163_DIFFS, 60, OPTS),
    ("Level164", "棒球场", l164_bg, L164_ELEMENTS, L164_DIFFS, 60, OPTS),
]
