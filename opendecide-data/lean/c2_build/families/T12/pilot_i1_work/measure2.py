"""scratch: token mean under overridden generator constants. usage: measure2.py N 'json overrides'"""
import sys, json, collections, time
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
from c2_kit import cards
from families.T12 import plugin as P
n = int(sys.argv[1]); ov = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
for k, v in ov.items():
    if k in ('LINES_W', 'QFORM_SHARES'): v = tuple(tuple(x) for x in v)
    if k == 'COMPLEMENT_RATE': v = {**P.COMPLEMENT_RATE, **v}
    setattr(P, k, v)
t = time.time()
with PL.open_family("T12") as kit:
    b = pilot.build_pilot(kit, n, run_g15=False)
    rows = [i.row for i in b.infos]
    rep = cards.token_report(rows)
    q = collections.Counter(r['qtype'] for r in rows)
    print(json.dumps({'ov': ov, 'rows': len(rows), 'mean': rep['mean'], 'max': rep['max'], 'yn': round(rep['yes_no_share'], 3),
                      'drops': b.stats['drops_by_gate'], 'fm': rep['field_means'], 's': round(time.time() - t)}))
