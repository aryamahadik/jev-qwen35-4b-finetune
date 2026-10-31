"""scratch: balance numbers of the v2.2 generator for the G0 text (real pools, units with the spec 4.1 overlay)."""
import sys, json, collections
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
from c2_kit import pipeline, cards
import negcount
n = int(sys.argv[1])
with PL.open_family("T12") as kit:
    pl = kit.plugin
    b = pilot.build_pilot(kit, n, run_g15=False)
    rows = [i.row for i in b.infos]
    yn = [r for r in rows if r['qtype'] == 'noul']
    ov = pipeline.overlay_report(b.units, pl)
    bad = sum(bool(pl.QFORMS[r['meta']['qform']].yes_is_bad) for r in yn) / len(yn)
    ks = [negcount.count(r['instructions'].rsplit('\n\n', 1)[-1]).k_syn for r in yn]
    tags = collections.Counter(t for u in b.units for t in u.rendered[0].row['meta']['edge'])
    base = [i for i in b.infos if i.row['role'] == 'base']
    print(json.dumps({
        'rows': len(rows), 'units': len(b.units), 'yn_share': round(len(yn) / len(rows), 3),
        'yes_rate': round(sum(r['gold'] for r in yn) / len(yn), 3), 'yes_is_bad': round(bad, 3),
        'k_syn>=1': round(sum(k >= 1 for k in ks) / len(ks), 3), 'k_syn>=2': round(sum(k >= 2 for k in ks) / len(ks), 3),
        'complement_share_of_yn': round(ov['complement_share_of_yes_no'], 3), 'nonsyn_pairs': round(ov['non_syntactic_share_of_pairs'], 3),
        'twin': round(ov['twin_share'], 3), 'equiv': round(ov['equiv_share'], 3), 'inv': round(ov['attack_share'], 3),
        'short_card': round(sum(1 for r in rows if r['meta']['defs_style'].endswith('_short')) / len(rows), 3),
        'defs_styles': dict(collections.Counter(r['meta']['defs_style'] for r in rows)),
        'tags': {k: round(v / len(b.units), 3) for k, v in sorted(tags.items())},
    }, indent=1))
    print(json.dumps(cards.token_report(rows)))
