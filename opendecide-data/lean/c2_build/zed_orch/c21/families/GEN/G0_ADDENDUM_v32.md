# G0 ADDENDUM v3.2: GEN (general program-gold rows)

Lane L-G. Author: Sonnet 5.5 high. Written Sun 18 Oct 2026 (UTC). Status: DRAFT for Opus batch 1 (Mon 19 Oct), with the
other v3.2 G0-lites and addenda. Design only: no rows, no generator run, no download, no model call, no code executed.
Read scope used: C2_1_BUILD_ORDER.md (L-G lane block and the v3.2 lane additions), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7,
8, 16, the PRE-REGISTERED RULES block of section 3 only, C2_1_EXTRA_LEVERS.md section 1 (ADOPT NOW), GEN/G0_LITE.md and
families/G0_APPROVALS.md, PREREG_FINAL.md blocks A77, A79, A82 (read only). The public-train inventory file loaded whole
(its section 4 "General" rows were seen); no research_v4 file, no hardest.md, no stripped excerpt of it was opened.
Not opened: any "ohs" or "sealed" path, OHS5_BRIEF_DRAFT.md, any C2 file, data/, logs/, ~/.claude, any generator of
T27 / T40-T46 / T42 / T43, any benchmark item text.
RELATION TO THE G0-LITE: GEN/G0_LITE.md (with its appended "Opus rulings 18 Oct") stays in force. Where this addendum
differs, this addendum binds, and it needs Opus approval (batch 1) before generator code for the NEW parts freezes.
Every identifier in section 11 is a NAME only (for the names-only manifest v1.1).

## 0. What this addendum changes (one paragraph)

(1) OWNER RULE (18 Oct, binding): every GEN row is answer-checked and G13-stamped WHEN IT IS MADE, through the stamp
wrapper; the 200-row G13 pilot (gate G-G1) is gone; set-level checks run once on the 1,000-row pilot and once on the built
family. (2) Sizes by SUBSTITUTION inside the 7,000: about 2,000 rows from vetted third-party generators (Reasoning Gym
allow-list, DeepMind Mathematics, bAbI; fresh seeds only) and 1,100 rows from six gold-by-construction hard-extension
forms replace 3,100 rows of the five original sub-blocks; the total stays 7,000. (3) A difficulty ladder L1-L4 with a
program parameter per sub-block, 25-30% of rows at L3-L4, and the measured bar "C2 <= 70% on L4". (4) A21 length coverage
by program length tiers. (5) The generic NOTA option is built but OUT of the mix. (6) The ADOPT NOW lever table for this
lane (section 7), the conformance record items (section 10) and the v3.2 shed positions (section 12).

## 1. Sizes by substitution (total stays 7,000 kept TRAIN rows; 600 DEV rows stay out of training)

The original forms (G0-lite section 3) keep their ids; their counts shrink as below. Pair share, letter balance, binary
yes-share, L1 thirds, token rules and wording rules of the G0-lite section 3 apply to the new rows too (hard-extension
forms add their own bars in section 4).

| Sub-block | Original rows | New rows | Change |
|---|---|---|---|
| ARITH (AR-F1 450, AR-F2 150, AR-F3 200) | 1,600 | 800 | -800 |
| LOGIC (LG-L1 300, LG-L2 300, LG-L3 200, LG-L4 100) | 1,500 | 900 | -600 |
| CAUSAL (CA-C1 250, CA-C2 200, CA-C3 150, CA-C4 100, CA-C5 100) | 1,300 | 800 | -500 |
| TEMPORAL (TM-T1 250, TM-T2 150, TM-T3 150, TM-T4 150) | 1,300 | 700 | -600 |
| TABLE (TB-B1 250, TB-B2 200, TB-B3 150, TB-B4 100) | 1,300 | 700 | -600 |
| TP third-party generators (section 3): TP-DM 600, TP-RG 1,000, TP-BA 400 | 0 | 2,000 | +2,000 |
| HX hard extensions (section 4): HX-E 300, HX-U 200, HX-S 200, HX-T 150, HX-O 150, HX-D 100 | 0 | 1,100 | +1,100 |
| **Total** | **7,000** | **7,000** | **0** |

Candidates generated: about 8,850 as in the G0-lite (about 16% buffer for stamp drops, answer-check drops, OHS-5 collision
drops up to 5%, A50 / A49c trims). A dropped row is replaced by the next seed of the SAME cell (form x level x pair slot);
the buffer is a plan for drops, not a cut of scope. If the buffer runs out in a cell, that cell ships at the achieved size
(logged), and no other sub-block back-fills it above +25% of its own target (G0-lite section 10 rule stays).
DEV rows: 600, never trained on: ARITH 90, LOGIC 90, CAUSAL 80, TEMPORAL 80, TABLE 80, TP 90 (30 per generator, from the
held-out tasks of section 3), HX 90. Domains D23 and D24 and 10% of wording groups stay dev-only. L-0 still decides whether
they merge into mixdev.
Mix interaction: GEN rows get NO hard-bin upweight (weight 1.0). The ladder bar in section 5 raises a program parameter; it
never drops rows by model score and never changes a weight.

## 2. Check at generation (OWNER RULE) [OWNER-ROW; plan 16.1 steps 0, 2, 3, 4, 6, 7]

Owner, 18 Oct: "If you're building one row, check that row at that same point and that's it ... then train."
Every GEN candidate row is written ONLY through the stamp wrapper, in batches of at most 500 rows, the same day. Per row:

| Step | What runs on THIS row | Pass rule |
|---|---|---|
| (a1) Answer: solver A = solver B | solver A (in the generator) and solver B (a PROGRAM from a separate Sonnet high session, G1) both compute the answer from the spec; for TP rows B re-derives it from the instance fields (section 3) | equal, else drop and log (sub-block, form, check id) |
| (a2) Render parse-back | solver B parses the final prompt text back to the spec and recovers every slot exactly | exact, else drop |
| (a3) Uniqueness | exactly one option equals the answer; options pairwise distinct after normalisation; no tie in any argmax / argmin / order; closed world; for TP rows each wrong option is rejected by the task's own check | 100%, else drop |
| (a4) Pad invariance (new, A21) | the answer with the inert padding removed equals the answer with it present (section 6) | 100%, else drop |
| (a5) Pair integrity | a pair partner dropped by any check drops the other member too; the pair is re-made from the next seed; pair share (>= 30% of rows in matched pairs per sub-block) is counted AFTER drops | pair_id never singleton |
| (a6) Names guard | every entity, variable, event and column name from NS-TRAIN; TP name rule of section 3; closed allow-list of domains, units, carriers, form ids | 0 names off the list, else drop |
| (a7) Token rule G6 | per row <= 1,536 tokens; mean <= 800 and > 1,024 on <= 10% are read per sub-block at set level | row over 1,536 dropped |
| (a8) PII scrub and guards | the C_DATA_SPEC guards of plan section 2 (CVE / GHSA ids, /rosetta/i, stackoverflow links, BIG-bench canary, benchmark repo names) | a hit drops the row (drop-only, never an edit) |
| (a9) decision_spans (G10) | `decision_spans` with ROLES (negation/polarity, number, entity/path/flag; AUTHORITY is not used by GEN) exported for voice-eligible forms | present on 100% of AR-F1, AR-F2, TM-T1, TM-T2 rows |
| (b) G13 stamp | the row goes to the stamp service on the Mac and is checked against EVERY registered target with every method listed for that target (R6 scaffolding exemption; OHS-AC binding for new rows; OHS-5 hash export from Sat 24 with a separate hash-export salt) | clean, else drop and log (row id, target name, method only; never the matched text) |
| (c) manifest stamp | row id, registry sha, method-set version, generator code sha, template hash, verdict | written; the mix guard refuses a row without a current clean stamp |

RULES AROUND THE WRAPPER
- No unstamped or failed row ever enters a family pool (there is no quarantine pool). A stamp is current only for its
  registry sha; a late target runs only the DELTA targets on the affected rows (step 6); any template or wording-pool change
  after hash export v1.1 means a NEW hash export, and rows from the changed templates are re-made (rows from unchanged
  templates keep their stamps).
- The 1,000-row pilot is generated THROUGH the wrapper, so its kept rows are pool rows. G3 (no free pilot tuning) stands:
  the pilot is the first measured look; ONE combined fix; no "re-run for free".
- FIX TRIGGER (plan 16.1 step 3), read on ALL pilot rows and on each full-generation day: more than 1% of rows dropped by
  the G13 stamp for a reason other than exempt scaffolding or OHS-5 collisions (collisions: dropped row by row; up to 5%
  of a sub-block is NOT the fix iteration) = the family's ONE combined fix. Answer-check drop rates use this G0-lite's own
  bars: A-vs-B disagreement <= 1.0% of candidates per sub-block, parse-back drops <= 2% per sub-block (G-A1, G-A2).
- SET-LEVEL checks run ONCE on the 1,000-row pilot and ONCE on the fully built family, never again at the mix: A50 G6 at
  size, A49c balance, wording variety (>= 50 per form, none > 2%), matched-pair share, the ladder and its bar, the G5 probe
  harness (G-S1 to G-S6 and the new probes of sections 3 and 4), G5-H and G3-H reads with Sonnet adjudication and Opus
  A43(d) confirmation. The confirm rule (one re-run on a fresh 2x sample, re-run decides) stays for GEN.
- Final mix: the binding G13 is one confirming pass (stamp audit + full exact / hash re-run on every mix row + fuzzy only
  on delta targets). GEN adds nothing to it.
- A template-level look is also needed by A1 (section 7): every row stores `template_id`, `operator_ids`, `wording_id`,
  `error_model_ids`, `level` and `length_tier` in the manifest.

## 3. Third-party generator sub-blocks TP-DM, TP-RG, TP-BA (about 2,000 rows) [CRIT A4; INV A11-A13]

Purpose: a second source of program-gold structure from outside our own generators (diversity for G). Gold is the output of
the third-party program on a fresh seed, re-derived by our solver B. No model writes or labels any TP row.

| Block | Generator (licence line from the inventory) | Rows | Eligibility and limits |
|---|---|---|---|
| TP-DM | DeepMind Mathematics, REGENERATED from the code (not the HF mirror). "Apache License / Version 2.0", https://raw.githubusercontent.com/google-deepmind/mathematics_dataset/master/LICENSE (inventory A13, fetched 18 Oct 2026) | 600 | modules whose answer is an exact integer, decimal or boolean and can be re-derived by our stdlib solver B (arithmetic, number theory, comparison, base conversion, measurement conversion, polynomial evaluation); at most 100 rows per module; interpolation / extrapolation test files and their instances are never read |
| TP-RG | Reasoning Gym generators, PER-TASK ALLOW-LIST. "Apache License / Version 2.0", https://raw.githubusercontent.com/open-thought/reasoning-gym/main/LICENSE (inventory A12) | 1,000 | at least 8 tasks from at least 4 categories; at most 150 rows per task; EXCLUDE gsm_symbolic (gsm8k is an A61(a) HIT), codeio ("transformed by an LLM"), and any task wrapping a public benchmark; review rush_hour, arc_1d, knights_knaves one by one; every task passes the admission test below |
| TP-BA | bAbI tasks generator (code only). "BSD License / For bAbI tasks software", https://raw.githubusercontent.com/facebookarchive/bAbI-tasks/master/LICENSE.md (inventory A11) | 400 | at least 5 tasks; at most 100 rows per task; the published bAbI test files are never read |

ADMISSION TEST FOR A TASK OR MODULE (all by program or record; Opus approves the allow-list in ONE batch, as a names-only
list, by Fri 23 12:00 because it is a source addition):
1. Licence record (URL, quote, fetch date) and A61(b) record present; not an A61(a) HIT; not a wrapper of a public benchmark;
   S-pre and S-post 8.5 PASS for the generator as for an L-R source (conservative reading; Opus to confirm, open point 3).
2. Solver B exists: a stdlib program written by a separate Sonnet high session from the task description and the instance
   field schema only, passing a 2,000-instance A=B fixture at 100% before the task is admitted.
3. The answer is an integer, 2-dp decimal, boolean or a small enumeration, so program near-miss distractors can be built
   (our own error models; never the generator's model-made text). Each wrong option must be REJECTED by the task's own
   answer check (so no wrong option is also correct).
4. Names: TP rows follow NS-TRAIN as far as the generator exposes entity names as slots; the generator's name lists are
   replaced by NS-TRAIN names at the config level. A task whose surface names cannot be replaced and are not label-
   independent filler is NOT admitted. (No names-guard exemption is requested; see open point 4.)
5. Fresh seeds only: every instance seed comes from the TRAINING-salt stream; a seed or instance that equals a published
   test instance is dropped by the stamp (the published files are G13 targets).
6. Run location: offline, no network, a pinned release sha, on the CPU host of L-0's choice (the bAbI generator is Lua; if it
   cannot run offline, TP-BA rolls alone and its 400 rows go back to LOGIC / TEMPORAL within +25% of their own targets).
HELD-OUT FOR DEV: per generator, one module or task (DM 1 module, RG 2 tasks, bAbI 1 task) is dev-only; it supplies the
TP dev rows and the P-4 held-out gap.
TP rows are NOT voice-eligible (math and symbol stems are not spoken in C2.1).

## 4. Hard-extension forms HX (1,100 rows; gold BY CONSTRUCTION only) [CRIT D3; plan section 2; G1]

Plan section 2 lists the hard-extension generators. G1 is binding: no LLM sets or checks a label; the critic's "two Claude
solvers + Opus adjudication" route is NOT used. Each form builds a typed world state, applies exactly one programmatic edit,
and the label changes by construction. All text is rendered from wording pools (Haiku medium, closed, hashed). All names
come from NS-TRAIN. Carriers reuse TXT-PROSE, TXT-BULLET, TXT-NUMBERED, TXT-TIMELINE, TXT-LEDGER.

| Id | Question | k | Rows | Gold by construction | Pair design | Form-specific PK gates |
|---|---|---|---|---|---|---|
| HX-E | Is the claim supported, contradicted or not stated by the facts? (one-edit flips) | 3 | 300 | fact base of typed statements; claim = a rendered statement with ONE edit (negation toggle, quantifier swap, scope shift, date shift by a stated unit); label = evaluator over the fact base; "not stated" = the subject or attribute absent from the fact base | claim pair (same facts, claim edited) and fact pair (same claim, one fact edited); >= 60% of rows in pairs | edit-type x label table: every edit type yields each of the 3 labels within 33.3% +/- 8 pp; claim-only probe (no facts) k=3 bars 36.3 / 39.3 |
| HX-U | Which value does the passage give for the asked attribute (4 values, one of them "The passage does not say")? | 4 | 200 | passage of typed facts; the asked fact is present (gold = its value) or REMOVED and replaced by an inert fact of EQUAL token length (gold = "does not say"); the fourth option text is fixed in every HX-U row (task-defined, not appended NOTA) | answerable / unanswerable twins; "does not say" is the gold in 30% of rows | length-only probe AUC 0.55 / 0.60 (equal-length replacement); question-only probe for the answerable-vs-not class AUC 0.55 / 0.60; no dangling reference to the removed fact (program check, 100%) |
| HX-S | Which summary sentence is NOT supported by the document? | 4 | 200 | document of 6-12 numbered facts; summary of 4 sentences, each rendered from one fact; ONE sentence is built from a mutated fact (attribute value changed, entity swapped, or an extra detail added) at a known span | pair = same document and summary frame, the mutation moved to another sentence | unsupported-sentence position 25% +/- 3 pp; sentence-surface probe (length, numeral presence, specificity) k=4 bars 28.0 / 31.0 |
| HX-T | Which step is the first wrong step in the derivation? | 4 | 150 | LOGIC derivation (80) or TABLE computation (70) trace of 4-8 steps with ONE injected error; later steps follow from the wrong value; gold = the injected position; options are 4 steps incl. the gold | pair = error moved to a different step | gold position 25% +/- 3 pp; step-length / token probe k=4 bars |
| HX-O | Select-all as per-option yes/no (90); ordinal bucket (60) | 2 / 4 | 150 | select-all: each option statement is true or false by evaluation of the world state; ordinal: the bucket (4 stated severity bands) computed from a stated measure and stated thresholds. Choice of buckets only; no Score item (renderer Score support is UNVERIFIED, critic A6) | pair = one slot edited so the bucket or the truth value changes | yes share 40-60%; ordinal buckets 25% +/- 5 pp each; options-only probe k bars |
| HX-D | User-defined operator: compute the value under operators defined in the prompt | 4 | 100 | 1-3 nonce operators from NS-TRAIN, each defined by a table or rule in the prompt; evaluate with exact arithmetic | pair = one entry of an operator table edited | operator-symbol probe (does the operator id predict the answer class) AUC / k bars; option-heuristic panel G-S2 |

All HX forms also face the GEN probes G-S1 to G-S6 pooled by form, the token rule, the wording rule (>= 50 wordings per
question form, none > 2%) and letter balance. The "genuine unknown at a fixed rate" mechanism is NOT a separate form: LG-L1
already holds it at 33.3% +/- 5 pp.
GENERIC NOTA (plan 16.9, extra-lever O10 default): a program transform that appends "none of the above" to any k-option form is
BUILT (name NOTA-GENERIC) and kept OUT of the mix. Task-defined classes (LG-L1 "undetermined", HX-E "not stated", HX-U
"does not say") are part of their form in every row and are in the mix; this reading is open point 2. The abstain-like gold
share across GEN (L1 undetermined, HX-E not stated, HX-U does not say) is REPORTED (about 5-6%), not gated.
HX rows are NOT voice-eligible (passages and traces are long and full of numbers); voice sources stay as approved.

## 5. Difficulty ladder [CRIT D1, D2; plan section 1 E]

Each mechanism gets a level parameter L1-L4 set by PROGRAM (never by a model read, never by filtering on another model's
score). Shares per sub-block: L1 <= 25%, L2 about 45-50%, L3 + L4 = 25-30% (consistent with the plan's "hard <= 30%, easy
<= 25%" and the ladder rule ">= 25% at L3-L4"). The old "hard bin" of the G0-lite IS L3 + L4. No upweight (GEN rule).

| Sub-block / form | Mechanism (program-parameter) | L1 | L2 | L3 | L4 |
|---|---|---|---|---|---|
| ARITH | DAG depth, fan-in, unit conversions, rounding rule, wrong-base percent trap | depth 3-4, no conversion | depth 5, one conversion | depth 6-7, two conversions, stated rounding | depth 8, fan-in 3, three conversions, a percent whose base is itself a derived quantity |
| LOGIC L1/L2/L4 | chain length, negated heads, ground atoms, distractor rules | chain 2, atoms <= 6 | chain 3-4, atoms <= 10 | chain 5-6, atoms <= 14, one negated head | chain 7+, atoms 16, two negated heads, over-chaining and converse traps both present |
| LOGIC L3 | search space | 4 items, 3 constraints | 4 items, 5 constraints | 5 items, 6 constraints | 6 items, 8 constraints (solution count fixed to 1) |
| CAUSAL | variables, mediators, collider on the queried pair, intervention depth | 4 vars, no collider | 5 vars | 6 vars, collider or confounder on the pair | 7 vars, collider plus mediator, counterfactual on a descendant |
| TEMPORAL | rule count, clamp vs roll-over with leap days, windows, weekend / holiday list size | one rule | two rules | leap-day case or end-of-month clamp inside a window | clamp + leap + holidays + dependency graph depth 5 |
| TABLE | rows, joins, group-by, ties excluded by program | 4-6 rows, one filter | 8-12 rows, filter + aggregate | 14-20 rows, group + order | 20 rows, join with fan-out trap, two filters |
| HX-E | edit type and distractor facts | date shift | negation | quantifier swap | scope shift with 6+ distractor facts |
| HX-U / HX-S / HX-T | passage size, distractor facts, mutation subtlety | 4-6 facts | 6-8 | 9-10, extra-detail mutation | 11-12, attribute-value mutation of a numeral, long trace |
| HX-O / HX-D | statements per question, threshold nearness, operator count | 3 statements | 4 | 5, thresholds within 10% | 6, near-threshold values, 3 operators |
| TP-DM / TP-RG / TP-BA | the generator's own difficulty knobs (DM module difficulty argument, RG task config, bAbI task id) | fixed in a level table BEFORE the pilot, one table per generator, hashed with the allow-list | | | |

Each hard cell has an easy-looking twin with the opposite label (matched pair at the same level). The alarming / calm quad is
not used by GEN (it is mandatory for T50, T51, T53, T41c, T56 only).
MEASURED BAR (D2, set-level, ONCE on the 1,000-row pilot): base 4B and C2 (C1 if C2 has no weights) are read on od-l4b
(queue priority 2, a pre-freeze data check on OUR models, not a kill gate). Bar: C2 accuracy on the L4 rows pooled over
sub-blocks (about 100 rows, binomial SE about 4.6 pp) is <= 70%. A miss is folded into the family's ONE combined fix by
RAISING the program parameter of the sub-block(s) whose L4 accuracy is above 70% (never by dropping rows by model score);
after the fix a miss is a report line, not a kill (difficulty is not validity). Per-sub-block L4 accuracy is reported.

## 6. A21 length coverage [LEV A21; plan 5 LENGTH COVERAGE]

Protects G on long inputs (LLM2Jev: narrow data took the 4B from 81.4 to 74.9; long data fixed long-input errors).
- Program LENGTH TIERS per row: LT1 < 256 tokens, LT2 256-511, LT3 512-1,023, LT4 1,024-1,536. Design shares per sub-block
  (fixed before any look): LT1 30%, LT2 30%, LT3 30%, LT4 10% (so mean <= 800 and > 1,024 tokens on <= 10%, G6).
- Lengthening is by INERT IN-WORLD PADDING only: extra table rows, extra events, extra rules, extra facts that the answer
  does not use (never filler prose, never repeated text). The pad is drawn independently of the label and shared by both
  members of a pair. Step (a4) of section 2 re-checks that padding does not change the answer.
- Probes G-S4 (length-only) and G-S5 apply per tier as well as pooled.
- L-0's CPU histogram (general block + block R + replay token lengths vs the public-G panel and G-like dev lengths) is run
  once on the built family. Pre-written GAP RULE (this addendum; L-0 may tighten it before the look, never loosen it after):
  in five token bins (< 128, 128-255, 256-511, 512-1,023, 1,024-1,536) a gap exists if the dev share of a bin exceeds the
  mix share (GEN + block R + replay) by more than 5 pp, or the dev p90 exceeds the mix p90 by more than 20%. If a gap
  shows, GEN's tier shares move toward the missing bins inside the G6 limits (one change, logged); this is PB (proof
  before use), not a kill.

## 7. ADOPT NOW levers and this lane (A1-A36; plan 16.2)

| Lever | GEN |
|---|---|
| A1 template-level gold-bug audit | CARRIES. GEN exports `template_id`, `operator_ids`, `error_model_ids` per row so the L-0 script can slice C2's confident disagreements by template. A flagged template is re-checked by solver B and an execution re-run; drop-only by template slice; Opus confirms each dropped template |
| A2 AFLite-style filter (one-fix repair) | AVAILABLE as a repair tool inside GEN's ONE combined fix for a failed shortcut probe: probe back under its bars, filtered <= 30% of the family, easy share (L1) still <= 25%; features are the G5 probe features (CPU), no model embeddings. It counts as the fix iteration |
| A3-A9, A13 row types | not GEN (other lanes) |
| A10 cue-invariance, A11 canonicaliser, A12 character perturbation, A14 long-input slice, A16 observation formats | NOT APPLICABLE: GEN is not a gate family and has no tool outputs. A21 (section 6) is the length lever for GEN |
| A15 format dialects of card body and tool schemas | NOT APPLICABLE: GEN has no policy card or tool schema. Its five table carriers and five text carriers are already approved |
| A17 multilingual | NOT ADOPTED (A82 9) |
| A18 voice generator C | VOICE (see VOICE addendum) |
| A19, A20, A22-A29 | recipe, preflight and reporting items (L-0, recipe, L-E); GEN supplies metadata only: `level`, `length_tier`, `sub_block`, `form_id`, held-out flag |
| A21 length coverage | CARRIES (section 6) |
| A30-A36 | serving and product |

## 8. Gate changes (class key as in the G0-lite: PK = PRE-FREEZE KILL, CPU, data only; PR = POST-TRAINING REPORT)

REPLACED / RE-TIMED
- G-G1 (200-row G13 pilot): REMOVED. Replaced by G-W1 to G-W3.
- G-A1, G-A2, G-A3 now run PER ROW at creation (section 2); their bars (100% on kept rows; disagreement <= 1.0% and parse-
  back drop <= 2% of candidates per sub-block, read on all pilot rows) are unchanged.
- G-S1 to G-S6, G-A4, G-A5, G-G2, G-H1, G-H2: bars unchanged; they run ONCE on the pilot and ONCE on the built family and
  now include the TP and HX sub-blocks pooled by sub-block and by form. G-H1 covers 300 rows stratified over the seven
  sub-blocks (about 43 each) and a Haiku read of 100% of the wording pools incl. the HX pools and the Choice-stem framing of
  TP rows; for each admitted TP task the question-template list is read in the allow-list review.

NEW
| Gate | Class | Numeric bar | Applies |
|---|---|---|---|
| G-W1 Stamp coverage | PK | 0 pool rows without a current clean stamp (CPU test on the pool and the manifest) | every batch; pilot; full |
| G-W2 Stamp drop rate | PK | fix trigger when > 1% of all pilot rows (or of a full-generation day) are G13-dropped outside exempt scaffolding and OHS-5 collisions; collisions <= 5% of a sub-block are not the fix iteration; > 5% is | pilot; daily |
| G-W3 Template-hash currency | PK | every stamped row's template hash equals the current export for its template (else re-made) | pilot; full |
| G-W4 Pair integrity | PK | pair_id never singleton; pair share >= 30% per sub-block after drops | pilot; full |
| G-T1 TP admission records | PK | 100% of admitted tasks/modules have licence record, A61(b) record, S-pre/S-post PASS, Opus allow-list approval, solver B fixture 100% (2,000 instances) | before any TP row |
| G-T2 TP distractor validity | PK | every wrong option rejected by the task's own check on 100% of kept TP rows | every row |
| G-T3 TP shape | PK | >= 8 RG tasks / >= 4 RG categories; <= 150 rows per RG task, <= 100 per DM module, <= 100 per bAbI task; TP share 2,000 +/- 0 until a sub-block rolls | pilot; full |
| G-X1 HX gold by construction | PK | edit applied by program; evaluator label equals the label implied by the edit rule on 100% of kept HX rows; zero LLM-set labels (G1) | every row |
| G-X2 HX form probes | PK | the per-form bars in the section 4 table; k=2 forms AUC 0.55 / 0.60, k=3 36.3 / 39.3 percent, k=4 28.0 / 31.0 percent; confirm rule applies | pilot; full |
| G-L1 Length tiers | PK | tier shares within +/- 3 pp of 30 / 30 / 30 / 10 per sub-block; mean <= 800; > 1,024 tokens on <= 10% | pilot; full |
| G-L2 Pad invariance | PK | 100% (per row check) | every row |
| G-D1b Ladder shares | PK | per sub-block L1 <= 25%, L3 + L4 in 25-30%, no trap_type above 35% of wrong-option slots | pilot; full |
| G-D2b C2 <= 70% on L4 (od-l4b read of our model) | PK-D (data-only read of OUR model, drop-nothing, parameter-raising only); a miss after the fix is a report line | pooled L4 accuracy of C2 <= 70% | pilot only |
| G-C1 Conformance record signed | PK (process) | a signed ruling-to-code conformance record for the current generator code sha and ruling sha exists before any record is built (section 10) | before the wrapper accepts GEN rows |
| P-7 Abstain-like gold share (L1 undetermined, HX-E not stated, HX-U does not say) | PR | report the share and per-class accuracy | after training |
| P-8 TP vs Claude-authored accuracy | PR | accuracy on TP dev rows (held-out tasks) vs original sub-block dev rows, with CI; no causal claim (P-6 stands) | after training |

## 9. Timeline (Sun 18 - Mon 2 Nov) [plan 16.7]

- Sun 18: this addendum; NEW NAMES (section 11) to L-0b for manifest v1.1.
- Mon 19: Opus batch 1; names freeze (v1.1). Generator CODE for original sub-blocks continues (no rows).
- Tue 20 - Fri 23: TP admission records; solver B fixtures; allow-list names to Opus by Fri 23 12:00 (last source addition;
  v1.2 names-only copy to L-S the same day). HX generators and wording pools; template hash export (a new one at every
  later template change).
- Wed 21: stamp-service throughput number (L-0b). Sat 24 18:00: conformance records signed (else GEN starts no rows) and
  stamp service signed off (else row jobs wait; the freeze date does not move).
- Sun 25: ROWS START (row-start guard): the 1,000-row pilot through the wrapper; Mon 26: set-level gates on the pilot,
  ladder read on od-l4b, measured token histogram for the money projection; ONE combined fix lands by Wed 28.
- Tue 27 - Wed 28: full generation, stamped at creation; set-level gates once on the built family; A1 template audit from C2
  reads (not a kill gate). Thu 29 12:00: last fix iterations. DATA FREEZE per the orchestrator's declaration (early Fri 30 12:00
  or fallback Mon 2 Nov 23:59).

## 10. Ruling-to-code conformance items for GEN (plan 16.1 step 0; a fresh Sonnet 5.5 high session writes the map and CPU
tests, never the GEN builder; Opus 5.5 high signs; the wrapper REFUSES GEN rows without the record)

| Clause (ruling id) | Code place (to be filled by the map) | CPU test id |
|---|---|---|
| G1 solver B is a program; no LLM label | solver B module; label writer | CT-G1-no-llm-label (grep + import test); CT-G1-B-blind (B imports nothing from A) |
| G2 / G3 fix iteration bookkeeping | pilot controller | CT-G3-one-fix (second fix request refused) |
| G5 probe harness (grouped split, L2 LR, max(AUC, 1-AUC), 97.5th-pct bound, perm check, planted-leak check, GBT counts for GEN) | L-0 harness config for GEN | CT-G5-planted-leak (AUC >= 0.80); CT-G5-perm (0.50 +/- 0.03) |
| G6 token rule | wrapper step (a7) | CT-G6-1536 |
| G10 decision_spans with roles | generator export | CT-G10-spans-present |
| C1 (CA-C4 / CA-C5 state independent random exogenous inputs, no fixed values; gold = d-separation / backdoor validity on the graph) | CAUSAL renderer and solver | CT-C1-no-fixed-exogenous |
| Ruling 4 (600 DEV rows never trained) | split writer | CT-R4-dev-not-in-mix |
| Ruling 6 (GEN voice source <= 5%; AR-F1, AR-F2, TM-T1/T2 stems <= 60 words, no table) | voice-eligible flag | CT-R6-voice-eligible-only-listed |
| This addendum: A=B and parse-back at creation; pad invariance; pair integrity; ladder shares; TP admission; HX gold by construction; NOTA-GENERIC out of the mix | wrapper steps (a1)-(a5); mix guard | CT-A-AB, CT-A-parse, CT-A-pad, CT-A-pair, CT-A-ladder, CT-A-TP-admit, CT-A-HX-edit, CT-A-nota-out |
| data/ohs3* and ohs3_parts/ skipped in every data/** glob | every GEN program | CT-OHS3-skip |
No GEN program reads a path containing "ohs" or "sealed"; the wrapper and registry are reached only through the stamp service.

## 11. NEW NAMES for the names-only manifest v1.1 (names only; no rows)

```
FAMILY: GEN (addendum v3.2)
NEW_SUB_BLOCKS: TP-DM, TP-RG, TP-BA, HX-E, HX-U, HX-S, HX-T, HX-O, HX-D
NEW_FORM_IDS: HX-E HX-U HX-S HX-T HX-O HX-D
EXTERNAL_SOURCES (code only; licence records pending):
  DeepMind Mathematics (google-deepmind/mathematics_dataset, Apache-2.0),
  Reasoning Gym (open-thought/reasoning-gym, Apache-2.0),
  bAbI-tasks (facebookarchive/bAbI-tasks, BSD)
RG_ALLOW_LIST: produced from the pinned release by program, Opus-approved by Fri 23 12:00; the manifest carries the final task
  names. Task names to REVIEW first (UNVERIFIED, from the inventory): rush_hour, arc_1d, knights_knaves. EXCLUDED by name:
  gsm_symbolic, codeio, any task wrapping a public benchmark
DM_MODULE_LIST: produced by program from the pinned code (modules with exact integer / decimal / boolean answers); Opus approves
BABI_TASK_LIST: produced by program from the pinned code; Opus approves
TP_ROLE_TAGS: TP-HELDOUT-DEV
LENGTH_TIERS: LT1, LT2, LT3, LT4
LADDER_LEVELS: L1, L2, L3, L4
TRANSFORMS: NOTA-GENERIC (built, OUT of the mix), PAD-INERT (inert in-world padding)
HX_EDIT_TYPES: EDIT-NEG, EDIT-QUANT, EDIT-SCOPE, EDIT-DATE, MUT-VALUE, MUT-ENTITY, MUT-EXTRA-DETAIL
HX_TASK_DEFINED_OPTION_TEXTS: NOT-STATED (HX-E), DOES-NOT-SAY (HX-U)
CARRIERS: reuse TXT-PROSE, TXT-BULLET, TXT-NUMBERED, TXT-TIMELINE, TXT-LEDGER (no new carrier)
NAMESPACE: NS-TRAIN only (TP generator name lists replaced by NS-TRAIN at config level)
```
The domain list of the G0-lite section 9 is unchanged (D01-D22 train, D23-D24 dev); HX forms reuse it.

## 12. Fix iteration, kill rule and shed positions (v3.2)

- ONE combined fix per family (G3). Triggers: the section 2 fix trigger; a PK gate failing at the pilot; A-vs-B disagreement
  or parse-back drops above their bars; G-H1 confirmed defects above the bar (4 rows or more of 300, or two defects in one
  template); a ladder miss (G-D2b, parameter-raising); OHS-5 collisions above 5% of a sub-block. A fix may change generator
  code, error models, carriers, wording pools, level tables, length-tier shares (not the A21 gap rule) and may use A2.
- KILL RULE: sub-blocks stay independent (ruling 3): a sub-block (incl. each TP and HX block) that fails a PK gate after its
  one fix, or is not through all PK gates at the declared data freeze, rolls to C2.2 / C3 with the gate and numbers
  logged; GEN ships with the sub-blocks that pass and the shortfall is not back-filled above +25% of the receiving
  sub-block's own target. POST-TRAINING lines are never kill rules. GEN is not a P0 family and does not count toward the
  6-of-9 floor.
- USAGE SHED (plan section 8, v3.2): research pass and extra tasksource scouting, then wave-C P1, then the voice pool, then
  open tier-C L-R datasets, then GENERAL ROWS (fifth), then remaining L-R, then remaining lanes. (The G0-lite said "third".)
- MONEY SHED (plan 16.7): step 8 is "general block to 5,000". Pre-registered way to apply it, only on a MEASURED projection:
  scale every kept form by 5/7 with whole pairs dropped together and the L3-L4 / length-tier shares kept, TP and HX scaled
  alike; nothing is shed on an estimate.

## 13. Open points for Opus (batch 1)

1. Substitution split (section 1): TP 2,000 and HX 1,100 out of the original 3,100 rows of five sub-blocks, with ARITH
   halved. Is this the right place to take the rows from, or should LOGIC / TABLE give more than ARITH?
2. NOTA: confirm that task-defined classes (L1 undetermined, HX-E not stated, HX-U does not say) are in the mix while the
   generic "none of the above" transform is out (extra-lever O10 default, plan 16.9).
3. Do the three TP generators need the full S-pre / S-post 8.5 stages like an L-R source? (I assume yes: conservative.)
4. TP names: this addendum requests NO names-guard exemption and instead admits only tasks whose name slots can be replaced
   by NS-TRAIN. If that leaves fewer than 8 RG tasks, should a scoped exemption (as for L-R / P1 realism) be asked for?
5. D2 bar for GEN: confirm that a pooled L4 read of about 100 rows is enough, or move the bar to the built family (n about
   700) as a report line.
6. Gap rule of section 6 is my proposal (5 pp per bin, p90 +20%); L-0 may tighten it before the look.
7. Whether the generator's offline run location for the bAbI Lua code is the Mac or a throwaway CPU VM (L-0).

---

## Binding conditions carried from families/G0_APPROVALS.md (copied word for word by the lane builder, Sun 18 Oct 2026; the
build skeptic checks the code against these lines; G1-G10 are already appended in GEN/G0_LITE.md and are not repeated)

### GEN general rows: APPROVE

Binding condition C1. CA-C4 (adjustment set) and CA-C5 (conditional independence) are graph questions. With
deterministic functions and fixed exogenous values, "independent given Z" is not defined. Rows of these two forms state
that the exogenous variables are independent random inputs and that the question is about the stated graph. They give
no fixed exogenous values. Gold = d-separation / backdoor validity on the graph (A and B as written).
Rulings: 1 the confirm rule is approved for GEN (G5), and GEN's GBT probes count as written. 2 see G2 (the G-H1 rule as
written is approved). 3 sub-block independence is approved (GEN is not P0; G4). 4 the 600 dev rows are never trained on;
L-0 decides whether they merge into mixdev. 5 L-0 confirms C2's general-type render shape before generator code
freezes. 6 GEN as a VOICE source (<= 5%) is included by default. The domain list is name-only and L-0 may replace items
after the G-name intersection without re-approval.

### Round 2 lines for GEN (verbatim)

- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- GEN: C1 (CA-C4/CA-C5 rows state independent random exogenous inputs; graph gold).

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: APPROVE (no must-fix).
Binding conditions: GEN-B1 point 1: the split stands. GEN-B2 point 2 confirmed (task-defined classes in the mix; NOTA-GENERIC out).
GEN-B3 point 3: yes, S-pre and S-post 8.5 per TP generator on a fixed seeded sample of 2,000 generated instances written before
the stage, once per stage. GEN-B4 point 4: no names exemption; fewer than 8 admissible RG tasks = G-T3 fails and TP-RG rolls alone
(rows back to the original sub-blocks within +25%). GEN-B5 points 5-6 confirmed (gap rule may be tightened before the look, never
loosened); point 7 is L-0's. GEN-B6 the RG allow-list, DM module list and bAbI task list are names-only additions due Fri 23 12:00
(manifest v1.2).
