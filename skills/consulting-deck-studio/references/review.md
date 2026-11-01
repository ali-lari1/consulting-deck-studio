# Review panel

Run this after the build is clean (no errors, warnings addressed). Use sub-agents if the harness has them, one per
reviewer with only the deck (`deck.md`, `contact-sheet.png`, `facts.md`) and the brief. Otherwise do sequential passes,
re-reading the deck as each reviewer. Each reviewer returns **at most 7 findings**, ranked, each with the slide
number, the problem, and a concrete fix (rewritten title, cut, or added data). Apply the fixes, rebuild, and repeat
once if anything structural changed.

## Who reviews (pick by deck type)

| Deck type | Reviewer 1 | Reviewer 2 |
|---|---|---|
| Status report, SteerCo pack, dashboard | **Sceptical SteerCo chair.** "What do you need from me? Why is this amber not red? What changed since last month? Who owns that?" | **PMO director.** RAG consistency with data, baseline vs forecast present, actions with owner and date, registers reconcile with slides |
| Gate paper, cost or QRA review, recovery plan | **Cost engineer or QS.** Estimate class, price base, P50/P80, contingency vs management reserve, claims excluded, EVM used correctly | **Assurance reviewer (gateway or IV&V).** Is the case evidenced? Are options fairly assessed? Conditions from the last gate? Delivery confidence justified? |
| Strategy, diagnostic, growth, market | **Engagement partner.** Is the answer first and sharp? Is the storyline MECE? Would the CEO repeat the governing thought? | **Sceptical CFO.** Do the numbers reconcile? What's the baseline? What would you need to believe? Where's the downside? |
| Operating model, cost review, transformation | **Engagement partner** (as above) | **Sceptical COO or HR director.** Is it deliverable? People impact? Double-counted savings? Who owns each lever? |
| Every deck | **Copy editor.** `copy.md`: plain words, specific numbers, no AI tells, consistent number formats, acronyms defined, titles 15-25 words that state the takeaway | **Designer.** Contact sheet: one message per slide, alignment and whitespace, highlight colour used once, consistent chrome, nothing decorative, legends and units present, on-brand |

## Checklist every reviewer applies
1. **Horizontal test:** read only the titles. Do they tell the full story with the answer first?
2. **Vertical test:** does each body prove its title, and nothing else?
3. **Numbers:** every number traces to `facts.md`, and the same number is identical everywhere (EAC, dates, counts).
4. **The ask:** the decision is explicit, early, and has an owner and date.
5. **Status honesty:** no RAG contradicts the data; reds and ambers have cause, impact, action, owner and date.
6. **Definitions:** RAG, risk scales, estimate class and the confidence level are stated.
7. **Placeholders:** each open `[[...]]` is listed for the user. None remain in a final deck.

## Scoring (for "review an existing deck" mode)
Score 1-5 on each dimension and show the three biggest fixes first:

| Dimension | 5 looks like |
|---|---|
| Answer first | The governing thought and ask are on page 2 |
| Storyline | Titles alone tell the story; MECE sections |
| Evidence | Every claim sourced; numbers reconcile |
| Exhibits | Each exhibit is the right form and proves its title |
| Status integrity | RAG defined, consistent with data, trended |
| Copy | Plain, specific, human; no jargon or AI tells |
| Design | Clean, consistent, on-brand, legible at 10pt+ |

Present the fixes as before and after titles where possible. That shows the improvement quickly.
