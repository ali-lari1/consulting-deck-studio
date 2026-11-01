---
deck: Calder Valley Homes: target operating model
context: Calder Valley Homes  |  Board and Executive Team  |  November 2026
tracker: Summary, Principles, Design, Decision rights, Transition
sticker: Draft for discussion
deck_type: operating-model
source: Calder Valley Homes HR and finance data, October 2026; staff workshops; transformation team analysis. Fictional example.
---

# Calder Valley Homes: a simpler organisation built around tenants
layout: title

```json
{"subtitle": "Design principles, target structure, decision rights and transition plan", "client": "Calder Valley Homes Board and Executive Team",
 "date": "25 November 2026", "prepared_by": "Transformation team"}
```

# We propose five divisions in place of nine directorates, saving £4.8m a year with 90 fewer posts by 2028
layout: exec-summary
section: Summary
footnote: Headcount is full-time equivalents (FTE). All changes follow the association's consultation policy and are subject to it.

```json
{"points": [
  {"lead": "Tenants wait too long because nine directorates share each decision",
   "support": ["A repair needing two directorates takes 23 days on average", "Six management layers separate tenants from the Chief Executive"]},
  {"lead": "Four principles guide the design",
   "support": ["One owner per tenant outcome", "Decisions taken close to tenants", "Fewer layers", "Common services shared"]},
  {"lead": "The target model has five divisions and five layers",
   "support": ["Average span of control rises from 4.1 to 7.0", "Headcount falls from 1,240 to 1,150 FTE: 60 vacancies and 30 voluntary exits"]},
  {"lead": "The new structure goes live on 1 July 2027",
   "support": ["Costs £3.1m to achieve; payback in 8 months from full run rate", "Repairs and tenant contact keep running throughout"]}]}
```

??? The saving is £4.8m a year at full run rate, which is 90 posts. 60 come from vacancies we would not refill and 30 from a voluntary exit window.

# Four design principles guide every choice in the new operating model
layout: columns
section: Principles

```json
{"columns": [
  {"header": "One owner per outcome", "icon": "target", "bullets": ["Each tenant outcome has one accountable director", "Repairs, rent and neighbourhoods each have a single owner", "No outcome is shared between three directorates"]},
  {"header": "Decide close to tenants", "icon": "house", "bullets": ["Area managers decide repairs priorities and allocations", "Directors decide only what crosses areas", ["Spend limits rise from £5k to £25k for area managers", 2]]},
  {"header": "Fewer layers, wider spans", "icon": "layers", "bullets": ["Five layers from Chief Executive to front line, down from six", "Average span of 7 reports, up from 4.1", "No manager with fewer than 5 reports"]},
  {"header": "Share common services", "icon": "users", "bullets": ["Finance, people, digital and data serve all divisions", "One housing system replaces four", "One performance dashboard, updated weekly"]}],
 "compare": [
  {"label": "Today", "values": ["2 of 8 outcomes owned", "23 days to close", "Span 4.1; six layers", "Four systems"]},
  {"label": "Target", "values": ["8 of 8", "14 days", "Span 7.0; five layers", "One system"]}]}
```

??? We agreed these principles with the Executive Team on 4 November. Every design choice later in the deck maps back to one of the four.

# Today nine directorates share tenant outcomes; the target model gives each outcome one owner
layout: before-after
section: Design
footnote: Spans and layers from the HR system, October 2026. Repairs times from the repairs system, January to September 2026.

```json
{"before_title": "Today", "after_title": "From 1 July 2027",
 "rows": [
  {"dimension": "Structure", "before": "Nine directorates, each with its own management team", "after": "**Five** divisions: homes, property, finance, people, digital"},
  {"dimension": "Layers", "before": "Six layers from Chief Executive to front line", "after": "**Five** layers"},
  {"dimension": "Span of control", "before": "Average of 4.1 reports per manager", "after": "Average of **7.0** reports per manager"},
  {"dimension": "Repairs", "before": "Three directorates touch each job; 23 days to close on average", "after": "One owner end to end; target **14** days"},
  {"dimension": "Systems", "before": "Four housing systems that do not share data", "after": "One housing system and one weekly dashboard"}]}
```

??? The 23-day figure is for jobs that need both property and homes teams to act, about 4 in 10 repairs.

# The target structure has five divisions reporting to the Chief Executive, with six neighbourhood area teams in Homes
layout: org-chart
section: Design
footnote: Roles only. Names and appointments follow the Board's approval and the formal consultation.

```json
{"nodes": [
  {"id": "board", "title": "Board"},
  {"id": "ceo", "title": "Chief Executive", "parent": "board"},
  {"id": "homes", "title": "Homes and Neighbourhoods", "name": "Director", "parent": "ceo", "highlight": true},
  {"id": "prop", "title": "Property and Development", "name": "Director", "parent": "ceo"},
  {"id": "fin", "title": "Finance and Corporate", "name": "Chief Finance Officer", "parent": "ceo"},
  {"id": "ppl", "title": "People and Culture", "name": "Director", "parent": "ceo"},
  {"id": "dig", "title": "Digital and Data", "name": "Director", "parent": "ceo"},
  {"id": "area", "title": "Six area teams", "name": "Area managers", "parent": "homes"}]}
```

??? Five divisions, down from nine directorates. Homes and Neighbourhoods is the largest, with six area teams that own repairs priorities, allocations and rent.

# Decision rights move to area managers and divisions, and every decision keeps one accountable owner
layout: raci
section: Decision rights
footnote: R = responsible, A = accountable, C = consulted, I = informed. Each decision has exactly one A.

```json
{"roles": ["Board", "Chief Executive", "Division directors", "Area managers", "Finance"],
 "activities": [
  {"name": "Approve the annual budget", "cells": ["A", "R", "C", "I", "R"]},
  {"name": "Approve spend over £250k", "cells": ["I", "A", "R", "I", "C"]},
  {"name": "Set repairs priorities", "cells": ["", "I", "A", "R", "C"]},
  {"name": "Allocate homes to tenants", "cells": ["", "I", "A", "R", ""]},
  {"name": "Recruit to posts within budget", "cells": ["", "I", "A", "R", "C"]},
  {"name": "Agree rent increases", "cells": ["A", "R", "C", "I", "R"]},
  {"name": "Approve new housing development schemes", "cells": ["A", "R", "R", "I", "C"]},
  {"name": "Change the housing system configuration", "cells": ["", "I", "A", "C", "C"]}]}
```

??? The big change is that area managers now carry responsibility for repairs priorities and allocations, which used to go to a directorate panel.

# Transition takes twelve months: consult in early 2027, go live on 1 July and embed through 2028
layout: roadmap
section: Transition
footnote: Quarters are calendar quarters. Go-live follows Board approval in December 2026 and formal consultation.

```json
{"periods": ["Q1 27", "Q2 27", "Q3 27", "Q4 27", "Q1 28", "Q2 28"],
 "phases": [{"name": "Consult and appoint", "start": 0, "end": 2}, {"name": "Go live", "start": 2, "end": 3}, {"name": "Embed", "start": 3, "end": 6}],
 "lanes": [
  {"name": "Structure", "items": [{"label": "Formal consultation", "start": 0, "end": 1, "rag": "G"}, {"label": "Director appointments", "start": 1, "end": 2}, {"label": "Structure live, 1 July", "type": "milestone", "at": 2}]},
  {"name": "People", "items": [{"label": "Voluntary exit window", "start": 0.5, "end": 1.5}, {"label": "Manager development", "start": 2, "end": 5}]},
  {"name": "Systems", "items": [{"label": "Decision rights guide", "start": 0, "end": 2}, {"label": "Single housing system", "start": 1, "end": 4.5, "rag": "A"}]},
  {"name": "Service", "items": [{"label": "Repairs line unchanged", "start": 0, "end": 3}, {"label": "Weekly dashboard", "start": 2, "end": 6}]}],
 "today": 0}
```

??? The single housing system is the biggest risk and is already amber. If it slips, the structure still goes live on 1 July, but the weekly dashboard starts later.
