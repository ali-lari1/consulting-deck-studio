"""More consulting layouts: logic trees, process, roadmap, timeline, org chart, RACI, S-curve/EVM, P-curve (QRA),
benefits tracker, stage gates, Marimekko, key numbers, quotes, before/after, benchmark, RAID log.
Field reference: references/layouts.md."""
import datetime

from . import components as C
from . import scene as S
from .components import G, T, r
from .deckmd import md_runs
from .layouts import _value_axis, chrome, default_side, fmt, layout, side_panels, table
from .layouts_pmo import MON, _date, _months_between


def _right(slide):
    return G.main_r if default_side(slide) else G.R


def _finish(els, slide, bottom):
    side = default_side(slide)
    if side:
        els += side_panels(bottom, side)
    return els


def _lerp_color(v):
    return T["G"] if v >= 0.95 else T["A"] if v >= 0.9 else T["R"]


# --------------------------------------------------------------------------- trees

def _tree(slide, ctx, driver):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = _right(slide)
    root = d["root"]
    nodes = []  # (depth, node, parent_index)

    def walk(n, depth, parent):
        idx = len(nodes)
        nodes.append([depth, n, parent, 0.0, 0.0])
        for c in n.get("children", []):
            walk(c, depth + 1, idx)
    walk(root, 0, None)
    depth = max(n[0] for n in nodes)
    leaves = [i for i, n in enumerate(nodes) if not n[1].get("children")]
    top = G.top + (24 if d.get("legend") else 0)
    avail = bottom - top
    lh = avail / len(leaves)
    if lh < (34 if driver else 26):
        raise S.LayoutError("tree has %d leaves; at most %d fit. Group branches or split the slide" % (
            len(leaves), int(avail / (34 if driver else 26))))
    gap = 26.0
    colw = (right - G.L - gap * depth) / (depth + 1)
    for k, i in enumerate(leaves):
        nodes[i][4] = top + lh * (k + 0.5)
    for i in range(len(nodes) - 1, -1, -1):
        kids = [j for j, n in enumerate(nodes) if n[2] == i]
        if kids:
            nodes[i][4] = (nodes[kids[0]][4] + nodes[kids[-1]][4]) / 2
    bh = min(lh - 6, 46.0 if driver else 36.0)
    for i, (dep, n, parent, _, cy) in enumerate(nodes):
        x = G.L + dep * (colw + gap)
        y = cy - bh / 2
        is_root = dep == 0
        fill = T["navy"] if is_root else (T["sky"] if n.get("highlight") else T["white"])
        line = None if is_root else (T["navy"] if n.get("highlight") else T["rule"])
        els.append(S.rect(x, y, colw, bh, fill=fill, line=line, lw=0.75))
        col = T["white"] if is_root else T["ink"]
        tx, tw = x + 8, colw - 16
        if n.get("rag"):
            els.append(C.rag_dot(x + 10, cy, n["rag"], 8))
            tx, tw = x + 20, colw - 28
        if driver:
            runs = [r(n["label"], 9, False, T["white"] if is_root else T["grey"])]
            val = n.get("value", "")
            runs.append(r("\n" + val, 13, True, col))
            if n.get("delta"):
                dc = T["white"] if is_root else (T["R"] if n.get("delta_bad") else T["G"])
                runs.append(r("  " + n["delta"], 9, True, dc))
            els.append(S.text(tx, y, tw, runs, lh=1.15, va="m", h=bh, max_lines=3))
        else:
            els.append(S.text(tx, y, tw, md_runs(n["text"], 10 if not is_root else 11, col, bold=is_root), lh=1.2,
                              va="m", h=bh, max_lines=3))
        if parent is not None:
            px = G.L + nodes[parent][0] * (colw + gap) + colw
            py = nodes[parent][4]
            mx = px + gap / 2
            els += [S.line(px, py, mx, py, T["mid"], 0.75), S.line(mx, py, mx, cy, T["mid"], 0.75),
                    S.line(mx, cy, x, cy, T["mid"], 0.75)]
        if driver and n.get("op") and parent is not None:
            pass
    if d.get("legend"):
        els += C.legend(G.L, G.top, [(k, c, l) for k, c, l in d["legend"]])
    return _finish(els, slide, bottom)


@layout("issue-tree")
def issue_tree(slide, ctx):
    """MECE issue or hypothesis tree, left to right. Leaves may carry rag (e.g. hypothesis status)."""
    return _tree(slide, ctx, driver=False)


@layout("driver-tree")
def driver_tree(slide, ctx):
    """Value driver tree: each node has label, value and optional delta."""
    return _tree(slide, ctx, driver=True)


# --------------------------------------------------------------------------- process and time

@layout("process-flow")
def process_flow(slide, ctx):
    """Chevron steps with detail underneath; optional owner/duration rows."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    steps = d["steps"]
    right = _right(slide)
    els += C.chevrons(G.L, G.top, right - G.L, 34, [s["title"] for s in steps], d.get("active"))
    n = len(steps)
    w = (right - G.L - 10 * (n - 1)) / n
    extra = [k for k in ("owner", "duration") if any(k in s for s in steps)]
    y0 = G.top + 46
    lim = bottom - len(extra) * 30
    low = y0
    for i, st in enumerate(steps):
        x = G.L + i * (w + 10)
        items = st.get("bullets") or ([st["text"]] if st.get("text") else [])
        b = C.bullets(x, y0, w, [(md_runs(t, 10), 1) if isinstance(t, str) else (md_runs(t[0], 10), t[1]) for t in items], size=10)
        if b["y"] + b["h"] > lim:
            raise S.LayoutError("step '%s' text overflows by %.0f pt" % (st["title"], b["y"] + b["h"] - lim))
        els.append(b)
        low = max(low, b["y"] + b["h"])
    y = low + 20
    for k in extra:
        for i, st in enumerate(steps):
            x = G.L + i * (w + 10)
            els.append(S.hline(x, y, x + w, T["rule"], 0.5))
            els.append(S.text(x, y + 4, w, [r(k.capitalize() + ": ", 9, True, T["grey"]), r(str(st.get(k, "")), 9)], max_lines=2))
        y += 30
    return _finish(els, slide, bottom)


@layout("roadmap")
def roadmap(slide, ctx):
    """Phased roadmap: lanes x periods with bars and milestones. Item start/end are period indices (0-based,
    fractions allowed; end is exclusive)."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = _right(slide)
    periods, lanes = d["periods"], d["lanes"]
    lab_w = d.get("label_width", 130)
    x0 = G.L + lab_w
    pw = (right - x0) / len(periods)
    y = G.top
    for i, p in enumerate(periods):
        els.append(S.rect(x0 + i * pw, y, pw - 1, 18, fill=T["navy"] if d.get("phases") is None else T["tint"]))
        els.append(S.text(x0 + i * pw, y + 4, pw, r(p, 8.5, True, T["white"] if d.get("phases") is None else T["grey"]),
                          align="c", max_lines=1))
    y += 22
    if d.get("phases"):
        for ph in d["phases"]:
            xa, xb = x0 + ph["start"] * pw, x0 + ph["end"] * pw
            els.append(S.poly([(xa, y), (xb - 8, y), (xb, y + 9), (xb - 8, y + 18), (xa, y + 18)], fill=T["navy"]))
            els.append(S.text(xa + 6, y + 4, xb - xa - 16, r(ph["name"], 8.5, True, T["white"]), max_lines=1))
        y += 24
    lane_h = min(64.0, (bottom - y - 24) / len(lanes))
    for li, ln in enumerate(lanes):
        ly = y + li * lane_h
        els.append(S.text(G.L, ly, lab_w - 10, r(ln["name"], 10, True, T["navy"]), va="m", h=lane_h, lh=1.15, max_lines=3))
        els.append(S.hline(G.L, ly + lane_h, right, T["rule"], 0.5))
        bars = [it for it in ln["items"] if it.get("type", "bar") == "bar"]
        bh = min(16.0, (lane_h - 8) / max(1, len(bars)))
        k = 0
        for it in ln["items"]:
            if it.get("type") == "milestone":
                mx = x0 + it["at"] * pw
                els.append(C.diamond(mx, ly + lane_h - 10, 9, T["R"] if it.get("rag") == "R" else T["navy"]))
                els.append(S.text(mx + 7, ly + lane_h - 16, 150, r(it["label"], 8, True), max_lines=1))
                continue
            bx, bw = x0 + it["start"] * pw + 1, (it["end"] - it["start"]) * pw - 2
            by = ly + 4 + k * bh
            k += 1
            col = T["navy"] if it.get("highlight", True) else T["navy_l"]
            els.append(S.rect(bx, by, bw, bh - 2, fill=col))
            if it.get("rag"):
                els.append(C.rag_dot(bx + 7, by + (bh - 2) / 2, it["rag"], 6))
            lw_ = S.line_width([r(it["label"], 8)])
            inside = lw_ + (18 if it.get("rag") else 8) < bw
            els.append(S.text(bx + (14 if it.get("rag") else 4) if inside else bx + bw + 4, by + (bh - 2 - 10) / 2 + 0.5,
                              max(bw, 160), r(it["label"], 8, False, T["white"] if inside else T["ink"]), max_lines=1))
    for i in range(1, len(periods)):
        els.append(S.line(x0 + i * pw, G.top + 18, x0 + i * pw, y + len(lanes) * lane_h, T["rule"], 0.4, dash="dot"))
    if d.get("today") is not None:
        tx = x0 + d["today"] * pw
        els.append(S.line(tx, G.top + 18, tx, y + len(lanes) * lane_h + 4, T["R"], 1, dash="dash"))
        els.append(S.text(tx + 3, y + len(lanes) * lane_h + 2, 60, r("Today", 7.5, True, T["R"])))
    return _finish(els, slide, bottom)


@layout("timeline")
def timeline(slide, ctx):
    """Milestones on a horizontal time axis, labels alternating above and below. done = filled marker."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = _right(slide)
    start = _date(d["start"]).replace(day=1)
    end = _date(d["end"])
    nm = max(1.0, _months_between(start, end))
    x0, x1 = G.L + 10, right - 10
    ay = (G.top + bottom) / 2

    def X(s):
        return x0 + _months_between(start, _date(s)) / nm * (x1 - x0)
    els.append(S.line(x0, ay, x1, ay, T["navy"], 2))
    m = start
    while m <= end:
        mx = X(m.isoformat())
        els.append(S.line(mx, ay - 4, mx, ay + 4, T["navy"], 1))
        if int(nm) <= 18 or m.month in (1, 4, 7, 10):
            els.append(S.text(mx - 20, ay + 7, 40, r(MON[m.month - 1] + ("\n%d" % m.year if m.month == 1 or m == start else ""),
                                                    7.5, False, T["grey"]), align="c", lh=1.15))
        m = datetime.date(m.year + m.month // 12, m.month % 12 + 1, 1)
    evs = sorted(d["events"], key=lambda e: e["date"])
    lane_up, lane_dn = [], []
    for k, ev in enumerate(evs):
        ex = X(ev["date"])
        up = k % 2 == 0
        lanes = lane_up if up else lane_dn
        level = 0
        while any(abs(ex - px) < 150 and lv == level for px, lv in lanes):
            level += 1
        lanes.append((ex, level))
        stem = 34 + level * 46
        ty = ay - stem if up else ay + stem
        els.append(S.line(ex, ay, ex, ty, T["mid"], 0.75))
        done = ev.get("done")
        els.append(S.rect(ex - 5, ay - 5, 10, 10, fill=T["navy"] if done else T["white"], line=T["navy"], lw=1.25, shape="ellipse"))
        if ev.get("rag"):
            els.append(C.rag_dot(ex, ay, ev["rag"], 6))
        dd = _date(ev["date"])
        runs = [r("%d %s %d\n" % (dd.day, MON[dd.month - 1], dd.year), 8, True, T["grey"]), r(ev["label"], 9.5, True, T["navy"])]
        if ev.get("detail"):
            runs.append(r("\n" + ev["detail"], 8.5))
        flip = ex + 144 > right
        t = S.text(ex - 144 if flip else ex + 4, 0, 140, runs, lh=1.2, max_lines=5, align="r" if flip else "l")
        t["y"] = ty - t["h"] if up else ty
        if t["y"] < G.top or t["y"] + t["h"] > bottom:
            raise S.LayoutError("timeline labels overflow; use fewer events or shorter labels")
        els.append(t)
    els += C.legend(G.L, bottom - 12, [("dot", T["navy"], "Complete"), ("outline", T["navy"], "Planned")])
    return _finish(els, slide, bottom)


@layout("org-chart")
def org_chart(slide, ctx):
    """Top-down governance or organisation chart. nodes: [{id, title, name?, parent?, note?, highlight?}]."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = _right(slide)
    nodes = {n["id"]: dict(n, kids=[]) for n in d["nodes"]}
    roots = []
    for n in d["nodes"]:
        (nodes[n["parent"]]["kids"] if n.get("parent") else roots).append(n["id"])

    def leaves(i):
        k = nodes[i]["kids"]
        return 1 if not k else sum(leaves(c) for c in k)

    def depth(i):
        k = nodes[i]["kids"]
        return 1 if not k else 1 + max(depth(c) for c in k)
    total = sum(leaves(r_) for r_ in roots)
    levels = max(depth(r_) for r_ in roots)
    slot = (right - G.L) / total
    bw = min(150.0, slot - 10)
    lvl_h = (bottom - G.top) / levels
    bh = min(48.0, lvl_h - 22)
    if bw < 70:
        raise S.LayoutError("org chart too wide (%d boxes in the bottom row); group roles" % total)

    def place(i, x0, lv):
        n = nodes[i]
        span = leaves(i) * slot
        cx = x0 + span / 2
        y = G.top + lv * lvl_h
        n["cx"], n["y"] = cx, y
        xx = x0
        for c in n["kids"]:
            place(c, xx, lv + 1)
            xx += leaves(c) * slot
    xx = G.L
    for r_ in roots:
        place(r_, xx, 0)
        xx += leaves(r_) * slot
    for i, n in nodes.items():
        hl = n.get("highlight")
        lvl0 = not n.get("parent")
        els.append(S.rect(n["cx"] - bw / 2, n["y"], bw, bh, fill=T["navy"] if lvl0 else (T["sky"] if hl else T["white"]),
                          line=None if lvl0 else T["navy"] if hl else T["rule"], lw=0.75))
        col = T["white"] if lvl0 else T["ink"]
        runs = [r(n["title"], 9.5, True, T["white"] if lvl0 else T["navy"])]
        if n.get("name"):
            runs.append(r("\n" + n["name"], 8.5, False, col))
        els.append(S.text(n["cx"] - bw / 2 + 5, n["y"], bw - 10, runs, align="c", va="m", h=bh, lh=1.15, max_lines=3))
        if n.get("note"):
            els.append(S.text(n["cx"] - bw / 2, n["y"] + bh + 2, bw, r(n["note"], 7.5, color=T["grey"]), align="c", max_lines=2))
        if n["kids"]:
            ys = n["y"] + bh
            ym = ys + (lvl_h - bh) / 2
            els.append(S.line(n["cx"], ys, n["cx"], ym, T["mid"], 0.75))
            xs = [nodes[c]["cx"] for c in n["kids"]]
            if len(xs) > 1:
                els.append(S.line(min(xs), ym, max(xs), ym, T["mid"], 0.75))
            for c in n["kids"]:
                els.append(S.line(nodes[c]["cx"], ym, nodes[c]["cx"], nodes[c]["y"], T["mid"], 0.75))
    return _finish(els, slide, bottom)


@layout("raci")
def raci(slide, ctx):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    roles = d["roles"]
    cols = [{"name": d.get("activity_header", "Activity or decision"), "width": 0.36, "kind": "bold"}] + \
           [{"name": ro, "width": 0.64 / len(roles), "align": "c"} for ro in roles]
    rows = [[a["name"]] + ["**%s**" % c if c in ("A", "R") else c for c in a["cells"]] for a in d["activities"]]
    for a in d["activities"]:
        if list(a["cells"]).count("A") != 1:
            raise S.LayoutError("'%s' needs exactly one A (accountable); has %d" % (a["name"], list(a["cells"]).count("A")))
    t, yy = table(G.L, G.top, G.R - G.L, cols, rows, size=10, bottom=bottom - 16)
    els += t
    els.append(S.text(G.L, yy + 8, 800, [r("R ", 8.5, True), r("Responsible   ", 8.5, color=T["grey"]), r("A ", 8.5, True),
                                          r("Accountable (one per row)   ", 8.5, color=T["grey"]), r("C ", 8.5, True),
                                          r("Consulted   ", 8.5, color=T["grey"]), r("I ", 8.5, True),
                                          r("Informed", 8.5, color=T["grey"])]))
    return els


# --------------------------------------------------------------------------- capital project controls

@layout("s-curve")
def s_curve(slide, ctx):
    """Cumulative planned value, earned value and actual cost; SPI and CPI computed from the data."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = G.main_r
    hdr, y = C.exhibit_header(G.L, G.top, right - G.L, d.get("exhibit", "Earned value, cumulative"), d.get("unit"))
    els += hdr
    xs = d["x"]
    pv, ev, ac = d["planned"], d.get("earned", []), d.get("actual", [])
    pre, suf, dp = d.get("prefix", ""), d.get("suffix", ""), d.get("decimals")
    allv = [v for v in pv + ev + ac if v is not None] + ([d["bac"]] if d.get("bac") else [])
    x0, x1 = G.L + 50, right - 90
    base, top = bottom - 26, y + 10
    lo, hi, sc = _value_axis(els, x0, top, base, 0, max(allv), lambda t_: fmt(t_, dp, pre, suf), x1)
    step = (x1 - x0) / max(1, len(xs) - 1)
    for i, lab in enumerate(xs):
        if len(xs) <= 14 or i % 2 == 0:
            els.append(S.text(x0 + i * step - 30, base + 5, 60, r(str(lab), 8, color=T["grey"]), align="c"))
    series = [("Planned value", pv, T["mid"], "dash"), ("Earned value", ev, T["navy"], None), ("Actual cost", ac, T["R"], None)]
    ends = []
    for name, vals, col, dash in series:
        pts = [(x0 + i * step, base - (v - lo) * sc) for i, v in enumerate(vals) if v is not None]
        for a, b in zip(pts, pts[1:]):
            els.append(S.line(a[0], a[1], b[0], b[1], col, 1.75 if not dash else 1.25, dash=dash))
        if pts:
            ends.append([pts[-1][1], name, col, pts[-1][0]])
    ends.sort()
    for k in range(1, len(ends)):
        if ends[k][0] - ends[k - 1][0] < 14:
            ends[k][0] = ends[k - 1][0] + 14
    for yy, name, col, ex in ends:
        els.append(S.text(max(ex, x1) + 6 if ex >= x1 - 1 else ex + 6, yy - 6, 90, r(name, 8.5, True, col), max_lines=1))
    if d.get("bac"):
        by = base - (d["bac"] - lo) * sc
        els.append(S.line(x0, by, x1, by, T["grey"], 0.75, dash="dot"))
        els.append(S.text(x0 + 4, by - 13, 200, r("Budget at completion %s" % fmt(d["bac"], dp, pre, suf), 8, color=T["grey"])))
    # computed indices at the last period with earned and actual values
    k = min(len([v for v in ev if v is not None]), len([v for v in ac if v is not None])) - 1
    side_y = G.top
    if k >= 0 and pv[k]:
        spi, cpi = ev[k] / pv[k], ev[k] / ac[k]
        sv, cv = ev[k] - pv[k], ev[k] - ac[k]
        hdr2, iy = C.header_box(G.side_x, side_y, G.R - G.side_x, 0, "Performance at %s" % xs[k])
        els += hdr2
        rows = [("SPI", "%.2f" % spi, _lerp_color(spi), "Schedule variance %s" % fmt(sv, dp, pre, suf)),
                ("CPI", "%.2f" % cpi, _lerp_color(cpi), "Cost variance %s" % fmt(cv, dp, pre, suf))]
        if d.get("bac"):
            eac = d["bac"] / cpi
            rows.append(("EAC", fmt(eac, dp, pre, suf), _lerp_color(d["bac"] / eac), "BAC / CPI; %s over budget" % fmt(eac - d["bac"], dp, pre, suf)
                         if eac > d["bac"] else "BAC / CPI"))
        for lab, val, col, note in rows:
            els.append(S.text(G.side_x, iy, 60, r(lab, 9, True, T["grey"])))
            els.append(S.text(G.side_x, iy + 12, 160, r(val, 22, True, T["navy"])))
            els.append(S.rect(G.side_x + S.line_width([r(val, 22, True)]) + 8, iy + 21, 9, 9, fill=col, shape="ellipse"))
            els.append(S.text(G.side_x, iy + 40, G.R - G.side_x, r(note, 8.5, color=T["grey"])))
            iy += 62
        side_y = iy + 6
        els.append(S.text(G.side_x, side_y, G.R - G.side_x, r("Green 0.95 or more; amber 0.90-0.95; red below 0.90. "
                                                               "Indices computed from the data shown.", 7.5, color=T["grey"]), lh=1.25))
        side_y += 34
    if d.get("takeaways"):
        els += side_panels(bottom, [(d.get("takeaways_title", "What this shows"), "numbered", d["takeaways"])], y=side_y)
    return els


@layout("p-curve")
def p_curve(slide, ctx):
    """Quantitative risk analysis: cumulative probability of cost or finish. Give samples (simulation output)
    or points [[value, probability 0-1], ...]. P-values and the budget's confidence level are computed."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = G.main_r if default_side(slide) else G.R
    hdr, y = C.exhibit_header(G.L, G.top, right - G.L, d.get("exhibit", "Cumulative probability of outturn"), d.get("unit"))
    els += hdr
    pre, suf, dp = d.get("prefix", ""), d.get("suffix", ""), d.get("decimals")
    if d.get("samples"):
        xsrt = sorted(d["samples"])
        n = len(xsrt)
        pts = [(v, (i + 1) / float(n)) for i, v in enumerate(xsrt)]
    else:
        pts = sorted((p[0], p[1]) for p in d["points"])

    def pval(p):
        for (a, pa), (b, pb) in zip(pts, pts[1:]):
            if pa <= p <= pb:
                return a + (b - a) * ((p - pa) / (pb - pa) if pb > pa else 0)
        return pts[-1][0] if p > pts[-1][1] else pts[0][0]

    def conf(v):
        if v <= pts[0][0]:
            return pts[0][1]
        for (a, pa), (b, pb) in zip(pts, pts[1:]):
            if a <= v <= b:
                return pa + (pb - pa) * ((v - a) / (b - a) if b > a else 0)
        return 1.0
    lo_v, hi_v = pts[0][0], pts[-1][0]
    pad = (hi_v - lo_v) * 0.05
    x0, x1 = G.L + 46, right - 20
    base, top = bottom - 28, y + 14
    from .layouts import nice_ticks
    ticks = nice_ticks(lo_v - pad, hi_v + pad, 6)
    a, b = ticks[0], ticks[-1]

    def X(v):
        return x0 + (v - a) / (b - a) * (x1 - x0)

    def Y(p):
        return base - p * (base - top)
    for p in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        els.append(S.text(x0 - 40, Y(p) - 6, 34, r("%d%%" % (p * 100), 8.5, color=T["grey"]), align="r"))
        els.append(S.hline(x0, Y(p), x1, T["rule"] if p else T["ink"], 0.4 if p else 0.75))
    for t_ in ticks:
        els.append(S.text(X(t_) - 30, base + 5, 60, r(fmt(t_, dp, pre, suf), 8.5, color=T["grey"]), align="c"))
    step = max(1, len(pts) // 120)
    sp = pts[::step] + ([pts[-1]] if pts[-1] not in pts[::step] else [])
    for (va, pa), (vb, pb) in zip(sp, sp[1:]):
        els.append(S.line(X(va), Y(pa), X(vb), Y(pb), T["navy"], 2))
    marks = d.get("percentiles", [50, 80])
    for k, pc in enumerate(marks):
        v = pval(pc / 100.0)
        els.append(S.line(X(v), Y(pc / 100.0), X(v), base, T["navy"], 0.75, dash="dash"))
        els.append(S.line(x0, Y(pc / 100.0), X(v), Y(pc / 100.0), T["navy"], 0.5, dash="dot"))
        els.append(S.text(X(v) + 4, Y(pc / 100.0) + 4 + k * 0, 120, [r("P%d  " % pc, 9, True, T["navy"]), r(fmt(v, dp, pre, suf), 9, True)]))
    if d.get("budget") is not None:
        bv = d["budget"]
        cb = conf(bv)
        els.append(S.line(X(bv), top, X(bv), base, T["R"], 1.25))
        els.append(S.text(X(bv) - 124, top, 120, [r("%s\n" % d.get("budget_label", "Budget"), 8.5, True, T["R"]),
                                                  r("%s  =  P%d" % (fmt(bv, dp, pre, suf), round(cb * 100)), 8.5, True, T["R"])],
                          align="r", lh=1.2))
    return _finish(els, slide, bottom)


@layout("benefits-tracker")
def benefits_tracker(slide, ctx):
    """Benefits: baseline, target, actual, progress bar (computed), status and due date."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    cols = [{"name": "Benefit", "width": 0.26, "kind": "bold"}, {"name": "Owner", "width": 0.11},
            {"name": "Baseline", "width": 0.09, "kind": "number"}, {"name": "Target", "width": 0.09, "kind": "number"},
            {"name": "Actual", "width": 0.09, "kind": "number"}, {"name": "Progress to target", "width": 0.20, "kind": "progress"},
            {"name": "Status", "width": 0.07, "kind": "rag"}, {"name": "Due", "width": 0.09}]
    rows = []
    for b in d["benefits"]:
        u, dp = b.get("unit", ""), b.get("decimals")
        prog = (b["actual"] - b["baseline"]) / float(b["target"] - b["baseline"]) if b["target"] != b["baseline"] else 0
        rows.append([b["name"], b.get("owner", ""), fmt(b["baseline"], dp) + u, fmt(b["target"], dp) + u,
                     fmt(b["actual"], dp) + u, prog, b.get("rag", ""), b.get("due", "")])
    t, yy = table(G.L, G.top, G.R - G.L, cols, rows, size=9.5, bottom=bottom - 16, min_h=26)
    els += t
    els += C.legend(G.L, yy + 8, [("bar", T["navy"], "Achieved"), ("bar", T["tint"], "Remaining to target"),
                                  ("dot", "G", "On track"), ("dot", "A", "At risk"), ("dot", "R", "Off track")])
    return els


@layout("stage-gate")
def stage_gate(slide, ctx):
    """Gate path: done / current / future gates with dates, decision and criteria under each."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    gates = d["gates"]
    n = len(gates)
    w = (G.R - G.L) / n
    ly = G.top + 26
    els.append(S.line(G.L + w / 2, ly, G.R - w / 2, ly, T["mid"], 2))
    for i, g in enumerate(gates):
        cx = G.L + i * w + w / 2
        st = g.get("status", "future")
        if i < n - 1 and st == "done":
            els.append(S.line(cx, ly, cx + w, ly, T["navy"], 3))
        fill = T["navy"] if st == "done" else T["white"]
        els.append(C.diamond(cx, ly, 22, fill if st != "current" else T["A"]))
        if st == "future":
            els.append(S.poly([(cx, ly - 11), (cx + 11, ly), (cx, ly + 11), (cx - 11, ly)], fill=T["white"], line=T["navy"], lw=1.25))
        els.append(S.text(cx - w / 2 + 6, G.top - 4, w - 12, r(g.get("label", "Gate %d" % i), 8.5, True, T["grey"]), align="c", max_lines=1))
        y = ly + 20
        els.append(S.text(G.L + i * w + 6, y, w - 12, r(g["name"], 10.5, True, T["navy"]), align="c", lh=1.15, max_lines=2))
        y += 30
        meta = [r(g.get("date", ""), 9, True)] + ([r("\n" + g["decision"], 9, color=T["grey"])] if g.get("decision") else [])
        t = S.text(G.L + i * w + 6, y, w - 12, meta, align="c", lh=1.2, max_lines=3)
        els.append(t)
        y += t["h"] + 8
        if g.get("criteria"):
            els.append(S.hline(G.L + i * w + 8, y, G.L + (i + 1) * w - 8, T["rule"], 0.5))
            b = C.bullets(G.L + i * w + 8, y + 4, w - 16, [(md_runs(c, 9), 1) for c in g["criteria"]], size=9, gap=3)
            if b["y"] + b["h"] > bottom:
                raise S.LayoutError("gate '%s' criteria overflow" % g["name"])
            els.append(b)
    els += C.legend(G.L, bottom - 12, [("diamond", T["navy"], "Passed"), ("diamond", T["A"], "Current gate"),
                                       ("diamond", T["mid"], "Future")])
    return els


# --------------------------------------------------------------------------- analysis

@layout("marimekko")
def marimekko(slide, ctx):
    """Variable-width 100% stacked columns (e.g. market by segment and player). Shares computed from values."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = _right(slide)
    hdr, y = C.exhibit_header(G.L, G.top, right - G.L, d.get("exhibit", ""), d.get("unit"))
    els += hdr
    cols = d["columns"]
    tot_w = sum(c["width_value"] for c in cols)
    x0, x1 = G.L + 34, right - 4
    top, base = y + 18, bottom - 34
    seg_names = []
    for c in cols:
        for sgm in c["segments"]:
            if sgm["label"] not in seg_names:
                seg_names.append(sgm["label"])
    pal = [T["navy"], T["blue"], T["navy_l"], T["mid"], T["sky"], T["tint"]]
    hl = d.get("highlight")
    x = x0
    for p in (0, 25, 50, 75, 100):
        els.append(S.text(G.L, base - p / 100.0 * (base - top) - 6, 28, r("%d%%" % p, 8, color=T["grey"]), align="r"))
    for c in cols:
        w = (x1 - x0) * c["width_value"] / tot_w
        csum = float(sum(sg["value"] for sg in c["segments"]))
        yy = base
        for sgm in c["segments"]:
            h = (base - top) * sgm["value"] / csum
            k = seg_names.index(sgm["label"])
            col = pal[k % len(pal)] if hl is None else (T["navy"] if sgm["label"] == hl else T["tint"] if k % 2 else T["sky"])
            els.append(S.rect(x, yy - h, w - 2, h, fill=col, line=T["white"], lw=0.75))
            dark = col in (T["navy"], T["blue"])
            if h > 14 and w > 34:
                els.append(S.text(x + 2, yy - h, w - 6, r("%d%%" % round(sgm["value"] / csum * 100), 8, True,
                                                          T["white"] if dark else T["ink"]), align="c", va="m", h=h, max_lines=1))
            yy -= h
        els.append(S.text(x, base + 4, w - 2, [r(c["label"] + "\n", 8.5, True), r(c.get("width_label", ""), 8, color=T["grey"])],
                          align="c", lh=1.15, max_lines=3))
        x += w
    els += C.legend(G.L, top - 18, [("bar", pal[k % len(pal)] if hl is None else (T["navy"] if s_ == hl else T["sky"]), s_)
                                   for k, s_ in enumerate(seg_names)])
    return _finish(els, slide, bottom)


@layout("key-numbers")
def key_numbers(slide, ctx):
    """2-6 headline figures, each with a label and a one-line explanation."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    nums = d["numbers"]
    per_row = 3 if len(nums) in (3, 5, 6) else 2 if len(nums) == 4 else len(nums)
    rows = (len(nums) + per_row - 1) // per_row
    cw = (G.R - G.L) / per_row
    rh = min(150.0, (bottom - G.top) / rows)
    for i, nb in enumerate(nums):
        x = G.L + (i % per_row) * cw
        y = G.top + (i // per_row) * rh
        if i % per_row:
            els.append(S.line(x - 8, y + 8, x - 8, y + rh - 16, T["rule"], 0.75))
        els.append(S.text(x + 8, y + 8, cw - 30, r(nb["value"], 34, True, T["navy"]), max_lines=1))
        if nb.get("rag"):
            els.append(C.rag_dot(x + 8 + S.line_width([r(nb["value"], 34, True)]) + 10, y + 26, nb["rag"], 11))
        els.append(S.text(x + 8, y + 54, cw - 30, r(nb["label"], 11, True), lh=1.2, max_lines=2))
        if nb.get("note"):
            els.append(S.text(x + 8, y + 86, cw - 30, md_runs(nb["note"], 9.5, T["grey"]), lh=1.25, max_lines=3))
    return els


@layout("quotes")
def quotes(slide, ctx):
    """Stakeholder or interview quotes, optionally grouped by theme. Quotes must be real and attributed by role."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    qs = d["quotes"]
    cols = 2 if len(qs) <= 4 else 3
    rows = (len(qs) + cols - 1) // cols
    gap = 18.0
    cw = (G.R - G.L - gap * (cols - 1)) / cols
    rh = min(170.0, (bottom - G.top - gap * (rows - 1)) / rows)
    for i, q in enumerate(qs):
        x = G.L + (i % cols) * (cw + gap)
        y = G.top + (i // cols) * (rh + gap)
        bar = S.rect(x, y, 3, rh, fill=T["navy"])
        els.append(bar)
        yy = y + 2
        if q.get("theme"):
            els.append(S.text(x + 14, yy, cw - 20, r(q["theme"], 9, True, T["navy"]), max_lines=1))
            yy += 16
        t = S.text(x + 14, yy, cw - 20, r("“" + q["text"] + "”", 11.5, False, T["ink"], italic=False), lh=1.35)
        if t["h"] > rh - 34:
            raise S.LayoutError("quote %d is too long for its box; trim it" % (i + 1))
        els.append(t)
        who = S.text(x + 14, yy + t["h"] + 6, cw - 20, r("– " + q["who"], 9, color=T["grey"]), max_lines=2)
        els.append(who)
        bar["h"] = who["y"] + who["h"] - y + 2
    return els


@layout("before-after")
def before_after(slide, ctx):
    """Current vs future state: rows of dimension | today | target, or two bullet columns."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    lab_w = 150.0 if d.get("rows") else 0
    aw = 40.0
    cw = (G.R - G.L - lab_w - aw) / 2
    xb, xa = G.L + lab_w, G.L + lab_w + cw + aw
    els.append(S.text(xb, G.top, cw, r(d.get("before_title", "Today"), 12, True, T["grey"])))
    els.append(S.text(xa, G.top, cw, r(d.get("after_title", "Target"), 12, True, T["navy"])))
    els.append(S.hline(xb, G.top + 20, xb + cw, T["grey"], 1.5))
    els.append(S.hline(xa, G.top + 20, xa + cw, T["navy"], 1.5))
    y = G.top + 30
    if d.get("rows"):
        even = min(64.0, (bottom - y) / len(d["rows"]))
        for row in d["rows"]:
            tb = S.text(xb, y + 6, cw - 10, md_runs(row["before"], 10.5, T["grey"]), lh=1.3)
            ta = S.text(xa, y + 6, cw - 10, md_runs(row["after"], 10.5), lh=1.3)
            h = max(max(tb["h"], ta["h"], 16) + 14, even)
            pad = (h - max(tb["h"], ta["h"], 16) - 14) / 2
            tb["y"] += pad
            ta["y"] += pad
            els.append(S.text(G.L, y + 6 + pad, lab_w - 10, r(row["dimension"], 10.5, True, T["navy"]), lh=1.2))
            els += [tb, ta]
            ax = xb + cw + 8
            els.append(S.poly([(ax, y + h / 2 - 6), (ax + aw - 26, y + h / 2 - 6), (ax + aw - 26, y + h / 2 - 10),
                               (ax + aw - 16, y + h / 2), (ax + aw - 26, y + h / 2 + 10), (ax + aw - 26, y + h / 2 + 6),
                               (ax, y + h / 2 + 6)], fill=T["sky"]))
            y += h
            els.append(S.hline(G.L, y, G.R, T["rule"], 0.5))
            if y > bottom:
                raise S.LayoutError("before/after rows overflow by %.0f pt" % (y - bottom))
    else:
        bb = C.bullets(xb, y, cw - 10, [(md_runs(t, 11, T["grey"]), 1) for t in d["before"]], size=11)
        ba = C.bullets(xa, y, cw - 10, [(md_runs(t, 11), 1) for t in d["after"]], size=11)
        els += [bb, ba]
        my = y + max(bb["h"], ba["h"]) / 2
        ax = xb + cw + 6
        els.append(S.poly([(ax, my - 10), (ax + aw - 18, my - 10), (ax + aw - 18, my - 16), (ax + aw - 6, my),
                           (ax + aw - 18, my + 16), (ax + aw - 18, my + 10), (ax, my + 10)], fill=T["sky"]))
    return els


@layout("benchmark")
def benchmark(slide, ctx):
    """Ranked peer comparison with the median (computed) and the subject highlighted."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    right = _right(slide)
    hdr, y = C.exhibit_header(G.L, G.top, right - G.L, d.get("exhibit", ""), d.get("unit"))
    els += hdr
    pre, suf, dp = d.get("prefix", ""), d.get("suffix", ""), d.get("decimals")
    items = sorted(d["items"], key=lambda it: it["value"], reverse=d.get("better", "high") == "high")
    vals = sorted(it["value"] for it in items)
    n = len(vals)
    med = (vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2.0)
    lab_w = d.get("label_width", 130)
    x0, x1 = G.L + lab_w, right - 60
    vmax = max(vals)
    sc = (x1 - x0) / vmax
    rh = min(26.0, (bottom - y - 30) / n)
    for i, it in enumerate(items):
        yy = y + 8 + i * rh
        hl = it.get("highlight")
        els.append(S.text(G.L, yy, lab_w - 10, r(it["label"], 9.5, hl, T["navy"] if hl else T["ink"]), align="r", va="m",
                          h=rh - 4, max_lines=1))
        els.append(S.rect(x0, yy + 3, it["value"] * sc, rh - 10, fill=T["navy"] if hl else T["navy_l"]))
        els.append(S.text(x0 + it["value"] * sc + 4, yy, 70, r(fmt(it["value"], dp, pre, suf), 9, hl), va="m", h=rh - 4))
    mx = x0 + med * sc
    els.append(S.line(mx, y + 2, mx, y + 10 + n * rh, T["R"], 1, dash="dash"))
    els.append(S.text(mx + 4, y + 10 + n * rh, 160, r("Median %s" % fmt(med, dp, pre, suf), 8.5, True, T["R"])))
    els.append(S.line(x0, y + 4, x0, y + 8 + n * rh, T["ink"], 0.75))
    return _finish(els, slide, bottom)


@layout("raid-log")
def raid_log(slide, ctx):
    """Risks, assumptions, issues, dependencies (and decisions) in one log, grouped by type."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    order = ["Risk", "Issue", "Assumption", "Dependency", "Decision"]
    items = sorted(d["items"], key=lambda it: (order.index(it["type"]) if it["type"] in order else 9, it.get("id", "")))
    cols = [{"name": "Type", "width": 0.10, "kind": "bold"}, {"name": "ID", "width": 0.06}, {"name": "Description", "width": 0.38},
            {"name": "Owner", "width": 0.12}, {"name": "Due", "width": 0.08}, {"name": "RAG", "width": 0.06, "kind": "rag"},
            {"name": "Status and next action", "width": 0.20}]
    rows = [[it["type"], it.get("id", ""), it["description"], it.get("owner", ""), it.get("due", ""), it.get("rag", ""),
             it.get("status", "")] for it in items]
    t, yy = table(G.L, G.top, G.R - G.L, cols, rows, size=9.5, bottom=bottom - 16)
    els += t
    els += C.legend(G.L, yy + 8, [("dot", "G", "On track"), ("dot", "A", "At risk"), ("dot", "R", "Off track or overdue")])
    return els
