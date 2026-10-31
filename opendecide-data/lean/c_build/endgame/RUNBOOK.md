# RUNBOOK: C round 1, train side (crowd → decontam → mix → round 1 → 6.3 gate)

Written 6 Oct 2026, 05:30 UTC; review fixes 06:00 UTC (hard caps on the server, exit codes, chained launches,
pre-flight gates, payer per owner decision 1, P2 on the L4 only, explicit E2 tags). Binding: PREREG_FINAL.md sections 3-5, A15, A17, A17-B1, A20, A21, A21.1, A22, the A20 (c)
record and the owner decisions of 6 Oct ~04:50 UTC; C_TRAIN_RECIPE.md sections 4-6. The final tests are in
`RUNBOOK_FINAL.md` (another session's file, same folder). Run everything from
`~/Documents/jev/opendecide-data/lean` on the Mac. **Where to start:** run `autopilot_check.py` (section 2). It prints
every family's state and the next step in this runbook.

---

## 0. State at handoff (6 Oct, 05:30 UTC)

**Done (free; no compute was charged):**
- **Adapters copied and checked.** Each copy was read back from the target Volume and its sha256 matched. Record:
  `c_build/endgame/COPY_RECORD.json`.

  | Account | Model | sha256 of adapter_model.safetensors |
  |---|---|---|
  | aryamhd | `models/q35_4b_main500k_init` (NEW; the round-1 init = C1's adapter) | `507d1c29…` (= PREREG C4 init rule) |
  | aryamhd | `models/q35_4b_base0` (NEW) | `d92d259f…` |
  | aryamhd | `q35_4b_main500k` (C1), `q35_4b_pxE` (4B-E), already there | `507d1c29…`, `1bbd8a79…` |
  | atmosphor | `models/q35_4b_pxE` (NEW; equals the aryamhd copy and `backups/gcp_models/q35_4b_pxE`) | `1bbd8a79…` |
  | atmosphor | `models/q35_4b_base0` (NEW) | `d92d259f…` |
  | atmosphor | `q35_4b_main500k` (C1), already there | `507d1c29…` |

  - `q35_4b_base0` is the A18.2 form: `crowd_select.py make-base0` zeroed 248 lora_B tensors of C1's adapter.
    The source was C1's top-level files, without `snaps/`. Local copy: `models/q35_4b_base0`.
  - Because it already exists, **skip step 1 of `c_build/crowd_r1/CROWD_READ_r1.sh`**: `make-base0` refuses an
    existing output. Use section A below instead of that script.
- **Pre-smoke input built (CPU).** `c_build/endgame/presmoke/`:
  - 1,227 rows and 271 relations, sampled as whole units from the current partial mix (125,125 rows).
  - Blocks: replay 525, F1 74, F2 71, F3 78, F5 148, F8 64, F9 68, F10 79, public 120.
  - `train_decoder.check_rows` passes on it on the Mac.
  - The config is `presmoke/q35_4b_c_presmoke.json`.
- **Tools written** (all in `c_build/endgame/`):

  | Tool | What it does | Cost |
  |---|---|---|
  | `autopilot_check.py` | read-only status | none |
  | `modal_preread.py` | pre-read tool | paid when launched |
  | `presmoke_mix.py` | builds the pre-smoke input | CPU |
  | `fill_config.py` | fills the round-1 config | CPU |
  | `r1_check.py` | preflight, first-100 abort check, step 100-300 projection, segment / relaunch cap, `mon` (the relaunch's view of the snap monitor, A28 R3); exit 0 only on GO | read-only |
  | `spend_guard.py` | credit guard, launch log, capped non-detached run, ledger lines | none (billing calls) |
  | `crowd_launch.sh` | guarded crowd launch (A0-A3), server-side cap | paid when launched |
  | `p1_presmoke.sh` | guarded P1 on jaypatil-duke credit, 14-min cap | paid when launched |
  | `r1_chain.sh` | round 1 D1-D5, every launch gated on a GO, server-side caps | paid when launched |

**NOT done (each needs the owner):**
1. **C1 pre-reads (A21 d) on the L4, and the pipeline pre-smoke (A20 d), cap $1, on jaypatil-duke credit (owner
   decision 1).**
   - **Billing re-checked (free):** 05:42 UTC metered $16.83, credit left **$13.36**; 05:48 UTC metered $17.41, credit
     left **$12.78**. The 05:15 line (metered $20.01, $10.18 left) does not match; the discrepancy is logged in the
     ledger. The newer numbers are used.
   - **rrun is still running** (`od-rrun`, ephemeral, 1 task) and the credit is falling (−$0.58 in 6 min of billing
     catch-up). `spend_guard.py check jaypatil-duke --cap-usd 1 --reserve 12` prints **REFUSED** (unexplained running
     app; and $12.78 − $12 = $0.78 < the $1 cap). **P1 was not run.** It runs once rrun has stopped and the check
     prints GO.
   - **B7 is now urgent:** rrun's own stop is $15 of rrun spend, not the owner's ≥ $12 reserve, and the reserve is
     $0.78 away.
   - **aryamhd** (card) for P1/P2: only with a new owner OK (the permission system refused it at 05:25).
   - Nothing was charged.
2. **Crowd reads were not started.** Starting them is the autopilot's job (section A).
   - **Budget risk:** all 13 families plus COMMIT come to about 80K candidate rows, which is about 240K reads. At the
     assumed 10.4 reads/s per H100 that is about $25-31, but atmosphor has only $15.22 of credit.
   - **About half the crowd will not fit.** The owner must choose: spill to the aryamhd card (rule (1) allows it, but
     the permission system asks the owner), or wait for credit.
   - **Measure the real speed on the first launch** (A6) and project again.
  - Check at 05:35 UTC: `crowd_cap.py atmosphor` on the F1-F8 task file (137,592 reads) printed **REFUSED**. It
    needs 76.5 min per container; the credit pays for 72 at $3.95/h. Re-check 05:50 UTC at the corrected $4.09/h:
    **REFUSED**, the credit pays for 69.5 min. Launch smaller family groups (`crowd_launch.sh atmosphor F3 F10`).

**Blockers found (no runbook command can run until each is fixed):**

| # | Blocker | Blocks |
|---|---|---|
| B1 | **No G13 counts-only decontamination tool exists.** `logs/decontam_counts/` is empty and no script writes it. `mixer.py --final` refuses without `--decontam-drops` files. Spec: section B | C2 |
| B2 | **`gate_c.py` does not exist** (recipe 6.1 and step 3). Neither does an L4 driver for the C gate. Spec: section E. `r1_check.py preflight` now REFUSES until `gate_c.py` + `tests/test_gate_c.py` pass, or the owner waives it | D1, E |
| B3 | **`mixer.py` crashes on the current data.** `denylist_query` (line 564) raises `TypeError: unhashable type: 'dict'`, because F10 declares its parents as dicts (`c_own_F10`). Today even `--dry-run` fails. Fix F10's parent declaration (a list of strings) or the mixer. `presmoke_mix.py` worked around it by capturing at assembly | C2 |
| B4 | **The public builders have no QC record.** `c_src/public/public-{1,2,3}/qc/QC_REPORT.json` is missing, and `mixer.py --final` refuses | C2 |
| B5 | **The score_nd.py interface is unknown on the C side** (it must not be opened). The sealed agent or orchestrator must provide its CLI and its prediction format as `c_build/endgame/SCORE_ND_CLI.json`. A wrong call could log or refuse a look. preflight REFUSES without it (or an owner waiver) | D1, E3 |
| B6 | **Snapshot monitors (recipe 5; stop rule at 25% and 50%) have no driver.** The old-slice shards (`data/c_old_slice_shards`) exist. A missing monitor means the stop rule cannot fire. preflight REFUSES until `endgame/snap_monitor.py` exists with `logs/snap_monitor_cputest.json` `pass: true` (contract: D5), or the owner waives it | D1, D5 |
| B7 | **rrun's cap was not lowered** (owner guard: keep at least $12 of jaypatil-duke credit). It still stops itself at $15. **URGENT (05:48 UTC): credit left $12.78 and falling while rrun runs** | final tests, P1 |
| B8 | **No FAM-1 step-0 driver** (recipe 5 / 11 step 6, adopted: read C1 on the L4 before launch, wall time logged). preflight REFUSES until `logs/fam1_step0_c1.json` has `wall_min` and `controls_pass: true` (and any `flags` reach the owner), or the owner waives it | D1 |
| B9 | **P2-Modal needs a PREREG amendment** (PREREG 4: gate reads on the L4 only). `modal_preread.py` refuses without the owner line `OWNER-AMENDMENT gate-reads-h100:` in PREREG_FINAL.md. Use P2-L4 | P2 |

**Review fixes, 6 Oct ~12:30 UTC (agents; no paid call):**
- **B8:** FAM-1 step 0 v1 (11:45 UTC) failed its controls: the negative control's push was +0.163 [0.036, 0.290].
  Cause, written before the re-read: uniform random labels are not a null under C1. They pull every prediction toward
  less confidence, which on confident gold-no rows is the yes direction. **Negative control v2** (`fam1_step0.py`
  `NEG_CONTROL`): the same 64 rows, with labels drawn from C1's own distribution and label smoothing 0, so the expected
  gradient is exactly 0. It runs **once** on the free L4 (`l4/fam1_rerun.sh`); v1 is kept as
  `logs/fam1_step0_c1.v1_randlabel.json`. The 4 rho flags (F1, F3, F5, F11) are a separate rule: only the owner's
  `fam1_flags` waiver clears them.
- **B5 is PARTIAL.** The dry run never reached the prediction format, and the printed fields are unknown.
  `score_nd_cli.py verify` now fails until the sealed agent confirms them (`score_nd_cli.py confirm --from <json>`;
  keys in its docstring), or the owner writes the `score_nd_cli` waiver.
- **E2** gets a step 0 that stages C1's pre-reads into `preds_*/`, sha256-checked (`stage_prereads.py`). **E4** runs
  without `--train-files` (see E4).
- **gate_c** now also checks the sealed record:
  - the stdout numbers must match the record;
  - the candidate's sealed preds sha256 must match the record;
  - the sealed metas (A21 d) must match;
  - the sealed read must be newer than `CANDIDATE_R1.json`;
  - the stop rule must not have fired, and the monitor must have read the 25/50/75% snapshots.
- **r1_chain:** seg3 launches only if the monitor is alive. The chain waits for the monitor before `ROUND 1 FINAL`, and a
  fired rule means no candidate.

**Review fixes, 6 Oct ~15:20 UTC (agent; CPU only, no paid call, nothing committed):**
- **B5 format (A25 a; superseded the earlier `nd_convert.py`, deleted):** `endgame/preds_to_gate.py` (pre-registered
  rule: choice row -> `choice` = argmax option text, a top tie -> the FIRST tied option in the readout's fixed order
  (probs key order = the item's option order); yes/no row -> `p_yes` = probs["yes"] as served, plus `choice`) writes
  `<stem>.gate.jsonl` + `<stem>.gate.json` (src/out/converter sha256, counts only).
  - **Dev proof (done, 6 Oct):** `$PY $E/preds_to_gate.py prove` -> PASS. On C1's 29 dev read files (9 dev splits x
    pre/perm/served + jagged + OPI; 26,481 rows, 13,959 yes/no), the frozen scorer's own `score_items` on the converted
    rows equals `gate_dev.score` on every row and every yes/no Brier term (0 mismatches, 0 ties, yes+no sums exactly 1).
    Record: `$E/logs/preds_to_gate_dev_proof.json`. Re-run it if `preds_to_gate.py` changes.
  - **Sealed synthetic confirm (done 16:07 UTC; re-run 17:00 UTC on the current score_nd_cli / gate_c, PASS again):**
    `$PY $E/sealed_confirm/confirm_a25.py` -> PASS, merged with
    `score_nd_cli.py confirm --from $E/sealed_confirm/confirm_a25.json` (status confirmed; `verify` -> OK). Converted
    S1 and C looks reach coverage and score exactly as the readout; a full tie scores as the first option; the scorer
    refuses unconverted files (coverage 0), `--ref-name` other than `C1`, and a second C look, and **a refused look
    writes no looks.jsonl line** (it raises before logging; under pipefail the command exits 2). gate_c's header and
    number checks accept the real printed S1 block. Real `sealed_nd/` untouched (stat only).
  - **Fixed:** the look commands passed `--ref-name q35_4b_main500k_pre`; the scorer refuses S1/S2/C unless it is `C1`.
- **Bootstrap (A25 b):** sealed looks use the frozen scorer's paired group bootstrap, 2,000 resamples, seed 7 (cell k:
  `default_rng(7+k)`); dev CIs (gate_dev) keep 10,000 / seed 0. `score_nd_cli` reads both from A25's text; the S1/C
  records carry `"bootstrap": {"resamples": 2000, "seed": 7}` (gate_c refuses otherwise) and every sealed result line
  says so (Monte Carlo difference only, ~0.1 pp on a bound).
- **G13:** methods 6 (mixdev structure hash), 8 (OPI / jagged templates) and the sealed checker (6 part P, 7 keywords)
  are in `decontam_g13.py` and the batch runner; TabFact is read from a sparse clone (`gh:`, 16,573 '#'-CSV tables,
  same hash as pipe tables); DSTC8 fetched (HF parquet branch); big_patent is streamed (`hfstream:`). Logs made by the
  older tool are flagged "methods not run (re-run)". The mixer's sealed check now passes `--structure-fields`.
- **Still open:** the mixdev ruling (F3/F6 text hits), the cosine threshold, OHS-3 / LongBench (owner), and every
  family log must be re-run with the new tool.

**Owner waivers (machine-checked by `r1_check.py preflight`).** Only the owner writes them, one line each in
PREREG_FINAL.md, starting the line: `OWNER-WAIVER r1-preflight <key>: <reason> (<date>)`, with `<key>` one of
`snapmon` (B6), `fam1_step0` (B8), `fam1_flags`, `gate_c` (B2), `score_nd_cli` (B5). **Agents never write them.**

---

## 1. Hard rules (unchanged from the binding documents)

1. **Never open:**
   - `data/ohs3*`, `data/*ohs3*`, `data/ohs3_parts/`, `lean/ohs3/`;
   - `bench/longbench_v2/`, `c_spec/sealed_brief/`;
   - the contents of `lean/sealed_nd/` (run its programs only), the contents of `preds_ohs*/`;
   - any Jev output (`*jev*`), `~/.claude/projects/**`, `/private/tmp/claude-501/**`;
   - **`c_build/preread/sealed_preread_c1/`**: C1's sealed predictions are keyed by option text, so they are sealed
     text. Programs only.
2. **Money:**
   - Free credit first, then the aryamhd card. No other card, ever.
   - Before and after every paid action, run the billing check (section 2) and add one line to `logs/budget_ledger.md`.
   - Modal billing lags by up to about 1 h. So every paid launch below has a **time cap enforced on the server** (a
     function timeout plus an absolute deadline that survives a preemption restart), or is a non-detached client
     killed at its cap (`spend_guard.py run`; Modal stops an ephemeral app when its client stops). A billing poll, or
     a `sleep; modal app stop` on the Mac, is not a cap.
   - Every launch on a credit account is logged in `c_build/endgame/logs/launches.jsonl` (`spend_guard.py record`).
     `spend_guard.py check` and `crowd_cap.py` count each logged launch's capped window after (now − 75 min) as
     **not yet billed**, and refuse while an app the log does not explain is running on that account.
3. **Credit per account** (Modal gives $30 a month, reset on 1 Nov). Credit left = 30 + `adjustments.credits` (that
   number is negative):

   | Account | Use | Credit left |
   |---|---|---|
   | atmosphor | crowd | $15.22 on 6 Oct 05:42 |
   | jaypatil-duke | pre-smoke, final tests (keep ≥ $12) | $12.78 on 6 Oct 05:48, falling while rrun runs |
   | aryamhd | round 1 | none: card only |

4. **Token-lean:**
   - Run long jobs as `nohup … > c_build/endgame/logs/<x>.log 2>&1 &`.
   - Wait with one blocking check of at most 140 s. Print at most 40 lines. No commits.
5. **Round 1 starts by itself** through `c_build/endgame/r1_chain.sh` only when D1 (`r1_check.py preflight`) exits
   0 (`GO`). `r1_check.py` exits 1 on `REFUSED`, `ABORT` or `STOP`, and every launch is chained on it with `&&` /
   `||`. It stops on:
   - the $55 projection, and the $55 **time caps** of the post-300 segments (relay `--stop-after-min`, server side;
     PREREG A28: was $35);
   - the A21 (c) first-100-step rules;
   - any `REFUSED`, `ABORT` or `STOP`, or a failed segment.

---

## 2. Shared setup (once per shell)

```bash
cd ~/Documents/jev/opendecide-data/lean
PY=../.venv/bin/python; M=../.venv/bin/modal; E=c_build/endgame
bill() { $M billing summary --for "this month" --json --profile "$1" | $PY -c \
  "import sys,json;d=json.load(sys.stdin);c=float(d['adjustments'].get('credits','0'));print('$1','metered',d['metered_cost'][:7],'billed',d['billed_cost'][:7],'credit_left',round(30+c,2))"; }
# ledger line with the live billing numbers:  $PY $E/spend_guard.py ledger <profile> "<what>: BEFORE|AFTER" --payer credit|card
# can this credit account pay a capped launch and keep its reserve?  $PY $E/spend_guard.py check <profile> --cap-usd X --reserve R
$PY $E/autopilot_check.py          # where are we? last line = NEXT step
```

---

## P. Prep (once, before round 1). P0 is done; P1 runs on jaypatil-duke credit; P2 on the L4

**P0. Adapter copies: DONE** (section 0). To re-check: `$PY $E/autopilot_check.py` should show `[x] init adapter on
aryamhd`.

**P1. Pipeline pre-smoke (A20 d), hard cap $1. Decides nothing; it proves the trainer accepts the new rows.**
- **Payer: jaypatil-duke credit** (owner decision 1, 6 Oct ~04:50 UTC; it has C1 + the init). It runs only if
  `spend_guard.py check` prints GO: credit left − not-yet-billed launches − $1 cap ≥ the $12 final-test reserve, and
  no unexplained app (rrun) is running there. The aryamhd card is used only with a new, explicit owner OK.
- **Cap:** `spend_guard.py run --cap-min 14` (14 min of one H100 at $4.09/h = $0.95). The client is NOT detached, so
  at 14 min it is interrupted and `modal app stop` is sent; if the Mac sleeps, the client dies and Modal stops the
  ephemeral app. (The speed function's own 2 h timeout is not the cap.)
- **Time:** about 6-8 min (image, 4B load, 40 steps at about 3 s). **Cost:** about $0.4-0.6.
```bash
# only if the families changed a lot since 05:25 UTC (else reuse presmoke/ as is):  $PY $E/presmoke_mix.py
nohup bash $E/p1_presmoke.sh > $E/logs/p1_presmoke.log 2>&1 &
# "P1 REFUSED" (exit 1) = the guard said no, nothing charged. Else done when the log prints "P1 DONE" / "P1 FAILED".
# The script: guard -> copy the two input files into data/ -> ledger BEFORE -> capped run -> remove the data/ files
# (also on any exit) -> remove the pilot folder on the Volume -> ledger AFTER.
```
- **Success:**
  - `logs/pilot/speed_h100_mt8192_log_every-1.json` has `oom: null`, `probe_ok: true` and `steps_run` 40;
  - every `log[].loss` is finite (preflight checks it: the A4 finite check on the smoke);
  - `s_per_step` is under 5.5.
  - `autopilot_check.py` then shows `[x] pre-smoke`.
- **On failure:**
  - a `check_rows` / `ValueError` before step 0 means the row format: send the message to the mixer owner;
  - an OOM means the micro-batch: report it, and do not change `micro_tokens` without an amendment;
  - a FILL / launch-check refusal means a config key;
  - `[spend_guard] cap ... reached`: report; do not relaunch without the owner.

**P2. C1 pre-reads (A21 d), cap $3. Kept sealed in `c_build/preread/`, sha256 only. No score is ever computed here.**

**Platform: P2-L4 only.** PREREG 4 fixes the scoring job to one GPU type, **the Google L4 VM**, and refparity is
against the stored L4 C1 read. **The candidate is later read on the same platform with the same tool** (pipeline
check: one GPU type, torch, CUDA, base revision and chat-template sha over all reads). No Modal account pays for P2.

- **P2-L4 (the only allowed platform; free Google credit, no Modal account).**
  - Platform: the PREREG 4 gate hardware, with the canonical `od_gcp.py predict`. VM `od-l4`, zone us-central1-a,
    project system-one-509903. About 2.5 h of L4 at about $1/h of Google trial credit.
  - Use the start/push pattern of `gate/RUNBOOK_4B_GATE.md` (driver `gate/gate_4b_fix2_l4.sh` is the closest model).
    The sealed suite goes to the VM only, as `~/lean/data/nd_suite_v2.jsonl`; it never goes into the Mac's `data/`.
  - On the VM, with `HF_HUB_OFFLINE=1` and common args `--name q35_4b_main500k --base Qwen/Qwen3.5-4B --revision
    851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --layout schema_branch_mark`:
    ```
    python od_gcp.py predict <common> --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev,eval_jagged,eval_opi --tag _pre
    python od_gcp.py predict <common> --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev --perm-seed 1 --tag _pre_perm
    python od_gcp.py predict <common> --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev --tta-choice --tag _pre_served
    python od_gcp.py predict <common> --splits nd_suite_v2 --tta-choice --tag _pre        # sealed: never print it
    ```
  - Fetch the `preds_*/q35_4b_main500k_pre*` files into `c_build/preread/preread_c1/`. Fetch `preds_nd_suite_v2/`
    into `c_build/preread/sealed_preread_c1/`. Then run the manifest step below.
- **P2-Modal: NEEDS AMENDMENT — do not run.** It would move the gate scoring job to a Modal H100, which PREREG 4 does
  not allow, and a refparity failure would only show at E2, after the ~$30 round 1. `modal_preread.py` refuses to
  launch unless PREREG_FINAL.md has the owner line `OWNER-AMENDMENT gate-reads-h100: <text>` (owner only; it must
  also amend PREREG 4 and the refparity REF). If the owner adopts it: payer = the owner's explicit choice (`P` is
  deliberately unset), hard cap = the tool's 44-min function timeout ($3.00 at $4.09/h), and every later C read
  (E2) must use the same tool.
  ```bash
  P=                                 # owner's explicit choice only; empty refuses below
  [ -n "$P" ] && $PY $E/spend_guard.py check $P --cap-usd 3 --reserve 12 && \
  $PY $E/spend_guard.py record $P preread_c1 44 1 && \
  MODAL_PROFILE=$P nohup $M run --detach $E/modal_preread.py::preread --name q35_4b_main500k \
    --out-name q35_4b_main500k_pre --minutes 40 > $E/logs/preread_launch.log 2>&1 &
  ```
  (Sets, in order: the sealed suite served; the 9 dev splits; jagged and OPI; `_perm`; `_revchoice`. A sealed
  set's error prints only its type, e.g. `KeyError`. **Never debug by opening the suite.**)
- **Manifest, sha256 only:**
  ```bash
  $PY - <<'EOF'
  import hashlib,json,pathlib
  r=pathlib.Path('c_build/preread'); fs=sorted(p for p in r.rglob('*') if p.is_file() and p.name!='PREREAD_MANIFEST.json')
  m={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in fs}
  json.dump({"rule":"PREREG A21 (d): sealed until the gate; sha256 only; no score computed","files":m,
             "complete":any('sealed_preread_c1' in k for k in m) and sum(k.endswith('.meta.json') for k in m)>=21},
            open(r/'PREREAD_MANIFEST.json','w'),indent=1); print(len(m),'files')
  EOF
  ```
- **Before the gate:** the stored REF is `q35_4b_main500k` (L4, 30 Sep). A fresh read on another GPU can fail
  refparity (max |dp| ≤ 0.05). The refparity look runs only at gate time (E2); the L4 avoids this risk.

---

## A. Per-family crowd read (A17, A20 d): atmosphor credit, one view, C1 + 4B-E + base 4B

**When:** a family shows `QC PASS; no crowd shards` in `autopilot_check.py`. Families that pass within about 30 min of
each other should go in one launch: each launch loads the model 3 times, about $0.5.

**Models on atmosphor (checked 05:20 UTC):**
- `q35_4b_main500k` (C1), `q35_4b_pxE` (4B-E) and `q35_4b_base0`, with the shas in section 0;
- the HF cache already has Qwen3.5-4B;
- `modal_crowd.py` asserts the pinned revision and the layout.

**A0-A3 are one guarded script** (`crowd_launch.sh`; `set -e`, so a REFUSED stops it before any upload or launch):
- A0/A1: shards and the estimate (CPU); a copy of the task file per launch in `$E/logs/`.
- Cap: `crowd_cap.py` prints CAP_MIN = min(1.5 × the estimated read time, what credit_left − $1 − not-yet-billed
  launches pays for 3 H100s at **$4.09/h**), or exits 1 (REFUSED) when the credit cannot pay or an app the launch log
  does not explain is running on atmosphor. The script then exits 1: **no A2/A3 after a REFUSED.**
- A2: upload shards (free). A3: a ledger line (BEFORE), the launch log entry, then three detached reads, each with
  `--max-min $CAP_MIN`. **The cap is enforced on the server** (`modal_crowd.py`: the call's function timeout
  = CAP_MIN, plus an absolute deadline checked at start, after every shard and by a watchdog, so a preemption restart
  cannot extend it). No Mac-side `sleep; app stop`, no app-id placeholders.
```bash
P=atmosphor; FAMS="F3 F10"; FL=$(echo $FAMS | tr ' ' ',')
bash $E/crowd_launch.sh $P $FAMS        # last line "LAUNCHED ..." or "REFUSED ..." (exit 1: owner decides)
# A4. wait (one check <= 140 s each time). Each app prints {"status": "deadline"} if it hit the cap; finished shards
#     are committed, so a relaunch (crowd_launch.sh again: it re-checks the credit) resumes.
# A5. fetch labels (free), then the completeness check
for f in $FAMS; do for m in q35_4b_main500k q35_4b_pxE q35_4b_base0; do
  MODAL_PROFILE=$P $M volume get opendecide crowd_r1_shards/$f/labels_$m data/c_crowd_r1_shards/$f/; done; done
$PY $E/autopilot_check.py | head -16                              # family now "crowd done; no G13 counts log"
$PY $E/spend_guard.py ledger $P "crowd $FL: AFTER" --payer credit
```
- **A6. Speed:**
  - After the first launch: measured reads/s = rows × 3 / (wall seconds of the slowest app − about 150 s load).
    Write it to `$E/logs/crowd_rate.json` and use it in A1 from then on.
  - If the remaining families' projection exceeds atmosphor's credit, **stop launching and ask the owner**: spill to
    the aryamhd card (rule (1)), or wait.
  - Never let atmosphor go past its credit. Its card must not be charged.
- **Success:** `crowd_select.crowd_complete(F)` is empty (`autopilot_check` moves on). Every shard has
  `labels_<model>` for all 3 models.
- **On failure:**
  - an app stopped by the cap (`"status": "deadline"`, or exit 3 from the watchdog): re-run `crowd_launch.sh` (it
    re-checks the credit; finished shards are skipped). Measure the rate first (A6);
  - `no shard manifest`: A2 was not run;
  - `not a crowd model`: wrong name;
  - a family's candidates changed after A1: `select` refuses a stale sha, so redo A1-A5 for that family.

---

## B. G13 counts-only decontamination (spec 7): per family as it passes, then once on the final mix

**BLOCKER B1:** no tool exists. The orchestrator must write it and run it (decision 1). This is the required contract,
so that `mixer.py` and `r1_check.py` accept its output.

- **Name:** `c_build/decontam_g13.py`. `autopilot_check.py` looks for that path.
- **Run:** `$PY c_build/decontam_g13.py --fam F3` (and `--final` for the mix). Each run is its own process. It prints
  counts only.
- **Training side:** what it reads.
  - Per family: `c_src/<F>/out/candidates_r1.jsonl` plus the refill pool (all candidates), and the family's
    Claude-written seeds, templates and packs (spec 7.2, "Claude-written seeds").
  - Final: `data/c_parts/c_train_r1.jsonl`.
- **Eval side** (spec 7.1):
  - the 9 dev splits, the mix-tuning dev (`c_src/*/out/mixdev_*.jsonl`), JevBench public 231 + v1.5.4, BTZSC;
  - `data/eval_opi.jsonl` and `data/eval_jagged.jsonl` (`state`, `instructions`, `options` only);
  - the 152 forbidden tasks, all splits of the OHS-1/2/3 source datasets, and TabFact tables (table hashes);
  - HateXplain and SBF posts, ejs-5 and the DI test sets;
  - LongBench v2 and OHS-3: in-process only. **Conflict to settle first:** the owner memory "exclude OHS-3 from
    scans" against spec 7.1's counts-only OHS-3 check. The owner decides whether this one counts-only program may
    read OHS-3.
  - The sealed suite is covered by `sealed_nd/qc/sealed_check.py`, which the mixer runs on the staged mix.
- **Methods:**
  1. exact normalized full text, and each sentence or line of ≥ 5 words;
  2. a substring check for every eval text of ≥ 5 words;
  3. shared word 10-grams;
  4. the Tulu-3 8-gram rule (> 50% of an eval item's tokens);
  5. MinHash on word 5-grams (Jaccard ≥ 0.8, confirmed by edit similarity ≥ 0.8);
  6. embedding cosine top-5, at the threshold fixed by hand on 100 open-set pairs at 0.85 / 0.90 / 0.95. **Not fixed
     yet: fix it before the first run**;
  7. table hashes where the eval has tables.

  Any hit drops the whole training unit.
- **Output:** `logs/decontam_counts/<F>.json` (and `final_mix_r1.json`), in this form:
  `{"set": "F3", "drop_ids": [...training ids...], "counts_by_eval_and_method": {...}, "short_items": {...},
  "inputs_sha256": {...}}`. No eval text, ever. The `drop_ids` key is what `mixer.decontam_drop_ids` reads.
- **The final mix must have 0 hits after drops** (G13). If `final_mix_r1.json` lists ids: add them to a drop file,
  re-run C2, and repeat until it is empty. `r1_check.py preflight` refuses otherwise.
- **Tool additions (7 Oct, g13-fix5; tests `endgame/tests/test_decontam_g13_fix5.py`):**
  - method 9 hashes tables in all 6 public-2 containers (markdown, pipe_plain incl. 2 columns, csv, json_records,
    key_value, html);
  - method 8 other direction (`templates_rev`, seeds only): a seed piece of >= 3 words equal to a dev / eval
    instruction sentence, or of 5-9 words inside one, makes `seeds_clean` false; shorter matches are report-only;
  - `decontam_g13.py freeze-mixdev` before a batch (status then names mixdev files changed since);
  - `decontam_g13.py refresh <sets> [--targets ...]`: when a log is stale only in mixdev (status says "`refresh`"),
    re-scan mixdev alone in minutes and merge (auto_pipeline does this itself); the same for a failed sealed-side child
    (`--targets ohs3 ohs3_src longbench_v2`) or big_patent (`G13_BIGPAT_STREAM=1 ... --targets
    ohs_src:NortheasternUniversity/big_patent`). Any tool edit, training-side change or other eval change = full run;
  - the sealed-side child keeps its own vector cache (`~/.cache/opendecide_ext/g13_emb_sealedside`, vectors + text
    hashes only; `G13_SIDE_CACHE=0` turns it off); prebuild: `decontam_g13.py side-embed-cache` (progress counts in
    `logs/decontam_counts/run/side_progress_embed.json`);
  - big_patent written ruling: `G13_BIGPAT_RULING=<tag>` counts only if PREREG_FINAL.md has the line
    `G13-BIGPAT-RULING <tag>`.

---

## C. Selection, final mix, config fill (CPU; free)

**C1. Selection.** For every family whose crowd and decontam are done:
```bash
$PY c_build/crowd_select.py select --fam F3 F10
```
- Writes `c_build/crowd_r1/select_<F>.json` and `g5_reread_<F>.json`.
- **Success:** the log line shows `pass True`, and `autopilot_check.py` shows the family `PASS`.
- **On failure:**
  - a bin budget or the label × bin chi-square (p ≤ 0.01) fails: owner review. Never hand-edit a selection.
  - `crowd read incomplete`: back to A5.
- The G5 re-read list (crowd p_g < 0.05, plus 300 seeded rows) goes to the family's G5 checker before the mix.

**C2. The final mix** (`mixer.py --final`). Needs every family `PASS` in `autopilot_check.py`, the public QC records
(B4) and the B3 fix.
```bash
$PY c_build/mixer.py --dry-run > $E/logs/mixer_dry.log 2>&1      # ~20 min; final_blockers must be [] and problems []
$PY -c "import json;d=json.load(open('c_build/mix_r1/dryrun_r1.json'));print(d['final_blockers'][:10]);print(d['problems'][:10])"
nohup $PY c_build/mixer.py --final --sealed-sha f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68 \
  --decontam-drops logs/decontam_counts/*.json > $E/logs/mixer_final.log 2>&1 &
```
- **What `--final` refuses** (the guards; never bypass one):
  - a family or public QC record that is not `pass=true`, or is not bound by full sha256 to the files on disk;
  - missing crowd label files, or a selection file that is stale, short or failing;
  - a sealed sha other than A15's;
  - no decontam drop list;
  - a failed gate: deny-list, fmt1 held-out styles, S7 held-out dev, G10, G18, `check_rows`;
  - the A22 token cap: rows ≥ 2,000 tokens ≤ 9% of new rows and ≤ 30% of new-row tokens; every row ≤ 7,900 tokens;
  - an unmet share: 90,000 replay, 45,250 own, 8,750 public, 6,000 commit, 150,000 in total;
  - `sealed_check.py` finding any row on the staged mix.
- **Success:** the log prints `FINAL written: 150,000 rows sha …`. Files written:
  - `data/c_parts/c_train_r1.jsonl`, `c_rel_r1.jsonl`, `c_mix_r1_manifest.json`;
  - `c_build/mix_r1/config_fill_r1.json`, `mix_report_r1.json`.
- **On failure:** `c_build/mix_r1/final_refused_r1.json` lists the problems. Fix them at the source family; never
  edit the mix.
- Then run G13 on the final mix (section B, `--final`). It must report 0 drop ids.

**C3. Config fill.**
```bash
$PY $E/fill_config.py --dry-run && $PY $E/fill_config.py      # fills epochs, expect_ord_rows, expect_kd_targets, expect_kd_full, seed
```
- It refuses unless the training files' sha256 equals the manifest and the config fill. It also refuses if any key
  other than the 5 FILL keys would change, or if the seed is C1's (20260925).
- It keeps the untouched template as `$E/q35_4b_c_r1.template.json`.

---

## D. Round 1 on aryamhd, 1×H100 (A28: ~$48-54, about 12 h at 4.5-4.9 s/step; hard stop $55, was $35)

**A28 (6 Oct, owner):** the round-1 hard stop is **$55** (was $35), with the same rules and formulas: the D1
projection, the D3 first-100 abort (5.508 s/step stays), the D4 projection and cap check, snap_monitor. Evidence:
`$E/logs/r1_speed_analysis.md` (real mix ~4.63 s/step, range 4.4-4.9; ~9,270 steps; ~12 h). Two tooling changes
follow from it: D1 adds a check at the measured rates, and D5 runs as relay segments, because ~12 h is longer than
the 10 h function timeout of `train_relay35` (`modal_od.py`). CPU tests: `$E/tests/test_r1_a28.py`.

**D0. Init check (done 05:20 UTC; repeat if in doubt).** The read-back sha256 must be `507d1c29…`:
```bash
MODAL_PROFILE=aryamhd $M volume get opendecide models/q35_4b_main500k_init/adapter_model.safetensors /tmp/i.st && shasum -a 256 /tmp/i.st && rm /tmp/i.st
```

**D1-D5 run as ONE gated chain** (owner decision 2: round 1 starts automatically when every gate passes):
```bash
nohup bash $E/r1_chain.sh > $E/logs/r1_chain.log 2>&1 &
# last line "CHAIN STOPPED: <why>" (ledger line written; nothing more launched) or "ROUND 1 FINAL: go to RUNBOOK D6"
```
`r1_check.py` exits 0 only on `GO`; each launch runs only after a `GO`. Every segment has a **server-side** cap
(relay `--stop-after-min` is an absolute end time that survives a preemption restart; A28: every cap is at most
540 min, 60 min under the 10 h function timeout), so a sleeping Mac or a dead client cannot overspend. Billing and a
ledger line come before and after every segment (`spend_guard.py ledger aryamhd ... --payer card`); segment wall
times go to `$E/logs/r1_segments.jsonl`.

**D1. Pre-flight** (`r1_check.py preflight`; record `$E/logs/r1_check_preflight.json`). REFUSED (exit 1) on any of:
- the config, mix, manifest, mix report, G13 logs, pre-smoke (incl. every loss finite), init sha (D0);
- the cost: steps (`config_fill.dry_run_steps`) × 2.754 s/step × 1.12 × $4.09/h + $2 > $55 (A28; was $35). 9,270
  steps ≈ $34.5, 9,375 ≈ $34.9. This old-rate check alone cannot see the real mix's speed, so **A28 adds** (keeping
  it): the same formula at the measured real-mix s/step, **central 4.63 and high 4.9**, must also be ≤ $55 (9,270 steps:
  $50.8 / $53.6; 9,375: $51.3 / $54.2; refused above 10,075 / 9,520 steps). No +12% on the measured rates: 4.9 is the
  top of their measured range (4.63 × 1.12 would be $56.6-57.2);
- **F2:** the rendered-prompt sha256 records `c_build/f2_l4.json` and `c_build/f2_local_mac.json` differ (6 views;
  train == gate_serve) — passes today;
- **A4:** `tests/test_ordinal_a4.py` fails (51 tests, ~15 s; passes today). The A4 finite check = pre-smoke losses
  finite + `check_rows` (option levels; the term is bounded) + the trainer's own abort on a non-finite term;
- **B6** stop-rule driver, **B8** FAM-1 step-0 record, **B2** `gate_c.py` + tests, **B5** `SCORE_ND_CLI.json`: each
  missing one refuses unless the owner wrote its waiver line (section 0);
- any app already running on aryamhd; a failed billing call. It also records aryamhd's metered $ as the baseline.

**D2. Segment 1: steps 0-100, the smoke (A21 c), logged every step.** `relay --stop-at-step 100 --log-every 1
--stop-after-min 30` (about 10 min, about $0.7; cap $2.05). Before any container starts, `relay`'s `_launch_checks`
(a FILL, or a file not uploaded) and the trainer's `check_rows`, `expect_trainable` (32,464,896), `expect_kd_*` and
`expect_ord_rows` refuse the launch. Done when `logs/relay_q35_4b_c_r1_stopped_at_100.json` exists.

**D3. The A21 (c) abort check** (`r1_check.py first100`; record `$E/logs/r1_check_first100.json`). **ABORT** on any of:
- a NaN or inf loss;
- a loss above 2.810 (3 × C1's first logged loss, 0.9367);
- fewer than 95 step records (a check_rows or loader failure, or the 30-min cap hit before step 100);
- s/step over steps 10-99 above 5.508 (2 × parity arm A's 2.754).
- **On ABORT:** the chain stops; nothing more runs; the checkpoint stays at `models/q35_4b_c_r1/_ckpt` on aryamhd for
  diagnosis; ledger line; the owner reviews; a re-run needs a cause and an amendment.

**D4. Segment 2: steps 100-300, then the recipe-4 projection** (`relay --expect-resume --stop-at-step 300
--stop-after-min 35`, about 12 min, about $0.8; cap $2.39; then `r1_check.py proj`).
- Spent so far = max(aryamhd metered − the D1 baseline, segment wall time × $4.09/h).
- Projected total = max(n_steps × s/step(100-300) × $4.09/h + $2, spent + rest × s/step × $4.09/h + $2).
- Budget left = floor((55 − spent − 2) / 4.09 × 60) minutes (A28; was 35). Segments for the rest (A28):
  k = ceil(rest minutes / (540 − 8)); the rest needs rest minutes + k × 8 min (one load/save per segment; k = 1 is
  the old rule).
- **STOP** (exit 1; the chain ends; ask the owner) if the projection is above $55, or if the budget left is shorter
  than the rest + k × 8 min: a run cut by the cap ends without `final` (no candidate, ~$50 lost). On GO it writes
  `$E/logs/r1_stop_after_min.txt` = min(budget left, 540) minutes, the cap of the first post-300 segment (seg3).
- **A28 numbers** (spend at 300 ≈ $2.1-2.2; k = 2): 9,270 steps at 4.63 s/step → $51.3 projected, budget ~746 min
  against 692 + 16 → **GO**, seg3 cap 540; at 4.9 → $54.2 but 733 + 16 > ~745 → **STOP**. D4 passes up to about
  4.88 s/step at 9,270 steps (4.82 at 9,375).

**D5. Segments 3, 4, ...: to the end (A28 relay)** (`relay --expect-resume --stop-after-min <cap>` each; about 11.5 h,
about $46-50 in all).
- **Why segments:** `train_relay35` has a 10 h function timeout. The relay stops each segment at its absolute end time:
  the trainer finishes the step, saves `_ckpt` (adapter, optimizer, scheduler, step, log, RNG states) and returns
  `stopped`; the client writes `logs/relay_q35_4b_c_r1_stopped_at_<N>.json`. The next segment (`--expect-resume`)
  resumes exactly at step N (the stop point and caps are RUN_KEYS, not part of the run's identity). The training
  math, step count, seed and data order do not change. `ckpt_every_min` 10 only bounds the loss on a preemption.
- **Each cap:** seg3's comes from `proj`. After a segment stops at its cap without `final`, `r1_check.py seg`
  re-reads the spend so far and the latest stop, and re-runs the D4 checks on the rest at s/step = max(proj's 100-300
  rate, the rate measured after step 300). It STOPs (the chain ends, checkpoint kept, owner decides) if the projection
  is above $55, if the budget left is shorter than the rest + k × 8 min, or if the segment made no progress. On GO it
  writes the next cap = min(budget left, 540). Expected at 4.63 s/step: seg3 540 min (to about step 7,200), then seg4
  about 205 min of budget for about 160 + 8 min of work → `final`. At most 4 post-300 segments (guard).
- **The $55 hard stop is the caps themselves:** at most (55 − spent − 2) dollars of H100 time from each launch,
  whatever happens (preemption restarts included), and each cap is re-derived from the spend so far. If a cap fires before the
  end and `seg` STOPs, the run stops at a checkpoint and there is no `final`: **the owner decides** (no relaunch
  beyond what `seg` allows).
- **If the local client dies:** the run continues (`--detach`) and still stops at its cap; logs with
  `MODAL_PROFILE=aryamhd $M app logs <app id>`. If the app crashed before `final` and the owner OKs a relaunch
  (A28 R2), from `lean/`: `nohup bash $E/r1_chain.sh relaunch > $E/logs/r1_relaunch.log 2>&1 &`. It runs
  `r1_check.py relaunch` (STOP if `final` exists, if an app still runs on aryamhd, or if the app list fails: A28 R3
  calls `modal app list --json` itself and STOPs on exit ≠ 0 or output that is not a JSON list, because
  `spend_guard.running_apps` reads an auth / network failure as "no apps"; else exactly `cap`: the minutes
  left under $55 from the spend so far, at most 540 per segment). **A28 R3:** it is also REFUSED while
  `$E/logs/snap_monitor_stop.json` (recipe 5 rule fired: no candidate this round), `snap_monitor_escalation.json`
  or `r1_monitor_dead.json` exists, or while the snap monitor is neither running (`$E/logs/snap_monitor.pid`, a live
  process) nor done (its state has the 25/50/75% reads, rule not fired); a stopped monitor is restarted by hand first
  (`nohup $PY $E/snap_monitor.py watch --profile aryamhd --name q35_4b_c_r1 >> $E/logs/snap_monitor.log 2>&1 &`; it
  resumes from its state). While the relaunched segment trains, `r1_check.py mon` is polled every 60 s and once after
  it; a monitor that stops before reading every snapshot is recorded in `r1_monitor_dead.json` (no further relaunch;
  owner decides), and after `final` the relaunch waits for the monitor's last reads, as the chain does. It then
  launches ONE segment (`relaunch1`, `relaunch2`,
  ...; log `$E/logs/r1_relaunch<k>.log`) through the chain's own `seg()` record: an open line before the launch and
  the start / end / rc line after it in `logs/r1_segments.jsonl`. So the next cap counts this segment's wall time
  even while billing lags (~75 min). If it also stops at its cap without `final`, run the same command again, and
  only while the owner's OK holds. **Never relaunch with `modal run` by hand:** that segment is not in
  `r1_segments.jsonl`, the next cap would see only the lagging billing and could overrun $55 by up to ~$5.
- **Spend so far (A28 R2):** max(billing delta, logged wall time). A launch whose line has client exit ≠ 0, or an
  open line with no closed line (the chain died mid-segment), may have run on to its cap under `--detach`: it is
  counted up to its capped window, bounded by the billing delta + the last 75 min of every logged window
  (`spend_guard.py`'s lag). The normal chain (every segment closed with exit 0) is unchanged.
- **Never** start a second D5 while one is running: two writers on one folder (preflight refuses while an app runs).
- **Monitors (recipe 5):**
  - The log prints a gradient-norm `ALERT` at 5 × the 200-step median for 20 steps. A non-finite term aborts by
    itself.
  - Snapshots are written at 25%, 50% and 75% (`snap_fracs`) to `models/q35_4b_c_r1/snaps/`.
  - **The pre-registered stop rule** (old slice below C1 − 1.5 pp at both 25% and 50%, or mean P(yes) on old yes/no
    rows drifting by more than 0.02) needs **B6's driver**, contract: `c_build/endgame/snap_monitor.py watch
    --profile aryamhd --name q35_4b_c_r1` (`r1_chain.sh` starts it beside segment 3 when the file exists). It polls
    the Volume for each snapshot, reads it on the L4 (old slice `data/c_old_slice_shards`, against C1's read of the
    same slice; plus the report-only mix-tuning dev, B3 at T = 1 and KL on 2,000 new rows), logs to
    `$E/logs/snap_monitor.jsonl`, and on the rule runs `MODAL_PROFILE=aryamhd $M app stop <relay app>` and writes a
    ledger line. Its CPU test (rule boundaries, the app-stop call mocked) writes `$E/logs/snap_monitor_cputest.json`
    `{"pass": true}`. Without it (or the owner's `snapmon` waiver) preflight refuses.
  - **Enforced (6 Oct fix):**
    - `r1_chain.sh` launches seg3 only if the monitor is alive 45 s after it starts and has logged `start`, and
      re-checks it (and the stop / escalation records) before every later segment (A28).
    - After the last segment, the chain waits for the monitor to read every snapshot. A fired rule
      (`logs/snap_monitor_stop.json`, including one fired by late reads after `final`) or a monitor that ended
      without every read stops the chain before `ROUND 1 FINAL`.
    - `gate_c.py` refuses the same cases (`check_stop_rule`).
    - preflight refuses monitor files left by an earlier run.
  - Snapshots are never read on the sealed suite, the dev gate splits, OHS, ejs-5, JevBench or LongBench, and they
    are never candidates.

**D6. End of round 1.**
- `logs/relay_q35_4b_c_r1_final.json` is written.
- Download the adapter (the one local copy, backup policy):
  ```bash
  MODAL_PROFILE=aryamhd $M volume get opendecide models/q35_4b_c_r1 ../../backups/modal_models/
  shasum -a 256 ../../backups/modal_models/q35_4b_c_r1/adapter_model.safetensors
  ```
- **Stop rule first (recipe 5):** `$PY $E/snap_monitor.py status` must show `fired: false` and reads 0.25, 0.5 and 0.75,
  and `$E/logs/snap_monitor_stop.json` must not exist. Otherwise **there is no candidate this round**: do not write
  `CANDIDATE_R1.json`; the owner reviews. gate_c refuses it anyway.
- **Before any read:** write that sha256, the UTC time and the config sha256 to `$E/CANDIDATE_R1.json` (recipe 6.2:
  one pre-registered candidate, the final-step adapter at full strength).
- `$PY $E/spend_guard.py ledger aryamhd "round 1: END (actual card spend)" --payer card` (repeat about 1 h later:
  billing lags).

---

## E. The 6.3 gate (round-1 go / no-go for round 2): sealed S1 look + dev guards, against C1's pre-reads

**BLOCKER B2:** `gate_c.py` must exist and be CPU-tested first. Its contract comes from recipe 6.1:
- It reads `gate_dev.py --mode ship` JSON and the sealed scorer's JSON.
- It applies only 6.3 (R1, R3 = D1-D6) and 6.4.
- **Tests:**
  1. it reproduces the near-null numbers;
  2. every rule at its boundary;
  3. it refuses a second confirm look, or a candidate whose sha256 is not `CANDIDATE_R1.json`'s;
  4. it refuses missing `_perm`, jagged or OPI reads.
- **A21 (d) addition:** it accepts C1's pre-reads only if their metas match the candidate's on GPU type, torch, CUDA,
  base revision, chat-template sha, layout and style. It also checks the `PREREAD_MANIFEST.json` sha256 of each
  pre-read file.

**Steps, in order:**
1. **E1. D2 set.** Re-derive the dev unseen set with C's training files added (`c_parts/c_train_r1` plus the 12
   PREREG files; name rule and text guard). Write the row list and its sha256 to the look log **before the
   candidate's first read**.
   - Command (it writes `$E/logs/d2_set_c_r1.json` once and refuses an existing one):
     `$PY $E/gate_c.py d2-set --train-files v14_parts/golden_train,train_v07,train_v08s2,train_v09s3,train_v10s4,train_v11,train_v11b,train_v11c,train_v13t,train_prism_arms,train_2b_kd,train_2b_rest,c_parts/c_train_r1`
   - Never overwrite `ship_unseen_sources.json`: it is frozen with a hard-coded sha.
2. **E2. Candidate reads, on the L4 with `od_gcp.py predict` (the P2-L4 platform and tool).**
   - **Step 0 (Mac, CPU): stage C1's pre-reads where gate_dev and gate_c read them** (`preds_<split>/`). Each file is
     sha256-checked against `PREREAD_MANIFEST.json` before and after the copy. A different existing file is never
     overwritten, and sealed files are never copied. The tool refuses before `CANDIDATE_R1.json` exists:
     `$PY $E/stage_prereads.py copy` (the last line must be `OK`; `check` hashes only, any time).
   - Upload `backups/modal_models/q35_4b_c_r1` (sha256 = `CANDIDATE_R1.json`) to the VM's `~/lean/models/`.
   - Same common args as P2-L4 but `--name q35_4b_c_r1`, and **the candidate's own tags (not P2's `_pre*`)**, so the
     files are the names gate_dev and gate_c read (`<name>`, `<name>_perm`):
     ```
     python od_gcp.py predict <common> --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev,eval_jagged,eval_opi
     python od_gcp.py predict <common> --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev --perm-seed 1 --tag _perm
     python od_gcp.py predict <common> --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev --tta-choice --tag _served
     python od_gcp.py predict <common> --splits nd_suite_v2 --tta-choice        # sealed: never print it
     ```
     Files: `preds_<split>/q35_4b_c_r1.jsonl`, `..._perm.jsonl`, `..._served.jsonl`; `preds_eval_{jagged,opi}/q35_4b_c_r1`;
     `preds_nd_suite_v2/q35_4b_c_r1` (sealed; fetched to `c_build/preread/sealed_c_r1/`, programs only).
     C1's side is `q35_4b_main500k_pre` (+ `_pre_perm`, `_pre_served`) from P2.
   - Then refparity for the fresh C1: `$PY gate_dev.py q35_4b_main500k_pre q35_4b_main500k --mode refparity` (recipe
     6.1: against the stored C1 read).
   - **If it fails, stop and ask the owner** (PREREG 4).
   - (P2-Modal / `modal_preread.py` only if the owner's `OWNER-AMENDMENT gate-reads-h100:` line exists; then both C1
     and the candidate use it.)
3. **E3. Look S1** (sealed scorer; logged in `sealed_nd/looks.jsonl`): the candidate vs C1 on part A's select set
   (2,542 items).
   - The CLI comes from the sealed agent (B5; confirmed 6 Oct, A25). The scorer verifies the suite sha and prints
     aggregates only. **Before the look:** `$PY $E/score_nd_cli.py verify` must print `OK` (dev proof + sealed confirm
     for the current `preds_to_gate.py`); otherwise no sealed look runs.
   - **The command** (= `SCORE_ND_CLI.json` `commands.S1`; both od_gcp files are converted by `preds_to_gate.py` first,
     the scorer reads the `.gate.jsonl` files, `--ref-name` must be `C1`):
     ```bash
     P=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build/preread
     set -o pipefail; $PY $E/preds_to_gate.py $P/sealed_c_r1/preds_nd_suite_v2/q35_4b_c_r1.jsonl \
       && $PY $E/preds_to_gate.py $P/sealed_preread_c1/preds_nd_suite_v2/q35_4b_main500k_pre.jsonl \
       && cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd && $PY score_nd.py look --kind S1 \
         --cand $P/sealed_c_r1/preds_nd_suite_v2/q35_4b_c_r1.gate.jsonl --cand-name q35_4b_c_r1 \
         --ref $P/sealed_preread_c1/preds_nd_suite_v2/q35_4b_main500k_pre.gate.jsonl --ref-name C1 \
         --note "S1: round-1 candidate vs C1 (q35_4b_main500k_pre), part A select set (recipe 6.3)" \
         2>&1 | tee $E/logs/s1_look_stdout.txt
     ```
     Exit 2 / a `REFUSED:` line = no look was logged (a refused look writes no looks.jsonl line); fix and re-run.
     The converters print counts only. The C look (6.4) is `commands.C` (same form, `--kind C`, tee `c_look_stdout.txt`).
   - **S1 record** (`$E/logs/s1_record_c_r1.json`, schema `gate_c.py --help-records`): transcribe the `A select
     (headline, micro)` row (n, cand%, ref%, delta, CI lo/hi in pp) and add `"bootstrap": {"resamples": 2000,
     "seed": 7}` (A25 b; the frozen scorer's, reported in every sealed result line; dev CIs stay 10,000 / seed 0).
   - gate_c checks that every number in the S1 record is among the printed ones (pp or fraction, one block), and that
     the capture holds exactly one look header naming kind S1, the candidate, ref C1, scope 2988 and the sha256[:12]
     of both converted `.gate.jsonl` files (which `preds_to_gate.py check` ties to the hashed od_gcp files). It also hashes `c_build/preread/sealed_c_r1/preds_nd_suite_v2/q35_4b_c_r1.jsonl`
     against the record and compares both sealed `.meta.json` files on the A21 (d) fields.
   - Nobody looks at per-item results.
4. **E4. Dev guards:**
   ```bash
   $PY gate_dev.py q35_4b_c_r1 q35_4b_main500k_pre --mode ship --json logs/ship_c_r1.json
   ```
   - **No `--train-files`** (fixed 6 Oct). gate_dev must use the frozen primary set (the 12 PREREG files).
     - With C's 13 files it sets `registered` to false and adds the note "not the pre-registered 9 splits and 12
       training files", and `gate_c.check_dev` then refuses ("gate_dev says NOT FINAL").
     - If C's files change the derived unseen set, gate_dev calls `stop()` and writes no JSON at all.
     - D2 on C's files comes from E1 (`gate_c.py d2-set`); gate_c applies it in E5. The frozen primary D2 is
       report-only (`d2_frozen_report`).
   - Its own verdict line is printed but does not decide C.
5. **E5.** `$PY gate_c.py --look 6.3 …` gives **R1**: CAND − C1 ≥ +2.0 pp on the select set and the paired 95% LB >
   0. It also gives **R3**: D1-D6 pass:

   | Rule | Test |
   |---|---|
   | D1 | full-set LB > −1.5 |
   | D2 | not (point < −1.0 and UB < 0) |
   | D3 | yes/no and choice ≥ C1 − 1.0 |
   | D4 | Brier ≤ C1 + 0.005 (PREREG 3.3 (d) cross-fit T) |
   | D5 | equivalence and permutation flips ≤ C1 + 2 pp |
   | D6 | ASR veto |

6. **Outcome:**
   - **Round 2 runs only if R1 and R3 both pass.** P(round 2) is about 13% under the prior.
   - Otherwise there is no round 2, and the finalist is round 1's candidate.
   - Then: the owner declares C finished, followed by the one confirm look (6.4) and `RUNBOOK_FINAL.md`.
   - Log the realized select SE and restate the confirm power **before** the confirm look.
   - Diagnostics (R2 learning, R4 retention) are report-only.

---

## F. Failure quick table

| Symptom | Do |
|---|---|
| `autopilot_check` says `QC sha binding` | the lane must re-run QC on the files on disk (stale pass) |
| crowd app stopped by the time cap (`"status": "deadline"` / exit 3) | `MODELS=<that model> bash $E/crowd_launch.sh atmosphor <FAMS>` (re-checks credit; resumes per shard) |
| `crowd_cap` / `crowd_launch` REFUSED | stop; owner chooses aryamhd card spill or wait (never past atmosphor's credit) |
| `spend_guard check` REFUSED (P1) | nothing charged; wait for rrun to stop / owner (B7) |
| `modal_preread.py` "NEEDS AMENDMENT" | use P2-L4 (PREREG 4) |
| `mixer.py` `TypeError: unhashable type: 'dict'` | B3: F10 parents must be a list of strings |
| `--final refused` | read `c_build/mix_r1/final_refused_r1.json`; fix at the source |
| preflight `REFUSED` | the chain launched nothing; fix the listed item, or (projection > $55 (A28), B2/B5/B6/B8) the owner decides / waives |
| first100 `ABORT` | stop; keep `_ckpt`; owner review; re-run needs an amendment |
| proj `STOP` | `modal app stop` is not needed (the segment ended at 300); ask the owner before D5 |
| seg `STOP` / D5 ended without `final` | the $55 caps (A28) cannot finish the rest, or a segment crashed: owner decides; a relaunch only via `r1_chain.sh relaunch` (D5, A28 R2: logged, so each cap counts it) |
| refparity fails at E2 | stop all looks; owner (PREREG 4) |
| `stage_prereads.py` REFUSED | a pre-read changed or is missing (sha256 != manifest): stop; owner (A21 d) |
| gate_c "not among the numbers the scorer printed" | the record was mis-transcribed: fix the record from the stdout capture (never re-run the look) |
| gate_c / chain "stop rule fired" or "snapshot reads missing" | no candidate this round (recipe 5); owner reviews |

## G. Files

| File | What |
|---|---|
| `c_build/endgame/autopilot_check.py` | read-only status and the next step |
| `c_build/endgame/r1_check.py` | preflight / first100 / proj / cap; exit 0 only on GO |
| `c_build/endgame/fill_config.py` | fills `runs/q35_4b_c_r1.json` from the mixer |
| `c_build/endgame/crowd_cap.py` | crowd time cap from the estimate, the credit left and not-yet-billed launches ($4.09/h; REFUSED when the credit cannot pay) |
| `c_build/endgame/crowd_launch.sh` | A0-A3 in one guarded script; the cap goes to `modal_crowd.py --max-min` (server side) |
| `c_build/endgame/spend_guard.py` | billing, launch log, `check` (credit − unbilled − cap ≥ reserve), capped non-detached `run`, ledger lines |
| `c_build/endgame/p1_presmoke.sh` | P1 on jaypatil-duke credit behind `spend_guard check`, 14-min cap |
| `c_build/endgame/r1_chain.sh` | D1-D5 chained on `r1_check.py` exit codes, server-side caps, ledger per segment |
| `c_build/endgame/logs/launches.jsonl`, `r1_segments.jsonl` | launch log (unbilled spend), round-1 segment wall times |
| `c_build/endgame/modal_preread.py` | Modal H100 pre-reads: NEEDS AMENDMENT (refuses without `OWNER-AMENDMENT gate-reads-h100:`) |
| `c_build/endgame/presmoke_mix.py`, `presmoke/` | the pre-smoke input (sample, sha256s, config) |
| `c_build/endgame/COPY_RECORD.json` | Volume copies and read-back sha256s |
| `c_build/endgame/logs/` | every launch log and check record |
| `c_build/preread/` | pre-read outputs (`sealed_preread_c1/` is sealed) |
| `c_build/endgame/stage_prereads.py` | E2 step 0: C1's pre-reads into `preds_*/`, sha256 vs the manifest (gate time only) |
| `c_build/endgame/l4/fam1_rerun.sh` | FAM-1 step-0 re-read (negative control v2) on the free L4; stockout fallback + 20-min retry |
