# Consulting Deck Studio: build plan

Working name: **consulting-deck-studio** (repo `ali-lari1/consulting-deck-studio`). A sibling of
pitch-deck-studio, with the same install story and the same "materials first, few questions, facts ledger,
review panel" approach, rebuilt for consulting work.

Status: DRAFT for approval. Deck-library counts are filled in when the research sweeps finish (section 2).

---

## 1. What it does

One agent skill that produces consulting-grade decks across four practices:

| Practice | Typical decks |
|---|---|
| **PMO** | Weekly/monthly status report, programme/portfolio dashboard, SteerCo pack, RAID and risk review, integrated schedule and milestone review, PMO setup and governance, go-live readiness, assurance and health check (IV&V), benefits tracking, close-out and lessons learned |
| **Capital Projects** (PMO sits under this, but gets its own deck types) | Business case and gate/sanction paper, independent project review, cost-to-complete and estimate review, schedule and critical-path review, quantified risk (P50/P80), delivery-model and procurement strategy, capital programme prioritisation, recovery plan, benchmarking, mobilisation and owner's-rep report |
| **Strategy** | Situation diagnostic, growth strategy and options, market entry and attractiveness, portfolio strategy, commercial due diligence summary, economic-development strategy, board strategy update, scenarios |
| **Management** | Operational diagnostic, cost and efficiency review, operating model and org design, transformation roadmap, transformation SteerCo update, post-merger integration, change plan, service review and benchmarking |

It asks contextual questions that are not scripted in advance, reads meeting notes and project files, can link to a
project so recurring decks (such as the monthly status report) roll forward, and outputs **editable PPTX, HTML and
PDF that render identically**.

### How it differs (from the landscape scan)
- Existing open-source "McKinsey-style" skills each do one job: a template library, chart styling or title rules.
  None cover PMO or Capital Projects. None read schedules (XER, MS Project XML) or transcripts. None apply a client
  template. None guarantee PPTX equals what you previewed.
- Commercial tools (Copilot, Gamma, Plus AI and others) produce generic structure, topic titles instead of action
  titles, and no waterfall or Marimekko charts. Their PPTX export drifts from the preview.

---

## 2. Research done so far

| Thread | Result | File |
|---|---|---|
| Slide craft and PMO/capital standards | Done. Checked against the GAO Schedule and Cost guides, AACE 18R-97, GOV.UK Gateway/NISTA, the GOV.UK and Economist style guides and Wikipedia's "Signs of AI writing". Craft rules are marked as "secondary" where the source is training material rather than the firms themselves. | `research/craft-and-standards.md` |
| Competitor and format landscape | Done, including the parity architecture | `research/landscape.md` |
| Deck library: Strategy | **52 verified** (41 tier 1, 6 tier 2, 5 tier 3). Some ops reviews will move to Management at merge. | `research/decks-strategy.json` |
| Deck library: Management | _running_ (17 verified before widening) | `research/decks-management.json` |
| Deck library: Capital Projects | _running_ (13 tier 1-2 and 6 tier 3 before widening) | `research/decks-capital-pmo.json` |
| Deck library: PMO | _running_ (12 before widening) | `research/decks-pmo.json` |

**Finding that shaped the library:** few public slide decks are authored by MBB or Big 4 firms. Government
releases are mostly prose reports, and US IV&V and QA reports are mostly written by boutique firms. As you
decided, the library is **tier-flagged**:
- **Tier 1:** authored by MBB or Big 4 (including Strategy&, Monitor Deloitte and EY-Parthenon).
- **Tier 2:** a client deck presenting named MBB or Big 4 work, or a firm-published slide-format report or conference deck.
- **Tier 3:** an established specialist firm, such as Oliver Wyman, Kearney, Roland Berger, L.E.K., Accenture,
  Turner & Townsend, AECOM, Jacobs, PCG or BerryDunn.

The target is 50-70 per practice. The skill ranks tier 1 first when it pulls comparables. Every record is verified
by opening the deck and records how it was published (firm, client, government, FOI or filing). Leaked
confidential material is excluded.

---

## 3. The workflow (what the user experiences)

```
0 Link      ->  1 Read everything  ->  2 Play back + ask  ->  3 Ghost deck (approve)  ->
4 Facts ledger  ->  5 Build  ->  6 QA + review panel  ->  7 Deliver (+ roll forward next period)
```

### 0. Link to a project (optional, but it makes recurring decks easy)
`init_project.py` creates `<engagement>/.cds/project.json` holding the client, sponsor, audience, RAG policy and
thresholds, baseline version, reporting cadence, stakeholder map, house template, and prior-period RAG and
milestones. It can be pointed at a folder, a Notion page, an Asana/Jira/Smartsheet/monday project, or a SharePoint
or Drive folder through whatever connector the agent has. Next month, "make the October status report" diffs
against September automatically and covers what moved, what slipped and which risks escalated.

### 1. Read before asking
Inputs read offline with the Python standard library only:

| Input | Formats |
|---|---|
| Meeting notes and transcripts | `.md` `.txt` `.docx` `.vtt` `.srt`, and Teams/Zoom/Otter/Granola/Fireflies exports |
| Schedules | Primavera `.xer`, MS Project XML (MSPDI), CSV/XLSX exports. `.mpp` must be saved as XML first. |
| Risk, RAID, cost, benefits | `.xlsx` and `.csv` (header mapping for common register layouts) |
| Prior decks and templates | `.pptx` (text, titles, theme), `.potx` (colours, fonts, logo, master background), PDF via the agent's PDF reading |
| Web | Client site for brand and context, and live research for strategy and market decks |
| Connectors (optional) | Notion, Asana, Jira/Confluence, Smartsheet, monday, Google Drive, SharePoint/OneDrive, P6/MSP MCP servers. Detected, never required. |

Each extractor writes normalised JSON (`research/schedule.json`, `risks.json`, `notes.json`, ...). Charts and
tables are built from that JSON, so every number traces back to a file.

### 2. Play back, then ask (adaptive, not scripted)
- The skill holds an **information-requirements model** per deck type. It is the mandatory, recommended and
  optional field matrix from `craft-and-standards.md` section 3.10. For example, a status report needs RAG with a
  rationale, milestones baseline vs forecast, budget/EAC, top risks, decisions needed and an as-of date.
- After reading, it plays back what it inferred, each item with a confidence level ("I read this as the October
  SteerCo pack for the Northline rail programme; the decision is approving the £14m contingency drawdown").
- It then generates questions only for the gaps. They are ranked by **impact on the storyline × uncertainty**,
  3-5 per round, each with a default you can accept, and multiple choice when the options are known. The next
  round depends on the last answer: "status report" leads to RAG policy and baseline, "gate paper" leads to estimate
  class and risk allowance, and "strategy" leads to the core question, hypotheses and options.
- The anchor questions always get covered: **what decision this deck drives, who is in the room, and whether it is
  presented or a pre-read.**
- Conflicts between files and what you said are flagged rather than silently resolved. Sensitive items (a sponsor
  under pressure, a contractor dispute) prompt "how should we frame this?", never "should we include it?".
- It stops asking when the remaining unknowns would not change the storyline, and those become visible
  `[[placeholders]]`. Delegation mode ("just draft it") skips the questions and lists its assumptions.

### 3. Ghost deck: the one approval gate
A titles-only storyboard covering the governing thought, the pyramid (SCQA or answer-first), sections, and one row
per slide (# | layout | action title | exhibit | facts used). Two automatic tests run:
- **Horizontal:** read only the titles; does the story stand alone, in order, with no gaps or repeats?
- **MECE:** are the section arguments mutually exclusive and collectively exhaustive?
You approve or edit it, and only then are slides built.

### 4. Facts ledger
`facts.md` holds one row per number or claim, with source, as-of date and status (`client`, `file`, `sourced`,
`estimate`, `placeholder`). Numbers are reconciled across slides (EAC on the dashboard equals EAC on the cost
slide). Illustrative data must carry an "Illustrative" label.

### 5. Build
The skill writes `deck.md` (the same authoring format idea as pitch-deck-studio, extended with consulting layouts),
and one engine renders all three outputs (section 4).

### 6. QA and review panel
Lint checks:
- Titles are full-sentence takeaways of at most 2 lines.
- The body proves the title (vertical logic).
- Every number has a unit, an as-of date and a source.
- No placeholders are left in the final deck.
- Mandatory fields for the deck type are present.
- RAG and 5x5 scales are defined.
- The banned-phrase and em-dash scan passes.
- No text overflows.
- The **PPTX/HTML pixel diff** passes.

The review panel adapts to the deck type and runs as sub-agents if available, otherwise as sequential passes:
- **Status and PMO decks:** a sceptical SteerCo chair and a PMO director.
- **Capital decks:** a cost engineer or QS, and an assurance reviewer.
- **Strategy and management decks:** an engagement partner and a sceptical client CFO.
- **All decks:** a copy editor and a designer.

### 7. Deliver
- `deck.pptx` (editable)
- `deck.html` (present: arrows, overview, notes)
- `deck.pdf`
- `deck.html?reader` (pre-read version)
- `facts.md` (open items)
- `brief.md` (the storyline and the questions the audience will ask)

For recurring decks, it saves the period snapshot to `.cds/history/`.

---

## 4. Rendering: PPTX equals HTML equals PDF

Your requirement is a 100% match. The design is **one scene, three writers, no reflow anywhere**:

1. **Layout engine (Python stdlib).** Each slide becomes a scene of absolutely positioned elements in EMU on a
   13.333 × 7.5 in grid, covering text boxes, rectangles, lines, connectors, circles, Harvey balls and images.
2. **Text is measured and broken by us, not by the renderer.** The engine reads the font's TTF tables (`cmap`,
   `hmtx`, `kern`) with `struct`, wraps lines itself, and emits each line explicitly. If text doesn't fit, the build
   fails with a lint error; nothing is ever silently shrunk.
3. **PPTX writer.** Raw OOXML written with `zipfile`, so there is no python-pptx dependency. Text boxes use
   `wrap="none"`, no autofit, zero insets, exact `spcPts` line spacing and `spc` letter spacing, with a per-font
   baseline calibration table.
4. **HTML writer.** The same coordinates, `position:absolute`, `white-space:pre`, the same font files and the same
   line heights.
5. **PDF.** Generated from the HTML by headless Chromium, the same path pitch-deck-studio uses.
6. **Charts, Gantt charts, RAG tables, heat maps, waterfalls and Marimekkos are drawn as grouped shapes.** They are
   pixel-identical and editable as shapes, but there is no data sheet behind them. An opt-in `native_charts: true`
   writes real PowerPoint charts, with a warning that they may render slightly differently. Tables are also drawn
   as shapes in parity mode.
7. **Fonts.** The default faces are metrically stable everywhere: Arial and Georgia, or Liberation equivalents on
   Linux. Optional open fonts (such as Inter or Source Serif) are bundled and embedded where the format allows.
   Keynote and Google Slides ignore embedded fonts, so the docs say so, and the default avoids depending on them.
8. **Parity check.** `export.py --parity` renders the PPTX with headless LibreOffice (if installed), renders the HTML
   with Chromium, and compares them per slide with a stdlib PNG decoder. The build fails if the differences go above
   a threshold. LibreOffice is not PowerPoint, so the release checklist also includes a manual check in PowerPoint
   for Mac and Windows, Keynote and Google Slides on the example decks.

**Biggest technical risk:** text-metric parity, specifically baseline offsets and kerning differences between
PowerPoint and Chromium. A **parity spike comes first** (milestone M0) before anything else is built.

---

## 5. Slide archetype library (layouts the engine renders)

About 40 layouts, each with tuned spacing and density rules:

- **Storyline:** title, executive summary (dot-dash and SCQA forms), tracker/agenda, section divider, key message, appendix, sources
- **Logic:** issue tree, driver tree, hypothesis tree, 2×2, options evaluation with Harvey balls, criteria scoring matrix, pros/cons, before/after, process flow, swimlane, governance structure, org chart, RACI
- **Numbers:** KPI tiles, bar, stacked bar, line, waterfall (bridge), Marimekko, scatter/bubble, benchmark ranking, sensitivity tornado
- **PMO and capital:** RAG dashboard (overall and by dimension, with trend arrows), status one-pager, milestone tracker (baseline vs forecast), Gantt/roadmap with critical path, look-ahead, RAID log, risk register table, 5×5 heat map (inherent → residual), QRA P-curve (P50/P80), S-curve (planned/earned/actual), EVM CPI/SPI, cost bridge (budget → EAC), contingency drawdown, change-request log, stage-gate path, decisions-required, benefits tracker

Every slide shares the same anatomy: tracker, action title, optional lead-in, body, optional takeaway box, source
line, page number.

---

## 6. Copy: consulting register, human voice

- Action titles are full sentences that state the so-what, with numbers and at most 2 lines.
- Plain words, active voice and concrete subjects.
- No "leverage / synergies / robust / holistic / unlock / delve / in today's landscape", no triplets for rhythm,
  no em-dash chains and no hedging stacks.
- A banned and flagged phrase list (from GOV.UK, The Economist and Wikipedia's "Signs of AI writing") is enforced by
  lint, and a humanizer pass runs if a humanizer skill is installed.
- Speaker notes carry the reasoning, so slides stay sparse. Notes also become the pre-read text in reader mode.

---

## 7. Design and brand

- **3-5 neutral house themes** following consulting conventions: white canvas, one accent, navy/grey, thin rules
  and a small source line. They are **not** imitations of any firm's brand. No MBB names, logos or trade dress are
  used anywhere in the output.
- **Client brand** comes from a URL (colours, fonts, logo), a guidelines PDF, or a `.potx`/`.pptx` template. From
  the template, v1 extracts the theme colours, fonts, logo and master background, and recreates them in both
  HTML and PPTX so parity holds. Full inheritance of the client master and layouts is v1.1.
- A density setting for SteerCo pre-reads (dense) versus presented decks (sparse).

---

## 8. Deck library in the repo

- `data/decks.json` holds the tiered, verified records (practice, deck types, firm, tier, year, client type, sector,
  URLs, publication route, slide sequence, storyline pattern, signature slides, design notes, standout moves and
  weaknesses).
- `references/library.md` holds cross-deck patterns per practice and deck type, such as "IV&V decks open with a
  per-criterion G/A/R scorecard" or "the best status decks put decisions required on page 1".
- `scripts/find_decks.py --practice pmo --type status-report --tier 1-2 --limit 8` pulls comparables.
- **Copyright:** the repo stores metadata, short paraphrased slide summaries and links only. No PDFs, slide images
  or long quotes are copied, and the output never copies a source deck.

---

## 9. Repo layout and install (mirrors pitch-deck-studio)

```
consulting-deck-studio/
  README.md  LICENSE (MIT)  CHANGELOG.md  CONTRIBUTING.md  THIRD_PARTY_NOTICES.md
  install.sh  install.ps1                     # links into every detected agent
  AGENTS.snippet.md  GEMINI.md  gemini-extension.json
  .claude-plugin/{plugin.json,marketplace.json}
  .github/workflows/validate.yml              # frontmatter, manifests, data schema, example builds, parity
  tools/validate.py  tools/gen_library_md.py
  docs/images/
  examples/                                   # 3 fictional engagements, each with deck.pptx/html/pdf + inputs
    northline-rail-monthly-status/            # PMO: from an XER + risk register CSV + SteerCo notes (.vtt)
    harbour-hospital-gate-3/                  # Capital: gate paper with QRA and cost bridge
    meridian-cost-review/                     # Management: diagnostic → operating model → roadmap
  skills/consulting-deck-studio/
    SKILL.md                                  # < 250 lines; loads references on demand
    references/  interview.md  storyline.md  slide-craft.md  copy.md  design-system.md
                 deck-types/{pmo,capital-projects,strategy,management}/*.md   # one file per deck type
                 standards/{rag.md,risk.md,schedule.md,cost.md,gateways.md,benefits.md}
                 library.md  review.md  ingest.md  compose.md  parity.md
    scripts/     init_project.py  ingest_{xer,mspdi,xlsx,docx,pptx,transcript}.py  brand_from_url.py
                 template_from_potx.py  find_decks.py  layout.py  fonts.py
                 build.py (deck.md → scene → html/pptx)  export.py (pdf, png, sheet, --check, --parity)
    assets/      themes.json  deck.css  deck.js  fonts/  templates/
    data/        decks.json
```

Install, the same as pitch-deck-studio:
- `npx skills add ali-lari1/consulting-deck-studio -g`
- `gh skill install ali-lari1/consulting-deck-studio` (gh v2.90 or later)
- Claude Code: `/plugin marketplace add …`
- Codex: `~/.agents/skills`
- Gemini CLI / Antigravity: extension
- OpenCode, Hermes, Grok, Cursor, Copilot, Windsurf, Kiro, Cline, Goose, Amp: `install.sh`
- Windows: `install.ps1`
- Fallback for other agents: the `AGENTS.snippet.md` snippet

**Requirements:** Python 3.8 or later. Chromium for PDF export (optional). LibreOffice for the automated parity
check (optional).

---

## 10. Build milestones

| # | Milestone | Done when |
|---|---|---|
| M0 | **Parity spike** | 6 test slides (dense text, Gantt, heat map, waterfall, table, chart) render identically in Chromium and PowerPoint/LibreOffice, with the diff under threshold. Go/no-go on the architecture. |
| M1 | Engine and 15 core layouts | Scene model, font metrics, PPTX and HTML writers, PDF export, overflow lint |
| M2 | Remaining ~25 layouts and themes | All archetypes in section 5, 3-5 themes, client brand from URL and `.potx` |
| M3 | Ingest | XER, MSPDI, XLSX/CSV registers, DOCX, VTT/SRT, PPTX, tested on sample files |
| M4 | Knowledge | `SKILL.md`, interview model, deck-type files (≈36), standards, copy rules, review panel |
| M5 | Library | `decks.json` (50-70 per practice, tiered), `library.md` patterns, `find_decks.py` |
| M6 | Examples | 3 fictional end-to-end engagements, built from raw inputs by the skill itself |
| M7 | Packaging and CI | Installers, manifests, validate workflow, README with screenshots, tested in Claude Code, Codex and Gemini CLI |
| M8 | Release | Create the GitHub repo and push v1.0.0, **only after you confirm** |

---

## 11. Decisions for you

1. **Name.** `consulting-deck-studio`, or another name?
2. **Default fonts.** Arial/Georgia gives the safest parity everywhere. Bundled Inter/Source Serif looks better but
   has caveats in Keynote and Google Slides.
3. **Native charts.** Shapes by default with native charts opt-in, as proposed, or the reverse?
4. **Repo visibility.** Public, like pitch-deck-studio?
