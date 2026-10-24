# -*- coding: utf-8 -*-
"""Mixed themes part 2 (paper-craft side views, full-bleed, original designs, no brands):
  Level245 非洲草原 - a savanna watering hole: acacias, giraffes, elephants, zebras, lions, safari jeep
  Level246 建筑工地 - a construction site: tower crane, steel frame, excavator, mixer, dump truck, workers
  Level247 火车站月台 - a train platform: canopy with clock, departure board, commuter train, benches
  Level248 集装箱码头 - a container port: gantry cranes, cargo ship, container stacks, trucks, tug boat
  Level249 植物温室 - inside a glasshouse: hanging baskets, potting shelves, cacti, orchids, gardener
  Level250 昆虫花园 - an insect's-eye garden: giant grass and flowers, ladybird, snail, ants, caterpillar
  Level251 玩具房   - a toy room: shelves of toys, block tower, teddy, rocking horse, train set, robot
  Level252 马戏团   - under the big top: striped canopy, ring, ringmaster, juggler, seal, clown car
  Level253 海盗船甲板 - a pirate ship deck: masts and sails, crow's nest, captain, parrot, cannon, wheel
  Level254 沙漠集市 - a desert bazaar: domed town, hanging carpets, lamps, spice piles, pots, camel
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, layer, palm, rock, sky, smoke_el, tree_round
from fills import far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_daily import elephant, giraffe, lion
from levels_festival import bunting, crowd_row
from levels_mix1 import big_leaf, camel, lantern
from levels_misc import seg_text
from levels_sports import stands

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)


def hard_hat(c, hx, hy, h, col):
    piece(c, [Ell(hx, hy - 4 * h, 9 * h, 6 * h), RRect(hx - 11 * h, hy - 4 * h, hx + 11 * h, hy - 2 * h, 1)], col, border=0.8, shadow=None)


def wheel(c, x, y, r, tyre=(40, 40, 46), hub=(170, 170, 180)):
    piece(c, Circ(x, y, r), tyre, shadow=SMALL)
    flat(c, Circ(x, y, r * 0.45), hub)


def container(c, x0, y0, w, h, col):
    piece(c, RRect(x0, y0, x0 + w, y0 + h, 1), col, border=1, shadow=SMALL)
    for k in range(1, int(w // 8)):
        flat(c, Thick(x0 + k * 8, y0 + 3, x0 + k * 8, y0 + h - 3, 1), lit(col, 0.82))


# =================================================================== Level 245 savanna
def acacia(c, x, base, s, col=(110, 150, 70)):
    piece(c, [Thick(x, base, x, base - 60 * s, 6 * s), Thick(x, base - 50 * s, x - 30 * s, base - 80 * s, 4 * s), Thick(x, base - 54 * s, x + 30 * s, base - 84 * s, 4 * s)],
          (120, 90, 60), shadow=PROP)
    piece(c, [Ell(x, base - 90 * s, 70 * s, 14 * s), Ell(x - 30 * s, base - 84 * s, 40 * s, 10 * s), Ell(x + 34 * s, base - 88 * s, 40 * s, 10 * s)], col, shadow=PROP)


def zebra(c, x, base, s, stripes=(40, 40, 46), face=1):
    for lx in (-18, -8, 12, 22):
        flat(c, RRect(x + lx * s * face - 3 * s, base - 30 * s, x + lx * s * face + 3 * s, base, 1), (240, 240, 236))
    piece(c, [Ell(x, base - 36 * s, 28 * s, 13 * s), Poly([(x + 18 * s * face, base - 42 * s), (x + 30 * s * face, base - 64 * s), (x + 40 * s * face, base - 60 * s),
                                                          (x + 30 * s * face, base - 34 * s)]), Ell(x + 40 * s * face, base - 62 * s, 10 * s, 6 * s)],
          (246, 246, 240), border=1.5, shadow=PROP)
    for k in range(6):
        flat(c, Thick(x - 20 * s + k * 8 * s, base - 46 * s, x - 22 * s + k * 8 * s, base - 28 * s, 2.4 * s), stripes)
    flat(c, [Thick(x + 24 * s * face, base - 50 * s, x + 32 * s * face, base - 54 * s, 2 * s), Thick(x + 22 * s * face, base - 44 * s, x + 30 * s * face, base - 48 * s, 2 * s)],
         stripes)
    flat(c, Thick(x + 26 * s * face, base - 62 * s, x + 34 * s * face, base - 70 * s, 3 * s), stripes)
    flat(c, Circ(x + 42 * s * face, base - 64 * s, 1.4 * s), INK)


def jeep(c, x, base, s, col):
    piece(c, [RRect(x - 50 * s, base - 34 * s, x + 50 * s, base - 10 * s, 5), RRect(x - 30 * s, base - 56 * s, x + 20 * s, base - 34 * s, 3)], col, border=1.5, shadow=PROP)
    flat(c, [Thick(x - 30 * s, base - 56 * s, x - 30 * s, base - 34 * s, 3), Thick(x + 20 * s, base - 56 * s, x + 20 * s, base - 34 * s, 3)], (60, 60, 70))
    flat(c, RRect(x - 26 * s, base - 52 * s, x + 16 * s, base - 38 * s, 2), (180, 210, 230))
    piece(c, RRect(x - 58 * s, base - 34 * s, x - 48 * s, base - 14 * s, 3), (60, 60, 70), shadow=SMALL)
    for wx in (x - 30 * s, x + 30 * s):
        wheel(c, wx, base - 8 * s, 12 * s)


def l245_bg(c, d):
    sky(c, (250, 190, 110), (250, 230, 180), 300)
    sun = (250, 120, 60) if "sun" not in d else (250, 200, 80)
    piece(c, Circ(120, 110, 46), sun, shadow=None)
    soft_union(c, [Circ(120, 110, 46)], (255, 210, 150), 0.4, spread=40)
    # mountain with snow cap
    piece(c, Poly([(600, 230), (760, 90), (820, 80), (930, 230)]), (170, 140, 140), shadow=LAYER)
    cap = (250, 250, 246) if "snow" not in d else (240, 200, 160)
    flat(c, Poly([(740, 108), (760, 90), (820, 80), (850, 108), (820, 116), (790, 104), (770, 118)]), cap)
    layer(c, 230, [(10, 0.01, 0.4), (6, 0.03, 1.2)], (210, 180, 110))
    acacia(c, 330, 250, 1.1)
    acacia(c, 520, 240, 0.7)
    # grass plain
    c.rect(0, 260, W, H, (220, 190, 110))
    rnd = random.Random(2451)
    for _ in range(120):
        x, y = rnd.uniform(0, W), rnd.uniform(270, 600)
        flat(c, [Thick(x, y, x - 3, y - 8, 1.4), Thick(x, y, x + 3, y - 9, 1.4)], (200, 168, 92))
    # watering hole
    flat(c, Ell(470, 400, 170, 34), (110, 160, 180))
    flat(c, Ell(470, 396, 140, 22), (140, 190, 206))
    # termite mound + flock of birds static
    piece(c, Poly([(820, 300), (836, 230), (850, 220), (866, 300)]), (180, 120, 80), shadow=PROP)
    for k, (x, y) in enumerate(((430, 80), (460, 70), (490, 86), (450, 100))):
        flat(c, [Thick(x - 8, y - 3, x, y, 2), Thick(x, y, x + 8, y - 3, 2)], (90, 70, 70) if "flock" not in d else (250, 250, 246))
    # giraffes (left middle)
    giraffe(c, 230, 380, 1.0, show_spots="spots" not in d)
    giraffe(c, 120, 370, 0.8)
    # elephants (right middle)
    elephant(c, 620, 380, 0.9, ear=(150, 140, 170) if "ear" not in d else (220, 150, 140))
    elephant(c, 740, 400, 0.6)
    # zebras drinking
    zebra(c, 420, 430, 1.1)
    zebra(c, 520, 440, 1.0, stripes=(40, 40, 46) if "zebra" not in d else (150, 90, 60), face=-1)
    # lion on a rock (right foreground)
    rock(c, 800, 560, 2.6, col=(170, 150, 130))
    lion(c, 780, 500, 1.3, mane=(170, 96, 40) if "mane" not in d else (90, 60, 50))
    # safari jeep (left foreground)
    jeep(c, 140, 560, 1.4, (200, 170, 100) if "jeep" not in d else (90, 140, 100))
    modern(c, 130, 500, (150, 140, 100), bottom=(120, 110, 80), hair=(90, 60, 40), h=1.1)
    # foreground grass tufts
    for x in range(0, W, 40):
        flat(c, [Thick(x, 600, x - 8, 570, 2), Thick(x + 6, 600, x + 10, 568, 2), Thick(x + 12, 600, x + 20, 574, 2)], (190, 160, 80))


L245_ELEMENTS = [
    bird_el("vulture", 300, 60, s=12, col=(80, 60, 60), speed=12),
    E("dust", lambda c, m: soft_union(c, [Ell(60, 552, 30, 12)], (230, 210, 170), 0.6, spread=10), pivot=(60, 552), daynight="untinted",
      anim=dict(driftVelocity=(-20, -6), driftLength=60, driftFade=True, driftGrow=1.5)),
    E("trunk", lambda c, m: flat(c, Thick(680, 340, 690, 372, 7), (160, 160, 176)), pivot=(680, 340), anim=dict(swingAngle=8, swingSpeed=0.5)),
    E("ripple", lambda c, m: c.ellipse_ring(470, 400, 40, 8, 1.6, (200, 230, 240)), pivot=(470, 400), daynight="untinted", anim=dict(pulse=0.4, scaleSpeed=0.6)),
]

L245_DIFFS = [
    ("sun", 120, 110, 0),
    ("flock", 460, 86, 0),
    ("snow", 795, 98, 0),
    ("spots", 260, 300, 0),
    ("ear", 652, 326, 0),
    ("zebra", 520, 404, 0),
    ("jeep", 140, 530, 0),
    ("mane", 824, 440, 0),
]


# =================================================================== Level 246 construction site
def l246_bg(c, d):
    sky(c, (130, 190, 240), (220, 236, 248), H)
    cloud_bg(c, 600, 60, 0.6)
    far_skyline(c, 260, 60, 150, (180, 196, 214), 2461)
    far_skyline(c, 410, 80, 170, (196, 208, 222), 2464)
    # building steel frame (right)
    frame = (200, 70, 60)
    for x in (560, 660, 760, 860):
        piece(c, RRect(x - 6, 120, x + 6, 470, 1), frame, shadow=SMALL)
    for k, y in enumerate((120, 210, 300, 390)):
        col = frame
        piece(c, RRect(550, y - 6, 870, y + 6, 1), col, shadow=SMALL)
    for y in (300, 390):
        flat(c, RRect(560, y + 6, 860, y + 30, 0), (190, 190, 196))
    for x in range(570, 860, 30):
        flat(c, Thick(x, 210, x + 30, 300, 1.4), (150, 150, 160))
    # scaffold + net
    for x in (540, 880):
        flat(c, Thick(x, 120, x, 470, 3), (150, 150, 160))
    flat(c, Thick(860, 114, 860, 70, 2), (90, 90, 100))
    piece(c, Poly([(862, 70), (900, 80), (862, 92)]), (60, 160, 90) if "beam" not in d else (240, 200, 60), shadow=SMALL)
    # tower crane (left)
    piece(c, [RRect(150, 60, 170, 470, 1)], (240, 200, 50), shadow=PROP)
    for y in range(70, 470, 20):
        flat(c, [Thick(150, y, 170, y + 20, 1.4), Thick(170, y, 150, y + 20, 1.4)], (200, 160, 30))
    piece(c, [Thick(60, 60, 600, 60, 8)], (240, 200, 50), shadow=PROP)
    for x in range(70, 600, 24):
        flat(c, [Thick(x, 56, x + 24, 64, 1.2)], (200, 160, 30))
    piece(c, RRect(60, 62, 110, 92, 2), (120, 120, 130) if "cab" not in d else (220, 90, 70), shadow=SMALL)
    cab = (250, 250, 246)
    piece(c, RRect(170, 64, 210, 100, 3), cab, border=1.2, shadow=SMALL)
    flat(c, RRect(176, 70, 204, 86, 2), (160, 200, 230))
    # ground
    c.rect(0, 470, W, H, (200, 170, 120))
    rnd = random.Random(2462)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(480, 600)
        flat(c, Circ(x, y, rnd.uniform(1.5, 3)), (180, 150, 104))
    # site fence with boards (back)
    for i, x in enumerate(range(-10, 540, 110)):
        piece(c, RRect(x, 400, x + 106, 470, 1), (60, 120, 90), border=1, shadow=SMALL)
        sign_box(c, x + 16, 418, x + 90, 450, (60, 120, 90), 2463 + i, vertical=False)
    # cement mixer (left middle)
    drum = (240, 140, 40) if "mixer" not in d else (90, 170, 120)
    piece(c, [RRect(220, 300, 330, 340, 4)], (220, 220, 226), border=1.5, shadow=PROP)
    piece(c, Poly([(230, 300), (330, 290), (310, 250), (250, 254)]), drum, border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, Thick(250 + k * 20, 256, 244 + k * 24, 298, 3), lit(drum, 0.8))
    for x in (240, 310):
        wheel(c, x, 346, 12)
    # workers on the frame
    for x, y, top in ((620, 300, (250, 150, 40)), (760, 210, (250, 150, 40))):
        hx, hy = modern(c, x, y, top if not (x == 620 and "hat" in d) else (90, 170, 220), bottom=(60, 70, 100), hair=(40, 30, 30), h=1.3)
        hard_hat(c, hx, hy, 1.3, (250, 220, 60))
    # excavator (bottom centre)
    exc = (250, 190, 40)
    piece(c, [RRect(380, 520, 520, 556, 6)], (60, 60, 70), shadow=PROP)
    for x in range(392, 520, 22):
        flat(c, Circ(x, 538, 8), (110, 110, 120))
    piece(c, [RRect(400, 470, 500, 520, 6), RRect(460, 440, 500, 480, 4)], exc, border=1.5, shadow=PROP)
    flat(c, RRect(466, 446, 494, 470, 2), (170, 210, 236))
    piece(c, [Thick(410, 480, 330, 430, 10), Thick(330, 430, 300, 490, 8)], exc, shadow=PROP)
    bucket = (90, 90, 100) if "bucket" not in d else (220, 70, 60)
    piece(c, Poly([(286, 486), (322, 486), (316, 516), (292, 520)]), bucket, border=1.2, shadow=SMALL)
    # dump truck (right foreground)
    truck = (220, 70, 60)
    piece(c, [Poly([(640, 500), (800, 500), (810, 470), (650, 476)]), RRect(640, 500, 820, 560, 4)], truck, border=1.5, shadow=PROP)
    piece(c, RRect(800, 490, 880, 560, 6), truck if "truck" not in d else (60, 130, 200), border=1.5, shadow=PROP)
    flat(c, RRect(820, 500, 870, 526, 2), (170, 210, 236))
    for x in (680, 760, 850):
        wheel(c, x, 566, 18)
    # cones + barrier (left foreground)
    for k, x in enumerate((40, 90, 140)):
        if k == 1 and "cone" in d:
            continue
        piece(c, [Poly([(x - 14, 590), (x + 14, 590), (x + 4, 540), (x - 4, 540)]), RRect(x - 18, 586, x + 18, 594, 1)], (250, 120, 40), shadow=SMALL)
        flat(c, Thick(x - 9, 566, x + 9, 566, 4), (250, 250, 246))
    # site office container
    piece(c, RRect(10, 470, 190, 530, 2), (240, 236, 226), border=1.5, shadow=PROP)
    flat(c, [RRect(30, 486, 70, 510, 2), RRect(120, 486, 160, 510, 2)], (170, 210, 236))


L246_ELEMENTS = [
    E("hook", lambda c, m: [flat(c, Thick(440, 64, 440, 170, 1.4), (60, 60, 70)), piece(c, RRect(400, 170, 480, 190, 2), (190, 190, 200), shadow=SMALL),
                            flat(c, [Thick(410, 170, 440, 150, 1.2), Thick(470, 170, 440, 150, 1.2)], (60, 60, 70))], pivot=(440, 64),
      anim=dict(swingAngle=3, swingSpeed=0.4, bobAmplitude=(30, 0), bobSpeed=0.08)),
    E("spark", lambda c, m: [flat(c, Poly(star_pts(700, 296, 10, 3, points=6)), (255, 230, 120))], pivot=(700, 296), daynight="untinted",
      anim=dict(blinkInterval=0.7, blinkDuration=0.3)),
    *smoke_el("dust", 300, 510, n=3, col=(220, 200, 170), r=10, rise=(-6, -14), length=40),
    bird_el("bird", 300, 140, s=8, speed=-16),
]

L246_DIFFS = [
    ("cab", 85, 77, 0),
    ("beam", 880, 81, 0),
    ("mixer", 280, 275, 0),
    ("hat", 621, 262, 0),
    ("bucket", 304, 502, 0),
    ("truck", 840, 525, 0),
    ("cone", 90, 568, 0),
]


# =================================================================== Level 247 train platform
def l247_bg(c, d):
    c.rect(0, 0, W, H, (200, 210, 220))
    # canopy roof
    piece(c, Poly([(-10, 0), (910, 0), (910, 70), (-10, 90)]), (90, 100, 120), shadow=PROP)
    for x in range(0, W, 60):
        flat(c, Thick(x, 0, x, 84 - x * 0.02, 3), (120, 130, 150))
    for x in (120, 450, 780):
        piece(c, RRect(x - 6, 80, x + 6, 470, 1), (110, 120, 140), shadow=SMALL)
    # hanging clock
    clock = (250, 250, 246) if "clock" not in d else (250, 220, 120)
    flat(c, Thick(120, 80, 120, 110, 2), (60, 60, 70))
    piece(c, Circ(120, 140, 30), (60, 60, 70), shadow=PROP)
    flat(c, Circ(120, 140, 24), clock)
    flat(c, [Thick(120, 140, 120, 122, 2.4), Thick(120, 140, 134, 146, 2.4)], (40, 40, 50))
    # departure board
    piece(c, RRect(300, 96, 600, 160, 4), (30, 34, 44), border=1.5, shadow=PROP)
    for r in range(3):
        col = (250, 200, 60) if not (r == 0 and "board" in d) else (90, 220, 120)
        flat(c, RRect(314, 106 + r * 18, 440, 118 + r * 18, 2), col)
        seg_text(c, 470, 104 + r * 18, 12, "%02d" % (10 + r * 7), (250, 250, 246), width=1.6)
        seg_text(c, 530, 104 + r * 18, 12, "%d" % (r + 3), (250, 140, 60), width=1.6)
    # roof lamp (right)
    lamp = (250, 240, 180) if "lamp" not in d else (240, 140, 60)
    flat(c, Thick(780, 84, 780, 100, 2), (60, 60, 70))
    piece(c, Poly([(756, 100), (804, 100), (794, 116), (766, 116)]), (60, 60, 70), shadow=SMALL)
    flat(c, Ell(780, 118, 14, 5), lamp)
    # train (side, across the middle)
    body = (230, 236, 240)
    piece(c, RRect(-20, 180, 920, 420, 16), body, border=2, shadow=PROP)
    flat(c, RRect(-20, 360, 920, 380, 0), (60, 130, 200))
    flat(c, RRect(-20, 386, 920, 394, 0), (240, 180, 40))
    for k, x in enumerate((30, 150, 470, 590, 710, 830)):
        flat(c, RRect(x, 210, x + 90, 290, 6), (60, 80, 100))
        soft_union(c, [RRect(x + 6, 216, x + 30, 284, 4)], (200, 230, 250), 0.3, spread=4)
    # passengers in windows
    for x, top in ((60, (220, 90, 80)), (500, (90, 140, 210)), (620, (240, 200, 80) if "passenger" not in d else (150, 100, 220)), (740, (120, 180, 120))):
        flat(c, Circ(x + 20, 248, 12), SKIN)
        flat(c, Ell(x + 18, 240, 13, 7), (40, 30, 30))
        flat(c, RRect(x + 4, 262, x + 36, 290, 6), top)
    # doors
    for x in (260, 380):
        door = (200, 210, 220) if not (x == 260 and "door" in d) else (240, 140, 60)
        piece(c, RRect(x, 200, x + 80, 400, 4), door, border=1.2, shadow=None)
        flat(c, RRect(x + 10, 214, x + 34, 300, 3), (60, 80, 100))
        flat(c, RRect(x + 46, 214, x + 70, 300, 3), (60, 80, 100))
    # platform
    c.rect(0, 420, W, H, (176, 170, 166))
    flat(c, RRect(0, 420, W, 440, 0), (240, 200, 60))
    for x in range(0, W, 14):
        flat(c, Circ(x + 7, 430, 2.4), (220, 180, 40))
    for x in range(0, W, 80):
        flat(c, Thick(x, 440, x - 30, 600, 1.2), (160, 154, 150))
    # bench
    bench = (90, 130, 200) if "bench" not in d else (220, 90, 80)
    piece(c, [RRect(20, 500, 200, 514, 3), RRect(20, 470, 200, 486, 3), RRect(30, 514, 38, 560, 1), RRect(182, 514, 190, 560, 1)], bench, shadow=PROP)
    modern(c, 80, 514, (200, 120, 160), bottom=(60, 70, 100), hair=(90, 60, 40), h=1.6, style="long")
    # passengers on the platform
    modern(c, 330, 560, (60, 70, 90), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0, bag=(150, 100, 60))
    modern(c, 560, 580, (240, 240, 236), bottom=(60, 70, 100), hair=(200, 150, 80), h=2.1)
    case = (220, 60, 60) if "case" not in d else (60, 160, 120)
    piece(c, [RRect(420, 520, 470, 580, 6), Thick(434, 520, 434, 494, 2), Thick(456, 520, 456, 494, 2), Thick(434, 494, 456, 494, 2)], case, border=1.2, shadow=SMALL)
    for x in (428, 462):
        flat(c, Circ(x, 582, 4), (40, 40, 46))
    # vending machine
    vend = (220, 60, 60) if "vend" not in d else (60, 130, 200)
    piece(c, RRect(740, 430, 840, 590, 4), vend, border=1.5, shadow=PROP)
    flat(c, RRect(752, 444, 828, 530, 3), (230, 240, 246))
    for r in range(3):
        for k in range(4):
            flat(c, RRect(758 + k * 18, 450 + r * 26, 770 + k * 18, 468 + r * 26, 2), [(240, 200, 60), (90, 180, 110), (90, 150, 220), (240, 120, 160)][(k + r) % 4])
    flat(c, RRect(756, 546, 824, 560, 2), (40, 40, 46))
    # pigeons
    for x in (630, 680):
        piece(c, [Ell(x, 590, 14, 8), Circ(x + 12, 580, 5)], (150, 150, 166), shadow=SMALL)


L247_ELEMENTS = [
    E("pigeon", lambda c, m: piece(c, [Ell(880, 410, 12, 7), Circ(890, 402, 5)], (150, 150, 166), shadow=SMALL), pivot=(880, 414), anim=dict(bobAmplitude=(0, 3), bobSpeed=1.6, bounce=True)),
    E("hand", lambda c, m: flat(c, Thick(120, 140, 112, 160, 1.6), (220, 40, 40)), pivot=(120, 140), anim=dict(rotateSpeed=60)),
    E("glow", lambda c, m: soft_union(c, [Ell(780, 130, 30, 14)], (255, 240, 180), 0.4, spread=16), daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.6)),
    E("paper", lambda c, m: piece(c, RRect(560, 520, 600, 548, 2), (250, 250, 246), shadow=SMALL), pivot=(580, 534), anim=dict(swingAngle=6, swingSpeed=0.8)),
]

L247_DIFFS = [
    ("clock", 120, 140, 0),
    ("board", 377, 112, 0),
    ("lamp", 780, 116, 0),
    ("door", 300, 300, 0),
    ("passenger", 640, 262, 0),
    ("bench", 110, 500, 0),
    ("case", 445, 540, 0),
    ("vend", 790, 510, 0),
]


# =================================================================== Level 248 container port
def l248_bg(c, d):
    sky(c, (140, 190, 236), (220, 232, 244), 300)
    cloud_bg(c, 300, 60, 0.6)
    far_skyline(c, 220, 40, 100, (184, 198, 214), 2481)
    # lighthouse on a breakwater (left)
    piece(c, RRect(-10, 210, 180, 226, 3), (160, 160, 170), shadow=SMALL)
    stripe = (220, 60, 60) if "light" not in d else (60, 120, 210)
    piece(c, Poly([(90, 210), (120, 210), (114, 100), (96, 100)]), (250, 250, 246), border=1.5, shadow=PROP)
    for y in (120, 160, 196):
        flat(c, Poly([(94, y), (116, y), (117, y + 14), (93, y + 14)]), stripe)
    piece(c, RRect(92, 86, 118, 100, 2), (60, 60, 70), shadow=SMALL)
    # sea
    c.rect(0, 226, W, 330, (70, 130, 180))
    for k in range(8):
        flat(c, Thick(40 + k * 110, 250 + (k % 3) * 20, 90 + k * 110, 250 + (k % 3) * 20, 1.6), (120, 170, 210))
    # cargo ship (right) with stacked containers
    piece(c, Poly([(380, 300), (910, 300), (910, 260), (360, 250)]), (40, 60, 90), border=1.5, shadow=PROP)
    flat(c, RRect(380, 286, 910, 294, 0), (200, 60, 60))
    rnd = random.Random(2482)
    cols = [(220, 80, 60), (60, 120, 200), (240, 180, 50), (90, 160, 110), (180, 90, 160), (240, 240, 236)]
    for r in range(3):
        for k in range(8):
            col = rnd.choice(cols)
            container(c, 420 + k * 52, 222 - r * 26, 50, 24, col)
    bridge = (250, 250, 246)
    piece(c, RRect(850, 150, 900, 250, 3), bridge, border=1.5, shadow=PROP)
    flat(c, RRect(856, 160, 894, 176, 2), (60, 80, 110) if "bridge" not in d else (240, 200, 60))
    # gantry cranes
    for k, x in enumerate((420, 640)):
        col = (60, 130, 200) if not (k == 0 and "crane" in d) else (240, 140, 40)
        piece(c, [RRect(x - 50, 120, x - 40, 330, 1), RRect(x + 40, 120, x + 50, 330, 1), Thick(x - 120, 120, x + 140, 120, 10)], col, shadow=PROP)
        piece(c, RRect(x - 10, 128, x + 30, 150, 2), (250, 250, 246), shadow=SMALL)
    # quay
    c.rect(0, 330, W, H, (170, 166, 160))
    flat(c, RRect(0, 330, W, 340, 0), (240, 200, 60))
    for x in range(0, W, 100):
        flat(c, Thick(x, 340, x - 40, 600, 1.2), (156, 152, 148))
    # container stacks on the quay
    for k, (x, col) in enumerate(((200, (220, 80, 60)), (252, (60, 120, 200)), (200, (240, 180, 50)), (252, (90, 160, 110)))):
        y = 380 if k < 2 else 354
        if k == 2 and "box1" in d:
            col = (240, 240, 236)
        container(c, x, y, 52, 26, col)
    for k, (x, col) in enumerate(((560, (60, 120, 200)), (612, (240, 240, 236)), (586, (220, 80, 60)))):
        y = 380 if k < 2 else 354
        if k == 2 and "box2" in d:
            col = (90, 160, 110)
        container(c, x, y, 52, 26, col)
    # truck with container (bottom left)
    cab = (250, 250, 246) if "truck" not in d else (240, 160, 40)
    piece(c, [RRect(20, 470, 80, 530, 6)], cab, border=1.5, shadow=PROP)
    flat(c, RRect(28, 478, 72, 500, 2), (170, 210, 236))
    piece(c, RRect(80, 516, 260, 526, 2), (60, 60, 70), shadow=SMALL)
    container(c, 86, 470, 168, 46, (220, 80, 60))
    for x in (50, 120, 230):
        wheel(c, x, 536, 13)
    # straddle carrier (centre bottom)
    sc = (240, 190, 50)
    piece(c, [RRect(380, 410, 392, 560, 1), RRect(500, 410, 512, 560, 1), RRect(374, 400, 518, 420, 3)], sc, shadow=PROP)
    piece(c, RRect(480, 380, 518, 404, 3), (250, 250, 246), shadow=SMALL)
    container(c, 396, 470, 100, 34, (60, 120, 200) if "carrier" not in d else (180, 90, 160))
    for x in (386, 506):
        wheel(c, x, 566, 10)
    # bollards + worker in vest (right)
    for x in (640, 700):
        piece(c, [RRect(x - 10, 560, x + 10, 590, 3), Ell(x, 558, 14, 5)], (60, 60, 70), shadow=SMALL)
    hx, hy = modern(c, 800, 590, (250, 150, 40) if "vest" not in d else (120, 220, 90), bottom=(60, 70, 100), hair=(40, 30, 30), h=2.0)
    hard_hat(c, hx, hy, 2.0, (250, 250, 246))


L248_ELEMENTS = [
    E("tug", lambda c, m: [piece(c, Poly([(120, 290), (220, 290), (210, 310), (130, 310)]), (220, 70, 60), border=1.2, shadow=SMALL),
                           piece(c, RRect(150, 270, 190, 290, 2), (250, 250, 246), shadow=None)], pivot=(170, 300), anim=dict(drift_across(120, 220, 10), bobAmplitude=(0, 2), bobSpeed=0.8)),
    bird_el("gull", 500, 60, s=9, speed=-18),
    bird_el("gull2", 300, 100, s=8, speed=16),
    E("hoist", lambda c, m: [flat(c, Thick(640, 124, 640, 220, 1.4), (60, 60, 70)), container(c, 616, 220, 50, 24, (240, 240, 236))], pivot=(640, 124),
      anim=dict(bobAmplitude=(0, 30), bobSpeed=0.12)),
]

L248_DIFFS = [
    ("light", 105, 150, 0),
    ("crane", 380, 120, 0),
    ("bridge", 875, 168, 0),
    ("box1", 226, 367, 0),
    ("box2", 612, 367, 0),
    ("truck", 50, 500, 0),
    ("carrier", 446, 487, 0),
    ("vest", 800, 540, 0),
]


# =================================================================== Level 249 glasshouse
def pot_plant(c, x, base, s, pot, leaf=(80, 150, 80), kind="bush", bloom=None):
    piece(c, Poly([(x - 14 * s, base - 22 * s), (x + 14 * s, base - 22 * s), (x + 10 * s, base), (x - 10 * s, base)]), pot, border=1.2, shadow=SMALL)
    if kind == "cactus":
        piece(c, [RRect(x - 6 * s, base - 56 * s, x + 6 * s, base - 20 * s, 6 * s), RRect(x - 16 * s, base - 46 * s, x - 8 * s, base - 30 * s, 4 * s),
                  RRect(x + 8 * s, base - 50 * s, x + 16 * s, base - 34 * s, 4 * s)], leaf, shadow=SMALL)
        if bloom:
            flat(c, Circ(x, base - 58 * s, 5 * s), bloom)
    elif kind == "orchid":
        flat(c, Thick(x, base - 22 * s, x + 4 * s, base - 60 * s, 1.6), (90, 120, 70))
        for k in range(3):
            fx, fy = x + 4 * s + k * 8 * s, base - 60 * s + k * 10 * s
            for a in range(5):
                r = math.radians(a * 72)
                piece(c, Ell(fx + 6 * s * math.cos(r), fy + 6 * s * math.sin(r), 5 * s, 4 * s), bloom or (240, 140, 200), shadow=None)
        piece(c, [Ell(x - 10 * s, base - 26 * s, 14 * s, 5 * s), Ell(x + 10 * s, base - 28 * s, 14 * s, 5 * s)], leaf, shadow=None)
    else:
        piece(c, [Circ(x, base - 34 * s, 14 * s), Circ(x - 10 * s, base - 26 * s, 10 * s), Circ(x + 10 * s, base - 28 * s, 10 * s)], leaf, shadow=SMALL)
        if bloom:
            flat(c, [Circ(x - 6 * s, base - 38 * s, 3.4 * s), Circ(x + 6 * s, base - 32 * s, 3.4 * s), Circ(x, base - 26 * s, 3.4 * s)], bloom)


def hanging_basket(c, x, y, s, bloom):
    flat(c, [Thick(x, y - 50 * s, x - 18 * s, y, 1), Thick(x, y - 50 * s, x + 18 * s, y, 1)], (90, 80, 70))
    piece(c, Poly([(x - 22 * s, y), (x + 22 * s, y), (x + 14 * s, y + 18 * s), (x - 14 * s, y + 18 * s)]), (170, 120, 70), border=1, shadow=SMALL)
    piece(c, [Circ(x - 14 * s, y - 2 * s, 10 * s), Circ(x, y - 8 * s, 12 * s), Circ(x + 14 * s, y - 2 * s, 10 * s), Ell(x - 18 * s, y + 20 * s, 6 * s, 14 * s),
              Ell(x + 18 * s, y + 22 * s, 6 * s, 16 * s)], (80, 150, 80), shadow=SMALL)
    flat(c, [Circ(x - 12 * s, y - 6 * s, 4 * s), Circ(x + 4 * s, y - 12 * s, 4 * s), Circ(x + 14 * s, y - 2 * s, 4 * s), Circ(x - 18 * s, y + 24 * s, 3.4 * s),
             Circ(x + 18 * s, y + 30 * s, 3.4 * s)], bloom)


def l249_bg(c, d):
    sky(c, (190, 220, 240), (230, 240, 236), H)
    # glass panes + arched frame
    for x in range(0, W + 1, 75):
        flat(c, Thick(x, 0, x, 470, 3), (240, 240, 236))
    for y in (90, 190, 290, 390):
        flat(c, Thick(0, y, W, y, 3), (240, 240, 236))
    for k in range(5):
        flat(c, Thick(0, 30 - k * 4 + 0, W, 30 - k * 4, 2), (240, 240, 236))
    # outside garden blurred through the glass
    soft_union(c, [Ell(160, 420, 160, 60), Ell(700, 430, 200, 60)], (150, 190, 140), 0.5, spread=30)
    # roof vent (top centre)
    vent = (190, 220, 240) if "vent" not in d else (240, 220, 150)
    piece(c, RRect(390, 40, 510, 90, 2), vent, border=2, border_col=(240, 240, 236), shadow=SMALL)
    # hanging baskets
    hanging_basket(c, 120, 140, 1.4, (240, 90, 120) if "basket1" not in d else (250, 200, 60))
    hanging_basket(c, 790, 140, 1.4, (150, 110, 230) if "basket2" not in d else (250, 140, 60))
    # big potted palm (centre back)
    for a, l in ((-150, 120), (-120, 140), (-60, 140), (-30, 120), (-90, 130)):
        big_leaf(c, 450, 300, a, l, (70, 150, 80))
    piece(c, Poly([(410, 300), (490, 300), (480, 360), (420, 360)]), (200, 120, 80), border=1.5, shadow=PROP)
    # floor + benches
    c.rect(0, 470, W, H, (170, 150, 130))
    for x in range(0, W, 50):
        flat(c, RRect(x + 2, 470, x + 48, 600, 2), (180, 160, 140))
    for x0, x1 in ((20, 380), (520, 880)):
        piece(c, [RRect(x0, 360, x1, 376, 2), RRect(x0 + 10, 376, x0 + 20, 470, 1), RRect(x1 - 20, 376, x1 - 10, 470, 1), RRect(x0, 430, x1, 440, 2)],
              (150, 110, 80), shadow=PROP)
    # left bench: cacti
    for k, x in enumerate((60, 130, 200, 270, 340)):
        pot = (220, 130, 90) if not (k == 3 and "cactus" in d) else (90, 150, 210)
        pot_plant(c, x, 360, 1.0, pot, leaf=(90, 160, 100), kind="cactus", bloom=(240, 90, 140) if k % 2 else None)
    # right bench: orchids
    for k, x in enumerate((560, 640, 720, 800)):
        pot_plant(c, x, 360, 1.1, (240, 240, 236), kind="orchid", bloom=[(240, 140, 200), (250, 250, 246), (200, 140, 230), (250, 200, 120)][k]
                  if not (k == 1 and "orchid" in d) else (240, 100, 80))
    # seedling trays under the benches
    for x0 in (40, 560):
        piece(c, RRect(x0, 410, x0 + 140, 430, 2), (60, 60, 70), shadow=SMALL)
        for k in range(7):
            flat(c, [Thick(x0 + 10 + k * 18, 412, x0 + 6 + k * 18, 402, 1.6), Thick(x0 + 10 + k * 18, 412, x0 + 14 + k * 18, 402, 1.6)], (110, 180, 90))
    # watering can (left foreground)
    can = (90, 160, 120) if "can" not in d else (240, 150, 60)
    piece(c, [RRect(60, 520, 140, 580, 8), Thick(140, 540, 184, 510, 6), Thick(70, 520, 110, 500, 4)], can, border=1.5, shadow=PROP)
    piece(c, Ell(186, 508, 9, 6), lit(can, 0.8), shadow=None)
    # gardener (centre)
    hx, hy = modern(c, 450, 590, (240, 240, 236), bottom=(60, 70, 100), hair=(200, 150, 80), h=2.2, style="long")
    apron = (90, 140, 90) if "apron" not in d else (200, 80, 80)
    piece(c, Poly([(436, 524), (468, 524), (472, 566), (432, 566)]), apron, border=1, shadow=None)
    # seed packet crate (right foreground)
    if "seeds" not in d:
        piece(c, RRect(740, 540, 850, 590, 3), (190, 150, 100), border=1.5, shadow=PROP)
        for k in range(4):
            piece(c, RRect(752 + k * 24, 516, 772 + k * 24, 548, 2), [(240, 90, 120), (250, 200, 60), (90, 160, 230), (120, 200, 120)][k], border=1, shadow=None)


L249_ELEMENTS = [
    E("mist", lambda c, m: soft_union(c, [Ell(700, 300, 120, 16)], (250, 252, 255), 0.35, spread=14), pivot=(700, 300), daynight="untinted",
      anim=dict(bobAmplitude=(20, 4), bobSpeed=0.2)),
    E("drip", lambda c, m: piece(c, Circ(186, 520, 4), (150, 200, 240), shadow=None), pivot=(186, 520), anim=dict(driftVelocity=(0, 40), driftLength=60, driftFade=True)),
    E("bee", lambda c, m: [piece(c, Ell(620, 220, 8, 6), (250, 210, 60), shadow=None), flat(c, Thick(620, 214, 620, 226, 2), (40, 30, 40))], pivot=(620, 220),
      anim=dict(orbitRadius=(50, 20), orbitSpeed=0.2)),
    E("swing", lambda c, m: hanging_basket(c, 450, 140, 0.9, (250, 250, 246)), pivot=(450, 95), anim=dict(swingAngle=3, swingSpeed=0.4)),
]

L249_DIFFS = [
    ("basket1", 120, 150, 0),
    ("vent", 450, 64, 0),
    ("basket2", 790, 150, 0),
    ("cactus", 270, 330, 0),
    ("orchid", 650, 310, 0),
    ("can", 110, 545, 0),
    ("apron", 452, 545, 0),
    ("seeds", 795, 548, 0),
]


# =================================================================== Level 250 insect's-eye garden
def ladybird(c, x, y, s, shell, spots=True):
    piece(c, [Ell(x, y, 22 * s, 18 * s)], shell, border=1.2, shadow=SMALL)
    flat(c, Thick(x, y - 18 * s, x, y + 18 * s, 1.6), INK)
    piece(c, Ell(x + 20 * s, y, 10 * s, 9 * s), (40, 40, 46), shadow=None)
    if spots:
        flat(c, [Circ(x - 10 * s, y - 6 * s, 3.4 * s), Circ(x + 8 * s, y + 6 * s, 3.4 * s), Circ(x - 6 * s, y + 9 * s, 3 * s), Circ(x + 9 * s, y - 8 * s, 3 * s)], INK)


def l250_bg(c, d):
    sky(c, (190, 226, 246), (236, 246, 236), H)
    soft_union(c, [Circ(760, 80, 80)], (255, 250, 220), 0.5, spread=60)
    # blurred far flowers
    for x, y, col in ((80, 220, (240, 180, 200)), (300, 240, (250, 230, 140)), (620, 220, (200, 180, 240)), (860, 260, (250, 200, 180))):
        soft_union(c, [Circ(x, y, 50)], col, 0.5, spread=30)
    # giant grass blades
    rnd = random.Random(2501)
    for k in range(26):
        x = rnd.uniform(-20, 920)
        h = rnd.uniform(200, 460)
        lean = rnd.uniform(-60, 60)
        col = rnd.choice([(110, 180, 90), (90, 160, 80), (130, 190, 100)])
        piece(c, Poly([(x - 10, 600), (x + 10, 600), (x + lean, 600 - h)]), col, shadow=SMALL)
    # big flower (centre top) on a stalk
    piece(c, Thick(450, 600, 440, 160, 10), (90, 160, 80), shadow=PROP)
    petal = (250, 200, 60) if "petal" not in d else (240, 120, 180)
    for a in range(8):
        r = math.radians(a * 45)
        piece(c, Ell(440 + 46 * math.cos(r), 120 + 34 * math.sin(r), 30, 18), petal, shadow=SMALL)
    piece(c, Circ(440, 120, 30), (200, 120, 50), shadow=SMALL)
    for k in range(10):
        flat(c, Circ(440 + 16 * math.cos(k), 120 + 12 * math.sin(k * 1.3), 3), (150, 80, 40))
    # dewdrop on a blade (left top)
    if "dew" not in d:
        piece(c, Ell(130, 150, 16, 20), (200, 236, 250, 0.85), shadow=SMALL)
        flat(c, Circ(124, 142, 5), (255, 255, 255))
    # butterfly resting (right top)
    wing = (90, 160, 240) if "wing" not in d else (240, 140, 60)
    piece(c, [Poly([(790, 150), (740, 100), (730, 150)]), Poly([(790, 150), (840, 100), (850, 150)]), Poly([(790, 154), (750, 190), (770, 160)]),
              Poly([(790, 154), (830, 190), (810, 160)])], wing, border=1.2, shadow=SMALL)
    flat(c, [Circ(752, 124, 7), Circ(828, 124, 7)], (250, 250, 246))
    flat(c, Thick(790, 130, 790, 176, 4), INK)
    # leaf platform with ladybird (middle left)
    big_leaf(c, 140, 380, -20, 240, (100, 170, 80))
    ladybird(c, 280, 320, 1.3, (220, 50, 50) if "ladybird" not in d else (250, 160, 40))
    # snail on a stone (middle right)
    rock(c, 640, 420, 2.4, col=(170, 160, 150))
    shell = (200, 140, 90) if "snail" not in d else (150, 120, 200)
    piece(c, [Ell(620, 352, 50, 14)], (220, 200, 170), border=1.2, shadow=SMALL)
    piece(c, Circ(620, 324, 30), shell, border=1.2, shadow=SMALL)
    for k in range(3):
        c.ellipse_ring(620 + k * 3, 324 + k * 2, 22 - k * 7, 22 - k * 7, 2.4, lit(shell, 0.8))
    flat(c, [Thick(664, 344, 674, 316, 2), Thick(670, 344, 684, 320, 2)], (220, 200, 170))
    flat(c, [Circ(674, 316, 3), Circ(684, 320, 3)], INK)
    # ground: soil + pebbles
    piece(c, hill_strip(500, [(10, 0.02, 0.4), (6, 0.05, 1.2)]), (150, 110, 80), shadow=LAYER)
    for _ in range(30):
        x, y = rnd.uniform(0, W), rnd.uniform(520, 600)
        flat(c, Ell(x, y, rnd.uniform(4, 10), rnd.uniform(3, 6)), (180, 150, 120))
    # mushroom (left bottom)
    mush = (220, 70, 60) if "mushroom" not in d else (120, 160, 220)
    piece(c, RRect(100, 500, 124, 580, 8), (246, 236, 216), shadow=PROP)
    piece(c, Poly([(112 + 60 * math.cos(math.pi * k / 12), 506 - 44 * math.sin(math.pi * k / 12)) for k in range(13)]), mush, shadow=PROP)
    flat(c, [Circ(90, 486, 6), Circ(124, 476, 7), Circ(150, 494, 5)], (250, 246, 236))
    # ants carrying a leaf (bottom centre)
    for k, x in enumerate((380, 430, 480)):
        piece(c, [Circ(x, 560, 6), Circ(x + 10, 558, 7), Circ(x + 22, 556, 6)], (60, 40, 40), shadow=SMALL)
        flat(c, [Thick(x + 8, 562, x + 2, 574, 1.4), Thick(x + 12, 562, x + 16, 574, 1.4)], (60, 40, 40))
    leaf = (120, 190, 90) if "leaf" not in d else (230, 150, 60)
    piece(c, Poly([(400, 548), (440, 520), (490, 530), (470, 552)]), leaf, shadow=SMALL)
    # caterpillar on a blade (bottom right)
    cat = (120, 200, 90) if "cat" not in d else (240, 150, 200)
    for k in range(6):
        piece(c, Circ(740 + k * 18, 520 - (k % 2) * 6, 12), cat, border=1, shadow=SMALL)
    piece(c, Circ(852, 506, 13), lit(cat, 0.9), border=1, shadow=SMALL)
    flat(c, [Circ(856, 502, 2.4)], INK)


L250_ELEMENTS = [
    E("bee", lambda c, m: [piece(c, Ell(560, 200, 14, 10), (250, 200, 60), shadow=SMALL), flat(c, [Thick(556, 191, 556, 209, 3), Thick(566, 192, 566, 208, 3)], (40, 30, 40)),
                           flat(c, [Ell(552, 186, 9, 6), Ell(566, 186, 9, 6)], (240, 250, 255))], pivot=(560, 200), anim=dict(orbitRadius=(60, 30), orbitSpeed=0.18)),
    E("antenna", lambda c, m: flat(c, [Thick(302, 312, 312, 296, 1.6), Thick(304, 324, 316, 312, 1.6)], INK), pivot=(302, 318), anim=dict(swingAngle=15, swingSpeed=1.2)),
    E("pollen", lambda c, m: [flat(c, Circ(x, y, 2.4), (255, 240, 160)) for x, y in ((520, 60), (380, 200), (700, 260), (200, 100))], daynight="untinted",
      anim=dict(driftVelocity=(10, -10), driftLength=50, driftFade=True)),
]

L250_DIFFS = [
    ("dew", 130, 150, 0),
    ("petal", 440, 120, 0),
    ("wing", 790, 146, 0),
    ("ladybird", 286, 320, 0),
    ("snail", 620, 328, 0),
    ("mushroom", 112, 490, 0),
    ("leaf", 445, 538, 0),
    ("cat", 796, 514, 0),
]


# =================================================================== Level 251 toy room
def teddy(c, x, base, s, fur, bow):
    piece(c, [Ell(x, base - 26 * s, 24 * s, 26 * s), Circ(x, base - 64 * s, 20 * s), Circ(x - 16 * s, base - 80 * s, 8 * s), Circ(x + 16 * s, base - 80 * s, 8 * s),
              Ell(x - 22 * s, base - 6 * s, 12 * s, 8 * s), Ell(x + 22 * s, base - 6 * s, 12 * s, 8 * s), Ell(x - 26 * s, base - 34 * s, 8 * s, 14 * s),
              Ell(x + 26 * s, base - 34 * s, 8 * s, 14 * s)], fur, border=1.5, shadow=PROP)
    flat(c, [Ell(x, base - 58 * s, 9 * s, 7 * s), Ell(x, base - 24 * s, 14 * s, 16 * s)], lit(fur, 1.2))
    flat(c, [Circ(x - 7 * s, base - 68 * s, 2.4 * s), Circ(x + 7 * s, base - 68 * s, 2.4 * s), Circ(x, base - 60 * s, 3 * s)], INK)
    piece(c, [Poly([(x, base - 46 * s), (x - 20 * s, base - 58 * s), (x - 20 * s, base - 34 * s)]), Poly([(x, base - 46 * s), (x + 20 * s, base - 58 * s), (x + 20 * s, base - 34 * s)])],
          bow, border=1, shadow=None)


def l251_bg(c, d):
    # wallpaper
    c.rect(0, 0, W, 430, (250, 236, 210))
    for x in range(0, W, 40):
        flat(c, RRect(x, 0, x + 20, 430, 0), (246, 228, 200))
    # window with curtains
    piece(c, RRect(360, 40, 540, 200, 3), (250, 250, 246), border=1.5, shadow=PROP)
    flat(c, RRect(372, 52, 528, 188, 2), (170, 214, 244))
    cloud_bg(c, 430, 110, 0.5)
    flat(c, [Thick(450, 52, 450, 188, 4), Thick(372, 120, 528, 120, 4)], (250, 250, 246))
    cur = (240, 140, 160) if "curtain" not in d else (120, 190, 230)
    for x0, x1 in ((330, 380), (520, 570)):
        piece(c, Poly([(x0, 30), (x1, 30), (x1 - 6, 220), (x0 + 6, 220)]), cur, border=1.2, shadow=SMALL)
    # kite pinned on the wall (left)
    kite = (240, 90, 90) if "kite" not in d else (90, 180, 120)
    piece(c, Poly([(100, 40), (138, 86), (100, 152), (62, 86)]), kite, border=1.5, shadow=PROP)
    flat(c, [Thick(100, 40, 100, 152, 2), Thick(62, 86, 138, 86, 2)], lit(kite, 0.7))
    for k in range(4):
        flat(c, Thick(100 + k * 6, 152 + k * 20, 106 + k * 6, 172 + k * 20, 2), (90, 90, 100))
    # shelf with toys (right)
    piece(c, RRect(640, 140, 880, 154, 2), (190, 140, 90), shadow=PROP)
    piece(c, RRect(640, 260, 880, 274, 2), (190, 140, 90), shadow=PROP)
    for k, (x, col) in enumerate(((680, (90, 150, 230)), (760, (240, 200, 60)), (840, (220, 80, 80)))):
        piece(c, [RRect(x - 18, 100, x + 18, 140, 4), Circ(x, 92, 12)], col, border=1.2, shadow=SMALL)
        flat(c, [Circ(x - 4, 90, 2), Circ(x + 4, 90, 2)], INK)
    duck = (250, 210, 60) if "duck" not in d else (240, 120, 180)
    piece(c, [Ell(700, 240, 26, 18), Circ(724, 220, 12)], duck, border=1.2, shadow=SMALL)
    flat(c, Poly([(734, 220), (748, 224), (734, 228)]), (240, 140, 50))
    for k in range(3):
        piece(c, RRect(780 + k * 32, 214, 808 + k * 32, 260, 2), [(90, 150, 230), (120, 200, 120), (240, 120, 120)][k], border=1, shadow=SMALL)
    # floor + rug
    c.rect(0, 430, W, H, (200, 160, 120))
    for y in range(430, H, 24):
        flat(c, Thick(0, y, W, y, 1.2), (186, 146, 108))
    flat(c, Ell(450, 520, 360, 70), (120, 170, 220))
    c.ellipse_ring(450, 520, 330, 60, 6, (250, 250, 246))
    # block tower (left middle)
    blocks = [(240, 90, 90), (90, 150, 230), (240, 200, 60), (120, 200, 120), (200, 120, 220)]
    for k, col in enumerate(blocks):
        if k == 4 and "block" in d:
            col = (250, 150, 60)
        x = 300 + (k % 2) * 6
        piece(c, RRect(x - 24, 430 - k * 44, x + 24, 474 - k * 44, 3), col, border=1.2, shadow=SMALL)
        flat(c, Poly(star_pts(x, 452 - k * 44, 10, 4)), (250, 250, 246))
    # teddy (right middle)
    teddy(c, 620, 460, 1.3, (200, 150, 100), (220, 60, 80) if "bow" not in d else (60, 160, 220))
    # rocking horse (left foreground)
    rh = (250, 246, 236) if "horse" not in d else (240, 180, 80)
    piece(c, [Ell(110, 590, 90, 14)], (200, 80, 60), shadow=PROP)
    piece(c, [Ell(110, 520, 46, 20), Poly([(140, 516), (160, 466), (176, 470), (160, 520)]), Ell(176, 470, 16, 10), Thick(70, 530, 60, 584, 6), Thick(150, 530, 160, 584, 6)],
          rh, border=1.5, shadow=PROP)
    flat(c, [Thick(150, 470, 136, 510, 5)], (200, 80, 60))
    flat(c, Circ(178, 466, 2), INK)
    # train set on the rug (bottom centre)
    flat(c, [Thick(320, 560, 640, 560, 3), Thick(320, 572, 640, 572, 3)], (150, 110, 80))
    eng = (220, 60, 60) if "train" not in d else (60, 160, 120)
    piece(c, [RRect(500, 520, 580, 566, 4), RRect(540, 496, 580, 524, 3), RRect(510, 504, 524, 520, 2)], eng, border=1.5, shadow=PROP)
    for x in (514, 540, 566):
        wheel(c, x, 570, 8, tyre=(40, 40, 46), hub=(240, 200, 60))
    for k, col in enumerate(((90, 150, 230), (240, 200, 60))):
        piece(c, RRect(380 + k * 60, 530, 430 + k * 60, 566, 3), col, border=1.2, shadow=SMALL)
        for x in (392 + k * 60, 418 + k * 60):
            wheel(c, x, 570, 7)
    # robot toy (right foreground)
    piece(c, [RRect(760, 500, 840, 580, 6), RRect(774, 450, 826, 500, 6), RRect(770, 580, 790, 600, 2), RRect(810, 580, 830, 600, 2)], (180, 190, 210), border=1.5, shadow=PROP)
    flat(c, [Circ(788, 474, 7), Circ(812, 474, 7)], (90, 220, 240))
    flat(c, RRect(776, 520, 824, 540, 3), (240, 120, 60))
    if "antenna" not in d:
        flat(c, Thick(800, 450, 800, 416, 4), (90, 90, 100))
        piece(c, Circ(800, 408, 13), (240, 80, 80), shadow=None)


L251_ELEMENTS = [
    E("top", lambda c, m: [piece(c, Poly([(380, 490), (420, 490), (400, 520)]), (240, 140, 200), shadow=SMALL), flat(c, Thick(400, 490, 400, 476, 3), (90, 90, 100))],
      pivot=(400, 505), anim=dict(stretch=(0.3, 0), scaleSpeed=6)),

    E("sun", lambda c, m: soft_union(c, [Poly([(372, 188), (528, 188), (600, 430), (300, 430)])], (255, 250, 220), 0.15, spread=12), daynight="untinted",
      anim=dict(twinkle=0.2, twinkleSpeed=0.4)),
]

L251_DIFFS = [
    ("kite", 100, 96, 0),
    ("curtain", 545, 125, 0),
    ("duck", 710, 234, 0),
    ("block", 300, 274, 0),
    ("bow", 620, 400, 0),
    ("horse", 120, 520, 0),
    ("train", 540, 534, 0),
    ("antenna", 800, 420, 0),
]


# =================================================================== Level 252 circus big top
def l252_bg(c, d):
    # canopy stripes radiating from the top centre
    c.rect(0, 0, W, 300, (150, 40, 50))
    for k in range(-8, 9):
        col = (220, 60, 60) if k % 2 else (250, 246, 236)
        flat(c, Poly([(450, -40), (450 + k * 110, 300), (450 + (k + 1) * 110, 300)]), col)
    flat(c, Thick(0, 300, W, 300, 6), (240, 200, 60))
    for x in range(0, W, 40):
        flat(c, Poly([(x, 300), (x + 40, 300), (x + 20, 320)]), (240, 200, 60))
    # trapeze platforms + spotlights
    plat = (90, 150, 230) if "plat" not in d else (240, 140, 60)
    piece(c, [RRect(120, 100, 190, 112, 2), Thick(155, 0, 155, 100, 3)], plat, shadow=SMALL)
    piece(c, [RRect(710, 100, 780, 112, 2), Thick(745, 0, 745, 100, 3)], (90, 150, 230), shadow=SMALL)
    spot = (250, 240, 180)
    piece(c, [RRect(836, 26, 884, 60, 4)], (60, 60, 70) if "spot" not in d else (230, 70, 70), shadow=SMALL)
    flat(c, Ell(860, 62, 16, 6), spot)
    soft_union(c, [Poly([(846, 62), (874, 62), (640, 480), (500, 480)])], spot, 0.12, spread=16)
    # flags along the rim
    bunting(c, -10, 120, 910, 120, [(240, 200, 60), (90, 150, 230), (120, 200, 120)], 14, sag=40, size=14,
            swap=(6, (200, 120, 220)) if "flag" in d else None)
    # audience stands
    stands(c, 300, 420, 2521, col=(120, 60, 70))
    # ring
    c.rect(0, 420, W, H, (200, 160, 110))
    flat(c, Ell(450, 520, 400, 80), (220, 60, 60))
    flat(c, Ell(450, 516, 380, 70), (230, 190, 130))
    # pedestal with stars (centre)
    ped = (90, 150, 230)
    piece(c, [RRect(400, 470, 500, 530, 6), Ell(450, 470, 50, 10)], ped, border=1.5, shadow=PROP)
    for x in (420, 450, 480):
        flat(c, Poly(star_pts(x, 500, 10, 4)), (250, 220, 60))
    # ringmaster on the pedestal
    hx, hy = modern(c, 450, 466, (200, 40, 50) if "pedestal" not in d else (60, 140, 90), bottom=(250, 250, 246), hair=(40, 30, 30), h=1.6)
    piece(c, [RRect(hx - 8, hy - 26, hx + 8, hy - 8, 2), Ell(hx, hy - 8, 14, 3)], (40, 40, 46), shadow=None)
    # juggler (left)
    jug = (120, 200, 120) if "juggler" not in d else (240, 140, 60)
    hx, hy = modern(c, 236, 520, jug, bottom=(90, 90, 160), hair=(200, 150, 80), h=1.8)
    # seal with ball (right)
    piece(c, [Ell(640, 520, 36, 18), Poly([(660, 512), (676, 470), (690, 476), (680, 520)]), Circ(682, 466, 12), Poly([(610, 530), (590, 546), (614, 540)])],
          (80, 90, 110), border=1.5, shadow=PROP)
    flat(c, [Circ(686, 462, 2), Circ(692, 470, 2.4)], INK)
    ball = (240, 200, 60) if "ball" not in d else (90, 150, 230)
    piece(c, Circ(684, 434, 18), ball, border=1.2, shadow=SMALL)
    flat(c, Thick(668, 434, 700, 434, 4), (220, 60, 60))
    # clown car (left foreground)
    car = (240, 140, 200)
    piece(c, [RRect(20, 540, 170, 580, 12), RRect(50, 510, 130, 544, 10)], car, border=1.5, shadow=PROP)
    flat(c, RRect(60, 516, 120, 536, 6), (180, 220, 240))
    for x in (50, 140):
        wheel(c, x, 584, 14, hub=(240, 200, 60))
    flat(c, Circ(90, 498, 12), (250, 246, 240))
    nose = (220, 40, 40) if "nose" not in d else (60, 160, 230)
    flat(c, Circ(98, 500, 5), nose)
    flat(c, [Circ(80, 488, 7), Circ(100, 486, 7)], (240, 140, 40))
    # popcorn cart (right foreground)
    pop = (250, 250, 246)
    piece(c, [RRect(760, 500, 880, 590, 4)], (220, 60, 60), border=1.5, shadow=PROP)
    piece(c, RRect(770, 440, 870, 500, 3), (240, 246, 250, 0.8), border=1.2, shadow=None)
    for k in range(14):
        flat(c, Circ(780 + (k * 37) % 84, 490 - (k * 13) % 40, 6), (250, 240, 200))
    box = (250, 250, 246) if "popcorn" not in d else (240, 200, 60)
    piece(c, Poly([(800, 520), (840, 520), (836, 560), (804, 560)]), box, border=1, shadow=SMALL)
    for k in range(3):
        flat(c, Thick(806 + k * 12, 520, 808 + k * 12, 560, 4), (220, 60, 60))


L252_ELEMENTS = [
    E("acrobat", lambda c, m: [flat(c, [Thick(420, 0, 420, 150, 1.4), Thick(480, 0, 480, 150, 1.4), Thick(420, 150, 480, 150, 3)], (200, 200, 210)),
                               modern(c, 450, 200, (240, 200, 60), bottom=(240, 200, 60), hair=(40, 30, 30), h=1.0)], pivot=(450, 0),
      anim=dict(swingAngle=18, swingSpeed=0.4)),
    E("pins", lambda c, m: [piece(c, Ell(236 + dx, 420 + dy, 5, 10), (250, 250, 246), shadow=None) for dx, dy in ((-20, 0), (0, -20), (20, 0))], pivot=(236, 420),
      anim=dict(rotateSpeed=160)),
    E("glow", lambda c, m: soft_union(c, [Ell(450, 516, 120, 30)], (255, 240, 180), 0.2, spread=20), daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.8)),
]

L252_DIFFS = [
    ("plat", 155, 106, 0),
    ("flag", 417, 165, 0),
    ("spot", 860, 43, 0),
    ("juggler", 236, 470, 0),
    ("ball", 684, 434, 0),
    ("nose", 98, 500, 0),
    ("pedestal", 450, 440, 0),
    ("popcorn", 820, 540, 0),
]


# =================================================================== Level 253 pirate ship deck
def l253_bg(c, d):
    sky(c, (120, 190, 240), (220, 236, 250), 320)
    cloud_bg(c, 680, 80, 0.6)
    # sea + island
    c.rect(0, 260, W, 400, (60, 140, 200))
    piece(c, Ell(140, 268, 110, 22), (230, 210, 150), shadow=SMALL)
    palm(c, 150, 262, h=70, lean=10)
    # masts + sails
    for x in (300, 640):
        piece(c, RRect(x - 8, 20, x + 8, 420, 2), (130, 90, 60), shadow=PROP)
        piece(c, RRect(x - 90, 60, x + 90, 68, 2), (120, 84, 56), shadow=SMALL)
        piece(c, RRect(x - 80, 210, x + 80, 218, 2), (120, 84, 56), shadow=SMALL)
    for x in (300, 640):
        sail = (250, 246, 230)
        piece(c, Poly([(x - 84, 68), (x + 84, 68), (x + 76, 200), (x - 76, 200)]), sail, border=1.5, shadow=PROP)
        piece(c, Poly([(x - 70, 218), (x + 70, 218), (x + 64, 330), (x - 64, 330)]), sail, border=1.5, shadow=PROP)
    patch = (200, 160, 110) if "patch" not in d else (90, 150, 220)
    piece(c, RRect(430 + 180, 120, 470 + 180, 160, 2), patch, shadow=None)
    flat(c, [Thick(612, 122, 648, 158, 1), Thick(648, 122, 612, 158, 1)], lit(patch, 0.7))
    # rigging ropes
    for x0, x1 in ((300, 120), (300, 470), (640, 470), (640, 860)):
        flat(c, Thick(x0, 40, x1, 420, 1.4), (90, 70, 50))
    # crow's nest + flag
    piece(c, [RRect(276, 20, 324, 40, 3)], (130, 90, 60), shadow=SMALL)
    flat(c, Thick(300, 20, 300, -10, 2), (90, 70, 50))
    flag = (40, 40, 50) if "flag" not in d else (200, 60, 60)
    piece(c, Poly([(302, 0), (350, 4), (350, 24), (302, 20)]), flag, shadow=SMALL)
    flat(c, [Circ(326, 12, 4)], (250, 250, 246))
    # deck
    c.rect(0, 400, W, H, (170, 120, 80))
    for y in range(400, H, 20):
        flat(c, Thick(0, y, W, y, 1.2), (150, 104, 68))
    piece(c, RRect(-10, 380, 910, 404, 2), (130, 90, 60), shadow=PROP)
    for x in range(10, W, 40):
        flat(c, RRect(x, 360, x + 8, 384, 1), (130, 90, 60))
    flat(c, RRect(-10, 354, 910, 364, 2), (120, 84, 56))
    # parrot on the rail (right)
    par = (60, 180, 90) if "parrot" not in d else (230, 70, 70)
    piece(c, [Ell(520, 330, 14, 22), Circ(524, 304, 11), Poly([(512, 346), (528, 346), (520, 380)])], par, border=1.2, shadow=SMALL)
    flat(c, Poly([(534, 300), (546, 306), (534, 312)]), (250, 200, 60))
    flat(c, Circ(528, 300, 2), INK)
    # barrels (left middle)
    for k, x in enumerate((240, 300)):
        band = (90, 90, 100)
        piece(c, [Ell(x, 450, 28, 40)], (160, 110, 70) if not (k == 1 and "barrel" in d) else (90, 140, 170), border=1.5, shadow=PROP)
        flat(c, [Thick(x - 26, 430, x + 26, 430, 4), Thick(x - 26, 470, x + 26, 470, 4)], band)
    # cannon (right middle)
    if "cannon" not in d:
        piece(c, [Thick(560, 440, 680, 410, 22), Circ(560, 442, 16)], (60, 60, 70), shadow=PROP)
        piece(c, [Circ(590, 470, 18), Circ(650, 466, 18)], (130, 90, 60), shadow=SMALL)
        flat(c, [Circ(520, 480, 10), Circ(540, 486, 10), Circ(530, 470, 10)], (40, 40, 46))
    # ship's wheel (left foreground)
    wheel_col = (150, 100, 60) if "wheel" not in d else (220, 180, 70)
    for k in range(8):
        a = k * math.pi / 4
        piece(c, Thick(110, 500, 110 + 70 * math.cos(a), 500 + 70 * math.sin(a), 6), wheel_col, shadow=SMALL)
    c.ellipse_ring(110, 500, 50, 50, 8, wheel_col)
    piece(c, Circ(110, 500, 16), (110, 74, 44) if "hub" not in d else (220, 180, 70), shadow=None)
    # captain (cartoon) behind the map table
    hx, hy = modern(c, 450, 520, (60, 60, 120), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0)
    piece(c, [Poly([(hx - 26, hy - 8), (hx + 26, hy - 8), (hx + 10, hy - 26), (hx - 10, hy - 26)])], (40, 40, 46), shadow=None)
    flat(c, Ell(hx + 3, hy + 8, 9, 5), (60, 40, 30))
    piece(c, RRect(360, 520, 540, 540, 3), (120, 84, 56), border=1.5, shadow=PROP)
    piece(c, Poly([(380, 512), (520, 512), (514, 526), (386, 526)]), (240, 220, 170), shadow=None)
    flat(c, [Thick(400, 518, 470, 520, 1.6), Thick(470, 518, 480, 522, 1.6)], (200, 60, 60))
    candle = (250, 240, 220) if "candle" not in d else (220, 80, 80)
    piece(c, RRect(500, 488, 512, 514, 2), candle, shadow=None)
    # treasure chest (right foreground)
    chest = (160, 100, 50) if "chest" not in d else (100, 110, 180)
    piece(c, [RRect(740, 500, 860, 570, 4), Poly([(740, 502), (860, 502), (850, 470), (750, 470)])], chest, border=1.5, shadow=PROP)
    flat(c, [RRect(740, 500, 860, 506, 0), RRect(792, 498, 808, 524, 2)], (240, 200, 70))
    flat(c, [Circ(760 + k * 14, 468 - (k % 2) * 6, 7) for k in range(7)], (250, 210, 80))


L253_ELEMENTS = [
    E("wave", lambda c, m: [flat(c, Thick(x, 300, x + 40, 300, 2), (150, 200, 240)) for x in (420, 760, 860)], daynight="untinted",
      anim=dict(bobAmplitude=(14, 0), bobSpeed=0.3)),
    bird_el("gull", 520, 40, s=10, speed=-16),
    E("pennant", lambda c, m: piece(c, Poly([(640, 20), (690, 26), (640, 34)]), (220, 60, 60), shadow=SMALL), pivot=(640, 27), anim=dict(stretch=(0.25, 0), scaleSpeed=1.4)),
    E("flame", lambda c, m: flat(c, Poly([(502, 488), (510, 488), (506, 474)]), (255, 190, 70)), pivot=(506, 488), daynight="untinted", anim=dict(stretch=(0.2, 0.4), scaleSpeed=5)),
]

L253_DIFFS = [
    ("flag", 326, 12, 0),
    ("patch", 630, 140, 0),
    ("parrot", 524, 330, 0),
    ("barrel", 300, 450, 0),
    ("hub", 110, 500, 0),
    ("cannon", 610, 440, 0),
    ("wheel", 110, 500, 0),
    ("candle", 506, 500, 0),
    ("chest", 800, 520, 0),
]


# =================================================================== Level 254 desert bazaar
def dome_house(c, x0, x1, base, top, wall, dome):
    piece(c, RRect(x0, top, x1, base, 2), wall, border=1.5, shadow=PROP)
    cx, r = (x0 + x1) / 2, (x1 - x0) * 0.36
    piece(c, Poly([(cx + r * math.cos(math.pi * k / 12), top - r * math.sin(math.pi * k / 12) * 1.1) for k in range(13)]), dome, border=1.5, shadow=PROP)
    flat(c, Thick(cx, top - r * 1.1, cx, top - r * 1.1 - 16, 2), (200, 170, 80))
    for wx in (x0 + 14, x1 - 34):
        flat(c, [RRect(wx, top + 20, wx + 20, top + 50, 10)], (90, 70, 70))


def l254_bg(c, d):
    sky(c, (250, 190, 120), (250, 226, 180), 300)
    # far dunes + town
    piece(c, hill_strip(220, [(14, 0.008, 0.4), (8, 0.02, 1.4)]), (236, 196, 140), shadow=LAYER)
    dome_house(c, 40, 200, 300, 160, (240, 220, 190), (90, 150, 200) if "dome" not in d else (220, 120, 70))
    dome_house(c, 220, 340, 300, 180, (236, 210, 176), (230, 190, 90))
    dome_house(c, 700, 860, 300, 170, (240, 220, 190), (110, 170, 150))
    piece(c, [RRect(560, 80, 590, 300, 2), Poly([(552, 82), (598, 82), (575, 50)])], (236, 210, 176), border=1.5, shadow=PROP)
    # string with hanging lamps
    pts = []
    for k in range(9):
        t = k / 8
        pts.append((360 + 300 * t, 110 + 50 * 4 * t * (1 - t)))
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 1.4), (90, 70, 60))
    for k, (x, y) in enumerate(pts[1:-1:2]):
        col = (240, 180, 60) if not (k == 3 and "lamp" in d) else (90, 190, 220)
        lantern(c, x, y + 18, 0.9, col, tassel=(200, 60, 60))
    # hanging carpets on a rail (centre)
    flat(c, Thick(360, 180, 680, 180, 4), (120, 90, 60))
    for k, x in enumerate((370, 480, 590)):
        base_col = [(180, 50, 60), (60, 90, 150), (200, 120, 50)][k]
        if k == 1 and "carpet" in d:
            base_col = (80, 140, 90)
        piece(c, RRect(x, 180, x + 90, 320, 2), base_col, border=1.2, shadow=PROP)
        flat(c, RRect(x + 10, 192, x + 80, 308, 2), lit(base_col, 1.25))
        flat(c, Poly([(x + 45, 210), (x + 72, 250), (x + 45, 290), (x + 18, 250)]), base_col)
        for j in range(5):
            flat(c, Thick(x + 6 + j * 18, 320, x + 6 + j * 18, 330, 2), (240, 220, 160))
    # ground
    c.rect(0, 330, W, H, (226, 196, 150))
    for x in range(0, W, 60):
        flat(c, RRect(x + 2, 330, x + 58, 600, 0), (230, 200, 154) if (x // 60) % 2 else (224, 194, 148))
    # stall awning (left) with spice piles
    piece(c, [Poly([(20, 330), (320, 330), (300, 360), (40, 360)])], (200, 80, 60), border=1.5, shadow=PROP)
    piece(c, RRect(30, 400, 320, 450, 3), (150, 100, 60), border=1.5, shadow=PROP)
    for k, (x, col) in enumerate(((70, (220, 120, 40)), (130, (230, 190, 50)), (190, (170, 50, 40)), (250, (120, 150, 60)), (300, (200, 160, 110)))):
        if k == 2 and "spice" in d:
            col = (120, 90, 170)
        piece(c, [Ell(x, 400, 26, 10), RRect(x - 26, 400, x + 26, 410, 2)], (170, 120, 70), shadow=SMALL)
        piece(c, Poly([(x - 22, 400), (x + 22, 400), (x, 372)]), col, shadow=None)
    # pottery (right)
    for k, (x, h, col) in enumerate(((560, 60, (190, 110, 70)), (620, 80, (170, 100, 70)), (680, 50, (200, 140, 90)))):
        if k == 1 and "pot" in d:
            col = (70, 140, 170)
        piece(c, [Ell(x, 420 - h / 2, 24, h / 2), RRect(x - 10, 420 - h - 10, x + 10, 420 - h + 2, 3)], col, border=1.5, shadow=PROP)
        flat(c, Thick(x - 20, 420 - h / 2, x + 20, 420 - h / 2, 3), (240, 220, 160))
    # camel (left foreground)
    camel(c, 110, 570, 1.4, blanket=(60, 110, 200) if "camel" not in d else (220, 180, 50))
    # fruit basket (centre)
    piece(c, Poly([(400, 520), (500, 520), (490, 560), (410, 560)]), (190, 140, 80), border=1.5, shadow=PROP)
    fruit = (240, 140, 40) if "fruit" not in d else (150, 200, 70)
    flat(c, [Circ(416 + k * 14, 514 - (k % 2) * 6, 9) for k in range(6)], fruit)
    # merchant (right foreground)
    hx, hy = modern(c, 790, 600, (240, 240, 230), bottom=(120, 90, 70), hair=(40, 30, 30), h=2.2)
    hat = (200, 60, 60) if "hat" not in d else (60, 140, 200)
    piece(c, [Ell(hx, hy - 8, 18, 10), RRect(hx - 16, hy - 12, hx + 16, hy - 4, 3)], hat, border=1, shadow=None)
    palm(c, 880, 600, h=200, lean=-20)


L254_ELEMENTS = [
    E("smoke", lambda c, m: piece(c, Circ(650, 140, 8), (240, 236, 230), shadow=None), pivot=(650, 140),
      anim=dict(driftVelocity=(4, -20), driftLength=50, driftFade=True, driftGrow=1.6)),
    E("cloth", lambda c, m: piece(c, Poly([(460, 334), (500, 334), (496, 366), (464, 366)]), (240, 220, 160), shadow=SMALL), pivot=(480, 334),
      anim=dict(swingAngle=5, swingSpeed=0.7)),
    bird_el("bird", 400, 60, s=9, speed=16),
    E("glow", lambda c, m: soft_union(c, [Circ(x, y + 18, 14) for x, y in ((435, 147), (585, 147))], (255, 210, 120), 0.3, spread=16), daynight="untinted",
      anim=dict(twinkle=0.5, twinkleSpeed=1.0)),
]

L254_DIFFS = [
    ("dome", 120, 140, 0),
    ("carpet", 525, 250, 0),
    ("lamp", 622, 150, 0),
    ("spice", 190, 390, 0),
    ("pot", 620, 380, 0),
    ("camel", 100, 512, 0),
    ("fruit", 450, 510, 0),
    ("hat", 790, 480, 0),
]


LEVELS = [
    ("Level245", "非洲草原", l245_bg, L245_ELEMENTS, L245_DIFFS, 60, OPTS),
    ("Level246", "建筑工地", l246_bg, L246_ELEMENTS, L246_DIFFS, 60, OPTS),
    ("Level247", "火车站月台", l247_bg, L247_ELEMENTS, L247_DIFFS, 60, OPTS),
    ("Level248", "集装箱码头", l248_bg, L248_ELEMENTS, L248_DIFFS, 60, OPTS),
    ("Level249", "植物温室", l249_bg, L249_ELEMENTS, L249_DIFFS, 60, OPTS),
    ("Level250", "昆虫花园", l250_bg, L250_ELEMENTS, L250_DIFFS, 60, OPTS),
    ("Level251", "玩具房", l251_bg, L251_ELEMENTS, L251_DIFFS, 60, OPTS),
    ("Level252", "马戏团", l252_bg, L252_ELEMENTS, L252_DIFFS, 60, OPTS),
    ("Level253", "海盗船甲板", l253_bg, L253_ELEMENTS, L253_DIFFS, 60, OPTS),
    ("Level254", "沙漠集市", l254_bg, L254_ELEMENTS, L254_DIFFS, 60, OPTS),
]
