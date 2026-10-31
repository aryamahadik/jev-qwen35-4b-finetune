"""Agreement harness T51: lane generator (in memory, no rows written) vs solver A gold vs solver B.
Run (from c21_fam):  python3 -m T51.solver_b.agree [--seeds N]
Counts only; no item text is printed.
"""
import argparse
import collections
import copy
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(os.path.dirname(_HERE))
if _FAM not in sys.path:
    sys.path.insert(0, _FAM)


def make_rowview(spec, rendering):
    m = spec.meta
    return {
        "card": spec.card,
        "entities": copy.deepcopy(m["entities"]),
        "request": {"S": m.get("S"), "B": m.get("B"), "R": m.get("R"), "readings": copy.deepcopy(m["readings"]), "exclusions": copy.deepcopy(m["exclusions"]),
                    "trajectory": copy.deepcopy(m["trajectory"])},
        "user_turns": [{"form": t.form, "slots": dict(t.slots)} for t in spec.user_turns],
        "history": [{"carrier": h.carrier, "text": h.text} for h in spec.history],
        "text": rendering["text"],
        "view": rendering.get("view", "primary"),
    }


def generate(offset=0):
    from T51.blocks import plan, build_cell
    specs, drops = [], []
    for c in plan():
        c2 = copy.deepcopy(c)
        c2.extras["idx"] = c2.extras.get("idx", 0) + offset
        specs += build_cell(c2, drops)
    return specs, drops


def compare(specs, label_row, stats, classes, factcls):
    for s in specs:
        for r in s.renderings:
            if not r.get("roundtrip", True):
                continue
            rv = make_rowview(s, r)
            b = label_row(rv)
            a = s.gold.label
            stats["rows"] += 1
            stats["label_agree"] += int(a == b["label"])
            f = b.get("facts", {})
            for k in ("traj_consistent", "excl_consistent"):
                if k in f:
                    stats[k + "_rows"] += 1
                    stats[k] += int(bool(f[k]))
                    if not f[k]:
                        factcls[(k, s.meta.get("variant"))] += 1
            if f.get("lane_mismatch"):
                factcls[("lane_mismatch", s.meta.get("kind"))] += 1
            if a != b["label"]:
                classes[(s.block, s.meta.get("variant"), s.meta.get("S"), s.meta.get("B"), s.meta.get("R"),
                         s.meta.get("kind"), a, b["label"], tuple(b.get("rules", [])), tuple(b.get("gaps", [])))] += 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    from T51.solver_b.t51_b import label_row
    stats, classes, factcls = collections.Counter(), collections.Counter(), collections.Counter()
    nd = 0
    for k in range(a.seeds):
        specs, drops = generate(k * 100000)
        nd += len(drops)
        compare(specs, label_row, stats, classes, factcls)
    n = stats["rows"]
    print("rows", n, "generator drops", nd)
    print("label_agree %d %.2f%%" % (stats["label_agree"], 100.0 * stats["label_agree"] / n))
    for k in ("traj_consistent", "excl_consistent"):
        print(k, stats[k], "/", stats[k + "_rows"])
    print("label-disagreement classes", len(classes), "rows", sum(classes.values()))
    for k, v in classes.most_common(a.top):
        print(v, k)
    print("fact classes", len(factcls), sum(factcls.values()))
    for k, v in factcls.most_common(a.top):
        print(v, k)
