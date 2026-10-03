# ejs-5 kit: OpenDecide on the ejs-5/jev-benchmark (868 n8n commit decisions)

This kit runs third-party held-out tests, so these rules apply:
- Never read, print or log item text or gold labels.
- Every script prints counts and aggregates only.
- The benchmark files stay in `bench/external_quarantine/ejs5/`, which is git-ignored.
- Each system runs **once**, with the settings in `PREREG_ejs5.md`, after the owner's OK.

| File | What it does |
|---|---|
| `convert.py` | Turns the 4 task files into our row format and writes `external_quarantine/ejs5/ejs5_rows.jsonl` (+ `.meta.json`). It reads the author's question, criteria and level names from `run_public_bench.py` by AST. |
| `run_ejs5.py` | Reads all 868 rows once with one system (C1 4B or 2B on the L4; cascade composed offline) through `decoder_io`. It writes `runs/<name>/{preds.jsonl, manifest.json, timing.json}` and appends to `runs/ledger.jsonl`. It has a pre-flight check plus `--dry-run` and `--fake-model` CPU modes. |
| `score_ejs5.py` | Scores the way the author scored Jev, using the author's own `summarize()` taken by AST. It runs a paired bootstrap over commits vs Jev's published answers, the late subset (from 2026-06-01, 268 rows) and the descriptive GPT and Opus context. |
| `ejs5lib.py` | Shared code: AST readers, `decide` (our probabilities into the author's answer space), the cascade rule (a copy of `ohs3_lib`) and the bootstrap. |
| `tests/` | `make_synthetic.py` builds a fake benchmark folder. `test_ejs5.py` holds 15 CPU tests on synthetic items with a tiny random model. |
| `PREREG_ejs5.md` | The draft pre-registration. |

## Done on the Mac (CPU, no GPU, no API)

```bash
cd ~/Documents/jev/bench/ejs5; P=~/Documents/jev/opendecide-data/.venv/bin/python
$P -m pytest -q tests                      # 15 passed (synthetic items only)
$P convert.py                              # 868 rows {route 180, triage 148, score 360, gate 180}; 622 commits; late 268
$P score_ejs5.py --check-published         # 12/12 published accuracies reproduced; 0 label mismatches
$P run_ejs5.py --name c1_main500k --model ~/Documents/jev/backups/modal_models/q35_4b_main500k --base Qwen/Qwen3.5-4B \
   --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --rows-sha256 7128b2b8545913fa263f6f4bbdcd0049b2368e0402d74a6516e51f24197b3a4f --dry-run
# pre-flight OK on 868 prompts; tokens mean 317, max 671 (the 2B stand-in q35_2b_armI_1600: PRISM-X spans found too)
```

## L4 run (only after the owner's OK)

### Mac: copy the code and rows (the VM must be free)

```bash
cd ~/Documents/jev; G="--zone us-central1-a --project system-one-509903"
gcloud compute instances start od-l4 $G
gcloud compute ssh od-l4 $G --command 'mkdir -p ~/bench/ejs5/runs ~/bench/external_quarantine/ejs5; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader'
gcloud compute scp $G bench/ejs5/ejs5lib.py bench/ejs5/convert.py bench/ejs5/run_ejs5.py bench/ejs5/PREREG_ejs5.md od-l4:~/bench/ejs5/
gcloud compute scp $G bench/external_quarantine/ejs5/ejs5_rows.jsonl bench/external_quarantine/ejs5/ejs5_rows.jsonl.meta.json od-l4:~/bench/external_quarantine/ejs5/
```

Copy only the code files, never `bench/ejs5/runs/`. Copying `runs/` would overwrite the VM's run ledger.

### VM: `gcloud compute ssh od-l4 --zone us-central1-a --project system-one-509903`

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader   # must print nothing
sha256sum ~/lean/decoder_io.py ~/lean/prism_x.py ~/lean/models/q35_4b_main500k/adapter_model.safetensors \
          ~/bench/external_quarantine/ejs5/ejs5_rows.jsonl
#   expect 8ba8ff4f... 3c4425bf... 507d1c29... 7128b2b8...
export HF_HOME=$HOME/hf HF_HUB_OFFLINE=1; cd ~/lean
R=7128b2b8545913fa263f6f4bbdcd0049b2368e0402d74a6516e51f24197b3a4f
C1="--model $HOME/lean/models/q35_4b_main500k --base Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
# 1) pre-flight with the VM's code (CPU, seconds)
~/od/bin/python ~/bench/ejs5/run_ejs5.py --name c1_main500k $C1 --rows-sha256 $R --dry-run
# 2) S1 = C1, once (about 4-6 min)
nohup ~/od/bin/python ~/bench/ejs5/run_ejs5.py --name c1_main500k $C1 \
  --adapter-sha256 507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078 --rows-sha256 $R \
  > ~/bench/ejs5/runs/c1_main500k.log 2>&1 &
tail -f ~/bench/ejs5/runs/c1_main500k.log      # until "c1_main500k: 868 rows read, 0 errors ..."
# 3) S2 = the 2B, once, after the PREREG amendment names it (values from the amendment)
nohup ~/od/bin/python ~/bench/ejs5/run_ejs5.py --name <2B_RUN> --model $HOME/lean/models/<2B_NAME> --base Qwen/Qwen3.5-2B \
  --revision <2B_REV> --adapter-sha256 <2B_SHA> --prism-x-sha256 <PX_SHA> --rows-sha256 $R \
  > ~/bench/ejs5/runs/<2B_RUN>.log 2>&1 &
```

### Mac: fetch, stop the VM and score

```bash
cd ~/Documents/jev; G="--zone us-central1-a --project system-one-509903"; P=opendecide-data/.venv/bin/python
gcloud compute scp --recurse $G od-l4:~/bench/ejs5/runs/c1_main500k bench/ejs5/runs/
gcloud compute scp $G od-l4:~/bench/ejs5/runs/ledger.jsonl bench/ejs5/runs/ledger_l4.jsonl
gcloud compute instances stop od-l4 $G
$P bench/ejs5/score_ejs5.py c1_main500k --json-out bench/ejs5/runs/scores_c1.json
# S3 = the cascade, after both runs are fetched, with the dev-only fit of THIS pair (refuses another pair's fit)
$P bench/ejs5/run_ejs5.py --cascade --name cascade_2b_c1 --small <2B_RUN> --big c1_main500k --fit-log <pair fit json>
$P bench/ejs5/score_ejs5.py c1_main500k <2B_RUN> cascade_2b_c1 --json-out bench/ejs5/runs/scores_all.json
```

## Time and cost (estimate)

- **Prompts:** mean 317 tokens, max 671. That is 275k input tokens per system, about 0.4 of the JevBench prompt
  length.
- **Measured on this L4 for JevBench** (818-token prompts, batch 1, eager):
  - 4B: load and warm-up 81 s; 231 rows in 57 s (p50 118 ms).
  - 2B PRISM-X: load and warm-up 25 s; 231 rows in 40 s.
- **Expected for ejs-5:**
  - 4B: about 1.5 min load and warm-up, plus about 1.5–3 min for 868 rows. About 5 min.
  - 2B: about 3–4 min.
  - Cascade: no GPU.
  - `--readout 2view` (if pre-registered) adds about 80 % to the read time.
- **In total:** about 20–25 min of L4 time including VM start, copies and stop. That is about **$0.30–0.40** of the
  Google credit (g2-standard-8 at about $0.85/h). There are no API, Modal or Jev calls.
