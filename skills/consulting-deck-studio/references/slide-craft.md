# Slide craft

## Action titles
- **A full sentence with a subject, a verb and the so-what.** For example, "Forecast cost has risen £40m since Gate
  3, driven mostly by utilities and signalling", not "Cost update".
- **Put the number or comparison that proves the claim in the title.** Conclusion first, then the evidence.
- **15-25 words, at most two lines.** The layout steps the size down 1pt at a time to fit, warns when it does, and
  fails beyond that. More than two lines usually means two messages, so split the slide.
- **The body must be able to prove the title wrong.** If the body can't support it, change one of them.
- **Never** use question titles (except in working sessions), "Overview", "Update", "Introduction", gerund fragments
  ("Understanding the…"), a colon ending or a full stop.
- **Same-tense, parallel phrasing** within a section.

## Anatomy (the house layouts and template grids implement this)
1. Tracker and context line (small, top)
2. Action title
3. Exhibit header: what the exhibit is, then the **unit line** (units, scope, as-of date: "£m, nominal, October 2026")
4. One exhibit or one structured layout, with numbered callouts that point at the insight
5. Optional side panel with numbered takeaways that match the callouts, or next steps
6. Optional so-what box, *only* on slides that carry an ask. It must not repeat the title.
7. Footnotes (definitions, scales, caveats), then `Source: system or document, date; team analysis`
8. Page number and confidentiality mark

## One message, the right density
- One message per slide. Two "and" clauses in the title means two slides.
- Presented: 30-60 words in the body. Pre-read: 80-150.
- At most 3-5 bullets per box and two levels. Body text no smaller than 10pt. Overflow is a build error: cut words,
  never type size.
- One highlight colour for the key datum and grey for context. At most about six series on a chart.

## Choosing the exhibit (pick what proves the title)

| The title claims... | Layout |
|---|---|
| A total moved from A to B because of X, Y, Z | `waterfall` (must reconcile) |
| A ranking, or a comparison with peers | `bar` with `orientation: bar`, or `benchmark` (computes the median) |
| A trend over time | `line` (end labels, no legend); `bar` with `cagr` for a few periods |
| Composition across segments of different size | `marimekko` |
| Positioning on two measures | `scatter` (bubbles for size) or `matrix-2x2` |
| Options compared on criteria | `options-matrix` (weights must total 100%), `columns` with `compare` |
| Slippage against plan | `gantt`, a milestone `table`, `status-summary` with a look-ahead |
| Risk exposure and movement | `risk-heatmap` (with `prev`), `raid-log` |
| Earned value / cost performance | `s-curve` (computes SPI, CPI and EAC) |
| Cost or schedule confidence | `p-curve` (computes P-values and the budget's confidence) |
| Sensitivity | `tornado` |
| Where the money or problem is | `driver-tree` (check the arithmetic) |
| How the question breaks down | `issue-tree` (MECE; `rag` on leaves for hypothesis status) |
| What we will do, and when | `process-flow`, `roadmap`, `timeline`, `stage-gate` |
| Who decides and who does | `org-chart`, `raci` (exactly one A per row) |
| What changes | `before-after` |
| What people told us | `quotes` (real and attributed by role, never invented) |
| A few numbers that matter most | `key-numbers` |

Chart rules: sort the bars; bar axes start at zero (if not, say so in a footnote, as the waterfall's `axis_min`
does); label directly instead of using legends where possible; show units; mark deltas and CAGR with an arrow callout.

## Status conventions (PMO and capital)
- **RAG is a judgement against a stated tolerance.** Define it in a footnote or the appendix, and keep it consistent
  across slides and periods. Every red or amber carries a cause, an impact, an action, an owner and a date.
- **Show the trend against last period** next to every RAG.
- **Watch for "watermelon" reporting** (green outside, red inside): if the schedule data says late, the slide can't
  say green. The emitters compute RAG from the data. When you override it, footnote why.
- **Baseline and forecast always appear together.** Never overwrite a baseline. Label re-baselines with the change
  reference.

## Failure modes reviewers flag (check before review)
- A topic title, or a title that doesn't match the body
- A kitchen-sink slide carrying several messages
- Numbers that don't reconcile across slides (EAC on page 3 against page 9)
- Missing units, as-of dates or sources; TBC or placeholder values in a final deck
- Decoration over information: 3D, gradients, icon tiles on every row, rainbow palettes
- An executive summary that restates the agenda instead of giving the answer
- A buried recommendation, or no clear ask
- Next steps without an owner and a date
- Undefined acronyms and jargon (see `copy.md`)
