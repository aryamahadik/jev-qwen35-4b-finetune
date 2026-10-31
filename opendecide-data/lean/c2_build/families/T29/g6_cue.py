"""c2_build/families/T29/g6_cue.py: which text feature of the card (without the question) predicts the choice gold.

Iteration 2 diagnosis tool for G6 view c_card_without_question. Builds N rows in memory (the pilot's own build_pilot,
G15 off, nothing written), pickles the choice rows' model-visible context, options, gold and the spec's rule structure,
then fits the c-view features (option token x card token crosses) and reports the strongest (gold option, card token)
associations plus structural counts per gold label.

  ../.venv/bin/python -B families/T29/g6_cue.py build [--n 6000] [--out PATH]     (from lean/c2_build; about 7 minutes)
  ../.venv/bin/python -B families/T29/g6_cue.py fit PATH                          (association tables)
"""
from __future__ import annotations

import argparse
import pickle
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))


def build(n: int, out: str):
    import pilot as PI
    import pilot_loaders as PL
    with PL.open_family("T29") as kit:
        b = PI.build_pilot(kit, n, run_g15=False)
    rows = []
    for i in b.infos:
        r = i.row
        if r["qtype"] != "choice":
            continue
        sp = i.spec
        rows.append({"id": r.get("id"), "qform": r["meta"].get("qform"), "options": r["options"], "gold": r["gold"],
                     "context": i.context, "question": i.question, "card": r["meta"]["card_id"], "meta": r["meta"],
                     "tags": list(getattr(sp, "tags", ()) or ()), "depth": getattr(sp, "depth", None)})
    Path(out).write_bytes(pickle.dumps({"n": len(b.infos), "rows": rows}))
    print(len(b.infos), "rows,", len(rows), "choice ->", out)


def fit(path: str):
    from pilot import toks
    d = pickle.loads(Path(path).read_bytes())
    rows = [r for r in d["rows"] if r["qform"] == "ch_verdict"]
    print("ch_verdict rows", len(rows), "of choice", len(d["rows"]))
    # gold option text -> card token presence
    glabels = Counter(r["gold"] for r in rows)
    print("gold labels", dict(glabels))
    tok_by_row = [set(toks(r["context"])) for r in rows]
    df = Counter(t for ts in tok_by_row for t in ts)
    N = len(rows)
    base = {g: c / N for g, c in glabels.items()}
    res = []
    for g in glabels:
        idx = [i for i, r in enumerate(rows) if r["gold"] == g]
        ct = Counter(t for i in idx for t in tok_by_row[i])
        for t, c in ct.items():
            if df[t] < 60:
                continue
            p = c / len(idx)
            q = (df[t] - c) / max(1, N - len(idx))
            res.append((abs(p - q), g, t, round(p, 3), round(q, 3), df[t]))
    for x in sorted(res, reverse=True)[:40]:
        print(x)
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("build", "fit"))
    ap.add_argument("path", nargs="?")
    ap.add_argument("--n", type=int, default=6000)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.n, a.out or a.path)
    else:
        fit(a.path)
