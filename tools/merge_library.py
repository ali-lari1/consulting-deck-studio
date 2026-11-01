#!/usr/bin/env python3
"""Merge the research sweeps (research/raw/decks-*.json) into skills/consulting-deck-studio/data/decks.json.

- one schema; stable ids; de-duplicated by URL and by firm+title
- practice: pmo | capital | strategy | management (+ also: secondary practice)
- operations/service reviews found by the strategy sweep move to management (strategy kept as 'also')
- raw deck types mapped to the playbook deck types in references/deck-types/*.md ('playbook')
- tier: 1 MBB/Big4-authored, 2 client deck presenting MBB/Big4 work or firm slide-format publications, 3 specialist firm
- format: slides (layout exemplar) | report (content reference only)
"""
import collections
import datetime
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "research", "raw")
OUT = os.path.join(ROOT, "skills", "consulting-deck-studio", "data", "decks.json")
FILES = ["decks-strategy.json", "decks-management.json", "decks-capital-pmo.json", "decks-capital-tier2.json", "decks-pmo.json"]
STRATEGY_TYPES = {"growth-strategy", "market-entry", "economic-development", "due-diligence"}

PLAYBOOK = {
    "pmo": {"status-report": "status-report", "pmo-dashboard": "dashboard", "steerco-pack": "steerco", "schedule-review": "schedule-review",
            "risk-register": "risk-review", "ivv-report": "assurance", "health-check": "assurance", "pmo-setup": "pmo-setup",
            "go-live-readiness": "go-live", "benefits-tracking": "benefits", "transformation-office": "steerco",
            "independent-review": "assurance", "lessons-learned": "close-out"},
    "capital": {"stage-gate": "gate-paper", "business-case": "gate-paper", "independent-review": "independent-review",
                "cost-review": "cost-review", "schedule-review": "independent-review", "risk-register": "qra",
                "delivery-model": "delivery-model", "programme-prioritisation": "prioritisation", "recovery-plan": "recovery-plan",
                "benefits-realisation": "gate-paper", "pmo-dashboard": "owners-report", "status-report": "owners-report",
                "mobilisation": "delivery-model", "benchmarking": "benchmarking", "lessons-learned": "close-out"},
    "strategy": {"growth-strategy": "growth-strategy", "market-entry": "market-entry", "due-diligence": "due-diligence",
                 "economic-development": "economic-development", "portfolio-review": "portfolio", "board-update": "board-update",
                 "benchmarking": "diagnostic", "operating-model": "diagnostic"},
    "management": {"diagnostic": "diagnostic", "cost-review": "cost-review", "operating-model": "operating-model",
                   "org-design": "operating-model", "transformation-roadmap": "transformation", "steerco-update": "transformation-office",
                   "pmi": "pmi", "change-management": "change-plan", "benchmarking": "service-review", "business-case": "transformation",
                   "board-update": "diagnostic", "portfolio-review": "cost-review", "growth-strategy": "transformation",
                   "due-diligence": "diagnostic", "economic-development": "service-review"},
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def norm_url(u):
    return re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower()).rstrip("/")


def practice_of(r):
    p = r.get("practice", "")
    p = {"capital-projects": "capital"}.get(p, p)
    return p


def main():
    seen_url, seen_key, out = {}, {}, []
    dropped = []
    for f in FILES:
        for r in json.load(open(os.path.join(RAW, f), encoding="utf-8")):
            p = practice_of(r)
            types = list(r.get("deck_types") or [])
            also = None
            if p == "strategy" and "operating-model" in types and not (STRATEGY_TYPES - {"growth-strategy"}) & set(types):
                p, also = "management", "strategy"
            u = norm_url(r.get("url"))
            k = (slug(r.get("firm", ""))[:12], slug(r.get("title", ""))[:40])
            if (u and u in seen_url) or k in seen_key:
                prev = seen_url.get(u) or seen_key.get(k)
                if p != prev["practice"] and p not in (prev.get("also") or []):
                    prev.setdefault("also", []).append(p)
                dropped.append((f, r.get("title", "")[:50]))
                continue
            rec = {
                "id": slug("%s-%s-%s" % (r.get("firm", "").split()[0], r.get("year") or "nd", r.get("title", "")))[:70],
                "title": r.get("title"), "firm": r.get("firm"), "firm_group": r.get("firm_group"), "tier": r.get("tier"),
                "practice": p, "also": [also] if also else [], "format": r.get("format") or "slides",
                "playbook": sorted({PLAYBOOK[p].get(t) for t in types if PLAYBOOK[p].get(t)}),
                "deck_types": types, "client": r.get("client"), "client_type": r.get("client_type"), "sector": r.get("sector"),
                "year": r.get("year"), "url": r.get("url"), "source_url": r.get("source_url"),
                "publication_route": r.get("publication_route"), "slide_count": r.get("slide_count") or r.get("page_count"),
                "verified": r.get("verified"),
                "sequence": r.get("slide_sequence") or r.get("section_sequence") or [],
                "storyline_pattern": r.get("storyline_pattern"), "signature_slides": r.get("signature_slides") or [],
                "design": r.get("design"), "design_quality": r.get("design_quality"),
                "standout_moves": r.get("standout_moves") or [], "weaknesses": r.get("weaknesses") or [],
                "content_value": r.get("content_value"), "rag_definitions": r.get("rag_definitions"), "caveat": r.get("caveat"),
            }
            rec = {k_: v for k_, v in rec.items() if v not in (None, "", [], {})}
            if u:
                seen_url[u] = rec
            seen_key[k] = rec
            out.append(rec)
    ids = collections.Counter(r["id"] for r in out)
    for r in out:
        if ids[r["id"]] > 1:
            r["id"] = r["id"][:64] + "-" + norm_url(r.get("url"))[-5:].replace("/", "")
    out.sort(key=lambda r: (["pmo", "capital", "strategy", "management"].index(r["practice"]), r["tier"], -(r.get("year") or 0)))
    meta = {"generated": datetime.date.today().isoformat(), "count": len(out),
            "note": "Publicly available consulting decks and reports, verified by opening each one. Tier 1 = authored by "
                    "MBB/Big 4; tier 2 = client material presenting MBB/Big 4 work, or firm slide-format publications; tier 3 = "
                    "specialist firms. format 'report' records are content references (structure, fields, finding formats), "
                    "not layout exemplars. Use for patterns and inspiration; never copy.",
            "by_practice": dict(collections.Counter(r["practice"] for r in out)),
            "decks": out}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(meta, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%d records (%d duplicates dropped) -> %s" % (len(out), len(dropped), os.path.relpath(OUT, ROOT)))
    for p in ("pmo", "capital", "strategy", "management"):
        rs = [r for r in out if r["practice"] == p]
        also = [r for r in out if p in r.get("also", [])]
        print("  %-10s %3d (+%d secondary)  tier %s  format %s" % (
            p, len(rs), len(also), dict(sorted(collections.Counter(r["tier"] for r in rs).items())),
            dict(collections.Counter(r["format"] for r in rs))))
        print("             playbook: %s" % dict(collections.Counter(t for r in rs for t in r.get("playbook", [])).most_common()))


if __name__ == "__main__":
    main()
