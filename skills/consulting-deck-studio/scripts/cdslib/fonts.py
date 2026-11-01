"""Font metrics for deterministic text layout.

Layout never asks a renderer how wide text is. It uses advance widths from bundled metric tables
(assets/metrics/*.json), generated once from the real fonts by tools/gen_metrics.py. Arial and Georgia
have metric-compatible open equivalents (Liberation Sans, Gelasio), so the same line breaks hold on
macOS, Windows, Linux and in PowerPoint, Keynote, LibreOffice and Chromium. Standard library only.
"""
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
METRICS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "metrics"))

# Family -> style -> font file names searched on this machine (first hit wins). Used for metric
# generation and to embed real font paths in HTML @font-face (local() first).
FONT_FILES = {
    "Arial": {
        "regular": ["Arial.ttf", "arial.ttf", "LiberationSans-Regular.ttf"],
        "bold": ["Arial Bold.ttf", "arialbd.ttf", "LiberationSans-Bold.ttf"],
        "italic": ["Arial Italic.ttf", "ariali.ttf", "LiberationSans-Italic.ttf"],
        "bolditalic": ["Arial Bold Italic.ttf", "arialbi.ttf", "LiberationSans-BoldItalic.ttf"],
    },
    "Georgia": {
        "regular": ["Georgia.ttf", "georgia.ttf", "Gelasio-Regular.ttf"],
        "bold": ["Georgia Bold.ttf", "georgiab.ttf", "Gelasio-Bold.ttf"],
        "italic": ["Georgia Italic.ttf", "georgiai.ttf", "Gelasio-Italic.ttf"],
        "bolditalic": ["Georgia Bold Italic.ttf", "georgiaz.ttf", "Gelasio-BoldItalic.ttf"],
    },
}
FONT_DIRS = ["/System/Library/Fonts/Supplemental", "/System/Library/Fonts", "/Library/Fonts",
             os.path.expanduser("~/Library/Fonts"), r"C:\Windows\Fonts",
             "/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/liberation2",
             "/usr/share/fonts/liberation", "/usr/share/fonts/truetype/gelasio", os.path.expanduser("~/.fonts")]


# Metric-compatible open stand-ins: same advance widths, so line breaks hold when the brand font is missing.
STAND_INS = {"Calibri": "Carlito", "Cambria": "Caladea", "Arial": "Liberation Sans", "Helvetica": "Liberation Sans",
             "Helvetica Neue": "Liberation Sans", "Times New Roman": "Liberation Serif", "Courier New": "Liberation Mono",
             "Georgia": "Gelasio", "Segoe UI": "Selawik"}
EXTRA_DIRS = []   # project font folders, added by build.py
_INDEX = None


def font_index():
    """{(family_lower, style): (path, face_index)} for every font file in the known folders."""
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    idx = {}
    for d in EXTRA_DIRS + FONT_DIRS + ["/System/Library/Fonts/Supplemental", os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts"),
                                       "/usr/share/fonts", "/usr/local/share/fonts"]:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for fn in files:
                if not fn.lower().endswith((".ttf", ".otf", ".ttc")):
                    continue
                p = os.path.join(root, fn)
                try:
                    data = open(p, "rb").read()
                    for k in range(len(ttc_offsets(data))):
                        t = TTF(p, k, data)
                        fam, sub = t.names()
                        if not fam or "glyf" not in t.tables and "CFF " not in t.tables:
                            continue
                        key = (fam.lower(), style_key(t.bold, t.italic))
                        idx.setdefault(key, (p, k))
                except Exception:
                    continue
    _INDEX = idx
    return idx


def locate(family, style="regular"):
    """Path, face index and the family actually used (the brand font or its stand-in), or None."""
    for fam in [family, STAND_INS.get(family)]:
        if not fam:
            continue
        hit = font_index().get((fam.lower(), style)) or (font_index().get((fam.lower(), "regular")) if style != "regular" else None)
        if hit:
            return hit[0], hit[1], fam
    return None


def style_key(bold=False, italic=False):
    return ("bold" if bold else "") + ("italic" if italic else "") or "regular"


def find_font_file(family, style="regular"):
    for name in FONT_FILES.get(family, {}).get(style, []):
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None


def ttc_offsets(data):
    if data[:4] == b"ttcf":
        n = struct.unpack(">I", data[8:12])[0]
        return list(struct.unpack(">%dI" % n, data[12:12 + 4 * n]))
    return [0]


class TTF:
    """Just enough of the TrueType/OpenType format to read names, vertical metrics and advance widths.
    `index` selects a face inside a .ttc collection."""

    def __init__(self, path, index=0, data=None):
        self.path = path
        d = self.data = data if data is not None else open(path, "rb").read()
        base = ttc_offsets(d)[index]
        n = struct.unpack(">H", d[base + 4:base + 6])[0]
        self.tables = {}
        for i in range(n):
            tag, _, off, ln = struct.unpack(">4sIII", d[base + 12 + 16 * i:base + 28 + 16 * i])
            self.tables[tag.decode("latin1")] = (off, ln)
        h = self.tables["head"][0]
        self.upm = struct.unpack(">H", d[h + 18:h + 20])[0]
        hh = self.tables["hhea"][0]
        self.hhea_ascender, self.hhea_descender, self.hhea_linegap = struct.unpack(">hhh", d[hh + 4:hh + 10])
        n_hm = struct.unpack(">H", d[hh + 34:hh + 36])[0]
        o2 = self.tables["OS/2"][0]
        ver = struct.unpack(">H", d[o2:o2 + 2])[0]
        self.typo_ascender, self.typo_descender, self.typo_linegap = struct.unpack(">hhh", d[o2 + 68:o2 + 74])
        self.win_ascent, self.win_descent = struct.unpack(">HH", d[o2 + 74:o2 + 78])
        self.cap_height = struct.unpack(">h", d[o2 + 88:o2 + 90])[0] if ver >= 2 else int(self.upm * 0.716)
        hm = self.tables["hmtx"][0]
        self.advances = [struct.unpack(">H", d[hm + 4 * i:hm + 4 * i + 2])[0] for i in range(n_hm)]
        self.cmap = self._cmap()
        fs = struct.unpack(">H", d[o2 + 62:o2 + 64])[0]
        self.italic, self.bold = bool(fs & 1), bool(fs & 32)

    def names(self):
        """(family, subfamily) preferring typographic names (16/17), Windows English."""
        if "name" not in self.tables:
            return None, None
        d = self.data
        off = self.tables["name"][0]
        count, sto = struct.unpack(">HH", d[off + 2:off + 6])
        got = {}
        for i in range(count):
            pid, eid, lid, nid, ln, so = struct.unpack(">HHHHHH", d[off + 6 + 12 * i:off + 18 + 12 * i])
            if nid not in (1, 2, 16, 17):
                continue
            raw = d[off + sto + so:off + sto + so + ln]
            if pid == 3 and lid in (0x409, 0):
                got[nid] = raw.decode("utf-16-be", "ignore")
            elif pid == 1 and nid not in got:
                got[nid] = raw.decode("mac_roman", "ignore")
        return got.get(16) or got.get(1), got.get(17) or got.get(2)

    def _cmap(self):
        d = self.data
        base = self.tables["cmap"][0]
        n = struct.unpack(">H", d[base + 2:base + 4])[0]
        subs = {}
        for i in range(n):
            pid, eid, off = struct.unpack(">HHI", d[base + 4 + 8 * i:base + 12 + 8 * i])
            subs[(pid, eid)] = base + off
        off = subs.get((3, 10)) or subs.get((3, 1)) or subs.get((0, 3)) or subs.get((0, 4))
        fmt = struct.unpack(">H", d[off:off + 2])[0]
        out = {}
        if fmt == 4:
            segx2 = struct.unpack(">H", d[off + 6:off + 8])[0]
            seg = segx2 // 2
            ends = struct.unpack(">%dH" % seg, d[off + 14:off + 14 + segx2])
            st = off + 16 + segx2
            starts = struct.unpack(">%dH" % seg, d[st:st + segx2])
            deltas = struct.unpack(">%dh" % seg, d[st + segx2:st + 2 * segx2])
            ro_base = st + 2 * segx2
            ros = struct.unpack(">%dH" % seg, d[ro_base:ro_base + segx2])
            for s in range(seg):
                for c in range(starts[s], ends[s] + 1):
                    if c == 0xFFFF:
                        continue
                    if ros[s] == 0:
                        g = (c + deltas[s]) & 0xFFFF
                    else:
                        a = ro_base + 2 * s + ros[s] + 2 * (c - starts[s])
                        g = struct.unpack(">H", d[a:a + 2])[0]
                        if g:
                            g = (g + deltas[s]) & 0xFFFF
                    if g:
                        out[c] = g
        elif fmt == 12:
            ngroups = struct.unpack(">I", d[off + 12:off + 16])[0]
            for i in range(ngroups):
                s, e, g0 = struct.unpack(">III", d[off + 16 + 12 * i:off + 28 + 12 * i])
                for c in range(s, e + 1):
                    out[c] = g0 + (c - s)
        return out

    def advance(self, cp):
        g = self.cmap.get(cp, 0)
        return self.advances[min(g, len(self.advances) - 1)]


# Code points we ship widths for: Latin-1, Latin Extended-A/B, general punctuation, currency, arrows,
# a few symbols used by consulting layouts (check marks, bullets, triangles for trend arrows).
RANGES = [(0x20, 0x7E), (0xA0, 0x24F), (0x2010, 0x2044), (0x20A0, 0x20BF), (0x2190, 0x2199),
          (0x2122, 0x2122), (0x2212, 0x2212), (0x2264, 0x2265), (0x25A0, 0x25CF), (0x2713, 0x2717)]


def metrics_from_ttf(path, index=0):
    f = TTF(path, index)
    widths = {}
    for a, b in RANGES:
        for cp in range(a, b + 1):
            if cp in f.cmap:
                widths[chr(cp)] = f.advance(cp)
    return {
        "source": os.path.basename(path), "upm": f.upm,
        "hhea": [f.hhea_ascender, f.hhea_descender, f.hhea_linegap],
        "typo": [f.typo_ascender, f.typo_descender, f.typo_linegap],
        "win": [f.win_ascent, f.win_descent], "cap_height": f.cap_height,
        "fallback": f.advance(ord("n")), "widths": widths,
    }


_CACHE = {}


class FontMissing(Exception):
    def __init__(self, family, style):
        Exception.__init__(self, "font '%s' (%s) is not installed and has no metric-compatible stand-in here. "
                                 "Put its .ttf/.otf files in <project>/fonts/ or install %s." % (
                                     family, style, STAND_INS.get(family, "it")))
        self.family = family


def metrics(family, bold=False, italic=False):
    key = (family, style_key(bold, italic))
    if key not in _CACHE:
        p = os.path.join(METRICS_DIR, "%s-%s.json" % (family.replace(" ", ""), key[1]))
        if os.path.exists(p):
            _CACHE[key] = json.load(open(p, encoding="utf-8"))
        else:
            hit = locate(family, key[1])
            if not hit:
                raise FontMissing(family, key[1])
            _CACHE[key] = metrics_from_ttf(hit[0], hit[1])
            _CACHE[key]["used_family"] = hit[2]
    return _CACHE[key]


def text_width(text, size_pt, family="Arial", bold=False, italic=False, tracking_pt=0.0):
    """Advance width in points. No kerning, no ligatures: both writers switch them off."""
    m = metrics(family, bold, italic)
    w = m["widths"]
    fb = m["fallback"]
    units = sum(w.get(ch, fb) for ch in text)
    return units * size_pt / m["upm"] + tracking_pt * len(text)
