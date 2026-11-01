"""Copy and structure lint for consulting decks. Returns findings as (level, slide_no, message)."""
import re

BANNED = [
    "delve", "underscore", "showcase", "foster", "leverage", "harness", "unlock", "elevate", "navigate the",
    "streamline", "tapestry", "testament to", "realm", "landscape", "journey", "pivotal", "crucial", "vital",
    "robust", "seamless", "holistic", "cutting-edge", "game-changer", "game changer", "transformative",
    "it is important to note", "it's worth noting", "worth noting", "in today's", "ever-changing", "at its core",
    "when it comes to", "in order to", "moving forward", "going forward", "at the end of the day", "synergies",
    "best-in-class", "world-class", "paradigm shift", "low-hanging fruit", "boil the ocean", "move the needle",
    "circle back", "deep dive", "touch base", "bandwidth", "value-add", "thought leadership", "not only",
    "in conclusion", "ultimately", "groundbreaking", "remarkable", "vibrant", "stunning", "may potentially",
    "could possibly", "significant", "substantial",
]
CONTENT_EXEMPT = {"title", "section", "agenda"}
NUM = re.compile(r"(?<![\w.])[£$€]?\d[\d,.]*\s?(%|m|bn|k|x|pp|weeks?|days?|months?)?\b")


def _texts(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in ("layout", "icon", "kind", "align", "start", "end", "today", "baseline", "forecast", "rag",
                         "trend", "key", "recommended", "float_to"):
                yield from _texts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _texts(v)


def lint(meta, slides, final=False):
    out = []
    for n, s in enumerate(slides, 1):
        lay = s["layout"]
        title = s["title"]
        words = len(title.split())
        texts = [title] + list(_texts(s["data"])) + [s.get("sowhat", "")] + s.get("footnotes", [])
        blob = " ".join(t for t in texts if t)
        if lay not in CONTENT_EXEMPT:
            if words < 6:
                out.append(("warn", n, "title reads like a topic label (%d words); state the takeaway" % words))
            if words > 28:
                out.append(("warn", n, "title is %d words; aim for 15-25" % words))
            if title.rstrip().endswith("."):
                out.append(("warn", n, "title ends with a full stop"))
            if NUM.search(blob) and not (s.get("source") or meta.get("source")):
                out.append(("warn", n, "slide has numbers but no source line"))
        low = blob.lower()
        for p in BANNED:
            if re.search(r"\b" + re.escape(p) + r"\b", low):
                out.append(("warn", n, "phrase to cut or replace with a fact: '%s'" % p))
        if "—" in blob:
            out.append(("warn", n, "em dash: rewrite as two sentences or use a colon"))
        ph = re.findall(r"\[\[[^\]]+\]\]", blob)
        if ph:
            out.append(("error" if final else "info", n, "%d placeholder(s) open: %s" % (len(ph), ", ".join(ph[:3]))))
        if lay not in CONTENT_EXEMPT and not s.get("notes"):
            out.append(("info", n, "no speaker notes"))
    return out
