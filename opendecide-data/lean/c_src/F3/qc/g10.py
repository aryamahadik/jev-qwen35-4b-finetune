"""G10 balance (independent F3 checker), all v4 rules that apply to F3: spec 8 G10 + spec 2.1 quotas + F3 G0 section 5
balance table (and XF01, XF02, XF04). Runs on out/candidates_r1.jsonl (the round-1 candidate pool) with the QC sidecar.
Two kinds of check:
- POOL checks: properties of each row or its display that selection cannot fix (abstain display and gold = 1/k, gold
  letter uniform, longest option, attack vs label); they must pass on the pool.
- SELECTED-SET targets: F3 G0 R1-13 says these are checked on the final selected set after G9 (bins and selection do
  not exist yet). They are reported on the pool AND checked for feasibility: a selection of the round-1 size (4,500
  rows; choice and yes/no sub-targets scaled) can meet the target from the pool's rows. Joint feasibility of all
  targets at once is not proven here. G9 crowd bins do not exist yet, so the 'bin' axis of the yes-rate cells is pooled.
Usage: g10.py [candidates_r1]"""
import json, math, sys
from collections import Counter, defaultdict
from scipy.stats import chisquare, chi2_contingency, binomtest
import qc_lib as L
sys.path.insert(0, str(L.LEAN / "c_src/common"))
import negcount

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
N_SEL = 4500  # round-1 F3 rows (spec 2.2; F3 G0 section 1)
U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def share_check(name, n_in, n_all, lo, hi, n_sel, scope="family"):
    """pool share + feasibility for a share target [lo, hi] on a selection of n_sel rows."""
    sh = n_in / max(1, n_all)
    feas = n_in >= math.ceil(lo * n_sel) and (n_all - n_in) >= math.ceil((1 - hi) * n_sel)
    return {"target": name, "scope": scope, "pool_share": round(sh, 4), "pool_n": n_in, "pool_den": n_all,
            "band": [lo, hi], "pool_in_band": lo <= sh <= hi, "feasible_on_selection": bool(feas)}


def rate_check(name, yes, n, lo, hi, n_sel_rows, scope):
    """pool yes-rate + feasibility: a subset of n_sel_rows rows (or all if fewer) with a rate inside [lo, hi]."""
    r = yes / max(1, n); m = min(n, n_sel_rows); no = n - yes
    feas = n > 0 and yes >= math.ceil(lo * m) and no >= math.ceil((1 - hi) * m)
    return {"target": name, "scope": scope, "pool_rate": round(r, 4), "n": n, "band": [lo, hi],
            "pool_in_band": lo <= r <= hi, "feasible_on_selection": bool(feas)}


def pool_checks(rows, side, out):
    ch = [r for r in rows if not L.is_yn(r)]; yn = [r for r in rows if L.is_yn(r)]
    P = {}
    # gold letter uniform per option bucket (canonical stored order), family and per sampler
    for scope in ["family"] + sorted({r["meta"]["sampler"] for r in ch}):
        rs = [r for r in ch if scope == "family" or r["meta"]["sampler"] == scope]
        for b in ("2-4", "5-9", "10-19", "20-60"):
            sub = [r for r in rs if bucket(len(r["options"])) == b]
            if len(sub) < 20:
                continue
            pos = Counter(r["options"].index(r["gold"]) for r in sub)
            exp = defaultdict(float)
            for r in sub:
                for j in range(len(r["options"])):
                    exp[j] += 1 / len(r["options"])
            keys = sorted(exp); ob = [pos.get(j, 0) for j in keys]; ex = [exp[j] for j in keys]
            # pool sparse tail positions (expected < 5) into one cell
            o2, e2, ot, et = [], [], 0, 0.0
            for o, e in zip(ob, ex):
                if e >= 5:
                    o2.append(o); e2.append(e)
                else:
                    ot += o; et += e
            if et > 0:
                o2.append(ot); e2.append(et)
            p = float(chisquare(o2, e2).pvalue) if len(o2) > 1 else 1.0
            P[f"gold_letter_{scope}_{b}"] = {"n": len(sub), "p": round(p, 4), "pass": p > 0.01}
    # longest option is gold within +/- 2 pp of 1/k (ties: expected m/k), family and per sampler
    for scope in ["family"] + sorted({r["meta"]["sampler"] for r in ch}):
        rs = [r for r in ch if scope == "family" or r["meta"]["sampler"] == scope]
        obs = exp = inv = 0.0
        for r in rs:
            ls = [len(o) for o in r["options"]]; mx = max(ls); m = sum(l == mx for l in ls)
            obs += int(len(r["gold"]) == mx); exp += m / len(ls); inv += 1 / len(ls)
        n = max(1, len(rs))
        P[f"longest_is_gold_{scope}"] = {"n": len(rs), "obs": round(obs / n, 4), "exp_with_ties": round(exp / n, 4),
                                         "mean_1_over_k": round(inv / n, 4), "pass": abs(obs - exp) / n <= 0.02}
    # abstain display (XF01): shown only at k >= 3; NEI only on open-world rows, None only on Q7 rows; gold = 1/k +/- 2 pp
    bad_k = bad_world = bad_q7 = 0; cells = defaultdict(lambda: [0, 0.0, 0])
    for r in ch:
        s = side[r["id"]]; ab = [o for o in r["options"] if L.is_abstain(o)]
        if s.get("qt") == "Q7" and not ab:
            bad_q7 += 1
        if not ab:
            continue
        k = len(r["options"])
        bad_k += int(k < 3)
        kind = s.get("abstain") or "?"
        bad_world += int(kind == "NEI" and s.get("world") != "open")
        bad_q7 += int(kind == "None" and s.get("qt") != "Q7")
        c = cells[(kind, bucket(k))]; c[0] += int(L.is_abstain(r["gold"])); c[1] += 1 / k; c[2] += 1
    P["abstain_display"] = {"shown_at_k_lt_3": bad_k, "NEI_on_closed_rows": bad_world, "None_display_rule_breaks": bad_q7,
                            "pass": bad_k == 0 and bad_world == 0 and bad_q7 == 0}
    for (kind, b), (g, e, n) in sorted(cells.items()):
        P[f"abstain_wrong_ge_50pct_{kind}_{b}"] = {"n_shown": n, "gold_share": round(g / n, 4),
                                                   "exp_1_over_k": round(e / n, 4), "wrong_share": round(1 - g / n, 4),
                                                   "pass": (1 - g / n) >= 0.5}
        # XF01 gold = 1/k +/- 2 pp: a selected-set target (F3 G0 R1-13), reported with feasibility
        out.setdefault("_abst_cells", []).append((kind, b, g, n, e / n))
    # attack present uncorrelated with the label
    t = [[0, 0], [0, 0]]
    for r in yn:
        t[int(bool(side[r["id"]].get("attack")))][int(r["gold"])] += 1
    p = float(chi2_contingency(t).pvalue) if min(map(sum, t)) > 0 else 1.0
    P["attack_vs_label_yes_no"] = {"table_[clean,attack]x[no,yes]": t, "p": round(p, 4), "pass": p > 0.01}
    t = [[0, 0], [0, 0]]
    for r in ch:
        if any(L.is_abstain(o) for o in r["options"]):
            t[int(bool(side[r["id"]].get("attack")))][int(L.is_abstain(r["gold"]))] += 1
    p = float(chi2_contingency(t).pvalue) if min(map(sum, t)) > 0 else 1.0
    P["attack_vs_abstain_gold_choice"] = {"table": t, "p": round(p, 4), "pass": p > 0.01}
    out["pool_checks"] = P
    out["pool_checks_pass"] = all(v["pass"] for v in P.values())


def selected_set_targets(rows, side, out):
    T = []; n_all = len(rows); scale = N_SEL / n_all
    ch = [r for r in rows if not L.is_yn(r)]; yn = [r for r in rows if L.is_yn(r)]
    n_ch_sel = round(N_SEL * 0.5); n_yn_sel = N_SEL - n_ch_sel
    T.append(share_check("yes/no share 45-55%", len(yn), n_all, 0.45, 0.55, N_SEL))
    # aggregate yes rate 50 +/- 2 per family x wording x (bin: pooled, G9 pending) x negation count (k_all, negcount)
    cells = defaultdict(lambda: [0, 0]); negq = {}
    for r in yn:
        q, _ = L.split_q(r["instructions"]); nc = negcount.count(q); negq[r["id"]] = nc
        c = cells[(r["meta"]["wording_id"], min(nc.k_all, 3))]; c[0] += int(r["gold"]); c[1] += 1
    fam = rate_check("aggregate yes rate 50+/-2", sum(c[0] for c in cells.values()), len(yn), 0.48, 0.52,
                     n_yn_sel, "family")
    T.append(fam)
    cell_res = [rate_check(f"yes rate cell wording={w} k_all={k}", y, n, 0.48, 0.52, round(n * scale), "cell")
                for (w, k), (y, n) in sorted(cells.items())]
    T.append({"target": "yes rate 50+/-2 per wording x k_all cell (bin pooled)", "scope": "cells",
              "cells": len(cell_res), "cells_in_band": sum(c["pool_in_band"] for c in cell_res),
              "cells_infeasible": [c["target"] for c in cell_res if not c["feasible_on_selection"]],
              "pool_in_band": all(c["pool_in_band"] for c in cell_res),
              "feasible_on_selection": all(c["feasible_on_selection"] for c in cell_res)})
    # per-card yes rate (R2-05): base rows within +/- 5 pp of the drawn rate (cards with >= 10 base rows); all rows 20-80%
    byc = defaultdict(list)
    for r in yn:
        byc[r["meta"]["card_id"]].append(r)
    off, out_band, infeas = [], [], []
    for c, rs in sorted(byc.items()):
        base = [r for r in rs if not r["meta"].get("twin_of")]; dr = side[rs[0]["id"]].get("card_yes_rate")
        ay = sum(r["gold"] for r in rs) / len(rs)
        if not (0.2 <= ay <= 0.8):
            out_band.append(c)
            ys = sum(r["gold"] for r in rs)
            if not rate_check("", ys, len(rs), 0.2, 0.8, round(len(rs) * scale), "")["feasible_on_selection"]:
                infeas.append(c)
        if len(base) >= 10 and dr is not None:
            by = sum(r["gold"] for r in base)
            if abs(by / len(base) - dr) > 0.05:
                off.append({"card": c, "n_base": len(base), "realized": round(by / len(base), 3), "drawn": dr})
            if not rate_check("", by, len(base), dr - 0.05, dr + 0.05, round(len(base) * scale), "")["feasible_on_selection"]:
                infeas.append(c)
    T.append({"target": "per-card base yes rate within +/-5 pp of drawn; all yes/no rows of a card 20-80%", "scope": "card",
              "cards_checked": sum(1 for rs in byc.values() if sum(1 for r in rs if not r['meta'].get('twin_of')) >= 10),
              "cards_off_drawn": len(off), "off_examples": off[:12], "cards_outside_20_80": out_band,
              "cards_infeasible": infeas, "pool_in_band": not off and not out_band,
              "feasible_on_selection": not infeas})
    out["_negq"] = negq
    return T, ch, yn, n_ch_sel, n_yn_sel


def f3_targets(rows, side, out, T, ch, yn, n_ch_sel, n_yn_sel):
    negq = out.pop("_negq"); byid = {r["id"]: r for r in rows}; samplers = sorted({r["meta"]["sampler"] for r in rows})
    for sp in samplers:
        ys = [r for r in yn if r["meta"]["sampler"] == sp]; m = round(len(ys) * N_SEL / len(rows))
        bad = sum(1 for r in ys if side[r["id"]].get("polarity") == "bad")
        T.append(share_check(f"'yes = bad outcome' 50+/-5 [{sp}]", bad, len(ys), 0.45, 0.55, m, sp))
        k1 = sum(1 for r in ys if negq[r["id"]].k_syn >= 1); ka = sum(1 for r in ys if negq[r["id"]].k_all >= 1)
        k2 = 0
        for r in ys:
            if negq[r["id"]].k_syn >= 2:
                tw = byid.get(r["meta"].get("twin_of") or "")
                k2 += int(tw is not None and L.is_yn(tw) and negcount.count(L.split_q(tw["instructions"])[0]).k_syn == 0)
        T.append(share_check(f"k_syn>=1 >= 10% [{sp}]", k1, len(ys), 0.10, 1.0, m, sp))
        T.append(share_check(f"k_all>=1 >= 15% [{sp}]", ka, len(ys), 0.15, 1.0, m, sp))
        T.append(share_check(f"k_syn>=2 with affirmative twin >= 3% [{sp}]", k2, len(ys), 0.03, 1.0, m, sp))
    bk = Counter(bucket(len(r["options"])) for r in ch)
    for b, t in (("2-4", .35), ("5-9", .35), ("10-19", .15), ("20-60", .15)):
        T.append(share_check(f"option bucket {b} {int(t*100)}+/-3", bk[b], len(ch), t - .03, t + .03, n_ch_sel))
    for kind in ("NEI", "None"):
        for (kd, b, g, n, e) in out.get("_abst_cells", []):
            if kd == kind:
                T.append(rate_check(f"abstain {kind} gold = 1/k +/-2 [{b}]", g, n, e - .02, e + .02, round(n * N_SEL / len(rows)), b))
    out.pop("_abst_cells", None)
    cw = {}
    for r in rows:
        cw[r["meta"]["card_id"]] = side[r["id"]].get("world")
    nopen = sum(1 for w in cw.values() if w == "open")
    T.append(dict(share_check("open-world cards 30+/-5 (card-level; selection keeps every card)", nopen, len(cw), .25, .35, len(cw)),
                  feasible_on_selection=.25 <= nopen / len(cw) <= .35))
    dec = Counter(side[r["id"]]["decisive_decile"] for r in rows if side[r["id"]].get("decisive_decile") is not None)
    obs = [dec.get(i, 0) for i in range(10)]; p = float(chisquare(obs).pvalue); nd = sum(obs); need = nd * N_SEL / len(rows) / 10
    T.append({"target": "decisive decile uniform (chi-square p > 0.01)", "scope": "family", "counts": obs, "p": round(p, 5),
              "pool_in_band": p > 0.01, "feasible_on_selection": min(obs) >= 0.8 * need})
    eb = Counter(side[r["id"]]["event_bin"] for r in rows)
    for b, t in ((0, .30), (1, .40), (2, .30)):
        T.append(share_check(f"event bin {['5-12','13-24','25-40'][b]} {int(t*100)}+/-5", eb[b], len(rows), t - .05, t + .05, N_SEL))
    nd_rows = [r for r in rows if not r["meta"].get("deep")]; dp = Counter(min(int(r["meta"]["depth"] or 1), 4) for r in nd_rows)
    for d, t in ((1, .15), (2, .30), (3, .30), (4, .25)):
        T.append(share_check(f"depth d{d} {int(t*100)}+/-5 (non-deep rows)", dp[d], len(nd_rows), t - .05, t + .05, round(N_SEL * .9)))
    T.append(share_check("deep rows <= 10%", len(rows) - len(nd_rows), len(rows), 0.0, 0.10, N_SEL))
    return samplers


def f3_targets2(rows, side, out, T, ch, yn, n_ch_sel, samplers):
    mech = ("VOID", "CORRECTION", "SUPERSEDE", "RENAME", "MERGE", "PLAIN")
    for mm in mech:
        on = [r for r in rows if mm in (side[r["id"]].get("mechanisms") or [])]
        T.append(share_check(f"decisive mechanism {mm} >= 8% of rows", len(on), len(rows), 0.08, 1.0, N_SEL))
        oy = [r for r in on if L.is_yn(r)]
        T.append(rate_check(f"yes rate on decisive mechanism {mm} 50+/-5", sum(r["gold"] for r in oy), len(oy), .45, .55,
                            round(len(oy) * N_SEL / len(rows)), "family"))
    for sp in samplers:
        rs = [r for r in rows if r["meta"]["sampler"] == sp]
        for mm in ("VOID", "CORRECTION", "SUPERSEDE", "RENAME", "MERGE", "CHECK"):
            ap = [r for r in rs if mm in (side[r["id"]].get("mech_present") or [])]
            if len(ap) < 20:
                continue
            dcs = sum(1 for r in ap if mm in (side[r["id"]].get("mechanisms") or []))
            T.append(share_check(f"{mm} decisive where present 50+/-10 [{sp}]", dcs, len(ap), .40, .60,
                                 round(len(ap) * N_SEL / len(rows)), sp))
    mk = sum(1 for r in ch if side[r["id"]].get("vocab") == "masked" and side[r["id"]].get("status_option_row"))
    sw = sum(1 for r in ch if side[r["id"]].get("vocab") == "swapped" and side[r["id"]].get("status_option_row"))
    T.append(share_check("masked status-option rows 10-15% of choice rows", mk, len(ch), .10, .15, n_ch_sel))
    T.append(share_check("swapped status-option rows 5+/-1% of choice rows", sw, len(ch), .04, .06, n_ch_sel))
    cards = {}
    for r in rows:
        c = cards.setdefault(r["meta"]["card_id"], {"inv": False, "few": False})
        c["inv"] |= bool(side[r["id"]].get("inverted_card")); c["few"] |= "fewshot" in (r["meta"].get("edge") or [])
    ni = sum(c["inv"] for c in cards.values()); nf = sum(c["few"] for c in cards.values()); nc = len(cards)
    T.append(dict(share_check("inverted cards 10-15% (card-level)", ni, nc, .10, .15, nc), feasible_on_selection=.10 <= ni / nc <= .15))
    T.append(dict(share_check("few-shot cards 5-10% (card-level)", nf, nc, .05, .10, nc), feasible_on_selection=.05 <= nf / nc <= .10))
    q7 = sum(1 for r in rows if side[r["id"]].get("qt") == "Q7")
    T.append(share_check("Q7 rows 10+/-3% of rows", q7, len(rows), .07, .13, N_SEL))
    tk = Counter(r["meta"].get("twin_kind") for r in rows); ids_ff = set()
    for r in rows:
        if r["meta"].get("twin_kind") in ("fact_flip", "premise_removal"):
            ids_ff.add(r["id"]); ids_ff.add(r["meta"]["twin_of"])
    T.append(share_check("contrast-set rows (fact-flip / premise-removal + base) 20-25%", len(ids_ff), len(rows), .20, .25, N_SEL))
    out["report_only"] = {"attack_twin_share (about 5%)": round(tk["attack"] / len(rows), 4),
                          "short_or_no_card_rows (about 15%)": round(sum(1 for r in rows if side[r["id"]].get("rule21")) / len(rows), 4),
                          "one_line_examples_cards (about 50%)": round(len({r["meta"]["card_id"] for r in rows if r["meta"]["defs_style"] == "one_line_examples"}) / nc, 4),
                          "difficulty_bins": "pending G9 crowd scoring (no bins exist yet); not checkable before G9",
                          "qt_counts": dict(Counter(side[r["id"]].get("qt") for r in rows))}


def main():
    rows, side = L.load(NAME)
    out = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "selection_size_r1": N_SEL,
           "note": "bin axis pooled (G9 pending); selected-set targets judged by feasibility, pool values reported"}
    pool_checks(rows, side, out)
    T, ch, yn, n_ch_sel, n_yn_sel = selected_set_targets(rows, side, out)
    samplers = f3_targets(rows, side, out, T, ch, yn, n_ch_sel, n_yn_sel)
    f3_targets2(rows, side, out, T, ch, yn, n_ch_sel, samplers)
    out["selected_set_targets"] = T
    out["targets_outside_band_on_pool"] = [t["target"] for t in T if not t["pool_in_band"]]
    out["targets_infeasible"] = [t["target"] for t in T if not t["feasible_on_selection"]]
    out["pass"] = out["pool_checks_pass"] and not out["targets_infeasible"]
    (L.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"pool_checks_pass": out["pool_checks_pass"],
                      "pool_fails": [k for k, v in out["pool_checks"].items() if not v["pass"]],
                      "outside_band": out["targets_outside_band_on_pool"], "infeasible": out["targets_infeasible"],
                      "pass": out["pass"]}, indent=1))


if __name__ == "__main__":
    main()
