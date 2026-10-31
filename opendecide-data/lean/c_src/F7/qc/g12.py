"""G12 dedup (independent F7 checker). C_DATA_SPEC 8 G12 + F7 G0 7, 9:
- exact hash: sha256 of the full model view (decoder_io.user_msg) and of (card, instructions, state): 0 duplicates;
- MinHash near-dups (datasketch, 128 perm, word 5-gram shingles of row-level wording + question + `state`, entity IDs
  kept; LSH 0.8 verified by exact Jaccard >= 0.8): pairs outside planned twin units (same call_id, or a fact_flip pair
  twin_of link) are counted (keep one);
- structure hash: one surface form per structure, except planned twins and format variants. (a) generator
  meta.structure_hash: groups of rows sharing it, split into planned (all rows of one twin unit / fact_flip pair) and
  unplanned (rows of different units: the same rubric + case structure rendered as separate base rows);
  (b) independent: card_id + gold + `state` with entity IDs, names and the wording masked -> repeats outside planned
  twins.
Usage: g12.py <name>"""
import hashlib, json, re, sys
from collections import Counter, defaultdict
from datasketch import MinHash, MinHashLSH
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
IDRX = re.compile(r"\b[A-Z]{1,4}-?\d{2,6}\b")
H = lambda s: hashlib.sha256(s.encode()).hexdigest()


def shingles(text, k=5):
    t = L.toks(text)
    return {" ".join(t[i:i + k]) for i in range(max(1, len(t) - k + 1))}


def mh(sh):
    m = MinHash(num_perm=128, seed=12)
    for s in sh:
        m.update(s.encode())
    return m


def main():
    d = L.dio(); rows = L.load(NAME); n = len(rows); ids = {r["id"]: r for r in rows}
    unit = {}
    for r in rows:
        unit[r["id"]] = r["call_id"]
    for r in rows:  # fact_flip pairs: twin and base form one planned unit (own call_ids by design)
        if r["meta"].get("twin_kind") == "fact_flip" and r["meta"].get("twin_of") in ids:
            unit[r["id"]] = unit[r["meta"]["twin_of"]] = "ff:" + r["meta"]["twin_of"]
    view = Counter(H(d.user_msg(r)) for r in rows)
    raw = Counter(H("\x1e".join([r.get("card") or "", r["instructions"], r["state"]])) for r in rows)
    res = {"gate": "G12", "file": f"out/{NAME}.jsonl", "rows": n,
           "exact_dup_model_view": sum(v - 1 for v in view.values()), "exact_dup_raw_fields": sum(v - 1 for v in raw.values())}
    cp = L.card_paras(rows)
    txt = {r["id"]: L.split_ins(r, cp)[1] + "\n" + r["state"] for r in rows}
    sh = {k: shingles(v) for k, v in txt.items()}; lsh = MinHashLSH(threshold=0.8, num_perm=128); ms = {}
    for k in sh:
        ms[k] = mh(sh[k]); lsh.insert(k, ms[k])
    pairs = set()
    for k in sh:
        for o in lsh.query(ms[k]):
            if o != k:
                a, b = sorted((k, o)); j = len(sh[a] & sh[b]) / max(1, len(sh[a] | sh[b]))
                if j >= 0.8:
                    pairs.add((a, b, round(j, 3)))
    bad = [p for p in pairs if unit[p[0]] != unit[p[1]]]
    res["minhash"] = {"pairs_ge_0.8": len(pairs), "planned_twin_pairs": len(pairs) - len(bad), "non_twin_pairs": len(bad),
                      "non_twin_same_card": sum(ids[a]["meta"]["card_id"] == ids[b]["meta"]["card_id"] for a, b, _ in bad),
                      "examples": [[a, b, j] for a, b, j in sorted(bad)[:10]]}
    g = defaultdict(list)
    for r in rows:
        g[r["meta"]["structure_hash"]].append(r["id"])
    multi = {h: v for h, v in g.items() if len(v) > 1}
    unpl = {h: v for h, v in multi.items() if len({unit[i] for i in v}) > 1}
    kinds = Counter()
    for v in unpl.values():
        kinds[tuple(sorted(Counter(ids[i]["meta"].get("row_kind") for i in v)))] += 1
    res["structure_hash_generator"] = {"distinct": len(g), "groups_gt1": len(multi), "groups_unplanned": len(unpl),
                                       "rows_in_unplanned_groups": sum(len(v) for v in unpl.values()),
                                       "extra_rows_unplanned": sum(len({unit[i] for i in v}) - 1 for v in unpl.values()),
                                       "unplanned_by_sampler": dict(Counter(ids[v[0]]["meta"]["sampler"] for v in unpl.values())),
                                       "unplanned_same_card": sum(len({ids[i]["meta"]["card_id"] for i in v}) == 1 for v in unpl.values()),
                                       "unplanned_same_gold": sum(len({ids[i]["gold"] for i in v}) == 1 for v in unpl.values()),
                                       "example_groups": [v for v in list(unpl.values())[:5]]}
    ind = defaultdict(list)
    for r in rows:
        st = IDRX.sub("<ID>", r["state"])
        st = re.sub(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", "<NAME>", st)
        ind[(r["meta"]["card_id"], r["gold"], st)].append(r["id"])
    iu = {k: v for k, v in ind.items() if len({unit[i] for i in v}) > 1}
    res["structure_independent"] = {"keys_unplanned": len(iu), "extra_rows": sum(len({unit[i] for i in v}) - 1 for v in iu.values()),
                                    "examples": [v for v in list(iu.values())[:5]]}
    res["pass"] = (res["exact_dup_model_view"] == 0 and res["exact_dup_raw_fields"] == 0 and res["minhash"]["non_twin_pairs"] == 0
                   and res["structure_hash_generator"]["groups_unplanned"] == 0 and res["structure_independent"]["keys_unplanned"] == 0)
    json.dump(res, open(L.QC / f"g12_{NAME}.json", "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("exact_dup_model_view", "exact_dup_raw_fields", "pass")}),
          json.dumps({k: v for k, v in res["structure_hash_generator"].items() if k != "example_groups"}),
          res["minhash"]["non_twin_pairs"], res["structure_independent"]["keys_unplanned"])


if __name__ == "__main__":
    main()
