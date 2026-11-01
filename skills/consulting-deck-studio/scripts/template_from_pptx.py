#!/usr/bin/env python3
"""Use a company template (.potx/.pptx) for a deck project.

Usage:
    python3 template_from_pptx.py <template.pptx|.potx> <project_dir> [--brand-only]

Copies the template into <project>/template/, reads its theme, fonts, layouts and placeholder grid, renders
each layout's graphics (logo, bars, fixed footer text) to template/chrome-<kind>.png for the HTML/PDF, and
writes <project>/brand.json. build.py then writes deck.pptx on the template's own masters and layouts.

--brand-only keeps the house layout grid and only takes colours and fonts (for 4:3 or unusual templates).
Needs LibreOffice for the chrome images; without it the PPTX is still fully on-template, but the HTML/PDF
show no template graphics (a warning says so).
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cdslib import fonts, render, template, write_pptx  # noqa: E402


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    src, project = argv[0], argv[1]
    brand_only = "--brand-only" in argv
    os.makedirs(os.path.join(project, "template"), exist_ok=True)
    dst = os.path.join(project, "template", os.path.basename(src))
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copy(src, dst)
    try:
        t = template.read(dst)
    except template.TemplateError as e:
        print("Template problem: %s" % e)
        return 1
    fonts.EXTRA_DIRS.insert(0, os.path.join(project, "fonts"))
    font_notes = []
    for role, fam in t["brand"]["fonts"].items():
        hit = fonts.locate(fam)
        if not hit:
            font_notes.append("MISSING  %s font '%s': put its .ttf/.otf files in %s/fonts/ (or install it), then re-run."
                              % (role, fam, project))
        elif hit[2] != fam:
            font_notes.append("STAND-IN %s font '%s' measured with metric-compatible '%s'. The PPTX still uses %s." % (
                role, fam, hit[2], fam))
        else:
            font_notes.append("ok       %s font '%s' (%s)" % (role, fam, os.path.basename(hit[0])))
    brand = {"mode": "brand" if brand_only else "template", "template": os.path.relpath(dst, project),
             "colors": t["brand"]["colors"], "fonts": t["brand"]["fonts"], "scheme": t["brand"]["scheme"]}
    if not brand_only:
        brand.update({"slide_size_pt": t["slide_size_pt"], "scale": t["scale"], "layouts": t["layouts"],
                      "layout_names": t["layout_names"], "grid": t["grid"], "slots": t["slots"], "chrome": {}})
        # render each layout's own graphics once, for the HTML/PDF background
        tmp = tempfile.mkdtemp(prefix="cds-chrome-")
        try:
            singles = []
            for kind in ("content", "title", "section", "blank"):
                p = os.path.join(tmp, "chrome-%s.pptx" % kind)
                write_pptx.write_template([{"els": [], "kind": kind}], p,
                                          {"path": dst, "layouts": t["layouts"], "scale": t["scale"]})
                singles.append(p)
            ff = [h[0] for h in (fonts.locate(f) for f in set(t["brand"]["fonts"].values())) if h]
            pngs = render.pptx_pngs(singles, tmp, font_files=ff)
            if pngs:
                for kind, pth in zip(("content", "title", "section", "blank"), pngs):
                    if os.path.exists(pth):
                        out = os.path.join(project, "template", "chrome-%s.png" % kind)
                        shutil.copy(pth, out)
                        brand["chrome"][kind] = os.path.relpath(out, project)
            else:
                t["warnings"].append("LibreOffice not found: deck.pptx will be on-template, but deck.html/pdf will not "
                                     "show the template's logo and graphics. Install LibreOffice and re-run this.")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    json.dump(brand, open(os.path.join(project, "brand.json"), "w", encoding="utf-8"), indent=1)
    print("Template: %s" % t["source"])
    print("  slide size %.2f x %.2f in, %s mode" % (t["slide_size_pt"][0] / 72, t["slide_size_pt"][1] / 72, brand["mode"]))
    print("  layouts: " + ", ".join("%s = '%s'" % kv for kv in t["layout_names"].items()))
    print("  colours: " + ", ".join("%s %s" % kv for kv in brand["colors"].items()))
    for n in font_notes:
        print("  " + n)
    for w in t["warnings"]:
        print("  WARN " + w)
    if t["has_slides"]:
        print("  note: the template's own sample slides are not copied into the deck")
    print("wrote %s" % os.path.join(project, "brand.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
