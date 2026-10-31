import sys, collections
sys.path.insert(0, '.')
import pilot_loaders as PL
from c2_kit.plugin import choose_forms
N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
with PL.open_family("T01") as kit:
    plugin, ctx = kit.plugin, kit.ctx
    ems = plugin.error_models()
    from families.T01.plugin import CHOICE_EM
    stat = collections.defaultdict(collections.Counter)
    for sampler in ("S1", "S2", "S3", "S4", "S6"):
        for seed in range(900000, 900000 + N):
            try:
                spec = plugin.sample(seed, sampler)
                if plugin.QFORMS[spec.qform].qtype != "choice":
                    continue
                rr = plugin.render(spec, ctx)
            except Exception:
                continue
            r = rr.row
            q = spec.qform
            key = plugin._row_key(spec)
            forms = choose_forms(spec, key)
            rk = plugin._option_renderer(spec, forms)
            vis = (r["state"] + "\n" + (r.get("card") or "") + "\n" + r["instructions"]).lower()
            gold = plugin.solve_a(spec)
            gt = rk(gold)
            gp = len(gt) > 3 and gt.lower() in vis
            outs = {}
            for n in CHOICE_EM[q]:
                a = ems[n].fn(spec)
                if a is None or a == gold:
                    continue
                outs.setdefault(a, []).append(n)
            c = stat[q]
            c["rows"] += 1
            c["gold_printed"] += gp
            ncand = len(outs)
            same_len = sum(1 for a in outs if len(rk(a)) == len(gt))
            printed = sum(1 for a in outs if (len(rk(a)) > 3 and rk(a).lower() in vis) == gp)
            both = sum(1 for a in outs if len(rk(a)) == len(gt) and (len(rk(a)) > 3 and rk(a).lower() in vis) == gp)
            for name, v in (("cand", ncand), ("samelen", same_len), ("sameprint", printed), ("both", both)):
                for t in (1, 2, 3):
                    c[f"{name}>={t}"] += v >= t
    for q, c in sorted(stat.items()):
        n = c["rows"]
        print(q, "rows", n, "gold_printed %.3f" % (c["gold_printed"] / n))
        for name in ("cand", "samelen", "sameprint", "both"):
            print("    %-9s >=1 %.3f  >=2 %.3f  >=3 %.3f" % (name, c[f"{name}>=1"] / n, c[f"{name}>=2"] / n, c[f"{name}>=3"] / n))
