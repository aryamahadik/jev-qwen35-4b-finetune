# serving/: S1 serving freeze for C2 (lane P7)

Tools for serving a C2 candidate on the same path as C1 (od-l4b, SGLang 0.5.20 S1, `reads/fast_read.py`). CPU tests only so far;
no tool here stops, restarts, flushes or signals a process it did not start. Tests: `cd lean && HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/serving/tests` (100 + 34 snap-monitor).

| file | what |
|---|---|
| `S1_CONFIG_PIN.json` | pinned S1 config of the production server (read-only GET /server_info, 17 Oct 17:29 UTC): `config_sha256` 2f9fa84a, `path_sha256` 9a068791 (model path masked), `server_info_stable_sha256` cb1b6901; argv, env, versions, merge manifest, code shas VM vs Mac |
| `s1_pin.py` | `collect` (read-only VM), `pin`, `verify --mode same|path [--info F | --vm]` (exit 1 on drift) |
| `merge_parity.py` | `merge` (non-C1 adapter -> BF16, all export checks), `serve` / `stop` (own pidfile only), `parity` (bar: argmax >= 99.5% and |d p(label)| <= 0.02 on >= 99%, n >= 2000, seeded, vs the HF adapter's `od_gcp.py predict --tta-choice`; refuses unless the server's `model_path/merge_manifest.json` names this adapter's sha256; records model path, manifest sha and config sha; `--min-n` under 2000 needs `--allow-small-n` and is never `PASS_gate`) |
| `d9_latency.py` | `measure` (refuses unless the served model's merge manifest names `--adapter`'s sha256; c = 1, speed/workloads/S.jsonl, sha-pinned, seeded, warm-up discarded) and `combine` (C1 record must be C1's pinned adapter; the two records must differ in served model path, manifest sha and config sha) -> the record `gate_c2.latency_rule` reads |
| `prompt_sha_check.py` | train / gate / S1-client rendered-prompt and token-id identity; record `c2_build/logs/p7_prompt_sha_check.json` |
| `vm_collect.py` | runs on the VM, read-only (used by `s1_pin.py collect`) |

## Window procedure (orchestrator; production is the L4's only GPU tenant: 21 of 24 GB)
1. Stop production with its own script (`speed/opt_c1_round2_20261017/vmcode/prod_stop.sh <label>`; it refuses while a C2 read job runs).
2. `merge_parity.py merge --adapter <cand dir> --expect-sha <sha of CANDIDATE_C2.json> --out ~/models/<cand>_merged` (cpu is safe at any time, cuda only with no server alive).
3. Reference (HF adapter, one GPU job): `od_gcp.py predict --name <cand> --splits <split> --tta-choice`.
4. Boot C1 merged on the same flags (`prod_start.sh`), then `d9_latency.py measure --label C1 --adapter <C1 adapter> --flush --i-own-the-window --out c1.json`; stop; `merge_parity.py serve --model ... --expect-sha ...` (checks the path hash against the pin), `parity ...`, `d9_latency.py measure --label C2 --adapter <cand dir> --flush --out cand.json`, `merge_parity.py stop`; restart production; `s1_pin.py verify --mode same --vm` must say ok.
5. `d9_latency.py combine --c1 c1.json --cand cand.json --out c2_build/logs/latency_c2.json`.
Copy `serving/` and `speed/workloads/` to the VM (e.g. `~/c2serving`, `P7_WORKLOAD_DIR`) and run with `~/od/bin/python -B`, `OD_LEAN=~/lean`; imports were checked on the VM's python.

## Notes
* `merge` on a real non-C1 adapter has not run (CPU tests cover the guard and the call into `export_local` with `adapter_sha=None`; layout/style must equal C1's, no other C1 pin). `export_local` writes the constant `"model": "q35_4b_main500k"` into every manifest; the adapter sha, not that field, is the identity, and the merge record notes it as `manifest_model_field`.
* `prompt_sha_check.py` used the C1 adapter folder in place of the C2 one: re-run it with `--adapter <C2 dir>` when the candidate exists.

## Open points
* D9 "single view": `--views 1` is the default (C_TRAIN_RECIPE D9); `--views 2` is the dev-gate readout. The record names the choice; rule it before the real run.
* The parity reference needs an HF-adapter read of the candidate on a non-dev, non-sealed split (the G-block is the natural one); this lane built no new dev file.
