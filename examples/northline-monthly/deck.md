---
deck: Northline Rail Programme: October status report
context: Northline Rail Programme  |  Monthly status report  |  October 2026
tracker: Summary, Schedule, Risk, Delivery
sticker: Draft for discussion
source: schedule.xer (P6, data date 31 Oct 2026); risk-register.xlsx; raid.csv; benefits.csv; SteerCo transcript 28 Oct. Fictional example.
---

# Northline Rail Programme: October 2026 status report
layout: title

```json
{"subtitle": "Built from the project's own schedule, risk register, RAID log and benefits register", "client": "Northline Transport Authority", "date": "4 November 2026", "prepared_by": "Programme Management Office"}
```

# Handover has slipped three weeks since September, and two risks have escalated to red
layout: status-summary
section: Summary
data_from: research/emit/lookahead.json as lookahead
sowhat: Approving the £14m drawdown by 14 November protects the 15 May handover
footnote: RAG from forecast finish against plan: on plan green, up to 10 working days amber, more red.

```json
{"rows": [
  {"area": "Schedule", "icon": "calendar-clock", "rag": "R", "trend": "down", "text": "Handover forecast moved **21 days** since September, to **15 May 2027**. Main civils finished 30 Oct, six weeks late."},
  {"area": "Risk", "icon": "triangle-alert", "rag": "R", "trend": "down", "text": "R07 (signalling software) rose from 12 to 20 and R12 (Christmas possessions) from 9 to 16. R21 fell from 9 to 6."},
  {"area": "Benefits", "icon": "target", "rag": "A", "trend": "flat", "text": "No benefits are realised before handover; both remain on track to be measured from May 2027."}],
 "decisions": [
  {"what": "Approve the £14m contingency drawdown", "owner": "SRO", "due": "14 Nov"},
  {"what": "Sponsor sign-off for contingency below the 5% floor", "owner": "Sponsor", "due": "21 Nov"}]}
```

??? From the SteerCo transcript: contingency after the drawdown would be about 2% of remaining work (Ruth Dube); the sponsor paper is due Friday.

# Four milestones moved since September; handover now depends on the operator's test windows
layout: table
section: Summary
footnote: Compares the October schedule (data date 31 Oct) with the September snapshot (data date 30 Sep).

```json
{"exhibit": "Milestone movement since the September report",
 "columns": [{"name": "Milestone", "width": 0.38, "kind": "bold"}, {"name": "September forecast", "width": 0.16}, {"name": "October forecast", "width": 0.16},
             {"name": "Moved", "width": 0.12, "kind": "number"}],
 "rows": [["Main civils complete", "20 Oct 2026", "12 Nov 2026", "+23 days"],
          ["Signalling software drop 4 accepted", "1 Nov 2026", "8 Nov 2026", "+7 days"],
          ["Test windows confirmed by operator", "5 Nov 2026", "14 Nov 2026", "+9 days"],
          ["Handover to operator", "24 Apr 2027", "15 May 2027", "**+21 days**"]]}
```

# Systems integration and trial running now drive the handover date
layout: gantt
section: Schedule
data_from: research/emit/gantt.json
footnote: Planned dates are the P6 target dates. RAG from forecast finish against plan.

```json
{"takeaways_title": "What the schedule shows",
 "takeaways": ["Every workstream is forecast to finish after plan; the critical path runs through signalling and systems integration.",
               "Handover is forecast for **15 May 2027**, six weeks after the planned 3 April."],
 "panels": [{"title": "Schedule quality", "bullets": ["4 of 11 activities lack a predecessor or successor; fix before the next risk analysis", "No negative float"]}]}
```

# Two risks moved into the red zone this month, and neither has a funded mitigation
layout: risk-heatmap
section: Risk
data_from: research/emit/risk-heatmap.json
footnote: Text ratings in the register mapped to 1-5 (very low to very high). Arrows show movement since the September register.
```json
{}
```

# Open RAID items needing attention before the next report
layout: raid-log
section: Delivery
data_from: research/emit/raid-log.json
```json
{}
```

# Both benefits are measured from handover, so neither has started to be realised
layout: benefits-tracker
section: Delivery
data_from: research/emit/benefits.json
```json
{}
```
