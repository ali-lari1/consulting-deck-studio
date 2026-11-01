#!/usr/bin/env python3
"""Find comparable real consulting decks in the bundled library (data/decks.json) for patterns and inspiration.

Usage:
    python3 find_decks.py [--practice pmo|capital|strategy|management] [--type <playbook type>] [--tier 1-2]
                          [--format slides|report] [--sector rail] [--q "keyword"] [--limit 8] [--full] [--stats]

Examples:
    python3 find_decks.py --practice pmo --type status-report --tier 1-3 --limit 6
    python3 find_decks.py --practice capital --type gate-paper --format slides
    python3 find_decks.py --q "operating model" --tier 1-2
    python3 find_decks.py --stats

Tier 1 = authored by MBB/Big 4; 2 = client material presenting their work or firm slide publications; 3 = specialist
firms. Format 'report' = content reference (fields, finding formats), not a layout exemplar. Use the patterns;
never copy wording, layouts or branding. Standard library only.
"""
import collections
import json
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "decks.json")


def arg(argv, k, default=None):
    return argv[argv.index(k) + 1] if k in argv else default


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    lib = json.load(open(DATA, encoding="utf-8"))
    decks = lib["decks"]
    if "--stats" in argv:
        print("%d decks (generated %s)" % (len(decks), lib["generated"]))
        for p in ("pmo", "capital", "strategy", "management"):
            rs = [d for d in decks if d["practice"] == p or p in d.get("also", [])]
            print("  %-10s %3d  tiers %s  types %s" % (p, len(rs), dict(sorted(collections.Counter(d["tier"] for d in rs).items())),
                                                      ", ".join("%s %d" % kv for kv in collections.Counter(
                                                          t for d in rs for t in d.get("playbook", [])).most_common(8))))
        return 0
    p, t, fm = arg(argv, "--practice"), arg(argv, "--type"), arg(argv, "--format")
    tier = arg(argv, "--tier", "1-3")
    lo, hi = (int(x) for x in (tier.split("-") if "-" in tier else (tier, tier)))
    sector, q = (arg(argv, "--sector") or "").lower(), (arg(argv, "--q") or "").lower()
    limit = int(arg(argv, "--limit", 8))
    out = []
    for d in decks:
        if p and d["practice"] != p and p not in d.get("also", []):
            continue
        if t and t not in d.get("playbook", []) and t not in d.get("deck_types", []):
            continue
        if fm and d.get("format") != fm:
            continue
        if not lo <= d.get("tier", 3) <= hi:
            continue
        if sector and sector not in (d.get("sector") or "").lower():
            continue
        blob = json.dumps(d, ensure_ascii=False).lower()
        if q and q not in blob:
            continue
        score = (3 - d.get("tier", 3)) * 2 + (d.get("design_quality") or 3) + (1 if d.get("format") == "slides" else 0) + \
            (2 if t and t in d.get("playbook", []) else 0) + (1 if (d.get("year") or 2000) > 2018 else 0) - \
            (3 if isinstance(d.get("slide_count"), int) and d["slide_count"] < 6 else 0)
        out.append((score, d))
    out.sort(key=lambda x: -x[0])
    if not out:
        print("No matches. Widen --tier, drop --type, or try --q. (--stats shows coverage.)")
        return 0
    for _, d in out[:limit]:
        print("\n[%s] %s (%s, %s) tier %s, %s, %s slides/pages" % (
            d["id"], d["title"], d.get("firm"), d.get("year") or "n.d.", d.get("tier"), d.get("format"), d.get("slide_count") or "?"))
        print("  client: %s | sector: %s | types: %s" % (d.get("client"), d.get("sector"), ", ".join(d.get("playbook", []))))
        print("  url: %s" % d.get("url"))
        if d.get("storyline_pattern"):
            print("  storyline: %s" % d["storyline_pattern"][:220])
        seq = d.get("sequence", [])
        if seq:
            n = len(seq) if "--full" in argv else 8
            print("  sequence: " + " | ".join(s[:70] for s in seq[:n]) + (" | ..." if len(seq) > n else ""))
        for m in d.get("standout_moves", [])[:3 if "--full" not in argv else 10]:
            print("  + %s" % m)
        if "--full" in argv:
            for w in d.get("weaknesses", []):
                print("  - %s" % w)
            if d.get("content_value"):
                print("  content value: %s" % d["content_value"])
            if d.get("rag_definitions"):
                print("  RAG definitions: %s" % d["rag_definitions"])
        if d.get("caveat"):
            print("  caveat: %s" % d["caveat"][:200])
    print("\n%d match(es); showing %d." % (len(out), min(limit, len(out))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
