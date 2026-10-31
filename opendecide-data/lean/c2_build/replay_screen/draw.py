"""replay_screen/draw.py: runs c_build/replay_sample.py (read-only, unchanged) in-process with the C2 seed and captures
the exact draw, writing nothing into c_build/.

How: the sampler's main() is called with --dry-run. Its module globals HERE / LOG are pointed at replay_screen/pool/
(so its dry-run report, the deny-list query copy and the log land there, never in c_build/), SEED is set to the C2 seed
(c2io.SEED = 20261013, A37 i), and summarize / draw_old_slice / quotas are wrapped to capture the rows, the relation
units, the eligible-pool unit list and the final E2-restratified draw. The deny-list verdicts are the real round-1 file
(same golden_train pool, as mix_c2.REPLAY['verdicts']).

  nice -n 10 ../../../.venv/bin/python -B draw.py --r1 75000 --r2 150000

Output: pool/draw_<r1>.json (ids of the draw, per-source counts, eligible counts, sampler report path).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
POOL = HERE / "pool"
C2_SEED = 20261013          # c2io.SEED (A37 i) = the A46 provisional-draw seed
POOL_DROPS_R1 = LEAN / "logs/decontam_counts/pool_drops_r1.json"
VERDICTS = LEAN / "c_build/replay_denylist_verdicts.json"


def capture_draw(r1: int, r2: int, seed: int = C2_SEED, margin: float = 0.10, old_slice: int = 2000) -> dict:
    sys.path.insert(0, str(LEAN / "c_build"))
    sys.path.insert(0, str(LEAN))
    import replay_sample as rs
    POOL.mkdir(parents=True, exist_ok=True)
    rs.SEED = seed
    rs.HERE = POOL
    rs.LOG = POOL / "progress_prep.log"
    cap = {"summ": {}, "quotas": [], "live": None, "old": None}

    orig_sum, orig_old, orig_q = rs.summarize, rs.draw_old_slice, rs.quotas

    def summ(rows, units, sel, name):
        cap["rows"], cap["units"] = rows, units
        cap["summ"][name.split()[0] + name.split()[1]] = set(sel)
        return orig_sum(rows, units, sel, name)

    def old(rows, units, live, q2, size=2000):
        cap["live"] = list(live)
        cap["rows"], cap["units"] = rows, units
        out = orig_old(rows, units, live, q2, size)
        cap["old"] = list(out)
        return out

    def quotas(n, total, *a, **k):
        cap["quotas"].append(dict(n))
        return orig_q(n, total, *a, **k)

    rs.summarize, rs.draw_old_slice, rs.quotas = summ, old, quotas
    argv = ["--dry-run", "--r1", str(r1), "--r2", str(r2), "--margin", str(margin), "--old-slice", str(old_slice),
            "--denylist-verdicts", str(VERDICTS)]
    t = time.time()
    rep = rs.main(argv)
    rows, units = cap["rows"], cap["units"]
    sel1 = cap["summ"]["round1"]
    sel2 = cap["summ"]["round2"]
    ids1 = sorted(rows[i]["id"] for ui in sel1 for i in units[ui]["rows"])
    ids2 = sorted(rows[i]["id"] for ui in sel2 for i in units[ui]["rows"])
    live_ids = sorted(rows[i]["id"] for ui in cap["live"] for i in units[ui]["rows"])
    old_ids = sorted(rows[i]["id"] for i in cap["old"])
    src = lambda ids, idx: Counter(idx[i] for i in ids)  # noqa: E731
    sidx = {r["id"]: r["source"] for r in rows}
    drops = set(json.loads(POOL_DROPS_R1.read_text())["drop_ids"])
    # relation units of the draw (whole units drop together); units holding a pool_drops_r1 id leave the replay in the
    # mixer (G13 drop list), so they are listed apart and kept out of the screening population
    unit_of = {rows[i]["id"]: units[ui]["id"] for ui in sel1 for i in units[ui]["rows"]}
    pool_drop_units = sorted({units[ui]["id"] for ui in sel1 if any(rows[i]["id"] in drops for i in units[ui]["rows"])})
    out = {
        "seed": seed, "r1": r1, "r2": r2, "margin": margin, "sampler_sec": round(time.time() - t),
        "sampler_sha256": rep.get("write", {}).get("sampler_sha256"),
        "eligible_before_old_slice": rep["eligible_before_old_slice"], "eligible": rep["eligible"],
        "quota": rep["quota"], "old_slice_ids": old_ids,
        "pool_drops_r1_in_draw": sum(i in drops for i in ids1),
        "eligible_by_source_before_old_slice": dict(src(live_ids, sidx)),
        "eligible_by_source": cap["quotas"][-1],
        "unit_of": unit_of, "pool_drop_units_in_draw": pool_drop_units,
        "draw_r1_by_source": dict(src(ids1, sidx)), "draw_r2_by_source": dict(src(ids2, sidx)),
        "draw_r1_ids": ids1, "draw_r2_ids_count": len(ids2),
        "eligible_ids_count": len(live_ids),
    }
    out["eligible_ids"] = live_ids
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--r1", type=int, default=75000)
    ap.add_argument("--r2", type=int, default=150000)
    ap.add_argument("--seed", type=int, default=C2_SEED)
    a = ap.parse_args()
    res = capture_draw(a.r1, a.r2, a.seed)
    p = POOL / f"draw_{a.r1}.json"
    p.write_text(json.dumps(res))
    print("wrote", p, "draw r1 rows", len(res["draw_r1_ids"]), "eligible", res["eligible"])
