# The reference library: 164 real consulting decks and reports

`data/decks.json` holds publicly available consulting material, each item verified by opening it. Every record has:
- the firm, tier, client, year and sector
- the URL and how it was published (firm, client, government, FOI or filing)
- its slide or section sequence and storyline pattern
- its signature slides, standout moves, weaknesses and design notes
- for reports, its `content_value`

Use it for **patterns and calibration**: what a real SteerCo pack, IV&V report or gate paper contains, how long it
runs, and how its best slides argue. **Never copy** wording, layouts or branding, and never cite a library deck as a
source of facts for the user's deck.

## Coverage (be honest about it)

| Practice | Records | Tier 1 (MBB/Big 4 authored) | Tier 2 | Tier 3 (specialists) | Slide decks | Reports |
|---|---|---|---|---|---|---|
| PMO | 29 | 6 | 6 | 17 | 10 | 19 |
| Capital projects | 58 | 9 | 5 | 44 | 58 | 0 |
| Strategy | 35 (+17 secondary) | 26 | 5 | 4 | 35 | 0 |
| Management | 42 | 34 | 2 | 6 | 31 | 11 |

Public slide decks written by MBB or Big 4 firms are rare for PMO and capital work. Most status reports and
assurance reviews are published as portrait reports, or written by specialist firms. Those records are tagged
`format: "report"` or tier 3. Use reports for *content*: required fields, rating scales and how findings are framed.
Use slide decks for *layout and flow*.

## How to use it in the workflow

| Step | Command | What to take from it |
|---|---|---|
| Storyline (step 4) | `python3 SKILL_DIR/scripts/find_decks.py --practice <p> --type <playbook type> --limit 6` | Typical sequence and length, and how the best decks open (answer first? rating first?) |
| A specific slide | `find_decks.py --q "heat map"` or `--q "waterfall"` | How real decks frame that exhibit: title, annotations, footnotes |
| Assurance and IV&V | `find_decks.py --practice pmo --type assurance --full` | Rating scales, RAG definitions (`rag_definitions`), finding → recommendation → response formats |
| Calibration | `find_decks.py --stats` | Whether the library has good comparables for this deck type. If not, rely on the playbook |

Types follow the playbooks in `deck-types/`:
- **PMO:** status-report, steerco, dashboard, risk-review, schedule-review, pmo-setup, go-live, assurance, benefits,
  close-out
- **Capital projects:** gate-paper, independent-review, cost-review, qra, delivery-model, prioritisation,
  recovery-plan, owners-report, benchmarking, close-out
- **Strategy:** diagnostic, growth-strategy, market-entry, due-diligence, portfolio, economic-development,
  board-update
- **Management:** diagnostic, cost-review, operating-model, transformation, transformation-office, pmi, service-review,
  change-plan

## Patterns across the library

### PMO (assurance, status, dashboards)
- **Ratings come before prose.** The strongest assurance packs give a rating per criterion or area (G/A/R with a
  defined scale), then findings, then recommendations *with target dates*. The weakest bury the rating in text.
- **Decision-ready openings.** The better packs open with a one-line, decision-ready recommendation tied to a dated
  governance decision point.
- **They track their own recommendations.** "204 actions agreed, n closed" builds credibility period after period.
- **A plan on a page** aligns assurance or PMO activity to programme milestones.
- **Typical length** is about 13 slides for a periodic pack. Reports run longer.
- **Common weaknesses:** heavy tables in small text, dashboards that are mostly text, and screenshots without
  commentary. The `status-summary` and `rag-dashboard` layouts and the density lint exist because of these.

### Capital projects
- **Navigation:** a persistent tracker or breadcrumb (Executive summary / Background / Findings / Appendices) on every
  slide, as in long independent reviews.
- **Conclusion-as-title on every content slide**, with a source line on every exhibit. The best reviews do this
  consistently.
- **Independence is stated** ("standalone assessment"), and the method sits in a callout.
- **Risk-rating chips on findings,** and issue-and-response grids phase by phase.
- **Stage-gate tied to budget and financial-plan phases.** Gate papers show the approvals timeline and the
  governance swimlane.
- **Typical length** is about 23 slides (median).
- **Common weaknesses:** text-dense finding slides, few quantified exhibits, and pages flattened to images.
  Reproduce the structure, not the density.

### Strategy
- **Exhibits are mostly bar charts and benchmarks, with maps for geographic work.** 2x2s and trees are rarer than
  folklore suggests. The insight is in the title and the annotation, not an exotic chart.
- **Numbered findings and section-numbered titles** (2.1, 2.2) help long decks. "Required versus actual" growth
  framing makes a target concrete.
- **Peer profiles in identical templates** make comparison easy.
- **Typical length** is about 39 slides (public-sector strategy decks run long). Board versions are 10-20.
- **Common weaknesses:** descriptive rather than prescriptive, dense paragraphs under titles, and firm credentials up
  front. Recommendations belong early.

### Management (operations, service reviews, cost, operating model)
- **Each recommendation carries its outcome, owner, response and target year,** often as columns in one table.
- **Opportunities already under way are separated from new ones,** so savings aren't double counted.
- **Numbered callouts tie waterfall bars to takeaway bullets.** The `waterfall` and `takeaways` layouts reproduce this.
- **Uniform service-profile templates** are used across departments or agencies.
- **Typical length:** the full compendiums run to about 54 slides, but council-facing versions compress to 15-20.
- **Common weaknesses:** label titles ("3. Finance"), table-heavy pages, few visuals. Use action titles, and move the
  tables to the appendix.

## Rebuilding the library
The raw sweeps are in `research/raw/` in the repository, not the installed skill. `tools/merge_library.py` rebuilds
`data/decks.json`. Add new records to a raw file with the same schema, mark how each one was verified, and rerun the
merge.
