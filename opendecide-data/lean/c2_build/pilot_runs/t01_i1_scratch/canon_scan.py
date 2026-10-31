import sys, collections
sys.path.insert(0, '.')
import pilot_loaders as PL
from c2_kit.plugin import choose_forms
from c2_kit import skin as K
from families.T01.plugin import CHOICE_EM
N = int(sys.argv[1]) if len(sys.argv) > 1 else 800
with PL.open_family("T01") as kit:
    plugin, ctx = kit.plugin, kit.ctx
    ems = plugin.error_models()
    st = collections.defaultdict(collections.Counter)
    for sampler in ("S1", "S2", "S3", "S4", "S6"):
        for seed in range(900000, 900000 + N):
            spec = plugin.sample(seed, sampler)
            qf = spec.qform
            if qf not in CHOICE_EM or qf == "ch_cash_which":
                continue
            key = plugin._row_key(spec)
            forms = choose_forms(spec, key)
            rk = plugin._option_renderer(spec, forms)
            sk = ctx.pick("T01", "skin", key, held_out=False)
            wd = ctx.pick("T01", "wording", key, qform=spec.qform)
            slots = spec.all_slots()
            vis = (sk.fill(slots, forms).text + "\n\n" + K.fill(plugin.block_template(spec), slots, forms).text + "\n"
                   + K.fill(plugin.rule_template(spec), slots, forms, field="instructions").text + "\n\n"
                   + wd.fill(slots, forms, field="instructions").text).lower()
            gold = plugin.solve_a(spec)
            printed = plugin._printed_values(spec)
            sig = lambda a: plugin._cue_sig(qf, a, rk, vis, printed)
            cand = {}
            for n in CHOICE_EM[qf]:
                a = ems[n].fn(spec)
                if a is not None and a != gold and not (qf == "ch_days" and a < 1):
                    cand.setdefault(a, []).append(n)
            gs = sig(gold)
            c = st[qf]
            c["rows"] += 1
            for i, nm in ((0, "surf"), (1, "canon")):
                c[nm + "_gold"] += gs[i]
                c[nm + "_cand"] += sum(sig(a)[i] for a in cand); c["n_cand"] += len(cand) if i == 0 else 0
    for qf, c in sorted(st.items()):
        print(qf, "rows", c["rows"], "cands/row %.2f" % (c["n_cand"] / c["rows"]),
              "| surface gold %.3f cand %.3f | canon gold %.3f cand %.3f" % (
                  c["surf_gold"] / c["rows"], c["surf_cand"] / c["n_cand"], c["canon_gold"] / c["rows"], c["canon_cand"] / c["n_cand"]))
