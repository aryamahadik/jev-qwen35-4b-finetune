"""Dev copy of the HC (high-cardinality) slice for choosing the shortlist embedder and K without touching eval.

States are the 150 dev.jsonl states (train-split Banking77/CLINC150 items never used in train or eval),
with the same three option-set sizes as eval_hc. Writes data/dev_hc.jsonl + data/dev_hc_calls.jsonl.
"""
import json

from build_data import NONE_TRAIN, OUT, Builder, load_keys, rng
from build_weakness_eval import LEVELS, product_labels, write

dev = [json.loads(l) for l in open(OUT / "dev.jsonl")]
core = [r for r in dev if r["qtype"] == "choice"]
keys = {ds: [v["key"] for v in load_keys(ds).values() if v.get("kind") == "intent"] for ds in ("banking77", "clinc150")}
distract, _ = product_labels(keys["banking77"] + keys["clinc150"])
H = Builder("dev_hc")
for r in core:
    full = keys[r["source"]] + [NONE_TRAIN]
    assert r["gold"] in full
    for lev in LEVELS:
        rr = rng("dev_hc", r["id"], lev)
        opts = list(full) if lev == "full" else list(full) + rr.sample(distract, lev - len(full))
        rr.shuffle(opts)
        H.row(group=r["group_id"], state=r["state"], source=r["source"], track="HC", qtype="choice",
              instructions=r["instructions"], options=opts, gold=r["gold"], role="choice",
              meta={"level": str(lev), "n_options": len(opts), "clean_id": r["id"]})
for row in H.rows:
    row["id"] = row["id"] + "_" + row["meta"]["level"]
    row["call_id"] = row["call_id"] + "_" + row["meta"]["level"]
assert len({row["id"] for row in H.rows}) == len(H.rows)
print("dev_hc:", write("dev_hc", H))
