"""Stream golden_train.jsonl once (read-only) with N workers; write per-row features (no text) to the scratchpad."""
import json, os, sys
from multiprocessing import Pool

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
SRC = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
TOK = ("/Users/aryamahadik/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
       "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json")
N = 9


def work(args):
    i, a, b, src, out = args
    from tokenizers import Tokenizer
    import feat
    tok = Tokenizer.from_file(TOK)
    sys_tok = len(tok.encode(feat.D.CYGNET_SYSTEM).ids) + 12  # chat template overhead (approx.)
    buf, n = [], 0
    with open(src, "rb") as fh, open(out, "w") as fo:
        if a:
            fh.seek(a - 1)
            fh.readline()
        while fh.tell() <= b:
            l = fh.readline()
            if not l:
                break
            r = json.loads(l)
            buf.append(feat.features(r))
            if len(buf) >= 256:
                flush(buf, tok, sys_tok, fo); n += len(buf); buf = []
        if buf:
            flush(buf, tok, sys_tok, fo); n += len(buf)
    return n


def flush(buf, tok, sys_tok, fo):
    enc = tok.encode_batch([f.pop("prompt") for f in buf], add_special_tokens=False)
    for f, e in zip(buf, enc):
        f["prompt_tok"] = len(e.ids) + sys_tok
        fo.write(json.dumps(f) + "\n")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else SRC
    tag = sys.argv[2] if len(sys.argv) > 2 else "golden"
    size = os.path.getsize(src)
    n = N if size > 50_000_000 else 1
    cuts = [size * k // n for k in range(n + 1)]
    jobs = [(k, cuts[k], cuts[k + 1] - 1 if k < n - 1 else size, src, f"{SP}/feat_{tag}_{k}.jsonl") for k in range(n)]
    with Pool(n) as p:
        counts = p.map(work, jobs)
    print(tag, sum(counts), counts)
