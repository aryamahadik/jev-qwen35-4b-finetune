"""G7 feature z-test (independent F6 checker). C_DATA_SPEC v4 8 G7 + F6 G0 6: one-sided binomial per unigram, bigram
and metadata feature, p0 = 1/k, alpha 0.01 Bonferroni over the tested features (n >= N_MIN occurrences).
- Yes/no rows: feature = presence of a lower-cased unigram/bigram in the model-visible text (card + instructions +
  state), a v4 G6(d) metadata value (qc_lib.meta_feats: depth, rule-count proxy, lengths, number magnitudes, name pool,
  template / wording / style id, sampler) or an F6 G7 feature (marker tokens, evidence tag, plan words, unless, only if,
  exactly when, complete, n_gaps, gap kinds / positions, frame_id, label form). Raw test p0 = .5 (majority direction);
  card-adjusted test (per-card yes rates are drawn U[20,80] by design): Poisson-binomial null with the row's
  leave-one-out card yes rate, normal approx + continuity, two-sided.
- Choice rows: feature = a unigram/bigram inside an option, an option kind (abstain kind, longest, shortest, verbatim in
  record, ID most / least mentioned) or a row-metadata x option-kind cross. Unit = (row, options with f);
  success = gold holds f; null = Poisson-binomial m_r / k_r.
Pass: no card-adjusted yes/no failure, no choice failure, no raw yes/no failure spanning > 1 card.
Usage: g7.py [name]"""
import json, math, re, sys
from collections import defaultdict, Counter
from scipy.stats import binom, norm
import qc_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
ALPHA = 0.01; N_MIN = 20
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
ABST = {"nei": ["Cannot be determined from the record", "The record does not settle this", "Not enough information to decide",
                "Undetermined on this record", "The record leaves this open"],
        "none": ["None of the listed outcomes", "None of these", "No listed outcome fits", "No outcome on this list applies"],
        "nothing": ["No additional detail is required", "No further fact is needed"]}
KIND = {t: k for k, ts in ABST.items() for t in ts}
BLANK1 = re.compile(r"\|[ \t]*\|"); BLANK2 = re.compile(r"<td>\s*</td>")
WATCH = ("not recorded", "unknown", "null", "self-reported", "unverified", "scheduled", "planned", "expected", "requested",
         "unless", "only if", "exactly when", "complete", "not", "no", "leave open", "rounded")
EDGES = {"len_state": (300, 500, 800, 1200, 2000), "len_ins": (2000, 3000, 4000, 5000), "len_card": (0, 500, 1000, 2000),
         "n_lines_state": (5, 10, 20, 40), "k_opts": (2, 4, 9, 19), "opt_len_mean": (10, 20, 30, 50), "opt_len_max": (15, 30, 50),
         "opt_len_min": (5, 10, 20), "q_n_numbers": (0, 1, 2, 3), "q_max_num_log": (1, 2, 3, 5, 8), "state_n_numbers": (5, 10, 20, 40),
         "state_max_num_log": (3, 5, 8), "n_rules_proxy": (2, 4, 6, 10)}


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binq(v, edges):
    for i, e in enumerate(edges):
        if v <= e:
            return i
    return len(edges)


def meta_set(r, s):
    cat, num = q.meta_feats(r, s)
    f = {f"m:{k}={v}" for k, v in cat.items()}
    for k, v in num.items():
        f.add(f"n:{k}~{binq(v, EDGES[k])}" if k in EDGES else f"n:{k}={v if v < 0 else int(v) if v < 50 else binq(v, (100, 300, 600, 1000, 1500, 2000))}")
    st = r["state"].lower()
    blank = bool(BLANK1.search(r["state"]) or BLANK2.search(st))
    f.add(f"txt:blank_cell={blank}")
    return f


def pb_test(ps, x):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, mu
    z = (abs(x - mu) - 0.5) / math.sqrt(var)
    return float(min(1.0, 2 * norm.sf(max(0.0, z)))), mu


def run_yn(rows, side):
    card = defaultdict(list)
    for r in rows:
        card[r["meta"]["card_id"]].append(int(r["gold"]))
    feats = defaultdict(list); y = [int(r["gold"]) for r in rows]; p_card = []
    for i, r in enumerate(rows):
        lab = card[r["meta"]["card_id"]]; n = len(lab) - 1
        p_card.append((sum(lab) - y[i]) / n if n > 0 else 0.5)
        for f in ngrams(q.full_text(r)) | meta_set(r, side.get(r["id"])):
            feats[f].append(i)
    tested = {f: ix for f, ix in feats.items() if N_MIN <= len(ix) <= len(rows) - N_MIN}
    out = []
    for f, ix in tested.items():
        n = len(ix); k = sum(y[i] for i in ix); x = max(k, n - k)
        p_raw = float(binom.sf(x - 1, n, 0.5)); pa, mu = pb_test([p_card[i] for i in ix], k)
        out.append({"feature": f, "n": n, "yes": k, "yes_rate": round(k / n, 4), "p_raw": p_raw, "p_card": pa,
                    "exp_yes_card": round(mu, 1), "n_cards": len({rows[i]["meta"]["card_id"] for i in ix})})
    return out, len(tested)


def opt_kinds(r):
    opts = r["options"]; st = r["state"]; stl = st.lower(); lens = [len(o) for o in opts]; kinds = [set() for _ in opts]
    ids = [re.findall(r"\b[A-Z]{1,4}-?\d{2,5}\b", o) for o in opts]
    cnt = [st.count(x[0]) if x else -1 for x in ids]; valid = [c for c in cnt if c >= 0]
    for i, o in enumerate(opts):
        if lens[i] == max(lens): kinds[i].add("kind:longest")
        if lens[i] == min(lens): kinds[i].add("kind:shortest")
        kinds[i].add("kind:" + KIND.get(o.strip(), "concrete"))
        if len(o) > 12 and o.lower() in stl: kinds[i].add("kind:verbatim_in_record")
        if cnt[i] >= 0 and len(set(valid)) > 1:
            if cnt[i] == max(valid): kinds[i].add("kind:id_most_mentioned")
            if cnt[i] == min(valid): kinds[i].add("kind:id_least_mentioned")
        if i == 0: kinds[i].add("kind:first")
        if i == len(opts) - 1: kinds[i].add("kind:last")
    return kinds


CROSS = ("kind:longest", "kind:shortest", "kind:nei", "kind:none", "kind:nothing", "kind:verbatim_in_record",
         "kind:id_most_mentioned", "kind:first", "kind:last")


def run_choice(rows, side):
    units = defaultdict(lambda: defaultdict(list))
    for ri, r in enumerate(rows):
        kinds = opt_kinds(r)
        mf = sorted(f for f in meta_set(r, side.get(r["id"])) if f.startswith(("m:sampler", "m:wording_id", "m:depth",
                    "m:sc_form", "m:sc_frame_id", "m:sc_card_variant", "m:sc_label_form", "m:sc_attack", "m:sc_kind",
                    "m:gk:", "m:gp:", "n:sc_n_gaps", "m:defs_style", "m:edge:")))
        for i, o in enumerate(r["options"]):
            g = int(o == r["gold"])
            fs = {"opt:" + t for t in ngrams(o)} | kinds[i]
            fs |= {m + "&" + kd for m in mf for kd in kinds[i] if kd in CROSS}
            for f in fs:
                units[f][ri].append(g)
    out = []; n_tested = 0
    for f, per in units.items():
        if len(per) < N_MIN: continue
        ps, x = [], 0
        for ri, gs in per.items():
            k = len(rows[ri]["options"]); m = len(gs)
            if m == k: continue
            ps.append(m / k); x += sum(gs)
        if len(ps) < N_MIN: continue
        n_tested += 1; p, mu = pb_test(ps, x)
        out.append({"feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(mu, 2), "p": p,
                    "n_cards": len({rows[ri]["meta"]["card_id"] for ri in per})})
    return out, n_tested


def main():
    rows, side = q.load(NAME)
    yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
    yres, n_y = run_yn(yn, side); cres, n_c = run_choice(ch, side)
    n_tests = n_y + n_c; thr = ALPHA / n_tests
    raw_fail = [o for o in yres if o["p_raw"] < thr]; card_fail = [o for o in yres if o["p_card"] < thr]
    ch_fail = [o for o in cres if o["p"] < thr]
    srt = lambda lst, key: sorted(lst, key=lambda o: o[key])[:40]
    watch = {w: next(({k: o[k] for k in ("n", "yes_rate", "p_raw", "p_card")} for o in yres if o["feature"] == w), None) for w in WATCH}
    res = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN, "n_tests": n_tests, "bonferroni_p": thr,
           "n_yes_no_rows": len(yn), "n_choice_rows": len(ch), "n_tested_yes_no": n_y, "n_tested_choice": n_c,
           "n_yes_no_card_adjusted_fails": len(card_fail), "n_yes_no_raw_fails": len(raw_fail),
           "yes_no_raw_fails_multi_card": len([o for o in raw_fail if o["n_cards"] > 1]), "n_choice_fails": len(ch_fail),
           "yes_no_card_adjusted_fails": srt(card_fail, "p_card"), "yes_no_raw_fails": srt(raw_fail, "p_raw"),
           "choice_fails_by_kind": dict(Counter(o["feature"].split("&")[-1] if "&" in o["feature"] else o["feature"].split(":")[0] for o in ch_fail)),
           "choice_fails": srt(ch_fail, "p"), "special_watch": watch,
           "top5_choice": srt(cres, "p")[:5], "top5_yes_no_card": srt(yres, "p_card")[:5]}
    res["pass"] = not card_fail and not ch_fail and res["yes_no_raw_fails_multi_card"] == 0
    json.dump(res, open(q.QC / f"g7_{NAME}.json", "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("n_tests", "bonferroni_p", "pass", "n_yes_no_card_adjusted_fails", "n_yes_no_raw_fails",
                                          "yes_no_raw_fails_multi_card", "n_choice_fails")}))


if __name__ == "__main__":
    main()
