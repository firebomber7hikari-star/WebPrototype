# -*- coding: utf-8 -*-
"""Gothic pack: medieval castles, werewolves and vampires (paper-craft side views, eerie but not gory):
  Level124 月下古堡 - the vampire's castle on a crag under a full moon, a black carriage on the winding road; moonlight <-> fog
  Level125 狼人之夜 - a village at the forest edge: villagers with torches and pitchforks, the werewolf howling on a rock; fog
  Level126 伯爵大厅 - inside the count's great hall: coffin, candelabra, ancestor portraits, a stained-glass rose window
  Level127 城堡庭院 - a medieval castle courtyard: blacksmith, knights, the well, banners on the walls; rain showers
  Level128 午夜墓园 - a gothic chapel and graveyard: the vampire rising from his coffin, bats, a lantern-bearing gravedigger; thunder
"""
import math
import random

from fdcore import CLEAR, E, FOG, H, OVERCAST, RAIN, THUNDER, W, W_, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, hill_strip, hill_y, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, barrel, crate, dead_tree, drift_across, gy, layer, sky, smoke_el, tree_pine
from fills import birds, cloud_bank, far_forest, far_ridge, puffs
from stylekit import figure, flame, star_field
from weather import cloud, fog_layer, flash, lightning, puddles, rain_layer, splash_rings

SKIN = (246, 214, 186)
PALE = (226, 228, 238)
NIGHT_EDGE = (120, 110, 140)          # dark scenes: cut edges in a muted tone instead of glowing white
STONE_N = (96, 92, 112)
STONE_N_D = (78, 74, 94)


def opts(**kw):
    o = dict(post=paper_post, anim_seconds=24.0, frames=72)
    o.update(kw)
    return o


# =================================================================== shared gothic kit
def dpiece(c, shapes, col, border=1.5, shadow=PROP):
    """Paper piece for night scenes: cut edge in a muted tone."""
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


def gothic_arch(x, y_top, w, y_bottom):
    """Pointed-arch opening (lancet): rectangle with a pointed top."""
    spring = y_top + w * 0.55
    return [RRect(x - w / 2, spring, x + w / 2, y_bottom, 0), Poly([(x - w / 2, spring + 1), (x + w / 2, spring + 1), (x, y_top)])]


def moon(c, x, y, r, col=(252, 246, 222)):
    soft_union(c, [Circ(x, y, r)], (255, 248, 220), 0.35, spread=r * 0.9)
    piece(c, Circ(x, y, r), col, shadow=None)
    for dx, dy, rr in ((-0.3, -0.2, 0.18), (0.25, 0.15, 0.14), (-0.05, 0.4, 0.1)):
        flat(c, Circ(x + dx * r, y + dy * r, rr * r), lit(col, 0.93))


def bat_shapes(x, y, s=1.0):
    return [Poly([(x, y), (x - 12 * s, y - 6 * s), (x - 8 * s, y), (x - 14 * s, y + 2 * s)]),
            Poly([(x, y), (x + 12 * s, y - 6 * s), (x + 8 * s, y), (x + 14 * s, y + 2 * s)]), Ell(x, y, 3 * s, 4 * s)]


def bat_el(eid, x, y, s=1.0, r=(26, 12), speed=0.25, phase=0.0, col=(30, 24, 40), **kw):
    return E(eid, lambda c, m: piece(c, bat_shapes(x, y, s), col, shadow=None), pivot=(x, y),
             anim=dict(orbitRadius=r, orbitSpeed=speed, stretch=(0, 0.5), scaleSpeed=3, phase=phase), daynight="untinted", **kw)


def crow(c, x, y, col=(26, 24, 32), s=1.0):
    piece(c, [Ell(x, y, 9 * s, 6 * s), Circ(x + 8 * s, y - 6 * s, 4.5 * s), Poly([(x - 6 * s, y - 2 * s), (x - 18 * s, y + 4 * s), (x - 6 * s, y + 4 * s)])],
          col, shadow=SMALL)
    flat(c, Poly([(x + 12 * s, y - 7 * s), (x + 18 * s, y - 5 * s), (x + 12 * s, y - 4 * s)]), (210, 170, 70))
    flat(c, [Thick(x - 1 * s, y + 5 * s, x - 2 * s, y + 10 * s, 1.2 * s), Thick(x + 3 * s, y + 5 * s, x + 3 * s, y + 10 * s, 1.2 * s)], (60, 50, 50))


def vampire(c, x, base, h=1.0, cape=(28, 22, 36), lining=(170, 30, 46), vest=(110, 20, 34), skin=PALE, hair=(24, 20, 28), eyes=(220, 40, 50),
            arms_up=False, flip=False):
    """The count: high-collared cape (red lining), slicked hair with a widow's peak. Original design."""
    k = -1 if flip else 1
    # cape behind the body
    spread = 40 * h if arms_up else 24 * h
    dpiece(c, Poly([(x - spread, base - (60 if arms_up else 4) * h), (x - 12 * h, base - 74 * h), (x + 12 * h, base - 74 * h),
                    (x + spread, base - (60 if arms_up else 4) * h), (x + 16 * h, base), (x - 16 * h, base)]), cape)
    flat(c, Poly([(x - spread * 0.8, base - (58 if arms_up else 8) * h), (x - 10 * h, base - 70 * h), (x + 10 * h, base - 70 * h),
                  (x + spread * 0.8, base - (58 if arms_up else 8) * h), (x + 12 * h, base - 4 * h), (x - 12 * h, base - 4 * h)]), lining)
    # suit
    dpiece(c, [Poly([(x - 12 * h, base), (x + 12 * h, base), (x + 10 * h, base - 70 * h), (x - 10 * h, base - 70 * h)])], (34, 30, 40), shadow=SMALL)
    flat(c, Poly([(x - 6 * h, base - 70 * h), (x + 6 * h, base - 70 * h), (x + 5 * h, base - 36 * h), (x - 5 * h, base - 36 * h)]), vest)
    flat(c, Poly([(x - 4 * h, base - 70 * h), (x + 4 * h, base - 70 * h), (x, base - 58 * h)]), (245, 244, 248))
    flat(c, Circ(x, base - 54 * h, 2.4 * h), (230, 190, 70))
    # high collar
    dpiece(c, [Poly([(x - 18 * h, base - 96 * h), (x - 8 * h, base - 72 * h), (x - 2 * h, base - 74 * h)]),
               Poly([(x + 18 * h, base - 96 * h), (x + 8 * h, base - 72 * h), (x + 2 * h, base - 74 * h)])], cape, shadow=None)
    # head
    hx, hy = x + 1 * h * k, base - 84 * h
    flat(c, Ell(hx, hy, 9 * h, 11 * h), skin)
    flat(c, [Poly([(hx - 10 * h, hy - 2 * h), (hx - 9 * h, hy - 11 * h), (hx, hy - 14 * h), (hx + 9 * h, hy - 11 * h), (hx + 10 * h, hy - 2 * h),
                   (hx + 4 * h, hy - 8 * h), (hx, hy - 4 * h), (hx - 4 * h, hy - 8 * h)])], hair)
    flat(c, [Circ(hx - 3.5 * h + 1 * h * k, hy, 1.5 * h), Circ(hx + 3.5 * h + 1 * h * k, hy, 1.5 * h)], eyes)
    flat(c, Thick(hx - 3 * h, hy + 6 * h, hx + 3 * h, hy + 6 * h, 1.2 * h), (120, 40, 50))
    flat(c, [Poly([(hx - 2.4 * h, hy + 6 * h), (hx - 1.4 * h, hy + 6 * h), (hx - 1.9 * h, hy + 8.4 * h)]),
             Poly([(hx + 1.4 * h, hy + 6 * h), (hx + 2.4 * h, hy + 6 * h), (hx + 1.9 * h, hy + 8.4 * h)])], (250, 250, 250))
    if arms_up:
        flat(c, [Circ(x - spread, base - 62 * h, 4 * h), Circ(x + spread, base - 62 * h, 4 * h)], skin)
    return hx, hy


def werewolf(c, x, base, h=1.0, fur=(92, 82, 96), belly=(150, 136, 140), eyes=(255, 214, 60), howl=False, flip=False):
    """Hunched wolf-man on two legs with ragged trousers. Original design."""
    k = -1 if flip else 1
    dark = lit(fur, 0.8)
    # legs (digitigrade) + feet
    dpiece(c, [Poly([(x - 14 * h, base - 34 * h), (x - 2 * h, base - 34 * h), (x - 8 * h, base - 14 * h), (x - 2 * h, base), (x - 16 * h, base),
                     (x - 18 * h, base - 16 * h)]),
               Poly([(x + 2 * h, base - 34 * h), (x + 16 * h, base - 34 * h), (x + 18 * h, base - 16 * h), (x + 20 * h, base), (x + 6 * h, base),
                     (x + 8 * h, base - 14 * h)])], dark)
    flat(c, [Poly([(x - 16 * h, base - 34 * h), (x + 18 * h, base - 34 * h), (x + 14 * h, base - 24 * h), (x + 8 * h, base - 28 * h), (x + 2 * h, base - 22 * h),
                   (x - 4 * h, base - 28 * h), (x - 12 * h, base - 22 * h)])], (80, 70, 110))
    # torso, hunched forward
    lean = 10 * h * k
    dpiece(c, [Poly([(x - 16 * h, base - 32 * h), (x + 16 * h, base - 32 * h), (x + 22 * h + lean, base - 74 * h), (x - 20 * h + lean, base - 80 * h)])], fur)
    flat(c, Poly([(x - 6 * h, base - 36 * h), (x + 8 * h, base - 36 * h), (x + 10 * h + lean, base - 66 * h), (x - 6 * h + lean, base - 68 * h)]), belly)
    # arms with claws
    for sx in (-1, 1):
        ax = x + sx * 20 * h + lean
        dpiece(c, [Thick(ax, base - 72 * h, ax + sx * 8 * h, base - 44 * h, 8 * h)], fur, shadow=SMALL)
        for f in (-3, 0, 3):
            flat(c, Poly([(ax + sx * 8 * h + f * h, base - 42 * h), (ax + sx * 8 * h + f * h + 1.2 * h, base - 42 * h),
                          (ax + sx * 9 * h + f * h, base - 34 * h)]), (240, 236, 220))
    # head: muzzle points forward, or up when howling
    hx, hy = x + 4 * h * k + lean, base - 88 * h
    if howl:
        muzzle = Poly([(hx - 6 * h, hy - 4 * h), (hx + 6 * h * k, hy - 26 * h), (hx + 12 * h * k, hy - 22 * h), (hx + 10 * h * k, hy + 2 * h)])
        ear = Poly([(hx - 10 * h * k, hy - 2 * h), (hx - 16 * h * k, hy - 14 * h), (hx - 4 * h * k, hy - 8 * h)])
    else:
        muzzle = Poly([(hx + 4 * h * k, hy - 6 * h), (hx + 24 * h * k, hy - 2 * h), (hx + 24 * h * k, hy + 4 * h), (hx + 4 * h * k, hy + 8 * h)])
        ear = Poly([(hx - 6 * h * k, hy - 8 * h), (hx - 4 * h * k, hy - 22 * h), (hx + 4 * h * k, hy - 10 * h)])
    dpiece(c, [Circ(hx, hy, 12 * h), muzzle, ear], fur, shadow=SMALL)
    flat(c, Circ(hx + 4 * h * k, hy - 3 * h, 2 * h), eyes)
    nose = (hx + 11 * h * k, hy - 24 * h) if howl else (hx + 24 * h * k, hy)
    flat(c, Circ(nose[0], nose[1], 2.2 * h), (30, 26, 32))
    # mane tufts
    flat(c, [Poly([(hx - 12 * h * k, hy + 4 * h), (hx - 22 * h * k, hy + 12 * h), (hx - 10 * h * k, hy + 14 * h)]),
             Poly([(hx - 8 * h * k, hy + 10 * h), (hx - 16 * h * k, hy + 22 * h), (hx - 2 * h * k, hy + 16 * h)])], dark)
    return hx, hy


def villager(c, x, base, body, h=1.2, hat=None, tool=None, tool_col=(140, 100, 70)):
    """figure() plus a pitchfork or a torch held up (the torch flame itself is an animated element)."""
    hx, hy = figure(c, x, base, body, h=h, hat=hat, border=1.5, shadow=PROP)
    if tool == "fork":
        top = base - 78 * h
        flat(c, Thick(x + 10 * h, base - 6 * h, x + 10 * h, top, 2.2 * h), tool_col)
        flat(c, [Thick(x + 4 * h, top, x + 16 * h, top, 1.8 * h)] + [Thick(x + dx * h, top, x + dx * h, top - 12 * h, 1.6 * h) for dx in (4, 10, 16)],
             (150, 150, 160))
    elif tool == "torch":
        flat(c, Thick(x + 10 * h, base - 20 * h, x + 14 * h, base - 66 * h, 2.6 * h), tool_col)
        flat(c, Ell(x + 14 * h, base - 66 * h, 3.4 * h, 2.4 * h), (90, 60, 40))
    flat(c, Circ(x + 9 * h, base - 24 * h, 3 * h), SKIN)
    return hx, hy


def torch_tip(x, base, h=1.2):
    return x + 14 * h, base - 68 * h


def iron_fence(c, x0, x1, base, h=46, col=(36, 32, 44), step=16):
    flat(c, [Thick(x0, base - h * 0.85, x1, base - h * 0.85, 2.4), Thick(x0, base - h * 0.25, x1, base - h * 0.25, 2.4)], col)
    x = x0
    while x <= x1:
        flat(c, [Thick(x, base, x, base - h, 2.4), Poly([(x - 3.5, base - h), (x + 3.5, base - h), (x, base - h - 9)])], col)
        x += step


def tombstone(c, x, base, s=1.0, col=(120, 118, 132), kind="round", cross=None):
    if kind == "round":
        shapes = [RRect(x - 15 * s, base - 38 * s, x + 15 * s, base, 3), Circ(x, base - 38 * s, 15 * s)]
    elif kind == "cross":
        shapes = [RRect(x - 4 * s, base - 62 * s, x + 4 * s, base, 1), RRect(x - 16 * s, base - 50 * s, x + 16 * s, base - 42 * s, 1)]
    else:
        shapes = [Poly([(x - 16 * s, base), (x + 16 * s, base), (x + 13 * s, base - 40 * s), (x, base - 50 * s), (x - 13 * s, base - 40 * s)])]
    dpiece(c, shapes, col)
    if kind != "cross":
        flat(c, [Thick(x - 7 * s, base - 30 * s, x + 7 * s, base - 30 * s, 1.6 * s), Thick(x - 7 * s, base - 22 * s, x + 7 * s, base - 22 * s, 1.6 * s)],
             lit(col, 0.8))
    if cross:
        flat(c, [Thick(x, base - 44 * s, x, base - 20 * s, 2.4 * s), Thick(x - 6 * s, base - 36 * s, x + 6 * s, base - 36 * s, 2.4 * s)], cross)


def coffin_shape(x, base, w, hgt):
    """Six-sided coffin standing upright (narrow foot, wide shoulders)."""
    return Poly([(x - w * 0.32, base), (x + w * 0.32, base), (x + w * 0.5, base - hgt * 0.72), (x + w * 0.36, base - hgt), (x - w * 0.36, base - hgt),
                 (x - w * 0.5, base - hgt * 0.72)])


def candelabra(c, x, base, h=1.0, arms=3, col=(196, 160, 80)):
    dpiece(c, [RRect(x - 10 * h, base - 6 * h, x + 10 * h, base, 2), Thick(x, base, x, base - 60 * h, 3 * h)], col, shadow=SMALL)
    tips = [(x, base - 60 * h)]
    if arms >= 3:
        flat(c, [Thick(x - 22 * h, base - 46 * h, x + 22 * h, base - 46 * h, 2.4 * h), Thick(x - 22 * h, base - 46 * h, x - 22 * h, base - 56 * h, 2.4 * h),
                 Thick(x + 22 * h, base - 46 * h, x + 22 * h, base - 56 * h, 2.4 * h)], col)
        tips += [(x - 22 * h, base - 56 * h), (x + 22 * h, base - 56 * h)]
    for tx, ty in tips:
        flat(c, RRect(tx - 3 * h, ty - 14 * h, tx + 3 * h, ty, 1), (246, 240, 226))
    return [(tx, ty - 14 * h) for tx, ty in tips]


def candle_flames(prefix, tips, s=0.7):
    out = []
    for i, (x, y) in enumerate(tips):
        out += flame("%s%d" % (prefix, i), x, y, s, glow_night=False)
    return out


# =================================================================== Level 124 moonlit castle (vampire's castle, moon <-> fog)
STEPS124 = [(CLEAR, 14), (FOG, 10)]
SKY124 = ((26, 26, 62), (86, 64, 112))
MILL124_Y = gy(470, [(14, 0.012, 0.4), (6, 0.03, 1.4)], 210) + 6 - 66
OWL124_Y = gy(470, [(14, 0.012, 0.4), (6, 0.03, 1.4)], 330) + 10 - 1.2 * 80 - 12


def keep_tower(c, x, base, w, h, roof, col=STONE_N, cone=1.6, wins=2, lit_win=(255, 206, 110)):
    dpiece(c, RRect(x - w / 2, base - h, x + w / 2, base, 1), col)
    for y in range(int(base - h) + 14, int(base), 14):
        flat(c, Thick(x - w / 2, y, x + w / 2, y, 1), lit(col, 0.86))
    dpiece(c, Poly([(x - w / 2 - 6, base - h + 2), (x + w / 2 + 6, base - h + 2), (x, base - h - w * cone)]), roof)
    for i in range(wins):
        wy = base - h + 22 + i * 36
        if wy + 20 < base:
            flat(c, gothic_arch(x, wy, 9, wy + 20), lit_win)


def l124_bg(c, d):
    sky(c, *SKY124, y1=420)
    moon(c, 160, 118, 58)
    cloud_bank(c, 250, (70, 60, 98), 1241, 0.9, shadow=None)
    far_ridge(c, 360, 120, (58, 52, 86), 1242, step=70)
    far_forest(c, 420, 40, (44, 46, 70), 1243, spacing=22)
    # the crag
    dpiece(c, Poly([(420, 610), (450, 360), (500, 300), (560, 280), (700, 286), (780, 330), (830, 610)]), (62, 56, 78), shadow=LAYER)
    flat(c, [Thick(520, 330, 470, 430, 3), Thick(700, 320, 760, 420, 3), Thick(600, 300, 640, 360, 2)], (50, 44, 64))
    # curtain wall + keep + towers
    dpiece(c, RRect(500, 210, 760, 296, 1), STONE_N)
    for x in range(500, 760, 20):
        dpiece(c, RRect(x, 198, x + 10, 212, 1), STONE_N, shadow=SMALL)
    keep_tower(c, 630, 296, 96, 190, (56, 40, 70), wins=3)
    keep_tower(c, 512, 296, 46, 140, (56, 40, 70))
    keep_tower(c, 752, 296, 48, 156, (56, 40, 70))
    keep_tower(c, 690, 210, 24, 50, (56, 40, 70), wins=1, cone=1.8)
    keep_tower(c, 570, 210, 26, 44, (56, 40, 70), wins=1, cone=1.8)
    # great window of the keep (lit gold / blood red)
    win = (230, 60, 70) if "window" in d else (255, 206, 110)
    soft_union(c, gothic_arch(630, 186, 26, 236), win, 0.45, spread=12)
    flat(c, gothic_arch(630, 186, 26, 236), win)
    flat(c, [Thick(630, 194, 630, 236, 2), Thick(617, 214, 643, 214, 2)], (60, 40, 60))
    # gate: portcullis down (A) / open dark gap (B)
    flat(c, gothic_arch(630, 250, 34, 296), (24, 18, 30))
    for xx in range(616, 646, 7):
        flat(c, Thick(xx, 258, xx, 296, 2), (110, 96, 90))
    for yy in range(266, 296, 9):
        flat(c, Thick(614, yy, 646, yy, 2), (110, 96, 90))
    # banner pole on the left tower (banner itself animated)
    flat(c, Thick(512, 84, 512, 40, 2.4), (40, 34, 44))
    # winding road + bridge
    road = (120, 104, 120)
    dpiece(c, Poly([(612, 296), (648, 296), (700, 360), (640, 420), (560, 470), (420, 520), (300, 610), (170, 610), (330, 500), (520, 430),
                    (600, 380), (630, 340)]), road, shadow=SMALL)
    # left hill with a dead wood
    layer(c, 470, [(14, 0.012, 0.4), (6, 0.03, 1.4)], (52, 50, 70))
    for x, s in ((40, 1.4), (120, 1.0), (330, 1.2)):
        dead_tree(c, x, gy(470, [(14, 0.012, 0.4), (6, 0.03, 1.4)], x) + 10, s, col=(34, 30, 42))
    # ruined windmill on the hill (its sails are gone in B)
    mx, mb = 210, gy(470, [(14, 0.012, 0.4), (6, 0.03, 1.4)], 210) + 6
    dpiece(c, [Poly([(mx - 18, mb), (mx + 18, mb), (mx + 12, mb - 70), (mx - 12, mb - 70)]),
               Poly([(mx - 16, mb - 68), (mx + 16, mb - 68), (mx, mb - 88)])], (70, 62, 80), shadow=SMALL)
    flat(c, gothic_arch(mx, mb - 30, 10, mb), (30, 26, 36))
    if "mill" not in d:
        hub = (mx, mb - 66)
        for a in (20, 110, 200, 290):
            ex, ey = hub[0] + 48 * math.cos(math.radians(a)), hub[1] + 48 * math.sin(math.radians(a))
            px, py = -math.sin(math.radians(a)) * 7, math.cos(math.radians(a)) * 7
            dpiece(c, [Thick(hub[0], hub[1], ex, ey, 2.4),
                       Poly([(hub[0] + (ex - hub[0]) * 0.3 + px, hub[1] + (ey - hub[1]) * 0.3 + py), (ex + px, ey + py), (ex, ey),
                             (hub[0] + (ex - hub[0]) * 0.3, hub[1] + (ey - hub[1]) * 0.3)])], (104, 90, 96), shadow=SMALL)
        flat(c, Circ(hub[0], hub[1], 4), (40, 34, 44))
    # owl on top of the right dead tree (missing in B)
    if "owl" not in d:
        ox, oy = 330, OWL124_Y
        dpiece(c, [Ell(ox, oy, 11, 14), Poly([(ox - 10, oy - 8), (ox - 9, oy - 22), (ox - 2, oy - 12)]),
                   Poly([(ox + 10, oy - 8), (ox + 9, oy - 22), (ox + 2, oy - 12)])], (120, 96, 80), shadow=SMALL)
        flat(c, [Circ(ox - 5, oy - 6, 4.6), Circ(ox + 5, oy - 6, 4.6)], (255, 214, 70))
        flat(c, [Circ(ox - 5, oy - 6, 1.8), Circ(ox + 5, oy - 6, 1.8)], (30, 24, 30))
        flat(c, Poly([(ox - 2, oy - 1), (ox + 2, oy - 1), (ox, oy + 3)]), (210, 160, 70))
    # right foreground: howling wolf on a rock (missing in B)
    dpiece(c, Poly([(780, 610), (800, 520), (860, 500), (920, 520), (920, 610)]), (70, 64, 86), shadow=LAYER)
    if "wolf" not in d:
        wx, wb = 850, 504
        dpiece(c, [Ell(wx, wb - 14, 22, 11), Thick(wx - 16, wb - 10, wx - 18, wb, 4), Thick(wx + 14, wb - 10, wx + 16, wb, 4),
                   Poly([(wx + 14, wb - 22), (wx + 26, wb - 46), (wx + 32, wb - 42), (wx + 26, wb - 16)]),
                   Poly([(wx - 20, wb - 16), (wx - 38, wb - 4), (wx - 22, wb - 8)])], (54, 50, 66), shadow=SMALL)
        flat(c, Poly([(wx + 20, wb - 34), (wx + 18, wb - 46), (wx + 24, wb - 38)]), (54, 50, 66))
    # graves + iron fence along the bottom
    for x, kind in ((520, "round"), (600, "cross"), (690, "gothic")):
        if x == 600 and "grave" in d:
            continue
        tombstone(c, x, 596, 0.9, kind=kind)
    iron_fence(c, 440, 780, 604, h=40)
    # the black carriage on the road
    cx, cb = 300, 560
    dpiece(c, [RRect(cx - 50, cb - 66, cx + 40, cb - 22, 8), Poly([(cx - 46, cb - 66), (cx + 36, cb - 66), (cx + 26, cb - 78), (cx - 36, cb - 78)])],
           (32, 28, 40))
    flat(c, RRect(cx - 18, cb - 60, cx + 10, cb - 40, 2), (255, 206, 110))
    wheel = (120, 100, 70)
    for wx_ in (cx - 34, cx + 26):
        c.ellipse_ring(wx_, cb - 16, 16, 16, 4, wheel)
        flat(c, [Thick(wx_ - 13, cb - 16, wx_ + 13, cb - 16, 1.6), Thick(wx_, cb - 29, wx_, cb - 3, 1.6)], wheel)
    if "lamp" not in d:
        flat(c, Thick(cx + 40, cb - 54, cx + 52, cb - 54, 2), (40, 34, 44))
        dpiece(c, RRect(cx + 48, cb - 70, cx + 60, cb - 52, 2), (255, 206, 110), shadow=None)
    # horses
    for i, hx in enumerate((cx + 96, cx + 130)):
        hb = cb + 4 - i * 6
        dpiece(c, [Ell(hx, hb - 34, 22, 12), Thick(hx - 14, hb - 26, hx - 16, hb, 3.4), Thick(hx + 14, hb - 26, hx + 16, hb, 3.4),
                   Poly([(hx + 14, hb - 40), (hx + 30, hb - 56), (hx + 36, hb - 50), (hx + 22, hb - 34)])], (26, 22, 32), shadow=SMALL)
        flat(c, Poly([(hx + 18, hb - 46), (hx + 10, hb - 60), (hx + 14, hb - 44)]), (60, 30, 50))
    flat(c, Thick(cx + 40, cb - 34, cx + 80, cb - 36, 2), (60, 50, 50))
    # coachman with a top hat
    dpiece(c, [RRect(cx + 26, cb - 100, cx + 42, cb - 76, 3), Circ(cx + 34, cb - 106, 6)], (40, 36, 50), shadow=SMALL)
    flat(c, [RRect(cx + 28, cb - 124, cx + 40, cb - 110, 1), RRect(cx + 24, cb - 112, cx + 44, cb - 108, 1)], (24, 20, 28))
    # foreground grass
    for x in range(0, 440, 18):
        flat(c, Poly([(x, 612), (x + 6, 588 - (x * 7) % 14), (x + 12, 612)]), (40, 44, 58))


def l124_banner(c, m):
    col = (60, 120, 90) if m else (150, 30, 46)
    dpiece(c, Poly([(513, 42), (552, 50), (542, 58), (554, 66), (513, 72)]), col, shadow=SMALL)
    flat(c, Circ(528, 57, 4), (230, 200, 120))


L124_ELEMENTS = [
    star_field("stars", 124, 70, 240, avoid=((90, 50, 230, 190),), mask=0),
    cloud("cloud_moon", 160, 140, 0.55, (90, 80, 120), 0, anim=drift_across(120, 200, 6)),
    E("banner", l124_banner, variant=True, pivot=(513, 57), anim=dict(stretch=(0.2, 0), scaleSpeed=1.4, swingAngle=4, swingSpeed=0.9)),
] + [
    bat_el("bat%d" % i, x, y, 0.9, phase=i * 0.33, speed=0.22 * (1 if i % 2 else -1))
    for i, (x, y) in enumerate(((470, 150), (800, 170), (560, 110)))
] + [
    fog_layer("fog1", 1244, 330, 450, 0.45, 9, 1, col=(150, 146, 176)),
    fog_layer("fog2", 1245, 470, 560, 0.4, 12, -1, col=(150, 146, 176)),
]

L124_DIFFS = [
    ("banner", 532, 57, 0),
    ("mill", 210, MILL124_Y, 0),
    ("window", 630, 214, 0),
    ("lamp", 354, 500, 0),
    ("owl", 330, OWL124_Y - 6, 0),
    ("grave", 600, 570, 0),
    ("wolf", 856, 476, 0),
]

# =================================================================== Level 125 werewolf night (village at the forest edge, fog)
STEPS125 = [(CLEAR, 12), (FOG, 10)]
HILL125 = [(10, 0.011, 0.6), (6, 0.027, 2.1)]
WOLF125 = (612, 264)          # werewolf on the crag: (x, base)
WOLF125_H = 1.45


def cottage(c, x, base, w, h, wall=(150, 136, 120), roof=(70, 50, 56), lit_win=True, win_col=(255, 200, 100), chimney_x=None):
    """Half-timbered cottage for night scenes; returns the window rects."""
    x0, x1, top = x - w / 2, x + w / 2, base - h
    dpiece(c, RRect(x0, top, x1, base, 1), wall)
    beam = (74, 56, 52)
    flat(c, [Thick(x0 + 3, top, x0 + 3, base, 3), Thick(x1 - 3, top, x1 - 3, base, 3), Thick(x0, top + h * 0.5, x1, top + h * 0.5, 3),
             Thick(x0 + 3, top + 2, x, top + h * 0.5, 2.2), Thick(x1 - 3, top + 2, x, top + h * 0.5, 2.2)], beam)
    if chimney_x is not None:
        dpiece(c, RRect(chimney_x - 7, top - w * 0.42, chimney_x + 7, top - w * 0.12, 1), (90, 70, 70), shadow=SMALL)
    dpiece(c, Poly([(x0 - 10, top + 3), (x1 + 10, top + 3), (x, top - w * 0.5)]), roof)
    wins = [(x0 + w * 0.18, top + h * 0.6, x0 + w * 0.18 + 16, top + h * 0.6 + 16), (x1 - w * 0.18 - 16, top + h * 0.6, x1 - w * 0.18, top + h * 0.6 + 16)]
    for r in wins:
        flat(c, RRect(*r, 1.5), win_col if lit_win else (40, 34, 46))
        flat(c, [Thick((r[0] + r[2]) / 2, r[1], (r[0] + r[2]) / 2, r[3], 1.4), Thick(r[0], (r[1] + r[3]) / 2, r[2], (r[1] + r[3]) / 2, 1.4)], beam)
    flat(c, RRect(x - 8, base - 24, x + 8, base, 2), (60, 44, 40))
    return wins


def pumpkin(c, x, base, s=1.0, col=(226, 120, 40), face=False):
    dpiece(c, [Ell(x - 7 * s, base - 11 * s, 9 * s, 11 * s), Ell(x + 7 * s, base - 11 * s, 9 * s, 11 * s), Ell(x, base - 11 * s, 9 * s, 12 * s)], col,
           shadow=SMALL)
    flat(c, Thick(x, base - 22 * s, x + 3 * s, base - 28 * s, 2.4 * s), (70, 100, 50))
    if face:
        flat(c, [Poly([(x - 8 * s, base - 14 * s), (x - 3 * s, base - 14 * s), (x - 5.5 * s, base - 19 * s)]),
                 Poly([(x + 3 * s, base - 14 * s), (x + 8 * s, base - 14 * s), (x + 5.5 * s, base - 19 * s)]),
                 Poly([(x - 8 * s, base - 9 * s), (x + 8 * s, base - 9 * s), (x + 4 * s, base - 5 * s), (x - 4 * s, base - 5 * s)])], (255, 220, 110))


def l125_bg(c, d):
    sky(c, (20, 34, 58), (70, 92, 116), y1=420)
    moon(c, 612, 120, 74, col=(250, 246, 226))
    cloud_bank(c, 236, (64, 80, 108), 1251, 0.8, shadow=None)
    far_ridge(c, 330, 70, (52, 66, 92), 1252, step=60)
    far_forest(c, 380, 60, (38, 52, 72), 1253, spacing=20)
    # the crag with the werewolf howling at the moon (his trousers change colour)
    dpiece(c, Poly([(470, 420), (520, 300), (560, 270), (650, 262), (700, 290), (740, 420)]), (50, 56, 74), shadow=LAYER)
    for a, b in (((540, 300), (500, 380)), ((690, 296), (720, 380)), ((600, 320), (590, 400)), ((650, 330), (670, 410))):
        flat(c, Thick(a[0], a[1], b[0], b[1], 2.4), (42, 46, 62))
    werewolf(c, WOLF125[0], WOLF125[1], h=WOLF125_H, howl=True, flip=False)
    if "pants" in d:
        x, base = WOLF125
        k = WOLF125_H
        flat(c, [Poly([(x - 16 * k, base - 34 * k), (x + 18 * k, base - 34 * k), (x + 14 * k, base - 24 * k), (x + 8 * k, base - 28 * k),
                       (x + 2 * k, base - 22 * k), (x - 4 * k, base - 28 * k), (x - 12 * k, base - 22 * k)])], (60, 130, 90))
    # pine forest on both sides of the crag
    for x, b, hh in ((420, 430, 120), (760, 424, 130), (820, 432, 110), (880, 426, 140), (460, 436, 90)):
        tree_pine(c, x, b, hh, col=(34, 60, 64), trunk=(50, 40, 40))
    if "pine" not in d:
        tree_pine(c, 790, 400, 100, col=(40, 70, 70), trunk=(50, 40, 40))
    # village street
    layer(c, 440, HILL125, (60, 70, 74))
    w1 = cottage(c, 90, gy(440, HILL125, 90) + 14, 130, 90, chimney_x=120, roof=(86, 50, 54))
    w2 = cottage(c, 260, gy(440, HILL125, 260) + 14, 110, 80, roof=(60, 60, 84), lit_win="window" not in d)
    # weathervane rooster on the first roof (missing in B)
    rx, ry = 90, gy(440, HILL125, 90) + 14 - 90 - 65
    flat(c, Thick(rx, ry + 2, rx, ry - 26, 2), (40, 36, 46))
    if "vane" not in d:
        dpiece(c, [Poly([(rx - 14, ry - 26), (rx + 4, ry - 36), (rx + 8, ry - 46), (rx + 14, ry - 40), (rx + 12, ry - 28), (rx - 4, ry - 22)])],
               (40, 36, 46), shadow=None)
    flat(c, Thick(rx - 10, ry - 12, rx + 10, ry - 12, 1.6), (40, 36, 46))
    # lantern post (lantern missing in B) - its glow is drawn here, the flame is static
    lx, lb = 360, 520
    flat(c, [Thick(lx, lb, lx, lb - 110, 4), Thick(lx, lb - 104, lx + 24, lb - 104, 3)], (36, 32, 42))
    if "lantern" not in d:
        soft_union(c, [Circ(lx + 24, lb - 86, 12)], (255, 200, 110), 0.4, spread=22)
        dpiece(c, [RRect(lx + 16, lb - 98, lx + 32, lb - 76, 2), Poly([(lx + 14, lb - 98), (lx + 34, lb - 98), (lx + 24, lb - 106)])], (255, 210, 120),
               shadow=None)
    # ground of the square
    piece(c, hill_strip(500, [(6, 0.02, 0.4)]), (66, 64, 70), shadow=LAYER)
    for x in range(-20, 920, 40):
        flat(c, Ell(x + (x * 13) % 20, 540 + (x * 7) % 40, 14, 4), (58, 56, 62))
    # cart with hay (wheel missing in B)
    cx, cb = 790, 560
    dpiece(c, [RRect(cx - 60, cb - 46, cx + 50, cb - 26, 2), Thick(cx + 50, cb - 30, cx + 96, cb - 20, 3)], (110, 80, 60))
    dpiece(c, [Ell(cx - 30, cb - 52, 34, 16), Ell(cx + 16, cb - 54, 32, 18)], (200, 170, 90), shadow=SMALL)
    wheels = [cx - 34, cx + 24]
    for wx in wheels:
        c.ellipse_ring(wx, cb - 16, 17, 17, 4, (70, 54, 46))
        flat(c, [Thick(wx - 14, cb - 16, wx + 14, cb - 16, 1.6), Thick(wx, cb - 30, wx, cb - 2, 1.6)], (70, 54, 46))
    # pumpkins by the fence (middle one turns into a jack-o'-lantern in B)
    for i, x in enumerate((40, 76, 112)):
        if i == 1 and "pumpkin" in d:
            continue
        pumpkin(c, x, 596, 1.2)
    # picket fence + grass in the foreground
    for x in range(150, 330, 22):
        dpiece(c, Poly([(x, 610), (x, 560), (x + 7, 552), (x + 14, 560), (x + 14, 610)]), (120, 110, 104), shadow=SMALL)
    flat(c, [Thick(150, 572, 330, 572, 3), Thick(150, 596, 330, 596, 3)], (100, 92, 88))
    for x in range(0, 900, 16):
        flat(c, Poly([(x, 612), (x + 5, 594 - (x * 5) % 12), (x + 10, 612)]), (44, 56, 54))


def l125_villagers():
    """The mob: (x, base, body, tool) - tools are drawn into the background, flames are elements."""
    return [(420, 548, (120, 70, 60), "torch"), (470, 556, (70, 90, 120), "fork"), (520, 552, (110, 100, 60), "torch"),
            (570, 560, (90, 60, 100), "fork"), (630, 554, (80, 110, 80), "torch")]


def l125_mob(c, m):
    for i, (x, b, body, tool) in enumerate(l125_villagers()):
        t = tool
        if i == 3 and m:
            t = "torch"
        villager(c, x, b, body, h=1.25, hat=(60, 50, 50) if i % 2 else None, tool=t)


L125_TORCHES = [torch_tip(x, b, 1.25) for x, b, _, t in l125_villagers() if t == "torch"]

L125_ELEMENTS = [
    star_field("stars", 125, 60, 220, avoid=((520, 30, 700, 210),)),
    cloud("cloud_moon", 520, 170, 0.6, (70, 86, 114), 0, anim=drift_across(470, 560, 5)),
    E("mob", l125_mob, variant=True, pivot=(520, 556), anim=dict(bobAmplitude=(0, 2), bobSpeed=0.9)),
] + [f for i, (x, y) in enumerate(L125_TORCHES) for f in flame("torch%d" % i, x, y, 1.1)] \
  + flame("torch_b", *torch_tip(570, 560, 1.25), 1.1, show="B") + [
    bat_el("bat0", 300, 180, 0.8, speed=0.2), bat_el("bat1", 860, 150, 0.8, speed=-0.24, phase=0.4),
    fog_layer("fog1", 1254, 380, 470, 0.45, 9, 1, col=(150, 166, 186)),
    fog_layer("fog2", 1255, 500, 580, 0.35, 12, -1, col=(150, 166, 186)),
] + smoke_el("chimney", 120, gy(440, HILL125, 90) + 14 - 90 - 130 * 0.42 - 4, n=3, col=(120, 126, 140), r=7)

L125_DIFFS = [
    ("pants", WOLF125[0], int(WOLF125[1] - 30 * WOLF125_H), 0),
    ("pine", 790, 350, 0),
    ("window", 260, int(gy(440, HILL125, 260) + 14 - 80 * 0.4 + 8), 0),
    ("vane", 92, int(gy(440, HILL125, 90) + 14 - 90 - 65 - 32), 0),
    ("lantern", 384, 432, 0),
    ("pumpkin", 76, 582, 0),
    ("mob", 586, 470, 0),
]

# =================================================================== Level 126 the count's great hall (interior)
WALL126 = (74, 58, 80)
GOLD = (206, 168, 86)


def portrait(c, x, y, w, h, bg, coat, seed=0, skin=PALE):
    """Ancestor portrait in a gilded frame: a pale nobleman in a dark coat."""
    dpiece(c, RRect(x - 6, y - 6, x + w + 6, y + h + 6, 3), GOLD)
    flat(c, RRect(x, y, x + w, y + h, 1), bg)
    cx = x + w / 2
    flat(c, Poly([(cx - w * 0.42, y + h), (cx + w * 0.42, y + h), (cx + w * 0.34, y + h * 0.7), (cx + w * 0.16, y + h * 0.6),
                  (cx - w * 0.16, y + h * 0.6), (cx - w * 0.34, y + h * 0.7)]), coat)
    flat(c, Poly([(cx - 6, y + h * 0.6), (cx + 6, y + h * 0.6), (cx, y + h * 0.78)]), (240, 238, 244))
    flat(c, Ell(cx, y + h * 0.45, w * 0.17, h * 0.17), skin)
    flat(c, Poly([(cx - w * 0.19, y + h * 0.43), (cx - w * 0.17, y + h * 0.3), (cx, y + h * 0.26), (cx + w * 0.17, y + h * 0.3), (cx + w * 0.19, y + h * 0.43),
                  (cx, y + h * 0.36)]), (30, 24, 32))
    flat(c, [Circ(cx - w * 0.06, y + h * 0.46, 1.6), Circ(cx + w * 0.06, y + h * 0.46, 1.6)], (200, 40, 50))


def rose_window(c, x, y, r, centre=(220, 60, 70), petals=((70, 100, 200), (200, 170, 70)), seed=0):
    dpiece(c, Circ(x, y, r + 10), (96, 84, 104))
    flat(c, Circ(x, y, r), (36, 30, 46))
    n = 12
    for i in range(n):
        a0, a1 = math.radians(i * 360 / n + 3), math.radians((i + 1) * 360 / n - 3)
        pts = [(x + r * 0.34 * math.cos(a0), y + r * 0.34 * math.sin(a0))]
        pts += [(x + (r - 5) * math.cos(a0 + (a1 - a0) * t / 6), y + (r - 5) * math.sin(a0 + (a1 - a0) * t / 6)) for t in range(7)]
        pts += [(x + r * 0.34 * math.cos(a1), y + r * 0.34 * math.sin(a1))]
        flat(c, Poly(pts), petals[i % len(petals)])
    flat(c, Circ(x, y, r * 0.28), centre)
    flat(c, Poly(star_pts(x, y, r * 0.2, r * 0.09, points=6)), lit(centre, 1.35))


def armor(c, x, base, h=1.0, plume=(190, 40, 50), metal=(160, 166, 184)):
    dpiece(c, [RRect(x - 16 * h, base - 6 * h, x + 16 * h, base, 2)], (70, 60, 70), shadow=SMALL)
    dpiece(c, [Thick(x - 7 * h, base - 6 * h, x - 8 * h, base - 44 * h, 7 * h), Thick(x + 7 * h, base - 6 * h, x + 8 * h, base - 44 * h, 7 * h),
               RRect(x - 16 * h, base - 92 * h, x + 16 * h, base - 44 * h, 6), Thick(x - 18 * h, base - 86 * h, x - 22 * h, base - 50 * h, 6 * h),
               Thick(x + 18 * h, base - 86 * h, x + 22 * h, base - 50 * h, 6 * h), RRect(x - 11 * h, base - 116 * h, x + 11 * h, base - 92 * h, 5)],
           metal)
    flat(c, [Thick(x - 8 * h, base - 106 * h, x + 8 * h, base - 106 * h, 2 * h), Thick(x, base - 92 * h, x, base - 60 * h, 1.6 * h)], lit(metal, 0.7))
    dpiece(c, Poly([(x - 2 * h, base - 116 * h), (x + 4 * h, base - 140 * h), (x + 18 * h, base - 128 * h), (x + 6 * h, base - 114 * h)]), plume,
           shadow=SMALL)
    flat(c, Thick(x + 24 * h, base, x + 24 * h, base - 150 * h, 2.4 * h), (110, 90, 70))
    flat(c, Poly([(x + 20 * h, base - 150 * h), (x + 28 * h, base - 150 * h), (x + 24 * h, base - 166 * h)]), metal)


def l126_bg(c, d):
    c.rect(0, 0, W, 620, WALL126)
    # stone courses on the back wall
    for y in range(20, 420, 28):
        flat(c, Thick(0, y, W, y, 1.2), lit(WALL126, 0.86))
        off = 30 if (y // 28) % 2 else 0
        for x in range(off, W, 60):
            flat(c, Thick(x, y, x, y + 28, 1.2), lit(WALL126, 0.86))
    # pointed vault arches along the top
    for x in range(0, W + 1, 150):
        flat(c, [Thick(x, 0, x, 420, 10)], lit(WALL126, 0.8))
    # the rose window with moonlight and its curtains
    rose_window(c, 450, 160, 86, centre=(80, 170, 110) if "rose" in d else (220, 60, 70))
    for x0, x1, k in ((316, 362, 1), (538, 584, -1)):
        dpiece(c, Poly([(x0, 40), (x1, 40), (x1 + 10 * k, 320), (x0 - 4 * k, 330)]), (130, 26, 40))
        for xx in (x0 + 14, x0 + 30):
            flat(c, Thick(xx, 44, xx + 4 * k, 320, 2), (104, 20, 32))
    flat(c, Thick(300, 40, 600, 40, 5), GOLD)
    # ancestor portraits (left one wears green in B)
    portrait(c, 110, 120, 96, 120, (60, 40, 50), (40, 90, 60) if "portrait" in d else (110, 24, 40))
    portrait(c, 694, 120, 96, 120, (50, 46, 70), (40, 34, 50))
    # crossed swords under the right portrait
    for a, b in (((700, 300), (790, 270)), ((700, 270), (790, 300))):
        dpiece(c, [Thick(a[0], a[1], b[0], b[1], 3)], (200, 204, 216), shadow=SMALL)
    dpiece(c, Poly([(728, 262), (762, 262), (762, 292), (745, 310), (728, 292)]), (130, 26, 40), shadow=SMALL)
    # wall shelf with books and a skull (skull missing in B)
    flat(c, Thick(40, 340, 250, 340, 5), (90, 64, 50))
    x = 48
    for i, col in enumerate(((120, 40, 50), (60, 70, 110), (140, 110, 60), (50, 80, 60), (110, 50, 90), (130, 90, 60))):
        hgt = 26 + (i * 7) % 12
        dpiece(c, RRect(x, 340 - hgt, x + 12, 338, 2), col, shadow=SMALL, border=1)
        x += 14
    if "skull" not in d:
        sx = 190
        dpiece(c, [Circ(sx, 318, 14), RRect(sx - 9, 322, sx + 9, 338, 4)], (230, 224, 210), shadow=SMALL)
        flat(c, [Circ(sx - 5, 318, 3.6), Circ(sx + 5, 318, 3.6), Poly([(sx - 2, 328), (sx + 2, 328), (sx, 324)])], (40, 30, 40))
    dpiece(c, [Ell(232, 334, 10, 6), RRect(226, 314, 238, 334, 3)], (90, 120, 90), shadow=SMALL, border=1)
    # floor: checkered marble, red runner up to the dais
    piece(c, RRect(-10, 420, W + 10, 620, 0), (60, 52, 66), shadow=(0, -3, 8, 0.3))
    for i, y in enumerate(range(420, 620, 30)):
        for j, x in enumerate(range(-30, W + 30, 60)):
            if (i + j) % 2:
                flat(c, Poly([(x + (x - 450) * (y - 420) / 400, y), (x + 60 + (x + 60 - 450) * (y - 420) / 400, y),
                              (x + 60 + (x + 60 - 450) * (y + 30 - 420) / 400, y + 30), (x + (x - 450) * (y + 30 - 420) / 400, y + 30)]),
                     (84, 74, 92))
    flat(c, Poly([(410, 460), (490, 460), (560, 620), (340, 620)]), (140, 28, 42))
    flat(c, [Thick(414, 466, 344, 616, 3), Thick(486, 466, 556, 616, 3)], GOLD)
    # dais + the coffin (open in A, lid closed in B)
    dpiece(c, [RRect(340, 440, 560, 470, 3)], (90, 80, 100))
    cx, cb = 450, 446
    dpiece(c, coffin_shape(cx, cb, 92, 196), (70, 40, 44))
    if "coffin" in d:
        dpiece(c, coffin_shape(cx, cb - 4, 84, 186), (96, 56, 56), shadow=SMALL)
        flat(c, [Thick(cx, cb - 160, cx, cb - 60, 5), Thick(cx - 22, cb - 130, cx + 22, cb - 130, 5)], GOLD)
    else:
        flat(c, coffin_shape(cx, cb - 6, 76, 176), (170, 30, 46))
        for k in range(4):
            flat(c, Thick(cx - 26 + k * 4, cb - 160 + k * 30, cx + 26 - k * 4, cb - 150 + k * 30, 1.6), (140, 22, 38))
    # side table with a goblet and a candle stub
    dpiece(c, [RRect(150, 474, 290, 488, 2), RRect(160, 488, 172, 560, 2), RRect(268, 488, 280, 560, 2)], (100, 70, 56))
    dpiece(c, [Poly([(196, 446), (220, 446), (214, 462), (202, 462)]), Thick(208, 462, 208, 472, 2.4), RRect(198, 470, 218, 474, 1)], GOLD,
           shadow=SMALL, border=1)
    flat(c, Ell(208, 448, 10, 2.4), (150, 20, 40))
    dpiece(c, RRect(252, 450, 262, 474, 1), (240, 234, 220), shadow=SMALL, border=1)
    # suit of armour (plume colour differs)
    armor(c, 800, 590, 1.3, plume=(60, 120, 200) if "plume" in d else (190, 40, 50))
    # black cat in the foreground (missing in B)
    if "cat" not in d:
        kx, kb = 96, 600
        dpiece(c, [Ell(kx, kb - 18, 18, 18), Circ(kx + 4, kb - 46, 12), Poly([(kx - 6, kb - 54), (kx - 4, kb - 66), (kx + 2, kb - 56)]),
                   Poly([(kx + 8, kb - 56), (kx + 14, kb - 66), (kx + 14, kb - 52)]), Thick(kx - 14, kb - 6, kx - 34, kb - 20, 4)], (24, 20, 28), shadow=SMALL)
        flat(c, [Ell(kx, kb - 47, 2.4, 3), Ell(kx + 8, kb - 47, 2.4, 3)], (240, 210, 60))
    # cobwebs in the top corners
    for (x, y, sx, sy) in ((0, 0, 1, 1), (W, 0, -1, 1)):
        for r in (30, 52, 74):
            pts = [(x + sx * r * math.cos(math.radians(a)), y + sy * r * math.sin(math.radians(a))) for a in range(0, 91, 15)]
            flat(c, [Thick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1) for i in range(len(pts) - 1)], (180, 176, 190))
        for a in range(0, 91, 30):
            flat(c, Thick(x, y, x + sx * 80 * math.cos(math.radians(a)), y + sy * 80 * math.sin(math.radians(a)), 1), (180, 176, 190))


L126_CANDLE_L = (60, 610)
L126_CANDLE_R = (712, 610)


def l126_candelabra(c, m):
    candelabra(c, L126_CANDLE_L[0], L126_CANDLE_L[1], 1.6)
    candelabra(c, L126_CANDLE_R[0], L126_CANDLE_R[1], 1.6)


def l126_count(c, m):
    vampire(c, 624, 560, h=1.5, lining=(60, 90, 170) if m else (170, 30, 46))


def l126_chandelier(x):
    def d(c, m):
        flat(c, Thick(x, 0, x, 52, 2), (40, 34, 44))
        c.ellipse_ring(x, 60, 46, 9, 3.4, GOLD)
        for dx in (-36, -12, 12, 36):
            yy = 60 + 8 * math.sqrt(max(0, 1 - (dx / 46) ** 2))
            flat(c, RRect(x + dx - 2.4, yy - 12, x + dx + 2.4, yy, 1), (246, 240, 226))
            flat(c, Poly([(x + dx - 2.6, yy - 12), (x + dx + 2.6, yy - 12), (x + dx, yy - 21)]), (255, 180, 70))
    return d


def l126_moonbeam(c, m):
    soft_union(c, [Poly([(400, 220), (500, 220), (620, 520), (280, 520)])], (190, 200, 255), 0.12, spread=30)


def _candelabra_tips(x, base, h):
    return [(x, base - 60 * h - 14 * h), (x - 22 * h, base - 56 * h - 14 * h), (x + 22 * h, base - 56 * h - 14 * h)]


L126_ELEMENTS = [
    E("moonbeam", l126_moonbeam, daynight="untinted", anim=dict(twinkle=0.35, twinkleSpeed=0.25)),
    E("chandelierL", l126_chandelier(160), pivot=(160, 0), daynight="untinted", anim=dict(swingAngle=2.5, swingSpeed=0.18)),
    E("chandelierR", l126_chandelier(740), pivot=(740, 0), daynight="untinted", anim=dict(swingAngle=2.5, swingSpeed=0.18, phase=0.5)),
    E("candelabra", l126_candelabra),
    E("count", l126_count, variant=True, pivot=(624, 560), anim=dict(bobAmplitude=(0, 2), bobSpeed=0.25)),
] + candle_flames("flameL", _candelabra_tips(*L126_CANDLE_L, 1.6), 0.9) + candle_flames("flameR", _candelabra_tips(*L126_CANDLE_R, 1.6), 0.9) \
  + flame("stub", 257, 450, 0.7, glow_night=False) + [
    bat_el("bat0", 262, 62, 0.9, r=(40, 14), speed=0.18),
]

L126_DIFFS = [
    ("rose", 450, 160, 0),
    ("portrait", 158, 214, 0),
    ("skull", 190, 326, 0),
    ("coffin", 420, 330, 0),
    ("plume", 812, 420, 0),
    ("cat", 98, 560, 0),
    ("count", 624, 480, 0),
]

# =================================================================== Level 127 castle courtyard (day, rain showers)
STEPS127 = [(CLEAR, 12), (OVERCAST, 4), (RAIN, 10), (OVERCAST, 4)]
STONE = (186, 178, 170)
STONE_D = (160, 152, 146)


def knight(c, x, base, h=1.0, tabard=(200, 50, 50), shield=(240, 200, 60), metal=(178, 184, 200), flip=False, sword_up=False):
    k = -1 if flip else 1
    piece(c, [Thick(x - 6 * h, base - 30 * h, x - 8 * h, base, 6 * h), Thick(x + 6 * h, base - 30 * h, x + 8 * h, base, 6 * h)], metal, border=1.2,
          shadow=PROP)
    piece(c, Poly([(x - 14 * h, base - 26 * h), (x + 14 * h, base - 26 * h), (x + 11 * h, base - 66 * h), (x - 11 * h, base - 66 * h)]), tabard,
          border=1.5, shadow=PROP)
    flat(c, [Thick(x, base - 62 * h, x, base - 32 * h, 3 * h), Thick(x - 9 * h, base - 50 * h, x + 9 * h, base - 50 * h, 3 * h)], (250, 240, 200))
    piece(c, [RRect(x - 10 * h, base - 88 * h, x + 10 * h, base - 64 * h, 5)], metal, border=1.2, shadow=SMALL)
    flat(c, Thick(x - 6 * h + 2 * k, base - 78 * h, x + 6 * h + 2 * k, base - 78 * h, 2.2 * h), (50, 50, 60))
    if sword_up:
        piece(c, [Thick(x + 14 * h * k, base - 56 * h, x + 34 * h * k, base - 100 * h, 3 * h)], (220, 224, 236), border=1, shadow=SMALL)
    else:
        piece(c, [Thick(x + 14 * h * k, base - 46 * h, x + 44 * h * k, base - 60 * h, 3 * h)], (220, 224, 236), border=1, shadow=SMALL)
    piece(c, Poly([(x - 22 * h * k, base - 62 * h), (x - 4 * h * k, base - 62 * h), (x - 4 * h * k, base - 38 * h), (x - 13 * h * k, base - 28 * h),
                   (x - 22 * h * k, base - 38 * h)]), shield, border=1.5, shadow=SMALL)
    flat(c, Poly(star_pts(x - 13 * h * k, base - 48 * h, 6 * h, 2.6 * h)), lit(shield, 0.7))


def wall_tower(c, x, base, w, h, roof):
    from levels_medieval import stone_blocks
    piece(c, RRect(x - w / 2, base - h, x + w / 2, base, 1), lit(STONE, 0.98), border=2, shadow=PROP)
    stone_blocks(c, x - w / 2, base - h, x + w / 2, base, STONE_D)
    piece(c, Poly([(x - w / 2 - 8, base - h + 2), (x + w / 2 + 8, base - h + 2), (x, base - h - w * 1.1)]), roof, border=2, shadow=PROP)
    flat(c, gothic_arch(x, base - h + 30, 12, base - h + 56), (70, 60, 80))


def l127_bg(c, d):
    from levels_medieval import arch, crenels, stone_blocks
    sky(c, (150, 196, 232), (214, 230, 242), y1=360)
    puffs(c, [(120, 60, 0.7), (770, 46, 0.6)], col=(252, 252, 248))
    far_ridge(c, 250, 60, (160, 186, 206), 1271, step=80)
    # curtain wall with walkway, gatehouse and two towers
    piece(c, RRect(-10, 150, W + 10, 340, 0), STONE, border=2, shadow=LAYER)
    stone_blocks(c, -10, 150, W + 10, 340, STONE_D, h=16, w=30)
    crenels(c, -10, W + 10, 150, STONE, size=14)
    wall_tower(c, 90, 340, 100, 210, (90, 110, 170))
    wall_tower(c, 810, 340, 100, 210, (70, 140, 90) if "roof" in d else (190, 70, 60))
    # gatehouse with the portcullis raised
    piece(c, RRect(380, 110, 520, 340, 1), lit(STONE, 1.03), border=2, shadow=PROP)
    stone_blocks(c, 380, 110, 520, 340, STONE_D)
    crenels(c, 380, 520, 110, lit(STONE, 1.03), size=14)
    arch(c, 450, 236, 70, 340, (70, 58, 64))
    for x in range(420, 482, 10):
        flat(c, Thick(x, 240, x, 262, 2.4), (110, 100, 96))
    flat(c, RRect(434, 300, 466, 340, 0), (130, 180, 120))      # glimpse of the meadow outside
    # banner poles on the wall (banners are animated)
    for x in (230, 670):
        flat(c, Thick(x, 150, x, 104, 2.4), (100, 84, 70))
    # courtyard: cobbles
    piece(c, RRect(-10, 340, W + 10, 620, 0), (196, 186, 170), shadow=(0, -3, 8, 0.3))
    rnd = random.Random(127)
    for y in range(350, 620, 22):
        for x in range(-20 + (y // 22 % 2) * 18, W + 20, 36):
            flat(c, Ell(x + rnd.uniform(-3, 3), y, 15, 8), (186, 176, 160))
    # blacksmith's forge (left): lean-to roof, hearth, anvil
    piece(c, RRect(10, 250, 230, 440, 1), (226, 214, 190), border=2, shadow=PROP)
    piece(c, Poly([(0, 262), (240, 262), (240, 246), (120, 214), (0, 246)]), (150, 96, 70), border=2, shadow=PROP)
    piece(c, [RRect(28, 330, 110, 440, 3)], (150, 140, 136), border=1.5, shadow=SMALL)
    stone_blocks(c, 28, 330, 110, 440, (130, 120, 116), h=14, w=20)
    flat(c, [RRect(44, 380, 94, 440, 0), Circ(69, 380, 25)], (60, 40, 40))
    # tools + the smith's shield on the forge wall (shield colour differs)
    for i, x in enumerate((140, 166, 192)):
        flat(c, Thick(x, 286, x, 330, 2.4), (110, 90, 70))
        flat(c, RRect(x - 7, 280, x + 7, 290, 2), (90, 90, 100))
    sh = (60, 120, 200) if "shield" in d else (220, 180, 60)
    piece(c, Poly([(150, 350), (190, 350), (190, 378), (170, 396), (150, 378)]), sh, border=1.5, shadow=SMALL)
    flat(c, Poly(star_pts(170, 368, 9, 4)), lit(sh, 0.7))
    piece(c, [RRect(150, 478, 206, 490, 2), Poly([(206, 478), (226, 482), (206, 486)]), RRect(164, 490, 192, 518, 2)], (80, 80, 92), border=1.5,
          shadow=PROP)
    piece(c, [RRect(50, 190, 72, 236, 1)], (150, 96, 70), border=1.5, shadow=SMALL)
    # the well (bucket missing in B)
    wx, wb = 470, 470
    piece(c, [RRect(wx - 46, wb - 40, wx + 46, wb, 4)], (176, 168, 160), border=2, shadow=PROP)
    stone_blocks(c, wx - 46, wb - 40, wx + 46, wb, (150, 142, 136), h=13, w=22)
    for dx in (-36, 36):
        piece(c, Thick(wx + dx, wb - 40, wx + dx, wb - 104, 4), (130, 90, 64), shadow=SMALL)
    piece(c, Poly([(wx - 56, wb - 98), (wx + 56, wb - 98), (wx, wb - 132)]), (160, 90, 64), border=2, shadow=PROP)
    flat(c, Thick(wx - 36, wb - 84, wx + 36, wb - 84, 3), (100, 76, 56))
    if "bucket" not in d:
        flat(c, Thick(wx + 6, wb - 84, wx + 6, wb - 60, 1.4), (90, 80, 70))
        piece(c, Poly([(wx - 6, wb - 60), (wx + 18, wb - 60), (wx + 15, wb - 42), (wx - 3, wb - 42)]), (150, 104, 70), border=1.2, shadow=SMALL)
    # stable (right) with a horse looking out
    piece(c, RRect(640, 300, 890, 470, 1), (200, 160, 110), border=2, shadow=PROP)
    for x in range(650, 890, 16):
        flat(c, Thick(x, 300, x, 470, 1.4), (176, 136, 92))
    piece(c, Poly([(630, 312), (900, 312), (900, 292), (765, 262), (630, 292)]), (150, 96, 70), border=2, shadow=PROP)
    flat(c, RRect(690, 350, 760, 470, 2), (90, 66, 50))
    horse = (250, 246, 236) if "horse" in d else (120, 80, 56)
    piece(c, [Ell(724, 384, 22, 14), Poly([(706, 376), (690, 410), (704, 416), (716, 392)]), Poly([(730, 372), (736, 356), (742, 372)])], horse,
          border=1.5, shadow=SMALL)
    flat(c, Thick(728, 372, 712, 410, 3), lit(horse, 0.7))
    flat(c, Circ(714, 382, 2), INK)
    flat(c, RRect(684, 404, 766, 414, 2), (110, 80, 60))
    # hay + barrels + crates by the stable (one barrel missing in B)
    piece(c, [Ell(810, 470, 46, 26), Ell(780, 478, 30, 18)], (232, 200, 110), border=1.5, shadow=PROP)
    bx = [560, 600, 580]
    for i, x in enumerate(bx):
        barrel(c, x, 520 if i < 2 else 480, 1.0)
    crate(c, 860, 560, 1.2)
    crate(c, 830, 590, 1.0)
    # chickens pecking (one missing in B)
    for x, b in ((300, 560), (340, 580)):
        if x == 340 and "chicken" in d:
            continue
        piece(c, [Ell(x, b - 10, 12, 9), Circ(x + 10, b - 20, 6), Poly([(x - 10, b - 14), (x - 18, b - 24), (x - 14, b - 8)])], (250, 246, 236),
              border=1, shadow=SMALL)
        flat(c, [Poly([(x + 8, b - 26), (x + 11, b - 30), (x + 14, b - 26)]), Poly([(x + 16, b - 20), (x + 21, b - 19), (x + 16, b - 17)])],
             (220, 50, 50))
    # page boy carrying firewood, maid with a basket
    figure(c, 230, 560, (90, 120, 170), h=1.3)
    figure(c, 400, 590, (170, 90, 110), h=1.35, hat=(240, 236, 226))
    piece(c, Ell(418, 548, 12, 8), (190, 140, 80), border=1, shadow=SMALL)
    # foreground grass tufts
    for x in range(0, 900, 22):
        if 260 < x < 640:
            continue
        flat(c, Poly([(x, 612), (x + 7, 596 - (x * 3) % 10), (x + 14, 612)]), (110, 150, 90))


def l127_banner(x, col_a, col_b=None, key=None):
    def d(c, m):
        col = col_b if (m and col_b) else col_a
        piece(c, Poly([(x - 18, 104), (x + 18, 104), (x + 18, 166), (x, 152), (x - 18, 166)]), col, border=1.5, shadow=SMALL)
        flat(c, Poly(star_pts(x, 128, 9, 4)), (250, 220, 90))
    return d


def l127_smith(c, m):
    figure(c, 112, 530, (110, 80, 60), h=1.45)
    piece(c, RRect(102, 482, 128, 512, 3), (150, 110, 70), shadow=None)     # leather apron


def l127_hammer(c, m):
    piece(c, [Thick(126, 496, 160, 470, 3.4), RRect(154, 458, 172, 474, 2)], (90, 90, 100), border=1, shadow=SMALL)


L127_ELEMENTS = [
    E("bannerL", l127_banner(230, (200, 50, 50), (60, 120, 200)), variant=True, pivot=(230, 104), anim=dict(swingAngle=3, swingSpeed=0.5)),
    E("bannerR", l127_banner(670, (200, 50, 50)), pivot=(670, 104), anim=dict(swingAngle=3, swingSpeed=0.5, phase=0.4)),
    E("smith", l127_smith),
    E("hammer", l127_hammer, pivot=(126, 496), anim=dict(swingAngle=22, swingSpeed=1.1)),
    E("knightA", lambda c, m: knight(c, 520, 584, 1.25, tabard=(200, 50, 50), shield=(240, 200, 60), sword_up=True), pivot=(520, 584),
      anim=dict(bobAmplitude=(0, 3), bobSpeed=0.8)),
    E("knightB", lambda c, m: knight(c, 640, 588, 1.25, tabard=(60, 90, 170), shield=(90, 170, 90) if m else (240, 240, 240), flip=True),
      variant=True, pivot=(640, 588), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.8, phase=0.5)),
] + flame("forge", 69, 434, 1.6) + smoke_el("forge_smoke", 61, 186, n=3, col=(220, 220, 226), r=9) + [
    cloud("cloud_r%d" % i, x, y, k, (170, 176, 190), W_(OVERCAST, RAIN)) for i, (x, y, k) in enumerate(((150, 40, 1.3), (450, 30, 1.5), (760, 40, 1.3)))
] + [
    puddles("puddles", [Ell(330, 470, 40, 9), Ell(600, 410, 34, 8), Ell(760, 590, 30, 7)]),
    rain_layer("rain", 127, 80, 26, 1.3, 0.7, 260, mask=W_(RAIN)),
] + splash_rings("splash", [(330, 470, 8), (600, 410, 7), (760, 590, 7)], mask=W_(RAIN))

L127_DIFFS = [
    ("bannerL", 230, 134, 0),
    ("roof", 810, 80, 0),
    ("shield", 170, 370, 0),
    ("bucket", 476, 400, 0),
    ("horse", 720, 386, 0),
    ("chicken", 342, 566, 0),
    ("knightB", 618, 540, 0),
]

# =================================================================== Level 128 midnight graveyard (thunder)
STEPS128 = [(OVERCAST, 8), (THUNDER, 10), (FOG, 6)]
HILL128 = [(8, 0.012, 0.3), (5, 0.03, 1.2)]


def l128_bg(c, d):
    sky(c, (24, 30, 46), (70, 70, 96), y1=430)
    moon(c, 760, 96, 44, col=(236, 238, 214))
    cloud_bank(c, 200, (56, 58, 80), 1281, 1.0, shadow=None)
    far_ridge(c, 330, 80, (44, 48, 66), 1282, step=70)
    far_forest(c, 380, 46, (34, 40, 54), 1283, spacing=20)
    # the chapel: nave + bell tower with a spire
    nave = (104, 98, 114)
    dpiece(c, RRect(150, 230, 380, 430, 1), nave)
    dpiece(c, Poly([(140, 234), (390, 234), (265, 160)]), (60, 52, 70))
    for x in (190, 250, 310):
        flat(c, gothic_arch(x, 270, 22, 330), (36, 30, 44))
    win = (90, 180, 120) if "window" in d else (200, 60, 80)
    for x in (190, 310):
        flat(c, gothic_arch(x, 274, 16, 326), (230, 190, 90))
    flat(c, gothic_arch(250, 274, 16, 326), win)
    flat(c, [Thick(250, 282, 250, 326, 1.6), Thick(242, 300, 258, 300, 1.6)], (36, 30, 44))
    flat(c, gothic_arch(265, 370, 34, 430), (30, 24, 36))
    tx = 80
    dpiece(c, RRect(tx - 34, 150, tx + 34, 430, 1), lit(nave, 1.05))
    flat(c, gothic_arch(tx, 180, 30, 240), (30, 24, 36))
    if "bell" not in d:
        dpiece(c, [Poly([(tx - 13, 230), (tx + 13, 230), (tx + 9, 204), (tx, 198), (tx - 9, 204)]), Circ(tx, 232, 4)], (200, 170, 80), shadow=None)
    dpiece(c, Poly([(tx - 42, 154), (tx + 42, 154), (tx, 40)]), (60, 52, 70))
    flat(c, [Thick(tx, 40, tx, 18, 2.4), Thick(tx - 8, 28, tx + 8, 28, 2.4)], (60, 52, 70))
    # ground with the graves
    layer(c, 430, HILL128, (52, 60, 62))
    graves = [(440, "round", 1.0), (500, "gothic", 0.9), (180, "cross", 1.1), (330, "round", 0.9), (40, "gothic", 1.0)]
    for x, kind, sc in graves:
        if x == 330 and "tomb" in d:
            continue
        b = gy(430, HILL128, x) + 22
        tombstone(c, x, b, sc, kind=kind, cross=(76, 74, 86) if x == 330 else None)
    # mausoleum on the right (door ajar in A, shut in B)
    mx, mb = 820, gy(430, HILL128, 820) + 30
    dpiece(c, [RRect(mx - 70, mb - 120, mx + 70, mb, 1), Poly([(mx - 82, mb - 118), (mx + 82, mb - 118), (mx, mb - 168)])], (112, 108, 124))
    for x in (mx - 52, mx + 52):
        dpiece(c, RRect(x - 7, mb - 116, x + 7, mb, 1), (136, 132, 146), shadow=SMALL)
    flat(c, RRect(mx - 26, mb - 86, mx + 26, mb, 1), (24, 20, 30))
    if "door" in d:
        flat(c, RRect(mx - 26, mb - 86, mx + 26, mb, 1), (88, 84, 100))
        flat(c, [Thick(mx, mb - 86, mx, mb, 1.6), Circ(mx - 6, mb - 44, 2.4), Circ(mx + 6, mb - 44, 2.4)], (60, 56, 70))
    else:
        dpiece(c, Poly([(mx + 26, mb - 86), (mx + 40, mb - 80), (mx + 40, mb + 4), (mx + 26, mb)]), (88, 84, 100), shadow=SMALL)
    flat(c, Poly(star_pts(mx, mb - 136, 9, 4)), (200, 190, 150))
    # gnarled tree with a crow (missing in B)
    dead_tree(c, 680, gy(430, HILL128, 680) + 14, 1.5, col=(30, 28, 36))
    if "crow" not in d:
        crow(c, 650, gy(430, HILL128, 680) + 14 - 1.5 * 84 - 12, s=1.5)
    # the open grave + coffin with its lid off
    gx, gb = 560, 540
    dpiece(c, [Ell(gx, gb, 120, 26)], (40, 36, 40), shadow=SMALL)
    dpiece(c, Poly([(gx - 140, gb - 4), (gx - 110, gb - 40), (gx - 70, gb - 30), (gx - 60, gb + 6)]), (90, 74, 62), shadow=SMALL)   # earth mound
    dpiece(c, [Poly([(gx - 70, gb - 6), (gx + 80, gb - 10), (gx + 90, gb + 10), (gx - 60, gb + 14)])], (80, 44, 46), shadow=SMALL)
    flat(c, Poly([(gx - 60, gb - 4), (gx + 74, gb - 7), (gx + 80, gb + 6), (gx - 52, gb + 9)]), (170, 30, 46))
    dpiece(c, Poly([(gx + 96, gb - 20), (gx + 196, gb - 34), (gx + 202, gb - 22), (gx + 100, gb - 6)]), (90, 54, 56), shadow=SMALL)   # lid
    flat(c, [Thick(gx + 120, gb - 22, gx + 180, gb - 30, 3), Thick(gx + 140, gb - 34, gx + 146, gb - 14, 3)], (200, 170, 80))
    # shovel stuck in the mound
    flat(c, [Thick(gx - 100, gb - 34, gx - 120, gb - 110, 3)], (130, 96, 70))
    flat(c, Poly([(gx - 106, gb - 30), (gx - 92, gb - 36), (gx - 98, gb - 12)]), (150, 150, 160))
    # iron fence along the front with a gate
    iron_fence(c, -10, 330, 612, h=50)
    iron_fence(c, 420, 910, 612, h=50)
    for x in (330, 420):
        dpiece(c, RRect(x - 8, 548, x + 8, 612, 1), (90, 86, 100), shadow=SMALL)
        dpiece(c, Circ(x, 544, 9), (110, 106, 120), shadow=SMALL)
    # gravedigger by the fence, frightened (his lantern is missing in B)
    villager(c, 240, 566, (90, 80, 60), h=1.3, hat=(60, 50, 44))
    if "lantern" not in d:
        lx, ly = 262, 506
        soft_union(c, [Circ(lx, ly + 10, 10)], (255, 200, 110), 0.45, spread=22)
        flat(c, Thick(lx, ly - 8, lx, ly, 1.6), (40, 36, 46))
        dpiece(c, [RRect(lx - 8, ly, lx + 8, ly + 20, 2), Poly([(lx - 10, ly), (lx + 10, ly), (lx, ly - 8)])], (255, 210, 120), shadow=None)
    for x in range(0, 900, 18):
        flat(c, Poly([(x, 614), (x + 6, 600 - (x * 3) % 10), (x + 12, 614)]), (34, 44, 44))


def l128_vampire(c, m):
    vampire(c, 560, 532, h=1.35, arms_up=True, lining=(60, 140, 90) if m else (170, 30, 46))


L128_ELEMENTS = [
    E("vampire", l128_vampire, variant=True, pivot=(560, 532), anim=dict(bobAmplitude=(0, 3), bobSpeed=0.5, stretch=(0, 0.02), scaleSpeed=0.5)),
    lightning("bolt", 460, 20, 200, interval=4.0, phase=0.2, seed=128),
    lightning("bolt2", 860, 20, 170, interval=6.0, phase=0.65, seed=129),
    flash("flash", 4.0, 0.2, alpha=0.3),
    rain_layer("rain", 128, 70, 28, 1.3, 0.55, 300, mask=W_(THUNDER), col=(190, 196, 220)),
    fog_layer("fog1", 1284, 370, 430, 0.4, 9, 1, col=(140, 146, 166)),
    fog_layer("fog2", 1285, 580, 612, 0.35, 12, -1, col=(140, 146, 166)),
] + [
    bat_el("bat%d" % i, x, y, 0.9, phase=i * 0.3, speed=0.22 * (1 if i % 2 else -1)) for i, (x, y) in enumerate(((470, 300), (640, 240), (380, 150)))
]

L128_DIFFS = [
    ("window", 250, 300, 0),
    ("bell", 80, 216, 0),
    ("tomb", 330, int(gy(430, HILL128, 330) + 22 - 0.9 * 30), 0),
    ("door", 836, int(gy(430, HILL128, 820) + 30 - 43), 0),
    ("crow", 652, int(gy(430, HILL128, 680) + 14 - 1.5 * 84 - 16), 0),
    ("vampire", 560, 470, 0),
    ("lantern", 262, 518, 0),
]

LEVELS = [
    ("Level124", "月下古堡", l124_bg, L124_ELEMENTS, L124_DIFFS, 140,
     opts(weather=dict(steps=STEPS124, blend=3.0), anim_seconds=24.0)),
    ("Level125", "狼人之夜", l125_bg, L125_ELEMENTS, L125_DIFFS, 140,
     opts(weather=dict(steps=STEPS125, blend=3.0), anim_seconds=22.0)),
    ("Level126", "伯爵大厅", l126_bg, L126_ELEMENTS, L126_DIFFS, 140, opts(anim_seconds=12.0, frames=60)),
    ("Level127", "城堡庭院", l127_bg, L127_ELEMENTS, L127_DIFFS, 140,
     opts(weather=dict(steps=STEPS127, blend=3.0), anim_seconds=30.0, frames=80)),
    ("Level128", "午夜墓园", l128_bg, L128_ELEMENTS, L128_DIFFS, 140,
     opts(weather=dict(steps=STEPS128, blend=3.0), anim_seconds=24.0)),
]
