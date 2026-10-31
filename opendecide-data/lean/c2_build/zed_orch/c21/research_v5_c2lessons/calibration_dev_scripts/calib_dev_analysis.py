import json, math, sys, os
from collections import defaultdict

LEAN = '/Users/aryamahadik/Documents/jev/opendecide-data/lean'

def load_jsonl(p):
    out = []
    with open(p) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out

def load_gold(dataset):
    p = f'{LEAN}/data/{dataset}.jsonl'
    return {r['id']: r for r in load_jsonl(p)}

def rows_for(dataset_dir, gold_name, model_file):
    gold = load_gold(gold_name)
    preds = load_jsonl(f'{LEAN}/{dataset_dir}/{model_file}.jsonl')
    out = []
    for pr in preds:
        g = gold.get(pr['id'])
        if g is None:
            continue
        probs = pr['probs']
        qt = g.get('qtype')
        gd = g['gold']
        if qt == 'noul':
            if isinstance(gd, str):
                gl = gd.strip().lower()
            else:
                gl = 'yes' if gd == 1 else 'no'
        else:
            if isinstance(gd, str):
                gl = gd
            else:
                opts = g.get('options')
                if not opts or not isinstance(gd, int) or gd >= len(opts):
                    continue
                gl = opts[gd]
        if gl not in probs:
            continue
        out.append({'id': pr['id'], 'qtype': qt, 'probs': probs, 'gold': gl,
                    'source': g.get('source'), 'meta': g.get('meta')})
    return out

def scale(probs, T):
    ks = list(probs.keys())
    lp = [math.log(max(probs[k], 1e-12)) / T for k in ks]
    m = max(lp)
    ex = [math.exp(x - m) for x in lp]
    s = sum(ex)
    return {k: e / s for k, e in zip(ks, ex)}

def stats(rows, T=1.0):
    n = len(rows)
    confs, corr, nll = [], [], 0.0
    for r in rows:
        p = scale(r['probs'], T) if T != 1.0 else r['probs']
        s = sum(p.values())
        top = max(p, key=p.get)
        confs.append(p[top] / s)
        corr.append(1 if top == r['gold'] else 0)
        nll += -math.log(max(p[r['gold']] / s, 1e-12))
    return confs, corr, nll / n

def ece_equal_mass(confs, corr, nb=10):
    idx = sorted(range(len(confs)), key=lambda i: confs[i])
    n = len(idx)
    tot = 0.0
    for b in range(nb):
        lo = b * n // nb
        hi = (b + 1) * n // nb
        if hi <= lo:
            continue
        sub = idx[lo:hi]
        c = sum(confs[i] for i in sub) / len(sub)
        a = sum(corr[i] for i in sub) / len(sub)
        tot += len(sub) / n * abs(c - a)
    return tot

def ece_width(confs, corr, nb=10):
    bins = defaultdict(list)
    for i, c in enumerate(confs):
        b = min(int(c * nb), nb - 1)
        bins[b].append(i)
    n = len(confs)
    tot = 0.0
    for b, sub in bins.items():
        c = sum(confs[i] for i in sub) / len(sub)
        a = sum(corr[i] for i in sub) / len(sub)
        tot += len(sub) / n * abs(c - a)
    return tot

GRID = [round(0.25 + 0.05 * i, 2) for i in range(0, 196)]  # 0.25..10.00

def best_T(rows):
    best = None
    for T in GRID:
        _, _, nll = stats(rows, T)
        if best is None or nll < best[1] - 1e-12:
            best = (T, nll)
    return best[0]

def summarize(rows, label, frozen_T=None):
    if not rows:
        return None
    confs, corr, nll = stats(rows, 1.0)
    acc = sum(corr) / len(corr)
    mc = sum(confs) / len(confs)
    e_em = ece_equal_mass(confs, corr)
    e_w = ece_width(confs, corr)
    Tb = best_T(rows)
    c2, k2, nll2 = stats(rows, Tb)
    e_em_T = ece_equal_mass(c2, k2)
    res = {'label': label, 'n': len(rows), 'acc': round(acc * 100, 2), 'mean_conf': round(mc * 100, 2),
           'gap_conf_minus_acc': round((mc - acc) * 100, 2), 'ECE_eqmass10_T1': round(e_em * 100, 2),
           'ECE_width10_T1': round(e_w * 100, 2), 'NLL_T1': round(nll, 4), 'T_opt_insample': Tb,
           'ECE_eqmass10_at_Topt': round(e_em_T * 100, 2), 'NLL_at_Topt': round(nll2, 4)}
    if frozen_T is not None:
        # frozen_T: dict qtype-> T ; apply per row
        rows_c = []
        confs3, corr3 = [], []
        for r in rows:
            T = frozen_T['noul'] if r['qtype'] == 'noul' else frozen_T['choice']
            p = scale(r['probs'], T)
            top = max(p, key=p.get)
            confs3.append(p[top])
            corr3.append(1 if top == r['gold'] else 0)
        res['ECE_eqmass10_at_frozenT'] = round(ece_equal_mass(confs3, corr3) * 100, 2)
        res['mean_conf_at_frozenT'] = round(sum(confs3) / len(confs3) * 100, 2)
    return res

if __name__ == '__main__':
    pass
