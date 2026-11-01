#!/usr/bin/env python3
"""Generate fictional Northline project inputs for two periods (tests/fixtures/northline/2026-09 and 2026-10):
schedule.xer (P6), risk-register.xlsx, raid.csv, benefits.csv, steerco.vtt, notes.docx, plus a small MS Project XML.
"""
import os
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "fixtures", "northline")

WBS = [("10", "Main civils"), ("20", "Track and OHLE"), ("30", "Signalling"), ("40", "Systems integration"),
       ("50", "Stations"), ("60", "Trial running and handover")]
# code, name, wbs, type, target start, target end, forecast start, forecast end (Oct period), float hrs, driving, act start, act end, preds
ACTS_OCT = [
    ("C100", "Utilities diversion Kings Cross", "10", "TT_Task", "2026-08-03", "2026-09-18", "2026-08-03", "2026-10-30", 0, "N", "2026-08-03", "2026-10-30", []),
    ("C200", "Main civils complete", "10", "TT_FinMile", "", "2026-10-31", "", "2026-11-12", 0, "N", "", "", ["C100"]),
    ("T100", "Track installation", "20", "TT_Task", "2026-10-15", "2026-12-18", "2026-10-18", "2027-01-07", 80, "N", "2026-10-18", "", ["C200"]),
    ("S100", "Signalling install", "30", "TT_Task", "2026-11-06", "2027-01-18", "2026-11-15", "2027-02-06", 0, "Y", "", "", ["C200"]),
    ("S200", "Signalling software drop 4 accepted", "30", "TT_FinMile", "", "2026-10-30", "", "2026-11-08", 0, "Y", "", "", ["S100"]),
    ("I100", "Systems integration testing", "40", "TT_Task", "2027-01-01", "2027-03-18", "2027-01-12", "2027-04-15", 0, "Y", "", "", ["S100", "S200"]),
    ("I200", "Test windows confirmed by operator", "40", "TT_FinMile", "", "2026-11-01", "", "2026-11-14", 0, "Y", "", "", []),
    ("F100", "Station fit-out", "50", "TT_Task", "2026-12-01", "2027-03-01", "2026-12-06", "2027-03-12", 200, "N", "", "", ["C200"]),
    ("F200", "Station 3 fit-out complete", "50", "TT_FinMile", "", "2026-12-12", "", "2026-12-19", 120, "N", "", "", ["F100"]),
    ("H100", "Trial running", "60", "TT_Task", "2027-02-18", "2027-03-18", "2027-04-15", "2027-05-14", 0, "Y", "", "", ["I100"]),
    ("H200", "Handover to operator", "60", "TT_FinMile", "", "2027-04-03", "", "2027-05-15", 0, "Y", "", "", ["H100", "F100", "T100"]),
]
SEPT_SHIFT = {"C100": "2026-10-09", "C200": "2026-10-20", "S200": "2026-11-01", "I200": "2026-11-05", "H200": "2027-04-24",
              "H100": "2027-04-20", "I100": "2027-04-01"}
RISKS_OCT = [("R07", "Signalling software maturity: supplier missed drops 3 and 4", "S. Novak", "Very high", "High", "12",
              "Recovery plan due 8 Nov; independent code review proposed (unfunded)", "Open"),
             ("R12", "Christmas possessions: 3 of 5 weekends unconfirmed", "Interface lead", "High", "High", "9",
              "Escalated to Network Rail route director; decision 21 Nov", "Open"),
             ("R03", "Utilities diversion claims from main contractor", "R. Dube", "Medium", "Very high", "15",
              "£6-9m exposure; valuation agreed, settlement talks under way", "Open"),
             ("R18", "Driver training capacity for trial running", "K. Ahmed", "Low", "Medium", "6",
              "Second simulator booked from January", "Open"),
             ("R21", "Late design changes at Station 3", "A. Silva", "Medium", "Low", "9", "Design freeze agreed 15 Oct", "Open"),
             ("R02", "Ground contamination at depot", "J. Patel", "Low", "Low", "4", "Survey clear", "Closed")]
RISKS_SEPT = [("R07", "Signalling software maturity: supplier missed drop 3", "S. Novak", "Medium", "High", "", "Supplier recovery plan", "Open"),
              ("R12", "Christmas possessions: 3 of 5 weekends unconfirmed", "Interface lead", "Medium", "Medium", "", "Raised with Network Rail", "Open"),
              ("R03", "Utilities diversion claims from main contractor", "R. Dube", "Medium", "Very high", "", "Valuation in progress", "Open"),
              ("R18", "Driver training capacity for trial running", "K. Ahmed", "Low", "Medium", "", "Options review", "Open"),
              ("R21", "Late design changes at Station 3", "A. Silva", "Medium", "Medium", "", "Change board set up", "Open"),
              ("R02", "Ground contamination at depot", "J. Patel", "Low", "Low", "", "Survey due", "Open")]


def xer(path, acts, data_date):
    L = ["ERMHDR\t21.12\t%s\tProject\tadmin\t\tdbxDatabaseNoName\tProject Management\tGBP" % data_date,
         "%T\tPROJECT", "%F\tproj_id\tproj_short_name\tlast_recalc_date", "%R\t1\tNORTHLINE\t" + data_date + " 08:00",
         "%T\tCALENDAR", "%F\tclndr_id\tclndr_name\tday_hr_cnt", "%R\t1\tStandard 5-day\t8",
         "%T\tPROJWBS", "%F\twbs_id\tproj_id\tparent_wbs_id\twbs_name\tproj_node_flag", "%R\t0\t1\t\tNorthline\tY"]
    L += ["%%R\t%s\t1\t0\t%s\tN" % (w, n) for w, n in WBS]
    L += ["%T\tTASK", "%F\ttask_id\tproj_id\twbs_id\tclndr_id\ttask_code\ttask_name\ttask_type\tstatus_code\ttarget_start_date\t"
          "target_end_date\tearly_start_date\tearly_end_date\tact_start_date\tact_end_date\ttotal_float_hr_cnt\tdriving_path_flag\tphys_complete_pct"]
    for k, a in enumerate(acts, 1):
        code, name, w, typ, ts, te, fs, fe, tf, drv, as_, ae, _ = a
        st = "TK_Complete" if ae else "TK_Active" if as_ else "TK_NotStart"
        L.append("%%R\t%d\t1\t%s\t1\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            k, w, code, name, typ, st, ts and ts + " 08:00", te + " 17:00", fs and fs + " 08:00", fe + " 17:00",
            as_ and as_ + " 08:00", ae and ae + " 17:00", tf, drv, 100 if ae else 40 if as_ else 0))
    ids = {a[0]: k for k, a in enumerate(acts, 1)}
    L += ["%T\tTASKPRED", "%F\ttask_pred_id\ttask_id\tpred_task_id\tpred_type"]
    n = 1
    for a in acts:
        for p in a[12]:
            L.append("%%R\t%d\t%d\t%d\tPR_FS" % (n, ids[a[0]], ids[p]))
            n += 1
    L.append("%E")
    open(path, "w", encoding="cp1252").write("\r\n".join(L))


def xlsx(path, rows, sheet="Risk register"):
    def cell(r, c, v):
        ref = "%s%d" % (chr(65 + c), r)
        if isinstance(v, (int, float)):
            return '<c r="%s"><v>%s</v></c>' % (ref, v)
        v = str(v).replace("&", "&amp;").replace("<", "&lt;")
        return '<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (ref, v)
    data = "".join('<row r="%d">%s</row>' % (i + 1, "".join(cell(i + 1, j, v) for j, v in enumerate(row))) for i, row in enumerate(rows))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="%s" sheetId="1" r:id="rId1"/></sheets></workbook>' % sheet)
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", '<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                   '<sheetData>%s</sheetData></worksheet>' % data)


def docx(path, paras):
    body = "".join('<w:p>%s<w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (
        '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % st if st else "", t.replace("&", "&amp;")) for st, t in paras)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/document.xml", '<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                   '<w:body>%s</w:body></w:document>' % body)


def main():
    for period, dd in (("2026-09", "2026-09-30"), ("2026-10", "2026-10-31")):
        d = os.path.join(OUT, period)
        os.makedirs(d, exist_ok=True)
        acts = ACTS_OCT
        if period == "2026-09":
            acts = []
            for a in ACTS_OCT:
                a = list(a)
                if a[0] in SEPT_SHIFT:
                    a[7] = SEPT_SHIFT[a[0]]
                if a[0] == "C100":
                    a[11] = ""
                acts.append(tuple(a))
        xer(os.path.join(d, "schedule.xer"), acts, dd)
        risks = RISKS_OCT if period == "2026-10" else RISKS_SEPT
        hdr = ["Risk ID", "Risk description", "Risk owner", "Likelihood", "Impact", "Prev score", "Mitigating actions", "Status"]
        xlsx(os.path.join(d, "risk-register.xlsx"), [["Northline risk register", "", "", "", "", "", "", ""], hdr] + [list(r) for r in risks])
    d = os.path.join(OUT, "2026-10")
    open(os.path.join(d, "raid.csv"), "w", encoding="utf-8").write(
        "Type,Ref,Description,Owner,Due date,RAG,Next action\n"
        "Risk,R07,Signalling software maturity,S. Novak,2026-11-08,Red,Recovery plan due\n"
        "Issue,I04,Test windows not confirmed by operator,L. Chen,2026-11-14,Red,SteerCo decision\n"
        "Assumption,A02,Possessions available at Easter 2027,Interface lead,2027-01-31,Amber,Confirm with Network Rail\n"
        "Dependency,D01,Operator driver training complete,K. Ahmed,2027-03-31,Green,On plan\n")
    open(os.path.join(d, "benefits.csv"), "w", encoding="utf-8").write(
        "Benefit,Owner,Unit,Baseline,Target,Actual,RAG,Due\n"
        "Journey time saving (minutes),Sponsor,min,0,6,0,Amber,May 27\n"
        "Peak capacity (trains per hour),Operator,tph,12,18,12,Amber,May 27\n")
    open(os.path.join(d, "steerco.vtt"), "w", encoding="utf-8").write(
        "WEBVTT\n\n00:00:05.000 --> 00:00:14.000\n<v Priya Shah>Let's start with schedule. Handover is now forecast for 15 May, six weeks later than the re-baseline.</v>\n\n"
        "00:00:15.000 --> 00:00:29.000\n<v Liang Chen>The operator still hasn't confirmed the test windows. If we don't have them by 14 November we lose another month.</v>\n\n"
        "00:00:30.000 --> 00:00:41.000\n<v Priya Shah>So the decision we need is the £14m drawdown. Can finance confirm contingency after that?</v>\n\n"
        "00:00:42.000 --> 00:00:55.000\n<v Ruth Dube>After the drawdown contingency would be about 2% of remaining work, below the 5% floor. That needs sponsor sign off.</v>\n\n"
        "00:00:56.000 --> 00:01:06.000\n<v Priya Shah>Agreed. Action: Ruth will draft the sponsor paper by Friday. Liang to chase the operator.</v>\n")
    docx(os.path.join(d, "pmo-notes.docx"), [("Heading1", "PMO notes, October 2026"), ("", "Signalling supplier missed software drop 4; recovery plan due 8 Nov."),
                                            ("", "Risk R12 escalated to the route director."), ("Heading2", "Actions"),
                                            ("", "PMO to re-run schedule risk analysis by 28 Nov.")])
    open(os.path.join(OUT, "small-msp.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?><Project xmlns="http://schemas.microsoft.com/project"><Name>Depot upgrade</Name>'
        '<StatusDate>2026-10-31T17:00:00</StatusDate><Tasks>'
        '<Task><UID>0</UID><ID>0</ID><Name>Depot upgrade</Name><OutlineLevel>0</OutlineLevel><Summary>1</Summary></Task>'
        '<Task><UID>1</UID><ID>1</ID><Name>Design</Name><OutlineLevel>1</OutlineLevel><Summary>1</Summary><Start>2026-06-01T08:00:00</Start><Finish>2026-09-30T17:00:00</Finish></Task>'
        '<Task><UID>2</UID><ID>2</ID><Name>Detailed design</Name><OutlineLevel>2</OutlineLevel><Summary>0</Summary><Start>2026-06-01T08:00:00</Start><Finish>2026-09-30T17:00:00</Finish>'
        '<ActualStart>2026-06-01T08:00:00</ActualStart><ActualFinish>2026-09-30T17:00:00</ActualFinish><PercentComplete>100</PercentComplete><TotalSlack>0</TotalSlack><Critical>1</Critical>'
        '<Baseline><Number>0</Number><Start>2026-06-01T08:00:00</Start><Finish>2026-08-31T17:00:00</Finish></Baseline></Task>'
        '<Task><UID>3</UID><ID>3</ID><Name>Build</Name><OutlineLevel>1</OutlineLevel><Summary>1</Summary><Start>2026-10-01T08:00:00</Start><Finish>2027-02-26T17:00:00</Finish></Task>'
        '<Task><UID>4</UID><ID>4</ID><Name>Construction</Name><OutlineLevel>2</OutlineLevel><Summary>0</Summary><Start>2026-10-01T08:00:00</Start><Finish>2027-02-26T17:00:00</Finish>'
        '<PercentComplete>15</PercentComplete><TotalSlack>0</TotalSlack><Critical>1</Critical><PredecessorLink><PredecessorUID>2</PredecessorUID></PredecessorLink>'
        '<Baseline><Number>0</Number><Start>2026-09-01T08:00:00</Start><Finish>2027-01-29T17:00:00</Finish></Baseline></Task>'
        '<Task><UID>5</UID><ID>5</ID><Name>Depot handover</Name><OutlineLevel>2</OutlineLevel><Summary>0</Summary><Milestone>1</Milestone><Start>2027-02-26T17:00:00</Start><Finish>2027-02-26T17:00:00</Finish>'
        '<TotalSlack>0</TotalSlack><Critical>1</Critical><PredecessorLink><PredecessorUID>4</PredecessorUID></PredecessorLink>'
        '<Baseline><Number>0</Number><Start>2027-01-29T17:00:00</Start><Finish>2027-01-29T17:00:00</Finish></Baseline></Task>'
        '</Tasks></Project>')
    print("wrote fixtures under", OUT)


if __name__ == "__main__":
    main()
