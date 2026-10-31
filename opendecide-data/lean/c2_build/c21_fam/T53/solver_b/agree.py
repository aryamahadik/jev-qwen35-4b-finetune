"""Agreement harness T53: lane generator (in memory, no rows written) vs solver A gold vs solver B.
Run (from c21_fam):  python3 -m T53.solver_b.agree [--seeds N]
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
    from T53.generator import with_results_output
    rv = {
        "card": spec.card,
        "user_turns": [{"form": t.form, "slots": dict(t.slots)} for t in spec.user_turns],
        "history": [{"author": h.author, "carrier": h.carrier, "path": h.path, "text": h.text} for h in spec.history],
        "text": rendering["text"],
        "view": rendering.get("view", "primary"),
        "tool_output": with_results_output(spec) if rendering.get("view") == "with_results" else "",
        "egress_facts": {"scope_host": spec.egress.scope_host} if spec.egress is not None else None,
    }
    return rv


def generate(offset=0):
    from T53.blocks import plan, build_cell
    from T53.registry import Registry
    reg = Registry()
    drops = []
    specs = []
    for c in plan():
        c2 = copy.deepcopy(c)
        c2.extras["idx"] = c2.extras.get("idx", 0) + offset
        specs += build_cell(c2, drops, None, reg)
    return specs, drops


def compare(specs, label_row, stats, classes, factcls):
    for s in specs:
        for r in s.renderings:
            if not r.get("roundtrip", True):
                continue
            rv = make_rowview(s, r)
            b = label_row(rv)
            a = (s.gold.label, s.gold.reason, s.gold.tier)
            bb = (b["label"], b["reason"], b["tier"])
            stats["rows"] += 1
            stats["label_agree"] += int(a[0] == bb[0])
            stats["triple_agree"] += int(a == bb)
            e = s.egress
            f = b.get("facts") or {}
            if e is not None and f.get("verdict"):
                stats["verdict_agree"] += int(e.verdict == f["verdict"])
                stats["verdict_rows"] += 1
                if e.verdict != f["verdict"]:
                    factcls[("verdict", e.verdict, f["verdict"])] += 1
                for key, ak in (("data_class", e.data_class), ("visibility", e.visibility), ("placement", e.placement),
                                ("channel", e.channel)):
                    stats[key + "_rows"] += 1
                    stats[key + "_agree"] += int(ak == f.get(key))
                    if ak != f.get(key):
                        factcls[(key, ak, f.get(key))] += 1
            if a != bb:
                classes[(s.meta.get("d_kind") or s.meta.get("quad") or s.meta.get("sub") or s.block, s.block, a, bb,
                         tuple(b.get("rules", [])), b.get("opaque"))] += 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    from T53.solver_b.t53_b import label_row
    stats, classes, factcls = collections.Counter(), collections.Counter(), collections.Counter()
    drops_total = 0
    for k in range(a.seeds):
        specs, drops = generate(k * 100000)
        drops_total += len(drops)
        compare(specs, label_row, stats, classes, factcls)
    n = stats["rows"]
    print("rows", n, "generator drops", drops_total)
    print("label_agree %d %.2f%%  triple_agree %d %.2f%%" % (stats["label_agree"], 100.0 * stats["label_agree"] / n,
                                                           stats["triple_agree"], 100.0 * stats["triple_agree"] / n))
    for k in ("verdict", "data_class", "visibility", "placement", "channel"):
        r = stats[k + "_rows"] or stats["verdict_rows"]
        print("fact %-10s agree %d / %d" % (k, stats[k + "_agree"], r))
    print("label-disagreement classes", len(classes), "rows", sum(classes.values()))
    for k, v in classes.most_common(a.top):
        print(v, k)
    print("fact-disagreement classes", len(factcls), "rows", sum(factcls.values()))
    for k, v in factcls.most_common(a.top):
        print(v, k)
