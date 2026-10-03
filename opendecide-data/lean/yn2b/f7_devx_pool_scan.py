"""Overlap scan of the F7 devx base texts (counts only; no text from any scanned file is printed or stored).

For every real base text used by data/v14_parts/f7_devx.jsonl (civil_comments / toxic_conv comments, SaferProducts
reports, wiki posts) it counts
  golden_hits : word 8-grams shared with any golden_train state (golden_train is in the fix2 training mix)
  f7_hits     : word 8-grams shared with any F7 train or probe state (membership test only)
  infam_hits / strict_hits / infam_y_hits : 12-gram hashes shared with the ship audit's reference sets
                (extra/build_fix1.load_refs: golden_dev + breadth_dev, held-out + every dev / eval split, yn2b devs)
Every count must be 0. Writes yn2b/f7_devx_pool_flags.json. CPU only, about 20 s (9 processes).
Usage (from opendecide-data/lean):  PYTHONHASHSEED=0 ../.venv/bin/python yn2b/f7_devx_pool_scan.py
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
for _p in (str(LEAN), str(LEAN / "yn2b"), str(LEAN / "extra")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True
OUT = LEAN / "yn2b/f7_devx_pool_flags.json"
TOK = re.compile(r"[a-z0-9]+")
N = 8


def grams(text):
    t = TOK.findall(text.lower())
    if len(t) < N:
        return {" ".join(t)} if t else set()
    return {" ".join(t[i:i + N]) for i in range(len(t) - N + 1)}


IDX = None


def _init(idx):
    global IDX
    IDX = idx


def _scan_range(args):
    path, start, end = args
    hits = defaultdict(int)
    with open(path, "rb") as f:
        f.seek(start)
        if start:
            f.readline()
        while f.tell() < end:
            line = f.readline()
            if not line:
                break
            try:
                st = json.loads(line).get("state")
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(st, str):
                st = json.dumps(st)
            for g in grams(st):
                for k in IDX.get(g, ()):
                    hits[k] += 1
    return dict(hits)


def scan(path, idx, procs=9):
    size = os.path.getsize(path)
    step = size // (procs * 4) + 1
    ranges = [(str(path), i, min(size, i + step)) for i in range(0, size, step)]
    tot = defaultdict(int)
    with mp.Pool(procs, initializer=_init, initargs=(idx,)) as pool:
        for h in pool.imap_unordered(_scan_range, ranges):
            for k, v in h.items():
                tot[k] += v
    return tot


def base_texts():
    """{ref: text} for every base text named in the devx rows' meta.orig (invented records are skipped)."""
    import f7_devx_build as B
    refs = {}
    for line in open(LEAN / "data/v14_parts/f7_devx.jsonl", encoding="utf-8"):
        r = json.loads(line)
        for ref in r["meta"]["orig"]:
            if ref.startswith("g:"):
                refs[ref] = B.TOX[ref][2]
            elif not ref.startswith("invented:"):
                refs[ref] = B.RAW[ref][2]
    return refs


def main():
    import build_fix1 as bf
    import check_yn2b as cy
    texts = base_texts()
    idx = defaultdict(list)
    for k, t in texts.items():
        for g in grams(t):
            idx[g].append(k)
    gold = scan(LEAN / "data/v14_parts/golden_train.jsonl", idx)
    f7 = defaultdict(int)
    for p in ("data/v14_parts/f7_train.jsonl", "data/v14_parts/f7_probe.jsonl"):
        for k, v in scan(LEAN / p, idx, procs=4).items():
            f7[k] += v
    Rf = bf.load_refs(lambda s: None)
    flags = {}
    for k, t in sorted(texts.items()):
        g12 = cy.row_ghash(t)
        flags[k] = {"golden_hits": gold.get(k, 0), "f7_hits": f7.get(k, 0),
                    "infam_hits": len(g12 & Rf["infam"]), "strict_hits": len(g12 & Rf["strict"]),
                    "infam_y_hits": len(g12 & Rf["infam_y"]), "n_gram8": len(grams(t))}
    bad = {k: v for k, v in flags.items() if any(v[x] for x in ("golden_hits", "f7_hits", "infam_hits", "strict_hits",
                                                               "infam_y_hits"))}
    OUT.write_text(json.dumps({"texts": len(flags), "with_any_overlap": len(bad), "flags": flags}, indent=1))
    print(f"{len(flags)} base texts, {len(bad)} with any overlap -> {OUT.relative_to(LEAN)}")
    return 1 if bad else 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    sys.exit(main())
