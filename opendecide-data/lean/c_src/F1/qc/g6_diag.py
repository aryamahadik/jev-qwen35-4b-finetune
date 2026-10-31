"""G6 diagnostic (independent F1 checker): (d) metadata baselines without construction-only fields (twin_kind,
row role, unit_kind) and per-feature-group ablations, to locate the cue. Writes qc/g6_diag_<name>.json."""
import json, sys
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MaxAbsScaler
import qc_lib as q
from g6 import cv_yn, cv_ch, optset

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
rows, side = q.load(NAME)
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
DROP = ("sc_twin_kind", "sc_role", "sc_unit_kind")
out = {}
y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
base = []
for r in yn:
    c, n = q.meta_feats(r, side.get(r["id"]))
    base.append({**{f"{k}={v}": 1.0 for k, v in c.items() if k not in DROP}, **n})
def run_yn(fs):
    X = DictVectorizer().fit_transform(fs).tocsr(); return cv_yn(MaxAbsScaler().fit_transform(X), X.toarray(), y, g)
out["yn_d_no_construction"] = run_yn(base)
for grp in ("sc_X_role", "sc_policy", "sc_n_amend", "sc_world", "sc_tie", "wording_id", "format_style"):
    out[f"yn_only_{grp}"] = run_yn([{k: v for k, v in d.items() if k.startswith(grp)} or {"none": 1.0} for d in base])
out["yn_chance"] = round(float(max(y.mean(), 1 - y.mean())), 4)
prow, yp, gp, F = [], [], [], []
for ri, r in enumerate(ch):
    s = side.get(r["id"]) or {}; roles = s.get("option_roles") or ["?"] * len(r["options"])
    os_ = optset(r, roles); c, n = q.meta_feats(r, s)
    m = {**{f"{k}={x}": 1.0 for k, x in c.items() if k not in DROP}, **n}
    for i, o in enumerate(r["options"]):
        d = dict(m); d.update({"o_" + k: x for k, x in os_[i].items()}); d["role=" + str(roles[i])] = 1.0
        prow.append(ri); yp.append(int(o == r["gold"])); gp.append(r["meta"]["card_id"]); F.append(d)
yp = np.array(yp)
def run_ch(fs):
    X = DictVectorizer().fit_transform(fs).tocsr(); return cv_ch(MaxAbsScaler().fit_transform(X), X.toarray(), yp, prow, gp)
out["ch_d_no_construction"] = run_ch(F)
out["ch_role_plus_world_qtype"] = run_ch([{k: v for k, v in d.items() if k.startswith(("role=", "sc_world", "sc_qtype", "k_opts"))} for d in F])
out["ch_optionset_only"] = run_ch([{k: v for k, v in d.items() if k.startswith("o_")} for d in F])
out["ch_chance"] = round(float(np.mean([1 / len(r["options"]) for r in ch])), 4)
(q.QC / f"g6_diag_{NAME}.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
