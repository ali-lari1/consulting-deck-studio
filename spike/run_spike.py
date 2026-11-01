#!/usr/bin/env python3
"""M0 parity spike: build 6 hard slides as scenes, write HTML + PPTX, render both, diff them.

  python3 spike/run_spike.py calibrate   # fit first-baseline model for LibreOffice -> assets/calibration.json
  python3 spike/run_spike.py             # build + render + diff the 6 test slides
Outputs go to spike/out/.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "skills", "consulting-deck-studio", "scripts"))
from cdslib import png, render, write_html, write_pptx  # noqa: E402
from cdslib import scene as S  # noqa: E402
from cdslib.scene import run  # noqa: E402

OUT = os.path.join(ROOT, "spike", "out")
INK, GREY, RULE, ACC = "#1A1A1A", "#5B6B7F", "#C9CFD6", "#0B2545"
RAG = {"R": "#C0392B", "A": "#E0A100", "G": "#2E8540"}


def chrome(title, n, source="Source: Spike test data; illustrative only", tracker="PMO | Status"):
    els = [S.text(48, 22, 600, run(tracker.upper(), size=8, color=GREY, bold=True), tracking=0.6),
           S.text(48, 40, 864, run(title, font="Georgia", size=22, color=ACC), lh=1.15, max_lines=2, name="Title"),
           S.hline(48, 500, 912, RULE, 0.5),
           S.text(48, 508, 700, run(source, size=8, color=GREY)),
           S.text(812, 508, 100, run(str(n), size=8, color=GREY), align="r")]
    return els


def slide_text():
    els = chrome("The programme is two months behind its re-baselined date, and three decisions this month "
                 "decide whether it recovers", 1)
    y = 120
    for head, body in [
        ("Schedule.", "Main civils finished in August, six weeks late, because the utilities diversion at Kings Cross "
                      "took longer than planned. Systems integration can still recover four of those weeks if test "
                      "windows are confirmed by 14 November."),
        ("Cost.", "Forecast at completion is £1.42bn against a £1.38bn budget. The £40m gap is covered by remaining "
                  "contingency, but contingency would fall to 3% of remaining work, below the 5% floor set at Gate 3."),
        ("Risk.", "Two of the top ten risks moved up this period: signalling software maturity and possession "
                  "availability over Christmas. Both now sit in the red zone."),
        ("Decisions needed.", "Approve the £14m contingency drawdown; confirm the December possession plan; and agree "
                              "who owns the systems integration risk between the client and the main contractor."),
    ]:
        t = S.text(48, y, 560, [run(head + " ", bold=True, size=12), run(body, size=12)], lh=1.35)
        els.append(t)
        y += t["h"] + 12
    els.append(S.rect(640, 120, 272, 230, fill="#EEF1F4"))
    els.append(S.text(656, 136, 240, run("What we are asking for", bold=True, size=11, color=ACC)))
    els.append(S.text(656, 160, 240, run("Approval to draw £14m from programme contingency so that systems "
                                         "integration can run in parallel with fit-out from January.", size=11), lh=1.35))
    els.append(S.text(656, 280, 240, run("£14m", font="Georgia", size=40, color=ACC)))
    return {"els": els, "notes": "Dense-text parity test."}


def slide_gantt():
    els = chrome("Systems integration is now the critical path; fit-out has five weeks of float", 2,
                 tracker="PMO | Schedule")
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]
    x0, x1, top = 260, 900, 112
    mw = (x1 - x0) / len(months)
    for i, m in enumerate(months):
        els.append(S.text(x0 + i * mw, top, mw, run(m, size=9, color=GREY, bold=True), align="c"))
        els.append(S.line(x0 + i * mw, top + 16, x0 + i * mw, 470, RULE, 0.5))
    rows = [("Main civils", 0.0, 1.2, "#8A97A8", False), ("Track and OHLE", 0.6, 3.1, "#8A97A8", False),
            ("Signalling install", 1.5, 4.0, ACC, True), ("Systems integration", 3.0, 6.4, ACC, True),
            ("Station fit-out", 2.0, 5.2, "#8A97A8", False), ("Trial running", 6.4, 7.6, ACC, True),
            ("Handover", 7.6, 7.9, ACC, True)]
    y = top + 30
    for name, a, b, col, crit in rows:
        els.append(S.text(48, y + 4, 200, run(name, size=11, bold=crit)))
        els.append(S.rect(x0 + a * mw, y + 2, (b - a) * mw, 16, fill=col))
        els.append(S.hline(48, y + 36, x1, RULE, 0.25))
        y += 44
    tx = x0 + 1.2 * mw
    els.append(S.line(tx, top + 16, tx, 470, RAG["R"], 1.0, dash="dash"))
    els.append(S.text(tx + 4, 474, 80, run("Today", size=8, color=RAG["R"], bold=True)))
    for xm, label in [(x0 + 6.4 * mw, "Trial running starts"), (x0 + 7.9 * mw, "Handover")]:
        els.append(S.rect(xm - 5, 446, 10, 10, fill=ACC, shape="ellipse"))
        els.append(S.text(xm - 120, 430, 112, run(label, size=8, color=ACC), align="r"))
    return {"els": els}


def slide_heatmap():
    els = chrome("Two risks moved into the red zone this period; none moved out", 3, tracker="PMO | Risk")
    gx, gy, c = 120, 112, 64
    def col(l, i):
        s = l * i
        return "#C0392B" if s >= 15 else "#E0A100" if s >= 8 else "#2E8540" if s >= 4 else "#9BC5A4"
    for li in range(5):
        for ii in range(5):
            L, I = 5 - li, ii + 1
            els.append(S.rect(gx + ii * c, gy + li * c, c - 3, c - 3, fill=col(L, I)))
    for k in range(5):
        els.append(S.text(gx - 24, gy + k * c + 24, 16, run(str(5 - k), size=10, color=GREY), align="r"))
        els.append(S.text(gx + k * c, gy + 5 * c + 4, c - 3, run(str(k + 1), size=10, color=GREY), align="c"))
    els.append(S.text(gx, gy + 5 * c + 22, 5 * c, run("Impact", size=10, bold=True), align="c"))
    els.append(S.text(48, gy + 120, 50, run("Likeli-\nhood", size=10, bold=True)))
    for rid, L, I in [("R07", 5, 4), ("R12", 4, 4), ("R03", 3, 5), ("R18", 2, 3), ("R21", 3, 2)]:
        els.append(S.rect(gx + (I - 1) * c + 14, gy + (5 - L) * c + 18, 34, 22, fill="#FFFFFF", shape="roundRect", radius=4))
        els.append(S.text(gx + (I - 1) * c + 14, gy + (5 - L) * c + 23, 34, run(rid, size=9, bold=True), align="c"))
    els.append(S.line(gx + 3 * c + 31, gy + 2 * c + 40, gx + 3 * c + 31, gy + 1 * c + 40, INK, 1.25, head="arrow"))
    tx = 480
    y = 112
    for rid, txt in [("R07", "Signalling software maturity: supplier missed two drops; probability raised to 5."),
                     ("R12", "Christmas possessions: Network Rail has not confirmed 3 of 5 weekends."),
                     ("R03", "Utilities diversion claims: £6-9m exposure; with commercial team.")]:
        els.append(S.text(tx, y, 50, run(rid, size=11, bold=True, color=RAG["R"])))
        t = S.text(tx + 50, y, 380, run(txt, size=11), lh=1.3)
        els.append(t)
        y += t["h"] + 14
    return {"els": els}


def slide_waterfall():
    els = chrome("Forecast cost rose £40m since Gate 3, mostly from utilities and signalling", 4, tracker="PMO | Cost")
    steps = [("Gate 3 budget", 1380, "total"), ("Utilities", 22, "up"), ("Signalling", 15, "up"),
             ("Design changes", 9, "up"), ("Scope removed", -6, "down"), ("Efficiencies", -0, "skip"),
             ("Forecast (EAC)", 1420, "total")]
    steps = [s for s in steps if s[2] != "skip"]
    base_y, scale = 450, 1.4  # pt per £m above 1,200
    floor = 1200
    x = 90
    bw, gap = 88, 32
    run_total = 0
    prev_top = None
    for label, v, kind in steps:
        if kind == "total":
            top_v, bot_v, colr = v, floor, ACC
            run_total = v
        elif kind == "up":
            bot_v, top_v, colr = run_total, run_total + v, RAG["R"]
            run_total += v
        else:
            top_v, bot_v, colr = run_total, run_total + v, RAG["G"]
            run_total += v
        yt, yb = base_y - (top_v - floor) * scale, base_y - (bot_v - floor) * scale
        els.append(S.rect(x, yt, bw, yb - yt, fill=colr))
        val = "£%s" % ("{:,}".format(v) if kind == "total" else ("+%d" % v if v > 0 else "%d" % v)) + "m"
        els.append(S.text(x - 10, yt - 18, bw + 20, run(val, size=10, bold=True), align="c"))
        els.append(S.text(x - 10, base_y + 8, bw + 20, run(label, size=10, color=GREY), align="c", lh=1.2))
        if prev_top is not None:
            els.append(S.line(x - gap, prev_top, x, prev_top, GREY, 0.5, dash="dot"))
        prev_top = base_y - (run_total - floor) * scale
        x += bw + gap
    els.append(S.hline(70, base_y, x - gap + 20, INK, 0.75))
    els.append(S.text(48, 120, 300, run("Axis starts at £1.2bn", size=8, color=GREY, italic=True)))
    return {"els": els}


def slide_table():
    els = chrome("Four of seven workstreams are on track; signalling and systems need decisions", 5,
                 tracker="PMO | Dashboard")
    cols = [("Workstream", 190), ("Lead", 120), ("Schedule", 80), ("Cost", 80), ("Risk", 80), ("Comment", 314)]
    rows = [("Civils", "J. Patel", "G", "G", "A", "Complete; close-out of claims under way"),
            ("Track and OHLE", "M. Okafor", "G", "A", "G", "Night working rate below plan in October"),
            ("Signalling", "S. Novak", "R", "A", "R", "Software drop 4 missed; recovery plan due 8 Nov"),
            ("Systems integration", "L. Chen", "R", "A", "R", "Test windows not yet confirmed by operator"),
            ("Stations", "A. Silva", "A", "G", "A", "Fit-out sequence reworked to protect float"),
            ("Operations readiness", "K. Ahmed", "G", "G", "G", "Driver training on plan"),
            ("Commercial", "R. Dube", "G", "A", "A", "Utilities claim valued at £6-9m")]
    x, y = 48, 108
    els.append(S.rect(48, y, 864, 26, fill=ACC))
    for name, w in cols:
        els.append(S.text(x + 8, y + 7, w - 16, run(name, size=10, bold=True, color="#FFFFFF"),
                          align="c" if name in ("Schedule", "Cost", "Risk") else "l"))
        x += w
    y += 26
    for r in rows:
        x = 48
        for (name, w), val in zip(cols, r):
            if name in ("Schedule", "Cost", "Risk"):
                els.append(S.rect(x + w / 2 - 7, y + 9, 14, 14, fill=RAG[val], shape="ellipse"))
            else:
                els.append(S.text(x + 8, y + 9, w - 16, run(val, size=10, bold=(name == "Workstream"))))
            x += w
        y += 32
        els.append(S.hline(48, y, 912, RULE, 0.5))
    return {"els": els}


def slide_harvey():
    els = chrome("Option B scores best on deliverability and cost; Option C only wins on speed", 6,
                 tracker="Strategy | Options")
    crit = ["Cost to complete", "Deliverability", "Speed", "Commercial risk", "Stakeholder support"]
    opts = [("A: Re-baseline", [2, 2, 1, 3, 2]), ("B: Parallel integration", [3, 4, 3, 3, 3]),
            ("C: Phased opening", [1, 2, 4, 2, 1])]
    x0, y0 = 260, 112
    for j, (o, _) in enumerate(opts):
        els.append(S.text(x0 + j * 150, y0, 140, run(o, size=11, bold=True, color=ACC), align="c", lh=1.2))
    for i, c in enumerate(crit):
        y = y0 + 44 + i * 52
        els.append(S.text(48, y + 6, 200, run(c, size=11)))
        els.append(S.hline(48, y + 40, 710, RULE, 0.5))
        for j, (_, sc) in enumerate(opts):
            els.append(S.pie(x0 + j * 150 + 58, y, 24, sc[i] * 90, fill=INK, line=INK, lw=1.0))
    els.append(S.rect(740, 112, 172, 300, fill="#EEF1F4"))
    els.append(S.text(752, 124, 148, run("Recommendation", size=11, bold=True, color=ACC)))
    els.append(S.text(752, 146, 148, run("Take Option B. It costs £14m now but protects the May handover and keeps "
                                         "contingency above the floor.", size=11), lh=1.35))
    return {"els": els}


def build(slides, name):
    os.makedirs(OUT, exist_ok=True)
    html_path = os.path.join(OUT, name + ".html")
    open(html_path, "w", encoding="utf-8").write(write_html.document(slides, name, stacked=True))
    write_pptx.write(slides, os.path.join(OUT, name + ".pptx"), name)
    singles = []
    sdir = os.path.join(OUT, "single")
    os.makedirs(sdir, exist_ok=True)
    for i, s in enumerate(slides, 1):
        p = os.path.join(sdir, "%s-pptx-%02d.pptx" % (name, i))
        write_pptx.write([s], p, name)
        singles.append(p)
    hp = render.html_pngs(html_path, len(slides), OUT)
    pp = render.pptx_pngs(singles, OUT)
    return hp, pp


def calib_slides():
    """One slide per font: 'H' samples at several sizes and line pitches, each alone in a 150x90 cell."""
    out, cells = [], []
    for font in ["Arial", "Georgia"]:
        els = []
        k = 0
        for size in [8, 12, 18, 28, 40]:
            for lh in [1.0, 1.2, 1.5]:
                cx, cy = 20 + (k % 6) * 155, 20 + (k // 6) * 125
                t = S.text(cx, cy, 150, run("HHHH", font=font, size=size), lh=lh)
                els.append(t)
                cells.append((len(out), font, size, t["lh"], cx, cy))
                k += 1
        out.append({"els": els})
    return out, cells


def baseline_row(img, x, y, w, h):
    """Lowest pixel row (in output px) inside the window that has dark ink."""
    last = None
    for r in range(y, min(img.h, y + h)):
        row = img.px[(r * img.w + x) * 3:(r * img.w + x + w) * 3]
        if min(row) < 110:
            last = r
    return last


def calibrate():
    cal_path = write_pptx.CAL_PATH
    if os.path.exists(cal_path):
        os.remove(cal_path)  # fit against the uncalibrated default model
    write_pptx._cal = None
    slides, cells = calib_slides()
    hp, pp = build(slides, "calib")
    imgs_h = [png.read(p) for p in hp]
    imgs_p = [png.read(p) for p in pp]
    k = render.SCALE
    data = {}
    for si, font, size, lh, cx, cy in cells:
        win = (int(cx * k), int(cy * k), int(150 * k), int(118 * k))
        bh = baseline_row(imgs_h[si], *win)
        bp = baseline_row(imgs_p[si], *win)
        dy_used = write_pptx.html_baseline(font, size, lh) - write_pptx.pptx_baseline(font, size, lh)
        # PPTX box top was cy + dy_used; observed baseline offset from that top, in pt:
        obs = (bp + 1) / k - (cy + dy_used)
        html_obs = (bh + 1) / k - cy
        data.setdefault(font, []).append((lh, size, obs, html_obs, write_pptx.html_baseline(font, size, lh)))
    cal = {}
    for font, rows in data.items():
        # least squares: obs = a*lh + b*size
        s_ll = sum(r[0] * r[0] for r in rows); s_ls = sum(r[0] * r[1] for r in rows); s_ss = sum(r[1] * r[1] for r in rows)
        s_lo = sum(r[0] * r[2] for r in rows); s_so = sum(r[1] * r[2] for r in rows)
        det = s_ll * s_ss - s_ls * s_ls
        a = (s_lo * s_ss - s_so * s_ls) / det
        b = (s_ll * s_so - s_ls * s_lo) / det
        resid = max(abs(a * r[0] + b * r[1] - r[2]) for r in rows)
        html_err = max(abs(r[3] - r[4]) for r in rows)
        cal[font] = {"a": round(a, 5), "b": round(b, 5), "max_resid_pt": round(resid, 3),
                     "html_model_err_pt": round(html_err, 3), "renderer": "LibreOffice"}
        print("%-8s a=%.4f b=%.4f  fit resid<=%.2fpt  html-model err<=%.2fpt" % (font, a, b, resid, html_err))
        for r in rows:
            print("   lh=%5.2f size=%4.1f  pptx=%.2f  html=%.2f (model %.2f)" % (r[0], r[1], r[2], r[3], r[4]))
    json.dump(cal, open(cal_path, "w"), indent=1)
    print("wrote", cal_path)


def main():
    if sys.argv[1:] == ["calibrate"]:
        return calibrate()
    slides = [slide_text(), slide_gantt(), slide_heatmap(), slide_waterfall(), slide_table(), slide_harvey()]
    hp, pp = build(slides, "spike")
    if not pp:
        print("LibreOffice not found: HTML rendered, PPTX written, parity not measured.")
        return
    worst = 0
    for i, (a, b) in enumerate(zip(hp, pp), 1):
        A, B = png.read(a).half(), png.read(b).half()
        ratio, heat = png.diff(A, B)
        png.write(png.side_by_side([A, B, heat]), os.path.join(OUT, "cmp-%02d.png" % i))
        worst = max(worst, ratio)
        print("slide %d: %.3f%% pixels differ" % (i, ratio * 100))
    print("worst: %.3f%%" % (worst * 100))


if __name__ == "__main__":
    main()
