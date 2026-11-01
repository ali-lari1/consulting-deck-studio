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
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cdslib import components as C  # noqa: E402
from cdslib import deckmd, lint, parity, render, write_html, write_pptx  # noqa: E402
from cdslib import layouts_pmo  # noqa: E402,F401  (registers PMO layouts)
from cdslib import scene as S  # noqa: E402
from cdslib.components import T, r  # noqa: E402
from cdslib.layouts import LAYOUTS  # noqa: E402


def error_slide(slide, ctx, msg):
    els, _ = C.frame(slide["title"], ctx["page"], None, None, ctx["meta"].get("context"))
    els.append(S.rect(36, 120, 888, 120, fill="#FDECEA", line=T["R"]))
    els.append(S.text(52, 136, 856, [r("Layout error: ", 12, True, T["R"]), r(msg, 12)], lh=1.35))
    return els


def build(project, pdf=False, do_parity=False, do_sheet=False, final=False, outline=False):
    src = os.path.join(project, "deck.md")
    meta, slides = deckmd.parse(open(src, encoding="utf-8").read())
    if outline:
        print("%-3s %-16s %s" % ("#", "layout", "action title"))
        for n, s in enumerate(slides, 1):
            print("%-3d %-16s %s" % (n, s["layout"], s["title"]))
        return 0
    findings = lint.lint(meta, slides, final)
    scenes = []
    for n, s in enumerate(slides, 1):
        ctx = {"meta": meta, "page": n, "total": len(slides)}
        f = LAYOUTS.get(s["layout"])
        try:
            if not f:
                raise S.LayoutError("unknown layout '%s' (known: %s)" % (s["layout"], ", ".join(sorted(LAYOUTS))))
            els = f(s, ctx)
        except (S.LayoutError, KeyError, IndexError, TypeError, ValueError) as e:
            msg = str(e) if isinstance(e, S.LayoutError) else "%s: %s (check the data block)" % (type(e).__name__, e)
            findings.append(("error", n, msg))
            els = error_slide(s, ctx, msg)
        scenes.append({"els": els, "notes": s.get("notes", "")})
    title = meta.get("deck", "Deck")
    open(os.path.join(project, "deck.html"), "w", encoding="utf-8").write(write_html.viewer(scenes, title))
    write_pptx.write(scenes, os.path.join(project, "deck.pptx"), title)
    print("built %d slides -> deck.html, deck.pptx" % len(scenes))
    if pdf:
        render.pdf(os.path.join(project, "deck.html"), os.path.join(project, "deck.pdf"))
        print("-> deck.pdf")
    if do_sheet:
        parity.sheet(scenes, os.path.join(project, "contact-sheet.png"))
        print("-> contact-sheet.png")
    if do_parity:
        res = parity.check(scenes, project, title)
        if res is None:
            print("parity: LibreOffice not found; skipped (install it, or check deck.pptx by eye in PowerPoint)")
        else:
            for n, ratio in res:
                lvl = "error" if ratio > 0.03 else "ok"
                if lvl == "error":
                    findings.append(("error", n, "PPTX differs from HTML on %.1f%% of pixels; see parity/cmp-%02d.png" % (ratio * 100, n)))
            print("parity: worst %.2f%% of pixels differ (threshold 3%%)" % (max(x[1] for x in res) * 100))
    order = {"error": 0, "warn": 1, "info": 2}
    for lvl, n, msg in sorted(findings, key=lambda x: (order[x[0]], x[1])):
        if lvl != "info" or os.environ.get("CDS_VERBOSE"):
            print("%-5s slide %-2d %s" % (lvl.upper(), n, msg))
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
