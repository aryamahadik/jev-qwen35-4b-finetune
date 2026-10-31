# Round 1 final verdict

**Verdict: NO SHIP.** C1 (`q35_4b_main500k`) remains the shipped decision model.

| Gate look | Candidate − C1 | 95% paired CI | Rule | Outcome |
|---|---:|---:|---|---|
| 6.3 S1 sealed select (n=2,542) | +0.90 pp | [−0.16, +1.96] | +2.0 pp and lower bound > 0 | No round 2 |
| 6.4 C confirmation (n=3,663) | +0.11 pp | [−0.69, +0.96] | +1.0 pp and lower bound > 0 | No ship |

All 6.3 development guards D1–D6 passed: retention, calibration, equivalence and permutation robustness, and the Jagged/OPI security checks. The candidate did not meet the pre-registered primary sealed-effect threshold, so it is not promoted over C1.

The sealed scorer records `no_ship` on C look 2. No further evaluation can turn the failed C-confirmation primary rule into a ship decision. The C-confirmation primary rule failed on its own; the full 6.4 helper report remains incomplete because the pinned scorer does not print the required pooled B1+B2 aggregate that the helper schema expects. This does not affect the conservative `no_ship` outcome.

## Follow-up

- Do not run a round-2 broad fine-tune from this candidate.
- Phase B should use C1 as its fast decision baseline.
- Phase B may later produce a separate concise-thinking LoRA only after its clean-set B1 measurements and router checks pass.
- OHS-3 remains a one-shot final test of the shipped model. Its harness still requires a filled, committed C1 configuration and its listed code-manifest commits before it can run.

## OHS-3 final evaluation: C1 vs Jev

The committed C1 configuration passed the H100 development smoke (100 dev rows, zero errors and parity checks passed), then completed its one allowed scored OHS-3 pass and load test. The two required pinned Jev runs completed with 2,456 / 2,456 calls answered in each run.

| Measure | C1 | Jev | Result |
|---|---:|---:|---|
| Micro accuracy (1,852 base rows) | 74.298% | 79.644% | Jev better |
| Macro accuracy (13 tasks) | 74.314% | 79.676% | Jev better |
| Yes/no Brier | 0.172 | 0.150 | Jev better |
| Complement violation (300 pairs) | 0.170 | 0.088 | Jev better |
| Option-order drift (304 pairs) | 0.023 | 0.041 | No clear difference |
| End-to-end p50 | 100.110 ms | 219.010 ms | C1 lower p50, but does not satisfy the pre-registered speed rule |
| End-to-end p95 | 603.070 ms | 301.370 ms | Jev lower |
| Cost / 1K decisions at 0.4 utilisation | $0.433 | $0.061 | Jev cheaper |

**Final decision-model verdict:** retain C1 as the OpenDecide baseline, but do not claim parity with or a win over Jev on OHS-3. The detailed approved-harness output is in `opendecide-data/lean/results_ohs3/final_table.md`.
