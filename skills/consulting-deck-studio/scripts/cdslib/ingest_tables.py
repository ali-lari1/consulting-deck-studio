"""Read registers and trackers from .xlsx / .csv: risk registers, RAID logs, benefits, milestones, cost reports.

read_table(path) -> {"source", "sheets": [{"name", "kind", "columns": {field: header}, "rows": [ {field: value} ],
                                           "unmapped": [headers]}]}
Header names are matched against synonym lists (case and punctuation insensitive). The sheet kind is guessed from
which fields are present: risk | raid | benefits | milestones | cost | table. Text ratings (Very high .. Very low,
percentages) become 1-5 scores. Standard library only; .xls (old binary) must be re-saved as .xlsx.
"""
import csv
import datetime
import os
import re
import xml.etree.ElementTree as ET
import zipfile

SYN = {
    "id": ["id", "ref", "reference", "risk id", "risk ref", "risk no", "no", "number", "raid id", "item id"],
    "type": ["type", "raid type", "category type", "item type"],
    "title": ["title", "risk", "risk title", "description", "risk description", "event", "item", "issue", "name",
              "benefit", "milestone", "activity", "summary"],
    "cause": ["cause"], "effect": ["effect", "consequence description"],
    "owner": ["owner", "risk owner", "action owner", "responsible", "lead"],
    "l": ["likelihood", "probability", "prob", "l", "p", "current likelihood", "residual likelihood"],
    "i": ["impact", "consequence", "severity", "i", "c", "current impact", "residual impact"],
    "score": ["score", "rating", "risk score", "risk rating", "pxi", "lxi", "current score", "residual score"],
    "prev_l": ["previous likelihood", "last likelihood", "prior likelihood"],
    "prev_i": ["previous impact", "last impact", "prior impact"],
    "prev_score": ["previous score", "prev score", "last score", "prior score", "last period score"],
    "mitigation": ["mitigation", "response", "actions", "treatment", "mitigating actions", "next action", "status and next action"],
    "status": ["status", "rag", "rag status", "state"],
    "trend": ["trend", "direction", "movement"],
    "due": ["due", "due date", "target date", "date due", "deadline"],
    "cost_impact": ["cost impact", "cost exposure", "financial impact", "exposure", "p50 cost", "expected value"],
    "baseline": ["baseline", "baseline value", "baseline date", "planned", "plan", "original"],
    "target": ["target", "target value"],
    "actual": ["actual", "actual value", "actual to date", "achieved", "actuals"],
    "forecast": ["forecast", "forecast date", "current forecast", "latest forecast", "eac", "estimate at completion", "outturn"],
    "budget": ["budget", "approved budget", "bac", "budget at completion", "current budget"],
    "unit": ["unit", "units", "measure"],
    "workstream": ["workstream", "work stream", "project", "programme", "package", "wbs", "area"],
}
NORM = {re.sub(r"[^a-z0-9]+", " ", s).strip(): k for k, lst in SYN.items() for s in lst}
WORDS = {"very high": 5, "almost certain": 5, "extreme": 5, "critical": 5, "severe": 5, "high": 4, "likely": 4, "major": 4,
         "medium": 3, "moderate": 3, "possible": 3, "low": 2, "unlikely": 2, "minor": 2, "very low": 1, "rare": 1,
         "negligible": 1, "insignificant": 1}
RAGW = {"red": "R", "r": "R", "amber": "A", "a": "A", "yellow": "A", "green": "G", "g": "G", "complete": "G", "closed": "G"}


def _norm(h):
    return re.sub(r"[^a-z0-9]+", " ", str(h).lower()).strip()


def score_1_5(v):
    if v in (None, ""):
        return None
    s = str(v).strip().lower()
    if s in WORDS:
        return WORDS[s]
    m = re.match(r"^(\d+(?:\.\d+)?)\s*%$", s)
    if m:
        p = float(m.group(1))
        return 1 if p < 10 else 2 if p < 30 else 3 if p < 50 else 4 if p < 70 else 5
    try:
        f = float(s)
        if 0 < f < 1:
            return score_1_5("%s%%" % (f * 100))
        return max(1, min(5, int(round(f))))
    except ValueError:
        return None


def excel_date(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return v
    if 20000 < f < 80000:
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(f))).isoformat()
    return v


def _xlsx(path):
    z = zipfile.ZipFile(path)
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    out = []
    for sh in wb.findall("m:sheets/m:sheet", ns):
        if sh.get("state") == "hidden":
            continue
        target = rels[sh.get("{%s}id" % ns["r"])].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(z.read(target))
        rows = []
        for row in root.iter("{%s}row" % ns["m"]):
            vals = {}
            for c in row.findall("m:c", ns):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                t = c.get("t")
                v = c.find("m:v", ns)
                if t == "s" and v is not None:
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % ns["m"]))
                elif t == "b" and v is not None:
                    val = v.text == "1"
                else:
                    val = v.text if v is not None else ""
                    if val and re.match(r"^-?\d+(\.\d+)?(E-?\d+)?$", str(val)):
                        f = float(val)
                        val = int(f) if f.is_integer() else f
                vals[col - 1] = val
            if vals:
                rows.append([vals.get(k, "") for k in range(max(vals) + 1)])
        out.append((sh.get("name"), rows))
    return out


def _csv(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|") if text.strip() else csv.excel
    return [(os.path.splitext(os.path.basename(path))[0], [r for r in csv.reader(text.splitlines(), dialect)])]


def _header_row(rows):
    """First row (of the first 15) with the most recognised headers."""
    best, bi = -1, 0
    for i, row in enumerate(rows[:15]):
        n = sum(1 for h in row if _norm(h) in NORM)
        if n > best:
            best, bi = n, i
    return bi


def _kind(fields):
    f = set(fields)
    if "type" in f and "title" in f:
        return "raid"
    if ("l" in f and "i" in f) or "score" in f:
        return "risk"
    if {"baseline", "target", "actual"} <= f:
        return "benefits"
    if "budget" in f and ("forecast" in f or "actual" in f):
        return "cost"
    if "baseline" in f and "forecast" in f:
        return "milestones"
    return "table"


def read_table(path):
    sheets = _xlsx(path) if path.lower().endswith((".xlsx", ".xlsm")) else _csv(path)
    out = {"source": os.path.basename(path), "sheets": []}
    for name, rows in sheets:
        rows = [r for r in rows if any(str(c).strip() for c in r)]
        if len(rows) < 2:
            continue
        hi = _header_row(rows)
        headers = [str(h).strip() for h in rows[hi]]
        cols, unmapped = {}, []
        for k, h in enumerate(headers):
            f = NORM.get(_norm(h))
            if f and f not in cols:
                cols[f] = k
            elif h:
                unmapped.append(h)
        recs = []
        for r in rows[hi + 1:]:
            rec = {f: (r[k] if k < len(r) else "") for f, k in cols.items()}
            for k, h in enumerate(headers):
                if h in unmapped and k < len(r) and r[k] not in ("", None):
                    rec.setdefault("extra", {})[h] = r[k]
            for f in ("due", "baseline", "forecast", "target", "actual"):
                if f in rec and any(w in _norm(headers[cols[f]]) for w in ("date", "due", "deadline")):
                    rec[f] = excel_date(rec[f])
            if "due" in rec:
                rec["due"] = excel_date(rec["due"])
            if not any(str(v).strip() for k_, v in rec.items() if k_ != "extra"):
                continue
            recs.append(rec)
        kind = _kind(cols)
        if kind == "risk":
            for rec in recs:
                for f in ("l", "i", "prev_l", "prev_i"):
                    if f in rec:
                        rec[f] = score_1_5(rec[f])
                if rec.get("l") and rec.get("i"):
                    rec["score"] = rec["l"] * rec["i"]
        for rec in recs:
            if "status" in rec and str(rec["status"]).strip().lower() in RAGW:
                rec["rag"] = RAGW[str(rec["status"]).strip().lower()]
        out["sheets"].append({"name": name, "kind": kind, "columns": {f: headers[k] for f, k in cols.items()},
                              "rows": recs, "unmapped": unmapped})
    return out
