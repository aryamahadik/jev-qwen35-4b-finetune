"""Dev tool (A45 c, T35 pass 2): per-row shape table of the choice rows (6,000-row in-memory build; writes only the pkl given).
  ../../.venv/bin/python -B families/T35/dev_tools/i4b_rows.py build N out.pkl
"""
import pickle, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2])); sys.path.insert(0, str(HERE.parent))
import pilot as PI, pilot_loaders as PL
import run_pilot_i4 as R
R.install_loader()
n, out = int(sys.argv[2]), sys.argv[3]
with PL.open_family("T35") as kit:
    b = PI.build_pilot(kit, n, run_g15=False)
rows = []
for i in b.infos:
    r = i.row
    if r["qtype"] != "choice":
        continue
    o = r["options"]; kd = PI.option_kinds(i); gi = o.index(r["gold"])
    cl = [len(x) for x in o]
    rows.append(dict(opts=list(o), gold=r["gold"], sampler=r["meta"].get("sampler"), qform=r["meta"].get("qform"), k=len(o), gold_abs="kind:abstain" in kd[gi],
                     gold_pos=gi, clen=cl, gold_clen=cl[gi], len_state=len(r["state"]), n_lines=r["state"].count("\n") + 1,
                     len_q=len(i.question), len_ins=len(r.get("instructions") or ""), card=r["meta"]["card_id"],
                     status_show="STATUS" in str(r["meta"]) , kinds=[sorted(x) for x in kd]))
pickle.dump(rows, open(out, "wb")); print(len(rows))
