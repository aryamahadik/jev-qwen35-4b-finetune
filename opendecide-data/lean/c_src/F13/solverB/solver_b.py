#!/usr/bin/env python3
"""F13 solver B (G2): independent re-derivation of gold from the rendered row text only.

Written from the frozen G0 spec (F13.G0.v7, sha256 b4bb6319...) and the observed row format; it never reads
c_src/F13/gen/ or any solver-A code, nor the sidecar meta (only row fields: state, card, instructions, options).

Usage: solver_b.py [--pools candidates_r1,qc_sample,mixdev_S5] [--workers 2] [--limit N] [--sampler S1]
                   [--out solverB/mismatch.json]
Writes mismatch.json: {summary, mismatches: [{id, gold, b_answer, spec_item, kind}]} (no row text).
"""
import argparse
import json
import os
import re
import sys
import time
import traceback
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sb_core as C  # noqa: E402
from sb_facts import extract, TR  # noqa: E402
from sb_solve import (parse_question, SolveError, CONFLICT, NOANS, CLAIMS, parse_case, split_case_outcome,  # noqa: E402
                      solve_case_outcome, eq)
import sb_q as Q  # noqa: E402

FAM = os.path.dirname(HERE)
OUT = os.path.join(FAM, 'out')

SPEC_ITEM = {
    'qp': 'Q-P SEM-09/17/24/25/30/54 (5, 6)', 'dec': 'Q-R decision SEM-26/27/29/50/51 (3.2)',
    'holder': 'Q-R holder SEM-52', 'ag1i': 'AG-1 open action items SEM-52 (3.2)',
    'ag1x': 'AG-1 window items SEM-34 (3.2)', 'ag1h': 'AG-1 holds/conditions SEM-53 (3.2)',
    'ver_rule': 'Q-R/AG-2 version in force SEM-16/23/28/35/61', 'ver_set': 'S3 version SEM-19/29/35/49',
    'val_set': 'S3 value in force SEM-29/35/49', 'stat': 'S3 status SEM-19/27', 'logcnt': 'S3 Q-T/AG-3 count',
    'total': 'AG-3 part totals SEM-38', 'argmax': 'Q-T argmax SEM-22', 'tcount': 'Q-T count',
    'tset': 'Q-T record set SEM-44', 'tp': 'S4 Q-P criteria (4.4)', 'cmp': 'Q-T compare', 'crit': 'Q-T criterion',
}


def opt_match(ans, opt, kind):
    if ans is None:
        return False
    if isinstance(ans, frozenset):
        o = re.sub(r"\s+only$", "", opt.strip())
        ids = [x.strip() for x in re.split(r",\s*|\s+and\s+", o) if x.strip()]
        return frozenset(ids) == ans
    if isinstance(ans, (int, Fraction)) and not isinstance(ans, bool):
        p = C.parse_num(opt)
        return p is not None and p[0] == ans
    if hasattr(ans, 'get') and ans.get('kind') == 'version':
        if kind == 'val_set':
            a = C.parse_num(ans['value'])
            p = C.parse_num(opt)
            if a and p:
                return a[0] == p[0] and C.norm(a[1]) == C.norm(p[1])
            return eq(ans['value'], opt)
        return ans['vid'] == opt.strip()
    return eq(str(ans), opt)


class Ans:
    def __init__(self, values, more, kind):
        self.values = values
        self.more = more
        self.kind = kind


def truth_of(values, more, pred):
    """Set of truth values of a claim over the possible answers."""
    if more:
        return {True, False}
    out = set()
    for a in values:
        if a in (CONFLICT,) or a == '*':
            out |= {True, False}
        elif a == NOANS or a is None:
            raise SolveError('no answer for claim')
        else:
            out.add(bool(pred(a)))
    if more:
        out |= {True, False}
    return out


def _date(s):
    return C.parse_date(s)


def eval_claim(f, card, claim):
    claim = claim.strip()
    for name, rx in CLAIMS:
        m = rx.match(claim)
        if not m:
            continue
        if name == 'qp':
            ctext, neg, X = split_case_outcome(f, card, m.group(1))
            case = parse_case(f, card, ctext)
            vals, more, info = solve_case_outcome(f, card, case)
            t = truth_of(vals, more, lambda a: eq(a, X))
            return ({not x for x in t} if neg else t), 'qp'
        if name == 'dec':
            ent, unit, neg, X, Dd = m.group(2), m.group(3), bool(m.group(4)), m.group(5), _date(m.group(6))
            vals, more = (Q.s6_decision if card.vote_k else Q.s2_decision)(f, card, ent, unit, Dd)
            t = truth_of(vals, more, lambda a: eq(a, X))
            return ({not x for x in t} if neg else t), 'dec'
        if name == 'holder':
            H, neg, aid, unit, Dd = m.group(1), bool(m.group(2)), m.group(4), m.group(5), _date(m.group(6))
            vals, more = Q.s6_holder(f, aid, unit, Dd)
            t = truth_of(vals, more, lambda a: eq(a, H))
            return ({not x for x in t} if neg else t), 'holder'
        if name == 'ver':
            V, setting, neg, unit, Dd = m.group(1), m.group(2), bool(m.group(3)), m.group(4), _date(m.group(5))
            v, more = Q.s3_config(f, setting, unit, Dd)
            t = truth_of({v['vid'] if v else NOANS}, more, lambda a: a == V)
            return ({not x for x in t} if neg else t), 'ver_set'
        if name == 'stat':
            ent, unit, neg, S, Dd = m.group(2), m.group(3), bool(m.group(4)), m.group(5), _date(m.group(6))
            vals, more = Q.s3_status(f, ent, unit, Dd)
            t = truth_of(vals, more, lambda a: eq(a, S))
            return ({not x for x in t} if neg else t), 'stat'
        if name == 'argmax':
            ent, has, hl, col, tn, unit = m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)
            per = (_date(m.group(8)), _date(m.group(9)))
            vals, more = Q.s4_argmax(f, tn, unit, per, col, hi=(hl == 'highest'))
            t = truth_of(vals, more, lambda a: a == ent)
            return ({not x for x in t} if has != 'has' else t), 'argmax'
        if name == 'cmp':
            col, a, neg, rel, b, tn, unit = m.group(1), m.group(2), bool(m.group(3)), m.group(4), m.group(5), \
                m.group(6), m.group(7)
            per = (_date(m.group(8)), _date(m.group(9)))
            vals, more = Q.s4_cmp(f, tn, unit, per, col, a, b, rel)
            t = set(vals) | ({True, False} if more else set())
            return ({not x for x in t} if neg else t), 'cmp'
        if name == 'crit':  # repair r6
            ent, has, col, opw, thrs, tn, unit = m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), \
                m.group(7), m.group(8)
            per = (_date(m.group(9)), _date(m.group(10)))
            op, thr = parse_cmp(opw + ' ' + thrs)
            vals, more = Q.s4_crit(f, tn, unit, per, col, ent, op, thr)
            t = set(vals) | ({True, False} if more else set())
            return ({not x for x in t} if has != 'has' else t), 'crit'
        if name == 'tp':
            ent, neg, X = m.group(2), bool(m.group(3)), m.group(4)
            per = (_date(m.group(5)), _date(m.group(6)))
            vals, more, nrows = Q.s4_tp(f, card, ent, per)
            t = truth_of(vals, more, lambda a: eq(a, X))
            return ({not x for x in t} if neg else t), 'tp'
    raise SolveError('claim not parsed: ' + claim[:80])


CMPS = [('at least', '>='), ('no fewer than', '>='), ('no less than', '>='), ('at most', '<='), ('no more than', '<='),
        ('not exceeding', '<='), ('more than', '>'), ('over', '>'), ('above', '>'), ('less than', '<'),
        ('fewer than', '<'), ('below', '<'), ('under', '<')]


def parse_cmp(s):
    s = s.strip()
    for w, op in CMPS:
        if s.startswith(w + ' '):
            p = C.parse_num(s[len(w) + 1:])
            if p:
                return op, p[0]
    raise SolveError('cmp phrase ' + s)


def solve_choice(f, card, q):
    k = q['kind']
    m = q['m']
    if k == 'qp_case':
        case = parse_case(f, card, m.group(1))
        vals, more, info = solve_case_outcome(f, card, case)
        return Ans(vals, more, 'qp')
    if k == 'tp_choice':
        vals, more, n = Q.s4_tp(f, card, m.group(2), (_date(m.group(3)), _date(m.group(4))))
        return Ans(vals, more, 'tp')
    if k == 'dec':
        fn = Q.s6_decision if card.vote_k else Q.s2_decision
        vals, more = fn(f, card, m.group(2), m.group(3), _date(m.group(4)))
        return Ans(vals, more, 'dec')
    if k == 'holder':
        vals, more = Q.s6_holder(f, m.group(2), m.group(3), _date(m.group(4)))
        return Ans(vals, more, 'holder')
    if k == 'ag1i':
        vals, more = Q.s6_count_open(f, m.group(1), m.group(2), _date(m.group(3)))
        return Ans(vals, more, 'ag1i')
    if k == 'ag1x':
        if m.group(1) == 'exceptions':
            vals, more = Q.count_exceptions(f, card, m.group(2), _date(m.group(3)))
        else:
            vals, more = Q.count_exclusions(f, m.group(2), _date(m.group(3)))
        return Ans(vals, more, 'ag1x')
    if k == 'ag1h':
        vals, more = Q.s2_count_holds(f, m.group(1), m.group(3), m.group(4), _date(m.group(5)))
        return Ans(vals, more, 'ag1h')
    if k == 'ver_rule':
        vals, more = Q.rule_version(f, card, m.group(1), m.group(2), _date(m.group(3)))
        return Ans(vals, more, 'ver_rule')
    if k in ('ver_set', 'val_set'):
        v, more = Q.s3_config(f, m.group(1), m.group(2), _date(m.group(3)))
        if v is None:
            return Ans({NOANS}, more, k)
        if v.get('value') and C.parse_num(v['value']) is None and k == 'val_set' and \
                re.match(r"^\[(not provided|illegible)", v['value']):
            return Ans({v}, True, k)
        return Ans({v}, more, k)
    if k == 'stat':
        vals, more = Q.s3_status(f, m.group(2), m.group(3), _date(m.group(4)))
        return Ans(vals, more, 'stat')
    if k == 'logcnt':
        vals, more = Q.s3_count(f, m.group(3), m.group(4), m.group(2), _date(m.group(5)))
        return Ans(vals, more, 'logcnt')
    if k == 'total':
        vals, more = Q.s4_total(f, m.group(2), m.group(3), (_date(m.group(4)), _date(m.group(5))), m.group(1))
        return Ans(vals, more or ('*' in vals), 'total')
    if k == 'argmax_c':
        vals, more = Q.s4_argmax(f, m.group(2), m.group(3), (_date(m.group(4)), _date(m.group(5))), m.group(7),
                                 hi=(m.group(6) == 'highest'))
        return Ans(vals, more, 'argmax')
    if k in ('tcount', 'tset'):
        op, thr = parse_cmp(m.group(7))
        per = (_date(m.group(4)), _date(m.group(5)))
        if k == 'tcount':
            vals, more, rows, header = Q.s4_count(f, m.group(2), m.group(3), per, m.group(6), op, thr)
            return Ans(vals, more, 'tcount')
        vals, more = Q.s4_set(f, m.group(2), m.group(3), per, m.group(6), op, thr)
        return Ans(vals, more, 'tset')
    raise SolveError('choice kind ' + k)


def _split_unit_val(mid, tail, known):
    """'autumn send to scale-up board' -> ('autumn', 'send to scale-up board') using the known value names."""
    if tail and tail.strip():
        return mid, tail.strip()
    best = None
    for x in known:
        if mid.endswith(' ' + x) and (best is None or len(x) > len(best)):
            best = x
    if best is None:
        raise SolveError('cannot split unit/value: ' + mid[:60])
    return mid[:-len(best) - 1], best


def known_values(f, card):
    k = set(card.outcomes) | set(card.dec_outcomes)
    k |= {n.outcome for n in f.notices} | {m.outcome for m in f.motions} | {p.outcome for p in f.proposals}
    k |= {c.new for c in f.ncorr if c.new} | {c.old for c in f.ncorr if c.old}
    k |= {c.new for c in f.mcorr if c.new} | {c.old for c in f.mcorr if c.old}
    k |= {l.status for l in f.logs if l.kind == 'status'}
    return {x for x in k if x}


def yn_claim_from_q(q, known=()):
    k = q['kind']
    m = q['m']
    if k == 'yn_qp':
        return 'the outcome for ' + m.group(1)
    if k == 'yn_dec':
        unit, X = _split_unit_val(m.group(3), m.group(5), known)
        return 'the decision on %s %s for %s is %s as of %s' % (m.group(1), m.group(2), unit, X, m.group(4))
    if k == 'yn_holder':
        return '%s is the holder of %s %s for %s as of %s' % (m.group(1), m.group(2), m.group(3), m.group(4),
                                                               m.group(5))
    if k == 'yn_ver':
        return 'version %s of the %s setting is in force for %s as of %s' % (m.group(1), m.group(2), m.group(3),
                                                                              m.group(4))
    if k == 'yn_stat':
        unit, X = _split_unit_val(m.group(3), m.group(5), known)
        return 'the status of %s %s for %s is %s as of %s' % (m.group(1), m.group(2), unit, X, m.group(4))
    if k == 'yn_tp':
        return '%s %s is %s for %s through %s' % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
    if k == 'yn_cmp':
        return 'the %s of %s is %s than that of %s in table %s for %s from %s through %s' % m.groups()
    if k == 'yn_crit':
        return '%s%s has %s of %s %s in table %s for %s from %s through %s' % (
            (m.group(1) + ' ') if m.group(1) else '', m.group(2), m.group(3), m.group(4), m.group(5), m.group(6),
            m.group(7), m.group(8), m.group(9))
    if k == 'yn_arg':
        return '%s%s has the %s %s in table %s for %s from %s through %s' % (
            (m.group(1) + ' ') if m.group(1) else '', m.group(2), m.group(3), m.group(4), m.group(5), m.group(6),
            m.group(7), m.group(8))
    return None


def solve_row(row):
    text = (row.get('card') or '') + '\n' + (row.get('instructions') or '')
    card = C.parse_card(text)
    secs = C.doc_sections(row['state'])
    f = extract(secs, card)
    f.card_tie = card.tie
    q = parse_question(row['instructions'])
    world = 'closed' if card.closed else ('open' if card.open else '?')
    opts = row.get('options')
    if q['frame'] == 'q' and q['kind'].startswith('yn_'):
        q = dict(frame='yn', fneg=False, claim=yn_claim_from_q(q, known_values(f, card)))
    if q['frame'] in ('yn', 'establish', 'settle'):
        t, kind = eval_claim(f, card, q['claim'])
        if q['frame'] == 'yn':
            if len(t) != 1:
                return dict(b='UNDETERMINED-YN', kind=kind, world=world)
            ans = t.pop()
        elif q['frame'] == 'establish':
            ans = (t == {True})
        else:
            ans = (len(t) == 1)
        if q['fneg']:
            ans = not ans
        return dict(b=1 if ans else 0, kind=kind, world=world, frame=q['frame'])
    if q['frame'] == 'q' and q['kind'] == 'inv':
        return solve_inverted(f, card, q, opts, world)
    A = solve_choice(f, card, q)
    vals = set(A.values)
    undet = A.more or len(vals) != 1 or CONFLICT in vals or '*' in vals
    nei = card.nei_opt
    none = card.none_opt
    if undet:
        if world == 'open':
            return dict(b=nei, kind=A.kind, world=world)
        return dict(b='UNDETERMINED-CLOSED', kind=A.kind, world=world, vals=_short(vals))
    a = vals.pop()
    if a == NOANS:
        return dict(b='NOANSWER', kind=A.kind, world=world)
    for o in opts or []:
        if o in (nei, none):
            continue
        if opt_match(a, o, A.kind):
            return dict(b=o, kind=A.kind, world=world)
    if world == 'closed':
        return dict(b=none, kind=A.kind, world=world, val=_short({a}))
    return dict(b='DETERMINED-NOT-LISTED', kind=A.kind, world=world, val=_short({a}))


def solve_inverted(f, card, q, opts, world):
    """G0 3.1 inverted rows (SEM-56, XF14): each listed case is solved separately. A case meets rule R when the version
    of R in force for its unit on its governing date exists and the case meets that version's condition; a withheld
    'Versions of rule R' part for the unit leaves it open."""
    from sb_solve import RuleBase, eval_cond
    rid = q['m'].group(1)
    nei, none = card.nei_opt, card.none_opt
    rb = RuleBase(f, card)
    vers = rb.rules.get(rid, [])
    hits, unk = [], []
    for o in opts or []:
        if o in (nei, none):
            continue
        case = parse_case(f, card, o)
        more = any(p.arg == rid for p in Q._parts(f, ('versions',), unit=case.unit))
        if more or case.gov == TR:
            unk.append(o)
            continue
        v = rb.in_force(vers, case.unit, case.gov)
        if v is None:
            continue
        missing = set()
        try:
            m = eval_cond(v.cond, case.vals, missing)
        except SolveError:
            m = None
        if m is None or missing:
            unk.append(o)
        elif m:
            hits.append(o)
    if len(hits) == 1:
        return dict(b=hits[0], kind='inv', world=world)
    if len(hits) > 1:
        return dict(b='INV-MULTI', kind='inv', world=world)
    if world == 'open':
        return dict(b=nei if unk else 'INV-NONE-OPEN', kind='inv', world=world)
    return dict(b=none if not unk else 'UNDETERMINED-CLOSED', kind='inv', world=world)


def _short(vals):
    out = []
    for v in list(vals)[:6]:
        if isinstance(v, frozenset):
            out.append(sorted(v))
        elif isinstance(v, Fraction):
            out.append(str(v))
        elif hasattr(v, 'get'):
            out.append(v.get('vid'))
        else:
            out.append(str(v))
    return out


def run_one(line):
    r = json.loads(line)
    rid = r['id']
    gold = r['gold']
    try:
        res = solve_row(r)
    except Exception as e:  # noqa
        res = dict(b='ERROR', err=(type(e).__name__ + ': ' + str(e))[:160],
                   tb=traceback.format_exc().strip().split('\n')[-3][:160])
    b = res.get('b')
    ok = (b == gold) if not isinstance(gold, str) else (isinstance(b, str) and b == gold)
    return rid, r['meta'].get('sampler'), gold, res, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pools', default='candidates_r1,qc_sample,mixdev_S5')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--sampler', default='')
    ap.add_argument('--out', default=os.path.join(HERE, 'mismatch.json'))
    ap.add_argument('--progress', default='')
    a = ap.parse_args()
    lines = []
    for pool in a.pools.split(','):
        with open(os.path.join(OUT, pool + '.jsonl')) as fh:
            for ln in fh:
                if a.sampler and ('"sampler": "%s"' % a.sampler) not in ln:
                    continue
                lines.append((pool, ln))
                if a.limit and len(lines) >= a.limit:
                    break
    t0 = time.time()
    results = []
    if a.workers > 1:
        import multiprocessing as mp
        with mp.Pool(a.workers) as pool:
            for i, res in enumerate(pool.imap(run_one, [ln for _, ln in lines], chunksize=8)):
                results.append(res)
                if a.progress and i % 500 == 0:
                    open(a.progress, 'w').write('%d/%d %.0fs\n' % (i, len(lines), time.time() - t0))
    else:
        for i, (_, ln) in enumerate(lines):
            results.append(run_one(ln))
    mism = []
    by = {}
    for (pool, _), (rid, S, gold, res, ok) in zip(lines, results):
        key = (pool, S)
        by.setdefault(key, [0, 0])
        by[key][0] += 1
        if not ok:
            by[key][1] += 1
            mism.append(dict(id=rid, pool=pool, sampler=S, gold=gold, b_answer=res.get('b'), kind=res.get('kind'),
                             world=res.get('world'), spec_item=SPEC_ITEM.get(res.get('kind'), 'G2 parse/solve'),
                             detail={k: v for k, v in res.items() if k in ('err', 'tb', 'vals', 'val', 'frame')}))
    # reviewed classes (solverB/reviewed.json: per-class verdict after manual triage against the G0 spec)
    rev, verdicts = {}, {}
    try:
        for cname, c in json.load(open(os.path.join(HERE, 'reviewed.json'))).items():
            verdicts[cname] = c.get('verdict')
            for rid in c['ids']:
                rev[rid] = cname
    except (OSError, ValueError):
        rev, verdicts = {}, {}
    for m in mism:
        if (m.get('detail') or {}).get('frame') == 'settle':
            m['spec_item'] += '; settle frame SEM-04, F13R2-13 (inner claim truth value)'
        m['review_class'] = rev.get(m['id'], 'UNREVIEWED')
    import hashlib
    shas = {}
    for pn in a.pools.split(','):
        fp = os.path.join(OUT, pn + '.jsonl')
        if os.path.exists(fp):
            shas[pn] = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
    summ = dict(rows=len(results), mismatches=len(mism), secs=round(time.time() - t0, 1),
                by_pool_sampler={'%s/%s' % k: v for k, v in sorted(by.items())},
                by_review_class={k: sum(1 for m in mism if m['review_class'] == k)
                                 for k in sorted({m['review_class'] for m in mism})},
                review_verdicts={k: verdicts.get(k) for k in sorted({m['review_class'] for m in mism}) if k in verdicts},
                pool_sha256=shas, spec_sha256_prefix='b4bb6319b3b74318',
                not_implemented='spec 6 added checks (single-deletion set D, sufficiency, trace checks) are not run '
                                'here; this file is the gold re-derivation (G2 label agreement) only')
    json.dump(dict(summary=summ, mismatches=mism), open(a.out, 'w'), indent=1, default=str)
    print(json.dumps(summ))


if __name__ == '__main__':
    main()
