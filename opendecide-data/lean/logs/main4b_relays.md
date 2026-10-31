# 4B main run (q35_4b_main500k): relay log

| Segment | Account | Start (UTC) | Stop (UTC) | Steps | Notes |
|---|---|---|---|---|---|
| 1 | jaypatil-duke | 30 Sep ~17:45 | 30 Sep 22:34 (--stop-after-min 290) | 0 -> 6510 | 0 ALERT; snapshots s002500 and s005000 backed up to handoff/main500k_snaps/ |
| 2 | arya-mahadik-ai | 30 Sep 22:37 | planned ~02:12 (--stop-after-min 215) | 6510 -> ... | Fits the September credit alone (about $19.4 left, about $17 planned) |

## Relay 1 -> 2 (30 Sep 22:34-22:37 UTC), with logs/relay_seg1_to_seg2.sh
- **Stop:** segment 1 stopped at step 6510 and wrote _ckpt with next_step 6510.
- **Download:** handoff/main_s1/_ckpt; compare_relay.py --check gave OK, problems [].
- **Upload:** the target path on arya-mahadik-ai was empty. Uploaded, re-downloaded to handoff/main_s1_back, and
  compare_relay --check gave OK again.
- **Frozen files:** unchanged vs the tag final-frozen (git diff --quiet).
- **Resume:** {"resumed_at_step": 6510, "checks": "manifest, config, data, env, code, tensors, optimizer order, data
  order: all match"}.
- **Learning rate:** the first segment-2 lr (step 6550) is 6.491094417395e-05. It equals the scheduler formula
  (train_decoder.py:758-760, evaluated at step+1) to every digit, as do segment 1's steps 6450 and 6500. The schedule
  continues exactly.

| 2 (done) | arya-mahadik-ai | 30 Sep 22:37 | 1 Oct 02:10 | 6510 -> 11290 | Clean stop; next_step 11290 |
| 3 | arya-mahadik-ai (same account, October credit) | 1 Oct ~02:13 | planned ~06:47 (--stop-after-min 274) | 11290 -> ... | No transfer: the checkpoint stays on the volume |

## Relay 2 -> 3 (1 Oct, about 02:11 UTC, same account)
- Segment 2 stopped at step 11290, and the app completed.
- Backup: handoff/main_s2/_ckpt was downloaded to the Mac, and compare_relay --check gave OK.
- logs/relay_same_account.sh: no app running; October used $9.30, so stop-after-min is 274 (keeping $2 of margin at
  $4.09/h). Frozen files are unchanged vs final-frozen.
- Segment 3 resume: {"resumed_at_step": 11290, "checks": "manifest, config, data, env, code, tensors, optimizer order,
  data order: all match"}. The lr at step 11300 is 5.205717232825e-05, which equals the formula at step+1 exactly.

| 3 (done) | arya-mahadik-ai | 1 Oct 02:13 | 1 Oct 06:46 | 11290 -> 17428 | Clean stop; next_step 17428 |
| 4 | aryamhd (fresh October credit) | 1 Oct ~06:50 | planned ~13:40 (--stop-after-min 410) | 17428 -> ... | Transfer verified |

## Relay 3 -> 4 (1 Oct, about 06:47 UTC), with logs/relay_transfer.sh arya-mahadik-ai aryamhd
- Download to handoff/main_s3: compare_relay OK. Upload to aryamhd (target path was empty), re-download to
  handoff/main_s3_back: OK.
- aryamhd October used $0.00, 13,029 steps left, so stop-after-min 410 (credit bound). Frozen files unchanged.
- Segment 4 resume: {"resumed_at_step": 17428, "checks": "...: all match"}. The lr at step 17450 is 2.946943945590e-05,
  which equals the formula at step+1 exactly.

| 4 (cancelled) | aryamhd | 1 Oct 06:49 | 1 Oct 13:16 (cancelled) | 17428 -> 25682 | The laptop lost its network, and Modal cancelled the .remote() input of `modal run --detach`. The signal save wrote _ckpt at next_step 25682, then the task was killed after 30 s. |
| 5 (final) | atmosphor | 1 Oct 13:39 | runs to the end | 25682 -> 30457 | Launched with extra/relay_spawn.py (.spawn()), so it does not depend on the laptop |

## Recovery after the segment-4 cancellation (1 Oct, 13:33-13:40 UTC)
- **Log:** at 13:16:24 the container received a cancellation signal. The checkpoint at next_step 25682 was written,
  then "failed to respond to cancellation for too long: 30 seconds - killing task", and the local client showed
  `[Errno 8] nodename nor servname provided` (no network).
- **Checkpoint:** downloaded from aryamhd to handoff/main_s4/_ckpt. manifest step 25682, state.pt next_step 25682,
  compare_relay --check OK (all files match the manifest). Only the about 40 steps after the 25626 save point were
  redone.
- **Transfer:** uploaded to atmosphor (target path empty), re-downloaded to handoff/main_s4_back, compare_relay OK.
  Frozen files unchanged.
- **New launcher:** extra/relay_spawn.py, with the same config logic as modal_od.relay and .spawn() in place of
  .remote(). App ap-vfLzIKSPzMPANbYUsQyX8a (detached), call fc-01M3VV4HH2MPASRZYEMAJQDJQ7, no stop point (runs to the
  end). Logs are streamed with `modal app logs` into logs/main4b_seg5.log.
- **Lesson:** future long segments must use the spawn launcher so that network loss cannot cancel them.
- **Snapshots:** 25888, 27411 and 28934 will all be written on atmosphor.
- Segment 5 resume: resumed_at_step 25682, all checks match; the lr at step 25700 is 4.563548878508e-06, which equals the formula at step+1 exactly.

## FINISHED (1 Oct 2026, about 17:16 UTC, atmosphor)
- All **30,457 steps** are done (train_meta: steps 30457, minutes 1380.98 ≈ 23.0 h of training). The final adapter is
  saved in models/q35_4b_main500k on atmosphor (app ap-vfLzIKSPzMPANbYUsQyX8a stopped normally). The laptop was
  offline during part of segment 5; the spawned run was not affected.
- Mac backup: /Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k (626 MB). It holds the final
  adapter (sha256 507d1c29…) and snapshots s025888 (a16f4b08…), s027411 (5433a908…) and s028934 (9fed952c…).
  gate/check_adapter.py gives ok for all 4.
- The 4B gate (goal step 2) is ready (gate/gate_4b_l4.sh). The owner asked to WAIT for "resume" before the L4 starts.
