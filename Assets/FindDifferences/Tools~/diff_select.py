# -*- coding: utf-8 -*-
"""
Picks which of a level's candidate differences are actually used (written to diff_selection.json, applied by
fdcore.build_level / apply_selection). Rules:
  * 3..5 differences per level (MIN_COUNT..MAX_COUNT)
  * any two differences are at least MIN_GAP px apart, edge to edge (15 % of the 900 px canvas width)
  * a difference needs >= MIN_PX changed pixels (smaller ones are hard to find and are dropped); purely animated
    differences (no static change) are not used
  * differences drawn by one shared element (e.g. an interior sprite that changes three things at once) form a bundle
    that is kept or dropped as a whole - unless the element tests each one with fdcore.on(id, m)
  * if fewer than MIN_COUNT existing differences fit, the level gets recolour differences: a solid paper piece
    (700-8000 px, not under an animated sprite, MIN_GAP from everything else) changes colour in B (fdcore.recolor_pixels)
  * among the valid choices: most differences first, then the largest total changed area

Every difference is measured on its own (background with only that id applied; each element switched to its B version
on its own), so the circles written to the selection are exact and are used as they are (no re-fitting).

  python diff_select.py measure [Level06 ...]   measure all candidates (writes nothing to Art/Levels) -> diff_stats.json
  python diff_select.py select                  choose subsets (+ recolours) from diff_stats.json -> diff_selection.json
  python diff_select.py verify [-v]             check the built Levels/*.asset of the scene list against the rules
"""
import itertools
import json
import math
import os
import re
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
STATS = os.path.join(HERE, "diff_stats.json")
SELECTION = os.path.join(HERE, "diff_selection.json")

MIN_COUNT, MAX_COUNT = 3, 5
MIN_GAP = 0.15 * 900          # 135 px between circles
MIN_PX = 400
THRESHOLD = 24                # same colour threshold as fdcore.check_differences / fit_differences
SEARCH = 170
AUTO_AREA = (700, 8000)
AUTO_SHIFTS = (150, 210, 120, 180)


def scene_levels():
    """Level names in the order of the Test77 scene list."""
    import fdcore
    names = {fdcore.guid_for("Levels/Level%02d.asset" % n): "Level%02d" % n for n in range(1, 1000)}
    text = open(os.path.join(fdcore.ROOT, "Test77.unity"), encoding="utf-8").read()
    block = text.split("  levels:", 1)[1].split("  startLevel:", 1)[0]
    return [names[g] for g in re.findall(r"guid: ([0-9a-f]{32})", block) if g in names]


# ------------------------------------------------------------------- measuring
def _changed(a, b):
    out = []
    for y in range(len(a)):
        ra, rb = a[y], b[y]
        if ra == rb:
            continue
        for x in range(len(ra) // 3):
            k = x * 3
            if abs(ra[k] - rb[k]) + abs(ra[k + 1] - rb[k + 1]) + abs(ra[k + 2] - rb[k + 2]) >= THRESHOLD:
                out.append((x, y))
    return out


def circle_of(pixels):
    """Same circle rule as fdcore.fit_differences, around a pixel set."""
    xs = [p[0] for p in pixels]
    ys = [p[1] for p in pixels]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    r = 0.5 * math.hypot(x1 - x0 + 1, y1 - y0 + 1) * 0.92 + 8
    return [int(round((x0 + x1) / 2)), int(round((y0 + y1) / 2)), int(round(max(18, r)))]


def _level(name):
    import generate_assets
    entry = next(l for l in generate_assets.ALL_LEVELS if l[0] == name)
    _, title, background, elements, diffs, time_limit, *opts = entry
    return background, elements, diffs, (opts[0] if opts else {})


def _measure(name):
    """Every candidate on its own: the background with only that id applied, and every element whose B version
    (variant drawing / A-B only / own B animation) changes the picture, switched on its own. An element whose change
    touches several differences ties them into one bundle."""
    import fdcore
    background, elements, diffs, opts = _level(name)
    if "custom" in opts:
        return name, None
    post, dn, wt = opts.get("post"), opts.get("day_night"), opts.get("weather")
    t0 = opts.get("preview_time", 0.0)

    def bg(d):
        c = fdcore.Canvas(fdcore.W, fdcore.H)
        background(c, d)
        w, h, rows = c.downsample()
        if post:
            post(rows, w, h, 0, 0, False)
        return rows

    sprites = {}
    for e in elements:
        fdcore.resolve_layout(e)
        x0, y0 = math.floor(e.bbox[0]), math.floor(e.bbox[1])
        px, py = e.pivot
        for key in ("A", "B"):
            if e.show not in ("both", key):
                continue
            box, rows = fdcore.render_element(e, key == "B" and (e.variant or e.show == "B"), post)   # as build_level does
            bx, by, bw, bh = box
            sprites[(e.id, key)] = dict(rows=rows, w=bw, h=bh, pivot_px=(px - x0, bh - (py - y0)), pos=(px, fdcore.H - py),
                                        anim=e.anim if key == "A" else e.animB, daynight=e.daynight, weather=e.weather)

    def layer(swap=None, override=None):
        out = []
        for e in elements:
            key = "B" if e.id == swap else "A"
            if e.id == swap and override is not None:
                out.append(override)
            elif (e.id, key) in sprites:
                out.append(sprites[(e.id, key)])
        return out

    def owners_of(changed):
        owners = {}
        for x, y in changed:
            best, bd = None, SEARCH * SEARCH
            for did, hx, hy in hints:
                dd = (x - hx) ** 2 + (y - hy) ** 2
                if dd <= bd:
                    best, bd = did, dd
            if best is not None:
                owners.setdefault(best, []).append((x, y))
        return owners

    bg_a = bg(set())
    pic_a = fdcore.render_frame(bg_a, layer(), 1, t0, dn, wt)
    hints = [(d[0], d[1], d[2]) for d in diffs]
    pix = {d[0]: set() for d in diffs}
    for did, _, _ in hints:
        pix[did].update(_changed(pic_a, fdcore.render_frame(bg({did}), layer(), 1, t0, dn, wt)))
    carriers, granular = {}, []
    for e in elements:
        if not (e.variant or e.show != "both" or e.animB != e.anim):
            continue
        changed = _changed(pic_a, fdcore.render_frame(bg_a, layer(e.id), 1, t0, dn, wt))
        # an element named like a difference owns all of its change; others go to the nearest difference hint
        owners = {e.id: changed} if (changed and e.id in pix) else owners_of(changed)
        if len(owners) > 1 and e.variant:
            # does the element draw each difference separately (fdcore.on)? then attribute its pixels by which
            # difference was switched on, and do not bundle them
            full = set(p for pts in owners.values() for p in pts)
            per = {}
            for o in owners:
                fdcore.ACTIVE = {o}
                try:
                    box, rows = fdcore.render_element(e, True, post)
                finally:
                    fdcore.ACTIVE = None
                spr = dict(sprites[(e.id, "B")], rows=rows)
                per[o] = _changed(pic_a, fdcore.render_frame(bg_a, layer(e.id, spr), 1, t0, dn, wt))
            if any(set(v) != full for v in per.values()):
                granular.append(e.id)
                owners = {o: v for o, v in per.items() if v}
        if not owners:                       # animation-only change: owner by id, else the nearest hint
            ex, ey = (e.bbox[0] + e.bbox[2]) / 2, (e.bbox[1] + e.bbox[3]) / 2
            ids = [h[0] for h in hints]
            owners = {e.id if e.id in ids else min(hints, key=lambda h: (h[1] - ex) ** 2 + (h[2] - ey) ** 2)[0]: []}
        for did, pts in owners.items():
            pix[did].update(pts)
        carriers[e.id] = sorted(owners)
    out = []
    for d in diffs:
        p = pix[d[0]]
        circ = circle_of(p) if p else [d[1], d[2], d[3] or 30]
        out.append(dict(id=d[0], x=circ[0], y=circ[1], r=circ[2], px=len(p)))
    return name, dict(diffs=out, carriers=carriers, granular=granular)


def measure(names):
    stats = json.load(open(STATS, encoding="utf-8")) if os.path.exists(STATS) else {}
    with Pool(min(14, os.cpu_count() or 4)) as pool:
        for name, st in pool.imap_unordered(_measure, names):
            if st is not None:
                stats[name] = st
                print(name, len(st["diffs"]), "candidates,", len(st["carriers"]), "carrier elements", flush=True)
            else:
                print(name, "custom builder - handled separately", flush=True)
    json.dump(stats, open(STATS, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


# ------------------------------------------------------------------- choosing
def gap(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"]) - a["r"] - b["r"]


def bundles(st):
    """Differences tied together by a carrier element (union-find)."""
    parent = {d["id"]: d["id"] for d in st["diffs"]}

    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for eid, ids in st["carriers"].items():
        if eid in st.get("granular", []):      # draws each difference on its own (fdcore.on)
            continue
        for a, b in zip(ids, ids[1:]):
            parent[root(a)] = root(b)
    groups = {}
    for d in st["diffs"]:
        groups.setdefault(root(d["id"]), []).append(d)
    return list(groups.values())


def best_subset(units):
    """units: lists of differences that go together. Best flat list with <= MAX_COUNT, all >= MIN_GAP apart."""
    best = None
    for k in range(1, len(units) + 1):
        for combo in itertools.combinations(units, k):
            flat_ = [d for u in combo for d in u]
            if len(flat_) > MAX_COUNT:
                continue
            if all(gap(a, b) >= MIN_GAP for a, b in itertools.combinations(flat_, 2)):
                score = (len(flat_), sum(d["px"] for d in flat_))
                if best is None or score > best[0]:
                    best = (score, flat_)
    return best[1] if best else []


def _auto(job):
    """Recolour candidates for one level: solid paper pieces away from the kept differences and from animated sprites."""
    import colorsys
    import fdcore
    name, kept, want = job
    background, elements, diffs, opts = _level(name)
    c = fdcore.Canvas(fdcore.W, fdcore.H)
    background(c, set())
    _, _, rows = c.downsample()
    boxes = []
    for e in elements:
        fdcore.resolve_layout(e)
        x0, y0, x1, y1 = e.bbox
        if (x1 - x0) * (y1 - y0) < 0.25 * fdcore.W * fdcore.H:   # full-screen effects (rain, fog, flash) do not block
            boxes.append((x0 - 10, y0 - 10, x1 + 10, y1 + 10))
    found = []
    for mode in ("hue", "flat"):          # whole pieces first; single faces only as a fallback
        visited = set()
        for sy in range(16, fdcore.H - 16, 10):
            for sx in range(16, fdcore.W - 16, 10):
                if (sx, sy) in visited:
                    continue
                k = sx * 3
                r, g, b = (v / 255.0 for v in rows[sy][k:k + 3])
                _, sat, val = colorsys.rgb_to_hsv(r, g, b)
                pixels, bb = fdcore.region_mask(rows, (sx, sy), mode=mode)
                if pixels is None:
                    visited.update(bb)          # oversized region: its pixels are not seeds either
                    continue
                visited.update(pixels)
                area = len(pixels)
                x0, y0, x1, y1 = bb
                w, h = x1 - x0 + 1, y1 - y0 + 1
                if not (AUTO_AREA[0] <= area <= AUTO_AREA[1]) or min(w, h) < 20 or max(w, h) > 4 * min(w, h):
                    continue
                inside = set(pixels)
                if area < 0.42 * w * h or ((x0 + x1) // 2, (y0 + y1) // 2) not in inside:   # rings, halos round a sun / moon
                    continue
                if x0 < 8 or y0 < 8 or x1 > fdcore.W - 9 or y1 > fdcore.H - 9:
                    continue
                if val < 0.18 or (sat < 0.08 and val > 0.9):                 # shadows, paper-white borders, white clouds
                    continue
                if any(not (x1 < bx0 or x0 > bx1 or y1 < by0 or y0 > by1) for bx0, by0, bx1, by1 in boxes):
                    continue
                hs = [colorsys.rgb_to_hsv(*(v / 255.0 for v in rows[py][px * 3:px * 3 + 3])) for px, py in pixels[::7]]
                mh, ms, mv = (sum(t[i] for t in hs) / len(hs) for i in range(3))
                if 0.1 <= mh <= 0.2 and mv > 0.75:                         # suns, lamps, yellow glows keep their colour
                    continue
                bright = mv > 0.85                                         # moons, glass, snow, clouds: only if nothing else fits
                circ = circle_of([(x0, y0), (x1, y1)])
                found.append(dict(x=sx, y=sy, cx=circ[0], cy=circ[1], r=circ[2], px=area, fill=area / (w * h), mode=mode, bright=bright))
    found.sort(key=lambda f: (f["bright"], f["mode"] != "hue", -f["fill"] * min(f["px"], 4000)))   # natural, whole, compact first
    chosen = []
    circles = [dict(x=k["x"], y=k["y"], r=k["r"]) for k in kept]
    for f in found:
        if len(chosen) >= want:
            break
        circ = dict(x=f["cx"], y=f["cy"], r=f["r"])
        if all(gap(circ, o) >= MIN_GAP for o in circles):
            circles.append(circ)
            chosen.append(f)
    return name, [[f["x"], f["y"], AUTO_SHIFTS[i % len(AUTO_SHIFTS)], f["mode"], f["cx"], f["cy"], f["r"]]
                  for i, f in enumerate(chosen)], chosen


def select(names=None):
    stats = json.load(open(STATS, encoding="utf-8"))
    order = [n for n in (names or scene_levels()) if n in stats]
    picks, jobs = {}, []
    for name in order:
        units = [u for u in bundles(stats[name]) if all(d["px"] >= MIN_PX for d in u)]
        picks[name] = best_subset(units)
        if len(picks[name]) < MIN_COUNT:
            jobs.append((name, picks[name], max(MIN_COUNT, 4) - len(picks[name])))
    autos = {}
    if jobs:
        with Pool(min(14, os.cpu_count() or 4)) as pool:
            for name, auto, chosen in pool.imap_unordered(_auto, jobs):
                autos[name] = auto
                picks[name] = picks[name] + [dict(id="auto", x=f["cx"], y=f["cy"], r=f["r"], px=f["px"]) for f in chosen]
    selection = json.load(open(SELECTION, encoding="utf-8")) if os.path.exists(SELECTION) else {}
    problems = []
    for name in order:
        st, pick = stats[name], picks[name]
        keep = [d for d in pick if d["id"] != "auto"]
        keep_ids = {d["id"] for d in keep}
        selection[name] = dict(keep=sorted(keep_ids), circles={d["id"]: [d["x"], d["y"], d["r"]] for d in keep},
                               auto=autos.get(name, []),
                               neutral=sorted(e for e, owners in st["carriers"].items() if not keep_ids & set(owners)))
        min_gap = min((gap(a, b) for a, b in itertools.combinations(pick, 2)), default=0)
        bad = not (MIN_COUNT <= len(pick) <= MAX_COUNT)
        problems += [name] if bad else []
        print("%-9s %d diffs (%d recoloured)  min px %5d  min gap %4d  %s%s" % (
            name, len(pick), len(autos.get(name, [])), min((d["px"] for d in pick), default=0), min_gap,
            ",".join(sorted(keep_ids)), "  !!" if bad else ""))
    json.dump(selection, open(SELECTION, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("levels breaking the rules:", problems or "none")


# ------------------------------------------------------------------- checking the result
def verify():
    """Checks the built level assets of the scene list: 3..5 differences, >= MIN_GAP apart (in every orbit view)."""
    import fdcore
    pattern = (r"- id: (\S+)\n\s+center: \{x: ([-\d.]+), y: ([-\d.]+)\}\n\s+radius: ([\d.]+)\n"
               r"\s+viewCenters:[ ]?(\[\]|(?:\n\s+- \{x: [-\d.]+, y: [-\d.]+\})+)")
    bad = 0
    for name in scene_levels():
        text = open(os.path.join(fdcore.LEVEL_DIR, name + ".asset"), encoding="utf-8").read()
        block = text.split("  differences:", 1)[1]
        items = []
        for m in re.finditer(pattern, block):
            views = [(float(a), float(b)) for a, b in re.findall(r"\{x: ([-\d.]+), y: ([-\d.]+)\}", m.group(5))]
            items.append((m.group(1), views or [(float(m.group(2)), float(m.group(3)))], float(m.group(4))))
        gaps = [math.hypot(a[1][v][0] - b[1][v][0], a[1][v][1] - b[1][v][1]) - a[2] - b[2]
                for a, b in itertools.combinations(items, 2) for v in range(min(len(a[1]), len(b[1])))]
        g = min(gaps, default=999)
        ok = MIN_COUNT <= len(items) <= MAX_COUNT and g >= MIN_GAP - 0.5
        bad += not ok
        if not ok or "-v" in sys.argv:
            print("%-9s %d diffs  min gap %4d  %s%s" % (name, len(items), g, " ".join(i[0] for i in items), "" if ok else "  !!"))
    print("levels breaking the rules:", bad)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "select"
    if cmd == "measure":
        measure(sys.argv[2:] or scene_levels())
    elif cmd == "verify":
        verify()
    else:
        select(sys.argv[2:] or None)
