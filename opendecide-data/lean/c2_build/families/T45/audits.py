"""families/T45/audits.py: the A42-D 3.3 reseed audit, the surface-name audit and the held-out-fault check of T45.

  reseed_audit(plugin, ctx, specs, frac, seed)   a seeded `frac` of the specs is regenerated from the same row spec
                                                 (qform, kind, fault, shown set, gold, pack, legend) with an independent seed
                                                 (new execution parameters, new surface draw, new padding, new option draw);
                                                 label flips are counted (bar: <= 1%; with < 100 audited rows: 0).
  name_audit(plugin, specs, n)                   re-executes `n` specs with the SURFACE names in place of the canonical
                                                 ones (real branch / table / file names): the executed answer must be
                                                 unchanged (the surface renaming cannot move a label).
  heldout_check(plugin, n)                       the training samplers never draw the held-out fault type; S5 does.
"""
from __future__ import annotations

import random

from . import executor as E
from . import scenarios as SC


def reseed_audit(plugin, ctx, specs, frac: float = 0.03, seed: int = 20261015) -> dict:
    R = random.Random(seed)
    k = max(1, int(round(frac * len(specs))))
    pick = R.sample(range(len(specs)), min(k, len(specs)))
    flips, errs, b_flips = [], [], []
    for i in pick:
        sp = specs[i]
        st = sp.structure
        key = f"reseed|{sp.seed}|{sp.sampler}|{i}"
        ok = False
        for attempt in range(6):
            p = SC.exec_params(random.Random(f"{key}|{attempt}"), st["kind"], st["fault"])
            p["variant"] = st["params"]["variant"] if st["fault"] == "error_body" else p["variant"]
            try:
                c = E.classify(E.run_exec(st["kind"], p))
            except E.ExecError as e:
                errs.append(str(e)[:80])
                continue
            ok = True
            break
        if not ok:
            continue
        got = c["label"] if sp.qform == "ch_outcome" else c["move"]
        if got != st["gold"]:
            flips.append((sp.seed, sp.sampler, got, st["gold"]))
            continue
        sp2 = sp.replace(structure={**st, "params": p, "surf": 777 + i, "pad": 555 + i, "opt": 333 + i, "meta_check": True})
        try:
            row = plugin.render(sp2, ctx).row
            if plugin.solve_b(plugin.parse(row, ctx)) != st["gold"]:
                b_flips.append((sp.seed, sp.sampler))
        except Exception as e:  # noqa: BLE001
            errs.append(f"render: {type(e).__name__}: {str(e)[:80]}")
    n = len(pick)
    limit = 0 if n < 100 else int(0.01 * n)
    return {"audited": n, "flips": len(flips), "b_flips": len(b_flips), "errors": len(errs), "limit": limit,
            "pass": len(flips) <= limit and not b_flips, "examples": flips[:3], "error_examples": errs[:3]}


def _map(obj, names: dict):
    if isinstance(obj, str):
        return SC._sub_names(obj, names)
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int):
        m = names.get(str(obj))
        return int(m) if m and m.isdigit() else obj           # sqlite ids stay integers; composite surface ids need no re-execution
    if isinstance(obj, (list, tuple)):
        return [_map(x, names) for x in obj]
    if isinstance(obj, dict):
        return {k: _map(v, names) for k, v in obj.items()}
    return obj


def name_audit(plugin, specs, n: int = 20, seed: int = 11) -> dict:
    R = random.Random(seed)
    chosen = R.sample(specs, min(n, len(specs)))
    bad, errs = [], 0
    for sp in chosen:
        st = sp.structure
        key = f"{sp.seed}|{sp.sampler}"
        sm = SC.surface(random.Random(key), st["kind"], st["pack"], st["params"])
        names = dict(sm["names"])
        if st["kind"] == "http":                       # item names are values; map them to the surface words too
            names.update({k: v for k, v in sm["vals"].items() if k.startswith("QN") or k == "QW0"})
        p2 = _map(st["params"], names)
        p2["fault"] = st["params"]["fault"]
        p2["variant"] = st["params"]["variant"]
        try:
            c = E.classify(E.run_exec(st["kind"], p2))
        except E.ExecError:
            errs += 1
            continue
        got = c["label"] if sp.qform == "ch_outcome" else c["move"]
        if got != st["gold"]:
            bad.append((sp.seed, sp.sampler, st["kind"], st["fault"], got, st["gold"]))
    return {"audited": len(chosen), "errors": errs, "mismatches": len(bad), "pass": not bad, "examples": bad[:3]}


def heldout_check(plugin, n: int = 400) -> dict:
    train_hits, s5_hits, s5_sw = 0, 0, 0
    for sampler in ("S1", "S2", "S3", "S4", "S5"):
        for seed in range(n if sampler != "S5" else n // 2):
            try:
                sp = plugin.sample(5_000_000 + seed, sampler)
            except Exception:  # noqa: BLE001
                continue
            hit = sp.structure["fault"] == SC.HELD_OUT_FAULT
            if sampler == "S5":
                s5_hits += hit
                s5_sw += sp.structure["gold"] == "SILENT_WRONG" and sp.qform == "ch_outcome"
            else:
                train_hits += hit
    return {"train_samplers_held_out_fault_rows": train_hits, "s5_held_out_fault_rows": s5_hits,
            "s5_silent_wrong_rows": s5_sw, "pass": train_hits == 0 and s5_hits > 0}
