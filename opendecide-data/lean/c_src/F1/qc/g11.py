"""G11 diversity (C_DATA_SPEC 2.1 quotas + section 8 G11) for F1 candidates_r1. Counts only, no row text."""
import json, gzip, random, statistics as st, collections as C, math, re, sys
import numpy as np
sys.path.insert(0, 'qc'); import qc_lib as q
rows, side = q.load('candidates_r1')
mix, _ = q.load('mixdev_S5')
R = {}
cards = C.defaultdict(list)
for r in rows: cards[r['meta']['card_id']].append(r)
n = len(rows); per = [len(v) for v in cards.values()]
R['rows'] = n; R['cards'] = len(cards); R['rows_per_card_max'] = max(per)
R['rows_per_card_median'] = st.median(per); R['rows_per_card_min'] = min(per)
R['packs'] = len({r['meta']['domain_pack'] for r in rows})
samp = C.Counter(r['meta']['sampler'] for r in rows)
R['samplers_train'] = dict(samp); R['sampler_max_rows'] = max(samp.values())
R['S5_in_train'] = samp.get('S5', 0); R['mixdev_samplers'] = dict(C.Counter(r['meta']['sampler'] for r in mix))
wd = C.Counter(r['meta']['wording_id'] for r in rows)
R['wording_pool'] = len(wd)
wpc = [len({r['meta']['wording_id'] for r in v}) for v in cards.values()]
R['wordings_per_card_min'] = min(wpc); R['cards_lt5_wordings'] = sum(1 for x in wpc if x < 5)
ds = C.Counter(r['meta']['defs_style'] for r in rows)
R['defs_styles'] = dict(ds); R['defs_styles_nonshort'] = len([k for k in ds if k != 'short'])
R['short_card_row_share'] = round(ds.get('short', 0) / n, 4)
R['cards_with_examples_style_share'] = round(sum(1 for v in cards.values() if any(r['meta']['defs_style'] == 'one_line_examples' for r in v)) / len(cards), 4)
def fewshot(r): return 'Worked case' in ((r.get('card') or '') + r['instructions'])
fs_cards = [c for c, v in cards.items() if any(fewshot(r) for r in v)]
R['fewshot_cards'] = len(fs_cards); R['fewshot_card_share'] = round(len(fs_cards) / len(cards), 4)
inv_cards = [c for c, v in cards.items() if any(side[r['id']]['qtype'] == 'Q4' for r in v)]
R['inverted_cards'] = len(inv_cards); R['inverted_card_share'] = round(len(inv_cards) / len(cards), 4)
R['inverted_row_share'] = round(sum(1 for r in rows if side[r['id']]['qtype'] == 'Q4') / n, 4)
ch = [r for r in rows if not q.is_yn(r)]
lf = C.Counter(side[r['id']].get('label_form') for r in ch)
R['choice_rows'] = len(ch); R['masked_share_choice'] = round(lf.get('masked', 0) / len(ch), 4)
R['swapped_share_choice'] = round(lf.get('swapped', 0) / len(ch), 4)
fs = C.Counter(r['meta']['format_style'] for r in rows)
R['format_styles'] = len(fs); R['format_style_max_share'] = round(max(fs.values()) / n, 4)
R['wording_max_share'] = round(max(wd.values()) / n, 4)
combo = C.Counter((r['meta']['format_style'], r['meta']['wording_id'], r['meta']['defs_style']) for r in rows)
R['template_combo_max_share'] = round(max(combo.values()) / n, 4)
# compression ratio over state texts (gzip)
raw = '\n'.join(r['state'] for r in rows).encode()
R['compression_ratio_state'] = round(len(raw) / len(gzip.compress(raw, 9)), 3)
# approximate Self-BLEU-4 on 300 sampled states (modified n-gram precision vs pooled others, geometric mean)
rng = random.Random(11); smp = rng.sample(rows, 300)
tok = [re.findall(r"\w+|[^\w\s]", r['state'].lower()) for r in smp]
def ng(t, k): return C.Counter(tuple(t[i:i + k]) for i in range(len(t) - k + 1))
NG = [[ng(t, k) for k in range(1, 5)] for t in tok]
top = [dict() for _ in range(4)]  # ngram -> [max, holder, second]
for i, g in enumerate(NG):
    for k in range(4):
        for x, c in g[k].items():
            t = top[k].get(x)
            if t is None: top[k][x] = [c, i, 0]
            elif c > t[0]: top[k][x] = [c, i, t[0]]
            elif c > t[2]: t[2] = c
sb = []
for i, g in enumerate(NG):
    ps = []
    for k in range(4):
        tot = sum(g[k].values()) or 1; m = 0
        for x, c in g[k].items():
            t = top[k][x]; o = t[2] if t[1] == i else t[0]
            m += min(c, o)
        ps.append(max(m / tot, 1e-9))
    sb.append(math.exp(sum(math.log(p) for p in ps) / 4))
R['self_bleu4_approx'] = round(sum(sb) / len(sb), 4)
# Vendi score on MiniLM state embeddings (G8 cache), 2000 rows, cosine kernel
z = np.load(q.TMP / 'g8_emb_candidates_r1.npz')
E = z['rowemb'][:, 2, :]; idx = np.random.RandomState(7).choice(len(E), 2000, replace=False)
X = E[idx].astype(np.float64); X = X / np.linalg.norm(X, axis=1, keepdims=True)
w = np.clip(np.linalg.eigvalsh(X @ X.T / len(X)), 0, None); w = w[w > 1e-12]
R['vendi_state_minilm_2000'] = round(float(np.exp(-(w * np.log(w)).sum())), 2)
R['golden_train_comparison'] = 'not computable: golden_train slice not in the checker allow-list; raw values reported'
R['claude_seed_rougeL'] = 'n/a: F1 rows are program-rendered; no Claude-written seed rows in this family'
chk = {
 'cards_ge_80': R['cards'] >= 80, 'rows_per_card_max_le_128': R['rows_per_card_max'] <= 128,
 'packs_ge_30': R['packs'] >= 30, 'train_samplers_ge_4': len(samp) >= 4 and R['S5_in_train'] == 0,
 'sampler_rows_le_2500': R['sampler_max_rows'] <= 2500, 'wording_pool_ge_30': R['wording_pool'] >= 30,
 'wordings_per_card_ge_5': R['wordings_per_card_min'] >= 5, 'defs_styles_ge_3': R['defs_styles_nonshort'] >= 3,
 'fewshot_cards_5_10pct': 0.05 <= R['fewshot_card_share'] <= 0.10,
 'inverted_cards_10_15pct': 0.10 <= R['inverted_card_share'] <= 0.15,
 'masked_choice_10_15pct': 0.10 <= R['masked_share_choice'] <= 0.15,
 'swapped_choice_about_5pct': 0.03 <= R['swapped_share_choice'] <= 0.07,
 'surface_template_le_2pct': R['format_style_max_share'] <= 0.02,
}
R['checks'] = chk; R['soft'] = {'rows_per_card_median_about_40_50': R['rows_per_card_median'],
 'short_card_rows_about_15pct': R['short_card_row_share'], 'examples_style_about_50pct_cards': R['cards_with_examples_style_share']}
R['failed'] = [k for k, v in chk.items() if not v]; R['pass'] = not R['failed']; R['gate'] = 'G11'
json.dump(R, open('qc/g11_candidates_r1.json', 'w'), indent=1)
print(json.dumps({k: R[k] for k in ('cards', 'rows_per_card_max', 'rows_per_card_median', 'packs', 'samplers_train', 'wording_pool', 'wordings_per_card_min', 'fewshot_card_share', 'inverted_card_share', 'masked_share_choice', 'swapped_share_choice', 'format_style_max_share', 'compression_ratio_state', 'self_bleu4_approx', 'vendi_state_minilm_2000', 'failed', 'pass')}))
