#!/usr/bin/env python3
"""Summarise solver B results (tmp/results_*.jsonl) into mismatch.json (ids, both answers, spec item; no row text)."""
import json, os, hashlib, collections, sys
here = os.path.dirname(os.path.abspath(__file__))
SPEC_ITEM = {
    'YN': 'G0 sec 1 YN (SEM-06 comparators, SEM-14 score, SEM-30 posterior, SEM-20/21 expected, SEM-31 action rule); sec 4 solver B',
    'BIN': 'G0 sec 1 BIN (SEM-11 bins, SEM-30 posterior; open world SEM-02 / sec 3)',
    'TIER': 'G0 sec 1 TIER (SEM-14, SEM-15 evaluation order, SEM-05 only-if, SEM-16 cut table)',
    'MAT': 'G0 sec 1 MAT (SEM-25 risk matrix)',
    'RANK-top': 'G0 sec 1 RANK-top (SEM-22 risk, SEM-12 ties; open world sec 3)',
    'RANK-order': 'G0 sec 1 RANK-order (SEM-22 risk, strict order, NOTA subset rule)',
    'DEC': 'G0 sec 1 DEC (SEM-21 total expected cost, SEM-33, SEM-12 ties)',
    'PRED': 'G0 sec 1 PRED (SEM-27 argmax of exact posterior; gold_probs exact)',
    'INV': 'G0 sec 1 INV rule (SEM-32 closed/open shapes)',
}
files = ['candidates_r1', 'qc_sample', 'mixdev_S5']
summary = {'solver': 'c_src/F8/solverB/solver_b.py',
           'solver_sha256': hashlib.sha256(open(os.path.join(here, 'solver_b.py'), 'rb').read()).hexdigest(),
           'spec_id': 'F8.G0.draft7', 'spec_sha256': '7570af9f0c8abca6a5cd46ab8b50656b9776c7a5bd572bd5ac6d2f0401cd1b35',
           'files': {}, 'mismatches': [], 'parse_failures': [], 'by_status': {}, 'by_form': {}}
tot = agree = 0
st = collections.Counter(); bf = collections.defaultdict(collections.Counter)
probs = 0; abst_a = abst_b = 0
for nm in files:
    p = os.path.join(here, '..', 'tmp', 'solverB', 'results_%s.jsonl' % nm)
    n = ok = 0
    for l in open(p):
        r = json.loads(l)
        n += 1
        st[r['status']] += 1
        bf[r.get('form', '?')][r['status']] += 1
        if r['status'] == 'OK':
            ok += 1
            probs += 1 if r.get('probs_checked') else 0
        elif r['status'] == 'PARSE_FAIL':
            summary['parse_failures'].append({'id': r['id'], 'file': nm + '.jsonl', 'solver_a': r['a'], 'solver_b': None,
                                              'why': r.get('why')})
        else:
            summary['mismatches'].append({'id': r['id'], 'file': nm + '.jsonl', 'kind': r['status'],
                                          'solver_a': r['a'], 'solver_b': r['b'],
                                          'spec_item': SPEC_ITEM.get(r.get('form'), 'G0 sec 4')})
        if r['status'] != 'PARSE_FAIL':
            abst_a += r['a'] in ('Cannot be determined from the information given', 'None of these')
    summary['files'][nm + '.jsonl'] = {'rows': n, 'agree': ok, 'agree_pct': round(100.0 * ok / n, 3) if n else None}
    tot += n; agree += ok
summary['rows_checked'] = tot
summary['agree'] = agree
summary['agree_pct'] = round(100.0 * agree / tot, 3) if tot else None
summary['by_status'] = dict(st)
summary['by_form'] = {k: dict(v) for k, v in bf.items()}
summary['pred_gold_probs_exact_checked'] = probs
summary['abstain_gold_rows'] = abst_a
summary['notes'] = [
    'Written from G0_SPEC.md draft 7 (sha256 matches G0_FROZEN.json) and C_DATA_SPEC 2.4/6 only; c_src/F8/gen/ (solver A, renderer) never opened.',
    'Input per row: card, instructions, state, options only (G3-style parse). The F8 sidecar is read only for solver A\'s gold_probs_exact (PRED check).',
    'Paradigms (spec 4): bayes/PRED integer population counting (lcm, cross-multiplication); expected/DEC integer ledger + pairwise tournament with SEM-12 by parsed ID number; points/tier/rules and risk matrix as SQL stages in in-memory sqlite3; rank pairwise tournament.',
    'Open world: z3 is not installed in the project venv (and no installs were made); replaced by an exact witness / counter-witness search: witness answer at one allowed point, then exact rational extremes of each multilinear comparison over the closed box (unbounded ends as limits) and full enumeration of Boolean unknowns.',
    'Comparison: label vs row gold (solver A), abstain decision (CBD/NOTA), PRED gold_probs exact vs sidecar gold_probs_exact and vs row meta.gold_probs floats.',
]
json.dump(summary, open(os.path.join(here, 'mismatch.json'), 'w'), indent=1)
print(json.dumps({k: summary[k] for k in ('rows_checked', 'agree', 'agree_pct', 'by_status')}))
print(json.dumps(summary['files']))
