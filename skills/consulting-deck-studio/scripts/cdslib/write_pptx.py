"""Scene -> editable .pptx, written as raw OOXML with zipfile (no python-pptx).

Parity rules: text boxes have zero insets, wrap="none", no autofit, one paragraph per pre-broken line
and exact line spacing; kerning is never requested. Shapes are plain DrawingML presets with the same
geometry as the HTML SVG. The first-line baseline is shifted by a per-font calibration (calibration.json)
so it lands where Chromium puts it.
"""
import json
import math
import os
import zipfile
from xml.sax.saxutils import escape

from . import fonts
from . import icons as I
from . import scene as S

EMU = 12700  # per point
HERE = os.path.dirname(os.path.abspath(__file__))
CAL_PATH = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "calibration.json"))
A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
RELS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"

_cal = None


def calibration():
    global _cal
    if _cal is None:
        _cal = json.load(open(CAL_PATH, encoding="utf-8")) if os.path.exists(CAL_PATH) else {}
    return _cal


def html_baseline(font, size, lh, bold=False, italic=False):
    """Where Chromium puts the first baseline below the line-box top: half-leading model, hhea metrics."""
    m = fonts.metrics(font, bold, italic)
    asc, desc = m["hhea"][0] / m["upm"] * size, -m["hhea"][1] / m["upm"] * size
    return (lh - (asc + desc)) / 2 + asc


def pptx_baseline(font, size, lh, bold=False, italic=False):
    """Where the presentation app puts the first baseline below the box top with exact line spacing.
    Model: baseline = a*lh + b*size, fitted per font by tools/calibrate.py. Default model (before
    calibration): the full line pitch minus the font descent."""
    c = calibration().get(font)
    if c:
        return c["a"] * lh + c["b"] * size
    m = fonts.metrics(font, bold, italic)
    return lh - (-m["hhea"][1] / m["upm"]) * size


def e(v):
    return int(round(v * EMU))


def _clr(hexv):
    return '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % hexv.lstrip("#").upper()


def _ln(color, lw, dash=None, head=None, tail=None):
    if not color:
        return "<a:ln><a:noFill/></a:ln>"
    d = {"dash": '<a:prstDash val="dash"/>', "dot": '<a:prstDash val="sysDot"/>'}.get(dash, "")
    he = '<a:headEnd type="triangle" w="med" len="med"/>' if tail == "arrow" else ""
    te = '<a:tailEnd type="triangle" w="med" len="med"/>' if head == "arrow" else ""
    return '<a:ln w="%d">%s%s%s%s</a:ln>' % (e(lw), _clr(color), d, he, te)


class Writer:
    def __init__(self):
        self.next_id = 2

    def nid(self):
        self.next_id += 1
        return self.next_id

    def xfrm(self, x, y, w, h, flipH=False, flipV=False, tag="a:xfrm"):
        fl = (' flipH="1"' if flipH else "") + (' flipV="1"' if flipV else "")
        return '<%s%s><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></%s>' % (
            tag, fl, e(x), e(y), max(e(w), 0), max(e(h), 0), tag)

    def sp(self, name, geom, x, y, w, h, fill, ln, body="", txbox=False):
        i = self.nid()
        return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr%s/><p:nvPr/></p:nvSpPr>'
                '<p:spPr>%s%s%s%s</p:spPr>%s</p:sp>') % (
            i, escape(name or "Shape %d" % i), ' txBox="1"' if txbox else "", self.xfrm(x, y, w, h), geom,
            fill, ln, body)

    def el(self, el):
        t = el["t"]
        if t == "group":
            kids = "".join(self.el(c) for c in el["children"])
            xs, ys, xe, ye = _bbox(el["children"])
            i = self.nid()
            x = self.xfrm(xs, ys, xe - xs, ye - ys)
            x = x.replace("</a:xfrm>", '<a:chOff x="%d" y="%d"/><a:chExt cx="%d" cy="%d"/></a:xfrm>' % (
                e(xs), e(ys), e(xe - xs), e(ye - ys)))
            return ('<p:grpSp><p:nvGrpSpPr><p:cNvPr id="%d" name="%s"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                    '<p:grpSpPr>%s</p:grpSpPr>%s</p:grpSp>') % (i, escape(el.get("name") or "Group %d" % i), x, kids)
        if t == "rect":
            prst = {"ellipse": "ellipse", "roundRect": "roundRect"}.get(el["shape"], "rect")
            av = "<a:avLst/>"
            if prst == "roundRect":
                adj = int(round(50000 * min(1.0, el.get("radius", 0) / (min(el["w"], el["h"]) / 2 or 1))))
                av = '<a:avLst><a:gd name="adj" fmla="val %d"/></a:avLst>' % adj
            geom = '<a:prstGeom prst="%s">%s</a:prstGeom>' % (prst, av)
            fill = _clr(el["fill"]) if el.get("fill") else "<a:noFill/>"
            return self.sp(el.get("name"), geom, el["x"], el["y"], el["w"], el["h"], fill, _ln(el.get("line"), el["lw"]))
        if t == "pie":
            out = ""
            sw = max(0.0, min(360.0, el["sweep"]))
            if sw >= 359.99:
                out += self.sp("Harvey", '<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>', el["x"], el["y"],
                               el["w"], el["h"], _clr(el["fill"]), _ln(None, 0))
            elif sw > 0:
                a0 = int(round((el["start"] % 360) * 60000))
                a1 = int(round(((el["start"] + sw) % 360) * 60000))
                geom = ('<a:prstGeom prst="pie"><a:avLst><a:gd name="adj1" fmla="val %d"/>'
                        '<a:gd name="adj2" fmla="val %d"/></a:avLst></a:prstGeom>') % (a0, a1)
                out += self.sp("Harvey", geom, el["x"], el["y"], el["w"], el["h"], _clr(el["fill"]), _ln(None, 0))
            if el.get("line"):
                out += self.sp("Harvey ring", '<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>', el["x"], el["y"],
                               el["w"], el["h"], "<a:noFill/>", _ln(el["line"], el["lw"]))
            return out
        if t == "line":
            x1, y1, x2, y2 = el["x1"], el["y1"], el["x2"], el["y2"]
            i = self.nid()
            return ('<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="%d" name="Line %d"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
                    '<p:spPr>%s<a:prstGeom prst="line"><a:avLst/></a:prstGeom>%s</p:spPr></p:cxnSp>') % (
                i, i, self.xfrm(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1), x2 < x1, y2 < y1),
                _ln(el["color"], el["lw"], el.get("dash"), el.get("head"), el.get("tail")))
        if t == "text":
            return self.text(el)
        if t == "icon":
            return self.icon(el)
        if t == "poly":
            return self.poly(el)
        raise ValueError("unsupported element for pptx: " + t)

    def custgeom(self, name, x, y, w, h, subpaths, box_w, box_h, fill, ln, closed_fill):
        """Freeform shape: subpaths in a box_w x box_h coordinate space, scaled to the shape's extent."""
        S_ = 1000.0
        paths = []
        for sp in subpaths:
            cmds = []
            for c in sp:
                if c[0] == "M":
                    cmds.append('<a:moveTo><a:pt x="%d" y="%d"/></a:moveTo>' % (c[1] * S_, c[2] * S_))
                elif c[0] == "L":
                    cmds.append('<a:lnTo><a:pt x="%d" y="%d"/></a:lnTo>' % (c[1] * S_, c[2] * S_))
                elif c[0] == "C":
                    cmds.append('<a:cubicBezTo><a:pt x="%d" y="%d"/><a:pt x="%d" y="%d"/><a:pt x="%d" y="%d"/></a:cubicBezTo>' % tuple(
                        v * S_ for v in c[1:]))
                elif c[0] == "Z":
                    cmds.append("<a:close/>")
            paths.append('<a:path w="%d" h="%d"%s>%s</a:path>' % (
                box_w * S_, box_h * S_, "" if closed_fill else ' fill="none"', "".join(cmds)))
        geom = ('<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/>'
                '<a:pathLst>%s</a:pathLst></a:custGeom>') % "".join(paths)
        return self.sp(name, geom, x, y, w, h, fill, ln)

    def icon(self, el):
        lw = el["stroke"] * el["w"] / 24.0
        ln = ('<a:ln w="%d" cap="rnd">%s<a:round/></a:ln>' % (e(lw), _clr(el["color"])))
        return self.custgeom("Icon: " + el["name"], el["x"], el["y"], el["w"], el["h"], I.get(el["name"]), 24, 24,
                             "<a:noFill/>", ln, False)

    def poly(self, el):
        x0, y0, w, h = el["x"], el["y"], max(el["w"], 0.01), max(el["h"], 0.01)
        pts = [(px - x0, py - y0) for px, py in el["points"]]
        sp = [["M", pts[0][0], pts[0][1]]] + [["L", a, b] for a, b in pts[1:]] + [["Z"]]
        fill = _clr(el["fill"]) if el.get("fill") else "<a:noFill/>"
        ln = _ln(el.get("line"), el["lw"]).replace("<a:ln ", '<a:ln ').replace("</a:ln>", "<a:miter/></a:ln>") \
            if el.get("line") else "<a:ln><a:noFill/></a:ln>"
        return self.custgeom(el.get("name") or "Freeform", x0, y0, w, h, [sp], w, h, fill, ln, True)

    def text(self, el):
        first = S.first_style(el)
        lh = el["lh"]
        dy = html_baseline(first["font"], first["size"], lh, first["bold"], first["italic"]) - \
            pptx_baseline(first["font"], first["size"], lh, first["bold"], first["italic"])
        top = el["y"] + S.text_offset_y(el) + dy
        algn = {"l": "l", "c": "ctr", "r": "r"}[el["align"]]

        def rpr(r, tag="a:rPr"):
            return '<%s lang="en-GB" sz="%d" b="%d" i="%d"%s dirty="0">%s<a:latin typeface="%s"/><a:cs typeface="%s"/></%s>' % (
                tag, int(round(r["size"] * 100)), r["bold"], r["italic"],
                ' spc="%d"' % int(round(el["tracking"] * 100)) if el["tracking"] else "",
                _clr(r["color"]), r["font"], r["font"], tag)

        out = []
        for p in el["paras"]:
            st = p["lines"][0][0] if p["lines"] and p["lines"][0] else p["style"]
            if p["bullet"]:
                bu = '<a:buClr><a:srgbClr val="%s"/></a:buClr><a:buSzPct val="100000"/><a:buFont typeface="%s"/><a:buChar char="%s"/>' % (
                    (p.get("bullet_color") or st["color"]).lstrip("#").upper(), st["font"], escape(p["bullet"]))
            else:
                bu = "<a:buNone/>"
            ppr = ('<a:pPr algn="%s" marL="%d" indent="%d"><a:lnSpc><a:spcPts val="%d"/></a:lnSpc>'
                   '<a:spcBef><a:spcPts val="%d"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft>%s</a:pPr>') % (
                algn, e(p["indent"]), -e(p["indent"]), int(round(lh * 100)), int(round(p["space_before"] * 100)), bu)
            body = []
            for k, line in enumerate(p["lines"]):
                if k:
                    body.append("<a:br>%s</a:br>" % rpr(st))
                body += ['<a:r>%s<a:t>%s</a:t></a:r>' % (rpr(r), escape(r["text"])) for r in line]
            out.append('<a:p>%s%s<a:endParaRPr lang="en-GB" sz="%d" dirty="0"/></a:p>' % (
                ppr, "".join(body), int(round(st["size"] * 100))))
        bodyxml = ('<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t" rtlCol="0">'
                   '<a:noAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody>') % "".join(out)
        return self.sp(el.get("name") or "Text", '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>', el["x"], top,
                       el["w"], el["need"], "<a:noFill/>", "<a:ln><a:noFill/></a:ln>", bodyxml, txbox=True)


def _bbox(els):
    xs, ys, xe, ye = [], [], [], []
    for c in els:
        if c["t"] == "line":
            xs.append(min(c["x1"], c["x2"])); xe.append(max(c["x1"], c["x2"]))
            ys.append(min(c["y1"], c["y2"])); ye.append(max(c["y1"], c["y2"]))
        elif c["t"] == "group":
            a, b, cc, d = _bbox(c["children"])
            xs.append(a); ys.append(b); xe.append(cc); ye.append(d)
        else:
            xs.append(c["x"]); ys.append(c["y"]); xe.append(c["x"] + c["w"]); ye.append(c["y"] + c["h"])
    return min(xs), min(ys), max(xe), max(ye)


def slide_xml(slide):
    w = Writer()
    shapes = "".join(w.el(x) for x in slide["els"])
    bg = slide.get("bg", "#FFFFFF")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld %s %s %s><p:cSld><p:bg><p:bgPr>%s<a:effectLst/></p:bgPr></p:bg><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
            '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>%s</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>') % (A, R, P, _clr(bg), shapes)


def notes_xml(text, n):
    paras = "".join('<a:p><a:r><a:rPr lang="en-GB" dirty="0"/><a:t>%s</a:t></a:r></a:p>' % escape(p)
                    for p in (text or "").split("\n")) or "<a:p/>"
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:notes %s %s %s><p:cSld><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
            '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Slide Image"/><p:cNvSpPr><a:spLocks noGrp="1" noRot="1" '
            'noChangeAspect="1"/></p:cNvSpPr><p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp>'
            '<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>%s'
            '</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>') % (
        A, R, P, paras)


THEME = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme %s name="CDS">'
         '<a:themeElements><a:clrScheme name="CDS"><a:dk1><a:srgbClr val="1A1A1A"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
         '<a:dk2><a:srgbClr val="0B2545"/></a:dk2><a:lt2><a:srgbClr val="EEF1F4"/></a:lt2>'
         '<a:accent1><a:srgbClr val="0B5FFF"/></a:accent1><a:accent2><a:srgbClr val="5B6B7F"/></a:accent2>'
         '<a:accent3><a:srgbClr val="2E8540"/></a:accent3><a:accent4><a:srgbClr val="E0A100"/></a:accent4>'
         '<a:accent5><a:srgbClr val="C0392B"/></a:accent5><a:accent6><a:srgbClr val="8A97A8"/></a:accent6>'
         '<a:hlink><a:srgbClr val="0B5FFF"/></a:hlink><a:folHlink><a:srgbClr val="5B6B7F"/></a:folHlink></a:clrScheme>'
         '<a:fontScheme name="CDS"><a:majorFont><a:latin typeface="%s"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
         '<a:minorFont><a:latin typeface="%s"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
         '<a:fmtScheme name="CDS"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
         '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
         '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
         '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
         '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>'
         '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements>'
         '<a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')

MASTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster %s %s %s><p:cSld><p:bg><p:bgRef idx="1001">'
          '<a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>'
          '</p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" '
          'accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" '
          'folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
          '<p:txStyles><p:titleStyle><a:lvl1pPr><a:defRPr sz="2400" kern="0"/></a:lvl1pPr></p:titleStyle><p:bodyStyle>'
          '<a:lvl1pPr><a:defRPr sz="1200" kern="0"/></a:lvl1pPr></p:bodyStyle><p:otherStyle><a:lvl1pPr><a:defRPr kern="0"/>'
          '</a:lvl1pPr></p:otherStyle></p:txStyles></p:sldMaster>')

LAYOUT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout %s %s %s type="blank" preserve="1">'
          '<p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
          '<p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')

NOTES_MASTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:notesMaster %s %s %s><p:cSld><p:spTree>'
                '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree>'
                '</p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
                'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
                '</p:notesMaster>')


def write(slides, path, title="Deck", font_major="Arial", font_minor="Arial"):
    """slides: list of {'els': [...], 'bg': '#FFFFFF', 'notes': str}."""
    n = len(slides)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/><Default Extension="jpeg" ContentType="image/jpeg"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
          '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
          '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>'
          '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>']
    for i in range(1, n + 1):
        ct.append('<Override PartName="/ppt/slides/slide%d.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' % i)
        ct.append('<Override PartName="/ppt/notesSlides/notesSlide%d.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>' % i)
    ct.append("</Types>")

    def rels(items):
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="%s">%s</Relationships>' % (
            PKG, "".join('<Relationship Id="%s" Type="%s/%s" Target="%s"/>' % (a, RELS, b, c) for a, b, c in items)))

    pres_rels = [("rId1", "slideMaster", "slideMasters/slideMaster1.xml"), ("rId2", "notesMaster", "notesMasters/notesMaster1.xml"),
                 ("rId3", "theme", "theme/theme1.xml"), ("rId4", "presProps", "presProps.xml"),
                 ("rId5", "viewProps", "viewProps.xml"), ("rId6", "tableStyles", "tableStyles.xml")]
    pres_rels += [("rId%d" % (100 + i), "slide", "slides/slide%d.xml" % i) for i in range(1, n + 1)]
    sld_ids = "".join('<p:sldId id="%d" r:id="rId%d"/>' % (255 + i, 100 + i) for i in range(1, n + 1))
    pres = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation %s %s %s saveSubsetFonts="1">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst><p:sldIdLst>%s</p:sldIdLst>'
            '<p:sldSz cx="%d" cy="%d"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle>'
            '<a:lvl1pPr><a:defRPr kern="0"/></a:lvl1pPr></p:defaultTextStyle></p:presentation>') % (
        A, R, P, sld_ids, e(S.SLIDE_W), e(S.SLIDE_H))

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", rels([("rId1", "officeDocument", "ppt/presentation.xml")]).replace(
            "</Relationships>",
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="%s/extended-properties" Target="docProps/app.xml"/></Relationships>' % RELS))
        z.writestr("docProps/core.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties '
                   'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                   'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>%s</dc:title><dc:creator>Consulting Deck Studio'
                   '</dc:creator></cp:coreProperties>' % escape(title))
        z.writestr("docProps/app.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties '
                   'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                   '<Application>Consulting Deck Studio</Application><Slides>%d</Slides></Properties>' % n)
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", rels(pres_rels))
        z.writestr("ppt/presProps.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr %s %s %s/>' % (A, R, P))
        z.writestr("ppt/viewProps.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr %s %s %s/>' % (A, R, P))
        z.writestr("ppt/tableStyles.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst %s '
                   'def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>' % A)
        z.writestr("ppt/theme/theme1.xml", THEME % (A, escape(font_major), escape(font_minor)))
        z.writestr("ppt/theme/theme2.xml", THEME % (A, escape(font_major), escape(font_minor)))
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER % (A, R, P))
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
                                                                         ("rId2", "theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT % (A, R, P))
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([("rId1", "slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", NOTES_MASTER % (A, R, P))
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels([("rId1", "theme", "../theme/theme2.xml")]))
        for i, s in enumerate(slides, 1):
            z.writestr("ppt/slides/slide%d.xml" % i, slide_xml(s))
            z.writestr("ppt/slides/_rels/slide%d.xml.rels" % i, rels([("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"),
                                                                       ("rId2", "notesSlide", "../notesSlides/notesSlide%d.xml" % i)]))
            z.writestr("ppt/notesSlides/notesSlide%d.xml" % i, notes_xml(s.get("notes", ""), i))
            z.writestr("ppt/notesSlides/_rels/notesSlide%d.xml.rels" % i, rels([("rId1", "notesMaster", "../notesMasters/notesMaster1.xml"),
                                                                                 ("rId2", "slide", "../slides/slide%d.xml" % i)]))
    return path
