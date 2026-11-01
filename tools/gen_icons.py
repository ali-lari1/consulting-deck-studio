#!/usr/bin/env python3
"""Convert bundled Lucide SVGs (assets/icons/lucide/*.svg) into assets/icons/icons.json.

Each icon becomes a list of sub-paths in a 24x24 box using only absolute M, L, C and Z, which map 1:1 to
DrawingML custGeom (moveTo, lnTo, cubicBezTo, close) and to SVG. Arcs, quadratics, rects, circles,
ellipses, lines, polylines and polygons are all converted. Standard library only.
"""
import glob
import json
import math
import os
import re
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "skills", "consulting-deck-studio", "assets", "icons", "lucide")
OUT = os.path.join(ROOT, "skills", "consulting-deck-studio", "assets", "icons", "icons.json")
NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
TOK = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def arc_to_cubics(x1, y1, rx, ry, phi, fa, fs, x2, y2):
    """SVG elliptical arc -> list of cubic segments (each (c1x,c1y,c2x,c2y,x,y)). W3C F.6 conversion."""
    if rx == 0 or ry == 0 or (x1 == x2 and y1 == y2):
        return [(x1, y1, x2, y2, x2, y2)]
    rx, ry = abs(rx), abs(ry)
    p = math.radians(phi)
    cp, sp = math.cos(p), math.sin(p)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1p ** 2) / rx ** 2 + (y1p ** 2) / ry ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(0, num / den)) * (-1 if fa == fs else 1)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx, cy = cp * cxp - sp * cyp + (x1 + x2) / 2, sp * cxp + cp * cyp + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a

    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(1, int(math.ceil(abs(dt) / (math.pi / 2) - 1e-9)))
    d = dt / n
    k = 4 / 3 * math.tan(d / 4)
    out = []
    t = t1
    for _ in range(n):
        c1, s1, c2, s2 = math.cos(t), math.sin(t), math.cos(t + d), math.sin(t + d)
        e1 = (rx * (c1 - k * s1), ry * (s1 + k * c1))
        e2 = (rx * (c2 + k * s2), ry * (s2 - k * c2))
        e3 = (rx * c2, ry * s2)
        pts = [(cx + cp * a - sp * b, cy + sp * a + cp * b) for a, b in (e1, e2, e3)]
        out.append((pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1]))
        t += d
    return out


def parse_d(d):
    pos = 0
    cmd = None
    x = y = sx = sy = 0.0
    last_c = last_q = None
    paths, cur = [], []
    sep = re.compile(r"[\s,]*")

    def skip():
        nonlocal pos
        pos = sep.match(d, pos).end()

    def num():
        nonlocal pos
        skip()
        m = NUM.match(d, pos)
        pos = m.end()
        return float(m.group(0))

    def flag():  # arc flags are single 0/1 characters and may be packed ("011.5")
        nonlocal pos
        skip()
        ch = d[pos]
        pos += 1
        return int(ch)

    def nums(k):
        return [num() for _ in range(k)]

    while True:
        skip()
        if pos >= len(d):
            break
        if d[pos].isalpha():
            cmd = d[pos]
            pos += 1
        rel = cmd.islower()
        c = cmd.upper()
        if c == "Z":
            cur.append(["Z"])
            x, y = sx, sy
            last_c = last_q = None
            continue
        if c == "M":
            a, b = nums(2)
            if rel:
                a, b = a + x, b + y
            if cur:
                paths.append(cur)
            cur = [["M", a, b]]
            x, y, sx, sy = a, b, a, b
            cmd = "l" if rel else "L"
            last_c = last_q = None
        elif c in "LHV":
            if c == "L":
                a, b = nums(2)
                if rel:
                    a, b = a + x, b + y
            elif c == "H":
                a, = nums(1)
                a, b = (a + x if rel else a), y
            else:
                b, = nums(1)
                a, b = x, (b + y if rel else b)
            cur.append(["L", a, b])
            x, y = a, b
            last_c = last_q = None
        elif c in "CS":
            if c == "C":
                v = nums(6)
                if rel:
                    v = [v[0] + x, v[1] + y, v[2] + x, v[3] + y, v[4] + x, v[5] + y]
            else:
                v4 = nums(4)
                if rel:
                    v4 = [v4[0] + x, v4[1] + y, v4[2] + x, v4[3] + y]
                c1 = (2 * x - last_c[0], 2 * y - last_c[1]) if last_c else (x, y)
                v = [c1[0], c1[1]] + v4
            cur.append(["C"] + v)
            last_c = (v[2], v[3])
            last_q = None
            x, y = v[4], v[5]
        elif c in "QT":
            if c == "Q":
                q = nums(4)
                if rel:
                    q = [q[0] + x, q[1] + y, q[2] + x, q[3] + y]
            else:
                e = nums(2)
                if rel:
                    e = [e[0] + x, e[1] + y]
                qc = (2 * x - last_q[0], 2 * y - last_q[1]) if last_q else (x, y)
                q = [qc[0], qc[1]] + e
            qx, qy, ex, ey = q
            cur.append(["C", x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y), ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey), ex, ey])
            last_q = (qx, qy)
            last_c = None
            x, y = ex, ey
        elif c == "A":
            rx, ry, phi = nums(3)
            fa, fs = flag(), flag()
            a, b = nums(2)
            if rel:
                a, b = a + x, b + y
            for seg in arc_to_cubics(x, y, rx, ry, phi, int(fa), int(fs), a, b):
                cur.append(["C"] + list(seg))
            x, y = a, b
            last_c = last_q = None
    if cur:
        paths.append(cur)
    return paths


def f(el, k, default=0.0):
    v = el.get(k)
    return float(v) if v not in (None, "") else default


def element_paths(el):
    tag = el.tag.split("}")[-1]
    if tag == "path":
        return parse_d(el.get("d", ""))
    if tag == "line":
        return [[["M", f(el, "x1"), f(el, "y1")], ["L", f(el, "x2"), f(el, "y2")]]]
    if tag in ("polyline", "polygon"):
        pts = [float(n) for n in NUM.findall(el.get("points", ""))]
        p = [["M", pts[0], pts[1]]] + [["L", pts[j], pts[j + 1]] for j in range(2, len(pts), 2)]
        return [p + ([["Z"]] if tag == "polygon" else [])]
    if tag == "rect":
        x, y, w, h = f(el, "x"), f(el, "y"), f(el, "width"), f(el, "height")
        rx = f(el, "rx", f(el, "ry", 0))
        ry = f(el, "ry", rx)
        if not rx:
            return [[["M", x, y], ["L", x + w, y], ["L", x + w, y + h], ["L", x, y + h], ["Z"]]]
        d = "M%s %sH%sA%s %s 0 0 1 %s %sV%sA%s %s 0 0 1 %s %sH%sA%s %s 0 0 1 %s %sV%sA%s %s 0 0 1 %s %sZ" % (
            x + rx, y, x + w - rx, rx, ry, x + w, y + ry, y + h - ry, rx, ry, x + w - rx, y + h, x + rx, rx, ry, x,
            y + h - ry, y + ry, rx, ry, x + rx, y)
        return parse_d(d)
    if tag in ("circle", "ellipse"):
        cx, cy = f(el, "cx"), f(el, "cy")
        rx = f(el, "r") if tag == "circle" else f(el, "rx")
        ry = f(el, "r") if tag == "circle" else f(el, "ry")
        d = "M%s %sA%s %s 0 0 1 %s %sA%s %s 0 0 1 %s %sZ" % (cx - rx, cy, rx, ry, cx + rx, cy, rx, ry, cx - rx, cy)
        return parse_d(d)
    return []


def main():
    icons = {}
    for p in sorted(glob.glob(os.path.join(SRC, "*.svg"))):
        root = ET.parse(p).getroot()
        subs = []
        for el in root.iter():
            subs += element_paths(el)
        icons[os.path.splitext(os.path.basename(p))[0]] = [
            [[c[0]] + [round(v, 3) for v in c[1:]] for c in sp] for sp in subs]
    json.dump({"source": "lucide-static 1.59.0 (ISC)", "box": 24, "stroke": 2, "icons": icons},
              open(OUT, "w"), separators=(",", ":"))
    print("%d icons -> %s" % (len(icons), OUT))


if __name__ == "__main__":
    main()
