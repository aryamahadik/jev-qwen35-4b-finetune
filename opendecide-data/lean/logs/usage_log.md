# Claude plan usage log (Max plan; weekly resets Mon 12 Oct 07:00 UTC)
| UTC | 5-h % | weekly % | agents | note |
|---|---|---|---|---|
| 6 Oct 00:00 | 37 | 27 | ~9 | |
| 6 Oct 00:48 | 57 | 32 | ~11 | |
| 6 Oct 01:00 | 64 | 34 | ~12 | burn ~7% weekly/h. Last-hour cache reads 614M tokens. The family-lane agents run 230-370 turns/h at 540-610K context each: polling every ~10-30 s plus huge contexts |
| 6 Oct 03:10 | 12 (reset 02:00) | 43 | ~7 | after the A21.1 lean switch (01:25): 5-h window 12% in 70 min ≈ 2.7% weekly/h (was 7%/h). Projected at data finish (~16 h): ~85% weekly. Tight; keep ≤ 6 lanes, minimise orchestrator turns |
| 6 Oct 16:57 | 25 | 68 | 0 | NEW SESSION start (A24 d). Budget per HANDOFF: lanes ≤20% to A26 cutoff, end ≤6%, reserve 3%. Resuming 6 lanes |
| 6 Oct 17:50 | ? | ? | 6 lanes + build-4 + prep-5 (7 agents) | A27 written; P1 pre-smoke chain running |
| 6 Oct 19:37 | 29 | 76 | 6 lanes + build-4 + prep-5 + r1-budget-cap | burn ~3%/h since 16:56 (incl. one-time speed-check 425K tok + prep-5 + a28 workflows) > 1.2%/h -> THROTTLE lanes 6 -> 4 (queue reordered by readiness: F11 F12 F13 F7 first); F4 crowd launched |
| 6 Oct ~20:00 | - | ~77 | 4 lanes + build-4 + public-repair + a28 + phaseB-B1b-prep | owner HANDOFF update: Phase B in parallel (B1b -> router fit -> B2) on free credit mahadikarya3/44; revised split data 18 / B 4 / end 4 / reserve 3; thresholds now: >=90% no new lane/B steps, >=93% scripts only |
| 7 Oct 00:30 | 12 | 84 | 3 lanes | burn 1.43%/h > 1.2 -> lanes 3 (F7 F13 F12 first), owner OK; public-repair paused at 84% (A29 a) |
| 7 Oct 03:33 | 4 | 88 | 3 lanes + G13 build + cap-fix4 + F11 G9 | burn 85->88 in 2 h = 1.5%/h; at 90% no new lane steps (expected ~05:00 UTC). F11 select PASS 3600/3600 (351 low-p_g + 300 sample) -> G9 re-read launched; F7 shows 'QC sha binding: no full sha256' (record lacks full sha); G13 tool still building |
| 7 Oct 04:53 | 14 | 90 | lanes STOPPED | weekly 90% -> rule: no new lane/Phase-B steps; end phase only (<=94%). Lanes workflow stopped (in repair: F1, F12, F13 -> round 2). Running: G13 batch (script, pid 1987, ETA ~18:30Z), a31 review, mixer review. 3-hourly cron removed to save usage (notifications drive the orchestrator). |
| 7 Oct 07:00 | 22 | 93 | push ceiling | A32 (a) 93% reached: F12/F13 lanes stopped (round 2). F5 A32 DONE (QC pass, crowd+select+G9 pass). F6 v1 failed G11 (option ROUGE-L 0.8) -> builder re-worded, v2 rebuild running (drive.sh, script); F6 agent steps (G5 delta, QC, crowd/G9 redo) NOT started (end-phase reserve 93-97). Running: G13 batch (7 fam, v1 F6 stale), g13-final-fastpath build. |
