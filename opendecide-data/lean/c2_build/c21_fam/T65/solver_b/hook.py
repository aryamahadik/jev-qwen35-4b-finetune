"""Plug point for the T65 pipeline: `checked.adapter(solver_b=hook.solver_b)` / `checked.run(..., solver_b=hook.solver_b)`.
solver_b(bview) -> {"status": "ok" | "abstain" | "error", "label": "YES" | "NO" | <class word> | None, "letter": ..., "cls": ..., "reason": ...}
The pipeline reads only status and label. B touches only the b-view fields (row_id, head, sub_block, rendered, options, witness_inputs)."""
from .solver import solve


def solver_b(bview):
    try:
        return solve(bview)
    except Exception as e:                       # noqa: BLE001 - a crash is an "error", never a guessed label
        return {"status": "error", "label": None, "letter": None, "cls": None, "reason": "%s" % type(e).__name__}
