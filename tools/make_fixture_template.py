#!/usr/bin/env python3
"""Generate tests/fixtures/acme-template.pptx: a fictional corporate template used to test template mode.

It deliberately differs from the house style: 10 x 5.625 in slides, teal/orange theme, Verdana, a logo image
and footer bar on the master, its own title placeholder style, a slide-number placeholder, and four layouts
(Title Slide, Title Only, Section Header, Blank). One sample slide is included so ingestion must drop it.
"""
import os
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "skills", "consulting-deck-studio", "scripts"))
from cdslib import png  # noqa: E402

A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CX, CY = 9144000, 5143500
TEAL, ORANGE = "00594F", "E87722"
HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'


def rels(items):
    return HDR + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>' % "".join(
        '<Relationship Id="%s" Type="%s/%s" Target="%s"/>' % x for x in [(a, RT, b, c) for a, b, c in items])


def ph(i, name, typ, x, y, w, h, idx=None, body=""):
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="%s"%s/></p:nvPr></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/>'
            '</a:xfrm></p:spPr><p:txBody><a:bodyPr%s/><a:lstStyle/><a:p><a:endParaRPr lang="en-GB"/></a:p></p:txBody></p:sp>') % (
        i, name, typ, ' idx="%d"' % idx if idx is not None else "", x, y, w, h, body)


def tree(inner):
    return ('<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
            '%s</p:spTree></p:cSld>') % inner


def main():
    out = os.path.join(ROOT, "tests", "fixtures", "acme-template.pptx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # logo: teal block with an orange square, 240x80 px
    w, h = 240, 80
    px = bytearray()
    for y in range(h):
        for x in range(w):
            if 10 <= x < 70 and 10 <= y < 70:
                px += bytes.fromhex(ORANGE)
            elif x >= 80 and 25 <= y < 55 and (x // 12) % 2 == 0:
                px += bytes.fromhex(TEAL)
            else:
                px += b"\xff\xff\xff"
    logo = os.path.join(os.path.dirname(out), "_logo.png")
    png.write(png.Image(w, h, px), logo)

    theme = (HDR + '<a:theme %s name="Acme"><a:themeElements><a:clrScheme name="Acme">'
             '<a:dk1><a:srgbClr val="262626"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
             '<a:dk2><a:srgbClr val="003A33"/></a:dk2><a:lt2><a:srgbClr val="EEF3F2"/></a:lt2>'
             '<a:accent1><a:srgbClr val="%s"/></a:accent1><a:accent2><a:srgbClr val="%s"/></a:accent2>'
             '<a:accent3><a:srgbClr val="5B9A8B"/></a:accent3><a:accent4><a:srgbClr val="A7C4BD"/></a:accent4>'
             '<a:accent5><a:srgbClr val="7F7F7F"/></a:accent5><a:accent6><a:srgbClr val="BFBFBF"/></a:accent6>'
             '<a:hlink><a:srgbClr val="00594F"/></a:hlink><a:folHlink><a:srgbClr val="7F7F7F"/></a:folHlink></a:clrScheme>'
             '<a:fontScheme name="Acme"><a:majorFont><a:latin typeface="Verdana"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
             '<a:minorFont><a:latin typeface="Verdana"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
             '<a:fmtScheme name="Acme"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
             '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
             '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
             '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>'
             '</a:themeElements></a:theme>') % (A, TEAL, ORANGE)

    E = 12700
    master_shapes = (
        ph(2, "Title Placeholder 1", "title", 30 * E, 22 * E, 560 * E, 48 * E, body=' anchor="b"') +
        ph(3, "Text Placeholder 2", "body", 30 * E, 82 * E, 660 * E, 270 * E, idx=1) +
        ph(4, "Slide Number Placeholder 3", "sldNum", 640 * E, 380 * E, 50 * E, 16 * E, idx=12) +
        '<p:pic><p:nvPicPr><p:cNvPr id="5" name="Logo"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
        '<p:blipFill><a:blip r:embed="rId9"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="%d" y="%d"/>'
        '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>' % (618 * E, 20 * E, 72 * E, 24 * E) +
        '<p:sp><p:nvSpPr><p:cNvPr id="6" name="Footer bar"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="0" y="%d"/>'
        '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:schemeClr val="accent1"/></a:solidFill>'
        '<a:ln><a:noFill/></a:ln></p:spPr></p:sp>' % (399 * E, CX, 6 * E) +
        '<p:sp><p:nvSpPr><p:cNvPr id="7" name="Footer text"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr><p:spPr><a:xfrm>'
        '<a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        '<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-GB" sz="700">'
        '<a:solidFill><a:srgbClr val="7F7F7F"/></a:solidFill><a:latin typeface="Verdana"/></a:rPr><a:t>Acme Advisory  |  Strictly confidential</a:t></a:r></a:p>'
        '</p:txBody></p:sp>' % (30 * E, 382 * E, 300 * E, 12 * E))
    master = (HDR + '<p:sldMaster %s %s %s><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree>'
              '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>%s</p:spTree></p:cSld>'
              '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" '
              'accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst>'
              '<p:sldLayoutId id="2147483649" r:id="rId1"/><p:sldLayoutId id="2147483650" r:id="rId2"/>'
              '<p:sldLayoutId id="2147483651" r:id="rId3"/><p:sldLayoutId id="2147483652" r:id="rId4"/></p:sldLayoutIdLst>'
              '<p:txStyles><p:titleStyle><a:lvl1pPr algn="l"><a:defRPr sz="2000" b="1"><a:solidFill><a:schemeClr val="accent1"/></a:solidFill>'
              '<a:latin typeface="+mj-lt"/></a:defRPr></a:lvl1pPr></p:titleStyle><p:bodyStyle><a:lvl1pPr><a:defRPr sz="1200">'
              '<a:solidFill><a:schemeClr val="tx1"/></a:solidFill><a:latin typeface="+mn-lt"/></a:defRPr></a:lvl1pPr></p:bodyStyle>'
              '<p:otherStyle><a:lvl1pPr><a:defRPr/></a:lvl1pPr></p:otherStyle></p:txStyles></p:sldMaster>') % (A, R, P, master_shapes)

    def lay(name, typ, inner):
        return (HDR + '<p:sldLayout %s %s %s type="%s" preserve="1"><p:cSld name="%s"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
                '<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>%s</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
                '</p:sldLayout>') % (A, R, P, typ, name, inner)

    layouts = [
        lay("Title Slide", "title", ph(2, "Title 1", "ctrTitle", 40 * E, 140 * E, 600 * E, 80 * E, body=' anchor="b"') +
            ph(3, "Subtitle 2", "subTitle", 40 * E, 230 * E, 600 * E, 40 * E, idx=1) +
            '<p:sp><p:nvSpPr><p:cNvPr id="4" name="Side band"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="0" y="0"/>'
            '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:schemeClr val="accent2"/></a:solidFill>'
            '<a:ln><a:noFill/></a:ln></p:spPr></p:sp>' % (14 * E, CY)),
        lay("Title Only", "titleOnly", ph(2, "Title 1", "title", 30 * E, 22 * E, 560 * E, 48 * E) +
            ph(3, "Slide Number 3", "sldNum", 640 * E, 380 * E, 50 * E, 16 * E, idx=12)),
        lay("Section Header", "secHead", ph(2, "Title 1", "title", 40 * E, 160 * E, 600 * E, 60 * E) +
            '<p:sp><p:nvSpPr><p:cNvPr id="4" name="Section band"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="0" y="0"/>'
            '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:schemeClr val="accent1"/></a:solidFill>'
            '<a:ln><a:noFill/></a:ln></p:spPr></p:sp>' % (CX, 120 * E)),
        lay("Blank", "blank", ""),
    ]
    sample = (HDR + '<p:sld %s %s %s>%s<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>') % (
        A, R, P, tree(ph(2, "Title 1", "title", 30 * E, 22 * E, 560 * E, 48 * E)))
    ct = (HDR + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" '
          'ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' +
          "".join('<Override PartName="/ppt/slideLayouts/slideLayout%d.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>' % i
                  for i in range(1, 5)) + "</Types>")
    pres = (HDR + '<p:presentation %s %s %s><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst><p:sldSz cx="%d" cy="%d"/><p:notesSz cx="6858000" cy="9144000"/>'
            '</p:presentation>') % (A, R, P, CX, CY)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels([("rId1", "officeDocument", "ppt/presentation.xml")]))
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", rels([("rId1", "slideMaster", "slideMasters/slideMaster1.xml"),
                                                           ("rId2", "slide", "slides/slide1.xml"), ("rId3", "theme", "theme/theme1.xml")]))
        z.writestr("ppt/theme/theme1.xml", theme)
        z.writestr("ppt/slideMasters/slideMaster1.xml", master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels(
            [("rId%d" % i, "slideLayout", "../slideLayouts/slideLayout%d.xml" % i) for i in range(1, 5)] +
            [("rId8", "theme", "../theme/theme1.xml"), ("rId9", "image", "../media/image1.png")]))
        for i, l in enumerate(layouts, 1):
            z.writestr("ppt/slideLayouts/slideLayout%d.xml" % i, l)
            z.writestr("ppt/slideLayouts/_rels/slideLayout%d.xml.rels" % i, rels([("rId1", "slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/slides/slide1.xml", sample)
        z.writestr("ppt/slides/_rels/slide1.xml.rels", rels([("rId1", "slideLayout", "../slideLayouts/slideLayout2.xml")]))
        z.write(logo, "ppt/media/image1.png")
    os.remove(logo)
    print("wrote", out)


if __name__ == "__main__":
    main()
