# GCP runbook (od-l4, od-l4b): C1 reads and extra CPU for the C2 build

Written 15 Oct 2026 by the Sonnet ops agent. Project `system-one-509903`, account mahadikarya2. Verified on **od-l4b** only
(od-l4 was never up this session: L4 stockout in us-central1-a). Both VMs are the same recipe (HANDOFF 1087-1089).

**16 Oct 2026: a third VM, `od-cpu1` (CPU only, no GPU, us-east4-c), was added for CPU work; see section 7 at the end.
`gcp_run.sh od-cpu1 ...` works the same way as for od-l4b, and it never touches the GPU quota.**

## Facts that decide how to use them
- **One GPU quota for the whole project: `GPUS_ALL_REGIONS = 1`.** od-l4 and od-l4b both hold an L4, so **only one of the
  two can be RUNNING at a time.** A second `start` fails with a "global ... quota" error. Plan: use the VM that is up for
  the C1 read AND for CPU jobs together (8 vCPU, 31 GB RAM; the read uses about 1 core).
- **L4 stockouts are common** (both zones refused for ~4 min on 15 Oct; a VM can even go STAGING then back to
  TERMINATED). Do not stop a VM you may need again soon: restarting can take many tries. Use the retry loop below.
- No external IP: all ssh/scp goes through IAP (`--tunnel-through-iap`; the helper does it). Login user `aryamahadik`.
- Max run time 30 h (`maxRunDuration` 108000 s, then STOP). Disk 146 GB, 88 GB free on od-l4b. A stopped VM costs only its disk.
- Layout on a VM: `~/lean` (the old GPU tree, `~/od` venv with torch 2.14+cu130, transformers 5.17, peft 0.21), the base
  Qwen3.5-4B in `~/.cache/huggingface`, the C1 adapter `~/lean/models/q35_4b_main500k` (sha256 starts `507d1c29`, checked on
  od-l4b), `~/cpu` = new CPU venv (Python 3.12.14, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, pyyaml, pytest, pyarrow
  26.0.0, same versions as the Mac `.venv`), `~/repo/opendecide-data/lean/...` = synced copy of the C2 code (same layout as
  the Mac, so `c2_kit.paths` finds its repo root), `~/jobs` = job scripts/logs.
- **G13 (`g13_c2.py`) cannot run on a VM.** Its targets are OHS-1/2/3/4, sealed_nd, LongBench v2, JevBench items and the
  sealed checkers, none of which may leave the Mac. Run G13 on the Mac only. G6 (`g6_at_size.py`, `g6_null_max.py`) and other
  in-memory family builds read only the family folders, so they run on the VM.
- od-l4b already held `~/lean/data/ohs.jsonl`, `ohs2.jsonl`, `ohs_relations.jsonl` from earlier bench runs. They were not
  put there by this agent and were not opened. Do not `ls`/`cat` `~/lean/data` casually; the synced tree under `~/repo` has
  0 paths containing "ohs" (checked after every sync).
- An old `~/autostop.sh` (stops the VM when the replay read ends) sits in `~` on od-l4b; it is not running. Nothing stops a
  VM automatically now. **Stop the VM yourself** once the preds are pulled (see 6).

## 1. Start / stop
```
P=system-one-509903
gcloud compute instances start od-l4  --zone us-central1-a --project $P     # or:
gcloud compute instances start od-l4b --zone us-east4-c   --project $P
gcloud compute instances stop  od-l4b --zone us-east4-c   --project $P     # od-l4: --zone us-central1-a
gcloud compute instances list --project $P --format='table(name,zone.basename(),status)'
```
Stockout (`ZONE_RESOURCE_POOL_EXHAUSTED`) or quota error: try the other VM, or loop (each try takes about 40 s):
```
for i in $(seq 1 40); do for v in od-l4:us-central1-a od-l4b:us-east4-c; do
  gcloud compute instances start ${v%%:*} --zone ${v##*:} --project $P >/dev/null 2>&1 && { echo up ${v%%:*}; break 2; }
done; sleep 15; done
```
sshd needs about 1 minute after RUNNING. Manual shell: `gcloud compute ssh od-l4b --zone us-east4-c --project $P --tunnel-through-iap`.

## 2. CPU jobs: `zed_orch/gcp_run.sh <vm> '<command>'`
Run from anywhere; the script starts the VM if needed, syncs, runs the command in `c2_build` on the VM with `$PY` = the CPU
venv's `python -B` (single-threaded BLAS by default; keep the command in single quotes so `$PY` is expanded on the VM),
then pulls every file the job wrote under `c2_build` (files newer than the job start) and the job log
(`zed_orch/logs/gcp_<JOB>.log`). Examples (from `c2_build`):
```
# foreground (the Mac shell waits); NEW output dir so nothing local is overwritten
JOB=t30_g6 zed_orch/gcp_run.sh od-l4b 'mkdir -p families/T30/pilot_vm && $PY zed_orch/g6_at_size.py T30 --n 6000 --dir pilot_vm'
# detached (survives a closed Mac): run several at once, one JOB name each, at most ~5 beside a running C1 read
BG=1 JOB=t28_g6 NOSYNC=1 zed_orch/gcp_run.sh od-l4b 'mkdir -p families/T28/pilot_vm && $PY zed_orch/g6_at_size.py T28 --n 6000 --dir pilot_vm'
ACTION=status JOB=t28_g6 zed_orch/gcp_run.sh od-l4b      # log tail and exit code (rc: 0 = done)
ACTION=pull   JOB=t28_g6 zed_orch/gcp_run.sh od-l4b      # fetch what it wrote
ACTION=sync zed_orch/gcp_run.sh od-l4b                    # sync only (about 30 s when little changed)
EXTRA_SYNC="gblock/route_a42d" ACTION=sync zed_orch/gcp_run.sh od-l4b   # add a c2_build folder that is skipped by default
ACTION=stop zed_orch/gcp_run.sh od-l4b                    # stop the VM
```
- A pulled file overwrites the Mac file of the same name, so always give VM runs a new `--dir`/output name and compare.
- What is synced: `c2_build` (without gblock, replay_screen, pilot_runs, t37b, transfer), `lean/c_build`, `lean/teach1`,
  `lean/c_src/common`, `PREREG_FINAL.md`. **Never synced** (rsync excludes, all case-insensitive where it matters):
  `*ohs*`/`*OHS*` (any case), `*jev*` (any case), `sealed_nd`, `sealed_brief`, `preread`, `external_quarantine`, `longbench_v2`,
  `decision_index`, `sealed_hashes*`, `.git`, `.venv`, `__pycache__`. After each sync the script runs
  `find ~/repo -ipath '*ohs*'` on the VM and aborts unless it prints 0.
- Manual equivalent: `rsync -az --delete <the excludes> -e <ssh wrapper> c2_build/ aryamahadik@...:~/repo/opendecide-data/lean/c2_build/`;
  the wrapper is generated by the script (`~/.cache/gcp_run/rsh_<vm>.sh`, the `gcloud compute ssh --dry-run` options).
- `g6_null_max.py` (A43): `$PY zed_orch/g6_null_max.py --family T06 --runner families/T06/run_pilot_i2.py --dir pilot_vm`
  (it uses multiprocessing; set `OMP_NUM_THREADS=1` is already the default; give it a quiet VM or use `BG=1`).

## 3. C1 reads on the GPU (od_gcp.py predict)
Code on the VM is the pinned one (od_gcp.py 9253209d, decoder_io.py 908c08d7, train_decoder.py c2c2d1d6 checked equal to the
Mac). Splits live in `~/lean/data/<split>.jsonl`; predictions land in `~/lean/preds_<split>/<name>.jsonl` plus `.meta.json`.
```
P=system-one-509903; Z=us-east4-c; V=od-l4b
# 1. push the split and its sha, check it on the VM (from lean/)
gcloud compute scp --tunnel-through-iap --zone $Z --project $P data/gblock_a42d_c1read.jsonl data/gblock_a42d_c1read.jsonl.sha256 $V:~/lean/data/
gcloud compute ssh $V --zone $Z --project $P --tunnel-through-iap --command 'cd ~/lean/data && sha256sum -c gblock_a42d_c1read.jsonl.sha256'
# 2. read, detached (the A18.2 readout; choice rows read twice with --tta-choice)
gcloud compute ssh $V --zone $Z --project $P --tunnel-through-iap --command 'cd ~/lean; (setsid nohup bash -c "HF_HUB_OFFLINE=1 ~/od/bin/python od_gcp.py predict --name q35_4b_main500k --base Qwen/Qwen3.5-4B --splits gblock_a42d_c1read --tta-choice; echo rc=\$?" > ~/jobs/c1read.log 2>&1 < /dev/null &)'
# 3. watch: the job prints only at the end ("gblock_a42d_c1read: N rows in Ts", "wrote preds_.../q35_4b_main500k.jsonl", rc=0)
gcloud compute ssh $V --zone $Z --project $P --tunnel-through-iap --command 'tail -c 300 ~/jobs/c1read.log; nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader'
# 4. pull (from lean/); route_a42d.py classify reads preds_gblock_a42d_c1read/
mkdir -p preds_gblock_a42d_c1read
gcloud compute scp --tunnel-through-iap --zone $Z --project $P "$V:~/lean/preds_gblock_a42d_c1read/q35_4b_main500k*" preds_gblock_a42d_c1read/
```
- `--name` must stay `q35_4b_main500k` (the adapter folder; layout `schema_branch_mark`, style `cygnet`, base revision
  851bf6e8... come from its train_meta; chat template sha a4aee8af... matched the stored C1 reads). Another split: same
  command, `--splits <name>`; a tag for a re-run: `--tag _x`. Always one GPU job at a time. A snapshot name may contain "/".
- No incremental output: the preds file is written when ALL splits finish. A killed job restarts from zero.
- A tiny proof run: `--splits gblock_smoke120` (60 choice + 60 yes/no rows, already on od-l4b) took 48 s after a 56 s load.

## 4. Measured (15 Oct 2026)
| item | result |
|---|---|
| C1 read, od-l4b L4, `--tta-choice`, 120 rows (60 choice = 120 reads, 60 yes/no = 60 reads) | 48 s = **2.5 rows/s = 3.75 reads/s**; model load + save about 56 s |
| Full G-block read (18,773 rows = 9,256 choice x2 + 9,517 yes/no = 28,029 reads) | started 21:32:05Z; expected about 2.1-2.3 h (done about 23:45Z) |
| T30 G6 at 6,000 rows, Mac, stored run (14 Oct, quiet Mac) | 158 s |
| T30 G6 at 6,000 rows, Mac rerun today (busy Mac, 45% CPU) | 483 s wall |
| T30 G6 at 6,000 rows, od-l4b via gcp_run.sh (1 thread, C1 read running alongside) | **167 s** compute; every number identical to the stored JSON |
| First sync over IAP (about 430 MB c2_build + 340 MB c_build) | about 2 min; later syncs about 30 s |
So one VM thread is about as fast as an unloaded Mac thread. The gain is parallelism: up to 5-6 single-thread CPU jobs on the
VM beside the C1 read, while the Mac stays free. A L4 read of 28K reads costs about 2 h of free credit.

## 5. Evidence files
`zed_orch/logs/gcp_check_T30_G6_vm.json` (VM) and `gcp_check_T30_G6_local_rerun.json` (Mac) equal `families/T30/pilot_i1/G6_AT_6000.json`
apart from the `seconds` field.

## 6. Finish
Pull results, then `ACTION=stop zed_orch/gcp_run.sh <vm>` (or the gcloud stop above). Check `pgrep -af od_gcp.py` and
`ls ~/jobs/*.rc` first: do not stop a VM with a running job or unpulled preds (a restart can hit a stockout).

## 7. od-cpu1: the CPU-only second VM (added 16 Oct 2026)
**Why:** od-l4b (8 vCPU) was overloaded (load 20-27) because it runs the L4 job and all the CPU jobs. od-cpu1 takes CPU jobs
(G6, family builds, pytest, mixing, replay screening) and leaves od-l4b to the GPU.

| item | value |
|---|---|
| name / zone | `od-cpu1` / `us-east4-c` (c3 is also offered in us-east4-a and -b) |
| machine | **c3-standard-8**: 8 vCPU (Intel Sapphire Rapids 8481C), 32 GB RAM, **no GPU** |
| why this type | fastest 8-vCPU type the quota allows: C3_CPUS (us-east4) is 11 and C4 has no quota; c2/n2 are older Cascade Lake |
| price (list, Cloud Billing catalog, us-east4) | running **$0.403/h** (8 x $0.03465 core + 32 GB x $0.00394) + disk $0.023/h = **about $0.426/h**; stopped **$0.023/h** (150 GB pd-balanced at $0.11/GB-month); 72 h run = about $30.7. od-l4b for comparison: $0.851/h. Paid from the GCP credit |
| boot disk | 150 GB pd-balanced, NVMe, made from the snapshot below (79 GB used, 67 GB free) |
| snapshot | **`od-l4b-boot-snap-20261016`** (us-east4, 65.7 GB stored = about $3.3/month; taken live from od-l4b, crash-consistent, 18:53 PDT 16 Oct = 01:53Z 17 Oct; od-cpu1 created 19:03 PDT). **Do not delete** (it recreates od-cpu1 in any us-east4 zone) |
| network | default network and subnet (10.150.0.3), **no external IP and no Cloud NAT**: reachable only through IAP ssh, and the VM itself cannot reach the internet (no pip, no HF download; jobs run offline from the synced tree) |
| run limit | `maxRunDuration` 72 h, then STOP (not DELETE); the clock restarts at every start |
| service account | 101184695888-compute@developer.gserviceaccount.com, the same 7 scopes as od-l4b; shielded VM (vTPM + integrity monitoring), secure boot off |
| quota | `CPUS_ALL_REGIONS` 16 = od-l4b 8 + od-cpu1 8, **so there is no room for another 8-vCPU VM**; the GPU quota is untouched |
| login | user `aryamahadik` (same keys as od-l4b came with the snapshot) |

**Note:** od-l4b itself currently HAS an external IP (35.221.17.174, ephemeral), unlike what sections above say; od-cpu1 has none.

### What is on od-cpu1 (verified 16 Oct)
Ubuntu 22.04, same image and software as od-l4b at snapshot time:
- `~/cpu`: Python 3.12.14, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, pyarrow 26.0.0, pytest 9.1.1, pyyaml.
- `~/od`: torch 2.14.0+cu130, transformers 5.17.0, peft 0.21.0. **CPU use only**: `torch.cuda.is_available()` is False, a CPU matmul runs;
  torch prints one harmless `UserWarning: Can't initialize NVML` at import. Recipe: `HF_HUB_OFFLINE=1 PYTHONPATH=$HOME/lean ~/od/bin/python ...`.
  A CPU forward pass of a 4B/2B model is slow; do not plan model reads here (use od-l4b for those).
- `~/repo/opendecide-data/lean/{c2_build,c_build,c_src,teach1,decoder_io.py,train_decoder.py,PREREG_FINAL.md}`: the C2 code tree as of the
  snapshot; `gcp_run.sh` brings it up to date at every sync. `find ~/repo -ipath '*ohs*' | wc -l` is 0.
- `~/lean` (the old GPU tree, models, base Qwen3.5-2B/4B in `~/.cache/huggingface`) came with the snapshot. **It also carries
  17 paths that contain "ohs" (copies of what od-l4b already held from earlier bench runs; counted, never opened or listed).**
  CPU jobs never need `~/lean/data`; do not glob it. Remove them only if the owner asks.
- `~/jobs` holds 754 stale job files copied from od-l4b: always use a new `JOB=` name.
- GPU leftovers: the image's `nvidia-persistenced`, `nvidia-fabricmanager` and `nvidia-cdi-refresh` units failed at boot (no GPU); they were
  masked/disabled on od-cpu1 only. The kernel logs "NVRM: No NVIDIA GPU found" lines at boot (cosmetic). `google-startup-scripts` sits idle
  so `systemctl is-system-running` says `starting`; harmless (ssh and jobs work; a stop takes about 2.4 min).
- `nproc` prints 1 inside a gcp_run job because the job sets `OMP_NUM_THREADS=1`; the VM has 8 vCPUs (run up to 7-8 single-thread jobs with `BG=1`).
- `gcp_run.sh` syncs `c2_build` WITHOUT `transfer/`, `gblock/`, `replay_screen/`, `pilot_runs/`, `t37b/`. A test that needs one (e.g.
  `tests/test_pilot.py` needs `transfer/T21`) fails on the VM until you pass `EXTRA_SYNC="transfer"` (98 MB). Not a VM defect.

### Commands (all from `c2_build/`; the script does the zone mapping and needs no GPU)
```
P=system-one-509903
# run a CPU job, foreground (starts the VM if needed: up to START_TRIES=6 tries, 20 s apart, on a c3 stockout)
JOB=my_job zed_orch/gcp_run.sh od-cpu1 'mkdir -p families/T30/pilot_c1 && $PY zed_orch/g6_at_size.py T30 --n 6000 --dir pilot_c1'
# detached, several at once (one JOB name each; at most 8 single-thread jobs)
BG=1 JOB=a NOSYNC=1 zed_orch/gcp_run.sh od-cpu1 '$PY zed_orch/g6_at_size.py T28 --n 6000 --dir pilot_c1'
ACTION=status JOB=a zed_orch/gcp_run.sh od-cpu1      # log tail and rc (0 = done)
ACTION=pull   JOB=a zed_orch/gcp_run.sh od-cpu1      # fetch what it wrote
ACTION=sync        zed_orch/gcp_run.sh od-cpu1       # code sync only
ACTION=stop        zed_orch/gcp_run.sh od-cpu1       # stop (cost drops to $0.023/h)
# a torch/transformers job on CPU (the ~/od venv), by hand
gcloud compute ssh od-cpu1 --zone us-east4-c --project $P --tunnel-through-iap --command 'cd ~/lean && HF_HUB_OFFLINE=1 PYTHONPATH=$HOME/lean ~/od/bin/python -B -c "import torch,transformers,peft;print(torch.__version__)"'
gcloud compute instances list --project $P --format='table(name,zone.basename(),machineType.basename(),status)'
```
### Stockout (seen 16 Oct) and moving the VM
A stopped od-cpu1 can fail to start: `ZONE_RESOURCE_POOL_EXHAUSTED ... c3-standard-8 ... us-east4-c` (it did right after a stop; the 4th
try, 100 s later, worked). So **leave it running while you still have CPU jobs**, and stop it only when the queue is empty. The script retries by
itself; for longer use `START_TRIES=30`. If the zone stays empty, move it (UNTESTED; stopped VM only), then set `ZONE=` for gcp_run.sh:
```
gcloud compute instances move od-cpu1 --zone us-east4-c --destination-zone us-east4-a --project $P
ZONE=us-east4-a zed_orch/gcp_run.sh od-cpu1 '...'
```
or make a fresh one from the snapshot in another zone (this is the exact command that made od-cpu1; change `--zone`, and delete the old
`od-cpu1` first, since the disk name `od-cpu1` is per zone):
```
SCOPES=https://www.googleapis.com/auth/devstorage.read_write,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/pubsub,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append
gcloud compute instances create od-cpu1 --project $P --zone us-east4-c --machine-type=c3-standard-8 \
  --create-disk=name=od-cpu1,source-snapshot=od-l4b-boot-snap-20261016,size=150GB,type=pd-balanced,boot=yes,auto-delete=yes,device-name=persistent-disk-0,interface=NVME \
  --network-interface=network=default,subnet=default,no-address,nic-type=GVNIC \
  --maintenance-policy=TERMINATE --provisioning-model=STANDARD --max-run-duration=72h --instance-termination-action=STOP \
  --service-account=101184695888-compute@developer.gserviceaccount.com --scopes=$SCOPES \
  --shielded-vtpm --shielded-integrity-monitoring --no-shielded-secure-boot
# the snapshot itself was made live with:
gcloud compute disks snapshot od-l4b --zone us-east4-c --project $P --snapshot-names od-l4b-boot-snap-20261016 --storage-location us-east4
```
(After a fresh create, mask the GPU units again: `sudo systemctl disable --now nvidia-cdi-refresh.path nvidia-cdi-refresh.service nvidia-fabricmanager.service nvidia-persistenced.service`.)

### Measured on od-cpu1 (16 Oct 2026)
| item | result |
|---|---|
| snapshot of the running od-l4b disk | 8.5 min to READY (18:53:36 to 19:02:09 PDT), od-l4b untouched (no stop) |
| create from snapshot to ssh | about 2 min; first IAP ssh worked on the first try |
| `tests/test_pilot.py` (20 tests, `$PY`, 1 thread) | **20 passed, 17.3 s pytest, 24 s ssh run**, 1:49 end to end including sync of 98 MB `transfer/`; same file on the busy Mac: 122 s |
| numpy 1500x1500 matmul x5, 1 thread | 0.53 s |
| stop | 2 min 24 s; start right after a stop: c3 stockout, ok on try 4 |

