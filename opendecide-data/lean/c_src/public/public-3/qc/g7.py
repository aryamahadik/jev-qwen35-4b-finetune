#!/usr/bin/env python3
"""G7 feature z-test, public-3 (independent checker, prep5/B4; counts only, never prints row text or n-grams of
record text: a failing text feature is reported by kind and counts only, metadata features by name).

Spec 8 G7: one-sided binomial per unigram, bigram and metadata feature; p0 = 1/k; alpha 0.01 Bonferroni over the
tested features (a feature is tested when it occurs in >= 20 units, the F11 checker's convention). No feature may fail.
Sample: rows_r1 + reserve (the mixed files).
Yes/no (noul): feature = a lower-cased word unigram / bigram present anywhere in the model-visible text (card +
  instructions + state), or a metadata value (qc/g6.py meta_d). x = rows with the feature's majority label,
  p = P(Bin(n, .5) >= x).
Choice: unit = (row, options holding f); f = a unigram / bigram inside an option text, an option kind (longest,
  shortest, card first / last, canonical index) or a row-metadata x option-kind cross; success = gold holds f; null =
  Poisson-binomial with p_r = m_r / k_r (normal approximation with continuity), both directions.
Writes qc/g7.json."""
import json, math, re
from collections import defaultdict
from scipy.stats import binom, norm
import qclib as Q
from g6 import meta_d, opt_feats

ALPHA, N_MIN = 0.01, 20
TOK = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")


def ngrams(t):
    w = TOK.findall((t or "").lower())
    return set(w) | {a + " " + b for a, b in zip(w, w[1:])}


def main():
    rows = [r for n in Q.MIXED for r in Q.load(n)]
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    tests = []   # (kind, name or None, n, p, majority share)
    cnt = defaultdict(lambda: [0, 0])
    for r in yn:
        fs = {("text", f) for f in ngrams("\n".join([r["card"] or "", r["instructions"], r["state"] or ""]))}
        fs |= {("meta", f) for f in meta_d(r)}
        for f in fs:
            cnt[f][0] += 1
            cnt[f][1] += r["gold"] == 1
    for (kind, f), (n, yv) in cnt.items():
        if n >= N_MIN:
            x = max(yv, n - yv)
            tests.append(("yn_" + kind, f, n, float(binom.sf(x - 1, n, 0.5)), round(x / n, 3)))
    # choice
    acc = defaultdict(lambda: [0.0, 0.0, 0.0, 0])   # successes, expected, variance, units
    for r in ch:
        o, gi = r["options"], r["options"].index(r["gold"])
        k = len(o)
        hold = defaultdict(set)
        for i, fd in opt_feats(r):
            for f in ngrams(o[i]) if not (isinstance(r["meta"].get("record_uid"), list)
                                          and len(r["meta"]["record_uid"]) > 1) else ():
                hold[("ch_text", f)].add(i)
            for f in fd["d"]:
                hold[("ch_meta_x_kind", f)].add(i)
                hold[("ch_kind", f.split("|", 1)[1])].add(i)
        for f, idx in hold.items():
            if len(idx) == k:
                continue                              # every option holds f: no information
            p0 = len(idx) / k
            a = acc[f]
            a[0] += gi in idx
            a[1] += p0
            a[2] += p0 * (1 - p0)
            a[3] += 1
    for (kind, f), (s, e, v, n) in acc.items():
        if n >= N_MIN and v > 0:
            z = (abs(s - e) - 0.5) / math.sqrt(v)
            tests.append((kind, f, n, float(norm.sf(z)), round(s / n, 3)))
    bar = ALPHA / max(1, len(tests))
    fails = [t for t in tests if t[3] < bar]
    by_kind = defaultdict(lambda: [0, 0])
    for t in tests:
        by_kind[t[0]][0] += 1
        by_kind[t[0]][1] += t[3] < bar
    rep_fail = [{"kind": t[0], "feature": t[1] if "meta" in t[0] or t[0] == "ch_kind" else None, "n": t[2],
                 "p": t[3], "share": t[4]} for t in sorted(fails, key=lambda t: t[3])[:50]]
    out = {"gate": "G7", "pass": not fails, "alpha": ALPHA, "n_min": N_MIN, "n_tests": len(tests),
           "bonferroni_p": bar, "yn_rows": len(yn), "choice_rows": len(ch),
           "tests_and_fails_by_kind": {k: {"tests": v[0], "fails": v[1]} for k, v in by_kind.items()},
           "min_p": min(t[3] for t in tests), "fails": rep_fail}
    (Q.HERE / "g7.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("pass", "n_tests", "bonferroni_p", "min_p", "tests_and_fails_by_kind")}))
    for f in rep_fail[:15]:
        print(f)


if __name__ == "__main__":
    main()
