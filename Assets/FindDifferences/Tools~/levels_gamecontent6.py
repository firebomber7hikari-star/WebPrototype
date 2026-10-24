# -*- coding: utf-8 -*-
"""Inside video games, part 6 (all designs original: no real games, characters, brands or logos):
  Level225 果冻堆叠 - a falling jelly-pair puzzle: well of stacked jelly blobs, next pairs, score, mascot
  Level226 打砖块   - a brick-breaker stage: brick wall, paddle, ball, power-up capsules, lives
  Level227 清版动作 - a side-scrolling brawler street: shop fronts, chibi hero vs. cartoon thugs, crates, HP bars
  Level228 贪吃蛇   - a garden snake game: tiled lawn, long snake, fruits, rocks, score
  Level229 打地鼠   - a whack-a-mole booth: holes with popping moles, hammer, timer, prize shelf
  Level230 星际星图 - a space strategy map: star systems and lanes, territories, fleets, resource bar
  Level231 挖矿沙盒 - a 2D digging sandbox: surface village, tunnels, ores, cave lake, hotbar
  Level232 魔法学院 - a magic-school classroom RPG: cauldron, floating books, students, quest panel
  Level233 海盗航海 - a top-down pirate sailing map: islands, ships, treasure mark, sea monster, compass
  Level234 恐龙乐园 - an isometric dinosaur-park builder: paddocks, dinosaurs, visitors, shop, build menu
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, PROP, SMALL, drift_across
from levels_retro import block, digits, sprite
from levels_gamecontent import OUTLINE, glyph_line, toon
from levels_gamecontent2 import bar, chibi
from levels_gamecontent3 import heart, panel

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
SKIN = (250, 220, 190)
BLOCK_COLS = {"r": (230, 70, 70), "o": (245, 150, 50), "y": (245, 210, 60), "g": (90, 190, 90), "c": (70, 190, 220), "b": (70, 110, 220),
              "p": (170, 90, 210)}


# =================================================================== Level 225 falling jelly-pair puzzle
def jelly(c, x, y, col, r=15):
    toon(c, Ell(x, y + 1, r, r - 1), col, w=1.6, shadow=None)
    flat(c, Ell(x - r * 0.35, y - r * 0.4, r * 0.3, r * 0.2), lit(col, 1.35))
    flat(c, [Circ(x - r * 0.3, y + 1, r * 0.14), Circ(x + r * 0.3, y + 1, r * 0.14)], (50, 40, 60))
WELL = ["..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "....p.....",
        "...ppp....",
        "y........c",
        "yy..gg..cc",
        "ry.ggo.bbc",
        "rrrbbooob.",
        "rcccbyoyyg",
        "ppcgggyyrg",
        ".pprrbbbrr"]
WX, WY, WS = 300, 50, 34


def l225_bg(c, d):
    c.gradient(0, H, (60, 50, 110), (120, 80, 150))
    rnd = random.Random(2251)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        flat(c, Poly(star_pts(x, y, rnd.choice((2, 3, 4)), 1, points=4, rot=0)), (230, 220, 255))
    # city silhouette in the background
    for k, x in enumerate(range(-20, W, 60)):
        h = 80 + (k * 37 % 90)
        flat(c, RRect(x, H - h, x + 54, H, 0), (80, 64, 130))
        for wy in range(int(H - h + 12), H - 10, 18):
            flat(c, RRect(x + 10, wy, x + 18, wy + 8, 0), (250, 220, 120) if (k + wy) % 3 else (100, 84, 150))
    # well
    toon(c, RRect(WX - 12, WY - 12, WX + 10 * WS + 12, WY + 16 * WS + 12, 10), (40, 34, 70), w=2.4)
    flat(c, RRect(WX, WY, WX + 10 * WS, WY + 16 * WS, 0), (24, 20, 46))
    for i in range(1, 10):
        flat(c, Thick(WX + i * WS, WY, WX + i * WS, WY + 16 * WS, 1), (36, 32, 64))
    for j in range(1, 16):
        flat(c, Thick(WX, WY + j * WS, WX + 10 * WS, WY + j * WS, 1), (36, 32, 64))
    for j, row in enumerate(WELL):
        for i, ch in enumerate(row):
            if (i, j) == (3, 10) and "block" in d:
                ch = "."
            if (i, j) == (6, 15) and "colour" in d:
                ch = "g"
            if ch in BLOCK_COLS:
                jelly(c, WX + (i + 0.5) * WS, WY + (j + 0.5) * WS, BLOCK_COLS[ch])
    # left panel: hold box + score
    panel(c, 40, 50, 250, 190, (250, 246, 236))
    glyph_line(c, 60, 160, 72, (120, 100, 140), 2252, w=1.8, size=9)
    jelly(c, 128, 124, BLOCK_COLS["g"] if "hold" not in d else BLOCK_COLS["o"], r=17)
    jelly(c, 166, 124, BLOCK_COLS["p"], r=17)
    panel(c, 40, 220, 250, 330, (250, 246, 236))
    glyph_line(c, 60, 160, 242, (120, 100, 140), 2253, w=1.8, size=9)
    digits(c, 60, 270, "128450", (90, 70, 120), 5)
    panel(c, 40, 360, 250, 440, (250, 246, 236))
    glyph_line(c, 60, 130, 382, (120, 100, 140), 2254, w=1.8, size=9)
    digits(c, 160, 374, "12", (220, 80, 80), 6)
    # right panel: next pieces
    panel(c, 668, 50, 860, 330, (250, 246, 236))
    glyph_line(c, 690, 780, 72, (120, 100, 140), 2255, w=1.8, size=9)
    jelly(c, 746, 122, BLOCK_COLS["c"], r=17)
    jelly(c, 784, 122, BLOCK_COLS["y"], r=17)
    jelly(c, 746, 202, BLOCK_COLS["r"] if "next" not in d else BLOCK_COLS["b"], r=17)
    jelly(c, 784, 202, BLOCK_COLS["r"] if "next" not in d else BLOCK_COLS["b"], r=17)
    jelly(c, 746, 282, BLOCK_COLS["g"], r=17)
    jelly(c, 784, 282, BLOCK_COLS["o"], r=17)
    # mascot (round cat-blob) cheering, bottom right
    mc = (250, 170, 200)
    toon(c, [Ell(770, 520, 70, 58), Poly([(712, 486), (722, 440), (748, 474)]), Poly([(828, 486), (818, 440), (792, 474)])], mc, w=2.2)
    for ex in (746, 794):
        flat(c, Ell(ex, 512, 7, 10), (50, 40, 60))
        flat(c, Circ(ex + 2, 508, 2.4), (250, 250, 250))
    flat(c, Poly([(762, 534), (778, 534), (770, 544)]), (230, 90, 110))
    flat(c, [Ell(728, 534, 9, 5), Ell(812, 534, 9, 5)], (250, 130, 150))
    bow = (250, 220, 70) if "mascot" not in d else (90, 200, 230)
    toon(c, [Poly([(770, 462), (744, 446), (744, 478)]), Poly([(770, 462), (796, 446), (796, 478)])], bow, w=1.6, shadow=None)
    flat(c, Circ(770, 462, 7), lit(bow, 0.85))
    # combo badge, bottom left
    badge = (250, 200, 60) if "badge" not in d else (90, 210, 140)
    toon(c, Poly(star_pts(140, 530, 70, 46, points=10)), badge, w=2.2)
    flat(c, [Thick(110, 520, 126, 540, 4), Thick(126, 520, 110, 540, 4)], (200, 60, 60))
    digits(c, 134, 512, "4", (200, 60, 60), 6)


L225_ELEMENTS = [
    E("falling", lambda c, m: [jelly(c, WX + 5.5 * WS, WY + 1.5 * WS, BLOCK_COLS["o"]), jelly(c, WX + 5.5 * WS, WY + 2.5 * WS, BLOCK_COLS["c"])],
      pivot=(WX + 5.5 * WS, WY + 2 * WS), anim=dict(bobAmplitude=(0, 30), bobSpeed=0.25)),
    E("arms", lambda c, m: toon(c, [Ell(694, 500, 14, 10), Ell(846, 500, 14, 10)], (250, 170, 200), w=1.6, shadow=None), pivot=(770, 500),
      anim=dict(bobAmplitude=(0, 8), bobSpeed=1.2, bounce=True)),
    E("spark", lambda c, m: [flat(c, Poly(star_pts(x, y, 12, 3, points=4, rot=0)), (255, 255, 220)) for x, y in ((220, 460), (60, 600 - 140), (640, 380))],
      daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.8)),
]

L225_DIFFS = [
    ("hold", 128, 124, 0),
    ("block", WX + 3.5 * WS, WY + 10.5 * WS, 0),
    ("colour", WX + 6.5 * WS, WY + 15.5 * WS, 0),
    ("next", 765, 202, 0),
    ("mascot", 770, 462, 0),
    ("badge", 140, 530, 0),
]


# =================================================================== Level 226 brick breaker
BRICKS = ["rrrrrrrrrrr",
          "oooooooooo.",
          "yyy.yyyyyyy",
          "ggggggg.ggg",
          "ccccccccccc",
          ".bbbbb.bbbb"]
BX, BY, BW, BH = 60, 70, 70, 28


def l226_bg(c, d):
    c.gradient(0, H, (30, 40, 80), (70, 40, 100))
    # grid floor glow
    for x in range(0, W + 1, 45):
        flat(c, Thick(x, 360, 450 + (x - 450) * 1.8, 600, 1.4), (90, 70, 150))
    for k, y in enumerate((380, 410, 450, 500, 560)):
        flat(c, Thick(0, y, W, y, 1.4), (90, 70, 150))
    # side walls (pipes)
    for x in (20, 860):
        toon(c, RRect(x, 50, x + 20, 600, 6), (160, 170, 200), w=2)
        for y in range(80, 600, 70):
            flat(c, RRect(x - 2, y, x + 22, y + 8, 2), (110, 120, 150))
    toon(c, RRect(20, 30, 880, 52, 6), (160, 170, 200), w=2)
    # bricks
    for j, row in enumerate(BRICKS):
        for i, ch in enumerate(row):
            if (i, j) == (9, 0) and "brick" in d:
                ch = "."
            if (i, j) == (2, 4) and "colour" in d:
                ch = "p"
            if ch in BLOCK_COLS:
                x, y = BX + i * BW, BY + j * BH
                toon(c, RRect(x + 2, y + 2, x + BW - 2, y + BH - 2, 4), BLOCK_COLS[ch], w=1.4, shadow=None)
                flat(c, RRect(x + 6, y + 5, x + BW - 6, y + 9, 2), lit(BLOCK_COLS[ch], 1.3))
    # metal (unbreakable) blocks
    for x in (200, 620):
        toon(c, RRect(x, 270, x + 80, 296, 4), (180, 186, 200) if not (x == 620 and "metal" in d) else (240, 190, 70), w=1.6, shadow=None)
        flat(c, [Circ(x + 10, 283, 3), Circ(x + 70, 283, 3)], (120, 126, 140))
    # paddle
    pad = (240, 90, 90) if "paddle" not in d else (90, 200, 120)
    toon(c, [RRect(380, 530, 520, 550, 10)], (200, 206, 220), w=2)
    toon(c, [RRect(374, 530, 400, 550, 8)], (240, 90, 90), w=1.6, shadow=None)
    toon(c, [RRect(500, 530, 526, 550, 8)], pad, w=1.6, shadow=None)
    # HUD: lives + score + stage
    for k in range(3):
        if k == 2 and "life" in d:
            continue
        toon(c, RRect(44 + k * 50, 570, 84 + k * 50, 584, 6), (240, 90, 90), w=1.4, shadow=None)
    digits(c, 620, 566, "004920", (250, 240, 200), 4)
    panel(c, 330, 4, 570, 28, (250, 240, 220), r=6, w=1.4)
    glyph_line(c, 350, 470, 16, (120, 100, 140), 2261, w=1.6, size=8)
    digits(c, 500, 8, "07", (200, 60, 60), 4)
    # lasers turrets at the bottom corners
    for x in (70, 790):
        tc = (120, 130, 170)
        if (x == 70 and "turretL" in d) or (x == 790 and "turretR" in d):
            tc = (230, 120, 70)
        toon(c, [RRect(x, 470, x + 40, 520, 6), RRect(x + 14, 440, x + 26, 470, 3)], tc, w=1.6)


L226_ELEMENTS = [
    E("ball", lambda c, m: [soft_union(c, [Circ(470, 420, 9)], (255, 255, 200), 0.5, spread=12), toon(c, Circ(470, 420, 9), (250, 250, 240), w=1.4, shadow=None)],
      pivot=(470, 420), daynight="untinted", anim=dict(orbitRadius=(120, 70), orbitSpeed=0.25)),
    E("capsule", lambda c, m: [toon(c, RRect(280, 330, 330, 352, 11), (90, 200, 240), w=1.6, shadow=None), digits(c, 298, 334, "1", (250, 250, 250), 3)],
      pivot=(305, 341), anim=dict(bobAmplitude=(0, 40), bobSpeed=0.3)),
    E("capsule2", lambda c, m: toon(c, RRect(560, 360, 610, 382, 11), (250, 160, 60), w=1.6, shadow=None), pivot=(585, 371),
      anim=dict(bobAmplitude=(0, 30), bobSpeed=0.35, phase=0.5)),
    E("spark", lambda c, m: [flat(c, Poly(star_pts(x, y, 9, 2, points=4, rot=0)), (255, 255, 220)) for x, y in ((150, 240), (760, 230), (450, 300))],
      daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.9)),
]

L226_DIFFS = [
    ("brick", BX + 9.5 * BW, BY + 0.5 * BH, 0),
    ("colour", BX + 2.5 * BW, BY + 4.5 * BH, 0),
    ("metal", 660, 283, 0),
    ("turretL", 90, 485, 0),
    ("turretR", 810, 485, 0),
    ("paddle", 513, 540, 0),
    ("life", 164, 577, 0),
]


# =================================================================== Level 227 side-scrolling brawler
def thug(c, x, base, s, shirt, hair=(60, 40, 30), face=-1, hat=None):
    """Cartoon street-tough (no weapons): big jaw, sleeveless shirt, fists."""
    toon(c, [RRect(x - 12 * s, base - 30 * s, x - 3 * s, base, 3), RRect(x + 3 * s, base - 30 * s, x + 12 * s, base, 3)], (60, 70, 110))
    toon(c, RRect(x - 18 * s, base - 70 * s, x + 18 * s, base - 28 * s, 8 * s), shirt)
    toon(c, [Circ(x + 22 * s * face, base - 52 * s, 9 * s), Circ(x - 20 * s * face, base - 46 * s, 8 * s)], SKIN, w=1.6, shadow=None)
    toon(c, Ell(x, base - 86 * s, 16 * s, 17 * s), SKIN)
    toon(c, Ell(x, base - 100 * s, 16 * s, 7 * s), hair, w=1.4, shadow=None)
    if hat:
        toon(c, [Ell(x, base - 100 * s, 18 * s, 6 * s), RRect(x - 4 * s * face, base - 102 * s, x + 24 * s * face, base - 96 * s, 2)], hat, w=1.4, shadow=None)
    flat(c, Thick(x + 3 * s * face, base - 88 * s, x + 11 * s * face, base - 90 * s, 2.4 * s), (40, 30, 40))
    flat(c, Thick(x + 2 * s * face, base - 76 * s, x + 10 * s * face, base - 76 * s, 1.6 * s), (40, 30, 40))


def l227_bg(c, d):
    c.gradient(0, 260, (250, 170, 120), (250, 214, 160))
    toon(c, Circ(160, 110, 46), (255, 230, 150), w=0, shadow=None)
    # far skyline
    for k, x in enumerate(range(-20, W, 70)):
        h = 70 + (k * 53 % 80)
        flat(c, RRect(x, 230 - h, x + 64, 240, 0), (200, 130, 120))
    # shop fronts
    shops = [((90, 150, 200), (240, 90, 90)), ((230, 200, 140), (60, 140, 110)), ((200, 120, 150), (250, 200, 70)), ((150, 170, 120), (90, 110, 200))]
    for k, (wall, awn) in enumerate(shops):
        x0 = k * 225
        if k == 2 and "awning" in d:
            awn = (150, 90, 210)
        toon(c, RRect(x0, 110, x0 + 225, 420, 0), wall, w=2, shadow=None)
        for wx in range(x0 + 24, x0 + 200, 66):
            toon(c, RRect(wx, 130, wx + 44, 186, 3), (180, 210, 230) if not (wx == 24 and "window" in d) else (250, 210, 120), w=1.6, shadow=None)
            flat(c, Thick(wx + 22, 130, wx + 22, 186, 2), lit(wall, 0.8))
        toon(c, RRect(x0 + 20, 206, x0 + 205, 236, 4), (250, 246, 236), w=1.6, shadow=None)
        glyph_line(c, x0 + 36, x0 + 190, 221, lit(awn, 0.8), 2271 + k, w=2.2, size=11)
        for s in range(6):
            col = awn if s % 2 == 0 else (250, 250, 246)
            toon(c, Poly([(x0 + 14 + s * 33, 244), (x0 + 47 + s * 33, 244), (x0 + 47 + s * 33, 270), (x0 + 30 + s * 33, 280), (x0 + 14 + s * 33, 270)]),
                 col, w=1.4, shadow=None)
        toon(c, RRect(x0 + 30, 290, x0 + 120, 420, 3), (120, 170, 200), w=1.6, shadow=None)
        toon(c, RRect(x0 + 140, 300, x0 + 196, 420, 3), lit(wall, 0.7) if not (k == 1 and "door" in d) else (240, 190, 90), w=1.6, shadow=None)
    # neon sign on shop 1 (vertical)
    sign = (240, 80, 120) if "sign" not in d else (80, 220, 220)
    toon(c, RRect(300, 40, 340, 190, 6), (40, 36, 56), w=2)
    for k in range(4):
        flat(c, RRect(308, 52 + k * 34, 332, 76 + k * 34, 4), sign)
    # pavement + road
    c.rect(0, 420, W, 470, (190, 186, 196))
    for x in range(0, W, 60):
        flat(c, Thick(x, 420, x - 10, 470, 1.6), (170, 166, 178))
    c.rect(0, 470, W, H, (90, 90, 106))
    for x in range(30, W, 140):
        flat(c, RRect(x, 540, x + 70, 548, 2), (240, 230, 160))
    # street props: hydrant, barrel, crate, phone booth
    hyd = (220, 60, 60) if "hydrant" not in d else (60, 140, 220)
    toon(c, [RRect(70, 380, 100, 440, 6), Ell(85, 378, 18, 8), RRect(60, 400, 110, 410, 3)], hyd, w=1.8)
    if "crate" not in d:
        toon(c, RRect(620, 380, 700, 460, 4), (200, 150, 90), w=2)
        flat(c, [Thick(620, 380, 700, 460, 4), Thick(700, 380, 620, 460, 4)], (160, 110, 60))
    toon(c, [RRect(760, 386, 820, 466, 10), Ell(790, 386, 30, 10)], (120, 120, 140), w=2)
    flat(c, [Thick(764, 410, 816, 410, 3), Thick(764, 440, 816, 440, 3)], (90, 90, 110))
    # HUD
    panel(c, 16, 14, 290, 76, (40, 36, 56))
    toon(c, Circ(48, 45, 22), (250, 220, 190), w=1.6, shadow=None)
    flat(c, Ell(48, 32, 20, 9), (60, 40, 30))
    bar(c, 82, 26, 270, 38, 0.72, (90, 220, 110))
    bar(c, 82, 50, 220, 60, 0.4, (90, 160, 250))
    panel(c, 610, 14, 884, 76, (40, 36, 56))
    bar(c, 640, 26, 860, 38, 0.55, (240, 80, 80) if "boss" not in d else (250, 200, 60))
    glyph_line(c, 640, 760, 58, (250, 240, 220), 2275, w=1.8, size=9)
    # go arrow
    toon(c, Poly([(780, 300), (840, 300), (840, 280), (880, 320), (840, 360), (840, 340), (780, 340)]), (250, 220, 60), w=2)
    # characters on the road
    thug(c, 560, 560, 1.2, (150, 80, 180), hat=(40, 40, 50))
    thug(c, 700, 590, 1.4, (60, 140, 90) if "thug" not in d else (240, 140, 50))
    chibi(c, 330, 590, s=1.6, hair=(40, 30, 40), outfit=(240, 240, 246), face=1)
    flat(c, RRect(310, 548, 350, 556, 2), (220, 40, 50))
    toon(c, Circ(380, 520, 12), SKIN, w=1.6, shadow=None)
    # food pickup on the ground
    toon(c, [Ell(160, 560, 34, 12), Ell(160, 548, 24, 16)], (250, 250, 246), w=1.6)
    toon(c, Ell(160, 540, 18, 10), (220, 140, 70), w=1.2, shadow=None)


L227_ELEMENTS = [
    E("hit", lambda c, m: [flat(c, Poly(star_pts(440, 500, 34, 14, points=8)), (255, 240, 120)), flat(c, Poly(star_pts(440, 500, 18, 8, points=8)), (255, 255, 240))],
      pivot=(440, 500), daynight="untinted", anim=dict(blinkInterval=1.2, blinkDuration=0.4)),
    E("cat", lambda c, m: [toon(c, [Ell(470, 98, 22, 12), Circ(492, 90, 9), Poly([(486, 84), (488, 74), (494, 82)]), Poly([(494, 82), (498, 74), (500, 84)])],
                                  (60, 50, 60), w=1.4, shadow=None)], pivot=(470, 108), anim=dict(bobAmplitude=(0, 2), bobSpeed=0.5)),
    E("smoke", lambda c, m: toon(c, [Circ(860, 100, 18), Circ(876, 86, 14)], (230, 220, 220), w=1.2, shadow=None), pivot=(866, 92),
      anim=dict(driftVelocity=(-10, -20), driftLength=60, driftFade=True, driftGrow=1.4)),
    E("arrow", lambda c, m: flat(c, Poly([(784, 304), (836, 304), (836, 336), (784, 336)]), (255, 250, 200, 0.5)), daynight="untinted",
      anim=dict(blinkInterval=0.8, blinkDuration=0.4)),
]

L227_DIFFS = [
    ("awning", 562, 262, 0),
    ("door", 393, 360, 0),
    ("window", 46, 158, 0),
    ("sign", 320, 115, 0),
    ("hydrant", 85, 410, 0),
    ("crate", 660, 420, 0),
    ("boss", 750, 32, 0),
    ("thug", 700, 510, 0),
]


# =================================================================== Level 228 snake game
SN = 40
SNAKE = [(3, 11), (4, 11), (5, 11), (6, 11), (6, 10), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (10, 8), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7),
         (14, 6), (14, 5), (15, 5)]


def cell(i, j):
    return 30 + i * SN + SN / 2, 60 + j * SN + SN / 2


def fruit(c, x, y, kind, s=1.0):
    if kind == "apple":
        toon(c, Circ(x, y, 14 * s), (230, 70, 70), w=1.6, shadow=None)
        flat(c, Thick(x, y - 12 * s, x + 3 * s, y - 20 * s, 2.4), (110, 80, 50))
        flat(c, Ell(x + 8 * s, y - 18 * s, 6 * s, 3 * s), (90, 180, 90))
    elif kind == "pear":
        toon(c, [Circ(x, y + 4 * s, 13 * s), Circ(x, y - 8 * s, 8 * s)], (200, 220, 90), w=1.6, shadow=None)
    elif kind == "grape":
        toon(c, [Circ(x + dx * s, y + dy * s, 6 * s) for dx, dy in ((-7, -6), (0, -6), (7, -6), (-4, 2), (4, 2), (0, 10))], (150, 80, 190), w=1.2, shadow=None)
    elif kind == "melon":
        toon(c, Ell(x, y, 17 * s, 13 * s), (90, 170, 80), w=1.6, shadow=None)
        flat(c, [Thick(x - 10 * s, y - 8 * s, x - 10 * s, y + 8 * s, 2), Thick(x, y - 12 * s, x, y + 12 * s, 2), Thick(x + 10 * s, y - 8 * s, x + 10 * s, y + 8 * s, 2)],
             (60, 130, 60))
    elif kind == "berry":
        toon(c, Poly([(x - 12 * s, y - 6 * s), (x + 12 * s, y - 6 * s), (x, y + 14 * s)]), (230, 60, 90), w=1.4, shadow=None)
        flat(c, Ell(x, y - 8 * s, 10 * s, 4 * s), (80, 170, 80))


def l228_bg(c, d):
    c.rect(0, 0, W, H, (110, 80, 60))
    # board
    toon(c, RRect(22, 52, 30 + 21 * SN + 8, 60 + 13 * SN + 8, 10), (90, 150, 70), w=2.4)
    for i in range(21):
        for j in range(13):
            x, y = 30 + i * SN, 60 + j * SN
            flat(c, RRect(x, y, x + SN, y + SN, 0), (150, 206, 110) if (i + j) % 2 else (140, 196, 100))
    # rocks
    for (i, j) in ((2, 2), (17, 10), (12, 2)):
        x, y = cell(i, j)
        if (i, j) == (17, 10) and "rock" in d:
            continue
        toon(c, [Ell(x, y + 4, 18, 13), Ell(x - 6, y - 4, 10, 8)], (150, 146, 156), w=1.6, shadow=(0, 2, 3, 0.25))
    # flowers / bushes on the board
    for (i, j) in ((19, 1), (1, 7), (8, 1)):
        x, y = cell(i, j)
        col = (250, 200, 60) if not ((i, j) == (8, 1) and "flower" in d) else (230, 110, 200)
        flat(c, [Circ(x + 8 * math.cos(a * 1.2566), y + 8 * math.sin(a * 1.2566), 7) for a in range(5)], col)
        flat(c, Circ(x, y, 5), (250, 250, 240))
    # fruits
    fruits = [((4, 3), "apple"), ((16, 11), "grape"), ((9, 12), "melon"), ((19, 6), "pear"), ((2, 9), "berry")]
    for (i, j), kind in fruits:
        x, y = cell(i, j)
        if (i, j) == (2, 9) and "fruit" in d:
            kind = "apple"
        fruit(c, x, y, kind)
    # snake
    body = (90, 140, 230) if "snake" not in d else (240, 150, 60)
    for k, (i, j) in enumerate(SNAKE):
        x, y = cell(i, j)
        col = body if 11 <= k < 14 else (90, 140, 230)
        toon(c, RRect(x - 17, y - 17, x + 17, y + 17, 10), col, w=1.6, shadow=None)
        flat(c, Circ(x, y, 5), lit(col, 1.25))
    hx, hy = cell(*SNAKE[-1])
    toon(c, RRect(hx - 19, hy - 19, hx + 19, hy + 19, 12), (90, 140, 230), w=1.8, shadow=None)
    for ey in (hy - 8, hy + 8):
        flat(c, Circ(hx + 6, ey, 5), (250, 250, 250))
        flat(c, Circ(hx + 8, ey, 2.4), (40, 30, 40))
    flat(c, Poly([(hx + 18, hy), (hx + 30, hy - 4), (hx + 26, hy), (hx + 30, hy + 4)]), (230, 70, 90))
    # HUD top
    panel(c, 30, 8, 250, 46, (250, 246, 236), r=8, w=1.6)
    fruit(c, 54, 27, "apple", 0.8)
    digits(c, 80, 16, "0190", (120, 90, 70), 5)
    panel(c, 640, 8, 870, 46, (250, 246, 236), r=8, w=1.6)
    for k in range(3):
        heart(c, 670 + k * 34, 27, 1.35, (230, 70, 90) if not (k == 2 and "heart" in d) else (200, 200, 210))
    glyph_line(c, 780, 860, 27, (120, 90, 70), 2281, w=1.8, size=9)
    # fence + wooden frame decoration at the bottom
    c.rect(0, 588, W, H, (130, 96, 70))
    for x in range(0, W, 30):
        flat(c, RRect(x + 4, 586, x + 26, 600, 2), (170, 130, 90))


L228_ELEMENTS = [
    E("tongue", lambda c, m: flat(c, Thick(*[v + o for v, o in zip(cell(15, 5), (20, 0))], *[v + o for v, o in zip(cell(15, 5), (34, 0))], 2.4), (230, 70, 90)),
      pivot=cell(15, 5), anim=dict(blinkInterval=0.9, blinkDuration=0.4)),
    E("bee", lambda c, m: [toon(c, Ell(400, 120, 10, 7), (250, 210, 60), w=1.2, shadow=None), flat(c, Thick(400, 113, 400, 127, 2), (40, 30, 40)),
                           flat(c, [Ell(396, 110, 5, 4), Ell(404, 110, 5, 4)], (240, 250, 255))], pivot=(400, 120),
      anim=dict(orbitRadius=(80, 30), orbitSpeed=0.2)),
    E("glint", lambda c, m: [flat(c, Poly(star_pts(*cell(i, j), 10, 2, points=4, rot=0)), (255, 255, 230)) for i, j in ((4, 3), (19, 6))], daynight="untinted",
      anim=dict(twinkle=1, twinkleSpeed=0.8)),
]

L228_DIFFS = [
    ("rock", *cell(17, 10), 0),
    ("flower", *cell(8, 1), 0),
    ("fruit", *cell(2, 9), 0),
    ("snake", *cell(13, 7), 0),
    ("heart", 738, 26, 0),
]


# =================================================================== Level 229 whack-a-mole booth
HOLES = [(200, 330), (450, 330), (700, 330), (260, 450), (640, 450), (450, 520)]


def mole(c, x, y, s=1.0, col=(150, 100, 70), hat=None):
    toon(c, [Ell(x, y - 20 * s, 30 * s, 34 * s)], col, w=2)
    flat(c, Ell(x, y - 6 * s, 20 * s, 16 * s), lit(col, 1.3))
    for ex in (x - 10 * s, x + 10 * s):
        flat(c, Circ(ex, y - 34 * s, 4 * s), (40, 30, 40))
    toon(c, Ell(x, y - 22 * s, 9 * s, 6 * s), (240, 130, 140), w=1.2, shadow=None)
    if hat:
        toon(c, [RRect(x - 22 * s, y - 56 * s, x + 22 * s, y - 50 * s, 2), RRect(x - 14 * s, y - 72 * s, x + 14 * s, y - 54 * s, 3)], hat, w=1.4, shadow=None)


def l229_bg(c, d):
    # booth back wall with stripes
    for k, x in enumerate(range(0, W, 60)):
        flat(c, RRect(x, 0, x + 60, 250, 0), (240, 90, 90) if k % 2 else (250, 240, 220))
    # header sign with bulbs
    toon(c, RRect(220, 16, 680, 96, 16), (60, 60, 140), w=2.4)
    glyph_line(c, 260, 640, 56, (250, 220, 90), 2291, w=4, size=20)
    # prize shelf (plushies)
    toon(c, RRect(20, 120, 260, 134, 3), (170, 120, 70), w=1.6)
    toon(c, RRect(640, 120, 880, 134, 3), (170, 120, 70), w=1.6)
    for k, (x, col) in enumerate(((60, (250, 200, 210)), (130, (190, 220, 250)), (200, (250, 230, 150)), (680, (200, 240, 190)), (750, (250, 190, 140)),
                                  (820, (220, 200, 250)))):
        if k == 4 and "plush" in d:
            col = (120, 200, 200)
        toon(c, [Ell(x, 100, 26, 22), Circ(x - 16, 80, 9), Circ(x + 16, 80, 9)], col, w=1.6)
        flat(c, [Circ(x - 8, 96, 2.6), Circ(x + 8, 96, 2.6)], (50, 40, 50))
    # timer clock (left) + score board (right)
    clock = (250, 200, 60) if "clock" not in d else (110, 200, 240)

    # cup of balls on the left wall
    toon(c, [RRect(70, 170, 150, 230, 8)], (250, 200, 60), w=2)
    for k in range(3):
        toon(c, Circ(90 + k * 20, 166, 10), [(240, 90, 90), (90, 160, 230), (90, 200, 120)][k], w=1.2, shadow=None)
    toon(c, RRect(700, 160, 860, 240, 8), (40, 40, 60), w=2)
    digits(c, 720, 180, "0350", (250, 220, 90), 8)
    # table top (mole board)
    c.rect(0, 250, W, H, (120, 80, 60))
    toon(c, Poly([(40, 250), (860, 250), (900, 600), (0, 600)]), (90, 180, 110), w=2.4, shadow=None)
    flat(c, Poly([(60, 262), (840, 262), (876, 596), (24, 596)]), (110, 196, 120))
    for x in range(80, 860, 60):
        flat(c, Thick(x, 262, x + (x - 450) * 0.1, 596, 1.4), (100, 186, 112))
    # holes
    for k, (x, y) in enumerate(HOLES):
        toon(c, Ell(x, y, 66, 24), (60, 40, 40), w=2, shadow=None)
        flat(c, Ell(x, y + 4, 58, 16), (30, 20, 24))
    # static moles (two up, one hidden)
    mole(c, 200, 330, hat=(220, 60, 60) if "hat" not in d else (60, 110, 210))
    if "mole" not in d:
        mole(c, 640, 450, col=(170, 120, 80))

    # rim fronts (hide mole bottoms)
    for k, (x, y) in enumerate(HOLES):
        toon(c, Poly([(x - 66, y), (x + 66, y), (x + 60, y + 18), (x - 60, y + 18)]), (110, 196, 120), w=1.6, shadow=None)
    # tickets
    if "ticket" not in d:
        for k in range(4):
            toon(c, RRect(60 + k * 12, 520 - k * 8, 150 + k * 12, 556 - k * 8, 3), (250, 210, 90), w=1.4, shadow=None)
            flat(c, Circ(105 + k * 12, 538 - k * 8, 6), (240, 140, 60))
    # timer clock on the table corner
    toon(c, Circ(848, 556, 38), clock, w=2.2)
    flat(c, Circ(848, 556, 28), (250, 250, 246))
    flat(c, [Thick(848, 556, 848, 536, 3), Thick(848, 556, 864, 564, 3)], (60, 50, 60))


L229_ELEMENTS = [
    E("mole1", lambda c, m: mole(c, 450, 330, col=(160, 110, 80)), pivot=(450, 330), anim=dict(bobAmplitude=(0, 30), bobSpeed=0.6, bounce=True)),
    E("mole2", lambda c, m: mole(c, 450, 520, col=(140, 100, 80)), pivot=(450, 520), anim=dict(bobAmplitude=(0, 26), bobSpeed=0.5, bounce=True, phase=0.4)),
    E("hammer", lambda c, m: [toon(c, Thick(760, 520, 700, 420, 8), (200, 160, 110), w=1.6), toon(c, RRect(660, 380, 740, 430, 12), (240, 80, 80), w=2),
                              flat(c, RRect(664, 386, 676, 424, 6), (250, 250, 246))], pivot=(760, 520), anim=dict(swingAngle=18, swingSpeed=0.8)),
    E("bulbs", lambda c, m: [flat(c, Circ(240 + k * 38, 22 if k % 2 else 90, 5), (255, 240, 160)) for k in range(12)], daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.4)),
    E("star", lambda c, m: flat(c, Poly(star_pts(450, 260, 22, 9, points=5)), (255, 230, 90)), pivot=(450, 260), daynight="untinted",
      anim=dict(blinkInterval=1.6, blinkDuration=0.5)),
]

L229_DIFFS = [
    ("plush", 750, 96, 0),
    ("clock", 848, 556, 0),
    ("hat", 200, 270, 0),
    ("mole", 640, 420, 0),
    ("ticket", 120, 525, 0),
]


# =================================================================== Level 230 space strategy map
SYSTEMS = [(120, 150, "b"), (260, 100, "b"), (230, 260, "b"), (380, 200, "n"), (470, 330, "n"), (560, 140, "r"), (700, 230, "r"), (640, 420, "n"),
           (800, 360, "r"), (330, 450, "b"), (120, 420, "n"), (780, 110, "r")]
LANES = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 9), (3, 4), (3, 5), (4, 7), (4, 9), (5, 6), (5, 11), (6, 8), (6, 7), (7, 8), (9, 10), (0, 10)]
OWN = {"b": (80, 150, 250), "r": (240, 90, 90), "n": (180, 180, 190)}


def l230_bg(c, d):
    c.gradient(0, H, (14, 16, 40), (30, 20, 56))
    rnd = random.Random(2301)
    for _ in range(140):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        flat(c, Circ(x, y, rnd.choice((0.8, 1.2, 1.8))), (220, 220, 255))
    # nebulae
    soft_union(c, [Ell(300, 300, 160, 90)], (120, 60, 160), 0.35, spread=60)
    soft_union(c, [Ell(700, 260, 140, 110)], (60, 100, 170), 0.3, spread=60)
    # territories
    for x, y, own in SYSTEMS:
        if own != "n":
            soft_union(c, [Circ(x, y, 60)], OWN[own], 0.18, spread=30)
    # lanes
    for a, b in LANES:
        (x0, y0, _), (x1, y1, _) = SYSTEMS[a], SYSTEMS[b]
        flat(c, Thick(x0, y0, x1, y1, 2), (110, 120, 170))
    # systems
    for k, (x, y, own) in enumerate(SYSTEMS):
        if k == 11 and "owner" in d:
            own = "b"
            toon(c, [Thick(x + 14, y - 12, x + 14, y - 46, 2.4), Poly([(x + 16, y - 46), (x + 44, y - 38), (x + 16, y - 28)])], OWN["b"], w=1.2, shadow=None)
        col = (255, 230, 150) if k % 3 else (200, 220, 255)
        soft_union(c, [Circ(x, y, 10)], col, 0.5, spread=12)
        toon(c, Circ(x, y, 9), col, w=1.4, shadow=None)
        c.ellipse_ring(x, y, 18, 18, 2.4, OWN[own])
        flat(c, RRect(x - 24, y + 22, x + 24, y + 32, 3), (40, 44, 70))
        glyph_line(c, x - 20, x + 22, y + 27, (200, 210, 240), 2302 + k, w=1.2, size=6)
    # space station
    if "station" not in d:
        toon(c, [RRect(36, 290, 56, 310, 2), RRect(84, 290, 104, 310, 2)], (90, 140, 220), w=1.2, shadow=None)
        toon(c, Circ(70, 300, 16), (200, 206, 220), w=1.6, shadow=None)
        flat(c, Circ(70, 300, 6), (250, 200, 80))
    # ringed planet decoration (system 4)
    planet = (200, 150, 110) if "planet" not in d else (110, 190, 140)
    toon(c, Circ(470, 330, 22), planet, w=1.6, shadow=None)
    c.ellipse_ring(470, 330, 36, 10, 3, (230, 210, 170))
    # fleets (chevrons) along lanes
    for x, y, col, ang in ((180, 120, OWN["b"], 0), (640, 190, OWN["r"], 3.6), (300, 360, OWN["b"], 1.2)):
        flat(c, Poly([(x + 14 * math.cos(ang), y + 14 * math.sin(ang)), (x + 10 * math.cos(ang + 2.4), y + 10 * math.sin(ang + 2.4)),
                      (x, y), (x + 10 * math.cos(ang - 2.4), y + 10 * math.sin(ang - 2.4))]), col)
    # top resource bar
    panel(c, 10, 8, 890, 44, (30, 34, 60), r=8, w=1.6)
    for k, col in enumerate(((250, 200, 60), (120, 220, 160), (150, 170, 250), (240, 120, 200))):

        flat(c, Circ(40 + k * 150, 26, 9), col)
        digits(c, 56 + k * 150, 18, str(1200 + k * 345), (220, 230, 250), 3)
    # side panel: selected system
    panel(c, 690, 470, 890, 590, (30, 34, 60), r=10, w=1.6)
    toon(c, Circ(730, 520, 26), (200, 150, 110) if "res" not in d else (110, 160, 230), w=1.4, shadow=None)
    glyph_line(c, 770, 870, 500, (220, 230, 250), 2310, w=1.6, size=8)
    for k in range(3):
        bar(c, 770, 520 + k * 20, 870, 528 + k * 20, 0.3 + k * 0.25, [(250, 200, 60), (120, 220, 160), (150, 170, 250)][k])
    # minimap
    panel(c, 10, 470, 200, 590, (30, 34, 60), r=10, w=1.6)
    for x, y, own in SYSTEMS:
        flat(c, Circ(20 + x * 0.2, 476 + y * 0.18, 3), OWN[own])
    flat(c, RRect(60, 500, 120, 540, 2), (250, 250, 250, 0.15))
    # comet
    if "comet" not in d:
        soft_union(c, [Poly([(240, 570), (320, 520), (246, 578)])], (200, 230, 255), 0.5, spread=8)
        toon(c, Circ(242, 574, 7), (240, 250, 255), w=1.2, shadow=None)


L230_ELEMENTS = [
    E("fleet", lambda c, m: flat(c, Poly([(400, 410), (388, 402), (392, 410), (388, 418)]), OWN["r"]), pivot=(394, 410),
      anim=dict(bobAmplitude=(40, 0), bobSpeed=0.2)),
    E("pulse", lambda c, m: c.ellipse_ring(380, 200, 26, 26, 2, (250, 250, 250)), pivot=(380, 200), daynight="untinted", anim=dict(pulse=0.3, scaleSpeed=1.0)),
    E("twinkle", lambda c, m: [flat(c, Poly(star_pts(x, y, 6, 1.5, points=4, rot=0)), (255, 255, 255)) for x, y in ((60, 300), (520, 60), (860, 200), (400, 560))],
      daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.6)),
]

L230_DIFFS = [
    ("owner", 800, 92, 0),
    ("planet", 470, 330, 0),
    ("res", 730, 520, 0),
    ("comet", 270, 550, 0),
    ("station", 70, 300, 0),
]


# =================================================================== Level 231 2D digging sandbox
T231 = 30
DIRT, STONE = (150, 104, 70), (120, 116, 128)


def l231_bg(c, d):
    c.gradient(0, 150, (130, 200, 250), (210, 236, 250))
    for x, y in ((140, 50), (600, 40)):
        toon(c, [Circ(x, y, 18), Circ(x + 22, y - 6, 22), Circ(x + 46, y, 16)], (250, 250, 250), w=1.4, shadow=None)
    # ground layers (tiles)
    rnd = random.Random(2311)
    for j in range(5, 20):
        for i in range(30):
            x, y = i * T231, j * T231
            if j == 5:
                col = (110, 190, 80)
            elif j < 9:
                col = DIRT
            else:
                col = STONE
            if (i, j) == (15, 10) and "ore" in d:
                col = (90, 210, 230)
            flat(c, RRect(x, y, x + T231, y + T231, 0), col if (i + j) % 2 else lit(col, 0.94))
            if j == 5:
                flat(c, RRect(x, y + 20, x + T231, y + T231, 0), DIRT)
    # tunnels / cave (dark)
    cave = [(i, 9) for i in range(4, 14)] + [(13, j) for j in range(6, 9)] + [(i, 13) for i in range(8, 24)] + [(8, j) for j in range(10, 13)] + \
           [(i, j) for i in range(18, 26) for j in range(15, 18)]
    for i, j in cave:
        flat(c, RRect(i * T231, j * T231, (i + 1) * T231, (j + 1) * T231, 0), (60, 50, 60))
    # underground lake
    for i in range(18, 26):
        for j in (17,):
            flat(c, RRect(i * T231, j * T231 + 6, (i + 1) * T231, (j + 1) * T231, 0), (70, 140, 220))
    # ores
    ores = [((2, 11), (240, 200, 60)), ((6, 15), (90, 210, 230)), ((15, 10), (230, 90, 80)), ((27, 12), (240, 200, 60)), ((11, 17), (190, 120, 230)),
            ((28, 17), (90, 210, 230))]
    for (i, j), col in ores:
        x, y = i * T231, j * T231
        flat(c, [RRect(x + 5, y + 6, x + 13, y + 14, 1), RRect(x + 16, y + 14, x + 24, y + 22, 1), RRect(x + 8, y + 18, x + 14, y + 24, 1)], col)
    # torches in the tunnels
    for i, j in ((6, 9), (12, 13), (20, 13)):
        x, y = i * T231 + 15, j * T231 + 6
        flat(c, RRect(x - 2, y + 4, x + 2, y + 20, 0), (150, 100, 60))
    # surface village: house, tree, chest
    hx = 600
    for j in range(3):
        for i in range(4):
            flat(c, RRect(hx + i * T231, 60 + j * T231, hx + (i + 1) * T231, 90 + j * T231, 0), (200, 150, 100) if (i + j) % 2 else (190, 140, 92))
    roof = (200, 70, 60) if "roof" not in d else (60, 110, 200)
    for k in range(3):
        flat(c, RRect(hx - 15 + k * 15, 60 - (k + 1) * 15, hx + 135 - k * 15, 60 - k * 15, 0), roof)
    flat(c, RRect(hx + 45, 90, hx + 75, 150, 0), (110, 70, 50))
    flat(c, RRect(hx + 90, 75, hx + 115, 100, 0), (170, 220, 250))
    # tree
    tx = 300
    flat(c, RRect(tx, 60, tx + 30, 150, 0), (130, 90, 60))
    leaf = (70, 160, 70)
    for i, j in ((-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, -1), (0, -1), (1, -1), (0, -2), (-2, 1), (-1, 1), (1, 1), (2, 1)):
        flat(c, RRect(tx + i * T231, 40 + j * T231, tx + (i + 1) * T231, 70 + j * T231, 0), leaf if (i + j) % 2 else lit(leaf, 1.12))
    if "apple" not in d:
        flat(c, [RRect(tx - 44, 44, tx - 26, 62, 3), RRect(tx + 52, 62, tx + 70, 80, 3), RRect(tx + 10, 4, tx + 28, 22, 3)], (230, 60, 60))
    # chest on the surface
    chest = (180, 120, 60) if "chest" not in d else (120, 120, 200)
    flat(c, RRect(40, 120, 90, 150, 2), chest)
    flat(c, [RRect(40, 128, 90, 132, 0), RRect(61, 128, 69, 140, 0)], (250, 200, 60))
    # hotbar
    panel(c, 240, 556, 660, 596, (60, 56, 70), r=6, w=1.6)
    for k in range(9):
        x = 250 + k * 45
        flat(c, RRect(x, 562, x + 40, 590, 3), (110, 104, 120) if k != 2 else (250, 220, 120))
        if k == 4 and "slot" in d:
            flat(c, RRect(x, 562, x + 40, 590, 3), (90, 200, 90))
        if k < 6:
            col = [(150, 150, 160), (150, 104, 70), (200, 160, 110), (240, 200, 60), (90, 210, 230), (230, 90, 80)][k]

            flat(c, RRect(x + 10, 568, x + 30, 584, 2), col)
    for k in range(6):
        heart(c, 30 + k * 26, 572, 0.9, (230, 60, 70))


L231_ELEMENTS = [
    E("miner", lambda c, m: [sprite(c, 300, 336, ["..hhh...", ".hsss...", ".sese...", "..ss....", ".bbbb...", "sbbbbs..", ".bbbb...", ".l..l...", ".l..l..."],
                                    {"h": (240, 200, 60), "s": SKIN, "e": (40, 30, 40), "b": (60, 120, 200), "l": (60, 60, 80)}, 6),
                             flat(c, Thick(340, 366, 366, 340, 4), (150, 100, 60)), flat(c, Thick(354, 334, 378, 350, 5), (180, 180, 190))],
      pivot=(324, 390), anim=dict(bobAmplitude=(50, 0), bobSpeed=0.15)),
    E("flames", lambda c, m: [flat(c, Poly([(i * T231 + 11, j * T231 + 10), (i * T231 + 19, j * T231 + 10), (i * T231 + 15, j * T231 - 2)]), (255, 190, 70))
                              for i, j in ((6, 9), (12, 13), (20, 13))], daynight="untinted", anim=dict(twinkle=0.4, twinkleSpeed=3)),
    E("bird", lambda c, m: flat(c, [Thick(500, 40, 508, 46, 2), Thick(508, 46, 516, 40, 2)], (60, 60, 80)), pivot=(508, 44), anim=drift_across(490, 520, 25)),
]

L231_DIFFS = [
    ("roof", 660, 30, 0),
    ("apple", 310, 60, 0),
    ("ore", 15 * T231 + 15, 10 * T231 + 15, 0),
    ("chest", 65, 135, 0),
    ("slot", 450 + 30, 576, 0),
]


# =================================================================== Level 232 magic-school classroom
def l232_bg(c, d):
    # stone walls + arched windows
    c.rect(0, 0, W, 420, (120, 110, 140))
    for r, y in enumerate(range(0, 420, 30)):
        off = (r % 2) * 40
        for x in range(-off, W, 80):
            flat(c, RRect(x + 2, y + 2, x + 78, y + 28, 3), (130, 120, 150) if (x // 80 + r) % 3 else (124, 114, 144))
    for k, x in enumerate((130, 770)):
        toon(c, [RRect(x - 60, 90, x + 60, 300, 4), Ell(x, 90, 60, 60)], (60, 50, 90), w=2.4, shadow=None)
        sky = (60, 60, 130)
        flat(c, [RRect(x - 50, 96, x + 50, 292, 2), Ell(x, 96, 50, 50)], sky)
        flat(c, [Thick(x, 50, x, 292, 4), Thick(x - 50, 180, x + 50, 180, 4)], (60, 50, 90))
        moon = (250, 240, 200) if not (k == 1 and "moon" in d) else (250, 170, 120)
        flat(c, Circ(x + 22, 120, 16), moon)
    # blackboard with runes
    toon(c, RRect(270, 60, 630, 230, 6), (120, 80, 50), w=2.4)
    flat(c, RRect(284, 74, 616, 216, 4), (40, 70, 60))
    for k in range(4):
        glyph_line(c, 300, 600 - k * 40, 96 + k * 30, (230, 240, 230), 2321 + k, w=2, size=12)
    rune = (240, 220, 120) if "rune" not in d else (120, 220, 250)
    c.ellipse_ring(560, 180, 30, 30, 3, rune)
    flat(c, Poly(star_pts(560, 180, 26, 10, points=5)), rune)
    # banners of the four houses
    for k, x in enumerate((230, 670)):
        col = [(180, 50, 60), (60, 90, 170)][k]
        toon(c, Poly([(x - 24, 40), (x + 24, 40), (x + 24, 170), (x, 190), (x - 24, 170)]), col, w=2)
        flat(c, Poly(star_pts(x, 100, 14, 6)), (250, 210, 90))
    # wooden floor
    c.rect(0, 420, W, H, (150, 100, 70))
    for y in range(420, H, 24):
        flat(c, Thick(0, y, W, y, 1.4), (130, 86, 60))
    # bookshelf (left)
    toon(c, RRect(10, 250, 180, 470, 4), (110, 70, 50), w=2.2)
    for r in range(4):
        y = 270 + r * 50
        flat(c, RRect(20, y + 40, 170, y + 46, 0), (90, 56, 40))
        rnd = random.Random(2325 + r)
        x = 24
        while x < 160:
            w = rnd.choice((10, 12, 14))
            col = rnd.choice([(200, 60, 60), (60, 120, 200), (90, 170, 100), (220, 180, 80), (150, 90, 180)])
            if r == 1 and x < 70 and "books" in d:
                col = (250, 250, 246)
            flat(c, RRect(x, y + 2, x + w - 2, y + 40, 1), col)
            x += w
    # cauldron (centre)
    cauldron = (60, 60, 70)
    toon(c, [Ell(450, 470, 90, 60), RRect(370, 420, 530, 440, 8)], cauldron, w=2.4)
    brew = (120, 230, 120) if "brew" not in d else (230, 120, 220)
    flat(c, Ell(450, 428, 74, 14), brew)
    for x in (390, 510):
        toon(c, RRect(x - 6, 520, x + 6, 560, 2), (60, 60, 70), w=1.6, shadow=None)
    # students (chibi with pointed hats)
    chibi(c, 250, 560, s=1.3, hair=(240, 200, 90), outfit=(40, 40, 70), face=1, hat=(40, 40, 70))
    chibi(c, 650, 560, s=1.3, hair=(120, 60, 40), outfit=(40, 40, 70), face=-1, hat=(40, 40, 70) if "hat" not in d else (200, 60, 70))
    # teacher at the board (right)
    chibi(c, 820, 470, s=1.4, hair=(230, 230, 236), outfit=(110, 60, 160), face=-1, hat=(110, 60, 160), weapon="staff")
    # owl on a perch (left top)
    toon(c, Thick(30, 220, 110, 220, 5), (110, 70, 50), w=1.4, shadow=None)
    toon(c, [Ell(70, 196, 20, 24), Poly([(54, 176), (58, 164), (64, 176)]), Poly([(76, 176), (82, 164), (86, 176)])], (150, 120, 90), w=1.6)
    flat(c, [Circ(62, 190, 6), Circ(78, 190, 6)], (250, 220, 90))
    flat(c, [Circ(62, 190, 2.6), Circ(78, 190, 2.6)], (40, 30, 40))
    # quest panel (bottom right)
    panel(c, 700, 520, 890, 592, (250, 240, 210), r=10, w=1.8)
    glyph_line(c, 716, 860, 540, (120, 90, 70), 2329, w=1.8, size=9)
    glyph_line(c, 716, 820, 562, (120, 90, 70), 2330, w=1.8, size=9)
    quest = (90, 190, 110) if "quest" not in d else (240, 160, 60)
    toon(c, Circ(866, 572, 12), quest, w=1.4, shadow=None)


L232_ELEMENTS = [
    E("book1", lambda c, m: [toon(c, Poly([(330, 300), (370, 290), (370, 320), (330, 330)]), (200, 60, 60), w=1.4), toon(c, Poly([(370, 290), (410, 300), (410, 330), (370, 320)]),
                                                                                                                 (250, 246, 230), w=1.4, shadow=None)],
      pivot=(370, 310), anim=dict(bobAmplitude=(0, 12), bobSpeed=0.4)),
    E("book2", lambda c, m: [toon(c, Poly([(520, 290), (556, 282), (556, 308), (520, 316)]), (60, 120, 200), w=1.4), toon(c, Poly([(556, 282), (592, 290), (592, 316), (556, 308)]),
                                                                                                                  (250, 246, 230), w=1.4, shadow=None)],
      pivot=(556, 300), anim=dict(bobAmplitude=(0, 10), bobSpeed=0.5, phase=0.5)),
    E("bubble1", lambda c, m: toon(c, Circ(430, 410, 10), (160, 250, 160), w=1.2, shadow=None), pivot=(430, 410),
      anim=dict(driftVelocity=(0, -40), driftLength=80, driftFade=True)),
    E("bubble2", lambda c, m: toon(c, Circ(476, 410, 8), (160, 250, 160), w=1.2, shadow=None), pivot=(476, 410),
      anim=dict(driftVelocity=(0, -40), driftLength=80, driftFade=True, phase=0.5)),
    E("sparkle", lambda c, m: [flat(c, Poly(star_pts(x, y, 9, 2, points=4, rot=0)), (255, 250, 200)) for x, y in ((800, 350), (840, 330), (360, 260))],
      daynight="untinted", anim=dict(twinkle=1, twinkleSpeed=0.8)),
]

L232_DIFFS = [
    ("moon", 792, 120, 0),
    ("rune", 560, 180, 0),
    ("books", 46, 341, 0),
    ("brew", 450, 428, 0),
    ("hat", 650, 450, 0),
    ("quest", 866, 572, 0),
]


# =================================================================== Level 233 pirate sailing map
def ship(c, x, y, s, sail, hull=(150, 100, 60), ang=0.0, flag=(40, 40, 50)):
    """Top-down sailing ship."""
    ca, sa = math.cos(ang), math.sin(ang)

    def p(dx, dy):
        return (x + (dx * ca - dy * sa) * s, y + (dx * sa + dy * ca) * s)
    toon(c, Poly([p(-34, -12), p(20, -14), p(40, 0), p(20, 14), p(-34, 12)]), hull, w=1.8)
    flat(c, Poly([p(-28, -8), p(18, -10), p(32, 0), p(18, 10), p(-28, 8)]), lit(hull, 1.2))
    for dx in (-14, 10):
        toon(c, Poly([p(dx - 4, -22), p(dx + 4, -22), p(dx + 6, 22), p(dx - 6, 22)]), sail, w=1.4, shadow=None)
    flat(c, Poly([p(34, -2), p(46, -6), p(46, 2)]), flag)


def island(c, x, y, rx, ry, seed, palms=2):
    toon(c, Ell(x, y, rx + 14, ry + 10), (240, 220, 160), w=2, shadow=(0, 3, 6, 0.2))
    toon(c, Ell(x, y - 4, rx, ry), (110, 180, 90), w=1.6, shadow=None)
    rnd = random.Random(seed)
    for _ in range(palms):
        px, py = x + rnd.uniform(-rx * 0.5, rx * 0.5), y + rnd.uniform(-ry * 0.5, ry * 0.3)
        flat(c, [Ell(px + 8 * math.cos(a), py + 8 * math.sin(a), 9, 4) for a in (0, 1.25, 2.5, 3.8, 5.0)], (60, 140, 70))
        flat(c, Circ(px, py, 3), (150, 100, 60))


def l233_bg(c, d):
    c.rect(0, 0, W, H, (70, 150, 210))
    rnd = random.Random(2331)
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        flat(c, [Thick(x, y, x + 8, y - 4, 1.6), Thick(x + 8, y - 4, x + 16, y, 1.6)], (120, 190, 236))
    # shallows
    soft_union(c, [Ell(220, 230, 170, 110), Ell(680, 420, 170, 110)], (120, 200, 230), 0.6, spread=30)
    # islands
    island(c, 220, 230, 120, 70, 2332, palms=4)
    island(c, 680, 420, 110, 70, 2333, palms=3)
    island(c, 760, 110, 60, 34, 2334, palms=1)
    island(c, 120, 500, 50, 30, 2335, palms=1)
    # port town on the big island
    for k, (x, y) in enumerate(((180, 210), (220, 196), (260, 214), (210, 244))):
        roof = [(220, 90, 70), (240, 160, 60), (200, 80, 90), (220, 90, 70)][k]
        if k in (0, 1) and "town" in d:
            roof = (70, 120, 210)
        toon(c, RRect(x - 14, y - 10, x + 14, y + 12, 2), (240, 230, 210), w=1.4, shadow=None)
        toon(c, Poly([(x - 18, y - 8), (x + 18, y - 8), (x, y - 24)]), roof, w=1.4, shadow=None)
    toon(c, RRect(276, 270, 330, 280, 2), (150, 100, 60), w=1.4, shadow=None)
    # treasure X + dotted route
    for k in range(10):
        t = k / 10
        x, y = 330 + (620 - 330) * t, 290 + (400 - 290) * t - 60 * math.sin(t * math.pi)
        flat(c, Circ(x, y, 3), (250, 250, 240))
    xm = (220, 50, 50) if "mark" not in d else (40, 40, 50)
    flat(c, [Thick(650, 390, 680, 420, 6), Thick(680, 390, 650, 420, 6)], xm)
    # lighthouse on the small island
    toon(c, [RRect(752, 70, 768, 112, 2), Poly([(748, 72), (772, 72), (760, 58)])], (250, 250, 246), w=1.4, shadow=None)
    flat(c, [RRect(752, 84, 768, 92, 0), RRect(752, 100, 768, 108, 0)], (220, 60, 60))
    # whirlpool
    for k in range(4):
        c.ellipse_ring(470, 130, 50 - k * 11, 30 - k * 7, 2.4, (200, 236, 250))
    # sea monster tentacles (cute)
    tent = (190, 90, 170) if "monster" not in d else (90, 190, 140)
    for k, (x, y) in enumerate(((300, 520), (340, 540), (380, 520))):
        toon(c, Poly([(x - 10, y + 10), (x + 10, y + 10), (x + 6, y - 30), (x - 2, y - 46), (x - 8, y - 30)]), tent, w=1.8)
        flat(c, [Circ(x, y - 10 + j * 10, 2.4) for j in range(2)], lit(tent, 1.3))
    # ships
    ship(c, 380, 330, 1.4, (250, 250, 246), flag=(40, 40, 50), ang=0.3)
    ship(c, 560, 160, 1.2, (240, 200, 160) if "sail" not in d else (220, 80, 80), hull=(120, 80, 50), flag=(60, 110, 200), ang=-0.5)
    ship(c, 820, 540, 1.1, (250, 250, 246), hull=(160, 110, 70), flag=(60, 110, 200), ang=3.4)
    # compass rose (top left)
    toon(c, Circ(70, 70, 50), (250, 240, 210), w=2)
    flat(c, Poly(star_pts(70, 70, 44, 10, points=4, rot=-90)), (200, 80, 70))
    flat(c, Poly(star_pts(70, 70, 30, 8, points=4, rot=-45)), (90, 80, 70))
    # gold HUD + mini scroll (bottom)
    panel(c, 260, 556, 640, 594, (250, 240, 210), r=10, w=1.8)
    toon(c, Circ(286, 575, 12), (250, 200, 60), w=1.4, shadow=None)
    digits(c, 306, 566, "2750", (120, 90, 60), 4)
    glyph_line(c, 400, 620, 576, (120, 90, 60), 2336, w=1.8, size=9)
    # barrel floating
    if "barrel" not in d:
        toon(c, Ell(80, 410, 18, 13), (170, 120, 70), w=1.6)
        flat(c, [Thick(70, 399, 70, 421, 2), Thick(90, 399, 90, 421, 2)], (110, 80, 50))


L233_ELEMENTS = [
    E("swirl", lambda c, m: c.ellipse_ring(470, 130, 20, 12, 3, (240, 250, 255)), pivot=(470, 130), anim=dict(rotateSpeed=90)),
    E("gull", lambda c, m: flat(c, [Thick(300, 100, 310, 106, 2), Thick(310, 106, 320, 100, 2)], (250, 250, 250)), pivot=(310, 104),
      anim=dict(orbitRadius=(60, 30), orbitSpeed=0.12)),
    E("wake", lambda c, m: [flat(c, Thick(330 - k * 16, 316 - k * 5, 336 - k * 16, 314 - k * 5, 2), (230, 246, 255)) for k in range(3)], daynight="untinted",
      anim=dict(twinkle=0.8, twinkleSpeed=1.2)),
    E("needle", lambda c, m: flat(c, Thick(70, 70, 70, 34, 3), (60, 60, 70)), pivot=(70, 70), anim=dict(swingAngle=12, swingSpeed=0.4)),
]

L233_DIFFS = [
    ("town", 220, 190, 0),
    ("mark", 665, 405, 0),
    ("monster", 340, 512, 0),
    ("sail", 560, 160, 0),
    ("barrel", 80, 410, 0),
]


# =================================================================== Level 234 dinosaur-park builder (isometric)
def dino(c, x, base, s, col, kind="long", face=1):
    if kind == "long":     # long-neck
        toon(c, [Ell(x, base - 24 * s, 34 * s, 18 * s), Poly([(x + 20 * s * face, base - 30 * s), (x + 44 * s * face, base - 86 * s), (x + 56 * s * face, base - 84 * s),
                                                              (x + 32 * s * face, base - 20 * s)]),
                 Ell(x + 54 * s * face, base - 88 * s, 11 * s, 7 * s), Poly([(x - 28 * s * face, base - 26 * s), (x - 64 * s * face, base - 14 * s), (x - 30 * s * face, base - 16 * s)])],
             col, w=1.8)
        for lx in (-20, -8, 10, 22):
            toon(c, RRect(x + lx * s - 4 * s, base - 14 * s, x + lx * s + 4 * s, base, 2), col, w=1.4, shadow=None)
        flat(c, Circ(x + 58 * s * face, base - 90 * s, 1.8 * s), (40, 30, 40))
    elif kind == "horn":   # three-horn
        for lx in (-16, -6, 12, 22):
            toon(c, RRect(x + lx * s - 4 * s, base - 12 * s, x + lx * s + 4 * s, base, 2), col, w=1.4, shadow=None)
        toon(c, [Ell(x, base - 22 * s, 30 * s, 16 * s), Ell(x + 30 * s * face, base - 28 * s, 14 * s, 12 * s)], col, w=1.8)
        toon(c, Ell(x + 22 * s * face, base - 36 * s, 10 * s, 20 * s), lit(col, 1.15), w=1.4, shadow=None)
        flat(c, [Poly([(x + 36 * s * face, base - 34 * s), (x + 58 * s * face, base - 46 * s), (x + 40 * s * face, base - 28 * s)])], (250, 246, 230))
        flat(c, Circ(x + 34 * s * face, base - 30 * s, 1.8 * s), (40, 30, 40))
    else:                  # big two-legged (friendly)
        toon(c, [Ell(x, base - 40 * s, 26 * s, 22 * s), Ell(x + 22 * s * face, base - 66 * s, 18 * s, 13 * s),
                 Poly([(x - 20 * s * face, base - 44 * s), (x - 60 * s * face, base - 30 * s), (x - 22 * s * face, base - 30 * s)])], col, w=1.8)
        toon(c, [RRect(x - 10 * s, base - 24 * s, x - 2 * s, base, 2), RRect(x + 6 * s, base - 24 * s, x + 14 * s, base, 2)], col, w=1.4, shadow=None)
        flat(c, Circ(x + 28 * s * face, base - 70 * s, 2 * s), (40, 30, 40))
        flat(c, Thick(x + 24 * s * face, base - 60 * s, x + 38 * s * face, base - 60 * s, 1.6), (40, 30, 40))


def l234_bg(c, d):
    c.rect(0, 0, W, H, (120, 190, 100))
    rnd = random.Random(2341)
    for _ in range(80):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        flat(c, Thick(x, y, x + 4, y - 6, 1.6), (106, 176, 90))
    # paths (isometric bands)
    path = (230, 210, 170)
    flat(c, Poly([(0, 330), (450, 590), (520, 560), (70, 300)]), path)
    flat(c, Poly([(430, 120), (900, 390), (900, 450), (380, 150)]), path)
    flat(c, Poly([(380, 150), (430, 120), (0, -130), (0, -60)]), path)
    # paddock 1 (left) - fence diamond with long-neck
    def fence_dia(cx, cy, rx, ry, col):
        pts = [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            n = int(math.hypot(x1 - x0, y1 - y0) / 22)
            for k in range(n + 1):
                px, py = x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n
                flat(c, RRect(px - 2, py - 16, px + 2, py, 1), col)
            flat(c, [Thick(x0, y0 - 12, x1, y1 - 12, 2), Thick(x0, y0 - 6, x1, y1 - 6, 2)], col)
    flat(c, Poly([(230, 70), (420, 170), (230, 270), (40, 170)]), (100, 170, 80))
    toon(c, Ell(300, 200, 50, 20), (90, 160, 220), w=1.4, shadow=None)
    fence_dia(230, 170, 190, 100, (170, 120, 70))
    for x, y in ((120, 150), (330, 130)):
        if x == 120 and "tree" in d:
            continue
        toon(c, [Circ(x, y - 30, 26), Circ(x - 16, y - 16, 16), Circ(x + 16, y - 16, 16)], (60, 140, 70), w=1.6)
        flat(c, RRect(x - 4, y - 14, x + 4, y + 4, 1), (130, 90, 60))
    dino(c, 220, 230, 1.1, (120, 170, 210) if "longneck" not in d else (230, 160, 90), kind="long")
    # paddock 2 (right) - three-horns
    flat(c, Poly([(690, 190), (880, 290), (690, 390), (500, 290)]), (170, 160, 90))
    fence_dia(690, 290, 190, 100, (120, 120, 130))
    for x, y in ((600, 270), (720, 230)):
        toon(c, [Ell(x, y, 24, 12), Ell(x + 6, y - 8, 16, 10)], (150, 146, 156), w=1.4, shadow=None)
    dino(c, 680, 330, 1.2, (230, 150, 90), kind="horn")
    dino(c, 790, 300, 1.0, (200, 120, 80) if "horn" not in d else (160, 110, 210), kind="horn", face=-1)
    # gift shop (bottom right) - iso box
    shop = (240, 120, 120)
    toon(c, Poly([(700, 470), (800, 520), (800, 580), (700, 530)]), (240, 230, 210), w=1.8, shadow=None)
    toon(c, Poly([(800, 520), (880, 480), (880, 540), (800, 580)]), (220, 210, 190), w=1.8, shadow=None)
    toon(c, Poly([(690, 468), (790, 410), (890, 478), (800, 524)]), shop, w=1.8, shadow=None)
    flat(c, Poly([(730, 500), (760, 515), (760, 548), (730, 533)]), (120, 80, 60))
    sign = (250, 200, 60) if "shop" not in d else (110, 200, 120)
    toon(c, Poly([(820, 516), (866, 494), (866, 524), (820, 546)]), sign, w=1.4, shadow=None)
    # visitors on paths
    for k, (x, y) in enumerate(((140, 380), (300, 470), (560, 220), (760, 380), (420, 540))):
        chibi(c, x, y, s=0.5, hair=[(40, 30, 30), (240, 200, 90), (120, 60, 40), (230, 120, 160), (40, 30, 30)][k],
              outfit=[(240, 90, 90), (90, 150, 230), (250, 200, 60), (90, 190, 110), (180, 110, 220)][k])
    # big friendly dino statue / attraction centre
    dino(c, 470, 400, 1.3, (110, 180, 110) if "rex" not in d else (220, 120, 170), kind="rex")
    # build menu (bottom left)
    panel(c, 10, 500, 330, 592, (250, 246, 236), r=10, w=1.8)
    for k in range(4):
        col = [(170, 120, 70), (90, 160, 220), (240, 120, 120), (110, 180, 110)][k]
        if k == 2 and "menu" in d:
            col = (250, 200, 60)
        toon(c, RRect(24 + k * 76, 512, 90 + k * 76, 578, 8), col, w=1.4, shadow=None)
        flat(c, RRect(36 + k * 76, 530, 78 + k * 76, 560, 4), lit(col, 1.3))
    # money / rating bar (top right)
    panel(c, 600, 10, 890, 50, (250, 246, 236), r=10, w=1.6)
    toon(c, Circ(626, 30, 12), (250, 200, 60), w=1.4, shadow=None)
    digits(c, 646, 20, "48200", (120, 90, 60), 4)
    for k in range(5):
        flat(c, Poly(star_pts(770 + k * 24, 30, 10, 4)), (250, 200, 60) if k < 4 else (200, 200, 210))


L234_ELEMENTS = [

    E("balloon", lambda c, m: [flat(c, Thick(300, 450, 304, 410, 1), (90, 90, 100)), toon(c, Ell(304, 400, 12, 15), (240, 80, 90), w=1.4, shadow=None)],
      pivot=(300, 450), anim=dict(swingAngle=8, swingSpeed=0.6)),
    E("bird", lambda c, m: flat(c, [Thick(560, 90, 570, 96, 2), Thick(570, 96, 580, 90, 2)], (60, 60, 80)), pivot=(570, 94), anim=drift_across(550, 590, 22)),
    E("splash", lambda c, m: c.ellipse_ring(300, 200, 20, 8, 2, (220, 240, 255)), pivot=(300, 200), daynight="untinted", anim=dict(pulse=0.4, scaleSpeed=0.8)),
]

L234_DIFFS = [
    ("longneck", 270, 160, 0),
    ("tree", 120, 130, 0),
    ("horn", 790, 280, 0),
    ("rex", 470, 350, 0),
    ("shop", 843, 520, 0),
    ("menu", 209, 545, 0),
]


LEVELS = [
    ("Level225", "果冻堆叠", l225_bg, L225_ELEMENTS, L225_DIFFS, 60, OPTS),
    ("Level226", "打砖块", l226_bg, L226_ELEMENTS, L226_DIFFS, 60, OPTS),
    ("Level227", "清版动作", l227_bg, L227_ELEMENTS, L227_DIFFS, 60, OPTS),
    ("Level228", "贪吃蛇", l228_bg, L228_ELEMENTS, L228_DIFFS, 60, OPTS),
    ("Level229", "打地鼠", l229_bg, L229_ELEMENTS, L229_DIFFS, 60, OPTS),
    ("Level230", "星际星图", l230_bg, L230_ELEMENTS, L230_DIFFS, 60, OPTS),
    ("Level231", "挖矿沙盒", l231_bg, L231_ELEMENTS, L231_DIFFS, 60, OPTS),
    ("Level232", "魔法学院", l232_bg, L232_ELEMENTS, L232_DIFFS, 60, OPTS),
    ("Level233", "海盗航海", l233_bg, L233_ELEMENTS, L233_DIFFS, 60, OPTS),
    ("Level234", "恐龙乐园", l234_bg, L234_ELEMENTS, L234_DIFFS, 60, OPTS),
]
