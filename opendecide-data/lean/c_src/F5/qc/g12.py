"""G12 dedup (independent F5 checker). C_DATA_SPEC 8 G12 + F5 G0 8/9:
- exact hash: sha256 of the full model view (decoder_io.user_msg) and of (card, instructions, state): 0 duplicates;
- MinHash near-dups (datasketch, 128 perm, word 5-gram shingles of question + record; LSH threshold 0.8, verified by
  exact Jaccard >= 0.8): 0 pairs outside planned twins (same base, or the two bases of one contrast pair);
  question-free record near-dups across bases are reported;
- structure hash: (a) generator meta.structure_hash maps to one base and one surface (rows of one base only);
  (b) independent: sampler + card + multiset of record tokens with IDs/names masked + pack-free question skeleton ->
  > 1 base per key outside contrast pairs counts as a duplicate structure.
Usage: g12.py <name>"""
import hashlib, json, re, sys
from collections import Counter, defaultdict
from datasketch import MinHash, MinHashLSH
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
IDRX = re.compile(r"\b[A-Z]{2,4}-\d{3,5}\b")
NAME_RX = re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b")
H = lambda s: hashlib.sha256(s.encode()).hexdigest()


def shingles(text, k=5):
    t = TOK.findall(text.lower())
    return {" ".join(t[i:i + k]) for i in range(max(1, len(t) - k + 1))}


def mh(sh):
    m = MinHash(num_perm=128, seed=12)
    for s in sh:
        m.update(s.encode())
    return m


def near_pairs(keys, texts, thr=0.8):
    sh = {k: shingles(texts[k]) for k in keys}; lsh = MinHashLSH(threshold=thr, num_perm=128); ms = {}
    for k in keys:
        ms[k] = mh(sh[k]); lsh.insert(k, ms[k])
    out = set()
    for k in keys:
        for o in lsh.query(ms[k]):
            if o != k:
                a, b = sorted((k, o)); j = len(sh[a] & sh[b]) / max(1, len(sh[a] | sh[b]))
                if j >= thr:
                    out.add((a, b, round(j, 3)))
    return sorted(out)


def main():
    d = L.dio(); rows = L.load(NAME); side = L.load_side(NAME); n = len(rows)
    base = {r["id"]: side[r["id"]]["base_id"] for r in rows}; pair = {r["id"]: side[r["id"]].get("pair_id") for r in rows}
    twin = lambda a, b: base[a] == base[b] or (pair[a] is not None and pair[a] == pair[b])
    view = Counter(H(d.user_msg(r)) for r in rows)
    raw = Counter(H("\x1e".join([r.get("card") or "", r["instructions"], r["state"]])) for r in rows)
    res = {"gate": "G12", "file": f"out/{NAME}.jsonl", "rows": n,
           "exact_dup_model_view": sum(v - 1 for v in view.values()), "exact_dup_raw_fields": sum(v - 1 for v in raw.values())}
    qrec = {r["id"]: L.split_q(r["instructions"])[0] + "\n" + r["state"] for r in rows}
    pq = near_pairs([r["id"] for r in rows], qrec)
    bad = [p for p in pq if not twin(p[0], p[1])]
    res["minhash_question_plus_record"] = {"pairs_ge_0.8": len(pq), "planned_twin_pairs": len(pq) - len(bad),
                                           "non_twin_pairs": len(bad), "examples": bad[:10]}
    rep = {}
    for r in rows:
        rep.setdefault(base[r["id"]], r["id"])
    byid = {x["id"]: x for x in rows}; rec = {rid: byid[rid]["state"] for rid in rep.values()}
    pr = near_pairs(list(rec), rec)
    badr = [p for p in pr if not twin(p[0], p[1])]
    res["minhash_record_only_info"] = {"base_pairs_ge_0.8": len(pr), "non_pair_base_pairs": len(badr), "examples": badr[:10]}
    # structure hash (a): generator's
    sh_b = defaultdict(set); b_sh = defaultdict(set)
    for r in rows:
        sh_b[r["meta"]["structure_hash"]].add(base[r["id"]]); b_sh[base[r["id"]]].add(r["meta"]["structure_hash"])
    res["structure_hash_generator"] = {"distinct": len(sh_b), "bases": len(b_sh),
                                       "hashes_spanning_bases": sum(len(v) > 1 for v in sh_b.values()),
                                       "bases_with_several_hashes": sum(len(v) > 1 for v in b_sh.values())}
    # structure hash (b): independent
    mask = lambda s: NAME_RX.sub(" zname ", IDRX.sub(" zid ", s))
    key_b = defaultdict(set)
    for r in rows:
        q, _ = L.split_q(r["instructions"])
        k = (r["meta"]["sampler"], r["meta"]["card_id"], tuple(sorted(Counter(TOK.findall(mask(r["state"]).lower())).items())),
             " ".join(TOK.findall(mask(q).lower())))
        key_b[H(repr(k))].add(r["id"])
    dup = []
    for k, ids in key_b.items():
        bs = {base[i] for i in ids}
        if len(bs) > 1:
            ids = sorted(ids)
            if not all(twin(ids[0], j) for j in ids[1:]):
                dup.append(ids[:4])
    res["structure_hash_independent"] = {"keys": len(key_b), "keys_spanning_non_twin_bases": len(dup), "examples": dup[:10],
                                         "definition": "sampler + card + record token multiset (IDs, person names masked) + question tokens (masked)"}
    res["pass"] = (res["exact_dup_model_view"] == 0 and res["exact_dup_raw_fields"] == 0 and not bad
                   and res["structure_hash_generator"]["hashes_spanning_bases"] == 0 and not dup)
    json.dump(res, open(L.QC / f"g12_{NAME}.json", "w"), indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) else {a: b for a, b in v.items() if a != "examples"}) for k, v in res.items()}))


if __name__ == "__main__":
    main()
