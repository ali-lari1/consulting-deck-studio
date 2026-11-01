#!/usr/bin/env python3
"""Scaffold a deck project and (optionally) link it to project files.

Usage:
    python3 init_project.py <project_dir> --name "Engagement name" [--practice pmo|capital|strategy|management]
                            [--deck status-report|steerco|gate-paper|diagnostic|strategy|...] [--source FILE ...]

Creates deck.md (front matter + a first slide), facts.md, brief.md, research/, assets/, fonts/ and
.cds/project.json. --source files (schedules, registers, notes, transcripts, prior decks) are recorded so
`ingest.py <project> --refresh` re-reads them every period. Never overwrites existing files.
"""
import datetime
import json
import os
import sys

FACTS = """# Facts ledger

Every number, date, name and claim on a slide must be a row here. Status: client | file | sourced | computed | estimate | placeholder.

| # | Fact | Value | Source (file, page or speaker) | As of | Status | Slides |
|---|---|---|---|---|---|---|
"""
BRIEF = """# Brief

**Decision this deck drives:** [[...]]
**Audience (who decides, who is sceptical):** [[...]]
**Presented or pre-read; time and slide budget:** [[...]]
**Governing thought (one sentence):** [[...]]
**Brand:** [[template / guidelines / website / house]]

## Assumptions to confirm

## Storyline (ghost deck)
Run `python3 SKILL_DIR/scripts/build.py <project> --outline` and paste the table here once deck.md has titles.

## Questions the audience will ask
"""

EMITS_FOR = {".xer": [("gantt", None), ("lookahead", None), ("timeline", None)], ".xml": [("gantt", None), ("lookahead", None)]}


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    p = argv[0]

    def arg(k, default=None):
        return argv[argv.index(k) + 1] if k in argv else default
    name = arg("--name", os.path.basename(os.path.abspath(p)))
    sources = []
    if "--source" in argv:
        i = argv.index("--source") + 1
        while i < len(argv) and not argv[i].startswith("--"):
            sources.append(argv[i])
            i += 1
    for d in ("research/inputs", "research/emit", "assets", "fonts", ".cds/history"):
        os.makedirs(os.path.join(p, d), exist_ok=True)

    def put(rel, text):
        fp = os.path.join(p, rel)
        if not os.path.exists(fp):
            open(fp, "w", encoding="utf-8").write(text)
            print("created", rel)
    put("deck.md", "---\ndeck: %s\ncontext: %s  |  [[meeting]]  |  %s\ntracker: [[Section 1]], [[Section 2]]\nsticker: Draft for discussion\n"
                   "source: [[source]]\n---\n\n# %s\nlayout: title\n\n```json\n{\"subtitle\": \"[[subtitle]]\", \"date\": \"%s\"}\n```\n" % (
                       name, name, datetime.date.today().strftime("%B %Y"), name, "%d %s" % (datetime.date.today().day, datetime.date.today().strftime("%B %Y"))))
    put("facts.md", FACTS)
    put("brief.md", BRIEF)
    emits = []
    for s in sources:
        stem, ext = os.path.splitext(os.path.basename(s))
        ext = ext.lower()
        for lay, _ in EMITS_FOR.get(ext, []):
            emits.append({"layout": lay, "from": "%s.schedule.json" % stem})
        if ext in (".xlsx", ".csv") and any(w in stem.lower() for w in ("risk",)):
            emits.append({"layout": "risk-heatmap", "from": "%s.table.json" % stem, "prev": True, "top": 6})
        if ext in (".xlsx", ".csv") and "raid" in stem.lower():
            emits.append({"layout": "raid-log", "from": "%s.table.json" % stem})
        if ext in (".xlsx", ".csv") and "benefit" in stem.lower():
            emits.append({"layout": "benefits", "from": "%s.table.json" % stem})
    cfg_p = os.path.join(p, ".cds", "project.json")
    if not os.path.exists(cfg_p):
        cfg = {"name": name, "practice": arg("--practice"), "deck_type": arg("--deck"), "created": datetime.date.today().isoformat(),
               "sources": [os.path.relpath(s, p) if not os.path.isabs(s) else s for s in sources], "emits": emits,
               "rag_policy": {"schedule_amber_days": 10, "definitions": {"G": "On track", "A": "At risk, recoverable within tolerance",
                                                                         "R": "Outside tolerance, decision needed"}}}
        json.dump(cfg, open(cfg_p, "w", encoding="utf-8"), indent=1)
        print("created .cds/project.json (%d sources, %d emits)" % (len(sources), len(emits)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
