# Copy: consulting precision, human voice

Readers are senior and short of time. They trust copy that is specific, plain and sourced, and they stop trusting it
the moment it sounds generated. Built on the GOV.UK style guide (gov.uk/guidance/style-guide), The Economist's style
guide, and Wikipedia's "Signs of AI writing" (en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), accessed November
2026.

## Rules
1. **Lead with the point.** The first words of a title, bullet or note carry the message.
2. **Be specific.** Use numbers with units and dates, named owners, and the actual system or document. Replace "a
   number of", "significant" or "various" with the figure.
3. **Use plain words.** "Use", not "leverage". "Help", not "facilitate". "Start", not "commence". "About", not
   "approximately".
4. **Use active voice and real subjects:** "The supplier missed drop 4", not "Drop 4 was not achieved".
5. **Keep sentences short:** 15-20 words in bullets, 25 at most anywhere. One idea per sentence.
6. **State the uncertainty once and precisely:** "P80 is £446m", not "costs may potentially increase somewhat".
7. **Define every acronym on first use** in each section, or in the appendix glossary (SPI, EAC, QRA, SRO, IV&V).
8. **Use British or American spelling to match the client,** consistently.
9. **Name numbers consistently:** £14m, £1,420m, 3.0%, 15 May 2027. Don't mix "15/05" and "May 15".
10. **Write speaker notes the way you'd say them.** Contractions are fine, and so is "we".

## Phrases to cut or replace with a fact (lint flags these)
- **AI tells:** delve, underscore, showcase, foster, leverage, harness, unlock, elevate, navigate the…, streamline,
  tapestry, testament to, realm, landscape (figurative), journey, pivotal, crucial, vital, robust, seamless, holistic,
  cutting-edge, game-changer, transformative.
- **Throat-clearing:** it is important to note, it's worth noting, in today's…, ever-changing, at its core, when it
  comes to, in order to (use "to"), moving forward, going forward, at the end of the day.
- **Consulting bloat:** synergies, best-in-class, world-class, paradigm shift, low-hanging fruit, boil the ocean,
  move the needle, circle back, deep dive, touch base, bandwidth, value-add, thought leadership. Also "end-to-end"
  unless literal, and "optimise" or "drive" without a metric.
- **Structure tells:** "not only… but also"; "from X to Y" scope sweeps; three adjectives for rhythm; "Whether you're
  A or B"; closing with "In conclusion", "Overall" or "Ultimately"; a "Key takeaways" header on every slide.
- **Inflation:** significant (without a number), substantial, remarkable, groundbreaking, vibrant, stunning.
- **Hedges:** may potentially, could possibly, somewhat, relatively (without a baseline).
- **Punctuation:** em dashes (rewrite as two sentences or use a colon), exclamation marks, emoji.

## Before and after

| Before | After |
|---|---|
| Schedule update | Handover has moved six weeks to 15 May 2027 because systems integration slipped |
| Leveraging synergies across workstreams to unlock significant value | Combining the three procurement teams saves £4.2m a year from 2028 |
| It is important to note that there are a number of risks going forward | Two risks moved into red this month: signalling software and Christmas possessions |
| Robust governance framework to drive holistic transformation | One SRO, one monthly committee, and a weekly savings tracker |
| Costs may potentially increase somewhat | P80 cost is £446m, £16m above the approved budget |
| Key stakeholders were engaged | We interviewed 34 staff, including all 12 ward managers |

## Mechanical checks (build.py lint, plus your own pass)
- Titles: 6-28 words, no full stop, no topic labels.
- Banned-phrase scan and em-dash scan.
- Every slide with numbers has a source line.
- No `[[placeholders]]` with `--final`.
- Your pass: read every title aloud. If it sounds like a press release, rewrite it. If a humanizer skill is installed,
  run the titles, takeaways and notes through it, then check that no number or claim changed.
