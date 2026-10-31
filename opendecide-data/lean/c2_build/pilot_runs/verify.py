import json, sys, re
from pathlib import Path
sys.path.insert(0, '.')
import pilot_loaders as PL
from c2_kit import paths
fams = ['T35','T30','T24','T33','T29','T31','T32','T23','T15','T12','T25','t37b','T36','T21','T20']
allok = True
for f in fams:
    pdir = PL.family_dir(f) / 'pilot'
    rep = json.load(open(pdir / 'PILOT_REPORT.json'))
    rows = [json.loads(l) for l in open(pdir / 'rows.jsonl')]
    rels = [json.loads(l) for l in open(pdir / 'relations.jsonl')]
    probs = []
    if len(rows) != rep['files']['n_rows']: probs.append('row count')
    ids = {r['id'] for r in rows}
    if f != 't37b':
        if any(x['a'] not in ids or x['b'] not in ids for x in rels): probs.append('dangling relation')
    else:
        bases = {json.loads(l)['id'] for l in open(pdir / 'bases.jsonl')}
        if any(x['a'] not in bases or x['b'] not in ids for x in rels): probs.append('dangling relation')
    for gate, sub in (('G5-H', 'g5h'), ('G3-H', 'g3h'), ('S13', 's13')):
        tasks = rep['chunks'].get(gate, [])
        tdir = pdir / sub / 'tasks'
        on_disk = sorted(p.name for p in tdir.glob('*.md')) if tdir.is_dir() else []
        want = sorted(Path(t['task_file']).name for t in tasks)
        if on_disk != want: probs.append(f'{gate} task files differ from report ({len(on_disk)} vs {len(want)})')
        for t in tasks:
            txt = open(t['task_file']).read()
            if t['answer_file'] not in txt: probs.append('answer path missing')
            items = json.loads(txt.split('keyed by its qid)\n\n', 1)[1])
            if len(items) != t['n_items'] or len(items) > 50: probs.append('item count')
            for it in items:
                if set(it) & {'gold', 'answer', 'label', 'id', 'meta', 'expected'}: probs.append('forbidden key')
            if any(r in txt for r in list(ids)[:0]): pass
            for rid in ids:
                if rid in txt: probs.append('row id leaked'); break
            if paths.never_open(t['task_file']) or paths.never_open(t['answer_file']): probs.append('never-open path')
            if Path(t['answer_file']).exists(): probs.append('answer file already exists')
        if tasks and not (pdir / sub / 'key.json').is_file(): probs.append(f'{gate} key missing')
    n_tasks = sum(len(v) for v in rep['chunks'].values())
    print(f, 'rows', len(rows), 'rels', len(rels), 'tasks', n_tasks, 'OK' if not probs else probs[:5])
    allok &= not probs
print('ALL OK' if allok else 'PROBLEMS')
