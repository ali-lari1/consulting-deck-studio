#!/usr/bin/env python3
"""Regenerate skills/consulting-deck-studio/assets/metrics/*.json from fonts installed on this machine.

Only advance widths and vertical metrics are stored (facts about the font, not the font program).
Run on a machine with Arial and Georgia (macOS/Windows) or Liberation Sans and Gelasio (Linux).
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "skills", "consulting-deck-studio", "scripts"))
from cdslib import fonts  # noqa: E402

os.makedirs(fonts.METRICS_DIR, exist_ok=True)
# Extra families (e.g. fonts used by bundled examples): python3 tools/gen_metrics.py Verdana "Avenir Next"
for family in sys.argv[1:]:
    for style in ("regular", "bold", "italic", "bolditalic"):
        hit = fonts.locate(family, style)
        if not hit or hit[2] != family:
            print("skip %s %s (not installed)" % (family, style))
            continue
        m = fonts.metrics_from_ttf(hit[0], hit[1])
        out = os.path.join(fonts.METRICS_DIR, "%s-%s.json" % (family.replace(" ", ""), style))
        json.dump(m, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        print("%s %s <- %s" % (family, style, m["source"]))
if sys.argv[1:]:
    sys.exit(0)
for family, styles in fonts.FONT_FILES.items():
    for style in styles:
        src = fonts.find_font_file(family, style)
        if not src:
            print("skip %s %s (not installed)" % (family, style))
            continue
        m = fonts.metrics_from_ttf(src)
        out = os.path.join(fonts.METRICS_DIR, "%s-%s.json" % (family, style))
        json.dump(m, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        print("%s %s <- %s (%d glyphs)" % (family, style, m["source"], len(m["widths"])))
