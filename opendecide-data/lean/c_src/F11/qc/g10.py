"""G10 balance (independent F11 checker, check:F11, c-lanes-v3). C_DATA_SPEC 8 G10 (v4) + F11 G0 9, from rows, meta and
relations only (visible text + meta; no generator internals). Difficulty bins are unscored (G9 crowd not run), so every
'x bin' cell is checked without the bin. F11 G0 9 (A39) checks every target on post-selection rows, so a pool-level
miss of a per-cell +/- 2 pp target is reported as selection-time when the cell is balanceable by 2.1's within-cell
downsampling; the gated pool-level checks are listed in GATED below.
GATED (v4): family yes rate 50 +/- 2; no wording x k_all cell whose yes rate differs from 50% at binomial p < 0.01
  Bonferroni (selection cannot fix a cell that is far off without heavy loss); gold letter uniform per option bucket
  (chi-square p > 0.01); longest option is gold within +/- 2 pp of 1/k (ties split; inverted rows read on the report
  blocks); abstain options wrong on >= 50% of rows that show them; attack present uncorrelated with the label
  (chi-square p > 0.01 on yes/no; choice attack twins keep the gold by construction, checked).
REPORTED (F11 G0 9): yes/no share per sampler; per-cell +/- 2 pp misses; marked-asked yes rates; negation shares; short
  card, masked, swapped shares; gold position in the card list (decile chi-square); None-option gold rate per bucket.
Small-cell rule for +/- t targets: met when |rate - target| <= t or |count - target * n| <= 1. Usage: g10.py <name>"""
import json, sys, re
from collections import Counter, defaultdict
from scipy.stats import chisquare, binomtest, chi2_contingency
import chk_lib as L
import f11_feats as X
sys.path.insert(0, str(L.LEAN / "c_src/common"))
import negcount  # noqa: E402

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME); rel = L.load_relations(NAME); byid = {r["id"]: r for r in rows}
yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
CHK = []


def check(name, ok, value, target, gated=True):
    CHK.append({"check": name, "gated": gated, "pass": bool(ok) if gated else True, "raw_ok": bool(ok), "value": value,
                "target": target})


def rate_ok(x, n, t, tol):
    return n == 0 or abs(x / n - t) <= tol or abs(x - t * n) <= 1


neg = {r["id"]: negcount.count(L.views(r)["qsent"]) for r in yn}
ny = sum(int(r["gold"]) for r in yn)
check("family yes rate 50 +/- 2", rate_ok(ny, len(yn), .5, .02), {"yes": ny, "n": len(yn), "rate": round(ny / len(yn), 4)},
      "0.48-0.52")
cells = defaultdict(lambda: [0, 0])
for r in yn:
    c = cells[(r["meta"]["wording_id"], neg[r["id"]].k_all)]; c[0] += 1; c[1] += int(r["gold"])
bar = 0.01 / max(1, len(cells))
far = {f"{w}|k{k}": [y, n] for (w, k), (n, y) in cells.items() if n and binomtest(y, n, .5).pvalue < bar}
off = {f"{w}|k{k}": [y, n] for (w, k), (n, y) in cells.items() if not rate_ok(y, n, .5, .02)}
check("wording x k_all cells: none far from 50% (binomial p < 0.01 Bonferroni)", not far,
      {"cells": len(cells), "far": far}, "0 far cells")
check("[selection-time] wording x k_all yes rate 50 +/- 2 (x bin after G9)", not off,
      {"cells": len(cells), "off": len(off), "examples": dict(list(off.items())[:12])}, "every cell", gated=False)
# gold letter uniform per option bucket (canonical order; expected count per position from each row's 1/k)
for bk in ("2-4", "5-9", "10-19", "20-60"):
    rs = [r for r in ch if L.bucket(len(r["options"])) == bk]
    if not rs:
        continue
    obs, exp = Counter(), Counter()
    for r in rs:
        k = len(r["options"]); g = L.gold_index(r)
        if bk in ("2-4", "5-9"):
            obs[g] += 1
            for i in range(k):
                exp[i] += 1 / k
        else:  # decile of the position
            obs[min(9, g * 10 // k)] += 1
            for i in range(k):
                exp[min(9, i * 10 // k)] += 1 / k
    keys = sorted(exp); o = [obs[i] for i in keys]; e = [exp[i] for i in keys]
    s = sum(o) / sum(e); e = [x * s for x in e]
    p = float(chisquare(o, e).pvalue) if len(keys) > 1 else 1.0
    check(f"gold letter uniform, bucket {bk} (chi-square p > 0.01)", p > 0.01,
          {"n": len(rs), "p": round(p, 4), "obs": o, "exp": [round(x, 1) for x in e]}, "p > 0.01")


def blocks(r):
    st = r["state"]; pos = sorted((st.find(o), i) for i, o in enumerate(r["options"]) if st.find(o) >= 0)
    out = [0] * len(r["options"])
    for j, (p, i) in enumerate(pos):
        end = pos[j + 1][0] if j + 1 < len(pos) else len(st)
        out[i] = end - p
    return out


lg, ex1k, per = 0.0, 0.0, defaultdict(lambda: [0.0, 0.0, 0])
for r in ch:
    lens = blocks(r) if r["meta"].get("subtype") == "inverted" else [len(o) for o in r["options"]]
    m = max(lens); tied = [i for i, x in enumerate(lens) if x == m]; g = L.gold_index(r); k = len(lens)
    hit = (1 / len(tied)) if g in tied else 0.0
    lg += hit; ex1k += 1 / k; b = per[L.bucket(k)]; b[0] += hit; b[1] += 1 / k; b[2] += 1
d = (lg - ex1k) / len(ch)
check("longest option is gold within +/- 2 pp of 1/k", abs(d) <= .02,
      {"rate": round(lg / len(ch), 4), "mean_1_over_k": round(ex1k / len(ch), 4), "diff_pp": round(100 * d, 2),
       "per_bucket": {k: [round(v[0] / v[2], 4), round(v[1] / v[2], 4), v[2]] for k, v in sorted(per.items())}},
      "|diff| <= 2 pp")
ab = defaultdict(lambda: [0, 0, 0.0])
for r in ch:
    a = [i for i, o in enumerate(r["options"]) if L.is_abstain(o)]
    if a:
        c = ab[L.bucket(len(r["options"]))]; c[0] += 1; c[1] += int(L.gold_index(r) in a); c[2] += 1 / len(r["options"])
tot = [sum(v[0] for v in ab.values()), sum(v[1] for v in ab.values())]
check("abstain (None) options wrong on >= 50% of rows that show them", tot[0] == 0 or tot[1] / tot[0] <= .5,
      {"rows_showing": tot[0], "gold_none": tot[1], "per_bucket_[n,gold,expected_1/k]":
       {k: [v[0], v[1], round(v[2], 1)] for k, v in sorted(ab.items())}}, "gold rate <= 0.5")
att = [r for r in yn if r["meta"].get("twin_kind") == "attack"]; non = [r for r in yn if r["meta"].get("twin_kind") != "attack"]
ya, yb = sum(int(r["gold"]) for r in att), sum(int(r["gold"]) for r in non)
p = float(chi2_contingency([[ya, len(att) - ya], [yb, len(non) - yb]])[1]) if att and non else 1.0
inv_ok = all(byid[x["a"]]["gold"] == byid[x["b"]]["gold"] for x in rel if x["type"] == "inv")
check("attack present uncorrelated with the label (yes/no chi-square p > 0.01; inv twins keep gold)", p > .01 and inv_ok,
      {"attack_yn": [ya, len(att)], "other_yn": [yb, len(non)], "p": round(p, 4), "inv_twins_same_gold": inv_ok},
      "p > 0.01")
# ---- reported F11 G0 9 targets
for s in sorted({r["meta"]["sampler"] for r in rows}):
    rs = [r for r in rows if r["meta"]["sampler"] == s]; k = sum(L.is_yn(r) for r in rs)
    check(f"[report] yes/no share sampler {s} 47 +/- 2", rate_ok(k, len(rs), .47, .02), [k, len(rs)], "0.45-0.49", False)
mk = defaultdict(lambda: [0, 0])
for r in yn:
    f = X.yn_feats(r); key = "marked" if "f11:asked_marked_any=True" in f else "unmarked"
    mk[key][0] += 1; mk[key][1] += int(r["gold"])
check("[report] P(yes | asked marked) and P(yes | unmarked) 50 +/- 2", all(rate_ok(y, n, .5, .02) for n, y in mk.values()),
      {k: [y, n] for k, (n, y) in mk.items()}, "each 0.48-0.52", False)
ks = Counter(min(2, neg[r["id"]].k_syn) for r in yn)
check("[report] negation k_syn >= 1 on >= 12% and k_syn = 2 on >= 3% of yes/no rows",
      (ks[1] + ks[2]) / len(yn) >= .12 and ks[2] / len(yn) >= .03, dict(ks), ">= 12% / >= 3%", False)
e = Counter(x for r in rows for x in set(r["meta"].get("edge") or []))
check("[report] short cards 15 +/- 2 of rows", rate_ok(e["short_card"], len(rows), .15, .02), [e["short_card"], len(rows)],
      "0.13-0.17", False)
em = Counter(x for r in ch for x in set(r["meta"].get("edge") or []))
check("[report] masked 10-15% and swapped 4-6% of choice rows",
      .10 <= em["masked"] / len(ch) <= .15 and .04 <= em["swapped"] / len(ch) <= .06,
      {"masked": em["masked"], "swapped": em["swapped"], "choice": len(ch)}, "10-15% / 4-6%", False)
dec = Counter(); dexp = Counter()
for r in ch:
    if r["meta"].get("subtype") == "inverted":
        continue
    lines = L.card_lines(r); idx = [L.option_card_line(r, o, lines)[0] for o in r["options"]]
    known = sorted(set(i for i in idx if i >= 0))
    gi = idx[L.gold_index(r)]
    if gi < 0 or len(known) < 2:
        continue
    rk = known.index(gi) / (len(known) - 1); dec[min(9, int(rk * 10))] += 1
    for i in known:
        dexp[min(9, int(known.index(i) / (len(known) - 1) * 10))] += 1 / len(known)
o = [dec[i] for i in range(10)]; ex_ = [dexp[i] for i in range(10)]; sc = sum(o) / sum(ex_)
pp = float(chisquare(o, [x * sc for x in ex_]).pvalue)
check("[report] gold position in the card list uniform over deciles (chi-square p > 0.01)", pp > .01,
      {"obs": o, "p": round(pp, 4)}, "p > 0.01", False)
gated = [c for c in CHK if c["gated"]]
out = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "yes_no": len(yn), "choice": len(ch),
       "checks": CHK, "failed_gated": [c["check"] for c in gated if not c["pass"]],
       "reported_misses": [c["check"] for c in CHK if not c["gated"] and not c["raw_ok"]],
       "pass": all(c["pass"] for c in gated)}
(L.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: out[k] for k in ("rows", "failed_gated", "reported_misses", "pass")}))
