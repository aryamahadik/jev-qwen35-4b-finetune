"""families/T45/prefreeze.py: parallel IN-MEMORY build + the A45 (d) pre-freeze gates of T45. Nothing is written but one
metrics file of numbers (no row file). Usage (from lean/c2_build):
  nice -n 10 ../../.venv/bin/python -B families/T45/prefreeze.py --n 5000 --workers 4 --out <metrics.json> [--g15]
The parent first executes every canonical structure once (warm_cache: two fresh processes each), then forks the workers, which
inherit the execution cache. Wall times are reported."""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))


def _work(args):
    n, base, g15 = args
    import pilot
    import pilot_loaders as PL
    from families.T45 import run_pilot_i1 as RUN
    PL.LOADERS["T45"] = RUN._t45
    RUN.install_patches()
    with PL.LOADERS["T45"]() as kit:
        return pilot.build_pilot(kit, n, seed_base=base, run_g15=g15)


def build(n, workers, g15=False, seed0=None):
    import pilot
    seed0 = pilot.SEED_BASE if seed0 is None else seed0
    per = -(-n // workers)
    per = -(-per // 4) * 4
    jobs = [(per, seed0 + w * 1_000_000, g15) for w in range(workers)]
    with mp.get_context("fork").Pool(workers) as pool:
        builds = pool.map(_work, jobs, chunksize=1)
    merged = pilot.Build("T45")
    off = 0
    for b in builds:
        for info in b.infos:
            info.unit += off
        merged.infos += b.infos
        merged.units += b.units
        merged.rels += b.rels
        off += len(b.units)
    st = {k: sum(b.stats.get(k, 0) for b in builds) for k in ("rows_written", "units_written", "units_attempted", "units_dropped")}
    drops = Counter()
    for b in builds:
        drops.update(b.stats["drops_by_gate"])
    st["drops_by_gate"] = dict(drops)
    st["reached_target"] = all(b.stats["reached_target"] for b in builds)
    merged.stats = st
    return merged


def analyze(b, plugin, quick=False):
    import pilot
    from c2_kit.choiceplan import plan_report
    from families.T45 import audits as AU
    from families.T45 import probes as PR
    infos = b.infos
    heads = PR.split_heads(infos)
    res = {"n_rows": len(infos), "rows_per_head": {h: len(v) for h, v in heads.items()}}
    g6 = pilot.g6(infos)
    res["g6_all"] = {"verdict": g6["verdict"], "chance": g6["choice"]["chance"], "views": {v: g6["choice"][v] for v in
                     ("a_question", "b_options", "c_card_without_question", "d_meta")}, "fails": g6["fails"]}
    for h, part in heads.items():
        gc = pilot.g6_choice(part)
        ch = gc["chance"]
        fails = [(v, m, gc[v][m]) for v in ("a_question", "b_options", "c_card_without_question", "d_meta") for m in ("lr", "gbt")
                 if gc[v][m] > ch + 0.02 + 1e-12]
        res["g6_" + h] = {"n": gc["n"], "chance": ch, "views": {v: gc[v] for v in
                          ("a_question", "b_options", "c_card_without_question", "d_meta")}, "fails": fails, "pass": not fails}
    g7 = pilot.g7(infos)
    res["g7"] = {"verdict": g7["verdict"], "n_tests": g7["n_tests"], "choice_fails": g7["choice_fails"][:8], "top5": g7["top5_choice"]}
    g10 = pilot.g10(infos, b.units, plugin)
    res["g10"] = {"verdict": g10["verdict"], "failing": g10["failing"],
                  "checks": {k: {"verdict": v["verdict"], "value": v["value"]} for k, v in g10["checks"].items()}}
    res["options_only"] = PR.options_only(infos)
    res["formatting_only"] = PR.formatting_only(infos)
    sets = [rr.option_set for u in b.units for rr in u.rendered if rr.option_set is not None]
    pr = plan_report(sets)
    res["plan_report"] = {k: pr[k] for k in pr if k in ("pass", "failing", "position", "rank", "longest_pp", "abstain")} or pr
    toks, how = pilot.real_tokens([i.row for i in infos])
    toks = list(toks)
    res["tokens"] = {"mean": round(sum(toks) / len(toks), 1), "max": max(toks), "how": how}
    cards = Counter(i.row["meta"]["card_id"] for i in infos)
    res["cards"] = {"n_cards": len(cards), "max_rows_per_card": max(cards.values())}
    out = Counter(i.row["gold"] for i in heads["ch_outcome"])
    mv = Counter(i.row["gold"] for i in heads["ch_move"])
    kinds = Counter(i.spec.structure["kind"] for i in infos)
    faults = Counter(i.spec.structure["fault"] for i in infos)
    res["balance"] = {"outcome_gold": dict(out), "move_gold": dict(mv), "kind": dict(kinds), "fault": dict(faults),
                      "success_share_outcome_head": round(out["SUCCESS"] / max(1, len(heads["ch_outcome"])), 4),
                      "success_share_all_rows": round((out["SUCCESS"] + sum(1 for i in heads["ch_move"]
                              if i.spec.structure["fault"] == "ok")) / len(infos), 4),
                      "registers": dict(Counter(i.row["meta"]["c2"]["register"] for i in infos))}
    if not quick:
        specs = [i.spec for i in infos]
        res["reseed_audit"] = AU.reseed_audit(plugin, None, specs, 0.03) if False else None
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--g15", action="store_true")
    ap.add_argument("--out", default="")
    ap.add_argument("--no-warm", action="store_true")
    a = ap.parse_args()
    from families.T45 import audits as AU
    from families.T45 import executor as E
    from families.T45 import plugin as P
    from families.T45 import run_pilot_i1 as RUN
    t0 = time.time()
    warm_s = 0.0
    if not a.no_warm:
        n_exec = P.warm_cache(workers=a.workers)
        warm_s = round(time.time() - t0, 1)
        print(f"warm: {n_exec} canonical executions (x2 runs) in {warm_s} s; stats {E.STATS}", flush=True)
    t1 = time.time()
    b = build(a.n, a.workers, a.g15)
    build_s = round(time.time() - t1, 1)
    print("built", len(b.infos), "rows", build_s, "s", b.stats, flush=True)
    RUN.install_patches()
    plugin, ctx = P.make_plugin()
    t2 = time.time()
    res = analyze(b, plugin)
    res["build_stats"] = b.stats
    specs = [i.spec for i in b.infos]
    res["reseed_audit"] = AU.reseed_audit(plugin, ctx, specs, 0.03)
    res["name_audit"] = AU.name_audit(plugin, specs, 20)
    res["heldout_check"] = AU.heldout_check(plugin, 300)
    res["wall_seconds"] = {"warm_cache": warm_s, "build": build_s, "analysis_and_audits": round(time.time() - t2, 1),
                           "total": round(time.time() - t0, 1)}
    res["exec_stats_parent"] = dict(E.STATS)
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    brief = {"g6_all_fails": [(f["view"], f["model"], f["acc"]) for f in res["g6_all"]["fails"]], "chance": res["g6_all"]["chance"],
             "g6_outcome": res["g6_ch_outcome"]["fails"], "g6_move": res["g6_ch_move"]["fails"], "g7": res["g7"]["verdict"],
             "g10": res["g10"]["failing"], "oo": res["options_only"], "fo": res["formatting_only"], "tokens": res["tokens"],
             "cards": res["cards"], "reseed": res["reseed_audit"], "name": res["name_audit"], "heldout": res["heldout_check"],
             "wall": res["wall_seconds"], "balance": {k: res["balance"][k] for k in ("success_share_outcome_head", "success_share_all_rows")}}
    print(json.dumps(brief, default=str))


if __name__ == "__main__":
    main()
