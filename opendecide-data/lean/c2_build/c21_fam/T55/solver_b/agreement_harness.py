"""T55 solver A vs solver B agreement harness (IN MEMORY ONLY; no rows written, no item text printed).
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

import t55_solver_b as sb  # noqa: E402
import t55_render_b as rb  # noqa: E402


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(total=1000, seeds=("b-agree-1",)):
    import t55_generator as gen
    n = 0
    per, agree, letter_bad = collections.Counter(), collections.Counter(), collections.Counter()
    classes, flags, abstains = collections.Counter(), collections.Counter(), collections.Counter()
    ragree, rdis, rabs, rcls = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for seed in seeds:
        for r in gen.generate_in_memory(total=total, seed=seed, standin=True):
            kind, val, _fam = rb.solve_text(r["rendered"]["text"])
            if kind == "abstain":
                rabs[(r["sub_block"], val)] += 1
            elif val == r["gold_letter"]:
                ragree[r["sub_block"]] += 1
            else:
                rdis[r["sub_block"]] += 1
                rcls[(r["sub_block"], "A=" + str(r["gold"]), r.get("entry"))] += 1
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
                if res.letter != r["gold_letter"]:
                    letter_bad[s] += 1
            else:
                classes[(s, "A=" + str(r["gold"]), "B=" + str(res.label), r.get("entry"), res.abstain or "-")] += 1
    return n, per, agree, letter_bad, classes, flags, abstains, (ragree, rdis, rabs, rcls)


def b6_reading_report(total, seeds):
    """Agreement of the two coded B6 readings against solver A (labels only)."""
    import t55_generator as gen
    out = {}
    for reading in ("last_step", "window"):
        ok = tot = 0
        for seed in seeds:
            for r in gen.generate_in_memory(total=total, seed=seed, standin=True):
                if r["sub_block"] == "b6_loop_poll":
                    tot += 1
                    ok += int(sb.solve_b6(sb.strip_gold(r), reading=reading).label == r["gold"])
        out[reading] = (ok, tot)
    return out


def main(argv):
    total = int(argv[1]) if len(argv) > 1 else 1000
    seeds = tuple(argv[2:]) or ("b-agree-1",)
    n, per, agree, letter_bad, classes, flags, abstains, rr = run(total, seeds)
    a = sum(agree.values())
    print("rows", n, "agree", a, "agreement %.4f%%" % (100.0 * a / max(1, n)))
    for s in sorted(per):
        print("  %-18s n=%5d agree=%5d %.3f%% letter_mismatch=%d" % (s, per[s], agree[s], 100.0 * agree[s] / per[s], letter_bad[s]))
    print("disagreement classes (count, sub-block, A, B, entry, abstain):")
    for k, c in sorted(classes.items(), key=lambda kv: -kv[1]):
        print("  ", c, k)
    print("B abstains:", dict(abstains))
    print("B flags:", dict(flags))
    ragree, rdis, rabs, rcls = rr
    print("RENDER OBSERVABILITY PARSE (text only; an abstain is an observability drop, not a disagreement):")
    for s in sorted(per):
        dec = ragree[s] + rdis[s]
        print("  %-18s decided=%5d agree=%5d disagree=%3d abstain=%3d coverage=%.1f%% agree_of_decided=%.3f%%" % (
            s, dec, ragree[s], rdis[s], per[s] - dec, 100.0 * dec / per[s], 100.0 * ragree[s] / max(1, dec)))
    for k, c in sorted(rcls.items(), key=lambda kv: -kv[1]):
        print("    render disagreement:", c, k)
    print("  render abstains:", dict(rabs))
    print("B6 reading comparison (agree/total):", b6_reading_report(total, seeds))
    print("sha256 solver_b:", sha(os.path.join(HERE, "t55_solver_b.py")))
    print("sha256 render_b:", sha(os.path.join(HERE, "t55_render_b.py")))
    print("sha256 generator:", sha(os.path.join(FAM, "t55_generator.py")))
    print("sha256 solver_a:", sha(os.path.join(FAM, "t55_solver_a.py")))


if __name__ == "__main__":
    main(sys.argv)
