"""G10 balance (independent F7 checker): C_DATA_SPEC 8 G10 (v4) rules that apply to F7, plus the F7 G0 section 6 and
7 balance targets that are computable from rows. Gated items have an explicit bound in the spec (a range, +/-, a cap,
>=, or a p-value); "about" targets are reported with a +/- 5 pp soft check (soft = report only).
A (data spec G10 v4): 0 yes/no rows (yes-rate rules n/a); gold letter uniform per K under a random permutation
  (chi-square p > 0.01; seed 10010); "longest option is gold" within +/- 2 pp of 1/K (option label; served option with
  its definition line); abstain options wrong on >= 50% of rows that show them (F7 shows none); "attack present"
  uncorrelated with the label (chi-square stratified by K, p > 0.01); ordinal: each level 1/K +/- 2 pp per sampler x K.
B (G0 6.1): per card n >= 2K and every level holds floor(n/K) or ceil(n/K) rows; mode x K x level 1/K +/- 2 pp on cells
  >= 50 rows (smaller cells pooled by mode: chi-square p > 0.01).
C (G0 6.2): boundary placement shares S2 and S6 (at >= 30%, below >= 20%, above >= 20%); S2 inclusive vs exclusive
  50 +/- 5 among boundary rows; S6 continuous side (spec S6: about 70 / 30, soft); >= 30% of rows carry a conv element;
  two-way conv direction 50 +/- 5 per convention x sampler (>= 100 elements; else pooled over samplers; C8+C9 pooled).
D (G0 6.3): absence words in `state` (checker regex) and negcount k_all over `state` vs level: chi-square summed over K
  strata, p > 0.01 per sampler.
E (G0 6.4, 7, 2.1 quotas): fact_flip pair rows 20-25%; inv twins about 5% overall and per sampler (soft); equiv twins
  about 10% (soft); masked names 10-15% of rows; swapped about 5% (soft); few-shot cards 5-10% of cards; one-line +
  examples about 50% of cards (soft); short-card rows 15 +/- 2 pp; deep rows <= 10%; reversed numbering cards <= 10%;
  scale meaning severity vs better 50 +/- 5 of cards; unmentioned rows 20-30% of S1, S2, S4 and decisive (C1 conv)
  40-60% of those; inert about 30% of S1, S3, S4 (soft); distractor about 20% of S4 (soft).
Usage: g10.py <name>"""
import json, random, re, sys
import numpy as np
from collections import Counter, defaultdict
from scipy.stats import chisquare, chi2, chi2_contingency
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
sys.path.insert(0, str(L.LEAN / "c_src/common"))
import negcount  # noqa: E402
ONE_WAY = {"C4", "C5", "C7"}


def within(v, lo, hi):
    return bool(lo - 1e-9 <= v <= hi + 1e-9)


def strat_chi2(tab_by_k):
    """sum of per-stratum chi-square statistics (rows = feature bucket, cols = level); -> (stat, dof, p)."""
    st, dof = 0.0, 0
    for tab in tab_by_k:
        t = np.array(tab, float)
        t = t[t.sum(1) > 0][:, t.sum(0) > 0]
        if t.shape[0] < 2 or t.shape[1] < 2:
            continue
        s, _, d, _ = chi2_contingency(t, correction=False); st += s; dof += d
    return round(st, 2), dof, (round(float(chi2.sf(st, dof)), 5) if dof else 1.0)


def bucket_table(rows, val, maxb=6):
    by_k = defaultdict(lambda: defaultdict(Counter))
    for r in rows:
        by_k[L.K(r)][min(val(r), maxb)][L.level(r)] += 1
    tabs = []
    for k, d in by_k.items():  # merge adjacent buckets until every bucket row has >= 5 x K rows (expected >= 5 per cell)
        rowsb, cur = [], [0] * k
        for b in sorted(d):
            cur = [x + d[b][j] for j, x in enumerate(cur)]
            if sum(cur) >= 5 * k:
                rowsb.append(cur); cur = [0] * k
        if sum(cur):
            if rowsb:
                rowsb[-1] = [x + y for x, y in zip(rowsb[-1], cur)]
            else:
                rowsb.append(cur)
        tabs.append(rowsb)
    return tabs


def main():
    rows = L.load(NAME); n = len(rows); res = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": n}
    fails, soft = [], []
    # ---------------- A
    A = {"yes_no_rows": sum(r["qtype"] != "choice" for r in rows)}
    if A["yes_no_rows"]:
        fails.append("A.yes_no_rows")
    rng = random.Random(10010); let = defaultdict(Counter)
    for r in rows:
        k = L.K(r); perm = list(range(k)); rng.shuffle(perm)
        let[k][perm.index(r["options"].index(r["gold"]))] += 1
    A["gold_letter_chi2_p_by_K"] = {str(k): round(float(chisquare([c[j] for j in range(k)]).pvalue), 4) for k, c in sorted(let.items())}
    if min(A["gold_letter_chi2_p_by_K"].values()) <= 0.01:
        fails.append("A.gold_letter")
    for nm, ln in (("label", lambda r, o: len(o)),
                   ("served", lambda r, o: len(o + (": " + L.card_defs(r.get("card"))[o] if o in L.card_defs(r.get("card")) else "")))):
        hit, exp, m = 0, 0.0, 0
        for r in rows:
            ls = [ln(r, o) for o in r["options"]]; mx = max(ls)
            if ls.count(mx) != 1:
                continue
            m += 1; hit += int(r["options"][ls.index(mx)] == r["gold"]); exp += 1 / L.K(r)
        d = round(100 * (hit - exp) / max(1, m), 2)
        A[f"longest_option_is_gold_{nm}"] = {"rows_unique_longest": m, "gold_longest": hit, "expected": round(exp, 1), "diff_pp": d}
        if abs(d) > 2:
            fails.append(f"A.longest_{nm}")
    ab = re.compile(r"not enough|none of|cannot be determined|insufficient|unknown", re.I)
    A["abstain_option_rows"] = sum(any(ab.search(o) for o in r["options"]) for r in rows)
    att = lambda r: int(bool((r["meta"].get("case_features") or {}).get("injected")) or r["meta"].get("twin_kind") == "inv")
    A["attack_rows"] = sum(att(r) for r in rows)
    A["attack_vs_level_chi2"] = strat_chi2(bucket_table(rows, att, 1))
    if A["attack_vs_level_chi2"][2] <= 0.01:
        fails.append("A.attack")
    sk = defaultdict(Counter)
    for r in rows:
        sk[(r["meta"]["sampler"], L.K(r))][L.level(r)] += 1
    lv = {}
    for (s, k), c in sorted(sk.items()):
        tot = sum(c.values()); dev = max(abs(c[j] / tot - 1 / k) for j in range(k)) * 100
        lv[f"{s}|K{k}"] = {"n": tot, "max_dev_pp": round(dev, 2)}
        if dev > 2:
            fails.append(f"A.level_share_{s}_K{k}")
    A["level_share_by_sampler_K"] = lv
    res["A_data_spec_G10"] = A
    # ---------------- B
    B = {}; byc = defaultdict(Counter); ck = {}
    for r in rows:
        byc[r["meta"]["card_id"]][L.level(r)] += 1; ck[r["meta"]["card_id"]] = L.K(r)
    bad = []
    for c, cnt in byc.items():
        k = ck[c]; nn = sum(cnt.values()); lo, hi = nn // k, -(-nn // k)
        if nn < 2 * k or any(not (lo <= cnt[j] <= hi) for j in range(k)):
            bad.append(c)
    B["cards"] = len(byc); B["cards_failing_per_card_quota"] = len(bad); B["examples"] = bad[:5]
    if bad:
        fails.append("B.per_card_quota")
    mk = defaultdict(Counter)
    for r in rows:
        mk[(r["meta"]["mode"], L.K(r))][L.level(r)] += 1
    mres, pooled = {}, defaultdict(list)
    for (m, k), c in sorted(mk.items()):
        tot = sum(c.values())
        if tot >= 50:
            dev = max(abs(c[j] / tot - 1 / k) for j in range(k)) * 100
            mres[f"{m}|K{k}"] = {"n": tot, "max_dev_pp": round(dev, 2)}
            if dev > 2:
                fails.append(f"B.mode_level_{m}_K{k}")
        else:
            pooled[m].append([c[j] for j in range(k)])
    for m, tabs in pooled.items():
        obs = [x for t in tabs for x in t]; exp = [sum(t) / len(t) for t in tabs for _ in t]
        p = float(chisquare(obs, exp).pvalue) if len(obs) > 1 else 1.0
        mres[f"{m}|pooled_small_cells"] = {"n": sum(obs), "chi2_p": round(p, 4)}
        if p <= 0.01:
            fails.append(f"B.mode_level_pooled_{m}")
    B["mode_K_level"] = mres
    res["B_G0_6_1"] = B
    # ---------------- C
    C = {}; bnd = defaultdict(Counter); cmpc = defaultdict(Counter)
    for r in rows:
        for e in r["meta"].get("edge") or []:
            if e["kind"] == "boundary":
                bnd[r["meta"]["sampler"]][e["placement"]] += 1; cmpc[r["meta"]["sampler"]][e.get("cmp")] += 1
    C["boundary_placement"] = {s: dict(c) for s, c in sorted(bnd.items())}
    C["boundary_cmp"] = {s: dict(c) for s, c in sorted(cmpc.items())}
    for s in ("S2", "S6"):
        c = bnd.get(s, Counter()); tot = sum(c.values()) or 1
        sh = {p: round(c[p] / tot, 4) for p in ("at", "below", "above", "interior")}
        C[f"{s}_placement_shares"] = sh
        if sh["at"] < 0.30 or sh["below"] < 0.20 or sh["above"] < 0.20:
            fails.append(f"C.placement_{s}")
    c2 = cmpc.get("S2", Counter()); inc = c2["incl"] / max(1, c2["incl"] + c2["excl"])
    C["S2_inclusive_share"] = round(inc, 4)
    if not within(inc, 0.45, 0.55):
        fails.append("C.S2_inclusive_vs_exclusive")
    c6 = cmpc.get("S6", Counter()); hi6 = c6["side_high"] / max(1, c6["side_high"] + c6["side_low"])
    C["S6_side_high_share_rows"] = round(hi6, 4)
    s6cards = defaultdict(set)
    for r in rows:
        if r["meta"]["sampler"] == "S6":
            for e in r["meta"].get("edge") or []:
                if e["kind"] == "boundary":
                    s6cards[e.get("cmp")].add(r["meta"]["card_id"])
    C["S6_cards_by_cmp"] = {k: len(v) for k, v in s6cards.items()}
    conv_rows = sum(any(e["kind"] == "conv" for e in r["meta"].get("edge") or []) for r in rows)
    C["conv_row_share"] = round(conv_rows / n, 4)
    if conv_rows / n < 0.30:
        fails.append("C.conv_share")
    dirs = defaultdict(Counter)
    for r in rows:
        g = L.level(r); m = r["meta"]["mode"]
        for e in r["meta"].get("edge") or []:
            if e["kind"] != "conv":
                continue
            cid = e["conv"]
            if cid in ONE_WAY or (cid == "C1" and m in ("ladder", "highest")):
                continue
            key = "C8+C9" if cid in ("C8", "C9") else cid
            dirs[(key, r["meta"]["sampler"])]["above" if e["alt_level"] > g else "below"] += 1
    dres, pool = {}, defaultdict(Counter)
    for (cid, s), c in sorted(dirs.items()):
        tot = c["above"] + c["below"]
        if tot >= 100:
            sh = c["above"] / tot; dres[f"{cid}|{s}"] = {"n": tot, "above_share": round(sh, 4)}
            if not within(sh, 0.45, 0.55):
                fails.append(f"C.direction_{cid}_{s}")
        else:
            pool[cid].update(c)
    for cid, c in sorted(pool.items()):
        tot = c["above"] + c["below"]; sh = c["above"] / tot
        rec = {"n": tot, "above_share": round(sh, 4)}
        if tot >= 100:
            rec["gated"] = True
            if not within(sh, 0.45, 0.55):
                fails.append(f"C.direction_{cid}_pooled")
        else:
            rec["gated"] = False
        dres[f"{cid}|pooled"] = rec
    C["conv_direction_two_way"] = dres
    res["C_G0_6_2"] = C
    # ---------------- D
    D = {}
    for s in sorted({r["meta"]["sampler"] for r in rows}):
        rs = [r for r in rows if r["meta"]["sampler"] == s]
        a = strat_chi2(bucket_table(rs, lambda r: len(L.NEG_RX.findall(r["state"])), 8))
        k = strat_chi2(bucket_table(rs, lambda r: negcount.k_all(r["state"]), 6))
        D[s] = {"absence_words_vs_level": a, "kall_state_vs_level": k}
        if a[2] <= 0.01:
            fails.append(f"D.absence_{s}")
        if k[2] <= 0.01:
            fails.append(f"D.kall_{s}")
    res["D_G0_6_3"] = D
    # ---------------- E
    E = {}; ids = {r["id"]: r for r in rows}
    ff = {r["id"] for r in rows if r["meta"].get("twin_kind") == "fact_flip"}
    ff |= {r["meta"]["twin_of"] for r in rows if r["meta"].get("twin_kind") == "fact_flip" and r["meta"].get("twin_of") in ids}
    E["fact_flip_pair_row_share"] = round(len(ff) / n, 4)
    if not within(len(ff) / n, 0.20, 0.25):
        fails.append("E.fact_flip_share")
    tk = Counter(r["meta"].get("twin_kind") for r in rows)
    E["equiv_twin_share"] = round(tk["equiv"] / n, 4); E["inv_twin_share"] = round(tk["inv"] / n, 4)
    E["inv_share_by_sampler"] = {s: round(sum(1 for r in rows if r["meta"]["sampler"] == s and r["meta"].get("twin_kind") == "inv")
                                          / sum(1 for r in rows if r["meta"]["sampler"] == s), 4)
                                 for s in sorted({r["meta"]["sampler"] for r in rows})}
    for nm, v, t in (("equiv", tk["equiv"] / n, 0.10), ("inv", tk["inv"] / n, 0.05)):
        if abs(v - t) > 0.05:
            soft.append(f"E.{nm}_share")
    lf = Counter(r["meta"].get("label_form") for r in rows)
    E["masked_row_share"] = round(lf["masked"] / n, 4); E["swapped_row_share"] = round(lf["swapped"] / n, 4)
    if not within(lf["masked"] / n, 0.10, 0.15):
        fails.append("E.masked_share")
    if abs(lf["swapped"] / n - 0.05) > 0.05:
        soft.append("E.swapped_share")
    cards = {}
    for r in rows:
        cards.setdefault(r["meta"]["card_id"], r)
    nc = len(cards)
    few = len({r["meta"]["card_id"] for r in rows if r["meta"].get("defs_style") == "few_shot"})
    E["fewshot_card_share"] = round(few / nc, 4)  # few-shot cards = 3 worked cases (defs_style few_shot), not 1-2-case style
    if not within(few / nc, 0.05, 0.10):
        fails.append("E.fewshot_cards")
    bds = Counter(r["meta"].get("base_defs_style") or r["meta"].get("defs_style") for r in cards.values())
    E["card_defs_styles"] = dict(bds)
    E["one_line_examples_card_share"] = round(bds["one_line_examples"] / nc, 4)
    if abs(bds["one_line_examples"] / nc - 0.5) > 0.05:
        soft.append("E.one_line_examples_cards")
    short_rows = sum(1 for r in rows if (r["meta"].get("base_defs_style") or r["meta"].get("defs_style")) == "short")
    E["short_card_row_share"] = round(short_rows / n, 4)
    if not within(short_rows / n, 0.13, 0.17):
        fails.append("E.short_rows")
    deep = sum(1 for r in rows if r["meta"].get("deep")); E["deep_row_share"] = round(deep / n, 4)
    if deep / n > 0.10:
        fails.append("E.deep_rows")
    rev = 0
    for r in cards.values():
        ol = r["meta"]["option_level"]; lo = [o for o, v in ol.items() if v == 0][0]; hi = [o for o, v in ol.items() if v == L.K(r) - 1][0]
        if L.opt_num(lo) and L.opt_num(hi) and int(L.opt_num(lo)) > int(L.opt_num(hi)):
            rev += 1
    E["reversed_numbering_cards"] = rev; E["reversed_numbering_card_share"] = round(rev / nc, 4)
    if rev / nc > 0.10:
        fails.append("E.reversed_numbering")
    sev = Counter()
    for r in cards.values():
        m = re.search(r"Higher on this scale means ([^.]*)\.", r["instructions"])
        sev["better" if m and m.group(1).startswith("better") else ("more" if m else "unparsed")] += 1
    E["scale_meaning_cards"] = dict(sev); bs = sev["better"] / max(1, sev["better"] + sev["more"])
    E["scale_better_share"] = round(bs, 4)
    if not within(bs, 0.45, 0.55):
        fails.append("E.scale_meaning")
    E["K_card_shares"] = {str(k): round(v / nc, 4) for k, v in sorted(Counter(L.K(r) for r in cards.values()).items())}
    um = {}
    for s in ("S1", "S2", "S4"):
        rs = [r for r in rows if r["meta"]["sampler"] == s]
        u = [r for r in rs if (r["meta"].get("case_features") or {}).get("unmentioned", 0) > 0]
        dec = [r for r in u if any(e["kind"] == "conv" and e["conv"] == "C1" for e in r["meta"].get("edge") or [])]
        um[s] = {"unmentioned_row_share": round(len(u) / len(rs), 4), "decisive_share": round(len(dec) / max(1, len(u)), 4)}
        if not within(len(u) / len(rs), 0.20, 0.30):
            fails.append(f"E.unmentioned_{s}")
        if not within(len(dec) / max(1, len(u)), 0.40, 0.60):
            fails.append(f"E.unmentioned_decisive_{s}")
    E["unmentioned"] = um
    ot = {}
    for s in ("S1", "S3", "S4"):
        rs = [r for r in rows if r["meta"]["sampler"] == s]
        inert = sum(1 for r in rs if (r["meta"].get("case_features") or {}).get("inert_subject")
                    or (r["meta"].get("case_features") or {}).get("other") == "inert")
        ot[s] = round(inert / len(rs), 4)
        if abs(inert / len(rs) - 0.30) > 0.05:
            soft.append(f"E.inert_{s}")
    E["inert_share"] = ot
    rs4 = [r for r in rows if r["meta"]["sampler"] == "S4"]
    dsh = sum(1 for r in rs4 if (r["meta"].get("case_features") or {}).get("other") == "distractor") / len(rs4)
    E["S4_distractor_share"] = round(dsh, 4)
    if abs(dsh - 0.20) > 0.05:
        soft.append("E.distractor_S4")
    res["E_quotas"] = E
    res["fails"] = fails; res["soft_misses"] = soft; res["pass"] = not fails
    json.dump(res, open(L.QC / f"g10_{NAME}.json", "w"), indent=1)
    print(json.dumps({"pass": res["pass"], "fails": fails, "soft": soft}))


if __name__ == "__main__":
    main()
