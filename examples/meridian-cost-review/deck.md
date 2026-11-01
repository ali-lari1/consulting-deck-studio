---
deck: Meridian Health: cost review and capital programme
context: Meridian Health Group  |  Board strategy session  |  November 2026
tracker: Diagnostic, Options, Plan, Capital
sticker: Draft for discussion
source: Meridian finance and activity data FY2025/26; PMO analysis. Fictional example.
---

# Meridian Health: closing the £38m gap and delivering the new surgical wing
layout: title

```json
{"subtitle": "Diagnostic findings, savings plan and capital programme status", "client": "Meridian Health Group Board",
 "date": "18 November 2026", "prepared_by": "Transformation Office"}
```

# Four numbers explain most of the deficit
layout: key-numbers
section: Diagnostic

```json
{"numbers": [
  {"value": "£38m", "label": "Recurrent deficit, FY2025/26", "note": "Up from £21m two years ago", "rag": "R"},
  {"value": "£812", "label": "Cost per bed day", "note": "6% above plan; peer median is **£744**", "rag": "R"},
  {"value": "£31m", "label": "Agency staff spend", "note": "38% above plan, concentrated in three wards", "rag": "R"},
  {"value": "71%", "label": "Elective activity vs 2019", "note": "Lost income of about **£14m** a year", "rag": "A"}]}
```

??? The rest of the deck explains each number and what we propose.

# The gap can be closed through income, pay and non-pay; pay offers the largest single lever
layout: issue-tree
section: Diagnostic
footnote: Dot shows our assessment of each hypothesis after the diagnostic: green supported, amber partly, red not supported.

```json
{"root": {"text": "How can Meridian close a £38m recurrent deficit within two years?", "children": [
  {"text": "Grow income", "children": [
    {"text": "Recover elective activity to 90% of 2019", "rag": "G"},
    {"text": "Improve clinical coding and tariff capture", "rag": "A"}]},
  {"text": "Reduce pay cost", "highlight": true, "children": [
    {"text": "Cut agency spend by converting to bank and substantive staff", "rag": "G", "highlight": true},
    {"text": "Reduce overtime through e-rostering", "rag": "G"}]},
  {"text": "Reduce non-pay cost", "children": [
    {"text": "Consolidate procurement across the three hospitals", "rag": "A"},
    {"text": "Release two leased buildings", "rag": "R"}]}]},
 "legend": [["dot", "G", "Supported"], ["dot", "A", "Partly supported"], ["dot", "R", "Not supported"]]}
```

# Cost per bed day is £812, and agency staff explain most of the overspend
layout: driver-tree
section: Diagnostic
footnote: Change is against the FY2025/26 plan.

```json
{"root": {"label": "Cost per bed day", "value": "£812", "delta": "+6%", "children": [
  {"label": "Pay", "value": "£520", "delta": "+9%", "delta_bad": true, "children": [
    {"label": "Agency", "value": "£96", "delta": "+38%", "delta_bad": true, "highlight": true},
    {"label": "Overtime", "value": "£41", "delta": "+12%", "delta_bad": true},
    {"label": "Substantive", "value": "£383", "delta": "+2%", "delta_bad": true}]},
  {"label": "Non-pay", "value": "£292", "delta": "+1%", "delta_bad": true, "children": [
    {"label": "Drugs", "value": "£118", "delta": "+3%", "delta_bad": true},
    {"label": "Clinical supplies", "value": "£97", "delta": "-1%"},
    {"label": "Facilities", "value": "£77", "delta": "0%"}]}]},
 "takeaways_title": "What the tree shows",
 "takeaways": ["Agency staff add **£96** per bed day, 38% more than planned.", "Non-pay is broadly on plan; the problem is pay."]}
```

# Meridian's cost per weighted activity unit is the third highest of 12 peers
layout: benchmark
section: Diagnostic
footnote: Peers are acute trusts of similar size and case mix; FY2025/26 published accounts.

```json
{"exhibit": "Cost per weighted activity unit (WAU)", "unit": "£, FY2025/26", "prefix": "£", "better": "low",
 "items": [{"label": "Peer A", "value": 3410}, {"label": "Peer B", "value": 3480}, {"label": "Peer C", "value": 3520},
           {"label": "Peer D", "value": 3590}, {"label": "Peer E", "value": 3620}, {"label": "Peer F", "value": 3655},
           {"label": "Peer G", "value": 3700}, {"label": "Peer H", "value": 3745}, {"label": "Peer I", "value": 3790},
           {"label": "Meridian", "value": 3880, "highlight": true}, {"label": "Peer J", "value": 3925}, {"label": "Peer K", "value": 4010}],
 "takeaways_title": "Implication",
 "takeaways": ["Reaching the peer median would save about **£9m** a year at current activity."]}
```

# Non-pay spend is concentrated: three suppliers hold over half of clinical supplies
layout: marimekko
section: Diagnostic

```json
{"exhibit": "Non-pay spend by category and supplier concentration", "unit": "Column width = annual spend; height = share of category spend",
 "columns": [{"label": "Drugs", "width_value": 62, "width_label": "£62m", "segments": [{"label": "Top 3 suppliers", "value": 41}, {"label": "Next 10", "value": 15}, {"label": "Long tail", "value": 6}]},
             {"label": "Clinical supplies", "width_value": 51, "width_label": "£51m", "segments": [{"label": "Top 3 suppliers", "value": 27}, {"label": "Next 10", "value": 14}, {"label": "Long tail", "value": 10}]},
             {"label": "Facilities", "width_value": 40, "width_label": "£40m", "segments": [{"label": "Top 3 suppliers", "value": 12}, {"label": "Next 10", "value": 13}, {"label": "Long tail", "value": 15}]},
             {"label": "IT", "width_value": 18, "width_label": "£18m", "segments": [{"label": "Top 3 suppliers", "value": 11}, {"label": "Next 10", "value": 5}, {"label": "Long tail", "value": 2}]}],
 "highlight": "Long tail",
 "takeaways_title": "Where to act",
 "takeaways": ["Facilities has the longest tail: 38% of spend sits with small suppliers.", "Consolidating it is the quickest non-pay saving."]}
```

# Staff and managers describe the same three problems
layout: quotes
section: Diagnostic
footnote: From 34 interviews in September and October 2026. Fictional quotes for this example.

```json
{"quotes": [
  {"theme": "Rostering", "text": "We fill gaps with agency because the roster is finished four days before the shift, not six weeks.", "who": "Ward manager, surgery"},
  {"theme": "Rostering", "text": "Overtime is approved by whoever is on shift. Nobody sees the total until month end.", "who": "Finance business partner"},
  {"theme": "Theatres", "text": "We lose a theatre list most weeks because the patient wasn't pre-assessed.", "who": "Consultant anaesthetist"},
  {"theme": "Procurement", "text": "Each hospital buys its own gloves. We have eleven contracts for the same product.", "who": "Procurement lead"}]}
```

# Five changes to the operating model address the root causes
layout: before-after
section: Options

```json
{"before_title": "Today", "after_title": "From April 2027",
 "rows": [
  {"dimension": "Rostering", "before": "Paper rosters, finalised four days ahead", "after": "E-rostering, published **six weeks** ahead"},
  {"dimension": "Temporary staff", "before": "Agency booked by wards directly", "after": "Central bank office; agency only with director sign-off"},
  {"dimension": "Theatres", "before": "Lists planned a week ahead; 14% cancelled on the day", "after": "Pre-assessment two weeks ahead; target **5%** cancellations"},
  {"dimension": "Procurement", "before": "Three hospitals, 11 glove contracts", "after": "One group category team; one contract per product"},
  {"dimension": "Performance", "before": "Monthly finance pack, five weeks after month end", "after": "Weekly ward dashboard on pay and activity"}]}
```

# We will deliver the programme in four stages, piloting on three wards before scaling
layout: process-flow
section: Plan

```json
{"steps": [
  {"title": "Diagnose", "bullets": ["Baseline cost per bed day by ward", "Agree savings targets with each division"], "owner": "Finance", "duration": "Done"},
  {"title": "Design", "bullets": ["E-rostering rules and bank office", "Procurement category plans"], "owner": "Transformation Office", "duration": "8 weeks"},
  {"title": "Pilot", "bullets": ["Three highest-agency wards", "Weekly tracking against the baseline", ["Go or no-go at week 12", 2]], "owner": "Divisional directors", "duration": "12 weeks"},
  {"title": "Scale", "bullets": ["Roll out to all 42 wards", "Hand over to business as usual"], "owner": "COO", "duration": "9 months"}],
 "active": "Design"}
```

# The savings plan reaches £38m by March 2029, with workforce changes delivering first
layout: roadmap
section: Plan
footnote: Indices are quarters from Q1 2027; savings are full-year recurrent.

```json
{"periods": ["Q1 27", "Q2 27", "Q3 27", "Q4 27", "Q1 28", "Q2 28", "Q3 28", "Q4 28"],
 "phases": [{"name": "Wave 1: quick wins (£14m)", "start": 0, "end": 3}, {"name": "Wave 2: structural (£24m)", "start": 3, "end": 8}],
 "lanes": [
  {"name": "Workforce", "items": [{"label": "E-rostering pilot", "start": 0, "end": 1.5, "rag": "G"}, {"label": "Bank office live", "start": 1, "end": 3}, {"label": "Agency cap", "type": "milestone", "at": 3}]},
  {"name": "Theatres", "items": [{"label": "Pre-assessment redesign", "start": 0.5, "end": 3, "rag": "A"}, {"label": "Extra weekend lists", "start": 3, "end": 6}]},
  {"name": "Procurement", "items": [{"label": "Category plans", "start": 0, "end": 2}, {"label": "Contract consolidation", "start": 2, "end": 7, "rag": "A"}]},
  {"name": "Estates", "items": [{"label": "Lease exit, Building C", "start": 4, "end": 7, "rag": "R"}, {"label": "Lease break", "type": "milestone", "at": 7, "rag": "R"}]}],
 "today": 0.2}
```

# Key milestones for the next eighteen months
layout: timeline
section: Plan

```json
{"start": "2026-11-01", "end": "2028-04-30",
 "events": [
  {"date": "2026-11-18", "label": "Board approves plan", "done": true},
  {"date": "2027-01-11", "label": "E-rostering pilot starts", "detail": "Three wards"},
  {"date": "2027-04-01", "label": "Bank office live"},
  {"date": "2027-06-30", "label": "Pilot go or no-go"},
  {"date": "2027-10-01", "label": "Agency cap in force"},
  {"date": "2028-01-15", "label": "Procurement contracts consolidated"},
  {"date": "2028-03-31", "label": "£14m recurrent saving", "detail": "End of wave 1 tracking"}]}
```

# The Transformation Committee owns delivery; one SRO is accountable to the Board
layout: org-chart
section: Plan

```json
{"nodes": [
  {"id": "board", "title": "Group Board"},
  {"id": "tc", "title": "Transformation Committee", "name": "Chair: Chief Executive", "parent": "board", "note": "Monthly"},
  {"id": "sro", "title": "Senior Responsible Owner", "name": "Chief Operating Officer", "parent": "tc"},
  {"id": "pmo", "title": "Transformation Office", "name": "Programme director + 6", "parent": "sro", "highlight": true},
  {"id": "w1", "title": "Workforce", "name": "Director of Nursing", "parent": "pmo"},
  {"id": "w2", "title": "Theatres", "name": "Surgical Director", "parent": "pmo"},
  {"id": "w3", "title": "Procurement", "name": "Head of Procurement", "parent": "pmo"},
  {"id": "w4", "title": "Estates", "name": "Director of Estates", "parent": "pmo"}]}
```

# Every savings decision has one accountable owner
layout: raci
section: Plan

```json
{"roles": ["Board", "SRO", "Transformation Office", "Workstream lead", "Finance"],
 "activities": [
  {"name": "Approve savings targets", "cells": ["A", "R", "C", "C", "C"]},
  {"name": "Design workstream changes", "cells": ["I", "A", "C", "R", "C"]},
  {"name": "Track savings weekly", "cells": ["I", "I", "R", "C", "A"]},
  {"name": "Go or no-go after pilot", "cells": ["I", "A", "R", "C", "C"]},
  {"name": "Report to Board", "cells": ["I", "A", "R", "I", "C"]}]}
```

# Wave 1 benefits are on track except theatre cancellations
layout: benefits-tracker
section: Plan
footnote: Actuals to October 2026 for the pilot wards only.

```json
{"benefits": [
  {"name": "Agency spend, pilot wards", "owner": "Dir. of Nursing", "unit": "k/wk", "baseline": 210, "target": 120, "actual": 168, "rag": "G", "due": "Jun 27"},
  {"name": "Rosters published 6 weeks ahead", "owner": "Dir. of Nursing", "unit": "%", "baseline": 0, "target": 95, "actual": 62, "rag": "G", "due": "Jun 27"},
  {"name": "On-the-day theatre cancellations", "owner": "Surgical Dir.", "unit": "%", "baseline": 14, "target": 5, "actual": 12, "rag": "R", "due": "Sep 27"},
  {"name": "Glove contracts", "owner": "Head of Proc.", "unit": "", "baseline": 11, "target": 1, "actual": 6, "rag": "A", "due": "Jan 28"}]}
```

# The new surgical wing is at Gate 3; full business case approval is due in January
layout: stage-gate
section: Capital
footnote: Gates follow the group's capital investment policy.

```json
{"gates": [
  {"label": "Gate 0", "name": "Strategic need", "date": "Mar 2025", "status": "done", "decision": "Approved"},
  {"label": "Gate 1", "name": "Outline business case", "date": "Oct 2025", "status": "done", "decision": "Approved, £430m"},
  {"label": "Gate 2", "name": "Design and procurement", "date": "Jun 2026", "status": "done", "decision": "Approved with conditions"},
  {"label": "Gate 3", "name": "Full business case", "date": "Jan 2027", "status": "current", "criteria": ["Contractor price within £430m", "QRA at P80 funded", "Planning consent"]},
  {"label": "Gate 4", "name": "Handover", "date": "Sep 2028", "status": "future", "criteria": ["Commissioning complete", "Benefits plan agreed"]}]}
```

# Construction has earned £101m of work against £124m planned, and each £1 spent has earned 89p
layout: s-curve
section: Capital
footnote: Enabling works and main construction only. Cumulative from January 2026.

```json
{"exhibit": "Earned value, cumulative", "unit": "£m, nominal", "prefix": "£", "bac": 140,
 "x": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
 "planned": [5, 12, 22, 35, 50, 66, 82, 98, 112, 124, 134, 140],
 "earned": [4, 10, 18, 29, 41, 54, 67, 80, 91, 101],
 "actual": [5, 12, 21, 33, 47, 61, 76, 91, 103, 114],
 "takeaways": ["At this efficiency the phase finishes about **£18m** over its £140m budget."]}
```

# The £430m budget has only about a one-in-four chance of being enough
layout: p-curve
section: Capital
footnote: Monte Carlo cost risk analysis, 5,000 iterations, October 2026 risk register.

```json
{"exhibit": "Probability that outturn cost is at or below", "unit": "£m, nominal", "prefix": "£",
 "points": [[410, 0.0], [420, 0.05], [428, 0.2], [434, 0.4], [437, 0.5], [441, 0.65], [446, 0.8], [452, 0.9], [462, 0.97], [475, 1.0]],
 "budget": 430, "budget_label": "Approved budget",
 "takeaways_title": "Implication for Gate 3",
 "takeaways": ["Funding to P80 needs **£16m** more than approved.", "The largest drivers are ground conditions and the M&E package."]}
```

# Open risks, issues and dependencies for the Board's attention
layout: raid-log
section: Capital

```json
{"items": [
  {"type": "Risk", "id": "R04", "description": "Ground conditions worse than surveyed under Block B", "owner": "Project director", "due": "Dec 26", "rag": "R", "status": "Extra boreholes ordered; results 6 Dec"},
  {"type": "Risk", "id": "R09", "description": "M&E subcontractor capacity in 2027", "owner": "Commercial lead", "due": "Jan 27", "rag": "A", "status": "Second supplier being qualified"},
  {"type": "Issue", "id": "I02", "description": "Planning condition 14 (traffic) not yet discharged", "owner": "Estates director", "due": "Nov 26", "rag": "A", "status": "Submission made 2 Nov"},
  {"type": "Assumption", "id": "A01", "description": "Inflation of 4% a year on construction costs", "owner": "Finance", "due": "Jan 27", "rag": "A", "status": "Recheck against index at Gate 3"},
  {"type": "Dependency", "id": "D03", "description": "Regional funding for equipment (£22m)", "owner": "CFO", "due": "Mar 27", "rag": "G", "status": "Bid submitted; decision expected March"}]}
```
