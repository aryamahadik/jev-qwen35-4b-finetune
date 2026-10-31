# OWNER RULES: orchestration and model routing (NOT research; binding for C2 and C2.1; owner 18 Oct 2026)

Owner, 18 Oct ~01:00 UTC: "make the perfect orchestration at its best ... understand where to use which model
Sonnet 5.5, Opus 5.5 and Haiku 5.5". The planner MUST apply this table to every lane and stage in C2_1_PLAN_v3.md and
C2_1_BUILD_ORDER.md (name the model and effort for each task). Never Fable. Every workflow agent sets `model` explicitly.

## Model routing
| Work | Model | Effort |
|---|---|---|
| Orchestrator: plans, rulings, GO packets, 8.5 source checks, verifying every agent's numbers before they are reported | Opus 5.5 (main session) | high |
| Design/judgment agents: plan synthesis, ruling drafts, plan/ruling skeptics, OHS-5 brief, sealed freeze sign-off, A43 (d) wrong-gold / ambiguous confirmations, G0-lite family approvals | Opus 5.5 | high |
| All code: generators, solver A, independent solver B, tools, sandbox executor, G13/select/mix runs that need judgment, trainer, eval harnesses | Sonnet 5.5 | high (routine runs: medium) |
| Code reviews and build skeptics (a fresh agent that did not write the code) | Sonnet 5.5 | high |
| Deep web research and research verification (refuters) | Sonnet 5.5 | high |
| First-pass adjudication of blind-read disagreements | Sonnet 5.5 | medium |
| Blind reads (G5-H / G9 / answerability), wording pools, licence-card scouting, extraction, counting, running known scripts, log condensing, HANDOFF drafts | Haiku 5.5 | medium (mechanical: low) |

Haiku script-runners stop and report after 2 failed attempts. A Haiku result that decides a gate is always checked by
the next tier (Sonnet adjudication, Opus confirmation) as the adopted G5-H/A43 chain says.

## Orchestration rules
1. Critical path first: C2 (GO #1, training, grid, GO #2) > OHS-5 sealed build > C2.1 generator code > C2.1 rows.
   A C2 step never waits for a C2.1 step.
2. Parallel lanes; exactly one writer per set of files; agents that write overlapping files get worktree isolation.
3. Single-resource locks: G13 runs on the Mac one job at a time (never overlapping C2's binding G13); the od-l4b GPU runs
   one job at a time; Modal is training only; execution gold only on the disposable sandbox VM.
4. Every build gets an independent skeptic before its output is used; every ruling gets an Opus skeptic.
5. Blindness: sealed-side agents never see training generators and training-side agents never see sealed material;
   blind readers get only Read + Write on their own task/answer files; the access audit runs on every read batch.
6. Workflows: pipeline by default (no idle barriers); loops always have a cap; no silent caps (log what is dropped).
7. Usage is decided on MEASURED get_usage before every large launch; ping the owner at 96%, never cross 98%.
8. Never idle: while a long job runs (G13, training, reads), the next step's tools and specs are prepared.
9. No placeholder arguments in workflow prompts; agents read files, not pasted summaries.
