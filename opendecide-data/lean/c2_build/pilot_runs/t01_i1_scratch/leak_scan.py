"""T01 scratch: structural cue scan over many choice rows (gold vs distractor rates of simple option cues)."""
import sys, collections, json
sys.path.insert(0, '.')
import pilot_loaders as PL
from c2_kit import pipeline
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
with PL.open_family("T01") as kit:
    plugin, ctx = kit.plugin, kit.ctx
    st = collections.defaultdict(lambda: collections.Counter())
    rule = collections.defaultdict(lambda: collections.Counter())
    n = 0
    for sampler in ("S1", "S2", "S3", "S4", "S6"):
        for seed in range(900000, 900000 + N):
            try:
                spec = plugin.sample(seed, sampler)
                if plugin.QFORMS[spec.qform].qtype != "choice":
                    continue
                rr = plugin.render(spec, ctx)
            except Exception as e:  # noqa
                continue
            r = rr.row
            q = spec.qform
            vis = (r["state"] + "\n" + (r.get("card") or "") + "\n" + r["instructions"]).lower()
            opts = r["options"]
            gi = opts.index(r["gold"])
            lens = [len(o) for o in opts]
            ver = [len(o) > 3 and o.lower() in vis for o in opts]
            c = st[q]
            c["rows"] += 1
            c["k_sum"] += len(opts)
            c["gold_ver"] += ver[gi]
            c["dist_ver"] += sum(ver) - ver[gi]
            c["dist_n"] += len(opts) - 1
            # rule: pick the verbatim option if exactly one is verbatim; pick the non-verbatim if exactly one is not
            nv = sum(ver)
            if nv == 1:
                rule[q]["only_ver_rows"] += 1; rule[q]["only_ver_gold"] += ver[gi]
            if nv == len(opts) - 1:
                rule[q]["only_nonver_rows"] += 1; rule[q]["only_nonver_gold"] += (not ver[gi])
            # length cues
            top = [j for j, x in enumerate(lens) if x == max(lens)]
            c["gold_longest"] += (gi in top) / len(top); c["exp_longest"] += 1 / len(opts)
            bot = [j for j, x in enumerate(lens) if x == min(lens)]
            c["gold_shortest"] += (gi in bot) / len(bot)
            n += 1
    print("rows", n)
    for q, c in sorted(st.items()):
        rows = c["rows"]
        print(q, "rows", rows, "k_mean %.2f" % (c["k_sum"] / rows),
              "gold_verbatim %.3f dist_verbatim %.3f" % (c["gold_ver"] / rows, c["dist_ver"] / max(1, c["dist_n"])),
              "longest %.3f vs %.3f" % (c["gold_longest"] / rows, c["exp_longest"] / rows),
              "shortest %.3f" % (c["gold_shortest"] / rows))
        r = rule[q]
        print("    only-one-verbatim rows %d gold-is-it %.3f | only-one-nonverbatim rows %d gold-is-it %.3f" % (
            r["only_ver_rows"], r["only_ver_gold"] / max(1, r["only_ver_rows"]), r["only_nonver_rows"],
            r["only_nonver_gold"] / max(1, r["only_nonver_rows"])))
