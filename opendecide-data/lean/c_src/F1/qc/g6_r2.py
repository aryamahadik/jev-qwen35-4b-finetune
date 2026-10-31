"""G6 (check:F1, workflow c-lanes-v3). Same views, models and 5-fold GroupKFold-by-card CV as qc/g6.py (the earlier
independent checker's script, imported unchanged), but view (d) uses ONLY metadata the model sees (workflow rule
"G6 metadata = only what the model sees"): surface/format ids that change the rendered text (format_style, wording_id,
defs_style), properties stated in the rendered card or question (qtype, world, policy, tie, attack, polarity,
X_role = role of the outcome named in a yes/no question, label_form), counts readable from the text (rules,
amendments, elements, options, tokens, lengths, numbers in the question), and option-set features / option roles.
Dropped (generator internals, not visible): sampler, unit_kind, twin_kind, short, deep, depth, n_inert, k_syn,
k_all, edge, row role. Usage: g6_r2.py NAME yn|ch -> qc/g6_r2_NAME_<part>.json; g6_r2.py NAME merge. Counts only."""
import json, math, sys, time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MaxAbsScaler
import qc_lib as q
import g6

VIS_CAT = ("qtype", "world", "policy", "tie", "attack", "pol", "X_role", "label_form")
VIS_NUM = ("n_rules", "n_amend", "n_elements", "len_tokens", "k")


def meta_vis(r, s):
    m = r["meta"]; v = q.views(r); s = s or {}
    cat = {k: str(m.get(k)) for k in ("format_style", "wording_id", "defs_style")}
    for k in VIS_CAT:
        if k in s:
            cat["sc_" + k] = str(s.get(k))
    num = {"len_state": len(r["state"]), "len_ins": len(r["instructions"]), "len_card": len(r.get("card") or ""),
           "n_lines_state": r["state"].count("\n"), "k_opts": len(v["opts"]) if not q.is_yn(r) else 2}
    for k in VIS_NUM:
        x = s.get(k)
        num["sc_" + k] = float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else -1.0
    nums = [float(x.replace(",", "")) for x in q.NUM_RX.findall(v["q"])][:20]
    num["q_n_numbers"] = len(nums); num["q_max_num_log"] = math.log1p(max(nums)) if nums else 0.0
    roles = s.get("option_roles") or []
    for ro in ("default", "escalate", "fallback", "M", "cbd", "none", "case", "other"):
        num["n_role_" + ro] = float(sum(1 for x in roles if x == ro))
    if s.get("code_share") is not None:
        num["code_share"] = float(s["code_share"])
    return cat, num


q.meta_feats = meta_vis  # g6 calls q.meta_feats at run time


def run_yn(rows, side, out):
    yn = [r for r in rows if q.is_yn(r)]
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = round(float(max(y.mean(), 1 - y.mean())), 4)
    V = [q.views(r) for r in yn]
    for key, f in (("a_question", "q"), ("c_card_without_question", "cardnoq")):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
        Xs = tv.fit_transform([v[f] for v in V]).tocsr(); Xd = TruncatedSVD(64, random_state=0).fit_transform(Xs)
        res = g6.cv_yn(Xs, Xd, y, g); best = max(res.values())
        out["yes_no"][key] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02}
        g6.log(f"yn {key} {out['yes_no'][key]}")
    md = []
    for r in yn:
        c, n = meta_vis(r, side.get(r["id"])); md.append({**{f"{k}={v}": 1.0 for k, v in c.items()}, **n})
    Xm = DictVectorizer().fit_transform(md).tocsr()
    res = g6.cv_yn(MaxAbsScaler().fit_transform(Xm), Xm.toarray(), y, g); best = max(res.values())
    out["yes_no"]["d_metadata_visible"] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02}
    g6.log(f"yn d {out['yes_no']['d_metadata_visible']}")
    out["yes_no"]["b_options"] = "n/a (yes/no options fixed)"
    out["n_yes_no"] = len(yn)


def main():
    name, part = sys.argv[1], sys.argv[2]
    if part == "merge":
        res = {"gate": "G6", "file": f"out/{name}.jsonl", "cv": "GroupKFold(5) by meta.card_id",
               "rule": "acc <= chance + 2 pp", "metadata": "model-visible only (see g6_r2.py docstring)"}
        for p in ("yn", "ch"):
            d = json.loads((q.QC / f"g6_r2_{name}_{p}.json").read_text())
            for k in ("yes_no", "choice"):
                if d.get(k):
                    res[k] = d[k]
            res[f"seconds_{p}"] = d.get("seconds")
        flat = [v["pass"] for part_ in ("yes_no", "choice") for k, v in res[part_].items()
                if isinstance(v, dict) and "pass" in v]
        res["pass"] = bool(flat) and all(flat)
        (q.QC / f"g6_r2_{name}.json").write_text(json.dumps(res, indent=1))
        print(json.dumps({"pass": res["pass"], **{f"{p}:{k}": v.get("best") for p in ("yes_no", "choice")
                                                for k, v in res[p].items() if isinstance(v, dict) and "best" in v}}))
        return
    rows, side = q.load(name)
    g6.log(f"rows {len(rows)} part {part}")
    out = {"yes_no": {}, "choice": {}}
    if part == "yn":
        run_yn(rows, side, out)
    else:
        g6.choice_part([r for r in rows if not q.is_yn(r)], side, out)
    out["seconds"] = round(time.time() - g6.T0, 1)
    (q.QC / f"g6_r2_{name}_{part}.json").write_text(json.dumps(out, indent=1))
    g6.log("done")


if __name__ == "__main__":
    main()
