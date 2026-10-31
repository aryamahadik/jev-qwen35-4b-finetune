# C2 pass-odds analysis (Opus, 17 Oct 2026 ~16:10 UTC; rules intact)

## Levers (L0-L7)
LEGITIMATE LEVERS FOR C2 (all inside adopted rules; no bar loosened; all must be done BEFORE training or before the first read)

L0. Make A68 runnable (otherwise the A62(c) stop still applies)
- The A68 block in PREREG_FINAL.md does not contain the marker word "OHSAC_REPORT_ONLY" (grep finds it 0 times). ruling_gate.py (c2_build/zed_orch/owner_options/) refuses any id "whose block lacks the marker". The switch also still has "7 defects to fix before arming" (HANDOFF). Fix both.
- The G13 batch running now (pid 17331) is plain `g13_c2.py candidates --block T01…SB5`. It started about 14:57 UTC, before A68, so it does not go through the capture wrapper and its logs will have no `drop_ids_by_class`. The owner_options README says: "a log that has an OHS-AC record but no valid split is refused (never guessed)". So the binding G13 has to run through `g13_c2_opt3.py … --ohsac-report-only A68`: candidates for all 20 blocks plus carry for F4 F5 F6 F11.

L1. G9 selection settings (the biggest data lever for the 5-of-6 agent core)
- **Trap selection is adopted but not implemented.** A42-D 6 ("changes A37 (e)") says: a unit is trap-flagged "if C1 … puts ≥ 0.25 probability on any tagged trap option" → "hard bin at 2 × selection weight … inside the spec 5.2 caps (hard ≤ 30%, easy ≤ 25%)"; "No trap type exceeds 35%". c2_select.py and crowd_select.py never use `meta.opt_err`, although T26, T28 and T33 rows carry it (T01 rows do not).
  - This puts C1's own mistakes into training, which raises pre-gate (a) and S1.
  - Headroom, from C1 crowd labels vs program gold on the candidates: T12 .60, T32 .60, T06 .63, T25 .66, T31 .67, T01 .68, T33 .70, T30 .71, T28 .72, T24 .75, T26 .79, T29 .84, T23 .85, T07 .89, T15 .90.
  - The easy bin is empty everywhere (p_g > 0.97 almost never; CROWD_READ_C1_17OCT pg_bins), so hard share is the only difficulty setting that moves. T32 is 36% hard and must be capped at 30%.
- **Balance repair that is allowed to under-fill.** A49 (c): "Balance checks bind on the selected rows … c2_select swaps units where it can." But `a49c.swap_balance` only fixes yes rate, yes/no share and twin share. The dry run (`_dryrun_20261017/partial_checks.json`, provisional selection) fails checks that swaps cannot touch:
  - T26 token mean 807.7 > 800 and longest-option −3.26;
  - longest-option outside ±2 pp for T06 (+3.36), T12 (−3.55) and T24 (+3.05);
  - T15 equiv share 4.56% (< 5%);
  - "T01: a card holds 67 rows > 64 (A42-D 1.5)";
  - twin share 25.3–27.6% for T01 T07 T12 T23 T25 T29;
  - yes/no share for T15 .44, T23 .40, T25 .39, T26 .43.
  - `mix_c2.a49c_assert` turns every one of these into a problem, and --final refuses.
  - Fix: one seeded, whole-unit, same-bin repair step for every binding A49c and cap check. It may stop below the target (spec 5.3: "Missing shares lower the total; they are never refilled") and never relabels. Write it, test it and get a skeptic review before the first real select. Record it as a program-fix ruling like A66, because A37 (e) says "selection unchanged".
  - T26 is the case that decides training: its pool after G13 drops is about its 1,400 target (batch-4 count 1,402; A55 estimate 1,600), so chance alone cannot fix its token mean.

L2. Start the G9 re-read now
- The rule (crowd_select.g5_reread) is: "every row with crowd p_g < 0.05 (all candidates) + a seeded 300 of the selected rows … any confirmed error = generator bug".
- The low-p_g set is already fixed, because all C1 reads are done: 695 rows. Agent core: T28 192, T26 90, T29 56, T33 26, T30 19.
- Reading these now gives the earliest warning of an agent-core loss. The seeded 300 per family have to wait for selection.

L3. Finish and freeze the dev sets before the binding G13 (or run one refresh-dev after)
- **Pre-gate (d) cannot be computed.** There is no `data/c2_t37b_dev.jsonl` (the 16 Oct G13 fix "drop[ped] c2_t37b_dev"). `gate_c2.complement_rule` returns UNMEASURED, so pregate raises Refused, and `split_rows` refuses a missing split anyway.
  - Spec 3.18: "T37b-dev: 300 complement pairs on binary-predicate yes/no rows of the 9 gate dev splits, written with held-out frame templates. They are never trained." A52 (a) moved only the T37b training block to C3.
  - Build it exactly as the spec says (negcount, 2/2 Haiku polarity reads, blind solver, any doubt drops the pair). Its frames must be outside the trained 379-pattern catalogue (A42-D 10.3: catalogue pairs "would score 0 violation by construction").
  - It needs a short pre-result Opus ruling on where the frames come from. The 33 A48-F7 held-out patterns are recorded as used "only for the G-proxy's 150 complement pairs … and the symmetrisation probe". So either author new held-out frames (with G-LEX 2/2) or say explicitly in the ruling that those 33 may be reused.
  - Do not re-point (d) to the G-proxy pairs: the C2R plan lists that as needing the owner's words.
- **The merged `data/c2_mixdev.jsonl` has no visible writer**, yet the gate and the snapshot monitor read it. Build it as "150 per trained family" (spec 7.1): entered families only. T27's mixdev is report-only (A62) and block mixdevs are report-only (A39 h).
- Any dev file that appears after a G13 run makes every log stale. So finish every dev file first and register T37b-dev as a G13 target in the one code-edit window after batch5. If anything changes later, run one `g13_c2.py refresh-dev`.

L4. Money (A61 e)
- The rule: "T_max = T_core = min($34, $32 − spend, C − $8)". C − 8 ≈ $22.96 is the binding term.
- Rough full mix: program families ≈ 18.4K rows, plus GW 4,450, GB ≈ 3.7K, MD ≈ 11.4K, SB5 ≤ 750, F5 1,500, F6/F11/F4 ≤ 2,500 and I10 125 ≈ 42–43K new rows. With replay that is ≈ 105K rows, about $24 at the dry-run rate ($11.81 per 57,437 rows, plus $2).
- A42-D 2.3 then trims in this order: I10 (125 rows) → wave 2 (T44/T45/T46, all empty) → MD rows above 8,000 → only then proportional. The proportional step cuts program families, which cuts (a) and S1.
- Levers:
  - (i) No C2 Modal spend on mahadikarya2/3 before training, because every dollar there lowers C. Keep crowd, grid and snapshot reads on od-l4b (A42-D 2.2: "0 on od-l4").
  - (ii) A61 (e) allows "other accounts or the card only by a new owner ruling at GO #1". Show the owner, neutrally, the projection at the A28 model (2.92 s/step) and at round 1's measured 3.716 s/step (+27%, ≈ $28–30). With a zero-margin trim, A37 (k) "stop and ask if the steps-100-300 projection is above T_max" fires if speed matches round 1. An extra account lifts T_core to about $30.5.
  - (iii) Get every passing block in on time:
    - F6: `zed_orch/f6_carry/install_carry_inputs.sh`, then `f6_carry_qc.py --write` before Tue 20 Oct 23:59 UTC;
    - F4/F5/F11: carry G13;
    - SB5 and md_*: the one A61 final-mix 8.5 run.
- **Not levers:**
  - The replay ratio. "Replay is floor(1.5 × realised new rows) for every new row" (A42-D 1.2; `REPLAY_X = 1.5`), so new rows are exactly 40%. Replay allows only drop-only quality steps: the A46 deny list (4,034 rows), human rows with p_g < 0.2, and `pg_anchor` (kept 81,209, dropped 1,368). Pre-cleaning replay against the binding new targets is also drop-only, and it keeps G13 #3 on the final mix near 0 drops.
  - `--leave-out`, which is only the spec 10.2 usage cut order.

L5. Candidate rule (A42-D 9 replaced A37 "one candidate: the final-step adapter")
- The grid is frozen at 18 candidates: final step, last-3 average and early+late average, each at α ∈ {0.5…1.0}. `runs/q35_4b_c2.json` saves 8 checkpoints (snap_fracs 0.25…0.92 plus the final).
- 9.5: "The final step stays the candidate unless the eligible candidate with the highest S has a paired 95% CI of its S gain … LB > 0 … If the final step is not eligible, the eligible candidate with the highest S is chosen."
- No new family entered, so S = mean(G-proxy, R mixdev) (9.3).
- This is the strongest pre-registered lever for the pre-gate and for S2: there are 18 chances at eligibility, and α < 1 trades a little R gain for general accuracy and Brier.
- Caveat to state in reports: eligibility is searched on the same dev reads, so the pre-gate result is optimistic. OHS-4 S1–S6 are not affected.
- Tools needed before training (train/README open items):
  - a per-candidate eligibility wrapper; today "gate_c2.py … has no per-candidate eligibility mode";
  - a read plan for all 18 candidates on od-l4b;
  - the grid.json sha recorded before any look;
  - CANDIDATE_C2.json written before the official pre-gate reads (check_candidate refuses a record written after the first read).
- Every G-proxy use carries the A61 (f) label.
- A42-D 10 symmetrisation is adopted only if complement violation falls by ≥ 0.02, with no accuracy or Brier loss on the G-proxy and the D1 yes/no rows, and D9 still passes. It helps S3/S4. Its q / flip-q read and latency scripts are missing.

L6. Same readout and layout everywhere
- Spec 9.1: "rendered-prompt sha identical across trainer, gate and server" (cygnet + schema_branch_mark).
- 7.3: merged bf16 on SGLang S1, with "≥ 99.5% argmax agreement" vs the HF adapter. 7.2: "C1 and C2 are read in the same job". D9: "same served path".
- Freeze one S1 config hash (the A35 / A49 f path) for both the C1 reference and C2.
- No trial-bundle dials: FP8 failed parity at 98.7–99.0%, and answer-changing dials need the owner's words.
- Run a CPU check of the prompt sha (modal_od_c2 vs gate_dev predict vs the S1 client) before launch.
- Temperature: one per type, fit leave-one-group-out on mixdev, bounded [0.8, 1.3], frozen with the candidate.

L7. Order of small steps
- Run `gate_c2.py d2-set` right after `mix --final` and before any read: "a D2 set written after the first read" is refused.
- Before launch: the snap-monitor CPU record, OWNER_GO_C2.txt and the FILL values.
- One pre-gate per candidate.

## Risks (R1-R10)
BIGGEST RISKS (ranked), how to see each one early, and my rough odds

R1. C2 never trains because of process gaps (probability of passing is 0 until these are fixed):
- the A68 marker is missing and the switch has 7 open defects;
- the batch5 logs cannot be used under Option 3, so a capture batch is needed (Mac alone, about 3–4 h);
- there is no T37b-dev, so the pre-gate refuses;
- there is no merged c2_mixdev file;
- trap selection is not implemented.
How to see it now: `owner_options/ac_report_only.py report` (dry run), and `mix_c2_opt3.py --dry-run` as soon as the capture logs exist.

R2. Agent core is exactly 5 of 6. A62: "any later loss at a binding gate (final G13, mix balance) = STOP".
- T26 is the weakest: pool ≈ target, and on the dry run its token mean, longest-option and yes/no checks fail.
- T28 is thin: 2,430–2,522 rows vs 2,400, after 564 binding OHS-4 hash drops.
- T33 is on its first G13: 3,213 candidates, so it can lose at most 813 rows.
- Low-p_g re-read rows: T28 192, T26 90. One confirmed wrong gold counts as a "generator bug".
How to see it: a scratch dry select on the capture logs, plus the early low-p_g re-read (P3).

R3. Pre-gate (b) has little statistical power.
- Transfer dev is 600 rows (T19 300 + T21 300), not spec 7.1's 1,200. The rule is "C2 − C1 ≥ +3.0 pp and LB > 0".
- At an SE of about 1.8–2 pp, C2 needs an observed gain of about +3.7–4 pp.
- Do not enlarge the set: the sizes are fixed by spec 7.1.
How to see it: you can't during training ("never read on … transfer dev", spec 9.1). The only early learning signal is mixdev at 25/50/75%, which is report-only.

R4. The R gain is too small for S1.
- S1 is "C2 − C1 ≥ +5.0 pp and paired 95% LB > 0" on n ≈ 1,454 with SE ≈ 1.15. It passes about 50% of the time at a true +5 and 78–82% at a true +6.
- Round 1's sealed general result was only +0.9 / +0.11.
How to see it: the mixdev trend at the snapshots. At the pre-gate, a rule of thumb: if (a) is below about +12 or (b) below about +4, S1 is a coin flip or worse (spec 1.3 expects R to be 40–60% of the in-family gain). Report this; change nothing.

R5. General harm.
- S2 needs LB > −1.5, which means a point estimate above about −0.5 (SE 0.51).
- The snapshot stop fires if the old slice is "below C1 − 1.5 pp at both the 25% and 50% snapshots". Round 1 was −1.85 / −1.40, missing the bar by 0.10.
- C2 runs about 4× the steps (≈ 6,500 vs 1,650) at the same LR, so the 25% read comes after about 4× more updates on new rows.
How to see it: at the snapshots, old slice, P(yes) drift ≤ 0.02 and KL(C1‖C2) on 2,000 new rows. Per grid candidate: D1 (LB > −1.5), D2, D3 (each ≥ C1 − 1.0) and the G-proxy (4.3: reject if UB < −0.5). The only allowed mitigation is a grid candidate with α < 1.

R6. Calibration: D4 needs Brier ≤ C1 + 0.005; round 1 was +0.0018. S4 is the same measure on OHS-4.
How to see it: D4 and the yes-share drift at the pre-gate.

R7. Complement checks (d) and S3.
- T37b is in C3 and RTW is empty, so real-text complements come only from GB twins (224), MD twins (1,545) and F5.
How to see it: (d) on the held-out-frame T37b-dev, and the G-proxy's 150 pairs (report-only). Symmetrisation (A42-D 10) is the only lever.

R8. Money and speed.
- T_core ≈ $22.96 with no margin. If speed matches round 1, the steps-100-300 stop-and-ask fires, and a proportional trim would cut program families.
How to see it: `mix_c2 --dry-run` with live C at GO #1.

R9. The one-shot A61 final-mix 8.5 run may HIT an md_* source or SB5. The removal path then risks the MD 8,000-row floor and the A60 shares. You only see this at that run.

R10. Time and usage.
- The carry QC records are due Tue 20 Oct 23:59 UTC and the block cutoff is Wed 21 Oct 23:59 UTC ("a cutoff that never waits").
- Weekly usage was 81% at 15:50 UTC Sat; the reset is Mon 19 Oct 15:00 UTC, plus one manual reset.

Rough odds (my estimate) once R1 is fixed:
- P(it trains) ≈ 0.6–0.7;
- P(pre-gate passes, given it trained) ≈ 0.4–0.55 (the grid helps, the small transfer dev hurts);
- P(S1–S6 pass, given the OHS-4 look) ≈ 0.4–0.5;
- so P(C2 ships) ≈ 0.10–0.20.

## Parallel lanes (P1-P9) and order after batch5
WHAT CAN RUN IN PARALLEL NOW (Sat 17 Oct, about 16:10 UTC)

Constraints while batch5 (pid 17331) runs on the Mac:
- Do not edit g13_c2.py, decontam_g13.py, or any mixdev, candidates or transfer-dev file.
- No second G13 run on the Mac.
- Never kill a job.

P1. Arm A68 (Sonnet build + Sonnet skeptic)
- Fix the 7 A68-switch defects in c2_build/zed_orch/owner_options/.
- The orchestrator adds the marker word "OHSAC_REPORT_ONLY" to the A68 block. The owner's words are already recorded, so this is a mechanical tag. If the permission classifier objects, do not work around it; ask the owner.

P2. Selection tools (Opus writes the short program-fix ruling; then Sonnet code + skeptic)
- In c2_select: A42-D 6 trap weighting, plus the A49c/cap repair (seeded, same bin, may stop below target, never relabels).
- Test it with a scratch-only dry selection on the current candidates and batch-4 drops (no select_<FAM>.json written). The target: T26, T01, T15, T23 and T25 pass.

P3. Early G9 re-read (Haiku dual blind reads → Sonnet adjudication → Opus confirms flags)
- The 695 rows with p_g < 0.05, agent core first: T28 192, T26 90, T29 56, T33 26, T30 19.

P4. T37b-dev (Opus frame ruling → Haiku authoring + G-LEX 2/2 + negcount + 2/2 polarity reads + blind solver → Sonnet builder)
- 300 pairs, staged outside data/ until batch5 ends.

P5. Dev splits for prediction (Sonnet)
- A builder for the merged c2_mixdev (trained families only), staged until batch5 ends.
- Predict-job manifests for mixdev, transfer dev, T37b-dev and the G-proxy.

P6. Grid tooling (Sonnet + skeptic; CPU tests only)
- Per-candidate eligibility wrapper (11 booleans per candidate).
- Read plan for the 18 candidates on od-l4b.
- Symmetrisation q / flip-q reads and latency script.
- CANDIDATE_C2 timing.

P7. Serving freeze (Sonnet, od-l4b, free)
- Pin the S1 config hash.
- Merge + parity harness (≥ 99.5%) and the D9 latency harness on the same served path.
- Prompt-sha check across trainer, gate and server.
- The snap-monitor CPU record.

P8. F6 carry (Haiku or Sonnet; light CPU)
- Run install_carry_inputs.sh, then `f6_carry_qc.py --write` before Tue 20 Oct 23:59 UTC.

P9. GO #1 request refresh (Haiku draft + Sonnet skeptic)
- A68 (b)(d) wording.
- Per-block binding drops vs OHS-AC report-only drops.
- The sentence that the G-proxy's A42-D 12.2 is unmet (A61 f), and the A67 sentence.
- T_core with live C (read once, by the orchestrator).
- The trim order, and the money at both speeds.

ONLY AFTER BATCH5 ENDS (one after another)
1. One code-edit window: register T37b-dev, then write the merged mixdev.
2. Capture batch via `g13_c2_opt3.py --ohsac-report-only A68`: candidates for the 20 blocks plus carry for F4 F5 F6 F11, Mac alone. Run refresh-dev only if a dev file changes later.
3. G9 select, then the seeded 300 re-reads per family.
4. Replay pre-clean and draw.
5. A61 final-mix 8.5 run (orchestrator, once).
6. `mix_c2_opt3 --final --credit-usd <C>`.
7. G13 #3.
8. d2-set.
9. Preflight.
10. GO #1.
11. Training on the mahadikarya2 → mahadikarya3 relay, with snapshot reads on od-l4b.
12. Grid and its 18 dev reads.
13. select_candidate.
14. Pre-gate.
15. GO #2 (L1, then J).

Stopping batch5 now and relaunching it through the wrapper would save about 3 h, but it needs the owner's OK. Earlier kill attempts were refused by the permission classifier, and the owner said not to stop running jobs. The default is to let it finish; its strict union counts also feed the A68 (d) report-only numbers.

Model routing: Opus for rulings and flag confirmations only; Sonnet for code, skeptic reviews and adjudication; Haiku for blind reads, authoring and drafts.

Key paths:
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/PREREG_FINAL.md
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/owner_options/README.md
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/c2_select.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/a49c.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gate_c2.py
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/train/README.md
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/_dryrun_20261017/partial_checks.json
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/reads/CROWD_READ_C1_17OCT.json
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/f6_carry/STATE.json
