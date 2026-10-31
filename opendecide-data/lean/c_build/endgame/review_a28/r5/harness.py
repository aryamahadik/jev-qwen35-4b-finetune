"""A28 r5 adversarial review harness (CPU only; counts only, never row texts). TAG today|sim.
today: the dry-run pools (deny-list verdicts taken from c_build/mix_r1's last real verdict file, no subprocess).
sim: F1 / F12 relation refusals and the deny-list bypassed (F1, F10, F12 at quota), as the fixer's sim.
Captures the state at cap_trim, runs the real cap_trim twice (determinism), recomputes every quota independently."""
import json, math, os, statistics, sys, time, hashlib
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
mx.WORK, mx.LOG, cs.LOG = W, W / "progress_mixer.log", W / "progress_mixer.log"
if TAG == "sim":
    mx.run_denylist = lambda ilog, q, rep, final=False: (rep.__setitem__("denylist_new", {"denied": []}), set())[1]
    _rp = cs.relation_problems
    cs.relation_problems = lambda fam, man, p, rels: [] if fam in ("F1", "F12") else _rp(fam, man, p, rels)
else:
    ver = json.loads((LEAN / "c_build/mix_r1/denylist_verdicts_mix_r1.json").read_text())["verdicts"]
    DEN = {k for k, v in ver.items() if v.get("verdict") in ("deny", "no_new_rows")}
    mx.run_denylist = lambda ilog, q, rep, final=False: (rep.__setitem__("denylist_new", {"denied": sorted(DEN)}), set(DEN))[1]
REAL = mx.cap_trim
CAP = {}
class Stop(Exception): pass
def cap(rows, rels, ntok, pools, ctx, targets, ever, handled, accept, rep):
    CAP.update(rows=list(rows), rels=list(rels), ntok=ntok, pools=pools, ctx=ctx, targets=dict(targets), ever=ever,
               ever0=dict(ever), accept=accept, tried0={b: set(p.tried) for b, p in pools.items()})
    raise Stop
mx.cap_trim = cap
t0 = time.time()
a = type("A", (), {"final": False, "dry_run": True, "sealed_sha": None, "decontam_drops": []})()
try:
    mx.build(a)
except Stop:
    pass
cap_t = time.time() - t0
SIDE = CAP["ctx"].get("sidecar") or {}
def restore():
    CAP["ever"].clear(); CAP["ever"].update(CAP["ever0"])
    for b, p in CAP["pools"].items():
        p.tried = set(CAP["tried0"][b])
def run():
    restore()
    rep = {}
    t = time.time()
    rows, rels, probs = REAL([dict(r) for r in CAP["rows"]], list(CAP["rels"]), CAP["ntok"], CAP["pools"], CAP["ctx"],
                             CAP["targets"], CAP["ever"], set(), CAP["accept"], rep)
    return rows, rels, probs, rep, time.time() - t
def lf_of(b, r):
    sd = SIDE.get(r["id"]) or {}
    m = r.get("meta") or {}
    if "label_form" in sd: return sd["label_form"]
    if "vocab" in sd: return sd["vocab"]
    if b == "F10" and "mode" in sd: return {"neutral": "masked", "swapped": "swapped"}.get(sd["mode"], "plain")
    return m.get("label_form")
def yb_of(r):
    sd = SIDE.get(r["id"]) or {}
    if isinstance(sd.get("yes_bad"), bool): return sd["yes_bad"]
    v = sd.get("polarity", sd.get("polarity_tag"))
    return {"bad": True, "not bad": False}.get(v)
def att_mx(r):
    m = r.get("meta") or {}
    return bool(m.get("attack_target")) or r.get("role") in ("attacked", "attack") or m.get("twin_kind") == "attack"
def att_broad(r):
    m = r.get("meta") or {}
    sd = SIDE.get(r["id"]) or {}
    return att_mx(r) or "attack" in str(m.get("twin_kind") or "").lower() or bool(sd.get("attack")) or \
        "attack" in str(r.get("role") or "").lower()
def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"
def stats(rows, ntok):
    by = defaultdict(list)
    for r in rows:
        if r["_block"] != "replay": by[r["_block"]].append(r)
    new = [r for v in by.values() for r in v]
    n, t = len(new), sum(ntok[r["id"]] for r in new)
    ln = sum(1 for r in new if ntok[r["id"]] >= 2000); lt = sum(ntok[r["id"]] for r in new if ntok[r["id"]] >= 2000)
    own = sum(len(v) for b, v in by.items() if b in cs.FAMS)
    out = {"_cap": {"new": n, "long": ln, "row_share": round(ln / n, 5), "tok_share": round(lt / t, 5),
                    "max_tok": max(ntok[r["id"]] for r in new)}, "_replay": len(rows) - n, "_own": own}
    for b, rr in sorted(by.items()):
        N = len(rr); d = {"n": N, "long": sum(1 for r in rr if ntok[r["id"]] >= 2000)}
        if b in cs.FAMS:
            ids = {r["id"]: r for r in rr}
            mem, mem_any = set(), set()
            for r in rr:
                to = (r.get("meta") or {}).get("twin_of")
                if to in ids:
                    mem_any |= {r["id"], to}
                    if str(ids[to].get("gold")) != str(r.get("gold")): mem |= {r["id"], to}
            yn = [r for r in rr if r["qtype"] == "noul"]
            ch = [r for r in rr if r["qtype"] == "choice" and r.get("options")]
            chl = [r for r in ch if lf_of(b, r) is not None]
            ybl = [r for r in yn if yb_of(r) is not None]
            negs = [cs.neg_count(r.get("instructions") or "") for r in yn]
            cards = Counter((r.get("meta") or {}).get("card_id") for r in rr)
            cw = defaultdict(set)
            for r in rr: cw[(r.get("meta") or {}).get("card_id")].add((r.get("meta") or {}).get("wording_id"))
            sh = lambda k, den: (k / den) if den else None  # noqa
            d.update(share_own=N / own, tset=sh(len(mem), N), tset_any=sh(len(mem_any), N), yn_share=sh(len(yn), N),
                     masked=sh(sum(lf_of(b, r) == "masked" for r in chl), len(chl)),
                     swapped=sh(sum(lf_of(b, r) == "swapped" for r in chl), len(chl)), lf_rows=len(chl),
                     yes_bad=sh(sum(bool(yb_of(r)) for r in ybl), len(ybl)), yb_rows=len(ybl),
                     attack_mx=sh(sum(map(att_mx, rr)), N), attack_broad=sh(sum(map(att_broad, rr)), N),
                     neg1=sh(sum(x >= 1 for x in negs), len(yn)), neg2=sh(sum(x >= 2 for x in negs), len(yn)),
                     deep=sh(sum(bool((r.get("meta") or {}).get("deep")) for r in rr), N),
                     short=sh(sum((r.get("meta") or {}).get("defs_style") in ("short", "none") for r in rr), N),
                     yes_rate=sh(sum(int(r["gold"]) for r in yn), len(yn)),
                     cards=len(cards), card_max=max(cards.values()), card_median=statistics.median(cards.values()),
                     min_w_per_card=min(len(v) for v in cw.values()),
                     wording_pool=len({(r.get("meta") or {}).get("wording_id") for r in rr}),
                     defs_styles=len({(r.get("meta") or {}).get("defs_style") for r in rr} - {None}),
                     packs=len({(r.get("meta") or {}).get("domain_pack") for r in rr} - {None}),
                     samplers=len({(r.get("meta") or {}).get("sampler") for r in rr} - {None}),
                     bins=dict(Counter((r.get("meta") or {}).get("difficulty_bin") or "na" for r in rr)),
                     g9_min_p=(min(mx.label_bin_p(rr)) if mx.label_bin_p(rr) else None))
            for k in ("2-4", "5-9", "10-19", "20-60"):
                d["opt_" + k] = sh(sum(bucket(len(r["options"])) == k for r in ch), len(ch))
        elif b == "public":
            d["by_source"] = dict(Counter(r["source"] for r in rr))
        elif b == "COMMIT":
            d["by_group"] = dict(Counter(cs.commit_group(r) for r in rr))
        out[b] = d
    return out
BANDS = {"yn_share": (0.45, 0.55), "opt_2-4": (0.32, 0.38), "opt_5-9": (0.32, 0.38), "opt_10-19": (0.12, 0.18),
         "opt_20-60": (0.12, 0.18), "neg1": (0.10, 1.0), "neg2": (0.02, 1.0), "deep": (0.0, 0.10),
         "short": (0.10, 0.20), "tset": (0.20, 0.25), "attack_mx": (0.05, 0.05), "attack_broad": (0.05, 0.05),
         "masked": (0.10, 0.15), "swapped": (0.05, 0.05), "yes_bad": (0.45, 0.55), "yes_rate": (0.48, 0.52)}
def verdict(v0, v1, band):
    lo, hi = band
    if v0 is None or v1 is None: return True
    if lo == hi: return abs(v1 - lo) <= abs(v0 - lo) + 1e-12
    ok = True
    if v1 < lo - 1e-12: ok &= v0 < lo - 1e-12 and v1 >= v0 - 1e-12
    if v1 > hi + 1e-12: ok &= v0 > hi + 1e-12 and v1 <= v0 + 1e-12
    return ok
def compare(s0, s1, targets):
    bad = []
    for b in s0:
        if b.startswith("_") or b not in cs.FAMS or b not in s1: continue
        x0, x1 = s0[b], s1[b]
        for k, band in BANDS.items():
            if k == "yn_share" and not (x0[k] is not None and 0 < x0[k] < 1): continue
            bb = {"masked": (0.40, 0.40), "swapped": (0.30, 0.30)}.get(k, band) if b == "F10" else band
            if not verdict(x0.get(k), x1.get(k), bb): bad.append(f"{b} {k} {x0.get(k):.4f}->{x1.get(k):.4f} {bb}")
        if x1["cards"] != x0["cards"]: bad.append(f"{b} cards {x0['cards']}->{x1['cards']}")
        if x1["card_max"] > max(128, x0["card_max"]): bad.append(f"{b} card_max {x1['card_max']}")
        if x1["min_w_per_card"] < min(5, x0["min_w_per_card"]): bad.append(f"{b} wordings/card {x0['min_w_per_card']}->{x1['min_w_per_card']}")
        if x1["wording_pool"] < min(30, x0["wording_pool"]): bad.append(f"{b} wording pool {x0['wording_pool']}->{x1['wording_pool']}")
        if x1["defs_styles"] < min(3, x0["defs_styles"]): bad.append(f"{b} defs {x0['defs_styles']}->{x1['defs_styles']}")
        if x1["packs"] < min(30, x0["packs"]): bad.append(f"{b} packs {x0['packs']}->{x1['packs']}")
        if x1["samplers"] < x0["samplers"]: bad.append(f"{b} samplers {x0['samplers']}->{x1['samplers']}")
        bn0, bn1 = x0["bins"], x1["bins"]
        if any(k in bn0 for k in ("easy", "medium", "hard")):
            for k, lo, hi in (("easy", 0, .25), ("medium", .45, 1), ("hard", 0, .30)):
                if not verdict(bn0.get(k, 0) / x0["n"], bn1.get(k, 0) / x1["n"], (lo, hi)): bad.append(f"{b} bin {k}")
        if x1["g9_min_p"] is not None and x1["g9_min_p"] <= 0.01 and (x0["g9_min_p"] is None or x0["g9_min_p"] > 0.01 or x1["g9_min_p"] < x0["g9_min_p"]):
            bad.append(f"{b} G9 p {x0['g9_min_p']}->{x1['g9_min_p']}")
        if x1["n"] > math.floor(1.5 * targets.get(b, 0)): bad.append(f"{b} > 1.5x target {x1['n']}")
        if x1["share_own"] > max(0.12, x0["share_own"]) + 1e-9: bad.append(f"{b} own share {x0['share_own']:.4f}->{x1['share_own']:.4f}")
    for b in ("public", "COMMIT"):
        k = "by_source" if b == "public" else "by_group"
        if b in s0 and s0[b].get(k) != s1.get(b, {}).get(k): bad.append(f"{b} {k} changed")
    return bad
s0 = stats(CAP["rows"], CAP["ntok"])
rows1, rels1, probs1, rep1, dt1 = run()
s1 = stats(rows1, CAP["ntok"])
ids1 = [r["id"] for r in rows1]
before_ids = {r["id"] for r in CAP["rows"]}
added = [r for r in rows1 if r["id"] not in before_ids]
rows2, _, _, rep2, dt2 = run()
ids2 = [r["id"] for r in rows2]
sha = lambda x: hashlib.sha256(json.dumps(x).encode()).hexdigest()[:16]  # noqa
a = rep1["a28_cap"]
res = {"tag": TAG, "hashseed": HS, "capture_s": round(cap_t), "trim_s": [round(dt1), round(dt2)],
       "ids_sha": [sha(ids1), sha(ids2)], "ids_set_sha": sha(sorted(ids1)), "deterministic_in_process": ids1 == ids2,
       "rep_equal": json.dumps(rep1, sort_keys=True, default=str) == json.dumps(rep2, sort_keys=True, default=str),
       "cap_before": s0["_cap"], "cap_after": s1["_cap"], "replay": [s0["_replay"], s1["_replay"]],
       "own": [s0["_own"], s1["_own"]], "added_rows": len(added),
       "added_max_tok": max((CAP["ntok"][r["id"]] for r in added), default=0),
       "problems": [p[:300] for p in probs1], "audit_count": a.get("guard_audit_break_count"),
       "remainder": a.get("remainder_rows"), "replay_cut": a.get("replay_cut"),
       "trims": {b: {k: t[k] for k in ("dropped_rows", "swapped_out_rows", "rows_before", "rows_lost_pct", "stuck_moves")} for b, t in a.get("trims_by_block", {}).items()},
       "refilled": a.get("refilled_rows_by_family"), "my_breaks": compare(s0, s1, CAP["targets"]),
       "targets": CAP["targets"], "before": s0, "after": s1}
(R / f"res_{TAG}_{HS}.json").write_text(json.dumps(res, default=str, indent=1))
print("DONE", TAG, HS, round(time.time() - t0))
