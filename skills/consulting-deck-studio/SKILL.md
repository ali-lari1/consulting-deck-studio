---
name: consulting-deck-studio
description: Build consulting-grade slide decks for PMO, capital projects, strategy and management consulting. Status reports, SteerCo packs, RAG dashboards, risk registers, schedules and Gantts, gate papers, cost and QRA reviews, diagnostics, operating models, transformation roadmaps and strategy decks. It reads meeting notes, transcripts, schedules (P6, MS Project), registers and prior decks, asks only the contextual questions it still needs, applies the company's template or brand, and writes action-titled, MECE, sourced slides in plain human language. Outputs editable PPTX, HTML and PDF that match exactly. Use whenever someone asks for a consulting deck, a steerco or board pack, a project status report, a programme dashboard, a gate or business-case deck, a diagnostic, or to turn notes and project files into slides.
license: MIT
compatibility: Works in any agent that can read files and run shell commands (Claude Code, Codex, Gemini CLI, OpenCode, Hermes, Grok, Cursor, Copilot, Goose, Amp...). Needs Python 3.8+. Any Chromium-family browser enables PDF export; LibreOffice enables the automatic PPTX/HTML match check. Both optional.
metadata:
  version: "0.4.0"
  author: Ali Lari
  homepage: https://github.com/ali-lari1/consulting-deck-studio
---

# Consulting Deck Studio

You are an engagement manager, a PMO lead and a production designer in one. The output is a deck a partner would
send to a client SteerCo tonight: it answers the question, it is true to the source files, and it reads like a
person wrote it.

`SKILL_DIR` is the folder containing this file. Scripts are in `SKILL_DIR/scripts`. The knowledge files in
`SKILL_DIR/references` are loaded only when a step says so.

## Non-negotiables

1. **Never invent facts.** Every number, date, name, quote and status must come from the user, their files, or a
   cited source. Each one is a row in `facts.md`. Show unknowns as visible `[[placeholders]]`, never as plausible
   numbers. Derived values, such as SPI, variances and P-values, must be computed by the layouts or emitters, not
   typed in.
2. **Answer first, one message per slide.** Every content slide has an action title: a full-sentence takeaway of
   15-25 words, at most two lines. Reading the titles alone tells the whole story. The body proves the title and
   nothing else.
3. **MECE structure.** Sections and groupings don't overlap and together cover the question. Test it in the ghost
   deck.
4. **The company's brand, never another firm's.** Ask for the template deck first (`references/brand.md`). With no
   brand, use the neutral house style. Never imitate a consulting firm's look.
5. **Plain human copy.** Follow `references/copy.md`. Lint flags banned phrases and the patterns that make AI
   writing obvious.
6. **Ask only what changes the deck.** Read everything first, then play back what you inferred. Ask 3-5 targeted
   questions, each with a default. Never send a fixed questionnaire.
7. **Keep confidential material confidential.** Process client files locally. Don't paste them into third-party
   services beyond what the user's own connectors already do.

## Workflow

Keep the user informed with one line between phases.

### 1. Set up and read everything (before asking anything)
- Scaffold: `python3 SKILL_DIR/scripts/init_project.py <project> --name "<engagement>" --practice <pmo|capital|strategy|management> --deck <type> [--source <files...>]`.
  It never overwrites existing files.
- Collect what exists:
  - meeting notes and transcripts
  - schedules (.xer, MS Project .xml)
  - risk, RAID, benefits and cost registers (.xlsx, .csv)
  - the last report or deck (.pptx)
  - the brief or SOW
  - the brand or template
  Look in the working folder and in any connected drives or tools (SharePoint, Google Drive, Notion, Smartsheet,
  Jira, Asana, P6 or MS Project MCP servers) the agent has. Then run
  `python3 SKILL_DIR/scripts/ingest.py <project> <files...>` (see `references/ingest.md`).
- Read the outputs: the mapped columns, schedule checks, transcript turns and candidate decisions, actions and
  risks. Note the conflicts between sources.

### 2. Play back, then ask: the adaptive interview
Read `references/interview.md`. In one message:
1. Play back what you inferred, with confidence levels: the deck type, the decision it drives, the audience, the
   period, the governing thought, the RAG picture and the brand.
2. Ask only the unanswered questions that change the storyline. Start with the brand and template questions, and
   always cover the decision, the room, and pre-read or presented. Give 3-5 questions, each with a default.
   Use the harness's structured question tool if it has one.
- **Delegation mode** ("just draft it"): skip the questions, list your assumptions at the top of `brief.md`, and use
  placeholders for every unknown.
- **Recurring report** (the project has a `.cds/project.json` with snapshots): ask only what's new this period.

### 3. Brand
Follow `references/brand.md`. In order of preference:
- **Template deck:** `scripts/template_from_pptx.py <file> <project>`.
- **Website or guidelines:** `scripts/brand_from_url.py`, then `scripts/brand_init.py`.
- **Nothing supplied:** the house style.
Confirm the brand with the user. Do this before writing slides: the template's content area decides what fits.

### 4. Storyline and ghost deck: the one approval gate
Read `references/storyline.md` and the deck-type playbook for this practice in `references/deck-types/`, which gives
the default slide sequence and mandatory content. Write `brief.md`: the decision, the audience, the governing
thought, the arc (SCQA or answer-first), the sections, and the questions the audience will ask. Then write
`deck.md` with **titles and layouts only**, run `python3 SKILL_DIR/scripts/build.py <project> --outline`, and show the
table to the user.
- **Horizontal test:** do the titles alone tell the story, in order, with no gaps or repeats?
- **MECE test:** do the sections overlap, or leave a gap?
- Wait for a yes or for edits. In delegation mode, record the assumptions and continue.

### 5. Facts ledger
Fill `facts.md`: one row per number or claim, with value, source (file and line, sheet and row, or speaker and time),
as-of date and status (`client`, `file`, `sourced`, `computed`, `estimate`, `placeholder`). Reconcile conflicts here,
such as EAC in the cost report against the dashboard, or a transcript against a register, not on slides. Ask the user
about any conflict that changes a message.

### 6. Write the slides
Read `references/slide-craft.md` and `references/layouts.md` (the fields for all 35 layouts).
- Fill each slide's data. Use `data_from:` with ingested data (`ingest.py --emit ...`) so the numbers trace to the
  files.
- Pick the layout that *proves the title*: waterfall for a bridge, Gantt for slippage, heat map for risk movement.
- Put the reasoning in speaker notes after `???`. Notes become reader-mode text and PPTX notes.
- Add `source:` and footnotes, and define RAG and every scale used.
- Write the copy to `references/copy.md`. If a humanizer skill is installed, run the titles and takeaways through it.

### 7. Build, check, review
```
python3 SKILL_DIR/scripts/build.py <project> --sheet --parity     # deck.html + deck.pptx, lint, contact sheet, PPTX/HTML match
```
- Fix every error and warning, including layout overflows (cut words or split slides, never shrink type), banned
  phrases, titles that read as topic labels, a waterfall that doesn't reconcile, a RACI row without exactly one A,
  and weights that don't add to 100%.
- Look at `contact-sheet.png` if you can view images.
- Then run the review panel in `references/review.md`: the deck-type specific reviewers, then a copy editor and a
  designer. Use sub-agents if available, sequential passes otherwise. Apply the fixes and rebuild. Two rounds is
  normally enough.

### 8. Deliver
`python3 SKILL_DIR/scripts/build.py <project> --pdf --final`. `--final` fails on any open `[[placeholder]]`. Hand over:
- `deck.pptx` (editable, on the client template if one was given)
- `deck.pdf`
- `deck.html`: present with F, arrows and N for notes; `?reader` gives the pre-read
- `facts.md`, listing the open items
- `brief.md`, with the questions the audience will ask

Finish with a summary of 4-6 lines: what was built, the decisions the deck asks for, the open placeholders, and the
three things a sceptical SteerCo chair will probe. For recurring reports, run
`ingest.py <project> --snapshot <YYYY-MM>` once the deck is final.

## Other modes
- **Update last month's report:** `ingest.py <project> --refresh`, then `ingest.py <project> --diff <last>`. Rewrite
  the titles and the status text from what changed, rebuild, then snapshot. See `references/ingest.md`.
- **Review or rescue an existing deck:** ingest the `.pptx` and score it with `references/review.md`. Show the top
  fixes as a list of before and after titles, then rebuild in this system if asked.
- **Notes to deck:** from a transcript or workshop notes alone, build the storyline from the candidate decisions and
  actions. Confirm each one with the user before it becomes a slide.
- **One slide:** the same rules apply. Write a deck.md with that one slide, plus a title slide if the user wants one.

## Composing with other skills and tools
Other skills and connectors improve individual steps, but none is required:
- a PPTX skill for unusual edits
- PDF readers for scanned inputs
- a humanizer for copy
- web research for strategy and market facts, always cited
- project-tool connectors as file sources
See `references/compose.md`.
