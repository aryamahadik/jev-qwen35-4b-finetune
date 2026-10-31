# A42-D draft (detail of A42) for orchestrator review

Status: DRAFT. `PREREG_FINAL.md` is not edited. The blockquote below is ready to append after the A43 block. The
time stamp is a placeholder.

Sources: `reports/research_oct14/FINAL_PLAN.md` (all), PREREG A37-A43, `teach1/C2_DATA_SPEC.md` sections 5, 6.3, 6.4, 7,
`c2_build/zed_orch/kit_instructions.txt` and `NEW_FAMILY_BRIEF.md`.

Orchestrator changes of 14 Oct applied: (a) in items 4, 9, 10 and 12 (G-proxy of at least 2,000 rows, paired-CI
rejection rule); (b) in items 12 and 13 (Jev budget and order); (c) everywhere (T40-T45).

Items marked **[DECIDE]** are things the plan does not state. Each carries a one-line recommendation. Search for
"[DECIDE]" to list them (41 in total). Remove the tags, or change the rule, when appending.

---

> **Ruling A42-D (14 Oct 2026, ~[HH:MM] UTC; orchestrator ruling under the owner's "yes approve" of 13:51 UTC on
> `reports/research_oct14/FINAL_PLAN.md` (A42 and its erratum); no bar is loosened). Detail of A42, as FINAL_PLAN.md P1
> requires. Written before any T40-T45 row exists: only generator code and G0-lite specs exist, and no row file is on
> disk.**
>
> New families, in order: **T40 CALL-GATE, T41 TAINT-GATE, T42 CODE-EXEC, T43 PATCH-VERDICT, T44 SEQ-CHECK,
> T45 TRACE-VERIFY.** Section numbers below refer to `lean/teach1/C2_DATA_SPEC.md` ("spec"). Where this ruling differs
> from an earlier text it says "Changes".
>
> - **1. Row budget, replay ratio and the spec 5 caps.**
>   - **1.1 Budget (rows kept in the final mix, before any loss at a gate):**
>
>     | ID | Family | Rows | Wave | Min. cards or specs (rows / 64, rounded up) | Class floor |
>     |---|---|---|---|---|---|
>     | T40 | CALL-GATE | 2,000 | 1 | 32 | VALID ≥ 40% |
>     | T41 | TAINT-GATE | 1,750 | 1 | 28 | benign (ALLOW + ALLOW_BENIGN_TRIGGER) ≥ 45% |
>     | T42 | CODE-EXEC | 2,000 (1,500 output + 500 equivalence) | 1 | 32 | none beyond G10 |
>     | T43 | PATCH-VERDICT | 1,750 | 2 | 28 | patch class D (does not apply) ≤ 5%; localisation "none" 5% |
>     | T44 | SEQ-CHECK | 1,250 (≤ 6 steps) | 2 | 20 | none beyond G10 |
>     | T45 | TRACE-VERIFY | 1,250 | 2 | 20 | SUCCESS ≥ 35% |
>     | | **Total** | **10,000** | | | |
>
>   - **1.2 Replay.**
>     - The new-family block gets replay = floor(1.0 × realised new-family rows), at most 10,000 rows, drawn by
>       `replay_sample.py` as in spec 5.4.
>     - Replay for all other new rows stays floor(1.5 × realised base new rows).
>     - Changes: A37 (d) and spec 5.3 ("replay = floor(1.5 × realised new rows)") for the new-family block only.
>     - Missing shares lower the total. Nothing is refilled (spec 5.3, A34 c). Replay follows the realised new-family
>       count.
>   - **1.3 Candidates and selection.** Each family generates 1.5 × its budget (spec 6.4 step 7), then the C1 crowd
>     selects down to the budget under item 6 and the spec 5.2 bins.
>   - **1.4 Total size.** The base mix stays at the A40 (d) cap of ≤ 125,000 rows. The new-family block adds at most
>     20,000 rows (10,000 new + 10,000 replay), so **C2 ≤ 145,000 rows.**
>     - **[DECIDE]** Whether A40's 125,000 binds the base mix only. Recommend yes. The $34 training trim (item 2.3) is the
>       real limiter, because the plan's base mix is ≈ 100-110K rows, not 125K.
>   - **1.5 New-row share.** New rows ≤ 43% and replay ≥ 57% of the final mix.
>     - Changes A37 (d) ("new ≤ 40%").
>     - Check: with base new rows b, new = b + 10,000 and replay = 1.5b + 10,000. At the program-only floor b = 26,600
>       this is 42.3%. At b = 50,000 it is 41.4%.
>     - **[DECIDE]** The 43% bound. Recommend it, because 1.0 × replay makes 40% unreachable.
>   - **1.6 Spec 5.2 caps, checked per family (`mix_c2.py` asserts each on the realised numbers):**
>
>     | Cap | Result for the 6 families |
>     |---|---|
>     | One family ≤ 2,400 rows | Max is 2,000 (T40, T42). Pass. |
>     | Agent tier ≤ 55% of new rows | Tier = T28, T35, T33, T29, T30, T27, T26, T31, T32 (13,600) + T40, T41, T44, T45 (6,250) = 19,850. This holds only if realised new rows ≥ 36,091. With the G-block present, new rows are ≥ 45,000 (≈ 44%). With program rows only (34,100) it would be 58.2%, so the assert is binding. |
>     | Coding tier | **[DECIDE]** T42 + T43 (3,750) are their own "coding tier", not in the agent tier. Recommend ≤ 15% of new rows (3,750 / 36,600 = 10.2% at the smallest mix). If they were agent-tier, the cap would fail (23,600 / 36,600 = 64.5%). |
>     | Free-form rows ≤ 25% per family | T41 carrier documents (Haiku-authored) ≤ 25%. The other five render program text only (0%). |
>     | Every row ≤ 2,000 tokens; family mean ≤ 800 | Same bar (instructions counted twice, spec 3.0). Plan text "prompts ≤ 800" is read as the family mean ≤ 800 with every row ≤ 2,000. |
>     | Yes/no 45-55%; G10 cells 50 ± 2 | None of the six has a yes/no head. If a head is binary, spec 3.0 balance applies to it. |
>     | Difficulty: easy ≤ 25%, hard ≤ 30% | Applied by the C1 crowd bins on candidates (G9). |
>     | No new ordinal rows | None. G18 does not apply to the six. |
>     | ≤ 64 rows per card; ≥ 20-30 cards | Minimums are in 1.1. |
>
>   - **1.7 Waves, cutoff, minimum to train.**
>     - Cutoff: Wed 21 Oct 23:59 UTC (A39 g). A family enters only if its pilot verdict (item 4) is logged by
>       **Mon 19 Oct 23:59 UTC** and it passes every gate by the cutoff.
>     - Training waves follow the table in 1.1. The pilot runs are item 4.4.
>     - The six families do not count toward spec 5.3's "at least 10 program families". Their absence never blocks
>       training.
>   - **1.8 Cost check.** About 20,000 short rows at about $0.25 per 1,000 rows ≈ $5. The binding number is the
>     `mix_c2.py` projection from real padded tokens (spec 5.5).
>
> - **2. Money.**
>   - **2.1 Caps.** The C2 Modal total is capped at **$40**, and training at **≤ $34** (A42 erratum), inside the goal's
>     $45 hard stop. The cap counts all C2 Modal spend on any account: training, the item 4 pilots, C1 and C2 reads, the
>     OHS-4, OHS-AC and anchor C2-side runs, baselines, SPEED-3 and the A41 (b) CPU scans (≤ $3).
>   - **2.2 Planned lines (FINAL_PLAN section 6):**
>
>     | Line | $ |
>     |---|---|
>     | C2 base mix | ≤ 29 |
>     | New-family block (1.4) | ≈ 5 |
>     | New-family pilots | ≈ 1.5 |
>     | C1 reads, dev gate, average, dial, symmetrisation probe (od-l4) | 0 |
>     | OHS-4 look + OHS-AC + anchors (C2 side) + ≤ 4B baselines | ≈ 4 |
>     | SPEED-3 | ≈ 2 |
>     | Reserve | ≈ 3.5 |
>
>     Training (base + new-family block) is ≤ 34. Training, pilots and evaluation come to ≤ 39.5. With SPEED-3 and the
>     reserve the plan sums to ≈ 45.
>   - **[DECIDE]** The plan's table sums to $45, but it also says the C2 total stays within $40. Recommend the $40 cap
>     covers every line. SPEED-3 runs last and is sized to min($2, $40 − spent). The reserve is whatever headroom is left.
>     Going above $40, up to $45, needs the owner's GO at the Fri 23 GO point.
>   - **2.3 Trim.** `mix_c2.py` projects from real padded tokens (0.163 ms per padded token at $4.09/h, spec 5.5).
>     The trim threshold is the **training cap of $34**, not $17 (as A39 f and A40 d already did).
>     - **[DECIDE]** Trim order. Recommend: (1) cut T43, T44 and T45 first, by seeded whole-unit removal keeping 1.0 ×
>       replay; (2) then the spec 5.5 proportional trim, keeping all other balance rules. The floor of 50,000 rows
>       (stop and ask) is unchanged.
>     - FINAL_PLAN rule kept: if the reserve falls below $2 before training, shrink wave 2 first.
>     - A37 (k) stop-and-ask: the steps 100-300 projection above **$34** (was $17). All other A37 (k) rules stand.
>   - **2.4 Accounts.** Free credit first, with the mahadikarya2 → mahadikarya3 relay.
>     - FINAL_PLAN says the aryamhd card is for training only. A37 (j) and A39 (f) say "no card".
>     - **[DECIDE]** Card use. Recommend: no card without an explicit owner GO naming the amount, for training only,
>       and never above the $40 cap.
>
> - **3. New-family gates.** They apply to each of T40-T45, with the 5.3/6.4 fix loop.
>   - **3.1 Kit gates, every one, at its spec 6.3 bar and the A43 G6 rule.**
>     - G0-lite; G1 provenance; G2 (solver B at 100%).
>     - G3 at 100%; G4 (≥ 3 relations, 100%, ≥ 1,000 rows per sampler).
>     - G5-H (0 confirmed wrong golds, ambiguous ≤ 1%; Sonnet first pass, Opus confirms every flag, A43 d).
>     - G6 on ≥ 5,000 QC rows (A43 a); G7; G8 < 10%; G9 (C1-only crowd); G10-G12; G13.
>     - G14: OHS-4 is frozen (A38) and OHS-AC is frozen as in item 13.
>     - G15 at 100%; G-SL, G3-H (≥ 98% per template), G-LEX, G-TW (100%), G-TPL (against OHS-4 and OHS-AC templates).
>     - The kit rules of `kit_instructions.txt`: choiceplan (`plan_report` passes: abstain gold at 1/k, gold position,
>       length rank), compact cards, and the polarity check.
>     - G18 does not apply (no ordinal rows).
>     - Execution gold: two independent hermetic runs (pinned CPython, no network, `PYTHONHASHSEED=0`, 5 s cap) must
>       agree on every row. T42 and T43 carry the witness, fuzz, coverage and differential requirements of
>       FINAL_PLAN section 3.
>     - **[DECIDE]** A gate that cannot apply to code bodies (G-SL, G3-H) applies to the authored text only. Recommend
>       each family's G0-lite lists such exemptions with a reason, and the orchestrator confirms them. Never a lower bar.
>   - **3.2 Probes (on ≥ 5,000 QC rows of the same generator, as in A43 a).**
>     - **Options-only probe** and **formatting-only probe:** each at chance ± 3 pp, two-sided. A result far below chance
>       also fails, because it shows an inverse artifact.
>       - **[DECIDE]** "Chance" = the larger of 1/k and the majority-class share. Recommend this definition.
>       - **[DECIDE]** The probe models and views are the ones G6 uses.
>     - **Diff-size probe (T42 and T43 only):** a predictor from diff and size features (added and removed lines, hunk
>       count, token edit distance, AST node delta) at chance ± 3 pp.
>     - A 1,000-row pilot cell outside its band must lie inside its pilot-size permutation null (p ≥ 0.05), else it counts
>       as a fail (A43 a).
>     - **[DECIDE]** libcst, jsonschema and hypothesis are not installed and there is no network. Recommend the
>       reformatting tell is removed by running original and mutant through the same `ast.unparse`, and Hypothesis cases
>       are replaced by seeded property generators. The probe still bars any formatting tell.
>   - **3.3 Reseed audit.** A seeded 3% of the candidate rows are regenerated with an independent seed from the same row
>     spec. More than 1% label flips drops the generator (the family fails that iteration).
>     - With fewer than 100 audited rows, one flip is already above 1%. So the bar means 0 flips.
>   - **3.4 Blind re-derivation.** A blind Haiku solves a seeded 5% of the final kept rows of each family. Every
>     disagreement with gold goes to Sonnet adjudication, then Opus confirmation (A43 d). Bar: 0 confirmed wrong golds,
>     ambiguous ≤ 1%.
>     - It is in addition to G5-H (100 rows at pilot, 300 at full).
>     - Haiku flags only. Rows are never relabelled.
>   - **3.5 G13.** Seed-first, then candidates, then the final mix, with 0 hits after drops. The target registry adds
>     the OHS-AC sealed-side export (counts only), the G-proxy export (item 12) and every public anchor in item 13, with
>     13-gram and repo/date exclusion.
>   - **3.6 Fix loop.** At most 2 fix iterations per family, on generator and templates only (spec 6.4 step 6).
>     - The first failed gate evaluation is iteration 0; fixes are iterations 1 and 2.
>     - A family that still fails any gate or probe after iteration 2 moves to **C3**. It is not refilled and no label
>       is ever relabelled.
>     - **[DECIDE]** The deadline for iteration 2 is Mon 19 Oct 23:59 UTC (1.7). Recommend this, so no fix runs after
>       the sealed freeze.
>
> - **4. New-family pilot gate.**
>   - **4.1 Pilot rows.** 1,500 rows per family and one short LoRA pass, starting from C1, recipe as in A37 (i), seed
>     20261013.
>     - **[DECIDE]** Pilot rows are new rows only, without replay (≈ 9,000 rows, ≈ $1.5, as the plan costs it).
>       Recommend this. It is a harsher test of the existing-dev drop bar and the bars are not loosened to compensate.
>   - **4.2 A family is kept only if all of these hold:**
>     - **(i)** its accuracy gain over C1 on **its own dev split** is **≥ +2.0 pt**;
>     - **(ii)** existing dev drops by **≤ 0.5 pt**;
>     - **(iii)** its G-proxy change is not rejected, as in 4.3.
>
>     A family that fails moves to C3.
>   - **4.3 G-proxy rule (replaces "must not fall by more than 0.5").**
>     - The G-proxy change is C2-pilot minus C1 accuracy on the G-proxy (item 12), paired by item.
>     - The CI is the 95% paired bootstrap, clustered by source document, 10,000 resamples, seed 0.
>     - **A family is rejected if the CI upper bound of its G-proxy change is below −0.5 pt.** There is no 0.5-pt point
>       threshold.
>     - At n = 2,000 the paired SE is ≈ 0.6 (scaled from A38's SE 0.51 at n = 2,883). The rule then rejects only a point
>       change below about −1.7 pt.
>   - **4.4 Own dev split and existing dev.**
>     - **[DECIDE]** Own dev split = 300 rows per family (the spec 7.1 mixdev of 150 plus 150), built from held-out
>       registries, packs and wordings, never trained, disjoint from the sealed split.
>     - **[DECIDE]** Existing dev = the 9 gate dev splits (7,056 rows), pooled accuracy, as pre-gate D1 reads it.
>       Recommend this reading.
>     - Pilot runs: Sat 17 Oct for T40, T41 and T42 (and T43 if its program gates have passed by then), Sun 18 Oct for the
>       rest.
>     - **[DECIDE]** If a joint run fails (ii) or (iii), re-pilot its families one at a time (≈ $0.25 each, inside the
>       reserve). Recommend this. Otherwise all families in that run move to C3.
>
> - **5. G-block routing (FINAL_PLAN item 6).**
>   - **5.1** C1 (adapter 507d1c29...) reads all ≈ 18.8K G-block rows, kept and dropped, on od-l4 with the A18.2 readout.
>     C1 output is a routing signal only. It is never a label or a target.
>   - **5.2 Classes** (on Haiku-accepted rows, Haiku confidence ≥ 0.80 per A39 d):
>     - AGREE-HIGH: C1's argmax equals the Haiku label and p_C1(label) ≥ **0.9**;
>     - AGREE-LOW: C1 agrees but p < 0.9. These rows are kept unchanged;
>     - DISAGREE: C1's argmax differs from the Haiku label.
>
>     **[DECIDE]** Rows already labelled by Opus (1,272) and rows dropped by A39 keep their status. Recommend this. C1
>     reads of dropped rows are report-only.
>   - **5.3 AGREE-HIGH:** keep **35%** as anchors by a seeded draw (seed 20261013), stratified by card × label. The other
>     65% leave the G-block.
>   - **5.4 DISAGREE:**
>     - They go to Opus under the A39 (d) reader rules (gold-free chunks of ≤ 50 items, TEACH-0 prompt, file-access
>       audit), **20-40 chunks**.
>     - A row is kept only at Opus confidence **≥ 0.85**. It then carries the Opus label, which may differ from Haiku's.
>       Otherwise it is dropped.
>     - **[DECIDE]** If DISAGREE rows exceed 40 chunks (2,000 items), take a seeded subsample uniform by card. Recommend
>       that unread DISAGREE rows are dropped, not kept on the Haiku label (Haiku is right on 53% of these).
>   - **5.5 Rebalance.** Yes share **40-60% per card**, by seeded down-sampling of the over-represented label within the
>     card. Never relabel. The A39 (e) limits stand: block ≤ 15,000 kept rows and no domain above 20%. The G-block mixdev
>     (150 per domain) is drawn before routing and is never trained.
>   - **5.6 Up-weight.** DISAGREE rows confirmed by Opus are weighted 1.0-1.5 × relative to AGREE-HIGH anchors.
>     - **[DECIDE]** Weights are realised only as sampling quotas. Recommend this, because G12 forbids repeated rows.
>   - **5.7** The A39 5% Opus audit and 6% per-domain re-read rule apply unchanged. G13 runs on the routed block. The
>     ≈ 5K rows freed may be reallocated only inside the base cap in 1.4.
>
> - **6. Trap selection (changes A37 (e) "Bins and selection are unchanged").**
>   - **6.1** Every distractor carries a metadata tag of the program corruption that made it (the named error model).
>     The tag is never in the prompt and is excluded from G7 features.
>   - **6.2** A relation unit is **trap-flagged** if C1 (the G9 C1-only read, A18.2 readout) puts **≥ 0.25** probability
>     on any tagged trap option.
>   - **6.3** Trap-flagged units go to the **hard bin** at **2 × selection weight** against other hard-bin units, inside
>     the spec 5.2 caps (hard ≤ 30%, easy ≤ 25%). If the flagged units would exceed 30%, the weight is scaled down until
>     it fits.
>     - **[DECIDE]** "2 ×" means a selection weight, not a repeated row. Recommend this, because G12 forbids repeats.
>   - **6.4** Trap types C1 picks most are favoured, ordered by the C1 pick rate on the family's own candidates.
>     - The dev pick rates are given as priors only: band off-by-one 50%, boundary 39%, rename/merger 38%, unit 38%,
>       not-yet-in-force 30%.
>     - **[DECIDE]** No trap type may exceed 35% of a family's trap-flagged units. Recommend this.
>   - **6.5** Units stay whole. G10, G11, the 2,400-row family cap and the crowd chi-square check still apply.
>     Everything that does not carry a corruption tag is selected as before.
>   - **[DECIDE]** The six new families use the same selection when their distractors carry tags (T42 mutants, T43
>     patches) and the 1.5 × candidates of 1.3 allow it. Recommend yes. T41, T44 and T45 are selected as before.
>
> - **7. Lifting the T37b 2K cap (changes spec 3.18, spec 4.2 and A37 (d)).**
>   - **7.1** Complement-twin rows are capped by block instead: G-block ≤ 5,000; metadata block ≤ 5,000;
>     replay-yes/no ≤ 10,000 (target 8,000-10,000, including the original T37b 2,000).
>   - **7.2** Replay twins are counted inside the replay budget (1.2).
>     - **[DECIDE]** G-block and metadata twins count inside the base new-row cap in 1.4, not on top of it. Recommend
>       this.
>   - **7.3 Catalogue and checks.**
>     - At least **300 negation patterns** in the trained catalogue.
>     - A program checks that **exactly one predicate changed**.
>     - A blind Haiku exactness check passes at **≥ 0.9**, per pattern.
>     - Sonnet audits **3%** of twin rows (seeded, stratified by pattern) and drops every pattern with more than 3% error.
>       A pattern with 33 or fewer audited rows is dropped on a single confirmed error.
>     - G-TW at 100% (gold(Q) = not gold(not-Q)), and G13.
>   - **7.4** At least 30 negation patterns are authored first, frozen and **held out of training**. They are the only
>     patterns used for the 150 complement pairs of the G-proxy (item 12) and for the item 10 probe.
>     - **[DECIDE]** The size of 30 held-out patterns. Recommend it, so the 150 pairs spread over at least 30 patterns.
>   - **7.5** Labels are never hand-edited. Gold is still 1 − gold of the base row (complement) or the same gold (equiv).
>
> - **8. Metadata as targets (changes A39 (b)); sealed-side source-name check.**
>   - **8.1 Change.** A39 (b) said "any human labels a source carries are NOT used as targets". For this block only,
>     upstream human or official metadata fields are targets when a program turns them into a task with deterministic
>     gold. Haiku and Opus are not label sources here. Haiku reads blind and flags only (A37 b).
>   - **8.2 Block.** 11 sources, one Sonnet mapper each (run as 3-4 agents). **40-80 tasks per source**, ≤ **200 rows per
>     task**, **8,000-12,000 rows** in total, ≥ **30% card-free** (per source).
>     - **[DECIDE]** No source above 15% of the block, and the 11 sources span at least 8 domains. Recommend both.
>   - **8.3 Source rules.** As A39 (b) and A40 (a): permissive licence verified upstream; deny-list pass; fresh; not in
>     C1's sources, OHS-1/2/3/4, OHS-AC, DI, JevBench, ejs-5 or LongBench v2; not Wikipedia/NQ, Federal Register, eCFR or
>     EDGAR. No source is a G-proxy source (item 12).
>   - **8.4 Noise gate.** A task is dropped if a Haiku blind read finds more than **8%** of its sampled rows clearly
>     wrong.
>     - **[DECIDE]** Sample 13 rows per task. Recommend this: one wrong row (7.7%) passes, two (15.4%) drop the task. It
>       costs about 6-11K reads, close to the plan's 6-8K.
>   - **8.5 Sealed-side source-name check.**
>     - Before any mapper is written, and again on the final mix, each source's identifiers (dataset name, publisher,
>       host, upstream ID, licence page URL) go to the sealed-side checker (the existing sealed-side child of
>       `decontam_g13`).
>     - It returns **PASS or HIT per source only**, against the OHS-4 and OHS-AC source lists. A HIT removes the whole
>       source.
>     - No C2-side agent opens any "ohs" path. The orchestrator sees counts only.
>   - **8.6** G13 on the block with 0 hits after drops. A source's human labels stay in the report-only quality audit.
>
> - **9. Checkpoint average and C1 → C2 interpolation (changes A37 (a) and (g): "one candidate: the final-step
>   adapter", "no snapshot, blend or second candidate").**
>   - **9.1** Training saves **6-10 checkpoints**. Averages and interpolation are computed **in merged-weight space**,
>     never by averaging LoRA A and B factors separately.
>   - **9.2 Candidate grid, frozen now:**
>     - the final step (the A37 default);
>     - last-k averages;
>     - an early+late average;
>     - for each of those, θ(α) = C1 + α(C2 − C1) with **α in {0.5, 0.6, 0.7, 0.8, 0.9, 1.0}**.
>
>     **[DECIDE]** k ∈ {2, 3, 4}, and early = the checkpoint nearest 33% of the steps with late = the final step, weights 1:1.
>     Recommend these.
>   - **9.3 Selection score, pre-registered:** S = the unweighted mean of three accuracies (in pt): the G-proxy, the R
>     mixdev (the program-family mixdev, spec 7.1) and the pooled OHS-AC dev splits of the six new families (those that
>     entered C2).
>     - **[DECIDE]** Equal weights. Recommend them.
>   - **9.4 Eligibility.** A candidate must pass pre-gate (a)-(d) of spec 7.2 (D1-D6, D9, complement) and the G-proxy
>     rule of item 4.3 versus C1.
>   - **9.5 Choice.** The highest S among eligible candidates, but the final step (α = 1.0) stays the candidate unless the
>     paired 95% CI of the S gain (clustered, 10,000 resamples, seed 0) has a lower bound > 0.
>     - **[DECIDE]** The paired-CI replacement rule. Recommend it, so a dial is never taken on noise.
>   - **9.6 Freeze.** The chosen candidate is **one** candidate. Its adapter sha and grid are recorded before any look.
>     Only dev, the G-proxy and the OHS-AC dev splits are read. Jev, OHS-4 and OHS-AC sealed are never used. The
>     candidate must still meet every ship rule of spec 7.3, so no new ship criterion is added (A39 h).
>
> - **10. Symmetrisation adoption rule.**
>   - **10.1** The served estimate is p = ½[p(q) + 1 − p(flip q)], sharing the cached prefix, on yes/no items that have a
>     program-made flip.
>     - The flip is a deterministic program from the trained catalogue of item 7. No Claude call happens at test time.
>     - Items without a program flip are served unsymmetrised.
>   - **10.2 Adopt only if, on dev (the G-proxy plus the 150 held-out-pattern complement pairs):**
>     - complement violation falls by **≥ 0.02**, and
>     - accuracy and calibrated Brier show **no loss**, and
>     - D9 (p50 latency ≤ 1.05 × C1, spec 7.2 c7) still passes on the symmetrised path.
>     - **[DECIDE]** "No loss" = point change in accuracy ≥ 0 and in Brier ≤ 0, on both the G-proxy and the D1 yes/no
>       rows. Recommend this.
>     - The plan puts the extra compute at 5-10%, so D9 may fail. Then it is not adopted.
>   - **10.3** The probe pairs use only held-out negation patterns. Pairs that use catalogue patterns would score 0
>     violation by construction.
>   - **10.4** If adopted, the candidate is "C2 + symmetrisation" and is frozen with item 9. SPEED-3 (item 11) reports both
>     modes. It is one served path, not a second candidate.
>
> - **11. SPEED-3 cost method.**
>   - **11.1** Cost per 1,000 requests =
>     (hourly instance price) ÷ (0.40 × T_sat × 3,600) × 1,000, where T_sat is the higher of the steady-state throughputs
>     (requests/s) measured at concurrency **64 and 128**. The 40% is the pre-registered utilisation.
>   - **11.2 Serving.** State-prefix reuse and chunked prefill on. US region. The configuration is hashed before the run.
>     **Headline latency is c = 1**, with c = 16 and c = 64 also reported (the run covers c = 1, 16, 64, 128).
>   - **11.3** Request mix: the frozen OHS-4 request file of A38, with the same prompts for C2 and for Jev. Jev's cost
>     uses OpenRouter list prices on the measured token counts, and its latency is measured from the same region,
>     interleaved.
>     - **[DECIDE]** ≥ 1,000 requests per concurrency level after a 100-request warm-up, and p50/p95 over the whole level.
>       Recommend this.
>   - **11.4** A cost win is C2's $/1K below Jev's. Reference values: C1 $0.079, Jev $0.061. Cap ≈ $2 of Modal inside the
>     $40 cap of item 2.
>
> - **12. G-proxy definition (P2; changes by the 14 Oct review).**
>   - **12.1 Size and content.** **≥ 2,000 rows** (not 400-600) from new official-metadata sources via `fetch_socrata.py`,
>     with ≥ 30% card-free rows and a yes share of 40-50%, **plus 150 complement pairs** that use negation patterns
>     held out of training (7.4).
>     - **[DECIDE]** At least 3 sources, none above 40% of rows. Recommend this.
>   - **12.2 Gold.** Program-mapped from official metadata, as in item 8. Same source rules as 8.3, the item 8.5
>     sealed-side source-name check, and **disjoint from the 11 training metadata sources**. Never trained. It is a G13
>     target (3.5).
>   - **12.3 Noise check.** A blind Haiku flag-only read.
>     - **[DECIDE]** 100 rows per source, and a source is dropped above 8% clearly wrong (the item 8.4 rule). Recommend
>       this.
>   - **12.4 Readers.** C1 reads it now. Jev reads it once, for evaluation only, **after** the candidate is frozen. Jev
>     output is never a selection signal.
>     - **[DECIDE]** The Jev read of the G-proxy is not in the Jev order of item 13.8. Recommend it goes after OHS-AC and
>       before the gating anchors (≈ 4,600 calls).
>   - **12.5 Uses.**
>     - The item 4 pilot gate, the item 9 score and the item 10 probe.
>     - A general-accuracy claim with ejs-5 paired and JevBench sealed, per FINAL_PLAN (a win only if both agree).
>     - It is **not** a ship rule. Spec 7.3 S1-S6 are unchanged.
>   - **12.6 Paired CI** everywhere it is used: 95%, clustered by source document (a complement pair is one cluster),
>     10,000 resamples, seed 0. Rejection means a CI upper bound below −0.5 pt of the change.
>
> - **13. OHS-AC freeze and the verdict rule (FINAL_PLAN section 4, verbatim where possible).**
>   - **13.1 Freeze.**
>     - OHS-AC is built blind by sealed agents in `lean/ohs_ac_sealed/` (git-ignored). The "ohs" name puts it under
>       every never-open rule. The orchestrator sees counts and hashes only.
>     - Every training glob excludes `data/ohs3*`, `ohs3_parts/`, `ohs4_sealed/` and `ohs_ac_sealed/`, and every public
>       anchor in the never-train manifest.
>     - The programmatic part is frozen **Sat 17 Oct** (manifest sha256 recorded in this file's A42-D addendum). The
>       Haiku surface text (≈ 5K paraphrases) is done **Mon 19 Oct**, before any training-side Haiku text. The final hash
>       is recorded then.
>     - Each of the six new families emits its sealed split first (by its HELD_OUT_SAMPLERS, through a sealed agent), and
>       its hash is recorded before its first training-side row.
>     - **[DECIDE]** FINAL_PLAN's day table has wave-1 pilot rows on Fri 16, before the Sat 17 manifest freeze. Recommend the
>       freeze is per family: family sealed split first, hash logged, then pilot rows. The full manifest hash on Sat 17
>       follows.
>     - **[DECIDE]** Block A1 covers the 17 existing families, whose rows already exist. Recommend the "before any
>       training-side row" rule is read for the six new families only. A1 uses each family's held-out rule variants and G-TPL
>       plus the sealed-side child of G13.
>     - **Held out for the sealed split:** registries and naming styles; idiom buckets (closures/late-binding, MRO);
>       2 mutation operators; 1 fault type (leave-one-fault-type-out); predicate vocabularies; plan lengths 7-8. No
>       training row uses a held-out value.
>       - **[DECIDE]** Mapping. Recommend: T40 and T41 registries and naming styles; T42 idiom buckets and 2 mutation
>         operators; T43 1 more mutation operator class; T44 predicate vocabularies and plan lengths 7-8; T45 1 fault type.
>   - **13.2 Suite (OHS-AC):**
>
>     | Block | Content | n | Detectable gap (ρ ≈ 0.5) |
>     |---|---|---|---|
>     | A1 agentic: existing | 17 program-gold families, rule-variant holdout, 120 base scenarios × minimal pair | 4,080 | block ≈ 1.6-2 pts |
>     | A2 agentic: new | CALL-GATE (T40) 500, TAINT-GATE (T41) 500, SEQ-CHECK (T44) 400, TRACE-VERIFY (T45) 400 | 1,800 | per family ≈ 5-5.6 pts |
>     | B coding | CODE-EXEC (T42) 900, PATCH-VERDICT (T43) 500 | 1,400 | block ≈ 3 pts; family ≈ 5 pts |
>     | C1 reliability | 600 base scenarios × 8 variants (paraphrase, option order, entity/tool rename, terse/typo, irrelevant rule paragraph, fact order, rule-swap, cue inversion) | 4,800 | pass^8 ≈ 7 pts |
>     | C2 hijack | 500 attacked × 3 tiers (static; best-of-10 rewrite; transfer from base Qwen3.5-4B) + 500 benign trigger-word items | 2,000 | 2% vs 8% ASR |
>     | Real-text slice | Real public policy docs, man-page commands and package READMEs, with program gold | 200 | sign check only |
>     | **Total** | | **≈ 14,300** | |
>
>     OHS-4 (frozen A38, one look): G 2,883 / R 1,454 / U 433 / X 281 pairs / consistency 881.
>   - **13.3 Public anchors** (eval-only, hashed in the never-train manifest, 13-gram and repo/date exclusion).
>     - **Gating** (part of the verdict):
>       - BFCL V4 selection + irrelevance (about 3,000; pinned to `bfcl-eval` 2025.12.17; reported as "selection
>         accuracy", not as an official BFCL score);
>       - InjecAgent (1,054) + NotInject (339);
>       - R-Judge (569);
>       - CRUXEval-O as MCQ (800);
>       - EquiBench Python (1,200);
>       - When2Call test, if its licence is clear (otherwise exploratory).
>     - **Exploratory** (reported, not gating): AgentProcessBench (3,000-step cluster sample); ATBench-Codex; ACPBench;
>       CodeJudgeBench (2,000 sample); LiveCodeBench post-cutoff execution; SWE-bench Verified patch verifier (1,000).
>   - **13.4 General accuracy:** G-proxy, ejs-5 paired and JevBench sealed, per the fair-test-pick rule. A win is claimed
>     only if both agree.
>   - **13.5 Baselines (≤ 4B only):** base Qwen3.5-4B zero-shot, C1, Qwen3Guard-Gen-4B, AgentDoG-4B (licence check),
>     xLAM-2-3b, and a rules-only layer. A win over Jev that loses to a 4B specialist is not a headline.
>   - **13.6 Fair run:**
>     - Identical text and options, with 1-2 sentence option definitions in the prompt so Jev can read our taxonomy.
>     - Every item in 2 option orders.
>     - Jev's default format is primary, plus 2 pre-registered wrappers.
>     - Calls are interleaved from the same region.
>     - Jev runs 3× on a 10% subsample. **If its spread exceeds 1 pt and a full 3× run does not fit the budget of 13.8,
>       the spread is reported and the worst of the runs that fit is used.** If the full 3× fits, the full set runs 3× and
>       the worst run is used.
>       - **[DECIDE]** "Worst" means the Jev run with the highest score on the metric in question (the hardest comparison
>         for C2). Recommend this.
>     - Errors count as wrong.
>     - Raw outputs are hashed.
>   - **13.7 pass^k, hijack, statistics:**
>     - pass^k: C2 is deterministic, so k comes from the 8 perturbations. Jev is also scored on identical-call stability.
>       Report pass^1, pass^4 and pass^8, plus strict group accuracy on fact-flip plus rule-swap groups.
>     - Hijack: ASR@1 and ASR@10, utility under attack and over-defence are always reported together. A model that always
>       says "ask" must not win.
>     - Statistics: paired by item, with a clustered bootstrap by base scenario (10K resamples). Holm correction across
>       blocks and across families within a block. n is fixed now at ρ = 0.5 (no Jev pilot).
>       - **[DECIDE]** Apply Holm to the "lower bound > 0" tests of the verdict, keeping the 95% interval for reporting.
>         Recommend this.
>   - **13.8 Jev budget (replaces the FINAL_PLAN cost paragraph).**
>     - OpenRouter is capped at **$10**, with **about $7 left**. The live balance is read and logged before the first Jev
>       call.
>     - **Order:** (1) the OHS-4 Jev read; (2) OHS-AC; (3) the gating anchors, only if funds remain.
>     - Each stage's projected cost uses the measured cost per call of the stage before it. A stage runs only if its
>       projection fits the balance, with a $0.50 margin.
>       - **[DECIDE]** The $0.50 margin. Recommend it.
>     - OHS-4 stays one Jev look (A38, A37 h). The 10% spread rule applies to OHS-AC and the anchors.
>     - Jev calls: about 33K for OHS-AC and about 17K for the anchors, ≈ $4-6 in the plan's estimate. C2-side inference
>       ≈ $2 of Modal, inside item 2.
>     - **[DECIDE]** A gating anchor that was not run cannot support "no gating anchor significantly worse". Recommend
>       DOMINATE is then reported as "not evaluable", with blocks A, B and the hijack part of C reported on their own.
>   - **13.9 Verdict rule (hashed before the look):**
>
>     | Verdict | Rule |
>     |---|---|
>     | WIN (block) | 95% CI lower bound > 0, AND point ≥ +4, AND no family's CI upper bound below −3 |
>     | DOMINATE | WIN on A, WIN on B, WIN on the hijack part of C, AND the real-text slice is not reversed, AND no gating anchor is significantly worse than Jev |
>     | General | Reported on its own as win, tie (TOST ±2 on the pooled sets) or loss; never folded into DOMINATE |
>
>     - **[DECIDE]** The sha256 of this item 13.9 table plus 13.6-13.8 is computed at append and recorded in the OHS-AC
>       manifest before any look. Recommend this.
>
> - **14. What does not change.**
>   - Never train on Jev outputs, sealed sets or eval sets. Jev results are never a selection signal.
>   - No model above 4B is trained, distilled from or used as a label source. Claude never assigns a label for T40-T45
>     (program or execution gold only). The Anthropic-terms caution of A37 (c) and A42 stands.
>   - No data-quality gate is loosened. A37 ship rule and pre-gate, A38, A39, A40, A41, A43, and both owner GO points
>     (before training, and before the OHS-4 look, the OHS-AC runs and SPEED-3) are unchanged.
>   - **What this ruling changes:** A37 (d) replay for the new-family block and the 40% new share (1.2, 1.5); A37 (e)
>     selection (6); A37 (a) and (g) one-candidate wording (9, 10); A39 (b) (8); spec 3.18 and 4.2 T37b cap (7); the spec
>     5.5 and A37 (k) $17 threshold becomes $34 (2.3); FINAL_PLAN P2 (12), the pilot-gate G-proxy line (4.3) and the
>     Jev cost paragraph and fair-run spread rule (13.6, 13.8).
