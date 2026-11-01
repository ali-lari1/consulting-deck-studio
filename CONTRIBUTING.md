# Contributing

Thanks for helping consultants spend less time pushing boxes around.

## Good first contributions
- **Library additions:** a *publicly available* consulting deck or report, with a source URL. Open it and record how
  you verified it. Add it to the matching file in `research/raw/` (same schema), then run
  `python3 tools/merge_library.py`. No leaked or confidential material.
- **Deck-type playbooks:** improve a file in `skills/consulting-deck-studio/references/deck-types/`. Keep the
  structure: purpose, default sequence (layouts), mandatory, ask about, pitfalls.
- **Layouts:** add to `scripts/cdslib/layouts*.py`. Use only scene primitives, so PPTX and HTML stay identical. Document
  the fields in `references/layouts.md`, add the layout to an example, and check `build.py --parity`.
- **Template edge cases:** if a real template ingests badly, open an issue with an anonymised `.potx` (no client
  content) and the output of `template_from_pptx.py`.
- **Readers:** new input formats in `scripts/cdslib/ingest_*.py`, with a fictional fixture in `tests/fixtures/`.

## Rules
- No invented data. Fixtures and examples are fictional and labelled as such.
- Standard-library Python 3.8+ only, and no network access at build time.
- Keep `SKILL.md` under 250 lines. Put detail in `references/`.
- Keep the frontmatter portable (`name`, `description`, `license`, `compatibility`, `metadata` only).
- Run `python3 tools/validate.py` before opening a PR. CI runs it too, and every example must build with zero warnings.
