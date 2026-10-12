# -*- coding: utf-8 -*-
"""
More paper-craft levels, each with its own camera:
  Level12 纸艺小屋 - front cut-away (doll's house: every room open towards the viewer)
  Level13 纸艺林冠 - worm's-eye view (lying on the forest floor, looking straight up)
  Level14 纸艺窗外 - first person through a rainy window (room frame in front, landscape behind)
  Level15 纸艺雪村 - 45° isometric winter village
"""
import math
import random
import fill_levels

from fdcore import E, H, W, lit, on
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from levels_views import P, iso_box, iso_cyl, iso_quad, iso_roof, ISO_SH, THICK, drift_across, paper_cloud

OPTS = {"post": paper_post}
INK = (70, 55, 65)
PROP = (2, 4, 7, 0.42)
LAYER = (1, 3, 11, 0.36)
SMALL = (1, 2, 3, 0.3)


def tiled(unit, step, ks):
    """Repeat a drawing at k * step; drifting by exactly one step then loops seamlessly."""
    def d(c, m):
        for k in ks:
            unit(c, m, k * step[0], k * step[1])
    return d


def seamless_drift(step, speed):
    sx, sy = step
    ln = math.hypot(sx, sy)
    return dict(driftVelocity=(sx / ln * speed, -sy / ln * speed), driftLength=ln)


def smoke_puffs(x, y, n=3, col=(245, 240, 236), r=8, show="both", prefix="smoke"):
    return [E("%s%d" % (prefix, i), (lambda: lambda c, m: piece(c, Circ(x, y, r), col, shadow=SMALL))(), show=show,
              anim=dict(driftVelocity=(5, 20), driftLength=60, driftFade=True, driftGrow=1.2, phase=i / n))
            for i in range(n)]


# =================================================================== Level 12 (doll's house cut-away)
GF, F1, ATTIC = (394, 540), (249, 382), 237
HL, HR, HM = 160, 740, 450


def l12_background(c, d):
    """纸艺小屋 - static part"""
    c.rect(0, 0, W, 660, (192, 226, 240))
    fill_levels.back_Level12(c, d)
    piece(c, Poly([(-20, 560), (120, 520), (300, 540), (520, 515), (760, 535), (920, 515), (920, 660), (-20, 660)]),
          (130, 195, 110), shadow=LAYER)
    # tree and mailbox outside
    piece(c, [Thick(820, 545, 820, 400, 20)], (140, 95, 68), border=2, shadow=PROP)
    piece(c, [Circ(820, 370, 58), Circ(780, 400, 36), Circ(860, 400, 36)], (90, 168, 95), shadow=PROP)
    for x, y in ((800, 360), (842, 386), (815, 405)):
        piece(c, Circ(x, y, 7), (230, 70, 70), shadow=SMALL)
    piece(c, [Thick(90, 548, 90, 498, 5), RRect(70, 470, 112, 500, 8)], (90, 140, 210), border=2, shadow=PROP)
    flat(c, Thick(112, 474, 112, 462, 3), (230, 80, 80))
    for x in (40, 130, 760):
        piece(c, [Thick(x, 548, x, 528, 2.5), Circ(x, 524, 6)], (255, 150, 180), shadow=SMALL)

    # rooms (back walls with paper wallpaper)
    kitchen, living = (174, GF[0], HM - 4, GF[1]), (HM + 4, GF[0], 726, GF[1])
    bedroom, bath = (174, F1[0], HM - 4, F1[1]), (HM + 4, F1[0], 726, F1[1])
    flat(c, RRect(*kitchen, 0), (250, 232, 202))
    for y in range(470, 540, 14):
        for x in range(174, 446, 14):
            if (x // 14 + y // 14) % 2:
                flat(c, RRect(x, y, x + 14, y + 14, 0), (240, 218, 186))
    flat(c, RRect(*living, 0), (230, 214, 240))
    for x in range(462, 726, 22):
        flat(c, RRect(x, GF[0], x + 9, GF[1], 0), (240, 228, 248))
    flat(c, RRect(*bedroom, 0), (205, 225, 246))
    for y in range(262, 382, 24):
        for x in range(186 + (y // 24 % 2) * 12, 446, 24):
            flat(c, Circ(x, y, 3), (225, 238, 252))
    flat(c, RRect(*bath, 0), (210, 240, 234))
    for y in range(F1[0], F1[1], 18):
        flat(c, Thick(HM + 4, y, 726, y, 1), (190, 222, 214))
    for x in range(HM + 4, 726, 18):
        flat(c, Thick(x, F1[0], x, F1[1], 1), (190, 222, 214))
    attic = Poly([(176, ATTIC), (HM, 92), (724, ATTIC)])
    flat(c, attic, (248, 230, 200))
    for k in range(1, 6):
        y = ATTIC - k * 24
        hw = (y - 92) * (HM - 176) / (ATTIC - 92)
        flat(c, Thick(HM - hw, y, HM + hw, y, 1.2), (225, 202, 168))

    # structure: walls, floors, roof
    wood = (175, 122, 86)
    piece(c, [RRect(HL, ATTIC, 174, GF[1]), RRect(726, ATTIC, HR, GF[1]), RRect(HM - 4, F1[0], HM + 4, F1[1]),
              RRect(HM - 4, GF[0], HM + 4, GF[1])], (245, 236, 220), shadow=PROP)
    piece(c, [RRect(HL - 6, F1[1], HR + 6, GF[0], 2), RRect(HL - 6, ATTIC, HR + 6, F1[0], 2),
              RRect(HL - 14, GF[1], HR + 14, GF[1] + 16, 2)], wood, border=2, shadow=PROP)
    piece(c, RRect(590, 98, 628, 170, 2), (190, 90, 75), border=2, shadow=PROP)
    piece(c, [Thick(136, ATTIC + 6, HM, 76, 22), Thick(HM, 76, 764, ATTIC + 6, 22)], (205, 82, 72), border=2.5, shadow=PROP)
    for t in (0.25, 0.5, 0.75):
        for (x0, y0, x1, y1) in ((136, ATTIC + 6, HM, 76), (HM, 76, 764, ATTIC + 6)):
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            flat(c, Circ(x, y, 6), (225, 110, 95))

    # kitchen
    fridge = (240, 170, 190) if "fridge" in d else (150, 210, 232)
    piece(c, RRect(184, 418, 236, 540, 5), fridge, border=2, shadow=PROP)
    flat(c, [Thick(186, 460, 234, 460, 2), Thick(228, 430, 228, 452, 3), Thick(228, 470, 228, 500, 3)], lit(fridge, 0.8))
    piece(c, RRect(242, 470, 330, 540, 2), (205, 160, 115), border=2, shadow=PROP)
    piece(c, RRect(238, 464, 334, 472, 2), (235, 225, 210), shadow=SMALL)
    flat(c, [RRect(250, 482, 282, 532, 2), RRect(290, 482, 322, 532, 2)], (190, 145, 100))
    piece(c, RRect(336, 462, 406, 540, 3), (245, 245, 240), border=2, shadow=PROP)
    flat(c, RRect(344, 488, 398, 530, 3), (70, 70, 85))
    flat(c, [Circ(350, 472, 3), Circ(364, 472, 3), Circ(378, 472, 3), Circ(392, 472, 3)], (90, 90, 100))
    piece(c, [RRect(346, 436, 394, 462, 6), Thick(338, 444, 348, 444, 3), Thick(392, 444, 402, 444, 3)], (150, 150, 165),
          border=1.5, shadow=SMALL)
    for x in (260, 290, 320):
        piece(c, RRect(x - 8, 410, x + 8, 430, 3), [(240, 200, 120), (180, 220, 150), (240, 150, 140)][(x // 30) % 3], shadow=SMALL)
    flat(c, Thick(244, 432, 336, 432, 3), (160, 115, 80))

    # living room
    piece(c, RRect(468, 436, 562, 540, 3), (200, 110, 90), border=2, shadow=PROP)
    for y in range(444, 540, 12):
        flat(c, Thick(470, y, 560, y, 1), (175, 90, 75))
    flat(c, [RRect(486, 476, 544, 540, 22)], (55, 40, 45))
    piece(c, RRect(460, 428, 570, 438, 2), (225, 205, 180), shadow=SMALL)
    painting = ((250, 160, 90), (240, 110, 120)) if "painting" in d else ((150, 205, 235), (110, 180, 110))
    piece(c, RRect(588, 404, 652, 452, 2), (200, 160, 90), border=1.5, shadow=PROP)
    flat(c, RRect(594, 410, 646, 446, 1), painting[0])
    flat(c, Poly([(594, 446), (612, 426), (628, 438), (646, 420), (646, 446)]), painting[1])
    piece(c, [RRect(578, 484, 712, 536, 10), RRect(572, 470, 594, 536, 8), RRect(696, 470, 718, 536, 8)], (120, 160, 210),
          border=2, shadow=PROP)
    flat(c, [RRect(600, 472, 642, 492, 6), RRect(646, 472, 690, 492, 6)], (150, 190, 235))
    rug = (90, 150, 220) if "rug" in d else (230, 90, 90)
    piece(c, RRect(574, 534, 716, 541, 2), rug, shadow=SMALL)
    piece(c, [RRect(680, 404, 716, 470, 4), Circ(698, 418, 14)], (150, 100, 70), border=2, shadow=PROP)
    flat(c, Circ(698, 418, 11), (250, 245, 230))
    flat(c, [Thick(698, 418, 698, 410, 1.5), Thick(698, 418, 704, 420, 1.5)], INK)
    flat(c, RRect(686, 434, 710, 466, 3), (110, 70, 50))

    # bedroom
    piece(c, [RRect(186, 340, 330, 380, 4), RRect(186, 316, 198, 380, 3), RRect(318, 330, 330, 380, 3)], (175, 125, 90),
          border=2, shadow=PROP)
    piece(c, RRect(198, 334, 318, 356, 6), (250, 200, 120), shadow=SMALL)
    flat(c, [Thick(210, 345, 306, 345, 2)], (240, 180, 100))
    piece(c, RRect(200, 324, 236, 340, 6), (252, 250, 245), shadow=SMALL)
    piece(c, Circ(226, 326, 10), (250, 210, 180), shadow=SMALL)
    flat(c, Thick(220, 327, 226, 327, 1.4), INK)
    piece(c, RRect(360, 278, 432, 382, 3), (160, 115, 85), border=2, shadow=PROP)
    rnd = random.Random(12)
    for row, y in enumerate((282, 316, 350)):
        flat(c, Thick(362, y + 30, 430, y + 30, 3), (130, 90, 65))
        x = 366
        while x < 424:
            w = rnd.choice((6, 8, 10))
            flat(c, RRect(x, y + 6 + rnd.randint(0, 6), x + w, y + 30, 1),
                 [(230, 90, 90), (90, 150, 220), (250, 200, 80), (120, 190, 120)][rnd.randint(0, 3)])
            x += w + 2
    piece(c, RRect(196, 262, 254, 306, 3), (190, 225, 245), border=3, border_col=(250, 248, 240), shadow=PROP)
    flat(c, [Thick(225, 262, 225, 306, 2.5), Thick(196, 284, 254, 284, 2.5)], (250, 248, 240))

    # bathroom
    piece(c, [Ell(530, 300, 24, 30)], (210, 225, 240), border=4, border_col=(220, 190, 120), shadow=PROP)
    piece(c, [RRect(476, 330, 524, 344, 4), RRect(494, 344, 506, 382, 2)], (250, 250, 248), border=2, shadow=PROP)
    piece(c, [RRect(560, 340, 704, 376, 14), Circ(574, 378, 5), Circ(690, 378, 5)], (252, 250, 248), border=2, shadow=PROP)
    for x in range(568, 700, 13):
        piece(c, Circ(x, 338 + (x % 3) * 2, 9), (250, 252, 255), shadow=SMALL)
    piece(c, [Thick(712, 300, 712, 350, 3), RRect(704, 304, 722, 336, 3)], (240, 140, 150), shadow=SMALL)

    # attic
    piece(c, RRect(232, 196, 282, ATTIC, 2), (200, 160, 110), border=2, shadow=PROP)
    flat(c, Thick(232, 214, 282, 214, 2), (175, 135, 90))
    piece(c, RRect(288, 214, 322, ATTIC, 2), (185, 145, 100), border=2, shadow=PROP)
    piece(c, [RRect(600, 205, 670, ATTIC, 6)], (120, 90, 120), border=2, border_col=(230, 190, 90), shadow=PROP)
    piece(c, Circ(HM, 175, 20), (190, 225, 245), border=4, border_col=(250, 248, 240), shadow=PROP)
    flat(c, [Thick(HM - 20, 175, HM + 20, 175, 2.5), Thick(HM, 155, HM, 195, 2.5)], (250, 248, 240))


def l12_sun(c, m):
    piece(c, Poly(star_pts(80, 70, 46, 34, points=12)), (255, 190, 80), shadow=PROP)
    piece(c, Circ(80, 70, 28), (255, 222, 95), border=2.5, shadow=PROP)


def l12_lamp(c, m):
    flat(c, Thick(300, GF[0], 300, GF[0] + 24, 1.5), (90, 80, 90))
    piece(c, Poly([(286, GF[0] + 40), (314, GF[0] + 40), (306, GF[0] + 24), (294, GF[0] + 24)]), (250, 200, 90), border=1.5,
          shadow=PROP)
    soft_union(c, [Ell(300, GF[0] + 46, 16, 8)], (255, 240, 170), 0.6, spread=8)


def l12_fire(c, m):
    soft_union(c, [Ell(515, 520, 26, 18)], (255, 170, 70), 0.45, spread=10)
    piece(c, Poly([(498, 538), (532, 538), (528, 516), (522, 522), (515, 498), (508, 520), (502, 512)]), (255, 140, 50),
          shadow=None)
    flat(c, Poly([(505, 538), (525, 538), (521, 524), (515, 512), (509, 526)]), (255, 225, 110))
    flat(c, [Thick(496, 538, 534, 532, 4), Thick(498, 532, 532, 538, 4)], (120, 75, 55))


def l12_pendulum(c, m):
    flat(c, Thick(698, 432, 698, 456, 1.6), (230, 190, 90))
    piece(c, Circ(698, 459, 5), (240, 200, 90), shadow=SMALL)


def l12_mobile(c, m):
    x, y = 270, F1[0]
    flat(c, Thick(x, y, x, y + 18, 1.2), (110, 100, 110))
    flat(c, Thick(x - 22, y + 18, x + 22, y + 18, 1.6), (150, 110, 90))
    for dx, col in ((-22, (250, 200, 80)), (0, (250, 150, 180)), (22, (150, 200, 250))):
        flat(c, Thick(x + dx, y + 18, x + dx, y + 30, 1), (110, 100, 110))
        piece(c, Poly(star_pts(x + dx, y + 36, 7, 3)), col, shadow=SMALL)


def l12_duck(c, m):
    col = (250, 160, 190) if m else (255, 210, 60)
    piece(c, [Ell(630, 330, 13, 8), Circ(640, 320, 7)], col, border=1.5, shadow=SMALL)
    flat(c, Poly([(646, 319), (653, 321), (646, 324)]), (240, 130, 50))
    flat(c, Circ(642, 318, 1.3), INK)


def l12_spider(c, m):
    flat(c, Thick(520, 118, 520, 176, 0.9), (110, 100, 110))
    piece(c, [Circ(520, 180, 6), Circ(520, 172, 4)], (60, 50, 60), shadow=SMALL)
    for s in (-1, 1):
        for k in range(3):
            flat(c, Thick(520, 179 + k * 2, 520 + s * 10, 174 + k * 5, 1), (60, 50, 60))


def l12_bubble(x):
    def d(c, m):
        piece(c, Circ(x, 330, 4.5), (235, 245, 255), border=1, border_col=(200, 225, 245), shadow=SMALL)
    return d


def l12_zzz(x, y, s):
    def d(c, m):
        piece(c, Poly([(x - s, y - s), (x + s, y - s), (x - s * 0.4, y + s * 0.6), (x + s, y + s * 0.6), (x + s, y + s),
                       (x - s, y + s), (x + s * 0.4, y - s * 0.6), (x - s, y - s * 0.6)]), (90, 110, 170), shadow=SMALL)
    return d


L12_ELEMENTS = [
    E("sun", l12_sun, pivot=(80, 70), anim=dict(rotateSpeed=-10)),
    E("cloud1", paper_cloud(330, 40, 0.8), anim=drift_across(295, 365, 9)),
    E("cloud2", paper_cloud(800, 90, 0.65), anim=drift_across(770, 830, 6)),
] + smoke_puffs(609, 88) + [
    E("lamp", l12_lamp, pivot=(300, GF[0]), anim=dict(swingAngle=6, swingSpeed=0.3)),
] + smoke_puffs(370, 432, col=(250, 250, 252), r=6, prefix="steam") + [
    E("fire", l12_fire, show="A", pivot=(515, 538), anim=dict(stretch=(0.08, 0.25), scaleSpeed=4, twinkle=0.15, twinkleSpeed=3)),
    E("pendulum", l12_pendulum, pivot=(698, 432), anim=dict(swingAngle=20, swingSpeed=0.5), animB={}),
    E("mobile", l12_mobile, pivot=(270, F1[0]), anim=dict(spinSpeed=0.12, spinShade=0.2, swingAngle=4, swingSpeed=0.3)),
] + [
    E("zzz%d" % i, l12_zzz(240, 300, 4 + i), anim=dict(driftVelocity=(6, 14), driftLength=40, driftFade=True, driftGrow=0.5,
                                                        phase=i / 3))
    for i in range(3)
] + [
    E("bubble%d" % i, l12_bubble(x), anim=dict(driftVelocity=(3, 18), driftLength=60, driftFade=True, driftGrow=0.6,
                                                bobAmplitude=(4, 0), bobSpeed=0.6, phase=i / 4))
    for i, x in enumerate((585, 610, 665, 685))
] + [
    E("duck", l12_duck, pivot=(632, 336), variant=True, anim=dict(bobAmplitude=(10, 2), bobSpeed=0.18, swingAngle=8, swingSpeed=0.5)),
    E("spider", l12_spider, show="A", pivot=(520, 118), anim=dict(stretch=(0, 0.25), scaleSpeed=0.25, swingAngle=4, swingSpeed=0.3)),
]

L12_DIFFS = [
    ("pendulum", 698, 452, 22),
    ("fire", 515, 516, 0),
    ("spider", 520, 168, 0),
    ("painting", 620, 428, 0),
    ("fridge", 210, 478, 0),
    ("duck", 634, 326, 0),
    ("rug", 645, 537, 0),
]


# =================================================================== Level 13 (worm's-eye view)
VP = (450.0, 300.0)
TRUNK_ANGLES = [195, 240, 285, 330, 18, 62, 108, 150]


def polar(r, a):
    return (VP[0] + r * math.cos(math.radians(a)), VP[1] + r * math.sin(math.radians(a)))


def l13_background(c, d):
    """纸艺林冠 - sky seen through the canopy"""
    c.rect(0, 0, W, 660, (140, 192, 230))
    for r, col in ((420, (160, 205, 238)), (320, (182, 220, 244)), (220, (205, 233, 248)), (130, (226, 243, 252))):
        piece(c, Circ(*VP, r), col, shadow=(0, 0, 10, 0.12))


def l13_canopy(c, m):
    """Trunks converge on the vanishing point; leaf clusters frame the opening."""
    for i, a in enumerate(TRUNK_ANGLES):
        base_l, base_r = polar(680, a - 7), polar(680, a + 7)
        tip_l, tip_r = polar(165, a - 2.5), polar(165, a + 2.5)
        col = (128, 88, 64) if i % 2 else (112, 78, 58)
        piece(c, Poly([base_l, tip_l, tip_r, base_r]), col, border=2, border_col=(170, 125, 90), shadow=PROP)
        flat(c, Poly([polar(680, a - 7), polar(165, a - 2.5), polar(165, a - 1.2), polar(680, a - 3)]), lit(col, 1.25))
        for r in (260, 360, 460):
            p0, p1 = polar(r, a - 3), polar(r + 18, a + 2)
            flat(c, Thick(p0[0], p0[1], p1[0], p1[1], 1.5), lit(col, 0.75))
        b0, b1 = polar(300, a), polar(255, a + 16)
        piece(c, Thick(b0[0], b0[1], b1[0], b1[1], 6), col, shadow=PROP)
    rnd = random.Random(31)
    greens = [(62, 128, 74), (82, 152, 86), (104, 176, 98), (126, 194, 108)]
    for layer, (rmin, rmax, size) in enumerate(((240, 330, 72), (200, 270, 56), (165, 225, 44), (150, 200, 30))):
        shapes = []
        for k in range(26):
            a = k * 360 / 26 + rnd.uniform(-6, 6)
            r = rnd.uniform(rmin, rmax)
            shapes.append(Circ(*polar(r, a), size * rnd.uniform(0.75, 1.1)))
        piece(c, shapes, greens[layer], shadow=(1, 3, 9, 0.35))
    if not m:   # red berries in the lower-left canopy (missing in B)
        for dx, dy in ((0, 0), (10, 6), (-8, 8), (4, 14), (14, -6)):
            bx, by = polar(205, 120)
            piece(c, Circ(bx + dx, by + dy, 5.5), (220, 50, 60), shadow=SMALL)


def l13_sun(c, m):
    piece(c, Poly(star_pts(520, 236, 38, 28, points=12)), (255, 190, 80), shadow=PROP)
    piece(c, Circ(520, 236, 22), (255, 150, 80) if m else (255, 224, 100), border=2.5, shadow=PROP)


def l13_balloon(c, m):
    x, y, r = 380, 232, 30
    base, stripe = ((120, 190, 120), (250, 250, 240)) if m else ((230, 80, 80), (255, 220, 110))
    piece(c, Circ(x, y, r), base, border=2.5, shadow=PROP)
    for k in range(0, 12, 2):
        a0, a1 = math.radians(k * 30), math.radians(k * 30 + 30)
        flat(c, Poly([(x, y), (x + r * math.cos(a0), y + r * math.sin(a0)), (x + r * math.cos(a1), y + r * math.sin(a1))]), stripe)
    piece(c, RRect(x - 7, y - 7, x + 7, y + 7, 2), (175, 120, 75), border=1.5, shadow=SMALL)


def l13_kite(c, m):
    x, y = 470, 372
    col = (90, 140, 230) if m else (250, 170, 60)
    flat(c, [Thick(x, y + 18, 380, 640, 1.1)], (240, 240, 240))
    piece(c, Poly([(x, y - 20), (x + 15, y), (x, y + 20), (x - 15, y)]), col, border=1.5, shadow=PROP)
    flat(c, [Thick(x, y - 20, x, y + 20, 1.4), Thick(x - 15, y, x + 15, y, 1.4)], lit(col, 0.7))
    for k, (dx, dy) in enumerate(((-6, 32), (4, 44), (-4, 56))):
        piece(c, Poly([(x + dx - 4, y + dy), (x + dx + 4, y + dy - 3), (x + dx + 2, y + dy + 4)]),
              [(230, 80, 80), (250, 220, 90), (120, 200, 120)][k], shadow=SMALL)


def l13_bird(x, y, s):
    def d(c, m):
        piece(c, [Poly([(x, y), (x - s, y - s * 0.5), (x - s * 1.6, y - s * 0.2), (x - s * 0.4, y + s * 0.2)]),
                  Poly([(x, y), (x + s, y - s * 0.5), (x + s * 1.6, y - s * 0.2), (x + s * 0.4, y + s * 0.2)]),
                  Ell(x, y + 1, s * 0.3, s * 0.6)], (60, 60, 80), shadow=(3, 6, 4, 0.2))
    return d


def l13_owl(c, m):
    x, y = polar(255, 195)
    piece(c, Ell(x, y, 15, 19), (60, 38, 32), border=2, border_col=(160, 115, 80), shadow=None)
    if not m:
        for s in (-1, 1):
            piece(c, Circ(x + s * 5, y - 2, 4.5), (255, 210, 60), shadow=None)
            flat(c, Circ(x + s * 5, y - 2, 2), (20, 15, 20))


def l13_squirrel(c, m):
    x, y = polar(275, 330)
    piece(c, [Ell(x, y, 9, 14), Circ(x, y - 15, 7), Ell(x + 10, y + 10, 8, 16)], (200, 120, 60), border=1.5, shadow=SMALL)
    flat(c, [Circ(x - 3, y - 16, 1.4), Circ(x + 3, y - 16, 1.4)], INK)


def l13_nest(c, m):
    x, y = polar(232, 62)
    piece(c, Ell(x, y + 8, 30, 14), (160, 115, 75), border=1.5, shadow=PROP)
    chicks = (-14, 0, 14) if not m else (-8, 8)
    for dx in chicks:
        piece(c, Circ(x + dx, y - 4, 8), (250, 220, 90), shadow=SMALL)
        flat(c, Poly([(x + dx - 4, y - 8), (x + dx + 4, y - 8), (x + dx, y - 16)]), (240, 130, 50))
    for k in range(5):
        flat(c, Thick(x - 28 + k * 13, y + 4, x - 20 + k * 13, y + 16, 1.6), (125, 85, 55))


def l13_leaf(a, col):
    def d(c, m):
        x, y = polar(90, a)
        piece(c, [Poly([(x - 9, y), (x, y - 5), (x + 9, y), (x, y + 5)]), Thick(x - 9, y, x - 13, y, 1.4)], col, border=1.2,
              shadow=SMALL)
    return d


def outward(a, speed, length):
    ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
    return dict(driftVelocity=(ux * speed, -uy * speed), driftLength=length, driftFade=True, driftGrow=2.2)


L13_ELEMENTS = [
    E("sun", l13_sun, pivot=(520, 236), variant=True, anim=dict(rotateSpeed=-10)),
    E("cloud1", paper_cloud(380, 300, 0.9), anim=drift_across(340, 425, 8)),
    E("cloud2", paper_cloud(560, 340, 0.6), anim=drift_across(535, 590, 5)),
    E("plane", lambda c, m: (flat(c, Thick(200, 240, 330, 220, 2), (250, 250, 250, 0.7)),
                             piece(c, [Ell(338, 219, 10, 3), Thick(334, 212, 340, 226, 3)], (240, 240, 245), shadow=SMALL)),
      anim=drift_across(200, 350, 18)),
    E("balloon", l13_balloon, pivot=(380, 232), variant=True,
      anim=dict(bobAmplitude=(6, 4), bobSpeed=0.12, pulse=0.05, scaleSpeed=0.12)),
    E("kite", l13_kite, pivot=(470, 380), variant=True, anim=dict(swingAngle=8, swingSpeed=0.4, bobAmplitude=(4, 5), bobSpeed=0.3)),
] + [
    E("bird%d" % i, l13_bird(x, y, 9), pivot=(x, y),
      anim=dict(drift_across(x - 15, x + 15, 24), stretch=(0.25, 0), scaleSpeed=2.4 + 0.4 * i, bobAmplitude=(0, 6), bobSpeed=0.3))
    for i, (x, y) in enumerate(((420, 270), (440, 258), (445, 284)))
] + [
    # the canopy is an element so the sky things pass behind it; it sways gently around the vanishing point
    E("canopy", l13_canopy, pivot=VP, variant=True, anim=dict(swingAngle=0.8, swingSpeed=0.1)),
    E("owl", l13_owl, variant=True, anim=dict(twinkle=0.0)),
    E("squirrel", l13_squirrel, show="A", pivot=polar(275, 330),
      anim=dict(bobAmplitude=(math.cos(math.radians(330)) * -14, -math.sin(math.radians(330)) * -14), bobSpeed=0.3, swingAngle=6,
                swingSpeed=0.6)),
    E("nest", l13_nest, variant=True, pivot=polar(232, 62), anim=dict(stretch=(0, 0.06), scaleSpeed=1.5)),
] + [
    # leaves fall towards the camera: they drift outward from the centre and grow
    E("leaf%d" % i, l13_leaf(a, col), pivot=polar(90, a),
      anim=dict(outward(a, 26, 260), rotateSpeed=80 + 20 * i, spinSpeed=0.5, spinShade=0.3, phase=i / 5))
    for i, (a, col) in enumerate(((20, (230, 120, 60)), (95, (250, 190, 70)), (170, (120, 190, 110)), (245, (230, 90, 70)),
                                   (310, (250, 210, 90))))
]

L13_DIFFS = [
    ("sun", 520, 236, 36),
    ("balloon", 380, 232, 38),
    ("kite", 470, 380, 30),
    ("owl", int(polar(255, 195)[0]), int(polar(255, 195)[1]), 22),
    ("squirrel", int(polar(275, 330)[0]), int(polar(275, 330)[1]), 30),
    ("chicks", int(polar(232, 62)[0]), int(polar(232, 62)[1]), 30),
    ("berries", int(polar(205, 120)[0] + 4), int(polar(205, 120)[1] + 5), 24),
]


# =================================================================== Level 14 (first person, rainy window)
WIN = (170, 50, 730, 438)


def l14_background(c, d):
    """纸艺窗外 - the landscape outside (the room is an element in front)"""
    c.rect(0, 0, W, 660, (176, 194, 212))
    piece(c, Poly([(0, 230), (120, 170), (250, 205), (380, 150), (520, 200), (660, 140), (820, 190), (920, 170), (920, 660), (0, 660)]),
          (152, 168, 194), shadow=LAYER)
    piece(c, Poly([(x, 270 + 18 * math.sin(x * 0.012)) for x in range(-20, 940, 20)] + [(940, 660), (-20, 660)]),
          (120, 160, 140), shadow=LAYER)
    piece(c, Poly([(x, 330 + 14 * math.sin(x * 0.015 + 2)) for x in range(-20, 940, 20)] + [(940, 660), (-20, 660)]),
          (100, 145, 120), shadow=LAYER)
    piece(c, Poly([(380, 660), (470, 345), (500, 312), (560, 300), (640, 312), (760, 300), (940, 296), (940, 330),
                   (760, 336), (650, 344), (560, 336), (520, 350), (510, 660)]), (135, 175, 205), shadow=PROP)
    piece(c, Poly([(-20, 392), (940, 372), (940, 400), (-20, 420)]), (150, 150, 160), shadow=PROP)
    for x in range(0, 900, 60):
        flat(c, Thick(x, 404 - x * 0.02, x + 28, 403 - x * 0.02, 2), (240, 240, 235))
    houses = [(230, 265, (220, 110, 90)), (285, 272, (110, 140, 200)), (640, 262, (240, 190, 90)), (690, 270, (150, 110, 170))]
    for x, y, roof in houses:
        if x == 285 and "roof" in d:
            roof = (120, 180, 110)
        piece(c, RRect(x - 18, y - 22, x + 18, y + 4, 2), (245, 236, 220), border=1.5, shadow=SMALL)
        piece(c, Poly([(x - 23, y - 20), (x + 23, y - 20), (x, y - 40)]), roof, border=1.5, shadow=SMALL)
        flat(c, RRect(x - 5, y - 12, x + 5, y + 4, 1), (110, 80, 85))
    for x, y, r in ((150, 300, 18), (360, 310, 22), (590, 320, 16), (800, 300, 20)):
        piece(c, [Thick(x, y + r, x, y + r + 16, 4), Circ(x, y, r)], (80, 135, 95), shadow=SMALL)
    for x, y, k in ((260, 95, 1.0), (560, 70, 1.2), (780, 110, 0.9)):
        if x == 560 and "cloud" in d:
            continue
        piece(c, [Circ(x - 30 * k, y + 8 * k, 22 * k), Circ(x, y, 30 * k), Circ(x + 32 * k, y + 8 * k, 22 * k),
                  RRect(x - 50 * k, y + 4 * k, x + 54 * k, y + 28 * k, 10 * k)], (205, 212, 225), shadow=PROP)


def l14_rain_unit(c, m, dx, dy):
    rnd = random.Random(77)
    for _ in range(110):
        x, y = rnd.uniform(WIN[0] - 260, WIN[2] + 260), rnd.uniform(WIN[1], WIN[1] + 128)
        flat(c, Thick(x + dx, y + dy, x + dx + 6, y + dy + 16, 1.2), (235, 242, 252, 0.7))


def l14_drop(x, y):
    def d(c, m):
        piece(c, [Circ(x, y, 4.5), Poly([(x - 4, y - 1), (x + 4, y - 1), (x, y - 10)])], (215, 232, 248), border=1,
              border_col=(250, 252, 255), shadow=SMALL)
        flat(c, Thick(x, y - 14, x, y - 40, 1.6), (230, 240, 252, 0.45))
    return d


def l14_room(c, m):
    """Wall with the window hole, window frame, sill and things on it."""
    x0, y0, x1, y1 = WIN
    wall = (238, 218, 196)
    piece(c, [RRect(-10, -10, W + 10, y0), RRect(-10, y1, W + 10, H + 10), RRect(-10, -10, x0, H + 10), RRect(x1, -10, W + 10, H + 10)],
          wall, shadow=(0, 0, 14, 0.3))
    for x in range(10, 900, 40):
        for y in range(15, 600, 40):
            if not (x0 - 10 < x < x1 + 10 and y0 - 10 < y < y1 + 10):
                flat(c, Poly(star_pts(x, y, 5, 2, points=4, rot=0)), (226, 202, 178))
    frame = (250, 247, 240)
    piece(c, [RRect(x0 - 12, y0 - 12, x1 + 12, y0 + 4), RRect(x0 - 12, y1 - 4, x1 + 12, y1 + 12), RRect(x0 - 12, y0 - 12, x0 + 4, y1 + 12),
              RRect(x1 - 4, y0 - 12, x1 + 12, y1 + 12), RRect((x0 + x1) / 2 - 7, y0, (x0 + x1) / 2 + 7, y1),
              RRect(x0, (y0 + y1) / 2 - 7, x1, (y0 + y1) / 2 + 7)], frame, shadow=PROP)
    piece(c, Thick(70, 34, 830, 34, 6), (170, 120, 85), border=1.5, shadow=PROP)
    # sill
    piece(c, RRect(x0 - 40, y1 + 8, x1 + 40, y1 + 34, 4), (205, 165, 125), border=2, shadow=PROP)
    piece(c, RRect(x0 - 30, y1 + 34, x1 + 30, y1 + 44, 2), (180, 140, 105), shadow=PROP)
    # plant (pot colour differs), books, cup
    pot = (90, 150, 220) if on("pot", m) else (220, 110, 80)
    for a in (-60, -30, 0, 30, 60):
        tx, ty = 230 + 34 * math.sin(math.radians(a)), y1 - 26 - 30 * math.cos(math.radians(a))
        piece(c, [Thick(230, y1 - 14, tx, ty, 3), Ell(tx, ty, 9, 5)], (80, 160, 90), shadow=SMALL)
    piece(c, Poly([(212, y1 - 18), (248, y1 - 18), (242, y1 + 10), (218, y1 + 10)]), pot, border=2, shadow=PROP)
    for k, col in enumerate(((230, 90, 90), (90, 150, 220), (250, 200, 80))):
        piece(c, RRect(320 + k * 2, y1 - 6 - k * 10, 400 - k * 6, y1 + 8 - k * 10, 2), col, border=1.5, shadow=SMALL)
    piece(c, [RRect(636, y1 - 18, 662, y1 + 8, 5), Thick(662, y1 - 10, 670, y1 - 6, 4)], (250, 248, 240), border=1.5, shadow=PROP)
    # radiator under the sill (red in B)
    rad = (220, 90, 80) if on("radiator", m) else (244, 242, 236)
    piece(c, RRect(360, 506, 560, 584, 6), rad, border=2, shadow=PROP)
    for xx in range(376, 550, 20):
        flat(c, Thick(xx, 514, xx, 576, 3), lit(rad, 0.86))
    # cat sitting on the sill (tail is animated)
    cx, cy = 560, y1 + 8
    piece(c, [Ell(cx, cy - 26, 26, 28), Circ(cx + 8, cy - 62, 17), Poly([(cx - 4, cy - 74), (cx - 2, cy - 92), (cx + 8, cy - 78)]),
              Poly([(cx + 12, cy - 78), (cx + 22, cy - 92), (cx + 24, cy - 72)])], (90, 90, 105), border=2, shadow=PROP)
    flat(c, [Ell(cx + 2, cy - 18, 12, 14)], (230, 225, 220))
    flat(c, [Thick(cx + 1, cy - 64, cx + 7, cy - 62, 1.6), Thick(cx + 12, cy - 62, cx + 18, cy - 64, 1.6)], (230, 225, 220))


def l14_curtain(x0, x1, side, m_dots):
    def d(c, m):
        pts = []
        for k in range(9):
            t = k / 8
            pts.append((x0 + (x1 - x0) * t, 40 + 4 * (k % 2)))
        bottom = [(x1 + side * 8, 470), (x0 - side * 6, 470)]
        shape = Poly(pts + bottom)
        piece(c, shape, (230, 120, 110), border=2, shadow=PROP)
        dot = (255, 225, 120) if (m and m_dots) else (252, 240, 232)
        for yy in range(70, 460, 34):
            for xx in range(int(min(x0, x1)) + 10, int(max(x0, x1)) - 4, 22):
                flat(c, Circ(xx + (yy // 34 % 2) * 8, yy, 3.5), dot)
        for k in (1, 3, 5, 7):
            xx = x0 + (x1 - x0) * k / 8
            flat(c, Thick(xx, 48, xx + side * 6, 466, 2), (200, 95, 90))
        piece(c, Thick(min(x0, x1) - 4, 300, max(x0, x1) + 4, 296, 5), (250, 210, 90), shadow=SMALL)
    return d


def l14_tail(c, m):
    piece(c, [Thick(584, 440, 610, 430, 7), Thick(610, 430, 622, 402, 7)], (90, 90, 105), border=2, shadow=SMALL)


def l14_person(c, m):
    x, y = 330, 386
    col = (250, 200, 70) if m else (230, 80, 90)
    flat(c, Thick(x, y - 26, x, y - 54, 1.6), (90, 80, 90))
    piece(c, [RRect(x - 6, y - 26, x + 6, y, 3), Circ(x, y - 31, 5)], (90, 140, 210), border=1.5, shadow=SMALL)
    piece(c, Poly([(x - 22, y - 50), (x + 22, y - 50), (x, y - 64)]), col, border=1.5, shadow=SMALL)


def l14_boat(c, m):
    x, y = 590, 318
    piece(c, Poly([(x - 16, y), (x + 16, y), (x + 10, y + 7), (x - 10, y + 7)]), (200, 110, 80), border=1.5, shadow=SMALL)
    piece(c, Poly([(x, y - 2), (x, y - 26), (x + 14, y - 4)]), (250, 248, 240), border=1.2, shadow=SMALL)


def l14_car(c, m):
    piece(c, [RRect(100, 386, 140, 398, 4), RRect(108, 378, 130, 388, 4)], (90, 150, 220), border=1.5, shadow=SMALL)
    flat(c, [Circ(110, 399, 4), Circ(132, 399, 4)], (60, 60, 70))


L14_ELEMENTS = [
    E("car", l14_car, anim=drift_across(98, 142, 26)),
    E("person", l14_person, pivot=(330, 386), variant=True,
      anim=dict(bobAmplitude=(34, 0), bobSpeed=0.05, spinSpeed=0.05, spinSnap=0.85)),
    E("boat", l14_boat, show="A", pivot=(590, 322), anim=dict(bobAmplitude=(6, 2), bobSpeed=0.12, swingAngle=6, swingSpeed=0.3)),
    # rain streaks: the pattern repeats every (48, 128) px, so drifting by that step loops seamlessly
    E("rain", tiled(l14_rain_unit, (48, 128), range(-4, 5)), bbox=(WIN[0] - 470, WIN[1] - 525, WIN[2] + 470, WIN[1] + 665),
      anim=seamless_drift((48, 128), 150)),
] + [
    E("drop%d" % i, l14_drop(x, y), anim=dict(driftVelocity=(0, -16 - 5 * i), driftLength=120, driftFade=True, phase=i / 5))
    for i, (x, y) in enumerate(((240, 120), (380, 90), (520, 140), (640, 100), (300, 300), (600, 280)))
] + [
    E("room", l14_room, variant=True),
    E("tail", l14_tail, pivot=(584, 440), anim=dict(swingAngle=16, swingSpeed=0.45), animB={}),
] + smoke_puffs(649, 418, col=(250, 250, 252), r=6, show="A", prefix="steam") + [
    E("curtain", l14_curtain(110, 196, -1, True), pivot=(150, 36), variant=True, anim=dict(swingAngle=1.5, swingSpeed=0.15)),
    E("curtain_r", l14_curtain(704, 790, 1, False), pivot=(750, 36), anim=dict(swingAngle=1.5, swingSpeed=0.13, phase=0.5)),
]

L14_DIFFS = [
    ("tail", 606, 424, 28),
    ("steam", 650, 392, 26),
    ("umbrella", 330, 352, 32),
    ("roof", 285, 242, 26),
    ("pot", 230, 434, 24),
    ("curtain", 152, 250, 42),
    ("boat", 592, 306, 26),
    ("cloud", 560, 80, 0),
    ("radiator", 460, 545, 0),
]


# =================================================================== Level 15 (isometric winter village)
SNOW = (246, 249, 253)


def iso_pine(c, X, Y, s=1.0, col=(70, 130, 95)):
    cx, cy = P(X, Y)
    soft_union(c, [Ell(cx + 18 * s, cy + 4, 22 * s, 9 * s)], (60, 80, 110), 0.25, spread=6)
    piece(c, Thick(cx, cy, cx, cy - 12 * s, 6 * s), (130, 90, 65), shadow=ISO_SH)
    tiers = []
    for k in range(3):
        top = cy - 70 * s + k * 16 * s
        w = (16 + k * 7) * s
        tiers.append(Poly([(cx, top), (cx - w, top + 30 * s), (cx + w, top + 30 * s)]))
    piece(c, tiers, col, border=1.5, shadow=ISO_SH)
    for k in range(3):
        top = cy - 70 * s + k * 16 * s
        w = (16 + k * 7) * s
        flat(c, Poly([(cx, top), (cx - w * 0.55, top + 14 * s), (cx, top + 10 * s), (cx + w * 0.55, top + 14 * s)]), SNOW)


def iso_house(c, X, Y, dx, dy, dz, wall, door, chimney=True):
    _, left, _ = iso_box(c, X, Y, 0, dx, dy, dz, wall)
    flat(c, Poly([P(X + dx * 0.35, Y + dy, 0), P(X + dx * 0.55, Y + dy, 0), P(X + dx * 0.55, Y + dy, dz * 0.62),
                  P(X + dx * 0.35, Y + dy, dz * 0.62)]), door)
    for wx in (X + dx * 0.12, X + dx * 0.7):
        flat(c, Poly([P(wx, Y + dy, dz * 0.42), P(wx + dx * 0.16, Y + dy, dz * 0.42), P(wx + dx * 0.16, Y + dy, dz * 0.75),
                      P(wx, Y + dy, dz * 0.75)]), (255, 220, 120))
    if chimney:
        iso_box(c, X + dx * 0.7, Y + dy * 0.2, dz, 0.3, 0.3, 0.75, (170, 90, 80), border=1.5)
    iso_roof(c, X - 0.1, Y - 0.1, dz, dx + 0.2, dy + 0.2, 0.6, SNOW)
    m = Y + dy / 2
    flat(c, Poly([P(X - 0.1, Y + dy + 0.1, dz), P(X + dx + 0.1, Y + dy + 0.1, dz), P(X + dx + 0.1, Y + dy + 0.1, dz + 0.08),
                  P(X - 0.1, Y + dy + 0.1, dz + 0.08)]), lit(wall, 0.85))


H1 = (1.2, 1.5, 1.6, 1.2, 1.0)
H2 = (3.7, 0.7, 1.4, 1.2, 1.1)
H3 = (7.2, 1.0, 1.7, 1.3, 1.0)
POND = (6.4, 6.3)
SNOWMAN = (3.6, 5.4)


def l15_background(c, d):
    """纸艺雪村 - static part"""
    from fill_iso import draw_surround, iso_ground
    iso_ground(c, (240, 245, 252), (230, 238, 248))
    for q in (iso_quad(4.4, 10, 5.4, 26), iso_quad(-16, 3.2, 1.0, 4.0), iso_quad(9.0, 3.2, 26, 4.0)):
        flat(c, q, (226, 232, 242))
    draw_surround(c, L15_SURROUND, l15_decor, "back")
    # paths trodden in the snow
    for q in (iso_quad(4.4, 2.4, 5.4, 10), iso_quad(1.0, 3.2, 9.0, 4.0)):
        flat(c, q, (226, 232, 242))
    # frozen pond
    cx, cy = P(*POND)
    ex = 1.7 * 36 * math.sqrt(2)
    piece(c, Ell(cx, cy, ex, ex / 2), (190, 222, 242), border=3, border_col=(250, 252, 255), shadow=(1, 3, 5, 0.25))
    for k in range(3):
        flat(c, Thick(cx - 40 + k * 30, cy - 10 + k * 6, cx - 10 + k * 30, cy - 18 + k * 6, 2), (225, 242, 252))
    # houses
    iso_house(c, *H1, (225, 120, 100), (120, 80, 70))
    iso_house(c, *H2, (110, 150, 210), (230, 200, 80) if "door" in d else (120, 80, 70))
    iso_house(c, *H3, (120, 180, 140), (120, 80, 70), chimney=False)
    # trees (one missing in B)
    for X, Y, s in ((0.6, 0.5, 1.0), (2.9, 0.4, 0.9), (9.2, 0.6, 1.0), (0.5, 4.6, 1.1), (9.3, 3.8, 0.9), (1.6, 8.6, 1.0),
                    (8.8, 8.8, 1.1), (9.3, 5.9, 0.8)):
        if (X, Y) == (9.3, 5.9) and "pine" in d:
            continue
        iso_pine(c, X, Y, s)
    # bench by the pond (missing in B)
    if "bench" not in d:
        iso_box(c, 4.4, 7.4, 0.25, 1.0, 0.3, 0.08, (170, 120, 85), border=1.5)
        for bx in (4.5, 5.3):
            iso_box(c, bx, 7.45, 0, 0.1, 0.2, 0.25, (110, 90, 80), border=1)
    # snowman with a scarf (red in A, blue in B)
    sx, sy = P(*SNOWMAN)
    soft_union(c, [Ell(sx + 14, sy + 4, 22, 8)], (60, 80, 110), 0.25, spread=6)
    piece(c, [Circ(sx, sy - 16, 18), Circ(sx, sy - 44, 13)], (252, 253, 255), border=2, border_col=(210, 222, 240), shadow=ISO_SH)
    scarf = (80, 130, 230) if "scarf" in d else (230, 70, 70)
    piece(c, [RRect(sx - 13, sy - 34, sx + 13, sy - 28, 3), Thick(sx + 6, sy - 30, sx + 10, sy - 18, 5)], scarf, shadow=SMALL)
    piece(c, [RRect(sx - 9, sy - 70, sx + 9, sy - 56, 2), RRect(sx - 13, sy - 57, sx + 13, sy - 53, 2)], (50, 50, 60), shadow=SMALL)
    flat(c, Poly([(sx, sy - 46), (sx + 14, sy - 43), (sx, sy - 41)]), (245, 140, 50))
    flat(c, [Circ(sx - 4, sy - 49, 1.6), Circ(sx + 4, sy - 49, 1.6)], INK)
    # lamp posts
    for X, Y in ((4.2, 3.0), (5.8, 5.2), (2.4, 4.2)):
        lx, ly = P(X, Y)
        piece(c, Thick(lx, ly, lx, ly - 46, 3), (70, 70, 85), shadow=ISO_SH)
        soft_union(c, [Circ(lx, ly - 50, 12)], (255, 230, 150), 0.35, spread=8)
        piece(c, Circ(lx, ly - 50, 6), (255, 230, 140), border=1.5, shadow=None)
    from fill_iso import draw_surround
    draw_surround(c, L15_SURROUND, l15_decor, "front")


def l15_decor(c, X, Y, r):
    x, y = P(X, Y)
    if r < 0.55:
        iso_pine(c, X, Y, 0.7 + 0.4 * r)
    elif r < 0.7:
        piece(c, [Ell(x, y - 8, 18, 12)], (150, 150, 160), shadow=ISO_SH)
        flat(c, Ell(x - 2, y - 14, 14, 6), SNOW)
    elif r < 0.85:
        iso_box(c, X, Y, 0, 0.8, 0.7, 0.6, (190, 120, 90), border=1.5)
        iso_roof(c, X - 0.05, Y - 0.05, 0.6, 0.9, 0.8, 0.4, SNOW)
    else:
        for k in range(3):
            iso_box(c, X + k * 0.35, Y, 0, 0.08, 0.08, 0.4, (150, 110, 80), border=1)


def _l15_surround():
    from fill_iso import surround_points
    return surround_points(15, step=64)


L15_SURROUND = _l15_surround()


def l15_snow_unit(seed, n, rmin, rmax):
    def unit(c, m, dx, dy):
        rnd = random.Random(seed)
        for _ in range(n):
            x, y = rnd.uniform(0, W), rnd.uniform(0, 200)
            flat(c, Circ(x + dx, y + dy, rnd.uniform(rmin, rmax)), (255, 255, 255, 0.9))
    return unit


def l15_skater(c, m):
    cx, cy = P(*POND, 0.6)
    piece(c, [RRect(cx - 5, cy - 6, cx + 5, cy + 12, 3), Circ(cx, cy - 12, 5), Thick(cx - 3, cy + 12, cx - 6, cy + 22, 2.5),
              Thick(cx + 3, cy + 12, cx + 7, cy + 21, 2.5)], (230, 80, 90), border=1.5, shadow=SMALL)
    flat(c, Circ(cx, cy - 12, 4), (250, 210, 180))
    flat(c, Thick(cx - 6, cy - 3, cx + 9, cy - 1, 2.5), (250, 220, 90))


def l15_lights(c, m):
    X, Y, dx, dy, dz = H3
    cols = [(255, 90, 90), (255, 220, 80), (110, 200, 255), (130, 230, 120)]
    for k in range(9):
        t = k / 8
        x, y = P(X - 0.1 + (dx + 0.2) * t, Y + dy + 0.1, dz + 0.04)
        soft_union(c, [Circ(x, y + 2, 4)], cols[k % 4], 0.6, spread=4)
        piece(c, Circ(x, y + 2, 2.6), cols[k % 4], shadow=None)


def l15_sled(c, m):
    a, b = P(8.6, 9.3, 0.15), P(8.6, 9.3, 0.15)
    x, y = a
    piece(c, [Poly([(x - 16, y), (x + 14, y + 8), (x + 16, y + 4), (x - 12, y - 4)])], (200, 80, 70), border=1.5, shadow=SMALL)
    piece(c, [RRect(x - 4, y - 18, x + 6, y - 2, 3), Circ(x + 1, y - 22, 5)], (90, 140, 210), border=1.2, shadow=SMALL)
    flat(c, Circ(x + 1, y - 22, 4), (250, 210, 180))


_dx, _dy = P(1, 0)[0] - P(0, 0)[0], P(1, 0)[1] - P(0, 0)[1]
_ln = math.hypot(_dx, _dy)

L15_ELEMENTS = [
    E("cloud1", paper_cloud(160, 70, 0.9, (250, 252, 255)), anim=drift_across(120, 200, 7)),
    E("cloud2", paper_cloud(720, 50, 0.7, (250, 252, 255)), anim=drift_across(690, 750, 5)),
] + smoke_puffs(*P(H1[0] + H1[2] * 0.85, H1[1] + H1[3] * 0.35, H1[4] + 0.85), show="A", prefix="smoke") \
  + smoke_puffs(*P(H2[0] + H2[2] * 0.85, H2[1] + H2[3] * 0.35, H2[4] + 0.85), prefix="smoke2") + [
    # the skater circles the pond the other way round in B
    E("skater", l15_skater, pivot=P(*POND, 0.6),
      anim=dict(orbitRadius=(62, 28), orbitSpeed=0.1, orbitDepth=0.2, swingAngle=8, swingSpeed=0.4),
      animB=dict(orbitRadius=(62, 28), orbitSpeed=-0.1, orbitDepth=0.2, swingAngle=8, swingSpeed=0.4)),
    E("lights", l15_lights, show="A", anim=dict(twinkle=0.6, twinkleSpeed=1.2)),
    E("sled", l15_sled, pivot=P(8.6, 9.3, 0.15),
      anim=dict(driftVelocity=(-_dx / _ln * 26, _dy / _ln * 26), driftLength=_ln * 7, driftFade=True)),
    E("snow_far", tiled(l15_snow_unit(3, 70, 1.0, 2.0), (0, 200), range(-1, 4)), bbox=(0, -210, W, 810),
      anim=seamless_drift((0, 200), 18)),
    E("snow_near", tiled(l15_snow_unit(9, 28, 2.5, 4.0), (0, 200), range(-1, 4)), bbox=(0, -210, W, 810),
      anim=dict(seamless_drift((0, 200), 34), bobAmplitude=(8, 0), bobSpeed=0.2)),
]

_lx, _ly = P(H3[0] + H3[2] / 2, H3[1] + H3[3] + 0.1, H3[4])
L15_DIFFS = [
    ("skater", int(P(*POND)[0]), int(P(*POND, 0.6)[1]), 72),
    ("smoke", int(P(H1[0] + H1[2] * 0.85, H1[1] + H1[3] * 0.35, H1[4] + 0.85)[0] + 6),
     int(P(H1[0] + H1[2] * 0.85, H1[1] + H1[3] * 0.35, H1[4] + 0.85)[1] - 24), 28),
    ("lights", int(_lx), int(_ly + 2), 0),
    ("scarf", int(P(*SNOWMAN)[0] + 2), int(P(*SNOWMAN)[1] - 28), 0),
    ("door", int(P(H2[0] + H2[2] * 0.45, H2[1] + H2[3], H2[4] * 0.3)[0]), int(P(H2[0] + H2[2] * 0.45, H2[1] + H2[3], H2[4] * 0.3)[1]), 0),
    ("pine", int(P(9.3, 5.9)[0]), int(P(9.3, 5.9)[1] - 36), 0),
    ("bench", int(P(4.9, 7.55, 0.2)[0]), int(P(4.9, 7.55, 0.2)[1]), 0),
]


LEVELS = [
    ("Level12", "纸艺小屋", l12_background, L12_ELEMENTS, L12_DIFFS, 140, OPTS),
    ("Level13", "纸艺林冠", l13_background, L13_ELEMENTS, L13_DIFFS, 130, OPTS),
    ("Level14", "纸艺窗外", l14_background, L14_ELEMENTS, L14_DIFFS, 130, OPTS),
    ("Level15", "纸艺雪村", l15_background, L15_ELEMENTS, L15_DIFFS, 140, OPTS),
]
