"""Decontamination: drop training rows that share any N-word run (default 10) with JevBench public text.
Reads JevBench only to REMOVE overlap (standard benchmark decontamination); nothing from it is ever written to train data.
  python decontam.py data/pg_train.jsonl [data/lah_train.jsonl ...] [--n 10]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JB = HERE.parents[1] / "bench/jevbench/datasets/public"
words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()


def grams(t, n):
    w = words(t)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def main():
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 10
    files = [a for a in sys.argv[1:] if a.endswith(".jsonl")]
    bench = set()
    for f in JB.glob("*.jsonl"):
        for l in open(f):
            r = json.loads(l)
            bench |= grams(json.dumps(r.get("state"), ensure_ascii=False) + " " + json.dumps(r.get("question"), ensure_ascii=False), n)
    for f in files:
        rows = [json.loads(l) for l in open(f)]
        keep = [r for r in rows if not (grams(r["state"] + " " + (r.get("instructions") or "") + " " + (r.get("card") or ""), n) & bench)]
        Path(f).write_text("".join(json.dumps(r) + "\n" for r in keep))
        print(f, "kept", len(keep), "of", len(rows), f"(dropped {len(rows) - len(keep)} sharing a {n}-gram with JevBench public)")


if __name__ == "__main__":
    main()
