"""OHS-1 core: merge the held-out parts (ohs/build_*.py -> data/ohs_parts/*.jsonl), validate, decontaminate against
everything we trained or selected on, add the consistency layer (ohs/variants.py), split into an open half (OHS-A,
items may be inspected) and a sealed half (OHS-S, aggregates only), then freeze: data/ohs.jsonl, ohs_relations.jsonl,
ohs_calls.jsonl and ohs.sha256. Commit these BEFORE any model is run on them (see PREREG_OHS.md).
  python build_ohs.py
"""
import glob
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
sys.path.insert(0, str(HERE / "ohs"))
rj = lambda p: [json.loads(l) for l in open(p)]
words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
TOUCHED = ["train_v07", "lah_train", "lah_train_unverified", "judge_train", "debate_train", "debate_dev", "ohr_train", "pg_train",
           "pg_dev", "inj_v2", "meta_pos", "meta_neg", "dev", "devzs", "devzs2", "devp", "devp_card", "eval", "eval_card",
           "eval_jagged", "eval_opi", "eval_long", "eval_multi"]


def grams(text, n=12):
    w = words(text)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def main():
    rows, rels = [], []
    for f in sorted(glob.glob(str(D / "ohs_parts/*.jsonl"))):
        if f.endswith("_relations.jsonl"):
            rels += rj(f)
        else:
            rows += rj(f)
    # validate
    ids = Counter(r["id"] for r in rows)
    assert not [i for i, c in ids.items() if c > 1], "duplicate ids"
    by_call = defaultdict(set)
    for r in rows:
        assert r["qtype"] in ("choice", "noul"), r["id"]
        if r["qtype"] == "choice":
            assert r["gold"] in r["options"] and len(set(r["options"])) == len(r["options"]) and 2 <= len(r["options"]) <= 255, r["id"]
        else:
            assert r["gold"] in (0, 1) and r["options"] is None, r["id"]
        by_call[r["call_id"]].add(r["state"])
    assert all(len(s) == 1 for s in by_call.values()), "a call_id spans different states"
    # decontaminate: drop any group whose text appears in, or shares a 12-word run with, anything we touched
    touched_text, touched_grams = set(), set()
    for name in TOUCHED:
        p = D / f"{name}.jsonl"
        if p.exists():
            for x in rj(p):
                t = x.get("state") or x.get("text") or ""
                touched_text.add(" ".join(words(t)))
                touched_grams |= grams(t)
    bad_groups = {r["group_id"] for r in rows if " ".join(words(r["state"])) in touched_text or (grams(r["state"]) & touched_grams)}
    dropped = sum(r["group_id"] in bad_groups for r in rows)
    rows = [r for r in rows if r["group_id"] not in bad_groups]
    keep = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in keep and x["b"] in keep]
    # consistency layer (new wordings, never used in train/dev/eval)
    n_var = 0
    try:
        import variants
        pick = lambda r: int(hashlib.sha256(("var:" + r["group_id"]).encode()).hexdigest(), 16) % 5 == 0
        base = [r for r in rows if r.get("role") == "aff" or (r.get("role") == "choice" and pick(r))]  # all yes/no, 1 in 5 choice
        new_rows, new_rels = variants.make_variants(base)
        rows += new_rows
        rels += new_rels
        n_var = len(new_rows)
    except ImportError:
        print("ohs/variants.py missing: no consistency layer")
    # open / sealed halves by group hash
    for r in rows:
        h = int(hashlib.sha256(("ohs1:" + r["group_id"]).encode()).hexdigest(), 16)
        r.setdefault("meta", {})["half"] = "A" if h % 2 == 0 else "S"
    calls = {}
    for r in rows:
        calls.setdefault(r["call_id"], {"call_id": r["call_id"], "state": r["state"], "row_ids": []})["row_ids"].append(r["id"])
    files = {"ohs.jsonl": rows, "ohs_relations.jsonl": rels, "ohs_calls.jsonl": list(calls.values())}
    digest = []
    for name, items in files.items():
        text = "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in items)
        (D / name).write_text(text)
        digest.append(f"{hashlib.sha256(text.encode()).hexdigest()}  {name}")
    (D / "ohs.sha256").write_text("\n".join(digest) + "\n")
    summ = {"rows": len(rows), "base_rows": len(rows) - n_var, "variant_rows": n_var, "relations": len(rels), "calls": len(calls),
            "dropped_for_overlap": dropped, "by_source": dict(Counter(r["source"] for r in rows)),
            "by_track": dict(Counter(r["track"] for r in rows)), "halves": dict(Counter(r["meta"]["half"] for r in rows)),
            "max_options": max(len(r["options"] or []) for r in rows)}
    (D / "ohs_summary.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
