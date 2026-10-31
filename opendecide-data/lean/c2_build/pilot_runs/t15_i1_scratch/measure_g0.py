"""G0 section 2 numbers for v1.3: 2,000 training specs (seeds 0-499 x S1-S4) and 1,500 relation units (seeds 0-299 x S1-S5)."""
import sys, collections, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
from concurrent.futures import ProcessPoolExecutor

def units(rng):
    lo, hi = rng
    import pilot_loaders as PL
    from c2_kit import pipeline
    out = []
    with PL.open_family('T15') as kit:
        plugin, ctx = kit.plugin, kit.ctx
        for seed in range(lo, hi):
            for smp in plugin.SAMPLERS:
                spec = plugin.sample(seed, smp)
                res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
                assert res.ok, res.problems[:2]
                out.append((spec.seed, smp, [(r['role'], r['qtype'], r['meta']['qform'], r['gold'], len(r['options'] or []), bool(r['options'] and 'Nobody may claim the child' in r['options']), r['meta']['twin_kind'], r['meta']['deep']) for r in res.rows]))
    return out

if __name__ == '__main__':
    import pilot_loaders as PL
    from families.T15 import plugin as T
    with PL.open_family('T15') as kit:
        plugin = kit.plugin
        specs = [plugin.sample(seed, smp) for seed in range(500) for smp in ('S1', 'S2', 'S3', 'S4')]
        gates = [s for s in specs if s.structure['track'] == 'gates']; claims = [s for s in specs if s.structure['track'] == 'claimants']
        out = collections.Counter(plugin.solve_a(s) for s in gates if s.qform == 'ch_outcome'); tot = sum(out.values())
        print('ch_outcome', {k: round(v / tot, 3) for k, v in sorted(out.items())}, tot)
        for k in (2, 3, 4):
            ss = [s for s in gates if s.qform == 'ch_outcome' and len(s.structure['gates']) == k]
            print(' eligible, gates', k, round(sum(plugin.solve_a(s) == 'eligible' for s in ss) / len(ss), 3), len(ss))
        who = [plugin.solve_a(s) for s in claims if s.qform == 'ch_claimant']
        print('ch_claimant gold none', round(sum(a == 'none' for a in who) / len(who), 3), len(who))
        print('deep gates', round(sum(s.deep for s in gates) / len(gates), 3), 'claims', round(sum(s.deep for s in claims) / len(claims), 3), 'family', round(sum(s.deep for s in specs) / len(specs), 3))
    chunks = [(a, a + 50) for a in range(0, 300, 50)]
    allu = []
    t0 = time.time()
    with ProcessPoolExecutor(6) as ex:
        for o in ex.map(units, chunks): allu += o
    rows = [r for _, _, rs in allu for r in rs]
    n = len(rows); print('units', len(allu), 'rows', n, round(time.time() - t0))
    yn = [r for r in rows if r[1] == 'noul']
    print('yes/no share', round(len(yn) / n, 3), 'twin', round(sum(r[6] == 'minimal_edit' for r in rows) / n, 3), 'equiv', round(sum(r[6] == 'equiv' for r in rows) / n, 3), 'attack', round(sum(r[6] == 'attack' for r in rows) / n, 3), 'deep', round(sum(r[7] for r in rows) / n, 3))
    cc = [r for r in rows if r[2] == 'ch_claimant']
    shown = [r for r in cc if r[5]]
    print('ch_claimant rows', len(cc), 'shown', round(len(shown) / len(cc), 3), 'gold nobody (shown)', sum(r[3] == 'Nobody may claim the child' for r in shown), 'share', round(sum(r[3] == 'Nobody may claim the child' for r in shown) / len(shown), 3))
    print('k dist', collections.Counter(r[4] for r in cc))
