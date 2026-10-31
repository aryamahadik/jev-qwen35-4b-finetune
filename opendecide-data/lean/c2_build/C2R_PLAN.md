# C2R plan (17 Oct 2026; Opus synthesis after 3 plans, 2 judges, 1 skeptic, revised)

## name
C2R-v2: a clean-room, general-first rebuild of C2 that runs only if the owner chooses it in words (D1). OHS-4 is the primary test and OHS-5 the confirmation. Every sealed bar, every pre-gate bar and ship rules S1-S6 stay binding, and every rule C2R changes is listed for the owner. One shot, 4B, continuing C1.

## summary
WHAT C2R IS
- One training run that continues C1:
  - Qwen3.5-4B, with C1's LoRA continued through init_adapter, r16.
  - The spec 9.1 recipe is unchanged.
  - The result is merged to bf16 and served on SGLang S1.
- It runs only if the owner picks it in words (D1).
- The other branch is K, which keeps the adopted rules. C2 does not train, and a frozen "C1-served" config gets the single OHS-4 read against Jev.
- Sources of the design:
  - The integrity plan's clean-room design is the base.
  - The accuracy plan gives the levers for general accuracy.
  - The newtest plan gives the OHS-5 build order, the L5 timing method and the claim statistics.

WHAT STAYS BINDING (unchanged)
- OHS-4 (frozen 13 Oct, unspent, built blind) is the primary test. L1 comes first, then J (two pinned Jev runs, spec 8.5 and 9.2).
- The OHS-AC union binds every admission check literally (A64 a). The union record is met.
- These all stay as written:
  - pre-gate bars (a)-(d), including D9;
  - S1-S6;
  - the spec 8.6 claim rules;
  - the A42-D 9.5 choice rule and 9.6 "one candidate";
  - the A42-D 11 SPEED-3 method;
  - the A42-D 13.8 Jev order and its stage-funding rule;
  - the A61 money caps and payers;
  - every never-probe rule.
- Rules are only ever added, and only when stricter.

WHAT C2R CHANGES (the owner's D1 words must cover each one; shown neutrally per A64 i)
1. New public sources enter training, as one pre-committed batch.
2. The A62(c)/A64(f) floors are replaced by R-new floors that are at least as strict.
3. Fixed A68 shares replace A37(d)'s 40/60 new/replay split.
4. Pre-gate changes:
   - (a) is re-pointed to the R-new mixdev;
   - (d) is re-pointed to a Fresh-Dev complement set if T37b-dev no longer exists;
   - a stricter check (e) is added.
5. A42-D 9.3's selection score uses the Fresh-Dev and R-new mixdev select halves, because the G-proxy is unmet (A61 f).
6. No T-family row or template is trained. The T-blocks and the A60 hold file stay on disk for C3.
- D1(b), decided separately: serving dials that change answers count as model changes and need the owner's words. Speed-only dials keep the 99.5% parity bar.
- The earlier headline "no gate, bar or claim rule is loosened" is withdrawn. C2R changes gates after a result, so it is the owner's call.

THE THREE PARTS
(1) General accuracy (the measured gap is transfer to fresh sources).
- One batch of 100-140 new public sources with human, official or program gold. A fresh, untainted Opus session picks them.
- Each source gets one whole-file 8.5 check before any mapper exists. A HIT bars the source, and the source is never replaced.
- The surviving sources are split 80/20 by source into training and a leave-source-out Fresh-Dev, which has select and gate halves.
- C1's reads drop whole units that C1 already knows and give double weight to units it gets wrong.
- Complement and negation twins are added; they must pass G5-H.
(2) Rule/agent, which pre-gate (a)/(b) and ship rule S1 need.
- About 72K program-gold rows from at least 12 NEW generator families, written blind across the 9 owner categories.
- Sonnet writes the code, Haiku writes all the wording, and solver B comes from a separate session.
- Formats come only from C2's pre-A38 format pool plus invented formats.
- No T-family code, templates or wording is used. The full spec 6.3 gate kit applies at unchanged bars.
(3) Serving.
- Speed-only dials must reach 99.5% or more same-argmax parity on the full 8,143 set.
- Dials that change answers are used only under D1(b): one frozen procedure, fit on select halves only, applied the same way to C1-served and C2R.
- Everything is sha-frozen before the first look, including a pinned C1-served fallback.

HONEST OUTLOOK [proj]
- P(the stop rule fires before GO #1) ≈ 0.4. P(pre-gate passes | trained) ≈ 0.6. P(S1-S6 pass | look) ≈ 0.5. So P(C2R ships) ≈ 0.15 (0.1-0.25).
- C2R − C1 on fresh sealed general ≈ +0.5 to +1.0 pp (80% range −0.5 to +2.5).
- Shipped model − Jev on OHS-4 G ≈ −4 to −5 pp.
- P(the OHS-4 "close" rule passes for the shipped model) ≈ 0.25. P("within 3 pp" on OHS-5) ≈ 0.02-0.03.
- Likely wins: end-to-end p50/p95, ECE, option-order drift, attack success. Rule/agent only if S1 passes.
- Cost at the pre-registered 40% utilisation is a likely loss.
- No plan can honestly promise "within 2-3 pp AND better on every other metric", and every report says so.

OWNER INPUT
- D1 (K or C2R, plus D1(b)), D2 (OHS-5), D3 (one H100 window of at most 1 h and $5).
- Then GO #1 and GO #2. At GO #2 the owner may name an optional Jev top-up.

## owner_decisions
How these are shown: the orchestrator presents them neutrally, with no request and no recommendation (A64 i). Only the owner's own words count.

D1: K or C2R.
- K keeps the adopted rules:
  - C2 does not train;
  - C1-served is frozen;
  - OHS-4 is read once for C1-served vs Jev;
  - the T-blocks go to C3.
- C2R needs the owner's words to cover these changes:
  1. New public sources enter training (one pre-committed batch of 100-140).
  2. The A62(c)/A64(f) floors (agent core ≥ 5 of 6; ≥ 10 program families) are replaced by R-new floors:
     - at least 10 generator families with 600 or more rows each;
     - at least 5 of 6 agent-core generators with 1,000 or more each;
     - 4 of 4 agent categories with 1,000 or more;
     - at least 7 of 9 categories with 600 or more.
  3. Fixed A68 shares replace the 40/60 new/replay rule.
  4. Pre-gate changes:
     - (a) re-pointed to the R-new mixdev, at the same +8.0 with LB > 0;
     - (d) re-pointed to a Fresh-Dev complement set if T37b-dev is gone;
     - a stricter (e) added.
  5. The A42-D 9.3 selection score uses Fresh-Dev and the R-new mixdev.
  6. No T-family is trained.

D1(b), separable: answer-changing serving dials count as model changes for whichever model ships.
- The dials: yes/no type bias, ordinal expected-value decoding and symmetrisation.
- If no: only speed-only dials and temperature.

D2: build OHS-5.
- Yes: about 5 more days, and replication and "within 3/2 pp" claims become possible.
- No: general claims rest on OHS-4 alone.

D3: one H100 window for SPEED-3/L5.
- At most 1 h and $5, on mahadikarya3 unless the owner names another account. This is an exception to "Modal = training only".
- No: SPEED-3 runs on the L4, labelled as such.

GO #1: training spend.
- Payers: the mahadikarya2 → mahadikarya3 relay only.
- Spare accounts or aryamhd only by a ruling that names the amount.

GO #2: the looks and the Jev stages.
- Optional: a named OpenRouter top-up if stage 6 (OHS-5 J) does not fit.

OPTIONAL: ejs-5 and JevBench sealed ($49). Only for a general-win claim, and no submission.

NOT PROPOSED (owner-only; would change standing rules):
- a split-aware deny-list (it would loosen A61 b);
- a base larger than 4B (the 4B/2B rule).

## sealed_test_strategy
A. PRINCIPLE
- Every existing sealed test binds exactly as frozen.
- C2R is disjoint by construction where we write the text, and by the binding run-only checks everywhere else.
- No bar moves after a result. Rules are only ever added, and only when stricter.
- Every C2R change to a gate is on the D1 list, in the owner's words.

B. OHS-4: PRIMARY (A38; frozen 13 Oct; 6,213 calls: G 2,883 / R 1,454 / U 433 / X 281 pairs / consistency 881)
- Under D1, C2R takes C2's single L1 slot: C1-served + C2R in one job.
- J is Jev once, after the L1 verdict, in two pinned runs.
- Unchanged:
  - pre-gate (a)-(d), with (a) re-pointed at the same +8.0 and LB > 0, plus the stricter (e);
  - S1-S6, with the pre-registered group_id bootstrap;
  - spec 8.6.
- If the pre-gate fails, OHS-4 is read once for C1-served vs Jev (A37 g).
- R stays a transfer test.
  - R-new uses only C2's pre-A38 format pool plus invented formats.
  - It excludes the 8.3 examples and the Federal Register, eCFR and EDGAR texts.
  - The structure-hash overlap with OHS-4 is reported as counts (8.3).
  - We do NOT claim that this keeps 8.3's 40% rule true, because OHS-4's actual syntaxes are unknown to us.
- SPEED-3 uses the frozen OHS-4 request file (A42-D 11.3).
  - It is part of L1/J, stores timings only, and no response body is kept or scored.

C. OHS-AC (14,407 calls; union of 27808b0c and fadec66f; suite c2dfefa6)
- The union binds every C2R G13, G-TPL and A64(e) check literally.
- What C2R trains:
  - no T-family;
  - none of their code, templates, packs, lexicons, wordings or samplers;
  - no coding rows.
- Held-out dimensions that PREREG 13.1 states in words are excluded by program assert:
  - no 7-8-step plans;
  - no trace fault-type item kind;
  - invented names only, never registry or naming-style names.
- Held-out VALUES that exist only in HELD_OUT_* lists cannot be excluded blind. They are covered only by the A64(e) literal check and G13/G-TPL.
- So C2R's A1/A2 results carry the label "transfer; unnamed held-out values checked by literal and hash checks only".
- WIN, DOMINATE and General stay as pre-registered. An unrun stage is handled per 13.8.
- The provenance defect is printed with every result.

D. OHS-5 (new; only if D2; brief sha in A68 before any C2R row)
Build:
- Fresh sealed session. It reads only the brief and the hash lists.
- Disjoint from DECL (program hash check), C1's sources, every earlier sealed or eval source, the bench list and the deny-list.
- Publisher, host and multi-word-name collisions with DECL are cleared before the freeze.
G5 (about 8,000 items, floor 6,000; rules copied from OHS-4 8.3, rationale recorded):
- yes/no 40-50% of items, with gold yes at 50%;
- at least 30% card-free;
- 2-8 options;
- at least 4 non-adjacent domains hold at least 50% of items, and no domain is above 15%;
- a 200-item noise-floor read per domain; a domain above 8% clearly wrong is dropped whole;
- leak filters, MinHash dedup and group_id splits;
- gold only from humans, officials or programs;
- only the scale differs from OHS-4: at least 20 sources, at most 500 items per source.
- A report-only freshness stratum.
K5: 1,200 complement pairs, with at least 150 frames written by sealed Sonnet, plus 800 option-order permutations.
X5: 400 attack/benign pairs from fresh sealed templates.
- No R part.
Exports:
- 10/12-grams, exact_full, sentences, substrings of at least 60 characters, MinHash ≥ 0.8 and structure hashes.
- Keywords: only dataset-specific identifiers (multi-word names; single tokens of at least 5 characters with Zipf < 3.0; upstream ids; URL paths). Never generic hosts or licence URLs.
- Audit: 0 failing entries.
At the freeze:
- reverse decontamination, returning k only;
- the spec 8.1 12-gram no-spillage re-scan.
After the freeze:
- hits drop training units, never OHS-5 items;
- a final-mix 8.5 HIT still drops the C2R source and is also logged as an OHS-5 build defect.
Look log:
- one L1 (C1-served + C2R), opened only if OHS-4 L1 shipped C2R, before any Jev call;
- one J (two pinned runs), as stage 6.

E. CLAIMS AND STATISTICS (fixed in A68)
- Paired by item, 10,000 resamples, seed 0. Two CIs are printed:
  - the pre-registered one, clustered by document (G) or pair (K/X);
  - a two-stage one (source, then document).
- Each claim uses the CI that makes it HARDER to pass:
  - "close" (CI includes −2) uses the CI with the lower upper bound;
  - LB-type claims use the lower LB;
  - the harm veto fires on either CI.
- Few-cluster caveat: OHS-4 G has about 9 sources.
- G claims use the Jev run that scores higher.
Ladder:
1. "Close to Jev on general" (OHS-4, spec 8.6).
2. "Close (replicated)": also passes on OHS-5. Otherwise "OHS-4 only".
3. "Within 3 pp": OHS-5 LB > −3.0 AND OHS-4 point ≥ −3.0.
4. "Within 2 pp": only after 3, with −2.0 in both places.
Wording rule:
- The point estimate and both CIs are printed next to every claim.
- "Close" is never headlined alone and never paraphrased as "within 2 pp".
- Think mode stays out of every headline.
Other metrics:
- Holm over 8 metrics: ECE, Brier, complement violation, option-order drift, attack success, e2e p50, e2e p95, and $/1K at 40%.
- "Better on every other metric" only if all 8 pass. Any metric significantly worse is printed as worse.
- Rule/agent: OHS-4 R LB > 0 in both pinned runs.
Harm veto (unadjusted): C2R is withdrawn if C2R − C1 on G5 has UB < −1.0.

F. NEVER-PROBE RULES
- Only the orchestrator runs 8.5, G13, G-TPL and A64(e): whole-file, once per stage, on fixed inputs.
- Tools print block and kind counts only. Hit ids stay inside the drop step.
- None of these:
  - analysis of dropped vs kept units by token, word, frame, length or source;
  - any reweight that uses them;
  - edits after a sealed check;
  - refill;
  - use of per-source survival.
- The taint register binds, and breach outputs are never cited.

G. OTHER TESTS
- OHS-3 is spent; it stays a G13 and deny-list target only.
- Report-only: OHS-1/2, SOB, Nimble, ejs-5, JevBench public, the DI sample.
- The vision side-bench is used once as a veto.
- No submission.

## data_strategy
KSAFE: the C2R-side vocabulary policy, fixed in A68 before any row. Nothing in it comes from hits.
(1) Generated text: every entity, tool, product, organisation, person and place slot is a seeded invented word.
- At least 6 characters, not a dictionary word.
- No real names, URLs or hosts.
(2) Real text: one deterministic scrub, applied to every row the same way.
- It removes URLs, hosts and emails, plus the row's own 8.5 identifiers.
(3) The A63 avoidance list is NOT used, because it was hit-informed. The binding keyword check still drops every hitting unit.
(4) No length cap on G real text. R-new has at least 30% of units over 120 words. No length reweight.
(5) Frame diversity: at least 12 card wordings and 12 instruction wordings per generator, all written by Haiku.
(6) Over-generation: R-new 4x and G 4x, from block-level counts only. Disclosed.
- Honest limit: KSAFE makes identifier slots safe by design. It does not make ordinary English safe.
- The rest is a drop-only tax that falls hardest on long units. Block-level survival: GB 17%, GW 19%, F4 19%, MD 61%, replay 31%.

REUSE (upper bounds; the final-mix G13 and the single final-mix 8.5 run bind)
- MD 6,359, SB5 1,039, GW 1,016, F4 1,010, GB 947, F11 336, I10 29: about 10.7K rows.
- Minus every source the step 0(d) form-shopping bar removes. All through the A66 writers.
- Replay: 25,245 of 81,209 survive.
  - The A46 screen runs first.
  - Replay is used as is, with no reweight. Disclosed limitation: keyword survival skews its mix.
  - KD through the C1 anchor.

NEW
(a) R-new: about 72K program-gold rows.
- At least 12 generator families across the 9 categories, 6 of them agent-core.
- Formats: C2's pre-A38 pool plus invented formats.
- The full gate kit applies.
- Expected 12-36K admitted, subsampled to an 18K target.
(b) G-breadth: one batch of 100-140 sources.
- About 70-100 are expected to pass 8.5, and 80% of those go to training.
- At most 150 rows per task-source; about 50K built; about 9-20K expected admitted.
- Type weights are set by the fresh session from C1's weak spots on non-sealed sets:
  - 4+ long options (61% vs 91%);
  - ordinal (Nimble score 68.8, SST-5 −9);
  - abstain (SQuAD2 yes-bias 65%);
  - typed decisions.
- Those sets become report-only.
- The deny-list stays split-unaware.
(c) Twins: within the A60 caps; the twin block must pass G5-H.
(d) Weighting: C1-wrong units ×2 (cap 2x), from C1 reads only. Nothing else is weighted.

TARGET MIX (D1 item 3)
- At most 66.5K rows, with the 50K floor.
- R-new 18K; G 22K (new about 12K plus reuse up to about 10.7K); twins within the caps; replay 20-25K.

STOP RULE (pre-registered; no refill and no second round)
Stop and report before GO #1 if any of these holds:
- R-new is under 9K rows;
- fewer than 10 generator families have 600 or more admitted rows;
- fewer than 5 of the 6 agent-core generators have 1,000 or more;
- any of the 4 agent categories is under 1,000;
- fewer than 7 of the 9 categories have 600 or more;
- G is under 12K, new G comes from fewer than 20 training sources, or G covers fewer than 8 domains;
- replay is under 20K;
- the total is under 50K;
- Fresh-Dev has fewer than 1,000 items or fewer than 12 sources;
- any final-mix check is incomplete.

DEV (never trained)
- Fresh-Dev with its select and gate halves, plus its complement set.
- The R-new mixdev, with select and gate halves.
- Transfer dev T19 + T21: 600 rows, sha 2b9702a7…. T36 and T20 are out.
- The 9 gate-dev splits (8,143 rows, devsel halves), _perm, jagged and OPI.
- D2 re-derived using C2R's files.
- The 2,000-row old slice, used only for the snapshot stop rule.

OUT
- All T-family rows and templates (C3), and the A60 hold file.
- DI blocks.
- F5 and F6.
- md_fdc, md_peps, SB6, every barred source and every source barred in step 0(d).
- Location: data/c2r_parts/. Every glob excludes data/ohs3*, ohs3_parts/, ohs4_sealed/, ohs_ac_sealed/, data/ohs5* and ohs5_sealed/.

## training_strategy
RECIPE (spec 9.1, unchanged; no new trainer code)
- Start: continue C1's LoRA through init_adapter (q35_4b_main500k, 507d1c29…; base Qwen3.5-4B @ 851bf6e8).
- LoRA: r16, alpha 32, dropout 0.05, QWEN35 targets, expect_trainable 32,464,896.
- Optimiser: AdamW, weight decay 0, clip 1.0, batch 16, micro_tokens 8192.
- Schedule: peak LR 5e-5, 5% warm-up, cosine to 0, exactly one pass.
- Losses: C1's, unchanged:
  - CE with label smoothing 0.05 (MNLI 0.08);
  - KD 0.5 only through the C1 anchor on replay;
  - complement/equiv at lam 1.0 with sym_cons;
  - lam_inv 1.0;
  - perm_twin 0.3 with lam_p 0.5;
  - lam_ord only on replay ordinal rows.
- Hard 0/1 labels on every new row.
- Seed: new, fixed in A68.
- Prompt: the one A68 layout. The rendered-prompt sha is identical across trainer, gate and server.

WEIGHTS
- C1-wrong units ×2. Through the trainer's existing per-row weight field if it has one.
- Otherwise each such unit is duplicated once in the mix, counted inside the 66.5K cap. No trainer edit.

CHECKPOINTS AND STOPS
- A checkpoint at every 10% (A42-D 9.1 allows 6-10). Resume from the last one on mahadikarya3.
- Snapshots at 25/50/75% are monitors only.
- Spec 10.4 stop rules:
  - abort on a non-finite loss;
  - stop if the old slice is below C1 − 1.5 pp at both 25% and 50%;
  - the P(yes) alarm.

SELECTION (A42-D 9, grid unchanged)
- The grid is three bases (final step, last-3 average, early+late average) × α ∈ {0.5, 0.6, 0.7, 0.8, 0.9, 1.0}, computed in merged-weight space.
- 9.5 rule: the final step stays unless the best eligible candidate's gain in S has LB > 0. A68 adds that it also needs a point gain ≥ 0 on the gate halves.
- S = the mean of Fresh-Dev and R-new mixdev select-half accuracy (D1 item 5).
- 9.6: one candidate.

NOT CHANGED, ON PURPOSE
- No r64/r128, no Brier-loss variant, no LR change.
- None of these has a pilot, and Modal is for training only. They stay C2.1/C3 items.

COMPUTE
- Modal H100, one run, about 4,100 steps at 66.5K rows.
- Expected 2.8-3.2 s/step (about 3.2-3.6 h); pessimistic 3.72 s/step (about 4.2 h).
- Relay mahadikarya2 → mahadikarya3. One adapter backup, and a local copy of the new model only (no duplicates).

## serving_strategy
SERVED PATH
- SGLang S1, bf16 merged weights, with the one A68 layout.
- Parity: the served path vs the HF adapter read on dev must reach ≥ 99.5% argmax agreement (spec 7.3), on the hardware used for the scored reads (free L4).

SPEED-ONLY DIALS (need ≥ 99.5% same-argmax parity on the full 8,143 set, tested on C1 first per the owner's 17 Oct rule)
- The exact batch-1 bundle: /v1/score, input_ids, skip tokenizer init, LM-head slice to option rows, the GC fix.
- The static-first layout with prefix reuse, only if it passed parity before A68.
- FP8 with a margin-gated BF16 fallback. τ is fit on the select half; the offline replay showed 99.92-99.96% agreement.
- A margin-gated second option-order view, skipping the second order when the margin is high.
- Keep-alive warm container, serving near the caller, admission control and a capped batching wait.

ANSWER-CHANGING DIALS (only under D1(b); model changes)
- yes/no bias correction per item type.
- Expected-value decoding for ordinal and score items.
- A42-D 10 symmetrisation, using the Haiku frame catalogue, with its adoption test re-pointed to Fresh-Dev plus the dev-only frames.
How they are fit:
- One frozen procedure, fit on the select halves only.
- Never aimed at any sealed set's documented base rate.
- At most 4 nested configs.
- Adopted only at ≥ 1 SE gain on both the select and gate halves.
- C1-served and C2R each get their parameters from the same procedure.
- D9 (p50 ≤ 1.05 × C1) is re-measured with every adopted dial on.

CALIBRATION
- The temperature is fit on the R-new mixdev and Fresh-Dev select halves. It does not change argmax.

FALLBACK
- C1-served is sha-frozen in step 7 (under K, right after the owner's words). It is what serves if C2R stops, fails the pre-gate, fails S1-S6 or is vetoed.

HARDWARE AND SPEED-3
- Scored reads run on the free L4.
- Under D3, the SPEED-3/L5 headline runs on one H100 window: at most 1 h and $5, with an in-code guard, during Jev stage 1 only.
- The measured H100-vs-L4 argmax agreement on dev (earlier 99.32%) is printed.
- If D3 = no, SPEED-3 runs on the L4 and is labelled as such.
- Cost = hourly price ÷ (0.40 × T_sat × 3,600) × 1,000, with T_sat taken at c = 64/128 (A42-D 11.1).
- A utilisation table (20/40/59/100%) is always printed.
- Measured 17 Oct: Jev $0.0234/1K; C1 is cheaper only above about 59% utilisation on H100.

MULTIMODAL (no fine-tune)
- Voice: Nemotron Speech Streaming 0.6B with VAD and end-of-turn, feeding the frozen model. Latency is reported after the end of speech. No claim vs Jev, which is text-only.
- Image: the native Qwen vision tower. The vision side-bench is run once as a no-harm veto. It stays behind (77.7 vs 85.1).
- Think mode is out of every headline.

## timeline_cost
TIMELINE (assumes D1 on Sun 18 Oct)
- Sat 17 Oct: step 0.
- Sun 18 - Tue 20: steps 1-2.
- Wed 21: step 3 (sources).
- Thu 22 - Tue 27: OHS-5 build and blind code, in parallel.
- Wed 28 Oct - Mon 2 Nov: rows and the full gate kit.
- Tue 3 - Wed 4: C1 reads and the C1-served freeze.
- Wed 4 - Thu 5: admission (G13 runs serially).
- About Thu 5 Nov: GO #1.
- About Fri 6: training, after the 1 Nov credit renewal, with T_core re-read live.
- Sat 7 - Sun 8: select, gate, freeze.
- Mon 9 - Tue 10: GO #2 and the looks.
- About Wed 11 Nov: report.
- If D2 = no: about 4 days sooner.
- Under K: the OHS-4 C1-served vs Jev read lands within about 2-3 days of the owner's words.

MODAL (A61 e: C2 total ≤ $40; training ≤ T_core)
- Training: about $15-17 expected; $19.3 pessimistic; one resume adds about $2-2.5, so the worst case is about $21.8.
- Compare with T_core ≈ $22.96 (stale; re-read live). The reserve is thin, and the spec 5.5 trim applies if needed.
- D3 window: at most $5.
- No Modal for reads.

OPENROUTER (cap $10, about $7 left; re-read live)
- OHS-4 J: about $0.5-1 (spec 9.2).
- OHS-AC plus anchors: about $4-6 (13.8 estimate).
- OHS-5 J: about 24K calls, projected from the measured cost per call (17 Oct measure: about $0.023 per 1K short decisions; longer items cost more). It may need a top-up that the owner names.
- Stage funding follows the 13.8 rule only.

$0 RESOURCES: the free L4 (od-l4b), od-cpu1 on GCP credit, and the CPU.

CLAUDE USAGE
- Heavy: fresh Opus, Sonnet and Haiku sessions for A68, sources, OHS-5, generators, mappers, wording and reads.
- Haiku does bulk work, Sonnet code, Opus rulings.
- Stop new work at 96%, and ping the owner at 96% (they have a manual reset); never cross 98%.

OPTIONAL: ejs-5 about $0.5; JevBench sealed $49 (owner only).

## expected_results
All figures are projections [proj] unless marked measured.

CHAIN
- P(the stop rule fires before GO #1) ≈ 0.4 (0.3-0.5). Main causes: the keyword wall on long units, and the full gate kit cutting R-new generators.
- P(pre-gate passes | trained) ≈ 0.6.
- P(S1-S6 pass | look) ≈ 0.5.
- P(no harm veto) ≈ 0.9.
- So P(C2R ships) ≈ 0.15 (0.1-0.25).

GENERAL ACCURACY
- C2R − C1 on fresh sealed general: about +0.5 to +1.0 pp (80% range −0.5 to +2.5).
- D1(b) dials, if approved, might add about +0.3 to +1.0 to both models. This is to be measured on the select halves in step 0/7.
- C1-served − Jev on OHS-4 G: about −4.5 to −5. Basis (measured): OHS-3 −5.3; text side-bench −1.7, not significant.
- C2R − Jev: about −4 (80% range −6.5 to −1.5).

CLAIMS (for the model that ships)
- OHS-4 "close" passes ≈ 0.25. With C2R as the shipped model ≈ 0.07.
- Replicated on OHS-5 ≈ 0.05.
- "Within 3 pp" ≈ 0.02-0.03; "within 2 pp" ≈ 0.01-0.02.
- At or above Jev ≈ 0.02.

OTHER METRICS
- Likely wins:
  - e2e p50/p95 (measured C1 137 vs 156 ms and 162 vs 224 ms, 100 pairs, with qualifiers);
  - ECE (measured 3.3 vs 6.0);
  - option-order drift;
  - attack success;
  - rule/agent, only if S1 passes.
- Uncertain: Brier, complement violation.
- Likely loss: $/1K at 40% (measured: C1 is cheaper only above about 59% utilisation on H100; the L4 basis is to be measured).
- P(all 8 Holm metrics pass) ≈ 0.02.
- Vision stays behind (77.7 vs 85.1). Voice is attached, with no claim.

WHAT THE OWNER GETS IN EVERY BRANCH
- A sha-frozen C1-served model with the best measured speed-only dials, plus the D1(b) dials if approved.
- One honest sealed general-gap number vs Jev, with point and both CIs.
- The SPEED-3 latency/cost results.
- C2R replaces it only if every binding rule passes.

## risks
SKEPTIC PROBLEMS: WHAT CHANGED, OR WHY NOT
1. Partly valid.
- Fixed: the "nothing loosened" headline is removed. The selection-score inputs, the pre-gate re-pointing and the answer-changing dials are now D1 items, and the layout is fixed before step 7.
- Rebutted: α and checkpoint averaging are not a new blend. A42-D item 9 was adopted 15 Oct, before any C2 result. It explicitly changed A37(a)/(g) and pre-registered the 18-candidate grid, the 9.5 rule and 9.6 "one candidate". C2R uses that grid unchanged.
- Rebutted: FP8 is a speed-only change held to the owner's 99.5% parity bar. It is one served path, the same logic as A42-D 10.4, not a second candidate.
2. Valid. Fixed: D1 item 2, with the floors mirrored at least as strictly.
3. Valid. Fixed: one layout in A68, used everywhere.
4. Valid. Fixed: both reweights are deleted.
5. Valid. Fixed:
- disclosures D-a to D-e;
- the taint register covers FACT A readers, the replan chain, this reviser and the skeptic, and the orchestrator if it read FACT A;
- fresh sessions work from the clean packet.
6. Valid. Fixed: Haiku writes all wording, Sonnet writes code only, and solver B comes from the format spec in a separate session.
7. Valid. Fixed: formats are restricted, overlap counts are reported, and the "keeps 40% true" claim is withdrawn.
8. Valid. Fixed: the outlook is chained, P(stop) is stated, and the gains are cut.
9. Valid. Fixed: the 13.8 order is kept, OHS-5 J is stage 6, and a named top-up is available at GO #2.
10. Valid. Fixed: OHS-5 L1 and the veto come before any Jev call.
11. Valid. Fixed:
- L5 runs only in stage 1 (A42-D 11.3 already says this);
- D3 is capped at 1 h and $5;
- 10% checkpoints with resume;
- the worst case includes one resume;
- the credit dates are checked in step 0(b).
12. Partly valid.
- Fixed: response bodies are dropped in code, request logging is off, and extra QPS tests run on Fresh-Dev.
- Rebutted: the pre-registered SPEED-3 levels stay on the frozen OHS-4 request file (spec 8 title; A42-D 11.3). They are part of L1/J and are never scored or stored, so they are not an extra look. Moving them would change a pre-registered method and break the token-count match with Jev's stage-1 read.
13. Valid, with one limit.
- Fixed: dials are tuned on select halves only, with at most 4 nested configs and the 1-SE rule.
- Limit: pre-gate (c1) still reads the full 8,143 set as pre-registered. The gate-half reading is added beside it, never in place of it.
14. Valid. Fixed: D1(b), and D9 is re-checked with all dials on.
15. Valid. Fixed: the C1-served freeze in step 7, or right after the owner's words under K.
16. Valid only as D1(b). The dials come from one procedure fit per model on select halves, and are never fit toward OHS-4's documented yes share.
17. Valid, with a correction. "More conservative" must mean the CI that makes each claim harder.
- A wider CI makes "close" (CI includes −2) easier, so "close" uses the CI with the lower upper bound.
- S1-S6 keep the pre-registered bootstrap; the two-stage CI is printed beside them as report-only.
18. Valid.
- Fixed: (a) G5 rules copied from 8.3; (b) DECL as hashes only; (d) the 12-gram re-scan; (e) the glob and path-guard exclusions are added first.
- (c) partly: after the sealed-side clearing, a HIT still drops the C2R source, because 8.5 binds and that is the stricter choice. It is also logged as an OHS-5 build defect.
19. Valid. Fixed: the step 0(d) records check. The G floor is re-checked before step 3.
20. Valid as far as visible. Fixed:
- the twin block gets the G5-H gate;
- selection acts on whole units;
- A64(e) runs on all dev rows;
- the held-out claim is narrowed to the dimensions PREREG 13.1 states in words.
- Input limit: the problem list was cut off partway through #20. Any later items must be checked against this revision.

DISCLOSURES (step 0 c)
- D-a: a planning agent joined drop ids to unit lengths. It is never cited and sets no number.
- D-b: FACT A computed per-source replay survival, which is hit-informed. All its readers are barred.
- D-c: a non-orchestrator agent ran an unlogged scratchpad driver calling ohsac_stage, and a real `candidates --ohsac-only` run on the DI blocks A61(c) had already ruled OUT. This went against plan F and A64(g).
- D-d: the skeptic's text quoted per-source figures and hit words. The skeptic and this reviser are barred, and this plan repeats neither.
- D-e: the earlier A61(d) and A64 breaches, the 09:00 UTC read-only Modal calls, the OHS-AC provenance defect, and G-proxy 12.2 unmet.

OTHER RISKS
- The keyword wall may fire the stop rule (≈ 0.4). It is a drop-only tax with no refill. This is stated, not worked around.
- Taint leakage: auto-loaded memory reaches every new session. Memory must never hold per-source or hit data; none was seen in the index on 17 Oct.
- Thin budget: worst case ≈ $21.8 vs T_core ≈ $22.96 (stale). The trim, or the 50K floor, may bind.
- Hardware: the L4 vs H100 agreement was 99.32% earlier. Accuracy is scored on the L4 and speed is measured on the H100, and both are disclosed.
- OHS-5 may miss its 6,000-item floor. Then rungs 2-4 are "not evaluable".
- The R-new gate kit may cut generators, as it cut T-families in C2.
- Haiku wording vs OHS-4 R's wording is a residual style overlap risk.
- The A37(c) licence caution is repeated: Claude-authored wording and Anthropic's terms.
- Timeline of about 3.5 weeks and heavy Claude usage.
- Honest ceiling: a 4B continuation is unlikely to reach the 2-3 pp target. The larger levers (a bigger base, a split-aware deny-list) are outside the standing rules and are owner-only.

## steps
0. TODAY, NO DATA (orchestrator, Opus; Haiku for counts; about 3-4 h; $0)
(a) Reconcile "0 of 15" against the 16 T-blocks, from records only.
- Expected: A62(a) moved T27 to C3. Counts only.
(b) Log live balances.
- Modal mahadikarya2/3, giving T_core = min($34, $32 − spend, C − $8) (A61 e). The HANDOFF figure of ≈ $22.96 is stale.
- The free-credit renewal date (1 Nov per HANDOFF), and whether unused October credit lapses.
- OpenRouter: $10 cap. Read the balance after the 16-17 Oct side-bench Jev runs.
(c) Write the process-disclosure record (sha-logged; list in risks D-a to D-e).
(d) Records-only program checks (counts printed):
- the A61(a) form-shopping bar on every 8.5-gated reuse source (md_*, SB5 and any source on the a61_85 membership list). A source with any variant or unrecorded 8.5 run before its first whole-file record is barred now. Print the barred rows per block, the new reuse upper bound and the 12K G-floor arithmetic;
- whether T37b-dev still exists;
- the transfer-dev file: T19 + T21, 600 rows, sha 2b9702a7….
(e) Taint register (sha-logged). Barred from authoring, picking or setting any C2R number:
- the A64 list;
- every session that read FACT A's per-source output, the planning-stage length-bucket join, kwfind/kwruns/a1_* output or ~/.claude files;
- the whole replan chain (fact agents, 3 planners, 2 judges, synthesis, skeptic, this reviser);
- the orchestrator context, if it read FACT A.
- Barred sessions may still run mechanical checks and append text.
(f) Build the clean packet by program. It contains:
- the spec and FORMAT.md;
- the stop report's block-level counts;
- PREREG with A63's word list redacted (redaction logged);
- this plan's requirement fields.
- A program checks that it holds no per-source survival figure, no replay source identifier and no hit word.
(g) Draft A68.
- A FRESH Opus session that is not in the register drafts it from the packet.
- A second fresh Opus session reviews it, and the first revises.
- The result is sha-logged but NOT appended.
(h) Show the owner the A62(c) stop report and A68 side by side as K vs C2R.
- Neutral: no request and no recommendation (A64 i).
- Also shown: the D1 change list, D1(b), and the D2 and D3 consequences.
(i) Until the owner's words, only no-data work runs:
- C1 speed-only trials on the free L4, each needing parity ≥ 99.5% same argmax on the full 8,143 set against the L4 BF16 S1 baseline:
  - the exact batch-1 bundle;
  - the static-first layout;
  - FP8 with a margin-gated BF16 fallback;
  - a margin-gated second option-order view;
  - keep-alive.
- Measurements of the answer-changing dials on C1, on the 8,143 select half only (sha256("devsel:"+group_id) even). Report-only.
- The CPU token count, and tool code with CPU tests.

1. ADOPT A68 (only after D1 = C2R in the owner's words; about half a day)
- The orchestrator appends A68 under the next free A-number. This happens before any source batch, OHS-5 brief, generator run or row exists.
- A68 fixes:
  - the D1 change list and D1(b);
  - KSAFE;
  - the taint register and the blind-authoring rules;
  - the source batch and the anti-adaptivity rule;
  - the ONE prompt layout. It is static-first only if that passed C1 parity in 0(i), otherwise cygnet + schema_branch_mark. The same layout is used for C1 reads, training, gates and serving (spec 9.1 sha identity);
  - the R-new floors and the full gate kit;
  - the OHS-5 brief sha (if D2);
  - admission and the stop rule;
  - the A42-D 9 grid with the C2R selection score S;
  - the pre-gate: bars unchanged, plus the stricter (e);
  - the C1-served freeze and the dial procedure;
  - the serving-freeze list;
  - SPEED-3/L5 and the D3 caps;
  - CIs, claims, Holm, the harm veto and the wording rule;
  - the Jev stage order with costs;
  - the budget, including one resume;
  - the disclosures;
  - the lesson "no sealed split is ever built with training-side generators again".
- Before any OHS-5 folder exists, data/ohs5* and ohs5_sealed/ join every training-glob exclusion (A42-D 13.1) and every C2R session's path guard, even if D2 = no.
- Where two rules conflict, the stricter one wins.

2. TOOLS, NO ROWS (Sonnet code plus a Sonnet skeptic; CPU tests; about 2 days). Tool shas are logged before first use (A64 g).
- nonce-name generator.
- KSAFE scrub.
- count-only wrappers for g13_c2.py and 8.5.
- g13_c2.py program fix: C2R block names and an OHS-5 slot. Hashes are only added.
- PreToolUse path guard.
- Fresh-Dev splitter: by source, then into select and gate halves by devsel hash.
- static-first renderer, used only if A68 picked it.
- Qwen3.5 token counter.
- margin-gated second view, in the server and as an offline evaluator.
- temperature fit.
- two-stage (source → document) bootstrap, printed beside the pre-registered one.
- whole-unit C1-read selector: a parent and its twins, minimal pairs and view groups move together.
- mix asserts: yes-rate 45-55% per source, at most 150 rows per task-source, 15-30% card-free rows.
- held-out-dimension asserts from the PREREG 13.1 text: no coding rows, no plan or sequence item with 7-8 steps, no trace fault-type item kind.
- L5 client. It stores timings and token counts only, drops response bodies in code, and refuses to start unless SGLang request logging is off.
- No length-reweight tool and no replay-reweight tool.

3. ONE SOURCE BATCH (the fresh Opus session picks; fresh Haiku sessions read metadata and licences; the orchestrator runs the checks; about 1 day)
(a) Pre-commit 100-140 candidate sources.
- Gold from humans, officials or programs; licence clean upstream.
- Not among C1's 204 replay sources.
- No eval or bench source: JevBench, ejs-5, Nimble, SOB, DI, LongBench v2, A15, G-proxy, Wikipedia and NQ are all out. Also out: Federal Register, eCFR and EDGAR.
- Tagged by gap type.
(b) Deny-list check, split-unaware (A61 b).
(c) One whole-file 8.5 run by the orchestrator against the OHS-4 and OHS-AC lists.
- A HIT bars the source for good.
- No substitute or near-neighbour source after a HIT.
- PASS/HIT results never choose further sources.
(d) Seeded 80/20 split by source into train and Fresh-Dev.
- Target: at least 2,000 dev items from at least 15 sources, at most 150 per source.
- Floor: 1,000 items and 12 sources.
(e) Freeze SOURCES_C2R_DECL.json by sha. It lists all candidates (including barred and dev sources), the reuse sources and C1's sources. A hash-only copy is exported for the OHS-5 side.
(f) Download raw files only.

4. OHS-5 SEALED BUILD (only if D2; about 5 days; in parallel with step 5)
- Built by a fresh sealed session: Opus lead, Sonnet code, Haiku reads. Folder lean/ohs5_sealed/, git-ignored.
- It reads only the OHS-5 brief (a separate file whose sha A68 records) and the hash lists. It never reads PREREG, A68, specs, pools or templates.
- G5 rules are copied from OHS-4 8.3, with the rationale recorded (see sealed_test_strategy D).
- Disjoint from DECL by a program hash check the builder cannot read. Before the freeze, the sealed side clears publisher, host and multi-word-name collisions with DECL.
- Reverse decontamination returns the count k only.
- The keyword audit must report 0 failing entries. The scorer and look log are built.
- Spec 8.1 no-spillage 12-gram re-scan: 0 files with 3 or more hits.
- Freeze. The orchestrator verifies the manifest, appends the addendum (shas, counts, k) and adds the OHS-5 exports to G13 and the 8.5 lists (hashes only).
- No C2R row may exist before this record.

5. BLIND CODE, NO ROWS (in parallel with step 4; about 4 days; fresh sessions only; path guard on)
- The fresh Opus session writes the capability brief:
  - the 9 categories;
  - formats only from C2's pre-A38 format pool (named from the spec) plus invented formats, with at least 50% of units in invented formats and no new real-world syntax;
  - the held-out dimensions named in PREREG 13.1, as exclusions in category terms.
- At least 12 generator families, including 6 agent-core generators that cover the 4 agent categories.
- Sonnet writes the generator code and solver A. A separate Sonnet session writes solver B from the format spec only.
- Haiku writes all card and instruction wordings: at least 12 + 12 per generator, plus a held-out set for the mixdev. Length spread: at least 30% of units over 120 words.
- A G0-lite spec per generator is frozen by sha before its first row.
- Sonnet writes the G mappers from a one-page spec per source.
- Haiku writes at least 40 negation frames (at least 30 for training, at least 10 dev-only), each with 2 blind reads.
- Authors never see check output, T-family or sealed paths, HANDOFF, or any barred session's output.

6. ROWS AND GATES (after the OHS-5 freeze record, or after step 3 if D2 = no; about 6 days)
(a) R-new.
- Pilot: 500 rows per generator.
- Full spec 6.3 kit at unchanged bars:
  - G2, G3, G4, G15, G-SL, G-TW and G18 at 100%;
  - G5-H: 0 wrong gold, ambiguous ≤ 1% of 300;
  - A50 G6: mean of 4 × 6,000-row builds ≤ chance + 2 pp;
  - G7; G8 < 10%; G10-G12; G-TPL.
- At most 2 fix rounds, counted from records (an unclear record counts higher), all before any sealed check.
- Then one frozen-seed pass to about 6K rows per generator (≈ 72K). A generator that fails after its rounds is out, with no refill.
(b) G-breadth.
- At most 150 rows per task-source, about 50K rows built.
- The A42-D 8.4 13-read noise gate runs per task; a task is dropped at 2 or more clearly wrong reads.
(c) Twins: complement and negation twins of eligible yes/no parents.
- Program polarity check plus a Haiku exactness check. Twin gold = 1 − parent gold.
- The twin block must pass G5-H (0 wrong, ≤ 1% ambiguous of 300) or it is out. The A60 shares bind.
(d) Dev sets:
- Fresh-Dev, with select and gate halves;
- a Fresh-Dev complement set of about 300 pairs from the dev-only frames, used for pre-gate (d) if T37b-dev is gone;
- the R-new mixdev: 150 rows per generator from held-out seeds and wordings, with select and gate halves.
(e) The A46 drop-only screen on the 25,245 replay survivors.
(f) The A64(e) held-out literal check over every training row and template, and ALL dev rows. Drops only.

7. C1 READS AND THE C1-SERVED FREEZE (free L4; about 1-2 days; $0)
- C1 reads every candidate in the A68 layout and logs p_gold and margin.
- The selection rule acts on whole units; a unit's p_gold is the minimum over its rows:
  - keep units below 0.97;
  - keep a seeded 25% of units above 0.97;
  - a unit with any row below 0.05 gets an A46-method blind re-read. Drop-only.
- C1 baselines on all dev sets.
- C1-served freeze (sha), before any training and any look. It covers:
  - weights 507d1c29…;
  - the layout;
  - the speed dials that passed parity;
  - temperature;
  - server config;
  - hardware class.
- Under D1(b), the frozen dial procedure also runs:
  - fit on the select halves (8,143 and Fresh-Dev);
  - at most 4 nested configs;
  - a config is adopted only if it gains ≥ 1 SE over the next simpler config on both the select and gate halves;
  - tie-break: fewer dials, then lower p50, then the default.
- Under K, the same freeze runs right after the owner's words, using the 8,143 halves only.

8. ADMISSION (orchestrator only; one G13 job at a time; about 1-2 days)
- Early checks on every candidate block:
  - G13, all methods, against OHS-4, the OHS-AC union, OHS-5, OHS-3, the public anchors including SOB, and the dev targets;
  - G-TPL against OHS-4, OHS-AC and OHS-5;
  - A64(e).
- Whole units drop and nothing is refilled. The step 0(d) bar is applied.
- Then, in order:
  - a pre-seeded subsample to the A68 shares;
  - mix_c2 assembly;
  - the final-mix G13;
  - the single final-mix 8.5 run, including the OHS-5 lists;
  - preflight a61_85;
  - the stop-rule check.
- Counts and shas only.

9. GO #1 (owner)
- The package contains:
  - the mix sha and rows per block;
  - the realised R-new family, agent-core and category floors;
  - the stop-rule numbers;
  - the per-block drop counts, quoted neutrally;
  - the live T_core;
  - the expected, pessimistic and worst-case cost (worst case includes one resume);
  - the disclosures and the C1-served sha.
- Payers: the mahadikarya2 → mahadikarya3 relay only.
- If pessimistic + one resume > T_core, the spec 5.5 trim applies down to the 50K floor. Below the floor, stop.
- Spare accounts or aryamhd only by an explicit owner ruling that names the amount.

10. TRAIN (Modal H100; one run; about 4-5 h; $15-19)
- Relay mahadikarya2 → mahadikarya3.
- A checkpoint at every 10% (A42-D 9.1), with resume from the last checkpoint on mahadikarya3.
- Spec 10.4 stop rules apply. Keep one adapter backup.

11. SELECT, GATE, FREEZE (free L4; about 2 days)
- Merge in merged-weight space. S1 vs HF parity must be ≥ 99.5% on dev.
- Run the A42-D 9 grid (3 bases × α 0.5-1.0 = 18) with the 9.5 rule.
  - S = the mean of Fresh-Dev select-half and R-new mixdev select-half accuracy.
  - A switch away from the final step also needs a point gain ≥ 0 on the gate halves.
- C2R dials: the same frozen procedure and configs, with parameters refit for C2R on the select halves only.
- Pre-gate, C1-served vs C2R in one job:
  - (a) R-new mixdev: +8.0 pp or more with LB > 0 on the full set, and also on its gate half;
  - (b) T19 + T21: +3.0 pp or more with LB > 0;
  - (c1)-(c7) as pre-registered, with D9 measured with every adopted dial on;
  - (d) complement: C2R < C1 (point);
  - (e) NEW: on the Fresh-Dev gate half, the LB of C2R − C1 must be > −1.5.
- Fit the temperature. The FP8 margin arm is adopted only at ≥ 99.5% parity.
- Vision side-bench, used once as a veto: C2R is vetoed if the UB of C2R − C1 is below −1.0. The voice result is report-only.
- Freeze the shas of weights, base/α, layout, dials, precision, temperature, server config, hardware class and the L5 client.

12. GO #2 (owner), in a fixed order; no Jev call before (4)
(1) OHS-4 L1 on the free L4: C1-served + C2R in one job. The S1-S6 verdict is logged. If the pre-gate failed, C1-served is read alone.
(2) Only if L1 shipped C2R: OHS-5 L1 (C1-served + C2R), then the harm veto is logged.
- If the veto fires, C1-served is restored.
- If C2R did not ship at L1, OHS-5 stays sealed for C3/2B.
(3) OHS-AC L1 as pre-registered.
(4) Jev stages in the A42-D 13.8 order:
- stage 1: OHS-4 J, two pinned runs, with the version id recorded;
- stage 2: OHS-AC;
- stage 3: the gating anchors;
- stage 4: the G-proxy, labelled "12.2 unmet";
- stage 5: the exploratory anchors;
- stage 6: OHS-5 J, two pinned runs.
- A stage starts only if one complete run plus $0.50 fits the live balance.
- The package gives each stage's projected cost. If stage 6 does not fit, the owner may name a top-up amount; otherwise it is "not evaluable".
(5) SPEED-3/L5, only during stage 1, inside the D3 window:
- c = 1 alternation with Jev on a pre-seeded 2,000-item OHS-4 subsample, from the same client;
- load levels c = 1/16/64/128, at least 1,000 requests each after a 100-request warm-up, on the frozen OHS-4 request file (A42-D 11.3);
- timings only.
- Extra open-loop QPS tests run only on Fresh-Dev or public items.
- If D3 = no, all of this runs on the free L4 and is labelled as such.

13. REPORT (a fresh Opus writer plus a fresh Opus skeptic)
- A disclosure header.
- On every claim: the point estimate and both CIs.
- The Holm table, the utilisation table and the harm veto.
- The orchestrator updates HANDOFF and memory, with no per-source data.

14. OPTIONAL, OWNER ONLY
- ejs-5 paired (about $0.5) and JevBench sealed ($49).
- Only for a "general win" claim, only if the OHS-4 G point is −1.0 or better, and both must agree.
- No submission.