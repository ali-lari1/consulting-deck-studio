"""Turn ingested project files into layout data blocks, and compare periods.

Every number in an emitted block comes from the source file; derived values (RAG from slip, variance in days,
scores, movement since last period) are computed and named in a "_derivation" key so the facts ledger can cite
them. The agent still edits wording, picks what to show, and writes the action title.
"""
import datetime


def _dt(s):
    return datetime.date(*[int(x) for x in s[:10].split("-")]) if s else None


def _days(a, b):
    return (_dt(b) - _dt(a)).days if a and b else None


def _rag_from_slip(slip, amber_days=10):
    if slip is None:
        return None
    return "G" if slip <= 0 else "A" if slip <= amber_days else "R"


def _fmt_d(s):
    d = _dt(s)
    return "%d %s" % (d.day, "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()[d.month - 1]) if d else ""


def gantt(sch, max_rows=8, amber_days=10, milestones=3):
    acts = [a for a in sch["activities"] if not a["summary"] and a["forecast"][0] and a["forecast"][1]]
    groups = {}
    for a in acts:
        groups.setdefault(a["wbs_top"] or a["wbs"] or "Programme", []).append(a)
    rows = []
    for name, g in groups.items():
        ps = [a["planned"][0] for a in g if a["planned"][0]]
        pf = [a["planned"][1] for a in g if a["planned"][1]]
        fs, ff = min(a["forecast"][0] for a in g), max(a["forecast"][1] for a in g)
        base = [min(ps), max(pf)] if ps and pf else None
        slip = _days(base[1], ff) if base else None
        rows.append({"name": name, "rag": _rag_from_slip(slip, amber_days), "critical": any(a["critical"] for a in g),
                     "baseline": base, "forecast": [fs, ff], "_slip_days": slip})
    rows.sort(key=lambda r_: r_["forecast"][0])
    if len(rows) > max_rows:
        rows = sorted(rows, key=lambda r_: (not r_["critical"], -(r_["_slip_days"] or 0)))[:max_rows]
        rows.sort(key=lambda r_: r_["forecast"][0])
    ms = [a for a in sch["activities"] if a["milestone"] and a["forecast"][1] and not a["actual"][1]]
    key_ms = []
    if ms:
        final = max(ms, key=lambda a: a["forecast"][1])          # the end milestone (handover, completion)
        key_ms.append(final)
        rest = [a for a in ms if a is not final]
        rest.sort(key=lambda a: (not a["critical"], -(_days(a["planned"][1], a["forecast"][1]) or 0)))
        key_ms += rest[:milestones - 1]
    key_ms.sort(key=lambda a: a["forecast"][1])
    all_dates = [d for r_ in rows for d in (r_["forecast"] + (r_["baseline"] or [])) if d] + [a["forecast"][1] for a in key_ms]
    data = {
        "exhibit": "Schedule, baseline vs current forecast",
        "unit": "%s, data date %s" % (sch.get("project") or sch["source"], _fmt_d(sch.get("data_date"))),
        "start": min(all_dates)[:7] + "-01", "end": max(all_dates), "today": sch.get("data_date"),
        "rows": [{k: v for k, v in r_.items() if not k.startswith("_") and v is not None} for r_ in rows],
        "milestones": [{"name": a["name"], "baseline": a["planned"][1] or a["forecast"][1], "forecast": a["forecast"][1]} for a in key_ms],
        "_derivation": {"source": sch["source"], "rag": "finish slip vs planned, calendar days: <=0 G, <=%d A, else R" % amber_days,
                        "slips_days": {r_["name"]: r_["_slip_days"] for r_ in rows}},
    }
    return data


def timeline(sch, limit=8):
    ms = sorted([a for a in sch["activities"] if a["milestone"] and a["forecast"][1]], key=lambda a: a["forecast"][1])[:limit]
    if not ms:
        return {"_note": "no milestones in %s" % sch["source"]}
    return {"start": ms[0]["forecast"][1][:7] + "-01", "end": ms[-1]["forecast"][1],
            "events": [{"date": a["forecast"][1], "label": a["name"], "done": bool(a["actual"][1])} for a in ms],
            "_derivation": {"source": sch["source"], "done": "actual finish recorded"}}


def lookahead(sch, days=90, limit=6, amber_days=10):
    dd = _dt(sch.get("data_date")) or datetime.date.today()
    end = dd + datetime.timedelta(days=days)
    ms = [a for a in sch["activities"] if a["milestone"] and a["forecast"][1] and dd <= _dt(a["forecast"][1]) <= end]
    ms.sort(key=lambda a: a["forecast"][1])
    ms = ms[:limit]
    allm = [a for a in sch["activities"] if a["milestone"] and a["forecast"][1] and not a["actual"][1]]
    if allm:
        final = max(allm, key=lambda a: a["forecast"][1])
        if final not in ms:
            ms = ms[:limit - 1] + [final]          # always show the end milestone, even beyond the window
    rows = []
    for a in ms:
        v = _days(a["planned"][1], a["forecast"][1]) if a["planned"][1] else None
        rows.append({"milestone": a["name"], "baseline": _fmt_d(a["planned"][1]), "forecast": _fmt_d(a["forecast"][1]),
                     "variance": "On plan" if not v else "%+d days" % v, "rag": _rag_from_slip(v, amber_days) or "G"})
    return {"title": "Look-ahead: key milestones in the next %d days" % days, "rows": rows,
            "_derivation": {"source": sch["source"], "window": "%s to %s" % (dd, end)}}


def _sheet(tbl, kind, name=None):
    for s in tbl["sheets"]:
        if (name and s["name"] == name) or (not name and s["kind"] == kind):
            return s
    for s in tbl["sheets"]:
        if not name:
            return s
    raise ValueError("no sheet of kind %s in %s" % (kind, tbl["source"]))


def risk_heatmap(tbl, prev=None, top=6, sheet=None):
    s = _sheet(tbl, "risk", sheet)
    rows = [r_ for r_ in s["rows"] if r_.get("l") and r_.get("i") and str(r_.get("status", "")).lower() not in ("closed", "retired")]
    rows.sort(key=lambda r_: -(r_["l"] * r_["i"]))
    prev_map = {}
    if prev:
        for r_ in _sheet(prev, "risk", sheet)["rows"]:
            if r_.get("id") and r_.get("l") and r_.get("i"):
                prev_map[str(r_["id"])] = [r_["l"], r_["i"]]
    risks = []
    for r_ in rows[:top]:
        rk = {"id": str(r_.get("id", "")), "title": str(r_.get("title", "")), "owner": str(r_.get("owner", "")),
              "l": r_["l"], "i": r_["i"], "mitigation": str(r_.get("mitigation", ""))}
        pv = prev_map.get(rk["id"]) or ([r_["prev_l"], r_["prev_i"]] if r_.get("prev_l") and r_.get("prev_i") else None)
        if pv:
            rk["prev"] = pv
        risks.append(rk)
    new = [r_["id"] for r_ in risks if prev_map and r_["id"] not in prev_map]
    open_scores = [r_["l"] * r_["i"] for r_ in rows]
    return {"risks": risks, "_derivation": {"source": tbl["source"],
                                            "selection": "up to %d open risks by likelihood x impact (%d open in register)" % (top, len(rows)),
                                            "open_red_15plus": sum(1 for v in open_scores if v >= 15),
                                            "open_amber_8_14": sum(1 for v in open_scores if 8 <= v < 15),
                                            "previous": "last snapshot" if prev else "previous-score columns" if any("prev" in x for x in risks) else "none",
                                            "new_this_period": new}}


def raid_log(tbl, sheet=None, limit=12):
    s = _sheet(tbl, "raid", sheet)
    items = []
    for r_ in s["rows"][:limit]:
        t = str(r_.get("type", "")).strip().title()
        t = {"R": "Risk", "A": "Assumption", "I": "Issue", "D": "Dependency"}.get(t[:1], t) if len(t) <= 1 else t
        items.append({"type": t, "id": str(r_.get("id", "")), "description": str(r_.get("title", "")), "owner": str(r_.get("owner", "")),
                      "due": str(r_.get("due", "")), "rag": r_.get("rag", ""), "status": str(r_.get("mitigation") or r_.get("status") or "")})
    return {"items": items, "_derivation": {"source": tbl["source"], "rows": len(s["rows"]), "shown": len(items)}}


def benefits(tbl, sheet=None):
    s = _sheet(tbl, "benefits", sheet)
    out = []
    for r_ in s["rows"]:
        try:
            out.append({"name": str(r_.get("title", "")), "owner": str(r_.get("owner", "")), "unit": str(r_.get("unit", "")),
                        "baseline": float(r_["baseline"]), "target": float(r_["target"]), "actual": float(r_["actual"]),
                        "rag": r_.get("rag", ""), "due": str(r_.get("due", ""))})
        except (KeyError, TypeError, ValueError):
            continue
    return {"benefits": out, "_derivation": {"source": tbl["source"], "progress": "(actual - baseline) / (target - baseline)"}}


def changes_table(changes):
    """Diff output -> table layout data ('what changed since last period')."""
    rows = []
    for c in changes:
        if c["kind"] == "milestone":
            rows.append([c["name"], _fmt_d(c["from"]), _fmt_d(c["to"]), "%+d days" % c["moved_days"]])
        elif c["kind"] == "milestone_achieved":
            rows.append([c["name"], "", "Achieved " + _fmt_d(c["on"]), ""])
        elif c["kind"] == "risk_moved":
            rows.append(["Risk %s: %s" % (c["id"], c["title"]), "Score %s" % c["from"], "Score %s" % c["to"], "%+d" % (c["to"] - c["from"])])
        elif c["kind"] == "risk_new":
            rows.append(["Risk %s: %s" % (c["id"], c["title"]), "New", "Score %s" % c.get("score", ""), ""])
        elif c["kind"] == "risk_removed":
            rows.append(["Risk %s: %s" % (c["id"], c["title"]), "", "Closed or removed", ""])
    return {"exhibit": "What changed since the last report",
            "columns": [{"name": "Item", "width": 0.46, "kind": "bold"}, {"name": "Last report", "width": 0.18},
                        {"name": "This report", "width": 0.18}, {"name": "Change", "width": 0.18, "kind": "number"}],
            "rows": rows, "_derivation": {"source": "ingest.py --diff", "items": len(rows)}}


def diff(cur_sched=None, prev_sched=None, cur_risk=None, prev_risk=None, amber_days=10):
    """What changed since the last snapshot: milestone moves, new/closed/escalated risks. Lines for the status deck."""
    out = []
    if cur_sched and prev_sched:
        pm = {a["id"]: a for a in prev_sched["activities"] if a["milestone"]}
        for a in cur_sched["activities"]:
            if a["milestone"] and a["id"] in pm and a["forecast"][1] and pm[a["id"]]["forecast"][1]:
                d = _days(pm[a["id"]]["forecast"][1], a["forecast"][1])
                if d:
                    out.append({"kind": "milestone", "id": a["id"], "name": a["name"], "moved_days": d,
                                "from": pm[a["id"]]["forecast"][1], "to": a["forecast"][1]})
                if a["actual"][1] and not pm[a["id"]]["actual"][1]:
                    out.append({"kind": "milestone_achieved", "id": a["id"], "name": a["name"], "on": a["actual"][1]})
    if cur_risk and prev_risk:
        c = {str(r_.get("id")): r_ for r_ in _sheet(cur_risk, "risk")["rows"] if r_.get("id")}
        p = {str(r_.get("id")): r_ for r_ in _sheet(prev_risk, "risk")["rows"] if r_.get("id")}
        for k, r_ in c.items():
            if k not in p:
                out.append({"kind": "risk_new", "id": k, "title": r_.get("title"), "score": r_.get("score")})
            elif r_.get("score") and p[k].get("score") and r_["score"] != p[k]["score"]:
                out.append({"kind": "risk_moved", "id": k, "title": r_.get("title"), "from": p[k]["score"], "to": r_["score"]})
        for k in p:
            if k not in c:
                out.append({"kind": "risk_removed", "id": k, "title": p[k].get("title")})
    return out
