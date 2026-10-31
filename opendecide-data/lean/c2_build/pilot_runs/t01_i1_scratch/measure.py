import sys, json, collections
sys.path.insert(0, '.')
import pilot, pilot_loaders as PL
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
with PL.open_family("T01") as kit:
    plugin = kit.plugin
    b = pilot.build_pilot(kit, n, run_g15=False, log=lambda m: None)
    rows = [i.row for i in b.infos]
    print("rows", len(rows), "units", b.stats["units_written"], "attempted", b.stats["units_attempted"], "drops", b.stats["drops_by_gate"])
    edge = collections.Counter(t for r in rows for t in (r["meta"].get("edge") or []))
    print("boundary share of rows %.3f" % (edge["boundary"] / len(rows)))
    print("edge tags", {k: round(v / len(rows), 3) for k, v in edge.most_common(12)})
    qt = collections.Counter(r["qtype"] for r in rows)
    print("yes/no share %.3f" % (qt["noul"] / len(rows)))
    # base qform drop rate: attempts per qform: re-sample same seeds
    att = collections.Counter(); ok = collections.Counter()
    okseeds = {(r["meta"]["sampler"], r["meta"]["seed"]) for r in rows if r["role"] == "base"}
    for smp in b.stats["training_samplers"]:
        for k in range(b.stats["seeds_per_sampler"]):
            seed = b.stats["seed_base"] + k
            spec = plugin.sample(seed, smp)
            q = spec.qform
            att[q] += 1
            ok[q] += (smp, seed) in okseeds
    for q in sorted(att):
        if q.startswith("ch_"):
            print("  %-15s attempted %4d kept %4d (%.0f%%)" % (q, att[q], ok[q], 100 * ok[q] / att[q]))
    kk = collections.Counter(len(r["options"]) for r in rows if r["qtype"] == "choice")
    print("k counts", dict(kk))
    print("ch qform rows", dict(collections.Counter(r["meta"]["qform"] for r in rows if r["qtype"] == "choice")))
