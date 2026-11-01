---
deck: Kestrel Foods: growth strategy to 2030
context: Kestrel Foods  |  Executive Committee  |  November 2026
tracker: Summary, Gap, Options, Bridge, Plan
sticker: Draft for discussion
deck_type: strategy
source: Kestrel Foods finance data 2022 to 2026 and 2027 plan; strategy team analysis. Fictional example.
---

# Kestrel Foods: closing a £210m growth gap by 2030
layout: title

```json
{"subtitle": "Momentum case, growth options and a plan to reach £1,200m revenue", "client": "Kestrel Foods Executive Committee",
 "date": "24 November 2026", "prepared_by": "Strategy team"}
```

# Momentum takes revenue to £990m by 2030; five initiatives worth £210m reach our £1,200m ambition
layout: exec-summary
section: Summary
footnote: Revenue is net sales in nominal pounds. Momentum case assumes the 2023 to 2026 growth rate continues.

```json
{"points": [
  {"lead": "Revenue grows 4.2% a year on momentum, to £990m in 2030",
   "support": ["That is £210m short of the £1,200m ambition", "Closing it needs 9.3% a year, double the current rate"]},
  {"lead": "We tested three routes: core only, a balanced portfolio and acquisition-led",
   "support": ["The balanced portfolio scores 3.3 out of 4", "Core only cannot close the gap; acquisitions cost £420m"]},
  {"lead": "The balanced portfolio closes the gap for £180m of investment",
   "support": ["Five initiatives: online direct, international, premium range, pricing and a bolt-on", "Payback is 4.5 years"]},
  {"lead": "Delivery runs in three phases from 2027 to 2030",
   "support": ["Pricing and premium range deliver first", "International and the bolt-on carry the most risk"]}]}
```

??? Lead with the answer: we can get to 1,200 but not by doing more of the same. The balanced portfolio is a mix of organic and one small acquisition.

# At current momentum, revenue reaches £990m in 2030, leaving a £210m gap to the ambition
layout: line
section: Gap
footnote: Momentum is 4.2% a year from 2026; ambition is 9.3% a year, compounded.

```json
{"exhibit": "Net revenue: actual, momentum and ambition", "unit": "£m, nominal, 2022 to 2030", "prefix": "£", "decimals": 0, "axis_min": 600, "axis_max": 1300,
 "x": ["2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"],
 "series": [
  {"name": "Actual", "values": [700, 735, 770, 805, 840], "highlight": true},
  {"name": "Momentum", "values": [null, null, null, null, 840, 875, 912, 950, 990], "forecast": true},
  {"name": "Ambition", "values": [null, null, null, null, 840, 918, 1003, 1097, 1200], "color": "#C62828", "forecast": true}],
 "takeaways_title": "What the chart shows",
 "takeaways": ["Growth has slowed from 5.0% in 2023 to 4.3% in 2026.", "The ambition needs **£1,200m** in 2030, **£210m** above momentum."]}
```

??? Actual growth: 5.0, 4.8, 4.5 and 4.3 per cent over the last four years. Momentum holds at 4.2 per cent. The ambition is the Board's 2030 target.

# The balanced portfolio scores 3.3 out of 4 and closes the full gap for £180m, less than half the cost of buying
layout: options-matrix
section: Options
sowhat: We recommend Option B: approve the balanced portfolio and release £25m for 2027
footnote: Scores run from 0 (poor) to 4 (strong). Weighted scores: A 2.8, B 3.3, C 2.2. Investment is cumulative 2027 to 2030.

```json
{"stages": ["Long list (6)", "Screened (3)", "Evaluated", "Recommendation"], "stage": "Evaluated",
 "criteria": [{"name": "Closes the £210m gap", "weight": "30%"}, {"name": "Investment needed", "weight": "20%"},
              {"name": "Payback", "weight": "15%"}, {"name": "Execution risk", "weight": "20%"},
              {"name": "Fit with capabilities", "weight": "15%"}],
 "options": [{"key": "A", "name": "Core only (£45m)", "scores": [1, 4, 3, 4, 3]},
             {"key": "B", "name": "Balanced portfolio (£180m)", "scores": [4, 3, 3, 3, 3]},
             {"key": "C", "name": "Acquisition-led (£420m)", "scores": [4, 1, 1, 1, 3]}],
 "recommended": "B",
 "rationale": ["Option A adds only £65m, so revenue stops at £1,055m", "Option C closes the gap but costs £420m and carries integration risk", "Option B reaches £1,200m with one small acquisition, not two large ones", "It builds on the pricing and premium range the team already runs"]}
```

??? Option A is the cheap route but it misses the target by £145m. Option C hits the number but at more than twice the cost. B sits in the middle.

# Five initiatives add £210m of revenue by 2030, and online direct and international deliver over half of it
layout: waterfall
section: Bridge
footnote: Vertical axis starts at £900m. Initiative values are 2030 revenue, net of overlap between initiatives.

```json
{"exhibit": "Bridge from momentum revenue to ambition, 2030", "unit": "£m, nominal, 2030", "prefix": "£",
 "axis_min": 900, "increase_is": "good",
 "start": {"label": "Momentum 2030", "value": 990},
 "steps": [{"label": "Online direct", "value": 65}, {"label": "International", "value": 50},
           {"label": "Premium range", "value": 40}, {"label": "Pricing and mix", "value": 25},
           {"label": "Bolt-on acquisition", "value": 30}],
 "end": {"label": "Ambition 2030", "value": 1200},
 "callouts": [1, 2],
 "takeaways_title": "What the bridge shows",
 "takeaways": ["Online direct and international add **£115m**, 55% of the gap.", "Pricing and mix is the smallest step and the least risky."]}
```

??? Check the arithmetic: 65 plus 50 plus 40 plus 25 plus 30 is 210. Added to 990 it gives 1,200. Online direct and international together are 115.

# Pricing and premium range deliver in 2027, while international and the bolt-on take until 2029 to reach full effect
layout: roadmap
section: Plan
footnote: Periods are calendar years. Bars show build and ramp-up; milestones show launch dates.

```json
{"periods": ["2027", "2028", "2029", "2030"],
 "phases": [{"name": "Build", "start": 0, "end": 1}, {"name": "Scale", "start": 1, "end": 3}, {"name": "Embed", "start": 3, "end": 4}],
 "lanes": [
  {"name": "Pricing and mix", "items": [{"label": "Price architecture", "start": 0, "end": 1.5, "rag": "G"}, {"label": "Full run rate (£25m)", "start": 1.5, "end": 4}]},
  {"name": "Premium range", "items": [{"label": "Develop six products", "start": 0, "end": 1}, {"label": "Launch and ramp", "start": 1, "end": 4}]},
  {"name": "Online direct", "items": [{"label": "Platform build", "start": 0.5, "end": 1.5, "rag": "A"}, {"label": "Scale to 40% of reach", "start": 1.5, "end": 4}]},
  {"name": "International", "items": [{"label": "Partner search", "start": 0, "end": 1}, {"label": "Two markets live", "start": 1, "end": 3, "rag": "A"}, {"label": "Third market", "type": "milestone", "at": 3}]},
  {"name": "Bolt-on", "items": [{"label": "Target screen", "start": 0.5, "end": 1.5}, {"label": "Close", "type": "milestone", "at": 1.5}, {"label": "Integrate", "start": 1.5, "end": 3, "rag": "A"}]}],
 "today": 0.1}
```

??? Pricing is ready to go in January. International and the bolt-on carry the most risk, so we stage them in 2028 and review at each gate.
