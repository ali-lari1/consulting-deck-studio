# Consulting Deck Studio: build plan

Working name: **consulting-deck-studio** (repo `ali-lari1/consulting-deck-studio`). A sibling of
pitch-deck-studio, with the same install story and the same "materials first, few questions, facts ledger,
review panel" approach, rebuilt for consulting work.

Status: approved 2026-11-01 (name, Arial/Georgia, shapes by default, public repo). M0 parity spike done; see section 4.

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
| Deck library: Strategy | 52 (41 tier 1, 6 tier 2, 5 tier 3), all slide decks | `research/raw/decks-strategy.json` |
| Deck library: Management | 32 (26 tier 1, 1 tier 2, 5 tier 3); 21 slide decks, 11 reports | `research/raw/decks-management.json` |
| Deck library: Capital Projects | 60 (10 tier 1, 6 tier 2, 44 tier 3), all slide decks | `research/raw/decks-capital-pmo.json` |
| Deck library: PMO | 37 (6 tier 1, 5 tier 2, 26 tier 3); 9 slide decks, 28 reports | `research/raw/decks-pmo.json` |

Total: 181 verified records. Strategy and Capital Projects meet the 50-70 target. Management and PMO fall short
even after adding portrait reports as content references (`format: "report"`): public slide-format PMO and
operations decks are rare. Some Strategy records are operations reviews and move to Management at merge (M5).

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

**M0 result (2026-11-01).** Six consulting slides (exec summary with look-ahead, Gantt baseline vs forecast,
5×5 heat map with risk table, cost bridge, RAG dashboard with KPI cards, Harvey-ball options matrix) render from one
scene to HTML and PPTX. Same line breaks everywhere. Measured drift HTML vs LibreOffice: ≤0.5pt vertical after
calibration, ≤2pt horizontal over a full 360pt line (LibreOffice rounds glyph positions to whole pixels). Findings:
- LibreOffice on macOS draws Arial with Liberation Sans (metric-identical) and Georgia with Linux Libertine (not
  compatible). The automated check therefore needs Gelasio installed for Georgia; Arial is the default face throughout.
- First-baseline model for exact line spacing: `baseline = 1.00·pitch − 0.20·size` (fit error ≤0.33pt).
- Icons: 116 Lucide icons (v1.59.0, ISC) converted to custGeom, so they are editable vector shapes in PowerPoint.
- PowerPoint itself is not on the build machine: open `spike/out/v1.pptx` in PowerPoint (Mac/Win) as the manual check.

**Biggest technical risk (before M0):** text-metric parity, specifically baseline offsets and kerning differences between
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

## 7. Brand and templates (core v1 feature)

Decks are built in the brand of the user's company. The house style below is only the fallback.

**Intake asks for this first, every time.** In round 1, before any content questions, the skill asks:
- Whose brand the deck carries: your firm's, or the client's (co-branded is allowed).
- Whether you can share a template deck (`.potx`, or any recent `.pptx` from the company). "Any deck you've
  sent recently works."
- Whether you have brand guidelines (PDF or a link) and the company website.
- Whether there is a deck you like the look of.
If files are already in the project folder or a connected drive, it finds them and confirms rather than asking.

**Order of preference:** template deck, then brand guidelines, then website, then a neutral house theme.
Any assumption it makes about the brand is shown in the playback before it builds anything.

**Template mode (a `.potx` or `.pptx` is supplied).** `template_from_pptx.py` reads the file and writes `brand.json` plus a
template pack:
- **Real master.** The output PPTX reuses the company's own slide master, layouts and theme. A colleague who opens
  it is in their normal template: same footer, logo, page numbers and layout menu.
- **Placeholders.** Titles and footers go into the template's own placeholder positions and text styles, read
  from each layout's geometry and the master `txStyles`.
- **Theme colours.** Colours are written as theme references (`schemeClr`), not hard-coded hex, so later edits stay
  on-brand. The RAG red, amber and green are mapped to the nearest on-brand equivalents, and the skill asks if
  none fit.
- **Theme fonts.** Metrics come from the installed font file. If the font isn't installed, the skill asks for the
  font files or uses a metric-compatible stand-in (Carlito for Calibri, Caladea for Cambria, Liberation for
  Arial/Times) and says so.
- **The layout grid comes from the template.** Content margins, the title area and safe areas are read from the
  layouts, so the consulting components reflow onto the company's grid rather than ours.
- **HTML and PDF match the template too.** Master and layout shapes (logos, rules, coloured bars, footer text,
  images) are parsed into the scene, so the HTML shows the same chrome. Anything the parser can't reproduce
  exactly, such as gradients or effects, is flagged. It is then rendered once as a background image from the
  template, so all three outputs still match.
- **Brand lint.** Checks that only theme colours and fonts are used, that the logo isn't distorted, that nothing
  sits on top of master elements, and that the template's own slide types are used where they exist (section
  divider, agenda).

**Guidelines or website only.** `brand_from_url.py` and the guidelines PDF supply the palette, fonts and logo. The
skill builds a clean master in that identity and produces a one-page brand sheet for confirmation.

**No brand at all.** It uses a neutral consulting house style: white, navy, grey, Arial, thin rules and plain RAG
dots. No firm's names, logos or trade dress are imitated.

**Density setting.** Choose between dense SteerCo pre-reads and sparse presented decks.

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
| M0 ✅ | **Parity spike** (done 2026-11-01) | 6 test slides (dense text, Gantt, heat map, waterfall, table, chart) render identically in Chromium and PowerPoint/LibreOffice, with the diff under threshold. Go/no-go on the architecture. |
| M1 | Engine and 15 core layouts | Scene model, font metrics, PPTX and HTML writers, PDF export, overflow lint |
| M2 | Remaining ~25 layouts + **brand/template mode** | All archetypes in section 5; template pack from `.potx`/`.pptx` (real master reuse, placeholders, theme colours/fonts, master chrome in HTML); brand from guidelines/URL; house fallback |
| M3 | Ingest | XER, MSPDI, XLSX/CSV registers, DOCX, VTT/SRT, PPTX, tested on sample files |
| M4 | Knowledge | `SKILL.md`, interview model, deck-type files (≈36), standards, copy rules, review panel |
| M5 | Library | `decks.json` (50-70 per practice, tiered), `library.md` patterns, `find_decks.py` |
| M6 | Examples | 3 fictional end-to-end engagements, built from raw inputs by the skill itself |
| M7 | Packaging and CI | Installers, manifests, validate workflow, README with screenshots, tested in Claude Code, Codex and Gemini CLI |
| M8 | Release | Create the GitHub repo and push v1.0.0, **only after you confirm** |

---

## 11. Decisions for you

Decided 2026-11-01: name `consulting-deck-studio`; Arial/Georgia (Arial throughout by default); charts as shapes
by default with native charts opt-in; public repo. Design direction from review: plain consulting conventions,
not "designed" slides. That means no icon tiles, cards, pills or banners. Icons are sparse, monochrome and inline.
