# -*- coding: utf-8 -*-
"""Sports & competition part 2 (paper-craft, full-bleed, no real teams, leagues, brands or logos):
  Level215 排球馆     - an indoor volleyball match seen from behind the end line: tall net, blockers, referee stand
  Level216 乒乓球馆   - a table-tennis hall: barriers, blue table, two players, umpire with flip score, stands
  Level217 拳击擂台   - a boxing night: spotlit ring with ropes and corner posts, two boxers, referee, bell table
  Level218 冰球场     - an ice-hockey rink: boards and glass, goal, players with sticks, goalie, ice resurfacer
  Level219 公路自行车赛 - a road race climbing through hills: cyclists, roadside fans, team car, finish arch
  Level220 高尔夫球场 - a golf green: flag, bunker, pond, putting golfer, caddie, gallery, leaderboard, cart
  Level221 体操馆     - a gymnastics arena: balance beam, uneven bars, floor mat, judges' table, scoreboard
  Level222 马术障碍赛 - a show-jumping arena: striped fences, horse and rider over a jump, grandstand, clock
  Level223 射箭场     - an archery range: row of targets, archers at the line, wind flags, tents, scoreboard
  Level224 沙滩排球   - beach volleyball: sand court, net, players, parasols, lifeguard tower, sea and boats
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, bush, cloud_bg, cloud_el, drift_across, palm, sky, tree_pine, tree_round
from fills import far_ridge, far_round_trees, far_skyline
from levels_akiba import modern, sign_box
from levels_misc import seg_text, wrestler
from levels_modern import crowd, player
from levels_sports import ad_boards, dpiece, flash_el, racket, stands
from levels_festival import bunting

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (246, 214, 186)
DARK_SKIN = (170, 120, 90)
HOME, AWAY = (214, 56, 60), (56, 108, 206)


def arms_up(c, x, base, h, skin=SKIN):
    """Raised arms for a player() figure (blocking / cheering)."""
    flat(c, [Thick(x - 9 * h, base - 44 * h, x - 13 * h, base - 70 * h, 3.4 * h), Thick(x + 9 * h, base - 44 * h, x + 13 * h, base - 70 * h, 3.4 * h)], skin)
    flat(c, [Circ(x - 13 * h, base - 71 * h, 2.6 * h), Circ(x + 13 * h, base - 71 * h, 2.6 * h)], skin)


def banner(c, x, y, col, mark=(250, 250, 246), w=26, h=88, edge=False):
    (dpiece if edge else piece)(c, Poly([(x - w, y), (x + w, y), (x + w, y + h), (x, y + h + 16), (x - w, y + h)]), col, shadow=PROP)
    flat(c, Poly(star_pts(x, y + 36, 13, 5)), mark)
    flat(c, [Thick(x - 16, y + 68, x + 16, y + 68, 3), Thick(x - 12, y + 76, x + 12, y + 76, 3)], lit(col, 0.72))


def wood_floor(c, y0, col, line, seed, step=14, board=180):
    c.rect(0, y0, W, H, col)
    rnd = random.Random(seed)
    for y in range(int(y0), H, step):
        flat(c, Thick(0, y, W, y, 1), line)
        off = rnd.uniform(0, board)
        for x in range(-board, W + board, board):
            flat(c, Thick(x + off, y, x + off, y + step, 1), line)


def horse(c, x, base, s, col, mane=(60, 40, 30), jump=False, face=1):
    """Paper horse; jump=True tucks the legs up (over a fence)."""
    f = face
    leg = lit(col, 0.82)
    if jump:
        flat(c, [Thick(x + 24 * s * f, base - 40 * s, x + 40 * s * f, base - 56 * s, 5 * s), Thick(x + 18 * s * f, base - 40 * s, x + 36 * s * f, base - 46 * s, 5 * s),
                 Thick(x - 24 * s * f, base - 40 * s, x - 46 * s * f, base - 20 * s, 5 * s), Thick(x - 18 * s * f, base - 40 * s, x - 40 * s * f, base - 16 * s, 5 * s)], leg)
    else:
        for lx in (-24, -14, 16, 26):
            flat(c, RRect(x + lx * s * f - 3 * s, base - 36 * s, x + lx * s * f + 3 * s, base, 1), leg)
    piece(c, [Ell(x, base - 44 * s, 38 * s, 17 * s),
              Poly([(x + 16 * s * f, base - 54 * s), (x + 30 * s * f, base - 88 * s), (x + 46 * s * f, base - 86 * s), (x + 40 * s * f, base - 42 * s)]),
              Poly([(x + 28 * s * f, base - 90 * s), (x + 44 * s * f, base - 96 * s), (x + 68 * s * f, base - 70 * s), (x + 58 * s * f, base - 62 * s)]),
              Poly([(x + 32 * s * f, base - 92 * s), (x + 34 * s * f, base - 104 * s), (x + 40 * s * f, base - 94 * s)])], col, border=1.5, shadow=PROP)
    flat(c, [Thick(x + 28 * s * f, base - 88 * s, x + 18 * s * f, base - 52 * s, 5 * s), Thick(x - 36 * s * f, base - 48 * s, x - 48 * s * f, base - 22 * s, 5 * s)], mane)
    flat(c, Circ(x + 62 * s * f, base - 68 * s, 2 * s), lit(col, 0.6))
    flat(c, Circ(x + 42 * s * f, base - 86 * s, 1.6 * s), INK)
    return x, base - 58 * s


def boxer(c, x, base, trunks, gloves, h=1.0, flip=False, skin=SKIN):
    wrestler(c, x, base, trunks=trunks, h=h, flip=flip)
    k = -1 if flip else 1
    piece(c, [Circ(x + 40 * h * k, base - 62 * h, 9 * h), Circ(x - 34 * h * k, base - 52 * h, 9 * h)], gloves, border=1.2, shadow=SMALL)


def stick_player(c, x, base, jersey, helmet, h=1.0, stick=(160, 110, 70), face=1):
    """Ice-hockey skater: padded jersey, helmet, stick down to the ice."""
    flat(c, [RRect(x - 6 * h, base - 20 * h, x - 1 * h, base - 2 * h, 1), RRect(x + 1 * h, base - 20 * h, x + 6 * h, base - 2 * h, 1)], (40, 40, 50))
    flat(c, [Thick(x - 9 * h, base, x + 2 * h, base, 1.6 * h), Thick(x, base, x + 11 * h, base, 1.6 * h)], (200, 210, 220))
    piece(c, RRect(x - 8 * h, base - 28 * h, x + 8 * h, base - 18 * h, 2), (40, 40, 50), shadow=SMALL)
    piece(c, [RRect(x - 11 * h, base - 48 * h, x + 11 * h, base - 26 * h, 5), RRect(x - 15 * h, base - 46 * h, x + 15 * h, base - 38 * h, 3)], jersey, border=1.5,
          shadow=PROP)
    flat(c, Thick(x - 11 * h, base - 32 * h, x + 11 * h, base - 32 * h, 2 * h), (250, 250, 246))
    piece(c, Thick(x + 10 * h * face, base - 40 * h, x + 26 * h * face, base - 2 * h, 2.6 * h), stick, shadow=SMALL)
    flat(c, Thick(x + 26 * h * face, base - 2 * h, x + 36 * h * face, base - 2 * h, 3 * h), (40, 40, 50))
    hx, hy = x + 1 * h, base - 55 * h
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    piece(c, [Ell(hx, hy - 3 * h, 8.5 * h, 6.5 * h)], helmet, border=1, shadow=None)
    flat(c, Thick(hx + 3 * h * face, hy + 1 * h, hx + 8 * h * face, hy + 4 * h, 1.2), (60, 60, 70))
    flat(c, Circ(hx + 3 * h * face, hy, 1.1 * h), INK)


def cyclist(c, x, base, jersey, helmet, s=1.0, bike=(60, 60, 70), shorts=(40, 40, 50)):
    """Road cyclist riding right (two wheels, crouched)."""
    for wx in (x - 22 * s, x + 22 * s):
        c.ellipse_ring(wx, base - 12 * s, 12 * s, 12 * s, 2 * s, (40, 40, 46))
    flat(c, [Thick(x - 22 * s, base - 12 * s, x - 4 * s, base - 14 * s, 2 * s), Thick(x - 4 * s, base - 14 * s, x + 14 * s, base - 30 * s, 2 * s),
             Thick(x - 22 * s, base - 12 * s, x - 8 * s, base - 32 * s, 2 * s), Thick(x - 8 * s, base - 32 * s, x + 14 * s, base - 30 * s, 2 * s),
             Thick(x + 14 * s, base - 30 * s, x + 22 * s, base - 12 * s, 2 * s)], bike)
    flat(c, [Thick(x - 6 * s, base - 34 * s, x + 2 * s, base - 18 * s, 4 * s), Thick(x + 2 * s, base - 18 * s, x - 2 * s, base - 10 * s, 3.4 * s)], shorts)
    piece(c, Poly([(x - 10 * s, base - 36 * s), (x - 2 * s, base - 46 * s), (x + 14 * s, base - 42 * s), (x + 10 * s, base - 34 * s)]), jersey, border=1.2,
          shadow=SMALL)
    flat(c, Thick(x + 10 * s, base - 40 * s, x + 16 * s, base - 30 * s, 2.6 * s), SKIN)
    hx, hy = x + 18 * s, base - 46 * s
    flat(c, Circ(hx, hy, 5.5 * s), SKIN)
    piece(c, Ell(hx - 1 * s, hy - 3 * s, 7 * s, 4 * s), helmet, border=0.8, shadow=None)
    flat(c, Circ(hx + 3 * s, hy, 1 * s), INK)


def target_face(c, x, y, r, cols=None):
    cols = cols or [(250, 250, 246), (40, 40, 50), (60, 140, 220), (220, 60, 60), (250, 210, 60)]
    piece(c, Circ(x, y, r), cols[0], border=1.2, shadow=PROP)
    for k, col in enumerate(cols[1:]):
        flat(c, Circ(x, y, r * (0.8 - k * 0.2)), col)


def parasol(c, x, base, top, col, stripe=(250, 250, 246), w=60):
    flat(c, Thick(x, base, x, top, 2.4), (220, 220, 220))
    piece(c, Poly([(x - w, top + 18), (x + w, top + 18), (x, top - 10)]), col, border=1.5, shadow=PROP)
    flat(c, Poly([(x - w * 0.34, top + 18), (x + w * 0.34, top + 18), (x, top - 10)]), stripe)


# =================================================================== Level 215 volleyball hall
def l215_bg(c, d):
    c.rect(0, 0, W, 260, (44, 50, 76))
    for x in range(0, W + 60, 60):
        flat(c, [Thick(x, 0, x + 30, 30, 2), Thick(x + 60, 0, x + 30, 30, 2)], (72, 78, 106))
    flat(c, Thick(0, 30, W, 30, 3), (86, 92, 120))
    stands(c, 50, 232, 2151, col=(72, 78, 106), edge=True)
    banner(c, 66, 32, (60, 140, 90) if "banner" not in d else (240, 190, 60), edge=True)
    banner(c, 834, 32, (200, 60, 70), edge=True)
    # hanging scoreboard
    flat(c, [Thick(390, 0, 390, 24, 3), Thick(510, 0, 510, 24, 3)], (100, 106, 130))
    dpiece(c, RRect(340, 20, 560, 120, 6), (30, 32, 44))
    flat(c, RRect(352, 32, 548, 108, 3), (16, 18, 26))
    flat(c, RRect(362, 42, 418, 98, 3), HOME)
    flat(c, RRect(482, 42, 538, 98, 3), AWAY if "board" not in d else (90, 190, 110))
    seg_text(c, 376, 52, 36, "2", (250, 250, 250), width=4)
    seg_text(c, 496, 52, 36, "1", (250, 250, 250), width=4)
    seg_text(c, 432, 58, 26, "24", (255, 200, 60), width=3)
    ad_boards(c, 232, 260, 11)
    wood_floor(c, 260, (226, 168, 110), (210, 152, 96), 2152)
    # court (seen from behind the end line)
    flat(c, Poly([(240, 290), (660, 290), (830, 600), (70, 600)]), (230, 120, 70))
    flat(c, Poly([(200, 290), (700, 290), (700, 300), (200, 300)]), (60, 120, 190))
    ln = (250, 250, 246)
    flat(c, [Thick(240, 290, 70, 600, 3), Thick(660, 290, 830, 600, 3), Thick(240, 290, 660, 290, 3), Thick(176, 470, 724, 470, 3)], ln)
    # far team (behind the net): two blockers jumping, one setter
    for x, col in ((360, AWAY), (520, AWAY)):
        player(c, x, 320, col, shorts=(40, 40, 50), h=1.25, hair=(40, 30, 30))
        arms_up(c, x, 320, 1.25)
    player(c, 620, 300, AWAY, shorts=(40, 40, 50), h=1.05, skin=DARK_SKIN)
    # net + posts
    pad = (60, 120, 200) if "pad" not in d else (240, 160, 50)
    for x in (150, 750):
        piece(c, RRect(x - 5, 236, x + 5, 420, 1), (180, 186, 196), shadow=PROP)
        piece(c, RRect(x - 12, 330, x + 12, 418, 4), pad if x == 150 else (60, 120, 200), border=1.2, shadow=SMALL)
    for x in range(160, 742, 9):
        flat(c, Thick(x, 252, x, 330, 0.8), (30, 30, 36))
    for y in range(254, 330, 9):
        flat(c, Thick(156, y, 744, y, 0.8), (30, 30, 36))
    flat(c, RRect(154, 246, 746, 256, 1), (250, 250, 246))
    flat(c, RRect(154, 326, 746, 332, 1), (250, 250, 246))
    for x in (220, 680):
        for k in range(6):
            flat(c, RRect(x - 2, 200 + k * 12, x + 2, 212 + k * 12, 0), (220, 60, 60) if k % 2 else (250, 250, 246))
    # referee stand (right)
    piece(c, [Thick(790, 470, 800, 340, 4), Thick(850, 470, 840, 340, 4), Thick(794, 420, 846, 420, 3)], (220, 224, 232), shadow=PROP)
    piece(c, RRect(780, 320, 860, 344, 3), (60, 120, 200) if "chair" not in d else (220, 60, 60), border=1.2, shadow=SMALL)
    modern(c, 820, 324, (250, 250, 246), bottom=(40, 40, 50), hair=(60, 50, 50), h=1.3)
    # ball cart (left foreground)
    if "cart" not in d:
        piece(c, [RRect(24, 520, 120, 530, 2), Thick(30, 530, 30, 584, 3), Thick(114, 530, 114, 584, 3), Thick(24, 584, 120, 584, 3)], (150, 156, 170),
              shadow=PROP)
        for k in range(4):
            for j in range(2):
                piece(c, Circ(38 + k * 22 + j * 11, 510 - j * 16, 10), (250, 220, 70) if (k + j) % 2 else (60, 120, 200), shadow=SMALL)
    # water bottles crate (right foreground)
    crate = (60, 160, 110) if "bottle" not in d else (240, 120, 160)
    piece(c, RRect(810, 540, 896, 590, 4), crate, border=1.5, shadow=PROP)
    for k in range(4):
        flat(c, [RRect(818 + k * 20, 516, 832 + k * 20, 544, 4), RRect(822 + k * 20, 510, 828 + k * 20, 518, 1)], (190, 226, 246))
    # near team (back view)
    player(c, 260, 560, HOME, shorts=(250, 250, 246), h=2.1, number="4", hair=(90, 60, 40))
    player(c, 600, 600, HOME if "shirt" not in d else (250, 200, 60), shorts=(250, 250, 246), h=2.4, number="8", skin=DARK_SKIN)
    player(c, 440, 480, HOME, shorts=(250, 250, 246), h=1.7, number="1", hair=(200, 150, 80))


L215_ELEMENTS = [
    E("ball", lambda c, m: [piece(c, Circ(450, 210, 12), (250, 220, 70), shadow=SMALL), flat(c, Thick(440, 204, 458, 216, 2.4), (60, 120, 200))],
      pivot=(450, 222), anim=dict(bobAmplitude=(0, 30), bobSpeed=0.8)),
    flash_el("flash1", [(140, 120), (520, 170), (700, 90)], phase=0.0),
    flash_el("flash2", [(300, 90), (620, 200), (240, 200)], phase=0.5, interval=2.2),
    E("glow", lambda c, m: soft_union(c, [RRect(352, 32, 548, 108, 3)], (180, 200, 255), 0.2, spread=20), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=1.2)),
]

L215_DIFFS = [
    ("banner", 66, 84, 0),
    ("board", 510, 70, 0),
    ("pad", 150, 374, 0),
    ("chair", 820, 332, 0),
    ("cart", 72, 540, 0),
    ("bottle", 853, 560, 0),
    ("shirt", 600, 520, 0),
]


# =================================================================== Level 216 table-tennis hall
def l216_bg(c, d):
    c.rect(0, 0, W, 250, (36, 44, 70))
    for k, x in enumerate(range(60, W, 160)):
        flat(c, RRect(x - 40, 8, x + 40, 18, 3), (230, 236, 246))
        soft_union(c, [RRect(x - 40, 8, x + 40, 18, 3)], (220, 230, 255), 0.25, spread=16)
    stands(c, 40, 196, 2161, col=(64, 72, 100), edge=True)
    # big screen
    dpiece(c, RRect(330, 24, 570, 140, 5), (24, 26, 36))
    flat(c, RRect(342, 36, 558, 128, 3), (40, 90, 150))
    flat(c, [RRect(356, 50, 440, 66, 3), RRect(356, 76, 420, 92, 3)], (120, 170, 230))
    seg_text(c, 470, 52, 46, "11", (250, 250, 250) if "screen" not in d else (250, 200, 60), width=4.4)
    # side banners
    for k, x in enumerate((70, 830)):
        col = (220, 70, 90) if k == 0 else (60, 150, 110)
        if k == 1 and "banner" in d:
            col = (150, 100, 220)
        dpiece(c, RRect(x - 40, 40, x + 40, 170, 3), col)
        sign_box(c, x - 26, 56, x + 26, 156, lit(col, 0.8), 2162 + k)
    # dark blue floor
    c.rect(0, 196, W, H, (40, 70, 130))
    for x in range(-200, W + 200, 70):
        flat(c, Thick(x, 196, x + (x - 450) * 0.6, 600, 1), (46, 78, 140))
    # barriers (red panels) around the playing area
    for i, x in enumerate(range(-20, 920, 90)):
        col = (200, 50, 60)
        if i == 7 and "barrier" in d:
            col = (60, 170, 110)
        piece(c, RRect(x + 2, 214, x + 88, 256, 2), col, border=1.2, shadow=SMALL)
        glyph = random.Random(2163 + i)
        for j in range(3):
            flat(c, Thick(x + 16 + j * 22, 228 + glyph.uniform(-4, 4), x + 26 + j * 22, 242 + glyph.uniform(-4, 4), 2), (250, 230, 230))
    # red floor of the court
    flat(c, Poly([(150, 256), (750, 256), (860, 600), (40, 600)]), (190, 70, 70))
    # far player
    modern(c, 450, 330, (250, 200, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.4)
    racket(c, 470, 300, 486, 286, col=(150, 100, 60), head=(220, 50, 50))
    # table (perspective)
    flat(c, Poly([(270, 346), (630, 346), (690, 470), (210, 470)]), (30, 30, 40))
    piece(c, Poly([(280, 336), (620, 336), (680, 456), (220, 456)]), (40, 90, 170), border=2, shadow=PROP)
    flat(c, [Thick(280, 336, 220, 456, 3), Thick(620, 336, 680, 456, 3), Thick(280, 336, 620, 336, 3), Thick(220, 456, 680, 456, 3),
             Thick(450, 336, 450, 456, 2)], (250, 250, 246))
    for x in (240, 660):
        flat(c, RRect(x - 4, 456, x + 4, 520, 1), (60, 60, 70))
    net = (30, 30, 36)
    flat(c, RRect(244, 384, 656, 402, 1), (60, 60, 70, 0.7))
    for x in range(248, 654, 6):
        flat(c, Thick(x, 386, x, 400, 0.7), net)
    flat(c, RRect(244, 380, 656, 386, 1), (250, 250, 246) if "net" not in d else (250, 200, 60))
    # umpire table + flip score (left)
    piece(c, RRect(40, 300, 170, 360, 3), (60, 64, 80), border=1.5, shadow=PROP)
    modern(c, 104, 300, (40, 60, 110), bottom=(40, 60, 110), hair=(130, 130, 140), h=1.3, glasses=True)
    piece(c, RRect(60, 316, 100, 350, 2), (250, 250, 246), border=1, shadow=SMALL)
    piece(c, RRect(108, 316, 148, 350, 2), (250, 250, 246) if "flip" not in d else (250, 200, 60), border=1, shadow=SMALL)
    seg_text(c, 72, 322, 22, "9", (40, 40, 50), width=2.6)
    seg_text(c, 120, 322, 22, "7", (40, 40, 50), width=2.6)
    # towel box + ball box (right)
    towel = (250, 140, 40) if "towel" not in d else (90, 180, 220)
    piece(c, RRect(760, 300, 860, 352, 4), towel, border=1.5, shadow=PROP)
    piece(c, Poly([(774, 300), (846, 300), (838, 286), (782, 286)]), (250, 250, 246), shadow=SMALL)
    # coach chairs (near corners)
    for x in (70, 830):
        piece(c, [RRect(x - 34, 520, x + 34, 534, 3), RRect(x - 34, 470, x - 26, 534, 2), RRect(x - 30, 534, x - 24, 590, 1),
                  RRect(x + 24, 534, x + 30, 590, 1)], (60, 64, 80), shadow=PROP)
    modern(c, 840, 590, (220, 60, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=2.0)
    if "bag" not in d:
        piece(c, RRect(30, 548, 120, 590, 8), (40, 120, 90), border=1.5, shadow=PROP)
        flat(c, Thick(46, 552, 104, 552, 3), (250, 250, 246))
    # near player (back view, big)
    modern(c, 450, 610, (60, 110, 210) if "shirt" not in d else (240, 120, 180), bottom=(40, 40, 50), hair=(90, 60, 40), h=2.6)
    racket(c, 490, 520, 520, 490, col=(150, 100, 60), head=(40, 40, 50))


L216_ELEMENTS = [
    E("ball", lambda c, m: piece(c, Circ(400, 320, 6), (250, 160, 40), shadow=SMALL), pivot=(400, 320),
      anim=dict(bobAmplitude=(40, 24), bobSpeed=0.9)),
    flash_el("flash", [(140, 110), (620, 80), (760, 150), (260, 160)], interval=1.9),
    E("lamp", lambda c, m: soft_union(c, [RRect(342, 36, 558, 128, 3)], (160, 200, 255), 0.18, spread=20), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=1.1)),
]

L216_DIFFS = [
    ("screen", 495, 75, 0),
    ("banner", 830, 105, 0),
    ("barrier", 650, 235, 0),
    ("net", 450, 383, 0),
    ("flip", 128, 333, 0),
    ("towel", 810, 322, 0),
    ("bag", 75, 569, 0),
    ("shirt", 451, 540, 0),
]


# =================================================================== Level 217 boxing night
def l217_bg(c, d):
    c.rect(0, 0, W, H, (26, 24, 40))
    # dark stands with crowd, big screens on the sides
    dpiece(c, RRect(-10, 120, 910, 300, 0), (44, 40, 62), shadow=LAYER)
    crowd(c, -6, 906, 130, 10, 2171, dy=17, cols=[(90, 60, 70), (60, 70, 100), (120, 110, 120), (70, 60, 50), (140, 60, 60)])
    for k, x in enumerate((110, 790)):
        dpiece(c, RRect(x - 90, 20, x + 90, 120, 5), (20, 20, 30))
        scr = (40, 70, 130) if not (k == 1 and "screen" in d) else (150, 60, 140)
        flat(c, RRect(x - 80, 30, x + 80, 110, 3), scr)
        flat(c, [Circ(x - 30, 70, 20), Circ(x + 30, 70, 20)], lit(scr, 1.5))
    # lighting rig
    flat(c, [Thick(220, 30, 680, 30, 6), Thick(240, 30, 240, 0, 3), Thick(660, 30, 660, 0, 3)], (70, 70, 86))
    for k, x in enumerate((280, 380, 520, 620)):
        dpiece(c, RRect(x - 14, 30, x + 14, 52, 3), (40, 40, 50), shadow=SMALL)
        flat(c, Ell(x, 52, 10, 4), (255, 240, 200))
    # ring apron + floor
    c.rect(0, 300, W, H, (40, 36, 52))
    dpiece(c, Poly([(120, 400), (780, 400), (840, 520), (60, 520)]), (60, 90, 160), shadow=PROP)
    flat(c, Poly([(60, 520), (840, 520), (840, 560), (60, 560)]), (30, 50, 110))
    sign_box(c, 300, 528, 600, 552, (30, 50, 110), 2172, glyph=(250, 250, 246), vertical=False)
    flat(c, Poly([(150, 410), (750, 410), (800, 512), (100, 512)]), (226, 226, 232))
    # far corner posts + ropes
    corner = (220, 50, 60) if "corner" not in d else (250, 200, 60)
    for x, col in ((150, corner), (750, (50, 90, 200))):
        piece(c, RRect(x - 7, 300, x + 7, 412, 2), (200, 200, 206), shadow=SMALL)
        piece(c, RRect(x - 11, 306, x + 11, 380, 4), col, border=1, shadow=SMALL)
    rope_cols = [(220, 50, 60), (250, 250, 246), (50, 90, 200)]
    for k, y in enumerate((318, 344, 370)):
        flat(c, Thick(150, y, 750, y, 3), rope_cols[k])
    # boxers + referee inside the ring
    boxer(c, 340, 470, (220, 50, 60), (220, 50, 60) if "glove" not in d else (250, 250, 246), h=1.2)
    boxer(c, 560, 470, (50, 90, 200), (50, 90, 200), h=1.2, flip=True, skin=DARK_SKIN)
    modern(c, 450, 440, (250, 250, 246) if "ref" not in d else (250, 190, 60), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.4)
    flat(c, Thick(436, 394, 466, 394, 2), (30, 30, 36))
    # near ropes + near posts
    for k, y in enumerate((430, 462, 494)):
        flat(c, Thick(60, y + 20, 840, y + 20, 4), rope_cols[k])
    for x in (60, 840):
        piece(c, RRect(x - 9, 400, x + 9, 560, 2), (200, 200, 206), shadow=PROP)
        piece(c, RRect(x - 14, 420, x + 14, 520, 5), (250, 250, 246), border=1, shadow=SMALL)
    # judge / bell table (front)
    dpiece(c, RRect(330, 560, 640, 610, 4), (70, 60, 50), shadow=PROP)
    bell = (230, 180, 60) if "bell" not in d else (120, 200, 220)
    dpiece(c, half_dome_pts(560, 560, 24, 22), bell, shadow=SMALL)
    flat(c, Circ(560, 548, 5), lit(bell, 1.3))
    dpiece(c, RRect(380, 540, 460, 562, 3), (30, 30, 40), shadow=SMALL)
    seg_text(c, 392, 544, 14, "300", (250, 80, 60), width=2)
    # corner stools + buckets
    if "stool" not in d:
        dpiece(c, [RRect(220, 566, 300, 578, 3), RRect(230, 578, 238, 610, 1), RRect(282, 578, 290, 610, 1)], (200, 50, 60), shadow=PROP)
    dpiece(c, Poly([(120, 560), (160, 560), (154, 600), (126, 600)]), (230, 230, 236), shadow=SMALL)
    towel = (250, 250, 246) if "towel" not in d else (90, 200, 120)
    dpiece(c, Poly([(712, 540), (796, 540), (790, 600), (720, 600)]), towel, shadow=PROP)
    flat(c, Thick(716, 560, 792, 560, 3), (50, 90, 200))


def half_dome_pts(cx, base, rx, ry, n=12):
    return Poly([(cx + rx * math.cos(math.pi * k / n), base - ry * math.sin(math.pi * k / n)) for k in range(n + 1)])


def beam217(x0, x1):
    def d(c, m):
        soft_union(c, [Poly([(x0 - 14, 52), (x0 + 14, 52), (x1 + 90, 470), (x1 - 90, 470)])], (255, 244, 210), 0.12, spread=14)
    return d


L217_ELEMENTS = [
    E("beamL", beam217(380, 380), daynight="untinted", anim=dict(twinkle=0.25, twinkleSpeed=0.7)),
    E("beamR", beam217(520, 520), daynight="untinted", anim=dict(twinkle=0.25, twinkleSpeed=0.9, phase=0.5)),
    flash_el("flash", [(60, 200), (300, 160), (620, 180), (860, 240)], interval=1.5),
    E("lead", lambda c, m: piece(c, Circ(396, 410, 9), (220, 50, 60), border=1.2, shadow=SMALL), pivot=(380, 410),
      anim=dict(bobAmplitude=(10, 0), bobSpeed=1.4)),
]

L217_DIFFS = [
    ("screen", 790, 70, 0),
    ("corner", 150, 343, 0),
    ("ref", 450, 410, 0),
    ("glove", 380, 400, 0),
    ("bell", 560, 545, 0),
    ("stool", 260, 585, 0),
    ("towel", 754, 570, 0),
]


# =================================================================== Level 218 ice hockey rink
ICE = (232, 242, 250)


def l218_bg(c, d):
    c.rect(0, 0, W, 220, (54, 60, 86))
    stands(c, 20, 196, 2181, col=(80, 88, 116), edge=True)
    banner(c, 70, 0, (60, 120, 200), edge=True, h=70)
    banner(c, 830, 0, (220, 60, 70) if "banner" not in d else (250, 200, 60), edge=True, h=70)
    # hanging cube scoreboard
    flat(c, Thick(450, 0, 450, 16, 4), (100, 106, 130))
    dpiece(c, Poly([(360, 16), (540, 16), (560, 50), (560, 120), (340, 120), (340, 50)]), (30, 32, 44))
    flat(c, RRect(354, 56, 546, 112, 3), (16, 18, 26))
    seg_text(c, 368, 64, 36, "3", HOME, width=4)
    seg_text(c, 504, 64, 36, "2", AWAY, width=4)
    seg_text(c, 420, 66, 30, "14", (255, 200, 60), width=3)
    # boards with ads + glass
    for i, x in enumerate(range(-10, 910, 130)):
        col = [(250, 250, 246), (60, 150, 220), (250, 250, 246), (240, 120, 40), (250, 250, 246), (90, 180, 110), (250, 250, 246), (220, 60, 110)][i]
        if i == 5 and "ad" in d:
            col = (150, 100, 220)
        piece(c, RRect(x + 2, 214, x + 128, 250, 1), col, border=1, shadow=SMALL)
        sign_box(c, x + 18, 220, x + 112, 244, lit(col, 0.85), 2182 + i, glyph=(60, 60, 80) if col == (250, 250, 246) else (250, 250, 246), vertical=False)
    flat(c, RRect(-10, 196, 910, 214, 0), (200, 220, 236, 0.5))
    flat(c, Thick(-10, 214, 910, 214, 3), (220, 220, 60))
    # ice
    c.rect(0, 250, W, H, ICE)
    rnd = random.Random(2183)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(260, 600)
        flat(c, Thick(x, y, x + rnd.uniform(10, 40), y + rnd.uniform(-3, 3), 1), (214, 228, 240))
    flat(c, [RRect(300, 250, 312, 600, 0)], (60, 110, 210))
    flat(c, [RRect(0, 250, 6, 600, 0)], (220, 60, 60))
    c.ellipse_ring(560, 430, 70, 34, 3, (60, 110, 210))
    flat(c, Circ(560, 430, 6), (60, 110, 210))
    c.ellipse_ring(180, 520, 70, 30, 3, (220, 60, 60))
    # goal (right) with crease
    c.ellipse(820, 340, 56, 22, (150, 200, 240), ymax=340)
    flat(c, Thick(740, 340, 900, 340, 3), (220, 60, 60))
    goal = (220, 60, 60) if "goal" not in d else (60, 110, 210)
    piece(c, [Thick(780, 340, 780, 290, 4), Thick(860, 340, 860, 290, 4), Thick(780, 290, 860, 290, 4)], goal, shadow=SMALL)
    for x in range(784, 860, 8):
        flat(c, Thick(x, 292, x + 12, 334, 0.8), (240, 240, 246))
    for y in range(296, 338, 8):
        flat(c, Thick(782, y, 858, y, 0.8), (240, 240, 246))
    # goalie
    stick_player(c, 812, 352, (220, 60, 60), (250, 250, 246), h=1.3, face=-1)
    piece(c, [RRect(796, 330, 808, 352, 3), RRect(816, 330, 828, 352, 3)], (250, 250, 246), shadow=SMALL)
    # penalty box door + bench (left)
    piece(c, RRect(40, 256, 160, 320, 3), (40, 44, 60), border=1.5, shadow=PROP)
    flat(c, RRect(48, 262, 152, 290, 2), (170, 200, 220))
    for x in (70, 120):
        modern(c, x, 312, (60, 110, 210), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.1)
    door = (250, 250, 246) if "door" not in d else (250, 200, 60)
    piece(c, RRect(170, 256, 200, 320, 2), door, border=1, shadow=SMALL)
    # players
    stick_player(c, 640, 470, (220, 60, 60), (40, 40, 50), h=1.7, face=1)
    stick_player(c, 460, 420, (60, 110, 210) if "jersey" not in d else (250, 200, 60), (60, 110, 210), h=1.5, face=1)
    stick_player(c, 300, 560, (60, 110, 210), (250, 250, 246), h=2.0, face=1)
    # ice resurfacer parked at the gate (left foreground)
    zam = (60, 160, 120) if "zam" not in d else (240, 150, 40)
    piece(c, [RRect(20, 470, 170, 540, 6), RRect(120, 430, 170, 480, 4)], zam, border=1.5, shadow=PROP)
    flat(c, RRect(128, 438, 162, 462, 3), (190, 220, 240))
    flat(c, RRect(30, 480, 110, 504, 3), lit(zam, 1.25))
    for x in (50, 140):
        piece(c, Circ(x, 544, 14), (40, 40, 46), shadow=SMALL)
    # puck bucket (near right)
    if "bucket" not in d:
        piece(c, Poly([(820, 540), (880, 540), (872, 596), (828, 596)]), (240, 140, 40), border=1.5, shadow=PROP)
        for k in range(4):
            flat(c, Ell(830 + k * 13, 538, 7, 3), (30, 30, 36))


L218_ELEMENTS = [
    E("puck", lambda c, m: flat(c, Ell(700, 474, 9, 4), (20, 20, 26)), pivot=(700, 474), anim=dict(bobAmplitude=(50, 6), bobSpeed=0.5)),
    flash_el("flash", [(200, 90), (520, 150), (760, 100), (380, 180)], interval=2.0),
    E("shine", lambda c, m: [flat(c, Thick(x, y, x + 50, y, 2.5), (250, 252, 255)) for x, y in ((380, 300), (640, 560), (200, 420), (520, 520))],
      daynight="untinted", anim=dict(twinkle=0.6, twinkleSpeed=0.8)),
]

L218_DIFFS = [
    ("banner", 830, 44, 0),
    ("ad", 712, 232, 0),
    ("goal", 820, 305, 0),
    ("door", 185, 288, 0),
    ("jersey", 460, 380, 0),
    ("zam", 95, 485, 0),
    ("bucket", 850, 568, 0),
]


# =================================================================== Level 219 road cycling race
ROAD219 = [(0, 470), (180, 440), (380, 400), (560, 352), (740, 300), (910, 262)]


def road_y(x):
    for (x0, y0), (x1, y1) in zip(ROAD219, ROAD219[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return ROAD219[-1][1]


def l219_bg(c, d):
    sky(c, (110, 180, 236), (214, 234, 248), 220)
    cloud_bg(c, 160, 50, 0.7)
    cloud_bg(c, 600, 36, 0.5)
    far_ridge(c, 150, 40, (170, 196, 214), 2191)
    piece(c, hill_strip(170, [(30, 0.006, 0.2), (14, 0.02, 1.2)]), (140, 190, 120), shadow=LAYER)
    # hilltop village
    for k, x in enumerate((560, 610, 660, 720)):
        roof = [(200, 90, 70), (220, 120, 70), (190, 80, 80), (210, 100, 60)][k]
        if k == 0 and "roof" in d:
            roof = (60, 110, 200)
        piece(c, RRect(x - 22, 150, x + 22, 186, 1), (240, 232, 214), border=1.2, shadow=SMALL)
        piece(c, Poly([(x - 28, 152), (x + 28, 152), (x, 124)]), roof, border=1.2, shadow=SMALL)
        flat(c, RRect(x - 6, 166, x + 6, 186, 1), (120, 90, 70))
    piece(c, [RRect(500, 100, 520, 186, 1), Poly([(496, 102), (524, 102), (510, 74)])], (230, 224, 210), border=1.2, shadow=SMALL)
    far_round_trees(c, 220, 18, (100, 160, 100), 2192)
    piece(c, hill_strip(230, [(20, 0.008, 0.6), (10, 0.03, 2.0)]), (120, 180, 100), shadow=LAYER)
    # vineyard rows on the slope
    for k in range(7):
        y = 250 + k * 16
        flat(c, Thick(0, y + 30, 360 - k * 30, y, 3), (90, 150, 80))
    # road
    pts_top = [(x, y - 26) for x, y in ROAD219]
    pts_bot = [(x, y + 26) for x, y in reversed(ROAD219)]
    piece(c, Poly(pts_top + pts_bot), (120, 120, 130), shadow=LAYER)
    for (x0, y0), (x1, y1) in zip(ROAD219, ROAD219[1:]):
        flat(c, Thick(x0, y0, x1, y1, 2), (250, 250, 246))
    # meadow below
    piece(c, Poly([(0, 496)] + [(x, y + 26) for x, y in ROAD219] + [(910, 610), (0, 610)]), (110, 176, 90), shadow=None)
    # finish arch (top right)
    arch = (220, 60, 60) if "arch" not in d else (60, 160, 110)
    piece(c, [RRect(760, 170, 776, 296, 2), RRect(860, 140, 876, 262, 2), Poly([(756, 168), (880, 138), (880, 170), (756, 198)])], arch, border=1.5,
          shadow=PROP)
    sign_box(c, 782, 156, 856, 178, lit(arch, 0.8), 2193, vertical=False)
    # team car with bikes on the roof (behind the riders)
    car = (250, 250, 246) if "car" not in d else (250, 200, 60)
    piece(c, [RRect(110, 390, 230, 432, 8), Poly([(132, 392), (210, 392), (196, 370), (146, 370)])], car, border=1.5, shadow=PROP)
    flat(c, [RRect(150, 374, 172, 390, 2), RRect(178, 374, 196, 390, 2)], (150, 190, 220))
    for x in (136, 206):
        piece(c, Circ(x, 434, 10), (40, 40, 46), shadow=SMALL)
    for k, col in enumerate(((220, 60, 60), (60, 110, 210))):
        c.ellipse_ring(140 + k * 40, 356, 8, 8, 1.6, (40, 40, 46))
        c.ellipse_ring(164 + k * 40, 356, 8, 8, 1.6, (40, 40, 46))
        flat(c, Thick(140 + k * 40, 356, 164 + k * 40, 356, 1.6), col)
    # roadside fans (upper side of the road)
    for k, x in enumerate((300, 400, 470)):
        y = road_y(x) - 30
        top = [(250, 200, 60), (220, 60, 60), (60, 110, 210)][k]
        hx, hy = modern(c, x, y, top, bottom=(40, 40, 50), hair=(40, 30, 30), h=1.2)
    fx, fy = 470, road_y(470) - 30
    flat(c, Thick(fx + 10, fy - 40, fx + 10, fy - 84, 1.6), (220, 220, 220))
    flag = (250, 250, 246) if "flag" not in d else (240, 120, 180)
    piece(c, Poly([(fx + 10, fy - 84), (fx + 48, fy - 76), (fx + 10, fy - 64)]), flag, shadow=SMALL)
    # roadside fans (lower side)
    for k, x in enumerate((560, 640)):
        y = road_y(x) + 70
        modern(c, x, y, [(90, 180, 110), (240, 140, 40)][k], bottom=(40, 40, 50), hair=(90, 60, 40), h=1.5)
    # riders (lead group)
    cyclist(c, 600, road_y(600) + 10, (250, 220, 60), (250, 250, 246), s=1.3)
    jc = (220, 60, 60) if "jersey" not in d else (90, 200, 220)
    cyclist(c, 470, road_y(470) + 14, jc, jc, s=1.4, shorts=(40, 40, 50) if "jersey" not in d else (60, 110, 210))
    cyclist(c, 360, road_y(360) + 12, (60, 110, 210), (60, 110, 210), s=1.45)
    cyclist(c, 250, road_y(250) + 16, (90, 180, 110), (250, 250, 246), s=1.5)
    # camera motorbike (front)
    moto = (40, 40, 50) if "moto" not in d else (220, 60, 60)
    for wx in (40, 110):
        piece(c, Circ(wx, 520, 16), (40, 40, 46), shadow=SMALL)
        flat(c, Circ(wx, 520, 6), (160, 160, 170))
    piece(c, Poly([(36, 506), (120, 506), (110, 482), (56, 482)]), moto, border=1.2, shadow=PROP)
    modern(c, 70, 486, (250, 250, 246), bottom=(40, 40, 50), hair=(40, 30, 30), h=1.2)
    modern(c, 100, 482, (60, 60, 70), bottom=(40, 40, 50), hair=(90, 60, 40), h=1.2)
    piece(c, RRect(104, 424, 128, 440, 2), (40, 40, 50), shadow=SMALL)
    # foreground: hay bales + flowers + tree
    for k, x in enumerate((300, 380)):
        piece(c, Ell(x, 570, 40, 24), (230, 196, 110) if not (k == 1 and "hay" in d) else (150, 200, 110), border=1.5, shadow=PROP)
        c.ellipse_ring(x, 570, 26, 14, 2, (200, 160, 80))
    tree_round(c, 820, 600, s=1.6, col=(80, 150, 80))
    if "tree" not in d:
        tree_round(c, 700, 600, s=1.1, col=(100, 170, 90))
    rnd = random.Random(2194)
    for _ in range(26):
        x, y = rnd.uniform(440, 660), rnd.uniform(560, 596)
        flat(c, Circ(x, y, 3.4), rnd.choice([(250, 250, 246), (250, 200, 60), (240, 120, 160)]))


L219_ELEMENTS = [
    cloud_el("cloud", 360, 40, 0.5, 8),
    bird_el("bird", 300, 80, s=8, speed=18),
    E("heli", lambda c, m: [piece(c, [Ell(250, 70, 24, 11), Thick(226, 70, 190, 64, 3)], (60, 60, 70), shadow=SMALL),
                            flat(c, Thick(220, 56, 280, 56, 2), (40, 40, 46))], pivot=(250, 70), anim=dict(bobAmplitude=(0, 5), bobSpeed=0.6)),
    E("wave", lambda c, m: flat(c, [Thick(658, 425, 676, 400, 3)], SKIN), pivot=(658, 425), anim=dict(swingAngle=25, swingSpeed=1.0)),
]

L219_DIFFS = [
    ("roof", 560, 150, 0),
    ("arch", 818, 205, 0),
    ("car", 170, 400, 0),
    ("flag", 498, 266, 0),
    ("jersey", 472, 380, 0),
    ("hay", 380, 570, 0),
    ("tree", 700, 560, 0),
]


# =================================================================== Level 220 golf green
def l220_bg(c, d):
    sky(c, (120, 186, 238), (214, 234, 248), 150)
    cloud_bg(c, 700, 40, 0.6)
    far_ridge(c, 110, 30, (176, 200, 216), 2201)
    # clubhouse
    piece(c, RRect(360, 80, 520, 130, 1), (240, 234, 220), border=1.5, shadow=PROP)
    piece(c, Poly([(350, 82), (530, 82), (500, 56), (380, 56)]), (110, 80, 70), border=1.5, shadow=PROP)
    for k in range(5):
        flat(c, RRect(372 + k * 30, 94, 390 + k * 30, 114, 1), (170, 200, 220))
    far_round_trees(c, 140, 26, (80, 140, 90), 2202)
    # fairway + rough
    c.rect(0, 150, W, H, (90, 160, 80))
    flat(c, Poly([(200, 150), (700, 150), (900, 330), (0, 330)]), (110, 186, 96))
    for k in range(8):
        flat(c, Poly([(200 + k * 62, 150), (231 + k * 62, 150), (k * 112 + 56, 330), (k * 112, 330)]), (118, 194, 104))
    # leaderboard (left)
    piece(c, [RRect(20, 60, 200, 210, 3), RRect(50, 210, 60, 280, 1), RRect(160, 210, 170, 280, 1)], (40, 100, 70), border=1.5, shadow=PROP)
    for r in range(5):
        col = (250, 250, 246) if not (r == 2 and "board" in d) else (250, 200, 60)
        flat(c, RRect(32, 74 + r * 26, 140, 92 + r * 26, 2), col)
        seg_text(c, 150, 74 + r * 26, 16, "-%d" % (8 - r), (220, 60, 60), width=2)
    # pond with a fountain + duck
    flat(c, Ell(760, 250, 140, 36), (80, 150, 210))
    flat(c, Ell(760, 244, 110, 22), (110, 180, 230))
    if "duck" not in d:
        piece(c, [Ell(700, 246, 14, 8), Circ(712, 236, 6)], (250, 250, 246), shadow=SMALL)
        flat(c, Poly([(717, 236), (726, 238), (717, 240)]), (250, 160, 40))
    # bunker
    piece(c, Ell(180, 380, 130, 40), (236, 214, 160), border=1.5, shadow=None)
    flat(c, [Thick(110, 380, 240, 372, 1.4), Thick(120, 392, 250, 384, 1.4)], (220, 196, 140))
    rake = (220, 60, 60) if "rake" not in d else (60, 110, 210)
    flat(c, [Thick(200, 360, 290, 330, 2.4)], rake)
    flat(c, Thick(190, 352, 204, 372, 4), rake)
    # green
    piece(c, Ell(520, 420, 260, 90), (130, 206, 110), border=1.5, shadow=None)
    for k in range(5):
        c.ellipse_ring(520, 420, 260 - k * 48, 90 - k * 16, 1.2, (140, 214, 120))
    # gallery behind the ropes (top)
    for x in range(30, 900, 50):
        flat(c, Thick(x, 314, x, 336, 2), (240, 240, 236))
    flat(c, Thick(0, 318, W, 318, 1.6), (240, 240, 236))
    for k, x in enumerate(range(250, 680, 46)):
        top = [(250, 250, 246), (60, 110, 210), (220, 60, 60), (250, 200, 60), (90, 180, 110), (240, 140, 180)][k % 6]
        modern(c, x, 312, top, bottom=(60, 70, 100), hair=(40, 30, 30) if k % 2 else (200, 150, 80), h=1.0)
    umb = (250, 200, 60) if "umbrella" not in d else (150, 100, 220)
    parasol(c, 430, 270, 230, umb, w=40)
    # flag + hole
    flat(c, Ell(640, 410, 9, 4), (30, 40, 30))
    flat(c, Thick(640, 410, 640, 300, 2.4), (250, 250, 246))
    flag = (220, 60, 60) if "flag" not in d else (250, 200, 60)
    piece(c, Poly([(642, 300), (690, 314), (642, 330)]), flag, shadow=SMALL)
    # golfer putting
    modern(c, 450, 470, (250, 250, 246), bottom=(40, 60, 110), hair=(90, 60, 40), h=1.8)
    flat(c, Thick(462, 420, 480, 470, 2.4), (180, 180, 190))
    # caddie with the bag (right)
    modern(c, 780, 520, (60, 110, 80), bottom=(250, 250, 246), hair=(40, 30, 30), h=1.9)
    bag = (60, 110, 210) if "bag" not in d else (220, 60, 60)
    piece(c, RRect(808, 430, 840, 520, 6), bag, border=1.5, shadow=PROP)
    for k in range(3):
        flat(c, Thick(814 + k * 10, 430, 812 + k * 12, 400, 2.4), (200, 200, 210))
    # golf cart (left foreground)
    cart = (250, 250, 246) if "cart" not in d else (90, 180, 110)
    piece(c, [RRect(20, 500, 200, 560, 8), RRect(40, 440, 50, 500, 1), RRect(170, 440, 180, 500, 1), RRect(30, 430, 190, 446, 3)], cart, border=1.5,
          shadow=PROP)
    flat(c, RRect(60, 470, 150, 500, 4), (60, 60, 70))
    for x in (56, 166):
        piece(c, Circ(x, 564, 16), (40, 40, 46), shadow=SMALL)
    # foreground flowers
    rnd = random.Random(2203)
    for _ in range(40):
        x, y = rnd.uniform(240, 900), rnd.uniform(560, 600)
        flat(c, Circ(x, y, 3.2), rnd.choice([(250, 250, 246), (250, 200, 60), (240, 120, 160)]))


L220_ELEMENTS = [
    E("ball", lambda c, m: piece(c, Circ(520, 452, 5), (250, 250, 250), shadow=SMALL), pivot=(520, 452), anim=dict(bobAmplitude=(60, 0), bobSpeed=0.3)),
    E("fountain", lambda c, m: [flat(c, Thick(800, 244, 800 + k * 6, 214, 2), (220, 240, 255)) for k in (-2, -1, 0, 1, 2)], pivot=(800, 244),
      daynight="untinted", anim=dict(stretch=(0, 0.2), scaleSpeed=2.0)),
    E("pennant", lambda c, m: flat(c, Poly([(42, 60), (42, 30), (70, 45)]), (250, 200, 60)), pivot=(42, 45), anim=dict(stretch=(0.2, 0), scaleSpeed=1.5)),
    bird_el("bird", 560, 40, s=8, speed=-20),
    cloud_el("cloud", 300, 30, 0.45, 7),
]

L220_DIFFS = [
    ("board", 86, 135, 0),
    ("duck", 710, 242, 0),
    ("rake", 240, 350, 0),
    ("umbrella", 430, 236, 0),
    ("flag", 664, 315, 0),
    ("bag", 824, 470, 0),
    ("cart", 110, 500, 0),
]


# =================================================================== Level 221 gymnastics arena
def gymnast(c, x, base, leotard, h=1.0, pose="stand", hair=(60, 40, 30)):
    if pose == "arabesque":
        flat(c, [Thick(x, base, x, base - 24 * h, 3.6 * h), Thick(x, base - 24 * h, x - 26 * h, base - 34 * h, 3.6 * h)], SKIN)
        piece(c, Ell(x, base - 34 * h, 7 * h, 12 * h), leotard, border=1.2, shadow=SMALL)
        flat(c, [Thick(x, base - 42 * h, x + 18 * h, base - 56 * h, 2.6 * h), Thick(x, base - 42 * h, x - 16 * h, base - 54 * h, 2.6 * h)], SKIN)
        hx, hy = x + 3 * h, base - 52 * h
    else:
        flat(c, [Thick(x - 3 * h, base, x - 2 * h, base - 24 * h, 3.6 * h), Thick(x + 3 * h, base, x + 2 * h, base - 24 * h, 3.6 * h)], SKIN)
        piece(c, Ell(x, base - 34 * h, 7 * h, 12 * h), leotard, border=1.2, shadow=SMALL)
        flat(c, [Thick(x - 5 * h, base - 42 * h, x - 12 * h, base - 62 * h, 2.6 * h), Thick(x + 5 * h, base - 42 * h, x + 12 * h, base - 62 * h, 2.6 * h)], SKIN)
        hx, hy = x, base - 52 * h
    flat(c, Circ(hx, hy, 6 * h), SKIN)
    flat(c, [Ell(hx - 1 * h, hy - 4 * h, 7 * h, 3.4 * h), Circ(hx - 6 * h, hy - 4 * h, 3 * h)], hair)
    flat(c, Circ(hx + 2.5 * h, hy, 1 * h), INK)


def l221_bg(c, d):
    c.rect(0, 0, W, 240, (50, 56, 84))
    stands(c, 30, 214, 2211, col=(80, 88, 118), edge=True)
    # scoreboard
    dpiece(c, RRect(330, 16, 570, 120, 5), (24, 26, 36))
    flat(c, RRect(342, 28, 558, 108, 3), (30, 40, 70))
    flat(c, [RRect(354, 40, 470, 56, 3), RRect(354, 68, 440, 84, 3)], (130, 160, 220))
    flat(c, [RRect(354, 40, 470, 56, 3), RRect(354, 68, 440, 84, 3)], (130, 160, 220) if "score" not in d else (240, 150, 80))
    seg_text(c, 486, 40, 30, "14", (250, 200, 60), width=3.4)
    seg_text(c, 486, 76, 20, "850", (250, 250, 250), width=2.4)
    banner(c, 70, 20, (150, 80, 180), edge=True)
    banner(c, 830, 20, (60, 150, 200), edge=True)
    ad_boards(c, 214, 240, 7)
    # blue podium floor
    c.rect(0, 240, W, H, (60, 90, 160))
    # floor exercise mat (left)
    mat = (70, 120, 200)
    flat(c, Poly([(20, 270), (360, 270), (400, 460), (-20, 460)]), mat)
    flat(c, Poly([(40, 280), (342, 280), (376, 448), (6, 448)]), (90, 140, 220))
    flat(c, [Thick(40, 280, 6, 448, 2), Thick(342, 280, 376, 448, 2)], (250, 250, 246))
    # balance beam (centre)
    beam = (226, 196, 150)
    piece(c, [RRect(440, 300, 720, 312, 3)], beam, border=1.5, shadow=PROP)
    for x in (470, 690):
        piece(c, [Thick(x, 312, x - 20, 392, 4), Thick(x, 312, x + 20, 392, 4)], (120, 120, 136), shadow=SMALL)
    piece(c, RRect(420, 392, 740, 420, 4), (60, 120, 200), border=1.2, shadow=SMALL)
    gymnast(c, 590, 300, (220, 60, 120) if "leo" not in d else (60, 180, 200), h=1.6, pose="arabesque")
    # uneven bars (right)
    bars = (226, 226, 236)
    piece(c, [RRect(780, 200, 788, 420, 1), RRect(868, 240, 876, 420, 1), Thick(784, 210, 872, 210, 4), Thick(784, 290, 872, 290, 4)], bars,
          shadow=PROP)
    for x in (784, 872):
        flat(c, [Thick(x, 420, x - 26, 440, 3), Thick(x, 420, x + 26, 440, 3)], (120, 120, 136))
    piece(c, RRect(770, 424, 890, 456, 4), (60, 120, 200) if "barmat" not in d else (240, 160, 50), shadow=SMALL)
    # gymnast on the floor (cartwheel pose)
    flat(c, [Thick(180, 380, 170, 420, 3.4), Thick(180, 380, 200, 418, 3.4), Thick(180, 380, 160, 340, 3.4), Thick(180, 380, 210, 344, 3.4)], SKIN)
    piece(c, Ell(180, 380, 10, 16), (90, 200, 160) if "mat" not in d else (240, 200, 60), border=1.2, shadow=SMALL)
    flat(c, Circ(184, 400, 6), SKIN)
    # judges' table (front)
    piece(c, RRect(200, 500, 700, 560, 4), (240, 240, 246), border=1.5, shadow=PROP)
    flat(c, RRect(200, 500, 700, 512, 2), (60, 90, 160))
    for k, x in enumerate((270, 380, 520, 630)):
        modern(c, x, 500, (40, 40, 56), bottom=(40, 40, 56), hair=[(40, 30, 30), (130, 130, 140), (90, 60, 40), (200, 150, 80)][k], h=1.4,
               glasses=k % 2 == 0)
        card = (250, 250, 246) if not (k == 2 and "card" in d) else (250, 200, 60)
        piece(c, RRect(x - 22, 520, x + 22, 548, 2), card, border=1, shadow=SMALL)
        seg_text(c, x - 14, 524, 18, "9.%d" % (k + 4), (40, 40, 50), width=2)
    # chalk bowl (left foreground)
    if "chalk" not in d:
        piece(c, [Ell(70, 520, 46, 14), RRect(60, 520, 80, 586, 2), Ell(70, 590, 30, 8)], (200, 200, 210), shadow=PROP)
        flat(c, Ell(70, 516, 38, 9), (250, 250, 250))
    # coach (right foreground)
    modern(c, 820, 600, (220, 60, 70), bottom=(40, 40, 56), hair=(40, 30, 30), h=2.2)
    piece(c, RRect(844, 520, 870, 560, 3), (250, 250, 246), border=1, shadow=SMALL)


L221_ELEMENTS = [
    E("swing", lambda c, m: [flat(c, [Thick(828, 210, 828, 254, 3.4)], SKIN), piece(c, Ell(828, 270, 8, 16), (60, 120, 220), border=1.2, shadow=SMALL),
                             flat(c, Circ(828, 292, 6), SKIN)], pivot=(828, 210), anim=dict(swingAngle=35, swingSpeed=0.5)),
    flash_el("flash", [(120, 110), (300, 160), (640, 100), (760, 170)], interval=1.8),
    E("ribbon", lambda c, m: flat(c, [Thick(210, 344, 260, 320, 2), Thick(260, 320, 300, 344, 2)], (240, 80, 140)), pivot=(210, 344),
      anim=dict(swingAngle=20, swingSpeed=1.0)),
]

L221_DIFFS = [
    ("score", 412, 62, 0),
    ("mat", 180, 380, 0),
    ("leo", 590, 268, 0),
    ("barmat", 830, 440, 0),
    ("card", 520, 534, 0),
    ("chalk", 70, 550, 0),
]


# =================================================================== Level 222 show jumping
def fence(c, x, base, w, h, a, b, wing=(250, 250, 246), rails=2):
    for wx in (x, x + w):
        piece(c, [RRect(wx - 6, base - h - 14, wx + 6, base, 1)], wing, border=1, shadow=SMALL)
        flat(c, Poly([(wx - 6, base - h - 14), (wx + 6, base - h - 14), (wx, base - h - 22)]), wing)
    for r in range(rails):
        y = base - h + r * (h / rails)
        piece(c, RRect(x, y, x + w, y + 6, 2), a, shadow=SMALL)
        for k in range(int(w // 24)):
            if k % 2:
                flat(c, RRect(x + k * 24, y, x + k * 24 + 24, y + 6, 0), b)


def l222_bg(c, d):
    sky(c, (120, 186, 238), (214, 234, 248), 160)
    cloud_bg(c, 160, 40, 0.6)
    far_round_trees(c, 130, 26, (90, 150, 90), 2221)
    # grandstand with roof (back)
    piece(c, Poly([(200, 40), (700, 40), (720, 64), (180, 64)]), (230, 230, 236), border=1.5, shadow=PROP)
    for x in (220, 450, 680):
        flat(c, RRect(x - 3, 64, x + 3, 160, 0), (200, 200, 210))
    stands(c, 64, 160, 2222, col=(150, 156, 170))
    # judges' box (right)
    piece(c, RRect(760, 60, 880, 150, 2), (240, 236, 226), border=1.5, shadow=PROP)
    piece(c, Poly([(750, 62), (890, 62), (820, 30)]), (160, 60, 60) if "judge" not in d else (60, 110, 200), border=1.5, shadow=PROP)
    flat(c, RRect(772, 78, 868, 112, 2), (170, 200, 220))
    # clock (left)
    piece(c, [RRect(50, 50, 140, 110, 3), RRect(90, 110, 100, 170, 1)], (30, 40, 50) if "clock" not in d else (120, 60, 140), border=1.5, shadow=PROP)
    seg_text(c, 60, 62, 30, "58", (250, 200, 60), width=3)
    # hedge + white rail
    piece(c, RRect(-10, 160, 910, 186, 6), (70, 140, 80), shadow=LAYER)
    for x in range(0, W, 40):
        flat(c, RRect(x, 182, x + 4, 206, 0), (250, 250, 246))
    flat(c, Thick(0, 190, W, 190, 3), (250, 250, 246))
    # sand arena
    c.rect(0, 206, W, H, (226, 196, 150))
    rnd = random.Random(2223)
    for _ in range(50):
        x, y = rnd.uniform(0, W), rnd.uniform(214, 600)
        flat(c, Thick(x, y, x + rnd.uniform(20, 50), y, 1.2), (214, 184, 138))
    # far fence
    fence(c, 300, 270, 120, 40, (60, 110, 210), (250, 250, 246))
    # flower boxes
    for k, x in enumerate((240, 470, 680)):
        col = [(220, 60, 90), (250, 200, 60), (220, 60, 90)][k]
        if k == 0 and "flowers" in d:
            col = (150, 100, 220)
        piece(c, RRect(x - 40, 262, x + 40, 280, 2), (250, 250, 246) if not (k == 0 and "flowers" in d) else (90, 150, 220), shadow=SMALL)
        flat(c, [Circ(x - 30 + j * 10, 258, 6) for j in range(7)], col)
        flat(c, [Circ(x - 25 + j * 10, 252, 5) for j in range(6)], (80, 150, 80))
    # main jump with horse and rider
    fence(c, 380, 440, 200, 70, (220, 60, 60) if "pole" not in d else (90, 180, 110), (250, 250, 246), rails=3)
    hx, hy = horse(c, 470, 400, 1.6, (150, 100, 70), jump=True)
    flat(c, Thick(hx + 10, hy - 2, hx + 40, hy - 40, 2), (60, 40, 30))
    jacket = (40, 50, 90) if "jacket" not in d else (200, 60, 70)
    piece(c, Poly([(hx - 10, hy - 2), (hx + 12, hy - 2), (hx + 20, hy - 34), (hx, hy - 38)]), jacket, border=1.2, shadow=SMALL)
    flat(c, [Thick(hx - 6, hy, hx + 14, hy + 20, 4), Thick(hx + 14, hy + 20, hx + 6, hy + 34, 3.4)], (250, 250, 246))
    flat(c, Circ(hx + 16, hy - 44, 7), SKIN)
    piece(c, Ell(hx + 15, hy - 48, 8, 5), (30, 30, 40), border=0.8, shadow=None)
    # water jump (left)
    if "water" not in d:
        flat(c, Poly([(20, 360), (220, 360), (240, 400), (0, 400)]), (90, 160, 220))
        flat(c, Poly([(40, 368), (200, 368), (210, 392), (20, 392)]), (130, 190, 240))
        fence(c, 30, 352, 180, 18, (250, 250, 246), (60, 160, 90), rails=1)
    # spare horse with groom (right)
    horse(c, 790, 470, 1.2, (240, 236, 226), mane=(200, 190, 180), face=-1)
    modern(c, 860, 470, (60, 110, 80) if "groom" not in d else (240, 140, 50), bottom=(40, 40, 50), hair=(90, 60, 40), h=1.6)
    # flags along the near rail
    for k, x in enumerate((140, 330, 560, 760)):
        flat(c, Thick(x, 600, x, 520, 2), (220, 220, 226))
        col = [(220, 60, 60), (250, 250, 246), (60, 110, 210), (250, 200, 60)][k]
        if k == 2 and "flag" in d:
            col = (240, 140, 200)
        piece(c, Poly([(x, 516), (x + 42, 530), (x, 548)]), col, shadow=SMALL)
    # spare fence + potted shrubs (lower arena)
    fence(c, 40, 500, 170, 44, (250, 200, 60), (60, 110, 210))
    for x in (260, 680):
        piece(c, Poly([(x - 22, 470), (x + 22, 470), (x + 16, 500), (x - 16, 500)]), (250, 250, 246), shadow=SMALL)
        piece(c, Circ(x, 452, 26), (80, 150, 80), shadow=SMALL)
    flat(c, Thick(0, 572, W, 572, 4), (250, 250, 246))
    for x in range(0, W, 60):
        flat(c, RRect(x, 572, x + 5, 600, 0), (250, 250, 246))


L222_ELEMENTS = [
    cloud_el("cloud", 520, 26, 0.45, 7),
    bird_el("bird", 300, 30, s=8, speed=20),
    E("tail", lambda c, m: flat(c, Thick(735, 432, 724, 462, 5), (200, 190, 180)), pivot=(735, 432), anim=dict(swingAngle=14, swingSpeed=0.8)),
    flash_el("flash", [(260, 100), (600, 120), (420, 90)], interval=2.4),
]

L222_DIFFS = [
    ("judge", 820, 48, 0),
    ("clock", 95, 80, 0),
    ("flowers", 240, 262, 0),
    ("groom", 860, 420, 0),
    ("jacket", 490, 350, 0),
    ("water", 120, 378, 0),
    ("flag", 577, 532, 0),
]


# =================================================================== Level 223 archery range
def archer(c, x, base, shirt, h=1.8, hair=(40, 30, 30), bow=(60, 60, 70)):
    """Archer at full draw, facing right."""
    hx, hy = modern(c, x, base, shirt, bottom=(40, 40, 50), hair=hair, h=h)
    sy = base - 34 * h
    flat(c, [Thick(x + 6 * h, sy, x + 30 * h, sy - 2 * h, 3 * h), Thick(x + 6 * h, sy, x - 4 * h, sy + 2 * h, 3 * h)], SKIN)
    bx = x + 32 * h
    piece(c, [Thick(bx, sy - 30 * h, bx + 6 * h, sy, 2.4 * h), Thick(bx + 6 * h, sy, bx, sy + 30 * h, 2.4 * h)], bow, shadow=SMALL)
    flat(c, [Thick(bx, sy - 30 * h, x - 4 * h, sy, 0.8), Thick(x - 4 * h, sy, bx, sy + 30 * h, 0.8)], (220, 220, 220))
    flat(c, Thick(x - 4 * h, sy, bx + 10 * h, sy, 1.2), (150, 110, 70))


def l223_bg(c, d):
    sky(c, (130, 190, 238), (220, 236, 248), 170)
    cloud_bg(c, 200, 40, 0.6)
    cloud_bg(c, 720, 60, 0.5)
    far_ridge(c, 130, 30, (176, 200, 216), 2231)
    far_round_trees(c, 170, 24, (90, 150, 90), 2232)
    # field with mowed stripes (perspective)
    c.rect(0, 170, W, H, (110, 180, 90))
    for k in range(10):
        flat(c, Poly([(k * 100 - 40, 170), (k * 100 + 10, 170), (k * 170 - 300, 600), (k * 170 - 380, 600)]), (118, 188, 98))
    # scoreboard (left)
    piece(c, [RRect(20, 40, 180, 140, 3), RRect(60, 140, 70, 200, 1), RRect(130, 140, 140, 200, 1)], (40, 60, 90), border=1.5, shadow=PROP)
    for r in range(3):
        flat(c, RRect(30, 54 + r * 26, 110, 70 + r * 26, 2), (250, 250, 246) if not (r == 0 and "score" in d) else (250, 200, 60))
        seg_text(c, 124, 52 + r * 26, 18, "5%d" % (8 - r), (250, 200, 60), width=2.2)
    # targets in a row (far)
    for k, x in enumerate((300, 400, 500, 600, 700, 800)):
        piece(c, [Thick(x - 18, 230, x - 10, 186, 3), Thick(x + 18, 230, x + 10, 186, 3)], (150, 110, 70), shadow=SMALL)
        cols = None
        if k == 3 and "target" in d:
            cols = [(250, 210, 60), (220, 60, 60), (250, 250, 246), (60, 140, 220), (40, 40, 50)]
        target_face(c, x, 196, 26, cols)
        flat(c, RRect(x - 10, 160, x + 10, 170, 2), (250, 250, 246))
        seg_text(c, x - 4, 160, 10, str(k + 1), (40, 40, 50), width=1.4)
    # wind flags on poles
    for k, x in enumerate((350, 550, 750)):
        flat(c, Thick(x, 240, x, 140, 2), (220, 220, 226))
    # tents (right)
    tent = (250, 250, 246)
    for k, x in enumerate((790, 870)):
        col = (220, 60, 60) if k == 0 else (60, 110, 210)
        if k == 1 and "tent" in d:
            col = (250, 200, 60)
        piece(c, [Poly([(x - 46, 290), (x + 46, 290), (x + 36, 258), (x - 36, 258)])], col, border=1.5, shadow=PROP)
        flat(c, [Poly([(x - 46, 290), (x + 46, 290), (x + 46, 298), (x - 46, 298)])], tent)
        flat(c, [Thick(x - 40, 298, x - 40, 360, 2), Thick(x + 40, 298, x + 40, 360, 2)], (220, 220, 226))
    modern(c, 800, 360, (250, 200, 60), bottom=(40, 40, 50), hair=(90, 60, 40), h=1.2)
    # shooting line
    flat(c, Thick(0, 470, W, 400, 4), (250, 250, 246))
    # bench with bags (left)
    if "bench" not in d:
        piece(c, [RRect(20, 430, 180, 444, 3), RRect(30, 444, 38, 486, 2), RRect(162, 444, 170, 486, 2)], (150, 110, 70), shadow=PROP)
        piece(c, RRect(40, 404, 100, 430, 6), (60, 110, 80), border=1.2, shadow=SMALL)
        piece(c, RRect(116, 410, 160, 430, 5), (220, 60, 60), border=1.2, shadow=SMALL)
    # archers along the line
    archer(c, 240, 470, (250, 250, 246), h=1.6)
    archer(c, 420, 450, (60, 110, 210) if "shirt" not in d else (240, 120, 180), h=1.7, hair=(200, 150, 80))
    archer(c, 620, 420, (220, 60, 60), h=1.5)
    # quivers on stands (foreground)
    for k, x in enumerate((320, 520)):
        col = (150, 80, 50) if not (k == 1 and "quiver" in d) else (60, 140, 200)
        piece(c, [Thick(x, 600, x, 520, 3)], (120, 120, 130), shadow=SMALL)
        piece(c, RRect(x - 12, 486, x + 12, 540, 5), col, border=1.2, shadow=SMALL)
        for j in range(3):
            flat(c, Thick(x - 6 + j * 6, 486, x - 8 + j * 7, 466, 1.4), (150, 110, 70))
            flat(c, Poly([(x - 8 + j * 7, 466), (x - 12 + j * 7, 458), (x - 4 + j * 7, 458)]), [(220, 60, 60), (250, 200, 60), (60, 110, 210)][j])
    # coach with binoculars (near right)
    modern(c, 760, 600, (40, 60, 110) if "coach" not in d else (230, 110, 50), bottom=(40, 40, 50), hair=(130, 130, 140), h=2.3)
    flat(c, [RRect(764, 480, 784, 494, 3)], (40, 40, 50))
    tree_round(c, 880, 600, s=1.4, col=(80, 150, 80))
    bush(c, 60, 600, s=1.6)


L223_ELEMENTS = [
    E("flag1", lambda c, m: piece(c, Poly([(350, 140), (380, 148), (350, 156)]), (250, 200, 60), shadow=SMALL), pivot=(350, 148),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.6)),
    E("flag2", lambda c, m: piece(c, Poly([(550, 140), (580, 148), (550, 156)]), (250, 200, 60), shadow=SMALL), pivot=(550, 148),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.4, phase=0.3)),
    E("flag3", lambda c, m: piece(c, Poly([(750, 140), (780, 148), (750, 156)]), (250, 200, 60), shadow=SMALL), pivot=(750, 148),
      anim=dict(stretch=(0.25, 0), scaleSpeed=1.5, phase=0.6)),
    E("arrow", lambda c, m: flat(c, Thick(500, 300, 530, 296, 1.6), (150, 110, 70)), pivot=(500, 300),
      anim=dict(driftVelocity=(120, -40), driftLength=140, driftFade=True)),
    cloud_el("cloud", 460, 30, 0.45, 7),
]

L223_DIFFS = [
    ("score", 140, 62, 0),
    ("target", 600, 196, 0),
    ("tent", 870, 278, 0),
    ("bench", 100, 440, 0),
    ("shirt", 420, 386, 0),
    ("quiver", 520, 512, 0),
    ("coach", 760, 530, 0),
]


# =================================================================== Level 224 beach volleyball
def l224_bg(c, d):
    sky(c, (90, 176, 240), (200, 232, 250), 210)
    cloud_bg(c, 120, 50, 0.6)
    cloud_bg(c, 600, 40, 0.5)
    # sea
    c.rect(0, 150, W, 230, (60, 150, 210))
    for k in range(6):
        y = 160 + k * 12
        flat(c, Thick(0, y, W, y, 1.6), (110, 190, 236))
    c.rect(0, 222, W, 300, (238, 214, 160))
    flat(c, Thick(0, 224, W, 224, 3), (250, 250, 246))
    # sailboat
    boat = (250, 250, 246) if "boat" not in d else (240, 120, 160)
    piece(c, Poly([(80, 170), (160, 170), (150, 184), (90, 184)]), (200, 80, 70), border=1.2, shadow=SMALL)
    flat(c, Thick(120, 170, 120, 96, 2), (120, 90, 70))
    piece(c, Poly([(122, 100), (122, 166), (168, 166)]), boat, border=1.2, shadow=SMALL)
    piece(c, Poly([(116, 110), (116, 166), (84, 166)]), (250, 250, 246), border=1.2, shadow=SMALL)
    # stands (temporary bleachers, left + right of the court)
    piece(c, Poly([(-10, 230), (300, 230), (300, 300), (-10, 300)]), (60, 110, 180), shadow=LAYER)
    crowd(c, -6, 296, 240, 4, 2241, dy=15)
    piece(c, Poly([(600, 230), (910, 230), (910, 300), (600, 300)]), (60, 110, 180), shadow=LAYER)
    crowd(c, 604, 906, 240, 4, 2242, dy=15)
    # sand
    c.rect(0, 300, W, H, (238, 214, 160))
    rnd = random.Random(2243)
    for _ in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(300, 600)
        flat(c, Circ(x, y, rnd.uniform(1, 2)), (220, 194, 140))
    # palm + lifeguard tower (behind the stands gap)
    palm(c, 330, 300, h=170, lean=-20)
    tower = (220, 60, 60) if "tower" not in d else (60, 160, 110)
    piece(c, [Thick(510, 300, 520, 200, 4), Thick(580, 300, 570, 200, 4)], (240, 236, 226), shadow=PROP)
    piece(c, RRect(496, 170, 594, 206, 3), tower, border=1.5, shadow=PROP)
    piece(c, Poly([(488, 172), (602, 172), (545, 140)]), (250, 250, 246), border=1.2, shadow=SMALL)
    # court lines (rope)
    ln = (60, 110, 210)
    flat(c, [Thick(180, 330, 720, 330, 3), Thick(180, 330, 60, 590, 3), Thick(720, 330, 840, 590, 3)], ln)
    # net
    for x in (130, 770):
        piece(c, RRect(x - 4, 270, x + 4, 440, 1), (230, 230, 236), shadow=PROP)
    for x in range(140, 762, 9):
        flat(c, Thick(x, 300, x, 360, 0.8), (30, 30, 36))
    for y in range(302, 360, 9):
        flat(c, Thick(136, y, 764, y, 0.8), (30, 30, 36))
    flat(c, RRect(134, 292, 766, 302, 1), (60, 110, 210))
    flat(c, Thick(130, 270, 60, 440, 1.2), (200, 200, 210))
    flat(c, Thick(770, 270, 840, 440, 1.2), (200, 200, 210))
    # far players (jumping block)
    for x in (380, 540):
        player(c, x, 300, (250, 200, 60), shorts=(250, 200, 60), h=1.3, skin=(226, 180, 140))
        arms_up(c, x, 300, 1.3, skin=(226, 180, 140))
    # parasol + cooler (right)
    parasol(c, 820, 470, 360, (250, 120, 60) if "parasol" not in d else (90, 180, 220))
    cooler = (60, 140, 220) if "cooler" not in d else (220, 60, 60)
    piece(c, [RRect(780, 430, 860, 476, 6), RRect(776, 424, 864, 438, 4)], cooler, border=1.5, shadow=PROP)
    flat(c, RRect(810, 446, 830, 452, 2), (250, 250, 246))
    # near players
    player(c, 300, 560, (220, 60, 90), shorts=(220, 60, 90), h=2.2, skin=(226, 180, 140), hair=(200, 150, 80))
    player(c, 560, 600, (220, 60, 90) if "top" not in d else (90, 200, 120), shorts=(220, 60, 90), h=2.5, skin=(200, 150, 110))
    # towel + bag (left foreground)
    if "towel" not in d:
        piece(c, Poly([(20, 560), (150, 548), (160, 590), (24, 598)]), (250, 200, 60), border=1.5, shadow=SMALL)
        for k in range(3):
            flat(c, Thick(30 + k * 44, 552 - k * 4, 36 + k * 44, 596 - k * 3, 6), (60, 160, 200))
    # sand bucket (front)
    piece(c, Poly([(680, 560), (720, 560), (714, 596), (686, 596)]), (240, 200, 50), border=1.2, shadow=SMALL)


L224_ELEMENTS = [
    E("ball", lambda c, m: [piece(c, Circ(460, 230, 13), (250, 250, 246), shadow=SMALL), flat(c, Thick(448, 226, 472, 234, 3), (250, 200, 60)),
                            flat(c, Thick(452, 240, 468, 220, 3), (60, 110, 210))], pivot=(460, 243), anim=dict(bobAmplitude=(0, 36), bobSpeed=0.7)),
    cloud_el("cloud", 380, 40, 0.5, 8),
    bird_el("gull", 200, 70, s=9, speed=20),
    bird_el("gull2", 700, 60, s=8, speed=-16),
    E("wave", lambda c, m: [flat(c, Thick(x, 216, x + 40, 216, 2), (230, 246, 255)) for x in (40, 240, 420, 720)], daynight="untinted",
      anim=dict(bobAmplitude=(10, 0), bobSpeed=0.3)),
]

L224_DIFFS = [
    ("boat", 125, 140, 0),
    ("tower", 545, 188, 0),
    ("parasol", 820, 360, 0),
    ("cooler", 820, 452, 0),
    ("top", 560, 520, 0),
    ("towel", 90, 574, 0),
]


LEVELS = [
    ("Level215", "排球馆", l215_bg, L215_ELEMENTS, L215_DIFFS, 60, OPTS),
    ("Level216", "乒乓球馆", l216_bg, L216_ELEMENTS, L216_DIFFS, 60, OPTS),
    ("Level217", "拳击擂台", l217_bg, L217_ELEMENTS, L217_DIFFS, 60, OPTS),
    ("Level218", "冰球场", l218_bg, L218_ELEMENTS, L218_DIFFS, 60, OPTS),
    ("Level219", "公路自行车赛", l219_bg, L219_ELEMENTS, L219_DIFFS, 60, OPTS),
    ("Level220", "高尔夫球场", l220_bg, L220_ELEMENTS, L220_DIFFS, 60, OPTS),
    ("Level221", "体操馆", l221_bg, L221_ELEMENTS, L221_DIFFS, 60, OPTS),
    ("Level222", "马术障碍赛", l222_bg, L222_ELEMENTS, L222_DIFFS, 60, OPTS),
    ("Level223", "射箭场", l223_bg, L223_ELEMENTS, L223_DIFFS, 60, OPTS),
    ("Level224", "沙滩排球", l224_bg, L224_ELEMENTS, L224_DIFFS, 60, OPTS),
]
