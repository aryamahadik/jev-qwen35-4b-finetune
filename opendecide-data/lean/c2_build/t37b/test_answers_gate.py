"""t37b/test_answers_gate.py: answers_gate.py (strict answer contract, G-LEX vote rule, READY / SHORT verdict).

Synthetic inputs are built in memory or under pytest's tmp_path; the real answer files, pools and the frozen v1 files
are only READ (their sha256 is compared before and after). No answer is made up on disk under lean/.
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/t37b/test_answers_gate.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

import pytest  # noqa: E402

from c2_kit import chunker  # noqa: E402
from t37b import answers_gate as G  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402

QIDS = ["qAAAAAAAAAA", "qBBBBBBBBBB", "qCCCCCCCCCC"]
FIVE = ["Is it a?", "Is it b?", "Is it c?", "Is it d?", "Is it e?"]


def raw(obj) -> bytes:
    return json.dumps(obj).encode()


def author_obj(qids=QIDS, qs=FIVE):
    return [{"qid": q, "questions": list(qs)} for q in qids]


def polarity_obj(qids=QIDS, rel="same"):
    return [{"qid": q, "relation": rel} for q in qids]


def sha_of(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ the file contract

def test_good_files_pass():
    assert G.validate_bytes(raw(author_obj()), "author_wording", QIDS) == []
    assert G.validate_bytes(raw(polarity_obj()), "polarity", QIDS) == []
    assert G.validate_bytes((json.dumps(polarity_obj(), indent=1) + "\n").encode(), "polarity", QIDS) == []
    for r in ("same", "opposite", "unclear"):
        assert G.validate_bytes(raw(polarity_obj(rel=r)), "polarity", QIDS) == []


@pytest.mark.parametrize("mutate", [
    lambda o: o[:2],                                                    # one item unanswered
    lambda o: o + [dict(o[0])],                                         # a qid answered twice (and too many objects)
    lambda o: [dict(o[0], qid="qZZZZZZZZZZ")] + o[1:],                  # unknown qid
    lambda o: [dict(o[0], qid="q123")] + o[1:],                         # malformed qid
    lambda o: [dict(o[0], extra="x")] + o[1:],                          # extra key
    lambda o: [{"qid": o[0]["qid"]}] + o[1:],                           # missing field
    lambda o: [dict(o[0], questions=FIVE[:4])] + o[1:],                 # 4 questions
    lambda o: [dict(o[0], questions=FIVE + ["Is it f?"])] + o[1:],      # 6 questions
    lambda o: [dict(o[0], questions="Is it a?")] + o[1:],               # not a list
    lambda o: [dict(o[0], questions=FIVE[:4] + [7])] + o[1:],           # a non-string
    lambda o: [dict(o[0], questions=FIVE[:4] + ["Is it e"])] + o[1:],   # no question mark
    lambda o: [dict(o[0], questions=FIVE[:4] + ["Is it e? "])] + o[1:],  # trailing space
    lambda o: [dict(o[0], questions=FIVE[:4] + [" Is it e?"])] + o[1:],  # leading space
    lambda o: [dict(o[0], questions=FIVE[:4] + ["Is\nit e?"])] + o[1:],  # two lines
    lambda o: [dict(o[0], questions=FIVE[:4] + [""])] + o[1:],           # empty
    lambda o: {"answers": o},                                           # not an array
])
def test_author_contract_rejects(mutate):
    assert G.validate_bytes(raw(mutate(author_obj())), "author_wording", QIDS)


@pytest.mark.parametrize("mutate", [
    lambda o: [dict(o[0], relation="Same")] + o[1:],
    lambda o: [dict(o[0], relation=" same")] + o[1:],
    lambda o: [dict(o[0], relation="same.")] + o[1:],
    lambda o: [dict(o[0], relation="SAME")] + o[1:],
    lambda o: [dict(o[0], relation="maybe")] + o[1:],
    lambda o: [dict(o[0], relation=None)] + o[1:],
    lambda o: [dict(o[0], relation=["same"])] + o[1:],
    lambda o: [dict(o[0], relation="same", why="x")] + o[1:],
    lambda o: [{"qid": o[0]["qid"], "answer": "same"}] + o[1:],
    lambda o: o[:1],
    lambda o: o + o[:1],
])
def test_polarity_contract_rejects(mutate):
    assert G.validate_bytes(raw(mutate(polarity_obj())), "polarity", QIDS)


@pytest.mark.parametrize("blob", [
    b"",
    b"   \n",
    "\ufeff".encode() + raw(polarity_obj()),                      # byte-order mark
    b"```json\n" + raw(polarity_obj()) + b"\n```",                  # markdown fence
    b"Here you go: " + raw(polarity_obj()),                         # text before
    raw(polarity_obj()) + b" thanks",                               # text after
    b"[" + raw(polarity_obj())[1:-1] + b",]",                       # trailing comma
    b'[{"qid": "qAAAAAAAAAA", "relation": "same", "relation": "same"}]',   # duplicate key
    b'[{"qid": "qAAAAAAAAAA", "relation": NaN}]',                   # non-JSON constant
    b"\xff\xfe[]",                                                  # not UTF-8
])
def test_unparseable_files_rejected(blob):
    assert G.validate_bytes(blob, "polarity", QIDS)


def test_strict_is_stricter_than_the_family_reader():
    """The family reader accepts ' Same'; the contract does not (the file is rejected, never edited)."""
    assert BL.norm_relation({"relation": " Same"}) == "same"
    assert G.validate_bytes(raw(polarity_obj()[:2] + [{"qid": QIDS[2], "relation": " Same"}]), "polarity", QIDS)
    b = chunker.make_batch("polarity", "T37b", [("k1", {"question_a": "A?", "question_b": "B?"})], seed="s", prompt="p")
    qid = next(iter(b.key))
    lenient, _p = chunker.load_answers(b, {b.chunks[0]["task_id"]: [{"qid": qid, "relation": "same", "note": 1}]})
    assert lenient == {"k1": {"relation": "same", "note": 1}}            # extra key accepted by the family reader
    assert G.validate_bytes(raw([{"qid": qid, "relation": "same", "note": 1}]), "polarity", [qid])


# ------------------------------------------------------------------------------------------------ the vote rule (G-LEX)

def test_glex_status_is_the_kit_rule():
    assert G.REQUIRED_READS == 2
    assert G.glex_status([("a", "same"), ("b", "same")], True) == "admitted"
    assert G.glex_status([("a", "same"), ("b", "unclear")], True) == "rejected"      # any other reading rejects
    assert G.glex_status([("a", "opposite"), ("b", "same")], True) == "rejected"
    assert G.glex_status([("a", "same")], True) == "pending"                          # one read is not 2/2
    assert G.glex_status([], True) == "pending"
    assert G.glex_status([("a", "same"), ("a", "same")], True) == "pending"           # one extractor twice is not 2
    assert G.glex_status([("a", "same"), ("b", "same")], False) == "unit_fail"
    assert G.glex_status([("a", "same"), ("b", "unclear")], False) == "rejected"      # rejected wins (kit order)
    assert G.glex_status([("a", "same"), ("b", "same")], True, required=3) == "pending"   # 3/3 kinds need 3


@pytest.fixture(scope="module")
def rounds_and_results():
    return G.validate_all()


def _r2(rounds):
    by = {r["name"]: r for r in rounds}
    return by["r2-read-A"], by["r2-read-B"]


def _all_same(rnd):
    return {c["task_id"]: [{"qid": it["qid"], "relation": "same"} for it in c["items"]] for c in rnd["batch"].chunks}


def test_vote_rows_follow_the_rule(rounds_and_results):
    rounds, _res = rounds_and_results
    ra, rb = _r2(rounds)
    va, vb = _all_same(ra), _all_same(rb)
    rows = G.vote_rows(ra["cands"], ra, rb, va, vb)
    assert len(rows) == len(ra["cands"]) == 100 and {r["status"] for r in rows} == {"admitted"}
    assert all(r["extractors"][0] != r["extractors"][1] for r in rows)
    # one 'unclear' read rejects that paraphrase for good; the others stay admitted
    tid = rb["batch"].chunks[0]["task_id"]
    vb2 = {k: [dict(a) for a in v] for k, v in vb.items()}
    vb2[tid][0]["relation"] = "unclear"
    rows2 = G.vote_rows(ra["cands"], ra, rb, va, vb2)
    assert sorted(r["status"] for r in rows2).count("rejected") == 1 and G.admitted_ids(rows2) != G.admitted_ids(rows)
    assert len(G.admitted_ids(rows2)) == 99
    # a rejected / missing read file removes its votes: those paraphrases are pending, never admitted
    vb3 = {k: v for k, v in vb.items() if k != tid}
    rows3 = G.vote_rows(ra["cands"], ra, rb, va, vb3)
    assert sum(r["status"] == "pending" for r in rows3) == len(rb["batch"].chunks[0]["items"])
    assert all(r["reads"][1] is None for r in rows3 if r["status"] == "pending")
    # the same extractor set twice (read A used for both reads) is one extractor: nothing is admitted
    rows4 = G.vote_rows(ra["cands"], ra, ra, va, va)
    assert {r["status"] for r in rows4} == {"pending"}


def test_valid_raw_uses_only_valid_files(rounds_and_results):
    rounds, results = rounds_and_results
    rnd, res = rounds[0], results[0]
    assert set(G.valid_raw(rnd, res)) == {f["task_id"] for f in res["files"]}
    bad = {**res, "files": [dict(res["files"][0], valid=False)] + res["files"][1:]}
    assert res["files"][0]["task_id"] not in G.valid_raw(rnd, bad)


# ------------------------------------------------------------------------------------------------ the real files

def test_every_real_answer_file_passes_and_nothing_is_edited(rounds_and_results):
    rounds, results = rounds_and_results
    assert [r["round"] for r in results] == ["v1-author", "v1-read-A", "v1-read-B", "r2-author", "r2-read-A",
                                             "r2-read-B"]
    assert [r["n_tasks"] for r in results] == [9, 5, 5, 3, 2, 2]
    assert [r["n_items"] for r in results] == [66, 212, 212, 22, 100, 100]
    files = [f for r in results for f in r["files"]]
    assert len(files) == 26 and all(f["valid"] for f in files), [f for f in files if not f["valid"]]
    assert all(not r["round_problems"] for r in results)
    before = {f["file"]: f["sha256"] for f in files}
    _r, again = G.validate_all()
    assert {f["file"]: f["sha256"] for r in again for f in r["files"]} == before
    for f in files:
        assert sha_of(_C2_BUILD / f["file"]) == f["sha256"]


def test_v1_freeze_untouched():
    assert G.v1_untouched() == []
    assert sha_of(AP.POOL_FILE) == G.redo2().V1_POOL_SHA256


def test_v1_untouched_detects_a_change(tmp_path, monkeypatch):
    fm = json.loads(G.FREEZE_MANIFEST.read_text(encoding="utf-8"))
    some = next(iter(fm["sha256"]))
    fm["sha256"][some] = "0" * 64
    p = tmp_path / "fm.json"
    p.write_text(json.dumps(fm), encoding="utf-8")
    monkeypatch.setattr(G, "FREEZE_MANIFEST", p)
    assert G.v1_untouched() == [f"{some} changed"]


def test_targets_are_the_g0_targets():
    t = G.pool_entry_targets()
    assert len(t) == 20 and sum(t.values()) == 155
    assert t == json.loads((AP.POOL_DIR / "MANIFEST.json").read_text(encoding="utf-8"))["report"]["targets"]
    assert sorted(set(t.values())) == [AP.TARGET_FIXED, AP.TARGET_SLOTTED] == [7, 12]


# ------------------------------------------------------------------------------------------------ the verdict

def test_gate_without_the_supplement_is_short_by_exactly_the_v1_shortfalls(tmp_path):
    g = G.gate(supplement=tmp_path / "absent.json")
    assert g["verdict"] == "SHORT" and not g["ready"]
    assert g["totals"] == {"target": 155, "admitted": 210, "v1": 210, "redo2": 0}
    assert sorted(g["shortfalls"]) == sorted([
        "gd_comve/against: 0 of 12 (short by 12)", "gd_multiwoz21_sysacts/match: 0 of 7 (short by 7)",
        "gd_nhtsa_complaints/injury: 0 of 7 (short by 7)", "gd_taskmaster1/status: 1 of 12 (short by 11)"])
    failed = {c["check"] for c in g["checks"] if not c["pass"]}
    assert failed == {"redo2 supplement admitted", "G0 minimum: every pool entry at or above its target"}


@pytest.fixture(scope="module")
def real_gate():
    return G.gate()


def test_gate_on_the_written_pools(real_gate):
    g = real_gate
    assert [c for c in g["checks"] if not c["pass"]] == []
    assert g["verdict"] == "READY" and g["ready"] and g["shortfalls"] == [] and g["issues"] == []
    assert g["totals"] == {"target": 155, "admitted": 309, "v1": 210, "redo2": 99}
    assert all(v["admitted"] >= v["target"] and v["shortfall"] == 0 for v in g["per_entry"].values())
    assert g["votes"]["redo2"] == {"admitted": 99, "rejected": 1} and g["votes"]["v1"] == {"admitted": 210, "rejected": 2}
    assert len(g["votes"]["rejected"]) == 3 and all(r["reads"][1] == "unclear" for r in g["votes"]["rejected"])
    assert g["validation"]["valid"] == g["validation"]["files"] == 26
    assert len(g["answer_files"]) == 26


def test_gate_flags_a_supplement_that_differs_from_the_votes(tmp_path):
    R = G.redo2()
    obj = json.loads(R.SUPP_POOL.read_text(encoding="utf-8"))
    obj["paraphrases"] = obj["paraphrases"][1:]                       # one admitted paraphrase silently missing
    p = tmp_path / "supp_missing.json"
    p.write_text(json.dumps(obj), encoding="utf-8")
    g = G.gate(supplement=p)
    assert g["verdict"] == "SHORT"
    assert "redo2 supplement on disk = re-derived admissions" in {c["check"] for c in g["checks"] if not c["pass"]}


def test_gate_flags_a_supplement_that_breaks_the_loader(tmp_path):
    R = G.redo2()
    obj = json.loads(R.SUPP_POOL.read_text(encoding="utf-8"))
    obj["paraphrases"][0] = dict(obj["paraphrases"][0], reads=["same", "unclear"])
    p = tmp_path / "supp_bad_read.json"
    p.write_text(json.dumps(obj), encoding="utf-8")
    g = G.gate(supplement=p)
    assert g["verdict"] == "SHORT"
    assert any(c["check"].startswith("merged pool loads") and not c["pass"] for c in g["checks"])
    dup = json.loads(R.SUPP_POOL.read_text(encoding="utf-8"))
    dup["paraphrases"].append(AP.load_pool(AP.POOL_FILE).paraphrases[0])         # a v1 paraphrase repeated
    p2 = tmp_path / "supp_dup.json"
    p2.write_text(json.dumps(dup), encoding="utf-8")
    assert G.gate(supplement=p2)["verdict"] == "SHORT"


def test_supplement_is_the_frozen_family_output():
    """pools/redo2 is exactly what the family's own admit stage rebuilds (same bytes), and v1 is not touched."""
    R = G.redo2()
    files, man = R.admit_files()
    for name, text in files.items():
        assert (R.SUPP / name).read_text(encoding="utf-8") == text, name
    assert man["report"]["merged_shortfall"] == {}
    pool = R.load_merged_pool()
    assert len(pool.paraphrases) == 309
    assert {c["sem"] for c in pool.paraphrases} == set(G.pool_entry_targets())
    assert all(c["reads"] == ["same", "same"] and c["status"] == "admitted" for c in pool.paraphrases)
    texts = [(c["sem"], AP.norm(c["template"])) for c in pool.paraphrases]
    assert len(set(texts)) == len(texts)
    for c in pool.paraphrases:                                       # the unchanged unit test on every loaded record
        assert G.unit_ok(c)[0], c["template"]
    assert BL.g0_problems() == []


# ------------------------------------------------------------------------------------------------ round integrity

def _round(tmp_path):
    items = [(f"id{i}", {"question_a": f"Is A{i}?", "question_b": f"Is B{i}?"}) for i in range(3)]
    b = chunker.make_batch("polarity", "T37b", items, seed="s", prompt="Judge.")
    root = tmp_path / "rnd"
    for relpath, text in b.files().items():
        (root / relpath).parent.mkdir(parents=True, exist_ok=True)
        (root / relpath).write_text(text, encoding="utf-8")
    text_fn = lambda bb, c, r: f"task {c['task_id']}\n"      # noqa: E731
    (root / "tasks").mkdir()
    (root / "answers").mkdir()
    for c in b.chunks:
        (root / "tasks" / f"{c['task_id']}.md").write_text(text_fn(b, c, root), encoding="utf-8")
    tasks = {"batch_id": b.batch_id, "tasks": [{"task_id": c["task_id"], "n_items": len(c["items"]),
                                                "answer_file": str(root / b.answer_path(c["task_id"]))}
                                               for c in b.chunks]}
    (root / "TASKS.json").write_text(json.dumps(tasks), encoding="utf-8")
    rnd = {"name": "synthetic", "kind": "polarity", "root": root, "batch": b, "tasks_json": root / "TASKS.json",
           "text": text_fn}
    return rnd, b, root


def test_round_integrity_checks(tmp_path):
    rnd, b, root = _round(tmp_path)
    tid = b.chunks[0]["task_id"]
    ans = root / b.answer_path(tid)
    qids = [it["qid"] for it in b.chunks[0]["items"]]
    ans.write_bytes(raw(polarity_obj(qids)))
    res = G.validate_round(rnd)
    assert res["n_valid"] == 1 and res["files"][0]["valid"] and res["files"][0]["sha256"] == sha_of(ans)
    # a stray file in answers/ is a round problem: every file of the round is rejected
    (root / "answers" / "stray.json").write_text("[]", encoding="utf-8")
    assert not G.validate_round(rnd)["files"][0]["valid"]
    (root / "answers" / "stray.json").unlink()
    # a task file that differs from its rebuild rejects that task
    (root / "tasks" / f"{tid}.md").write_text("edited\n", encoding="utf-8")
    r2 = G.validate_round(rnd)
    assert any("task file differs" in p for p in r2["files"][0]["problems"])
    (root / "tasks" / f"{tid}.md").write_text(rnd["text"](b, b.chunks[0], root), encoding="utf-8")
    # a chunk file that differs from the rebuild rejects that task
    cpath = root / b.chunk_path(tid)
    good = cpath.read_text(encoding="utf-8")
    cpath.write_text(good.replace("Is A0?", "Is A9?"), encoding="utf-8")
    assert any("chunk file" in p for p in G.validate_round(rnd)["files"][0]["problems"])
    cpath.write_text(good, encoding="utf-8")
    # a missing answer file, then an answer that breaks the contract
    ans.unlink()
    assert G.validate_round(rnd)["files"][0]["problems"] == ["answer file missing"]
    ans.write_bytes(raw(polarity_obj(qids, rel="Same")))
    bad = G.validate_round(rnd)["files"][0]
    assert not bad["valid"] and any("relation" in p for p in bad["problems"])
    assert ans.read_bytes() == raw(polarity_obj(qids, rel="Same"))      # never edited
    assert G.valid_raw(rnd, G.validate_round(rnd)) == {}
    # a wrong TASKS.json batch id rejects the round
    man = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    man["batch_id"] = "other"
    (root / "TASKS.json").write_text(json.dumps(man), encoding="utf-8")
    ans.write_bytes(raw(polarity_obj(qids)))
    rr = G.validate_round(rnd)
    assert rr["round_problems"] and not rr["files"][0]["valid"]


def test_cli_validate_and_gate_write_nothing_without_flag(capsys):
    rec = G.RECORD
    before = sha_of(rec) if rec.is_file() else None
    assert G.main(["validate"]) == 0
    assert G.main(["gate"]) == 0
    capsys.readouterr()
    assert (sha_of(rec) if rec.is_file() else None) == before
