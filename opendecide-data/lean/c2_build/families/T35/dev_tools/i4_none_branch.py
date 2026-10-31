"""Which None branch of T35Plugin._draw fires (counts by return line), for given seeds. Dev tool; writes nothing."""
import sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(C2 / "families" / "T35"))
import pilot_loaders as PL
sys.argv = ["x"]
import importlib.util
spec = importlib.util.spec_from_file_location("rp", str(C2 / "families/T35/run_pilot_i3.py"))
rp = importlib.util.module_from_spec(spec); spec.loader.exec_module(rp)
rp.install_loader()
seeds = [int(s) for s in sys.argv_seeds] if hasattr(sys, "argv_seeds") else [900027, 900031, 900101, 900107, 900112, 900001, 900002]
cnt = collections.defaultdict(collections.Counter)
cur = {}
def tracer(frame, ev, arg):
    if frame.f_code.co_name == "_draw":
        def lt(fr, e, a):
            if e == "return":
                cnt[cur["s"]][fr.f_lineno if a is None else "ok"] += 1
            return lt
        return lt
with PL.open_family("T35") as kit:
    p = kit.plugin
    for s in seeds:
        cur["s"] = s
        print(s, p._plan(s, "S4"))
        sys.settrace(tracer)
        try:
            p.sample(s, "S4")
        except Exception as e:
            print("ERR", s, str(e)[:60])
        sys.settrace(None)
        print(s, dict(cnt[s]))
    import hashlib
    from collections import Counter
    P = sys.modules[type(p).__module__]
    for s in seeds[:5]:
        print(s, P.CH_LINES[int(P.uhash(P.FAMILY, "ch_nlines", "S4", s) * len(P.CH_LINES))], P.CH_GROUPS[int(P.uhash(P.FAMILY, "ch_ngroups", "S4", s) * len(P.CH_GROUPS))])
