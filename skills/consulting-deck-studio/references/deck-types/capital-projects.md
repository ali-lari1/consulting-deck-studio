# Capital project deck types

Capital decks are read by sponsors, boards, funders and assurance bodies who know the difference between a P50 and a
P80. Show the estimate class, price base and confidence level beside every cost figure, and the baseline and data date
beside every date. Standards are in `references/standards.md`.

---

## 1. Investment decision / gate paper (business case)
**Purpose:** secure approval at a gate (Gateway 0-5, or the client's own capital policy). **Length:** 10-15 slides
plus a substantial appendix. **Read** as a pre-read, then discussed.

**Default sequence:**
1. `title`
2. `exec-summary`: the ask (the amount, the gate, the conditions), the case for it, the risks and the
   recommendation
3. `stage-gate`: where we are and what this gate decides
4. `columns`: strategic case (need, objectives, constraints)
5. Options: `options-matrix` (the long list → short list → preferred)
6. `waterfall`: the cost build-up or the change since the last gate, with the estimate class in the unit line
7. `p-curve`: the QRA, P50 and P80, and the budget's confidence level
8. `timeline` or `roadmap`: the delivery plan, with key gates
9. `columns`: commercial case (procurement route, risk allocation)
10. `benefits-tracker` or `key-numbers`: the economic case (BCR, NPV, benefits)
11. `risk-heatmap`: the top risks
12. `decisions`: the resolution wording

**Mandatory:**
- the amount requested
- the gate and framework
- the estimate class and accuracy range
- the price base (real or nominal) and VAT treatment
- P50 and P80, and which one the budget is set at
- contingency and management reserve shown separately
- the options considered, including do-minimum
- conditions from the previous gate, closed or open

**Ask about:** the framework and gate, the confidence policy, the funding source, what the approving body has pushed
back on before, and any conditions.

**Pitfalls:**
- a single-point estimate at Class 4-5
- optimism bias unadjusted or unstated
- the preferred option scored by the team that designed it, with no independent challenge

## 2. Independent project review (cost and schedule)
**Purpose:** an independent view of whether the project will be delivered for the forecast cost and date.

**Default sequence:**
1. `key-numbers`: the review's view of cost and date against the project's
2. `exec-summary`
3. `waterfall`: the project EAC → adjustments → the review's view
4. `gantt`: the project forecast against the review's view
5. `p-curve` (the review's QRA)
6. `table` of findings with severity
7. `columns`: recommendations
8. `decisions`

**Mandatory:** the scope, method and evidence; the documents reviewed and as-of dates; where the review disagrees
with the project and why; independence.

## 3. Cost-to-complete or estimate review
**Default sequence:**
1. `exec-summary`
2. `waterfall`: budget → committed → forecast to complete → EAC
3. `bar`: EAC by package or WBS against budget
4. `s-curve` (SPI, CPI and EAC are computed)
5. `line`: contingency drawdown against progress
6. `table` of estimate basis by package, with class and confidence
7. `tornado`: sensitivity
8. `decisions`

**Mandatory:** committed against uncommitted, claims and disputes (quantified or shown as excluded), and
escalation (inflation) assumptions.

**Pitfalls:** unquantified claims sitting silently outside the EAC, and SPI used to make time claims.

## 4. Quantitative risk analysis results (QRA, SRA)
**Default sequence:**
1. `key-numbers`: P50, P80 and the budget's confidence level
2. `p-curve` (cost)
3. `p-curve` (finish date), with dates as numbers, or a `table`
4. `tornado`: the top drivers
5. `risk-heatmap`: the risks behind the drivers
6. `columns`: contingency recommendation at the chosen confidence level
7. Appendix: model method, the correlation assumptions and the iteration count

**Mandatory:** the model method, iterations, the risk register version and date, and the treatment of correlation.

## 5. Delivery model and procurement strategy
**Default sequence:**
1. `exec-summary`
2. `columns`: models considered (design-bid-build, design-build, alliance, PPP, delivery partner)
3. `options-matrix`: weighted criteria, with risk transfer, market appetite, control, cost certainty and time
4. `table`: risk allocation, owner by risk category
5. `timeline`: the procurement programme
6. `decisions`

**Ask about:** market sounding results, the client's capability to manage the contract, and policy constraints.

## 6. Capital programme prioritisation (portfolio)
**Default sequence:**
1. `key-numbers` (the envelope, demand and the gap)
2. `scatter` (value against deliverability, with bubbles for cost)
3. `matrix-2x2` (strategic fit against readiness)
4. `bar`: a ranked list with the funding cut-off line
5. `roadmap`: phasing within the envelope
6. `decisions`

**Mandatory:** the prioritisation criteria and weights (agreed before scoring), the envelope by year, and committed
against uncommitted spend.

## 7. Recovery plan (troubled project)
**Default sequence:**
1. `exec-summary`: where we are, why, and the recovery ask
2. `driver-tree` or `waterfall`: what caused the overrun
3. `gantt`: re-forecast with float
4. `options-matrix`: recovery options
5. `roadmap` for recovery
6. `org-chart` or `raci`: governance changes
7. `risk-heatmap`
8. `decisions`

**Pitfalls:**
- a recovery date with no risk analysis
- root causes stated as symptoms ("productivity")
- no change to governance

## 8. Contingency and change control review
**Default sequence:**
1. `waterfall`: original budget → approved changes → current budget → EAC
2. `line`: contingency remaining against progress
3. `table`: change requests by status, value and authority
4. `columns`: risk realisation versus scope change
5. `decisions`

**Mandatory:** keep scope change (moves the baseline) separate from contingency drawdown (risk realised), and state
the approval authority thresholds.

## 9. Owner's representative or monthly project report
This is the status report from `pmo.md`, plus:
- a commercial section: claims, early warnings and compensation events, each with value and status
- a safety section (if in scope): incidents and leading indicators
- a design-maturity or consents tracker
Use `table` and `rag-dashboard`.

## 10. Benchmarking
**Default sequence:**
1. `benchmark`: unit cost against peers (the median is computed)
2. `scatter`: cost against size or complexity
3. `table`: normalisation (location, date, scope)
4. `columns`: what explains the gap

**Mandatory:** the peer set and how it was chosen, normalisation to a common price base and location, and data
sources and dates.

**Pitfalls:** comparing outturn against estimate, and unnormalised currencies or years.
