"""scratch (verdict diagnosis): why does the yes/no a_question view reach 0.522 at 6,000 rows? Builds in memory, writes a
small JSON of yes rates by qform / wording / card, and the CV accuracy of qform-only and wording-only predictors."""
import sys, json, time
from collections import defaultdict
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
import numpy as np

with PL.open_family("T12") as kit:
    b = pilot.build_pilot(kit, 6000, run_g15=False)
    infos = b.infos
    yn = [i for i in infos if i.row["qtype"] == "noul"]
    print("n yes/no", len(yn), "meta keys", sorted(yn[0].row["meta"].keys()))
    y = np.array([int(i.row["gold"]) for i in yn])
    print("yes rate", y.mean())
    out = {"n_yn": len(yn), "yes_rate": float(y.mean())}
    by_q = defaultdict(list)
    for i in yn:
        by_q[i.row["meta"].get("qform")].append(int(i.row["gold"]))
    out["by_qform"] = {k: [len(v), round(sum(v) / len(v), 4)] for k, v in sorted(by_q.items(), key=lambda kv: str(kv[0]))}
    print(json.dumps(out["by_qform"], indent=0))
    # question-only text predictors, same CV folds as G6
    folds = pilot._folds([i.row["meta"]["card_id"] for i in yn])
    qf = [str(i.row["meta"].get("qform")) for i in yn]

    def cv_acc(keys):
        correct = 0
        for tr, te in folds:
            d = defaultdict(list)
            for j in tr:
                d[keys[j]].append(y[j])
            glob = float(np.mean([y[j] for j in tr]))
            for j in te:
                r = np.mean(d[keys[j]]) if keys[j] in d else glob
                correct += int((r > 0.5) == bool(y[j])) if r != 0.5 else int(y[j] == 1)
        return correct / len(yn)
    out["cv_qform_only"] = round(cv_acc(qf), 4)
    wk = [i.question for i in yn]
    # wording = the question with ids masked is not exposed; use the template tag of the row if present
    tags = []
    for i in yn:
        t = [x for x in (i.row["meta"].get("templates") or []) if "-WD-" in str(x)]
        tags.append(t[0] if t else "none")
    out["cv_wording_tag_only"] = round(cv_acc(tags), 4)
    print(out["cv_qform_only"], out["cv_wording_tag_only"])
    # per-card yes rates and per-wording
    byw = defaultdict(list)
    for t, yy in zip(tags, y):
        byw[t].append(int(yy))
    out["wording_rates_n>=30"] = {k: [len(v), round(sum(v) / len(v), 3)] for k, v in sorted(byw.items()) if len(v) >= 30}
    json.dump(out, open("families/T12/pilot_i1_work/g6_diag_i1.json", "w"), indent=1)
