import sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import gen_full_c2 as G
N = int(sys.argv[1])
with G.loader_patch("T32"):
    with G.PL.open_family("T32") as kit:
        pl = kit.plugin; P = sys.modules[type(pl).__module__]
        base = collections.Counter(); tw = collections.Counter(); k = 0; n = 0; extra = collections.Counter()
        while n < N:
            seed, smp = 62_000_000 + k // 4, ["S1", "S2", "S3", "S4"][k % 4]; k += 1
            if P._draw(P.BASE_SHARES, P._strat("qform", smp, idx=seed // 2, size=50)) != "ch_status": continue
            sp = pl.sample(seed, smp); n += 1
            st = pl._fold(sp)[0]; base[st] += 1
            for r in pl.relations(sp):
                if r.kind == "twin": tw[pl._fold(r.spec)[0]] += 1
                elif r.kind in ("equiv", "inv"): extra[st] += 1
print("base", dict(base)); print("twin", dict(tw)); print("equiv/inv", dict(extra))
tot = collections.Counter(); 
for d in (base, tw, extra): tot.update(d)
T = sum(tot.values()); print({s: round(tot[s] / T, 3) for s in tot}, "twins/base", round(sum(tw.values()) / N, 3))
