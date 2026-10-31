"""T56 solver A vs solver B agreement harness (IN MEMORY ONLY; no rows written; no item text printed).
Usage: python3 -I solver_b/agreement_harness.py [total_per_seed] [seed ...]"""
import collections
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
ROOT = os.path.dirname(FAM)
for p in (HERE, ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

import t56_solver_b as sb  # noqa: E402


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(total=1000, seeds=("b-agree-1",)):
    import t56_generator as gen
    n = 0
    per, agree, reason_ok, letter_ok = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    classes, flags, abstains = collections.Counter(), collections.Counter(), collections.Counter()
    for seed in seeds:
        for r in gen.generate_in_memory(total=total, seed=seed, standin=True):
            res = sb.solve(r)
            s = r["sub_block"]
            n += 1
            per[s] += 1
            for f in res.flags:
                flags[(s, f)] += 1
            if res.abstain:
                abstains[(s, res.abstain)] += 1
            if res.label == r["gold"]:
                agree[s] += 1
                if res.reason == r["gold_reason"]:
                    reason_ok[s] += 1
                if res.letter == r["gold_letter"]:
                    letter_ok[s] += 1
            if res.label != r["gold"] or res.reason != r["gold_reason"]:
                classes[(s, r["fault"], "A=%s/%s" % (r["gold"], r["gold_reason"]), "B=%s/%s" % (res.label, res.reason),
                         "|".join(res.reasons_all), res.abstain or "-")] += 1
    return n, per, agree, reason_ok, letter_ok, classes, flags, abstains


def main(argv):
    total = int(argv[1]) if len(argv) > 1 else 1000
    seeds = tuple(argv[2:]) or ("b-agree-1",)
    n, per, agree, reason_ok, letter_ok, classes, flags, abstains = run(total, seeds)
    a = sum(agree.values())
    ar = sum(reason_ok.values())
    print("rows", n, "label agree", a, "%.4f%%" % (100.0 * a / max(1, n)), " label+reason agree", ar, "%.4f%%" % (100.0 * ar / max(1, n)))
    for s in sorted(per):
        print("  %-14s n=%5d label=%5d (%.3f%%) label+reason=%5d (%.3f%%) letter_ok(of label-agree)=%d" % (
            s, per[s], agree[s], 100.0 * agree[s] / per[s], reason_ok[s], 100.0 * reason_ok[s] / per[s], letter_ok[s]))
    print("disagreement classes (count: sub-block, fault, A label/reason, B label/reason, B reasons-all, abstain):")
    for k, c in sorted(classes.items(), key=lambda kv: -kv[1]):
        print("  ", c, k)
    print("B abstains:", dict(abstains))
    print("B flags:", dict(flags))
    print("sha256 solver_b:", sha(os.path.join(HERE, "t56_solver_b.py")))
    print("sha256 generator:", sha(os.path.join(FAM, "t56_generator.py")))
    print("sha256 solver_a:", sha(os.path.join(FAM, "t56_solver_a.py")))


if __name__ == "__main__":
    main(sys.argv)
