# A61 adoption draft, revision 2 (unreviewed)

## ruling_text
> **Ruling A61 (17 Oct 2026; orchestrator ruling, Opus. Made under the owner's decision of 17 Oct 03:21 UTC, quoted in the draft. Draft: `c2_build/zed_orch/di_train/A61_DRAFT.md`, sha256 `ec261d2b9906382a936390d6531d2b16a39bbdad4e3061c8e92cc3cb0a1aeb62`, written 03:41 UTC. Adopted at the moment this text is appended here, which is after the DI block results. It is appended after A62 and the Post-freeze addendum and keeps its draft number. No gate, bar, cap, probe threshold or isolation rule is loosened. Drops only. Nothing is relabelled. Tag A61-HLE.)** The draft is adopted with the changes in (a) to (i). Each change is either stricter than the draft or records a result. **Outcome: no DI block enters C2. DI new rows are 0 and the DI part is 0. The draft's row-cap and money changes therefore do not take effect (e).**
>
> - **Times.** All times are UTC, taken from file times or the session log. This Mac's clock runs on EDT (UTC−4).
>   - The owner's decision is in the session log at 03:21 UTC.
>   - The draft labels the owner's decision "~04:40 UTC" and itself "~04:50 UTC". Both labels are wrong and are not used.
>   - Order of events:
>     - 03:21: the owner's decision;
>     - 03:41: the draft;
>     - 04:58: the first *recorded* DI 8.5 result (DI-LANG).
>   - DI-LANG's input form shows that earlier runs happened and were not recorded. Their times are unknown.
>
> - **(a) Draft (a) 7 as adopted (A42-D 8.5). Recorded HITs stand. There is no exemption, no hashing change and no re-run.**
>   - A42-D 8.5 (15 Oct) reads: "each source's identifiers (dataset name, publisher, host, upstream ID, licence page URL) go to the sealed-side checker … It returns **PASS or HIT per source only**, against the OHS-4 and OHS-AC source lists. A HIT removes the whole source." It has no platform exemption.
>   - A58 applied 8.5 as written to SB6, whose host is `github.com/google-research-datasets/tydiqa`: "**SB6 (TyDi QA yes/no) OUT** — 8.5 HIT".
>   - A16 (a) (3 Oct) reads: "Bare platform words (Wikipedia, Reddit, GitHub, arXiv, Zenodo, PubMed, ...) never match on their own."
>     - It sits in A16's deny-list bullet.
>     - A16.1 pins the tools that implement A16: denylist.py v1.2, deny_aliases.json v1.1, negcount.py v1.1 and replay_sample.py.
>     - denylist.py implements A16 (a) through its PLATFORM set.
>   - A16 (a) does not reach 8.5. 8.5 is a separate check, adopted 12 days later. Reading A16 (a) into 8.5 now would change a bar after HITs.
>   - **What the tool does.** `meta_src/source_name_check.py` has sha256 `72fe203a015aa4d5b292878dc871b21dcc4f0fdcab70e03fb142904b64fa1542`. It was last written 15 Oct 18:10, before every DI run.
>     - It hashes the five 8.5 identifiers.
>     - It also hashes extras: the dataset URL (its docstring says "extra, not required by 8.5"), the other hosts, and five strings built from each host. The extras make it stricter than 8.5.
>     - It reads the OHS-AC files "only if present" and exits 0. So until the (f) fix, no run proves which exports it read.
>   - **Binding input.** A source's binding input is every input file for that source written before its first recorded 8.5 result, unchanged. If there are several such files, all of them count, and their entries fold together. This one rule binds every source, including the ones that passed.
>   - **Valid PASS.** A PASS admits a source only if it meets all of these:
>     - it comes from one whole-file run by the orchestrator;
>     - the run used the source's binding input;
>     - every export was verified by the (f) integrity check.
>   - No PASS on record meets this. Every earlier PASS (md_*, SB5, gp_*) came before the (f) fix.
>   - **HIT.** A recorded HIT removes the source, whatever its input form or export set. A drop is never a loosening. Nobody examines which identifier produced a HIT.
>   - **No re-run and no readmission.** No source with a recorded 8.5 HIT is ever re-run or readmitted, in C2 or in C2.1, under any later rule. These sources are:
>     - DI-KR_gsm8k;
>     - di_hover;
>     - di_isarcasmeval;
>     - the nine DI-TS sources of `zed_orch/di_train/work/di_ts_sources.json` (ts_logical_entailment, ts_temporal_nli, ts_perspectrum, ts_lonli, ts_spacenli, ts_wice, ts_fol_nli, ts_recast, ts_tracie). All nine have github.com licence pages, and R7 records that "EVERY GitHub-licensed candidate returns HIT";
>     - SB6_tydiqa;
>     - md_fdc;
>     - md_peps.
>
> - **(b) Draft (a) 5 as adopted (deny-list).**
>   - **Adopted text:** "`c_src/common/denylist.py check --fail-on-taint`, run by the orchestrator on the full provenance query (dataset, config, split, every upstream source). A taint verdict removes the source, with no override."
>   - **Struck from the draft**, because these lines describe the replay path, not `check`:
>     - "A `di_test` taint scoped to a split blocks only that split. That is the owner's decision, and the deny-list already scopes it that way.";
>     - "The deny-list taints only its test split (`3G#25.1`, `di:GSM8K`).";
>     - "… only its DI split (`3G#25.2`)" (HoVer);
>     - "… only its DI split" (iSarcasmEval).
>   - **Grounds:**
>     - The pinned denylist.py v1.2 (`e268d566…`): `verdict_new` says "New data (public, commit, packs): taint anywhere in the item or its parents denies". It never reads scope. Only `verdict_replay` reads scope.
>     - Test `test_denylist.py:308` (commit 6d79bf2, 4 Oct 02:15 UTC) asserts that the query "ParticleMedia/RAGTruth (Summary task, train split)" is taint.
>     - DENY_CLASSES.md: the class text says `taint` "denies the dataset as new data". The scope text's only stated carve-out is "replay rows from the train split are kept".
>   - The owner's quoted decision asks for "commercial-licence train splits". It names no deny-list rule. A split-aware `check` goes to C2.1 (h 1). That carries the owner's intent forward without changing a tool after its verdict.
>   - **A17-B1 is distinguished, not overruled.**
>     - A17-B1 reads: "Clean maths set for the B1/B2 rules: GSM8K TRAIN, a seeded 500 items, frozen now. The deny-list blocks only GSM8K test, and the Decision Index uses test items."
>     - That set is a frozen evaluation set for the think rules. It is not training data, and no `check` was run for it.
>     - Its sentence says which items the entries mark (their scope). It does not rule on the new-data verdict.
>     - The set stays frozen as it is.
>   - The C1 replay drop_part results (arc, binj_offensive, clinc150, gd_ragtruth_summary, gd_winogrande; `c_build/replay_denylist_verdicts.json`) come from `verdict_replay`. They are unchanged.
>
> - **(c) Blocks. All five DI blocks are OUT on one ground: no DI source has a valid 8.5 PASS (a), so draft (c) 2 ("PASS is required") is unmet.** This ground needs no breach output.
>   - **DI-KR (GSM8K main train): OUT.** Two further records would each remove it on their own:
>     - the whole-source 8.5 HIT: `DI-KR/work/qc_stage1.json` (05:23), on `SOURCES_DIKR_85.json` (05:20);
>     - the `check` verdict deny (05:14): taint, entries `3G#25.1` and `di:GSM8K`, scope split, cat di_test, exit 3.
>   - **DI-LANG: OUT.**
>     - Recorded HITs: di_hover and di_isarcasmeval (`DI-LANG/provenance/name_check_result.txt`, 04:58).
>     - di_hotpotqa_wiki passed in that same run. That PASS is not valid under (a) and admits nothing. The source was only HoVer's evidence text and had no task.
>     - The deny-list was never run.
>   - **DI-TS: OUT.**
>     - The recorded HIT is R7 in `DI-TS/rulings/R1_TASK.md` (05:16).
>     - Its input is inferred, not recorded. It is most likely `work/di_ts_sources.json` (05:05).
>     - `DI-TS/SOURCES_DITS_85.json` (05:53) is a re-shape made after the HIT: it drops the licence page URL and adds huggingface.co and `#alt` rows. It is not run.
>     - R7's verdict "invalid" on the SPDX variant stands. R7's re-run instruction is overruled.
>     - The deny-list verdict was pass (`work/dits_prov_verdicts.json`), but the driver ran it, not the orchestrator as A58 requires. It no longer matters.
>   - **DI-RC and DI-TOOLS:** empty, as drafted. They move to C2.1.
>   - **Counts for the record** (none of these rows enters):
>     - DI-KR: 7,473 → 6,943 gold-checked → 3,594 candidates + 300 dev; A46 −6.
>     - DI-LANG: A46 −661 (457 wrong gold, 204 ambiguous); 3,816 candidates + 265 dev.
>     - DI-TS: 4,378 candidates + 294 dev; Opus −54.
>   - **Records.**
>     - Each of the five `data/c2_parts/<B>/qc/QC_REPORT.json` files gets an `a61` object holding a verbatim copy of its top-level fields.
>     - Then `pass` is set to false, because mix_c2.py `admission` gates on it.
>     - Every mix run passes `--leave-out DI-KR DI-LANG DI-TS DI-RC DI-TOOLS`.
>     - The built pools stay on disk, unused.
>     - Draft (c) 9-12 do not run for the DI blocks: no DI candidates G13, no crowd selection, no pilot. Cost $0.
>
> - **(d) Breaches recorded.** None of them changes an admission. All are disclosed at GO #1.
>   - Builder code was written before any valid PASS in DI-KR, DI-LANG and DI-TS. That breaks draft (a) 7 and the order of work in (c).
>   - Block drivers ran the 8.5 checker themselves on per-identifier, blank-field and variant inputs. These runs probed the sealed keyword set:
>     - DI-KR's `split_by_identifier`;
>     - DI-TS's `work/di_ts_sources_*` and `work/v_*` runs, which R7 describes;
>     - DI-LANG leaving fields out after earlier runs.
>   - Their outputs are breach output. They are never cited and never shape an input or a ruling. This ruling rests on (a)'s valid-PASS rule and on whole-source HIT records. HIT records are used only to drop.
>   - The DI-TS deny-list `check` was run by its driver.
>   - A fact-gathering agent read 20 PASS/HIT lines of `meta_src/name_check_ohs4_result.txt`. Nothing relies on them.
>   - **From now on:**
>     - only the orchestrator runs `source_name_check.py`;
>     - it runs once per stage, on whole input files that this ruling fixes;
>     - there is no per-identifier, blank-field or variant run;
>     - nothing an earlier run showed shapes an input.
>
> - **(e) Money, rows and payers with the DI part at 0.**
>   - The owner gave the Modal reserve "for the extra training". No extra training exists, so the draft's (f) row-cap change and (g) money change do not take effect. A42-D 2.1-2.3 stand:
>     - **C2 Modal total ≤ $40** ("No line may take the total above $40"). Training ≤ $34.
>     - **T_max = T_core = min($34, $32 − C2 Modal spend to date)**, fixed at the training GO.
>     - A37 (k) steps 100-300 stop-and-ask: above this T_max.
>     - After training, each line runs only if spend to date plus its projection is ≤ $40. SPEED-3 runs last, in full or not at all.
>   - **Rows:** core ≤ 125,000 (A40 d, A42-D 1.4). With the DI part at 0, the whole mix is ≤ 125,000. The 50,000-row floor (stop and ask) is unchanged.
>   - **Payers.** This sets payer order, not a cap. Free credit only, with balances read live and logged before launch, in this order: mahadikarya2, mahadikarya3, jaypatil-duke, atmosphor, arya-mahadik-ai, mahadikarya44.
>     - aryamhd is never used. A card use needs a new owner ruling that names the amount (A42-D 2.4).
>     - If live free credit cannot cover T_core plus evaluation, SPEED-3 and the $2 reserve, T_core is lowered to fit, and the A42-D 2.3 trim order applies.
>     - GO #1 states that trim, the dollar figure that would avoid it, and the live balance per account.
>
> - **(f) 8.5 tool fixes and the final-mix check.**
>   - **Pins.** These files are untracked in git, so their sha256 values are logged here before any edit:
>     - `source_name_check.py`: `72fe203a…1542`, with a copy in `c2_build/_backup_a61/`;
>     - `meta_src/SOURCES_CANDIDATES.json`: `644cb9f5…f5f7`, written 15 Oct 18:09:58, one second before its result and never edited since;
>     - `zed_orch/sb_blocks/SOURCES_SB56_85.json`: `c4a9f5f5…1c4b`;
>     - `zed_orch/sb_blocks/SOURCES_SB5_85.json`: `bdb1e171…f4e`.
>     - The post-edit sha256 of the tool is logged before its first run.
>   - **Fold.** This implements "PASS or HIT per source only".
>     - Entries with id `<id>` or `<id>#…` fold into source `<id>`, and duplicate ids fold too.
>     - A source is a HIT if any of its entries hits. The tool prints one line per source.
>     - The fold can turn a PASS into a HIT, never the reverse.
>   - **Export integrity under `--exports all`.** This implements "against the OHS-4 and OHS-AC source lists" and the Post-freeze addendum: "the union of this export and the freeze export `27808b0c…` binds every later G13 / admission check".
>     - The tool requires and verifies three exports:
>       - OHS-4: MANIFEST sha256 `3771b47a…5470b`, which is g13_c2's pin, naming the A38 freeze `c0217e77…09c3`;
>       - the OHS-AC final export: MANIFEST `fadec66f…cd9b`;
>       - the OHS-AC freeze export: MANIFEST `27808b0c…3f6e`.
>     - It checks each keyword file against its MANIFEST.
>     - If an export is missing or does not match, it prints only "<export> missing" or "<export> MISMATCH", gives no verdict, and exits 2.
>     - It still reads the OHS-AC preliminary file when present.
>     - `--exports ohs4` never gives a binding verdict.
>   - **"Hashing unchanged" is tested, not assumed.** These tests run before the fixed tool is used:
>     - (1) `source_hashes()` returns identical sets under the old and new code for every entry of the five recorded inputs: SOURCES_CANDIDATES.json, SOURCES_SB5_85.json, SOURCES_SB56_85.json, SOURCES_DIKR_85.json and DI-LANG `name_check_sources.json`. The test loads no sealed file and prints only booleans and counts.
>     - (2) The source text of g13_c2's `keyword_hashes`, `URL_RE`, `sha_hex` and `KW_STRIP` is byte-identical in 904d914c, 213634d7, 32256eaa and every later g13_c2.py used here. It is identical in the first three today.
>     - (3) The fold and the integrity check are tested only on fixture export folders that the test itself creates.
>     - If any test fails, the tool is not used, and the final-mix 8.5 is incomplete.
>   - **Freeze export restore.**
>     - The freeze export is not on disk as a separate copy.
>     - A fresh sealed agent re-exports the frozen items into a folder of their own.
>     - The copy binds only if its MANIFEST sha256 equals `27808b0c…3f6e` exactly.
>     - One restore serves this check, A57 step 6 and A64 (h) if A64 is adopted.
>   - **Scope of the final-mix run.** It runs only on the 8.5-gated sources that have at least 1 row in the final mix, after the final all-block G13 drops and every trim. These are the metadata-block sources (row source `c2_md_<x>` maps to `md_<x>`) and SB5 if it enters (`c2_sb5` maps to `SB5_uci293`).
>     - A row whose source maps to no id in the binding inputs makes `--final` refuse.
>     - md_met, md_fdc, md_peps, the unchosen md sources and gp_* are not run.
>   - **Input.**
>     - `mix_c2.py --final` writes the membership list.
>     - One input file copies, unchanged, every entry of those sources from their binding inputs:
>       - SOURCES_CANDIDATES.json for md_*;
>       - both SB5 files for every `SB5_uci293` and `SB5_uci293#…` entry.
>     - No field is added, removed or reshaped for any source.
>     - The sha256 of each binding input and of the built file is logged before the run.
>     - It is one run, by the orchestrator, with `--exports all`.
>   - **Incomplete check.** If the check is incomplete (exit 2, failed tests, or no restored freeze export), no 8.5-gated source has a valid PASS. Every one of them is removed by the path below.
>   - **After a HIT or an incomplete check.** This path is fixed now, before the result. Every step only drops rows, and nothing refills.
>     1. `mix_c2.py --remove-sources <file>` loads the written final mix. It removes every row of the named sources, with their relation units and twins, through `mx.drop_rows`. It adds no pool row.
>     2. It runs `fit_block_in_mix(META_BLOCK, …)`: the A42-D 8.2 caps (source ≤ 15%, domain ≤ 20%), by whole tasks, seeded. This is the same call `apply_targets` makes after every metadata reduction. `merge_md.fit` (the builder stage, with its 40-task floor) is not used.
>     3. It runs `finish()`'s steps after the refill loop, unchanged, with no refill: `plan_shares`, then `apply_targets` if the agent cap applies; `replay_to_rule`; `budget_trim_a61`; `a60_enforce` (A60 c-e) with `replay_to_rule`; `arabic_cap_trim`; `tag_replay_unit`; then `gates()`.
>     4. Inside `gates()`, `block_rules(META_BLOCK, …, proportional_trim=<this mix's budget.proportional_used>)` asserts 8.2. It requires at least 8 domains. The 8,000-row floor is waived only after spec 5.5's proportional step, and an 8.5 removal is not that step. If 8.2 fails, the metadata block is removed whole by step 1, and steps 3-4 run again.
>     5. An SB5 HIT removes SB5 by step 1.
>     6. Any other gate failure: stop at GO #1, no training.
>     7. There is no second 8.5 run, because a removal adds no source. Preflight refuses unless every 8.5-gated source left in the mix had a PASS line in that one run, on the input whose sha256 was logged.
>   - **G-proxy, disclosed.**
>     - The gp_* PASSes (A42-D 12.2) rest on OHS-4 plus the AC preliminary file only.
>     - This ruling does not re-check them. The G-proxy is never trained, its file is frozen (12.2: "never edited afterwards"), and no remedy for a HIT was fixed before the G-proxy was used.
>     - GO #1 states this. Any re-check needs its own ruling, and that ruling must fix the remedy first.
>
> - **(g) G13 targets and g13_c2.py predecessors.**
>   - **Targets:**
>     - `di_test` is unchanged.
>     - `di_src_splits` is complete (`g13_di/di_pins.json`).
>     - `di03_public` is rebuilt on a quiet Mac by the draft's (e) 2 fallback, before the Mon 19 Oct ~14:00 UTC run.
>   - **A61-HLE.** The coverage gap "HLE not scanned (gated)" (HLE, 513 requests) is accepted for `di03_public` only. Any other gap leaves the target incomplete.
>     - If `di03_public` is incomplete at that run, the final run proceeds against every other target, and GO #1 says so.
>     - If it is complete, both DI targets bind on every block of the final mix (c 12).
>   - The DI quarantine files stay never-train (`g13_di/di_never_train.json`).
>   - **Predecessor shas.** Two shas join REFRESH_COMPATIBLE_TOOL_SHAS: `213634d77c868e28a6130cc13fb2910c032f88d1d37811c829bd5edf3db8853c` (`_backup_a61/g13_c2.py`) and `32256eaa2328c5029b02b2835ff00cb97bb34cd3abf748db0d6631e680b75776`. They join only after tests show all of these:
>     - (1) For a non-DI fixture block, each predecessor's candidates log equals the new code's log field for field. The only exceptions are g13_c2's fixed bookkeeping list: `wall_s`, `unix`, `engine.embed_stats`, the checkers' `wall_s` and the top-level `refreshed` list. `refresh-dev --check` accepts the log, and the refresh equals a full run.
>     - (2) The A61 hunks are the only difference. If the sob_wiring patches are applied in the same window, exactly their hunks are allowed too, and SB5 then gets a full candidates run.
>     - (3) No non-DI target spec reaches `decision_index_03/`. The added QUARANTINE_OK paths change no `allowed()` answer and no file set of a non-DI target.
>     - (4) `needs_di` is False for every non-final run.
>   - Test (3) runs inside the process and outputs only booleans and counts. It never prints or logs a path (`_NO_ECHO`). Only the orchestrator runs it.
>   - The edit is made only when no G13 run is live. If any test fails, the blocks get full candidates runs.
>
> - **(h) Reports and C2.1.**
>   - **In C2,** the DI is report-only. No DI train split is trained, so the draft's in-family and task-type labels do not apply. DI tables state "no DI train split trained in C2".
>   - **C2.1 needs all of these before any check runs on a DI train split:**
>     1. a PREREG rule for a split-aware `check`, with a declared split field and tests, adopted before that check runs;
>     2. the (a) bar: no source with a recorded 8.5 HIT is re-run or readmitted;
>     3. 8.5 changes stricter only: a change to 8.5's hashing, identifier list or exports may only add hashes, identifiers or exports. It binds every source alike, including those that passed (md_*, SB5, gp_*). There is no platform-host exemption.
>   - The draft's (i) list (harder program-gold families, DI-RC, DI-TOOLS, head and loss ideas) stays recorded only.
>
> - **(i) Unchanged, and what this ruling changes.**
>   - **Unchanged:**
>     - every adopted gate, cap and bar through A62 and the Post-freeze addendum;
>     - the 40/60 split and the 1.5× replay;
>     - both owner GO points;
>     - the 96% usage stop and the 98% ceiling;
>     - the never-open rules;
>     - the A42-D block text and its sha256.
>   - **Changed:**
>     - the G13 target registry, which gains `di03_public` and `di_src_splits`;
>     - `source_name_check.py` (f);
>     - `mix_c2.py`: `--remove-sources`, the membership list, and the money and row constants back to A42-D 2.1-2.3 and 1.4;
>     - `train/c2_check.py`: the money constants;
>     - the five DI QC records.
>   - **The GO #1 request lists:**
>     - per DI block: 0 rows, drops by step, the A46 counts, the recorded 8.5 and deny-list verdicts as counts, and the breaches in (d);
>     - the HLE gap;
>     - the final-mix 8.5 counts and any removal;
>     - the G-proxy disclosure;
>     - the money basis in (e).

## per_source
DI-KR_gsm8k (GSM8K main train): OUT. There is no valid 8.5 PASS. It has a recorded whole-source HIT (DI-KR/work/qc_stage1.json, 05:23, on SOURCES_DIKR_85.json sha ddffa28a…). The deny-list check verdict is deny: taint, entries 3G#25.1 and di:GSM8K, scope split, exit 3. It is barred for good (A61 a): never re-run or readmitted.
di_hover (HoVer train): OUT. No valid PASS; HIT recorded at 04:58 (DI-LANG/provenance/name_check_result.txt). Barred for good.
di_isarcasmeval (English train): OUT. No valid PASS; HIT recorded at 04:58. Barred for good.
di_hotpotqa_wiki (HoVer evidence text only): not admitted. Its PASS came from DI-LANG's re-shaped run, made before export verification. That PASS is not valid and admits nothing. It had no task. It is not on the HIT bar, but it has no route into C2.
DI-TS: ts_logical_entailment, ts_temporal_nli, ts_perspectrum, ts_lonli, ts_spacenli, ts_wice, ts_fol_nli, ts_recast, ts_tracie (work/di_ts_sources.json, 05:05, all with github.com licence pages): OUT. No valid PASS. R7 records a HIT for every GitHub-licensed candidate. All nine are barred for good. SOURCES_DITS_85.json, the post-HIT re-shape, is never run. The deny-list pass in dits_prov_verdicts.json was run by the driver and no longer matters.
DI-RC, DI-TOOLS: 0 rows. They move to C2.1. QC pass is set to false.
md_cma, md_cordis_h2020, md_fsa, md_gbif, md_gene_ontology, md_geonames, md_musicbrainz, md_openalex, md_ror, md_usgs, md_worldbank: provisional. Their PASSes were on OHS-4 plus the AC preliminary file only, so none is a valid PASS yet. Each enters only if it has at least 1 final-mix row and gets a PASS in the single final-mix run (--exports all, verified exports). That run uses its unchanged SOURCES_CANDIDATES.json entry (sha 644cb9f5…). A HIT or an incomplete check removes the source through the fixed drop-only path. md_cma's input is not changed, even though it holds github.com/ClevelandMuseumArt.
md_met: not in the mix and not run.
md_fdc, md_peps: recorded HITs. Barred for good.
SB5_uci293: provisional. It enters only on a PASS in the same final-mix run, using every SB5 entry of both pre-result files (SOURCES_SB56_85.json c4a9f5f5… and SOURCES_SB5_85.json bdb1e171…, folded together). A HIT or an incomplete check removes SB5.
SB6_tydiqa: OUT (A58), recorded HIT. Barred for good.
SB4: OUT per A58. No 8.5 run was ever requested, and none is run now.
gp_* (G-proxy): PASS on OHS-4 plus the AC preliminary file. Not re-checked by this ruling; disclosed at GO #1. A re-check needs its own ruling, with the remedy fixed first.

## program_fixes
Each fix below says which rule it implements and quotes that rule. Every rule was registered before the result the fix affects.

1. c2_build/meta_src/source_name_check.py: FOLD.
- Pre-edit sha256 is 72fe203a015aa4d5b292878dc871b21dcc4f0fdcab70e03fb142904b64fa1542 (untracked). Back it up to c2_build/_backup_a61/source_name_check.py.
- Behaviour: entries with id <id> or <id>#…, and duplicate ids, fold into source <id>. The source is HIT if any entry hits. The tool prints one line per source.
- Implements A42-D 8.5 (15 Oct): "It returns **PASS or HIT per source only**".
- Effect: stricter only. It can turn a PASS into a HIT, never the reverse.

2. c2_build/meta_src/source_name_check.py: EXPORT INTEGRITY under --exports all.
- It requires and verifies OHS-4: the MANIFEST sha must equal g13_c2's SEALED_HASHES_MANIFEST_SHA256 3771b47a…5470b, naming the A38 freeze c0217e77…09c3. Reusing g13_c2's existing OHS-4 export-check class is allowed.
- It requires the OHS-AC final export (MANIFEST fadec66fdb38…cd9b) and the OHS-AC freeze export (MANIFEST 27808b0ccbaf…3f6e, from the restored folder).
- It checks each keyword file's sha256 against its MANIFEST.
- On a missing or mismatched export it prints only "<export> missing" or "<export> MISMATCH", gives no verdicts, and exits 2.
- The AC preliminary file is still read when present.
- Implements A42-D 8.5 "against the OHS-4 and OHS-AC source lists". It also implements the Post-freeze addendum (~05:35 UTC): "the union of this export and the freeze export `27808b0c…` binds every later G13 / admission check". The final-mix run is a later admission check.

3. Tests for 1 and 2: c2_build/tests/test_source_name_check_a61.py.
- (a) For every entry of SOURCES_CANDIDATES.json, SOURCES_SB5_85.json, SOURCES_SB56_85.json, SOURCES_DIKR_85.json and DI-LANG name_check_sources.json, source_hashes() is identical under the old module (_backup_a61) and the new one. The test loads no sealed file and prints booleans and counts only.
- (b) The source text of g13_c2 keyword_hashes, URL_RE, sha_hex and KW_STRIP is byte-identical in _backup_refresh (904d914c), _backup_a61 (213634d7), the current file (32256eaa) and the post-window file.
- (c) The fold, duplicate ids, exit 2 on missing and exit 2 on MISMATCH are tested on fixture export folders that the test creates under tmp. The sealed folders are never touched.
- Rule implemented: A61 (f), "Hashing unchanged" is tested, not assumed.

4. c2_build/mix_c2.py (pre-edit sha c448994b…; back up to _backup_a61/mix_c2.py).
- (a) --final writes the membership list c2_build/logs/a61_85_membership.json. It lists the 8.5-gated sources with at least 1 final-mix row, mapping c2_md_<x> to md_<x> and c2_sb5 to SB5_uci293. A row whose source has no mapping makes --final refuse.
- (b) New --remove-sources FILE, drop-only. It loads the written final mix, removes every row of the named sources with their relation units and twins (mx.drop_rows), and adds no pool row. It then runs fit_block_in_mix(META_BLOCK); the tail of finish() after the refill loop, without refills (plan_shares/apply_targets, replay_to_rule, budget_trim_a61, a60_enforce + replay_to_rule, arabic_cap_trim, tag_replay_unit); and gates(). If block_rules(META_BLOCK, proportional_trim=<recorded>) fails, MD is removed whole the same way and the tail and gates run again. Any other failure refuses.
- (c) Preflight refuses unless every 8.5-gated source in the mix has a PASS line in the single logged 8.5 result, with an input sha that matches the log.
- Implements A42-D 8.5: "again on the final mix" and "A HIT removes the whole source". Also A42-D 8.2 (the caps and the 8,000 floor as mix_c2 defines them) and spec 5.3 (a block that fails is left out, nothing refills). All are fixed before the final-mix result.
- Tests (fixture): no id is ever added; an MD source removal refits caps; an 8.2 failure removes MD whole; an SB5 removal works; replay follows floor(1.5 × new); preflight refuses on membership mismatch.

5. c2_build/mix_c2.py constants.
- C2_MODAL_CAP_USD changes from 45 to 40, T_MAX_CAP/T_MAX_BASE from 39/37 to 34/32 (so T_max = T_core), and ROWS_MAX from 150000 to 125000. An assertion that there are 0 DI rows is an equivalent alternative.
- c2_build/train/c2_check.py (pre sha 14648f6c…; back up): CAP_TOTAL, TMAX_CAP and TMAX_BASE change from 45/39/37 to 40/34/32. The formula string becomes "min(34, 32 - spend to date)".
- Implements A42-D 2.1: "No line may take the total above $40. Only a new owner ruling can change the cap." Also A42-D 2.3: "T_max = min($34, $32 − C2 Modal spend to date)", and A40 (d) / A42-D 1.4 (125,000). The owner's reserve grant covered only "the extra training", and the DI part is 0.
- Update the mixer and train tests that assert the A61 constants. Both suites must pass.
- The relay list (PROFILES/RELAY_ACCOUNTS) is unchanged: free credit only, never aryamhd.

6. c2_build/g13_c2.py: add 213634d7… and 32256eaa… to REFRESH_COMPATIBLE_TOOL_SHAS, only after the A61 (g) tests (1)-(4) pass, in the single code-edit window, with no G13 run live.
- Implements g13_c2's own refresh contract, which predates the result (docstring lines 105-109 and comment 1557-1562): a predecessor is valid when its "full-run code path is the same" and "the merged log is what a full run on the current files writes, field for field, apart from bookkeeping: wall_s, unix, engine.embed_stats, the checkers' wall_s and the new top-level "refreshed" list".

7. Records, not tools: in data/c2_parts/{DI-KR,DI-LANG,DI-TS,DI-RC,DI-TOOLS}/qc/QC_REPORT.json, add an a61 object holding a verbatim copy of the prior top-level fields, then set pass to false. These are drops, under draft (c) 2 "PASS is required" and mix_c2 admission "QC pass is not true".

8. Deliberately NOT changed:
- c_src/common/denylist.py: a split-aware check is C2.1, under its own PREREG rule.
- g13_c2 keyword_hashes, URL_RE, sha_hex, KW_STRIP: no hashing change and no platform stoplist.
- Every 8.5 input file: none is edited.

## orchestrator_commands
All paths are under /Users/aryamahadik/Documents/jev/opendecide-data/lean. Run from lean unless a step says otherwise. No step opens an ohs or sealed path on the C2 side. No checker runs except in step 9.

1. ADOPT
- Write the ruling_text to c2_build/zed_orch/di_train/A61_FINAL.md.
- Run `date -u +%H:%M`, then append the file to PREREG_FINAL.md as written.
- Log in HANDOFF.md: the adoption time (UTC), the sha256 of PREREG_FINAL.md after the append, and the A61_FINAL.md sha256.

2. DI QC RECORDS
For B in DI-KR DI-LANG DI-TS DI-RC DI-TOOLS:
- run a 10-line python -I script that loads data/c2_parts/$B/qc/QC_REPORT.json;
- it sets j['a61'] = {'ruling':'A61','outcome':'OUT (no valid 8.5 PASS; A61 c)','prior_top_level': {k: j[k] for k in j if k!='a61'}} and then j['pass'] = False;
- it writes the file back;
- log the sha256 before and after in c2_build/zed_orch/di_train/A61_EDIT_RECORD.json.
From now on, add `--leave-out DI-KR DI-LANG DI-TS DI-RC DI-TOOLS` to every mix_c2.py run.

3. SINGLE CODE-EDIT WINDOW
- Start only when `pgrep -fl g13_c2.py` prints nothing.
- Pin and back up before editing:
  - meta_src/source_name_check.py: 72fe203a015aa4d5b292878dc871b21dcc4f0fdcab70e03fb142904b64fa1542;
  - mix_c2.py: c448994b…;
  - train/c2_check.py: 14648f6c…;
  - g13_c2.py: 32256eaa….
  Copy each with `cp c2_build/<f> c2_build/_backup_a61/` and verify it with `shasum -a 256`.
- Brief one Sonnet code agent with program_fixes 1-6. The brief must state:
  - never open or list any path containing ohs or sealed;
  - never run source_name_check.py on real exports;
  - tests use fixture folders under tmp only;
  - print booleans and counts only.
- Run in c2_build:
  - `../../.venv/bin/python -B -m pytest tests/test_source_name_check_a61.py`;
  - the mixer suite;
  - the train suite.
- Run the g13 REFRESH tests (1)-(4) in-process (boolean output only). Only if all of them pass, add the two shas.
- Apply sob_wiring.patch and sob_wiring_tests.patch in this same window if they are planned.
- Then get one Opus skeptic review of the diff.
- Log the post-edit sha256 values in A61_EDIT_RECORD.json.

4. FREEZE EXPORT RESTORE
- This restore is shared with A57 step 6 and A64 (h).
- Brief a fresh sealed agent under AC_SEALED_BRIEF to re-export the frozen items as a hash-only export into c2_build/sealed_hashes_ac_freeze/.
- The orchestrator receives only the MANIFEST sha256. It must equal 27808b0ccbaf69aae058745ef0e80db6f5b692648198f26161bf749c3f1c3f6e. Record PASS or FAIL in A61_EDIT_RECORD.json.

5. di03_PUBLIC
- On a quiet Mac (load below about 4, no G13 run live), run `bench/external_quarantine/decision_index_03/venv/bin/python -B c2_build/g13_di/di_rebuild.py run --skip-download`, then `di_register.py finalize` and `di_register.py export`.
- Check that g13_di/di_pins.json has di03_public set to true, with only the A61-HLE gap. Otherwise record it as incomplete for GO #1.

6. FINAL ALL-BLOCK G13 (Mon 19 Oct ~14:00 UTC), as planned.

7. MIX
- Run `c2_build/mix_c2.py --final ... --leave-out DI-KR DI-LANG DI-TS DI-RC DI-TOOLS`.
- This writes c2_build/logs/a61_85_membership.json.

8. BUILD THE 8.5 INPUT
- Use a python -I script that takes the membership ids and builds c2_build/zed_orch/di_train/A61_FINAL_85_INPUT.json = {"sources": [...]} by copying entries unchanged:
  - for each md id, every entry of meta_src/SOURCES_CANDIDATES.json (sha 644cb9f5b6ca34dc5e5ac21b021bc559c2bb465d66bf7baf720b254cdd86f5f7) whose id equals that id or starts with id+'#';
  - for SB5 (only if it is in the membership), every entry with id SB5_uci293 or SB5_uci293#… from zed_orch/sb_blocks/SOURCES_SB56_85.json (sha c4a9f5f555838a548a844f165b2571c9f39a79dce89babcc5dc1e358f0fc1c4b) and from zed_orch/sb_blocks/SOURCES_SB5_85.json (sha bdb1e171ec59601ab3cc0cd215e2e215bb788ee0ef10a506f3831b8aa2a09f4e).
- No other entry is copied, and no field is edited.
- Before the run, verify the three binding shas and log them together with the sha256 of the built file.

9. ONE 8.5 RUN (orchestrator only)
- Run `cd c2_build && ../../.venv/bin/python -B meta_src/source_name_check.py --file zed_orch/di_train/A61_FINAL_85_INPUT.json --exports all > zed_orch/di_train/A61_FINAL_85_RESULT.txt; echo $? > zed_orch/di_train/A61_FINAL_85_EXIT.txt`.
- Record the PASS and HIT counts and the HIT ids. Do not re-run it.

10. REMOVAL (if needed)
- If the exit code is 2, the tests in step 3 failed, or step 4 failed, write every membership id to c2_build/logs/a61_85_remove.json.
- Otherwise write every HIT id there.
- If the file is non-empty, run `c2_build/mix_c2.py --final --remove-sources c2_build/logs/a61_85_remove.json`.
- If anything other than the MD block's 8.2 check fails: stop, no training, report at GO #1.

11. PREFLIGHT
- Run it as usual. It must confirm that every 8.5-gated source in the mix has a PASS line in A61_FINAL_85_RESULT.txt and that the input sha matches the log.

12. GO #1 REQUEST
Include:
- DI: 0 rows, with per-block drops by step, A46 counts, 8.5 and deny-list verdict counts, and the (d) breaches;
- the HLE gap and the di03_public status;
- the final-mix 8.5 counts and any removal, plus the MD 8.2 outcome;
- the G-proxy disclosure;
- the money basis: $40 cap, T_max = T_core = min($34, $32 − spend), live balance per relay account, and any trim with the dollar figure that would avoid it;
- the fact-gathering breach (20 lines of name_check_ohs4_result.txt).

## risks
REVIEWER POINTS: HOW EACH IS HANDLED
1. Truncation: accepted. The text is now complete, from (a) to (i).
2. Readmission route in (g)(2): accepted. (a) now names every source with a recorded HIT: DI-KR_gsm8k, di_hover, di_isarcasmeval, the nine DI-TS sources, SB6, md_fdc and md_peps. None is ever re-run or readmitted. (h)3 allows only stricter changes to 8.5 and no platform-host exemption.
3. Money: accepted. With the DI part at 0, the $40 cap and T_max = T_core = min(34, 32 − spend) apply again. A37 (k) and the post-training checks use these, and mix_c2/c2_check constants are reverted. Partly rebutted on the relay: the six-account list is a payer order of free-credit accounts, not a money bar, and these accounts have paid for C lines before (PREREG :1721). Every dollar stays capped at $40, and aryamhd is never used. The list is kept.
4. "Implements 8.5 as written": accepted. The text now says the tool hashes more than 8.5 requires (stricter) and that it checked OHS-AC "only if present" with exit 0, so no earlier PASS is valid. The gp_* PASSes are disclosed and not re-checked.
5. Post-freeze addendum: accepted. The HITs now rest on 8.5's own text and on "a drop is never a loosening". The addendum is cited only for the later final-mix check, which it does bind.
6. Selective citation: mostly accepted. All DI blocks are now OUT on one ground, "no valid PASS", which needs no breach output. The hotpot PASS admits nothing. Partly rebutted: using recorded HITs to DROP while giving no weight to PASSes from the same runs is not selective. It is the stated asymmetric rule (a HIT on any form removes; only a valid PASS admits), and it always errs toward dropping.
7. A17-B1: accepted. It is distinguished (frozen evaluation set, not training data, no check run, it states entry scope only) and left frozen. The replay precedents are kept on the replay path.
8. Fit function: accepted. The exact path is named: fit_block_in_mix(META_BLOCK), then finish()'s steps after the refill loop, then gates()/block_rules. merge_md.fit is explicitly excluded. This is fixed before the result. The ruling makes no input change for md_cma, even though a full-export HIT may be foreseeable.
9. Tool verification: accepted. The pre-edit sha 72fe203a… is pinned. source_hashes() must be identical on the five recorded inputs, and keyword_hashes, URL_RE, sha_hex and KW_STRIP must be byte-identical across versions. I checked these four today: they are identical in 904d914c, 213634d7 and 32256eaa. The binding input shas are pinned.
10. Bookkeeping fields: accepted. g13_c2's own list is cited.
11. Smaller items: accepted. The owner's time is 03:21:11 UTC (session log), before the draft at 03:41. Adoption is defined as the moment of the append, with the time logged by the command. 04:58 is called the first RECORDED result. The test commit time is 4 Oct 02:15 UTC.

REMAINING RISKS
- The freeze export (27808b0c) may not be restorable. The final-mix 8.5 is then incomplete, and the MD block and SB5 are removed with no refill. The mix shrinks; check the 50,000 floor and the minimum to train.
- md_cma (and possibly other md sources) may HIT against the full exports. MD may then fail 8.2 (at least 8 domains, or the 8,000 floor, which is not waived) and be removed whole.
- New code paths (--remove-sources, fold, integrity) could carry bugs. The fixture tests and the skeptic review mitigate this, and a failure leads to removal (drop) and never to admission.
- The G-proxy PASSes rest on incomplete exports. If a gp source shares a source name with OHS-AC, G-proxy-based selection could carry sealed bias. This is disclosed, not fixed.
- A64 (not adopted) may void more earlier passes. This ruling does not depend on A64, and it shares the freeze restore with it.
- The deny-list split scope stays unresolved for new data until C2.1 has a rule. Owner intent ("train splits") is deferred, not overruled.
- Earlier unrecorded DI-LANG runs and the variant runs already leaked information about the sealed keyword set to C2-side agents. The mitigation is the no-reuse rule. The leak cannot be undone.
- The money revert may trigger the A42-D 2.3 trims (item 10, wave 2, MD tail) exactly as they stood before A61.
- Timing: the code-edit window must finish before Mon 19 Oct ~14:00 UTC with no G13 run live. If it slips, the final-mix 8.5 is incomplete, and MD and SB5 are removed.

WHAT I DID TO CHECK
I read only code and records, plus the session log (for the owner's time). I computed sha256 values and AST source hashes. I opened no ohs or sealed path and ran no checker.
