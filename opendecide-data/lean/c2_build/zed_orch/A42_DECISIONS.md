# A42-D: Opus rulings on the 41 [DECIDE] tags (15 Oct 2026)

Source: `zed_orch/A42_DETAIL_DRAFT.md` (Sonnet). Result: `zed_orch/A42_DETAIL_FINAL.md` (ready to append after the A43
erratum). `PREREG_FINAL.md` is not edited.

Binding principles applied:
- no gate is loosened;
- Jev is never a selection signal;
- Modal $40 (training ≤ $34) and OpenRouter $10 (about $7 left);
- OHS-AC programmatic freeze before any new-family training-side row;
- money trims follow FINAL_PLAN's cut order (item 10 → wave 2 → item 8's tail);
- spec 5 caps kept (scale rows down, never raise a cap);
- G-proxy ≥ 2,000 rows with paired-CI rules; Jev order OHS-4 → OHS-AC → anchors;
- simpler and stricter where the plan is silent.

Verdicts: **A** = accepted as drafted; **A+** = accepted and tightened; **M** = modified; **R** = rejected.

| # | Draft § | Draft recommendation | Ruling | Reason (one line) |
|---|---|---|---|---|
| 1 | 1.4 | A40's 125,000 binds the base mix only (C2 ≤ 145,000) | **R.** 125,000 binds the whole C2 mix, block and twins included. A breach trims by 2.3 | The plan never raises A40 (d). Stricter and simpler. |
| 2 | 1.5 | New share ≤ 43%, since 1.0× replay makes 40% unreachable | **R.** 40/60 kept. New-family rows scaled 10,000 → 6,664, so floor(1.5×) replay fits the plan's 10,000 replay rows | The plan does not change spec 5's 40% cap. Scale rows down, never raise a cap. |
| 3 | 1.6 | T42 + T43 form a separate "coding tier" ≤ 15% | **R.** No new tier. All six count in the agent tier ≤ 55% (passes at ≥ 36,844 new rows; else T40-T45 scale down) | The plan creates no tier. This is the stricter reading of spec 5.2. |
| 4 | 2.2 | $40 covers every line; SPEED-3 = min($2, $40 − spent); above $40, up to $45, on an owner GO on Fri 23 | **M.** $40 covers every line, including the A41 (b) scans. No pre-authorised path above $40 (only a new owner ruling). SPEED-3 runs in full or not at all | FINAL_PLAN says the total stays ≤ $40. The $45 path would loosen the cap. |
| 5 | 2.3 | Trim T43-T45 first (keeping 1.0× replay), then spec 5.5 | **R.** T_max = min($34, $32 − spend to date). Trim item 10 → wave 2 (T44, T45) → item 8's tail (rows > 8,000) → spec 5.5 | Owner's cut order. T43 is plan item 4, ranked above items 8-10. The table's ≈ $45 is over $40. |
| 6 | 2.4 | No card without an owner GO naming the amount; training only; within $40 | **A** (also within $34) | Strictest reconciliation of A39 (f) and FINAL_PLAN. |
| 7 | 3.1 | G-SL and G3-H apply to authored text only; G0-lite lists exemptions; orchestrator confirms | **A+.** Exempt only program-rendered spans that both execution runs re-derive, and only from checks undefined on code. Confirmed before the first row, never after a result | Blocks post-hoc exemptions, which would be a hidden loosening. |
| 8 | 3.2 | "Chance" = max(1/k, majority share) | **A**, simplified to the majority share of the probe's evaluation split (always ≥ 1/k) | Same value, simpler. Measured where the probe is scored. |
| 9 | 3.2 | Probe models and views = those of G6 | **A.** Every G6 model, on the probe's input view | Reuses tested code. No new bar. |
| 10 | 3.2 | No libcst, jsonschema or hypothesis: `ast.unparse` both sides, seeded generators | **A+.** ≥ 200 seeded property cases per patch. In-house JSON-schema subset with solver B at 100%. Every count unchanged | No network or new packages, and every bar is kept. |
| 11 | 3.6 | Iteration-2 deadline Mon 19 Oct 23:59 UTC | **A+.** A fix never edits the frozen split. If a fix changes a shared oracle, affected sealed items are dropped (never relabelled), counts only | No fix after the sealed text. Sealed golds stay right without relabelling. |
| 12 | 4.1 | Pilot = new rows only, no replay (≈ 9K rows, ≈ $1.5) | **A.** Generated after the OHS-AC freeze | Harsher retention test, with no bar moved. |
| 13 | 4.4 | Own dev = 300 rows per family, from held-out registries, packs and wordings | **M.** 300 per family from training-side values with dev-only packs, registers and wordings (spec 7.1). No sealed-reserved value. Built after the freeze | Sealed-reserved values in a selection set would leak the sealed split. |
| 14 | 4.4 | Existing dev = 9 gate dev splits (7,056 rows), pooled, as D1 reads it | **A** | Matches the spec 7.1 retention set. |
| 15 | 4.4 | A failed joint run re-pilots its families singly (≈ $0.25 each) | **R.** Every family is piloted alone from the start (6 passes, ≈ $1.5). No re-pilot | Clean attribution and one test per family (no second chance), at the same cost. |
| 16 | 5.2 | Opus-labelled (1,272) and A39-dropped rows keep their status; C1 reads of dropped rows are report-only | **A** | No relabel. The A39 outcome stands. |
| 17 | 5.4 | Over 40 chunks: seeded subsample by card; unread DISAGREE rows dropped | **A** | Haiku is right on only 53% of these. Stricter. |
| 18 | 5.6 | Up-weight realised as sampling quotas | **A+.** Quotas only, with the factor fixed at 1.0× | The plan's 1.0-1.5× was unpinned. The low end is simplest and avoids over-weighting ambiguous rows. |
| 19 | 6.3 | "2×" is a selection weight, not repeated rows | **A** | G12 forbids repeated rows. |
| 20 | 6.4 | No trap type above 35% of a family's trap-flagged units | **A** | Limits trap-template learning, the plan's named risk. |
| 21 | 6.5 | T42/T43 (tagged distractors) also get trap selection | **R.** T40-T45 are selected as before | Plan item 1 targets the existing R families. A37 (e) stays unchanged where the plan is silent. |
| 22 | 7.2 | G-block and metadata twins count inside the base new-row cap | **M.** Inside the G-block 15,000 and metadata 12,000 caps, and inside 125,000 (replay 1.5×) | The "base cap" is gone (#1). Each block's own cap is stricter. |
| 23 | 7.4 | ≥ 30 held-out negation patterns | **A+.** ≤ 5 pairs per pattern | Forces the 150 pairs to spread over at least 30 patterns. |
| 24 | 8.2 | No source above 15%; at least 8 domains | **A+.** Also no domain above 20% (as A39 e) | Only 11 sources. Mirrors the A39 limits. |
| 25 | 8.4 | 13 noise-check rows per task | **A** (seeded). 2 of 13 wrong drops the task | 1 wrong (7.7%) passes and 2 (15.4%) drop. Near the plan's read volume. |
| 26 | 9.2 | k ∈ {2, 3, 4}; early = checkpoint nearest 33%, late = final, 1:1 | **M.** k = 3 only. Early+late as drafted. 18 candidates | The plan names one "last-k average". Fewer candidates means less selection noise. |
| 27 | 9.3 | Equal weights in S | **A.** The third term is the 4.4 own dev splits (C2-side), with a two-term fallback | The plan's "OHS-AC dev splits" cannot mean sealed items (never-open rule and freeze). |
| 28 | 9.5 | Final step stays unless the paired-CI lower bound of the S gain is > 0 | **A.** One test (best eligible vs final step). An ineligible final step gives the best eligible; none eligible means the pre-gate fails | A dial is never taken on noise. Closes the ineligible case. |
| 29 | 10.2 | "No loss" = accuracy point ≥ 0 and Brier ≤ 0, on the G-proxy and D1 yes/no | **A** | Strictest reading of "no loss". |
| 30 | 11.3 | ≥ 1,000 requests per level after a 100-request warm-up; p50/p95 per level | **A+.** Jev latency and tokens come from the one OHS-4 Jev read. No other Jev call | A38 allows one look. Keeps OpenRouter inside the 13.8 order. |
| 31 | 12.1 | At least 3 G-proxy sources, none above 40% | **A** | The plan's 2-3 sources, scaled to ≥ 2,000 rows. Limits concentration. |
| 32 | 12.3 | 100 rows per source; drop a source above 8% wrong | **A+.** A dropped source is replaced before hashing. Hash before C1's first read | Keeps ≥ 2,000 rows and ≥ 3 sources. No post-read edits. |
| 33 | 12.4 | Jev G-proxy read after OHS-AC, before the gating anchors | **M.** Stage 4, after the gating anchors and before the exploratory ones | Binding order OHS-4 → OHS-AC → anchors. The General verdict is never part of DOMINATE. |
| 34 | 13.1 | Per-family freeze (own sealed split hashed, then pilot rows); manifest on Sat 17 | **R.** One OHS-AC programmatic freeze before any T40-T45 row (pilot, QC, probe, dev, candidate). Pilots move after it. A family missing from it stays out of C2 | A42's text and the owner principle. The plan gives no reason for Fri 16 pilot rows before the Sat 17 freeze. |
| 35 | 13.1 | "Before any training-side row" covers the six new families only; A1 uses held-out variants | **A+.** A1 goes in the same manifest. No later row of the 17 families uses an A1 held-out variant (G-TPL plus sealed-side G13) | Their rows predate A42. The guard keeps the holdout clean. |
| 36 | 13.1 | Held-out mapping; T43 holds out "1 more mutation operator class" | **M.** T42 and T43 both hold out the same 2 operators, with no extra T43 class. The rest as drafted | Both families use mutants, so a T43 row with a T42-held operator would leak. The plan lists 2 operators. |
| 37 | 13.6 | "Worst" = Jev's highest-scoring run | **A.** Up to 3 complete runs as the balance allows. Best complete run per metric. Spread always reported | Hardest comparison for C2. Defines the partial-budget case. |
| 38 | 13.7 | Holm on the "lower bound > 0" tests; 95% for reporting | **M.** Holm on superiority tests only. Harm vetoes (family UB below −3, anchor significantly worse) use unadjusted 95% | Holm on the vetoes would weaken them, which is a loosening. |
| 39 | 13.8 | $0.50 margin | **A.** A stage starts only if one full run plus the margin fits, and then runs in full. Re-runs come before the next stage. Balance-only: the plan's "anchors only if the OHS-AC lower bound > 0" is dropped | Protects the $10 cap. An outcome-conditioned stage would make a Jev result a selection signal. |
| 40 | 13.8 | Unrun gating anchor → DOMINATE "not evaluable" | **A+.** "Not met" wins if any other part fails. General is "not evaluable" without stage 4 | DOMINATE is never claimed without the anchor veto. |
| 41 | 13.9 | sha256 of 13.6-13.9 recorded in the OHS-AC manifest | **M.** sha256 of the whole appended A42-D block, recorded in the next PREREG addendum with the manifest hash and given to the sealed assembler, before the freeze | Covers every rule. The orchestrator cannot write sealed paths. |

## Edits outside the tags

- Header: dated 15 Oct 2026, with no time placeholder. Adds an append-time check that no T40-T45 row file exists.
- 1.1: groups named as in FINAL_PLAN's ranked list: wave 1 = T40, T41 (item 3); coding = T42, T43 (item 4);
  wave 2 = T44, T45 (item 9). The cut order's "wave 2" is therefore T44 and T45. Minimum cards stay at the plan's
  sizes / 64.
- 2.2: the money table is trimmed to $40. The od-l4 fallback is paid only from the reserve.
- 9.6: "OHS-AC dev splits" becomes the 4.4 own dev splits, so no sealed file is ever read for selection.
- 13.3: the When2Call licence decision is recorded before the 13.9 hash.
- 14: the draft said "no model above 4B is trained, distilled from or used as a label source", which contradicts A39
  and item 10. It is replaced by FINAL_PLAN's actual rule (baselines ≤ 4B; no third-party big-model data) plus A37 (b)
  and A39 (d).

## Open items for the orchestrator

1. At append, confirm that no T40-T45 row file exists (header clause).
2. The freeze-first rule compresses the schedule: freeze → rows → gates and probes → single-family pilots, all by
   Mon 19 Oct 23:59 UTC. Freezing on Fri 16, if every sealed part is ready, recovers a day.
3. Expected T_max ≈ $27.5-30.5 (it depends on the A41 (b) scan spend). At the plan's estimates ($29 + $4.2), item 10 is
   cut first and may be enough. Wave 2 is next.
