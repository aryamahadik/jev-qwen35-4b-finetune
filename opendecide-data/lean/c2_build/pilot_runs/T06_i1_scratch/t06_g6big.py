import sys, json, collections, importlib, random, copy
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1]); base = int(sys.argv[2]) if len(sys.argv) > 2 else pilot.SEED_BASE
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, seed_base=base, run_g15=False)
infos = b.infos
ch = [i for i in infos if i.row['qtype']=='choice']; yn=[i for i in infos if i.row['qtype']=='noul']
rule=[i for i in ch if i.row['meta']['qform']=='ch_rule']; end=[i for i in ch if i.row['meta']['qform']!='ch_rule']
for lab,l in (('ALL choice',ch),('ch_rule',rule),('ch_end',end)):
    r = pilot.g6_choice(l); print('G6', lab, r['n'], r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')}, flush=True)
r = pilot.g6_yes_no(yn); print('G6 yes/no', r['n'], {v: r[v] for v in ('a_question','c_card_without_question','d_meta')}, flush=True)
