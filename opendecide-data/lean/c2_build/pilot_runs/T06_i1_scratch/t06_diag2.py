"""Scratch diagnostic: build N rows in memory (real pools) and report choice-plan balance, twins, tokens, G6 by form."""
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
print('rows', len(b.infos), 'units', len(b.units), 'attempted', b.stats['units_attempted'], 'drops', b.stats['drops_by_gate'], b.stats['drop_examples'])
infos = b.infos
ch = [i for i in infos if i.row['qtype'] == 'choice']
yn = [i for i in infos if i.row['qtype'] == 'noul']
print('yes/no share', round(len(yn)/len(infos),4), 'yes rate', round(sum(i.row['gold'] for i in yn)/len(yn),4))
by = collections.defaultdict(list)
for i in ch: by[i.row['meta']['qform']].append(i)
for q,l in by.items(): print(q, len(l))
rule = by['ch_rule']
keys = collections.Counter(i.rr.option_set.gold.key for i in rule)
tot = sum(keys.values())
print('ch_rule gold keys (all roles)', {k: (v, round(v/tot,3)) for k,v in sorted(keys.items())})
for role in ('base','twin','equiv','attack','complement'):
    c = collections.Counter(i.rr.option_set.gold.key for i in rule if i.row['role']==role)
    if c: print('  role', role, sum(c.values()), dict(sorted(c.items())))
pos = collections.Counter(i.rr.option_set.gold_index for i in rule)
print('ch_rule gold position', dict(sorted(pos.items())))
sets = [i.rr.option_set for i in ch]
rep = CP.plan_report(sets)
print(json.dumps({k: rep[k] for k in ('rows','abstain_cells','positions','positions_chi2_p','length_ranks','length_ranks_chi2_p','longest_gold_pp','failing','pass')}, indent=0))
# by kind
for q,l in by.items():
    r2 = CP.plan_report([i.rr.option_set for i in l])
    print(q, 'longest_pp', r2['longest_gold_pp'], 'pos', r2['positions'], 'pos_p', r2['positions_chi2_p'], 'rank', r2['length_ranks'], r2['length_ranks_chi2_p'])
# gold rank by date order
rk = collections.defaultdict(collections.Counter)
for q in ('ch_end_reject','ch_end_withdraw'):
    for i in by.get(q, []):
        os_ = i.rr.option_set
        rk[(q,len(os_.options))][os_.meta['gold_rank']] += 1
for k,v in sorted(rk.items()): print('date rank', k, dict(sorted(v.items())))
# tokens
rows = [i.row for i in infos]
rep = CD.token_report(rows)
print(json.dumps(rep, indent=0))
print(json.dumps(CD.style_report(rows), indent=0))
# tags
tags = collections.Counter(t for i in infos if i.row['role']=='base' for t in i.row['meta']['edge'])
n = sum(1 for i in infos if i.row['role']=='base')
print('trap shares (base rows)', {k: round(v/n,3) for k,v in sorted(tags.items())})
if G6:
    r = pilot.g6_choice(ch)
    print('G6 choice', r['n'], r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
    r = pilot.g6_choice(rule); print('G6 ch_rule', r['n'], r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
    r = pilot.g6_yes_no(yn); print('G6 yes/no', {v: r[v] for v in ('a_question','c_card_without_question','d_meta')})
