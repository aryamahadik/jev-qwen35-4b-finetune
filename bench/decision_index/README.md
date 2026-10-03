# Decision Index sample run of C1 (PREREG_FINAL A13, report-only)

This folder runs our shipped 4B (C1 = `Qwen/Qwen3.5-4B` @ `851bf6e8` + LoRA `q35_4b_main500k`, adapter sha256
`507d1c29...db078`) through the public Decision Index harness once, on a ~10K-request stratified sample, on the L4.
The harness's own sampler, scorer and index formula are used. Jev's numbers come from the published board. No Jev
or OpenRouter calls are made.

**Report-only (A13).** The results are never used to choose training data, families, weights or models. Builders never
see per-item results. Before any C training, C's data is decontaminated against every Index test item.

## What is where

| Path | Holds | In git |
|---|---|---|
| `bench/decision_index/od_engine.py` | the engine adapter (Index request -> our decision rows -> C1 readout) | yes |
| `bench/decision_index/di_tools.py` | sample, preflight, checks, overlap, score + report (counts and aggregates only) | yes |
| `bench/decision_index/test_od_engine.py` | CPU tests on synthetic questions (fake model) | yes |
| `bench/decision_index/check_oracle.py` | oracle mapping check over the whole sample (aggregates only) | yes |
| `bench/decision_index/*.json`, `progress.log` | manifests, checks and reports (counts, hashes, scores only) | yes |
| `bench/external_quarantine/decision_index/` | harness clone, rebuilt suite, samples, per-item results (`.gitignore` = `*`) | no |

## Harness

- Repository `github.com/flaviusburca/decision-index`, pinned at commit `52a698928a9ae5bdf16b75687c903871db29c6e5`
  (21 Sep 2026, "Headline index is the plain area mean, matching the leaderboard"). Its 21 unit tests pass.
- Suite: 132,422 requests, 37 benchmarks, 19 in the index (panel `core25-observed-protocol-v1`). This is the **v0.1
  board** (`index-v0.1.json` in the HF space `multimodalart/jev-decision-index`). The space's current board is v0.2.1
  (43 benchmarks, a different suite and harness). So our number compares with Jev's **v0.1** entry: index 59.51.
- Every question in the suite is a single-select `choice` with 2 to 255 options and a probability per option. The
  harness has no free-text, ranking or multi-select request type. Ranking (ToolRet, BRIGHT), multi-select (SATA,
  BFCL, ACOS) and forecasting are already split into per-candidate yes/no or choice questions. The harness then scores
  them as nDCG, case-exact or Brier. So **no request type is unsupported by our readout**. Only capacity limits
  (prompt > 16,384 tokens) can make a request `unsupported`, and the harness counts that as wrong.
- Engine interface: `Engine.__call__(state, questions) -> (response, raw)`. The response must give a probability for
  every option (sum 1 within 0.01) and a chosen key. `Unsupported` = declared capacity limit, scored as wrong.
- Index: each benchmark is scored with its native index metric (subject-, song-, user- or perturbation-macro accuracy,
  conservative macro-F1, nDCG@10, realized quality). The five areas are equal-weight means of their benchmarks, and
  `Decision Index = 100 x mean of the 5 area raws`. Unanswered requests count as zero.

## Suite: rebuilt from pinned public sources

The suite's Hub dataset (`multimodalart/decision-index-suite`) returns 404, so the suite was rebuilt with the harness's
own `suite rebuild` (pinned git commits, Hub revisions and sha256-checked URLs). That needed three local fixes (no
harness code was changed):

1. **Path fix.** The harness writes Hub and HTTP sources under `work/raw/`, but its builders read
   `work/artifacts/benchmark-suite/raw/`. Fixed by moving the files and adding a symlink. No code was changed.
2. **BANKING77.** The pinned `PolyAI/banking77` revision only holds a loading script. Its own source URLs (PolyAI
   GitHub `test.csv`, `categories.json`) were downloaded into place.
3. **Habermas Machine.** The data file is not in the pinned git repo; it was fetched from the URL in that repo's
   README, then benchmark 50 was normalized and the suite frozen (`rebuild_finish.sh`).

**HLE (catalog 45, display-only, 513 requests) is missing.** `cais/hle` is gated, and this HF account has not accepted
its terms (HTTP 403). HLE does not enter the index.

**Rebuild check** (`verify_rebuild.json`, `di_tools.py verify-rebuild`): **36 of 37 benchmarks are identical** to the
lab's frozen suite (`hub/manifest.json`). Each has the same normalized-source sha256, the same selected group ids and
the same request and field counts. HLE is the only one missing. The rebuilt file has 131,909 requests
(= 132,422 - 513 HLE), 117,251 cases and 774,689 fields. Its sha256 is `3eb7aa1e...` (uncompressed), so it is not the
pinned `288d3720...`, because HLE is absent.

To make it byte-identical (optional, ~5 min, before the L4 run only): accept the terms at
`huggingface.co/datasets/cais/hle` (auto-approved), then run
`bench/external_quarantine/decision_index/venv/bin/python -m decision_index suite rebuild --work work --only 45` in
the quarantine dir, then `di_tools.py verify-rebuild` and `di_tools.py sample` again. Adding HLE changes the sample (the
sampler rotates over the benchmarks present), so the sample sha256 below would change.

## Sample (harness sampler, fixed seed)

`di_tools.py sample --n 10000` calls the harness CLI `python -m decision_index suite sample --dir <rebuilt suite>
--n 10000 --seed 20260919`. The seed is the harness default (= `FREEZE_SEED`). The sampler hash-orders each benchmark's
case groups by `sha256("20260919:<catalog id>:<group id>")` and takes one group per benchmark per round until 10,000
requests. Groups stay whole, and the 442 excluded questions are skipped.

| | value |
|---|---|
| seed | 20260919 |
| requests / case groups / questions | **10,001** / 7,841 / 82,939 |
| benchmarks | 36 (all 19 index benchmarks; HLE absent, see above) |
| sample sha256 (uncompressed) | `70386e7bef9fa1d4fc8e7f056a9aa4b5d84ef08162a27d091d42c7de2cb6c362` |
| sample sha256 (`sample10k.jsonl.gz`) | `8b4999de8ef6c29ac05df498264941a5ec5afe948ba8e9bf3faa95ba663fb6db` |
| rebuilt suite sha256 (uncompressed) | `3eb7aa1eabd0a3de999008e9a3922068a1fb7499024175020acbf83b326e1fca` |
| per benchmark | `sample_manifest_sample10k.json` |

Per-benchmark sample: 230 requests per benchmark, except RouterBench 462 (two tracks per case), BPoMP 1,273 (linked
perturbation groups), GSM8K 460 (two tracks), ACOS 885 (linked groups), Home appliance 160, ContractNLI 123,
GPQA 196, SimpleBench 10 (all of these), and 229 for catalog ids 39 and up.

How the 82,939 questions map to our readout (fixed rule, `od_engine.py`):

| our row | questions | share | reads |
|---|---:|---:|---|
| yes/no with a definitions card (yes/no keys + descriptions) | 67,016 | 80.8% | 1 |
| yes/no without card | 2,720 | 3.3% | 1 |
| choice, options = descriptions (positional keys A, B, ... / option_N) | 7,279 | 8.8% | 2 (given + reversed) |
| choice, named keys with definitions ("A. key: description") | 5,924 | 7.1% | 2 |
| **unsupported request type** | **0** | **0%** | - |

The yes/no questions come mostly from ACOS (51,414; display-only), ToolRet (7,360) and BRIGHT (7,359): they hold
per-candidate relevance, SATA multi-select and BFCL per-function questions. The harness itself turns these into
nDCG, case-exact and Brier scores. Total reads: **96,142**.

Capacity: the preflight (`preflight_sample10k.json`, real C1 tokenizer, both views) finds **2 of 10,001 requests**
over the shipped 16,384-token limit (`decoder_io.MAX_LEN`): one POP909-CL request (23,303 tokens) and one BRIGHT request
(32,359 tokens). Both are refused as `unsupported` and score as wrong. No request has more than 255 options (max 151).

## Checks done on the Mac (CPU)

| check | result |
|---|---|
| harness unit tests (`repo/tests`) | 21/21 pass |
| rebuild vs the lab's manifest | 36/37 benchmarks identical (sources sha256, groups, counts); HLE missing |
| **harness index math on Jev's published v0.1 values** (`check_index_math.json`) | 19 Jev per-benchmark raws -> harness `recompute` -> **59.51 / 46.26 / 44.79**, equal to the published Jev entry; 5 area raws within 0.0001 (rounding) |
| harness scorer + our rebuilt suite on a **published full v0.1 run** (`check_parity.json`; Kshetrajna/decision-index-results, reflex-27b, 132,422 rows) | rescored index **56.23 / 42.15 / 40.88 = published**; all 19 index benchmarks diff 0.0; 32/32 per-benchmark scores exact (4 are None in both, HLE not rescorable) |
| engine tests (`test_od_engine.py`, synthetic questions, fake model) | 6/6 pass: mapping rules, prompt shows definitions, Unsupported over the limit, harness `validate` passes, readout == `decoder_io.predict(tta_choice=True)` |
| readout equality on 93 real smoke rows (47 choice, 46 yes/no; fake model) | max abs diff vs `decoder_io.predict` = **0.0** |
| **end-to-end smoke**: harness `run` with `od_engine:ODEngine --option fake=true` on a 50-request harness sample (seed 20260919, all 36 benchmarks, 554 questions), then harness `score` | 50/50 `ok`, 0 unsupported, 0 errors, all 36 benchmarks scored, area coverage 1.0; index 30.09 (random 1-layer model, so this is noise; `report_smoke50.json`) |
| **oracle mapping check** (`check_oracle.py` -> `check_oracle_sample10k.json`, independent verifier, 3 Oct): the readout is replaced by a stub that finds the gold option's label in each RENDERED prompt view; the rest is the real engine + harness `validate` + harness `score` on all 10,001 sample requests | 96,108/96,108 views: the gold's label in the prompt = its position under the view's permutation (0 mismatches, 0 ambiguous); 9,999 ok + 2 unsupported; every benchmark scores its ceiling (1.0; ToolRet 0.6208 and BRIGHT 0.2535 = best nDCG@10 of the candidates; RouterBench 0.908 = mean best quality); oracle index 89.37 = the most this sample allows. Per-item oracle files deleted |
| verifier re-runs (3 Oct) | harness tests 21/21; engine tests 6/6; smoke50 fake run through harness `run` + `score`: 50/50 ok, index 30.09, probabilities identical to the first run (max diff 0); sampler re-drawn: same uncompressed sha256 `70386e7b...` (the .gz hash differs only by the gzip header time) |

Jev's per-item results are not published, only its aggregates. So "reproduce Jev" here means two checks: the harness's
index code reproduces Jev's published index from Jev's published per-benchmark values, and the harness scorer
reproduces a published full run exactly on our rebuilt suite.

## L4 run (od-l4b), exact commands

The VM must be free (no training or other reads). One run. A restart is allowed only after a crash: rerun the same
command, and the harness resumes from `results.jsonl` and retries only `error` rows.

### Mac: copy the code and the sample

```bash
cd ~/Documents/jev
VM=od-l4b; G="--zone us-east4-c --project system-one-509903"   # od-l4b = the us-east4-c clone (ejs-5, A12 ran there)
gcloud compute instances start $VM $G
gcloud compute ssh $VM $G --command 'mkdir -p ~/bench/decision_index ~/bench/external_quarantine/decision_index/{repo,sample,runs}; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader'
COPYFILE_DISABLE=1 tar -C bench/external_quarantine/decision_index/repo --exclude __pycache__ -czf /tmp/di_harness.tgz decision_index pyproject.toml LICENSE
gcloud compute scp $G /tmp/di_harness.tgz $VM:~/bench/external_quarantine/decision_index/
gcloud compute ssh $VM $G --command 'tar -C ~/bench/external_quarantine/decision_index/repo -xzf ~/bench/external_quarantine/decision_index/di_harness.tgz'
gcloud compute scp $G bench/decision_index/od_engine.py $VM:~/bench/decision_index/
gcloud compute scp $G bench/external_quarantine/decision_index/sample/sample10k.jsonl.gz $VM:~/bench/external_quarantine/decision_index/sample/
```

### VM: `gcloud compute ssh od-l4b $G`

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader   # must print nothing
sha256sum ~/lean/decoder_io.py ~/lean/models/q35_4b_main500k/adapter_model.safetensors \
          ~/bench/decision_index/od_engine.py ~/bench/external_quarantine/decision_index/sample/sample10k.jsonl.gz
#   expect 8ba8ff4f...  507d1c29...  f3fa1c63...  8b4999de...
export HF_HOME=$HOME/hf HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_XET=1
export PYTHONPATH=$HOME/bench/external_quarantine/decision_index/repo:$HOME/bench/decision_index
D=$HOME/bench/external_quarantine/decision_index
cd ~/bench/decision_index
nohup ~/od/bin/python -m decision_index run --engine od_engine:ODEngine \
    --rows $D/sample/sample10k.jsonl.gz --out $D/runs/c1_sample10k --compact \
    --option base=Qwen/Qwen3.5-4B --option revision=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a \
    --option adapter=$HOME/lean/models/q35_4b_main500k \
    --option adapter_sha256=507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078 \
    --option lean=$HOME/lean > $D/runs/c1_sample10k.log 2>&1 &
tail -f $D/runs/c1_sample10k.log | grep --line-buffered -E '"event": ?"(ready|complete|failed)"|Traceback|Error'   # runner lines are compact JSON
cat $D/runs/c1_sample10k/status.json     # progress: completed / counts / elapsed_seconds (written every 10 requests)
```

`--compact` keeps item text out of `results.jsonl`, which then holds ids, statuses, probabilities and timings only.
The `od_engine_stats` line at the end counts the harness's 2 warm-up calls too (requests = 10,003).

### Mac: fetch, stop the VM, score

```bash
gcloud compute scp --recurse $G $VM:~/bench/external_quarantine/decision_index/runs/c1_sample10k bench/external_quarantine/decision_index/runs/
gcloud compute scp $G $VM:~/bench/external_quarantine/decision_index/runs/c1_sample10k.log bench/external_quarantine/decision_index/runs/
gcloud compute instances stop $VM $G
P=bench/external_quarantine/decision_index/venv/bin/python
$P bench/decision_index/di_tools.py score --name sample10k --run bench/external_quarantine/decision_index/runs/c1_sample10k
#   -> bench/decision_index/report_sample10k.json: our index, areas and per-benchmark scores (harness) vs Jev v0.1 (published)
```

## Time estimate (L4)

Workload (preflight): 96,142 reads, **79.6 M prompt tokens** (about 92 M after padding to multiples of 256). The big
items: ACOS 19.2 M (51,414 short reads), ContractNLI 10.4 M, Home appliance 9.4 M, BRIGHT 8.8 M, ToolRet 5.5 M,
RouterBench 5.3 M and API-Bank 4.8 M (about 10.5 K tokens per question).

Measured C1 speed on the L4:
- ejs-5 at batch 1: about 4.5 K padded tokens/s (115 ms per 512-token pass).
- OHS-1+2 A5 read at batch 16: about 2.4 K tokens/s (rough token count).

**Estimate: about 6 to 9 hours** (92 M / 4.5 K/s = 5.7 h, 79.6 M / 2.4 K/s = 9.2 h), plus about 1 minute to load.
Plan one overnight run. At on-demand g2-standard-8 prices (about $0.85/h, approximate) that is roughly $5-8 of VM
time; no API cost. The sample file is in the sampler's round-robin order, so the rate after the first ~30 min
(`status.json`: completed / elapsed_seconds) extrapolates fairly.

## Overlap disclosure (A13, counts only)

`di_tools.py overlap` (`overlap_sample10k.json`) compares the sample with C1's training file
`v14_parts/golden_train.jsonl` (501,732 rows). It uses 12-grams of lowercase words, as the OHS-3 check did. A 12-gram
found in more than 20 sample requests counts as template text and is ignored.

**285 of 10,001 sample requests** share at least one 12-gram with 1,019 training rows.

| benchmark | in index | overlapping / sample | main training sources |
|---|---|---|---|
| MuSR | no | **160 / 230 (69.6%)** | musr_object_placements, musr_murder_mysteries, musr_team_allocation (C1 trained on 298 MuSR rows; MuSR has one split) |
| BRIGHT | yes | 57 / 230 (24.8%) | gd_prm800k_steps, judge_prm800k, gd_helpsteer3_pref, gd_totto_claims (shared documents) |
| ToolRet | yes | 23 / 230 (10.0%) | gd_prm800k_steps, gd_totto_claims, hard_nli_b |
| RouterBench | yes | 10 / 462 (2.2%) | arc (ARC train rows inside RouterBench prompts), gd_medqa_yn |
| BFCL | yes | 8 / 230 (3.5%) | hard_evidence_claims_b |
| MMLU | yes | 6 / 230 (2.6%) | gd_medqa_yn |
| ContractNLI | yes | 3 / 123 (2.4%) | proc_multihop, hard_contracts |
| CRUXEval | yes | 1 / 229 | gd_totto_claims, gd_prm800k_steps |
| SATA 7, ANLI 4, API-Bank 2, NLI4CT 2, BANKING77 1, SGD 1 | no | small | various |

Training sources named after Index datasets, with row counts in C1's training file: banking77 2,300, clinc150 2,651,
arc 414, gd_winogrande 4,734, musr_* 298. Of these, only MuSR shows real item overlap. BANKING77 1/230, CLINC150 0,
ARC 0 and WinoGrande 0 sampled requests overlap: those rows come from the train splits, and the Index uses test splits.
Note for A13: BANKING77 and CLINC150 are C1 **training** sources (train split), not only dev sources. The MuSR,
BRIGHT and ToolRet scores of C1 should be reported with this overlap.
