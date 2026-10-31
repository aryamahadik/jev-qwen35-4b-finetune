"""Counts only: share of word pieces each view loses to MiniLM's 256-token cap, per family pool."""
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as T
import numpy as np
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(T.MODEL); out = {}
for fam in sys.argv[1:]:
    rows, sha = T.load_pool(T.LEAN / f"c_src/{fam}/out/candidates_r1.jsonl"); views = T.pool_views(fam, rows)
    d = {"pool_sha256": sha}
    for s, name in enumerate(("q", "card", "state")):
        ts = list(dict.fromkeys(t for v in views for t in v[0][s]))
        L = np.array([len(x) for x in tok(ts, add_special_tokens=True)["input_ids"]])
        d[name] = {"chunks": len(ts), "share_chunks_over_256": round(float((L > 256).mean()), 4),
                   "share_wordpieces_lost": round(float(np.clip(L - 256, 0, None).sum() / L.sum()), 4)}
    out[fam] = d; print(fam, json.dumps(d), flush=True)
json.dump(out, open("trunc.json", "w"), indent=1)
