"""Gentler AFLite drops (16 Oct 2026): per round drop only the most predictable 12% of rows (pooled held-out accuracy score, ties seeded),
rebalance yes/no classes by seeded down-sampling, stop at G8v3 pass or < 300 rows. Drops only. Output gblock/g8_gw/aflg_<T>.json."""
import argparse, json, random, sys
from pathlib import Path
import numpy as np
CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB / "gblock" / "tools"))
import gw_aflite_drop as D  # noqa: E402
W, G = D.W, D.G
FRAC, MIN_ROWS, SEED, MAX_R = 0.12, 300, 20261013, 20


def scores(fam, pool, jobs):
    rows, sha, store, views, _ = G.embed_family(fam, pool)
    feats, cards, _ = G.features(fam, rows, views, store)
    s0 = G.ADAPTERS[fam]["seed0"]
    specs = [("base", part, "real", 0, s0 + 100000 * s) for s in range(4) for part in feats]
    acc = G.run_specs_batch(fam, {"base": feats}, cards, specs, jobs)
    sc = np.zeros(len(rows))
    for part, F in feats.items():
        rd = np.zeros(len(F["rows"])); rt = np.zeros(len(F["rows"]))
        for s in range(4):
            r, w = acc[("base", part, "real", 0, s0 + 100000 * s)]
            rd += r; rt += w
        sc[F["rows"]] = np.divide(rt, rd, out=np.zeros_like(rt), where=rd > 0)
    return sc


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("type"); ap.add_argument("--jobs", type=int, default=3); a = ap.parse_args()
    t = a.type; fam = "GW_" + t; rng = random.Random(f"{SEED}:aflg:{t}"); log = []
    G.CACHE.mkdir(parents=True, exist_ok=True)
    pool = W.make_pool(t); rows = [json.loads(l) for l in pool.open(encoding="utf-8")]
    ok = False
    for rd in range(MAX_R):
        pool.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        rep = G.family_report(fam, pool, W.WORK / f"GW_{t}.json", a.jobs)
        gp = {p: (d["test"]["verdict"], d["test"]["p"], d["real"]["share"]) for p, d in rep["parts"].items()}
        log.append({"round": rd, "rows": len(rows), "g8v3_pass": bool(rep["pass"]), "g8v3": gp})
        print(t, log[-1], flush=True)
        if rep["pass"]:
            ok = True; break
        sc = scores(fam, pool, a.jobs)
        order = sorted(range(len(rows)), key=lambda i: (-sc[i], rng.random()))
        dr = set(order[: max(1, int(FRAC * len(rows)))])
        keep = [r for i, r in enumerate(rows) if i not in dr]
        if rows[0]["qtype"] == "noul":
            by = {0: [], 1: []}
            for i, r in enumerate(keep):
                by[int(r["gold"])].append(i)
            big = 0 if len(by[0]) > len(by[1]) else 1
            dd = set(rng.sample(by[big], len(by[big]) - len(by[1 - big])))
            keep = [r for i, r in enumerate(keep) if i not in dd]
        rows = keep
        if len(rows) < MIN_ROWS:
            log.append({"round": rd + 1, "rows": len(rows), "note": "below 300 rows"}); break
    (G.OUTDIR / f"aflg_{t}.json").write_text(json.dumps({"type": t, "ok": ok, "rows": len(rows), "log": log,
                                                        "kept_ids": [r["id"] for r in rows] if ok else []}, indent=1))
    print(t, "ok" if ok else "OUT", len(rows))
