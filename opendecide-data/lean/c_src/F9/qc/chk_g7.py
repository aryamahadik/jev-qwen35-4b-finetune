"""G7 feature z-test (independent F9 checker, check:F9, c-lanes-v3). C_DATA_SPEC 8 G7 + F9 G0 1.9 / 5: one-sided
binomial per unigram, bigram and metadata feature, p0 = 1/k, alpha 0.01 Bonferroni over all tested features (n >= 20).
- Yes/no: feature = lower-cased word unigram/bigram present in the model-visible text (card + instructions + state) or a
  visible metadata value (chk_lib.meta_feats), plus F9 visible nuisance features (G0 1.9 / 5): stated null token
  present in the text, identical repeated line, repeated first-ID on two lines, attack row, looked-up ID listed / first
  row / last row / above every listed ID of its prefix, question-token overlap with the text (count and max
  frequency, binned). Both directions: x = rows with the majority label, p = P(Bin(n, .5) >= x).
  Card-adjusted test (leave-one-out card yes rate, Poisson-binomial normal approx.) reported and gated.
- Choice: unit = (row, option set holding f); success = gold holds f; null p = m_r / k_r; Poisson-binomial normal
  approx. with continuity, both directions. Features: option-text n-grams, option kinds (abstain kinds, longest,
  shortest, numeric max / min, in text, first / last in the text among the options, mentioned in the question, record
  set closest to the other options (F9-A35), set size), and meta x kind crosses (meta without format_style /
  wording_id / domain_pack).
Pass rule (as the F6 / F10 / F11 checkers): no choice failure, no card-adjusted yes/no failure, and no raw (p0 = .5)
yes/no failure spanning > 1 card. Usage: chk_g7.py <name>"""
import json, math, re, sys
from collections import defaultdict
from scipy.stats import binom, norm
import chk_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA, N_MIN = 0.01, 20
TOK = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")
ID_RX = re.compile(r"\b([A-Z][A-Z0-9]{0,6})-(\d{2,7})\b")
NULL_RX = re.compile(r"(?:[\"'“«]([^\"'”»\n]{1,20})[\"'”»]|\b([A-Za-z/_.-]{1,12}))\s+means the value is not known")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binlog(v):
    return int(math.log2(1 + abs(v))) * (1 if v >= 0 else -1)


def meta_set(r, s):
    c, n = L.meta_feats(r, s)
    f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        f.add(f"meta:{k}={binlog(v) if k.startswith(('len_', 'n_lines', 'opt_len', 'state_max', 'q_max', 'sc_real')) else v}")
    return f


def vis_feats(r, s, qfreq):
    st = r["state"]; v = L.views(r, s); f = set()
    if r.get("role") == "attacked":
        f.add("f9:attack_row")
    for m in NULL_RX.finditer(v["cardnoq"]):
        tokn = (m.group(1) or m.group(2) or "").strip()
        if tokn and re.search(r"(?<![\w-])" + re.escape(tokn) + r"(?![\w-])", st):
            f.add("f9:null_token_present")
    lines = [l.strip() for l in st.split("\n") if len(l.strip()) > 8]
    if len(lines) != len(set(lines)):
        f.add("f9:repeated_line")
    firsts = [m.group(0) for m in (ID_RX.search(l) for l in st.split("\n")) if m]
    if len(firsts) != len(set(firsts)):
        f.add("f9:repeated_first_id")
    qids = [m for m in ID_RX.finditer(v["q"])]
    if qids:
        qi = qids[0].group(0); pre = qids[0].group(1)
        same = [int(m.group(2)) for m in ID_RX.finditer(st) if m.group(1) == pre]
        f.add("f9:qid_listed" if qi in st else "f9:qid_unlisted")
        if same and int(qids[0].group(2)) > max(same):
            f.add("f9:qid_above_all")
        if same and int(qids[0].group(2)) < min(same):
            f.add("f9:qid_below_all")
        if firsts:
            if firsts[0] == qi: f.add("f9:qid_first_line")
            if firsts[-1] == qi: f.add("f9:qid_last_line")
    qt = {t for t in TOK.findall(v["q"].lower()) if len(t) >= 3 and qfreq.get(t, 0) < 0.3}
    sl = st.lower(); cnt = [len(re.findall(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", sl)) for t in qt]
    f.add(f"f9:q_overlap_n={min(sum(c > 0 for c in cnt), 6)}")
    f.add(f"f9:q_overlap_max={binlog(max(cnt) if cnt else 0)}")
    return f


def opt_kinds(r, s=None):
    opts = r["options"]; ls = [len(o) for o in opts]; st = r["state"]; out = []
    q = L.qtext(r, s).lower()
    nums = [L.as_num(o) for o in opts]; nv = [x for x in nums if x is not None]
    pos = [L.first_pos(st, o) for o in opts]; ok = sorted(p for p in pos if p >= 0)
    sets = [L.set_ids(o) for o in opts]
    if sum(x is not None for x in sets) >= 2:  # the "no record" option of a record-set pick is the empty set
        sets = [frozenset() if (x is None and L.abstain_kind(o) == "no_record") else x for x, o in zip(sets, opts)]
    sv = [x for x in sets if x is not None]
    cen = None
    if len(sv) >= 3:
        dist = [sum(len(a ^ b) for b in sv) if a is not None else None for a in sets]
        cen = min(d for d in dist if d is not None)
    for i, o in enumerate(opts):
        k = set()
        ak = L.abstain_kind(o)
        if ak:
            k.add("kind:abstain"); k.add("kind:abstain_" + ak)
        if ls[i] == max(ls): k.add("kind:longest")
        if ls[i] == min(ls): k.add("kind:shortest")
        if nums[i] is not None and len(nv) >= 2:
            if nums[i] == max(nv): k.add("kind:num_max")
            if nums[i] == min(nv): k.add("kind:num_min")
        if pos[i] >= 0:
            k.add("kind:in_text")
            if len(ok) >= 2:
                if pos[i] == ok[0]: k.add("kind:first_in_text")
                if pos[i] == ok[-1]: k.add("kind:last_in_text")
        if len(o) >= 3 and o.lower() in q: k.add("kind:in_question")
        if sets[i] is not None:
            k.add(f"kind:set_size={len(sets[i])}")
            if cen is not None and dist[i] == cen: k.add("kind:set_center")
        out.append(k)
    return out


def pb(x, ps):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, 1.0
    return float(norm.sf((x - 0.5 - mu) / math.sqrt(var))), float(norm.sf((mu - x - 0.5) / math.sqrt(var)))


def pb_exact(x, ps):
    """recheck2 (6 Oct): exact Poisson-binomial tails P(X >= x), P(X <= x) by DP (the spec G7 test is an exact one-sided
    binomial; the normal approximation is far too lenient in the 'under' direction when p0 = 1/k is small)."""
    import numpy as np
    pmf = np.zeros(len(ps) + 1); pmf[0] = 1.0
    for j, p in enumerate(ps, 1):
        pmf[1:j + 1] = pmf[1:j + 1] * (1 - p) + pmf[0:j] * p; pmf[0] *= (1 - p)
    return float(min(1.0, pmf[x:].sum())), float(min(1.0, pmf[:x + 1].sum()))


def qfreqs(rows, side):
    c = defaultdict(int)
    for r in rows:
        for t in set(TOK.findall(L.qtext(r, side.get(r["id"])).lower())):
            c[t] += 1
    return {t: n / max(1, len(rows)) for t, n in c.items()}


def main():
    rows, side = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    qf = qfreqs(yn, side)
    cy = defaultdict(lambda: [0, 0])
    for r in yn:
        c = cy[r["meta"]["card_id"]]; c[0] += 1; c[1] += int(r["gold"])
    F = defaultdict(lambda: [0, 0, set(), 0.0, 0.0])
    for r in yn:
        s = side.get(r["id"]); g = int(r["gold"]); cid = r["meta"]["card_id"]; n_c, y_c = cy[cid]
        pr = (y_c - g) / (n_c - 1) if n_c > 1 else 0.5
        txt = "\n\n".join([r.get("card") or "", r["instructions"], r["state"]])
        for f in ngrams(txt) | meta_set(r, s) | vis_feats(r, s, qf):
            e = F[f]; e[0] += 1; e[1] += g; e[2].add(cid); e[3] += pr; e[4] += pr * (1 - pr)
    C = defaultdict(lambda: [0, [], set()]); D = [0, 0.0, 0]
    for r in ch:
        s = side.get(r["id"]); k = len(r["options"]); kinds = opt_kinds(r, s); cid = r["meta"]["card_id"]; gi = L.gold_index(r)
        ms = {m for m in meta_set(r, s) if not m.startswith(("meta:format_style", "meta:domain_pack", "meta:wording_id"))}
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
            fails.append({"part": "yes_no", "feature": f, "n": n, "yes_rate": round(y / n, 4), "p": p, "n_cards": len(cards)})
        elif p < bar * 100:
            near += 1
        if var > 0:
            pa = float(min(norm.sf((y - 0.5 - mu) / math.sqrt(var)), norm.sf((mu - y - 0.5) / math.sqrt(var))))
            if pa < bar:
                adj.append({"feature": f, "n": n, "yes_rate": round(y / n, 4), "card_expected_rate": round(mu / n, 4), "p": pa,
                            "n_cards": len(cards)})
    n_exact = 0
    for f, (x, ps, cards) in tested_ch.items():
        ph, pl = pb(x, ps)
        if min(ph, pl) < 0.01:  # recheck2: gate on the exact tail too (fail if either the approximation or exact < bar)
            eh, el = pb_exact(x, ps); n_exact += 1
            ph, pl = min(ph, eh), min(pl, el)
        if min(ph, pl) < bar:
            fails.append({"part": "choice", "feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(sum(ps), 2),
                          "dir": "over" if ph < pl else "under", "p": min(ph, pl), "n_cards": len(cards)})
        elif min(ph, pl) < bar * 100:
            near += 1
    fails.sort(key=lambda d: d["p"]); adj.sort(key=lambda d: d["p"])
    ynr = [f for f in fails if f["part"] == "yes_no"]; chf = [f for f in fails if f["part"] == "choice"]
    ynm = [f for f in ynr if f["n_cards"] > 1]
    kinds = {f: {"n_rows": len(v[1]), "gold_hits": v[0], "expected": round(sum(v[1]), 2)} for f, v in sorted(tested_ch.items())
             if f.startswith("kind:")}
    f9y = {f: {"n": v[0], "yes_rate": round(v[1] / v[0], 4)} for f, v in sorted(tested_yn.items()) if f.startswith("f9:")}
    ok = not chf and not adj and not ynm
    out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "pool_sha256": L.sha(L.OUT / f"{NAME}.jsonl"), "alpha": ALPHA,
           "n_min": N_MIN, "n_tests": n_tests, "bonferroni_p": bar,
           "n_yes_no_rows": len(yn), "n_choice_rows": len(ch), "n_tested_yes_no": len(tested_yn), "n_tested_choice": len(tested_ch),
           "n_fail_choice": len(chf), "n_fail_yes_no_raw": len(ynr), "n_fail_yes_no_raw_multi_card": len(ynm),
           "n_fail_yes_no_card_adjusted": len(adj), "near_within_100x": near,
           "choice_exact_poisson_binomial_checked": n_exact,
           "diag_gold_stored_first": {"rows": D[2], "gold_first": D[0], "expected": round(D[1], 1),
                                      "note": "stored option order; the trainer re-shuffles; judged in G10"},
           "pass_rule": "no choice failure, no card-adjusted yes/no failure, no raw yes/no failure spanning > 1 card",
           "kind_features": kinds, "f9_yes_no_features": f9y,
           "fails_choice": chf[:60], "fails_yes_no_raw_multi_card": ynm[:60], "fails_yes_no_raw_single_card": len(ynr) - len(ynm),
           "card_adjusted_fails": adj[:60], "pass": ok}
    (L.QC / f"g7_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("n_tests", "n_fail_choice", "n_fail_yes_no_raw", "n_fail_yes_no_raw_multi_card",
                                          "n_fail_yes_no_card_adjusted", "near_within_100x", "pass")}))


if __name__ == "__main__":
    main()
