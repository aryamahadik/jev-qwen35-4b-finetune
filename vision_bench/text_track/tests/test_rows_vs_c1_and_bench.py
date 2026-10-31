import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
"""Rows, views and options for ALL 4,850 decisions equal C1's own code (lean/jevbench_od.py to_row/state_text, fastcore readout
views_for) and the bench's own helpers (score.py options/gold_idx). Nothing in lean/ or the bench is edited or written."""
import ast, json, sys, types
from common import *
import tt_core as tt
# --- C1's to_row / state_text, taken from the source text of lean/jevbench_od.py
src = open(f"{LEAN}/jevbench_od.py").read()
tree = ast.parse(src)
ns = {"json": json}
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("state_text", "to_row"):
        exec(compile(ast.Module([n], []), "jevbench_od", "exec"), ns)
# --- fastcore views_for (A5 2view)
src2 = open(f"{LEAN}/hosting/fastcore/readout.py").read()
ns2 = {}
for n in ast.parse(src2).body:
    if isinstance(n, ast.FunctionDef) and n.name == "views_for":
        exec(compile(ast.Module([n], []), "readout", "exec"), ns2)
# --- the bench's score.py helpers
sys.path.insert(0, BENCH)
import score as bench_score
ds = tt.load_decisions()
assert len(ds) == 4850
n = 0
for d in ds:
    q = d["q"]
    task = types.SimpleNamespace(question=q, state=json.loads(d["state"]) if d["state"].startswith(("{", "[")) else d["state"])
    row_c1, keys_c1 = ns["to_row"](task)
    row, keys = tt.to_row(q, d["state"])
    assert row == row_c1 and keys == keys_c1, d["id"]
    assert ns["state_text"](task.state) == d["state"]
    assert tt.views_for(row) == ns2["views_for"](row, 2), d["id"]
    assert tt.bench_options(q) == bench_score.options(q)
    case_gold = None
    n += 1
cases = {c["id"]: c for c in (json.loads(l) for l in open(tt.data_path(), encoding="utf-8"))}
for d in ds:
    c = cases[d["id"]]
    assert d["gold"] == bench_score.gold_idx(c["questions"][d["qid"]], c["gold"][d["qid"]]), d["id"]
# bench answer format round trip through the bench's own pred_dist
import random
for d in random.Random(0).sample(ds, 400):
    q = d["q"]; k = len(bench_score.options(q))
    p = [random.random() for _ in range(k)]; s = sum(p); p = [x / s for x in p]
    dist, ok = bench_score.pred_dist(q, tt.bench_answer(q, p))
    assert ok and max(abs(a - b) for a, b in zip(dist, p)) < 1e-9, d["id"]
# diagnostic variant: bare criteria strings differ ONLY in the option text of score rows
sc = [d for d in ds if d["q"]["type"] == "score"]
assert len(sc) == 1000
r1, _ = tt.to_row(sc[0]["q"], sc[0]["state"], True); r2, _ = tt.to_row(sc[0]["q"], sc[0]["state"], False)
assert r1["options"] == [f"{i}: {o}" for i, o in enumerate(r2["options"])] and r2["options"] == [str(x) for x in sc[0]["q"]["criteria"]]
print(f"ROWS/VIEWS/OPTIONS/GOLD IDENTICAL for {n} decisions; score items {len(sc)}; noul {sum(d['q']['type']=='noul' for d in ds)}; choice {sum(d['q']['type']=='choice' for d in ds)}")
print("ROWS TEST PASSED")
