"""Scratch diagnostic (not part of the family): build the pilot in memory and report the choice G6 per question form."""
import sys, json, collections, importlib, copy, random
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2); sys.path.insert(0, C2 + '/families/T06')
import pilot
sys.argv = ['x']
rp = importlib.import_module('families.T06.run_pilot')
import pilot_loaders as PL
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
with rp._t06() as kit:
    b = pilot.build_pilot(kit, 1000, run_g15=False)
infos = b.infos
print('rows', len(infos))
ch = [i for i in infos if i.row['qtype'] == 'choice']
by = collections.defaultdict(list)
for i in ch: by[i.row['meta']['qform']].append(i)
for q, l in by.items(): print(q, len(l))
# gold key distribution of ch_rule
if 'ch_rule' in by:
    keys = collections.Counter()
    for i in by['ch_rule']:
        os_ = i.rr.option_set
        keys[os_.gold.key] += 1
    print('ch_rule gold keys', dict(keys), {k: round(v/sum(keys.values()),3) for k,v in keys.items()})
    pos = collections.Counter(i.rr.option_set.gold_index for i in by['ch_rule'])
    print('ch_rule positions', dict(sorted(pos.items())))
def g6c(lst, label):
    r = pilot.g6_choice(lst)
    print(label, 'n', r['n'], 'chance', r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
g6c(ch, 'all choice')
for q, l in by.items():
    g6c(l, q)
