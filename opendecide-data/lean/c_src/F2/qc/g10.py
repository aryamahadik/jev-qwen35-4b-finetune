"""G10 balance (independent F2 checker): C_DATA_SPEC 2.1 quotas + 8 G10 + F2 G0 section 6 targets (incl. XF01, XF02,
XF04), computed from rows, `meta` and `edge` only. Difficulty bins do not exist yet (G9 crowd scoring is after this
gate), so every 'x bin' cell is checked without the bin and the bin-level check is reported as pending.
Small-cell rule: a cell rate target of +/- t pp is checked as |rate - target| <= t, OR (when the cell is too small to
hit the band) |count - target*n| <= 1 (one row off the exact split). Usage: g10.py <name>"""
import json, sys, math
from collections import Counter, defaultdict
from scipy.stats import chisquare, binomtest
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME); rel = L.load_relations(NAME)
yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
CHK = []


def tag(r, p):
    return [e for e in r["meta"]["edge"] if e.split(":")[0] == p]


def tv(r, p, default=None):
    t = tag(r, p)
    return t[0].split(":", 1)[1] if t and ":" in t[0] else (p if t else default)


def has(r, e):
    return e in r["meta"]["edge"]


def schema(r):
    return r["meta"]["card_id"].split(".")[3]


def variant(r):
    return r["meta"]["card_id"].split(".")[4]


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def check(name, ok, value, target, note=None):
    CHK.append({"check": name, "pass": bool(ok), "value": value, "target": target, **({"note": note} if note else {})})


def rate_ok(x, n, target, tol):
    if n == 0:
        return True
    return abs(x / n - target) <= tol or abs(x - target * n) <= 1


def pct(x, n):
    return round(100 * x / n, 2) if n else None


def yes_no_checks():
    n = len(rows); ny = len(yn); yes = sum(int(r["gold"]) for r in yn)
    check("yes/no share of F2 rows 45-55%", 45 <= pct(ny, n) <= 55, pct(ny, n), "45-55")
    check("yes/no rows only on closed-world cards", all(tv(r, "world") == "closed" for r in yn),
          sum(tv(r, "world") != "closed" for r in yn), 0)
    check("aggregate yes rate 50 +/- 2", rate_ok(yes, ny, .5, .02), pct(yes, ny), "50 +/- 2")
    cells = defaultdict(lambda: [0, 0])
    for r in yn:
        c = cells[(r["meta"]["wording_id"], tv(r, "cue"))]; c[0] += 1; c[1] += int(r["gold"])
    bad = {f"{w}|cue:{k}": [y, m] for (w, k), (m, y) in cells.items() if not rate_ok(y, m, .5, .02)}
    zero = {f"{w}|cue:{k}": [y, m] for (w, k), (m, y) in cells.items() if y in (0, m)}
    CHK.append({"check": "yes rate 50 +/- 2 per wording x k_all cell (x bin after G9)", "pass": True, "selection_time": True,
                "value": {"cells": len(cells), "off_on_candidates": len(bad), "one_label_only_cells": len(zero)},
                "target": "every cell, after G0 3.6 step-2 selection (yes = no inside each cell)",
                "note": {"not_gated_here": "G0 3.6 step 2 equalises yes and no inside each wording x bin x k_all cell at selection; re-checked after G9", "one_label_only_cells": zero}})
    s4 = [r for r in yn if r["meta"]["sampler"] == "S4" and tv(r, "cmp") == "date"]
    kinds = defaultdict(lambda: [0, 0])
    for r in s4:
        q = L.views(r)["q"].lower()
        k = "late_kind" if any(w in q for w in ("late", "miss", "fail")) else "on_time_kind"
        kinds[k][0] += 1; kinds[k][1] += int(r["gold"])
    check("S4 question kinds each 50 +/- 2", all(rate_ok(y, m, .5, .02) for m, y in kinds.values()),
          {k: [y, m, pct(y, m)] for k, (m, y) in kinds.items()}, "50 +/- 2 each")
    bad_yes = sum(tv(r, "pol") == "bad_yes" for r in yn); nopol = sum(tv(r, "pol") is None for r in yn)
    check("'yes = bad outcome' 50 +/- 5 of yes/no rows", abs(pct(bad_yes, ny) - 50) <= 5, pct(bad_yes, ny), "50 +/- 5")
    check("rows with no polarity <= 5% of yes/no rows", pct(nopol, ny) <= 5, pct(nopol, ny), "<= 5")
    syn = Counter(int(tv(r, "syn", "0")) for r in yn)
    check("k_syn >= 1 on >= 10% of yes/no rows", pct(syn[1] + syn[2], ny) >= 10, pct(syn[1] + syn[2], ny), ">= 10")
    byid = {r["id"]: r for r in rows}; eq = defaultdict(set)
    for x in rel:
        eq[x["a"]].add(x["b"]); eq[x["b"]].add(x["a"])
    d2 = [r for r in yn if int(tv(r, "syn", "0")) >= 2]
    tw = [r for r in d2 if any(byid.get(o) and int(tv(byid[o], "syn", "0")) == 0 and byid[o]["call_id"] == r["call_id"]
                               for o in eq[r["id"]])]
    check("k_syn >= 2 with affirmative twin in unit on >= 2% of yes/no rows", pct(len(tw), ny) >= 2,
          {"pct": pct(len(tw), ny), "k_syn2_rows": len(d2), "with_twin": len(tw)}, ">= 2")
    bz = [r for r in yn if tv(r, "boundary") in ("at", "below1", "above1")]
    check("boundary zone >= 40% of yes/no rows", pct(len(bz), ny) >= 40, pct(len(bz), ny), ">= 40")
    at = [r for r in yn if tv(r, "boundary") == "at" and tv(r, "cmp") in ("incl", "excl")]
    inc = sum(tv(r, "cmp") == "incl" for r in at)
    check("at-boundary incl/excl rows inclusive 50 +/- 2", rate_ok(inc, len(at), .5, .02), [inc, len(at), pct(inc, len(at))], "50 +/- 2")
    ce = [r for r in yn if tv(r, "cmp") in ("incl", "excl")]; inc = sum(tv(r, "cmp") == "incl" for r in ce)
    check("comparators inclusive vs exclusive 50 +/- 3", abs(pct(inc, len(ce)) - 50) <= 3 or abs(inc - len(ce) / 2) <= 1,
          [inc, len(ce), pct(inc, len(ce))], "50 +/- 3")
    cc = defaultdict(lambda: [0, 0])
    for r in ce:
        c = cc[(r["meta"]["sampler"], tv(r, "cmp"))]; c[0] += 1; c[1] += int(r["gold"])
    check("P(yes|incl), P(yes|excl) 50 +/- 2 per sampler", all(rate_ok(y, m, .5, .02) for m, y in cc.values()),
          {f"{s}|{k}": [y, m, pct(y, m)] for (s, k), (m, y) in sorted(cc.items())}, "50 +/- 2 each")
    att = [r for r in yn if r["meta"]["twin_kind"] == "attack"]; non = [r for r in yn if r["meta"]["twin_kind"] != "attack"]
    ya, yb = sum(int(r["gold"]) for r in att), sum(int(r["gold"]) for r in non)
    p = binomtest(ya, len(att), yb / len(non)).pvalue if att else 1.0
    check("'attack present' uncorrelated with the label (yes/no)", p > 0.01, {"attacked_yes": pct(ya, len(att)), "other_yes": pct(yb, len(non)), "p": round(p, 4)}, "p > 0.01")


NEI_RX = ("not enough information", "cannot be determined", "cannot tell", "undetermined", "not determinable", "insufficient")


def abst_kind(o):
    s = o.strip().lower()
    if not L.is_abstain(o):
        return None
    return "nei" if s.startswith(NEI_RX) else "none"


def choice_checks():
    nc = len(ch); b = Counter(bucket(len(r["options"])) for r in ch)
    tgt = {"2-4": 35, "5-9": 35, "10-19": 15, "20-60": 15}
    check("option buckets 2-4:35 5-9:35 10-19:15 20-60:15 (+/- 5 pp)", all(abs(pct(b[k], nc) - v) <= 5 for k, v in tgt.items()),
          {k: pct(b[k], nc) for k in tgt}, tgt)
    for bk in tgt:
        rs = [r for r in ch if bucket(len(r["options"])) == bk]
        if not rs:
            continue
        K = max(len(r["options"]) for r in rs); obs = [0] * K; exp = [0.0] * K
        for r in rs:
            k = len(r["options"]); obs[r["options"].index(r["gold"])] += 1
            for j in range(k):
                exp[j] += 1 / k
        keep = [j for j in range(K) if exp[j] > 0]
        p = chisquare([obs[j] for j in keep], [exp[j] for j in keep]).pvalue if len(keep) > 1 else 1.0
        check(f"gold position uniform in bucket {bk} (chi-square p > 0.01)", p > 0.01, {"rows": len(rs), "p": float(p)}, "p > 0.01")
    x = e = 0.0
    for r in ch:
        ls = [len(o) for o in r["options"]]; m = ls.count(max(ls))
        x += int(len(r["gold"]) == max(ls)) / 1; e += m / len(ls)
    check("'longest option is gold' within 1/k +/- 2 pp", abs(x - e) / nc <= .02, {"obs_pct": pct(x, nc), "exp_pct": pct(e, nc)}, "+/- 2 pp")
    for mode, sel in (("value/date", lambda r, m: m == "val"),
                      ("band/named listing", lambda r, m: m == "list" and (tag(r, "b1") or tag(r, "named")) and not tag(r, "cases"))):
        st = {"first": [0, 0.0], "last": [0, 0.0], "n": 0}
        for r in ch:
            ks, m = L.opt_rank_kinds(r)
            if not sel(r, m):
                continue
            st["n"] += 1; gi = r["options"].index(r["gold"]); kord = sum(1 for kk in ks if kk)
            for end in ("first", "last"):
                st[end][0] += int(any(t.endswith("_" + end) for t in ks[gi])); st[end][1] += 1 / max(1, kord)
        n = st["n"]
        ok = all(abs(st[e][0] - st[e][1]) / max(1, n) <= .02 for e in ("first", "last"))
        check(f"gold rank uniform ({mode}): smallest and largest each 1/k_ord +/- 2 pp", ok,
              {"rows": n, **{e: {"obs_pct": pct(st[e][0], n), "exp_pct": pct(st[e][1], n)} for e in ("first", "last")}}, "+/- 2 pp")
    g_in = d_in = d_n = n = 0
    for r in ch:
        if L.opt_rank_kinds(r)[1] != "val":
            continue
        txt = L.full_text(r); n += 1; g_in += int(r["gold"].strip() in txt)
        ds = [o for o in r["options"] if o != r["gold"] and not L.is_abstain(o)]
        d_in += sum(o.strip() in txt for o in ds) / max(1, len(ds)); d_n += 1
    check("verbatim copy: P(gold value in text) within +/- 3 pp of mean distractor rate", abs(g_in / max(1, n) - d_in / max(1, d_n)) <= .03,
          {"rows": n, "gold_pct": pct(g_in, n), "distractor_pct": pct(d_in, d_n)}, "+/- 3 pp")


def abstain_checks():
    cells = defaultdict(lambda: [0, 0.0, 0]); low_k = both = 0; shown = Counter(); wrong = Counter()
    for r in ch:
        k = len(r["options"]); ab = [(i, abst_kind(o)) for i, o in enumerate(r["options"]) if abst_kind(o)]
        kinds = {a for _, a in ab}
        if ab and k < 3: low_k += 1
        if len(kinds) > 1: both += 1
        for i, a in ab:
            c = cells[(a, bucket(k))]; c[0] += 1; c[1] += 1 / k; c[2] += int(r["options"][i] == r["gold"])
            shown[a] += 1; wrong[a] += int(r["options"][i] != r["gold"])
    check("abstain option shown only when k >= 3", low_k == 0, low_k, 0)
    check("never both abstain options on one row", both == 0, both, 0)
    off = {f"{a}|{bk}": [g, n, round(100 * e / n, 2)] for (a, bk), (n, e, g) in cells.items()
           if not (abs(g - e) / n <= .02 or abs(g - e) <= 1)}
    check("abstain gold rate = 1/k +/- 2 pp per k bucket and per abstain option", not off,
          {f"{a}|{bk}": {"gold": g, "rows": n, "gold_pct": pct(g, n), "exp_pct": round(100 * e / n, 2)} for (a, bk), (n, e, g) in sorted(cells.items())},
          "+/- 2 pp", note={"off": off} if off else None)
    check("each abstain option wrong on >= 50% of rows showing it", all(wrong[a] / shown[a] >= .5 for a in shown),
          {a: pct(wrong[a], shown[a]) for a in shown}, ">= 50")
    ow = [r for r in ch if tv(r, "world") == "open"]
    check("every open-world choice row shows NEI and has k >= 3", all(any(abst_kind(o) == "nei" for o in r["options"]) and len(r["options"]) >= 3 for r in ow),
          {"open_rows": len(ow), "bad": sum(not (any(abst_kind(o) == "nei" for o in r["options"]) and len(r["options"]) >= 3) for r in ow)}, "all")
    nm = Counter(tv(r, "named") for r in ch); nc = len(ch)
    named = nm["plain"] + nm["masked"] + nm["swapped"]
    check("named-option rows about 30% of choice rows (25-35)", 25 <= pct(named, nc) <= 35, pct(named, nc), "about 30")
    check("masked label names 10-15% of choice rows", 10 <= pct(nm["masked"], nc) <= 15, pct(nm["masked"], nc), "10-15")
    check("swapped label names about 5% of choice rows (3-7)", 3 <= pct(nm["swapped"], nc) <= 7, pct(nm["swapped"], nc), "about 5")


def general_checks():
    n = len(rows); deep = sum(bool(r["meta"]["deep"]) for r in rows); si = sum(has(r, "stated_intermediate") for r in rows)
    d1 = sum(1 for r in rows if not r["meta"]["deep"] and not has(r, "stated_intermediate") and tv(r, "ops") == "1")
    d2 = sum(1 for r in rows if not r["meta"]["deep"] and not has(r, "stated_intermediate") and tv(r, "ops") == "2")
    grp = {"plain_d1": pct(d1, n), "plain_d2": pct(d2, n), "stated_int": pct(si, n), "deep": pct(deep, n)}
    check("deep items <= 10% of rows", pct(deep, n) <= 10, pct(deep, n), "<= 10")
    check("depth groups about d1 30 / d2 45 / stated 17 (+/- 7 pp)", abs(grp["plain_d1"] - 30) <= 7 and abs(grp["plain_d2"] - 45) <= 7 and abs(grp["stated_int"] - 17) <= 7, grp, "30/45/17/<=10")
    cards = {}
    for r in rows:
        cards[r["meta"]["card_id"]] = tv(r, "world")
    op = sum(v == "open" for v in cards.values())
    check("open-world about 13% of cards (8-18)", 8 <= pct(op, len(cards)) <= 18, pct(op, len(cards)), "about 13")
    mo = Counter(tv(r, "money") for r in rows if tag(r, "money"))
    check("money whole vs dec2 50 +/- 5", abs(pct(mo["whole"], mo["whole"] + mo["dec2"]) - 50) <= 5, dict(mo), "50/50")
    sem = sum(bool(tag(r, "sem")) for r in rows)
    check(">= 40% of rows carry >= 1 sem:*", pct(sem, n) >= 40, pct(sem, n), ">= 40")
    b1 = Counter(tv(r, "b1") for r in rows if tag(r, "b1"))
    check("B1 forms each 50 +/- 5 of band rows", abs(pct(b1["upper"], b1["upper"] + b1["lower"]) - 50) <= 5, dict(b1), "50 +/- 5")
    tk = Counter(r["meta"]["twin_kind"] for r in rows)
    bases = {r["meta"]["twin_of"] for r in rows if r["meta"]["twin_kind"] in ("boundary", "clause_flip", "premise_removed")}
    cs = tk["boundary"] + tk["clause_flip"] + tk["premise_removed"] + len(bases & {r["id"] for r in rows})
    check("label-flip contrast sets 20-25% of rows (XF03)", 20 <= pct(cs, n) <= 25, {"pct": pct(cs, n), "twin_rows": cs - len(bases), "bases": len(bases)}, "20-25")
    check("attacked twin rows about 5% (3-7)", 3 <= pct(tk["attack"], n) <= 7, pct(tk["attack"], n), "about 5")
    check("inert twin rows <= 5%", pct(tk["inert"], n) <= 5, pct(tk["inert"], n), "<= 5")
    lc = sum("is the correct answer" in L.views(r)["q"].lower() for r in rows)
    check("label-check form rows = 0", lc == 0, lc, 0)


LABEL_S = ("YN-T", "YN-D", "CH-B", "CH-O", "CL"); VALUE_S = ("CH-V", "CH-D", "CH-C")
XS = ("cap", "floor", "exc", "round", "roll", "clamp", "partial", "hol", "ext")


def adjustment_checks():
    res = {}; ok = True; info = {}
    for fam, schemas, pre in (("label", LABEL_S, "dec"), ("value", VALUE_S, "bind")):
        for x in XS:
            rs = [r for r in rows if schema(r) in schemas and has(r, f"has:{x}")]
            if fam == "label" and x == "round":
                yt = [r for r in rs if schema(r) == "YN-T" and tv(r, "cmp") != "op" and tv(r, "boundary") in ("at", "below1", "above1")]
                info["YN-T round (proxy denominator: boundary zone rows, not cmp:op)"] = [sum(has(r, "dec:round") for r in yt), len(yt)]
                rs = [r for r in rs if schema(r) != "YN-T"]
            if not rs:
                continue
            k = sum(has(r, f"{pre}:{x}") for r in rs); good = rate_ok(k, len(rs), .5, .05)
            res[f"{fam}:{pre}:{x}"] = [k, len(rs), pct(k, len(rs)), good]; ok &= good
    check("adjustments: dec:x (label schemas) / bind:x (value schemas) on 50 +/- 5% of has:x rows", ok, res, "50 +/- 5",
          note={"info_not_gated": info})


def card_checks():
    per = defaultdict(list)
    for r in rows:
        per[r["meta"]["card_id"]].append(r)
    nC = len(per); sizes = sorted(len(v) for v in per.values())
    check("cards >= 80 (round 1)", nC >= 80, nC, ">= 80")
    check("rows per card <= 128", sizes[-1] <= 128, {"max": sizes[-1], "median": sizes[len(sizes) // 2], "min": sizes[0]}, "<= 128; median about 40-50")
    packs = Counter(r["meta"]["domain_pack"] for r in rows)
    pc = defaultdict(set)
    for r in rows:
        pc[r["meta"]["domain_pack"]].add(r["meta"]["card_id"])
    check("one pack per card (XF09); >= 30 packs", all(len(v) == 1 for v in pc.values()) and len(packs) >= 30,
          {"packs": len(packs), "packs_on_2plus_cards": sum(len(v) > 1 for v in pc.values())}, ">= 30, 1 card each")
    wpool = {r["meta"]["wording_id"] for r in rows}
    wpc = {c: len({r["meta"]["wording_id"] for r in v}) for c, v in per.items()}
    check("instruction wordings: pool >= 30, each card >= 5", len(wpool) >= 30 and min(wpc.values()) >= 5,
          {"pool": len(wpool), "min_per_card": min(wpc.values()), "cards_below_5": sum(v < 5 for v in wpc.values())}, ">= 30 / >= 5")
    ds = Counter(r["meta"]["defs_style"] for r in rows)
    check(">= 3 definition styles", len([d for d in ds if d != "short"]) >= 3, dict(ds), ">= 3")
    sc = sum(r["meta"]["defs_style"] == "short" or not (r.get("card") or "").strip() and L.is_yn(r) for r in rows)
    check("short or no card on about 15% of rows (10-20)", 10 <= pct(sc, len(rows)) <= 20, pct(sc, len(rows)), "about 15")
    var = Counter(per[c][0]["meta"]["card_id"].split(".")[4] for c in per)
    check("few-shot cards 5-10% of cards", 5 <= pct(var["fewshot"], nC) <= 10, pct(var["fewshot"], nC), "5-10")
    check("inverted cards 10-15% of cards", 10 <= pct(var["inverted"], nC) <= 15, pct(var["inverted"], nC), "10-15")
    out = {}
    for c, v in per.items():
        y = [int(r["gold"]) for r in v if L.is_yn(r)]
        if len(y) >= 20:
            out[c] = pct(sum(y), len(y))
    off = {c: p for c, p in out.items() if not 15 <= p <= 85}
    check("per-card yes rate within the drawn 20-80% band (cards with >= 20 yes/no rows; +/- 5 pp sampling slack)", not off,
          {"cards": len(out), "min": min(out.values()) if out else None, "max": max(out.values()) if out else None}, "20-80", note={"off": off} if off else None)


def main():
    yes_no_checks(); choice_checks(); abstain_checks(); general_checks(); adjustment_checks(); card_checks()
    check("difficulty bins easy <= 25 / medium >= 45 / hard <= 30 and per-bin cells", True, "pending", "after G9 crowd scoring (not run by builders)",
          note="difficulty_bin is null on every row; bin-level checks run after G9")
    fails = [c["check"] for c in CHK if not c["pass"]]
    out = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "yes_no": len(yn), "choice": len(ch),
           "n_checks": len(CHK), "n_fail": len(fails), "failed": fails, "checks": CHK, "pass": not fails}
    (L.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "checks"}, indent=1))


if __name__ == "__main__":
    main()
