import json,re,collections
F='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl'
TS=('gd_gen_tables','gd_feverous','gd_totto_claims','gd_infotabs_nli','gd_semtabfacts_sci','gd_tatqa','gd_tathqa','gd_wtq','gd_finqa','gd_tabmcq')
ops={'count':re.compile(r"\b(how many|number of|count|(two|three|four|five|six|seven|eight|nine|ten|\d+) (times|games|matches|episodes|players|teams|races|wins|people|rows|entries|of the))\b",re.I),
'superlative':re.compile(r"\b(highest|lowest|largest|smallest|longest|shortest|earliest|latest|most|fewest|least|maximum|minimum|top|best|worst)\b",re.I),
'comparative_arith':re.compile(r"\b(more than|less than|fewer than|greater than|higher than|lower than|larger than|smaller than|longer than|shorter than|difference|sum|total|average|mean|combined|than)\b",re.I),
'only_unique':re.compile(r"\b(only|the sole|unique|exactly one)\b",re.I),
'neg_existence':re.compile(r"\b(there (is|are|was|were) no|none of|no (player|team|row|one|game)|never|not)\b",re.I),
}
c=collections.Counter(); per=collections.defaultdict(collections.Counter)
pipeless=0
for l in open(F):
    j=l.find('"source": "'); s=l[j+11:l.find('"',j+11)]
    if s not in TS: continue
    r=json.loads(l)
    if r['qtype']!='noul': continue
    claim=r['instructions']+' '+r['state'][-300:]
    hit=[k for k,rx in ops.items() if rx.search(claim)]
    c['n']+=1
    for k in hit: c[k]+=1; per[s][k]+=1
    if not hit: c['simple']+=1
    per[s]['n']+=1
print(dict(c))
for s,v in per.items(): print(s,dict(v))
