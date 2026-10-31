import sys, collections, json, pickle
from pathlib import Path
import numpy as np
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot, pilot_loaders as PL  # noqa: E402
from families.T26 import loader as LD  # noqa: E402
from sklearn.feature_extraction import DictVectorizer  # noqa: E402

base, nrows = int(sys.argv[1]), int(sys.argv[2])
with LD.open_t26() as kit:
    fk = PL.FamilyKit("T26", PL.family_dir("T26"), kit.plugin, kit.ctx, "loader", "pools_v2/", [])
    b = pilot.build_pilot(fk, nrows, seed_base=base, run_g15=False)
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    T, D, Y, Rw = pilot._pair_rows(ch, "d_meta")
    Y, Rw = np.array(Y), np.array(Rw)
    groups = [ch[ri].row["meta"]["card_id"] for ri in Rw]
    folds = pilot._folds(list(groups))
    import pickle as _p
    _p.dump({"D": D, "Y": Y, "Rw": Rw, "groups": groups, "qf": [i.row["meta"]["qform"] for i in ch],
             "gold": [i.row["gold"] for i in ch]}, open("g6_pairs.pkl", "wb"))
    names = sorted({k for d in D for k in d})
    print(len(ch), "rows", len(Y), "pairs", names)

    def acc(drop=(), keep=None):
        Dd = [{k: v for k, v in d.items() if k not in drop and (keep is None or k in keep)} for d in D]
        Xd = DictVectorizer(sparse=False).fit_transform(Dd)
        sc = np.zeros(len(Y))
        for tr, te in folds:
            if len(set(Y[tr])) < 2:
                continue
            sc[te] = pilot._gbt().fit(Xd[tr], Y[tr]).predict_proba(Xd[te])[:, 1]
        best = collections.defaultdict(list)
        for s, ri, yy in zip(sc, Rw, Y):
            best[ri].append((s, yy))
        a = np.zeros(len(ch))
        for ri, lst in best.items():
            m = max(s for s, _ in lst)
            top = [yy for s, yy in lst if s >= m - 1e-12]
            a[ri] = sum(top) / len(top)
        return round(float(a.mean()), 4)
    print("all", acc())
    print("drop deep", acc(drop=("deep",)))
