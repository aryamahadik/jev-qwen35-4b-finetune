"""G11 diversity (independent F6 checker). C_DATA_SPEC v4 2.1 quotas / 8 G11 + F6 G0 8 (G11) and 7 (samplers):
- counts: cards >= 80 (r1), one pack per card, training samplers S1-S4 only (S5 never), rows per sampler <= 2,500
  over both rounds (r1 pool), rows per card max 128 (target after selection; pool reported);
- instruction wordings: approved pool >= 30 (formats-2 F6 pool after F6's lint), each card uses >= 5;
- definition styles >= 3 (one-line, one-line + 1-2 examples on ~50% of cards, decision list), short card ~15% of rows,
  few-shot cards 5-10%, inverted (C-CASE) cards 10-15%, masked 10-15% / swapped ~5% of choice rows, yes/no 45-55%;
- surface template = defs_style x format_style x wording_id x frame_id x sampler (F6 G0 8); max share <= 2%;
- Claude seeds, pairwise word-level ROUGE-L F1 < 0.7 (own LCS; lowercased; slots one token): F6 wordings used,
  question frames (G0 3.1 closed list; designed polarity minimal pairs reported apart), attack lines, option texts;
- corpus metrics (gzip ratio, Self-BLEU-4 on a 200-row sample, Vendi on the G8 MiniLM cache). The golden_train
  comparison is outside this checker's allow-list: pending (orchestrator). Usage: g11.py [name]"""
import gzip, json, math, random, re, statistics, sys
from collections import Counter, defaultdict
import numpy as np
import qc_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows, side = q.load(NAME)
W = re.compile(r"\{[a-z]+\}|<[a-z]+>|[a-z0-9]+")
toks = lambda s: W.findall(s.lower())
P = {}
VIEW = 2  # G8 cache view index: 0 question, 1 card without question, 2 record state


def lcs(a, b):
    if not a or not b: return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge_l(a, b):
    ta, tb = toks(a), toks(b); l = lcs(ta, tb)
    if l == 0: return 0.0
    p, r = l / len(tb), l / len(ta); return 2 * p * r / (p + r)


def seeds_check(items, exempt=None):
    best = (0.0, None); hits = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            s = rouge_l(items[i][1], items[j][1])
            if s > best[0]: best = (s, [items[i][0], items[j][0]])
            if s >= 0.7: hits.append([items[i][0], items[j][0], round(s, 3)])
    ex = [h for h in hits if exempt and exempt(h)]
    return {"n": len(items), "max": round(best[0], 3), "pair": best[1], "pairs_ge_0.7": len(hits),
            "exempt_pairs": ex, "non_exempt_pairs": [h for h in hits if h not in ex]}


C = lambda f: Counter(f(r) for r in rows)
cards = C(lambda r: r["meta"]["card_id"]); packs = C(lambda r: r["meta"]["domain_pack"])
card_pack = defaultdict(set); card_wd = defaultdict(set); card_ds = defaultdict(set); card_form = defaultdict(set)
for r in rows:
    m = r["meta"]; card_pack[m["card_id"]].add(m["domain_pack"]); card_wd[m["card_id"]].add(m["wording_id"])
    card_ds[m["card_id"]].add(m["defs_style"]); card_form[m["card_id"]].add(side[r["id"]]["form"])
samp = C(lambda r: r["meta"]["sampler"])
counts = {"rows": len(rows), "cards": len(cards), "packs": len(packs),
          "packs_per_card_max": max(len(v) for v in card_pack.values()),
          "cards_per_pack_max": max(Counter(p for v in card_pack.values() for p in v).values()),
          "samplers": dict(samp), "rows_per_card_max": max(cards.values()), "rows_per_card_median": statistics.median(cards.values()),
          "rows_per_card_max_after_r1_selection_est": round(max(cards.values()) * 3600 / len(rows), 1)}
P["cards_ge_80"] = len(cards) >= 80
P["one_pack_per_card"] = counts["packs_per_card_max"] == 1
P["samplers_S1_S4_only"] = set(samp) <= {"S1", "S2", "S3", "S4"}
P["rows_per_sampler_pool_le_2500"] = all(v <= 2500 for v in samp.values())
# wordings: approved pool (formats-2 F6 pool after F6's own lint) and per-card use
sys.path.insert(0, str(q.LEAN / "c_src"))
fp = [json.loads(l) for l in open(q.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl") if l.strip()]
f6w = {w["id"]: w for w in fp if w.get("family") == "F6"}
try:
    from F6.gen import styles_f6
    approved = {w["id"] for w in styles_f6.wording_pool()}
except Exception as e:  # report, never guess
    approved = None; counts["approved_pool_error"] = repr(e)[:200]
used = C(lambda r: r["meta"]["wording_id"])
counts.update({"wordings_in_f6_pool": len(f6w), "wordings_approved": len(approved) if approved is not None else None,
               "wordings_used": len(used), "wordings_used_not_in_approved": sorted(set(used) - (approved or set())),
               "wordings_per_card_min": min(len(v) for v in card_wd.values()),
               "cards_with_lt5_wordings": sum(1 for v in card_wd.values() if len(v) < 5)})
P["wording_pool_ge_30"] = (approved is not None and len(approved) >= 30)
P["wordings_used_ge_30"] = len(used) >= 30
P["each_card_ge_5_wordings"] = counts["cards_with_lt5_wordings"] == 0
# definition styles, short card, few-shot, inverted, label forms, yes/no share
ds_cards = Counter(next(iter(v)) if len(v) == 1 else "mixed" for v in card_ds.values())
EXRX = re.compile(r"(?im)\bexamples?\b|\bworked example\b|\bfor instance\b")
ex_cards = {r["meta"]["card_id"] for r in rows if EXRX.search((r.get("card") or "") + "\n" + r["instructions"])}
inv_cards = {c for c, f in card_form.items() if "c_case" in f}
ch = [r for r in rows if not q.is_yn(r)]
lf = Counter(side[r["id"]]["label_form"] for r in ch)
short_rows = sum(1 for r in rows if r["meta"]["defs_style"] == "short")
counts.update({"defs_style_cards": dict(ds_cards), "cards_with_examples": len(ex_cards), "inverted_cards": len(inv_cards),
               "short_card_row_share": round(short_rows / len(rows), 4), "masked_share_choice": round(lf["masked"] / len(ch), 4),
               "swapped_share_choice": round(lf["swapped"] / len(ch), 4), "yes_no_share": round(1 - len(ch) / len(rows), 4)})
P["defs_styles_ge_3_incl_examples"] = len([k for k in ds_cards if k != "mixed"]) >= 3 and len(ex_cards) >= 1
P["examples_on_about_50pct_cards"] = 0.40 <= len(ex_cards) / len(cards) <= 0.60
FS_RX = re.compile(r"(?m)Worked example:")  # recheck fix: few-shot blocks (gen/examples_f6.py) were never measured
fs_cards = {r["meta"]["card_id"] for r in rows if FS_RX.search((r.get("card") or "") + "\n" + r["instructions"])}
counts["few_shot_cards"] = len(fs_cards); counts["few_shot_card_share"] = round(len(fs_cards) / len(cards), 4)
P["few_shot_cards_5_10pct"] = 0.05 <= len(fs_cards) / len(cards) <= 0.10
P["short_card_about_15pct_rows"] = 0.10 <= short_rows / len(rows) <= 0.20
P["inverted_cards_10_15pct"] = 0.10 <= len(inv_cards) / len(cards) <= 0.15
P["masked_10_15pct"] = 0.10 <= lf["masked"] / len(ch) <= 0.15
P["swapped_about_5pct"] = 0.03 <= lf["swapped"] / len(ch) <= 0.07
P["yes_no_45_55pct"] = 0.45 <= 1 - len(ch) / len(rows) <= 0.55
# surface template share
st = C(lambda r: (r["meta"]["defs_style"], r["meta"]["format_style"], r["meta"]["wording_id"], side[r["id"]]["frame_id"], r["meta"]["sampler"]))
top = st.most_common(1)[0]
surface = {"n_templates": len(st), "max_share": round(top[1] / len(rows), 4), "max_count": top[1],
           "wording_max_share": round(max(used.values()) / len(rows), 4),
           "style_max_share": round(max(C(lambda r: r["meta"]["format_style"]).values()) / len(rows), 4),
           "frame_max_share": round(max(C(lambda r: side[r["id"]]["frame_id"]).values()) / len(rows), 4)}
P["surface_template_le_2pct"] = top[1] / len(rows) <= 0.02
# Claude seeds ROUGE-L
from F6.gen import lex
POLAR = {("can", "cannot"), ("highest", "lowest"), ("determined", "leave"), ("establish", "show")}
def polar(h):
    a, b = lex.FRAMES.get(h[0], ""), lex.FRAMES.get(h[1], "")
    da = set(toks(a)) ^ set(toks(b))
    return len(da) <= 2 and any(set(p) <= da or (p[0] in da) for p in POLAR) and abs(len(toks(a)) - len(toks(b))) <= 1
seeds = {"wordings": seeds_check(sorted((i, f6w[i]["text"]) for i in used if i in f6w)),
         "question_frames": seeds_check(sorted(lex.FRAMES.items()), exempt=polar),
         "attack_lines": seeds_check([(str(i), t) for i, t in enumerate(lex.ATTACK_LINES)]),
         "option_texts": seeds_check([(k + str(i), t) for k, ts in lex.OPTION_TEXT.items() for i, t in enumerate(ts)])}
seeds["question_frames"]["note"] = "G0 3.1 closed frame list (frozen in G0): every pair >= 0.7 is a designed minimal pair (can/cannot, highest/lowest, filtered/unfiltered, whether/that); reported, not counted"
P["seeds_rouge_l_lt_0.7"] = all(not v["non_exempt_pairs"] for k, v in seeds.items() if k != "question_frames")
# corpus metrics
rng = random.Random(11)
states = [r["state"] for r in rows]
raw = "\n".join(states).encode(); gz = len(gzip.compress(raw)) / len(raw)
smp = rng.sample(rows, 200)
def ngr(t, n): return Counter(tuple(t[i:i + n]) for i in range(len(t) - n + 1))
def bleu4(h, refs):
    ps = []
    for n in range(1, 5):
        hc = ngr(h, n); mx = Counter()
        for rf in refs:
            for g, c in ngr(rf, n).items(): mx[g] = max(mx[g], c)
        num = sum(min(c, mx[g]) for g, c in hc.items()); den = max(1, sum(hc.values())); ps.append((num + 1) / (den + 1))
    rl = min((abs(len(rf) - len(h)), len(rf)) for rf in refs)[1]
    bp = 1.0 if len(h) > rl else math.exp(1 - rl / max(1, len(h)))
    return bp * math.exp(sum(math.log(p) for p in ps) / 4)
tk = [toks(r["state"])[:300] for r in smp]
sb = float(np.mean([bleu4(tk[i], tk[:i] + tk[i + 1:i + 41]) for i in range(len(tk))]))
vendi = None
try:
    import hashlib; _sha = hashlib.sha256((q.OUT / "candidates_r1.jsonl").read_bytes()).hexdigest()  # recheck fix: pool-sha keyed cache
    z = np.load(q.TMP / f"g8_emb_candidates_r1_{_sha[:16]}.npz"); E = z["rowemb"].astype(np.float64); E = E[:, VIEW] if E.ndim == 3 else E
    idx = np.random.default_rng(11).choice(len(E), size=min(2000, len(E)), replace=False); X = E[idx]
    X = X / np.linalg.norm(X, axis=1, keepdims=True); K = X @ X.T / len(X); ev = np.linalg.eigvalsh(K); ev = ev[ev > 1e-12]
    vendi = float(np.exp(-(ev * np.log(ev)).sum()))
except Exception as e:
    vendi = "error " + repr(e)[:100]
metrics = {"gzip_ratio_states": round(gz, 4), "self_bleu4_200": round(sb, 4), "vendi_minilm_2000": vendi,
           "golden_train_comparison": "pending (orchestrator; golden_train outside this checker's allow-list)"}
res = {"gate": "G11", "file": f"out/{NAME}.jsonl", "counts": counts, "surface_template": surface, "claude_seeds_rouge_l": seeds,
       "corpus_metrics": metrics, "pass_parts": P, "fail_parts": [k for k, v in P.items() if not v]}
res["pass"] = all(P.values())
json.dump(res, open(q.QC / f"g11_{NAME}.json", "w"), indent=1)
print("fail_parts", res["fail_parts"]); print(json.dumps(counts)[:900]); print(json.dumps(surface)); print(json.dumps(metrics))
print({k: (v["max"], v["pairs_ge_0.7"], len(v["non_exempt_pairs"])) for k, v in seeds.items()})
