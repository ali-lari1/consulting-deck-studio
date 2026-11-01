# Changelog

## 1.0.1 (2026-11-02)
- **Gallery:** 8 new example decks (gate paper, independent review, assurance/IV&V, risk review, market entry, growth
  strategy, operating model, post-merger integration), giving 12 deck types with screenshots in `docs/gallery.md`.
  The 8 decks were written by agents following the skill.
- **Fixes they found:**
  - Gantt charts over about 18 months switch to quarter, half-year or year headers.
  - Gantt and table legends can be relabelled (`legend_labels`, `rag_labels`, `legend: false`).
  - Unknown icons are reported as layout errors with suggestions.
  - A waterfall starting at 0 no longer divides by zero.
  - The 2x2 shows its "High" y-axis label, and long axis labels fit.
  - Roadmap milestone labels near the right edge flip left.
  - Waterfall callout numbering is documented.

## 1.0.0 (2026-11-02)
First public release.
- **Engine:** one scene drawn to editable PPTX (raw OOXML) and HTML/PDF with identical line breaks. Calibrated
  baselines, automatic per-font calibration, a LibreOffice/Chromium parity check, and Lucide icons as vector shapes.
- **35 consulting layouts** across PMO, capital projects, strategy and management. SPI, CPI, EAC, P-values,
  benchmark medians and benefit progress are computed, and reconciliation and RACI/weight checks fail the build.
- **Brand:** client template mode (real master and layouts, placeholders, theme fonts and colours, keep-out zones),
  brand from a website and logo, and a neutral house style.
- **Inputs:** P6 XER, MS Project XML, XLSX/CSV registers, VTT/SRT transcripts, DOCX/MD notes and PPTX decks. Emitters
  build Gantt, look-ahead, timeline, heat map, RAID, benefits and "what changed" data, and projects link across
  periods.
- **Knowledge:** an adaptive interview, storyline and ghost deck, slide craft, copy rules, standards, 36 deck-type
  playbooks, and a review panel. Lint covers copy, structure and mandatory content per deck type.
- **Library:** 164 verified public consulting decks and reports, tiered, with `find_decks.py`.
- **Packaging:** installers for 14+ agents, Claude plugin and Gemini extension manifests, and CI.
