"""T26 fix iteration 1: calibration of the overlay and the abstain balance on a seed range that is NOT the pilot's.

Builds units for N seeds per training sampler (real pools via families/T26/loader.py, in memory, no G15), then prints the
shares the G10 / overlay / G6-G7 bars read: verdict thirds, none share per k, longest-option gold, twin / equiv / attack
shares, yes/no share, yes rate, yes_is_bad, Mode F share, register shares. Nothing is written.

  ../../.venv/bin/python -B pilot_runs/T26_i1_work/calib.py --n 1500 --base 2000000
"""
import argparse
import collections
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))

from c2_kit import choiceplan, pipeline  # noqa: E402
from families.T26 import loader as LD  # noqa: E402
from families.T26 import plugin as P  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--base", type=int, default=2_000_000)
    ap.add_argument("--samplers", default="S1,S2,S3,S4")
    a = ap.parse_args()
    with LD.open_t26() as kit:
        pl, ctx = kit.plugin, kit.ctx
        units, bad, specs = [], collections.Counter(), []
        for smp in a.samplers.split(","):
            for k in range(a.n):
                spec = pl.sample(a.base + k, smp)
                u = pipeline.build_unit(pl, spec, ctx, run_g15=False)
                if u.ok:
                    units.append(u)
                    specs.append(spec)
                else:
                    bad[u.problems[0][0]] += 1
        rows = [r for u in units for r in u.rows]
        n = len(rows)
        yn = [r for r in rows if r["qtype"] == "noul"]
        out = {"units": len(units), "dropped": dict(bad), "rows": n, "yes_no_share": round(len(yn) / n, 4),
               "yes_rate": round(sum(r["gold"] for r in yn) / len(yn), 4)}
        qf = pl.QFORMS
        out["yes_is_bad"] = round(sum(1 for r in yn if qf[r["meta"]["qform"]].yes_is_bad) / len(yn), 4)
        kinds = collections.Counter(r["meta"]["twin_kind"] for r in rows)
        out["twin_share"] = round(kinds["minimal_edit"] / n, 4)
        out["equiv_share"] = round(kinds["equiv"] / n, 4)
        out["attack_share"] = round(kinds["attack"] / n, 4)
        out["complement_rows_of_yes_no"] = round(2 * kinds["complement"] / len(yn), 4)
        legit = sum(1 for sp, u in zip(specs, units) if P._decide(pl._statuses(sp)) == "apply"
                    and "|URG|" in u.rows[0]["meta"]["c2"]["skin_id"])
        out["legit_alarming_of_base"] = round(legit / len(units), 4)
        out["apply_of_base"] = round(sum(1 for sp in specs if P._decide(pl._statuses(sp)) == "apply") / len(units), 4)
        edge = collections.Counter(e for u in units for e in u.rows[0]["meta"]["edge"])
        out["lookalike_of_base"] = round(edge["lookalike_domain"] / len(units), 4)
        out["right_domain_missing_addendum_of_base"] = round(edge["right_domain_missing_addendum"] / len(units), 4)
        erow = collections.Counter(e for r in rows for e in r["meta"]["edge"])
        out["lookalike_of_rows"] = round(erow["lookalike_domain"] / n, 4)
        out["right_domain_missing_addendum_of_rows"] = round(erow["right_domain_missing_addendum"] / n, 4)
        out["mode_f"] = round(sum(1 for r in rows if r["meta"]["c2"]["author_mode"] == "F") / n, 4)
        regs = collections.Counter(r["meta"]["c2"]["register"] for r in rows)
        out["register_max"] = round(max(regs.values()) / n, 4)
        # verdict thirds over every emitted ch_verdict row (base + twin + equiv + inv), by role
        sets = [rr.option_set for u in units for rr in u.rendered if rr.option_set is not None]
        vr = [rr for u in units for rr in u.rendered if rr.row["meta"]["qform"] == "ch_verdict"]
        c = collections.Counter(rr.option_set.gold.key for rr in vr)
        tot = sum(c.values())
        out["verdict_all"] = {k: round(v / tot, 4) for k, v in sorted(c.items())}
        for kind in (None, "minimal_edit", "equiv", "attack"):
            cc = collections.Counter(rr.option_set.gold.key for rr in vr if rr.row["meta"]["twin_kind"] == kind)
            t = sum(cc.values())
            out[f"verdict_{kind}"] = {"n": t, **{k: round(v / t, 3) for k, v in sorted(cc.items())}}
        fr = [rr for u in units for rr in u.rendered if rr.row["meta"]["qform"] == "ch_failing"]
        per_k = collections.defaultdict(lambda: [0, 0])
        for rr in fr:
            k = len(rr.option_set.options)
            per_k[k][0] += 1
            per_k[k][1] += rr.option_set.gold.key == "none"
        out["none_by_k"] = {k: {"rows": v[0], "none": v[1], "share": round(v[1] / v[0], 4), "target": round(1 / k, 4)}
                            for k, v in sorted(per_k.items())}
        for kind in (None, "minimal_edit", "equiv", "attack"):
            xs = [rr for rr in fr if rr.row["meta"]["twin_kind"] == kind]
            out[f"failing_{kind}"] = {"n": len(xs), "none_share": round(sum(rr.option_set.gold.key == "none" for rr in xs)
                                                                      / max(1, len(xs)), 3),
                                      "expected": round(sum(1 / len(rr.option_set.options) for rr in xs) / max(1, len(xs)), 3)}
        out["plan_report"] = choiceplan.plan_report(sets)
        print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
