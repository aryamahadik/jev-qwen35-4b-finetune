# L1_HANDOFF: C2's one pre-registered OHS-4 look, run-only (sealed-side handoff; follows c2_build/zed_orch/RULING_L1_PRELOOK.md)

Updated 18 Oct 2026 after the Opus ruling. **NOTHING HERE HAS BEEN RUN ON REAL DATA.** No Modal call, no spend, no model read, no score on OHS-4; the real
`ohs4_sealed/scorer/looks.jsonl` and `ohs4_sealed/answers/` do not exist. This file holds no item text, no label, no count by type and no content of any sealed
path (path names only). Everything was exercised only on a SYNTHETIC suite (section 11).

## 1. Hashes (PREREG A38 pins)
All OK: `MANIFEST.json` (c0217e77...), suite (5f303084...), request file (34993431...), Jev runner (5bc81eab...), scorer (2743ae8c..., from the manifest) and
EVERY file the manifest lists (all 243 are re-hashed on every command, about half a second). Re-checked on every command; a difference stops with `REFUSED: hash mismatch: <file name>` (names only).

## 2. The commands (from `jev/opendecide-data/lean`)
```bash
PY=../.venv/bin/python
$PY -B c2_build/train/l1_look/l1_cli.py check          # 0. free, CPU, changes nothing: GO or STOP with the reason
MODAL_PROFILE=mahadikarya3 ../.venv/bin/modal run c2_build/train/l1_look/modal_app_l1.py::l1 --run-id l1_$(date -u +%m%d_%H%M) [--finish]   # 1. THE GPU job
$PY -B c2_build/train/l1_look/l1_cli.py finish         # 2. CPU: freeze T -> answers -> the frozen scorer's L1 -> S1-S6 -> c2_build/train/L1_RESULT.json
$PY -B c2_build/train/l1_look/l1_cli.py freeze-t       # optional, between 1 and 2: see T (dev numbers only) before the look is taken
```
`--finish` runs step 2 right after step 1. Only `modal run` is accepted (no `deploy`, `serve`, `shell`, `--detach`). Payer `mahadikarya3` through
`grid_h100/OWNER_GO1_PAYER.json`; `aryamhd` is refused always; the C2 relay accounts are refused until training is over.

## 3. What must exist before step 1 (each is a guard)
| File | Role |
|---|---|
| `c2_build/train/L1_OWNER_GO2.json` | The owner's GO #2 in his own words (`go`, `owner_words`, `written_utc`). Also required by J. |
| `c2_build/CANDIDATE_C2.json` | `name q35_4b_c2`, `grid_candidate`, `adapter_sha256`; one of `train/GRID_RECORD.json` with the same sha. A `symmetris*` flag is refused. |
| `c2_build/logs/gate_c2_pregate_q35_4b_c2.json` | The pre-gate result `gate_c2.py pregate` writes; same adapter sha; newer than CANDIDATE_C2.json. |
| `c2_build/train/WAIVER_B_A100.json` | PREREG Record A100, judged by the orchestrator's own `c2_build/waiver_a100.waiver_active` (the full quote equals the A100 sentence, waives (b) only, and the sentence is in `OWNER_GO_C2.txt` and in PREREG's Record A100), not by the record id alone. |
| `c2_build/train/CHOSEN_A98_NOCANDIDATE.json` + a NEW `c2_build/train/CHOSEN.json` | A100 mode only (RULING item 8): the A98 record (sha 54ba8937...) kept for audit; the re-run's CHOSEN.json names the same candidate and sha as CANDIDATE_C2.json. |
| **`c2_build/train/PARITY_<grid_candidate>.json`** (canonical; also found under `grid_h100/results/*/parity/<cand>/`) | A passing H100 parity record for THIS candidate (C1 + C2 mode): `bar.PASS` and `bar.PASS_gate` true, `all.argmax_agree` >= 0.995 on n >= 2000, `gpu` H100, same cand and adapter sha, no listed problems. Written by `modal_app_grid.py::parity`. |
| `train/GRID_RECORD.json`, `logs/p7_prompt_sha_check.json`, `models/q35_4b_c2/` on the payer Volume | Exist (the grid ran from them). |
The real `PARITY_final_a10.json` (sha 95f0a220...) and the real `CANDIDATE_C2.json` (sha 86ce1de4...) were read (non-sealed) and are ACCEPTED by the guard; only the pre-gate result is still missing. The A97 (2) copy record is the orchestrator's step and is not a runner guard (its file name is not fixed anywhere); the pre-gate must be newer than CANDIDATE_C2.json (checked).

**Parity guard (note).** The ruling (item 8, precondition 5) says parity "is not a runner guard" and allows a "parity pending" wording. The coordinator's later
instruction is stricter: the runner REFUSES without a passing parity record, and I built that. So the "pending" wording can never appear; every result with S1-S6
all passing also names the parity record. Say so if the ruling's softer form is wanted.

**Pre-gate reading (A100).** Effective PASS (C1 + C2 in one job) when the result says pass, OR when the ONLY failing check is a FAILED (b) and the A100 waiver
record is valid. Then `disclosure[0]` of `L1_RESULT.json` is the ruling's A100 line (with the candidate's (b) numbers from the waiver record) and S6 shows the
waived check. C1 alone only if another check fails. A (b)-only failure with the waiver missing is REFUSED (never read as C1 alone). An unmeasured (b) is not
waived. Under the waiver the candidate must be `final_a10` AND its adapter sha256 is pinned in code (`93aba519264b8ad3fa4b8e2a80a5b89fe7eb5d184d789cc5fcfdd32c46b08041`); anything else stops the runner: "stop and report".

## 4. Guards (all CPU-tested; refusals are content-free)
`prepare_plan` (GPU step), in order: (1) hash pins, EVERY manifest file; (2) one look only (no `L1_RESULT.json`, no granted L1 in the scorer's log, no answer files, no raw
reads); (3) owner GO #2; (4) CANDIDATE_C2.json; (5) pre-gate + waiver: the pre-gate's identity and order are REQUIRED, never skipped (CANDIDATE `written_unix`, pre-gate `time_unix`,
`checks.candidate.adapter_sha256` and `cand` must all be present and valid; `written_unix <= time_unix`; the sha equals the candidate's; cand is `q35_4b_c2`); (6) A100 preconditions and the
parity record (C1 + C2 mode); (7) the mixdev file must be the gate's (sha from the grid plan) and the A80 (c) trained families must leave at least 2 groups per type; (8) the request file is the
suite's and the suite has every field the rules read (`l1verdict.suite_problems`: x_pair pairs, attack_pushes_toward, base items of the consistency rows, group ids, R domain_index), so a missing
field can never surface after the look; (9) payer guard + ledger (the grid's USD 15.00 ledger: stop-launch 13.50, cancel 14.60; timeout 3,000 s, one container under about USD 3.8); (10) the estimate fits.
`write_raw` re-checks "no raw reads yet" first, so a concurrent second launch can never overwrite the read-only raw reads.
`finish` re-checks: run record ok; the raw reads are the bytes the GPU job returned (sha256 against `run_record.json` / `RAW_RUN.json`); pre-gate mode, waiver sha and parity sha equal those of the GPU
job; T frozen from dev reads BEFORE any sealed raw read is opened and never re-fitted; BOTH models' answers are computed and validated (every call answered, keys exactly the options, finite, sum 1) BEFORE
either answer file is written, and before the look; the look is the frozen scorer's `run_look("L1")`.
**Crash resume (no second look).** If the scorer logged L1 granted and the process died before `L1_scorer_output.json` was saved, `finish` again: checks the answer files' sha256 against the look log, rebuilds the
printed output with the scorer's own pure `report` / `compare` functions (no look), saves it read-only, adds a disclosure line saying so, and finishes. If the output was saved, it is used. The look log keeps ONE granted L1.
**Files for J:** `answers/c1_ohs4.jsonl`, `c2_ohs4.jsonl`, `raw/*` are written once, mode 0444, with sha256 in `answers/SHA256SUMS`; a re-run reproduces the same bytes or refuses; the scorer's J look and `j_run.py` re-verify them.

## 5. The GPU job (the grid's path)
One container, one H100 (`H100!`, `max_containers=1`, `retries=0`, payer Volume read-only, nothing written to Modal storage). Same image build steps and server
arguments as the 19 grid reads: SGLang 0.5.20 on `sglang_host.server_cmd` (merged BF16, fp32 LM head, hybrid extra_buffer cache, triton linear-attn, no
speculation), resolved args held to the S1 pin, one `path_sha256` over both boots, merges by `merge_direct` (held to C1's sha 507d1c29... and to the candidate's sha),
the grid reader (`l1reader` = `GridReader` + an in-memory set + errors by class name only). C1, then C2. Per model: the C2 mixdev (dev, for T) and the look's calls with
the A5 readout (choice: given + exact reversal averaged; yes/no once; T = 1 as served). The rows travel as a function argument (never a Volume or an image layer).
The container prints counts and seconds only and keeps no server log. Region: unpinned, as the grid ran (the only mode).

## 6. The temperature T (RULING item 1; binding procedure, implemented in `l1temp.py`)
Per model (C1, C2 each) and type (yes/no, choice), on THIS job's 2-view c2_mixdev reads at T = 1, **only the A80 (c) trained-family rows** (T33, T12, T24, T07 and the
report-only file are out): groups = the union of `sampler:S5` (one group), `pack:<meta.domain_pack>` and `register:<meta.format_style>` (a row with no value joins no
group of that kind; a group needs >= 1 row of the type, no minimum; fewer than 2 groups = stop, no fallback). M(T) = median over groups of `calibrate.nll` for every T of
`calibrate.GRID` (0.25..10.00, step 0.05); T_raw = first argmin; **T = min(1.3, max(0.8, T_raw))**. Applied after view aggregation with `calibrate.scaled`. Frozen in
`L1_T_FROZEN.json` (0444, sha in the result) with T, T_raw, M(T_raw), M(1.0), groups per kind, row count, the mixdev sha, and REPORT-ONLY fits (by meta.family, pack only,
register only, C1's shipped 1.00/1.00). Only T binds. (On the real mixdev: 18 trained families, 138 yes/no and 130 choice groups; the fit takes about 1 s.)

## 7. The verdict (spec 7.3, one look; RULING items 2-5)
S1 R: diff >= +5.0 pp and paired LB > 0. S2 G: LB > -1.5 pp. S3 complement pairs whose base is in G or R, cluster = group_id, the scorer's violation definition: C2 <= C1
(a tie passes) and UB(C2 - C1) < +0.01 (a rate = 1.0 pp). S4: **binary** (p_yes - gold)^2 (the D4 scale) over the yes/no scored items of G, R and X at the mixdev T,
C2 <= C1 + 0.005; part U and the embedded consistency calls are out; the scorer's 2-class number (= 2 x binary) is stored report-only. S5: PREREG 3.3 (g) OPI attack
success, point rule C2 <= max(C1 + 2 pp, 3%); the frozen scorer prints NO attack-success figure (X accuracy only: part, clean, attacked), so its X figures and the
attacked error rate are stored beside S5 with the difference disclosed (and any attack/ASR key the scorer might print would be found and stored). S6: pre-gate recorded
(+ waiver). Bootstrap: the scorer's recipe (10,000, seed 0, group_id, 2.5/97.5), cross-checked against the scorer's printed numbers. **Report-only, also in the result:** `s1_excluding_r20` (PREREG A38 sensitivity: S1 on part R without the items of domain_index r20, from the answer files; the S1 verdict uses all of R). **S3 on the real suite:** the complement rows are placed by looking up each row's BASE item (never trusting a field, never skipping); the real suite's complement bases are R and U items (none in G), so S3 uses the R-based pairs and the U-based ones are out of scope (their number is stored). Rules text hash
`l1verdict.RULES_SHA` = 65c8a26fb1f2ea5a6391aaea1da6eac2dc80eef3eff8470ffc4c4c1b4e9e7fe3 (replaces e6571a8f...; stored in the result). `L1_RESULT.json` starts with
`disclosure` (A100 line first when (b) was waived, then the SPEED-3 line) and carries `carried_rulings` (A68, A80, A95, A97 (3), A88/A89, Jev no T) and the `parity` record.

## 8. SPEED-3: not run (RULING item 7); region
Allowed ("in full or not at all", A42-D 2.3). No partial SPEED-3 is reported. The result and J_RESULT carry the line: "SPEED-3 was not run: the load test was not built before
the one-shot final, and A42-D 2.3 allows it only in full or not at all. The spec 8.6 Speed and Cost claims against Jev on OHS-4 are therefore not evaluable; any latency
or cost figure quoted comes from earlier C1 measurements (SPEED-2 / C1 optimisation) and is labelled as such." The region is unpinned ('any'), as the grid ran; that is the only mode (no environment variable is read for it).

## 9. Cost and time (real request file; ledger spent 8.01 of 15.00 after the parity job)
| scenario | C1 + C2 | C1 alone |
|---|---|---|
| low | 9.8 min, USD 0.80 | 5.8 min, USD 0.50 |
| likely | 13.6 min, **USD 1.09** | 8.2 min, USD 0.68 |
| high | 22.6 min, USD 1.77 | 14.1 min, USD 1.12 |
One container is capped near USD 3.8 (3,000 s). The parity job (about USD 0.8) is separate. CPU finish about 2 minutes.

## 10. If something goes wrong
| Event | State | Action |
|---|---|---|
| a guard refuses | nothing started | fix the named file; re-run `check` |
| GPU job fails or is cancelled | no raw files, look NOT taken | the ledger line shows the cost; re-run step 1 |
| `finish` stops before the scorer | answers (0444) and T may exist | fix; re-run `finish` (same bytes or refusal) |
| `finish` stops after the scorer granted L1 | `answers/L1_scorer_output.json` saved | re-run `finish`: no second look |
| scorer refuses (`L1 already used`) | logged in the look log | stop; report |

## 11. Dry run (synthetic suite only): 150 tests pass (54 guards, 16 T, 18 verdict, 7 Modal glue, 55 end to end; about 80 s, CPU)
Run the files one at a time (`pytest -q l1_look/tests/test_l1_guards.py`, then `test_l1_temp.py`, ...); no test shares a temp file any more (the verdict tests build records in memory).
An OHS-4-shaped suite of generic fake items; the sealed scorer and Jev-runner CODE copied into a temp tree (no data). Covered: every guard in order with refusals checked for item text; the pre-gate identity
and order fields (each absent or mistyped field refused, equal times pass); the A100 waiver through `waiver_a100.waiver_active` (record id, scope, truncated or extended quote, quote missing from PREREG or
OWNER_GO_C2.txt), the pinned adapter, A100 preconditions; parity cases; the gate's mixdev sha; the group-count stop; ALL manifest files re-hashed (an extra entry, a missing and a tampered one); the T
procedure against `calibrate.py`'s own functions (bit for bit); the full GPU job on fakes (real tokenizer and P7 check, real tiny merges, fake SGLang, two boots on one path); the reader daemon as a subprocess;
the entrypoint glue; `finish` end to end (T first, answers 0444, one look, S1-S6, second look refused), the crash between the granted look and the saved output (resumed, aggregates equal to what the scorer printed,
still one look), invalid or incomplete answers refused before the look with NEITHER answer file written, raw reads checked against the run record, `freeze-t` end to end, C1-alone and A100 modes; the S1-without-r20
report, the base-item lookup (a missing base or a conflicting base_part stops), `suite_problems`; J on a loopback fake of OpenRouter incl. a crash after the J look (resumed with no runner, no balance call,
no second read). The real looks log, answers folder and `.env` were never touched. A dry run of the rule evaluation with DUMMY in-memory answers (never a model) on the real suite confirmed that every field the rules read
is present (counts per part only; nothing kept on disk).

## 12. File shas (new files only; no pinned file was edited; sha256; `RULES_SHA` unchanged 65c8a26f...)
```
6f57d5336c9eac91b73087fb777fb0e4339478e6651e3f1cd15e7b296c849688  l1_look/__init__.py
c6bb2fd550d5e3ae173cf0a92419a499d0402a8f4736709303d0c147807dcd57  l1_look/j_run.py
a08d83d55ad123c24660877e51dbac802534cd17f8e6ac2bb87b5754ea916520  l1_look/l1_cli.py
a7bf720b7257e6b843ae419842e6189adace8f361efe1e84b33ff00cbf846c0c  l1_look/l1common.py
69f597097a04099a1af756323bdebffbee7637fe207efa45cf864b44094f2116  l1_look/l1reader.py
94fafba77259ca327cacd517bbd904cac0308e3060a3a366d454d540e0bcced9  l1_look/l1session.py
6bbe99dacb320e9f3fe7de468117e54718038bb551072edb6f22e973da0e54f7  l1_look/l1temp.py
ebcc970c77e85b75758fe8c310d016e225d7878163d3f7bf759fdcc1b2bccea7  l1_look/l1verdict.py
6000a2e37b50edb87291d8cb008f04a2f0c6ee60f371523c1ed1bf13bb3b405b  l1_look/modal_app_l1.py
dcef45f1c8a9387db523cf707f1f99c347b0751019e89399a21abf3a01e615a9  l1_look/tests/synth.py
8d222b5f47c6f767e40e1aa0a9ca1ffb6200188a6bb4dd5695f8f70033462cf4  l1_look/tests/test_l1_dryrun.py
e7b5911886924c0d4a034e6931d6061cd5f2ba5967fcb48c4a985e17ed793bae  l1_look/tests/test_l1_guards.py
0ce05bc5db2b7b7714025732d8fc36202a29c99fd69ce02e2e38ed909ae3e922  l1_look/tests/test_l1_temp.py
aadf0e110aaaba59865826640c936302707ea370a016022301c0f8c4bf90878c  l1_look/tests/test_l1_verdict.py
7382bac74038496235986f209c2381f5963f515b85b6ff91b64c16bbe01220ac  l1_look/tests/test_modal_app_l1.py
```
The orchestrator adds them to `c2_build/zed_orch/a64/A64_TOOLS.md` (`l1_cli.py shas` prints the tool files; `L1_RESULT.json` records them again at the look). J: `J_HANDOFF.md`.
