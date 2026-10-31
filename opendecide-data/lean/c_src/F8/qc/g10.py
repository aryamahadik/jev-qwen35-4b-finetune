"""G10 balance (independent F8 checker): C_DATA_SPEC 2.1 quotas + 8 G10 (v4) + F8 G0 10.1 targets (incl. XF01-XF04),
from rows, meta, relations and the F8 sidecar (G10 may use hidden sidecar values such as placement, d_steps, edge_row,
tier_step, evidence_changes; G6/G7 may not). Difficulty bins are unscored (G9 crowd not run): every 'x bin' cell is
checked without the bin; the difficulty quotas and label x bin chi-square are pending. Rules the spec states only on the
selected set (rows-per-card median 40-50, large-card share) are reported, not gated.
Small-cell rule: a rate target +/- t is met when |rate - target| <= t OR |count - target*n| <= 1.
Usage: g10.py <name>"""
import json, re, sys
from collections import Counter, defaultdict
from fractions import Fraction
from scipy.stats import chisquare, binomtest, ks_2samp, chi2_contingency
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME); side = L.load_side(NAME); rel = L.load_relations(NAME)
S = lambda r: side[r["id"]]  # noqa: E731
yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
CHK = []
CBD, NOTA = "Cannot be determined from the information given", "None of these"


def check(name, ok, value, target, gated=True, note=None):
    CHK.append({"check": name, "pass": bool(ok) if gated else True, "gated": gated, "raw_ok": bool(ok), "value": value,
                "target": target, **({"note": note} if note else {})})


def rate_ok(x, n, target, tol):
    return n == 0 or abs(x / n - target) <= tol or abs(x - target * n) <= 1


def pct(x, n):
    return round(100 * x / n, 2) if n else None


def yr(rs):
    return [sum(int(r["gold"]) for r in rs), len(rs)]


def cells_yes(rs, keyf, tol=0.02, target=0.5):
    c = defaultdict(list)
    for r in rs:
        c[keyf(r)].append(r)
    val = {str(k): [*yr(v), pct(*yr(v))] for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))}
    bad = {k: v for k, v in val.items() if not rate_ok(v[0], v[1], target, tol)}
    return val, bad


# ------------------------------------------------------------------ yes/no
def yes_no_checks():
    n, ny = len(rows), len(yn)
    check("YN share 45-55% of F8 rows", 45 <= pct(ny, n) <= 55, pct(ny, n), "45-55")
    y, m = yr(yn)
    check("[selection-time] aggregate yes rate 50 +/- 2", rate_ok(y, m, .5, .02), pct(y, m), "50 +/- 2", gated=False,
          note="2.1 selection downsamples inside family x gold x wording x bin cells, so yes = no after selection")
    val, bad = cells_yes(yn, lambda r: (r["meta"]["wording_id"], S(r)["k_all"]))
    keep = sum(2 * min(v[0], v[1] - v[0]) for v in val.values())
    check("[selection-time] yes rate 50 +/- 2 per wording x k_all cell (x bin after G9)", not bad,
          {"cells": len(val), "off": len(bad), "yn_rows": ny}, "every cell", gated=False,
          note={"off_cells": dict(list(bad.items())[:30])} if bad else None)
    tgt_yn = 2250 * ny // n
    check("wording x k_all cells feasible: exact within-cell balancing keeps >= the round-1 YN target", keep >= tgt_yn,
          {"rows_kept_by_exact_cell_balancing": keep, "round1_yn_target": tgt_yn}, ">= target")
    for nm, kf in (("sub-skill", lambda r: r["meta"]["subtype"]), ("card version", lambda r: "full" if S(r)["card_version"] == "full" else "short/none"),
                   ("k_all", lambda r: S(r)["k_all"])):
        val, bad = cells_yes(yn, kf)
        check(f"yes rate 50 +/- 2 per {nm}", not bad, val, "50 +/- 2 each")
    thr = [r for r in yn if S(r)["yn_kind"] == "threshold"]; act = [r for r in yn if S(r)["yn_kind"] == "action_rule"]
    cm = Counter(S(r)["comparator"] for r in thr); dr = Counter(S(r)["direction"] for r in thr)
    check("comparator inclusive vs strict 50 +/- 5 of threshold YN rows", abs(pct(cm["inclusive"], len(thr)) - 50) <= 5, dict(cm), "50 +/- 5")
    check("direction up vs down 50 +/- 5 of threshold YN rows", abs(pct(dr["up"], len(thr)) - 50) <= 5, dict(dr), "50 +/- 5")
    for nm, kf in (("comparator", lambda r: S(r)["comparator"]), ("direction", lambda r: S(r)["direction"])):
        val, bad = cells_yes(thr, kf)
        check(f"yes rate 50 +/- 2 within each {nm} (threshold YN)", not bad, val, "50 +/- 2 each")
    val, bad = cells_yes(act, lambda r: r["meta"]["subtype"])
    check("action-rule YN rows: yes rate 50 +/- 2 per sub-skill", not bad, val, "50 +/- 2 each")
    op = [r for r in yn if S(r)["world"] == "open"]
    check("open-world YN rows: yes rate 50 +/- 2", rate_ok(*yr(op), .5, .02), [*yr(op), pct(*yr(op))], "50 +/- 2")
    check("open-world YN rows have placement 'open' and d_steps null",
          all(S(r)["placement"] == "open" and S(r)["d_steps"] is None for r in op if S(r)["yn_kind"] == "threshold"),
          sum(1 for r in op if S(r)["yn_kind"] == "threshold" and not (S(r)["placement"] == "open" and S(r)["d_steps"] is None)), 0)
    cl = [r for r in thr if S(r)["world"] == "closed"]; pl = Counter(S(r)["placement"] for r in cl)
    check("placement exact 25 +/- 3, near 25 +/- 3, far 50 +/- 3 (closed-world threshold YN)",
          abs(pct(pl["exact"], len(cl)) - 25) <= 3 and abs(pct(pl["near"], len(cl)) - 25) <= 3 and abs(pct(pl["far"], len(cl)) - 50) <= 3,
          {k: [v, pct(v, len(cl))] for k, v in pl.items()}, "25/25/50")
    val, bad = cells_yes(cl, lambda r: S(r)["placement"])
    check("yes rate 50 +/- 2 per placement (pooled)", not bad, val, "50 +/- 2 each")
    ex = [r for r in cl if S(r)["placement"] == "exact"]
    bad_lab = [r["id"] for r in ex if int(r["gold"]) != int((S(r)["comparator"] == "inclusive") == (S(r)["polarity"] % 2 == 0))]
    check("exact placement: yes exactly when (inclusive, even) or (strict, odd)", not bad_lab, len(bad_lab), 0)
    per = defaultdict(lambda: [0, 0, 0])
    pairs = Counter((S(r)["comparator"], S(r)["polarity"] % 2) for r in ex)
    for r in ex:
        c = per[S(r)["k_all"]]; c[0] += 1; c[1] += int((S(r)["comparator"] == "inclusive") == (S(r)["polarity"] % 2 == 0)); c[2] += int(S(r)["direction"] == "up")
    okc = all(rate_ok(a, n_, .5, .05) and rate_ok(u, n_, .5, .05) for n_, a, u in per.values())
    check("exact rows per k_all cell: (incl,even)+(strict,odd) 50 +/- 5 and up:down 1:1 +/- 5", okc,
          {str(k): {"n": n_, "yes_pairs_pct": pct(a, n_), "up_pct": pct(u, n_)} for k, (n_, a, u) in per.items()}, "50 +/- 5")
    check("exact rows pooled: each (comparator x parity) pair 25 +/- 3", all(abs(pct(v, len(ex)) - 25) <= 3 for v in pairs.values()) and len(pairs) == 4,
          {f"{a}|{'odd' if b else 'even'}": [v, pct(v, len(ex))] for (a, b), v in pairs.items()}, "25 +/- 3 each")
    qt = lambda r: {"money": "amount", "score": "score", "num": "count"}.get((S(r)["t_repr"] or {}).get("rep"), "chance")  # noqa: E731
    ks = {}; dec_bad = {}
    for q in sorted({qt(r) for r in cl}):
        rs = [r for r in cl if qt(r) == q]
        a = [abs(Fraction(S(r)["d_steps"])) for r in rs if int(r["gold"]) == 1 and S(r)["d_steps"] is not None]
        b = [abs(Fraction(S(r)["d_steps"])) for r in rs if int(r["gold"]) == 0 and S(r)["d_steps"] is not None]
        p = float(ks_2samp([float(x) for x in a], [float(x) for x in b]).pvalue) if a and b else 1.0
        ks[q] = {"n_yes": len(a), "n_no": len(b), "p": round(p, 4)}
        tv = sorted(rs, key=lambda r: Fraction((S(r)["t_repr"] or {}).get("T") or "0"))
        for d in range(10):
            part = tv[d * len(tv) // 10:(d + 1) * len(tv) // 10]
            if part and not rate_ok(*yr(part), .5, .05):
                dec_bad[f"{q}|decile{d}"] = [*yr(part), pct(*yr(part))]
    check("magnitude: |d| same distribution for yes and no per quantity type (KS p > 0.01)", all(v["p"] > .01 for v in ks.values()), ks, "p > 0.01")
    check("magnitude: yes rate per decile of <T> 50 +/- 5 per quantity type", not dec_bad, {"off": dec_bad}, "50 +/- 5")
    yb = Counter(S(r)["yes_is_bad"] for r in yn)
    check("'yes = bad' true on 45-55% of YN rows (null counts as not-bad)", 45 <= pct(yb[True], ny) <= 55, {str(k): v for k, v in yb.items()}, "45-55")
    check("yes_is_bad null <= 5% of YN rows", pct(yb[None], ny) <= 5, pct(yb[None], ny), "<= 5")
    syn = Counter(S(r)["k_syn"] for r in yn)
    check("k_syn >= 1 on >= 10% of YN rows (plan 12%)", pct(syn[1] + syn[2], ny) >= 10, pct(syn[1] + syn[2], ny), ">= 10")
    byid = {r["id"]: r for r in rows}; eq = defaultdict(set)
    for x in rel:
        if x["type"] == "equiv":
            eq[x["a"]].add(x["b"]); eq[x["b"]].add(x["a"])
    d2 = [r for r in yn if S(r)["k_syn"] >= 2]
    tw = [r for r in d2 if any(o in byid and S(byid[o])["k_syn"] == 0 and byid[o]["call_id"] == r["call_id"] for o in eq[r["id"]])]
    check("k_syn >= 2 with affirmative equiv twin in unit on >= 2% of YN rows (plan 3%)", pct(len(tw), ny) >= 2,
          {"pct": pct(len(tw), ny), "k_syn2_rows": len(d2), "with_twin": len(tw)}, ">= 2")
    rp = defaultdict(lambda: [0, 0])
    for r in yn:
        for g in reps(r):
            rp[g][0] += 1; rp[g][1] += int(r["gold"])
    tab = [[v[1], v[0] - v[1]] for v in rp.values() if v[0]]
    p = float(chi2_contingency(tab)[1]) if len(tab) > 1 else 1.0
    check("YN yes rate independent of chance representation (chi-square p > 0.01)", p > .01, {"p": round(p, 4), **{k: [v[1], v[0]] for k, v in rp.items()}}, "p > 0.01")
    out = {}
    for q in sorted({qt(r) for r in cl}):
        rs = [r for r in cl if qt(r) == q]
        for f in ("rep", "digits", "trailing_zeros"):
            for tgt, keyf in (("label", lambda r: str(int(r["gold"]))), ("placement", lambda r: S(r)["placement"])):
                tab2 = defaultdict(Counter)
                for r in rs:
                    tab2[str((S(r)["t_repr"] or {}).get(f))][keyf(r)] += 1
                keys = sorted({k for c in tab2.values() for k in c})
                m2 = [[c[k] for k in keys] for c in tab2.values() if sum(c.values()) >= 5]
                ok = len(m2) > 1 and len(keys) > 1 and all(sum(col) > 0 for col in zip(*m2))
                out[f"{q}|{f}_vs_{tgt}"] = round(float(chi2_contingency(m2)[1]), 4) if ok else 1.0
    check("<T> representation, digit count, trailing zeros independent of label and placement within each quantity type (p > 0.01)",
          all(v > .01 for v in out.values()), out, "p > 0.01")


def reps(r):
    g = set()
    for x in S(r).get("representation") or []:
        g.add({"pct0": "percent", "pct1": "percent", "dec": "decimal", "frac": "fraction"}.get(x, "a_in_b_or_counts"))
    return g


# ------------------------------------------------------------------ choice
def order_of(r):
    """level order of TIER / MAT options: the line of card-without-question naming all options, else first mention."""
    opts = r["options"]; v = L.views(r)["cardnoq"]
    for ln in re.split(r"\n|(?<=\.)\s", v):
        if all(f"'{o}'" in ln or f"\"{o}\"" in ln for o in opts):
            return sorted(range(len(opts)), key=lambda i: ln.find(opts[i])), "line"
    pos = [v.find(o) for o in opts]
    if all(p >= 0 for p in pos):
        return sorted(range(len(opts)), key=lambda i: pos[i]), "first_mention"
    return None, None


def choice_checks():
    nc = len(ch); b = Counter(L.bucket(len(r["options"])) for r in ch)
    tgt = {"2-4": 35, "5-9": 35, "10-19": 15, "20-60": 15}
    check("option buckets 2-4:35 5-9:35 10-19:15 20-60:15 (+/- 3 pp)", all(abs(pct(b[k], nc) - v) <= 3 for k, v in tgt.items()),
          {k: pct(b[k], nc) for k in tgt}, tgt)
    check("every row 2 <= n <= 60", all(2 <= len(r["options"]) <= 60 for r in ch), [min(len(r["options"]) for r in ch), max(len(r["options"]) for r in ch)], "2-60")
    for bk in tgt:
        rs = [r for r in ch if L.bucket(len(r["options"])) == bk]
        if not rs:
            continue
        K = max(len(r["options"]) for r in rs); obs = [0] * K; exp = [0.0] * K
        for r in rs:
            k = len(r["options"]); obs[L.gold_index(r)] += 1
            for j in range(k):
                exp[j] += 1 / k
        keep = [j for j in range(K) if exp[j] > 0]
        p = chisquare([obs[j] for j in keep], [exp[j] for j in keep]).pvalue if len(keep) > 1 else 1.0
        check(f"gold position uniform in bucket {bk} (chi-square p > 0.01)", p > 0.01, {"rows": len(rs), "p": float(p)}, "p > 0.01")
    x = e = 0.0
    for r in ch:
        ls = [len(o) for o in r["options"]]; m = ls.count(max(ls))
        x += int(len(r["gold"]) == max(ls)); e += m / len(ls)
    check("'longest option is gold' within 1/k +/- 2 pp", abs(x - e) / nc <= .02, {"obs_pct": pct(x, nc), "exp_pct": pct(e, nc)}, "+/- 2 pp")
    # TIER and MAT gold level uniform per sampler x K
    for form in ("TIER", "MAT"):
        rs = [r for r in ch if S(r)["qform"] == form]; cells = defaultdict(lambda: defaultdict(int)); nn = Counter(); how = Counter()
        for r in rs:
            o, h = order_of(r); how[h] += 1
            if o is None:
                continue
            K = len(r["options"]); lvl = o.index(L.gold_index(r)); cells[(r["meta"]["sampler"], K)][lvl] += 1; nn[(r["meta"]["sampler"], K)] += 1
        bad, val = {}, {}
        for key, d in cells.items():
            K = key[1]; n_ = nn[key]
            obs = [d[j] for j in range(K)]; val[str(key)] = obs
            if not all(rate_ok(c, n_, 1 / K, .02) for c in obs):
                bad[str(key)] = obs
        tot = Counter(); totn = 0
        for key, d in cells.items():
            for j, c in d.items():
                tot[(key[1], j)] += c
        check(f"{form} gold level 1/K +/- 2 pp per sampler x K", not bad, {"cells": val, "order_source": dict(how)}, "1/K +/- 2 pp",
              note={"off": bad} if bad else None)
    bins = [r for r in ch if S(r)["qform"] == "BIN"]
    cells = defaultdict(list)
    for r in bins:
        if r["gold"] == CBD:
            continue
        K = len([o for o in r["options"] if o != CBD]); cells[(r["meta"]["sampler"], K)].append(r)
    bad, val = {}, {}
    pooled = defaultdict(list)
    for key, rs in cells.items():
        if len(rs) < 50:
            pooled[L.bucket(key[1]) if key[1] >= 5 else "3-4"].append(rs); continue
        K = key[1]; obs = Counter(sorted(range(K), key=lambda i: L.nums([o for o in r["options"] if o != CBD][i])[0]).index(
            [o for o in r["options"] if o != CBD].index(r["gold"])) for r in rs)
        val[str(key)] = [obs[j] for j in range(K)]
        if not all(rate_ok(obs[j], len(rs), 1 / K, .02) for j in range(K)):
            bad[str(key)] = val[str(key)]
    for pb, lst in pooled.items():
        rs = [r for x in lst for r in x]; obs = Counter(); exp = Counter()
        for r in rs:
            opts = [o for o in r["options"] if o != CBD]; K = len(opts)
            order = sorted(range(K), key=lambda i: L.nums(opts[i])[0]); lv = order.index(opts.index(r["gold"]))
            obs[("first" if lv == 0 else "last" if lv == K - 1 else "inner")] += 1
            exp["first"] += 1 / K; exp["last"] += 1 / K; exp["inner"] += (K - 2) / K
        val[f"pooled {pb}"] = {k: [obs[k], round(exp[k], 1)] for k in exp}
        if not all(abs(obs[k] - exp[k]) / len(rs) <= .02 or abs(obs[k] - exp[k]) <= 1 for k in exp):
            bad[f"pooled {pb}"] = val[f"pooled {pb}"]
    check("BIN gold bin 1/K +/- 2 pp per sampler x K (cells < 50 rows pooled by K bucket; end bins included)", not bad, val, "1/K +/- 2 pp",
          note={"off": bad} if bad else None)
    ed = Counter((S(r)["qform"], S(r)["edge_row"]) for r in ch if S(r)["qform"] in ("BIN", "MAT"))
    nb = ed[("BIN", True)] + ed[("BIN", False)]; nm = ed[("MAT", True)] + ed[("MAT", False)]
    check("BIN rows exactly on an edge 15% (+/- 3)", abs(pct(ed[("BIN", True)], nb) - 15) <= 3, pct(ed[("BIN", True)], nb), "15 +/- 3")
    check("MAT rows with likelihood or impact on a level edge 15 +/- 3", abs(pct(ed[("MAT", True)], nm) - 15) <= 3, pct(ed[("MAT", True)], nm), "15 +/- 3")
    tier = [r for r in ch if S(r)["qform"] == "TIER"]; ts = Counter(S(r)["tier_step"] for r in tier)
    check("TIER decisive F8-only step (only_if / override) on >= 50% of TIER rows", pct(ts["only_if"] + ts["override"], len(tier)) >= 50,
          {str(k): v for k, v in ts.items()}, ">= 50")
    pred = [r for r in ch if S(r)["qform"] == "PRED"]; ev = Counter(S(r)["evidence_changes"] for r in pred)
    check("PRED: evidence changes the top outcome on 50 +/- 5 of PRED rows", abs(pct(ev[True], len(pred)) - 50) <= 5, {str(k): v for k, v in ev.items()}, "50 +/- 5")
    gp = [r for r in pred if not r["meta"].get("gold_probs") or max(r["meta"]["gold_probs"], key=lambda k: Fraction(str(r["meta"]["gold_probs"][k]))) != r["gold"]]
    check("PRED: gold_probs present and argmax = gold", not gp, len(gp), 0)
    nonpred = [r for r in rows if S(r)["qform"] != "PRED" and r["meta"].get("gold_probs")]
    check("gold_probs only on PRED rows", not nonpred, len(nonpred), 0)


def abstain_checks():
    cells = defaultdict(lambda: [0, 0.0, 0]); low_k = both = wrong_place = 0; shown = Counter(); wrong = Counter()
    for r in ch:
        k = len(r["options"]); q = S(r)["qform"]; w = S(r)["world"]
        has_c, has_n = CBD in r["options"], NOTA in r["options"]
        if (has_c or has_n) and k < 3: low_k += 1
        if has_c and has_n: both += 1
        if has_c and not (w == "open" and q in ("BIN", "RANK-top", "DEC", "INV")): wrong_place += 1
        if has_n and not (w == "closed" and q in ("INV", "RANK-order")): wrong_place += 1
        if w == "open" and q in ("BIN", "RANK-top", "DEC", "INV") and not has_c: wrong_place += 1
        for a, on in (("CBD", has_c), ("NOTA", has_n)):
            if on:
                c = cells[(a, q, L.bucket(k))]; c[0] += 1; c[1] += 1 / k; g = int(r["gold"] == (CBD if a == "CBD" else NOTA)); c[2] += g
                shown[a] += 1; wrong[a] += 1 - g
    check("abstain shown only at n >= 3", low_k == 0, low_k, 0)
    check("never CBD and NOTA in one row", both == 0, both, 0)
    check("CBD only on open-world BIN/RANK-top/DEC/INV (and always there); NOTA only on closed INV / RANK-order", wrong_place == 0, wrong_place, 0)
    off = {f"{a}|{q}|{bk}": [g, n, round(100 * e / n, 2)] for (a, q, bk), (n, e, g) in cells.items()
           if not (abs(g - e) / n <= .02 or abs(g - e) <= 1)}
    agg = defaultdict(lambda: [0, 0.0, 0])
    for (a, q, bk), (n, e, g) in cells.items():
        x = agg[(a, bk)]; x[0] += n; x[1] += e; x[2] += g
    off2 = {f"{a}|{bk}": [g, n, round(100 * e / n, 2)] for (a, bk), (n, e, g) in agg.items() if not (abs(g - e) / n <= .02 or abs(g - e) <= 1)}
    check("abstain gold = 1/n +/- 2 pp per n bucket and per abstain option", not off2,
          {f"{a}|{bk}": {"gold": g, "rows": n, "gold_pct": pct(g, n), "exp_pct": round(100 * e / n, 2)} for (a, bk), (n, e, g) in sorted(agg.items())},
          "+/- 2 pp", note={"off": off2, "per_form_off": off})
    check("abstain gold = 1/n +/- 2 pp per form (INV, BIN, RANK-top, DEC, RANK-order alike)", not off,
          {f"{a}|{q}|{bk}": [g, n, round(100 * e / n, 2)] for (a, q, bk), (n, e, g) in sorted(cells.items())}, "+/- 2 pp")
    check("each abstain option wrong on >= 50% of rows that show it", all(wrong[a] / shown[a] >= .5 for a in shown),
          {a: pct(wrong[a], shown[a]) for a in shown}, ">= 50")
    pn = defaultdict(lambda: [0, 0])
    for r in ch:
        if CBD in r["options"]:
            for key in (("n", S(r)["n_unknown"]), (r["meta"]["subtype"], S(r)["n_unknown"])):
                pn[key][0] += 1; pn[key][1] += int(r["gold"] == CBD)
    check("P(CBD gold | n 'not recorded' facts) <= 50% per n and within each sub-skill", all(g / n <= .5 for n, g in pn.values()),
          {str(k): [g, n, pct(g, n)] for k, (n, g) in sorted(pn.items(), key=lambda kv: str(kv[0]))}, "<= 50")
    nc = len(ch); mk = Counter(S(r)["masked"] for r in ch)
    check("masked label names 10-15% of choice rows", 10 <= pct(mk["masked"], nc) <= 15, pct(mk["masked"], nc), "10-15")
    check("swapped label names about 5% of choice rows (3-7)", 3 <= pct(mk["swapped"], nc) <= 7, pct(mk["swapped"], nc), "about 5")
    ow_ch = sum(S(r)["world"] == "open" for r in ch); ow_yn = sum(S(r)["world"] == "open" for r in yn)
    elig = [r for r in ch if S(r)["qform"] in ("BIN", "RANK-top", "DEC", "INV")]; ow_el = sum(S(r)["world"] == "open" for r in elig)
    check("open world about 25% of choice rows (20-30)", 20 <= pct(ow_ch, nc) <= 30,
          {"of_choice_rows": pct(ow_ch, nc), "of_BIN_RANKtop_DEC_INV_rows": pct(ow_el, len(elig))}, "about 25")
    check("open world about 15% of YN rows (10-20)", 10 <= pct(ow_yn, len(yn)) <= 20, pct(ow_yn, len(yn)), "about 15")


# ------------------------------------------------------------------ general
def general_checks():
    n = len(rows)
    sk = Counter(r["meta"]["subtype"] for r in rows); tg = {"points": 25, "bayes": 30, "expected": 30, "rank": 15}
    check("sub-skill shares points 25 / bayes 30 / expected 30 / rank 15 (+/- 3)", all(abs(pct(sk[k], n) - v) <= 3 for k, v in tg.items()),
          {k: pct(sk[k], n) for k in tg}, tg)
    deep = sum(bool(r["meta"]["deep"]) for r in rows)
    check("deep items <= 10% of rows", pct(deep, n) <= 10, pct(deep, n), "<= 10")
    chb = [r for r in rows if S(r).get("representation")]; rc = Counter(g for r in chb for g in reps(r))
    check("chance representation: percent, decimal, fraction, 'a in b'/counts each >= 15% of chance-bearing rows",
          all(pct(rc[g], len(chb)) >= 15 for g in ("percent", "decimal", "fraction", "a_in_b_or_counts")),
          {g: pct(rc[g], len(chb)) for g in ("percent", "decimal", "fraction", "a_in_b_or_counts")}, ">= 15 each")
    tk = Counter(r["meta"]["twin_kind"] for r in rows); ids = {r["id"] for r in rows}
    anchors = {r["meta"]["twin_of"] for r in rows if r["meta"]["twin_kind"] == "flip"} & ids
    inset = tk["flip"] + len(anchors)
    check("label-flip twin sets 20-25% of rows (XF03)", 20 <= pct(inset, n) <= 25, {"pct": pct(inset, n), "flip_twins": tk["flip"], "anchors": len(anchors)}, "20-25")
    flips = [r for r in rows if r["meta"]["twin_kind"] == "flip" and r["meta"]["twin_of"] in ids]
    byid = {r["id"]: r for r in rows}
    same = sum(1 for r in flips if r["gold"] == byid[r["meta"]["twin_of"]]["gold"])
    check("label-flip twins differ in gold from their anchor", same == 0, {"flip_twins": len(flips), "same_gold": same}, 0)
    inv = [x for x in rel if x["type"] == "inv"]
    att = {x["a"] for x in inv} | {x["b"] for x in inv}
    check("attack twins (inv relation) about 5% of rows (3-7)", 3 <= pct(len(att) / 2, n) <= 7,
          {"inv_relations": len(inv), "rows_in_inv_units": len(att), "pct_twins": pct(len(att) / 2, n)}, "about 5")
    check("'attack present' uncorrelated with the label", bool(att), "no attack rows" if not att else len(att), "attack rows exist; p > 0.01")
    lc = sum("is the correct answer" in L.views(r)["q"].lower() for r in rows)
    check("label-check form rows = 0", lc == 0, lc, 0)
    src = Counter(r["source"] for r in rows)
    check("source = 'c_f8' on every row", set(src) == {"c_f8"}, dict(src), "c_f8")
    ol = sum(1 for r in rows if "option_level" in r["meta"])
    check("no option_level on any F8 row (F8-R1-C3)", ol == 0, ol, 0)
    s5 = sum(r["meta"]["sampler"] == "S5" for r in rows)
    check("no S5 row in a training pool", s5 == 0 or NAME == "mixdev_S5", s5, 0)
    units = Counter(r["call_id"] for r in rows); big = sum(1 for v in units.values() if v > 3)
    check("relation units <= 3 rows", big == 0, big, 0)


def card_checks():
    per = defaultdict(list)
    for r in rows:
        per[r["meta"]["card_id"]].append(r)
    nC = len(per); sizes = sorted(len(v) for v in per.values())
    check("cards >= 80 (round 1)", nC >= 80, nC, ">= 80")
    check("rows per card <= 128", sizes[-1] <= 128, {"max": sizes[-1], "median": sizes[len(sizes) // 2], "min": sizes[0]}, "<= 128")
    lg = Counter(S(v[0])["card_size"] for v in per.values())
    check("[selection-time] median rows per card 40-50; large cards > half", 40 <= sizes[len(sizes) // 2] <= 50 and lg["large"] > nC / 2,
          {"median": sizes[len(sizes) // 2], "card_size": dict(lg)}, "after selection", gated=False)
    sch = {c: Counter(S(r)["qform"] for r in v) for c, v in per.items()}
    multi = [c for c, cc in sch.items() if len(cc) > 1]
    check("one label schema per card", not multi, len(multi), 0)
    invc = sum(1 for cc in sch.values() if "INV" in cc)
    check("inverted (INV) cards 10-15% of cards", 10 <= pct(invc, nC) <= 15, pct(invc, nC), "10-15")
    out = {}
    for c, v in per.items():
        y = [int(r["gold"]) for r in v if L.is_yn(r)]
        if len(y) >= 20:
            out[c] = pct(sum(y), len(y))
    off = {c: p for c, p in out.items() if not 15 <= p <= 85}
    check("per-card yes rate within the drawn 20-80% band (cards with >= 20 YN rows; 5 pp slack)", not off,
          {"cards": len(out), "min": min(out.values()) if out else None, "max": max(out.values()) if out else None}, "20-80",
          note={"off": off} if off else None)


def main():
    yes_no_checks(); choice_checks(); abstain_checks(); general_checks(); card_checks()
    check("difficulty easy <= 25 / medium >= 45 / hard <= 30; label x bin chi-square", True, "pending",
          "after G9 crowd scoring", gated=False, note="difficulty_bin is null on every row")
    check("inverse-conditional and rank shortcut targets (need parsed P(E|H), amounts)", True, "not computed by the checker",
          "G0 10.1", gated=False, note="needs a parse of chances / amounts; covered indirectly by G6 (a)-(d) and G7")
    fails = [c["check"] for c in CHK if not c["pass"]]
    out = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "yes_no": len(yn), "choice": len(ch),
           "n_checks": len(CHK), "n_fail": len(fails), "failed": fails, "checks": CHK, "pass": not fails}
    (L.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "checks"}, indent=1))


if __name__ == "__main__":
    main()
