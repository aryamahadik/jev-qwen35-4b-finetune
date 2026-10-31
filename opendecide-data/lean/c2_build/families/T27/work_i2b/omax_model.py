"""Scratch: one-feature (in-sample majority per value) accuracy of the MODEL overlap (items excluded) on infos_after.pkl."""
import sys, pickle, collections
sys.dont_write_bytecode = True
from pathlib import Path
C2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
for p in (str(C2), str(C2 / "families" / "T27")):
    sys.path.insert(0, p)
import pilot_loaders as PL, run_pilot as RP, run_pilot_i2 as R2
R2._install_supplement(); PL.LOADERS["T27"] = RP._t27; PL.open_family = RP._redirect(R2.OUT_NAME)
infos = pickle.load(open(str(C2 / "families/T27/work_i2b/infos_after.pkl"), "rb"))
with PL.open_family("T27") as kit:
    from families.T27 import plugin as P, overlap as OV
    pl = kit.plugin; m = pl._ovl()
    by = collections.defaultdict(collections.Counter); n = 0
    form_by = collections.defaultdict(collections.Counter)
    for i in infos:
        sp = i.spec
        if sp.qform != "ch_next": continue
        env = sp.env()
        os_ = [m.o(env["TASK"], sp.slots["TASK"].value[1], a, sp.slots[f"REQ{k}"].value[1]) for k, a, _, _ in P.asked_actions(env)]
        y = pl.solve_a(sp)
        by[round(max(os_), 2)][y] += 1
        for k, a, _, _ in P.asked_actions(env):
            form_by[sp.slots[f"REQ{k}"].value[1]][y] += 1
        n += 1
    acc = sum(max(c.values()) for c in by.values()) / n
    out = [f"choice rows {n}; model o_max values {len(by)}; in-sample majority-per-value accuracy {acc:.4f} (chance 0.3333)"]
    for v in sorted(by): out.append(f"  o_max={v} n={sum(by[v].values())} " + str(dict(by[v])))
    facc = sum(max(c.values()) for c in form_by.values()) / sum(sum(c.values()) for c in form_by.values())
    out.append(f"request-form identity: {len(form_by)} forms, in-sample majority accuracy {facc:.4f}")
    open(str(C2 / "families/T27/work_i2b/omax_model.txt"), "w").write("\n".join(out)); print("\n".join(out[:12]))
