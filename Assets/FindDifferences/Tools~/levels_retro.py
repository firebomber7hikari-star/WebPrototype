# -*- coding: utf-8 -*-
"""80s / 90s video-game nostalgia (all designs original: no real consoles, brands, logos or characters):
  Level155 游戏卧室   - a 90s kid's bedroom: CRT TV with a console and two pads, beanbags, posters, cartridge shelf, beige PC
  Level156 卡带店     - a game rental shop: walls of game boxes, counter with a till, demo TV, kids browsing
  Level157 像素平台   - inside an 8-bit platformer: pixel hills, brick platforms, coins, a slime, the goal flag, HUD
  Level158 像素太空   - an 8-bit space shooter: alien formation, shields, the player's ship, planet, HUD
  Level159 街机厅     - a 90s arcade hall: rows of cabinets, token counter, fluorescent tubes, kids playing
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from fills import wallpaper_diamonds, wallpaper_stripes
from levels_akiba import modern, sign_box
from levels_homes import planks, monstera

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
NIGHT_EDGE = (110, 100, 130)


# =================================================================== shared props
def sprite(c, x, y, rows, pal, s=4):
    """Pixel sprite from strings: each character is a palette key ('.' = empty); (x, y) = top left."""
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != "." and ch in pal:
                flat(c, RRect(x + i * s, y + j * s, x + (i + 1) * s, y + (j + 1) * s, 0), pal[ch])


def block(c, x, y, s, col, kind="brick"):
    flat(c, RRect(x, y, x + s, y + s, 0), col)
    dark, light = lit(col, 0.7), lit(col, 1.25)
    flat(c, [RRect(x, y, x + s, y + 3, 0), RRect(x, y, x + 3, y + s, 0)], light)
    flat(c, [RRect(x, y + s - 3, x + s, y + s, 0), RRect(x + s - 3, y, x + s, y + s, 0)], dark)
    if kind == "brick":
        flat(c, [RRect(x, y + s / 2 - 1, x + s, y + s / 2 + 1, 0), RRect(x + s / 2 - 1, y, x + s / 2 + 1, y + s / 2, 0)], dark)
    elif kind == "gem":
        flat(c, Poly([(x + s / 2, y + 6), (x + s - 6, y + s / 2), (x + s / 2, y + s - 6), (x + 6, y + s / 2)]), (250, 250, 240))


def digits(c, x, y, text, col, s=3):
    """Tiny 3x5 pixel digits for HUDs."""
    font = {"0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"], "2": ["###", "..#", "###", "#..", "###"],
            "3": ["###", "..#", "###", "..#", "###"], "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
            "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", ".#.", ".#.", ".#."], "8": ["###", "#.#", "###", "#.#", "###"],
            "9": ["###", "#.#", "###", "..#", "###"]}
    for k, ch in enumerate(text):
        sprite(c, x + k * 4 * s, y, font.get(ch, ["...", "...", "...", "...", "..."]), {"#": col}, s)


def crt(c, x0, y0, x1, y1, body=(70, 66, 72), screen=None, edge=None):
    """CRT television; screen(c, rect) paints the picture. Returns the screen rect."""
    pk = (lambda sh, col, **kw: piece(c, sh, col, border_col=edge, **kw)) if edge else (lambda sh, col, **kw: piece(c, sh, col, **kw))
    pk(RRect(x0, y0, x1, y1, 10), body, border=1.5, shadow=PROP)
    r = (x0 + 14, y0 + 14, x1 - 50, y1 - 14)
    flat(c, RRect(r[0] - 4, r[1] - 4, r[2] + 4, r[3] + 4, 14), (30, 30, 34))
    if screen:
        screen(c, r)
    for y in range(int(r[1]), int(r[3]), 4):
        flat(c, Thick(r[0], y, r[2], y, 0.8), (0, 0, 0, 0.12))
    for k in range(2):
        flat(c, Circ(x1 - 26, y0 + 30 + k * 26, 7), (190, 186, 180))
    flat(c, [Thick(x1 - 36 + k * 6, y1 - 34, x1 - 36 + k * 6, y1 - 18, 1.4) for k in range(4)], lit(body, 0.7))
    return r


def mini_game(c, r, sky=(110, 170, 240), ground=(200, 120, 60), hero=(230, 60, 60)):
    """A tiny platformer picture for screens."""
    x0, y0, x1, y1 = r
    flat(c, RRect(x0, y0, x1, y1, 0), sky)
    w, h = x1 - x0, y1 - y0
    flat(c, Ell(x0 + w * 0.3, y1 - h * 0.25, w * 0.25, h * 0.3), (90, 180, 90))
    flat(c, RRect(x0, y1 - h * 0.2, x1, y1, 0), ground)
    flat(c, RRect(x0, y1 - h * 0.2, x1, y1 - h * 0.16, 0), (80, 170, 70))
    for k in range(3):
        flat(c, RRect(x0 + w * (0.5 + k * 0.08), y0 + h * 0.4, x0 + w * (0.58 + k * 0.08) - 1, y0 + h * 0.48, 0), (200, 120, 60))
    flat(c, RRect(x0 + w * 0.15, y1 - h * 0.34, x0 + w * 0.15 + h * 0.1, y1 - h * 0.2, 0), hero)
    flat(c, Ell(x0 + w * 0.75, y0 + h * 0.18, w * 0.08, h * 0.06), (250, 250, 250))


def pad(c, x, y, col, s=1.0):
    """Game pad (original shape) seen from above."""
    piece(c, [RRect(x - 22 * s, y - 9 * s, x + 22 * s, y + 9 * s, 8 * s)], col, border=1, shadow=SMALL)
    flat(c, [RRect(x - 17 * s, y - 2 * s, x - 7 * s, y + 2 * s, 1), RRect(x - 14 * s, y - 5 * s, x - 10 * s, y + 5 * s, 1)], (40, 40, 46))
    flat(c, [Circ(x + 10 * s, y + 2 * s, 2.6 * s), Circ(x + 16 * s, y - 2 * s, 2.6 * s)], (220, 60, 70))


def cartridge(c, x, base, col, label, w=34, h=40):
    piece(c, [RRect(x - w / 2, base - h, x + w / 2, base, 3)], col, border=1, shadow=SMALL)
    flat(c, RRect(x - w / 2 + 5, base - h + 6, x + w / 2 - 5, base - h * 0.4, 1), label)
    flat(c, Thick(x - w / 2 + 4, base - 6, x + w / 2 - 4, base - 6, 1.2), lit(col, 0.8))


def game_box(c, x0, y0, x1, y1, col, art, seed):
    piece(c, RRect(x0, y0, x1, y1, 1), col, shadow=SMALL)
    rnd = random.Random(seed)
    flat(c, RRect(x0 + 3, y0 + 3, x1 - 3, y0 + (y1 - y0) * 0.22, 0), lit(col, 0.7))
    flat(c, Circ((x0 + x1) / 2 + rnd.uniform(-3, 3), y0 + (y1 - y0) * 0.6, (x1 - x0) * 0.28), art)


# =================================================================== Level 155 90s bedroom
def l155_bg(c, d):
    wallpaper_stripes(c, (0, 0, W, 420), (200, 214, 236), (190, 204, 228), w=36)
    flat(c, RRect(0, 0, W, 12, 0), (236, 240, 246))
    # window (left) with curtains
    flat(c, RRect(40, 60, 230, 230, 0), (160, 210, 240))
    flat(c, [Ell(90, 200, 50, 26), Ell(170, 210, 60, 30)], (120, 180, 110))
    piece(c, [RRect(32, 52, 238, 62, 0), RRect(32, 52, 42, 240, 0), RRect(228, 52, 238, 240, 0), RRect(132, 62, 138, 230, 0), RRect(26, 230, 244, 242, 1)],
          (250, 250, 246), shadow=SMALL)
    # posters (original designs)
    rob = (90, 110, 200) if "poster" not in d else (200, 80, 80)
    piece(c, RRect(270, 50, 370, 190, 1), (30, 30, 50), shadow=PROP)
    flat(c, [RRect(300, 80, 340, 120, 4), RRect(292, 124, 348, 170, 4)], rob)
    flat(c, [Circ(312, 98, 5), Circ(328, 98, 5)], (250, 230, 90))
    flat(c, [RRect(278, 56, 362, 70, 1)], (250, 200, 60))
    piece(c, RRect(700, 50, 850, 150, 1), (250, 240, 200), shadow=PROP)
    flat(c, Poly([(700, 150), (760, 100), (850, 150)]), (60, 160, 90))
    piece(c, [RRect(730, 110, 800, 126, 6), Circ(744, 128, 7), Circ(788, 128, 7)], (220, 50, 60), shadow=None)
    flat(c, RRect(706, 56, 844, 68, 1), (40, 40, 60))
    # cartridge shelf (above TV)
    piece(c, RRect(400, 170, 640, 180, 1), (170, 120, 80), shadow=SMALL)
    carts = [(80, 80, 90), (180, 60, 60), (70, 110, 170), (200, 200, 200), (80, 80, 90), (110, 160, 90)]
    if "cart" in d:
        carts[3] = (240, 180, 60)
    for k, col in enumerate(carts):
        cartridge(c, 424 + k * 38, 170, col, (240, 230, 200))
    # beige PC on a desk (right)
    piece(c, [RRect(690, 300, 890, 314, 2), RRect(700, 314, 712, 420, 2), RRect(868, 314, 880, 420, 2)], (180, 130, 90), border=1.5, shadow=PROP)
    crt(c, 720, 190, 840, 290, body=(226, 220, 200), screen=lambda c, r: (flat(c, RRect(*r, 0), (40, 90, 140)),
                                                                           flat(c, [Thick(r[0] + 6, r[1] + 10 + k * 10, r[2] - 6 - k * 6, r[1] + 10 + k * 10, 2)
                                                                                    for k in range(4)], (200, 230, 250))))
    piece(c, RRect(730, 290, 830, 300, 1), (226, 220, 200), shadow=SMALL)
    piece(c, RRect(714, 294, 816, 304, 2), (220, 214, 196), shadow=SMALL)
    piece(c, [RRect(846, 260, 880, 300, 3)], (226, 220, 200), shadow=SMALL)
    # carpet
    c.rect(0, 420, W, H, (150, 110, 150))
    rnd = random.Random(1551)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(430, 600)
        flat(c, Thick(x, y, x + 6, y, 2), (140, 100, 140))
    flat(c, Thick(0, 420, W, 420, 4), (230, 230, 226))
    # TV cabinet + CRT + console
    piece(c, RRect(390, 330, 650, 440, 3), (140, 100, 70), border=1.5, shadow=PROP)
    flat(c, [Thick(520, 334, 520, 436, 1.6)], (120, 84, 58))
    crt(c, 400, 200, 640, 334, body=(60, 58, 64), screen=lambda c, r: mini_game(c, r))
    console = (90, 90, 100) if "console" not in d else (200, 200, 210)
    piece(c, [RRect(430, 380, 510, 404, 4)], console, border=1, shadow=SMALL)
    flat(c, [RRect(440, 386, 470, 390, 1), Circ(498, 392, 3)], (220, 60, 70))
    flat(c, RRect(530, 360, 640, 420, 2), (110, 76, 50))
    for k in range(4):
        game_box(c, 536 + k * 26, 368, 558 + k * 26, 418, [(220, 60, 60), (60, 120, 200), (240, 200, 60), (90, 170, 100)][k], (250, 250, 240), 1550 + k)
    # cables to the pads
    flat(c, [Thick(450, 404, 330, 530, 1.6), Thick(490, 404, 600, 540, 1.6)], (40, 40, 46))
    # kids on beanbags (seen from behind, slightly turned)
    for x, bag, top, hair in ((300, (220, 80, 80), (80, 140, 220), (40, 30, 30)), (630, (80, 170, 120), (240, 200, 70), (150, 90, 50))):
        if x == 630 and "beanbag" in d:
            bag = (240, 160, 50)
        piece(c, [Ell(x, 560, 80, 44), Ell(x - 10, 520, 60, 40)], bag, border=1.5, shadow=PROP)
        modern(c, x, 560, top, bottom=(60, 70, 110), hair=hair, h=2.3)
    pad(c, 330, 530, (90, 90, 100), 1.2)
    pad(c, 600, 540, (90, 90, 100) if "pad" not in d else (220, 60, 60), 1.2)
    # snacks
    can = (220, 50, 50) if "can" not in d else (60, 140, 220)
    piece(c, RRect(170, 520, 194, 560, 4), can, border=1, shadow=SMALL)
    flat(c, Thick(170, 534, 194, 534, 3), (250, 250, 250))
    piece(c, Poly([(90, 570), (140, 570), (146, 516), (84, 516)]), (240, 190, 60), border=1, shadow=SMALL)
    flat(c, Circ(115, 540, 12), (220, 60, 60))
    # puzzle cube + comic on the floor (right)
    piece(c, RRect(780, 540, 820, 580, 3), (40, 40, 46), shadow=SMALL)
    for i in range(3):
        for j in range(3):
            flat(c, RRect(782 + i * 13, 542 + j * 13, 793 + i * 13, 553 + j * 13, 1), [(220, 60, 60), (250, 250, 246), (60, 120, 220), (250, 200, 60), (90, 180, 90)][(i * 3 + j) % 5])
    piece(c, Poly([(840, 590), (900, 580), (900, 540), (846, 548)]), (250, 240, 220), shadow=SMALL)


def l155_hero(c, m):
    flat(c, RRect(436, 296, 446, 310, 0), (230, 60, 60))


L155_ELEMENTS = [
    E("hero", l155_hero, anim=dict(bobAmplitude=(0, 14), bobSpeed=0.7, bounce=True)),
    E("curtainL", lambda c, m: piece(c, Poly([(20, 52), (56, 52), (62, 250), (16, 256)]), (240, 200, 90), shadow=SMALL), pivot=(38, 52),
      anim=dict(swingAngle=1.5, swingSpeed=0.25)),
    E("curtainR", lambda c, m: piece(c, Poly([(214, 52), (250, 52), (254, 256), (208, 250)]), (240, 200, 90), shadow=SMALL), pivot=(232, 52),
      anim=dict(swingAngle=1.5, swingSpeed=0.25, phase=0.5)),
    E("cursor", lambda c, m: flat(c, RRect(760, 246, 768, 250, 0), (200, 230, 250)), daynight="untinted", anim=dict(blinkInterval=1.0, blinkDuration=0.5)),
    E("glow", lambda c, m: soft_union(c, [RRect(420, 220, 580, 320, 4)], (180, 220, 255), 0.18, spread=24), daynight="untinted",
      anim=dict(twinkle=0.3, twinkleSpeed=2.0)),
]

L155_DIFFS = [
    ("poster", 320, 125, 0),
    ("cart", 538, 150, 0),
    ("console", 470, 392, 0),
    ("beanbag", 650, 540, 0),
    ("pad", 600, 540, 0),
    ("can", 182, 540, 0),
]


# =================================================================== Level 156 game rental shop
BOXES = [(220, 60, 60), (60, 120, 200), (240, 200, 60), (90, 170, 100), (160, 90, 180), (240, 140, 60), (50, 50, 60), (230, 230, 226)]


def box_wall(c, x0, x1, y0, y1, rows, seed, swap=None):
    piece(c, RRect(x0, y0, x1, y1, 2), (150, 110, 80), border=1.5, shadow=PROP)
    rnd = random.Random(seed)
    h = (y1 - y0 - 10) / rows
    for r in range(rows):
        top, base = y0 + 6 + r * h, y0 + 6 + (r + 1) * h
        flat(c, RRect(x0 + 4, base - 6, x1 - 4, base, 0), (120, 86, 60))
        x, i = x0 + 8, 0
        while x < x1 - 30:
            col = rnd.choice(BOXES)
            art = rnd.choice(BOXES)
            if swap and swap[0] == r and swap[1] == i:
                col = swap[2]
            game_box(c, x, base - h * 0.82, x + 24, base - 6, col, art, rnd.randint(0, 999))
            x += 28
            i += 1


def l156_bg(c, d):
    c.rect(0, 0, W, 460, (240, 232, 214))
    flat(c, RRect(0, 0, W, 16, 0), (250, 246, 236))
    # shop sign strip
    piece(c, RRect(260, 24, 640, 70, 3), (40, 50, 90), border=1.5, shadow=PROP)
    sign_box(c, 280, 30, 620, 64, (40, 50, 90), 1561, glyph=(250, 220, 90), vertical=False)
    # walls of game boxes
    box_wall(c, 10, 250, 90, 450, 5, 1562)
    box_wall(c, 650, 890, 90, 450, 5, 1563, swap=(2, 3, (250, 250, 246)) if "box" in d else None)
    # demo TV on a bracket (centre)
    flat(c, [Thick(450, 70, 450, 100, 6)], (80, 80, 86))
    crt(c, 350, 100, 550, 220, body=(50, 50, 56), screen=lambda c, r: mini_game(c, r, sky=(250, 170, 100) if "tv" in d else (110, 170, 240)))
    # posters
    piece(c, RRect(290, 250, 380, 380, 1), (250, 250, 240), shadow=PROP)
    flat(c, RRect(296, 256, 374, 374, 0), (60, 40, 90))
    piece(c, Poly(star_pts(335, 300, 28, 12, points=5)), (250, 210, 60) if "star" not in d else (120, 220, 240), shadow=None)
    flat(c, RRect(300, 340, 370, 366, 1), (230, 70, 80))
    piece(c, RRect(520, 250, 610, 380, 1), (250, 250, 240), shadow=PROP)
    flat(c, RRect(526, 256, 604, 374, 0), (60, 140, 200))
    flat(c, [RRect(546, 280, 584, 340, 6), Poly([(546, 300), (526, 330), (546, 330)]), Poly([(584, 300), (604, 330), (584, 330)])], (240, 240, 246))
    flat(c, Circ(565, 300, 8), (60, 140, 200))
    # floor tiles
    c.rect(0, 460, W, H, (220, 216, 210))
    for r, y in enumerate(range(460, H, 36)):
        for k, x in enumerate(range(0, W, 36)):
            if (r + k) % 2:
                flat(c, RRect(x, y, x + 36, y + 36, 0), (200, 60, 60))
    # counter with till and glass case
    piece(c, RRect(300, 400, 600, 500, 3), (60, 70, 110), border=1.5, shadow=PROP)
    flat(c, RRect(316, 416, 584, 470, 2), (190, 226, 240))
    for k, x in enumerate((340, 400, 460, 520)):
        hh = (80, 80, 90) if not (k == 2 and "handheld" in d) else (240, 180, 60)
        piece(c, RRect(x, 426, x + 36, 462, 4), hh, shadow=SMALL)
        flat(c, RRect(x + 6, 430, x + 30, 446, 1), (140, 180, 120))
        flat(c, [Circ(x + 12, 454, 3), Circ(x + 26, 454, 3)], (220, 60, 70))
    till = (200, 200, 206) if "till" not in d else (230, 120, 80)
    piece(c, [Poly([(500, 400), (580, 400), (572, 360), (508, 360)]), RRect(516, 340, 566, 362, 2)], till, border=1.2, shadow=SMALL)
    flat(c, RRect(522, 344, 560, 356, 1), (60, 200, 140))
    # cashier behind the counter
    modern(c, 420, 460, (230, 70, 80), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.3, glasses=True)
    flat(c, Poly([(410, 380), (430, 380), (420, 396)]), (250, 250, 246))
    # kids browsing
    hx, hy = modern(c, 160, 594, (60, 140, 200), bottom=(50, 60, 90), hair=(200, 150, 80), h=2.3, style="long")
    bp = (240, 200, 60) if "backpack" not in d else (110, 180, 110)
    piece(c, RRect(118, 494, 146, 540, 6), bp, border=1, shadow=SMALL)
    modern(c, 760, 594, (90, 170, 100), bottom=(50, 60, 90), hair=(40, 30, 30), h=2.4)
    piece(c, RRect(782, 500, 806, 530, 1), (220, 60, 60), shadow=SMALL)
    # return bin
    piece(c, [RRect(620, 500, 700, 590, 4)], (230, 190, 60), border=1.5, shadow=PROP)
    flat(c, RRect(636, 510, 684, 530, 2), (40, 40, 46))


L156_ELEMENTS = [
    E("hero", lambda c, m: flat(c, RRect(386, 178, 396, 192, 0), (230, 60, 60)), anim=dict(bobAmplitude=(30, 0), bobSpeed=0.25)),
    E("fan", lambda c, m: (flat(c, Thick(150, 16, 150, 40, 3), (90, 90, 96)), flat(c, [Ell(150, 44, 60, 5)], (200, 200, 206))), pivot=(150, 44),
      anim=dict(stretch=(0.8, 0), scaleSpeed=3.0)),
    E("neon", lambda c, m: soft_union(c, [RRect(260, 24, 640, 70, 3)], (120, 160, 255), 0.25, spread=16), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=1.5)),
]

L156_DIFFS = [
    ("box", 734, 290, 0),
    ("tv", 430, 160, 0),
    ("star", 335, 300, 0),
    ("handheld", 478, 444, 0),
    ("till", 540, 372, 0),
    ("backpack", 132, 517, 0),
]


# =================================================================== Level 157 inside an 8-bit platformer
S = 30          # tile size
SKY157 = (100, 160, 250)


def l157_bg(c, d):
    c.rect(0, 0, W, H, SKY157)
    # pixel hills + bushes
    for cx, w, h, col in ((120, 260, 140, (60, 170, 80)), (520, 320, 180, (80, 190, 90)), (820, 220, 120, (60, 170, 80))):
        for k in range(int(h / 10)):
            ww = w * (1 - (k / (h / 10)) ** 2) ** 0.5
            flat(c, RRect(cx - ww / 2, 480 - (k + 1) * 10, cx + ww / 2, 480 - k * 10, 0), col)
        flat(c, [RRect(cx - 20, 480 - h * 0.6, cx - 10, 480 - h * 0.6 + 20, 0), RRect(cx + 16, 480 - h * 0.45, cx + 26, 480 - h * 0.45 + 20, 0)],
             lit(col, 0.7))
    hill = (60, 170, 80)
    for k in range(10):
        ww = 260 * (1 - (k / 14) ** 2) ** 0.5 * (1 - k / 14)
        flat(c, RRect(120 - ww / 2, 480 - (k + 1) * 10, 120 + ww / 2, 480 - k * 10, 0), hill)
    # pixel clouds (static, a couple drift as elements)
    for x, y in ((90, 70), (640, 50)):
        sprite(c, x, y, ["..####....", ".######...", "##########", "##########", ".########."], {"#": (250, 250, 250)}, 8)
    # ground tiles
    for x in range(0, W, S):
        for y in range(480, H, S):
            block(c, x, y, S, (190, 110, 60), kind="dirt")
        flat(c, RRect(x, 480, x + S, 490, 0), (90, 200, 70))
    # gap in the ground (pit)
    if "pit" not in d:
        flat(c, RRect(600, 480, 660, H, 0), (40, 40, 60))
    # floating platforms
    for x in range(240, 390, S):
        block(c, x, 330, S, (200, 100, 60) if "bricks" not in d or x != 300 else (110, 110, 130))
    block(c, 420, 330, S, (240, 200, 60) if "gem" not in d else (90, 200, 230), kind="gem")
    for x in range(660, 780, S):
        block(c, x, 380, S, (200, 100, 60))
    # pipe-free tower: stone steps
    for k in range(3):
        for j in range(k + 1):
            block(c, 480 + k * S, 450 - j * S, S, (150, 150, 160), kind="stone")
    # goal flag (right)
    flat(c, RRect(846, 140, 852, 480, 0), (230, 230, 230))
    flat(c, Circ(849, 136, 6), (250, 200, 60))
    fl = (230, 60, 60) if "flag" not in d else (60, 120, 230)
    flat(c, Poly([(852, 150), (900, 166), (852, 182)]), fl)
    block(c, 834, 450, S, (150, 150, 160), kind="stone")
    # trees
    for x, col in ((40, (40, 140, 70)), (420, (40, 140, 70))):
        flat(c, RRect(x - 6, 430, x + 6, 480, 0), (120, 70, 40))
        if x == 420 and "tree" in d:
            col = (220, 140, 40)
        sprite(c, x - 24, 382, ["..####..", ".######.", "########", "########", ".######.", "..####.."], {"#": col}, 6)
    # HUD
    flat(c, RRect(0, 0, W, 36, 0), (20, 20, 30))
    digits(c, 20, 8, "004250", (250, 250, 250), 4)
    lives = 3 if "life" not in d else 2
    for k in range(lives):
        sprite(c, 690 + k * 44, 4, [".#.#.", "#####", "#####", ".###.", "..#.."], {"#": (240, 60, 80)}, 6)
    sprite(c, 400, 6, [".###.", "#####", "#####", "#####", ".###."], {"#": (250, 210, 60)}, 5)
    digits(c, 440, 8, "17", (250, 250, 250), 4)


def l157_hero(c, m):
    sprite(c, 120, 404, ["..###...", ".#####..", ".#o#o#..", ".#####..", "..##....", ".####...", "#.##.#..", ".#..#..."],
           {"#": (230, 60, 60), "o": (250, 250, 250)}, 8)


def l157_slime(c, m):
    sprite(c, 700, 452, ["..####..", ".######.", "##o##o##", "########"], {"#": (130, 80, 200), "o": (250, 250, 250)}, 7)


def coin(x, y, ph):
    return E("coin%d" % x, lambda c, m: sprite(c, x - 8, y - 12, [".##.", "#yy#", "#yy#", "#yy#", "#yy#", ".##."], {"#": (230, 170, 40), "y": (250, 220, 90)}, 4),
             pivot=(x, y), anim=dict(spinSpeed=1.0, phase=ph))


L157_ELEMENTS = [
    E("hero", l157_hero, anim=dict(bobAmplitude=(0, 60), bobSpeed=0.5, bounce=True)),
    E("slime", l157_slime, anim=dict(bobAmplitude=(40, 0), bobSpeed=0.2)),
    E("cloud", lambda c, m: sprite(c, 340, 110, ["..###...", ".#####..", "########"], {"#": (250, 250, 250)}, 8),
      anim=dict(bobAmplitude=(40, 0), bobSpeed=0.05)),
] + [coin(x, y, i * 0.2) for i, (x, y) in enumerate(((255, 300), (285, 300), (315, 300), (690, 350), (720, 350)))]

L157_DIFFS = [
    ("gem", 435, 345, 0),
    ("pit", 630, 540, 0),
    ("bricks", 315, 345, 0),
    ("flag", 870, 166, 0),
    ("tree", 420, 400, 0),
    ("life", 793, 19, 0),
]


# =================================================================== Level 158 8-bit space shooter
ALIEN_A = ["..#..#..", "...##...", "..####..", ".#o##o#.", "########", "#.#..#.#", "..#..#.."]
ALIEN_B = ["..####..", ".######.", "##o##o##", "########", ".#.##.#.", "#......#"]


def l158_bg(c, d):
    c.rect(0, 0, W, H, (10, 12, 30))
    rnd = random.Random(1581)
    for _ in range(90):
        x, y = rnd.uniform(0, W), rnd.uniform(40, 600)
        s = rnd.choice((2, 2, 3))
        flat(c, RRect(x, y, x + s, y + s, 0), rnd.choice([(250, 250, 250), (180, 200, 255), (255, 230, 160)]))
    # planet with a ring (top right)
    flat(c, Circ(780, 150, 70), (200, 120, 80))
    flat(c, [RRect(718, 120, 842, 134, 0), RRect(714, 160, 846, 172, 0)], (170, 96, 66))
    ring = (230, 210, 140) if "ring" not in d else (120, 220, 240)
    c.ellipse_ring(780, 150, 120, 26, 6, ring, ymin=150)
    c.ellipse_ring(780, 150, 120, 26, 6, ring, ymax=126)
    # moon (left)
    flat(c, Circ(110, 200, 30), (180, 180, 196) if "moon" not in d else (230, 200, 120))
    flat(c, [Circ(100, 192, 6), Circ(120, 212, 4)], (150, 150, 166))
    # shields
    for k, x in enumerate((150, 360, 570, 780)):
        rows = ["..######..", ".########.", "##########", "##########", "###....###", "##......##"]
        if k == 2 and "shield" in d:
            rows = ["..######..", ".########.", "#.....####", "#.....####", "#.....####", "##......##"]
        sprite(c, x - 30, 440, rows, {"#": (90, 220, 110)}, 6)
    # HUD
    digits(c, 20, 10, "012900", (250, 250, 250), 4)
    digits(c, 380, 10, "050000", (250, 200, 60) if "hiscore" not in d else (240, 90, 120), 4)
    lives = 3 if "lives" not in d else 2
    for k in range(lives):
        sprite(c, 740 + k * 50, 6, ["..#..", ".###.", "#####", "#.#.#"], {"#": (90, 200, 250)}, 7)
    flat(c, RRect(0, 580, W, 584, 0), (90, 220, 110))


def l158_aliens(c, m):
    cols = [(240, 80, 120), (250, 200, 60), (120, 220, 240)]
    for r in range(3):
        for k in range(7):
            x, y = 190 + k * 76, 120 + r * 60
            col = cols[r]
            sprite(c, x, y, ALIEN_A if r != 1 else ALIEN_B, {"#": col, "o": (10, 12, 30)}, 5)


L158_ELEMENTS = [
    E("aliens", l158_aliens, anim=dict(bobAmplitude=(40, 6), bobSpeed=0.12)),
    E("ship", lambda c, m: sprite(c, 420, 520, ["....#....", "...###...", "...###...", ".#######.", "#########", "##.###.##"], {"#": (90, 200, 250)}, 6),
      anim=dict(bobAmplitude=(160, 0), bobSpeed=0.1, phase=0.3)),
    E("shot", lambda c, m: flat(c, RRect(445, 470, 449, 486, 0), (250, 250, 160)), daynight="untinted",
      anim=dict(driftVelocity=(0, -120), driftLength=360, driftFade=True)),
    E("ufo", lambda c, m: sprite(c, 0, 60, ["...####...", ".########.", "##.##.##.#", ".########."], {"#": (230, 60, 60)}, 5),
      anim=drift_across(0, 50, 50, start=200)),
    E("stars", lambda c, m: [flat(c, RRect(x, y, x + 2, y + 6, 0), (200, 210, 255)) for x, y in ((60, 300), (300, 260), (640, 330), (860, 280))],
      anim=dict(driftVelocity=(0, 60), driftLength=200, driftFade=True)),
    E("boom", lambda c, m: sprite(c, 600, 240, ["#..#..#", ".#.#.#.", "..###..", "###.###", "..###..", ".#.#.#.", "#..#..#"],
                                  {"#": (250, 180, 60)}, 5), daynight="untinted", anim=dict(blinkInterval=2.0, blinkDuration=0.4)),
]

L158_DIFFS = [
    ("ring", 780, 150, 0),
    ("shield", 558, 461, 0),
    ("lives", 857, 20, 0),
    ("moon", 110, 200, 0),
    ("hiscore", 426, 20, 0),
]


# =================================================================== Level 159 90s arcade hall
def cabinet(c, x, base, body, marquee, screen_col, seed, w=110, h=230):
    x0, x1 = x - w / 2, x + w / 2
    piece(c, [Poly([(x0, base), (x1, base), (x1, base - h * 0.55), (x1 - 8, base - h * 0.8), (x1, base - h), (x0, base - h), (x0 + 8, base - h * 0.8),
                    (x0, base - h * 0.55)])], body, border=1.5, border_col=NIGHT_EDGE, shadow=PROP)
    flat(c, RRect(x0 + 8, base - h + 6, x1 - 8, base - h * 0.86, 2), marquee)
    sign_box(c, x0 + 12, base - h + 8, x1 - 12, base - h * 0.88, marquee, seed, glyph=(250, 250, 240), vertical=False)
    flat(c, RRect(x0 + 14, base - h * 0.82, x1 - 14, base - h * 0.56, 4), (20, 20, 26))
    flat(c, RRect(x0 + 18, base - h * 0.8, x1 - 18, base - h * 0.58, 2), screen_col)
    flat(c, Poly([(x0 - 4, base - h * 0.52), (x1 + 4, base - h * 0.52), (x1 + 8, base - h * 0.44), (x0 - 8, base - h * 0.44)]), lit(body, 0.7))
    flat(c, [Thick(x - 30, base - h * 0.5, x - 30, base - h * 0.47 - 12, 3), Circ(x - 30, base - h * 0.5 - 12, 5)], (40, 40, 46))
    flat(c, [Circ(x + 4 + k * 12, base - h * 0.49, 4) for k in range(3)], (230, 60, 70))
    flat(c, RRect(x - 10, base - 60, x + 10, base - 40, 2), (40, 40, 46))
    flat(c, RRect(x - 4, base - 54, x + 4, base - 46, 1), (250, 200, 60))


def l159_bg(c, d):
    c.rect(0, 0, W, 440, (60, 56, 80))
    for x in range(0, W, 60):
        flat(c, Thick(x, 0, x, 440, 1), (54, 50, 72))
    # fluorescent tubes (static housings; glows are elements)
    for x in (150, 450, 750):
        flat(c, RRect(x - 90, 10, x + 90, 22, 4), (220, 230, 236))
    # posters (original fighting / racing designs)
    piece(c, RRect(40, 50, 150, 190, 1), (30, 30, 40), border=1.2, border_col=NIGHT_EDGE, shadow=PROP)
    fighter = (240, 80, 60) if "poster" not in d else (80, 160, 240)
    flat(c, [Circ(96, 90, 16), Poly([(74, 108), (118, 108), (128, 180), (64, 180)]), Thick(118, 120, 140, 100, 8)], fighter)
    flat(c, RRect(46, 56, 144, 68, 1), (250, 210, 60))
    piece(c, RRect(750, 50, 860, 190, 1), (250, 240, 210), border=1.2, border_col=NIGHT_EDGE, shadow=PROP)
    flat(c, Poly([(756, 184), (800, 120), (854, 184)]), (90, 90, 100))
    piece(c, [RRect(776, 140, 836, 156, 6), Circ(788, 158, 7), Circ(826, 158, 7)], (230, 60, 60), shadow=None)
    # floor
    c.rect(0, 440, W, H, (40, 40, 56))
    rnd = random.Random(1591)
    for _ in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(446, 600)
        flat(c, Poly(star_pts(x, y, 4, 1.6, points=4, rot=0)), rnd.choice([(250, 200, 60), (120, 220, 240), (240, 100, 180)]))
    # row of cabinets
    marquees = [(230, 60, 60), (60, 120, 220), (250, 200, 60), (120, 200, 120), (200, 100, 220)]
    screens = [(60, 120, 200), (200, 80, 60), (40, 160, 90), (220, 180, 60), (90, 60, 160)]
    for k, x in enumerate((190, 320, 450, 580, 710)):
        mq = marquees[k] if not (k == 3 and "marquee" in d) else (250, 140, 40)
        cabinet(c, x, 450, (50, 50, 70), mq, screens[k], 1590 + k)
    # token counter (right) with the attendant behind it
    modern(c, 826, 380, (240, 240, 236), bottom=(50, 50, 60), hair=(40, 30, 30), h=2.0)
    piece(c, RRect(790, 300, 900, 450, 2), (150, 60, 50), border=1.5, border_col=NIGHT_EDGE, shadow=PROP)
    flat(c, RRect(796, 300, 900, 312, 0), (200, 180, 140))
    jar = (230, 200, 90) if "tokens" not in d else (200, 200, 210)
    piece(c, [RRect(850, 236, 896, 300, 8)], (200, 230, 240, 0.8), border=1, border_col=NIGHT_EDGE, shadow=SMALL)
    flat(c, RRect(854, 262, 892, 296, 6), jar)
    flat(c, RRect(848, 230, 898, 240, 2), (220, 60, 60))
    # vending: fan on the counter
    flat(c, Thick(36, 440, 36, 300, 4), (90, 90, 96))
    # empty stools in front of the free cabinets
    for x in (320, 580):
        stool = (220, 60, 60) if not (x == 320 and "stool" in d) else (60, 120, 220)
        piece(c, [Ell(x, 500, 30, 10), RRect(x - 4, 500, x + 4, 570, 2), Ell(x, 572, 22, 5)], stool, border=1, border_col=NIGHT_EDGE, shadow=PROP)
    # kids playing at the cabinets
    for x, top, hair in ((190, (240, 240, 236), (40, 30, 30)), (450, (230, 120, 60), (40, 30, 30)), (710, (60, 140, 210), (90, 60, 40))):
        modern(c, x, 592, top, bottom=(50, 60, 90), hair=hair, h=2.4)
    # kid watching with a drink
    hx, hy = modern(c, 620, 598, (240, 200, 60) if "shirt" not in d else (120, 200, 120), bottom=(50, 60, 90), hair=(40, 30, 30), h=2.5)
    piece(c, RRect(640, 498, 656, 526, 2), (230, 60, 60), shadow=SMALL)


def l159_screen(x, w=110, h=230, base=450):
    r = (x - w / 2 + 18, base - h * 0.8, x + w / 2 - 18, base - h * 0.58)

    def d(c, m):
        soft_union(c, [RRect(*r, 2)], (180, 220, 255), 0.3, spread=12)
        flat(c, RRect(r[0] + 8, r[3] - 14, r[0] + 16, r[3] - 6, 0), (250, 250, 250))
    return E("scr%d" % x, d, daynight="untinted", anim=dict(twinkle=0.35, twinkleSpeed=2.5, phase=(x * 0.01) % 1))


L159_ELEMENTS = [l159_screen(x) for x in (190, 320, 450, 580, 710)] + [
    E("tube%d" % x, (lambda x: lambda c, m: soft_union(c, [RRect(x - 90, 10, x + 90, 22, 4)], (230, 240, 255), 0.5, spread=16))(x), daynight="untinted",
      anim=dict(twinkle=0.15 if x != 750 else 0.6, twinkleSpeed=1.0 if x != 750 else 6.0)) for x in (150, 450, 750)
] + [
    E("fan", lambda c, m: (flat(c, Circ(36, 290, 30), (200, 200, 210, 0.5)), flat(c, [Ell(36, 290, 28, 6), Ell(36, 290, 6, 28)], (220, 220, 230))),
      pivot=(36, 290), anim=dict(rotateSpeed=360)),
]

L159_DIFFS = [
    ("poster", 96, 130, 0),
    ("marquee", 580, 236, 0),
    ("tokens", 873, 280, 0),
    ("stool", 320, 520, 0),
    ("shirt", 621, 526, 0),
]


LEVELS = [
    ("Level155", "游戏卧室", l155_bg, L155_ELEMENTS, L155_DIFFS, 60, OPTS),
    ("Level156", "卡带店", l156_bg, L156_ELEMENTS, L156_DIFFS, 60, OPTS),
    ("Level157", "像素平台", l157_bg, L157_ELEMENTS, L157_DIFFS, 60, OPTS),
    ("Level158", "像素太空", l158_bg, L158_ELEMENTS, L158_DIFFS, 60, OPTS),
    ("Level159", "街机厅", l159_bg, L159_ELEMENTS, L159_DIFFS, 60, OPTS),
]
