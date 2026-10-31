import sys, time, collections, re
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
from families.T42 import plugin as P, gen_pad as GP
plugin, ctx = P.make_plugin()
t0 = time.time()
sets = collections.defaultdict(list)
for seed in range(0, 39):
    try:
        sp = plugin.sample(seed, "S3")
    except Exception as e:
        print("fail", seed, repr(e)[:150]); continue
    st = sp.structure
    toks = frozenset(P.TOK_RE.findall((st["f"] + "\n" + st["g"]).lower()))
    sets[st["skeleton"]].append((st["label"], toks, GP.n_numbers(st["f"]), round(GP.mag_sum(st["f"]), 3), round(GP.mag_sum(st["g"]), 3), st["attempt"]))
print("secs", round(time.time() - t0), dict(P.DIAG))
for sk, v in sets.items():
    base = set(plugin._vocab(sk, P.TRAIN_OPS))
    print(sk, [(l[:4], len(t - base), len(base - t), q, a, b, at) for l, t, q, a, b, at in v])
