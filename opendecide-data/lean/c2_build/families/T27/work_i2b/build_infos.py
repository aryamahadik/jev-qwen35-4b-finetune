"""Scratch (never a gate): in-memory N-row T27 build with the run_pilot_i2 setup; pickles the RowInfos for cue analysis.
usage (from lean/c2_build): ../../.venv/bin/python -B families/T27/work_i2b/build_infos.py N OUT.pkl"""
import pickle
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
for p in (str(C2), str(C2 / "families" / "T27")):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.setrecursionlimit(20000)
import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
import run_pilot as RP  # noqa: E402
import run_pilot_i2 as R2  # noqa: E402

N = int(sys.argv[1])
out = sys.argv[2]
R2._install_supplement()
PL.LOADERS["T27"] = RP._t27
PL.open_family = RP._redirect(R2.OUT_NAME)
t0 = time.time()
with PL.open_family("T27") as kit:
    b = pilot.build_pilot(kit, N, run_g15=False, log=lambda m: print(m, file=sys.stderr, flush=True))
print("built", len(b.infos), round(time.time() - t0), "s", flush=True)
try:
    pickle.dump(b.infos, open(out, "wb"))
    print("pickled full infos", flush=True)
except Exception as e:  # noqa: BLE001
    print("full pickle failed:", repr(e)[:300], flush=True)
    from types import SimpleNamespace as NS
    lite = []
    for i in b.infos:
        os_ = getattr(i.rr, "option_set", None) if i.rr is not None else None
        ops = None if os_ is None else NS(meta=dict(os_.meta), options=[NS(text=o.text, role=o.role, key=o.key) for o in os_.options])
        st = getattr(i.spec, "structure", None)
        lite.append(NS(row=i.row, question=i.question, context=i.context, unit=i.unit, ff_text=i.ff_text,
                       rr=NS(attack_id=getattr(i.rr, "attack_id", None), option_set=ops),
                       structure=st, qform=getattr(i.spec, "qform", None)))
    pickle.dump(lite, open(out, "wb"))
    print("pickled lite infos", flush=True)
