# F4 `gen3_polarity_ladder`: row format for decide2 (agent C)

This note is the input for F4's independent `decide2` (SPEC 8.1: written by agent C, who has not read F4's
`decide()`). Read the rows, this note and SPEC 5 F4. Do not read `gen3_polarity_ladder.py`, and do not import
`pl_frames.gold`, `pl_frames.CELL_FLIPS` or `pl_frames.CELL_ROLE`. Work out each question's polarity from its wording.

## Files

| What | Path |
|---|---|
| Train rows | `data/v14_parts/yn2b_raw/gen3_polarity_ladder.jsonl` (1,500 rows, 750 units) |
| Dev rows | `data/v14_parts/yn2b_raw/dev/gen3_polarity_ladder.jsonl` (300 rows: 150 `dev_kind` iid, 150 holdout) |
| Relations | `yn2b_raw/relations/` and `yn2b_raw/dev/relations/`, file `gen3_polarity_ladder.jsonl` |
| Cards | `data/v14_parts/yn2b_defs/gen3_polarity_ladder__<meta.defs>.json`. Key order is the card order; `yes` and `no` come last |
| Proposition sources | `yn2b/f4_sources.json`: `latent_id -> {kind, P, ...}`, with the source row id for (b) and the base row id for (a) |
| Frame templates | `golden_src/gen3/pl_frames.py` `QUADS` (text only), or `yn2b/f4_templates.json` |

## Row shape

- Every row is yes/no: `options ["yes","no"]`, `gold "yes"|"no"`. Units have exactly 2 rows with the same state.
  - The `view "base"` row asks the plain question. It has `polarity 0` and `role "para"`.
  - The `view "ladder"` row asks the same thing through 1 or 2 flips. It has `polarity 1` and `role "neg"`, or
    `polarity 2` and `role "dneg"`.
  - Relation: `complement` when the ladder row has polarity 1, `equiv` when it has polarity 2.
- `meta.tpl = "<quad>.<cell>"`, for example `dd2.10`. The quad picks a frame. The cell digits pick the switch
  alternative: the first digit for `{A}`, the second for `{B}`. The tpl id is metadata. Derive the answer from the
  instruction text.
- `instructions` is the frame with `{A}`, `{B}` and `{d}` filled in. `{d}` is the proposition P, a clause.
  - (a) P looks like `"<label>" is the listed <noun> that fits <text> best`.
  - (b) P is a restated program decision. The table below lists the forms.
- `meta.pack`: `a` for human-label rows; `f1a`, `f1b`, `f2`, `f3` or `f6.<F6 pack>` for program decisions.
- `meta.renderer` is the proposition kind: `a.<source>`, `f1.outcome`, `f1.record`, `f1b.claim`, `f1b.log`,
  `f2.may`, `f2.verdict`, `f2.output`, `f3.state`, `f3.record`, `f6.term` or `f6.record`.
- `meta.fmt` is the source row's format. The state is copied byte for byte from the source or base row.
- (a) rows also carry `meta.derived_from`, the golden_train base row id. That row's `gold` is the human label.

## Card (yes/no rows; `card_style` none means the model sees no card)

The lines come in this order:

1. (a) only: `task` (the labelling task, Claude-written), then the listed labels with Claude-written definitions.
   These are the gold label, the nearest wrong label (L is one of the two) and up to 4 more of the base row's labels, in shuffled order.
2. (b) only: the source row's extra definition lines, if it had any. Examples: the F1b rounding rules, the F6
   operative definition, the F3 dialogue references.
3. `the statement holds` and `the statement fails`: what makes P true or false.
   - (a): `"L" fits ... better than any other listed ... does.`
   - (b): the source row's own yes and no definitions.
4. `yes` and `no`. They restate the question as a statement, and its denial, with the same switches filled in.

## Truth of P (what decide2 must establish independently)

- **(a)** P is true if and only if the quoted label equals the human gold of the base row (`meta.derived_from` in
  `data/v14_parts/golden_train.jsonl`). The base row's options use the real label names: F4(a) never uses
  renamed-label rows.
- **(b)** P is true if and only if the source family's decision is yes. The suggested route:
  1. Rebuild the source question from P.
  2. Run that family's decide2 (`v3_rule_chain`, `v3_tool_guard`, `v3_state_track`, `v3_def_literal`) on
     `{state, instructions: <rebuilt question>, meta: {fmt, tpl, ...}}` with the card lines from step 2 above.
  3. Alternatively, look the source row up through `yn2b/f4_sources.json` (`src_key`, `src_rid`) and re-run decide2
     on the original source row.

| renderer | P form | source question it restates |
|---|---|---|
| f1.outcome | `the outcome of this <req> under the <doc> is "<x>"` | F1 pos1/pos2/pos3 |
| f1.record | `the decision recorded in the case file for this <req> is consistent with the <doc>` | F1 jdg1-3 |
| f1b.claim | `under the rules in the card, the evidence establishes the claim` | F1 bpos1/2 |
| f1b.log | `under the card's rules, the fact-check log entry for this claim is consistent with the evidence` | F1 bjdg1/2 |
| f2.may | `the proposed call may run under the policy` | F2 may0-4 |
| f2.verdict | `the verdict the guardrail logged for the proposed call is consistent with the policy` | F2 judge0-4 |
| f2.output | `the assistant's output meets every requirement stated for it` | F2 output0-4 |
| f3.state | the machine's JB yes-statement, for example `order SO-1 is in status returned at the end of the log` | F3 yes/no q templates |
| f3.record | `the agent's recorded state is consistent with ...` / `every value in the agent record is supported by ...` / `every entry of the agent record matches ...` | F3 jdg.a/b/h |
| f6.term | `the <entity> is a '<term>' under <clause> ...` (5 wordings, one per is0-is4) | F6 is0-4 |
| f6.record | `the classification recorded ... is consistent with <clause>` (5 wordings) | F6 judge0-4 |

## Frames

There are 10 frame families with 3 quads each; `pl_frames.QUADS` holds the exact text.

- **Training families:**
  - `verdict_record`, `sign_off` and `compliance_flag`: they evaluate a record and are the tier `judge` rows;
  - `decision_direct`, `exception_scope`, `gatekeeping`, `burden` and `checklist`.
- **Held out** (dev_holdout only): `audit_finding` (record) and `counter_hypothesis`.

**What every frame assumes.** P is either established or ruled out by the material. That holds for every F4
proposition, because each is a program decision or a human gold label. So "nothing supports the idea that P" and
"there is no truth in saying that P" are read as "P is false".

**Gatekeeping frames** say "exactly when P". A gate admits, a rule lets a case proceed, or a step passes an item **if
and only if** P holds. Acting "properly" means acting as that rule requires.

## Expected agreement

SPEC 8.1 requires agreement with the program gold on 100% of rows. If more than 1% of rows disagree, that is a
generator bug to report to builder A, not a reason to filter.

## R2 changes (1 Oct; `yn2b/r2_polarity_ladder_gate.json`)

- **Two frames reworded** (`pl_frames`, with decide2's frame text re-synced):
  - `gk2`: "... would it be proper / improper to let this case proceed / stop this case?" ("clear this case" also reads
    as "close the case").
  - `cf1`: "A compliance scanner attached a note to this file stating that ... is that note well founded /
    unfounded?" ("is that flag warranted" also reads as "does the file have a compliance problem").
- **F4(a) pair and bundle** (`gen3_polarity_ladder.a_pair`): the near miss is the wrong label whose F4 card definition
  overlaps gold's most; the bundle keeps gold and the near miss a mutual nearest pair (another label goes in only if it
  is less similar to each of them than they are to each other). Only labels that occur both as gold and as near miss in
  the pool are quoted, and truth(P) is balanced per quoted label.
- **Steering**: truth(P) is balanced per proposition kind on the depth-0 rows (train), and the surface shortcut solvers
  (`SURFACE_SOLVERS`) are steered from below as well as above.
