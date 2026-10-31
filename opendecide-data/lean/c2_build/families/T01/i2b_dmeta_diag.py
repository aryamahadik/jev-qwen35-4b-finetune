"""Diagnostic (read-only): which pilot.meta_features / option features drive the choice d_meta view at 6,000 rows.

  ../../.venv/bin/python -B families/T01/i2b_dmeta_diag.py build   (from lean/c2_build) -> pilot_i2/i2b/choice_rows.json
  ../../.venv/bin/python -B families/T01/i2b_dmeta_diag.py rank                            -> pilot_i2/i2b/DMETA_DRIVERS.json
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
OUT = C2 / "families/T01/pilot_i2/i2b"


def build(n=6000):
    import pilot
    from families.T01 import run_pilot_i2 as R
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with R._patched() as PL:
        with PL.open_family("T01") as kit:
            b = pilot.build_pilot(kit, n, run_g15=False)
            ch = [i for i in b.infos if i.row["qtype"] == "choice"]
            g6 = pilot.g6_choice(ch)
            print("d_meta", g6["d_meta"], "chance", g6["chance"], "n", g6["n"])
            for i in ch:
                r = i.row
                cat, num = pilot.meta_features(i)
                kinds = pilot.option_kinds(i)
                opts = r["options"]
                clen = [len(o) for o in opts]
                order = sorted(range(len(opts)), key=lambda j: -clen[j])
                rank = {j: q for q, j in enumerate(order)}
                g = opts.index(r["gold"])
                rows.append({"cat": cat, "num": num, "k": len(opts), "pos": g, "gold_len_rank": rank[g],
                             "gold_kinds": sorted(kinds[g]), "all_kinds": [sorted(s) for s in kinds],
                             "clen": clen, "gold": g, "opts": opts, "card": r["meta"]["card_id"],
                             "qform": r["meta"].get("qform"), "sampler": r["meta"].get("sampler")})
    (OUT / "choice_rows.json").write_text(json.dumps(rows))
    print("rows", len(rows))


def chi2(table):
    """table: {value: Counter(role)} -> (chi2, dof, n)."""
    roles = sorted({r for c in table.values() for r in c})
    n = sum(sum(c.values()) for c in table.values())
    tot = Counter()
    for c in table.values():
        tot.update(c)
    x = 0.0
    for c in table.values():
        nv = sum(c.values())
        for r in roles:
            e = nv * tot[r] / n
            if e > 0:
                x += (c.get(r, 0) - e) ** 2 / e
    return x, (len(table) - 1) * (len(roles) - 1), n


def rank():
    from scipy.stats import chi2 as C
    rows = json.loads((OUT / "choice_rows.json").read_text())
    n = len(rows)
    chance = sum(1 / r["k"] for r in rows) / n
    res = {"n": n, "chance": round(chance, 4)}
    # 1. role distributions overall
    res["gold_pos_by_k"] = {k: dict(sorted(Counter(r["pos"] for r in rows if r["k"] == k).items())) for k in (2, 3, 4, 5)}
    res["gold_len_rank_by_k"] = {k: dict(sorted(Counter(r["gold_len_rank"] for r in rows if r["k"] == k).items()))
                                 for k in (2, 3, 4, 5)}
    for kind in ("kind:longest", "kind:shortest", "kind:abstain", "kind:neg", "kind:verbatim_in_text"):
        exp = sum(sum(kind in s for s in r["all_kinds"]) / r["k"] for r in rows) / n
        obs = sum(kind in r["gold_kinds"] for r in rows) / n
        res.setdefault("gold_kind_vs_expected", {})[kind] = {"gold_rate": round(obs, 4), "expected_if_label_blind": round(exp, 4),
                                                              "diff_pp": round(100 * (obs - exp), 2)}
    # 2. row-level categorical meta features vs gold role (len-rank bucket as the d_meta cross uses it, and kinds)
    def role(r):
        b = int((r["gold_len_rank"] / max(1, r["k"] - 1)) * 4)
        return f"lr{b}|neg{int('kind:neg' in r['gold_kinds'])}|abs{int('kind:abstain' in r['gold_kinds'])}"
    feats = defaultdict(lambda: defaultdict(Counter))
    for r in rows:
        for kk, vv in r["cat"].items():
            feats[kk][vv][role(r)] += 1
        feats["k"][r["k"]][role(r)] += 1
    out = []
    for kk, tab in feats.items():
        x, dof, nn = chi2(tab)
        out.append({"feature": kk, "values": len(tab), "chi2": round(x, 1), "dof": dof,
                    "p": float(C.sf(x, dof)) if dof else None, "excess_per_row": round((x - dof) / nn, 4)})
    res["categorical_vs_gold_role"] = sorted(out, key=lambda d: -d["excess_per_row"])
    # 3. numeric row-level features vs gold len-rank / pos: eta^2 style (mean gold role by feature tercile)
    numrank = []
    for f in rows[0]["num"]:
        vals = [r["num"][f] for r in rows]
        if len(set(vals)) < 2:
            continue
        cut = sorted(vals)
        t1, t2 = cut[n // 3], cut[2 * n // 3]
        tab = defaultdict(Counter)
        for r, v in zip(rows, vals):
            tab["lo" if v <= t1 else "mid" if v <= t2 else "hi"][role(r)] += 1
        x, dof, nn = chi2(tab)
        numrank.append({"feature": f, "chi2": round(x, 1), "dof": dof, "p": float(C.sf(x, dof)),
                        "excess_per_row": round((x - dof) / nn, 4)})
    res["numeric_vs_gold_role"] = sorted(numrank, key=lambda d: -d["excess_per_row"])
    # 4. option-level univariate: pick the option with the max of the feature within its row (ties split)
    def pick_acc(score):
        a = 0.0
        for r in rows:
            s = [score(r, j) for j in range(r["k"])]
            m = max(s)
            top = [j for j, v in enumerate(s) if v >= m - 1e-12]
            a += (r["gold"] in top) / len(top)
        return round(a / n, 4)
    opt = {}
    for nm, fn in (("longest", lambda r, j: r["clen"][j]), ("shortest", lambda r, j: -r["clen"][j]),
                   ("first", lambda r, j: -j), ("last", lambda r, j: j),
                   ("neg", lambda r, j: float("kind:neg" in r["all_kinds"][j])),
                   ("abstain", lambda r, j: float("kind:abstain" in r["all_kinds"][j])),
                   ("verbatim", lambda r, j: float("kind:verbatim_in_text" in r["all_kinds"][j]))):
        opt[nm] = pick_acc(fn)
    res["option_pick_acc_vs_chance"] = opt
    # 5. per qform x len-rank (where the signal sits)
    byq = {}
    for q in sorted({r["qform"] for r in rows}, key=str):
        sub = [r for r in rows if r["qform"] == q]
        byq[str(q)] = {"n": len(sub), "k": dict(Counter(r["k"] for r in sub)),
                       "gold_len_rank_share": {str(k): round(sum(r["gold_len_rank"] == k for r in sub) / len(sub), 3) for k in range(4)},
                       "gold_pos_share": {str(k): round(sum(r["pos"] == k for r in sub) / len(sub), 3) for k in range(4)},
                       "gold_longest": round(sum("kind:longest" in r["gold_kinds"] for r in sub) / len(sub), 3),
                       "gold_shortest": round(sum("kind:shortest" in r["gold_kinds"] for r in sub) / len(sub), 3),
                       "chance": round(sum(1 / r["k"] for r in sub) / len(sub), 3)}
    res["by_qform"] = byq
    (OUT / "DMETA_DRIVERS.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("n", "chance", "gold_kind_vs_expected", "option_pick_acc_vs_chance")}, indent=1))
    print("top categorical:", json.dumps(res["categorical_vs_gold_role"][:6]))
    print("top numeric:", json.dumps(res["numeric_vs_gold_role"][:6]))


if __name__ == "__main__":
    {"build": build, "rank": rank}[sys.argv[1]]()
