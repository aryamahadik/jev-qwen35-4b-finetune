# Option-order drift test (dev only, 30 Sep 2026, 4B-E, Google L4)

**Question (Codex + projection):** does 4B-E change its answer when the options are reordered? Does a 2-view read
(normal + reversed order, averaged, which is decoder_io's tta_choice) fix it without hurting accuracy?

**Data:**
- All 3,814 choice rows of 8 dev splits.
- Twins are made like OHS-3's: reversed, or rotated by a seeded k (seed "drift20260930").
- **No OHS data was used.**

**Reads:**
- existing identity and 2-view reads (preds_*/q35_4b_pxE_parity and _tta);
- new rotated and rotated-2-view reads (drift/drift_read.py, outputs in drift/out/).

The reversed single read is derived as 2·tta − identity. Analysis: drift/analyze_drift.py. Full table:
drift/drift_result.txt.

| | Single read | 2-view read |
|---|---|---|
| Accuracy (3,814 dev choice rows) | 76.40 | 76.51 (+0.11) |
| Drift, reversed twins | 8.23% | 0.00% (by construction) |
| Drift, rotated twins | 7.37% | 3.72% |
| **OHS-3 mix (149 reversed + 155 rotated)** | **7.79%** | **1.90%** |
| Drift at 10+ options | 17.2% | 5.0% |

**Jev's noise floor:**
- Jev's run-to-run argmax disagreement on identical inputs is 1.14-1.98% on OHS-1/2. This is a lower bound on its
  drift.
- The 2-view read therefore puts us at about Jev's floor. The single read is about 4x worse.

**Cost of the fix:**
- About 2x compute on choice rows, and yes/no stays 1 read. On JevBench that is about 1.6x tokens.
- On the cost formula that moves $0.0245 to about $0.039 per 1K, the same as Jev's $0.038, and costs about 2-3
  Score A points.
- Prefix caching (both views share the state and the question) could cut the real compute cost. **Test that before
  deciding.**

**Decision:** needed before OHS-3, and it must be pre-registered as a PREREG amendment. Options:
- (a) 2-view read for OHS-3: consistency ≈ Jev, cost and speed still likely ahead with direct hosting;
- (b) a single read everywhere: cheapest, but loses consistency;
- (c) 2-view only where drift is large.

Never choose the read on OHS-3 results.
