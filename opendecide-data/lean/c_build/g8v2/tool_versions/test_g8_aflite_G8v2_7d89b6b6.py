"""Tests for g8_aflite.py (G8v2, PREREG_FINAL A19). CPU only, no MiniLM: synthetic features plus checks that the
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
    feats = {"yes_no": dict(rows=np.arange(n), cards=cards, X=X, y=y),
             "choice": dict(rows=np.arange(n), cards=cards, X=Xp, pair_row=pr, pair_opt=po, k=np.full(n, k),
                            gi=gi, lab=(po == gi[pr]).astype(np.int64))}
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


def test_chance_rates():
    feats, _ = synth()
    p = feats["yes_no"]["y"].mean(); assert G.chance("yes_no", feats["yes_no"]) == round(max(p, 1 - p), 4)
    assert G.chance("choice", feats["choice"]) == 0.25


def test_run_choice_reads_top_option():
    feats, cards = synth(cue=6.0); C = feats["choice"]
    trs = [tr[C["rows"]] for tr in G.partitions(cards, 3)]
    reads, right = G.run_choice(C["X"], C["pair_row"], C["lab"], trs[:16], 300, 0)
    s = G.summarize(reads, right); assert s["acc"] > 0.95 and 5 <= s["mean_reads"] <= 11


def test_verdict_rule():
    F = {"y": np.array([0, 1, 1, 1])}  # chance 0.75
    nw = [{"share": s} for s in np.linspace(0.10, 0.20, 20)]; ng = [{"share": s} for s in np.linspace(0.15, 0.30, 20)]
    v = G.verdict("yes_no", F, {"share": 0.19, "acc": 0.76}, nw, ng)
    assert v["threshold"] == min(v["q95_within"], v["q95_global"]) and v["pass"]
    assert not G.verdict("yes_no", F, {"share": 0.30, "acc": 0.70}, nw, ng)["pass"]
    assert not G.verdict("yes_no", F, {"share": 0.10, "acc": 0.78}, nw, ng)["pass"]  # acc > chance + 2 pp


def _end_to_end(cue, monkeypatch):
    monkeypatch.setattr(G, "P", 16)  # fewer partitions keep the test short; the rule is unchanged
    feats, cards = synth(n_cards=30, per=20, cue=cue, seed=3)
    G.ADAPTERS["T"] = dict(G._BASE, it_yn=300, it_ch=300)
    specs = []
    for part in feats:
        specs += [("base", part, "real", 0, 1)] + [("base", part, kind, s, 1) for kind in ("within", "global")
                                                   for s in range(G.K_NULL)]
    res = G.run_specs("T", {"base": feats}, cards, specs, jobs=1)
    out = {}
    for part, F in feats.items():
        S = lambda kind, s: G.summarize(*res[("base", part, kind, s, 1)])  # noqa: E731
        out[part] = G.verdict(part, F, S("real", 0), [S("within", s) for s in range(G.K_NULL)],
                              [S("global", s) for s in range(G.K_NULL)])
    return out


def test_end_to_end_cue_fails_and_no_cue_passes(monkeypatch):
    strong = _end_to_end(1.5, monkeypatch)
    assert not strong["yes_no"]["pass"] and not strong["choice"]["pass"]
    none = _end_to_end(0.0, monkeypatch)
    assert none["yes_no"]["pass_acc"] and none["choice"]["pass_acc"]


def test_plant_gold_side_only():
    rows, views = [], []
    rng = np.random.default_rng(0)
    for i in range(4000):
        if i % 2:
            rows.append({"qtype": "noul", "gold": int(rng.random() < 0.5), "options": None})
            views.append(([["q"], ["card"], ["w " * 5]], None))
        else:
            rows.append({"qtype": "choice", "gold": "b", "options": ["a", "b", "c"]})
            views.append(([["q"], ["card"], ["s"]], ["a", "b", "c"]))
    G.ADAPTERS["T"] = dict(G._BASE)
    pv, n = G.plant("T", rows, views, "yes_no", 0.2, 0)
    hit = [G.TOKEN in pv[i][0][2][-1] for i in range(len(rows)) if rows[i]["qtype"] == "noul"]
    gold = [rows[i]["gold"] for i in range(len(rows)) if rows[i]["qtype"] == "noul"]
    assert not any(h for h, g in zip(hit, gold) if g == 0) and n == sum(hit)
    assert abs(np.mean([h for h, g in zip(hit, gold) if g == 1]) - 0.2) < 0.04
    pc, n = G.plant("T", rows, views, "choice", 0.4, 1)
    marked = [pc[i][1] for i in range(len(rows)) if rows[i]["qtype"] == "choice" and pc[i][1] != views[i][1]]
    assert len(marked) == n and all(m == ["a", "b " + G.TOKEN, "c"] for m in marked)
    assert abs(n / 2000 - 0.4) < 0.04


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
