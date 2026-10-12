# -*- coding: utf-8 -*-
"""
Fairy-tale fantasy levels with a lit, volumetric look:
  Level04 童话城堡 (fairy-tale castle, dreamy day)
  Level05 魔法森林 (enchanted forest, twilight)

Depth cues used here
  * per-pixel lighting (sphere / cylinder / cone shaders, light from the upper left)
  * soft contact shadows and glows (alpha blended)
  * aerial perspective (haze over distant layers) and parallax cloud layers
  * animation: 3D spin (gems), orbit with depth scaling (fairy, wisp),
    floating objects whose ground shadow shrinks and fades in sync
"""
import math
import random

from fdcore import (E, H, W, WHITE, cone, cylinder, drop_shadow, glow, glow_disc, linear, lit,
                    shaded_sphere, sparkle, sphere)


# ------------------------------------------------------------------- helpers
def drift_across(x_left, x_right, speed, start_offset=0.0):
    """Looping horizontal drift for an element spanning [x_left, x_right] (scene px).
    It travels from just off the left edge to just off the right edge, starting at its rest position."""
    s_min = -(x_right + 10)
    s_max = W + 10 - x_left
    length = s_max - s_min
    return dict(driftVelocity=(speed, 0), driftLength=length, driftStart=s_min,
                phase=((start_offset - s_min) / length) % 1.0)


def cloud3d(c, x, y, k, tint=(255, 250, 255), shadow=(205, 195, 235), alpha=1.0):
    """Puffy cloud: each puff is a softly lit sphere over a flat tinted base."""
    c.ellipse(x + 33 * k, y + 20 * k, 72 * k, 13 * k, shadow + (0.7 * alpha,))
    puffs = ((-22, 8, 20), (88, 8, 22), (0, 0, 30), (66, 0, 30), (32, -14, 36), (34, 10, 30))
    for dx, dy, r in puffs:
        px, py, rr = x + dx * k, y + dy * k, r * k
        c.ellipse(px, py, rr, rr, sphere(px, py, rr, tint, amb=0.78, kd=0.32, spec=0.0,
                                         rim=shadow, rim_k=0.0, alpha=alpha))


def cloud_extent(x, k):
    return x - 45 * k, x + 112 * k


def arch_window(c, x, y, w, h, col):
    c.rect(x - w / 2, y - h / 2 + w / 2, x + w / 2, y + h / 2, col)
    c.ellipse(x, y - h / 2 + w / 2, w / 2, w / 2, col, ymax=y - h / 2 + w / 2 + 0.5)


def tower(c, x, r, top, bottom, wall, roof, apex_y, roof_bw, pole=True):
    body = cylinder(x, r, wall, top=top, bottom=bottom, ao=0.22, spec=0.12, shin=12)
    c.rect(x - r, top, x + r, bottom, body)
    c.ellipse(x, bottom, r, r * 0.22, body, ymin=bottom)
    base_y = top + 2
    c.ellipse(x, base_y, roof_bw, roof_bw * 0.22, cylinder(x, roof_bw, lit(roof, 0.7), spec=0.05), ymin=base_y)
    c.polygon([(x, apex_y), (x - roof_bw, base_y), (x + roof_bw, base_y)],
              cone(x, apex_y, base_y, roof_bw, roof, spec=0.3, shin=20))
    if pole:
        c.rect(x - 1.2, apex_y - 24, x + 1.2, apex_y + 2, (120, 95, 80))
        shaded_sphere(c, x, apex_y - 25, 2.6, (255, 215, 90), spec=0.6)


def pine(c, x, base, h, col):
    for k in range(3):
        top = base - h + k * h * 0.22
        w = h * (0.22 + k * 0.1)
        c.polygon([(x, top), (x - w, top + h * 0.45), (x + w, top + h * 0.45)], col)
    c.rect(x - 3, base - h * 0.12, x + 3, base, lit(col, 0.8))


def petal_draw(x, y, col):
    def d(c, m):
        c.ellipse(x, y, 7, 3.5, sphere(x, y, 7, col, ry=3.5, amb=0.6, kd=0.5, spec=0.2))
    return d


# =================================================================== Level 04
CASTLE_PINK = (235, 95, 160)
CASTLE_BLUE = (95, 115, 225)
CASTLE_PURPLE = (150, 90, 220)
GEM_A, GEM_B = (90, 210, 255), (255, 110, 200)
SPOTS = [(88, 410, 9, 7), (118, 392, 11, 8), (150, 412, 9, 7), (102, 427, 6, 4), (136, 428, 6, 4)]


def l4_background(c, d):
    """童话城堡 - static part"""
    c.gradient(0, 380, (110, 130, 230), (255, 200, 225))
    glow_disc(c, 160, 70, 220, (255, 240, 210), 0.55, power=1.6)
    # rainbow
    bands = [(255, 90, 90), (255, 160, 70), (255, 230, 90), (110, 220, 120), (90, 170, 255), (120, 110, 240), (190, 110, 230)]
    for i, col in enumerate(bands):
        rx = 380 - i * 9
        c.ellipse_ring(470, 390, rx, rx * 0.72, 9.5, col + (0.42,), ymax=340)
    # mountains: lit left face, shaded right face, snow caps
    def mountain(bl, peak, br, litc, darkc):
        mid = (peak[0] + 12, bl[1])
        c.polygon([bl, peak, mid], litc)
        c.polygon([mid, peak, br], darkc)
        px, py = peak
        c.polygon([(px, py), (px - 26, py + 30), (px - 12, py + 24), (px, py + 34), (px + 4, py + 30)], (250, 250, 255))
        c.polygon([(px, py), (px + 4, py + 30), (px + 14, py + 26), (px + 26, py + 34)], (205, 210, 245))
    mountain((-60, 345), (130, 215), (330, 345), (175, 165, 232), (125, 115, 195))
    mountain((500, 345), (700, 200), (930, 345), (175, 165, 232), (125, 115, 195))
    mountain((190, 345), (330, 245), (480, 345), (155, 148, 218), (108, 102, 178))
    mountain((400, 345), (565, 255), (720, 345), (155, 148, 218), (108, 102, 178))
    # aerial haze over the distance
    c.rect(0, 190, W, 345, lambda px, py: (255, 215, 235, 0.32 * (py - 190) / 155))
    # far hills and meadow
    shaded_sphere(c, 150, 400, 270, (135, 205, 150), ry=90, amb=0.62, kd=0.45, spec=0.04)
    shaded_sphere(c, 770, 405, 290, (125, 198, 145), ry=95, amb=0.62, kd=0.45, spec=0.04)
    c.rect(0, 430, W, H, linear(0, 430, 0, H, (120, 205, 110), (75, 160, 85)))
    shaded_sphere(c, 450, 470, 330, (115, 205, 110), ry=110, amb=0.58, kd=0.5, spec=0.05)

    # -- trees behind the castle sides
    def tree(x, y, s):
        c.rect(x - 7 * s, y, x + 7 * s, y + 70 * s, cylinder(x, 7 * s, (130, 85, 55), spec=0.05))
        for dx, dy, r in ((-27, 18, 26), (27, 18, 26), (0, -6, 38)):
            shaded_sphere(c, x + dx * s, y + dy * s, r * s, (80, 165, 95), amb=0.5, kd=0.6, spec=0.08)
    drop_shadow(c, 255, 445, 60, 10, 0.3)
    tree(255, 375, 0.9)
    drop_shadow(c, 660, 447, 75, 11, 0.3)
    tree(660, 362, 1.25)

    # -- castle
    drop_shadow(c, 450, 408, 240, 22, 0.4)
    tower(c, 380, 20, 235, 330, (225, 215, 240), CASTLE_PURPLE, 160, 28, pole=False)
    tower(c, 520, 20, 235, 330, (225, 215, 240), CASTLE_PURPLE, 160, 28, pole=False)
    for x in (380, 520):
        arch_window(c, x, 262, 8, 14, (60, 50, 100))
    tower(c, 450, 42, 205, 305, (240, 232, 250), CASTLE_PINK, 100, 54)
    arch_window(c, 450, 250, 16, 28, (60, 50, 100))
    wall = linear(360, 300, 540, 300, (248, 240, 253), (200, 190, 225))
    c.rect(360, 300, 540, 405, wall)
    for x in range(362, 540, 22):
        c.rect(x, 288, x + 12, 301, wall)
        c.rect(x, 288, x + 12, 291, (255, 250, 255))
    c.rect(360, 300, 540, 305, (185, 175, 210))
    # gate
    c.ellipse_ring(450, 352, 27, 27, 5, (205, 195, 220), ymax=352)
    c.rect(422, 352, 427, 405, (205, 195, 220))
    c.rect(473, 352, 478, 405, (205, 195, 220))
    c.rect(427, 352, 473, 405, (75, 50, 60))
    c.ellipse(450, 352, 23, 23, (75, 50, 60), ymax=352)
    for x in (434, 442, 450, 458, 466):
        c.rect(x - 1, 335, x + 1, 405, (130, 110, 105))
    for y in (360, 375, 390):
        c.rect(427, y - 1, 473, y + 1, (130, 110, 105))
    # front towers
    tower(c, 345, 28, 262, 412, (242, 232, 250), CASTLE_BLUE, 175, 38)
    tower(c, 555, 28, 262, 412, (242, 232, 250), CASTLE_BLUE, 175, 38)
    for x in (345, 555):
        arch_window(c, x, 320, 12, 22, (60, 50, 100))
        arch_window(c, x, 372, 10, 18, (60, 50, 100))
    # bushes at the castle foot
    for x, y, rx, ry in ((300, 425, 42, 24), (330, 432, 30, 18), (600, 425, 42, 24), (570, 432, 30, 18)):
        shaded_sphere(c, x, y, rx, (90, 175, 95), ry=ry, amb=0.5, kd=0.6, spec=0.08)

    # path
    c.polygon([(432, 405), (468, 405), (515, 470), (610, 600), (310, 600), (390, 470)],
              linear(450, 405, 450, 600, (248, 225, 185), (215, 180, 140)))
    for i, (x, y, r) in enumerate(((452, 430, 9), (440, 470, 12), (470, 515, 14), (430, 560, 16))):
        shaded_sphere(c, x, y, r * 1.6, (225, 205, 175), ry=r * 0.55, amb=0.6, kd=0.5, spec=0.1)

    # big mushroom
    drop_shadow(c, 120, 563, 75, 11, 0.38)
    stem = cylinder(120, 22, (248, 238, 218), top=430, bottom=560, ao=0.3, spec=0.1)
    c.rect(98, 430, 142, 560, stem)
    c.ellipse(120, 560, 22, 6, stem, ymin=560)
    c.ellipse(120, 436, 80, 60, sphere(120, 436, 80, (225, 55, 70), ry=60, spec=0.35, shin=24), ymax=436.5)
    c.ellipse(120, 436, 80, 12, linear(0, 436, 0, 448, (240, 205, 185), (200, 160, 145)), ymin=436)
    for i, (x, y, rx, ry) in enumerate(SPOTS):
        if "spots" in d and i == 2:
            continue
        c.ellipse(x, y, rx, ry, sphere(x, y, rx, (255, 250, 245), ry=ry, amb=0.75, kd=0.3, spec=0.3))
    # small mushroom
    drop_shadow(c, 205, 567, 36, 6, 0.35)
    stem = cylinder(205, 8, (248, 238, 218), top=525, bottom=565, ao=0.3)
    c.rect(197, 525, 213, 565, stem)
    c.ellipse(205, 528, 36, 28, sphere(205, 528, 36, (225, 55, 70), ry=28, spec=0.35), ymax=528.5)
    c.ellipse(205, 528, 36, 6, (230, 195, 175), ymin=528)
    for x, y, rx, ry in ((193, 515, 5, 4), (216, 511, 6, 4)):
        c.ellipse(x, y, rx, ry, sphere(x, y, rx, (255, 250, 245), ry=ry, amb=0.75, kd=0.3, spec=0.3))

    # pedestal for the floating gem
    drop_shadow(c, 760, 562, 48, 9, 0.4)
    plinth = cylinder(760, 34, (190, 185, 210), spec=0.1)
    c.rect(726, 548, 794, 562, plinth)
    c.ellipse(760, 562, 34, 6, plinth, ymin=562)
    c.ellipse(760, 548, 34, 6, (215, 210, 232))
    c.rect(736, 478, 784, 548, cylinder(760, 24, (185, 180, 205), top=478, bottom=548, ao=0.3, spec=0.12))
    cap = cylinder(760, 32, (200, 195, 222), spec=0.15)
    c.rect(728, 470, 792, 482, cap)
    c.ellipse(760, 482, 32, 6, cap, ymin=482)
    c.ellipse(760, 470, 32, 7, (232, 228, 245))

    # flowers
    rnd = random.Random(11)
    for i in range(26):
        x, y = rnd.randint(10, 890), rnd.randint(455, 590)
        if 300 < x < 620 or (40 < x < 240 and y < 570) or (700 < x < 820):
            continue
        col = [(255, 120, 170), (255, 225, 90), (255, 255, 255), (190, 140, 255)][i % 4]
        c.line(x, y, x, y + 12, 2, (60, 140, 70), caps=False)
        shaded_sphere(c, x, y, 5, col, amb=0.55, kd=0.55, spec=0.3)


def l4_balloon(c, m):
    base = (60, 120, 230) if m else (225, 60, 70)
    stripe = (255, 210, 70)
    for x0, x1 in ((772, 780), (808, 800)):
        c.line(x0, 172, x1, 190, 1.4, (110, 85, 70))
    c.rect(778, 188, 802, 206, cylinder(790, 12, (175, 115, 65), spec=0.1))
    c.rect(777, 186, 803, 190, (140, 90, 50))
    c.ellipse(790, 125, 40, 46, sphere(790, 125, 40, base, ry=46, spec=0.4, shin=30))
    c.ellipse(790, 125, 14, 46, sphere(790, 125, 40, stripe, ry=46, spec=0.4, shin=30))
    c.polygon([(770, 160), (810, 160), (803, 176), (777, 176)], cylinder(790, 20, lit(base, 0.85), spec=0.1))


def l4_island(c, m):
    c.polygon([(103, 178), (227, 178), (200, 212), (172, 252), (146, 214)],
              linear(110, 178, 220, 250, (170, 125, 100), (80, 55, 60)))
    c.polygon([(130, 200), (150, 200), (160, 232)], (120, 85, 75))
    c.rect(196, 182, 202, 246, lambda px, py: (175, 225, 255, max(0.0, 0.85 * (1 - (py - 182) / 64))))
    c.ellipse(165, 178, 63, 15, sphere(165, 178, 63, (115, 205, 105), ry=15, amb=0.6, kd=0.5, spec=0.08))
    if not m:
        c.rect(166, 140, 174, 175, cylinder(170, 4, (130, 85, 55)))
        shaded_sphere(c, 158, 148, 14, (75, 165, 90), amb=0.5, kd=0.6, spec=0.1)
        shaded_sphere(c, 172, 134, 20, (85, 175, 95), amb=0.5, kd=0.6, spec=0.1)
    shaded_sphere(c, 130, 172, 6, (255, 130, 170), spec=0.3)
    shaded_sphere(c, 205, 174, 5, (255, 230, 100), spec=0.3)


def l4_flag(x, apex):
    y = apex - 24

    def d(c, m):
        c.polygon([(x + 1, y), (x + 27, y + 7), (x + 1, y + 14)], linear(x, y, x + 27, y + 14, (255, 130, 175), (200, 60, 120)))
    return d


def l4_window_glow(x, y, w, h):
    def d(c, m):
        glow_disc(c, x, y, w * 2.4, (255, 200, 90), 0.55)
        arch_window(c, x, y, w, h, (255, 222, 130))
        arch_window(c, x, y + h * 0.15, w * 0.5, h * 0.5, (255, 245, 200))
    return d


def l4_gem(c, m):
    base = GEM_B if m else GEM_A
    T, L, R, B, C = (760, 382), (737, 418), (783, 418), (760, 458), (756, 416)
    c.polygon([T, L, C], lit(base, 1.25))
    c.polygon([T, C, R], lit(base, 0.95))
    c.polygon([L, B, C], lit(base, 0.78))
    c.polygon([C, B, R], lit(base, 0.58))
    c.line(T[0], T[1], C[0], C[1], 1.4, (255, 255, 255, 0.7))
    c.line(L[0], L[1], C[0], C[1], 1.2, (255, 255, 255, 0.45))
    c.polygon([(752, 394), (745, 410), (751, 408)], (255, 255, 255, 0.8))


def l4_gem_glow(c, m):
    glow_disc(c, 760, 420, 60, GEM_B if m else GEM_A, 0.5, power=1.8)


def l4_fairy(c, m):
    glow_disc(c, 660, 360, 24, (255, 240, 180), 0.6)
    for x, y, rx, ry in ((651, 352, 9, 6), (669, 352, 9, 6), (653, 363, 6, 4), (667, 363, 6, 4)):
        c.ellipse(x, y, rx, ry, (205, 240, 255, 0.75))
    shaded_sphere(c, 660, 363, 4.5, (255, 190, 225), spec=0.4)
    shaded_sphere(c, 660, 355, 4, (255, 225, 205), spec=0.4)


GEM_BOB = dict(bobAmplitude=(0, 8), bobSpeed=0.4)
SPARKLES4 = [(300, 140), (610, 120), (420, 300), (505, 180), (720, 265), (240, 320), (830, 330),
             (60, 300), (860, 60), (400, 40), (700, 455), (820, 420)]
PETALS = [(300, 30), (520, 15), (700, 55), (850, 25), (150, 10)]

L4_ELEMENTS = [
    # parallax clouds: far = small, pale, slow; near = big, fast
    E("cloud_far1", lambda c, m: cloud3d(c, 250, 70, 0.5, alpha=0.8), anim=drift_across(*cloud_extent(250, 0.5), 7)),
    E("cloud_far2", lambda c, m: cloud3d(c, 640, 45, 0.45, alpha=0.75), anim=drift_across(*cloud_extent(640, 0.45), 6)),
    E("cloud_near", lambda c, m: cloud3d(c, 470, 36, 0.95), anim=drift_across(*cloud_extent(470, 0.95), 16)),
] + [
    E("sparkle%d" % i, (lambda x, y: lambda c, m: sparkle(c, x, y, 7))(x, y),
      anim=dict(twinkle=0.9, twinkleSpeed=0.35 + (i * 29 % 9) / 12, pulse=0.3,
                scaleSpeed=0.35 + (i * 29 % 9) / 12, rotateSpeed=20 if i % 2 else -20, phase=(i * 0.173) % 1))
    for i, (x, y) in enumerate(SPARKLES4)
] + [
    E("island", l4_island, pivot=(165, 190), variant=True,
      anim=dict(bobAmplitude=(0, 10), bobSpeed=0.18, swingAngle=2, swingSpeed=0.12)),
    E("balloon", l4_balloon, pivot=(790, 125), variant=True,
      anim=dict(bobAmplitude=(0, 8), bobSpeed=0.2, swingAngle=3, swingSpeed=0.15)),
    E("flag_left", l4_flag(345, 175), pivot=(346, 158), show="A",
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.6, swingAngle=4, swingSpeed=1.2)),
    E("flag_keep", l4_flag(450, 100), pivot=(451, 83),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.4, swingAngle=4, swingSpeed=1.0, phase=0.3)),
    E("flag_right", l4_flag(555, 175), pivot=(556, 158),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.7, swingAngle=4, swingSpeed=1.3, phase=0.6)),
    E("window_keep", l4_window_glow(450, 250, 16, 28), anim=dict(twinkle=0.3, twinkleSpeed=0.6)),
    E("window_left", l4_window_glow(345, 320, 12, 22), anim=dict(twinkle=0.3, twinkleSpeed=0.8, phase=0.4)),
    E("window", l4_window_glow(555, 320, 12, 22), show="A", anim=dict(twinkle=0.3, twinkleSpeed=0.7, phase=0.7)),
    # floating gem: the contact shadow shrinks and fades while the gem rises (same speed & phase)
    E("gem_shadow", lambda c, m: drop_shadow(c, 760, 471, 24, 5, 0.55),
      anim=dict(pulse=-0.3, scaleSpeed=0.4, twinkle=0.6, twinkleSpeed=0.4)),
    E("gem_glow", l4_gem_glow, pivot=(760, 420), variant=True,
      anim=dict(GEM_BOB, pulse=0.12, scaleSpeed=0.8, twinkle=0.25, twinkleSpeed=0.8)),
    E("gem", l4_gem, pivot=(760, 420), variant=True, anim=dict(GEM_BOB, spinSpeed=0.3, spinShade=0.35)),
    # fairy circling the right tree; it flies the other way round in the modified picture
    E("fairy", l4_fairy, pivot=(660, 360),
      anim=dict(orbitRadius=(70, 20), orbitSpeed=0.18, orbitDepth=0.35, stretch=(0.25, 0), scaleSpeed=4),
      animB=dict(orbitRadius=(70, 20), orbitSpeed=-0.18, orbitDepth=0.35, stretch=(0.25, 0), scaleSpeed=4)),
] + [
    E("petal%d" % i, petal_draw(x, y, (255, 170, 200) if i % 2 else (255, 215, 230)),
      anim=dict(driftVelocity=(-14, -30), driftLength=360, driftFade=True, rotateSpeed=90 + 25 * i,
                bobAmplitude=(10, 0), bobSpeed=0.4, phase=i / len(PETALS)))
    for i, (x, y) in enumerate(PETALS)
]

L4_DIFFS = [
    ("balloon", 790, 135, 50),
    ("island_tree", 168, 140, 32),
    ("flag", 358, 158, 26),
    ("window", 555, 320, 24),
    ("gem", 760, 420, 46),
    ("fairy", 660, 360, 82),
    ("spots", 150, 412, 22),
]


# =================================================================== Level 05
MUSHROOMS5 = [(690, 545, 16), (720, 562, 12), (660, 566, 10), (760, 528, 18)]
BREW_A, BREW_B = (120, 255, 130), (200, 110, 255)


def l5_background(c, d):
    """魔法森林 - static part"""
    c.gradient(0, 390, (18, 22, 66), (88, 58, 135))
    rnd = random.Random(5)
    for _ in range(90):
        x, y = rnd.randint(0, W), rnd.randint(0, 300)
        if math.hypot(x - 720, y - 100) < 80 or x < 330 and y < 160:
            continue
        c.circle(x, y, rnd.choice((0.9, 1.2, 1.6)), (230, 235, 255))
    # moon
    glow_disc(c, 720, 100, 160, (190, 210, 255), 0.32, power=1.6)
    shaded_sphere(c, 720, 100, 45, (238, 238, 252), amb=0.72, kd=0.4, spec=0.04)
    c.ellipse(704, 88, 9, 7, (210, 212, 235, 0.7))
    c.ellipse(736, 116, 7, 5, (210, 212, 235, 0.7))
    c.ellipse(728, 84, 4, 3, (210, 212, 235, 0.7))
    # forest layers + mist (aerial perspective)
    rnd = random.Random(9)
    for x in range(-20, 940, 38):
        pine(c, x + rnd.randint(-10, 10), 365, rnd.randint(80, 130), (52, 60, 120))
    c.rect(0, 290, W, 400, lambda px, py: (175, 185, 250, 0.32 * max(0.0, 1 - abs(py - 350) / 50)))
    for x in range(10, 940, 55):
        pine(c, x + rnd.randint(-12, 12), 398, rnd.randint(110, 170), (32, 42, 88))
    c.rect(0, 385, W, H, linear(0, 385, 0, H, (38, 80, 88), (16, 38, 48)))

    # big tree house
    trunk = cylinder(160, 55, (115, 78, 58), top=100, bottom=540, ao=0.35, spec=0.05)
    c.rect(105, 90, 215, 540, trunk)
    for pts in ([(108, 495), (60, 548), (112, 542), (135, 512)], [(212, 495), (262, 550), (208, 542), (185, 512)]):
        c.polygon(pts, linear(pts[0][0], 495, pts[1][0], 550, (110, 75, 55), (70, 45, 35)))
    for x0, x1 in ((128, 124), (190, 196), (150, 147)):
        c.line(x0, 140, x1, 470, 2, (80, 52, 40, 0.7), caps=False)
    # branch for owl and lantern
    c.polygon([(205, 222), (345, 205), (345, 213), (205, 238)], linear(0, 205, 0, 238, (125, 88, 64), (70, 45, 35)))
    # canopy
    for x, y, r in ((60, 70, 70), (300, 60, 62), (130, 20, 95), (235, 40, 80)):
        shaded_sphere(c, x, y, r, (40, 105, 95), amb=0.45, kd=0.6, spec=0.05)
    # door
    c.ellipse(160, 472, 25, 25, (70, 45, 32), ymax=472)
    c.rect(135, 472, 185, 528, (70, 45, 32))
    c.ellipse(160, 472, 21, 21, linear(140, 0, 180, 0, (150, 95, 60), (100, 62, 40)), ymax=472)
    c.rect(139, 472, 181, 528, linear(139, 0, 181, 0, (150, 95, 60), (100, 62, 40)))
    for x in (150, 160, 170):
        c.rect(x - 0.7, 455, x + 0.7, 528, (85, 55, 38))
    glow_disc(c, 160, 470, 16, (255, 200, 110), 0.5)
    c.circle(160, 470, 5, (255, 220, 140))
    shaded_sphere(c, 174, 500, 3, (240, 200, 90), spec=0.6)
    # tree window (round in A, square in B)
    glow_disc(c, 178, 330, 40, (255, 200, 110), 0.38)
    if "treewindow" in d:
        c.rect(161, 313, 195, 347, (70, 45, 30))
        c.rect(165, 317, 191, 343, (255, 214, 120))
        c.rect(177, 317, 179, 343, (110, 70, 45))
        c.rect(165, 329, 191, 331, (110, 70, 45))
    else:
        c.circle(178, 330, 17, (70, 45, 30))
        c.circle(178, 330, 13, (255, 214, 120))
        c.rect(177, 317, 179, 343, (110, 70, 45))
        c.rect(165, 329, 191, 331, (110, 70, 45))
    # owl body (head is animated)
    shaded_sphere(c, 305, 200, 17, (135, 100, 78), ry=22, amb=0.5, kd=0.6, spec=0.08)
    c.ellipse(305, 206, 10, 14, (205, 180, 145))
    for x in (299, 311):
        c.ellipse(x, 214, 4, 2.5, (240, 170, 60))

    # pond
    c.ellipse(470, 485, 152, 40, (55, 95, 105))
    c.ellipse(470, 485, 148, 37, linear(0, 448, 0, 522, (70, 115, 185), (30, 60, 120)))
    c.ellipse(512, 476, 48, 7, glow(512, 476, 48, (225, 232, 255), 0.6, ry=7))
    for x, y in ((420, 497), (520, 472), (470, 508), (562, 494)):
        c.ellipse(x, y, 18, 6, sphere(x, y, 18, (65, 155, 95), ry=6, amb=0.55, kd=0.55, spec=0.15))
        c.polygon([(x, y), (x + 18, y - 2), (x + 18, y + 2)], (45, 85, 135))
    if "lotus" not in d:
        for x, y, rx, ry in ((513, 465, 5, 7), (527, 465, 5, 7), (520, 461, 5, 9)):
            c.ellipse(x, y, rx, ry, sphere(x, y, rx, (255, 160, 205), ry=ry, amb=0.6, kd=0.5, spec=0.3))
        shaded_sphere(c, 520, 468, 3, (255, 225, 110), spec=0.4)

    # stepping stones
    for x, y, rx in ((640, 520, 20), (612, 556, 22), (585, 590, 24)):
        drop_shadow(c, x + 2, y + 5, rx + 3, 6, 0.4)
        shaded_sphere(c, x, y, rx, (125, 130, 158), ry=rx * 0.38, amb=0.5, kd=0.6, spec=0.2)

    # cauldron on a little fire
    glow_disc(c, 380, 590, 85, (255, 140, 60), 0.3, ry=22)
    for x0, x1 in ((345, 412), (352, 405)):
        c.line(x0, 596, x1, 584, 7, cylinder(380, 40, (110, 70, 45), spec=0.05))
    for x in (352, 408):
        c.line(380 + (x - 380) * 0.7, 565, x, 592, 4, (45, 40, 55))
    shaded_sphere(c, 380, 550, 42, (60, 55, 78), ry=33, amb=0.45, kd=0.6, spec=0.55, shin=40)
    c.ellipse_ring(380, 522, 41, 9, 4, (95, 90, 112))
    c.ellipse(380, 522, 37, 6, (25, 20, 32))

    # glowing mushrooms
    for i, (x, y, r) in enumerate(MUSHROOMS5):
        if "mushroom" in d and i == 3:
            continue
        glow_disc(c, x, y + r * 0.9, r * 2.6, (90, 220, 240), 0.25, ry=r * 0.8)
        stem = cylinder(x, r * 0.32, (205, 232, 238), spec=0.1)
        c.rect(x - r * 0.32, y, x + r * 0.32, y + r * 1.1, stem)
        c.ellipse(x, y + 1, r, r * 0.75, sphere(x, y + 1, r, (85, 215, 235), ry=r * 0.75, amb=0.78, kd=0.35, spec=0.35), ymax=y + 1.5)
        c.ellipse(x, y + 1, r, r * 0.16, (60, 165, 190), ymin=y + 1)
        for dx, dy in ((-0.4, -0.35), (0.3, -0.5), (0.1, -0.15)):
            c.circle(x + dx * r, y + dy * r, r * 0.12, (220, 255, 255))
    # ferns
    for bx, by, s in ((20, 600, 1.0), (860, 600, 1.1), (300, 600, 0.8)):
        for k in range(-3, 4):
            a = math.radians(-90 + k * 22)
            ex, ey = bx + math.cos(a) * 70 * s, by + math.sin(a) * 70 * s
            c.polygon([(bx, by), (bx + (ex - bx) * 0.5 - 6, by + (ey - by) * 0.5), (ex, ey), (bx + (ex - bx) * 0.5 + 6, by + (ey - by) * 0.5)],
                      linear(bx, by, ex, ey, (25, 70, 60), (60, 130, 100)))


def l5_firefly(x, y):
    def d(c, m):
        glow_disc(c, x, y, 9, (200, 255, 140), 0.75)
        c.circle(x, y, 1.8, (250, 255, 220))
    return d


def l5_bat(c, m):
    col = (32, 26, 50)
    c.polygon([(604, 88), (578, 78), (582, 86), (574, 90), (588, 94), (598, 98)], col)
    c.polygon([(616, 88), (642, 78), (638, 86), (646, 90), (632, 94), (622, 98)], col)
    c.ellipse(610, 92, 6, 9, col)
    c.polygon([(605, 85), (606, 77), (609, 84)], col)
    c.polygon([(615, 85), (614, 77), (611, 84)], col)
    c.circle(607.5, 89, 1.1, (255, 200, 120))
    c.circle(612.5, 89, 1.1, (255, 200, 120))


def l5_owl_head(c, m):
    for s in (-1, 1):
        c.polygon([(305 + s * 8, 160), (305 + s * 17, 147), (305 + s * 15, 163)], (110, 80, 62))
    shaded_sphere(c, 305, 172, 17, (140, 108, 84), ry=15, amb=0.5, kd=0.6, spec=0.08)
    for s in (-1, 1):
        x = 305 + s * 7
        c.circle(x, 172, 7, (225, 205, 170))
        c.circle(x, 172, 4.6, (255, 205, 60))
        c.circle(x, 172, 2.3, (20, 15, 25))
        c.circle(x - 1.2, 170.8, 0.9, WHITE)
    c.polygon([(302, 177), (308, 177), (305, 183)], (240, 160, 60))


def l5_lantern(c, m):
    c.line(240, 214, 240, 246, 1.5, (60, 45, 35))
    if not m:
        glow_disc(c, 240, 262, 46, (255, 190, 90), 0.5, power=1.7)
    c.polygon([(232, 248), (248, 248), (244, 241), (236, 241)], (60, 55, 70))
    glass = (255, 215, 120) if not m else (70, 72, 95)
    c.rect(231, 249, 249, 275, cylinder(240, 9, glass, amb=0.8 if not m else 0.5, spec=0.3))
    if not m:
        c.ellipse(240, 264, 3, 6, (255, 250, 220))
    for x in (231, 240, 249):
        c.rect(x - 0.8, 249, x + 0.8, 275, (55, 50, 65))
    c.polygon([(230, 275), (250, 275), (246, 281), (234, 281)], (60, 55, 70))


def l5_crystal(c, m):
    base = (170, 120, 255)
    T, B = (600, 298), (600, 364)
    L1, R1, L2, R2 = (587, 318), (613, 318), (587, 345), (613, 345)
    M1, M2 = (603, 316), (603, 347)
    c.polygon([T, L1, M1], lit(base, 1.3))
    c.polygon([T, M1, R1], lit(base, 0.95))
    c.polygon([L1, M1, M2, L2], lit(base, 1.1))
    c.polygon([M1, R1, R2, M2], lit(base, 0.7))
    c.polygon([L2, M2, B], lit(base, 0.85))
    c.polygon([M2, R2, B], lit(base, 0.55))
    c.line(593, 322, 593, 340, 1.5, (255, 255, 255, 0.6))


def l5_wisp(c, m):
    glow_disc(c, 160, 300, 20, (140, 210, 255), 0.75)
    c.circle(160, 300, 4, (240, 250, 255))


def l5_leaf(x, y, col):
    def d(c, m):
        c.polygon([(x - 8, y), (x - 3, y - 4), (x + 4, y - 4), (x + 8, y), (x + 4, y + 4), (x - 3, y + 4)],
                  linear(x - 8, y - 4, x + 8, y + 4, lit(col, 1.2), lit(col, 0.75)))
        c.line(x - 8, y, x + 8, y, 0.8, lit(col, 0.6))
    return d


def l5_mushroom_glow(x, y, r):
    def d(c, m):
        glow_disc(c, x, y - r * 0.2, r * 2.4, (110, 235, 255), 0.4)
    return d


def l5_ripple(x, y):
    def d(c, m):
        c.ellipse_ring(x, y, 20, 5, 1.6, (180, 210, 255, 0.8))
    return d


def l5_brew(c, m):
    col = BREW_B if m else BREW_A
    glow_disc(c, 380, 512, 60, col, 0.35, ry=32)
    c.ellipse(380, 522, 36, 6, sphere(380, 522, 36, col, ry=6, amb=0.85, kd=0.3, spec=0.5))


def l5_bubble(x, y):
    def d(c, m):
        col = BREW_B if m else BREW_A
        shaded_sphere(c, x, y, 4.5, col, amb=0.7, kd=0.4, spec=0.7, shin=30)
    return d


def l5_flame(c, m):
    glow_disc(c, 380, 582, 26, (255, 160, 60), 0.45)
    c.polygon([(362, 592), (398, 592), (393, 576), (386, 581), (380, 561), (374, 579), (367, 573)], (255, 140, 40))
    c.polygon([(370, 592), (390, 592), (386, 581), (380, 571), (374, 583)], (255, 225, 110))


FIREFLIES = [(420, 400), (560, 410), (650, 450), (820, 480), (90, 420), (290, 470), (760, 380),
             (340, 330), (500, 560), (860, 330), (240, 560), (620, 260)]
LEAVES = [(110, 120, (230, 150, 60)), (260, 100, (90, 190, 150)), (60, 160, (240, 190, 80)),
          (330, 90, (230, 120, 70)), (190, 150, (120, 200, 160))]

L5_ELEMENTS = [
    E("moon_halo", lambda c, m: glow_disc(c, 720, 100, 85, (205, 220, 255), 0.3), anim=dict(pulse=0.06, scaleSpeed=0.2)),
    E("bat", l5_bat, show="A", pivot=(610, 90),
      anim=dict(stretch=(0, 0.6), scaleSpeed=3, bobAmplitude=(22, 9), bobSpeed=0.12)),
    E("crystal_glow", lambda c, m: glow_disc(c, 600, 331, 60, (180, 130, 255), 0.4), pivot=(600, 331),
      anim=dict(bobAmplitude=(0, 7), bobSpeed=0.3, pulse=0.12, scaleSpeed=0.6, twinkle=0.3, twinkleSpeed=0.6)),
    E("crystal", l5_crystal, pivot=(600, 331), anim=dict(bobAmplitude=(0, 7), bobSpeed=0.3, spinSpeed=0.22, spinShade=0.3)),
    E("wisp", l5_wisp, pivot=(160, 300),
      anim=dict(orbitRadius=(90, 24), orbitSpeed=0.14, orbitDepth=0.4, twinkle=0.3, twinkleSpeed=1.2)),
    E("owl_head", l5_owl_head, pivot=(305, 186),
      anim=dict(swingAngle=22, swingSpeed=0.22), animB={}),
    E("lantern", l5_lantern, pivot=(240, 214), variant=True,
      anim=dict(swingAngle=6, swingSpeed=0.35, twinkle=0.15, twinkleSpeed=2.2),
      animB=dict(swingAngle=6, swingSpeed=0.35)),
] + [
    E("ripple%d" % i, l5_ripple(x, y),
      anim=dict(driftVelocity=(0, -0.5), driftLength=2, driftFade=True, driftGrow=1.8, phase=p))
    for i, (x, y, p) in enumerate(((430, 497, 0.0), (430, 497, 0.5), (505, 505, 0.25)))
] + [
    E("brew", l5_brew, pivot=(380, 520), variant=True,
      anim=dict(pulse=0.05, scaleSpeed=0.5, twinkle=0.25, twinkleSpeed=0.9)),
] + [
    E("bubble%d" % i, l5_bubble(x, 520), variant=True,
      anim=dict(driftVelocity=(2, 24), driftLength=42, driftFade=True, driftGrow=0.5, phase=i / 3))
    for i, x in enumerate((370, 384, 392))
] + [
    E("flame", l5_flame, pivot=(380, 592),
      anim=dict(stretch=(0.08, 0.3), scaleSpeed=5, twinkle=0.15, twinkleSpeed=3)),
] + [
    E("mushroom_glow%d" % i, l5_mushroom_glow(x, y, r), show="A" if i == 3 else "both",
      anim=dict(pulse=0.12, scaleSpeed=0.3 + 0.07 * i, twinkle=0.45, twinkleSpeed=0.3 + 0.07 * i, phase=i * 0.27))
    for i, (x, y, r) in enumerate(MUSHROOMS5)
] + [
    E("firefly%d" % i, l5_firefly(x, y),
      anim=dict(orbitRadius=(12 + i * 7 % 15, 8 + i * 5 % 9), orbitSpeed=(0.12 + (i % 4) * 0.05) * (1 if i % 2 else -1),
                bobAmplitude=(0, 6), bobSpeed=0.3, twinkle=0.85, twinkleSpeed=0.45 + (i % 5) * 0.15, phase=(i * 0.31) % 1))
    for i, (x, y) in enumerate(FIREFLIES)
] + [
    E("leaf%d" % i, l5_leaf(x, y, col),
      anim=dict(driftVelocity=(8, -26), driftLength=380, driftFade=True, rotateSpeed=-70 - 20 * i,
                bobAmplitude=(14, 0), bobSpeed=0.35, phase=i / len(LEAVES)))
    for i, (x, y, col) in enumerate(LEAVES)
]

L5_DIFFS = [
    ("treewindow", 178, 330, 24),
    ("lantern", 240, 262, 32),
    ("owl", 305, 172, 28),
    ("lotus", 520, 466, 20),
    ("brew", 380, 515, 46),
    ("mushroom", 760, 525, 30),
    ("bat", 610, 90, 44),
]


LEVELS = [
    ("Level04", "童话城堡", l4_background, L4_ELEMENTS, L4_DIFFS, 130),
    ("Level05", "魔法森林", l5_background, L5_ELEMENTS, L5_DIFFS, 140),
]
