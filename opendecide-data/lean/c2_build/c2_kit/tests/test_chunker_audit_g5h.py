"""Tests for c2_kit.chunker (TEACH-0 chunks), c2_kit.audit (file-access auditor) and c2_kit.g5h (G5-H)."""
from __future__ import annotations

import json

import pytest

from c2_kit import audit as A
from c2_kit import chunker as C
from c2_kit import g5h
from c2_kit import pipeline
from c2_kit.paths import LEAN

PROMPT = "Answer each question from its text only. Reply with JSON."


def _items(n):
    return [(f"c2_r00:{i:016x}", {"kind": "yes/no", "text": f"Text {i}.", "question": "Is it so?"}) for i in range(n)]


def test_batches_are_gold_free_opaque_and_small():
    b = C.make_batch("blind_read", "R00", _items(120), seed="s1", prompt=PROMPT)
    assert [len(c["items"]) for c in b.chunks] == [50, 50, 20]
    assert len(b.key) == 120 and all(q.startswith("q") and len(q) == 11 for q in b.key)
    blob = json.dumps(b.chunks)
    assert "c2_r00:" not in blob and "gold" not in blob
    files = b.files()
    assert set(files) >= {b.prompt_path(), f"key/{b.batch_id}.json", f"manifest/{b.batch_id}.json"}
    assert all("c2_r00:" not in t for p, t in files.items() if p.startswith("chunks/"))
    b2 = C.make_batch("blind_read", "R00", _items(120), seed="s1", prompt=PROMPT)
    assert b2.key == b.key and b2.chunks == b.chunks                      # deterministic
    b3 = C.make_batch("blind_read", "R00", _items(120), seed="s2", prompt=PROMPT)
    assert set(b3.key) != set(b.key)                                      # another seed, other opaque ids


@pytest.mark.parametrize("kind,item,kw", [
    ("blind_read", {"kind": "yes/no", "text": "t", "question": "q", "gold": 1}, {}),
    ("blind_read", {"kind": "choice", "text": "t", "question": "q", "options": ["a", "b"], "meta": {}}, {}),
    ("blind_read", {"kind": "choice", "text": "t", "question": "q"}, {}),
    ("extract_g3h", {"text": "t", "schema": [{"field": "x", "type": "str", "answer": "y"}]}, {}),
    ("author_skin", {"brief": "write a memo", "register": "memo", "extra": 1}, {}),
    ("author_skin", {"brief": "write a memo where the claim is approved", "register": "memo"},
     {"forbid_strings": ("approved",)}),
    ("author_pack", {"brief": f"see {LEAN}/ohs4_sealed/brief.md"}, {}),
    ("nonsense", {"brief": "x"}, {}),
])
def test_items_that_leak_or_overreach_are_refused(kind, item, kw):
    with pytest.raises(C.ChunkError):
        C.make_batch(kind, "R00", [("id-1", item)], seed="s", prompt=PROMPT, **kw)


def test_label_blind_authoring_needs_and_applies_forbid_strings():
    item = [("s1", {"brief": "a short memo about a purchase", "register": "memo"})]
    with pytest.raises(C.ChunkError):
        C.make_batch("author_skin", "R00", item, seed="s", prompt=PROMPT)
    C.make_batch("author_skin", "R00", item, seed="s", prompt=PROMPT, forbid_strings=("approve", "manual review"))
    with pytest.raises(C.ChunkError):
        C.make_batch("author_skin", "R00", item, seed="s", prompt="Never write the word approve.",
                     forbid_strings=("approve",))


def test_internal_ids_never_reach_the_chunk_or_prompt():
    with pytest.raises(C.ChunkError):
        C.make_batch("blind_read", "R00", [("rid-77", {"kind": "yes/no", "text": "see rid-77", "question": "q"})],
                     seed="s", prompt=PROMPT)
    with pytest.raises(C.ChunkError):
        C.make_batch("blind_read", "R00", _items(2), seed="s", prompt="ids: c2_r00:0000000000000000")
    with pytest.raises(C.ChunkError):
        C.make_batch("blind_read", "R00", _items(2), seed="s", prompt=PROMPT, max_items=51)


def test_load_answers_maps_back_and_reports_misuse():
    b = C.make_batch("blind_read", "R00", _items(60), seed="s", prompt=PROMPT)
    t0, t1 = b.chunks[0], b.chunks[1]
    raw = {t0["task_id"]: [{"qid": it["qid"], "answer": "yes"} for it in t0["items"]],
           t1["task_id"]: {it["qid"]: {"answer": "no"} for it in t1["items"][:-1]}}
    raw[t1["task_id"]][t0["items"][0]["qid"]] = "no"         # answered in the wrong task
    raw[t1["task_id"]]["qdeadbeef00"] = "no"                 # unknown
    got, probs = C.load_answers(b, raw)
    assert len(got) == 59 and all(v == {"answer": "yes"} for k, v in got.items() if b.task_of[
        next(q for q, i in b.key.items() if i == k)] == t0["task_id"])
    assert any("belongs to" in p for p in probs) and any("unknown" in p for p in probs)
    assert any("unanswered" in p for p in probs)


def test_auditor_passes_clean_agents_and_flags_everything_else():
    root = str(LEAN / "c2_build" / "_tasks")
    b = C.make_batch("blind_read", "R00", _items(3), seed="s", prompt=PROMPT)
    tid = b.chunks[0]["task_id"]
    rd, wr = b.allowed(root, tid)
    chunk = f"{root}/{b.chunk_path(tid)}"

    def tu(name, **inp):
        return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}}

    clean = [tu("Read", file_path=chunk), tu("Read", file_path=f"{root}/{b.prompt_path()}"),
             tu("Write", file_path=f"{root}/{b.answer_path(tid)}", content="{}")]
    rep = A.audit(clean, allowed_read=rd, allowed_write=wr)
    assert rep.ok and rep.n_calls == 3 and not rep.as_dict()["notes"]
    rep = A.audit(clean[:1] + clean[2:], allowed_read=rd, allowed_write=wr)
    assert rep.ok and rep.as_dict()["notes"]                                  # prompt never read: a note only
    other = f"{root}/chunks/{tid[:-3]}999.json"
    cases = {
        "violation": [tu("Read", file_path=other)],
        "critical": [tu("Read", file_path=str(LEAN / "ohs4_sealed" / "suite.jsonl"))],
    }
    for sev, ev in cases.items():
        rep = A.audit(clean + ev, allowed_read=rd, allowed_write=wr)
        assert not rep.ok and rep.as_dict()["critical" if sev == "critical" else "violations"]
    for ev in ([tu("Bash", command="ls")], [tu("Glob", pattern="**/*.json")], [tu("WebFetch", url="https://x.test")],
               [tu("Write", file_path=f"{root}/answers/someone_else.json", content="{}")]):
        assert not A.audit(clean + ev, allowed_read=rd, allowed_write=wr).ok
    rep = A.audit(clean + [tu("Bash", command=f"cat {LEAN}/teach0/jev_U/out.json")], allowed_read=rd,
                  allowed_write=wr)
    assert rep.as_dict()["critical"]
    nested = {"records": [{"x": clean}, {"y": [tu("Read", file_path=other)]}]}
    assert not A.audit(nested, allowed_read=rd, allowed_write=wr).ok


# ------------------------------------------------------------------------------------------------ G5-H

def _rows(plugin, ctx, n=40):
    out = []
    for seed in range(n):
        res = pipeline.build_unit(plugin, plugin.sample(seed, "S1"), ctx, run_g15=False)
        out += res.rows
    return out


def test_two_reads_differ_in_order_and_ids(plugin, ctx):
    rows = _rows(plugin, ctx, 20)
    a, b = g5h.make_reads(rows, "R00", seed="pilot", prompt=PROMPT)
    assert set(a.key.values()) == set(b.key.values()) == {r["id"] for r in rows}
    assert set(a.key) != set(b.key)
    ia, ib = C.item_by_internal(a), C.item_by_internal(b)
    r = rows[0]
    assert {k: v for k, v in ia[r["id"]].items() if k != "qid"} == g5h.read_item(r)
    assert {k: v for k, v in ib[r["id"]].items() if k != "qid"} == g5h.read_item(r)
    assert ia[r["id"]]["qid"] != ib[r["id"]]["qid"]
    assert "gold" not in json.dumps(a.chunks) and "meta" not in json.dumps(b.chunks)


def test_normalize_answer():
    yn = {"kind": "yes/no"}
    ch = {"kind": "choice", "options": ["Auto-approved", "Manual review"]}
    assert g5h.normalize_answer(yn, "Yes.") == 1 and g5h.normalize_answer(yn, {"answer": "no"}) == 0
    assert g5h.normalize_answer(yn, "maybe") is None
    assert g5h.normalize_answer(ch, "manual review") == "Manual review" and g5h.normalize_answer(ch, "B") == "Manual review"
    assert g5h.normalize_answer(ch, "(A)") == "Auto-approved" and g5h.normalize_answer(ch, "C") is None


def test_score_queue_controls_quarantine_and_finalize(plugin, ctx):
    rows = _rows(plugin, ctx, 60)
    by_id = {r["id"]: r for r in rows}
    a, b = g5h.make_reads(rows, "R00", seed="pilot", prompt=PROMPT)
    items = C.item_by_internal(a)

    def say(r, right=True):
        g = r["gold"]
        if r["qtype"] == "noul":
            return {"answer": ("yes" if g == 1 else "no") if right else ("no" if g == 1 else "yes")}
        return {"answer": g if right else next(o for o in r["options"] if o != g)}

    wrong_b = {rows[3]["id"], rows[7]["id"]}
    ans_a = {r["id"]: say(r) for r in rows}
    ans_b = {r["id"]: say(r, r["id"] not in wrong_b) for r in rows}
    del ans_a[rows[11]["id"]]                                           # a missing answer goes to the queue too
    res = g5h.score(rows, items, ans_a, ans_b, seed="pilot")
    assert set(res["queue"]) == wrong_b | {rows[11]["id"]}
    assert len(res["control"]) == 30 and not set(res["control"]) & set(res["queue"])
    adj, key = g5h.adjudication_items(by_id, res, seed="pilot")
    assert len(adj) == 33 and all("program_answer" in it for _, it in adj)
    verdicts = {rid: "gold_ok" for rid in key.values()}
    rep = g5h.finalize(by_id, res, verdicts)
    assert rep["missing_verdicts"] == [] and rep["wrong_gold"] == []
    assert rep["pass"]                                   # quarantine drops a template's rows; it is not a failure
    assert rep["quarantined_templates"] == res["quarantined"]
    if res["quarantined"]:
        assert any(rows_of in rep["drop_rows"] for rows_of in [r["id"] for r in rows
                   if r["meta"]["c2"]["skin_id"] in res["quarantined"]])
    rep = g5h.finalize(by_id, res, {**verdicts, rows[3]["id"]: "wrong_gold"})
    assert not rep["pass"] and rep["generator_bug"]
    rep = g5h.finalize(by_id, res, {k: v for k, v in verdicts.items() if k != rows[7]["id"]})
    assert not rep["pass"] and rep["missing_verdicts"] == [rows[7]["id"]]
    two_amb = {**verdicts, rows[3]["id"]: "ambiguous", rows[7]["id"]: "ambiguous"}
    rep = g5h.finalize(by_id, res, two_amb)
    assert rep["ambiguous_rate"] == 2 / len(rows) and rep["pass"] == (2 / len(rows) <= 0.01)
    assert set(two_amb) >= set(rep["ambiguous"]) and rows[3]["id"] in rep["drop_rows"]


def test_template_quarantine_above_three_percent(plugin, ctx):
    rows = _rows(plugin, ctx, 60)
    a, _ = g5h.make_reads(rows, "R00", seed="q", prompt=PROMPT)
    items = C.item_by_internal(a)
    target = rows[0]["meta"]["c2"]["skin_id"]
    ans = {}
    for r in rows:
        right = r["meta"]["c2"]["skin_id"] != target or r is not rows[0]
        g = r["gold"]
        ans[r["id"]] = {"answer": (("yes" if g == 1 else "no") if right else ("no" if g == 1 else "yes"))
                        if r["qtype"] == "noul" else (g if right else next(o for o in r["options"] if o != g))}
    res = g5h.score(rows, items, ans, None, seed="q")
    n = res["templates"][target]["n"]
    assert (target in res["quarantined"]) == (1 / n > 0.03)
