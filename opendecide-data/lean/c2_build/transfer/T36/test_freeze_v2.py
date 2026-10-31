"""transfer/T36/test_freeze_v2.py: tests for freeze_v2.py (the T36 pool freeze-v2).

  contract     validate_answer: one test per way an answer file can break its contract; never edits a file
  votes        G-LEX with the kit rule (2 distinct extractors, 3 for precedence and window, one other pick rejects);
               G3-H round 2 votes (frozen prompt and schema, the read saw the candidate's text, first passing candidate)
  family data  (needs the family's files) all 33 answer files valid, v1 reproduced byte for byte and carried over,
               every G0 minimum met, G-LEX gate, G3-H on every document, the Mode F cap, every pool piece passes every
               program gate when rows are built from it, an excluded or corrupt G3-H file changes the verdict
Nothing is written under the family folder. Run (from lean/):
  ../.venv/bin/python -B -m pytest -q -p no:cacheprovider c2_build/transfer/T36/test_freeze_v2.py
"""
from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, pipeline  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T36 import extract as E  # noqa: E402
from transfer.T36 import freeze as F  # noqa: E402
from transfer.T36 import freeze_v2 as V  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402
from transfer.T36 import redo2 as R  # noqa: E402

HAVE_DATA = (V.POOLS_V1 / "MANIFEST.json").exists() and (V.HAIKU / "redo2" / "REDO2_INDEX.json").exists()
needs_data = pytest.mark.skipif(not HAVE_DATA, reason="needs the family's pools/ and haiku/ folders (after A38)")


# ------------------------------------------------------------------------------------------------ contract

def _task(kind="author_skin", qids=("q1", "q2"), keys=None, **kw):
    return V.Task("redo1", "T-000", kind, Path("unused.json"), tuple(qids), keys or V.KEYS[kind], **kw)


def _data(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def test_a_valid_text_file_passes_and_keeps_file_order():
    got, probs = V.validate_answer(_task(), _data([{"qid": "q2", "text": "b"}, {"qid": "q1", "text": "a"}]))
    assert probs == [] and list(got) == ["q2", "q1"] and got["q1"] == {"text": "a"}


@pytest.mark.parametrize("data, word", [
    (b"\xff\xfe", "UTF-8"),
    (b"[{]", "valid JSON"),
    (b'{"qid": "q1", "text": "a"}', "not a JSON array"),
    (b'[{"qid": "q1", "qid": "q2", "text": "a"}]', "duplicate key"),
    (b'\xef\xbb\xbf[{"qid": "q1", "text": "a"}]', "valid JSON"),                                   # BOM
    (_data([{"qid": "q1", "text": "a"}]), "unanswered"),
    (_data([{"qid": "q1", "text": "a"}, {"qid": "q2", "text": "b"}, {"qid": "q1", "text": "c"}]), "twice"),
    (_data([{"qid": "q1", "text": "a"}, {"qid": "q9", "text": "b"}]), "not an item"),
    (_data([{"qid": "q1", "text": "a", "note": "x"}, {"qid": "q2", "text": "b"}]), "keys"),
    (_data([{"qid": "q1"}, {"qid": "q2", "text": "b"}]), "keys"),
    (_data([{"qid": "q1", "text": "  "}, {"qid": "q2", "text": "b"}]), "non-empty"),
    (_data([{"qid": "q1", "text": 5}, {"qid": "q2", "text": "b"}]), "non-empty"),
    (_data(["q1", {"qid": "q2", "text": "b"}]), "not an object"),
])
def test_every_way_to_break_the_contract_is_rejected(data, word):
    got, probs = V.validate_answer(_task(), data)
    assert got is None and any(word in p for p in probs), probs


def test_redo2_texts_contract():
    t = _task("author_skin", keys=V.REDO2_KEYS, n_texts=3)
    ok = [{"qid": "q1", "texts": ["a", "b", "c"]}, {"qid": "q2", "texts": ["d", "e", "f"]}]
    assert V.validate_answer(t, _data(ok))[1] == []
    for bad, word in ((["a", "b"], "exactly 3"), (["a", "a", "c"], "different"), (["a", "b", ""], "exactly 3"),
                      ("abc", "exactly 3")):
        got, probs = V.validate_answer(t, _data([{"qid": "q1", "texts": bad}, ok[1]]))
        assert got is None and any(word in p for p in probs), (bad, probs)


def test_lexicon_meaning_must_be_copied_exactly_from_the_choices():
    t = _task("extract_lex", choices={"q1": ("asks A", "asks B"), "q2": ("asks A", "asks B")})
    assert V.validate_answer(t, _data([{"qid": "q1", "meaning": "asks A"}, {"qid": "q2", "meaning": "asks B"}]))[1] == []
    got, probs = V.validate_answer(t, _data([{"qid": "q1", "meaning": "Asks A"}, {"qid": "q2", "meaning": "asks B"}]))
    assert got is None and any("copied exactly" in p for p in probs)


def test_g3h_and_pack_contracts():
    t = _task("extract_g3h")
    ok = [{"qid": "q1", "project": "Harbor Lantern", "person": "NONE"}, {"qid": "q2", "project": "X Y", "person": "A B"}]
    assert V.validate_answer(t, _data(ok))[1] == []
    assert V.validate_answer(t, _data([{**ok[0], "person": ""}, ok[1]]))[0] is None
    assert V.validate_answer(t, _data([{**ok[0], "person": ["A"]}, ok[1]]))[0] is None
    tp = _task("author_pack")
    pk = {"project": "Dim Orrery Map", "packages": ["aa-bb", "cc-dd", "ee-ff"], "people": ["Ilse Varga", "Tomasz Brenner"]}
    assert V.validate_answer(tp, _data([{"qid": "q1", **pk}, {"qid": "q2", **pk}]))[1] == []
    for key, val in (("packages", ["aa-bb", "cc-dd"]), ("people", ["Ilse Varga"]), ("people", "Ilse Varga")):
        assert V.validate_answer(tp, _data([{"qid": "q1", **pk, key: val}, {"qid": "q2", **pk}]))[0] is None


def test_validate_all_reports_every_status_and_never_edits(tmp_path):
    good, bad = tmp_path / "good.json", tmp_path / "bad.json"
    good.write_text(json.dumps([{"qid": "q1", "text": "a"}, {"qid": "q2", "text": "b"}]))
    bad.write_text('[{"qid": "q1", "text": "a"}]')
    mk = lambda name, f: V.Task("redo1", name, "author_skin", f, ("q1", "q2"), V.KEYS["author_skin"])   # noqa: E731
    tasks = [mk("good", good), mk("bad", bad), mk("gone", tmp_path / "gone.json"), mk("audit", good)]
    before = {p: p.read_bytes() for p in (good, bad)}
    res = V.validate_all(tasks, frozenset({"redo1:audit"}))
    assert {k: r.status for k, r in res.items()} == {"redo1:good": "valid", "redo1:bad": "invalid",
                                                     "redo1:gone": "missing", "redo1:audit": "excluded"}
    assert res["redo1:bad"].answers is None and res["redo1:audit"].answers is None       # nothing of it is used
    assert res["redo1:good"].answers == {"q1": {"text": "a"}, "q2": {"text": "b"}}
    assert before == {p: p.read_bytes() for p in (good, bad)}


def test_resolve_excluded():
    a = V.Task("redo1", "T-1", "author_skin", Path("a"), ("q",), V.KEYS["author_skin"])
    b = V.Task("redo2", "T-1", "author_skin", Path("b"), ("q",), V.REDO2_KEYS, n_texts=2)
    c = V.Task("redo2-g3h", "G-1", "extract_g3h", Path("c"), ("q",), V.KEYS["extract_g3h"])
    assert V.resolve_excluded([a, b, c], ["G-1", "redo1:T-1"]) == frozenset({"redo2-g3h:G-1", "redo1:T-1"})
    for bad in ("T-1", "nope"):
        with pytest.raises(SystemExit):
            V.resolve_excluded([a, b, c], [bad])
    assert V.resolve_excluded([a, b, c], []) == frozenset()


# ------------------------------------------------------------------------------------------------ G-LEX votes

def _reads(reg, n, answer, start=0):
    """n independent reads (each its own batch, so its own task ids) recorded with freeze.record_glex."""
    for i in range(start, start + n):
        b = chunker.make_batch("extract_lex", "TOY", reg.lexicon_items(), seed=f"read-{i}", prompt="pick the meaning")
        raw = {c["task_id"]: [{"qid": it["qid"], "meaning": answer(reg, b.key[it["qid"]], i)} for it in c["items"]]
               for c in b.chunks}
        got, _ = chunker.load_answers(b, raw)
        F.record_glex(reg, b, got)


def _toy():
    reg = LX.LexiconRegistry("TOY")
    reg.declare("q.toy.a", "question", "asks A")
    reg.declare("q.toy.b", "question", "asks B")
    reg.declare("prec.P1", "precedence", "deny rules beat allow rules")
    reg.declare("prec.P2", "precedence", "allow rules beat deny rules")
    q = reg.add("Is {PKG} fine?", "q.toy.a", slots={"PKG": "id"})
    p = reg.add("deny rules beat allow rules", "prec.P1")
    reg.unit_test_all()
    assert q.unit_ok and p.unit_ok, (q.unit_problems, p.unit_problems)
    return reg, q.form_id, p.form_id


def test_glex_needs_two_distinct_extractors_and_three_for_precedence():
    own = lambda reg, fid, i: reg.sems[reg.forms[fid].sem_id].meaning                    # noqa: E731
    reg, q, p = _toy()
    _reads(reg, 1, own)
    assert (reg.status(q), reg.status(p)) == ("pending", "pending")
    _reads(reg, 1, own, start=1)                                                          # a second read: ids differ
    assert (reg.status(q), reg.status(p)) == ("admitted", "pending")                     # 2/2 question, 2 of 3 precedence
    assert (reg.forms[p].required, reg.forms[q].required) == (3, 2)
    _reads(reg, 1, own, start=2)
    assert reg.status(p) == "admitted"
    assert reg.gate([q, p])["pass"]


def test_glex_one_other_pick_rejects_for_good():
    reg, q, p = _toy()
    other = lambda reg_, fid, i: "asks B" if (i == 1 and fid == q) else reg_.sems[reg_.forms[fid].sem_id].meaning   # noqa: E731
    _reads(reg, 3, other)
    assert reg.status(q) == "rejected" and reg.status(p) == "admitted"                    # no re-vote
    assert not reg.gate([q])["pass"]
    reg2, q2, _p2 = _toy()
    _reads(reg2, 2, lambda r, fid, i: "a meaning that is not on the list")               # not listed: counts as another pick
    assert reg2.status(q2) == "rejected"


# ------------------------------------------------------------------------------------------------ G3-H round 2 votes

def _g3h_tree(tmp_path, monkeypatch, *, answers, expected_person="Dana Okafor", piece_text="TEXT0", read_text=None):
    """A one-task G3-H read on disk: key, chunk (frozen prompt and schema), answers, expected values."""
    root = tmp_path / "extract"
    for d in ("key", "chunks", "answers", "pool"):
        (root / d).mkdir(parents=True)
    fields = E.g3h_fields()
    schema = g3h.extraction_item("", fields)["schema"]
    gid = "g3h2|t36|free|ci_log|000|c0"
    (root / "key" / "B1.json").write_text(json.dumps({"batch_id": "B1", "key": {"qg1": gid}}))
    (root / "chunks" / "G-000.json").write_text(json.dumps({
        "task_id": "G-000", "kind": "extract_g3h", "prompt_sha": V._sha(E.G3H_PROMPT),
        "instructions": E.G3H_PROMPT.split("\n"),
        "items": [{"qid": "qg1", "text": read_text or piece_text, "schema": schema}]}))
    (root / "answers" / "G-000.json").write_text(json.dumps(answers))
    (root / "pool" / "g3h_expected.jsonl").write_text(json.dumps({
        "g3h_id": gid, "text_sha256": V._sha(piece_text), "expected": {"project": "Harbor Lantern", "person": expected_person}}) + "\n")
    monkeypatch.setattr(R, "G3H_ROOT", root)
    task = V.Task("redo2-g3h", "G-000", "extract_g3h", root / "answers" / "G-000.json", ("qg1",),
                  V.KEYS["extract_g3h"], meta={"batch_id": "B1"})
    row = {"task": "A-000", "pool": "freeform", "qid": "qa", "iid": "t36|free|ci_log|000", "register": "ci_log",
           "held_out": False, "facts": {"PERSON": "Dana Okafor", "PROJECT": "Harbor Lantern"},
           "candidates": [{"j": 0, "ok": True, "reasons": [], "piece": SimpleNamespace(text=piece_text), "text": piece_text},
                          {"j": 1, "ok": False, "reasons": ["lint"], "piece": None, "text": "x"}]}
    return task, row, fields


def _votes(tmp_path, monkeypatch, status="valid", **kw):
    task, row, fields = _g3h_tree(tmp_path, monkeypatch, **kw)
    results = V.validate_all([task], frozenset({task.label}) if status == "excluded" else frozenset())
    return V.redo2_g3h([row], results, fields), row


OK_ANSWER = [{"qid": "qg1", "project": "Harbor Lantern", "person": "Dana Okafor"}]


def test_g3h_round2_vote_passes_on_an_exact_match(tmp_path, monkeypatch):
    votes, row = _votes(tmp_path, monkeypatch, answers=OK_ANSWER)
    assert [v["ok"] for v in votes["votes"]] == [True] and len(votes["votes"]) == 1       # the lint-failed candidate has no vote
    kept, rows = V.select_documents([row], votes)
    assert len(kept) == 1 and rows[0]["kept_j"] == 0


@pytest.mark.parametrize("answers, why", [
    ([{"qid": "qg1", "project": "Harbor Lantern", "person": "NONE"}], "person"),
    ([{"qid": "qg1", "project": "Harbor Lantern", "person": "dana okafor"}], "person"),
    ([{"qid": "qg1", "project": "Harbor Lanter", "person": "Dana Okafor"}], "project"),
])
def test_g3h_round2_vote_fails_on_any_difference(tmp_path, monkeypatch, answers, why):
    votes, row = _votes(tmp_path, monkeypatch, answers=answers)
    v = votes["votes"][0]
    assert not v["ok"] and why in v["diffs"][0]
    assert V.select_documents([row], votes)[0] == []


def test_g3h_round2_unanswered_text_mismatch_and_drift(tmp_path, monkeypatch):
    votes, _ = _votes(tmp_path, monkeypatch, answers=OK_ANSWER, status="excluded")          # the audit failed
    assert [v["diffs"] for v in votes["votes"]] == [["no answer"]]
    votes, _ = _votes(tmp_path / "b", monkeypatch, answers=OK_ANSWER, read_text="another text")  # read saw other text
    assert not votes["votes"][0]["ok"] and "another text" in votes["votes"][0]["diffs"][0]
    (tmp_path / "c").mkdir()
    with pytest.raises(V.Blocked):                                                          # expected value drifted
        _votes(tmp_path / "c", monkeypatch, answers=OK_ANSWER, expected_person="Someone Else")


def test_g3h_round2_refuses_a_read_that_is_not_the_frozen_prompt(tmp_path, monkeypatch):
    task, row, fields = _g3h_tree(tmp_path, monkeypatch, answers=OK_ANSWER)
    chunk_file = tmp_path / "extract" / "chunks" / "G-000.json"
    chunk = json.loads(chunk_file.read_text())
    chunk["instructions"] = chunk["instructions"] + ["Also say who is nicest."]
    chunk_file.write_text(json.dumps(chunk))
    with pytest.raises(V.Blocked):
        V.redo2_g3h([row], V.validate_all([task]), fields)


def test_first_passing_candidate_wins_and_the_rest_are_discarded():
    mk = lambda j, ok, g: {"j": j, "ok": ok, "g3h_ok": g, "piece": f"piece{j}"}                  # noqa: E731
    base = {"task": "t", "qid": "q", "iid": "i", "register": "r", "held_out": False}
    rows = [{**base, "candidates": [mk(0, True, False), mk(1, True, True), mk(2, True, True)]},    # 0 fails G3-H
            {**base, "candidates": [mk(0, False, None), mk(1, True, True)]},                      # 0 fails lint
            {**base, "candidates": [mk(0, True, True), mk(1, True, True)]},                       # first wins
            {**base, "candidates": [mk(0, True, False), mk(1, True, None)]}]                      # none passes
    kept, out = V.select_documents(rows, {"report": {"quarantined": []}})
    assert [r["kept_j"] for r in out] == [1, 1, 0, None] and kept == ["piece1", "piece1", "piece0"]
    kept, out = V.select_documents(rows[:1], {"report": {"quarantined": ["g3h2|i|c1", "g3h2|i|c2"]}})
    assert kept == [] and out[0]["kept_j"] is None


def test_the_mode_f_cap_and_the_maintainer_diagnostic():
    docs = [dataclasses.replace(_doc(i), held_out=(i >= 8)) for i in range(11)]
    kept, quar = V.finalize_documents(docs, t_train=6, t_held=3)                            # caps 2 and 1
    assert sum(1 for d in kept if not d.held_out) == 2 and sum(1 for d in kept if d.held_out) == 1
    assert len(quar) == 11 - 3 and all(q["reason"] == "Mode F cap" for q in quar)
    kept2, quar2 = V.finalize_documents(docs, t_train=30, t_held=30)
    assert len(kept2) == 11 and quar2 == []
    assert V.direct_maintainer_statement(_doc(0, "Dana Okafor maintains Harbor Lantern.", "Dana Okafor"))
    assert V.direct_maintainer_statement(_doc(0, "project=X maintainer=Dana Okafor", "Dana Okafor"))
    assert not V.direct_maintainer_statement(_doc(0, "owner=Dana Okafor " + "x" * 100 + " owner-role=maintainer",
                                                  "Dana Okafor"))


def _doc(i, text=None, person="Dana Okafor"):
    t = text or f"Document {i} says that Harbor Lantern is looked at and {person} maintains it."
    return F.rekey(make_skin(f"d{i}", "T36", t, {"PERSON": "name", "PROJECT": "name"}, register="ci_log",
                             author_mode="F", brief={"PERSON": person, "PROJECT": "Harbor Lantern"}))


# ------------------------------------------------------------------------------------------------ the family's data

@pytest.fixture(scope="module")
def res():
    return V.assemble()


@needs_data
def test_every_answer_file_of_every_round_is_valid(res):
    v = res["validation"]
    assert v["files_total"] == 33 and v["files_valid"] == 33 and v["files_not_valid"] == []
    assert v["stray_files_not_used"] == [] and v["excluded_tasks"] == []
    assert v["summary"] == {"redo1/valid": 5, "redo2-g3h/valid": 2, "redo2/valid": 5, "v1-author/valid": 14,
                            "v1-extract/valid": 7}


@needs_data
def test_v1_is_reproduced_byte_for_byte_and_carried_over(res):
    integrity = res["manifest"]["v1_integrity"]
    assert integrity["ok"] and all(integrity["reproduced_by_this_builder_without_round2_documents"].values())
    assert set(integrity["reproduced_by_this_builder_without_round2_documents"]) == set(V.V1_POOL_FILES)
    assert all(integrity["every_v1_piece_carried_over"].values())
    v1 = json.loads((V.POOLS_V1 / "MANIFEST.json").read_text())["sha256"]
    for name, sha in v1.items():
        assert V._sha((V.POOLS_V1 / name).read_bytes()) == sha                               # v1 on disk is untouched
    old_docs = {d["skin_id"] for d in json.loads((V.POOLS_V1 / "documents.json").read_text())}
    assert old_docs <= {d.skin_id for d in res["pieces"]["docs"]}


@needs_data
def test_every_g0_minimum_is_met_and_the_verdict_is_ready(res):
    c = res["counts"]
    assert res["blocking"] == [] and res["shortfalls"] == [] and res["ready"] is True
    assert res["status"].startswith("READY")
    assert c["packs_train"] >= V.TARGETS["packs_train"] and c["packs_held"] >= V.TARGETS["packs_held"]
    for pool in ("skin", "skin_heldout", "freeform", "freeform_heldout"):
        for reg, want in V.TARGETS[pool].items():
            assert c[pool].get(reg, 0) >= want, (pool, reg, c[pool])
    assert c["attack"] >= V.TARGETS["attack"]
    for qf, want in V.TARGETS["wording"].items():
        assert c["wording"].get(qf, 0) >= want, (qf, c["wording"])
    assert V.TARGETS == F.TARGETS and V.G3H_BAR == g3h.PASS_RATE == 0.98                      # nothing lowered


@needs_data
def test_glex_gate_passes_on_every_pool_form_with_the_kit_rule(res):
    g = res["manifest"]["glex"]
    assert g["gate_on_pool_forms"]["pass"] and g["gate_on_all_forms"]["pass"]
    assert g["admitted"] == g["forms"] == 118 and g["strict_kind_forms"] == 0
    assert g["required_votes"] == {"question": 2}
    lex = json.loads(res["files"]["lexicon.json"])
    for f in lex["forms"]:
        assert f["status"] == "admitted" and len({e[0] for e in f["extractions"]}) >= 2
        assert all(e[1] == f["sem_id"] for e in f["extractions"])


@needs_data
def test_every_frozen_document_passed_g3h_and_respects_the_cap(res):
    votes = json.loads(res["files"]["g3h_votes.json"])
    ok = {v["id"] for v in votes["redo2"] if v["ok"]} | {v["id"] for v in votes["round1"] if v["ok"]}
    docs = res["pieces"]["docs"]
    kept = [v for v in votes["redo2"] if any(r["task"] == v["task_id"] and r["qid"] == v["qid"] and r["kept_j"] == v["j"]
                                             for r in votes["redo2_items"])]
    assert len(docs) == 42 and len(kept) == 41 and all(v["ok"] for v in kept) and len(votes["redo2"]) == 82
    assert {v["id"] for v in kept} <= ok
    skins = res["pieces"]["skins"]
    for held in (False, True):
        n_t = sum(1 for s in skins if s.held_out == held)
        n_f = sum(1 for d in docs if d.held_out == held)
        assert n_f <= n_t // 3                                                                # 1 document per 3 Mode T skins
        assert n_f / (n_f + n_t) <= 0.25
    man = res["manifest"]["g3h"]
    assert man["round1"] == {"documents": 34, "pass": 1, "fail": 33, "failing_fields": {"person": 33}}
    assert man["redo2"]["templates_quarantined"] == [] and man["documents_frozen"] == 42
    assert (man["cross_check_with_redo2_g3h_check"] or {}).get("same_items_and_candidates") is True


@needs_data
def test_texts_and_ids_are_unique_and_the_files_match_their_manifest(res):
    pieces = res["pieces"]["skins"] + res["pieces"]["attacks"] + res["pieces"]["docs"]
    assert len({p.skin_id for p in pieces}) == len(pieces) == 282
    assert len({" ".join(p.text.casefold().split()) for p in pieces}) == len(pieces)
    man = res["manifest"]
    for name, sha in man["sha256"].items():
        assert V._sha(res["files"][name]) == sha
    assert set(man["sha256"]) == set(res["files"]) - {"MANIFEST.json"}


@needs_data
def test_pools_build_rows_through_every_program_gate(res):
    """The v2 pools are usable: units built from them (and from each document) pass G2, G3, G4, G-SL, G-LEX, G-TW."""
    ctx, packs = V.pools_from(lambda name: res["files"][name])
    plugin = P.T36Plugin(lexicon=ctx.lexicon, packs=packs)
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording") == 118
    bad = []
    for seed in range(10):
        for smp in plugin.SAMPLERS:
            u = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            if not u.ok:
                bad.append((seed, smp, u.problems[:2]))
    docs = sorted((s for s in ctx.skins.values() if s.author_mode == "F"), key=lambda s: s.skin_id)
    assert len(docs) == 42
    for i, d in enumerate(docs):
        u = pipeline.build_unit(plugin, plugin.sample(i, "S5" if d.held_out else "S1"), ctx, run_g15=False, skin=d)
        if not u.ok:
            bad.append((d.skin_id, u.problems[:2]))
    assert not bad, bad[:3]


@needs_data
def test_excluding_the_g3h_answers_leaves_exactly_the_mode_f_shortfalls():
    names = ["redo2-g3h:T36-extract_g3h-6e8bc463-000", "redo2-g3h:T36-extract_g3h-6e8bc463-001"]
    out = V.assemble(names)
    assert out["ready"] is False and out["status"].startswith("SHORT")
    assert {s["item"].split("/")[0] for s in out["shortfalls"]} == {"freeform", "freeform_heldout"}
    assert sum(s["shortfall"] for s in out["shortfalls"]) == 41
    assert out["manifest"]["g3h"]["redo2"]["answer_files_used"] == []
    assert out["manifest"]["answer_files"]["excluded_tasks"] == names


@needs_data
def test_a_corrupt_g3h_answer_is_rejected_whole_and_not_edited(tmp_path):
    tasks = V.discover_tasks()
    t = next(x for x in tasks if x.round == "redo2-g3h")
    original = t.answer_file.read_bytes()
    broken = tmp_path / "broken.json"
    data = json.loads(original)
    data[0]["extra"] = "x"
    broken.write_text(json.dumps(data))
    r = V.validate_all([dataclasses.replace(t, answer_file=broken)])[t.label]
    assert r.status == "invalid" and r.answers is None and any("keys" in p for p in r.problems)
    assert t.answer_file.read_bytes() == original and broken.read_text() == json.dumps(data)


@needs_data
def test_writing_is_guarded(res, monkeypatch, tmp_path):
    with pytest.raises(SystemExit):                                                          # a blocking problem writes nothing
        V.write_pools({**res, "blocking": ["x"]}, tmp_path / "p")
    assert not (tmp_path / "p").exists()
    root = tmp_path / "exists"
    root.mkdir()
    (root / "MANIFEST.json").write_text("other content")
    with pytest.raises(SystemExit):                                                          # written once
        V.write_pools(res, root)
    assert (root / "MANIFEST.json").read_text() == "other content"


@pytest.mark.skipif(not (V.POOLS_V2 / "MANIFEST.json").exists(), reason="pools_v2 not written yet")
def test_the_written_pools_equal_the_verdict_and_load(res):
    for name, text in res["files"].items():
        assert (V.POOLS_V2 / name).read_text(encoding="utf-8") == text, name
    out = V.verify_pools_v2()
    assert out["ok"] and out["sha_mismatches"] == [] and out["v1_unchanged"] and out["v1_files_match_v1_manifest"]
    plugin, ctx = V.make_plugin()
    assert len(plugin.packs) == 46 and len(ctx.skins) == 400
