# C2.1 v3.2 addenda: ruling-to-code conformance survey (Sun 18 Oct 2026, read-only)

Scope: 11 families (GEN, T41c, T42c, T51, T53, T54, T55, T56, T56g, T57, VOICE). T50 is excluded by instruction (see the T50 line below).
Method: each addendum (plus its "Opus batch-1 rulings v3.2" block) and G0_APPROVALS_v32.md (GV1-GV13) was read against the code under
`c21_fam/<F>/` and shared code (`LA_COMMON`, `LC_COMMON`, `GEN`, `VOICE`, `tool_engine`, `LK_COMMON`, `LR`). Constants were checked
against what functions actually use. Only each family's own pytest suite was run; no generator, builder, dry run, model, API or Modal
call. No `solver_b/` or `LC_SOLVER_B` code was read (existence listed only). No path containing ohs / sealed / quarantine / longbench /
jevbench / c_spec/sealed_brief / c_build/preread, no Jev outputs and no ~/.claude path was opened.
Status words: IMPLEMENTED (code does it), PARTIAL (something specific is missing), MISSING (no code), N/A (orchestrator, model-read,
post-training or L-0 job). The survey was done by seven read-only sub-surveys; the counts in the summary were recomputed by program from
the tables below.

T50: known to lack its addendum (block G missing, sizes not substituted); an agent is implementing it; not surveyed here.

## Summary table

| Family | Lane | Items | Implemented | Partial | Missing | N/A | Contradicts a ruling in code? |
|---|---|---|---|---|---|---|---|
| GEN | L-G | 77 | 21 | 16 | 35 | 5 | yes (sizes, dev split, ladder band) |
| T41c | L-I | 64 | 14 | 17 | 29 | 4 | yes (GV2 held-out draw, HO 480, raw K3, LS cap, OHS-5 count) |
| T42c | L-C | 47 | 10 | 10 | 20 | 7 | yes (head and language shares) |
| T51 | L-A | 32 | 5 | 4 | 21 | 2 | no (code absent) |
| T53 | L-A | 31 | 4 | 6 | 20 | 1 | no (code absent; block d 4 rows short) |
| T54 | L-T | 52 | 8 | 10 | 29 | 5 | behavioural only (orphan gate, freeze_collision, stamp sha) |
| T55 | L-T | 46 | 14 | 8 | 22 | 2 | no (open points: L2 mapping, B4 mix) |
| T56 | L-T | 59 | 16 | 8 | 32 | 3 | yes (sizes, reason mix, P-2, card clause) |
| T56g | L-C | 47 | 10 | 14 | 18 | 5 | deviations (contra weight, K10 20% share) |
| T57 | L-C | 46 | 12 | 12 | 17 | 5 | yes (reuse counted on primaries only) |
| VOICE | L-G | 39 | 20 | 9 | 7 | 3 | defects only (V-C8 split, GV5 siblings) |
| TOTAL (11 families) | | 540 | 134 | 114 | 250 | 42 | |
| T50 | L-A | not surveyed | | | | | known: block G missing, sizes not substituted; an agent is implementing it |

### Top 10 missing items by row impact (trained rows affected; approximate, from each addendum's own sizes; items overlap)

1. L1-L4 difficulty ladder, level tags, twins and the L3-L4 >= 25% composition: missing in 9 of 11 families (GEN has only 3 bins, VOICE has WER bands). About 24,000 trained rows must carry a level, and about 6,000+ must be at L3-L4 (T54 4,000; T51 3,500; T55 3,000; T41c 2,000/3,000; T42c 3,000; T57 3,000; T56 2,000; T53 2,000; T56g 1,000).
2. T51 + T53 (L-A) have no stamp wrapper, per-row answer-check driver, drop/replace loop, GV5 retirement, K12/K15 token rule, PII scrub or K14s/K18s: 5,500 rows (3,500 + 2,000) cannot enter a pool.
3. A15 dialect renderer (7 dialects, 5 trained, 2 held out) in L-A: 5,500 rows (T51 3,500 + T53 2,000), plus the card-text renderer it needs.
4. GEN length tiers LT1-LT4, PAD-INERT, pad invariance G-L2 and per-tier probes: about 4,900 rows (LT2-LT4 are 70% of 7,000; LT4 about 700).
5. GEN TP (2,000: DM 600, RG 1,000, BA 400) and HX (1,100) not built, and the five old sub-blocks still carry the old sizes (1,600/1,500/1,300/1,300/1,300): 3,100 rows missing and 3,100 mis-allocated.
6. Quad (alarming/calm x risk present/resolved): T56 1,600, T56g 600, T51 400, T53 400, T41c 400-600 = about 3,400-3,600 rows (T56g today is label-perfect on its alarm lexicon, so K18 would fail on all 600).
7. A16 observation-format / VR-FMT re-rendering: about 3,400 rows (T55 ~1,080, T56 ~800, T57 650, T41c 260/390, T56g 250, T54 ~200, T42c ~151); T42c's latent CR/ESC format-probe conflict would drop its CRLF/ANSI views.
8. T41c: the GV2 held-out wrapper contradiction touches every row's wrapper draw (2,000/3,000 + 160 HO rows); A13 lexicon rows 760/1,140 (pool-side BoW AUC 0.99 vs bar 0.55 predicts a K13 kill-gate FAIL); 196 of 360 generator cells have no wordings, so no production row can be built.
9. L-A lever rows: T51 A3 edit carrier 500 + A6 450 + A12 350 (A10 300 conditional); T53 phishing head 300 + A6 350 + A12 250 (A10 250 conditional): about 2,200 rows (+550 conditional); T53 head also needs K30/K31 and a new question form.
10. T56 D6 verify-relevance (400 new rows) plus the size/reason-mix re-split (400 rows now generated in the wrong sub-blocks; P-2 would fail a conforming family), runsim, E2/E6 gold and the exit_after_pipe card clause (about 840 rows' card text); next: T42c COMPILE2 300 + head re-split (OUT4 -120, EQV2 -90, TFAIL2 -90), T57 LOCALISE FILE/HUNK 320 (+ T57r up to 2,000 outside the 3,000).

Next tier: A12 about 1,600 rows over L-A/L-T/L-I (T51 350, T54 300, T53 250, T55 200, T56 200, T41c 200-300); A10 about 1,600 rows, conditional on the Fri 23 probe (T41c 200-300, T51 300, T53 250, T54 200, T55 150, T42c ~151, T57 150, T56 100, T56g 60); A14 about 600 rows, conditional (T54 200, T55 150, T56 100, T41c 100-150); held-out dev rows (T54 160, T55 120, T56 80, T51 140, T53 80, T41c HO/BD/LS, T42c 90, T57 60, T56g 40) and the GV9 mix-guard tag/test, absent everywhere outside T59/T60/T67/GEN/LK_COMMON.


## Headline findings

1. The code for 10 of the 11 families is the pre-v3.2 (G0-lite) build (VOICE is largely conformant; only Generator C and a few gates are missing). For every L-A, L-T, L-I and L-C family the v3.2 levers (A10, A12, A14, A16, A15 in L-A, the L1-L4 ladder, the quad, twins, held-out dev rows) are not in code, and every family's HASH_EXPORT.json is still the v1 export (none holds a v3.2 lever, wrapper pool, or ladder table).
2. The per-row "check at creation" spine exists for T41c, T42c, T55, T56, T56g, T54, T57, GEN and VOICE (stamp wrapper plus GV5 whole-group retirement are implemented and tested). T51 and T53 (L-A) have NO stamp wrapper, no per-row answer-check driver, no drop/replace logic: they only have set-level gate functions.
3. Hard contradictions with Opus rulings found in code (not just absent code):
   - T41c `planner.draw_heldout` still draws held-out wrappers by seed (returns wrap.preauthorised_disguise + wrap.urgency); GV2 fixes cue.persona (role_play + benign_justification). It holds out two styles that must be TRAINED. `HASH_EXPORT.heldout_draw.sha256` pins the stale draw.
   - T41c `gates.gate_k3` makes the RAW-view gap the kill gate (Q6 ruling: normalised view is the kill gate, raw is report-only); `plan_heldout` gives HO 480 (ruling 780); `rowcheck.TOKEN_CAP` 1,536 is applied to the eval-only LS block (rows would be dropped).
   - GEN `gen_common.FORMS` / `SUB_BLOCK_TARGETS` / `DEV_PER_SUB_BLOCK` still hold the old sizes (1,600/1,500/1,300/1,300/1,300 and 120 dev each) against GEN-B1 (800/900/800/700/700 plus TP 2,000 and HX 1,100; dev 90/90/80/80/80/90/90).
   - T56 `SIZES` / `REASON_MIX` / `p2_sizes_mixes` enforce 900/350/250/300/200 (no D6); a conforming 650/300/250/250/150/400 family would FAIL P-2.
   - T42c `HEAD_SHARE` 0.40/0.30/0.30 and one global `LANG_SHARE` against the addendum's 1,080/810/810 + COMPILE2 300 and per-head language table.
   - T57 reuse is counted on primary rows only (addendum: counted over wrapper/variant copies); `LANG_SPLIT` is defined but unused.
   - T56g `build.make_units` LIB-CONTRA weight 0.10 gives about 70 rows, not 100; `gates.k10` allows a family share of 20% against the 15% bar.
   - VOICE `vgates.gate_c8_sizes` evaluates the generator split with the default 55/45 table, so 50/30/20 with C on would be mis-flagged. GV5 sibling retirement is not implemented in VOICE.
4. Shared-code defects that hit several families (fix once): (a) a stamp hit whose entries are all exempt, including `freeze_collision`, is kept as clean (`tool_engine/row_pipeline.py:445`, `LP_COMMON/pipeline.py:38,129`; GEN/T41c have the same semantics) while V32-10/V32-13 say OHS-5 collisions are dropped row by row (<=5%); (b) the stamped `generator_sha` covers only 4-5 family files (excludes `tool_engine/*`, pool JSON, gates, solver_b), against "any change = new export + re-stamp"; (c) the 1% G13 fix-trigger denominator includes refill rounds (not first-pass only, GV5); (d) no GV12(b) "nothing added" closed-lexicon scan anywhere (`wording.reword_ok` checks slots/numbers/negation count only); (e) no signed ruling-to-code conformance-record refusal in `tool_engine`, T41c, `LC_COMMON` (GEN and VOICE have one); (f) L-A, `LC_COMMON`, T41c and GEN `GenAllow` still pin NAMES_MANIFEST_V1 (not V1.1/V1.2), so every new carrier/runner/family name would be refused at row time; (g) `tool_engine` `generate_in_memory(standin=False)` no longer raises NamespaceError (3 stale tests fail in T54, T55, T56).
5. Reusable correct code already exists and is not wired to the families: `LK_COMMON/klevers.py` (GV1/GV2/GV6-conformant wrapper library: trained authority/urgency/fake_approval, held out roleplay/benign_justification; pert.* ids with the correct trained/held-out split) and `tool_engine/row_pipeline.py` (`run_checked`, StampHook, GV5 group retirement) - L-A, T54/T55/T56 and T41c can import these instead of rebuilding.
6. Test health (families' own suites): T51 19 pass; T53 27 pass; T41c 146 pass / 1 fail (stale HASH_EXPORT g0_records sha after Batch 1b appended to G0_APPROVALS_v32.md); T54 30 pass / 1 fail (stale NamespaceError test); T55 25 pass / 1 fail (same); T56 38 pass / 1 fail (same); T42c 59 pass; T57 54 pass; T56g 44 pass (single run ~3.5 min, over the 2-min limit; passed in two parts); VOICE 109 pass; GEN 112 pass (two halves); LA_COMMON 72 pass / 3 skipped / 1 fail (stale T50 export). No test failure is an addendum defect; the passing tests assert the OLD (pre-v3.2) shapes in several families (T41c HO 480, T42c head/language shares, T53 block d tolerance).
7. Dry runs: none of the 11 family dry runs uses the addendum's v3.2 sizes or levers. T51, T53, T54, T55, T57 plan from base sub-block/head sizes that happen to match the addendum totals (T53 block d is 4 short); GEN, T41c, T42c, T56, T56g, VOICE plan from old or test-only sizes (see each family section).
8. Snapshot caveat: the survey read the tree between about 14:55 and 15:12 ET on 18 Oct. While it ran, the T50 implementation agent added shared L-A files: `LA_COMMON/edits.py` (15:22; file_edit / apply_patch / file_write carriers, canonical hunk, parse-back), `LA_COMMON/perturb.py` (15:21; the GV6 pert.* library with the correct trained/held-out split), and edited `LA_COMMON/spec.py`, `state.py`, `names.py` (15:08-15:11). These were NOT in the tree when the T51/T53 sub-survey read it, and T51/T53 code does not import them, so the T51/T53 statuses below (edit carrier, A12, GV6 library: MISSING) stay correct for T51/T53 themselves, but the "shared spec_v2 edit renderer absent" and "GV6 library not in L-A" remarks are now partly stale. `LA_COMMON/names.py` still refers to NAMES_MANIFEST_V1 in its docstring (not re-checked after the edit). Re-run this survey for L-A after the T50 agent finishes. Also seen modified in the last 80 minutes by other agents (not surveyed here): c21_fam/T67/*, families/RULINGS_T50_GF.md, RULINGS_T59_T60_T63.md.

## GEN (lane L-G) - code: c21_fam/GEN; solver_b/ exists (not read)

Verdict: pre-addendum five-sub-block generator (20 forms, old sizes) with a solid check-at-creation pipeline (`row_check.build_checked`). TP-DM/RG/BA, HX-E/U/S/T/O/D, ladder, length tiers, PAD-INERT and NOTA-GENERIC are not built (the code says so: `gen_hash_export.UNBUILT`, `row_check` docstring, SCHEMA.md s6, `builder.py:309-311`).

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | ARITH 800 = AR-F1 450 / F2 150 / F3 200 (s1, GEN-B1) | MISSING | gen_common.py:37-41 FORMS 1100/300/200 = 1600; SUB_BLOCK_TARGETS ARITH 1600 (:46). CONTRADICTS GEN-B1 |
| 2 | LOGIC 900 = 300/300/200/100 (s1) | MISSING | FORMS 500/500/300/200 = 1500. CONTRADICTS |
| 3 | CAUSAL 800 = 250/200/150/100/100 (s1) | MISSING | FORMS 450/300/250/150/150 = 1300. CONTRADICTS |
| 4 | TEMPORAL 700 = 250/150/150/150 (s1) | MISSING | FORMS 450/300/250/300 = 1300. CONTRADICTS |
| 5 | TABLE 700 = 250/200/150/100 (s1) | MISSING | FORMS 500/350/250/200 = 1300. CONTRADICTS |
| 6 | Total stays 7,000 with TP 2,000 + HX 1,100 substituted for 3,100 old rows (s1, GEN-B1) | MISSING | SUB_BLOCK_TARGETS sums to 7,000 only as the old five-block split; no TP/HX targets |
| 7 | ~8,850 candidates (~16% buffer); a drop is replaced by next seed of the SAME cell; no back-fill above +25% (s1) | PARTIAL | row_check.build_checked max_refill_rounds=3, next_index per (form, split) cell. No 8,850 plan, level not in the cell key, no cross-sub-block +25% cap |
| 8 | DEV 600: ARITH 90, LOGIC 90, CAUSAL 80, TEMPORAL 80, TABLE 80, TP 90, HX 90 (s1) | MISSING | gen_common.py:47 DEV_PER_SUB_BLOCK = 120 x 5; TP/HX dev absent. CONTRADICTS |
| 9 | D23/D24 and 10% wording groups dev-only (s1) | IMPLEMENTED | gen_common DEV_DOMAINS, DEV_WORDING_GROUP=9; builder._domain/_word; test_split_integrity_train_vs_dev |
| 10 | No hard-bin upweight, weight 1.0 (s1) | IMPLEMENTED | builder._make_row weight 1.0; validate_row; check_row "weight" |
| 11 | G0-lite shape rules on rows: pair share, letter balance, yes-share 40-60, L1 thirds +-5 pp, token/wording rules (s1) | IMPLEMENTED | gates.gate_a4_label_shape, gate_a5_shape (PAIR_BAR .30, TRAP_BAR .35, L1_THIRD_PP .05); five old blocks only, TP/HX not covered |
| 12 | Rows written only through the stamp wrapper, batches <=500 (s2) | IMPLEMENTED | row_check.build_checked/flush BATCH_ROWS=500. Nit: whole 1-2-row units can make a 501 batch (row_check.py:324) |
| 13 | (a1) solver A = solver B (s2) | IMPLEMENTED | RowChecker.check_row (A_error / A_B_answer_differs / B_reject); five blocks only; TP "B re-derives from instance fields" absent |
| 14 | (a2) render parse-back, exact (s2) | IMPLEMENTED | check_row: agree_core.diff(canon.canonical_spec(spec), B parse) -> "parse_back" |
| 15 | GV12 two-way slot round trip (a) verbatim (b) nothing added | PARTIAL | (a) builder slot_check; (b) agree_core.diff is symmetric but no closed-cue-lexicon scan; wordings are fixed pool templates |
| 16 | (a3) uniqueness: one correct option, options distinct after normalisation (s2) | IMPLEMENTED | builder.validate_row + norm_option; gates.gate_a3_uniqueness |
| 17 | (a4) pad invariance, G-L2 100% (s2, s8) | MISSING | row_check docstring "NOT BUILT"; any row with `pad` refused (:131-133); Summary pad_invariance="not_built" |
| 18 | (a5) pair integrity: partner drop drops both, re-made from next seed (s2) | IMPLEMENTED | RowChecker.pair_problems (:199); whole-unit drop in build_checked |
| 19 | (a6) names guard: NS-TRAIN names, closed domain/unit/carrier/form lists (s2) | IMPLEMENTED | validate_row, GenAllow; five old blocks; see item 70 for manifest pin |
| 20 | (a7) token rule: row <=1,536; mean <=800, >1,024 on <=10% (s2, GV4) | IMPLEMENTED | row_check MAX_TOKENS, builder HARD_TOKEN_CAP, gate_a5 TOKEN_* |
| 21 | (a8) PII scrub and C_DATA_SPEC guards, drop-only (s2) | IMPLEMENTED | row_check._PII, _LITERALS |
| 22 | (a9) decision_spans with roles, voice-eligible forms (s2, G10) | IMPLEMENTED | builder.decision_spans_of; row_check.decision_span_problems |
| 23 | (b) G13 stamp via StampHook; hit drops whole group, spec retired, never re-worded (s2, GV5) | IMPLEMENTED | build_checked.flush drops group; replacement = new index = new seed; RefusingHook default |
| 24 | (c) manifest stamp (row id, registry sha, method-set, generator sha, template hash, verdict) (s2) | IMPLEMENTED | `r["stamp"]` in flush; registry_sha check in production |
| 25 | Pilot through the wrapper; G3 one combined fix; CT-G3-one-fix (s2, s10, s12) | MISSING | No pilot/fix controller anywhere in GEN |
| 26 | Fix trigger >1% G13 drops excl. exempt/OHS-5; collisions <=5% of a sub-block not the fix, >5% is (G-W2) | PARTIAL | Summary.as_dict fix_trigger_g13 (row_check.py:266) with collateral. Missing: per-sub-block collision counter/5% rule; rate over all refill rounds; freeze_collision hits kept as clean |
| 27 | A-vs-B disagreement <=1.0%, parse-back drop <=2% per sub-block (G-A1/G-A2) | IMPLEMENTED | gates.gate_a1_agreement (.01), gate_a2_parseback (.02); summary is pooled, per-block rates derived from the drop log |
| 28 | Set-level gates once: G-A4/A5, G-S1..S6 with bars, confirm rule, wording >=50 and <=2% (s2, s8) | IMPLEMENTED | gates.run_all; probes.bars verified (k-way +3/+6 pp, AUC .55/.60); five old blocks only, G-S3 iterates FORMS only |
| 29 | Final mix = one confirming pass, GEN adds nothing (s2) | N/A | L-0 |
| 30 | A1 metadata per row: template_id, operator_ids, wording_id, error_model_ids, level, length_tier (s2, s7) | PARTIAL | builder._make_row:309-311 fills first four; level and length_tier None; held-out flag absent |
| 31 | Template hash export current at every change; stamped rows' template hash current (G-W3) | PARTIAL | gen_hash_export.py + HASH_EXPORT.json CURRENT; build_checked refuses on global mismatch. No per-template currency check; export hashes the stale sizes |
| 32 | G-W1 stamp coverage: 0 pool rows without current clean stamp (CPU test) (s8) | MISSING | no coverage-test function in gates.py or tests |
| 33 | TP-DM 600 (DeepMind Mathematics regenerated from code, <=100/module, 1 module held out) (s3) | MISSING | No generator/adapter/solver B (solver_b has arith/causal/logic/table/temporal only) |
| 34 | TP-RG 1,000: >=8 tasks, >=4 categories, <=150/task, excl. gsm_symbolic/codeio (s3) | MISSING | none |
| 35 | TP-BA 400: >=5 tasks, <=100/task, Lua offline else rolls alone (s3) | MISSING | none |
| 36 | TP admission: licence + A61(b), S-pre/S-post 8.5 per generator on fixed seeded 2,000-instance sample, once per stage (GEN-B3, G-T1) | MISSING | no sampler, S-pre/S-post, fixtures |
| 37 | TP distractors from own error models, each wrong option rejected by the task's check (G-T2) | MISSING | none |
| 38 | TP names: no exemption (GEN-B4); NS-TRAIN replacement of generator name lists | PARTIAL | No exemption path exists (GenAllow closed); NS-TRAIN replacement not built |
| 39 | TP fresh TRAINING-salt seeds; published test instances dropped; offline; pinned release sha | MISSING | none |
| 40 | TP held-out dev: DM 1 module, RG 2 tasks, bAbI 1 task, tag TP-HELDOUT-DEV; 30 dev rows each | MISSING | none |
| 41 | G-T3 TP shape; <8 admissible RG tasks -> TP-RG rolls alone, rows back to original sub-blocks within +25% (GEN-B4) | MISSING | no gate, no roll/redistribution logic |
| 42 | TP rows not voice-eligible (s3) | N/A | voice flag limited to AR-F1/F2, TM-T1/T2 (builder.VOICE_ELIGIBLE_FORMS); no TP rows exist |
| 43 | HX-E 300 (3 labels, one-edit flips, claim and fact pairs >=60%) (s4) | MISSING | no generator/evaluator/edit code; only wording keys in pools/hx_forms.json |
| 44 | HX-U 200 (passage + removed fact, fixed "does not say" text, 30% gold) | MISSING | none |
| 45 | HX-S 200 (6-12 numbered facts, 4-sentence summary with 1 mutated fact) | MISSING | none |
| 46 | HX-T 150 (80 LOGIC + 70 TABLE traces, 4-8 steps, 1 injected error) | MISSING | none |
| 47 | HX-O 150 (select-all as yes/no 90, ordinal bucket 60) | MISSING | none |
| 48 | HX-D 100 (1-3 nonce operators from NS-TRAIN, exact arithmetic) | MISSING | none |
| 49 | G-X1 (edit applied by program, label = edit-rule label, 100%) and G-X2 probe bars (s4, s8) | MISSING | no gate/probe for HX |
| 50 | HX wording pools >=50 per form, none >2% (s4) | PARTIAL | pools/hx_forms.json 7 keys x 56 and hashed; keys not in gen_common.POOL_SPEC, not loaded by pool_loader, not checked by check_pool |
| 51 | HX_EDIT_TYPES and fixed option texts NOT-STATED / DOES-NOT-SAY (s11) | MISSING | names exist only in NAMES_MANIFEST_V1_1/V1_2 |
| 52 | NOTA-GENERIC built but OUT of the mix (s4, GEN-B2, CT-A-nota-out) | MISSING | listed UNBUILT (gen_hash_export.py:39); "out of the mix" holds trivially, "built" half absent |
| 53 | Task-defined classes in the mix: LG-L1 "Undetermined" 33.3% +-5 pp (GEN-B2) | IMPLEMENTED | gen_common.OPTION_TEXTS["LG-L1"]; gates.gate_a4 L1_THIRD_PP .05 (HX-E / HX-U halves = items 43-44) |
| 54 | Carriers reuse TXT-PROSE/BULLET/NUMBERED/TIMELINE/LEDGER, no new carrier (s4, s11) | IMPLEMENTED | gen_common.TEXT_CARRIERS, TABLE_CARRIERS |
| 55 | P-7 abstain-like share report (s8) | N/A | post-training report |
| 56 | Difficulty ladder L1-L4 as program parameter per sub-block mechanism, stored as `level` (s5) | PARTIAL | Only 3 bins easy/mid/hard (arith.BIN_STEPS, logic.bin_of_rules, tables.BIN_DIMS) with different parameters than s5; UNBUILT lists the ladder |
| 57 | Ladder shares per sub-block: L1 <=25%, L2 ~45-50%, L3+L4 25-30%; trap <=35% (G-D1b) (s5, s8) | PARTIAL | BIN_SHARE_TARGET .20/.55/.25 (L2 55% > 45-50%); gates EASY_MAX .25 / HARD_MAX .30 are upper bounds only (no >=25% hard floor); trap <=35% enforced. CONTRADICTS the ruling's 25-30% L3+L4 band |
| 58 | Each hard cell has an easy-looking twin with opposite label at the same level (s5) | PARTIAL | pairs exist (pair_problems) but same-level not asserted |
| 59 | G-D2b: C2 <=70% on L4 rows (pooled ~100 pilot rows); miss fixed by raising parameter (GEN-B5) | MISSING | no L4 tagging, pooled-L4 report or parameter-raising path |
| 60 | TP/HX level tables fixed and hashed with the allow-list before the pilot (s5) | MISSING | none |
| 61 | Length tiers LT1-LT4 per row, shares 30/30/30/10 +-3 pp per sub-block (G-L1) (s6) | MISSING | length_tier None; only tokens_est and mean/>1024 gates |
| 62 | PAD-INERT in-world padding, label-independent, shared by pair members (s6) | MISSING | UNBUILT list |
| 63 | Probes G-S4 and G-S5 also per tier (s6) | MISSING | gates.gate_s4/s5 per form only |
| 64 | A21 gap-rule histogram (5 bins, >5 pp, p90 +20%; tighten never loosen) (s6, GEN-B5) | N/A | L-0 CPU histogram |
| 65 | A2 AFLite-style repair inside the ONE fix: probes under bars, filtered <=30%, counts as the fix (s7) | PARTIAL | adversary.py is an always-on generation-time AFLite-style filter; no post-hoc repair mode with 30% cap or fix bookkeeping |
| 66 | A3-A17 row types: A10/A11/A12/A14/A15/A16 not applicable; A17 not adopted (s7) | N/A | nothing required |
| 67 | G-W4 pair integrity: never singleton, pair share >=30% per sub-block (s8) | IMPLEMENTED | pair_problems + gate_a5_shape, generic over `sub_block` (five old blocks) |
| 68 | G-C1: signed ruling-to-code conformance record before the wrapper accepts GEN rows (s8, s10) | PARTIAL | build_checked refuses production without conformance_ok(generator_sha) (ConformanceRecordRequired); no record/map/sign-off file exists in the tree |
| 69 | s10 conformance tests CT-G1..CT-A-* | PARTIAL | No CT-* ids; equivalents exist (no-network, A=B, parse, pair, 1536, spans, planted leak, C1, OHS3-skip). Missing: CT-G3-one-fix, CT-R4-dev-not-in-mix, CT-R6, CT-A-pad/ladder/TP-admit/HX-edit/nota-out |
| 70 | Names: manifest v1.1/v1.2 carry the GEN v3.2 names (s11) | PARTIAL | gen_common.DEFAULT_MANIFEST = NAMES_MANIFEST_V1.json (:31); GenAllow requires gen_form_ids == the 20 FORMS so HX/TP forms would be refused. V1_1/V1_2 contain the names but are only hashed, never loaded |
| 71 | Kill rule: sub-blocks independent; failing block rolls to C2.2/C3 with numbers; no back-fill above +25% (s12) | PARTIAL | cells built independently; no roll/logging/back-fill logic |
| 72 | Money shed: scale every kept form by 5/7, whole pairs dropped together (s12) | MISSING | none (conditional) |
| 73 | P-8 TP vs Claude-authored dev accuracy (s8) | MISSING | needs TP dev rows (item 40) |
| 74 | GV9: held-out dev rows tagged heldout_family / split.dev_only; mix guard excludes them | PARTIAL | rows carry split="dev" only; no heldout_family/dev_only tag, no TP held-out flag, no mix guard/CT-R4 in GEN |
| 75 | Binding C1: CA-C4/CA-C5 independent random exogenous inputs, no fixed values | IMPLEMENTED | causal.py:806 pool key "ca.indep"; test_gen_core.py:328 |
| 76 | Ruling 6: GEN voice source <=5%; AR-F1/F2, TM-T1/T2 stems <=60 words, no table | IMPLEMENTED | builder voice flag; VOICE/vcommon.GEN_SOURCE_CAP .05. No CT-R6 test |
| 77 | GEN-B6: RG allow-list, DM module list, bAbI task list names-only, due Fri 23 12:00 (manifest v1.2) | MISSING | not yet due (today Sun 18) |

Contradictions with Opus rulings: (1) GEN-B1 sizes in `gen_common.FORMS` / `SUB_BLOCK_TARGETS` (items 1-6); HASH_EXPORT is CURRENT but hashes these stale constants. (2) DEV split 120 x 5 vs 90/90/80/80/80 + TP 90 + HX 90. (3) G-D1b: gates cap hard at <=30% but have no 25% floor; `BIN_SHARE_TARGET` L2 55% above 45-50%. Softer: fix-trigger pools refill rounds; 501-row batch possible; freeze_collision-exempt hits kept; adversary.py always on with no 30% cap; GenAllow loads manifest V1. Not found: names exemption for TP, NOTA-GENERIC in the mix, same-skeleton regeneration after G13, loosened bars.
Dry run uses addendum sizes? NO. `dryrun.py` builds 1 example per each of the 20 old FORMS (n_per_form=1, pair_prob=0.0, test pool); it never reads SUB_BLOCK_TARGETS or dev counts.
Tests: 112/112 pass (two halves; one run is cut by the 2-min limit); `gen_hash_export.py --check` prints CURRENT (stale sizes). No test covers TP/HX/ladder/tier/pad.

## T41c (lane L-I) - code: c21_fam/T41c/t41c; solver_b/ exists (not read)

Verdict: check-at-generation path, G0-lite label table, K1-K5/K8/K9/K12 and GV5 retirement are in code; NONE of A10, A12, A14, A16, ladder/quad, twins or K13-K19. Held-out wrapper draw contradicts GV2. 196 of 360 required generator cells have no wordings (HASH_EXPORT pool_coverage) and the directive/cue pools are not generator-shaped, so no production row can be built yet.

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | N = 2,000 vs 3,000 (s0, Q9) | IMPLEMENTED | planner.py:726 plan_specs(N), :103 bucket_counts; tests at both sizes. N not recorded in HASH_EXPORT (orchestrator item) |
| 2 | Stamp stage 1: schema + anchor faithfulness K9 (s1.1.1) | IMPLEMENTED | rowcheck.py:308 RowChecker.check_rendered |
| 3 | Stage 2: solver A == program solver B per row, drop and log (s1.1.2) | IMPLEMENTED | rowcheck.check_rendered: solve_b; AB_DISAGREE / B_ERROR / B_ANOMALY |
| 4 | Stage 3: facts-absent decidability + pair-group integrity (s1.1.3) | IMPLEMENTED | FACTS_ABSENT_UNDECIDABLE; build.build_rows_checked drops every group member |
| 5 | Stage 3 new invariants: A12 survival, A16 label-preserving, A10 cue-source, A14 layout, quad integrity | MISSING | no code (grep pert, survival, inverse, cue, lay., obs., quad: none) |
| 6 | Stage 4: names allow-list, G8 hosts/raw-IP, G6 cap, PII, G10 export (s1.1.4) | IMPLEMENTED | export.names_checker (NAMES_MANIFEST_V1_1); names.RAW_IP_POOL; rowcheck.py:45 TOKEN_CAP=1536; pii_problems; export.decision_spans |
| 7 | Stage 5: G13 stamp service against every target and method (s1.1.5) | PARTIAL | only a seam: rowcheck G13Hook/G13Result/MissingG13/TestOnlyG13; interface differs from L-0b StampHook (no family/generator_sha sent, no "error" verdict, no "freeze_collision" exemption kind); adapter needed |
| 8 | Stage 6: manifest stamp {row id, registry sha, method-set, code sha, template hash, verdict} (s1.1.6) | PARTIAL | stamp_batch emits all six; but RowChecker.template_hash omits solver_b/verbs.py, pools/*.json, lexicon and held-out draw (build_export().template_hash includes them) |
| 9 | No unstamped or failed row enters pool/mix (s1.1, s1.2) | IMPLEMENTED | RowChecker.__init__ production guards; build_rows_checked returns accepted rows with stamps |
| 10 | K10 and 200-row pilot removed (s1.2) | IMPLEMENTED | no K10 code; stale comment only at pkg/gates.py:5 |
| 11 | Quotas after drops (a): non-G13 drop regenerated on SAME skeleton, fresh wording seed, <=2 attempts (s1.3) | IMPLEMENTED | build.build_rows_checked max_attempts=3, wording_salt; tests for salt |
| 12 | GV5: G13 hit retires skeleton and WHOLE group, never re-worded; first-pass triggers count collateral (s1.3) | IMPLEMENTED | build.py flush(): unaccepted verdict -> retired group, no salt retry; test_g13_hit_retires_the_whole_group_and_is_never_reworded |
| 13 | Quotas (b): oversample every cell >=10% and draw a NEW skeleton per retired/dropped group (s1.3, GV5) | MISSING | no oversample parameter in planner, no refill loop; cells fall below quota (K4 +-1.5 pp at risk) |
| 14 | Fix-trigger lines: G13 >1%, A/B <=2%, anchor <=3%, guard <=2%, facts-absent <=3% on first-pass drops (s1.4) | IMPLEMENTED | rowcheck.py:47 TRIGGERS; trigger_lines:418 from attempt-0 drops only |
| 15 | OHS-5 collisions dropped row by row, <=5%, not a fix iteration; R6 scaffolding exempt (s1.4) | PARTIAL | R6 exempt done (exempt_scaffold); an OHS-5 collision cannot be distinguished: counts toward the 1% trigger and retires the group; no separate 5% bar. CONTRADICTS s1.4 |
| 16 | New trigger lines: A12 survival <=10%, A16 <=5%, A10 cue-source 0, A14 layout <=5% (s1.4) | MISSING | TRIGGERS has no such keys |
| 17 | Set-level checks once per family: K1-K9, K11-K12 (s1.5) | IMPLEMENTED | report.run_prefreeze K1,K2,K3,K4,K5,K8,K9,K12 (+K6ii); K7 in gates._validity; K13-K19 missing (below) |
| 18 | Mix needs a clean stamp for the final registry sha; replay clean-up (s1.6) | N/A | L-0b |
| 19 | GV9: dev rows tagged heldout_family / split.dev_only; mix guard excludes them | PARTIAL | only Spec.block (train/ho/bd/ls); no tags, no exclusion test |
| 20 | GV12 two-way slot round trip (b) nothing added | PARTIAL | (a) anchors verbatim done (solver_a.check_rendered); (b) no scan of slot/wrapper text for added value/negation/qualifier/target/lexicon word |
| 21 | A13 lexicon: 120-200 stems, frozen with template hash, HIT = stem in focus directive sentence (s2.1) | PARTIAL | pools/lex_attack_register_v1.json 136 stems, hash-exported; pool_check.lexicon_hits pool-level only; no per-row hit flag; word.benign_worded / word.alarm_register not in ids.py or Spec |
| 22 | A13 shares: 50% benign-worded among agent-directed attack (25% of N), 50% alarm-register among agent-directed benign (13% of N), each goal class 35-65%, >=70% hit in trigger subtype (s2.2) | MISSING | no planner draw/quota; pools not consumable (pool_coverage only class-level; HIGH 491/569 mappable, 114 no slot); no men.* pool |
| 23 | K13 (a) hit-rate diff <=5 pp (b) payload BoW AUC <=0.55 / bound <=0.60 (c) view (d) planted-stem power >=0.80 (s2.3) | MISSING | no K13; pool-side bow_auc_all 0.993 vs bar 0.55 predicts a K13(b) FAIL (kill gate) |
| 24 | P9 report line (s2.4) | MISSING | needs row tags; none exist |
| 25 | A10 Fri-23 rule GV1 (>=10 of 200 flips; none by 18:00 = not built; toggles sampling only) (s3.1, B5) | MISSING | no sampling toggle/A10 code; no wrong threshold either |
| 26 | A10: 11 base styles (+3), 5 cue families, cue wording pool (s3.2, Q2/B2) | PARTIAL | pools/cue_wrappers_v1.json 453 frames over 9 styles, hash-exported; ids.py:107 WRAPPERS still the 8 G0-lite styles; frames use {directive} but pools.cell_names() wants {core} cells - not consumable |
| 27 | A10 pair design: 5% wrapped + 5% twin (200/300 rows), cue only in carrier-tag spans (s3.2) | MISSING | no code |
| 28 | MUST-FIX GV2: held-out wrapper = cue.persona (role_play + benign_justification), fixed not drawn (s3.2, s15) | MISSING | planner.py:90 draw_heldout is the old seeded 2-of-8 draw (verified: returns wrap.preauthorised_disguise + wrap.urgency); holds out two styles GV2 says must be TRAINED. CONTRADICTS GV2; HASH_EXPORT.heldout_draw.sha256 pins it; test only asserts "2 wrappers" |
| 29 | K16 (a)-(e) cue gates; P10 (s3.3-3.4) | MISSING | no code |
| 30 | A12 design: 10% rows +-2 pp per label, 5 trained families, protected spans, zero_width = U+200B only (s4.1, GV6) | MISSING | no perturbation code (hid.zero_width in render.apply_hidden is an attack wrapper, not A12) |
| 31 | A12 shared library with canonical pert.* ids; held-out fullwidth/bidi/upside_down fixed (s4.2, Q8, GV6) | MISSING | no pert.* in code (klevers.py has it, not imported) |
| 32 | K17 survival / flag probe / held-out absent / family shares; P11 (s4.3-4.4) | MISSING | no code |
| 33 | A14 Fri-23 probe rule GV3 + toggle (s5.1) | MISSING | no toggle |
| 34 | A14 design: 5% slice, 1,000-1,500 tokens, 5 layouts, 3 fillers, 1 held-out layout, carrier mix 50/30/15/5 (s5.2-5.3, GV4) | MISSING | no lay.*/fill.*; artifacts.py:20 LEN_TARGETS has 3 buckets (641-780 top before 1500-3000), so a 750-1,250 carrier is unreachable; G6 cap itself is done (rowcheck.TOKEN_CAP, gates.gate_k8) |
| 35 | K18 and P12 (s5.4-5.5) | MISSING | no code |
| 36 | A16: 7 observation operators on 40% of the 4 tool-output carriers (~13% of N), one held-out operator drawn (s6.1-6.2) | MISSING | no obs.* code (carrier types exist) |
| 37 | K19 inverse normaliser + operator probe; P13 (s6.3-6.4) | MISSING | no code |
| 38 | A6 wording pool: 5 placement kinds x 2 sub-pools, >=80 per cell, 800 total (s7.1-7.2) | IMPLEMENTED | pools/a6_gate_directed_v1.json 10 cells x 80 = 800, hash-exported (data only) |
| 39 | A6 pool gates PG1-PG4 (s7.3) | PARTIAL | PG1: G13 stamp not run on the pool (status PRE-STAMP); PG2 holds by construction, no gate fn; PG3 slot syntax only; PG4 80/cell met, no <=2% gate |
| 40 | Difficulty ladder: 6 mechanisms x L1-L4, one primary per row, others capped at L2 (s8.1-8.2) | MISSING | no mech.*/level/genre code |
| 41 | K14 composition: L3-L4 >=25% of N, L4 >=10%, easy twin >=90%, quad groups >=100/150 (s8.3) | MISSING | no code |
| 42 | K15 measured L4 bar (4-way <=70%), fix raises the program parameter; P14 (s8.4, Q5/B4) | MISSING | no ladder parameter to raise |
| 43 | Twin generator: tuple interface, 3 Aya + 3 Gandalf kinds, 4-gram overlap <=20%, TRAINING-salt names (s9.1-9.2) | MISSING | no twin code (POOL_MANIFEST lists it as not written) |
| 44 | TW1-TW6 twin gates (s9.3, Q7/B4) | MISSING | no code |
| 45 | A1 template_id on every row (s10.1) | PARTIAL | Rendered.meta["wording"] has pool-entry ids; no `template_id` field in Spec/Rendered/stamp |
| 46 | A2 AFLite fix knob (s10.2) | N/A | L-0 tool |
| 47 | A15 `dialect = fmt.*` manifest field (s10.3, Q4, GV7) | MISSING | no `dialect` field (no dialect rendering - correct per GV7) |
| 48 | A24 held-out values: 1 cue family, 2 goals, 1 format, 1 placement, 3 pert, 1 operator, 1 layout (s10.4) | PARTIAL | goals/format/placement done and training excludes them; wrapper pair wrong (item 28); pert, obs, layout absent |
| 49 | HO block 480 -> 780 (>=80 per original value, >=60 per new value, one value per row, stamped) (s11) | PARTIAL | plan_heldout(per_value=80) = 480 and tests assert 480 (old size - CONTRADICTS); +60 blocks for 3 pert + 1 obs + 1 layout missing |
| 50 | K3 on the NORMALISED view; per-axis gaps report-only; raw gap published (s11, Q6/B4) | MISSING | gates.py:216 gate_k3 uses raw view as the kill gate. CONTRADICTS Q6 |
| 51 | BD 400 benign dev with the same A12/A16 shares, stamped (s11) | PARTIAL | plan_benign_dev(400) = 100 ALLOW + 300 ALLOW_BENIGN; no A12/A16 shares; not built/stamped in run_prefreeze |
| 52 | LS 150 eval-only at 1.5-3K tokens + A14 layouts incl. held-out layout (s11) | PARTIAL | plan_long_slice(150) len_target=3; but rowcheck TOKEN_CAP 1536 applies to the 'ls' block so LS rows are dropped on the checked path; no layouts. CONTRADICTS |
| 53 | K1/K2/K4 gain layout/long/operator/pert flags, cue family, mechanism/level, 25/13/10/10/5/quad shares (s12.1) | MISSING | gates.k1_features, k2_features, gate_k4 unchanged G0-lite |
| 54 | Facts-absent ONE value 30% in every label, carrier, subtype AND s2-8 cell +-2 pp, exact quotas (s12.1) | PARTIAL | FACTS_ABSENT_SHARE=0.30; gate_k4 checks label/carrier/subtype; assign_strata greedy not exact; s2-8 cells do not exist |
| 55 | K5-K9, K12 unchanged; K6(ii) per-row at creation 98%; K10 replaced (s12.1) | IMPLEMENTED | gates.gate_k5/k8/k9/k12/k6_rows; per-row A/B in rowcheck |
| 56 | Kill rule; K15 and post-training lines never kill (s12.2) | N/A | process rule |
| 57 | Thu-22 hash export v1.1 (all A10 and A14 templates, A6 pool, frozen lexicon) (s12.3, T41c-B5) | PARTIAL | HASH_EXPORT.json self-states "PRE-STAMP ... Not the Thu 22 v1.1 export"; lacks A12/A14/A16/ladder/twin templates; stale (test fails) |
| 58 | s13 C41-01..C41-13 base clauses + s14 rulings R2-T41c-a..e | IMPLEMENTED | table.py rules and O1-O5; planner.py:38 (30%); probe.py:96 97.5th pct; truth.py K6(i); TOKEN_CAP; RAW_IP_POOL; probe.ProbeHarness |
| 59 | C41-14 stamp order, drop-and-log, quota after drops, group regeneration | PARTIAL | order/logging/groups done; quota refill/oversample missing (item 13) |
| 60 | C41-15..C41-21 (lexicon/K13, A10, A12, A14, A16, ladder/quad/L4, twins) | MISSING | see items 21-44 |
| 61 | Signed ruling-to-code conformance record and run-time refusal without it (s12.3, s13) | MISSING | no record/map anywhere; no ConformanceRecordRequired / TemplateHashStale guard in T41c (GEN/stamp_hook.py has both) |
| 62 | G9 spot-check: HARD/SOFT list vs T50 effects-to-label table; edit-as-action rows (s13) | MISSING | no G9 or T50 reference in code or tests |
| 63 | s15 names for manifest v1.1 | PARTIAL | NAMES_MANIFEST_V1_1.json has every s15 id; ids.py has none of the new ids; check_ids_on_manifest covers only the 5 guard categories |
| 64 | GV8 (pooled sub-block probes), GV10, GV11, GV13 | N/A | not applicable to T41c |

Contradictions with Opus rulings: (1) GV2/s3.2/T41c-B2: `planner.draw_heldout` (item 28). (2) s11 HO 480 vs 780 (item 49). (3) Q6: `gate_k3` raw view is the kill gate (item 50). (4) s11 LS: TOKEN_CAP applied to the eval-only block (item 52). (5) s1.4: OHS-5 collision counts toward the 1% trigger (item 15). (6) Stale text: pkg/gates.py:5 "K10 (G13 pilot)"; artifacts.py:20/24 comments say 641-1200 but LEN_TARGETS[2] is (641,780) (deviates from G0-lite D6; A14 carriers unreachable). (7) Design interaction: ladder L4 `mech.tail_placement` needs place.p4, which the current held-out draw withholds from training. Not found: same-skeleton regeneration after a G13 hit, a "95%" bound, old ">= 10" / ">5%, 11" A10 thresholds.
Dry run uses addendum sizes? NO. `pkg/dryrun.py` build_examples(n=20) uses plan_specs(max(40,n*3)) with a test pool; run_prefreeze(N=2000) only at 500 rows in tests; HO still 480; no A10/A12/A14/A16/ladder/twin rows.
Tests: 146 pass / 1 fail (59 s). The failure is `test_hashexport.py::test_committed_export_is_current`: HASH_EXPORT g0_records holds the G0_APPROVALS_v32.md sha c10a6a... but the file is now 6c02a7... (Batch 1b appended); addendum and G0_LITE shas still match. Re-export needed; not a code defect.

## T42c (lane L-C) - code: c21_fam/T42c (flat module layout) + LC_COMMON; solver_b/ exists (not read)

Verdict: 3,000-row builders, solver A, G5 probe harness, check-at-creation boundary and carried G0-lite gates are done; COMPILE2, A10, A16, ladder and the new sizes are not in code (`LC_COMMON/README.md:66`: "Not built yet (v3.2 addenda): T42c COMPILE2 head, A10 wrapper rows, A16 views, difficulty ladders, T57/T56g addendum items 2-5 and the L-R feed contracts").

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | COMPILE2 head: 300 rows (Py 120 / TS 90 / Go 90 / bash 0; YES 150 / NO 150), form T42c-Q-COMPILE2 (>=50 wordings) (s2#1, s3, s4.1) | MISSING | config.py:5 HEADS=("OUT4","EQV2","TFAIL2"); 3 question forms x 60 wordings; no "COMPILE2" string in T42c, LC_COMMON, ROW_SCHEMA.md, HASH_EXPORT |
| 2 | Head sizes OUT4 1,080 / EQV2 810 / TFAIL2 810 (s3, B1 item 1) | MISSING | config.py:6 HEAD_SHARE 0.40/0.30/0.30 (=1,200/900/900); planner.py:156. CONTRADICTS |
| 3 | Per-head language table (OUT4 852/72/60/96, EQV2 and TFAIL2 639/54/45/72, COMPILE2 120/90/90/0) (s3) | MISSING | config.py:11 one global LANG_SHARE 0.72/0.06/0.04/0.09/0.09 for every head (Py ~1,944 vs 2,130; JS/TS 270 vs 180; Go 243 vs 150 on 2,700 exec rows). Caps still hold |
| 4 | K4/K5/K6/K10 denominators = 2,700 exec rows; K11 on 3,000; COMPILE2 trace bin n/a (s3) | N/A | blocked by item 1; gates k4/k10 index meta.trace_bin and would break on a COMPILE2 row |
| 5 | +20% order-invariance copies incl. COMPILE2 reversal (s3) | PARTIAL | build.py: OUT4 permuted_row, EQV2 reversed_row at 0.20; TFAIL2 none (G0-lite); COMPILE2 reversal absent |
| 6 | Reuse <=4 per base module per head, <=6 overall, counting wrapper/view copies (s3, s8) | PARTIAL | gates.py:297 k13b counts all rows incl. copies but set-level only, not at creation |
| 7 | Quotas counted AFTER drops (s3) | IMPLEMENTED | planner.py:295 settle() releases dropped specs; checker.filter runs inside SolverA.run |
| 8 | Every quota cell oversampled by 15% at generation (s3) | MISSING | no 1.15 factor; config.py:37 CANDIDATES_PER_KEPT=1.5 defined and unused |
| 9 | COMPILE2 toolchains and gold: chk_py/ts/go cards, tsc --noEmit, go vet, GO-AN-1..n, manifest = checker name/version/config sha/image id (s4.2) | MISSING | sandbox_iface has no typecheck/tsc/go-vet request builder or CHECK_CARD renderer |
| 10 | COMPILE2 witness: 3 runs identical in status AND error-class set (K18) (s4.2) | MISSING | no code |
| 11 | Python type-checker licence record + K21 + B3 (MPL-2.0 allowed only run unmodified; GPL/LGPL/AGPL/NC/unknown out) (s4.3, T42c-B3) | MISSING | no licence record or allow-list code ("licen" hits: 0) |
| 12 | Licence fallback: 120 Python COMPILE2 rows move to TS 150 / Go 150 (B2) (s4.3) | MISSING | no planner switch |
| 13 | Constructions CT-E1..10, CT-OK-1..6, >=5 classes per language, no class >25% of NO, suppression <=10% of YES, minimal pairs >=50%; K22/K23 (s4.4, s9) | MISSING | no generator, no gates |
| 14 | COMPILE2 solver A vs B in a different invocation form; A=B=spec 100%; K19/K20 (s4.5) | MISSING | no COMPILE2 in B's schema or hash export (count-only grep); generic block rule exists (agreelib 2%) |
| 15 | A10 wrapper rows ~151 (OUT4 54 / EQV2 41 / TFAIL2 41 / COMPILE2 15), W1/W2/W4 trained, answer correct 50%+-5, clean twin, <=1 of A10/A16 per row, CUE_COMMENT, K24 (s5) | MISSING | no wrapper code (no CUE_COMMENT, no W1..W5) |
| 16 | W3 + W5 FIXED held out (GV2); 60 dev rows outside; heldout_family/split.dev_only tagging (GV9) | MISSING | no tags in T42c/LC_COMMON; no seeded-draw code either, so no contradiction |
| 17 | GV1 build rule: build A10 iff >=10 of 200 flips on Fri 23 probe | MISSING | no flag or parameter |
| 18 | A16 source-as-observation views OBS-GUTTER/CRLF/ANSI/WRAP/TAB/BANNER, 5% of each head (~151 rows), one format held out + 30 dev rows, de-render byte-identical, K25 (s6, B1 item 5) | MISSING | no view registry. Latent blocker: LC_COMMON/checked.py format_problems regex flags CR and ESC, so OBS-CRLF/OBS-ANSI rows would be dropped as control_char |
| 19 | Difficulty ladder L1-L4 from mechanism parameters, 20/30/30/20 +-5, L3-L4 >=25% per head, TWIN rule, K26 (s7, B1 item 3) | MISSING | no level field/mechanism parameters (only trace bins and EQV2 hard_no analogues) |
| 20 | K27 measured bar: C2 <=70% on L4 rows of the 1,000-row pilot | N/A | model read by orchestrator; needs item 19 |
| 21 | s8(a) manifest complete (K1) and witness rule per head incl. "2-run witness refused" (CM-05) | PARTIAL | WITNESS_RUNS=3 in requests (sandbox_iface 38,69,95; solver_a 129); completeness/runs>=3 checked only post hoc by gates.k1; RowChecker._answer_checks does not check run count |
| 22 | s8(a) solver A = solver B = spec expectation per row (G1) | IMPLEMENTED | solver_a _fin_* vs spec_expectation; checked.make_checker -> solver_b hook per row |
| 23 | s8(a) OUT4 options distinct, gold unique | IMPLEMENTED | out4.py (seen-set), solver_a._fin_out4 |
| 24 | s8(a) generator lint (K12), names guard (K15), G6 per row, format probe | IMPLEMENTED | solver_a.finalize (lint, provenance); checked._answer_checks (names, tokens > 1536, format_problems); gates.k14 |
| 25 | s8(a) PII scrub | MISSING | LC_COMMON/checked.py has none (tool_engine/row_pipeline.py:159 _PII exists but unused by L-C) |
| 26 | s8(a) exact-duplicate refusal (AST-normalised hash) and reuse ledger AT CREATION (K29) | MISSING | only post-hoc gates.k13 / k13b; RowChecker has no ledger |
| 27 | s8(a) executed-step count from twin run and bin recorded | IMPLEMENTED | solver_a instrument_steps -> manifest steps_final/bin_final; meta trace_bin |
| 28 | s8(a) ladder level, wrapper/view ids and A1 fields on 100% of rows (K30) | PARTIAL | meta has wording_id, form, construction, mutator_op, distractor_kinds; no template id, level, wrapper/view id, no K30 |
| 29 | s8(b)(c) G13 stamp via service in batches <=500; stamp record; drop log; no unstamped row (K28 part) | IMPLEMENTED | LC_COMMON/checked.py RowChecker._stamp, code_sha(), StampServiceRequired; build.py:84 stamps order copies |
| 30 | GV5: G13 hit retires spec and whole pair/group; first-pass triggers incl. collateral | PARTIAL | checked.py:244,252 drops row + pair partner + same base_module and retires; gap: retirement forward-only, so a primary stamped in an earlier call stays if its later copy hits G13 |
| 31 | s8 fix trigger: >1% = ONE combined fix; OHS-5 <=5%; K28 | PARTIAL | RowChecker.summary reports drops incl. collateral; no threshold logic, no K28, no exemption classification; gates.py:337 K16 text still says "200-row G13 pilot" |
| 32 | Yield <80% raises fix-iteration flag (CM-07); G3 parameter-file sha frozen at pilot launch (CM-02) | PARTIAL | gates.py:341 yield_gate FAIL (no flag); generator_sha stamped but no parameter-file sha |
| 33 | AFLite-style repair as the ONE fix tool (A2) | N/A | orchestrator-side |
| 34 | Carried gates K1-K15 | IMPLEMENTED | gates.py run_gates (K1-K15, K13b, yield) |
| 35 | s11 NAMES: runner.python_typecheck/tsc_noemit/go_vet, card.t42c.chk_*, defs_card.t42c.compile2, CHECK_CARD, CUE_COMMENT | PARTIAL | present in NAMES_MANIFEST_V1_1/V1_2; LC_COMMON/paths.py:10 and names_guard pin V1, so COMPILE2/A10 rows fail NAME_NOT_IN_FAMILY_LIST until repinned |
| 36 | s12 G13 targets added (MBPP splits etc.) | N/A | L-0b registry |
| 37 | Template/cue-pool/view-renderer/COMPILE2-wording hash export (16.1 step 6) | MISSING | HASH_EXPORT v1: forms EQV2/OUT4/TFAIL2 only; HEAD_SHARE/LANG_SHARE are the old values; no COMPILE2/CT/W/OBS/ladder tables |
| 38 | s10 MBPP slice contract (LR-code, P1-realism, block R, <=300 rows outside 3,000, T42c-Q-TFAIL2 form, 3 identical runs, A=B, problem-level G13, MUT-01..14; B4/LR-M7) | PARTIAL | LR/mappers/mbpp.py: train split only, cap 300, family LR-code, exec gold via hook, 50% yes, stamp_fn mandatory. Gaps: own regex mutator (no MUT-01..14 ids), two exec calls not three, own form id lr_mbpp_test_fails (not the T42c-Q-TFAIL2 pool), G13 hit drops that row only (siblings stay) |
| 39 | GV7: A15 dialect not carried; renderer `dialect` parameter at default | N/A | nothing to carry |
| 40 | GV9: mix builder excludes heldout_family / split.dev_only rows (CPU test) | MISSING | no tags/test in L-C code (exist in T59/T60/T67/GEN/LK_COMMON) |
| 41 | GV12 two-way slot round trip incl. nothing-added | N/A | no per-row Haiku rewording in L-C (authored pools) |
| 42 | Ruling (b): per-language step counters; 10% agreement on 100 Python programs before any row | IMPLEMENTED | sandbox_iface.step_agreement; solver_a.agreement_*; order not enforced in code |
| 43 | Ruling (e): authored failure markers for Go/bash | IMPLEMENTED | LC_COMMON/codeview.py:88-120 |
| 44 | G5 probe harness | IMPLEMENTED | LC_COMMON/probe.py (C_FIXED, BOOT=2000, perm_tol .03, leak_ok >=.80) |
| 45 | G1 solver B imports stdlib + schema only (CM-01) | N/A | not verified (solver_b not read) |
| 46 | Toolchain pins/image digests appended before first non-Python row | PARTIAL | config.py:60 PINS_PENDING=True; pins "PENDING_L0_IMAGE_RECORD" |
| 47 | Conformance seed T42c-CM-01..16 as named CPU tests | MISSING | 0 "CM-" ids in tests |

Contradictions with Opus rulings / addendum: (1) config.py:6 HEAD_SHARE (no COMPILE2) vs s3/B1 item 1. (2) config.py:11 global LANG_SHARE vs s3 language table. (3) gates.py:337 stale "200-row G13 pilot" text. (4) Latent: checked.py format_problems rejects CRLF/ANSI view rows; names_guard pinned to manifest V1 rejects all new carrier/runner names. No seeded draw of W3/W5, no GitHub issue text, no licence list in code.
Dry run uses addendum sizes? NO. `dryrun.py` dry_rows() = 20 rows over the 3 old forms with C.HEAD_SHARE 0.40/0.30/0.30, SimExecutor, test pool.
Tests: 59 pass (45.6 s); they assert the old HEAD_SHARE/LANG_SHARE shape.

## T51 (lane L-A) - code: c21_fam/T51 + LA_COMMON; solver_b/ exists (not read)

Verdict: still v3.1 code. HASH_EXPORT (created 2026-10-18T16:15:57Z) hashes only v3.1 tables. T51 and T53 are the only families with NO check-at-creation pipeline: stamp/G13 appear only as docstrings (T51/gates.py, LA_COMMON/pilot.py); no `checked.py`; no per-row driver, drop log or replacement loop.

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | Stamp wrapper: every row answer-checked and G13-stamped at creation; K14 -> K14s; stamp record in manifest (s0.1, s8) | MISSING | no stamp call/adapter in T51/ or LA_COMMON/ (StampHook/run_checked exist only in GEN, tool_engine, LP/LK/LC_COMMON) |
| 2 | Per-row answer checks (K1 A=B, K3, K4, K8, K13, K16, spans) with drop and log (s8a, s2) | PARTIAL | checks exist only as set-level functions in gates.py (k1_agreement ... k16_names); generator._render raises GeneratorDefect for an output-only fact in a primary row (crash, not logged drop) |
| 3 | K12 token rule: 1,536 per-row cap, mean <=800, >1,024 on <=10% (s2, GV4) | MISSING | no k12 in T51/gates.py (T50/gates.py:248-258 has one, not used) |
| 4 | PII scrub per row (s8a) | MISSING | none |
| 5 | Drops: failing group dropped whole; replacement is a NEW spec/new seed, <=2 attempts, short cell reported; G13-hit group never re-rendered (s8, GV5) | MISSING | seed = cell idx (generator.group_id "T51-%05d"); no replacement/retire logic |
| 6 | K14s bar: non-exempt drops <=1% on all 1,000 pilot rows and each full-gen day, OHS-5 <=5%, collateral counted (s8, s10) | MISSING | no drop counter or K14s; stale text gates.py:2, LA_COMMON/pilot.py:2 ("200-row G13 pilot") |
| 7 | Redo hash export after changes to edit renderer, consumer templates, A6 pool, wrappers, transforms, dialects (s8) | PARTIAL | LA_COMMON/hash_export.py exists and matches v3.1 code; none of the v3.2 components exist to hash |
| 8 | Sizes unchanged (s3): matrix 1,760 / traj 720 / consent 640 / compaction 380 = 3,500 (1,650/1,000/850), 65/35 views, dev 10%, 1,000-row pilot | IMPLEMENTED | blocks.py plan_stats() = 3500 {ALLOW 1650, ASK 1000, BLOCK 850} and the block splits; canon.assign_split(0.10); pilot.pilot_cells n_rows=1000 |
| 9 | Overlays stratified by label; <=2 overlays per row (T51-B2) | MISSING | no overlay assignment code |
| 10 | A3 edit carrier core: `consumer` attribute, eligible kinds, V1-V5 only, M resolved from edit + consumer record (s4) | MISSING | model.Entity has no consumer field; resolve_M handles only shell calls; spec_v1 only (shared spec_v2 edit renderer absent) |
| 11 | Primary-view rule: edit row primary only if the consumer record is visible; K4 extended (s4) | MISSING | _facts() has no consumer fact |
| 12 | K20 equivalent-effect check + bars (500 rows +-5%, 0 on branch, label shares +-2 pp, consumer visible 100%) (s4, s10) | MISSING | gates.py ends at k17 |
| 13 | Carrier mix file_edit 45% / file_write 40% / apply_patch 15%; apply_patch held out (s4) | MISSING | no such carriers |
| 14 | T51-B1: T51 oracle (not T50 R22-R27) labels T51 edit rows (s13) | N/A | no edit rows yet; model.label is the only labeller |
| 15 | A6 gate-directed injection: 450 rows (225 cue + 225 benign twins), cue type x label +-5 pp, K21 (s5, s10) | MISSING | no free-text field/cue pool/stub/K21 |
| 16 | A10 conditional: 300 rows, GV1 rule, 3 trained wrapper families, GV2 held-out roleplay + benign_justification, K27 (s6, s10) | MISSING | nothing built; no GV1 code anywhere in L-A; nothing contradicts GV1/GV2 either |
| 17 | A12 perturbation: 350 rows, 5 trained + held-out fullwidth/bidi, G10 survival, drop family losing >25%, K22 (s6, GV6) | MISSING | no transforms in L-A; GV6 library is in LK_COMMON/klevers.py but not imported |
| 18 | A15 dialects: 7 (5 trained, XML and CLI help held out), 12-25% each, K23 (s6, s10, GV7) | MISSING | no dialect renderer (card is a dict; no card-text renderer in L-A) |
| 19 | Difficulty ladder L1-L4 per row, >=25% L3-L4 (design 1,050), M1-M4 each populate 4 levels, K24 (s7) | MISSING | no per-row level; `Glob` import in generator.py:12 unused so M3 glob widening is not buildable |
| 20 | Mandatory quad (alarming/calm x risk present/resolved): 100 specs x 4 = 400 rows (s7) | MISSING | the only quad is the v3.1 consent quad (different) |
| 21 | K25 measured bar: C2 or C1 <=70% on L4 rows of the pilot (s7, s10) | MISSING | no L4 tag |
| 22 | A24 held-out 140 rows (wrapper 25 if A10, dialects 35, transforms 30, apply_patch 30, composed ID-format family 20), tag heldout_family, K26, GV9 (s7, s10) | MISSING | no heldout_family tag; model.id_formats has 18 formats with none held out |
| 23 | K5 / K6 also run WITHIN each carrier (shell, edit) (s10) | MISSING | one carrier only |
| 24 | v3.1 set-level gates kept: K9, K10 (>=12 formats, none >12%), K5/K6/K7/K11/K17 (s10) | IMPLEMENTED | gates.py k9_boundary, k10_id_formats, k5_target_string, k6_format, k7_balance, k11_pairs, k17_neighbours |
| 25 | G10 decision_spans with AUTHORITY (scope declarations, boundaries, delegation pointers, consent naming) (s1, s8) | IMPLEMENTED | generator.py register_form roles; render_turns -> spec.decision_spans; test_t51_a64_skeptic |
| 26 | K19 legs (a)+(b) (R2-T51-b mapping) (s1) | IMPLEMENTED | LA_COMMON/g9.py k21a_lanes; test_k21a passes |
| 27 | K19 leg (c): T50 block-G single-E6-effect edit specs mapped to a T51 entity view with an edit-carrier action (s9) | MISSING | g9.k21a_lanes covers only seven infra.* shell intents; T50 has no edit-as-action specs yet |
| 28 | Carried v3.1: R2-T51-a, compaction K/D, K3 identity, SLT-1 lane rule, 6 cards ask_on_soft OFF | IMPLEMENTED | model.py; blocks.build_compaction; k3_contrast; generator.make_card |
| 29 | Names (s11): carriers file_edit, apply_patch; consumer stems; wrapper/transform/dialect names; namespace kinds | PARTIAL | manifest V1_1/V1_2 and c21_infra/namespace.py done; L-A code pinned to NAMES_MANIFEST_V1 (LA_COMMON/__init__.py MANIFEST_PATH, HASH_EXPORT names) whose T51 list lacks file_edit/apply_patch/file_write - the allow-list would refuse them |
| 30 | Row tags: `sub_block` field and `overlay` list on rows (s11) | MISSING | meta carries only block and variant |
| 31 | GV12 two-way slot round trip | PARTIAL | (a) by construction (wording.render_form computes spans from slot offsets); (b) missing: WordingPool.validate checks only slot names/counts, no closed-lexicon scan |
| 32 | GV3 (A14), GV4 (A14 only), GV8, GV13 | N/A | not applicable / permissive for T51 |

Contradictions with Opus rulings: none in logic (no old thresholds, wrong held-out wrapper set, or same-skeleton regeneration exists because none of it is built). Stale text only: LA_COMMON/pilot.py:2, T51/gates.py:2; code pinned to pre-batch-1 NAMES_MANIFEST_V1.
Dry run uses addendum sizes? NO. `dryrun.py` picks 12 cells from blocks.plan() and builds 20 in-memory specs; no overlay rows (edit carrier, A6, dialect, level, held-out tag). The plan it draws from does match the addendum sizes exactly.
Tests: T51 19 pass (~8 s). LA_COMMON: 72 pass / 3 skipped / 1 fail (stale T50 export; T51 and T53 exports current).

## T53 (lane L-A) - code: c21_fam/T53 + LA_COMMON; solver_b/ exists (not read)

Verdict: still v3.1 code; same L-A gap as T51 (no stamp wrapper or per-row driver). Sink withdrawal (T53-M1) is respected.

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | Stamp wrapper: all rows answer-checked and G13-stamped at creation; K18 -> K18s; stamp record (s0.1, s8) | MISSING | no stamp/G13 call in T53/ or LA_COMMON; gates.py:2 still says "K18 (G13 pilot) ... orchestrator's" |
| 2 | Per-row answer checks (K1/K2, K7 A=B verdict and label, K9, K10 per group, K16, K17, K20, spans, PII) with drop and log (s8a, s2) | PARTIAL | set-level fns gates.k1_registered, k2_checksum, k7_agreement, k9_fact_coverage, k10_contrast, k16_not_live, k17_split, k20_names; nothing drops/logs per row or group; finish() does not reject a primary row with an output-only fact (T51 does) |
| 3 | K15 token rule: 1,536 per-row cap, mean <=800, >1,024 on <=10% (s2, GV4) | MISSING | no k15 or estimator in T53/gates.py |
| 4 | Drops: group dropped whole; replacement a NEW spec/new seed, <=2 attempts; G13-hit group never re-worded (s8, GV5) | MISSING | no replacement/retire logic; seed = cell idx |
| 5 | K18s bar: <=1% non-exempt drops on all 1,000 pilot rows and each day; OHS-5 <=5% (s8, s10) | MISSING | no counter |
| 6 | Hash export redo after changes to mutators, cue pool, wrappers, transforms, dialects, head forms (s8) | PARTIAL | machinery exists, export current for v3.1; no v3.2 entries |
| 7 | Sizes unchanged: a 440, b 480, c 360, d 420, e 160, f 140 = 2,000 (958/210/832) (s3) | PARTIAL | plan_stats nominal = 1,996 (d 416): ALLOW 956, ASK 208, BLOCK 832; block d is 4 short (blocks.D_ITEMS single-row ALLOW 113 vs 115, ASK 108 vs 110) and the test tolerates it (>=1995); with FIX-5 oversampling the plan is 2,022 |
| 8 | FIX-5: ASK cells oversampled >=10%; K13 read on the final set (s1, s2, s10) | IMPLEMENTED | blocks.OVERSAMPLE=1.10, OVERSAMPLED_KINDS; gates.k13_balance |
| 9 | Overlays stratified by label so block totals do not move (s3) | MISSING | no overlay code |
| 10 | PHISHING HEAD form: t53_dest_verdict, >=50 wordings, 4 lettered options TRUSTED / LOOKALIKE / TRANSPORT_DEFECT / UNRELATED, letters shuffled (s4, s11) | MISSING | only T53.Q.reason and T53.Q.tier registered (generator.py:36-37); LA_COMMON/heads.py HEADS = {reason, tier} |
| 11 | Head gold = existing normaliser verdict, lookalike over transport, solver B recomputes with different normaliser 100% (s4, K30) | PARTIAL | primitives exist (destination.normalise, destination.verdict, EgressRecord.verdict); no head wrapper; solver B coverage not inspected |
| 12 | Head draw: 300 rows, cap min(300, 25% of specs), exact 75 x 4, same split as primary (s4, K30) | MISSING | no drawer |
| 13 | T53-B1: head drawer stratifies the six K31 string features across classes before K31 | MISSING | none |
| 14 | K30 integrity and K31 probes (4-way balanced accuracy <=28%, ub <=31%); M6 head ladder (s4, s7, s10) | MISSING | gates.py has only k24_heads (reason/tier); probe.kway_probe reusable |
| 15 | G9 head consistency check: head gold and primary label from the same destination record, 100% (s9) | MISSING | none |
| 16 | Sinks WITHDRAWN (T53-M1): no `sink` attribute, rule 6 log/telemetry only, K23 unchanged, K32 withdrawn (s5) | IMPLEMENTED | grep finds no sink/stdout_echo/temp_file/shell_history in T53 or LA_COMMON; engine.r6; truth_table has no sink input |
| 17 | A6 injection: 350 rows (175 + 175; a 100, d 150, e 50, f 50), 4 cue types, K25 (s6, s10) | MISSING | none |
| 18 | A10 conditional: 250 rows (a 80, b 80, c 40, d 50), GV1/GV2, K34 (s6) | MISSING | none; no GV1 rule in code |
| 19 | A12: 250 rows, never touch hostnames/URLs/tokens/paths, K26, GV6 ids (s6) | MISSING | none; klevers.py library not imported |
| 20 | A15 dialects (7; 5 trained, XML and CLI help held out) incl. MCP-schema dialects on mcp_call rows, K27, GV7 (s6) | MISSING | no dialect renderer; McpAction.text() prints only "mcp_call server.tool json" |
| 21 | Ladder L1-L4 per row, >=25% L3-L4 (600 rows), M1-M5 plus M6 on heads, K28 (s7) | MISSING | no level tags; M2 follow-up escalation and M4 indirection chains do not exist |
| 22 | Quad (alarming/calm x risk present/resolved): 100 specs x 4 = 400 rows (s7) | MISSING | existing "quad" is the v3.1 provenance quad (different) |
| 23 | K29 measured bar (C2 <=70% on L4) (s7, s10) | MISSING | no L4 tag |
| 24 | A24 held-out 80 rows (wrappers 15, dialects 25, transforms 20, TOML file_write payload 20), tag heldout_family, K33, GV9 (s7) | MISSING | no tag; payloads are dotenv KEY=value only, so TOML has no base format to hold out from |
| 25 | K22 leg (b'): T50 edit specs that reach R13 mapped to a T53 spec (s9) | MISSING | g9.k21b_egress covers T50 egress/share/publish/git.push only; T50 has no edit actions |
| 26 | Carried SLT-2 conditions R2-T53-a..e (rule 2, totality, tiers, ask_on_soft, exhaustive K23) | IMPLEMENTED | engine.py r2, first_match, r4/r5/r7, finalize; gates.k23_first_match; test_k23 |
| 27 | FIX-3 offline verifiers and K21 no-network test; G8 one TLD list and raw-IP pool; G10 spans with AUTHORITY | IMPLEMENTED | gates.k21_no_network; destination RESERVED/SPECIAL/GENERIC_TLDS; cards.raw_ip; forms T53.U.* |
| 28 | Names (s11): head ids, t53_dest_verdict, fmt.toml, wrapper/transform/dialect names | PARTIAL | NAMES_MANIFEST_V1_2 has them; L-A pinned to V1 whose T53 carriers lack fmt.toml; no form registered |
| 29 | Row tags `head = t53_phishing`, `overlay` lists (s11) | MISSING | none |
| 30 | GV12 two-way round trip | PARTIAL | spans survive by construction; no "nothing added" scan |
| 31 | GV3, GV8, GV13; T53-B3 (heads roll with the family), T53-B4 (A6 shortfall reported, not back-filled) | N/A | policy or depends on missing builds |

Contradictions with Opus rulings: none in logic (sink withdrawal respected; no old thresholds). Minor: block d plan is 4 rows under its nominal 420. Stale text: T53/gates.py:2, LA_COMMON/pilot.py:2; V1 manifest pin.
Dry run uses addendum sizes? NO. `dryrun.py` builds 20 in-memory specs from 12 cells; no head rows, no overlays.
Tests: 27 pass (~6 s).

## T54 (lane L-T) - code: c21_fam/T54 + shared c21_fam/tool_engine; solver_b/ exists (not read)

Verdict: pre-addendum G0-lite build plus the shared check-at-generation pipeline. No Part S lever library exists anywhere for L-T (no A8/A10/A12/A14/A16 code; grep for smell., xform., pert., wrap., obsfmt, layout., lever_tag, ladder, view.long, schema_binds, dev_only, held_out = zero hits in T54/ and tool_engine/). HASH_EXPORT.json is "v1" (2026-10-18T08:57:28Z), `extra` empty.

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | Family stays 4,000; sub-blocks 1000/800/800/500/500/400; body label mixes and pair types unchanged (s0, s2) | IMPLEMENTED | t54_generator.py:27-28 SIZES/TOTAL; ENTRIES; LABEL_MIX; test_plan_sizes_and_label_mixes |
| 2 | Lever slices drawn by substitution from ONE quota table pro rata by label x N-bin; A10/A14 quotas revert to plain rows if not built (s2, V32-3) | MISSING | build_plan has no lever columns/quota table/build toggle |
| 3 | A8 description anatomy: sentence-tagged sent.purpose/params/safety/returns (s3.1) | MISSING | tool_engine/state.py:107 builds `desc` as one string; render.render_tool_line |
| 4 | A8 six operators (purpose_removed, param_docs_dropped, truncated, near_duplicate_tool, boilerplate_prefix, stale_description); pool.t54.boilerplate_prefix >=30 (s3.2) | MISSING | no operator code; pool_manifest.json has 30 forms, none a smell/boilerplate pool |
| 5 | A8 dependency rule: drop-only a8_dep_drop; S4 sent.safety never removable; solver B re-parses the SMELLY render (s3.3, V32-1) | MISSING | no a8_dep_drop; ANSWER_CODES (row_pipeline.py:39-43) lacks it |
| 6 | A8 slice 500 = S1 150 / S2 150 / S3 100 / S4 50 / S5 25 / S6 25 (s2, T54-B3) | MISSING | no constants |
| 7 | card.t54.schema_binds visible line: every stale row and >=50% of other rows; T54-B5 (s3.4, V32-2) | MISSING | t54_wording.CARD_TEXT has only strict_ask, defaults_ok, read_before_write, parallel_ok; id exists only in NAMES_MANIFEST_V1_2 |
| 8 | A12: 300 rows = S1 100 / S3 80 / S4 50 / S5 70; 5 trained transforms; edit budget <=25% chars per word and <=30% words; user turn only (s2, s4, S.4) | MISSING | no transform library; tool_engine/perturb.py `perturb.*` are the S3 deletion ids, unrelated |
| 9 | A12 survival: invert(apply(span))==span, xform_drop by role, spans re-exported with new offsets, drop trigger >20% (S.4, V32-4) | MISSING | render.decision_spans exists but is not wired to any perturbation |
| 10 | A10 (conditional): 200 rows = S1 80 / S3 70 / S4 50; trained wrap.authority/urgency/fake_approval; pools >=20 each; lint; wrapper_spans; clean twin_of; code and pools hash-exported Thu 22 either way (S.3, V32-6) | MISSING | no wrapper pools/lint/spans |
| 11 | GV2: held-out wrappers FIXED = wrap.roleplay + wrap.benign_justification (S.2) | MISSING | no code; no seeded wrapper draw exists, so no contradiction |
| 12 | GV1 A10 build rule (flip = label differs wrapped vs unwrapped, build iff >=10/200) (S.3) | N/A | orchestrator's Fri 23 probe; code side is only the build toggle (item 2) |
| 13 | A14 (conditional): 200 rows = S1 60 / S3 50 / S4 40 / S6 50; layouts, fillers, view.long <=16 turns, ev_pos, lever.a14 tag (S.5, V32-7) | MISSING | no layout/filler/view.long code; only view.primary and view.with_outputs |
| 14 | GV4: G6 binds A14, no exemption; A14 rows 1,100-1,536 tokens inside ">1,024 on <=10%" (S.5, s11.1) | PARTIAL | G6 enforced flat (row_pipeline.py:34 MAX_TOKENS=1536; gates_common.token_gate); the 1,100-1,536 slice build window absent (no A14) |
| 15 | GV3 A14 build rule: gap >=5 pp and paired-bootstrap lower bound >0 (S.5) | N/A | orchestrator probe |
| 16 | A16 re-render of 40% of with-outputs rows (~200 re-rendered, 0 extra rows); default plain_kv 60%; 8 non-default formats 3-8% each; fmt_drop; 256-token cap after formatting; T54-B4 ids (S.6, V32-5) | MISSING | no obsfmt code; `cap_tokens=256` in t54_render._call_text (line 91) is an unused parameter |
| 17 | Difficulty ladder: 9 mechanisms m.t54.* L1-L4, row level = max mechanism, L4 only if >=2 mechanisms at L3+; tags on 100% rows (s3.5, s5, S.7) | MISSING | only N-bin edges coincide with distractor levels; no tags |
| 18 | V32-8: >=25% rows at L3-L4 (each sub-block >=20%), L4 >=8%, twin with opposite label for >=80% of L3-L4 (s6.1, S.7) | MISSING | none |
| 19 | V32-12 C2 accuracy on L4 rows <=70% on the pilot (s6.2) | N/A | model read by orchestrator (depends on item 17) |
| 20 | V32-1 A8 label preservation 100%; >40% dropped = revise (s6.1) | MISSING | not in t54_gates.run_all |
| 21 | V32-2 A8 balance per operator (call-bearing share 40-60%; AUC <=0.55/0.60; S1 4-way <=28%/31%; schema_binds presence) | MISSING | not in t54_gates |
| 22 | V32-3 lever slice sizes +-2 pp; label mix +-5 pp; lever_tag -> label probe | MISSING | not in t54_gates |
| 23 | V32-4 A12 survival 100% of kept rows, drop trigger 20% | MISSING | not in t54_gates |
| 24 | V32-5 A16 label preservation, 0 over 256-token cap, format-id -> label probe, each format 3-8% | MISSING | not in t54_gates |
| 25 | V32-6 A10 wrapper lint 0 violations, 100% clean twin, wrapper-family probe | MISSING | not in t54_gates |
| 26 | V32-7 A14 label preservation, ev_pos probe, length-only probe, budget | MISSING | not in t54_gates |
| 27 | V32-9 / GV9: 160 dev-only held-out rows OUTSIDE the 4,000 (wrapper 40, xform 40, format 40, layout 40), tagged split.dev_only; draw file with seed+sha before any pilot; mix guard test (S.2, s11.2) | MISSING | no tag, dev rows, draw file or mix guard; no C2.1 mix builder in the tree |
| 28 | V32-10 stamp-drop trigger: >1% non-exempt stamp drops = ONE combined fix, read on all pilot rows and each day (s6.1, s7d) | IMPLEMENTED | row_pipeline.py:36 FIX_TRIGGER_RATE=0.01; Summary.as_dict fix_trigger_g13 with collateral (pair_partner_of_hit); denominator includes refill rounds, not strictly first-pass |
| 29 | V32-10 clause: OHS-5 collisions dropped row by row, <=5% of the family | PARTIAL | finish_batch (row_pipeline.py:445) keeps any hit whose entries are all exempt incl. freeze_collision; not dropped, not counted against 5%. Same logic in LP_COMMON/pipeline.py:38,129 |
| 30 | V32-11 hash export v1.1 includes every wrapper/boilerplate/filler pool, layout, transform lib; 0 unexported templates at first row | MISSING | HASH_EXPORT.json version "v1", `extra` empty; t54_hash_export.py code list is 7 base files |
| 31 | R32-1..R32-4 post-training report lines | N/A | post-training |
| 32 | GV8 / s6.4 / s11.5: P-5a..P-5e POOLED across equal-k sub-blocks on the 1,000-row pilot (s6.4) | MISSING | t54_gates p5a/p5b/p5c loop per sub-block only |
| 33 | S.1 row tags: lever_tag, a16, ladder_level, ladder_mechs, split, held_out, pair_id, orphan(bool), twin_of | MISSING | records carry group_id + pair_role; orphan True on orphans only; others absent |
| 34 | GV6 canonical pert.* ids; zero_width = U+200B only; fullwidth/bidi/upside_down held out | MISSING | no perturbation code; no xform.* alias either; manifest v1.2 has pert.* only |
| 35 | GV7 / s11.4: renderer carries a `dialect` parameter at its default | MISSING | grep "dialect" in T54/ and tool_engine/: 0 hits (0 rows affected) |
| 36 | s7(a) answer checks: A=B; B parse of RENDERED text; S2/S6 uniqueness; C1 span pointer; names guard (P-13); output lint (P-14); G6; PII; slot survival; decision_spans | IMPLEMENTED | row_pipeline.check_row (A_recompute_differs, A_B_label_differs, render_fidelity, names_off_allowlist, token_cap, output_lint, slot_lost, pii, decision_spans); t54_checked._s6_unique, _answer_has_span |
| 37 | GV12 two-way slot round trip (a) spans survive (b) none ADDED, via solver-B parse + closed-lexicon scan | PARTIAL | (a) per row via slot_lost; pool-time tool_engine/wording.reword_ok = same slot set, numbers multiset, negation COUNT; (b) beyond numbers/negations absent: no qualifier/delegation/order/consent/target/cue-lexicon scan; pool predates GV12 |
| 38 | s7(b)(c) G13 stamp: single stamp boundary, batches <=500, stamp stored, no default hook, refuse unstamped | IMPLEMENTED | row_pipeline StampHook, RefusingHook, StampServiceRequired, BATCH_ROWS=500, finish_batch writes r["stamp"] |
| 39 | GV5: G13 hit retires spec/skeleton and the WHOLE pair; replacement a new spec with a new seed; never same skeleton | IMPLEMENTED | finish_batch lines 447-457 drops whole group, counts retired_groups; refill line 492 new gid `~rN`; test_a_g13_hit_drops_the_whole_pair... |
| 40 | Pair closure after a NON-G13 drop: partner stays, marked orphan; P-12 on kept rows (s7) | PARTIAL | row_pipeline.py:421-423 sets orphan; but gates_common.pair_integrity (in run_all) requires exactly one a + one b per group so any orphan fails it; pair_share counts orphans as paired |
| 41 | Quota-driven generation: seeds advance until every cell quota filled; drops counted by reason; no back-fill | PARTIAL | refill capped (run_checked max_refill_rounds=2); groups lost after round 3 vanish with no unfilled-cell report |
| 42 | Pilot rows are real rows; after the combined fix, rows from CHANGED template ids are discarded and regenerated | MISSING | rec["template_id"] exists, no discard logic |
| 43 | s7(e) set-level checks once per family incl. ladder + V32-12, G5 harness (P-5a..e, P-6..P-9, V32-2..8) | PARTIAL | t54_gates.run_all covers P-1..P-14 body gates; V32 and ladder gates absent; docstring line 5 stale (P-15) |
| 44 | Stamp wrapper refuses to run without a signed ruling-to-code conformance record for its code sha (s1, S.8, 16.1 step 0) | MISSING | row_pipeline.guard_facts checks only freeze/registry/allow-list pins; no "conformance" check in tool_engine, T54 or c21_infra/row_start_guard.py |
| 45 | Generator code sha in the stamp; any template/engine change = new export + re-stamp (s7c, V32-11) | PARTIAL | t54_checked.adapter code_files = 4 T54 files only; tool_engine/*, t54_gates, t54_checked, solver_b not in the stamped sha |
| 46 | DAG builder exported read-only to L-K: `build_dag(scenario_record)`, module path, code sha, CPU test ids (s8, S.9) | PARTIAL | tool_engine/dag.py exists (T60 imports it, t60_g9.py:150) with CPU tests; no function named build_dag(scenario_record), no export record/notice |
| 47 | G9 hook `t54_label_oracle(record, card) -> label` exported read-only; test [t54_g9_oracle_export] (s8, s1) | PARTIAL | no function of that name; T59 cross-family leg imports T54 generate_in_memory (t59_g9.py leg_a); T54's own gold is t54_solver_a.gold_label(rec); no export test |
| 48 | G10 decision_spans with roles on user turns (s8, s1) | IMPLEMENTED | render.decision_spans, ROLES_G10; t54_render.finalize; check_row; test_g10_decision_spans_roles_offsets_and_authority |
| 49 | T54-B1: T54 cards state "ask when a required value has no source" visibly | IMPLEMENTED | t54_wording CARD_TEXT strict_ask / defaults_ok; every row carries a base card (T59's line is T59's job) |
| 50 | s9 NAMES (T54-specific + shared L-T ids; pert.* not xform.*; T54-B4/B5) | PARTIAL | manifest V1_2 done; code side: tool_engine/names.py MANIFEST_DEFAULT and HASH_EXPORT names point to NAMES_MANIFEST_V1.json; not repinned; no code emits any new id |
| 51 | s1 clauses C1, Rl-1, Rl-4, S1-S6 rule tables, G1, G5 harness, G6, G7 | IMPLEMENTED | t54_solver_a (CALL_BEARING, gold_s1..s6); read_before_write card text; tests; solver_b/ exists |
| 52 | GV13 same-action conformance; T54-B2 (rename ladder ids later = name-only) | N/A | GV13 "Applied" list is T59/T60/T67 only; B2 is a name-only note |

Contradictions with Opus rulings: no old thresholds ("3.0%, 6 of 200"), seeded wrapper draw, or old A14 exemption in code (none of it is built). Behavioural conflicts: item 40 (`pair_integrity` fails any orphan); item 29 (freeze_collision hits kept); item 45 (stamped sha excludes tool_engine/solver_b); item 37 (count-based pool round trip). Stale text: t54_gates.py:5 (P-15 200-row pilot). Seen outside scope: tool_engine/perturb.py:15-24 draws T55's held-out violation types by seed (HELDOUT_SEED).
Dry run uses addendum sizes? NO. `t54_dryrun.py` = generate_in_memory(total<=200, standin=True) from base SIZES only; no lever slices, no dev rows, no tags. The sub-block totals match the addendum.
Tests: 30 pass / 1 fail (12 s). The failure `test_production_mode_is_refused_until_namespace_has_the_noun_kinds` is a stale assertion (c21_infra/namespace.py now has noun_entity/noun_field); side effect: production-mode generation is no longer blocked by names.

## T55 (lane L-T) - code: c21_fam/T55 + shared c21_fam/tool_engine; solver_b/ exists (not read)

Verdict: pre-v3.2 body build. No v3.2 lever exists for L-T (no A7/D6, quad, A10, A12, A14, A16, ladder, lever_tag, split.dev_only, pert.*, obsfmt.*, wrap.*, layout.*). HASH_EXPORT "v1" (2026-10-18T08:57Z) matches current files and names none of the v3.2 items.

| # | Addendum item | Status | Evidence |
|---|---|---|---|
| 1 | s0/s3 LIMBO withdrawn; no LIMBO number in any row, card, pool or bar | IMPLEMENTED | case-insensitive grep: 0 hits for "limbo" in T55, T56, tool_engine incl. pools; no dedicated lint test [t55_no_limbo_numbers_in_pools] |
| 2 | s0/s4 A16 obs-format perturbation: 40% of 2,700 output-bearing rows (~1,080), 0 extra rows, 1 format held out, B normaliser, 256-token cap | MISSING | t55_render only has render.kv_lines (plain_kv); no obsfmt code |
| 3 | s0/s4 A12: 200 rows by substitution (B1 70, B4 60, B3 40, B5 30); survival inverse; held-out families dev-only | MISSING | no transform library/inverse/xform_drop; tool_engine/perturb.py is only the fault/violation manifest |
| 4 | s0/s4 A10 wrappers: up to 150 rows (B1 50, B4 30, B2 40, B3 30); GV1 rule; GV2 roleplay + benign_justification held out; lint; wrapper_spans; pools/code hash-exported Thu 22 either way | MISSING | no wrapper pools/code/build switch |
| 5 | s0/s4 A14 long slice: up to 150 rows (B1 40, B2 20, B3 30, B6 60); view.long, layouts, fillers, B6 history 20-60 calls, ev_pos; GV3; GV4 tokens 1,100-1,536 | MISSING | no view.long/layout/filler code; only MAX_TOKENS=1536 (G6) |
| 6 | s0/s5 Ladder m.t55.* L1-L4; L3-L4 >=25% of family and >=20% each sub-block; L4 >=8%; twin >=80%; tags on 100% rows | MISSING | no ladder/level fields |
| 7 | s7(a) per-row checks: A=B (B1/B3/B4/B5/B6), B2 two-world sim = B replay, B3 invariants, P-10 parse (abstain drops), render fidelity, names, lint, G6, PII, decision_spans | IMPLEMENTED | row_pipeline.check_row (:218); t55_checked.adapter abstain_is_drop=True, _b2_ledger, _lint; sa.b2_label raises on rule/sim mismatch |
| 8 | s7(b)(c) G13 stamp on every row; stamp in manifest; no unstamped row in a pool | IMPLEMENTED | run_checked raises StampServiceRequired (:372); finish_batch attaches r["stamp"] (:458-462). Caveat: generator_sha covers only t55_generator, t55_render, t55_solver_a, t55_wording (t55_checked.py:60) |
| 9 | s7/GV5 G13 hit retires spec and whole pair; new seed; orphans only after non-G13 drops | IMPLEMENTED | finish_batch drops/retires whole group (:447-457); refill `~rN` new RNG stream (:492); orphan flag (:421-423) |
| 10 | s7/V32-8 trigger: >1% non-exempt stamp drops on ALL pilot rows and each day = ONE fix; OHS-5 collisions dropped row by row (<=5%); first-pass incl. collateral | PARTIAL | FIX_TRIGGER_RATE=0.01, fix_trigger_g13 with collateral; (a) all-exempt hits incl. freeze_collision are KEPT (:445, docstring :79); (b) denominator includes refill rounds; (c) per run not per day |
| 11 | s7(a)/GV12 two-way Haiku round trip (P-13) | PARTIAL | wording.reword_ok (:83) slot set, number multiset, negation count; slot_lost (:261); (b) "no decision span ADDED" closed-lexicon scan missing |
| 12 | s2 Sub-block totals B1 900, B4 400, B2 600, B3 500, B5 300, B6 300 = 3,000; label mixes and pairs unchanged | IMPLEMENTED | t55_generator.SIZES (:23), LABEL_MIX; p2_sizes_mix |
| 13 | s2 Lever quota table (A12 200 / A10 150 / A14 150 / 2,500 plain), one lever_tag per row, revert to plain if not built | MISSING | no lever_tag, a16, ladder_level, twin_of, held_out fields (Part S.1) |
| 14 | s2/S.2/GV9 dev-only held-out rows: 120 outside the 3,000 (wrapper 30, transform 30, format 30, layout 30), tagged split.dev_only, mix guard | MISSING | no generator, tag or mix guard |
| 15 | S.2 seeded draws of held-out format (1 of yaml/paginated/ansi/progress_noise) and layout (1 of 5), recorded with seed+sha before any pilot | MISSING | no draw code or ladder file |
| 16 | Rl-5/s2 two held-out VIOLATION types by seeded draw before any pilot; dev-only rows outside the 3,000 | PARTIAL | perturb.py:15-25 HELDOUT_SEED draw = {duplicate_in_unique_list, order_violation}; build_b3 uses TRAIN_TYPES; p3_perturbation_coverage leak check; no dev-only row generator or tag |
| 17 | V32-1 A12 survival (100% restored, drop trigger >20%) | MISSING | no code |
| 18 | V32-2 A16 label preservation, 256-token cap, format-id probe, each format 3-8% | MISSING | no code |
| 19 | V32-3 A10 lint, clean twin, wrapper-family probe | MISSING | no code |
| 20 | V32-4 A14 label preservation, ev_pos and length probes | MISSING | no code |
| 21 | V32-5 lever slices (sizes +-2 pp, label mix +-5 pp, lever_tag probe, 2x2 cells >=8% after substitution) | MISSING | cell check p3_perturbation_coverage exists only on the body |
| 22 | V32-6 ladder gate | MISSING | no code |
| 23 | V32-7 held-out hygiene (0 leaks, mix guard test) | MISSING | no code |
| 24 | V32-9 / S.9 hash export v1.1 incl. wrapper pools, fillers, layouts, format renderers | MISSING | export is v1, `extra` empty |
| 25 | V32-10 / INV lever invariance [t55_rules_ignore_lever_fields] | PARTIAL | rule fns take no lever field (vacuous); no lever-stripped recompute/test |
| 26 | V32-11 structure-only probe extended with format id, wrapper family, transform family, layout, ev_pos, ladder level | MISSING | structural_features (t55_gates.py:229) has only tokens, user_turns, n_tools, gold_letter, wording_id, template_id, view |
| 27 | V32-12 C2 <=70% on L4 rows (pilot, fix trigger) | MISSING | no L4 tags to read |
| 28 | s6.3 R32-1..R32-4 post-training report lines | N/A | need tags that do not exist yet |
| 29 | s6 scope note / GV8 pilot-pooled sub-block probes P-5/6/7 | PARTIAL | p5/p6/p7 run per sub-block (len(rs)>=40); no pooled-by-k variant |
| 30 | s8 Ledger simulator exported read-only to L-K as `tool_engine.ledger` (new_world, commit, lose_ack, read_back, offer_key; module path, API, sha, CPU test ids) | PARTIAL | logic exists as tool_engine/state.py Ledger (:156), effects_after (:181), ambiguous_write_simulated_gold (:207); no `ledger` module/API/export contract; LK_COMMON and T59 do not import it |
| 31 | s8/G10 decision_spans with roles on user turns; wrapper_spans separate | PARTIAL | render.decision_spans, ROLES_G10, t55_render.finalize (:273), check_row (:270); no wrapper_spans; no spans for the `detail` channel (needed for A12) |
| 32 | s9 NAMES (m.t55.*, shared lever names) for manifest v1.1 | IMPLEMENTED | NAMES_MANIFEST_V1_1/V1_2 contain them; no T55 code emits them yet |
| 33 | s7(e) set-level body gates: A50 G6, wording variety, pair share, P-5/6/7/9/19 | IMPLEMENTED | gc.token_gate, wording_gate, pair_share_gate(0.30); p5/p6/p7/p9/p19 in t55_gates.run_all (:385) |
| 34 | C1 B3 first-match order | IMPLEMENTED | t55_solver_a.b3_label (:115); test_c1_b3_order... |
| 35 | C2 B6 first-match order (6 rules) | IMPLEMENTED | b6_label (:176); test_c2_b6_order |
| 36 | C3 exhaustive truth tables B1/B2/B3/B5/B6 (rule table = A = B) | IMPLEMENTED | t55_gates.p4_* (:50-222); solver_b/tests (12 pass) |
| 37 | Rl-3 P-10 observability: per-row drop; pilot drop >2% = fix | PARTIAL | per-row drop render_unobservable exists; no 2% threshold/flag |
| 38 | Rl-4 B5 cards: both published settings present, each card <=25% | IMPLEMENTED | build_plan forces both; p19_b5_thresholds (:359) |
| 39 | G1 solver B independent code with event-sourced replay | IMPLEMENTED | solver_b/ exists (not read) |
| 40 | G3 no pilot tuning; ONE combined fix [t55_fix_log_single_iteration] | MISSING | no fix-log structure/test |
| 41 | G5 one probe harness, permutation and injected-leak sanity | IMPLEMENTED | tool_engine/probe_stub.py; test_probe_wiring_and_power |
| 42 | G6 mean<=800, none >1,536, >1,024 on <=10% | IMPLEMENTED | MAX_TOKENS (row_pipeline.py:34); token_gate (gates_common.py:102) |
| 43 | S.8 stamp wrapper refuses to run without a signed conformance record for its code sha | MISSING | row_start_guard.py / guard_facts check only freeze, registry, allow-list pins |
| 44 | T55-B2 item 8: remove the withdrawn LIMBO sentence from tools_s5.md (L-0/orchestrator task) | MISSING | zed_orch/c21/training_inputs/excerpts/tools_s5.md line 18 still has "56-74% ... 28% to 4%" |
| 45 | Item 7 / GV7: renderers take a `dialect` parameter, default = current | MISSING | no `dialect` parameter in t55_render (trivial) |
| 46 | GV13 same-action conformance with P0 engines | N/A | GV13 lists only T59/T60/T67; no G9 leg in T55 |

Contradictions with Opus rulings: none of the hard kind (no wrong wrapper draw, no same-skeleton regeneration, no old thresholds). Open points: (a) ladder L2 for `m.t55.implicit` names duplicate_in_unique_list and order_violation, which are exactly the code's seeded held-out draw (`perturb.HELDOUT_TYPES`), so L2 would be empty - re-map before building; (b) `perturb.t55_cell` uses a "persistence" reading of the 2x2 cells that differs from G0-lite 3.1 and has no Opus acknowledgement (V32-5 depends on it); (c) LABEL_MIX for B4 folds the body's Y-STOP 10% into ASK (about 20 rows) though the addendum says body mixes unchanged; (d) t55_gates.py docstring still names P-17 (200-row pilot).
Dry run uses addendum sizes? PARTLY. `t55_dryrun.py` (<=200 rows, in-memory, stand-in names) goes through build_plan with SIZES = the addendum sub-block totals; no lever quotas or tags.
Tests: 25 pass / 1 fail (stale NamespaceError assertion; `generate_in_memory(standin=False)` now builds production-name rows with no guard or stamp, nothing written); solver_b/tests 12 pass; tool_engine/tests 89 pass / 1 fail (same).

## T56 (lane L-T, done half) - code: c21_fam/T56 + shared c21_fam/tool_engine; solver_b/ exists (not read)

Verdict: pre-v3.2 body build; D6 sub-block (A7), runsim, quad, all levers and the new sizes are absent; the old sizes are what the gates enforce.

| # | Addendum item | Status | Evidence |
|---|---|---|---|
| 1 | s0/s3 D6 VERIFY-RELEVANCE sub-block (A7): 400 rows / 200 pairs, five output-only faults | MISSING | SUB_BLOCKS has 5 entries (t56_generator.py:25); no d6, no lever.a7 |
| 2 | s2 Sizes D1 650 / D2 300 / D3 250 / D4 250 / D5 150 / D6 400 and reason mixes | MISSING | SIZES = 900/350/250/300/200 (t56_generator.py:26, verified); REASON_MIX (:76) D1 120/165/90/75 vs 87/119/65/54, D2 175 vs 150, D4 75/35/40 vs 63/29/33, D5 100 vs 75. CONTRADICTS |
| 3 | s3.1 `tool_engine.runsim` symbolic run simulator + five faults: f_zero_collected 45, f_filter_excl 45, f_toplevel_only 40, f_exit_masked 40, f_unrelated_tests 30 (DONE twins 200); renderers fmt.selection_list, fmt.listing_nested, prog.tail, op.pipe | MISSING | no runsim module; no D6 fault anywhere in T56 or tool_engine; perturb.FAULT_REASON has the 13 body faults only |
| 4 | s3.1 f_exit_masked: output-only through world property n, identical call, pipe tail window K, fmt.summary_first in 50% of D6 and 25% of other rows | MISSING | no code |
| 5 | s3.2 Gold v3.2 E1-E6 (A on hidden state plus visible window; B on text only) [t56_e1_e6_truth_table] | PARTIAL | t56_solver_a.failing_conditions (:70) has E1, E3, E4, E5; missing E2 (pipe window, summary status), E6 (collected = listed count incl. zero; nested listing), visible-window computation; no E1-E6 truth-table test |
| 6 | T56-M1: hard bin = f_filter_excl, f_toplevel_only, f_exit_masked, f_unrelated_tests (155 D6 rows); f_zero_collected out of the hard bin | MISSING | perturb.HARD_FAULTS (:65) = the 7 body faults; no D6 fault in it (f_zero_collected is absent, so not wrongly inside) |
| 7 | s3.3 `clause.t56.exit_after_pipe` added to `card.t56.evidence_required` (all f_exit_masked pairs, >=50% of other rows) (T56-B2) | MISSING | t56_wording.CARDS["card.t56.evidence_required"] has no such clause or slot |
| 8 | s3.4 / s8 no test-file diff in any row (T56g boundary) | PARTIAL | true by construction; no explicit per-row check |
| 9 | s3.5 ladder tie, s3.6 fix-menu (drop a fault, move its quota inside D6) | MISSING | no code |
| 10 | s4 Quad alarm/calm x risk-present/resolved over D1, D2, D4, D6 (1,600 rows), pool.t56.alarm_decoration, cells 20-30%, twin rule | MISSING | only tw.WARNINGS (5 benign strings, 20% of calls); no cells/pool/resolved-trajectory structure |
| 11 | s5 A12: 200 rows (D1 100, D2 40, D4 40, D5 20) on task statement and claim, identical transform in both pair members | MISSING | no code |
| 12 | s5 A16: ~800 rows (40%) in non-default obsfmt, 1 format held out | MISSING | no code |
| 13 | s5 A10: up to 100 rows (D1 50, D2 20, D4 20, D5 10), same wrapper bytes in task and claim of both pair members; GV1/GV2 | MISSING | no code |
| 14 | s5 A14: up to 100 rows (D1 40, D2 30, D4 30), view.long up to 16 turns, tokens 1,100-1,536 (GV3/GV4), ev_pos | MISSING | no code |
| 15 | s2 Lever quota table and `lever_tag` / D6 = lever.a7 | MISSING | no tags |
| 16 | s2/S.2/GV9 dev-only held-out rows: 80 outside the 2,000 (wrapper 20, transform 20, format 20, layout 20), seeded format/layout draws | MISSING | no code |
| 17 | s6 Ladder m.t56.* L1-L4 (L3-L4 >=25%, >=20% per sub-block, L4 >=8%, twin) | MISSING | no code |
| 18 | V32-1 D6 A/B agreement (E1-E6) | MISSING | no code |
| 19 | V32-2 D6 pair check (claim, task, skeleton byte-identical; output-only difference) | MISSING | body p3_pair_identity/_pair exist; no D6 rule |
| 20 | V32-3 D6 composition and leakage (fault counts, pipe-presence and summary_first probes, clause >=50%) | MISSING | no code |
| 21 | V32-4 P-8 recompute with D6 in the hard bin and on D6 alone | PARTIAL | t56_gates.p8_hard_bin_outputs (:108) has AUC<=0.65 / bound<=0.70 with perturb.HARD_FAULTS; D6 faults and the "D6 alone" read missing |
| 22 | V32-5 quad gate | MISSING | no code |
| 23 | V32-6 A12 survival | MISSING | no code |
| 24 | V32-7 A16 preservation | MISSING | no code |
| 25 | V32-8 A10 gates | MISSING | no code |
| 26 | V32-9 A14 gates | MISSING | no code |
| 27 | V32-10 lever slices and P-4 re-run on tag mix | MISSING | no code |
| 28 | V32-11 ladder gate | MISSING | no code |
| 29 | V32-12 held-out hygiene | MISSING | no code |
| 30 | V32-13 stamp drop trigger (>1% = ONE fix; OHS-5 collisions dropped row by row) | PARTIAL | fix_trigger_g13 exists; exempt/freeze_collision hits kept (row_pipeline.py:445); denominator includes refills |
| 31 | V32-14 hash export v1.1 (D6 fixtures, alarm pool, layouts, renderers, wrapper pools) | MISSING | export v1, `extra` empty |
| 32 | V32-15 structure-only probe extended with format id, layout id, pipe presence, lever tag, wrapper/transform family, ev_pos, alarm score | MISSING | t56_gates.structural_features has tokens, n_calls, n_output_lines, output_chars, stage, wording_id, template_id, gold_letter only |
| 33 | V32-16 C2 <=70% on L4 | MISSING | no L4 tags |
| 34 | s7.3 R32-1..R32-5 post-training report lines (incl. "symbolic gold, no execution check", T56-B4) | N/A | report-time; needs D6 and tags |
| 35 | s7 scope note / GV8 pilot-pooled probes | IMPLEMENTED | P-4 runs pooled plus per sub-block when >=60 rows (p4_claim_only); P-5..P-8 family-wide |
| 36 | s8(a) per-row checks: A=B incl. reason, evidence-sufficiency, pair identity at creation (D5: claim and task only), names, lint, G6, PII | IMPLEMENTED | t56_checked.adapter (compare_reason=True, _sufficiency, _pair); generator asserts pair identity (_generate_group_once :543) |
| 37 | s8 D3 reachability BFS = DFS (P-20) checked per row | PARTIAL | set-level gate p20_reachability (:201) only; generator/check_row do not compare E.reachable with E.reachable_dfs per row (D3's 250 rows) |
| 38 | s8/GV12 two-way reword round trip (counts, rev numbers, targets, predicate names, negations) | PARTIAL | reword_ok + slot_lost; no closed-lexicon added-span scan |
| 39 | s8/G10 decision_spans with roles plus A12 survival; wrapper_spans | PARTIAL | t56_render.finalize (:135) exports spans for the task statement only (no claim spans); no survival check or wrapper_spans |
| 40 | s8(b)(c) G13 stamp and manifest; GV5 | IMPLEMENTED | shared pipeline as T55 #8/#9; head rows also stamped (run_checked :497-523); generator_sha file list narrow (t56_checked.py:68) |
| 41 | s8/Rl-6 G7 head rows: <=25% of specs, outside the 2,000, same split, reason head P-7 kill gate | IMPLEMENTED | build_plan (:142-146); head_rows; p7_reason_head, head_share |
| 42 | s8(e) body set-level gates: wording (>=50 claim wordings, none >2%), per-claim DONE share 40-60%, stage strata 30-37%, token, pair share | IMPLEMENTED | p9_claims, p10_stages, gc.wording_gate, token_gate, pair_share_gate("P-pairs",0.60) in run_all (:220) |
| 43 | Gate disposition: P-2 amended to s2 sizes and mixes | MISSING | p2_sizes_mixes enforces gen.SIZES and REASON_MIX = the old numbers; a conforming family would fail it. CONTRADICTS |
| 44 | Gate disposition: P-12 amended (each of five D6 faults >=5% of D6 CONTINUE rows; hard bin >=40%) | PARTIAL | hard-bin >=40% check exists (p12_fault_coverage); D6 per-fault coverage does not |
| 45 | s9 NAMES (f_*, d6_verify_relevance, fmt.*, m.t56.*, clause.t56.exit_after_pipe, quad.*, pool.t56.alarm_decoration, lever.a7) | IMPLEMENTED | in NAMES_MANIFEST_V1_1/V1_2; no T56 code emits them |
| 46 | Rl-1 A vs B evidence-sufficiency invariant | IMPLEMENTED | sa.evidence_sufficiency (:138); B compared on label, letter, reason in check_row |
| 47 | Rl-2 single-fault generation and fixed precedence | IMPLEMENTED | perturb.PRECEDENCE_D1 (:59), PRECEDENCE_D4 (:61); sa.gold (:104) refuses mixed faults |
| 48 | Rl-3 + T56-B1: D5 the only pair allowed to differ by a verification call; claim byte-identical | IMPLEMENTED | p3_pair_identity and _pair exempt only d5_unverified |
| 49 | Rl-4 P-8 kill gate AUC<=0.65 and bound<=0.70 | IMPLEMENTED | t56_gates.p8_hard_bin_outputs (:108) |
| 50 | Rl-5 D3 execution cross-check only after sandbox sign-off | IMPLEMENTED | execution slice gated off; test_no_generated_code_is_executed_and_no_file_reads |
| 51 | Rl-7 pairs >=60% | IMPLEMENTED | pair_share_gate("P-pairs",...,0.60) |
| 52 | G1 solver B independent code | IMPLEMENTED | solver_b/ exists (6 tests pass; not read) |
| 53 | G3 single combined fix [t56_fix_log_single_iteration] | MISSING | no fix-log structure/test |
| 54 | G5 probe harness sanity | IMPLEMENTED | test_probe_power_planted_claim_leak_and_reason_leak_are_caught |
| 55 | G6 mean<=800, none >1,536, >1,024 on <=10% | IMPLEMENTED | token_gate as P-14; MAX_TOKENS |
| 56 | S.8 conformance-record refusal | MISSING | same as T55 #43 |
| 57 | T56-B2: no new reason class | IMPLEMENTED | perturb.REASONS is still the 8 classes |
| 58 | GV13 same-action conformance | N/A | not listed as applied to T56; nearest overlap D4 stray_change - flag for orchestrator |
| 59 | A15 dialect (GV7, item 9) | N/A | addendum does not require a dialect parameter for T56 |

Contradictions with Opus rulings: (1) `SIZES` / `REASON_MIX` / `p2_sizes_mixes` enforce the old 900/350/250/300/200 (no D6). (2) `card.t56.evidence_required` lacks `clause.t56.exit_after_pipe` (T56-B2). (3) f_zero_collected is outside the hard bin only because it does not exist (T56-M1 trivially unmet, not violated). (4) t56_gates.py docstring still names P-17 (200-row pilot). No wrong held-out draw, no same-skeleton regeneration, no old A14/A10 thresholds.
Dry run uses addendum sizes? NO. `t56_dryrun.py` (<=200 rows, in-memory) runs build_plan with the old SIZES; no D6.
Tests: 38 pass / 1 fail (same stale NamespaceError assertion as T55); solver_b/tests 6 pass.

Shared L-T code findings (T54, T55, T56; fix once in tool_engine/row_pipeline.py): (1) all-exempt stamp hits incl. freeze_collision are kept (:445, :79); (2) stamp generator_sha covers 4-5 family files only; (3) G13 rate denominator includes refill rounds (not first-pass); (4) wording.reword_ok lacks the GV12(b) scan; (5) no conformance-record gate and no 2% P-10 flag; (6) generate_in_memory(standin=False) runs with production noun kinds and no guard.

## T56g (lane L-C) - code: c21_fam/T56g + LC_COMMON + tool_engine/row_pipeline; solver_b/ exists (not read)

Verdict: the check-at-creation spine and the G13 retire rule are in code; almost every v3.2 content change is absent (quad, LEX-ALARM-1, ladder, L4 variants, legit twins, A10 wrappers, A16 VR-FMT). The family code looks like the pre-v3.2 G0-lite build plus the checked.py wiring.

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | A10 wrapper rows: 60 trained (W1, W2, W4 x 20; half HACK, half NO-HACK; from LIB-NORMAL); conditional on Fri 23 probe GV1 (s2.1, s4) | MISSING | no wrapper/CUE_COMMENT code in T56g or LC_COMMON; config.CARRIERS lacks CUE_COMMENT |
| 2 | Wrapper sits in DIFF comment, never in TASK_CARD or INTEGRITY_CARD; equal rate HACK/NO-HACK; clean twin; CM-13 (s4, s12) | MISSING | only rows.comment_text / spec["comment_line"] (neutral/"fixed" pools), no wrappers |
| 3 | W3 and W5 held out (fixed, GV2/T56g-B3); 40 held-out dev rows outside the 1,000; 0 in training (s4) | MISSING | no wrapper code, so no seeded draw exists; nothing contradicts the ruling yet (addendum body still says "seeded draw"; Opus block overrides to fixed) |
| 4 | K19 wrapper gates (s8) | MISSING | gates.py has K1-K15 only |
| 5 | A16 VR-FMT-1..8 on the 250 with-outputs copies; shared parser with T57; one format held out; parse-back 100%; 256-token cap (s5) | MISSING | solver_a._visible_result emits plain "N passed"/"N failed: names" capped at 900 chars; config.OUTPUT_CAP_TOKENS=256 defined, never used; no VR-FMT in T56g, T57, T42c, LC_COMMON or GEN |
| 6 | K20 VR-FMT gates (s8) | MISSING | not in gates.py |
| 7 | Quad Q-AH/Q-CH/Q-AO/Q-CO, 25% each (floor 15, cap 35), cell tag for all rows (s6) | MISSING | no cell code; hacks f2/f7/f8 are alarm-only, honest rows calm-only: lexicon is label-perfect today so K18 would fail |
| 8 | LEX-ALARM-1 fixed by builder and hashed before the pilot (T56g-B1, item 2) | MISSING | no lexicon in code; HASH_EXPORT has 0 hits for LEX/lexicon |
| 9 | Honest alarming cells only through the unchanged label function; special-case value never in V (CPU assertion, else drop); test edits only in unprotected files (s6, T56g-B1 item 4) | PARTIAL | label function unchanged; solver_a.decide/finalize drop honest rows with a signature or protected edit; no alarming-honest builder, no "value never in V" assertion |
| 10 | Legit twins SPEC-SPECIAL, SPEC-TESTEDIT, FIXTURE-FIX (LD-TWIN) (s6) | MISSING | build.honest_cands only uses T57.build_candidates |
| 11 | Ladder L1-L4; mechanisms LD-MSG/SPEC/BREADTH/REACH/TWIN/CONTRA; composition 20/30/30/20 +-5; L3-L4 >=25%; K21 incl. hunk-position probe (s6, s8) | MISSING | no level/mechanism/position-probe code; no level field in rows |
| 12 | L4 hack variants F4-V1, F7-V1, F7-V2, each >=20 rows after drops, inside F4 and F7 (s6, K24) | MISSING | hacks.BUILDERS = {1..8} only |
| 13 | K22 measured bar, C2 <=70% on L4 (s6, s8) | N/A | model read; rows carry no level field to slice by (item 11) |
| 14 | Sizes 1,000 = 600/100/300, HACK/NO-HACK splits, languages, python <=75% (s3) | PARTIAL | config ROW_TYPES, LIB_NORMAL_SPLIT (300/250/50), LIB_CONTRA_SPLIT, NATURAL_SPLIT, LANG_SHARE correct; but build.make_units draws contra with weight {True: 0.10} per library unit = ~70 LIB-CONTRA rows of 700, not 100; no per-slice quota |
| 15 | Extra copies: +25% with-outputs (exactly, CM-11), 10% swapped, reuse <=2 per task per label (s3) | PARTIAL | constants right; make_units uses `rng.random() < WITH_OUTPUTS_COPIES` per spec (stochastic, ~+-14 rows on 250); reuse only set-level (gates.k_reuse) |
| 16 | Every quota cell oversampled by 15%; quotas counted after drops (s3) | PARTIAL | after-drop counting done (build_rows planner.add(s,-1)); no 15% oversample |
| 17 | Every row reaches the pool only through the stamp wrapper; no hook means no rows (s7) | IMPLEMENTED | LC_COMMON/checked.py RowChecker.__init__ raises StampServiceRequired; T56g/checked.run_checked refuses SimExecutor in production; caveat: build_rows(checker=None) still returns unstamped rows, no pool writer (CM-16 not enforced at a writer) |
| 18 | Answer checks: C1 VISIBLE_PASS 2 runs agreeing; HELDOUT_FAIL in fresh container; matcher A; protected path; A=B (K2); library hacks matching no clause and honest rows failing H dropped (K9); per-row K3 scan; LIB-CONTRA C2 assertion (s7a) | IMPLEMENTED | solver_a.row_requests (VISIBLE_RUNS=2), decide, finalize, _leak_scan; task.contra_ok in make_g_tasks; checked.make_checker wires solver B |
| 19 | Tamper self-test passed for the VM batch, recorded in the row manifest (s7a) | MISSING | no manifest field; gates.k3 returns "tamper_self_test: PENDING" |
| 20 | Names guard (no exemption) and G6 token rule per row (s7a) | IMPLEMENTED | LC_COMMON/checked._answer_checks: default_guard().check; tokens.count > MAX_TOKENS (1536); format_problems |
| 21 | PII scrub per row (s7a) | MISSING | no PII code in T56g or LC_COMMON |
| 22 | G10 decision_spans export for TASK_CARD, roles incl. AUTHORITY on protected-path list and SPEC-OVER-TEST clause (s7a, CM-05) | MISSING | rows.build_row emits no spans |
| 23 | Exact-duplicate refusal on AST-normalised hash and reuse ledger at creation (s7a) | PARTIAL | meta.norm_hash recorded; K13/K14b set-level only |
| 24 | Record quad cell, ladder level, wrapper id, VR-FMT id and A1 fields on 100% rows; K25 (s7a, s8) | PARTIAL | present: wording_id, meta.family, manifest.signatures, meta.form, norm_hash; absent: quad, level, wrapper id, VR-FMT id, K25 |
| 25 | G13 stamp: batches <=500, every target/method, registry-sha bound, scaffolding exemption, stamp record, drop log (s7b, s7c) | IMPLEMENTED | RowChecker._stamp; BATCH_ROWS from tool_engine.row_pipeline; registry sha checked in production |
| 26 | GV5: G13 hit retires spec and the whole pair/group; replacement new seed | IMPLEMENTED | RowChecker._stamp drops hit_pairs/hit_bases (stamp_partner_of_hit), self.retired persists; test_a_g13_hit_drops_the_pair_partner. Caveat: quad and wrapper twins must share pair_id/base_module when added |
| 27 | NATURAL slice: Claude authors the pair, executor labels, wrapper stamps; Haiku/Opus K12 read can only DROP (s7a) | PARTIAL | natural.natural_specs goes through SolverA (no author-set label); K12 is a PENDING stub; no reader/drop-only audit code |
| 28 | FIX TRIGGER: >1% non-exempt drops of pilot or any day = ONE combined fix; OHS-5 <=5% (s7) | MISSING | LC_COMMON/checked.RowChecker.summary has no rate/flag (tool_engine and VOICE do) |
| 29 | Answer-check bars: block drop >3% returns the block; kept yield <800 is a fix iteration (s7) | IMPLEMENTED | agreelib.batch_verdict with hook.BLOCK_DROP_LIMIT (value in solver_b, not read); gates.k2 <=0.03; C.YIELD_FLOOR=0.80; K9 DROP_SHARE_MAX=0.10 |
| 30 | Set-level checks once: wording variety (>=50 per form and card form, none >2%), pair share, K4-K15, K17-K24, A50/A49c/G5-H/G3-H/A43(d) (s7) | PARTIAL | K1-K15, lint, yield, k11 pairs >=0.5 exist; gates.k14 max share only for T56g-Q-HACK (key=None for card/clause forms); K17-K25 absent; A50/A49c/... external |
| 31 | AFLite-style repair as the one fix tool (<=30%, must not touch K4 folds) (s7) | MISSING | no AFLite in T56g or LC_COMMON (GEN/adversary.py is for 4-option forms, not wired) |
| 32 | K4 amended: folds {F1,F5},{F2,F6},{F3,F7},{F4,F8}; MEAN of 4 AUCs >=0.70 and none <0.60; ORIENTED AUC floor (T56g-B2) (s8) | IMPLEMENTED | config.FOLDS, K4_MEAN_MIN=0.70, K4_EACH_MIN=0.60; gates.k4 uses probe.auc_score (raw AUC, positive=HACK), not sym_auc; test_k4_rotation_rule... |
| 33 | K4 "CIs reported"; fold balance per language reported (s1) | PARTIAL | only the 97.5% upper bootstrap bound per rotation (ci_hi); no CI of the mean; no per-language fold balance |
| 34 | K5-K8 near-chance bars: max(AUC,1-AUC) <=0.55, upper <=0.60 (s8, T56g-B2) | IMPLEMENTED | probe.binary_probe sym_auc; passes_binary (BIN_AUC_MAX .55, BIN_UPPER_MAX .60); used only here, not for K4 |
| 35 | Natural DEV split: >=100 rows, whole tasks, seeded draw before any pilot, never trained, excluded from K4-K8 folds (s1, K12) | PARTIAL | natural.assign_dev shuffles only if the caller passes rng (default rng=None = input order); nothing outside tests calls it; flag meta.natural_dev; gates.k7/k8 do not exclude dev rows |
| 36 | K16 replaced: the G13 line dropped, no 200-row G13 pilot (s7, s8) | PARTIAL | gates.py:312 pending_pipeline_gates still says "K16 needs 200-row G13 pilot (<=1% hit)" (stale text contradicting s7); no pilot code; test asserts K16 PENDING |
| 37 | K17 quad cells 15-35% with hard-cell twin share; K18 alarm-lexicon probe AUC <=0.55 (s8) | MISSING | not in gates.py |
| 38 | K23 check at creation: 100% stamped plus answer-check record, drops <=1% (OHS-5 <=5%) (s8) | PARTIAL | RowChecker enforces the stamp; no K23 gate/report computes "0 unstamped" or the drop rate |
| 39 | R6, R7, R8 post-training report lines (s8) | N/A | eval side; need quad/level/wrapper/VR-FMT fields that rows do not carry yet |
| 40 | Names (s9): CUE_COMMENT, LEX-ALARM-1, Q-*, W1-5, VR-FMT-1..8, LD-*, L1-4, F4-V1, F7-V1, F7-V2, SPEC-SPECIAL, SPEC-TESTEDIT, FIXTURE-FIX | IMPLEMENTED | in NAMES_MANIFEST_V1_1 and V1_2; per_family_names.T56g carrier list includes CUE_COMMENT |
| 41 | No new G13 targets (s10) | N/A | none |
| 42 | G3 / CM-02: parameter file sha frozen at pilot launch; later change needs the fix-iteration flag (s11, s12) | PARTIAL | checked.code_sha covers every generator file incl. config.py (stamps go stale on any change); no separate parameter-file sha or fix-iteration flag |
| 43 | Conformance tests T56g-CM-01..16 (s12) | MISSING | no CM test ids in T56g/tests (the map is a separate session's job) |
| 44 | A15 not carried (T56g-B3 item 6, GV7) | IMPLEMENTED | no dialect parameter in T56g or LC_COMMON |
| 45 | GV9: held-out dev rows tagged heldout_family / split.dev_only and excluded by the mix builder | PARTIAL | T56g tags only meta.natural_dev (different tag name); wrapper/format dev rows do not exist; no C2.1 mix builder in c21_fam to test |
| 46 | GV12 two-way round trip | N/A | no Haiku rewording of rows in this family |
| 47 | GV1, GV3, GV4, GV6, GV8 | N/A | GV1 covered by item 1; A12, A14, A15 not carried |

Contradictions with Opus rulings: no max(AUC,1-AUC) as the K4 floor (K4 is oriented - OK); no seeded W3/W5 draw (no wrapper code); no old A10 size; no same-skeleton regeneration after a G13 hit. Deviations: `gates.k10` allows family share `PER_FAMILY_MAX_SHARE + 0.05` = up to 20% vs the s6/K24 bar "none above 15% of HACK rows"; `build.make_units` LIB-CONTRA ~70 not 100; hack builders F2/F7/F8 alarm-only and honest builders calm-only (the confound the quad exists to remove); gates.py:312 stale K16 text.
Dry run uses addendum sizes? NO. `dryrun.dry_rows(n=20)` default (tests use 24-160 rows), SimExecutor, test wording pool; no wrappers, quad, ladder, VR-FMT, 600/100/300 or 1,000. HASH_EXPORT.json hashes 1 form, 1 template, 1 seed pool; no LEX-ALARM-1, W1-W5, VR-FMT or quad entries.
Tests: 44 tests, all pass, but one run takes ~3.5 min (over the 2-min limit; first run killed at 120 s after 42 passed; the two slow tests passed in a second run of 98 s).

## T57 (lane L-C) - code: c21_fam/T57 + LC_COMMON + LR mappers; solver_b/ exists (not read)

Verdict: no v3.2-addendum design item is in code. The 3,000-row builders, solver A, G5 probe harness, the check-at-generation boundary and the carried G0-lite gates are done. HASH_EXPORT v1 (2026-10-18T10:52:20Z).

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | A10 wrapper rows ~150 (VERDICT 50 / BEST4 40 / TESTSEL 20 / LOCALISE 40), W1/W2/W4 trained, answer correct 50%+-5, clean twin, CUE_COMMENT, COMMENT_DECOY kept and wrapper comments counted in K8, K18 (s4) | MISSING | no wrapper code; only COMMENT_DECOY exists (build.py:193 decorate, DECOY_SHARE_OF_INCORRECT 0.15, gates.k8) |
| 2 | W3/W5 FIXED held out (GV2), 60 dev rows outside, GV1 build rule, GV9 tags | MISSING | none (0 heldout_family/dev_only hits) |
| 3 | A16 VR-FMT-1..8 on the 650 with-outputs copies, one format held out, parse-back 100%, 256-token cap, shared parser with T56g, K22 (s5) | MISSING | solver_a.py:447-460 _visible_result emits one hard-coded plain format capped by text[:900] chars; config.py:49 OUTPUT_CAP_TOKENS=256 defined, never used |
| 4 | Ladder L1-L4 with mechanisms M-WP, M-NEAR, M-EXTRA, M-LOC, M-TSEL, M-HELP, M-LEAK; 20/30/30/20 +-5; L3-L4 >=25% per head; TWIN; K20; K24 (s6, B1 item 3) | MISSING | no level/mechanism/twin-share code |
| 5 | Wrong-but-passing class mix WP-LOGIC 45 / WP-INCOMPLETE 35 / WP-TYPE 8 / WP-BOUNDARY 7 / WP-OBO 5 (+-5, each >=3%), stored witness per INCORRECT candidate; K19 | MISSING | config.REASON_MIX (PARTIAL/REGRESSION/NOFIX 40/35/25) is a different axis; no WP tags (a witness per candidate does exist in the manifest) |
| 6 | CAND-EXTRA ("does more than the reference") >=8% of INCORRECT candidates, floor 80 rows (s6) | MISSING | task.py:23 CAND_IDS = INVERSE, ALTFIX, HALFSITE, NEARMISS, HELPERSHIFT, NARROWGUARD, WRONGPLACE; no CAND-EXTRA |
| 7 | LEAKAGE tags LK0/LK1/LK2, LK2 <=10% of rows, K9 LOCALISE probe adds "card text names the gold entity" (s6, s11) | MISSING | no tags; gates.k9 LOCALISE features unchanged |
| 8 | LOCALISE 800 = FUNC 480 / FILE 120 / HUNK 200; FILE = 4-file module; HUNK = program-built multi-hunk diff (1 bug hunk + 3 benign from EQ-YES library); executed HUNK rule; K21 (s7) | MISSING | heads.py localise_spec is function-level only; LOCALISE modules are single-file (build.py make_units kind "L", n_files=1); no granularity tag or hunk generator |
| 9 | Head sizes VERDICT 1,000 / BEST4 800 / TESTSEL 400 / LOCALISE 800 (unchanged) (s3) | IMPLEMENTED | config.py:6 HEAD_ROWS; build.py Planner.unit_kind |
| 10 | Language split per head 750/90/80/80, 600/72/64/64, 300/36/32/32, 600/72/64/64 (s3) | PARTIAL | config.py:14 LANG_SPLIT holds exactly these numbers but is unused (only pilot.py has its own list); Planner.lang() draws from LANG_SHARE 0.72/0.06/0.04/0.09/0.09 (README open item 10); ~90 rows shift from Python; caps hold |
| 11 | Extra copies: +20% order-invariance (BEST4/TESTSEL/LOCALISE), reason-head rows from <=25% of INCORRECT specs, outside the 3,000 (s3, G7) | IMPLEMENTED | build.py:485 ORDER_COPIES 0.20; build.py:432 reason_rows 0.25*len(INCORRECT primary); K3 bars |
| 12 | +25% with-outputs copies exactly 25% of VERDICT/BEST4/LOCALISE (CM-10) | PARTIAL | build.py:386 per-spec coin flip `rng.random() < 0.25`, not exact; no gate on the share |
| 13 | Reuse <=4 per module per head, <=8 overall, COUNTED OVER wrapper and variant copies (s3) | PARTIAL | gates.py:285 k_reuse and derive_rows_a room() count primary rows only, excluding twin, with-outputs, order and reason copies. CONTRADICTS addendum |
| 14 | Every quota cell oversampled by 15%, fixed (s3) | MISSING | no oversample factor |
| 15 | Quotas counted after drops | IMPLEMENTED | build.py build_rows add_spec(s,-1) for reserved specs not kept; loop until primary rows >= n_target |
| 16 | L-R LOCALISE realism: ManySStuBs4J 400 + TSSB-3M 400 (outside 3,000; CC-BY-4.0; Sk 25 span probe) (s8) | MISSING | no downloader/mapper in c21_fam/LR |
| 17 | SWE-Gym feed (cap 1,000) with per-REPO licence whitelist (MIT, Apache-2.0, BSD-2, BSD-3, CC0) (s8) | PARTIAL | LR/downloaders/dl_swe_gym.py whitelisted repos only (REPO_LICENCES.json, no ISC); LR/mappers/swe_gym.py (LR-09) builds file-localisation pick-ones, NOT T57r VERDICT/function-LOCALISE rows |
| 18 | SWE-smith procedural feed (cap 1,000; problem_statement barred; GPL/LGPL dropped) (s8, A82 8) | MISSING | no downloader/mapper |
| 19 | T57r slice up to 2,000 rows (VERDICT + function LOCALISE; CORRECT = dataset fix after gold-sanity; INCORRECT = own-mutator edit with failing witness; pairs >=80%; per-repo images; solver B own runner; gates T57r-K1..K10 + R1) (s9) | MISSING | nothing under T57/; LR-09 docstring says these rows "belong to the T57r family on the signed-off sandbox, not here" |
| 20 | T57-B2: no GitHub issue text / problem_statement in any T57r or LR-09/LR-10 row; scan T57r-K7 | PARTIAL | LR side OK (dl_swe_gym.py drops problem_statement and hints_text; mapper uses no issue text); T57r-K7 8-gram scan absent |
| 21 | T57-B3: partial subset of human-patch hunks not used | N/A | no T57r code, nothing contradicts |
| 22 | T57-B4 + s12: T57r a new row-job family id with P1-realism names exemption; CUE_COMMENT; defs_card.t57r.*; runner.repo_image_pytest | PARTIAL | names in NAMES_MANIFEST_V1_1/V1_2; names_guard pinned to V1 (LC_COMMON/paths.py:10) where T57r is not an allowed family |
| 23 | s10(a) gates a/b module-level (T_s, kill share, undecided >25% drops module); gate c differential; gate d A=B=spec; BEST4 exactly one CORRECT; TESTSEL exactly one fails-before/passes-after; LOCALISE rules | IMPLEMENTED | solver_a.py module_gates (:213-254), :280 differential Drop, :387 best4_not_exactly_one_correct, :395 localise_no_failing_test, :403-444 testsel_*; gates k1/k2/k3/k13; solver B per row via checked.py |
| 24 | C1 module-use ledger: TESTSEL module never used by another head/T42c/T56g, AT CREATION; K23; K10 cross-row scan | PARTIAL | by construction (unit kind "T"; modgen.gen_module(seed, lang, FAMILY) family-salted); gates.k10 reports testsel_modules_shared_with_other_heads; no explicit ledger or K23 gate |
| 25 | K10 hidden-suite leak scan on the rendered row | IMPLEMENTED | solver_a.py:412 Drop hidden_test_leak; gates.k10 |
| 26 | s10(a) names guard (closed list, no P1 exemption inside 3,000), G6 per row, lint, format probe | IMPLEMENTED | rows.row_names -> default_guard; checked._answer_checks; solver_a._lint |
| 27 | PII scrub | MISSING | not in LC_COMMON/checked.py |
| 28 | Exact-duplicate refusal and reuse ledger enforced AT CREATION | PARTIAL | reuse enforced at planning (primaries only); exact-dup refusal only post hoc (gates.k14) |
| 29 | Record ladder level, WP tag, LK tag, granularity, wrapper id, VR-FMT id and A1 fields on 100% of rows (K26); A16 parse-back | PARTIAL | meta has wording_id, cands[].kind, bug_op; no template id, no new tags, no K26 |
| 30 | s10(b)(c) G13 stamp wrapper, <=500 batches, stamp record, drop log, no unstamped row in a pool | IMPLEMENTED | same RowChecker (LC_COMMON/checked.py); T57/checked.py; build.py:489 stamps order and reason rows too |
| 31 | GV5 retire spec and whole group on a G13 hit | PARTIAL | as T42c item 30 (base module = task id; forward-only retirement); test_a_g13_hit_retires_the_whole_base_module |
| 32 | Fix trigger (>1% / OHS-5 <=5%) K25; yield <80% | PARTIAL | summary only; gates.py:344 K17 pending text still says "200-row G13 pilot"; yield gate FAIL at 0.80, no flag |
| 33 | AFLite repair as ONE fix tool (A2) | N/A | orchestrator tool |
| 34 | Carried gates K1-K16 (+ K14b reuse, lint, yield) | IMPLEMENTED | gates.py run_gates |
| 35 | New gates K18 (A10), K19 (WP/CAND-EXTRA), K20 (ladder), K21 (granularity), K22 (VR-FMT), K23 (ledger), K24 (L4 bar), K25, K26; R6-R8 | MISSING | none in gates.py (only K17 pending) |
| 36 | s13 G13 targets added (SWE-bench etc.) | N/A | registry side |
| 37 | Hash export covering new wording/cue pools/view renderers/granularity tables | MISSING | T57/HASH_EXPORT.json v1: 8 forms x 60 (480 templates), names pinned to V1; no WP-*, CAND-EXTRA, LK*, FUNC/FILE/HUNK, VR-FMT, W1..W5 |
| 38 | G7 reason head (<=25% of INCORRECT specs, k=3 bars) | IMPLEMENTED | build.reason_rows; config K3_ACC_MAX/K3_UPPER_MAX; gates.k7 |
| 39 | C2 wording fix in the G0-lite (no "Claude-written tests/suites" in gate a and risk 1; CM-07) | MISSING | families/T57/G0_LITE.md still says "Claude-written-test risk" (line 44), "Claude-written hidden suites" (line 213), "Claude-written suites" (line 170) (doc, 0 rows) |
| 40 | Ruling (c): T_s rule (0.90 if >=70% of 50 pilot modules; one recipe revision; floor 0.80; non-Python extension to 20 modules) | IMPLEMENTED | pilot.py (38 Py + 4 JS/TS + 4 Go + 4 bash); solver_a.pilot_threshold/set_threshold; config TS_* |
| 41 | Ruling (d): patches editing test files excluded | IMPLEMENTED | task.py header + candidate construction from module files only |
| 42 | GV7 (A15 only in L-A) | N/A | not carried |
| 43 | GV12 two-way slot round trip | N/A | no per-row Haiku rewording |
| 44 | G5 probe harness | IMPLEMENTED | LC_COMMON/probe.py (shared) |
| 45 | Toolchain pins/digests | PARTIAL | config.py:65 PINS_PENDING=True |
| 46 | Conformance seed T57-CM-01..17 as named tests | MISSING | 0 "CM-" ids in tests |

Contradictions with Opus rulings / addendum: (1) `gates.k_reuse` and `derive_rows_a` count primaries only; s3 says reuse is counted over wrapper and variant copies. (2) LANG_SPLIT unused, LANG_SHARE slack replaces the table (inside the bars). (3) gates.py:344 K17 still names the removed 200-row pilot. (4) G0_LITE.md still carries the "Claude-written" wording C2 orders replaced. (5) OUTPUT_CAP_TOKENS (256 tokens) defined but the visible result is cut at 900 characters. (6) V1 names pin refuses T57r and CUE_COMMENT (latent). No seeded wrapper draw, no GitHub issue text in rows, no partial human-hunk subset, no non-approved licence found.
Dry run uses addendum sizes? PARTLY and trivially. `dryrun.py` builds 20 rows with the unchanged head sizes (HEAD_ROWS drives the planner); no A10/A16/ladder/WP/CAND-EXTRA/granularity.
Tests: 54 pass (115.5 s).

## VOICE (lane L-G) - code: c21_fam/VOICE (vcommon, voice_check, pool, vgates, noiser, span_check, voice_hash_export, dryrun); solver_b/ exists (not read)

Verdict: all of section 3 and the Opus conditions are in code; Generator C (20%, ~600 rows) and its gates V-C12, V-C14, V-C15 are not built; GV5 sibling retirement is missing.

| # | Addendum item (section) | Status | Evidence |
|---|---|---|---|
| 1 | Mix-entry rule: (i) all PK/PK-D gates pass at set level, (ii) Opus confirmation record, (iii) clean twin and current stamps, (iv) voice <=8% of new rows, (v) no human-label or L-R source (s2, VOICE-B4/B5) | PARTIAL | (iii) voice_check.mix_guard; (iv) pool.voice_share_ok, vgates.gate_c8_sizes; (v) check_variant reasons source_human_label/source_lr, gate_c8; no code for (i) or (ii); mix_guard does not check (i), (ii) or (iv) itself |
| 2 | Generator C (VGEN-C): PN-SWAP, HOMOPH-SWAP, BOUNDARY-SHIFT; dictionary-based; corruption rate calibrated by a program loop; ~600 rows (s1, A18) | MISSING | HASH_EXPORT "unbuilt" and voice_hash_export.UNBUILT list VGEN-C; SCHEMA.md s7 "Generator C is not built"; noiser.py has only generator B ops |
| 3 | Dictionary licence list = MIT / Apache / BSD / CC0 / CC BY / CC BY-SA only; NC, ND, GPL, LGPL, unknown not used (VOICE-M1) (s1, V-C11) | IMPLEMENTED | vcommon.DICTIONARY_LICENCES_ALLOWED exact SPDX list (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC0-1.0, CC-BY-4.0, CC-BY-SA-4.0); dictionary_licence_ok requires spdx, quote, url, fetched; test uses CC-BY-NC-4.0 and expects refusal; no unqualified "CC" |
| 4 | V-C11 gate: licence record (quote, URL, fetch date) for the dictionary used, else C is OFF (s1) | PARTIAL | function wired into VariantChecker.c_ok and generator_shares; no gate_c11 entry in vgates; the record itself does not exist (HASH_EXPORT unbuilt lists it) |
| 5 | V-C12 phoneme-key coverage >=98% of eligible tokens (s1) | MISSING | no phoneme key code |
| 6 | V-C13 neighbour validity: 100% of swaps recomputed by checker B's own phoneme edit distance (s1) | PARTIAL | voice_check.check_variant (C branch) only checks recorded swap distance `d <= 1` and flag `swaps_checked_by_B`; trusts the caller; no phoneme edit-distance code |
| 7 | V-C14 band calibration of C on >=1,000 noised variants within +-3 pp of 30/35/25/10/0 (s1) | MISSING | gate_c9_noiser generic; noiser.calibrate is for B |
| 8 | V-C15 swap-class mix within +-10 pp of B's (s1) | MISSING | none |
| 9 | Generator shares A 50 / B 30 / C 20 (+-3 pp); C off gives A 55 / B 45 (VOICE-B3) (s1) | IMPLEMENTED | vcommon.GENERATOR_SHARE (.55/.45), GENERATOR_SHARE_ABC (.50/.30/.20), GENERATOR_TOL .03, generator_shares; test_generator_shares_follow_the_licence_record |
| 10 | V-C8 adds the generator split with C present (s4) | PARTIAL | vgates.gate_c8_sizes takes no `shares` arg; uses the default 55/45 table, so with C ON (50/30/20) it flags A (0.50 vs 0.55) and ignores C. Defect |
| 11 | Strata 75/20/5; bands 30/35/25/10/0; LOCKED 560 ms with forced flush; GEN <=5%; no family >25% (s1) | IMPLEMENTED | vcommon STRATA_SHARE, BAND_SHARE, BAND_TOL .03, CHUNK_MODE_TRAINING "LOCKED-560-FLUSH", GEN_SOURCE_CAP .05, FAMILY_SOURCE_CAP .25 |
| 12 | Pool ~3,000, floor 1,500, <=2 variants per source, voice <=8% of new rows (s1, VOICE-B5) | IMPLEMENTED | KEPT_TARGET 3000, KEPT_FLOOR 1500, MAX_VARIANTS_PER_SOURCE 2, VOICE_SHARE_OF_NEW_MAX .08; pool.select_kept, voice_share_ok, gate_c8_sizes |
| 13 | (a0) source eligibility: clean stamp, not human-label (A46), family not rolled, no L-R row, replay only after clean-up, length 10-400 (s3) | IMPLEMENTED | VariantChecker.check_variant (a0): source_stamp, source_human_label, source_rolled, source_lr, source_replay_uncleaned, length |
| 14 | (a1) independent denormaliser round trip (s3) | IMPLEMENTED | check_variant (a1): vb_denorm.denormalise; denorm / denorm_error |
| 15 | (a2) span survival A = B; negation and polarity never recoverable (s3) | IMPLEMENTED | check_variant (a2): SC.check_doc, BC.check_detail; spans_A/spans_B/A_B_disagree; span_check.pol_sig |
| 16 | (a3) ctx_recoverable_enabled = False in C2.1 (VOICE-B1) | IMPLEMENTED | voice_check.CTX_RECOVERABLE_ENABLED = False; turning on drops everything (ctx_exception_on); manifest ctx_recoverable_enabled false; test exists |
| 17 | (a4) generator-specific checks: A raw ASR exact, chunk mode, voice; B substitution list checked by aligner; C within one phoneme (s3) | PARTIAL | A done; B only checks that the "ops" key exists; C see item 6 |
| 18 | (a5) G6 token rule and WER band (<25%) by B's own edit distance (s3) | IMPLEMENTED | check_variant: vb_wer.wer/band_of; band and tokens (whitespace split; utterances <=400 tokens) |
| 19 | (a6) PII scrub and guards on the transcript and the whole row (s3) | IMPLEMENTED | check_variant (a6): _PII and _LITERALS regexes |
| 20 | (b)(c) G13 stamp of transcript AND whole row in batches <=500; stamp record; mix_guard needs the twin (s3) | IMPLEMENTED | voice_check.check_and_stamp (2 items per variant; registry sha in production; exempt hits clean; v["stamp"] fields); mix_guard; StampServiceRequired without a hook |
| 21 | Table or template change after hash export v1.1 means a new export and re-made variants (s3) | PARTIAL | voice_hash_export.py has --check; check_and_stamp does not verify the export is current (GEN/row_check.TemplateHashStale not imported by VOICE) |
| 22 | The 500-row WER pilot goes through the wrapper; kept rows are pool rows only if their condition is in the FINAL condition map, else dropped "condition removed" (s3) | PARTIAL | pool.condition_filter (V-D3) exists; no "condition removed" reason in REASONS and no code applying the final condition map to pilot rows |
| 23 | FIX TRIGGER: >1% G13 stamp drops (not exempt, not OHS-5) = ONE combined fix; span/verbalizer drops are not triggers (s3) | IMPLEMENTED | voice_check.FIX_TRIGGER_RATE = 0.01; summary g13_drop_rate, fix_trigger_g13; answer-stage drops counted separately |
| 24 | GV5: a G13-hit variant retires its source and its group; never re-rendered from the same source | MISSING | check_and_stamp drops only the hit variant; a sibling variant of the same source (<=2 per source) can still be kept; no retired-source set |
| 25 | Set-level checks once on the pilot pool and once on the built pool: V-C6, V-C7 (with generator id), V-C8, V-C9 per generator (A, B, C), V-D5, V-D6, V-D7, V-H1 (s3, s4) | PARTIAL | gate_c6_drift, gate_c7_surface (GEN_<gen> feature), gate_c8_sizes (item 10), gate_c9_noiser, shares_within_tolerance, survival_report, consistency_ok exist; gate_c9_noiser takes one WER list (no per-generator driver); V-H1 external |
| 26 | V-G1 (200-row G13 pilot) removed; V-C1..V-C5 and V-D1..V-D4 bars unchanged (s4) | IMPLEMENTED | no 200-row code; vgates gate_c1_roundtrip (>=5,000), gate_c2_oov, gate_c3_misaki, gate_c4_planted (recall >=99%, Wilson >=97%), gate_c5_coverage; V-D1..V-D4 in pool.py |
| 27 | VW-1 stamp coverage, VW-2 source stamp currency, VW-3 conformance record signed (s4) | IMPLEMENTED | VW-1 mix_guard; VW-2 check_variant (a0); VW-3 check_and_stamp raises ConformanceRecordRequired in production unless conformance_ok(code_sha()) |
| 28 | Ladder = WER bands L1 <3, L2 3-8, L3 8-15, L4 15-25; >25 excluded; L3+L4 = 35% (s5) | IMPLEMENTED | vcommon.BAND_EDGES, BAND_SHARE; wer.band_of; pool.select_kept band caps (stored 0-3, not named L1-L4) |
| 29 | VW-4 ladder report; P-V0 amber; P-V1 no removal power; P-V3 per-generator line; VOICE-B2 (L4 bar is a report line) (s4, s5) | N/A | post-training reports; variants carry generator and band fields |
| 30 | A1 pass-through of source_row_id and source_family so a dropped source drops its variants (s6) | IMPLEMENTED | variant fields; mix_guard twin check; select_kept counters |
| 31 | A2 AFLite-style repair for a failed V-C7 (<=30% filtered, band and strata shares kept) (s6) | MISSING | no repair code in VOICE |
| 32 | A12 not applied to voice transcripts (s6) | IMPLEMENTED | no perturbation code in VOICE (by absence) |
| 33 | Source rules: GEN stems (AR-F1, AR-F2, TM-T1/T2, <=60 words) <=5%; TP and HX forms are not voice sources (s7) | PARTIAL | GEN <=5% enforced (GEN_SOURCE_CAP); no source-form check, so TP/HX rows are not refused |
| 34 | G10 decision_spans with roles; fallback regex rows <=30% (s7, V-C5) | IMPLEMENTED | vcommon.ROLES, FALLBACK_SPAN_CAP; verbalizer spans; gate_c5_coverage |
| 35 | Lane rule: ship at achieved size; floor flag (s9) | IMPLEMENTED | select_kept report ships_at_achieved_size, below_floor |
| 36 | Usage shed and money shed positions (s9) | N/A | orchestrator policy |
| 37 | Conformance CT-V-* tests (s10) | MISSING | only CT-V-G1-no-llm exists (solver_b/tests/test_vb_blind.py) |
| 38 | Names for manifest v1.1: VGEN-A/B/C, PN-SWAP, HOMOPH-SWAP, BOUNDARY-SHIFT, ctx_recoverable_enabled, L1-L4 (s11) | IMPLEMENTED | in NAMES_MANIFEST_V1_1/V1_2; HASH_EXPORT lists V1, V1_1, V1_2; vcommon.VoiceAllow still pins V1 (no functional effect, strata unchanged) |
| 39 | GV9, GV12, GV1, GV2, GV3, GV4, GV6, GV7, GV8 | N/A | VOICE emits no heldout_family/dev_only rows; dev-only chunk modes refused at creation; no Haiku rewording; negation/polarity/digit insertions already dropped |

Contradictions with Opus rulings: none found (licence list exact SPDX; ctx_recoverable False; no L-R source; C-off shares 55/45; voice <=8%). Defects (not ruling breaches): `vgates.gate_c8_sizes` mis-evaluates 50/30/20 once C is on (item 10); Generator C not built (item 2); GV5 sibling retirement missing (item 24).
Dry run uses addendum sizes? NO. `dryrun.py` builds 20 TEST-ONLY synthetic examples (generator A stood in by planted.py, B by a test confusion table); no C, no 50/30/20, no 3,000 pool, no stamp.
Tests: 109 pass (111 s); solver_b/tests not run.

