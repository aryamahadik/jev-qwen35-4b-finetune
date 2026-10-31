import sys, collections
sys.path.insert(0, '.')
import pilot_loaders as PL
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
with PL.open_family("T01") as kit:
    plugin, ctx = kit.plugin, kit.ctx
    cnt = collections.Counter(); lenr = collections.Counter(); valr = collections.Counter()
    for sampler in ("S4",):
        for seed in range(900000, 900000 + 4 * N):
            try:
                spec = plugin.sample(seed, sampler)
                if spec.qform != "ch_total":
                    continue
                rr = plugin.render(spec, ctx)
            except Exception:
                continue
            os_ = rr.option_set
            k = len(os_.options)
            keys = [o.key for o in os_.options]
            gk = os_.gold.key
            vr = sorted(keys).index(gk)
            texts = [o.text for o in os_.options]
            lens = [len(t) for t in texts]
            gl = lens[os_.gold_index]
            below = sum(1 for x in lens if x < gl); eq = sum(1 for x in lens if x == gl) - 1
            cnt[k] += 1
            valr[(k, vr)] += 1
            lenr[(k, below, eq)] += 1
    print("k counts", dict(cnt))
    print("value rank", sorted(valr.items()))
    print("length rank (k, below, ties)", sorted(lenr.items()))
