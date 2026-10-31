import json,re,collections
F='/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl'
R={
 'meta_framed_2nd_order': re.compile(r"(\bdisagree|second (side|note|speaker|commenter)|the other side|is (he|she|sam|jo|the (first|second) \w+|the reply|the claim|that claim) (wrong|right|correct|mistaken)|undercut|the first note|says the opposite|replies:)",re.I),
 'intention_action_story': re.compile(r"(?m)^(Intention|Action):"),
 'response_format_check': re.compile(r"\b(exactly (one|two|three|\d+) words?|valid json|json (array|object)|required format|output format|format (rule|requirement)s?|does the (response|output|reply) (follow|meet|satisf|compl))",re.I),
 'tool_call_decision': re.compile(r"\b(tool call|function call|call the (tool|function|api)|invoke|execute the (command|call)|arguments|endpoint|refund_order|send_email|delete_\w+|transfer_funds)\b",re.I),
 'state_after_events': re.compile(r"\b(after (all|these|the|those) (events|updates|operations|transactions|steps|changes|moves|actions)|final (state|status|balance|position|inventory|count)|current (state|status|balance)|at the end of (the|this) (log|sequence|day|session))",re.I),
 'lead_rubric': re.compile(r"\b(lead score|qualified lead|sales[- ]qualified|budget, authority|ideal customer profile|buying (signal|intent)|prospect)\b",re.I),
 'business_days_dst_tz': re.compile(r"\b(business days?|working days?|daylight saving|time ?zone|utc|leap year)\b",re.I),
}
c=collections.Counter(); srcs=collections.defaultdict(collections.Counter); ex=collections.defaultdict(list)
for l in open(F):
    r=json.loads(l); t=r['instructions']+'\n'+r['state']
    for k,rx in R.items():
        tt=r['instructions'] if k in ('meta_framed_2nd_order',) else t
        if rx.search(tt):
            c[(k,r['qtype'])]+=1; srcs[k][r['source']]+=1
            if len(ex[k])<4 and hash(r['id'])%97==0: ex[k].append((r['source'],r['instructions'][:140]))
for k in R:
    print('==',k,{q:c[(k,q)] for q in ('noul','choice')}, srcs[k].most_common(10))
    for e in ex[k]: print('    ',e)
