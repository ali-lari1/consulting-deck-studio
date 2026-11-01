"""Consulting slide components built from scene primitives.

Conventions follow standard consulting practice (not any firm's brand): tracker and draft sticker,
action title, exhibit header with a unit line, dark header-bar boxes, numbered callouts tied to a
takeaways column, legends for every encoding, footnotes and source, and an optional so-what bar.
All sizes are in points on the 960 x 540 canvas.
"""
from . import scene as S
from .scene import run

THEME = {
    "font": "Arial", "title_font": "Arial",
    "ink": "#1A1A1A", "navy": "#0B2545", "blue": "#2F5D9A", "sky": "#DCE6F2", "grey": "#5F6B7A",
    "mid": "#A3ADB8", "rule": "#C9CFD6", "tint": "#F2F4F7", "white": "#FFFFFF",
    "R": "#C62828", "A": "#E8A300", "G": "#2E7D32", "R_t": "#F6D3D1", "A_t": "#FBEBC2", "G_t": "#D5EAD6",
    "navy_l": "#8FA6C4",
}
T = THEME
HOUSE = dict(THEME)


class Grid:
    """Where things go on the 960 x 540 canvas. House values below; template mode replaces them with
    positions read from the client's slide layouts."""
    def __init__(self, **kw):
        self.L, self.R = 36.0, 924.0               # content left / right edge
        self.main_r, self.side_x = 626.0, 650.0     # main exhibit right edge, side panel left edge
        self.top = 104.0                           # body top
        self.title = dict(x=36.0, y=34.0, w=888.0, h=52.0, size=20.0, bold=True, color=None, font=None, lines=2)
        self.rule_y = 90.0                         # rule under the title (None = template draws its own)
        self.context_y, self.tracker_y = 14.0, 13.0
        self.sowhat_y, self.foot_y = 446.0, 486.0
        self.page = dict(x=804.0, y=520.0, w=120.0, align="r")
        self.foot_bottom = 532.0                   # footnotes end above this
        self.chrome = True                         # draw context line, tracker, confidential mark
        self.scale = 1.0                           # canvas pt -> output pt (template slide size / 960)
        self.keepout = []                          # [x, y, w, h] boxes the template's own graphics occupy
        self.__dict__.update(kw)


G = Grid()


def set_grid(g):
    G.__dict__.clear()
    G.__dict__.update(g.__dict__)


def blend(a, b, t):
    """Mix hex colour a toward b by t (0..1)."""
    a, b = a.lstrip("#"), b.lstrip("#")
    return "#%02X%02X%02X" % tuple(int(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t) for i in (0, 2, 4))


def apply_brand(brand):
    """brand: {colors: {primary, secondary, text, light, ...}, fonts: {heading, body}}. Unset keys keep house values."""
    T.clear()
    T.update(HOUSE)
    c = brand.get("colors", {})
    T["navy"] = c.get("primary", T["navy"])
    T["blue"] = c.get("secondary", blend(T["navy"], "#FFFFFF", 0.35))
    T["ink"] = c.get("text", T["ink"])
    T["tint"] = c.get("light", T["tint"])
    T["grey"] = c.get("muted", T["grey"])
    for k in ("R", "A", "G", "R_t", "A_t", "G_t", "rule", "mid"):
        if k in c:
            T[k] = c[k]
    T["sky"] = blend(T["navy"], "#FFFFFF", 0.85)
    T["navy_l"] = blend(T["navy"], "#FFFFFF", 0.5)
    f = brand.get("fonts", {})
    T["font"] = f.get("body", T["font"])
    T["title_font"] = f.get("heading", T["font"])


RAG_WORD = {"R": "Red", "A": "Amber", "G": "Green"}


def r(text, size=11, bold=False, color=None, italic=False, font=None):
    return run(text, font=font or T["font"], size=size, bold=bold, italic=italic, color=color or T["ink"])


def frame(title, page, tracker=None, active=None, context=None, sticker=None, sowhat=None, footnotes=None,
          source=None, confidential=True):
    """Standard page furniture on the current grid. Returns (elements, body_bottom_y)."""
    L, R_ = G.L, G.R
    els = []
    sw = S.line_width([r(sticker, 8)]) + 14 if sticker else 0
    if G.chrome and context:
        els.append(S.text(L, G.context_y, 520, r(context, 8, color=T["grey"]), max_lines=1))
    if G.chrome and tracker:
        widths = [S.line_width([r(t, 8, True)]) for t in tracker]
        x = R_ - sum(widths) - 14 * (len(tracker) - 1) - (sw + 16 if sticker else 0)
        for t, w in zip(tracker, widths):
            on = t == active
            els.append(S.text(x, G.tracker_y, w + 1, r(t, 8, on, T["navy"] if on else T["mid"])))
            if on:
                els.append(S.hline(x, G.tracker_y + 11, x + w, T["navy"], 1.25))
            x += w + 14
    if sticker:
        sx, sy = free_x(R_ - sw, G.tracker_y - 3, sw, 15)
        els.append(S.rect(sx, sy, sw, 15, fill=None, line=T["ink"], lw=0.75))
        els.append(S.text(sx, sy + 4, sw, r(sticker, 8, False, T["ink"]), align="c", max_lines=1))
    els.append(title_text(title))
    if G.rule_y is not None:
        els.append(S.hline(L, G.rule_y, R_, T["rule"], 0.75))
    bottom = G.foot_y - 6
    if sowhat:
        y = G.sowhat_y
        els.append(S.rect(L, y, R_ - L, 32, fill=None, line=T["navy"], lw=1.0))
        els.append(S.text(L + 12, y, R_ - L - 24, r(sowhat, 12, True, T["navy"]), va="m", h=32, max_lines=2))
        bottom = y - 8
    lines = []
    for i, fn in enumerate(footnotes or [], 1):
        lines.append({"runs": [r("%d. %s" % (i, fn), 7.5, color=T["grey"])]})
    if source:
        lines.append({"runs": [r("Source: ", 7.5, True, T["grey"]), r(source, 7.5, color=T["grey"])]})
    fy = G.foot_bottom - 10.0 * max(1, len(lines))
    if lines:
        els.append(S.paras(L, fy - 2, min(760, R_ - L - 140), lines, lh=1.25))
    pg = G.page
    if pg:
        els.append(S.text(pg["x"], pg["y"], pg["w"], r(str(page), 8, color=T["grey"]), align=pg.get("align", "r"), name="Page"))
    if G.chrome and confidential:
        els.append(S.text(R_ - 260, 520, 130, r("Confidential", 7.5, color=T["mid"]), align="r"))
    return els, min(bottom, fy - 8)


def free_x(x, y, w, h, gap=8.0):
    """Slide a box left until it clears the template's keep-out zones (logos, bars)."""
    moved = True
    while moved:
        moved = False
        for kx, ky, kw, kh in G.keepout:
            if x < kx + kw and x + w > kx and y < ky + kh and y + h > ky:
                x = kx - w - gap
                moved = True
    return x, y


FIT_LOG = []   # (title, from_size, to_size) when a title had to step down to fit; build.py reports these


def title_text(title):
    """Action title in the grid's title box. Steps the size down 1pt at a time (to 80% of the house/template size,
    never below 16pt) before failing, and logs any step-down so the build can warn."""
    tt = G.title
    size = tt["size"]
    floor = max(16.0, tt["size"] * 0.8)
    while True:
        try:
            el = S.text(tt["x"], tt["y"], tt["w"], r(title, size, tt["bold"], tt["color"] or T["navy"],
                                                     font=tt["font"] or T["title_font"]),
                        lh=1.15, max_lines=tt["lines"], name="Title", h=tt["h"], va=tt.get("va", "t"),
                        align=tt.get("align", "l") if tt.get("align") in ("l", "c", "r") else "l")
            if size < tt["size"]:
                FIT_LOG.append((title, tt["size"], size))
            return el
        except S.LayoutError:
            if size - 1 < floor:
                raise S.LayoutError("title does not fit in %d lines even at %.0fpt; shorten it (%d words)" % (
                    tt["lines"], (size) * G.scale, len(title.split())))
            size -= 1


def exhibit_header(x, y, w, title, unit=None):
    """Bold exhibit title, grey unit line, hairline. Returns (els, y_below)."""
    els = [S.text(x, y, w, r(title, 11, True, T["navy"]))]
    yy = y + 15
    if unit:
        els.append(S.text(x, yy, w, r(unit, 9, color=T["grey"])))
        yy += 13
    els.append(S.hline(x, yy + 2, x + w, T["navy"], 0.75))
    return els, yy + 8


def header_box(x, y, w, h, title, icon=None, fill=None):
    """Side panel: bold navy header over a 1.5pt rule (no box, no icon). Returns (els, inner_y)."""
    els = [S.text(x, y, w, r(title, 11, True, T["navy"])), S.hline(x, y + 18, x + w, T["navy"], 1.5)]
    return els, y + 26


def callout(cx, cy, n, d=13, fill=None):
    """Numbered circle that ties an exhibit feature to a takeaway."""
    return [S.rect(cx - d / 2, cy - d / 2, d, d, fill=fill or T["navy"], shape="ellipse"),
            S.text(cx - d / 2, cy - d / 2, d, r(str(n), 8, True, T["white"]), align="c", va="m", h=d)]


def takeaways(x, y, w, items, title="Key takeaways", h=None, icon="lightbulb", size=10.5):
    """Header box with numbered takeaways. items: [text] or [(bold lead, text)]."""
    paras = []
    for it in items:
        if isinstance(it, list):  # pre-built runs
            paras.append(it)
            continue
        lead, body = (it if isinstance(it, tuple) else (None, it))
        paras.append([r(lead + " ", size, True)] + [r(body, size)] if lead else [r(body, size)])
    blocks = []
    yy = y + 26
    for i, runs in enumerate(paras, 1):
        t = S.text(x + 22, yy, w - 22, runs, lh=1.3)
        blocks += callout(x + 7, yy + 7, i) + [t]
        yy += t["h"] + 10
    hh = h or (yy - y + 2)
    els, _ = header_box(x, y, w, hh, title, icon)
    return els + blocks, y + hh


def bullets(x, y, w, items, size=11, lh=1.3, gap=5):
    """items: [str | (str, level) | (runs, level)]. Level 1 '•', level 2 '–'."""
    paras = []
    for it in items:
        txt, lvl = (it, 1) if not isinstance(it, tuple) else it
        runs = [r(txt, size)] if isinstance(txt, str) else txt
        paras.append({"runs": runs, "bullet": "•" if lvl == 1 else "–", "indent": 11.0 if lvl == 1 else 22.0,
                      "space_before": gap if lvl == 1 else 2, "bullet_color": T["navy"]})
    return S.paras(x, y, w, paras, lh=lh)


def rag_dot(cx, cy, status, d=11):
    return S.rect(cx - d / 2, cy - d / 2, d, d, fill=T[status], shape="ellipse")


def rag_pill(x, y, status, w=50, label=None):
    """Plain status: filled dot and the word (no pill)."""
    return [S.rect(x, y + 3, 9, 9, fill=T[status], shape="ellipse"),
            S.text(x + 14, y + 2, w, r(label or RAG_WORD[status], 9.5))]


def trend(cx, cy, direction, color=None, s=9):
    """Filled triangle: up / down / flat (right)."""
    c = color or T["grey"]
    h = s / 2
    if direction == "up":
        pts = [(cx - h, cy + h * 0.8), (cx + h, cy + h * 0.8), (cx, cy - h * 0.9)]
    elif direction == "down":
        pts = [(cx - h, cy - h * 0.8), (cx + h, cy - h * 0.8), (cx, cy + h * 0.9)]
    else:
        pts = [(cx - h * 0.8, cy - h), (cx - h * 0.8, cy + h), (cx + h * 0.9, cy)]
    return S.poly(pts, fill=c)


def diamond(cx, cy, s=10, fill=None):
    h = s / 2
    return S.poly([(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy)], fill=fill or T["navy"])


def legend(x, y, items, size=8.5):
    """items: [(kind, colour_or_status, label)] kinds: dot, bar, outline, line, dash, diamond, harvey."""
    els = []
    for kind, col, label in items:
        c = T.get(col, col)
        if kind == "dot":
            els.append(S.rect(x, y + 1.5, 8, 8, fill=c, shape="ellipse"))
        elif kind == "bar":
            els.append(S.rect(x, y + 2, 14, 7, fill=c))
        elif kind == "outline":
            els.append(S.rect(x, y + 2, 14, 7, fill=None, line=c, lw=1))
        elif kind == "line":
            els.append(S.line(x, y + 5.5, x + 14, y + 5.5, c, 1.25))
        elif kind == "dash":
            els.append(S.line(x, y + 5.5, x + 14, y + 5.5, c, 1.25, dash="dash"))
        elif kind == "diamond":
            els.append(diamond(x + 5, y + 5.5, 9, c))
        elif kind in ("up", "down", "flat"):
            els.append(trend(x + 5, y + 5.5, kind, c, 8))
        elif kind == "harvey":
            els.append(S.pie(x, y + 1, 9, col * 90, fill=T["navy"], line=T["navy"], lw=0.75))
        w0 = 14 if kind in ("bar", "outline", "line", "dash") else 10
        t = S.text(x + w0 + 4, y, 200, r(label, size, color=T["grey"]))
        t["w"] = S.line_width(t["paras"][0]["lines"][0]) + 1
        els.append(t)
        x += w0 + 4 + t["w"] + 14
    return els


def kpi_card(x, y, w, h, icon, label, value, sub=None, status=None):
    """One cell of a number strip: big figure, label, optional note; status as a dot. No card styling."""
    els = [S.text(x, y, w - 12, r(value, 24, True, T["navy"]))]
    if status:
        els.append(S.rect(x + S.line_width([r(value, 24, True)]) + 6, y + 9, 9, 9, fill=T[status], shape="ellipse"))
    els.append(S.text(x, y + 32, w - 12, r(label, 9.5, True)))
    if sub:
        els.append(S.text(x, y + 46, w - 12, r(sub, 9, color=T["grey"])))
    return els


def icon_tile(x, y, name, s=26, fill=None, color=None):
    """Inline monochrome line icon (no tile), vertically centred in an s-high row."""
    k = 15
    return [S.icon(name, x, y + (s - k) / 2, k, color or T["navy"], 2)]


def chevrons(x, y, w, h, labels, active=None, notch=10):
    els = []
    n = len(labels)
    cw = (w + notch * (n - 1)) / n
    for i, lab in enumerate(labels):
        x0 = x + i * (cw - notch)
        pts = [(x0, y), (x0 + cw - notch, y), (x0 + cw, y + h / 2), (x0 + cw - notch, y + h), (x0, y + h)]
        if i:
            pts.append((x0 + notch, y + h / 2))
        on = lab == active
        els.append(S.poly(pts, fill=T["navy"] if on else T["sky"]))
        els.append(S.text(x0 + (notch if i else 6) + 2, y, cw - notch - (notch if i else 6) - 4,
                          r(lab, 9, True, T["white"] if on else T["navy"]), align="c", va="m", h=h, lh=1.15))
    return els
