"""GEN solver B: entry point.

    from b_main import solve_row
    out = solve_row({"form": ..., "k": ..., "carrier": ..., "stem": ..., "options": [...]})

Input: ONLY the fields a reader of the final prompt has (form id, option count, carrier id, stem, options). No spec, no label.
Output: {"status": "ok", "answer_index", "answer_text", "answer_letter", "parse", "info"}
     or {"status": "parse_fail" | "reject", "code", "detail"}.
B imports nothing from solver A. Standard library only.
"""
import b_arith
import b_causal
import b_logic
import b_table
import b_temporal
from bcommon import ParseFail, Reject

BLOCKS = {
    "AR-F1": b_arith, "AR-F2": b_arith, "AR-F3": b_arith,
    "LG-L1": b_logic, "LG-L2": b_logic, "LG-L3": b_logic, "LG-L4": b_logic,
    "CA-C1": b_causal, "CA-C2": b_causal, "CA-C3": b_causal, "CA-C4": b_causal, "CA-C5": b_causal,
    "TM-T1": b_temporal, "TM-T2": b_temporal, "TM-T3": b_temporal, "TM-T4": b_temporal,
    "TB-B1": b_table, "TB-B2": b_table, "TB-B3": b_table, "TB-B4": b_table,
}
FORM_K = {"AR-F1": 4, "AR-F2": 2, "AR-F3": 4, "LG-L1": 3, "LG-L2": 4, "LG-L3": 4, "LG-L4": 2, "CA-C1": 4, "CA-C2": 4, "CA-C3": 4, "CA-C4": 4,
          "CA-C5": 2, "TM-T1": 4, "TM-T2": 4, "TM-T3": 4, "TM-T4": 2, "TB-B1": 4, "TB-B2": 4, "TB-B3": 4, "TB-B4": 2}


def solve_row(view):
    form = view["form"]
    opts = list(view["options"])
    try:
        mod = BLOCKS.get(form)
        if mod is None:
            raise ParseFail("unknown_form", str(form))
        if len(opts) != FORM_K[form] or len(set(o.strip() for o in opts)) != len(opts):
            raise ParseFail("option_list_shape", "%d options" % len(opts))
        if mod is b_table:
            out = mod.solve(form, view["stem"], opts, carrier=view.get("carrier"))
        else:
            out = mod.solve(form, view["stem"], opts)
        out = dict(out)
        out["status"] = "ok"
        out["answer_letter"] = "ABCD"[out["answer_index"]]
        return out
    except ParseFail as e:
        return {"status": "parse_fail", "code": e.code, "detail": e.detail}
    except Reject as e:
        return {"status": "reject", "code": e.code, "detail": e.detail}
    except Exception as e:   # a crash is a B defect and is counted as its own class by the harness
        return {"status": "b_error", "code": type(e).__name__, "detail": str(e)[:200]}
