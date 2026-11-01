---
deck: Lantern Customer Platform Programme: risk review
context: Harbour Mutual Insurance  |  Programme Board  |  November 2026
tracker: Summary, Risks, Exposure, Actions
sticker: Draft for discussion
deck_type: risk-review
source: Lantern programme risk register, version 14 dated 30 October 2026; PMO analysis. Fictional example.
---

# Lantern Programme risk review: where we stand and what needs funding
layout: title

```json
{"subtitle": "Risk position, movement since September and decisions for the Programme Board",
 "client": "Harbour Mutual Insurance Programme Board", "date": "11 November 2026", "prepared_by": "Programme Management Office"}
```

# Four of 24 open risks are red, and three of them still have no funded mitigation
layout: key-numbers
section: Summary
footnote: Score = likelihood x impact on a 5 x 5 scale. Red is 15 or more; amber 8 to 14; green 7 or less. Exposure is the P80 cost of risks above the £42.0m base estimate.

```json
{"numbers": [
 {"value": "24", "label": "Open risks", "note": "Down from 26 in September", "rag": "A"},
 {"value": "4", "label": "Red risks", "note": "Two entered the red zone this month", "rag": "R"},
 {"value": "£12.0m", "label": "Quantified exposure at P80", "note": "Against £6.0m of contingency", "rag": "R"},
 {"value": "3", "label": "New risks this period", "note": "None scores above 9", "rag": "G"}]}
```

??? Count of reds: R03, R07, R11 and R14. R07 and R14 are the two that entered red this month. Exposure of 12.0 is the P80 of 54.0 less the base of 42.0.

# Four risks are red: two moved up into the red zone this month and the vendor delay worsened again
layout: risk-heatmap
section: Risks
footnote: Score = likelihood x impact on a 5 x 5 scale. Red is 15 or more; amber 8 to 14; green 7 or less. Arrows show movement since the September review.

```json
{"exhibit": "Top risks, current position and movement", "unit": "Likelihood x impact, 30 October 2026",
 "risks": [
  {"id": "R03", "title": "Data migration vendor misses the March 2027 cutover", "owner": "A. Mensah", "l": 5, "i": 4, "prev": [4, 4], "mitigation": "Options on next page; decision needed 25 Nov"},
  {"id": "R07", "title": "Loss of integration specialists to a competitor", "owner": "HR director", "l": 4, "i": 4, "prev": [3, 4], "mitigation": "Retention bonus proposal, £0.6m, not yet funded"},
  {"id": "R11", "title": "Regulator approval of the new claims process slips", "owner": "Compliance head", "l": 3, "i": 5, "prev": [3, 5], "mitigation": "Pre-submission meeting held 22 Oct; submission 8 Dec"},
  {"id": "R14", "title": "Test environment unavailable for 6 weeks in Q1", "owner": "T. Okafor", "l": 5, "i": 3, "prev": [4, 3], "mitigation": "Second environment quoted at £0.9m"},
  {"id": "R05", "title": "Penetration test finds serious security flaws", "owner": "CISO", "l": 3, "i": 4, "prev": [3, 4], "mitigation": "Early test booked for 15 Jan"},
  {"id": "R09", "title": "Budget freeze in the first quarter", "owner": "CFO", "l": 2, "i": 5, "prev": [3, 5], "mitigation": "Funding confirmed to March by the Board"},
  {"id": "R16", "title": "Call centre training not complete by go-live", "owner": "Operations head", "l": 3, "i": 3, "prev": [3, 3], "mitigation": "Training plan agreed; pilot group trained"}]}
```

??? R07 went from 12 to 16 and R14 from 12 to 15, so they are the two new reds. R03 was already red at 16 and is now 20. R09 improved from 15 to 10 after the Board confirmed funding.

# The vendor delay has three mitigation options, and splitting the cutover by region is the best value
layout: columns
section: Risks
footnote: Residual score is the expected likelihood x impact after the option is in place. Cutover dates assume a decision by 25 November 2026.

```json
{"columns": [
 {"header": "A: Contractual recovery plan", "icon": "file-text", "bullets": ["Vendor adds two engineers at its own cost", "Weekly delivery checkpoint with penalty clauses", "Cutover date stays 22 March 2027", ["But the vendor has missed two plans already", 2], "Owner: A. Mensah"]},
 {"header": "B: Add a second migration partner", "icon": "users", "bullets": ["Second partner takes the three smallest product lines", "Needs 10 weeks to onboard", "Cutover date holds on a 22 March 2027 target", "Adds interface risk between two partners", "Owner: Commercial lead"]},
 {"header": "C: Split cutover by region", "icon": "git-branch", "bullets": ["North region cuts over 22 March 2027", "South region follows on 17 May 2027", "Vendor load halves in each wave", "Two sets of go-live support needed", "Owner: Delivery director"]}],
 "compare": [
  {"label": "Extra cost", "values": ["£0.4m", {"text": "£2.1m", "rag": "R"}, "£1.2m"]},
  {"label": "Last region live", "values": ["22 Mar 2027", "22 Mar 2027", {"text": "17 May 2027", "rag": "A"}]},
  {"label": "Residual score", "values": [{"text": "16", "rag": "R"}, {"text": "12", "rag": "A"}, {"text": "9", "rag": "A"}]}]}
```

??? Option C is our recommendation: it has the lowest residual score, though it delays the last region by eight weeks. Option A is cheapest but leaves the risk red.

# Funding the risks to P80 needs a budget of £54.0m, and today's £48.0m has only a 30% chance of holding
layout: p-curve
section: Exposure
footnote: Monte Carlo cost risk analysis, 5,000 iterations, risk register version 14 dated 30 October 2026. Base estimate £42.0m; correlation applied between migration and testing risks.

```json
{"exhibit": "Probability that programme cost is at or below", "unit": "£m, nominal, 2026 prices", "prefix": "£", "decimals": 1,
 "points": [[44, 0.0], [46, 0.1], [48, 0.3], [50, 0.47], [50.4, 0.5], [52, 0.65], [54, 0.8], [56, 0.91], [58, 0.97], [61, 1.0]],
 "percentiles": [50, 80], "budget": 48, "budget_label": "Current budget",
 "takeaways_title": "Implication",
 "takeaways": ["P50 is **£50.4m** and P80 is **£54.0m**, so P80 needs £6.0m more than today's budget.", "Migration delay and the test environment drive most of the spread."]}
```

??? The base estimate is 42.0 and the budget is 48.0, so the budget already holds 6.0 of contingency. The curve says that is a 30% confidence level.

# Seven issues and dependencies need action by January, and two issues are already red
layout: raid-log
section: Actions

```json
{"items": [
 {"type": "Issue", "id": "I04", "description": "Migration vendor has not delivered the second data mapping", "owner": "A. Mensah", "due": "20 Nov", "rag": "R", "status": "Escalated to vendor CEO on 4 Nov"},
 {"type": "Issue", "id": "I07", "description": "Test environment shared with payments team in Q1", "owner": "T. Okafor", "due": "30 Nov", "rag": "A", "status": "Second environment quote received"},
 {"type": "Issue", "id": "I09", "description": "Two integration architects resigned in October", "owner": "HR director", "due": "15 Nov", "rag": "R", "status": "Replacements interviewing"},
 {"type": "Dependency", "id": "D02", "description": "Regulator approval of claims process before May 2027 launch", "owner": "Compliance head", "due": "8 Dec", "rag": "A", "status": "Submission on track for 8 Dec"},
 {"type": "Dependency", "id": "D05", "description": "Payments team release freeze ends 10 January", "owner": "Delivery director", "due": "10 Jan", "rag": "A", "status": "Confirmed in writing"},
 {"type": "Dependency", "id": "D06", "description": "Legacy system support contract extended beyond March 2027", "owner": "CFO", "due": "31 Jan", "rag": "G", "status": "Draft extension with legal"},
 {"type": "Dependency", "id": "D08", "description": "Union consultation on call centre changes complete", "owner": "Operations head", "due": "15 Jan", "rag": "G", "status": "Consultation started 2 Nov"}]}
```

??? I04 and I09 are the two red issues; both fall due this month.

# We ask the Board for three decisions on the four red risks, costing £2.7m in total
layout: decisions
section: Actions

```json
{"decisions": [
 {"what": "Approve option C: split the data migration cutover by region", "recommendation": "Approve £1.2m from contingency; North live 22 March, South 17 May 2027", "owner": "Programme Board", "due": "25 Nov"},
 {"what": "Fund a retention bonus for the integration specialists", "recommendation": "Approve £0.6m for 12 named staff, paid in two instalments in 2027", "owner": "HR director", "due": "25 Nov"},
 {"what": "Buy a second test environment for Q1 2027", "recommendation": "Approve £0.9m; it removes the six-week test gap", "owner": "Delivery director", "due": "25 Nov"},
 {"what": "Re-run the risk analysis after these decisions", "recommendation": "Note. Report the P80 and the budget confidence at the December Board", "owner": "PMO lead", "due": "9 Dec"}]}
```

??? The three funded decisions are 1.2, 0.6 and 0.9, which is £2.7m.
