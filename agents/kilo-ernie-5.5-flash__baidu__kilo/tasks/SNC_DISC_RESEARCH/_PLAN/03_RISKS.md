# 03 — Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Local model hallucinates ServiceNow UI paths | High | High | WT1 verifies against vendor docs; peers labelled "knowledge-based", flagged for human spot-check. |
| Small local models (3b) too weak for nuance | Medium | Medium | Assign them narrower slices; escalate to bigger model (deepseek-r1:32b) for reasoning-heavy parts. |
| Free API key rate-limited / quota exhausted | Medium | Medium | UsageTracker caps concurrency + daily req/tokens; probe marks unreachable; orchestrator degrades. |
| Web docs behind login / JS-rendered | Medium | Medium | Use webfetch/defuddle; fall back to Playwright; cite what was fetched. |
| Release drift (menu paths differ) | High | Low | Note per-release differences explicitly; scope to current GA. |
| Parallel outputs contradict each other | Medium | Medium | Lead (WT1) integrates + reconciles; single combined report is the source of truth. |
| Context window overflow on big model | Low | Medium | Chunk research; pass distilled snippets, not raw dumps. |
| No live ServiceNow instance to verify | High | Medium | Deliverable is documentation-grade; flag every "verify on your instance" point. |