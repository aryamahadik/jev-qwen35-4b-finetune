"""Scratch: ch_rule display / gold shares per k and per key, with real pools; then G6 per view."""
import sys, json, collections, importlib
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
G6 = (len(sys.argv) > 2 and sys.argv[2] == 'g6')
import pilot
rp = importlib.import_module('families.T06.run_pilot')
from c2_kit import choiceplan as CP, cards as CD
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
infos = b.infos
print('rows', len(infos), 'units', len(b.units), 'attempted', b.stats['units_attempted'], 'drops', b.stats['drops_by_gate'], b.stats['drop_examples'])
ch = [i for i in infos if i.row['qtype'] == 'choice']; yn = [i for i in infos if i.row['qtype'] == 'noul']
print('yes/no share', round(len(yn)/len(infos),4), 'yes rate', round(sum(i.row['gold'] for i in yn)/len(yn),4))
by = collections.defaultdict(list)
for i in ch: by[i.row['meta']['qform']].append(i)
for q,l in by.items(): print(q, len(l))
rule = by['ch_rule']
bk = collections.defaultdict(collections.Counter)
for i in rule:
    os_ = i.rr.option_set
    bk[len(os_.options)][os_.gold.key]+=1
for k,c in sorted(bk.items()): print('k', k, sum(c.values()), {a:(v, round(v/sum(c.values()),3)) for a,v in sorted(c.items())})
disp = collections.Counter(tuple(sorted(o.key for o in i.rr.option_set.options)) for i in rule)
print('displays', dict(disp))
for role in ('base','twin','equiv','attack'):
    c = collections.Counter(i.rr.option_set.gold.key for i in rule if i.row['role']==role)
    print('  role', role, sum(c.values()), dict(sorted(c.items())))
rep = CP.plan_report([i.rr.option_set for i in ch])
print('plan_report cells', rep['abstain_cells'], 'pos', rep['positions'], rep['positions_chi2_p'], 'longest', rep['longest_gold_pp'])
rows = [i.row for i in infos]
r = CD.token_report(rows); print('tokens mean', r['mean'], 'max', r['max'])
tags = collections.Counter(t for i in infos if i.row['role']=='base' for t in i.row['meta']['edge'])
n = sum(1 for i in infos if i.row['role']=='base')
print('trap shares (base rows)', {k: round(v/n,3) for k,v in sorted(tags.items())})
if G6:
    for lab, l in (('all choice', ch), ('ch_rule', rule), ('ch_end', by['ch_end_reject']+by['ch_end_withdraw'])):
        r = pilot.g6_choice(l); print('G6', lab, r['n'], r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
    r = pilot.g6_yes_no(yn); print('G6 yes/no', {v: r[v] for v in ('a_question','c_card_without_question','d_meta')})
