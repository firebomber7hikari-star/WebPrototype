# -*- coding: utf-8 -*-
"""
Find Differences asset generator (pure Python, no dependencies).

Every level is split into
  * a static background (original / modified)         Art/LevelXX/BG_A.png, BG_B.png
  * animated elements layered on top (transparent)    Art/LevelXX/E_<id>[_A|_B].png
and described by Levels/LevelXX.asset (FindDifferencesLevel ScriptableObject).
UI sprites go to Art/UI_*.png. All .meta files get stable GUIDs derived from the asset path.

Run:  python generate_assets.py            -> writes the assets
      python generate_assets.py --preview[=DIR]  -> also writes preview PNGs (t = 0)
"""
import copy
import hashlib
import json
import math
import os
import random
import struct
import sys
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ART_DIR = os.path.join(ROOT, "Art")
LEVEL_DIR = os.path.join(ROOT, "Levels")

W, H = 900, 600   # picture size in pixels
SS = 2            # supersampling factor


def guid_for(name):
    return hashlib.md5(("FindDifferences/" + name).encode("utf-8")).hexdigest()


LEVEL_SCRIPT_GUID = guid_for("Scripts/FindDifferencesLevel.cs")


# --------------------------------------------------------------------------- PNG
def write_png(path, width, height, rows, alpha):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6 if alpha else 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# ------------------------------------------------------------------- Rasterizer
class Canvas:
    """
    Span rasterizer. All drawing coordinates are scene pixels (y down);
    (ox, oy) is the scene position of the canvas' top-left corner, so a small
    transparent canvas can render one element using the same scene coordinates.
    """

    def __init__(self, w, h, ss=SS, alpha=False, ox=0, oy=0):
        self.ss = ss
        self.ch = 4 if alpha else 3
        self.ox, self.oy = ox, oy
        self.w, self.h = int(round(w * ss)), int(round(h * ss))
        self.rows = [bytearray(self.w * self.ch) for _ in range(self.h)]

    # -- low level
    # A "paint" is either an opaque (r, g, b) tuple, an (r, g, b, alpha 0..1) tuple,
    # or a shader callable(px, py) -> (r, g, b, alpha) evaluated per pixel (scene coords).
    def _pix(self, col):
        return bytes(col[:3]) + (b"\xff" if self.ch == 4 else b"")

    def _span(self, y, x0, x1, col):
        """x0/x1 in scene pixels, y is a supersampled row index."""
        if y < 0 or y >= self.h:
            return
        a = max(0, int(round((x0 - self.ox) * self.ss)))
        b = min(self.w, int(round((x1 - self.ox) * self.ss)))
        if b <= a:
            return
        if callable(col):
            self._blend(y, a, b, col)
        elif len(col) == 4:
            self._blend(y, a, b, lambda px, py, c=col: c)
        else:
            self.rows[y][a * self.ch:b * self.ch] = self._pix(col) * (b - a)

    def _blend(self, y, a, b, shader):
        row, ch, s, ox = self.rows[y], self.ch, self.ss, self.ox
        py = self._py(y)
        for i in range(a, b):
            r, g, bl, al = shader((i + 0.5) / s + ox, py)
            if al <= 0.0:
                continue
            r = 0 if r < 0 else 255 if r > 255 else int(r)
            g = 0 if g < 0 else 255 if g > 255 else int(g)
            bl = 0 if bl < 0 else 255 if bl > 255 else int(bl)
            k = i * ch
            if al >= 1.0:
                row[k], row[k + 1], row[k + 2] = r, g, bl
                if ch == 4:
                    row[k + 3] = 255
            elif ch == 3:
                row[k] += int((r - row[k]) * al)
                row[k + 1] += int((g - row[k + 1]) * al)
                row[k + 2] += int((bl - row[k + 2]) * al)
            else:
                da = row[k + 3] / 255.0
                oa = al + da * (1 - al)
                f = da * (1 - al)
                row[k] = int((r * al + row[k] * f) / oa)
                row[k + 1] = int((g * al + row[k + 1] * f) / oa)
                row[k + 2] = int((bl * al + row[k + 2] * f) / oa)
                row[k + 3] = int(oa * 255)

    def _rows(self, y0, y1):
        a = max(0, int(math.floor((y0 - self.oy) * self.ss)))
        b = min(self.h, int(math.ceil((y1 - self.oy) * self.ss)))
        return range(a, b)

    def _py(self, y):
        return (y + 0.5) / self.ss + self.oy

    # -- primitives
    def gradient(self, y0, y1, c0, c1):
        for y in self._rows(y0, y1):
            t = min(1, max(0, (self._py(y) - y0) / max(1e-6, (y1 - y0))))
            col = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
            self._span(y, self.ox, self.ox + self.w / self.ss, col)

    def rect(self, x0, y0, x1, y1, col):
        for y in self._rows(y0, y1):
            self._span(y, x0, x1, col)

    def ellipse(self, cx, cy, rx, ry, col, ymin=None, ymax=None):
        if rx <= 0 or ry <= 0:          # shapes shrunk past nothing (negative grow) draw nothing
            return
        for y in self._rows(cy - ry, cy + ry):
            py = self._py(y)
            if (ymin is not None and py < ymin) or (ymax is not None and py > ymax):
                continue
            d = 1 - ((py - cy) / ry) ** 2
            if d > 0:
                hw = rx * math.sqrt(d)
                self._span(y, cx - hw, cx + hw, col)

    def circle(self, cx, cy, r, col):
        self.ellipse(cx, cy, r, r, col)

    def ellipse_ring(self, cx, cy, rx, ry, thick, col, ymin=None, ymax=None):
        irx, iry = rx - thick, ry - thick
        for y in self._rows(cy - ry, cy + ry):
            py = self._py(y)
            if (ymin is not None and py < ymin) or (ymax is not None and py > ymax):
                continue
            d = 1 - ((py - cy) / ry) ** 2
            if d <= 0:
                continue
            ow = rx * math.sqrt(d)
            di = 1 - ((py - cy) / iry) ** 2 if iry > 0 else -1
            if di <= 0:
                self._span(y, cx - ow, cx + ow, col)
            else:
                iw = irx * math.sqrt(di)
                self._span(y, cx - ow, cx - iw, col)
                self._span(y, cx + iw, cx + ow, col)

    def polygon(self, pts, col):
        ys = [p[1] for p in pts]
        n = len(pts)
        for y in self._rows(min(ys), max(ys)):
            py = self._py(y)
            xs = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= py < y1) or (y1 <= py < y0):
                    xs.append((x0 + (py - y0) * (x1 - x0) / (y1 - y0), 1 if y1 > y0 else -1))
            xs.sort()
            wind = 0
            for i in range(len(xs) - 1):
                wind += xs[i][1]
                if wind != 0:
                    self._span(y, xs[i][0], xs[i + 1][0], col)

    def line(self, x0, y0, x1, y1, width, col, caps=True):
        if width <= 0:
            return
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln * width / 2, dx / ln * width / 2
        self.polygon([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], col)
        if caps:
            self.circle(x0, y0, width / 2, col)
            self.circle(x1, y1, width / 2, col)

    def round_rect(self, x0, y0, x1, y1, r, col):
        self.rect(x0 + r, y0, x1 - r, y1, col)
        self.rect(x0, y0 + r, x1, y1 - r, col)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
            self.circle(cx, cy, r, col)

    def star(self, cx, cy, r_out, r_in, col, points=5, rot=-90):
        pts = []
        for i in range(points * 2):
            r = r_out if i % 2 == 0 else r_in
            a = math.radians(rot + i * 180 / points)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.polygon(pts, col)

    def bird(self, x, y, size, col):
        self.line(x - size, y - size * 0.45, x, y, size * 0.22, col)
        self.line(x, y, x + size, y - size * 0.45, size * 0.22, col)

    def outline_circle(self, cx, cy, r, w, col):
        self.ellipse_ring(cx, cy, r, r, w, col)

    # -- output
    def downsample(self):
        s, ch = self.ss, self.ch
        ow, oh = self.w // s, self.h // s
        n = s * s
        out = []
        for oy in range(oh):
            srcs = self.rows[oy * s:(oy + 1) * s]
            row = bytearray(ow * ch)
            for ox in range(ow):
                if ch == 3:
                    for c in range(3):
                        t = 0
                        for r in srcs:
                            for k in range(s):
                                t += r[(ox * s + k) * 3 + c]
                        row[ox * 3 + c] = t // n
                else:
                    # premultiplied average avoids dark fringes on transparent edges
                    sa = sr = sg = sb = 0
                    for r in srcs:
                        for k in range(s):
                            i = (ox * s + k) * 4
                            a = r[i + 3]
                            if a:
                                sa += a
                                sr += r[i] * a
                                sg += r[i + 1] * a
                                sb += r[i + 2] * a
                    if sa:
                        row[ox * 4:ox * 4 + 4] = bytes((sr // sa, sg // sa, sb // sa, sa // n))
            out.append(row)
        return ow, oh, out


# ------------------------------------------------------------------- shared shapes
WHITE = (255, 255, 255)
BLACK = (40, 35, 45)


def cloud(c, x, y, k):
    for dx, dy, r in ((0, 0, 30), (32, -14, 36), (66, 0, 30), (34, 10, 30)):
        c.circle(x + dx * k, y + dy * k, r * k, WHITE)


def cloud_bbox(x, y, k, pad=3):
    return (x - 30 * k - pad, y - 50 * k - pad, x + 96 * k + pad, y + 40 * k + pad)


def bird_bbox(x, y, size, pad=2):
    return (x - size - pad - size * 0.11, y - size * 0.56 - pad, x + size + pad + size * 0.11, y + size * 0.11 + pad)


def butterfly(c, x, y, col):
    c.ellipse(x - 7, y - 4, 7, 6, col)
    c.ellipse(x + 7, y - 4, 7, 6, col)
    c.ellipse(x - 5, y + 5, 5, 4, col)
    c.ellipse(x + 5, y + 5, 5, 4, col)
    c.ellipse(x, y, 2, 9, BLACK)


class E:
    """Animated element definition.

    draw(c, modified) paints the element in scene coordinates.
    show: 'both' | 'A' (original only) | 'B' (modified only)
    variant: True if the drawing differs between the pictures (two sprites)
    anim / animB: ElementAnim fields (animB defaults to anim)
    """

    def __init__(self, eid, draw, bbox=None, pivot=None, anim=None, animB=None, show="both", variant=False,
                 daynight="tinted", weather=0):
        """bbox=None: measured automatically from the drawing. pivot=None: bbox centre."""
        self.id, self.draw, self.bbox = eid, draw, bbox
        self.pivot = pivot
        self.anim = anim or {}
        self.animB = self.anim if animB is None else animB
        self.show, self.variant = show, variant
        self.daynight = daynight      # 'tinted' | 'night' (only at night) | 'day' (fades at night) | 'untinted'
        self.weather = weather        # bit mask of WEATHER types the element is visible in (0 = always)


# ------------------------------------------------------------------- lighting / shaders
# Light comes from the upper left, slightly in front (scene coords: x right, y down, z to viewer).
_L = (-0.45, -0.6, 0.66)
_LN = math.sqrt(sum(v * v for v in _L))
LIGHT = tuple(v / _LN for v in _L)
_HV = (LIGHT[0], LIGHT[1], LIGHT[2] + 1.0)
_HN = math.sqrt(sum(v * v for v in _HV))
HALF = tuple(v / _HN for v in _HV)


def lit(col, k):
    """Brighten (k > 1) or darken (k < 1) a colour."""
    return tuple(max(0, min(255, int(c * k))) for c in col[:3])


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def shade_normal(base, nx, ny, nz, amb=0.5, kd=0.65, spec=0.35, shin=28, rim=None, rim_k=0.0, alpha=1.0):
    d = nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]
    k = amb + kd * (d if d > 0 else 0.0)
    h = nx * HALF[0] + ny * HALF[1] + nz * HALF[2]
    sp = spec * (h ** shin) * 255 if h > 0 else 0.0
    r, g, b = base[0] * k + sp, base[1] * k + sp, base[2] * k + sp
    if rim is not None and rim_k > 0:
        e = (1 - max(0.0, nz)) ** 3 * rim_k
        r, g, b = r + (rim[0] - r) * e, g + (rim[1] - g) * e, b + (rim[2] - b) * e
    return (r, g, b, alpha)


def sphere(cx, cy, rx, base, ry=None, **kw):
    """Shader for a lit sphere / ellipsoid centred at (cx, cy)."""
    ry = ry or rx

    def f(px, py):
        nx, ny = (px - cx) / rx, (py - cy) / ry
        d = nx * nx + ny * ny
        nz = math.sqrt(1 - d) if d < 1 else 0.0
        return shade_normal(base, nx, ny, nz, **kw)
    return f


def cylinder(cx, r, base, top=None, bottom=None, ao=0.25, **kw):
    """Vertical cylinder shading (+ ambient occlusion towards `bottom`)."""
    def f(px, py):
        nx = max(-1.0, min(1.0, (px - cx) / r))
        col = shade_normal(base, nx, 0.0, math.sqrt(1 - nx * nx), **kw)
        if top is not None and bottom is not None and ao > 0:
            t = max(0.0, min(1.0, (py - top) / max(1e-6, bottom - top)))
            k = 1 - ao * t * t
            col = (col[0] * k, col[1] * k, col[2] * k, col[3])
        return col
    return f


def cone(ax, ay, by, bw, base, **kw):
    """Cone with apex (ax, ay) and base half-width bw at y = by."""
    def f(px, py):
        hw = max(1e-3, bw * (py - ay) / max(1e-6, by - ay))
        nx = max(-1.0, min(1.0, (px - ax) / hw))
        nz = math.sqrt(1 - nx * nx)
        n = (nx * 0.9, -0.45, nz * 0.9)
        ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
        return shade_normal(base, n[0] / ln, n[1] / ln, n[2] / ln, **kw)
    return f


def linear(x0, y0, x1, y1, c0, c1, alpha=1.0):
    dx, dy = x1 - x0, y1 - y0
    dd = dx * dx + dy * dy or 1

    def f(px, py):
        t = max(0.0, min(1.0, ((px - x0) * dx + (py - y0) * dy) / dd))
        return (c0[0] + (c1[0] - c0[0]) * t, c0[1] + (c1[1] - c0[1]) * t, c0[2] + (c1[2] - c0[2]) * t, alpha)
    return f


def glow(cx, cy, r, col, alpha=0.8, power=2.0, ry=None):
    ry = ry or r

    def f(px, py):
        d = math.sqrt(((px - cx) / r) ** 2 + ((py - cy) / ry) ** 2)
        return (col[0], col[1], col[2], alpha * (1 - d) ** power if d < 1 else 0.0)
    return f


def soft_shadow(cx, cy, rx, ry, alpha=0.35, col=(20, 10, 40)):
    def f(px, py):
        d = ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2
        return (col[0], col[1], col[2], alpha * (1 - d) ** 1.5 if d < 1 else 0.0)
    return f


def shaded_sphere(c, cx, cy, r, base, ry=None, **kw):
    c.ellipse(cx, cy, r, ry or r, sphere(cx, cy, r, base, ry=ry, **kw))


def glow_disc(c, cx, cy, r, col, alpha=0.8, power=2.0, ry=None):
    c.ellipse(cx, cy, r, ry or r, glow(cx, cy, r, col, alpha, power, ry))


def drop_shadow(c, cx, cy, rx, ry, alpha=0.35):
    c.ellipse(cx, cy, rx, ry, soft_shadow(cx, cy, rx, ry, alpha))


def sparkle(c, x, y, r, col=(255, 255, 230)):
    glow_disc(c, x, y, r * 1.6, col, 0.55)
    c.star(x, y, r, r * 0.22, col, points=4, rot=0)


# ------------------------------------------------------------------- UI sprites
def ui_sprite(size, fn):
    rows = []
    for y in range(size):
        row = bytearray(size * 4)
        for x in range(size):
            r, g, b, a = fn(x + 0.5, y + 0.5)
            row[x * 4:x * 4 + 4] = bytes((r, g, b, max(0, min(255, int(a * 255)))))
        rows.append(row)
    return rows


def aa(d):  # signed distance (negative = inside) -> coverage
    return max(0.0, min(1.0, 0.5 - d))


def gen_ui():
    out = {}
    s = 128
    out["UI_Ring"] = (s, ui_sprite(s, lambda x, y: (255, 255, 255,
                      aa(abs(math.hypot(x - 64, y - 64) - 56) - 6))), (0, 0, 0, 0))
    out["UI_Circle"] = (s, ui_sprite(s, lambda x, y: (255, 255, 255,
                        aa(math.hypot(x - 64, y - 64) - 62))), (0, 0, 0, 0))

    def seg_dist(px, py, ax, ay, bx, by):
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - ax - t * dx, py - ay - t * dy)

    out["UI_Cross"] = (s, ui_sprite(s, lambda x, y: (255, 255, 255, aa(min(
        seg_dist(x, y, 24, 24, 104, 104), seg_dist(x, y, 104, 24, 24, 104)) - 11))), (0, 0, 0, 0))

    def rbox(x, y, size=64, r=20):
        qx = abs(x - size / 2) - (size / 2 - r)
        qy = abs(y - size / 2) - (size / 2 - r)
        d = math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - r
        return (255, 255, 255, aa(d + 0.5))
    out["UI_RoundBox"] = (64, ui_sprite(64, rbox), (24, 24, 24, 24))

    def star_fn(x, y):
        def inside(px, py):
            a = math.atan2(py - 64, px - 64) + math.pi / 2
            r = math.hypot(px - 64, py - 64)
            k = (a % (2 * math.pi / 5)) / (2 * math.pi / 5)
            return r < 26 + (58 - 26) * abs(k - 0.5) * 2
        cov = sum(inside(x - 0.5 + ox, y - 0.5 + oy) for oy in (0.25, 0.75) for ox in (0.25, 0.75))
        return (255, 255, 255, cov / 4)
    out["UI_Star"] = (s, ui_sprite(s, star_fn), (0, 0, 0, 0))
    return out


# ------------------------------------------------------------------- meta / yaml
def texture_meta(guid, border=(0, 0, 0, 0), max_size=2048):
    return f"""fileFormatVersion: 2
guid: {guid}
TextureImporter:
  internalIDToNameTable: []
  externalObjects: {{}}
  serializedVersion: 13
  mipmaps:
    mipMapMode: 0
    enableMipMap: 0
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: {max_size}
  textureSettings:
    serializedVersion: 2
    filterMode: 1
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  lightmap: 0
  compressionQuality: 50
  spriteMode: 1
  spriteExtrude: 1
  spriteMeshType: 0
  alignment: 0
  spritePivot: {{x: 0.5, y: 0.5}}
  spritePixelsToUnits: 100
  spriteBorder: {{x: {border[0]}, y: {border[1]}, z: {border[2]}, w: {border[3]}}}
  spriteGenerateFallbackPhysicsShape: 1
  alphaUsage: 1
  alphaIsTransparency: 1
  spriteTessellationDetail: -1
  textureType: 8
  textureShape: 1
  singleChannelComponent: 0
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  applyGammaDecoding: 0
  platformSettings:
  - serializedVersion: 3
    buildTarget: DefaultTexturePlatform
    maxTextureSize: {max_size}
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
    bones: []
    spriteID: {guid[:16]}0800000000000000
    internalID: 0
    vertices: []
    indices:
    edges: []
    weights: []
    secondaryTextures: []
  spritePackingTag:
  pSDRemoveMatte: 0
  pSDShowRemoveMatteOption: 0
  userData:
  assetBundleName:
  assetBundleVariant:
"""


def asset_meta(guid):
    return f"""fileFormatVersion: 2
guid: {guid}
NativeFormatImporter:
  externalObjects: {{}}
  mainObjectFileID: 11400000
  userData:
  assetBundleName:
  assetBundleVariant:
"""


def sprite_ref(guid):
    return "{fileID: 21300000, guid: %s, type: 3}" % guid if guid else "{fileID: 0}"


def num(v):
    return ("%.4f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


ANIM_FIELDS = [
    ("phase", 0), ("bobAmplitude", (0, 0)), ("bobSpeed", 0), ("bounce", False),
    ("swingAngle", 0), ("swingSpeed", 0), ("rotateSpeed", 0),
    ("pulse", 0), ("stretch", (0, 0)), ("scaleSpeed", 0),
    ("twinkle", 0), ("twinkleSpeed", 0),
    ("driftVelocity", (0, 0)), ("driftLength", 0), ("driftStart", 0), ("driftFade", False), ("driftGrow", 0),
    ("orbitRadius", (0, 0)), ("orbitSpeed", 0), ("orbitDepth", 0), ("orbitAlign", False),
    ("spinSpeed", 0), ("spinShade", 0), ("spinSnap", 0), ("blinkInterval", 0), ("blinkDuration", 0.3),
]


def anim_yaml(name, anim, indent):
    unknown = set(anim) - {f for f, _ in ANIM_FIELDS}
    assert not unknown, unknown
    pad = " " * indent
    lines = [f"{pad}{name}:"]
    for field, default in ANIM_FIELDS:
        v = anim.get(field, default)
        if isinstance(default, tuple):
            # anim values use Unity's y-up convention already
            v = f"{{x: {num(float(v[0]))}, y: {num(float(v[1]))}}}"
        elif isinstance(default, bool):
            v = "1" if v else "0"
        else:
            v = num(float(v))
        lines.append(f"{pad}  {field}: {v}")
    return lines


DAYNIGHT_MODES = {"tinted": 0, "night": 1, "day": 2, "untinted": 3}


def night_factor(dn, t):
    """Python port of DayNightCycle.NightFactor (0 = day, 1 = night)."""
    if not dn or dn.get("period", 0) <= 0:
        return 0.0
    raw = 0.5 - 0.5 * math.cos((t / dn["period"] + dn.get("phase", 0.0)) * math.pi * 2)
    x = min(1.0, max(0.0, (raw - 0.25) / 0.5))
    return x * x * (3 - 2 * x)


CLEAR, OVERCAST, RAIN, SNOW, FOG, THUNDER, HEAT = range(7)
WEATHER_TINTS = {OVERCAST: (0.80, 0.82, 0.88), RAIN: (0.64, 0.69, 0.80), SNOW: (0.90, 0.93, 1.00),
                 FOG: (0.90, 0.92, 0.95), THUNDER: (0.46, 0.49, 0.64), HEAT: (1.00, 0.90, 0.72)}
_TINT_FIELDS = {OVERCAST: "overcastTint", RAIN: "rainTint", SNOW: "snowTint", FOG: "fogTint",
                THUNDER: "thunderTint", HEAT: "heatTint"}


def W_(*types):
    """Weather mask helper: W_(RAIN, THUNDER) -> bit mask."""
    m = 0
    for t in types:
        m |= 1 << t
    return m


def weather_weights(wc, t):
    """Python port of WeatherCycle.Evaluate -> list of 7 weights."""
    w = [0.0] * 7
    steps = (wc or {}).get("steps") or []
    if not steps:
        w[0] = 1.0
        return w
    total = sum(max(0.01, d) for _, d in steps)
    tau = t % total
    start = 0.0
    blend = wc.get("blend", 3.0)
    for i, (typ, d) in enumerate(steps):
        d = max(0.01, d)
        if tau < start + d or i == len(steps) - 1:
            nxt = steps[(i + 1) % len(steps)][0]
            b = min(blend, d)
            into = tau - (start + d - b)
            if b > 0 and into > 0:
                x = min(1.0, into / b)
                k = x * x * (3 - 2 * x)
                w[typ] += 1 - k
                w[nxt] += k
            else:
                w[typ] += 1
            return w
        start += d
    return w


def weather_tint(wc, w):
    tints = dict(WEATHER_TINTS)
    tints.update((wc or {}).get("tints", {}))
    out = [w[0]] * 3
    for typ, tint in tints.items():
        for c in range(3):
            out[c] += w[typ] * tint[c]
    return tuple(out)


def night_tint(dn, n):
    tint = dn.get("tint", (0.33, 0.37, 0.62)) if dn else (1, 1, 1)
    return tuple(1 + (c - 1) * n for c in tint)


LEVEL_TIME_LIMIT = 60     # seconds for every level (overrides the per-level value in the level modules)


def level_asset(name, title, guid_a, guid_b, diffs, time_limit, elements, day_night=None, weather=None, orbit=None):
    """diffs: (id, x, y, r) or (id, x, y, r, [(x, y) per main view]) in y-down picture pixels.
    orbit: dict(view_count, hold, turn, frames_a=[guid...], frames_b=[guid...]) for camera-orbit levels."""
    lines = [
        "%YAML 1.1",
        "%TAG !u! tag:unity3d.com,2011:",
        "--- !u!114 &11400000",
        "MonoBehaviour:",
        "  m_ObjectHideFlags: 0",
        "  m_CorrespondingSourceObject: {fileID: 0}",
        "  m_PrefabInstance: {fileID: 0}",
        "  m_PrefabAsset: {fileID: 0}",
        "  m_GameObject: {fileID: 0}",
        "  m_Enabled: 1",
        "  m_EditorHideFlags: 0",
        f"  m_Script: {{fileID: 11500000, guid: {LEVEL_SCRIPT_GUID}, type: 3}}",
        f"  m_Name: {name}",
        "  m_EditorClassIdentifier: ",
        f"  levelName: \"{title.encode('unicode_escape').decode('ascii')}\"",
        f"  original: {sprite_ref(guid_a)}",
        f"  modified: {sprite_ref(guid_b)}",
        f"  timeLimit: {LEVEL_TIME_LIMIT or time_limit}",
        "  differences:",
    ]
    for dd in diffs:
        did, x, y, r = dd[:4]
        lines += [f"  - id: {did}", f"    center: {{x: {num(float(x))}, y: {num(float(H - y))}}}", f"    radius: {r}"]
        views = dd[4] if len(dd) > 4 else []
        if views:
            lines.append("    viewCenters:")
            lines += [f"    - {{x: {num(float(vx))}, y: {num(float(H - vy))}}}" for vx, vy in views]
        else:
            lines.append("    viewCenters: []")
    lines.append("  elements:")
    for e in elements:
        lines += [
            f"  - id: {e['id']}",
            f"    spriteOriginal: {sprite_ref(e['guidA'])}",
            f"    spriteModified: {sprite_ref(e['guidB'])}",
            f"    position: {{x: {num(float(e['pos'][0]))}, y: {num(float(e['pos'][1]))}}}",
            f"    pivot: {{x: {num(float(e['pivot'][0]))}, y: {num(float(e['pivot'][1]))}}}",
        ]
        lines += anim_yaml("animOriginal", e["animA"], 4)
        lines += anim_yaml("animModified", e["animB"], 4)
        lines.append(f"    dayNight: {DAYNIGHT_MODES[e.get('daynight', 'tinted')]}")
        lines.append(f"    weatherMask: {e.get('weather', 0)}")
        lines.append(f"    viewMask: {e.get('viewmask', 0)}")
    dn = day_night or {}
    tint = dn.get("tint", (0.33, 0.37, 0.62))
    lines += ["  dayNight:",
              f"    period: {num(float(dn.get('period', 0)))}",
              f"    phase: {num(float(dn.get('phase', 0)))}",
              f"    nightTint: {{r: {num(float(tint[0]))}, g: {num(float(tint[1]))}, b: {num(float(tint[2]))}, a: 1}}"]
    wc = weather or {}
    lines.append("  weather:")
    steps = wc.get("steps") or []
    if steps:
        lines.append("    steps:")
        for typ, d in steps:
            lines += [f"    - type: {typ}", f"      duration: {num(float(d))}"]
    else:
        lines.append("    steps: []")
    lines.append(f"    blend: {num(float(wc.get('blend', 3.0)))}")
    tints = dict(WEATHER_TINTS)
    tints.update(wc.get("tints", {}))
    for typ, field in _TINT_FIELDS.items():
        r, g, b = tints[typ]
        lines.append(f"    {field}: {{r: {num(float(r))}, g: {num(float(g))}, b: {num(float(b))}, a: 1}}")
    ob = orbit or {}
    lines += ["  orbit:", f"    viewCount: {ob.get('view_count', 3)}", f"    holdTime: {num(float(ob.get('hold', 5.0)))}",
              f"    turnTime: {num(float(ob.get('turn', 1.0)))}"]
    for key, field in (("frames_a", "framesOriginal"), ("frames_b", "framesModified")):
        frames = ob.get(key) or []
        if frames:
            lines.append(f"    {field}:")
            lines += [f"    - {sprite_ref(g)}" for g in frames]
        else:
            lines.append(f"    {field}: []")
    return "\n".join(lines) + "\n"


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def save_image(rel, w, h, rows, alpha, max_size=2048, border=(0, 0, 0, 0)):
    path = os.path.join(ART_DIR, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_png(path, w, h, rows, alpha)
    guid = guid_for("Art/" + rel)
    write_text(path + ".meta", texture_meta(guid, border=border, max_size=max_size))
    return guid


def measure_element(e, modified, margin=150):
    """Scene-space bounding box of everything the element draws."""
    c = Canvas(W + 2 * margin, H + 2 * margin, alpha=True, ox=-margin, oy=-margin)
    e.draw(c, modified)
    xmin = ymin = 10 ** 9
    xmax = ymax = -1
    for j, row in enumerate(c.rows):
        a = bytes(row[3::4])
        st = a.lstrip(b"\x00")
        if not st:
            continue
        ymin, ymax = min(ymin, j), max(ymax, j)
        xmin = min(xmin, len(a) - len(st))
        xmax = max(xmax, len(a.rstrip(b"\x00")) - 1)
    if ymax < 0:
        raise ValueError(f"element {e.id} draws nothing")
    s = c.ss
    return (math.floor(-margin + xmin / s) - 1, math.floor(-margin + ymin / s) - 1,
            math.ceil(-margin + (xmax + 1) / s) + 1, math.ceil(-margin + (ymax + 1) / s) + 1)


def resolve_layout(e):
    if e.bbox is None:
        keys = [k for k in ("A", "B") if e.show in ("both", k)]
        boxes = [measure_element(e, k == "B") for k in (keys if e.variant else keys[:1])]
        e.bbox = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                  max(b[2] for b in boxes), max(b[3] for b in boxes))
    if e.pivot is None:
        e.pivot = ((e.bbox[0] + e.bbox[2]) / 2, (e.bbox[1] + e.bbox[3]) / 2)


def render_element(e, modified, post=None):
    x0, y0, x1, y1 = e.bbox
    x0, y0 = math.floor(x0), math.floor(y0)
    x1, y1 = math.ceil(x1), math.ceil(y1)
    c = Canvas(x1 - x0, y1 - y0, alpha=True, ox=x0, oy=y0)
    e.draw(c, modified)
    w, h, rows = c.downsample()
    if post:
        post(rows, w, h, x0, y0, True)
    return (x0, y0, w, h), rows


def eval_anim(a, t):
    """Python port of ElementAnim.Evaluate (keep in sync with FindDifferencesLevel.cs).
    Returns offset (Unity y-up px), angle (deg, CCW), (scale x, scale y), alpha, brightness."""
    tau = math.pi * 2
    g = lambda k, d=0: a.get(k, d)
    ph = g("phase") * tau

    bob = math.sin(t * g("bobSpeed") * tau + ph)
    amp = g("bobAmplitude", (0, 0))
    ox, oy = amp[0] * bob, amp[1] * bob
    if g("bounce", False):
        oy = abs(bob) * amp[1]

    angle = g("rotateSpeed") * t + g("swingAngle") * math.sin(t * g("swingSpeed") * tau + ph)

    w = math.sin(t * g("scaleSpeed") * tau + ph)
    s = 1 + g("pulse") * w
    st = g("stretch", (0, 0))
    sx, sy = s * (1 + st[0] * w), s * (1 + st[1] * w)

    alpha = 1 - g("twinkle") * (0.5 + 0.5 * math.sin(t * g("twinkleSpeed") * tau + ph))
    bright = 1.0

    orb = g("orbitRadius", (0, 0))
    if g("orbitSpeed") != 0 and (orb[0] != 0 or orb[1] != 0):
        an = t * g("orbitSpeed") * tau + ph
        ox += math.cos(an) * orb[0]
        oy += math.sin(an) * orb[1]
        depth = -math.sin(an)  # lower half of the tilted orbit is closer to the viewer
        k = 1 + g("orbitDepth") * depth
        sx, sy = sx * k, sy * k
        bright *= 1 - g("orbitDepth") * 0.8 * (1 - depth) / 2
        if g("orbitAlign", False):
            sgn = 1 if g("orbitSpeed") > 0 else -1
            angle += math.degrees(math.atan2(math.cos(an) * orb[1] * sgn, -math.sin(an) * orb[0] * sgn))

    if g("spinSpeed") != 0:
        cs = math.cos(t * g("spinSpeed") * tau + ph)
        if g("spinSnap") > 0:  # stay mostly flat, flip quickly (paper cut-out turning around)
            cs = math.copysign(abs(cs) ** (1 - 0.9 * g("spinSnap")), cs)
        sx *= cs
        bright *= 1 - g("spinShade") * (1 - abs(cs))

    if g("blinkInterval") > 0:
        iv = g("blinkInterval")
        local = (t + g("phase") * iv) % iv
        dd = max(0.01, g("blinkDuration", 0.3))
        kk = 1 - local / dd if local < dd else 0.0
        if dd * 0.3 < local < dd * 0.45:
            kk *= 0.25
        alpha *= kk

    v = g("driftVelocity", (0, 0))
    length = g("driftLength")
    sp = math.hypot(v[0], v[1])
    if length > 0 and sp > 0:
        d = (g("phase") * length + t * sp) % length
        ox += v[0] / sp * (g("driftStart") + d)
        oy += v[1] / sp * (g("driftStart") + d)
        p = d / length
        if g("driftFade", False):
            alpha *= math.sin(p * math.pi)
        k = 1 + g("driftGrow") * p
        sx, sy = sx * k, sy * k
    return (ox, oy), angle, (sx, sy), alpha, bright


def downscale(rows, w, h, k):
    """Box-downscale RGB rows by integer factor k."""
    if k == 1:
        return [bytearray(r) for r in rows]
    out = []
    for oy in range(h // k):
        src = rows[oy * k:(oy + 1) * k]
        row = bytearray((w // k) * 3)
        for ox in range(w // k):
            for c in range(3):
                t = 0
                for r in src:
                    for i in range(k):
                        t += r[(ox * k + i) * 3 + c]
                row[ox * 3 + c] = t // (k * k)
        out.append(row)
    return out


def draw_sprite(dst, k, spr, t, night=0.0, tint=(1.0, 1.0, 1.0), weather=None):
    """Composite one animated element into preview rows `dst` (scale 1/k of the picture)."""
    (offx, offy), ang, (sx, sy), al, br = eval_anim(spr["anim"], t)
    mask = spr.get("weather", 0)
    if mask:
        if weather is None:
            al *= 1.0 if mask & 1 else 0.0
        else:
            al *= min(1.0, sum(wv for i, wv in enumerate(weather) if mask & (1 << i)))
    mode = spr.get("daynight", "tinted")
    if mode == "night":
        al *= night
        tint = (1.0, 1.0, 1.0)
    elif mode == "day":
        al *= 1 - night
        tint = (1.0, 1.0, 1.0)
    elif mode == "untinted":
        tint = (1.0, 1.0, 1.0)
    mul = (br * tint[0], br * tint[1], br * tint[2])
    if al <= 0.004 or abs(sx) < 1e-3 or abs(sy) < 1e-3:
        return
    rows, w, h = spr["rows"], spr["w"], spr["h"]
    pvx, pvy = spr["pivot_px"]
    px, py = spr["pos"][0] + offx, spr["pos"][1] + offy
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    xs, ys = [], []
    for lx, ly in ((-pvx, -pvy), (w - pvx, -pvy), (-pvx, h - pvy), (w - pvx, h - pvy)):
        lx, ly = lx * sx, ly * sy
        xs.append(px + ca * lx - sa * ly)
        ys.append(py + sa * lx + ca * ly)
    dw, dh = W // k, H // k
    i0, i1 = max(0, int(min(xs) / k)), min(dw, int(max(xs) / k) + 1)
    j0, j1 = max(0, int((H - max(ys)) / k)), min(dh, int((H - min(ys)) / k) + 1)
    for j in range(j0, j1):
        wy = H - (j + 0.5) * k - py
        drow = dst[j]
        for i in range(i0, i1):
            wx = (i + 0.5) * k - px
            u = (ca * wx + sa * wy) / sx + pvx
            v = (-sa * wx + ca * wy) / sy + pvy
            if 0 <= u < w and 0 <= v < h:
                srow = rows[h - 1 - int(v)]
                q = int(u) * 4
                a = srow[q + 3]
                if a:
                    f = a / 255.0 * al
                    for c in range(3):
                        d = drow[i * 3 + c]
                        drow[i * 3 + c] = int(d + (min(255, srow[q + c] * mul[c]) - d) * f)


def _tables(tint):
    return [bytes(min(255, int(v * tint[c])) for v in range(256)) for c in range(3)]


def render_frame(bg_small, sprites, k, t, day_night=None, weather=None):
    night = night_factor(day_night, t)
    tint = night_tint(day_night, night)
    wts = None
    if weather and weather.get("steps"):
        wts = weather_weights(weather, t)
        wt = weather_tint(weather, wts)
        tint = (tint[0] * wt[0], tint[1] * wt[1], tint[2] * wt[2])
    rows = [bytearray(r) for r in bg_small]
    if tint != (1.0, 1.0, 1.0) and min(tint) < 0.999:
        tabs = _tables(tint)
        for r in rows:
            for c in range(3):
                r[c::3] = bytes(r[c::3]).translate(tabs[c])
    for spr in sprites:
        draw_sprite(rows, k, spr, t, night, tint, wts)
    return rows


def write_apng(path, w, h, frames, fps):
    """Animated PNG (plays in browsers / most image viewers)."""
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    out = [b"\x89PNG\r\n\x1a\n", chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)),
           chunk(b"acTL", struct.pack(">II", len(frames), 0))]
    seq = 0
    for n, rows in enumerate(frames):
        out.append(chunk(b"fcTL", struct.pack(">IIIIIHHBB", seq, w, h, 0, 0, 1, fps, 0, 0)))
        seq += 1
        data = zlib.compress(b"".join(b"\x00" + bytes(r) for r in rows), 6)
        if n == 0:
            out.append(chunk(b"IDAT", data))
        else:
            out.append(chunk(b"fdAT", struct.pack(">I", seq) + data))
            seq += 1
    out.append(chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(b"".join(out))


def stack(top, bottom, w, gap=6, col=(60, 40, 70)):
    sep = [bytearray(bytes(col) * w) for _ in range(gap)]
    return top + sep + bottom


def check_differences(name, a, b, diffs, threshold=24, pad=6):
    """QA: pixels that differ between the two pictures must lie inside a marked difference.
    Prints per-difference pixel counts (0 usually means a purely animated difference)."""
    inside = [0] * len(diffs)
    stray = 0
    stray_box = [W, H, 0, 0]
    for y in range(H):
        ra, rb = a[y], b[y]
        if ra == rb:
            continue
        for x in range(W):
            k = x * 3
            if abs(ra[k] - rb[k]) + abs(ra[k + 1] - rb[k + 1]) + abs(ra[k + 2] - rb[k + 2]) < threshold:
                continue
            hit = False
            for i, (_, cx, cy, r) in enumerate(diffs):
                if (x - cx) ** 2 + (y - cy) ** 2 <= (r + pad) ** 2:
                    inside[i] += 1
                    hit = True
            if not hit:
                stray += 1
                stray_box = [min(stray_box[0], x), min(stray_box[1], y), max(stray_box[2], x), max(stray_box[3], y)]
    report = ", ".join(f"{d[0]}={n}" for d, n in zip(diffs, inside))
    warn = f"  !! {stray} stray px in {stray_box}" if stray > 30 else ""
    print(f"  check {name}: {report}{warn}")


def fit_differences(name, a, b, diffs, threshold=24, search=170):
    """Auto-size differences given as (id, x, y, 0): every changed pixel goes to the nearest such hint within
    `search` px; the region becomes the circle around that pixel cluster's bounding box.
    Differences with an explicit radius (> 0, e.g. purely animated ones) are kept as they are."""
    hints = [(i, d[1], d[2]) for i, d in enumerate(diffs) if d[3] <= 0]
    boxes = {i: [10 ** 9, 10 ** 9, -1, -1] for i, _, _ in hints}
    for y in range(H):
        ra, rb = a[y], b[y]
        if ra == rb:
            continue
        for x in range(W):
            k = x * 3
            if abs(ra[k] - rb[k]) + abs(ra[k + 1] - rb[k + 1]) + abs(ra[k + 2] - rb[k + 2]) < threshold:
                continue
            best, bd = None, search * search
            for i, hx, hy in hints:
                dd = (x - hx) ** 2 + (y - hy) ** 2
                if dd <= bd:
                    best, bd = i, dd
            if best is not None:
                bx = boxes[best]
                bx[0], bx[1] = min(bx[0], x), min(bx[1], y)
                bx[2], bx[3] = max(bx[2], x), max(bx[3], y)
    out = list(diffs)
    for i, hx, hy in hints:
        x0, y0, x1, y1 = boxes[i]
        if x1 < 0:
            print(f"  !! {name}: difference '{diffs[i][0]}' shows no visible change near ({hx}, {hy})")
            out[i] = (diffs[i][0], hx, hy, 30) + tuple(diffs[i][4:])
            continue
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        r = 0.5 * math.hypot(x1 - x0 + 1, y1 - y0 + 1) * 0.92 + 8
        out[i] = (diffs[i][0], int(round(cx)), int(round(cy)), int(round(max(18, r)))) + tuple(diffs[i][4:])
    return out


ACTIVE = None     # difference ids shown in the B picture of the level being built (None = all of them)


def on(did, modified):
    """For elements that draw several differences in one sprite: True when drawing the B picture and difference `did`
    is one of the level's selected differences (see diff_selection.json)."""
    return modified and (ACTIVE is None or did in ACTIVE)


SELECTION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_selection.json")
_selection = None


def diff_selection():
    """{level: [difference ids actually used]} chosen by diff_select.py; levels missing from it use all their diffs."""
    global _selection
    if _selection is None:
        _selection = json.load(open(SELECTION_FILE, encoding="utf-8")) if os.path.exists(SELECTION_FILE) else {}
    return _selection


def _hsv(px, k):
    import colorsys
    return colorsys.rgb_to_hsv(px[k] / 255.0, px[k + 1] / 255.0, px[k + 2] / 255.0)


def region_mask(rows, seed, limit=9000, mode="hue"):
    """The paper piece under `seed`: connected pixels (4-neighbour) of the same hue as the seed (lit and shaded faces
    of one piece belong together; white cut edges and outlines stop it). Returns (pixels, bbox), or (None, pixels seen)
    when it grows past `limit` pixels. mode "flat": exact colour match only (one face of a piece)."""
    sx, sy = seed
    r0 = rows[sy][sx * 3:sx * 3 + 3]
    h0, s0, v0 = _hsv(rows[sy], sx * 3)
    grey = s0 < 0.18
    seen = {(sx, sy)}
    stack = [(sx, sy)]
    out = []
    x0 = y0 = 10 ** 9
    x1 = y1 = -1
    while stack:
        x, y = stack.pop()
        out.append((x, y))
        if len(out) > limit:
            return None, seen
        x0, y0, x1, y1 = min(x0, x), min(y0, y), max(x1, x), max(y1, y)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen:
                if mode == "flat":
                    px, k = rows[ny], nx * 3
                    ok = abs(px[k] - r0[0]) + abs(px[k + 1] - r0[1]) + abs(px[k + 2] - r0[2]) <= 30
                    if ok:
                        seen.add((nx, ny))
                        stack.append((nx, ny))
                    continue
                h, sat, v = _hsv(rows[ny], nx * 3)
                if grey:
                    ok = sat < 0.18 and abs(v - v0) < 0.08
                else:
                    dh = min(abs(h - h0), 1 - abs(h - h0))
                    ok = dh < 0.035 and abs(sat - s0) < 0.22 and abs(v - v0) < 0.32
                if ok:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
    return out, (x0, y0, x1, y1)


def recolor_pixels(rows, pixels, hue_shift):
    """Spot-the-difference recolour of one paper piece, aiming for colours that still look natural: green foliage
    turns autumn orange, grey / pale pieces get a clear tint, anything else swaps to a contrasting hue."""
    import colorsys
    if not pixels:
        return
    hs = [_hsv(rows[y], x * 3) for x, y in pixels[:400]]
    mh = sum(h for h, _, _ in hs) / len(hs)
    ms = sum(s for _, s, _ in hs) / len(hs)
    for x, y in pixels:
        k = x * 3
        h, sat, v = _hsv(rows[y], k)
        if ms < 0.18:
            h, sat, v = hue_shift / 360.0, 0.5, min(max(v, 0.45), 0.85)
        elif 0.2 < mh < 0.47:                       # greens
            h, sat, v = 0.08, max(sat, 0.55), max(v, 0.5)
        else:
            h, v = (h + hue_shift / 360.0) % 1.0, max(v, 0.35)
        rows[y][k:k + 3] = bytes(int(round(c * 255)) for c in colorsys.hsv_to_rgb(h, sat, v))


def apply_selection(name, elements, diffs):
    """Keep only the differences chosen by diff_select.py, with the circles it measured (no re-fitting). Elements listed
    as `neutral` only carried dropped differences: they are drawn and animated the same in both pictures (B-only ones
    are removed)."""
    sel = diff_selection().get(name)
    if sel is None:
        return elements, diffs
    neutral = set(sel.get("neutral", []))
    out = []
    for e in elements:
        if e.id in neutral:
            if e.show == "B":
                continue
            e = copy.copy(e)
            e.variant, e.show, e.animB = False, "both", e.anim
        out.append(e)
    circles = sel.get("circles", {})
    kept = [(d[0],) + tuple(circles.get(d[0], d[1:4])) for d in diffs if d[0] in sel["keep"]]
    return out, kept


def build_level(name, title, background, elements, diffs, time_limit,
                preview_dir=None, anim_dir=None, frames=48, fps=12, post=None, day_night=None, anim_seconds=None,
                weather=None, preview_time=0.0):
    """post(rows, w, h, ox, oy, has_alpha): optional pass over every finished image (e.g. paper grain).
    day_night: dict(period=seconds, phase=0..1, tint=(r, g, b)) enables the day/night cycle.
    anim_seconds: length of the animated preview (time-lapse when longer than frames / fps).
    weather: dict(steps=[(type, seconds), ...], blend=seconds, tints={type: (r, g, b)}) weather cycle."""
    global ACTIVE
    elements, diffs = apply_selection(name, elements, diffs)
    sel = diff_selection().get(name)
    ACTIVE = set(sel["keep"]) if isinstance(sel, dict) else None
    autos = sel.get("auto", []) if isinstance(sel, dict) else []
    diff_ids = {d[0] for d in diffs}
    diffs = list(diffs) + [("auto%d" % i,) + tuple(a[4:7] if len(a) >= 7 else (a[0], a[1], 0)) for i, a in enumerate(autos)]
    bg = {}
    plain_a = None
    for key, d in (("A", set()), ("B", diff_ids)):
        c = Canvas(W, H)
        background(c, d)
        w, h, rows = c.downsample()
        if key == "A":
            plain_a = [bytearray(r) for r in rows]
        else:
            for x, y, shift, *rest in autos:          # recolour the paper piece under the seed (found in the plain A picture)
                pixels, _ = region_mask(plain_a, (x, y), mode=rest[0] if rest else "hue")
                if pixels:
                    recolor_pixels(rows, pixels, shift)
        if post:
            post(rows, w, h, 0, 0, False)
        bg[key] = rows
        bg["guid" + key] = save_image(f"{name}/BG_{key}.png", w, h, rows, alpha=False, max_size=1024)

    entries = []
    sprites = {"A": [], "B": []}
    for e in elements:
        resolve_layout(e)
        guids = {}
        cache = None
        x0, y0 = math.floor(e.bbox[0]), math.floor(e.bbox[1])
        x1, y1 = math.ceil(e.bbox[2]), math.ceil(e.bbox[3])
        px, py = e.pivot
        for key in ("A", "B"):
            if e.show not in ("both", key):
                guids[key] = None
                continue
            if key == "B" and not e.variant and guids.get("A"):
                guids["B"] = guids["A"]
            else:
                suffix = f"_{key}" if e.variant else ""
                box, rows = render_element(e, key == "B", post)
                guids[key] = save_image(f"{name}/E_{e.id}{suffix}.png", box[2], box[3], rows, alpha=True)
                cache = (box, rows)
            (bx, by, bw, bh), rows = cache
            sprites[key].append(dict(rows=rows, w=bw, h=bh, pivot_px=(px - x0, bh - (py - y0)),
                                     pos=(px, H - py), anim=e.anim if key == "A" else e.animB, daynight=e.daynight,
                                     weather=e.weather))
        entries.append(dict(
            id=e.id, guidA=guids["A"], guidB=guids["B"],
            pos=(px, H - py),
            pivot=((px - x0) / (x1 - x0), 1 - (py - y0) / (y1 - y0)),
            animA=e.anim, animB=e.animB, daynight=e.daynight, weather=e.weather))

    if any(d[3] <= 0 for d in diffs):
        a = render_frame(bg["A"], sprites["A"], 1, preview_time, day_night, weather)
        b = render_frame(bg["B"], sprites["B"], 1, preview_time, day_night, weather)
        diffs = fit_differences(name, a, b, diffs)

    path = os.path.join(LEVEL_DIR, name + ".asset")
    write_text(path, level_asset(name, title, bg["guidA"], bg["guidB"], diffs, time_limit, entries, day_night, weather))
    write_text(path + ".meta", asset_meta(guid_for("Levels/" + name + ".asset")))
    print("wrote", name, "-", len(entries), "elements")

    if preview_dir:
        os.makedirs(preview_dir, exist_ok=True)
        a = render_frame(bg["A"], sprites["A"], 1, preview_time, day_night, weather)
        b = render_frame(bg["B"], sprites["B"], 1, preview_time, day_night, weather)
        check_differences(name, a, b, diffs)
        mark = Canvas(W, H, ss=1)
        mark.rows = b
        for _, x, y, r in diffs:
            mark.outline_circle(x, y, r, 3, (255, 0, 0))
        write_png(os.path.join(preview_dir, name + "_preview.png"), W, H * 2 + 6, stack(a, b, W), alpha=False)

    if anim_dir:
        os.makedirs(anim_dir, exist_ok=True)
        k = 2
        small = {key: downscale(bg[key], W, H, k) for key in ("A", "B")}
        out = []
        step = (anim_seconds / frames) if anim_seconds else 1.0 / fps
        for f in range(frames):
            t = f * step
            out.append(stack(render_frame(small["A"], sprites["A"], k, t, day_night, weather),
                             render_frame(small["B"], sprites["B"], k, t, day_night, weather), W // k, gap=4))
        path = os.path.join(anim_dir, name + "_anim.png")
        write_apng(path, W // k, (H // k) * 2 + 4, out, fps)
        print("wrote", path)
