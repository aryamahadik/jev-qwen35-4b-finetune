# yn2b SPEC (final): hard yes/no data for the final 2B

**Status:** final draft after the red-team, 30 Sep 2026, for owner review. Nothing is built, trained or edited yet.
It replaces `SPEC_draft.md`, which stays unchanged for the record. Section 1 lists every change and why.

**Inputs:** `SPEC_draft.md`, `gap_targets.json`, the three designs (`suite_examgap.json`, `agentic_suite.json`,
`robust/suite_spec.json`), `REQUIREMENTS_review.md`, `golden_src/GOLDEN_SPEC.md`, `PREREG_FINAL.md`,
`FINETUNE_PLAN.md`, the 30 Sep audit, and the pipeline code (all read only).

## Hard rules (breaking one rejects the data)

1. **GOLDEN_SPEC applies.** Labels come only from deterministic CPU programs that Claude writes. No model labels
   any row. Rows that reuse human text keep that text's licence.
2. **No bigger models, no Jev.** No model bigger than our 4B is used. No Jev output is used for anything.
3. **Held-out sets.**
   - JevBench item text is never copied.
   - OHS-1 and OHS-2 are analysed only. Nothing from them is copied or fitted.
   - OHS-3 is read only by the decontamination program, which prints counts only. Its composition (for example the
     task list in PREREG_OHS3) never sets a family, a count or a priority.
4. **Amendments first.** Amendments A1 and A2 are committed before the matching GPU step (section 12).
5. **GPU needs GO.** Every GPU step waits for the owner's GO.
6. **Frozen code stays frozen.**
   - The 4B relay keeps launching from the `final-frozen` checkout.
   - All 2B code and config work happens in a new git worktree.
   - Nothing edits `train_decoder.py`, `decoder_io.py`, `prism_x.py`, `writeblock.py`, golden_train or
     golden_relations.

---

## 0. Summary

**What.** 8 program-labelled families (§3).

| Part | Families | Base rows | Split by type |
|---|---|---|---|
| Wave 1 | F1-F6 | 17,500 | |
| Wave 2 | F7-F8 | 2,500 | |
| **All base rows** | | **20,000** | 12,600 yes/no, 5,100 choice, 2,300 score-style |
| Attack twins | | about 1,300 | |
| **Total** | | **about 21,300** | **4.1% of the 2B training file** |

Wave 2 goes in only if it is green before arm B launches.

**Targets.** The 2B's largest measured yes/no gaps, and the JevBench v1.5 families that we have no rows for today:

| Target | Rows today |
|---|---|
| Tool-call guardrail | 0 guardrail yes/no rows, 290 tool-selection rows |
| State tracking | 0 |
| Lead-qualification Score | 0 score-style rows |

Also covered: long rule chains, polarity, and literal definitions.

**Labels.** Exact program gold only. There is no 4B teacher on these rows, so the trainer target is 0.95 / 0.05.

**Gate: a pre-registered 2-arm A/B of short 2B runs (§11).**
- Arm A (control) does not need yn2b, so it can train as soon as the 2B smoke passes.
- Arm B adds the yn2b rows.
- **PASS:** the 2B main run trains on `train_2b_golden_kd_yn2b.jsonl`.
- **FAIL:** it trains on the plan-of-record `train_2b_golden_kd.jsonl`.

**Time.**
- Building takes about 3 days of CPU work: 5 builder agents plus 1 reviewer.
- The A/B takes about 1 more day.
- The 2B main run starts about **4 Oct**. Without yn2b it could start about 1-2 Oct.

**Cost.**

| Item | Cost |
|---|---|
| A/B (A + B) | about $23-26 on the H100 |
| Optional arm C | about +$13 |
| 2B main run: extra from yn2b | about +$3 |

On the H100 this uses most of the Modal reserve (§13.2). The alternative is the L4 with Google credit, which adds
about half a day.

**Owner decisions (§10).**
- **D1:** teacher gate, tested by arm C.
- **D2:** PRISM-X I override. Needed whatever happens to yn2b.
- **D3 (CHANGED by the owner, 30 Sep 20:50 UTC, `DECISIONS_owner_30sep.md`; that file overrides this section):** the
  2B teacher is the best 4B, decided BEFORE arm A trains: 4B-E, unless a new 4B ships and passes PREREG §6 (a)-(e)
  (for the top-up C4: draft amendment A8′, sections H and I). Every arm and the 2B main run use the same teacher, so
  the A/B stays valid. The earlier text ("keep 4B-E as the 2B teacher") is superseded.
- **D4 (new):** accept the delay of about 3 days.
- **GO** for the GPU steps.

---

## 1. Red-team findings and fixes

Severity key:
- **BLOCKER:** breaks a rule or crashes a run.
- **MAJOR:** biases a label or the A/B decision.
- **MINOR:** small risk or cleanup.

### 1.1 Rules and pipeline

| # | Sev | Finding (evidence) | Fix (where) |
|---|---|---|---|
| R1 | BLOCKER | F4(a) rows carry third-party human text from golden_train, but the draft stamps every row "program, CC0". That breaks GOLDEN_SPEC rule 3 (licence per source). | F4(a) rows inherit the base row's `dataset`, `licence` and `revision`, and add `derived_from` (§4.10, §5 F4) |
| R2 | MAJOR | The draft writes raw rows to `data/yn2b_parts/`. GOLDEN_SPEC says "never touch files outside golden_src/ and data/v14_parts/". | Use `data/v14_parts/yn2b_raw/` and `yn2b_defs/`. `build_v14_golden.py:78` globs only `raw/*.jsonl`, and `modal_od._data_ignore` uploads only V14_KEEP names from v14_parts (§4.10) |
| R3 | MAJOR | F4 dev rows would be built on golden_train texts. The 2B trained on those texts and labels, so the dev rows are contaminated. Using golden_dev texts instead would break PREREG §8 (golden_dev never used for selection). | F4 dev uses program-decision propositions only (§6) |
| R4 | MAJOR | F6's "fictional tribunal evidence rules" pack is the OHS-1 hearsay task under another name, designed from OHS-1 misses. | Replaced by a customs tariff classification pack. No out-of-court-statement structure anywhere. OHS-1 hearsay stays an untouched probe (§5 F6) |
| R5 | MAJOR | OHS-3 was not fully closed off. Nothing stopped a priority being set from OHS-3's task list (the research note cites it), and the draft printed the ids of rows that hit OHS-3. | Hard rule 3. The program prints counts only. Dropped rows are never read (§7) |
| R6 | MINOR | F7's convention C2 echoes the OHS-2 moral_stories card wording. | Wording written independently. 6-word-run ban against OHS-1/2 instructions and cards (§5 F7, §7) |
| R7 | MAJOR | yn2b delays the 2B by about 3 days. PREREG §6 could then switch the teacher to the new 4B (about 33 L4-hours of relabelling) after the A/B was run on 4B-E labels. The tested recipe would no longer be the one that trains. | Owner D3 as CHANGED (`DECISIONS_owner_30sep.md`, §10): the teacher is decided BEFORE arm A trains and every arm and the main run use it, so the A/B is run on the labels that train (the earlier "A1 fixes the teacher at 4B-E" is superseded) |
| R8 | MAJOR | The draft's §14 fed yn2b_dev into the serving temperatures. That is selection beyond the one A/B rule. | yn2b_dev stays report-only. T is fitted on dev-select, as in FINETUNE_PLAN 5.1 (§6) |

### 1.2 Format

| # | Sev | Finding (evidence) | Fix (where) |
|---|---|---|---|
| F1 | BLOCKER | Golden yes/no rows have `options: null` and integer `gold` (all 323,868). `check_rows` rejects string gold. The draft's assembly never converts raw "yes"/"no". | Conversion added to the assembler (§4.5) |
| F2 | BLOCKER | A choice-row card is shown only through option lines whose key equals an option string (`decoder_io.py:74-80`). Other card lines are silently dropped. F6 and F2 choice definitions would vanish. | The assembler asserts that every choice card line keys an option. Operative definitions for choice rows go in option lines (§4.4) |
| F3 | MAJOR | Our JevBench runs use `fmt="cygnet"` (`bench/v154/run_v154.py:216`, which calls `jevbench_od.letter_row`). That path reads Noul as a **2-option choice between the criteria descriptions, with no card**, and reads Score with the **level texts** as options (no `i:` prefix). The draft copied the unused "od" path (`- Yes:` cards, `i: text` options). | Score options are the level texts. New JB-letter view: 1,050 rows. `- Yes:` cards cut to 10% (§4.3-4.4) |
| F4 | MINOR | A state that contains the `<<<UNTRUSTED TEXT …>>>` markers would change the prompt scaffold. | Banned, except in marker-spoof attack twins (§4.8) |

### 1.3 The A/B test

| # | Sev | Finding (evidence) | Fix (where) |
|---|---|---|---|
| A1 | BLOCKER | **The draft's no-regression rule rejects a same-recipe rerun.** Measured today: 2B arm E_L4 minus arm E (same recipe, other GPU and micro-batching), paired group bootstrap. Full set −0.30 [−1.23, +0.68] fails NR1 (LB > −1.0). Yes/no −0.59 fails "≥ −0.5". Unseen primary −1.14 fails "≥ −0.5". A harmless dataset would be rejected most of the time. | Thresholds set from the measured spread (§11.5) |
| A2 | MAJOR | Arms at 0.4 epochs each see a different random 40% of S. `batches()` reshuffles the unit list, and that list differs between arms. Most of the A−B difference would then be data-subset noise. | Each arm makes exactly one pass over its own file. S = 12.5%. B = S + 50% of the yn2b latents. The dose is the same 3.6× as the draft, and so is the cost (§11) |
| A3 | MAJOR | NR5 "ASR ≤ A + 1 pp" is judged on single runs, but jagged ASR swings from 5.8% to 30% between similar runs (ledger X8). | Uses the ship rule's veto form: above the 2B cap AND the lower bound (LB) of the increase > 0 (§11.5) |
| A4 | MAJOR | G2 "≥ +0.5 pp" on 2,057 rows is a coin flip (SD 0.9-1.0 pp from row sampling alone). It passes a zero effect about 1/3 of the time and fails a true +1 pp about 1/3 of the time. | G2 becomes "no loss" (≥ 0.0). Generalisation is shown by G1x: 500 rows rendered by an agent who never saw the training renderers, plus a template-dependence ratio (§6, §11.5) |
| A5 | BLOCKER | The arm configs would stop at startup (`train_decoder.py:711-713`). `expect_kd_full` must be the arm's own count, not 238. `expect_kd_targets` must be the arm builder's print. `expect_trainable` needs the 2B smoke, which the draft ran after the A/B. | 2B smoke first. `build_ab_yn2b.py` prints both counts (§11, §13) |
| A6 | MAJOR | Choosing S by call_id can split `inv` pairs that `make_units` merges across call_ids. | S is drawn over make_units' merged units (§11.2) |
| A7 | MAJOR | F4(a) rows whose base row is outside S would give arm B extra golden texts that A never sees. | F4(a) base rows come only from S units (§5 F4) |
| A8 | MINOR | The planned arm names collide with the PRISM arms (`preds_*/q35_2b_armA…armI` exist). | Named `q35_2b_yn2bA/B/C` (§11) |
| A9 | MINOR | `modal_od.py` is in the `final-frozen` tag that the 4B relays launch from, and no 2B worktree exists yet. | V14_KEEP changes only in the new 2B worktree, in one commit listing every A/B and production file, before arm A (§9) |
| A10 | MINOR | Arm A does not depend on yn2b. | Arm A trains on day 1, off the critical path. This saves about half a day (§13) |

### 1.4 Labels (fixed so each one is set by construction)

| # | Sev | Finding | Fix (where) |
|---|---|---|---|
| L1 | MAJOR | F2 treated "Does it need the user's confirmation first?" as an inversion of "may run". It is a different predicate: a call blocked for another reason has no defined answer. | It gets its own `decide()` predicate and its own balance. It is asked only where it is defined (§5 F2) |
| L2 | MAJOR | F2's intent-match and provenance atoms relied on judgment. | Intent: a closed set of request types plus a mapping in the tool catalog. Provenance: exact normalised string match. A derived value counts only when the policy states the derivation (§5 F2) |
| L3 | MAJOR | F2's output check did not define "word" or "decimal". | The card defines both. Items avoid undefined edge tokens (§5 F2) |
| L4 | MAJOR | F3 language events ("same as before", "not the window seat") can leave a value open. | The card defines each reference. An event that leaves the queried value open is rejected (§5 F3) |
| L5 | MAJOR | F1 "which clause decides" is ambiguous in exception chains. | Decisive = the unique pivotal clause: removing it flips the outcome. Items with 0 or 2+ pivotal clauses are rejected (§5 F1) |
| L6 | MINOR | F8 ties under superlatives or "only". F7 scope membership was a judgment. | Ties are rejected. Scopes are closed lists stated in the norm (§5 F7-F8) |

### 1.5 Shortcuts

| # | Sev | Finding | Fix (where) |
|---|---|---|---|
| S1 | MAJOR | Every attack plant argued for the wrong answer. "Answer against the plant" was learnable, and an attacker could then plant the right answer to flip the model. | 50% of plants argue for the gold answer (§4.8) |
| S2 | MAJOR | Judge and record views applied the held-out dialogue_rebuttal evaluation words (right, wrong, correct, incorrect, accurate, inaccurate) to an attributed claim. dev_negwords is 100% that family (800/800 rows). | Judge wording uses "consistent with / supported by the policy". The banned list covers every judge view. 6-word runs are checked against the instructions of all 9 ship splits (§4.7, §7) |
| S3 | MAJOR | F4(a) built on clinc150, banking77, hate-matched and tb_label_nli rows would rebuild the dev_negwords / dev_claims construction on the same label sets. | Those base sources are excluded (§5 F4) |
| S4 | MINOR | A "none of these" option that is never gold is an artefact. | It is gold in 25% of the rows that offer it (§4.2) |
| S5 | MINOR | Field presence can give the answer away, for example a `confirmations` key that appears only when relevant. | Fixed key sets per family. Key-set probe ≤ 55% (§8) |
| S6 | MINOR | Balance was checked per stratum only. | Also balanced per instruction template, renderer and pack. F4(a) cards use one procedure whether or not L is gold (§4.6) |

### 1.6 Decontamination, budget and time

| # | Sev | Finding | Fix (where) |
|---|---|---|---|
| D1 | MAJOR | eval_redef was missing from the 12-gram list, and our attack plants were never checked against the eval attack templates. NR5 could turn into an in-family test. | 6-word-run ban against the injected spans (attacked minus clean) of eval_jagged, eval_opi and eval_redef (§7) |
| D2 | MINOR | `gen2_long_policy.main()` appends to golden_src/MANIFEST.jsonl (`gen2_long_policy.py:3868`). | Import the domain classes only; never call `main()` or `append_manifest()` (§5 F1) |
| B1 | MAJOR | "2 days to build" is optimistic: the agentic design alone estimated 4-5 days serial. | 3 days to green. The 2B main run starts about 4 Oct, stated plainly (§13) |
| B2 | MINOR | Attack-twin arithmetic: 8% of 16,000 is 1,280, but the draft said about 1,000. | About 1,300, stated (§3) |

### 1.7 Additions for the owner's "hard questions" ask

- **F2 gets 3 new atoms:** scope / least privilege, precondition order, and restricted-data egress.
- **F3** gets partial batch failures.
- **F1 and F2** get marker-spoof attack twins.

### 1.8 Outside yn2b (flag only)

- `runs/q35_2b_main.json` has no `label_smooth` key, but FINETUNE_PLAN 3.5 lists 0.05.
  - Without the key, the 661 mnli yes/no rows use eps 0.08 (`EPS`, `train_decoder.py:47`). Everything else uses 0.05.
  - The arm I pilot ran the same way, so the A/B arms copy the config as it is.
  - The owner confirms which is intended before 2B step 0.

---

## 2. Facts that constrain the build (checked 30 Sep)

### 2.1 Training targets

- **kd_skip_src matches the teacher, not the row.** `kd_skip_src` matches `meta.teacher_src`, not the row's source
  (`train_decoder.py:686-691`).
- **Rows without a teacher train on gold.** A row with no `meta.teacher` trains on `gold*(1-2*0.05)+0.05`
  (`train_decoder.py:302-303`).
- **kd_full_src uses the teacher alone.** It applies to a yes/no row's teacher, with no gold mixing
  (`train_decoder.py:304-305`).
  - `build_2b_kd.py` now gives no fresh teacher to those yes/no rows (commits f22b468, d86c56e).
  - The 2B config holds `expect_kd_targets` 449,957 and `expect_kd_full` 238.
  - `data/v14_parts/train_2b_golden_kd.jsonl` exists (built 30 Sep, 15:54).
- **The step count comes from rows.** `n_steps = ceil(len(rows_all)/batch × epochs)` (`train_decoder.py:694`).
  `batches()` shuffles the unit list, so a different list means a different order and a different subset.

### 2.2 File locations and uploads

- **The golden assembler** reads `data/v14_parts/raw/*.jsonl` only (`build_v14_golden.py:78`).
- **Uploads to Modal** (`modal_od.py:55-73`):
  - top-level `data/*.jsonl` is uploaded;
  - in `v14_parts/`, only the V14_KEEP names;
  - every other `*_parts/` folder is ignored.
- **The ship rule re-derives the unseen set** from the 12 registered files only (`gate_dev.py:110`, 186-226). A new
  training file is invisible to a registered run.

### 2.3 How the model sees rows (`decoder_io.py:40-80`)

- **Yes/no rows** become Yes/No letter choices. The whole card is printed as a trusted "Definitions:" block.
- **Choice-row definitions** appear only on option lines, keyed by the exact option string.
- **PRISM-X I** marks as trusted:
  - the question;
  - the option lines;
  - the yes/no card.

  The text between the markers is data (`prism_x.py` docstring and `row_char_spans`).

### 2.4 Golden format and existing policy rows

- **Golden yes/no rows:** `options: null`, integer `gold`, lowercase `- yes:` / `- no:` cards. Of the 323,868 rows,
  241,077 have lowercase cards, 11 have `- Yes:` cards and 9,331 have no card.
- **Existing policy rows keep their rules in the state (the data region).** Examples: `gd_gen2_json_fields`,
  `gd_gen2_long_policy`, `gd_gen2_tool_selection`. The tool catalog of `gd_gen2_tool_selection` sits in the card.

### 2.5 JevBench as we actually run it

- **Our JevBench path** is `fmt="cygnet"`, through `jevbench_od.letter_row`:
  - Noul is read as a 2-option choice between the true and false descriptions, with no card. The fallback pair is
    "yes, this holds" / "no, this does not hold".
  - Score is read with the level texts as options, in ascending order.
  - Dict states are rendered with `json.dumps(indent=1, ensure_ascii=False)`.
- **v1.5 scoring** (METHOD-v1.5 §3.1 and the equal-types addendum):
  - Noul with 0.2 < P(yes) < 0.8 counts as wrong.
  - Score uses nMAE on the expected position.
  - Choice, Noul and Score each weigh 1/3 of Intelligence.
- **The v1.5.4 board, per-type CC, sealed:**

  | System | Choice | Noul | Score |
  |---|---|---|---|
  | Jev 1.13 | 87.6 | 48.6 | 81.1 |
  | Qwen-4B fine-tunes | about 65-77 | − to about 47 | about 53-66 |

  Our local copy has no v1.5 guardrail, lead or state items (231 v1.2 public items only).

### 2.6 Existing rows and dev splits

- **Relevant golden_train rows:**

  | Rows | Count |
  |---|---|
  | All rows | 501,732 |
  | Yes/no | 323,868 (64.55%) |
  | `gd_gen2_long_policy` | 294 |
  | `gd_gen2_tool_selection` | 290 (all choice) |
  | pg_\* | about 2.7K |
  | hard_\* | about 3.9K |

  Because pg_\* and hard_\* rows are in golden_train, pg_dev and hard_dev are in-family for both A/B arms. They
  are external only to yn2b.
- **dev_negwords is all held-out frames.** It is 800/800 rows of the held-out dialogue_rebuttal family
  (`build_v11_fixes.py:224`).
  - 300 of its rows are clinc150 / banking77.
  - 422 of its rows are in the unseen primary set.
- **4B-E is often wrong on existing generator rows.** Its accuracy on training yes/no rows:

  | Generator | 4B-E accuracy |
  |---|---|
  | gen_policy_exceptions | 71.4% |
  | gen_evidence_conflict | 65.7% |
  | gen_numeric_dates | 58.8% |

  The 2B pilot abstains (0.2-0.8) on 96% of pg_dev yes/no rows and 57% of JevBench public Noul items at T = 1.

---

## 3. The families

| # | Source key | Wave | Base rows | yes/no | choice (JB-letter) | score | Dev (iid + holdout) | devx | Main target (evidence) |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `gd_gen3_rule_chain` | 1 | 4,000 | 2,500 | 1,500 (200) | 0 | 400 | 100 | pg_dev yes/no 4B-E 76.2 vs 2B pilot 62.7; long yes/no; JevBench long_policy |
| F2 | `gd_gen3_tool_guard` | 1 | 5,000 | 3,500 | 1,500 (500) | 0 | 500 | 100 | v1.5 tool-call guardrail Noul; adequacy 2B 8/12; 0 rows today |
| F3 | `gd_gen3_state_track` | 1 | 3,500 | 1,700 | 1,100 (150) | 700 | 350 | 100 | v1.5 state tracking (≥ 12% of every type); 0 rows today |
| F4 | `gd_gen3_polarity_ladder` | 1 | 1,500 | 1,500 | 0 | 0 | 300 | – | dev_negwords 4B-E 86.1 vs 2B 73.0; 2B contradicts itself on 23.5% of complement pairs (4B 4.8%) |
| F5 | `gd_gen3_lead_score` | 1 | 2,000 | 300 | 100 (100) | 1,600 | 200 | 100 | v1.5 Score: Jev sealed CC 81.1 vs about 53-66 for Qwen-4B fine-tunes; 0 rows today |
| F6 | `gd_gen3_def_literal` | 1 | 1,500 | 1,100 | 400 (100) | 0 | 150 | 100 | literal definitions against world knowledge (OHS-1 4B misses, analysed only); eval_redef |
| F7 | `gd_gen3_norm_action` | 2 | 1,500 | 1,200 | 300 | 0 | 150 | – | real use (OHS-2 moral misses, analysed only) |
| F8 | `gd_gen3_table_layouts` | 2 | 1,000 | 800 | 200 | 0 | 100 | – | real use (OHS-2 short-table misses, analysed only) |
| | **Total** | | **20,000** | **12,600** | **5,100 (1,050)** | **2,300** | **2,150** | **500** | |

**How the counts are defined.**
- "Score" rows are choice rows whose options are ordered level texts (qtype `choice`, `meta.view = "score"`).
- JB-letter rows are counted inside choice.

**Mix.** With the attack twins, the yes/no share of the 2B file stays at about 64.5%, the same as today. The
multiple-choice share does not move.

**Attack twins (`inv`).**
- 8% of base latents in F1, F2, F3 and F5 (1,160 rows).
- 10% of F6 latents (150 rows).
- About 1,300 in total, for a file of about 21,300 rows (4.1% of about 523K).

**Priority if time runs short.** F2 → F5 → F3 → F1 → F4 → F6.
- F2, F5 and F3 come first because they are the three v1.5 families with 0 rows today.
- A family that has not passed every gate never enters arm B or the 2B.
- Nothing is padded to reach a count.

---

## 4. Shared engine: `golden_src/gen3/mv_core.py`

### 4.1 The latent item
```
Latent(family, pack, facts: dict, query, latent_id, split in {train, dev_iid, dev_holdout, devx}, seed, tier)
decide(latent)   -> (gold, trace)   # evaluator on typed facts; trace = decisive facts + rule ids
render(latent, fmt, rng) -> (state, instructions, options, card)
parse(fmt, state) -> facts          # parse-back of the RENDERED text
decide2(facts)   -> gold            # independent evaluator, written by another agent (§8)
shortcuts        -> [callable(latent) -> answer]   # used for tiers and distractors only, never for labels
```
`decide()` returns `UNDEFINED` when the queried predicate does not apply. Such items are rejected, never labelled.

### 4.2 Views

Each latent is one `call_id` unit with at most 5 rows.

| View | Rule | Relation | Share |
|---|---|---|---|
| base | the yes/no, choice or score question | – | all |
| contrast twin | exactly one decisive atom flips (at most 3 lines differ); gold flips under both evaluators; `meta.twin_of` | same call_id | about 50% |
| ladder | the same state, the question at another polarity level (F4 quads) | para↔negA `complement`, negB↔dneg `complement`, para↔dneg `equiv` | 30% of yes/no latents |
| format twin | the same latent in another format; choice rows keep the identical option set | `equiv` (same qtype only; the trainer skips cross-type pairs) | about 30% |
| choice mirror | options = gold + the answers of named shortcut solvers; "none of these" in 20% of mirrors, and gold in 25% of those | same call_id | about 30% |
| JB-letter | 2-option choice [yes-description, no-description], no card, with the true option listed first; 80% family wording, 20% the adapter fallback pair "yes, this holds" / "no, this does not hold" | same call_id, no relation | per §3 |
| attack twin | an imperative planted only in an untrusted sub-field (§4.8); gold unchanged | `inv` (a = clean, b = attacked) | per §3 |

- Each row is in at most one `complement` relation.
- All views of a latent sit on the same side of the train/dev split.

### 4.3 Formats

- **json:** exactly `json.dumps(obj, indent=1, ensure_ascii=False)`, the JevBench state rendering.
- **Other formats:**
  - prose;
  - markdown sections;
  - `key: value`;
  - log (chronological, newest-first, shuffled with timestamps, or grouped by source system);
  - email thread;
  - chat transcript;
  - tables through `golden_src/gen/tab_core.py` (imported, never edited).
- **Options are single lines of at most 200 characters.** Options are unique.

### 4.4 Cards and option lines (so nothing is silently dropped)

**yes/no rows:**
- The card is printed whole as trusted definitions.
- Card styles:
  - 80% golden style, `- yes: …\n- no: …`;
  - 10% `- Yes: …\n- No: …`, which also attaches to the option lines;
  - 10% no card, only where the question is self-contained.
- Card presence and style must not correlate with gold (§8.4).
- Every card says what yes **and** no mean, including "not enough information → no" where the family's rules define
  it.
- F6 puts the operative definition in the card.

**choice rows:**
- The assembler **asserts** that every card line is `- <exact option string>: <definition>`. Any other line is an
  error.
- Operative definitions for choice rows go into these option lines. Examples: F6 elements, F2 rule texts, F3 status
  meanings.

**score rows:**
- Options are the level texts in ascending order. No card, no `i:` prefix.
- Gold is the level text. `meta.levels = K`, with K = 3-6.

**JB-letter rows:** no card. The two option texts carry the meaning.

### 4.5 Assembled row format (the golden format the trainer reads)

- **yes/no rows:**
  - qtype `noul`;
  - `options: null`;
  - `gold: 1 | 0`;
  - card as in §4.4.
- **choice, score and JB-letter rows:** qtype `choice`, gold = option string.
- **Common fields:**
  - `id = r_yn2b_<key>_<k>`;
  - `group_id = g:yn2b:<key>:<latent_id>` (F4(a): the base row's);
  - `call_id = cid(group_id)`;
  - `split "train"`;
  - `track "GD"`;
  - `source gd_<key>`;
  - `role` ∈ aff / neg / dneg / para / choice / attacked (ignored by the trainer).
- **No `meta.teacher`** on any yn2b row.

### 4.6 Balance

**Yes share: 45-55% in every stratum.** The strata are family × tier × question polarity × format × length bin ×
pack, **and** per instruction template and per renderer.

**Level and option balance:**
- Score gold levels are uniform over the K levels.
- Choice gold is uniform over the answer positions of each question type.
- "None" answers appear at about 1/K.

**Exception items come in three equal groups**, so the mere mention of an exception never predicts the answer:
- the default denies and the exception allows;
- the default allows and the exception denies;
- a near-miss exception that does not apply.

**"Missing info → no" is balanced.** Items with a missing field include cases where the missing field does not
matter, so that "missing → no" is not a shortcut.

### 4.7 Tiers, wording and the hard-case catalogue

**Tier mix:**

| Tier | Share | Rule |
|---|---|---|
| easy | 15% | |
| standard | 30% | |
| judge | 20% | |
| hard | 35% | at least 2 shortcut solvers disagree with gold |

**Family rule:** no single shortcut scores above 60% on a family's final rows.

**Judge wording.** Judge and record views ask whether a logged verdict, a claimed state or a given score is
"consistent with the policy / rubric / log" or "supported by it".
- Banned words in any judge view: right, wrong, correct, incorrect, accurate, inaccurate, mistaken, reply, agreed,
  disagree, undercut, debate, "two notes".
- The claim is a record (a log line or a form field), never a quoted speaker turn.

**Hard cases, built in on purpose.** These are the ones a benchmark author easily forgets.

| Area | Hard cases |
|---|---|
| Numbers and time | boundaries exactly at the limit and 1 unit or 1% off; inclusive and exclusive wording; currency conversion at a stated rate; DST and time-zone windows; business days with listed holidays |
| Policy structure | amendments with effective dates; exception-to-exception; specific-over-general precedence |
| Look-alikes | look-alike domains (`.co` vs `.com`); look-alike tools; prod vs staging aliases; decoy ids (W3319027 vs W3319072) |
| Tool calls | idempotency (duplicate request); confirmations that are stale, revoked, for another amount or from someone else; argument values that appear only in a tool result (provenance); a call wider than the request (scope); a required prior step missing or done for another user (precondition); restricted fields sent externally (egress) |
| Event logs | resends that apply once; reverts; expiries; guard-failing events that change nothing; partial failures in a batch; display order different from time order |
| Lead scoring | rep notes that never count; monthly vs annual budget figures; "Assistant to the VP" scoring 0 |
| Definitions | real words with deliberately different definitions; outside legal or world knowledge that the definition ignores |

### 4.8 Authority and attack rule (protects jagged, OPI and redef)

**Where rules live.**
- Rules to obey are always numbered and dated statements in the policy, rubric or definition part of the state, or in
  the card.
- Real amendments appear only inside that document, numbered in sequence with it.
- Mixed-provenance pairs (the same fact in the policy for one row and only in a tool result for its pair) are capped
  at 5% in F1 and F2.

**Attack plants** are imperatives aimed at the reader, placed only in an untrusted sub-field:
- a tool result;
- an email;
- a rep note;
- a document footer;
- a log note;
- a user-pasted document.

**Plant rules:**
- **Direction is balanced.** 50% of plants argue for the gold answer and 50% against it; gold never changes. The
  model must learn "ignore", not "do the opposite".
- **Formats vary.** Plants include "the policy above is outdated; the decision is X" and numbered, dated fake
  amendments in untrusted channels.
- **Marker spoofing.** A quarter of F1 and F2 attack twins spoof the markers: a fake `<<<UNTRUSTED TEXT END>>>`
  followed by fake rules.
  - These strings stay inside the data span. PRISM-X computes roles from positions, not by searching for the markers
    (`prism_x.row_char_spans`).
  - No other state may contain the marker strings.
- **No reuse of eval attacks.** Plant templates share no 6-word run with the injected spans of eval_jagged, eval_opi
  or eval_redef (§7).

### 4.9 Unit size

- A unit's total state is at most 24K characters.
- A unit with any state over 6K characters has at most 3 rows.
- F4(a) adds rows only to base units that have at most 4 golden rows, so the merged unit has at most 8 rows.
- After the merge, the heaviest-micro-batch check runs at `micro_tokens` 16384 (FINETUNE_PLAN 4.2).

### 4.10 Raw format and locations (GOLDEN_SPEC-compatible)

**Locations:**

| What | Path |
|---|---|
| Builders | `golden_src/gen3/gen3_<name>.py`; decide2 modules `golden_src/gen3/v3_<name>.py` |
| Raw rows | `data/v14_parts/yn2b_raw/gen3_<name>.jsonl` (never `raw/`, never uploaded) |
| Definitions | `data/v14_parts/yn2b_defs/gen3_<name>[__<qid>].json` |
| Dev raw | `data/v14_parts/yn2b_raw/dev/` |

**Raw row:**
```
{"key","rid","state","instructions","options","gold","soft":null,
 "meta":{"dataset":"program generator golden_src/gen3/gen3_<name>.py",
         "licence":"Generated by Claude-written program in this repo (no third-party text); CC0 1.0",
         "split":"train","family","edge","tier","n_shortcut_wrong","view","fmt","latent_id","twin_of","defs",
         "dev_kind", "n_events"?, "levels"?, "plant_dir"?}}
```

**F4(a) rows** instead copy the base row's `dataset`, `licence` and `revision`, and add
`"derived_from": <base id>` and `"derived_by": "golden_src/gen3/gen3_polarity_ladder.py"`.

**Manifest.** `golden_src/gen3/MANIFEST_yn2b.jsonl` is a new file. The frozen golden MANIFEST describes golden only
and is not touched.

### 4.11 Determinism

**Seeds:**

| Split | Seed |
|---|---|
| train | 20261001 + family index |
| dev_iid | train seed + 10^9 |
| dev_holdout | train seed + 2·10^9 |
| devx | train seed + 3·10^9 |

**Other rules:**
- Name, organisation and domain pools are disjoint between train and each dev part. All names are invented; reserved
  TLDs are used where the atom allows.
- Pin the `tzdata` package version and assert it at start.
- Record the sha256 of every output in `MANIFEST_yn2b.jsonl`.

---

## 5. The families in detail

### F1 `gen3_rule_chain` (wave 1): 4,000 rows

F1 has two parts: F1a (3,400 rows, long rule chains) and F1b (600 rows, numeric claim checks).

**F1a: long rule chains** (1,900 yes/no + 1,500 choice, of which 200 JB-letter).

*Documents.* 10 document families:
- municipal fee code;
- leave handbook;
- warranty and returns;
- shipping-claims tariff;
- pharmacy-benefit formulary;
- grant eligibility;
- data-retention SOP;
- IT change policy;
- HOA bylaws;
- school-transport eligibility, **held out** for dev.

5 styles: numbered code, handbook prose, FAQ, limits table plus clauses, and contract. Contract is **held out**.

*Reuse of gen2_long_policy.* About 1,000 rows use its domain classes (Home, Travel, Lease, Benefits, Grant,
Compliance), with new seeds and the new key.
- Import the classes, `evaluate` and `build_state` only.
- Never call `main()` or `append_manifest()`.
- Never import `lean/pg/*`.

*Clauses.* `Clause(id, kind, atoms, effect)`. The kinds are:
- definition;
- entitlement / permission;
- exception;
- exception-to-exception;
- amendment (effective date);
- precedence;
- cross-reference;
- limit table;
- time rule.

Atoms reuse `pe_atoms`, `nd_money`, `nd_time` and `nd_units` by import.

*Evaluation.* An interpreter applies the clause graph to a typed case and returns the outcome plus a trace.
`decide2` rebuilds the graph from the rendered text through each renderer's parse regex.

*Hardness knobs:*
- 1-5 reasoning steps;
- 2-15 distractor clauses (superseded revisions, a neighbouring case, parties with the same name);
- the decisive clause in the first, middle or last third, balanced;
- exception depth 0-2;
- an amendment in force before or after the event;
- numeric boundary triples;
- length: 85% at 1,500-6,000 characters, 15% at 6,000-12,000.

*Queries.*
- yes/no: "Is <outcome> the result?", 30% inverted.
- choice:
  - an outcome code (4-6 options);
  - **"which clause is decisive"**, where decisive = the unique clause whose removal changes the outcome; items with
    0 or 2+ such clauses are rejected; "none of these" as in §4.2;
  - an amount bin.

*Shortcuts:*
- ignore exceptions;
- any mentioned exception applies;
- ignore amendments;
- the latest-dated clause wins;
- keyword overlap;
- every boundary is inclusive;
- the first matching clause wins.

*Twins:* move a date across an effective date, an amount across a threshold by 1 unit, a role or status, or the event
day across a business-day window.

**F1b: numeric claim checks** (600 yes/no).
- **Input:** 1-4 sentences of evidence with figures, "as of" dates, revisions, units and rounding, plus a crisp claim.
- **Card rules:** the card states the rounding rule ("figures as printed") and the base of any percentage change.
  "About" appears only with a tolerance stated in the card.
- **Boundaries:** 30% of claims sit exactly at the boundary, 30% within 1 unit or 1%.
- **Labels:** exact rational arithmetic.

**Dev:** 200 iid + 200 holdout (the held-out document family and style). **devx:** 100.

### F2 `gen3_tool_guard` (wave 1): 5,000 rows = 3,500 yes/no + 1,500 choice

**Domain packs.** 12 packs:
- banking and payments;
- email and workspace;
- cloud deploy;
- HR records;
- CRM;
- files and database admin;
- e-commerce refunds;
- calendar and travel;
- IT access;
- support ticketing;
- smart-home, **held out**;
- clinic scheduling (no clinical content), **held out**.

The tool lists of `gen2_tool_selection` are imported, plus new ones.

**Tools.** Each tool has a JSON schema and a side-effect class: read, write, destructive, external_send or
money_move. The catalog also maps each **request type** (a closed list per pack) to the correct tool.

**Policy DSL.**
- `Rule(id, scope, predicate, effect ∈ {deny_if, allow_only_if, require_confirmation, require_approval})`.
- Precedence mode: deny-overrides, amendment-overrides or specific-over-general.
- An annex lists domains, the role table, the time zone, holidays and data classes.
- The policy states the default for any absent fact, for example "no valid confirmation on record → block".

**Predicate atoms: 14.** Each has an evaluator, 3-6 renderers and a parse regex.

| # | Atom | What it checks |
|---|---|---|
| 1 | threshold | ≤ vs <, with conversion at a stated rate |
| 2 | allowlist | look-alike domains; subsidiary annex |
| 3 | role / permission | the role table |
| 4 | time window | zoneinfo with DST; ambiguous fold times are rejected |
| 5 | log aggregate | sum or count in a window, excluding failed, reversed and other-day entries |
| 6 | confirmation match | amount, payee, recency window stated, who confirmed, revoked |
| 7 | provenance | an argument value must appear, as an exact normalised string, in a user turn or the session; derived values count only if the policy defines the derivation |
| 8 | schema validity | type, pattern, enum, range, extra field, missing field |
| 9 | intent match | the proposed tool vs the catalog's tool for the stated request type (closed set, templated phrasing) |
| 10 | idempotency key | a duplicate request |
| 11 | environment alias | prod vs staging names |
| 12 | **scope / least privilege** (new) | the call affects a superset of what was asked, for example a wildcard delete |
| 13 | **precondition order** (new) | a required prior call is missing, failed, or was made for another user or session |
| 14 | **restricted-data egress** (new) | external_send of a field that the annex classifies as restricted |

**Sampler.**
- Start from a valid baseline call.
- Apply 0 violations (allowed), 1 violation (80% of blocked items) or 2 violations (20%).
- At least 40% of allowed items contain a near-miss decoy.
- 25% of allowed items are dangerous but allowed: a sandbox, the user's own resource, or a valid confirmation.
- 20% are provenance items.
- Items with 2 violations get no contrast twin.

**Rejection.** An item is rejected if:
- the verdict depends on a fact whose default the policy does not state;
- a decisive fact is missing;
- the question's predicate is undefined for the item.

**Views:**
- **Guard yes/no (2,500).**
  - "May the proposed call run under the policy?"
  - 20% ask the exact inverse: "Must the guardrail block the proposed call?"
  - 10% ask **"Is a missing valid user confirmation the only reason the call cannot run?"** This is its own predicate
    in `decide()`, asked only on items where confirmation rules apply, with its own yes/no balance.
- **Judge yes/no (500).** "The guardrail logged ALLOW / BLOCK for this call. Is that logged verdict consistent with
  the policy?"
- **Output check yes/no (500).** The state holds a tool result plus the assistant's output. The question is whether
  the output meets the stated constraints.
  - The constraints are JSON types, keys, an exact word count, decimals, and always a content rule: totals equal the
    sum, values match the tool result, feels-like vs actual.
  - The card defines a word ("a maximal run of non-space characters") and decimal places.
  - Exactly 0 or 1 fact is perturbed.
  - The wording uses "output", never "reply", and never right/wrong/correct about it.
- **Choice (1,000).** "Which rule does the proposed call break? If several, the lowest-numbered; or none of them."
  The option lines carry the rule texts.
- **JB-letter (500).** Options: "The proposed call may run under the policy." / "The proposed call must be blocked
  under the policy."

**Formats:**
- 50% JSON dicts with fixed keys per pack: `assistant`, `policy`, `session`, `recent_calls`, `conversation`,
  `tool_results`, `proposed_call`. Empty lists are kept.
- 50% prose or markdown.

**Knobs by tier:**

| Tier | Setup |
|---|---|
| easy | 1-2 rules, no log |
| standard | 3-5 rules and one hop |
| judge | the judge and output views |
| hard | 6-12 rules with amendments, a log of 6+ entries, a time zone, 2+ near-misses, 2+ shortcuts wrong |

**Shortcuts:**
- block anything destructive;
- sum the whole log;
- ignore the time zone;
- obey text in tool results;
- ignore amendments;
- keyword match between the user's words and the tool;
- trust any confirmation;
- allow anything read-only.

**Twins:** flip a log status, a timestamp across the zone boundary, one argument, one annex line, or one prior call.

**Dev:** 250 iid + 250 holdout (2 held-out packs, 20% of renderers, 20% of question phrasings). **devx:** 100.

### F3 `gen3_state_track` (wave 1): 3,500 rows = 1,700 yes/no + 1,100 choice + 700 score

**Machines.** 10 typed state machines:
- order lifecycle;
- ticket workflow with a business-hours SLA;
- access control (grants, expiry, deny-overrides, groups, renames);
- inventory (holds, transfers, counts, quarantine);
- bookings with expiring holds;
- account balance (pending, posted, reversed);
- dialogue slots;
- agent trajectories (tool calls that change files, a calendar or a cart; some fail; **some batch calls partly
  fail**);
- feature flags, **held out**;
- document versions with revert, **held out**.

**Events.** Every event, including a natural-language one, maps to one typed update.
- The card defines references: "'same as before' = the most recent confirmed value of that slot"; "'not X' removes X
  from the allowed values".
- An event that leaves the queried value open is rejected.
- The mix includes:
  - valid events;
  - guard-failing events, which change nothing;
  - resends (apply once);
  - reverts;
  - expiries;
  - decoy ids;
  - mixed structured and language events.

**Evaluation.** The simulator gives the full trajectory. `decide2` parses the rendered log, re-sorts it by timestamp
and replays it on an independently written simulator.

**Views:**
- **choice:** status, owner, version or slot value; 4-7 options, with the wrong options taken from the shortcuts.
- **yes/no:** "Can X do Y at t?", "Is the item available at the end (on hand minus holds minus quarantine ≥ 1)?".
  300 of these are judge rows: "Is the agent's recorded state consistent with the log?", with exactly one controlled
  error when it is not.
- **score:** bucketed counts or an escalation level, K = 4-6. Traps land on different levels where possible.
- **JB-letter:** 150 rows.

**Knobs by tier:** easy has 2-5 events, standard 6-12, and hard 13-40 with 2+ shortcuts wrong.

**Limits:** every state is at most 10,000 characters. `meta.n_events` is recorded.

**Shortcuts:**
- the last event wins;
- ignore guards;
- apply resends twice;
- display order is time order;
- ignore expiry;
- fuzzy entity id.

**Dev:** 175 iid + 175 holdout (the 2 held-out machines). **devx:** 100.

### F4 `gen3_polarity_ladder` (wave 1): 1,500 standalone yes/no, plus ladder views inside F1, F2, F3 and F6

**Quads.** Each quad is frame × switch A × switch B. This gives para (0 flips), negA or negB (1 flip) and dneg (2
flips). Gold = truth(P) XOR flipA XOR flipB.

**Frames.** 10 frame families:
- the 7 in `robust/ladder_proto.py`;
- sign_off;
- compliance_flag;
- audit_finding.

8 are used for training; 2 are **held out**. Frames that evaluate a record use the judge wording rule (§4.7).

**Base propositions P:**
- **(a) 750 rows on human hard-gold golden_train rows.** Eligibility:
  - The base row sits in an **S unit** (§11.2) whose golden unit has at most 4 rows. One quad per base group.
  - Excluded:
    - rows with a vote-share teacher or `gold_probs`;
    - roles attacked, defswap and neg;
    - `gd_gen*` sources;
    - **every base source that appears in any dev split under the ship rule's name match**: clinc150, banking77,
      std_hate, gd_ghc_hate and tb_label_nli.

  How the rows are built:
  - P = 'the right label for the text is "L"'. L is the gold label (50%) or the nearest wrong label (50%), by
    definition word overlap.
  - **The card is built by one procedure in both cases:** L plus the same near-miss bundle, in shuffled order.
  - The card says: "yes: L is the label that fits the text best among the listed labels; no: another listed label
    fits better."
  - Licence per R1.
  - The label is the human gold transformed by a program.
- **(b) 750 rows on program decisions** from F1, F2, F3 and F6 train latents. The slot `{d}` is the decision
  proposition.

**Constraints:**
- 50% of rows have depth 0. Depth is balanced against truth(P), so counting negations gives exactly 50%.
- Every cue word is at most 60% tied to answer-flipping questions (`cue_shares`).
- No 6-word run is shared with:
  - the dialogue_rebuttal templates;
  - any v11 train template;
  - the instruction of any row in the 9 ship splits.
- The banned cues of §4.7 apply.

**Dev:** 150 iid + 150 holdout (the 2 held-out frame families). The dev set uses **(b)-type propositions only** (R3).

### F5 `gen3_lead_score` (wave 1): 2,000 rows = 1,600 score + 300 yes/no + 100 JB-letter

**Rubric archetypes.** Training uses 3:
- a points table with bands, caps, negatives, recency windows, disqualifiers, thresholds and post-threshold
  overrides;
- a criteria-count ladder (BANT) that counts only the prospect's own words;
- a gated ladder.

A weighted scorecard with a tie-break rule is **held out** for dev.

**Packs.** 10 industry packs; 2 are **held out**.

**Where the rubric lives.** In the state, as a numbered and dated section. It states:
- which source wins for company size (the enrichment figure or the self-reported range);
- the title → seniority table (titles outside the table are rejected at generation);
- which budget statuses count (approved, requested, hoped, hypothetical);
- that rep notes and quoted bosses never count unless the rubric says so.

**Latent lead:**
- company size, from both sources;
- title;
- budget amount, period and status;
- target date relative to "today";
- events (type, date, attended, duplicates);
- email domain against a personal-domain list;
- customer, competitor and region flags;
- decoy secondary contacts;
- rep notes.

**Scoring.** A scorer computes the points and the level. `scorer2` recomputes both from the parsed text.

**Sampling:**
- 40% of items land within ±3 points of a threshold.
- Every item has at least 1 trap that moves the level if misapplied (2+ for hard items).
- Levels are uniform over 0..K−1, with K = 3-6.

**Views:**
- **Score (1,600).** "What qualification level does the rubric give this lead?" The options are the level texts.
- **yes/no (300):**
  - 150 ask "Is this lead sales-ready under the rubric?";
  - 150 are judge rows: "The recorded score is N, with the reason given. Is that score consistent with the rubric?"
- **JB-letter (100).**

**Shortcuts:**
- ignore the window;
- ignore the cap;
- trust rep notes;
- use the self-reported size;
- count registrations;
- score the wrong contact;
- treat monthly as annual.

**Dev:** 100 iid + 100 holdout. **devx:** 100.

### F6 `gen3_def_literal` (wave 1): 1,500 rows = 1,100 yes/no + 400 choice (100 JB-letter)

**Packs.** 10 packs:
- **customs tariff classification** (it replaces the tribunal evidence pack, R4);
- sports eligibility;
- club membership;
- insurance terms;
- school policy;
- platform content rules;
- procurement;
- tenancy;
- grant rules;
- workplace safety.

2 packs and 3 invented terms are **held out**.

**Definitions.**
- A term T is defined by 2-4 elements joined by AND or OR, plus 0-2 stated exclusions.
- For yes/no rows, the operative definition sits **in the card**. For choice rows, each element and exclusion is an
  option line (§4.4).
- 30% of items use a real word with a deliberately different definition.
- Never use "hearsay", Federal Rules of Evidence wording, or out-of-court-statement structures.

**Facts.** Each fact pattern has 1-3 outside-knowledge distractors that the definition ignores.

**Gold:** every element is met AND no stated exclusion applies.

**Twins and views:**
- **exclusion twin:** the outside rule is written into the card definition, so gold flips;
- **element twin:** one element fact flips, so gold flips;
- **equiv:** the outside rule appears as background in the facts only, so gold stays;
- **attack twin (10%, `inv`):** a counter-definition is planted in the state, so gold stays. Its template shares no
  6-word run with eval_redef plants.
- **Choice:** "Which element is not met?" (elements + "all are met").

**Dev:** 75 iid + 75 holdout. **devx:** 100.

### F7 `gen3_norm_action` (wave 2): 1,500 rows = 1,200 yes/no + 300 choice

**Norms.** About 60 norm schemas written by Claude: actor, required or forbidden act, and scope. **The scope is a
closed list stated in the norm.** Nothing comes from moral_stories. 10 schemas are held out.

**Actions.** Actions are tagged in scope or not, required act done, goal achieved (always stated) and motive. The text
is rendered from the tags.

**Conventions.** The card states the convention, written independently of any OHS card (R6):
- **C1:** the action does not breach the norm; an out-of-scope action passes; motive is irrelevant.
- **C2:** the action complies with the norm and also achieves the stated goal.

The question wording differs from `gd_gen_msn_*`, so each convention is tied to its own card.

**Twins:** a motive-flip twin (`equiv`) and an action-flip twin (gold flips).

**Dev:** 150.

### F8 `gen3_table_layouts` (wave 2): 1,000 rows = 800 yes/no + 200 choice

**Tables.** Short tables of 4-12 rows, in the 8 `tab_core` layouts plus JSON records. The fixed-width and key:value
layouts are **held out**. 20% of items have no card.

**Claims:**
- counting;
- superlative or range (**ties rejected**);
- comparison;
- difference or sum;
- "there is no";
- multi-condition lookup;
- "only" (ties rejected).

TabFact surface quirks are not copied.

**Views:** `equiv` pairs of the same table in 2 layouts, and twins that change one cell.

**Dev:** 100.

---

## 6. Dev sets (all report-only; never ship splits; never used to fit T)

**`data/yn2b_dev.jsonl` (2,150 rows) + `data/yn2b_dev_relations.jsonl`.** The part is recorded in `meta.dev_kind`:
- **iid:** training templates, a new seed stream, disjoint name pools.
- **holdout:** whole held-out packs, archetypes, machines, frame families, templates and phrasings (about 1,075 rows).

**`data/yn2b_devx.jsonl` (500 rows: F1, F2, F3, F5 and F6, 100 each).**
- **Who writes it.** Reviewer agent R writes new renderers and question wordings from the latent schema and this
  spec only. R never reads the training renderers.
- **Latents.** It uses dev_holdout latents only.
- **Labels.** Labels come from the shared `decide()`, and agent R's own parse-back agrees with them on 100% of rows.
- **Why it matters.** It is the owner's "templates not used to make the training rows" test.

**Reports:**
- accuracy per family × tier;
- the commitment rate (share of yes/no and JB-letter answers outside 0.2-0.8);
- committed accuracy (P(gold) ≥ 0.8);
- F3 accuracy by `n_events`;
- Score nMAE.

**Freezing.** Both files and their sha256 are frozen in A1 part 2 **before arm B trains and before any A/B read**.
Serving temperatures are fitted on dev-select only (FINETUNE_PLAN 5.1).

---

## 7. Decontamination (programs only; new `yn2b/check_yn2b.py`, run from the 2B worktree)

1. **12-word runs against held-out text.** Every new state, instruction and option is checked against the
   following. A hit drops the whole latent unit.
   - `held_out_grams()`:
     - OHS-1/2/3 states;
     - eval, eval_card, eval_jagged, eval_opi, **eval_redef**, eval_long, eval_multi;
     - `bench/jevbench/datasets/public`.
   - OHS-1/2/3 instructions and options.
   - Every string of `bench/jevbench_v154/datasets/public/*.jsonl`.

   **OHS-3 is held in memory only.** The program prints the hit **count** per family. Dropped rows are never printed,
   read or used to redesign anything.
2. **12-word runs against every dev and eval split:**
   - dev, devzs, devzs2, devp_card, pg_dev, debate_dev, dev_nc, taskbank_dev, hard_dev, dev_negwords, dev_claims;
   - hard12_dev, proc12_dev, planted12_dev;
   - golden_dev, breadth_dev.
3. **6-word runs on instruction and plant templates.** No template shares a 6-word run with:
   - the dialogue_rebuttal templates;
   - the v11 train templates;
   - **the instruction of every row in the 9 ship splits**;
   - OHS-1/2 instructions and cards;
   - the **injected spans** of eval_jagged, eval_opi and eval_redef (attacked text minus clean text).

   The banned words of §4.7 and the cue-share rule (≤ 60%) apply to every family.
4. **Unseen set with the new file.** `yn2b/check_unseen.py` calls
   `gate_dev.derive_unseen(SPLITS, list(gate_dev.TRAIN_FILES) + ["v14_parts/yn2b_train"])`.
   - It asserts that the unseen set equals `UNSEEN_FROZEN_ROWS` (17 sources, 3,847 rows) and that
     `overlap.flagged == {}`.
   - The `gd_gen3_*` keys match no dev source.
   - It never writes `ship_unseen_sources.json`.
5. **Exact dedupe** on normalised state + instruction, against golden_train and within yn2b. F4(a) rows share a state
   with their base row by design.
6. **Dev against train inside yn2b.**
   - Holdout and devx states share at most 20% of their 12-grams with any train state.
   - No iid dev state equals a train state.
7. **Names.** No pool name is a substring of any JevBench public string or of OHS-1/2 text. OHS-3 is checked by hash
   comparison only.
8. **Disclosure.**
   - The families were designed from OHS-1/2 error analyses, dev diagnostics (both halves) and the JevBench v1.5
     method text.
   - No item text was copied.
   - OHS-1/2 and JevBench public gains are not claimed as held-out evidence.

---

## 8. Label verification

**1. Two independent programs.** `decide` works on the latent facts. `decide2` works on the parse-back of the
rendered text and is written by **another agent that has not read `decide`**:

| decide2 for | Written by |
|---|---|
| F1 | E |
| F2 | C |
| F3 | B |
| F4 | C |
| F5 | D |
| F6 | A |
| F7 / F8 | the agent that did not write that family |
| devx renderers | R |

- They must agree on 100% of kept rows.
- If they disagree on more than 1% of generated items, stop and fix the generator. Never just filter.

**2. Grounding.** Every decisive fact in the trace appears verbatim in the rendered text.

**3. Structure checks:**
- contrast twins flip gold under both programs;
- equiv views keep gold;
- complement views invert it;
- attack twins keep it;
- every complement pair is a yes/no pair with golds that sum to 1;
- items with two independent sufficient reasons are rejected, except the declared 2-violation F2 items, which get no
  twins.

**4. Artefact probes. Every one must pass on each family.**
- A TF-IDF 1-2-gram logistic regression trained on train rows scores ≤ 60% on the family's dev from state + question,
  and ≤ 55% from the question alone.
- A **key-set / section-set probe** scores ≤ 55%.
- |corr(gold, x)| < 0.05 for x = length, format, position, tier, polarity, card presence and card style.
- No shortcut scores above 60%.
- Balance holds per template, renderer and pack (§4.6).

**5. Review. It verifies only; labels stay program-made.**
- (a) The builder reads 30 random rows and 5 full twin sets per family.
- (b) A fresh reviewer agent R2, with no generator code and no gold, **blind-solves 100 rows per family**, plus 50
  devx rows.
  - Every disagreement is traced.
  - A generator bug means fix → regenerate → re-run every gate.
  - **Pass:** 0 open generator bugs, and ≥ 97% agreement after tracing.
- (c) An ambiguity hunt on 30 hard items per family. Any reading under which the gold is wrong means a template fix.
- (d) Optional: the owner spot-checks 40 rows.

**6. Existing generators (before D1).** Run the FINETUNE_PLAN §3.4 audit on 30 teacher-vs-gold disagreements for
each of gd_gen_numeric_dates, gd_gen_evidence_conflict and gd_gen_tables.
- 15 or more wrong out of 30 triggers the §3.4 action rule.
- Arm C runs only if each generator has ≥ 27/30 labels correct.

**Outputs.** Results go to `logs/yn2b_checks.json`. `yn2b_summary.json` holds the counts, shares and sha256 of every
output.

---

## 9. How the rows enter the 2B

**Code.** All new files:
- `golden_src/gen3/` (mv_core, gen3_\*, v3_\*);
- in `yn2b/`: `assemble_yn2b.py`, `merge_yn2b.py`, `build_ab_yn2b.py`, `check_yn2b.py`, `check_unseen.py`,
  `ab_readout.py`, `teacher_gate_2b.py`.

**Assembly (`assemble_yn2b.py`).**
- It reuses `build_v13_breadth.card` and the `cid` helper, and applies §4.4-4.5.
- It asserts the choice-card rule and the no-marker rule.
- It writes:
  - `data/v14_parts/yn2b_train.jsonl`;
  - `data/v14_parts/yn2b_relations.jsonl`;
  - `data/yn2b_dev.jsonl` and `data/yn2b_dev_relations.jsonl`;
  - `data/yn2b_devx.jsonl`.

**Merge (`merge_yn2b.py`).** It runs after the unchanged `build_2b_kd.py`, and after `teacher_gate_2b.py` if D1 is
adopted.
- **It writes new files:**
  - `data/v14_parts/train_2b_golden_kd_yn2b.jsonl`;
  - `data/v14_parts/golden_relations_yn2b.jsonl`.
- **It asserts:**
  - no id collisions;
  - `train_decoder.check_rows(rows, kd=0.5)` passes;
  - no yn2b row has `meta.teacher`;
  - every relation's ends exist, with valid golds per type;
  - the kd count equals the input file's (449,957, or teacher_gate's print).
- Families dropped by the A/B are left out.
- It never overwrites an input.

**Targets.**
- Every yn2b row: gold smoothed to 0.95 / 0.05.
- `kd_skip_src ["blend50"]`, `kd_full_src ["gd_gen2_probability"]` and `expect_kd_full` 238 are unchanged.
- **Weights:** uniform, one pass, no up-weighting (FINETUNE_PLAN §7).

**Config (2B worktree only, after A1 part 3 is committed):**
```
runs/q35_2b_main.json:
  "train_file": "v14_parts/train_2b_golden_kd_yn2b.jsonl",
  "rel_file":   "v14_parts/golden_relations_yn2b.jsonl",
  "epochs":     from replay_steps.py --config runs/q35_2b_main.json (about 31.8K steps),
  "expect_kd_targets": 449957 (or teacher_gate's print)
```

**V14_KEEP.** One commit in the 2B worktree, before arm A, adds:
- `yn2b_ab_A.jsonl`, `yn2b_ab_A_rel.jsonl`;
- `yn2b_ab_B.jsonl`, `yn2b_ab_B_rel.jsonl`;
- `yn2b_ab_C.jsonl`;
- `train_2b_golden_kd_yn2b.jsonl`, `golden_relations_yn2b.jsonl`.

The 4B relays keep launching from the `final-frozen` checkout, which never uploads these.

**Other steps:**
- `yn2b_dev` and `yn2b_devx` are small top-level files and upload automatically.
- On the L4, copy the needed files to `~/lean/data/`.

**Compute.** About +4.2% steps (+1.3K), about +$3 on the H100.

---

## 10. Owner decisions

- **D1: teacher gate on exact-label generator rows (Option B).**
  - **Default:** OFF, the tested setting.
  - **Recommendation:** run arm C (+about $13, or about +16 L4-hours) **if** both of these hold:
    - the §8.6 audit clears the three generators;
    - the money allows it (§13.2).

    Arm C is the largest lever we have on 2B yes/no commitment: on these rows, targets inside 0.2-0.8 fall from
    35.8% to 13.7%. It is adopted only under the arm-C rule (§11.6).
- **D2: PRISM-X I override for the 2B.** Required whatever happens to yn2b. Text: A2 (§12).
- **D3: the 2B teacher (CHANGED by the owner on 30 Sep, 20:50 UTC; `DECISIONS_owner_30sep.md` overrides this
  section).**
  - The draft recommended fixing the teacher at 4B-E. The owner decided instead: the teacher is the best 4B, decided
    BEFORE arm A trains.
  - A new 4B becomes the teacher only if it ships under the ship rule and passes PREREG §6 (a)-(e); for the top-up C4
    that is draft amendment A8′, sections H and I. Otherwise the 4B-E labels are used.
  - Every arm (A, B, C) and the 2B main run use the same teacher, so the A/B stays valid; arm A waits for this
    decision. A relabel (about $16-23 on Modal) needs its own owner GO.
- **D4: accept the delay of about 3 days.**
  - The plan of record could start the 2B about 1-2 Oct.
  - With yn2b it starts about 4 Oct.
  - If the owner wants the 2B sooner, the fallback is to drop yn2b. Adding it later as a continued fine-tune would
    need its own candidate amendment and replay rows (A18 forgetting).
- **GO** for:
  - the 2B smoke;
  - arm A;
  - arm B (and C);
  - the reads;
  - the 2B main run.

---

## 11. The A/B test (pre-registered in A1 part 1, before arm A trains)

### 11.1 Question
Do the new rows teach skills that generalise, without harming anything we can measure, when added to the 2B recipe?

### 11.2 Data

**S (control subsample).**
- `build_ab_yn2b.py` runs `train_decoder.make_units` on `train_2b_golden_kd.jsonl` + golden_relations. That keeps
  `inv` merges intact.
- It keeps the merged units with `int(sha256("yn2b-ab:" + min(call_ids of the unit)), 16) % 8 == 0`. That is about
  12.5%, about 62.7K rows.
- Relations are filtered to rows present.

**yn2b half.** Latent units with `int(sha256("yn2b-ab-half:" + latent_id), 16) % 2 == 0`.
- About 10.6K rows.
- The builder asserts that each family is within ±5% of half.
- F4(a) rows come only from S units (§5 F4).

**Prints.** The builder prints each arm file's rows, units, kd targets and kd_full count. These values go into the
arm configs.

### 11.3 Arms (identical recipe to `runs/q35_2b_main.json`, only `train_file`, `rel_file`, `epochs` and the `expect_*` counts differ)

| Arm (pred name) | Train file | Rows | Steps (one pass, from replay) |
|---|---|---|---|
| A: control (`q35_2b_yn2bA`) | S | about 62.7K | about 3.8K |
| B: yn2b (`q35_2b_yn2bB`) | S + the yn2b half (wave 1 + any green wave 2) | about 73.3K | about 4.45K |
| C: optional, D1 (`q35_2b_yn2bC`) | B with teacher_gate applied to S | about 73.3K | about 4.45K |

**How the arms are run.**
- **One full pass per arm.** Every arm sees every S row exactly once. `epochs` comes from
  `replay_steps.py --config` per arm, and the arms differ only by the added rows.
- **The dose is a stress test.** The new rows are 14.5% of arm B's file vs 4.1% in production, about 3.6×. A pass
  implies safety at 1×; a fail may be the dose.
- **One GPU type** (H100, one arm per Modal account), from one code commit.
- **Arm A trains first** (day 1), because it does not need yn2b.
- **An infrastructure crash resumes from the checkpoint.** It is never re-run with another seed.

### 11.4 Reads

- **One job.** All arms are read in one job on the L4. If the L4 is in stockout, all arms are read on Modal in one
  job; the GPU type is never mixed.
- **Model loading.** `od_gcp.py predict`, pinned 2B base revision, layout from `train_meta`, PRISM-X loaded from the
  adapter.
- **Splits read:**
  - the 9 gate splits;
  - the 9 `_perm` reads (`--perm-seed 1`);
  - eval_jagged, eval_opi, eval_redef;
  - yn2b_dev, yn2b_devx.
- **Readout.** `yn2b/ab_readout.py` imports gate_dev's `load_rows`, `group_boot` (group_id units, 10,000 resamples,
  seed 0), the tb_mixtral-free full set, `crossfit` Brier, `relation_flips`, `perm_flips` and `asr_compare`.
  - yn2b dev sets bootstrap over `latent_id`.
  - It writes `logs/yn2b_ab.json` and one line in `logs/yn2b_ab_looks.jsonl`.
  - It is **not** a ship look.

### 11.5 Pass rule for B (B minus A; all must hold)

**Why these thresholds.** The draft's rule rejected a same-recipe rerun. The table below is measured today on
existing preds:
- **Pair:** 2B arm E_L4 minus arm E. The recipe is the same; the GPU and the micro-batching differ. This is the
  closest thing to a re-run we have.
- **Method:** paired group bootstrap over the 9 splits.
- **What the SD covers:** row sampling only. Training noise comes on top; the observed point differences were 0.1-1.75
  bootstrap SDs.

| Set (rows) | E_L4 − E point | 95% CI | Bootstrap SD | Draft rule | New rule |
|---|---|---|---|---|---|
| Full, no tb_mixtral (7,056) | −0.30 | [−1.23, +0.68] | 0.49 | ≥ −0.3 **and LB > −1.0 (fails)** | point ≥ −1.0 |
| Yes/no (3,867) | −0.59 | [−2.12, +0.99] | 0.78 | ≥ −0.5 (fails) | point ≥ −1.5 |
| Choice (3,189) | +0.06 | [−1.07, +1.12] | 0.56 | ≥ −1.0 | point ≥ −1.0 (the ship rule's (c) margin) |
| Unseen primary (3,847) | −1.14 | [−2.38, +0.13] | 0.65 | ≥ −0.5 (fails) | point ≥ −1.5 |
| dev_negwords + pg_dev + hard_dev (2,057) | −0.24 | [−2.06, +1.50] | 0.89 | ≥ +0.5 (coin flip) | point ≥ 0.0 |
| Human splits (600-1,728 each) | −1.45 to +1.50 | – | 0.74-1.69 | fail if any drop > 2.0 | report; drop > 3.0 flagged to the owner |

**G1: held-out learning (yn2b_dev holdout, about 1,075 rows).**
- Accuracy ≥ +5.0 pp, with LB > 0.
- Committed accuracy on yes/no + JB-letter rows ≥ +5.0 pp.

**G1x: template independence (yn2b_devx, 500 rows).**
- Accuracy ≥ +3.0 pp, with LB > 0.
- The gain on devx ≥ 0.5 × the gain on dev_iid. A smaller ratio means the families mostly learned templates.

**Family drop.** A wave-1 family whose pooled (holdout + devx) point difference is < 0 is **dropped** from the final
add. That only moves the file towards A, so no re-run is needed.

**G2: external, no loss.** Pooled dev_negwords + pg_dev + hard_dev: point ≥ 0.0. The gain is reported; this A/B cannot
resolve under about 2 pp here.

**No regression.** All on the tb_mixtral-free full set, as in the ship rule:

| | Constraint | Must hold |
|---|---|---|
| NR1 | Full set | point ≥ −1.0 pp |
| NR2 | Choice | point ≥ −1.0 pp |
| | Yes/no | point ≥ −1.5 pp |
| NR3 | Unseen primary | point ≥ −1.5 pp |
| NR4 | Calibrated yes/no Brier (d) | ≤ +0.005 |
| | Equivalence flips (e) | ≤ +2 pp |
| | Permutation flips (f) | ≤ +2 pp |
| NR5 | Jagged / OPI | fail only if B's ASR > the 2B cap (6.9% / 5.4%) **and** the bootstrap LB of (B − A) > 0 |
| | eval_redef accuracy | fail if the point drop > 4.0 pp |
| NR6 | dev, devzs, dev_nc, devp_card, dev_claims | report; a drop > 3.0 pp is flagged to the owner, not an automatic fail |

**How often this rule is wrong.**
- **Harmless add:** each of NR1-NR3 fails about 5-10% of the time, about 20-25% for all of them together.
- **Harmful add:** a true −1.5 pp full-set harm fails NR1 about 75-80% of the time.
- **Below 1 pp:** the rule does not certify effects that small. The final ship rule against v11r stays decisive.

**Verdict.**
- **PASS** (G1, G1x, G2 and NR1-NR5 all hold): the 2B main run uses `train_2b_golden_kd_yn2b.jsonl`, minus dropped
  families.
- **FAIL:** the plan-of-record `train_2b_golden_kd.jsonl`, the same day.
- One A/B, one verdict.

### 11.6 Arm C rule (D1)

Adopt Option B only if all of these hold, and the owner approves:
- C passes NR1-NR5 against A;
- (C − B) full-set point ≥ 0.0;
- (C − B) committed yes/no accuracy on the 9 splits ≥ +1.0 pp;
- (C − B) Brier (d) ≤ +0.002.

### 11.7 Cost

| Item | Estimate |
|---|---|
| 2B smoke (needed anyway) | H100 about 45 min, about $3 |
| Arm A | 3.8K steps × 1.54-1.89 s = 1.6-2.0 h, about $7-9 |
| Arm B | 4.45K steps, 1.9-2.35 h, about $8-10 |
| Reads | about 3 L4-hours per arm, about $3 each |
| **A + B total** | **about $23-26** |
| Arm C | about +$13 |

These use the FINETUNE_PLAN 2B speed estimate (13-16 h per 30,457 steps). The speed is not measured on golden yet.

**Option L4.** Use it when the Modal reserve is too thin.
- All arms run on the Google L4, at about 13 s/step: arm A about 14 h, arm B about 16 h, arm C about 16 h.
- The cost is about 30-45 L4-hours of Google credit and no Modal money.
- Arm A runs D1-D2, off the critical path. Arm B moves the verdict by about half a day.
- The GPU type is never mixed between arms.

### 11.8 What the A/B cannot show

- Effects under about 1 pp.
- Gains on the unseen JevBench v1.5 items, which are inferred from G1 and G1x only.
- Whether a fail is caused by the 3.6× dose.

---

## 12. Amendment texts (appended to PREREG_FINAL.md; fill the `<…>` values)

### A1 part 1 (commit before arm A trains): the yn2b design and A/B rule

> **Amendment A1 (<date>): program-labelled yn2b rows for the final 2B, and the A/B that decides them.**
> 1. **Design.**
>    - `yn2b/SPEC.md` (sha256 `<sha>`): 8 families `gd_gen3_*`, gold-only targets, and the data, arms and pass rule of
>      its §11.
>    - golden_train is unchanged, and so is the 4B.
>    - If the A/B passes, §10.10's "frozen at 501,732 rows" no longer holds for the 2B's file.
> 2. **Teacher.** Per the owner's D3 as changed on 30 Sep (`DECISIONS_owner_30sep.md`): the 2B teacher is the best
>    4B, decided before arm A trains. PREREG §6 applies as written, all of (a)-(e) (for C4: amendment A8′, sections H
>    and I); otherwise 4B-E. Every arm and the 2B main run use the same teacher.
> 3. **Disclosure.**
>    - The families were chosen from OHS-1/OHS-2 error analyses (no text copied), dev diagnostics on both halves, and
>      the JevBench v1.5 method text.
>    - No OHS-3 or JevBench half-B information was used.
>    - dev_negwords' held-out frame family stays out of training.
> 4. **Selection bias.** The A/B uses the dev splits for one data choice. That adds a small selection bias to the later
>    ship look, which we accept and disclose.
> 5. **Unchanged:** REF (v11r), the ship rule, the caps, §8, no JevBench submission, and OHS-3 once, blind.

### A1 part 2 (commit before arm B trains and before any A/B read)

> Build numbers:
> - counts per family `<table>`;
> - `MANIFEST_yn2b.jsonl` sha `<sha>`;
> - sha256 of yn2b_dev `<sha>` and yn2b_devx `<sha>`.
>
> Gate results:
> - decontamination: `<hits dropped per family; OHS-3 counts only>`;
> - `check_unseen`: 17 sources, 3,847 rows, 0 flags;
> - label checks: `<decide/decide2 100%, blind solve ≥ 97%>`.

### A1 part 3 (commit before 2B step 0)

> - **A/B result:** `<G1, G1x, G2, NR1-NR6>` → `<PASS/FAIL>`. Dropped families: `<list>`.
> - **Final 2B file:** `<name, rows, sha>`.
> - **Schedule:** replayed steps `<S>`; C2 snapshots `<s085, s090, s095>`.
> - **D1:** `<not adopted | adopted, owner approval <date>>`.
> - **label_smooth:** `<as config | 0.05>` (see §1.8).

### A2 (commit before arm A trains)

> **Amendment A2 (<date>): PRISM-X arm I adopted for the final 2B (owner override for security).**
> - The pre-registered accuracy margin for I vs E_L4 failed (−0.27 pp [−1.34, +0.79]).
> - The owner adopts arm I because layout E at 1,600 steps would be vetoed on jagged ASR (10.0% vs a cap of 6.9%,
>   +6.1 pp [+2.8, +9.6]). I_1600 has 1.1%.
> - The ship rule, REF and caps are unchanged. Latency is reported with PRISM-X on.
> - 2B base revision for scoring: `<hash>`.

### Addendum to FINETUNE_PLAN.md

> - §3.3 now ends with `merge_yn2b.py`.
> - §3.5: `train_file`, `rel_file` and `epochs` as in SPEC §9.
> - §6: +$23-26 for the A/B (+$13 with C), and about +$3 for the 2B pass.
> - §7's "20K-row A/B pilot: not resolvable" is superseded for this decision only. The A/B here is a one-pass,
>   stress-dose, 2-arm test with non-inferiority margins taken from measured 2B spread and a held-out and
>   template-independent generalisation bar. It resolves harm of about 1.5 pp or more and in-family generalisation,
>   not effects under 1 pp.
> - Up-weighting, curricula and teacher sharpening stay rejected.

---

## 13. Build plan, timeline, and where each piece is used

### 13.1 Who

- **5 builder agents (A-E):**
  - A: mv_core, F4, F6's decide2;
  - B: F2 atoms, renderers and views; F3's decide2;
  - C: F3 machines and simulator; F2's and F4's decide2;
  - D: F1 engine, F1a and F1b; F5's decide2; then F6;
  - E: F5; F1's decide2; all tooling (assemble, merge, build_ab, check_yn2b, check_unseen, ab_readout,
    teacher_gate).
- **Reviewer R:** writes the devx renderers.
- **Reviewer R2:** blind solve and ambiguity hunt.

Everything is CPU work and new files only.

### 13.2 Timeline

| Day | CPU (agents) | GPU (needs GO) | Owner |
|---|---|---|---|
| **D0, 30 Sep (now)** | Create the 2B worktree. `build_ab_yn2b.py` builds arm A's file and prints its counts; `replay_steps` for arm A; §8.6 label audit; mv_core and the F1/F2/F3/F5 engines; `check_yn2b` skeleton | – | Review this spec. Decide D1-D4 |
| **D1, 1 Oct** | Family rows plus cross-agent decide2. R starts the devx renderers | **2B smoke** (heaviest units at 16384, trainable count), then **arm A** (about 2 h) | Commit A1 part 1 and A2 **before arm A**. V14_KEEP commit. GO |
| **D2, 2 Oct** | All gates (§7, §8.1-8.4). R2 blind solve and ambiguity hunt. Fixes. Wave 2 only if wave 1 is green | – | – |
| **D3, 3 Oct** | Assemble; decontamination; `check_unseen`; freeze the dev files; build arm B (and C) files; replay | **Arm B (and C)** about 2.3 h in parallel, then **reads of all arms in one job** (about 6-9 L4-hours) | Commit A1 part 2 before arm B. D1 approval if C runs |
| **D4, 4 Oct** | `ab_readout` verdict; merge the final file (or keep the plan of record); replay; heavy-unit re-check | **2B main run** (about 13-16 h, about $56-70) | Commit A1 part 3. GO |
| **D5, 5 Oct** | – | 2B main run ends; ship reads | Ship look vs v11r (PREREG §5) |

**Critical path.** Wave-1 gates (D3) → arm B → reads → verdict (D4). Arm A and the smoke are off it.
- If wave 1 is not fully green on D3, arm B runs with the families that passed, in priority order.
- If the verdict fails, the 2B main run starts on the plan-of-record file the same day.

**Money.**
- **Before yn2b.** The 30 Sep audit puts what is left at 4B about $77-85 and 2B about $57-70. That leaves a Modal
  reserve of about $36-62, and it depends on the unconfirmed October refill (7 × $28).
- **yn2b on the H100** adds about $26-39 (smoke, A, B, optional C) plus about $3 of extra 2B steps. The reserve then
  falls to **about $0-35**.
- **If the refill is not confirmed by D1**, run the arms on the Google L4 instead (§11.7 option L4). That costs about
  30-45 L4-hours of Google credit and no Modal money, and arm B then adds about half a day to the critical path.

### 13.3 What each piece is, when it is built, and where it is used

| What we do | When | Used in |
|---|---|---|
| Generators, gates, yn2b_dev, yn2b_devx | Now → D3, CPU, while the 4B trains | the arm B file, then the 2B training file |
| §8.6 label audit and teacher_gate | Now | arm C → the 2B file, if D1 is adopted |
| build_ab and arm A | D0-D1 | the control of the A/B |
| 2B smoke | D1 | fills `expect_trainable` for the arms **and** the 2B main run |
| Decontamination and `check_unseen` | D3 | A1 part 2; ship-rule integrity of the 2B |
| A/B verdict | D4 | decides whether yn2b is in the 2B main run |
| Merged file, config values, A1 part 3 | D4 | 2B main training |
| yn2b_dev and devx reports (commitment, Score nMAE) | after the 2B | the write-up and the JevBench half-A report, never T fitting |
| Ship look vs v11r | D5 | ship decision (PREREG §3-5) |
| OHS-3 once, blind | last | final claim vs Jev |

---

## 14. Optional later: the 4B variant (owner must-have #4)

This is not on the 2B's path.
- **What:** "4B_main + yn2b", a short continued fine-tune from the new 4B adapter.
  - About 2,000 steps.
  - yn2b_train plus at least 75% replay from golden_train. A18 showed forgetting at about 48% replay.
  - Gold targets only.
- **When it can be used:** only if it passes the same ship rule against 4B_main. The clean 500K 4B stays the headline.
- **Cost:** about $8-10 on the H100, plus reads.
- The teacher rule is superseded. The owner's D3 of 30 Sep (`DECISIONS_owner_30sep.md`) makes the teacher the best 4B,
  decided before arm A. The top-up C4 (`prereg_drafts/A8prime.md`) can become the teacher only if it ships and passes
  PREREG §6 (a)-(e) before any 2B A/B arm trains; the relabel needs its own owner GO.

---

## 15. Risks and limits

- **Gains may stay in-family (A18, G2).**
  - Guarded by G1 (held-out families) and G1x (independent renderers), and by the "no loss" G2.
  - The realistic dev-gate effect for the full 2B is about 0 to +1.0 pp.
  - The main payoff is confident yes/no, guardrail, state and Score answers on JevBench v1.5, and fewer
    self-contradictions.
- **Security.** Guarded by the authority rule, balanced-direction plants, marker-spoof twins, definitions in the
  card, the eval-template bans, and NR5.
  - Jagged ASR is noisy run to run, so the final ship veto stays the real test.
- **No plan-of-record 2B if yn2b ships and the 2B then fails the ship rule.**
  - The fallback is v11r or I_1600 (PREREG §5). A second 2B main run (about $56-70) is not in the budget.
  - The A/B is the only protection against this, and it cannot see harm under about 1.5 pp. The owner accepts this
    with D4.
- **Label bugs.** Guarded by the two-program rule, parse-back, grounding, the blind solve and the ambiguity hunt.
- **Leakage.** Guarded by the 12-gram and 6-gram checks, the banned words, `check_unseen` and the F4(a) source
  exclusion.
- **Time.** The build may run past D3. Families enter only in priority order, and only when green.
- **Unmeasurable locally.** The v1.5 guardrail, lead and state items. The 2B pilot's abstain rates come from a
  1,600-step model.

**Scratch evidence.** The noise table in §11.5 was computed with
`/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/ab_noise.py`
(read-only on `preds_*`).
