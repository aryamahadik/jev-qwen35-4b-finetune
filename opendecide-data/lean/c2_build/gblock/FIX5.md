# G-block fix5: five yes/no cards re-rendered with the `no` definition (PREREG_FINAL A39 c/d)

13 Oct 2026. CPU only, no network, no label set or read, no file deleted.

## Why

`tools/build_candidates.py` printed every yes/no card as the `- yes: ...` line only (its default `--yesno-card yes`).
For five admitted cards the `no` definition holds edge rules that a reader (and later the model) must see:

| card | domain | candidates |
|---|---|---|
| gb_recipes_3_c0 | recipes | 1051 |
| gb_sci_abstracts_2_c0 | sci_abstracts | 525 |
| gb_gov_news_2_c0 | gov_news | 526 |
| gb_volunteer_posts_3_c0 | volunteer_posts | 219 |
| gb_news_1_c0 | news | 525 |
| **total** | | **2846** |

## What changed (all new files, except the route.py edit)

1. **Replacements** `candidates/fix5_candidates.jsonl` (2846 rows). Same text, same card (same `group_id`, `domain`,
   `card_id`, `state`, `instructions`, `qtype`), `id` = old id + `_b2`
   (`c2_gblock:<text_id>:<card_id>_b2`), `card` = `- yes: <yes def>` newline `- no: <no def>` (the replay format).
   Checked with the build's own `Renderer` (decoder_io sha-pinned, style `cygnet`, layout `schema_branch_mark`,
   formats-1 `loader_check`, markers, chunk-item guard, pinned Qwen3.5-4B tokenizer, cap 2,000 tokens) plus: the block
   `Definitions:` / `- yes: ..` / `- no: ..` is printed whole, once, right before the question. Result: 0 failures;
   tokens min / median / max 303 / 571 / 1199 (the `no` line adds 27 / 29 / 41). `candidates/fix5_stats.json`.
2. **Superseded** `candidates/superseded_fix5.json`: the 2846 old ids (`superseded_ids`, `per_card`, `replacement_suffix`,
   the hashes it was made for). The old rows stay in `candidates.jsonl`, `label/key.json`, `label/chunks/` and the Haiku
   answers; their hashes, `label/MANIFEST.json` and `candidates/build_stats.json` are unchanged
   (candidates `37c01d86...`, key `233b0de9...`). The active set is `candidates.jsonl` minus superseded plus
   `fix5_candidates.jsonl`: still 20003 rows, one card per text, unique ids (asserted); card and domain counts unchanged.
3. **Chunks** `label/fix5/chunks/chunk_0000.json` .. `chunk_0056.json` (56 x 50 + 1 x 46 = 2846 items), TEACH-0 format
   `{qid, kind, text, question, definitions}` (all `yes/no`, gold-free, no internal id in any chunk: asserted),
   new opaque qids (`q` + HMAC-SHA256 with their own secret, `gblock|fix5|blind_read|20261013`; asserted disjoint
   from the 29,569 qids of `label/key.json` and `label/opus_queue/key.json`), seeded order that mixes the five domains.
   `label/fix5/key.json` = `{qid: replacement id}` (orchestrator only, never sent to a reader);
   `label/fix5/MANIFEST.json` = chunk, candidates, key and superseded sha256s.
4. **`tools/route.py`** (edited): the exclusion filter.
   - It reads `candidates/superseded_fix5.json` (refuses a file that does not match `candidates.jsonl`) and gives every
     superseded id the status `superseded` before any accept / route / audit decision. So they cannot reach
     `label/accepted_haiku.jsonl` or the Opus queue (`opus_queue/chunks`, `key.json`, `roles.json`); a final assert in
     `main` checks that none did. A chunk holding only superseded ids needs no Haiku answer. `ROUTE.md` counts only the
     live candidates and says how many were superseded.
   - New opt-in flag `--fix5` (default off): adds the `_b2` replacements (inputs verified against
     `label/fix5/MANIFEST.json`; chunk names `fix5/chunk_XXXX`) and reads their Haiku answers from `label/fix5/haiku/`
     (or `--fix5-haiku DIR`). Without `--fix5` the replacements are simply not routed yet.
   - Tested (CPU, in memory / `--dry-run`): with no superseded ids the old logic gives exactly the existing
     `accepted_haiku.jsonl` (10992) and Opus queue (9566); with the filter, accepted = 10992 - 1902 = 9090 and no
     superseded id anywhere; routed rows other than the superseded ones are unchanged; the missing-chunk guard still
     refuses.
5. **`tools/fix5.py`** (new): the deterministic builder of items 1-3 (`--dry-run` writes nothing; idempotent; refuses to
   change `label/fix5/key.json` once fix5 Haiku answers exist unless `--force`).

## What was NOT changed / what the orchestrator must do next

- The existing `label/accepted_haiku.jsonl`, `label/opus_queue/` and `label/ROUTE.md` (written 15:15, provisional: 7
  Haiku chunks still unanswered) were NOT rewritten, to avoid changing a queue that may be in use. They still list the
  superseded ids until `route.py` runs again. The next run replaces them; because the queue key changes it needs
  `--force`.
- Base Haiku chunks still contain the superseded yes-only items; Haiku answers on them (and any not yet read) are
  ignored by `route.py`.
- Reading the replacements: send `label/fix5/chunks/chunk_XXXX.json` to the Haiku readers (TEACH-0 prompt and the
  file-access audit, as for the base chunks), save answers as `label/fix5/haiku/chunk_XXXX.json`
  (`[{qid, answer, confidence}]`), then route with
  `../../../.venv/bin/python tools/route.py --fix5 --force [--haiku label/haiku_merged] [--allow-missing-chunks]`.
  Opus then sees the replacement items through the normal queue (new Opus qids from the `_b2` ids).
- Any step that reads `candidates.jsonl` directly (the later training-row assembly) must drop `superseded_ids` and add
  `fix5_candidates.jsonl`; the id suffix `_b2` marks the replacements.
- Expected yes-share per card will move because the reader now sees the `no` rule; per-domain yes-share (A39 e,
  40-60%) is checked later on the labelled rows, not here.

## Hashes (sha256)

| file | sha256 |
|---|---|
| candidates/candidates.jsonl (unchanged) | 37c01d864062b46ec5b89b0873591daf92ce594dc86d25a8b7c0f9c707c76d49 |
| label/key.json (unchanged) | 233b0de9ced7296755a14627f22def7bed45693043344596c881853d4504fd90 |
| candidates/fix5_candidates.jsonl | 2ad2cd424fcefa50fe7545a185eb776e9e43a29ba6a31a6e3077b8d05b1badbf |
| candidates/superseded_fix5.json | 95b1bf9e0ede4e9bcc38869b681456578a2e33f50e4cc387aaf3f5a888f4e4b3 |
| label/fix5/key.json | 78e5a4a0d3776ef6d6e38bf33489027075f67a4e99e5be227b6e8708cf3a77af |
| label/fix5/MANIFEST.json | 1d6b790a32213eb6a4f43d3ce595839a1ca65b73e58e26e4c57b86ba9f55c9be |

## Route run with the fix5 answers (13 Oct 2026, orchestrator decisions)

Decisions (orchestrator):
1. The six base chunks chunk_0016, chunk_0102, chunk_0180, chunk_0197, chunk_0205 and chunk_0390 PASSED the file-access
   audit (each agent read only its own chunk, some in two pages, and wrote its own answer file; the earlier failure was a
   string-match false positive). Their 300 answers are included. The provisional merged file of 15:15 (19,632 rows) had
   left them out.
2. chunk_0252 was refused by the Haiku AUP filter. It has no answer file, so its 40 live items go to Opus.
3. fix5 chunks that failed the audit: the list is empty ([]), so no fix5 answer was discarded. All 57 fix5 files are used
   as written. Route was not re-run for this decision.

Inputs:
- `label/haiku_merged/answers_all.json`: 19,932 rows from the 400 base answer files (`{qid, answer, confidence, chunk}`).
  Checked: 0 conflicts, 0 qids outside their own chunk, 0 duplicate qids. Unanswered: chunk_0252 (no file, 50 items) and
  chunk_0054 (29 of 50 answered, 21 unanswered). Replaces the provisional 19,632-row file.
- `label/fix5/haiku/chunk_0000.json` .. `chunk_0056.json`: 57 files, 2,838 answers, every qid inside its own chunk, 0
  duplicates. Full coverage for 55 chunks; chunk_0008 49 of 50 and chunk_0023 43 of 50 (8 unanswered). No file was
  changed.

Route (run once): `tools/route.py --fix5 --force --haiku label/haiku_merged --allow-missing-chunks`, exit 0, problems 0.

Final counts:
- Live candidates: 20,003 (17,157 base not superseded + 2,846 `_b2` replacements). Superseded excluded: 2,846.
- Accepted (Haiku confidence >= 0.80): 11,200 (56.0%); base 9,225, fix5 1,975.
- Routed to Opus: 8,803 = low confidence 8,733 + invalid 4 (choice answer not in the options, all base) + missing 66
  (base 58 = chunk_0252 40 + chunk_0054 18; fix5 8 = chunk_0023 7 + chunk_0008 1).
- Audit sample (5% of accepted rows, ceil per domain, read by Opus): 565 (base 462, fix5 103).
- Opus queue: 9,368 items in 188 chunks (`label/opus_queue/chunks/`) = 8,803 routed + 565 audit; 974 fix5 `_b2` items and
  8,394 base items. Replaces the provisional queue (9,566 items, 192 chunks) with --force.
- Superseded ids remaining: 0 in `label/accepted_haiku.jsonl`, 0 in `label/opus_queue/key.json`, 0 in `roles.json`.
- Every live candidate is in exactly one of: accepted, or the Opus queue as routed (accepted and routed do not overlap).

Not changed: `label/haiku/answers_all.json` (provisional, 15:15, 19,632 rows) still exists and was not rewritten. Do not use
it as a route input; this run used `label/haiku_merged` only. Items still open for Opus: chunk_0252 (40 live), chunk_0054
(18 live), fix5 chunk_0023 (7) and chunk_0008 (1), plus the 3-item final chunk is fully answered.
