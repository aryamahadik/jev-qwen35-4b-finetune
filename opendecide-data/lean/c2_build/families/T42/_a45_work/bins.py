import sys, random, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
from families.T42 import plugin as P, gen_eq as GE
plugin, ctx = P.make_plugin()
names = [n for n in sorted(GE.SKELETONS) if n not in P.EQ_EXCLUDED]
for sk in names:
    out = {}
    for lab in P.LABELS:
        h = collections.Counter(); modes = collections.Counter()
        for t in range(300):
            R = random.Random(f"b|{sk}|{lab}|{t}")
            n_eq = R.choice([1, 2, 3, 4]) if lab == "SAME" else R.choice([0, 1, 2, 3])
            b = plugin._build_pair(R, sk, lab, n_eq, R.random() < .35, P.TRAIN_OPS)
            if b is None: h["none"] += 1; continue
            size, _ = P.tok_diff(b[0], b[1]); h[P.diff_bin(size)] += 1; modes[b[3]] += 1
        out[lab[:6] + (lab[8:11] if lab != "SAME" else "")] = [h.get(i, 0) for i in range(4)] + [h.get("none", 0)]
    print(sk, out)
