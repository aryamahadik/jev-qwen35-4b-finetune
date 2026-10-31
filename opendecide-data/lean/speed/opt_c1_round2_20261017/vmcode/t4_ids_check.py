"""t4_ids_check.py (run with ~/sgl/bin/python = the SGLang server's own transformers/tokenizers): re-tokenize every
sequence text of t4_seqs.jsonl the way SGLang would for a `text` request (AutoTokenizer from the served model dir) and
compare with the client ids. Prints counts only."""
import json
import sys
import time
from pathlib import Path

from transformers import AutoTokenizer
import tokenizers
import transformers

H = Path.home()
model = sys.argv[1] if len(sys.argv) > 1 else str(H / "models" / "q35_4b_main500k_merged")
tok = AutoTokenizer.from_pretrained(model)
print({"transformers": transformers.__version__, "tokenizers": tokenizers.__version__, "tok_class": type(tok).__name__})
n = same_a = same_b = 0
bad = []
t0 = time.time()
by_bucket = {}
with open(H / "opt_r2" / "cache" / "t4_seqs.jsonl") as f:
    for line in f:
        r = json.loads(line)
        a = tok(r["text"])["input_ids"]                                   # SGLang: tokenizer(text) default specials
        b = tok(r["text"], add_special_tokens=False)["input_ids"]
        n += 1
        ea, eb = a == r["ids"], b == r["ids"]
        same_a += ea
        same_b += eb
        bb = by_bucket.setdefault(r["bucket"], [0, 0])
        bb[0] += 1
        bb[1] += (ea or eb)
        if not (ea or eb) and len(bad) < 20:
            bad.append({"id_hash": hash(r["id"]) & 0xffff, "k": r["k"], "len_client": len(r["ids"]), "len_server": len(a)})
print(json.dumps({"sequences": n, "identical_default_specials": same_a, "identical_no_specials": same_b,
                  "identical_either": sum(v[1] for v in by_bucket.values()), "by_bucket": by_bucket, "mismatch_examples": bad,
                  "seconds": round(time.time() - t0, 1)}))
