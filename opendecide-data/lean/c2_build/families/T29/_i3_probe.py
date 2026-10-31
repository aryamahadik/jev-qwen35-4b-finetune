"""Scratch probe (iteration 3): rows by (qform, twin_kind) of a pilot build, with the yes_is_bad flag."""
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
with PL.open_family("T29") as kit:
    b = PI.build_pilot(kit, n, run_g15=False)
    qf = kit.plugin.QFORMS
    c = Counter()
    for i in b.infos:
        r = i.row
        if r["qtype"] != "noul":
            continue
        q = r["meta"]["qform"]
        c[(q, r["meta"]["twin_kind"], qf[q].yes_is_bad)] += 1
    tot = sum(c.values())
    bad = sum(v for k, v in c.items() if k[2])
    print("yn rows", tot, "bad share", bad / tot)
    for k in sorted(c, key=str):
        print(k, c[k])
    print("units", len(b.units), "rows", len(b.infos))
