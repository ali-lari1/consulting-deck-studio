#!/usr/bin/env python3
"""M0 v1: the six parity test slides rebuilt as conventional consulting slides with the component
library. Run: python3 spike/slides_v1.py  (writes spike/out/v1.html, v1.pptx, renders, diffs)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "skills", "consulting-deck-studio", "scripts"))
import run_spike  # noqa: E402
from cdslib import components as C  # noqa: E402
from cdslib import png  # noqa: E402
from cdslib import scene as S  # noqa: E402
from cdslib.components import T, r  # noqa: E402

CTX = "Northline Rail Programme  |  Monthly SteerCo  |  October 2026"
TRACK = ["Summary", "Schedule", "Risk", "Cost", "Workstreams", "Options"]
SRC = "Programme controls period 7 report (Oct 2026); PMO analysis"
LBL = dict(size=8.5, bold=True, color=T["grey"])


def page(n, active, title, sowhat=None, footnotes=None, source=SRC):
    return C.frame(title, n, TRACK, active, CTX, "Preliminary", sowhat, footnotes, source)


def s1_summary():
    els, bottom = page(1, "Summary", "The programme is six weeks behind its re-baselined date, and three decisions "
                       "this month determine whether it recovers",
                       sowhat="Approving the £14m drawdown by 14 November protects the May 2027 handover date",
                       footnotes=["Re-baselined at Gate 3, March 2026. Trend compares with the September report."])
    x0, xs, xt, xx, xr = 36, 150, 210, 246, 610
    y = 104
    for xh, txt in [(x0, "Area"), (xs, "Status"), (xt - 4, "Trend"), (xx, "Summary")]:
        els.append(S.text(xh, y, 120, C.r(txt, **LBL)))
    els.append(S.hline(x0, y + 14, xr, T["navy"], 0.75))
    y += 22
    rows = [
        ("calendar-clock", "Schedule", "R", "down",
         [r("Forecast handover moved from ", 10.5), r("3 Apr to 15 May 2027", 10.5, True),
          r(". Utilities diversion at Kings Cross ran six weeks late; systems integration is now on the critical path.", 10.5)]),
        ("pound-sterling", "Cost", "A", "flat",
         [r("EAC of ", 10.5), r("£1,420m", 10.5, True), r(" against a £1,380m budget. Remaining contingency covers the gap "
                                                          "but falls to 3% of remaining work, below the 5% floor.", 10.5)]),
        ("triangle-alert", "Risk", "R", "down",
         [r("Two of the top ten risks moved into red: signalling software maturity and Christmas possession "
            "availability. Both lack funded mitigations.", 10.5)]),
        ("users", "Stakeholders", "G", "flat",
         [r("Operator and Network Rail remain aligned on the May date. Sponsor briefing held on 22 October.", 10.5)]),
    ]
    for ic, label, rag, tr, body in rows:
        t = S.text(xx, y + 2, xr - xx, body, lh=1.3)
        h = max(30, t["h"] + 6)
        els += C.icon_tile(x0, y + (h - 26) / 2 - 1, ic)
        els.append(S.text(x0 + 22, y, 90, r(label, 10.5, True, T["navy"]), va="m", h=h - 4))
        els += C.rag_pill(xs, y + (h - 15) / 2 - 2, rag)
        els.append(C.trend(xt + 6, y + h / 2 - 2, tr, T[{"down": "R", "up": "G", "flat": "grey"}[tr]] if tr != "flat" else T["grey"]))
        els.append(t)
        y += h + 6
        els.append(S.hline(x0, y - 3, xr, T["rule"], 0.5))
    els += C.legend(x0, y + 4, [("dot", "G", "On track"), ("dot", "A", "At risk, recoverable"),
                                ("dot", "R", "Off track, decision needed")])
    els += C.legend(x0 + 330, y + 4, [("down", T["R"], "Worse"), ("flat", T["grey"], "Unchanged"),
                                      ("up", T["G"], "Better")])
    hdr, ly = C.exhibit_header(x0, y + 26, xr - x0, "Look-ahead: key milestones in the next 90 days")
    els += hdr
    lc = [("Milestone", 250), ("Baseline", 80), ("Forecast", 80), ("Variance", 70), ("Status", 94)]
    cx = x0
    for name, w in lc:
        els.append(S.text(cx, ly, w - 6, C.r(name, **LBL)))
        cx += w
    ly += 14
    for ms, b, f, v, st in [("Signalling software drop 4 accepted", "30 Oct", "8 Nov", "+9 days", "R"),
                            ("Test windows confirmed by operator", "1 Nov", "14 Nov", "+13 days", "R"),
                            ("Station 3 fit-out complete", "12 Dec", "19 Dec", "+7 days", "A"),
                            ("Systems integration starts", "6 Jan", "6 Jan", "On plan", "G")]:
        cx = x0
        for (name, w), val in zip(lc, [ms, b, f, v, None]):
            if name == "Status":
                els += C.rag_pill(cx, ly + 2, st)
            else:
                els.append(S.text(cx, ly + 4, w - 6, r(val, 10, name == "Variance" and st == "R",
                                                        T["R"] if (name == "Variance" and st == "R") else None)))
            cx += w
        ly += 19
        els.append(S.hline(x0, ly, xr, T["rule"], 0.5))
    # Decisions box
    bx, bw = 630, 294
    box, iy = C.header_box(bx, 104, bw, bottom - 104 - 4, "Decisions needed from the SteerCo")
    els += box
    yy = iy
    for i, (what, owner, due) in enumerate([
            ("Approve £14m contingency drawdown for parallel systems integration", "SRO", "14 Nov"),
            ("Confirm the December possession plan with Network Rail", "Interface lead", "21 Nov"),
            ("Assign one owner for systems integration risk across client and contractor", "Commercial director", "30 Nov")], 1):
        els += C.callout(bx + 7, yy + 7, i)
        t = S.text(bx + 22, yy, bw - 22, r(what, 10.5, True), lh=1.3)
        els.append(t)
        yy += t["h"] + 3
        els.append(S.text(bx + 22, yy, bw - 22, [r("Owner: ", 9, True, T["grey"]), r(owner + "   ", 9, color=T["grey"]),
                                                  r("Due: ", 9, True, T["grey"]), r(due, 9, color=T["grey"])]))
        yy += 22
        if i < 3:
            els.append(S.hline(bx, yy - 8, bx + bw, T["rule"], 0.5))
    return {"els": els}


def s2_gantt():
    els, bottom = page(2, "Schedule", "Systems integration is now the critical path; handover holds only if test "
                       "windows are confirmed by 14 November",
                       footnotes=["Baseline is the Gate 3 re-baseline (March 2026). Float shown is total float on the "
                                  "Level 2 schedule."])
    hx, hw = 36, 600
    hdr, y = C.exhibit_header(hx, 104, hw, "Integrated schedule, baseline vs current forecast",
                              "Level 2 programme schedule, October 2026 to June 2027")
    els += hdr
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    x0, x1 = 186, 636
    mw = (x1 - x0) / len(months)
    for i, m in enumerate(months):
        els.append(S.rect(x0 + i * mw, y, mw - 1, 14, fill=T["tint"]))
        els.append(S.text(x0 + i * mw, y + 3, mw, r(m, 8, True, T["grey"]), align="c"))
    gy0 = y + 18
    rows = [("Main civils", "G", (0.0, 1.0), (0.0, 1.4), False),
            ("Track and OHLE", "G", (0.5, 3.0), (0.6, 3.2), False),
            ("Signalling install", "A", (1.2, 3.6), (1.5, 4.2), True),
            ("Systems integration", "R", (3.0, 5.6), (3.4, 6.5), True),
            ("Station fit-out", "A", (2.0, 5.0), (2.2, 5.4), False),
            ("Trial running", "A", (5.6, 6.6), (6.5, 7.5), True)]
    rh = 30
    for i, (name, rag, base, fc, crit) in enumerate(rows):
        yy = gy0 + i * rh
        els.append(C.rag_dot(hx + 6, yy + rh / 2, rag, 9))
        els.append(S.text(hx + 16, yy, 160, r(name, 10, crit), va="m", h=rh))
        els.append(S.rect(x0 + base[0] * mw, yy + 6, (base[1] - base[0]) * mw, 6, fill=None, line=T["mid"], lw=0.75))
        els.append(S.rect(x0 + fc[0] * mw, yy + 14, (fc[1] - fc[0]) * mw, 9,
                          fill=T["navy"] if crit else "#8FA6C4"))
        els.append(S.hline(hx, yy + rh, x1, T["rule"], 0.4))
    for i in range(1, len(months)):
        els.append(S.line(x0 + i * mw, gy0, x0 + i * mw, gy0 + len(rows) * rh + 34, T["rule"], 0.4, dash="dot"))
    my = gy0 + len(rows) * rh + 4
    els.append(S.text(hx + 16, my, 160, r("Handover milestone", 10, True), va="m", h=24))
    els.append(C.diamond(x0 + 6.1 * mw, my + 12, 10, T["mid"]))
    els.append(C.diamond(x0 + 7.5 * mw, my + 12, 11, T["navy"]))
    els.append(S.line(x0 + 6.1 * mw + 7, my + 12, x0 + 7.5 * mw - 8, my + 12, T["R"], 1, head="arrow"))
    els.append(S.text(x0 + 6.1 * mw - 50, my + 18, 100, r("3 Apr", 8, color=T["grey"]), align="c"))
    els.append(S.text(x0 + 7.5 * mw - 50, my + 18, 100, r("15 May", 8, True, T["navy"]), align="c"))
    tx = x0 + 1.03 * mw
    els.append(S.line(tx, gy0 - 4, tx, my + 30, T["R"], 1, dash="dash"))
    els.append(S.text(tx + 3, my + 22, 60, r("Today", 7.5, True, T["R"])))
    # float bracket on fit-out
    fy = gy0 + 4 * rh + 26
    els.append(S.line(x0 + 5.4 * mw, fy, x0 + 6.5 * mw, fy, T["G"], 1, head="arrow", tail="arrow"))
    els.append(S.text(x0 + 5.4 * mw, fy + 1, 1.1 * mw, r("5 wks float", 7.5, True, T["G"]), align="c"))
    els += C.callout(x0 + 6.5 * mw + 12, gy0 + 3 * rh + 18, 1)
    els += C.callout(x0 + 2.2 * mw - 12, gy0 + 4 * rh + 18, 2)
    els += C.callout(x0 + 7.5 * mw + 14, my + 12, 3)
    els += C.legend(hx, my + 36, [("outline", T["mid"], "Baseline"), ("bar", T["navy"], "Forecast, critical path"),
                                  ("bar", "#8FA6C4", "Forecast, other"), ("diamond", T["navy"], "Milestone"),
                                  ("dash", T["R"], "Today")])
    tk, _ = C.takeaways(650, 104, 274, [
        "Systems integration now drives handover. Its finish has slipped seven weeks, to late March.",
        "Station fit-out has five weeks of float, so it can move to make room for testing.",
        "The 15 May date holds only if the operator confirms test windows by 14 November."], title="What the schedule shows")
    els += tk
    nb, iy = C.header_box(650, _ + 14, 274, bottom - _ - 14, "Next steps")
    els += nb
    els.append(C.bullets(650, iy, 274, ["Operator to confirm test windows (14 Nov)",
                                         "Delivery partner to issue resequenced fit-out plan (21 Nov)",
                                         "PMO to re-run schedule risk analysis on the new logic (28 Nov)"], size=10))
    return {"els": els}


def s3_risk():
    els, bottom = page(3, "Risk", "Two risks moved into the red zone this period, and neither has a funded mitigation yet",
                       footnotes=["Score = likelihood x impact on a 5 x 5 scale. Red is 15 or more; amber 8 to 14; green 7 or less."])
    hdr, y = C.exhibit_header(36, 104, 286, "Top risks, current position", "Likelihood x impact, October 2026")
    els += hdr
    gx, c = 66, 47
    gy = y + 16
    els.append(S.text(36, y, 120, r("Likelihood", 8.5, True, T["grey"])))
    for li in range(5):
        for ii in range(5):
            L, I = 5 - li, ii + 1
            sc = L * I
            k = "R_t" if sc >= 15 else "A_t" if sc >= 8 else "G_t"
            els.append(S.rect(gx + ii * c, gy + li * c, c - 2, c - 2, fill=T[k]))
    for k in range(5):
        els.append(S.text(gx - 16, gy + k * c + 18, 10, r(str(5 - k), 8.5, color=T["grey"]), align="r"))
        els.append(S.text(gx + k * c, gy + 5 * c + 2, c - 2, r(str(k + 1), 8.5, color=T["grey"]), align="c"))
    els.append(S.text(gx, gy + 5 * c + 14, 5 * c, r("Impact", 9, True, T["grey"]), align="c"))

    def pos(L, I):
        return gx + (I - 1) * c + (c - 2) / 2, gy + (5 - L) * c + (c - 2) / 2

    moves = [("R07", (3, 4), (5, 4)), ("R12", (3, 3), (4, 4))]
    for rid, (pl, pi), (cl, ci) in moves:
        px, py = pos(pl, pi)
        cx, cy = pos(cl, ci)
        els.append(S.rect(px - 13, py - 8, 26, 16, fill=None, line=T["grey"], lw=0.75))
        els.append(S.line(px, py - 9, cx, cy + 9, T["ink"], 1, head="arrow"))
    for rid, L, I in [("R07", 5, 4), ("R12", 4, 4), ("R03", 3, 5), ("R18", 2, 3), ("R21", 3, 2)]:
        cx, cy = pos(L, I)
        if rid in ("R07", "R12"):
            cx += 0
        els.append(S.rect(cx - 14, cy - 8, 28, 16, fill=T["navy"]))
        els.append(S.text(cx - 14, cy - 8, 28, r(rid, 8, True, T["white"]), align="c", va="m", h=16))
    els += C.legend(36, gy + 5 * c + 32, [("bar", T["navy"], "Now"), ("outline", T["grey"], "Last period")])
    # table
    tx, tw = 342, 582
    cols = [("ID", 34), ("Risk", 196), ("Owner", 74), ("Score", 58), ("", 22), ("Mitigation and status", 198)]
    yy = 104
    els.append(S.rect(tx, yy, tw, 22, fill=T["navy"]))
    cx = tx
    for name, w in cols:
        els.append(S.text(cx + 6, yy, w - 10, r(name, 9, True, T["white"]), va="m", h=22))
        cx += w
    yy += 22
    data = [("R07", "Signalling software maturity: supplier missed drops 3 and 4", "S. Novak", "12 → 20", "up", "R",
             "Recovery plan due 8 Nov; independent code review proposed (unfunded)"),
            ("R12", "Christmas possessions: 3 of 5 weekends unconfirmed", "Interface lead", "9 → 16", "up", "R",
             "Escalated to Network Rail route director; decision 21 Nov"),
            ("R03", "Utilities diversion claims from main contractor", "R. Dube", "15 → 15", "flat", "R",
             "£6-9m exposure; valuation agreed, settlement talks under way"),
            ("R18", "Driver training capacity for trial running", "K. Ahmed", "6 → 6", "flat", "A",
             "Second simulator booked from January"),
            ("R21", "Late design changes at Station 3", "A. Silva", "9 → 6", "down", "G",
             "Design freeze agreed 15 Oct; change board in place")]
    for d in data:
        cells = [S.text(0, 0, cols[1][1] - 12, r(d[1], 9.5), lh=1.25), S.text(0, 0, cols[5][1] - 12, r(d[6], 9.5), lh=1.25)]
        h = max(c_["h"] for c_ in cells) + 10
        cx = tx
        els.append(S.text(cx + 6, yy + 5, 30, r(d[0], 9.5, True, T[d[5]] if d[5] != "A" else "#8A6100")))
        cx += cols[0][1]
        cells[0]["x"], cells[0]["y"] = cx + 6, yy + 5
        els.append(cells[0])
        cx += cols[1][1]
        els.append(S.text(cx + 6, yy + 5, cols[2][1] - 10, r(d[2], 9.5), lh=1.25))
        cx += cols[2][1]
        els.append(S.text(cx + 6, yy + 5, cols[3][1] - 10, r(d[3], 9.5, True)))
        cx += cols[3][1]
        els.append(C.trend(cx + 9, yy + 11, d[4], T["R"] if d[4] == "up" else T["G"] if d[4] == "down" else T["grey"], 8))
        cx += cols[4][1]
        cells[1]["x"], cells[1]["y"] = cx + 6, yy + 5
        els.append(cells[1])
        yy += h
        els.append(S.hline(tx, yy, tx + tw, T["rule"], 0.5))
    els += C.legend(tx, yy + 6, [("up", T["R"], "Score rising"), ("flat", T["grey"], "Unchanged"),
                                 ("down", T["G"], "Falling")])
    return {"els": els}


def s4_cost():
    els, bottom = page(4, "Cost", "Forecast cost has risen £40m since Gate 3, driven mostly by utilities and "
                       "signalling", footnotes=["Vertical axis starts at £1,300m.", "EAC = estimate at completion; "
                                                "excludes £12m of unquantified claims."])
    hdr, y = C.exhibit_header(36, 104, 600, "Bridge from Gate 3 budget to current forecast",
                              "£m, nominal, October 2026")
    els += hdr
    steps = [("Gate 3 budget", 1380, "total"), ("Utilities diversion", 22, "up"), ("Signalling", 15, "up"),
             ("Design changes", 9, "up"), ("Scope removed", -6, "down"), ("Current EAC", 1420, "total")]
    base_y, floor = bottom - 34, 1300
    scale = (base_y - (y + 40)) / (1430 - floor)
    x, bw, gap = 70, 66, 30
    tot, prev = 0, None
    centers = []
    for label, v, kind in steps:
        if kind == "total":
            top_v, bot_v, col = v, floor, T["navy"]
            tot = v
        else:
            bot_v, top_v = (tot, tot + v) if v > 0 else (tot + v, tot)
            col = T["R"] if v > 0 else T["G"]
            tot += v
        yt, yb = base_y - (top_v - floor) * scale, base_y - (bot_v - floor) * scale
        els.append(S.rect(x, yt, bw, yb - yt, fill=col))
        val = "{:,}".format(v) if kind == "total" else ("+%d" % v if v > 0 else "%d" % v)
        els.append(S.text(x - 12, yt - 15, bw + 24, r(val, 10, True), align="c"))
        els.append(S.text(x - 12, base_y + 5, bw + 24, r(label, 9, color=T["ink"]), align="c", lh=1.15))
        if prev is not None:
            els.append(S.line(x - gap, prev, x, prev, T["grey"], 0.5, dash="dot"))
        prev = base_y - (tot - floor) * scale
        centers.append((x + bw / 2, yt))
        x += bw + gap
    els.append(S.hline(56, base_y, x - gap + 14, T["ink"], 0.75))
    # total-change bracket
    yb = y + 18
    els.append(S.line(centers[0][0], yb, centers[-1][0], yb, T["navy"], 0.75))
    els.append(S.line(centers[0][0], yb, centers[0][0], centers[0][1] - 18, T["navy"], 0.75))
    els.append(S.line(centers[-1][0], yb, centers[-1][0], centers[-1][1] - 18, T["navy"], 0.75, head="arrow"))
    els.append(S.rect(centers[2][0] + 40, yb - 9, 104, 18, fill=T["white"], line=T["navy"], lw=0.75, shape="roundRect", radius=9))
    els.append(S.text(centers[2][0] + 40, yb - 9, 104, r("+£40m (+2.9%)", 9, True, T["navy"]), align="c", va="m", h=18))
    for n, k in [(1, 1), (2, 2), (3, 4)]:
        els += C.callout(centers[k][0] + bw / 2 + 9, centers[k][1] + 8, n)
    tk, _ = C.takeaways(650, 104, 274, [
        [r("Utilities added ", 10.5), r("£22m", 10.5, True), r(": the six-week overrun at Kings Cross and the contractor's prolongation claim.", 10.5)],
        [r("Signalling added ", 10.5), r("£15m", 10.5, True), r(" after two missed software drops.", 10.5)],
        [r("Deferring the Station 5 canopy saves ", 10.5), r("£6m", 10.5, True), r(", but the sponsor has not approved it.", 10.5)],
        [r("That leaves ", 10.5), r("£41m", 10.5, True), r(" of contingency, 3.0% of remaining work against a 5% floor.", 10.5)]], title="What drives the increase")
    els += tk
    nb, iy = C.header_box(650, _ + 14, 274, bottom - _ - 14, "Open points")
    els += nb
    els.append(C.bullets(650, iy, 274, ["£12m of unquantified claims sit outside the EAC",
                                         "Scope removal needs sponsor approval"], size=10))
    return {"els": els}


def s5_dashboard():
    els, bottom = page(5, "Workstreams", "Four of seven workstreams are on track; signalling and systems integration "
                       "need SteerCo decisions",
                       footnotes=["Green: on track. Amber: at risk but recoverable within tolerance. Red: outside "
                                  "tolerance, needs a decision. SPI and CPI are cumulative earned-value indices."])
    kp = [("activity", "Weeks behind baseline", "6", "Handover forecast 15 May 2027", "R"),
          ("calendar-check", "Schedule performance (SPI)", "0.91", "Down from 0.94 in September", "A"),
          ("coins", "Cost performance (CPI)", "0.97", "Stable for three periods", "A"),
          ("piggy-bank", "Contingency remaining", "£41m", "3.0% of remaining work; floor is 5%", "R")]
    w = 888 / 4
    for i, (ic, lab, val, sub, st) in enumerate(kp):
        els += C.kpi_card(36 + i * w + (14 if i else 0), 104, w, 72, ic, lab, val, sub, st)
        if i:
            els.append(S.line(36 + i * w, 106, 36 + i * w, 168, T["rule"], 0.75))
    cols = [("Workstream", 150), ("Lead", 90), ("Schedule", 62), ("Cost", 52), ("Risk", 52), ("Trend", 52),
            ("Key issue and next step", 430)]
    tx, yy = 36, 190
    els.append(S.rect(tx, yy, 888, 22, fill=T["navy"]))
    cx = tx
    for name, cw in cols:
        al = "c" if name in ("Schedule", "Cost", "Risk", "Trend") else "l"
        els.append(S.text(cx + 6, yy, cw - 12, r(name, 9, True, T["white"]), va="m", h=22, align=al))
        cx += cw
    yy += 22
    rows = [("Civils", "J. Patel", "G", "G", "A", "flat", "Complete; contractor claims being closed out"),
            ("Track and OHLE", "M. Okafor", "G", "A", "G", "flat", "Night-shift productivity 8% below plan; extra crew from Nov"),
            ("Signalling", "S. Novak", "R", "A", "R", "down", "Software drop 4 missed; recovery plan due 8 Nov"),
            ("Systems integration", "L. Chen", "R", "A", "R", "down", "Test windows not confirmed; decision needed 14 Nov"),
            ("Stations", "A. Silva", "A", "G", "A", "up", "Fit-out resequenced to protect float"),
            ("Operations readiness", "K. Ahmed", "G", "G", "G", "flat", "Driver training on plan"),
            ("Commercial", "R. Dube", "G", "A", "A", "flat", "Utilities claim valued at £6-9m")]
    rh = 30
    for i, row in enumerate(rows):
        cx = tx
        for (name, cw), val in zip(cols, row):
            if name in ("Schedule", "Cost", "Risk"):
                els.append(C.rag_dot(cx + cw / 2, yy + rh / 2, val, 10))
            elif name == "Trend":
                els.append(C.trend(cx + cw / 2, yy + rh / 2, val,
                                   T["R"] if val == "down" else T["G"] if val == "up" else T["grey"], 8))
            else:
                els.append(S.text(cx + 6, yy, cw - 12, r(val, 9.5, name == "Workstream"), va="m", h=rh))
            cx += cw
        yy += rh
        els.append(S.hline(tx, yy, tx + 888, T["rule"], 0.5))
    els.append(S.hline(tx, yy, tx + 888, T["navy"], 0.75))
    els += C.legend(tx, yy + 8, [("dot", "G", "On track"), ("dot", "A", "At risk"), ("dot", "R", "Off track"),
                                 ("up", T["G"], "Improving"), ("flat", T["grey"], "Stable"),
                                 ("down", T["R"], "Worsening")])
    return {"els": els}


def s6_options():
    els, bottom = page(6, "Options", "Option B scores highest overall; it costs £14m now but is the only option that "
                       "protects the May handover",
                       sowhat="Recommend Option B: approve £14m to run systems integration in parallel with fit-out",
                       footnotes=["Scores are the PMO's assessment with the delivery partner, reviewed by the client "
                                  "commercial team on 28 October. Weighted score out of 4."])
    chev = C.chevrons(36, 102, 600, 24, ["Long list (7)", "Screened (3)", "Evaluated", "Recommendation"], "Evaluated")
    els += chev
    crit = [("Protects May handover", "30%"), ("Cost to complete", "25%"), ("Deliverability", "20%"),
            ("Commercial risk", "15%"), ("Stakeholder support", "10%")]
    opts = [("A", "Re-baseline to Sept 2027", [1, 4, 3, 3, 1]), ("B", "Parallel integration (+£14m)", [4, 2, 3, 3, 3]),
            ("C", "Phased opening", [2, 3, 2, 1, 2])]
    x0, cw, y0 = 300, 112, 140
    els.append(S.rect(x0 + cw + 2, y0 - 4, cw - 4, 286, fill=None, line=T["navy"], lw=1.5))
    for j, (k, name, _) in enumerate(opts):
        els.append(S.text(x0 + j * cw + 8, y0, cw - 16, [r("Option %s\n" % k, 10, True, T["navy"]), r(name, 9, color=T["grey"])],
                          align="c", lh=1.2))
    els.append(S.text(220, y0 + 12, 70, r("Weight", 9, True, T["grey"]), align="c"))
    els.append(S.hline(36, y0 + 36, x0 + 3 * cw, T["navy"], 0.75))
    weights = [0.30, 0.25, 0.20, 0.15, 0.10]
    for i, (c_, wtxt) in enumerate(crit):
        y = y0 + 42 + i * 38
        els.append(S.text(36, y, 180, r(c_, 10.5), va="m", h=26))
        els.append(S.text(220, y, 70, r(wtxt, 10.5, color=T["grey"]), align="c", va="m", h=26))
        for j, (_, _, sc) in enumerate(opts):
            els.append(S.pie(x0 + j * cw + cw / 2 - 10, y + 3, 20, sc[i] * 90, fill=T["navy"], line=T["navy"], lw=1))
        els.append(S.hline(36, y + 32, x0 + 3 * cw, T["rule"], 0.5))
    y = y0 + 42 + 5 * 38
    els.append(S.text(36, y, 180, r("Weighted score", 10.5, True), va="m", h=26))
    for j, (_, _, sc) in enumerate(opts):
        tot = sum(a * b for a, b in zip(sc, weights))
        els.append(S.text(x0 + j * cw, y, cw, r("%.1f" % tot, 13, True, T["navy"] if j == 1 else T["ink"]), align="c",
                          va="m", h=26))
    els += C.legend(36, y + 34, [("harvey", 0, "Poor"), ("harvey", 1, ""), ("harvey", 2, ""), ("harvey", 3, ""),
                                 ("harvey", 4, "Strong")], size=8)
    box, iy = C.header_box(650, 104, 274, bottom - 104 - 4, "Rationale")
    els += box
    els.append(C.bullets(650, iy, 274, [
        "Only option that keeps the 15 May 2027 handover",
        "£14m is within remaining contingency, though it takes the balance below the 5% floor",
        ("Floor breach needs sponsor sign-off", 2),
        "Delivery partner has run parallel integration on two comparable schemes",
        "Option A is cheaper but slips revenue service by four months"], size=10.5))
    return {"els": els}


def main():
    slides = [s1_summary(), s2_gantt(), s3_risk(), s4_cost(), s5_dashboard(), s6_options()]
    hp, pp = run_spike.build(slides, "v1")
    ims = []
    worst = 0
    for i, (a, b) in enumerate(zip(hp, pp or []), 1):
        A, B = png.read(a).half(), png.read(b).half()
        ratio, heat = png.diff(A, B)
        png.write(png.side_by_side([A, B, heat]), os.path.join(run_spike.OUT, "v1-cmp-%02d.png" % i))
        worst = max(worst, ratio)
        ims.append(A)
        print("slide %d: %.3f%% differ" % (i, ratio * 100))
    if not pp:
        ims = [png.read(a).half() for a in hp]
    top, bot = png.side_by_side(ims[:3]), png.side_by_side(ims[3:])
    px = bytearray(top.px) + bytearray(b"\x90" * (top.w * 8 * 3)) + bot.px
    png.write(png.Image(top.w, top.h * 2 + 8, px), os.path.join(run_spike.OUT, "v1-sheet.png"))
    print("worst %.3f%%" % (worst * 100))


if __name__ == "__main__":
    main()
