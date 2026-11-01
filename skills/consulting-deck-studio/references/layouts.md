# deck.md format and layout reference

A deck is one `deck.md` file. `build.py` turns it into `deck.html`, `deck.pptx` and (with `--pdf`) `deck.pdf`, all
drawn from the same layout, so the three always match. A complete worked example is in
`examples/northline-rail-steerco/deck.md`.

## File structure

```
---
deck: Northline Rail Programme: October SteerCo      # file title
context: Client  |  Meeting  |  Month Year            # small line top-left of every content slide
tracker: Summary, Schedule, Risk, Cost                 # section names shown top-right; slide `section:` highlights one
sticker: Preliminary                                   # or "Draft for discussion"; omit for final decks
source: Default source line for every slide            # slides can override
confidential: yes                                      # "no" hides the Confidential mark
---

# Action title: a full sentence that states the takeaway, 15-25 words, no full stop
layout: status-summary
section: Summary                 # which tracker item to highlight
sowhat: One-line implication or ask, shown in a box above the footnotes (use sparingly: slides with an ask)
footnote: Numbered footnote. Repeat the key for more.
source: Overrides the deck source for this slide
sticker: Overrides the deck sticker

```json
{ "layout data": "see below" }
```

??? Speaker notes. They go into the PPTX notes pane and appear under each slide in reader mode (deck.html?reader).
```

**Inline text:** `**bold**` is the only markup inside strings. **Sub-bullets:** where a field takes bullets, a
two-item list `["text", 2]` is a level-2 bullet.

**Side panels.** Chart and Gantt layouts accept a right-hand column:
- `takeaways` (numbered sentences, which match numbered callouts on the exhibit), titled by `takeaways_title`
  (default "What this shows").
- `panels`, a list of `{"title", "bullets"}` bullet panels stacked underneath.
Leave both out to give the exhibit the full width.

**Overflow is an error, never a silent shrink.** If content doesn't fit, the slide shows a red error card and
the build exits 1. Fix it by cutting words, splitting the slide, or moving detail to the appendix.

## Structure layouts

| layout | data fields |
|---|---|
| `title` | `subtitle`, `client`, `date`, `prepared_by`, `confidential` (bool), `confidential_text` |
| `agenda` | `items`: strings or `{title, note}`; `active`: 1-based index to highlight (for repeated tracker pages) |
| `section` | `number` (e.g. "02"), `subtitle` |
| `exec-summary` | `points`: `[{lead, support: [..]}]`. The dot-dash format: bold lead statements on the left, supporting points on the right. 3-5 points. |
| `columns` | `columns`: `[{header, icon?, bullets}]` (2-4 columns); `compare`: `[{label, values: [text or {text, rag}]}]`, an aligned comparison strip under the columns (cost, date, risk) |
| `decisions` | `decisions`: `[{what, recommendation, owner, due}]` |

## Exhibit layouts

All exhibit layouts take `exhibit` (the bold exhibit title) and `unit` (the grey unit line, e.g. "£m, nominal,
October 2026"). Number formatting is set with `prefix` ("£"), `suffix` ("%") and `decimals`.

| layout | data fields |
|---|---|
| `bar` | `categories`, `series: [{name, values}]`, `orientation`: `column` (default) or `bar` (horizontal, for long labels and rankings), `highlight` (index of the bar to emphasise; the others go grey), `stacked`, `cagr: {from, to, label}`, `label_width` |
| `line` | `x`, `series: [{name, values, highlight?, color?, forecast? (dashed), markers?}]`, `axis_min`, `axis_max`. Lines are labelled at their ends, with no legend. |
| `waterfall` | `start: {label, value}`, `steps: [{label, value}]`, `end: {label, value?}`, `axis_min`, `callouts`: step indices to number, `increase_is`: `bad` (default, increases red) or `good`, `show_total_change`. **If `end.value` doesn't equal start + steps, the build fails.** |
| `matrix-2x2` | `x: {label, low, high}`, `y: {...}`, `quadrants`: [top-left, top-right, bottom-left, bottom-right] labels, `highlight_quadrant` (0-3), `items: [{label, x 0-1, y 0-1, size?, highlight?}]` |
| `table` | `columns: [{name, width (fraction or pt), kind: text, bold, number, rag or trend, align?, good?: up or down}]`, `rows: [[...]]`. Adds a RAG or trend legend when those columns exist. |

## PMO and capital-project layouts

| layout | data fields |
|---|---|
| `status-summary` | `rows: [{area, icon?, rag: R, A or G, trend: up, flat or down, text}]`, `decisions: [{what, owner, due}]`, `decisions_title`, `lookahead: {title, rows: [{milestone, baseline, forecast, variance, rag}]}` |
| `rag-dashboard` | `kpis: [{value, label, note, rag}]` (a number strip; 3-5 work best), `rows: [{workstream, lead, schedule, cost, risk, trend, comment}]`; `columns` and `keys` override the default table |
| `gantt` | `start`, `end`, `today` (ISO dates), `rows: [{name, rag?, critical?, baseline: [s, e], forecast: [s, e], float_to?, float_label?, callout?}]`, `milestones: [{name, baseline, forecast, callout?}]`, plus side panels |
| `risk-heatmap` | `risks: [{id, title, owner, l 1-5, i 1-5, prev?: [l, i], mitigation, trend?}]`, `red_from` (default 15), `amber_from` (default 8). Movement arrows come from `prev`. |
| `options-matrix` | `criteria: [{name, weight: "30%"}]` (weights must total 100%), `options: [{key, name, scores 0-4}]`, `recommended`, `stages` + `stage` (chevron funnel), `rationale` (bullets) |

## Logic, process and organisation layouts

| layout | data fields |
|---|---|
| `issue-tree` | `root: {text, children: [{text, rag?, highlight?, children}]}` (up to 3 levels below the root; about 12 leaves). `rag` on leaves records the hypothesis status. `legend: [[kind, colour, label]]`. Plus side panels. |
| `driver-tree` | `root: {label, value, delta?, delta_bad?, highlight?, children}`. **Check the children add up to the parent** before building; the build does not do arithmetic on display strings. |
| `process-flow` | `steps: [{title, bullets or text, owner?, duration?}]`, `active` (the title of the current step) |
| `roadmap` | `periods`, `phases: [{name, start, end}]`, `lanes: [{name, items: [{label, start, end, rag?, highlight?} or {type: "milestone", label, at, rag?}]}]`, `today` (period index, fractions allowed) |
| `timeline` | `start`, `end`, `events: [{date, label, detail?, done?, rag?}]` |
| `org-chart` | `nodes: [{id, title, name?, parent?, note?, highlight?}]` (top-down; about 6 boxes in the widest row) |
| `raci` | `roles`, `activities: [{name, cells: [R/A/C/I/""]}]`. **Each row needs exactly one A.** |
| `before-after` | `rows: [{dimension, before, after}]`, or `before`/`after` bullet lists; `before_title`, `after_title` |

## Capital project controls layouts

| layout | data fields |
|---|---|
| `s-curve` | `x`, `planned`, `earned`, `actual` (cumulative), `bac`. **SPI, CPI, the variances and EAC (BAC/CPI) are computed from the data**, never typed in. Plus `takeaways`. |
| `p-curve` | `samples` (raw simulation outcomes) or `points: [[value, cumulative p]]`, `percentiles` (default [50, 80]), `budget`, `budget_label`. **P-values and the budget's confidence level are computed.** |
| `benefits-tracker` | `benefits: [{name, owner, unit, baseline, target, actual, rag, due, decimals?}]`. Progress to target is computed. |
| `stage-gate` | `gates: [{label, name, date, status: done, current or future, decision?, criteria?}]` |
| `raid-log` | `items: [{type: Risk, Issue, Assumption, Dependency or Decision, id, description, owner, due, rag, status}]`, sorted by type |

## Analysis layouts

| layout | data fields |
|---|---|
| `marimekko` | `columns: [{label, width_value, width_label, segments: [{label, value}]}]`, `highlight` (segment label). Shares are computed. |
| `benchmark` | `items: [{label, value, highlight?}]`, `better`: `high` or `low`. The median is computed. |
| `key-numbers` | `numbers: [{value, label, note?, rag?}]` (2-6) |
| `tornado` | `base`, `drivers: [{name, range, low, high}]` (output value in the low and high case). Sorted by swing automatically. |
| `scatter` | `points: [{label, x, y, size?, rag?, highlight?}]`, `x_label`, `y_label`, `bubbles` (size = area), `reference: [{x or y, label}]`, `x_format` and `y_format` ({prefix, suffix, decimals}) |
| `quotes` | `quotes: [{text, who (role, not name), theme?}]`. **Quotes must be real and attributed by role.** Never invent them. |

## Conventions the layouts enforce

- **RAG** is a plain dot plus the word. Every slide that uses RAG or trend shows a legend, and the RAG definitions
  belong in a footnote or the appendix.
- **Trends** are triangles: green when things improve, red when they get worse. For risk scores, a rising score is
  red.
- **Icons** (`icon` fields) are Lucide line icons: monochrome, inline and sparse. Names are in
  `assets/icons/lucide/`. Use them on row labels or column headers where they help scanning. Never use them as
  decoration.
- **Callout numbers** on an exhibit must match the numbered takeaways beside it.
