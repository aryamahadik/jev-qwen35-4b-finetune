# Phase B handoff (fast/adaptive thinking): state at 6 Oct 2026 ~21:50 UTC

**Order:** B1b → router fit → B2 concise LoRA (HANDOFF.md "PHASE B"; PREREG A17-B1, A30).

## B1b: prepared and tested, NOT run
- **Pre-registered:** PREREG A30, written before any run.
- **Code:** in `think/` (modal_think.py configs bf16/fp8_dflash_m16 and bf16/fp8_mtp, eval_think.py, b1b_sets.py).
  43 CPU tests pass.
- **Key finding:** B1a's DFlash failure was our setting, not an SGLang bug. SGLang reserves speculative state for
  129 requests × 16 draft tokens = 99 GB. Capping requests at 16 brings it to 13 GB. Native MTP (NEXTN 3/1/4) is
  the second arm; no speculation is the fallback.
- **Clean set:** GSM8K TRAIN 500, frozen (hashes in A30).
- **Commands:**
  - `bash think/b1b_copy.sh mahadikarya3` (free volume copy of C1)
  - `bash think/b1b_launch.sh mahadikarya3` (fallback: mahadikarya44)
  - `bash think/b1b_fetch.sh mahadikarya3 <run>`
- **Cost:** cap $8 per launch, expected ~$5.1. Phase-B total cap $30; $5.57 spent so far. Free credit only, never
  aryamhd or jaypatil-duke.

## Two locks in b1b_launch.sh (by design)
1. **Date lock:** it refuses before Mon 12 Oct 07:00 UTC. This is the owner decision "Data first, Phase B later",
   made only to save Claude weekly usage. If the owner runs Phase B outside Claude (e.g. Codex), the owner may lift
   this lock.
2. **Overlap lock: OPEN, must be done first.** A17-B1 needs a counts-only overlap check of the B1b set against the
   public test sets AND the A16(a) list: OHS-3, the sealed exports, the DI test items (all 36 source datasets) and
   JevBench, plus ejs-5. Only GSM8K / MMLU / CRUXEval / ARC / CLadder / OHS-1/2 were checked.
   - It must run as a sealed-side, in-process, counts-only program that prints hit counts only, never text. Nobody
     reads those sets.
   - It writes `think/data/clean_b1b/overlap_a16a.json` with `"b1b_math500_hits": 0`. Until that file exists, the
     launcher refuses.

## Then
- **Router fit:** gate_dev.SPLITS dev splits only, free L4 (router.py ready; tasks built: 3,181 rows, ~6.2 L4 h).
  Needs its own amendment.
- **B2:** concise self-distilled LoRA (same 4B, no bigger teacher), ~$10-15, pass rule: ≥ 25% fewer think tokens at
  ≥ 98% of B1 accuracy. Needs its own amendment.
- **Never tune or decide on** OHS-3, DI test, ejs-5, JevBench or the sealed suite.
