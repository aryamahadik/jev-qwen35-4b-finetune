"""One small in-memory harness run (generator side, CPU, nothing written) and the pipeline wiring check."""
import os

import pytest

from T67.solver_b import agree, hook


def test_small_harness_run_meets_the_bar():
    stats, classes, why, _ = agree.run(40, [5])
    allc = stats[("ALL", "ALL")]
    assert allc["labelled"] >= 40
    assert allc["agree"] >= 0.99 * allc["labelled"], dict(classes)
    for key in ("PLAN_JSON", "K8S_MANIFEST", "CI_WORKFLOW"):
        assert stats[("T67-GATE", key)]["rows"] > 0
    # abstain only ever comes from the R10 statements
    assert all("R10" in k[3] for k in why), dict(why)


def test_the_hook_plugs_into_the_family_adapter_and_check_row():
    from LP_COMMON import pipeline as pl
    from T67 import checked, generator
    import json
    with open(agree.POOL) as fh:
        pool = json.load(fh)
    ctx = generator.Ctx(seed=3, standin=True, pool=pool)
    ad = checked.adapter(ctx.lock_table, solver_b=hook.solver_b)
    assert ad.solver_b is hook.solver_b
    plan = list(generator.build_plan(total=30, seed=3))
    seen = 0
    for g in plan[:20]:
        for rec in generator.generate_group(ctx, g):
            reasons, notes = pl.check_row(rec, ad)
            assert "B_error" not in reasons and "A_B_label_differs" not in reasons, reasons
            seen += 1
    assert seen > 10
