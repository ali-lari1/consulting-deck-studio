# PMO and capital-project standards (what reviewers expect)

Condensed from `research/craft-and-standards.md`, section 3, with sources. [V] = verified against the primary
document. [S] = secondary or practitioner source. [P] = convention to confirm with the client's own policy.

## RAG (no universal standard: define it in every deck)

| | Schedule [P] | Cost [P] | General |
|---|---|---|---|
| **Green** | Forecast within tolerance (e.g. under 2 weeks' slip on critical milestones) | EAC within ±5% of budget | On track; issues managed in the team |
| **Amber** | Slip above tolerance but recoverable (e.g. 2-6 weeks), with a recovery plan | EAC 5-10% over budget, mitigation identified | At risk; needs management attention |
| **Red** | Critical milestone or end date will be missed; no credible recovery | EAC more than 10% over, or contingency exhausted | Off track; escalation or a decision is needed |

- The emitters default to schedule RAG from slip: on plan green, up to 10 working days amber, more red. Replace this
  with the client's tolerances in `.cds/project.json`.
- **UK Delivery Confidence Assessment** [V]: NISTA (formerly IPA) now reports Red, Amber and Green; older reports used
  five levels. Use the client's scale.
- Every red or amber needs a cause, an impact, an action, an owner and a date. Show the trend against last period.

## Risk
- **Register fields:**
  - ID
  - cause → event → effect description
  - category
  - one owner
  - likelihood and impact (1-5) with defined anchors
  - inherent and residual score
  - response strategy (avoid, reduce, transfer, accept; exploit or enhance for opportunities)
  - actions with dates
  - trend
  - proximity
  - status
  - for capital projects, the quantified impact (minimum, most likely and maximum cost and days)
- **5×5 heat map:** score = L × I. The thresholds vary, so state them. The house default is red 15 or more, amber
  8-14, green 7 or less. Configure it with `red_from` and `amber_from`.
- **QRA (Monte Carlo)** [V, GAO-20-195G]: report P50 and P80. State which one the budget is set at, and keep
  management reserve separate. No single confidence level is "best practice". P80 portfolio-wide can be unaffordable.
  Use the `p-curve` layout, which computes the budget's confidence level.

## Schedule [V, GAO-16-89G]
- **Best practices:** all activities captured; logic-linked; resourced; durations set; traceable horizontally and
  vertically; a verifiable critical path; reasonable float; a schedule risk analysis; updated with actuals; a
  maintained baseline.
- **Exec Gantt:** 10-25 summary rows, baseline under forecast, milestones as diamonds, a today line, the critical path
  highlighted.
- **Report near-critical paths** (float under 10-15 working days) and the quality checks from
  `ingest.py`: open ends, negative float, float over 44 days, past forecasts not actualised.
- **Look-ahead:** 4-6 weeks for working level, 90 days for SteerCo.

## Cost and earned value
- **Show:** budget (BAC), commitments, actuals, estimate to complete, EAC (actuals + ETC), variance, contingency
  (opening, drawn, released, remaining) and management reserve. State the currency, price base (real or nominal) and
  VAT treatment.
- **EVM formulas** (ANSI/EIA-748; PMBOK): CV = EV − AC; SV = EV − PV; CPI = EV/AC; SPI = EV/PV; EAC = BAC/CPI;
  TCPI = (BAC − EV)/(BAC − AC). The `s-curve` layout computes these, with thresholds of 0.95 or more green, 0.90-0.95
  amber, below 0.90 red [P].
- **SPI is in cost terms.** Use the critical path or earned schedule for time conclusions.
- **Budget to EAC** is a `waterfall`. **Contingency drawdown** against progress is a `line`; flag when burn outpaces
  progress.

## Estimate classes [V, AACE 18R-97]

| Class | Definition | Accuracy (low / high) | Use |
|---|---|---|---|
| 5 | 0-2% | −20 to −50% / +30 to +100% | Concept screening |
| 4 | 1-15% | −15 to −30% / +20 to +50% | Feasibility |
| 3 | 10-40% | −10 to −20% / +10 to +30% | Budget authorisation |
| 2 | 30-75% | −5 to −15% / +5 to +20% | Control or bid check |
| 1 | 65-100% | −3 to −10% / +3 to +15% | Check estimate |

Show the class next to any capital cost. A single-point Class 5 number is a flagged failure.

## Gates and assurance
- **UK Gateway** [V] (GOV.UK toolkit, now NISTA): 0 Strategic assessment, 1 Business justification, 2 Delivery
  strategy, 3 Investment decision, 4 Readiness for service, 5 Operations review and benefits. International NISTA
  guidance uses gates 1-5, so don't assume the domestic numbering. Use the client's own capital policy where it has
  one.
- **IPA Inc. FEL Index** [V, vendor]: a proprietary front-end-loading score. Cite the score, but don't reproduce its
  weights.
- **IV&V and health checks:** the finding → rating → recommendation → management response structure. Rate per
  criterion or area, and report movement since the last review.
- **PRINCE2 Highlight Report** [S]: status against time, cost, quality, scope, benefits and risk; products; change
  requests; key risks and issues.

## Change control
- **Fields:** ID, requester, description, reason, options, and impact on scope, cost, schedule, risk and benefits;
  then recommendation, approval authority (by threshold), decision and baseline updated (yes or no).
- **Keep scope change** (which moves the baseline) **separate from risk realisation** (which draws contingency).

## Benefits
- **Register fields:** benefit, type (cashable or not), KPI, baseline, target, owner (a business owner, not the PM),
  realisation date, status and dis-benefits.
- **Report** what has been realised to date, the forecast and what is at risk. Tie benefits to the business case and
  the post-implementation review. The `benefits-tracker` layout computes progress.
