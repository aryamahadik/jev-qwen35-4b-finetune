"""G8 (AFLite-lite, G8v3 rule, c_src/common/g8_aflite.py unchanged) for the GW wave-2 types: the GW adapter.

c_src/common/g8_aflite.py has F1-F6 adapters only and is pinned, so this wrapper imports it, registers one adapter per GW type and
redirects its output / cache folders to c2_build/gblock/g8_gw (nothing is written under lean/c_build or c_src). Row text, label
and options are used exactly as the F-family adapters do (instructions split into question sentence(s) + rest; card text +
rest; state; options); gold is the qtype's gold. The only GW-specific part is the held-out unit ("card" in the G8 split):
GW rows share one answer card per type, so the 50/50 partition is made by authoring unit instead:
    W1 W3 W4 W7 W8 : meta.wave2.haiku_task_id (the Haiku authoring task: 10-24 units per type)
    W2 : text_id (source passage)   W6 : repo   (no authoring task; units of source text)
The unit is written into meta.card_id of a COPY of the pool (candidates are untouched).

    python -B gblock/tools/gw_g8.py run W1 [--jobs 3]       (from c2_build)
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

CB = Path(__file__).resolve().parents[2]
LEAN = CB.parent
sys.path.insert(0, str(LEAN / "c_src" / "common"))
import g8_aflite as G  # noqa: E402

WORK = CB / "gblock" / "g8_gw"
UNIT = {"W1": "haiku_task_id", "W3": "haiku_task_id", "W4": "haiku_task_id", "W7": "haiku_task_id", "W8": "haiku_task_id",
        "W2": "text_id", "W6": "repo"}
G.OUTDIR = WORK
G.CACHE = WORK / "cache"
for i, t in enumerate(UNIT):
    fam = "GW_" + t
    G.ADAPTERS[fam] = dict(G._BASE, split="sent", chunk_q=True, seed0=20261013 + 1000 * i, yn_bal=True)
    G.FAMILY_G8[fam] = WORK / "no_family_g8.json"  # none exists: reproduction check is skipped


def make_pool(t: str) -> Path:
    rows = [json.loads(l) for l in (LEAN / "data/c2_parts/GW/out/candidates_c2.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r["meta"]["wave2"]["type"] == t]
    for r in rows:
        r["meta"]["card_id"] = f"{t}:{r['meta']['wave2'][UNIT[t]]}"
    p = WORK / "pools" / f"GW_{t}.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return p


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("types", nargs="+")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    G.CACHE.mkdir(parents=True, exist_ok=True)
    for t in a.types:
        pool = make_pool(t)
        rep = G.family_report("GW_" + t, pool, WORK / f"GW_{t}.json", a.jobs)
        print(t, "pass", rep["pass"], {p: (d["test"]["verdict"], d["test"]["p"], d["real"]["share"]) for p, d in rep["parts"].items()},
              "raw_share_seed0", rep["old_rule"]["raw_share_all_rows_seed0"], flush=True)
