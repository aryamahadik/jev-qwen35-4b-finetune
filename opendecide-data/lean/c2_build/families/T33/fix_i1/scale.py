"""In-memory scale check (nothing written under the family folder): build N rows with the pilot's own code path and
run G6 / G7 / G10 / overlay / spec 3.0 on them. Usage: scale.py N out.json"""
import sys, json, time, collections
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode=True
import pilot, pilot_loaders as PL
from c2_kit import cards
N=int(sys.argv[1]); OUT=sys.argv[2]; FAST=len(sys.argv)>3 and sys.argv[3]=='fast'
t0=time.time()
with PL.open_family('T33') as kit:
    b=pilot.build_pilot(kit, N, run_g15=False, log=lambda m: print(m, file=sys.stderr, flush=True))
    print('built', b.stats['rows_written'], b.stats['units_written'], b.stats['drops_by_gate'], b.stats['drop_examples'], file=sys.stderr, flush=True)
    infos=b.infos
    res={'stats':b.stats}
    res['g10']=pilot.g10(infos, b.units, kit.plugin)
    res['overlay']=pilot.overlay(b.units, kit.plugin)
    res['spec30']=pilot.spec30(infos, kit.plugin)
    rows=[i.row for i in infos]
    res['tokens']=cards.token_report(rows)
    res['styles']=cards.style_report(rows)
    # skins and registers
    sk=collections.Counter(r['meta']['c2']['skin_id'] for r in rows)
    res['skin_rows_hist']=dict(sorted(collections.Counter(sk.values()).items()))
    print('g10 done', time.time()-t0, file=sys.stderr, flush=True)
    if FAST:
        json.dump(res, open(OUT,'w'), indent=1, default=str); print('written', OUT, file=sys.stderr, flush=True); sys.exit(0)
    res['g7']=pilot.g7(infos)
    print('g7 done', time.time()-t0, file=sys.stderr, flush=True)
    res['g6']=pilot.g6(infos)
    print('g6 done', time.time()-t0, file=sys.stderr, flush=True)
json.dump(res, open(OUT,'w'), indent=1, default=str)
print('written', OUT, time.time()-t0, file=sys.stderr, flush=True)
