"""DI-KR binding probes (A61 c 7 / A42-D 3.2 / A50): options-only and formatting-only, every G6 model (lr, gbt), 5-fold GroupKFold CV by problem,
on the FULL train build (all non-dev problems that survive the gold check, >= 5,000 rows), mean over the four seed bases 20261013 / 11M / 12M / 13M.
Bar: each cell's mean accuracy within chance +- 3 pp, two-sided (chance = 1/4: all rows have 4 options). The standard G6 views (question only,
card-without-question, metadata) are computed and reported with the same band (report). Usage: python -B kr_probe.py [bases...]; writes work/probe_report.json."""
import json, math, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_rows import *
import pilot
from pilot import RowInfo
from scipy import sparse
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
from collections import defaultdict


def feats(info, view):
    r = info.row; opts = r["options"]; k = len(opts)
    vals = [int(o) for o in opts]; lv = [math.log10(v) for v in vals]
    srt = sorted(range(k), key=lambda j: vals[j]); rank = {j: n for n, j in enumerate(srt)}
    clen = [len(o) for o in opts]; mlv = sum(lv) / k
    T, D = [], []
    for j, o in enumerate(opts):
        v = vals[j]
        shape = "".join("d" for _ in o)
        tz = len(o) - len(o.rstrip("0"))
        fm = {"clen": float(clen[j]), "len_rank": sorted(clen, reverse=True).index(clen[j]) / (k - 1), "is_longest": float(clen[j] == max(clen)),
              "is_shortest": float(clen[j] == min(clen)), "trailing_zeros": float(tz), "ends0": float(o.endswith("0")), "ends5": float(o.endswith("5")),
              "distinct_digits": float(len(set(o))), "repeat_adj": float(any(a == b for a, b in zip(o, o[1:]))), "pos": float(j)}
        tk = ["shape:" + shape, f"tz:{tz}", f"pos:{j}", f"len_rank:{int(fm['len_rank'] * 3)}"]
        if view == "e_format":
            T.append(tk); D.append(fm); continue
        # options-only: everything derivable from the option strings and their displayed order
        others = [lv[m] for m in range(k) if m != j]
        dn = dict(fm)
        dn.update({"lv": lv[j], "vrank": float(rank[j]), "is_min": float(rank[j] == 0), "is_max": float(rank[j] == k - 1),
                   "dev_mean": lv[j] - mlv, "nearest_gap": min(abs(lv[j] - x) for x in others), "mean_gap": sum(abs(lv[j] - x) for x in others) / (k - 1),
                   "mod2": float(v % 2), "mod3": float(v % 3), "mod5": float(v % 5), "mod10": float(v % 10), "m5": float(v % 5 == 0), "m10": float(v % 10 == 0),
                   "m100": float(v % 100 == 0), "first_digit": float(o[0]), "digsum": float(sum(map(int, o))), "digsum_mod9": float(sum(map(int, o)) % 9)})
        tk += ["o:" + o, f"ld:{o[-1]}", f"fd:{o[0]}", f"v_rank:{rank[j]}", f"v_rank_len:{rank[j]}_{len(o)}"]
        T.append(tk); D.append(dn)
    return T, D


def cv_view(infos, view):
    Tl, Dl, Y, Rw = [], [], [], []
    for ri, info in enumerate(infos):
        T, D = feats(info, view)
        for j, o in enumerate(info.row["options"]):
            Tl.append(T[j]); Dl.append(D[j]); Y.append(int(o == info.row["gold"])); Rw.append(ri)
    Y, Rw = np.array(Y), np.array(Rw)
    Xs = HashingVectorizer(n_features=2 ** 18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(Tl)
    Xd = DictVectorizer(sparse=False).fit_transform(Dl)
    groups = [infos[ri].row["meta"]["card_id"] for ri in Rw]
    folds = pilot._folds(groups)
    res = {}
    for nm in ("lr", "gbt"):
        sc = np.zeros(len(Y))
        for tr, te in folds:
            if nm == "lr":
                sca = MaxAbsScaler().fit(Xd[tr])
                Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
                Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
                sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
            else:
                sc[te] = pilot._gbt().fit(Xd[tr], Y[tr]).predict_proba(Xd[te])[:, 1]
        best = defaultdict(list)
        for s, ri, yy in zip(sc, Rw, Y):
            best[ri].append((s, yy))
        acc = np.zeros(len(infos))
        for ri, lst in best.items():
            m = max(s for s, _ in lst); top = [yy for s, yy in lst if s >= m - 1e-12]
            acc[ri] = sum(top) / len(top)
        res[nm] = round(float(acc.mean()), 4)
    return res


def infos_of(rows):
    return [RowInfo(row=r, question=r["instructions"], context=r["state"]) for r in rows]


def main():
    bases = [int(x) for x in sys.argv[1:]] or list(BASES)
    out = {"ruling": "A61 c 7 / A42-D 3.2 / A50 (a): mean over four builds of each view x model cell; binding: options_only, formatting_only at chance +- 3 pp two-sided",
           "bases": bases, "builds": {}}
    for b in bases:
        t0 = time.time()
        rows, drops = build(b, "train")
        inf = infos_of(rows)
        std = pilot.g6_choice(inf)
        cells = {"options_only": cv_view(inf, "b_options_num"), "formatting_only": cv_view(inf, "e_format")}
        for v in ("a_question", "b_options", "c_card_without_question", "d_meta"):
            cells["std_" + v] = std[v]
        out["builds"][str(b)] = {"rows": len(rows), "drops": drops, "chance": std["chance"], "cells": cells, "seconds": round(time.time() - t0)}
        print(b, len(rows), cells, round(time.time() - t0), flush=True)
    agg = {}
    for c in out["builds"][str(bases[0])]["cells"]:
        for m in ("lr", "gbt"):
            accs = [out["builds"][str(b)]["cells"][c][m] for b in bases]
            ch = [out["builds"][str(b)]["chance"] for b in bases]
            ex = sum(a - x for a, x in zip(accs, ch)) / len(accs)
            binding = c in ("options_only", "formatting_only")
            agg[f"{c}/{m}"] = {"accs": accs, "mean_excess_pp": round(ex * 100, 2), "binding": binding,
                               "pass_band_pm3pp": bool(abs(ex) <= 0.03 + 1e-9)}
    out["cells"] = agg
    out["verdict"] = "pass" if all(v["pass_band_pm3pp"] for v in agg.values() if v["binding"]) else "fail"
    out["report_only_outside_band"] = [k for k, v in agg.items() if not v["binding"] and not v["pass_band_pm3pp"]]
    json.dump(out, open(WORK / "probe_report.json", "w"), indent=1)
    print(json.dumps({"verdict": out["verdict"], "cells": {k: v["mean_excess_pp"] for k, v in agg.items()}}))


if __name__ == "__main__":
    main()
