"""families/T43/qc_build.py: the A45 pre-freeze in-memory QC build (>= 5,000 rows) in parallel shards, then pilot.g6 / g7 / g10, the
A42-D 3.2 probes and the per-head G6 on the merged infos. Nothing is written but a metrics JSON of numbers (no row file).

  ../../.venv/bin/python -B families/T43/qc_build.py --rows 5200 --workers 8 --out families/T43/QC_METRICS.json
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))


def _shard(args):
    w, n, run_g15 = args
    import pilot
    import pilot_loaders as PL
    from families.T43 import run_pilot_i1 as RUN
    PL.LOADERS["T43"] = RUN._t43
    RUN.install_patches()
    with PL.LOADERS["T43"]() as kit:
        b = pilot.build_pilot(kit, n, seed_base=pilot.SEED_BASE + 100_000 * (w + 1), run_g15=run_g15)
    from families.T43 import plugin as P
    b.stats["diag"] = dict(P.DIAG)
    return w, b.infos, b.units, b.stats


def _shard_quick(args):
    """Sample + render only (no gates): the fast loop for generator fixes. Returns RowInfos (units = None)."""
    w, n, _ = args
    import pilot
    from families.T43 import plugin as P
    plugin, ctx = P.make_plugin()
    infos, k, fails = [], 0, 0
    train = ("S1", "S2", "S3", "S4")
    while len(infos) < n:
        smp, seed = train[k % 4], pilot.SEED_BASE + 100_000 * (w + 1) + k // 4
        k += 1
        try:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
        except Exception:  # noqa: BLE001
            fails += 1
            continue
        q, cx = pilot.split_question(rr)
        infos.append(pilot.RowInfo(rr.row, spec, rr, len(infos), q, cx, None))
    return w, infos, [], {"drops_by_gate": {"sample_fail": fails}, "drop_examples": {}, "diag": dict(P.DIAG)}


def run(rows: int, workers: int, run_g15: bool, log=print, quick: bool = False, pickle_to: str | None = None, prefix: int = 0) -> dict:
    import pilot
    from families.T43 import probes as PR
    from families.T43 import run_pilot_i1 as RUN
    per = -(-rows // workers)
    t0 = time.time()
    with mp.get_context("fork").Pool(workers) as pool:
        out = pool.map(_shard_quick if quick else _shard, [(w, per, run_g15) for w in range(workers)])
    infos, units, stats, pre = [], [], [], []
    for w, inf, un, st in sorted(out, key=lambda x: x[0]):
        pre += inf[:prefix]
        off = len(units)
        for i in inf:
            i.unit += off
        infos += inf
        units += un
        stats.append(st)
    log(f"merged {len(infos)} rows from {workers} shards in {time.time() - t0:.0f}s")
    RUN.install_patches()
    from families.T43 import plugin as P
    plugin, _ = P.make_plugin()
    if pickle_to:
        import pickle
        Path(pickle_to).write_bytes(pickle.dumps([(i.row, i.spec.structure) for i in infos]))
    g6, g7 = pilot.g6(infos), pilot.g7(infos)
    g10 = {"verdict": "skipped (quick)", "failing": [], "checks": {}} if quick else pilot.g10(infos, units, plugin)
    res = {"n_rows": len(infos), "seconds_build": round(time.time() - t0, 1),
           "g6": {"verdict": g6["verdict"], "fails": g6["fails"], "choice": g6["choice"]},
           "g6_by_head": PR.g6_by_head(infos),
           "g7": {"verdict": g7["verdict"], "n_tests": g7["n_tests"], "choice_fails": g7["choice_fails"][:8]},
           "g10": {"verdict": g10["verdict"], "failing": g10["failing"], "failing_checks": {k: g10["checks"][k] for k in g10["failing"]}},
           "options_only": PR.options_only(infos), "formatting_only": PR.formatting_only(infos), "diff_size": PR.diff_size(infos),
           "drops": [s["drops_by_gate"] for s in stats], "drop_examples": [s["drop_examples"] for s in stats][:2]}
    if prefix:
        import dataclasses
        umap, pre2 = {}, []
        for i in pre:
            umap.setdefault(i.unit, len(umap))
            pre2.append(dataclasses.replace(i, unit=umap[i.unit]))
        pre_units = [None] * len(umap)
        for old_u, new_u in umap.items():
            pre_units[new_u] = units[old_u] if units else None
        g7p = pilot.g7(pre)
        g10p = {"verdict": "skipped (quick)", "failing": [], "checks": {}} if quick else pilot.g10(pre2, pre_units, plugin)
        res["at_prefix"] = {"n_rows": len(pre), "g7": {"verdict": g7p["verdict"], "n_tests": g7p["n_tests"], "choice_fails": g7p["choice_fails"][:8]},
                            "g10": {"verdict": g10p["verdict"], "failing": g10p["failing"], "failing_checks": {k: g10p["checks"][k] for k in g10p["failing"]}}, "g6": {k: v for k, v in pilot.g6(pre).items() if k in ("verdict", "fails", "choice")},
                            "g6_by_head": PR.g6_by_head(pre), "options_only": PR.options_only(pre),
                            "formatting_only": PR.formatting_only(pre), "diff_size": PR.diff_size(pre)}
    toks, how = pilot.real_tokens([i.row for i in infos])
    cards = {}
    for i in infos:
        cards[i.row["meta"]["card_id"]] = cards.get(i.row["meta"]["card_id"], 0) + 1
    res["tokens"] = {"mean": sum(toks) / len(toks), "max": max(toks), "by": how}
    byh = {}
    for i, t in zip(infos, toks):
        byh.setdefault(i.spec.structure["head"] + ":" + i.spec.structure["kind"], []).append(t)
    res["tokens_by_head"] = {k: round(sum(v) / len(v)) for k, v in byh.items()}
    res["cards"] = {"n": len(cards), "max_rows": max(cards.values())}
    heads = {}
    for i in infos:
        k = i.spec.structure["head"]
        heads[k] = heads.get(k, 0) + 1
    res["heads"] = heads
    pv = [i for i in infos if i.spec.structure["head"] == "pv"]
    res["pv_gold"] = {k: sum(i.row["gold"] == k for i in pv) / len(pv) for k in sorted({i.row["gold"] for i in pv})}
    ll = [i for i in infos if i.spec.structure["head"] in ("ll", "lf")]
    res["loc_none_share"] = sum(i.row["gold"].startswith("none") for i in ll) / max(1, len(ll))
    diag = {}
    for s in stats:
        for k, v in s.get("diag", {}).items():
            diag[k] = diag.get(k, 0) + v
    res["diag"] = dict(sorted(diag.items()))
    tl = {}
    for i in pv:
        st = i.spec.structure
        tl.setdefault(st["template"].split("_")[0] if st["kind"] == "module" else st["template"], {}).setdefault(i.row["gold"][:4], 0)
        tl[st["template"].split("_")[0] if st["kind"] == "module" else st["template"]][i.row["gold"][:4]] += 1
    res["pv_label_by_template"] = tl
    ll1 = {}
    for i in infos:
        st = i.spec.structure
        if st["head"] == "ll":
            ll1.setdefault(st["template"], {}).setdefault(i.row["gold"], 0)
            ll1[st["template"]][i.row["gold"]] += 1
    res["ll_line_by_template"] = ll1
    return res, infos, units


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=5200)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--no-g15", action="store_true")
    ap.add_argument("--quick", action="store_true", help="sample + render only (no gates): the fix loop")
    ap.add_argument("--pickle", default=None)
    ap.add_argument("--prefix", type=int, default=0, help="also report the metrics on the first N rows of every shard")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "QC_METRICS.json"))
    a = ap.parse_args()
    res, _, _ = run(a.rows, a.workers, not a.no_g15, log=lambda m: print(m, file=sys.stderr, flush=True), quick=a.quick, pickle_to=a.pickle, prefix=a.prefix)
    Path(a.out).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("n_rows", "g6", "g7", "g10")}, default=str)[:1500])
