---
deck: Marlow Crossing: independent cost and schedule review
context: Marlow Crossing Authority  |  Board assurance  |  November 2026
tracker: Summary, Cost, Schedule, Findings
sticker: Draft for discussion
deck_type: cost-review
source: Independent review team analysis of project documents as of 30 September 2026. Fictional example.
---

# Marlow Crossing: independent review of forecast cost and opening date
layout: title

```json
{"subtitle": "Independent cost and schedule review for the Marlow Crossing Authority Board",
 "client": "Marlow Crossing Authority", "date": "10 November 2026", "prepared_by": "Independent Review Team"}
```

# The review puts final cost at £337m and opening in June 2028; the project says £312m and January 2028
layout: key-numbers
section: Summary
footnote: Scope: the Marlow Crossing cable-stayed bridge and approaches. Method: 27 interviews, a re-run of the project schedule and a line-by-line check of the cost report. Documents are dated to 30 September 2026. The review team had no role in design or delivery. RAG: green means the review agrees with the project; red means the review differs by more than 5% on cost or 8 weeks on date.

```json
{"numbers": [
 {"value": "£312m", "label": "Project forecast cost (EAC)", "note": "Project cost report, September 2026", "rag": "G"},
 {"value": "£337m", "label": "Review view of cost", "note": "**£25m** (8.0%) above the project", "rag": "R"},
 {"value": "28 Jan 2028", "label": "Project opening date", "note": "Project schedule, September 2026", "rag": "G"},
 {"value": "23 Jun 2028", "label": "Review view of opening", "note": "**21 weeks** later than the project", "rag": "R"}]}
```

??? The two numbers on the right are where we disagree with the project. Everything else in the pack explains why.

# The project's forecast is optimistic on productivity, utilities and steel, and we expect a later opening
layout: exec-summary
section: Summary

```json
{"points": [
 {"lead": "Cost", "support": ["We add **£29m** of risks the forecast leaves out, and remove £4m counted twice", "Review view is **£337m**, 8.0% above the project"]},
 {"lead": "Schedule", "support": ["Pile caps are running 12 weeks behind and delay everything after them", "Review view of opening is 23 June 2028, 21 weeks later"]},
 {"lead": "Findings", "support": ["Six findings: two high, three medium, one low", "Both high findings are on the critical path"]},
 {"lead": "What we ask", "support": ["Reforecast to the review view, then fund contingency at P80", "Fix the two high findings before the next payment milestone"]}]}
```

??? Where we agree with the project: the design is sound and the main contractor has held its prices on the work already let.

# The review adds £25m to the project's £312m forecast, mainly for pile cap productivity and unpriced utilities
layout: waterfall
section: Cost
footnote: Increases are shown in red. Utilities diversion excludes any claims from the utility owner.
footnote: Vertical axis starts at £290m.

```json
{"exhibit": "Project forecast cost to review view of cost", "unit": "£m, nominal, September 2026, project estimate class 3",
 "axis_min": 290, "prefix": "£", "start": {"label": "Project EAC", "value": 312},
 "steps": [{"label": "Pile cap productivity", "value": 9}, {"label": "Utilities diversion unpriced", "value": 14},
           {"label": "Steel price escalation", "value": 6}, {"label": "Contingency counted twice", "value": -4}],
 "end": {"label": "Review view", "value": 337},
 "callouts": [0, 1],
 "takeaways_title": "Where we disagree",
 "takeaways": ["Pile caps take 14 weeks per cap, not the 10 weeks in the forecast: **+£9m**.", "The utility owner's diversion quote of **£14m** is not in the forecast.", "Contingency is held in two budget lines, so we remove **£4m**."]}
```

??? 312 plus 9, 14 and 6 is 341, less 4 is 337. The steel increase uses the current index and the contractor's mill order dates.

# The review expects opening 21 weeks after the project's date because pile caps delay the whole chain
layout: gantt
section: Schedule
footnote: The review view re-runs the project's schedule logic with measured productivity.

```json
{"exhibit": "Project forecast against review forecast", "unit": "Level 2 schedule, January 2027 to June 2028",
 "start": "2027-01-01", "end": "2028-06-30", "today": "2027-01-04",
 "legend_labels": {"baseline": "Project forecast", "critical": "Review view, critical path", "other": "Review view, other"},
 "rows": [
  {"name": "Foundations and pile caps", "rag": "R", "critical": true, "callout": 1, "baseline": ["2027-01-04", "2027-04-30"], "forecast": ["2027-01-04", "2027-07-23"]},
  {"name": "Abutments and piers", "rag": "R", "critical": true, "baseline": ["2027-03-01", "2027-08-13"], "forecast": ["2027-05-24", "2027-10-22"]},
  {"name": "Deck beam erection", "rag": "A", "critical": true, "baseline": ["2027-06-01", "2027-11-12"], "forecast": ["2027-08-30", "2028-02-18"]},
  {"name": "Parapets and drainage", "rag": "A", "baseline": ["2027-09-06", "2027-12-17"], "forecast": ["2027-12-06", "2028-04-14"]},
  {"name": "Surfacing and systems", "rag": "A", "baseline": ["2027-11-01", "2028-01-07"], "forecast": ["2028-03-06", "2028-05-12"]},
  {"name": "Load testing and commissioning", "rag": "R", "critical": true, "callout": 2, "baseline": ["2027-11-05", "2028-01-28"], "forecast": ["2028-04-03", "2028-06-23"]}],
 "milestones": [{"name": "Opening", "baseline": "2028-01-28", "forecast": "2028-06-23", "callout": 3}],
 "takeaways_title": "What the schedule shows",
 "takeaways": ["Pile caps finish 12 weeks late, and nothing downstream has float to absorb it.", "Testing takes about 12 weeks in both plans, and neither has any float.", "Opening moves from 28 January to 23 June 2028."]}
```

??? Check the arithmetic: 28 January to 23 June is 147 days, or 21 weeks.

# Six findings, two of them high severity, explain the gap between the project and the review
layout: table
section: Findings
footnote: Severity: Red = high (changes cost by more than £5m or opening by more than 8 weeks); Amber = medium (£1m to £5m or 2 to 8 weeks); Green = low (below those).

```json
{"exhibit": "Review findings by severity", "unit": "Evidence as of 30 September 2026",
 "rag_labels": {"R": "High severity", "A": "Medium", "G": "Low"},
 "columns": [{"name": "#", "width": 0.04}, {"name": "Finding", "width": 0.36, "kind": "bold"}, {"name": "Severity", "width": 0.09, "kind": "rag"},
             {"name": "Effect", "width": 0.17}, {"name": "Evidence", "width": 0.22}, {"name": "Owner", "width": 0.12}],
 "rows": [["1", "Pile cap productivity is below the forecast rate", "R", "+£9m, +12 weeks", "Site records, caps 1 to 6", "Construction director"],
          ["2", "Utility diversion quote of £14m is not in the forecast", "R", "+£14m", "Utility owner quote, 14 Aug", "Commercial director"],
          ["3", "Steel escalation uses a stale index", "A", "+£6m", "Mill order dates, index", "Commercial director"],
          ["4", "Testing window has no float", "A", "Up to 6 weeks", "Schedule logic check", "Planning manager"],
          ["5", "Contingency held in two budget lines", "A", "-£4m", "Cost report lines 41 and 58", "Finance lead"],
          ["6", "Risk register not updated since June", "G", "None directly", "Register version history", "Risk manager"]]}
```

??? Findings 1 and 2 are the two highs. The effects on cost in findings 1, 2, 3 and 5 are the four bars in the waterfall.

# The Board should reforecast to the review view and fund the two high findings before the next payment milestone
layout: decisions
section: Findings

```json
{"decisions": [
 {"what": "Reforecast cost to £337m and opening to 23 June 2028", "recommendation": "Adopt the review view as the planning basis until the project can evidence its own faster rates", "owner": "Project director", "due": "15 Dec"},
 {"what": "Agree the £14m utility diversion with the utility owner", "recommendation": "Negotiate a fixed price before the October 2027 diversion window closes", "owner": "Commercial director", "due": "31 Jan"},
 {"what": "Commission a pile cap productivity recovery plan", "recommendation": "Contractor to present a plan with a second rig option and its cost", "owner": "Construction director", "due": "29 Jan"},
 {"what": "Re-run the quantified risk analysis on the new forecast", "recommendation": "Set contingency at P80 and publish the confidence level", "owner": "Risk manager", "due": "28 Feb"}]}
```

??? Ask for the reforecast first. The other three decisions follow from it.
