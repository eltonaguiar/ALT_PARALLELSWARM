#!/usr/bin/env python3
"""Create one isolated git worktree + branch per agent, and commit only that agent's folder."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

PHASE_DIRS = [
    "00_PREREQ", "01_PLAN", "02_CLARIFICATIONS", "03_PHASES",
    "04_QA", "05_FINAL", "06_FILESCOPE",
]


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.setdefault("GIT_AUTHOR_NAME", "ALT_PARALLELSWARM bot")
    env.setdefault("GIT_AUTHOR_EMAIL", "bot@alt-parallelswarm.local")
    env.setdefault("GIT_COMMITTER_NAME", env["GIT_AUTHOR_NAME"])
    env.setdefault("GIT_COMMITTER_EMAIL", env["GIT_AUTHOR_EMAIL"])
    result = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, env=env)
    if check and result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed:\n{result.stdout}\n{result.stderr}")
    return result


def branch_for(agent_id: str) -> str:
    return f"agent/{agent_id}"


def worktree_path(repo: Path, agent_id: str, root: Path | None = None) -> Path:
    root = root or repo.parent
    safe = agent_id.replace("/", "-")
    return Path(root) / f"wt-{safe}"


def scaffold(path: Path, agent_id: str, wt_number: int) -> Path:
    base = path / "agents" / agent_id / f"SNC_DISC__WT{wt_number}"
    for name in PHASE_DIRS:
        (base / name).mkdir(parents=True, exist_ok=True)
    marker = base / "00_PREREQ" / "PREREQ.md"
    if not marker.exists():
        marker.write_text(f"# Pre-requisites — {agent_id}\n\n_Pending runner._\n", encoding="utf-8")
    return base


def create(repo: Path, agent_id: str, base: str = "main",
           root: Path | None = None, wt_number: int = 2) -> Path:
    repo = Path(repo).resolve()
    path = worktree_path(repo, agent_id, root)
    branch = branch_for(agent_id)
    if path.exists():
        scaffold(path, agent_id, wt_number)
        return path
    exists = run(["git", "rev-parse", "--verify", branch], repo, check=False).returncode == 0
    if exists:
        run(["git", "worktree", "add", str(path), branch], repo)
    else:
        run(["git", "worktree", "add", "-b", branch, str(path), base], repo)
    scaffold(path, agent_id, wt_number)
    return path


def commit_and_push(path: Path, agent_id: str, message: str, push: bool = True) -> dict:
    path = Path(path).resolve()
    folder = f"agents/{agent_id}"
    run(["git", "add", "--", folder], path)
    diff = run(["git", "diff", "--cached", "--quiet"], path, check=False)
    committed = False
    if diff.returncode != 0:
        run(["git", "commit", "-m", message], path)
        committed = True
    result = {"worktree": str(path), "branch": branch_for(agent_id),
              "committed": committed, "pushed": False, "push_error": None}
    if push:
        try:
            run(["git", "push", "origin", f"HEAD:refs/heads/{branch_for(agent_id)}"], path)
            result["pushed"] = True
        except Exception as exc:  # keep the artifact even if the push is unavailable
            result["push_error"] = str(exc)[:400]
    return result


def status(repo: Path) -> list[dict]:
    repo = Path(repo).resolve()
    out = run(["git", "worktree", "list", "--porcelain"], repo).stdout
    entries, current = [], {}
    for line in out.splitlines():
        if not line:
            if current:
                entries.append(current)
            current = {}
        elif line.startswith("worktree "):
            current["worktree"] = line.split(" ", 1)[1]
        elif line.startswith("branch "):
            current["branch"] = line.split(" ", 1)[1].replace("refs/heads/", "")
    if current:
        entries.append(current)
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create")
    c.add_argument("--repo", required=True)
    c.add_argument("--agent", required=True)
    c.add_argument("--base", default="main")
    c.add_argument("--root")
    c.add_argument("--wt", type=int, default=2)
    l = sub.add_parser("list")
    l.add_argument("--repo", required=True)
    a = sub.add_parser("commit")
    a.add_argument("--worktree", required=True)
    a.add_argument("--agent", required=True)
    a.add_argument("--message", required=True)
    a.add_argument("--no-push", action="store_true")
    args = parser.parse_args()
    if args.cmd == "create":
        print(create(Path(args.repo), args.agent, args.base,
                     Path(args.root) if args.root else None, args.wt))
    elif args.cmd == "list":
        print(json.dumps(status(Path(args.repo)), indent=2))
    else:
        print(json.dumps(commit_and_push(Path(args.worktree), args.agent,
                                         args.message, push=not args.no_push), indent=2))


if __name__ == "__main__":
    main()
