"""G6 d_meta with and without the generator-side depth / deep tags (are they the meta leak?)."""
import sys, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot as P, pilot_loaders as PL
base, n = int(sys.argv[1]), int(sys.argv[2])
with PL.open_family('T15') as kit:
    b = P.build_pilot(kit, n, seed_base=base, run_g15=False)
    infos = b.infos
    yn = [i for i in infos if i.row['qtype'] == 'noul']; ch = [i for i in infos if i.row['qtype'] == 'choice']
    print('rows', len(infos), flush=True)
    r1 = (P.g6_yes_no(yn), P.g6_choice(ch))
    print('WITH depth/deep   yn d_meta', r1[0]['d_meta'], 'chance', r1[0]['chance'], '| choice d_meta', r1[1]['d_meta'], 'chance', r1[1]['chance'], flush=True)
    orig = P.meta_features
    def nodeep(info):
        cat, num = orig(info); num = {k: v for k, v in num.items() if k not in ('depth', 'deep')}; return cat, num
    P.meta_features = nodeep
    r2 = (P.g6_yes_no(yn), P.g6_choice(ch))
    print('WITHOUT depth/deep yn d_meta', r2[0]['d_meta'], '| choice d_meta', r2[1]['d_meta'], flush=True)
    print('others (without): yn', {k: r2[0][k] for k in ('a_question', 'c_card_without_question')}, 'choice', {k: r2[1][k] for k in ('a_question', 'b_options', 'c_card_without_question')})
