"""G7 feature z-test (independent F10 checker, check:F10, c-lanes-v3; test as in the F6/F11 checkers). C_DATA_SPEC 8
G7 + F10 G0 8: one-sided binomial per unigram, bigram and metadata feature, p0 = 1/k, alpha 0.01 Bonferroni over all
tested features (n >= 20).
- Yes/no: feature = lower-cased word unigram/bigram present in the model-visible text (card + instructions + state) or
  a visible metadata value (chk_lib.meta_feats), plus F10 yes/no features from visible parsing: asked term first /
  last on the card, asked term string inside the record, asked-term card position (capped 6), terms on card (binned),
  negation word in the question. Both directions: x = rows with the majority label, p = P(Bin(n, .5) >= x).
  Card-adjusted test (leave-one-out card yes rate, Poisson-binomial normal approx.) reported and gated.
- Choice: unit = (row, option set holding f); success = gold holds f; null p = m_r / k_r; Poisson-binomial normal
  approx. with continuity, both directions. Features: option-text n-grams, option kinds (abstain, longest, shortest,
  listed first / last among the options' card positions, option string in the record, visible definition shown with
  the option), and meta x kind crosses (meta without format_style / wording_id / domain_pack).
- Diagnostic only (not gated; G10 judges it): option displayed first in the stored order.
Pass rule (F6 / F11 checkers' rule): no choice failure, no card-adjusted yes/no failure, and no raw (p0 = .5) yes/no
failure spanning > 1 card (a single-card raw failure is that card's designed U[20,80] yes rate). Usage: chk_g7.py <name>"""
import json, math, re, sys
from collections import defaultdict
from scipy.stats import binom, norm
import chk_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA, N_MIN = 0.01, 20
TOK = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")
NEG_RX = re.compile(r"(?i)\b(not|no|never|isn't|doesn't|fails?|lack)\b")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binlog(v):
    return int(math.log2(1 + abs(v))) * (1 if v >= 0 else -1)


def meta_set(r, s):
    c, n = L.meta_feats(r, s)
    f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        f.add(f"meta:{k}={binlog(v) if k.startswith(('len_', 'n_lines', 'opt_len', 'state_max')) else v}")
    return f


def yn_feats(r):
    T = L.card_terms(r); a = L.asked_term(r, T); q = L.split_q(r["instructions"])[0]; f = set()
    f.add(f"f10:n_terms={min(len(T), 12)}")
    if a:
        i = T.index(a); f.add(f"f10:asked_pos={min(i, 6)}")
        if i == 0: f.add("f10:asked_first")
        if i == len(T) - 1: f.add("f10:asked_last")
        if re.search(re.escape(a), r["state"]): f.add("f10:asked_in_record")
    else:
        f.add("f10:asked_not_found")
    f.add(f"f10:q_neg_words={min(len(NEG_RX.findall(q)), 3)}")
    return f


def opt_kinds(r):
    opts = r["options"]; ls = [len(o) for o in opts]; T = L.card_terms(r); out = []
    pos = [T.index(o) if o in T else -1 for o in opts]; ok = sorted(p for p in pos if p >= 0)
    for i, o in enumerate(opts):
        k = set()
        if L.is_abstain(r, o): k.add("kind:abstain")
        if ls[i] == max(ls): k.add("kind:longest")
        if ls[i] == min(ls): k.add("kind:shortest")
        if pos[i] >= 0 and len(ok) >= 2:
            if pos[i] == ok[0]: k.add("kind:list_first")
            if pos[i] == ok[-1]: k.add("kind:list_last")
        if len(o) >= 2 and o in r["state"]: k.add("kind:in_record")
        if L.def_line(r, o): k.add("kind:def_visible")
        out.append(k)
    return out


def pb(x, ps):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, 1.0
    return float(norm.sf((x - 0.5 - mu) / math.sqrt(var))), float(norm.sf((mu - x - 0.5) / math.sqrt(var)))


def main():
    rows, side = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    cy = defaultdict(lambda: [0, 0])
    for r in yn:
        c = cy[r["meta"]["card_id"]]; c[0] += 1; c[1] += int(r["gold"])
    F = defaultdict(lambda: [0, 0, set(), 0.0, 0.0])
    for r in yn:
        g = int(r["gold"]); cid = r["meta"]["card_id"]; n_c, y_c = cy[cid]
        pr = (y_c - g) / (n_c - 1) if n_c > 1 else 0.5
        txt = "\n\n".join([r.get("card") or "", r["instructions"], r["state"]])
        for f in ngrams(txt) | meta_set(r, side.get(r["id"])) | yn_feats(r):
            e = F[f]; e[0] += 1; e[1] += g; e[2].add(cid); e[3] += pr; e[4] += pr * (1 - pr)
    C = defaultdict(lambda: [0, [], set()]); D = [0, 0.0, 0]
    for r in ch:
        k = len(r["options"]); kinds = opt_kinds(r); cid = r["meta"]["card_id"]; gi = L.gold_index(r)
        ms = {m for m in meta_set(r, side.get(r["id"])) if not m.startswith(("meta:format_style", "meta:domain_pack", "meta:wording_id"))}
        per = defaultdict(lambda: [0, 0])
        for i, o in enumerate(r["options"]):
            gold = int(i == gi)
            fs = {"opt:" + t for t in ngrams(o)} | kinds[i] | {f"x:{m}&{kd}" for m in ms for kd in kinds[i]}
            for f in fs:
                per[f][0] += 1; per[f][1] += gold
        for f, (m, x) in per.items():
            e = C[f]; e[0] += x; e[1].append(m / k); e[2].add(cid)
        D[0] += int(gi == 0); D[1] += 1 / k; D[2] += 1
    tested_yn = {f: v for f, v in F.items() if N_MIN <= v[0] < len(yn)}
    tested_ch = {f: v for f, v in C.items() if len(v[1]) >= N_MIN and 0 < sum(v[1]) < len(v[1])}
    n_tests = len(tested_yn) + len(tested_ch); bar = ALPHA / max(1, n_tests)
    fails, adj, near = [], [], 0
    for f, (n, y, cards, mu, var) in tested_yn.items():
        x = max(y, n - y); p = float(binom.sf(x - 1, n, 0.5))
        if p < bar:
            fails.append({"part": "yes_no", "feature": f if not f[0].isalnum() or ":" in f else "<ngram>", "ngram": f if ":" not in f else None,
                          "n": n, "yes_rate": round(y / n, 4), "p": p, "n_cards": len(cards)})
        elif p < bar * 100:
            near += 1
        if var > 0:
            pa = float(min(norm.sf((y - 0.5 - mu) / math.sqrt(var)), norm.sf((mu - y - 0.5) / math.sqrt(var))))
            if pa < bar:
                adj.append({"feature": f, "n": n, "yes_rate": round(y / n, 4), "card_expected_rate": round(mu / n, 4), "p": pa, "n_cards": len(cards)})
    for f, (x, ps, cards) in tested_ch.items():
        ph, pl = pb(x, ps)
        if min(ph, pl) < bar:
            fails.append({"part": "choice", "feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(sum(ps), 2),
                          "dir": "over" if ph < pl else "under", "p": min(ph, pl), "n_cards": len(cards)})
        elif min(ph, pl) < bar * 100:
            near += 1
    fails.sort(key=lambda d: d["p"]); adj.sort(key=lambda d: d["p"])
    ynr = [f for f in fails if f["part"] == "yes_no"]; chf = [f for f in fails if f["part"] == "choice"]
    ynm = [f for f in ynr if f["n_cards"] > 1]
    kinds = {f: {"n_rows": len(v[1]), "gold_hits": v[0], "expected": round(sum(v[1]), 2)} for f, v in sorted(tested_ch.items()) if f.startswith("kind:")}
    f10y = {f: {"n": v[0], "yes_rate": round(v[1] / v[0], 4)} for f, v in sorted(tested_yn.items()) if f.startswith("f10:")}
    ok = not chf and not adj and not ynm
    out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN, "n_tests": n_tests, "bonferroni_p": bar,
           "n_yes_no_rows": len(yn), "n_choice_rows": len(ch), "n_tested_yes_no": len(tested_yn), "n_tested_choice": len(tested_ch),
           "n_fail_choice": len(chf), "n_fail_yes_no_raw": len(ynr), "n_fail_yes_no_raw_multi_card": len(ynm),
           "n_fail_yes_no_card_adjusted": len(adj), "near_within_100x": near,
           "diag_gold_displayed_first": {"rows": D[2], "gold_first": D[0], "expected": round(D[1], 1),
                                         "note": "stored option order; the trainer re-shuffles; judged in G10"},
           "pass_rule": "no choice failure, no card-adjusted yes/no failure, no raw yes/no failure spanning > 1 card",
           "kind_features": kinds, "f10_yes_no_features": f10y,
           "fails_choice": chf[:60], "fails_yes_no_raw_multi_card": ynm[:60], "fails_yes_no_raw_single_card": len(ynr) - len(ynm),
           "card_adjusted_fails": adj[:60], "pass": ok}
    for d in out["fails_yes_no_raw_multi_card"]:
        d.pop("ngram", None)
    (L.QC / f"g7_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("n_tests", "n_fail_choice", "n_fail_yes_no_raw", "n_fail_yes_no_raw_multi_card",
                                          "n_fail_yes_no_card_adjusted", "near_within_100x", "pass")}))


if __name__ == "__main__":
    main()
