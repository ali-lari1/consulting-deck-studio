"""PPTX vs HTML parity check: render both per slide, compare, write comparison images."""
import os
import shutil
import tempfile

from . import png, render, write_html, write_pptx


def check(slides, out_dir, name="deck", tpl=None):
    """Returns list of (slide_no, ratio) and writes parity/cmp-NN.png. None if LibreOffice is missing."""
    pdir = os.path.join(out_dir, "parity")
    os.makedirs(pdir, exist_ok=True)
    stacked = os.path.join(pdir, "_stacked.html")
    open(stacked, "w", encoding="utf-8").write(write_html.document(slides, name, stacked=True))
    tmp = tempfile.mkdtemp(prefix="cds-parity-")
    try:
        singles = []
        for i, s in enumerate(slides, 1):
            p = os.path.join(tmp, "slide-%02d.pptx" % i)
            if tpl:
                write_pptx.write_template([s], p, tpl, name)
            else:
                write_pptx.write([s], p, name)
            singles.append(p)
        pp = render.pptx_pngs(singles, tmp, font_files=render.scene_font_files(slides))
        if not pp:
            return None
        hp = render.html_pngs(stacked, len(slides), tmp)
        res = []
        for i, (a, b) in enumerate(zip(hp, pp), 1):
            A, B = png.read(a).half(), png.read(b).half()
            ratio, heat = png.diff(A, B)
            png.write(png.side_by_side([A, B, heat]), os.path.join(pdir, "cmp-%02d.png" % i))
            res.append((i, ratio))
        return res
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        os.remove(stacked)


def sheet(slides, out_path, cols=3):
    """Contact sheet PNG of the HTML render (half size)."""
    tmp = tempfile.mkdtemp(prefix="cds-sheet-")
    try:
        stacked = os.path.join(tmp, "s.html")
        open(stacked, "w", encoding="utf-8").write(write_html.document(slides, "sheet", stacked=True))
        ims = [png.read(p).half() for p in render.html_pngs(stacked, len(slides), tmp)]
        rows = [png.side_by_side(ims[i:i + cols]) for i in range(0, len(ims), cols)]
        W = rows[0].w
        px = bytearray()
        for k, rw in enumerate(rows):
            if rw.w < W:
                pad = bytearray(b"\xff" * ((W - rw.w) * 3))
                line = bytearray()
                for y in range(rw.h):
                    line += rw.px[y * rw.w * 3:(y + 1) * rw.w * 3] + pad
                rw = png.Image(W, rw.h, line)
            px += rw.px
            if k < len(rows) - 1:
                px += bytearray(b"\x90" * (W * 8 * 3))
        H = sum(rw.h for rw in rows) + 8 * (len(rows) - 1)
        png.write(png.Image(W, H, px), out_path)
        return out_path
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
