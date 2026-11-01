# Consulting deck craft and PMO/capital-project standards: reference for the deck skill

Provenance and verification (access date 2026-11-01): standards sections were verified against primary documents fetched this session (NISTA/IPA Gateway guidance, GAO-16-89G, GAO-20-195G, AACE 18R-97 text, IPA annual report 2015-16, GOV.UK style guide, Wikipedia Signs of AI writing, Economist style guide text). Items tagged [V] are verified against a primary or official source. Items tagged [S] rest on secondary sources (consulting-training blogs, unofficial wikis) and need client or firm confirmation. Items tagged [P] are practitioner convention with no published standard (e.g. RAG percentage thresholds, CPI bands, 5x5 banding). Consulting house-style claims are [S]: no McKinsey, BCG or Bain publication was found that states them.

---

## 1. Consulting slide craft

### 1.1 Core frameworks
| Concept | Rule for the skill |
|---|---|
| Pyramid Principle (Minto) | Lead with the answer. Group supporting points under it, usually 3 (2-5). Each group is one idea, and the group sits one level of abstraction above its members. Order each group by time, structure or importance, never arbitrarily. |
| Vertical logic | Each point answers "why?" or "how do you know?" from the level above. The reader can stop at any depth. |
| Horizontal logic | Points at one level form a deductive chain or an inductive set of like items. |
| SCQA / SCR | Situation (uncontested), Complication (change or tension), Question (implied), Answer (the governing thought). Use it for the exec summary and the opening of each section. Keep S and C to 1-2 sentences each. |
| MECE | Categories must not overlap and must cover the whole. Test with: could one item sit in two boxes? What is missing? A "catch-all other" bucket over about 10% signals a broken cut. |
| Governing thought | One sentence that answers the client's question, including the decision or action asked for. Everything in the deck traces to it. |

Source notes for 1.1 [V/S]: Wikipedia (MECE) attributes MECE to Barbara Minto at McKinsey in the late 1960s and records the critique that forcing a MECE cut can exclude useful overlap and does not filter out irrelevant items. A consulting-prep article (Leland) states the pyramid as answer first, three layers, a summary at every level, ordering by time, structure or degree, and MECE support, reasoned inductively or deductively. A search summary of Minto-derived material describes the vertical relationship as each level answering the question the level above raises, and the horizontal relationship as peers belonging to one kind of idea. SCQA wording was not confirmed in a primary Minto source, so treat the SCQA steps as practitioner convention [S].

### 1.2 Action titles
- Write a full-sentence takeaway: subject, verb, "so what". Not a topic label ("Cost overview" becomes "Forecast cost has risen 8% since baseline, driven by two scope changes").
- Length [S]: published training sources agree on a full-sentence takeaway of at most two lines, and one vendor guide suggests under about 15 words. Treat 15-25 words as a working band and two lines as the hard cap, at 20-24pt. Over 2 lines usually means two messages, so split the slide.
- Include the number or the comparison that proves the claim. Put the conclusion before the evidence.
- The title must be falsifiable by the body. If the body cannot prove it, change the title or the body.
- Parallel phrasing across titles in a section makes the story scannable.
- Avoid: question titles (except in working sessions), "Overview", "Update", "Introduction", gerund fragments ("Understanding…"), and titles ending in a colon.

### 1.3 Horizontal and vertical logic as tests
- Horizontal test: copy all titles into a list. A reader who sees only that list should get the full storyline, with no gaps and no repeated points. Make the skill output this list as a QA artefact.
- Vertical test: for each slide, ask whether the body (chart, table, bullets) proves exactly the title. Anything that does not support the title is cut or moved to the appendix.
- Ghost deck (storyboard): write all titles first, then sketch the empty exhibit type per slide (chart type, axes, expected "shape"), then fill with data. Review the ghost deck with the client lead before building. Tag each ghost slide with the hypothesis and the data needed. This is hypothesis-driven working (answer-first, then prove or disprove).

### 1.4 Executive summary formats
- Dot-dash: dot = key message in a full sentence; dashes = 2-4 supporting facts under it. Dots read alone as the executive summary.
- SCQA paragraph for decision memos: S, C, Q (often implicit), A, then the "ask".
- Place it at slide 2-3. Put the decision requested at the top, not the bottom.
- Keep it to one page of about 150-200 words. It mirrors the section titles one-to-one.

### 1.5 Navigation
- Tracker (section marker) at top-left or top-right: small tag or breadcrumb showing the current section, optionally with all sections and the current one highlighted. It is mandatory on decks longer than about 10 slides.
- Agenda slide reused as a section divider, with the current section highlighted.
- Page numbers on every content slide. Needed for steerco discussion ("go to page 14").

### 1.6 Slide anatomy (top to bottom)
1. Tracker or section tag
2. Action title (1-2 lines)
3. Subtitle or lead-in: units, scope, "as of" date (e.g. "Forecast cost, GBPm, as of 30 Sep")
4. Body: one exhibit or one structured layout, with callouts that point at the insight
5. Takeaway box ("so what" or "implication") for decision slides, optional elsewhere. Do not duplicate the title.
6. Source and notes line, bottom-left, small (8-9pt): "Source: ...; Note: ..." plus the analysis owner if internal
7. Page number, plus confidentiality marker or footer

### 1.7 Sourcing and footnotes
- Every number is sourced: document or system, date or version, owner. Use the format "Source: [system/doc], [date]; [team] analysis".
- Mark estimates, forecasts and assumptions explicitly. Distinguish actuals from forecast in the lead-in.
- Footnotes use numbered or lettered markers and are placed above the source line. Keep definitions (e.g. "RAG status per Appendix X") there, not in the body.
- Unsourced or "illustrative" data must say so on the slide ("Illustrative"). Never leave placeholder numbers that look real.

### 1.8 One message per slide and density
- One message per slide. Two "and" clauses in the title means two slides.
- Density norms: consulting decks are denser than keynote slides. A working or pre-read slide can carry 80-150 words. A presented slide carries 30-60 words. Use a minimum 10-12pt body, with 14pt+ where possible. Never shrink text below 10pt to fit.
- Rule of thumb: max 3-5 bullets per box, max 2 levels, max about 6 data series per chart, one highlighted colour for the key datum and grey for context.

### 1.9 Chart selection
| Need | Use | Avoid |
|---|---|---|
| Compare categories | Horizontal bar (long labels) or column (few categories, ordered) | 3D, pie with more than 4 slices |
| Trend over time (continuous) | Line (up to about 5 lines); column if discrete periods and few points | Dual axes without labelling |
| Bridge or variance (budget to EAC, baseline to forecast) | Waterfall (walk) with start, steps, end totals; sort steps by size or logic | Stacked bars with tiny deltas |
| Composition at one point | 100% stacked bar, or pie/donut only for 2-4 parts | Pie with more than 5 parts |
| Composition over time | Stacked column; area only for continuous totals | More than 5-6 stacks |
| Two dimensions, size matters (market share vs segment size) | Marimekko (variable width and height) | Using it for simple comparisons |
| Correlation and positioning | Scatter or bubble; label outliers only | Labelling every point |
| Prioritisation | 2x2 matrix (label axes with low/high plus criteria, name each quadrant, place items by evidence) | Quadrants with no stated axes scale |
| Qualitative assessment grid | Harvey balls (0/25/50/75/100%) in a criteria x options table, with a legend and a defined scale | Harvey balls without a defined rubric |
| Schedule | Gantt, milestone tracker | Gantt of over about 25 rows on one page |
| Flows and processes | Chevron or swimlane | Unconnected boxes |
- Always: sort bars, show units, direct-label rather than legends where possible, axes start at zero for bars, mark CAGR or delta with an arrow callout, cut gridlines.

### 1.10 House-style differences [S] (no firm publishes these rules; the training sources in the Sources list are vendors and bloggers, so treat as tendencies)
| Trait | McKinsey | BCG | Bain |
|---|---|---|---|
| Title | Longer action titles, 2 lines, "so what" first | Action titles, often with a short section tag above | Answer-first, concise titles; "results" orientation |
| Structure | Strict Pyramid, MECE, issue trees, SCQA exec summary | Insight-led, strong on frameworks (growth-share matrix, 2x2s) | Hypothesis-driven, "Answer First", emphasis on quantified results |
| Look | White space, restrained palette, simple charts, a takeaway box or sticker | Green palette, a visible "so what" or insight box | Red accent, often dense, text-heavy tables acceptable |
| Footer | Source/notes, page number | Source, page number | Source, page number |
Do not hard-code a firm identity. Offer a neutral house style and a theme switch (palette, title length, takeaway box on or off). Client branding overrides.

### 1.11 Common failure modes reviewers flag
- Topic titles, or titles that do not match the body (title says X, chart shows Y).
- Several messages on one slide; "kitchen-sink" slides.
- Chart and title mismatch; axis not starting at zero; truncated axes; missing units; missing "as of" date.
- Numbers on different slides that do not reconcile (total versus sum of parts; same metric with different values).
- Unsourced data, "TBC" or placeholder values that survive to the final.
- Decoration over information (3D, gradients, clip art, rainbow palettes).
- Wall-of-text, font under 10pt, inconsistent alignment, margins and spacing.
- Executive summary that repeats the agenda rather than stating the answer.
- Recommendation buried at the end; no clear "ask" or decision.
- Jargon and acronyms undefined; "synergies", "leverage", "holistic".
- No next steps with owner and date.
- RAG statuses with no rationale or threshold; every item green until the last week ("watermelon" reporting: green outside, red inside).

---

## 2. Flow between slides

- So-what chaining: each title builds on the previous. Check that slide N+1 title answers the question the slide N title raises. Use connective logic in titles ("Because…, therefore…", "However…", "As a result…") sparingly.
- Transitions without filler: use the section divider plus a one-sentence bridge (the divider carries the section's key message, not just its name).
- Section structure: executive summary → context and scope → findings by section (each opens with a one-slide section summary) → recommendation → implementation, risks, next steps → decision requested → appendix.
- Repeat the agenda with the current section highlighted at each section start.
- Deductive (argument chain) when the audience is neutral or supportive; inductive (grouped evidence) when the conclusion may be resisted; keep the answer first in both for senior audiences.
- Appendix logic: backup that supports but does not carry the story: methodology, detailed data tables, assumptions, full registers, definitions (RAG, scoring scale), alternative scenarios. Reference each from the main slide ("see Appendix B, p.32"). Appendix slides have action titles too.
- Pre-read vs presented:
| Attribute | Pre-read / reading deck | Presented / SteerCo deck |
|---|---|---|
| Density | High: 80-150 words, self-explanatory | Lower: 30-60 words, speaker adds context |
| Slides | Can be longer (20-40) | 8-15 main slides plus appendix |
| Titles | Full story in titles and callouts | Full story in titles, with the verbal narrative |
| Decisions | Stated explicitly on the slide | Called out on a decision slide, timed in the agenda |
- SteerCo deck: decisions first. Typical order: decisions needed (top), overall status and RAG, achievements since last period, key issues and risks needing escalation, look-ahead, financials, then detail in the appendix. Aim for 30-60 min. Each agenda item is labelled Decide / Discuss / Note.
- Working session deck: more questions as titles, options laid out, space to annotate, less polish, lots of "strawman" labels; outputs are captured as decisions and actions.
- Close with decisions requested, owner, and date. Nothing new appears on the final slide.

---

## 3. PMO and capital-project artefact standards

### 3.1 Status report / programme dashboard: required content
- Header: programme name, reporting period, "as of" date, author, version, distribution.
- Overall RAG with one-line rationale, plus RAG by dimension (schedule, cost, scope/quality, risk, resources, benefits, stakeholders). Show trend arrow versus last period.
- Executive summary: 3-5 sentences, covering what changed, what is at risk, what is needed.
- Progress since last period (accomplishments) and next-period look-ahead (typically 4-6 weeks, or 90 days for SteerCo).
- Milestone tracker: baseline date, forecast date, variance (days), status.
- Critical path / key dependencies: top driving path and near-critical, with float.
- Cost: approved budget, actuals to date, forecast (EAC), variance, contingency (opening, drawn, remaining).
- Top risks and issues (top 5-10), decisions needed (with owner and due date), change requests pending.
- Resources, benefits (where tracked), and next steps.
- Appendix: full registers (RAID: risks, assumptions, issues, dependencies), decision log, change log.

### 3.2 RAG definitions
No universal standard. Define explicitly in the deck footnote or appendix and keep it consistent. Typical thresholds [P] (no published standard; the percentages below are conventions to confirm with the client PMO policy):
| Status | Schedule | Cost | General |
|---|---|---|---|
| Green | On track; forecast within tolerance (e.g. under 5% / under 2 weeks slip on critical milestones) | EAC within +/-5% (or inside tolerance) of budget | Delivery on track; issues managed in team |
| Amber | Forecast slip above tolerance but recoverable (e.g. 5-15% or 2-6 weeks), recovery plan in place | EAC 5-10% above budget, mitigation identified | At risk; management attention needed |
| Red | Critical-path milestone or end date will be missed; no credible recovery (above e.g. 15% or 6+ weeks) | EAC over 10% above budget or contingency exhausted | Off track; escalation or decision required |
- UK Delivery Confidence Assessment (DCA) [V]: the likelihood of delivery to time, cost and quality. Historic IPA annual reports (e.g. 2015-16) used five levels: Green, Amber/Green, Amber, Amber/Red, Red. The current NISTA reports (2024-25, 2025-26) describe three groups, Red, Amber and Green, with a separate 'Reset' label in 2024-25 for a significant baseline change. NISTA's gateway guidance for international use defines Green as delivery highly likely with no major outstanding risks, Amber as feasible but with significant issues that look resolvable if addressed promptly, and Red as appearing unachievable with major issues that look unmanageable at this stage (re-baselining or viability reassessment may be needed). It also rates time, cost and quality separately: Amber time means behind schedule with a realistic recovery plan; Red means likely late and re-baselining likely. Offer 3-level as the default and 5-level only if the client already uses it.
- Rules: RAG is a judgement against tolerance, not a mood. A red or amber must carry cause, impact, action, owner, date. Avoid "grey" unless "not started / not assessed".

### 3.3 Risk register fields
| Field | Notes | Mandatory? |
|---|---|---|
| ID | Unique, stable | Always |
| Title / description in cause-event-effect form: "Because of [cause], [event] may occur, resulting in [effect on objective]" | Avoids vague statements like "supply chain risk" | Always |
| Category / WBS / objective affected | Cost, schedule, quality, safety, reputation | Always on the full register |
| Owner (single named person) and action owner | | Always |
| Likelihood (1-5) and Impact (1-5) | Define scale anchors in £ and days; score = L x I (1-25) | Always |
| Inherent score (before controls) and residual (after planned responses) | PRINCE2 and ISO 31000 style | Full register; on the dashboard show current score only |
| Response strategy | Avoid / reduce (mitigate) / transfer / accept / exploit (opportunity) / enhance / share | Always |
| Mitigation actions with due dates and status | | Always |
| Trend | Rising / stable / falling vs last period | Dashboard and full register |
| Proximity / date | When the risk could occur | Recommended |
| Quantified impact: cost (min / most likely / max), schedule days; probability % | Feeds QRA | Capital projects (Class 3 and above estimates) |
| Status | Open / closed / occurred; if it occurred, move to the issues log | Always |
| Secondary risks, contingency allocation | | Capital projects |
- 5x5 heat map: thresholds commonly Low 1-4 (green), Medium 5-9 (amber), High 10-16 (orange), Critical 17-25 (red). Define explicitly [P] (confirm against the client risk policy).
- Quantified risk analysis: Monte Carlo on cost and schedule produces a distribution. P50 = 50% chance of not being exceeded; P80 = 80%. GAO-20-195G [V] says no specific confidence level is a best practice. Budgeting to the mean of the cost S-curve is common, while a high-risk programme may adopt 70 or 80 percent to cover risks unknown at the time and reduce the chance of re-baselining. It also warns that funding every project in a portfolio at P80 can make the portfolio unaffordable. Contingency amount follows the confidence level management chooses. Report both P50 and P80, state which one the budget is set at, and keep management reserve separate. GAO-16-89G [V] requires a schedule risk analysis to set schedule contingency and identify high-priority risks.

### 3.4 Issues, actions, decisions logs
- Issue log: ID, description, impact, owner, severity or priority, raised date, target date, status, escalation level.
- Action log: ID, action, owner, due date, status, source meeting.
- Decision log: ID, decision, date, decision-maker (forum), rationale, alternatives rejected, implications, status.
- Change log: see 3.8.
- Assumptions and dependencies logs (RAID = Risks, Assumptions, Issues, Dependencies).

### 3.5 Schedule conventions
- Gantt: summary level for exec decks (10-25 rows), with milestones as diamonds, a "today" line, baseline bar under the forecast bar, critical path highlighted, dependencies shown only for key links.
- Milestone tracker: milestone, baseline date, forecast/actual date, variance, owner, status (RAG).
- Baseline versus forecast: always show both. Never overwrite the baseline. Variance in days or weeks. Label approved re-baselines with the change reference.
- Float: total float (slack before the project end date is delayed) and free float; critical path = longest path / zero or negative float. Report near-critical paths (e.g. float under 10-15 working days). GAO Schedule Assessment Guide requires logic-linked activities, a verifiable critical path, reasonable float, resource-loading and a schedule risk analysis.
- Look-ahead: 4-6 week (working level) and 3-month (SteerCo).
- Schedule quality checks: open ends, constraints, negative float, out-of-sequence progress (DCMA 14-point style).

### 3.6 Cost conventions
- Show: Approved budget (BAC or sanctioned), commitments, actuals to date, forecast to complete (ETC), EAC (= actuals + ETC), variance (budget - EAC), contingency (opening, drawn, released, remaining), and management reserve.
- Budget to EAC bridge as a waterfall.
- Contingency drawdown: plot remaining contingency against percent complete or time. Flag if the burn rate exceeds the progress rate.
- S-curve: cumulative planned (PV) versus actual (AC) versus earned (EV) over time, with forecast to completion dashed.
- EVM (ANSI/EIA-748; PMBOK): CV = EV - AC; SV = EV - PV; CPI = EV / AC; SPI = EV / PV; EAC (typical) = BAC / CPI; TCPI = (BAC - EV) / (BAC - AC). CPI/SPI below 1.0 are adverse; common thresholds: 0.95-1.05 green, 0.90-0.95 amber, under 0.90 red [P]. SPI measured in cost terms, so also use earned schedule or the critical path for time conclusions.
- Currency, price base (real / nominal), VAT/tax treatment and FX assumptions must be stated.
- AACE International estimate classes (RP 18R-97, process industries; peers for other industries):
| Class | Maturity (project definition) | Typical accuracy range (low / high) | Typical use |
|---|---|---|---|
| 5 | 0-2% | -20% to -50% / +30% to +100% | Concept screening |
| 4 | 1-15% | -15% to -30% / +20% to +50% | Study, feasibility |
| 3 | 10-40% | -10% to -20% / +10% to +30% | Budget authorisation, control |
| 2 | 30-75% | -5% to -15% / +5% to +20% | Control, bid check |
| 1 | 65-100% | -3% to -10% / +3% to +15% | Check estimate, bid |
Show the estimate class beside any capital cost figure, since a Class 5 number with a single-point value is a flagged failure mode.

### 3.7 Stage gate and assurance frameworks
| Framework | What to use it for in a deck |
|---|---|
| UK Gateway Reviews (NISTA, which now holds the former IPA assurance toolkit) [V] | Six gates on the GOV.UK toolkit: Gate 0 Strategic assessment (programme level); Gate 1 Business justification; Gate 2 Delivery strategy (before commitments to suppliers); Gate 3 Investment decision; Gate 4 Readiness for service; Gate 5 Operations review and benefit realisation. Toolkit guidance is dated 20 Aug 2026 (earlier IPA versions 15 Jul 2021). The NISTA guidance for international use has five gates (1 to 5) aligned to early, intermediate and full business cases, so do not assume the domestic 0-5 numbering in non-UK work. Show the current gate, the last DCA colour, and recommendation status. |
| IPA (Independent Project Analysis, Inc.) FEL Index [V, vendor source] | Front-end loading is the work of defining a capital project before sanction. IPA's FEL Index scores overall project definition and three components (site factors, engineering status, execution planning) against industry benchmarks, built from data on over 10,000 site and sustaining capital projects. IPA reports that better definition goes with better cost and schedule outcomes and that the average index fell into its 'Poor' range recently. The index is proprietary, so a deck can cite the score but should not reproduce its scoring weights. The earlier 'FEL 1/2/3' stage labels are common industry usage, not an IPA index definition. Not the UK Infrastructure and Projects Authority. |
| GAO Cost Estimating and Assessment Guide, GAO-20-195G (12 Mar 2020) [V] | Four characteristics of a high-quality estimate: comprehensive, well documented, accurate, credible. It sets out a twelve-step process (Table 3 of the guide) with sensitivity, risk and uncertainty analysis. Use as an audit checklist. |
| GAO Schedule Assessment Guide, GAO-16-89G (published 22 Dec 2015) [V] | Ten best practices: capture all activities; sequence them; assign resources; set durations; verify horizontal and vertical traceability; confirm the critical path; keep total float reasonable; run a schedule risk analysis; update with actual progress and logic; maintain a baseline. They map to four characteristics: comprehensive, well-constructed, credible, controlled. |
| PMI PMBOK Guide [V for counts, domain names from memory] | 7th edition: 12 principles and 8 performance domains. PMI now also publishes an 8th edition that PMI's standards page describes as having six principles and seven performance domains, so confirm which edition the client uses. Domain names recalled for 7th (Stakeholder, Team, Development approach and life cycle, Planning, Project work, Delivery, Measurement, Uncertainty) were not re-fetched [S]. Quantified risk techniques in the PMI risk practice standard include Monte Carlo simulation and sensitivity analysis [S, unofficial copies only]. |
| PRINCE2 7 (PeopleCert; launched Sept 2023) [S] | Official manual text was not accessible. From the unofficial prince2.wiki: the Highlight Report is a one-page board update covering reporting period, status against six variables (time, cost, quality, scope, benefits, risk), current and next products, change requests, and key risks and issues. PRINCE2 7 folds registers into a Project Log (daily log, issue, lessons, quality, risk and product registers). Field lists for the risk register were not available, so use the Risk register fields in 3.3 and confirm against the manual. |
| HM Treasury Orange Book (May 2023 edition; first published 2013) [V for date, S for content] | Government risk management guidance. The GOV.UK page confirms edition and date but not content. Secondary sources describe five principles, the inherent versus residual distinction, and risk appetite with escalation triggers. Use 'inherent' and 'residual' scoring and an appetite statement for UK public sector clients. |
| MoR (Management of Risk, AXELOS/PeopleCert) | Not retrieved. Treat as a PRINCE2-aligned alternative and ask the client which risk framework applies. |

### 3.8 Change control
- Change request fields: ID, title, requester, date, description, reason, options considered, impact on scope, cost, schedule, risk, benefits, quality, recommendation, approval authority (by threshold), decision, date, baseline updated (Y/N), reference.
- Approval thresholds are tiered (e.g. PM up to X, SteerCo/Board above). State these on the change slide.
- Dashboard view: counts (raised, approved, rejected, pending), cumulative cost and schedule impact of approved changes, and trend. Show a change waterfall from original to current budget.
- Change versus contingency drawdown: distinguish scope change (changes baseline) from risk realisation (uses contingency).

### 3.9 Benefits realisation
- Benefits register: ID, benefit, type (financial/non-financial, cashable/non-cashable), KPI and measure, baseline, target, owner (a business owner, not the PM), realisation date, status, dependencies, dis-benefits.
- Benefits profile: planned vs forecast vs realised over time. Report as "realised to date, forecast, at risk".
- Tie benefits to the business case and the Gate 5 / post-implementation review.
- Often forgotten: benefits owner sign-off, measurement start date, and what happens after programme closure.

### 3.10 Mandatory fields by deck type
| Element | Weekly/monthly status report | SteerCo / Board deck | Risk review | Capital project sanction / gate paper | Cost/schedule deep-dive | PMO portfolio dashboard |
|---|---|---|---|---|---|---|
| Overall RAG + rationale | M | M | R | M | R | M (per project) |
| RAG by dimension + trend | M | M | O | M | R | M |
| Decisions needed (owner, date) | M | M (first page) | M | M (the approval ask) | O | R |
| Milestones baseline vs forecast | M | M (key) | O | M | M | M |
| Critical path / float | R | R | O | M | M | O |
| Budget / actual / EAC / variance | M | M | O | M | M | M |
| Contingency drawdown | R | M (capital) | R | M | M | O |
| EVM CPI/SPI | O | R (large) | O | R | M | R |
| Estimate class + P50/P80 | O | M (capital) | R | M | M | O |
| Top risks (5-10) with score + trend | M | M | M (full) | M | R | R |
| Issues, actions, decisions logs | M (top lines) | R | M (issues linked) | O | O | O |
| Change requests pending | R | M | O | R | R | O |
| Benefits | R | M | O | M | O | M |
| Gate / assurance status | R | M | O | M | O | R |
| Look-ahead | M | M | O | R | O | O |
| "As of" date, source, version | M | M | M | M | M | M |
M = mandatory, R = recommended, O = optional.

---

## 4. Humanised copy for consulting

### 4.1 Principles (verified against the named guides)
- GOV.UK style guide [V]: use plain English; keep sentences to about 25 words or fewer; prefer active voice; use 'use' not 'utilise' or 'leverage'; avoid 'deliver' for abstract things; avoid 'drive' for people or schemes; drop 'in order to' and 'going forward'; avoid metaphors; sentence case for titles; 'to' for ranges instead of dashes; avoid semicolons; do not use bold or italics for emphasis; explain abbreviations on first use; avoid 'please' unless needed; numerals for numbers in most contexts; bullets need a lead-in line and at least two items.
- Economist style guide [V, introduction text]: opens with the aim of clear writing from clear thinking, and reproduces Orwell's six rules: no stock figures of speech, prefer the short word, cut a word where possible, use the active voice, avoid foreign, scientific or jargon words when an everyday one exists, and break any rule rather than write something barbarous.
- Wikipedia 'Signs of AI writing' [V]: flags overused words such as delve, crucial, pivotal, vibrant, showcase, underscore and tapestry, 'serves as' and 'stands as' in place of 'is', negative parallelisms ('not just X, but Y'), inflated significance, promotional tone, tacked-on '-ing' analysis phrases, vague attribution to unnamed experts, default lists of three, leftover chatbot hedging or placeholders, and Markdown or boldface overuse. The page stresses these are indicators, not proof, and that fixing surface tells does not fix accuracy or sourcing.
- Orwell: prefer the short word, cut needless words, active voice, avoid jargon where an everyday equivalent exists.
- Economist: short sentences, plain verbs, concrete nouns, no hedging and no cliches; numbers over adjectives.
- GDS content design: write for the reader, plain English, one idea per sentence, 'you/we' voice where the context allows, front-load the point.
- Minto: write the conclusion first; each sentence should serve the one above it.
- Wikipedia "Signs of AI writing": watch for inflated significance, promotional tone, vague attribution, tidy rule-of-three lists, "not only... but also" constructions, em-dash overuse, headline-style Title Case, and formulaic summary endings. Fix by naming specifics, sources, numbers and dates.

### 4.2 Do
- State the finding in the first sentence, with a number: "Forecast cost is £412m, £31m above budget."
- Use concrete subjects and active verbs: "The contractor missed three milestones" (not "Milestones were missed").
- Name who, what, by when: "Owner: J. Patel. Due: 14 Nov."
- Vary sentence length. Short sentences for conclusions; a longer one only when the logic needs it.
- Use the client's terms (WBS names, system names) and define each acronym once.
- Quantify: replace "significant", "substantial", "considerable" with the number.
- Say what you do not know: "Not yet confirmed; the supplier reply is due 8 Nov."
- Keep bullets as fragments of equal grammatical form; use full sentences for titles.
- Prefer "because", "so", "but" over "furthermore", "moreover", "consequently".

### 4.3 Don't
- Do not open with throat-clearing ("It is important to note that…", "In today's fast-paced landscape…").
- Do not stack three adjectives or three parallel nouns by reflex.
- Do not use em dashes as a rhythm tic. Use a full stop, comma or colon.
- Do not close a slide with a summarising platitude ("Ultimately, this ensures success").
- Do not use vague attribution ("experts say", "industry reports suggest"). Name the source.
- Do not use the "not just X, but Y" or "it's not about X, it's about Y" construction.
- Do not use Title Case on titles or bullets. Use sentence case.
- Do not use emoji, exclamation marks, or promotional adjectives.
- Do not hedge every claim ("may potentially"). Hedge once, where uncertainty is real, and give the range or confidence level.

### 4.4 Banned and flagged phrases (starter list; extend in the skill)
| Category | Examples |
|---|---|
| AI tells (verbs and nouns) | delve, delve into, underscore (v.), showcase, foster, leverage (v.), harness, unlock, elevate, navigate (the landscape), streamline, tapestry, testament to, realm, landscape (figurative), journey, pivotal, crucial, vital, robust, seamless, holistic, comprehensive (as filler), cutting-edge, game-changer, transformative |
| Throat-clearing | it is important to note, it's worth noting, in today's, in an ever-changing, at its core, when it comes to, in order to (use "to"), moving forward, going forward, at the end of the day |
| Consulting bloat | synergies, best-in-class, world-class, paradigm shift, low-hanging fruit, boil the ocean, move the needle, circle back, deep dive, touch base, bandwidth, ecosystem (as a filler), value-add, thought leadership, end-to-end (unless literal), alignment (as a goal), enablers, optimise (without a metric), drive (without a metric), "stakeholder engagement" with no names |
| Structure tells | "Not only… but also", "From X to Y" scope sweeps, rule-of-three adjective lists, "Whether you're A or B", closing "In conclusion/Overall/Ultimately", "key takeaways" headers on every slide |
| Inflation | significant (without a number), substantial, remarkable, groundbreaking, vibrant, rich, stunning |
| Hedges | may potentially, could possibly, somewhat, relatively (without a baseline) |
Replace rather than just delete: ask what the claim is, and give the number or the source.

### 4.5 Mechanical checks the skill can run
- Title length (words and lines), sentence case, ends without a full stop.
- Banned-phrase and em-dash density scan; count of "not only/but" constructions.
- Every number has a unit, period and source.
- Reading-grade check (aim for about grade 8-11 for exec content; precision beats simplicity for technical appendices).
- Parallel structure across bullets.
- Acronym defined on first use per section or in a glossary.

---

## 5. Adaptive interviewing and inference from context

### 5.1 Infer first, ask second
- Before asking anything, scan the available material: meeting notes, emails, previous decks, RAID logs, schedules, cost reports, the project charter, org charts. Extract: client and sponsor, audience and their seniority, purpose or decision, timeline, last status, known issues, naming and format conventions, previous RAG values, open actions.
- Present inferences back as a short assumption list for confirmation ("I have taken the audience to be the SteerCo, the decision to be X, and the period to be Oct. Correct?"). Confirmation questions are cheaper than open ones and avoid asking things the user has already said.
- Ask only what changes the deck: if either answer would produce the same slides, do not ask.
- Mark each inference with confidence; ask about low-confidence, high-impact items first.

### 5.2 Core intake questions (the minimum viable set)
1. Decision or outcome: What should the audience decide, approve or do after this deck? (If none, is it for information, alignment or discussion?)
2. Audience: Who is in the room (names or roles), what do they already know, what do they care about, who is sceptical, who decides?
3. Format and setting: presented or pre-read; time available; SteerCo, working session, board paper, client workshop?
4. The one-sentence answer: If they remember one thing, what is it? (the governing thought)
5. Evidence and data: what is available, what is the source of truth, what is the cutoff date, what is estimated?
6. Constraints: length, template/branding, confidentiality, politically sensitive items, items that must (or must not) appear.
7. Deadlines and review: who reviews, when, is there a previous version to match?
8. For PMO decks: reporting period, baseline version, RAG policy and thresholds, escalation routes, tolerances.

### 5.3 Adaptive technique
- Branch on the deck type: pick the next question from the answer to the last. Status report: ask about RAG policy and baseline. Strategy deck: ask about the question, hypotheses, options. Capital sanction: ask about gate, estimate class, risk allowance.
- Ask 3-5 questions at a time, ordered by impact, with suggested defaults the user can accept ("Default: SteerCo, 12 slides, decision-first. OK?"). Offer multiple choice where options are known; leave one open "anything else I should know?".
- Probe for stories and specifics rather than opinions: "What happened last SteerCo when X was raised?" (Mom Test principle: ask about past behaviour and facts, not hypothetical preferences).
- Use funnel questioning: broad then narrow; follow with "what would make that wrong?" to surface risks and sensitivities.
- SPIN (Situation, Problem, Implication, Need-payoff) provides a sequence for uncovering why the decision matters; use sparingly because of its sales origin.
- Clarify terms: "When you say 'overspend', is this against baseline budget or last forecast?"
- Reflect back: summarise understanding in the ghost deck (titles only) and ask for edits. A ghost deck is itself the best interview tool: people react to a draft faster than they specify from scratch.
- Do not ask for what a file already contains. If a document conflicts with the user's statement, flag the conflict and ask which wins.
- Stop interviewing when remaining unknowns would not change the storyline; mark them as assumptions on the slide or in a note.
- Sensitive content: if the material shows politically sensitive items (a sponsor under pressure, a contractor dispute), ask how to frame, not whether to include.

### 5.4 "What decision does this deck need to drive" prompts
- "After the meeting, what will be different if it goes well?"
- "Who has to say yes, and to what exactly?"
- "What will they ask that we cannot yet answer?"
- "What is the cost of no decision this month?"
- "If you only had 5 minutes with them, what would you say?"

---

## Sources
All accessed 2026-11-01. [V] = fetched and read this session; [S] = secondary or search summary only; [N] = fetch failed or not read.

Gateway and government
- [V] NISTA, Guidance to Conducting Gateway Assurance Reviews, for international use (Aug 2026): https://assets.publishing.service.gov.uk/media/6a7ddaf40ad4bc475be7de10/NISTA_IGR_Gateway_Assurance_Reviews_Guidance_August2026.pdf
- [V] GOV.UK, NISTA assurance review toolkit (gate list, dates, IPA now part of NISTA): https://www.gov.uk/government/collections/nista-assurance-review-toolkit
- [V] IPA Gate 2 Delivery Strategy workbook (v1.0, 2021): https://assets.publishing.service.gov.uk/media/60f018b3e90e0764ce826745/1174-APS-2-CCS0521656666-001_IPA_Gateway_Web1.pdf
- [V] IPA Gate 0 Strategic Assessment workbook: https://assets.publishing.service.gov.uk/media/60f01860e90e0764cb10bd8a/1174-APS-0-CCS0521656666-001_IPA_Gateway_Web.pdf
- [V] IPA Annual Report on Major Projects 2015-16 (five-level DCA): https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/535243/ipa_annual_report_on_major_projects_2015_2016.pdf
- [S] NISTA Major Projects Annual Report 2025-26 (three DCA groups): https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26
- [S] NISTA Annual Report 2024-25 (Annex A definitions, Reset label): https://www.gov.uk/government/publications/nista-annual-report-2024-2025/nista-annual-report-2024-25
- [V, partial] IPA Cost Estimating Requirements: https://assets.publishing.service.gov.uk/media/6050f086e90e07527e988210/IPA_CostEstimatingRequirements.pdf
- [V, page only] HM Treasury, The Orange Book (2013, May 2023 edition): https://www.gov.uk/government/publications/orange-book
- [S] Orange Book PDF: https://gov.uk/government/publications/orange-book/the-orange-book-management-of-risk-principles-and-concepts

Cost, schedule, estimating
- [V] GAO-16-89G Schedule Assessment Guide: https://www.gao.gov/products/gao-16-89g and PDF https://www.gao.gov/assets/gao-16-89g.pdf
- [V] GAO-20-195G Cost Estimating and Assessment Guide: https://www.gao.gov/products/gao-20-195g and PDF https://www.gao.gov/assets/gao-20-195g.pdf
- [V] AACE International RP 18R-97 (Table 1 matrix; copy hosted by Government of Canada): https://canadabuys.canada.ca/documents/pub/att/2021/10/28/2305b22cf3ce2931a9ca532a8274cba4/appendix_e_-_annex_7.2_-_classification_system_cost_estimate_matrix.pdf
- [V, vendor] IPA (Independent Project Analysis) FEL Toolbox / FEL Index: https://www.ipaglobal.com/services/applications-tools/fel-toolbox
- [S] IPA newsletter June 2025 (FEL Index trend): https://www.ipaglobal.com/resources/newsletter/ipa-newsletter-june-2025-volume-17-issue-2/newsletter2025-q2-volume17-issue-2

Project management standards
- [S] PMI, 12 project management principles: https://www.pmi.org/-/media/pmi/documents/public/pdf/pmbok-standards/12-project-management-principles.pdf
- [S] PMI, PMBOK Guide page (edition counts): https://www.pmi.org/standards/pmbok (direct fetch returned 403; counts taken from search summary)
- [N] PMI Practice Standard for Project Risk Management: only unofficial copies found; buy or verify at https://www.pmi.org/standards
- [S] PRINCE2 wiki, Highlight report (unofficial): https://prince2.wiki/management-products/reports/highlight-report/
- [S] PRINCE2 wiki, Project log (unofficial): https://prince2.wiki/management-products/project-log/
- [S] PeopleCert PRINCE2 version history: https://www.prince2.com/usa/prince2-processes
- [N] Official PRINCE2 7 manual (product descriptions for highlight report and risk register): not accessible

Consulting craft
- [S] Leland, The Pyramid Principle in Consulting: https://www.joinleland.com/library/a/the-pyramid-principle-in-consulting-what-to-know
- [V] Wikipedia, MECE principle: https://en.wikipedia.org/wiki/MECE_principle
- [V] Slideworks, How to write action titles like McKinsey: https://slideworks.io/resources/how-to-write-action-titles-like-mckinsey
- [V] Think Insights, Write good slide titles: https://thinkinsights.net/insights/write-good-slide-titles
- [S] Think Insights, Pyramid Principle: https://thinkinsights.net/index.php/strategy/pyramid-principle
- [S] StrategyU, Consulting presentations: https://strategyu.co/consulting-presentations/
- [S] Deckary, Consulting slide standards: https://deckary.com/blog/consulting-slide-standards
- [S] think-cell, How to tell a better data story one slide at a time: https://www.think-cell.com/en/blog/how-to-tell-a-better-data-story-one-slide-at-a-time
- [S] Duarte and HBR: the search did not locate an HBR slide-headline article. 'Present Your Data Like a Pro' is by Joel Schwartzberg (HBR, 2020). Duarte's book is HBR Guide to Persuasive Presentations. Not used for any rule above.
- [N] Minto International (minto.com) and The Pyramid Principle book: not fetched; claims about vertical and horizontal logic rest on the secondary sources above.

Writing
- [V] GOV.UK A to Z style guide: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/ (redirect from https://www.gov.uk/guidance/style-guide/a-to-z-of-gov-uk-style)
- [V] Wikipedia, Signs of AI writing (first 100,000 of about 241,000 characters read): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- [V, publisher preview] The Economist Style Guide introduction (Profile Books preview): https://profilebooks.com/wp-content/uploads/wpallimport/files/PDFs/9781782833482_preview.pdf (economist.com direct fetch was blocked)
- [S] Orwell, Politics and the English Language: https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/

Interviewing (not re-verified this round)
- [N] Fitzpatrick, The Mom Test: https://www.momtestbook.com/
- [N] Block, Flawless Consulting; Rackham, SPIN Selling; Torres, Continuous Discovery Habits: https://www.producttalk.org/
