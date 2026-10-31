# T37b-dev build (draft ruling A70). Everything lives here; nothing is written into data/.

Code: t37bdev.py (library + CLI). Tests: test_t37bdev.py (`HF_HUB_OFFLINE=1 ../../.venv/bin/python -B staged/t37b_dev/test_t37bdev.py` from c2_build).
No G13 job is run; g13_c2.py / decontam_g13.py are not touched.

## Round 1 (done, 17 Oct ~17:29 UTC)
* POOL.json / POOL_REPORT.json: program filters of A70 (d) on the 9 gate dev splits. Pool = 497 rows = 497 groups
  (the 1,605 of the ruling is the count before the source, class and question-negcount filters). 449 survive the cheap
  scope screen of polarity programs A/B before any subject is known; with the 45-per-source cap at most 410 can be kept.
* PLAN.json + PLAN_FREEZE.json: seeded order (key t37b-dev-a70-v1), 497 entries, N0 = 350, extension = next 150 (147 left).
  The frame per entry is not in the plan yet: frames3 fixes it as sha(key|base id) over the frozen frames.
* frames_r1/: Haiku frame authoring (tier A only), 2 tasks. decomp_a/, decomp_b/: two independent Haiku subject reads of the
  first 350 plan questions, 7 tasks each.

## Round 2 (done, 17 Oct ~17:45 UTC)
* frames2 (`t37bdev.py frames2`): 67 unique tier-A candidates from frames_r1 -> A70 (c) lint 54 pass -> decontamination scan
  (rg, whole words, case-insensitive, all of lean/data except paths with ohs / sealed / jev; pattern file decontam_r1.patterns.txt)
  dropped 1 ("Does it hold that", 961 hits) -> 53 candidates -> G-LEX tasks glex_r1_a and glex_r1_b (7 tasks each, same 318 probe
  items, separate seeds/chunks): 3 frame-over-core probes (expected same) + 3 FRAME_NOT probes (expected opposite) per frame.
* ext_decomp: subject reads (two independent) for plan entries 350..496 (decomp_ext_a, decomp_ext_b, 3 tasks each). This is a
  read-only precomputation; WHICH entries count is decided only in `finish` (first 300 survivors in plan order; extension used
  only if the first 350 give fewer than 300).
* Frame assignment (changed from the round-1 note, nothing was paired yet): frame of plan entry pos = frames[pos % n] over the
  frozen frames ordered by sha256(key|frame|frame) (balanced; keeps the 120-per-frame cap reachable).
* Code for the later stages is written and tested on simulated answers in a scratch copy (deleted): round3, round4, finish.

## Next stages (commands from c2_build: HF_HUB_OFFLINE=1 ../../.venv/bin/python -B staged/t37b_dev/t37bdev.py <cmd>)
1. `round3` (needs glex_r1_a/b and decomp_ext_a/b answers): admit a frame only when all 6 probes are read the expected way in BOTH
   rounds; < 3 admitted -> stops and says a second tier-A authoring round is needed (tier B only if still < 3 after 2 rounds).
   Else freezes FRAMES_FROZEN.json + FRAMES_FREEZE.json (sha256), builds CANDIDATES.json for all 497 plan entries (subject
   consensus, partner span, polarity programs A and B both 'opposite', construction check = base + exactly one 'not', negcount,
   379 trained + 33 held-out patterns must not yield the partner), and writes: pol_r3_a/b (Haiku polarity x2) and
   solve_r3_base / solve_r3_partner (Haiku blind solver with 'unsure', base and partner in separate batches). ROUND3_TASKS.json.
2. `round4` (needs the four round-3 batches): drop on polarity reads; keep if solver answers are yes/no and differ; the rest
   (same, unsure, missing) -> REVIEW_QUEUE.json + review_r4 (Sonnet, gold-free, items = text, definitions, both questions).
   Blind-vs-gold agreement is report-only (A70 e has no such rule; A45 b is a training rule).
3. `finish` (needs review_r4): keep review 'exact' only; first 300 survivors in plan order under 45/source and 120/frame caps;
   extension only if the first 350 give < 300; fewer than 300 after the extension -> FINISH_FAILED.json and NO files (no smaller
   set, no fallback to the 33). Else c2_t37b_dev.jsonl (base raw line + partner, alternating) and c2_t37b_dev_relations.jsonl,
   sha256 in T37BDEV_FREEZE.json. Files are never edited afterwards.
