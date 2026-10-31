"""Extra F7 quota statistics read back from rows through the parser (counts only): S1 decisive-path boundary share
(>= 15%), S2 near-miss share (R17), override firing uniformity (T17), S6 per-cut coverage (T23), cut-point magnitudes.

  python f7stats.py <rows.jsonl> [--out stats.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f7packs as PK  # noqa: E402
import f7parse as PS  # noqa: E402
import f7solveb as SB  # noqa: E402


def atoms(c):
    t = c["t"]
    if t == "atom":
        return [c["a"]]
    if t in ("and", "or", "allof", "anyof"):
        return [a for p in c["parts"] for a in atoms(p)]
    if t == "unless":
        return atoms(c["a"]) + [c["b"]]
    if t == "onlyif":
        return atoms(c["main"]) + [c["c"]]
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--out")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.rows, encoding="utf-8")]
    st = collections.Counter()
    fire = collections.defaultdict(collections.Counter)
    cut_cov = collections.defaultdict(collections.Counter)
    mags = set()
    for r in rows:
        m = r["meta"]
        pack = PK.pack_by_id(m["domain_pack"])
        PC, case, _ = PS.parse_row(r, pack)
        D = SB.domains(PC, pack)
        env = SB.env_from_case(PC, case, D)
        g = PC["option_level"][r["gold"]]
        K = PC["K"]
        ranks = PC.get("ranks") or []
        if m["sampler"] == "S1" and PC["mode"] in ("ladder", "highest"):
            st["S1_rows"] += 1
            path = []
            if PC["mode"] == "ladder":
                for k in range(1, min(g + 2, K)):
                    path += atoms(PC["crits"][k])
            else:
                for k in ([g] if g >= 1 else []) + list(range(g + 1, K)):
                    path += atoms(PC["crits"][k])
            hit = False
            for at in path:
                if at["kind"] in ("num", "date"):
                    x = env[at["term"]]
                    r_ = D[at["term"]]["r"]
                    if abs(Fraction(x) - Fraction(at["t"])) <= Fraction(r_):
                        hit = True
            st["S1_decisive_path_at_or_one_step"] += hit
        if m["sampler"] == "S2" and PC["mode"] in ("ladder", "highest") and g < K - 1:
            st["S2_rows_below_top"] += 1
            near = False
            for k in range(g + 1, K):
                c = PC["crits"][k]
                if c["t"] in ("and", "allof"):
                    vals = [SB.crit_holds(p, env, D, ranks) for p in c["parts"]]
                    if sum(1 for v in vals if not v) == 1:
                        near = True
            st["S2_near_miss"] += near
        if PC.get("overrides"):
            fl = next((o for o in PC["overrides"] if o["type"] == "floor"), None)
            cp = next((o for o in PC["overrides"] if o["type"] == "cap"), None)
            ff = bool(fl) and SB.crit_holds(fl["cond"], env, D, ranks)
            cf = bool(cp) and SB.crit_holds(cp["cond"], env, D, ranks)
            pat = "both" if ff and cf else "floor" if ff else "cap" if cf else "none"
            fire[m["card_id"]][(pat, g)] += 1
        if PC["mode"] == "cut":
            b = next((e for e in m["edge"] if e["kind"] == "boundary"), None)
            x = env[PC["qty_term"]]
            cuts = sorted({rg[1] for rg in PC["ranges"].values() if rg[0] in ("int", "ge")} |
                          {v for rg in PC["ranges"].values() if rg[0] == "half" for v in (rg[1], rg[3]) if v is not None})
            if b and b["placement"] != "interior" and cuts:
                ci = min(range(len(cuts)), key=lambda i: abs(Fraction(x) - cuts[i]))
                cut_cov[(K, b["placement"])][ci] += 1
            for c in cuts:
                if c > 0:
                    mags.add(math.floor(math.log10(float(c))))
    out = dict(st)
    if st["S1_rows"]:
        out["S1_decisive_path_boundary_share"] = round(st["S1_decisive_path_at_or_one_step"] / st["S1_rows"], 4)
    if st["S2_rows_below_top"]:
        out["S2_near_miss_share"] = round(st["S2_near_miss"] / st["S2_rows_below_top"], 4)
    out["override_cards"] = len(fire)
    out["override_patterns"] = {cid: {f"{p}|{l}": n for (p, l), n in sorted(c.items())} for cid, c in fire.items()}
    out["S6_cut_coverage"] = {f"K{k}|{p}": dict(sorted(c.items())) for (k, p), c in sorted(cut_cov.items())}
    out["cut_point_orders_of_magnitude"] = sorted(mags)
    path = a.out or a.rows + ".stats.json"
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("override_patterns", "S6_cut_coverage")}))


if __name__ == "__main__":
    main()
