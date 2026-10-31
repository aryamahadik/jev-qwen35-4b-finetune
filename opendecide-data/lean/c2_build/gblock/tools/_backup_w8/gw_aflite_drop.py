"""AFLite drops for a GW type that fails G8 (< 10% predictable): drops only, seeded, never a relabel (16 Oct 2026).

Each round: G8v3 row predictability on the current rows (4 partition seeds x 64 partitions, tau 0.75, >= 8 pooled reads, grouped
by the GW unit as in gw_g8.py); every predictable row is dropped; yes/no gold classes are then down-sampled to equal size (seeded).
Stops when the mean per-seed predictable share is < TARGET, or the type falls below 300 rows (the type leaves GW).
Writes gblock/g8_gw/afl_<T>.json with the kept ids and the round log.   python -B gblock/tools/gw_aflite_drop.py W3 [--jobs 2]
"""
import argparse, json, random, sys
from pathlib import Path
import numpy as np
CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB / "gblock" / "tools"))
import gw_g8 as W  # noqa: E402  (registers adapters, redirects G8 output folders)
G = W.G
TARGET, MIN_ROWS, SEED, MAX_R = 0.08, 300, 20261013, 12


def predictable(fam, pool, jobs):
    rows, sha, store, views, _ = G.embed_family(fam, pool)
    feats, cards, _ = G.features(fam, rows, views, store)
    s0 = G.ADAPTERS[fam]["seed0"]
    specs = [("base", part, "real", 0, s0 + 100000 * s) for s in range(4) for part in feats]
    acc = G.run_specs_batch(fam, {"base": feats}, cards, specs, jobs)
    flag = np.zeros(len(rows), bool); shares = []
    for part, F in feats.items():
        rd = np.zeros(len(F["rows"])); rt = np.zeros(len(F["rows"]))
        for s in range(4):
            r, w = acc[("base", part, "real", 0, s0 + 100000 * s)]
            rd += r; rt += w
            shares.append(float(((np.divide(w, r, out=np.zeros_like(w), where=r > 0) >= G.TAU) & (r >= G.MIN_READS)).mean()))
        pred = (np.divide(rt, rd, out=np.zeros_like(rt), where=rd > 0) >= G.TAU) & (rd >= 4 * G.MIN_READS / 4)
        flag[F["rows"][pred]] = True
    return rows, flag, float(np.mean(shares))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("type"); ap.add_argument("--jobs", type=int, default=2); a = ap.parse_args()
    t = a.type; fam = "GW_" + t; rng = random.Random(f"{SEED}:aflite:{t}"); log = []
    G.CACHE.mkdir(parents=True, exist_ok=True)
    pool = W.make_pool(t); rows = [json.loads(l) for l in pool.open(encoding="utf-8")]
    for rd in range(MAX_R):
        pool.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        rs, flag, share = predictable(fam, pool, a.jobs)
        log.append({"round": rd, "rows": len(rows), "mean_seed_share": round(share, 4), "predictable_rows": int(flag.sum())})
        print(t, log[-1], flush=True)
        if share < TARGET or len(rows) < MIN_ROWS:
            break
        keep = [r for r, f in zip(rows, flag) if not f]
        if rows[0]["qtype"] == "noul":
            by = {0: [], 1: []}
            for i, r in enumerate(keep):
                by[int(r["gold"])].append(i)
            big = 0 if len(by[0]) > len(by[1]) else 1
            dr = set(rng.sample(by[big], len(by[big]) - len(by[1 - big])))
            keep = [r for i, r in enumerate(keep) if i not in dr]
        rows = keep
        if len(rows) < MIN_ROWS:
            log.append({"round": rd + 1, "rows": len(rows), "note": "below 300 rows"}); break
    ok = len(rows) >= MIN_ROWS and log[-1].get("mean_seed_share", 1) < TARGET
    (G.OUTDIR / f"afl_{t}.json").write_text(json.dumps({"type": t, "ok": ok, "rows": len(rows), "log": log,
                                                       "kept_ids": [r["id"] for r in rows] if ok else []}, indent=1))
    print(t, "ok" if ok else "OUT", len(rows))
