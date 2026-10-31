"""F4 quota report on a row set (rows + sidecar): 2.1 / G0 section 6, 7.5, 8 shares, negcount quotas (k_syn / k_all).

  python quota.py <rows.pkl | rows.jsonl sidecar.jsonl>
Returns a dict of measured shares and a list of failed checks (hard checks only; 'about' targets are reported)."""
from __future__ import annotations

import collections
import json
import pickle
import sys


def bucket(k):
    return "2-4" if k <= 4 else ("5-9" if k <= 9 else ("10-19" if k <= 19 else "20-60"))


def report(rows, side, cards=None):
    sd = {s["id"]: s for s in side}
    n = len(rows)
    out, fails = {}, []
    yn = [r for r in rows if r["qtype"] != "choice"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    out["rows"] = n
    out["yn_share"] = round(len(yn) / n, 4)
    if not 0.45 <= out["yn_share"] <= 0.55:
        fails.append("yn_share")
    out["yes_rate"] = round(sum(1 for r in yn if r["gold"] == 1) / max(1, len(yn)), 4)
    if abs(out["yes_rate"] - 0.5) > 0.02:
        fails.append("yes_rate")
    yb = [sd[r["id"]]["yes_bad"] for r in yn]
    out["yes_bad_share"] = round(sum(1 for x in yb if x) / max(1, len(yb)), 4)
    if abs(out["yes_bad_share"] - 0.5) > 0.05:
        fails.append("yes_bad")
    ksyn = [sd[r["id"]]["k_syn"] for r in yn]
    out["yn_syn_neg_share"] = round(sum(1 for k in ksyn if k >= 1) / max(1, len(yn)), 4)
    if out["yn_syn_neg_share"] < 0.10:
        fails.append("syn_neg<10%")
    out["yn_dneg_share"] = round(sum(1 for r in yn if sd[r["id"]]["form"] == "YN-dn") / max(1, len(yn)), 4)
    if out["yn_dneg_share"] < 0.02:
        fails.append("dneg<2%")
    out["yn_k_syn_ge2_share"] = round(sum(1 for k in ksyn if k >= 2) / max(1, len(yn)), 4)
    kall = collections.Counter(sd[r["id"]]["k_all"] for r in yn)
    out["yn_k_all_hist"] = dict(sorted(kall.items()))
    # yes rate per negation count
    yr = collections.defaultdict(lambda: [0, 0])
    for r in yn:
        c = yr[sd[r["id"]]["k_all"]]
        c[0] += r["gold"] == 1
        c[1] += 1
    out["yes_rate_by_k_all"] = {k: round(a / b, 3) for k, (a, b) in sorted(yr.items())}
    units = collections.Counter(sd[r["id"]]["unit"] for r in rows)
    out["unit_share"] = {k: round(v / n, 4) for k, v in sorted(units.items())}
    ct = sum(1 for r in rows if "twinset:contrast" in r["meta"]["edge"]) / n
    out["contrast_twinset_share"] = round(ct, 4)
    if not 0.20 <= ct <= 0.25:
        fails.append("contrast_share")
    att = sum(1 for r in rows if r["meta"]["twin_kind"] == "attack") / n
    out["attacked_share"] = round(att, 4)
    inert = sum(1 for r in rows if any(e.startswith("inert:") for e in r["meta"]["edge"])) / n
    out["inert_sentence_share"] = round(inert, 4)
    lab = lambda r: next(e for e in r["meta"]["edge"] if e.startswith("L:"))
    il, cl = collections.defaultdict(lambda: [0, 0]), collections.defaultdict(lambda: [0, 0])
    for r in rows:
        e = r["meta"]["edge"]
        x = il[lab(r)]
        x[0] += any(t.startswith("inert:") for t in e)
        x[1] += 1
        y = cl[(lab(r), "neg" if sd[r["id"]]["claim_neg"] else "pos")]
        y[0] += any(t.startswith("carrier:") for t in e)
        y[1] += 1
    out["inert_share_by_label"] = {k: round(a / b, 3) for k, (a, b) in sorted(il.items())}
    out["carrier_share_by_label_pol"] = {"/".join(k): round(a / b, 3) for k, (a, b) in sorted(cl.items())}
    ch3 = collections.Counter(sd[r["id"]]["label_c"] for r in rows if sd[r["id"]]["form"] == "CH-3")
    t3 = sum(ch3.values())
    out["ch3_gold_share"] = {k: round(v / max(1, t3), 4) for k, v in sorted(ch3.items())}
    if t3 and any(abs(v / t3 - 1 / 3) > 0.02 for v in ch3.values()):
        fails.append("ch3_gold_share")
    nb = collections.defaultdict(lambda: [0, 0.0, 0])
    for r in rows:
        if sd[r["id"]]["form"] == "CH-claim" and any(o.startswith("None of these") for o in r["options"]):
            x = nb[bucket(len(r["options"]))]
            x[0] += r["gold"].startswith("None of these")
            x[1] += 1 / len(r["options"])
            x[2] += 1
    out["none_gold_minus_1k_pp"] = {b: (round(100 * (a - e) / c, 2), c) for b, (a, e, c) in sorted(nb.items())}
    wy = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        w = next(e for e in r["meta"]["edge"] if e.startswith("world:"))
        x = wy[w]
        x[2] += sd[r["id"]]["claim_neg"]
        x[3] += 1
        if r["qtype"] != "choice":
            x[0] += r["gold"] == 1
            x[1] += 1
    out["by_world"] = {w: {"yes_rate": round(a / max(1, b), 4), "neg_claim": round(c / d_, 4), "rows": d_}
                       for w, (a, b, c, d_) in sorted(wy.items())}
    for w, v in out["by_world"].items():
        if abs(v["yes_rate"] - 0.5) > 0.02:
            fails.append("yes_rate_" + w)
        if not 0.30 <= v["neg_claim"] <= 0.40:
            fails.append("neg_claim_" + w)
    for k, v in out["inert_share_by_label"].items():
        if abs(v - 0.30) > 0.02:
            fails.append("inert_" + k)
    for k, v in out["carrier_share_by_label_pol"].items():
        if abs(v - 0.25) > 0.03:
            fails.append("carrier_" + k)
    out["deep_rows"] = sum(1 for r in rows if r["meta"]["deep"])
    out["depth_hist"] = dict(sorted(collections.Counter(r["meta"]["depth"] for r in rows).items()))
    if any(not 2 <= r["meta"]["depth"] <= 4 for r in rows if r["meta"]["sampler"] != "S5"):
        fails.append("training_depth_outside_2_4")
    der = [r for r in rows if any(e in ("L:F", "L:R") for e in r["meta"]["edge"]) or
           ("L:T" in r["meta"]["edge"] and not sd[r["id"]]["claim_neg"]) or
           ("L:Fa" in r["meta"]["edge"] and sd[r["id"]]["claim_neg"])]
    ow_der = [r for r in der if "world:ow" in r["meta"]["edge"]]
    def sh(xs, tag):
        return round(sum(1 for r in xs if tag in r["meta"]["edge"]) / max(1, len(xs)), 4)
    out["inf_mix"] = {"n_derived": len(der), "mt_of_ow": sh(ow_der, "inf:mt"), "link": sh(der, "inf:link"),
                      "exc": sh(der, "inf:exc"),
                      "thr_or_date": round(sum(1 for r in der if "inf:thr" in r["meta"]["edge"] or
                                               "inf:date" in r["meta"]["edge"]) / max(1, len(der)), 4)}
    td = [r for r in der if "inf:thr" in r["meta"]["edge"] or "inf:date" in r["meta"]["edge"]]
    out["inf_mix"]["boundary_of_thr"] = sh(td, "boundary:eq")
    # choice rows
    if ch:
        bk = collections.Counter(bucket(len(r["options"])) for r in ch)
        out["option_buckets"] = {k: round(v / len(ch), 4) for k, v in sorted(bk.items())}
        gl = collections.defaultdict(collections.Counter)
        for r in ch:
            gl[bucket(len(r["options"]))][r["options"].index(r["gold"])] += 1
        out["gold_pos_minmax_by_bucket"] = {b: (min(c.values()), max(c.values()), len(c)) for b, c in gl.items()}
        lf = collections.Counter(sd[r["id"]]["label_form"] for r in ch)
        out["label_form_share_choice"] = {k: round(v / len(ch), 4) for k, v in lf.items()}
        out["form_share_choice"] = {k: round(v / len(ch), 4) for k, v in
                                    collections.Counter(sd[r["id"]]["form"] for r in ch).items()}
        ab = [r for r in ch if any(o.startswith("None of these") or o.lower().startswith("cannot be determined")
                                   for o in r["options"])]
        abw = sum(1 for r in ab if not (r["gold"].startswith("None of these") or
                                        r["gold"].lower().startswith("cannot be determined")))
        out["abstain_shown_rows"] = len(ab)
        out["abstain_wrong_share"] = round(abw / max(1, len(ab)), 4)
        if ab and abw / len(ab) < 0.5:
            fails.append("abstain_wrong<50%")
        from scipy.stats import chisquare
        gk = collections.defaultdict(collections.Counter)
        for r in ch:
            gk[len(r["options"])][r["options"].index(r["gold"])] += 1
        pv = {}
        for b in ("2-4", "5-9", "10-19", "20-60"):
            # pooled per bucket: position as a fraction of k, in k equal-width bins of the bucket's smallest k
            ks = [k for k in gk if bucket(k) == b]
            if not ks:
                continue
            m = min(ks)
            cnt = collections.Counter()
            for k in ks:
                for pos, c in gk[k].items():
                    cnt[int(pos * m / k)] += c
            obs = [cnt[i] for i in range(m)]
            exp_ = [0.0] * m
            for k in ks:
                tot = sum(gk[k].values())
                for pos in range(k):
                    exp_[int(pos * m / k)] += tot / k
            pv[b] = round(float(chisquare(obs, exp_).pvalue), 4)
            if pv[b] <= 0.01:
                fails.append("gold_pos_" + b)
        out["gold_pos_chi2_p"] = pv
        lgf = collections.defaultdict(lambda: [0, 0.0, 0])
        for r in ch:
            x = lgf[sd[r["id"]]["form"]]
            x[0] += max(r["options"], key=len) == r["gold"]
            x[1] += 1 / len(r["options"])
            x[2] += 1
        out["longest_gold_pp_by_form"] = {f: round(100 * (a - b) / c, 2) for f, (a, b, c) in lgf.items()}
        lg = sum(1 for r in ch if max(r["options"], key=len) == r["gold"])
        exp = sum(1 / len(r["options"]) for r in ch)
        out["longest_is_gold_minus_chance_pp"] = round(100 * (lg - exp) / len(ch), 2)
        if abs(100 * (lg - exp) / len(ch)) > 2:
            fails.append("longest_gold")
    out["sampler_share"] = {k: round(v / n, 4) for k, v in
                            sorted(collections.Counter(r["meta"]["sampler"] for r in rows).items())}
    out["short_card_rows_share"] = round(sum(1 for r in rows if sd[r["id"]]["short"]) / n, 4)
    cc = collections.Counter(r["meta"]["card_id"] for r in rows)
    v = sorted(cc.values())
    out["cards"] = len(cc)
    out["rows_per_card_median_max"] = (v[len(v) // 2], v[-1])
    if v[-1] > 128:
        fails.append("card>128")
    out["packs"] = len({r["meta"]["domain_pack"] for r in rows})
    ds = collections.Counter()
    seen = set()
    for r in rows:
        if r["meta"]["card_id"] not in seen:
            seen.add(r["meta"]["card_id"])
            ds[r["meta"]["defs_style"]] += 1
    out["defs_style_cards"] = dict(ds)
    out["wordings"] = len({r["meta"]["wording_id"] for r in rows})
    wc = collections.defaultdict(set)
    for r in rows:
        wc[r["meta"]["card_id"]].add(r["meta"]["wording_id"])
    out["min_wordings_per_card"] = min(len(x) for x in wc.values())
    tpl = collections.Counter((r["meta"]["wording_id"], next(e for e in r["meta"]["edge"] if e.startswith("frame:")))
                              for r in rows)
    out["max_template_share"] = round(max(tpl.values()) / n, 4)
    if max(tpl.values()) / n > 0.02:
        fails.append("template>2%")
    out["styles"] = len({r["meta"]["format_style"] for r in rows})
    calls = collections.Counter(r["call_id"] for r in rows)
    out["max_call_unit"] = max(calls.values())
    if max(calls.values()) > 3:
        fails.append("call_unit>3")
    lens = sorted(sd[r["id"]]["len_tokens"] for r in rows)
    out["len_median_max"] = (lens[len(lens) // 2], lens[-1])
    if lens[-1] > 1900:
        fails.append("len>1900")
    return out, fails


def load(argv):
    if argv[0].endswith(".pkl"):
        d = pickle.load(open(argv[0], "rb"))
        return d["rows"], d["side"]
    rows = [json.loads(x) for x in open(argv[0])]
    side = [json.loads(x) for x in open(argv[1])]
    return rows, side


if __name__ == "__main__":
    rows, side = load(sys.argv[1:])
    o, f = report(rows, side)
    print(json.dumps({"report": o, "fails": f}, indent=1, default=str))
