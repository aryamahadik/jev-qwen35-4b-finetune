#!/usr/bin/env python3
"""public-1 QC: spec 3.1 (v2) 'unused records only' and the Wikipedia passage dedup against C1's sources
(repair round 1, PREREG A29 a). Counts and ids only; prints no row text.

Indexes are rebuilt here from C1 golden_train (data/v14_parts/golden_train.jsonl, the allow-listed replay file), not
taken from the builder's tmp/ indexes:
  - golden units: every normalised full state, every normalised line (split on newlines) of >= 6 words and every
    sentence of >= 8 words of every state and instructions;
  - word 10-grams (lib/grams.py tokenisation) of state, instructions, card and options: of every row ("all") and of
    the rows of the 7 sources spec 3.1 names (qnli, gd_answer_equiv, gd_hotpotqa_yesno, gd_feverous, gd_totto_claims,
    gd_wtq, boolq; "named").
Checked text of every public-1 row (rows_r1, reserve, mtdev): state, instructions and options. 10-grams that occur in
any public-1 template or card string (lib/pools.py, authored here, not a record) are not counted.
A row fails if (a) its full state, one of its state / instruction lines (>= 6 words) or sentences (>= 8 words), or an
option (>= 6 words) equals a golden unit, or (b) it shares any word 10-gram with golden_train ('all'; 'named' is the
subset reported for the spec's list). Pass = zero failing rows.

Usage: qc_unused.py   (writes qc/gate_unused.json)
"""
from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
P1 = HERE.parent
sys.path.insert(0, str(P1 / "lib"))
from grams import gram_hashes  # noqa: E402
from textnorm import h64, norm, sent_hashes  # noqa: E402
import pools  # noqa: E402

GT = P1.parents[2] / "data" / "v14_parts" / "golden_train.jsonl"
NAMED = {"qnli", "gd_answer_equiv", "gd_hotpotqa_yesno", "gd_feverous", "gd_totto_claims", "gd_wtq", "boolq"}
FILES = {"rows": "out/public1_rows_r1.jsonl", "reserve": "out/public1_reserve.jsonl", "mtdev": "out/public1_mtdev.jsonl"}


def lines6(text):
    for ln in (text or "").split("\n"):
        n = norm(ln)
        if n.count(" ") + 1 >= 6:
            yield h64(n)


def main():
    t0 = time.time()
    units, g_all, g_named, buf_a, buf_n = set(), [], [], [], []
    n = 0
    with open(GT) as f:
        for line in f:
            r = json.loads(line)
            st, ins = r.get("state") or "", r.get("instructions") or ""
            units.add(h64(norm(st)))
            units.update(lines6(st + "\n" + ins))
            units.update(sent_hashes(st))
            units.update(sent_hashes(ins))
            texts = [st, ins, r.get("card") or ""] + [o for o in (r.get("options") or []) if isinstance(o, str)]
            gs = [g for g in (gram_hashes(t) for t in texts if t) if g.size]
            if gs:
                a = np.concatenate(gs)
                buf_a.append(a)
                if r.get("source") in NAMED:
                    buf_n.append(a)
            n += 1
            if n % 50000 == 0:
                g_all.append(np.unique(np.concatenate(buf_a)))
                buf_a = []
                if buf_n:
                    g_named.append(np.unique(np.concatenate(buf_n)))
                    buf_n = []
    if buf_a:
        g_all.append(np.unique(np.concatenate(buf_a)))
    if buf_n:
        g_named.append(np.unique(np.concatenate(buf_n)))
    A = np.unique(np.concatenate(g_all))
    N = np.unique(np.concatenate(g_named))
    del g_all, g_named
    t_idx = round(time.time() - t0)
    # template / card 10-grams (authored here; excluded from the share count)
    tmpl = set()
    for o in pools.all_pool_objects():
        for v in o.values():
            if isinstance(v, str):
                for piece in v.replace("{", " ").replace("}", " ").split("\n"):
                    tmpl.update(gram_hashes(piece).tolist())

    def shared(arr, g):
        if g.size == 0:
            return 0
        i = np.searchsorted(arr, g)
        i[i >= arr.size] = arr.size - 1
        return int((arr[i] == g).sum())

    res = {"golden_rows": n, "golden_units": len(units), "golden_10grams_all": int(A.size),
           "golden_10grams_named": int(N.size), "index_secs": t_idx, "files": {}}
    fail_ids = collections.defaultdict(list)
    for part, rel in FILES.items():
        cnt = collections.Counter()
        for line in open(P1 / rel):
            r = json.loads(line)
            st, ins = r["state"] or "", r["instructions"] or ""
            opts = [o for o in (r.get("options") or []) if isinstance(o, str)]
            hs = {h64(norm(st))} | set(lines6(st + "\n" + ins)) | set(sent_hashes(st)) | set(sent_hashes(ins))
            hs |= {h64(norm(o)) for o in opts if norm(o).count(" ") + 1 >= 6}
            unit_hit = bool(hs & units)
            g = np.unique(np.concatenate([gram_hashes(t) for t in [st, ins] + opts] + [np.zeros(0, np.uint64)]))
            if tmpl and g.size:
                g = g[~np.isin(g, np.fromiter(tmpl, dtype=np.uint64))]
            sa, sn = shared(A, g), shared(N, g)
            key = f"{part}|{r['source']}"
            cnt[f"{key}|rows"] += 1
            cnt[f"{key}|unit_hit"] += unit_hit
            cnt[f"{key}|share_10gram_all"] += sa > 0
            cnt[f"{key}|share_10gram_named"] += sn > 0
            if unit_hit or sa:
                fail_ids[part].append(r["id"])
        res["files"][part] = dict(sorted(cnt.items()))
    res["failing_rows"] = {k: len(v) for k, v in fail_ids.items()}
    res["failing_ids_first20"] = {k: v[:20] for k, v in fail_ids.items()}
    res["pass"] = not any(fail_ids.values())
    res["secs"] = round(time.time() - t0)
    (HERE / "gate_unused.json").write_text(json.dumps(res, indent=1))
    print("UNUSED pass", res["pass"], res["failing_rows"], "secs", res["secs"])


if __name__ == "__main__":
    main()
