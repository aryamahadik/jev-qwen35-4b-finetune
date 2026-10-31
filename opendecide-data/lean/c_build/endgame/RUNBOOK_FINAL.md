# RUNBOOK_FINAL: the final tests, run in parallel once the shipped 4B is fixed

Written 6 Oct 2026, 05:20 UTC, by a workflow agent. **Nothing in this file has been run.** Only the free CPU parity
check of the new helper `c_build/endgame/di_merge_think.py` ran (PASS; see (b)). No OHS-3, sealed, preds_ohs* or Jev
output file was opened to write this.

Sources: PREREG_FINAL §3-5, A10, A12, A13, A15, A16, A17, A17-B0b/B0c, A17-B1, A18, A20, A21, A21.1, A22, the A20 (c)
record, Owner decisions 6 Oct ~04:50 UTC; C_TRAIN_RECIPE §4-6 and §11; PREREG_OHS3.md; prep89/ohs3_runbook.md;
bench/decision_index/README.md; bench/ejs5/README.md + PREREG_ejs5.md; bench/v154/README.md; think/modal_think.py;
prereg_drafts/speed_cost_definition.md.

---

## 0. One-page summary

| Test | Runs when | Account (who pays) | Cap | Expected cost | Expected wall time | Owner GO? |
|---|---|---|---|---|---|---|
| (a) OHS-3, once | after the shipped model is fixed **and** the PREREG_OHS3 model amendment is committed | Jev: OpenRouter key in `.env`. OD: Modal **jaypatil-duke** credit | OpenRouter $3.00 (script cap); Modal $9.00 | OpenRouter ~$0.25-0.30; Modal ~$5.5-10 (dev smoke $1-2 + scored/timed pass $4-8 + load test $0.5-0.9) | ~1.5-2 h (Jev collect runs in parallel with the H100 pass) | **YES** (PREREG_OHS3; memory "GO points only") |
| (b) Decision Index re-check | **only if the shipped model is not C1** (A17: DI is read once per shipped system; C1 = 54.83 and C1+think = 57.74 exist) | GCP L4 `od-l4b`, Google credit (same machine and settings as A13) | 10 L4-hours | ~$6 of Google credit (C1 took 24,870 s = 6.9 h) | ~7.2 h + 15 min scoring | covered by the 6 Oct payment rule **if** GCP is credit-only (blocker B9) |
| (c) Jev read on the sealed suite (J look) | once, after the C look's verdict is logged (A15, recipe 6.2, §11 step 9) | OpenRouter key in `.env` | $1.50 | ~$0.25-0.50 | ~20-40 min | **YES** (A15: "The OpenRouter spend is an owner GO point") |
| (d) ejs-5 paired read | **only if the shipped model is C** (recipe §11 step 10, "If SHIP: ejs-5 once"); C1's S1 run is done (3 Oct) | GCP L4 `od-l4`, Google credit | 1 L4-hour | ~$0.30-0.40 | ~20-25 min | needs a PREREG_ejs5 amendment naming the new system first |
| (e) Speed/cost on H100 | any time after the shipped model is fixed (independent of the others) | Modal **jaypatil-duke** credit | $3.00 (`--max-usd 3`; script hard cap $15) | ~$1.5 | ~25-30 min | covered by the 6 Oct payment rule |
| (f) Report | after (a)-(e) | none (Mac CPU) | $0 | $0 | ~1 h | — |
| (g) Free reads from gate files: hijack (jagged/OPI), consistency, OHS-1/2 practice, Nimble, JevBench local | after the C look; JevBench/OHS-1/2/Nimble reads of C only if C ships | Mac CPU; C's extra reads on the L4 (Google credit) | 2 L4-hours | ~$0-2 | ~1-2 h | no (report-only) |

**Budget fit (jaypatil-duke):** (a) $9 + (e) $3 = $12 cap, ~$7-11.5 expected. This is exactly the owner's "keep ≥ $12 of
jaypatil-duke credit for the final tests". See blocker B5: at 05:16 UTC jaypatil-duke had already metered $20.01 this
month (credits $19.82, billed $0) and `rrun` was still running with its cap at $15.

**OpenRouter fit:** (a) + (c) expected ≤ $1, caps $4.50, against a balance of about $7.6 of the $10 limit.

**Never in this runbook:** a JevBench leaderboard submission (the owner must say so first), any read of LongBench v2,
any second OHS-3 run, any second C or J look, any card other than aryamhd's.

---

## 1. Hard rules for whoever runs this

1. **Never open** `data/ohs3*`, `data/*ohs3*`, `data/ohs3_parts/`, `lean/ohs3/`, `bench/longbench_v2/`,
   `c_spec/sealed_brief/`, the contents of `lean/sealed_nd/` (run its programs only), the contents of `preds_ohs*/`,
   and any Jev output (`*jev*`) except through the existing scoring programs at the very end. The OHS-3 programs below
   read OHS-3 in-process and print counts and aggregates only. Never `cat`, `head` or `grep` their inputs or outputs.
2. **Before and after every paid action**, run the billing check (§3) and append one line to
   `logs/budget_ledger.md` (date UTC, account, what, metered before → after, credit or card).
3. **Accounts.** Final tests use jaypatil-duke credit. Crowd = atmosphor. Round-1 training = aryamhd (card). No other
   card is ever charged. If a final test cannot fit in jaypatil-duke's credit, it moves to aryamhd (the only card
   allowed) and the ledger says so.
4. **Token-lean.** Long jobs run with `nohup … &` and a log. Wait with one blocking check of ≤ 140 s. Print ≤ 40 lines.
5. **No agent commits.** Steps marked COMMIT need the owner or an owner-authorised session.
6. **Every test runs once.** If a run dies, resume it with the same command (all harnesses below resume). Never pass
   `--limit` on real OHS-3, the real DI run or the sealed suite.

---

## 2. Step 0: what fixes the shipped model (prerequisite, not a final test)

The task text says "once the 6.3 gate has picked the shipped model". By the recipe, **6.3 decides only whether round 2
runs; the shipped model is fixed by the one C look (6.4)**:

1. Round 1 ends; the final-step adapter `q35_4b_c_r1` and its sha256 go to the look log before any read (recipe 6.2).
2. **S1 look** (sealed part A select set) plus dev guards D1-D6 → the 6.3 go / no-go.
   - 6.3 FAIL (the likely case, P ≈ 87%): no round 2. The finalist is `q35_4b_c_r1`.
   - 6.3 PASS: round 2 needs an owner GO (~$55, over the remaining C budget, recipe §4 trim rule). **STOP for the owner.**
3. **The owner declares C finished** (recipe §11 step 9). Then the **C look** (part A confirm + all of A per domain +
   B + P) and the guards P1-P3, D1-D6, D9 (recipe 6.4) give SHIP or NO SHIP.
4. Log the verdict in the sealed look log (this is what unlocks the J look in (c)):
   ```bash
   cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd
   ../../.venv/bin/python score_nd.py status
   ../../.venv/bin/python score_nd.py verdict --verdict <ship|no_ship> --look-id <id of the C look> --note "6.4 gate_c verdict"
   ```
5. `SHIP = q35_4b_c_r1` if SHIP, else `SHIP = q35_4b_main500k` (C1 stays, A10). Write a dated PREREG_FINAL note naming
   SHIP and its adapter sha256 (COMMIT), then the PREREG_OHS3 model amendment ((a), step A3) (COMMIT).

Steps 1-4 need `gate_c.py`, which does not exist yet (blocker B1).

---

## 3. Shared setup (copy once per shell)

```bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
P=../.venv/bin/python; M=../.venv/bin/modal
REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
SHIP=q35_4b_main500k            # or q35_4b_c_r1 if the C look said SHIP
SHIP_SHA=507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078   # C1; for C: shasum -a 256 of its adapter

# Modal spend check (before and after every paid action)
bill() { $M billing summary --for "this month" --json --profile "$1" | $P -c 'import json,sys; d=json.load(sys.stdin); print(sys.argv[1], "metered", d["metered_cost"], "billed", d["billed_cost"], "credits", d["adjustments"]["credits"])' "$1"; }
bill jaypatil-duke; bill aryamhd

# OpenRouter usage (prints numbers only; the key is never printed)
$P - <<'EOF'
import json, urllib.request
k = next(l.split("=", 1)[1].strip().strip("\"'") for l in open("../.env") if l.startswith("OPENROUTER_API_KEY="))
r = urllib.request.Request("https://openrouter.ai/api/v1/key", headers={"Authorization": "Bearer " + k})
d = json.load(urllib.request.urlopen(r, timeout=20))["data"]
print({x: d.get(x) for x in ("usage", "limit", "limit_remaining")})
EOF
```

**If SHIP = q35_4b_c_r1** (it trains on aryamhd), make the one local copy and put it on jaypatil-duke's Volume
(free; the memory rule allows one local copy per model):
```bash
MODAL_PROFILE=aryamhd $M volume get opendecide models/q35_4b_c_r1 ../../backups/modal_models/
shasum -a 256 ../../backups/modal_models/q35_4b_c_r1/adapter_model.safetensors     # must equal the look-log sha256
MODAL_PROFILE=jaypatil-duke $M volume put opendecide ../../backups/modal_models/q35_4b_c_r1 models/q35_4b_c_r1
MODAL_PROFILE=jaypatil-duke $M volume ls opendecide models | grep q35_4b_c_r1
```
(C1 `models/q35_4b_main500k` is already on jaypatil-duke's Volume, checked 05:18 UTC.)

---

## 4. The tests

### (a) OHS-3, run ONCE (OD scored on the H100 host; Jev twice + one unscored timing pass)

**Harness** (built 1-2 Oct, CPU-tested, `prep89/ohs3_runbook.md`): `prep89/ohs3_preflight.py`,
`prep89/ohs3_jev_collect.py` (wraps `run_jev.py`, exactly as OHS-2), `prep89/modal_ohs3_host.py` (one H100, direct
tunnel, A5 readout), `prep89/ohs3_timing.py`, `prep89/load_test_c1.py`, `prep89/ohs3_final_table.py` → `score_ohs3.py`
(the OHS-3 scorer of record; `score_ohs.py` stays the OHS-1/2 scorer). PREREG_OHS3 rules: Jev pinned to
`typesafe/jev-1.13-20260917`, run twice (`jev_guard`, `jev_r2_guard`); OD once per model in its serving configuration;
primary = micro, macro, yes/no Brier on the 1,852 base rows, Holm (3), "beats" / "matches"; 10,000 resamples, seed 0.

**Decisions to write into the config and the model amendment (recommended values):**

| Key | Value | Why |
|---|---|---|
| `models.4b.name`, `adapter_sha256` | `$SHIP`, `$SHIP_SHA` (add a `_candidates` entry for `q35_4b_c_r1` if it ships) | §2 |
| `models.4b.readout_choice` | `2view` | shipped A5 readout (choice twice, yes/no once) |
| `T_primary`, `T_single`, `T_fit_log` | C1: 1.00 / 1.00 from `prep89/t_rule_check.py --json`. C: recipe 6.0 serving T (bounded [0.8, 1.3]); see blocker B2 | 6.0 |
| `models.2b.*`, `cascade.run` | not run / `false` | final goal = 4B only |
| `decisions.od_scored_run` (D1) | `served_h100` | one OD pass gives accuracy and speed; rule 4 holds as written; no L4 needed |
| `decisions.jev_timing` (D2) | `extra_pass` | both scored Jev runs exactly as OHS-2; a third unscored timing pass (disclosed, ~+$0.1) |
| `hosting.endpoint` | `modal_forward_tunnel` | what `modal_ohs3_host.py` does |
| `speed.rule_S1` | default: "p50 CI (Jev − OD) entirely above 0 AND p95 point estimate lower" | speed draft |
| `cost.utilisation_for_claim` | 0.4 | conservative (speed draft C1) |
| `speed.headline_system` | `4b` | |
| accuracy-won rule | "beats", or "matches" (LB > −2 pp) with point ≥ 0 | final goal; quote it |
| think mode on OHS-3 | **not run** (blocker B10) | B1 rule not passed; the host has no think path |

**A. Free checks (Mac CPU, any time, no OHS-3 call):**
```bash
$P prep89/test_ohs3_prep.py                 # 97 checks, ~35 s
$P prep89/ohs3_preflight.py --config prep89/ohs3_config.template.json --template
```

**B. Missing dev 2-view reads for the DEV smoke** (default refs are `<SHIP>` and `<SHIP>_2v` on dev_nc and devp_card;
no `q35_4b_main500k_2v` exists; blocker B6). One read on the gate's L4 settings, ~10 min (or add it to the pre-reads):
```bash
# on the L4 VM (as in RUNBOOK_4B_GATE), adapter at ~/lean/models/$SHIP
~/od/bin/python od_gcp.py predict --name $SHIP --base Qwen/Qwen3.5-4B --revision $REV --layout schema_branch_mark \
    --splits dev_nc,devp_card --tta-choice --tag _2v
# copy preds_dev_nc/${SHIP}_2v.* and preds_devp_card/${SHIP}_2v.* back to the Mac
```

**C. Pre-register (COMMIT; owner):**
```bash
cp prep89/ohs3_config.template.json prep89/ohs3_config.json    # fill every <OWNER ...> with the table above
git add score_ohs3.py hosting/ prep89/*.py prep89/ohs3_config.json prep89/ohs3_runbook.md prep89/READOUT_DEV.md \
    prep89/readout_dev.json prep89/readout_dev.txt prep89/t_fit_*.json
git commit -m "OHS-3 harness + run config (before any OHS-3 run)"
$P prep89/ohs3_preflight.py --config prep89/ohs3_config.json   # must end "READY for GO"; prints the config sha256
# then commit the rule-4 readout amendment (prereg_drafts/AMENDMENT_OHS3_rule4_readout.md) and the PREREG_OHS3 model
# amendment: SHIP + sha256, readout, T, D1, D2, endpoint, S1 rule, utilisation, accuracy-won rule, sha256 of
# score_ohs3.py and prep89/ohs3_*.py, the scorer INTERPRETATION points, and the A10 D overlap disclosure (blocker B8).
```
(`score_ohs3.py`, `hosting/` and `prep89/` are untracked today; the preflight refuses until they are committed.)

**D. OWNER GO, then run (three things in parallel):**
```bash
bill jaypatil-duke                                       # log "before"
mkdir -p logs/ohs3
# D1. Jev: two scored runs (OpenRouter, cap $3; resumable; stops if run_jev.py differs from HEAD)
nohup $P prep89/ohs3_jev_collect.py --go --usage-check --cost-cap 3.0 > logs/ohs3/jev_collect.log 2>&1 &
# D2. OD DEV smoke first (dev rows only, no OHS-3; ~$1-2; the host has never run on a GPU, blocker B11)
MODAL_PROFILE=jaypatil-duke $M run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \
    --name h100_dev_smoke --dev-smoke dev_nc:60,devp_card:40 --go > logs/ohs3/dev_smoke.log 2>&1
tail -5 logs/ohs3/dev_smoke.log                          # parity bars must pass; else STOP (no OHS-3 call made)
# D3. The ONE scored + timed OD pass (D1 = served_h100), with the C1-style load test in the same session.
#     Never --detach (the Mac is the timing client; Ctrl-C stops the H100). Resumes if re-run with the same command.
MODAL_PROFILE=jaypatil-duke nohup $M run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \
    --model-key 4b --name ohs3_timing --od-preds-name $SHIP --then-load-test --go > logs/ohs3/timing.log 2>&1 &
# D4. optional: Jev latency run-to-run noise (Jev only, unscored, ~$0.1-0.35)
$P prep89/ohs3_timing.py --config prep89/ohs3_config.json --name ohs3_timing_jev2 --go > logs/ohs3/jev2.log 2>&1
bill jaypatil-duke                                       # log "after"
```
Watch only `tail -3 logs/ohs3/*.log` (counts and timings; the logs hold no item text). Kill switch: Ctrl-C or
`MODAL_PROFILE=jaypatil-duke $M app stop -y <app id>`.

**E. Score and final table (Mac CPU, ~5-10 min):**
```bash
$P prep89/ohs3_final_table.py --config prep89/ohs3_config.json --go \
    --timing logs/ohs3/timing/ohs3_timing/summary.json \
    --load-test logs/ohs3/load_test/ohs3_timing_c1/summary.json
# -> results_ohs3/score_ohs3_all.json, results_ohs3/final_table.md/.json (aggregates only)
```
Report every endpoint whatever its direction; disclose the third Jev pass, non-pinned Jev rows, unanswered calls,
refills, the 12-gram overlap (A10 D, with and without; B8) and that OHS-1/2 are practice sets.

### (b) Decision Index re-check (same harness and settings as A13 / A17-B0b)

**Only if SHIP ≠ C1.** If C1 ships, the report uses the existing `bench/decision_index/report_sample10k.json`
(54.83 vs Jev v0.1 59.51) and `report_think10k.json` (C1 + think 57.74, "DI-informed design, prototype system").

Settings, unchanged: harness `flaviusburca/decision-index` at the pinned commit in `bench/decision_index/README.md`;
the same seeded sample `sample10k.jsonl.gz` (sha256 `8b4999de…`); engine `od_engine:ODEngine` (sha256 `f3fa1c63…`,
choice read twice, yes/no once, T = 1); `--compact`; base Qwen3.5-4B @ `$REV`; GCP L4 `od-l4b` (us-east4-c). If C's
serving T is not 1, disclose that DI used T = 1 as before (argmax and accuracy do not change). The think part is the
A17-B0b knowledge route: the same 1,344 base-model think answers, merged by `c_build/endgame/di_merge_think.py`
(byte-identical to the B0b merge; parity check PASSED 05:19 UTC).

```bash
cd ~/Documents/jev
VM=od-l4b; G="--zone us-east4-c --project system-one-509903"
gcloud compute instances start $VM $G
gcloud compute ssh $VM $G --command 'nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader'  # must print nothing
gcloud compute scp --recurse $G backups/modal_models/q35_4b_c_r1 $VM:~/lean/models/      # the shipped adapter
# the harness, od_engine.py and the sample are already on od-l4b from A13; re-copy only if the sha256 check below fails
gcloud compute ssh $VM $G      # then on the VM:
  sha256sum ~/lean/decoder_io.py ~/lean/models/q35_4b_c_r1/adapter_model.safetensors \
            ~/bench/decision_index/od_engine.py ~/bench/external_quarantine/decision_index/sample/sample10k.jsonl.gz
  #   expect 8ba8ff4f...  <C sha256>  f3fa1c63...  8b4999de...
  export HF_HOME=$HOME/hf HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_XET=1
  export PYTHONPATH=$HOME/bench/external_quarantine/decision_index/repo:$HOME/bench/decision_index
  D=$HOME/bench/external_quarantine/decision_index; cd ~/bench/decision_index
  nohup ~/od/bin/python -m decision_index run --engine od_engine:ODEngine \
      --rows $D/sample/sample10k.jsonl.gz --out $D/runs/c_r1_sample10k --compact \
      --option base=Qwen/Qwen3.5-4B --option revision=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a \
      --option adapter=$HOME/lean/models/q35_4b_c_r1 --option adapter_sha256=<C sha256> \
      --option lean=$HOME/lean > $D/runs/c_r1_sample10k.log 2>&1 &
  cat $D/runs/c_r1_sample10k/status.json        # progress; ~6.9 h (C1: 24,870 s)
# Mac, after "complete": fetch, stop the VM, then score under NEW names (never overwrite report_sample10k.json)
gcloud compute scp --recurse $G $VM:~/bench/external_quarantine/decision_index/runs/c_r1_sample10k bench/external_quarantine/decision_index/runs/
gcloud compute instances stop $VM $G
Q=bench/external_quarantine/decision_index; DI=bench/decision_index
ln -s suite_sample10k $Q/sample/suite_c_r1_10k;      cp $DI/sample_manifest_sample10k.json $DI/sample_manifest_c_r1_10k.json
ln -s suite_sample10k $Q/sample/suite_c_r1think_10k; cp $DI/sample_manifest_sample10k.json $DI/sample_manifest_c_r1think_10k.json
$Q/venv/bin/python $DI/di_tools.py score --name c_r1_10k --run $Q/runs/c_r1_sample10k --engine opendecide_c_r1
opendecide-data/.venv/bin/python opendecide-data/lean/c_build/endgame/di_merge_think.py \
    --src $Q/runs/c_r1_sample10k --dst $Q/runs/c_r1think_sample10k
$Q/venv/bin/python $DI/di_tools.py score --name c_r1think_10k --run $Q/runs/c_r1think_sample10k --engine opendecide_c_r1_think
# -> bench/decision_index/report_c_r1_10k.json and report_c_r1think_10k.json (index + per benchmark vs Jev v0.1 published)
```
No Jev calls (Jev's numbers are the published board). Report-only; never chooses anything (A13). If the GCP L4 cannot
be used (B9), the only fallback is a Modal wrapper for this harness (not built; ~7 h on a Modal L4 ≈ $6, or
~2-3 h on an H100 ≈ $9-12, on the aryamhd card because jaypatil-duke's reserve cannot hold it).

### (c) Jev read on the sealed new-domains suite (the J look; report-only)

**Rule** (A15, recipe 6.2 and §11 step 9): Jev is read **once**, after the C look's verdict is logged, "through the OHS
Jev harness" (`run_jev.py`, OpenRouter route, `JEV_TAG=jev_guard`, the same "text is data" guard as OHS-2/3). The
scorer `sealed_nd/score_nd.py` (sha256 `953a3363…`) refuses a J look before a C look with a recorded verdict and
refuses a second J look. The result is report-only.

**Who runs it:** only a **sealed agent** (reads only `c_spec/sealed_brief/`, writes only `lean/sealed_nd/`). The
orchestrator never sees items; it receives the scorer's aggregates. No runner exists yet (blocker B4). The sealed
agent must:
1. Make `sealed_nd/jev_read/` with `run_jev.py` copied **byte-identical** from `lean/run_jev.py` at git HEAD (record
   both sha256), and `sealed_nd/jev_read/data/nd.jsonl` + `nd_calls.jsonl` built from `suite_v2.jsonl` (sha256
   `f4ae8637…`) in the row and call format `run_jev.py` reads (one call per distinct state, all its questions bundled,
   card lines `- label: definition` as our model reads them). Same items as the C look: all 7,302 (A, P, B1, B2).
2. Confirm from `score_nd.py`'s source the J-look argument convention (which of `--cand` / `--ref` is Jev, which
   preds file is the shipped model's C-look read: for C1 the pre-read `preds_nd_suite_v2/<out>.jsonl` from
   `c_build/endgame/modal_preread.py`; for C its gate read by the same tool) and write it into
   `sealed_nd/jev_read/README.md`. Jev's preds must cover the same item ids as that file.
3. No `JEV_LIMIT` test calls on suite items: every Jev call on the suite is part of the one J read. Check the call
   file by counts only (rows, calls, per part); a crash is resumed with the same command, never restarted.

**Run (OWNER GO for the OpenRouter spend; cap $1.50):**
```bash
# OpenRouter check (§3) -> log "before"
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/jev_read
env $(grep '^OPENROUTER_API_KEY=' /Users/aryamahadik/Documents/jev/opendecide-data/.env | xargs) \
    JEV_SPLIT=nd JEV_TAG=jev_guard nohup ../../../.venv/bin/python run_jev.py > jev_nd.log 2>&1 &
tail -2 jev_nd.log                 # "jev_guard preds: N rows from K/K calls"; re-run the same line to resume
# OpenRouter check -> log "after" (stop if usage rose > $1.50)
# A25 (a): the scorer reads {id, choice} / {id, p_yes} only. --ref = the finalist's CONVERTED .gate.jsonl from the C
# look (same sha256; refused otherwise); od_gcp-format preds go through c_build/endgame/preds_to_gate.py first.
# A refused look writes no looks.jsonl line. J CIs = the frozen scorer's 2,000 resamples / seed 7 (A25 b).
cd .. && ../../.venv/bin/python score_nd.py look --kind J --cand <per the README in step 2> --cand-name <...> \
    --ref <...> --ref-name <...> --note "J look: Jev once after the C verdict (A15)"
```
Expected: ~5 M input tokens at $0.042 per million (plus per-call billing seen so far, $0.032-0.038 per 1,000 calls)
→ ~$0.25-0.50; ~20-40 min at run_jev.py's concurrency. Risk: B2 items are 4-8K tokens; if Jev refuses long inputs,
those rows count as wrong for Jev and are reported separately.

### (d) ejs-5 paired read (only if SHIP = C)

PREREG_ejs5 §2: S1 = C1 is done (3 Oct, `c1_main500k`, readout 2view; the ledger refuses a repeat). Recipe §11 step
10: if C ships, ejs-5 once (in-domain: C trained on 6,000 commit rows from other repos, never n8n). This needs a dated
PREREG_ejs5 amendment naming S4 = `q35_4b_c_r1` + sha256, readout 2view, T = 1, before the run (COMMIT). Report form:
full set + late rows + Gate, paired bootstrap over commits vs Jev's published answers (no Jev calls; B5 report-only).
```bash
# L4 od-l4 (us-central1-a), Google credit; VM must be free (nvidia-smi prints nothing)
cd ~/Documents/jev; G="--zone us-central1-a --project system-one-509903"
gcloud compute instances start od-l4 $G
gcloud compute scp --recurse $G backups/modal_models/q35_4b_c_r1 od-l4:~/lean/models/
gcloud compute scp $G bench/ejs5/*.py od-l4:~/bench/ejs5/
gcloud compute ssh od-l4 $G     # then on the VM:
  export HF_HOME=$HOME/hf HF_HUB_OFFLINE=1; cd ~/lean
  R=7128b2b8545913fa263f6f4bbdcd0049b2368e0402d74a6516e51f24197b3a4f
  CR="--model $HOME/lean/models/q35_4b_c_r1 --base Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
  ~/od/bin/python ~/bench/ejs5/run_ejs5.py --name c_r1 $CR --rows-sha256 $R --readout 2view --dry-run
  nohup ~/od/bin/python ~/bench/ejs5/run_ejs5.py --name c_r1 $CR --readout 2view \
      --adapter-sha256 <C sha256> --rows-sha256 $R > ~/bench/ejs5/runs/c_r1.log 2>&1 &
# Mac: fetch, stop, score (paired vs Jev's published answers; C1 alongside)
gcloud compute scp --recurse $G od-l4:~/bench/ejs5/runs/c_r1 bench/ejs5/runs/
gcloud compute instances stop od-l4 $G
opendecide-data/.venv/bin/python bench/ejs5/score_ejs5.py c1_main500k c_r1 --json-out bench/ejs5/runs/scores_c_r1.json
```
~20-25 min of L4 incl. start/stop (~$0.30-0.40 Google credit). If the L4 cannot be used (B9): skip and disclose.

### (e) Speed and cost on the H100 (jaypatil-duke credit)

Two sources, both needed in the report:
1. **Against Jev, end to end:** the OHS-3 served pass in (a) (S1/S2 = client-timed p50/p95 per call, interleaved
   with Jev at concurrency 1) and its load test (cost C1 = $ per 1,000 decisions at 40% and 100% utilisation). Nothing
   extra to run.
2. **Model-side speed (fast path and think path):** the B1a harness `think/modal_think.py` (SGLang 0.5.20; DFlash is
   broken on 0.5.20, so `bf16_nospec` only) with the C1 fast path through `think/fast_timing.py`
   (`decoder_io.GraphRunner`, p50/p95 per decision at batch 1 and batched). B1a on aryamhd: fast path p50 14.1 ms /
   p95 19.2 ms (batch 1), batch 8 9.9 ms per decision; think decode 242 tok/s, cap300 1.29 s, DEER1024 3.06 s/item.
```bash
$P think/modal_think.py --dry-run        # CPU, no Modal: inputs, configs, cost estimate, caps
$P think/modal_think.py --estimate
bill jaypatil-duke                       # log "before"
MODAL_PROFILE=jaypatil-duke nohup $M run think/modal_think.py::bench --configs bf16_nospec --max-usd 3 \
    --fast-config bf16_nospec --mem-fraction 0.25 --run final_speed_$(date -u +%Y%m%d) > think/final_speed.log 2>&1 &
tail -3 think/final_speed.log
bill jaypatil-duke                       # log "after"
$P think/modal_think.py --score think/runs/final_speed_<date>
```
`--fast-config bf16_nospec --mem-fraction 0.25` are the flags of B1a's successful fast-path run (`think/b1a_run8.log`;
the default `fast_config` is bf16_dflash, which would skip the fast path here; 0.25 fixed the OOM of SGLang at 55% +
CUDA graphs = 46 GB). Expected
~$1.5 (B1a clean runs: nospec 412 s + fast path 794 s + engine starts), first run on this account also fills the HF
cache (~5 min). **If SHIP = C:** `modal_think.py` hard-codes the C1 fast path (`C1_DIR`, line 49), so C's fast-path
number needs a 2-line parameter change first (blocker B7), or the report states that C and C1 are the same
architecture (merged r16 LoRA) and quotes recipe guard D9 (C's p50 ≤ C1 × 1.05, measured by the gate).

### (f) The report

Fill `c_build/endgame/REPORT_TEMPLATE.md` from the files each row names. Aggregates only. Then write the ledger lines
and a dated PREREG_FINAL record of what ran, what it cost and every deviation (COMMIT). (The template's text was
returned by the workflow agent of 6 Oct 05:20 UTC; the agent harness blocked it from writing that file itself, so the
orchestrator saves it there.)

### (g) Free or cheap report-only reads (no new decisions)

```bash
# hijack / prompt injection (dev attack sets; Jev guard reads already exist), after the C look
#   (if C1 ships, drop the duplicate q35_4b_main500k; q35_4b_pxE_fresh = the gate's fresh 4B-E read)
$P score_jagged.py $SHIP q35_4b_main500k q35_4b_pxE_fresh jev_guard
$P score_opi.py    $SHIP q35_4b_main500k q35_4b_pxE_fresh jev_guard
# consistency on dev (equivalence flips over 722 pairs, permutation flips, complement violations): from the gate's
# output (gate_c.py D5 / PREREG 3.3 (e)(f)); C1's values are in logs/gate4b/look_ship1.txt
# OHS-1/2 practice sets (A12; never used to choose anything). C1's reads exist under the A12 name
# q35_4b_main500k_b100 (byte-identical to C1); results_ohs/ holds the A12 and A17-B0c scores. For C, read once on the
# L4 with the shipped readout (A12 settings), then score both:
#   ~/od/bin/python od_gcp.py predict --name q35_4b_c_r1 --base Qwen/Qwen3.5-4B --revision $REV --splits ohs,ohs2 --tta-choice
$P score_ohs.py q35_4b_c_r1 q35_4b_main500k_b100 --split ohs  --jev jev_guard,jev_r2_guard
$P score_ohs.py q35_4b_c_r1 q35_4b_main500k_b100 --split ohs2 --jev jev_guard,jev_r2_guard
# JevBench v1.5.4 public items, local and unofficial (C1's run exists: bench/runs/v154_q35_4b_main500k). For C on the L4:
#   ~/od/bin/python ~/bench/v154/run_v154.py --lean ~/lean --model ~/lean/models/q35_4b_c_r1 --base Qwen/Qwen3.5-4B --revision $REV
python3 ../../bench/v154/score_v154.py v154_q35_4b_c_r1 v154_q35_4b_main500k jev_p1 jev_p2 --ref jev_p1 \
    --json-out ../../bench/runs/scores_v154_final.json
# NO JevBench submission (public or sealed, incl. the $49 sealed run) without the owner's explicit OK.
# Nimble public suite (A18, report-only; only if C ships; C1: bench/nimble_suite/report_nimble_c1.json, C1+think in
# report_b0b.json). On the L4: PYTHONPATH=<di repo>:<od_engine dir> ~/od/bin/python run_nimble.py --data data --out preds_c_r1
# (run_nimble.py builds od_engine.ODEngine with C1's settings: point its adapter + adapter_sha256 options at C first),
# then on the Mac: python3 ../../bench/nimble_suite/score_nimble.py preds_c_r1
```

---

## 5. Parallel launch plan (after Step 0 and the commits)

| t (min) | Mac | Modal jaypatil-duke | GCP L4 | OpenRouter |
|---|---|---|---|---|
| 0 | billing + OpenRouter "before"; (a)-A free checks | (e) speed bench starts | (b) DI starts on od-l4b (only if C ships) | (a)-D1 Jev collect starts |
| 0-15 | | (a)-D2 dev smoke | (d) ejs-5 on od-l4 (only if C ships) | |
| 15-60 | watch logs (one check ≤ 140 s) | (a)-D3 scored + timed pass, then load test | | (c) Jev sealed read (sealed agent), then J look |
| 60-90 | (a)-E score + final table; (g) scorers | stop; billing "after" | | OpenRouter "after" |
| ~7.5 h | (b) score + think merge; (f) report | | stop VMs | |

Separate containers per test (A20 d). The DI run is the long pole; the report can ship with "(b) pending" if C1
ships, because (b) is then not needed.

---

## 6. Blockers and open decisions (in the order they bite)

| # | Blocker | Needed for | Who / fix |
|---|---|---|---|
| B1 | `gate_c.py` does not exist (recipe §11 step 3). No S1 or C look, no 6.3/6.4 verdict, no D9 latency read can run. The sealed look log is empty (`score_nd.py status`: "No looks recorded"). | Step 0, everything | orchestrator: write + CPU-test it before round 1 ends |
| B2 | No tool fits C's serving T (recipe 6.0 step 2: leave-one-group-out, median-group NLL, bounded [0.8, 1.3]); the OHS-3 harness checks T only against `prep89/t_rule_check.py` (the A5 rule). | (a) if C ships | build the 6.0 fit and teach `ohs3_lib.check_fit_logs` its log, by amendment, before the OHS-3 config is committed. Not needed if C1 ships (1.00 / 1.00). |
| B3 | Commits: `score_ohs3.py`, `hosting/`, `prep89/` are untracked; the filled `ohs3_config.json` and the PREREG_OHS3 model amendment must be committed before any OHS-3 call. Agents may not commit. | (a) | owner (or an owner-authorised session) |
| B4 | No sealed Jev runner exists in `sealed_nd/`, and the J-look `--cand/--ref` convention is unknown to non-sealed agents. | (c) | a sealed agent, per (c) steps 1-2 |
| B5 | jaypatil-duke: metered **$20.01** this month at 05:16 UTC (credits $19.82, billed $0); `rrun` still running with `CAP_USD = 15.0` (`c_build/rrun.py` line 59; the owner asked for it to drop). If the monthly credit is $30, only ~$10 is left, below the $12 reserve. | (a), (e) | owner: confirm the credit size; lower the rrun cap or stop rrun now; overflow goes to aryamhd (card) and is logged |
| B6 | No `<SHIP>_2v` dev reads on dev_nc / devp_card (the OHS-3 dev smoke's default 2-view refs); none exist for C1 either. | (a) dev smoke | one L4 read ((a) step B), or derive the file from the pre-read tool's dev reads: choice rows = mean of `<out>` and `<out>_revchoice` (the smoke compares only choice rows on the 2-view ref); pass it with `--smoke-ref-2v` |
| B7 | If C ships: `think/modal_think.py` fast path is hard-wired to C1; the OHS-3 config has no C entry; PREREG_ejs5 needs an S4 amendment; C's adapter must be copied to jaypatil-duke's Volume and `backups/modal_models/`. | (a), (d), (e) | orchestrator, before the final tests |
| B8 | A10 D requires OHS-3 "with and without the overlapping items, identified by program, counts only"; `score_ohs3.py` / `ohs3_final_table.py` have no exclusion option and no id-producing program exists. | (a) report | write a small counts-only wrapper and freeze it in the OHS-3 amendment before the run |
| B9 | GCP L4 (Google credit) is not in the 6 Oct payment decision. DI, ejs-5, JevBench-local, C's OHS-1/2 and 2-view reads were all L4 jobs. | (b), (d), (g), B6 | owner: confirm GCP is credit-only (no card); else these move to aryamhd (card) or are skipped |
| B10 | Think mode is not shippable yet: A17's B1 rule (think path ≥ 85% of full thinking at ≤ 1 s median) is unproven (B1a cap300 = 1.29 s; B1b not run). `modal_ohs3_host.py` has no think path. | what "the shipped system" means on OHS-3 | recommended: OHS-3 = the one-pass shipped 4B only; think mode reported on DI only ("DI-informed design"); owner decides before the OHS-3 amendment |
| B11 | `modal_ohs3_host.py` has never run on a GPU (ohs3_runbook §6.1). | (a) | the dev smoke (D2) runs first; stop on any parity failure |
| B12 | The A21 (d) C1 pre-reads are not done yet. A parallel agent is building `c_build/endgame/modal_preread.py` (Modal H100; sealed → `/vol/sealed_preread_c1/preds_nd_suite_v2/`, dev, attack, perm, revchoice; its docstring example uses profile aryamhd, while the owner put pre-reads on jaypatil-duke). The C look needs C1's sealed reads as its reference, and the tool says C's gate reads must use the same tool. | Step 0 | pre-read job (owner decision 1: jaypatil-duke credit) |

Owner GO points in this runbook: (a) OHS-3; (c) the OpenRouter spend of the sealed Jev read; any JevBench submission
(not planned); round 2 (if 6.3 passes).
