# CLARIFICATIONS — SNC_DISC__WT1

**Agent:** `deepseek-v4.1-flash-fast__freebuff__buffy` (DeepSeek V4.1 Flash Fast / Freebuff)

The brief invited clarifications before going deep. Here are the ones that actually change the
output, with the decision I made so the work is not blocked.

| # | question | decision taken | would change if… |
|---|---|---|---|
| C1 | Which ServiceNow release should this target? | **Release-agnostic**, with the release label quoted on every citation (pages I used are labelled Brazil / Zurich / Xanadu / Washington DC). | you say "we are on X" → I would collapse the variant notes and pin menu paths to that release |
| C2 | Does "configuration options" include **patterns** (horizontal pattern editor, steps, steps params)? | Treated as **out of scope for depth**, listed as a configuration surface with a pointer. Fully documenting pattern authoring is its own worktree (proposed `SNC_DISC__WT2`). | yes — pattern authoring is where most custom Discovery effort actually goes |
| C3 | Is Cloud Discovery / Service Mapping / ACC in scope? | Mentioned only where they alter the CMDB write path (e.g. Service Mapping forces modern identifiers). | yes — cloud is a different configuration surface with different duplicate modes |
| C4 | Do you want the "verify in your instance" checks spelled out? | Yes — section 15 has copy-paste check steps, because half of "Discovery made a duplicate" is diagnosed from Discovery Status + CI Class Manager, not from docs. | — |
| C5 | Do you want this as one long doc or per-topic docs? | One reference with a stable section map (easier for a swarm to diff and for a human to grep), plus a raw evidence digest at `research/EVIDENCE_DIGEST.md`. | — |

## Requests to other agents

- **None blocking.** I can browse (see `00_PREREQ/PREREQ.md`).
- If another agent is on **patterns** (`SNC_DISC__WT2`) or **Cloud Discovery**, my reference links to
  them by section rather than duplicating, so we merge cleanly.
- If a login-gated KB article is needed later, that is the one thing I cannot reach — ask an agent
  with an authenticated Now Support session.
