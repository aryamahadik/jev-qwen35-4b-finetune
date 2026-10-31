# A61 adoption revision 3

## ruling_text
> **Ruling A61 (17 Oct 2026; orchestrator ruling, Opus. Made under the owner's decision of 17 Oct 03:21 UTC, quoted in the draft. Draft: `c2_build/zed_orch/di_train/A61_DRAFT.md`, sha256 `ec261d2b9906382a936390d6531d2b16a39bbdad4e3061c8e92cc3cb0a1aeb62`, written 03:41 UTC. Adoption text revision 3. Adopted at the moment this text is appended to PREREG_FINAL.md, which is after the DI block results. It is appended at the end of the file, after every entry already there, and keeps its draft number. When this revision was written, the last entries were A62, A60, the Post-freeze addendum, A63, A58 erratum E1, A64 and A65. No gate, bar, cap, probe threshold or isolation rule is loosened. Drops only. Nothing is relabelled. Where this ruling and an earlier entry both bind (A64 in particular), the stricter applies. Tag A61-HLE.)** The draft is adopted with the changes in (a) to (i). Each change is either stricter than the draft or records a result. **Outcome: no DI block enters C2. DI new rows are 0 and the DI part is 0. So the draft's row-cap, money and account changes do not take effect (e).**
>
> - **Times.** All times are UTC, taken from file times or the session log. This Mac's clock runs on EDT (UTC−4).
>   - The owner's decision is in the session log at 03:21 UTC.
>   - The draft labels the owner's decision "~04:40 UTC" and itself "~04:50 UTC". Both labels are wrong and are not used.
>   - Order of events:
>     - 03:21: the owner's decision;
>     - 03:41: the draft;
>     - 04:58: the first *recorded* DI 8.5 result (DI-LANG).
>   - DI-LANG's input form shows that earlier runs happened and were not recorded. Their times are unknown.
>   - From 08:08, `g13_c2.py` was being edited under A64 (g). A64 was adopted at ~08:15.
>
> - **(a) Draft (a) 7 as adopted (A42-D 8.5): binding inputs, valid PASS and bars. There is no exemption, no hashing change and no re-run of a barred source.**
>   - A42-D 8.5 (15 Oct) reads: "each source's identifiers (dataset name, publisher, host, upstream ID, licence page URL) go to the sealed-side checker … It returns **PASS or HIT per source only**, against the OHS-4 and OHS-AC source lists. A HIT removes the whole source." It has no platform exemption.
>   - A58 applied 8.5 as written: "**SB6 (TyDi QA yes/no) OUT** — 8.5 HIT". It applied no exemption.
>   - A16 (a) (3 Oct) reads: "Bare platform words (Wikipedia, Reddit, GitHub, arXiv, Zenodo, PubMed, ...) never match on their own."
>     - It sits in A16's deny-list bullet.
>     - A16.1 pins the tools that implement A16: denylist.py v1.2, deny_aliases.json v1.1, negcount.py v1.1 and replay_sample.py.
>     - denylist.py implements A16 (a) through its PLATFORM set.
>   - A16 (a) does not reach 8.5. 8.5 is a separate check, adopted 12 days later. Reading A16 (a) into 8.5 now would change a bar after HITs.
>   - **What the tool does.** `meta_src/source_name_check.py` has sha256 `72fe203a015aa4d5b292878dc871b21dcc4f0fdcab70e03fb142904b64fa1542`. It was last written 15 Oct 18:10, before every DI run.
>     - It hashes the five 8.5 identifiers.
>     - It also hashes extras: the dataset URL (its docstring says "extra, not required by 8.5"), the other hosts, and five strings built from each host. The extras make it stricter than 8.5.
>     - It reads the OHS-AC files "only if present" and exits 0. So until the (f) fix, no run proves which exports it read.
>   - **Binding inputs (a closed list).** A binding input is used unchanged. Only these exist:
>     - **md_\***: `meta_src/SOURCES_CANDIDATES.json` (`644cb9f5…f5f7`), written 15 Oct 18:09:58. The record shows two whole-file runs on this one file and no other form: OHS-4 only, then OHS-4 plus the AC preliminary file (`meta_src/NOTES.md:13-14`).
>     - **SB5_uci293**: every `SB5_uci293` and `SB5_uci293#…` entry of `zed_orch/sb_blocks/SOURCES_SB56_85.json` (`c4a9f5f5…1c4b`, 03:35:18) and of `SOURCES_SB5_85.json` (`bdb1e171…f4e`, 03:35:31), folded together. The orchestrator built both before SB5's one recorded verdict (`SB5/HANDOFF_85_DENYLIST.json`, 03:36). The later file only adds or lengthens identifiers, and the fold keeps every entry of both.
>     - No other source has a binding input. No other 8.5 input written before this ruling binds or admits anything. This covers the DI files, their variant files and re-shapes, and the G-proxy's files.
>   - **Valid PASS.** A PASS admits a source only if all of these hold:
>     - the source is not barred;
>     - it comes from the single final-mix run of (f), which is one whole-file run by the orchestrator;
>     - the run used the source's binding input;
>     - every export was verified by the (f) integrity check, and A64 (h) is met;
>     - the sha256 values of the tool and of `g13_c2.py`, logged before and after the run, equal the tested ones.
>   - No PASS on record meets this. Every earlier PASS (md_\*, SB5, gp_\*) came before the (f) fix. This rule binds every source, including the ones that passed.
>   - **HIT.** A recorded whole-file HIT removes the source, whatever its input form or export set. A drop is never a loosening. Nobody examines which identifier produced a HIT, and no ruling states which kind of identifier did.
>   - **Form-shopping bar.** A source is barred if, before its first whole-file record, any 8.5 run on it used a per-identifier, blank-field or other variant form, or used a form that the record does not keep. The evidence is input files and records only: their names, ids, fields and times. No run output is read. The bar is drop-only.
>   - **Scope of a bar.** A barred source is never re-run through 8.5. It is never admitted as new training data, in C2 or C2.1, under any later rule, id, alias or form.
>     - An entry that names the same dataset is the barred source. That means the same upstream id or dataset URL, a derivative listed with it, or a mirror, subset or renamed copy.
>     - A bar does not reach C1 replay rows, which keep the replay rules. It does not reach any G13 target.
>   - **Barred on a recorded whole-file HIT** (cited by id, file and time only):
>     - DI-KR_gsm8k: `DI-KR/work/qc_stage1.json` (05:23), on `SOURCES_DIKR_85.json` (`ddffa28a…`, 05:20);
>     - di_hover and di_isarcasmeval: `DI-LANG/provenance/name_check_result.txt` (04:58);
>     - SB6_tydiqa, with every `SB6_*` entry of `SOURCES_SB56_85.json` (its listed derivatives): A58, `SB6/HANDOFF_85_DENYLIST.json` (03:36);
>     - md_fdc and md_peps: `meta_src/NOTES.md:13-14` (15 Oct, written when no mapper existed: `NOTES.md:3`).
>   - **Barred by the form-shopping bar:**
>     - **DI-TS: every source in any DI-TS 8.5 input.**
>       - The nine are ts_logical_entailment, ts_temporal_nli, ts_perspectrum, ts_lonli, ts_spacenli, ts_wice, ts_fol_nli, ts_recast and ts_tracie (`work/di_ts_sources.json`, 05:05:54).
>       - Variant inputs exist for all nine, written before any whole-file record: `work/di_ts_sources_{final,final_nohost,nameonly,noHF,nohost,spdx}.json` and `work/v_{ds,lic,name,pub,up}.json` (05:06:10-05:07:27).
>       - Also barred: DI-TS_logical_entailment, DI-TS_perspectrum and DI-TS_temporal_nli (`DI-TS/SOURCES_DITS_85.json`, 05:53:29). They name three of the same upstream datasets.
>     - **DI-LANG**: di_hover, di_isarcasmeval and di_hotpotqa_wiki (`DI-LANG/provenance/name_check_sources.json`, 04:58:42). Its `_about` note records that identifier fields were left out of it, and the runs before it are not recorded.
>   - **Effect on the metadata block.** md_fdc and md_peps have 0 MD rows. They were HITs before any mapper was written (`NOTES.md:3, 13-14`). `data/c2_parts/MD/out/candidates_c2.jsonl` holds exactly the 11 c2_md_\* sources (10,491 rows, 11 domains, read at 08:20). So barring the two does not change A42-D 8.2 (11 sources, at least 8 domains, the 8,000 floor).
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
> - **(c) Blocks. All five DI blocks are OUT on one ground: no DI source has a valid 8.5 PASS (a), so draft (c) 2 ("PASS is required") is unmet.** This ground needs no run output. Every DI source with an 8.5 input is also barred (a).
>   - **DI-KR (GSM8K main train): OUT.** Two further records would each remove it on their own:
>     - the recorded whole-file HIT (a);
>     - the `check` verdict deny (05:14): taint, entries `3G#25.1` and `di:GSM8K`, scope split, cat di_test, exit 3.
>   - **DI-LANG: OUT.**
>     - di_hover and di_isarcasmeval have recorded HITs (a).
>     - All three sources are barred by the form-shopping bar, di_hotpotqa_wiki included. No PASS line of the 04:58 run is cited, and none admits anything. di_hotpotqa_wiki was only HoVer's evidence text and had no task.
>     - The deny-list was never run.
>   - **DI-TS: OUT.**
>     - All its sources are barred by the form-shopping bar (a).
>     - No line of R7 (`DI-TS/rulings/R1_TASK.md`, 05:16) is cited. R7's re-run instruction is overruled.
>     - `DI-TS/SOURCES_DITS_85.json` (05:53) is a re-shape made after R7. It is never run.
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
>     - DI-TS's variant inputs listed in (a);
>     - DI-LANG leaving fields out after earlier runs.
>   - Their outputs are breach output. They are never cited and never shape an input or a ruling. This ruling rests on three things only: (a)'s valid-PASS rule; the form-shopping bar, which reads no output; and whole-file HIT records, cited by id, file and time and used only to drop.
>   - Revision 2 of this text quoted a line of R7 that describes the variant runs and names a kind of identifier. It also inferred which md source might hit. Revision 3 strikes all of these remarks. Nothing rests on them.
>   - The `_about` note of the DI-LANG input also holds a remark drawn from the unrecorded runs. Only the fact that fields were left out is cited.
>   - The DI-TS deny-list `check` was run by its driver.
>   - A fact-gathering agent read 20 PASS/HIT lines of `meta_src/name_check_ohs4_result.txt`. Nothing relies on them.
>   - **From now on:**
>     - only the orchestrator runs `source_name_check.py`;
>     - it runs once per stage, on whole input files that this ruling fixes;
>     - there is no per-identifier, blank-field or variant run;
>     - nothing an earlier run showed shapes an input.
>
> - **(e) Money, rows and payers with the DI part at 0.**
>   - The owner gave the Modal reserve "for the extra training". No extra training exists, so draft (f) (rows) and draft (g) (money) do not take effect. Draft (g) is headed "Changes A42-D 2.1-2.4 … the accounts", so its six-account relay lapses with it. A42-D 2.1-2.4 stand:
>     - **C2 Modal total ≤ $40** ("No line may take the total above $40"). Training ≤ $34.
>     - **T_max = T_core = min($34, $32 − C2 Modal spend to date)**, fixed at the training GO. Only the credit fit below can lower it further.
>     - A37 (k) steps 100-300 stop-and-ask: above this T_max.
>     - After training, each line runs only if spend to date plus its projection is ≤ $40. SPEED-3 runs last, in full or not at all.
>   - **Rows:** core ≤ 125,000 (A40 d, A42-D 1.4). With the DI part at 0, the whole mix is ≤ 125,000. The 50,000-row floor (stop and ask) is unchanged.
>   - **Payers (A42-D 2.4, unchanged).** Free credit first, on the mahadikarya2 → mahadikarya3 relay only.
>     - jaypatil-duke, atmosphor, arya-mahadik-ai and mahadikarya44 pay for no C2 line unless a new owner ruling names them.
>     - The longer list is not neutral. Under the credit fit below, more accounts can avoid a T_core cut. The line revision 2 cited (PREREG_FINAL.md:1721, a phase-B payer rule) says "never aryamhd or jaypatil-duke". It grants nothing for C2.
>     - aryamhd is used only on an explicit owner GO that names the amount, for training only, inside the $40 and $34 caps (A42-D 2.4). Otherwise A39 (f) "no card" holds.
>   - **Credit fit.** This is stricter only: it can lower T_core, never raise it.
>     - C is the live free credit on mahadikarya2 plus mahadikarya3, each less c2_check's $1 per-account reserve. It is read and logged before the final mix and again at the training GO.
>     - T_core = min($34, $32 − spend, C − $8). The $8 is evaluation $4 + SPEED-3 $2 + the $2 reserve.
>     - Any cut uses the A42-D 2.3 trim order.
>     - At the 16 Oct planning balances ($19.09 + $13.84 − $2 = $30.93) and T_core ≈ $30.5, the cut would be about $7.6. The live figures decide.
>   - **GO #1 states** the two live balances, C, the T_core they allow, the trim steps the cut forces, and the dollar figure that would avoid the cut. Only a new owner ruling can add accounts or the card, and GO #1 is where the owner may give one. The orchestrator does not ask at any other point.
>
> - **(f) 8.5 tool fixes and the final-mix check.**
>   - **Pins.** These files are untracked in git, so their sha256 values are logged here before any edit:
>     - `source_name_check.py`: `72fe203a…1542`, backed up in `c2_build/_backup_a61_adopt/` (never in `_backup_a61/`);
>     - `meta_src/SOURCES_CANDIDATES.json`: `644cb9f5…f5f7`, written 15 Oct 18:09:58, one second before its result and never edited since;
>     - `zed_orch/sb_blocks/SOURCES_SB56_85.json`: `c4a9f5f5…1c4b`;
>     - `zed_orch/sb_blocks/SOURCES_SB5_85.json`: `bdb1e171…f4e`.
>     - The post-edit sha256 of the tool is logged before its first run.
>   - **Fold.** This implements "PASS or HIT per source only".
>     - Entries with id `<id>` or `<id>#…` fold into source `<id>`, and duplicate ids fold too.
>     - A source is a HIT if any of its entries hits. The tool prints one line per source.
>     - The fold can turn a PASS into a HIT, never the reverse.
>   - **Compare set. It is stricter only, by construction.**
>     - The tool builds its compare set only with the unchanged `load_hashes` and `HEX64`.
>     - It reads every file the old tool read, when present: the OHS-4 keyword file, the OHS-AC keyword file and the AC preliminary file. It adds the freeze export's keyword hashes (below).
>     - `identifier_texts` and `source_hashes` are unchanged.
>     - g13_c2's export classes (and A64's union reader) may be used to verify files only, never to load the compare set.
>     - So for every file, the new compare set contains the old one.
>   - **Export integrity under `--exports all`.** This implements "against the OHS-4 and OHS-AC source lists", the Post-freeze addendum ("the union of this export and the freeze export `27808b0c…` binds every later G13 / admission check") and A64 (h).
>     - The tool requires and verifies:
>       - OHS-4: MANIFEST sha256 `3771b47a…5470b`, which is g13_c2's pin, naming the A38 freeze `c0217e77…09c3`;
>       - the OHS-AC final export: MANIFEST `fadec66f…cd9b`;
>       - A64 (h)'s union record for the freeze export, MANIFEST `27808b0c…3f6e`.
>     - The freeze export's keyword hashes enter the compare set in one of two ways. They come from the union files the record names, each verified against its recorded sha256. Or, if the record shows 0 freeze keyword hashes outside the final export, they come from the final export itself.
>     - It checks each keyword file against its MANIFEST or record.
>     - If an export is missing or does not match, it prints only "<export> missing" or "<export> MISMATCH", gives no verdict, and exits 2. It catches exceptions and prints nothing else.
>     - It still reads the OHS-AC preliminary file when present.
>     - `--exports ohs4` never gives a binding verdict.
>   - **"Hashing unchanged" is tested, not assumed.** These tests run before the fixed tool is used:
>     - (1) `source_hashes()` returns identical sets under the old and new code for every entry of five recorded inputs: SOURCES_CANDIDATES.json, SOURCES_SB5_85.json, SOURCES_SB56_85.json, SOURCES_DIKR_85.json and DI-LANG `name_check_sources.json`. These are hashing fixtures only. The test loads no sealed file and prints only booleans and counts.
>     - (2) The source text of these functions is byte-identical across versions:
>       - g13_c2's `keyword_hashes`, `URL_RE`, `sha_hex` and `KW_STRIP`, in 904d914c, 213634d7, 32256eaa (if its copy is kept, step 3), the window-start `g13_c2.py` and the `g13_c2.py` used at the step-9 run;
>       - source_name_check's `load_hashes`, `HEX64`, `identifier_texts` and `source_hashes`, in 72fe203a and the fixed tool.
>       - At 08:20, g13_c2's four were identical in every `g13_c2.py` copy under c2_build back to 14 Oct, in a 32256eaa copy, and in the file being edited under A64.
>     - (3) Containment is tested on fixture export folders that the test creates. They hold keyword lines under "hash" and under other keys, several kinds, non-hash strings, and blank and bad lines. For each file, the fixed tool's compare set must contain the set that the old `load_hashes` gives.
>     - (4) The fold, duplicate ids, exit 2 on missing and exit 2 on MISMATCH are tested on fixture folders only.
>     - If any test fails, the tool is not used, and the final-mix 8.5 is incomplete.
>   - **Freeze export (A64 h).**
>     - The freeze export is not on disk as a separate copy.
>     - Its restore is A64 (h)'s union record. A fresh sealed agent builds it once, in A64's order:
>       - find a verified byte copy;
>       - if none is found, re-derive it with the freeze-time export code, keyword sources and FORMAT.md bytes;
>       - if that fails too, stop.
>     - It binds only if the MANIFEST sha256 equals `27808b0c…3f6e` exactly and every listed file verifies.
>     - The same record serves A57 step 6 and A64 (h).
>     - If it fails, A64 (h) applies: no OHS-AC hash-compare result admits anything, and the orchestrator stops and reports.
>   - **Scope of the final-mix run.** It runs only on the 8.5-gated sources that have at least 1 row in the final mix, after the final all-block G13 drops and every trim. These are the metadata-block sources (row source `c2_md_<x>` maps to `md_<x>`) and SB5 if it enters (`c2_sb5` maps to `SB5_uci293`).
>     - An MD or SB5 row whose source maps to no id in the binding inputs makes `--final` refuse.
>     - md_met, md_fdc, md_peps, the unchosen md sources and gp_\* are not run.
>   - **Input.**
>     - `mix_c2.py --final` writes the membership list.
>     - One input file copies, unchanged, every entry of those sources from their binding inputs:
>       - SOURCES_CANDIDATES.json for md_\*;
>       - both SB5 files for every `SB5_uci293` and `SB5_uci293#…` entry.
>     - No field is added, removed or reshaped for any source.
>     - The sha256 of each binding input and of the built file is logged before the run.
>     - It is one run, by the orchestrator, with `--exports all` and no `--role`.
>   - **Incomplete check.** The check is incomplete if any of these holds:
>     - the exit file is missing or does not hold 0;
>     - an output line is not "<id> PASS" or "<id> HIT";
>     - a membership id has no line or more than one line, or a line names an id outside the membership;
>     - a test in (f) failed;
>     - A64 (h) is not met;
>     - the sha256 of the tool or of `g13_c2.py` at the run differs from the tested one.
>     - Then no 8.5-gated source has a valid PASS, and every one of them is removed by the path below.
>   - **After a HIT or an incomplete check.** This path is fixed now, before the result. Every step only drops rows, and nothing refills.
>     1. `mix_c2.py --remove-sources <file>` loads the written final mix. It removes every row of the named sources, with their relation units and twins, through `mx.drop_rows`. It adds no pool row and never rewrites the membership list.
>     2. It runs `fit_block_in_mix(META_BLOCK, …)`: the A42-D 8.2 caps (source ≤ 15%, domain ≤ 20%), by whole tasks, seeded. This is the same call `apply_targets` makes after every metadata reduction. `merge_md.fit` (the builder stage, with its 40-task floor) is not used.
>     3. It runs `finish()`'s steps after the refill loop, unchanged, with no refill: `plan_shares`, then `apply_targets` if the agent cap applies; `replay_to_rule`; `budget_trim_a61`; `a60_enforce` (A60 c-e) with `replay_to_rule`; `arabic_cap_trim`; `tag_replay_unit`; then `gates()`.
>     4. Inside `gates()`, `block_rules(META_BLOCK, …)` asserts 8.2 and requires at least 8 domains.
>        - The 8,000-row floor is lowered only by P. P is the number of MD rows that spec 5.5's proportional step removed in the written final mix, taken from that mix's own budget record. P = 0 if the step cut no MD row or the record lacks P.
>        - `proportional_trim=True` is never passed on this path. So the waiver never covers a shortfall caused by an 8.5 removal.
>        - If 8.2 fails, the metadata block is removed whole by step 1, and steps 3-4 run again.
>     5. An SB5 HIT removes SB5 by step 1.
>     6. If the tail would run the proportional step again, or any other gate fails: stop at GO #1, no training.
>     7. There is no second 8.5 run, because a removal adds no source.
>   - **Enforcement before training.** The gate the chain runs is `train/preflight_c2.py` (`c2_chain.sh start`).
>     - Its new `a61_85` check (program fix 6) recomputes the 8.5-gated sources from the mix on disk.
>     - It FAILS unless the logged input, result and exit files match their logged sha256 values, the exit is 0, and every gated source in the mix has exactly one PASS line and no HIT.
>     - No flag clears it.
>   - **G-proxy: A42-D 12.2 is unmet (disclosed).**
>     - 12.2 says the G-proxy "follows the 8.3 source rules and the 8.5 sealed-side source-name check". Under (a), no gp_\* source has a valid 8.5 PASS. Their PASSes rest on OHS-4 plus the AC preliminary file, with no verified export. So 12.2's 8.5 requirement is unmet for the whole G-proxy.
>     - The G-proxy is a selection signal, not only a file that is never trained. A42-D 12.5 uses it in four places: the item 4.3 pilot gate, the item 9.3 score S, the 9.4 eligibility rule and the item 10.2 adoption rule.
>     - 8.5 already fixes the remedy for one source: "A HIT removes the whole source", and 12.2 applies that.
>     - No rule fixes how removing a source from a frozen file ("never edited afterwards") carries into later uses. These are the pilot verdicts already logged, and S, eligibility and adoption, where a smaller G-proxy can move a result either way. That is not a pure drop. So this ruling does not decide it and runs no gp_\* check. gp_\* has no binding input (a).
>     - Consequences, fixed now:
>       1. GO #1 states, in these words: "A42-D 12.2 is unmet: no G-proxy source has a valid 8.5 PASS (A61 a, f)."
>       2. Every item 4.3 pilot verdict, the item 9 choice and the item 10 decision is reported with the label "G-proxy: A42-D 12.2 8.5 requirement unmet".
>       3. No claim cites the G-proxy while 12.2 is unmet. This includes the 12.5 general-accuracy claim.
>       4. A re-check needs its own ruling. That ruling applies 8.5's whole-source remedy, fixes its effect on each use, and is adopted before the first item 9 candidate score is computed. Without one, items 9 and 10 run as registered, labelled as in 2.
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
>   - **Predecessor shas.** Two shas may join REFRESH_COMPATIBLE_TOOL_SHAS:
>     - `213634d77c868e28a6130cc13fb2910c032f88d1d37811c829bd5edf3db8853c` (`_backup_a61/g13_c2.py`, checked at window start and never overwritten);
>     - `32256eaa2328c5029b02b2835ff00cb97bb34cd3abf748db0d6631e680b75776`, but only if a byte copy is first kept in `_backup_a61_adopt/` and verified (step 3).
>   - They join only after tests show all of these:
>     - (1) For a non-DI fixture block, each predecessor's candidates log equals the new code's log field for field. The only exceptions are g13_c2's fixed bookkeeping list: `wall_s`, `unix`, `engine.embed_stats`, the checkers' `wall_s` and the top-level `refreshed` list. `refresh-dev --check` accepts the log, and the refresh equals a full run.
>     - (2) The diff between each predecessor and the new file holds only the A61 hunks, the sob_wiring hunks and the new REFRESH_COMPATIBLE_TOOL_SHAS lines.
>       - A64 (g)'s hunks are not on this list. `g13_c2.py` has carried them since 08:08.
>       - While they are present, (2) fails for both predecessors. Then neither joins, fix 7 makes no edit, and their blocks get full candidates runs.
>       - Whether a log is refresh-compatible across A64's own edit is a question for A64.
>     - (3) No non-DI target spec reaches `decision_index_03/`. The added QUARANTINE_OK paths change no `allowed()` answer and no file set of a non-DI target.
>     - (4) `needs_di` is False for every non-final run.
>   - Test (3) runs inside the process and outputs only booleans and counts. It never prints or logs a path (`_NO_ECHO`). Only the orchestrator runs it.
>   - The edit is made only when no G13 run is live and A64's edit of `g13_c2.py` is finished. Its post-edit sha256 must be logged in `zed_orch/a64/A64_TOOLS.md` and equal the file on disk. If any test fails, the blocks get full candidates runs.
>
> - **(h) Reports and C2.1.**
>   - **In C2,** the DI is report-only. No DI train split is trained, so the draft's in-family and task-type labels do not apply. DI tables state "no DI train split trained in C2".
>   - **C2.1 needs all of these before any check runs on a DI train split:**
>     1. a PREREG rule for a split-aware `check`, with a declared split field and tests, adopted before that check runs;
>     2. the (a) bars in their full scope: no barred source (recorded HIT or form-shopping bar) is re-run or admitted under any id, alias or form, and an entry that names the same dataset is the barred source;
>     3. 8.5 changes stricter only. A change to 8.5's hashing, identifier list, exports or compare set may only add hashes, identifiers or exports. It binds every source alike, including those that passed (md_\*, SB5, gp_\*). There is no platform-host exemption.
>   - The draft's (i) list (harder program-gold families, DI-RC, DI-TOOLS, head and loss ideas) stays recorded only.
>
> - **(i) Unchanged, and what this ruling changes.**
>   - **Unchanged:**
>     - every adopted gate, cap and bar in PREREG_FINAL.md before this entry, including A62, A60, the Post-freeze addendum, A63, A58 erratum E1, A64 and A65;
>     - A40 (d) and A42-D 1.4 and 2.1-2.4, including the two-account relay;
>     - the 40/60 split and the 1.5× replay;
>     - both owner GO points;
>     - the 96% usage stop and the 98% ceiling;
>     - the never-open rules;
>     - the A42-D block text and its sha256.
>   - **Changed** (code and records only; no rule changes):
>     - the G13 target registry, which gains `di03_public` and `di_src_splits`;
>     - `source_name_check.py` (fixes 1-3);
>     - `mix_c2.py`: the membership list, `--remove-sources` with the P floor, the 0-DI refusal (fix 4), and the constants and relay back to A42-D with the credit fit (fix 5);
>     - `train/c2_check.py`, `train/preflight_c2.py`, `train/make_modal_od_c2.py` with the regenerated `train/modal_od_c2.py`, `snap_monitor_c2.py` and `train/c2_chain.sh`. The A61-draft constants and the six-account list go back to A42-D 1.4, 2.1, 2.3 and 2.4 (fix 5). The preflight gets the 8.5 check (fix 6);
>     - `g13_c2.py`, only if fix 7's tests pass;
>     - the five DI QC records.
>   - **The GO #1 request lists:**
>     - per DI block: 0 rows, drops by step, the A46 counts, the recorded 8.5 and deny-list verdicts as counts, the bars, and the breaches in (d);
>     - the HLE gap;
>     - the final-mix 8.5 counts, any removal, P and the MD 8.2 outcome;
>     - the G-proxy disclosure in the words of (f);
>     - the A64 (h) status;
>     - the money basis in (e).

## per_source
DI-KR_gsm8k (GSM8K main train): OUT and barred for good (A61 a). There is no valid 8.5 PASS. The recorded whole-file HIT is DI-KR/work/qc_stage1.json (05:23), on SOURCES_DIKR_85.json (sha ddffa28a…, 05:20). The deny-list check verdict is deny: taint, entries 3G#25.1 and di:GSM8K, scope split, exit 3. It is never re-run or admitted under any id or form.
di_hover (HoVer train): OUT and barred for good. No valid PASS. Recorded HIT at 04:58 (DI-LANG/provenance/name_check_result.txt). The form-shopping bar also applies: the DI-LANG input's own note records fields left out, and the earlier runs are not recorded.
di_isarcasmeval (English train): OUT and barred for good, on the same two grounds as di_hover.
di_hotpotqa_wiki (HoVer evidence text only): OUT and barred for good by the form-shopping bar (DI-LANG/provenance/name_check_sources.json, 04:58:42). No result line for it is cited. It had no task.
DI-TS (ts_logical_entailment, ts_temporal_nli, ts_perspectrum, ts_lonli, ts_spacenli, ts_wice, ts_fol_nli, ts_recast, ts_tracie; and DI-TS_logical_entailment, DI-TS_perspectrum, DI-TS_temporal_nli, which name three of the same upstream datasets): OUT and barred for good by the form-shopping bar. Variant inputs exist for all nine: work/di_ts_sources_{final,final_nohost,nameonly,noHF,nohost,spdx}.json and work/v_{ds,lic,name,pub,up}.json, 05:06:10-05:07:27, before any whole-file record. No line of R7 is cited. SOURCES_DITS_85.json, the post-R7 re-shape, is never run. The deny-list pass in dits_prov_verdicts.json was run by the driver and no longer matters.
DI-RC, DI-TOOLS: 0 rows. They move to C2.1. QC pass is set to false.
md_cma, md_cordis_h2020, md_fsa, md_gbif, md_gene_ontology, md_geonames, md_musicbrainz, md_openalex, md_ror, md_usgs, md_worldbank: provisional. Their earlier PASSes rest on OHS-4 plus the AC preliminary file only, so none is a valid PASS yet. Each enters only if it has at least 1 final-mix row and gets a PASS in the single final-mix run (--exports all, verified exports, A64 h met). That run uses the source's unchanged SOURCES_CANDIDATES.json entries (sha 644cb9f5…). No source's input is changed. A HIT or an incomplete check removes the source through the fixed drop-only path.
md_met: not in the mix and not run.
md_fdc, md_peps: barred for good. Their recorded HITs are in meta_src/NOTES.md:13-14 (15 Oct, before any mapper existed: NOTES.md:3). They have 0 MD rows. MD's candidates_c2.jsonl holds exactly the 11 c2_md_* sources (10,491 rows, 11 domains), so A42-D 8.2 is unaffected.
SB5_uci293: provisional. It enters only on a PASS in the same final-mix run. That run uses every SB5 entry of both pre-verdict files, folded together: SOURCES_SB56_85.json (c4a9f5f5…, 03:35:18) and SOURCES_SB5_85.json (bdb1e171…, 03:35:31). The orchestrator built both before SB5's one recorded verdict (03:36), and the later file only adds or lengthens identifiers. A HIT or an incomplete check removes SB5.
SB6_tydiqa, with its listed derivative entries (SB6_deriv_MIRACL, SB6_deriv_Mr_TyDi, SB6_deriv_TyDiQA-GoldP, SB6_deriv_XOR-TyDi_QA): OUT (A58) and barred for good, on the recorded HIT (SB6/HANDOFF_85_DENYLIST.json, 03:36). This bars training admission only. The bench's G13 targets are unaffected.
SB4: OUT per A58. No 8.5 run was ever requested, and none is run now.
gp_* (G-proxy): no valid 8.5 PASS. A42-D 12.2 is unmet. The G-proxy is a selection signal (4.3, 9.3, 9.4, 10.2). This is disclosed at GO #1 with the consequences in (f). There is no binding input and no run. A re-check needs its own ruling, which applies 8.5's whole-source remedy and is adopted before the first item 9 score.

## program_fixes
Each fix below says which rule it implements and quotes that rule. Every rule was registered before the result the fix affects. Every pre-edit file is backed up in c2_build/_backup_a61_adopt/ (new folder). c2_build/_backup_a61/ is never written.

1. c2_build/meta_src/source_name_check.py: FOLD.
- Pre-edit sha256 is 72fe203a015aa4d5b292878dc871b21dcc4f0fdcab70e03fb142904b64fa1542 (untracked).
- Behaviour: entries with id <id> or <id>#…, and duplicate ids, fold into source <id>. The source is HIT if any entry hits. The tool prints one line per source.
- Implements A42-D 8.5 (15 Oct): "It returns **PASS or HIT per source only**".
- Effect: stricter only. It can turn a PASS into a HIT, never the reverse.

2. c2_build/meta_src/source_name_check.py: COMPARE SET AND EXPORT INTEGRITY under --exports all.
- Compare set: it is built only by the unchanged load_hashes and HEX64. The input is every file the old tool read when present (../sealed_hashes/keyword_hashes.jsonl, ../sealed_hashes_ac/keyword_hashes.jsonl, ../sealed_hashes_ac/source_keywords_prelim.jsonl), plus the freeze export's keyword hashes, read in one of two ways:
  - from the union files named by A64 (h)'s union record, each verified against the record;
  - from the final export, if the record shows 0 freeze keyword hashes outside it.
- identifier_texts and source_hashes stay byte-identical.
- g13_c2's Exports, AcHashFiles and ExportsAC classes, and A64's union reader, may be used only to verify files. They never build the compare set.
- Verification:
  - OHS-4: the MANIFEST sha must equal g13_c2's SEALED_HASHES_MANIFEST_SHA256 3771b47ad06157a97973eaf3539c9bde0b87e97b5b4458148a51f2506025470b, naming the A38 freeze c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3.
  - The OHS-AC final export: MANIFEST fadec66fdb3824ca3e81096c65b15d5e8cac7998a05fc964d0ce1b4fdb36cd9b.
  - A64 (h)'s union record for the freeze export: MANIFEST 27808b0ccbaf69aae058745ef0e80db6f5b692648198f26161bf749c3f1c3f6e, every listed file verified.
  - Each keyword file's sha256 is checked against its MANIFEST or record.
- On a missing or mismatched export it prints only "<export> missing" or "<export> MISMATCH", gives no verdicts, and exits 2. Exceptions are caught; no other text is printed.
- The AC preliminary file is still read when present.
- Implements A42-D 8.5 "against the OHS-4 and OHS-AC source lists". It also implements the Post-freeze addendum (~05:35 UTC): "the union of this export and the freeze export `27808b0c…` binds every later G13 / admission check". And it implements A64 (h): "No OHS-AC hash-compare result admits anything until a sealed-side union record for the freeze export 27808b0c… exists". The final-mix run is a later admission check.

3. Tests for 1 and 2: c2_build/tests/test_source_name_check_a61.py.
- (a) For every entry of SOURCES_CANDIDATES.json, SOURCES_SB5_85.json, SOURCES_SB56_85.json, SOURCES_DIKR_85.json and DI-LANG name_check_sources.json, source_hashes() is identical under the old module (_backup_a61_adopt/meta_src/source_name_check.py) and the new one. These are hashing fixtures. The test loads no sealed file and prints booleans and counts only.
- (b) Byte-identical source text, checked by AST segment:
  - g13_c2's keyword_hashes, URL_RE, sha_hex and KW_STRIP in _backup_refresh/g13_c2.py (904d914c), _backup_a61/g13_c2.py (213634d7), the 32256eaa copy if kept, the window-start g13_c2.py, and the g13_c2.py whose sha is logged for the step-9 run;
  - source_name_check's load_hashes, HEX64, identifier_texts and source_hashes, old (72fe203a) vs new.
- (c) Containment, on fixture export folders that the test creates under tmp. The fixtures hold keyword lines under "hash" and other keys, several kinds, non-hash strings, and blank and invalid lines. For each file, the new tool's compare set must contain the old load_hashes set over the same file.
- (d) The fold, duplicate ids, exit 2 on missing and exit 2 on MISMATCH, tested on fixture folders under tmp. The sealed folders are never touched.
- Rule implemented: A61 (f), "Hashing unchanged" is tested, not assumed, and the compare set is stricter only.

4. c2_build/mix_c2.py: MEMBERSHIP, REMOVAL AND THE 0-DI REFUSAL.
- The pre-edit sha is c448994b50f3a3c4b8d525074c71f1afc3dde51715a560747c61ac3278b0ac09. Back it up to _backup_a61_adopt/mix_c2.py. _backup_a61/mix_c2.py (c38d7a8f…, the pre-draft mixer) stays as it is.
- (a) --final:
  - writes the membership list c2_build/logs/a61_85_membership.json. It lists the 8.5-gated sources with at least 1 final-mix row, mapping c2_md_<x> to md_<x> and c2_sb5 to SB5_uci293;
  - refuses if an MD or SB5 row's source has no mapping;
  - refuses if any row of a DI block is in the mix or the DI part is above 0;
  - records P (the MD rows removed by spec 5.5's proportional step) in the budget record.
- (b) New --remove-sources FILE, drop-only:
  - It loads the written final mix and removes every row of the named sources with their relation units and twins (mx.drop_rows). It adds no pool row and never rewrites the membership list.
  - It then runs fit_block_in_mix(META_BLOCK); then the tail of finish() after the refill loop, without refills (plan_shares/apply_targets, replay_to_rule, budget_trim_a61, a60_enforce + replay_to_rule, arabic_cap_trim, tag_replay_unit); then gates().
  - block_rules gets a new floor argument: the 8,000 floor less P. proportional_trim=True is never passed on this path.
  - If 8.2 fails, MD is removed whole the same way, and the tail and gates run again.
  - It refuses if the tail would run the proportional step again. Any other failure refuses.
- Implements A42-D 8.5: "again on the final mix" and "A HIT removes the whole source". Also A42-D 8.2 (the caps, at least 8 domains, and the 8,000 floor, which is waived only by spec 5.5's proportional step) and spec 5.3 (a block that fails is left out, nothing refills). All are fixed before the final-mix result.
- Tests (fixture):
  - no id is ever added;
  - an MD source removal refits the caps;
  - an 8.2 failure removes MD whole;
  - with P > 0 and a removal shortfall larger than P, MD is removed whole;
  - with P = 0, a waiver never applies;
  - an SB5 removal works;
  - replay follows floor(1.5 × new);
  - the membership list is not rewritten;
  - a DI row makes --final refuse.

5. CONSTANTS, CREDIT FIT AND RELAY BACK TO A42-D. Every item is required; none is an alternative to another.
- c2_build/mix_c2.py:
  - C2_MODAL_CAP_USD 45 → 40;
  - T_MAX_CAP/T_MAX_BASE 39/37 → 34/32, so T_max = T_core;
  - ROWS_MAX 150000 → 125000;
  - RELAY_ACCOUNTS → ("mahadikarya2", "mahadikarya3");
  - new --credit-usd C, required with --final: T_core = min(34, 32 − spend, C − 8). It can only lower T_core.
  - The 0-DI refusal of fix 4 (a) is in addition to these changes, never instead of them.
- c2_build/train/c2_check.py (pre 14648f6c3ca663e2c9d30dc9a41526d101ab45845fde4beb341c04a278eed19a):
  - CAP_TOTAL, TMAX_CAP and TMAX_BASE 45/39/37 → 40/34/32;
  - RELAY_ACCOUNTS/PROFILES → ("mahadikarya2", "mahadikarya3");
  - tmax --fix records min(34, 32 − spend, C_live − 8), with C_live read through BILL for the two accounts, each less CREDIT_RESERVE;
  - the formula string becomes "min(34, 32 - spend to date, live credit - 8)".
- c2_build/train/preflight_c2.py (pre 67b4602a30015ed88af4463c1ef83fbafa81be060380b22ab53ae9e1d06f37e2):
  - MAX_ROWS 150_000 → 125_000;
  - the accounts check covers the two relay accounts;
  - "free credit covers T_max and the later lines" becomes a FAIL when false, not a report;
  - FAIL if logs/c2_tmax.json exists with another cap_total or formula.
- c2_build/train/make_modal_od_c2.py (pre 9739914f2b3971421a73c8d7ee15f41e0b8ca7e07599546bdabaaf12bd60506f): ALLOWED_PROFILES → the two. Regenerate train/modal_od_c2.py (pre ab09a1d795101c58ec668238fa4556b46c74c8d850eb61032e1b4cbab774ad11) so that C2_ALLOWED_PROFILES is the two. `make_modal_od_c2.py --check` must pass.
- c2_build/snap_monitor_c2.py (pre 4bd0612e44ad692176bd242598d8674f7216fdfcc1c2ad625a76b9b8fb672d3e): PROFILES → the two.
- c2_build/train/c2_chain.sh (pre 4f01b32e36f75454687b38ea26889077393067a162f26bd45eb8355867fd7c77): RELAY → "mahadikarya2 mahadikarya3".
- Some docstrings and comments state the draft's $45 / $39 / $37 / 150,000 or the six-account list as in force. Each is corrected to A42-D or marked "A61 draft, not adopted":
  - c2_check.py lines 1-12 and 35-39;
  - preflight_c2.py lines 10, 16-21 and 54;
  - c2_chain.sh lines 9-11, 19 and 32;
  - mix_c2.py lines 61, 89-104 and 186-194;
  - make_modal_od_c2.py lines 11-12 and 29;
  - snap_monitor_c2.py line 62.
- Implements:
  - A42-D 2.1: "No line may take the total above $40. Only a new owner ruling can change the cap.";
  - A42-D 2.3: "T_max = min($34, $32 − C2 Modal spend to date)";
  - A42-D 2.4: "Free credit first, with the mahadikarya2 → mahadikarya3 relay";
  - A40 (d) / A42-D 1.4 (125,000).
  - The owner's reserve grant covered only "the extra training", and the DI part is 0.
- Update the tests that assert the draft constants or the six accounts: tests/test_mix_c2_a61.py, test_mix_c2.py, test_mix_c2_a42d.py, test_mix_c2_t46.py, test_snap_monitor_c2.py and train/tests/test_train_tools.py.
- New tests:
  - the credit fit only lowers T_core;
  - the c2_tmax.json guard works;
  - the relay is exactly the two accounts;
  - aryamhd is refused.
- Every suite must pass.

6. c2_build/train/preflight_c2.py: THE 8.5 GATE BEFORE TRAINING.
- A new check, a61_85, runs on every preflight (c2_chain.sh start). It recomputes the 8.5-gated sources from the mix on disk (c2_train.jsonl, already sha-checked against the manifest): md_<x> for every row with source c2_md_<x>, and SB5_uci293 if any row has source c2_sb5.
- It FAILS unless all of these hold:
  - zed_orch/di_train/A61_FINAL_85_INPUT.json, A61_FINAL_85_RESULT.txt and A61_FINAL_85_EXIT.txt exist and match the sha256 values logged in A61_EDIT_RECORD.json;
  - the exit file holds 0;
  - every result line is "<id> PASS" or "<id> HIT", and the result names each folded id of the input exactly once and no other id;
  - every gated source in the mix is in the input and has a PASS line;
  - no gated source in the mix has a HIT line.
- If the mix has no gated row, the check passes and says so.
- A missing or unreadable file is a FAIL. Neither --ack-pending nor --offline clears it.
- Implements A42-D 8.5 "again on the final mix" and A61 (f) "Valid PASS".
- Tests (fixture, under tmp):
  - it passes when every line is PASS;
  - it fails on each of these: a missing file, a sha mismatch, exit 2, exit 1, a bad line, a missing id, a duplicate id, an extra id, a HIT id left in the mix, a gated source not in the input;
  - --ack-pending does not clear it.

7. c2_build/g13_c2.py: PREDECESSOR SHAS.
- Add 213634d77c868e28a6130cc13fb2910c032f88d1d37811c829bd5edf3db8853c and, if its copy is kept, 32256eaa2328c5029b02b2835ff00cb97bb34cd3abf748db0d6631e680b75776 to REFRESH_COMPATIBLE_TOOL_SHAS.
- Conditions: only after the A61 (g) tests (1)-(4) pass, in the single code-edit window, with no G13 run live, and after A64's edit of this file is finished and its sha is logged in zed_orch/a64/A64_TOOLS.md.
- While A64 (g)'s hunks are in the file, test (2) fails, and this fix makes no edit.
- Implements g13_c2's own refresh contract, which predates the result (docstring and the comment above REFRESH_COMPATIBLE_TOOL_SHAS): a predecessor is valid when its "full-run code path is the same" and "the merged log is what a full run on the current files writes, field for field, apart from bookkeeping: wall_s, unix, engine.embed_stats, the checkers' wall_s and the new top-level "refreshed" list".

8. Records, not tools: in data/c2_parts/{DI-KR,DI-LANG,DI-TS,DI-RC,DI-TOOLS}/qc/QC_REPORT.json, add an a61 object holding a verbatim copy of the prior top-level fields, then set pass to false. These are drops, under draft (c) 2 "PASS is required" and mix_c2 admission "QC pass is not true".

9. Deliberately NOT changed:
- c_src/common/denylist.py: a split-aware check is C2.1, under its own PREREG rule.
- g13_c2 keyword_hashes, URL_RE, sha_hex and KW_STRIP: no hashing change and no platform stoplist.
- source_name_check load_hashes, HEX64, identifier_texts and source_hashes: unchanged.
- Every 8.5 input file: none is edited.
- c2_build/_backup_a61/: never written.

## orchestrator_commands
All paths are under /Users/aryamahadik/Documents/jev/opendecide-data/lean. Run from lean unless a step says otherwise. No step opens an ohs or sealed path on the C2 side. No checker runs except in step 9.

1. ADOPT
- Write the ruling_text to c2_build/zed_orch/di_train/A61_FINAL.md.
- Run `date -u +%H:%M`, then append the file to the end of PREREG_FINAL.md as written.
- Check that the A42-D block sha256 still equals cbdc29d950bba3bad3e1fa2559346eae9405522c30bb7a4ffe0aaf7873665d2f.
- Log in HANDOFF.md: the adoption time (UTC), the sha256 of PREREG_FINAL.md after the append, and the A61_FINAL.md sha256.

2. DI QC RECORDS
For B in DI-KR DI-LANG DI-TS DI-RC DI-TOOLS:
- run a 10-line python -I script that loads data/c2_parts/$B/qc/QC_REPORT.json;
- it sets j['a61'] = {'ruling':'A61','outcome':'OUT (no valid 8.5 PASS; A61 c)','prior_top_level': {k: j[k] for k in j if k!='a61'}} and then j['pass'] = False;
- it writes the file back;
- log the sha256 before and after in c2_build/zed_orch/di_train/A61_EDIT_RECORD.json.
From now on, add `--leave-out DI-KR DI-LANG DI-TS DI-RC DI-TOOLS` to every mix_c2.py run.

3. SINGLE CODE-EDIT WINDOW
- Start only when all of these hold:
  - `pgrep -fl g13_c2.py` prints nothing;
  - A64's edit of g13_c2.py is finished: zed_orch/a64/A64_TOOLS.md exists, and its logged post-edit sha256 of g13_c2.py equals `shasum -a 256 c2_build/g13_c2.py`;
  - no other lane is editing any file below.
- Check the old backups first, before any copy:
  - `shasum -a 256 c2_build/_backup_a61/g13_c2.py c2_build/_backup_refresh/g13_c2.py c2_build/_backup_a61/mix_c2.py` must give 213634d77c868e28a6130cc13fb2910c032f88d1d37811c829bd5edf3db8853c, 904d914c477db958a1793897c0e7f07f13f76891c1ba3a19cb49321860b96569 and c38d7a8f789cbca0348ddfc727910e9855b3752d5acc2f699ec4486f20d0b5ae.
  - If either g13_c2.py copy differs: no predecessor joins, test 3(b) fails, and the final-mix 8.5 is incomplete.
  - If the mixer copy differs, record it. Fix 5 uses only the values written in this ruling.
- Make the new backup folder:
  - `mkdir c2_build/_backup_a61_adopt`. If it already exists, stop.
  - Copy each file with `cp -n`, keeping its relative path: meta_src/source_name_check.py, mix_c2.py, g13_c2.py, snap_monitor_c2.py, train/c2_check.py, train/preflight_c2.py, train/c2_chain.sh, train/make_modal_od_c2.py, train/modal_od_c2.py, and every test file that fixes 3-7 edit.
  - Verify each copy with `shasum -a 256` against its source and log both in A61_EDIT_RECORD.json.
  - Never write into _backup_a61/.
- The pre-edit shas at drafting (08:20 UTC) are listed in program_fixes 1, 4 and 5. g13_c2.py was being edited under A64 then (d149bc1d… at 08:10, e8246a79… at 08:19). Its window-start sha is the one logged.
- About 32256eaa: no copy exists under c2_build. Byte copies exist only in the session scratch folder (/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/adbc4a3b-e366-431b-b0e2-96c55904b928/scratchpad/orig/g13_c2.py, among others). To keep it as a candidate, copy one to c2_build/_backup_a61_adopt/g13_c2.32256eaa.py and verify sha 32256eaa2328c5029b02b2835ff00cb97bb34cd3abf748db0d6631e680b75776. Otherwise it does not join.
- Brief one Sonnet code agent with program_fixes 1-8. The brief must state:
  - never open or list any path containing ohs or sealed;
  - never run source_name_check.py on real exports;
  - tests use fixture folders under tmp only;
  - print booleans and counts only;
  - never write into _backup_a61/ or any FREEZE/ path.
- Run in c2_build:
  - `../../.venv/bin/python -B -m pytest tests/test_source_name_check_a61.py`;
  - the mixer suite;
  - the train suite;
  - tests/test_snap_monitor_c2.py;
  - `../../.venv/bin/python -B train/make_modal_od_c2.py --check`.
- Run the g13 REFRESH tests (1)-(4) in-process (boolean output only). Add the shas only if all of them pass.
- Apply sob_wiring.patch and sob_wiring_tests.patch in this window only if they are planned and not already in the files. The window-start g13_c2.py already imports sob_g13.
- Then get one Opus skeptic review of the diff.
- Log the post-edit sha256 values in A61_EDIT_RECORD.json.

4. FREEZE EXPORT (A64 h UNION RECORD)
- This is one build, shared with A57 step 6 and A64 (h).
- Brief a fresh sealed agent under AC_SEALED_BRIEF and A64 (h). It works in this order:
  - find a byte copy of the freeze export (MANIFEST 27808b0ccbaf69aae058745ef0e80db6f5b692648198f26161bf749c3f1c3f6e) in every place A64 (h) lists;
  - if none is found, re-derive it with the freeze-time export code, keyword sources and FORMAT.md bytes;
  - if that fails too, stop.
- The brief also restates:
  - A57 sealed-side access audit = 0: the agent never opens the pool quarantine (c2_build/a57_pool_quarantine/) or any T4x haiku folder, and the export path skips build_manifest(), as the addendum's deviation (i) records;
  - it writes only into its own new folder, never into FREEZE/ or any existing export folder. The addendum's deviation (ii) records that FREEZE/GENERATOR_INPUTS.json was overwritten once by an export run;
  - the export is hash-only, and every file is verified against its MANIFEST.
- The orchestrator receives only:
  - the MANIFEST sha256, which must equal 27808b0c…3f6e;
  - file verification PASS/FAIL;
  - |freeze \ final| per kind, as counts;
  - the access-audit count.
- Record them in A61_EDIT_RECORD.json. If the record fails, A64 (h) applies: stop and report at GO #1. The final-mix 8.5 is then incomplete.

5. di03_PUBLIC
- On a quiet Mac (load below about 4, no G13 run live), run `bench/external_quarantine/decision_index_03/venv/bin/python -B c2_build/g13_di/di_rebuild.py run --skip-download`, then `di_register.py finalize` and `di_register.py export`.
- Check that g13_di/di_pins.json has di03_public set to true, with only the A61-HLE gap. Otherwise record it as incomplete for GO #1.

6. FINAL ALL-BLOCK G13 (Mon 19 Oct ~14:00 UTC), as planned.

7. MIX
- Read the live free credit on mahadikarya2 and mahadikarya3 (`../.venv/bin/python -B c2_build/train/c2_check.py status --profile <account>`). Log C (the sum, less $1 per account).
- Run `../.venv/bin/python -B c2_build/mix_c2.py --final ... --spend-to-date <X> --credit-usd <C> --leave-out DI-KR DI-LANG DI-TS DI-RC DI-TOOLS`.
- This writes c2_build/logs/a61_85_membership.json and records P. Log its sha256.

8. BUILD THE 8.5 INPUT
- Use a python -I script that takes the membership ids and builds c2_build/zed_orch/di_train/A61_FINAL_85_INPUT.json = {"sources": [...]} by copying entries unchanged:
  - for each md id, every entry of meta_src/SOURCES_CANDIDATES.json (sha 644cb9f5b6ca34dc5e5ac21b021bc559c2bb465d66bf7baf720b254cdd86f5f7) whose id equals that id or starts with id+'#';
  - for SB5 (only if it is in the membership), every entry with id SB5_uci293 or SB5_uci293#… from zed_orch/sb_blocks/SOURCES_SB56_85.json (sha c4a9f5f555838a548a844f165b2571c9f39a79dce89babcc5dc1e358f0fc1c4b) and from zed_orch/sb_blocks/SOURCES_SB5_85.json (sha bdb1e171ec59601ab3cc0cd215e2e215bb788ee0ef10a506f3831b8aa2a09f4e).
- No other entry is copied, and no field is edited.
- Before the run, verify the three binding shas. Log them together with the sha256 of the built file.

9. ONE 8.5 RUN (orchestrator only)
- From c2_build, log `shasum -a 256 g13_c2.py meta_src/source_name_check.py zed_orch/di_train/A61_FINAL_85_INPUT.json` in A61_EDIT_RECORD.json. The first two must equal the tested shas.
- Run `../../.venv/bin/python -B meta_src/source_name_check.py --file zed_orch/di_train/A61_FINAL_85_INPUT.json --exports all > zed_orch/di_train/A61_FINAL_85_RESULT.txt; echo $? > zed_orch/di_train/A61_FINAL_85_EXIT.txt`. Do not pass --role.
- Log the same three shas again, plus those of the RESULT and EXIT files. The before and after values must be equal.
- Record the PASS and HIT counts and the HIT ids. Do not re-run it.

10. REMOVAL (if needed)
- The check is incomplete if any (f) condition holds: the exit file is missing or not 0; a bad line; a membership id with no line or more than one; an extra id; a failed step-3 test; a failed step 4; or a sha change in step 9. If so, write every membership id to c2_build/logs/a61_85_remove.json.
- Otherwise write every HIT id there.
- If the file is non-empty, run `../.venv/bin/python -B c2_build/mix_c2.py --final --remove-sources c2_build/logs/a61_85_remove.json --spend-to-date <X> --credit-usd <C> --leave-out DI-KR DI-LANG DI-TS DI-RC DI-TOOLS`.
- If anything other than the MD block's 8.2 check fails, or the proportional step would run again: stop, no training, report at GO #1.

11. PREFLIGHT
- c2_chain.sh start runs preflight_c2.py. Its a61_85 check must PASS (program fix 6). --ack-pending does not clear it.
- Its money and accounts checks use the two relay accounts and the live credit fit.

12. GO #1 REQUEST
Include:
- DI: 0 rows, with per-block drops by step, A46 counts, 8.5 and deny-list verdict counts, the bars, and the (d) breaches;
- the HLE gap and the di03_public status;
- the A64 (h) union-record status;
- the final-mix 8.5 counts and any removal, plus P and the MD 8.2 outcome;
- the G-proxy disclosure, in the words of (f);
- the money basis: the $40 cap; T_max = T_core = min($34, $32 − spend, C − $8); the live balance of mahadikarya2 and mahadikarya3; any trim, and the dollar figure that would avoid it;
- the fact-gathering breach (20 lines of name_check_ohs4_result.txt).

## changes
Revision 2 to revision 3, by problem:

(3) MONEY/ACCOUNTS: accepted. (e) now reverts to A42-D 2.4 (mahadikarya2 → mahadikarya3 only). The six-account list lapses with draft (g), whose heading names "the accounts". The text says the list is not neutral, and that PREREG:1721 says "never aryamhd or jaypatil-duke". Extra accounts or the card need a new owner ruling, which GO #1 may carry. The credit-fit rule ("T_core lowered to fit") was only a report in the code, so it is now implemented: mix_c2 gets --credit-usd, c2_check tmax --fix applies min(34, 32 − spend, C − 8), and preflight FAILs when credit does not cover. The planning cut (~$7.6) is stated. Fix 5 reverts every relay list: c2_check RELAY_ACCOUNTS/PROFILES, mix_c2 RELAY_ACCOUNTS, make_modal_od_c2 ALLOWED_PROFILES with modal_od_c2 regenerated, snap_monitor_c2 PROFILES, c2_chain.sh RELAY, and every comment. Code labelled "A61 g" (c2_check.py:35-39, make_modal_od_c2.py:12,29, snap_monitor_c2.py:62, c2_chain.sh:9-10,32, mix_c2.py:193-194) is named.

(3) REVERT INCOMPLETE: accepted. preflight_c2.py is now in fix 5: MAX_ROWS goes to 125,000, the money and accounts docstrings are fixed, and a new c2_tmax.json guard is added. The c2_check.py docstring (1-12), c2_chain.sh:19 and mix_c2.py docstring lines are named. All four mix_c2 changes are required (C2_MODAL_CAP_USD 40, T_MAX 34/32, ROWS_MAX 125000, RELAY two). The 0-DI refusal is "in addition, never instead".

(4) EXPORT SIDE: accepted, with both remedies. The compare set is built only by the unchanged load_hashes/HEX64 over every file the old tool read, plus the freeze hashes. g13_c2's classes may only verify, never load. load_hashes, HEX64, identifier_texts and source_hashes must be byte-identical (test b). A new fixture containment test (c) checks the compare set for every file.

(5) ENFORCEMENT POINT: accepted. New fix 6 adds an a61_85 check to preflight_c2.py. It recomputes the gated sources from the mix on disk and needs logged-sha matches, exit 0, exactly one line per input id, and PASS with no HIT for every gated source. No flag clears it, and it has fixture tests. preflight is pinned, backed up and in (i) Changed. "Incomplete" now covers any nonzero or missing exit, bad, missing, duplicate or extra lines, failed tests, A64 (h) unmet, or a sha change at the run.

COMMAND DEFECT: accepted. Backups now go into a new folder, c2_build/_backup_a61_adopt/ (mkdir fails if it exists; cp -n). Step 3 first checks that _backup_a61/g13_c2.py = 213634d7, _backup_refresh = 904d914c and _backup_a61/mix_c2.py = c38d7a8f. _backup_a61/ is never written. Also found: g13_c2.py is no longer 32256eaa. A64 (g)'s edit has been landing since 08:08 UTC (d149bc1d, then e8246a79). 32256eaa exists only in the session scratch folder, so it joins only if a verified copy is kept. The window waits for A64_TOOLS.md. While A64's hunks are present, test (g)(2) fails and no predecessor joins; this is stated.

(8) BREACH OUTPUT: accepted. The R7 "EVERY GitHub-licensed" line, the "github.com licence pages" remark, the SB6 host detail, the md_cma GitHub note, the foreseeability risk and "R7's verdict invalid on the SPDX variant" are struck. DI-TS is barred on the drop-only form-shopping bar, which needs no output. The bar covers every source in every DI-TS 8.5 input, including the three DI-TS_* ids (same upstreams). HITs are cited by id, file and time only. (d) records that revision 2 had quoted these remarks.

(7) G-PROXY: accepted. The text states plainly that A42-D 12.2 is unmet. It says the G-proxy is a selection signal (4.3, 9.3 S, 9.4, 10.2), and that 8.5's "A HIT removes the whole source" is the remedy. The false sentence is struck. Fixed consequences: exact GO #1 words, a label on every pilot, item 9 and item 10 result, no claim citing the G-proxy, and a deadline for a re-check ruling before the first item 9 score.

(2) FORM-SHOPPING: accepted. A closed list of binding inputs now applies (SOURCES_CANDIDATES.json for md_*, both SB files for SB5). A form-shopping bar covers any variant or unrecorded run before the first whole-file record, so di_hotpotqa_wiki and all DI-TS and DI-LANG sources are barred. The bar's scope covers any id, alias, derivative or renamed copy. It excludes C1 replay and G13 targets. The SB6 derivative entries are barred too.

(6) MD: accepted. The MD effect is stated with NOTES.md:3,13-14: 0 rows for md_fdc/md_peps, and 11 sources, 10,491 rows and 11 domains in MD. The floor waiver is now limited to P, the proportional step's own MD cut, through a new block_rules floor argument. proportional_trim=True is never passed on the removal path.

MINOR: accepted. The header and (i) now cover every prior entry: A62, A60, the addendum, A63, A58 E1, A64 and A65. Step 10 has --leave-out. The freeze restore brief restates the A57 audit = 0, the build_manifest skip and "never write into FREEZE/". The restore is now A64 (h)'s union record, since A64 is adopted. "If A64 is adopted" is removed, and A64 (h)'s stop applies.

## risks
REBUTTALS: none of the ten problems is invalid. Partial points:
- (7): the sentence "no remedy for a HIT was fixed" was wrong and is struck. 8.5 fixes the source-level remedy. The ruling still does not apply it to gp_* now. Removing a source from a frozen selection file after logged pilot verdicts can move S, eligibility or adoption either way, so it is not a pure drop. It is disclosed, claims are withheld, and a separate ruling must come before the first item 9 score.
- (4): the problem offered "byte-identical OR fixture test". Both are required.
- (3) money: the ~$8 cut depends on live balances and spend to date. GO #1 states the live figure.

REMAINING RISKS
- The A64 (h) union record may fail (freeze-time FORMAT.md bytes may be lost). Then the final-mix 8.5 is incomplete, MD and SB5 are removed with no refill, and the orchestrator stops and reports.
- With two accounts, the credit fit will probably cut T_core by about $7-8. The trims then run in order: item 10, wave 2, MD tail to 8,000, proportional. If MD sits at 8,000 with P = 0, any md removal fails the floor and removes MD whole.
- Any md source may HIT against the full exports. MD may then fail 8.2 and be removed whole.
- A64's edit of g13_c2.py is still in progress (08:08-08:19 UTC). The A61 window waits for it. While A64's hunks are present, no predecessor can join, so blocks need full candidates G13 runs, which puts time pressure on Mon 19 Oct ~14:00 UTC. If the window slips, the final-mix 8.5 is incomplete.
- The only 32256eaa copies are in a session scratch folder, which may vanish.
- I did not open DI-KR/work/qc_stage1.json. If it holds split_by_identifier output, the citation still names only the file and time, and the HIT is used only to drop. DI-KR is also out on the deny verdict (exit 3), which needs no 8.5 output.
- SB5's two forms (13 s apart) are both orchestrator-built, both come before its one verdict, and both are folded. Barring SB5 was judged unnecessary, because the fold keeps every form.
- The "same dataset" scope needs judgment for renamed copies. It over-drops rather than under-drops.
- The G-proxy stays a selection signal with 12.2 unmet. If a gp source shares a name with OHS-AC, selection may carry sealed-set bias.
- New code paths (fold, compare set, --remove-sources, P floor, credit fit, preflight gate) could carry bugs. Fixture tests and the skeptic review mitigate this, and every failure drops or stops.
- The earlier leaks to C2-side agents cannot be undone. The deny-list split scope stays open until C2.1.

WHAT I DID TO CHECK
- I used read-only shell only, ran no checker and made no probe. I opened no path containing ohs or sealed, no name_check_*result* file and no variant run output.
- I used stat (file times only, not opened) on name_check_result.txt, R1_TASK.md and qc_stage1.json.
- I read:
  - PREREG A42-D 1.4, 2.1-2.4, 8.2-8.5, 9.3-10.2 and 12, plus :1721;
  - A57, A58, the addendum, A63, E1, A64, A65 and the A64 r3 union-record section;
  - the A61 draft;
  - the code: source_name_check, preflight_c2, c2_check, c2_chain.sh, the mix_c2 constants and block_rules, the g13_c2 export classes and refresh list;
  - the ids and fields of the DI/SB/MD 8.5 input files, the SB5/SB6 handoff verdicts, NOTES.md and the MD/SB5 candidate counts.
- The DI-LANG input's _about note holds a remark drawn from the unrecorded runs. I saw it; it is not used.
- I computed sha256 values and compared AST segments of the hashing helpers across every g13_c2.py copy. One of those copies (32256eaa) is in the session scratch folder.
