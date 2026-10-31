import pytest

from oc1 import common as C
from oc1 import voice as V


def test_wer():
    assert V.wer("the cat sat", "the cat sat") == 0.0
    assert V.wer("The cat, sat!", "the cat sat") == 0.0                      # punctuation / case ignored
    assert V.wer("the cat sat", "the cat") == pytest.approx(1 / 3)
    assert V.wer("a b c d", "a x c d y") == pytest.approx(2 / 4)
    assert V.wer("", "") == 0.0 and V.wer("", "x") == 1.0
    assert V.wer("well-known fact", "well known fact") == 0.0


def test_speakable_and_clean():
    assert V.clean_state("Message:\nHello   there,\nfriend") == "Hello there, friend"
    long_ok = "I ordered the blue jacket last week and it still has not arrived at my house yet."
    assert V.speakable(long_ok) and not V.speakable("too short") and not V.speakable("x" * 300)
    assert not V.speakable("Check https://example.com for the details of this very long order status update")
    assert not V.speakable("Total = $45.00 {balance} due at the end of the month for all of the services used")


def item(i, qtype, state, n_opts=3):
    q = {"type": qtype, "instructions": "q"}
    if qtype == "choice":
        q["options"] = [f"o{k}" for k in range(n_opts)]
    return {"id": i, "qtype": qtype, "request": {"id": i, "state": state, "questions": {"q0": q}}}


def test_pick_prompts_balanced_deterministic():
    txt = "The delivery was late and the package arrived damaged, so I would like a refund please."
    items = [item(f"n{i}", "noul", txt + f" {i}") for i in range(80)] + [item(f"c{i}", "choice", txt + f" {i}") for i in range(80)]
    items += [item("big", "choice", txt, 20), item("bad", "noul", "short")]
    a = V.pick_prompts(items, n=40, seed=0)
    b = V.pick_prompts(items, n=40, seed=0)
    assert [x["id"] for x in a] == [x["id"] for x in b] and len(a) == 40
    assert sum(x["qtype"] == "noul" for x in a) == 20
    assert "big" not in {x["id"] for x in a} and "bad" not in {x["id"] for x in a}
    assert V.with_state(a[0]["request"], "new")["state"] == "new" and V.with_state(a[0]["request"], "new")["questions"] == a[0]["request"]["questions"]


def test_streaming_latency_algebra():
    # 10 chunks of 0.16 s, each computed in 20 ms: the compute keeps up, nothing queues behind the audio
    r = V.streaming_latency([20.0] * 10, audio_s=1.6, chunk_s=0.16, flush_ms=15.0)
    assert r["backlog_ms"] == pytest.approx(20.0, abs=0.5)               # last chunk finishes 20 ms after its arrival
    assert r["final_flush_ms"] == pytest.approx(35.0, abs=0.6)
    assert r["expected_unflushed_ms"] == pytest.approx(r["final_flush_ms"] + 80.0, abs=0.1)
    # compute slower than real time builds a backlog
    slow = V.streaming_latency([300.0] * 10, audio_s=1.6, chunk_s=0.16, flush_ms=10.0)
    assert slow["backlog_ms"] > 1000 and slow["final_flush_ms"] > r["final_flush_ms"]
