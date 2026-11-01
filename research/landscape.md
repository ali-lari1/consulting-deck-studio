# Competitive landscape: consulting-deck agent skill (as of 2026-11-01)

Method: 8 web searches (standard mode), no repo-level verification. Search snippets only; star counts and features are NOT verified against the repos. Items marked [UNVERIFIED] need a direct check. No evidence found on anything "changed since Oct 2026" (searches surfaced nothing dated after mid-2026).

## 1. Existing open-source skills / repos

| Repo | Notes | Format | Approach |
|---|---|---|---|
| seulee26/mckinsey-pptx | ~367 stars (per gittrend/sourcepulse listing, last push 2026-04-24). Claude Code plugin, 40 slide templates, subagent picks template and explains choice | PPTX | Template library |
| sruthir28/enterprise-ai-skills (also skills.sh/sruthir28/mckinsey-claude-skills) | Multi-skill: MECE problem breakdown, claim-style titles, mckinsey-charts. Needs python-pptx, Py 3.9+ | PPTX | Pipeline: structure -> titles -> charts |
| likaku/mck-ppt-design-skill | 5-stage workflow "to avoid sloppy output" | PPTX | Design-system + workflow |
| kgraph57/mckinsey-style-visualization-skill | Hypothesis-led headlines, hex palettes, type rules | charts | Chart styling only |
| wshobson/agents pptx-deck-context | Narrative/design context prep; action-title one of several frameworks; low catalog score (65/100) | n/a | Pre-step only |
| fleurytian / mann1988 awesome-claude-skills "mckinsey-consultant" | Persona-style prompt skill | text | Prompt only |
| skillcreatorai/ai-agent-skills pptx; Anthropic pptx skill | Generic PPTX generation | PPTX | Generic |
| strategyu.co "Claude Code Skills" | Rules: no pies, no takeaway boxes, insight titles | guidance | Opinion/rules |

Observed pattern: nearly all are python-pptx based, single-purpose (style OR charts OR narrative), generic "McKinsey look". No result showed: workstream-specific packs (Capital Projects / PMO), schedule-aware decks, client .potx application, or data-linked project sources. [Based on absence in results; verify with direct GitHub search.]

Sources:
- https://github.com/sruthir28/enterprise-ai-skills
- https://skills.sh/sruthir28/mckinsey-claude-skills
- https://gittrend.io/repo/seulee26/mckinsey-pptx
- https://www.sourcepulse.org/projects/28704884
- https://claudemarketplaces.com/skills/likaku/mck-ppt-design-skill/mck-ppt-design
- https://claudemarketplaces.com/skills/kgraph57/mckinsey-style-visualization-skill/mckinsey-style-visualization
- https://www.claudemarket.ai/skills/wshobson/agents/pptx-deck-context
- https://claudemarketplaces.com/skills/fleurytian/awesome-claude-skills/mckinsey-consultant
- https://strategyu.co/strategy-consulting-aiskills/

## 2. Commercial tools and complaints

Evidence is thin and mostly vendor-authored (Deckary sells a PPT add-in; Prezi/SlidesAI/Gamma are competitors) - treat as biased.
- Copilot in PowerPoint: agentic build/revise GA April 2026 (Rework). Limited to standard PPT chart types; waterfall and Mekko unsupported (Deckary review).
- Gamma: fast, visual; chart support basic, PPTX export limited (Deckary). Web-native, not PPT-native.
- think-cell (~$299/yr listed by Deckary): standard for waterfall/Gantt/Mekko; add-in, not generative.
- General critique (Deckary): AI tools optimize for speed/visuals, not structured thinking, data viz and PPT compatibility needed in consulting.
- Not found: first-hand consultant complaint threads (action titles, brand templates). Recommend a follow-up on Reddit r/consulting, LinkedIn, Wall Street Oasis. Action titles specifically were not covered by any result.
- Not researched in this pass: Plus AI, Beautiful.ai, Prezent, Skywork, Manus, UpSlide, Macabacus, Gemini in Slides.

Sources:
- https://deckary.com/blog/copilot-powerpoint-review
- https://deckary.com/blog/ai-slide-generator
- https://deckary.com/blog/best-ai-presentation-maker
- https://resources.rework.com/tools/ai-tools/best-ai-presentation-tools-2026
- https://prezi.com/blog/client-decks-ai-slide-builder-consultants-2026/
- https://www.slidesai.io/blog/best-ai-tools-for-consultants
- https://gamma.app/explore/content/guides/gamma-for-consultants-creating-polished-strategy-decks-without-a-designer

## 3. Output format reality

Web evidence:
- python-pptx has no native waterfall; ChartEx (waterfall/treemap/sunburst) is an unmerged upstream PR (#778) and open issue (#651); a fork (MHoroszowski/python-pptx PR #57) claims ChartEx write + round-trip [UNVERIFIED]. ChartEx waterfall lives in mc:AlternateContent and needs Office 2016+.
- python-pptx cannot open .potx out of the box (content-type allowlist); workaround: re-save as .pptx or patch content type. Mixing master from one file and layouts from another is not supported (issue #1028). Built-in template has no table/chart placeholder layouts.
- Sources: https://github.com/scanny/python-pptx/issues/778 , https://github.com/scanny/python-pptx/issues/651 , https://github.com/MHoroszowski/python-pptx/pull/57/files , https://github.com/scanny/python-pptx/issues/1028 , https://github.com/MHoroszowski/python-pptx/issues/19

Engineering judgment (not web-sourced, validate by prototype):
- Consultants need editable native PPTX: shapes, tables, native charts with embedded workbook. Images fail because partners/managers edit last-minute. HTML/PDF only as preview.
- stdlib-only (zipfile + string XML) is feasible: slides are plain XML; native bar/line/pie charts need chart XML + embedded xlsx (xlsx also writable with zipfile). Costs: you own relationship parts, content types, and PowerPoint repair-dialog risk; need a validation loop (LibreOffice render + XML schema check).
- Low-risk native patterns using plain shapes/tables (no chart parts): Gantt = rectangles on a date grid (or stacked bar with invisible first series if a real chart is wanted); RAG table = table with filled cells/ovals; heat map = table with cell fills; waterfall = stacked column with transparent base series (works with standard c:barChart, avoids ChartEx), or rectangles + connectors.
- Client template: ship layout-mapping (layout name -> role) and clone slides into the client's master by selecting layouts by name; accept .potx by rewriting [Content_Types].xml override to the presentation main type; use theme colours/fonts (schemeClr, +mj-lt/+mn-lt) instead of hardcoded values so a swapped master restyles everything.

## 4. Integration sources

- MS Project / P6 file-based MCP servers exist: osama-ata/p6xer-mcp-server (PyP6Xer, 13 tools, uvx), shamshirialireza/p6-mcp (XER + live P6 EPPM, DCMA-14, EV), paulieb89/pyp6xer-mcp, SCurveLabs/longpath (XER + MSPDI + .mpp via MPXJ, S-curve, float), jeffmodeler/project-mcp (MSP, P6, Synchro), HorizunMsProjectMcp (NuGet; .mpp/.xer/MSPDI, no Java).
- Smartsheet: official MCP server GA 2026-03-24; Claude connector in Settings > Connectors.
- Asana: official hosted MCP (GA). Atlassian (Jira/Confluence): official cloud MCP. monday.com: official MCP. Notion: official. (Auth-gated connectors for several of these appear in this environment.)
- Procore, Aconex: nothing found in this pass [gap; check Procore developer portal / Oracle Aconex API]. SharePoint/OneDrive, Google Drive, Granola, Otter, Fireflies, Teams/Zoom: not researched in this pass.
- Easy offline parsing (engineering judgment): XER (tab-delimited text, %T table / %F fields / %R rows - stdlib-parseable), MSPDI XML (Project "Save as XML"), CSV/XLSX exports from Smartsheet/Jira/Asana/Monday, .vtt/.srt transcripts, .docx/.md notes. .mpp is binary - require XML export or MPXJ.
- Recommended design: offline-file-first ingest (XER/MSPDI/CSV/VTT) with optional MCP enrichment, so skill works in any agent.

Sources:
- https://glama.ai/mcp/servers/osama-ata/p6xer-mcp-server
- https://mcpservers.org/servers/shamshirialireza/p6-mcp
- https://glama.ai/mcp/servers/paulieb89/pyp6xer-mcp
- https://glama.ai/mcp/servers/SCurveLabs/longpath
- https://github.com/jeffmodeler/project-mcp
- https://nuget.org/packages/horizunmsprojectmcp
- https://www.smartsheet.com/content-center/smartsheet-mcp-server-now-generally-available
- https://developers.smartsheet.com/ai-mcp/smartsheet/changelog.md
- https://thedigitalprojectmanager.com/partner-spotlight/smartsheet/smartsheet-mcp/
- https://workmanagementhub.com/claude-ai-project-management/
- https://toolradar.com/blog/best-mcp-servers-project-management

## 5. Skill distribution standards

- Agent Skills open standard (SKILL.md: YAML frontmatter + Markdown, optional scripts/references), published by Anthropic at agentskills.io, Dec 2025; spec at https://agentskills.io/specification ; ~40 supporting products listed by June 2026 (secondary source). Validate with `npx skills-ref validate ./skill`.
- `npx skills add <owner/repo | url | path>` (Vercel skills CLI / skills.sh), `-g` for global.
- `gh skill install <repo> [skill[@version]]` exists: GitHub CLI >= v2.90.0, public preview (changelog 2026-04-16/17), aliases `gh skill add`, `gh skills add`; flags `--agent claude-code`, `--scope user|project`, `--dir`, `--force`; pins by tag/SHA; `gh skill preview` to inspect; publish support. Default agent github-copilot.
- Claude plugin marketplace, Gemini extensions, Codex ~/.agents/skills: not verified in this pass. Not verified: any change since Oct 2026.
- Implication: ship one repo with `skills/<name>/SKILL.md` + scripts, tagged releases (gh pins by tag), plus plugin manifest for Claude marketplace.

Sources:
- https://github.blog/changelog/2026-04-17-manage-agent-skills-with-github-cli/
- https://man.archlinux.org/man/extra/github-cli/gh-skill-install.1.en
- https://mer.vin/2026/04/gh-skill-install-pin-and-publish-agent-skills-from-github-repos/
- https://devtoollab.com/blog/agent-skills-open-standard-guide
- https://developertoolkit.ai/en/developer-scorecard-guide/agent-skills/
- https://pinggy.io/blog/ai_agent_skills/
- https://nevercodealone.de/de/vibe-coding/vibe-coding-best-practices/skills-sh-agent-skills-ki-coding-agents-2026

## Open follow-ups
1. Fetch top repos (seulee26, likaku, sruthir28) to confirm stars, licence, chart nativeness (chart parts vs images).
2. Consultant-voice complaints (Reddit/WSO/LinkedIn).
3. Procore/Aconex, SharePoint, Granola/Otter/Fireflies connector status.
4. Prototype stdlib chart part + embedded xlsx and render check in LibreOffice/PowerPoint.
5. Confirm Codex/Gemini/Claude marketplace install paths and any post-Oct-2026 changes.

---

## 2b. Gap fill: commercial tools (added)

Still vendor-heavy; no Reddit/HN/Fishbowl threads surfaced via the search tool (site-restricted search not available). Practitioner sentiment remains a gap.
- Plus AI: native add-in for PowerPoint and Google Slides; positioned for consultants; ranked near top by Deckary/Prezi (both biased). https://plusai.com/blog/best-ai-tools-for-consultants , https://plusai.com/use-cases/ai-for-consultants
- think-cell Assist (AI): drafts titles, summarises slides, generates charts; "70% chart-time saving" is a vendor claim. think-cell output uses PowerPoint's own charts and shapes (editable, sharp at any zoom). https://www.think-cell.com/en/resources/content-hub/think-cell-assist-7-ai-tools-to-improve-your-powerpoint-slides , https://www.think-cell.com/en/resources/manual/basicconcepts
- Copilot: competitors call output "functional but short of consulting quality"; an Indezine interview (via Flevy) calls it transformative for consultants - opinion split. https://deckary.com/blog/copilot-powerpoint-review , https://flevy.com/blog/wp-json/wp/v2/posts/14760
- Prezent: enterprise; applies company fonts/colours/layouts automatically (one French roundup, https://ahaslides.com/fr/blog/ai-powerpoint). UpSlide, Beautiful.ai, Gemini in Slides: no usable results. Mekko Graphics internals: not found.
- Takeaway (judgment): the recurring positive differentiators are brand-template adherence and native editability; the recurring negatives are generic structure and weak charts. Follow up with direct Reddit/HN/Fishbowl reading.

## 6. HTML / PDF / PPTX parity

### (a) Rendering identical geometry
Web evidence is thin here; most of this is engineering judgment and must be proven by prototype.

Single layout model (judgment):
- One intermediate "scene" JSON: slide = list of boxes in EMU (914400/in; 13.333x7.5in = 12192000x6858000). Two emitters: HTML (position:absolute; left/top/width/height in pt or EMU/12700; font-size in pt) and PPTX (a:off/a:ext, sz in 1/100 pt). No flow layout in either target; all layout decided once in Python.
- Text: precompute line breaks yourself and emit one paragraph per visual line (or explicit <a:br/>/<br>), so neither renderer wraps. PPTX: `<a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0"><a:noAutofit/></a:bodyPr>`; HTML: `white-space:pre; overflow:visible; padding:0; margin:0`. This removes the wrapping divergence documented in LibreOffice bugs (below).
- Metrics: read TTF `head.unitsPerEm`, `cmap`, `hmtx` (+ `hhea` advance, `kern`/GPOS for kerning) with `struct` (stdlib). Caveat: browsers apply GPOS kerning and ligatures by default; PowerPoint applies kerning only when `kern` attr set (`<a:rPr kern="0">` vs `kern="1200"`), and no ligatures. For parity: HTML `font-kerning:none; font-variant-ligatures:none; text-rendering:geometricPrecision`, and PPTX `kern="0"`, or compute with kerning and set both on. Hinting/rounding means sub-pixel width drift, so leave ~1% slack and left/centre/right-align by box edge, not by measured width.
- Line height: PowerPoint `<a:lnSpc><a:spcPts val="N00"/>` (exact, in 1/100 pt) ↔ CSS `line-height:Npt`. Exact line spacing is safest since both then ignore font ascent/descent metrics for pitch, but first-baseline position still differs: PowerPoint places the baseline within the exact line box using the font's ascent/descent proportion; CSS uses half-leading. Fix by calibration: render a test slide per font in both targets, measure baseline offset as a fraction of em, and apply a per-font y-correction in the emitter (judgment; verify).
- Letter spacing: CSS `letter-spacing:Xpt` ↔ `<a:rPr spc="X*100">` (1/100 pt). Paragraph spacing: `spcBef`/`spcAft` spcPts ↔ margins; set to 0 and place each paragraph explicitly.
- Reported LibreOffice mismatches that justify exact/explicit settings: at-least vs exact line spacing plus unexpected 6pt after-paragraph; proportional spacing mapped to "single"; autofit mishandling; text-box wrapping differing even with identical fonts; table-cell wrap differences traced to hyphenation. https://www.libreoffice.org/bugzilla/show_bug.cgi?id=103476 , https://www.libreoffice.org/bugzilla/show_bug.cgi?id=136231 , https://bugs.libreoffice.org/show_bug.cgi?id=139599 , https://www.libreoffice.org/bugzilla/show_bug.cgi?id=154399 , https://bugs.libreoffice.org/show_bug.cgi?id=123103 , https://www.libreoffice.org/bugzilla/show_bug.cgi?id=95953 (several old; recheck status on current LO)
- Avoid PPTX tables for parity (cell padding, row auto-grow, wrap vary by app). Use positioned rectangles + text boxes for grids; offer tables only in a non-parity "editable table" mode. (judgment)

Fonts:
- PowerPoint embeds TrueType only; fonts with restrictive OS/2 fsType embedding flags will not embed; check the licence. Sources conflict on Mac: older guidance says Mac PowerPoint can't embed or read embedded fonts; newer guide describes a Mac embed option; Indezine says embedded fonts won't work on Mac, tablet or phone. Keynote: no embedding. Google Slides: no embedding, but it supports most Google Fonts natively. https://pptfaq.com/FAQ00076_Embedding_fonts.htm , https://www.indezine.com/products/powerpoint/learn/textandfonts/can-this-font-be-embedded.html , https://www.indezine.com/products/powerpoint/learn/textandfonts/alternatives-to-safe-fonts.html , https://slidor.fr/en/blog/comment-incorporer-des-polices-dans-powerpoint , https://docs.aspose.com/slides/python-net/embedded-font/index.md , https://nusupport.nebraska.edu/TDClient/33/Portal/KB/PrintArticle?ID=390
- The `embeddedFontLst` XML (p:embeddedFontLst/p:embeddedFont with regular/bold/italic r:id to .fntdata parts; .fntdata is an obfuscated/compressed EOT-like blob) was NOT confirmed by sources - prototype before promising. [UNVERIFIED]
- Recommendation: default to fonts present everywhere (Arial, Calibri/Cambria on Office installs, Georgia, Times New Roman, Verdana) and measure with those exact TTFs (note Arial vs Liberation Sans/Helvetica metric-compatibility: LO and Linux substitute Liberation fonts, which are metric-compatible, but Mac may substitute Helvetica). Treat embedding as an opt-in for OFL fonts (e.g. Inter) on Windows PowerPoint only, with a documented Mac/Keynote/Slides caveat. Always ship the HTML/PDF as the visual source of truth.

### (b) Charts: grouped shapes vs native chart parts
- think-cell uses PowerPoint's own charts and shapes, kept data-driven (vendor). That implies the market leader accepts app-rendered charts but controls layout precisely via an add-in at runtime; a static generator cannot do that. https://www.think-cell.com/en/resources/manual/basicconcepts , https://deckary.com/blog/think-cell-review . Mekko Graphics internals: not found.
- Native c:chart parts: layout of axes, legends, label placement and gap/overlap are computed by each app (PowerPoint, LibreOffice, Keynote, Google Slides differ); no HTML equivalent matches pixel for pixel. High parity risk, high data-editability.
- Grouped shapes (rect/line/text per bar, axis, label): exact parity across HTML, PPTX, PDF, and fully editable as shapes, but not data-editable. Judgment: for a "100% match" hard requirement, make drawn-shape charts the default, and optionally embed the data as an adjacent hidden/notes table or custom XML so a user can regenerate. Offer a `--native-charts` flag with a warning, for where data editing outranks parity.
- Waterfall/Gantt/heatmap/RAG all trivially drawn as shapes.

### (c) Verification
- Pipeline: PPTX -> `soffice --headless --convert-to pdf` -> `pdftoppm -png` (or `soffice --convert-to png` for slide 1 only); HTML -> Chromium headless screenshot per slide at fixed viewport (13.333in x 96 = 1280x720 CSS px, deviceScaleFactor chosen to match). Diff the PNGs.
- Stdlib-only PNG decode is feasible (zlib + defilter filters 0-4; ~60 lines); compute per-pixel abs diff, report % pixels over threshold plus bounding boxes; Pillow/numpy optional for speed and for writing a diff image. (judgment)
- Caveat: LibreOffice is not PowerPoint. It is a proxy only; text anti-aliasing and Impress layout quirks produce false diffs/false passes (see bugs above). Real fidelity needs a PowerPoint (or Keynote/Slides) render, which cannot be automated headlessly on Linux; use a human spot-check on a calibration deck. Also gate on tolerance (e.g. <0.5% pixels beyond 32/255 after 1px blur) rather than exact equality.
- Also verify structurally (no rendering): per text box, assert `wrap="none"`, no autofit, computed width <= box width; fail the build otherwise.

### (d) PDF source
- From HTML via Chromium print-to-PDF: deterministic, embeds subset fonts, vector, exact CSS geometry, identical to what you see in HTML. It is the PDF of the HTML, not of the PPTX.
- From PPTX via LibreOffice: shows what LO thinks the PPTX looks like (known divergences); from PowerPoint (Export as PDF, Windows/Mac): the faithful rendering of the PPTX as the user's client sees it, but not automatable in CI.
- Recommendation: ship the HTML-Chromium PDF as the canonical PDF (page size 13.333x7.5in, `@page{size:13.333in 7.5in;margin:0}`), and use LO-PDF only as an automated regression oracle for the PPTX against it. Judgment; no web source.

### Recommended parity architecture (summary)
Scene JSON in EMU -> measurer (stdlib TTF hmtx/cmap, kerning policy matched in both targets) pre-breaks every line -> three emitters: HTML (absolute, white-space:pre), PPTX (noAutofit, wrap=none, zero insets, exact line spacing, spc letter-spacing, charts as grouped shapes, theme colour/fonts), PDF (Chromium from the HTML). CI gate: soffice->PNG vs Chromium->PNG diff with tolerance and structural asserts. Cross-platform safe fonts by default; optional embed for licensed-OK fonts, Windows-only. Caveat: "100%" can only be guaranteed vs the HTML/PDF and LibreOffice; PowerPoint/Keynote/Slides need a human calibration check.
