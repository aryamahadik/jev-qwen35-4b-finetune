"""Scan: sample() over seeds for each sampler; counts failures. Dev tool; writes nothing."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2))
import importlib.util, pilot_loaders as PL
spec = importlib.util.spec_from_file_location("rp", str(C2 / "families/T35/run_pilot_i3.py"))
rp = importlib.util.module_from_spec(spec); spec.loader.exec_module(rp); rp.install_loader()
a, b = int(sys.argv[1]), int(sys.argv[2])
with PL.open_family("T35") as kit:
    p = kit.plugin
    bad = {}
    for smp in ("S1", "S2", "S3", "S4", "S5"):
        for s in range(a, b):
            try:
                if smp == "S5" and not p.card_packs.get("S5"):
                    continue
                p.sample(s, smp)
            except Exception as e:
                bad.setdefault(smp, []).append((s, str(e)[:70]))
    print({k: (len(v), v[:3]) for k, v in bad.items()})
