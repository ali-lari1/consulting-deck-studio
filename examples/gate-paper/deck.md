---
deck: Eastbrook Water Treatment Works Upgrade: Gate 3 investment decision
context: Calder Valley Water  |  Investment Committee  |  November 2026
tracker: Decision, Case, Cost, Risk
sticker: Draft for discussion
deck_type: gate-paper
source: Eastbrook project team, Class 3 estimate and QRA, October 2026. Fictional example.
---

# Eastbrook Water Treatment Works Upgrade: Gate 3 request for £194m
layout: title

```json
{"subtitle": "Investment decision paper for the Calder Valley Water Investment Committee",
 "client": "Calder Valley Water Investment Committee", "date": "12 November 2026", "prepared_by": "Eastbrook Project Team"}
```

# We ask the Committee to approve £194m for a new membrane plant, funded at P80 with all Gate 2 conditions closed
layout: exec-summary
section: Decision
footnote: P50 and P80 are the costs with a 50% and 80% chance of not being exceeded. Estimate is AACE Class 3 (accuracy -10% to +20%), 2026 Q3 prices, excluding recoverable VAT.

```json
{"points": [
 {"lead": "The ask", "support": ["Approve **£194m** at Gate 3, set at P80", "Includes £18m risk allowance and £12m management reserve, held separately"]},
 {"lead": "The case", "support": ["The 1974 works cannot meet the 2029 treatment standard", "Serves 214,000 customers; no spare capacity if a stream fails"]},
 {"lead": "The preferred option", "support": ["New membrane plant on the adjacent site scores **3.2 of 4**", "Rebuilding on the current site scores 2.6 and takes 14 months longer"]},
 {"lead": "The risks", "support": ["Ground conditions and membrane supply drive most of the uncertainty", "Without the extra £12m, the budget has only a 50% chance of holding"]},
 {"lead": "Gate 2 conditions", "support": ["Four of four closed: planning consent, land purchase, design freeze, supplier price check"]}]}
```

??? Lead with the ask. The Committee set P80 as the confidence policy in 2025, so £194m is P80 by design. All four Gate 2 conditions were signed off by the assurance panel in October.

# Eastbrook has passed three gates, and Gate 3 is the decision to release construction funding
layout: stage-gate
section: Decision
footnote: Gates follow the Calder Valley Water capital investment policy.

```json
{"gates": [
 {"label": "Gate 0", "name": "Strategic need", "date": "Mar 2024", "status": "done", "decision": "Approved"},
 {"label": "Gate 1", "name": "Options", "date": "Feb 2025", "status": "done", "decision": "Approved, £8m development"},
 {"label": "Gate 2", "name": "Concept design", "date": "Jun 2026", "status": "done", "decision": "Approved with 4 conditions"},
 {"label": "Gate 3", "name": "Investment decision", "date": "Nov 2026", "status": "current", "criteria": ["Class 3 estimate at P80", "Preferred option evidenced", "Gate 2 conditions closed", "Funding source confirmed", "Delivery plan with float"]},
 {"label": "Gate 4", "name": "Handover", "date": "Mar 2029", "status": "future", "criteria": ["Treatment standard met", "Operator trained"]}]}
```

??? Gate 3 releases the construction contract award. Gate 4 is operational handover in March 2029.

# The new membrane plant scores highest at 3.2 of 4, ahead of a rebuild on the current site
layout: options-matrix
section: Case
sowhat: We recommend Option C: build a new membrane plant on the adjacent site
footnote: Scores 0 (poor) to 4 (strong), set by the project team and challenged by the independent assurance panel on 22 September 2026. Scores are weighted by the percentages shown.

```json
{"stages": ["Long list (9)", "Short list (4)", "Evaluated", "Recommendation"], "stage": "Evaluated",
 "criteria": [{"name": "Meets 2029 treatment standard", "weight": "30%"}, {"name": "Whole-life cost", "weight": "25%"},
              {"name": "Deliverability", "weight": "20%"}, {"name": "Resilience", "weight": "15%"}, {"name": "Carbon", "weight": "10%"}],
 "options": [{"key": "A", "name": "Do minimum", "scores": [0, 4, 3, 0, 1]},
             {"key": "B", "name": "Refurbish existing works", "scores": [2, 2, 3, 1, 2]},
             {"key": "C", "name": "New membrane plant, adjacent site", "scores": [4, 3, 3, 3, 2]},
             {"key": "D", "name": "Rebuild on current site", "scores": [4, 1, 2, 3, 3]}],
 "recommended": "C",
 "rationale": ["Option A fails the 2029 standard and risks regulator enforcement", "Option C keeps the old works running during construction",
               "Option D matches C on resilience but needs a 14-month outage plan", ["Temporary supply would cost an extra £21m", 2],
               "Option B meets only part of the standard"]}
```

??? The panel changed two scores on Option B and none on Option C. Do minimum scores well on cost only because it avoids spend now.

# The £194m request builds up from £120m of works, with risk allowances added separately to reach P80
layout: waterfall
section: Cost
footnote: P50 = £182m after the £18m risk allowance. Management reserve of £12m takes the total to P80.
footnote: Contingency and management reserve are held by the Investment Committee, not the project.

```json
{"exhibit": "Cost build-up to the Gate 3 request", "unit": "£m, 2026 Q3 prices, excl. VAT, AACE Class 3 estimate (-10% / +20%)",
 "prefix": "£", "start": {"label": "Construction works", "value": 120},
 "steps": [{"label": "Preliminaries and site", "value": 16}, {"label": "Design and project management", "value": 21},
           {"label": "Land and consents", "value": 7}, {"label": "Risk allowance to P50", "value": 18},
           {"label": "Management reserve to P80", "value": 12}],
 "end": {"label": "Gate 3 request (P80)", "value": 194},
 "callouts": [3, 4],
 "takeaways_title": "What this shows",
 "takeaways": ["The base estimate is **£164m** before any risk allowance.", "Risk allowance of **£18m** takes the cost to P50, £182m.", "The extra **£12m** reserve lifts confidence from 50% to 80%."]}
```

??? 120 plus 16, 21 and 7 gives a base estimate of 164. Add 18 for P50 at 182, then 12 for P80 at 194. Optimism bias is already inside the risk allowance, not added again.

# At £194m the budget has an 80% chance of holding, against 50% at the £182m base case
layout: p-curve
section: Risk
footnote: Monte Carlo cost risk analysis, 5,000 iterations, risk register version 7 dated 9 October 2026, with correlation between ground and civils risks.

```json
{"exhibit": "Probability that outturn cost is at or below", "unit": "£m, 2026 Q3 prices, excl. VAT", "prefix": "£",
 "points": [[165, 0.0], [172, 0.05], [177, 0.25], [182, 0.5], [188, 0.68], [194, 0.8], [200, 0.9], [208, 0.97], [215, 1.0]],
 "percentiles": [50, 80], "budget": 194, "budget_label": "Requested budget (P80)",
 "takeaways_title": "Implication for Gate 3",
 "takeaways": ["Funding at P80 meets the Committee's confidence policy.", "The largest drivers are ground conditions and membrane supply lead times."]}
```

??? The curve is the output of the quantified risk analysis. If the Committee funded at P50 it would accept a one-in-two chance of returning for more money.

# We ask the Committee for three approvals and one note to protect the P80 funding
layout: decisions
section: Decision

```json
{"decisions": [
 {"what": "Approve £194m at P80 for Option C, released in two tranches", "recommendation": "Approve. Tranche 1 of £150m now; tranche 2 of £44m at construction contract award", "owner": "Investment Committee", "due": "12 Nov"},
 {"what": "Authorise award of the construction contract up to £136m", "recommendation": "Approve once the membrane supplier price check is repeated in January 2027", "owner": "Director of Capital Delivery", "due": "29 Jan"},
 {"what": "Hold the £12m management reserve centrally", "recommendation": "Approve. Release only by Committee decision, reported quarterly", "owner": "Chief Financial Officer", "due": "12 Nov"},
 {"what": "Note the Gate 4 criteria and the March 2029 handover date", "recommendation": "Note. Progress reported to the Committee each quarter against the P80 budget", "owner": "Director of Capital Delivery", "due": "Feb 27"}]}
```

??? The tranche split is 150 plus 44, which is 194. The £136m contract ceiling is construction works plus preliminaries, 120 plus 16.
