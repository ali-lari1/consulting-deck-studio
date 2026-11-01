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


# Mandatory content by deck type (references/deck-types/*.md). Each rule: (kind, arg, message)
#   layouts: any of these layouts present;  text: regex found anywhere;  early: one of these layouts in the first N slides
DECK_RULES = {
    "status-report": [("layouts", {"status-summary", "rag-dashboard"}, "no status overview (status-summary or rag-dashboard)"),
                      ("decisions", None, "no decisions needed (decisions slide or status-summary decisions)"),
                      ("layouts", {"gantt", "timeline", "table"}, "no milestone view (gantt, timeline or milestone table)"),
                      ("layouts", {"risk-heatmap", "raid-log"}, "no risk view (risk-heatmap or raid-log)"),
                      ("text", r"(?i)look-?ahead|next (30|60|90) days|next period", "no look-ahead")],
    "steerco": [("early", ({"decisions", "status-summary"}, 4), "decisions are not in the first four slides"),
                ("decisions", None, "no decisions slide")],
    "dashboard": [("layouts", {"rag-dashboard", "table", "scatter"}, "no portfolio view")],
    "risk-review": [("layouts", {"risk-heatmap"}, "no risk heat map"),
                    ("text", r"(?i)likelihood|probability", "risk scoring scale not described")],
    "gate-paper": [("layouts", {"options-matrix", "columns"}, "no options assessment"),
                   ("layouts", {"p-curve"}, "no QRA / confidence level (p-curve)"),
                   ("text", r"(?i)\bclass [1-5]\b|estimate class", "estimate class not stated"),
                   ("text", r"(?i)\bP(50|80|90)\b", "P50/P80 not stated"),
                   ("decisions", None, "no decision requested")],
    "cost-review": [("layouts", {"waterfall"}, "no budget-to-EAC bridge (waterfall)"),
                    ("text", r"(?i)nominal|real terms|price base", "price base (real or nominal) not stated")],
    "schedule-review": [("layouts", {"gantt"}, "no Gantt"), ("text", r"(?i)critical path", "critical path not discussed")],
    "diagnostic": [("layouts", {"issue-tree", "driver-tree"}, "no issue or driver tree"), ("early", ({"exec-summary", "key-numbers"}, 3), "answer is not up front")],
    "strategy": [("early", ({"exec-summary"}, 3), "no executive summary up front"), ("decisions", None, "no recommendation or decision slide")],
    "operating-model": [("layouts", {"before-after"}, "no current vs target view"), ("layouts", {"raci", "org-chart"}, "no decision rights or structure")],
    "transformation": [("layouts", {"roadmap"}, "no roadmap"), ("layouts", {"waterfall", "benefits-tracker", "key-numbers"}, "no value case")],
}


def deck_rules(meta, slides):
    out = []
    dt = (meta.get("deck_type") or "").strip()
    lays = [s["layout"] for s in slides]
    blob = " ".join([s["title"] for s in slides] + [t for s in slides for t in _texts(s["data"])] +
                    [f for s in slides for f in s.get("footnotes", [])] + [s.get("notes", "") for s in slides])
    content = [s for s in slides if s["layout"] not in ("title", "agenda", "section")]
    for kind, arg, msg in DECK_RULES.get(dt, []):
        ok = True
        if kind == "layouts":
            ok = bool(arg & set(lays))
        elif kind == "text":
            ok = bool(re.search(arg, blob))
        elif kind == "decisions":
            ok = "decisions" in lays or any(s["layout"] == "status-summary" and s["data"].get("decisions") for s in slides) \
                or any(s["layout"] == "options-matrix" and s["data"].get("recommended") for s in slides)
        elif kind == "early":
            ok = any(s["layout"] in arg[0] for s in content[:arg[1]])
        if not ok:
            out.append(("warn", 0, "%s deck: %s (references/deck-types)" % (dt, msg)))
    rag_used = any(l in ("status-summary", "rag-dashboard", "risk-heatmap", "raid-log", "benefits-tracker") for l in lays) or \
        any(c.get("kind") == "rag" for s in slides for c in s["data"].get("columns", []) if isinstance(c, dict))
    if rag_used and not re.search(r"(?i)green[^.]{0,80}(amber|red)|amber[^.]{0,80}red|red is|red:|rag (policy|definitions)", blob):
        out.append(("warn", 0, "RAG is used but never defined; add a footnote or appendix definition (standards.md)"))
    if len(content) > 6 and not any(s["layout"] in ("exec-summary", "status-summary", "key-numbers", "decisions") for s in content[:3]):
        out.append(("warn", 0, "the answer is not in the first three content slides (exec-summary or status-summary)"))
    return out
