"""Fit the first-baseline model (baseline = a * line pitch + b * size) for fonts that have no calibration yet.

Renders 'HHHH' samples at several sizes and line pitches to PPTX (LibreOffice) and HTML (Chromium), measures
where the baseline lands in each, and solves for a and b by least squares. Results are cached per project in
.cds/calibration.json and merged over the bundled assets/calibration.json.
"""
import json
import os
import shutil
import tempfile

from . import png, render, write_html, write_pptx
from . import scene as S
from .scene import run

SIZES, PITCHES = [9, 12, 18, 28], [1.0, 1.2, 1.5]


def _baseline_row(img, x, y, w, h):
    last = None
    for r_ in range(y, min(img.h, y + h)):
        row = img.px[(r_ * img.w + x) * 3:(r_ * img.w + x + w) * 3]
        if min(row) < 110:
            last = r_
    return last


def fit(families, cache_path):
    """Calibrate the given font families (regular weight). Returns {family: {a, b, ...}} for those fitted."""
    todo = [f for f in families if f not in write_pptx.calibration()]
    if not todo:
        return {}
    tmp = tempfile.mkdtemp(prefix="cds-cal-")
    out = {}
    try:
        slides, cells = [], []
        for fam in todo:
            els = []
            k = 0
            for size in SIZES:
                for lh in PITCHES:
                    cx, cy = 20 + (k % 6) * 155, 20 + (k // 6) * 125
                    t = S.text(cx, cy, 150, run("HHHH", font=fam, size=size), lh=lh)
                    els.append(t)
                    cells.append((len(slides), fam, size, t["lh"], cx, cy))
                    k += 1
            slides.append({"els": els})
        stacked = os.path.join(tmp, "cal.html")
        open(stacked, "w", encoding="utf-8").write(write_html.document(slides, "cal", stacked=True))
        hp = render.html_pngs(stacked, len(slides), tmp)
        singles = []
        for i, s in enumerate(slides):
            p = os.path.join(tmp, "cal-%02d.pptx" % i)
            write_pptx.write([s], p, "cal")
            singles.append(p)
        pp = render.pptx_pngs(singles, tmp, font_files=render.scene_font_files(slides))
        if not pp:
            return {}
        H = [png.read(p) for p in hp]
        P = [png.read(p) for p in pp]
        k2 = render.SCALE
        rows = {}
        for si, fam, size, lh, cx, cy in cells:
            win = (int(cx * k2), int(cy * k2), int(150 * k2), int(118 * k2))
            bh, bp = _baseline_row(H[si], *win), _baseline_row(P[si], *win)
            if bh is None or bp is None:
                continue
            used = write_pptx.html_baseline(fam, size, lh) - write_pptx.pptx_baseline(fam, size, lh)
            obs_pptx = (bp + 1) / k2 - (cy + used)        # where the app put the baseline below the box top
            obs_html = (bh + 1) / k2 - cy                 # where Chromium put it
            # we want: pptx model == what the app does; keep HTML as the reference
            rows.setdefault(fam, []).append((lh, size, obs_pptx, obs_html - write_pptx.html_baseline(fam, size, lh)))
        for fam, rs in rows.items():
            sll = sum(r_[0] ** 2 for r_ in rs); sls = sum(r_[0] * r_[1] for r_ in rs); sss = sum(r_[1] ** 2 for r_ in rs)
            slo = sum(r_[0] * r_[2] for r_ in rs); sso = sum(r_[1] * r_[2] for r_ in rs)
            det = sll * sss - sls * sls
            a, b = (slo * sss - sso * sls) / det, (sll * sso - sls * slo) / det
            # Chromium's own offset from the half-leading model (font-specific rounding): fold it in
            hb = sum(r_[3] / r_[1] for r_ in rs) / len(rs)
            out[fam] = {"a": round(a, 5), "b": round(b - hb, 5), "renderer": "LibreOffice", "auto": True,
                        "max_resid_pt": round(max(abs(a * r_[0] + b * r_[1] - r_[2]) for r_ in rs), 3)}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if out:
        cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
        cache.update(out)
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        json.dump(cache, open(cache_path, "w"), indent=1)
        write_pptx.load_extra_calibration(cache_path)
    return out
