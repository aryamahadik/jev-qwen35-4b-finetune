"""Independent re-check of the packs-2 v1.1 claims (does not import build_packs). Run from the packs-2 folder: ../../../../.venv/bin/python qc/verify_v11.py"""
import json, re, collections
P = [json.loads(l) for l in open('packs.jsonl')]
M = json.load(open('../../common/markers.json'))
mk = set()
for c in M['classes'].values():
    mk |= {str(w).lower() for w in c.get('words', []) + c.get('same_marker_forms', [])}
mk |= {'null', 'false', 'true', 'yes', 'not listed'}
STATUS_RX = re.compile(r'^(un|in|re|de)?(record\w*|list|lists|listed|listing\w*|waitlist\w*|shortlist\w*|checklist\w*|stated|missing|blanks?|blanked|pending|known|available|availability|applicable|specified|determined|unknowns?)$')
tok = lambda s: [t for t in re.split(r'[^a-z0-9]+', re.sub(r'\{\w+\}', ' ', s.lower())) if t]
def hits(s, allow=()):
    t = tok(s); raw = s.lower().strip(); out = []
    for m in mk:
        if m in allow: continue
        if not re.search(r'[a-z0-9]', m):
            if raw == m or m in raw.split(): out.append(m)
            continue
        mt = tok(m)
        if any(t[i:i+len(mt)] == mt for i in range(len(t)-len(mt)+1)): out.append(m)
    out += [x for x in t if STATUS_RX.match(x) and x not in allow]
    return out
FUNC = set('a an the of in on at to for by with from and or is are was were be been has have had its it this that as per into s'.split())
c = collections.Counter(); bad = collections.Counter()
for p in P:
    real = [a for e in p['entity_types'] for a in e['attributes']]
    lexw = set()
    for a in real:
        lx = a.get('lexicon')
        if not lx or not all(k in lx for k in ('phrases', 'key_word_forms', 'state_words')): bad['lexicon missing'] += 1; continue
        c['attrs'] += 1
        if a['type'] == 'boolean':
            c['booleans'] += 1
            if a.get('neg_statement') and re.search(r'\b(no|not)\b', a['neg_statement']): c['neg'] += 1
            else: bad['neg'] += 1
        if a['type'] == 'tag':
            c['tags'] += 1
            if a.get('none_statement') and 'none' in tok(a['none_statement']): c['none'] += 1
            else: bad['none'] += 1
        strs = [a['key'], a['label']] + a['aliases'] + a.get('values', []) + [a.get('unit', '')] + a.get('unit_synonyms', []) + lx['key_word_forms'] + lx['state_words'] + a['concept_set']['members']
        for s in lx['phrases']:
            if s == a.get('neg_statement'): bad['mk neg'] += bool(hits(s, ('no',)))
            elif s == a.get('none_statement'): bad['mk none'] += bool(hits(s, ('none',)))
            else: strs.append(s)
        for s in strs:
            if s and hits(s): bad['marker'] += 1; print('MK', p['slot'], a['key'], s, hits(s))
        for s in lx['phrases'] + lx['key_word_forms'] + lx['state_words'] + a.get('values', []) + [a['key']] + [a.get('unit', '')] + a.get('unit_synonyms', []):
            lexw |= {t for t in tok(s) if t not in FUNC}
    for e in p['entity_types']:
        for s in [e['singular'], e['plural']] + e['aliases'] + e.get('name_pool', []):
            if hits(s): bad['marker entity'] += 1
    ctx = set(p.get('inert_context_vocab', []))
    c['ctx_min'] = min(c.get('ctx_min', 10**9), len(ctx))
    ov = ctx & lexw
    if ov: bad['ctx overlap'] += len(ov)
    nlw = set(lexw)
    for d in p['document_types']: nlw |= set(tok(d)) - FUNC
    for s in p['outcome_sets']:
        for o in s['outcomes']: nlw |= set(tok(o['name'])) - FUNC
    case = p['entity_types'][0]['key']
    ent = {a['key']: e['key'] for e in p['entity_types'] for a in e['attributes']}
    cl = 0
    for w in p['label_words']:
        c['label_words'] += 1
        if hits(w['word']): bad['marker label'] += 1
        if set(tok(w['word'])) & nlw: bad['label vs lexicon'] += 1; print('LW', p['slot'], w['word'], set(tok(w['word'])) & nlw)
        elif {ent[t['attr']] for t in w['predicate']['terms']} == {case}: cl += 1
    c['packs_case12'] += cl >= 12
    rubric = set()
    for a in real:
        for m in a['concept_set']['members']: rubric |= set(tok(m)) - FUNC
    fl = p['filler_items']
    c['fillers'] += len(fl)
    if sum(f['kind'] == 'event' for f in fl) < 3 or sum(f['kind'] == 'state' for f in fl) < 3: bad['filler kinds'] += 1
    for f in fl:
        if set(tok(f['label'])) - FUNC & rubric: bad['filler overlap'] += 1; print('FO', p['slot'], f['label'])
    for a in real:
        if len(a['concept_set']['members']) < 3: bad['thin concept set'] += 1
    if set(p['disjointness_list']) != {x['key'] for x in p['inert_attributes']} | {f['key'] for f in fl}: bad['disjointness list'] += 1
print(dict(c)); print('BAD', dict(bad))
