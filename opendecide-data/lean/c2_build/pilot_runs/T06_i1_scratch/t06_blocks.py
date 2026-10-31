import sys, json, collections, statistics
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import cards as CD
mx, tok = CD._tokenizer()
n = lambda s: len(tok.encode(s, add_special_tokens=False).ids)
rows=[json.loads(l) for l in open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/pilot/rows.jsonl')]
agg = collections.defaultdict(list)
for r in rows:
    blocks = r['state'].split('\n\n')
    for b in blocks:
        if b.startswith('Order record'): k = 'record:'+r['meta']['format_style'].split('/')[1]
        elif 'posted this notice' in b: k='notice'
        elif b.startswith('Message added'): k='attack'
        else: k='message:'+r['meta']['c2']['author_mode']
        agg[k].append(n(b))
for k,v in sorted(agg.items()): print(k, len(v), round(statistics.mean(v),1))
ins = [n(r['instructions']) for r in rows]
print('instr', statistics.mean(ins))
# wording tokens
