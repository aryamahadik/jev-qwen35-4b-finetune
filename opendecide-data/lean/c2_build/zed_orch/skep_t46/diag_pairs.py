"""Skeptic diagnostic for T46 (A59 review): a fresh 6,000-row QC-style build at a NON-registered seed base, then the G6 yes/no views
with folds grouped by (sampler, seed pair) instead of by card, to check that the below-chance yes/no cells of the card-grouped G6 do not
hide a positive cue. Diagnostic only; not a gate; nothing is written into any family folder.
  $PY zed_orch/skep_t46/diag_pairs.py SEEDBASE OUT.json"""
import sys, json, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import numpy as np
import gen_full_c2 as G
P = G.pilot
sb, out = int(sys.argv[1]), Path(sys.argv[2])
t0 = time.time()
with G.loader_patch("T46"):
    with G.PL.open_family("T46") as kit0:
        kit, xrep = G.apply_exclusions(kit0, set())
        b = G.pilot.build_pilot(kit, 6000, seed_base=sb, run_g15=False)
yn = [i for i in b.infos if i.row["qtype"] == "noul"]
y = np.array([int(i.row["gold"]) for i in yn])
res = {"seed_base": sb, "n_rows": len(b.infos), "n_yes_no": len(yn), "yes_rate": float(y.mean()), "gen_seconds": round(time.time() - t0)}
def folds_by(groups):
    return P._folds(groups)
pair = [f'{i.row["meta"]["sampler"]}|{i.row["meta"]["seed"] // 2}' for i in yn]
card = [i.row["meta"]["card_id"] for i in yn]
both = [f"{a}#{b_}" for a, b_ in zip(pair, card)]
views = {"a_question": [i.question for i in yn], "c_card_without_question": [i.context for i in yn]}
for gname, groups in (("card", card), ("pair", pair)):
    fl = folds_by(groups)
    for nm, tx in views.items():
        Xs = P._text_matrix(tx)
        res[f"yes_no/{nm}/groups={gname}"] = P._cv_binary(Xs, P._dense(Xs), y, fl)
    Xs, Xd = P._meta_matrices(yn)
    res[f"yes_no/d_meta/groups={gname}"] = P._cv_binary(Xs, Xd, y, fl)
# question text split into its two lines: proposed action line vs wording line
prop = [i.question.split("\n")[0] if "Proposed action" in i.question else "" for i in yn]
res["proposed_line_present"] = sum(1 for p in prop if p)
# semantic yes ("the proposed action is the right call") by (qform, asked class)
tab = {}
for i in yn:
    t = i.row["meta"]["t46"]
    c = int(t["cls"] == t["ask"]) if t["ask"] else None
    k = f'{i.row["meta"]["qform"]}|{t["ask"]}'
    a = tab.setdefault(k, [0, 0, 0]); a[0] += 1; a[1] += int(i.row["gold"]); a[2] += c
res["cell_yes_and_correct"] = {k: [v[0], round(v[1] / v[0], 3), round(v[2] / v[0], 3)] for k, v in sorted(tab.items())}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(res, indent=1))
print(json.dumps(res)[:1500])
