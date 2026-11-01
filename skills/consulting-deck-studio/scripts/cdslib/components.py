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
    "L": 36.0, "Rm": 924.0, "title_y": 34.0, "body_y": 104.0, "sowhat_y": 446.0, "foot_y": 486.0,
}
T = THEME
RAG_WORD = {"R": "Red", "A": "Amber", "G": "Green"}


def r(text, size=11, bold=False, color=None, italic=False, font=None):
    return run(text, font=font or T["font"], size=size, bold=bold, italic=italic, color=color or T["ink"])


def frame(title, page, tracker=None, active=None, context=None, sticker=None, sowhat=None, footnotes=None,
          source=None, confidential=True):
    """Standard page furniture. Returns (elements, body_bottom_y)."""
    L, R_ = T["L"], T["Rm"]
    els = []
    x = L
    if context:
        els.append(S.text(x, 14, 520, r(context, 8, color=T["grey"])))
    sw = S.line_width([r(sticker.upper(), 7, True)], 0.4) + 16 if sticker else 0
    if tracker:
        widths = [max(54.0, S.line_width([r(t, 7.5, True)]) + 14) for t in tracker]
        x = R_ - sum(widths) - 2 * (len(tracker) - 1) - (sw + 6 if sticker else 0)
        for t, w in zip(tracker, widths):
            on = t == active
            els.append(S.rect(x, 11, w, 14, fill=T["navy"] if on else T["tint"]))
            els.append(S.text(x, 14.5, w, r(t, 7.5, True, T["white"] if on else T["grey"]), align="c"))
            x += w + 2
    if sticker:
        els.append(S.rect(R_ - sw, 11, sw, 14, fill=None, line=T["R"], lw=0.75))
        els.append(S.text(R_ - sw, 14.5, sw, r(sticker.upper(), 7, True, T["R"]), align="c", tracking=0.4, max_lines=1))
    els.append(S.text(L, T["title_y"], R_ - L, r(title, 20, True, T["navy"], font=T["title_font"]), lh=1.15,
                      max_lines=2, name="Title"))
    els.append(S.hline(L, 90, R_, T["rule"], 0.75))
    bottom = T["foot_y"] - 6
    if sowhat:
        y = T["sowhat_y"]
        els.append(S.rect(L, y, R_ - L, 32, fill=T["navy"]))
        els.append(S.icon("arrow-right", L + 10, y + 8, 16, T["white"], 2.25))
        els.append(S.text(L + 34, y, R_ - L - 44, r(sowhat, 12, True, T["white"]), va="m", h=32, max_lines=2))
        bottom = y - 8
    lines = []
    for i, fn in enumerate(footnotes or [], 1):
        lines.append({"runs": [r("%d. %s" % (i, fn), 7.5, color=T["grey"])]})
    if source:
        lines.append({"runs": [r("Source: ", 7.5, True, T["grey"]), r(source, 7.5, color=T["grey"])]})
    fy = 532 - 10.0 * max(1, len(lines))
    if lines:
        els.append(S.paras(L, fy - 2, 760, lines, lh=1.25))
    els.append(S.text(R_ - 120, 520, 120, r(str(page), 8, color=T["grey"]), align="r"))
    if confidential:
        els.append(S.text(R_ - 260, 520, 130, r("Confidential", 7.5, color=T["mid"]), align="r"))
    return els, min(bottom, fy - 8)


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
    """Box with a dark header bar. Returns (els, inner_y)."""
    els = [S.rect(x, y, w, h, fill=fill or T["white"], line=T["rule"], lw=0.75),
           S.rect(x, y, w, 22, fill=T["navy"])]
    tx = x + 8
    if icon:
        els.append(S.icon(icon, x + 7, y + 4, 14, T["white"], 2.25))
        tx += 20
    els.append(S.text(tx, y, w - (tx - x) - 8, r(title, 10, True, T["white"]), va="m", h=22))
    return els, y + 30


def callout(cx, cy, n, d=14, fill=None):
    """Numbered circle that ties an exhibit feature to a takeaway."""
    return [S.rect(cx - d / 2, cy - d / 2, d, d, fill=fill or T["navy"], shape="ellipse"),
            S.text(cx - d / 2, cy - d / 2, d, r(str(n), 8, True, T["white"]), align="c", va="m", h=d)]


def takeaways(x, y, w, items, title="Key takeaways", h=None, icon="lightbulb", size=10.5):
    """Header box with numbered takeaways. items: [text] or [(bold lead, text)]."""
    paras = []
    for it in items:
        lead, body = (it if isinstance(it, tuple) else (None, it))
        paras.append([r(lead + " ", size, True)] + [r(body, size)] if lead else [r(body, size)])
    blocks = []
    yy = y + 32
    for i, runs in enumerate(paras, 1):
        t = S.text(x + 30, yy, w - 40, runs, lh=1.3)
        blocks += callout(x + 16, yy + 7, i) + [t]
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
    return [S.rect(x, y, w, 15, fill=T[status + "_t"], shape="roundRect", radius=7.5),
            S.rect(x + 6, y + 4, 7, 7, fill=T[status], shape="ellipse"),
            S.text(x + 16, y + 3, w - 18, r(label or RAG_WORD[status], 8, True, T[status] if status != "A" else "#8A6100"))]


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
    els = [S.rect(x, y, w, h, fill=T["tint"]), S.rect(x, y, 3, h, fill=T[status] if status else T["navy"])]
    els.append(S.icon(icon, x + 12, y + 10, 16, T["navy"], 2))
    els.append(S.text(x + 34, y + 12, w - 44, r(label, 8.5, True, T["grey"])))
    els.append(S.text(x + 12, y + 32, w - 20, r(value, 20, True, T["navy"])))
    if sub:
        els.append(S.text(x + 12, y + h - 18, w - 20, r(sub, 8.5, color=T["grey"])))
    return els


def icon_tile(x, y, name, s=26, fill=None, color=None):
    return [S.rect(x, y, s, s, fill=fill or T["sky"]), S.icon(name, x + s * 0.2, y + s * 0.2, s * 0.6, color or T["navy"], 2)]


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
