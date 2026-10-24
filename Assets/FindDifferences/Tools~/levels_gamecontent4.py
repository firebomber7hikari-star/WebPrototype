# -*- coding: utf-8 -*-
"""Inside video games, part 4 (all designs original: no real games, characters, brands or logos):
  Level195 隐藏物品   - a hidden-object antique shop crammed with curios, with the item list below
  Level196 竖版弹幕   - a vertical bullet-hell shooter: boss, drone formation, bullet rings, the player's plane
  Level197 潜行博物馆 - a top-down stealth heist: display cases, laser grid, guards with torch cones, cameras
  Level198 MMO主城    - an MMO town square: fountain, guild hall, players with name bars, chat box, skill bar
  Level199 地牢肉鸽   - a roguelike dungeon room: doors, chest, shop rug, pots, slimes, relics and room map
  Level200 游乐园经营 - an isometric theme-park builder: coaster, ferris wheel, carousel, guests, budget panel
  Level201 台球       - a top-down pool table: racked balls, cue and aim line, player panels
  Level202 拼图       - a jigsaw on a wooden table: half-finished landscape, loose pieces, box lid, tea
  Level203 大逃杀     - a battle-royale drop: island from above, safe zone, parachutes, airdrop, alive count
  Level204 MOBA对线   - a MOBA lane: towers, minions, heroes, river, jungle camp, skill bar, minimap
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from stylekit import flame
from levels_retro import digits, sprite
from levels_gamecontent import OUTLINE, glyph_line, toon
from levels_gamecontent2 import P, bar, chibi, iso_box, iso_house, iso_tree, rot_poly
from levels_gamecontent3 import heart, panel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 220, 190)


def vase(c, x, base, h, col, neck=0.4):
    toon(c, [Ell(x, base - h * 0.4, h * 0.32, h * 0.4), RRect(x - h * neck * 0.3, base - h, x + h * neck * 0.3, base - h * 0.6, 3)], col, w=1.4, shadow=None)
    flat(c, Thick(x - h * 0.28, base - h * 0.42, x + h * 0.28, base - h * 0.42, 2), lit(col, 0.7))


# =================================================================== Level 195 hidden-object antique shop
def l195_bg(c, d):
    c.rect(0, 0, W, 500, (120, 80, 70))
    for x in range(0, W, 30):
        flat(c, Thick(x, 0, x, 500, 1), (110, 72, 62))
    # shelves (three bays)
    for bx in (20, 320, 620):
        toon(c, RRect(bx, 30, bx + 260, 420, 4), (90, 60, 40), w=2)
        for y in (120, 210, 300, 390):
            flat(c, RRect(bx + 6, y, bx + 254, y + 10, 0), (140, 96, 62))
    # bay 1: vases, teapot, books
    vase(c, 60, 120, 70, (60, 110, 180))
    vase(c, 120, 120, 54, (200, 80, 70) if "vase" not in d else (90, 170, 110))
    vase(c, 180, 120, 76, (220, 200, 150))
    vase(c, 240, 120, 50, (120, 70, 140))
    toon(c, [Ell(90, 196, 30, 20), Thick(118, 192, 140, 176, 6), RRect(84, 168, 96, 178, 3)], (240, 236, 220) if "teapot" not in d else (230, 160, 70), w=1.4,
         shadow=None)
    flat(c, Thick(62, 190, 50, 176, 6), (240, 236, 220) if "teapot" not in d else (230, 160, 70))
    for k, col in enumerate(((170, 60, 60), (60, 100, 160), (70, 130, 90), (200, 160, 70), (120, 80, 140), (150, 110, 80))):
        flat(c, RRect(150 + k * 18, 150, 166 + k * 18, 210, 1), col)
    for k in range(5):
        toon(c, RRect(40 + k * 44, 250, 76 + k * 44, 300, 3), [(200, 180, 120), (150, 150, 160), (180, 120, 80), (110, 150, 120), (210, 200, 190)][k], w=1.2, shadow=None)
        flat(c, Circ(58 + k * 44, 272, 9), (60, 50, 50))
    toon(c, [Circ(80, 360, 28), Thick(80, 388, 80, 390, 2)], (90, 140, 200), w=1.4, shadow=None)
    flat(c, [Ell(74, 352, 12, 8), Ell(92, 368, 9, 6)], (110, 170, 100))
    toon(c, [RRect(70, 386, 90, 392, 1), Thick(80, 330, 80, 390, 2)], (200, 160, 70), w=1, shadow=None)
    globe_stand = (200, 160, 70) if "globe" not in d else (90, 90, 110)
    flat(c, [RRect(70, 386, 90, 392, 1)], globe_stand)
    c.ellipse_ring(80, 360, 32, 32, 3, globe_stand)
    for k in range(3):
        toon(c, RRect(140 + k * 40, 340, 170 + k * 40, 390, 4), [(160, 120, 80), (90, 90, 100), (200, 190, 170)][k], w=1.2, shadow=None)
    # bay 2: clocks, mask, candles, music box
    toon(c, Circ(380, 76, 34), (200, 160, 70), w=1.6, shadow=None)
    flat(c, Circ(380, 76, 26), (250, 246, 230))
    flat(c, [Thick(380, 76, 380, 58, 3), Thick(380, 76, 394, 82, 3)], (40, 40, 50))
    clock2 = (130, 80, 50) if "clock" not in d else (60, 120, 160)
    toon(c, [RRect(440, 40, 490, 120, 6), Circ(465, 40, 25)], clock2, w=1.6, shadow=None)
    flat(c, Circ(465, 44, 16), (250, 246, 230))
    toon(c, [Ell(540, 70, 34, 40)], (240, 220, 180) if "mask" not in d else (90, 170, 210), w=1.6, shadow=None)
    flat(c, [Ell(528, 66, 8, 6), Ell(552, 66, 8, 6)], (40, 30, 40))
    flat(c, Thick(530, 92, 550, 92, 3), (180, 60, 60))
    for k in range(4):
        toon(c, RRect(350 + k * 26, 170, 362 + k * 26, 210, 2), (246, 240, 220), w=1.2, shadow=None)
    toon(c, [RRect(470, 160, 560, 210, 4), RRect(470, 150, 560, 164, 4)], (150, 60, 80), w=1.4, shadow=None)
    flat(c, RRect(500, 176, 530, 196, 2), (240, 200, 90))
    for k in range(6):
        vase(c, 350 + k * 38, 300, 40 + (k % 3) * 10, [(80, 150, 140), (200, 120, 60), (150, 150, 200)][k % 3])
    toon(c, [Poly([(360, 390), (420, 390), (408, 340), (372, 340)])], (110, 90, 70), w=1.4, shadow=None)
    toon(c, [Ell(500, 360, 50, 22), RRect(494, 380, 506, 390, 1)], (200, 200, 210), w=1.4, shadow=None)
    # bay 3: telescope, hats, picture frames, lamp
    toon(c, [Thick(650, 110, 740, 60, 12), Thick(700, 110, 700, 86, 3)], (200, 160, 70), w=1.4, shadow=None)
    for k, col in enumerate(((60, 50, 60), (150, 60, 60), (90, 110, 150))):
        toon(c, [Ell(780 + k * 30, 116, 22, 5), RRect(768 + k * 30, 86, 792 + k * 30, 116, 4)], col, w=1.2, shadow=None)
    for k in range(3):
        toon(c, RRect(640 + k * 80, 140, 706 + k * 80, 206, 3), (200, 160, 70), w=1.4, shadow=None)
        flat(c, RRect(648 + k * 80, 148, 698 + k * 80, 198, 2), [(150, 190, 220), (200, 140, 110), (140, 180, 120)][k])
    lamp = (90, 160, 120) if "lamp" not in d else (220, 120, 160)
    toon(c, [Thick(700, 300, 700, 250, 3), Poly([(670, 250), (730, 250), (718, 222), (682, 222)])], lamp, w=1.4, shadow=None)
    for k in range(4):
        toon(c, Circ(760 + k * 28, 284, 13), [(220, 60, 60), (250, 200, 60), (60, 120, 220), (90, 180, 110)][k], w=1.2, shadow=None)
    toon(c, [RRect(650, 340, 860, 390, 4)], (110, 80, 60), w=1.4, shadow=None)
    for k in range(5):
        flat(c, RRect(660 + k * 40, 350, 690 + k * 40, 380, 2), (200, 180, 140))
    # counter + rug + umbrella stand + cat
    c.rect(0, 420, W, H, (90, 60, 46))
    toon(c, RRect(300, 430, 620, 500, 4), (130, 90, 60), w=2)
    toon(c, [RRect(520, 404, 590, 432, 4)], (200, 200, 210), w=1.4, shadow=None)
    stand = (60, 90, 70) if "stand" not in d else (170, 70, 60)
    toon(c, RRect(200, 430, 250, 500, 4), stand, w=1.6, shadow=None)
    flat(c, [Thick(212, 430, 206, 380, 3), Thick(236, 430, 244, 386, 3)], (60, 50, 50))
    toon(c, [Ell(700, 480, 40, 18), Circ(734, 462, 15), Poly([(724, 452), (728, 436), (736, 450)]), Poly([(738, 450), (746, 436), (746, 454)])], (80, 70, 80), w=1.4,
         shadow=None)
    # item list panel
    panel(c, 20, 512, 880, 592, (60, 44, 40), r=12, w=2)
    shapes = [lambda x, y: vase(c, x, y + 18, 34, (200, 200, 200)), lambda x, y: toon(c, Circ(x, y, 14), (200, 200, 200), w=1.2, shadow=None),
              lambda x, y: toon(c, Ell(x, y, 16, 18), (200, 200, 200), w=1.2, shadow=None), lambda x, y: toon(c, rot_poly(x, y, 30, 22, 0), (200, 200, 200), w=1.2, shadow=None)]
    for k in range(8):
        x = 70 + k * 104
        flat(c, RRect(x - 40, 520, x + 40, 584, 6), (90, 66, 56))
        found = k in (1, 4) or (k == 6 and "list" in d)
        shapes[k % 4](x, 552)
        if found:
            flat(c, [Thick(x - 30, 530, x + 30, 576, 3), Thick(x + 30, 530, x - 30, 576, 3)], (90, 200, 110))


L195_ELEMENTS = flame("c1", 356, 170, s=0.5, glow_night=False) + flame("c2", 408, 170, s=0.5, glow_night=False) + [
    E("tail", lambda c, m: toon(c, Thick(662, 486, 640, 456, 6), (80, 70, 80), w=1.2, shadow=None), pivot=(662, 486), anim=dict(swingAngle=16, swingSpeed=0.6)),
    E("hint", lambda c, m: flat(c, Poly(star_pts(270, 360, 10, 2, points=4, rot=0)), (255, 255, 230)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
    E("dust", lambda c, m: soft_union(c, [Poly([(400, 0), (520, 0), (700, 420), (560, 420)])], (255, 240, 200), 0.1, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.3)),
]

L195_DIFFS = [
    ("vase", 120, 96, 0),
    ("teapot", 92, 190, 0),
    ("globe", 80, 360, 0),
    ("clock", 465, 70, 0),
    ("mask", 540, 70, 0),
    ("lamp", 700, 240, 0),
    ("stand", 225, 465, 0),
    ("list", 694, 552, 0),
]


# =================================================================== Level 196 vertical bullet-hell
def plane(c, x, y, s, body, wing):
    toon(c, Poly([(x, y - 34 * s), (x + 8 * s, y - 10 * s), (x + 40 * s, y + 6 * s), (x + 40 * s, y + 14 * s), (x + 8 * s, y + 10 * s), (x + 14 * s, y + 26 * s),
                  (x - 14 * s, y + 26 * s), (x - 8 * s, y + 10 * s), (x - 40 * s, y + 14 * s), (x - 40 * s, y + 6 * s), (x - 8 * s, y - 10 * s)]), body, w=1.6)
    flat(c, [Poly([(x + 10 * s, y - 4 * s), (x + 38 * s, y + 8 * s), (x + 10 * s, y + 6 * s)]), Poly([(x - 10 * s, y - 4 * s), (x - 38 * s, y + 8 * s), (x - 10 * s, y + 6 * s)])],
         wing)
    flat(c, Ell(x, y - 14 * s, 5 * s, 9 * s), (120, 220, 250))


def drone(c, x, y, col):
    toon(c, [Circ(x, y, 18), Poly([(x - 30, y - 6), (x - 16, y - 2), (x - 16, y + 6), (x - 30, y + 10)]), Poly([(x + 30, y - 6), (x + 16, y - 2), (x + 16, y + 6), (x + 30, y + 10)])],
         col, w=1.4, shadow=None)
    flat(c, Circ(x, y, 7), (250, 240, 120))


def l196_bg(c, d):
    c.gradient(0, H, (60, 120, 200), (110, 190, 230))
    # sea islands
    for x, y, r in ((140, 420, 70), (720, 200, 80), (420, 560, 60)):
        toon(c, Ell(x, y, r, r * 0.6), (230, 210, 150), w=1.6, shadow=None)
        flat(c, Ell(x, y - 4, r * 0.8, r * 0.45), (110, 180, 100))
        tc = (60, 140, 70) if not (x == 720 and "island" in d) else (230, 140, 50)
        for dx in (-r * 0.3, r * 0.2):
            flat(c, Circ(x + dx, y - 6, r * 0.18), tc)
    # boss
    toon(c, [Poly([(330, 40), (570, 40), (600, 110), (520, 150), (380, 150), (300, 110)])], (90, 80, 110), w=2)
    flat(c, [RRect(320, 70, 360, 110, 4), RRect(540, 70, 580, 110, 4)], (60, 56, 80))
    core = (250, 80, 120) if "core" not in d else (90, 220, 140)
    toon(c, Circ(450, 100, 30), core, w=1.6, shadow=None)
    flat(c, Circ(442, 92, 10), lit(core, 1.4))
    bar(c, 250, 14, 650, 26, 0.7 if "hp" not in d else 0.35, (240, 80, 90))
    # drone formation
    for k, (x, y) in enumerate(((180, 200), (260, 240), (640, 240), (720, 300), (120, 300), (780, 140))):
        drone(c, x, y, (200, 90, 90) if not (k == 1 and "drone" in d) else (90, 160, 230))
    # static bullet rings (pink)
    for k in range(16):
        a = math.radians(k * 22.5)
        flat(c, Circ(450 + math.cos(a) * 120, 210 + math.sin(a) * 70, 7), (250, 120, 200))
        flat(c, Circ(450 + math.cos(a) * 120, 210 + math.sin(a) * 70, 3), (255, 230, 250))
    # power capsule
    cap = (250, 200, 60) if "capsule" not in d else (120, 220, 250)
    toon(c, RRect(560, 370, 610, 396, 12), cap, w=1.6, shadow=None)
    glyph_line(c, 572, 604, 383, (90, 60, 30), 1960, w=2, size=8)
    # player plane + options
    plane(c, 450, 500, 1.4, (240, 240, 246), (220, 60, 60) if "wing" not in d else (60, 120, 220))
    # HUD
    digits(c, 20, 40, "0582100", (250, 250, 250), 4)
    for k in range(3 if "bombs" not in d else 2):
        toon(c, Circ(34 + k * 34, 570, 13), (250, 140, 60), w=1.4, shadow=None)
    for k in range(3):
        plane(c, 820 + k * 26, 572, 0.3, (240, 240, 246), (220, 60, 60))


L196_ELEMENTS = [
    E("ring", lambda c, m: [flat(c, Circ(450 + math.cos(math.radians(k * 30)) * 50, 100 + math.sin(math.radians(k * 30)) * 50, 6), (255, 220, 100)) for k in range(12)],
      pivot=(450, 100), daynight="untinted", anim=dict(rotateSpeed=50)),
    E("shot", lambda c, m: [flat(c, RRect(x - 2, 440, x + 2, 460, 1), (200, 250, 255)) for x in (436, 464)], daynight="untinted",
      anim=dict(driftVelocity=(0, 300), driftLength=240, driftFade=True)),
    E("optL", lambda c, m: toon(c, Circ(396, 520, 9), (120, 220, 250), w=1.2, shadow=None), pivot=(450, 520), anim=dict(orbitRadius=(54, 10), orbitSpeed=0.5)),
    E("cloud1", lambda c, m: flat(c, [Ell(100, 0, 60, 18), Ell(130, -8, 34, 14)], (250, 250, 255, 0.8)), anim=dict(driftVelocity=(0, -40), driftLength=660)),
    E("cloud2", lambda c, m: flat(c, [Ell(760, 0, 50, 16), Ell(790, -8, 30, 12)], (250, 250, 255, 0.8)), anim=dict(driftVelocity=(0, -30), driftLength=660, phase=0.5)),
]

L196_DIFFS = [
    ("island", 720, 194, 0),
    ("core", 450, 100, 0),
    ("hp", 550, 20, 0),
    ("drone", 260, 240, 0),
    ("capsule", 585, 383, 0),
    ("wing", 450, 510, 0),
    ("bombs", 102, 570, 0),
]


# =================================================================== Level 197 stealth museum heist
def l197_bg(c, d):
    c.rect(0, 0, W, H, (60, 60, 84))
    for j in range(0, H, 50):
        for i in range(0, W, 50):
            flat(c, RRect(i + 1, j + 1, i + 49, j + 49, 2), (70, 70, 96) if (i + j) // 50 % 2 else (66, 66, 90))
    # walls (top-down) with paintings
    toon(c, [RRect(0, 0, W, 40, 0), RRect(0, 0, 30, H, 0), RRect(870, 0, W, H, 0), RRect(300, 220, 600, 250, 0)], (110, 100, 120), w=2, shadow=None)
    for k, x in enumerate((120, 260, 640, 780)):
        col = [(200, 120, 90), (90, 150, 200), (160, 200, 120), (220, 190, 110)][k]
        if k == 2 and "painting" in d:
            col = (200, 100, 200)
        toon(c, RRect(x - 40, 6, x + 40, 36, 2), (200, 160, 70), w=1.4, shadow=None)
        flat(c, RRect(x - 34, 10, x + 34, 32, 1), col)
    # red carpet runner
    flat(c, RRect(400, 250, 500, 600, 0), (150, 50, 60))
    for x, y in ((830, 300), (60, 520)):
        toon(c, [Poly([(x - 18, y + 20), (x + 18, y + 20), (x + 14, y - 4), (x - 14, y - 4)]), Circ(x - 8, y - 16, 14), Circ(x + 8, y - 18, 14)], (80, 150, 90), w=1.4)
    # display cases
    def case(x, y, item):
        toon(c, RRect(x - 34, y - 34, x + 34, y + 34, 6), (180, 180, 196), w=1.6)
        flat(c, RRect(x - 28, y - 28, x + 28, y + 28, 4), (150, 210, 230, 0.7))
        item(x, y)
    case(150, 160, lambda x, y: toon(c, Poly(ngon(x, y, 16, 6, rot=30)), (90, 220, 240) if "gem" not in d else (240, 80, 120), w=1.4, shadow=None))
    case(750, 160, lambda x, y: toon(c, Poly([(x - 16, y + 8), (x + 16, y + 8), (x + 18, y - 12), (x + 8, y - 2), (x, y - 16), (x - 8, y - 2), (x - 18, y - 12)]),
                                     (250, 200, 60) if "crown" not in d else (200, 200, 216), w=1.4, shadow=None))
    case(150, 420, lambda x, y: vase(c, x, y + 20, 40, (90, 130, 200)))
    case(750, 420, lambda x, y: toon(c, Circ(x, y, 16), (200, 160, 110), w=1.4, shadow=None))
    # statue (centre)
    statue = (200, 200, 210) if "statue" not in d else (200, 160, 90)
    toon(c, Circ(450, 130, 44), (130, 126, 140), w=1.6)
    toon(c, [Circ(450, 120, 18), Ell(450, 148, 24, 14)], statue, w=1.4, shadow=None)
    # laser grid
    for y in (300, 330, 360):
        flat(c, Thick(30, y, 300, y, 2), (250, 60, 60))
    for x in (40, 290):
        flat(c, RRect(x - 6, 290, x + 6, 370, 2), (90, 90, 110))
    # cameras + vent
    cam = (40, 40, 50) if "camera" not in d else (220, 160, 60)
    for x, y, ang in ((50, 60, 40), (850, 200, 150)):
        toon(c, rot_poly(x, y, 36, 20, ang), cam if x == 850 else (40, 40, 50), w=1.2, shadow=None)
        soft_union(c, [Poly([(x, y), (x + math.cos(math.radians(ang - 20)) * 180, y + math.sin(math.radians(ang - 20)) * 180),
                             (x + math.cos(math.radians(ang + 20)) * 180, y + math.sin(math.radians(ang + 20)) * 180)])], (250, 250, 160), 0.1, spread=8)
    if "vent" not in d:
        toon(c, RRect(700, 520, 780, 570, 3), (130, 130, 146), w=1.6, shadow=None)
        for k in range(4):
            flat(c, Thick(708, 528 + k * 11, 772, 528 + k * 11, 2), (90, 90, 106))
    # thief (top-down-ish chibi)
    chibi(c, 330, 520, s=0.9, hair=(30, 30, 40), outfit=(40, 40, 56), face=1)
    flat(c, RRect(310, 462, 352, 470, 2), (30, 30, 40))
    # detection meter
    panel(c, 620, 50, 860, 90, (30, 30, 44))
    toon(c, Ell(644, 70, 14, 9), (250, 250, 250), w=1.2, shadow=None)
    flat(c, Circ(644, 70, 5), (40, 40, 50))
    bar(c, 670, 64, 846, 76, 0.3, (250, 200, 60))


def guard_el(eid, x, y, ang, ph):
    def d(c, m):
        soft_union(c, [Poly([(x, y), (x + math.cos(math.radians(ang - 22)) * 150, y + math.sin(math.radians(ang - 22)) * 150),
                             (x + math.cos(math.radians(ang + 22)) * 150, y + math.sin(math.radians(ang + 22)) * 150)])], (255, 240, 150), 0.35, spread=10)
        toon(c, Circ(x, y, 16), (60, 90, 160), w=1.4, shadow=None)
        flat(c, Circ(x, y, 9), (40, 40, 50))
    return E(eid, d, pivot=(x, y), daynight="untinted", anim=dict(swingAngle=30, swingSpeed=0.12, phase=ph))


L197_ELEMENTS = [
    guard_el("guard1", 560, 400, 200, 0.0),
    guard_el("guard2", 620, 300, 300, 0.5),
    E("laser", lambda c, m: [soft_union(c, [Thick(30, y, 300, y, 2)], (255, 80, 80), 0.5, spread=6) for y in (300, 330, 360)], daynight="untinted",
      anim=dict(twinkle=0.5, twinkleSpeed=1.5)),
    E("rec", lambda c, m: flat(c, Circ(856, 192, 4), (255, 60, 60)), daynight="untinted", anim=dict(blinkInterval=1.0, blinkDuration=0.5)),
]

L197_DIFFS = [
    ("painting", 640, 21, 0),
    ("gem", 150, 160, 0),
    ("crown", 750, 158, 0),
    ("statue", 450, 130, 0),
    ("camera", 850, 200, 0),
    ("vent", 740, 545, 0),
]


# =================================================================== Level 198 MMO town square
def namebar(c, x, y, col, seed):
    flat(c, RRect(x - 30, y - 7, x + 30, y + 7, 4), (20, 20, 30, 0.6))
    glyph_line(c, x - 26, x + 30, y, col, seed, w=1.6, size=8)


def l198_bg(c, d):
    c.gradient(0, 300, (130, 190, 240), (220, 236, 250))
    for x0, x1, top in ((150, 310, 200), (590, 710, 190)):
        toon(c, RRect(x0, top, x1, 300, 2), (200, 190, 200), w=1.6, shadow=None)
        for wx in range(x0 + 14, x1 - 20, 34):
            flat(c, RRect(wx, top + 20, wx + 18, top + 44, 2), (250, 230, 160))
    # buildings around the square
    def bld(x0, x1, top, wall, roof, seed):
        toon(c, RRect(x0, top, x1, 300, 2), wall, w=2)
        toon(c, Poly([(x0 - 10, top + 4), (x1 + 10, top + 4), ((x0 + x1) / 2, top - (x1 - x0) * 0.35)]), roof, w=2)
        for wx in range(int(x0) + 16, int(x1) - 20, 40):
            flat(c, RRect(wx, top + 30, wx + 22, top + 60, 3), (250, 230, 160))
    bld(-10, 160, 160, (230, 210, 180), (90, 120, 190), 1)
    bld(700, 910, 150, (220, 200, 170), (190, 80, 60), 2)
    # guild hall (centre back)
    toon(c, RRect(300, 90, 600, 300, 3), (210, 200, 196), w=2.4)
    toon(c, Poly([(280, 96), (620, 96), (450, 20)]), (120, 70, 150), w=2.4)
    toon(c, RRect(410, 200, 490, 300, 40), (110, 70, 50), w=2)
    for k, x in enumerate((340, 560)):
        col = (200, 60, 70) if not (k == 1 and "banner" in d) else (60, 160, 100)
        toon(c, Poly([(x - 22, 110), (x + 22, 110), (x + 22, 200), (x, 216), (x - 22, 200)]), col, w=1.6, shadow=None)
        flat(c, Poly(star_pts(x, 150, 12, 5)), (250, 210, 80))
    # plaza
    c.rect(0, 300, W, H, (210, 196, 170))
    for y in range(300, H, 26):
        for x in range((y // 26 % 2) * 26, W, 52):
            flat(c, RRect(x + 1, y + 1, x + 25, y + 25, 3), (220, 206, 180))
    # fountain
    toon(c, Ell(450, 400, 130, 40), (180, 180, 196), w=2)
    flat(c, Ell(450, 396, 112, 30), (110, 190, 240))
    toon(c, [RRect(436, 300, 464, 396, 4)], (190, 190, 206), w=1.6, shadow=None)
    statue = (190, 190, 206) if "statue" not in d else (220, 180, 80)
    toon(c, [Circ(450, 290, 14), Poly(star_pts(450, 260, 20, 8))], statue, w=1.4, shadow=None)
    # trade stalls
    for k, (x, col) in enumerate(((120, (230, 80, 80)), (780, (80, 150, 220)))):
        if k == 1 and "awning" in d:
            col = (250, 200, 60)
        toon(c, RRect(x - 70, 360, x + 70, 420, 3), (170, 120, 80), w=1.8)
        toon(c, Poly([(x - 80, 360), (x + 80, 360), (x + 70, 320), (x - 70, 320)]), col, w=1.8)
        for i in range(4):
            flat(c, Poly([(x - 80 + i * 40, 360), (x - 60 + i * 40, 360), (x - 56 + i * 35, 320), (x - 70 + i * 35, 320)]), (250, 250, 246))
        for i in range(3):
            toon(c, Circ(x - 40 + i * 40, 396, 12), [(250, 200, 60), (200, 90, 200), (90, 200, 120)][i], w=1.2, shadow=None)
    # players with name bars
    players = [(230, 470, (60, 110, 210), (240, 200, 90), (120, 220, 120)), (330, 520, (200, 60, 70), (40, 40, 50), (250, 250, 250)),
               (560, 500, (110, 70, 170), (250, 250, 250), (250, 200, 80)), (680, 470, (60, 160, 120), (150, 90, 40), (120, 220, 120)),
               (800, 540, (240, 140, 60), (90, 60, 40), (250, 250, 250)), (100, 540, (90, 90, 110), (230, 120, 160), (250, 200, 80))]
    for k, (x, y, outfit, hair, ncol) in enumerate(players):
        chibi(c, x, y, s=0.9, hair=hair, outfit=outfit, face=1 if x < 450 else -1, weapon="sword" if k % 2 else "staff")
        namebar(c, x, y - 110, ncol if not (k == 3 and "name" in d) else (250, 90, 90), 1980 + k)
    # pet next to a player
    if "pet" not in d:
        toon(c, [Ell(610, 530, 16, 12), Circ(624, 518, 10)], (250, 230, 160), w=1.2, shadow=None)
    # UI: chat box, skill bar, minimap
    toon(c, Circ(850, 50, 42), (220, 210, 180), w=2, shadow=None)
    flat(c, Circ(850, 50, 34), (170, 200, 140))
    flat(c, Circ(850, 50, 5), (250, 250, 250))
    flat(c, Circ(868, 36, 9), (250, 200, 60) if "marker" not in d else (220, 60, 60))
    panel(c, 280, 552, 620, 596, (40, 40, 56))
    icons = [(220, 80, 70), (90, 150, 220), (240, 200, 70), (90, 180, 100), (170, 120, 200), (240, 140, 60)]
    if "skill" in d:
        icons[3] = (250, 250, 250)
    for k, col in enumerate(icons):
        toon(c, RRect(290 + k * 54, 558, 332 + k * 54, 590, 5), col, w=1.2, shadow=None)
    toon(c, RRect(10, 6, 260, 80, 8), (20, 20, 30), w=1.2, shadow=None)
    for k in range(3):
        glyph_line(c, 20, 240 - k * 40, 22 + k * 20, [(250, 250, 250), (250, 200, 80), (120, 220, 120)][k], 1990 + k, w=1.6, size=8)


L198_ELEMENTS = [
    E("water", lambda c, m: [flat(c, Ell(450 + dx, 330, 4, 10), (200, 240, 255)) for dx in (-20, 20)], daynight="untinted",
      anim=dict(driftVelocity=(0, -40), driftLength=60, driftFade=True)),
    E("sparkle", lambda c, m: flat(c, Poly(star_pts(340, 420, 10, 2, points=4, rot=0)), (255, 255, 200)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.8)),
    E("levelup", lambda c, m: c.ellipse_ring(330, 520, 36, 10, 3, (250, 220, 90)), pivot=(330, 520), daynight="untinted",
      anim=dict(pulse=0.3, scaleSpeed=0.8, twinkle=0.5, twinkleSpeed=0.8)),
    E("bird", lambda c, m: flat(c, [Thick(200, 60, 210, 66, 2), Thick(210, 66, 220, 60, 2)], (80, 80, 100)), anim=drift_across(200, 220, 20, start=210)),
]

L198_DIFFS = [
    ("banner", 560, 160, 0),
    ("statue", 450, 268, 0),
    ("awning", 780, 340, 0),
    ("name", 680, 360, 0),
    ("pet", 615, 525, 0),
    ("marker", 870, 36, 0),
    ("skill", 473, 574, 0),
]


# =================================================================== Level 199 roguelike dungeon room
def l199_bg(c, d):
    c.rect(0, 0, W, H, (40, 34, 50))
    toon(c, RRect(30, 50, 870, 580, 6), (90, 80, 100), w=2.5, shadow=None)
    for j in range(80, 550, 40):
        for i in range(60, 840, 40):
            flat(c, RRect(i + 1, j + 1, i + 39, j + 39, 3), (110, 100, 116) if (i + j) // 40 % 2 else (104, 94, 110))
    # doors
    for x, y, w, h in ((420, 50, 60, 30), (420, 550, 60, 30), (30, 285, 30, 60), (840, 285, 30, 60)):
        toon(c, RRect(x, y, x + w, y + h, 4), (60, 44, 40), w=1.6, shadow=None)
    # shop rug with items
    toon(c, RRect(580, 100, 820, 220, 8), (150, 50, 70), w=1.6, shadow=None)
    for k, col in enumerate(((240, 90, 90), (90, 180, 240), (250, 200, 60))):
        x = 620 + k * 80
        if k == 1 and "shop" in d:
            col = (120, 220, 120)
        toon(c, Circ(x, 150, 16), col, w=1.4, shadow=None)
        flat(c, Circ(x - 12, 196, 6), (250, 200, 60))
        digits(c, x - 4, 190, str(15 + k * 5), (250, 250, 250), 2)
    # chest, statue, pots, spikes
    toon(c, [RRect(120, 120, 200, 170, 5), RRect(120, 104, 200, 124, 10)], (160, 100, 50) if "chest" not in d else (110, 110, 200), w=1.8)
    flat(c, RRect(154, 124, 166, 144, 2), (250, 200, 60))
    statue = (170, 166, 180) if "statue" not in d else (200, 140, 90)
    toon(c, [RRect(426, 250, 474, 290, 3), Circ(450, 232, 20)], statue, w=1.6)
    for k, (x, y) in enumerate(((100, 460), (140, 500), (780, 470))):
        if k == 1 and "pot" in d:
            flat(c, [Poly([(x - 14, y + 12), (x - 4, y - 2), (x + 2, y + 12)]), Poly([(x + 4, y + 12), (x + 12, y), (x + 16, y + 12)])], (190, 120, 80))
            continue
        toon(c, [Ell(x, y, 18, 20), RRect(x - 10, y - 26, x + 10, y - 16, 3)], (190, 120, 80), w=1.4)
    for i in range(4):
        for j in range(2):
            x, y = 300 + i * 30, 440 + j * 30
            toon(c, Poly([(x, y + 22), (x + 12, y), (x + 24, y + 22)]), (190, 190, 200), w=1, shadow=None)
    # slimes + hero
    for x, y, col in ((620, 380, (100, 200, 120)), (700, 420, (100, 200, 120))):
        toon(c, Poly([(x - 20, y + 10), (x + 20, y + 10), (x + 16, y - 6), (x, y - 20), (x - 16, y - 6)]), col, w=1.4)
        flat(c, [Circ(x - 6, y - 2, 3), Circ(x + 6, y - 2, 3)], (30, 30, 50))
    chibi(c, 450, 420, s=0.9, hair=(150, 90, 40), outfit=(60, 110, 210), face=1, weapon="sword")
    # HUD
    for k in range(4 if "hearts" not in d else 3):
        heart(c, 30 + k * 30, 22, 1.2, (240, 70, 90))
    for k, (col, n) in enumerate((((250, 200, 60), "23"), ((200, 200, 210), "2"), ((90, 90, 110), "1"))):
        flat(c, Circ(190 + k * 70, 22, 9), col)
        digits(c, 204 + k * 70, 14, n, (250, 250, 250), 3)
    for k in range(5):
        col = [(220, 80, 200), (90, 220, 240), (250, 160, 60), (120, 200, 90), (240, 90, 90)][k]
        if k == 2 and "relic" in d:
            col = (250, 250, 250)
        toon(c, Poly(ngon(420 + k * 34, 24, 13, 6, rot=30)), col, w=1.2, shadow=None)
    # room map
    for (i, j) in ((0, 1), (1, 1), (2, 1), (1, 0), (2, 0), (2, 2), (3, 1)):
        col = (250, 250, 250) if (i, j) == (2, 1) else (120, 120, 140)
        if (i, j) == (3, 1) and "map" in d:
            col = (250, 200, 60)
        flat(c, RRect(740 + i * 36, 2 + j * 15, 772 + i * 36, 15 + j * 15, 2), col)


L199_ELEMENTS = flame("torchL", 60, 90, s=1.2, glow_night=False) + flame("torchR", 840, 90, s=1.2, glow_night=False) + [
    E("glint", lambda c, m: flat(c, Poly(star_pts(186, 110, 9, 2, points=4, rot=0)), (255, 255, 220)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
    E("swing", lambda c, m: soft_union(c, [Poly([(470, 360), (520, 340), (510, 380)])], (255, 255, 255), 0.5, spread=6), pivot=(470, 370),
      daynight="untinted", anim=dict(blinkInterval=1.4, blinkDuration=0.3)),
]

L199_DIFFS = [
    ("shop", 700, 150, 0),
    ("chest", 160, 138, 0),
    ("statue", 450, 256, 0),
    ("pot", 140, 500, 0),
    ("hearts", 120, 22, 0),
    ("relic", 488, 24, 0),
    ("map", 864, 23, 0),
]


# =================================================================== Level 200 theme-park builder (isometric)
def l200_bg(c, d):
    c.rect(0, 0, W, H, (130, 200, 110))
    for k in range(-30, 80):
        flat(c, Thick(*P(k, -40), *P(k, 80), 1), (120, 188, 100))
        flat(c, Thick(*P(-40, k), *P(80, k), 1), (120, 188, 100))
    # paths
    flat(c, Poly([P(14, 4), P(16, 4), P(16, 40), P(14, 40)]), (220, 200, 160))
    flat(c, Poly([P(4, 20), P(40, 20), P(40, 22), P(4, 22)]), (220, 200, 160))
    objs = []
    # roller coaster (north-east): elevated loop track with supports
    track = [P(18 + 6 * math.cos(t / 12 * math.pi * 2), 10 + 4 * math.sin(t / 12 * math.pi * 2)) for t in range(13)]
    hts = [60 + 40 * math.sin(t / 12 * math.pi * 4) for t in range(13)]
    def coaster():
        for (x, y), h in zip(track, hts):
            flat(c, Thick(x, y, x, y - h, 3), (150, 150, 160))
        pts = [(x, y - h) for (x, y), h in zip(track, hts)]
        for a, b in zip(pts, pts[1:]):
            flat(c, Thick(a[0], a[1], b[0], b[1], 8), (220, 60, 60))
            flat(c, Thick(a[0], a[1], b[0], b[1], 3), (250, 200, 200))
        x, y = pts[3]
        toon(c, RRect(x - 22, y - 20, x + 22, y + 4, 5), (250, 200, 60) if "car" not in d else (90, 160, 230), w=1.2, shadow=None)
    objs.append((28, coaster))
    # carousel (west)
    def carousel():
        x, y = P(28, 20)
        toon(c, Ell(x, y, 60, 30), (230, 220, 200), w=1.6, shadow=None)
        for k in range(6):
            a = k * math.pi / 3
            flat(c, Thick(x + math.cos(a) * 40, y + math.sin(a) * 20, x + math.cos(a) * 40, y + math.sin(a) * 20 - 46, 2), (200, 160, 70))
        roof = (230, 80, 120) if "carousel" not in d else (80, 160, 230)
        toon(c, Poly([(x - 64, y - 50), (x + 64, y - 50), (x, y - 100)]), roof, w=1.8)
        for k in range(4):
            flat(c, Poly([(x - 64 + k * 32, y - 50), (x - 48 + k * 32, y - 50), (x, y - 100)]), (250, 250, 246))
    objs.append((44, carousel))
    def teacups():
        x, y = P(8, 14)
        toon(c, Ell(x, y, 70, 34), (200, 190, 220), w=1.6, shadow=None)
        for k, col in enumerate(((240, 120, 160), (120, 200, 240), (250, 210, 90), (150, 220, 140))):
            a = k * math.pi / 2 + 0.4
            cx, cy = x + math.cos(a) * 42, y + math.sin(a) * 18
            toon(c, [Ell(cx, cy - 6, 18, 9), RRect(cx - 14, cy - 6, cx + 14, cy + 8, 6)], col, w=1.2, shadow=None)
    objs.append((22, teacups))
    # ticket booth + balloon stand + food stalls (south)
    objs.append((40, lambda: iso_box(c, 17, 22, 1, 1, 34, (240, 200, 90) if "booth" not in d else (200, 120, 200))))
    objs.append((44, lambda: iso_house(c, 18, 25, (250, 240, 220), (220, 80, 80))))
    objs.append((46, lambda: iso_house(c, 20, 25, (250, 240, 220), (80, 140, 220))))
    def balloons():
        x, y = P(12.5, 24.5)
        flat(c, Thick(x, y, x, y - 40, 2), (90, 80, 70))
        for k, col in enumerate(((240, 80, 90), (250, 200, 60), (90, 180, 240))):
            toon(c, Ell(x - 18 + k * 18, y - 56 - (k % 2) * 10, 12, 15), col if not (k == 1 and "balloon" in d) else (120, 220, 120), w=1, shadow=None)
    objs.append((38, balloons))
    # fountain
    objs.append((37, lambda: (toon(c, Ell(*P(15, 21), 40, 20), (200, 200, 210), w=1.4, shadow=None),
                              flat(c, Ell(*P(15, 21), 30, 14), (90, 180, 240) if "fountain" not in d else (240, 120, 160)))))
    # trees
    for i, j in ((6, 14), (4, 18), (24, 20), (26, 24), (22, 30), (10, 32), (14, 34), (28, 16), (3, 26), (24, 8), (6, 34)):
        objs.append((i + j + 1, (lambda i, j: lambda: iso_tree(c, i, j, (70, 160, 80) if not ((i, j) == (24, 20) and "tree" in d) else (230, 140, 50)))(i, j)))
    for _, f in sorted(objs, key=lambda o: o[0]):
        f()
    # HUD
    toon(c, RRect(10, 8, 890, 44, 10), (40, 50, 80), w=1.6, shadow=None)
    flat(c, Circ(34, 26, 10), (250, 200, 60))
    digits(c, 54, 18, "48200", (250, 250, 250), 3)
    flat(c, Circ(250, 26, 10), (180, 220, 250))
    digits(c, 270, 18, "862", (250, 250, 250), 3)
    toon(c, RRect(830, 90, 888, 420, 12), (40, 50, 80), w=1.6, shadow=None)
    icons = [(220, 60, 60), (230, 80, 120), (240, 200, 90), (90, 180, 100), (90, 160, 230)]
    if "menu" in d:
        icons[1] = (250, 250, 250)
    for k, col in enumerate(icons):
        flat(c, RRect(838, 100 + k * 62, 880, 150 + k * 62, 8), (250, 240, 220))
        toon(c, Circ(859, 125 + k * 62, 12), col, w=1.2, shadow=None)


def wheel_el():
    x, y, r = 640, 300, 100

    def d(c, m):
        c.ellipse_ring(x, y, r, r, 5, (90, 140, 220))
        for k in range(8):
            a = math.radians(k * 45)
            flat(c, Thick(x, y, x + math.cos(a) * r, y + math.sin(a) * r, 2.4), (200, 200, 210))
            toon(c, Circ(x + math.cos(a) * r, y + math.sin(a) * r, 11), [(240, 80, 90), (250, 200, 60), (90, 200, 120), (170, 120, 220)][k % 4], w=1, shadow=None)
    return E("wheel", d, pivot=(x, y), anim=dict(rotateSpeed=14))


TW_, TH_ = 30, 15
L200_ELEMENTS = [
    E("wheelstand", lambda c, m: flat(c, [Thick(640, 300, 600, 420, 6), Thick(640, 300, 680, 420, 6)], (150, 150, 160))),
    wheel_el(),
] + [E("guest%d" % k, (lambda k: lambda c, m: toon(c, Circ(*P(15, 6 + k * 3), 5), [(240, 80, 90), (90, 160, 230), (250, 200, 60)][k % 3], w=1, shadow=None))(k),
       anim=dict(driftVelocity=(-TW_ * 0.6, -TH_ * 0.6), driftLength=200, phase=k / 4)) for k in range(4)] + [
    E("coasterflash", lambda c, m: flat(c, Poly(star_pts(560, 110, 10, 2, points=4, rot=0)), (255, 255, 230)), daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.7)),
]

L200_DIFFS = [
    ("car", 570, 228, 0),
    ("carousel", P(28, 20)[0], P(28, 20)[1] - 76, 0),
    ("booth", P(17.5, 22.5)[0], P(17.5, 22.5)[1] - 30, 0),
    ("balloon", P(12.5, 24.5)[0], P(12.5, 24.5)[1] - 60, 0),
    ("fountain", P(15, 21)[0], P(15, 21)[1], 0),
    ("tree", P(24.5, 20.5)[0], P(24.5, 20.5)[1] - 20, 0),
    ("menu", 859, 187, 0),
]


# =================================================================== Level 201 pool table
BALLS = [(250, 200, 40), (40, 90, 200), (220, 50, 50), (110, 50, 140), (240, 130, 40), (30, 140, 80), (140, 40, 40), (30, 30, 36)]


def ball(c, x, y, col, stripe=False, num=None):
    if stripe:
        toon(c, Circ(x, y, 15), (250, 250, 246), w=1.2, shadow=(0, 2, 3, 0.3))
        flat(c, RRect(x - 15, y - 7, x + 15, y + 7, 3), col)
    else:
        toon(c, Circ(x, y, 15), col, w=1.2, shadow=(0, 2, 3, 0.3))
    flat(c, Circ(x, y, 6), (250, 250, 246))
    flat(c, Circ(x - 5, y - 6, 3), (255, 255, 255))


def l201_bg(c, d):
    c.rect(0, 0, W, H, (50, 40, 50))
    for x in range(0, W, 40):
        flat(c, Thick(x, 0, x, H, 1), (56, 46, 56))
    toon(c, RRect(60, 90, 840, 520, 30), (120, 70, 40), w=3)
    flat(c, RRect(100, 130, 800, 480, 6), (40, 130, 90))
    for x, y in ((100, 130), (450, 124), (800, 130), (100, 480), (450, 486), (800, 480)):
        flat(c, Circ(x, y, 20), (20, 20, 26))
    for k in range(1, 8):
        for y in (110, 500):
            flat(c, Poly([(100 + k * 87.5, y - 4), (104 + k * 87.5, y), (100 + k * 87.5, y + 4), (96 + k * 87.5, y)]), (240, 230, 200))
    flat(c, Thick(275, 130, 275, 480, 1.4), (60, 150, 110))
    # racked balls (triangle)
    rack = [(0, 0), (1, -0.5), (1, 0.5), (2, -1), (2, 0), (2, 1), (3, -1.5), (3, -0.5), (3, 0.5), (3, 1.5), (4, -2), (4, -1), (4, 0), (4, 1), (4, 2)]
    for k, (i, j) in enumerate(rack):
        x, y = 560 + i * 27, 305 + j * 31
        col = BALLS[k % 8]
        stripe = k >= 8
        if k == 7:
            col = BALLS[7]
            stripe = False
        if k == 4 and "ball" in d:
            col = (240, 120, 200)
        if k == 11 and "stripe" in d:
            stripe = not stripe
        ball(c, x, y, col, stripe)
    ball(c, 220, 305, (250, 250, 246))
    # chalk + scoreboard + player panels
    toon(c, RRect(760, 500, 790, 524, 3), (60, 140, 220) if "chalk" not in d else (230, 90, 90), w=1.4, shadow=None)
    for k, x0 in enumerate((20, 520)):
        panel(c, x0, 14, x0 + 360, 72, (30, 30, 40))
        toon(c, Circ(x0 + 30, 43, 22), (60, 110, 210) if k == 0 else ((200, 60, 70) if "avatar" not in d else (90, 180, 110)), w=1.4, shadow=None)
        chibi(c, x0 + 30, 66, s=0.4, hair=(90, 60, 40), outfit=(60, 110, 210) if k == 0 else (200, 60, 70))
        for i in range(7):
            col = BALLS[i] if k == 0 else BALLS[i]
            flat(c, Circ(x0 + 80 + i * 26, 43, 9), col if i < (3 if k == 0 else 5) else (70, 70, 80))
    rack_col = (170, 110, 60) if "rack" not in d else (200, 60, 60)
    toon(c, Poly([(40, 590), (180, 590), (110, 536)]), rack_col, w=1.4, shadow=None)
    flat(c, Poly([(62, 582), (158, 582), (110, 546)]), (50, 40, 50))
    panel(c, 400, 540, 500, 590, (30, 30, 40))
    digits(c, 420, 552, "4", (250, 250, 250), 5)
    flat(c, Thick(448, 554, 456, 580, 2), (250, 250, 250))
    digits(c, 464, 552, "2", (250, 250, 250), 5)
    # power bar
    panel(c, 850, 140, 886, 470, (30, 30, 40))
    flat(c, RRect(856, 300, 880, 464, 4), (250, 140, 60))


L201_ELEMENTS = [
    E("cue", lambda c, m: (toon(c, Thick(40, 360, 196, 312, 7), (220, 190, 140), w=1.2, shadow=(0, 3, 4, 0.3)), flat(c, Thick(180, 317, 196, 312, 7), (240, 240, 246))),
      pivot=(220, 305), anim=dict(bobAmplitude=(-14, 4), bobSpeed=0.6)),
    E("aim", lambda c, m: [flat(c, Circ(236 + k * 24, 305, 2.4), (250, 250, 250)) for k in range(12)], daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=1.0)),
    E("lampglow", lambda c, m: soft_union(c, [Ell(450, 305, 300, 150)], (255, 250, 220), 0.12, spread=40), daynight="untinted", anim=dict(twinkle=0.3, twinkleSpeed=0.3)),
]

L201_DIFFS = [
    ("ball", 560 + 2 * 27, 305 - 31, 0),
    ("stripe", 560 + 4 * 27, 305 - 31, 0),
    ("chalk", 775, 512, 0),
    ("avatar", 550, 43, 0),
    ("rack", 110, 570, 0),
]


# =================================================================== Level 202 jigsaw
PZ, PX0, PY0 = 60, 220, 70


def piece_shape(x, y, s=PZ):
    return [RRect(x, y, x + s, y + s, 2), Circ(x + s, y + s / 2, s * 0.16), Circ(x + s / 2, y + s, s * 0.16)]


def l202_picture(c, x0, y0, s, d, clip=None):
    """The puzzle picture: sky, sun, mountains, lake, house; drawn in a 7x5 cell area of size s."""
    W_, H_ = 7 * s, 5 * s
    flat(c, RRect(x0, y0, x0 + W_, y0 + H_ * 0.5, 0), (130, 190, 240))
    flat(c, Circ(x0 + W_ * 0.8, y0 + H_ * 0.18, s * 0.45), (250, 220, 90) if "sun" not in d else (250, 130, 110))
    flat(c, Poly([(x0, y0 + H_ * 0.55), (x0 + W_ * 0.25, y0 + H_ * 0.18), (x0 + W_ * 0.5, y0 + H_ * 0.55)]), (110, 130, 170))
    flat(c, Poly([(x0 + W_ * 0.35, y0 + H_ * 0.55), (x0 + W_ * 0.6, y0 + H_ * 0.25), (x0 + W_ * 0.9, y0 + H_ * 0.55)]), (130, 150, 190))
    flat(c, RRect(x0, y0 + H_ * 0.5, x0 + W_, y0 + H_, 0), (110, 180, 100))
    flat(c, Ell(x0 + W_ * 0.3, y0 + H_ * 0.78, W_ * 0.22, H_ * 0.1), (90, 160, 220))
    hx, hy = x0 + W_ * 0.72, y0 + H_ * 0.62
    flat(c, RRect(hx, hy, hx + s * 1.2, hy + s * 0.9, 0), (240, 230, 210))
    flat(c, Poly([(hx - 8, hy + 2), (hx + s * 1.2 + 8, hy + 2), (hx + s * 0.6, hy - s * 0.6)]), (200, 70, 60) if "roof" not in d else (80, 120, 200))


def l202_bg(c, d):
    c.rect(0, 0, W, H, (170, 120, 80))
    for y in range(0, H, 30):
        flat(c, Thick(0, y, W, y, 1.4), (156, 108, 70))
    # board with the half-finished picture
    toon(c, RRect(PX0 - 10, PY0 - 10, PX0 + 7 * PZ + 10, PY0 + 5 * PZ + 10, 6), (240, 236, 226), w=2)
    l202_picture(c, PX0, PY0, PZ, d)
    missing = {(1, 0), (2, 0), (3, 0), (0, 1), (3, 1), (4, 1), (2, 3), (5, 4), (6, 4), (6, 3)}
    for (i, j) in missing:
        flat(c, RRect(PX0 + i * PZ, PY0 + j * PZ, PX0 + (i + 1) * PZ, PY0 + (j + 1) * PZ, 0), (230, 226, 216))
    for i in range(8):
        flat(c, Thick(PX0 + i * PZ, PY0, PX0 + i * PZ, PY0 + 5 * PZ, 1), (60, 60, 60, 0.25))
    for j in range(6):
        flat(c, Thick(PX0, PY0 + j * PZ, PX0 + 7 * PZ, PY0 + j * PZ, 1), (60, 60, 60, 0.25))
    # loose pieces around
    for k, (x, y, col) in enumerate(((60, 120, (130, 190, 240)), (110, 260, (110, 180, 100)), (60, 400, (130, 150, 190)), (760, 110, (130, 190, 240)),
                                     (780, 260, (90, 160, 220)), (720, 400, (110, 180, 100)), (360, 470, (130, 190, 240)), (520, 480, (110, 130, 170)))):
        if k == 5 and "piece" in d:
            col = (250, 220, 90)
        toon(c, piece_shape(x, y), col, w=1.4, shadow=(0, 3, 4, 0.3))
    # box lid with the picture
    toon(c, rot_poly(140, 540, 200, 110, -8), (240, 236, 226), w=2)
    flat(c, rot_poly(140, 540, 180, 90, -8), (130, 190, 240))
    flat(c, Poly([(56, 590), (230, 566), (236, 590)]), (110, 180, 100))
    flat(c, Poly([(60, 586), (130, 520), (190, 576)]), (110, 130, 170))
    flat(c, Circ(110, 520, 16), (250, 220, 90) if "lid" not in d else (240, 120, 160))
    # tea cup + coaster
    coaster = (90, 140, 200) if "coaster" not in d else (200, 90, 120)
    toon(c, Circ(820, 540, 44), coaster, w=1.6, shadow=None)
    toon(c, [Circ(820, 540, 30), Thick(850, 540, 870, 530, 6)], (250, 250, 246), w=1.6)
    flat(c, Circ(820, 540, 22), (170, 110, 60))
    # timer + counter
    panel(c, 330, 520, 570, 590, (60, 44, 40))
    digits(c, 350, 534, "1225", (250, 250, 250), 5)
    glyph_line(c, 480, 560, 556, (250, 250, 250), 2021, w=2, size=10)


L202_ELEMENTS = [
    E("steam%d" % k, (lambda k: lambda c, m: toon(c, Circ(820, 500, 7), (246, 246, 250), w=1, shadow=None))(k), anim=dict(driftVelocity=(4, 30), driftLength=70,
                                                                                                                       driftFade=True, driftGrow=1.4, phase=k / 3))
    for k in range(3)] + [
    E("held", lambda c, m: toon(c, piece_shape(560, 300), (130, 190, 240), w=1.4, shadow=(0, 8, 8, 0.3)), anim=dict(bobAmplitude=(10, 8), bobSpeed=0.3)),
    E("glow", lambda c, m: soft_union(c, [RRect(PX0 + 3 * PZ, PY0, PX0 + 4 * PZ, PY0 + PZ, 2)], (250, 250, 160), 0.4, spread=8), daynight="untinted",
      anim=dict(twinkle=0.7, twinkleSpeed=0.8)),
]

L202_DIFFS = [
    ("sun", PX0 + 7 * PZ * 0.8, PY0 + 5 * PZ * 0.18, 0),
    ("roof", PX0 + 7 * PZ * 0.72 + PZ * 0.6, PY0 + 5 * PZ * 0.62 - 10, 0),
    ("piece", 750, 430, 0),
    ("coaster", 820, 540, 0),
    ("lid", 110, 520, 0),
]


# =================================================================== Level 203 battle royale drop
def l203_bg(c, d):
    c.rect(0, 0, W, H, (60, 130, 190))
    island = Poly([(80, 120), (260, 50), (520, 70), (760, 60), (860, 200), (830, 400), (700, 560), (420, 580), (200, 540), (60, 380)])
    toon(c, island, (230, 210, 150), w=2.4, shadow=None)
    flat(c, Poly([(110, 140), (270, 80), (520, 100), (740, 90), (820, 210), (790, 390), (680, 530), (420, 550), (220, 510), (100, 370)]), (120, 180, 100))
    # river + bridge
    pts = [(300, 70), (330, 200), (300, 330), (360, 460), (330, 570)]
    for a, b in zip(pts, pts[1:]):
        flat(c, Thick(a[0], a[1], b[0], b[1], 22), (80, 150, 210))
    toon(c, rot_poly(312, 270, 60, 16, 10), (170, 130, 90) if "bridge" not in d else (200, 200, 210), w=1.4, shadow=None)
    # roads
    for a, b in (((120, 270), (800, 260)), ((500, 100), (520, 540))):
        flat(c, Thick(a[0], a[1], b[0], b[1], 8), (190, 180, 160))
    # towns (roof grids)
    for k, (cx, cy) in enumerate(((180, 200), (600, 180), (620, 420), (430, 380))):
        for i in range(3):
            for j in range(2):
                col = [(200, 80, 60), (90, 120, 190), (230, 200, 150)][(i + j + k) % 3]
                if k == 2 and (i, j) == (1, 0) and "roof" in d:
                    col = (250, 250, 250)
                toon(c, RRect(cx + i * 30 - 40, cy + j * 30 - 30, cx + i * 30 - 16, cy + j * 30 - 8, 2), col, w=1, shadow=None)
    # forests
    for x, y in ((240, 400), (260, 430), (220, 450), (700, 300), (720, 330), (740, 290), (420, 160), (440, 190)):
        if (x, y) == (720, 330) and "forest" in d:
            continue
        toon(c, Circ(x, y, 14), (60, 140, 70), w=1, shadow=None)
    # boat + airdrop crate
    toon(c, Poly([(120, 520), (170, 520), (160, 536), (128, 536)]), (250, 250, 246) if "boat" not in d else (230, 90, 90), w=1.2, shadow=None)
    toon(c, RRect(540, 300, 566, 326, 3), (230, 80, 60) if "crate" not in d else (90, 160, 230), w=1.4, shadow=None)
    flat(c, Thick(553, 300, 553, 326, 2), (250, 250, 250))
    # storm outside the safe zone + zone ring
    soft_union(c, [RRect(-10, -10, 910, 610, 0)], (150, 90, 200), 0.18, spread=1)
    c.ellipse_ring(480, 320, 220, 200, 4, (250, 250, 250))
    # flight path
    for k in range(0, 18, 2):
        flat(c, Thick(40 + k * 48, 40 + k * 10, 64 + k * 48, 45 + k * 10, 2), (250, 250, 250))
    # HUD
    panel(c, 740, 10, 890, 50, (20, 20, 30))
    glyph_line(c, 750, 810, 30, (250, 250, 250), 2031, w=2, size=9)
    digits(c, 820, 18, "64", (250, 250, 250), 4)
    stripe = (220, 60, 60) if "light" not in d else (60, 120, 220)
    toon(c, Poly([(70, 380), (94, 380), (88, 320), (76, 320)]), (250, 250, 246), w=1.4, shadow=None)
    flat(c, [RRect(72, 360, 92, 370, 0), RRect(75, 336, 89, 346, 0)], stripe)
    toon(c, [RRect(72, 306, 92, 322, 2), Poly([(70, 308), (94, 308), (82, 294)])], stripe, w=1.2, shadow=None)
    panel(c, 300, 10, 600, 40, (20, 20, 30))
    for k in range(11):
        flat(c, Thick(310 + k * 28, 18, 310 + k * 28, 32 if k % 3 else 24, 2), (250, 250, 250))


def chute(eid, x, y, col, ph):
    def d(c, m):
        toon(c, [Poly([(x - 24, y - 30), (x + 24, y - 30), (x + 18, y - 44), (x - 18, y - 44)])], col, w=1.2, shadow=None)
        flat(c, [Thick(x - 22, y - 30, x, y, 1), Thick(x + 22, y - 30, x, y, 1)], (250, 250, 250))
        toon(c, Circ(x, y + 4, 6), (240, 200, 90), w=1, shadow=None)
    return E(eid, d, anim=dict(bobAmplitude=(10, 12), bobSpeed=0.25, phase=ph))


L203_ELEMENTS = [chute("chute%d" % k, x, y, col, k * 0.2) for k, (x, y, col) in enumerate(((380, 260, (240, 80, 90)), (480, 470, (90, 200, 120)),
                                                                                            (690, 220, (250, 200, 60)), (200, 330, (120, 160, 240))))] + [
    E("plane", lambda c, m: toon(c, Poly([(60, 40), (100, 46), (60, 52), (66, 46)]), (220, 220, 230), w=1.2, shadow=None), anim=dict(driftVelocity=(48, -10), driftLength=860)),
    E("zonepulse", lambda c, m: c.ellipse_ring(480, 320, 220, 200, 2, (250, 250, 250)), pivot=(480, 320), daynight="untinted",
      anim=dict(pulse=0.03, scaleSpeed=0.5, twinkle=0.5, twinkleSpeed=0.5)),
]

L203_DIFFS = [
    ("bridge", 312, 270, 0),
    ("roof", 630, 400, 0),
    ("forest", 720, 330, 0),
    ("boat", 145, 528, 0),
    ("crate", 553, 313, 0),
    ("light", 82, 340, 0),
]


# =================================================================== Level 204 MOBA lane
def tower(c, x, y, team, crystal=None):
    col = (70, 130, 230) if team == 0 else (230, 70, 80)
    toon(c, [Ell(x, y, 34, 16)], (150, 146, 160), w=1.6, shadow=None)
    toon(c, Poly([(x - 22, y), (x + 22, y), (x + 14, y - 80), (x - 14, y - 80)]), (190, 186, 200), w=1.6)
    toon(c, Poly([(x, y - 124), (x + 14, y - 100), (x, y - 80), (x - 14, y - 100)]), crystal or col, w=1.6)


def l204_bg(c, d):
    c.rect(0, 0, W, H, (70, 120, 70))
    rnd = random.Random(2040)
    for _ in range(40):
        flat(c, Ell(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(20, 50), rnd.uniform(10, 20)), (80, 132, 78))
    # lane (diagonal) + river
    flat(c, Poly([(0, 520), (0, 600), (120, 600), (900, 120), (900, 20), (800, 20)]), (190, 170, 130))
    flat(c, Poly([(0, 120), (120, 0), (900, 500), (900, 620), (780, 620)]), (80, 150, 200))
    # jungle trees + bushes
    for x, y in ((80, 300), (140, 340), (200, 260), (700, 470), (760, 520), (820, 440), (620, 560), (260, 80), (320, 40)):
        toon(c, [Circ(x, y, 26), Circ(x + 18, y + 10, 18)], (40, 100, 50) if not ((x, y) == (760, 520) and "tree" in d) else (200, 140, 60), w=1.6)
    toon(c, Ell(560, 120, 60, 26), (60, 140, 60) if "bush" not in d else (130, 90, 160), w=1.6, shadow=None)
    # jungle camp monster
    camp = (170, 110, 200) if "camp" not in d else (240, 160, 60)
    toon(c, [Ell(160, 470, 34, 24), Poly([(140, 452), (130, 430), (150, 448)]), Poly([(180, 452), (190, 430), (170, 448)])], camp, w=1.6)
    flat(c, [Circ(150, 466, 4), Circ(170, 466, 4)], (250, 240, 120))
    # towers
    tower(c, 200, 520, 0)
    tower(c, 720, 170, 1, crystal=(230, 70, 80) if "crystal" not in d else (250, 220, 90))
    # minions
    for k in range(4):
        x, y = 340 + k * 26, 420 - k * 16
        toon(c, Circ(x, y, 9), (90, 150, 240), w=1.2, shadow=None)
    for k in range(4):
        x, y = 470 + k * 26, 340 - k * 16
        toon(c, Circ(x, y, 12), (240, 90, 90) if not (k == 2 and "minion" in d) else (250, 250, 250), w=1.2, shadow=None)
    # heroes with HP bars
    for x, y, outfit, hair, frac in ((380, 470, (60, 110, 210), (240, 200, 90), 0.8), (560, 300, (200, 60, 70), (40, 40, 50), 0.5)):
        chibi(c, x, y, s=0.8, hair=hair, outfit=outfit, face=1 if x < 450 else -1, weapon="sword")
        bar(c, x - 30, y - 104, x + 30, y - 96, frac, (90, 210, 110) if x < 450 else (240, 80, 90))
    # ward
    if "ward" not in d:
        toon(c, [Thick(640, 420, 640, 390, 3), Circ(640, 384, 8)], (250, 200, 60), w=1.2, shadow=None)
    # HUD: KDA, skill bar, minimap
    panel(c, 360, 6, 540, 40, (20, 20, 30))
    digits(c, 376, 14, "5", (250, 250, 250), 4)
    digits(c, 430, 14, "2", (250, 250, 250), 4)
    digits(c, 484, 14, "7", (250, 250, 250), 4)
    panel(c, 260, 540, 640, 596, (30, 30, 40))
    icons = [(220, 80, 70), (90, 150, 220), (240, 200, 70), (170, 120, 200)]
    if "skill" in d:
        icons[2] = (90, 200, 120)
    for k, col in enumerate(icons):
        toon(c, RRect(280 + k * 90, 548, 340 + k * 90, 590, 8), col, w=1.4, shadow=None)
    toon(c, RRect(760, 450, 890, 590, 6), (30, 40, 30), w=2, shadow=None)
    flat(c, Thick(770, 580, 880, 460, 6), (190, 170, 130))
    flat(c, Circ(800, 550, 5), (90, 150, 240))
    flat(c, Circ(850, 490, 9), (240, 90, 90) if "dot" not in d else (250, 220, 90))


L204_ELEMENTS = [
    E("cd", lambda c, m: soft_union(c, [RRect(370, 548, 430, 590, 8)], (0, 0, 0), 0.5, spread=1), daynight="untinted", anim=dict(twinkle=0.8, twinkleSpeed=0.3)),
    E("ripple", lambda c, m: [flat(c, Thick(x, y, x + 30, y + 16, 2), (150, 210, 250)) for x, y in ((100, 80), (420, 260), (700, 420))],
      anim=dict(driftVelocity=(20, -10), driftLength=40, driftFade=True)),
    E("glow", lambda c, m: soft_union(c, [Circ(200, 406, 16)], (120, 180, 255), 0.5, spread=20), daynight="untinted", anim=dict(pulse=0.2, scaleSpeed=0.8)),
]

L204_DIFFS = [
    ("tree", 770, 525, 0),
    ("bush", 560, 120, 0),
    ("camp", 160, 462, 0),
    ("crystal", 720, 68, 0),
    ("minion", 522, 308, 0),
    ("ward", 640, 400, 0),
    ("skill", 490, 569, 0),
    ("dot", 850, 490, 0),
]


LEVELS = [
    ("Level195", "隐藏物品", l195_bg, L195_ELEMENTS, L195_DIFFS, 60, OPTS),
    ("Level196", "竖版弹幕", l196_bg, L196_ELEMENTS, L196_DIFFS, 60, OPTS),
    ("Level197", "潜行博物馆", l197_bg, L197_ELEMENTS, L197_DIFFS, 60, OPTS),
    ("Level198", "MMO主城", l198_bg, L198_ELEMENTS, L198_DIFFS, 60, OPTS),
    ("Level199", "地牢肉鸽", l199_bg, L199_ELEMENTS, L199_DIFFS, 60, OPTS),
    ("Level200", "游乐园经营", l200_bg, L200_ELEMENTS, L200_DIFFS, 60, OPTS),
    ("Level201", "台球", l201_bg, L201_ELEMENTS, L201_DIFFS, 60, OPTS),
    ("Level202", "拼图", l202_bg, L202_ELEMENTS, L202_DIFFS, 60, OPTS),
    ("Level203", "大逃杀", l203_bg, L203_ELEMENTS, L203_DIFFS, 60, OPTS),
    ("Level204", "MOBA对线", l204_bg, L204_ELEMENTS, L204_DIFFS, 60, OPTS),
]
