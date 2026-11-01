# Third-party notices and credits

Consulting Deck Studio is original work under the MIT licence.

| Component | Licence | Use |
|---|---|---|
| [Lucide](https://lucide.dev) icons (lucide-static 1.59.0) | ISC (see `skills/consulting-deck-studio/assets/icons/lucide/LICENSE`) | 116 SVG icons bundled and converted to vector paths (`assets/icons/icons.json`) |
| `brand_from_url.py`, from [pitch-deck-studio](https://github.com/ali-lari1/pitch-deck-studio) | MIT (same author) | Brand extraction from a website |
| Font metrics for Arial, Georgia and Verdana | n/a: facts about the fonts (advance widths and vertical metrics), not font software | Deterministic line breaking. No font files are bundled. Fonts come from the user's system, or from metric-compatible open fonts (Liberation, Carlito, Caladea, Gelasio) |
| Chromium, LibreOffice | Their own licences; called if installed, never bundled | PDF export, contact sheets, the PPTX/HTML parity check |

**Ideas, not code.** While planning, we surveyed open-source "consulting slides" skills (for example
seulee26/mckinsey-pptx, sruthir28/enterprise-ai-skills, likaku/mck-ppt-design-skill). No code or text was taken from
them. The craft conventions here (pyramid principle, MECE, action titles) are long-standing practice, credited in
`references/storyline.md`.

**Standards** are cited in `references/standards.md`: GAO-16-89G, GAO-20-195G, AACE 18R-97, the GOV.UK Gateway
toolkit (NISTA), ANSI/EIA-748 and PMI PMBOK. No standard text is reproduced beyond short paraphrase.

**The deck library** (`data/decks.json`) records facts about publicly available decks and reports: their sequence,
structure and design notes, with links to the original publishers. It doesn't reproduce their content. All rights in
those documents belong to their owners.
