# Clarifications / requests — openrouter-free__openrouter__kilo

**Capability gate:** PASS

## Questions for the orchestrator
- None.

## Assumptions
- "Thorough" = configuration surface + processing order + CI Class Manager locations + duplicate/insert-update controls.
- ServiceNow release-agnostic unless a source pins a release.
- Free-tier API key: I'll use rate-limited `free` tier models from openrouter for sub-agent calls; my own context window is large enough to do primary synthesis.

## Backup plan if blocked
- If outbound HTTP to support.servicenow.com KB articles is blocked, use cached content from community forum posts and third-party ServiceNow documentation mirrors (e.g., `wiki.servicenow.com` archived pages).
- If my context exceeds limit during synthesis, split the reference into sections (config → order → ci_cm → dedup) and concatenate in `05_FINAL/`.