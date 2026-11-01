#!/usr/bin/env python3
"""Create <project>/brand.json from a website scan and/or explicit choices (no template available).

Usage:
    python3 brand_init.py <project> [--site <project>/research/site.json] [--primary #0B2545] [--secondary #2F5D9A]
                          [--heading-font "Font"] [--body-font "Font"] [--logo path.png]

Order of preference: explicit flags > site scan (brand_from_url.py) > house style. Colours too light for titles
are darkened (and reported). Fonts must be installed or supplied in <project>/fonts/, otherwise Arial is used
and the script says so. Logos must be PNG or JPEG (export SVG logos to PNG first).
"""
import json
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cdslib import fonts  # noqa: E402
from cdslib.components import blend  # noqa: E402


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def image_size(path):
    d = open(path, "rb").read(65536)
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", d[16:24])
    if d[:2] == b"\xff\xd8":
        i = 2
        while i < len(d):
            if d[i] != 0xFF:
                i += 1
                continue
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", d[i + 5:i + 9])
                return w, h
            i += 2 + struct.unpack(">H", d[i + 2:i + 4])[0]
    raise SystemExit("logo must be PNG or JPEG: %s" % path)


def arg(argv, k):
    return argv[argv.index(k) + 1] if k in argv else None


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    project = argv[0]
    fonts.EXTRA_DIRS.insert(0, os.path.join(project, "fonts"))
    notes = []
    site = {}
    sp = arg(argv, "--site")
    if sp and os.path.exists(sp):
        site = json.load(open(sp, encoding="utf-8"))
    primary = arg(argv, "--primary")
    if not primary and site:
        vars_ = site.get("brand_css_vars", {})
        for k, v in vars_.items():
            if any(w in k.lower() for w in ("primary", "brand", "accent")) and str(v).startswith("#") and len(v) == 7:
                primary = v
                break
        primary = primary or site.get("theme_color") or (site.get("colors_chromatic") or [None])[0]
    secondary = arg(argv, "--secondary") or ((site.get("colors_chromatic") or [None, None])[1:2] or [None])[0]
    colors = {}
    if primary:
        p = primary if primary.startswith("#") else "#" + primary
        if len(p) == 4:
            p = "#" + "".join(c * 2 for c in p[1:])
        orig = p
        while lum(p) > 0.40:
            p = blend(p, "#000000", 0.12)
        if p != orig:
            notes.append("primary %s is too light for titles on white; darkened to %s (keep %s as secondary)" % (orig, p, orig))
            secondary = secondary or orig
        colors["primary"] = p.upper()
    if secondary:
        colors["secondary"] = (secondary if secondary.startswith("#") else "#" + secondary).upper()
    fonts_out = {}
    cands = [arg(argv, "--heading-font"), arg(argv, "--body-font")] + list(site.get("fonts", []))
    for role, fam in (("heading", arg(argv, "--heading-font")), ("body", arg(argv, "--body-font"))):
        choice = fam
        if not choice:
            for c in site.get("fonts", []):
                if fonts.locate(c.strip("'\" ")):
                    choice = c.strip("'\" ")
                    break
        if choice and not fonts.locate(choice):
            notes.append("%s font '%s' is not installed here; using Arial. Put the .ttf/.otf files in %s/fonts/ "
                         "and re-run to use it." % (role, choice, project))
            choice = None
        if choice:
            fonts_out[role] = choice
    if "heading" in fonts_out and "body" not in fonts_out:
        fonts_out["body"] = fonts_out["heading"]
    brand = {"mode": "brand", "colors": colors, "fonts": fonts_out}
    logo = arg(argv, "--logo")
    if logo:
        os.makedirs(os.path.join(project, "assets"), exist_ok=True)
        dst = os.path.join(project, "assets", "logo" + os.path.splitext(logo)[1].lower())
        shutil.copy(logo, dst)
        w, h = image_size(dst)
        brand["logo"] = {"path": os.path.relpath(dst, project), "aspect": round(w / float(h), 4)}
    json.dump(brand, open(os.path.join(project, "brand.json"), "w", encoding="utf-8"), indent=1)
    print("brand.json: colours %s, fonts %s%s" % (colors or "house", fonts_out or "house (Arial)",
                                                    ", logo " + brand["logo"]["path"] if logo else ""))
    for n in notes:
        print("  note: " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
