"""Tests for g8_aflite.py (G8v3, PREREG_FINAL A19 as fixed). CPU only, no MiniLM: synthetic features plus checks that the
adapters' text extraction equals each family's own qc_lib functions (read via ast from the family file, never
imported, so nothing is written inside c_src/F*/). Run: python3 -m pytest -q -p no:cacheprovider test_g8_aflite.py"""
import ast, json, re, sys
from pathlib import Path
import numpy as np
import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import g8_aflite as G  # noqa: E402

C_SRC = G.LEAN / "c_src"


def family_fn(fam, name):
    """Exec one function of c_src/<fam>/qc/qc_lib.py (source read only) and return it."""
    src = (C_SRC / fam / "qc/qc_lib.py").read_text(); tree = ast.parse(src)
    ns = {"re": re, "SENT_RX": re.compile(r"(?<=[.!?])\s+")}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("split_q", "views", name):
            exec(compile(ast.Module([node], []), fam, "exec"), ns)
    return ns[name]


SAMPLES = [
    "Rule one applies.\n\nDoes the rule apply to case A? Answer yes or no.\n\nNote: inert.",
    "Line one. Line two?\nThird line! Is it so? Yes.\n\nTail para.",
    "No question mark here.\n\nSecond para.",
    "Single line question?",
]


@pytest.mark.parametrize("fam", ["F1", "F2", "F3", "F4", "F5", "F6"])
def test_split_q_matches_family(fam):
    fn = family_fn(fam, "split_q"); ad = G.ADAPTERS[fam]
    for ins in SAMPLES:
        mine = G.split_q_para(ins) if ad["split"] == "para" else G.split_q_sent(ins, nl_rest=ad["split"] == "sent")
        assert mine == fn(ins)


@pytest.mark.parametrize("fam", ["F1", "F2", "F3", "F4", "F6"])
def test_views_match_family_on_pool(fam):
    pool = C_SRC / fam / "out/candidates_r1.jsonl"
    if not pool.exists():
        pytest.skip("pool absent")
    views = family_fn(fam, "views"); ad = G.ADAPTERS[fam]
    with open(pool) as fh:
        rows = [json.loads(next(fh)) for _ in range(300)]
    for r in rows:
        segs, opts = G.row_views(ad, r); v = views(r)
        q = G.chunks(v["q"]) if ad["chunk_q"] else [v["q"]]
        card = v["cardnoq"] if (r["qtype"] == "noul" or not ad["strip_card_choice"]) else \
            v["cardnoq"].replace(r.get("card") or "", "")
        assert segs == [q, G.chunks(card), G.chunks(v["state"])]
        if r["qtype"] != "noul":
            if ad["opt_defs"]:
                d = G.card_defs(r.get("card")); assert opts == [o + (": " + d[o] if o in d else "") for o in r["options"]]
            else:
                assert opts == r["options"]


def test_f5_views_match_g8_inline():
    pool = C_SRC / "F5/out/candidates_r1.jsonl"
    if not pool.exists():
        pytest.skip("pool absent")
    sq = family_fn("F5", "split_q")
    with open(pool) as fh:
        rows = [json.loads(next(fh)) for _ in range(300)]
    for r in rows:  # F5 g8.py: (q, card + "\n" + rest, state), every view chunked
        q, rest = sq(r["instructions"])
        exp = [G.chunks(q), G.chunks(((r.get("card") or "") + "\n" + rest).strip()), G.chunks(r["state"])]
        assert G.row_views(G.ADAPTERS["F5"], r)[0] == exp



def synth(n_cards=40, per=30, k=4, d=8, seed=0, cue=0.0):
    """Synthetic yes/no + choice feature sets in the layout features() returns. cue > 0 puts label signal in X."""
    rng = np.random.default_rng(seed); cards = np.repeat([f"c{i:03d}" for i in range(n_cards)], per)
    n = len(cards); rate = np.repeat(rng.uniform(0.2, 0.8, n_cards), per)
    y = (rng.random(n) < rate).astype(np.int64)
    X = rng.normal(size=(n, d)).astype(np.float32); X[:, 0] += cue * (2 * y - 1)
    gi = rng.integers(0, k, n); pr = np.repeat(np.arange(n), k); po = np.tile(np.arange(k), n)
    Xp = rng.normal(size=(n * k, d)).astype(np.float32); Xp[:, 0] += cue * (po == gi[pr])
    ks = np.full(n, k)
    feats = {"yes_no": dict(rows=np.arange(n), cards=cards, X=X, y=y, g_within=G._group_ids(cards),
                            g_global=np.zeros(n, np.int64)),
             "choice": dict(rows=np.arange(n), cards=cards, X=Xp, pair_row=pr, pair_opt=po, k=ks, gi=gi,
                            lab=(po == gi[pr]).astype(np.int64), g_global=G._group_ids(ks.astype(str)),
                            g_within=G._group_ids(np.char.add(np.char.add(cards, "|"), ks.astype(str))))}
    return feats, cards


def test_partitions_half_of_cards_and_seeded():
    _, cards = synth()
    a, b = G.partitions(cards, 5), G.partitions(cards, 5)
    assert len(a) == G.P and all((x == y).all() for x, y in zip(a, b))
    for tr in a[:5]:
        assert len(set(cards[tr].tolist())) == 20 and not set(cards[tr].tolist()) & set(cards[~tr].tolist())


def test_permutations_keep_card_and_k_structure():
    feats, _ = synth()
    F = feats["yes_no"]; yw = G.permute_labels("yes_no", F, "within", 1)
    for c in set(F["cards"].tolist()):
        m = F["cards"] == c; assert yw[m].sum() == F["y"][m].sum()
    assert not (yw == F["y"]).all()
    yg = G.permute_labels("yes_no", F, "global", 1); assert yg.sum() == F["y"].sum()
    C = feats["choice"]; lab = G.permute_labels("choice", C, "within", 1)
    assert lab.shape == C["lab"].shape and (np.bincount(C["pair_row"], weights=lab) == 1).all()
    assert (G.permute_labels("yes_no", F, "within", 7) == G.permute_labels("yes_no", F, "within", 7)).all()
    F2 = {k: v for k, v in F.items() if not k.startswith("g_")}  # group ids rebuilt when absent: same law
    assert (G.permute_labels("yes_no", F2, "within", 3) == G.permute_labels("yes_no", F, "within", 3)).all()


def test_within_card_permutation_is_uniform():
    F = {"y": np.array([1, 0, 0, 1, 0, 0]), "cards": np.array(["a"] * 3 + ["b"] * 3)}
    seen = {}
    for s in range(3000):
        t = tuple(G.permute_labels("yes_no", F, "within", s)); seen[t] = seen.get(t, 0) + 1
    assert len(seen) == 9 and min(seen.values()) > 3000 / 9 * 0.8  # 3 x 3 equally likely outcomes


def test_chance_rates():
    feats, _ = synth()
    p = feats["yes_no"]["y"].mean(); assert G.chance("yes_no", feats["yes_no"]) == round(max(p, 1 - p), 4)
    assert G.chance("choice", feats["choice"]) == 0.25


def test_run_choice_reads_top_option():
    feats, cards = synth(cue=6.0); C = feats["choice"]
    trs = [tr[C["rows"]] for tr in G.partitions(cards, 3)]
    reads, right = G.run_choice(C["X"], C["pair_row"], C["lab"], trs[:16], 300, 0)
    s = G.summarize(reads, right); assert s["acc"] > 0.95 and 5 <= s["mean_reads"] <= 11


def test_plant_rechunks_state_like_family():
    segs = [["q"], ["c"], G.chunks(" ".join(["w"] * 240))]
    s2, _ = G.plant_views(segs, None, G.TOKEN, "state")
    assert s2[2] == G.chunks(" ".join(["w"] * 240 + [G.TOKEN])) and len(s2[2]) == 3


def test_lr_batch_matches_sklearn():
    from sklearn.linear_model import LogisticRegression
    rng = np.random.default_rng(1); n, d = 600, 20
    X = rng.normal(size=(n, d)).astype(np.float32); w = rng.normal(size=d)
    Y = np.stack([(X @ w + rng.normal(size=n) * s > 0).astype(np.int64) for s in (0.5, 2.0, 50.0)], 1)
    tr = rng.random(n) < 0.5
    for bal in (False, True):
        SW = np.ones(Y.shape)
        if bal:
            npos = Y[tr].sum(0); SW = np.where(Y == 1, tr.sum() / (2.0 * npos), tr.sum() / (2.0 * (tr.sum() - npos)))
        W, b, _ = G.lr_batch(X, tr, Y, SW, tol=1e-8)
        for j in range(Y.shape[1]):
            m = LogisticRegression(C=1.0, max_iter=5000, tol=1e-8, class_weight="balanced" if bal else None)
            m.fit(X[tr], Y[tr, j])
            assert np.allclose(W[:, j], m.coef_[0], atol=2e-3) and abs(b[j] - m.intercept_[0]) < 2e-3


def test_batch_and_sklearn_runners_agree():
    feats, cards = synth(cue=0.5, seed=5)
    G.ADAPTERS["T"] = dict(G._BASE)
    specs = [("base", "yes_no", "real", 0, 1), ("base", "choice", "real", 0, 1)]
    old = G.P
    try:
        G.P = 6
        a = G.run_specs_batch("T", {"base": feats}, cards, specs, 1)
        b = G.run_specs_sklearn("T", {"base": feats}, cards, specs, 1)
    finally:
        G.P = old
    for k in specs:
        assert (a[k][0] == b[k][0]).all() and (a[k][1] == b[k][1]).mean() > 0.95


def test_lr_batch_row_replacement_equals_modified_data():
    rng = np.random.default_rng(2); n, d = 400, 10
    X = rng.normal(size=(n, d)).astype(np.float32); y = (X[:, 0] + rng.normal(size=n) > 0).astype(np.int64)
    idx = np.sort(rng.choice(n, 40, replace=False)); V = rng.normal(size=(40, d)).astype(np.float32) + 2.0
    X2 = X.copy(); X2[idx] = V; tr = rng.random(n) < 0.6; Y = np.stack([y, y], 1)
    Wr, br, _ = G.lr_batch(X, tr, Y, np.ones(Y.shape), tol=1e-8, rep=[None, (idx, V)])
    W0, b0, _ = G.lr_batch(X, tr, y[:, None], np.ones((n, 1)), tol=1e-8)
    W2, b2, _ = G.lr_batch(X2, tr, y[:, None], np.ones((n, 1)), tol=1e-8)
    assert np.allclose(Wr[:, 0], W0[:, 0], atol=1e-4) and np.allclose(Wr[:, 1], W2[:, 0], atol=1e-4)
    assert abs(br[1] - b2[0]) < 1e-4


def test_lr_batch_groups_equal_modified_data():
    """Planted groups: two columns share one shifted row set with different masks = fits on the modified X."""
    rng = np.random.default_rng(4); n, d = 500, 12
    X = rng.normal(size=(n, d)).astype(np.float32); y = (X[:, 0] + rng.normal(size=n) > 0).astype(np.int64)
    idx = np.sort(rng.choice(n, 80, replace=False)); D = (rng.normal(size=(80, d)) + 1.5).astype(np.float32)
    M = np.stack([rng.random(80) < 0.5, rng.random(80) < 0.9], 1).astype(np.float32)
    tr = rng.random(n) < 0.6; Y = np.stack([y, y, y], 1); grp = [(np.array([1, 2]), idx, D, M)]
    W, b, _ = G.lr_batch(X, tr, Y, None, tol=1e-8, groups=grp)
    Zg = G.lin_scores(X, ~tr, W, b, grp)
    for j, c in ((0, None), (1, 0), (2, 1)):
        Xm = X.copy()
        if c is not None:
            Xm[idx] += M[:, c:c + 1] * D
        W1, b1, _ = G.lr_batch(Xm, tr, y[:, None], np.ones((n, 1)), tol=1e-8)
        assert np.allclose(W[:, j], W1[:, 0], atol=1e-4) and abs(b[j] - b1[0]) < 1e-4
        assert np.allclose(Zg[:, j], Xm[~tr] @ W1[:, 0] + b1[0], atol=1e-3)


def test_mc_test_and_band():
    rng = np.random.default_rng(0); NS = rng.normal(size=(340, 2))
    b, K, p = G.mc_test((9.0, 9.0), NS); assert (b, K) == (0, 340) and p == 1 / 341
    assert G.decide(b, K, final=False)["verdict"] == "FAIL"
    assert G.decide(3, 340, final=False)["verdict"] == "EXTEND" and G.decide(10, 340, final=False)["verdict"] == "PASS"
    assert G.decide(8, 1000, final=True)["verdict"] == "FAIL" and G.decide(9, 1000, final=True)["verdict"] == "PASS"
    assert G.decide(8, 1000, final=True)["decided_inside_band"]
    b2, _, _ = G.mc_test((NS[:, 0].max() + 1, -99.0), NS); assert b2 == 1  # only the top-acc null ties it
    j = G.judge((9.0, 9.0), NS); assert j["verdict"] == "FAIL" and j["stage"] == 1
    NS2 = np.repeat(rng.normal(size=(1000, 1)), 2, 1); s1 = np.sort(NS2[:340, 0]); v = (s1[-3] + s1[-4]) / 2
    assert G.mc_test((v, v), NS2[:340])[0] == 3 and G.judge((v, v), NS2[:340])["verdict"] == "EXTEND"
    j2 = G.judge((v, v), NS2); assert j2["stage"] == 2 and j2["K"] == 1000 and j2["verdict"] in ("PASS", "FAIL")


def test_rule_size_under_exchangeable_null():
    """Real drawn from the null's own law: the staged rule FAILs at most ~alpha of the time."""
    rng = np.random.default_rng(1); fails, n = 0, 3000
    C = np.array([[1.0, 0.6], [0.6, 1.0]]); Lc = np.linalg.cholesky(C)
    for _ in range(n):
        A = rng.normal(size=(1001, 2)) @ Lc.T
        fails += G.judge(tuple(A[0]), A[1:])["verdict"] == "FAIL"
    assert fails / n <= G.RULE["alpha"] + 3 * np.sqrt(G.RULE["alpha"] / n)


def test_cue_views():
    segs = [["Is the cat here?"], ["card"], G.chunks("One. Two three.")]
    s2, _ = G.cue_views("yes_no", "swap", segs, None); assert s2[0] == ["Is this cat here?"] and s2[1:] == segs[1:]
    assert G.cue_views("yes_no", "swap", [["Is it?"], ["c"], ["s"]], None) is None
    s3, _ = G.cue_views("yes_no", "repeat", segs, None); assert s3[2] == G.chunks("One. Two three. Two three.")
    s4, _ = G.cue_views("yes_no", "token", segs, None); assert s4[2][-1].endswith(G.TOKEN)
    _, o = G.cue_views("choice", "token", segs, ["a b", "c d", "e"], gi=1, lab=[0, 1, 0])
    assert o == ["a b", "c d " + G.TOKEN, "e"]
    _, o = G.cue_views("choice", "shorter", segs, ["a b", "c d", "e"], gi=1, lab=[0, 1, 0]); assert o == ["a", "c d", "e"]
    assert G.cue_views("choice", "shorter", segs, ["a", "c d", "e"], gi=1, lab=[0, 1, 0]) is None
    u1 = G.plant_uniforms(50, "yes_no", "token", 2); assert (u1 == G.plant_uniforms(50, "yes_no", "token", 2)).all()
    ps = {"elig": np.arange(50) % 2 == 0}
    m1, m2 = (G.plant_marks(ps, "yes_no", "token", d, 2) for d in (0.2, 0.4))
    assert not (m1 & ~m2).any() and not m2[1::2].any()  # nested across strengths, eligible rows only


class FakeStore:
    """Deterministic unit vectors per text (no MiniLM)."""
    def vec(self, t):
        v = np.random.default_rng(list(G._key(t)[:8])).normal(size=384).astype(np.float32)
        return (v / np.linalg.norm(v)).astype(np.float16).astype(np.float32)

    def ensure(self, texts):
        return 0


def fake_pool(n=120, seed=0):
    rng = np.random.default_rng(seed); rows = []
    for i in range(n):
        st = " ".join(f"Fact {j} about item {i}." for j in range(1 + i % 3))
        r = {"instructions": f"Rules here.\n\nDoes the rule cover item {i}?", "card": f"card {i % 10}", "state": st,
             "meta": {"card_id": f"c{i % 10}"}}
        if i % 2:
            r.update(qtype="noul", gold=int(rng.random() < 0.5), options=None)
        else:
            r.update(qtype="choice", options=[f"opt {j} for {i}" for j in range(3)], gold=f"opt {i % 3} for {i}")
        rows.append(r)
    return rows


@pytest.mark.parametrize("pca", [0, 8])
def test_plant_store_shift_equals_refeaturing(pca):
    G.ADAPTERS["T"] = dict(G._BASE, pca=pca); rows = fake_pool(); views = G.pool_views("T", rows); st = FakeStore()
    feats, cards, fit = G.features("T", rows, views, st)
    for part in feats:
        F = feats[part]
        for cue in G.CUES[part]:
            ps = G.plant_store("T", views, feats, fit, st, part, cue)
            pv = list(views)
            for a, i, _, nv in G._cue_rows("T", views, F, part, cue):
                pv[i] = nv
            Zp = np.stack([[np.mean([st.vec(t) for t in seg], 0) for seg in segs] for segs, _ in pv])
            if part == "yes_no":
                exp = np.hstack([Zp[:, s] if not pca else fit["pca_row"][s].transform(Zp[:, s]) -
                                 fit["pca_row"][s].transform(fit["Z"][:, s]) + fit["B"][s] for s in range(3)])[F["rows"]]
            else:
                exp = F["X"].copy(); po = fit["pca_opt"]
                for j, i in enumerate(F["rows"]):
                    for o, (a_, b_) in enumerate(zip(pv[i][1], views[i][1])):
                        if a_ != b_:
                            dv = st.vec(a_) - st.vec(b_); dv = dv if po is None else dv @ po.components_.T
                            k = np.flatnonzero((F["pair_row"] == j) & (F["pair_opt"] == o))[0]
                            exp[k, len(dv) * 0 + sum(b.shape[1] for b in fit["B"]):][:len(dv)] += dv
                            exp[k, sum(b.shape[1] for b in fit["B"]) + len(dv):][:len(dv)] += dv * fit["B"][0][i]
            got = F["X"].copy(); got[ps["idx"]] += ps["D"]
            assert np.allclose(got, exp, atol=1e-5), (part, cue)
            assert ps["elig"].sum() == len(set(ps["unit_row"].tolist())) > 0


def test_score_planted_equals_refeatured_file(monkeypatch):
    """Integration: a planted column (strength 1.0) scores like the re-featured planted file; strength 0 = real."""
    monkeypatch.setattr(G, "P", 6)
    G.ADAPTERS["T"] = dict(G._BASE, it_yn=300, it_ch=300); rows = fake_pool(200, seed=2); st = FakeStore()
    views = G.pool_views("T", rows); feats, cards, fit = G.features("T", rows, views, st)
    pst = {part: {cue: G.plant_store("T", views, feats, fit, st, part, cue) for cue in G.CUES[part]} for part in feats}
    c0, c1 = ("real", 0, ("token", 0.0, 0)), ("real", 0, ("token", 1.0, 0))
    res = G.score("T", feats, cards, {part: {G.REAL: (0,), c0: (0,), c1: (0,)} for part in feats}, 1, pstores=pst)
    for part, F in feats.items():
        pv = list(views)
        for a, i, _, nv in G._cue_rows("T", views, F, part, "token"):
            pv[i] = nv
        fp, _, _ = G.features("T", rows, pv, st)
        rp = G.score("T", fp, cards, {part: {G.REAL: (0,)}}, 1)
        assert res[(part, "real:0", 0)] == res[(part, G.ckey(c0), 0)]
        got, exp = res[(part, G.ckey(c1), 0)], rp[(part, "real:0", 0)]
        assert abs(got["acc"] - exp["acc"]) < 0.01 and abs(got["share"] - exp["share"]) < 0.02


def test_end_to_end_v3(monkeypatch, tmp_path):
    """Staged rule on synthetic data: a strong cue FAILs; no cue gives an unremarkable p. Cache resumes runs."""
    monkeypatch.setattr(G, "P", 12); monkeypatch.setitem(G.RULE, "k_stages", (40, 100))
    monkeypatch.setitem(G.RULE, "alpha", 0.05); G.ADAPTERS["T"] = dict(G._BASE, it_yn=300, it_ch=300)
    for cue in (1.5, 0.0):
        feats, cards = synth(n_cards=30, per=20, cue=cue, seed=3); cp = tmp_path / f"c{cue}.json"
        want = {part: {G.REAL: G.SEEDS_ALL, **G.null_cols(100)} for part in feats}
        res = G.score("T", feats, cards, want, jobs=1, cache_path=cp)
        assert G.score("T", feats, cards, want, jobs=1, cache_path=cp) == res  # all from the cache
        for part in feats:
            j = G.judge(G.stat(res, part, G.REAL, G.SEEDS_ALL), G.null_stats(res, part, 100))
            assert (j["verdict"] == "FAIL") if cue else (j["p"] > 0.05), (cue, part, j)
