"""13-gram decontamination of the large_labelsets rows against every data/*.jsonl except ohs*.jsonl (never opened),
data/v14_parts/golden_{train,dev}.jsonl and the other v14 raw parts. Run with PYTHONHASHSEED=0. Writes decon_hits.json."""
import json, re, glob, os, collections, sys
LEAN='/Users/aryamahadik/Documents/jev/opendecide-data/lean'
MINE=['oiics_event','msha_injury','druglabel_section','naics_subsector','wands_product']
W=re.compile(r"\w+")
def grams(t,n=13):
    w=W.findall(t.lower())
    return {hash(' '.join(w[i:i+n])) for i in range(max(0,len(w)-n+1))}
mine={}; allg=collections.defaultdict(set)
for k in MINE:
    for l in open(f'{LEAN}/data/v14_parts/raw/{k}.jsonl'):
        r=json.loads(l); g=grams(r['state'])
        mine[(k,r['rid'])]=g
        for h in g: allg[h].add((k,r['rid']))
print('our 13-grams', len(allg))
files=[f for f in glob.glob(f'{LEAN}/data/*.jsonl') if not os.path.basename(f).startswith('ohs')]
files+=[f'{LEAN}/data/v14_parts/golden_train.jsonl', f'{LEAN}/data/v14_parts/golden_dev.jsonl']
files+=[f for f in glob.glob(f'{LEAN}/data/v14_parts/raw/*.jsonl') if os.path.basename(f)[:-6] not in MINE]
hits=collections.defaultdict(set)
for f in sorted(files):
    n=0
    for l in open(f, errors='ignore'):
        w=W.findall(l.lower())
        for i in range(max(0,len(w)-12)):
            h=hash(' '.join(w[i:i+13]))
            if h in allg:
                for x in allg[h]: hits[x].add(os.path.basename(f))
        n+=1
    print(os.path.basename(f), n, 'cum hit rows', len(hits), flush=True)
out={f'{k}|{rid}':sorted(v) for (k,rid),v in hits.items()}
json.dump(out, open(''+LEAN+'/golden_src/large_labelsets/decon_hits.json','w'), indent=0)
print(collections.Counter(k.split('|')[0] for k in out))
print(collections.Counter(f for v in out.values() for f in v).most_common(20))
