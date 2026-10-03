# A12 result: C1 vs Jev on OHS-1 + OHS-2 (practice sets from now on), 3 Oct 2026

C1 was read once on the backup L4 od-l4b as `q35_4b_main500k_b100` (byte-identical to C1). It used the shipped A5 readout:
choice rows read twice, yes/no rows once, T = 1. Scoring used `score_ohs.py` unchanged, against Jev runs `jev_guard` and
`jev_r2_guard`.

| Test | C1 micro | Jev micro | C1 − Jev [95% CI] | C1 macro | Jev macro | Brier C1 / Jev |
|---|---|---|---|---|---|---|
| OHS-1 (1,847 base rows) | 80.4 | 81.7 | −1.2 [−2.9, +0.4], tie | 80.1 | 81.5 | 0.140 / 0.114 |
| OHS-2 (1,320 base rows) | 81.0 | 81.5 | −0.6 [−2.2, +1.1], tie | 81.3 | 82.0 | 0.057 / 0.038 |
| **Pooled by rows** | **≈80.65** | **≈81.61** | **≈ −1.0** | | | |

Older 4Bs on the same tests: v11b was −3.1 on OHS-1, and v11c was −1.0 on OHS-2.

A12 branch rule: pooled C1 is not ≥ Jev + 1.0 pp, so the work does not stop. It continues with C, starting from C1,
because B adopted nothing.
