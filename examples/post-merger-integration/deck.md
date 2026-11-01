---
deck: Northgate and Verano: integration plan
context: Northgate Components  |  Integration Steering Committee  |  January 2027
tracker: Value, Day 1, Benefits, Governance, Plan
sticker: Draft for discussion
deck_type: transformation
source: Northgate and Verano integration planning files, January 2027; Integration Management Office analysis. Fictional example.
---

# Northgate and Verano: integration plan from Day 1 to Day 100
layout: title

```json
{"subtitle": "Savings target, Day-1 readiness and integration governance", "client": "Integration Steering Committee",
 "date": "26 January 2027", "prepared_by": "Integration Management Office"}
```

# The merger targets £62m of net annual savings and gains for £48m of one-off cost, starting on 1 March 2027
layout: key-numbers
section: Value
footnote: Benefit means cost savings plus extra profit from cross-selling, net run-rate by year three. Cost to achieve is one-off and cumulative over three years.

```json
{"numbers": [
  {"value": "£62m", "label": "Net run-rate benefit, year three", "note": "Gross £67m less **£5m** customer losses"},
  {"value": "£48m", "label": "One-off cost to achieve", "note": "Paid back about nine months after full run rate"},
  {"value": "1 Mar 2027", "label": "Day 1", "note": "Day 100 is 8 June 2027"},
  {"value": "5 of 8", "label": "Day-1 must-haves on track", "note": "Two at risk, one red"}]}
```

??? Four numbers frame the decision. The £62m is net of customer loss we expect from overlapping accounts. Competitively sensitive data stayed with the clean team until clearance.

# Day 1 is 1 March 2027 and Day 100 is 8 June 2027, with a Steering Committee review at each
layout: timeline
section: Day 1
footnote: Day 1 is the first day of combined ownership. Day 100 is counted from Day 1, inclusive.

```json
{"start": "2026-12-01", "end": "2027-09-30",
 "events": [
  {"date": "2026-12-15", "label": "Integration plan approved", "done": true},
  {"date": "2027-01-20", "label": "Competition clearance received", "done": true},
  {"date": "2027-03-01", "label": "Day 1", "detail": "Combined ownership"},
  {"date": "2027-03-30", "label": "Day 30 review", "detail": "Day-1 issues closed"},
  {"date": "2027-06-08", "label": "Day 100 review", "detail": "Benefit plan reset"},
  {"date": "2027-09-30", "label": "Supplier contracts renegotiated", "detail": "First £8m run-rate"}]}
```

??? Clearance came on 20 January, so the clean-team restrictions on pricing and customer data lift on Day 1, not before.

# Five of eight Day-1 must-haves are on track, two are at risk, and payroll is red
layout: table
section: Day 1
footnote: Green means on track for Day 1. Amber means at risk with a recovery plan agreed. Red means Day 1 will be missed without a decision.

```json
{"exhibit": "Day-1 must-haves and status", "unit": "As at 26 January 2027",
 "columns": [{"name": "Must-have", "width": 0.33, "kind": "bold"}, {"name": "Owner", "width": 0.15}, {"name": "Due", "width": 0.09},
             {"name": "Status", "width": 0.09, "kind": "rag"}, {"name": "Comment", "width": 0.34}],
 "rows": [["Legal entities and banking in place", "General Counsel", "19 Feb", "G", "Accounts opened; signatories agreed"],
          ["Employees paid correctly", "HR director", "25 Feb", "R", "No single payroll file; fallback is two payrolls"],
          ["Top 200 customers contacted", "Sales director", "26 Feb", "G", "Letters approved; calls scheduled"],
          ["Suppliers paid without interruption", "Finance director", "26 Feb", "G", "Vendor list matched across both ledgers"],
          ["Email and access for 310 shared staff", "IT director", "26 Feb", "A", "Accounts built; testing slipped a week"],
          ["Safety and quality systems unchanged at all 11 sites", "Operations director", "28 Feb", "G", "No change on Day 1"],
          ["Regulatory notices filed", "General Counsel", "20 Jan", "G", "Clearance received"],
          ["Brand and signage rules agreed", "Marketing director", "12 Feb", "A", "Joint name decision awaiting Steering Committee"]]}
```

??? Count them: five green, two amber and one red. Payroll is red because the two systems cannot produce one file by Day 1. The fallback is safe but costs £0.2m a month.

# Procurement and footprint deliver 41 of the £67m gross benefit; after £5m of customer losses the net target is £62m
layout: waterfall
section: Benefits
footnote: Run-rate by year three. Phasing: £18m in year one, £42m in year two, £62m in year three. Customer losses are expected on overlapping accounts.

```json
{"exhibit": "Net run-rate benefit by type", "unit": "£m per year, year three", "prefix": "£",
 "increase_is": "good",
 "start": {"label": "Today", "value": 0}, "show_total_change": false,
 "steps": [{"label": "Procurement", "value": 24}, {"label": "Footprint and operations", "value": 17},
           {"label": "Overheads", "value": 14}, {"label": "Revenue cross-sell", "value": 12},
           {"label": "Customer losses", "value": -5}],
 "end": {"label": "Net benefit", "value": 62},
 "callouts": [1, 4],
 "takeaways_title": "What the bridge shows",
 "takeaways": ["Procurement and footprint add **£41m**, 61% of gross benefit.", "Cross-sell is the least certain step and is phased in from year two."]}
```

??? 24 plus 17 plus 14 plus 12 gives 67 gross. Take off 5 of customer loss and the net is 62. 41 over 67 is 61 per cent.

# The Integration Management Office reports to the Steering Committee and runs six workstreams, including the clean team
layout: org-chart
section: Governance
footnote: Roles only. The clean team handles competitively sensitive data until Day 1 under the competition-law protocol.

```json
{"nodes": [
  {"id": "steer", "title": "Integration Steering Committee", "name": "Chairs: both CEOs"},
  {"id": "imo", "title": "Integration Management Office", "name": "Integration Director", "parent": "steer", "highlight": true},
  {"id": "com", "title": "Commercial", "name": "Sales director", "parent": "imo"},
  {"id": "ops", "title": "Operations and supply", "name": "Operations director", "parent": "imo"},
  {"id": "fit", "title": "Finance and IT", "name": "Finance director", "parent": "imo"},
  {"id": "ppl", "title": "People and culture", "name": "HR director", "parent": "imo"},
  {"id": "cmm", "title": "Communications", "name": "Head of communications", "parent": "imo"},
  {"id": "clean", "title": "Clean team and legal", "name": "General Counsel", "parent": "imo"}]}
```

??? The IMO is eight people. Each workstream lead owns Day-1 must-haves and a savings target, and reports weekly to the IMO.

# Benefits build from £18m in year one to £62m in year three, led by procurement and footprint
layout: roadmap
section: Plan
footnote: Quarters are calendar quarters. Run-rate by year three: £62m net. Cumulative one-off cost of £48m.

```json
{"periods": ["Q1 27", "Q2 27", "Q3 27", "Q4 27", "2028", "2029"],
 "phases": [{"name": "Prepare", "start": 0, "end": 0.67}, {"name": "Day 1 to Day 100", "start": 0.67, "end": 1.67}, {"name": "Integrate", "start": 1.67, "end": 4}, {"name": "Optimise", "start": 4, "end": 6}],
 "lanes": [
  {"name": "Procurement", "items": [{"label": "Supplier consolidation", "start": 1.67, "end": 4, "rag": "G"}, {"label": "Full run rate (£24m)", "start": 4, "end": 6}]},
  {"name": "Footprint", "items": [{"label": "Site review", "start": 1, "end": 2.5}, {"label": "Close two sites", "start": 2.5, "end": 5, "rag": "A"}]},
  {"name": "IT and finance", "items": [{"label": "Single ERP", "start": 1, "end": 5, "rag": "A"}, {"label": "Shared service centre", "start": 4, "end": 6}]},
  {"name": "Milestones", "items": [{"label": "Day 1", "type": "milestone", "at": 0.67}, {"label": "Day 100", "type": "milestone", "at": 1.67}, {"label": "£62m", "type": "milestone", "at": 5.6}]}],
 "today": 0}
```

??? Procurement is first because contracts renew from Q2. The single ERP is amber: it is the longest item and sets the date for the shared service centre.
