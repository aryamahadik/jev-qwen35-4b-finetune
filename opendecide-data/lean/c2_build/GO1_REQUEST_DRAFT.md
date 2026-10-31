# C2 training: GO #1 packet (FINAL numbers, 18 Oct 2026)

Refreshed 18 Oct 2026 ~06:20 UTC after the last final G13 (round 10) converged.
Status: the owner gave GO #1 in advance ("go 1", Record A81). This page holds the final numbers behind it and what is still open before launch.
Every count below is a count only. No row text is quoted. Numbers marked "projection" are guesses, not results.

## Answer first

- The mix is final: **59,340 rows = 23,736 new + 35,604 replay** (replay is exactly 1.5 x new). Train file sha256 starts `cc1d1ff550e4`. The last final G13 (c2_final) is complete, current, and has **0 binding drops**.
- Projected training cost **$14.36** (projection) against **T_max $22.96** (live credit C $30.96, so C minus $8). It fits.
- Preflight says **NOT GO** today. Three of its lines are the items GO #1 fills (owner-GO file, T_max fix, config FILL values). **Two more lines are not covered by GO #1 and need the orchestrator before launch** (see "Open before launch").
- Honest odds that C2 passes every check and ships: **about 15 to 20%**.

## What changed since the last draft

- A68: OHS-4 is the binding sealed test; OHS-AC is report-only for C2 (counts below).
- A69 faithful repair (Record A78) found three families that fail the adopted text; Ruling A80 ("ok go with b") lets C2 train with agent core 4 of 6.
- A76: the final G13 was run to convergence, 10 rounds, drops only.
- A61 (f): the single 8.5 run hit three MD sources; MD then failed A42-D 8.2 and was removed whole.
- Record A81: your "go 1" is the GO #1 for C2, with conditions (below).

## Rows per block (final mix)

| Block | Rows | | Block | Rows |
|---|---|---|---|---|
| replay | 35,604 | | F5 | 1,362 |
| T28 (core) | 2,247 | | F6 | 930 |
| T29 (core) | 2,000 | | F11 | 552 |
| T30 (core) | 1,400 | | F4 | 500 |
| T26 (core) | 1,398 | | GB | 3,376 |
| T31 | 999 | | GW | 3,696 |
| T01 | 1,600 | | I10 | 100 |
| T23 | 794 | | SB5 | 682 |
| T06 | 600 | | | |
| T15 | 900 | | | |
| T25 | 600 | | **Total** | **59,340** |

- New 23,736, replay 35,604. Floor 50,000 rows: held. Cap 125,000: far under.
- 8,690 relations (negation twins): equiv 1,442, inv 2,866, complement 4,382.
- 50,104 units; dry-run steps 3,709; epochs 0.9901.
- Agent core: **4 of 6** (T28, T29, T30, T26). A80 gate true.
- Program families: **10** (T28, T29, T30, T26, T31, T01, T23, T06, T15, T25). Minimum 10: met, with no spare.

## Families entered and left, and why

| Item | Status | Why |
|---|---|---|
| T28 T29 T30 T26 T31 T01 T23 T06 T15 T25 | IN | pass faithful A69, G9 reads, final G13 |
| T33 (was core) | OUT | refused by the faithful A69 repair, (f)(iii) (Record A78): 450 to 396 rows, 12.0% dropped, two checks still failing |
| T12 | OUT | refused by the faithful A69 repair, (f)(iii): longest-option check |
| T24 | OUT | refused by the faithful A69 repair, (f)(iii): longest-option check |
| T07 | OUT | generator bug (A72 precedent) |
| T32 | OUT | failed the G13 check |
| T27 | OUT (C3) | G5-H ambiguous (A62) |
| T35, T37b | OUT (C3) | A52, A65: no candidates / last allowed round failed |
| T40 to T46 | OUT | A64, A59 e, A67, A68 c: C3 or no rows on disk |
| MD | OUT | 8.5 run hit md_worldbank, md_usgs, md_cma (A61 a); MD then failed A42-D 8.2 (under 8,000 rows or 8 domains), removed whole, no waiver |
| F11 (MAMS) | IN, 552 rows | carry block, passed final G13 |
| DI blocks (KR, LANG, TS, RC, TOOLS) | OUT | A61 (c): DI rows 0 |
| SB1, SB4, SB6 | OUT | A58; SB6 also 8.5 HIT |

Newly selected rows that were not read before got the A74 G9 read: T06 96, T25 14, T26 2, T31 2. 0 wrong gold, 0 ambiguous.

## Rulings and records this packet must state

- **Ruling A80** (your words, "ok go with b"): for C2 only, the agent-core minimum is 4 of 6 instead of 5 of 6. The program-family minimum stays 10. A69 stays exactly as adopted. T33, T12 and T24 mixdev rows are report-only ("family not trained in C2"). Disclosed in every C2 report.
- **Record A81** (your words, "go 1"): read as GO #1 for C2. The orchestrator launches only if ALL hold, otherwise it stops and asks:
  1. the last final G13 is complete, current, with 0 binding drops (**met**);
  2. d2-set is written before any read (**met**, below);
  3. preflight_c2 says GO except the items GO #1 itself fills: OWNER_GO_C2.txt, c2_check tmax --fix, FILL values (**not yet, see below**);
  4. projected training cost is at most T_max and fits the relay's live credit (**met**: $14.36 vs $22.96; credit $30.96);
  5. payers mahadikarya2 then mahadikarya3 only (**met**);
  6. the mix is the A80 mix, no family beyond the faithful-A69 set (**met**).
  GO #1 also covers pausing the C1 server on od-l4b while the grid candidates boot. GO #2 (the one OHS-4 look) still needs your words.
- **A68** (OHS-AC report-only): every C2 report says it. Any OHS-AC score of C2 carries the label "report-only for training (A68): training text shares generator frames with A1/A2/B".
- **A61 (f) sentence, exact:** "A42-D 12.2 is unmet: no G-proxy source has a valid 8.5 PASS (A61 a, f)." Every G-proxy result carries that label. No claim may cite the G-proxy until a separate ruling fixes the remedy.
- **A67 / A59 e:** "T46 -> C3 (A59 e: fix count >= 3 against 1 allowed; iteration 1 failed G0-lite)".
- **A62:** "agent core 5/6 (T27 -> C3, A62)" was the old wording; under Ruling A80 it is now **agent core 4/6**.
- **A76:** drops-only convergence; frozen binding drop lists a76_excl_g13final_3 to _8; MD left out through --leave-out; one 8.5 run only (membership = SB5_uci293, 682 rows).
- Breaches disclosed under A61 (d): builder code ran before a valid PASS; block drivers ran per-identifier or variant 8.5 runs; a driver ran the DI-TS deny-list; a fact agent read 20 lines of an OHS-4 name-check result.

## A68: OHS-AC report-only counts (final G13, c2_final)

- Binding drops: **0** (all binding targets zero). Code-literal hits 0. Quarantined templates 0.
- OHS-AC hits, report-only, NOT applied: 38,281 units (45,934 rows) of 50,104 units. By method (units): hash side exact_full 1,816, exact_raw 1,816, exact_sentence 10,124, keyword 38,044, ngram10 10,112, ngram12 10,110, skeleton_instructions 63, skeleton_line 2,774; row side exact_full 1,816, exact_seg 10,124, minhash 3,249, ngram10 10,112, ngram12 10,110, substring 2,903, tulu8 8,925.
- OHS-4 short-exact matches are also report-only by the existing design: 233 raw, 462 normalised.
- Plain words: most of the training text shares generator frames with the OHS-AC test, so C2's OHS-AC score is not a clean test. The binding sealed test is OHS-4.

## d2-set (A81 condition 2)

`gate_c2.py d2-set` was written once, before any read: 17 sources, 3,847 rows, 1,519 units. Content sha256 of the sources `138afa6e87b48155`; file `c2_build/logs/d2_set_c2.json` sha256 `a5f4711bcc89ae5c...` (full: `a5f4711bcc89ae5cae01f62e711640e0464d1899f7bdc22ad4d4ff39b7a999f3`). The 12 PREREG training files plus `c2_parts/c2_train` were passed.

## Money (live, read once by preflight, control plane only)

| Item | Value |
|---|---|
| Free credit mahadikarya2 | $19.10 |
| Free credit mahadikarya3 | $13.86 |
| Total / usable (each less $1) = C | $32.96 / $30.96 |
| T_max after the fix = min(34, 32 - 0 spent, C - 8) | **$22.96** (the credit term binds) |
| Credit covers T_max plus later lines (eval $4, SPEED-3 $2, reserve $2) | yes, exactly: $22.96 + $8 = $30.96 |
| Mix projection (training + $2 overhead) | **$14.36** |
| At round-1 speed 3.716 s/step | $17.66 (3.83 h); at the A28 speed 2.92 s/step: $14.30 (3.01 h) |
| C2 Modal cap, any account | $40 |
| Spend to date | $0 |

- Payers: the relay mahadikarya2 then mahadikarya3 only. No card, no extra account (A61 e). The extra-account option is not needed: the projection is under T_max at both speeds.
- Margin: at the slower round-1 speed, $17.66 vs $22.96 leaves $5.30.
- Grid reads (C1 + 18 candidates + parity) run on the free od-l4b ("use l4 free"), not the H100. No Modal spend for them. Pausing the C1 server there while the candidates boot is covered by A81.

## Open before launch (from today's preflight, NOT GO)

Preflight (default mode) printed these problems. The first four are the GO-fills (A81 condition 3). The last two are not.

GO #1 fills:
1. `train/OWNER_GO_C2.txt` missing.
2. T_max not fixed yet (`c2_check.py tmax --fix`, run by `preflight_c2.py --fix-tmax` inside `c2_chain.sh start`).
3. Config FILL values: epochs 0.9901, expect_ord_rows 14, expect_kd_targets 31549, expect_kd_full 43 (`preflight_c2.py fill`).
4. `pending_after_mix` list needs `--ack-pending` (G13 on the final mix: done; OHS-4 sealed-side child counts: orchestrator to confirm before acknowledging).

Not covered by GO #1:
5. **a61_85:** preflight reads `zed_orch/di_train/A61_FINAL_85_{INPUT.json,RESULT.txt,EXIT.txt}` plus `A61_EDIT_RECORD.json` with their sha256 values. None exist. The single 8.5 run's files are in `c2_build/logs/` under other names (`a61_85_input.json`, `a61_85_result.txt`; 3 HIT, 8 PASS, SB5_uci293 PASS) and there is no exit file. The orchestrator must stage them under the expected names (a copy, no new 8.5 run) and log the shas, or rule otherwise. No flag clears this check.
6. **C1 init adapter missing on both Volumes:** `models/q35_4b_main500k_init` (sha 507d1c29) is not on mahadikarya2 or mahadikarya3 (rc 1). It must be put there (storage only, no compute) before the chain starts. A copy exists on mahadikarya44's Volume per HANDOFF; there is no local copy in `lean/models`.

Everything else in preflight passed: config recipe, mix hash match, rows within 50,000 to 125,000, OHS-4 sha, A42-D block sha, mount probes, snap-monitor CPU record, no stale records, relay accounts exist, no app running.

## Exact launch steps for the orchestrator (README train/)

```
cd opendecide-data/lean ; PY=../.venv/bin/python -B
# 0. the two blockers above (stage the 8.5 files; put the C1 init on both Volumes)
# 1. OWNER_GO_C2.txt: plain text, non-empty (preflight only checks that it exists and is not empty).
#    Content: the owner's words verbatim, with the date: Record A81 "go 1" (18 Oct 2026 ~04:00 UTC), plus Ruling A80 "ok go with b".
$PY c2_build/train/preflight_c2.py fill --dry-run && $PY c2_build/train/preflight_c2.py fill
$PY c2_build/train/preflight_c2.py --offline            # CPU checks, never a GO
# 2. T_max: fixed once, reads live credit on both accounts (expected 22.96). The chain's start does this itself:
$PY c2_build/train/c2_check.py tmax --fix                # or let `start` run preflight --fix-tmax
# 3. launch on mahadikarya2 (free credit)
nohup bash c2_build/train/c2_chain.sh start --ack-pending > c2_build/train/logs/c2_chain.log 2>&1 &
# 4. exit 3 / RELAY (mahadikarya2 credit used up): free hash-checked copy, then resume on mahadikarya3
bash c2_build/train/c2_chain.sh copy
nohup bash c2_build/train/c2_chain.sh resume mahadikarya3 > c2_build/train/logs/c2_chain_mahadikarya3.log 2>&1 &
# 5. watch
tail c2_build/train/logs/c2_chain.log ; $PY c2_build/train/c2_check.py status ; $PY c2_build/snap_monitor_c2.py status
```

Stop rules stay as built: first100 abort, A37 (k) projection stop if training + $2 is above T_max, snap-monitor 25/50/75% reads.

## Tool and file shas (as run)

mix_c2 `214c3d36`, c2_select `2850c3e4`, a69_faithful `c042493b`, gate_c2 `7d4f1f8b`, grid_elig `a4cc6636`, preflight_c2 `84bc2b28`, g13_c2 `17bf92cb`. Train `cc1d1ff550e4`, rel `9bee74bfda38`. Membership file `761c10ae77f5` (SB5_uci293 only).

## Honest odds (estimate, not a result)

| Step | Rough chance |
|---|---|
| C2 trains (after the two blockers are cleared) | high, if they are |
| Pre-gate passes, given it trained | 0.4 to 0.55 |
| S1 to S6 pass, given the OHS-4 look | 0.4 to 0.5 |
| **C2 ships (all of them)** | **about 0.15 to 0.20** |

- Lower than before: agent core is 4 of 6, T33, T12 and T24 are out, and the program-family count has no spare (10 of a minimum 10).
- S1 needs +5.0 pp with a positive lower bound. Pre-gate (b) has little power (600 transfer rows).
- Expected (guesses): new rule/agent set +4 to +10 pp, unseen tasks 0 to +4 pp, general skill -1.0 to +0.5 pp. A gap of about 5 pp to Jev on general skill is expected to remain.
- No bar was loosened. A80 changes only the agent-core minimum, for C2, in your words.

## Honest baseline (C1 today)

C1 sealed OHS-3 74.3 vs Jev 79.6 (older comparator). Text side-bench Index 77.6 vs Jev 1.14 79.3 (no difference demonstrated). Latency p50 100 ms vs 219 ms; p95 603 ms vs 301 ms.

## The question

Your GO #1 is already recorded (A81). Nothing here needs a new answer unless a condition fails. The two blockers in "Open before launch" (items 5 and 6) are orchestrator work. If you want a different path for item 5 (for example a ruling instead of staging the files), say so in your own words.
