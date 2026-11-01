"""Render HTML (headless Chromium) and PPTX (headless LibreOffice) to per-slide PNGs for parity checks."""
import glob
import os
import platform
import shutil
import subprocess
import tempfile

from . import png
from . import scene as S

CANDIDATES_MAC = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Arc.app/Contents/MacOS/Arc",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
CANDIDATES_WIN = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
         "microsoft-edge", "msedge", "brave-browser", "brave"]
SOFFICE = ["/Applications/LibreOffice.app/Contents/MacOS/soffice", r"C:\Program Files\LibreOffice\program\soffice.exe"]
SCALE = 2  # render at 1920x1080


PLAYWRIGHT_PATTERNS = [
    "chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell",
    "chromium_headless_shell-*/chrome-*/headless_shell",
    "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
    "chromium-*/chrome-linux*/chrome", "chromium-*/chrome-win*/chrome.exe",
]


def find_browsers(explicit=None):
    """Every usable Chromium, best first: explicit/env, Playwright headless shell (most reliable
    headless), then installed browsers."""
    found = [c for c in [explicit, os.environ.get("CHROME_PATH")] if c and os.path.exists(c)]
    for root in [os.path.expanduser("~/Library/Caches/ms-playwright"), os.path.expanduser("~/.cache/ms-playwright"),
                 os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")]:
        for pat in PLAYWRIGHT_PATTERNS:
            found += sorted(glob.glob(os.path.join(root, pat)), reverse=True)
    sysname = platform.system()
    found += [c for c in (CANDIDATES_MAC if sysname == "Darwin" else CANDIDATES_WIN if sysname == "Windows" else [])
              if os.path.exists(c)]
    found += [shutil.which(n) for n in NAMES if shutil.which(n)]
    seen, out = set(), []
    for f in found:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def find_browser(explicit=None):
    b = find_browsers(explicit)
    return b[0] if b else None


def find_soffice():
    for c in [os.environ.get("SOFFICE_PATH")] + SOFFICE:
        if c and os.path.exists(c):
            return c
    return shutil.which("soffice") or shutil.which("libreoffice")


def chromium(browser, args, timeout=90):
    """Run one headless Chromium command. With browser=None, try each candidate until one succeeds."""
    if browser is None:
        err = "no Chromium-family browser found (set CHROME_PATH)"
        for b in find_browsers():
            ok, err = chromium(b, args, timeout)
            if ok:
                return True, ""
        return False, err
    prof = tempfile.mkdtemp(prefix="cds-chrome-")
    shell = "headless-shell" in browser or "headless_shell" in browser
    cmd = [browser, "--headless" if shell else "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--hide-scrollbars", "--user-data-dir=" + prof, "--virtual-time-budget=4000",
           "--run-all-compositor-stages-before-draw"] + args
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return r.returncode == 0, r.stderr.decode(errors="ignore")[-800:]
    except subprocess.TimeoutExpired:
        return False, "%s timed out after %ss" % (os.path.basename(browser), timeout)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def html_pngs(html_path, n, out_dir, browser=None):
    """Screenshot a stacked deck (slides edge to edge) once, then crop per slide."""
    shot = os.path.join(out_dir, "_html_full.png")
    ok, err = chromium(browser, ["--force-device-scale-factor=%d" % SCALE,
                                 "--window-size=%d,%d" % (int(S.SLIDE_W), int(S.SLIDE_H) * n),
                                 "--screenshot=" + shot, "file://" + os.path.abspath(html_path)])
    if not ok or not os.path.exists(shot):
        raise SystemExit("Chromium screenshot failed: " + err)
    full = png.read(shot)
    W, H = int(S.SLIDE_W) * SCALE, int(S.SLIDE_H) * SCALE
    paths = []
    for i in range(n):
        p = os.path.join(out_dir, "html-%02d.png" % (i + 1))
        png.write(full.crop(0, i * H, W, H), p)
        paths.append(p)
    os.remove(shot)
    return paths


def pdf(html_path, pdf_path, browser=None):
    ok, err = chromium(browser, ["--no-pdf-header-footer", "--print-to-pdf=" + os.path.abspath(pdf_path),
                                 "file://" + os.path.abspath(html_path)])
    if not ok:
        raise SystemExit("PDF export failed: " + err)
    return pdf_path


def pptx_pngs(single_slide_pptx, out_dir, soffice=None):
    """LibreOffice exports only the first slide to PNG, so callers pass one single-slide pptx per slide."""
    soffice = soffice or find_soffice()
    if not soffice:
        return None
    W, H = int(S.SLIDE_W) * SCALE, int(S.SLIDE_H) * SCALE
    flt = 'png:impress_png_Export:{"PixelWidth":{"type":"long","value":"%d"},"PixelHeight":{"type":"long","value":"%d"}}' % (W, H)
    prof = tempfile.mkdtemp(prefix="cds-lo-")
    try:
        subprocess.run([soffice, "-env:UserInstallation=file://" + prof, "--headless", "--convert-to", flt,
                        "--outdir", out_dir] + list(single_slide_pptx), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=300)
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    return [os.path.join(out_dir, os.path.splitext(os.path.basename(p))[0] + ".png") for p in single_slide_pptx]
