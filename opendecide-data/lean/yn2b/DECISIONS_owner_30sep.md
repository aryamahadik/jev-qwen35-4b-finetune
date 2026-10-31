# Owner decisions on yn2b (30 Sep 2026, about 20:50 UTC)

These override SPEC section 10 where they differ.

- **D4, delay:** ACCEPTED. The 2B main run is about 4 Oct and final results about 6 Oct.
- **D3, teacher: CHANGED from the SPEC.** The teacher is the best 4B, decided BEFORE arm A trains.
  - If the new 500K 4B passes the ship gate vs 4B-E, it relabels the same 422,044 rows on Modal (about $16-20,
    about 3 h). build_2b_kd.py is rerun and arm A's control file is rebuilt from the new labels.
  - Otherwise the 4B-E labels (train_2b_golden_kd.jsonl, built 30 Sep) are used.
  - Every arm (A, B, C) and the 2B main run use the same teacher, so the A/B stays valid.
  - Consequence: arm A waits for the gate (about 1 Oct evening). It is not on the critical path.
- **D1, arm C (teacher gate on exact-label generator rows):** RUN IT. It is adopted only under the SPEC 11.6 rule.
- **Where the A/B arms run:** the Google L4 first (free credit). Modal H100 is the fallback if the L4 is stocked out
  or too slow for the timeline. A second L4 VM may be used to run arms in parallel if quota allows.
- **D2, PRISM-X I override:** already decided by the owner (30 Sep 12:30 UTC). The A2 text is committed before
  arm A.
- **GO is still required** for each GPU step: the 2B smoke, the arms, the reads, the relabel and the 2B main run.
