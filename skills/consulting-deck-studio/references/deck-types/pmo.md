# PMO deck types

Inputs usually available are the schedule (`.xer` or MS Project `.xml`), registers (risk, RAID, benefits, change,
cost), last period's deck, SteerCo or board transcripts and action logs. Ingest them first (`references/ingest.md`)
and link the project for recurring reports.

The **mandatory** lists below are the minimum a SteerCo chair or programme director expects. Where a mandatory item
is missing from the inputs, show a `[[placeholder]]` and ask; never drop it silently.

---

## 1. Monthly or weekly status report
**Purpose:** tell the governance forum where the programme stands against plan, what changed, and what it must
decide. **Length:** 6-10 slides plus appendix. **Usually** a pre-read, presented for 15-20 minutes.

**Default sequence:**
1. `title`
2. `status-summary`: rows for schedule, cost, risk, benefits and stakeholders, each with RAG, trend and text; a
   decisions panel; the look-ahead pulled in with `data_from: … as lookahead`
3. `table` or `timeline`: what changed since last period (from `ingest.py --diff`) and milestones achieved
4. `gantt` (from emit) with takeaways and next steps
5. `risk-heatmap` (with `prev` from the snapshot)
6. `waterfall` (budget to EAC) or `s-curve` if earned value is tracked
7. `rag-dashboard`: one row per workstream
8. `decisions`
9. Appendix: `raid-log`, the full milestone `table`, RAG definitions

**Mandatory:**
- overall RAG with a rationale
- RAG by dimension, with the trend
- decisions needed, each with an owner and a date
- milestones, baseline against forecast
- budget, actuals and EAC
- the top 5-10 risks with score and trend
- the look-ahead
- the as-of date and sources
- RAG definitions

**Ask about:** the RAG policy and tolerances (once), the current baseline, escalations, and achievements not in the
files.

**Pitfalls:**
- "Watermelon" greens that contradict the schedule data
- an achievements list with no "so what"
- the decisions slide buried at the back
- a new period's numbers mixed with old commentary
- risks rescored without saying so

## 2. SteerCo or programme board pack
**Purpose:** get decisions. **Length:** 8-15 main slides. **Order:** decisions first (`references/storyline.md`).

**Default sequence:**
1. `title`
2. `agenda`: each item labelled Decide, Discuss or Note
3. `decisions` (yes, up front)
4. `status-summary`
5. One slide per escalation (an issue, a risk, or a change request with its options), as an `options-matrix` or
   `columns` with `compare`, plus the recommendation
6. Look-ahead (`timeline` or `table`)
7. Financials (`waterfall`)
8. Appendix

**Mandatory:** every decision with options, a recommendation, the impact (cost, time, risk) and the cost of not
deciding. Actions from the last meeting closed off (a `table` with RAG).

**Pitfalls:** decisions phrased as updates ("Contingency position") rather than asks ("Approve £14m…"), and
options without a recommendation.

## 3. Programme or portfolio dashboard
**Purpose:** compare many projects on one page. **Layouts:**
- `rag-dashboard`, with KPIs such as projects red, value at risk and forecast against budget
- `scatter` (SPI against CPI, with bubbles for budget)
- `table`, one row per project, with RAG columns and trend

**Mandatory:** a consistent RAG basis across projects, the data date for each project, and the trend.

**Pitfalls:** mixed data dates, and different RAG rules in different projects.

## 4. Risk review (RAID deep-dive)
**Purpose:** make the risk position and its movement clear, and get owners to commit to funded mitigations.

**Default sequence:**
1. `key-numbers`: open risks, red risks, quantified exposure, and new this period
2. `risk-heatmap` with `prev`
3. One slide per red risk: cause → event → effect, the mitigation options as `columns` with `compare`, the owner
   and the cost
4. `p-curve` or `tornado` if a QRA exists
5. `raid-log` (issues and dependencies)
6. `decisions`

**Mandatory:** the scoring scale and thresholds, inherent against residual where the client uses it, single owners
and dated actions.

**Pitfalls:**
- vague risks ("supply chain risk") with no cause or effect
- every risk amber
- mitigation that is really "monitor"

## 5. Schedule review or recovery plan
**Purpose:** explain the slip, the critical path and the credible recovery.

**Default sequence:**
1. `exec-summary`
2. `gantt` (baseline against forecast, float, the milestone moves)
3. `table` of driving activities with their float
4. `p-curve` from the schedule risk analysis (finish-date confidence)
5. Recovery options as an `options-matrix`
6. `roadmap` for the recovery plan
7. `decisions`

**Mandatory:** the baseline source and date, the critical path, near-critical paths, the schedule quality checks
(from ingest), and the confidence level of any new date.

**Pitfalls:** a new date with no risk analysis, and float consumed silently.

## 6. PMO set-up or mobilisation
**Purpose:** agree governance, cadence, tools and roles for a new programme.

**Default sequence:**
1. `exec-summary`
2. `org-chart` (the governance forums)
3. `raci` (decisions and owners, exactly one A per row)
4. `process-flow` (reporting cycle: data cut → validation → pack → SteerCo)
5. `table` (meeting cadence: forum, chair, frequency, inputs, decisions)
6. `columns` (RAG definitions, tolerances, escalation thresholds)
7. `roadmap` (the first 90 days)

**Mandatory:** escalation thresholds for time, cost and scope; who owns the baseline; change authority levels.

## 7. Go-live or readiness review
**Purpose:** go or no-go, with criteria.

**Default sequence:**
1. `exec-summary` (the recommendation: go, go with conditions, or no-go)
2. `table` of readiness criteria, each with RAG and evidence
3. `risk-heatmap` of cutover risks
4. `timeline` for the cutover plan
5. `columns`: the conditions and the rollback plan
6. `decisions`

**Mandatory:** the criteria agreed in advance, evidence per criterion, the rollback trigger and owner, and
hypercare.

## 8. Assurance, health check or IV&V report
**Purpose:** an independent view of delivery confidence.

**Default sequence:**
1. `key-numbers` (overall rating, findings by severity)
2. `table` of ratings by area, with movement since last review
3. One `columns` slide per significant finding: observation → impact → recommendation → management response
4. `table` tracking previous recommendations
5. `decisions`

**Mandatory:** the scope and method of the review, the rating scale, the evidence base (interviews, documents), and
independence statements where relevant.

**Pitfalls:** findings without evidence, and recommendations without owners or dates.

## 9. Benefits review
**Default sequence:**
1. `benefits-tracker`
2. `line` (benefits profile: planned against realised)
3. `table` of dis-benefits and dependencies
4. `decisions`

**Mandatory:** a business owner per benefit, the baseline and the measurement start date.

## 10. Close-out and lessons learned
**Default sequence:**
1. `key-numbers` (final cost against budget, time against plan, benefits)
2. `waterfall` (budget to outturn)
3. `before-after` or `columns`: what worked, what didn't, and what to repeat
4. `table` of lessons, each with the owner of the change
5. Handover `raci`

**Pitfalls:** lessons phrased as complaints, with nothing to change.
