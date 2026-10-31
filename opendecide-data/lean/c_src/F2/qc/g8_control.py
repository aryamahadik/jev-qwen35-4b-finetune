"""G8 null control (report only): the same AFLite-lite procedure (grouped by card) with labels permuted: yes/no gold
shuffled within each card (keeps the card's yes rate), choice gold moved to a seeded random option of the row. Its
predictable share is the floor that partition-to-partition model stability gives with no real cue.
Usage: g8_control.py <name> (needs the g8 embedding cache)"""
import json, sys, random
import numpy as np
import qc_lib as L
import g8

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
D = np.load(L.QC / f"tmp/g8_emb_{NAME}.npz"); Z = D["rowemb"].astype(np.float32); OI = D["opt_idx"]; OV = D["opt_vec"]
out = {}
for seed in (4242, 4343):
    rng = random.Random(seed); perm = [dict(r) for r in rows]; byc = {}
    for i, r in enumerate(perm):
        if L.is_yn(r):
            byc.setdefault(r["meta"]["card_id"], []).append(i)
        else:
            r["gold"] = r["options"][rng.randrange(len(r["options"]))]
    for idx in byc.values():
        gl = [perm[i]["gold"] for i in idx]; rng.shuffle(gl)
        for i, v in zip(idx, gl):
            perm[i]["gold"] = v
    out[f"seed_{seed}"] = g8.aflite(perm, Z, OI, OV, True)
    g8.log(f"control {seed} {out[f'seed_{seed}']}")
(L.QC / f"g8_control_{NAME}.json").write_text(json.dumps(out, indent=1))
g8.log("done")
