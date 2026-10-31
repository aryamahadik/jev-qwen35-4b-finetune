# decide2 re-checks (1 Oct 2026)

**Short version.**
- **F4 (as builder C): PASS.** The F4 builder changed only two frame strings in `v3_polarity_ladder.py`. The signs
  still come from the English wording, not from the generator. decide2 agrees with gold on 1,500/1,500 train and
  300/300 dev rows, including all 118 rows that use the two edited frames.
- **F6 (as builder A): PASS.** The F6 builder changed the exclusion grammar (one sentence per exclusion) and added
  claim-stating JB questions. Label meaning did not change: builder A's original decide2 gives the same answer as the
  current one on 1,800/1,800 rows. Agreement with gold is 1,650/1,650 train and 150/150 dev.
- **F2 devx (as builder C): FIXED, 100/100.** The crash was on the decide2 side. The devx rows are well formed;
  decide2 just could not read R's layout. I added a devx reader to `v3_tool_guard.py`. It now agrees with gold on
  100/100 devx rows. Train and dev answers are unchanged, row for row.
- CPU only. No model, no GPU, no Modal / gcloud / ssh. No data file, report, MANIFEST or tracked file was changed.
  Changed: `golden_src/gen3/v3_tool_guard.py`. New: `yn2b/tests/test_v3_tool_guard_devx.py` and this note.

How independence was checked (all three re-checks):
- Rows were stripped before decide2 saw them: no gold, tier, polarity, role, view, tpl or renderer.
- An import blocker refused every generator module (`gen3_*`, `pl_*`, `tg_*`, `rc_*`, `dl_*`, `dx_*`). Only the known
  shared data modules were allowed: `mv_core`, `rc_skins` and `dl_packs`.
- An audit hook listed every file opened while solving.
- Scripts and outputs are in the scratchpad (`recheck1oct/`).

## 1. F4 `v3_polarity_ladder.py` (re-check as builder C)

**What changed.** I diffed the file against the copy saved just before the edit
(`scratchpad/r2f4/v3_polarity_ladder.py.orig`, sha256 `5e26d820…`; now `565dfe8c…`, the hash in
`decide2_rerun_1oct.json`). Only four things changed: the docstring, one comment, and two `FRAMES` entries. No logic
and no imports changed.

| Frame | Before | Now |
|---|---|---|
| `compliance_flag.scanner` | "A compliance scanner flagged this file with the note that {C}. … is that flag {warranted+ / unwarranted-}?" | "A compliance scanner attached a note to this file stating that {C}. … is that note {well founded+ / unfounded-}?" |
| `gatekeeping.rule` | "… would it be {proper+ / improper-} to {clear+ / stop-} this case?" | "… would it be {proper+ / improper-} to {let this case proceed+ / stop this case-}?" |

**Signs, read again from the English:**
- **Scanner note.** The note says C. "Well founded" means yes iff C. "Unfounded" means yes iff not C. An inner
  negation turns C into not-P. The signs are right.
- **Gate rule.** The rule lets a case proceed exactly when C.
  - "Proper to let it proceed" means yes iff C. "Proper to stop it" means yes iff not C.
  - "Improper" flips each of these.
  - The signs are right, and there is no "clear = close the case" reading left.

**Independence.**
- decide2 never imports `gen3_polarity_ladder`, `pl_frames` or `pl_sources` (statically, and at run time under the
  blocker).
- It never opens `f4_sources.json` or `f4_templates.json`. It opened only the `yn2b_defs` cards and the other v3_*
  decide2 modules.
- Truth of P comes from the golden_train human gold for (a) rows, and from the source family's decide2 for (b) rows.
- **Small doc point.** The docstring says decide2 reads only `meta.defs`, `card_style` and `derived_from`. `truth_b`
  also passes `meta.fmt` to the source decide2. That is a format tag, not label information.

**Results** (gold-blind, generator imports blocked):

| Check | Train | Dev |
|---|---|---|
| Agreement | 1,500/1,500 | 300/300 |
| Undefined | 0 | 0 |
| `compliance_flag.scanner` rows | 30/30 | 4/4 |
| `gatekeeping.rule` rows | 80/80 | 4/4 |
| Wording probes on the edited-frame rows (each switch flipped must flip the answer) | 380/380 (both splits together) | |
| Full CLI: complement / equiv relations | 379 / 371, 0 broken | 81 / 69, 0 broken |
| Full CLI: route 2 (the original source row) | 750/750 | 300/300 |
| Full CLI: all wording probes | 5,461/5,461 | 1,075/1,075 |

- **Every cell is covered.** All four switch cells of both edited frames occur in train (inner × ask, act × ask). So
  100% agreement covers every combination.
- decide2's flip count equals `meta.polarity` on every row.
- **Old wording is gone.** It appears in 0 rows of the raw files, the assembled train / dev / devx files and arms
  A/B/C.
  - The new wording is in 110 train rows, 8 dev_iid rows and 68 rows of arms B and C.
- The assembled F4 golds equal the raw golds:
  - train 1,500;
  - dev_iid 150;
  - dev_holdout 150;
  - arm B 724 (arm C the same).
- **Disclosure.** The F4 builder also re-pinned two relation counts in builder C's `test_v3_polarity_ladder.py`
  (375/375 → 379/371). These are counts only (`r2_polarity_ladder_gate.json`).

## 2. F6 `v3_def_literal.py` (re-check as builder A)

**What changed.** I diffed the file against builder A's copy from before the R2 fixes
(`scratchpad/f6r2/orig/v3_def_literal.py`, sha256 `a645fa0c…`; now `4b8df3cc…`).
1. **Exclusion grammar.**
   - The text "It is not T if A[, unless B]; nor if C." became "It is not T if A[, unless B]. It is also not T if C.".
   - The regex, the split and the round-trip renderer changed to match.
2. **New questions.** Five claim-stating JB questions (`jbf`) were added.
3. **New refusal.** The fallback pair 'yes, this holds' / 'no, this does not hold' is now UNDEFINED under a question
   that states no claim.

`evaluate()`, `DEFAULT_READINGS` and the fact parsers did not change. In `dl_packs` (the shared surface data) the only
change is a new `EXCLUSIVE_ATTRS` table, which decide2 never reads.

**Label meaning is unchanged.**
- I ran builder A's original decide2 on today's rows, with every definition converted back to the old one-sentence
  list.
  - It gives the same answer as the current decide2 on 1,630/1,650 train rows and 148/150 dev rows.
  - The other 20 + 2 rows are exactly the `jbf` questions, which the original could not parse.
- For those rows, I mapped each question to its original JB wording: 22/22 gave the same answers.
- **Total: 1,800/1,800 rows give the same answer.**
- **"Unless" binds the same way.** Under both grammars an "unless" applies only to its own exclusion: the old parser
  also split per exclusion before reading "unless". 194 rows (180 train + 14 dev) have an "unless" on an exclusion
  that is not the last one. Those are the rows the R2 fix was about, and they get the same answer.
- **The old grammar is refused, not misread.** The current decide2 marks the old one-sentence form UNDEFINED (263
  converted rows; strict round trip). It never reads it differently.

**Results** (gold-blind, generator imports blocked):
- Train 1,650/1,650 and dev 150/150, with 0 undefined.
- The full CLI is clean:
  - structure: contrast 313 flipped, complement 171, equiv 246, inv 150 (dev: 44 / 32), with 0 broken;
  - cards: 0 mismatches.
  - The reading sensitivity is as before: `unrecorded_negative=holds` changes 4 train rows, and the gold follows the
    default.
- **Disclosure.** The F6 builder also updated builder A's `test_v3_def_literal_unit.py`, in line with the code change:
  - the definition text now uses the new grammar;
  - the old "; nor if" form is rejected;
  - the fallback pair is UNDEFINED under "Which statement fits" and answered under a claim-stating question.

## 3. F2 `v3_tool_guard.py` on devx (re-check as builder C)

**Why it crashed.** The problem was on the decide2 side.
- `parse_state` sent every JSON state that has a `policy` key to the training JSON reader. That reader indexes
  `obj["assistant"]`.
- The resulting KeyError escaped `decide2_row`, which only catches `SolverError`, and the CLI stopped.
- The JSON keys were only the first gap. R's devx surface differs everywhere:
  - three layouts (JSON lists, `### Section` markdown, `=== SECTION ===` brief);
  - 14 rule forms and 4 amendment forms, in R's own wording;
  - a catalog with argument roles;
  - new annex / session / confirmation / resource / call-log lines;
  - 10 question forms (13 wordings);
  - "None: the call breaks no rule", two JB option pairs, and R's output-requirement wording.
- The rows themselves are fine. Every line parses, and every stated "UTC offset at the current time" matches zoneinfo.

**Fix.** The new section 6b in `v3_tool_guard.py` (sha256 `10089ea5…` → `e25c0053…`):
- It reads R's surface into the same `Facts` / `Spec` objects. The evaluator stays shared.
- A state this reader does not know now gives UNDEFINED instead of a crash.
- It is switched on only when `Facts.dialect == "dx2"`.

Where R's policy text states a rule differently from the training wording, the devx path follows R's text:
- **Specific-over-general** applies only to same-argument limits, daily totals of the same kind and hours of use. It
  also displaces 'every tool' rules.
- **"The limit in rule N becomes V"** also amends daily counts and totals.
- **"Is the lack of a valid confirmation under rule K the only reason…"** is yes iff the broken rules are exactly
  [K].
- **Argument roles** come from the catalog.
- **"Resources a call affects"** are the matches of its pattern argument only.
- **Daily totals and the conditional confirmation** use the amount as written.
- **A word** is a run of characters without a space.

**How it was written.**
- The reader was written from the rendered devx rows (state, question, options) only.
- I did not read R's renderers or parse-back (`dx_*.py`), or the generator (`tg_*`, `gen3_tool_guard`). I only
  grepped their import lines and the `dx_common.py` docstring.
- Gold was compared once, after the reader read all 100 rows. Nothing was tuned after that.

**Results:**

| Check | Result |
|---|---|
| devx agreement | **100/100**, 0 undefined |
| By question family | block 22, choice 27, confirm 5, jb 10 (2 fallback), judge 5 + 5 (negated), may 16, output 4 + 6 (negated) |
| Gold-blind (rows reduced to rid / state / question / options), generator imports blocked | 100/100; no file opened while solving |
| Reading switches (all 10 alternatives, including the new `dx_table_amend=global`) | no devx answer changes |
| Each devx row re-laid out in the other two layouts | identical facts and answers, 300/300 |
| Did R's wording decide any row differently from the training engine's reading? (gold-free check) | no: precedence, confirmation-only question, affected resources and word split all give the same answers. "The limit in rule N becomes V" on daily counts (20 rows) cannot be read by the training engine at all |

**Train and dev did not move.**
- I compared the original file with the edited one on every row, under the default reading and all 9 original
  alternatives: 52,020 + 5,240 comparisons, 0 differences in answer or refusal.
- The parsed facts are identical, and no train or dev row takes the devx path.
- Train 5,202/5,202 and dev 524/524. The CLI (`--sensitivity`, no write) now runs through train, dev and devx with
  exit code 0.
- F4's decide2 calls `v3_tool_guard` for F2 propositions. I re-ran it after the edit and got the same result as
  before (1,500/1,500, 300/300).

**Tests.**
- The new `yn2b/tests/test_v3_tool_guard_devx.py` has 6 tests, and all pass:
  - devx rows read and agree;
  - all three layouts are read;
  - train and dev never take the devx path;
  - an unknown JSON layout gives UNDEFINED;
  - no reading switch changes a devx answer.
- Full suite: see section 4.

## 4. Full test suite after the edits

`PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider --basetemp=<scratch> yn2b/tests`:
- **Result: 1,239 passed, 1 skipped, 0 failed** (7 min 10 s), after the `v3_tool_guard.py` edit.
- The skip is the known one: `test_v3_state_track_written.py:95`, "not the pinned build".
- The new devx test file was written after that run started. I ran it on its own, together with the F2 test files:
  150 passed, 1 skipped (the same skip).

**Files this work changed** (sha256 snapshot of `golden_src/gen3/`, `yn2b/`, `yn2b_raw/` and the dev files, taken
before and after):
- `golden_src/gen3/v3_tool_guard.py`;
- new: `yn2b/tests/test_v3_tool_guard_devx.py`;
- new: this note.

No `__pycache__` was written.

Other agents changed files during this run. These are not mine:
- `yn2b/merge_yn2b.py`, `yn2b/tests/test_assemble_merge.py` and the new `yn2b/tests/test_merge_exclude.py` (05:57-05:59);
- the new `yn2b/devx_fresh_blind_solve.json` (06:10).

`git status` shows the same 6 tracked files modified as at the start.

## 5. Open points for the owner / A1 part 2

1. **R's devx parse-back is not an independent label check.** `dx_common.py` says R's parse-back is "text → facts →
   the shared decide()".
   - It shows that the rendered text holds the latent facts.
   - It does not show that R's new rule wording means what `decide()` computes.
   - For F2, the extended `v3_tool_guard` is now the first program that derives devx labels from R's wording, and it
     agrees 100/100.
   - F1, F3, F5 and F6 have no such program.
   - Their decide2 modules read 0/100 of their devx rows:
     - F1 and F6 give UNDEFINED.
     - F3 raises ValueError on 71 rows; F5 raises ParseError on all 100. These are crashes, the same kind of bug as
       F2's.
   - Out of scope here, not touched. Disclose this in A1 part 2.
2. **`decide2_rerun_1oct.json` has a stale hash.** It records `v3_tool_guard` sha256 `10089ea5…`; the file is now
   `e25c0053…`. Its train and dev counts are still exact, because the answers are identical. I did not run
   `--write-report`, so `v3_tool_guard_agreement.json` and the MANIFEST are unchanged.
   - If you want devx in the agreement record, run
     `../.venv/bin/python golden_src/gen3/v3_tool_guard.py --write-report`. It rewrites the report and appends one
     MANIFEST line.
3. **The F4 and F6 two-program rule holds.** The generator side made the edits, but they are wording and grammar only.
   decide2 still derives every label independently, and the old and new decide2 agree on every F6 row. No action is
   needed beyond disclosure.
