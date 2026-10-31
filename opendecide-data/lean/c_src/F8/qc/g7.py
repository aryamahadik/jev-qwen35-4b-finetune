"""G7 feature z-test (independent F8 checker). C_DATA_SPEC 8 G7 + F8 G0 10.3: one-sided binomial per unigram, bigram
and metadata feature, p0 = 1/k, alpha 0.01 Bonferroni over the tested features (n >= 20).
- Yes/no rows: feature = presence of a lower-cased word unigram/bigram in the model-visible text (card + instructions +
  state) or an observable metadata value (qc_lib.meta_feats: incl. <T> representation, digit count, trailing zeros,
  each rendered SEM id, card version, RANK-order subset class; numbers binned). Two-sided: x = rows with the feature's
  majority label, p = P(Bin(n, .5) >= x).
- Choice rows: feature = a unigram/bigram inside an option text, or an option kind (abstain, longest, shortest, numeric
  first / last, listing-order first / last in the card-without-question), plus row-metadata x option-kind crosses.
  Unit = (row, option set holding f); success = gold holds f; null = Poisson-binomial with p = m_r / k_r (normal approx
  with continuity), both directions.
Each failing feature is reported with its distinct card count. Usage: g7.py <name>"""
import json, math, re, sys
from collections import defaultdict
from scipy.stats import binom, norm
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA = 0.01
N_MIN = 20
TOK = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binlog(v):
    return int(math.log2(1 + abs(v))) * (1 if v >= 0 else -1)


def meta_set(r, s):
    c, n = L.meta_feats(r, s)
    f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        if k.startswith("sem:"):
            f.add(f"meta:{k}")
        elif k.endswith("_log"):
            f.add(f"meta:{k}={int(v)}")
        elif k.startswith(("len_", "ntok", "n_lines", "opt_len", "n_stated")):
            f.add(f"meta:{k}={binlog(v)}")
        else:
            f.add(f"meta:{k}={v}")
    return f


def onum(o):
    n = L.nums(o)
    return n[0] if n else None


def opt_kinds(r):
    opts = r["options"]; ls = [len(o) for o in opts]; out = []
    vals = [onum(o) for o in opts]; nv = sorted(v for v in vals if v is not None)
    v = L.views(r)["cardnoq"] + "\n" + r["state"]; pos = [v.find(o) for o in opts]; ok = sorted(set(p for p in pos if p >= 0))
    for i, o in enumerate(opts):
        k = set()
        if L.is_abstain(o): k.add("kind:abstain")
        if ls[i] == max(ls): k.add("kind:longest")
        if ls[i] == min(ls): k.add("kind:shortest")
        if vals[i] is not None and len(set(nv)) >= 2:
            if vals[i] == nv[0]: k.add("kind:num_first")
            if vals[i] == nv[-1]: k.add("kind:num_last")
        if pos[i] >= 0 and len(ok) >= 2:
            if pos[i] == ok[0]: k.add("kind:list_first")
            if pos[i] == ok[-1]: k.add("kind:list_last")
        out.append(k)
    return out


def pb_test(x, ps):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, 1.0
    z_hi = (x - 0.5 - mu) / math.sqrt(var); z_lo = (mu - x - 0.5) / math.sqrt(var)
    return float(norm.sf(z_hi)), float(norm.sf(z_lo))


def main():
    rows = L.load(NAME); side = L.load_side(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    F = defaultdict(lambda: [0, 0, set()])
    for r in yn:
        g = int(r["gold"]); cid = r["meta"]["card_id"]
        for f in ngrams(L.full_text(r)) | meta_set(r, side[r["id"]]):
            e = F[f]; e[0] += 1; e[1] += g; e[2].add(cid)
    C = defaultdict(lambda: [0, [], set()])
    for r in ch:
        k = len(r["options"]); kinds = opt_kinds(r); cid = r["meta"]["card_id"]; gi = L.gold_index(r)
        ms = {m for m in meta_set(r, side[r["id"]]) if not m.startswith(("meta:sem:", "meta:format_style", "meta:domain_pack",
                                                                          "meta:wording_id"))}
        per = defaultdict(lambda: [0, 0])
        for i, o in enumerate(r["options"]):
            gold = int(i == gi)
            fs = {"opt:" + t for t in ngrams(o)} | kinds[i]
            fs |= {f"x:{m}&{kd}" for m in ms for kd in kinds[i]}
            for f in fs:
                per[f][0] += 1; per[f][1] += gold
        for f, (m, x) in per.items():
            e = C[f]; e[0] += x; e[1].append(m / k); e[2].add(cid)
    tested_yn = {f: v for f, v in F.items() if N_MIN <= v[0] < len(yn)}
    tested_ch = {f: v for f, v in C.items() if len(v[1]) >= N_MIN and 0 < sum(v[1]) < len(v[1])}
    n_tests = len(tested_yn) + len(tested_ch)
    bar = ALPHA / max(1, n_tests)
    fails, near = [], 0
    for f, (n, y, cards) in tested_yn.items():
        x = max(y, n - y); p = float(binom.sf(x - 1, n, 0.5))
        if p < bar:
            fails.append({"part": "yes_no", "feature": f, "n": n, "yes_rate": round(y / n, 4), "p": p, "n_cards": len(cards)})
        elif p < bar * 100:
            near += 1
    for f, (x, ps, cards) in tested_ch.items():
        p_hi, p_lo = pb_test(x, ps)
        if min(p_hi, p_lo) < bar:
            fails.append({"part": "choice", "feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(sum(ps), 2),
                          "dir": "over" if p_hi < p_lo else "under", "p": min(p_hi, p_lo), "n_cards": len(cards)})
        elif min(p_hi, p_lo) < bar * 100:
            near += 1
    fails.sort(key=lambda d: d["p"])
    multi = [f for f in fails if f["n_cards"] > 1]
    out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN, "n_tests": n_tests,
           "bonferroni_p": bar, "n_yes_no_rows": len(yn), "n_choice_rows": len(ch),
           "n_tested_yes_no": len(tested_yn), "n_tested_choice": len(tested_ch),
           "n_fail": len(fails), "n_fail_multi_card": len(multi), "n_fail_single_card": len(fails) - len(multi),
           "near_within_100x": near, "fails": fails[:200], "pass": len(fails) == 0}
    (L.QC / f"g7_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "fails"}))
    for f in fails[:40]:
        print({k: v for k, v in f.items() if k != "feature"} | {"feature_kind": f["feature"].split(":")[0]})


if __name__ == "__main__":
    main()
