"""families/T32/test_freeze_v2.py: freeze_v2 (the T32 pools_v2 re-freeze), in memory.

Nothing here writes into the family folder: the freeze runs in memory, and the pool files are written to pytest's tmp
folder through plain writers (the kit's guarded writers are tested to refuse before A38). The real Haiku answer files
are read, never changed.

Checks: the answer-file contract validator (file-level and item-level rejects, off-list reads, never an edit); the
contract is derivable for every item of every real chunk; every real answer file of every round passes; the validated
rebuild equals the family loader; a rejected / ignored answer file never becomes a vote and a missing authoring answer
blocks the freeze; G3-H (unanswered fails, 98% per register); the frozen result: every G0 minimum, the G-LEX gate over
the used forms, v1 byte identity for the files v2 shares with v1, the redo2 Mode F intros merged, round-1 quarantines
standing; the writer refuses before A38; the pools load back (sha256 verified, tamper detected) and rebuild into a
KitCtx and a plugin.
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T32/test_freeze_v2.py
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

from c2_kit import paths  # noqa: E402
from families.T32 import authoring as A  # noqa: E402
from families.T32 import extract as X  # noqa: E402
from families.T32 import freeze_v2 as F  # noqa: E402
from families.T32 import plugin as P  # noqa: E402

HERE = Path(__file__).resolve().parent
TOPICS = ["the house move", "the office move"]


# ------------------------------------------------------------------------------------------------ synthetic tasks
def _list_def():
    items = {
        "qA": {"qid": "qA", "brief": 'Write 3 different intros. Answer field: "intros" (a list of 3 strings).'},
        "qB": {"qid": "qB", "brief": 'Write 2 different intros. Answer field: "intros" (a list of 2 strings).'}}
    return F.ChunkDef("T-free-000", "author_freeform", items)


def _skin_def():
    return F.ChunkDef("T-skin-000", "author_skin", {
        "qA": {"qid": "qA", "brief": 'Write 2 different notes. Answer field: "lines".'},
        "qB": {"qid": "qB", "brief": 'Write 2 different notes. Answer field: "lines".'}})


def _pack_def():
    return F.ChunkDef("T-pack-000", "author_pack", {
        "qA": {"qid": "qA", "brief": 'Write one pack. Answer field: "pack" (one JSON object with exactly the lists '
                                      'tasks, events and topics).'}})


def _lex_def():
    return F.ChunkDef("T-lex-000", "extract_lex", {
        "qA": {"qid": "qA", "text": "x", "choices": ["m1", "m2", "none of these"]},
        "qB": {"qid": "qB", "text": "y", "choices": ["m1", "m2", "none of these"]}})


def _g3h_def():
    return F.ChunkDef("T-g3h-000", "extract_g3h", {
        "qA": {"qid": "qA", "text": "t", "schema": [{"field": "topic", "choices": TOPICS}, {"field": "owner"}]}})


def _b(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


GOOD_LIST = [{"qid": "qA", "intros": ["a", "b", "c"]}, {"qid": "qB", "intros": ["x", "y"]}]


def test_valid_file_accepted_as_written():
    rep = F.validate_answer_bytes(_b(GOOD_LIST), _list_def())
    assert rep["ok"] and rep["n_valid_items"] == 2 and not rep["item_problems"] and rep["in_order"]
    assert rep["items"] == GOOD_LIST                     # the objects as written, untouched


def test_out_of_order_file_is_valid_but_noted():
    rep = F.validate_answer_bytes(_b(GOOD_LIST[::-1]), _list_def())
    assert rep["ok"] and rep["in_order"] is False


@pytest.mark.parametrize("data, why", [
    (b"\xff\xfe[]", "not UTF-8"),
    ("﻿[]".encode(), "byte-order mark"),
    (b"[{]", "not valid JSON"),
    (b'[{"qid": "qA", "qid": "qB"}]', "duplicate key"),
    (b'[{"qid": "qA", "intros": NaN}]', "NaN"),
    (b'{"qid": "qA"}', "not a JSON array"),
])
def test_file_level_rejects_before_any_item(data, why):
    rep = F.validate_answer_bytes(data, _list_def())
    assert not rep["ok"] and rep["items"] == [] and why in rep["file_problems"][0]


@pytest.mark.parametrize("mut, why", [
    (lambda a: a + [3], "is not an object"),
    (lambda a: a + [dict(a[0])], "used twice"),
    (lambda a: a[:1], "not answered"),
    (lambda a: a + [{"qid": "qZ", "intros": ["a", "b", "c"]}], "unknown qid"),
    (lambda a: [dict(a[0], extra="x"), a[1]], "differ from the contract"),
    (lambda a: [{"intros": ["a", "b", "c"]}, a[1]], "qid is not a string"),
    (lambda a: [{"qid": "qA", "forms": ["a", "b", "c"]}, a[1]], "differ from the contract"),   # wrong field
])
def test_file_level_rejects_on_structure(mut, why):
    rep = F.validate_answer_bytes(_b(mut(json.loads(json.dumps(GOOD_LIST)))), _list_def())
    assert not rep["ok"] and rep["items"] == []
    assert any(why in p for p in rep["file_problems"]), rep["file_problems"]


@pytest.mark.parametrize("bad", [["a", "b"], ["a", "b", "c", "d"], ["a", "", "c"], ["a", "  ", "c"], ["a", 1, "c"],
                                 "abc", None])
def test_item_level_reject_keeps_the_rest(bad):
    ans = [{"qid": "qA", "intros": bad}, GOOD_LIST[1]]
    rep = F.validate_answer_bytes(_b(ans), _list_def())
    assert rep["ok"] and rep["n_valid_items"] == 1 and len(rep["item_problems"]) == 1
    assert rep["items"] == [GOOD_LIST[1]] and rep["item_problems"][0].startswith("qA:")


def test_skin_lines_field_and_count_from_write_n():
    good = [{"qid": "qA", "lines": ["a", "b"]}, {"qid": "qB", "lines": ["c", "d"]}]
    assert F.validate_answer_bytes(_b(good), _skin_def())["n_valid_items"] == 2
    rep = F.validate_answer_bytes(_b([good[0], {"qid": "qB", "lines": ["c"]}]), _skin_def())
    assert rep["ok"] and rep["n_valid_items"] == 1 and "exactly 2" in rep["item_problems"][0]
    rep = F.validate_answer_bytes(_b([good[0], {"qid": "qB", "skins": ["c", "d"]}]), _skin_def())
    assert not rep["ok"]                                       # "skins" is not the field this item names


def test_pack_contract():
    pk = {"tasks": ["fetch a"], "events": ["the visit"], "topics": ["the move"]}
    assert F.validate_answer_bytes(_b([{"qid": "qA", "pack": pk}]), _pack_def())["n_valid_items"] == 1
    for bad in ({"tasks": ["a"], "events": ["b"]}, {**pk, "extra": []}, {**pk, "tasks": "a"}, {**pk, "tasks": [""]},
                [], "x"):
        rep = F.validate_answer_bytes(_b([{"qid": "qA", "pack": bad}]), _pack_def())
        assert rep["ok"] and rep["n_valid_items"] == 0 and rep["item_problems"], bad


def test_lex_meaning_off_list_is_a_non_matching_read_not_a_missing_one():
    rep = F.validate_answer_bytes(_b([{"qid": "qA", "meaning": "m1"}, {"qid": "qB", "meaning": "something else"}]),
                                  _lex_def())
    assert rep["ok"] and rep["n_valid_items"] == 2 and rep["off_list"] == ["qB"]        # kept: H41 rejects the form
    rep = F.validate_answer_bytes(_b([{"qid": "qA", "meaning": ""}, {"qid": "qB", "meaning": "none of these"}]),
                                  _lex_def())
    assert rep["n_valid_items"] == 1 and rep["off_list"] == [] and rep["item_problems"][0].startswith("qA:")
    rep = F.validate_answer_bytes(_b([{"qid": "qA", "meaning": 3}, {"qid": "qB", "meaning": "m2"}]), _lex_def())
    assert rep["item_problems"] and rep["n_valid_items"] == 1


def test_g3h_contract():
    ok = F.validate_answer_bytes(_b([{"qid": "qA", "topic": TOPICS[0], "owner": "Priya"}]), _g3h_def())
    assert ok["n_valid_items"] == 1 and ok["off_list"] == []
    none = F.validate_answer_bytes(_b([{"qid": "qA", "topic": "NONE", "owner": "NONE"}]), _g3h_def())
    assert none["n_valid_items"] == 1 and none["off_list"] == []
    off = F.validate_answer_bytes(_b([{"qid": "qA", "topic": "the moon", "owner": "Priya"}]), _g3h_def())
    assert off["n_valid_items"] == 1 and off["off_list"] == ["qA"]              # a failing read (g3h.compare), not unread
    for bad in ({"qid": "qA", "topic": TOPICS[0], "owner": ""}, {"qid": "qA", "topic": None, "owner": "Priya"},
                {"qid": "qA", "topic": TOPICS[0], "owner": ["Priya"]}):
        rep = F.validate_answer_bytes(_b([bad]), _g3h_def())
        assert rep["ok"] and rep["n_valid_items"] == 0 and rep["item_problems"]
    assert not F.validate_answer_bytes(_b([{"qid": "qA", "topic": TOPICS[0]}]), _g3h_def())["ok"]    # missing key


def test_contract_not_derivable_rejects_the_file():
    d = F.ChunkDef("T-x", "author_freeform", {"qA": {"qid": "qA", "brief": "no field named here"}})
    rep = F.validate_answer_bytes(_b([{"qid": "qA", "intros": ["a"]}]), d)
    assert not rep["ok"] and "contract not derivable" in rep["file_problems"][0]
    d = F.ChunkDef("T-x", "author_freeform", {"qA": {"qid": "qA", "brief": 'Answer field: "forms" (a list of 2 strings)'}})
    assert not F.validate_answer_bytes(_b([{"qid": "qA", "forms": ["a", "b"]}]), d)["ok"]   # wrong field for the kind


def test_validation_never_edits_the_input():
    data = _b(GOOD_LIST)
    before = bytes(data)
    F.validate_answer_bytes(data, _list_def())
    assert data == before


# ------------------------------------------------------------------------------------------------ the real answers
@pytest.fixture(scope="module")
def validation():
    return F.validate_all()


def test_contract_is_derivable_for_every_real_item():
    n = 0
    for name, root in F.ROUNDS.items():
        defs = F.defs_from_chunks(root / "chunks")
        assert defs, name
        for cd in defs.values():
            for it in cd.items.values():
                assert F.item_contract(cd.kind, it) is not None, (name, cd.task_id, it["qid"])
                n += 1
    expected = sum(json.loads(m.read_text(encoding="utf-8"))["n_items"]
                   for root in F.ROUNDS.values() for m in (root / "manifest").glob("*.json"))
    assert n == expected == 1403


def test_every_real_answer_file_of_every_round_passes(validation):
    sizes = {"author": 28, "extract": 23, "redo2_author": 2, "redo2_extract": 2}
    for name, r in validation["rounds"].items():
        assert r["tasks"] == sizes[name] and len(r["files"]) == sizes[name], name
        assert not r["rejected"] and not r["missing"] and not r["integrity_problems"] and not r["index_problems"], name
        assert r["item_rejects"] == 0 and r["off_list_items"] == 0, name
        assert r["stray"] in ([], ["README.txt"]), name
        assert all(f["path_matches_task"] and f["ok"] and not f["ignored"] for f in r["files"].values()), name
    assert F.validation_ok(validation)
    assert validation["ambiguity"]["ok"] and validation["ambiguity"]["n_points"] == 45
    assert "no haiku/redo folder" in validation["redo"]


def test_accepted_answers_are_the_objects_in_the_files(validation):
    rep = validation["rounds"]["redo2_extract"]
    acc = F.accepted(rep)
    assert set(acc) == set(rep["files"])
    for tid, items in acc.items():
        on_disk = json.loads((F.R.EXTRACT_ROOT / "answers" / f"{tid}.json").read_text(encoding="utf-8"))
        assert items == on_disk


def test_ignored_task_is_rejected_whole_and_never_a_vote():
    tid = "T32-extract_g3h-9a1661ac-000"
    rep = F.validate_round("redo2_extract", F.R.EXTRACT_ROOT, ignore=(tid,))
    assert rep["rejected"] == [tid] and rep["files"][tid]["ignored"] and not rep["files"][tid]["ok"]
    assert tid not in F.accepted(rep) and "T32-extract_g3h-9a1661ac-001" in F.accepted(rep)
    assert "ignored" in rep["files"][tid]["file_problems"][0]


# ------------------------------------------------------------------------------------------------ G3-H
def _piece(i, reg="family_chat"):
    return {"iid": f"r2|{reg}|0|{i}", "register": reg, "facts": {"OWNER": "Priya", "TOPIC": "the house move"}}


GOOD_READ = {"topic": "the house move", "owner": "Priya"}


def test_g3h_unanswered_intro_fails():
    rows, rep = F.g3h_results([_piece(0), _piece(1)], {"r2|family_chat|0|0": GOOD_READ})
    assert [r["ok"] for r in rows] == [True, False] and rows[1]["diffs"] == ["unanswered"]
    assert rep["templates"]["family_chat"]["rate"] == 0.5 and rep["quarantined"] == ["family_chat"]


def test_g3h_bar_is_98_percent_per_register():
    ps = [_piece(i) for i in range(50)] + [_piece(i, "flatmates") for i in range(9)]
    got = {p["iid"]: GOOD_READ for p in ps}
    rows, rep = F.g3h_results(ps, got)
    assert rep["quarantined"] == [] and all(r["ok"] for r in rows)
    got[ps[0]["iid"]] = {"topic": "the office move", "owner": "Priya"}            # 49/50 = 98%: still passes
    got[ps[50]["iid"]] = {"topic": "the house move", "owner": "NONE"}              # 8/9 = 88.9%: quarantined
    rows, rep = F.g3h_results(ps, got)
    assert rep["quarantined"] == ["flatmates"] and not rows[0]["ok"] and rows[1]["ok"]
    assert set(rep["drop_rows"]) == {ps[0]["iid"]} | {p["iid"] for p in ps[50:]}      # mismatch + whole register


# ------------------------------------------------------------------------------------------------ the freeze
@pytest.fixture(scope="module")
def frozen():
    def snap():
        return {p: p.stat().st_mtime_ns for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    before = snap()
    res = F.run(())
    assert snap() == before, "run() must write nothing"
    return res


def test_status_ready_every_g0_minimum_and_gate(frozen):
    assert frozen["status"] == "READY" and frozen["shortfalls"] == [] and frozen["blocked"] == []
    by = {c["id"]: c for c in frozen["checks"]}
    assert all(c["met"] for c in by.values())
    assert by["message_forms_per_sem"]["have"] >= 12 and len(by["message_forms_per_sem"]["by"]) == 13
    assert by["wordings_per_qform"]["have"] >= 3 and len(by["wordings_per_qform"]["by"]) == 10
    assert by["wordings_total"]["have"] >= 30
    assert by["packs_frozen_per_setting"]["total"] == 30 and by["packs_frozen_per_setting"]["have"] == 5
    assert by["skins_per_register"]["have"] >= 6 and len(by["skins_per_register"]["by"]) == 11
    assert by["registers"]["have"] == [11, 2]
    assert by["glex_gate_used_forms"]["status_counts"] == {"admitted": 469}
    assert by["g3h_per_template"]["have"] >= 0.98


def test_requested_gaps_are_reported_not_hidden_and_not_binding(frozen):
    g = frozen["requested_gaps"]
    assert {k: v["gap"] for k, v in g.items()} == {"attack_notes": 0, "freeform_intros": 20, "message_forms": 12,
                                                   "packs": 12, "skins": 15, "wordings": 10}
    assert all(v["binding"] is False for v in g.values())


def test_g_lex_is_two_of_two_over_the_used_forms(frozen):
    reg, used = frozen["reg"], frozen["adm_lex"]
    assert set(used.forms) <= set(reg.forms) and len(used.forms) == 469
    assert all(used.status(f) == "admitted" and used.forms[f].required == 2 for f in used.forms)
    assert all(len({e for e, s in used.forms[f].extractions if s == used.forms[f].sem_id}) == 2 for f in used.forms)
    assert frozen["lex_gate_used"]["pass"] is True
    # the 5 rejected yn_dneg_broken wordings are quarantined, never used; the whole-registry gate still lists them
    assert frozen["lex_gate_registry"]["pass"] is False and len(frozen["rejected_forms"]) == 5
    assert not set(frozen["rejected_forms"]) & set(used.forms)
    st = {q["form_id"] for q in frozen["rows"]["quarantine.jsonl"] if q["stage"] == "G-LEX"}
    assert st == set(frozen["rejected_forms"])


def test_v1_rebuilt_from_validated_answers_is_byte_identical_where_unchanged(frozen):
    ident = frozen["v1_identity"]
    for n in ("skins.jsonl", "skins_held.jsonl", "attack_notes.jsonl", "packs.jsonl", "packs_reserve.jsonl",
              "lexicon_admitted.jsonl", "lexicon_registry.json"):
        assert ident[n] == "identical", n
    assert ident["freeform.jsonl"] == "differs" and ident["quarantine.jsonl"] == "differs"


def test_redo2_mode_f_merged_and_round1_quarantines_stand(frozen):
    rows = frozen["rows"]
    f, fh = rows["freeform.jsonl"], rows["freeform_held.jsonl"]
    r1 = [r for r in f + fh if r["round"] == "r1"]
    r2 = [r for r in f + fh if r["round"] == "redo2"]
    assert len(r1) == 12 and {r["register"] for r in r1} == {"email_digest"}       # nothing from round 1 is revived
    assert len(r2) == 88 and len(f) == 81 and len(fh) == 19
    assert all(r["g3h"] == "pass" for r in f + fh)
    assert {r["register"] for r in fh} == {"sms_export", "forum_thread"}
    assert not {r["register"] for r in f} & {"sms_export", "forum_thread"}
    ids = [r["id"] for r in f + fh]
    assert len(ids) == len(set(ids)) and all(i.startswith("r2|") for i in (r["id"] for r in r2))
    q = rows["quarantine.jsonl"]
    assert sum(1 for x in q if x["stage"] == "G3-H") == 98                         # the v1 entries, all kept
    assert sum(1 for x in q if x["stage"] == "redo2 lint") == 20
    assert not any(x["stage"] == "redo2 G3-H" for x in q)                          # no redo2 mismatch this round
    mf = frozen["counts"]["mode_f"]
    assert mf["redo2"]["g3h_mismatch"] == 0 and mf["redo2"]["quarantined_registers"] == []
    assert mf["round1"]["quarantined_registers"] and "email_digest" not in mf["round1"]["quarantined_registers"]
    assert mf["training_share_of_narrative_texts"] <= 0.40


def test_votes_sidecar_records_every_vote(frozen):
    v = frozen["votes"]
    lex = [x for x in v if x["gate"] == "G-LEX"]
    assert len(lex) == 474 and all(len(x["reads"]) == 2 for x in lex)
    assert sum(1 for x in v if x["gate"] == "G3-H" and x["round"] == "r1") == 110
    r2 = [x for x in v if x["gate"] == "G3-H" and x["round"] == "redo2"]
    assert len(r2) == 88 and all(x["ok"] and x["answer"]["owner"] != "NONE" for x in r2)


def test_pool_texts_carry_no_gold_label(frozen):
    banned = set(P.T32.LABEL_WORDS)
    import re
    rx = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in sorted(banned, key=len, reverse=True)) + r")\b", re.I)
    for name in ("skins.jsonl", "skins_held.jsonl", "freeform.jsonl", "freeform_held.jsonl", "attack_notes.jsonl"):
        for r in frozen["rows"][name]:
            txt = r["text"] if isinstance(r["text"], str) else json.dumps(r["text"])
            assert not rx.search(txt), (name, r["id"], txt)


class _Plain:
    """Plain writers for the tmp folder (the kit's guarded ones only write under lean/)."""
    @staticmethod
    def write_json(p, obj):
        p = Path(p)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return p

    @staticmethod
    def write_jsonl(p, rows):
        p = Path(p)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        return p


@pytest.fixture(scope="module")
def written(frozen, tmp_path_factory):
    root = tmp_path_factory.mktemp("pools_v2")
    man = F.write_pools(frozen, root, _Plain)
    return root, man


def test_manifest_is_complete(written, frozen):
    _root, man = written
    assert man["status"] == "READY" and man["family"] == "T32" and man["version"] == "freeze-v2"
    assert man["g0_spec"]["sha256"] == P.T32.G0_SHA256
    assert man["ignored_task_ids"] == [] and "ignored_note" in man
    assert {m["id"] for m in man["minimums"]} >= {"message_forms_per_sem", "skins_per_register", "glex_gate_used_forms"}
    assert man["requested_gaps"]["freeform_intros"]["binding"] is False
    assert man["how_to_load"]["plugin_reads_pool_files"] is False and "g13_seed" in man["how_to_load"]
    assert set(man["files"]) >= {"pools_v2/skins.jsonl", "pools_v2/freeform.jsonl", "pools_v2/lexicon_registry.json",
                                 "pools_v2/votes_sidecar.jsonl", "pools_v2/validation_report.json"}
    assert man["inputs"]["answer_files"] and all(v["ok"] for v in man["inputs"]["answer_files"].values())
    assert len(man["inputs"]["answer_files"]) == 28 + 23 + 2 + 2
    # the sidecars match g13's SEED_SKIP (not scanned as templates) while the pool files do not
    import re
    skip = re.compile(r"sealedqc|denylist|lint|manifest|report|check|verdict|summary|draw|gates|sidecar|qc_side", re.I)
    assert skip.search("votes_sidecar.jsonl") and skip.search("validation_report.json") and skip.search("MANIFEST.json")
    assert not skip.search("freeform.jsonl") and not skip.search("skins.jsonl")


def test_pools_load_back_and_rebuild_into_ctx_and_plugin(written):
    root, _man = written
    pools = F.load_pools(root)
    assert len(pools["freeform"]) == 81 and len(pools["freeform_held"]) == 19 and len(pools["packs"]) == 30
    assert len(pools["lexicon"].forms) == 469
    skins, probs = F.build_skins(pools)
    assert probs == [] and len(skins) == len(pools["skins"]) + len(pools["skins_held"]) + len(
        pools["attack_notes"]) + len(pools["freeform"]) + len(pools["freeform_held"])
    ctx = F.kit_ctx(pools)
    assert ctx.lexicon is pools["lexicon"] and len(ctx.skins) == len(skins)
    assert any(s.author_mode == "F" and s.held_out for s in ctx.skins.values())
    plugin = P.T32(lexicon=pools["lexicon"])
    for sem in P.SIG:
        assert plugin._forms_of(sem), sem                                  # every message sem has admitted forms


def test_load_pools_detects_a_changed_byte(written, tmp_path):
    root, _ = written
    for p in root.iterdir():
        (tmp_path / p.name).write_bytes(p.read_bytes())
    F.load_pools(tmp_path)
    f = tmp_path / "freeform.jsonl"
    f.write_bytes(f.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="sha256"):
        F.load_pools(tmp_path)


def test_writer_refuses_before_a38(frozen, tmp_path, monkeypatch):
    fake = tmp_path / "PREREG_FINAL.md"
    fake.write_text("# no A38 here\n", encoding="utf-8")
    monkeypatch.setattr(paths, "PREREG", fake)
    before = sorted(p.name for p in F.POOLS_V2.iterdir()) if F.POOLS_V2.exists() else None
    with pytest.raises(paths.DataBeforeFreeze):
        F.write_pools(frozen)
    after = sorted(p.name for p in F.POOLS_V2.iterdir()) if F.POOLS_V2.exists() else None
    assert after == before


# ------------------------------------------------------------------------------------------------ rebuild equals v1
def test_validated_collect_equals_the_family_loader(validation):
    ok = {t: v for t, v in F.accepted(validation["rounds"]["author"]).items()}
    mine, authored, cov = F.collect_validated(ok)
    theirs, authored1 = X.collect()
    assert authored == authored1 and cov == {"missing_tasks": [], "unanswered_items": 0}
    assert {k: [(p["iid"], p["ok"], p["out"], p["problems"]) for p in v] for k, v in mine.items()} == \
           {k: [(p["iid"], p["ok"], p["out"], p["problems"]) for p in v] for k, v in theirs.items()}


def test_missing_authoring_answer_blocks_the_freeze(validation):
    tid = sorted(validation["rounds"]["author"]["files"])[0]
    res = F.run((tid,))
    # the rebuilt extraction batches no longer match the manifests / keys the answers were scored against
    assert res["status"] == "BLOCKED" and res["blocked"] and "extract" in " ".join(res["blocked"])
    assert "pools" not in res and "rows" not in res


def test_ignoring_the_redo2_reads_keeps_every_minimum_and_drops_the_unread_intros(validation):
    ids = ("T32-extract_g3h-9a1661ac-000", "T32-extract_g3h-9a1661ac-001")
    res = F.run(ids)
    assert res["status"] == "READY" and res["shortfalls"] == [] and res["ignored"] == list(ids)
    mf = res["counts"]["mode_f"]
    assert mf["redo2"]["passed_training"] == 0 and mf["pool_training"] == 12 and mf["pool_held_out"] == 0
    q = [x for x in res["rows"]["quarantine.jsonl"] if x["stage"] == "redo2 G3-H"]
    assert len(q) == 88 and all("unanswered" in " ".join(x["reasons"]) for x in q)
    assert res["requested_gaps"]["freeform_intros"]["gap"] == 108
