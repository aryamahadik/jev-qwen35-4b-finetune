# Frozen run configs (relay runs across Modal accounts)

Each file sets every key. `modal_od.py::relay` (Modal) or `od_gcp.py relay` (L4 tail) reads it, and only the stop point
and `--expect-resume` come from the command line. The trainer refuses unknown keys, and refuses to resume if the
config, data, code or software differ.

## q35_4b_main.json: FINETUNE_PLAN.md section 2.1, applied 30 Sep
The research round's verified changes are applied:
- `r16`/`alpha32` (the tested from-base setting);
- `epochs` 0.97124, exactly one real pass of 30,457 steps (checked by replay_steps.py);
- `aux_norm` "batch" (the loss does not depend on packing);
- `kd` 0.5 on the 43,363 human soft-label rows, with `kd_skip_src` blend50;
- `label_smooth` REMOVED (code review, 30 Sep): the per-source default is exactly what 4B-E, v11 and arm I trained
  with (0.05; MNLI yes/no 0.08);
- `kd_full_src` for the 238 exact-probability rows;
- snapshots every 2,500 steps and at 85/90/95%;
- startup `expect_*` checks.

**Still set by the pilot:** `micro_tokens` (candidates 0 / 10240 / 16384 / 24576; the fastest allowed value) and
whether to install causal-conv1d.

**Owner decisions (current values in the file):**
1. **Weak yes/no family weight:** 1.0x now. The roadmap said 1.5-2x; the research recommends 1.0x (earlier in-family
   gains did not transfer).
2. **`lr`:** 7e-5 now. The critic notes that 5e-5 is the direction the evidence points for a run 17x longer.
3. **KL anchor share:** 0.6% of rows. Tested runs had 6%. Options: add anchors on a seeded 6% of rows (+2% compute),
   or monitor snapshots on dev_nc/devzs.
4. **Cost cap:** if a full pass costs more than $135, give the 4B up to $175 and move the 2B to the L4, or trim
   uniformly.

## q35_2b_main.json: DRAFT. PRISM-X I FROZEN by the owner (30 Sep, 12:30 UTC)
- **Owner decision:** the final 2B uses full PRISM-X I: layout E + authority signal + shadow memory + option-query
  head.
  - Evidence (ledger X18): accuracy ties the plain 2B (−0.27 [−1.34, +0.79]); jagged hijack 1.1% vs 10.0%
    (−8.9 pp [−5.7, −12.0]).
  - A plain 2B would fail the 2B ship rule's attack cap (6.9%).
  - This overrides the pre-registered accuracy-only rule. The owner's reason is security; the cost is a slower 2B
    (no CUDA graphs with PRISM-X).
- **Arm I's tested regime:** from base, r32/a64, lr 1e-4, loss weights 1/1/0.5, kd 0.5, no `label_smooth` key (the
  per-source default), `aux_norm` "micro" at micro_tokens 16384.
- **base_revision:** 15852e8c…, the L4 cache snapshot that arm I and E_L4 used.
- **Still FILL:** `epochs` (replay on the built 2B file), `expect_trainable` (2B smoke), `expect_kd_targets` (the
  build_2b_kd print). The trainer refuses to run until these are filled.
