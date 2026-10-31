"""Generation-time answer-check hook (owner rule 18 Oct). `check_row(row, packages)` runs solver B on one fresh row; a row on which B
disagrees, refuses, or whose shown diff does not apply to the pristine tree is dropped with a reason class (no item text).
`check_batch` applies the T56g block rule (more than 3% dropped for disagreement returns the block; G0-lite K2)."""
from LC_SOLVER_B import agreelib

from .. import schema
from .solve import solve

BLOCK_DROP_LIMIT = 0.03


def check_row(row, packages):
    out = solve(schema.b_view(row, packages))
    st = out["status"]
    if st == "ok" and out["label"] == row["label"]:
        return {"row_id": row["row_id"], "keep": True, "reason": None, "b_label": out["label"]}
    if st == "ok":
        return {"row_id": row["row_id"], "keep": False, "reason": "B_label_differs", "b_label": out["label"]}
    return {"row_id": row["row_id"], "keep": False, "reason": "B_%s:%s" % (st, agreelib.why_class(out["evidence"].get("why"))), "b_label": None}


def check_batch(rows, packages):
    return agreelib.batch_verdict([check_row(r, packages) for r in rows], BLOCK_DROP_LIMIT)
