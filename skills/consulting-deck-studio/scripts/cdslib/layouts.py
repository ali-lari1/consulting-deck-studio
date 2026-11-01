"""Consulting slide layouts: data in, scene elements out.

Every layout is a function f(slide, ctx) -> list of elements, registered in LAYOUTS. `slide` is a parsed
deck.md slide (title, data, footnotes, sowhat, source, section); `ctx` holds deck metadata and the page
number. Layouts raise scene.LayoutError when content does not fit, and build.py reports it as a lint error.
The field reference for each layout is in references/layouts.md.
"""
import datetime
import math

from . import components as C
from . import scene as S
from .components import T, r
from .deckmd import md_runs

LAYOUTS = {}
MAIN_X, MAIN_R, SIDE_X, SIDE_R = 36.0, 626.0, 650.0, 924.0
TOP = 104.0


def layout(name):
    def deco(f):
        LAYOUTS[name] = f
        return f
    return deco


# --------------------------------------------------------------------------- helpers

def chrome(slide, ctx, sowhat=True):
    m = ctx["meta"]
    return C.frame(slide["title"], ctx["page"], m.get("tracker"), slide.get("section"), m.get("context"),
                   slide.get("sticker", m.get("sticker")), slide.get("sowhat") if sowhat else None,
                   slide.get("footnotes"), slide.get("source", m.get("source")),
                   confidential=m.get("confidential", "yes") != "no")


def fmt(v, dp=None, prefix="", suffix=""):
    if dp is None:
        dp = 0 if abs(v) >= 100 or float(v).is_integer() else 1
    s = "{:,.{dp}f}".format(abs(v), dp=dp)
    return ("-" if v < 0 else "") + prefix + s + suffix


def nice_ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / float(n)
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if raw <= m * mag)
    a, b = math.floor(lo / step) * step, math.ceil(hi / step) * step
    ticks, v = [], a
    while v <= b + step / 2:
        ticks.append(round(v, 10))
        v += step
    return ticks


def side_panels(ctx_bottom, panels, x=SIDE_X, w=None, y=TOP):
    """Stack right-hand panels. panels: [(title, kind, items)], kind = 'numbered' | 'bullets'."""
    w = w or (SIDE_R - x)
    els = []
    for title, kind, items in panels:
        if not items:
            continue
        if kind == "numbered":
            part, y2 = C.takeaways(x, y, w, [md_runs(t, 10.5) if isinstance(t, str) else t for t in items], title=title)
            els += part
            y = y2 + 14
        else:
            hdr, iy = C.header_box(x, y, w, 0, title)
            b = C.bullets(x, iy, w, [(md_runs(t, 10.5), 1) if isinstance(t, str) else (md_runs(t[0], 10.5), t[1])
                                     for t in items], size=10.5)
            els += hdr + [b]
            y = iy + b["h"] + 16
    if y - 16 > ctx_bottom:
        raise S.LayoutError("side panels need %.0f pt, %.0f available" % (y - 16 - TOP, ctx_bottom - TOP))
    return els


def default_side(slide):
    d = slide["data"]
    panels = []
    if d.get("takeaways"):
        panels.append((d.get("takeaways_title", "What this shows"), "numbered", d["takeaways"]))
    for extra in d.get("panels", []):
        panels.append((extra["title"], "bullets", extra["bullets"]))
    return panels


def rag_color(s):
    return T[s] if s in ("R", "A", "G") else T["mid"]


def trend_color(t, good="up"):
    if t == "flat":
        return T["grey"]
    return T["G"] if t == good else T["R"]


# --------------------------------------------------------------------------- structure

@layout("title")
def title_slide(slide, ctx):
    d, m = slide["data"], ctx["meta"]
    els = [S.rect(0, 0, 960, 6, fill=T["navy"])]
    if m.get("client_logo_text"):
        els.append(S.text(60, 60, 400, r(m["client_logo_text"], 11, True, T["grey"])))
    t = S.text(60, 190, 760, r(slide["title"], 32, True, T["navy"], font=T["title_font"]), lh=1.12, max_lines=3)
    els.append(t)
    y = t["y"] + t["h"] + 14
    if d.get("subtitle"):
        st = S.text(60, y, 760, r(d["subtitle"], 15, color=T["grey"]), lh=1.25, max_lines=2)
        els.append(st)
        y += st["h"]
    els.append(S.hline(60, 430, 900, T["rule"], 0.75))
    bits = [x for x in (d.get("client"), d.get("date"), d.get("prepared_by")) if x]
    els.append(S.text(60, 442, 700, r("   |   ".join(bits), 10, color=T["grey"])))
    stk = slide.get("sticker", m.get("sticker"))
    if stk:
        w = S.line_width([r(stk, 8)]) + 14
        els += [S.rect(900 - w, 40, w, 15, line=T["ink"]), S.text(900 - w, 44, w, r(stk, 8), align="c")]
    if d.get("confidential", True):
        els.append(S.text(60, 500, 600, r(d.get("confidential_text", "Confidential and proprietary. For "
                                              "internal discussion only."), 8, color=T["mid"])))
    return els


@layout("agenda")
def agenda(slide, ctx):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    items = d["items"]
    active = d.get("active")
    row = min(48.0, (bottom - TOP - 10) / max(1, len(items)))
    y = TOP + 8
    for i, it in enumerate(items, 1):
        on = active is None or active == i
        col = T["navy"] if on else T["mid"]
        els.append(S.text(MAIN_X, y, 50, r("%02d" % i, 22, True, col), va="m", h=row - 8))
        els.append(S.text(MAIN_X + 60, y, 700, r(it if isinstance(it, str) else it["title"], 15, on and active is not None, col),
                          va="m", h=row - 8, max_lines=1))
        if not isinstance(it, str) and it.get("note"):
            els.append(S.text(MAIN_X + 620, y, 268, r(it["note"], 10, color=T["grey"]), va="m", h=row - 8, align="r"))
        y += row
        els.append(S.hline(MAIN_X, y - 4, SIDE_R, T["rule"], 0.5))
    return els


@layout("section")
def section(slide, ctx):
    d = slide["data"]
    els = [S.rect(0, 0, 960, 6, fill=T["navy"])]
    if d.get("number"):
        els.append(S.text(60, 170, 200, r(str(d["number"]), 54, True, T["sky"])))
    els.append(S.text(60, 250, 800, r(slide["title"], 30, True, T["navy"]), lh=1.15, max_lines=2))
    if d.get("subtitle"):
        els.append(S.text(60, 330, 760, r(d["subtitle"], 13, color=T["grey"]), lh=1.3, max_lines=3))
    els.append(S.text(T["Rm"] - 120, 520, 120, r(str(ctx["page"]), 8, color=T["grey"]), align="r"))
    return els


@layout("exec-summary")
def exec_summary(slide, ctx):
    """Dot-dash executive summary: bold lead statements (left) with supporting points (right)."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    lead_w, gap = 300.0, 24.0
    built = []
    for pt in d["points"]:
        lead = S.text(MAIN_X, 0, lead_w, md_runs(pt["lead"], 12.5, T["navy"], bold=True), lh=1.28)
        sup = C.bullets(MAIN_X + lead_w + gap, 0, SIDE_R - MAIN_X - lead_w - gap,
                        [(md_runs(x, 11), 1) for x in pt.get("support", [])], size=11, gap=4) if pt.get("support") else None
        built.append((lead, sup, max(lead["h"], sup["h"] if sup else 0)))
    need = sum(h for _, _, h in built) + 20 * len(built)
    if TOP + need > bottom:
        raise S.LayoutError("executive summary needs %.0f pt, %.0f available; cut or move points to the appendix" % (
            need, bottom - TOP))
    pad = min(26.0, (bottom - TOP - need) / (2 * len(built)))
    y = TOP
    for k, (lead, sup, h) in enumerate(built):
        top = y + 10 + pad
        lead["y"] = top
        els.append(lead)
        if sup:
            sup["y"] = top
            els.append(sup)
        y = top + h + 10 + pad
        els.append(S.hline(MAIN_X, y, SIDE_R, T["rule"] if k < len(built) - 1 else T["navy"], 0.75))
    return els


@layout("columns")
def columns(slide, ctx):
    """2-4 columns, each a bold header over a rule with bullets; optional inline icon."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    cols = d["columns"]
    n = len(cols)
    gap = 22.0
    w = (SIDE_R - MAIN_X - gap * (n - 1)) / n
    low = TOP
    for i, c in enumerate(cols):
        x = MAIN_X + i * (w + gap)
        tx = x
        if c.get("icon"):
            els.append(S.icon(c["icon"], x, TOP, 16, T["navy"], 2))
            tx = x + 24
        hd = S.text(tx, TOP, w - (tx - x), md_runs(c["header"], 12, T["navy"], True), lh=1.2, max_lines=2)
        els.append(hd)
        ry = TOP + max(hd["h"], 18) + 4
        els.append(S.hline(x, ry, x + w, T["navy"], 1.5))
        b = C.bullets(x, ry + 8, w, [(md_runs(t, 10.5), 1) if isinstance(t, str) else (md_runs(t[0], 10.5), t[1])
                                     for t in c["bullets"]], size=10.5)
        lim = bottom - (len(d.get("compare", [])) * 34 + 14 if d.get("compare") else 0)
        if b["y"] + b["h"] > lim:
            raise S.LayoutError("column '%s' overflows by %.0f pt" % (c["header"], b["y"] + b["h"] - lim))
        els.append(b)
        low = max(low, b["y"] + b["h"])
    comp = d.get("compare")
    if comp:
        y = low + 26
        for row in comp:
            for i, val in enumerate(row["values"]):
                x = MAIN_X + i * (w + gap)
                els.append(S.hline(x, y, x + w, T["rule"], 0.75))
                els.append(S.text(x, y + 4, w, r(row["label"], 8.5, True, T["grey"]), max_lines=1))
                v = val if isinstance(val, dict) else {"text": val}
                tx = x
                if v.get("rag"):
                    els.append(C.rag_dot(x + 5, y + 24, v["rag"], 9))
                    tx = x + 14
                els.append(S.text(tx, y + 17, w - (tx - x), r(v["text"], 11, True, T["navy"]), max_lines=1))
            y += 34
    return els


# --------------------------------------------------------------------------- charts

def _value_axis(els, x, y_top, y_base, lo, hi, unit_fmt, grid_to):
    ticks = nice_ticks(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    sc = (y_base - y_top) / (hi - lo)
    for t in ticks:
        yy = y_base - (t - lo) * sc
        els.append(S.text(x - 46, yy - 6, 40, r(unit_fmt(t), 8.5, color=T["grey"]), align="r"))
        els.append(S.hline(x, yy, grid_to, T["rule"] if t != 0 else T["ink"], 0.4 if t != 0 else 0.75))
    return lo, hi, sc


@layout("bar")
def bar(slide, ctx):
    """Column or horizontal bar chart, single or multi-series, with direct value labels."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    side = default_side(slide)
    right = MAIN_R if side else SIDE_R
    hdr, y = C.exhibit_header(MAIN_X, TOP, right - MAIN_X, d.get("exhibit", ""), d.get("unit"))
    els += hdr
    cats, series = d["categories"], d["series"]
    pre, suf, dp = d.get("prefix", ""), d.get("suffix", ""), d.get("decimals")
    hi_idx = d.get("highlight")
    stacked = d.get("stacked", False)
    if len(series) > 1:
        cols = [T["navy"], "#8FA6C4", T["mid"], T["blue"], "#C9D3DF"]
        els += C.legend(MAIN_X, y, [("bar", cols[i % 5], s["name"]) for i, s in enumerate(series)])
        y += 18
    else:
        cols = [T["navy"]]
    totals = [sum(s["values"][i] for s in series) for i in range(len(cats))] if stacked else \
        [max(s["values"][i] for s in series) for i in range(len(cats))]
    vmax = max(totals)
    vmin = min(0, min(min(s["values"]) for s in series))
    if d.get("orientation", "column") == "bar":
        lab_w = d.get("label_width", 150)
        x0, x1 = MAIN_X + lab_w, right - 50
        rows = len(cats)
        rh = min(34.0, (bottom - y - 10) / rows)
        sc = (x1 - x0) / (vmax - vmin or 1)
        for i, c in enumerate(cats):
            yy = y + i * rh
            els.append(S.text(MAIN_X, yy, lab_w - 10, r(c, 10, i == hi_idx), va="m", h=rh - 4, align="r", lh=1.15))
            xs = x0 - vmin * sc
            bh = (rh - 10) / (1 if stacked else len(series))
            for j, s in enumerate(series):
                v = s["values"][i]
                col = (T["navy"] if (hi_idx is None or i == hi_idx) else "#8FA6C4") if len(series) == 1 else cols[j % 5]
                by = yy + 2 + (0 if stacked else j * bh)
                els.append(S.rect(min(xs, xs + v * sc), by, abs(v * sc), bh, fill=col))
                if not stacked:
                    els.append(S.text(xs + max(v, 0) * sc + 4, by, 60, r(fmt(v, dp, pre, suf), 9, i == hi_idx), va="m", h=bh))
                xs += v * sc if stacked else 0
            if stacked:
                els.append(S.text(xs + 4, yy + 2, 60, r(fmt(totals[i], dp, pre, suf), 9, True), va="m", h=rh - 10))
        els.append(S.line(x0 - vmin * sc, y - 2, x0 - vmin * sc, y + rows * rh, T["ink"], 0.75))
    else:
        base = bottom - 30
        lo, hi, sc = (vmin, vmax * 1.08, 0)
        plot_top = y + 22
        sc = (base - plot_top) / (hi - lo)
        n = len(cats)
        slot = (right - MAIN_X - 10) / n
        bw = min(56.0, slot * 0.62)
        for i, c in enumerate(cats):
            cx = MAIN_X + 10 + slot * i + slot / 2
            yb = base + lo * sc
            if stacked or len(series) == 1:
                acc = 0.0
                for j, s in enumerate(series):
                    v = s["values"][i]
                    col = (T["navy"] if (hi_idx is None or i == hi_idx) else "#8FA6C4") if len(series) == 1 else cols[j % 5]
                    els.append(S.rect(cx - bw / 2, yb - (acc + v) * sc, bw, v * sc, fill=col))
                    if stacked and v * sc > 14:
                        els.append(S.text(cx - bw / 2, yb - (acc + v) * sc, bw, r(fmt(v, dp), 8.5, color=T["white"] if j == 0 else T["ink"]),
                                          align="c", va="m", h=v * sc))
                    acc += v
                els.append(S.text(cx - slot / 2, yb - acc * sc - 15, slot, r(fmt(acc, dp, pre, suf), 9.5, i == hi_idx or stacked),
                                  align="c"))
            else:
                sw = bw / len(series)
                for j, s in enumerate(series):
                    v = s["values"][i]
                    bx = cx - bw / 2 + j * sw
                    els.append(S.rect(bx, yb - v * sc, sw - 1, v * sc, fill=cols[j % 5]))
                    els.append(S.text(bx - 10, yb - v * sc - 13, sw + 20, r(fmt(v, dp), 8), align="c"))
            els.append(S.text(cx - slot / 2 + 2, base + 5, slot - 4, r(c, 9, i == hi_idx), align="c", lh=1.15, max_lines=2))
        els.append(S.hline(MAIN_X, base, right, T["ink"], 0.75))
        if d.get("cagr"):
            g = d["cagr"]
            a, b = g.get("from", 0), g.get("to", n - 1)
            xa, xb = MAIN_X + 10 + slot * a + slot / 2, MAIN_X + 10 + slot * b + slot / 2
            yy = plot_top - 8
            els.append(S.line(xa, yy, xb, yy, T["navy"], 0.75, head="arrow"))
            lw_ = S.line_width([r(g["label"], 9, True)]) + 16
            els.append(S.rect((xa + xb) / 2 - lw_ / 2, yy - 9, lw_, 18, fill=T["white"], line=T["navy"], shape="ellipse"))
            els.append(S.text((xa + xb) / 2 - lw_ / 2, yy - 9, lw_, r(g["label"], 9, True, T["navy"]), align="c", va="m", h=18))
    if side:
        els += side_panels(bottom, side)
    return els


@layout("line")
def line_chart(slide, ctx):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    side = default_side(slide)
    right = MAIN_R if side else SIDE_R
    hdr, y = C.exhibit_header(MAIN_X, TOP, right - MAIN_X, d.get("exhibit", ""), d.get("unit"))
    els += hdr
    xs, series = d["x"], d["series"]
    pre, suf, dp = d.get("prefix", ""), d.get("suffix", ""), d.get("decimals")
    allv = [v for s in series for v in s["values"] if v is not None]
    lo = d.get("axis_min", min(0, min(allv)))
    hi = d.get("axis_max", max(allv))
    x0, x1 = MAIN_X + 50, right - 110
    base, top = bottom - 26, y + 10
    lo, hi, sc = _value_axis(els, x0, top, base, lo, hi, lambda t: fmt(t, dp, pre, suf), x1)
    step = (x1 - x0) / max(1, len(xs) - 1)
    for i, lab in enumerate(xs):
        if len(xs) <= 12 or i % 2 == 0 or i == len(xs) - 1:
            els.append(S.text(x0 + i * step - 30, base + 5, 60, r(str(lab), 8.5, color=T["grey"]), align="c"))
    labels = []
    for j, s in enumerate(series):
        hl = s.get("highlight", j == 0)
        col = s.get("color") or (T["navy"] if hl else ["#8FA6C4", T["mid"], "#C9D3DF"][j % 3])
        pts = [(x0 + i * step, base - (v - lo) * sc) for i, v in enumerate(s["values"]) if v is not None]
        for a, b in zip(pts, pts[1:]):
            els.append(S.line(a[0], a[1], b[0], b[1], col, 2.0 if hl else 1.25, dash="dash" if s.get("forecast") else None))
        if s.get("markers", hl):
            for px, py in pts:
                els.append(S.rect(px - 2.5, py - 2.5, 5, 5, fill=col, shape="ellipse"))
        last = [v for v in s["values"] if v is not None][-1]
        labels.append([pts[-1][1], s["name"], fmt(last, dp, pre, suf), col, hl])
    labels.sort()
    for k in range(1, len(labels)):  # keep end labels apart
        if labels[k][0] - labels[k - 1][0] < 24:
            labels[k][0] = labels[k - 1][0] + 24
    for yy, name, val, col, hl in labels:
        els.append(S.text(x1 + 8, yy - 12, 100, [r(val + "\n", 9.5, True, col), r(name, 8.5, hl, col)], lh=1.2))
    if side:
        els += side_panels(bottom, side)
    return els


@layout("waterfall")
def waterfall(slide, ctx):
    """Bridge from a start total through steps to an end total. Fails if the stated end does not reconcile."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    side = default_side(slide)
    right = MAIN_R if side else SIDE_R
    hdr, y = C.exhibit_header(MAIN_X, TOP, right - MAIN_X, d.get("exhibit", ""), d.get("unit"))
    els += hdr
    pre, suf, dp = d.get("prefix", ""), d.get("suffix", ""), d.get("decimals")
    start, steps = d["start"], d["steps"]
    end_v = start["value"] + sum(s["value"] for s in steps)
    if "value" in d["end"] and abs(d["end"]["value"] - end_v) > 1e-6:
        raise S.LayoutError("waterfall does not reconcile: %s + steps = %s, but end says %s" % (
            start["value"], end_v, d["end"]["value"]))
    bars = [(start["label"], start["value"], "total")] + [(s["label"], s["value"], "step") for s in steps] + \
           [(d["end"]["label"], end_v, "total")]
    running, lo_seen, hi_seen = 0.0, [], []
    for _, v, k in bars:
        if k == "total":
            running = v
        else:
            running += v
        lo_seen.append(running)
        hi_seen.append(running)
    floor = d.get("axis_min", 0)
    top_v = max(hi_seen + [start["value"] + max(0, sum(max(0, s["value"]) for s in steps))])
    base_y = bottom - 34
    plot_top = y + 44
    sc = (base_y - plot_top) / (top_v - floor)
    n = len(bars)
    slot = (right - MAIN_X - 20) / n
    bw = min(70.0, slot * 0.68)
    x = MAIN_X + 20 + (slot - bw) / 2
    tot, prev, centers = 0.0, None, []
    for label, v, kind in bars:
        if kind == "total":
            top_v_, bot_v, col = v, floor, T["navy"]
            tot = v
        else:
            bot_v, top_v_ = (tot, tot + v) if v >= 0 else (tot + v, tot)
            col = T["R"] if (v > 0) == (d.get("increase_is", "bad") == "bad") else T["G"]
            tot += v
        yt, yb = base_y - (top_v_ - floor) * sc, base_y - (bot_v - floor) * sc
        els.append(S.rect(x, yt, bw, max(yb - yt, 0.75), fill=col))
        lab = fmt(v, dp, pre, suf) if kind == "total" else (("+" if v > 0 else "") + fmt(v, dp))
        els.append(S.text(x - 14, yt - 15, bw + 28, r(lab, 10, True), align="c"))
        els.append(S.text(x - slot * 0.16, base_y + 5, bw + slot * 0.32, r(label, 9), align="c", lh=1.15, max_lines=2))
        if prev is not None:
            els.append(S.line(x - (slot - bw), prev, x, prev, T["grey"], 0.5, dash="dot"))
        prev = base_y - (tot - floor) * sc
        centers.append((x + bw / 2, yt))
        x += slot
    els.append(S.hline(MAIN_X + 10, base_y, x - (slot - bw) + 10, T["ink"], 0.75))
    if d.get("show_total_change", True):
        delta = end_v - start["value"]
        pct = delta / start["value"] * 100 if start["value"] else 0
        txt = "%s%s (%s%.1f%%)" % ("+" if delta >= 0 else "", fmt(delta, dp, pre, suf), "+" if pct >= 0 else "", pct)
        yb_ = y + 20
        a, b = centers[0][0], centers[-1][0]
        els += [S.line(a, yb_, b, yb_, T["navy"], 0.75), S.line(a, yb_, a, centers[0][1] - 18, T["navy"], 0.75),
                S.line(b, yb_, b, centers[-1][1] - 18, T["navy"], 0.75, head="arrow")]
        lw_ = S.line_width([r(txt, 9, True)]) + 18
        els.append(S.rect((a + b) / 2 - lw_ / 2, yb_ - 9, lw_, 18, fill=T["white"], line=T["navy"], shape="roundRect", radius=9))
        els.append(S.text((a + b) / 2 - lw_ / 2, yb_ - 9, lw_, r(txt, 9, True, T["navy"]), align="c", va="m", h=18))
    for n_, idx in enumerate(d.get("callouts", []), 1):
        cx, cy = centers[idx]
        els += C.callout(cx + bw / 2 + 9, cy + 8, n_)
    if side:
        els += side_panels(bottom, side)
    return els


@layout("matrix-2x2")
def matrix_2x2(slide, ctx):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    side = default_side(slide)
    right = MAIN_R if side else SIDE_R
    x0, x1 = MAIN_X + 40, right - 20
    y0, y1 = TOP + 10, bottom - 34
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    ql = d.get("quadrants", ["", "", "", ""])  # TL, TR, BL, BR
    hq = d.get("highlight_quadrant")
    for k, (qx, qy) in enumerate([(x0, y0), (mx, y0), (x0, my), (mx, my)]):
        els.append(S.rect(qx + 1, qy + 1, (x1 - x0) / 2 - 2, (y1 - y0) / 2 - 2, fill=T["sky"] if hq == k else T["tint"]))
        if ql[k]:
            ax = "l" if k in (0, 2) else "r"
            tx = qx + 8 if ax == "l" else qx + (x1 - x0) / 2 - 208
            ty = qy + 8 if k < 2 else qy + (y1 - y0) / 2 - 20
            els.append(S.text(tx, ty, 200, r(ql[k], 9, True, T["grey"]), align=ax))
    els.append(S.line(x0, y1, x1 + 6, y1, T["ink"], 1, head="arrow"))
    els.append(S.line(x0, y1, x0, y0 - 6, T["ink"], 1, head="arrow"))
    xa, ya = d["x"], d["y"]
    els.append(S.text(x0, y1 + 6, x1 - x0, r(xa["label"], 9.5, True), align="c"))
    els.append(S.text(x0, y1 + 6, 120, r(xa.get("low", "Low"), 8.5, color=T["grey"])))
    els.append(S.text(x1 - 120, y1 + 6, 120, r(xa.get("high", "High"), 8.5, color=T["grey"]), align="r"))
    els.append(S.text(MAIN_X - 6, y0 - 2, 44, r(ya["label"], 9.5, True), lh=1.15))
    els.append(S.text(MAIN_X - 6, y1 - 14, 44, r(ya.get("low", "Low"), 8.5, color=T["grey"])))
    for it in d["items"]:
        px, py = x0 + it["x"] * (x1 - x0), y1 - it["y"] * (y1 - y0)
        rad = it.get("size", 1.0) * 7
        hl = it.get("highlight")
        els.append(S.rect(px - rad, py - rad, 2 * rad, 2 * rad, fill=T["navy"] if hl else T["mid"], shape="ellipse"))
        els.append(S.text(px + rad + 4, py - 6, 150, r(it["label"], 9, hl, T["navy"] if hl else T["ink"])))
    if side:
        els += side_panels(bottom, side)
    return els


# --------------------------------------------------------------------------- tables

def table(x, y, w, columns, rows, size=9.5, bottom=None, header=True, pad=6.0, min_h=22.0):
    """Consulting table. columns: [{name, width (fraction or pt), align, kind: text|rag|trend|number|bold}].
    Widths that are fractions are of w. Row height grows with wrapped text."""
    widths = []
    fixed = sum(c["width"] for c in columns if c.get("width", 0) > 1)
    frac_cols = [c for c in columns if not c.get("width") or c["width"] <= 1]
    rest = w - fixed
    tot_frac = sum(c.get("width") or 1.0 / len(frac_cols) for c in frac_cols) or 1
    for c in columns:
        cw = c["width"] if c.get("width", 0) > 1 else rest * (c.get("width") or 1.0 / len(frac_cols)) / tot_frac
        widths.append(cw)
    els = []
    if header:
        els.append(S.rect(x, y, w, 22, fill=T["navy"]))
        cx = x
        for c, cw in zip(columns, widths):
            al = c.get("align", "c" if c.get("kind") in ("rag", "trend") else "r" if c.get("kind") == "number" else "l")
            els.append(S.text(cx + pad, y, cw - 2 * pad, r(c["name"], 9, True, T["white"]), va="m", h=22, align=al, max_lines=1))
            cx += cw
        y += 22
    for row in rows:
        cells, h = [], min_h
        cx = x
        for c, cw, val in zip(columns, widths, row):
            k = c.get("kind", "text")
            if k in ("text", "bold", "number"):
                al = c.get("align", "r" if k == "number" else "l")
                t = S.text(cx + pad, y + 5, cw - 2 * pad, md_runs(str(val), size, bold=(k == "bold")), lh=1.25, align=al)
                cells.append(t)
                h = max(h, t["h"] + 10)
            else:
                cells.append((k, val, cx + cw / 2, c.get("good", "up")))
            cx += cw
        for cell in cells:
            if isinstance(cell, tuple):
                k, val, cx_, good = cell
                if k == "rag" and val:
                    els.append(C.rag_dot(cx_, y + 11.5, val, 10))
                elif k == "trend" and val:
                    els.append(C.trend(cx_, y + 11.5, val, trend_color(val, good), 8))
            else:
                els.append(cell)
        y += h
        els.append(S.hline(x, y, x + w, T["rule"], 0.5))
        if bottom and y > bottom:
            raise S.LayoutError("table overflows by %.0f pt; split it or move rows to the appendix" % (y - bottom))
    return els, y


@layout("table")
def table_slide(slide, ctx):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    side = default_side(slide)
    right = MAIN_R if side else SIDE_R
    y = TOP
    if d.get("exhibit"):
        hdr, y = C.exhibit_header(MAIN_X, TOP, right - MAIN_X, d["exhibit"], d.get("unit"))
        els += hdr
    t, yy = table(MAIN_X, y, right - MAIN_X, d["columns"], d["rows"], bottom=bottom - 16)
    els += t
    kinds = {c.get("kind") for c in d["columns"]}
    leg = []
    if "rag" in kinds:
        leg += [("dot", "G", "On track"), ("dot", "A", "At risk"), ("dot", "R", "Off track")]
    if "trend" in kinds:
        leg += [("up", T["G"], "Improving"), ("flat", T["grey"], "Stable"), ("down", T["R"], "Worsening")]
    if leg:
        els += C.legend(MAIN_X, yy + 8, leg)
    if side:
        els += side_panels(bottom, side)
    return els


@layout("decisions")
def decisions(slide, ctx):
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    cols = [{"name": "#", "width": 28, "kind": "bold"}, {"name": "Decision required", "width": 0.34, "kind": "bold"},
            {"name": "Recommendation and impact", "width": 0.40}, {"name": "Owner", "width": 0.13},
            {"name": "By", "width": 0.13}]
    rows = [[str(i), x["what"], x.get("recommendation", ""), x.get("owner", ""), x.get("due", "")]
            for i, x in enumerate(d["decisions"], 1)]
    t, _ = table(MAIN_X, TOP, SIDE_R - MAIN_X, cols, rows, size=11, bottom=bottom - 4,
                 min_h=44)
    return els + t
