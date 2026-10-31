"""Tests for merge_md.py (noise gate, caps) on a temporary copy of one source part. Run:
   .venv/bin/python -B meta_src/test_merge_md_c.py"""
import json, shutil, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import merge_md as M
from c2_kit import g5h

def main():
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(M.PARTS / "md_cma", tmp / "md_cma")
    M.PARTS = tmp
    srcs, _ = M.load_sources()
    s = srcs["md_cma"]
    key = {}
    for k in (tmp / "md_cma/noise_gate/key").glob("MD_*.json"):
        key.update(json.loads(k.read_text())["key"])
    byid = {r["id"]: r for r in s["all_rows"]}
    victim = sorted({r["meta"]["task_id"] for r in s["rows"]})[3]
    flipped = 0
    ans = {}
    for qid, rid in key.items():
        r = byid[rid]; it = g5h.read_item(r)
        right = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
        a = right
        if r["meta"]["task_id"] == victim and flipped < 2 and not r["meta"].get("twin_of"):
            flipped += 1
            a = ("no" if right == "yes" else "yes") if r["qtype"] == "noul" else [o for o in r["options"] if o != right][0]
        ans[qid] = {"answer": a, "confidence": 0.9}
    (tmp / "md_cma/noise_gate/answers/all.json").write_text(json.dumps({"t": ans}))
    drop, rep = M.gate_source("md_cma", s)
    assert drop == {victim}, (drop, rep)
    assert rep["status"] == "complete" and rep["answers"] == len(key), rep
    assert M.gate_source("md_cma", s, 0.95)[0] == set()          # A51 (a): answers at confidence 0.9 are below a 0.95 bar
    assert M.CLEAR_CONF == 0.7
    # one wrong answer only: kept
    (tmp / "md_cma/noise_gate/answers/all.json").write_text(json.dumps({"t": {q: (dict(a, answer=("no" if a["answer"] == "yes" else "yes")) if i == 0 and a["answer"] in ("yes", "no") else a) for i, (q, a) in enumerate(ans.items())}}))
    drop2, _ = M.gate_source("md_cma", s)
    assert len(drop2) <= 1
    # caps: source a full (59 tasks), seven more sources of 45 tasks each, one domain each: a is above 15% and is trimmed
    rows = []
    tids = sorted({r["meta"]["task_id"] for r in s["rows"]})
    for n in "abcdefgh":
        keep = set(tids if n == "a" else tids[:45])
        for r in s["rows"]:
            if r["meta"]["task_id"] not in keep:
                continue
            r2 = json.loads(json.dumps(r)); r2["id"] += n; r2["source"] = f"s_{n}"; r2["meta"]["task_id"] += n; r2["meta"]["domain"] = "d_" + n
            r2["meta"]["twin_of"] = (r2["meta"]["twin_of"] + n) if r2["meta"]["twin_of"] else None
            rows.append(r2)
    steps = []
    out, _ = M.fit(rows, [], steps)
    n = len(out)
    assert not any(x.get("unfixable") for x in steps), steps
    assert sum(1 for r in out if r["source"] == "s_a") <= 0.15 * n + 1, steps
    assert len({r["meta"]["task_id"] for r in out if r["source"] == "s_a"}) >= 40
    print("ok", len(rows), "->", len(out), steps[:3])

main()
