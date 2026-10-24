# -*- coding: utf-8 -*-
"""Hero & dragon fantasy (paper-craft, original characters only):
  Level170 勇者启程 - the starting village: notice board, weapon shop, elder sends the young hero off, dragon peak far away
  Level171 王城觐见 - the throne room: king and princess on the dais, guards, banners, the hero kneeling on the red carpet
  Level172 地下城   - a dungeon cross-section: torches, the hero's party, slimes, treasure chest, spike trap, locked door
  Level173 恶龙巢穴 - the dragon's hoard cave: a sleeping dragon on piles of gold, crystals, the hero tiptoeing in
  Level174 屠龙决战 - the final battle on a volcano: the dragon breathes fire, the hero's shield, mage's magic circle
"""
import math
import random

from fdcore import E, H, W, lit
from paper import Circ, Ell, Poly, RRect, Thick, flat, ngon, paper_post, piece, soft_union, star_pts
from kit import INK, LAYER, PROP, SMALL, bird_el, cloud_bg, cloud_el, drift_across, house, layer, sky, tree_pine, tree_round
from fills import far_ridge, far_round_trees
from stylekit import flame, smoke
from levels_gothic import bat_el, gothic_arch, knight
from levels_medieval import crenels, stone_blocks

OPTS = dict(post=paper_post, anim_seconds=12.0, frames=60)
NIGHT_EDGE = (120, 110, 140)
SKIN = (246, 214, 186)
GOLD = (240, 196, 70)
GOLD_D = (200, 150, 50)
HERO_TUNIC, HERO_CAPE, HERO_HAIR = (60, 110, 210), (200, 50, 50), (150, 90, 40)


def dpiece(c, shapes, col, border=1.5, shadow=PROP):
    """Paper piece for dark scenes: cut edge in a muted tone instead of glowing white."""
    piece(c, shapes, col, border=border, border_col=NIGHT_EDGE, shadow=shadow)


# =================================================================== characters
def hero(c, x, base, h=1.0, tunic=HERO_TUNIC, cape=HERO_CAPE, hair=HERO_HAIR, face=1, sword="side", shield=None, edge=None, pk=None):
    """The young hero: spiky hair, cape, tunic, boots, sword (side / up / None), optional round shield."""
    pk = pk or piece
    k = face
    pk(c, Poly([(x - 8 * h * k, base - 46 * h), (x + 4 * h * k, base - 46 * h), (x - 6 * h * k, base - 8 * h), (x - 22 * h * k, base - 12 * h)]), cape,
       shadow=PROP)
    flat(c, [RRect(x - 6 * h, base - 22 * h, x - 1 * h, base, 1), RRect(x + 1 * h, base - 22 * h, x + 6 * h, base, 1)], (240, 230, 210))
    flat(c, [RRect(x - 7 * h, base - 10 * h, x - 1 * h, base, 1), RRect(x + 1 * h, base - 10 * h, x + 7 * h + 2 * h * k, base, 1)], (120, 80, 50))
    pk(c, Poly([(x - 10 * h, base - 20 * h), (x + 10 * h, base - 20 * h), (x + 8 * h, base - 46 * h), (x - 8 * h, base - 46 * h)]), tunic, shadow=PROP)
    flat(c, RRect(x - 9 * h, base - 28 * h, x + 9 * h, base - 24 * h, 1), (120, 80, 50))
    flat(c, RRect(x - 2 * h, base - 28 * h, x + 2 * h, base - 24 * h, 0), GOLD)
    hx, hy = x + 1 * h * k, base - 54 * h
    flat(c, Circ(hx, hy, 8 * h), SKIN)
    flat(c, Circ(hx + 3.5 * h * k, hy, 1.2 * h), INK)
    flat(c, Poly([(hx - 10 * h, hy - 1 * h), (hx - 8 * h, hy - 10 * h), (hx - 4 * h, hy - 14 * h), (hx + 2 * h, hy - 12 * h), (hx + 6 * h, hy - 15 * h),
                  (hx + 7 * h, hy - 9 * h), (hx + 11 * h, hy - 7 * h), (hx + 6 * h * k, hy - 4 * h), (hx - 4 * h * k, hy - 3 * h)]), hair)
    if sword == "side":
        flat(c, Thick(x + 8 * h * k, base - 40 * h, x + 14 * h * k, base - 28 * h, 3 * h), SKIN)
        pk(c, Thick(x + 14 * h * k, base - 30 * h, x + 34 * h * k, base - 4 * h, 3.4 * h), (220, 226, 236), shadow=SMALL)
        flat(c, Thick(x + 9 * h * k, base - 34 * h, x + 19 * h * k, base - 26 * h, 2.6 * h), GOLD)
    elif sword == "up":
        flat(c, Thick(x + 8 * h * k, base - 42 * h, x + 14 * h * k, base - 60 * h, 3 * h), SKIN)
        pk(c, Thick(x + 14 * h * k, base - 62 * h, x + 22 * h * k, base - 100 * h, 3.4 * h), (220, 226, 236), shadow=SMALL)
        flat(c, Thick(x + 8 * h * k, base - 62 * h, x + 20 * h * k, base - 60 * h, 2.6 * h), GOLD)
    if shield:
        pk(c, Circ(x - 10 * h * k, base - 34 * h, 12 * h), shield, shadow=SMALL)
        flat(c, Poly(star_pts(x - 10 * h * k, base - 34 * h, 7 * h, 3 * h)), lit(shield, 0.65))
    return hx, hy


def mage(c, x, base, h=1.0, robe=(110, 70, 170), hat=None, hair=(240, 200, 90), orb=(120, 220, 255), face=1, pk=None):
    pk = pk or piece
    k = face
    hat = hat or robe
    pk(c, Poly([(x - 13 * h, base), (x + 13 * h, base), (x + 7 * h, base - 44 * h), (x - 7 * h, base - 44 * h)]), robe, shadow=PROP)
    flat(c, RRect(x - 13 * h, base - 5 * h, x + 13 * h, base, 1), lit(robe, 1.25))
    hx, hy = x + 1 * h * k, base - 52 * h
    flat(c, Ell(hx - 3 * h * k, hy + 3 * h, 9 * h, 11 * h), hair)
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    flat(c, Circ(hx + 3 * h * k, hy, 1.1 * h), INK)
    pk(c, [Ell(hx, hy - 6 * h, 17 * h, 4 * h), Poly([(hx - 9 * h, hy - 7 * h), (hx + 9 * h, hy - 7 * h), (hx - 4 * h * k, hy - 34 * h)])], hat, shadow=SMALL)
    flat(c, Poly(star_pts(hx + 1 * h, hy - 16 * h, 4 * h, 1.6 * h)), GOLD)
    flat(c, Thick(x + 6 * h * k, base - 36 * h, x + 14 * h * k, base - 30 * h, 3 * h), robe)
    pk(c, Thick(x + 16 * h * k, base, x + 16 * h * k, base - 64 * h, 2.4 * h), (140, 96, 60), shadow=SMALL)
    pk(c, Circ(x + 16 * h * k, base - 68 * h, 5 * h), orb, shadow=None)


def healer(c, x, base, h=1.0, robe=(246, 244, 236), trim=(70, 160, 110), hair=(120, 70, 40), face=1, pk=None):
    pk = pk or piece
    k = face
    pk(c, Poly([(x - 12 * h, base), (x + 12 * h, base), (x + 7 * h, base - 44 * h), (x - 7 * h, base - 44 * h)]), robe, shadow=PROP)
    flat(c, [Thick(x, base - 42 * h, x, base - 4 * h, 2.4 * h), RRect(x - 12 * h, base - 5 * h, x + 12 * h, base, 1)], trim)
    hx, hy = x + 1 * h * k, base - 52 * h
    pk(c, Ell(hx - 1 * h * k, hy + 1 * h, 10 * h, 11 * h), trim, shadow=None)
    flat(c, Circ(hx + 1 * h * k, hy + 1 * h, 6.4 * h), SKIN)
    flat(c, Ell(hx + 1 * h * k, hy - 4 * h, 6 * h, 2.6 * h), hair)
    flat(c, Circ(hx + 4 * h * k, hy + 1 * h, 1.1 * h), INK)
    pk(c, Thick(x + 14 * h * k, base, x + 14 * h * k, base - 58 * h, 2.2 * h), (230, 220, 200), shadow=SMALL)
    c.ellipse_ring(x + 14 * h * k, base - 64 * h, 6 * h, 6 * h, 2 * h, GOLD)


def elder(c, x, base, h=1.0, robe=(140, 100, 70), gem=(90, 200, 120), face=1):
    k = face
    piece(c, Poly([(x - 12 * h, base), (x + 12 * h, base), (x + 7 * h, base - 40 * h), (x - 7 * h, base - 40 * h)]), robe, shadow=PROP)
    hx, hy = x + 1 * h * k, base - 47 * h
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    flat(c, Poly([(hx - 5 * h, hy + 2 * h), (hx + 7 * h * k, hy + 2 * h), (hx + 2 * h * k, hy + 20 * h)]), (246, 246, 246))
    flat(c, Ell(hx - 1 * h * k, hy - 5 * h, 8 * h, 3.4 * h), (246, 246, 246))
    flat(c, Circ(hx + 3 * h * k, hy - 1 * h, 1.1 * h), INK)
    piece(c, [Thick(x + 14 * h * k, base, x + 16 * h * k, base - 56 * h, 2.6 * h), Ell(x + 16 * h * k, base - 60 * h, 6 * h, 7 * h)], (130, 90, 56), shadow=SMALL)
    flat(c, Circ(x + 16 * h * k, base - 60 * h, 4.6 * h), gem)


def king(c, x, base, h=1.0, robe=(190, 40, 50), crown=GOLD, pk=None):
    """Seated king (front view)."""
    pk = pk or piece
    pk(c, Poly([(x - 22 * h, base), (x + 22 * h, base), (x + 14 * h, base - 44 * h), (x - 14 * h, base - 44 * h)]), robe, shadow=PROP)
    flat(c, [RRect(x - 22 * h, base - 6 * h, x + 22 * h, base, 2), RRect(x - 3 * h, base - 44 * h, x + 3 * h, base, 0)], (250, 248, 240))
    flat(c, [Circ(x - 14 * h + i * 7 * h, base - 3 * h, 1.2 * h) for i in range(5)], (40, 40, 50))
    flat(c, Ell(x, base - 44 * h, 18 * h, 6 * h), (250, 248, 240))
    hx, hy = x, base - 54 * h
    flat(c, Circ(hx, hy, 8 * h), SKIN)
    flat(c, Poly([(hx - 8 * h, hy + 1 * h), (hx + 8 * h, hy + 1 * h), (hx, hy + 18 * h)]), (240, 240, 240))
    flat(c, [Circ(hx - 3 * h, hy - 1 * h, 1.1 * h), Circ(hx + 3 * h, hy - 1 * h, 1.1 * h)], INK)
    pk(c, Poly([(hx - 9 * h, hy - 5 * h), (hx + 9 * h, hy - 5 * h), (hx + 10 * h, hy - 17 * h), (hx + 5 * h, hy - 11 * h), (hx, hy - 19 * h),
                (hx - 5 * h, hy - 11 * h), (hx - 10 * h, hy - 17 * h)]), crown, shadow=SMALL)
    flat(c, Circ(hx, hy - 8 * h, 1.8 * h), (220, 40, 60))


def princess(c, x, base, h=1.0, dress=(240, 150, 190), hair=(240, 200, 90), pk=None):
    pk = pk or piece
    pk(c, Poly([(x - 18 * h, base), (x + 18 * h, base), (x + 6 * h, base - 30 * h), (x + 6 * h, base - 44 * h), (x - 6 * h, base - 44 * h),
                (x - 6 * h, base - 30 * h)]), dress, shadow=PROP)
    flat(c, [Thick(x - 15 * h, base - 8 * h, x + 15 * h, base - 8 * h, 2 * h)], lit(dress, 1.2))
    hx, hy = x, base - 52 * h
    flat(c, [Ell(hx, hy + 6 * h, 10 * h, 15 * h)], hair)
    flat(c, Circ(hx, hy, 7 * h), SKIN)
    flat(c, [Circ(hx - 2.6 * h, hy, 1.0 * h), Circ(hx + 2.6 * h, hy, 1.0 * h)], INK)
    flat(c, Ell(hx, hy - 5 * h, 8 * h, 3 * h), hair)
    flat(c, Poly([(hx - 6 * h, hy - 7 * h), (hx + 6 * h, hy - 7 * h), (hx + 4 * h, hy - 12 * h), (hx, hy - 9 * h), (hx - 4 * h, hy - 12 * h)]), GOLD)


def slime(c, x, base, s=1.0, col=(100, 200, 240), pk=None):
    pk = pk or piece
    pk(c, Poly([(x - 20 * s, base), (x + 20 * s, base), (x + 18 * s, base - 14 * s), (x + 6 * s, base - 30 * s), (x, base - 34 * s), (x - 6 * s, base - 30 * s),
                (x - 18 * s, base - 14 * s)]), col, shadow=SMALL)
    flat(c, Ell(x - 8 * s, base - 22 * s, 4 * s, 3 * s), lit(col, 1.4))
    flat(c, [Circ(x - 6 * s, base - 14 * s, 2.4 * s), Circ(x + 6 * s, base - 14 * s, 2.4 * s)], (30, 30, 50))
    flat(c, Thick(x - 4 * s, base - 8 * s, x + 4 * s, base - 8 * s, 1.4 * s), (30, 30, 50))


def chest(c, x, base, s=1.0, col=(160, 100, 50), band=GOLD, open_=False, pk=None):
    pk = pk or piece
    w, h = 34 * s, 24 * s
    pk(c, RRect(x - w, base - h, x + w, base, 3 * s), col, shadow=PROP)
    if open_:
        pk(c, Poly([(x - w, base - h), (x + w, base - h), (x + w - 4 * s, base - h - 30 * s), (x - w + 4 * s, base - h - 30 * s)]), lit(col, 0.85), shadow=None)
        flat(c, Ell(x, base - h, w - 4 * s, 6 * s), GOLD)
    else:
        pk(c, [RRect(x - w, base - h - 18 * s, x + w, base - h + 2, 10 * s)], col, shadow=None)
    flat(c, [RRect(x - w + 8 * s, base - h - (0 if open_ else 18 * s), x - w + 14 * s, base, 0), RRect(x + w - 14 * s, base - h - (0 if open_ else 18 * s), x + w - 8 * s, base, 0)],
         band)
    flat(c, RRect(x - 5 * s, base - h - 4 * s, x + 5 * s, base - h + 8 * s, 1), band)


def dragon(c, x, base, s=1.0, body=(70, 150, 90), belly=(230, 210, 140), wing=None, horn=(240, 230, 200), eye=(250, 220, 60), face=1,
           pose="stand", pk=None, spikes=None):
    """Original paper dragon. pose: 'stand' | 'fly' | 'sleep'. (x, base) = belly-on-ground point."""
    pk = pk or piece
    k = face
    wing = wing or lit(body, 0.8)
    spikes = spikes or lit(body, 0.7)
    X = lambda dx: x + dx * s * k
    Y = lambda dy: base - dy * s
    if pose == "sleep":
        pk(c, [Thick(X(-120), Y(30), X(-170), Y(14), 26 * s), Thick(X(-170), Y(14), X(-150), Y(-2), 18 * s), Thick(X(-150), Y(-2), X(40), Y(4), 14 * s),
               Thick(X(40), Y(4), X(90), Y(10), 9 * s)], body, shadow=PROP)
        pk(c, Poly([(X(90), Y(4)), (X(118), Y(14)), (X(92), Y(24))]), spikes, shadow=SMALL)
        pk(c, Ell(X(-40), Y(56), 110 * s, 56 * s), body, shadow=PROP)
        flat(c, Ell(X(-30), Y(26), 80 * s, 18 * s), belly)
        for i in range(7):
            sx = -130 + i * 30
            sy = 56 + 52 * math.sqrt(max(0, 1 - ((sx + 40) / 112) ** 2))
            pk(c, Poly([(X(sx - 12), Y(sy - 6)), (X(sx), Y(sy + 18)), (X(sx + 12), Y(sy - 6))]), spikes, shadow=None)
        pk(c, Poly([(X(-110), Y(70)), (X(-60), Y(118)), (X(10), Y(124)), (X(40), Y(86)), (X(-20), Y(64))]), wing, shadow=SMALL)
        flat(c, [Thick(X(-60), Y(118), X(-30), Y(72), 3 * s), Thick(X(10), Y(124), X(0), Y(72), 3 * s)], lit(wing, 0.8))
        pk(c, [Thick(X(50), Y(60), X(110), Y(30), 30 * s)], body, shadow=SMALL)
        hx, hy = X(130), Y(26)
        pk(c, [Ell(hx, hy, 30 * s, 20 * s), RRect(hx, hy - 10 * s, hx + 44 * s * k, hy + 14 * s, 8 * s) if k > 0 else
               RRect(hx - 44 * s, hy - 10 * s, hx, hy + 14 * s, 8 * s)], body, shadow=SMALL)
        flat(c, Thick(hx + 4 * s * k, hy + 8 * s, hx + 40 * s * k, hy + 8 * s, 2 * s), lit(body, 0.6))
        flat(c, Thick(hx - 4 * s * k, hy - 6 * s, hx + 10 * s * k, hy - 4 * s, 2.4 * s), INK)            # closed eye
        flat(c, Circ(hx + 36 * s * k, hy - 2 * s, 2 * s), INK)
        pk(c, [Poly([(hx - 16 * s * k, hy - 14 * s), (hx - 50 * s * k, hy - 30 * s), (hx - 22 * s * k, hy - 4 * s)]),
               Poly([(hx - 4 * s * k, hy - 18 * s), (hx - 30 * s * k, hy - 44 * s), (hx - 10 * s * k, hy - 10 * s)])], horn, shadow=SMALL)
        return (hx, hy)
    flying = pose == "fly"
    # far wing (behind the body)
    sh = (0, 120)
    pk(c, Poly([(X(-10), Y(110)), (X(-60 if not flying else 20), Y(230 if not flying else 260)), (X(-120 if not flying else -60), Y(200 if not flying else 230)),
                (X(-150 if not flying else -120), Y(150 if not flying else 170)), (X(-70), Y(116))]), lit(wing, 0.85), shadow=SMALL)
    # tail
    tail = [(X(-60), Y(70)), (X(-120), Y(50)), (X(-170), Y(70 if not flying else 40)), (X(-210), Y(110 if not flying else 30))]
    pk(c, [Thick(a[0], a[1], b[0], b[1], (24 - i * 6) * s) for i, (a, b) in enumerate(zip(tail, tail[1:]))], body, shadow=PROP)
    tx, ty = tail[-1]
    pk(c, Poly([(tx, ty - 14 * s), (tx - 24 * s * k, ty), (tx, ty + 14 * s), (tx + 6 * s * k, ty)]), spikes, shadow=SMALL)
    # legs
    if flying:
        pk(c, [Thick(X(-30), Y(56), X(-50), Y(26), 16 * s), Thick(X(30), Y(56), X(44), Y(30), 13 * s)], lit(body, 0.92), shadow=SMALL)
    else:
        pk(c, [Thick(X(-40), Y(60), X(-46), Y(4), 20 * s), Thick(X(34), Y(60), X(38), Y(4), 16 * s)], lit(body, 0.92), shadow=SMALL)
        flat(c, [Ell(X(-40), Y(2), 16 * s, 5 * s), Ell(X(44), Y(2), 14 * s, 5 * s)], lit(body, 0.8))
    # body + belly
    pk(c, Ell(X(-6), Y(76), 72 * s, 42 * s), body, shadow=PROP)
    flat(c, Ell(X(4), Y(62), 54 * s, 22 * s), belly)
    for i in range(4):
        flat(c, Thick(X(-30 + i * 18), Y(48), X(-30 + i * 18), Y(78), 1.4 * s), lit(belly, 0.85))
    # neck + head
    neck = [(X(40), Y(92)), (X(72), Y(130)), (X(86), Y(166))]
    pk(c, [Thick(a[0], a[1], b[0], b[1], (28 - i * 6) * s) for i, (a, b) in enumerate(zip(neck, neck[1:]))], body, shadow=PROP)
    for i in range(6):
        px, py = -50 + i * 24, 116 - abs(i - 2) * 4
        pk(c, Poly([(X(px - 10), Y(py - 6)), (X(px), Y(py + 14)), (X(px + 10), Y(py - 6))]), spikes, shadow=None)
    hx, hy = X(100), Y(176)
    pk(c, [Ell(hx, hy, 26 * s, 18 * s), Poly([(hx, hy - 12 * s), (hx + 44 * s * k, hy - 4 * s), (hx + 46 * s * k, hy + 10 * s), (hx, hy + 14 * s)])],
       body, shadow=SMALL)
    flat(c, Thick(hx + 6 * s * k, hy + 8 * s, hx + 42 * s * k, hy + 6 * s, 2 * s), lit(body, 0.6))
    flat(c, Circ(hx + 40 * s * k, hy - 2 * s, 2 * s), INK)
    flat(c, Ell(hx + 4 * s * k, hy - 5 * s, 6 * s, 5 * s), eye)
    flat(c, Ell(hx + 5 * s * k, hy - 5 * s, 1.6 * s, 4 * s), INK)
    pk(c, [Poly([(hx - 12 * s * k, hy - 12 * s), (hx - 46 * s * k, hy - 36 * s), (hx - 20 * s * k, hy - 2 * s)]),
           Poly([(hx, hy - 16 * s), (hx - 24 * s * k, hy - 52 * s), (hx - 8 * s * k, hy - 8 * s)])], horn, shadow=SMALL)
    # near wing
    wpts = [(X(10), Y(104)), (X(-20 if not flying else 60), Y(240 if not flying else 280)), (X(-80 if not flying else 0), Y(222 if not flying else 270)),
            (X(-120 if not flying else -70), Y(176 if not flying else 210)), (X(-100), Y(130)), (X(-40), Y(110))]
    pk(c, Poly(wpts), wing, shadow=PROP)
    for p in wpts[2:5]:
        flat(c, Thick(wpts[1][0], wpts[1][1], p[0], p[1], 2.4 * s), lit(wing, 0.75))
    flat(c, Thick(wpts[0][0], wpts[0][1], wpts[1][0], wpts[1][1], 4 * s), lit(wing, 0.75))
    return (hx + 46 * s * k, hy + 4 * s)


# =================================================================== Level 170 starting village
def l170_bg(c, d):
    sky(c, (130, 190, 240), (226, 238, 246), 330)
    cloud_bg(c, 120, 60, 0.7)
    cloud_bg(c, 520, 40, 0.5)
    # far dragon peak with a castle on the next hill
    piece(c, Poly([(560, 260), (700, 70), (730, 90), (760, 60), (900, 230), (920, 260)]), (130, 110, 130), shadow=LAYER)
    flat(c, Poly([(700, 70), (730, 90), (760, 60), (770, 100), (690, 100)]), (90, 70, 90))
    far_ridge(c, 250, 50, (150, 186, 200), 1701, step=90)
    piece(c, [RRect(180, 150, 260, 210, 0), RRect(170, 120, 196, 210, 0), RRect(244, 120, 270, 210, 0)], (186, 196, 214), shadow=SMALL)
    crenels(c, 180, 260, 150, (186, 196, 214), size=10)
    piece(c, [Poly([(166, 122), (200, 122), (183, 92)]), Poly([(240, 122), (274, 122), (257, 92)])], (90, 110, 170), shadow=SMALL)
    flat(c, Thick(257, 92, 257, 70, 2), (90, 90, 100))
    piece(c, Poly([(257, 66), (296, 74), (257, 90)]), (220, 60, 60) if "flag" not in d else (250, 200, 60), shadow=None)
    far_round_trees(c, 290, 24, (110, 170, 110), 1702)
    # village street
    layer(c, 330, [(10, 300, 0)], (150, 200, 110))
    for x, s_ in ((240, 1.3), (300, 1.0), (640, 1.2), (880, 1.0)):
        tree_round(c, x, 372, s=s_, col=(90, 160, 90))
    for x in (500, 440):
        tree_pine(c, x, 340, h=90, col=(70, 130, 90))
    house(c, 120, 380, 150, 110, (246, 230, 200), (190, 80, 60), wins=2)
    piece(c, RRect(60, 290, 180, 320, 3), (120, 80, 50), border=1.5, shadow=SMALL)                         # weapon shop sign board
    if "sign" not in d:
        piece(c, [Thick(80, 306, 160, 306, 5), Thick(96, 296, 96, 316, 3)], (220, 226, 236), shadow=None)
    else:
        piece(c, Poly([(104, 294), (136, 294), (136, 306), (120, 318), (104, 306)]), (220, 226, 236), shadow=None)
    from kit import chimney
    chimney(c, 806, 250)
    house(c, 760, 380, 170, 120, (236, 216, 180), (80, 120, 170) if "roof" not in d else (120, 160, 80), wins=3)
    piece(c, RRect(720, 280, 800, 304, 3), (120, 80, 50), border=1.5, shadow=SMALL)
    flat(c, [Ell(746, 292, 10, 7), RRect(756, 288, 774, 298, 2)], (240, 200, 90))                       # inn sign (mug)
    # notice board with quest posters
    piece(c, [RRect(334, 380, 342, 470, 1), RRect(468, 380, 476, 470, 1)], (120, 80, 50), shadow=PROP)
    piece(c, RRect(320, 320, 490, 420, 3), (170, 120, 80), border=1.5, shadow=PROP)
    piece(c, Poly([(310, 324), (500, 324), (405, 290)]), (120, 80, 60), border=1.5, shadow=SMALL)
    posters = [(250, 240, 210), (250, 240, 210), (250, 240, 210)]
    if "poster" in d:
        posters[1] = (250, 190, 190)
    for k, col in enumerate(posters):
        x = 340 + k * 50
        piece(c, RRect(x, 334, x + 40, 400, 1), col, shadow=SMALL)
        flat(c, Circ(x + 20, 336, 3), (200, 50, 50))
    # wanted poster: dragon head silhouette + strokes
    flat(c, Poly([(350, 360), (370, 350), (376, 362), (366, 372), (350, 372)]), (60, 60, 70))
    for k in range(3):
        flat(c, [Thick(396, 350 + k * 12, 424, 350 + k * 12, 2), Thick(446, 350 + k * 12, 474, 350 + k * 12, 2)], (110, 100, 90))
    # cobbled road
    flat(c, Poly([(-10, 480), (910, 480), (910, 610), (-10, 610)]), (196, 184, 164))
    rnd = random.Random(1703)
    for y in range(486, 600, 18):
        x = rnd.uniform(-20, 0)
        while x < 910:
            w = rnd.uniform(24, 40)
            flat(c, RRect(x, y, x + w - 3, y + 14, 5), (210, 200, 180))
            x += w
    # flower pots + well + cart
    for x, col in ((210, (240, 90, 120)), (260, (250, 200, 60))):
        if x == 260 and "flower" in d:
            col = (120, 120, 240)
        piece(c, Poly([(x - 14, 470), (x + 14, 470), (x + 10, 444), (x - 10, 444)]), (190, 110, 70), shadow=SMALL)
        flat(c, [Circ(x - 7, 438, 7), Circ(x + 7, 438, 7), Circ(x, 430, 7)], col)
    piece(c, [Ell(580, 452, 44, 14), RRect(536, 420, 624, 456, 4)], (160, 156, 166), border=1.5, shadow=PROP)
    stone_blocks(c, 536, 420, 624, 456, (130, 126, 136), h=12, w=20)
    piece(c, [RRect(544, 360, 550, 424, 1), RRect(610, 360, 616, 424, 1)], (120, 80, 50), shadow=SMALL)
    piece(c, Poly([(530, 366), (630, 366), (580, 336)]), (190, 80, 60), border=1.5, shadow=SMALL)
    flat(c, Thick(580, 366, 580, 392, 1.4), (90, 80, 70))
    piece(c, Poly([(564, 392), (596, 392), (592, 420), (568, 420)]), (150, 110, 70) if "bucket" not in d else (70, 130, 200), shadow=SMALL)
    piece(c, [RRect(820, 500, 900, 540, 3)], (170, 120, 80), border=1.5, shadow=PROP)
    piece(c, Circ(836, 548, 16), (120, 80, 50), shadow=SMALL)
    flat(c, Circ(836, 548, 5), (80, 60, 40))
    for k in range(3):
        piece(c, Circ(840 + k * 18, 492, 10), (230, 120, 40), shadow=None)
    # villagers waving the hero off
    elder(c, 520, 590, h=1.9, gem=(90, 200, 120) if "gem" not in d else (230, 70, 90), face=-1)
    from kit import person
    person(c, 640, 580, (220, 140, 170), h=1.7)
    person(c, 690, 586, (110, 170, 120), h=1.2, hat=(200, 160, 90))
    # chicken
    if "chicken" not in d:
        piece(c, [Ell(160, 556, 18, 13), Circ(176, 540, 8)], (250, 250, 246), shadow=SMALL)
        flat(c, [Poly([(183, 540), (192, 543), (183, 546)])], (250, 180, 40))
        flat(c, Circ(176, 532, 4), (220, 50, 50))
    # the hero (front, big)
    hero(c, 360, 594, h=2.2, sword="side", shield=(150, 110, 70))


L170_ELEMENTS = [
    E("dragon_far", lambda c, m: dragon(c, 730, 40, s=0.12, body=(70, 50, 70), face=1, pose="fly", pk=lambda c, sh, col, **kw: flat(c, sh, col)),
      pivot=(730, 30), anim=dict(orbitRadius=(40, 10), orbitSpeed=0.08)),
    E("hand", lambda c, m: (flat(c, Thick(650, 528, 666, 506, 4), SKIN), flat(c, Circ(668, 504, 5), SKIN)), pivot=(650, 528),
      anim=dict(swingAngle=20, swingSpeed=1.2)),
    cloud_el("cloud", 330, 90, 0.5, 6),
    bird_el("bird", 450, 80, s=8, speed=20),
] + smoke("chim", 806, 220, n=3)

L170_DIFFS = [
    ("flag", 268, 77, 0),
    ("sign", 120, 306, 0),
    ("roof", 760, 230, 0),
    ("poster", 410, 367, 0),
    ("flower", 260, 434, 0),
    ("bucket", 580, 406, 0),
    ("gem", 490, 476, 0),
    ("chicken", 168, 548, 0),
]


# =================================================================== Level 171 throne room
STONE_T, STONE_TD = (186, 176, 170), (164, 154, 150)


def l171_bg(c, d):
    c.rect(0, 0, W, 430, STONE_T)
    stone_blocks(c, 0, 0, W, 430, STONE_TD, h=22, w=44)
    # tall arched windows with light
    for k, x in enumerate((80, 820)):
        piece(c, gothic_arch(x, 40, 90, 300), (140, 130, 130), border=2, shadow=PROP)
        glass = (160, 200, 240) if not (k == 1 and "window" in d) else (240, 180, 120)
        flat(c, gothic_arch(x, 50, 74, 292), glass)
        flat(c, [Thick(x, 70, x, 292, 3), Thick(x - 37, 180, x + 37, 180, 3)], (140, 130, 130))
    # banners
    for k, x in enumerate((210, 330, 570, 690)):
        col = (60, 90, 170) if k % 2 else (180, 40, 50)
        piece(c, Poly([(x - 30, 30), (x + 30, 30), (x + 30, 240), (x, 270), (x - 30, 240)]), col, border=1.5, shadow=PROP)
        emb = GOLD if not (k == 2 and "banner" in d) else (250, 250, 246)
        flat(c, Poly(star_pts(x, 120, 20, 8)), emb)
        flat(c, RRect(x - 34, 24, x + 34, 34, 2), GOLD_D)
    # dais + throne
    piece(c, RRect(330, 300, 570, 430, 2), (150, 120, 110), border=2, shadow=PROP)
    for k in range(3):
        flat(c, RRect(330 - k * 30, 400 + k * 12, 570 + k * 30, 412 + k * 12, 1), (170, 140, 130))
    piece(c, [Poly([(400, 380), (500, 380), (500, 180), (470, 160), (450, 130), (430, 160), (400, 180)])], GOLD, border=2, shadow=PROP)
    flat(c, Poly([(412, 380), (488, 380), (488, 190), (450, 156), (412, 190)]), (170, 40, 60))
    flat(c, Circ(450, 160, 8), (220, 40, 60))
    king(c, 450, 384, h=2.0, robe=(190, 40, 50) if "robe" not in d else (70, 110, 190))
    # princess beside the throne
    princess(c, 560, 404, h=1.7, dress=(240, 150, 190) if "dress" not in d else (150, 220, 200))
    # advisor
    elder(c, 340, 400, h=1.6, robe=(80, 70, 110), gem=(120, 200, 250))
    # red carpet (perspective) + floor
    c.rect(0, 430, W, H, (200, 190, 176))
    for y in range(430, H, 34):
        flat(c, Thick(0, y, W, y, 1.4), (180, 170, 156))
    for x in range(-400, 1300, 90):
        flat(c, Thick(450 + (x - 450) * 0.3, 430, x, H, 1.4), (180, 170, 156))
    flat(c, Poly([(390, 430), (510, 430), (640, 610), (260, 610)]), GOLD)
    flat(c, Poly([(398, 430), (502, 430), (622, 610), (278, 610)]), (180, 40, 50))
    med = GOLD if "carpet" not in d else (60, 140, 90)
    flat(c, Ell(450, 470, 44, 16), med)
    flat(c, Poly(star_pts(450, 470, 30, 12, rot=-90)), (180, 40, 50))
    # guards
    knight(c, 210, 560, h=1.6, tabard=(180, 40, 50), shield=(240, 200, 60) if "shield" not in d else (90, 160, 220), flip=False, sword_up=True)
    knight(c, 700, 560, h=1.6, tabard=(60, 90, 170), shield=(240, 200, 60), flip=True, sword_up=True)
    # hero kneeling (back view) + gift chest
    piece(c, Poly([(420, 590), (480, 590), (476, 520), (424, 520)]), HERO_CAPE, border=1.5, shadow=PROP)
    flat(c, [RRect(410, 576, 430, 596, 3), RRect(470, 576, 490, 596, 3)], (120, 80, 50))
    flat(c, Circ(450, 510, 15), SKIN)
    flat(c, Poly([(432, 512), (436, 494), (446, 488), (458, 490), (468, 498), (468, 512), (450, 504)]), HERO_HAIR)
    piece(c, Thick(500, 594, 560, 586, 5), (220, 226, 236), shadow=SMALL)
    if "chest" not in d:
        chest(c, 330, 590, s=1.0)
    # potted plants at the corners
    for x in (40, 860):
        piece(c, Poly([(x - 26, 600), (x + 26, 600), (x + 20, 560), (x - 20, 560)]), (200, 180, 150), border=1.5, shadow=PROP)
        piece(c, [Circ(x - 16, 540, 18), Circ(x + 14, 536, 20), Circ(x, 518, 20)], (80, 150, 90), shadow=SMALL)


def chandelier(x, y, n):
    def d(c, m):
        flat(c, Thick(x, 0, x, y, 2), (120, 100, 70))
        piece(c, [Ell(x, y + 6, 70, 10)], GOLD_D, border=1.2, shadow=SMALL)
        for i in range(n):
            cx = x - 60 + i * 120 / (n - 1)
            flat(c, RRect(cx - 3, y - 12, cx + 3, y + 2, 1), (250, 248, 236))
    return d


L171_ELEMENTS = [
    E("chand1", chandelier(210, 290, 5), pivot=(210, 0), anim=dict(swingAngle=0.8, swingSpeed=0.2)),
    E("chand2", chandelier(690, 290, 5), pivot=(690, 0), anim=dict(swingAngle=0.8, swingSpeed=0.2, phase=0.5)),
] + [f for i in range(5) for f in flame("cf%d" % i, 150 + i * 30, 278, s=0.5, glow_night=False)] + \
    [f for i in range(5) for f in flame("cg%d" % i, 630 + i * 30, 278, s=0.5, glow_night=False)] + [
    E("beam1", lambda c, m: soft_union(c, [Poly([(44, 60), (116, 60), (300, 600), (180, 600)])], (255, 246, 210), 0.16, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.25)),
    E("beam2", lambda c, m: soft_union(c, [Poly([(784, 60), (856, 60), (720, 600), (600, 600)])], (255, 246, 210), 0.16, spread=20), daynight="untinted",
      anim=dict(twinkle=0.4, twinkleSpeed=0.25, phase=0.5)),
]

L171_DIFFS = [
    ("window", 820, 160, 0),
    ("banner", 570, 120, 0),
    ("robe", 450, 360, 0),
    ("dress", 560, 380, 0),
    ("carpet", 450, 470, 0),
    ("shield", 190, 488, 0),
    ("chest", 330, 568, 0),
]


# =================================================================== Level 172 dungeon cross-section
DSTONE, DSTONE_D = (84, 80, 100), (66, 62, 82)


def l172_bg(c, d):
    c.rect(0, 0, W, H, (40, 36, 52))
    # rock mass + two corridor levels
    for y0, y1 in ((20, 250), (300, 560)):
        dpiece(c, RRect(-10, y0, 910, y1, 0), DSTONE, shadow=LAYER)
        stone_blocks(c, -10, y0, 910, y1, DSTONE_D, h=24, w=48)
    flat(c, RRect(-10, 250, 910, 300, 0), (56, 50, 66))
    flat(c, RRect(-10, 560, 910, 610, 0), (56, 50, 66))
    for x in range(0, 900, 60):
        flat(c, Thick(x, 254, x + 40, 254, 2), (70, 64, 80))
    # stairs between the levels (right)
    for k in range(6):
        dpiece(c, RRect(720 + k * 26, 300 - k * 10, 900, 310 - k * 10, 1), (100, 94, 110), shadow=None)
    # upper level: locked door, banner, cobwebs, barrels
    dpiece(c, gothic_arch(150, 110, 80, 250), (120, 80, 50))
    flat(c, [Thick(130, 160, 130, 250, 2), Thick(170, 160, 170, 250, 2)], (90, 60, 40))
    flat(c, RRect(136, 196, 164, 222, 3), (200, 200, 210) if "lock" not in d else GOLD)
    flat(c, Thick(110, 188, 190, 188, 4), (60, 56, 70))
    ban = (130, 40, 60) if "banner" not in d else (60, 120, 90)
    dpiece(c, Poly([(380, 40), (440, 40), (440, 160), (410, 180), (380, 160)]), ban)
    flat(c, Circ(410, 96, 14), (200, 180, 120))
    if "web" not in d:
        for a in range(0, 91, 18):
            r = math.radians(a)
            flat(c, Thick(900, 20, 900 - math.cos(r) * 80, 20 + math.sin(r) * 80, 1.2), (200, 200, 210))
        for rr in (30, 55, 78):
            pts = [(900 - math.cos(math.radians(a)) * rr, 20 + math.sin(math.radians(a)) * rr) for a in range(0, 91, 18)]
            flat(c, [Thick(p[0], p[1], q[0], q[1], 1) for p, q in zip(pts, pts[1:])], (200, 200, 210))
    for x in (560, 600):
        dpiece(c, [RRect(x - 18, 196, x + 18, 250, 6)], (130, 90, 60))
        flat(c, [Thick(x - 18, 210, x + 18, 210, 2), Thick(x - 18, 236, x + 18, 236, 2)], (80, 70, 70))
    # wall gem
    dpiece(c, Poly(ngon(700, 100, 16, 6)), (90, 200, 220) if "gem" not in d else (230, 80, 120))
    # the party walking right (upper level)
    hero(c, 380, 250, h=1.7, sword="up", shield=(150, 110, 70), pk=dpiece)
    mage(c, 300, 250, h=1.6, pk=dpiece, robe=(110, 70, 170) if "robe" not in d else (60, 140, 90))
    healer(c, 236, 250, h=1.5, pk=dpiece)
    # hanging chains + crates (fill)
    for x, ln in ((470, 120), (800, 90)):
        for y in range(300, 300 + ln, 10):
            c.ellipse_ring(x, y + 5, 4, 6, 1.6, (130, 126, 140))
    dpiece(c, [RRect(560, 520, 610, 560, 2), RRect(586, 484, 630, 520, 2)], (130, 96, 64))
    flat(c, [Thick(560, 520, 610, 560, 2), Thick(586, 484, 630, 520, 2)], (100, 72, 50))
    dpiece(c, [Ell(470, 230, 16, 20), RRect(462, 206, 478, 214, 2)], (170, 110, 80))
    dpiece(c, [Ell(500, 236, 12, 14)], (150, 100, 120))
    # lower level: spike trap, slimes, treasure, lever
    for i in range(8):
        x = 300 + i * 18
        dpiece(c, Poly([(x, 560), (x + 9, 534), (x + 18, 560)]), (190, 190, 200), shadow=None)
    slime(c, 120, 560, s=1.6, col=(100, 200, 240), pk=dpiece)
    slime(c, 520, 560, s=1.3, col=(240, 120, 160) if "slime" not in d else (250, 200, 60), pk=dpiece)
    chest(c, 680, 560, s=1.3, col=(160, 100, 50), pk=dpiece)
    dpiece(c, RRect(820, 470, 860, 520, 3), (100, 94, 110))
    lever = Thick(840, 500, 812, 460, 4) if "lever" not in d else Thick(840, 500, 868, 460, 4)
    dpiece(c, [lever], (150, 110, 70), shadow=SMALL)
    # skull-free bones: just stacked rocks + a puddle
    flat(c, Ell(250, 558, 40, 6), (60, 80, 110))
    # rope from the upper floor
    flat(c, Thick(40, 300, 40, 470, 3), (180, 150, 100))


def torch_el(x, y):
    return [E("sconce%d" % x, lambda c, m: dpiece(c, [Poly([(x - 8, y), (x + 8, y), (x + 4, y + 20), (x - 4, y + 20)])], (90, 80, 70), shadow=SMALL))] + \
        flame("torch%d" % x, x, y, s=1.4, glow_night=False) + [
        E("tglow%d" % x, lambda c, m: soft_union(c, [Circ(x, y - 10, 30)], (255, 190, 100), 0.25, spread=50), daynight="untinted",
          anim=dict(pulse=0.08, scaleSpeed=1.3, phase=(x * 0.01) % 1))]


L172_ELEMENTS = torch_el(80, 90) + torch_el(500, 90) + torch_el(220, 380) + torch_el(620, 380) + [
    E("orb", lambda c, m: soft_union(c, [Circ(326, 141, 10)], (160, 230, 255), 0.6, spread=24), daynight="untinted", anim=dict(pulse=0.2, scaleSpeed=0.8)),
    bat_el("bat1", 760, 60, s=1.2, r=(40, 14)),
    bat_el("bat2", 420, 340, s=1.0, r=(30, 10), phase=0.4),
    E("drip", lambda c, m: flat(c, Ell(250, 310, 2, 4), (120, 160, 220)), anim=dict(driftVelocity=(0, -140), driftLength=240, driftFade=True)),
    E("sparkle", lambda c, m: flat(c, Poly(star_pts(700, 520, 9, 2, points=4, rot=0)), (255, 240, 180)), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=0.8)),
]

L172_DIFFS = [
    ("lock", 150, 209, 0),
    ("banner", 410, 105, 0),
    ("web", 860, 60, 0),
    ("gem", 700, 100, 0),
    ("robe", 300, 228, 0),
    ("slime", 520, 540, 0),
    ("lever", 840, 480, 0),
]


# =================================================================== Level 173 dragon's hoard
def coin_pile(c, x, base, w, h, seed):
    dpiece(c, Ell(x, base, w, h), GOLD_D, shadow=LAYER)
    flat(c, Ell(x, base - h * 0.15, w * 0.96, h * 0.85), GOLD)
    rnd = random.Random(seed)
    for _ in range(int(w * h / 90)):
        a = rnd.uniform(0, math.pi)
        r = rnd.uniform(0.1, 0.9)
        cx, cy = x + math.cos(a) * w * r, base - math.sin(a) * h * r * 0.9
        flat(c, Ell(cx, cy, 6, 3.4), (250, 222, 110) if rnd.random() < 0.5 else (226, 172, 60))


def l173_bg(c, d):
    c.rect(0, 0, W, H, (34, 30, 46))
    # cave walls and the entrance glow (left)
    dpiece(c, Poly([(-10, -10), (910, -10), (910, 120), (800, 160), (700, 110), (560, 150), (420, 100), (300, 140), (180, 90), (60, 150), (-10, 120)]),
           (56, 50, 70), shadow=LAYER)
    flat(c, Poly([(-10, 200), (60, 160), (110, 240), (90, 420), (-10, 460)]), (90, 120, 150))
    soft_union(c, [Ell(30, 320, 70, 140)], (200, 220, 250), 0.25, spread=40)
    dpiece(c, Poly([(80, 600), (110, 240), (60, 160), (150, 170), (200, 240), (180, 600)]), (60, 54, 74), shadow=LAYER)
    dpiece(c, Poly([(760, 600), (790, 300), (860, 200), (910, 180), (910, 600)]), (60, 54, 74), shadow=LAYER)
    # back wall rock shelves, stalagmites, glowing mushrooms
    dpiece(c, Poly([(150, 600), (190, 260), (300, 200), (420, 230), (560, 190), (700, 240), (790, 300), (800, 600)]), (46, 42, 60), shadow=LAYER)
    for x, hh in ((250, 120), (330, 80), (640, 110), (720, 70)):
        dpiece(c, Poly([(x - 18, 470), (x + 18, 470), (x, 470 - hh)]), (60, 54, 76), shadow=SMALL)
    for x, y in ((300, 230), (420, 260), (580, 220), (690, 270)):
        flat(c, [RRect(x - 2, y, x + 2, y + 12, 1)], (200, 190, 170))
        flat(c, Ell(x, y, 9, 5), (120, 230, 200))
    for x, ln in ((390, 90), (530, 70)):
        flat(c, [Thick(x, 120, x + 8, 120 + ln * 0.5, 2), Thick(x + 8, 120 + ln * 0.5, x - 4, 120 + ln, 2)], (80, 90, 70))
    # stalactites
    for k, (x, ln) in enumerate(((240, 60), (340, 40), (470, 70), (620, 46), (740, 64))):
        if k == 2 and "stalactite" in d:
            continue
        dpiece(c, Poly([(x - 16, 100), (x + 16, 100), (x, 100 + ln)]), (70, 64, 86), shadow=SMALL)
    # crystals on the walls
    for x, y, col, key in ((840, 260, (150, 120, 250), "crystal"), (190, 300, (90, 200, 230), None), (870, 400, (150, 120, 250), None)):
        if key and key in d:
            col = (240, 110, 150)
        for dx, hh in ((-12, 40), (0, 60), (14, 34)):
            dpiece(c, Poly([(x + dx - 7, y), (x + dx + 7, y), (x + dx, y - hh)]), col, shadow=None)
            flat(c, Poly([(x + dx, y - hh), (x + dx + 4, y - 6), (x + dx, y)]), lit(col, 1.3))
    # gold hoard
    coin_pile(c, 480, 610, 420, 150, 1731)
    coin_pile(c, 760, 610, 160, 90, 1732)
    coin_pile(c, 240, 610, 120, 60, 1733)
    # treasures on the pile
    if "crown" not in d:
        dpiece(c, Poly([(640, 520), (690, 520), (694, 488), (680, 502), (665, 484), (650, 502), (636, 488)]), GOLD, shadow=SMALL)
        flat(c, Circ(665, 506, 4), (220, 40, 60))
    dpiece(c, [Poly([(300, 520), (330, 520), (326, 492), (304, 492)]), RRect(312, 520, 318, 540, 0), RRect(302, 540, 328, 546, 1)],
           (200, 204, 216) if "goblet" not in d else (240, 120, 60), shadow=SMALL)
    dpiece(c, Thick(380, 560, 360, 470, 5), (210, 216, 226), shadow=SMALL)
    flat(c, Thick(352, 488, 376, 496, 4), GOLD_D)
    dpiece(c, Circ(580, 560, 22), (180, 50, 60), shadow=SMALL)
    flat(c, Poly(star_pts(580, 560, 12, 5)), GOLD)
    for x, col in ((440, (220, 40, 70)), (520, (60, 160, 230)), (720, (60, 200, 120))):
        if x == 520 and "jewel" in d:
            col = (250, 250, 250)
        dpiece(c, Poly([(x, 550), (x + 16, 568), (x, 586), (x - 16, 568)]), col, shadow=None)
    # the sleeping dragon on top of the pile
    dragon(c, 470, 470, s=1.35, body=(190, 70, 60), belly=(240, 200, 140), wing=(150, 50, 60), horn=(240, 230, 200) if "horn" not in d else (60, 60, 70),
           face=1, pose="sleep", pk=dpiece)
    # the hero tiptoeing in from the entrance, holding a torch
    hero(c, 150, 590, h=1.8, sword=None, shield=(150, 110, 70), pk=dpiece)
    flat(c, Thick(172, 520, 190, 490, 4), (130, 90, 56))


L173_ELEMENTS = flame("torch", 192, 488, s=1.3, glow_night=False) + [
    E("tglow", lambda c, m: soft_union(c, [Circ(192, 476, 30)], (255, 190, 100), 0.3, spread=60), daynight="untinted",
      anim=dict(pulse=0.1, scaleSpeed=1.3)),
    E("z1", lambda c, m: piece(c, [Thick(706, 380, 722, 380, 3), Thick(722, 380, 706, 396, 3), Thick(706, 396, 722, 396, 3)], (240, 240, 250), shadow=None),
      daynight="untinted", anim=dict(driftVelocity=(20, 50), driftLength=90, driftFade=True, driftGrow=0.8)),
    E("z2", lambda c, m: piece(c, [Thick(706, 380, 718, 380, 2.4), Thick(718, 380, 706, 392, 2.4), Thick(706, 392, 718, 392, 2.4)], (240, 240, 250), shadow=None),
      daynight="untinted", anim=dict(driftVelocity=(20, 50), driftLength=90, driftFade=True, driftGrow=0.8, phase=0.5)),
    E("shroom", lambda c, m: [soft_union(c, [Circ(x, y, 8)], (120, 230, 200), 0.4, spread=16) for x, y in ((300, 230), (420, 260), (580, 220), (690, 270))],
      daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=0.4)),
    E("glint1", lambda c, m: flat(c, Poly(star_pts(300, 556, 10, 2, points=4, rot=0)), (255, 250, 220)), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=0.6)),
    E("glint2", lambda c, m: flat(c, Poly(star_pts(800, 556, 10, 2, points=4, rot=0)), (255, 250, 220)), daynight="untinted",
      anim=dict(twinkle=1.0, twinkleSpeed=0.5, phase=0.5)),
    bat_el("bat", 560, 60, s=1.2, r=(50, 16), speed=0.2),
]

L173_DIFFS = [
    ("stalactite", 470, 130, 0),
    ("crystal", 840, 230, 0),
    ("crown", 665, 502, 0),
    ("goblet", 315, 520, 0),
    ("jewel", 520, 568, 0),
    ("horn", 610, 420, 0),
]


# =================================================================== Level 174 final battle on the volcano
def l174_bg(c, d):
    c.gradient(0, 380, (90, 40, 70), (250, 140, 80))
    soft_union(c, [Circ(160, 120, 40)], (255, 220, 160), 0.5, spread=50)
    flat(c, Circ(160, 120, 34), (255, 210, 140))
    # far volcano with lava
    dpiece(c, Poly([(540, 380), (720, 150), (800, 150), (1020, 380)]), (90, 60, 70), shadow=LAYER)
    flat(c, Poly([(720, 150), (800, 150), (786, 166), (734, 166)]), (250, 140, 50))
    flat(c, [Poly([(750, 160), (764, 160), (740, 300), (720, 380), (708, 380), (730, 290)]),
             Poly([(780, 160), (792, 162), (840, 280), (860, 380), (848, 380), (824, 286)])], (250, 120, 50))
    far_ridge(c, 360, 60, (110, 60, 70), 1741, step=80, shadow=LAYER)
    # ruined castle wall (left)
    piece(c, [RRect(0, 200, 110, 400, 0), RRect(110, 270, 230, 400, 0)], (130, 110, 120), border=1.5, border_col=NIGHT_EDGE, shadow=LAYER)
    stone_blocks(c, 0, 200, 230, 400, (110, 92, 104), h=20, w=36)
    crenels(c, 0, 100, 200, (130, 110, 120), size=14)
    flat(c, Thick(60, 200, 60, 120, 3), (60, 50, 50))
    flag = (60, 90, 170) if "flag" not in d else (240, 200, 60)
    dpiece(c, Poly([(60, 120), (110, 132), (96, 140), (112, 150), (60, 156)]), flag, shadow=SMALL)
    # rocky battle ground
    dpiece(c, Poly([(-10, 400), (200, 380), (420, 410), (640, 390), (910, 410), (910, 610), (-10, 610)]), (80, 60, 64), shadow=LAYER)
    flat(c, [Poly([(300, 470), (420, 460), (520, 480), (440, 500), (320, 494)])], (250, 120, 50))         # lava crack
    flat(c, [Poly([(330, 476), (420, 468), (490, 480), (430, 490)])], (255, 200, 90))
    # broken pillars
    for x, hh, key in ((260, 110, None), (840, 150, "pillar")):
        if key and key in d:
            hh = 70
        dpiece(c, [RRect(x - 18, 420 - hh, x + 18, 420, 1), RRect(x - 24, 410, x + 24, 424, 2)], (160, 150, 156))
        flat(c, Poly([(x - 18, 420 - hh), (x - 4, 420 - hh - 12), (x + 8, 420 - hh + 4), (x + 18, 420 - hh - 6), (x + 18, 420 - hh + 6), (x - 18, 420 - hh + 6)]),
             (160, 150, 156))
    # glowing crystal by the ledge
    crys = (120, 220, 250) if "crystal" not in d else (250, 120, 200)
    for dx, hh in ((-10, 40), (2, 60), (16, 30)):
        dpiece(c, Poly([(720 + dx - 8, 460), (720 + dx + 8, 460), (720 + dx, 460 - hh)]), crys, shadow=None)
    # the dragon (flying, facing left towards the party)
    dragon(c, 560, 370, s=1.0, body=(60, 50, 80), belly=(200, 160, 120), wing=(110, 40, 60),
           horn=(240, 230, 200) if "horn" not in d else (60, 180, 200), eye=(250, 90, 40), face=-1, pose="fly", pk=dpiece, spikes=(160, 50, 60))
    # boulders + fallen banner (right ground)
    for x, y, sz in ((620, 470, 26), (680, 520, 34), (880, 470, 30), (780, 560, 40)):
        dpiece(c, Poly([(x - sz, y + sz * 0.5), (x - sz * 0.6, y - sz * 0.5), (x + sz * 0.3, y - sz * 0.7), (x + sz, y + sz * 0.5)]), (100, 76, 80))
    flat(c, Thick(500, 560, 600, 470, 3), (90, 70, 50))
    dpiece(c, Poly([(596, 474), (640, 490), (626, 510), (580, 494)]), (60, 90, 170), shadow=SMALL)
    # the party on the ledge (foreground)
    dpiece(c, Poly([(-10, 520), (120, 500), (330, 520), (360, 610), (-10, 610)]), (70, 52, 58), shadow=LAYER)
    hero(c, 250, 590, h=2.2, sword="up", shield=(150, 110, 70) if "shield" not in d else (60, 120, 200), pk=dpiece)
    mage(c, 110, 590, h=2.0, robe=(110, 70, 170), hat=(110, 70, 170) if "hat" not in d else (190, 60, 60), pk=dpiece)
    healer(c, 40, 596, h=1.7, pk=dpiece)


MOUTH = (414, 198)


def _cone(length, w0, w1, wobble=()):
    """Flame wedge from the dragon's mouth towards the party (down-left)."""
    mx, my = MOUTH
    ang = math.atan2(260, -150)
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    pts = [(mx + nx * w0, my + ny * w0)]
    n = 6
    for i in range(1, n + 1):
        t = i / n
        w = w0 + (w1 - w0) * t + (wobble[i % len(wobble)] if wobble else 0)
        pts.append((mx + ux * length * t + nx * w, my + uy * length * t + ny * w))
    tip = (mx + ux * (length + 20), my + uy * (length + 20))
    back = [(mx + ux * length * (i / n) - nx * (w0 + (w1 - w0) * i / n), my + uy * length * (i / n) - ny * (w0 + (w1 - w0) * i / n)) for i in range(n, -1, -1)]
    return Poly(pts + [tip] + back)


def fire_el(c, m):
    soft_union(c, [_cone(200, 8, 40)], (255, 200, 80), 0.5, spread=14)
    flat(c, _cone(190, 7, 32, (0, 6, -4, 5)), (255, 150, 50))
    flat(c, _cone(150, 4, 16), (255, 240, 160))


def ember(k):
    rnd = random.Random(1740 + k)
    x, y = rnd.uniform(300, 900), rnd.uniform(420, 580)
    return E("ember%d" % k, lambda c, m: flat(c, Circ(x, y, 2.6), (255, 190, 90)), daynight="untinted",
             anim=dict(driftVelocity=(rnd.uniform(-10, 10), 40), driftLength=160, driftFade=True, phase=k / 6))


L174_ELEMENTS = [
    E("fire", fire_el, pivot=MOUTH, daynight="untinted", anim=dict(stretch=(0.08, 0.1), scaleSpeed=3.0, twinkle=0.2, twinkleSpeed=4)),
    E("circle", lambda c, m: (c.ellipse_ring(176, 426, 26, 26, 2.4, (160, 230, 255)), flat(c, Poly(star_pts(176, 426, 22, 9, points=6)), (160, 230, 255, 0.5))),
      pivot=(176, 426), daynight="untinted", anim=dict(rotateSpeed=40, twinkle=0.3, twinkleSpeed=1.0)),
    E("lava", lambda c, m: soft_union(c, [Ell(410, 480, 110, 16)], (255, 160, 60), 0.4, spread=20), daynight="untinted", anim=dict(twinkle=0.5, twinkleSpeed=0.7)),
] + [ember(k) for k in range(6)] + smoke("vsmoke", 760, 150, n=3, col=(120, 90, 100), r=16, rise=(6, 30), length=100)

L174_DIFFS = [
    ("flag", 85, 138, 0),
    ("pillar", 840, 300, 0),
    ("crystal", 722, 432, 0),
    ("horn", 500, 150, 0),
    ("shield", 228, 515, 0),
    ("hat", 110, 450, 0),
]


LEVELS = [
    ("Level170", "勇者启程", l170_bg, L170_ELEMENTS, L170_DIFFS, 60, OPTS),
    ("Level171", "王城觐见", l171_bg, L171_ELEMENTS, L171_DIFFS, 60, OPTS),
    ("Level172", "地下城", l172_bg, L172_ELEMENTS, L172_DIFFS, 60, OPTS),
    ("Level173", "恶龙巢穴", l173_bg, L173_ELEMENTS, L173_DIFFS, 60, OPTS),
    ("Level174", "屠龙决战", l174_bg, L174_ELEMENTS, L174_DIFFS, 60, OPTS),
]
