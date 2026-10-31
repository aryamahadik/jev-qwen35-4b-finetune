import sys, json
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode=True
import pilot, pilot_loaders as PL
base=int(sys.argv[1])
with PL.open_family('T33') as kit:
    b=pilot.build_pilot(kit, 1000, seed_base=base, run_g15=False)
    g=pilot.g6(b.infos)
    yn=g['yes_no']; ch=g['choice']
    print(base, 'verdict', g['verdict'], 'yn n', yn['n'], {v:(yn[v]['lr'],yn[v]['gbt']) for v in ('a_question','c_card_without_question','d_meta')}, 'ch n', ch['n'], 'chance', ch['chance'], {v:(ch[v]['lr'],ch[v]['gbt']) for v in ('a_question','b_options','c_card_without_question','d_meta')}, g['fails'])
