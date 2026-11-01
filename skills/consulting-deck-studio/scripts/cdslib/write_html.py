"""Scene -> HTML. Absolute positioning, pre-broken lines, no kerning or ligatures, so Chromium draws
exactly what the PPTX writer draws. Shapes are inline SVG with the same geometry as DrawingML."""
import html
import math

from . import icons as I
from . import scene as S

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#E9E9E6}
.slide{position:relative;width:960px;height:540px;overflow:hidden;background:#fff;
  font-kerning:none;font-variant-ligatures:none;font-feature-settings:"kern" 0,"liga" 0,"clig" 0;
  text-rendering:geometricPrecision;-webkit-font-smoothing:antialiased}
.slide svg{position:absolute;overflow:visible}
.tx{position:absolute;white-space:pre}
.tx>div{white-space:pre;overflow:visible}
"""


def _fam(f):
    known = {"Arial": "Arial,'Liberation Sans',Helvetica,sans-serif", "Georgia": "Georgia,Gelasio,'Times New Roman',serif"}
    if f in known:
        return known[f]
    from .fonts import STAND_INS
    alt = STAND_INS.get(f)
    return "'%s'%s,sans-serif" % (f, ",'%s'" % alt if alt else "")


def _dash(d, lw):
    if d == "dash":
        return ' stroke-dasharray="%.2f %.2f"' % (4 * lw, 3 * lw)
    if d == "dot":
        return ' stroke-dasharray="%.2f %.2f"' % (lw, lw)
    return ""


def _svg_open(x, y, w, h):
    return '<svg style="left:%.3fpx;top:%.3fpx" width="%.3f" height="%.3f" viewBox="%.3f %.3f %.3f %.3f">' % (
        x, y, max(w, 0.01), max(h, 0.01), x, y, max(w, 0.01), max(h, 0.01))


def _arrow(x1, y1, x2, y2, lw, color):
    ang = math.atan2(y2 - y1, x2 - x1)
    L, W = 3.0 * lw, 1.5 * lw
    bx, by = x2 - L * math.cos(ang), y2 - L * math.sin(ang)
    px, py = -math.sin(ang) * W, math.cos(ang) * W
    return '<polygon points="%.3f,%.3f %.3f,%.3f %.3f,%.3f" fill="%s"/>' % (
        x2, y2, bx + px, by + py, bx - px, by - py, color)


def el_html(e):
    t = e["t"]
    if t == "group":
        return "".join(el_html(c) for c in e["children"])
    if t == "rect":
        pad = e["lw"] if e.get("line") else 0
        out = _svg_open(e["x"] - pad, e["y"] - pad, e["w"] + 2 * pad, e["h"] + 2 * pad)
        fill = e["fill"] or "none"
        stroke = ' stroke="%s" stroke-width="%.3f"' % (e["line"], e["lw"]) if e.get("line") else ""
        if e["shape"] == "ellipse":
            out += '<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="%s"%s/>' % (
                e["x"] + e["w"] / 2, e["y"] + e["h"] / 2, e["w"] / 2, e["h"] / 2, fill, stroke)
        else:
            r = e.get("radius", 0) if e["shape"] == "roundRect" else 0
            out += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="%.3f" fill="%s"%s/>' % (
                e["x"], e["y"], e["w"], e["h"], r, fill, stroke)
        return out + "</svg>"
    if t == "line":
        pad = e["lw"] * 3 + 4
        x0, y0 = min(e["x1"], e["x2"]) - pad, min(e["y1"], e["y2"]) - pad
        w, h = abs(e["x2"] - e["x1"]) + 2 * pad, abs(e["y2"] - e["y1"]) + 2 * pad
        out = _svg_open(x0, y0, w, h)
        out += '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%.3f"%s/>' % (
            e["x1"], e["y1"], e["x2"], e["y2"], e["color"], e["lw"], _dash(e.get("dash"), e["lw"]))
        if e.get("head") == "arrow":
            out += _arrow(e["x1"], e["y1"], e["x2"], e["y2"], e["lw"], e["color"])
        if e.get("tail") == "arrow":
            out += _arrow(e["x2"], e["y2"], e["x1"], e["y1"], e["lw"], e["color"])
        return out + "</svg>"
    if t == "pie":
        pad = e["lw"]
        out = _svg_open(e["x"] - pad, e["y"] - pad, e["w"] + 2 * pad, e["h"] + 2 * pad)
        cx, cy, r = e["x"] + e["w"] / 2, e["y"] + e["h"] / 2, e["w"] / 2
        sw = max(0.0, min(360.0, e["sweep"]))
        if sw >= 359.99:
            out += '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s"/>' % (cx, cy, r, e["fill"])
        elif sw > 0:
            a0, a1 = math.radians(e["start"]), math.radians(e["start"] + sw)
            out += '<path d="M%.3f,%.3f L%.3f,%.3f A%.3f,%.3f 0 %d 1 %.3f,%.3f Z" fill="%s"/>' % (
                cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, 1 if sw > 180 else 0,
                cx + r * math.cos(a1), cy + r * math.sin(a1), e["fill"])
        if e.get("line"):
            out += '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="none" stroke="%s" stroke-width="%.3f"/>' % (
                cx, cy, r, e["line"], e["lw"])
        return out + "</svg>"
    if t == "text":
        top = e["y"] + S.text_offset_y(e)
        al = {"l": "left", "c": "center", "r": "right"}[e["align"]]
        out = ['<div class="tx" style="left:%.3fpx;top:%.3fpx;width:%.3fpx;text-align:%s;letter-spacing:%.3fpx">' % (
            e["x"], top, e["w"], al, e["tracking"])]
        for p in e["paras"]:
            out.append('<div style="position:relative;margin-top:%.3fpx;padding-left:%.3fpx">' % (
                p["space_before"], p["indent"]))
            for k, line in enumerate(p["lines"]):
                # The line box's strut must use the same font and size as the text, or Chromium shifts the
                # baseline (default 16px serif strut). Lines use the largest run on the line.
                big = max(line, key=lambda r: r["size"]) if line else p["style"]
                out.append('<div style="position:relative;height:%.3fpx;line-height:%.3fpx;font-family:%s;font-size:%.2fpx">' % (
                    e["lh"], e["lh"], _fam(big["font"]), big["size"]))
                if k == 0 and p["bullet"]:
                    st = line[0] if line else p["style"]
                    out.append('<span style="position:absolute;left:%.3fpx;font-family:%s;font-size:%.2fpx;color:%s">%s</span>' % (
                        -p["indent"], _fam(st["font"]), st["size"], p.get("bullet_color") or st["color"],
                        html.escape(p["bullet"])))
                for r in line:
                    out.append('<span style="font-family:%s;font-size:%.2fpx;font-weight:%s;font-style:%s;color:%s">%s</span>' % (
                        _fam(r["font"]), r["size"], 700 if r["bold"] else 400, "italic" if r["italic"] else "normal",
                        r["color"], html.escape(r["text"])))
                out.append("</div>")
            out.append("</div>")
        out.append("</div>")
        return "".join(out)
    if t == "icon":
        sw = e["stroke"]
        return ('<svg style="left:%.3fpx;top:%.3fpx" width="%.3f" height="%.3f" viewBox="0 0 24 24">'
                '<path d="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>') % (e["x"], e["y"], e["w"], e["h"], I.svg_d(I.get(e["name"])),
                                                       e["color"], sw)
    if t == "poly":
        pad = e["lw"] if e.get("line") else 0
        out = _svg_open(e["x"] - pad, e["y"] - pad, e["w"] + 2 * pad, e["h"] + 2 * pad)
        stroke = ' stroke="%s" stroke-width="%.3f" stroke-linejoin="miter"' % (e["line"], e["lw"]) if e.get("line") else ""
        out += '<polygon points="%s" fill="%s"%s/>' % (" ".join("%.3f,%.3f" % p for p in e["points"]),
                                                       e.get("fill") or "none", stroke)
        return out + "</svg>"
    if t == "image":
        return '<img style="position:absolute;left:%.3fpx;top:%.3fpx;width:%.3fpx;height:%.3fpx" src="%s">' % (
            e["x"], e["y"], e["w"], e["h"], html.escape(e["src"]))
    raise ValueError("unknown element " + t)


def slide_html(slide):
    return '<section class="slide" style="background:%s">%s</section>' % (
        slide.get("bg", "#FFFFFF"), "".join(el_html(e) for e in slide["els"]))


def document(slides, title="Deck", stacked=True):
    """stacked=True puts slides edge to edge (for screenshots and parity checks)."""
    body = "".join(slide_html(s) for s in slides)
    gap = "" if stacked else ".slide{margin:24px auto;box-shadow:0 2px 12px rgba(0,0,0,.15)}"
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s</title>'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><style>%s%s</style></head>'
            '<body>%s</body></html>') % (html.escape(title), CSS, gap, body)


VIEWER_CSS = """
body{background:#E6E8EB;font-family:Arial,'Liberation Sans',sans-serif}
.wrap{display:flex;flex-direction:column;align-items:center;gap:20px;padding:24px 16px 80px}
.frame{position:relative;box-shadow:0 1px 6px rgba(0,0,0,.18)}
.frame .slide{position:absolute;left:0;top:0;transform-origin:0 0}
.note{display:none;max-width:960px;width:100%;font-size:14px;line-height:1.5;color:#2A2F36;background:#fff;
  padding:12px 16px;border-left:3px solid #0B2545;white-space:pre-wrap;box-sizing:border-box}
body.notes .note{display:block}
.hud{position:fixed;right:12px;bottom:10px;font-size:11px;color:#5F6B7A;background:rgba(255,255,255,.85);padding:4px 8px}
body.present{background:#000;overflow:hidden}
body.present .wrap{padding:0;gap:0}
body.present .frame{display:none;box-shadow:none}
body.present .frame.on{display:block;position:fixed;top:50%;left:50%}
body.present .note,body.present .hud{display:none}
@media print{
  @page{size:13.333in 7.5in;margin:0}
  body{background:#fff}.wrap{padding:0;gap:0;display:block}.hud,.note{display:none!important}
  .frame{box-shadow:none;width:13.333in!important;height:7.5in!important;page-break-after:always;break-after:page;overflow:hidden}
  .frame .slide{transform:scale(1.33333)!important}
}
"""

VIEWER_JS = """
(function(){
var F=[].slice.call(document.querySelectorAll('.frame')),i=0,b=document.body;
if(/[?&]reader/.test(location.search))b.classList.add('notes');
function fit(){
  if(b.classList.contains('present')){
    var s=Math.min(innerWidth/960,innerHeight/540);
    F.forEach(function(f,k){f.classList.toggle('on',k===i);f.style.width=960*s+'px';f.style.height=540*s+'px';
      f.style.marginLeft=-480*s+'px';f.style.marginTop=-270*s+'px';f.firstElementChild.style.transform='scale('+s+')';});
  }else{
    var s=Math.min(1,(document.documentElement.clientWidth-32)/960);
    F.forEach(function(f){f.style.width=960*s+'px';f.style.height=540*s+'px';f.style.margin='';
      f.firstElementChild.style.transform='scale('+s+')';});
  }
}
addEventListener('resize',fit);
addEventListener('keydown',function(e){
  var k=e.key;
  if(k==='f'||k==='F'){b.classList.toggle('present');fit();}
  else if(k==='n'||k==='N'||k==='r'||k==='R'){b.classList.toggle('notes');}
  else if(k==='Escape'){b.classList.remove('present');fit();}
  else if(b.classList.contains('present')){
    if(k==='ArrowRight'||k===' '||k==='PageDown'){i=Math.min(F.length-1,i+1);fit();}
    if(k==='ArrowLeft'||k==='PageUp'){i=Math.max(0,i-1);fit();}
  }
});
F.forEach(function(f,k){f.addEventListener('dblclick',function(){i=k;b.classList.add('present');fit();});});
fit();
})();
"""


def viewer(slides, title="Deck", page_in=(13.333, 7.5)):
    """Presentable single-file deck: scroll view, F = present, arrows, N = notes, ?reader = notes open, print = PDF."""
    parts = []
    for k, s in enumerate(slides, 1):
        parts.append('<div class="frame" id="s%d">%s</div>' % (k, slide_html(s)))
        if s.get("notes"):
            parts.append('<div class="note"><b>Slide %d.</b> %s</div>' % (k, html.escape(s["notes"])))
    css = VIEWER_CSS.replace("13.333in 7.5in", "%.3fin %.3fin" % page_in).replace(
        "width:13.333in!important;height:7.5in!important", "width:%.3fin!important;height:%.3fin!important" % page_in).replace(
        "scale(1.33333)", "scale(%.5f)" % (page_in[0] * 96 / 960.0))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s</title>'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><style>%s%s</style></head><body>'
            '<div class="wrap">%s</div><div class="hud">F present &middot; arrows &middot; N notes &middot; Ctrl/Cmd+P PDF</div>'
            '<script>%s</script></body></html>') % (html.escape(title), CSS, css, "".join(parts), VIEWER_JS)
