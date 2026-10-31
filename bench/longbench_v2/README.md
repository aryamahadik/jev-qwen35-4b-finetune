# LongBench v2 kit: longjev's "Jev keeps 8K tokens" protocol, with our model as the scorer and the reader

The protocol, item sets, comparison rule and disclosures are in `PREREG_longbench_v2.md`.

Rules:
- Never print item text or gold.
- Each model runs once.
- Real runs only after the owner's OK.

## Files

| File | What it does |
|---|---|
| `lb_lib.py` | The protocol. Verbatim copies of longjev's chunker, question rendering, round-robin keep, gap rendering, effective budget, split, Wilson and McNemar. Item sets, row builders, an index-keyed A5 readout and Newcombe. |
| `convert.py` | Pinned `data.json` → `kit/lb_items.jsonl` (no gold), `lb_gold.jsonl`, `lb_index.jsonl` (no text) and `lb_meta.json` (counts, sha256). Checks the 42 / 163 / 96 set sizes. |
| `lb_select.py` | longjev's steps with our model as the scorer: prepare, keep, assemble (too-long retry). `--plan` gives CPU counts and the compute estimate. Not named `select.py`, which would shadow Python's stdlib `select` module. |
| `run_lb.py` | L4 runner, one model per call. Has a manifest with every sha256, a ledger that allows only one run per adapter, and timing. Never opens gold. `--fake-model` for CPU tests. |
| `cascade_lb.py` | 2B → 4B cascade. Uses ohs3_lib's rule, chunk routing offline from both runs, live final reads. Config: `cascade_lb.template.json`. |
| `score_lb.py` | Primary: test_proxy against Jev 86/163, unpaired Newcombe. Secondary sets, breakdowns and diagnostics. `--jev-items` gives a paired bootstrap if per-item Jev answers ever appear. |
| `overlap_counts.py` | Counts-only 13-gram check of our train/dev jsonl against LongBench questions, options and sampled contexts. |
| `make_synthetic.py`, `tests/test_lb.py` | Synthetic data and the tests: parity with longjev's own code, readout = `ohs3_lib.a5_read`, cascade rule = ohs3_lib's, end to end, guards. |

## Commands

### Mac: data and checks (done 2 Oct; CPU only)

```bash
cd ~/Documents/jev; PY=opendecide-data/.venv/bin/python
# data (pinned revision) is in bench/external_quarantine/longbench_v2/hf_2b48e494/data.json
$PY bench/longbench_v2/convert.py --data bench/external_quarantine/longbench_v2/hf_2b48e494/data.json \
    --tokenizer backups/modal_models/q35_4b_main500k
$PY bench/longbench_v2/lb_select.py --plan --items bench/external_quarantine/longbench_v2/kit/lb_items.jsonl \
    --model backups/modal_models/q35_4b_main500k --base Qwen/Qwen3.5-4B
$PY -m pytest -q bench/longbench_v2/tests            # 13 tests, ~1 min, synthetic items only
```

### Mac: copy the kit and the items (NOT the gold) to the VM, only when the L4 is free

```bash
P=system-one-509903; Z=us-central1-a; Q=bench/external_quarantine/longbench_v2/kit
gcloud compute ssh od-l4 --zone $Z --project $P --command 'mkdir -p ~/bench/external_quarantine/longbench_v2/kit'
gcloud compute scp --recurse bench/longbench_v2 od-l4:~/bench/ --zone $Z --project $P
gcloud compute scp $Q/lb_items.jsonl $Q/lb_meta.json $Q/lb_index.jsonl \
    od-l4:~/bench/external_quarantine/longbench_v2/kit/ --zone $Z --project $P
```

### VM: optional timing smoke on SYNTHETIC items with the real model

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv   # must list nothing
export HF_HOME=$HOME/hf HF_HUB_OFFLINE=1; cd ~/bench/longbench_v2
~/od/bin/python make_synthetic.py --out ~/lb_syn/data.json --n 110 --n-long 6
~/od/bin/python convert.py --data ~/lb_syn/data.json --tokenizer ~/lean/models/q35_4b_main500k --out ~/lb_syn/kit --synthetic
~/od/bin/python run_lb.py --model ~/lean/models/q35_4b_main500k --base Qwen/Qwen3.5-4B \
    --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --choice-readout 2view \
    --items ~/lb_syn/kit/lb_items.jsonl --out ~/lb_syn/run_4b --limit 3
```

### VM: the real run (owner's OK). The 4B takes about 2.5 h; the 2B about 0.8 h.

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv   # must list nothing
export HF_HOME=$HOME/hf HF_HUB_OFFLINE=1; cd ~/bench/longbench_v2
mkdir -p ~/bench/longbench_v2/runs
~/od/bin/python run_lb.py --model ~/lean/models/q35_4b_main500k --base Qwen/Qwen3.5-4B \
    --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --choice-readout 2view \
    --items ~/bench/external_quarantine/longbench_v2/kit/lb_items.jsonl 2>&1 | tee ~/bench/longbench_v2/runs/lb2_q35_4b_main500k.log
# later, the shipped 2B (fill its dir, revision and A5 readout from its ship record; the current arm-I candidate is
# ~/lean/models/q35_2b_armI_1600 on Qwen/Qwen3.5-2B @ 15852e8c16360a2fea060d615a32b45270f8a8fc):
# ~/od/bin/python run_lb.py --model ~/lean/models/<2b> --base Qwen/Qwen3.5-2B --revision <commit> --choice-readout <2view|single> --items ...
# then the cascade, once both are complete:
# ~/od/bin/python cascade_lb.py --config cascade_lb.json --items ~/bench/external_quarantine/longbench_v2/kit/lb_items.jsonl
```

If the VM stops mid-run, add `--resume` to the same command. It continues the same run and re-reads nothing that is already finished.

### Mac: fetch and score (gold never leaves the Mac)

```bash
gcloud compute scp --recurse od-l4:~/bench/longbench_v2/runs/lb2_q35_4b_main500k bench/longbench_v2/runs/ --zone $Z --project $P
$PY bench/longbench_v2/score_lb.py --run bench/longbench_v2/runs/lb2_q35_4b_main500k \
    --overlap bench/external_quarantine/longbench_v2/overlap_counts_c1_train.json
```

The cascade config (`cascade_lb.json`, from `cascade_lb.template.json`) must name the dev-only fit log and its sha256;
`cascade_lb.py` refuses a config whose tau, w_big, route_on or T differ from that log. If longjev's per-item file
(`results/raw/items.jsonl`) ever appears, `score_lb.py --jev-items <file>` recomputes Jev's headline from it
(`primary.jev_file_headline`, must equal 86/163) and adds a paired comparison.
