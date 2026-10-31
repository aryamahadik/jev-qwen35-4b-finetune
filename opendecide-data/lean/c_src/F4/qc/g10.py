"""G10 balance (independent F4 checker): C_DATA_SPEC 8 G10 + 2.1 quotas + F4 G0 section 8 targets (XF01, XF02),
computed from rows, `meta`, `edge`, the QC sidecar and the shared negcount (recomputed on the rendered question).
Two kinds of check (as F4 G0 8 says: "G10 is rechecked on rows after selection"; G9 bins do not exist yet, so every
'x bin' axis is pooled and the bin check is pending):
- POOL checks: properties of each row or its display that selection cannot fix (gold letter uniform per bucket,
  longest option, abstain/None display and gold rate, CH-3 OPEN share, attack vs label). They must pass on the pool.
- TARGETS: shares the stratified selection sets (yes rate per wording x negation cell, yes_bad, negation quotas, option
  buckets, sampler / card / style shares, twin shares, carriers, inert, negative claims, depth, decisive position,
  HANS overlap). Reported on the pool with a tolerance: a cell passes when it is inside the band, or when the band
  miss is consistent with sampling noise (two-sided binomial p > 0.01), or when a selection of the round-1 size can
  reach the band from the pool's rows (feasibility, stated per check). Usage: g10.py [candidates_r1]"""
import json, math, re, sys
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import chisquare, chi2_contingency, binomtest
import qc_lib as L
sys.path.insert(0, str(L.LEAN / "c_src/common"))
import negcount

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
N_SEL = 3600  # round-1 F4 kept rows (spec 2.2, F4 G0 0.1)
rows = L.load(NAME)
side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
rels = L.load_relations(NAME)
yn = [r for r in rows if r["qtype"] == "noul"]; ch = [r for r in rows if r["qtype"] != "noul"]
CHK = []


def add(name, ok, kind, **info):
    CHK.append({"check": name, "kind": kind, "pass": bool(ok), **info})


def tag(r, p, default=None):
    for e in r["meta"].get("edge", []):
        if e.split(":")[0] == p:
            return e.split(":", 1)[1] if ":" in e else p
    return default


def band_ok(x, n, lo, hi):
    """inside [lo, hi], or the miss is consistent with noise (binomial p > 0.01 against the nearest band edge)."""
    if n == 0:
        return True, None
    r = x / n
    if lo <= r <= hi:
        return True, 1.0
    t = lo if r < lo else hi
    p = binomtest(x, n, t).pvalue
    return p > 0.01, round(float(p), 4)


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def chi_p(table):
    t = np.array(table, dtype=float)
    t = t[t.sum(1) > 0][:, t.sum(0) > 0]
    if t.shape[0] < 2 or t.shape[1] < 2:
        return 1.0
    return float(chi2_contingency(t)[1])


def pool_checks():
    rng = np.random.default_rng(10)
    # P1 gold letter uniform per option bucket: u = (g + U) / k is uniform under H0; chi-square over 10 bins
    by_b = defaultdict(list)
    for r in ch:
        k = len(r["options"]); g = r["options"].index(r["gold"])
        by_b[bucket(k)].append((g + rng.random()) / k)
    for b, us in sorted(by_b.items()):
        h = np.histogram(us, bins=10, range=(0, 1))[0]
        p = float(chisquare(h).pvalue)
        add(f"gold_letter_uniform[{b}]", p > 0.01, "pool", n=len(us), chi2_p=round(p, 4))
    # exact per-k chi-square for the small fixed-k forms
    for k in (2, 3):
        gs = [r["options"].index(r["gold"]) for r in ch if len(r["options"]) == k]
        p = float(chisquare(np.bincount(gs, minlength=k)).pvalue)
        add(f"gold_letter_uniform[k={k}]", p > 0.01, "pool", n=len(gs), counts=np.bincount(gs, minlength=k).tolist(),
            chi2_p=round(p, 4))
    # P2 longest option is gold within +/- 2 pp of 1/k (expected with ties = mean(|longest| / k))
    for b in ("all", "2-4", "5-9", "10-19", "20-60"):
        sel = [r for r in ch if b == "all" or bucket(len(r["options"])) == b]
        hit = exp = 0.0
        for r in sel:
            lens = [len(o) for o in r["options"]]; mx = max(lens); lg = [i for i, x in enumerate(lens) if x == mx]
            hit += int(r["options"].index(r["gold"]) in lg); exp += len(lg) / len(lens)
        n = len(sel); d = (hit - exp) / n
        p = binomtest(int(hit), n, exp / n).pvalue if n else 1.0
        add(f"longest_option_gold[{b}]", abs(d) <= 0.02 or p > 0.01, "pool", n=n, observed=round(hit / n, 4),
            expected=round(exp / n, 4), diff_pp=round(100 * d, 2), binom_p=round(float(p), 4))
    # P3 'None of these follows' (CH-claim): gold 1/k +/- 2 pp per k bucket on rows that show it; wrong >= 50%
    none = [r for r in ch if any(L.is_abstain(o) for o in r["options"])]
    nb = defaultdict(lambda: [0, 0.0, 0])
    for r in none:
        k = len(r["options"]); b = bucket(k); s = nb[b]
        s[0] += int(L.is_abstain(r["gold"])); s[1] += 1 / k; s[2] += 1
    for b, (x, e, n) in sorted(nb.items()):
        p = binomtest(x, n, e / n).pvalue
        add(f"abstain_gold_1_over_k[{b}]", abs(x / n - e / n) <= 0.02 or p > 0.01, "pool", n=n,
            observed=round(x / n, 4), expected=round(e / n, 4), binom_p=round(float(p), 4))
    wrong = sum(1 for r in none if not L.is_abstain(r["gold"]))
    cd = [r for r in ch if side[r["id"]]["form"] == "CH-3"]
    add("abstain_wrong_ge_50pct", len(none) and wrong / len(none) >= 0.5, "pool", rows_showing=len(none),
        wrong_share=round(wrong / max(1, len(none)), 4))
    # CH-3 OPEN ('cannot be determined' / masked equivalent) gold share 1/3 +/- 2 pp (XF01): from the label of c
    lab = Counter(side[r["id"]]["label_c"] for r in cd)
    for l in ("F", "R", "O"):
        ok, p = band_ok(lab[l], len(cd), 1 / 3 - 0.02, 1 / 3 + 0.02)
        add(f"CH-3_gold_share[{l}]", ok, "pool", n=len(cd), share=round(lab[l] / max(1, len(cd)), 4), band_p=p)
    # P4 attack present uncorrelated with the label (yes/no gold; CH-3/CH-2 label; CH-claim claim vs None)
    def att(r):
        return int(r["role"] == "attacked")
    t = [[sum(1 for r in yn if att(r) == a and int(r["gold"]) == y) for y in (0, 1)] for a in (0, 1)]
    add("attack_vs_label[yes_no]", chi_p(t) > 0.01, "pool", table=t, chi2_p=round(chi_p(t), 4))
    for form in ("CH-3", "CH-2", "CH-claim"):
        rs = [r for r in ch if side[r["id"]]["form"] == form]
        labs = sorted({(side[r["id"]]["label_c"] if form != "CH-claim" else str(L.is_abstain(r["gold"]))) for r in rs})
        lf = lambda r: side[r["id"]]["label_c"] if form != "CH-claim" else str(L.is_abstain(r["gold"]))
        t = [[sum(1 for r in rs if att(r) == a and lf(r) == l) for l in labs] for a in (0, 1)]
        add(f"attack_vs_label[{form}]", chi_p(t) > 0.01, "pool", table=t, labels=labs, chi2_p=round(chi_p(t), 4))
    add("label_check_form_rows_0", not any(re.search(r'correct answer "', r["instructions"]) for r in rows), "pool")


def yes_rate_cells():
    """yes rate 50 +/- 2 per wording x negation count (k_all on the question, recomputed) and within each world."""
    kall = {}
    for r in yn:
        kall[r["id"]] = negcount.count(r["instructions"]).k_all
    cells = defaultdict(lambda: [0, 0])
    for r in yn:
        for key in (f"w={r['meta']['wording_id']}|neg={min(3, kall[r['id']])}",
                    f"world={tag(r, 'world')}", "family"):
            c = cells[key]; c[0] += int(r["gold"]); c[1] += 1
    bad = []; n_cells = 0; n_in_band = 0
    for key, (x, n) in sorted(cells.items()):
        if key.startswith("w="):
            n_cells += 1
            n_in_band += int(abs(x / n - 0.5) <= 0.02)
            p = binomtest(x, n, 0.5).pvalue
            if p <= 0.01 / max(1, sum(1 for k in cells if k.startswith("w="))):
                bad.append({"cell": key, "n": n, "yes": x, "p": round(float(p), 5)})
    fam = cells["family"]
    add("yes_rate_family", abs(fam[0] / fam[1] - 0.5) <= 0.02, "target", n=fam[1], yes_rate=round(fam[0] / fam[1], 4))
    for w in ("ow", "cw", "any"):
        x, n = cells[f"world={w}"]
        ok, p = band_ok(x, n, 0.48, 0.52)
        add(f"yes_rate_world[{w}]", ok, "target", n=n, yes_rate=round(x / max(1, n), 4), band_p=p)
    add("yes_rate_wording_x_neg_cells", not bad, "target", n_cells=n_cells, cells_inside_2pp=n_in_band,
        cells_rejecting_50pct_at_p01=bad, note="bin axis pooled (G9 pending); small cells judged by binomial p > 0.01 / n_cells (Bonferroni)")
    return kall


def target_checks(kall):
    n = len(rows); S = lambda r: side[r["id"]]
    ok, p = band_ok(len(yn), n, 0.45, 0.55)
    add("yes_no_share_45_55", ok, "target", share=round(len(yn) / n, 4), band_p=p)
    # negation quotas (negcount recomputed on the rendered question: yes/no `instructions` = wording + question)
    ks = {r["id"]: negcount.count(r["instructions"]).k_syn for r in yn}
    s1 = sum(1 for r in yn if ks[r["id"]] >= 1) / len(yn)
    add("k_syn_ge1_ge10pct_yes_no", s1 >= 0.10, "target", share=round(s1, 4))
    eqv = defaultdict(set)
    for rel in rels:
        if rel["type"] == "equiv":
            eqv[rel["a"]].add(rel["b"]); eqv[rel["b"]].add(rel["a"])
    form = {r["id"]: S(r)["form"] for r in rows}
    dn = [r for r in yn if ks[r["id"]] >= 2 and any(form.get(o) == "YN-F" for o in eqv[r["id"]])]
    add("double_negation_with_affirmative_twin_ge2pct", len(dn) / len(yn) >= 0.02, "target",
        share=round(len(dn) / len(yn), 4), rows=len(dn))
    mism = sum(1 for r in yn if ks[r["id"]] != S(r)["k_syn"] or kall[r["id"]] != S(r)["k_all"])
    add("negcount_matches_builder_sidecar", mism == 0, "info", mismatches=mism)
    yb = [S(r)["yes_bad"] for r in yn]
    x = sum(1 for v in yb if v is True)
    ok, p = band_ok(x, len(yb), 0.45, 0.55)
    add("yes_bad_50pm5", ok and all(v is not None for v in yb), "target", share=round(x / len(yb), 4), band_p=p,
        na=sum(1 for v in yb if v is None))
    # option buckets
    bc = Counter(bucket(len(r["options"])) for r in ch)
    for b, t in (("2-4", .35), ("5-9", .35), ("10-19", .15), ("20-60", .15)):
        ok, p = band_ok(bc[b], len(ch), t - 0.05, t + 0.05)
        add(f"option_bucket[{b}]", ok, "target", share=round(bc[b] / len(ch), 4), target=t, band_p=p)
    # samplers
    sc = Counter(r["meta"]["sampler"] for r in rows)
    add("sampler_shares_20_30", all(0.20 <= v / n <= 0.30 for v in sc.values()) and set(sc) <= {"S1", "S2", "S3", "S4"},
        "target", shares={k: round(v / n, 4) for k, v in sorted(sc.items())})
    add("no_S5_or_heldout_sampler_rows", "S5" not in sc, "pool")
    # label forms (choice rows)
    lf = Counter(S(r)["label_form"] for r in ch)
    ok1, p1 = band_ok(lf["masked"], len(ch), 0.10, 0.15); ok2, p2 = band_ok(lf["swapped"], len(ch), 0.03, 0.07)
    add("masked_10_15pct_choice", ok1, "target", share=round(lf["masked"] / len(ch), 4), band_p=p1)
    add("swapped_about_5pct_choice", ok2, "target", share=round(lf["swapped"] / len(ch), 4), band_p=p2)
    add("label_forms_only_on_CH3_CH2", all(S(r)["form"] in ("CH-3", "CH-2") for r in ch
                                            if S(r)["label_form"] != "plain"), "pool")
    # cards: count, inverted (CH-entity only) cards, few-shot cards, definition styles, short-card rows, world / unless
    cards = defaultdict(list)
    for r in rows:
        cards[r["meta"]["card_id"]].append(r)
    N = len(cards)
    inv = [c for c, rs in cards.items() if all(S(r)["form"] == "CH-entity" for r in rs)]
    add("inverted_cards_10_15pct", math.ceil(0.10 * N) <= len(inv) <= math.floor(0.15 * N), "target", cards=N,
        inverted=len(inv), band=[math.ceil(0.10 * N), math.floor(0.15 * N)])
    fs_rx = re.compile(r"^(Worked examples|Solved cases|Examples|Sample input and output)\b|^\|\s*Case\s*\|\s*Answer\s*\||"
                       r"^(Answer|Correct choice|Output|A): (Yes|No)\b", re.M)
    # repair r1: the original regex covered 4 of the 18 formats-1 few-shot headers and 4 answer-line forms; a worked
    # example's case is "Record: ... Question: ...?" (F4 G0 7.5 / parser section 4), so that shape is also detected
    fs_case = re.compile(r"Record: [^\n]*? Question: [^\n]*?\?")
    fs = [c for c, rs in cards.items() if any(fs_rx.search((r.get("card") or "") + "\n" + r["instructions"]) or
                                               fs_case.search((r.get("card") or "") + "\n" + r["instructions"])
                                               for r in rs)]
    add("few_shot_cards_5_10pct", 0.05 <= len(fs) / N <= 0.10, "target", few_shot_cards=len(fs), share=round(len(fs) / N, 4),
        note="detected by the formats-1 few-shot template headers / answer lines")
    ds = Counter(rs[0]["meta"]["defs_style"] for rs in cards.values())
    add("definition_styles_ge3", len([k for k in ds if k != "short"]) >= 3, "target",
        card_shares={k: round(v / N, 3) for k, v in ds.items()})
    ex = ds.get("one_line_examples", 0) / N
    add("examples_style_about_50pct_cards", 0.40 <= ex <= 0.60, "target", share=round(ex, 3))
    short = sum(1 for r in rows if S(r)["short"]) / n
    add("short_card_rows_about_15pct", 0.12 <= short <= 0.18, "target", share=round(short, 4))
    ns = [rs for rs in cards.values() if not S(rs[0])["short"]]
    ow = sum(1 for rs in ns if tag(rs[0], "world") == "ow") / max(1, len(ns))
    add("world_mode_OW65_CW35_nonshort_cards", 0.58 <= ow <= 0.72, "target", ow_share=round(ow, 3), cards=len(ns))
    um = Counter(tag(rs[0], "unless") for rs in ns if tag(rs[0], "world") == "ow" and tag(rs[0], "unless") in ("strict", "listc"))
    tot = um["strict"] + um["listc"]
    add("unless_mode_strict_listc_50_50", tot == 0 or 0.35 <= um["strict"] / tot <= 0.65, "target", counts=dict(um))
    rpc = sorted(len(v) for v in cards.values())
    add("rows_per_card_max_128", rpc[-1] <= 128, "pool", max=rpc[-1], median=rpc[len(rpc) // 2], min=rpc[0])
    add("cards_ge_80_one_pack_each", N >= 80 and len({rs[0]["meta"]["domain_pack"] for rs in cards.values()}) == N, "target",
        cards=N)
    # twins, attacks, inert pairs, deep
    unit = Counter(S(r)["unit"] for r in rows)
    tw = unit["contrast"] / n
    add("contrast_twin_rows_20_25pct", 0.20 <= tw <= 0.25, "target", share=round(tw, 4))
    at = sum(1 for r in rows if r["role"] == "attacked") / n
    add("attack_rows_about_5pct", 0.04 <= at <= 0.06, "target", share=round(at, 4))
    add("deep_rows_le_10pct", sum(1 for r in rows if r["meta"]["deep"]) / n <= 0.10, "target",
        deep=sum(1 for r in rows if r["meta"]["deep"]))
    dp = Counter(r["meta"]["depth"] for r in rows)
    add("depth_mix_45_35_20", all(abs(dp[d] / n - t) <= 0.07 for d, t in ((2, .45), (3, .35), (4, .20))), "target",
        shares={d: round(v / n, 3) for d, v in sorted(dp.items())})
    labs = sorted({tag(r, "L") for r in rows})
    t = [[sum(1 for r in rows if r["meta"]["depth"] == d and tag(r, "L") == l) for l in labs] for d in sorted(dp)]
    add("label_mix_equal_across_depths", chi_p(t) > 0.01, "target", chi2_p=round(chi_p(t), 5), labels=labs)
    # carriers 25 +/- 3 and inert 30 +/- 2 of rows of every label (carriers within positive / negative claim rows)
    for pol in (False, True):
        for l in labs:
            rs = [r for r in rows if tag(r, "L") == l and bool(S(r)["claim_neg"]) == pol]
            if len(rs) < 30:
                continue
            x = sum(1 for r in rs if S(r)["carrier"]); ok, p = band_ok(x, len(rs), 0.22, 0.28)
            add(f"carrier_rate[L={l}|neg={pol}]", ok, "target", n=len(rs), share=round(x / len(rs), 4), band_p=p)
    for l in labs:
        rs = [r for r in rows if tag(r, "L") == l]
        x = sum(1 for r in rs if S(r)["inert"]); ok, p = band_ok(x, len(rs), 0.28, 0.32)
        add(f"inert_rate[L={l}]", ok, "target", n=len(rs), share=round(x / len(rs), 4), band_p=p)
    # negative claims 30-40% in each world; label mix independent of claim polarity
    for w in ("ow", "cw", "any"):
        rs = [r for r in rows if tag(r, "world") == w]
        x = sum(1 for r in rs if S(r)["claim_neg"]); ok, p = band_ok(x, len(rs), 0.30, 0.40)
        add(f"negative_claim_share[{w}]", ok, "target", n=len(rs), share=round(x / max(1, len(rs)), 4), band_p=p)
        if w in ("ow", "cw"):
            from scipy.stats import chi2 as _chi2
            ll = sorted({tag(r, "L") for r in rs}); stat = df = 0; per = {}
            for fm in sorted({S(r)["form"] for r in rs} - {"CH-entity"}):
                t = [[sum(1 for r in rs if S(r)["form"] == fm and bool(S(r)["claim_neg"]) == pol and tag(r, "L") == l)
                      for l in ll] for pol in (False, True)]
                tt = np.array(t, dtype=float); tt = tt[tt.sum(1) > 0][:, tt.sum(0) > 0]
                if tt.shape[0] == 2 and tt.shape[1] >= 2:
                    c2, pp, d_, _ = chi2_contingency(tt); stat += c2; df += d_; per[fm] = round(float(pp), 4)
            pc = float(_chi2.sf(stat, df)) if df else 1.0
            raw = [[sum(1 for r in rs if bool(S(r)["claim_neg"]) == pol and tag(r, "L") == l) for l in ll] for pol in (False, True)]
            add(f"label_mix_vs_claim_polarity[{w}]", pc > 0.01, "target", chi2_p_stratified_by_form=round(pc, 5),
                per_form_p=per, pooled_chi2_p_info=round(chi_p(raw), 5),
                note="stratified by answer form; CH-entity excluded (its claim is positive by spec, F4 G0 1)")
        else:
            t = [[sum(1 for r in rs if r["qtype"] == "noul" and bool(S(r)["claim_neg"]) == pol and int(r["gold"]) == y)
                  for y in (0, 1)] for pol in (False, True)]
            add("yes_rate_vs_claim_polarity[any]", chi_p(t) > 0.01, "target", chi2_p=round(chi_p(t), 5), table=t)
    # decisive statement position decile: uniform per sampler and per label
    def _blk(r):
        # repair r2: the measured block is written by the builder (decisive_block; "mixed" = the S1 interleaved
        # section, G0 8 "per sampler x layout"); older sidecars fall back to the most-decisive block
        if S(r).get("decisive_block"):
            return S(r)["decisive_block"]
        dp = S(r).get("decisive_pos") or {}
        return max(dp, key=lambda k: (dp[k][2], -("table", "facts", "attrib", "mixed", "rules").index(k))) if dp else None
    for key, f in (("sampler", lambda r: r["meta"]["sampler"]), ("label", lambda r: tag(r, "L")),
                   ("sampler_x_block", lambda r: f"{r['meta']['sampler']}|{_blk(r)}")):
        grp = defaultdict(list)
        for r in rows:
            d = S(r)["decisive_decile"]
            if d is not None:
                grp[f(r)].append(int(d))
        for g, ds_ in sorted(grp.items()):
            h = np.bincount(np.clip(ds_, 0, 9), minlength=10); p = float(chisquare(h).pvalue)
            add(f"decisive_decile_uniform[{key}={g}]", p > 0.01, "target", n=len(ds_), chi2_p=round(p, 5))
    # HANS: label mix equal across quartiles of claim-to-record word overlap, computed inside each answer-form group
    W = re.compile(r"[a-z0-9]+(?:[-/][a-z0-9]+)*")
    def ovl(r):
        q = set(W.findall(L.views(r)["q"].lower())); stt = set(W.findall(r["state"].lower()))
        return len(q & stt) / max(1, len(q))
    for grp, sel in (("yes_no", yn), ("CH-3/CH-2", [r for r in ch if S(r)["form"] in ("CH-3", "CH-2")])):
        ov = [ovl(r) for r in sel]
        qs = np.quantile(ov, [0.25, 0.5, 0.75]); qi = [int(np.searchsorted(qs, v, side="right")) for v in ov]
        ll = sorted({tag(r, "L") for r in sel})
        t = [[sum(1 for r, b in zip(sel, qi) if b == j and tag(r, "L") == l) for l in ll] for j in range(4)]
        from scipy.stats import chi2 as _chi2
        stat = df = 0
        for fm in sorted({(S(r)["form"], tag(r, "world")) for r in sel}):
            tt = np.array([[sum(1 for r, b in zip(sel, qi) if b == j and (S(r)["form"], tag(r, "world")) == fm and tag(r, "L") == l)
                            for l in ll] for j in range(4)], dtype=float)
            tt = tt[tt.sum(1) > 0][:, tt.sum(0) > 0]
            if tt.shape[0] >= 2 and tt.shape[1] >= 2:
                c2, _, d_, _ = chi2_contingency(tt); stat += c2; df += d_
        ps = float(_chi2.sf(stat, df)) if df else 1.0
        add(f"HANS_label_mix_vs_overlap_quartile[{grp}]", ps > 0.01, "target", chi2_p_stratified_by_form_x_world=round(ps, 5),
            pooled_chi2_p_info=round(chi_p(t), 5), n=len(sel),
            note="overlap = question words found in the record; stratified by answer form x world (the L(c) mix differs by form and world by design)")
        if grp == "yes_no":
            tyn = [[sum(1 for r, b in zip(sel, qi) if b == j and int(r["gold"]) == y) for y in (0, 1)] for j in range(4)]
            add("HANS_yes_rate_vs_overlap_quartile[yes_no]", chi_p(tyn) > 0.01, "target", chi2_p=round(chi_p(tyn), 5))
    # HANS on CH-claim: an option whose sentence appears verbatim in the record is gold at its 1/k share
    hit = exp = n_ = 0
    for r in ch:
        if S(r)["form"] != "CH-claim":
            continue
        vo = [i for i, o in enumerate(r["options"]) if len(o) > 12 and o.lower() in r["state"].lower()]
        if vo and len(vo) < len(r["options"]):
            n_ += 1; hit += int(r["options"].index(r["gold"]) in vo); exp += len(vo) / len(r["options"])
    p = binomtest(hit, n_, exp / n_).pvalue if n_ else 1.0
    add("HANS_CH-claim_verbatim_option_is_gold_at_chance", p > 0.01, "target", rows=n_, gold_hits=hit,
        expected=round(exp, 1), binom_p=float(p), note="V2 topic line 'whether <c>' names the row's c = the gold claim")

def main():
    pool_checks(); kall = yes_rate_cells(); target_checks(kall)
    pool_fail = [c["check"] for c in CHK if c["kind"] == "pool" and not c["pass"]]
    tgt_fail = [c["check"] for c in CHK if c["kind"] == "target" and not c["pass"]]
    res = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "yes_no": len(yn), "choice": len(ch),
           "bin_axis": "pending (G9 crowd scoring not run); every 'x bin' cell pooled", "checks": CHK,
           "pool_fails": pool_fail, "target_fails": tgt_fail,
           "pass": not pool_fail and not tgt_fail}
    json.dump(res, open(L.QC / f"g10_{NAME}.json", "w"), indent=1)
    print(json.dumps({"pass": res["pass"], "pool_fails": pool_fail, "target_fails": tgt_fail}, indent=0))


if __name__ == "__main__":
    main()
