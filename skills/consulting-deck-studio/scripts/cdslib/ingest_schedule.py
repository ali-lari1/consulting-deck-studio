"""Read schedules: Primavera P6 .xer and MS Project XML (MSPDI, "Save As > XML"). Standard library only.

Both produce the same normalised structure:
  {"source", "format", "project", "data_date", "activities": [
      {id, name, wbs, level, summary, milestone, planned: [s, f], baseline: [s, f] | None, forecast: [s, f],
       actual: [s | None, f | None], pct, float_days, critical, preds: [ids]}],
   "checks": {...}}
Dates are ISO yyyy-mm-dd. "planned" is the P6 target / MSP baseline when present; "forecast" is actual where
known, otherwise early (P6) or scheduled (MSP) dates. .mpp files are binary: ask the user to save as XML.
"""
import os
import xml.etree.ElementTree as ET


def _d(s):
    s = (s or "").strip()
    return s[:10] if len(s) >= 10 and s[4] == "-" else None


def read_xer(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    tables, cur, fields = {}, None, []
    for line in text.splitlines():
        parts = line.rstrip("\r\n").split("\t")
        if parts[0] == "%T":
            cur = parts[1]
            tables[cur] = []
        elif parts[0] == "%F":
            fields = parts[1:]
        elif parts[0] == "%R" and cur:
            tables[cur].append(dict(zip(fields, parts[1:])))
    projs = tables.get("PROJECT", [])
    if not projs:
        raise ValueError("no PROJECT table in %s (is this an XER export?)" % path)
    proj = projs[0]
    pid = proj.get("proj_id")
    cal_hours = {c.get("clndr_id"): float(c.get("day_hr_cnt") or 8) for c in tables.get("CALENDAR", [])}
    wbs = {w["wbs_id"]: w for w in tables.get("PROJWBS", []) if w.get("proj_id") == pid}

    def wbs_path(wid):
        names = []
        while wid in wbs and wbs[wid].get("proj_node_flag") != "Y":
            names.append(wbs[wid]["wbs_name"])
            wid = wbs[wid].get("parent_wbs_id")
        return list(reversed(names))
    preds = {}
    for p in tables.get("TASKPRED", []):
        preds.setdefault(p["task_id"], []).append(p["pred_task_id"])
    acts = []
    code = {t["task_id"]: t.get("task_code") for t in tables.get("TASK", [])}
    for t in tables.get("TASK", []):
        if t.get("proj_id") != pid or t.get("task_type") in ("TT_WBS", "TT_LOE"):
            continue
        hrs = cal_hours.get(t.get("clndr_id"), 8.0) or 8.0
        tf = t.get("total_float_hr_cnt")
        wpath = wbs_path(t.get("wbs_id"))
        a_s, a_f = _d(t.get("act_start_date")), _d(t.get("act_end_date"))
        fs = a_s or _d(t.get("restart_date")) or _d(t.get("early_start_date")) or _d(t.get("target_start_date"))
        ff = a_f or _d(t.get("reend_date")) or _d(t.get("early_end_date")) or _d(t.get("target_end_date"))
        acts.append({
            "id": t.get("task_code"), "name": t.get("task_name"), "wbs": " / ".join(wpath), "wbs_top": wpath[0] if wpath else "",
            "level": len(wpath), "summary": False, "milestone": t.get("task_type") in ("TT_Mile", "TT_FinMile"),
            "planned": [_d(t.get("target_start_date")), _d(t.get("target_end_date"))], "baseline": None,
            "forecast": [fs, ff], "actual": [a_s, a_f],
            "pct": float(t.get("phys_complete_pct") or 0), "float_days": round(float(tf) / hrs, 1) if tf not in (None, "") else None,
            "critical": t.get("driving_path_flag") == "Y" or (tf not in (None, "") and float(tf) <= 0),
            "status": {"TK_Complete": "complete", "TK_Active": "in progress", "TK_NotStart": "not started"}.get(t.get("status_code"), ""),
            "preds": [code.get(p) for p in preds.get(t["task_id"], [])],
        })
    return _finish({"source": os.path.basename(path), "format": "P6 XER", "project": proj.get("proj_short_name"),
                    "data_date": _d(proj.get("last_recalc_date") or proj.get("next_data_date")), "activities": acts})


def read_mspdi(path):
    root = ET.parse(path).getroot()
    ns = {"m": root.tag.split("}")[0][1:]} if root.tag.startswith("{") else {"m": ""}
    q = (lambda t: "m:" + t) if ns["m"] else (lambda t: t)

    def g(el, tag):
        x = el.find(q(tag), ns)
        return x.text if x is not None else None
    tasks = root.findall(".//%s/%s" % (q("Tasks"), q("Task")), ns)
    acts, stack, by_uid = [], [], {}
    for t in tasks:
        if g(t, "UID") in (None, "0") or g(t, "IsNull") == "1":
            continue
        lvl = int(g(t, "OutlineLevel") or 1)
        name = g(t, "Name") or ""
        summary = g(t, "Summary") == "1"
        while stack and stack[-1][0] >= lvl:
            stack.pop()
        opath = [s[1] for s in stack]
        if summary:
            stack.append((lvl, name))
        base = None
        for b in t.findall(q("Baseline"), ns):
            if g(b, "Number") == "0" and g(b, "Start"):
                base = [_d(g(b, "Start")), _d(g(b, "Finish"))]
        slack = g(t, "TotalSlack")
        a_s, a_f = _d(g(t, "ActualStart")), _d(g(t, "ActualFinish"))
        pct = float(g(t, "PercentComplete") or 0)
        uid = g(t, "UID")
        by_uid[uid] = g(t, "ID") or uid
        acts.append({
            "id": g(t, "ID") or uid, "uid": uid, "name": name, "wbs": " / ".join(opath), "wbs_top": opath[0] if opath else name if summary else "",
            "level": lvl, "summary": summary, "milestone": g(t, "Milestone") == "1",
            "planned": base or [_d(g(t, "Start")), _d(g(t, "Finish"))], "baseline": base,
            "forecast": [a_s or _d(g(t, "Start")), a_f or _d(g(t, "Finish"))], "actual": [a_s, a_f], "pct": pct,
            "float_days": round(float(slack) / 4800.0, 1) if slack not in (None, "") else None,
            "critical": g(t, "Critical") == "1",
            "status": "complete" if pct >= 100 else "in progress" if pct > 0 else "not started",
            "preds": [p.findtext(q("PredecessorUID"), namespaces=ns) for p in t.findall(q("PredecessorLink"), ns)],
        })
    for a in acts:
        a["preds"] = [by_uid.get(p, p) for p in a["preds"]]
    return _finish({"source": os.path.basename(path), "format": "MS Project XML", "project": root.findtext(q("Name"), namespaces=ns)
                    or root.findtext(q("Title"), namespaces=ns), "data_date": _d(root.findtext(q("StatusDate"), namespaces=ns) or
                                                                             root.findtext(q("CurrentDate"), namespaces=ns)),
                    "activities": acts})


def _finish(sch):
    """Schedule-quality checks in the spirit of the GAO Schedule Assessment Guide / DCMA 14-point (a subset)."""
    acts = [a for a in sch["activities"] if not a["summary"]]
    ids = {a["id"] for a in acts}
    has_succ = set()
    for a in acts:
        for p in a["preds"]:
            has_succ.add(p)
    open_ends = [a["id"] for a in acts if not a["preds"] or a["id"] not in has_succ]
    neg = [a["id"] for a in acts if a["float_days"] is not None and a["float_days"] < 0]
    high = [a["id"] for a in acts if a["float_days"] is not None and a["float_days"] > 44 and not a["milestone"]]
    dd = sch.get("data_date")
    stale = [a["id"] for a in acts if dd and a["forecast"][1] and a["forecast"][1] < dd and not a["actual"][1]]
    n = max(1, len(acts))
    sch["checks"] = {
        "activities": len(acts), "milestones": sum(1 for a in acts if a["milestone"]),
        "critical": sum(1 for a in acts if a["critical"]),
        "missing_logic": {"count": len(open_ends), "pct": round(100.0 * len(open_ends) / n, 1), "ids": open_ends[:10],
                          "note": "start and finish activities are expected open ends"},
        "negative_float": {"count": len(neg), "ids": neg[:10]},
        "high_float_over_44d": {"count": len(high), "pct": round(100.0 * len(high) / n, 1)},
        "forecast_in_past_not_actualised": {"count": len(stale), "ids": stale[:10]},
        "unknown_preds": sum(1 for a in acts for p in a["preds"] if p not in ids),
    }
    return sch
