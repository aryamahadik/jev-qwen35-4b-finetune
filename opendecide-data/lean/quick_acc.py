"""Accuracy (argmax) per split and per source for several prediction names; dev splits only by default."""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
names, splits = sys.argv[1].split(","), sys.argv[2].split(",")
by_src = "--src" in sys.argv
for sp in splits:
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / f"data/{sp}.jsonl")}
    pd = HERE / ("preds" if sp == "eval" else f"preds_{sp}")
    line, srcs = [], defaultdict(dict)
    for n in names:
        f = pd / f"{n}.jsonl"
        if not f.exists():
            line.append(f"{n}=NA")
            continue
        c, t, cs = 0, 0, defaultdict(lambda: [0, 0])
        for l in open(f):
            p = json.loads(l)
            r = rows[p["id"]]
            g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
            ok = max(p["probs"], key=p["probs"].get) == g
            c += ok
            t += 1
            cs[r["source"]][0] += ok
            cs[r["source"]][1] += 1
        line.append(f"{n}={100 * c / t:.1f}")
        for s, (a, b) in cs.items():
            srcs[s][n] = f"{100 * a / b:.0f}"
    print(f"{sp:10s} " + "  ".join(line))
    if by_src:
        for s, d in sorted(srcs.items()):
            print(f"   {s:28s} " + "  ".join(f"{n}={v}" for n, v in d.items()))
