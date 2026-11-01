"""The scene model: every slide is a flat list of absolutely positioned elements in points.

A slide is 960 x 540 pt (13.333 x 7.5 in, 16:9). Both writers (HTML and PPTX) draw exactly these
elements at exactly these coordinates, and text arrives already broken into lines, so no renderer
ever reflows anything. That is what makes PPTX == HTML == PDF.

Element kinds (plain dicts so scenes serialise to JSON for debugging and tests):
  rect    x y w h fill line lw shape("rect"|"ellipse"|"roundRect") radius
  line    x1 y1 x2 y2 color lw dash(None|"dash"|"dot") head(None|"arrow") tail
  pie     x y w h start sweep fill line lw          (Harvey balls, P-curve markers)
  text    x y w h paras lh align("l"|"c"|"r") va("t"|"m"|"b") tracking
          paras = [{lines: [[run, ...], ...], bullet, indent, space_before}]; run = {text font size bold italic color}
  icon    name x y w h color stroke                  (Lucide line icon, 24-unit geometry)
  poly    points fill line lw                         (chevrons, trend triangles)
  image   x y w h src
  group   children name
"""
from . import fonts

SLIDE_W, SLIDE_H = 960.0, 540.0


class LayoutError(Exception):
    pass


def run(text, font="Arial", size=12, bold=False, italic=False, color="#1A1A1A"):
    return {"text": text, "font": font, "size": float(size), "bold": bool(bold), "italic": bool(italic), "color": color}


def _tokens(runs):
    """Split runs into (piece, style) tokens at spaces, keeping the trailing space on each word."""
    out = []
    for r in runs:
        style = {k: v for k, v in r.items() if k != "text"}
        txt = r["text"]
        i = 0
        while i < len(txt):
            j = txt.find(" ", i)
            if j < 0:
                out.append((txt[i:], style))
                break
            out.append((txt[i:j + 1], style))
            i = j + 1
    return out


def _w(piece, st, tracking):
    return fonts.text_width(piece, st["size"], st["font"], st["bold"], st["italic"], tracking)


def wrap(runs, width, tracking=0.0):
    """Greedy word wrap with exact advance widths. Explicit '\n' inside a run forces a break.
    Returns a list of lines, each a list of runs with trailing spaces trimmed."""
    paras, cur = [], []
    for r in runs:
        parts = r["text"].split("\n")
        for k, p in enumerate(parts):
            if k:
                paras.append(cur)
                cur = []
            if p:
                cur.append(dict(r, text=p))
    paras.append(cur)

    lines = []
    for para in paras:
        line, lw = [], 0.0
        for piece, st in _tokens(para):
            pw = _w(piece.rstrip(" "), st, tracking)
            if line and lw + pw > width + 0.01:
                lines.append(line)
                line, lw = [], 0.0
            if not line and pw > width + 0.01:
                raise LayoutError("word wider than box: %r (%.1f > %.1f pt)" % (piece, pw, width))
            line.append((piece, st))
            lw += _w(piece, st, tracking)
        lines.append(line)

    out = []
    for line in lines:
        merged = []
        for piece, st in line:
            if merged and all(merged[-1][k] == v for k, v in st.items()):
                merged[-1]["text"] += piece
            else:
                merged.append(dict(st, text=piece))
        if merged:
            merged[-1]["text"] = merged[-1]["text"].rstrip(" ")
        out.append(merged)
    return out


def line_width(line, tracking=0.0):
    return sum(_w(r["text"], r, tracking) for r in line)


def text(x, y, w, runs, lh=1.2, align="l", va="t", h=None, max_lines=None, tracking=0.0, name=None):
    """A single paragraph (or several split by '\n'). Shorthand for paras() without bullets."""
    if isinstance(runs, dict):
        runs = [runs]
    return paras(x, y, w, [{"runs": runs}], lh=lh, align=align, va=va, h=h, max_lines=max_lines,
                 tracking=tracking, name=name)


def paras(x, y, w, items, lh=1.2, align="l", va="t", h=None, max_lines=None, tracking=0.0, name=None, gap=0.0):
    """Lay out paragraphs in one box. Each item: {runs, bullet (None|"•"|"–"|"1."), indent (pt),
    space_before (pt)}. Wrapped lines of a paragraph stay in that paragraph (soft breaks in PPTX), so a
    bulleted list is one editable text box with real bullets. Raises LayoutError on overflow."""
    out_paras, total_lines = [], 0
    size = 0
    for k, it in enumerate(items):
        runs = it["runs"] if isinstance(it["runs"], list) else [it["runs"]]
        indent = it.get("indent", 0.0 if not it.get("bullet") else 12.0)
        lines = wrap(runs, w - indent, tracking)
        size = max([size] + [r["size"] for line in lines for r in line] + [runs[0]["size"]])
        sb = 0.0 if k == 0 else it.get("space_before", gap)
        out_paras.append({"lines": lines, "bullet": it.get("bullet"), "indent": indent, "space_before": sb,
                          "bullet_color": it.get("bullet_color"), "style": dict(runs[0], text="")})
        total_lines += len(lines)
    pitch = round(lh * size, 2)
    need = pitch * total_lines + sum(p["space_before"] for p in out_paras)
    if max_lines and total_lines > max_lines:
        raise LayoutError("%s: %d lines > max %d" % (name or "text", total_lines, max_lines))
    if h is None:
        h = need
    elif need > h + 0.01:
        raise LayoutError("%s: text needs %.1f pt but box is %.1f pt" % (name or "text", need, h))
    return {"t": "text", "x": x, "y": y, "w": w, "h": h, "paras": out_paras, "lh": pitch, "align": align,
            "va": va, "tracking": tracking, "name": name, "need": need}


def first_style(el):
    for p in el["paras"]:
        for line in p["lines"]:
            if line:
                return line[0]
    return el["paras"][0]["style"]


def rect(x, y, w, h, fill=None, line=None, lw=0.75, shape="rect", radius=0, name=None):
    return {"t": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill, "line": line, "lw": lw,
            "shape": shape, "radius": radius, "name": name}


def hline(x1, y, x2, color="#1A1A1A", lw=0.75, dash=None):
    return {"t": "line", "x1": x1, "y1": y, "x2": x2, "y2": y, "color": color, "lw": lw, "dash": dash,
            "head": None, "tail": None}


def line(x1, y1, x2, y2, color="#1A1A1A", lw=0.75, dash=None, head=None, tail=None):
    return {"t": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "color": color, "lw": lw, "dash": dash,
            "head": head, "tail": tail}


def pie(x, y, d, sweep, fill="#1A1A1A", line="#1A1A1A", lw=0.75, start=-90):
    return {"t": "pie", "x": x, "y": y, "w": d, "h": d, "start": start, "sweep": sweep, "fill": fill,
            "line": line, "lw": lw}


def group(children, name=None):
    return {"t": "group", "children": children, "name": name}


def icon(name, x, y, size=16, color="#1A1A1A", stroke=2.0):
    """A Lucide line icon (24-unit box) scaled to `size` pt. Drawn as editable vector paths."""
    return {"t": "icon", "name": name, "x": x, "y": y, "w": size, "h": size, "color": color, "stroke": stroke}


def poly(points, fill=None, line=None, lw=0.75, name=None):
    """Closed polygon (chevrons, triangles, brackets as open polylines with fill=None and closed=False)."""
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return {"t": "poly", "points": points, "fill": fill, "line": line, "lw": lw, "name": name,
            "x": min(xs), "y": min(ys), "w": max(xs) - min(xs), "h": max(ys) - min(ys)}


def text_offset_y(el):
    """Vertical offset of the first line inside the box for va = m/b."""
    need = el["need"]
    if el["va"] == "m":
        return (el["h"] - need) / 2
    if el["va"] == "b":
        return el["h"] - need
    return 0.0
