import json
import sys

import pytest
import torch

from oc1 import common as C
from oc1 import items as I
from oc1 import backend as B
from oc1 import measure as M

from fastcore import testing as T          # noqa: E402  (hosting/ is on sys.path after oc1.items)
from fakes import FakeSGLangServer           # noqa: E402

TOL = 2e-5


@pytest.fixture(scope="module")
def world():
    tok, ro = T.c1_tokenizer(), T.readout()
    R = I.readout_mod()
    SH = I.sglang_host_mod()
    model = T.tiny_model(seed=0)
    srv = FakeSGLangServer(model)
    client = SH.SGLangClient(srv.url, timeout=60.0, max_connections=64)
    items = C.read_jsonl(C.ROOT / "data" / "P.jsonl")
    pick = []
    for kind in ("noul", "2-4", "5-9", "10-25", "26+"):
        pick += [it for it in items if it["bucket"] == kind and len(it["request"]["state"]) < 600][:3]
    preps = [I.prepare_one(it, R, ro, tok) for it in pick]
    yield {"srv": srv, "client": client, "preps": preps, "items": pick, "model": model, "tok": tok, "ro": ro, "R": R,
           "dio": R.dio}
    client.close()
    srv.close()


def ref_probs(w, prep, it):
    """decoder_io.predict(tta_choice=True) on the same tiny model = the A5 readout."""
    row = prep.named[0][1]
    out = w["dio"].predict(w["model"], w["tok"], [row], batch_size=1, dev="cpu", tta_choice=True)[0]
    return out


def test_generate_backend_equals_decoder_io(world):
    gen = B.GenerateBackend(world["client"])
    for it, prep in zip(world["items"], world["preps"]):
        ans, meta = gen.read(prep, return_views=True)
        got = B.answer_probs(ans["q0"], prep.qtype)
        ref = ref_probs(world, prep, it)
        for k in ref:
            assert abs(got[k] - ref[k]) < TOL, (prep.bucket, k)
        assert meta["prompt_tokens"] == prep.n_tokens and meta["n_seq"] == len(prep.items)


def test_score_backend_equals_generate_backend(world):
    gen, sc = B.GenerateBackend(world["client"]), B.ScoreBackend(world["client"])
    for prep in world["preps"]:
        a = B.answer_probs(gen.read(prep)[0]["q0"], prep.qtype)
        b = B.answer_probs(sc.read(prep)[0]["q0"], prep.qtype)
        assert max(abs(a[k] - b[k]) for k in a) < TOL, prep.bucket
    assert world["srv"].calls["score"] >= len(world["preps"])


def test_score_body_reproduces_each_views_ids_exactly(world):
    for prep in world["preps"]:
        by_q = {}
        for it in prep.items:
            by_q.setdefault(it.q, []).append(it)
        for its in by_q.values():
            body = B.score_body(its)
            assert body["apply_softmax"] is True and body["item_first"] is False and body["label_token_ids"] == its[0].flat
            for it, suffix in zip(its, body["items"]):
                assert body["query"] + suffix == it.ids and len(suffix) >= 1
            assert len(body["query"]) >= 1


def test_scores_to_logits_validates():
    class It:                       # a stand-in work item
        flat, sizes = [1, 2, 3], [2, 1]
    out = B.scores_to_logits([It], [[0.1, 0.2, 0.7]])
    assert torch.allclose(out[0], torch.tensor([0.3, 0.7]).log(), atol=1e-6)
    with pytest.raises(B.BackendError):
        B.scores_to_logits([It], [[0.1, 0.2]])
    with pytest.raises(B.BackendError):
        B.scores_to_logits([It], [[0.0, 0.0, 0.0]])
    with pytest.raises(B.BackendError):
        B.scores_to_logits([It, It], [[0.1, 0.2, 0.7]])


def test_read_many_equals_individual_reads(world):
    gen = B.GenerateBackend(world["client"])
    group = world["preps"][:4]
    many, meta = gen.read_many(group)
    assert meta["n_seq"] == sum(len(p.items) for p in group)
    for p, ans in zip(group, many):
        one = gen.read(p)[0]
        a, b = B.answer_probs(ans["q0"], p.qtype), B.answer_probs(one["q0"], p.qtype)
        assert max(abs(a[k] - b[k]) for k in a) < 1e-9


def test_measurements_run_and_report(world):
    gen = B.GenerateBackend(world["client"])
    preps = world["preps"]
    par = M.parity_pass(gen, preps, conc=4)
    assert par["n_missing"] == 0 and len(par["answers"]) == len(preps)
    assert all("probs" in a for a in par["answers"].values())
    assert any("views" in a for a in par["answers"].values())          # choice rows keep the per-view probabilities
    assert par["summary"]["ok"] == len(preps) and par["summary"]["decisions_per_h"]
    lat = M.latency_batch1(gen, preps * 2, warm=3)
    assert lat["n"] == len(preps) * 2 - 3 and lat["wall_ms"]["p50"] > 0 and lat["server_e2e_ms"]["n"] == lat["n"]
    bat = M.latency_batched(gen, preps * 2, b=4, rounds=3, warm_rounds=1)
    assert bat["one_call"]["call_ms"]["n"] >= 1 and bat["simultaneous"]["per_call_ms"]["n"] >= 4
    tp = M.throughput(gen, preps, (2, 4), client=world["client"])
    assert tp["c2"]["ok"] == len(preps) and tp["c4"]["decisions_per_h"] > 0
    ph = M.prefix_hit(gen, preps, client=world["client"], conc=2, n=10)
    assert ph["rows"] == min(10, len(preps)) and ph["cached_token_share"] is not None
    assert world["srv"].calls["flush"] >= 3


def test_closed_loop_collects_errors_without_dying(world):
    gen = B.GenerateBackend(world["client"])
    world["srv"].fail_next = 2
    recs, wall = M.closed_loop(gen.read, world["preps"][:6], 1)
    bad = [r for r in recs if not r["ok"]]
    assert len(bad) == 2 and len(recs) == 6
    s = M.loop_summary(recs, wall)
    assert s["failed"] == 2 and s["errors"]
