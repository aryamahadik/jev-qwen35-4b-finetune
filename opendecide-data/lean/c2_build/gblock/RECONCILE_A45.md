# RECONCILE_A45: every G-block count, from the files

Written by `tools/route_a42d.py reconcile` (A45 task, 15 Oct 2026). Nothing was relabelled; no file in the build was
changed. All numbers below are recomputed from the files named in the table.

## Populations

| Population | File | Count |
|---|---|---:|
| Wave-1 rows in `candidates.jsonl` (includes the superseded ones) | `candidates/candidates.jsonl` | 20,003 |
| Superseded by fix5 (card re-rendered with the `no` line) | `candidates/superseded_fix5.json` | 2,846 |
| fix5 `_b2` replacements | `candidates/fix5_candidates.jsonl` | 2,846 |
| **Live wave-1 candidates** (20,003 - 2,846 = 17,157 base, + 2,846 replacements) | candidates + fix5 | **20,003** |
| Haiku-accepted (conf >= 0.80) | `label/accepted_haiku.jsonl` | 11,200 |
| of which in the 5% Opus audit sample | same, `audit` = true | 565 (493 of them read, 0 disagreements) |
| Routed to Opus by the Haiku cascade (low conf 8,733 + invalid 4 + missing 66) | `label/opus_queue/roles.json` role `route` | 8,803 |
| Opus queue (routed + audit), in 188 chunks | `label/opus_queue/{key,roles}.json` | 9,368 |
| Chunks the A41 selection ran (150 seeded + 14 slipped) | `SELECTION_A41.json` (150) + A41 note (14) | 164 |
| Chunks with an Opus answer file | `label/opus/` | 163 |
| Items in those 163 chunks (nominal 163 x 50 = 8,150; the last queue chunk has 18) | `label/opus_queue/chunks/` | 8,118 |
| of which with no answer in the file | `label/opus/` | 52 |
| Opus answers | `label/opus/` | 8,066 |
| of which route items | | 7,573 |
| of which audit items (Haiku-accepted rows) | | 493 |
| **Opus-kept** (route items, valid, conf >= 0.85) | `opus_finalize_A39.json` `opus_kept` | **1,272** (recomputed: 1,272) |
| **A39-dropped** (route items read, conf < 0.85) | `opus_finalize_A39.json` `dropped.low_conf` | **6,301** (recomputed: 6,301) |
| Routed rows never read by Opus (24 unselected chunks, chunk 15, the 52 unanswered) | derived | 1,230 |
| Labelled pool (Haiku 11,200 + Opus 1,272) | | 12,472 |
| G-block mixdev (150 x 11 domains, drawn from the pool) | `route_a42d/mixdev_ids.json` | 1,650 |

Items in answered chunks without an answer: 52 (48 route items, 4 audit items). The never-read rows by
reason: {"chunk not answered (A41 selection / chunk 15)": 1182, "in an answered chunk, no answer": 48}.

## The routing population A42-D 5.1 means: 18,773 rows ("about 18.8K")

The C1 read covers every wave-1 row that carries a Haiku or an Opus verdict, kept and dropped:

    haiku_accepted 11,200 + opus_kept 1,272 + a39_dropped 6,301 = 18,773

- **18.8K is not a file count.** No file holds it. It is 11,200 + 7,573 = 18,773: the Haiku-accepted rows
  plus the Opus-read route items (1,272 kept + 6,301 dropped). FINAL_PLAN item 6 and A42-D 5.1 round it to 18.8K.
  The state map's "8,150 items in 163 answered chunks" is the nominal 163 x 50. The chunks hold 8,118
  items, 8,066 were answered, and 7,573 of those are route items. 7,573 = 1,272 + 6,301 is
  therefore consistent with the files; it is not a shortfall against 8,150.
- The 493 audit items are Haiku-accepted rows. They are in the 11,200, not in the 7,573.
- Rows never read by Opus (1,230) have no kept or dropped verdict. They are outside the
  population (they were never kept and are not in the 12,472). They are not read by C1 either; adding them would be a
  report-only extra and is not needed for any rule.
- The live candidates (20,003) are the whole wave-1 set. 18,773 of them have a verdict.
- Per-domain counts of the population: {"gov_news": 1942, "learning": 1913, "museum": 2031, "news": 1933, "office_help": 1525, "open_data": 1940, "park_programs": 616, "recipes": 2038, "sci_abstracts": 1964, "travel": 2020, "volunteer_posts": 851}.

## Wave 2 and W8 are not in the routing population

| Population | File | Count |
|---|---|---:|
| Wave-2 candidates (W1-W7) | `wave2/candidates/candidates.jsonl` | 11,832 |
| Haiku-kept (Haiku = program/construction gold, conf >= 0.80) | `wave2/kept_haiku.jsonl` | 9,073 |
| Opus-kept at the queue (agrees with gold, conf >= 0.85) | `wave2/opus_finalize_A40.json` `opus_kept` | 431 |
| Opus queue dropped | same, `dropped` | 2,270 + 67 no answer |
| Pool (9,073 + 431) | | 9,504 |
| After the A40 (ii) seeded cap | `wave2/final_kept_A40.jsonl` | 7,295 |
| W8 candidates / Haiku-kept / Opus-kept / capped | `w8_candidates.jsonl`, `kept_haiku_w8.jsonl`, `opus_finalize_w8.json`, `final_kept_w8.jsonl` | 1,702 / 1,574 / 54 / 1,200 |

- **ROUTE.md vs opus_finalize_A40.json.** `wave2/ROUTE.md` was written 13 Oct 17:53 UTC, before the Opus reads. Its line
  "Opus reads have NOT been run" was true then and is stale now. `opus_finalize_A40.json` (18:04) is later and is the
  record the PREREG A40 result cites: 64 of 65 chunks read, 431 kept, 2,270 dropped. The two files do not conflict
  once dated. `ROUTE.md` was not edited.
- **Why they are outside.** Wave-2 and W8 labels are the program or by-construction gold (A40 c), not Haiku or Opus labels.
  A42-D 5.2 defines its classes on "Haiku-accepted rows (Haiku confidence >= 0.80 per A39 d)", FINAL_PLAN item 6's
  evidence is on the wave-1 cascade, and wave 2 has its own cap (A40 d: 8,000, 9,200 with W8). The 15,000 cap of
  A39 e / A42-D 5.5 is the wave-1 block's.
- HANDOFF's "G-block 12,472, wave 2 7,295, W8 1,200" is the labelled pools: 12,472 = 11,200 + 1,272.
- The A40 note says wave 2 is 8,495 after W8 (7,295 + 1,200). The sum of the three pools is 12,472 + 8,495 = 20,967.

## Consequence for A42-D item 5

- Classes (5.2) apply to the 11,200 Haiku-accepted rows minus the mixdev rows drawn from them.
- The 1,272 Opus-kept rows and 6,301 dropped rows keep their status; their C1 reads are report-only.
- The mixdev (1,650 rows, 150 per domain) comes out of the 12,472 kept rows before any class is formed and is never trained.
- The "about 5K rows freed" of 5.7 is the 65% AGREE-HIGH leaving the block plus the rebalance.
