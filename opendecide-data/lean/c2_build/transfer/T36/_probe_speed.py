import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import pilot_loaders as PL
from transfer.T36 import plugin as P
with PL.open_family("T36") as kit:
    pl = kit.plugin
    t = time.time(); n = 0
    for k in range(400):
        s = ["S1","S2","S3","S4"][k % 4]; seed = 3_000_000 + k // 4
        kind, _ = P.slot_of(s, seed)
        if kind != "choice": continue
        spec = pl.sample(seed, s); n += 1
    print(n, time.time() - t)
