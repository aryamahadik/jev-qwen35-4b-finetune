"""SOLVER A for T66: labels from the EXECUTION WITNESSES stored in the record (MERGE, SEMVER) or from the construction (MSG). Solver B is a separate program that
re-executes the rendered row (ROW_SCHEMA.md).

  MERGE   YES iff both side suites pass on the resolved file in 3 identical runs (merge_spec.label_from_witness)
  SEMVER  BREAKING iff the shown callers all pass on the old API and at least one fails on the new API in 3 identical runs (semver.label_from_witness)
  MSG     YES iff the message is the diff's own; NO iff it is another change spec's message or a trivial hunk's message; the NO constraints are re-checked here
          (>= 4 tokens, token Jaccard < 0.5 against the true message)
"""
from . import merge_spec as MS, msg_spec as MSG, semver as SV


def gold_a(rec):
    spec = rec["spec"]
    head = spec["head"]
    if head == "MERGE":
        return MS.label_from_witness(spec["witness"])
    if head == "SEMVER":
        return SV.label_from_witness(spec["witness"])
    if len(spec["message"].split()) < 4:                  # Opus ruling Q8 R5: every message has >= 4 tokens, YES included (a true message must be usable as a swap)
        return None
    if spec["origin"] == "own":
        return "YES"
    own = rec["manifest"].get("own_message")
    if len(spec["message"].split()) < 4:
        return None
    if own is not None and MSG.jaccard(spec["message"], own) >= 0.5:
        return None
    return "NO"
