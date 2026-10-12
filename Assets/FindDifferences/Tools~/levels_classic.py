# -*- coding: utf-8 -*-
"""Classic levels: 乡村小屋 / 海边沙滩 / 星空探险."""
import math
import random

from fdcore import *  # noqa: F401,F403
from fdcore import H, W, WHITE, BLACK, E, cloud, cloud_bbox, bird_bbox, butterfly


# ------------------------------------------------------------------- Level 1
def l1_background(c, d):
    """乡村小屋 - static part"""
    c.gradient(0, 400, (110, 190, 245), (205, 235, 255))
    c.ellipse(170, 430, 320, 130, (120, 195, 95))
    c.ellipse(760, 440, 360, 150, (100, 175, 80))
    # windmill tower (blades are animated)
    c.polygon([(776, 338), (804, 338), (797, 270), (783, 270)], (235, 225, 205))
    c.round_rect(785, 312, 795, 338, 4, (140, 95, 60))
    c.rect(0, 410, W, H, (110, 185, 75))
    c.polygon([(470, 430), (510, 430), (600, 600), (380, 600)], (215, 185, 135))
    if "chimney" not in d:
        c.rect(546, 158, 580, 215, (150, 70, 55))
        c.rect(541, 150, 585, 162, (120, 55, 45))
    c.rect(375, 245, 605, 432, (245, 210, 160))
    c.rect(375, 425, 605, 435, (200, 160, 110))
    c.polygon([(350, 252), (630, 252), (490, 140)], (205, 65, 55))
    c.rect(350, 248, 630, 258, (170, 45, 40))

    def window(x0, y0, glass):
        c.rect(x0 - 4, y0 - 4, x0 + 54, y0 + 46, WHITE)
        c.rect(x0, y0, x0 + 50, y0 + 42, glass)
        c.rect(x0 + 23, y0, x0 + 27, y0 + 42, WHITE)
        c.rect(x0, y0 + 19, x0 + 50, y0 + 23, WHITE)
    window(398, 290, (165, 215, 250))
    window(532, 290, (255, 225, 90) if "window" in d else (165, 215, 250))
    c.round_rect(463, 340, 517, 432, 8, (135, 85, 45))
    c.circle(505, 390, 4, (250, 210, 80))
    # tree
    c.rect(132, 270, 162, 455, (125, 82, 45))
    for x, y, r in ((147, 235, 72), (95, 275, 52), (200, 275, 52), (147, 290, 55)):
        c.circle(x, y, r, (60, 150, 65))
    for x, y in ((115, 225), (175, 235), (95, 290), (150, 300)):
        c.circle(x, y, 10, (225, 40, 40))
    if "apple" not in d:
        c.circle(198, 285, 10, (225, 40, 40))
    # fence
    for x in range(640, 900, 34):
        c.polygon([(x, 455), (x + 18, 455), (x + 18, 515), (x, 515)], (240, 235, 220))
        c.polygon([(x, 455), (x + 9, 443), (x + 18, 455)], (240, 235, 220))
    c.rect(630, 468, 900, 476, (225, 215, 195))
    c.rect(630, 495, 900, 503, (225, 215, 195))
    # flowers
    rnd = random.Random(7)
    for i in range(14):
        x, y = rnd.randint(20, 340), rnd.randint(480, 585)
        col = [(255, 90, 140), (255, 230, 60), (190, 120, 255)][i % 3]
        c.line(x, y, x, y + 16, 3, (60, 140, 60), caps=False)
        for k in range(5):
            a = math.radians(k * 72)
            c.circle(x + 6 * math.cos(a), y + 6 * math.sin(a), 5, col)
        c.circle(x, y, 4, (255, 245, 200))


def l1_sun_rays(c, m):
    for i in range(12):
        a = math.radians(i * 30)
        c.line(780 + 52 * math.cos(a), 90 + 52 * math.sin(a), 780 + 70 * math.cos(a), 90 + 70 * math.sin(a), 6, (255, 200, 60))


def l1_sun_disk(c, m):
    c.circle(780, 90, 45, (255, 140, 30) if m else (255, 214, 40))
    c.circle(780, 90, 36, (255, 160, 60) if m else (255, 228, 90))


def l1_blades(c, m):
    for k in range(4):
        a = math.radians(45 + k * 90)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        p0x, p0y = 790 + ux * 7, 272 + uy * 7
        p1x, p1y = 790 + ux * 42, 272 + uy * 42
        c.polygon([(p0x + nx * 2, p0y + ny * 2), (p1x + nx * 2, p1y + ny * 2),
                   (p1x + nx * 13, p1y + ny * 13), (p0x + nx * 9, p0y + ny * 9)], (250, 246, 236))
        c.line(790, 272, p1x, p1y, 3, (150, 105, 70))
    c.circle(790, 272, 6, (120, 80, 50))


def l1_duck(c, m):
    c.ellipse(720, 560, 30, 20, (255, 225, 70))
    c.ellipse(712, 556, 14, 8, (245, 205, 50))
    c.circle(745, 538, 13, (255, 225, 70))
    c.polygon([(755, 536), (772, 540), (755, 545)], (255, 140, 30))
    c.circle(748, 534, 2.5, BLACK)


def l1_smoke(c, m):
    c.circle(563, 140, 11, (235, 235, 240))


L1_ELEMENTS = [
    E("cloud_far", lambda c, m: cloud(c, 300, 40, 0.6), cloud_bbox(300, 40, 0.6),
      anim=dict(driftVelocity=(14, 0), driftLength=1150, driftStart=-400, phase=400 / 1150)),
    E("cloud_drift", lambda c, m: cloud(c, 520, 60, 0.9), cloud_bbox(520, 60, 0.9),
      anim=dict(driftVelocity=(22, 0), driftLength=1150, driftStart=-650, phase=650 / 1150)),
    E("cloud", lambda c, m: cloud(c, 150, 85, 1.1), cloud_bbox(150, 85, 1.1), show="A",
      anim=dict(bobAmplitude=(8, 3), bobSpeed=0.15)),
    E("sun_rays", l1_sun_rays, (705, 15, 855, 165), anim=dict(rotateSpeed=-15)),
    E("sun", l1_sun_disk, (733, 43, 827, 137), variant=True, anim=dict(pulse=0.05, scaleSpeed=0.4)),
    E("bird1", lambda c, m: c.bird(330, 120, 14, BLACK), bird_bbox(330, 120, 14), pivot=(330, 117),
      anim=dict(stretch=(0, 0.6), scaleSpeed=2.2, bobAmplitude=(25, 6), bobSpeed=0.08)),
    E("bird2", lambda c, m: c.bird(365, 100, 11, BLACK), bird_bbox(365, 100, 11), pivot=(365, 98),
      anim=dict(stretch=(0, 0.6), scaleSpeed=2.6, bobAmplitude=(20, 5), bobSpeed=0.1, phase=0.3)),
] + [
    E("smoke%d" % i, l1_smoke, (550, 127, 576, 153), show="A",
      anim=dict(driftVelocity=(5, 20), driftLength=75, driftFade=True, driftGrow=1.0, phase=i / 3))
    for i in range(3)
] + [
    E("windmill", l1_blades, (745, 227, 835, 317), pivot=(790, 272),
      anim=dict(rotateSpeed=-70), animB=dict(rotateSpeed=70)),
    E("butterfly1", lambda c, m: butterfly(c, 260, 470, (255, 120, 180)), (245, 458, 275, 481),
      anim=dict(stretch=(0.6, 0), scaleSpeed=3, bobAmplitude=(35, 18), bobSpeed=0.12)),
    E("butterfly2", lambda c, m: butterfly(c, 60, 525, (255, 170, 40)), (45, 513, 75, 536),
      anim=dict(stretch=(0.6, 0), scaleSpeed=3.4, bobAmplitude=(25, 14), bobSpeed=0.15, phase=0.5)),
    E("duck", l1_duck, (686, 520, 776, 582), pivot=(720, 580),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.7, swingAngle=6, swingSpeed=0.5)),
]

L1_DIFFS = [
    ("sun", 780, 90, 70),
    ("cloud", 185, 82, 80),
    ("chimney", 563, 175, 45),
    ("window", 557, 311, 40),
    ("apple", 198, 285, 26),
    ("windmill", 790, 272, 50),
]


# ------------------------------------------------------------------- Level 2
def l2_background(c, d):
    """海边沙滩 - static part"""
    c.gradient(0, 260, (120, 205, 255), (215, 240, 255))
    c.gradient(255, 420, (40, 150, 215), (90, 200, 230))
    c.rect(0, 410, W, H, (242, 220, 160))
    for x in range(-40, 950, 120):
        c.ellipse(x, 410, 80, 18, (242, 220, 160))
    # umbrella and palm tree are elements so they sit above the animated waves
    # towel
    c.polygon([(120, 520), (300, 520), (330, 575), (95, 575)], (255, 200, 60))
    c.polygon([(140, 535), (310, 535), (316, 547), (130, 547)], (255, 120, 90))
    # ball shadow
    c.ellipse(390, 552, 24, 5, (220, 195, 135))
    # sand castle (flag cloth is animated)
    c.rect(480, 470, 600, 540, (215, 180, 110))
    c.rect(505, 430, 575, 472, (215, 180, 110))
    for x in range(480, 600, 24):
        c.rect(x, 460, x + 14, 472, (215, 180, 110))
    for x in range(505, 575, 20):
        c.rect(x, 420, x + 12, 432, (215, 180, 110))
    c.round_rect(528, 500, 552, 540, 10, (160, 120, 70))
    c.rect(539, 375, 542, 422, (110, 70, 40))
    c.star(80, 470, 24, 10, (255, 150, 60), rot=-80)
    c.circle(80, 470, 4, (255, 200, 120))
    c.ellipse(440, 580, 12, 8, (255, 210, 210))
    c.ellipse(620, 590, 10, 7, (250, 235, 220))


def l2_sun(c, m):
    c.circle(110, 85, 48, (255, 225, 80))
    c.circle(110, 85, 38, (255, 236, 130))


def l2_waves(c, m):
    for i in range(5):
        y = 290 + i * 18
        for x in range(-130 + 30 + (i % 2) * 40, 1100, 130):
            c.ellipse(x, y, 26, 3, (170, 230, 250))


def l2_boat(c, m):
    c.polygon([(560, 300), (700, 300), (680, 330), (580, 330)], (160, 90, 50))
    c.rect(560, 306, 700, 311, (240, 240, 240))
    c.rect(626, 180, 632, 302, (110, 70, 40))
    c.polygon([(634, 190), (634, 292), (700, 292)], (250, 110, 110) if m else WHITE)
    c.polygon([(622, 205), (622, 292), (575, 292)], (255, 240, 200))


def l2_umbrella(c, m):
    c.rect(197, 330, 203, 520, (230, 230, 230))
    c.ellipse(200, 345, 110, 60, (60, 120, 230) if m else (230, 60, 60), ymax=345)
    for k in range(-2, 3):
        c.polygon([(200, 285), (200 + k * 44 - 11, 345), (200 + k * 44 + 11, 345)], WHITE)
    c.ellipse(200, 345, 110, 6, (200, 200, 200), ymin=345)


def l2_trunk(c, m):
    for i in range(14):
        t = i / 13
        c.circle(780 + 40 * t * t, 560 - 300 * t, 18 - 5 * t, (150, 100, 55) if i % 2 == 0 else (135, 88, 48))


def l2_crown(c, m):
    top = (820, 255)
    for a, ln in ((200, 120), (235, 110), (290, 100), (330, 115), (10, 110), (160, 100)):
        r = math.radians(a)
        ex, ey = top[0] + ln * math.cos(r), top[1] + ln * math.sin(r) * 0.7
        mx, my = (top[0] + ex) / 2, (top[1] + ey) / 2 - 18
        c.polygon([top, (mx, my - 10), (ex, ey), (mx, my + 12)], (50, 160, 70))
    nuts = [(808, 272), (832, 276)] + ([] if m else [(820, 290)])
    for x, y in nuts:
        c.circle(x, y, 11, (110, 70, 35))


def l2_ball(c, m):
    c.circle(390, 520, 30, WHITE)
    c.ellipse(390, 520, 30, 12, (70, 150, 240))
    c.ellipse(390, 520, 9, 30, (240, 80, 80))


def l2_crab(c, m):
    cx, cy = 690, 545
    for s in (-1, 1):
        for k in range(3):
            c.line(cx + s * 18, cy + 4 + k * 6, cx + s * 36, cy + 14 + k * 8, 4, (200, 50, 40))
        c.line(cx + s * 20, cy - 6, cx + s * 34, cy - 22, 5, (200, 50, 40))
        c.circle(cx + s * 36, cy - 26, 9, (225, 60, 50))
        c.line(cx + s * 8, cy - 14, cx + s * 10, cy - 26, 3, (200, 50, 40))
        c.circle(cx + s * 10, cy - 28, 5, WHITE)
        c.circle(cx + s * 10, cy - 28, 2.5, BLACK)
    c.ellipse(cx, cy, 26, 17, (230, 70, 55))


GULL = (70, 70, 80)
L2_ELEMENTS = [
    E("sun", l2_sun, (60, 35, 160, 135), anim=dict(pulse=0.05, scaleSpeed=0.35)),
    E("waves", l2_waves, (-130, 284, 1030, 368),
      anim=dict(driftVelocity=(-14, 0), driftLength=130)),
    E("gull1", lambda c, m: c.bird(320, 90, 18, GULL), bird_bbox(320, 90, 18), pivot=(320, 88),
      anim=dict(stretch=(0, 0.6), scaleSpeed=2.0, bobAmplitude=(15, 8), bobSpeed=0.1)),
    E("gull", lambda c, m: c.bird(380, 130, 14, GULL), bird_bbox(380, 130, 14), pivot=(380, 128), show="A",
      anim=dict(stretch=(0, 0.6), scaleSpeed=2.4, bobAmplitude=(12, 6), bobSpeed=0.13, phase=0.4)),
    E("gull3", lambda c, m: c.bird(440, 70, 12, GULL), bird_bbox(440, 70, 12), pivot=(440, 69),
      anim=dict(stretch=(0, 0.6), scaleSpeed=2.8, bobAmplitude=(18, 6), bobSpeed=0.09, phase=0.7)),
    E("boat", l2_boat, (555, 175, 705, 335), pivot=(630, 330), variant=True,
      anim=dict(swingAngle=3, swingSpeed=0.3, bobAmplitude=(0, 4), bobSpeed=0.3)),
    E("umbrella", l2_umbrella, (88, 283, 312, 522), variant=True),
    E("trunk", l2_trunk, (760, 245, 840, 580)),
    E("palm", l2_crown, (690, 160, 950, 305), pivot=(820, 258), variant=True,
      anim=dict(swingAngle=3, swingSpeed=0.25)),
    E("ball", l2_ball, (358, 488, 422, 552),
      anim=dict(bobAmplitude=(0, 45), bobSpeed=0.5, bounce=True, rotateSpeed=-120), animB={}),
    E("flag", lambda c, m: c.polygon([(542, 377), (572, 388), (542, 399)], (240, 60, 60)), (541, 375, 574, 401),
      pivot=(542, 388), show="A", anim=dict(stretch=(0.25, 0), scaleSpeed=1.6, swingAngle=4, swingSpeed=1.2)),
    E("crab", l2_crab, (646, 508, 734, 580), pivot=(690, 560), show="A",
      anim=dict(bobAmplitude=(16, 0), bobSpeed=0.25, swingAngle=4, swingSpeed=1.0)),
]

L2_DIFFS = [
    ("sail", 667, 255, 50),
    ("gull", 380, 128, 34),
    ("coconut", 820, 287, 26),
    ("umbrella", 200, 318, 65),
    ("flag", 557, 388, 30),
    ("crab", 690, 538, 52),
    ("ball", 390, 500, 55),
]


# ------------------------------------------------------------------- Level 3
TWINKLES = [(40, 40), (260, 30), (380, 60), (560, 40), (600, 205), (850, 40), (880, 200),
            (40, 250), (330, 300), (560, 330), (840, 420), (30, 420), (620, 260), (250, 190)]


def l3_background(c, d):
    """星空探险 - static part"""
    c.gradient(0, H, (12, 16, 52), (55, 35, 100))
    rnd = random.Random(42)
    for _ in range(110):
        x, y = rnd.randint(0, W), rnd.randint(0, 470)
        c.circle(x, y, rnd.choice((1.2, 1.5, 2, 2.5)), (255, 255, rnd.randint(200, 255)))
    c.circle(120, 110, 60, (240, 235, 200))
    c.circle(100, 90, 12, (215, 210, 175))
    c.circle(145, 130, 9, (215, 210, 175))
    if "crater" not in d:
        c.circle(128, 78, 7, (215, 210, 175))
    c.ellipse(450, 640, 650, 170, (120, 115, 135))
    c.ellipse(200, 560, 50, 12, (95, 90, 110))
    c.ellipse(650, 540, 70, 15, (95, 90, 110))
    c.ellipse(820, 585, 40, 10, (95, 90, 110))
    c.rect(700, 395, 704, 500, (220, 220, 230))


def l3_comet(c, m):
    c.polygon([(300, 210), (390, 160), (308, 225)], (140, 200, 255))
    c.polygon([(305, 215), (380, 175), (300, 205)], (200, 230, 255))
    c.circle(300, 214, 10, (230, 245, 255))


def l3_planet(c, m):
    pc = (180, 110, 230) if m else (240, 150, 70)
    c.ellipse_ring(720, 130, 110, 30, 9, (230, 210, 160), ymax=130)
    c.circle(720, 130, 62, pc)
    c.ellipse(700, 110, 30, 8, tuple(min(255, v + 30) for v in pc))
    c.ellipse(735, 150, 38, 7, tuple(max(0, v - 30) for v in pc))
    c.ellipse_ring(720, 130, 110, 30, 9, (230, 210, 160), ymin=130)


def l3_ufo(c, m):
    c.ellipse(220, 300, 34, 30, (150, 230, 240), ymax=300)
    c.ellipse(210, 288, 10, 6, (210, 250, 255))
    c.ellipse(220, 312, 80, 20, (170, 170, 190))
    c.ellipse(220, 306, 80, 8, (200, 200, 215))


def l3_ufo_lights(c, m):
    for k in range(-2, 3):
        c.circle(220 + k * 30, 318, 5.5, (90, 240, 120) if m else (255, 220, 60))


def l3_rocket(c, m):
    fin = (60, 200, 120) if m else (230, 60, 60)
    c.polygon([(430, 400), (395, 455), (395, 470), (432, 445)], fin)
    c.polygon([(490, 400), (525, 455), (525, 470), (488, 445)], fin)
    c.round_rect(430, 270, 490, 460, 22, (235, 235, 245))
    c.polygon([(430, 290), (490, 290), (460, 215)], (230, 60, 60))
    c.rect(452, 420, 468, 470, (200, 200, 215))
    c.circle(460, 330, 18, (90, 90, 110))
    c.circle(460, 330, 13, (240, 90, 90) if m else (110, 200, 255))


def l3_flame(c, m):
    c.polygon([(440, 462), (480, 462), (460, 515)], (255, 170, 40))
    c.polygon([(448, 462), (472, 462), (460, 495)], (255, 240, 120))


ROCKET_BOB = dict(bobAmplitude=(0, 6), bobSpeed=0.5)
UFO_MOVE = dict(bobAmplitude=(0, 8), bobSpeed=0.35, swingAngle=5, swingSpeed=0.25)

L3_ELEMENTS = [
    E("twinkle%d" % i, (lambda x, y: lambda c, m: c.star(x, y, 8, 2, (255, 250, 210), points=4))(x, y),
      (x - 9, y - 9, x + 9, y + 9),
      anim=dict(twinkle=0.9, twinkleSpeed=0.4 + (i * 37 % 7) / 10, pulse=0.25,
                scaleSpeed=0.4 + (i * 37 % 7) / 10, phase=(i * 0.137) % 1))
    for i, (x, y) in enumerate(TWINKLES)
] + [
    E("bigstar", lambda c, m: c.star(470, 70, 20, 8, (255, 230, 90)), (448, 48, 492, 92), pivot=(470, 71), show="A",
      anim=dict(rotateSpeed=25, pulse=0.12, scaleSpeed=0.6)),
    E("star2", lambda c, m: c.star(860, 300, 14, 6, (255, 230, 90)), (844, 284, 876, 316), pivot=(860, 301),
      anim=dict(rotateSpeed=-25)),
    E("comet", l3_comet, (286, 155, 395, 228), pivot=(330, 200), show="A",
      anim=dict(bobAmplitude=(8, 4), bobSpeed=0.3)),
    E("planet", l3_planet, (606, 64, 834, 196), pivot=(720, 130), variant=True,
      anim=dict(bobAmplitude=(0, 6), bobSpeed=0.15, swingAngle=3, swingSpeed=0.1)),
    E("ufo", l3_ufo, (136, 266, 304, 340), pivot=(220, 310), anim=dict(UFO_MOVE)),
    E("ufo_lights", l3_ufo_lights, (136, 266, 304, 340), pivot=(220, 310), variant=True,
      anim=dict(UFO_MOVE, twinkle=0.5, twinkleSpeed=1.5)),
    E("flame", l3_flame, (438, 458, 482, 517), pivot=(460, 462),
      anim=dict(ROCKET_BOB, stretch=(0.12, 0.3), scaleSpeed=5)),
    E("rocket", l3_rocket, (390, 212, 530, 475), pivot=(460, 345), variant=True, anim=dict(ROCKET_BOB)),
    E("moonflag", lambda c, m: (c.rect(704, 397, 760, 432, (70, 140, 240)), c.star(732, 414, 10, 4, WHITE)),
      (703, 395, 762, 434), pivot=(704, 414), anim=dict(stretch=(0.2, 0), scaleSpeed=1.4, swingAngle=3, swingSpeed=1)),
]

L3_DIFFS = [
    ("bigstar", 470, 70, 32),
    ("crater", 128, 78, 22),
    ("comet", 345, 190, 55),
    ("planet", 720, 130, 70),
    ("fin", 460, 440, 75),
    ("porthole", 460, 330, 26),
    ("ufo", 220, 318, 60),
]


LEVELS = [
    ("Level01", "乡村小屋", l1_background, L1_ELEMENTS, L1_DIFFS, 100),
    ("Level02", "海边沙滩", l2_background, L2_ELEMENTS, L2_DIFFS, 110),
    ("Level03", "星空探险", l3_background, L3_ELEMENTS, L3_DIFFS, 120),
]
