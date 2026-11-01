"""Parse deck.md, the authoring format.

    ---
    deck: Northline Rail Programme          # deck-level settings (front matter)
    context: Northline Rail Programme | Monthly SteerCo | October 2026
    tracker: Summary, Schedule, Risk, Cost
    sticker: Preliminary
    source: Programme controls period 7 report (Oct 2026)
    ---

    # The programme is six weeks behind its re-baselined date      <- one slide per "# " line (the action title)
    layout: status-summary
    section: Summary
    sowhat: Approving the £14m drawdown by 14 November protects the May 2027 handover
    footnote: Re-baselined at Gate 3, March 2026.                 <- repeatable
    source: Programme controls ...                                 <- overrides the deck source

    ```json
    { ...layout data... }
    ```

    ??? Speaker notes run to the next slide. They become PPTX notes and reader-mode text.

Inline text supports **bold** only. Lists in front matter are comma separated.
"""
import json
import re

LIST_KEYS = {"tracker"}
REPEAT_KEYS = {"footnote"}


class DeckError(Exception):
    pass


def _kv(line):
    m = re.match(r"^([a-z_][a-z0-9_-]*)\s*:\s*(.*)$", line.strip())
    return (m.group(1), m.group(2).strip()) if m else (None, None)


def parse(text):
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    meta = {}
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            k, v = _kv(lines[i])
            if k:
                meta[k] = [x.strip() for x in v.split(",") if x.strip()] if k in LIST_KEYS else v
            i += 1
        i += 1
    slides = []
    cur = None
    mode = "keys"
    buf = []
    for n in range(i, len(lines)):
        line = lines[n]
        if mode == "json":
            if line.strip().startswith("```"):
                try:
                    cur["data"] = json.loads("\n".join(buf) or "{}")
                except ValueError as e:
                    raise DeckError("slide %d (%s): bad JSON in data block: %s" % (len(slides), cur["title"][:40], e))
                mode, buf = "body", []
            else:
                buf.append(line)
            continue
        if line.startswith("# "):
            cur = {"title": line[2:].strip(), "layout": None, "data": {}, "footnotes": [], "notes": "", "line": n + 1}
            slides.append(cur)
            mode = "keys"
            continue
        if cur is None:
            continue
        if line.strip().startswith("```"):
            mode, buf = "json", []
            continue
        if line.strip().startswith("???"):
            mode = "notes"
            cur["notes"] = line.strip()[3:].strip()
            continue
        if mode == "notes":
            cur["notes"] += ("\n" if cur["notes"] else "") + line
            continue
        k, v = _kv(line)
        if k and mode == "keys":
            if k == "footnote":
                cur["footnotes"].append(v)
            else:
                cur[k] = v
        elif line.strip():
            mode = "body"
    for s in slides:
        s["notes"] = s["notes"].strip()
        if not s.get("layout"):
            raise DeckError("slide '%s' (line %d) has no layout:" % (s["title"][:50], s["line"]))
    return meta, slides


def md_runs(text, size=11, color=None, bold=False, font=None):
    """'Forecast moved to **15 May**' -> runs, using components.r for styling."""
    from .components import r
    out = []
    for k, part in enumerate(re.split(r"\*\*", text)):
        if part:
            out.append(r(part, size, bold or (k % 2 == 1), color, font=font))
    return out or [r("", size, bold, color, font=font)]
