"""F3 gate runner on emitted row files (counts only; never prints row text).

  python checks.py <rows.jsonl> [--part candidates|qc|dev] [--g4-rows 1200] [--out report.json]

G3 (standalone round trip): fmt1 loader_check (check 8), parse, structure hash = meta.structure_hash (check 1),
solver B on the parse = gold (check 2), IDs (3), stated toggles present (4), negcount vs the parsed stem form (5),
options (6), illustration / worked-example blocks (7).
G15: train_decoder.check_rows on every row; loader_check under 3 random permutations (gold letter maps back);
relation units share one call_id and hold <= 3 rows; real-tokenizer length < 1,900 (F3 cap) and <= 7,900 (global).
G4: metamorphic.run on >= 1,000 parsed rows (M1, M2, M3, M5, M9 structural; M4, M8 re-rendered).
G18: no row carries meta.option_level (F3 has no ordinal rows; spec section 1).
Quotas: negcount k_syn >= 1 on >= 10% of yes/no rows, k_all >= 1 on >= 15%, k_syn >= 2 with an affirmative twin on
>= 3% (per sampler and family). fmt1 guard: training files use no held-out style and no S5 row; dev files use only
held-out styles and S5. Import lint: parse_f3 and solver_b import no renderer, sampler or textforms code.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402
import parse_f3 as P  # noqa: E402
import questions as QS  # noqa: E402
import solver_b as SB  # noqa: E402
from f3common import C_SRC, FMT1_DIR, LEAN  # noqa: E402

sys.path.insert(0, str(C_SRC / "common"))
import negcount  # noqa: E402

sys.path.insert(0, str(FMT1_DIR))
from fmt1 import card as fmt1_card  # noqa: E402
from fmt1 import pool as fmt1_pool  # noqa: E402

NEG_EXPECT = {"A": (0, 0), "N1": (1, 1), "N2": (1, 1), "N3": (0, 1), "N4": (1, 1), "N5": (0, 1)}


def expected_neg(Q):
    if Q["form"] == "choice":
        return (0, 0)
    f = Q.get("neg", "A")
    comp = 1 if Q.get("cmp") in ("no fewer than", "no more than") else 0
    if f == "A":
        return (0, comp)
    if f == "D":
        return (2, 2) if Q.get("dbase") in ("N1", "N2") else (1, 2)
    return NEG_EXPECT[f]


def g3_row(row):
    lc = fmt1_card.loader_check(row, seed="f3-g3")
    if not lc["ok"]:
        return False, "loader_check"
    try:
        Pp = P.parse_row(row)
    except Exception as ex:
        return False, "parse:" + type(ex).__name__
    S, Q = Pp["S"], Pp["Q"]
    exp = {"S": S, "Q": Q, "toggles": Pp["toggles"], "hash": row["meta"]["structure_hash"],
           "options": row.get("options"), "neg": expected_neg(Q)}
    res = P.check_row(row, None, exp)
    if not res["ok"]:
        return False, res["why"]
    return True, "ok"


def g15(rows, rels):
    sys.path.insert(0, str(LEAN))
    td = fmt1_card._td()
    out = collections.Counter()
    try:
        td.check_rows(rows)
        out["check_rows_pass"] = len(rows)
    except ValueError as ex:
        out["check_rows_FAIL"] = 1
    rng = random.Random(7)
    for r in rows:
        n = len(r["options"]) if r["qtype"] == "choice" else 2
        ok = True
        for _ in range(3):
            perm = list(range(n))
            rng.shuffle(perm)
            res = fmt1_card.loader_check(r, perm=perm, check_rows=False)
            ok = ok and res["ok"]
        out["perm_letter_map_pass" if ok else "perm_letter_map_FAIL"] += 1
    units = collections.defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r["id"])
    big = [k for k, v in units.items() if len(v) > 3]
    out["units"] = len(units)
    out["units_over_3"] = len(big)
    ids = {r["id"]: r["call_id"] for r in rows}
    bad_rel = 0
    for x in rels:
        if x["type"] in ("complement", "equiv", "inv"):
            if x["a"] not in ids or x["b"] not in ids or ids[x["a"]] != ids[x["b"]]:
                bad_rel += 1
    out["relations_not_in_one_unit"] = bad_rel
    return dict(out)


def quotas(rows, side):
    by = collections.defaultdict(collections.Counter)
    sid = {s["id"]: s for s in side}
    twin_of = {r["id"]: r["meta"]["twin_of"] for r in rows}
    for r in rows:
        if r["qtype"] != "noul":
            continue
        sp = r["meta"]["sampler"]
        s = sid[r["id"]]
        for key in (sp, "family"):
            c = by[key]
            c["yn"] += 1
            c["ksyn1"] += s["k_syn"] >= 1
            c["kall1"] += s["k_all"] >= 1
            c["ksyn2_twin"] += s["k_syn"] >= 2 and r["meta"]["twin_of"] is not None
            c["yes"] += r["gold"] == 1
            c["bad"] += (s.get("polarity") == "bad") == bool(r["gold"] == 1) and s.get("polarity") is not None \
                if False else 0
    out = {}
    for k, c in by.items():
        yn = max(1, c["yn"])
        out[k] = {"yn_rows": c["yn"], "k_syn>=1": round(c["ksyn1"] / yn, 4), "k_all>=1": round(c["kall1"] / yn, 4),
                  "k_syn>=2_with_aff_twin": round(c["ksyn2_twin"] / yn, 4), "yes_rate": round(c["yes"] / yn, 4)}
        out[k]["pass"] = out[k]["k_syn>=1"] >= 0.10 and out[k]["k_all>=1"] >= 0.15 and \
            out[k]["k_syn>=2_with_aff_twin"] >= 0.03
    return out


def import_lint():
    bad = []
    for f in ("parse_f3.py", "solver_b.py"):
        src = open(os.path.join(HERE, f)).read()
        for mod in ("render_f3", "textforms", "samplers", "logbuild", "cards", "build", "fmt1.render", "fmt1 import"):
            if re.search(r"^\s*(?:import|from)\s+" + re.escape(mod.split()[0]) + r"\b", src, re.M):
                bad.append(f"{f}:{mod}")
    src = open(os.path.join(HERE, "solver_b.py")).read()
    if re.search(r"^\s*(?:import|from)\s+solver_a\b", src, re.M):
        bad.append("solver_b:solver_a")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--part", default="candidates")
    ap.add_argument("--g4-rows", type=int, default=1300)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.rows)]
    base = a.rows[:-6]
    side = [json.loads(l) for l in open(base + ".sidecar.jsonl")]
    rels = [json.loads(l) for l in open(base + ".relations.jsonl")]
    rep = {"file": os.path.basename(a.rows), "rows": len(rows)}
    g3 = collections.Counter()
    for r in rows:
        ok, why = g3_row(r)
        g3[why] += 1
    rep["G3"] = {"pass": g3.get("ok", 0), "fail": {k: v for k, v in g3.items() if k != "ok"},
                 "rate": round(g3.get("ok", 0) / max(1, len(rows)), 6)}
    rep["G15"] = g15(rows, rels)
    toks = [s["real_tokens"] for s in side]
    rep["length"] = {"max_real_tokens": max(toks), "rows_ge_1900": sum(t >= 1900 for t in toks),
                     "rows_gt_7900": sum(t > 7900 for t in toks),
                     "median": sorted(toks)[len(toks) // 2]}
    rep["G18"] = {"rows_with_option_level": sum(1 for r in rows if (r.get("meta") or {}).get("option_level"))}
    rep["quotas_negcount"] = quotas(rows, side)
    try:
        if a.part == "dev":
            for r in rows:
                fmt1_pool.dev_style(r["meta"]["format_style"])
            rep["fmt1_guard"] = {"dev_rows_all_heldout_styles": True,
                                 "s5_rows": sum(1 for r in rows if r["meta"]["sampler"] == "S5")}
        else:
            rep["fmt1_guard"] = fmt1_pool.refuse_held_out(rows)
    except Exception as ex:
        rep["fmt1_guard"] = {"FAIL": str(ex)[:200]}
    rep["import_lint_violations"] = import_lint()
    if a.part != "dev" or a.g4_rows:
        import metamorphic as M
        import g4render
        rng = random.Random(20261003)
        pick = rows[:]
        rng.shuffle(pick)
        pick = pick[:a.g4_rows]
        cards = g4render.cards_for(a.part)
        rep["G4"] = M.run(pick, cards, n_min=1000 if a.part != "dev" else 1, render_fn=g4render.render_variant)
    out = a.out or base + ".gates.json"
    with open(out, "w") as f:
        json.dump(rep, f, indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("quotas_negcount",)}, indent=1)[:4000])


if __name__ == "__main__":
    main()
