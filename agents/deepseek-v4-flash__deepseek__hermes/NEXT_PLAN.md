# Next plan — coverage-driven research (author: `deepseek-v4-flash__deepseek__hermes`)

**Model / provider for this folder:** `deepseek-v4-flash` via `deepseek`.

## The problem this fixes

The first fleet run looked healthy on the internal check (8/8, 7/8, 6/8 "topics") and then failed the
private rubric: **no agent covered all four required constructs** (best was 2/4 with a section and a
mechanism; two agents were 0/4).

Root cause is not model quality. It is **planning**: the three research questions were derived from the
brief, not from a topic map of the domain. "Data Refresh Rules" was never asked about, so no model could
have found it. An agent cannot research a topic that the plan never contains.

## Design constraint (non-negotiable)

The rubric must not reach the models. So the fix cannot be "put the rubric in the prompt". Instead:

- a **private topic map** lives outside the repo (`~/.alt_parallelswarm_private/`), same leak rules as the rubric
- the planner expands the topic map into **neutral research questions** that reach the area without naming
  the graded construct (e.g. asking about *how CMDB data is kept current on a schedule* rather than
  "Data Refresh Rules")
- `shared/judge.py` remains post-hoc and refuses in-repo rubrics

## Phases

1. **Topic map (private)** — for each relevant construct: synonyms, adjacent mechanisms, likely source
   types (KB article, product doc, community thread). Stored outside the tree.
2. **Question expansion** — planner turns each topic into 2–3 neutral questions plus one "does this exist
   under a different name?" probe. Output goes into `01_PLAN/PLAN.md` so the run is auditable.
3. **Run** — same harness, same worktrees, same budget tracker. No prompt contains a rubric term
   (verify with the existing grep gate before every run).
4. **Judge** — post-hoc scoring against the private rubric; write ids/counts only.
5. **Coverage debt** — each agent's `FINAL_SUMMARY.md` gains a "coverage debt" section listing which of
   its own planned questions returned nothing, so a thin document self-reports instead of looking complete.

## Risks

| risk | mitigation |
|---|---|
| Neutral questions become so vague the models find nothing | pair each with one concrete adjacent mechanism term that is *not* a graded construct |
| Topic map leaks via plan files | plan files store the questions only; the map stays outside the repo |
| Local models ignore extra questions | cap at 6 questions/agent and enforce the existing rounds budget |
| Judge over-fits to phrasing | keep the "own section + mechanism phrase" rule; don't reward keyword stuffing |

## Success criteria

- All four rubric items reach `mentioned` for at least 2 agents, and ≥1 agent reaches `quality` on all four
- Zero rubric terms in any prompt/plan file (grep gate passes)
- Each agent's FINAL_SUMMARY lists coverage debt explicitly
- Budget ledger shows no provider exceeding its concurrency cap during the run

## Code changes required

- `shared/agent_runner.py`: take a question set from `--questions-file` (currently hardcoded `QUESTIONS`)
- `shared/planner.py` (new): topic map → neutral questions, with a `--check-leak` mode that greps output
  against the rubric term list before anything is written
- `shared/make_cards.py`: include coverage debt in the card
