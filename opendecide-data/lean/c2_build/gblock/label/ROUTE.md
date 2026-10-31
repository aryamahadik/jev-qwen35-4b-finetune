# G-block label routing, step 1 (PREREG_FINAL A39 d)

Haiku 5.5 answered the gold-free chunks in `label/chunks/`. A valid answer with confidence >= 0.80 is accepted as given; everything else (confidence < 0.80, invalid, unanswered) goes to Opus 5.5, together with a seeded 5% audit sample of the accepted rows (ceil(5%) per domain, seed 20261013). Opus keeps a row only at confidence >= 0.85 (step 2, later); if Haiku and Opus disagree on more than 6% of a domain's audit rows, that domain's accepted rows are re-read by Opus. No label is edited by hand. Written by `tools/route.py`.

## Totals

- Candidates: 20003; Haiku answer files: 58; chunks with no answer: 1.
- Superseded (A39 fix5, FIX5.md): 2846 ids are excluded from every count below; their '*_b2' replacements are included (--fix5).
- Accepted (Haiku, conf >= 0.80): 11200 (56.0%); pilot reference: 53% (A39 d).
- Routed to Opus: 8803 = low confidence 8733 + invalid 4 + unanswered 66.
- Audit sample (accepted rows also read by Opus): 565.
- Opus queue: 9368 items in 188 chunks (`label/opus_queue/chunks/`).
- Problems: 0.

Routing reasons: low_confidence 8733; missing 66; invalid: answer is not one of the options 4

## Per domain

| domain | candidates | answered | invalid | missing | accepted (conf >= 0.80) | accept rate | low conf | audit | Opus queue | accepted label mix |
|---|---|---|---|---|---|---|---|---|---|---|
| gov_news | 2102 | 2093 | 0 | 9 | 954 | 45.4% | 1139 | 48 | 1196 | yes 31.9% of 624 yes/no |
| learning | 2102 | 2098 | 1 | 4 | 884 | 42.1% | 1213 | 45 | 1263 | yes 22.5% of 650 yes/no |
| museum | 2102 | 2093 | 1 | 9 | 1542 | 73.4% | 550 | 78 | 638 | yes 34.8% of 808 yes/no |
| news | 2102 | 2090 | 2 | 12 | 969 | 46.1% | 1119 | 49 | 1182 | yes 36.1% of 476 yes/no |
| office_help | 1642 | 1635 | 0 | 7 | 759 | 46.2% | 876 | 38 | 921 | yes 82.5% of 378 yes/no |
| open_data | 2102 | 2096 | 0 | 6 | 892 | 42.4% | 1204 | 45 | 1255 | yes 35.9% of 565 yes/no |
| park_programs | 667 | 664 | 0 | 3 | 352 | 52.8% | 312 | 18 | 333 | yes 42.1% of 261 yes/no |
| recipes | 2102 | 2100 | 0 | 2 | 1640 | 78.0% | 460 | 82 | 544 | yes 37.4% of 1004 yes/no |
| sci_abstracts | 2102 | 2094 | 0 | 8 | 1194 | 56.8% | 900 | 60 | 968 | yes 38.2% of 802 yes/no |
| travel | 2102 | 2098 | 0 | 4 | 1442 | 68.6% | 656 | 73 | 733 | yes 26.3% of 832 yes/no |
| volunteer_posts | 878 | 876 | 0 | 2 | 572 | 65.1% | 304 | 29 | 335 | yes 32.9% of 513 yes/no |

## Per card

| card | candidates | answered | invalid | missing | accepted (conf >= 0.80) | accept rate | low conf | audit | Opus queue | accepted label mix |
|---|---|---|---|---|---|---|---|---|---|---|
| gb_gov_news_1_c0 (yes/no) | 526 | 525 | 0 | 1 | 297 | 56.5% | 228 | 12 | 241 | yes 37.7% |
| gb_gov_news_2_c0 (yes/no) | 526 | 522 | 0 | 4 | 327 | 62.2% | 195 | 20 | 219 | yes 26.6% |
| gb_gov_news_2_c1 (choice) | 525 | 523 | 0 | 2 | 147 | 28.0% | 376 | 6 | 384 | top 'drivers and travellers' 58.5% (6 labels) |
| gb_gov_news_3_c1 (choice) | 525 | 523 | 0 | 2 | 183 | 34.9% | 340 | 10 | 352 | top 'service or place change' 43.7% (5 labels) |
| gb_learning_1_c0 (yes/no) | 526 | 525 | 0 | 1 | 257 | 48.9% | 268 | 10 | 279 | yes 45.5% |
| gb_learning_1_c1 (choice) | 525 | 525 | 1 | 0 | 96 | 18.3% | 428 | 6 | 435 | top 'theory first' 53.1% (5 labels) |
| gb_learning_2_c1 (choice) | 526 | 526 | 0 | 0 | 138 | 26.2% | 388 | 7 | 395 | top 'explain an idea' 67.4% (4 labels) |
| gb_learning_3_c0 (yes/no) | 525 | 522 | 0 | 3 | 393 | 74.9% | 129 | 22 | 154 | yes 7.4% |
| gb_museum_1_c0 (yes/no) | 526 | 523 | 0 | 3 | 454 | 86.3% | 69 | 20 | 92 | yes 46.7% |
| gb_museum_1_c1 (choice) | 525 | 522 | 1 | 3 | 327 | 62.3% | 194 | 18 | 216 | top 'flat image' 69.7% (5 labels) |
| gb_museum_3_c0 (yes/no) | 526 | 524 | 0 | 2 | 354 | 67.3% | 170 | 17 | 189 | yes 19.5% |
| gb_museum_3_c1 (choice) | 525 | 524 | 0 | 1 | 407 | 77.5% | 117 | 23 | 141 | top 'something else' 33.2% (6 labels) |
| gb_news_1_c0 (yes/no) | 525 | 523 | 0 | 2 | 95 | 18.1% | 428 | 6 | 436 | yes 71.6% |
| gb_news_2_c1 (choice) | 525 | 521 | 2 | 4 | 232 | 44.2% | 287 | 10 | 303 | top 'no direct stake' 74.6% (5 labels) |
| gb_news_3_c0 (yes/no) | 526 | 522 | 0 | 4 | 381 | 72.4% | 141 | 20 | 165 | yes 27.3% |
| gb_news_3_c1 (choice) | 526 | 524 | 0 | 2 | 261 | 49.6% | 263 | 13 | 278 | top 'something that happened' 86.6% (5 labels) |
| gb_office_help_1_c0 (yes/no) | 547 | 544 | 0 | 3 | 378 | 69.1% | 166 | 23 | 192 | yes 82.5% |
| gb_office_help_1_c1 (choice) | 547 | 543 | 0 | 4 | 179 | 32.7% | 364 | 6 | 374 | top 'make something work' 67.0% (4 labels) |
| gb_office_help_3_c1 (choice) | 548 | 548 | 0 | 0 | 202 | 36.9% | 346 | 9 | 355 | top 'fix a fault' 72.3% (5 labels) |
| gb_open_data_1_c0 (yes/no) | 525 | 525 | 0 | 0 | 273 | 52.0% | 252 | 15 | 267 | yes 18.3% |
| gb_open_data_2_c1 (choice) | 526 | 525 | 0 | 1 | 211 | 40.1% | 314 | 12 | 327 | top 'count or track trends' 81.0% (5 labels) |
| gb_open_data_3_c0 (yes/no) | 525 | 522 | 0 | 3 | 292 | 55.6% | 230 | 12 | 245 | yes 52.4% |
| gb_open_data_3_c1 (choice) | 526 | 524 | 0 | 2 | 116 | 22.1% | 408 | 6 | 416 | top 'people and health' 48.3% (6 labels) |
| gb_park_programs_1_c0 (yes/no) | 166 | 166 | 0 | 0 | 134 | 80.7% | 32 | 8 | 40 | yes 51.5% |
| gb_park_programs_2_c0 (yes/no) | 167 | 166 | 0 | 1 | 127 | 76.0% | 39 | 6 | 46 | yes 32.3% |
| gb_park_programs_2_c1 (choice) | 167 | 165 | 0 | 2 | 29 | 17.4% | 136 | 4 | 142 | top 'relaxed walk or tour' 48.3% (3 labels) |
| gb_park_programs_3_c1 (choice) | 167 | 167 | 0 | 0 | 62 | 37.1% | 105 | 0 | 105 | top 'guided walk or trip' 56.5% (5 labels) |
| gb_recipes_3_c0 (yes/no) | 1051 | 1050 | 0 | 1 | 1004 | 95.5% | 46 | 50 | 97 | yes 37.4% |
| gb_recipes_3_c1 (choice) | 1051 | 1050 | 0 | 1 | 636 | 60.5% | 414 | 32 | 447 | top 'main dish' 32.2% (7 labels) |
| gb_sci_abstracts_2_c0 (yes/no) | 525 | 524 | 0 | 1 | 408 | 77.7% | 116 | 22 | 139 | yes 28.4% |
| gb_sci_abstracts_2_c1 (choice) | 525 | 521 | 0 | 4 | 175 | 33.3% | 346 | 8 | 358 | top 'cells or molecules' 28.0% (6 labels) |
| gb_sci_abstracts_3_c0 (yes/no) | 526 | 524 | 0 | 2 | 394 | 74.9% | 130 | 19 | 151 | yes 48.2% |
| gb_sci_abstracts_3_c1 (choice) | 526 | 525 | 0 | 1 | 217 | 41.3% | 308 | 11 | 320 | top 'method or software' 34.1% (5 labels) |
| gb_travel_1_c0 (yes/no) | 525 | 522 | 0 | 3 | 452 | 86.1% | 70 | 18 | 91 | yes 5.1% |
| gb_travel_1_c1 (choice) | 525 | 525 | 0 | 0 | 286 | 54.5% | 239 | 20 | 259 | top 'getting there' 54.2% (5 labels) |
| gb_travel_2_c1 (choice) | 526 | 525 | 0 | 1 | 324 | 61.6% | 201 | 22 | 224 | top 'plan the route' 49.1% (4 labels) |
| gb_travel_3_c0 (yes/no) | 526 | 526 | 0 | 0 | 380 | 72.2% | 146 | 13 | 159 | yes 51.6% |
| gb_volunteer_posts_1_c0 (yes/no) | 220 | 219 | 0 | 1 | 171 | 77.7% | 48 | 6 | 55 | yes 11.1% |
| gb_volunteer_posts_2_c0 (yes/no) | 219 | 218 | 0 | 1 | 201 | 91.8% | 17 | 16 | 34 | yes 42.8% |
| gb_volunteer_posts_2_c1 (choice) | 220 | 220 | 0 | 0 | 59 | 26.8% | 161 | 2 | 163 | top 'professional or office skills' 32.2% (6 labels) |
| gb_volunteer_posts_3_c0 (yes/no) | 219 | 219 | 0 | 0 | 141 | 64.4% | 78 | 5 | 83 | yes 45.4% |

## Files

- `label/accepted_haiku.jsonl`: {id, label, confidence, qid, audit} per accepted row (qid = the Haiku chunk qid).
- `label/opus_queue/chunks/chunk_XXXX.json`: TEACH-0 items, new opaque qids; routed and audit items mixed.
- `label/opus_queue/key.json` ({qid: candidate id}) and `label/opus_queue/roles.json` ({candidate id: {role, reason}}): orchestrator only, never sent to a reader.
- Inputs (sha256): candidates 37c01d864062b46e; fix5 candidates 2ad2cd424fcefa50; fix5 key 78e5a4a0d3776ef6; haiku answers (all files) 00e0694c8636b590; key 233b0de9ced72967; superseded_fix5 95b1bf9e0ede4e9b
