"""Read a company template (.potx or .pptx) and turn it into a brand + grid the layouts can use.

What is extracted:
  - slide size (16:9 templates of any physical size are supported; content is laid out on the 960 x 540
    canvas and scaled into the template's size by the PPTX writer)
  - theme colours (dk1/lt1/dk2/lt2/accent1-6) and theme fonts (major/minor)
  - the layouts to use: title, content (Title Only preferred), section, closing/blank
  - placeholder geometry and title text style for the content layout (position, size, weight, colour, anchor)
  - slide-number placeholder geometry, body placeholder geometry (= content area)
The output PPTX reuses the template's real masters and layouts (write_pptx template mode). For HTML/PDF the
master + layout graphics (logos, bars, fixed footer text) are rendered once per layout to a background image
(LibreOffice), so all three outputs show the same chrome. Standard library only.
"""
import os
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "rel": "http://schemas.openxmlformats.org/package/2006/relationships"}
EMU = 12700.0
SLOTS = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"]


class TemplateError(Exception):
    pass


def _rels(z, part):
    d, f = posixpath.split(part)
    rp = posixpath.join(d, "_rels", f + ".rels")
    out = {}
    if rp in z.namelist():
        for rel in ET.fromstring(z.read(rp)).findall("rel:Relationship", NS):
            out[rel.get("Id")] = (rel.get("Type").rsplit("/", 1)[-1],
                                  posixpath.normpath(posixpath.join(d, rel.get("Target"))))
    return out


def _lum(hexv):
    r, g, b = (int(hexv[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _color(el, scheme, clrmap=None):
    """Resolve a fill/colour element (solidFill or a colour child) to hex, or None."""
    if el is None:
        return None
    for c in el.iter():
        tag = c.tag.split("}")[-1]
        if tag == "srgbClr":
            return "#" + c.get("val").upper()
        if tag == "schemeClr":
            v = c.get("val")
            v = {"tx1": "dk1", "bg1": "lt1", "tx2": "dk2", "bg2": "lt2"}.get(v, v) if not clrmap else clrmap.get(v, v)
            return scheme.get(v)
        if tag == "sysClr":
            return "#" + (c.get("lastClr") or "000000").upper()
    return None


def _xfrm(sp):
    x = sp.find(".//a:xfrm", NS)
    if x is None:
        return None
    off, ext = x.find("a:off", NS), x.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return [int(off.get("x")) / EMU, int(off.get("y")) / EMU, int(ext.get("cx")) / EMU, int(ext.get("cy")) / EMU]


def _placeholders(root):
    out = {}
    for sp in root.iter("{%s}sp" % NS["p"]):
        ph = sp.find("p:nvSpPr/p:nvPr/p:ph", NS)
        if ph is None:
            continue
        typ = ph.get("type", "body")
        out.setdefault(typ, {"xfrm": _xfrm(sp), "sp": sp, "idx": ph.get("idx")})
        if out[typ]["xfrm"] is None:
            out[typ]["xfrm"] = _xfrm(sp)
    return out


def read(path):
    if not zipfile.is_zipfile(path):
        raise TemplateError("%s is not a .pptx/.potx file (Keynote and Google Slides: export as .pptx first)" % path)
    z = zipfile.ZipFile(path)
    names = z.namelist()
    pres_part = "ppt/presentation.xml"
    if pres_part not in names:
        raise TemplateError("no ppt/presentation.xml in %s" % path)
    pres = ET.fromstring(z.read(pres_part))
    sz = pres.find("p:sldSz", NS)
    cx, cy = int(sz.get("cx")), int(sz.get("cy"))
    w_pt, h_pt = cx / EMU, cy / EMU
    ratio = cy / float(cx)
    if abs(ratio - 0.5625) > 0.01:
        raise TemplateError("template is %.2f:1 (not 16:9). Only 16:9 templates can be reused as masters; "
                            "the brand colours and fonts can still be used (--brand-only)." % (cx / float(cy)))
    prels = _rels(z, pres_part)
    master_part = next(t for typ, t in prels.values() if typ == "slideMaster")
    mrels = _rels(z, master_part)
    theme_part = next(t for typ, t in mrels.values() if typ == "theme")
    theme = ET.fromstring(z.read(theme_part))
    scheme = {}
    cs = theme.find(".//a:clrScheme", NS)
    for slot in SLOTS:
        el = cs.find("a:" + slot, NS)
        if el is not None:
            scheme[slot] = _color(el, {})
    fs = theme.find(".//a:fontScheme", NS)
    major = fs.find("a:majorFont/a:latin", NS).get("typeface")
    minor = fs.find("a:minorFont/a:latin", NS).get("typeface")
    master = ET.fromstring(z.read(master_part))
    clrmap = dict(master.find("p:clrMap", NS).attrib) if master.find("p:clrMap", NS) is not None else {}
    clrmap = {k: v for k, v in clrmap.items()}

    layouts = []
    for rid, (typ, part) in mrels.items():
        if typ != "slideLayout":
            continue
        lx = ET.fromstring(z.read(part))
        name = lx.find("p:cSld", NS).get("name", "")
        layouts.append({"part": part, "type": lx.get("type", "cust"), "name": name, "xml": lx})

    def pick(*types, names=()):
        for t in types:
            for l_ in layouts:
                if l_["type"] == t:
                    return l_
        for n in names:
            for l_ in layouts:
                if n in l_["name"].lower():
                    return l_
        return None

    content = pick("titleOnly", "obj", "tx", names=("title only", "content")) or layouts[0]
    title_l = pick("title", names=("title slide", "cover")) or content
    section = pick("secHead", names=("section", "divider")) or content
    blank = pick("blank", names=("blank",)) or content

    mph = _placeholders(master)
    cph = _placeholders(content["xml"])

    def geom(typ):
        for src in (cph, mph):
            if typ in src and src[typ]["xfrm"]:
                return src[typ]["xfrm"]
        return None

    title_g = geom("title")
    body_g = geom("body") or (mph.get("body") or {}).get("xfrm")
    num_g = geom("sldNum")
    # title style: master titleStyle lvl1, then layout/master title placeholder lstStyle overrides
    ts = master.find("p:txStyles/p:titleStyle/a:lvl1pPr", NS)
    d = ts.find("a:defRPr", NS) if ts is not None else None
    tsize = int(d.get("sz", "3200")) / 100.0 if d is not None else 32.0
    tbold = (d.get("b") == "1") if d is not None else False
    tcolor = _color(d.find("a:solidFill", NS), scheme, clrmap) if d is not None else None
    tfont = d.find("a:latin", NS).get("typeface") if d is not None and d.find("a:latin", NS) is not None else "+mj-lt"
    talign = ts.get("algn", "l") if ts is not None else "l"
    anchor = "t"
    for src in (cph, mph):
        if "title" in src:
            bp = src["title"]["sp"].find("p:txBody/a:bodyPr", NS)
            if bp is not None and bp.get("anchor"):
                anchor = bp.get("anchor")
                break
    for src in (mph, cph):  # layout overrides master
        if "title" in src:
            lv = src["title"]["sp"].find("p:txBody/a:lstStyle/a:lvl1pPr/a:defRPr", NS)
            if lv is not None:
                tsize = int(lv.get("sz", int(tsize * 100))) / 100.0
                if lv.get("b"):
                    tbold = lv.get("b") == "1"
                c = _color(lv.find("a:solidFill", NS), scheme, clrmap)
                tcolor = c or tcolor
    tfont = {"+mj-lt": major, "+mn-lt": minor}.get(tfont, tfont)

    k = 960.0 / w_pt  # template pt -> canvas pt
    S_ = lambda g: [v * k for v in g] if g else None  # noqa: E731
    title_c, body_c, num_c = S_(title_g), S_(body_g), S_(num_g)

    # brand colours: primary = darkest of accent1/dk2 that is not near-black text
    acc1, dk2 = scheme.get("accent1"), scheme.get("dk2")
    primary = acc1 if acc1 and _lum(acc1[1:]) < 0.45 else (dk2 or acc1)
    brand = {
        "mode": "template",
        "colors": {"primary": primary, "secondary": scheme.get("accent2") or primary, "text": scheme.get("dk1", "#1A1A1A"),
                   "light": scheme.get("lt2") if scheme.get("lt2") and _lum(scheme["lt2"][1:]) > 0.85 else None},
        "fonts": {"heading": major, "body": minor},
        "scheme": scheme,
    }
    brand["colors"] = {kk: v for kk, v in brand["colors"].items() if v}

    L = body_c[0] if body_c else (title_c[0] if title_c else 36.0)
    R = (body_c[0] + body_c[2]) if body_c else 960 - L
    top_title = title_c or [L, 30.0, R - L, 52.0]
    body_top = max(top_title[1] + top_title[3] + 12, body_c[1] if body_c else 0)
    body_bottom = body_c[1] + body_c[3] if body_c else 486.0
    foot_bottom = min(body_bottom + 30, (num_c[1] - 2) if num_c else 532.0, 532.0)
    # keep-out zones: the master's and content layout's own graphics (logos, bars, fixed text)
    keep = []
    for root in (master, content["xml"]):
        tree = root.find("p:cSld/p:spTree", NS)
        for el in list(tree):
            tag = el.tag.split("}")[-1]
            if tag not in ("sp", "pic", "grpSp", "graphicFrame", "cxnSp"):
                continue
            if el.find(".//p:nvPr/p:ph", NS) is not None:
                continue
            g = _xfrm(el)
            if not g or g[2] * g[3] > 0.5 * w_pt * h_pt:
                continue
            keep.append([round(v * k, 2) for v in g])
    grid = {
        "L": round(L, 2), "R": round(R, 2), "top": round(body_top, 2),
        "main_r": round(L + (R - L) * 0.664, 2), "side_x": round(L + (R - L) * 0.664 + 24, 2),
        "title": {"x": round(top_title[0], 2), "y": round(top_title[1], 2), "w": round(top_title[2], 2), "h": round(top_title[3], 2),
                  "size": round(min(tsize * k, 28.0), 2), "bold": tbold, "color": tcolor, "font": tfont,
                  "lines": 2, "va": {"t": "t", "ctr": "m", "b": "b"}.get(anchor, "t"), "align": talign},
        "rule_y": None, "chrome": top_title[1] >= 30, "keepout": keep,
        "context_y": 12.0, "tracker_y": 11.0,
        "sowhat_y": round(foot_bottom - 74, 2), "foot_y": round(foot_bottom - 34, 2), "foot_bottom": round(foot_bottom, 2),
        "page": {"x": round(num_c[0], 2), "y": round(num_c[1] + (num_c[3] - 10) / 2, 2), "w": round(num_c[2], 2), "align": "r"} if num_c else None,
    }
    def slot(lay, types, inherit=True):
        ph_ = _placeholders(lay["xml"])
        for t in types:
            if not inherit and t not in ph_:
                continue
            g = (ph_.get(t) or {}).get("xfrm") or (mph.get(t) or {}).get("xfrm")
            if g:
                size, bold, color = tsize, tbold, tcolor
                for src in (mph.get(t), ph_.get(t)):
                    if src:
                        lv = src["sp"].find("p:txBody/a:lstStyle/a:lvl1pPr/a:defRPr", NS)
                        if lv is not None:
                            size = int(lv.get("sz", int(size * 100))) / 100.0
                            bold = lv.get("b", "1" if bold else "0") == "1"
                            color = _color(lv.find("a:solidFill", NS), scheme, clrmap) or color
                bp = (ph_.get(t) or mph.get(t))["sp"].find("p:txBody/a:bodyPr", NS)
                va = {"t": "t", "ctr": "m", "b": "b"}.get(bp.get("anchor") if bp is not None and bp.get("anchor") else "t", "t")
                return {"x": g[0] * k, "y": g[1] * k, "w": g[2] * k, "h": g[3] * k, "size": size * k, "bold": bold,
                        "color": color, "va": va}
        return None

    slots = {"title": {"title": slot(title_l, ["ctrTitle", "title"]), "subtitle": slot(title_l, ["subTitle", "body"], False)},
             "section": {"title": slot(section, ["title"]), "subtitle": slot(section, ["body"], False)}}
    if slots["title"]["subtitle"]:
        slots["title"]["subtitle"].update(size=min(slots["title"]["subtitle"]["size"], 24.0), bold=False,
                                          color=scheme.get("dk1"))
    warnings = []
    if tsize * k > 28:
        warnings.append("template title size %.0fpt is too large for two-line action titles; reduced to %.0fpt" % (
            tsize, 28 / k))
    if not body_c:
        warnings.append("no body placeholder found; content area inferred from the title")
    return {
        "source": os.path.basename(path), "slide_size_pt": [round(w_pt, 3), round(h_pt, 3)], "scale": round(w_pt / 960.0, 6),
        "layouts": {"content": content["part"], "title": title_l["part"], "section": section["part"], "blank": blank["part"]},
        "layout_names": {kk: v["name"] for kk, v in (("content", content), ("title", title_l), ("section", section), ("blank", blank))},
        "brand": brand, "grid": grid, "slots": slots, "warnings": warnings,
        "has_slides": any(re.match(r"ppt/slides/slide\d+\.xml$", n) for n in names),
    }
