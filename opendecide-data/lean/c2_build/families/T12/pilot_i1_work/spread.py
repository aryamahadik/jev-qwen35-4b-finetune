"""scratch: the report-only spread items (register, skin, wording shares) of an in-memory 1,000-row build."""
import sys, json, collections
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
sb = int(sys.argv[1]) if len(sys.argv) > 1 else pilot.SEED_BASE
with PL.open_family("T12") as kit:
    b = pilot.build_pilot(kit, 1000, seed_base=sb, run_g15=False)
    rows = [i.row for i in b.infos]
    s = pilot.spec30(b.infos, kit.plugin)['checks']
    print(sb, {k: s[k]['value'] for k in ('register_max_share', 'skin_max_rows', 'wording_max_share')}, s['cards']['min_wordings_per_card'],
          'yn', round(sum(r['qtype'] == 'noul' for r in rows) / len(rows), 3), 'mean', s['mean_tokens']['value'])
