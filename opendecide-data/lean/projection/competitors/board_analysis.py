#!/usr/bin/env python3
"""Where would our 4B land on the real JevBench v1.5.4 board?  Read-only analysis, CPU only, no network.

Inputs (read only):
  bench/v154/leaderboard_v154.json                                  the official v1.5.4 board snapshot (30 Sep)
  bench/jevbench_v154/results/v1.4.2.2/jevbench-v1.4.2.2-results.json  v1.4 board: argmax accuracy on the 231 public items
  bench/runs/{v154_q35_4b_pxE, v154_q35_2b_armI_1600, jev_p1, jev_p2}   our public-item runs (per item)
  bench/runs/scores_v154_all.json                                   our public-item scores (official v1.5 formulas)

Output: stdout only (saved as board_analysis_out.txt next to this file).
Run:    python3 board_analysis.py > board_analysis_out.txt
"""
import json
import math
import statistics as st
import sys

import numpy as np

sys.dont_write_bytecode = True
J = "/Users/aryamahadik/Documents/jev"
sys.path.insert(0, f"{J}/bench/v154")
import v154lib as L  # noqa: E402

B = json.load(open(f"{J}/bench/v154/leaderboard_v154.json"))
V14 = json.load(open(f"{J}/bench/jevbench_v154/results/v1.4.2.2/jevbench-v1.4.2.2-results.json"))
OURS = json.load(open(f"{J}/bench/runs/scores_v154_all.json"))["runs"]
G_MED = B["G_med"]
SYS = {s["key"]: s for s in B["systems"]}
RANKED = [s for s in B["systems"] if s.get("ranked") and s.get("full_coverage") and s.get("axes")]
JEV = SYS["jev-1.13.0"]
SEC = lambda t: print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)

# ------------------------------------------------------------------------------------------------ sizes
# Parameter counts (B) read by hand from the board's display/underlying fields (the board has no numeric field).
PARAMS = {
    "cygnet": 12, "winnow-12b": 12, "jev-1.13.0": None, "jev-omni": 12, "surogate-rune-26b-a4b-v3-rtxpro6000-a2": 26,
    "manchego-v21-v15": None, "djev": 26,
    "jevk5-v0.3-4b": 4, "plumb-4b": 4, "decider-4b-v2": 4, "decision-4b-v12": 4, "imajev-4b-rtx5090-a2": 4,
    "decision-4b-v11": 4, "semif-qwen3.5-4b": 4, "spark-s1-4b-v6": 4, "metask-jev-4b": 4, "hopper": 4,
    "malkuth-4b": 4, "reflex-4b": 4, "raw-qwen3-4b-instruct-2507": 4, "jevk5-v02": 4, "instinct-dual-4b": 4,
    "kev-4b": 4, "open-alternative-jev": 4, "localjev-qwen3.5-4b": 4, "typecastlm": 4,
    "opensourcejev-qwen35-4b-q4km": 4, "qwen3-reranker-4b": 4, "zerank-2": 4, "raw-phi-4-mini": 3.8,
    "smalljev": 2.5, "decider-2b": 1.9, "malkuth-2b": 2, "decision-2b": 2, "system-one-open": 2,
    "open-jev-zefan-2b": 2, "jevact": 2, "raw-qwen3-1.7b": 1.7,
    "simplejev-qwen3.5-0.8b": 0.8, "mghafiri-qwen3.5-0.8b-decision-model": 0.8, "deem-0.8-v1": 0.8,
    "kev-0.6b": 0.6, "raw-qwen3-0.6b": 0.6, "bosun-v31-0.6b": 0.6, "decision-fast": 0.6, "kev-0.5b": 0.5,
    "bge-reranker-v2-m3": 0.57, "mxbai-rerank-base-v2": 0.49, "mirror": 0.44, "laya": 0.42, "certo": 0.4,
    "opendecision": 0.4, "jeff": 0.4, "von-395m": 0.4, "gliner2-large": 0.4, "open-jev-deberta-v3-large": 0.43,
    "lev-350m": 0.35, "laya-multilingual": 0.32, "laya-typed-decisions": 0.4, "gliner2.5-multi": 0.29,
    "gliner2": 0.19, "openjev-verdict": 0.15, "openjev-verdict-1.4": 0.15, "gte-reranker-modernbert-base": 0.15,
    "needle-3": 0.12, "needle-3-tools": 0.12, "verdict-small": 0.12, "gliner2.5-small": 0.07,
}
# Qwen3.5-4B-class fine-tunes / readouts: the group our 4B belongs to (decoder 4B, trained or tuned for Jev-style items)
FT4B = ["jevk5-v0.3-4b", "plumb-4b", "decider-4b-v2", "decision-4b-v12", "imajev-4b-rtx5090-a2", "decision-4b-v11",
        "semif-qwen3.5-4b", "spark-s1-4b-v6", "metask-jev-4b", "hopper", "malkuth-4b", "reflex-4b", "jevk5-v02",
        "instinct-dual-4b", "kev-4b", "open-alternative-jev", "typecastlm", "opensourcejev-qwen35-4b-q4km",
        "localjev-qwen3.5-4b"]
TOP4B = ["jevk5-v0.3-4b", "plumb-4b", "decider-4b-v2", "decision-4b-v12", "imajev-4b-rtx5090-a2", "decision-4b-v11"]


def f(x, w=6, d=1):
    return f"{x:{w}.{d}f}" if isinstance(x, (int, float)) else f"{'-':>{w}s}"


def cc(s, split):
    p = (s.get("intelligence") or {}).get("per_type_split") or {}
    return (p.get(split) or {}).get("cc")


def row(s):
    I, ax = s.get("intelligence") or {}, s.get("axes") or {}
    cp = (s.get("calibration") or {}).get("parts") or {}
    sp, co = s.get("speed") or {}, s.get("cost") or {}
    return dict(key=s["key"], rank=s.get("rank"), A=(s.get("scores") or {}).get("A"), I=ax.get("intelligence"),
                Io=I.get("I_open"), Is=I.get("I_sealed"), gap=I.get("gap"), excess=I.get("excess"),
                pen=I.get("penalty"), C=ax.get("calibration"), S=ax.get("speed"), D=ax.get("cost"),
                oC=cc(s, "open|choice"), oN=cc(s, "open|noul"), oS=cc(s, "open|score"),
                sC=cc(s, "sealed|choice"), sN=cc(s, "sealed|noul"), sS=cc(s, "sealed|score"),
                abst=(cp.get("noul") or {}).get("abstention_rate"), brier=(cp.get("noul") or {}).get("brier"),
                p50=sp.get("p50_s_raw"), p95=sp.get("p95_s_raw"), p50adj=sp.get("p50_s_adjusted"),
                usd=co.get("usd_per_1000"), kind=s.get("endpoint_kind"), gpu=s.get("gpu"),
                params=PARAMS.get(s["key"]), display=s["display"])


def print_table(keys, title):
    print(f"\n{title}")
    print(f"{'rk':>3} {'key':30} {'A':>6} {'I':>5} {'Io':>5} {'Is':>5} {'gap':>5} | {'oC':>5} {'oN':>5} {'oS':>5} | "
          f"{'sC':>5} {'sN':>5} {'sS':>5} | {'C':>5} {'S':>5} {'$':>5} | {'abst':>4} {'p50ms':>6} {'$/1K':>7} "
          f"{'size':>5} host")
    for k in keys:
        r = row(SYS[k])
        print(f"{r['rank'] or '-':>3} {k[:30]:30} {f(r['A'],6,2)} {f(r['I'],5)} {f(r['Io'],5)} {f(r['Is'],5)} "
              f"{f(r['gap'],5)} | {f(r['oC'],5)} {f(r['oN'],5)} {f(r['oS'],5)} | {f(r['sC'],5)} {f(r['sN'],5)} "
              f"{f(r['sS'],5)} | {f(r['C'],5)} {f(r['S'],5)} {f(r['D'],5)} | "
              f"{f(100*r['abst'] if r['abst'] is not None else None,4,0)} {f(1000*r['p50'] if r['p50'] else None,6,0)} "
              f"{f(r['usd'],7,4)} {f(r['params'],5,1) if r['params'] else '  n/a'} {r['kind']}/{r['gpu']}")


SEC("1. Extraction: top 10 by Score A, Jev, and every <=4B / ~2B system (ranked, full coverage)")
order = B["board"]["A"]["order"]
top10 = order[:10]
small = [k for k in order if PARAMS.get(k) is not None and PARAMS[k] <= 4.0 and k not in top10]
print_table(top10, "Top 10 by Score A (Jev is #3)")
print_table([k for k in small if PARAMS[k] >= 1.5], "Other <=4B systems (1.5B-4B), by Score A rank")
print_table([k for k in small if PARAMS[k] < 1.5], "Sub-1.5B systems, by Score A rank (for completeness)")
print("\nNot ranked / partial: evalengine-decision-4b (PARTIAL, 74 context overflows), mica-v01-4b (partial run), "
      "jobe-qwen3.5-4b (not measured). classifier.dev (fast) is an honorable mention that runs on Jev: A 74.66, I 75.8.")

# ------------------------------------------------------------------------------------------------ field gap
SEC("2. The field's open -> sealed relationship")
F = [row(s) for s in RANKED if (s.get("intelligence") or {}).get("I_open") is not None]
F = [r for r in F if r["Io"] >= 20]  # below ~20 the chance-corrected numbers are noise around chance
gaps = np.array([r["gap"] for r in F])
med = float(np.median(gaps))
mad = float(np.median(np.abs(gaps - med))) * 1.4826
keep = [r for r in F if abs(r["gap"] - med) <= 3 * mad]
out = [r for r in F if abs(r["gap"] - med) > 3 * mad]
print(f"Frozen G_med (v1.5.0 batch) = {G_MED:.2f}.  Sample: ranked, full coverage, I_open >= 20: n = {len(F)}; "
      f"median gap {med:.2f}, robust sd {mad:.2f}.")
print(f"Outliers (|gap - median| > 3 robust sd), excluded from the fit: "
      + ", ".join(f"{r['key']} ({r['gap']:+.1f})" for r in out))
x = np.array([r["Io"] for r in keep]); y = np.array([r["Is"] for r in keep])
b1, b0 = np.polyfit(x, y, 1)
res = y - (b0 + b1 * x)
print(f"OLS on n = {len(keep)}: I_sealed = {b0:.2f} + {b1:.3f} x I_open   (resid sd {res.std(ddof=2):.2f}, "
      f"R^2 {1 - res.var() / y.var():.3f})")
groups = {
    "all (kept)": [r for r in keep],
    "Qwen3.5-4B-class fine-tunes/readouts": [r for r in keep if r["key"] in FT4B],
    "top-6 4B (ranks 4-10)": [r for r in F if r["key"] in TOP4B],
    "<=2.5B": [r for r in keep if r["params"] is not None and r["params"] <= 2.5],
    ">=9B open weights": [r for r in keep if r["params"] is None and r["kind"] in ("gpu", "demo") or
                          (r["params"] or 0) >= 9],
    "closed APIs (Jev, GPT, Gemini, DeepSeek...)": [r for r in keep if r["kind"] == "api"],
}
for g, rs in groups.items():
    if not rs:
        continue
    gg = [r["gap"] for r in rs]
    resid = [r["Is"] - (b0 + b1 * r["Io"]) for r in rs]
    print(f"  {g:44s} n={len(rs):3d}  median gap {st.median(gg):+5.1f}  mean {st.mean(gg):+5.1f}  "
          f"range [{min(gg):+.1f}, {max(gg):+.1f}]  mean residual vs OLS {st.mean(resid):+5.1f}")
print("Per-type open-sealed gap, top-6 4B vs Jev (CC points):")
for k in TOP4B + ["spark-s1-4b-v6", "jev-1.13.0", "cygnet", "winnow-12b"]:
    r = row(SYS[k])
    print(f"  {k:26s} choice {r['oC'] - r['sC']:+6.1f}   noul {r['oN'] - r['sN']:+6.1f}   score {r['oS'] - r['sS']:+6.1f}"
          f"   (noul abstention pooled {100 * r['abst']:.0f}%)")
t4 = [row(SYS[k]) for k in TOP4B]
print("  top-6 4B median per type: choice {:+.1f}, noul {:+.1f}, score {:+.1f}".format(
    st.median(r["oC"] - r["sC"] for r in t4), st.median(r["oN"] - r["sN"] for r in t4),
    st.median(r["oS"] - r["sS"] for r in t4)))

# ------------------------------------------------------------------------------------------------ public acc
SEC("3. A common yardstick: argmax accuracy on the SAME 231 public items (v1.4.2.2 board) -> v1.5.4 board")
v14 = {s["key"]: s.get("public_accuracy") for s in V14["systems"]}
v14["imajev-4b-rtx5090-a2"] = v14.get("imajev_4b")
pairs = [(k, v14[k], row(SYS[k])) for k in SYS if k in v14 and v14[k] and SYS[k].get("ranked")
         and SYS[k].get("axes") and (SYS[k].get("intelligence") or {}).get("I_open", -99) >= 20]
ours_acc = {"4B-E": OURS["v154_q35_4b_pxE"]["diagnostics"]["argmax_correct_v14"] / 231,
            "2B-I": OURS["v154_q35_2b_armI_1600"]["diagnostics"]["argmax_correct_v14"] / 231,
            "jev_p1 (ours)": OURS["jev_p1"]["diagnostics"]["argmax_correct_v14"] / 231}
print("Our public argmax accuracy: " + ", ".join(f"{k} {v:.4f}" for k, v in ours_acc.items())
      + f";  board's v1.4 value for Jev {v14['jev-1.13.0']:.4f} (identical -> our Jev runs match the board's).")
rank_pub = sorted([(v, k) for k, v in v14.items() if v], reverse=True)
above = [k for v, k in rank_pub if v > ours_acc["4B-E"]]
print(f"Systems with public accuracy above our 4B-E ({ours_acc['4B-E']:.3f}): {len(above)} -> {', '.join(above)}")


def fit(rs, yk):
    xx = np.array([a for _, a, _ in rs]); yy = np.array([r[yk] for _, _, r in rs])
    s1, s0 = np.polyfit(xx, yy, 1)
    rr = yy - (s0 + s1 * xx)
    return s0, s1, rr.std(ddof=2), np.corrcoef(xx, yy)[0, 1]


for label, rs in (("all systems (I_open>=20)", pairs), ("Qwen3.5-4B class", [p for p in pairs if p[0] in FT4B])):
    print(f"\n  {label}: n = {len(rs)}")
    for yk in ("Io", "Is", "I"):
        s0, s1, sd, rho = fit(rs, yk)
        print(f"    board {yk:3s} = {s0:7.1f} + {s1:6.1f} x acc  (resid sd {sd:4.1f}, r = {rho:+.2f})  ->  "
              f"4B-E {s0 + s1 * ours_acc['4B-E']:5.1f}, 2B-I {s0 + s1 * ours_acc['2B-I']:5.1f}")
print("\n  4B-class systems (public acc -> board):")
for k, a, r in sorted([p for p in pairs if p[0] in FT4B], key=lambda p: -p[1]):
    print(f"    {k:28s} acc {a:.3f}  I_open {r['Io']:5.1f}  I_sealed {r['Is']:5.1f}  I {r['I']:5.1f}  "
          f"noul abst {100 * r['abst']:3.0f}%")

# ------------------------------------------------------------------------------------------------ commit mechanics
SEC("4. The Noul abstention band and what committing is worth (public items, our runs; board peers)")
items = L.load_public(f"{J}/bench/jevbench_v154")


def load(name):
    recs = {}
    for line in open(f"{J}/bench/runs/{name}/results.jsonl"):
        if line.strip():
            d = json.loads(line)
            recs[d["task_id"]] = d
    return recs


def outs_for(recs, transform=None):
    o = []
    for iid, it in items.items():
        rec = recs.get(iid)
        if transform and rec and rec.get("probs") and it["question"]["type"] == "noul":
            rec = dict(rec, probs=transform(dict(rec["probs"])))
        o.append(L.item_outcome(it, rec))
    return o


def commit(p):
    y = p.get("yes", 0.0)
    return {"yes": 1.0 if y > 0.5 else 0.0, "no": 0.0 if y > 0.5 else 1.0}


def band_edge(p):  # move only the abstaining answers to the nearest band edge on their argmax side
    y = p.get("yes", 0.0)
    if 0.5 < y < 0.8:
        y = 0.8
    elif 0.2 < y <= 0.5:
        y = 0.2
    return {"yes": y, "no": 1.0 - y}


for name in ("v154_q35_4b_pxE", "v154_q35_2b_armI_1600", "jev_p1", "jev_p2"):
    recs = load(name)
    base = outs_for(recs)
    no = [o for o in base if o["type"] == "noul"]
    ab = [o for o in no if o["abstain"]]
    q = sum(o["argmax_correct"] for o in ab) / len(ab) if ab else float("nan")
    c = [o for o in no if not o["abstain"]]
    line = (f"  {name:24s} noul n={len(no)} abstain {len(ab)} ({100 * len(ab) / len(no):.0f}%), "
            f"argmax acc on abstained q = {q:.2f}, acc when committed {sum(o['correct'] for o in c) / len(c):.2f}")
    print(line)
    for tag, tf in (("as returned", None), ("full commit", commit), ("band edge", band_edge)):
        oo = outs_for(recs, tf)
        I, det = L.intelligence_open(oo)
        C, parts = L.calibration(oo)
        print(f"      {tag:12s} I {I:5.1f}  noul CC {det['noul']['cc']:5.1f}  Calib {C:5.1f} "
              f"(noul part {parts['noul']['score']:5.1f}, ECE {parts['noul']['ece']:.3f}, Brier {parts['noul']['brier']:.3f})")

print("\nBoard peers: what the same commit would give them (EST).  CC_noul = 2*acc - 1; committing turns each")
print("abstention into a correct answer with prob q.  The board gives only the pooled abstention rate, so the")
print("open/sealed split assumes sealed abstention = open + 0.10.")


def committed_equiv(r, q, delta=0.10):
    a_pool = r["abst"]
    a_o = max(0.0, a_pool - delta * 180 / 495)
    a_s = min(0.95, a_o + delta)
    n_o = r["oN"] + 200 * a_o * q
    n_s = r["sN"] + 200 * a_s * q
    Io = (r["oC"] + min(n_o, 100) + r["oS"]) / 3
    Is = (r["sC"] + min(n_s, 100) + r["sS"]) / 3
    return Io, Is, (Io + Is) / 2, n_o, n_s


for k in TOP4B + ["spark-s1-4b-v6", "decider-2b", "malkuth-2b", "jev-1.13.0", "cygnet", "winnow-12b"]:
    r = row(SYS[k])
    vals = [committed_equiv(r, q) for q in (0.55, 0.62, 0.70)]
    print(f"  {k:24s} as returned I {r['I']:5.1f} ->  committed (q .55/.62/.70): "
          + " / ".join(f"{v[2]:5.1f}" for v in vals)
          + f"   [q .62: Io {vals[1][0]:.1f}, Is {vals[1][1]:.1f}, noul {vals[1][3]:.0f}/{vals[1][4]:.0f}]")

# ------------------------------------------------------------------------------------------------ our placement
SEC("5. Our 4B-E on the real board: three estimates of I_open, then I_sealed from the field")
pub = OURS["v154_q35_4b_pxE"]
jp = OURS["jev_p1"]
raw_I, dec_I = pub["I_open"], 78.7  # 78.7 = committed what-if (RESULTS_30sep.md, recomputed in section 4)
jev_pub = jp["I_open"]
Jo, Js, Ji = JEV["intelligence"]["I_open"], JEV["intelligence"]["I_sealed"], JEV["axes"]["intelligence"]
g4 = st.median(r["gap"] for r in keep if r["key"] in FT4B)
gt6 = st.median(row(SYS[k])["gap"] for k in TOP4B)


def board_I(Io, gap=None):
    Is = (b0 + b1 * Io) if gap is None else Io - gap
    g, ex, pen = L.overfit_penalty(Io, Is, G_MED)
    return Is, (Io + Is) / 2 * pen, pen


print(f"Jev: public-231 I {jev_pub:.1f} (our run) vs board I_open {Jo:.1f}, I_sealed {Js:.1f}, I {Ji:.1f}.  "
      f"The public 231 are {Jo - jev_pub:.1f} points harder for Jev than the board's open set.")
print(f"Field: OLS I_sealed = {b0:.2f} + {b1:.3f} I_open;  4B-class median gap {g4:.1f};  top-6 4B median gap {gt6:.1f}.")
print(f"Dev optimism: the public items were our development set.  EST discount 3-6 I points (v0.10 lesson: public")
print(f"+6.9 vs Jev, held-out lost).\n")
cases = [
    ("M1 literal, raw", raw_I), ("M1 literal, decisive", dec_I),
    ("M2 Jev-anchored, raw", Jo + (raw_I - jev_pub)), ("M2 Jev-anchored, decisive", Jo + (dec_I - jev_pub)),
]
print(f"  {'method':30s} {'I_open':>6s} | {'I via OLS':>9s} {'I via 4B gap':>12s} | same, after -4 dev discount")
for lab, Io in cases:
    a = board_I(Io)[1]
    b = board_I(Io, g4)[1]
    a2 = board_I(Io - 4)[1]
    b2 = board_I(Io - 4, g4)[1]
    print(f"  {lab:30s} {Io:6.1f} | {a:9.1f} {b:12.1f} | {a2:6.1f} {b2:6.1f}")
s0, s1, sd, _ = fit([p for p in pairs if p[0] in FT4B], "I")
m3raw = s0 + s1 * ours_acc["4B-E"]
print(f"\n  M3 peer-anchored, raw: 4B-class regression on public accuracy -> board I {m3raw:.1f} (resid sd {sd:.1f})")
pe = [committed_equiv(row(SYS[k]), 0.62)[2] for k in TOP4B]
print(f"  M3 peer-anchored, decisive: top-6 4B committed-equivalent I (q=.62) median {st.median(pe):.1f}, "
      f"range [{min(pe):.1f}, {max(pe):.1f}]")

# ------------------------------------------------------------------------------------------------ Monte Carlo
SEC("6. Monte Carlo placement (EST inputs, stated below) and P(beat Jev)")
rng = np.random.default_rng(0)
N = 200_000
jA, cygA = JEV["scores"]["A"], SYS["cygnet"]["scores"]["A"]
boardA = sorted([s["scores"]["A"] for s in RANKED], reverse=True)
boardI = sorted([s["axes"]["intelligence"] for s in RANKED], reverse=True)


def speed_axis(p50):
    return L.speed(p50, p50 * 1.03, "gpu")


# Speed: the evaluator runs open weights on its own GPU (H100 / RTX 5090 / RTX PRO 6000).
# EST raw p50 on their GPU: lognormal, median 30 ms, 80% range ~ 17-55 ms (L4 eager measured 110 ms; H100+graphs EST 24).
p50 = np.exp(rng.normal(math.log(0.030), 0.45, N))
p95 = p50 * 1.03  # our p95/p50 on the L4 was 1.02
S = 0.5 * (100 - 20 * np.log10((2 * p50 + 0.15) / 0.1)) + 0.5 * (100 - 20 * np.log10((2 * p95 + 0.15) / 0.1))
assert abs(S[0] - speed_axis(p50[0])) < 1e-9
# Cost: tokens x $0.03/M.  Our public 817.8 tok vs Jev 914.8; Jev's board cost implies 769 tok -> ours ~687 (EST sd 6%).
usd = 0.0245 * (JEV["cost"]["usd_per_1000"] / 0.0384198) * np.exp(rng.normal(0, 0.06, N))
D = 100 - 30 * np.log10(usd / 0.001)
scen = {
    # name: (I mean, I sd, Calib mean, Calib sd)  -- all EST, see board.md section 4
    "raw readout (as trained, T=1)": (m3raw, 3.5, 85.5, 2.0),
    "decisive readout (yes/no committed)": (68.5, 4.0, 77.5, 2.5),
    "band-edge readout (abstentions -> 0.2/0.8)": (68.5, 4.0, 81.5, 2.5),
}
res = {}
for lab, (mi, si, mc, sc) in scen.items():
    I = rng.normal(mi, si, N)
    C = rng.normal(mc, sc, N)
    A = 4 / (1 / I + 1 / C + 1 / S + 1 / D)
    A = np.where(I < 50, A * (np.clip(I, 0, None) / 50) ** 2, A)
    rankA = 1 + np.searchsorted(-np.array(boardA), -A)  # position among the current 106 ranked rows
    rankI = 1 + np.searchsorted(-np.array(boardI), -I)
    res[lab] = dict(I=I, A=A)
    q = lambda v: np.percentile(v, [10, 50, 90])
    print(f"\n  {lab}")
    print(f"    I      10/50/90 = {q(I)[0]:5.1f} / {q(I)[1]:5.1f} / {q(I)[2]:5.1f}     P(I > Jev {Ji:.1f}) = {np.mean(I > Ji):.2f}"
          f"   P(I > Winnow {SYS['winnow-12b']['axes']['intelligence']:.1f}) = {np.mean(I > SYS['winnow-12b']['axes']['intelligence']):.2f}")
    print(f"    Calib {mc:.1f}, Speed median {np.median(S):.1f} (10-90 {q(S)[0]:.1f}-{q(S)[2]:.1f}), "
          f"Cost median {np.median(D):.1f} (${np.median(usd):.4f}/1K)")
    print(f"    Score A 10/50/90 = {q(A)[0]:5.2f} / {q(A)[1]:5.2f} / {q(A)[2]:5.2f}    P(A > Jev {jA:.2f}) = {np.mean(A > jA):.2f}"
          f"   P(A > Cygnet {cygA:.2f}, i.e. #1) = {np.mean(A > cygA):.2f}")
    print(f"    Score A rank among today's 106: median #{int(np.median(rankA))} (10-90: #{int(np.percentile(rankA, 10))}"
          f"-#{int(np.percentile(rankA, 90))});  Intelligence rank median #{int(np.median(rankI))} "
          f"(10-90: #{int(np.percentile(rankI, 10))}-#{int(np.percentile(rankI, 90))})")

print("\n  Sensitivity of the decisive / band-edge readouts to the Intelligence centre and spread:")
for mi in (65.0, 66.5, 68.5, 70.5, 72.0):
    for si in (3.0, 4.0, 5.0):
        I = rng.normal(mi, si, N)
        out_ = []
        for mc in (77.5, 81.5):
            C = rng.normal(mc, 2.5, N)
            A = 4 / (1 / I + 1 / C + 1 / S + 1 / D)
            out_.append(np.mean(A > jA))
        print(f"    I ~ N({mi:.1f}, {si:.0f}):  P(I > Jev) {np.mean(I > Ji):.2f}   P(A > Jev) decisive {out_[0]:.2f}, "
              f"band-edge {out_[1]:.2f}")

print("\n  Axis-by-axis vs Jev on the board (Jev: I 72.0, C 88.0, S 83.8 [616 ms p50 measured by the evaluator], $ 54.7):")
print(f"    P(Speed > {JEV['axes']['speed']:.1f}) = {np.mean(S > JEV['axes']['speed']):.3f};  even L4-eager 110 ms gives "
      f"{L.speed(0.110, 0.112, 'gpu'):.1f}.  Break-even raw p50 ~ {1000 * (0.1 * 10 ** ((100 - JEV['axes']['speed']) / 20) - 0.15) / 2:.0f} ms.")
print(f"    P(Cost > {JEV['axes']['cost']:.1f}) = {np.mean(D > JEV['axes']['cost']):.3f}")

# ------------------------------------------------------------------------------------------------ owner joint
SEC("7. Owner's success definition: joint probability (Gaussian copula over the factor Bernoullis)")
from statistics import NormalDist  # noqa: E402

nd = NormalDist()
P_board_I = float(np.mean(res["decisive readout (yes/no committed)"]["I"] > Ji))
F = {  # name: P   (sources in board.md section 6)
    "ohs_acc": 0.45,      # OHS-3 overall accuracy point >= Jev (FINAL_PROJECTION reconciled)
    "jb_pub": 0.88,       # JevBench public-item run, decisive readout, Intelligence >= Jev as returned (re-run risk)
    "jb_board": P_board_I,  # real board Intelligence > Jev (this file, section 6)
    "cons_comp": 0.70,    # complement violations <= Jev
    "cons_perm": 0.30,    # option-order drift <= Jev
    "hijack": 0.97, "inject": 0.70,  # point win; a significant win is ~0.10
    "speed": 0.75,        # median end-to-end < Jev with direct hosting (0.9 if timed before OHS-3; ~0.1 via Modal)
    "cost": 0.95,         # JevBench formula
}
names = list(F)
R = np.eye(len(names))


def setc(a, b, r):
    i, j = names.index(a), names.index(b)
    R[i, j] = R[j, i] = r


setc("ohs_acc", "jb_board", 0.40)   # same model quality, different items
setc("ohs_acc", "jb_pub", 0.20)
setc("jb_pub", "jb_board", 0.30)
setc("ohs_acc", "cons_comp", 0.30)  # violations rise as yes/no accuracy falls (projection sec. 10)
setc("cons_comp", "cons_perm", 0.20)
setc("hijack", "inject", 0.20)
Z = rng.multivariate_normal(np.zeros(len(names)), R, 400_000)
W = {n: Z[:, i] < nd.inv_cdf(F[n]) for i, n in enumerate(names)}


def joint(req, override=None):
    ov = override or {}
    m = np.ones(len(Z), bool)
    for n in req:
        p = ov.get(n, F[n])
        m &= Z[:, names.index(n)] < nd.inv_cdf(p)
    return m.mean()


def indep(req, override=None):
    ov = override or {}
    return float(np.prod([ov.get(n, F[n]) for n in req]))


print("Factors: " + ", ".join(f"{n} {F[n]:.2f}" for n in names))
print("Correlations: ohs_acc~jb_board .40, ohs_acc~jb_pub .20, jb_pub~jb_board .30, ohs_acc~cons_comp .30, "
      "cons_comp~cons_perm .20, hijack~inject .20; all others 0.")
V = [
    ("O1 owner, JevBench = public-item run, consistency = both endpoints",
     ["ohs_acc", "jb_pub", "cons_comp", "cons_perm", "hijack", "inject", "speed", "cost"], None),
    ("O2 same, consistency = complement only",
     ["ohs_acc", "jb_pub", "cons_comp", "hijack", "inject", "speed", "cost"], None),
    ("O3 O1 but JevBench = the real board (sealed half counted)",
     ["ohs_acc", "jb_board", "cons_comp", "cons_perm", "hijack", "inject", "speed", "cost"], None),
    ("O4 O2 but JevBench = the real board",
     ["ohs_acc", "jb_board", "cons_comp", "hijack", "inject", "speed", "cost"], None),
    ("O5 O1 with the speed lever done (direct hosting timed, 0.90)",
     ["ohs_acc", "jb_pub", "cons_comp", "cons_perm", "hijack", "inject", "speed", "cost"], {"speed": 0.90}),
    ("O6 O2 with speed lever done", ["ohs_acc", "jb_pub", "cons_comp", "hijack", "inject", "speed", "cost"],
     {"speed": 0.90}),
    ("O7 O1 if we stopped today (Modal endpoint, speed 0.10)",
     ["ohs_acc", "jb_pub", "cons_comp", "cons_perm", "hijack", "inject", "speed", "cost"], {"speed": 0.10}),
    ("O8 O2 with OHS-3 'beat' read as PREREG 'matches' (0.50)",
     ["ohs_acc", "jb_pub", "cons_comp", "hijack", "inject", "speed", "cost"], {"ohs_acc": 0.50}),
    ("O9 O2 with injection needing a significant win (0.10)",
     ["ohs_acc", "jb_pub", "cons_comp", "hijack", "inject", "speed", "cost"], {"inject": 0.10}),
    ("O10 accuracy-only core: OHS-3 >= Jev AND JevBench public >= Jev", ["ohs_acc", "jb_pub"], None),
]
for lab, req, ov in V:
    print(f"  {lab:70s} copula {joint(req, ov):.3f}   independent {indep(req, ov):.3f}")
