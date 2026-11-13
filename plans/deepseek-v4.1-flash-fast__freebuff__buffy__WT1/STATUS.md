# STATUS — SNC_DISC__WT1

| | |
|---|---|
| agent | `deepseek-v4.1-flash-fast__freebuff__buffy` |
| model / provider | `DeepSeek V4.1 Flash Fast` / Freebuff–Codebuff (Buffy runtime) |
| worktree | `SNC_DISC__WT1` |
| deliverable | `agents/deepseek-v4.1-flash-fast__freebuff__buffy/SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` |
| commit | `0f49a5b` (pushed to `main`) |

## Goal met?

Yes. 542-line, 19-section reference over 28 cited sources, covering the four goal areas plus all four
IRE rule families the operator named as the quality bar: identification rules (§11), reconciliation
rules (§12), IRE data source rules (§12A) and Data Refresh Rules (§12B).

## How it was produced

Native `web_search` + `read_url` in this agent runtime, digest-first: search → fetch authority →
quote into `research/EVIDENCE_DIGEST.md` → synthesise. No vendor API key, so this run has no
`budget.py` ledger entry (registered in `agents.yaml → self_runs` instead).

## Verification actually run

- every non-obvious claim carries `[S<n>]`; all 28 ids resolve in §18
- four rule families grep-checked in the committed file (7 / 15 / 2 / 12 hits)
- 8 items that could not be confirmed are tagged **UNVERIFIED** in §17 rather than guessed
- `python3 -m py_compile shared/*.py`, `yaml.safe_load(agents.yaml)`, budget acquire/release + cap test
- post-push: file, wiring and contributor row re-read from `origin/main`, not just the local tree

## Blockers / limitations

- No live ServiceNow instance, so §10 navigation paths are documentation-sourced, not clicked through.
- New York/Utah release labels differ; claims are pinned to the release label printed on each source.
- Pattern authoring (steps, step parameters, pattern debugging) was deliberately out of scope.

## Swarm finding worth keeping

The shared harness crashed every dispatched agent before its first model call
(`budget.acquire()` read `entry["inflight"]`, which `_roll()` never created → `KeyError: 'inflight'`;
`wall_s` ≈ 4.2 s, `sources: 0`). Fixed in `shared/budget.py`. **After** the fix the local 7B models
still returned unsourced prose — the wrapper was not the limiting factor; CPU-bound 7B inference and
the model's refusal to cite were.
