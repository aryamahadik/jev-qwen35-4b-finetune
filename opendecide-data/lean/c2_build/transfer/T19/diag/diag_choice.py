import sys,json,collections as C
sys.dont_write_bytecode=True
sys.path.insert(0,'.')
import pilot, pilot_loaders as PL
n=int(sys.argv[1]) if len(sys.argv)>1 else 6000
with PL.open_family('T19') as kit:
    b=pilot.build_pilot(kit,n,run_g15=False)
ch=[i for i in b.infos if i.row['qtype']=='choice']
for qf in ('ch_verdict','ch_gap'):
    sub=[i for i in ch if i.row['meta']['qform']==qf]
    g=pilot.g6_choice(sub)
    print(qf,len(sub),{k:(v if not isinstance(v,dict) else v) for k,v in g.items() if k in('n','chance','a_question','b_options','c_card_without_question','d_meta')},flush=True)
    if qf=='ch_gap':
        print(C.Counter((len(i.row['options']),i.row['options'].index(i.row['gold'])) for i in sub))
