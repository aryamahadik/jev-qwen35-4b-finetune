# OpenDecide 4B: final report (TEMPLATE)
Fill every `{{…}}` from the Source named. Aggregates only; sealed domains as D-ids only; report every endpoint whatever its direction. *ref* = measured before the final tests. Runbook: `c_build/endgame/RUNBOOK_FINAL.md`.

## 0. What shipped
| Item | Value | Source |
|---|---|---|
| Shipped 4B | `{{q35_4b_c_r1 \| q35_4b_main500k}}` | `sealed_nd/score_nd.py status` verdict |
| Adapter sha256 | `{{…}}` | look log / PREREG_FINAL note |
| Base | Qwen/Qwen3.5-4B @ 851bf6e8…, layout schema_branch_mark, style cygnet | train_meta |
| Readout | choice/Score 2 views (given + reversal, prob. mean); yes/no once; T choice `{{}}`, yes/no `{{}}`, Score 1 | recipe 6.0; PREREG_OHS3 amendment |
| Think mode | `{{shipped / not shipped (B1 rule unmet)}}` | A17, A17-B1 |
| 6.3 | `{{no round 2 / round 2}}`: S1 select CAND−C1 `{{}}` pp [`{{}}`] | gate_c.py |
| 6.4 C look | `{{SHIP / NO SHIP}}` | gate_c.py |
| Carried disclosures | if C1: A10 A (ship look 1 DO NOT SHIP on (e); F7 probe NO GO); C1 never "passed the ship rule" | A10 |

### 0.1 C look (6.4): candidate vs C1
| Rule | Pass when | CAND | C1 | Diff [CI] | Pass? |
|---|---|---|---|---|---|
| P1 part A confirm | ≥ +1.0 pp and LB > 0 | {{}} | {{}} | {{}} | {{}} |
| P2 each domain | no UB < −2.0 pp | — | — | worst {{}} | {{}} |
| P3 part B (B1+B2) | not UB < 0 | {{}} | {{}} | {{}} | {{}} |
| D1 dev full (7,056) | LB > −1.5 pp | {{}} | {{}} | {{}} | {{}} |
| D2 unseen-source, re-derived | not (pt < −1.0 and UB < 0) | {{}} | {{}} | {{}} | {{}} |
| D3 yes/no; choice | ≥ C1 − 1.0 pp each | {{}} | {{}} | {{}} | {{}} |
| D4 calibrated Brier | ≤ C1 + 0.005 | {{}} | {{}} | {{}} | {{}} |
| D5 equiv flips; perm flips | ≤ C1 + 2 pp | {{}} | {{}} | {{}} | {{}} |
| D6 jagged / OPI ASR | > max(C1+2pp, 3%) and LB>0 fails | {{}} | {{}} | {{}} | {{}} |
| D9 latency p50 | ≤ C1 × 1.05 | {{}} ms | {{}} ms | {{}} | {{}} |
Power: ~77% at a true +2.0 pp (recipe 6.4); dev detectable ~1 pp (PREREG 3.5).

## 1. Accuracy vs Jev on unseen domains
### 1.1 Sealed new-domains suite (J look, report-only; suite f4ae8637…, scorer 953a3363…; Jev with guard)
| Set | Items | OD | Jev 1.13 | OD−Jev [CI] | C1 *ref* |
|---|---|---|---|---|---|
| **Part A confirm** | 3,663 | {{}} | {{}} | {{}} | {{}} |
| Part A all | 6,205 | {{}} | {{}} | {{}} | {{}} |
| Non-adjacent (D1,D10,D11,D12) | 3,446 | {{}} | {{}} | {{}} | {{}} |
| Adjacent (D2–D5) | 2,759 | {{}} | {{}} | {{}} | {{}} |
| Per domain (8) | ~550 | {{}} | {{}} | {{}} | {{}} |
| Part P | 600 | {{}} | {{}} | {{}} | {{}} |
| B1 commits | 298 | {{}} | {{}} | {{}} | {{}} |
| B2 long docs | 199 | {{}} | {{}} | {{}} | {{}} |
| Jev unanswered | — | — | {{}} | — | — |
| B3 yes-share alarm | — | {{}} | {{}} | report-only | {{}} |

### 1.2 OHS-3 (`results_ohs3/final_table.md`, `score_ohs3_all.json`; Jev = mean of jev_guard + jev_r2_guard, pinned typesafe/jev-1.13-20260917)
| Endpoint (base rows) | OD | Jev | Diff [CI] | Holm p | Verdict |
|---|---|---|---|---|---|
| **Micro (1,852)** | {{}} | {{}} | {{}} | {{}} | {{}} |
| Macro (13 tasks) | {{}} | {{}} | {{}} | {{}} | {{}} |
| Brier yes/no (716; Jev−OD) | {{}} | {{}} | {{}} | {{}} | {{}} |
| Secondary `_bc` micro; `_1v_cal` micro | {{}} | {{}} | {{}} | BH {{}} | — |
| Track U / Track F | {{}} | {{}} | {{}} | — | — |
| Per task (13) | {{}} | {{}} | {{}} | — | — |
| Without 12-gram-overlap items (A10 D) | {{}} | {{}} | {{}} | — | — |
| Jev run1 vs run2; unanswered; non-pinned | — | {{}} | — | — | — |
| "Accuracy ≥ Jev" (beats, or matches with pt ≥ 0) | {{won/not}} | | | | |

### 1.3 Practice/public (report-only)
| Set | Shipped | C1 *ref* | C1+think *ref* | Jev | Source |
|---|---|---|---|---|---|
| OHS-1 micro | {{}} | 80.4 | 80.9 | 81.7 | score_ohs.py; A17-B0c |
| OHS-2 micro | {{}} | 81.0 | 80.8 | 81.5 | same |
| Decision Index 10K index | {{}} | 54.83 | 57.74 (DI-informed) | 59.51 (v0.1 pub.) | report_*.json |
| DI GSM8K/CRUX/MMLU/GPQA/CLadder | {{}} | {{}} | 98.3/82.5/86.8/43.9/71.6 | {{pub.}} | report_think10k.json |
| Nimble all-13 / clean | {{}} | 74.2 / {{}} | 76.4 / 75.1 | 76.0 / 74.3 | report_b0b.json |
| ejs-5 full / late / Gate | {{}} | {{}} | — | {{pub. answers}} | bench/ejs5/runs/scores_*.json |

## 2. Hijack / prompt injection (score_jagged.py, score_opi.py)
| Set | Metric | Shipped | C1 *ref* | 4B-E | Jev guard | Rule |
|---|---|---|---|---|---|---|
| Jagged (486 items) | ASR | {{}} | 0.0% | 0.6% | {{}} | D6 cap |
| OPI (180 texts) | ASR | {{}} | 1.3% | 1.8% | {{}} | D6 cap |
| OHS-3 | same "text is data" guard for both | — | — | — | — | descriptive |

## 3. Consistency
| Measure | Set | Shipped | C1 *ref* | Jev | Source |
|---|---|---|---|---|---|
| Equivalence flips | dev 722 pairs | {{}} | 8.86% (fails PREREG (e) vs 5.68%) | — | gate D5; A10 |
| Permutation flips | dev | {{}} | 2.43% | — | gate D5 |
| Complement violations | dev | {{}} | 3.30% | — | A10 C |
| Complement violation | OHS-3 `_neg` | {{}} | — | {{}} | score_ohs3.py |
| Option-order drift (304; reversed/rotated) | OHS-3 | {{}} | — | {{}} | final_table.md |
| F7 nested negation (252 pairs) | probe | {{if read}} | 34.5% | — | A10 |
Note: with 2 views, reversed twins drift ~0 by construction; quote the rotated twins.

## 4. Speed (H100)
| Measure | OD | Jev | Source |
|---|---|---|---|
| **S1 e2e p50/call, OHS-3, conc. 1, interleaved** | {{}} ms | {{}} ms | logs/ohs3/timing/ohs3_timing/summary.json |
| S1 rule (CI of Jev−OD p50 > 0 AND p95 lower) | {{pass/fail}} | | same |
| p95 / p99 / server_ms | {{}} | {{}} | same |
| Fast path p50/p95, batch 1 | {{}} (*ref* 14.1/19.2 ms) | — | think/runs/final_speed_* |
| Fast path, batch 8 per decision | {{}} (*ref* 9.9 ms) | — | same |
| Think decode; cap300; DEER1024 | {{}} (*ref* 242 tok/s; 1.29 s; 3.06 s) | — | same |
| Cold start (not in S1) | {{}} | {{}} | timing summary |

## 5. Cost
| Measure | OD | Jev | Source |
|---|---|---|---|
| **C1 $/1K decisions, 40% util.** | {{}} | {{}} ($0.042/M input tok × measured) | ohs3_final_table.py |
| C1 at 100% | {{}} | {{}} | same |
| C2 as-run OHS-3 per 1K calls | {{}} | {{}} | billing / OpenRouter |
| C3 JevBench formula per 1K | {{}} | 0.0384 | scores_v154_*.json |
| Tokens/call in/out | {{}} | {{}} | final_table.md |
| Cheaper than Jev? | {{yes/no}} | | |
Caveats: self-hosting operating cost not included; layout E prompts are longer; 2 views double choice reads.

### 5.1 Spend
| Account | Use | Amount | Credit/card |
|---|---|---|---|
| aryamhd | round-1 training ({{}} steps, {{}} s/step) | {{}} | card |
| atmosphor | crowd read | {{}} | credit |
| jaypatil-duke | rrun, pre-reads, pre-smoke, final tests | {{}} | credit |
| GCP L4 | DI / ejs-5 / OHS-1/2 / JevBench-local | {{}} | Google credit |
| OpenRouter | OHS-3 Jev ×2 + timing; sealed J | {{}} | key limit $10 |

## 6. JevBench
Local, unofficial, 231 public v1.5.4 items (score_v154.py): shipped {{}}, C1 {{}}, Jev {{}} (Intelligence-only column = the fair comparison; band edge disclosed). **No JevBench submission (public or sealed, incl. the $49 sealed run) without the owner's explicit OK.**

## 7. Claims allowed
- "Beats Jev on OHS-3" only per the PREREG_OHS3 "beats" rule. "Matches" only per its −2.0 pp / −0.010 rule. Otherwise the result is "neither" or "Jev is better".
- "Better than C1 on new domains" only if P1 passed.
- "Faster than Jev" only if the S1 rule holds. "Cheaper" only if our C1 cost at 40% is below Jev's.
- J read, OHS-1/2, DI, Nimble, ejs-5 and JevBench are report-only.
- State the power: ~1 pp on the dev full set, ~1.5 pp on unseen sources.

## 8. Deviations/disclosures
- {{third unscored Jev timing pass (D2 extra_pass)}}
- {{A10 D overlap, with and without}}
- {{OHS-1/2 practice since A12}}
- {{DI-informed label}}
- {{A20 (c) parity FAIL: 1×H100}}
- {{A22 F10 length rule}}
- {{A15 isolation incident}}
- {{post-run bug fixes: old and new numbers}}