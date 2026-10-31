"""t4_ids_dump.py (run with ~/od/bin/python): for every sequence of the 8,143 P decisions, write the rendered text and the
ids the client sends (decoder_io path = what fast_read / the 17 Oct harness send as input_ids). Output is a local file
under ~/opt_r2/cache (never printed). Step 2 (t4_ids_check.py, ~/sgl python) re-tokenizes the text with the SERVER's
tokenizer stack and compares."""
import json
import pathlib
import sys
import time
from pathlib import Path

_o = pathlib.Path.exists


def _s(self, *a, **k):
    try:
        return _o(self, *a, **k)
    except PermissionError:
        return False


pathlib.Path.exists = _s
H = Path.home()
for p in (str(H / "lean" / "hosting"), str(H / "lean"), str(H / "opt_r2")):
    sys.path.insert(0, p)
from oc1 import common as C  # noqa: E402
from oc1 import items as I  # noqa: E402

R = I.readout_mod()
tok, ro, info = I.load_c1(H / "lean" / "models" / "q35_4b_main500k")
rows = C.read_jsonl(H / "opt_r2" / "data" / "P.jsonl")
out = H / "opt_r2" / "cache" / "t4_seqs.jsonl"
t0 = time.time()
n_seq = n_tok = 0
with open(out, "w") as f:
    for it in rows:
        named = R.parse_v1(it["request"])
        items = R.build_items(ro, named, choice_views=2, render=True)
        R.tokenize_items(tok, items)
        for k, x in enumerate(items):
            f.write(json.dumps({"id": it["id"], "bucket": it["bucket"], "k": k, "text": x.text, "ids": list(map(int, x.ids))}) + "\n")
            n_seq += 1
            n_tok += len(x.ids)
print({"decisions": len(rows), "sequences": n_seq, "tokens": n_tok, "s": round(time.time() - t0, 1), "file": str(out)})
