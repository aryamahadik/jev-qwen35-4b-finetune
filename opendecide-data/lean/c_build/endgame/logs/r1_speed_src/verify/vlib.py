import os, sys, json, random, math
from collections import defaultdict, Counter
os.environ["OD_STYLE"] = "cygnet"
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
sys.path.insert(0, LEAN)
import decoder_io, train_decoder as td
decoder_io.LAYOUT = "schema_branch_mark"
tok = decoder_io.load_tokenizer("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
ro = decoder_io.Readout(tok)


def rj(p):
    with open(p) as f:
        return [json.loads(l) for l in f if l.strip()]


def ntok(rows, perms):
    texts = decoder_io.prompt_texts(ro, rows, perms)
    return [len(x) for x in tok(texts, add_special_tokens=False)["input_ids"]]


def pad(n, P=None):
    P = P or decoder_io.PAD_MULTIPLE
    return -(-n // P) * P


def run(rows, rels, seed, n_steps, cfg, budgets=(8192,), pads=(256,), lens_cache=None):
    """Exact replay of train()'s draws; per step and per (budget,pad) packing: padded/real tokens, micro count."""
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in ids and x["b"] in ids]
    units, merged = td.make_units(rows, rels)
    rel_by_row = defaultdict(list)
    for x in rels:
        rel_by_row[x["a"]].append(x)
    random.seed(seed)
    twin_rng = random.Random(seed + 1)
    gen = td.batches(units, cfg["batch"])
    uid = {r["id"]: k for k, u in enumerate(units) for r in u}
    out = []
    for step in range(n_steps):
        b = next(gen)
        perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                 else random.sample([0, 1], 2) for r in b]
        tw = td.pick_twins(b, perms, cfg["perm_twin"], twin_rng)
        # real token length of every sequence (rows, then twins)
        L = ntok(b, perms)
        Lt = ntok([b[i] for i, _ in tw], [p for _, p in tw]) if tw else []
        tlen = defaultdict(list)
        for i, l in enumerate(L):
            tlen[i].append(l)
        for (i, _), l in zip(tw, Lt):
            tlen[i].append(l)
        ac = td.aux_counts(cfg, b, rel_by_row)
        f = {"hash": td._batch_hash(b), "rows": len(b), "twins": len(tw), "real": sum(L) + sum(Lt),
             "n_ord": sum(1 for r in b if td.is_ordinal(r)), "ac_cons": ac["cons"], "ac_inv": ac["inv"],
             "anc": sum(1 for r in b if (r.get("meta") or {}).get("anchor"))}
        for P in pads:
            old = decoder_io.PAD_MULTIPLE
            decoder_io.PAD_MULTIPLE = P
            try:
                for B in budgets:
                    groups = td._micro_groups(b, uid, tw, B)
                    padded, mc, mi, maxL = 0, 0, 0, 0
                    for g in groups:
                        seq = [l for i in g for l in tlen[i]]
                        padded += len(seq) * pad(max(seq), P)
                        maxL = max(maxL, pad(max(seq), P))
                        a = td.aux_counts(cfg, [b[i] for i in g], rel_by_row)
                        mc += a["cons"]; mi += a["inv"]
                    f[f"pad_{B}_{P}"] = padded
                    f[f"nmb_{B}_{P}"] = len(groups)
                    f[f"cons_{B}_{P}"] = mc
                    f[f"inv_{B}_{P}"] = mi
                    f[f"shapes_{B}_{P}"] = sorted((sum(len(tlen[i]) for i in g),
                                                   pad(max(l for i in g for l in tlen[i]), P)) for g in groups)
            finally:
                decoder_io.PAD_MULTIPLE = old
        out.append(f)
    return out, units, rels
