# -*- coding: utf-8 -*-
"""Everyday-town themes, part 12: festivals and special places (paper-craft, full-bleed, no real brands or logos):
  Level610 灯光节     - a winter light festival at night: light tunnel, glowing sculptures, visitors
  Level611 舞狮       - a lion dance in an old street: two lions, drummer, firecrackers, red lanterns
  Level612 庙会       - a temple fair: gate, stalls of toys and snacks, sugar figures, crowds
  Level613 秋日古寺   - an old temple in autumn: pagoda, maples, stone lanterns, monk sweeping leaves
  Level614 圣诞老人工坊 - Santa's workshop: workbenches, toys, elves, sleigh, fireplace
  Level615 丰收市集   - a harvest fair: hay bales, pumpkin contest, pie stand, tractor ride, bunting
  Level616 水灯节     - a floating-lantern night on a river: lanterns on the water, bridge, temple silhouettes
  Level617 动车检修库 - a high-speed train depot: trains on inspection pits, gantries, workers
  Level618 天文馆     - a planetarium: domed show with stars and planets, reclined audience, projector
  Level619 海边游乐码头 - a seaside amusement pier: carousel, big wheel, snack stand, gulls; day / night
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, sky, spin_el, tree_round
from fills import cloud_bank, far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_modern import crowd
from levels_daily3 import counter, room, wall_shelf, lantern
from levels_daily5 import maple
from levels_daily7 import sea
from stylekit import day_night, star_field, window_glow

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
NIGHT_EDGE = (110, 110, 140)


def npiece(c, shapes, col, border=1.5, shadow=PROP):
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


def lion(c, x, base, body=(220, 50, 50), mane=(250, 200, 60), s=1.0, face_right=True):
    k = 1 if face_right else -1
    npiece(c, [RRect(x - 70 * s, base - 70 * s, x + 50 * s, base - 30 * s, 16 * s)], body)
    flat(c, [Thick(x - 60 * s + j * 22 * s, base - 70 * s, x - 50 * s + j * 22 * s, base - 30 * s, 4 * s) for j in range(5)], mane)
    for dx in (-50, -20, 20, 40):
        flat(c, RRect(x + dx * s - 5 * s, base - 34 * s, x + dx * s + 5 * s, base, 2), (250, 250, 250))
    hx = x + k * 66 * s
    npiece(c, [Circ(hx, base - 70 * s, 34 * s)], mane)
    npiece(c, [Circ(hx, base - 72 * s, 26 * s)], body)
    flat(c, [Circ(hx - 10 * s, base - 82 * s, 7 * s), Circ(hx + 10 * s, base - 82 * s, 7 * s)], (250, 250, 250))
    flat(c, [Circ(hx - 10 * s, base - 82 * s, 3 * s), Circ(hx + 10 * s, base - 82 * s, 3 * s)], INK)
    flat(c, [Ell(hx, base - 62 * s, 16 * s, 8 * s)], (250, 250, 250))
    flat(c, Circ(hx, base - 102 * s, 8 * s), (60, 160, 120))


# =================================================================== Level 610 winter light festival (night)
def l610_bg(c, d):
    c.gradient(0, 360, (16, 20, 50), (40, 40, 80))
    rnd = random.Random(6101)
    for _ in range(50):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 220), rnd.choice((1.2, 1.8))), (250, 246, 220))
    far_skyline(c, 300, 60, 200, (40, 44, 70), 6102, win=(120, 110, 150))
    c.rect(0, 360, W, H, (200, 210, 230))
    for k in range(20):
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(380, 600), rnd.uniform(40, 90), 5), (186, 196, 220))
    # light tunnel (arches of bulbs)
    for k in range(5):
        r = 170 - k * 18
        c.ellipse_ring(450, 420, r, r * 0.9, 3, (90, 100, 140), ymax=420)
        for j in range(18):
            a = math.pi * j / 17
            col = [(255, 220, 120), (150, 220, 255), (255, 150, 200)][(j + k) % 3]
            flat(c, Circ(450 - r * math.cos(a), 420 - r * 0.9 * math.sin(a), 5), col)
    # glowing sculptures: deer (left), giant star (right)
    deer = (150, 220, 255) if "deer" not in d else (255, 200, 120)
    flat(c, [Ell(140, 420, 50, 22), Thick(180, 410, 200, 340, 8), Ell(206, 334, 14, 10)] +
         [Thick(x, 430, x, 500, 6) for x in (110, 130, 160, 178)] + [Thick(198, 326, 186, 296, 4), Thick(206, 326, 220, 296, 4)], deer)
    soft_union(c, [Ell(140, 420, 50, 22)], deer, 0.3, spread=20)
    npiece(c, Poly(star_pts(760, 360, 60, 26)), (255, 230, 120) if "star" not in d else (255, 140, 200), shadow=SMALL)
    flat(c, Thick(760, 420, 760, 500, 6), (90, 100, 140))
    # visitors in silhouette-ish winter coats
    for k, (x, col) in enumerate(((300, (200, 70, 70)), (380, (60, 90, 150)), (560, (240, 200, 90)), (640, (90, 150, 110)))):
        if k == 2 and "coat" in d:
            col = (250, 250, 250)
        modern(c, x, 600, col, bottom=(40, 40, 50), hair=(40, 30, 30), h=2.2, style="long" if k % 2 else "short")
    # hot drink stand
    npiece(c, [RRect(20, 520, 150, 600, 3), Poly([(10, 524), (160, 524), (140, 494), (30, 494)])], (150, 100, 70))
    flat(c, RRect(30, 536, 140, 560, 2), (255, 220, 140) if "stand" not in d else (140, 220, 255))


L610_ELEMENTS = [
    E("tunnelglow", lambda c, m: soft_union(c, [Ell(450, 330, 170, 90)], (255, 220, 160), 0.15, spread=40), daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.6)),
    E("sparkle", lambda c, m: [flat(c, Poly(star_pts(450 + 140 * math.cos(a), 300 - 80 * math.sin(a), 6, 2, points=4)), (255, 255, 230)) for a in (0.4, 1.4, 2.4)],
      daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=1.2)),
    E("starglow", lambda c, m: soft_union(c, [Circ(760, 360, 40)], (255, 230, 140), 0.3, spread=40), daynight="untinted", anim=dict(pulse=0.08, scaleSpeed=0.6)),
    E("steam", lambda c, m: soft_union(c, [Circ(90, 486, 6)], (240, 240, 250), 0.6, spread=6), anim=dict(driftVelocity=(2, 16), driftLength=40, driftFade=True)),
]

L610_DIFFS = [
    ("stand", 85, 548, 0),
    ("deer", 160, 400, 0),
    ("star", 760, 360, 0),
    ("coat", 561, 540, 0),
]


# =================================================================== Level 611 lion dance
def l611_bg(c, d):
    sky(c, (140, 196, 236), (236, 236, 232), 200)
    # shophouses with red signs
    for k, x0 in enumerate((-10, 300, 610)):
        piece(c, RRect(x0, 40, x0 + 310, 380, 2), [(236, 214, 180), (220, 210, 200), (240, 220, 196)][k], border=1.5, shadow=PROP)
        for i in range(3):
            flat(c, RRect(x0 + 30 + i * 96, 70, x0 + 86 + i * 96, 140, 3), (150, 190, 220))
        col = (200, 40, 40) if not (k == 1 and "sign" in d) else (40, 90, 160)
        piece(c, RRect(x0 + 40, 170, x0 + 270, 214, 3), col, border=1.2, shadow=SMALL)
        sign_box(c, x0 + 60, 178, x0 + 250, 206, (250, 220, 100), 6111 + k, vertical=False)
        flat(c, RRect(x0 + 20, 240, x0 + 290, 380, 2), (90, 60, 50))
    # street
    piece(c, RRect(-10, 380, 910, 612, 0), (170, 160, 150), shadow=LAYER)
    # two lions
    lion(c, 300, 560, s=1.4)
    lion(c, 640, 540, body=(250, 190, 40) if "lion" not in d else (60, 150, 90), mane=(220, 60, 60), s=1.3, face_right=False)
    # drummer + drum
    npiece(c, [Ell(820, 560, 50, 18), RRect(770, 520, 870, 560, 6)], (200, 40, 40) if "drum" not in d else (60, 120, 200))
    flat(c, Ell(820, 520, 50, 14), (240, 220, 180))
    modern(c, 840, 600, (250, 200, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.2)
    # crowd behind a rope + firecracker string on a pole
    crowd(c, 20, 420, 400, 2, 6112, step=16, dy=18)
    flat(c, Thick(120, 380, 120, 240, 3), (90, 90, 100))
    flat(c, [RRect(110, 250 + k * 14, 130, 262 + k * 14, 3) for k in range(8)], (220, 40, 40))
    # oranges on a table (offering)
    piece(c, [RRect(460, 420, 560, 432, 2)], (150, 100, 70), shadow=PROP)
    flat(c, [Circ(478 + k * 16, 412 - (k % 2) * 8, 9) for k in range(5)], (250, 150, 40) if "oranges" not in d else (120, 190, 90))


L611_ELEMENTS = [
    lantern("lan%d" % i, x, 20, s=0.9) for i, x in enumerate((150, 450, 750))
] + [
    E("head", lambda c, m: (npiece(c, [Circ(392, 490, 34)], (250, 200, 60)), npiece(c, [Circ(392, 488, 26)], (220, 50, 50)),
                            flat(c, [Circ(382, 478, 7), Circ(402, 478, 7)], (250, 250, 250))), pivot=(392, 510), anim=dict(swingAngle=10, swingSpeed=1.0)),
    E("pop", lambda c, m: [flat(c, Poly(star_pts(120 + 18 * math.cos(a), 360 + 18 * math.sin(a), 8, 3)), (255, 220, 120)) for a in (0, 2.1, 4.2)],
      daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=2.0)),
    E("smoke", lambda c, m: soft_union(c, [Circ(130, 360, 10)], (220, 220, 226), 0.7, spread=10), anim=dict(driftVelocity=(10, 20), driftLength=80, driftFade=True)),
    E("stick", lambda c, m: flat(c, Thick(800, 500, 830, 470, 3), (150, 110, 70)), pivot=(800, 500), anim=dict(swingAngle=20, swingSpeed=2.0)),
]

L611_DIFFS = [
    ("sign", 455, 192, 0),
    ("lion", 560, 480, 0),
    ("drum", 820, 548, 0),
    ("oranges", 510, 410, 0),
]


# =================================================================== Level 612 temple fair
def l612_bg(c, d):
    sky(c, (140, 196, 236), (236, 236, 232), 200)
    # temple gate (centre)
    flat(c, RRect(380, 160, 520, 340, 0), (110, 80, 70))
    piece(c, [RRect(340, 100, 380, 340, 2), RRect(520, 100, 560, 340, 2)], (200, 50, 40), border=1.5, shadow=PROP)
    piece(c, Poly([(300, 110), (600, 110), (580, 70), (450, 50), (320, 70)]), (60, 70, 80), border=1.5, shadow=PROP)
    piece(c, RRect(400, 120, 500, 160, 3), (250, 200, 60) if "plaque" not in d else (60, 120, 200), border=1.2, shadow=SMALL)
    sign_box(c, 412, 126, 488, 154, (200, 50, 40), 6121, vertical=False)
    far_round_trees(c, 240, 30, (110, 160, 110), 6122, x0=-20, x1=340)
    far_round_trees(c, 240, 30, (110, 160, 110), 6123, x0=560, x1=920)
    piece(c, RRect(-10, 330, 910, 612, 0), (200, 186, 166), shadow=LAYER)
    # stalls (left: toys, right: snacks)
    for k, (x0, col) in enumerate(((20, (220, 60, 60)), (620, (250, 190, 50)))):
        if k == 1 and "awning" in d:
            col = (90, 160, 220)
        piece(c, Poly([(x0, 280), (x0 + 260, 280), (x0 + 250, 320), (x0 + 10, 320)]), col, border=1.5, shadow=PROP)
        flat(c, [Thick(x0 + 10, 320, x0 + 10, 470, 4), Thick(x0 + 250, 320, x0 + 250, 470, 4)], (120, 90, 70))
        piece(c, RRect(x0, 420, x0 + 260, 470, 3), (150, 110, 80), border=1.2, shadow=PROP)
    # toy stall goods: pinwheels + masks
    for k in range(5):
        x = 50 + k * 46
        flat(c, Thick(x, 420, x, 360, 2), (150, 110, 70))
        flat(c, [Poly([(x, 350), (x + 12, 344), (x + 6, 356)]), Poly([(x, 350), (x - 6, 338), (x + 6, 344)]), Poly([(x, 350), (x - 12, 356), (x - 6, 344)]),
                 Poly([(x, 350), (x + 6, 362), (x - 6, 356)])], [(240, 90, 90), (90, 170, 230), (250, 200, 60), (120, 200, 120), (200, 120, 220)][k])
    # snack stall: candied haws + steam basket
    for k in range(5):
        x = 650 + k * 40
        flat(c, Thick(x, 420, x, 350, 2), (200, 170, 120))
        flat(c, [Circ(x, 360 + j * 12, 6) for j in range(4)], (220, 40, 50) if not (k == 2 and "haw" in d) else (120, 200, 120))
    # sugar-figure maker in the middle
    piece(c, RRect(400, 440, 500, 500, 3), (150, 110, 80), border=1.2, shadow=PROP)
    piece(c, [Poly(star_pts(450, 420, 18, 8))], (250, 190, 60), border=1, shadow=SMALL)
    modern(c, 450, 560, (60, 90, 150), bottom=(40, 40, 50), hair=(240, 240, 246), h=1.8, glasses=True)
    # crowd + kids
    for k, (x, col, h) in enumerate(((130, (240, 200, 90), 2.3), (240, (200, 110, 150), 1.5), (330, (90, 150, 110), 2.3), (580, (120, 170, 220), 2.3),
                                     (690, (250, 160, 90), 1.5), (800, (150, 120, 180), 2.3))):
        if k == 3 and "shirt" in d:
            col = (250, 250, 250)
        modern(c, x, 600, col, bottom=(50, 50, 60), hair=[(40, 30, 30), (90, 60, 40), (220, 180, 90)][k % 3], h=h, style="twin" if h < 2 else "short")


L612_ELEMENTS = [
    lantern("lan%d" % i, x, 220, s=0.8) for i, x in enumerate((360, 540))
] + [
    E("pinwheel%d" % i, (lambda x, col: lambda c, m: flat(c, [Poly([(x, 350), (x + 12, 344), (x + 6, 356)]), Poly([(x, 350), (x - 6, 338), (x + 6, 344)]),
                                                             Poly([(x, 350), (x - 12, 356), (x - 6, 344)]), Poly([(x, 350), (x + 6, 362), (x - 6, 356)])], col))(x, col),
      pivot=(x, 350), anim=dict(rotateSpeed=180)) for i, (x, col) in enumerate(((96, (90, 170, 230)), (188, (120, 200, 120))))
] + [
    E("steam", lambda c, m: soft_union(c, [Circ(860, 400, 8)], (250, 250, 250), 0.7, spread=8), anim=dict(driftVelocity=(2, 20), driftLength=60, driftFade=True)),
    bird_el("bird", 450, 30, s=8, speed=-18),
]

L612_DIFFS = [
    ("plaque", 450, 140, 0),
    ("awning", 750, 300, 0),
    ("haw", 730, 378, 0),
    ("shirt", 581, 545, 0),
]


# =================================================================== Level 613 old temple in autumn
def stone_lantern(c, x, base, col=(170, 166, 160)):
    piece(c, [RRect(x - 18, base - 20, x + 18, base, 2), RRect(x - 6, base - 70, x + 6, base - 20, 2), RRect(x - 22, base - 100, x + 22, base - 70, 3),
              Poly([(x - 32, base - 100), (x + 32, base - 100), (x, base - 126)])], col, border=1.2, shadow=PROP)
    flat(c, RRect(x - 10, base - 94, x + 10, base - 76, 2), (60, 50, 50))


def l613_bg(c, d):
    sky(c, (140, 190, 230), (240, 230, 214), 260)
    far_ridge(c, 150, 60, (170, 150, 150), 6131)
    # pagoda (left back)
    for k in range(4):
        y = 270 - k * 52
        w = 80 - k * 12
        piece(c, RRect(160 - w * 0.6, y - 30, 160 + w * 0.6, y, 2), (200, 60, 50), border=1.2, shadow=PROP)
        piece(c, Poly([(160 - w - 10, y - 28), (160 + w + 10, y - 28), (160 + w * 0.5, y - 50), (160 - w * 0.5, y - 50)]), (60, 70, 80) if not (k == 2 and "eave" in d)
              else (90, 140, 90), border=1.2, shadow=PROP)
    flat(c, Thick(160, 66, 160, 30, 3), (200, 170, 80))
    # main hall (right back)
    piece(c, RRect(520, 160, 860, 300, 2), (220, 200, 170), border=1.5, shadow=PROP)
    piece(c, Poly([(490, 166), (890, 166), (840, 110), (540, 110)]), (60, 70, 80), border=1.5, shadow=PROP)
    for x in (560, 640, 720, 800):
        flat(c, RRect(x, 180, x + 40, 300, 2), (200, 60, 50))
    piece(c, RRect(640, 120, 740, 150, 3), (250, 210, 80), border=1, shadow=SMALL)
    # courtyard
    piece(c, RRect(-10, 300, 910, 612, 0), (200, 190, 170), shadow=LAYER)
    for y in range(320, H, 30):
        flat(c, Thick(0, y, W, y, 1.2), (186, 176, 156))
    # maples
    maple(c, 380, 330, s=1.6, col=(220, 70, 50))
    maple(c, 880, 360, s=1.4, col=(240, 150, 50) if "maple" not in d else (90, 160, 90))
    # stone lanterns + bell
    stone_lantern(c, 260, 460)
    stone_lantern(c, 560, 470, col=(170, 166, 160) if "lantern" not in d else (200, 160, 110))
    piece(c, [RRect(700, 340, 800, 352, 2), RRect(704, 352, 712, 460, 2), RRect(788, 352, 796, 460, 2)], (120, 80, 60), shadow=PROP)
    piece(c, [RRect(732, 360, 768, 410, 12), Ell(750, 410, 22, 6)], (120, 100, 70), border=1, shadow=SMALL)
    # monk sweeping + visitors + leaf piles
    modern(c, 440, 600, (240, 160, 60), bottom=(240, 160, 60), hair=(246, 214, 186), h=2.3)
    flat(c, [Thick(460, 530, 500, 600, 3), Poly([(492, 596), (520, 596), (512, 606), (488, 606)])], (170, 130, 80))
    modern(c, 140, 600, (90, 120, 160), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.3, bag=(200, 160, 100))
    modern(c, 700, 600, (220, 110, 150) if "visitor" not in d else (120, 200, 140), bottom=(60, 60, 80), hair=(90, 60, 40), h=2.2, style="long")
    rnd = random.Random(6132)
    for _ in range(40):
        x, y = rnd.uniform(0, 900), rnd.uniform(500, 600)
        flat(c, Ell(x, y, 5, 3), rnd.choice([(220, 80, 50), (240, 160, 50), (200, 60, 50)]))


L613_ELEMENTS = [
    E("leaf%d" % i, (lambda x: lambda c, m: flat(c, Ell(x, 160, 6, 3), (230, 100, 50)))(x),
      anim=dict(driftVelocity=(10, -24), driftLength=360, driftFade=True, spinSpeed=0.8, bobAmplitude=(10, 0), bobSpeed=0.5, phase=i / 3))
    for i, x in enumerate((340, 400, 860))
] + [
    E("broom", lambda c, m: flat(c, [Thick(460, 530, 500, 600, 3)], (170, 130, 80)), pivot=(460, 530), anim=dict(swingAngle=16, swingSpeed=0.8)),
    E("incense", lambda c, m: soft_union(c, [Circ(690, 310, 4)], (230, 230, 236), 0.7, spread=4), anim=dict(driftVelocity=(4, 20), driftLength=80, driftFade=True,
                                                                                                           driftGrow=2.0)),
    bird_el("crow", 500, 80, s=9, speed=-16, col=(40, 40, 50)),
]

L613_DIFFS = [
    ("eave", 160, 156, 0),
    ("maple", 880, 270, 0),
    ("lantern", 560, 410, 0),
    ("visitor", 701, 548, 0),
]


# =================================================================== Level 614 Santa's workshop
def gift(c, x, base, w, h, col, ribbon=(250, 220, 90)):
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 2), col, border=1.2, shadow=PROP)
    flat(c, [Thick(x, base - h, x, base, 4), Thick(x - w / 2, base - h / 2, x + w / 2, base - h / 2, 4)], ribbon)
    flat(c, [Circ(x - 6, base - h - 4, 6), Circ(x + 6, base - h - 4, 6)], ribbon)


def elf(c, x, base, col=(60, 150, 80), h=1.6):
    modern(c, x, base, col, bottom=(200, 50, 50), hair=(220, 180, 90), h=h)
    hx, hy = x + 1 * h, base - 46 * h
    flat(c, Poly([(hx - 9 * h, hy - 4 * h), (hx + 9 * h, hy - 4 * h), (hx + 16 * h, hy - 20 * h)]), col)
    flat(c, Circ(hx + 16 * h, hy - 20 * h, 3 * h), (250, 250, 250))


def l614_bg(c, d):
    room(c, (150, 90, 70), (140, 84, 66), (170, 120, 80), (154, 106, 70), floor_y=470)
    # log beams + window with snow outside
    for x in range(0, 900, 180):
        flat(c, RRect(x, 0, x + 20, 470, 0), (120, 70, 56))
    piece(c, RRect(360, 50, 540, 200, 4), (120, 70, 56), border=1.5, shadow=PROP)
    flat(c, RRect(370, 60, 530, 190, 3), (60, 70, 110))
    for k in range(12):
        flat(c, Circ(380 + (k * 37) % 140, 70 + (k * 23) % 110, 3), (250, 250, 255))
    flat(c, [Thick(450, 60, 450, 190, 4), Thick(370, 125, 530, 125, 4)], (120, 70, 56))
    # fireplace (left) with stockings
    piece(c, RRect(20, 220, 260, 470, 3), (170, 90, 70), border=1.5, shadow=PROP)
    flat(c, RRect(70, 320, 210, 470, 40), (40, 26, 26))
    piece(c, RRect(10, 210, 270, 230, 3), (120, 70, 56), shadow=SMALL)
    for k, x in enumerate((60, 140, 220)):
        npiece(c, [Poly([(x - 12, 230), (x + 12, 230), (x + 12, 270), (x + 22, 278), (x + 18, 292), (x - 12, 284)])],
               [(220, 50, 50), (60, 150, 80), (250, 250, 250)][k] if not (k == 1 and "stocking" in d) else (250, 200, 60), border=1, shadow=SMALL)
    # toy shelves (right)
    for r, y in enumerate((150, 250, 350)):
        wall_shelf(c, 600, 890, y, col=(120, 70, 56))
        for i in range(5):
            x = 630 + i * 56
            col = [(220, 60, 60), (60, 120, 210), (250, 200, 60), (120, 200, 120), (200, 120, 220)][(i + r) % 5]
            if r == 1 and i == 2 and "toy" in d:
                col = (250, 250, 250)
            if r == 0:
                npiece(c, [RRect(x - 16, y - 40, x + 16, y, 4), Circ(x, y - 48, 10)], col, border=1, shadow=SMALL)        # toy soldiers / dolls
            elif r == 1:
                npiece(c, [Circ(x, y - 18, 18)], col, border=1, shadow=SMALL)                                              # balls
                flat(c, Thick(x - 18, y - 18, x + 18, y - 18, 3), (250, 250, 250))
            else:
                npiece(c, [RRect(x - 22, y - 26, x + 22, y - 10, 4), Circ(x - 12, y - 6, 6), Circ(x + 12, y - 6, 6)], col, border=1, shadow=SMALL)   # toy cars
    # workbench with elves
    counter(c, 280, 580, 380, 470, (150, 100, 70))
    elf(c, 340, 380, h=1.4)
    elf(c, 520, 380, col=(200, 50, 50) if "elf" not in d else (90, 140, 220), h=1.4)
    gift(c, 430, 380, 50, 40, (60, 150, 80))
    # sleigh + sack of gifts (front)
    npiece(c, [Poly([(560, 560), (840, 560), (860, 520), (840, 500), (600, 500), (580, 520)])], (200, 40, 40))
    flat(c, [Thick(560, 580, 880, 580, 5), Thick(580, 560, 580, 580, 4), Thick(820, 560, 820, 580, 4)], (230, 190, 70))
    npiece(c, [Ell(690, 470, 70, 50)], (170, 120, 80) if "sack" not in d else (90, 140, 200))
    for k, (x, col) in enumerate(((60, (220, 60, 60)), (140, (60, 120, 210)), (220, (250, 200, 60)))):
        gift(c, x, 600, 60, 46 - k * 6, col)


L614_ELEMENTS = [
    E("fire", lambda c, m: (flat(c, Poly([(90, 470), (110, 420), (130, 446), (150, 400), (170, 446), (190, 424), (200, 470)]), (250, 140, 50)),
                            flat(c, Poly([(110, 470), (130, 440), (150, 456), (170, 436), (180, 470)]), (255, 220, 120))),
      pivot=(145, 470), daynight="untinted", anim=dict(stretch=(0.06, 0.2), scaleSpeed=3.0, twinkle=0.12, twinkleSpeed=2.5)),
    E("hammer", lambda c, m: flat(c, [Thick(352, 330, 372, 310, 3), RRect(366, 300, 382, 314, 2)], (150, 150, 160)), pivot=(352, 330), anim=dict(swingAngle=20, swingSpeed=1.6)),
    E("snow", lambda c, m: [flat(c, Circ(380 + k * 30, 60, 2.6), (250, 250, 255)) for k in range(6)], bbox=(360, 50, 540, 200),
      anim=dict(driftVelocity=(0, -20), driftLength=120, driftFade=True)),
    E("glow", lambda c, m: soft_union(c, [Ell(140, 440, 80, 40)], (255, 190, 100), 0.3, spread=30), daynight="untinted", anim=dict(pulse=0.08, scaleSpeed=1.0)),
]

L614_DIFFS = [
    ("stocking", 140, 262, 0),
    ("toy", 742, 232, 0),
    ("elf", 521, 330, 0),
    ("sack", 690, 470, 0),
]


# =================================================================== Level 615 harvest fair
def l615_bg(c, d):
    sky(c, (130, 190, 236), (240, 226, 200), 260)
    cloud_bg(c, 760, 60, 0.7)
    far_round_trees(c, 210, 34, (210, 140, 70), 6151)
    piece(c, RRect(-10, 240, 910, 612, 0), (170, 190, 100), shadow=LAYER)
    # bunting
    for x in range(0, 900, 36):
        flat(c, Poly([(x, 60), (x + 30, 60), (x + 15, 84)]), [(220, 70, 60), (250, 200, 60), (90, 150, 210)][(x // 36) % 3])
    flat(c, Thick(0, 60, W, 60, 2), (120, 100, 80))
    # barn backdrop
    piece(c, RRect(620, 120, 880, 300, 2), (190, 60, 50), border=1.5, shadow=PROP)
    piece(c, Poly([(600, 126), (900, 126), (750, 70)]), (90, 70, 70), border=1.5, shadow=PROP)
    flat(c, RRect(710, 200, 790, 300, 2), (250, 240, 220) if "door" not in d else (120, 170, 220))
    # pumpkin contest table with ribbons
    piece(c, [RRect(60, 380, 380, 394, 3), RRect(70, 394, 80, 460, 2), RRect(360, 394, 370, 460, 2)], (150, 110, 80), border=1.2, shadow=PROP)
    for k, (x, r) in enumerate(((120, 30), (220, 44), (320, 26))):
        piece(c, [Ell(x - r * 0.5, 380 - r, r * 0.6, r), Ell(x + r * 0.5, 380 - r, r * 0.6, r), Ell(x, 380 - r, r * 0.6, r)],
              (240, 130, 40) if not (k == 1 and "pumpkin" in d) else (240, 236, 210), border=1.2, shadow=PROP)
        flat(c, Thick(x, 380 - r * 2, x + 4, 380 - r * 2 - 10, 4), (100, 120, 60))
    piece(c, [Circ(220, 280, 14), Poly([(214, 290), (220, 290), (214, 310), (208, 306)]), Poly([(220, 290), (226, 290), (232, 306), (226, 310)])],
          (60, 110, 200) if "ribbon" not in d else (220, 60, 60), border=1, shadow=SMALL)
    # pie stand
    piece(c, [RRect(440, 330, 600, 420, 3), Poly([(430, 330), (610, 330), (590, 296), (450, 296)])], (250, 246, 236), border=1.5, shadow=PROP)
    flat(c, [Poly([(430 + j * 36, 330), (448 + j * 36, 330), (446 + j * 36, 296), (438 + j * 36, 296)]) for j in range(5)], (220, 70, 60))
    for k in range(3):
        piece(c, Ell(470 + k * 50, 324, 20, 6), (220, 170, 100) if not (k == 1 and "pie" in d) else (150, 90, 170), border=1, shadow=None)
    # hay bales + scarecrow kid + visitors
    for x, y in ((100, 560), (180, 580)):
        piece(c, RRect(x - 40, y - 40, x + 40, y, 4), (230, 200, 110), border=1.2, shadow=PROP)
        flat(c, [Thick(x - 40, y - 26, x + 40, y - 26, 2), Thick(x - 40, y - 12, x + 40, y - 12, 2)], (200, 170, 80))
    modern(c, 380, 600, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=2.3, style="long")
    modern(c, 600, 600, (120, 150, 200), bottom=(50, 50, 60), hair=(130, 130, 140), h=2.3, glasses=True)
    modern(c, 680, 600, (220, 110, 120) if "kid" not in d else (250, 220, 90), bottom=(60, 70, 110), hair=(40, 30, 30), h=1.5, style="twin")
    piece(c, [Ell(820, 590, 30, 10)], (150, 110, 70), shadow=SMALL)


L615_ELEMENTS = [
    E("tractor", lambda c, m: (piece(c, [RRect(0, 470, 70, 500, 4), RRect(40, 446, 70, 472, 3)], (60, 140, 80), border=1.2, shadow=PROP),
                               piece(c, [Circ(16, 504, 14), Circ(60, 508, 10)], (40, 40, 46), shadow=SMALL),
                               piece(c, RRect(-90, 474, -6, 500, 3), (230, 200, 110), border=1, shadow=SMALL),
                               piece(c, [Circ(-70, 506, 8), Circ(-26, 506, 8)], (40, 40, 46), shadow=SMALL)),
      anim=dict(drift_across(-90, 70, 30, start=400))),
    E("balloon", lambda c, m: (flat(c, Thick(692, 544, 700, 480, 1), (90, 90, 100)), piece(c, Ell(700, 466, 14, 17), (240, 90, 120), border=1, shadow=SMALL)),
      pivot=(692, 544), anim=dict(swingAngle=8, swingSpeed=0.5)),
    bird_el("goose", 400, 110, s=10, speed=-16),
]

L615_DIFFS = [
    ("pumpkin", 220, 336, 0),
    ("ribbon", 220, 290, 0),
    ("pie", 520, 324, 0),
    ("door", 750, 250, 0),
    ("kid", 681, 564, 0),
]


# =================================================================== Level 616 floating-lantern night
def water_lantern(c, x, y, col=(255, 210, 120), s=1.0):
    npiece(c, [Poly([(x - 14 * s, y), (x + 14 * s, y), (x + 10 * s, y - 16 * s), (x - 10 * s, y - 16 * s)])], col, border=0.8, shadow=None)
    flat(c, Ell(x, y + 2 * s, 16 * s, 4 * s), (60, 140, 90))


def l616_bg(c, d):
    c.gradient(0, 300, (16, 20, 50), (50, 40, 80))
    rnd = random.Random(6161)
    for _ in range(50):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 200), rnd.choice((1.2, 1.8))), (250, 246, 220))
    npiece(c, Circ(760, 80, 30), (250, 240, 200) if "moon" not in d else (250, 190, 140), shadow=None)
    # temple silhouettes + trees on the far bank
    for x, w, h in ((80, 120, 120), (300, 90, 80), (560, 140, 140)):
        flat(c, [RRect(x - w / 2, 300 - h, x + w / 2, 300, 2), Poly([(x - w / 2 - 20, 300 - h), (x + w / 2 + 20, 300 - h), (x, 300 - h - 50)])], (30, 30, 50))
        flat(c, Thick(x, 300 - h - 50, x, 300 - h - 80, 3), (30, 30, 50))
    flat(c, [Circ(x, 290, 28) for x in range(150, 900, 120)], (24, 26, 44))
    # river
    c.gradient(300, H, (30, 40, 80), (20, 30, 60))
    for k in range(20):
        x, y = rnd.uniform(0, 900), rnd.uniform(310, 600)
        flat(c, Thick(x, y, x + rnd.uniform(20, 60), y, 2), (60, 70, 120))
    # arched bridge (right)
    c.ellipse_ring(760, 380, 150, 80, 12, (80, 60, 70), ymax=380)
    npiece(c, RRect(590, 290, 930, 304, 3), (80, 60, 70))
    flat(c, [Thick(600 + k * 30, 290, 600 + k * 30, 270, 3) for k in range(11)] + [Thick(600, 270, 910, 270, 3)], (80, 60, 70))
    # lanterns on the water (static)
    for k, (x, y, s) in enumerate(((120, 400, 1.2), (260, 440, 1.0), (380, 520, 1.4), (520, 470, 1.1), (680, 560, 1.6), (820, 480, 1.0))):
        col = (255, 210, 120) if not (k == 2 and "lantern" in d) else (255, 140, 200)
        water_lantern(c, x, y, col=col, s=s)
    # people releasing lanterns from a small boat
    npiece(c, Poly([(40, 600), (220, 600), (200, 570), (60, 570)]), (120, 80, 60) if "boat" not in d else (60, 110, 160))
    modern(c, 110, 580, (250, 200, 80), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.6, style="long")
    modern(c, 170, 580, (200, 90, 120) if "shirt" not in d else (90, 170, 220), bottom=(40, 40, 50), hair=(90, 60, 40), h=1.6)


L616_ELEMENTS = [
    E("float%d" % i, (lambda x, y, s: lambda c, m: (water_lantern(c, x, y, s=s), soft_union(c, [Circ(x, y - 8 * s, 10 * s)], (255, 200, 120), 0.5, spread=24 * s)))(x, y, s),
      daynight="untinted", pivot=(x, y), anim=dict(bobAmplitude=(30, 3), bobSpeed=0.08, phase=i / 4)) for i, (x, y, s) in enumerate(((200, 360, 0.9), (460, 400, 1.0),
                                                                                                                                  (620, 380, 0.8), (300, 580, 1.2)))
] + [
    E("glows", lambda c, m: [soft_union(c, [Circ(x, y - 8 * s, 10 * s)], (255, 200, 120), 0.45, spread=24 * s) for x, y, s in
                             ((120, 400, 1.2), (260, 440, 1.0), (380, 520, 1.4), (520, 470, 1.1), (680, 560, 1.6), (820, 480, 1.0))], daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.8)),
    E("sky", lambda c, m: (npiece(c, [Poly([(0, 200), (16, 200), (14, 176), (2, 176)])], (255, 210, 120), border=0.8, shadow=None),
                           soft_union(c, [Circ(8, 190, 8)], (255, 200, 120), 0.5, spread=20)), daynight="untinted",
      anim=dict(driftVelocity=(10, 20), driftStart=300, driftLength=200, driftFade=True)),
]

L616_DIFFS = [
    ("lantern", 380, 508, 0),
    ("boat", 130, 585, 0),
    ("moon", 760, 80, 0),
    ("shirt", 171, 548, 0),
]


# =================================================================== Level 617 high-speed train depot
def bullet_train(c, x0, x1, base, body=(246, 248, 252), stripe=(60, 110, 200), nose_right=True, screen=(60, 80, 110)):
    pts = [(x0, base - 10), (x0, base - 80), (x1 - 120, base - 80), (x1 - 40, base - 60), (x1, base - 20), (x1, base - 10)] if nose_right else \
        [(x1, base - 10), (x1, base - 80), (x0 + 120, base - 80), (x0 + 40, base - 60), (x0, base - 20), (x0, base - 10)]
    piece(c, Poly(pts), body, border=1.5, shadow=PROP)
    if not nose_right:
        flat(c, Poly([(x0 + 116, base - 74), (x0 + 50, base - 58), (x0 + 40, base - 46), (x0 + 120, base - 46)]), screen)
    flat(c, RRect(x0 + 4, base - 40, x1 - 20, base - 32, 1), stripe)
    for x in range(int(x0) + 30, int(x1) - 150, 50):
        flat(c, RRect(x, base - 68, x + 34, base - 52, 4), (60, 80, 110))


def l617_bg(c, d):
    room(c, (180, 186, 196), (172, 178, 190), (110, 112, 120), (100, 102, 110), floor_y=470)
    # roof trusses + skylights
    for x in range(0, 900, 150):
        flat(c, Poly([(x + 20, 0), (x + 130, 0), (x + 120, 40), (x + 30, 40)]), (200, 220, 240))
    flat(c, Thick(0, 44, W, 44, 6), (130, 134, 146))
    for x in range(0, 900, 40):
        flat(c, [Thick(x, 50, x + 40, 90, 2), Thick(x + 40, 50, x, 90, 2)], (150, 154, 166))
    flat(c, Thick(0, 92, W, 92, 5), (130, 134, 146))
    # inspection gantries
    for k, x in enumerate((260, 640)):
        flat(c, [Thick(x - 120, 470, x - 120, 160, 5), Thick(x + 120, 470, x + 120, 160, 5)], (250, 200, 60))
        flat(c, RRect(x - 124, 152, x + 124, 172, 3), (250, 200, 60) if not (k == 1 and "gantry" in d) else (90, 160, 220))
    # two trains on pits
    bullet_train(c, -40, 520, 330, stripe=(60, 110, 200))
    bullet_train(c, 380, 940, 460, stripe=(220, 70, 70), nose_right=False, screen=(60, 80, 110) if "stripe" not in d else (250, 190, 60))
    flat(c, RRect(-10, 336, 910, 344, 0), (60, 60, 70))
    # workers in hi-vis + tool cart + sign
    for k, (x, b) in enumerate(((200, 600), (520, 600), (760, 600))):
        modern(c, x, b, (60, 90, 150), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.2)
        flat(c, RRect(x - 17, b - 84, x + 17, b - 44, 3), (250, 160, 40) if not (k == 1 and "vest" in d) else (120, 220, 90))
        piece(c, [Ell(x + 2, b - 112, 18, 12)], (250, 250, 250), shadow=SMALL)
    piece(c, [RRect(320, 540, 420, 590, 4)], (220, 70, 60) if "cart" not in d else (60, 120, 200), border=1.5, shadow=PROP)
    piece(c, [Circ(336, 596, 8), Circ(404, 596, 8)], (40, 40, 46), shadow=SMALL)
    piece(c, RRect(820, 110, 890, 150, 3), (60, 140, 90), border=1.2, shadow=SMALL)
    sign_box(c, 830, 118, 880, 142, (250, 250, 250), 6171, vertical=False)


L617_ELEMENTS = [
    E("lamp%d" % i, (lambda x: lambda c, m: (flat(c, Thick(x, 92, x, 120, 1.4), (90, 90, 100)), piece(c, Poly([(x - 20, 136), (x + 20, 136), (x + 12, 120), (x - 12, 120)]),
                                                                                                     (60, 60, 70), shadow=SMALL),
                                            soft_union(c, [Ell(x, 140, 14, 5)], (255, 240, 200), 0.6, spread=14)))(x), pivot=(x, 92), daynight="untinted",
      anim=dict(swingAngle=2, swingSpeed=0.3, phase=i / 3)) for i, x in enumerate((140, 450, 760))
] + [
    E("spark", lambda c, m: [flat(c, Thick(600, 400, 600 + 12 * math.cos(a), 400 - 12 * math.sin(a), 1.6), (255, 220, 120)) for a in (0.3, 1.0, 1.8, 2.6)],
      daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=3.0)),
    E("beacon", lambda c, m: soft_union(c, [Circ(260, 156, 5)], (255, 160, 60), 0.9, spread=12), daynight="untinted", anim=dict(twinkle=0.9, twinkleSpeed=1.2)),
]

L617_DIFFS = [
    ("gantry", 640, 162, 0),
    ("stripe", 465, 400, 0),
    ("vest", 521, 536, 0),
    ("cart", 370, 565, 0),
]


# =================================================================== Level 618 planetarium
def l618_bg(c, d):
    c.rect(0, 0, W, H, (14, 16, 36))
    # dome edge
    c.ellipse_ring(450, 470, 520, 470, 10, (40, 44, 70), ymax=470)
    rnd = random.Random(6181)
    for _ in range(140):
        flat(c, Circ(rnd.uniform(0, W), rnd.uniform(0, 420), rnd.choice((1.0, 1.4, 2.0))), (250, 246, 220))
    # milky way band
    soft_union(c, [Poly([(0, 300), (300, 140), (900, 40), (900, 120), (300, 220), (0, 380)])], (140, 120, 200), 0.18, spread=30)
    # projected planets
    for k, (x, y, r, col) in enumerate(((160, 120, 40, (230, 160, 90)), (430, 200, 26, (90, 150, 230)), (700, 110, 50, (230, 200, 140)))):
        if k == 1 and "planet" in d:
            col = (220, 90, 90)
        if k == 0 and "mars" in d:
            col = (150, 200, 120)
        piece(c, Circ(x, y, r), col, border=1, border_col=(60, 60, 90), shadow=None)
        flat(c, Ell(x - r * 0.3, y - r * 0.3, r * 0.35, r * 0.2), lit(col, 1.2))
    c.ellipse_ring(700, 110, 80, 18, 4, (220, 200, 150) if "ring" not in d else (120, 220, 230))
    # constellation lines
    pts = [(560, 280), (600, 250), (650, 270), (690, 240), (740, 260)]
    flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.2) for i in range(len(pts) - 1)], (150, 180, 240))
    flat(c, [Circ(x, y, 3) for x, y in pts], (255, 250, 220))
    # rows of reclined seats with heads
    for r, (y, s) in enumerate(((470, 1.0), (530, 1.2), (590, 1.4))):
        for k in range(8):
            x = 60 + k * 112 + (r % 2) * 50
            hit = (r == 1 and k == 5 and "seat" in d) or (r == 2 and k == 1 and "seat2" in d)
            npiece(c, [RRect(x - 40 * s, y - 30 * s, x + 40 * s, y + 10 * s, 10 * s)], (90, 40, 60) if not hit else (60, 110, 160), border=1, shadow=SMALL)
            flat(c, Circ(x, y - 34 * s, 10 * s), [(40, 30, 30), (90, 60, 40), (220, 180, 90)][(k + r) % 3])
    # projector in the middle
    npiece(c, [RRect(430, 400, 470, 470, 4), Circ(450, 390, 30)], (60, 60, 80))
    flat(c, [Circ(426, 384, 8), Circ(474, 384, 8)], (150, 200, 240))


L618_ELEMENTS = [
    E("comet", lambda c, m: (flat(c, Thick(0, 60, 60, 30, 3), (200, 230, 255, 0.7)), flat(c, Circ(62, 29, 4), (255, 255, 240))), daynight="untinted",
      anim=dict(driftVelocity=(120, 50), driftStart=0, driftLength=600, driftFade=True)),
    E("twinkle", lambda c, m: [flat(c, Poly(star_pts(x, y, 6, 2, points=4)), (255, 255, 230)) for x, y in ((90, 300), (330, 60), (520, 160), (860, 220))],
      daynight="untinted", anim=dict(twinkle=0.7, twinkleSpeed=0.8)),
    E("beam", lambda c, m: soft_union(c, [Poly([(440, 380), (460, 380), (720, 120), (680, 100)])], (200, 220, 255), 0.08, spread=20), daynight="untinted",
      anim=dict(swingAngle=4, swingSpeed=0.1)),
]

L618_DIFFS = [
    ("planet", 430, 200, 0),
    ("ring", 700, 110, 0),
    ("seat", 670, 524, 0),
    ("mars", 160, 120, 0),
    ("seat2", 172, 584, 0),
]


# =================================================================== Level 619 seaside amusement pier (day / night)
DN619 = day_night(40.0, tint=(0.26, 0.28, 0.52))


def l619_bg(c, d):
    sky(c, (120, 186, 236), (240, 226, 210), 300)
    cloud_bank(c, 110, (250, 250, 246), 6191, k=0.6)
    sea(c, 280, seed=6192, n=14)
    # pier deck on stilts
    piece(c, RRect(-10, 400, 910, 420, 0), (170, 120, 80), border=1.5, shadow=PROP)
    for x in range(10, 900, 60):
        flat(c, RRect(x, 420, x + 10, 612, 1), (130, 90, 60))
    flat(c, [Thick(-10, 380, 910, 380, 3)] + [Thick(x, 380, x, 400, 2) for x in range(0, 900, 30)], (250, 250, 250))
    # big wheel structure (left)
    flat(c, [Thick(180, 400, 140, 160, 6), Thick(180, 400, 220, 160, 6)], (230, 230, 240))
    c.ellipse_ring(180, 170, 130, 130, 5, (240, 240, 246))
    # carousel (centre)
    piece(c, Poly([(380, 260), (560, 260), (470, 190)]), (220, 60, 60) if "canopy" not in d else (60, 120, 210), border=1.5, shadow=PROP)
    for k in range(5):
        flat(c, Poly([(380 + k * 36, 260), (398 + k * 36, 260), (470, 194)]), (250, 250, 250))
    piece(c, RRect(386, 260, 554, 276, 3), (250, 200, 60), shadow=SMALL)
    flat(c, Thick(470, 276, 470, 380, 5), (230, 190, 70))
    piece(c, Ell(470, 384, 96, 14), (200, 60, 60), border=1.2, shadow=PROP)
    # snack stand (right) + sign
    piece(c, [RRect(680, 300, 860, 380, 3), Poly([(670, 300), (870, 300), (850, 266), (690, 266)])], (250, 246, 236), border=1.5, shadow=PROP)
    flat(c, [Poly([(670 + j * 40, 300), (690 + j * 40, 300), (688 + j * 36, 266), (680 + j * 36, 266)]) for j in range(5)], (60, 140, 200))
    piece(c, RRect(700, 316, 840, 344, 3), (250, 200, 60) if "sign" not in d else (220, 90, 160), border=1, shadow=SMALL)
    sign_box(c, 712, 322, 828, 338, (200, 60, 60), 6193, vertical=False)
    # people on the pier
    modern(c, 300, 400, (240, 200, 90), bottom=(60, 70, 110), hair=(90, 60, 40), h=1.6, style="long")
    modern(c, 620, 400, (90, 150, 220) if "shirt" not in d else (250, 120, 90), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.7)
    modern(c, 900, 400, (200, 110, 150), bottom=(60, 60, 80), hair=(220, 180, 90), h=1.6, style="twin")
    # lifebuoy on the rail
    c.ellipse_ring(560, 360, 14, 14, 7, (250, 120, 40) if "buoy" not in d else (90, 200, 220))


def wheel(c, m):
    flat(c, [Thick(180 - 126 * math.cos(a), 170 - 126 * math.sin(a), 180 + 126 * math.cos(a), 170 + 126 * math.sin(a), 2) for a in [k * math.pi / 6 for k in range(6)]],
         (240, 240, 246))
    for k in range(12):
        a = k * math.pi / 6
        piece(c, RRect(180 + 126 * math.cos(a) - 10, 170 + 126 * math.sin(a) - 6, 180 + 126 * math.cos(a) + 10, 170 + 126 * math.sin(a) + 10, 3),
              [(240, 90, 90), (90, 160, 230), (250, 200, 60)][k % 3], border=1, shadow=SMALL)


def horses(c, m):
    for k, (x, col) in enumerate(((420, (250, 250, 250)), (470, (250, 200, 60)), (520, (240, 160, 190)))):
        flat(c, Thick(x, 276, x, 340, 2), (230, 190, 70))
        piece(c, [Ell(x, 344, 18, 10), Circ(x + 14, 334, 7), RRect(x - 12, 350, x - 8, 368, 1), RRect(x + 8, 350, x + 12, 368, 1)], col, border=1, shadow=SMALL)


L619_ELEMENTS = [
    E("wheel", wheel, pivot=(180, 170), anim=dict(rotateSpeed=10)),
    E("horses", horses, pivot=(470, 340), anim=dict(bobAmplitude=(0, 8), bobSpeed=0.6, stretch=(0.2, 0), scaleSpeed=0.4)),
    E("bulbs", lambda c, m: [flat(c, Circ(x, 262, 4), (255, 230, 140)) for x in range(390, 560, 16)] + [flat(c, Circ(180 + 130 * math.cos(a), 170 + 130 * math.sin(a), 3.4),
                                                                                                             (255, 230, 140)) for a in [k * math.pi / 12 for k in range(24)]],
      daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=1.4)),
    E("glow", lambda c, m: soft_union(c, [Ell(470, 300, 120, 70), Circ(180, 170, 140)], (255, 220, 150), 0.18, spread=30), daynight="night"),
    window_glow("stand", [(690, 350, 850, 376)]),
    bird_el("gull", 600, 120, s=9, speed=-20, daynight="day"),
]

L619_DIFFS = [
    ("canopy", 470, 230, 0),
    ("sign", 770, 330, 0),
    ("shirt", 621, 352, 0),
    ("buoy", 560, 360, 0),
]


LEVELS = [
    ("Level610", "灯光节", l610_bg, L610_ELEMENTS, L610_DIFFS, 60, OPTS),
    ("Level611", "舞狮", l611_bg, L611_ELEMENTS, L611_DIFFS, 60, OPTS),
    ("Level612", "庙会", l612_bg, L612_ELEMENTS, L612_DIFFS, 60, OPTS),
    ("Level613", "秋日古寺", l613_bg, L613_ELEMENTS, L613_DIFFS, 60, OPTS),
    ("Level614", "圣诞老人工坊", l614_bg, L614_ELEMENTS, L614_DIFFS, 60, OPTS),
    ("Level615", "丰收市集", l615_bg, L615_ELEMENTS, L615_DIFFS, 60, OPTS),
    ("Level616", "水灯节", l616_bg, L616_ELEMENTS, L616_DIFFS, 60, OPTS),
    ("Level617", "动车检修库", l617_bg, L617_ELEMENTS, L617_DIFFS, 60, OPTS),
    ("Level618", "天文馆", l618_bg, L618_ELEMENTS, L618_DIFFS, 60, OPTS),
    ("Level619", "海边游乐码头", l619_bg, L619_ELEMENTS, L619_DIFFS, 60, dict(OPTS, day_night=DN619, anim_seconds=40.0, frames=80)),
]
