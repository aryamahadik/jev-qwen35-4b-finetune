#!/usr/bin/env python3
"""F9 independent solver B (G2). Written from the frozen G0 spec (c_src/F9/G0_SPEC.md v7, sha 70e75711...) and the
row format only; it never reads c_src/F9/gen/ or solver A. Paradigm: parse the served text back (card clauses,
containers, question grammar), load the parsed cells into sqlite, answer with SQL (scaled-integer exact arithmetic,
T4 IS NOT NULL masks, T5 completion loop over the parsed domains), then map the answer onto the row's options.

Usage: solver_b.py [--limit N] [--files a,b] [--debug] ; writes solverB/mismatch.json (ids, answers, spec item; no
row text)."""
import sys, os, json, re, time, argparse, collections, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sb_parse import parse_card, find_containers, ParseError
from sb_model import build
from sb_query import Ctx, compile_terms
from sb_eval import parse_question, Unsupported
from sb_run import evaluate, make_mapper, parse_domains, Undecided

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'out')
FILES = ['candidates_r1.jsonl', 'qc_sample.jsonl', 'mixdev_S5.jsonl']
WORDING_Q = {'So what does the data say?', 'Which option lines up with the data?'}
QW = (r'(?:Is|Does|What|Which|How|Among|In [^,?]{1,20}, what|At what)')


def find_question(ins):
    """The question sentence: the last question-word sentence ending in '?' outside card bullets / examples."""
    best = None
    for line in ins.split('\n'):
        s = line.strip()
        if s.startswith('- ') or s.startswith('>') or s.lower().startswith(('example', 'illustration', 'for example')):
            continue
        for m in re.finditer(r"(?<![\w'])(" + QW + r"\b[^?\n]*\?)", s):
            qq = m.group(1)
            if qq in WORDING_Q or re.match(r"A [^:]*: does it", qq):
                continue
            if '<' in qq:
                continue
            best = qq
    return best


def spec_item(Q, m, card):
    """Spec items the row exercises (for the mismatch report)."""
    items = []
    op = (Q or {}).get('op', '?')
    items.append('1.2:' + op)
    if card.world:
        items.append(card.world)
    if card.unk_mode:
        items.append(card.unk_mode)
    if card.tie_option:
        items.append('T24-option')
    elif card.tie_chain:
        items.append('T24-key')
    if card.terms:
        items.append('T7-T9')
    if card.overrides:
        items.append('T30')
    if m is not None and m.kind == 'log':
        items.append('T41' if op.startswith('l_req') else 'T32/T33')
    if m is not None and m.kind == 'join':
        items.append('T29')
    return items


def solve_row(r):
    meta = r['meta']
    ins = r['instructions']
    qs = find_question(ins)
    if qs is None:
        raise ParseError('question not found')
    if r['qtype'] == 'noul':
        card_text = r['card'] or ''
    else:
        card_text = ins.replace(qs, ' ')
    card = parse_card(card_text, short=not r['card'] and r['qtype'] == 'noul')
    tables = find_containers(r['state'], card)
    m = build(r, card, tables)
    ctx = Ctx(m, card)
    ctx.violations, ctx.notes = set(), set()
    ctx.domains, ctx.domvals = parse_domains(card, getattr(m, 'cols', {}))
    ctx.terms = compile_terms(ctx, m.cols) if card.terms else {}
    Q = parse_question(qs, m, card, ctx, r['qtype'])
    ans = evaluate(Q, m, ctx, r, make_mapper(r, m, ctx, Q))
    return ans, Q, m, card, ctx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--files', default=','.join(FILES))
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--out', default=os.path.join(HERE, 'mismatch.json'))
    a = ap.parse_args()
    t0 = time.time()
    res = dict(files={}, mismatches=[], spec_violations=[], undecided=[], n_rows=0, n_agree=0)
    dbg = collections.Counter()
    notes = collections.Counter()
    for fn in a.files.split(','):
        path = os.path.join(OUT, fn)
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        n = agree = 0
        for i, line in enumerate(open(path)):
            if a.limit and i >= a.limit:
                break
            r = json.loads(line)
            n += 1
            Q = m = card = ctx = None
            try:
                ans, Q, m, card, ctx = solve_row(r)
            except (ParseError, Undecided, Unsupported, KeyError, ValueError, IndexError, AttributeError,
                    TypeError) as e:
                reason = type(e).__name__ + ': ' + re.sub(r"'[^']*'|\"[^\"]*\"", "<v>", str(e).split(':')[0])[:60]
                res['undecided'].append(dict(id=r['id'], file=fn, sampler=r['meta']['sampler'],
                                             subtype=r['meta']['subtype'], qtype=r['qtype'], gold=r['gold'],
                                             solver_b=None, reason=reason))
                dbg[reason] += 1
                if a.debug:
                    print('UNDECIDED', r['id'], type(e).__name__, str(e)[:150])
                continue
            for nt in ctx.notes:
                notes[nt] += 1
            if ctx.violations:
                res['spec_violations'].append(dict(id=r['id'], file=fn, sampler=r['meta']['sampler'],
                                                   subtype=r['meta']['subtype'], qtype=r['qtype'],
                                                   solver_a_gold=r['gold'], solver_b=ans,
                                                   labels_agree=ans == r['gold'],
                                                   spec_items=sorted(ctx.violations)))
            if ans == r['gold']:
                agree += 1
            else:
                res['mismatches'].append(dict(id=r['id'], file=fn, sampler=r['meta']['sampler'],
                                              subtype=r['meta']['subtype'], qtype=r['qtype'],
                                              solver_a_gold=r['gold'], solver_b=ans,
                                              spec_items=spec_item(Q, m, card),
                                              edge=r['meta'].get('edge'), twin_kind=r['meta'].get('twin_kind')))
                if a.debug:
                    print('MISMATCH', r['id'], 'gold', repr(r['gold'])[:40], 'B', repr(ans)[:40], Q.get('op'))
        res['files'][fn] = dict(rows=n, agree=agree, sha256=h)
        res['n_rows'] += n
        res['n_agree'] += agree
    res['n_label_mismatch'] = len(res['mismatches'])
    res['n_spec_violation'] = len(res['spec_violations'])
    res['n_mismatch'] = res['n_label_mismatch'] + res['n_spec_violation'] + 0
    res['notes'] = dict(notes)
    res['n_undecided'] = len(res['undecided'])
    res['undecided_reasons'] = dict(dbg.most_common())
    res['seconds'] = round(time.time() - t0, 1)
    res['solver'] = ('c_src/F9/solverB/solver_b.py + sb_*.py (sqlite on the text parsed back from state, card and '
                     'question; written from G0_SPEC.md v7 and the row format only; never reads c_src/F9/gen/)')
    spec = os.path.join(os.path.dirname(HERE), 'G0_SPEC.md')
    res['g0_spec_sha256'] = hashlib.sha256(open(spec, 'rb').read()).hexdigest()
    res['n_mismatch_note'] = ('n_mismatch = label mismatches + rows that break a G0 never-generated rule (labels may '
                              'still agree; see spec_violations)')
    json.dump(res, open(a.out, 'w'), indent=1, default=str)
    print(json.dumps({k: res[k] for k in ('n_rows', 'n_agree', 'n_label_mismatch', 'n_spec_violation', 'n_undecided',
                                          'seconds', 'notes')}))
    for k, v in dbg.most_common(12):
        print(v, k)


if __name__ == '__main__':
    main()
