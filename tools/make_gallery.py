#!/usr/bin/env python3
"""Build the deck-type gallery: docs/images/gallery/<example>.png (up to 6 slides per deck) and docs/gallery.md.

Run after building each example with --sheet:  python3 tools/make_gallery.py
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "skills", "consulting-deck-studio", "scripts"))
from cdslib import png  # noqa: E402

# (example folder, practice, deck type, one-line description, slide numbers to show or None for the first 6)
DECKS = [
    ("northline-monthly", "PMO", "Monthly status report (built from project files)",
     "Built from the programme's own P6 schedule, risk register, RAID log and benefits register, compared with last month.", None),
    ("northline-rail-steerco", "PMO", "SteerCo pack",
     "Decisions first, then status, schedule, risk, cost, workstreams and recovery options.", [3, 4, 6, 7, 10, 14]),
    ("assurance-review", "PMO", "Assurance / IV&V health check", "Ratings by area, significant findings with management responses, recommendation tracker.", None),
    ("risk-review", "PMO", "Risk review", "Heat map with movement, mitigation options for the top risk, sensitivity, RAID.", None),
    ("gate-paper", "Capital projects", "Gate 3 investment decision paper", "Stage gates, options, cost build-up with estimate class, QRA confidence, the resolution.", None),
    ("independent-review", "Capital projects", "Independent cost and schedule review", "Project view against the review's view of cost and date, findings by severity.", None),
    ("market-entry", "Strategy", "Market entry", "Market sizing, where to play, entry mode options and the recommendation.", None),
    ("growth-strategy", "Strategy", "Growth strategy", "Momentum against ambition, the revenue bridge by initiative, options and roadmap.", None),
    ("meridian-cost-review", "Management + capital", "Diagnostic, savings plan and capital programme",
     "Issue and driver trees, benchmark, Marimekko, quotes, roadmap, benefits, S-curve, P-curve, tornado.", [3, 4, 5, 6, 16, 17]),
    ("operating-model", "Management", "Operating model and org design", "Design principles, today against target, structure, decision rights, transition roadmap.", None),
    ("post-merger-integration", "Management", "Post-merger integration plan", "Day 1 and Day 100, must-haves, synergies by type, integration office.", None),
    ("template-demo", "Any", "The same SteerCo pack on a client template", "Built on the client's own master, layouts, fonts and colours.", [1, 3, 6, 7, 8, 14]),
]


def slide(sheet, k):
    return sheet.crop(((k - 1) % 3) * 968, ((k - 1) // 3) * 548, 960, 540).half()


def main():
    out_dir = os.path.join(ROOT, "docs", "images", "gallery")
    os.makedirs(out_dir, exist_ok=True)
    md = ["# Gallery: one example per deck type", "",
          "Every deck below was built by the skill from a fictional brief or fictional project files, and renders "
          "identically as PPTX, HTML and PDF. The source `deck.md` and the PPTX/PDF for each are in "
          "[`examples/`](../examples). Images show up to six slides of each deck.", ""]
    done = 0
    for ex, practice, kind, desc, picks in DECKS:
        cs = os.path.join(ROOT, "examples", ex, "contact-sheet.png")
        if not os.path.exists(cs):
            print("skip %s (no contact sheet; build it with --sheet)" % ex)
            continue
        sheet = png.read(cs)
        n = (sheet.h + 8) // 548 * 3
        ks = picks or list(range(1, 7))
        ims = []
        for k in ks:
            if ((k - 1) // 3) * 548 + 540 <= sheet.h and ((k - 1) % 3) * 968 + 960 <= sheet.w:
                im = slide(sheet, k)
                if any(v < 250 for v in im.px[::997]):
                    ims.append(im)
        rows = [png.side_by_side(ims[i:i + 3], 8) for i in range(0, len(ims), 3)]
        W = max(r.w for r in rows)
        px = bytearray()
        for i, r in enumerate(rows):
            if r.w < W:
                pad = bytearray(b"\xff" * ((W - r.w) * 3))
                line = bytearray()
                for y in range(r.h):
                    line += r.px[y * r.w * 3:(y + 1) * r.w * 3] + pad
                r = png.Image(W, r.h, line)
            px += r.px
            if i < len(rows) - 1:
                px += bytearray(b"\xff" * (W * 8 * 3))
        H = sum(r.h for r in rows) + 8 * (len(rows) - 1)
        png.write(png.Image(W, H, px), os.path.join(out_dir, ex + ".png"))
        md += ["## %s: %s" % (practice, kind), "", desc, "",
               "![%s](images/gallery/%s.png)" % (kind, ex), "",
               "Source: [`examples/%s/deck.md`](../examples/%s/deck.md) | [PDF](../examples/%s/deck.pdf) | [PPTX](../examples/%s/deck.pptx)" % (ex, ex, ex, ex), ""]
        done += 1
    open(os.path.join(ROOT, "docs", "gallery.md"), "w", encoding="utf-8").write("\n".join(md))
    print("gallery: %d decks -> docs/gallery.md, docs/images/gallery/" % done)


if __name__ == "__main__":
    main()
