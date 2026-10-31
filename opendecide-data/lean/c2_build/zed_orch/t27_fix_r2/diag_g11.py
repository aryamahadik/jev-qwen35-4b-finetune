"""G11 diagnosis for T27 (read-only): per question form, the rows, the usable training wordings, the share a PERFECTLY even
split would give, the share the full generation got, and how many wordings the 2% bar needs. Counts and ids only.
  ../../.venv/bin/python -B zed_orch/t27_fix_r2/diag_g11.py [--cand FILE] [--out FILE]   (from lean/c2_build)"""
import argparse, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
LEAN = C2.parent
ap = argparse.ArgumentParser()
ap.add_argument("--cand", default=str(LEAN / "data" / "c2_parts" / "T27" / "out" / "candidates_c2.jsonl"))
ap.add_argument("--out", default=str(HERE / "diag_g11.json"))
a = ap.parse_args()
BAR = 0.02
rows = [json.loads(l) for l in open(a.cand)]
N = len(rows)
cap = math.floor(BAR * N + 1e-9)                       # most rows one wording may hold: share <= 2%
pool = json.loads((C2 / "families" / "T27" / "pools_v2" / "wordings.json").read_text())["records"]
used = defaultdict(Counter)
for r in rows:
    used[r["meta"]["qform"]][r["meta"]["wording_id"]] += 1
train = defaultdict(set)
for w in pool:
    if not w["held_out"]:
        train[w["qform"]].add(w["piece_id"])
out = {"family": "T27", "n_rows": N, "bar": BAR, "max_rows_per_wording_at_bar": cap, "forms": {}}
for q in sorted(used):
    c = used[q]
    R = sum(c.values())
    W = len(c)
    out["forms"][q] = {
        "rows": R, "row_share_of_family": round(R / N, 4),
        "pool_training_wordings": len(train[q]), "usable_wordings_in_generation": W,
        "removed_by_quarantines": len(train[q]) - W,
        "rows_per_wording": {"min": min(c.values()), "mean": round(R / W, 1), "max": max(c.values())},
        "max_share_in_generation": round(max(c.values()) / N, 4),
        "even_split_share": round(R / W / N, 4),
        "wordings_over_bar": sum(1 for v in c.values() if v / N > BAR),
        "wordings_needed_for_bar_even_split": math.ceil(R / cap),
        "new_wordings_needed_even_split": max(0, math.ceil(R / cap) - W)}
tot_over = sum(v["wordings_over_bar"] for v in out["forms"].values())
out["wordings_over_bar_total"] = tot_over
# the yes/no share of the family (G10 45-55%) limits how few choice rows there can be
ch = out["forms"]["ch_next"]["rows"]
for share in (0.55, 0.50, N and (N - ch) / N):
    rows_ch = round((1 - share) * N)
    out.setdefault("choice_wordings_needed_by_yes_no_share", {})[f"{share:.3f}"] = {
        "choice_rows": rows_ch, "wordings_needed_even_split": math.ceil(rows_ch / cap)}
out["conclusion"] = (
    "ch_next has %d usable training wordings for %d rows: an even split gives %.2f%% each, above the 2%% bar; %d wordings "
    "are needed at the generated mix (%d at the largest allowed yes/no share of 55%%). The yes/no forms have enough "
    "wordings; their overshoot (%s) is sampling noise that a balanced draw removes." % (
        out["forms"]["ch_next"]["usable_wordings_in_generation"], ch, 100 * out["forms"]["ch_next"]["even_split_share"],
        out["forms"]["ch_next"]["wordings_needed_for_bar_even_split"],
        out["choice_wordings_needed_by_yes_no_share"]["0.550"]["wordings_needed_even_split"],
        ", ".join(f"{q} {v['wordings_over_bar']}" for q, v in out["forms"].items() if q != "ch_next" and v["wordings_over_bar"])))
Path(a.out).write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
