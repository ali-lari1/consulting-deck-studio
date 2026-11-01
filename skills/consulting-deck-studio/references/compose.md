# Composing with other skills and connectors

Nothing here is required. The skill works with Python 3 alone. When these are available, use them and say so in one
line.

## Inputs
| Need | Use if available | Fallback |
|---|---|---|
| Files in SharePoint, OneDrive, Google Drive, Notion, Confluence, Box | The agent's connector (MCP or built-in) to **find and download** the schedule, registers, notes and last deck into `<project>/inputs/` | Ask the user to drop the files in the project folder |
| Smartsheet, Jira, Asana, monday.com, MS Project, Primavera P6 MCP servers | Export to CSV/XLSX/XML via the connector, then `ingest.py` | Ask for an export (CSV, MSPDI XML, XER) |
| Meeting transcripts (Teams, Zoom, Otter, Granola, Fireflies) | The tool's export or connector to fetch the `.vtt`, `.srt` or `.txt` | Ask the user to paste or upload |
| Scanned PDFs, PDF reports | A PDF skill or reader to extract text and tables | Ask for the source file |
| Market and competitor facts (strategy decks) | Web search or research tools. **Cite every number with source and date in `facts.md`** | Placeholders, plus a list of data to request |

Never paste client files into a third-party service the user hasn't already connected.

## Production
| Need | Use if available | Notes |
|---|---|---|
| Humanised copy | A humanizer skill | Run titles, takeaways and notes through it, then check that no number or claim changed |
| Unusual PowerPoint edits (animations, embedded objects, merging into an existing deck) | A PPTX skill | Do the edits on a **copy** of `deck.pptx`. The original stays the source of truth because it matches the HTML and PDF |
| Editable native charts | `build.py` writes shape-drawn charts so the formats match exactly | If the user insists on chart objects with data sheets, say they may render slightly differently, then use a PPTX skill on a copy |
| Sharing | The agent's artifact or document tools for the HTML | `deck.html` is a single self-contained file |

## Review
If the harness supports sub-agents, run the review panel (`review.md`) as parallel sub-agents, one per reviewer. Give
each one only the deck files and the brief.
