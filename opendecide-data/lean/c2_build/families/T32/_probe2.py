import sys, collections, random
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot_loaders as PL
from c2_kit.plugin import ContractError
import families.T32.plugin as M
with PL.open_family("T32") as kit:
    p = kit.plugin
    for smp in ("S2","S3","S5"):
        for seed in range(400):
            try: p.sample(seed, smp)
            except ContractError:
                pair = seed // 2
                goal = p._goal(p.__class__.__mro__[0] and "ch_due", seed, smp)
                qf = M._draw(M.BASE_SHARES, M._strat("qform", smp, idx=pair, size=50))
                card = min(M.CARDS - 1, int(M.uhash("T32", "card", smp, pair) * M.CARDS))
                g = p._goal(qf, seed, smp); sh = p._shape(smp, seed)
                rng = random.Random(f"T32|{smp}|{seed}"); c = collections.Counter()
                for _ in range(300):
                    try: p._build(rng, seed, smp, qf, card, g)
                    except M._Retry as e: c[str(e)[:50]] += 1
                    except ContractError as e: c["CE " + str(e)[:50]] += 1
                print(seed, qf, g, sh, dict(c))
