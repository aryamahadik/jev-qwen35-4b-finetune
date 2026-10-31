"""G7 feature z-test (independent F4 checker). C_DATA_SPEC 8 G7 + F4 G0 8: one-sided binomial per unigram, bigram and
metadata feature, p0 = 1/k, alpha 0.01 Bonferroni over the tested features (n >= N_MIN occurrences).
- Yes/no rows: feature = presence of a lower-cased word unigram/bigram in the model-visible text (card + instructions +
  state), or a metadata value (F4 G0 8 list + visible generator tags; numbers binned). Test in the majority direction:
  p = P(Bin(n, .5) >= x). Card-adjusted variant (per-card yes rates are drawn 20-80% by design, spec 2.1 / F4 G0 8):
  null p_r = the row's card yes rate (leave-one-out), Poisson-binomial via normal approx + continuity, both directions.
- Choice rows: feature = a unigram/bigram inside an option text (+ its definition line), or an option kind (abstain,
  longest, shortest, negative claim, verbatim in record, entity most/least mentioned in record), or a row-metadata x
  option-kind cross. Unit = (row, option with f); success = option is gold; null = Poisson-binomial p = m_r / k_r.
- Audit-only (never pass-deciding, F4 G0 8): pivot / inference tags and the hidden twin-set tag.
Pass: no failing feature in the card-adjusted yes/no test and none in the choice test; raw yes/no failures are reported
with their card counts (a single-card feature carries that card's drawn yes rate). Usage: g7.py <name>"""
import json, math, re, sys
from collections import defaultdict, Counter
from scipy.stats import binom, norm
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
ALPHA = 0.01
N_MIN = 20
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
NEG = re.compile(r"\bnot\b|n't\b|\bno\b|\bnever\b")
HIDDEN = ("pivot", "inf", "twinset", "L")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binq(v, edges):
    for i, e in enumerate(edges):
        if v <= e:
            return i
    return len(edges)


def meta_set(r, sc, audit=False):
    m = r["meta"]; f = set()
    for k in ("sampler", "wording_id", "format_style", "defs_style", "domain_pack"):
        f.add(f"meta:{k}={m.get(k)}")
    f.add(f"meta:depth={m.get('depth')}")
    for e in m.get("edge", []):
        p = e.split(":")[0]
        if p in HIDDEN:
            if audit:
                f.add("audit:" + e)
            continue
        f.add("tag:" + e)
    for k in ("carrier", "inert", "label_form", "short", "inverted", "bait"):
        f.add(f"sc:{k}={sc.get(k)}")
    for k, edges in (("n_rules", (3, 4, 5, 6, 8)), ("n_ents", (2, 3, 4, 6, 10, 20)), ("n_stmts", (6, 8, 10, 13, 16, 20)),
                     ("len_tokens", (400, 600, 800, 1000, 1300, 1600))):
        f.add(f"sc:{k}~{binq(sc.get(k) or 0, edges)}")
    st = r["state"].lower()
    f.add(f"txt:n_unless~{min(3, st.count('unless') + st.count('except'))}")
    f.add(f"txt:n_numbers~{binq(len(L.nums(r['state'])), (0, 2, 4, 8))}")
    f.add(f"txt:has_source={'source' in st or 'reported that' in st}")
    f.add(f"txt:notrec={('not recorded' in st) or ('null' in st)}")
    return f


def pb_test(ps, x):
    """one-sided normal approx (continuity) in the observed direction for a Poisson-binomial count x with success probs
    ps (spec 8 G7: one-sided test; recheck:F4 removed the former two-sided doubling, which was laxer by a factor 2)."""
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, mu
    z = (abs(x - mu) - 0.5) / math.sqrt(var)
    return float(min(1.0, norm.sf(max(0.0, z)))), mu


def run_yn(rows, side):
    card = defaultdict(list)
    for r in rows:
        card[r["meta"]["card_id"]].append(int(r["gold"]))
    feats = defaultdict(list)  # f -> list of row index
    y = [int(r["gold"]) for r in rows]
    p_card = []
    for i, r in enumerate(rows):
        lab = card[r["meta"]["card_id"]]
        n = len(lab) - 1
        p_card.append((sum(lab) - y[i]) / n if n > 0 else 0.5)
        fs = ngrams((r.get("card") or "") + "\n" + r["instructions"] + "\n" + r["state"])
        fs |= meta_set(r, side[r["id"]], audit=True)
        for f in fs:
            feats[f].append(i)
    tested = {f: ix for f, ix in feats.items() if len(ix) >= N_MIN and len(ix) <= len(rows) - N_MIN}
    out = []
    for f, ix in tested.items():
        n = len(ix); k = sum(y[i] for i in ix); x = max(k, n - k)
        p_raw = float(binom.sf(x - 1, n, 0.5))
        pa, mu = pb_test([p_card[i] for i in ix], k)
        out.append({"feature": f, "n": n, "yes": k, "yes_rate": round(k / n, 4), "p_raw": p_raw, "p_card": pa,
                    "exp_yes_card": round(mu, 1), "n_cards": len({rows[i]["meta"]["card_id"] for i in ix})})
    return out, len(tested)


def opt_kinds(r, defs):
    opts = r["options"]; st = r["state"]; stl = st.lower(); k = len(opts)
    lens = [len(o) for o in opts]; kinds = [set() for _ in opts]
    ids = [re.findall(r"[A-Z]{2}[-/][A-Z0-9]{4,6}", o) for o in opts]
    cnt = [st.count(x[0]) if x else -1 for x in ids]
    valid = [c for c in cnt if c >= 0]
    for i, o in enumerate(opts):
        if lens[i] == max(lens): kinds[i].add("kind:longest")
        if lens[i] == min(lens): kinds[i].add("kind:shortest")
        if L.is_abstain(o): kinds[i].add("kind:abstain")
        if NEG.search(o.lower()): kinds[i].add("kind:neg")
        if len(o) > 12 and o.lower() in stl: kinds[i].add("kind:verbatim_in_record")
        if cnt[i] >= 0 and len(set(valid)) > 1:
            if cnt[i] == max(valid): kinds[i].add("kind:id_most_mentioned")
            if cnt[i] == min(valid): kinds[i].add("kind:id_least_mentioned")
        if o in defs: kinds[i].add("kind:has_def")
    return kinds


def run_choice(rows, side):
    d = L.dio()
    units = defaultdict(lambda: defaultdict(list))  # f -> row index -> [is_gold per option holding f]
    for ri, r in enumerate(rows):
        defs = d.card_defs(r.get("card")); kinds = opt_kinds(r, defs)
        mf = sorted(f for f in meta_set(r, side[r["id"]]) if not f.startswith("meta:domain_pack")
                    and not f.startswith("meta:format_style"))
        for i, o in enumerate(r["options"]):
            g = int(o == r["gold"])
            fs = {"opt:" + t for t in ngrams(o + " " + defs.get(o, ""))} | kinds[i]
            fs |= {m + "&" + kd for m in mf for kd in kinds[i] if kd in ("kind:longest", "kind:shortest", "kind:neg",
                                                                        "kind:abstain", "kind:verbatim_in_record",
                                                                        "kind:id_most_mentioned")}
            for f in fs:
                units[f][ri].append(g)
    out = []; n_tested = 0
    for f, per in units.items():
        n_rows = len(per)
        if n_rows < N_MIN:
            continue
        ps, x = [], 0
        for ri, gs in per.items():
            k = len(rows[ri]["options"]); m = len(gs)
            if m == k:
                continue  # every option holds f: carries no information
            ps.append(m / k); x += sum(gs)
        if len(ps) < N_MIN:
            continue
        n_tested += 1
        p, mu = pb_test(ps, x)
        out.append({"feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(mu, 2), "p": p,
                    "n_cards": len({rows[ri]["meta"]["card_id"] for ri in per})})
    return out, n_tested


def main():
    rows = L.load(NAME)
    side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
    yn = [r for r in rows if r["qtype"] == "noul"]; ch = [r for r in rows if r["qtype"] != "noul"]
    yres, n_y = run_yn(yn, side)
    cres, n_c = run_choice(ch, side)
    n_tests = n_y + n_c; thr = ALPHA / n_tests
    vis = lambda f: not f.startswith("audit:")
    raw_fail = [o for o in yres if o["p_raw"] < thr and vis(o["feature"])]
    card_fail = [o for o in yres if o["p_card"] < thr and vis(o["feature"])]
    ch_fail = [o for o in cres if o["p"] < thr]
    audit_fail = [o for o in yres if (o["p_raw"] < thr or o["p_card"] < thr) and not vis(o["feature"])]
    watch = ("unless", "except", "most", "some", "may be", "not", "only if", "rules out", "establish",
             "it is not the case", "complete", "not recorded", "null", "source", "yes", "no")
    watch_rep = {w: next(({k: o[k] for k in ("n", "yes_rate", "p_raw", "p_card")} for o in yres if o["feature"] == w), None)
                 for w in watch}
    srt = lambda lst, key: sorted(lst, key=lambda o: o[key])[:40]
    res = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN, "n_tests": n_tests,
           "bonferroni_p": thr, "n_yes_no_rows": len(yn), "n_choice_rows": len(ch), "n_tested_yes_no": n_y,
           "n_tested_choice": n_c,
           "yes_no_card_adjusted_fails": srt(card_fail, "p_card"),
           "yes_no_raw_fails": srt(raw_fail, "p_raw"),
           "yes_no_raw_fails_multi_card": len([o for o in raw_fail if o["n_cards"] > 1]),
           "n_choice_fails": len(ch_fail), "n_yes_no_card_adjusted_fails": len(card_fail), "n_yes_no_raw_fails": len(raw_fail),
           "choice_fails_by_option_kind": dict(Counter((o["feature"].split("&")[-1] if "&" in o["feature"] else o["feature"])
                                                       for o in ch_fail)),
           "choice_fails": srt(ch_fail, "p"),
           "audit_only_fails": [{k: o[k] for k in ("feature", "n", "yes_rate", "p_raw", "p_card")} for o in
                                sorted(audit_fail, key=lambda o: o["p_card"])[:20]],
           "special_watch": watch_rep,
           "top5_choice": srt(cres, "p")[:5], "top5_yes_no_card": srt(yres, "p_card")[:5]}
    res["pass"] = not card_fail and not ch_fail and res["yes_no_raw_fails_multi_card"] == 0
    json.dump(res, open(L.QC / f"g7_{NAME}.json", "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("n_tests", "bonferroni_p", "pass")}),
          "card_fail", len(card_fail), "raw_fail", len(raw_fail), "raw_multi", res["yes_no_raw_fails_multi_card"],
          "choice_fail", len(ch_fail), "audit_fail", len(audit_fail))


if __name__ == "__main__":
    main()
