---
deck: Benefits Modernisation Programme: independent assurance review
context: Department of Community Services  |  Programme Board  |  October 2026
tracker: Rating, Findings, Follow-up
sticker: Draft for discussion
deck_type: assurance
source: Independent assurance team: 31 interviews and 46 documents, 8 September to 9 October 2026. Fictional example.
---

# Benefits Modernisation Programme: independent assurance review, second review
layout: title

```json
{"subtitle": "Independent verification and validation report for the Programme Board",
 "client": "Department of Community Services Programme Board", "date": "20 October 2026", "prepared_by": "Independent Assurance Team"}
```

# Delivery confidence is amber overall: two of eight areas are red, and one finding is critical
layout: key-numbers
section: Rating
footnote: Scope: the full programme, including supplier delivery. Method: 31 interviews, 46 documents and a sample of test evidence. The assurance team has no delivery role and reports to the Audit Committee. Rating scale: Green means delivery is on course; Amber means delivery is achievable if named issues are fixed; Red means delivery is at risk without urgent action.

```json
{"numbers": [
 {"value": "Amber", "label": "Overall delivery confidence", "note": "Unchanged since the April 2026 review", "rag": "A"},
 {"value": "2 of 8", "label": "Areas rated red", "note": "Suppliers, and data and architecture; 4 amber, 2 green", "rag": "R"},
 {"value": "12", "label": "Findings", "note": "**1** critical, **3** high, **5** medium, **3** low", "rag": "R"},
 {"value": "4 of 9", "label": "April recommendations closed", "note": "2 are overdue", "rag": "A"}]}
```

??? Overall is amber because governance and risk management are strong. Without the fix to data migration the programme would move to red at the next review.

# Supplier management and data migration are red and worsening, while risk management has improved
layout: table
section: Rating
footnote: Rating scale as on the previous page. Trend compares with the April 2026 review: up means improved, down means worse.

```json
{"exhibit": "Ratings by area, October 2026", "unit": "Compared with the April 2026 review",
 "columns": [{"name": "Area", "width": 0.25, "kind": "bold"}, {"name": "Rating", "width": 0.08, "kind": "rag"}, {"name": "Trend", "width": 0.08, "kind": "trend"},
             {"name": "Why", "width": 0.59}],
 "rows": [["Governance and sponsorship", "G", "flat", "Board meets monthly; decisions are logged and followed up"],
          ["Business case and benefits", "A", "down", "£11m of the £42m yearly benefit depends on the delayed release 4"],
          ["Schedule and delivery", "A", "down", "Release 3 is six weeks late; release 4 plan is untested"],
          ["Cost and resourcing", "A", "flat", "Forecast is 9% over budget; 14 of 60 posts vacant"],
          ["Risk and issue management", "G", "up", "Register is current and risks have named owners"],
          ["Suppliers and contracts", "R", "down", "Change requests average 41 days to agree; two suppliers disagree on scope"],
          ["Data and architecture", "R", "down", "No tested plan to migrate 2.3 million customer records"],
          ["Testing and release readiness", "A", "up", "Automated testing covers 68% of journeys, up from 40%"]]}
```

??? Count of ratings: two green, four amber, two red. The two red areas are the subject of the next two pages.

# Finding 1, critical: the plan to move 2.3 million customer records has never been tested end to end
layout: columns
section: Findings
footnote: Severity: critical means the programme objective cannot be met without action; high means a milestone is at risk. Management response received 15 October 2026.

```json
{"columns": [
 {"header": "Observation", "icon": "search", "bullets": ["Two trial migrations used 4% of the records", "The full run has never been rehearsed", "No rollback plan exists if cutover fails", "Data quality owner is not named"]},
 {"header": "Impact", "icon": "triangle-alert", "bullets": ["Cutover in July 2027 could overrun its 48-hour window", "Customers could miss payments if records are wrong", "Failure would delay release 4 by about three months"]},
 {"header": "Recommendation", "icon": "list-checks", "bullets": ["Rehearse a full-volume migration by 28 February 2027", "Write and test a rollback plan by 31 March 2027", "Name a data quality owner by 6 November 2026", "Owner: Chief Data Officer"]},
 {"header": "Management response", "icon": "message-square", "bullets": ["Accepted in full", "Rehearsal booked for 22 February 2027", "Rollback plan drafted; test date to be agreed", "Data owner named by 30 October"]}],
 "compare": [
  {"label": "Severity", "values": [{"text": "Critical", "rag": "R"}, {"text": "Cutover at risk", "rag": "R"}, {"text": "Due 28 Feb 2027", "rag": "A"}, {"text": "Accepted", "rag": "G"}]},
  {"label": "Evidence", "values": ["Migration trial reports", "Release 4 plan", "Plan review, 12 Oct", "Response, 15 Oct"]}]}
```

??? This is the finding that would turn the programme red. Management accepted it fully, so the follow-up is about dates, not disagreement.

# Finding 2, high: change requests take 41 days to agree because two suppliers disagree on scope
layout: columns
section: Findings
footnote: Severity: high means a milestone is at risk. Management response received 15 October 2026.

```json
{"columns": [
 {"header": "Observation", "icon": "search", "bullets": ["Twenty-two change requests are open, with 41 days average age", "The platform and integration suppliers each read one interface as the other's job", "The contract sets 15 days for a decision"]},
 {"header": "Impact", "icon": "triangle-alert", "bullets": ["Release 4 scope is not fixed", "Cost forecast is 9% over budget, partly through rework", "Supplier relations are strained"]},
 {"header": "Recommendation", "icon": "list-checks", "bullets": ["Hold a joint scope workshop by 20 November 2026", "Set a 10-day limit for change decisions", "Escalate unresolved items to the SRO each fortnight", "Owner: Commercial Director"]},
 {"header": "Management response", "icon": "message-square", "bullets": ["Accepted in part", "Agrees the workshop and the fortnightly escalation", "Keeps the 15-day contract limit until the contract is varied"]}],
 "compare": [
  {"label": "Severity", "values": [{"text": "High", "rag": "R"}, {"text": "Scope not fixed", "rag": "A"}, {"text": "Due 20 Nov 2026", "rag": "A"}, {"text": "Part accepted", "rag": "A"}]},
  {"label": "Evidence", "values": ["Change log, 22 items", "Cost report, September", "Contract clause 14.2", "Response, 15 Oct"]}]}
```

??? Management accepted part of this one. We still think 10 days is needed, and will check progress in January.

# Four of nine recommendations from April are closed; the two overdue ones both concern suppliers
layout: table
section: Follow-up
footnote: Status: Green = closed and evidenced; Amber = in progress and on time; Red = overdue.

```json
{"exhibit": "Progress on the nine recommendations from the April 2026 review", "unit": "Status at 9 October 2026",
 "columns": [{"name": "Recommendation", "width": 0.42, "kind": "bold"}, {"name": "Owner", "width": 0.16}, {"name": "Due", "width": 0.10},
             {"name": "Status", "width": 0.08, "kind": "rag"}, {"name": "Evidence", "width": 0.24}],
 "rows": [["Appoint a full-time SRO", "Permanent Secretary", "Jun 26", "G", "Appointed 1 June"],
          ["Refresh the risk register monthly", "Programme Director", "May 26", "G", "Six monthly refreshes"],
          ["Fix scope of release 3", "Programme Director", "Jun 26", "G", "Scope signed 12 June"],
          ["Agree a benefits owner for each benefit", "Business Lead", "Jul 26", "G", "Owners named for all 8 benefits"],
          ["Publish an integrated release plan", "Delivery Lead", "Dec 26", "A", "Draft with the Board"],
          ["Automate regression tests", "Test Manager", "Jan 27", "A", "68% coverage"],
          ["Recruit 14 vacant posts", "Resourcing Lead", "Dec 26", "A", "Nine offers made"],
          ["Agree a joint supplier governance forum", "Commercial Director", "Aug 26", "R", "Not yet met"],
          ["Reset supplier performance measures", "Commercial Director", "Sep 26", "R", "Draft not agreed"]]}
```

??? Count: four green, three amber, two red. That matches the four of nine on the summary page.

# The Board should fund the data rehearsal, settle the supplier scope dispute and review progress in January
layout: decisions
section: Follow-up

```json
{"decisions": [
 {"what": "Fund a full-volume data migration rehearsal", "recommendation": "Approve £1.4m from contingency; the rehearsal runs by 28 February 2027", "owner": "SRO", "due": "6 Nov"},
 {"what": "Name a data quality owner and approve a tested rollback plan", "recommendation": "Chief Data Officer to own both; rollback test by 31 March 2027", "owner": "Chief Data Officer", "due": "6 Nov"},
 {"what": "Resolve the supplier scope dispute", "recommendation": "Joint workshop by 20 November; SRO decides any open points the same day", "owner": "Commercial Director", "due": "20 Nov"},
 {"what": "Schedule a follow-up check of the red areas", "recommendation": "Assurance team returns in January 2027 to check the two red areas", "owner": "Programme Director", "due": "29 Jan"}]}
```
