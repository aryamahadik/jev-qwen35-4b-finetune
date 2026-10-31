"""T42c Solver B. Input: schema.b_view(row) (carriers + witness_inputs, no label). Output per ROW_SCHEMA.md section 1.

Method (differs from solver A, which labels from sandbox witnesses / the IR interpreter): own parser + own evaluator per language
(LC_SOLVER_B), an own domain enumerator for EQV2 (the whole declared domain, first differing point reported), an own option matcher
for OUT4 (the observable is rendered to the per-language option text and compared with the OPTIONS lines), and an own test runner
model for TFAIL2.  B reports `status` 'ok' or 'unsupported'/'timeout'/'unmatched' - those are NEVER labels and are counted apart.
"""
import itertools

from LC_SOLVER_B import langs
from LC_SOLVER_B.common import Budget, Timeout, Unsupported, match_option


def _files(lang, blocks):
    return {b["path"]: b["text"] for b in blocks}


# ------------------------------------------------------------------------------------------------ OUT4
def solve_out4(view):
    lang = view["lang"]
    car = view["carriers"]
    wi = view["witness_inputs"]
    files = _files(lang, car["SRC_FILE"])
    prog = langs.program(lang, files, Budget(3_000_000))
    inst = None
    created = False
    outs = []
    for c in wi["calls"]:
        if not created:
            inst = prog.fresh(c["fn"])
            created = True
        r = prog.invoke(inst, c["fn"], c["args"])
        outs.append(r)
    last = outs[-1]
    early = [o for o in outs[:-1] if o[0] == "exc"]
    res = {"row_id": view["row_id"], "runs": 1, "observable": {last[0]: last[1]}, "evidence": {"calls": len(outs)}}
    st, letter = match_option(lang, last, car["OPTIONS"], wi.get("ret_type"))
    if early:
        # ROW_SCHEMA: "Earlier calls must succeed". The rendered CALL_SPEC has no guard, so a real run would stop at the first
        # failing call. B refuses to label (contract breach) and keeps the label the guarded reading would give, for diagnosis.
        res["status"] = "prefix_failed"
        res["label"] = None
        res["evidence"]["guarded_label"] = letter
        res["evidence"]["early_exc"] = [o[1] for o in early]
        return res
    res["status"] = "ok" if st == "ok" else "unmatched_" + st
    res["label"] = letter
    return res


# ------------------------------------------------------------------------------------------------ EQV2
def _param_values(p):
    t = p["t"]
    if t in ("int", "str"):
        return list(p["vals"])
    if t == "bool":
        return [False, True]
    if t in ("ints", "strs"):
        out = []
        for ln in range(0, p["maxlen"] + 1):
            for tup in itertools.product(p["elem"], repeat=ln):
                out.append(list(tup))
        return out
    raise Unsupported("param type " + t)


def _enumerate_points(wi):
    dom = wi["domain"]
    if wi["mode"] == "pure":
        lists = [_param_values(p) for p in dom]
        for tup in itertools.product(*lists):
            yield [list(x) if isinstance(x, list) else x for x in tup]
        return
    # seq: every call sequence of length 0..maxlen over the operations
    elems = []
    for op in dom["ops"]:
        lists = [_param_values(p) for p in op["params"]]
        for tup in itertools.product(*lists):
            elems.append({"fn": op["fn"], "args": [list(x) if isinstance(x, list) else x for x in tup]})
    for ln in range(0, dom["maxlen"] + 1):
        for seq in itertools.product(elems, repeat=ln):
            yield list(seq)


def _observe(prog, wi, point):
    if wi["mode"] == "pure":
        inst = prog.fresh(wi["function"])
        return [prog.invoke(inst, wi["function"], point)]
    inst = None
    created = False
    outs = []
    for c in point:
        if not created:
            inst = prog.fresh(c["fn"])
            created = True
        outs.append(prog.invoke(inst, c["fn"], c["args"]))
    if wi.get("snapshot"):
        if not created:
            inst = prog.fresh(wi["snapshot"])
        outs.append(prog.invoke(inst, wi["snapshot"], []))
    return outs


def solve_eqv2(view):
    lang = view["lang"]
    wi = view["witness_inputs"]
    pa, pb = view["carriers"]["PROGRAM_PAIR"]
    progs = [langs.program(lang, _files(lang, p["blocks"]), Budget(40_000_000)) for p in (pa, pb)]
    n = 0
    first = None
    for pt in _enumerate_points(wi):
        n += 1
        oa = _observe(progs[0], wi, pt)
        ob = _observe(progs[1], wi, pt)
        if oa != ob:
            first = {"point": pt, "a": oa, "b": ob}
            break
    return {"row_id": view["row_id"], "status": "ok", "label": "NO" if first else "YES",
            "distinguishing": first["point"] if first else None, "points": n, "runs": 1,
            "evidence": {"first_diff": first}}


# ------------------------------------------------------------------------------------------------ TFAIL2
def solve_tfail2(view):
    lang = view["lang"]
    car = view["carriers"]
    wi = view["witness_inputs"]
    files = _files(lang, car["SRC_FILE"])
    t = car["TEST_FILE"]
    files[t["path"]] = t["text"]
    res = langs.run_tests(lang, files, only=[wi["test_path"]], mode="plain" if lang == "python" else "native",
                          budget=Budget(6_000_000))
    failed = res["exit"] != 0 or any(o in ("failed", "error") for o in res["outcomes"].values())
    return {"row_id": view["row_id"], "status": "ok", "label": "YES" if failed else "NO", "runs": 1,
            "evidence": {"outcomes": res["outcomes"], "exit": res["exit"]}}


def solve(view):
    head = view["head"]
    try:
        if head == "OUT4":
            return solve_out4(view)
        if head == "EQV2":
            return solve_eqv2(view)
        if head == "TFAIL2":
            return solve_tfail2(view)
        raise Unsupported("head " + head)
    except Unsupported as e:
        return {"row_id": view["row_id"], "status": "unsupported", "label": None, "evidence": {"why": str(e)[:200]}}
    except Timeout as e:
        return {"row_id": view["row_id"], "status": "timeout", "label": None, "evidence": {"why": str(e)[:200]}}
