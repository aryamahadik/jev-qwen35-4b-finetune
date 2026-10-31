# ALREADY TESTED on C1 (NOT research; measured 12-17 Oct 2026; do NOT re-plan these as new work)

Sources: speed/opt_c1_20261017/results/, speed/opt_c1_round2_20261017/{TRIALS.md, VOICE_REAL.md, MULTIMODAL_C1_PREVIEW.md,
h100/TRIALS_H100.md}, commit 01d67c5 (B1a).
- Serving: SGLang S1 (merged bf16) is the adopted path. H100 batch-1 server p50/p95 32/41 ms (round 1); SGLang 0.5.20
  fast path 14.1 / 19.2 ms per decision (batch 8: 9.9 ms/decision; graph == eager). Cold start 131 s (needs a warm pool).
- End-to-end (laptop -> us-west, c=1, small n): C1 p50 137 vs Jev 156 ms; p95 162 vs 224 ms.
- FAILED / no gain at the 99.5% parity bar: FP8 W8A8 (+21% throughput, parity 98.7-99.0%), block-FP8 (98.38%), FP8
  margin gate (not confirmed out of sample), exact server bundle (no gain), full-graph prefill (crashes on GDN),
  DFlash speculative decoding (fails on 0.5.20 KV accounting).
- Cost: $0.0137 per 1K at 100% GPU use, $0.0275 at 50%, $0.069 at 20%; Jev measured $0.0234 per 1K -> C1 is cheaper only
  above ~59% utilisation. OHS-3 measured run cost C1 $0.433 vs Jev $0.061 (low utilisation).
- Image: --mm-feature-transport=cuda_ipc 94.6 -> 75.1 ms, +66% c8 throughput, answers unchanged (ADOPTED). Vision
  side-bench Index C1 77.7 vs Jev 1.14 85.1 (base 73.6).
- Voice: Nemotron Speech Streaming EN 0.6B, 560 ms mode + forced flush (LOCKED); ~86 ms after end of speech; decision
  unchanged 97% on synthetic audio, 89% on real speech.
- Think mode: decode 242 tok/s, cap300 1.29 s, DEER1024 3.06 s/item; helps track C (+3.4), hurts F (-5.4) on practice sets.

WHAT IS LEFT (the only NEW speed/cost/quality work; the planner must give each a lane, model tier, gate and day):
1. Training-side (C2.1 run): FP8-aware training (KL to the bf16 parent) so 8-bit passes 99.5% parity; option-order-
   invariant training so one read per choice question passes parity; compact static-first prompt (prefix cache).
2. Data-side: ASR-error rows (real speech 89% -> >= 97%); image decision data later (vision gap 77.7 vs 85.1).
3. Deployment (no training, free/cheap): warm pool (no 131 s cold start), hosting near users, cheapest GPU that keeps
   parity (measure on the free L4 / GCP credit, never Modal), batching to keep utilisation above ~59%.
4. Security: the coding-agent security families (shell gate, scope, secrets, injection carriers, K/X attack robustness)
   and the Tier-1 security eval harnesses (licence-checked; eval only), prepared before C2.1 training.
5. Selective think tier (owner-reserved): a router that uses think only on types where it helps.
