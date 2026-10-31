"""Tests for the LongBench v2 kit, on SYNTHETIC items only (CPU, no GPU, no weights, no real item is read).

  cd /Users/aryamahadik/Documents/jev && opendecide-data/.venv/bin/python -m pytest -q bench/longbench_v2/tests

1. parity: every protocol piece in lb_lib equals longjev's own code (the quarantined checkout at 9d317786)
2. the index-keyed readout equals prep89/ohs3_lib.a5_read (= decoder_io.predict) on a tiny random model
3. the index-keyed cascade rule equals ohs3_lib's
4. end to end: synthetic data -> convert -> run_lb (fake model, twice) -> score_lb -> cascade_lb -> score_lb
5. guards: run_lb never opens the gold file; real items refuse --limit / --fake-model / a second run
"""
from __future__ import annotations

import builtins
import importlib.util
import io
import json
import random
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

KIT = Path(__file__).resolve().parents[1]
REPO = KIT.parents[1]
LEAN = REPO / "opendecide-data" / "lean"
LONGJEV = REPO / "bench" / "external_quarantine" / "longbench_v2" / "longjev_repo"
ADAPTER = REPO / "backups" / "modal_models" / "q35_4b_main500k"  # tokenizer + train_meta only (no weights are loaded)
sys.path.insert(0, str(KIT))
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "prep89"))
import lb_lib as lb  # noqa: E402
import lb_select as sel  # noqa: E402

need_longjev = pytest.mark.skipif(not (LONGJEV / "src/longjev/chunker.py").exists(), reason="longjev checkout missing")
need_adapter = pytest.mark.skipif(not (ADAPTER / "tokenizer.json").exists(), reason="adapter tokenizer missing")


def words(rng, n):
    W = "alpha beta gamma delta river stone ledger audit clause tenant budget invoice harbor".split()
    return " ".join(rng.choice(W) for _ in range(n))


def synth_text(rng, n_chars):
    parts, size = [], 0
    while size < n_chars:
        p = ". ".join(words(rng, rng.randint(3, 15)) for _ in range(rng.randint(1, 30)))
        if rng.random() < 0.3:
            p = p.replace(". ", "\n", 3)
        if rng.random() < 0.05:
            p = "x" * rng.randint(3000, 7000)  # an oversized piece without separators (hard split)
        parts.append(p)
        size += len(p) + 2
    return "\n\n".join(parts)[:n_chars]


def synth_item(rng, i, n_chars):
    return {"_id": f"syn{i:04d}", "question": "  Q " + words(rng, 12) + " ", "context": synth_text(rng, n_chars),
            **{f"choice_{L}": " " + words(rng, rng.randint(0, 6)) for L in "ABCD"}, "answer": "A",
            "domain": "d", "sub_domain": "s", "difficulty": "easy", "length": "short"}


# ------------------------------------------------------------------------------------------------ 1. parity with longjev

@pytest.fixture(scope="module")
def lj():
    sys.path.insert(0, str(LONGJEV / "src"))
    import longjev.api as api
    import longjev.assembler as asm
    import longjev.chunker as ch
    import longjev.questions as qs
    import longjev.selectors as sels
    import longjev.tokens as tk
    spec = importlib.util.spec_from_file_location("longjev_eval_longbench", LONGJEV / "eval/longbench.py")
    elb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(elb)
    spec = importlib.util.spec_from_file_location("longjev_eval_report", LONGJEV / "eval/report.py")
    rep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rep)
    return SimpleNamespace(api=api, asm=asm, ch=ch, qs=qs, sels=sels, tk=tk, elb=elb, rep=rep)


@need_longjev
def test_constants_match_longjev(lj):
    assert lj.ch.SEPARATORS == lb.SEPARATORS
    assert lj.asm.GAP_TOKENS == lb.GAP_TOKENS
    assert lj.api.SINGLE_LIMIT_TOKENS == lb.SINGLE_LIMIT_TOKENS and lj.api.MARGIN == lb.MARGIN
    assert lj.elb.DEV_SIZE == lb.DEV_SIZE and tuple(lj.elb.LETTERS) == lb.LETTERS
    src = (LONGJEV / "eval/run.py").read_text()
    assert "CHARS_PER_TOKEN = 3.0" in src and "BUDGETS = (8_000, 16_000, 28_000)" in src
    assert 'fits = record["context_tokens"] + 600 <= lj.max_budget_tokens' in src
    import inspect
    sig = inspect.signature(lj.api.LongJev.__init__)
    assert sig.parameters["chunk_tokens"].default == lb.CHUNK_TOKENS
    assert sig.parameters["max_budget_tokens"].default == lb.MAX_BUDGET


@need_longjev
def test_chunker_parity(lj):
    rng = random.Random(1)
    est = lj.tk.TokenEstimator(3.0)
    for i in range(40):
        text = synth_text(rng, rng.randint(1, 60_000))
        theirs = lj.ch.chunk_state(text, 800, est)
        ours = lb.chunk_state(text)
        assert [(c.id, c.label, c.start, c.end, c.text, c.est_tokens) for c in theirs] == \
               [(c.id, c.label, c.start, c.end, c.text, c.est_tokens) for c in ours]
        assert "".join(c.text for c in ours) == text


@need_longjev
def test_questions_split_budget_parity(lj, tmp_path):
    rng = random.Random(2)
    items = [synth_item(rng, i, 100) for i in range(150)]
    items[3]["choice_B"] = ""  # empty option renders as its letter alone
    items[4]["question"] = "Q " + words(rng, 15000)  # a long question lowers the effective budget
    p = tmp_path / "d.json"
    p.write_text(json.dumps(items))
    loaded = lj.elb.load(p)
    assert {x["_id"] for x in loaded if x["split"] == "dev"} == lb.dev_ids(items)
    fake_self = SimpleNamespace(estimator=lj.tk.TokenEstimator(3.0))
    for it in items:
        q = lj.elb.question(it)
        assert q["q"].to_json() == lb.choice_json(it)
        assert lj.qs.render(q["q"]) == lb.render(lb.choice_json(it))
        cq = lj.qs.chunk_questions(q)
        assert cq["rel__q"]["instructions"] == lb.rel_instruction(it)
        assert cq["suff__q"]["instructions"] == lb.SUFF_CHUNK_TEMPLATE.format(lb.render(lb.choice_json(it)))
        assert lj.qs.final_questions(q) == lb.final_questions(it)
        for b in (8000, 16000, 28000):
            assert lj.api.LongJev.effective_budget(fake_self, q, b) == lb.effective_budget(it, b)
    assert lb.effective_budget(items[4]) < 8000


@need_longjev
def test_select_render_recalibrate_parity(lj):
    rng = random.Random(3)
    for trial in range(60):
        text = synth_text(rng, rng.randint(20_000, 200_000))
        chunks = lb.chunk_state(text)
        ntok = [max(1, int(len(c.text) / rng.uniform(2.5, 4.5))) for c in chunks]
        theirs_r = lj.api.LongJev.recalibrate(chunks, lj.sels.ChunkScores(
            rel={"q": np.zeros(len(chunks), np.float32)}, tokens=np.array(ntok, np.int32), chars_per_token=3.5))
        ours_r = lb.recalibrate(chunks, ntok)
        assert [c.est_tokens for c in theirs_r] == [c.est_tokens for c in ours_r] == ntok
        # scores with many ties (rounded), as float32 like longjev's arrays
        rel = np.asarray([round(rng.random(), 1) for _ in chunks], dtype=np.float32)
        for budget in (1000, 8000, 16000):
            k_t = lj.asm.select_round_robin(ours_r, {"q": rel}, budget)
            k_o = lb.select_round_robin(ours_r, {"q": rel}, budget)
            assert k_t == k_o
            assert lj.asm.render_state(ours_r, k_t) == lb.render_state(ours_r, k_o)
            assert sum(ours_r[i].est_tokens + lb.GAP_TOKENS for i in k_o) <= budget or len(k_o) == 1


@need_longjev
def test_stats_parity(lj):
    for k, n in ((0, 10), (5, 10), (86, 163), (163, 163)):
        assert lj.rep.wilson(k, n) == lb.wilson(k, n)
    for b, c in ((16, 10), (0, 0), (3, 9)):
        assert lj.rep.mcnemar(b, c) == lb.mcnemar(b, c)


# ------------------------------------------------------------------------------------------------ 2. readout

@pytest.fixture(scope="module")
def fake():
    import decoder_io as dio
    import run_lb as R
    from transformers import AutoTokenizer
    sel.set_prompt_layout(dio, ADAPTER, "Qwen/Qwen3.5-4B")
    tok = AutoTokenizer.from_pretrained(str(ADAPTER))
    tok.padding_side = "right"
    model = R.tiny_model(tok)
    return SimpleNamespace(dio=dio, tok=tok, model=model, ro=dio.Readout(tok))


@need_adapter
def test_read_rows_equals_a5_read(fake):
    import ohs3_lib
    rng = random.Random(4)
    rows = []
    for i in range(14):
        if i % 3 == 0:
            rows.append({"id": f"n{i}", "qtype": "noul", "state": synth_text(rng, rng.randint(50, 3000)),
                         "instructions": "Q " + words(rng, 8), "options": None})
        else:
            rows.append({"id": f"c{i}", "qtype": "choice", "state": synth_text(rng, rng.randint(50, 3000)),
                         "instructions": "Q " + words(rng, 8), "options": [f"opt {i} {j} {words(rng, 3)}" for j in range(4)]})
    for readout in ("2view", "single"):
        ours = lb.read_rows(fake.dio, fake.model, fake.ro, rows, "cpu", readout, batch_size=4, token_budget=3000)
        p1, pr = ohs3_lib.a5_read(fake.dio, fake.model, fake.ro, rows, "cpu", readout, batch_size=4, token_budget=3000)
        for r, o, a, b in zip(rows, ours, p1, pr):
            if r["qtype"] == "noul":
                assert o["p_yes"] == b["yes"]
            else:
                assert o["p1"] == [a[x] for x in r["options"]]
                assert o["p"] == [b[x] for x in r["options"]]
    assert ohs3_lib.predict_batches(rows, 4, 3000) == lb.predict_batches(rows, 4, 3000)


@need_adapter
def test_duplicate_options_keep_both(fake):
    row = {"id": "dup", "qtype": "choice", "state": "some text", "instructions": "Q?", "options": ["x", "y", "y", "z"]}
    o = lb.read_rows(fake.dio, fake.model, fake.ro, [row], "cpu", "2view")[0]
    assert len(o["p"]) == 4 and abs(sum(o["p"]) - 1) < 1e-6 and o["p"][1] != o["p"][2]
    assert lb.argmax_letter([0.2, 0.3, 0.3, 0.2]) == "B"


# ------------------------------------------------------------------------------------------------ 3. cascade rule

def test_cascade_rule_equals_ohs3_lib():
    import cascade_lb as C
    import ohs3_lib
    rng = random.Random(5)
    for _ in range(300):
        n = rng.choice([2, 4])
        row = {"qtype": "noul"} if n == 2 else {"qtype": "choice", "options": ["a", "b", "c", "d"]}
        keys = ["yes", "no"] if n == 2 else row["options"]
        ps = [rng.random() for _ in range(n)]
        pb = [rng.random() for _ in range(n)]
        if n == 2:
            ps, pb = [ps[0], 1 - ps[0]], [pb[0], 1 - pb[0]]
        T, tau, w = rng.uniform(0.5, 2), rng.uniform(0.3, 1.0), rng.choice([1.0, 0.7])
        d = lambda p: dict(zip(keys, p))  # noqa: E731
        Td = {"noul": T, "choice": T}
        assert C.scaled(ps, T) == list(ohs3_lib.apply_T(d(ps), row, Td).values())
        rt = ohs3_lib.cascade_routed(row, d(ps), tau)
        assert C.routed(ps, tau) == rt
        assert C.answer(ps, pb, rt, w) == list(ohs3_lib.cascade_answer(row, d(ps), d(pb), rt, w).values())


# ------------------------------------------------------------------------------------------------ 4. end to end

@pytest.fixture(scope="module")
def e2e(tmp_path_factory):
    import convert
    import make_synthetic
    d = tmp_path_factory.mktemp("lb2")
    make_synthetic.main(["--out", str(d / "data.json"), "--n", "112", "--n-long", "10", "--long-min", "106000",
                         "--long-max", "125000", "--seed", "11"])
    convert.main(["--data", str(d / "data.json"), "--tokenizer", str(ADAPTER), "--out", str(d / "kit"), "--synthetic"])
    return d


@need_adapter
def test_end_to_end(e2e, monkeypatch):
    import cascade_lb as C
    import run_lb as R
    import score_lb as S
    kit = e2e / "kit"
    real_open = builtins.open

    def guarded(f, *a, **k):  # run_lb must never open the gold labels
        assert "lb_gold" not in str(f), "run_lb opened the gold file"
        return real_open(f, *a, **k)

    monkeypatch.setattr(builtins, "open", guarded)
    monkeypatch.setattr(io, "open", guarded)  # pathlib's read_text / open go through io.open
    base = ["--fake-model", "--model", str(ADAPTER), "--base", "Qwen/Qwen3.5-4B", "--choice-readout", "2view",
            "--items", str(kit / "lb_items.jsonl")]
    out_b = R.main(base + ["--out", str(e2e / "big"), "--name", "big"])
    out_s = R.main(base + ["--out", str(e2e / "small"), "--name", "small"])
    monkeypatch.setattr(builtins, "open", real_open)
    monkeypatch.setattr(io, "open", real_open)
    with pytest.raises(SystemExit, match="exists"):  # once per model: no silent second run
        R.main(base + ["--out", str(e2e / "big")])
    with pytest.raises(SystemExit, match="complete"):  # a finished run is never resumed
        R.main(base + ["--out", str(e2e / "big"), "--resume"])
    index = {r["id"]: r for r in lb.read_jsonl(kit / "lb_index.jsonl")}
    union = {i for i, m in index.items() if lb.in_set(m, "all_proxy") or lb.in_set(m, "all_own")}
    preds = lb.read_jsonl(out_b / "preds.jsonl")
    assert {p["id"] for p in preds} == union
    cs = {r["id"]: r for r in lb.read_jsonl(out_b / "chunk_scores.jsonl")}
    items = {it["id"]: it for it in lb.read_jsonl(kit / "lb_items.jsonl")}
    for p in preds:
        it = items[p["id"]]
        assert len(cs[p["id"]]["p_yes"]) == p["n_chunks"] == len(lb.chunk_state(it["context"]))
        if p["final_failed"] is None:
            assert p["pred"] in lb.LETTERS and abs(sum(p["p"]) - 1) < 1e-6
            assert p["kept_tokens"] + lb.GAP_TOKENS * p["n_kept"] <= p["budget"] or p["n_kept"] == 1
            # the kept set is exactly longjev's selection on the stored scores
            chunks = lb.recalibrate(lb.chunk_state(it["context"]), cs[p["id"]]["tokens"])
            kept, b = sel.keep(it, chunks, cs[p["id"]]["p_yes"])
            assert sorted(kept) == p["kept"] and b == p["budget"]
    huge = [p for p in preds if p["budget"] < lb.BUDGET]
    assert huge and all(p["final_failed"] == "too_long" and p["failed_chunks"] == p["n_chunks"] for p in huge)
    res = S.score(out_b, kit)
    tp = res["sets"]["test_proxy"]
    assert tp["n"] == sum(lb.in_set(m, "test_proxy") for m in index.values())
    assert res["primary"]["comparison"]["verdict"] in ("better", "worse", "no significant difference")
    assert res["diagnostics"]["final_failed"] == len(huge)
    tp_ids = sorted(i for i, m in index.items() if lb.in_set(m, "test_proxy"))
    ov = e2e / "ov.json"
    ov.write_text(json.dumps({"hit_ids": {"question_option": tp_ids[:1], "context": tp_ids + ["not-an-item"]}}))
    so = S.score(out_b, kit, overlap=ov)["sensitivity_overlap"]
    assert so["test_proxy_minus_question_option"]["n"] == tp["n"] - 1
    assert so["test_proxy_minus_context"]["n"] == 0 and so["test_proxy_minus_context"]["dropped"] == tp["n"]
    # the failed item counts wrong under the strict rule and is dropped under longjev's rule
    allp = res["sets"]["all_proxy"]
    assert allp["longjev_rule"]["n"] == allp["n"] - sum(1 for p in huge if lb.in_set(index[p["id"]], "all_proxy"))
    # cascade (fake small = fake big: same tiny model)
    fit = {"dev_only": True, "splits": ["dev"], "config_values": {"tau": 0.9, "w_big": 1.0, "route_on": "raw"},
           "small": {"model": "small", "T": {"noul": 1.0, "choice": 0.95}},
           "big": {"model": "big", "T": {"noul": 1.0, "choice": 1.0}}}  # a synthetic cascade_rule_fit.py --json
    (e2e / "fit.json").write_text(json.dumps(fit))
    cfg = {"name": "casc", "tau": 0.9, "w_big": 1.0, "route_on": "raw",
           "fit_log": str(e2e / "fit.json"), "fit_log_sha256": lb.sha256_file(e2e / "fit.json"),
           "small": {"run": str(out_s), "model": str(ADAPTER), "base": "Qwen/Qwen3.5-4B", "choice_readout": "2view",
                     "T": {"noul": 1.0, "choice": 0.95}},
           "big": {"run": str(out_b), "model": str(ADAPTER), "base": "Qwen/Qwen3.5-4B", "choice_readout": "2view",
                   "T": {"noul": 1.0, "choice": 1.0}}}
    cargs = ["--config", str(e2e / "casc.json"), "--items", str(kit / "lb_items.jsonl"), "--out", str(e2e / "casc"),
             "--fake-model"]
    # tau / w_big / route_on / T only from the named dev-only fit log
    for bad, msg in (({"fit_log": None}, "must name"), ({"tau": 0.8}, "differs from its fit log"),
                     ({"small": {**cfg["small"], "T": {"noul": 1.0, "choice": 1.0}}}, "differs from its fit log"),
                     ({"fit_log_sha256": "0" * 64}, "sha256")):
        (e2e / "casc.json").write_text(json.dumps({**cfg, **bad}))
        with pytest.raises(SystemExit, match=msg):
            C.main(cargs)
    assert not (e2e / "casc").exists()
    (e2e / "casc.json").write_text(json.dumps(cfg))
    out_c = C.main(cargs)
    mc = json.loads((out_c / "manifest.json").read_text())
    assert mc["adapters_sha256"]["big"] == lb.sha256_file(ADAPTER / "adapter_model.safetensors")
    assert {"cascade_lb.py", "run_lb.py", "lb_lib.py", "lb_select.py", "decoder_io.py"} <= set(mc["code_sha256"])
    with pytest.raises(SystemExit, match="runs once"):
        C.main(cargs)
    rc = S.score(out_c, kit)
    assert rc["sets"]["all_proxy"]["n"] == allp["n"]
    assert 0 <= rc["cascade"]["chunk_routed_share"] <= 1
    # identical small and big reads -> the cascade's chunk scores equal each model's -> same kept sets
    pc = {p["id"]: p for p in lb.read_jsonl(out_c / "preds.jsonl")}
    for p in preds:
        assert pc[p["id"]]["kept"] == p["kept"]


# ------------------------------------------------------------------------------------------------ 5. real-data guards

def fake_real_kit(tmp_path):
    rng = random.Random(6)
    kit = tmp_path / "kit"
    kit.mkdir()
    it = synth_item(rng, 0, 1000)
    (kit / "lb_items.jsonl").write_text(json.dumps({"id": it["_id"], **it}) + "\n")
    meta = {"real": True, "data_sha256": lb.DATA_SHA256, "data_revision": lb.DATA_REVISION, "counts": {}, "sets": {},
            "files": {"lb_items.jsonl": lb.sha256_file(kit / "lb_items.jsonl")}}
    (kit / "lb_meta.json").write_text(json.dumps(meta))
    return kit


@need_adapter
def test_real_guards(tmp_path, monkeypatch):
    import run_lb as R
    kit = fake_real_kit(tmp_path)
    base = ["--model", str(ADAPTER), "--base", "Qwen/Qwen3.5-4B", "--choice-readout", "2view",
            "--items", str(kit / "lb_items.jsonl"), "--out", str(tmp_path / "o")]
    with pytest.raises(SystemExit, match="synthetic data only"):
        R.main(base + ["--limit", "1"])
    with pytest.raises(SystemExit, match="not allowed"):
        R.main(base + ["--fake-model"])
    ledger = tmp_path / "LEDGER.jsonl"
    sha = lb.sha256_file(ADAPTER / "adapter_model.safetensors")
    ledger.write_text(json.dumps({"event": "start", "name": "x", "adapter_sha256": sha, "data_sha256": lb.DATA_SHA256,
                                  "out": "/elsewhere", "utc": "t"}) + "\n")
    monkeypatch.setattr(R, "LEDGER", ledger)
    with pytest.raises(SystemExit, match="run once per model"):
        R.main(base)


def test_published_numbers_consistent():
    import score_lb as S
    j = S.JEV
    # McNemar discordant counts agree with the two accuracies (86 - 80 = 16 - 10)
    assert j["test_jev_8k"]["k"] - j["test_embed_16k"]["k"] == j["mcnemar_jev_vs_embed_test"]["only_jev"] - \
        j["mcnemar_jev_vs_embed_test"]["only_embed"]
    assert round(lb.mcnemar(16, 10), 2) == 0.33
    d, lo, hi = lb.newcombe_diff(86, 163, 86, 163)
    assert d == 0 and lo < 0 < hi


@need_longjev
def test_jev_file_headline_equals_longjev_report(lj, tmp_path, monkeypatch):
    """Fed per-item answers in longjev's results/raw/items.jsonl format (SYNTHETIC here), our scorer reproduces the
    number longjev's own eval/report.build prints for "jev" on the test split (and the McNemar pairing it uses)."""
    import contextlib
    import score_lb as S
    rng = random.Random(9)
    rows, gold = [], {}
    for i in range(42 + 163 + 60):
        split = "dev" if i < 42 else "test" if i < 205 else rng.choice(["dev", "test"])
        fits, ans = i >= 205, rng.choice("ABCD")
        gold[f"j{i}"] = ans
        r = {"id": f"j{i}", "split": split, "domain": "d", "sub_domain": "s", "difficulty": "easy", "length": "short",
             "answer": ans, "n_chunks": 50, "context_tokens": 20000 if fits else 60000, "results": {}, "fits": fits,
             "timing": {"embed": {"seconds": 1, "requests": 1}, "jev": {"seconds": 1, "requests": 50, "tokens": 1}},
             "shortlist": 40, "vote": {"choice": rng.choice("ABCD")}}
        for s in ("truncate", "embed", "jev", "embed_then_jev"):
            for b in ((8000, 16000, 28000) if split == "dev" else (8000, 16000)):
                p = 0.6 if (s, b) == ("jev", 8000) else 0.4
                ch = None if rng.random() < 0.04 else (ans if rng.random() < p else rng.choice("ABCD"))
                r["results"][f"{s}@{b}"] = {"choice": ch, "suff": 0.5, "kept": [0], "state_tokens": 7000, "seconds": 1}
        if fits:
            r["direct"] = {"choice": ans, "suff": 0.9}
        rows.append(r)
    (tmp_path / "results/raw").mkdir(parents=True)
    (tmp_path / "results/raw/items.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    monkeypatch.chdir(tmp_path)
    with contextlib.redirect_stdout(io.StringIO()):
        summ = lj.rep.build()
    assert summ["frozen_budgets"]["jev"] == 8000
    h = summ["headline"]["jev"]["test"]
    test_ids = {r["id"] for r in rows if not r["fits"] and r["split"] == "test"}
    got = S.jev_file_headline(tmp_path / "results/raw/items.jsonl", gold, test_ids)
    assert (got["k"], got["n"]) == (h["k"], h["n"]) and got["file_rows_in_test_proxy"] == 163
    assert lb.wilson(got["k"], got["n"]) == (h["low"], h["high"])
    # longjev's paired() McNemar (jev vs embed) = our longjev_pairing when embed's answers play "ours"
    emb = summ["frozen_budgets"]["embed"]
    ours = [{"id": r["id"], "pred": r["results"][f"embed@{emb}"]["choice"]} for r in rows if r["id"] in test_ids]
    pr = S.compare_paired(ours, gold, tmp_path / "results/raw/items.jsonl", n_boot=200)["longjev_pairing"]
    pj = summ["pairs"]["test"]["jev_vs_embed"]
    assert (pr["n"], pr["only_jev"], pr["only_ours"]) == (pj["n"], pj["only_first"], pj["only_second"])
    assert pr["mcnemar_p"] == round(pj["p"], 4)


def test_compare_paired(tmp_path):
    import score_lb as S
    rng = random.Random(8)
    ids = [f"i{k}" for k in range(60)]
    gold = {i: rng.choice("ABCD") for i in ids}
    ours = [{"id": i, "pred": gold[i] if rng.random() < 0.6 else "A"} for i in ids]
    jev = [{"id": i, "results": {"jev@8000": {"choice": gold[i] if rng.random() < 0.5 else "B"}}} for i in ids]
    p = tmp_path / "items.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in jev) + "\n")
    res = S.compare_paired(ours, gold, p, n_boot=2000)
    a = sum(r["pred"] == gold[r["id"]] for r in ours)
    b = sum(r["results"]["jev@8000"]["choice"] == gold[r["id"]] for r in jev)
    assert res["n_common"] == 60 and res["diff_pp"] == round(100 * (a - b) / 60, 2)
    assert res["only_ours"] - res["only_jev"] == a - b
    lo, hi = res["paired_bootstrap95_pp"]
    assert lo <= res["diff_pp"] <= hi
