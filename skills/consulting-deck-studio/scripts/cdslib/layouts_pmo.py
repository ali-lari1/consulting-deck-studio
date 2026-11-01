"""PMO and capital-project layouts: status summary, RAG dashboard, Gantt, risk heat map, options matrix."""
import calendar
import datetime

from . import components as C
from . import scene as S
from .components import G, T, r
from .deckmd import md_runs
from .layouts import chrome, default_side, layout, side_panels, table, trend_color

LBL = dict(size=8.5, bold=True, color=T["grey"])
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def lbl(text):
    return C.r(text, **LBL)


@layout("status-summary")
def status_summary(slide, ctx):
    """Rows of area | RAG | trend | summary, a decisions panel, and an optional look-ahead table."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    x0, xs, xt, xx = G.L, G.L + 114, G.L + 176, G.L + 210
    xr = G.main_r - 16
    y = G.top
    for xh, txt in [(x0, "Area"), (xs, "Status"), (xt - 4, "Trend"), (xx, "Summary")]:
        els.append(S.text(xh, y, 120, lbl(txt)))
    els.append(S.hline(x0, y + 14, xr, T["navy"], 0.75))
    y += 22
    for row in d["rows"]:
        t = S.text(xx, y + 2, xr - xx, md_runs(row["text"], 10.5), lh=1.3)
        h = max(30, t["h"] + 6)
        lx = x0
        if row.get("icon"):
            els += C.icon_tile(x0, y - 2, row["icon"], h - 4)
            lx = x0 + 22
        els.append(S.text(lx, y, xs - lx - 4, r(row["area"], 10.5, True, T["navy"]), va="m", h=h - 4, lh=1.15))
        els += C.rag_pill(xs, y + (h - 15) / 2 - 2, row["rag"])
        tr = row.get("trend", "flat")
        els.append(C.trend(xt + 6, y + h / 2 - 2, tr, trend_color(tr, "up")))
        els.append(t)
        y += h + 6
        els.append(S.hline(x0, y - 3, xr, T["rule"], 0.5))
    els += C.legend(x0, y + 4, [("dot", "G", "On track"), ("dot", "A", "At risk, recoverable"),
                                ("dot", "R", "Off track, decision needed")])
    els += C.legend(x0 + 330, y + 4, [("down", T["R"], "Worse"), ("flat", T["grey"], "Unchanged"), ("up", T["G"], "Better")])
    la = d.get("lookahead")
    if la:
        hdr, ly = C.exhibit_header(x0, y + 26, xr - x0, la.get("title", "Look-ahead: key milestones"))
        els += hdr
        lc = [("Milestone", 0.43), ("Baseline", 0.14), ("Forecast", 0.14), ("Variance", 0.13), ("Status", 0.16)]
        W = xr - x0
        cx = x0
        for name, f in lc:
            els.append(S.text(cx, ly, W * f - 6, lbl(name)))
            cx += W * f
        ly += 14
        for m in la["rows"]:
            cx = x0
            late = m["rag"] == "R"
            for (name, f), val in zip(lc, [m["milestone"], m["baseline"], m["forecast"], m.get("variance", ""), None]):
                if name == "Status":
                    els += C.rag_pill(cx, ly + 2, m["rag"])
                else:
                    hot = name == "Variance" and late
                    els.append(S.text(cx, ly + 4, W * f - 6, r(val, 10, hot, T["R"] if hot else None), max_lines=1))
                cx += W * f
            ly += 19
            els.append(S.hline(x0, ly, xr, T["rule"], 0.5))
        y = ly
    if y > bottom:
        raise S.LayoutError("status rows need %.0f pt, %.0f available; shorten summaries or drop the look-ahead" % (
            y - G.top, bottom - G.top))
    dec = d.get("decisions")
    if dec:
        hdr, iy = C.header_box(G.side_x, G.top, G.R - G.side_x, 0, d.get("decisions_title", "Decisions needed"))
        els += hdr
        yy = iy
        w = G.R - G.side_x
        for i, x in enumerate(dec, 1):
            els += C.callout(G.side_x + 7, yy + 7, i)
            t = S.text(G.side_x + 22, yy, w - 22, md_runs(x["what"], 10.5, bold=True), lh=1.3)
            els.append(t)
            yy += t["h"] + 3
            meta = []
            if x.get("owner"):
                meta += [r("Owner: ", 9, True, T["grey"]), r(x["owner"] + "   ", 9, color=T["grey"])]
            if x.get("due"):
                meta += [r("Due: ", 9, True, T["grey"]), r(x["due"], 9, color=T["grey"])]
            if meta:
                els.append(S.text(G.side_x + 22, yy, w - 22, meta))
                yy += 14
            yy += 8
            if i < len(dec):
                els.append(S.hline(G.side_x, yy - 6, G.R, T["rule"], 0.5))
        if yy > bottom:
            raise S.LayoutError("decisions panel overflows by %.0f pt" % (yy - bottom))
    return els


@layout("rag-dashboard")
def rag_dashboard(slide, ctx):
    """Number strip of KPIs over a workstream RAG table."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    kp = d.get("kpis", [])
    y = G.top
    if kp:
        w = (G.R - G.L) / len(kp)
        for i, k in enumerate(kp):
            els += C.kpi_card(G.L + i * w + (14 if i else 0), y, w, 72, None, k["label"], k["value"], k.get("note"), k.get("rag"))
            if i:
                els.append(S.line(G.L + i * w, y + 2, G.L + i * w, y + 64, T["rule"], 0.75))
        y += 86
    cols = d.get("columns") or [
        {"name": "Workstream", "width": 0.17, "kind": "bold"}, {"name": "Lead", "width": 0.10},
        {"name": "Schedule", "width": 0.07, "kind": "rag"}, {"name": "Cost", "width": 0.06, "kind": "rag"},
        {"name": "Risk", "width": 0.06, "kind": "rag"}, {"name": "Trend", "width": 0.06, "kind": "trend"},
        {"name": "Key issue and next step", "width": 0.48}]
    keys = d.get("keys") or ["workstream", "lead", "schedule", "cost", "risk", "trend", "comment"]
    rows = [[row.get(k, "") for k in keys] for row in d["rows"]]
    t, yy = table(G.L, y, G.R - G.L, cols, rows, bottom=bottom - 16, min_h=d.get("row_height", 26))
    els += t
    els += C.legend(G.L, yy + 8, [("dot", "G", "On track"), ("dot", "A", "At risk"), ("dot", "R", "Off track"),
                                     ("up", T["G"], "Improving"), ("flat", T["grey"], "Stable"), ("down", T["R"], "Worsening")])
    return els


def _date(s):
    p = [int(x) for x in str(s).split("-")]
    return datetime.date(p[0], p[1], p[2] if len(p) > 2 else 1)


def _dm(s):
    d = _date(s)
    return "%d %s" % (d.day, MON[d.month - 1])


def _months_between(a, b):
    """Fractional months from date a (first of its month) to date b."""
    whole = (b.year - a.year) * 12 + (b.month - a.month)
    return whole + (b.day - 1) / float(calendar.monthrange(b.year, b.month)[1])


@layout("gantt")
def gantt(slide, ctx):
    """Baseline vs forecast bars by workstream, milestones (baseline -> forecast), today line, float brackets."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    side = default_side(slide)
    right = G.main_r if side else G.R
    hdr, y = C.exhibit_header(G.L, G.top, right - G.L, d.get("exhibit", "Schedule, baseline vs forecast"), d.get("unit"))
    els += hdr
    start = _date(d["start"]).replace(day=1)
    end = _date(d["end"])
    nm = max(1, _months_between(start, end))
    nm_int = int(nm + 0.999)
    lab_w = d.get("label_width", 150)
    x0, x1 = G.L + lab_w, right
    mw = (x1 - x0) / nm_int

    def X(s):
        return x0 + _months_between(start, _date(s)) * mw

    for i in range(nm_int):
        mdate = datetime.date(start.year + (start.month - 1 + i) // 12, (start.month - 1 + i) % 12 + 1, 1)
        lab = MON[mdate.month - 1] + (" %s" % str(mdate.year)[2:] if mdate.month == 1 or i == 0 else "")
        els.append(S.rect(x0 + i * mw, y, mw - 1, 14, fill=T["tint"]))
        els.append(S.text(x0 + i * mw, y + 3, mw, r(lab, 7.5 if mw < 40 else 8, True, T["grey"]), align="c", max_lines=1))
    gy0 = y + 18
    rows = d["rows"]
    ms = d.get("milestones", [])
    leg_h = 22
    avail = bottom - gy0 - leg_h - (len(ms) * 26 + 8 if ms else 0)
    rh = min(32.0, avail / max(1, len(rows)))
    if rh < 18:
        raise S.LayoutError("Gantt has too many rows (%d) for one slide; group them or split the slide" % len(rows))
    for i, row in enumerate(rows):
        yy = gy0 + i * rh
        if row.get("rag"):
            els.append(C.rag_dot(G.L + 6, yy + rh / 2, row["rag"], 9))
        els.append(S.text(G.L + 16, yy, lab_w - 20, r(row["name"], 10, row.get("critical", False)), va="m", h=rh, lh=1.1, max_lines=2))
        if row.get("baseline"):
            b0, b1 = X(row["baseline"][0]), X(row["baseline"][1])
            els.append(S.rect(b0, yy + rh * 0.2, b1 - b0, rh * 0.2, fill=None, line=T["mid"], lw=0.75))
        f0, f1 = X(row["forecast"][0]), X(row["forecast"][1])
        els.append(S.rect(f0, yy + rh * 0.46, f1 - f0, rh * 0.3, fill=T["navy"] if row.get("critical") else T["navy_l"]))
        if row.get("float_to"):
            fx = X(row["float_to"])
            fy = yy + rh * 0.61
            els.append(S.line(f1 + 2, fy, fx, fy, T["G"], 0.75, head="arrow"))
            els.append(S.text(f1 + 2, yy + rh * 0.78, fx - f1, r(row.get("float_label", "float"), 7.5, True, T["G"]), align="c"))
        if row.get("callout"):
            els += C.callout(f1 + 10, yy + rh * 0.61, row["callout"])
        els.append(S.hline(G.L, yy + rh, x1, T["rule"], 0.4))
    my = gy0 + len(rows) * rh + 4
    for i in range(1, nm_int):
        els.append(S.line(x0 + i * mw, gy0, x0 + i * mw, my + len(ms) * 26, T["rule"], 0.4, dash="dot"))
    for m in ms:
        els.append(S.text(G.L + 16, my, lab_w - 20, r(m["name"], 10, True), va="m", h=24, max_lines=1))
        fx = X(m["forecast"])
        if m.get("baseline") and m["baseline"] != m["forecast"]:
            bx = X(m["baseline"])
            els.append(C.diamond(bx, my + 12, 10, T["mid"]))
            late = fx > bx
            els.append(S.line(bx + (7 if late else -7), my + 12, fx + (-8 if late else 8), my + 12, T["R"] if late else T["G"], 1, head="arrow"))
            els.append(S.text(bx - 40, my + 17, 80, r(_dm(m["baseline"]), 7.5, color=T["grey"]), align="c"))
        els.append(C.diamond(fx, my + 12, 11, T["navy"]))
        els.append(S.text(fx - 40, my + 17, 80, r(_dm(m["forecast"]), 7.5, True, T["navy"]), align="c"))
        if m.get("callout"):
            els += C.callout(fx + 14, my + 12, m["callout"])
        my += 26
    if d.get("today"):
        tx = X(d["today"])
        els.append(S.line(tx, gy0 - 4, tx, my + 4, T["R"], 1, dash="dash"))
    els += C.legend(G.L, my + 8, [("outline", T["mid"], "Baseline"), ("bar", T["navy"], "Forecast, critical path"),
                                     ("bar", T["navy_l"], "Forecast, other"), ("diamond", T["navy"], "Milestone")] +
                    ([("dash", T["R"], "Today")] if d.get("today") else []))
    if side:
        els += side_panels(bottom, side)
    return els


@layout("risk-heatmap")
def risk_heatmap(slide, ctx):
    """5x5 likelihood x impact grid with movement since last period, plus the top-risk table."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    red, amber = d.get("red_from", 15), d.get("amber_from", 8)
    hdr, y = C.exhibit_header(G.L, G.top, 286, d.get("exhibit", "Top risks, current position"),
                              d.get("unit", "Likelihood x impact"))
    els += hdr
    gx = G.L + 30
    c = min(47.0, (bottom - y - 60) / 5)
    gy = y + 16
    els.append(S.text(G.L, y, 120, r("Likelihood", 8.5, True, T["grey"])))
    for li in range(5):
        for ii in range(5):
            sc = (5 - li) * (ii + 1)
            k = "R_t" if sc >= red else "A_t" if sc >= amber else "G_t"
            els.append(S.rect(gx + ii * c, gy + li * c, c - 2, c - 2, fill=T[k]))
    for k in range(5):
        els.append(S.text(gx - 16, gy + k * c + c / 2 - 6, 10, r(str(5 - k), 8.5, color=T["grey"]), align="r"))
        els.append(S.text(gx + k * c, gy + 5 * c + 2, c - 2, r(str(k + 1), 8.5, color=T["grey"]), align="c"))
    els.append(S.text(gx, gy + 5 * c + 14, 5 * c, r("Impact", 9, True, T["grey"]), align="c"))

    def pos(L, I, slot=0):
        return gx + (I - 1) * c + (c - 2) / 2, gy + (5 - L) * c + (c - 2) / 2 + slot

    risks = d["risks"]
    seen = {}
    placed = {}
    for rk in risks:
        key = (rk["l"], rk["i"])
        n = seen.get(key, 0)
        seen[key] = n + 1
        placed[rk["id"]] = n
    for rk in risks:
        if rk.get("prev"):
            pl, pi = rk["prev"]
            if (pl, pi) != (rk["l"], rk["i"]):
                px, py = pos(pl, pi)
                cx, cy = pos(rk["l"], rk["i"])
                els.append(S.rect(px - 13, py - 8, 26, 16, fill=None, line=T["grey"], lw=0.75))
                els.append(S.line(px, py + (-9 if cy < py else 9), cx, cy + (9 if cy < py else -9), T["ink"], 1, head="arrow"))
    for rk in risks:
        n = seen[(rk["l"], rk["i"])]
        k = placed[rk["id"]]
        cx, cy = pos(rk["l"], rk["i"], (k - (n - 1) / 2.0) * 17)
        els.append(S.rect(cx - 14, cy - 8, 28, 16, fill=T["navy"]))
        els.append(S.text(cx - 14, cy - 8, 28, r(rk["id"], 8, True, T["white"]), align="c", va="m", h=16))
    els += C.legend(G.L, gy + 5 * c + 32, [("bar", T["navy"], "Now"), ("outline", T["grey"], "Last period")])
    tx = G.L + 306
    cols = [{"name": "ID", "width": 36, "kind": "bold"}, {"name": "Risk", "width": 0.37},
            {"name": "Owner", "width": 0.13}, {"name": "Score", "width": 64, "kind": "bold"},
            {"name": "", "width": 20, "kind": "trend", "good": "down"}, {"name": "Mitigation and status", "width": 0.40}]
    rows = []
    for rk in risks:
        score = rk["l"] * rk["i"]
        sc_txt = ("%d → %d" % (rk["prev"][0] * rk["prev"][1], score)) if rk.get("prev") else str(score)
        tr = rk.get("trend") or ("up" if rk.get("prev") and score > rk["prev"][0] * rk["prev"][1] else
                                 "down" if rk.get("prev") and score < rk["prev"][0] * rk["prev"][1] else "flat")
        rows.append([rk["id"], rk["title"], rk.get("owner", ""), sc_txt, tr,
                     rk.get("mitigation", "")])
    t, yy = table(tx, G.top, G.R - tx, cols, rows, size=9.5, bottom=bottom - 16)
    els += t
    els += C.legend(tx, yy + 6, [("up", T["R"], "Score rising"), ("flat", T["grey"], "Unchanged"), ("down", T["G"], "Score falling")])
    return els


@layout("options-matrix")
def options_matrix(slide, ctx):
    """Weighted Harvey-ball evaluation of options, recommended option outlined, rationale panel."""
    d = slide["data"]
    els, bottom = chrome(slide, ctx)
    y0 = G.top
    if d.get("stages"):
        els += C.chevrons(G.L, G.top - 2, G.main_r - G.L, 24, d["stages"], d.get("stage"))
        y0 = G.top + 36
    crit, opts = d["criteria"], d["options"]
    lab_w = 180.0
    wcol = 60.0 if any("weight" in c for c in crit) else 0
    x0 = G.L + lab_w + wcol
    cw = (G.main_r - x0) / len(opts)
    rows_h = min(38.0, (bottom - y0 - 110) / len(crit))
    rec = d.get("recommended")
    for j, o in enumerate(opts):
        hd = S.text(x0 + j * cw + 6, y0, cw - 12, [r("Option %s\n" % o["key"], 10, True, T["navy"]),
                                                  r(o["name"], 9, color=T["grey"])], align="c", lh=1.2, max_lines=3)
        els.append(hd)
    if wcol:
        els.append(S.text(G.L + lab_w, y0 + 12, wcol, r("Weight", 9, True, T["grey"]), align="c"))
    hy = y0 + 40
    els.append(S.hline(G.L, hy, G.main_r, T["navy"], 0.75))
    weights = [float(str(c.get("weight", "0")).rstrip("%")) / 100 for c in crit]
    for i, c_ in enumerate(crit):
        y = hy + 6 + i * rows_h
        els.append(S.text(G.L, y, lab_w - 6, r(c_["name"], 10.5), va="m", h=rows_h - 8, lh=1.15, max_lines=2))
        if wcol:
            els.append(S.text(G.L + lab_w, y, wcol, r(str(c_["weight"]), 10.5, color=T["grey"]), align="c", va="m", h=rows_h - 8))
        for j, o in enumerate(opts):
            dd = min(20.0, rows_h - 14)
            els.append(S.pie(x0 + j * cw + cw / 2 - dd / 2, y + (rows_h - 8 - dd) / 2, dd, o["scores"][i] * 90,
                             fill=T["navy"], line=T["navy"], lw=1))
        els.append(S.hline(G.L, y + rows_h - 4, G.main_r, T["rule"], 0.5))
    y = hy + 6 + len(crit) * rows_h
    if wcol:
        els.append(S.text(G.L, y, lab_w, r("Weighted score", 10.5, True), va="m", h=26))
        for j, o in enumerate(opts):
            tot = sum(a * b for a, b in zip(o["scores"], weights))
            els.append(S.text(x0 + j * cw, y, cw, r("%.1f" % tot, 13, True, T["navy"] if o["key"] == rec else T["ink"]),
                              align="c", va="m", h=26))
        if abs(sum(weights) - 1) > 0.001:
            raise S.LayoutError("criteria weights add to %.0f%%, not 100%%" % (sum(weights) * 100))
        y += 30
    if rec:
        j = [o["key"] for o in opts].index(rec)
        els.append(S.rect(x0 + j * cw + 2, y0 - 4, cw - 4, y - y0 + 2, fill=None, line=T["navy"], lw=1.5))
    els += C.legend(G.L, y + 6, [("harvey", 0, "Weak"), ("harvey", 1, ""), ("harvey", 2, ""), ("harvey", 3, ""),
                                    ("harvey", 4, "Strong")], size=8)
    if y + 20 > bottom:
        raise S.LayoutError("options matrix overflows by %.0f pt" % (y + 20 - bottom))
    if d.get("rationale"):
        els += side_panels(bottom, [(d.get("rationale_title", "Rationale"), "bullets", d["rationale"])])
    else:
        side = default_side(slide)
        if side:
            els += side_panels(bottom, side)
    return els
