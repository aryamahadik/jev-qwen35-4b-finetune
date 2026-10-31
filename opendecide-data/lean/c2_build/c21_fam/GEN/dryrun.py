"""Tiny dry run: build 20 in-memory GEN examples (one per form) with the TEST-ONLY wording pool and PROVISIONAL names.
Never writes a file. For unit tests and for a human glance only; these are NOT rows.
    python3 dryrun.py            -> prints a one-line summary per example
    python3 dryrun.py --show     -> also prints each stem and options
"""
import sys

from builder import Builder, validate_row
from gen_common import FORMS, GenAllow, make_testonly_pool


def build_examples(seed="dryrun-1", n_per_form=1, split="train"):
    pool = make_testonly_pool()
    b = Builder(seed, pool, allow=GenAllow(), provisional=True, mode="dry")
    rows = []
    for form in FORMS:
        got = 0
        i = 0
        while got < n_per_form and i < 50:
            for r in b.unit(form, split, i, pair_prob=0.0):
                rows.append(r)
                got += 1
            i += 1
    return rows


def main(argv):
    rows = build_examples()
    allow = GenAllow()
    bad = 0
    for r in rows:
        probs = validate_row(r, allow)
        bad += bool(probs)
        print("%-6s %-5s bin=%-4s carrier=%-12s tok=%-4d label=%s %s" % (r["form"], r["split"], r["difficulty"]["bin"], r["carrier"], r["tokens_est"], r["label_letter"], probs or "ok"))
        if "--show" in argv:
            print("   " + r["stem"].replace("\n", "\n   "))
            for i, o in enumerate(r["options"]):
                print("   %s) %s" % ("ABCD"[i], o))
    print("%d examples, %d with problems (TEST-ONLY pool, provisional names; not rows)" % (len(rows), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
