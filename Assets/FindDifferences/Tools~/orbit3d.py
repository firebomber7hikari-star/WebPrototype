# -*- coding: utf-8 -*-
"""
Tiny 3D paper-diorama renderer + builder for camera-orbit levels (CameraOrbit in FindDifferencesLevel.cs).

The scene sits on a round paper turntable. It is rendered with an orthographic camera (fixed pitch) from
`frames` yaw angles over a full turn; the runtime flips through those frames while the camera turns and holds
on `view_count` main views (frame 0, frames/view_count, ...). The light is fixed in the world, so faces change
brightness and ground shadows swing around as the camera orbits.

Primitives: box, gable roof, cylinder, cone, sphere, flat ground decal. Painter's algorithm per object.
"""
import math
import os

from fdcore import (Canvas, H, LEVEL_DIR, W, asset_meta, check_differences, downscale, draw_sprite, guid_for, level_asset,
                    lit, render_element, resolve_layout, save_image, stack, write_apng, write_png, write_text)
from paper import Circ, Ell, Poly, RRect, flat, piece, soft_union

PITCH = math.radians(34.0)
CX, CY, SCALE = 450.0, 335.0, 34.0
_L = (-0.55, 0.45, 0.72)
_LN = math.sqrt(sum(v * v for v in _L))
LIGHT = tuple(v / _LN for v in _L)          # world space, fixed while the camera turns
OBJ_SHADOW = (2, 4, 6, 0.35)


# ------------------------------------------------------------------- camera
class Cam:
    def __init__(self, yaw):
        self.yaw = yaw
        self.c, self.s = math.cos(yaw), math.sin(yaw)
        self.sp, self.cp = math.sin(PITCH), math.cos(PITCH)

    def rot(self, x, y):
        return x * self.c + y * self.s, -x * self.s + y * self.c

    def proj(self, x, y, z=0.0):
        xr, yr = self.rot(x, y)
        return (CX + xr * SCALE, CY + (yr * self.sp - z * self.cp) * SCALE)

    def depth(self, x, y, z=0.0):
        _, yr = self.rot(x, y)
        return yr * self.cp + z * self.sp

    def facing(self, n):
        _, nyr = self.rot(n[0], n[1])
        return nyr * self.cp + n[2] * self.sp > 0.02


def shade(col, n, amb=0.6, kd=0.5):
    d = max(0.0, n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2])
    return lit(col, amb + kd * d)


def _norm(v):
    ln = math.sqrt(sum(a * a for a in v)) or 1.0
    return tuple(a / ln for a in v)


def _rot2(px, py, a):
    ca, sa = math.cos(a), math.sin(a)
    return px * ca - py * sa, px * sa + py * ca


def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


# ------------------------------------------------------------------- primitives
class Obj:
    """faces: [(points3d, normal, colour)], centre for sorting, footprint + height for the ground shadow."""

    def __init__(self, faces, centre, footprint=None, height=0.0, sphere=None, border=1.6, shadow=True):
        self.faces, self.centre = faces, centre
        self.footprint, self.height = footprint or [], height
        self.sphere = sphere            # (x, y, z, r, colour)
        self.border, self.shadow = border, shadow


def box(x, y, z, w, d, h, col, rot=0.0):
    a = math.radians(rot)
    local = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    base = [(x + p[0], y + p[1]) for p in (_rot2(px, py, a) for px, py in local)]
    faces = [([(bx, by, z + h) for bx, by in base], (0, 0, 1), col)]
    for i in range(4):
        (x0, y0), (x1, y1) = base[i], base[(i + 1) % 4]
        n = _norm((y1 - y0, -(x1 - x0), 0))
        faces.append(([(x0, y0, z), (x1, y1, z), (x1, y1, z + h), (x0, y0, z + h)], n, col))
    return Obj(faces, (x, y, z + h / 2), base, z + h)


def roof(x, y, z, w, d, h, col, rot=0.0, overhang=0.2):
    a = math.radians(rot)
    w2, d2 = w / 2 + overhang, d / 2 + overhang

    def P(px, py, pz):
        rx, ry = _rot2(px, py, a)
        return (x + rx, y + ry, pz)
    ridge_l, ridge_r = P(-w2, 0, z + h), P(w2, 0, z + h)
    faces = []
    for side in (1, -1):
        n_local = _norm((0, side * h, d2))
        nx, ny = _rot2(n_local[0], n_local[1], a)
        faces.append(([ridge_l, ridge_r, P(w2, side * d2, z), P(-w2, side * d2, z)], (nx, ny, n_local[2]), col))
    for side in (1, -1):
        nx, ny = _rot2(side, 0, a)
        faces.append(([P(side * w2, -d2, z), P(side * w2, d2, z), P(side * w2, 0, z + h)], (nx, ny, 0), lit(col, 0.92)))
    fp = [P(-w2, -d2, 0)[:2], P(w2, -d2, 0)[:2], P(w2, d2, 0)[:2], P(-w2, d2, 0)[:2]]
    return Obj(faces, (x, y, z + h * 0.4), fp, z + h)


def cylinder(x, y, z0, z1, r, col, n=18):
    faces = [([(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z1) for k in range(n)], (0, 0, 1), col)]
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        am = (a0 + a1) / 2
        faces.append(([(x + r * math.cos(a0), y + r * math.sin(a0), z0), (x + r * math.cos(a1), y + r * math.sin(a1), z0),
                       (x + r * math.cos(a1), y + r * math.sin(a1), z1), (x + r * math.cos(a0), y + r * math.sin(a0), z1)],
                      (math.cos(am), math.sin(am), 0), col))
    fp = [(x + r * math.cos(2 * math.pi * k / 12), y + r * math.sin(2 * math.pi * k / 12)) for k in range(12)]
    return Obj(faces, (x, y, (z0 + z1) / 2), fp, z1)


def cone(x, y, z0, z1, r, col, n=18):
    faces = []
    h = z1 - z0
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        am = (a0 + a1) / 2
        faces.append(([(x + r * math.cos(a0), y + r * math.sin(a0), z0), (x + r * math.cos(a1), y + r * math.sin(a1), z0), (x, y, z1)],
                      _norm((math.cos(am) * h, math.sin(am) * h, r)), col))
    fp = [(x + r * math.cos(2 * math.pi * k / 12), y + r * math.sin(2 * math.pi * k / 12)) for k in range(12)]
    return Obj(faces, (x, y, z0 + h * 0.35), fp, z1)


def sphere(x, y, z, r, col):
    fp = [(x + r * math.cos(2 * math.pi * k / 12), y + r * math.sin(2 * math.pi * k / 12)) for k in range(12)]
    return Obj([], (x, y, z), fp, z + r * 0.6, sphere=(x, y, z, r, col))


def decal(pts, col, z=0.0):
    """Flat shape lying on the ground (no shadow, drawn before all objects)."""
    return Obj([([(px, py, z) for px, py in pts], (0, 0, 1), col)], (0, 0, -100), shadow=False, border=0)


def circle_pts(x, y, r, n=32):
    return [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


# ------------------------------------------------------------------- rendering
def _sphere_shader(cx, cy, rr, col, cam):
    lx, ly = cam.rot(LIGHT[0], LIGHT[1])
    # light in screen space: x right, y down the screen, z out of the screen towards the viewer
    sl = _norm((lx, ly * cam.sp - LIGHT[2] * cam.cp, ly * cam.cp + LIGHT[2] * cam.sp))

    def f(px, py):
        nx, ny = (px - cx) / rr, (py - cy) / rr
        d2 = nx * nx + ny * ny
        nz = math.sqrt(1 - d2) if d2 < 1 else 0.0
        k = 0.6 + 0.5 * max(0.0, nx * sl[0] + ny * sl[1] + nz * sl[2])
        return (col[0] * k, col[1] * k, col[2] * k, 1.0)
    return f


def render_scene(c, objs, cam, base_radius=10.5, base_col=(150, 196, 118), side_col=(170, 128, 92), thick=0.9):
    # turntable
    rx, ry = base_radius * SCALE, base_radius * SCALE * cam.sp
    t = thick * cam.cp * SCALE
    soft_union(c, [Ell(CX + 6, CY + t + 14, rx, ry)], (40, 40, 60), 0.3, spread=20)
    piece(c, [Ell(CX, CY + t, rx, ry), RRect(CX - rx, CY, CX + rx, CY + t, 0)], side_col, border=3, shadow=None)
    flat(c, Ell(CX, CY, rx, ry), base_col)
    # ground decals
    for o in objs:
        if not o.shadow and o.faces:
            for pts, n, col in o.faces:
                flat(c, Poly([cam.proj(*p) for p in pts]), col)
    # ground shadows (light fixed in the world)
    sx, sy = -LIGHT[0] / LIGHT[2], -LIGHT[1] / LIGHT[2]
    shapes = []
    for o in objs:
        if not o.shadow or not o.footprint:
            continue
        pts = o.footprint + [(px + sx * o.height * 0.85, py + sy * o.height * 0.85) for px, py in o.footprint]
        hull = convex_hull(pts)
        if len(hull) >= 3:
            shapes.append(Poly([cam.proj(px, py, 0.0) for px, py in hull]))
    if shapes:
        soft_union(c, shapes, (40, 50, 40), 0.22, spread=5)
    # objects, far to near
    for o in sorted((o for o in objs if o.shadow), key=lambda o: cam.depth(*o.centre)):
        if o.sphere:
            x, y, z, r, col = o.sphere
            px, py = cam.proj(x, y, z)
            rr = r * SCALE
            piece(c, Circ(px, py, rr), col, border=o.border, shadow=OBJ_SHADOW)
            c.ellipse(px, py, rr, rr, _sphere_shader(px, py, rr, col, cam))
            continue
        vis = []
        for pts, n, col in o.faces:
            if cam.facing(n):
                vis.append((sorted_depth(cam, pts), Poly([cam.proj(*p) for p in pts]), shade(col, n)))
        if not vis:
            continue
        piece(c, [v[1] for v in vis], vis[0][2], border=o.border, shadow=OBJ_SHADOW)
        for _, poly, col in sorted(vis, key=lambda v: v[0]):
            flat(c, poly, col)


def sorted_depth(cam, pts):
    return sum(cam.depth(*p) for p in pts) / len(pts)


# ------------------------------------------------------------------- orbit timing (mirror of CameraOrbit.Evaluate)
def orbit_state(t, view_count=3, hold=5.0, turn=1.0):
    seg = hold + turn
    idx = int(math.floor(t / seg))
    local = t - idx * seg
    frm = idx % view_count
    if local <= hold:
        k = 0.0
    else:
        x = min(1.0, (local - hold) / turn)
        k = x * x * (3 - 2 * x)
    return (frm + k) / view_count, frm, k


def view_weight(view, frm, k, view_count):
    if view == frm:
        return 1.0 if k <= 0 else max(0.0, min(1.0, 1 - k / 0.15))
    if view == (frm + 1) % view_count:
        return max(0.0, min(1.0, (k - 0.85) / 0.15))
    return 0.0


# ------------------------------------------------------------------- builder
def build_orbit_level(name, title, scene, view_elements, global_elements, diffs3d, time_limit, sky,
                      frames=24, view_count=3, hold=5.0, turn=1.0, post=None,
                      preview_dir=None, anim_dir=None, **_):
    """scene(diff_ids) -> [Obj]; view_elements(cam, view) -> [E]; sky(c) paints the backdrop;
    diffs3d: [(id, (x, y, z), radius_px[, (screen_dx, screen_dy)])] - the optional offset is applied in screen space
    (for billboard elements such as flags that always point the same way on screen)."""
    diff_ids = {d[0] for d in diffs3d}
    guids = {"A": [], "B": []}
    small = {"A": [], "B": []}
    full_main = {}
    for k in range(frames):
        cam = Cam(2 * math.pi * k / frames)
        for key, d in (("A", set()), ("B", diff_ids)):
            c = Canvas(W, H)
            sky(c)
            render_scene(c, scene(d), cam)
            w, h, rows = c.downsample()
            if post:
                post(rows, w, h, 0, 0, False)
            guids[key].append(save_image(f"{name}/F_{key}_{k:02d}.png", w, h, rows, alpha=False, max_size=1024))
            if anim_dir:
                small[key].append(downscale(rows, W, H, 2))
            if k % (frames // view_count) == 0:
                full_main[(key, k // (frames // view_count))] = rows
    print("  rendered", frames, "frames x 2")

    # elements: global ones + per-view ones (viewMask bit)
    all_elements = [(e, 0) for e in global_elements]
    for v in range(view_count):
        cam = Cam(2 * math.pi * v / view_count)
        all_elements += [(e, 1 << v) for e in view_elements(cam, v)]
    entries, sprites = [], {"A": [], "B": []}
    for e, vmask in all_elements:
        resolve_layout(e)
        gids, cache = {}, None
        x0, y0 = math.floor(e.bbox[0]), math.floor(e.bbox[1])
        x1, y1 = math.ceil(e.bbox[2]), math.ceil(e.bbox[3])
        px, py = e.pivot
        for key in ("A", "B"):
            if e.show not in ("both", key):
                gids[key] = None
                continue
            if key == "B" and not e.variant and gids.get("A"):
                gids["B"] = gids["A"]
            else:
                box_, rows = render_element(e, key == "B", post)
                gids[key] = save_image(f"{name}/E_{e.id}{'_' + key if e.variant else ''}.png", box_[2], box_[3], rows, alpha=True)
                cache = (box_, rows)
            (bx, by, bw, bh), rows = cache
            sprites[key].append(dict(rows=rows, w=bw, h=bh, pivot_px=(px - x0, bh - (py - y0)), pos=(px, H - py),
                                     anim=e.anim if key == "A" else e.animB, viewmask=vmask))
        entries.append(dict(id=e.id, guidA=gids["A"], guidB=gids["B"], pos=(px, H - py),
                            pivot=((px - x0) / (x1 - x0), 1 - (py - y0) / (y1 - y0)), animA=e.anim, animB=e.animB,
                            daynight=e.daynight, weather=e.weather, viewmask=vmask))

    # differences: centre per main view
    diffs = []
    per_view = []
    for v in range(view_count):
        cam = Cam(2 * math.pi * v / view_count)
        row = []
        for dd in diffs3d:
            x, y = cam.proj(*dd[1])
            off = dd[3] if len(dd) > 3 else (0, 0)
            row.append((x + off[0], y + off[1]))
        per_view.append(row)
    for i, dd in enumerate(diffs3d):
        did, p, r = dd[:3]
        views = [per_view[v][i] for v in range(view_count)]
        diffs.append((did, views[0][0], views[0][1], r, views))

    orbit = dict(view_count=view_count, hold=hold, turn=turn, frames_a=guids["A"], frames_b=guids["B"])
    path = os.path.join(LEVEL_DIR, name + ".asset")
    write_text(path, level_asset(name, title, guids["A"][0], guids["B"][0], diffs, time_limit, entries, orbit=orbit))
    write_text(path + ".meta", asset_meta(guid_for("Levels/" + name + ".asset")))
    print("wrote", name, "-", len(entries), "elements,", frames, "frames per picture")

    def compose(rows_bg, key, view, k_scale, t=0.0, weights=None):
        rows = [bytearray(r) for r in rows_bg]
        for spr in sprites[key]:
            vm = spr["viewmask"]
            if vm:
                if weights:
                    w = sum(weights[v] for v in range(view_count) if vm & (1 << v))
                else:
                    w = 1.0 if vm & (1 << view) else 0.0
                if w < 0.5:
                    continue
            draw_sprite(rows, k_scale, spr, t)
        return rows

    if preview_dir:
        os.makedirs(preview_dir, exist_ok=True)
        for v in range(view_count):
            a = compose(full_main[("A", v)], "A", v, 1)
            b = compose(full_main[("B", v)], "B", v, 1)
            view_diffs = [(d[0], d[4][v][0], d[4][v][1], d[3]) for d in diffs]
            check_differences(f"{name} view {v}", a, b, view_diffs)
            mark = Canvas(W, H, ss=1)
            mark.rows = b
            for _, x, y, r in view_diffs:
                mark.outline_circle(x, y, r, 3, (255, 0, 0))
            write_png(os.path.join(preview_dir, f"{name}_view{v}.png"), W, H * 2 + 6, stack(a, b, W), alpha=False)

    if anim_dir:
        os.makedirs(anim_dir, exist_ok=True)
        cycle = view_count * (hold + turn)
        n_frames, fps = 108, 12
        out = []
        for f in range(n_frames):
            t = cycle * f / n_frames
            yaw01, frm, k = orbit_state(t, view_count, hold, turn)
            idx = int(round(yaw01 * frames)) % frames
            weights = [view_weight(v, frm, k, view_count) for v in range(view_count)]
            cur = frm if k < 0.5 else (frm + 1) % view_count
            out.append(stack(compose(small["A"][idx], "A", cur, 2, t, weights),
                             compose(small["B"][idx], "B", cur, 2, t, weights), W // 2, gap=4))
        p = os.path.join(anim_dir, name + "_anim.png")
        write_apng(p, W // 2, (H // 2) * 2 + 4, out, fps)
        print("wrote", p)
