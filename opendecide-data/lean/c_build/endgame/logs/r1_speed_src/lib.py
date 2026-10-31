import os, sys, json, random, math
os.environ["OD_STYLE"] = "cygnet"; os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
sys.path.insert(0, LEAN)
import decoder_io, train_decoder as td
decoder_io.LAYOUT = "schema_branch_mark"
assert decoder_io.STYLE == "cygnet"
tok = decoder_io.load_tokenizer("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
PAD = decoder_io.PAD_MULTIPLE
ro = decoder_io.Readout(tok)  # sets decoder_io.WIDE (labels for >26 options)

def prompt(r, p=None):
    return r.get("_prompt") or decoder_io.render_chat(tok, decoder_io.CYGNET_SYSTEM, decoder_io.user_msg(r, p))

def ntok(texts):
    return [len(x) for x in tok(texts, add_special_tokens=False)["input_ids"]]

def padded(n):
    p = max(1, decoder_io.PAD_MULTIPLE); return -(-min(n, decoder_io.MAX_LEN) // p) * p

def read_jsonl(p):
    with open(p) as f:
        return [json.loads(l) for l in f if l.strip()]

def step_feats(batch, perms, tw, uid, budget=8192, anchor=False, lens=None):
    """Per step: micro-batches as the trainer forms them; real token lengths of every sequence (rows + twins)."""
    groups = td._micro_groups(batch, uid, tw, budget) if budget > 0 else [list(range(len(batch)))]
    f = {"rows": len(batch), "twins": len(tw), "n_micro": len(groups), "pad_tok": 0, "real_tok": 0, "attn": 0.0,
         "anc_pad_tok": 0, "max_len": 0, "n_seq": 0}
    for idx in groups:
        loc = set(idx)
        seqs = [(batch[i], perms[i]) for i in idx] + [(batch[i], p2) for i, p2 in tw if i in loc]
        if lens is None:
            L = ntok([prompt(r, p) for r, p in seqs])
        else:
            L = [lens[r["id"]] for r, _ in seqs]
        P = padded(max(L))
        f["pad_tok"] += len(L) * P; f["real_tok"] += sum(L); f["attn"] += len(L) * P * P / 1e6
        f["max_len"] = max(f["max_len"], max(L)); f["n_seq"] += len(L)
        if anchor:
            anc = [i for i in idx if (batch[i].get("meta") or {}).get("anchor")]
            if anc:
                La = L[:len(idx)]
                pos = {i: j for j, i in enumerate(idx)}
                f["anc_pad_tok"] += len(anc) * padded(max(La[pos[i]] for i in anc))
    return f

def replay(rows, rels, seed, n_steps, batch=16, perm_twin=0.3, budget=8192, anchor=False, lens=None):
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in ids and x["b"] in ids]
    units, merged = td.make_units(rows, rels)
    random.seed(seed)
    twin_rng = random.Random(seed + 1)
    gen = td.batches(units, batch)
    uid = {r["id"]: k for k, u in enumerate(units) for r in u}
    out = []
    for step in range(n_steps):
        b = next(gen)
        h = td._batch_hash(b)
        perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                 else random.sample([0, 1], 2) for r in b]
        tw = td.pick_twins(b, perms, perm_twin, twin_rng)
        f = step_feats(b, perms, tw, uid, budget, anchor, lens)
        f["hash"] = h; f["batch_ids"] = [r["id"] for r in b]
        out.append(f)
    return out, units
