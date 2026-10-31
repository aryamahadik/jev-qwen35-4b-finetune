"""Generation-time answer-check hook (owner rule 18 Oct: "check that row at that same point").

`check_row(row)` runs solver B on one freshly generated row and says whether B reproduces the label A set. A row for which B
disagrees, refuses (unsupported / timeout / unmatched option) or breaches the contract (earlier OUT4 call raises) is NOT kept:
the stamp wrapper calls this before G13 and drops the row with the returned reason class (no item text). `check_batch` applies
the G0-lite block rule (T42c-K3: more than 2% dropped for disagreement returns the block to the generator).
"""
from LC_SOLVER_B import agreelib

from .. import schema
from . import crosschecks as X
from .solve import solve

BLOCK_DROP_LIMIT = 0.02


def _prose_ok(row):
    """B's own parse of the PROSE carriers must agree with the structured inputs it evaluates: the CALL_SPEC text must name the
    witness calls (OUT4) and the DOMAIN_DECL text must be the witness domain (EQV2); a YES pair must not be two identical programs.
    Returns a reason class or None. A parser limit counts as a failure here (the row is dropped, never waved through)."""
    try:
        if row["head"] == "OUT4":
            if not X.callspec_matches(row["lang"], row["carriers"]["CALL_SPEC"], row["witness_inputs"]):
                return "call_spec_differs_from_witness_calls"
        elif row["head"] == "EQV2":
            if not X.domain_matches(X.domain_from_text(row["carriers"]["DOMAIN_DECL"]), row["witness_inputs"]):
                return "domain_text_differs_from_witness_domain"
            pa, pb = row["carriers"]["PROGRAM_PAIR"]
            if row["label"] == "YES" and pa["blocks"] == pb["blocks"]:
                return "yes_pair_programs_identical"
    except Exception as e:                                   # noqa: BLE001 - class name only, no text
        return "prose_parse_" + type(e).__name__
    return None


def check_row(row):
    out = solve(schema.b_view(row))
    st = out["status"]
    if st == "ok" and out["label"] == row["label"]:
        bad = _prose_ok(row)
        if bad:
            return {"row_id": row["row_id"], "keep": False, "reason": "B_prose_" + bad, "b_label": out["label"]}
        return {"row_id": row["row_id"], "keep": True, "reason": None, "b_label": out["label"]}
    if st == "ok":
        return {"row_id": row["row_id"], "keep": False, "reason": "B_label_differs", "b_label": out["label"]}
    return {"row_id": row["row_id"], "keep": False, "reason": "B_%s:%s" % (st, agreelib.why_class(out["evidence"].get("why"))), "b_label": None}


def check_batch(rows):
    return agreelib.batch_verdict([check_row(r) for r in rows], BLOCK_DROP_LIMIT)
