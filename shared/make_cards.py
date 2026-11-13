#!/usr/bin/env python3
"""
make_cards.py — generate a top-level INDEX.md and one AGENT_CARD.md per worktree.

The card answers exactly the four questions the brief asks of every agent:
  what worktree am I in · what was my goal · what is my output format · what files did I touch
plus model/provider so the fleet is unambiguous.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"
STATE = REPO / "shared" / "state"


def read(p: Path, default: str = "") -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return default


def branch_for(slug: str) -> str:
    r = subprocess.run(["git", "-C", str(REPO), "branch", "--list", f"agent/{slug}",
                        "--format=%(refname:short)"], capture_output=True, text=True)
    return (r.stdout.strip() or f"agent/{slug} (merged)")


def rubric_for(slug: str) -> dict:
    p = STATE / "rubric_scores.json"
    if not p.exists():
        return {}
    try:
        for row in json.loads(p.read_text()):
            if slug in row.get("doc", ""):
                return row
    except Exception:
        pass
    return {}


def main():
    roster = yaml.safe_load((REPO / "agents.yaml").read_text())["agents"]
    by_id = {a["id"]: a for a in roster}
    rows = []

    for folder in sorted(p for p in AGENTS_DIR.iterdir() if p.is_dir()):
        slug = folder.name
        meta = by_id.get(slug)
        if not meta:
            # agent from another contributor: derive from the <model>__<provider>__<harness> name
            parts = slug.split("__")
            meta = {"model": parts[0] if parts else "?", "provider": parts[1] if len(parts) > 1 else "?",
                    "base_url": "", "note": "external contributor folder (not in this roster)",
                    "wt": ""}
        wt_dirs = sorted(folder.glob("SNC_DISC__WT*"))
        if not wt_dirs:
            continue
        if not meta.get("wt"):
            meta["wt"] = wt_dirs[0].name.replace("SNC_DISC__WT", "")
        wt = wt_dirs[0]
        qa = read(wt / "04_QA" / "QA.md")
        prereq = read(wt / "00_PREREQ" / "PREREQ.md")
        final = read(wt / "05_FINAL" / "FINAL_SUMMARY.md")
        files = sorted(str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file())
        rub = rubric_for(slug)
        can_browse = "| Web search reachable | YES" in prereq
        m_qa = re.search(r"topic coverage \| (\d+)/(\d+)", qa)
        rows.append(dict(slug=slug, model=meta.get("model", "?"), provider=meta.get("provider", "?"),
                         base_url=meta.get("base_url", ""), note=meta.get("note", ""),
                         wt_num=meta.get("wt", "?"), wt_path=str(Path.home() / f"wt-{slug}"),
                         branch=branch_for(slug), files=files, qa=m_qa.groups() if m_qa else ("?", "?"),
                         can_browse=can_browse, rub=rub, final=final, qa_text=qa))

    # ---------------- per-worktree cards ----------------
    for r in rows:
        card = f"""# Agent card — `{r['slug']}`

**Model:** `{r['model']}`
**Provider:** `{r['provider']}`
**Endpoint:** `{r['base_url'] or 'n/a'}`
**Role note:** {r['note'] or '—'}

## Where this work lives
| | |
|---|---|
| worktree | `{r['wt_path']}` |
| branch | `{r['branch']}` |
| folder in repo | `agents/{r['slug']}/SNC_DISC__WT{r['wt_num']}/` |

## Goal
Produce as thorough a technical reference as possible on ServiceNow **Discovery configuration**:
configuration options and properties, order of operations, key bread crumbs under **CI Class Manager**,
and the configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records.

## Output format
`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every claim carrying a source URL
or explicitly marked UNVERIFIED; plus `04_QA/QA.md` and `05_FINAL/FINAL_SUMMARY.md`.

## Self-reported status
- capability gate: **{'browsing OK' if r['can_browse'] else 'NO BROWSING'}**
- internal topic check: **{r['qa'][0]}/{r['qa'][1]}**
- private rubric (external): **{r['rub'].get('passed', '?')}/4 mentioned, {r['rub'].get('strong', '?')}/4 quality**
- sources cited: **{r['rub'].get('sources', '?')}**

## Files modified ({len(r['files'])})
```
{chr(10).join(r['files'])}
```
"""
        (AGENTS_DIR / r["slug"] / "AGENT_CARD.md").write_text(card, encoding="utf-8")

    # ---------------- root index ----------------
    lines = ["# Fleet index — SNC_DISC_RESEARCH", "",
             "Each agent ran in its own git worktree and wrote only inside its own folder,",
             "so every branch merges without conflict. Cards below are generated from the run data.",
             "",
             "| agent folder | model | provider | browse | internal check | private rubric | card |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| [`agents/{r['slug']}`](agents/{r['slug']}/AGENT_CARD.md) | `{r['model']}` | "
                     f"{r['provider']} | {'yes' if r['can_browse'] else 'no'} | {r['qa'][0]}/{r['qa'][1]} | "
                     f"{r['rub'].get('passed','?')}/4 mentioned · {r['rub'].get('strong','?')}/4 quality | "
                     f"[card](agents/{r['slug']}/AGENT_CARD.md) |")
    lines += ["", "## Folder contract (every agent)", "",
              "```",
              "agents/<model>__<provider>__<harness>/",
              "  AGENT_CARD.md                 # this summary: model, worktree, goal, format, files",
              "  SNC_DISC__WT<n>/",
              "    00_PREREQ/PREREQ.md         # can I browse? playwright? context?",
              "    01_PLAN/PLAN.md             # goal, format, phases, risks, success criteria",
              "    02_CLARIFICATIONS/CLARIFY.md",
              "    03_PHASES/phaseN_*.md       # heartbeat per phase",
              "    04_QA/QA.md",
              "    05_FINAL/DISCOVERY_CONFIG_REFERENCE.md",
              "    05_FINAL/FINAL_SUMMARY.md",
              "    06_FILESCOPE/FILESCOPE.md",
              "    research/                   # raw search→digest transcripts",
              "```",
              "",
              "## Grading",
              "Private rubrics live **outside** this repo (`~/.alt_parallelswarm_private/`). "
              "`shared/judge.py` refuses to score if the rubric is inside the tree, and no rubric term "
              "appears in any agent prompt. See `HARNESS.md` → Grading.",
              ""]
    (REPO / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps([{k: r[k] for k in ("slug", "model", "provider", "qa")} | 
                      {"rubric": r["rub"].get("strong"), "sources": r["rub"].get("sources")} for r in rows], indent=2))


if __name__ == "__main__":
    main()
