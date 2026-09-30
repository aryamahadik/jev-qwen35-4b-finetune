# Relay protocol for the 500K run across Modal accounts (research + code audit, 30 Sep 2026)

Source: workflow wf_75d60cf8-329 (3 research agents, 18 adversarial verifiers, synthesis). Nothing is implemented yet.

**Relay protocol for the Qwen3.5-4B LoRA run split across Modal accounts**

**Short answer.** The resume logic is already right on the math. It restores the step, adapter, AdamW state, LR schedule, torch/CUDA RNG and the exact data order (`train_decoder.py:510-546`). The real risks are elsewhere:
- **Silent restart:** if anything differs, the trainer starts from step 0 without stopping. At its next save it deletes the checkpoint you copied in (`train_decoder.py:547-548`, `:415-420`).
- **Different stack on a new account:** a new account can quietly get different software (unpinned packages) or a different base model (unpinned revision).

Fix those, pass test C, and switching accounts costs nothing beyond the float noise two normal uninterrupted runs already show. Bit-exact equality is not possible even with no account switch (see D).

The run has 31,359 steps: ceil(501,732 / 16), from `train_decoder.py:466`. The warmup is 1,567 steps.

---

**(A) Fixes before step 0** (files are in `opendecide-data/lean/`; nothing has been edited yet)

These are required. Each one blocks a known failure.

1. **A fingerprint mismatch must stop the run, not restart it** (`train_decoder.py:526-548`).
   - If `_ckpt/state.pt` exists and the fingerprint differs, raise an error and print a key-by-key config diff. For that, store the full config dict in `state.pt` (`:412-414`).
   - Add a config key `expect_resume` (true on accounts 2-7). It raises if `/vol/models/<name>/_ckpt/state.pt` is missing, which catches a wrong `--name` or a copy that landed in a nested folder.
   - Add every new per-segment setting (`expect_resume`, `stop_after_min`, `stop_at_step`, `allow_code_change`) to the exclusion list at `:396`. Otherwise the setting itself changes the fingerprint.

2. **Include the data and the code in the identity check.**
   - Today the fingerprint (`:394-401`) hashes only the config, `n_steps` and the row ids.
   - Add the sha256 of the train file bytes and the relations file bytes (read at `:461-462`) to the fingerprint. The relations file drives unit grouping and shuffling (`:134-171`, `:468`).
   - Store the sha256 of `train_decoder.py`, `decoder_io.py`, `prism_x.py` and `writeblock.py` in `state.pt` and require them to match on resume, unless `allow_code_change` is set.
   - Why: code and `data/` are uploaded from the laptop at every launch (`modal_od.py:41`, `:45`). Modal's docs say these files are "added to your container as it starts up" (https://modal.com/docs/guide/images).
   - Commit the code and data before step 0, and do not edit the repo until the run ends.

3. **Pin every package exactly in `image35`** (`modal_od.py:35-38`).
   - Today peft, accelerate, datasets, numpy, sentencepiece, protobuf, hf_transfer and sentence-transformers have no version pin.
   - PyPI released peft 0.21.1 today. Account 1's image has 0.21.0 (`logs/probe35.log`), so a new account building today would already differ.
   - Pin to account 1's build: `peft==0.21.0 accelerate==1.15.0 datasets==5.0.1 numpy==2.5.3 protobuf==7.36.2 sentencepiece==0.2.2 hf_transfer==0.1.9 sentence-transformers==6.1.0 triton==3.8.0 tokenizers==0.23.2 huggingface-hub==1.33.0 safetensors==0.8.0 fla-core==0.5.2 cuda-bindings==13.4.3`, plus the existing torch, transformers and flash-linear-attention pins.
   - Better still, run `pip freeze` inside that image once and pin everything it lists.
   - Pin the full Python patch version in `debian_slim(python_version="3.12.x")`, which accepts a full version (https://modal.com/docs/sdk/py/latest/modal.Image).

4. **Use the same Image Builder Version in all 7 workspaces.** It is a per-workspace setting that fixes the OS, the bundled Python and Modal's client libraries (https://modal.com/docs/guide/images). Check and set it with `modal workspace settings list` and `modal workspace settings set image-builder-version <account 1's value>` (https://modal.com/docs/cli/latest/workspace).

5. **Pin the base model revision.**
   - `decoder_io.py:187`, `:192` and `:195` call `from_pretrained` with no revision, so they load "main".
   - `HF_HOME=/vol/hf` (`modal_od.py:39`) lives on each account's own Volume, so every account downloads whatever "main" is at that moment.
   - Add a config key `base_revision` = `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` for Qwen3.5-4B (`15852e8c16360a2fea060d615a32b45270f8a8fc` for 2B). It must be the full 40-character hash (https://huggingface.co/docs/huggingface_hub/guides/download).
   - Pass `revision=` to the tokenizer call and both model calls.

6. **Check that the adapter really loaded** (`train_decoder.py:531`).
   - Today the result of `set_peft_model_state_dict` is thrown away. PEFT loads with `strict=False` (https://github.com/huggingface/peft/blob/main/src/peft/utils/save_and_load.py), so a key-name mismatch would leave the LoRA weights at their initial values and nothing would say so.
   - Keep the result and raise if `unexpected_keys` is not empty, or if any key containing `lora_` is in `missing_keys`. Do not assert that `missing_keys` is empty: it always lists every base weight.
   - At save time, store a sha256 of every trainable tensor in `state.pt`. After loading, recompute them and require a match before step 1.

7. **Check the optimizer mapping.**
   - `opt.load_state_dict` (`:534`) pairs saved state with parameters by position only (https://github.com/pytorch/pytorch/blob/main/torch/optim/optimizer.py).
   - Save the ordered list of trainable parameters as (name, shape, dtype) in `state.pt`, and require it to be identical before loading.
   - Assert that every trainable parameter is float32.

8. **Record and check the environment and GPU.**
   - Store in `state.pt`: the versions of torch, transformers, peft, accelerate, triton, fla-core, tokenizers, safetensors and huggingface-hub; `sys.version`; the CUDA and cuDNN versions; `torch.cuda.get_device_name(0)` and `multi_processor_count`; the git SHA; `base_revision`.
   - On resume, raise on any difference. The one exception is the host driver, which Modal controls (https://modal.com/docs/guide/cuda): log it only.
   - The SM count matters because the CUDA dropout grid, and so the random masks, depends on it (https://github.com/pytorch/pytorch/blob/main/aten/src/ATen/native/cuda/Dropout.cu).

9. **Prove the data stream was rebuilt exactly.** Save `random.getstate()`, `twin_rng.getstate()` and a hash of the next batch's row ids in `state.pt`. After the replay loop (`:536-541`), require all three to match. Python only guarantees `random()` itself across versions, not `shuffle` or `sample` (https://docs.python.org/3.12/library/random.html).

10. **Commit the Volume after every checkpoint.**
    - Today `vol.commit()` runs only after training finishes (`modal_od.py:129`).
    - Add an `on_ckpt` callback to `train()`, have `modal_od` pass `vol.commit`, and print the checkpoint line only after the commit returns.
    - Modal does not document what happens to recent writes when a container is killed (https://modal.com/docs/guide/volumes).

11. **Planned self-stop.**
    - Add config keys `stop_after_min` and `stop_at_step`.
    - Time `stop_after_min` from the start of `train()`. Do not use `t0`, which `:545` shifts back by the saved minutes.
    - At a step boundary: save the checkpoint, commit, and return `{"stopped_at": next_step}` without writing the final adapter.
    - `_train_impl` (`modal_od.py:124-129`) and the local entrypoint (`:380-381`) must then skip the predictions and `_save`.
    - Never use Modal's spend limit as the stop. The docs only say "Modal stops workloads" and give no grace period or commit guarantee (https://modal.com/docs/guide/budgets).

12. **Make preemption safe.**
    - GPU functions cannot opt out of preemption. Modal sends SIGINT, sends a second interrupt (simulating SIGKILL) 30 s later, then restarts the function on the same input (https://modal.com/docs/guide/preemption).
    - Add a SIGINT handler that only sets a flag. The loop checks the flag after each step, then saves, commits and exits. Saving at a step boundary keeps the saved CUDA RNG state the same as in an uninterrupted run.
    - Lower `ckpt_every_min` to 5. It is already excluded from the fingerprint (`:396`).
    - Never use `modal container stop` for a handoff: it cancels the input and reschedules it (https://modal.com/docs/cli/latest/container).
    - Whether our SIGINT handler actually runs inside a Modal function is not verified. Test C2 checks it.

13. **Fix the `_ckpt.old` crash loop.**
    - If the container dies between `:418` and `:420`, `_ckpt.old` is left next to a valid `_ckpt`. The startup recovery (`:521-525`) ignores it, and every later save then fails at `ckpt.rename(old)` with "directory not empty".
    - Fix: in `_save_ckpt`, delete `old` before renaming. At startup, delete `_ckpt.old` whenever `_ckpt/state.pt` exists.

14. **Make the final save safe.**
    - Today `:630-639` writes the adapter into `out_dir`, deletes `_ckpt`, then writes `train_meta.json`, and the commit comes later.
    - New order: write the adapter, PRISM-X files, tokenizer and `train_meta.json` to a temp directory; rename it; commit; only then delete `_ckpt` and commit again.
    - Refuse to start if a final adapter and `train_meta.json` already exist.

15. **GPU and timeout.**
    - `train_remote35` and the `train` entrypoint both default to "L40S" (`modal_od.py:150`, `:368`). Hard-code `gpu="H100!"` for this run. Plain "H100" can be upgraded to an H200; the "!" prevents that (https://modal.com/docs/guide/gpu).
    - Raise the timeout from `4*3600` (`:150`) to about `9*3600`, with `stop_after_min` below it. The maximum is 24 h (https://modal.com/docs/guide/timeouts).

16. **One frozen config file, Modal only.**
    - `modal_od` and `od_gcp` have different defaults: lam 0.5 vs 1.0, beta 0 vs 1, style od vs cygnet, the v0.11 loss terms, log_every 25 vs 50 (`modal_od.py:365-369` vs `od_gcp.py:160-177`).
    - Add an entrypoint that reads one committed JSON with every key written out, including `micro_tokens`, `seed`, `targets` and `base_revision`. Only `expect_resume` and `stop_after_min` come from the command line.
    - Keep `micro_tokens` the same for all 31,359 steps (`:551`, `:604-606`).

17. **Add a CPU resume test.**
    - `tests/` has none. The existing `train()` test never saves, because the 15-minute default never fires (`test_train_loss.py:533-557`).
    - The fakes need extending: the fake peft has no `set_peft_model_state_dict`, and the fake model saves `fake.pt` instead of `adapter_model.safetensors` (`:488-489`, `:510-517`).
    - Interrupt with `stop_at_step` at N/2, resume, and require `torch.equal` on the weights and optimizer state compared with a straight run. Also require the same batch ids, perms, twins and LR.
    - Also test that a mismatch raises, that `expect_resume` with no checkpoint raises, and that `.old` gets cleaned up.

Recommended. These save money and time; they do not affect accuracy.

18. **Copy `/vol/triton_cache` with each checkpoint** (`modal_od.py:40`). It should be harmless, but I have not verified that it reuses the same kernel choices (https://github.com/triton-lang/triton/issues/9368).
19. **Launch with `modal run --detach`** so a laptop disconnect does not stop the app (https://modal.com/docs/cli/latest/run).
20. **Set a workspace budget in each account** as a backstop so the card is never charged.

---

**(B) Account switch procedure**

**One-time setup per account** (no GPU needed):
1. Log into the account in the browser, then run `MODAL_PROFILE=acctN modal token new`. The profile takes its name from `MODAL_PROFILE`, or else from the workspace name (SDK 1.5.5, `modal/token_flow.py:142-151`). Check with `modal profile list`.
2. Create the secret `opendecide-keys` with the same keys as account 1 (`modal_od.py:44`).
3. Set the image-builder-version to account 1's value, and set the budget.
4. Optional: run a CPU-only function to prebuild the image and download the pinned model revision into `/vol/hf`, so GPU time is not spent on that. This function does not exist yet.

**Handoff from account N to account N+1:**
1. Wait until account N's function has exited by itself: the log shows the stopped line and the commit, and `modal app list` shows no running app.
2. Download the checkpoint: `mkdir -p handoff/segN && MODAL_PROFILE=acctN modal volume get opendecide models/<name>/_ckpt handoff/segN`. Files land in `handoff/segN/_ckpt/`. The local folder must exist first; otherwise SDK 1.5.5 treats the destination as a single file path (`modal/cli/_download.py:53-56`). Do the same for `triton_cache`.
3. Check it on the laptop.
   - Recompute `shasum -a 256` for every file and compare with `manifest.json`. The manifest does not exist yet: `_save_ckpt` needs to write it (step, fingerprint, sha256 of every file) as the last file before the rename.
   - Load `state.pt` with torch and check that the step equals the stopped step and the fingerprint is the expected one.
   - This is the only integrity check on the download: `modal volume get` only checks the HTTP status. Upload does verify an MD5 checksum (`modal/_utils/blob_utils.py:161`).
4. Keep `handoff/segN` until the final model has been evaluated.
5. Upload into an empty path: `MODAL_PROFILE=acct(N+1) modal volume put opendecide handoff/segN/_ckpt models/<name>/_ckpt`, plus `triton_cache` (use `-f` only for that one). Use the same `<name>` on every account, because `out_dir` is `/vol/models/{name}` (`modal_od.py:128`).
6. Download it again from account N+1 and compare the sha256 values with the manifest.
7. Launch with `MODAL_PROFILE=acct(N+1) modal run --detach ...` using the frozen config, `expect_resume` and `stop_after_min`.
8. In the first log lines, confirm:
   - the environment and GPU checks passed;
   - `resumed_at_step` equals the stopped step;
   - the adapter, optimizer and RNG checks passed.

   Then confirm the first logged `lr` matches the formula at `train_decoder.py:510-512`, to every digit:
   - for s < 1567: lr = 1e-4 × (s+1) / 1567
   - otherwise: lr = 1e-4 × 0.5 × (1 + cos(π × (s − 1567) / 29,792))
9. If anything raises, do not change flags to get past it. Diff the configs and investigate.
10. Only one container may ever write to `models/<name>` at a time.

**Budget per segment:** the H100 costs $0.001097/s, about $3.95/h (https://modal.com/pricing). CPU, memory and startup cost extra.
- Start segment 1 with `stop_after_min=360` (about $23.70 of GPU).
- Read the real cost per hour from the dashboard and tune later segments to stop at about $26.

---

**(C) Pre-registered test to run before the real run** (needs your go-ahead)

**Setup:**
- All fixes from A are in, the final pinned image is built, and the frozen config and real 501,732-row data are used. So `n_steps` is 31,359 and the test runs the real first 300 steps of the warmup.
- `stop_at_step=300` in every run. Compare the step-300 checkpoints.
- Only `log_every` may be smaller (it affects printing only).

**Runs:**
- **A1:** account 1, steps 0 to 300 straight.
- **A2:** account 2, steps 0 to 300 straight, on a fresh account (its own image build, model download and Triton cache). A1 vs A2 measures the noise between two uninterrupted runs.
- **B:** account 1, steps 0 to 150; then the full procedure from B; then account 2, steps 150 to 300.

**Exact checks** (any failure means FAIL; fix and rerun):
- **E1:** B prints `resumed_at_step` 150, and every check on load passes: adapter tensor hashes, optimizer names and shapes, environment, GPU name and SM count, Python RNG states, next-batch hash.
- **E2:** the sha256 of every checkpoint file is the same on account 1, the laptop and account 2.
- **E3:** at every logged step, `lr`, `n_cons`, `n_inv`, `n_twin`, `n_rel_skipped` and the batch-id hash are identical across A1, A2 and B.

**Noise checks** (tolerance fixed now, before the results):
- d(X,Y) = ‖θX − θY‖₂ / ‖θA1‖₂, taken over all trainable tensors at step 300.
- g(X,Y) = the mean |loss difference| over the logged steps 150-299.
- **PASS** if d(A1,B) ≤ 1.5 × d(A1,A2) and g(A1,B) ≤ 1.5 × g(A1,A2).
- If A1 and A2 turn out bit-identical, then B must be bit-identical too.
- The 1.5 factor is a chosen margin, because there is only one noise pair. An extra straight run A3 would tighten it.

**C2, preemption** (optional, about 20 minutes): during a B segment, have a timer thread send SIGINT to the process. Check that the checkpoint and commit finish within 30 s and that a relaunch resumes exactly.
- Do not use `modal.exception.simulate_preemption` for this. It raises `KeyboardInterrupt` from SIGALRM, which bypasses a SIGINT handler.
- With `jitter_seconds > 0`, it also draws from Python's global random stream, which would shift our data order (SDK 1.5.5 `modal/exception.py:296-326`).

**Cost and step time:** I have not measured the step time. At a guess of about 5 s/step, the test is about 2 H100-hours, roughly $8 plus startup. Use it to measure the real time per step. Seven accounts at about $26 each give about 46 H100-hours, so the run only fits if a step takes 5.3 s or less.

---

**(D) Honest answer: remaining accuracy risk**

1. **Once A is fixed and C passes, a systematic loss from switching accounts is ruled out.** The bugs that could cause one (wrong adapter, wrong optimizer moments, wrong data, different base model or packages, silent restart) all stop the run loudly instead. Data order is the known place where resuming really costs accuracy: CheckFreq measured up to a 13% drop from a broken iterator (https://www.usenix.org/system/files/fast21-mohan.pdf). Our replay is exact and E3 proves it.

2. **What cannot be removed: float noise.** It exists in an uninterrupted run too.
   - Sources: SDPA flash-attention backward is non-deterministic by default; the FLA Triton kernels use TF32, about 5e-4 precision (`logs/budget_ledger.md:99`), and re-tune per container; cuBLAS gives no guarantee across setups.
   - Every preemption restart inside a single account already causes the same kind of break.
   - Its size is the same as run-to-run noise. Published work finds top-line accuracy "not noticeably impacted", though some slices of the data are more sensitive (https://arxiv.org/abs/2106.11872). In fine-tuning, different seeds can give quite different results (https://arxiv.org/abs/2002.06305).
   - In this project the dev CI is about ±1.2 pp (`budget_ledger.md:147`), and jagged ASR swings from 5.8% to 30% between runs (`:146`).
   - So "zero accuracy loss" in the bit-exact sense is impossible even with no account switch. "No loss beyond what running it again once would give" is achievable, and C measures it.

3. **One open question.** The only real resume so far (2B O1 on an L4) had exact data order and LR, with identical counts and lr at steps 225 and 250. But the per-step losses differed: 0.8532 vs 0.8747 at step 225, and 1.1625 vs 1.1452 at step 250, with most of the gap in the cons term (`logs/train_q35_2b_armO1.log`).
   - No straight-vs-straight baseline was ever run, so I cannot say whether that gap is pure noise.
   - I found no unsaved random state in `prism_x.py`, `writeblock.py` or `compute_loss`.
   - The A1-vs-A2 comparison in test C answers this. Treat the relay as unproven until then.

4. **Risks to finishing the run, not to accuracy.**
   - Account policy: the terms put restrictions on free use and allow suspension. Section 1.3(c) bars letting third parties use an account, which matters if the 7 accounts belong to other people (https://modal.com/legal/terms).
   - Keeping every handoff checkpoint on the laptop protects against losing an account. Asking support@modal.com, or applying for academic credits (up to $10k, https://modal.com/pricing), would remove the need for relays entirely.