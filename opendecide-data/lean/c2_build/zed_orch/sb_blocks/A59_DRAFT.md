Ruling A59 (draft). The orchestrator appends it to `lean/PREREG_FINAL.md` after the last entry. The file is append-only: lines 2356-2825, the A42-D block hashed as `cbdc29d9…`, are not edited. Opus 5.5 wrote it on 17 Oct 2026.

Inputs read: PREREG from A42-D to the end (A42-D 1-14, A45-A56, the Freeze addendum, A55), `zed_orch/A57_DRAFT.md`, `zed_orch/sb_blocks/A58_DRAFT.md`, HANDOFF.md lines 120-200, the JOB3 round-1 summary, and the layout of `c2_build/`. I opened no "ohs" or "sealed" path and read no bench item.

---

> **Ruling A59 (17 Oct 2026; orchestrator ruling, Opus. It rules on the JOB3 investigation of C1's disposition/action drop on System One Bench. It acts under the owner's 17 Oct approval of bench-driven post-freeze blocks (A58) and the owner's request in this run: "add little Arabic … fewer examples so that model can at least understand a little". No gate, bar, cap or waiver rule is loosened. No row is ever relabelled.)**
>
> - **(a) Findings accepted. No existing data changes.**
>   - No C2 family, block or replay source teaches a disposition convention that conflicts with what its labels plainly mean. The overloaded words ("stop" in T27 and T30, "escalate" in T26, T31 and T45) are defined on their own cards.
>   - Nothing is regenerated, excluded or relabelled:
>     - none of T01-T45, GB/GW/MD/RTW, item 10, the G-proxy or SB4-SB6;
>     - no golden_train source;
>     - the smcalflow and star replay rows stay (1,146 + 740). Drop-only screening (A46) is for label noise, and the evidence shows no harm from them.
>   - **What follows:** no existing family re-runs any gate, and no fix round opens. This includes the A49 (d) and A52 (d) rounds, which are unchanged.
>
> - **(b) T46 DISPOSITION-GATE: admitted as a post-freeze, training-only program block.**
>   - **Why it is allowed.** A42-D 13.1 ("a family whose sealed split is not in the frozen manifest does not enter C2") governs T40-T45, the families whose job is the OHS-AC verdict. T46 enters under A58's precedent for bench-driven post-freeze blocks.
>   - **What it is not part of:**
>     - It has no OHS-AC split and is in no OHS-AC verdict.
>     - It does not count toward spec 5.3's 10 program families, the agent core, or A42-D 1.2's 6,666 rows for T40-T45.
>   - **How 13.1's purpose is still kept.**
>     - T46 rows are written after the freeze, so they cannot shape a sealed item.
>     - G-TPL against the OHS-4 and OHS-AC templates binds.
>     - The sealed-side G13 child with the held-out keyword hashes binds.
>     - T46 imports no code, template, pool or lexicon from the 17 A1 families or from T40-T45. Only `c2_kit` is shared.
>     - It does not import `job3_disposition/probe_gen.py` or its tables. This keeps the probe a clean dev set (item g).
>   - **Tier and caps.**
>     - T46 is in the agent tier (the ≤ 55% cap applies).
>     - Its kept budget is **1,200 rows**. Candidates are 1,800 (1.5×), with at least 20 cards and at most 64 rows per card.
>     - Replay is floor(1.5 × realised rows), drawn only from A46-screened rows. If the screened pool is short, T46 shrinks; no unscreened row is drawn.
>   - **Trim order.** T46 is cut in A42-D 2.3 step 2, together with T44 and T45 in proportion.
>
> - **(c) T46 content. These are G0-lite targets, and the orchestrator confirms G0 before the first row.**
>   - **Workflows:** 6 (invoice, support/refund, agent run, access request, HR/leave, deployment).
>   - **Vocabularies:** at least 8 label sets in snake_case and spelled-out forms: pay/hold/reject/escalate, continue/observe/human_review/stop, refund/replace/human_agent/decline, approve/deny/ask, and others.
>   - **States:**
>     - JSON, YAML or key-value, with thresholds in the state.
>     - Ticket-form states count as free-form, capped at 25%.
>   - **Policy arms:** stated-policy rows 55%, and plain-only rows 45% whose state fields alone settle the answer.
>   - **Definitions:** printed on 60% of rows and absent on 40%. Coded labels make up 25% of rows, and every coded-label row prints its definitions.
>   - **One meaning per word.** A program-asserted T46 lexicon maps each surface label to exactly one semantic class across the whole family. A row without definitions may use only labels in that lexicon.
>   - **Special row types:**
>     - boundary rows (equal to the limit, and limit + 0.01) 20%;
>     - conflicting signals with a printed priority 15%;
>     - "alarming but permitted" 15%;
>     - minimal-edit twins (one field flips the label) on at least 20% of rows, under G4.
>   - **Gold shares:** permissive 30, hold-type 25, deny/stop 25, human/escalate 20 (each ± 3%).
>   - **Yes/no:** 45-55% yes, with permissive-yes and cautious-yes forms equal.
>   - **Abstain gold:** whatever the kit's choiceplan/`plan_report` requires, and that check must pass. The proposal's "≤ 8%" applies only where `plan_report` allows it.
>   - **Size and wording:**
>     - every row ≤ 2,000 tokens and the family mean ≤ 800 (spec 3.0);
>     - no instruction or definition string shares an 8-gram with any bench instruction or criteria string. This is checked by the decontamination program only, as in A58 (c) 5.
>   - **Gold:** program gold only. A second, independent paradigm (solver B) must agree on 100%. Claude never assigns a label.
>
> - **(d) Arabic slice (owner request).**
>   - **Size:** at most **60 training rows** (5% of T46), plus 30 rows in T46's own dev, which are report-only.
>   - **Format:** as in A58 (d): English instructions and definitions, and Arabic state values (names, reasons, notes). State keys and digits stay in Western form.
>   - **Source of the Arabic text:**
>     - fixed program slot tables, authored by fresh Haiku agents as training-side pools, with train and dev-only partitions;
>     - each item has a program-assigned meaning class and must pass G-LEX 2/2 (two blind reads give the table's class);
>     - no free-form LLM Arabic.
>   - **Deciding fact.** At most half of the Arabic rows carry the deciding fact in an Arabic note. Those notes come only from G-LEX-passed items.
>   - **Disjoint from the probe.** No slot value is exactly equal to any string in the probe's `to_ar` tables (program check, 0 required).
>   - **Arabic cap.** The owner's Arabic cap now counts every Arabic training row in C2: **SB4 + SB5 + T46-ar ≤ 1,500**. `mix_c2.py` asserts it. If the total is over, SB4 and SB5 are cut in proportion by seeded (20261013) whole units, and nothing is refilled. A58 (e) is otherwise unchanged.
>   - **Gating.** The slice is built whatever the probe's Arabic arms show (the owner asked for it). Those arms are report-only.
>
> - **(e) Gates and deadline.**
>   - **Binding gates, at their existing bars:**
>     - G0-lite, G1, G2 at 100%, G3 at 100%, G4, G-SL, G3-H, G-LEX, G-TPL, G15;
>     - the A42-D 3.3 reseed audit, and the 3.2 options-only and formatting-only probes;
>     - **G6 per A50 (a):** four 6,000-row QC builds at seed bases 900000, 11,000,000, 12,000,000 and 13,000,000; every cell mean ≤ chance + 2 pp;
>     - G7, and G10 (report-only on candidates, binding on the selected rows, per A49 c);
>     - G5-H on 300 rows, stratified with at least 120 rows without definitions and at least 30 Arabic rows; 0 confirmed wrong golds and ambiguity ≤ 1%; Sonnet does the first pass and Opus confirms every flag;
>     - the A42-D 3.4 blind 5% re-derivation;
>     - G9, a C1-only crowd read with the A42-D 1.3 selection bins;
>     - G13 (seed, candidates and the final mix).
>   - **Fix iterations.** At most **one** fix iteration after iteration 0, on the generator and templates only. This is stricter than A42-D 3.6's two, and matches A49 (d) and A52.
>   - **Hard deadline: Mon 19 Oct 12:00 UTC.** By then T46's selected 1,200 rows, its own dev and its replay tag must have passed every gate above except the final-mix G13. If they have not, T46 moves to C3, and the final all-block G13 (~14:00 UTC) is never delayed for it.
>   - **Own dev:** 300 rows (A42-D 4.4). It uses dev-only wordings, names, values and Arabic slot items, and at least one dev-only workflow skin (≥ 30% of dev). It is never trained. It and the probe file join the C2-side G13 dev targets. The A53 waiver does not apply to T46.
>
> - **(f) Pilot gate, applied as A42-D 4.**
>   - **The pilot:**
>     - 1,500 pilot rows from a seed range disjoint from the candidate, QC and dev seeds;
>     - one short LoRA pass from C1 with no replay, recipe A37 (i), seed 20261013;
>     - at most $0.30 on mahadikarya44, inside the $40 cap;
>     - verdict logged by **Mon 19 Oct 23:59 UTC** (A42-D 1.6).
>   - **Kept only if all of these hold:**
>     - **(i)** own-dev gain ≥ +2.0 pt (point);
>     - **(ii)** the existing dev drops by ≤ 0.5 pt;
>     - **(iii)** the G-proxy change is not rejected under 4.3;
>     - **(iv) a new harm veto, which only adds strictness:** on own-dev rows with cautious gold (hold-type, deny/stop, human/escalate), the pilot's accuracy is no more than 2.0 pt below C1's (point). This blocks trading caution for permissiveness.
>   - **If it fails:** T46 and its tagged replay unit leave the mix. Removing them is drop-only, so G13 is not re-run.
>   - **Lean:** the cautious lean per form (permissive and cautious, on own dev) is report-only. The target is |lean| ≤ 3 pp; C1 measured −7.3 / +5.5.
>
> - **(g) Fresh probe (`job3_disposition/probe/`, shard sha256 c82007086c750fe4fe1d…, key 529ca8a90a7d5d72dd3e…, `probe_analyse.py` a788032e606c1035a662…).**
>   - It is a C2-side diagnostic, report-only under its pre-registered R1-R5, and never trained. It is a G13 dev target. It decides nothing about T46: T46 is decided now, and its own pilot gate admits or rejects it.
>   - **When it runs:**
>     - The C1 read runs in the next free od-l4b window, as the investigator's command gives it. Nobody stops or restarts the VM for it.
>     - If T46 is piloted, the pilot adapter reads the probe too.
>     - Base-Qwen reads are optional, on the L4 only, and report-only.
>
> - **(h) What the mix must handle.**
>   - `mix_c2.py` re-runs every assert with T46 included: 40/60, 125,000, agent tier ≤ 55%, the one-family cap, free-form, tokens, the Arabic cap (d), and the T_max projection from real padded tokens (A42-D 2.3).
>   - The final all-block G13 input is the superset: it contains T46's selected rows, its tagged replay, its own dev, the probe and the A58 bench target. Any later removal is drop-only. Any change that adds a row re-runs G13 on the added rows.
>   - If T46 enters, its own dev joins the A42-D 9.3 pooled own dev.
>   - OHS-4 and the OHS-AC manifests are unchanged. T46 shares no oracle with the sealed mode, so the 3.6 sealed re-run does not apply.
>
> - **(i) How reports label the bench after C2.** If T46 enters, the System One Bench questions on invoice disposition, customer-service action, credential/security disposition and agent-trace action are marked "in-family after C2 (T46; items excluded by G13)", following A58 (f)'s rules. The bench never selects anything.
>
> - **(j) Incident log.**
>   - The investigating agent saw another chain's command line in a `ps` listing (one sealed read-split name, no contents) and ran one `ls -la` that printed only the directory's own entry. This is logged by description only, and the name is not repeated.
>   - The probe was authored and hash-checked before this happened, so it is kept.
>   - T46 is built by fresh agents that cannot see the JOB3 transcripts.
>   - New process rule: C2-side agents never list processes or directories that belong to other chains on a shared VM.
>
> - **(k) What does not change.** A42-D 1-14, A43-A58, every gate, bar and cap, the $40 and $34 caps, both owner GO points, the 96% / 98% usage rule, the never-open rules, and the A42-D block text and its sha256. The training-GO request reports T46's realised rows, the Arabic rows per block, the drops at each gate, the G6/probe tables, the lean per form, the pilot verdict and the probe's R1-R5 readout.

---

**Implementation steps for the Sonnet agent, in order. Stop at the first failure and report it.**

1. **Record the ruling.** Append the A59 block above to `lean/PREREG_FINAL.md` (append-only), then log its sha256. This is the orchestrator's step; check it is done before writing any code.
2. **Create `c2_build/families/T46/` from scratch:** `G0_SPEC.md`, `plugin.py` (a C2Plugin), `solver_b.py` (a different paradigm, for example a rule-table evaluator against the plugin's procedural decide), `fixtures.py`, `test_plugin.py` and `haiku/`.
   - Import only from `c2_kit`. Do not import from `job3_disposition/` or from any other family.
   - G0 must state every target in (c) and (d), the seed ranges (candidates, pilot, dev, QC bases 900000 / 11M / 12M / 13M, all disjoint), the T46 lexicon (label → one semantic class), the dev-only workflow skin and the free-form definition (ticket form).
3. **Wire T46 into the build.**
   - `c2_kit/plugin.py` FAMILIES: add `"T46": "agent"`.
   - `mix_c2.py`:
     - add T46 to AGENT and to a new `POST_FREEZE = ("T46",)` set;
     - include it in trim step "wave2" in proportion with T44 and T45;
     - exclude it from the program-family count, the agent-core count and the T40-T45 6,666 sum;
     - tag its replay as its own unit;
     - add an `ARABIC_CAP = 1500` assert over SB4 + SB5 + T46 rows with `meta.lang_state == "ar"`, with a seeded (20261013) proportional whole-unit SB4/SB5 trim if over.
   - `c2_select.py`, `gen_full_c2.py` and `qc_full_c2.py`: add T46 wherever these files list families.
   - Add unit tests for every change, and run the existing mix tests.
4. **Haiku pools (fresh agents, one task file each, `audit_cc_reads.py` on every transcript).**
   - English surface wordings and definitions, in train and dev-only partitions.
   - Arabic slot tables (names, reasons, notes with a program meaning class), in train and dev-only partitions.
   - G-LEX 2/2 blind reads, keeping only items that pass.
   - A program check that no Arabic slot value exactly equals any string in `probe_gen.py`'s `to_ar` tables (0 required). Freeze the pools and log their hashes.
5. **Pre-row checks.** The orchestrator confirms G0. Then run:
   - `test_plugin.py`;
   - G2 (solver A = solver B on ≥ 2,000 specs, 100%), G3, G4 (≥ 3 relations, ≥ 1,000 rows per sampler), G-SL, G3-H, and G-TPL through the run-only checkers;
   - the 3.3 reseed audit and the 3.2 probes;
   - A50 G6 (four 6,000-row builds; every cell mean ≤ chance + 2 pp), G7 and G13-seed.
   - On any failure: one fix iteration (generator or templates only, same seed bases), then T46 moves to C3 if it still fails.
6. **Generate the rows.** 1,800 candidates (at most 60 Arabic train rows in the final 1,200; at most 90 among the candidates), the 300-row own dev (30 Arabic, ≥ 30% dev-only workflow skin, in `data/c2_parts/T46/out/` so the c2_mixdev glob finds it) and the 1,500 pilot rows. Run `plan_report`, the polarity check and G15.
7. **Label checks.**
   - G5-H on 300 rows (≥ 120 without definitions, ≥ 30 Arabic): Sonnet does the first pass and Opus confirms every flag.
   - The 3.4 blind 5% Haiku re-derivation, then adjudication.
   - Drops only, never a relabel.
8. **Selection and decontamination.**
   - C1 crowd read (G9) of the candidates on od-l4b, using the SGLang path if A49 (f) passed. Do not stop or restart the VM. If no L4 window is free in time, a Modal fallback from the reserve is allowed only if the reserve stays ≥ $2 at the training GO.
   - Select down to 1,200 with the spec 5.2 bins. Check G10 on the selected rows.
   - Register the probe shard and T46's own dev as C2 dev targets in `g13_c2.py`.
   - Run G13 on the candidates. The decontamination program runs the 8-gram bench-wording check.
9. **Deadline check, Mon 19 Oct 12:00 UTC.** Either write `families/T46/qc/READY.json` (gates passed, shas) or write a C3 note. Then hand the superset to the final all-block G13.
10. **Pilot** (≤ $0.30 on mahadikarya44, recipe A37 (i), seed 20261013, 1,500 rows, no replay). Read the own dev, the 9 existing dev splits and the G-proxy. Apply (f) (i)-(iv) and write `families/T46/qc/PILOT_GATE.json` by Mon 19 Oct 23:59 UTC. If it fails, drop T46 and its replay unit from the mix (drop-only).
11. **Probe.** When od-l4b is next up, run the C1 probe read with the investigator's command, then `probe_analyse.py`. If a pilot adapter exists, read the probe with it too. Report-only.
12. **Report** into the training-GO request draft: T46 rows, Arabic rows per block against the 1,500 cap, drops at each gate, the G6/probe tables, the lean per form, the pilot verdict, the probe R1-R5 readout, the bench in-family labels and the (j) incident line.

Relevant paths:
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/PREREG_FINAL.md
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T46/ (to create)
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/c2_kit/plugin.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/mix_c2.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/c2_select.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/g13_c2.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/job3_disposition/probe/
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/sb_blocks/A58_DRAFT.md