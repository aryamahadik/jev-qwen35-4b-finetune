"""Pick leverage-bounded-decoding knobs (tau, meta_min) OFFLINE from saved per-variant probabilities on DEV splits only.
Prints the best settings by mean dev accuracy; choose one that does not lower any clean split.
  python tune_lbd.py LABEL dev,devp_card,pg_dev
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pick(info, tau, mm):
    full, top = info["full"], max(info["full"], key=info["full"].get)
    best, btv = None, 0.0
    for j, pj in zip(info.get("var_idx") or range(len(info.get("var", []))), info.get("var", [])):
        tv = 0.5 * sum(abs(full[k] - pj.get(k, 0.0)) for k in full)
        if tv >= tau and info["meta"][j] >= mm and max(pj, key=pj.get) != top and tv > btv:
            best, btv = pj, tv
    return best or full


def correct(row, p):
    g = row["gold"]
    return float(max(p, key=p.get) == (("yes" if g == 1 else "no") if row["qtype"] == "noul" else g))


if __name__ == "__main__":
    label, splits = sys.argv[1], sys.argv[2].split(",")
    data = {}
    for sp in splits:
        pd = HERE / ("preds" if sp == "eval" else f"preds_{sp}")
        assert not sp.startswith("eval"), "tuning only on dev splits"
        rows = [json.loads(l) for l in open(HERE / f"data/{sp}.jsonl")]
        infos = [json.loads(l) for l in open(pd / f"{label}_sys.infos.jsonl")]
        data[sp] = list(zip(rows, infos))
    res = []
    for tau in (0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 1.1):
        for mm in (0.3, 0.5, 0.7, 0.8, 0.9, 0.95):
            accs = {sp: sum(correct(r, pick(i, tau, mm)) for r, i in d) / len(d) * 100 for sp, d in data.items()}
            drops = {sp: sum(pick(i, tau, mm) is not i["full"] for r, i in d) for sp, d in data.items()}
            res.append((sum(accs.values()) / len(accs), tau, mm, accs, drops))
    off = next(r for r in res if r[1] == 1.1)
    print("LBD off:", {k: round(v, 2) for k, v in off[3].items()})
    for m, tau, mm, accs, drops in sorted(res, key=lambda x: -x[0])[:8]:
        print(f"tau {tau:.2f} meta {mm:.2f} mean {m:.2f}", {k: round(v, 2) for k, v in accs.items()}, "drops", drops)
