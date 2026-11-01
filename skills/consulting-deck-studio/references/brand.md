# Brand and templates

Every deck carries the brand of the company presenting it: the user's firm, the client, or both. Settle the brand
**before** writing slides, because the template's grid decides how much fits on each slide.

## Ask first (round 1 of the interview, every time)

1. "Whose brand should this deck carry: your firm's or the client's?"
2. "Can you share a template deck? A .potx, or any recent .pptx from the company, works. I'll build on its real
   master, so the logo, footer and layouts are theirs."
3. "Do you have brand guidelines or a website I should follow?"

If a `.potx` or `.pptx` is already in the project folder or a connected drive (SharePoint, Google Drive, Notion),
find it and confirm it rather than asking. Keynote and Google Slides templates must be exported to `.pptx` first.

## Order of preference

| You have | Run | Result |
|---|---|---|
| A template deck | `python3 SKILL_DIR/scripts/template_from_pptx.py <file> <project>` | The output PPTX uses the template's own masters, layouts, theme colours and fonts. Titles and slide numbers are real placeholders. HTML and PDF show the same graphics. |
| Guidelines or a website | `python3 SKILL_DIR/scripts/brand_from_url.py <url> --out <project>/research/site.json`, then `python3 SKILL_DIR/scripts/brand_init.py <project> --site <project>/research/site.json [--logo logo.png] [--primary #hex] [--heading-font F --body-font F]` | House layouts in the brand's colours and fonts, with the logo top-right |
| Nothing | (nothing) | The neutral house style: white, navy and grey, Arial, plain RAG |

Both scripts write `<project>/brand.json`, which `build.py` picks up automatically. Read their output aloud to the user
(colours, fonts, layouts chosen) and ask them to confirm.

## What to tell the user, and when to ask

- **Font missing.** If the script prints `MISSING`, ask for the font files (`.ttf`/`.otf`) to put in `<project>/fonts/`.
- **Stand-in font.** If it prints `STAND-IN`, say that layout uses a metric-compatible substitute (for example
  Carlito for Calibri) and the PPTX still names the real font.
- **Template not 16:9.** If the template is 4:3 or another unusual size, offer `--brand-only`. That takes the colours
  and fonts but keeps the house grid.
- **Smaller content area.** A template's content area is often smaller than the house grid. Expect more `LayoutError`s
  and titles stepped down 1-2pt. Fix them by cutting words, not by asking for smaller type.
- **RAG colours.** If the brand has no usable red, amber and green, keep the conventional ones and say so. RAG must
  stay legible.
- **Light primary colour.** `brand_init.py` darkens a primary colour that is too light for titles, and reports it.
  Show the user the result.

## Never

- Never imitate another firm's brand, such as McKinsey, BCG, Bain, Deloitte, PwC, EY or KPMG, unless the user *is*
  that firm and supplied its template.
- Never pull a logo from the web for a client without the user's say-so. Ask for the file instead.
