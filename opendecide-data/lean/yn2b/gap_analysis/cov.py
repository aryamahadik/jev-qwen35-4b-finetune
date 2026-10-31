import json,re,collections,sys
F='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl'
src=collections.Counter(); srcq=collections.Counter(); role=collections.Counter()
fam=collections.Counter(); edge=collections.Counter(); edge_yn=collections.Counter()
flags=collections.Counter(); flag_src=collections.defaultdict(collections.Counter)
flag_ex=collections.defaultdict(list)
famre=re.compile(r"'family': '([^']*)'"); edgere=re.compile(r"'edge': '([^']*)'"); edgel=re.compile(r"'edge': \[([^\]]*)\]")
teach=collections.Counter()
T={
 'norm_observance': lambda s,q,S: ('norm' in q.lower() and ('Norm' in S or 'norm' in S.lower()[:400])) or bool(re.search(r'(?m)^Norm:',S)),
 'intention_action': lambda s,q,S: bool(re.search(r'(?mi)^Intention:',S)) and bool(re.search(r'(?mi)^Action:',S)),
 'table_any': lambda s,q,S: S.count('|')>=12 or bool(re.search(r'(?mi)^(table|columns?)\b',S)),
 'hearsay': lambda s,q,S: 'hearsay' in (q+S).lower(),
 'given_definition_q': lambda s,q,S: bool(re.search(r'\b(is defined as|means an?|is an? [a-z -]+ (that|which)|applying the definition|as defined|under (the )?rule|definition provided)\b',q.lower())),
 'exception_unless': lambda s,q,S: bool(re.search(r'\b(unless|except|exempt|exemption|provided that|does not apply)\b',(q+' '+S).lower())),
 'numeric_threshold_q': lambda s,q,S: bool(re.search(r'\b(less than|more than|fewer than|greater than|at least|at most|exceed|exceeds|over|under|below|above)\b[^.?]{0,25}\d',q.lower())),
 'negframe_q': lambda s,q,S: bool(re.search(r"\b(not|n't|wrong|disagree|incorrect|false|never|no longer|mistaken|undercut|contradict)\b",q.lower())),
 'tool_any': lambda s,q,S: bool(re.search(r'\b(tool call|tool_call|function call|function_call|api call|the agent calls?|arguments?:|"arguments"|tool:|tools available|available tools)\b',(q+' '+S).lower())),
 'tool_guard_q': lambda s,q,S: bool(re.search(r'\b(should the (agent|assistant) (call|run|execute|invoke|send|proceed)|is (this|the) (tool|function|api) call (allowed|permitted|safe|valid|correct)|may the (agent|assistant)|allowed to (call|execute|run))\b',q.lower())),
 'state_tracking_q': lambda s,q,S: bool(re.search(r'\b(after (all|these|the) (events|updates|changes|messages|steps|turns)|at the end of the (log|conversation|sequence)|current (state|status|balance|value) of|final (state|status|balance|value))\b',(q+' '+S[-300:]).lower())),
 'lead_qual': lambda s,q,S: bool(re.search(r'\b(lead|prospect|ideal customer|icp|bant|sales[- ]qualified|mql|sql\b)',q.lower())),
 'response_adequacy_q': lambda s,q,S: bool(re.search(r'\b(does the (response|answer|reply|output)|is the (response|answer|reply|output)|response (satisf|meet|follow|compl)|correctly (answer|follow))\b',q.lower())),
 'evidence_sufficiency': lambda s,q,S: bool(re.search(r'\b(enough (information|evidence)|sufficient (information|evidence)|cannot be determined|insufficient)\b',(q).lower())),
 'count_q': lambda s,q,S: bool(re.search(r'\b(how many|number of|count of|exactly (one|two|three|four|five|\d+)|at least (two|three|four|five|\d+) (times|of|rows|games|items))\b',q.lower())),
 'superlative_q': lambda s,q,S: bool(re.search(r'\b(highest|lowest|most|least|largest|smallest|longest|shortest|earliest|latest|first|last|maximum|minimum|best|worst)\b',q.lower())),
 'only_q': lambda s,q,S: bool(re.search(r'\b(the only|only one|there is no|there are no|none of|no [a-z]+ (has|had|have|is|was|were))\b',q.lower())),
 'temporal_q': lambda s,q,S: bool(re.search(r'\b(before|after|between|deadline|within \d+|days?|business day|time ?zone|utc|dst|leap)\b',q.lower())),
}
def claim_text(r):
    # for table rows, statement often lives in state tail; include last 400 chars of state in q for flag detection of claims
    return r['instructions']+' '+r['state'][-400:]
n=0
for l in open(F):
    r=json.loads(l); n+=1
    s=r['source']; q=r['qtype']; src[s]+=1; srcq[(s,q)]+=1; role[r.get('role')]+=1
    m=r.get('meta') or ''
    if not isinstance(m,str): m=str(m)
    fm=famre.search(m); fam[(fm.group(1) if fm else None, q)]+=1
    e=edgere.search(m) or None
    tags=[]
    if e: tags=[e.group(1)]
    else:
        el=edgel.search(m)
        if el: tags=re.findall(r"'([^']*)'",el.group(1))
    for t in tags: edge[(t,q)]+=1
    if "'teacher'" in m: teach[q]+=1
    Q=claim_text(r); S=r['state']
    for k,f in T.items():
        try: hit=f(s,Q if k.endswith('_q') else r['instructions'],S)
        except Exception: hit=False
        if hit:
            flags[(k,q)]+=1; flag_src[k][s]+=1
            if len(flag_ex[k])<6 and hash(r['id'])%50==0: flag_ex[k].append((s,r['instructions'][:160]))
out=dict(n=n,src=[(list(k),v) for k,v in srcq.items()],role=dict(role),fam=[(list(k),v) for k,v in fam.items()],edge=[(list(k),v) for k,v in edge.items()],
 flags=[(list(k),v) for k,v in flags.items()],flag_src={k:v.most_common(25) for k,v in flag_src.items()},flag_ex=flag_ex,teach=dict(teach))
json.dump(out,open('/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/gap/cov.json','w'))
print('done',n)
