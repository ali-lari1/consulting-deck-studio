#!/usr/bin/env python3
"""Extract brand signals from a company website: name, description, colours, fonts, logo and image candidates.

Usage:
    python3 brand_from_url.py <url> [--out site.json] [--assets <dir>]

--assets downloads the best logo and the social image into <dir> (only from the site you pass).
Standard library only. The output is a set of suggestions: always confirm with the user before treating
it as the brand.
"""
import colorsys
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
MAX = 5 * 1024 * 1024
GENERIC_FONTS = {"sans-serif", "serif", "monospace", "system-ui", "-apple-system", "blinkmacsystemfont", "inherit",
                 "initial", "ui-sans-serif", "ui-serif", "ui-monospace", "segoe ui", "roboto", "helvetica neue", "arial",
                 "helvetica", "apple color emoji", "segoe ui emoji", "segoe ui symbol", "noto color emoji", "cursive",
                 "var", "unset", "emoji", "math", "fangsong", "times new roman", "courier new", "menlo", "monaco",
                 "consolas", "liberation mono", "sfmono-regular", "noto sans", "ubuntu", "cantarell", "fira sans",
                 "droid sans", "oxygen", "open sans"}


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read(MAX)
        if binary:
            return data, r.headers.get("Content-Type", "")
        enc = r.headers.get_content_charset() or "utf-8"
        return data.decode(enc, errors="ignore")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.links, self.imgs, self.styles, self.title = {}, [], [], [], ""
        self._in_title = self._in_style = False
        self.inline_svgs = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = (a.get("property") or a.get("name") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "title":
            self._in_title = True
        elif tag == "style":
            self._in_style = True
        elif tag == "svg":
            self.inline_svgs += 1
        if a.get("style"):
            self.styles.append(a["style"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_style:
            self.styles.append(data)


def norm_hex(h):
    h = h.lower().lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    return "#" + h[:6] if len(h) >= 6 else None


def rgb_to_hex(m):
    try:
        r, g, b = [int(float(x)) for x in m[:3]]
        return "#%02x%02x%02x" % (r, g, b)
    except Exception:
        return None


def classify(hexc):
    r, g, b = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.18 or l < 0.06 or l > 0.96:
        return "neutral", l
    return "chromatic", l


def colors_from_css(css):
    out = Counter()
    for m in re.finditer(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", css):
        h = norm_hex(m.group(0))
        if h:
            out[h] += 1
    for m in re.finditer(r"rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)", css):
        h = rgb_to_hex(m.groups())
        if h:
            out[h] += 1
    return out


def brand_vars(css):
    found = {}
    for m in re.finditer(r"--([\w-]*(?:brand|primary|accent|main|highlight)[\w-]*)\s*:\s*([^;}{]+)", css, re.I):
        val = m.group(2).strip()
        h = None
        hm = re.search(r"#([0-9a-fA-F]{3,8})\b", val)
        if hm:
            h = norm_hex(hm.group(0))
        else:
            rm = re.search(r"rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)", val)
            if rm:
                h = rgb_to_hex(rm.groups())
        if h:
            found["--" + m.group(1)] = h
    return found


def fonts_from_css(css):
    out = Counter()
    for m in re.finditer(r"font-family\s*:\s*([^;}{]+)", css, re.I):
        for fam in m.group(1).split(","):
            f = fam.strip().strip("'\"").strip()
            if f and f.lower() not in GENERIC_FONTS and not f.startswith("var(") and len(f) < 40:
                out[re.sub(r"\s*(fallback|Fallback)$", "", f)] += 1
    for m in re.finditer(r"@font-face\s*{[^}]*font-family\s*:\s*['\"]?([^;'\"]+)", css, re.I):
        out[m.group(1).strip()] += 2
    return out


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    url = argv[1]
    if not re.match(r"^https?://", url):
        url = "https://" + url
    out_path = argv[argv.index("--out") + 1] if "--out" in argv else None
    assets = argv[argv.index("--assets") + 1] if "--assets" in argv else None

    try:
        html = fetch(url)
    except Exception as e:
        print(json.dumps({"url": url, "error": str(e), "hint": "site blocked the fetch; read it with your browser tool"}))
        return 1
    p = Page()
    p.feed(html)
    base = url
    css_texts = list(p.styles)
    google_fonts, sheets = [], []
    for l in p.links:
        rel, href = l.get("rel", "").lower(), l.get("href", "")
        if "stylesheet" in rel and href:
            full = urllib.parse.urljoin(base, href)
            if "fonts.googleapis.com" in full:
                google_fonts += [urllib.parse.unquote_plus(f.split(":")[0]) for f in
                                 urllib.parse.parse_qs(urllib.parse.urlparse(full).query).get("family", [])]
            else:
                sheets.append(full)
    for s in sheets[:6]:
        try:
            css_texts.append(fetch(s))
        except Exception:
            pass
    css = "\n".join(css_texts)

    colors = colors_from_css(css)
    theme = p.meta.get("theme-color")
    if theme and theme.strip().startswith("#") and norm_hex(theme.strip()):
        colors[norm_hex(theme.strip())] += 50
    bvars = brand_vars(css)
    for h in bvars.values():
        colors[h] += 20
    chromatic, neutrals = [], []
    for h, n in colors.most_common(40):
        kind, l = classify(h)
        (chromatic if kind == "chromatic" else neutrals).append({"hex": h, "count": n, "lightness": round(l, 2)})

    fonts = fonts_from_css(css)
    for g in google_fonts:
        fonts[g] += 5

    icons, logos = [], []
    for l in p.links:
        rel = l.get("rel", "").lower()
        if "icon" in rel and l.get("href"):
            icons.append({"rel": rel, "href": urllib.parse.urljoin(base, l["href"]), "sizes": l.get("sizes", "")})
    for im in p.imgs:
        blob = " ".join([im.get("src", ""), im.get("alt", ""), im.get("class", ""), im.get("id", "")]).lower()
        src = im.get("src") or im.get("data-src") or ""
        if src and "logo" in blob:
            logos.append({"src": urllib.parse.urljoin(base, src), "alt": im.get("alt", "")})
    images = [urllib.parse.urljoin(base, im.get("src")) for im in p.imgs
              if im.get("src") and not im.get("src", "").startswith("data:")][:20]

    result = {
        "url": url,
        "title": p.title.strip(),
        "site_name": p.meta.get("og:site_name", ""),
        "description": p.meta.get("og:description") or p.meta.get("description", ""),
        "og_image": urllib.parse.urljoin(base, p.meta["og:image"]) if p.meta.get("og:image") else "",
        "theme_color": theme or "",
        "brand_css_vars": dict(list(bvars.items())[:24]),
        "colors_chromatic": chromatic[:8],
        "colors_neutral": neutrals[:8],
        "fonts": [f for f, _ in fonts.most_common(6)],
        "google_fonts": google_fonts,
        "logo_candidates": logos[:6],
        "icons": icons[:6],
        "inline_svgs": p.inline_svgs,
        "image_candidates": images,
        "notes": "Suggestions only. The accent is usually the most frequent chromatic colour or a --brand/--primary var. "
                 "If the logo is an inline SVG (inline_svgs > 0, no logo_candidates), ask the user for the file.",
    }

    if assets:
        os.makedirs(assets, exist_ok=True)
        targets = []
        if logos:
            targets.append(("logo", logos[0]["src"]))
        elif icons:
            best = sorted(icons, key=lambda i: ("apple-touch" in i["rel"], i["sizes"]), reverse=True)[0]
            targets.append(("icon", best["href"]))
        if result["og_image"]:
            targets.append(("og-image", result["og_image"]))
        saved = []
        for name, src in targets:
            try:
                data, ctype = fetch(src, binary=True)
                ext = {"image/svg+xml": ".svg", "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
                       "image/x-icon": ".ico", "image/vnd.microsoft.icon": ".ico"}.get(ctype.split(";")[0].strip(),
                                                                                         os.path.splitext(urllib.parse.urlparse(src).path)[1] or ".bin")
                path = os.path.join(assets, name + ext)
                with open(path, "wb") as f:
                    f.write(data)
                saved.append(path)
            except Exception as e:
                saved.append("failed %s: %s" % (src, e))
        result["downloaded"] = saved

    text = json.dumps(result, indent=2)
    if out_path:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote " + out_path)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
