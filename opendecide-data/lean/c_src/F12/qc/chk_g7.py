"""G7 feature z-test (independent F12 checker, check:F12, c-lanes-v3; adapted from the F9 checker's chk_g7.py).
C_DATA_SPEC 8 G7 + F12 G0 8: one-sided binomial per unigram, bigram and metadata feature, p0 = 1/k, alpha 0.01
Bonferroni over all tested features (n >= 20).
- Yes/no: feature = lower-cased word unigram/bigram present in the model-visible text (card + instructions + state) or a
  visible metadata value (chk_lib.meta_feats), plus F12 visible features (G0 8): the question's target tool T is the
  listed tool with the most word overlap with the request / first listed / last listed; a value stated without naming
  its param; stored result / records / proposed call / tool-result turn / correction / role line present; question
  token overlap with the text. Both directions: x = rows with the majority label, p = P(Bin(n, .5) >= x).
  Card-adjusted test (leave-one-out card yes rate, Poisson-binomial normal approx.) reported and gated.
- Choice: unit = (row, option set holding f); success = gold holds f; null p = m_r / k_r; Poisson-binomial normal
  approx. with continuity, both directions. Features: option-text n-grams, option kinds (abstain kinds, C-ACT fixed
  options, longest, shortest, in text, first / last in the text among the options, mentioned in the question, option =
  first listed tool, option has max token overlap with the request, param name present in the conversation), and
  meta x kind crosses (meta without format_style / wording_id / domain_pack).
Pass rule (as the F6 / F9 / F10 / F11 checkers): no choice failure, no card-adjusted yes/no failure, and no raw
(p0 = .5) yes/no failure spanning > 1 card. Usage: chk_g7.py <name>"""
import json, math, re, sys
from collections import defaultdict
from scipy.stats import binom, norm
import chk_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA, N_MIN = 0.01, 20
TOK = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")
WRD = re.compile(r"[a-z0-9]+")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binlog(v):
    return int(math.log2(1 + abs(v))) * (1 if v >= 0 else -1)


def meta_set(r, s):
    c, n = L.meta_feats(r, s)
    f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        f.add(f"meta:{k}={binlog(v) if k.startswith(('len_', 'n_lines', 'opt_len', 'state_max', 'q_max', 'sc_real', 'state_n')) else v}")
    return f


def request_text(s):
    S = (s or {}).get("S") or {}
    out = []
    for t in S.get("conv") or []:
        if t.get("who") == "user":
            for st in t.get("st") or []:
                if st.get("t") == "req" and st.get("_text"):
                    out.append(st["_text"])
    return out[-1] if out else ""


def tool_words(name):
    return {w for w in re.split(r"[_\W]+", name.lower()) if w and not w.isdigit()}


def catalog_order(r, s):
    """listed tool names in the order they first appear in the state (visible catalog order)."""
    S = (s or {}).get("S") or {}
    names = [t["name"] for t in S.get("tools") or []]
    pos = {n: L.first_pos(r["state"], n) for n in names}
    return [n for n in sorted(names, key=lambda n: pos[n]) if pos[n] >= 0]


def overlap_max(r, s):
    """listed tools with the most word overlap with the latest request (ties all kept)."""
    req = set(WRD.findall(request_text(s).lower()))
    cat = catalog_order(r, s)
    if not cat or not req:
        return set()
    sc = {n: len(tool_words(n) & req) for n in cat}
    m = max(sc.values())
    return {n for n, v in sc.items() if v == m} if m > 0 else set()


def conv_params(s):
    S = (s or {}).get("S") or {}
    return {st.get("p") for t in S.get("conv") or [] for st in t.get("st") or [] if st.get("p")}


def vis_feats(r, s, qfreq):
    v = L.views(r, s); f = set(); S = (s or {}).get("S") or {}
    if r.get("role") == "attacked":
        f.add("f12:attack_row")
    qt = ((s or {}).get("q") or {}).get("tool")
    cat = catalog_order(r, s)
    if qt:
        om = overlap_max(r, s)
        f.add(f"f12:qtool_max_overlap={qt in om}")
        if cat:
            f.add(f"f12:qtool_first_listed={cat[0] == qt}"); f.add(f"f12:qtool_last_listed={cat[-1] == qt}")
    conv = S.get("conv") or []
    sts = [st for t in conv for st in t.get("st") or []]
    f.add(f"f12:unnamed_value={any(st.get('t') == 'val' and not st.get('p') for st in sts)}")
    f.add(f"f12:stored={bool(S.get('stored'))}"); f.add(f"f12:records={min(len(S.get('records') or []), 3)}")
    f.add(f"f12:call_shown={S.get('call') is not None}"); f.add(f"f12:tool_turn={any(t.get('who') == 'tool' for t in conv)}")
    f.add(f"f12:correction={any(st.get('t') == 'corr' for st in sts)}"); f.add(f"f12:role_line={S.get('role') is not None}")
    f.add(f"f12:n_user_turns={min(sum(t.get('who') == 'user' for t in conv), 4)}")
    qtk = {t for t in TOK.findall(v["q"].lower()) if len(t) >= 3 and qfreq.get(t, 0) < 0.3}
    sl = r["state"].lower(); cnt = [len(re.findall(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", sl)) for t in qtk]
    f.add(f"f12:q_overlap_n={min(sum(c > 0 for c in cnt), 6)}")
    f.add(f"f12:q_overlap_max={binlog(max(cnt) if cnt else 0)}")
    return f


def opt_tool(o, names):
    if o in names:
        return o
    for pre in ("Call ",):
        if o.startswith(pre) and o[len(pre):] in names:
            return o[len(pre):]
    for n in names:  # masked / swapped C-ACT call options: "<label> <T>"
        if o.endswith(" " + n):
            return n
    return None


def opt_param(o, params):
    for pre in ("Ask for ",):
        if o.startswith(pre):
            return o[len(pre):]
    m = re.search(r" on ([a-z0-9_]+)(?: and ([a-z0-9_]+))?$", o)
    if m:
        return m.group(1)
    return o if o in params else None


def opt_kinds(r, s=None):
    opts = r["options"]; ls = [len(o) for o in opts]; st = r["state"]; out = []
    q = L.qtext(r, s).lower()
    pos = [L.first_pos(st, o) for o in opts]; ok = sorted(p for p in pos if p >= 0)
    S = (s or {}).get("S") or {}
    names = {t["name"] for t in S.get("tools") or []}
    allp = {p["name"] for t in S.get("tools") or [] for p in t.get("params") or []}
    cat = catalog_order(r, s); om = overlap_max(r, s); cp = conv_params(s)
    for i, o in enumerate(opts):
        k = set()
        ak = L.abstain_kind(o)
        if ak:
            k.add("kind:abstain"); k.add("kind:abstain_" + ak)
        if o in L.ACT_FIXED:
            k.add("kind:" + L.ACT_FIXED[o])
        if ls[i] == max(ls): k.add("kind:longest")
        if ls[i] == min(ls): k.add("kind:shortest")
        if pos[i] >= 0:
            k.add("kind:in_text")
            if len(ok) >= 2:
                if pos[i] == ok[0]: k.add("kind:first_in_text")
                if pos[i] == ok[-1]: k.add("kind:last_in_text")
        if len(o) >= 3 and o.lower() in q: k.add("kind:in_question")
        t = opt_tool(o, names)
        if t:
            k.add("kind:tool_option")
            if cat and t == cat[0]: k.add("kind:first_listed_tool")
            if cat and t == cat[-1]: k.add("kind:last_listed_tool")
            if t in om: k.add("kind:max_overlap_tool")
        p = opt_param(o, allp)
        if p:
            k.add("kind:param_option")
            if p in cp: k.add("kind:param_named_in_conv")
        out.append(k)
    return out


def pb(x, ps):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, 1.0
    return float(norm.sf((x - 0.5 - mu) / math.sqrt(var))), float(norm.sf((mu - x - 0.5) / math.sqrt(var)))


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
    kinds = {f: {"n_rows": len(v[1]), "gold_hits": v[0], "expected": round(sum(v[1]), 2)} for f, v in sorted(tested_ch.items())
             if f.startswith("kind:")}
    f12y = {f: {"n": v[0], "yes_rate": round(v[1] / v[0], 4)} for f, v in sorted(tested_yn.items()) if f.startswith("f12:")}
    ok = not chf and not adj and not ynm
    out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "pool_sha256": L.sha(L.OUT / f"{NAME}.jsonl"), "alpha": ALPHA,
           "n_min": N_MIN, "n_tests": n_tests, "bonferroni_p": bar,
           "n_yes_no_rows": len(yn), "n_choice_rows": len(ch), "n_tested_yes_no": len(tested_yn), "n_tested_choice": len(tested_ch),
           "n_fail_choice": len(chf), "n_fail_yes_no_raw": len(ynr), "n_fail_yes_no_raw_multi_card": len(ynm),
           "n_fail_yes_no_card_adjusted": len(adj), "near_within_100x": near,
           "diag_gold_stored_first": {"rows": D[2], "gold_first": D[0], "expected": round(D[1], 1),
                                      "note": "stored option order; the trainer re-shuffles; judged in G10"},
           "pass_rule": "no choice failure, no card-adjusted yes/no failure, no raw yes/no failure spanning > 1 card",
           "kind_features": kinds, "f12_yes_no_features": f12y,
           "fails_choice": chf[:60], "fails_yes_no_raw_multi_card": ynm[:60], "fails_yes_no_raw_single_card": len(ynr) - len(ynm),
           "card_adjusted_fails": adj[:60], "pass": ok}
    (L.QC / f"g7_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("n_tests", "n_fail_choice", "n_fail_yes_no_raw", "n_fail_yes_no_raw_multi_card",
                                          "n_fail_yes_no_card_adjusted", "near_within_100x", "pass")}))


if __name__ == "__main__":
    main()
