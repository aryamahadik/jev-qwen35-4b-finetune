import json, glob, sys
from pathlib import Path
R = {"T06":3,"T31":3,"T01":3,"T23":2,"T12":2,"T24":2,"T15":2,"T33":2,"T32":2,"T27":2,"T28":1,"T30":1,"T07":1,"T26":1,"T25":1}
def short(v, n=170): return json.dumps(v, default=str)[:n]
for p in sorted(glob.glob('../data/c2_parts/*/qc/GEN_REPORT.json')):
    g = json.load(open(p)); f = g['family']; G = g['gates']
    bd = Path(f'families/{f}/pilot_i{R[f]}')
    pr = json.load(open(bd/'PILOT_REPORT.json')) if (bd/'PILOT_REPORT.json').exists() else {}
    pg = pr.get('gates', {})
    ver = json.load(open(bd/'PILOT_VERDICT.json')) if (bd/'PILOT_VERDICT.json').exists() else {}
    print(f"=== {f} pass={g['program_pass']} failing={g['program_failing']} cands={g['n_candidates']} qtype={g['qtype']} removed={g['exclusions']['skins_removed']} dead={g['exclusions']['dead_qforms']} redrawn={g['exclusions'].get('redrawn')}")
    pq = pr.get('files', {}).get('qtype'); print('   pilot qtype', pq)
    for k in g['program_failing']:
        if k == 'G10':
            for c in G['G10']['failing_binding']:
                print(f"   G10.{c}: FULL {short(G['G10']['checks'][c]['value'])} | bar {G['G10']['checks'][c]['bar'][:70]} | PILOT {short((pg.get('G10',{}).get('checks',{}).get(c) or {}).get('value'))} [{(pg.get('G10',{}).get('checks',{}).get(c) or {}).get('verdict')}]")
        elif k == 'G6':
            for x in G['G6']['fails']:
                print(f"   G6 {x['part']}/{x['view']}/{x['model']}: FULL {x['acc']} vs chance {x['chance']} (+{100*(x['acc']-x['chance']):.2f}pp)")
            for a in glob.glob(str(bd/'G6_AT_*.json')): 
                d = json.load(open(a)); print('   PILOT G6_AT', Path(a).name, d.get('G6_verdict'), short(d.get('G6_cells_max'),200))
        else:
            d = G.get(k, {}); print(f"   {k}: FULL verdict={d.get('verdict')} {short({kk:vv for kk,vv in d.items() if kk not in ('bar',)},260)} | PILOT {short((pg.get(k) or {}).get('verdict'))}")
    if 'verdict_summary' in ver or ver: print('   pilot verdict keys', short({k: ver[k] for k in list(ver)[:6]}, 300))
