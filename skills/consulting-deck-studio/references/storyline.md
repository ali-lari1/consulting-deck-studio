# Storyline: from the question to a ghost deck

## The pyramid, answer first
- **Governing thought:** one sentence that answers the audience's question, including the decision or action asked
  for. Everything in the deck traces back to it. Write it in `brief.md` before any slide.
- **Supporting points:** under the governing thought, usually 3 (2-5) points, each one idea, grouped and ordered by
  time, structure or importance, never at random. Each point becomes a section, and its sentence becomes the
  section's opening title.
- **Vertical logic:** each level answers "why?" or "how do you know?" for the level above. A reader can stop at any
  depth.
- **Horizontal logic:** the points at one level form either a deductive chain (because A, and B, therefore C) or an
  inductive group of like items (three reasons, three options).
- **MECE:** groupings must not overlap and must cover the question. Test it: could one item sit in two groups? What
  is missing? An "other" bucket holding more than about 10% means the cut is wrong. (MECE is a tool, not a religion:
  allow overlap where forcing a cut would hide something important, and say so.)

## Opening the deck: SCQA
For the executive summary, and the opening of each section:
- **Situation:** uncontested context, in one sentence.
- **Complication:** what changed, or the tension, in one sentence.
- **Question:** usually implicit.
- **Answer:** the governing thought, then the ask.

Senior audiences get the answer on page 2 or 3. Use the `exec-summary` layout (dot-dash: bold statements on the left,
2-4 supporting facts each on the right) or `status-summary` for PMO decks. The executive summary mirrors the section
titles one to one. It states the answer, not the agenda.

**Deductive or inductive?** When the audience is neutral or supportive, a deductive chain is fine. When the
conclusion may be resisted, lead with grouped evidence (inductive). Either way, state the answer first for senior
readers.

## The ghost deck (the approval gate)
1. Write every slide's action title and layout in `deck.md`, with no data yet.
2. `build.py <project> --outline` prints `# | layout | title`. Paste it into `brief.md`.
3. Run the two tests:
   - **Horizontal:** read only the titles, top to bottom. Is it the whole story, in order, with no gaps or repeats?
     Does each title answer the question raised by the one before it?
   - **MECE:** list the section titles. Do they overlap? Is anything missing?
4. Tag each slide with the evidence it needs (which file, which number) and check that `facts.md` can supply it. A
   slide whose proof doesn't exist yet becomes a hypothesis to test or an open question, not a claim.
5. Show the outline to the user and get a yes or edits before filling slides.

## Section structure (default)
1. Title
2. Executive summary (the answer and the ask)
3. Context and scope (only if the audience needs it; often a single slide or none)
4. Findings or status, by section. Each section opens with an agenda slide (with `active`) or a `section` divider
   whose title *is* the section's message.
5. Recommendation or options
6. Implementation, risks and next steps, each with an owner and a date
7. Decisions requested (the `decisions` layout). Nothing new appears on the final slide.
8. Appendix: method, full registers, definitions (RAG, scoring scales, estimate class), detailed data. Appendix slides
   still have action titles, and main slides point to them ("see p.24").

## SteerCo and board packs: decisions first
Use this order: decisions needed → overall status and RAG → what changed since last time → escalated risks and issues →
look-ahead → financials → detail in the appendix. Label each agenda item **Decide**, **Discuss** or **Note**. Allow
30-60 minutes and 8-15 main slides.

## Pre-read or presented

| | Pre-read (reading deck) | Presented |
|---|---|---|
| Words per slide | 80-150, self-explanatory | 30-60; the speaker adds the rest (put it in the notes) |
| Length | 20-40 slides acceptable | 8-15 main slides plus appendix |
| Titles | Carry the full story, with callouts on exhibits | Carry the full story, plus the verbal narrative |
| Decisions | Stated on the slide | On a decision slide, timed in the agenda |

## Flow between slides
- **So-what chaining:** slide N+1 answers the question slide N raises. Use connectives ("As a result", "However")
  sparingly.
- **Dividers carry the section's message**, not just its name.
- **Parallel phrasing** for titles in the same section makes the story scannable.
- **No dead ends:** every finding leads to an implication, a recommendation or an explicit "no action needed".

## Working sessions (a different genre)
Titles can be questions. Lay the options out side by side, label straw men "Strawman", and leave room to
annotate. Capture the outputs afterwards as decisions and actions.
