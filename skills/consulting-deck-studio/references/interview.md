# The adaptive interview

The goal is to get what only the user knows, in as few questions as possible, and to ask nothing a file already
answers. There is no fixed questionnaire. Questions are generated from the gap between what this deck type requires
and what you have already found.

## 1. Infer first

Before asking anything, read every input (`ingest.py` output) and extract:

| Infer | Typical sources |
|---|---|
| Client, programme, sponsor, SRO | Notes header, SOW, previous deck title slide, schedule project name |
| Deck type and practice | The user's words, previous deck, file mix (a .xer plus a risk register usually means a status or schedule review) |
| Audience and setting | Meeting invites, transcript speakers, "SteerCo"/"Board" in notes |
| Reporting period, as-of date | Schedule data date, register dates, transcript date |
| Decision(s) needed | Transcript decision candidates, "approve/agree/sign off" in notes, gate in the cycle |
| Last period's RAG and messages | Previous deck (`.pptx` ingest), `.cds/history` snapshots |
| Numbers | Registers, schedule, cost reports. Each one goes into `facts.md` with its source |
| Sensitivities | "concern", "escalate", disputes, a sponsor under pressure |
| Brand | Template in the folder, logo files, company website |

Mark each inference **high**, **medium** or **low** confidence.

## 2. Play back

Open with a short playback the user can correct in one line:

> Here is what I have. Northline Rail, October SteerCo pack (from the P6 data date and the 28 Oct transcript).
> The decision is the £14m contingency drawdown (*high*: Priya says "the decision we need" at 00:30). Audience is the
> SteerCo, chaired by the SRO (*medium*). The status is red on schedule and amber on cost (*medium*: computed from the
> schedule, not stated by anyone). Brand: none found. Correct anything that's wrong.

## 3. Ask only what changes the storyline

Rank the gaps by **impact × uncertainty**: low-confidence items that would change the governing thought, the section
order or a RAG status come first. If two possible answers would produce the same slides, don't ask.

Rules:
- **3-5 questions per round**, numbered, each with a default the user can accept ("Default: presented, 12 slides").
- Use multiple choice where the options are known, and leave one open "anything I should know?".
- Ask about facts and past events, not preferences: "What happened when this went to the last SteerCo?" beats "How
  should we frame it?". Except for sensitive items, where you ask how to frame, never whether to include.
- **Conflicts get flagged, not resolved silently:** "The cost report says EAC £1,420m, the dashboard says £1,412m.
  Which is current?"
- At most two rounds before the ghost deck. The ghost deck is itself the best question: people react to a draft
  faster than they specify one.

### Always covered (unless the files already settle them)
1. **Brand:** whose brand, and is there a template deck (`.potx`/`.pptx`) or guidelines? (`brand.md`)
2. **The decision:** what should the audience decide, approve or do afterwards? If nothing, is it for information,
   alignment or discussion?
3. **The room:** who decides, who is sceptical, what do they already know?
4. **Format:** presented or pre-read, the time slot, and any slide limit.

### Branch on the deck type
Take the next questions from the playbook in `references/deck-types/`, and only the ones still unanswered.

| Deck type | Typical follow-ups |
|---|---|
| Status report / SteerCo | RAG policy and tolerances (ask once, store in `.cds/project.json`). Which baseline is current? Reporting period. Achievements since last time. Escalations. |
| Gate paper / business case | Which gate and framework (Gateway, internal policy)? Estimate class. Confidence level the budget is set at (P50 or P80). Options considered. The approval being sought. |
| Cost or schedule review | Baseline vs forecast source. Contingency held, and at what level. Known claims. Tolerance for re-baselining. |
| Risk review | Scoring scale and thresholds. Risk appetite. Inherent vs residual. QRA availability. |
| Strategy | The question in one sentence. The leading hypotheses. Options already ruled out. What would make the board say no? |
| Diagnostic / cost review | Baseline year and scope. Savings target. Benchmark peer set. What has been tried before? |
| Operating model / org | Design principles agreed? Constraints (headcount, unions, location). Who must sign off? |
| Transformation / PMI | Value at stake and phasing. Governance forum. Day-1 must-haves. |

### Decision prompts (when the decision is fuzzy)
- "After the meeting, what will be different if it goes well?"
- "Who has to say yes, and to what exactly?"
- "What will they ask that we can't yet answer?"
- "What does it cost if nothing is decided this month?"

## 4. Stop

Stop asking when the remaining unknowns would not change the storyline. Those become `[[placeholders]]` on slides
and rows in `facts.md` with status `placeholder`, and the delivery summary lists them.

## Recurring reports

When `.cds/project.json` and snapshots exist, the interview shrinks to:
1. "Here's what changed since <last period>", from `ingest.py --diff`. "Anything else that happened that isn't in
   the files?"
2. "Any new decisions or escalations for this SteerCo?"
3. "Has the RAG policy or the baseline changed?"
