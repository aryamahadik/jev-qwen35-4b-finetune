"""Scratch: which numeric metadata feature drives the choice d_meta gbt cell at 6,000 rows (report only)."""
import sys, json
from pathlib import Path
from collections import defaultdict
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2))
import numpy as np
import pilot, pilot_loaders as PL
from sklearn.feature_extraction import DictVectorizer

with PL.open_family("T33") as kit:
    b = pilot.build_pilot(kit, 6000, run_g15=False)
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
T, D, Y, Rw = pilot._pair_rows(ch, "d_meta")
Y, Rw = np.array(Y), np.array(Rw)
groups = np.array([ch[ri].row["meta"]["card_id"] for ri in Rw])
folds = pilot._folds(list(groups))
keys = sorted(D[0])
num_meta = ["len_state", "len_ins", "len_card", "len_q", "k", "n_numbers", "mag_max", "mag_mean", "depth", "deep", "n_lines"]


def acc_for(drop):
    DD = [{k: v for k, v in d.items() if k not in drop} for d in D]
    Xd = DictVectorizer(sparse=False).fit_transform(DD)
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sc[te] = pilot._gbt().fit(Xd[tr], Y[tr]).predict_proba(Xd[te])[:, 1]
    best = defaultdict(list)
    for s, ri, yy in zip(sc, Rw, Y):
        best[ri].append((s, yy))
    tot = 0.0
    for lst in best.values():
        m = max(s for s, _ in lst)
        top = [yy for s, yy in lst if s >= m - 1e-12]
        tot += sum(top) / len(top)
    return round(tot / len(best), 4)


out = {"all": acc_for(set()), "n_choice": len(ch)}
for k in num_meta:
    out["drop_" + k] = acc_for({k})
out["only_option_feats"] = acc_for(set(num_meta))
by_q = defaultdict(list)
for i in ch:
    by_q[i.row["meta"].get("qform")].append(i)
out["qform_counts"] = {k: len(v) for k, v in by_q.items()}
Path(__file__).with_name("diag_dmeta.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
