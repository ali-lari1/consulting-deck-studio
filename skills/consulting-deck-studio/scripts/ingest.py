#!/usr/bin/env python3
"""Read project inputs into <project>/research/inputs/*.json, emit layout data, and compare periods.

Usage:
    python3 ingest.py <project> <file> [<file> ...]
        .xer  .xml (MS Project)              -> schedule
        .xlsx .xlsm .csv                     -> registers (risk, RAID, benefits, milestones, cost) or plain tables
        .vtt .srt                            -> transcript (speakers, turns, candidate decisions/actions/risks)
        .docx .md .txt                       -> notes
        .pptx                                -> prior deck (titles, text, notes per slide)
    python3 ingest.py <project> --emit <gantt|timeline|lookahead|risk-heatmap|raid-log|benefits> <input.json>
                      [--prev <older input.json>] [--top N] [--sheet NAME]
        prints a JSON data block for deck.md (also saved under research/emit/)
    python3 ingest.py <project> --refresh              re-read every source in .cds/project.json and re-emit its data
                                                      blocks (vs the latest snapshot); then rebuild the deck
    python3 ingest.py <project> --snapshot <label>     save research/inputs as period <label> (e.g. 2026-10)
    python3 ingest.py <project> --diff <label>         what changed since that period (milestone moves, risk changes)

Everything stays on this machine. Candidates found in notes are pointers for you to check, not facts.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cdslib import emit, ingest_schedule, ingest_tables, ingest_text  # noqa: E402


def detect(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xer":
        return "schedule", ingest_schedule.read_xer
    if ext == ".xml":
        head = open(path, "rb").read(4096).decode("utf-8", "ignore")
        if "schemas.microsoft.com/project" in head or "<Project" in head:
            return "schedule", ingest_schedule.read_mspdi
    if ext in (".xlsx", ".xlsm", ".csv"):
        return "table", ingest_tables.read_table
    if ext in (".vtt", ".srt"):
        return "transcript", ingest_text.read_transcript
    if ext == ".docx":
        return "notes", ingest_text.read_docx
    if ext in (".md", ".txt"):
        head = open(path, "rb").read(2048).decode("utf-8", "ignore")
        if head.startswith("WEBVTT"):
            return "transcript", ingest_text.read_transcript
        return "notes", ingest_text.read_plain
    if ext in (".pptx", ".potx"):
        return "deck", ingest_text.read_pptx
    if ext == ".mpp":
        raise SystemExit("%s: .mpp is binary. In MS Project use File > Save As > XML (*.xml), then ingest that." % path)
    if ext == ".xls":
        raise SystemExit("%s: old .xls format. Re-save as .xlsx or .csv." % path)
    raise SystemExit("%s: unsupported file type %s" % (path, ext))


def summarise(kind, d):
    if kind == "schedule":
        c = d["checks"]
        lines = ["%s: %s, data date %s; %d activities, %d milestones, %d critical" % (
            d["format"], d.get("project"), d.get("data_date"), c["activities"], c["milestones"], c["critical"])]
        lines.append("  checks: missing logic %d (%.0f%%), negative float %d, float > 44d %.0f%%, forecasts in the past not "
                     "actualised %d" % (c["missing_logic"]["count"], c["missing_logic"]["pct"], c["negative_float"]["count"],
                                        c["high_float_over_44d"]["pct"], c["forecast_in_past_not_actualised"]["count"]))
        return lines
    if kind == "table":
        out = []
        for s in d["sheets"]:
            out.append("sheet '%s': %s, %d rows; mapped %s" % (s["name"], s["kind"], len(s["rows"]),
                                                                 ", ".join("%s<-%s" % kv for kv in s["columns"].items())))
            if s["unmapped"]:
                out.append("  unmapped columns (kept under 'extra'): %s" % ", ".join(s["unmapped"][:12]))
        return out
    c = d.get("candidates", {})
    extra = ""
    if kind == "transcript":
        extra = "%d turns, speakers: %s; " % (len(d["turns"]), ", ".join(d["speakers"][:8]) or "not labelled")
    if kind == "deck":
        extra = "%d slides; " % len(d["slides"])
    return ["%s%s candidates: %s" % (extra, kind, ", ".join("%d %s" % (len(v), k) for k, v in c.items()))]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    project = argv[0]
    inputs = os.path.join(project, "research", "inputs")
    os.makedirs(inputs, exist_ok=True)
    if argv[1] == "--refresh":
        cfg_p = os.path.join(project, ".cds", "project.json")
        cfg = json.load(open(cfg_p, encoding="utf-8"))
        files = [os.path.join(project, f) if not os.path.isabs(f) else f for f in cfg.get("sources", [])]
        missing = [f for f in files if not os.path.exists(f)]
        for f in missing:
            print("WARN source not found, skipped: %s" % os.path.relpath(f, project))
        files = [f for f in files if f not in missing]
        if files:
            main([project] + files)
        hist = os.path.join(project, ".cds", "history")
        last = sorted(os.listdir(hist))[-1] if os.path.isdir(hist) and os.listdir(hist) else None
        for e in cfg.get("emits", []):
            if not os.path.exists(os.path.join(inputs, e["from"])):
                continue
            args = [project, "--emit", e["layout"], os.path.join(inputs, e["from"])]
            if e.get("prev") and last and os.path.exists(os.path.join(hist, last, e["from"])):
                args += ["--prev", os.path.join(hist, last, e["from"])]
            if e.get("top"):
                args += ["--top", str(e["top"])]
            import contextlib
            import io
            with contextlib.redirect_stdout(io.StringIO()):
                main(args)
            print("emitted %s from %s%s" % (e["layout"], e["from"], " (vs %s)" % last if "--prev" in args else ""))
        return 0
    if argv[1] == "--snapshot":
        dst = os.path.join(project, ".cds", "history", argv[2])
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(inputs, dst)
        print("saved %d input files as period %s" % (len(os.listdir(dst)), argv[2]))
        return 0
    if argv[1] == "--diff":
        old = os.path.join(project, ".cds", "history", argv[2])

        def load(folder, kind):
            for f in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
                if f.endswith(".%s.json" % kind):
                    yield f, json.load(open(os.path.join(folder, f), encoding="utf-8"))
        cs, ps = dict(load(inputs, "schedule")), dict(load(old, "schedule"))
        ct, pt = dict(load(inputs, "table")), dict(load(old, "table"))
        changes = []
        for f, d in cs.items():
            if f in ps:
                changes += emit.diff(cur_sched=d, prev_sched=ps[f])
        for f, d in ct.items():
            if f in pt and any(s["kind"] == "risk" for s in d["sheets"]):
                changes += emit.diff(cur_risk=d, prev_risk=pt[f])
        print(json.dumps(changes, indent=1, ensure_ascii=False))
        return 0
    if argv[1] == "--emit":
        what, src = argv[2], argv[3]
        d = json.load(open(src, encoding="utf-8"))
        prev = json.load(open(argv[argv.index("--prev") + 1], encoding="utf-8")) if "--prev" in argv else None
        top = int(argv[argv.index("--top") + 1]) if "--top" in argv else None
        sheet = argv[argv.index("--sheet") + 1] if "--sheet" in argv else None
        fn = {"gantt": lambda: emit.gantt(d, max_rows=top or 8), "timeline": lambda: emit.timeline(d, limit=top or 8),
              "lookahead": lambda: emit.lookahead(d, limit=top or 6),
              "risk-heatmap": lambda: emit.risk_heatmap(d, prev, top=top or 6, sheet=sheet),
              "raid-log": lambda: emit.raid_log(d, sheet=sheet, limit=top or 12),
              "benefits": lambda: emit.benefits(d, sheet=sheet)}.get(what)
        if not fn:
            raise SystemExit("unknown --emit target %s" % what)
        out = fn()
        os.makedirs(os.path.join(project, "research", "emit"), exist_ok=True)
        json.dump(out, open(os.path.join(project, "research", "emit", what + ".json"), "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    for path in argv[1:]:
        kind, reader = detect(path)
        d = reader(path)
        stem = os.path.splitext(os.path.basename(path))[0]
        out = os.path.join(inputs, "%s.%s.json" % (stem, kind))
        json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("%s -> %s" % (os.path.basename(path), os.path.relpath(out, project)))
        for line in summarise(kind, d):
            print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
