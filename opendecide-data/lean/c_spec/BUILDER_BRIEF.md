# BUILDER BRIEF (verbatim extracts; generated 6 Oct 2026 01:15 UTC by the orchestrator)

Exact text copied from c_spec/C_DATA_SPEC.md v4 (sections 2.1, 2.2, 2.4, 6, 8, 10) and PREREG_FINAL.md (A15, A16, A16.1, A16.2, A19, A20, A21).

It is binding exactly like the sources and replaces reading them in full. Open a source section only when the brief points to text it does not contain.



## PREREG amendments (verbatim)

> **Amendment A15 (3 Oct 2026, 20:45 UTC; before any C data, generator, pack, style, public row or commit row exists, and
> before any model has read the suite): the sealed new-domains dev suite is FROZEN (G14).**
> - **Files** (git-ignored, under `lean/sealed_nd/`; never opened by C builders):
>   - suite `suite_v2.jsonl`, sha256 `f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68`;
>   - scorer `score_nd.py`, sha256 `953a3363c6b8d103d32a4c34bdda735c2a34bb5278cbffd27f292ec41841cfd7`. It verifies the
>     suite sha before every look and prints aggregates only, including the B3 yes-share block. It logs every look in
>     `looks.jsonl` and refuses any look not in recipe 6.2: S1, S2, C once, and J (Jev) once, only after a C look with a
>     recorded ship verdict.
> - **Counts.** 7,302 items in total; 2,988 select and 4,314 confirm (sha256("ndsel:" + group_id) mod 5).
>   - **Part A (headline):** 6,205 items in 8 domains, split 2,542 select / 3,663 confirm.
>     - Non-adjacent: D1, D10, D11, D12, holding 3,446 items (55.5%).
>     - Adjacent: D2, D3, D4, D5, holding 2,759 items.
>     - The largest domain is 16.1%.
>   - **Other parts:** P 600 (3 x 200); B1 298 (2 within-B1 near-duplicate groups dropped from 300); B2 199 (1
>     decontamination drop from 200; 4,148-7,718 tokens).
>   - **Item balance:** yes/no 46.5% of items, gold yes 50.0%; 58.2% card-free; 2-8 options.
> - **Adjacency labels** were fixed at pick time, before any model read, and never change. The non-adjacent ids are
>   listed above.
> - **Build history (disclosed):**
>   - v1 (9 domains, only 1 non-adjacent) failed the >= 4 non-adjacent / >= 50% rule. It was never read by a model.
>     No waiver was used: 3 new non-adjacent domains were built, and whole adjacent domains were dropped from the bottom
>     of the v1 priority list.
>   - Counts-only 12-gram decontamination against C1's training file (501,732 rows) dropped 43 v1 items and 18 new
>     items, whole groups each time.
>   - Noise-floor reads were flag-only, at most 1.5% clearly wrong per domain, and no domain was dropped.
> - **Isolation incident (disclosed):** sealed item text had spilled into shared session temp folders (tool-results,
>   task outputs, scratchpad). With the owner's OK, the 31 flagged files were deleted and the sealed workflows'
>   transcripts were moved into `sealed_nd/`. A re-scan (12-gram hashes) found 0 files with >= 3 hits outside
>   `sealed_nd/`. C builders may not open session folders (spec v4 "Who may read what").
> - **Orchestrator access:** the orchestrator has seen this suite only as counts by domain id. It has never seen any
>   domain, source or theme name, or any item.
> - **Jev read:** once, at the C look, after the ship verdict is logged, through the OHS Jev harness. The OpenRouter
>   spend is an owner GO point. The result is report-only.

> **Amendment A16 (3 Oct 2026, 21:00 UTC; after A15 and before any C training row, generator run, pack, style pool,
> codebook, public row, commit row or C candidate exists): the C plan, round 1.**
> - **Plan documents** (frozen at these sha256 prefixes; any change needs a new amendment):
>   - `c_spec/C_DATA_SPEC.md` v4 `4ca129963bef3e0a`;
>   - `c_spec/C_TRAIN_RECIPE.md` v4 `f4b7915088942f9b`;
>   - `c_spec/ADDENDUM_research.md` `0da2e8341929597e`.
>   - The G0 family specs (`c_src/<family>/G0_SPEC.md`) are frozen per family, and their sha256 is logged before that
>     family's first generator run. They are still closing their last ambiguities, and a generator cannot run until
>     its G0 has 0 open label-flip ambiguities.
> - **Model and training:**
>   - Init: C1 = `q35_4b_main500k` (sha256 507d1c29...). Same LoRA (r16/a32, QWEN35 targets) and same loss weights as
>     C1, plus the A4 ordinal term `lam_ord` 1.0.
>   - Config `runs/q35_4b_c_r1.json` (`f3bb379e...`). The seed is fixed at **20261003**. `epochs`, `expect_ord_rows`
>     and the KD counts are filled mechanically from the mixer and batch dry run.
>   - Trainer `train_decoder.py` `c2c2d1d6...`, readout `decoder_io.py` `908c08d7...`. Every change is default-off, and
>     C1 reproduces bit for bit.
>   - One candidate in round 1. Budget about $30 under the owner's GO, plus a smoke run of at most $0.5.
> - **Data, round 1:** 150,000 rows.
>   - 90,000 replay rows (60%): `c_build/replay_sample.py` `4f93a215...`, which draws round 1 nested inside round 2.
>   - 60,000 new rows: own families 45,250, licensed public 8,750, commits from other repos 6,000.
>   - G9 crowd scoring runs on the free L4 only (owner, 3 Oct).
> - **Deny-list** (`c_src/common/denylist.py` `a6dec381...`, aliases `b9cc417f...`). It reads `ohs3/used_sources.json`
>   only in-process and prints verdicts only. Orchestrator rulings:
>   - (a) Bare platform words (Wikipedia, Reddit, GitHub, arXiv, Zenodo, PubMed, ...) never match on their own. Real
>     text overlap is caught by the counts-only n-gram decontamination against OHS-1/2/3, the sealed exports, Decision
>     Index test items and JevBench items, run before every freeze.
>   - (b) An entry rejected only for label quality (silver or noisy labels) is `no_new_rows`, not `taint`. This
>     applies to T-REx, so MuSiQue (human-validated) passes. Contamination, licence, forbidden-task, dev and eval
>     entries stay `taint`.
>   - (c) "locked" counts as "avoid".
>   - (d) A10 is handled by the A8′ whole-source drop of `gd_redocred` and `gd_helpsteer3_pref`.
>   - (e) Attacked replay rows with C1 p_g < 0.2 are counted as successful attacks, not dropped. Their unit is judged
>     by its clean partner.
> - **Counters:**
>   - `c_src/common/negcount.py` uses closed lexicons, which XF17 allows before the freeze.
>   - Ruling: "neither ... nor" counts as one syntactic negation (k_syn 1), so it cannot fill the double-negation quota.
> - **Addendum D2** (facility-location selection) is NOT adopted. Selection stays stratified and representative.
> - **Gate (recipe 6.2-6.4, unchanged):**
>   - Ship: the sealed part-A confirm gain over C1 is >= +1.0 pp with LB > 0, AND guards D1-D6 and D9 pass.
>   - Round 2 runs only if the select gain is >= +2.0 pp with LB > 0 and the guards pass.
>   - Looks: S1, then (S2), then C once; Jev is read once after the ship verdict.
>   - ejs-5, OHS-1/2/3, JevBench, the Decision Index and LongBench never choose anything.

> **Amendment A16.1 (4 Oct 2026, 00:10 UTC; before any generator run, C row selection or C candidate): tool versions
> that implement A16's rulings.**
> - Pinned versions:
>   - `c_src/common/denylist.py` v1.2 `e268d5667f181bba` (was `a6dec381`);
>   - `deny_aliases.json` v1.1 `40eeb47e2f379ea8` (was `b9cc417f`);
>   - `negcount.py` v1.1 `79368f465d438617` ("neither ... nor" k_syn 1);
>   - `c_build/replay_sample.py` `5735ca3eb673895d` (was `4f93a215`).
> - What changed:
>   - A16 (b) is applied as 17 sub-entries moved to `no_new_rows` / `label_quality`, including T-REx. Mixed or
>     text-based reasons stay `taint`.
>   - The replay writer refuses pending or stale verdicts and requires the A15 suite sha.
> - The round-1 replay draw was written with these versions (20:50 UTC, 3 Oct): 99,069 rows in 20 shards, plus a
>   2,000-row old slice. Its manifest sha256s are `3f96d3ed...` and `9118d6b5...`.
> - Two more rulings:
>   - (f) The X15 2-of-3-annotator filter applies to every EDOS row: F10/F11 S7 and public 3E.
>   - (g) On choice rows, everything a row needs goes in `instructions`, `state` or `- option: definition` card lines.
>     The `schema_branch_mark` layout shows only option-definition lines from the card on choice rows. Every family
>     must pass `loader_check` on every row. Token caps count `instructions` twice, because the layout repeats them.

> **Amendment A16.2 (4 Oct 2026, 02:30 UTC; before any C candidate exists): the round-1 launcher is pinned, and the plan
> files are committed.**
> - Pinned: `modal_od.py` `c25e4f38781242f0`. It uploads only `c_parts/c_train_r1.jsonl` and `c_rel_r1.jsonl` (plus the
>   r2 pair). It never uploads `*_shards` or `ohs3` paths, and its `_launch_checks` refuse `FILL` values and missing
>   data files.
> - Unchanged pins: trainer `c2c2d1d6...`, readout `908c08d7...`, config `f3bb379e...`, spec v4 `4ca12996...`, recipe
>   v4 `f4b79150...`.
> - Committed alongside this amendment: the plan, tools and tests. Not committed: REVIEW_* and LICENCE_CHECK_*, which
>   name sealed-suite candidates.
> - F2 prompt identity passes on od-l4b and on the Mac (same 6 view hashes). The Modal record is added at the smoke
>   run.
> - **Owner-facing correction:** recipe v4's own projection, not the earlier chat estimate, is the registered
>   expectation for OHS-3:
>   - median -0.8 vs Jev;
>   - P(>= Jev - 1) 56%, P(>= Jev) 31%, P(>= Jev + 1) 14%;
>   - C ships in about 22% of simulated runs.

> **Amendment A19 (5 Oct 2026, 22:45 UTC; orchestrator ruling; written before the shared tool exists or is run on any
> family): G8 (AFLite-lite) is judged against a label-shuffled null, not a fixed 10% bar.**
> - **Why:** under the spec 8 set-up (frozen MiniLM-L6, 64 partitions, linear models, tau 0.75, grouped by card), the
>   fixed "< 10% predictable" bar fails on shuffled labels.
>   - Label-permuted controls already run by the families score 13.8-27% (F4 13.8%; F5 19.3-26.7%; F1 yes/no null
>     18.7-21.9%), so the bar cannot be met even by data with no cue.
>   - Linear models trained on overlapping partitions make correlated guesses, so chance alone yields "predictable" rows.
> - **New rule (G8v2), per family and per part (yes/no; choice):**
>   1. The features, partitions, models, tau and grouping by card are unchanged.
>   2. K = 20 seeded label permutations within card form the null, plus K = 20 global permutations.
>   3. Pass needs both of these:
>      - the real grouped predictable share is at most the smaller of the two nulls' 95th percentiles;
>      - pooled grouped held-out accuracy is at most chance + 2 pp (the G6 rule; chance = the majority or 1/k rate).
>   4. A fail keeps the spec 8 action: find the cue and fix the generator. No bulk deletes.
>   5. The old raw share stays in every report.
> - **Power check before use:** cues planted on real family rows must FAIL G8v2 and shuffled labels must PASS it.
>   - The cue is a token added to the gold-side rows at several strengths.
>   - The planted-cue result is recorded with the tool. If the tool cannot catch a moderate planted cue, this
>     amendment is void and G8 stays as written.
> - **Scope:** one shared tool, `c_src/common/g8_aflite.py`, used by every family. Report-only files go to
>   `c_build/g8v2/` until a family's QC re-run adopts them. No other gate changes.

> **Amendment A20 (6 Oct 2026, 00:05 UTC; owner asked for maximum speed with no loss of quality; orchestrator
> ruling): speed-ups that change no data, no gate and no training math.**
> - **Diagnosis:** agent transcripts show 65-90% of every repair round's wall time is waiting on Python jobs.
>   - The Mac runs at load 50-120 on 10 cores, with 5.7 GB of swap and 10 GB of free disk.
>   - Model thinking time is the minor part.
> - **(a) Cloud CPU for heavy jobs:**
>   - `c_build/rrun.py` runs a family's generator, solver-B or QC command unchanged in a Modal CPU container, then copies
>     the outputs back.
>   - It runs on a profile with unused monthly credit. Spend is logged in `logs/budget_ledger.md`, and it stops
>     itself at $15 in total.
>   - **Adoption test before use:** a deterministic gate script must give identical JSON locally and remotely. A
>     seeded learner gate must give the same pass/fail with shares inside its seed spread.
>   - From adoption on, every gate re-run of a family uses one platform consistently.
> - **(b) Family lanes without batch barriers:** at most 5 family pipelines at once, each running
>   gen → G2 → check → repair rounds.
>   - The prompts, gates, G0 specs and the never-open lists are the same as the lean build and `c-repair-rounds`.
>   - Each family has one owner lane, recorded in a `LANE_LOCK.md` note. Any other lane that meets the note stops
>     without changing anything.
> - **(c) Training on several H100s (DDP)** with the same global batch (16), steps, learning-rate schedule, seed and
>   losses. Losses are normalised over the global batch, not per rank.
>   - **Adoption test 1:** a CPU gloo test with 1 vs 2 ranks on a tiny model gives gradients equal within 1e-5
>     relative (fp32).
>   - **Adoption test 2:** a ≤ $4 GPU parity run of 50 steps, 1×H100 vs 4×H100, on rows from C1's old training data.
>     The per-step loss must match within bf16 noise.
>   - If either test fails, round 1 trains on 1×H100 as planned.
> - **(d) Overlap:**
>   - **Crowd:** the crowd read (A17, ~$15) runs per family as each family passes every gate, on parallel containers.
>     Same models and same single view.
>   - **Pre-smoke:** a pipeline-only pre-smoke on the partial mix runs now (≤ $1). Its outputs decide nothing.
>   - **Contamination:** the counts-only decontamination check runs per family as each passes.
>   - **Final tests:** they run once each, as planned, but at the same time on separate containers.

> **Amendment A21 (6 Oct 2026, 00:55 UTC; owner asked again for more speed with no compromise; orchestrator
> ruling): remove the remaining waits. No data, gate or training-math change.**
> - **(a) All families at once:** after the 02:00 UTC usage-window reset, the A20 family lanes run every remaining
>   family at once (F2, F7-F13, COMMIT), with no queue. Lanes poll about every 75 s, not every 30 s, to save usage.
> - **(b) The end runs itself.** An autopilot chains these steps with no idle gaps, each starting the moment its input
>   is ready:
>   1. per-family crowd read (A17) and decontamination, then `mixer.py --final`;
>   2. round-1 training on 8×H100 if the A20 (c) parity test passes, else 4×H100 if it passed for 4, else 1×H100;
>   3. the 6.3 gate;
>   4. the final tests in parallel.
> - **Round-1 training** is pre-authorised by the owner (~$30). The autopilot stops at the projected-cost hard stop and
>   at any refused check.
> - **(c) The real run's first 100 steps are the smoke.** They abort automatically on any of: NaN or inf loss, a loss
>   above 3x C1's start loss, a failed `check_rows`, or a throughput below half the parity run.
>   - This replaces the separate smoke run. The pipeline pre-smoke on the partial mix (A20 d) still runs before it.
> - **(d) C1's reads are pre-computed now:**
>   - which sets: the sealed suite (A15), the dev splits and the final-test sets other than OHS-3;
>   - storage: kept sealed in `c_build/preread/` with sha256 only; no score is computed or looked at before the gate
>     or the final report;
>   - OHS-3 is not touched before the end.



## C_DATA_SPEC v4 extracts (verbatim)

### 2.1 Rules that apply to every family

**Definitions.**
- A **task card** is one unique (family, sampler, domain pack, label schema, instruction family). Two cards must
  differ in the domain pack and in the label schema or rule set.
- A **domain pack** is a Claude-written bundle: setting, roles, entity name pools, invented jargon, document types,
  units, number ranges. Target: a shared pool of >= 300 packs (round 1 >= 200). Every family uses >= 40 packs (round 1
  >= 30). The QC program drops any pack that hits the sealed keyword block-list (section 9). Builders never read that
  list; the program applies it.
- **(v4, F4) Persona seeds.** When Claude writes a pack or a scenario, the "who is deciding" role is seeded from an
  O*NET occupation title (CC BY 4.0; `gd_onet_occupation`, KEEP in `LICENCE_REGISTER.md` section 4). Titles only, drawn
  by program (fixed seed, spread over O*NET major groups); the pack records `persona_seed` (O*NET code) and declares
  O*NET as a parent (3.H). Credit O*NET in the notices file. **PersonaHub (CC-BY-NC-SA-4.0) is never used** (3.G).
  O*NET's rejected.json entry (large_labelsets: alternate titles / SOC direct-match file, overlap) is class
  `no_new_rows`. Persona seeds are titles inside Claude-written packs, not rows from O*NET, so a `no_new_rows` hit on
  this persona-seed parent passes. Seeds come from the main occupation titles, never the alternate-titles or SOC
  direct-match file.
  Packs still pass the sealed keyword block-list and decontamination (7.2).
- A **sampler** is the code that draws the hidden structure (rules, facts, events, tables). Each family has
  **>= 4 training samplers (S1-S4, plus S6 and up when a family needs more) and 1 held-out sampler (S5)**. Each training sampler gives at most 2,500 rows over
  both rounds, so F1 (10,800 rows) needs 5. The samplers must differ in shape (for example forward vs label-first vs
  table-first vs narrative). S5 feeds only the mix-tuning dev. Reason: a model trained on one logic sampler scored 99.9%
  in distribution and 57.3% on a second sampler of the same problems (Zhang et al. 2022, arXiv 2205.11502); a
  competitor's generator gave +26 pp from its first 6K rows, then +5.

**Pipeline for every own row.**
1. Sample a structure with a training sampler (fixed seed).
2. Solver A (the generator's own logic) computes the label.
3. Render to text: template + domain pack + format style + instruction wording + definition style.
4. Parse the rendered text back with an independent parser written from the family spec, not from the renderer.
5. Solver B, of a different paradigm, re-solves the parsed structure. It must agree with solver A on 100% of rows.
6. Emit twins (fact-flip, negation, premise removal, attack) and their relations.
7. Record provenance (section 2.4).

**Expert level means:** professional documents (policies, SOPs, case files, audit logs, schedules, multi-table
reports, change logs), 2-6 interacting conditions, exceptions and precedence, values at the exact boundary, implicit
cues ("fail to", "lack", "no fewer than"), and functional distractors (each wrong option comes from one specific,
plausible error). It does not mean outside knowledge. Every question must be decidable from the card and the text
alone. Facts are about invented entities, so memory cannot answer (FLD design rule 1, arXiv 2411.12498).

**Per-family quotas (all own families).**

| Quota | Value |
|---|---|
| Max share of own rows per family | 12% |
| Cards per family | round 1 >= 80, round 2 >= 150 (F12: 40 / 80; F13: 40 / 70) |
| Rows per card | max 128; median about 40-50 |
| Instruction wordings | pool >= 30 per family; each card uses >= 5 |
| Definition styles | >= 3 per family: one-line, one-line + 1-2 examples (about 50% of cards), rubric or decision list; plus a short or no card on about 15% of rows |
| Yes/no vs choice | 45-55% yes/no where the family allows both |
| Yes rate | Per card: drawn uniformly from 20-80% (cards differ). Aggregate: 50% +/- 2 within each family x wording x difficulty bin x negation count |
| "Yes = bad outcome" polarity | 50% +/- 5 of yes/no rows |
| Syntactic negation in yes/no questions | >= 10% of each family's yes/no rows (today 6.6% overall) |
| Double negation with affirmative twin | >= 2% of each family's yes/no rows (overall new-row target 2-5%) |
| Minimal-pair (label-flip) twins | 20-25% of own rows sit in a twin set |
| Attack twins (instruction injection, label unchanged) | about 5% of own rows, `inv` relation; wording never matches eval_opi or eval_jagged (section 7) |
| Few-shot cards (1-3 worked examples in the card) | 5-10% of cards |
| Inverted cards ("which of these cases meets rule X?") | 10-15% of cards |
| Masked label names (neutral IDs) | 10-15% of choice rows (F10: 40%) |
| Swapped label names (familiar word, different definition) | about 5% of choice rows (F10: 30%) |
| Option counts (choice rows) | 2-4: 35%; 5-9: 35%; 10-19: 15%; 20-60: 15% |
| Gold letter position | uniform per option-count bucket (the trainer shuffles again at train time) |
| Abstain options | when "not enough information" or "none of these" is shown, it is the wrong answer on >= 50% of those rows |
| Deep items (beyond the family's default depth cap) | <= 10% of the family's rows; they form the depth sweep (section 10) |
| Difficulty (set by the scoring crowd, below) | easy <= 25%, medium >= 45%, hard <= 30% |
| Label-check form (`Is the correct answer "X"?`) | 0 new rows |

**Relation units and batching (code fact: `train_decoder.make_units` groups rows by `call_id`).**
- All rows joined by a `complement`, `equiv` or `inv` relation share one `call_id`.
- A relation unit holds **at most 3 rows**. The trainer may add permutation twins on top.
- Contrast twins with no relation term (label-flip pairs, deleted-premise twins) get their own `call_id`.
- Units with any row of 2,000 tokens or more hold at most 2 rows.

**Difficulty and selection.**
- p_g = probability on the gold answer. The scoring crowd is REF = C1 (step B adopted nothing), 4B-E and the base
  Qwen3.5-4B, each read with the shipped A5 readout on the free L4 (decision 3). Crowd p_g = the mean of the three.
  No model above 4B is used.
- Bins: easy if crowd p_g > 0.97; medium if 0.30 < p_g <= 0.97; hard if p_g <= 0.30.
- Generate about 1.5x the target rows. Keep all medium and hard rows and 30% of easy rows. Then downsample **inside
  each family x gold label x wording x difficulty-bin cell**, so yes = no and gold letters stay uniform in every bin.
  C1 leans "yes", so gold-"no" rows are harder; selecting without strata would break the balance.
- A family with more than 30% hard rows after the G5 re-read has its depth cap lowered.


### 2.2 The 13 families

Rows: round 1 / round 2. Cards: round 1 / round 2 minimum.

| Family | Share | Rows (r1 / r2) | Cards (r1 / r2) |
|---|---|---|---|
| F1 Policy composition and precedence | 12% | 5,400 / 10,800 | 80 / 150 |
| F2 Rule arithmetic, money, quantities, dates | 7% | 3,150 / 6,300 | 80 / 150 |
| F3 State tracking and record chains | 10% | 4,500 / 9,000 | 80 / 150 |
| F4 Indirect evidence and multi-hop yes/no | 8% | 3,600 / 7,200 | 80 / 150 |
| F5 Hard and negated yes/no | 8% | 3,600 / 7,200 (r2 size set by the probe) | 80 / 150 |
| F6 Not enough information, abstain as gold | 8% | 3,600 / 7,200 | 80 / 150 |
| F7 Ordinal rubrics | 7% | 3,150 / 6,300 | 80 / 150 |
| F8 Risk and probability | 5% | 2,250 / 4,500 | 80 / 150 |
| F9 Tables, JSON and logs | 9% | 4,050 / 8,100 | 80 / 150 |
| F10 Invented jargon and definition following (30% real-text codebook) | 8% | 3,600 / 7,200 | 80 / 150 |
| F11 Fine-grained taxonomies, close distractors (30% real-text codebook) | 8% | 3,600 / 7,200 | 80 / 150 |
| F12 Tool and action selection | 6% | 2,700 / 5,400 | 40 / 80 |
| F13 Long documents, program-built | 4.5% | 2,050 / 4,100 (incl. DocFinQA's fallback, +250 / +500) | 40 / 70 |
| **Total** | about 100% (F13 4.5% includes the +250 / +500 DocFinQA fallback) | **45,250 / 90,500** | **>= 960 / >= 1,800** |

Shares F1-F12 are of the original 45,000 / 90,000. F13 carries the DocFinQA fallback rows (DocFinQA is out after the
3 Oct licence check; it returns only by amendment, and then F13 goes back to 1,800 / 3,600).

**F1. Policy composition and precedence**
- Skill: apply 3-12 rules to a case when rules have exceptions, amendments with effective dates, supersession, and a
  precedence policy stated in the card (specific beats general, later beats earlier, or a named priority order).
- Structure: rule base over 4-10 case attributes (Boolean, threshold, date, category); 0-3 amendments (modify, repeal,
  insert, with dates); a case with 0-2 attributes missing.
- Samplers: forward (rules, then case); label-first (pick the outcome, build a decisive chain of depth 1-4 and >= 1
  near-miss rule that fails on exactly one condition); decision-table-first; narrative policy memo. S5 (held out):
  flowchart text. Default depth cap 4; depth 5-6 only as deep items.
- Labels: solver A forward chaining with precedence; solver B z3 (MIT) or brute force over the parsed rules.
- Questions: choice among 3-8 outcomes (including "escalate" and, in open-world cards, "cannot be determined");
  yes/no ("Is the claim approved?" and negated forms); inverted ("Which case would be approved?").
- Twins: flip one attribute at a boundary; repeal the decisive rule; move an effective date; add an inert rule.
- Shortcuts to block: number of rules, exception words, and the decisive rule's position must not predict the label.
  Decisive rule position is uniform.

**F2. Rule arithmetic, money, quantities and dates**
- Skill: compute an amount, count or date under caps, floors, proration, tiers, stated rounding and exceptions, then
  decide a threshold or pick the value.
- **Depth (changed).** A one-pass readout cannot do long arithmetic (competitor "decider": rule paragraphs scored 0.24
  vs 0.67 for one sentence). Default: at most 2 operations, or more operations only when the text states each
  intermediate value. Items with 3-4 unstated operations are deep items (<= 10% of F2) and feed the depth sweep.
- Samplers: forward formula graphs; target-first (result placed below, at, or above a threshold by +/- 1 unit, 30%
  exactly at the boundary); tiered rate tables; calendar and business-day rules. S5 (held out): payroll-style
  statements.
- Labels: solver A Python `Decimal` + `datetime`; solver B an independent integer-cents and day-ordinal implementation
  on the parsed text.
- Distractors: each from one named error (missed cap, wrong rounding, off-by-one day, ignored exception, wrong tier,
  wrong unit).
- State day counts when the card's rule needs them (a competitor's date items went from 0.65 to 1.00 with stated day
  counts).
- Shortcuts to block: number magnitude; answer = largest or smallest option.

**F3. State tracking and record chains**
- Skill: track entity state over 5-40 events with VOID, CORRECTION, supersede, rename, merge and transfer; follow ID
  chains across notices.
- Samplers: forward event sequences; target-first (decisive event at a uniform random position, distractor events on
  look-alike IDs); ledger tables; multi-notice correspondence. S5 (held out): git-like log syntax.
- Labels: solver A event replay; solver B an independent version-graph resolver that follows pointers backwards from
  the query on the parsed text.
- Questions: final or at-time value; which record is current; "Does X still hold Y?" (with negated forms); "not
  enough information" when the card says the log may be incomplete.
- Metamorphic checks: no-op events, commuting reorders and ID renames leave the label unchanged.
- Shortcuts to block: last-event recency, ID string similarity. (A competitor's event-log family with VOID and
  CORRECTION entries took fresh yes/no from 58.8 to 71.6.)

**F4. Indirect evidence and multi-hop yes/no**
- Skill: decide whether a claim follows, is contradicted, or is undetermined from facts plus general statements, over
  2-4 hops, with defeasible exceptions.
- Samplers: forward chaining over a fact graph; FLD-style deduction with distractor facts and rules (Apache-2.0 code
  idea, our own implementation); evidence tables; witness statements. S5 (held out): facts embedded in narrative prose.
- Labels: solver A forward chainer; solver B model enumeration (truth tables) on parsed facts.
- Lexical overlap between claim and text is decorrelated from the label (HANS control).
- 30% of rows carry one inert but relevant-looking sentence; the label must not change (GSM-NoOp showed drops up to 65%
  from one such clause).

**F5. Hard and negated yes/no**
- Skill: answer yes/no correctly under negation, double negation, scope shifts, implicit negation (fail to, lack,
  deny, refuse, rule out, hardly, no fewer than, unless, other than), quantifiers and modal negation.
- Base items: (fact, question) pairs from the F1-F4 and F9 structures, and from human-gold public items in section 3
  (SQuAD 2.0 answerability, MuSiQue, 2WikiMultihopQA yes/no, QuALITY and Qasper yes/no, GHC, EDOS). For soft-labelled
  bases, the negated row gets 1 - p. ShARC, CAD-SNLI, Measuring Hate Speech, Social IQa, CosmosQA and NewsMTSC are
  not bases, and neither is any set built on them (3.G, 3.H). The F5 builder runs the deny-list check on every base
  source and its parents.
- Each base gives 4 rows in 2 units:
  - unit 1 (3 rows, one `call_id`): affirmative; negated (`complement`); double-negated (`equiv` to the affirmative);
  - unit 2 (1 row, own `call_id`): a scope-shift or implicit-cue variant, labelled by polarity logic.
- Cue bank: >= 250 templates in >= 12 cue families. 25 templates are held out for the hard-negation probe and never
  trained. No template may match a dev or eval negation wording (dev_negwords is a held-out template family; dev's
  dneg is 92% "Should the statement that ... be rejected?"; the C1 failure frame "only non-hateful" + outer "be
  rejected" is also a dev wording and is blocked).
- Labels: a polarity-logic program over the base label; solver B re-derives polarity from the parsed question.
- Balance: P(yes | number of negation cues) = 0.50 +/- 0.02 for 0, 1, 2 and 3 cues, so counting negations cannot help.
  "Yes = bad" at 50%. At least 25% of F5 rows are double negation.
- Size: 8% in round 1. Round 2's F5 share comes from the hard-negation probe under the bounded weight rule (recipe 7.2).

**F6. Not enough information and abstain as gold**
- Construction: start from an answerable twin and remove exactly one necessary premise (open-world card). Build "none
  of these" by deleting the gold option and checking that no remaining option qualifies. Add yes/no "Can it be
  determined that ...?" rows with the semantics stated in the card.
- Labels: solver A an open-world solver that proves neither answer follows; solver B z3 shows both answers are
  satisfiable.
- Target: gold is NEI or "none of these" on about 10% of all new choice rows (F6 plus other families).
  (v4, addendum C5, CONSIDER: **not applied in round 1**. Varying the gold-NEI rate per card over 0-20% while keeping
  the ~10% aggregate needs an owner OK or an amendment first.)
- The NEI option must also appear on rows where it is wrong (>= 50% of rows that show it).

**F7. Ordinal rubrics**
- Skill: pick a level on a 3-7 level rubric where adjacent levels differ in exactly one stated criterion.
- Samplers: random points; level boundaries (the decisive criterion just met or just missed); multi-criterion
  scoring sheets; narrative incident write-ups; **(v4, A2) cut-point rubrics (sampler id S6)**: a stated quantity binned by stated cut
  points (the card states the quantity, its unit and 3-7 ranges; the pack sets the numbers), with the top level as
  common as the others and values placed at, just below and just above each cut. No software-change size rubric here
  (that skill is the commit block's, under guard 4). The cut-point sampler is about 1/5 of F7 rows (r1 about 630 / r2 about 1,260),
  inside F7's 7%. S5 (held out): rubric as a table.
- Labels: solver A rubric evaluator; solver B independent re-implementation from the parsed rubric.
- Metamorphic: raising a severity factor never lowers the level.
- Labels carry their number ("Level 3 - Elevated") because the trainer shuffles options. Gold is uniform across levels,
  **end levels included (v4, A2)**: per sampler x K, each level is 1/K +/- 2 pp of rows, and every card shows gold at
  every level at least once (G10). Short end levels are fixed by generating more, never by relabelling. Distractors include both adjacent levels.
- **(v4, A1) Ordinal meta.** Every F7 row carries `meta.option_level` (option text to level index 0..K-1) and passes the
  ordinal target lint (G18).
- **(v4, A2) Report-only check (dev, never ejs-5).** On dev ordinal rows, the ratio of end-level predictions to
  end-level gold (C1: 0.65) is logged for C at each snapshot. Target >= 0.9. It chooses nothing.

**F8. Risk and probability**
- Skill: apply a card-defined scoring rule (points table), base rates with stated likelihoods (Bayes), expected cost
  or value, and risk-tier thresholds.
- Questions: probability-bin choice; "Is the expected loss above X?"; rank options by risk.
- Labels: solver A exact fractions (`fractions.Fraction`); solver B an independent exact implementation.
- **Soft targets (changed).** `meta.gold_probs` (exact posteriors) only on choice rows that ask which outcome will
  happen. Every yes/no row ("Is the expected loss above X?") has a hard 0/1 label, and the F8 source is **not** in
  `kd_full_src`. Reason: more soft yes/no targets push answers into the 0.4-0.6 band that JevBench v1.5.4 scores as an
  abstention.
- No real-outcome labels (noisy, high Bayes error). UCI credit outcome data is excluded for this reason.

**F9. Tables, JSON and logs**
- Skill: filter, count, aggregate, compare, join two tables, argmax with a stated tie rule, date windows; pick records
  out of JSON arrays of 10-200 records; read log lines.
- Containers: markdown table, CSV, HTML table, JSON, YAML, fixed-width text, log lines.
- Multi-select as single-letter choice: options list record sets ("A: R2 and R5 only").
- Labels: solver A pandas; solver B sqlite on the parsed text.
- Metamorphic: row shuffle, column rename and unit restatement leave the label unchanged.
- Shortcuts to block: answer in the first row; number magnitude.

**F10. Invented jargon and definition following**
- Skill: decide using terms that exist only in the card, and definitions that override a word's usual meaning (for
  example "minor" defined as "over $5,000").
- Invented words are checked against a large word list (>= 300K entries, 3 languages) and carry no morphology hint (no
  "-phobia", "mal-", "-itis").
- 40% of F10 choice rows use neutral IDs ("Category K7"); 30% use swapped label words; 10% of F10 rows are
  label-description rows (the text paraphrases one definition).
- Twins: swap two definitions; the label must follow the definition.
- Labels: solver A definition substitution; solver B attribute matcher on the parsed definitions.
- 30% of F10 rows are real-text codebook variants (section 2.3).
- Evidence: GoLLIE went from 42.3 to 55.3 F1 on unseen schemas; removing examples inside definitions cost the most
  (-5.4). 7-12B models lean on label names more than on definitions (Codebook LLMs).

**F11. Fine-grained taxonomies and close distractors**
- Skill: choose among 20-60 near-synonym labels with sharp definitions and boundary notes.
- Construction: items are attribute vectors (for example mechanism, object, severity, actor) rendered through
  templates; a mapping table gives the label.
- Option display: all labels on 50% of rows; a subset of 8-15 that includes the 2-3 nearest labels on 50%. Codes on
  50%, names on 50%.
- Close distractors: every row has >= 1 option that differs from gold in one attribute.
- Labels: solver A the mapping table; solver B a decision tree compiled independently from the card text.
- 30% of F11 rows are real-text codebook variants (section 2.3).

**F12. Tool and action selection**
- Catalog: >= 200 invented APIs in >= 40 domains, written by Claude, with JSON-schema parameters. No public tool
  dataset text is used (they contain LLM-written text; see 3.G).
- Requests come from structured intents. Outcomes: call tool X; ask for a missing parameter; unable; answer directly
  without a tool. Also "which parameter is missing?" and "is this call valid?" (yes/no).
- Distractor tools differ in one capability or one parameter.
- Labels: solver A schema matcher; solver B independent validator.
- Disclosure: the four outcomes copy When2Call's design (a Jev Decision Index test). Report DI When2Call as "trained on
  a similar task design", never as unseen.

**F13. Long documents, program-built**
- Coherent documents of 2,000-7,900 tokens: manuals, case files, audit logs, multi-table reports. Every section is
  domain content from the same pack. No filler text.
- Decisive content sits in 1-3 sections at depths uniform across the 10 deciles. Near-miss sections: a superseded
  version, another region's rule, a look-alike ID.
- Questions reuse the F1, F3, F6 and F9 skills. Length bins: 2-4K tokens 50%, 4-6K 30%, 6-7.9K 20% (token cap,
  section 6).
- **(v4, F3) "Aggregate" sub-type, about 20% of F13 rows (r1 about 410 / r2 about 820), inside F13's 4.5%.** The answer
  needs facts from **2-3 sections**: a count (for example of active exceptions), the latest valid version among
  several, or a total over a table split across sections. Labels come from the generator's ground truth (solver A) and
  an independent re-solve on the parsed document (solver B), like every family; no LLM labels, no filler. The decisive
  sections keep the uniform-depth rule; `meta.subtype` = "aggregate". Low confidence: expected LongBench v2 effect +0
  to +2 pp.
- Twins: move the decisive section (gold unchanged; `equiv`, a 2-row unit); delete it (gold becomes NEI; its own
  unit, no relation term).
- Evidence for this design: burying a short state in filler cost a competitor 22-43 pp, and training on filler moved
  real long documents by only +/- 1 pp; ProLong found synthetic long SFT data hurt. So F13 uses coherent documents and
  stays small, and real long documents come from the public block (3B).


### 2.4 Row format (own rows)

Same raw format as `GOLDEN_SPEC.md`, with extra meta:

```
{"id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card",
 "meta": {"family": "F1".."F13", "spec_id", "card_id", "domain_pack", "sampler": "S1".."S4" | "S6".."S9" | "S5" (S5 is always the held-out sampler: mix-tuning dev items only, never a training row),
          "gen_version", "git_sha", "seed", "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep": bool,
          "format_style", "wording_id", "defs_style", "twin_of", "twin_kind",
          "text_source": null | {"dataset", "record_id", "split": "train"},
          "licence": "CC0 1.0 (program-generated)" | <dataset licence for real-text rows>,
          "edge": [...], "gold_probs"?: {...},
          "option_level"?: {<option text>: <level index 0..K-1>},   (v4, A1: required on every ordinal row)
          "subtype"?: "aggregate" | "cutpoint" | ...,               (v4: F13 aggregate, F7 cut-point)
          "persona_seed"?: <O*NET code>}}                           (v4, F4: when the pack or scenario has one)
```

**(v4, A1) Ordinal rows.** An ordinal row is any row whose options are the levels of one ordered scale: every F7 row,
every commit score row, no public row in round 1 (UCI Car and Nursery classes are not marked ordinal, like F8 bins,
so A4 keeps its sized row set), and replay rows whose options carry level numbers (the mixer detects these by
program, adds `option_level`, and counts them in its report). F8 probability-bin rows are not marked ordinal in round
1 (this keeps the row set that the recipe's A4 mean term was sized on: F7 own rows + commit Score rows + replay). `option_level` keys the canonical option text, so the trainer's option shuffle does not change it.
Commit rows carry the same meta keys that apply to them, plus `input_view` ("message_only" | "message_diff") and, on
message-only rows, `trigger_entities` (4.2).

Definitions go to `data/c_parts/defs/<key>.json`. Relations (`complement`, `equiv`, `inv`) go to the relation file in
the format `train_decoder.py` reads. Builders live in `c_src/<family>/`; outputs in `data/c_parts/`.

---


## 6. Format augmentation

| Lever | Spec | Evidence |
|---|---|---|
| Format style pool | About 400 styles = container (prose, memo, email thread, chat log, JSON, YAML, CSV, markdown table, HTML snippet, key-value record, bullet SOP, log lines, diff, form) x card style x register x instruction position. 50 styles are held out for the mix-tuning dev only and never trained. The sealed suite uses its own styles, written by the sealed agent | Prompt format alone moved LLaMA-2-13B by up to 76 points (Sclar et al.) |
| Instruction wordings | >= 30 per family, >= 5 per card; >= 3 per public dataset | Many templates gave +1.9 to +5.6 ROUGE-L on small Qwen3/Llama models, more on the worst template (Sadrieh and Stefanik 2026) |
| Definition styles | one-line; one-line + 1-2 examples (about 50% of cards); rubric table; short or no card (about 15% of rows; today 4%) | GoLLIE ablation; Super-NI "definition + examples" |
| Few-shot cards | 5-10% of cards | Flan: >= 5% few-shot templates improved zero-shot |
| Inverted cards | 10-15% of cards | Flan: removing input inversion cost 8.6 MMLU and 7.8 BBH points |
| Masked / swapped label names | 10-15% / about 5% of choice rows | GoLLIE; Codebook LLMs |
| Option counts | 2-60, buckets in section 2.1 | C1 weak at 21+ options |
| Registers and locales | Formal, casual, terse, verbose; US and UK spelling; date formats; currencies; units | AttrPrompt |
| Lengths | Non-long rows: median 500-900 tokens. Long rows: 2,000-7,900. No row above 7,900 real tokens (fits `micro_tokens` 8192) | |
| Batching | A relation unit holds at most 3 rows (F5 splits its quadruple into a 3-row unit and a 1-row unit); long units at most 2 rows | Same-batch paraphrases gave conflicting updates on 57-64% of weights (Sadrieh and Stefanik) |

Format variety lives inside `state`, `instructions`, `options` and the card. The outer prompt layout
(`schema_branch_mark`, cygnet style) stays exactly as trained, served and evaluated.

**Token cap (real tokenizer, enforced by the mixer).** Rows of 2,000 tokens or more are at most 9% of new rows and at
most 30% of new-row tokens. Planned round 2 (assumptions: own non-long rows about 850 estimated tokens, F13 about
4,600, public long about 5,600, commits about 800): long rows are about 6,000 (5% of new rows) and about 25% of new-row
tokens. If the real count passes 30%, the mixer drops F13 and 3B rows from the 6-7.9K bin first.

---


## 8. QC checklist (every family passes every gate before it enters a mix)

| Gate | Pass rule | Tool / cost |
|---|---|---|
| G0 Spec first | 1-page spec per generator with a semantics table (open or closed world; "unless", "only if", "at least", inclusive or exclusive "or", date ranges, rounding, ties, units; exception precedence). Every choice that could flip a label is stated in the card. A second Claude session lists ambiguities; all are resolved | CPU |
| G1 Provenance | Every row has the section 2.4 meta. Every public source has an upstream licence URL + commit + sha256, and a document-text licence note. Every (H) set is dropped unless an upstream record is found (decision 6). **(merge 3 Oct)** The cited URL is the official record named in `LICENCE_REGISTER.md` section 1-2 (never an HF card or mirror); the builder re-reads it, and a changed or missing record fails G1. Per-item text filters are logged per item (QuALITY article field, Qasper arXiv licence, CommitPackFT `license`). **(v3)** The 3.H deny-list program passes every dataset and every declared parent, and no input path is on the 7.4 Jev list (mixer input log) | CPU |
| G2 Independent re-derivation | Solver B (different paradigm) agrees with solver A on **100% of rows**. Any mismatch: stop, fix, regenerate the whole generator. **This and G3-G4 are the primary label guarantees**, because Claude both writes and blind-reads, so Claude errors can correlate | CPU |
| G3 Round-trip parse | Parse the rendered text back and re-solve: **100% agreement** | CPU |
| G4 Metamorphic tests | >= 3 relations per generator (option shuffle, rename, inert sentence, row or rule reorder, negate a premise, remove a premise, monotonic severity, injected instruction), **100% pass** on >= 1,000 rows. Hypothesis (MPL-2.0) for property tests | CPU |
| G5 Blind read | A separate Claude session (never a generator author) sees only the card and text. **Claude is a flag-only reader (decision 2): it never sets, edits or chooses a label.** 300 rows per family; 600 for F1, F5, F6, F13 and commits. **Zero confirmed wrong golds** (95% upper bound 1.0% at n = 300, 0.5% at n = 600). Ambiguous <= 1%. A confirmed error is a generator bug: fix, regenerate, re-sample a fresh 300. Claude only flags; a label is never edited by hand. Public and real-text rows: dataset-level decisions only (drop the dataset if > 8% clearly wrong; SQuAD 2.0 > 5%), never row by row. **(v4, B1)** The 600 commit rows include 300 message-only rows (stratified over route, triage and gate); a message-only row whose decisive fact the reader cannot find in the message counts as ambiguous (bar <= 1%). Above the bar: tighten matcher M (alias lists, stop list), regenerate the message-only rows and re-sample a fresh 300 | agent time |
| G6 Partial-input and metadata baselines | Per family, 5-fold CV on a **separate QC sample of >= 5,000 rows** from the same generators (F8, F12 and F13 have fewer real rows): bag-of-n-grams logistic regression + small gradient-boosted trees on (a) question only, (b) options only, (c) card without question, (d) metadata only (depth, rule count, length, option lengths, number magnitudes, name pool, template id, sampler id, repo). Accuracy <= chance + 2 pp. **(v4, B1)** Message-only commit rows are a separate group, and (d) adds the number of areas or entities M hits and `input_view` | CPU |
| G7 Feature z-test | One-sided binomial per unigram, bigram and metadata feature; p0 = 1/k; alpha 0.01 Bonferroni over features. Yes/no with 50K features: a feature fails at 200 occurrences with >= 67.9% one label, 1,000 with >= 58.0%, 5,000 with >= 53.6%. No feature may fail. Fix by matched twins first, z-filtering second. **(v4, B1)** On the message-only route slice, "option is the first area M hits" is a tested feature on rows where M hits m >= 2 areas (p0 = 1/m) | CPU |
| G8 AFLite-lite | Frozen MiniLM-L6 (Apache-2.0) embeddings, 64 partitions, linear models, tau 0.75. Predictable share < 10% per family. Over 10%: find the cue and fix the generator; do not bulk-delete | CPU |
| G9 Difficulty from the crowd | C1, 4B-E and base 4B score every candidate row on the free L4 (decision 3; not the H100). Bins and stratified selection as in 2.1. Every row with crowd p_g < 0.05 enters a G5 re-read sample (300 per family; any confirmed error = generator bug). After stratified selection, label x bin chi-square p > 0.01. (v4) Selection stays stratified and representative (addendum D1): no LESS, influence, IFD or targeted selection. Addendum D2 (facility location on C1 hidden states for public 3A-3E rows) is CONSIDER: D2 is decided once, in the C PREREG amendment (before any C row exists). It is adopted for round-1 public rows (3A-3E) only if this G9 L4 pass can log C1's pooled hidden states at no extra time. Otherwise it lapses for C (it cannot be added later) | free L4, about 20-28 h (no Modal spend) |
| G10 Balance | Aggregate yes rate 50% +/- 2 per family x wording x bin x negation count (per-card rates vary 20-80% by design); gold letter uniform per option bucket (chi-square p > 0.01); "longest option is gold" within +/- 2 pp of 1/k; abstain options wrong on >= 50% of rows that show them; "attack present" uncorrelated with the label. **(v4)** Commit gate (per rule) and match (per card) yes rates within 20-80%, aggregate 50% +/- 2 per type x wording x bin (B2); per gate rule, the message-only yes rate is within 5 pp of the rule's drawn rate, checked on rules with >= 20 message-only rows and pooled by rate decile otherwise (B1); ordinal levels: F7 each level 1/K +/- 2 pp per sampler x K, commit score each level >= 1/K - 5 pp per rubric, end levels included (A2); replay hard-label yes/no rate 50% +/- 5 per wording cell with >= 50 rows; smaller cells are checked pooled by wording family (E2, section 5) | CPU |
| G11 Diversity | Card, pack and sampler counts as in 2.1; no surface template above 2% of a family; every Claude seed has ROUGE-L < 0.7 to all other seeds; compression ratio, Self-BLEU and Vendi score no worse than the same family's slice of golden_train | CPU |
| G12 Dedup | Exact hash: 0 duplicates. MinHash near-dups: keep one. Structure hash: one surface form per structure, except planned twins and format variants | CPU (datasketch, MIT) |
| G13 Decontamination | Section 7. Zero hits after drops | CPU + orchestrator counts-only runs (decision 1) |
| G14 Sealed separation | The sealed suite exists and is frozen, with its sha256 committed in a PREREG amendment, before any C data exists: no generator run, pack, style pool, codebook, public row or commit row. No C builder has read access to it. The build log shows the order | process |
| G15 Loader round-trip | Every row passes `train_decoder.check_rows`; render each row through `decoder_io.user_msg` under a random permutation; map the displayed gold letter back to the canonical gold: **100% match**. Print 20 rendered prompts per family and read them. **(v2)** Every relation unit shares one `call_id` and has <= 3 rows; units with a row >= 2,000 tokens have <= 2 rows; real-tokenizer length <= 7,900 for every row | CPU |
| G16 Owner audit (**optional, non-blocking**, decision 11) | If the founder chooses: 200 rows answered blind on an audit page: 30 from each high-risk block (F1, F5, F6, F13, commits) + 50 stratified over the rest. Agreement >= 95% per block, and every disagreement is adjudicated against the spec. About 2-3 hours. Round 1 never waits for it; a failed block found later is fixed before round 2 | owner time |
| G17 Post-round-1 cartography | Log per-row gold probability at the 25/50/75/100% snapshots. Audit 30 rows per family from the low-confidence, low-variability region with G5. If >= 15 of 30 are wrong, fix the generator before round 2 | reads only |
| G18 Ordinal target lint (v4, A1) | Every ordinal row (2.4) has `meta.option_level` covering all its options, and `round_half_even(E_target) == gold level` on the actual training target after smoothing, KD and the C1 anchor (section 5). Fallback to smoothed gold, else drop. **100% pass** in the builder and again in the mixer, before every freeze | CPU |

Public rows pass G1, G6 (on our framings), G7, G10, G12, G13, G15 and a G5 read of 100 rows per dataset (300 for
SQuAD 2.0). (v4) Replay rows on a level scale also pass G18.

---


## 10. Mix-tuning dev (separate from the sealed suite)

| Part | Items | Use |
|---|---|---|
| 13 families x 400 (S5 sampler, held-out packs, held-out styles) | 5,200 | Bounded weight update (recipe 7.2); paired SE about 1.8-2.5 pp per family |
| Depth sweep: F1, F2, F3, F4 x 5 depth levels x 60 | 1,200 | Sets round-2 depth caps: the deepest level where round 1's candidate CAND - C1 >= +3 pp and CAND >= chance + 15 pp |
| Hard-negation probe (the 25 held-out cue templates) | 400 | Report only (recipe 6.4); F5 size for round 2 (recipe 7.2) |
| Commits from 30 held-out repos | 400 | Commit transfer before any ejs-5 read |
| Public: our own 10% splits (by page or record; never official dev or test) | 600 | Public-block check |
| F14 hold-out family: one skill family that is never trained (the QC agent picks it, for example constraint scheduling) | 400 | Report only: transfer to an untrained family |
| Codebook behavioural tests (generic labels, swapped labels, exclusion pairs) | 300 | Report only |
| **Total** | **about 8,500** | Never used for the final ship decision |

Rules for this set (rules S7):
- No item shares a `group_id` or normalized text with golden_train or with any C training row.
- Wikipedia-based public items are split by page title.
- Commit items come from the 30 held-out repos of both commit datasets. **(v4, B1)** They mirror the training form:
  30% of their route, triage and gate items are message-only (same keep rule), inside the 400.
- The 50 held-out format styles are C-side only. The sealed suite has its own styles.
- Temperature refits use dev or this set only (recipe 6.4).
- **(v4, B3) Yes-share drift alarm, report-only.** At each training snapshot the dev read logs, per part and per
  domain (each family, commit type, public dataset and F14), mean P(yes) and the predicted yes share on yes/no items,
  without using gold. Snapshot reads use a fixed T stated in advance: T = 1 (C1's recipe 6.0 serving T is not yet
  fitted for snapshots). Alarm if a domain that is 50/50 by construction falls outside 30-70%. An alarm is logged and
  reported; it never moves a share, weight, temperature, readout or candidate by itself (any change needs an
  amendment before round 2).
- **(v4, A2)** Ordinal items here also log the end-level ratio (end-level predictions / end-level gold), report-only.

---


## G8 RULING (A19.1, verbatim pointer)
See PREREG_FINAL.md "Record A19 result + Amendment A19.1" and c_src/<FAM>/tmp/repair/G8_RULING.md. Choice parts: G8v3 p > 0.009. Yes/no parts: the G8 bar is not gating (proven infeasible); G6 + G7 (and a TF-IDF G6 baseline if the A19.1 power check requires it) carry yes/no screening once c_build/g8v2/A19_ADOPTED exists.
