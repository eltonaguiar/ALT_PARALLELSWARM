"""
worktree_manager.py — scaffold per-model worktrees with the standard contract.

Given a task name and a list of model keys, create:
  tasks/<task>/worktrees/WT<n>_<slug>/
      00_WORKTREE.md
      01_GOAL.md
      02_OUTPUTFORMAT.md
      03_FILESSCOPE.md
      phases/            (empty; agents drop phaseN.md as they start a phase)
      files/             (deliverables)
      05_QA.md
      06_FINALSUMMARY.md

If a task.json exists it is used as the source of truth for goals/output/scope;
otherwise generic placeholders are written for the agent to fill.

Usage:
  python -m swarm.worktree_manager --task SNC_DISC_RESEARCH
  python -m swarm.worktree_manager --task SNC_DISC_RESEARCH --models ollama/qwen2.5:7b ollama/llama3.2:3b
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "tasks"


def slugify(model_key: str) -> str:
    s = model_key.replace("/", "-").replace(":", "-")
    return re.sub(r"[^a-zA-Z0-9._-]", "", s).lower()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def scaffold(task: str, assignments: list[dict], force: bool = False) -> list[Path]:
    """assignments: [{model, role, goal, output_format, files_scope}]"""
    made = []
    base = TASKS / task / "worktrees"
    for i, a in enumerate(assignments, start=1):
        slug = a.get("slug") or slugify(a["model"])
        wt = base / f"WT{i}_{slug}"
        # never clobber an already-authored worktree (e.g. the lead's WT1)
        if (wt / "00_WORKTREE.md").exists() and not force:
            print(f"  skip (exists): {wt.relative_to(ROOT)}")
            continue
        (wt / "phases").mkdir(parents=True, exist_ok=True)
        (wt / "files").mkdir(parents=True, exist_ok=True)

        _write(wt / "00_WORKTREE.md", (
            f"# Worktree WT{i}_{slug}\n\n"
            f"- **Task:** {task}\n"
            f"- **Model / provider:** `{a['model']}`\n"
            f"- **Role:** {a.get('role','contributor')}\n"
            f"- **Branch/worktree:** local folder `tasks/{task}/worktrees/WT{i}_{slug}`\n"
            f"- **Created:** scaffolded by worktree_manager.py\n"
        ))
        _write(wt / "01_GOAL.md", f"# Goal — WT{i}_{slug}\n\n{a.get('goal','(fill in)')}\n")
        _write(wt / "02_OUTPUTFORMAT.md",
               f"# Output format — WT{i}_{slug}\n\n{a.get('output_format','Markdown, headed sections.')}\n")
        _write(wt / "03_FILESSCOPE.md",
               f"# Files in scope — WT{i}_{slug}\n\n{a.get('files_scope','Only files under this worktree\'s `files/`.')}\n")
        _write(wt / "05_QA.md", f"# QA — WT{i}_{slug}\n\n_Status: pending_\n")
        _write(wt / "06_FINALSUMMARY.md", f"# Final summary — WT{i}_{slug}\n\n_Status: pending_\n")
        made.append(wt)
    return made


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold swarm worktrees")
    ap.add_argument("--task", required=True)
    ap.add_argument("--models", nargs="*", default=[], help="model keys to scaffold")
    ap.add_argument("--force", action="store_true", help="overwrite existing worktrees")
    args = ap.parse_args()

    task_dir = TASKS / args.task
    cfg_path = task_dir / "task.json"
    assignments: list[dict] = []
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text())
        for a in cfg.get("worktrees", []):
            assignments.append({
                "model": a["model"],
                "role": a.get("role", "contributor"),
                "goal": a.get("goal", ""),
                "output_format": a.get("output_format", "Markdown, headed sections."),
                "files_scope": a.get("files_scope", ""),
                "slug": a.get("slug"),
            })
    elif args.models:
        assignments = [{"model": m, "goal": "(fill in)"} for m in args.models]
    else:
        ap.error("no task.json and no --models given")

    made = scaffold(args.task, assignments, force=args.force)
    print(f"scaffolded {len(made)} worktree(s) under {TASKS / args.task / 'worktrees'}")
    for w in made:
        print("  ", w.relative_to(ROOT))


if __name__ == "__main__":
    main()