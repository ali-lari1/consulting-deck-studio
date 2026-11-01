"""Minimal PNG read/write and image diff, standard library only (for the parity check)."""
import struct
import zlib


class Image:
    def __init__(self, w, h, px):
        self.w, self.h, self.px = w, h, px  # px: bytearray RGB, row-major

    def crop(self, x, y, w, h):
        out = bytearray()
        for r in range(y, y + h):
            out += self.px[(r * self.w + x) * 3:(r * self.w + x + w) * 3]
        return Image(w, h, out)

    def half(self):
        """2x2 box downsample: removes most sub-pixel anti-aliasing noise between renderers."""
        w, h = self.w // 2, self.h // 2
        src, sw = self.px, self.w
        out = bytearray(w * h * 3)
        for y in range(h):
            r0, r1 = (2 * y) * sw * 3, (2 * y + 1) * sw * 3
            for x in range(w):
                a, b = r0 + 6 * x, r1 + 6 * x
                o = (y * w + x) * 3
                for c in range(3):
                    out[o + c] = (src[a + c] + src[a + 3 + c] + src[b + c] + src[b + 3 + c]) >> 2
        return Image(w, h, out)


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def read(path):
    d = open(path, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG: " + path
    i, idat, pal = 8, b"", None
    while i < len(d):
        ln, typ = struct.unpack(">I4s", d[i:i + 8])
        body = d[i + 8:i + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype, _, _, inter = struct.unpack(">IIBBBBB", body)
        elif typ == b"PLTE":
            pal = body
        elif typ == b"IDAT":
            idat += body
        i += 12 + ln
    assert depth == 8 and inter == 0, "only 8-bit non-interlaced PNG supported"
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(idat)
    stride = w * bpp
    prev = bytearray(stride)
    rows = []
    p = 0
    for _ in range(h):
        f = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                left = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((left + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                left = line[x - bpp] if x >= bpp else 0
                ul = prev[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + _paeth(left, prev[x], ul)) & 255
        rows.append(line)
        prev = line
    px = bytearray(w * h * 3)
    o = 0
    for line in rows:
        for x in range(w):
            if ctype == 2:
                px[o:o + 3] = line[3 * x:3 * x + 3]
            elif ctype == 6:
                a = line[4 * x + 3]
                for c in range(3):  # composite on white
                    px[o + c] = (line[4 * x + c] * a + 255 * (255 - a)) // 255
            elif ctype == 3:
                k = line[x] * 3
                px[o:o + 3] = pal[k:k + 3]
            elif ctype == 0:
                px[o:o + 3] = bytes([line[x]] * 3)
            elif ctype == 4:
                g, a = line[2 * x], line[2 * x + 1]
                v = (g * a + 255 * (255 - a)) // 255
                px[o:o + 3] = bytes([v] * 3)
            o += 3
    return Image(w, h, px)


def write(img, path):
    raw = b"".join(b"\x00" + bytes(img.px[y * img.w * 3:(y + 1) * img.w * 3]) for y in range(img.h))

    def chunk(t, b):
        return struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", img.w, img.h, 8, 2, 0, 0, 0)) +
                chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def diff(a, b, tol=40, reach=1):
    """Share of pixels that differ by more than `tol` (max channel) from every pixel within `reach`
    px in the other image, checked both ways. Tolerates one-pixel anti-aliasing shifts, but catches
    moved text, wrong line breaks, missing shapes and colour changes. Returns (ratio, heatmap Image)."""
    assert (a.w, a.h) == (b.w, b.h), "size mismatch %sx%s vs %sx%s" % (a.w, a.h, b.w, b.h)
    w, h = a.w, a.h
    heat = bytearray(a.px)
    for i in range(0, len(heat), 3):  # faded copy of A as background
        v = (heat[i] + heat[i + 1] + heat[i + 2]) // 3
        heat[i:i + 3] = bytes([200 + v // 5] * 3)
    bad = 0

    def miss(src, dst, x, y):
        o = (y * w + x) * 3
        s0, s1, s2 = src[o], src[o + 1], src[o + 2]
        for yy in range(max(0, y - reach), min(h, y + reach + 1)):
            base = yy * w * 3
            for xx in range(max(0, x - reach), min(w, x + reach + 1)):
                q = base + xx * 3
                if abs(dst[q] - s0) <= tol and abs(dst[q + 1] - s1) <= tol and abs(dst[q + 2] - s2) <= tol:
                    return False
        return True

    A, B = a.px, b.px
    for y in range(h):
        for x in range(w):
            o = (y * w + x) * 3
            if abs(A[o] - B[o]) <= tol and abs(A[o + 1] - B[o + 1]) <= tol and abs(A[o + 2] - B[o + 2]) <= tol:
                continue
            if miss(A, B, x, y) or miss(B, A, x, y):
                bad += 1
                heat[o:o + 3] = b"\xe0\x10\x50"
    return bad / float(w * h), Image(w, h, heat)


def side_by_side(images, gap=8):
    h = max(i.h for i in images)
    w = sum(i.w for i in images) + gap * (len(images) - 1)
    out = bytearray(b"\xff" * (w * h * 3))
    x0 = 0
    for im in images:
        for y in range(im.h):
            out[(y * w + x0) * 3:(y * w + x0 + im.w) * 3] = im.px[y * im.w * 3:(y + 1) * im.w * 3]
        x0 += im.w + gap
    return Image(w, h, out)
