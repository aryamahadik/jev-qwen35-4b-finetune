"""T01 full-generation diagnosis (in memory, CPU only, no writes except the --out JSON).

  python -B zed_orch/t01diag/diag_build.py --mode pilot|tool --seed-base N --n N [--g15 0|1] [--yn 0|1] --out FILE

mode pilot: the pilot runner's own path (run_pilot_i3._patched + PL.open_family), NO exclusion step (as g6_at in the runner).
mode tool : gen_full_c2.loader_patch + quarantine_sources + apply_exclusions (the tool's path), plain pilot.build_pilot after.
Reports: k mix, gold position per k (option sets and distinct (row_key, k) cells), qform x k, qform x gold position,
chi-square tests, G6 (choice part; yes/no with --yn 1), G10 gold_position / gold_rank / longest, and a digest of the rows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
import gen_full_c2 as GF  # noqa: E402


def chi2_uniform_p(c):
    from scipy.stats import chisquare
    return None if sum(c) < 5 * len(c) else round(float(chisquare(c).pvalue), 4)


def chi2_indep_p(table):
    from scipy.stats import chi2_contingency
    import numpy as np
    t = np.array([r for r in table if sum(r) > 0])
    t = t[:, t.sum(0) > 0]
    if t.shape[0] < 2 or t.shape[1] < 2:
        return None
    return round(float(chi2_contingency(t)[1]), 4)


def digest(rows):
    h = hashlib.sha256()
    for r in rows:
        h.update(json.dumps([r["id"], r["state"], r["instructions"], r.get("options"), r["gold"]],
                            ensure_ascii=False, sort_keys=True).encode())
    return h.hexdigest()


def analyse(b, plugin, with_g6=True, with_yn=False):
    infos = b.infos
    rows = [i.row for i in infos]
    sets = [(rr.option_set, plugin._row_key(rr.spec) if hasattr(rr, "spec") else None) for u in b.units for rr in u.rendered
            if rr.option_set is not None]
    # row-level (all choice rows)
    ch = [i for i in infos if i.row["qtype"] == "choice"]
    kmix = Counter(len(i.row["options"]) for i in ch)
    pos_k = defaultdict(lambda: Counter())
    qf_k_pos = defaultdict(lambda: defaultdict(Counter))
    qf_k = defaultdict(Counter)
    cell = {}
    for i in ch:
        o = i.row["options"]
        k, p = len(o), o.index(i.row["gold"])
        qf = i.row["meta"]["qform"]
        pos_k[k][p] += 1
        qf_k_pos[k][qf][p] += 1
        qf_k[qf][k] += 1
        cell[(plugin._row_key(i.spec), k)] = p
    out = {"n_rows": len(rows), "n_units": len(b.units), "rows_digest": digest(rows),
           "n_choice_rows": len(ch), "n_yes_no_rows": len(rows) - len(ch),
           "k_mix_rows": {str(k): v for k, v in sorted(kmix.items())},
           "gold_pos_rows": {str(k): [pos_k[k][j] for j in range(k)] for k in sorted(pos_k)},
           "gold_pos_rows_chi2_p": {str(k): chi2_uniform_p([pos_k[k][j] for j in range(k)]) for k in sorted(pos_k)},
           "qform_x_k": {q: dict(sorted(v.items())) for q, v in sorted(qf_k.items())},
           "qform_x_gold_pos": {str(k): {q: [c[j] for j in range(k)] for q, c in sorted(d.items())}
                                for k, d in sorted(qf_k_pos.items())},
           "qform_x_gold_pos_indep_chi2_p": {str(k): chi2_indep_p([[c[j] for j in range(k)] for c in d.values()])
                                              for k, d in sorted(qf_k_pos.items())}}
    # distinct (row_key, k) cells: the draw is one hash per cell, twin rows repeat it
    cell_pos = defaultdict(Counter)
    for (rk, k), p in cell.items():
        cell_pos[k][p] += 1
    out["gold_pos_distinct_cells"] = {str(k): [cell_pos[k][j] for j in range(k)] for k in sorted(cell_pos)}
    out["gold_pos_distinct_cells_chi2_p"] = {str(k): chi2_uniform_p([cell_pos[k][j] for j in range(k)])
                                              for k in sorted(cell_pos)}
    out["rows_per_distinct_cell"] = round(len(cell) and len(ch) / len(cell), 3)
    recs, marg = [], defaultdict(lambda: [0.0, 0.0, 0])
    for i in ch:
        r = i.row
        o = r["options"]
        k, gp = len(o), o.index(r["gold"])
        lens = [len(x) for x in o]
        kinds = pilot.option_kinds(i)
        order = sorted(range(k), key=lambda j: (-lens[j], j))
        glr = order.index(gp)                       # 0 = the longest
        recs.append({"qform": r["meta"]["qform"], "sampler": r["meta"].get("sampler"), "seed": i.spec.seed, "k": k,
                     "gold_pos": gp, "gold_len_rank": glr, "lens": lens, "kinds": [sorted(x) for x in kinds], "card": r["meta"]["card_id"],
                     "unit": i.unit, "options": o, "gold_text": r["gold"], "gold_rank_meta": (r["meta"].get("gold_rank"))})
        for kd in {x for ks in kinds for x in (ks if isinstance(ks, (list, tuple, set)) else [ks])}:
            has = [kd in (ks if isinstance(ks, (list, tuple, set)) else [ks]) for ks in kinds]
            marg[kd][0] += has[gp] / 1.0
            marg[kd][1] += sum(has) / k
            marg[kd][2] += 1
    out["gold_has_kind_vs_expected"] = {kd: {"gold_rate": round(v[0] / v[2], 4), "expected_if_blind": round(v[1] / v[2], 4),
                                             "diff_pp": round(100 * (v[0] - v[1]) / v[2], 2), "rows": v[2]}
                                        for kd, v in sorted(marg.items())}
    out["_records"] = recs
    g10 = pilot.g10(infos, b.units, plugin)
    chk = g10["checks"]
    out["G10"] = {k: {"verdict": chk[k]["verdict"], "value": chk[k]["value"]}
                  for k in ("gold_position", "gold_rank", "longest_option_gold_pp") if k in chk}
    out["G10_failing"] = g10.get("failing")
    if with_g6:
        t = time.time()
        g6c = pilot.g6_choice(ch)
        out["G6_choice"] = g6c
        mx = max((g6c[v][m], v, m) for v in g6c if isinstance(g6c[v], dict) for m in ("lr", "gbt"))
        out["G6_choice_max"] = mx
        out["G6_choice_excess_pp"] = round(100 * (mx[0] - g6c["chance"]), 2)
        if with_yn:
            yn = [i for i in infos if i.row["qtype"] == "noul"]
            g6y = pilot.g6_yes_no(yn)
            out["G6_yes_no"] = g6y
            out["G6_yes_no_max"] = max((g6y[v][m], v, m) for v in g6y if isinstance(g6y[v], dict) and "lr" in g6y[v]
                                       for m in ("lr", "gbt"))
        out["g6_seconds"] = round(time.time() - t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("pilot", "tool"), required=True)
    ap.add_argument("--seed-base", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--g15", type=int, default=0)
    ap.add_argument("--yn", type=int, default=0)
    ap.add_argument("--no-g6", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time()
    if a.mode == "pilot":
        from families.T01 import run_pilot_i3 as R
        with R._patched() as P:
            with P.open_family("T01") as kit:
                b = pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=bool(a.g15))
                res = analyse(b, kit.plugin, not a.no_g6, bool(a.yn))
                res["exclusion_step"] = "none (runner path)"
    else:
        banned = set().union(*map(set, GF.quarantine_sources("T01").values()))
        with GF.loader_patch("T01"):
            with PL.open_family("T01") as kit0:
                kit, xrep = GF.apply_exclusions(kit0, banned)
                b = pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=bool(a.g15))
                res = analyse(b, kit.plugin, not a.no_g6, bool(a.yn))
                res["exclusion_step"] = {k: xrep[k] for k in ("banned_ids", "skins_removed", "dead_qforms",
                                                               "wordings_before", "wordings_after")}
    res.update({"mode": a.mode, "seed_base": a.seed_base, "n_requested": a.n, "g15": a.g15,
                "build_stats": {k: b.stats[k] for k in ("rows_written", "units_written", "units_attempted",
                                                       "units_dropped", "drops_by_gate")},
                "seconds": round(time.time() - t0)})
    recs = res.pop("_records", [])
    Path(a.out).write_text(json.dumps(res, indent=1, default=str))
    Path(a.out + ".records.jsonl").write_text("\n".join(json.dumps(x, default=str) for x in recs))
    print(json.dumps({k: res.get(k) for k in ("mode", "seed_base", "n_rows", "rows_digest", "k_mix_rows",
                                              "gold_pos_rows", "G6_choice_max", "G6_choice_excess_pp", "G10_failing",
                                              "seconds")}, default=str))


if __name__ == "__main__":
    main()
