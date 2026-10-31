> **Ruling A70 (DRAFT, pre-result; 17 Oct 2026 ~17:15 UTC; orchestrator ruling author, Opus; T37b-dev frame source and build, spec 3.18 / 7.1 / 7.2 (d); no bar, gate or cap loosened; nothing relabelled; no model has read any T37b-dev row).**
> - **(a) Decision.** T37b-dev is rebuilt for C2 with NEW held-out frames authored now (Haiku, G-LEX 2/2). The 33 A48-F7 held-out patterns are NOT reused. A48-F7's use record ("used only for the G-proxy's 150 complement pairs, <= 5 per pattern, and the symmetrisation probe") stays as written. Pre-gate (d) stays on T37b-dev and is not re-pointed to the G-proxy pairs. Its bar is unchanged: complement violation C2 < C1 (point), with the CI report-only.
> - **(b) Why (counts and shas).**
>   - (i) The 33 are recorded as single-use, and the G-proxy has already used them up. `data/c2_gproxy/gproxy_pairs_report.json` (sha256 f229e75925a07ab3…) shows 150 pairs on all 30 complement patterns, exactly 5 each, which is the A42-D 7.4 cap. 300 more pairs would need at least 10 more per pattern.
>   - (ii) Independence. (d) is an eligibility condition for each of the 18 grid candidates (A42-D 9.4). The G-proxy pairs feed S (9.3) and the item 10 adoption (10.2). One frame set must not steer all three decisions.
>   - (iii) Held out in substance. The item-7 frame shape that A48 (h) admits is "(Is it | Would it be) + truth word + optional 'to say' + that". It has exactly 44 surfaces. 34 are trained (`TRAINED_CATALOGUE.json` sha256 c6045501…). The other 10 are the frames of the 33 (`HELDOUT_REALISED.json` sha256 92aff6e0…, plus the 3 FRAMES_DEV of G0 S7). Overlap is 0 and no surface is left free. Each of those 10 frames is one opener swap or one "to say" away from a trained frame.
>   - (iv) No existing engine yields a T37b-dev base.
>     - The 9 gate dev splits have 4,329 yes/no rows.
>     - `negtwins.plan.base_record` admits 0 of them: 2,526 have a card format it cannot parse and 1,803 are card-free.
>     - `t37b.select.eligible` in dev mode admits 0: 2,511 have role != aff, 1,418 are not in the T37b registry, 303 have program gold and 97 have Claude gold.
>     - `t37b/builder.py` therefore stays the frozen C3 family code and is not used. It uses FRAMES_DEV and writes into data/.
>     - After the program filters in (d) below, 1,605 role-aff rows remain (31 sources, 1,159 groups). The negtwins parser reads 236 of their cores, so the builder needs a Haiku core path.
> - **(c) Frames.**
>   - Only positive (truth-preserving) "... that" openers are used, and only in the FRAME_NOT form: the frame + the base predicate with exactly one added "not". This is the syntactic form G0 S15 planned.
>   - A48 (h) classes (i)-(iv) bind as rules, checked by program:
>     - no negated interrogative;
>     - no "can/could ... not";
>     - the subject is only the expletive "it", with the opener one of Is it / Would it be / Does it / Would it;
>     - no word from a closed epistemic, evidential or source list;
>     - grammatical.
>   - Further lint, all by program:
>     - 3-8 words, ending in "that";
>     - no "?", "," or "n't";
>     - negcount 0;
>     - no LOCAL_BANS hit;
>     - the normalised surface is not among the 44 surfaces, FRAMES_TRAIN or the seed frames.
>   - Tiers:
>     - Tier A contains none of the 12 item-7 truth words and none of their listed variants.
>     - Tier B is a new shape that does contain such a word. It is a count-triggered fallback only, used only if fewer than 3 tier-A frames are admitted after 2 rounds, and only to reach 3 frames.
>   - The item-7 whitelist (`lexicon.a48h_frame_problems`) still binds item 7 and is not changed there.
>   - G-LEX 2/2. Each frame gets 3 frame-over-core probes (expected "same") and 3 FRAME_NOT probes (expected "opposite"), each read twice independently. Any other pick rejects the frame for good.
>   - A frame with any occurrence in training-side text, or in any existing dev or eval row, is dropped before the freeze.
>   - At least 3 frames are needed. The admitted frames are frozen (sha256 logged) before any base is paired.
> - **(d) Bases.** Rows of the 9 gate dev splits that meet all of these:
>   - qtype noul, with hard gold 0/1 (no gold_probs, teacher or attack_target);
>   - role aff, with exactly one "?" in the instructions;
>   - a card that is empty or does not mention yes/no;
>   - a binary predicate: a natively 2-class source, a one-vs-rest question over a nominal label set, or a program-defined predicate;
>   - never a source with a neutral/middle or ordinal/polar label set, and never LLM-written gold (an unclear source is excluded);
>   - a question with negcount 0 and a core of class DO, COP or HAVE.
>   - Limits:
>     - The base's own aff->neg relations in other dev splits are untouched, because the T37b-dev unit lives in its own split. 1,122 of the aff rows have such a relation.
>     - One pair per base and per group_id.
>     - At most 45 pairs per source (15%) and at most 120 per frame (40%).
>     - Not balanced (G0 A1 precedent).
> - **(e) Pairs and checks (spec 3.18; any doubt drops the pair).**
>   - The partner is the base row with only these fields changed: the instructions (question span replaced by frame + negated predicate + "?"), id, role "complement", gold = 1 - base gold, and meta. The card is unchanged; all 1,122 existing gate-dev complement pairs keep the card too.
>   - negcount must find exactly one added cue on the predicate span, and both program readings must agree. The A43 (f) checks and the G0 H28 scope rule apply.
>   - No trained pattern (379; sha checked) or held-out pattern (33), applied to the base core, may yield the partner. So 10.1 cannot score a violation of 0 by construction.
>   - Two independent Haiku polarity reads must both say "opposite".
>   - A blind Haiku solver answers the base and the partner separately. A pair that is inconsistent or "unsure" goes to a gold-free Sonnet review. It is kept only on "exact"; "not exact" or "unsure" drops it.
>   - The seeded plan (key t37b-dev-a70-v1) is frozen before any read.
>     - The first 300 survivors in plan order are kept.
>     - If fewer than 300 survive, one extension of 150 plan entries is allowed.
>     - If it is still short, the build stops and returns counts. No smaller set is frozen, and there is no fallback to the 33.
> - **(f) Staging and freeze.**
>   - Everything is built under `c2_build/staged/t37b_dev/`. Nothing goes into data/ before the orchestrator's code-edit window.
>   - Outputs: `c2_t37b_dev.jsonl` (300 byte-identical base copies + 300 partners) and `c2_t37b_dev_relations.jsonl` ({a, b, type: "complement"}).
>   - Their sha256 is recorded before any model read, and the files are never edited afterwards. Any change means a new sha, one refresh-dev and a new record.
>   - No model reads T37b-dev before the grid's dev reads (A42-D 9.4). There C1 and the candidates are read in one job (spec 7.2). (d) is read on the candidate's frozen served path (10.4). Jev never reads it. It is never a selection signal (A42-D 6) and never trained. A49 (c) does not apply.
> - **(g) G13 registration (orchestrator, in the code-edit window after batch5).**
>   - Done BEFORE the capture batch, whether or not the file is ready.
>   - `g13_c2.py` C2_DEV gains "c2_t37b_dev" (lean:data/c2_t37b_dev.jsonl), with every field and every method, as for c2_transfer_dev.
>   - A53_TARGETS is unchanged, so no A53 waiver applies.
>   - `mix_c2.py` DEV_SETS gains it.
>   - Backups and CPU tests come first.
>   - The predict manifests and the 18-candidate read plan include it.
>   - Never add the target after the capture batch: refresh-dev refuses a changed target-name list, so that would force a full capture run.
>   - If the file arrives after the capture batch, run one `refresh-dev`, but only after a CPU test shows that the A68 wrapper path keeps its OHS-AC capture record. Otherwise a full capture run is needed.
>   - Units hit only by c2_t37b_dev are expected to be 0. Any hit drops its unit, with no waiver.
>   - Replay pre-clean, the carry runs (F4 F5 F6 F11) and G13 #3 include the target (spec 3.19, 5.4).
> - **(h) Money and rows.** 0 training rows and $0 Modal (A61 e unchanged). Reads run on od-l4b.
> - **(i) Record.** The orchestrator appends this ruling and the three sha256s (frames freeze, plan freeze, final freeze) when they exist. C3 builders treat the A70 frames as held out.

## spec_for_builders
T37b-DEV BUILD SPEC (A70). Lane: c2_build/staged/t37b_dev/. Run from lean/c2_build with ../../.venv/bin/python -B, HF_HUB_OFFLINE=1. No Modal. Never run or import-execute any G13 scan. Never edit g13_c2.py, decontam_g13.py or t37b/*. Never write under data/. Before opening any path, check it with c2io.refusal (skip and count refused paths). Never open a path containing ohs/sealed/preread/quarantine/longbench/jev. Report counts, ids, paths and shas only.

S0. Layout and roles
Folders under staged/t37b_dev/:
- frames/
- bases/
- pairs/
- out/
- tests/

Code:
- Sonnet writes build_t37b_dev.py and tests/test_build_t37b_dev.py.
- A Sonnet skeptic reviews the code before any --write step (A66 a discipline).

Read-only helpers:
- negtwins.core: tokens, split_instruction, parse, has_negation, make_pattern, apply
- negtwins.checks.check_pair
- negtwins.frozen.load_trained (verifies the catalogue sha c6045501…)
- negtwins.heldout.realise (the 33)
- negtwins.lexicon: LOCAL_BANS, norm_frame
- negtwins.probe_bank: DO, COP
- c2_kit.polarity: read, problems
- the negcount kit
- the G0 H28 scope rule in t37b/polarity.py (call it or port it with parity tests)

All Haiku and Sonnet reads follow the A39 (d) reader rules: gold-free chunks of <= 50 items, the TEACH-0 prompt, fresh agents per round, and a file-access audit. Model routing:
- Haiku: authoring, G-LEX, polarity and solver reads.
- Sonnet: code, skeptic review, pair review.
- Opus: none further.

S1. Frame candidates (Haiku, rounds R1 and R2 max)
- Each round drafts 12 tier-A and 8 tier-B positive "... that" openers.
- Tier A contains none of these tokens: true, truly, truth, untrue, untruth, correct, correctly, incorrect, accurate, accurately, accuracy, inaccurate, right, rightly, wrong, false, falsely, falsehood, falsity, mistaken, mistake, case, so.
- Tier B has a new shape and may contain one of them.
- Program lint (frames/lint_R<n>.json). Every condition must hold:
  - the opener is one of Is it / Would it be / Does it / Would it;
  - it ends with "that" and has 3-8 words;
  - no "?", "," or "n't";
  - kit negcount k_all = 0;
  - no LOCAL_BANS hit;
  - no "not" token;
  - no closed-list epistemic, evidential or source word: show(n|s), establish(ed), prove(n|d), confirm(ed), evident, evidence, know(n), believe(d), think, thought, seem(s), appear(s), likely, probabl(e|y), certain(ly), sure, fair, safe, agree(d), claim(ed), said, state(d), argue, suggest, held, assume, presume, doubt, unfounded, accepted, plausible, reasonable, reckon;
  - the normalised surface is not among the 44 item-7 surfaces (34 catalogue frames + 10 held-out frames), FRAMES_TRAIN, C.SEED_* frames or earlier candidates.
- Text scan (frames/scan_R<n>.json): case-insensitive, token-boundary search of each lint-passing frame string. A frame with >= 1 hit is dropped. Scanned text:
  - every training-side text field (instructions, state, card, options) of the files listed as train/seed inputs in each block's newest logs/decontam_counts/c2_cand_<B>.json;
  - the F4/F5/F6/F11 carry pools;
  - the replay pool files mix_c2.py names;
  - the 9 gate dev splits, eval_jagged, eval_opi and data/c2_gproxy/*.jsonl;
  - c2_mixdev and transfer dev, if they exist.

S2. G-LEX 2/2 (Haiku)
- For each surviving frame, use 3 probe-bank cores (DO or COP):
  - probe "same": core vs frame + declarative core;
  - probe "opposite": core vs frame + declarative core with one "not" (FRAME_NOT, via core.apply).
- Two independent reads with separate seeds and chunks. Answer set: same / opposite / neither-or-ungrammatical.
- A frame is admitted only if all 12 picks equal the expected relation. Otherwise it is rejected for good, with no re-vote.
- Choice:
  - all admitted tier-A frames in hash order;
  - if there are fewer than 3 after R2, add admitted tier-B frames in hash order, only up to 3 frames in total;
  - if there are still fewer than 3, STOP and return counts.
- Write frames/admitted.json and frames/FRAMES_FREEZE.json (sha256 of admitted.json, the frame list with tiers, the read files' shas, UTC) BEFORE S4.

S3. Bases (program; bases/eligible.json holds ids and per-reason counts)
- From data/<split>.jsonl for the 9 SPLITS (gate_dev.SPLITS), keep rows that meet all of these:
  - qtype noul, gold in {0,1}, no meta gold_probs, teacher or attack_target;
  - role aff;
  - instructions with exactly one "?";
  - a card that is empty or has no \b(yes|no)\b;
  - a binary-predicate source: natively 2-class, a one-vs-rest question over a nominal label set (topic, intent), or program-defined (pg_*). Excluded: any source with a neutral/middle or ordinal/polar label set (NLI 3-way, stance, emotion/affect, ratings/scales) and any LLM-written gold. The builder decides from the dev builders' provenance and records the rule and evidence per source. If a source stays unclear, a 2/2 Haiku "binary / not binary / unsure" read on its question templates decides; anything short of 2/2 "binary" excludes the source.
- Program baseline: 1,605 rows over 31 sources before the source rule. Provisionally binary: clinc150, banking77, rotten_tomatoes, irony, spam, ag_news, hate, bbc and pg_*, about 1,167 rows. Provisionally out: climate, tb_mixtral, emotion and hard_*. The builder confirms.
- Question span: the substring ending in the single "?".
  - Program path: negtwins split_instruction + parse reads the core.
  - Otherwise, Haiku core path (pairs/core_tasks, for the unread bases among the first 700 in seeded order). Haiku returns (i) the exact question span and (ii) a positive core question parseable as DO, COP or HAVE.
  - Program checks for the Haiku path:
    - the span occurs exactly once;
    - the core's content tokens are a subset of the span's content tokens plus a closed function-word list, after stripping s/es/ed/ing.
  - Program checks for both paths:
    - negcount(span) = negcount(core) = 0;
    - the class is DO, COP or HAVE (MOD is out);
    - the G0 H28 scope rule holds: no quantifier, modal, negation or subordinator in the subject; the auxiliary is in AUX_OK; the rest has no modal; only wide-scope-safe quantifiers; never all/every/each.

S4. Plan (program; bases/plan.json + bases/PLAN_FREEZE.json written before any S5 read)
- Order eligible bases by sha256("t37b-dev-a70-v1|" + id).
- Assign frames round-robin in hash order, skipping a frame whose FRAME_NOT application fails check_pair for that core.
- Partner question = core.apply(core, make_pattern("FRAME_NOT", cls, frame=f, contr="not")).
- Partner instructions = base instructions with the span replaced once.
- Plan-time program asserts (drop the entry on failure):
  - kit negcount: k_all(partner question) = k_all(span) + 1 = 1, and k_syn <= 1;
  - not contracted;
  - c2_kit.polarity.problems(partner core, -1) is empty (A43 f);
  - check_pair is True;
  - no LOCAL_BANS hit;
  - apply() of every trained pattern (load_trained) and every held-out pattern (realise) to the base core never yields the partner question (normalised);
  - the partner instructions differ from the instructions of every row in the 9 dev splits, the G-proxy files and the other plan entries.
- The plan lists every eligible base. S5 reads the first 450 entries; one extension reads the next 150.

S5. Pair reads (any doubt drops)
- (i) Polarity 2/2 (Haiku). Each item is (base span, partner question), with no state, card or gold. Two independent reads; answers opposite / same / neither. Keep only if both say "opposite".
- (ii) Blind solver (Haiku). Each row (base or partner) is shown alone with its state, card and instructions, and no gold. The chunk seeding puts the two rows of a pair in different chunks and different agents. Answers yes / no / unsure.
  - Consistent (exactly one yes) -> pass.
  - Inconsistent or unsure -> (iii).
- (iii) Review (Sonnet, gold-free, no solver answers). Each item is both rows in full. Answers exact / not_exact / unsure, with one line of reason. Keep only "exact".
- Base-gold vs solver disagreement is report-only.

S6. Keep-walk (program)
- Walk the plan order. Keep an entry if it passed S4 and S5 and all of these hold:
  - kept per source < 45;
  - kept per frame < 120;
  - its base id and group_id are unused.
- Stop at 300.
- If fewer than 300 after the first 450 entries, run S5 once on the next 150 entries and continue the walk.
- If still short, or if fewer than 3 frames are in use, STOP and return counts. Freeze nothing.

S7. Rows (program)
- Base: a byte-identical copy of its data/<split>.jsonl row, with the original id.
- Partner:
  - id: "t37bdev:" + sha256(base_id + "|" + frame + "|" + partner_question)[:16];
  - group_id and call_id: the base's;
  - source, state, card and options: the base's, unchanged;
  - qtype: noul;
  - instructions: the partner instructions;
  - gold: 1 - base gold;
  - role: "complement";
  - meta: base meta + twin_of, twin_kind "complement", dev_only true, never_train true, and t37b_dev = {ruling "A70", pair_id "t37bdev_pair:NNN", frame, frame_id, tier, op "FRAME_NOT", cls, core_path program|haiku_core, base_split, seed}.
- Relations: one {"a": base id, "b": partner id, "type": "complement"} per pair.
- Index: pair_id, base_split, base_id, partner_id, frame, tier, cls, core_path, source, group_id, base_gold.

S8. Final program checks (any failure -> no write, problems listed)
- 300 relations and 600 rows; both rows of each pair are noul; partner gold = 1 - base gold.
- Each base equals its source row byte for byte. The partner differs from the base only in id, instructions (within the span), role, gold and meta. The card is unchanged.
- One pair per base and per group. Source <= 45, frame <= 120, >= 3 frames, and every frame is in FRAMES_FREEZE.
- Every S4 assert passes again, and every pair has its S5 decision.
- No T37b-dev id or group is in data/c2_gproxy/*.
- The frame scan gives 0 hits.
- CPU fixture test: gate_c2.relations and gate_c2.complement_stats run on a copy of the out files in a temp root with synthetic predictions. They give n = 300, and gate_c2.complement_rule is not UNMEASURED.

S9. Write (staged only, after the skeptic review)
- out/c2_t37b_dev.jsonl, out/c2_t37b_dev_relations.jsonl, out/c2_t37b_dev_index.json, each with a .sha256 file.
- out/BUILD_REPORT.json:
  - counts per step and reason, per source, frame, class, split and core_path;
  - base yes share;
  - read-file shas;
  - problems (must be [] ).
- out/T37B_DEV_FREEZE.json: the out shas, the FRAMES_FREEZE and PLAN_FREEZE shas, n_pairs 300, n_rows 600, UTC, "no model read".
- The writer refuses any path outside staged/t37b_dev/.

S10. Orchestrator code-edit window (after batch5, before the capture batch; not this lane)
- (1) Back up g13_c2.py, mix_c2.py and tests/test_g13_c2.py to c2_build/_backup_a70_t37bdev/ and log their sha256s.
- (2) In g13_c2.py C2_DEV add:
  "c2_t37b_dev": {"paths": ["lean:data/c2_t37b_dev.jsonl"], "fields": None, "train_fields": None, "note": "T37b-dev (A70): held-out-frame complement pairs on gate-dev yes/no rows; never trained: every field, every method"}
  Replace the docstring line "(c2_t37b_dev removed 16 Oct 2026 ...)" and the comment that says it is not a target. Leave A53_TARGETS unchanged.
- (3) In mix_c2.py DEV_SETS add "c2_t37b_dev": DATA / "c2_t37b_dev.jsonl" and fix its comment.
- (4) Adapt the T37b-dev target test from _backup_a52_t37bdev/test_g13_c2.py: fields None, no A53 waiver, method 6 keys present. On CPU only, run tests/test_g13_c2.py, the refresh tests, tests/test_gate_c2.py and the mix tests.
- (5) If out/ is frozen, cp the two out files and their .sha256 files to data/ and verify the shas against T37B_DEV_FREEZE.json.
- (6) Then write the merged mixdev.
- (7) Add c2_t37b_dev (600 rows) to the pre-gate predict manifest and the 18-candidate od-l4b read plan, with C1 in the same job.
- (8) Capture batch.
- If the file was not ready at (5):
  - copy it in later;
  - before relying on refresh-dev, run a CPU test that the g13_c2_opt3.py --ohsac-report-only A68 path through refresh-dev keeps the A68 capture record (drop_ids_by_class);
  - then run refresh-dev --check, then one refresh-dev;
  - otherwise run a full capture.
- Never add the target after the capture batch.
- Report units hit only by c2_t37b_dev (expected 0; a hit drops its unit).
- Replay pre-clean, the carry runs and G13 #3 include the target.

S11. Stop rules (return counts to the orchestrator)
- Fewer than 3 frames after R2.
- Fewer than 300 pairs after one extension.
- Any S8 failure.
- Any refused-path access or audit hit.
- Never fall back to the 33. Never write into data/.

S12. Usage estimate
- Haiku: about 55-70 chunk tasks (frames + G-LEX about 8, cores about 12, polarity about 18-21, solver about 18-24, source reads if needed about 2).
- Sonnet: review 1-3 chunks, plus builder and skeptic.
- Modal $0.