"""Read meeting notes, transcripts and prior decks: .docx, .md/.txt, .vtt/.srt (Teams, Zoom, Otter, Granola,
Fireflies exports), .pptx. Standard library only.

Every reader returns {"source", "format", "text"} plus structure where the format has it:
  transcripts -> "turns": [{t, speaker, text}], "speakers"
  docx        -> "paragraphs": [{style, text}], "tables": [[[cell, ...], ...]]
  pptx        -> "slides": [{n, title, text, notes}]
and "candidates": lines that look like decisions, actions, risks, dates and numbers. Candidates are pointers for
the agent to read in context, not facts: confirm each with the user or the source before it reaches a slide.
"""
import os
import re
import xml.etree.ElementTree as ET
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
CAND = {
    "decisions": re.compile(r"\b(agreed|decided|decision|approved|sign(ed)? off|go ahead|we will go with|endorse[sd]?)\b", re.I),
    "actions": re.compile(r"\b(action|to do|will (send|share|confirm|draft|update|follow up|check|book|issue)|by (mon|tue|wed|thu|fri|next week|end of)|owner)\b", re.I),
    "risks": re.compile(r"\b(risk|concern|worried|slip(ped|page)?|delay(ed)?|overrun|blocker|issue|escalat\w+|at risk)\b", re.I),
    "numbers": re.compile(r"[£$€]\s?\d|\d+(\.\d+)?\s?(%|m\b|bn\b|k\b|weeks?|days?|months?)", re.I),
    "dates": re.compile(r"\b\d{1,2}(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\b|\b(q[1-4])\s?\d{2,4}\b|\b20\d\d-\d\d-\d\d\b", re.I),
}


def candidates(lines):
    out = {k: [] for k in CAND}
    for ln in lines:
        txt = ln if isinstance(ln, str) else "%s: %s" % (ln.get("speaker") or "?", ln["text"])
        for k, rx in CAND.items():
            if rx.search(txt) and len(out[k]) < 40:
                out[k].append(txt[:300])
    return out


def _decode(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", "ignore")


def read_transcript(path):
    text = _decode(path)
    turns = []
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n"))
    for b in blocks:
        lines = [l for l in b.strip().split("\n") if l.strip()]
        if not lines or lines[0].strip() in ("WEBVTT",) or lines[0].startswith("NOTE"):
            continue
        ts = None
        body = []
        for l in lines:
            m = re.match(r"^\s*(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{1,3}\s*-->", l)
            if m:
                ts = l.split("-->")[0].strip()
            elif re.match(r"^\d+$", l.strip()) and not body and ts is None:
                continue
            else:
                body.append(l.strip())
        if not body:
            continue
        txt = " ".join(body)
        speaker = None
        m = re.match(r"^<v(?:\.[^ >]*)?\s+([^>]+)>(.*?)(</v>)?$", txt)
        if m:
            speaker, txt = m.group(1).strip(), m.group(2)
        else:
            m = re.match(r"^([A-Z][\w.'\- ]{1,40}?):\s+(.*)$", txt)
            if m:
                speaker, txt = m.group(1).strip(), m.group(2)
        txt = re.sub(r"</?[^>]+>", "", txt).strip()
        if turns and turns[-1]["speaker"] == speaker and speaker:
            turns[-1]["text"] += " " + txt
        else:
            turns.append({"t": ts, "speaker": speaker, "text": txt})
    if not turns:  # plain "Name: text" transcript without cues
        for l in text.splitlines():
            m = re.match(r"^\s*\[?([\d:]+)?\]?\s*([A-Z][\w.'\- ]{1,40}?):\s+(.*)$", l)
            if m:
                turns.append({"t": m.group(1), "speaker": m.group(2).strip(), "text": m.group(3).strip()})
    speakers = sorted({t["speaker"] for t in turns if t["speaker"]})
    return {"source": os.path.basename(path), "format": "transcript", "speakers": speakers, "turns": turns,
            "text": "\n".join("%s: %s" % (t["speaker"] or "?", t["text"]) for t in turns), "candidates": candidates(turns)}


def read_docx(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    paras, tables, lines = [], [], []
    for el in body:
        if el.tag == W + "p":
            st = el.find("%spPr/%spStyle" % (W, W))
            style = st.get(W + "val") if st is not None else ""
            t = "".join(x.text or "" for x in el.iter(W + "t")).strip()
            if t:
                paras.append({"style": style, "text": t})
                lines.append(("#" * int(style[-1]) + " " if re.match(r"Heading[1-6]$", style) else "") + t)
        elif el.tag == W + "tbl":
            rows = []
            for tr in el.iter(W + "tr"):
                rows.append([" ".join(x.text or "" for x in tc.iter(W + "t")).strip() for tc in tr.iter(W + "tc")])
            tables.append(rows)
            lines += [" | ".join(r_) for r_ in rows]
    return {"source": os.path.basename(path), "format": "docx", "paragraphs": paras, "tables": tables,
            "text": "\n".join(lines), "candidates": candidates(lines)}


def read_plain(path):
    text = _decode(path)
    lines = [l for l in text.splitlines() if l.strip()]
    return {"source": os.path.basename(path), "format": "text", "text": text, "candidates": candidates(lines)}


def read_pptx(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    nums = sorted(int(m.group(1)) for n in names for m in [re.match(r"ppt/slides/slide(\d+)\.xml$", n)] if m)
    order = []
    try:
        pres = ET.fromstring(z.read("ppt/presentation.xml"))
        rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
        R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
        for s in pres.iter(P + "sldId"):
            m = re.search(r"slide(\d+)\.xml", rmap.get(s.get(R + "id"), ""))
            if m:
                order.append(int(m.group(1)))
    except Exception:
        order = nums
    slides, lines = [], []
    for k, n in enumerate(order or nums, 1):
        root = ET.fromstring(z.read("ppt/slides/slide%d.xml" % n))
        title, texts = "", []
        for sp in root.iter("{http://schemas.openxmlformats.org/presentationml/2006/main}sp"):
            ph = sp.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}ph")
            paras = ["".join(t.text or "" for t in p.iter(A + "t")) for p in sp.iter(A + "p")]
            txt = "\n".join(p for p in paras if p.strip())
            if ph is not None and ph.get("type") in ("title", "ctrTitle") and not title:
                title = txt.replace("\n", " ")
            elif txt:
                texts.append(txt)
        for gf in root.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}tbl"):
            for tr in gf.iter(A + "tr"):
                texts.append(" | ".join("".join(t.text or "" for t in tc.iter(A + "t")) for tc in tr.iter(A + "tc")))
        notes = ""
        nrel = "ppt/slides/_rels/slide%d.xml.rels" % n
        if nrel in names:
            for r_ in ET.fromstring(z.read(nrel)):
                if r_.get("Type", "").endswith("/notesSlide"):
                    np_ = "ppt/" + r_.get("Target").replace("../", "")
                    if np_ in names:
                        nr = ET.fromstring(z.read(np_))
                        notes = "\n".join("".join(t.text or "" for t in p.iter(A + "t")) for p in nr.iter(A + "p")).strip()
        slides.append({"n": k, "title": title, "text": "\n".join(texts), "notes": notes})
        lines += [title] + texts
    return {"source": os.path.basename(path), "format": "pptx", "slides": slides,
            "text": "\n\n".join("## %d. %s\n%s" % (s["n"], s["title"], s["text"]) for s in slides),
            "candidates": candidates([l for l in lines if l])}
