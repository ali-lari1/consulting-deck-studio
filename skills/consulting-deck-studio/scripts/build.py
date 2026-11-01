#!/usr/bin/env python3
"""Build a consulting deck: deck.md -> deck.html + deck.pptx (+ deck.pdf), with lint and parity checks.

Usage:
    python3 build.py <project_dir> [--pdf] [--parity] [--sheet] [--final] [--outline]

  <project_dir>/deck.md   authoring file (see references/layouts.md)
  --pdf      also export deck.pdf (headless Chromium)
  --parity   render PPTX (LibreOffice) and HTML (Chromium) per slide and compare; writes parity/cmp-NN.png
  --sheet    write contact-sheet.png
  --final    treat open [[placeholders]] as errors
  --outline  print the ghost deck (slide | layout | title) and stop
Exit code 1 if any slide failed to lay out or lint found errors. Standard library only.
"""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cdslib import components as C  # noqa: E402
from cdslib import calibrate, deckmd, fonts, lint, parity, render, write_html, write_pptx  # noqa: E402
from cdslib import layouts_more, layouts_pmo  # noqa: E402,F401  (register layouts)
from cdslib import scene as S  # noqa: E402
from cdslib.components import T, r  # noqa: E402
from cdslib.layouts import LAYOUTS  # noqa: E402


def error_slide(slide, ctx, msg):
    try:
        els, _ = C.frame(slide["title"], ctx["page"], None, None, ctx["meta"].get("context"))
    except S.LayoutError:
        words = slide["title"].split()
        els, _ = C.frame(" ".join(words[:8]) + " ...", ctx["page"], None, None, ctx["meta"].get("context"))
    els.append(S.rect(36, 120, 888, 120, fill="#FDECEA", line=T["R"]))
    els.append(S.text(52, 136, 856, [r("Layout error: ", 12, True, T["R"]), r(msg, 12)], lh=1.35))
    return els


KIND = {"title": "title", "section": "section"}


def load_brand(project):
    """Apply brand.json (template, brand or house). Returns (brand dict or None, tpl for the PPTX writer or None)."""
    fonts.EXTRA_DIRS[:] = [os.path.join(project, "fonts")]
    C.apply_brand({})
    C.set_grid(C.Grid())
    p = os.path.join(project, "brand.json")
    if not os.path.exists(p):
        return None, None
    b = json.load(open(p, encoding="utf-8"))
    C.apply_brand(b)
    tpl = None
    if b.get("logo") and b.get("mode") != "template":
        lp = os.path.join(project, b["logo"]["path"])
        mime = "jpeg" if lp.lower().endswith((".jpg", ".jpeg")) else "png"
        h = 20.0
        w = h * b["logo"]["aspect"]
        C.G.logo = {"src": "data:image/%s;base64,%s" % (mime, base64.b64encode(open(lp, "rb").read()).decode()), "w": w, "h": h}
        C.G.keepout = [[C.G.R - w, C.G.tracker_y - 4, w, h]]
    if b.get("mode") == "template":
        C.set_grid(C.Grid(scale=b["scale"], **b["grid"]))
        tpl = {"path": os.path.join(project, b["template"]), "layouts": b["layouts"], "scale": b["scale"]}
    return b, tpl


def chrome_image(project, brand, kind):
    rel = (brand or {}).get("chrome", {}).get(kind)
    if not rel or not os.path.exists(os.path.join(project, rel)):
        return None
    data = base64.b64encode(open(os.path.join(project, rel), "rb").read()).decode("ascii")
    return {"t": "image", "x": 0, "y": 0, "w": 960, "h": 540, "src": "data:image/png;base64," + data, "html_only": True}


def build(project, pdf=False, do_parity=False, do_sheet=False, final=False, outline=False):
    src = os.path.join(project, "deck.md")
    meta, slides = deckmd.parse(open(src, encoding="utf-8").read())
    brand, tpl = load_brand(project)
    cal_cache = os.path.join(project, ".cds", "calibration.json")
    write_pptx._cal = None
    write_pptx.load_extra_calibration(cal_cache)
    fams = {T["font"], T["title_font"]}
    if (do_parity or os.environ.get("CDS_CALIBRATE")) and render.find_soffice():
        done = calibrate.fit(sorted(fams), cal_cache)
        if done:
            print("calibrated baseline for: %s" % ", ".join(done))
    if outline:
        print("%-3s %-16s %s" % ("#", "layout", "action title"))
        for n, s in enumerate(slides, 1):
            print("%-3d %-16s %s" % (n, s["layout"], s["title"]))
        return 0
    findings = lint.lint(meta, slides, final)
    scenes = []
    for s in slides:
        if s.get("data_from"):
            for spec in s["data_from"].split(","):
                spec = spec.strip()
                path, _, key = spec.partition(" as ")
                fp = os.path.join(project, path.strip())
                if not os.path.exists(fp):
                    findings.append(("error", slides.index(s) + 1, "data_from file not found: %s (run ingest.py --refresh)" % path))
                    continue
                ext = {k: v for k, v in json.load(open(fp, encoding="utf-8")).items() if not k.startswith("_")}
                if key.strip():
                    s["data"].setdefault(key.strip(), ext)
                else:
                    s["data"] = dict(ext, **s["data"])
    for n, s in enumerate(slides, 1):
        ctx = {"meta": meta, "page": n, "total": len(slides), "slots": (brand or {}).get("slots") if tpl else None}
        kind = KIND.get(s["layout"], "content")
        f = LAYOUTS.get(s["layout"])
        C.FIT_LOG[:] = []
        try:
            if not f:
                raise S.LayoutError("unknown layout '%s' (known: %s)" % (s["layout"], ", ".join(sorted(LAYOUTS))))
            els = f(s, ctx)
        except fonts.FontMissing as e:
            print("ERROR %s" % e)
            return 1
        except (S.LayoutError, KeyError, IndexError, TypeError, ValueError) as e:
            msg = str(e) if isinstance(e, S.LayoutError) else "%s: %s (check the data block)" % (type(e).__name__, e)
            findings.append(("error", n, msg))
            els = error_slide(s, ctx, msg)
        for _, a, b in C.FIT_LOG:
            findings.append(("warn", n, "title stepped down from %.0f to %.0fpt to fit two lines; consider shortening it" % (
                a * (tpl["scale"] if tpl else 1), b * (tpl["scale"] if tpl else 1))))
        if s["layout"] not in ("title", "section", "agenda") and not any(f[0] == "error" and f[1] == n for f in findings):
            body = [e for e in els if e.get("name") not in ("Title", "Page") and e.get("y", 0) > C.G.top - 1 and
                    e.get("y", 0) < C.G.foot_y - 30 and e["t"] != "image"]
            if body:
                low = max(e["y"] + e.get("h", 0) for e in body if "h" in e)
                avail = C.G.foot_y - 40 - C.G.top
                if (low - C.G.top) < 0.5 * avail:
                    findings.append(("info", n, "slide is more than half empty; consider a richer exhibit, merging it with "
                                                "another slide, or moving it to the appendix"))
        bgimg = chrome_image(project, brand, kind) if tpl else None
        scenes.append({"els": ([bgimg] if bgimg else []) + els, "notes": s.get("notes", ""), "kind": kind})
    title = meta.get("deck", "Deck")
    page_in = tuple(v / 72.0 for v in brand["slide_size_pt"]) if tpl else (13.333, 7.5)
    open(os.path.join(project, "deck.html"), "w", encoding="utf-8").write(write_html.viewer(scenes, title, page_in))
    if tpl:
        write_pptx.write_template(scenes, os.path.join(project, "deck.pptx"), tpl, title)
        print("template: %s (layouts: %s)" % (os.path.basename(tpl["path"]), ", ".join(
            "%s='%s'" % kv for kv in brand.get("layout_names", {}).items())))
    else:
        write_pptx.write(scenes, os.path.join(project, "deck.pptx"), title, T["title_font"], T["font"])
    print("built %d slides -> deck.html, deck.pptx" % len(scenes))
    if pdf:
        render.pdf(os.path.join(project, "deck.html"), os.path.join(project, "deck.pdf"))
        print("-> deck.pdf")
    if do_sheet:
        parity.sheet(scenes, os.path.join(project, "contact-sheet.png"))
        print("-> contact-sheet.png")
    if do_parity:
        res = parity.check(scenes, project, title, tpl)
        if res is None:
            print("parity: LibreOffice not found; skipped (install it, or check deck.pptx by eye in PowerPoint)")
        else:
            for n, ratio in res:
                lvl = "error" if ratio > 0.03 else "ok"
                if lvl == "error":
                    findings.append(("error", n, "PPTX differs from HTML on %.1f%% of pixels; see parity/cmp-%02d.png" % (ratio * 100, n)))
            print("parity: worst %.2f%% of pixels differ (threshold 3%%)" % (max(x[1] for x in res) * 100))
    findings += lint.deck_rules(meta, slides)
    order = {"error": 0, "warn": 1, "info": 2}
    for lvl, n, msg in sorted(findings, key=lambda x: (order[x[0]], x[1])):
        if lvl != "info" or os.environ.get("CDS_VERBOSE"):
            print("%-5s %s %s" % (lvl.upper(), ("slide %-2d" % n) if n else "deck    ", msg))
    import re as _re
    ph = sorted({m for s_ in slides for m in _re.findall(r"\[\[[^\]]+\]\]", json.dumps(s_, ensure_ascii=False))})
    if ph:
        print("open placeholders (%d): %s%s" % (len(ph), ", ".join(ph[:12]), " ..." if len(ph) > 12 else ""))
    empties = [f[1] for f in findings if f[0] == "info" and "half empty" in f[2]]
    if empties:
        print("note: slides %s are more than half empty" % ", ".join(str(x) for x in empties))
    errs = sum(1 for f in findings if f[0] == "error")
    warns = sum(1 for f in findings if f[0] == "warn")
    print("%d error(s), %d warning(s)" % (errs, warns))
    return 1 if errs else 0


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    flags = set(argv[1:])
    return build(argv[0], "--pdf" in flags, "--parity" in flags, "--sheet" in flags, "--final" in flags,
                 "--outline" in flags)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
