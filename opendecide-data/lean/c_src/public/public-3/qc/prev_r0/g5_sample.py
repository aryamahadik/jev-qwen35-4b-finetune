#!/usr/bin/env python3
"""G5 blind read sample for public-3 (independent checker, prep5/B4). Spec 8 G5: public rows get a dataset-level
read of 100 rows per dataset (no SQuAD 2.0 here), flag-only: the reader never sets, edits or chooses a label; drop
the dataset if > 8% are clearly wrong.
Own seeded draw (seed below), not the builder's out/public3_g5_sample_ids.json (that file is only checked: ids exist
in the current mixed files, 100 per dataset). Sample frame: rows_r1 + reserve; stratified per dataset by
(qtype, k, gold) with largest-remainder allocation, rows ordered by sha256(seed|id) inside a stratum.
Each row is rendered exactly as the model sees it: decoder_io.user_msg (pinned A16 readout, STYLE / LAYOUT of runs/q35_4b_c_r1.json)
under a seeded random option permutation; the reader also sees the gold as displayed (letter + option, or Yes / No).
Writes qc/g5_sample_ids.json and qc/g5_render.jsonl (id, dataset, prompt, gold_shown); prints counts only."""
import hashlib, json, random, sys
from collections import Counter, defaultdict
import qclib as Q

sys.path.insert(0, str(Q.P3.parents[2] / "c_src" / "formats" / "formats-1"))
from fmt1 import card as fcard  # noqa: E402

SEED = "public3-qc-g5-prep5-20261006"
PER = 100


def main():
    rows = [r for n in Q.MIXED for r in Q.load(n)]
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[r["source"]][(r["qtype"], len(r["options"] or []), str(r["gold"]))].append(r)
    pick = {}
    for ds, strata in sorted(by.items()):
        n = sum(len(v) for v in strata.values())
        quota = {s: PER * len(v) / n for s, v in strata.items()}
        base = {s: int(q) for s, q in quota.items()}
        rest = PER - sum(base.values())
        for s in sorted(quota, key=lambda s: (-(quota[s] - base[s]), str(s)))[:rest]:
            base[s] += 1
        ids = []
        for s, v in sorted(strata.items(), key=lambda x: str(x[0])):
            v = sorted(v, key=lambda r: hashlib.sha256(f"{SEED}|{r['id']}".encode()).hexdigest())
            ids += [r["id"] for r in v[:base[s]]]
        pick[ds] = sorted(ids, key=lambda i: hashlib.sha256(f"{SEED}|order|{i}".encode()).hexdigest())
    (Q.HERE / "g5_sample_ids.json").write_text(json.dumps({"seed": SEED, "per_dataset": PER, "frame": list(Q.MIXED),
                                                            "ids": pick}, indent=1))
    dio = fcard._dio()
    cfg = json.load(open(Q.P3.parents[2] / "runs/q35_4b_c_r1.json"))
    dio.STYLE, dio.LAYOUT = cfg["style"], cfg["layout"]          # what C round 1 trains on (cygnet, schema_branch_mark)
    rid = {r["id"]: r for r in rows}
    with open(Q.HERE / "g5_render.jsonl", "w") as f:
        for ds, ids in pick.items():
            for i in ids:
                r = rid[i]
                opts = ["Yes", "No"] if r["qtype"] == "noul" else r["options"]
                perm = list(range(len(opts)))
                random.Random(f"{SEED}|perm|{i}").shuffle(perm)
                prompt = dio.user_msg(r, perm)
                if r["qtype"] == "noul":
                    shown = "Yes" if r["gold"] == 1 else "No"
                else:
                    shown = f"{dio.label(perm.index(opts.index(r['gold'])))}. {r['gold']}"
                f.write(json.dumps({"id": i, "dataset": ds, "prompt": prompt, "gold_shown": shown}) + "\n")
    b = json.load(open(Q.OUT / "public3_g5_sample_ids.json"))
    bids = b.get("ids") or b.get("samples") or b
    flat = []

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, str) and x in rid:
            flat.append(x)
    walk(bids)
    bc = Counter(rid[i]["source"] for i in flat)
    print(json.dumps({"mine": {k: len(v) for k, v in pick.items()},
                      "builder_ids_found_in_mixed": dict(bc), "builder_ids_total_found": len(flat),
                      "overlap_with_builder": len(set(flat) & {i for v in pick.values() for i in v})}))


if __name__ == "__main__":
    main()
