"""Orchestration of a T42c build (CPU/dry-run side): plan units -> generate specs (+ pair partners) -> Solver A -> rows.

`build_rows` is what the 1,000-row pilot and the full run call after the freeze and the row-start guard. Here it is only
ever called with a SimExecutor in tests / the dry run. It never writes rows to disk.
"""
import collections
import random

from . import config as C
from . import out4, eqv2, tfail2
from . import rows as ROWS
from .base import Skip
from .planner import Planner
from .solver_a import SolverA

GEN = {"OUT4": (out4.gen_out4, out4.make_pair), "EQV2": (eqv2.gen_eqv2, eqv2.make_pair), "TFAIL2": (tfail2.gen_tfail2, tfail2.make_pair)}


def make_specs(cell, tries=10, skips=None, planner=None):
    out = _make_specs(cell, tries, skips, planner)
    if planner is not None:
        planner.note_result(cell, bool(out))
    return out


def _make_specs(cell, tries, skips, planner):
    gen, pair = GEN[cell["head"]]
    for k in range(tries):
        seed = "%d.%d" % (cell["seed"], k)
        try:
            spec = gen(cell, seed)
            spec["group"] = spec["lo"]["id"]
            if cell["unit"] == "single":
                if planner is not None and not planner.bal_ok(spec):
                    raise Skip("balance cell full")
                return [spec]
            partner = pair(spec, cell["unit"], seed)
            partner["group"] = spec["group"]
            pid = "p%s" % cell["seed"]
            spec["meta"] = dict(spec["meta"], pair_id=pid, pair_kind=cell["unit"])
            partner["meta"] = dict(partner["meta"], pair_id=pid, pair_kind=cell["unit"])
            if planner is not None and not (planner.bal_ok(spec) and planner.bal_ok(partner)):
                raise Skip("balance cell full")
            return [spec, partner]
        except Skip as e:
            if skips is not None:
                skips[cell["head"] + ":" + str(e)[:48]] += 1
    return []


def build_rows(n_target, executor, picker, seed=0, chunk=20, ts_ok=True, max_chunks=400, perm_share=C.ORDER_INVARIANCE_COPIES, checker=None):
    planner = Planner(seed, ts_ok)
    solver = SolverA(executor, picker, checker)
    rows, skips, n_ids = [], collections.Counter(), 0
    chunks = 0
    while len(rows) < n_target and chunks < max_chunks:
        chunks += 1
        specs = []
        for _ in range(chunk):
            new = make_specs(planner.unit(), skips=skips, planner=planner)
            planner.reserve(new)                       # in-flight specs count toward the quotas immediately
            specs += new
        for s in specs:
            s["row_id"] = "T42c-%s-%06d" % (s["head"], n_ids)
            n_ids += 1
        new_rows, _ = solver.run(specs)
        planner.settle(specs, new_rows)
        rows += new_rows
    for sig, k in planner.starved.items():
        skips["STARVED:" + "/".join(str(x) for x in sig)] += k
    rows = rows[:max(n_target, 0)] if len(rows) > n_target else rows
    n_rows_before_copies = len(rows)
    rng = random.Random("T42c-perm:%s" % seed)
    out4_rows = [r for r in rows if r["head"] == "OUT4"]
    rng.shuffle(out4_rows)
    for r in out4_rows[:int(round(perm_share * len(out4_rows)))]:
        rows.append(ROWS.permuted_row(r, rng, "T42c-OUT4-%06d" % n_ids, picker))
        n_ids += 1
    eq = [r for r in rows if r["head"] == "EQV2" and not r["meta"].get("perm_copy")]
    rng.shuffle(eq)
    for r in eq[:int(round(perm_share * len(eq)))]:
        rows.append(ROWS.reversed_row(r, "T42c-EQV2-%06d" % n_ids, picker))
        n_ids += 1
    if checker is not None:                                    # the order-invariance copies are rows too: checked and stamped when made
        copies = rows[n_rows_before_copies:]
        rows = rows[:n_rows_before_copies] + checker.filter(copies)
    return rows, solver.log, skips
