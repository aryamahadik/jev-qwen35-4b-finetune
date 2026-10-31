"""G7 feature z-test (C_DATA_SPEC v4 8 G7): one-sided binomial per unigram, bigram and metadata feature, p0 = 1/k,
alpha 0.01 Bonferroni over the tested features (features with n >= 20 units). Independent re-run on public-2.
Test sets (each with its own Bonferroni): per dataset and pooled, on rows_r1 and on rows_r1 + reserve_r1.
- Yes/no rows: feature = presence of a lower-cased word unigram / bigram in the model-visible text (card +
  instructions + state) or a metadata value (framing, wording_id, card_id, card_route, defs_style, format_style,
  depth, negation count k_all of the question). Both directions: x = rows with the feature's majority label,
  p = P(Bin(n, .5) >= x).
- Choice rows: feature = a unigram / bigram inside an option, an option kind (abstain, longest, shortest, numeric
  max / min, option text in the state, option text in the instructions) and framing x option kind. Unit = a row where
  m (1 <= m < k) options hold f; success = the gold holds f; null = Poisson-binomial with p = m / k (normal approx with
  continuity), both directions. The stored option order is not a feature: the trainer re-permutes options.
"""
import math
import re
import sys
from collections import defaultdict

from scipy.stats import binom, norm

from qclib import DATASETS, LEAN, load_all, write_gate

sys.path.insert(0, str(LEAN / "c_src" / "common"))
import negcount  # noqa: E402

ALPHA, NMIN = 0.01, 20
ABSTAIN = ("None of these", "None of the listed values")
WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def grams(text):
    w = WORD.findall(str(text).lower())
    return set(w) | {a + " " + b for a, b in zip(w, w[1:])}


def num(o):
    try:
        return float(str(o).replace(",", "").strip().rstrip("%"))
    except ValueError:
        return None


def yn_feats(r):
    f = {"t:" + g for g in grams((r.get("card") or "") + " " + r["instructions"] + " " + r["state"])}
    m = r["meta"]
    for k in ("framing", "wording_id", "card_id", "card_route", "defs_style", "format_style", "depth"):
        f.add(f"m:{k}={m.get(k)}")
    f.add(f"m:k_all={negcount.count(r['instructions']).k_all}")
    return f


def opt_feats(r):
    """[set of features per option]"""
    opts = r["options"]
    L = [len(o) for o in opts]
    nums = [num(o) for o in opts]
    nn = [x for x in nums if x is not None]
    st, ins = r["state"].lower(), r["instructions"].lower()
    fr = r["meta"]["framing"]
    out = []
    for i, o in enumerate(opts):
        kinds = set()
        if o in ABSTAIN:
            kinds.add("abstain")
        if L[i] == max(L):
            kinds.add("longest")
        if L[i] == min(L):
            kinds.add("shortest")
        if nums[i] is not None and len(nn) >= 2:
            if nums[i] == max(nn):
                kinds.add("num_max")
            if nums[i] == min(nn):
                kinds.add("num_min")
        if o.lower() in st:
            kinds.add("in_state")
        if o.lower() in ins:
            kinds.add("in_instructions")
        f = {"o:" + g for g in grams(o)} | {"k:" + k for k in kinds} | {f"x:{fr}|{k}" for k in kinds}
        out.append(f)
    return out


def test_yn(rows):
    cnt = defaultdict(lambda: [0, 0])
    for r in rows:
        for f in yn_feats(r):
            c = cnt[f]
            c[0] += 1
            c[1] += int(r["gold"])
    tested = {f: c for f, c in cnt.items() if c[0] >= NMIN}
    bar = ALPHA / max(1, len(tested))
    fails = []
    for f, (n, y) in tested.items():
        x = max(y, n - y)
        p = float(binom.sf(x - 1, n, .5))
        if p < bar:
            fails.append([f, n, y, p])
    return len(tested), bar, sorted(fails, key=lambda z: z[3])


def test_ch(rows):
    acc = defaultdict(lambda: [0, 0.0, 0.0, 0])   # units, successes, E, Var
    for r in rows:
        of = opt_feats(r)
        k = len(r["options"])
        gi = r["options"].index(r["gold"])
        allf = set().union(*of)
        for f in allf:
            m = sum(f in s for s in of)
            if m == k:
                continue
            p = m / k
            a = acc[f]
            a[0] += 1
            a[1] += int(f in of[gi])
            a[2] += p
            a[3] += p * (1 - p)
    tested = {f: a for f, a in acc.items() if a[0] >= NMIN}
    bar = ALPHA / max(1, len(tested))
    fails = []
    for f, (n, s, e, v) in tested.items():
        sd = math.sqrt(v) if v > 0 else 1e-9
        p_up = float(norm.sf((s - .5 - e) / sd))
        p_dn = float(norm.cdf((s + .5 - e) / sd))
        p = min(p_up, p_dn)
        if p < bar:
            fails.append([f, n, int(s), round(e, 1), p, "up" if p_up < p_dn else "down"])
    return len(tested), bar, sorted(fails, key=lambda z: z[4])


def main():
    data = load_all()
    nums, allfails = {}, []
    for setname, rows in (("rows_r1", data["rows_r1"]), ("rows_plus_reserve", data["rows_r1"] + data["reserve_r1"])):
        for ds in DATASETS + ("pooled",):
            R = rows if ds == "pooled" else [r for r in rows if r["source"] == ds]
            yn = [r for r in R if r["qtype"] == "noul"]
            ch = [r for r in R if r["qtype"] == "choice"]
            d = {}
            if yn:
                n, bar, f = test_yn(yn)
                d["yes_no"] = {"rows": len(yn), "features_tested": n, "bonferroni_p": bar, "fails": len(f), "top_fails": f[:8]}
                allfails += [f"{setname}|{ds}|yn|{x[0]}" for x in f]
            if ch:
                n, bar, f = test_ch(ch)
                d["choice"] = {"rows": len(ch), "features_tested": n, "bonferroni_p": bar, "fails": len(f), "top_fails": f[:8]}
                allfails += [f"{setname}|{ds}|ch|{x[0]}" for x in f]
            nums[f"{setname}|{ds}"] = d
    ok = not allfails
    write_gate("G7", ok, nums, fails_total=len(allfails), fails_list=allfails[:60])
    print("G7", ok, len(allfails), allfails[:12])


if __name__ == "__main__":
    main()
