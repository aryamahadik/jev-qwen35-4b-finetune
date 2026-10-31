#!/usr/bin/env python3
"""Run solver B on every row of out/candidates_r1.jsonl, out/qc_sample.jsonl, out/mixdev_S5.jsonl.
Writes per-row results to solverB/tmp/results_<file>.jsonl and mismatches (ids, both answers, spec item; no row text)
to solverB/mismatch.json. Usage: run_all.py [file,...] [--merge]"""
import json, sys, time, re, traceback, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solver_b as B
OUT = os.path.join(HERE, '..', 'out')
FILES = ['candidates_r1.jsonl', 'qc_sample.jsonl', 'mixdev_S5.jsonl']
PROG = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build/progress_phase2.log'
QSPEC = {'Q1': 'G0 1.1 Q1 + sec 2 steps 1-8 (final outcome)', 'Q2': 'G0 1.1 Q2 (outcome + basis) + sec 2',
         'Q3': 'G0 1.1 Q3 (yes/no, open world sec 2 A10/A12)', 'Q4': 'G0 1.1 Q4 (which case qualifies)',
         'S5': 'G0 3 S5 / 11.6 (flowchart DAG)'}


def one(r):
    try:
        a = B.answer(r)
    except B.ParseError as e:
        return {'id': r['id'], 'file': None, 'status': 'PARSE_ERROR', 'err': re.sub(r"'[^']*'", "'..'", str(e))[:120],
                'gold': r['gold'], 'depth_gold': r['meta']['depth']}
    except Exception as e:
        return {'id': r['id'], 'status': 'EXCEPTION', 'err': type(e).__name__ + ': ' + traceback.format_exc().strip().split('\n')[-2][:160],
                'gold': r['gold'], 'depth_gold': r['meta']['depth']}
    ok = a['ans'] == r['gold']
    dok = a['depth'] is None or a['depth'] == r['meta']['depth']   # S5: depth not derivable from the DAG
    return {'id': r['id'], 'status': 'OK' if ok and dok else ('ANS_MISMATCH' if not ok else 'DEPTH_MISMATCH'),
            'q': a.get('q'), 'gold': r['gold'], 'solver_b': a['ans'], 'depth_gold': r['meta']['depth'],
            'depth_b': a['depth']}


def main():
    files = sys.argv[1].split(',') if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else FILES
    for f in files:
        t0 = time.time(); n = 0; c = collections.Counter()
        with open(os.path.join(HERE, 'tmp', 'results_' + f), 'w') as w:
            for l in open(os.path.join(OUT, f)):
                r = json.loads(l); n += 1
                res = one(r); res['file'] = f; res['sampler'] = r['meta']['sampler']; res['qtype'] = r['qtype']
                c[res['status']] += 1
                w.write(json.dumps(res) + '\n')
                if n % 1000 == 0:
                    print(f, n, dict(c), round(time.time() - t0, 1), flush=True)
        print('DONE', f, n, dict(c), round(time.time() - t0, 1), flush=True)
    merge()


def merge():
    mm = []; tot = collections.Counter(); per = {}
    for f in FILES:
        p = os.path.join(HERE, 'tmp', 'results_' + f)
        if not os.path.exists(p):
            continue
        c = collections.Counter()
        for l in open(p):
            x = json.loads(l); c[x['status']] += 1; tot[x['status']] += 1
            if x['status'] != 'OK':
                q = x.get('q') or ('Q3' if x['qtype'] == 'noul' else 'Q1/Q2/Q4')
                item = QSPEC['S5'] if x['sampler'] == 'S5' else QSPEC.get(q, q)
                if x['status'] == 'DEPTH_MISMATCH':
                    item = 'G0 1 depth algorithm (X,P,O,A; F1R1-A13/A14)'
                elif x['status'] in ('PARSE_ERROR', 'EXCEPTION'):
                    item = 'G0 4 parse (G3) / ' + item
                mm.append({k: x.get(k) for k in ('id', 'file', 'sampler', 'qtype', 'q', 'status', 'gold', 'solver_b',
                                                  'depth_gold', 'depth_b', 'err')} | {'spec_item': item})
        per[f] = dict(c)
    n = sum(tot.values())
    rep = {'rows_checked': n, 'agree': tot['OK'], 'agree_pct': round(100.0 * tot['OK'] / n, 3) if n else 0,
           'by_status': dict(tot), 'by_file': per, 'mismatches': mm}
    json.dump(rep, open(os.path.join(HERE, 'mismatch.json'), 'w'), indent=1)
    print('MERGED', n, dict(tot), flush=True)


if __name__ == '__main__':
    if '--merge' in sys.argv:
        merge()
    else:
        main()
