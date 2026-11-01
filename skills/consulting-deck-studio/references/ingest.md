# Inputs and linking to a project

Read what the user already has before asking anything. Everything runs offline with the Python standard library.
All outputs land in `<project>/research/inputs/`.

## Reading files

```
python3 SKILL_DIR/scripts/ingest.py <project> <file> [<file> ...]
```

| File | What you get | Notes |
|---|---|---|
| `.xer` (Primavera P6) | Activities: WBS, planned (target) vs forecast vs actual dates, float in days, critical flag, logic | Also schedule-quality checks: missing logic, negative float, float over 44 days, past forecasts not actualised |
| `.xml` (MS Project, "Save As > XML") | The same structure, with baseline 0 as planned | `.mpp` is binary: ask the user to save it as XML |
| `.xlsx` / `.csv` registers | Each sheet's columns mapped to standard fields, and its kind guessed: `risk`, `raid`, `benefits`, `milestones`, `cost` or `table` | Text ratings (Very high .. Very low, percentages) become 1-5. Unmapped columns are kept under `extra`. **Read the "mapped" line and check it.** |
| `.vtt` / `.srt` / transcript `.txt` | Speakers and turns, plus candidate decisions, actions, risks, numbers and dates | Exports from Teams, Zoom, Otter, Granola and Fireflies all work |
| `.docx` / `.md` / `.txt` notes | Text with headings and tables, plus candidates | |
| `.pptx` (previous deck or template) | Per-slide title, text and notes | Use last period's deck for wording, structure and what was promised |

**Candidates are pointers, not facts.** Read each one in context. Every number or claim that goes on a slide gets a
row in `facts.md`, citing its file and the line or speaker.

## Turning files into slide data

```
python3 SKILL_DIR/scripts/ingest.py <project> --emit gantt        research/inputs/<x>.schedule.json
python3 SKILL_DIR/scripts/ingest.py <project> --emit lookahead    research/inputs/<x>.schedule.json
python3 SKILL_DIR/scripts/ingest.py <project> --emit timeline     research/inputs/<x>.schedule.json
python3 SKILL_DIR/scripts/ingest.py <project> --emit risk-heatmap research/inputs/<x>.table.json [--prev <last period's json>] [--top 6]
python3 SKILL_DIR/scripts/ingest.py <project> --emit raid-log     research/inputs/<x>.table.json
python3 SKILL_DIR/scripts/ingest.py <project> --emit benefits     research/inputs/<x>.table.json
```

Each emit writes `research/emit/<layout>.json`. Pull it into a slide with `data_from:`. Inline JSON on the slide
overrides it, which is where takeaways and panels go:

```
# Systems integration and trial running now drive the handover date
layout: gantt
data_from: research/emit/gantt.json
```

A file can also fill one key of another layout: `data_from: research/emit/lookahead.json as lookahead` on a
`status-summary` slide. The `_derivation` key in each emitted file records how values were computed: the RAG rule,
the selection rule and the period compared. Cite it in `facts.md`.

## Linking a project: monthly status reports

```
python3 SKILL_DIR/scripts/init_project.py <project> --name "Programme" --practice pmo --deck status-report \
        --source path/to/schedule.xer path/to/risk-register.xlsx path/to/raid.csv
```

This records the sources and the emits in `<project>/.cds/project.json`. Each period:

1. The user updates the source files, or points `sources` at the new exports. If a connector is available (SharePoint,
   Google Drive, Notion, Smartsheet, Jira, Asana, P6 or MS Project MCP), export from it to those paths.
2. `python3 SKILL_DIR/scripts/ingest.py <project> --refresh` re-reads every source and re-emits every block.
   Heat-map arrows compare against the latest snapshot.
3. `python3 SKILL_DIR/scripts/ingest.py <project> --diff <last period>` lists what changed: milestones moved (days),
   milestones achieved, and risks new, removed or re-scored. Build the "what changed" slide and the status-summary
   text from this.
4. Update the action titles and takeaways, then build.
5. When the deck is final: `python3 SKILL_DIR/scripts/ingest.py <project> --snapshot <YYYY-MM>`.

The RAG policy lives in `project.json` (`rag_policy`), and the default schedule rule is: on plan green, up to 10
working days late amber, later red. **Ask the user for their programme's RAG definitions in the first status report**
and record them there. Never invent a tolerance.
