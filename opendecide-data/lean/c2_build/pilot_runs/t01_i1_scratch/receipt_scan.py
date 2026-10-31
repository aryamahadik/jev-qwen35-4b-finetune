import sys, collections
sys.path.insert(0, '.')
import pilot_loaders as PL
from c2_kit.plugin import choose_forms
from families.T01.plugin import CHOICE_EM
N = int(sys.argv[1]) if len(sys.argv) > 1 else 800
qf = sys.argv[2] if len(sys.argv) > 2 else "ch_receipt_day"
sampler = sys.argv[3] if len(sys.argv) > 3 else "S6"
with PL.open_family("T01") as kit:
    plugin, ctx = kit.plugin, kit.ctx
    ems = plugin.error_models()
    c = collections.Counter()
    ex = []
    for seed in range(900000, 900000 + N):
        spec = plugin.sample(seed, sampler)
        if spec.qform != qf:
            continue
        key = plugin._row_key(spec)
        forms = choose_forms(spec, key)
        rk = plugin._option_renderer(spec, forms)
        try:
            rr = plugin.render.__wrapped__(spec, ctx) if hasattr(plugin.render, "__wrapped__") else None
        except Exception:
            rr = None
        # build the visible text without options: render the row from the unfiltered path
        from c2_kit import skin as K
        sk = ctx.pick("T01", "skin", key, held_out=False)
        wd = ctx.pick("T01", "wording", key, qform=spec.qform)
        slots = spec.all_slots()
        vis = (sk.fill(slots, forms).text + "\n\n" + K.fill(plugin.block_template(spec), slots, forms).text + "\n"
               + K.fill(plugin.rule_template(spec), slots, forms, field="instructions").text + "\n\n"
               + wd.fill(slots, forms, field="instructions").text).lower()
        gold = plugin.solve_a(spec)
        printed = plugin._printed_values(spec)
        sig = lambda a: plugin._cue_sig(qf, a, rk, vis, printed)
        gs = sig(gold)
        cand = {}
        for n in CHOICE_EM[qf]:
            a = ems[n].fn(spec)
            if a is not None and a != gold:
                cand.setdefault(a, []).append(n)
        def sides(keep):
            b = sum(1 for a in cand if a < gold and keep(a)); u = sum(1 for a in cand if a > gold and keep(a))
            return b, u
        c["rows"] += 1
        c["gold_surface"] += gs[0]; c["gold_canon"] += gs[1]
        for name, keep in (("none", lambda a: True), ("same_sig", lambda a: sig(a) == gs),
                           ("same_canon", lambda a: sig(a)[1] == gs[1]), ("same_surface", lambda a: sig(a)[0] == gs[0]),
                           ("canon0", lambda a: not sig(a)[1]), ("canon1", lambda a: sig(a)[1])):
            b, u = sides(keep)
            c[name + "_both_sides"] += (b >= 1 and u >= 1)
        ex.append((gs, [(a, sig(a)) for a in cand]))
    n = c["rows"]
    print(qf, "rows", n, "gold surface %.3f canon %.3f" % (c["gold_surface"] / n, c["gold_canon"] / n))
    for name in ("none", "same_sig", "same_canon", "same_surface", "canon0", "canon1"):
        print("  %-13s both sides available %.3f" % (name, c[name + "_both_sides"] / n))
    for gs, lst in ex[:6]:
        print("   gold", gs, lst)
