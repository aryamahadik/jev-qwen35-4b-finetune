"""A28 r7 adversarial review harness v2 (+ simbins, median / per-card yes / gate short) (CPU only; counts only, never row texts). TAG today|sim.
Capture (as review r5): build() runs to cap_trim, the state is kept, the real cap_trim runs twice (determinism).
Every 2.1 quota and the cap are recomputed here independently from the rows, the relation files and the sidecars."""
import json, math, os, sys, time, hashlib
from collections import Counter, defaultdict
from pathlib import Path
LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
sys.path.insert(0, str(LEAN / "c_build"))
import crowd_select as cs  # noqa
import mixer as mx  # noqa
TAG = sys.argv[1]
HS = os.environ.get("PYTHONHASHSEED", "x")
R = Path(__file__).resolve().parent
W = R / f"work_{TAG}_{HS}"
W.mkdir(exist_ok=True)
mx.WORK, mx.LOG, cs.LOG = W, W / "progress_mixer.log", W / "progress_mixer.log"
if TAG in ("sim", "simbins"):
    mx.run_denylist = lambda ilog, q, rep, final=False: (rep.__setitem__("denylist_new", {"denied": []}), set())[1]
    _rp = cs.relation_problems
    cs.relation_problems = lambda fam, man, p, rels: [] if fam in ("F1", "F12") else _rp(fam, man, p, rels)
else:
    ver = json.loads((LEAN / "c_build/mix_r1/denylist_verdicts_mix_r1.json").read_text())["verdicts"]
    DEN = {k for k, v in ver.items() if v.get("verdict") in ("deny", "no_new_rows")}
    mx.run_denylist = lambda ilog, q, rep, final=False: (rep.__setitem__("denylist_new", {"denied": sorted(DEN)}), set(DEN))[1]
if TAG == "simbins":
    PROV = ("F1", "F2", "F7", "F8", "F10", "F12", "F13")
    _lf = cs.load_family
    def _bin(r):   # seeded, length-correlated (long rows harder): proxy long = rendered json >= 7,000 chars
        u = mx.h64(mx.SEED, "r7bins", r["id"]) % 1000 / 1000
        e, mm = ((0.10, 0.60) if len(json.dumps(r)) >= 7000 else (0.24, 0.80))
        return "easy" if u < e else "medium" if u < mm else "hard"
    def load_family(ilog, fam):
        rows, rels = _lf(ilog, fam)
        if fam in PROV:
            rows = [r | {"meta": dict(r.get("meta") or {}, difficulty_bin=_bin(r))} for r in rows]
        return rows, rels
    cs.load_family = load_family
    _ok = mx.own_keys
    mx.own_keys = lambda r, b: _ok(r, (r.get("meta") or {}).get("difficulty_bin") or b if b == "na" else b)
REAL = mx.cap_trim
CAP = {}
class Stop(Exception): pass
def cap(rows, rels, ntok, pools, ctx, targets, ever, handled, accept, rep):
    CAP.update(rows=list(rows), rels=list(rels), ntok=ntok, pools=pools, ctx=ctx, targets=dict(targets), ever=ever,
               ever0=dict(ever), accept=accept, tried0={b: set(p.tried) for b, p in pools.items()}, handled=set(handled))
    raise Stop
mx.cap_trim = cap
t0 = time.time()
a = type("A", (), {"final": False, "dry_run": True, "sealed_sha": None, "decontam_drops": []})()
try:
    mx.build(a)
except Stop:
    pass
cap_t = time.time() - t0
NT = CAP["ntok"]
# ---- independent reference data (relation files + sidecars read here, not via mixer)
INVB, SIDE = set(), {}
for f in cs.FAMS:
    ff = cs.fam_files(f)
    if ff["rel"] is not None and Path(ff["rel"]).exists():
        for l in open(ff["rel"]):
            x = json.loads(l)
            if x.get("type") == "inv":
                INVB.add(x["b"])
    s = Path(ff["cand"]).with_name("candidates_r1.sidecar.jsonl")
    if s.exists():
        for l in open(s):
            x = json.loads(l)
            SIDE[x.get("id")] = x
def lform(f, r):
    sd, m = SIDE.get(r["id"], {}), r.get("meta") or {}
    if f == "F10":
        return {"neutral": "masked", "swapped": "swapped"}.get(sd.get("mode"), "plain") if "mode" in sd else None
    return sd.get("label_form") or sd.get("vocab") or m.get("label_form")
def ybad(r):
    sd = SIDE.get(r["id"], {})
    if isinstance(sd.get("yes_bad"), bool):
        return sd["yes_bad"]
    return {"bad": True, "not bad": False}.get(sd.get("polarity") or sd.get("polarity_tag"))
def bk(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"
def stats(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["_block"]].append(r)
    new = [r for b, v in by.items() if b != "replay" for r in v]
    nt = sum(NT[r["id"]] for r in new)
    lr = [r for r in new if NT[r["id"]] >= 2000]
    own = sum(len(by.get(f, [])) for f in cs.FAMS)
    out = {"rows": len(rows), "new": len(new), "replay": len(by["replay"]), "own": own,
           "long_row_share": len(lr) / len(new), "long_tok_share": sum(NT[r["id"]] for r in lr) / nt,
           "replay_share": len(by["replay"]) / len(rows), "pub": dict(Counter(r["source"] for r in by["public"])),
           "com": dict(Counter(str(cs.commit_group(r)) for r in by["COMMIT"])), "fam": {}}
    for f in cs.FAMS:
        Rf = by.get(f, [])
        if not Rf:
            continue
        n = len(Rf)
        ids = {r["id"]: r for r in Rf}
        tsA, tsB = set(), set()
        for r in Rf:
            m = r.get("meta") or {}
            t, k = m.get("twin_of"), str(m.get("twin_kind") or "").lower()
            if t in ids and str(ids[t].get("gold")) != str(r.get("gold")):
                tsA |= {r["id"], t}
            if t in ids and not ("attack" in k or k == "inv" or r["id"] in INVB):
                tsB |= {r["id"], t}
        att = sum(1 for r in Rf if r["id"] in INVB or r.get("role") in ("attacked", "attack") or
                  "attack" in str((r.get("meta") or {}).get("twin_kind") or "").lower())
        short = sum(1 for r in Rf if (r.get("meta") or {}).get("defs_style") in ("short", "none", "no_card") or
                    SIDE.get(r["id"], {}).get("short") is True)
        ch = [r for r in Rf if r.get("qtype") == "choice"]
        yn = [r for r in Rf if r.get("qtype") != "choice"]
        lf = Counter(lform(f, r) for r in ch)
        lfc = sum(v for k, v in lf.items() if k is not None)
        yb = [ybad(r) for r in yn]
        ybn = [x for x in yb if x is not None]
        cards = Counter((r.get("meta") or {}).get("card_id") for r in Rf)
        fsc = {(r.get("meta") or {}).get("card_id") for r in Rf if SIDE.get(r["id"], {}).get("fewshot_card") is True or
               (r.get("meta") or {}).get("defs_style") == "few_shot"}
        ivc = {(r.get("meta") or {}).get("card_id") for r in Rf if SIDE.get(r["id"], {}).get("inverted_card") is True or
               SIDE.get(r["id"], {}).get("inverted") is True}
        ob = Counter(bk(len(r.get("options") or [])) for r in ch)
        cy = defaultdict(lambda: [0, 0])
        for r in yn:
            cy[(r.get("meta") or {}).get("card_id")][0] += 1
            cy[(r.get("meta") or {}).get("card_id")][1] += int(str(r.get("gold")) == "1")
        bins_ = Counter((r.get("meta") or {}).get("difficulty_bin") or "na" for r in Rf)
        out["fam"][f] = {"n": n, "share": n / own, "long": sum(1 for r in Rf if NT[r["id"]] >= 2000) / n,
                         "twin_set": len(tsA) / n, "twin_setB": len(tsB) / n, "attack": att / n, "short": short / n,
                         "yes_no": len(yn) / n, "yes_rate": (sum(1 for r in yn if str(r.get("gold")) == "1") / len(yn)) if yn else None,
                         "masked": (lf["masked"] / lfc) if lfc else None, "swapped": (lf["swapped"] / lfc) if lfc else None,
                         "yes_bad": (sum(ybn) / len(ybn)) if ybn else None, "cards": sorted(map(str, cards)),
                         "max_card": max(cards.values()), "median_card": sorted(cards.values())[len(cards) // 2],
                         "cy": {str(k): v for k, v in cy.items()}, "bins": dict(bins_), "fs_cards": len(fsc) / len(cards), "inv_cards": len(ivc) / len(cards),
                         **{f"opt_{k}": (ob[k] / len(ch) if ch else None) for k in ("2-4", "5-9", "10-19", "20-60")}}
    return out
BANDS = {"twin_set": (0.20, 0.25), "attack": (0.05, 0.05), "short": (0.10, 0.20), "masked": (0.10, 0.15),
         "swapped": (0.05, 0.05), "yes_bad": (0.45, 0.55), "opt_2-4": (0.32, 0.38), "opt_5-9": (0.32, 0.38),
         "opt_10-19": (0.12, 0.18), "opt_20-60": (0.12, 0.18), "fs_cards": (0.05, 0.10), "inv_cards": (0.10, 0.15)}
F10B = {"masked": (0.40, 0.40), "swapped": (0.30, 0.30)}
def dist(v, b):
    return max(0.0, b[0] - v, v - b[1])
def compare(s0, s1, targets, refilled):
    bad, near = [], []
    if s1["long_row_share"] > 0.09 + 1e-12 or s1["long_tok_share"] > 0.30 + 1e-12:
        bad.append(f"cap not met {s1['long_row_share']:.4f}/{s1['long_tok_share']:.4f}")
    if s1["pub"] != s0["pub"] or s1["com"] != s0["com"]:
        bad.append("public/commit counts changed")
    for f, a in s0["fam"].items():
        b = s1["fam"].get(f)
        if b is None:
            bad.append(f"{f} vanished"); continue
        for k, band in BANDS.items():
            band = F10B.get(k, band) if f == "F10" else band
            v0, v1 = a.get(k), b.get(k)
            if v0 is None or v1 is None:
                continue
            for edge in ((band[0], 1.0), (0.0, band[1])):   # each band edge its own rule
                if dist(v1, edge) > dist(v0, edge) + 1e-9:
                    bad.append(f"{f} {k} {v0:.4f}->{v1:.4f} band {band}")
                    break
            if dist(v1, band) > 0 and abs(v1 - v0) > 0.005:
                near.append(f"{f} {k} {v0:.4f}->{v1:.4f}")
        if a["yes_rate"] is not None and abs(b["yes_rate"] - 0.5) > max(0.02, abs(a["yes_rate"] - 0.5)) + 1e-9:
            bad.append(f"{f} yes_rate {a['yes_rate']:.4f}->{b['yes_rate']:.4f}")
        if set(b["cards"]) != set(a["cards"]):
            bad.append(f"{f} card set changed ({len(a['cards'])}->{len(b['cards'])})")
        if b["max_card"] > 128:
            bad.append(f"{f} rows per card {b['max_card']}")
        lim = 0.12 if f in refilled else max(0.12, a["share"])
        if b["share"] > lim + 1e-9:
            bad.append(f"{f} share {a['share']:.4f}->{b['share']:.4f} > {lim:.4f}")
        if b["n"] > math.floor(1.5 * targets[f]):
            bad.append(f"{f} rows {b['n']} > 1.5x target {targets[f]}")
    return bad, near
GATE_SHORT = {"F4": (0.12, 0.18), "F5": (0.12, 0.18), "F7": (0.13, 0.17), "F10": (0.13, 0.17)}
def extra(s0, s1):
    out = {}
    from scipy.stats import binomtest
    for f, a in s0["fam"].items():
        b = s1["fam"].get(f)
        if not b:
            continue
        lo, hi = GATE_SHORT.get(f, (0.10, 0.20))
        sh = [round(a["short"], 4), round(b["short"], 4), (lo <= a["short"] <= hi) and not (lo <= b["short"] <= hi)]
        out_c, out_c10 = 0, 0
        for c, (n0, y0) in a["cy"].items():
            n1, y1 = b["cy"].get(c, [0, 0])
            if not n1 or not (0.2 <= y0 / n0 <= 0.8) or 0.2 <= y1 / n1 <= 0.8:
                continue
            out_c += 1
            if binomtest(y1, n1, 0.2 if y1 / n1 < 0.2 else 0.8).pvalue < 0.01:
                out_c10 += 1
        def bx(d):
            t = sum(d.values()) or 1
            return {k: round(v / t, 3) for k, v in d.items()}
        out[f] = {"median_card": [a["median_card"], b["median_card"]], "short_gate": sh,
                  "cards_yes_rate_left_20_80": out_c, "of_which_binom_p_lt_01": out_c10,
                  "bins": [bx(a["bins"]), bx(b["bins"])] if TAG == "simbins" or "na" not in a["bins"] else None}
    return out
def digest(rows):
    return hashlib.sha256(json.dumps([(r["id"], r["_block"]) for r in rows]).encode()).hexdigest()[:16]
def restore():
    CAP["ever"].clear(); CAP["ever"].update(CAP["ever0"])
    for b, p in CAP["pools"].items():
        p.tried = set(CAP["tried0"][b])
def run():
    restore()
    rep = {}
    t = time.time()
    rows, rels, probs = REAL([dict(r) for r in CAP["rows"]], list(CAP["rels"]), NT, CAP["pools"], CAP["ctx"],
                             CAP["targets"], CAP["ever"], set(CAP["handled"]), CAP["accept"], rep)
    return rows, rels, probs, rep, time.time() - t
s0 = stats(CAP["rows"])
rows1, rels1, probs1, rep1, t1 = run()
s1 = stats(rows1)
i0 = {r["id"] for r in CAP["rows"]}
added = [r for r in rows1 if r["id"] not in i0]
refilled = {r["_block"] for r in added if r["_block"] in cs.FAMS}
bad, near = compare(s0, s1, CAP["targets"], refilled)
if any(NT[r["id"]] >= 2000 for r in added):
    bad.append(f"{sum(NT[r['id']] >= 2000 for r in added)} added rows >= 2000 tokens")
ac = rep1["a28_cap"]
rem = ac.get("remainder_rows", 0)
if rem and s1["replay"] != math.floor(1.5 * s1["new"]):
    bad.append(f"replay {s1['replay']} != floor(1.5 x {s1['new']})")
if (rows1 and len({r['id'] for r in rows1}) != len(rows1)):
    bad.append("duplicate ids")
d1 = digest(rows1)
rows2, _, probs2, rep2, t2 = run()
d2 = digest(rows2)
res = {"tag": TAG, "hs": HS, "capture_s": round(cap_t), "trim_s": [round(t1), round(t2)], "digest": [d1, d2],
       "same_in_process": d1 == d2 and probs1 == probs2, "probs": probs1, "remainder": rem, "replay_cut": ac.get("replay_cut"),
       "cap": [round(s0["long_row_share"], 4), round(s0["long_tok_share"], 4), round(s1["long_row_share"], 4), round(s1["long_tok_share"], 4)],
       "replay_share": [round(s0["replay_share"], 4), round(s1["replay_share"], 4)], "new": [s0["new"], s1["new"]],
       "added_rows": len(added), "refilled_fams": sorted(refilled), "violations": bad, "moved_outside_band": near,
       "fam": {f: {k: [round(s0["fam"][f][k], 4) if isinstance(s0["fam"][f][k], float) else s0["fam"][f][k],
                       round(s1["fam"][f][k], 4) if isinstance(s1["fam"][f][k], float) else s1["fam"][f][k]]
                   for k in ("n", "share", "long", "twin_set", "twin_setB", "attack", "short", "masked", "swapped", "yes_bad", "yes_rate")}
               for f in s0["fam"] if f in s1["fam"]},
       "extra": extra(s0, s1),
       "audit": (ac.get("audit") or {}) if isinstance(ac.get("audit"), dict) else str(ac.get("audit"))[:300]}
(R / f"res_{TAG}_{HS}.json").write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: res[k] for k in ("tag", "hs", "capture_s", "trim_s", "digest", "same_in_process", "remainder", "cap",
                                       "replay_share", "new", "added_rows")}))
print("violations", len(bad), bad[:12])
print("probs", [p[:120] for p in probs1][:6])
