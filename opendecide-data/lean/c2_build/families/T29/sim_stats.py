"""c2_build/families/T29/sim_stats.py: pilot-size statistics of the row mix over many seed bases (no rendering; nothing
is written). Prints the mean / sd / range of the numbers the Stage B pilot gates look at.

  ../.venv/bin/python -B -m families.T29.sim_stats [--runs 20] [--rows 1000] [--set NAME=VALUE ...]   (from lean/c2_build)
"""
from __future__ import annotations

import argparse
import ast
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T29 import balance_sim as BS  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=20)
    ap.add_argument("--rows", type=int, default=1000)
    ap.add_argument("--first", type=int, default=40)
    ap.add_argument("--set", nargs="*", default=[])
    a = ap.parse_args(argv)
    from families.T29 import plugin as P
    for kv in a.set:
        k, v = kv.split("=", 1)
        setattr(P, k, ast.literal_eval(v))
    cols = defaultdict(list)
    parts = defaultdict(list)
    with BS.open_plugin() as kit:
        pl = kit.plugin
        for b in range(a.first, a.first + a.runs):
            rows = BS.simulate(pl, a.rows, b * 1_000_000 + 900_000)
            n = len(rows)
            yn = [r for r in rows if r["qtype"] == "noul"]
            cv = [r for r in rows if r["qform"] == "ch_verdict"]
            shown = [r for r in cv if r["shown"]]
            qf = pl.QFORMS
            comp = [r for r in yn if r["role"] == "complement"]
            d = defaultdict(int)
            for r in yn:
                d[r["role"]] += 2 * r["answer"] - 1
            for k, v in d.items():
                parts[k].append(v)
            cols["yes_rate"].append(sum(r["answer"] for r in yn) / len(yn))
            cols["yes_no_share"].append(len(yn) / n)
            cols["twin_share"].append(sum(r["role"] == "twin" for r in rows) / n)
            cols["equiv_share"].append(sum(r["role"] == "equiv" for r in rows) / n)
            cols["attack_share"].append(sum(r["role"] == "attack" for r in rows) / n)
            cols["premise_share"].append(sum(r["role"] == "premise_removal" for r in rows) / n)
            cols["complement_rows_of_yes_no"].append(len(comp) / len(yn))
            cols["syntactic_share_of_yes_no"].append(sum(qf[r["qform"]].complement_kind == "syntactic" for r in yn)
                                                     / len(yn))
            cols["non_syntactic_share_of_pairs"].append(
                sum(qf[r["qform"]].complement_kind != "syntactic" for r in comp) / max(1, len(comp)))
            cols["yes_is_bad"].append(sum(bool(qf[r["qform"]].yes_is_bad) for r in yn) / len(yn))
            cols["cannot_of_shown"].append(sum(r["answer"] == "cannot" for r in shown) / max(1, len(shown)))
            cols["deep_share"].append(sum(r["deep"] for r in rows) / n)
            cols["ch_rule_none_gold"].append(sum(r["answer"] == "none" for r in rows if r["qform"] == "ch_rule")
                                             / max(1, sum(r["qform"] == "ch_rule" for r in rows)))
            for q in ("yn_go", "yn_ask", "yn_refuse", "yn_not_go"):
                rs = [r for r in yn if r["qform"] == q]
                if rs:
                    cols["yes_" + q].append(sum(r["answer"] for r in rs) / len(rs))
    print(f"{a.runs} runs x {a.rows} rows")
    for k, v in cols.items():
        print(f"  {k:32s} mean {st.mean(v):.4f} sd {st.pstdev(v):.4f} min {min(v):.4f} max {max(v):.4f}")
    print("  yes - no by role (rows): " + ", ".join(f"{k} {st.mean(v):+.1f} (sd {st.pstdev(v):.1f})"
                                                   for k, v in parts.items()))
    y = cols["yes_rate"]
    print(f"  yes rate outside 50 +- 2 pp: {sum(abs(x - 0.5) > 0.02 for x in y)}/{len(y)}; yes/no share outside 45-55%:"
          f" {sum(not 0.45 <= x <= 0.55 for x in cols['yes_no_share'])}/{len(y)}; twin share outside 20-25%: "
          f"{sum(not 0.20 <= x <= 0.25 for x in cols['twin_share'])}/{len(y)}")


if __name__ == "__main__":
    main()
