# reads/: fast C1 reads on the free L4 (A49 f) and the C2 replay inputs

Written 16 Oct 2026 (UTC) by the Sonnet ops agent. Binding: `PREREG_FINAL.md` A35 (SGLang S1), A18.2 (readout), A46
(replay screen), A49 (f) (faster C1 reads). C1 output here is a routing / selection signal only, never a label or a target.

| file | what |
|---|---|
| `fast_read.py` | `serve`, `stop`, `predict`, `label`, `parity` on the VM: SGLang S1 + the A18.2 readout; same files as `od_gcp.py predict` / `od_gcp.py label` |
| `export_merged.py` | writes C1 merged in BF16 (no Modal): `hosting/export_c1_merged.export_local` with a `modal` stub |
| `replay_c2.py` | the C2 replay inputs: `draw`, `old-slice`, `verify`, `reuse-r1-labels`, `second-pass` (runs `c_build/replay_sample.py` unchanged, in-process) |
| `PARITY_A49F.json` (+ `_fast_preds.jsonl`) | the A49 (f) parity test, 2,000 seeded G-block rows |
| `replay_work/` | the sampler's own outputs (log, `replay_draw.json`, deny query copy, reuse labels) |

## 1. The fast path (what it is)

Arm S1 of A35 without Modal: SGLang 0.5.20, merged BF16 C1 (adapter sha256 `507d1c29...`), fp32 LM head, hybrid prefix
cache (`extra_buffer`), triton linear-attention backends, no speculation. `fast_read.serve` builds the command with
`hosting/sglang_host.server_cmd` and checks the resolved args with `check_server_args` (0 problems, 0 warnings on the VM).
Reads use `hosting/fastcore/readout.py` (= `decoder_io` byte for byte: prompt text, candidate ids, 2view probability
average for choice rows, single read for yes/no, T = 1.0) and `sglang_host.parse_generate_response` (candidate
log-probabilities of one prefill-only pass, logsumexp per letter). Output order is input order; no sampling.

Differences from the H100 S1 run, all outside the parity-critical argument list: attention backend `triton` (flashinfer needs
a CUDA 13 `nvcc` JIT; FA3 is Hopper only), `--mem-fraction-static 0.8`, `--max-running-requests 32`,
`--max-mamba-cache-size 128` (SGLang caps running requests at 25: 5 state slots per request), L4 instead of H100.
The parity test below is what binds.

### One-time VM setup (done on od-l4b, 16 Oct; all inside `~`)
```
curl -LsSf https://astral.sh/uv/install.sh | sh ; uv venv ~/sgl --python 3.12 ; . ~/sgl/bin/activate ; uv pip install sglang==0.5.20
sudo apt-get install -y g++-12                       # SGLang JIT kernels (silu_and_mul) need a host C++ compiler
mkdir -p ~/bin ; ln -sf /usr/bin/g++-12 ~/bin/c++ ; ln -sf /usr/bin/g++-12 ~/bin/g++
N=~/sgl/lib/python3.12/site-packages/nvidia/cu13 ; ln -sfn lib $N/lib64 ; ln -sf libcudart.so.13 $N/lib/libcudart.so
scp hosting/ (tar, no tests) -> ~/lean/hosting ; scp fast_read.py export_merged.py -> ~/reads
# 3 pinned base files the VM snapshot lacks (preprocessor_config.json, video_preprocessor_config.json, LICENSE) come from the
# Mac HF cache of the same revision -> ~/jobs/base_extra ; export_merged checks all 12 base pins (sha256 / git blob sha1)
cd ~/reads ; HF_HUB_OFFLINE=1 ~/od/bin/python -B export_merged.py --lean ~/lean --out ~/models/q35_4b_main500k_merged --extra ~/jobs/base_extra
```
The export passed every `export_c1_merged` check (in-memory merge == written, fresh second merge == written, LoRA formula
check, base copies, config) in 107 s on the L4; merged on `cuda`, as `od_gcp.py predict` merges.

### Start / stop the server (VM; one GPU job at a time, the L4 is shared with nothing else)
```
~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton"   # about 3 min
~/od/bin/python -B ~/reads/fast_read.py stop
```
`start_server.sh` (copy of the scratch script; kept on the VM) exports `CUDA_HOME=~/sgl/.../nvidia/cu13`, `PATH` with `~/bin`
and `~/sgl/bin`, `TORCH_CUDA_ARCH_LIST=8.9`, then runs `fast_read.py serve "$@"`. Do not run `pkill -f` patterns that appear in
your own ssh command line (it kills the ssh shell).

## 2. Parity (A49 f) and throughput

Test: 2,000 rows of `data/gblock_a42d_c1read.jsonl` (sha256 `937ef0e0...`), seed 20261016 (`random.Random(seed).sample`,
fixed before the run, one run, no re-draw), against `preds_gblock_a42d_c1read/q35_4b_main500k.jsonl` (sha256 `7f52b536...`,
the HF path, `--tta-choice`). Choice rows are read in both option orders and averaged, exactly as the reference. The G-block
rows carry no gold, so "p(label)" is p of the reference's argmax answer; the stricter max-over-options difference is also
reported. Result: `PARITY_A49F.json`.

| measure | bar | result |
|---|---|---|
| argmax agreement, all 2,000 | >= 99.5% | **99.90%** (2 of 2,000; both yes/no near-ties, reference margins 0.008 and 0.003) |
| rows with abs diff p(label) <= 0.02 | >= 99% | **99.95%** (max 0.071; p99 0.0104) |
| max-over-options abs diff <= 0.02 | (stricter) | 99.95% |
| choice rows (991): argmax / abs diff | | 100.00% / max 0.018 |
| yes/no rows (1,009): argmax / abs diff | | 99.80% / max 0.071 |

PASS. Throughput on the L4: **13.1 reads/s = 8.7 rows/s** (2,991 reads, 1.72 M prompt tokens, 32% served from the prefix
cache, 229 s) against 3.75 reads/s = 2.5 rows/s for `od_gcp.py predict` on the same VM: about 3.5 times faster. A full
G-block read (18,773 rows) is about 36 min instead of 1.6-2.1 h.

## 3. Crowd reads (`c2_select.py tasks --write-shards` -> read -> labels)

`c2_select.py` is the CPU-side owner of the plan; it refuses to write before the OHS-4 freeze (A38). From `c2_build`:
```
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
$PY -B c2_select.py tasks [--fam T28 ...] --write-shards      # crowd_c2/crowd_tasks_c2.json + data/c2_crowd_shards/<FAM>/shard_NNN.jsonl
```
Crowd rows are read with ONE view (given option order, no TTA, A37 e): `--views 1`. Push the shards, read, pull the labels:
```
P=system-one-509903 ; Z=us-east4-c ; V=od-l4b
tar czf /tmp/x.tgz -C data c2_crowd_shards ; gcloud compute scp --tunnel-through-iap --zone $Z --project $P /tmp/x.tgz $V:~/jobs/
gcloud compute ssh $V ... --command 'cd ~/lean/data && tar xzf ~/jobs/x.tgz'                 # sha256 of shards.json checked after
# server up (section 1); one shard per call is resumable (a finished shard is skipped):
for FAM in T28 T35 ... ; do for i in $(seq 0 $((N-1))); do
  ~/od/bin/python -B ~/reads/fast_read.py label --shards-dir data/c2_crowd_shards/$FAM --shard $i --views 1 ; done ; done
# -> data/c2_crowd_shards/<FAM>/labels_q35_4b_main500k/shard_NNN.{jsonl,meta.json}; settings tta_choice false, as c2_select checks
tar czf - -C ~/lean/data/c2_crowd_shards . --include='labels_*' | ...   # pull back to the same path on the Mac, then select
$PY -B c2_select.py select [--fam ...]
```
Throughput for one view is about 1.5 times the 2view rate (about 12-13 rows/s on typical rows); `c2_select.READ_ROWS_PER_H`
assumed 124,000 rows/h (H100); the L4 does about 40,000 rows/h with one view. Trap flags (G-block routing, spec 5.1) use the
2view read: `fast_read.py predict --splits gblock_a42d_c1read` (default `--views 2`), then pull
`preds_gblock_a42d_c1read/q35_4b_main500k.jsonl` as `route_a42d.py classify` expects.

## 4. G-proxy and pilot-evaluation reads (C1 side)

The pilot A/B (`pilot_ab/l4_reads.sh read-c1`) reads C1 once on the 9 gate dev splits, the G-proxy (`pab_gproxy`) and each own
dev, with the A18.2 readout (`--tta-choice`, tag `_pab`). With the fast path, replace the `od_gcp.py predict` line by
```
~/od/bin/python -B ~/reads/fast_read.py predict --name q35_4b_main500k --splits pab_own_$FAM,pab_gproxy,dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev --tag _pab
```
(`--views 2` is the default; output `preds_<split>/q35_4b_main500k_pab.jsonl` + `.meta.json` in the same format; `meta.engine`
is `sglang`). **The pilot adapters themselves still read with `od_gcp.py predict`**: the fast path serves C1 only (the merge
export is pinned to C1's adapter sha). To serve a pilot or a snapshot the same way, `export_merged.py` needs its adapter pin
parameterised; until then use the HF path for them. The pairing in `verdict.py` is by item, so a C1 read on the fast path and a
pilot read on the HF path compare as the A49 (f) parity test allows (99.9% argmax, 99.95% within 0.02).

## 5. Replay inputs for `mix_c2.py` (spec 5.4)

All steps deterministic and seeded (C2 seed 20261013 = `c2io.SEED`). `PY` as above; from `c2_build/reads`:
```
nice -n 10 $PY -B replay_c2.py draw              # about 10 min: sampler --write-shards --r1 75000 --r2 150000 --margin 0.10
$PY -B replay_c2.py old-slice                    # round-1 old slice -> data/c_old_slice_shards, byte-checked against c_build/replay_r1_write.json
$PY -B replay_c2.py verify                       # the shards == the A46 screen's draw (replay_screen/pool/draw_75000.json)
$PY -B replay_c2.py reuse-r1-labels              # round-1 HF labels of byte-identical read inputs -> replay_work/reuse_labels.jsonl
# VM: push data/c2_replay_shards + reuse_labels.jsonl, then (server up)
~/od/bin/python -B ~/reads/fast_read.py label --shards-dir data/c2_replay_shards --shard $i --reuse ~/jobs/reuse_labels.jsonl   # i = 0..16
# pull data/c2_replay_shards/labels_q35_4b_main500k/ back to the Mac, then:
$PY -B replay_c2.py second-pass                  # p_g rule (A16) + C1 anchor flags -> c2_build/replay_c2_pg_anchor.json
```
The deny inputs `replay_screen/REPLAY_DENY_A46.json`, `REPLAY_UNSCREENED_A46.json` and `logs/decontam_counts/pool_drops_r1.json` are
mixer inputs (`mix_c2.py --decontam-drops ...`), not sampler inputs; the sampler has no row-id input. The shards are the sampler's raw
draw, and the mixer needs a label for every shard row, so rows of units the mixer will drop are read too.

`screen.py coverage` on the shards lists 4,094 human-label rows outside the screened population; every one of them sits in a relation
unit that holds a `pool_drops_r1.json` id (the mixer drops those whole units), so no row that can train is unscreened (0 others; the
14 `REPLAY_UNSCREENED_A46` ids and the 3,830 `REPLAY_DENY_A46` ids that are in the shards leave through `--decontam-drops`).

Read status (16 Oct): started 00:42 UTC on od-l4b, `~/jobs/label_driver.sh` (detached; restarts the server and retries a shard up
to 3 times; log `~/jobs/label_driver.log`, ends with `DRIVER_DONE`). Replay rows are heavier than G-block rows (less prefix sharing):
shard 0 took 929 s (3,643 rows read + 1,215 reused; 7.4 reads/s), so 17 shards take about 4.3 h, ETA about 05:00 UTC. Shard 0 was
validated end to end (`shard_done`, settings identical to the HF path's, reused labels bit-equal to the round-1 file, all rows
normalised). When it is done: `bash c2_build/reads/finish_replay.sh` (pulls the labels, checks every shard, runs `second-pass`),
then stop the VM (`zed_orch/gcp_run.sh od-l4b` with `ACTION=stop`) if nothing else needs it. Other agents' CPU jobs share the VM's 8 vCPUs;
the read is GPU-bound (the L4 is power-capped at 72 W, SM clock about 1.07 GHz), so they do not slow it much.

If the final new-row count is below the draw size, the final replay is a prefix subset of this draw (`mix_c2.trim_replay`), so no
re-read is needed; a LARGER draw would need a new `draw` and a new read of the difference only (`label` skips finished shards).
