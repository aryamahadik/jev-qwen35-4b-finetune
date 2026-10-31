import sys, json, collections, importlib, random, copy
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1])
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
ch = [i for i in b.infos if i.row['qtype'] == 'choice']
end = [i for i in ch if i.row['meta']['qform'].startswith('ch_end')]
print('ch_end rows', len(end))
r = pilot.g6_choice(end); print('G6 ch_end', r['n'], r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
# null: permute the gold within each row's options
def permuted(infos, seed):
    rnd = random.Random(seed); out=[]
    for i in infos:
        j = copy.copy(i); row = copy.deepcopy(i.row); row['gold'] = rnd.choice(row['options']); j.row = row; out.append(j)
    return out
for sd in (1,2):
    r = pilot.g6_choice(permuted(end, sd)); print('NULL', sd, r['n'], r['chance'], {v: r[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
