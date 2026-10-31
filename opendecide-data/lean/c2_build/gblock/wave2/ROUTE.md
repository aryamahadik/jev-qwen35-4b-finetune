# G-block wave 2: Haiku keep/queue route

PREREG_FINAL Ruling A40 (c), steps 1 and 3 sampling. Generated from `route/route_stats.json`; gold never edited.
Opus reads have NOT been run. They wait for the Mon 19 Oct reset (A39 g, A41 a).

## Rules applied

- **Keep** (A40 c.1): Haiku's answer equals the program gold AND Haiku confidence >= 0.80.
- **Queue** for the blind Opus read (A40 c.2), one reason per item, first match wins:
  - `missing`: no usable Haiku verdict (qid not answered, or chunk has no Haiku output).
  - `invalid`: answer not an allowed label, confidence not a number in [0, 1], or a duplicate qid.
  - `disagree`: valid answer != gold (any confidence).
  - `low_confidence`: valid answer == gold, confidence < 0.80.
- **Audit** (A40 c.3): per type, round(5% x kept) of kept items, chosen by seeded hash (seed 20261013), sent to Opus as role `audit`. The per-domain 6% re-read rule is applied after the Opus audit reads.
- **chunk_129**: the orchestrator marks its audit as failed and it has no Haiku output. Its Haiku answers are not used, so its 50 items are treated as `missing` and queued. They are not dropped and not kept.
- **Agreement rate** = valid Haiku answers equal to gold / valid Haiku answers. The second rate restricts to confidence >= 0.80.

## Counts per type

| Type | Task | Candidates | Valid answers | Agreement | Agreement (conf >= 0.80) | Kept | Keep rate | Queued: missing | invalid | disagree | low_conf | Queued total | Audit (of kept) | Opus items |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| W1 | injection | 1716 | 1709 | 99.8% | 100.0% | 1639 | 95.5% | 7 | 0 | 4 | 66 | 77 | 82 | 159 |
| W2 | pii | 1710 | 1699 | 99.9% | 100.0% | 1656 | 96.8% | 11 | 0 | 1 | 42 | 54 | 83 | 137 |
| W3 | rag_faithfulness | 1704 | 1695 | 99.8% | 99.9% | 1664 | 97.7% | 9 | 0 | 3 | 28 | 40 | 83 | 123 |
| W4 | off_topic | 1800 | 1789 | 99.1% | 99.9% | 1619 | 89.9% | 11 | 0 | 17 | 153 | 181 | 81 | 262 |
| W5 | search_relevance | 1724 | 1713 | 82.1% | 95.7% | 747 | 43.3% | 11 | 0 | 307 | 659 | 977 | 37 | 1014 |
| W6 | commit_type | 1692 | 1680 | 64.8% | 82.2% | 332 | 19.6% | 11 | 1 | 592 | 756 | 1360 | 17 | 1377 |
| W7 | tool_routing | 1486 | 1479 | 99.7% | 99.9% | 1416 | 95.3% | 7 | 0 | 5 | 58 | 70 | 71 | 141 |
| **all** | | **11832** | **11764** | **92.1%** | **98.8%** | **9073** | **76.7%** | **67** | **1** | **929** | **1762** | **2759** | **454** | **3213** |

Counts of raw Haiku answers equal to gold (valid answers only):

- W1: 1705 of 1709
- W2: 1698 of 1699
- W3: 1692 of 1695
- W4: 1772 of 1789
- W5: 1406 of 1713
- W6: 1088 of 1680
- W7: 1474 of 1479
- all: 10835 of 11764

## Integrity

- Candidates: 11832; verify chunks: 237; chunk sizes 50 (last 32). `candidates.jsonl` and `key.json` match the verify manifest hashes.
- Kept 9073 + queued 2759 = 11832 (asserted in the script).
- Haiku entries: malformed 0, foreign or misplaced qids 1 (ignored; the real item is counted as `missing`). Haiku chunk status not ok: {'chunk_129.json': 'audit failed (orchestrator instruction): no Haiku output'}.
- Opus queue: 3213 items = 2759 queued + 454 audit, in 65 gold-free TEACH-0 chunks (last chunk 13 items).
- Audit by type (kept, 5% stratified): W1 82, W2 83, W3 83, W4 81, W5 37, W6 17, W7 71.

## Files

- `kept_haiku.jsonl`: the kept candidate rows, unchanged from `candidates/candidates.jsonl`.
- `kept_haiku_provenance.jsonl`: per kept row, the Haiku answer and confidence, the gold label, and whether it is in the Opus audit.
- `opus_queue/chunk_NNN.json`: gold-free TEACH-0 chunks (qid, kind, text, question, options, definitions). `opus_queue/key.json` maps each new qid to its row id, type and gold (scoring only). `opus_queue/roles.json` gives role (queued / audit), reason and the Haiku verdict. `opus_queue/manifest.json` holds the hashes.
- `route/decisions.jsonl`: one decision per candidate. `route/route_stats.json`: the counts above.

