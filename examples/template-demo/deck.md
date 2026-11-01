---
deck: Northline Rail Programme: October SteerCo
context: Northline Rail Programme  |  Monthly SteerCo  |  October 2026
tracker: Summary, Schedule, Risk, Cost, Workstreams, Options
sticker: Preliminary
source: Programme controls period 7 report (Oct 2026); PMO analysis. Fictional example.
---

# Northline Rail Programme: October 2026 SteerCo
layout: title

```json
{"subtitle": "Programme status, schedule recovery options and decisions needed",
 "client": "Northline Transport Authority", "date": "4 November 2026", "prepared_by": "Programme Management Office"}
```

??? Fictional example built with Consulting Deck Studio.

# Agenda
layout: agenda

```json
{"items": [{"title": "Summary and decisions needed", "note": "10 min"},
           {"title": "Schedule: critical path and handover date", "note": "10 min"},
           {"title": "Risk: two risks escalated to red", "note": "10 min"},
           {"title": "Cost: £40m increase since Gate 3", "note": "10 min"},
           {"title": "Workstream status", "note": "5 min"},
           {"title": "Recovery options and recommendation", "note": "15 min"}]}
```

# Handover has slipped six weeks; three decisions this month decide whether it recovers
layout: exec-summary
section: Summary
footnote: Re-baselined at Gate 3, March 2026.

```json
{"points": [
  {"lead": "Handover has moved from 3 April to 15 May 2027",
   "support": ["The utilities diversion at Kings Cross finished six weeks late", "Systems integration is now on the critical path, with no float"]},
  {"lead": "Forecast cost is £1,420m, £40m over the Gate 3 budget",
   "support": ["Utilities (+£22m) and signalling (+£15m) explain most of the increase", "Contingency still covers it, but falls to 3% of remaining work against a 5% floor"]},
  {"lead": "Two of the top ten risks moved into red this period",
   "support": ["Signalling software maturity: the supplier missed drops 3 and 4", "Christmas possessions: Network Rail has confirmed 2 of 5 weekends"]},
  {"lead": "We recommend running systems integration in parallel with fit-out (Option B)",
   "support": ["It costs £14m from contingency and is the only option that holds the May date", "It needs SteerCo approval by 14 November to keep the test windows"]}]}
```

??? Walk through the four lead statements; the detail is in the following slides.

# Handover has slipped six weeks; three decisions this month decide whether it recovers
layout: status-summary
section: Summary
footnote: Re-baselined at Gate 3, March 2026. Trend compares with the September report.

```json
{"rows": [
  {"area": "Schedule", "icon": "calendar-clock", "rag": "R", "trend": "down", "text": "Forecast handover moved from **3 Apr to 15 May 2027**. The utilities diversion ran six weeks late; systems integration is now on the critical path."},
  {"area": "Cost", "icon": "pound-sterling", "rag": "A", "trend": "flat", "text": "EAC of **£1,420m** against a £1,380m budget. Contingency covers the gap but falls to 3% of remaining work, below the 5% floor."},
  {"area": "Risk", "icon": "triangle-alert", "rag": "R", "trend": "down", "text": "Two of the top ten risks moved into red: signalling software maturity and Christmas possessions. Neither has a funded mitigation."},
  {"area": "Stakeholders", "icon": "users", "rag": "G", "trend": "flat", "text": "The operator and Network Rail still back the May date. Sponsor briefing held on 22 October."}],
 "lookahead": {"title": "Look-ahead: key milestones in the next 90 days", "rows": [
  {"milestone": "Signalling software drop 4 accepted", "baseline": "30 Oct", "forecast": "8 Nov", "variance": "+9 days", "rag": "R"},
  {"milestone": "Test windows confirmed by operator", "baseline": "1 Nov", "forecast": "14 Nov", "variance": "+13 days", "rag": "R"},
  {"milestone": "Station 3 fit-out complete", "baseline": "12 Dec", "forecast": "19 Dec", "variance": "+7 days", "rag": "A"},
  {"milestone": "Systems integration starts", "baseline": "6 Jan", "forecast": "6 Jan", "variance": "On plan", "rag": "G"}]},
 "decisions_title": "Decisions needed from the SteerCo",
 "decisions": [
  {"what": "Approve £14m contingency drawdown for parallel systems integration", "owner": "SRO", "due": "14 Nov"},
  {"what": "Confirm the December possession plan with Network Rail", "owner": "Interface lead", "due": "21 Nov"},
  {"what": "Assign one owner for systems integration risk across client and contractor", "owner": "Commercial director", "due": "30 Nov"}]}
```

??? This is the one-page version for SteerCo members who read only page 3.

# Schedule
layout: section

```json
{"number": "02", "subtitle": "Critical path, float and the handover date"}
```

# Handover holds only if the operator confirms test windows by 14 November
layout: gantt
section: Schedule
footnote: Baseline is the Gate 3 re-baseline (March 2026). Float is total float on the Level 2 schedule.

```json
{"exhibit": "Integrated schedule, baseline vs current forecast", "unit": "Level 2 programme schedule, October 2026 to June 2027",
 "start": "2026-10-01", "end": "2027-06-30", "today": "2026-11-03",
 "rows": [
  {"name": "Main civils", "rag": "G", "baseline": ["2026-10-01", "2026-10-31"], "forecast": ["2026-10-01", "2026-11-12"]},
  {"name": "Track and OHLE", "rag": "G", "baseline": ["2026-10-15", "2027-01-01"], "forecast": ["2026-10-18", "2027-01-07"]},
  {"name": "Signalling install", "rag": "A", "critical": true, "baseline": ["2026-11-06", "2027-01-18"], "forecast": ["2026-11-15", "2027-02-06"]},
  {"name": "Systems integration", "rag": "R", "critical": true, "callout": 1, "baseline": ["2027-01-01", "2027-03-18"], "forecast": ["2027-01-12", "2027-04-15"]},
  {"name": "Station fit-out", "rag": "A", "callout": 2, "baseline": ["2026-12-01", "2027-03-01"], "forecast": ["2026-12-06", "2027-03-12"], "float_to": "2027-04-15", "float_label": "5 wks float"},
  {"name": "Trial running", "rag": "A", "critical": true, "baseline": ["2027-02-18", "2027-03-18"], "forecast": ["2027-04-15", "2027-05-14"]}],
 "milestones": [{"name": "Handover", "baseline": "2027-04-03", "forecast": "2027-05-15", "callout": 3}],
 "takeaways_title": "What the schedule shows",
 "takeaways": ["Systems integration now drives handover. Its finish has slipped four weeks, to mid-April.",
               "Station fit-out has five weeks of float, so it can move to make room for testing.",
               "The 15 May date holds only if the operator confirms test windows by 14 November."],
 "panels": [{"title": "Next steps", "bullets": ["Operator to confirm test windows (14 Nov)", "Delivery partner to issue a resequenced fit-out plan (21 Nov)", "PMO to re-run schedule risk analysis on the new logic (28 Nov)"]}]}
```

??? Numbered callouts tie each bar to the takeaways on the right.

# Two risks moved into the red zone this period, and neither has a funded mitigation yet
layout: risk-heatmap
section: Risk
footnote: Score = likelihood x impact on a 5 x 5 scale. Red is 15 or more; amber 8 to 14; green 7 or less.

```json
{"exhibit": "Top risks, current position", "unit": "Likelihood x impact, October 2026",
 "risks": [
  {"id": "R07", "title": "Signalling software maturity: supplier missed drops 3 and 4", "owner": "S. Novak", "l": 5, "i": 4, "prev": [3, 4], "mitigation": "Recovery plan due 8 Nov; independent code review proposed (unfunded)"},
  {"id": "R12", "title": "Christmas possessions: 3 of 5 weekends unconfirmed", "owner": "Interface lead", "l": 4, "i": 4, "prev": [3, 3], "mitigation": "Escalated to Network Rail route director; decision 21 Nov"},
  {"id": "R03", "title": "Utilities diversion claims from main contractor", "owner": "R. Dube", "l": 3, "i": 5, "prev": [3, 5], "mitigation": "£6-9m exposure; valuation agreed, settlement talks under way"},
  {"id": "R18", "title": "Driver training capacity for trial running", "owner": "K. Ahmed", "l": 2, "i": 3, "prev": [2, 3], "mitigation": "Second simulator booked from January"},
  {"id": "R21", "title": "Late design changes at Station 3", "owner": "A. Silva", "l": 3, "i": 2, "prev": [3, 3], "mitigation": "Design freeze agreed 15 Oct; change board in place"}]}
```

??? R07 and R12 need funded mitigations; ask owners to bring them in November.

# Forecast cost has risen £40m since Gate 3, driven mostly by utilities and signalling
layout: waterfall
section: Cost
footnote: Vertical axis starts at £1,300m.
footnote: EAC = estimate at completion; excludes £12m of unquantified claims.

```json
{"exhibit": "Bridge from Gate 3 budget to current forecast", "unit": "£m, nominal, October 2026",
 "axis_min": 1300, "prefix": "£", "start": {"label": "Gate 3 budget", "value": 1380},
 "steps": [{"label": "Utilities diversion", "value": 22}, {"label": "Signalling", "value": 15},
           {"label": "Design changes", "value": 9}, {"label": "Scope removed", "value": -6}],
 "end": {"label": "Current EAC", "value": 1420}, "callouts": [1, 2, 4],
 "takeaways_title": "What drives the increase",
 "takeaways": ["Utilities added **£22m**: the six-week overrun at Kings Cross and the contractor's prolongation claim.",
               "Signalling added **£15m** after two missed software drops.",
               "Deferring the Station 5 canopy saves **£6m**, but the sponsor has not approved it."],
 "panels": [{"title": "Open points", "bullets": ["£12m of unquantified claims sit outside the EAC", "Scope removal needs sponsor approval"]}]}
```

# Contingency has fallen faster than work has been completed since Gate 3
layout: line
section: Cost
footnote: Floor is the minimum contingency set at Gate 3: 5% of remaining work.

```json
{"exhibit": "Contingency remaining vs floor", "unit": "% of remaining work, month end", "suffix": "%", "decimals": 1,
 "x": ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
 "series": [{"name": "Contingency remaining", "values": [8.2, 7.9, 7.4, 6.6, 5.9, 4.8, 3.9, 3.0], "highlight": true},
            {"name": "Floor", "values": [5, 5, 5, 5, 5, 5, 5, 5], "color": "#C62828", "forecast": true, "markers": false}],
 "takeaways_title": "What the trend shows",
 "takeaways": ["Contingency crossed the 5% floor in August and has fallen about 0.9 points a month since.",
               "At this rate it runs out by February 2027, before trial running starts."]}
```

# Four of seven workstreams are on track; two need SteerCo decisions
layout: rag-dashboard
section: Workstreams
footnote: Green: on track. Amber: at risk but recoverable within tolerance. Red: outside tolerance, needs a decision. SPI and CPI are cumulative earned-value indices.

```json
{"kpis": [{"value": "6", "label": "Weeks behind baseline", "note": "Handover forecast 15 May 2027", "rag": "R"},
          {"value": "0.91", "label": "Schedule performance (SPI)", "note": "Down from 0.94 in September", "rag": "A"},
          {"value": "0.97", "label": "Cost performance (CPI)", "note": "Stable for three periods", "rag": "A"},
          {"value": "£41m", "label": "Contingency remaining", "note": "3.0% of remaining work; floor is 5%", "rag": "R"}],
 "rows": [
  {"workstream": "Civils", "lead": "J. Patel", "schedule": "G", "cost": "G", "risk": "A", "trend": "flat", "comment": "Complete; contractor claims being closed out"},
  {"workstream": "Track and OHLE", "lead": "M. Okafor", "schedule": "G", "cost": "A", "risk": "G", "trend": "flat", "comment": "Night-shift productivity 8% below plan; extra crew from November"},
  {"workstream": "Signalling", "lead": "S. Novak", "schedule": "R", "cost": "A", "risk": "R", "trend": "down", "comment": "Software drop 4 missed; recovery plan due 8 Nov"},
  {"workstream": "Systems integration", "lead": "L. Chen", "schedule": "R", "cost": "A", "risk": "R", "trend": "down", "comment": "Test windows not confirmed; decision needed 14 Nov"},
  {"workstream": "Stations", "lead": "A. Silva", "schedule": "A", "cost": "G", "risk": "A", "trend": "up", "comment": "Fit-out resequenced to protect float"},
  {"workstream": "Operations readiness", "lead": "K. Ahmed", "schedule": "G", "cost": "G", "risk": "G", "trend": "flat", "comment": "Driver training on plan"},
  {"workstream": "Commercial", "lead": "R. Dube", "schedule": "G", "cost": "A", "risk": "A", "trend": "flat", "comment": "Utilities claim valued at £6-9m"}]}
```

# Signalling and systems integration hold nearly three-quarters of schedule risk
layout: bar
section: Workstreams
footnote: P80 minus P50 finish date from the October schedule risk analysis (1,000 iterations).

```json
{"exhibit": "Contribution to schedule risk by workstream", "unit": "Working days between P50 and P80 finish", "orientation": "bar",
 "categories": ["Systems integration", "Signalling", "Station fit-out", "Track and OHLE", "Operations readiness", "Civils"],
 "series": [{"name": "Days", "values": [21, 14, 5, 4, 3, 1]}], "highlight": 0, "label_width": 140,
 "takeaways_title": "Implication",
 "takeaways": ["Mitigation money should go to systems integration and signalling first; together they explain 35 of 48 days.",
               "Fit-out and track risk is small enough to manage within the workstreams."]}
```

# Programme spend has grown 29% a year since 2023, and 2027 is the peak year
layout: bar
section: Cost
footnote: 2026 and 2027 are forecasts.

```json
{"exhibit": "Annual capital spend", "unit": "£m, nominal", "categories": ["2023", "2024", "2025", "2026F", "2027F"],
 "series": [{"name": "Spend", "values": [190, 260, 340, 410, 455]}], "highlight": 4, "prefix": "£",
 "cagr": {"from": 0, "to": 3, "label": "+29% a year"},
 "takeaways_title": "What this means",
 "takeaways": ["2027 needs £455m, the highest of any year; funding is confirmed for £430m.",
               "The £25m gap must be closed before the Q1 2027 budget round."]}
```

# The three recovery options trade cost against the May 2027 handover date
layout: columns
section: Options

```json
{"columns": [
  {"header": "A: Re-baseline to September 2027", "bullets": ["No extra spend now", "Revenue service slips by four months", ["Lost fares of about £18m", 2], "Needs a new Gate 3 approval"]},
  {"header": "B: Run integration in parallel with fit-out", "bullets": ["£14m from contingency", "Holds the 15 May 2027 handover", "Contingency drops below the 5% floor", ["Sponsor must approve the breach", 2]]},
  {"header": "C: Phased opening", "bullets": ["Open three of five stations in May", "£6m of temporary works", "Operator has not agreed to it", "Two openings mean two sets of assurance work"]}],
 "compare": [
  {"label": "Extra cost now", "values": ["£0", "£14m", "£6m"]},
  {"label": "Handover", "values": [{"text": "Sept 2027", "rag": "R"}, {"text": "15 May 2027", "rag": "G"}, {"text": "May 2027 (partial)", "rag": "A"}]},
  {"label": "Contingency after", "values": [{"text": "3.0%", "rag": "A"}, {"text": "2.0%", "rag": "R"}, {"text": "2.6%", "rag": "R"}]}]}
```

# Option B scores highest: £14m now, and the only option that protects May
layout: options-matrix
section: Options
sowhat: We recommend Option B: approve £14m to run systems integration in parallel with fit-out
footnote: Scores are the PMO's assessment with the delivery partner, reviewed by the client commercial team on 28 October.

```json
{"stages": ["Long list (7)", "Screened (3)", "Evaluated", "Recommendation"], "stage": "Evaluated",
 "criteria": [{"name": "Protects May handover", "weight": "30%"}, {"name": "Cost to complete", "weight": "25%"},
              {"name": "Deliverability", "weight": "20%"}, {"name": "Commercial risk", "weight": "15%"},
              {"name": "Stakeholder support", "weight": "10%"}],
 "options": [{"key": "A", "name": "Re-baseline to Sept 2027", "scores": [1, 4, 3, 3, 1]},
             {"key": "B", "name": "Parallel integration (+£14m)", "scores": [4, 2, 3, 3, 3]},
             {"key": "C", "name": "Phased opening", "scores": [2, 3, 2, 1, 2]}],
 "recommended": "B",
 "rationale": ["Only option that keeps the 15 May 2027 handover", "£14m is within remaining contingency, though it takes the balance below the 5% floor", ["Floor breach needs sponsor sign-off", 2], "The delivery partner has run parallel integration on two comparable schemes", "Option A is cheaper but delays revenue service by four months"]}
```

# Option B sits in the only quadrant that keeps both the date and an acceptable cost
layout: matrix-2x2
section: Options

```json
{"x": {"label": "Confidence in May 2027 handover", "low": "Low", "high": "High"},
 "y": {"label": "Extra cost", "low": "Low", "high": "High"},
 "quadrants": ["Pay more, still late", "Pay to protect the date", "Cheap but late", "Best case"],
 "highlight_quadrant": 1,
 "items": [{"label": "A: Re-baseline", "x": 0.12, "y": 0.1}, {"label": "B: Parallel integration", "x": 0.78, "y": 0.62, "highlight": true, "size": 1.3},
           {"label": "C: Phased opening", "x": 0.42, "y": 0.35}, {"label": "Do nothing", "x": 0.2, "y": 0.04}],
 "takeaways_title": "Reading the matrix",
 "takeaways": ["No option sits in the best-case quadrant.", "B buys confidence in the date for £14m; A and C save money but miss May."]}
```

# Milestones due before the next SteerCo
layout: table
section: Workstreams

```json
{"exhibit": "Milestones due by 4 December 2026",
 "columns": [{"name": "Milestone", "width": 0.34, "kind": "bold"}, {"name": "Owner", "width": 0.14}, {"name": "Due", "width": 0.10},
             {"name": "Status", "width": 0.08, "kind": "rag"}, {"name": "Comment", "width": 0.34}],
 "rows": [["Signalling software drop 4 accepted", "S. Novak", "8 Nov", "R", "Supplier confirms drop on 6 Nov"],
          ["Test windows confirmed by operator", "L. Chen", "14 Nov", "R", "Depends on SteerCo decision 1"],
          ["December possession plan agreed", "Interface lead", "21 Nov", "A", "Route director meeting on 18 Nov"],
          ["Resequenced fit-out plan issued", "A. Silva", "21 Nov", "G", "Draft shared with operator"],
          ["Schedule risk analysis re-run", "PMO", "28 Nov", "G", "New logic loaded"]]}
```

# The SteerCo needs to make three decisions by 30 November to hold the May handover
layout: decisions
section: Summary

```json
{"decisions": [
  {"what": "Approve £14m contingency drawdown for parallel systems integration", "recommendation": "Approve. It is the only option that holds 15 May 2027; contingency falls to 2% of remaining work", "owner": "SRO", "due": "14 Nov"},
  {"what": "Confirm the December possession plan with Network Rail", "recommendation": "Escalate to route director; without three more weekends, signalling slips a further three weeks", "owner": "Interface lead", "due": "21 Nov"},
  {"what": "Assign one owner for systems integration risk", "recommendation": "Commercial director to own it, with a joint client and contractor risk budget", "owner": "Commercial director", "due": "30 Nov"}]}
```
