#!/usr/bin/env python3
"""Repo checks: SKILL.md frontmatter (Agent Skills spec), references exist, every layout documented, examples build
with no errors. Run before every commit: python3 tools/validate.py [--no-build]"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SK = os.path.join(ROOT, "skills", "consulting-deck-studio")
sys.path.insert(0, os.path.join(SK, "scripts"))
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


s = open(os.path.join(SK, "SKILL.md"), encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
check(m, "SKILL.md: missing frontmatter")
fm = m.group(1) if m else ""
name = re.search(r"^name:\s*(.+)$", fm, re.M)
desc = re.search(r"^description:\s*(.+)$", fm, re.M)
check(name and name.group(1).strip() == "consulting-deck-studio", "name must equal the directory name")
check(desc and 1 <= len(desc.group(1)) <= 1024, "description must be 1-1024 chars (is %d)" % (len(desc.group(1)) if desc else 0))
for key in re.findall(r"^(\w[\w-]*):", fm, re.M):
    check(key in {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}, "non-portable frontmatter key: " + key)
check(s.count("\n") < 250, "SKILL.md should stay under 250 lines (is %d)" % s.count("\n"))
for ref in set(re.findall(r"references/([\w./-]+\.md)", s)):
    check(os.path.exists(os.path.join(SK, "references", ref)), "SKILL.md references missing file: " + ref)
for ref in set(re.findall(r"scripts/([\w./-]+\.py)", s)):
    check(os.path.exists(os.path.join(SK, "scripts", ref)), "SKILL.md references missing script: " + ref)

from cdslib import layouts, layouts_more, layouts_pmo  # noqa: E402,F401
doc = open(os.path.join(SK, "references", "layouts.md"), encoding="utf-8").read()
for lay in layouts.LAYOUTS:
    check("`%s`" % lay in doc, "layout '%s' is not documented in references/layouts.md" % lay)

import json as _json  # noqa: E402
lib = _json.load(open(os.path.join(SK, "data", "decks.json"), encoding="utf-8"))
ids = [d.get("id") for d in lib["decks"]]
check(len(ids) == len(set(ids)), "data/decks.json: duplicate ids")
for d in lib["decks"]:
    for k in ("id", "title", "url", "tier", "practice", "format", "verified"):
        check(d.get(k) not in (None, ""), "data/decks.json: %s missing %s" % (d.get("id"), k))
    check(d.get("practice") in ("pmo", "capital", "strategy", "management"), "data/decks.json: %s bad practice" % d.get("id"))
    check(d.get("tier") in (1, 2, 3), "data/decks.json: %s bad tier" % d.get("id"))

for shipped, src in [("status-report-from-files.md", "northline-monthly"), ("steerco-pack.md", "northline-rail-steerco"),
                     ("diagnostic-and-capital.md", "meridian-cost-review")]:
    a = os.path.join(SK, "assets", "examples", shipped)
    b = os.path.join(ROOT, "examples", src, "deck.md")
    check(os.path.exists(a) and open(a, encoding="utf-8").read() == open(b, encoding="utf-8").read(),
          "assets/examples/%s is out of sync with examples/%s/deck.md (copy it over)" % (shipped, src))

if "--no-build" not in sys.argv:
    for ex in sorted(os.listdir(os.path.join(ROOT, "examples"))):
        d = os.path.join(ROOT, "examples", ex)
        if not os.path.exists(os.path.join(d, "deck.md")):
            continue
        r = subprocess.run([sys.executable, os.path.join(SK, "scripts", "build.py"), d], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = r.stdout.decode(errors="ignore")
        check(r.returncode == 0, "example %s failed to build:\n%s" % (ex, out[-800:]))
        check(" 0 warning(s)" in out, "example %s has warnings:\n%s" % (ex, "\n".join(l for l in out.splitlines() if l.startswith("WARN"))))

if errors:
    print("FAIL")
    for e in errors:
        print(" - " + e)
    sys.exit(1)
print("OK: SKILL.md, references, %d layouts documented, examples build clean" % len(layouts.LAYOUTS))
