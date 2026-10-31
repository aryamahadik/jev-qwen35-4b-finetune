# J_HANDOFF: the Jev read of OHS-4, once, after the L1 verdict is logged (sealed-side handoff; follows c2_build/zed_orch/RULING_L1_PRELOOK.md items 5-7)

Updated 18 Oct 2026. **NOT RUN.** No OpenRouter call was made, `.env` was not read, no Jev output file was opened. Only a loopback fake of OpenRouter was used (synthetic suite).
No item text, label or count by type in this file.

## What exists
- The Jev runner is the pinned one: `ohs4_sealed/scorer/run_jev_ohs4.py` (sha 5bc81eab..., PREREG A38; hash-checked on every command). Plain httpx to OpenRouter `/v1/systemone`, model id fixed
  in the file (`MODEL = "jev-1.13"`), retries off, resumable (answered calls are skipped), key from `opendecide-data/.env` read by the runner itself, never printed. It writes only inside the
  sealed folder (`answers/jev_ohs4.jsonl`, `answers/jev_ohs4_usage.jsonl`) and prints counts.
- The frozen scorer's look J: refuses J before a logged L1, a second J, a changed suite, a changed L1 answer file (it re-verifies their sha256).
- Wrapper `c2_build/train/l1_look/j_run.py`: ordering guards, the live balance check, a spend watchdog, **the pinned-model checks of the ruling**, the J look, the spec 8.6 claims, a content-free
  `c2_build/train/J_RESULT.json` (read-only).

## Commands (from `jev/opendecide-data/lean`; `PY=../.venv/bin/python`)
```bash
$PY -B c2_build/train/l1_look/j_run.py check   # guards + LIVE OpenRouter balance (numbers only); spends nothing; no Jev call
$PY -B c2_build/train/l1_look/j_run.py go      # check -> pinned runner (concurrency 4, watched, up to 3 resume passes for transient failures) -> pinned-model checks -> the J look -> J_RESULT.json
$PY -B c2_build/train/l1_look/j_run.py score   # only the model checks + J look + result, after a COMPLETE runner pass (if `go` stopped after the runner)
```
Sealed-side commands: the orchestrator may run them (they print counts, shas and the balance only) but must not open `answers/` or the sealed folder. An interrupted `go` is resumed by running `go` again.

## Guards (each refusal content-free)
1. Hash pins. 2. The L1 verdict is logged: `L1_RESULT.json` exists AND the scorer's log holds a granted L1; no finished J (`J_RESULT.json` with status other than `not_run`). **Crash resume:** if the scorer logged J granted and the process died before the result was written, `go`/`score` finish from the saved files: no runner, no balance call, no key read, no second Jev read, no second look (the Jev answer file's sha256 is checked against the look log; a lost scorer output is rebuilt with the scorer's own pure functions and a disclosure line says so).
3. The owner's GO #2 record `L1_OWNER_GO2.json`. 4. The L1 answer files still have the sha256 recorded in `L1_RESULT.json`.
5. **Live balance** (GET `https://openrouter.ai/api/v1/key`, key from `.env`, never printed): refused if unreadable, unknown, or under USD 2.00 left.
6. **Watchdog:** usage polled every 45 s; the runner is stopped (resumable) if usage rose more than USD 1.50.
7. **The pin binds (RULING items 6 and 6b).** The runner's request id (`MODEL`) must be exactly `jev-1.13` and the frozen runner is never edited (sha 5bc81eab...). The ONE accepted SERVED id is hard-coded in
   `j_run.py`: **`typesafe/jev-1.13-20260917`** (ruling 6b: the id the provider resolves `jev-1.13` to; the bare string `jev-1.13` is NOT accepted as a served id). Before `run_look("J")` the usage file (statuses,
   error classes and the served model field; no content) is checked and NO J look is taken if any call ended HTTP 404/410, if an answered call reports any other served id (a 1.14 id, `typesafe/jev-router`, another 1.13 date
   suffix), if an answered call reports no served id, if more than one distinct served id appears, if more than half the calls failed as bad requests (HTTP 400/422), or if nothing was answered; a remaining HTTP 401/402
   also stops the look until resolved. In the model cases the wrapper writes `J_RESULT.json` with `status: not_run`, claims "not evaluable", the served-id counts and the disclosure lines; it uses no substitute id and does NOT
   use up the J look. **An earlier not-run record is renamed, never deleted or overwritten:** `J_RESULT_NOTRUN_<HHMM>Z.json` (suffix `_2`, `_3` if the same minute); a TAKEN result is never moved. Transient failures
   (429 / 5xx / timeouts) are retried only by the pinned runner's own resume (at most two further passes) before anything is scored; calls still unanswered then count wrong for Jev, their number is `unanswered_calls`.
   Served ids found are listed in `served_check.served_models`. No probe completion call is ever made.
8. **After a complete paid pass, `score` takes the one look with NO network at all** (no runner, no key read, no balance call). `go` on a complete pass also sends zero calls (the runner skips answered ids) but does read the key and
   the balance. The 6b situation (a complete 6,213-call pass refused by an over-literal first guard, $0.17 spent) is exactly this: archive the not-run record, then `score`.
   **Certificates:** the balance check (`check`, `go`) uses urllib; the python.org Python has no CA store, so export the venv's certifi bundle first:
   `export SSL_CERT_FILE=$(../.venv/bin/python -c 'import certifi; print(certifi.where())')`.

## Cost and time
About 6.2K calls. Round 1's Jev route cost USD 0.032-0.038 per 1,000 calls plus tokens; spec 9.2 estimates USD 0.5-1. Cap USD 1.50 (watchdog). About 20-60 minutes at concurrency 4, resumable.

## J_RESULT.json (report-only; Jev outputs are used for nothing else). `disclosure` comes first:
1. "Spec 8.6 asks for LB > 0 in both pinned Jev runs; A37 (h), A38 and A42-D 13.8 allow one OHS-4 Jev read, so every C2-vs-Jev claim here rests on ONE pinned run and is weaker than the two-run test in spec 8.6."
   (The citation is A37 (h) + A38 "Looks" + A42-D 13.8; the earlier "A38 (h)" was wrong.)
2. Once the served id passed: the ruling-6b line: "OHS-4 Jev comparator: Jev 1.13, requested as 'jev-1.13' by the A38-frozen runner (sha 5bc81eab...). All N responses reported the served id 'typesafe/jev-1.13-20260917' (a 17 Sep 2026 snapshot; the project's full id for Jev 1.13 since the OHS-3 era, HANDOFF.md:2642). Jev 1.14 (14 Oct) is not the comparator. A first guard compared the bare string 'jev-1.13' and refused before any look; it was corrected by ruling 6b, and the same single read was then scored once (Jev spend $X). The records cannot show the alias's snapshot on 13 Oct; no other 1.13 snapshot is on record." (N = the answered count; $X = the sum of the archived not-run records' OpenRouter spend plus this run's.) In a not-run record the earlier "Jev 1.14 is NOT the comparator" line is used instead.
3. The SPEED-3 "not run" line (same text as in L1_HANDOFF.md section 8).
Then: the frozen scorer's J aggregates; per model (C2 if read, and C1) the claims block, each labelled "comparator: Jev 1.13 (requested jev-1.13; served typesafe/jev-1.13-20260917)": R and U lower bounds, the G gap with its CI against the "-2 pp or better"
test, calibrated Brier by part (G, R, X and U: spec 8.6 says 'per part', and U's exclusion from S4 is a ship-rule scoping, not a claims rule) and the three consistency metrics per type, pooled and per part of the BASE item (looked up, never skipped), with CIs; Jev answer-file sha256, answered / unanswered counts, usage totals (calls, errors, HTTP statuses, summed token fields, ms p50/p95; no text),
the served-model check, the runner passes, and the OpenRouter before / after / spent.

## Known limits, stated now
- Speed and cost claims against Jev are not evaluable (SPEED-3 not run). Jev has no mixdev T (never fitted on Jev output): its probabilities enter as returned.
- If the pre-gate mode was C1 alone, J compares C1 with Jev only and the claims block has C1 only.
- If the served id is anything but `typesafe/jev-1.13-20260917`, the J read cannot be scored as pre-registered; changing the runner's request id changes its sha and needs the owner's own words and a re-pin.

## Dry run (synthetic data, loopback fake of OpenRouter): part of the 150 tests of `l1_look/tests` (`test_l1_dryrun.py`)
J refused before the L1 verdict; refused on low / unknown / unreadable balance with no runner call; the full path (J look logged after L1 in the temp log, result 0444, a second J refused by the wrapper
and by the scorer); a changed L1 answer file refused; the watchdog stops a runner above the cap; `check` makes no Jev call; the key is never returned or printed; HTTP 404 and 410 (no look, `not_run`
record, no response text stored), all-400 (not scored), a served model other than the pin (not scored, ids listed), a `not_run` record that does not use up the look and is replaced by a later good run,
transient 503s absorbed by the resume pass, persistent failures counted wrong and disclosed, a runner whose model id is not the pin refused, and a crash after the J look (resumed with no runner call and no second read, with or without the saved scorer output); ruling 6b: every other served id refused before the look (1.14, router, another date, missing, two distinct), the not-run record renamed and never overwritten, and the look taken by `score` on an already-complete pass with zero new calls. The real `.env` was not read; the real scorer log does not exist yet.
