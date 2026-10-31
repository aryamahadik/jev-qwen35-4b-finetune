"""Tests for transfer/T21/freeze_v2.py (nothing is written to the repo; the freeze itself is only refused against a temp
folder).

  contract    validate_answer: one JSON list, exactly {qid, payload...}, every expected qid once; every way to break it is
              rejected whole and the file is never touched; load_disk_batch detects a tampered prompt, chunk or key;
              a task named in --ignore / AUDIT_FAILED_IGNORED is ignored (its answers are dropped)
  votes       record_votes follows c2_kit.lexicon: 2/2 admits, an unlisted / other-sense vote rejects for good, one read
              stays pending, a precedence form needs 3/3, an extractor cannot vote twice; g3h_votes: exact compare,
              a missing read is a mismatch
  select      G0 section 9: the lowest-ranked passing candidates fill exactly the need; a cell short of passers stays short
  registry    canonical_registry keeps the v1 reads, records the new reads through the kit, and does not depend on the
              order of the chosen forms
  union       relint_union flags a repeated text across pools, a label word and a banned pack word
  build       (one full in-memory freeze-v2, ~15 s) every answer file of every round valid; freeze-v1 reproduced byte for
              byte and untouched; v1 pieces carried over unchanged; G0 minimums, G-LEX used-form gate, kit rules (two
              distinct reads, no strict kinds); the chosen pieces are the lowest-ranked passers; the plugin runs on
              these pools; ignoring the three newest answers gives SHORT with exactly the cells that wait on them;
              pools_v2/ on disk (when frozen) equals this build byte for byte
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/transfer/T21/test_freeze_v2.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T21 import freeze_pools as FP  # noqa: E402
from transfer.T21 import freeze_v2 as FV  # noqa: E402
from transfer.T21 import haiku_author as HA  # noqa: E402

THREE_NEWEST = ("T21-extract_g3h-3000b2f2-000", "T21-extract_lex-97beea5b-000", "T21-extract_lex-b62465a2-000")


# ------------------------------------------------------------------------------------------------ small batches
def _batch(kind: str = "extract_lex", n: int = 3):
    if kind == "extract_lex":
        items = [(f"internal-form-{i:03d}", {"text": f"text {i}", "choices": ["a", "b"]}) for i in range(n)]
    elif kind == "extract_g3h":
        items = [(f"internal-note-{i:03d}", {"text": f"note {i}", "schema": [{"field": "claimant"}]}) for i in range(n)]
    else:
        items = [(f"internal-item-{i:03d}", {"brief": f"b{i}"}) for i in range(n)]
    return chunker.make_batch(kind, "T21", items, seed="seed", prompt="prompt text")


def _write(tmp_path: Path, name: str, content) -> Path:
    p = tmp_path / name
    p.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    return p


def _answers(b, payload="meaning", value="a"):
    return [{"qid": q, payload: value} for q in b.key]


# ------------------------------------------------------------------------------------------------ answer contract
def test_validate_answer_accepts_the_exact_contract(tmp_path):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    p = _write(tmp_path, "ok.json", _answers(b))
    before = p.read_bytes()
    r = FV.validate_answer(b, tid, p, ("meaning",))
    assert r["ok"] and r["problems"] == [] and r["n"] == 3 and len(r["answers"]) == 3
    assert r["sha256"] == FV._sha(before) and p.read_bytes() == before


@pytest.mark.parametrize("name, build", [
    ("wrapper object", lambda b: {"answers": _answers(b)}),
    ("extra key", lambda b: [dict(a, extra=1) for a in _answers(b)]),
    ("wrong payload key", lambda b: _answers(b, payload="text")),
    ("skipped qid", lambda b: _answers(b)[:-1]),
    ("qid twice", lambda b: _answers(b) + _answers(b)[:1]),
    ("unknown qid", lambda b: _answers(b)[:-1] + [{"qid": "qdeadbeef00", "meaning": "a"}]),
    ("empty payload", lambda b: [dict(a, meaning="  ") for a in _answers(b)]),
    ("payload not a string", lambda b: [dict(a, meaning=None) for a in _answers(b)]),
    ("qid not a string", lambda b: [dict(a, qid=1) for a in _answers(b)]),
    ("not objects", lambda b: [a["qid"] for a in _answers(b)]),
])
def test_validate_answer_rejects_every_contract_break(tmp_path, name, build):
    b = _batch()
    p = _write(tmp_path, "bad.json", build(b))
    before = p.read_bytes()
    r = FV.validate_answer(b, b.chunks[0]["task_id"], p, ("meaning",))
    assert not r["ok"] and r["problems"] and r["answers"] == [], name
    assert p.read_bytes() == before                                           # never edited


def test_validate_answer_rejects_bad_files(tmp_path):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    good = json.dumps(_answers(b))
    for name, text in (("fenced", "```json\n" + good + "\n```"), ("text before", "Here you go: " + good),
                       ("two lists", good + good), ("NaN", good.replace('"a"', "NaN", 1)), ("empty file", ""),
                       ("not json", "[{"), ("BOM", "﻿" + good)):
        r = FV.validate_answer(b, tid, _write(tmp_path, "f.json", text), ("meaning",))
        assert not r["ok"] and r["answers"] == [], name
    r = FV.validate_answer(b, tid, tmp_path / "missing.json", ("meaning",))
    assert not r["ok"] and r["problems"] == ["answer file missing"]


def test_validate_answer_payload_types(tmp_path):
    b = _batch("author_pack")
    qids = list(b.key)
    tid = b.chunks[0]["task_id"]
    pk = {"agreements": ["A"], "parties": ["B"]}
    assert FV.validate_answer(b, tid, _write(tmp_path, "p.json", [{"qid": q, "pack": pk} for q in qids]), ("pack",))["ok"]
    assert not FV.validate_answer(b, tid, _write(tmp_path, "p2.json", [{"qid": q, "pack": "A B"} for q in qids]),
                                  ("pack",))["ok"]
    assert not FV.validate_answer(b, tid, _write(tmp_path, "p3.json", [{"qid": q, "pack": {}} for q in qids]),
                                  ("pack",))["ok"]
    assert FV.validate_answer(b, tid, _write(tmp_path, "t.json", [{"qid": q, "text": "x"} for q in qids]), ("text",))["ok"]
    assert not FV.validate_answer(b, tid, _write(tmp_path, "t2.json", [{"qid": q, "text": 3} for q in qids]),
                                  ("text",))["ok"]


def test_validate_answer_g3h_two_fields(tmp_path):
    b = _batch("extract_g3h")
    tid = b.chunks[0]["task_id"]
    both = [{"qid": q, "claimant": "Brindle Foods", "agreement": "Lowmoor hosting agreement"} for q in b.key]
    assert FV.validate_answer(b, tid, _write(tmp_path, "g.json", both), ("claimant", "agreement"))["ok"]
    # a wrong value is a G3-H mismatch (item level), not a bad file; a missing / extra field or a non-string is a bad file
    assert FV.validate_answer(b, tid, _write(tmp_path, "g1.json", [dict(a, claimant="") for a in both]),
                              ("claimant", "agreement"))["ok"]
    for name, bad in (("missing field", [{"qid": q, "claimant": "X"} for q in b.key]),
                      ("extra field", [dict(a, note="x") for a in both]),
                      ("non-string", [dict(a, agreement=None) for a in both]),
                      ("list value", [dict(a, claimant=["X"]) for a in both])):
        r = FV.validate_answer(b, tid, _write(tmp_path, "g2.json", bad), ("claimant", "agreement"))
        assert not r["ok"] and r["answers"] == [], name


def _disk_batch(tmp_path: Path, b) -> Path:
    root = tmp_path / "disk"
    for rel, text in b.files().items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def test_load_disk_batch_detects_tampering(tmp_path):
    b = _batch(n=4)
    root = _disk_batch(tmp_path, b)
    got, probs = FV.load_disk_batch(root, b.batch_id)
    assert probs == [] and got.key == b.key and got.task_of == b.task_of
    # a changed prompt
    prompt = root / "prompts" / f"{b.prompt_sha[:16]}.txt"
    prompt.write_text("another prompt", encoding="utf-8")
    assert any("prompt" in p for p in FV.load_disk_batch(root, b.batch_id)[1])
    prompt.write_text(b.prompt, encoding="utf-8")
    # a changed chunk
    cpath = root / "chunks" / f"{b.chunks[0]['task_id']}.json"
    c = json.loads(cpath.read_text(encoding="utf-8"))
    c["items"][0]["text"] = "changed"
    cpath.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    assert any("chunk" in p for p in FV.load_disk_batch(root, b.batch_id)[1])
    cpath.write_text(b.files()[f"chunks/{b.chunks[0]['task_id']}.json"], encoding="utf-8")
    # a key that maps a qid to another internal id
    kpath = root / "key" / f"{b.batch_id}.json"
    k = json.loads(kpath.read_text(encoding="utf-8"))
    q0, q1 = sorted(k["key"])[:2]
    k["key"][q0], k["key"][q1] = k["key"][q1], k["key"][q0]
    kpath.write_text(json.dumps(k), encoding="utf-8")
    assert any("not derived" in p for p in FV.load_disk_batch(root, b.batch_id)[1])


def test_ignored_audit_failures_are_dropped(tmp_path, monkeypatch):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    p = _write(tmp_path, f"{tid}.json", _answers(b))
    spec = FV.TaskSpec("redo2-b", tid, "glex", b.kind, ("meaning",), p, b)
    res, _ = FV.validate_all([spec], ignore=(tid,))
    r = res[("redo2-b", tid)]
    assert not r["ok"] and r["audit_failed_ignored"] and r["answers"] == []
    res, _ = FV.validate_all([spec])                                   # nothing ignored by default
    assert res[("redo2-b", tid)]["ok"]
    monkeypatch.setattr(FV, "AUDIT_FAILED_IGNORED", (p.name,))        # the module list works by file name too
    res, _ = FV.validate_all([spec])
    assert res[("redo2-b", tid)]["audit_failed_ignored"] and not res[("redo2-b", tid)]["ok"]


def test_a_changed_task_file_rejects_its_answers(tmp_path):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    p = _write(tmp_path, f"{tid}.json", _answers(b))
    spec = FV.TaskSpec("redo2-b", tid, "glex", b.kind, ("meaning",), p, b, problems=["the task file on disk differs"])
    res, _ = FV.validate_all([spec])
    assert not res[("redo2-b", tid)]["ok"] and res[("redo2-b", tid)]["answers"] == []


def test_a_rejected_v1_file_is_a_baseline_problem_and_an_unmapped_file_is_found(tmp_path, monkeypatch):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    p = _write(tmp_path, f"{tid}.json", "[{")
    spec = FV.TaskSpec("author-v1", tid, "glex", b.kind, ("meaning",), p, b)
    _res, probs = FV.validate_all([spec])
    assert any("author-v1" in x for x in probs)
    stray = _write(tmp_path, "stray.json", "[]")
    monkeypatch.setattr(FV, "ANSWER_DIRS", (tmp_path,))
    _res, probs = FV.validate_all([FV.TaskSpec("redo2-a", tid, "x", b.kind, ("meaning",), p, b)])
    assert any("unmapped answer file" in x and stray.name in x for x in probs)


# ------------------------------------------------------------------------------------------------ G-LEX / G3-H votes
SEM_A, SEM_B = "q.t21.alpha", "q.t21.beta"
MEAN_A, MEAN_B = "asks alpha", "asks beta"


def _reg(strict: bool = False):
    reg = LexiconRegistry("T21")
    reg.declare(SEM_A, "question", MEAN_A)
    reg.declare(SEM_B, "question", MEAN_B)
    f = reg.add("Is alpha true in clause {CAP_ID}?", SEM_A, slots={"CAP_ID": "id"}, source="haiku", family="T21",
                haiku_task_id="t", haiku_prompt_sha="0" * 64)
    reg.unit_test_all()
    return reg, f.form_id


def test_record_votes_two_of_two_admits():
    reg, fid = _reg()
    FV.record_votes(reg, "r1", {fid: {"meaning": MEAN_A}})
    assert reg.status(fid) == "pending"                                        # one read is never enough
    c = FV.record_votes(reg, "r2", {fid: {"meaning": MEAN_A}})
    assert reg.status(fid) == "admitted" and c["listed"] == 1
    assert reg.gate([fid])["pass"]


@pytest.mark.parametrize("pick", [MEAN_B, "NONE", "asks something else entirely", None])
def test_record_votes_a_disagreement_rejects_for_good(pick):
    reg, fid = _reg()
    FV.record_votes(reg, "r1", {fid: {"meaning": MEAN_A}})
    FV.record_votes(reg, "r2", {fid: {"meaning": pick}})
    assert reg.status(fid) == "rejected"
    FV.record_votes(reg, "r3", {fid: {"meaning": MEAN_A}})                     # a later agreeing read cannot rescue it
    assert reg.status(fid) == "rejected" and not reg.gate([fid])["pass"]


def test_record_votes_extra_keys_and_independence():
    reg, fid = _reg()
    FV.record_votes(reg, "r1", {fid: {"meaning": MEAN_A, "extra": 1}})         # not exactly {"meaning"}: no valid pick
    assert reg.status(fid) == "rejected"
    reg, fid = _reg()
    FV.record_votes(reg, "r1", {fid: {"meaning": MEAN_A}})
    with pytest.raises(LexiconError):
        FV.record_votes(reg, "r1", {fid: {"meaning": MEAN_A}})                 # one extractor cannot vote twice
    assert FV.record_votes(reg, "r2", {"nope#00000000": {"meaning": MEAN_A}}) == {"form_not_in_registry": 1}


def test_a_precedence_form_needs_three_distinct_reads():
    reg = LexiconRegistry("T21")
    reg.declare("prec.t21.later", "precedence", "the later rule wins")
    f = reg.add("the newer rule overrides", "prec.t21.later", source="haiku", family="T21", haiku_task_id="t",
                haiku_prompt_sha="0" * 64)
    reg.unit_test_all()
    assert f.required == 3
    for i, ext in enumerate(("r1", "r2")):
        FV.record_votes(reg, ext, {f.form_id: {"meaning": "the later rule wins"}})
    assert reg.status(f.form_id) == "pending"                                  # 2/2 is not enough for a strict kind
    FV.record_votes(reg, "r3", {f.form_id: {"meaning": "the later rule wins"}})
    assert reg.status(f.form_id) == "admitted"


def _g3_spec(b, answers):
    spec = FV.TaskSpec("redo2-b", b.chunks[0]["task_id"], "g3h", "extract_g3h", ("claimant", "agreement"),
                       Path("unused.json"), b)
    res = {("redo2-b", spec.task_id): {"ok": answers is not None, "answers": answers or []}}
    return spec, res


def test_g3h_votes_exact_compare_and_missing_reads():
    b = _batch("extract_g3h", 3)
    iids = sorted(b.key.values())
    qid_of = {iid: q for q, iid in b.key.items()}
    expected = {iid: {"claimant": f"Alpha {i}", "agreement": f"Beta {i} agreement"} for i, iid in enumerate(iids)}
    ans = [{"qid": qid_of[iids[0]], "claimant": "Alpha 0", "agreement": "Beta 0 agreement"},        # exact
           {"qid": qid_of[iids[1]], "claimant": " Alpha 1 ", "agreement": "Beta 1 agreement"},      # outer spaces: fine
           {"qid": qid_of[iids[2]], "claimant": "Alpha 2", "agreement": "Beta 2 contract"}]         # wrong agreement
    spec, res = _g3_spec(b, ans)
    out = FV.g3h_votes(b, expected, [spec], res)
    assert out[iids[0]]["ok"] and out[iids[1]]["ok"] and not out[iids[2]]["ok"]
    assert "agreement" in out[iids[2]]["diffs"][0]
    spec, res = _g3_spec(b, None)                                              # file rejected: every narrative drops
    out = FV.g3h_votes(b, expected, [spec], res)
    assert all(not d["ok"] and d["diffs"] == ["no extraction"] and not d["read"] for d in out.values())


# ------------------------------------------------------------------------------------------------ selection
def _plans(n_by_cell: dict):
    plan = {}
    for cell, n in n_by_cell.items():
        for r in range(n):
            plan[f"{cell}.{100 + r}"] = {"cell": cell, "rank": r}
    return {"packs": {}, "skins": plan, "freeform": {}, "wordings": {}}


def test_select_takes_the_lowest_ranked_passers_and_leaves_the_rest_unused():
    plans = _plans({"skins|a": 6})
    bad = {"skins|a.100", "skins|a.103"}
    chosen, sel = FV.select([("skins", "a", 2)], plans, lambda p, i: "lint: x" if i in bad else "pass")
    assert chosen["skins"] == ["skins|a.101", "skins|a.102"]
    rec = sel["skins|a"]
    assert rec["short_after"] == 0 and [c["used"] for c in rec["candidates"]] == [False, True, True, False, False, False]
    assert rec["candidates"][0]["status"] == "lint: x"


def test_select_leaves_a_cell_short_when_passers_run_out():
    plans = _plans({"skins|a": 3})
    chosen, sel = FV.select([("skins", "a", 2)], plans, lambda p, i: "pass" if i.endswith("101") else "G3-H: no read")
    assert chosen["skins"] == ["skins|a.101"] and sel["skins|a"]["short_after"] == 1


# ------------------------------------------------------------------------------------------------ registry
def test_canonical_registry_keeps_v1_reads_and_ignores_chosen_order():
    base = FV.load_v1()["lexicon"]
    q = HA.QSTRINGS
    assert q                                                                   # fixture texts stay out of the pools
    new = [{"iid": "x1", "qform": "yn_capped", "sem": "q.t21.yn_capped", "slots": {"CAP_ID": "id"}, "tid": "tid-1",
            "psha": "1" * 64, "text": "Per the test, is liability limited by the cap of clause {CAP_ID} here?",
            "extractions": [("e1", "q.t21.yn_capped"), ("e2", "q.t21.yn_capped")]},
           {"iid": "x2", "qform": "ch_clause", "sem": "q.t21.ch_clause", "slots": {}, "tid": "tid-2",
            "psha": "2" * 64, "text": "Per the test, which clause decides how this claim is treated?",
            "extractions": [("e1", "q.t21.ch_clause"), ("e2", "q.t21.ch_clause")]}]
    a = FV.canonical_registry(base, new)
    b = FV.canonical_registry(base, list(reversed(new)))
    assert a.to_json() == b.to_json()
    assert len(a.forms) == len(base["forms"]) + 2
    v1 = LexiconRegistry.from_json(base)
    for fid, f in v1.forms.items():
        assert a.forms[fid].extractions == f.extractions and a.forms[fid].unit_ok
    for c in new:
        fid = FV._form_id(c["sem"], c["text"])
        assert a.status(fid) == "admitted" and [e for e, _ in a.forms[fid].extractions] == ["e1", "e2"]


# ------------------------------------------------------------------------------------------------ union lint
def _good_pool():
    v1 = FV.load_v1()
    return v1["packs"], v1["skins"], v1["freeform"], v1["attacks"], v1["wordings"]


def test_relint_union_passes_the_v1_pools():
    assert FV.relint_union(*_good_pool()) == []


def test_relint_union_flags_a_repeated_text_a_label_word_and_a_banned_name():
    packs, skins, free, attacks, wordings = _good_pool()
    dup = make_skin("T21-SK-board_note.900", "T21", skins[0].text, dict(skins[0].slots), register="board_note")
    assert any("duplicate" in p for p in FV.relint_union(packs, skins + [dup], free, attacks, wordings))
    leaky = make_skin("T21-SK-board_note.901", "T21", "The cap is unlimited for {CLAIMANT} under the {AGREEMENT}.",
                      {"CLAIMANT": "name", "AGREEMENT": "name"}, register="board_note")
    assert any("T21-SK-board_note.901" in p for p in FV.relint_union(packs, skins + [leaky], free, attacks, wordings))
    bad_pack = dict(packs[0], pack_id="t21-pk-900", agreements=["Lowfield bulk sales agreement"] + packs[0]["agreements"][1:])
    assert any("t21-pk-900" in p for p in FV.relint_union(packs + [bad_pack], skins, free, attacks, wordings))
    again = dict(packs[0], pack_id="t21-pk-901")
    assert any("repeat" in p for p in FV.relint_union(packs + [again], skins, free, attacks, wordings))


# ------------------------------------------------------------------------------------------------ the full build
@pytest.fixture(scope="module")
def built():
    return FV.build()


def test_every_answer_file_of_every_round_is_valid(built):
    files = built["manifest"]["answer_files"]
    assert files["by_round"] == {"author-v1|ok": 21, "extract-v1|ok": 5, "redo2-a|ok": 6, "redo2-b|ok": 3}
    assert all(f["ok"] and not f["problems"] and f["sha256"] for f in files["files"])
    assert files["audit_failed_ignored"] == [] and FV.AUDIT_FAILED_IGNORED == ()


def test_v1_is_reproduced_and_untouched(built):
    man = built["manifest"]
    assert all(man["v1"]["reproduced_by_rebuild"].values()) and len(man["v1"]["reproduced_by_rebuild"]) == 8
    assert FV.v1_integrity() == [] and FP.check_targets() == []
    assert man["problems"]["v1_integrity"] == [] and man["problems"]["rebuild"] == []
    v1m = json.loads((FV.POOLS_V1 / "manifest.json").read_text(encoding="utf-8"))
    assert man["v1"]["pool_sha256"] == {n: i["sha256"] for n, i in v1m["pool_files"].items()}


def test_v1_pieces_are_carried_over_unchanged(built):
    f, v1 = built["files"], FV.load_v1()
    for name, key in (("packs.json", "packs"), ("wordings.json", "wordings")):
        got = {x.get("pack_id") or x["form_id"]: x for x in json.loads(f[name])}
        for x in v1[key]:
            assert got[x.get("pack_id") or x["form_id"]] == x
    for name, key in (("skins.json", "skins"), ("freeform.json", "freeform"), ("attacks.json", "attacks")):
        got = {d["skin_id"]: d for d in json.loads(f[name])}
        for s in v1[key]:
            assert got[s.skin_id] == json.loads(json.dumps(FV.asdict(s)))
    lex_v1, lex_v2 = v1["lexicon"], json.loads(f["lexicon.json"])
    by_id = {x["form_id"]: x for x in lex_v2["forms"]}
    for x in lex_v1["forms"]:
        assert by_id[x["form_id"]]["extractions"] == x["extractions"] and by_id[x["form_id"]]["status"] == x["status"]
    assert lex_v2["sems"] == lex_v1["sems"] and lex_v2["antonyms"] == lex_v1["antonyms"]


def test_verdict_ready_every_g0_minimum_met_and_no_target_lowered(built):
    assert built["verdict"] == "READY" and built["ready"] is True
    assert built["shortfalls"] == [] and built["problems"] == []
    t = FV.TARGET
    assert t["packs"] == {"total": 40, "train": 32, "held_out": 8} and t["attacks"] == 30
    assert t["skins_train_per_register"] == 12 and t["skins_held_per_register"] == 16
    assert t["freeform_per_train_register"] == 5
    assert t["wordings"] == {"yn_capped": 30, "ch_clause": 26, "yn_uncapped": 14, "yn_not_capped": 14, "yn_free_of": 14}
    assert all(x["admitted"] >= x["target"] and x["shortfall"] == 0 for x in built["tally"])
    c = built["counts"]
    assert c["packs"] == {"total": 40, "train": 32, "held_out": 8} and c["attacks"] == 30
    assert all(n == 12 for k, n in c["skins_by_register"].items() if k.endswith("|train"))
    assert all(n == 16 for k, n in c["skins_by_register"].items() if k.endswith("|held"))
    assert all(n == 5 for n in c["freeform_by_register"].values()) and len(c["freeform_by_register"]) == 8
    assert c["wordings_by_qform"] == t["wordings"] and c["lexicon_forms"] == 98


def test_glex_gate_and_kit_rules(built):
    g = built["manifest"]["gates"]
    assert g["G-LEX_used_forms"]["pass"] and g["G-LEX_used_forms"]["status_counts"] == {"admitted": 98}
    kit = g["G-LEX_kit_rules"]
    assert kit["strict_kinds_in_registry"] == [] and kit["required_reads"] == {"2": 98}
    assert kit["admitted_with_fewer_distinct_reads"] == [] and kit["admitted_not_all_agreeing"] == []
    assert kit["admitted_unit_failing"] == []
    new = kit["new_forms_distinct_reads"]
    assert len(new) == 5 and all(v == ["haiku-glex-question-redo2-r1", "haiku-glex-question-redo2-r2"] for v in new.values())
    assert g["G3-H"]["all_templates_pass"] and g["G3-H"]["items"] == 50 and g["G3-H"]["ok"] == 50
    assert g["plugin_smoke"]["ok"] and g["plugin_smoke"]["units"] == 15


def test_the_chosen_pieces_are_the_lowest_ranked_passers(built):
    sel = built["manifest"]["redo2"]["selection"]
    assert sum(len(v["chosen"]) for v in sel.values()) == 20 and all(v["short_after"] == 0 for v in sel.values())
    full = built["state"]["selection"]
    for cell, rec in full.items():
        passers = [c["iid"] for c in rec["candidates"] if c["status"] == "pass"]
        assert rec["chosen"] == passers[:rec["need"]], cell
        used = [c["iid"] for c in rec["candidates"] if c["used"]]
        assert used == rec["chosen"]
    # the two lint drops of the previous round are what moved the skin ranks
    drops = built["manifest"]["counts"]["redo2_lint_drops"]
    assert drops == {"packs": 0, "skins": 2, "freeform": 0, "wordings": 0}


def test_union_ids_do_not_collide_and_provenance_names_every_chosen_piece(built):
    f = built["files"]
    prov = json.loads(f["provenance.json"])
    assert sum(len(v) for v in prov["chosen"].values()) == 20
    for name, key in (("skins.json", "skin_id"), ("freeform.json", "skin_id"), ("attacks.json", "skin_id"),
                      ("packs.json", "pack_id")):
        ids = [d[key] for d in json.loads(f[name])]
        assert len(ids) == len(set(ids)), name
    assert len(json.loads(f["skins.json"])) == 128 and len(json.loads(f["freeform.json"])) == 40
    assert len(json.loads(f["wordings.json"])) == 98 and len(json.loads(f["packs.json"])) == 40


def test_manifest_hashes_and_quarantine(built):
    man, f = built["manifest"], built["files"]
    assert set(man["sha256"]) == set(f) - {"MANIFEST.json"}
    assert all(FV._sha(f[n]) == s for n, s in man["sha256"].items())
    q = json.loads(f["quarantine.json"])
    assert len(q) == man["quarantined"] == 22
    assert sorted({r["round"] for r in q}) == ["redo2", "v1"] and sum(r["round"] == "redo2" for r in q) == 2
    assert man["verdict"] == "READY" and man["transfer_dev_only"] is True and man["trained"] is False
    assert man["rows_generated"] is False and "pools_v2" in man["build"]


def test_pools_load_and_the_plugin_runs_on_them(built):
    texts = built["files"]
    pools = FV.pools_from_texts(texts)
    assert len(pools.packs) == 40 and len(pools.wordings) == 98 and pools.lexicon.gate()["pass"]
    ctx = FV.make_ctx(pools, quarantine=False)                                 # the frozen pools as written
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording") == 98
    ctx = FV.make_ctx(pools)                                                    # minus quarantine_i1.json (FIX-1)
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording") == 97
    assert not {"T21-WD-yn_not_capped-10e86065", "T21-SK-contract_ticket.006", "T21-MF-claims_log.003"} & set(ctx.skins)
    assert FV.smoke(pools, 2)["ok"]
    with pytest.raises(ValueError):                                            # a tampered file is refused
        FV.pools_from_texts(dict(texts, **{"wordings.json": texts["wordings.json"] + " "}))


def test_freeze_refuses_when_a_manifest_exists(built, tmp_path):
    (tmp_path / "MANIFEST.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        FV.freeze(built, tmp_path)
    assert [p.name for p in tmp_path.iterdir()] == ["MANIFEST.json"]            # nothing was written


def test_ignoring_the_three_newest_answers_leaves_exactly_the_waiting_cells_short():
    out = FV.build(ignore=THREE_NEWEST, smoke_seeds=0)
    assert out["verdict"] == "SHORT"
    assert sorted(out["shortfalls"]) == sorted([
        "freeform_F|dispute_email: 3/5 (short 2)", "freeform_F|legal_memo: 4/5 (short 1)",
        "freeform_F|counsel_chat: 4/5 (short 1)", "freeform_F|contract_faq: 4/5 (short 1)",
        "wordings|yn_capped: 28/30 (short 2)", "wordings|ch_clause: 24/26 (short 2)",
        "wordings|yn_free_of: 13/14 (short 1)"])
    ans = out["manifest"]["answer_files"]
    assert ans["by_round"]["redo2-b|rejected"] == 3 and ans["audit_failed_ignored"] == sorted(THREE_NEWEST)
    # packs and skins need no read: they still close
    assert out["counts"]["packs"] == {"total": 40, "train": 32, "held_out": 8}
    assert all(n == 12 for k, n in out["counts"]["skins_by_register"].items() if k.endswith("|train"))


def test_pools_v2_on_disk_equals_this_build(built):
    man = FV.POOLS_V2 / "MANIFEST.json"
    if not man.is_file():
        pytest.skip("pools_v2/ is not frozen yet")
    for name, text in built["files"].items():
        assert (FV.POOLS_V2 / name).read_text(encoding="utf-8") == text, name
    assert sorted(p.name for p in FV.POOLS_V2.iterdir()) == sorted(built["files"])
    pools = FV.load_pools()
    assert pools.manifest["verdict"] == "READY"
