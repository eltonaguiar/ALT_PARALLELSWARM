#!/usr/bin/env python3
"""
orchestrate.py — run N agents in parallel, each in its own git worktree.

Responsibilities
  1. create/refresh a worktree + branch per agent (agent/<slug>) off main
  2. run shared/agent_runner.py per agent, respecting max_parallel
  3. commit each agent's folder in its own branch, push the branches
  4. write ORCHESTRATION.md at repo root (who ran, model, verdict, where)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

SHARED = Path(__file__).resolve().parent
REPO = SHARED.parent


def load_env():
    for p in (Path.home() / ".hermes" / ".env", REPO / ".env"):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def sh(cmd, cwd=None, timeout=180):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def ensure_worktree(slug: str) -> Path:
    wt = REPO.parent / f"wt-{slug}"
    if not (wt / ".git").exists():
        r = sh(["git", "worktree", "add", "-B", f"agent/{slug}", str(wt), "main"], cwd=REPO)
        if r.returncode != 0:
            raise RuntimeError(f"worktree add failed for {slug}: {r.stderr[-300:]}")
    return wt


def run_agent(agent: dict, rounds: str) -> dict:
    slug = agent["id"]
    t0 = time.time()
    try:
        wt = ensure_worktree(slug)
    except Exception as e:
        return {"agent": slug, "status": "worktree_error", "error": str(e)[:200]}
    key = os.environ.get(agent.get("api_key_env") or "", "")
    cmd = [sys.executable, str(SHARED / "agent_runner.py"),
           "--agent-id", slug, "--model", agent["model"], "--provider", agent["provider"],
           "--base-url", agent.get("base_url", "http://localhost:11434/v1"),
           "--wt", str(wt), "--wt-num", str(agent.get("wt", 1)), "--rounds", rounds]
    if key:
        cmd += ["--api-key", key]
    r = sh(cmd, cwd=wt, timeout=5400)
    out = {"agent": slug, "model": agent["model"], "provider": agent["provider"],
           "worktree": str(wt), "branch": f"agent/{slug}",
           "exit": r.returncode, "wall_s": round(time.time() - t0, 1)}
    m = re.search(r'\{.*?"qa_score".*?\}', r.stdout, re.S)
    if m:
        out.update(json.loads(m.group(0)))
    else:
        out["error"] = (r.stdout[-300:] + r.stderr[-300:]).strip()[:400]
    # commit + push this agent's own branch
    folder = f"agents/{slug}"
    sh(["git", "add", folder], cwd=wt)
    c = sh(["git", "commit", "-m", f"agent({slug}): {agent['model']} via {agent['provider']} — {agent.get('note','')}"], cwd=wt)
    out["commit"] = "ok" if c.returncode == 0 else (c.stdout + c.stderr).strip()[:200]
    p = sh(["git", "push", "-u", "origin", f"agent/{slug}"], cwd=wt, timeout=300)
    out["push"] = "ok" if p.returncode == 0 else (p.stdout + p.stderr).strip()[:200]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", default=str(REPO / "agents.yaml"))
    ap.add_argument("--only", default="", help="comma-separated agent ids")
    ap.add_argument("--rounds", default="")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    load_env()
    cfg = yaml.safe_load(Path(args.roster).read_text())
    agents = cfg["agents"]
    if args.only:
        wanted = {x.strip() for x in args.only.split(",")}
        agents = [a for a in agents if a["id"] in wanted]
    rounds = args.rounds or str(cfg.get("rounds", 3))
    max_par = int(cfg.get("max_parallel", 2))

    print(f"task={cfg.get('task')} agents={len(agents)} max_parallel={max_par} rounds={rounds}", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max_par) as ex:
        results = list(ex.map(lambda a: run_agent(a, rounds), agents))

    lines = [f"# Orchestration report — {cfg.get('task')}", "",
             f"Generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
             f"Agents: {len(results)} · max_parallel: {max_par} · rounds: {rounds}",
             f"Total wall time: {round(time.time()-t0,1)}s", "",
             "| agent (folder) | model | provider | QA | sources | browse | branch | push |",
             "|---|---|---|---|---|---|---|---|"]
    for r in results:
        lines.append("| `{a}` | {m} | {p} | {qa}/{t} | {s} | {b} | `{br}` | {pu} |".format(
            a=r.get("agent"), m=r.get("model", "?"), p=r.get("provider", "?"),
            qa=r.get("qa_score", "-"), t=r.get("topics", "-"), s=r.get("sources", "-"),
            b=("yes" if r.get("can_browse") else "no"), br=r.get("branch", "-"), pu=r.get("push", "-")))
    lines += ["", "## Where the work is", ""]
    for r in results:
        lines.append(f"- `{r.get('agent')}` → worktree `{r.get('worktree')}` · "
                     f"folder `agents/{r.get('agent')}/SNC_DISC__WT{r.get('wt', '?')}`")
    lines += ["", "Each branch holds that agent's own folder only, so branches merge without conflicts.", ""]
    (REPO / "ORCHESTRATION.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(results, indent=2))
    (SHARED / "state" / "last_run.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
