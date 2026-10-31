"""Plug points for the T63 pipeline. `solver_b(bview)` takes ONLY schema.b_view(rec) and returns
{"status": "ok"|"abstain"|"error", "label": ..., "letter": ..., "reason": ...}. Wire it as `checked.adapter(..., solver_b=hook.solver_b)` or
`checked.run(..., solver_b=hook.make_solver_b(exports=..., table=...))`.

Sources B cannot rebuild from the row (G0-lite 2.2 / 2.3) are passed in as PLAIN DATA, never read from a file by B:
  exports   {"python": {module: [names]}, "node": {...}, "go": {...}}  (the sha-bound L-0 image-record stdlib export; public names), with export_sha its sha
  table     {(dep_id, project_id, "LC-USE-n", "LC-DIST-n"): "COMPATIBLE"|"REVIEW"|"INCOMPATIBLE"} (the hashed T63-LIC-TABLE), with table_sha
EX-B1, EX-B2 and LIC rows REQUIRE their source AND its sha (Opus ruling Q3a, 18 Oct): source missing, sha not configured, a witness without a sha, a
different sha, or a FIXTURE source -> abstain (reasons no_export_source / no_table_source / no_export_sha / no_table_sha / witness_*_sha_missing /
*_sha_mismatch / fixture_*_source). `fixture=True` declares the sources non-production; they are then refused unless `allow_fixture=True` (the
build-stage CPU harness only: K1 on fixtures is build-stage evidence, not production evidence), and the result carries "fixture": True.
NEAR, EX-A1 and EX-A2 need no source."""
from . import exists_b, lic_b, near_b
from .common import Abstain, abstain, letter_for, ok

_STATE = {"exports": None, "export_sha": None, "table": None, "table_sha": None, "fixture": False, "allow_fixture": False}


def configure(exports=None, export_sha=None, table=None, table_sha=None, fixture=False, allow_fixture=False):
    """Set the module-level sources used by `solver_b`. Passing nothing clears them."""
    _STATE.update(exports=exports, export_sha=export_sha, table=table, table_sha=table_sha, fixture=fixture, allow_fixture=allow_fixture)


def _dispatch(bview, exports, export_sha, table, table_sha, fixture, allow_fixture):
    head, sub = bview["head"], bview["sub_block"]
    if head == "NEAR" and sub == "NEAR":
        return near_b.solve(bview)
    if head == "EXISTS":
        if sub == "EX-A1":
            return exists_b.solve_a1(bview)
        if sub == "EX-A2":
            return exists_b.solve_a2(bview)
        if sub == "EX-B1":
            return exists_b.solve_b1(bview, exports, export_sha, fixture, allow_fixture)
        if sub == "EX-B2":
            return exists_b.solve_b2(bview, exports, export_sha, fixture, allow_fixture)
    if head == "LIC" and sub == "LIC":
        return lic_b.solve(bview, table, table_sha, fixture, allow_fixture)
    raise Abstain("unknown_block")


def evaluate(bview, exports=None, export_sha=None, table=None, table_sha=None, fixture=False, allow_fixture=False):
    try:
        label, reason = _dispatch(bview, exports, export_sha, table, table_sha, fixture, allow_fixture)
        extra = {}
        if bview.get("sub_block") == "EX-B1":
            extra["xcheck"] = exists_b.b1_export_crosscheck(bview, label, exports)
        if fixture and bview.get("sub_block") in ("EX-B1", "EX-B2", "LIC"):
            extra["fixture"] = True
        return ok(label, letter_for(label, bview), reason, **extra)
    except Abstain as e:
        return abstain(e.reason)
    except Exception as e:                                                # noqa: BLE001 - a parser crash is an error, never a guessed label
        return {"status": "error", "label": None, "letter": None, "reason": "crash:" + type(e).__name__}


def table_from_label_fn(label_fn, deps, projects):
    """Plain table {(dep, project, "LC-USE-n", "LC-DIST-n"): label} from any callable label_fn(dep, project, usage_id, distribution_id) -> label
    (for example the loaded hashed table's lookup). Cells the callable refuses (KeyError / ValueError) are left out, so B abstains on them."""
    out = {}
    for d in deps:
        for p in projects:
            for u in range(1, 6):
                for s in range(1, 4):
                    try:
                        out[(d, p, "LC-USE-%d" % u, "LC-DIST-%d" % s)] = label_fn(d, p, "LC-USE-%d" % u, "LC-DIST-%d" % s)
                    except (KeyError, ValueError):
                        pass
    return out


def make_solver_b(exports=None, export_sha=None, table=None, table_sha=None, fixture=False, allow_fixture=False):
    def solver_b(bview):
        return evaluate(bview, exports, export_sha, table, table_sha, fixture, allow_fixture)
    return solver_b


def solver_b(bview):
    """Module-level plug point (uses the sources set by `configure`)."""
    return evaluate(bview, _STATE["exports"], _STATE["export_sha"], _STATE["table"], _STATE["table_sha"], _STATE["fixture"], _STATE["allow_fixture"])
