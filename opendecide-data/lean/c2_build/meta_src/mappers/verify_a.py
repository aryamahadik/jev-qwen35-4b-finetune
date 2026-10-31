"""verify_a.py: solver B for the numeric-threshold tasks. Parses the field value out of the RENDERED state and the threshold out of
the question, then re-derives gold (independent of the task lambdas). Prints per-source agreement."""
import importlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
LEAN = Path(__file__).resolve().parents[3]
SKIP = ("pages", "dist", "title", "span", "stations_ge", "_gt_", "ch_", "_c_")
tot = bad = 0
for name in ("openalex", "musicbrainz", "worldbank", "usgs"):
    m = importlib.import_module(name)
    recs = {m.rid_of(r): r for r in m.load()}
    rows = [json.loads(l) for l in open(LEAN / "data/c2_md_parts" / name / "rows.jsonl")]
    n = b = 0
    for r in rows:
        tid = r["meta"]["task_id"].split(":", 1)[1]
        if "_ge_" not in tid or any(s in tid for s in SKIP) or r["qtype"] != "noul":
            continue
        F = m.fields_of(recs[r["meta"]["record_id"]])
        task = [t for t in m.tasks() if t.tid == tid][0] if False else None
        key = None
        # the needed key is gold_field
        key = r["meta"]["gold_field"].split(",")[0]
        lab = F[key][0]
        mm = re.search(r'(?<![\w])(?:"%s"|%s|%s)(?:: | = | \| | )"?(-?\d+(?:\.\d+)?)' % (re.escape(key), re.escape(key), re.escape(lab)), r["state"])
        if not mm:
            print("PARSE FAIL", tid, r["state"][:200]); b += 1; continue
        val = float(mm.group(1))
        thr = float(re.search(r"(\d+(?:\.\d+)?)", r["instructions"]).group(1))
        neg = r["meta"]["polarity"] == -1
        exp = (val >= thr) != neg
        n += 1
        if int(exp) != r["gold"]:
            b += 1; print("MISMATCH", tid, val, thr, neg, r["gold"])
    print(name, "checked", n, "bad", b); tot += n; bad += b
print("TOTAL", tot, "BAD", bad)
