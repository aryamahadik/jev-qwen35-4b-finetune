"""c2_build/families/T29/test_validate_answers.py: the answer validator (validate_answers.py) on small synthetic rounds
(tmp dirs; nothing in haiku/ is touched), and, when the files exist, the real answer files of all four rounds and the
redo2 supplement pools/redo2/ (read only).

Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T29/test_validate_answers.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import lexicon as LX  # noqa: E402
from families.T29 import validate_answers as V  # noqa: E402

HERE = Path(__file__).resolve().parent
POOLS = HERE / "pools"
SUPP = POOLS / "redo2"
REDO2_EX = HERE / "haiku" / "redo2" / "extract"

# G0 floors as test_authoring.py states them (hard-coded here so that a lowered pool_freeze.G0 is caught)
FLOORS = {"packs": 75, "actions": 120, "skins_training": 800, "skins_held_out": 80, "registers_training": 8,
          "registers_held_out": 2, "attack_lines": 60, "freeform_training": 100, "lex_comparator": 60,
          "lex_precedence": 20, "lex_confirmation": 60, "wordings_total": 30, "wordings_training": 150,
          "wordings_held_out": 30, "wordings_per_form_training": 5}


# ------------------------------------------------------------------------------------------------ synthetic rounds
def _sha(o) -> str:
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def make_round(tmp_path: Path, kind: str, items: list, answers, *, row_extra: dict | None = None) -> tuple:
    """One-task round: (root, row). items: chunk items (qid included); answers: the raw answer object (or str text)."""
    root = tmp_path / "round"
    for d in ("chunks", "answers", "manifest"):
        (root / d).mkdir(parents=True, exist_ok=True)
    tid, batch = "T29-test-000", "T29-test"
    chunk = {"task_id": tid, "kind": kind, "prompt_sha": "x", "items": items}
    (root / "chunks" / f"{tid}.json").write_text(json.dumps(chunk, ensure_ascii=False))
    (root / "manifest" / f"{batch}.json").write_text(json.dumps({"tasks": [{"task_id": tid, "sha256": _sha(chunk)}]}))
    if answers is not None:
        text = answers if isinstance(answers, str) else json.dumps(answers)
        (root / "answers" / f"{tid}.json").write_text(text)
    row = {"task_id": tid, "kind": kind, "batch_id": batch, "n_items": len(items),
           "answer_file": str(root / "answers" / f"{tid}.json"), **(row_extra or {})}
    (root / "TASKS.json").write_text(json.dumps({"tasks": [row]}))
    return root, row


LEX_ITEMS = [{"qid": "qaaaaaaaaaa", "text": "t1", "choices": ["m1", "m2"]},
             {"qid": "qbbbbbbbbbb", "text": "t2", "choices": ["m2", "m3"]}]


def test_valid_lexicon_round_passes(tmp_path):
    root, row = make_round(tmp_path, "extract_lex", LEX_ITEMS,
                           [{"qid": "qaaaaaaaaaa", "meaning": "m1"}, {"qid": "qbbbbbbbbbb", "meaning": "m3"}],
                           row_extra={"outputs_expected": 2})
    rep = V.check_task(root, row)
    assert rep["ok"] and rep["outputs"] == 2 and rep["problems"] == []
    full = V.check_round("t", root)
    assert full["valid"] == ["T29-test-000"] and not full["invalid"] and not full["stray_files"]


def test_a_meaning_outside_the_items_own_choices_is_rejected(tmp_path):
    # "m1" is a choice of item 1 only: copying it onto item 2 is invalid, and so is a paraphrase
    root, row = make_round(tmp_path, "extract_lex", LEX_ITEMS,
                           [{"qid": "qaaaaaaaaaa", "meaning": "m1"}, {"qid": "qbbbbbbbbbb", "meaning": "m1"}])
    rep = V.check_task(root, row)
    assert not rep["ok"] and "choices" in rep["problems"][0]
    root, row = make_round(tmp_path / "b", "extract_lex", LEX_ITEMS,
                           [{"qid": "qaaaaaaaaaa", "meaning": "m 1"}, {"qid": "qbbbbbbbbbb", "meaning": "m3"}])
    assert not V.check_task(root, row)["ok"]


def test_missing_duplicate_and_outside_qids_are_rejected(tmp_path):
    cases = {
        "unanswered": [{"qid": "qaaaaaaaaaa", "meaning": "m1"}],
        "answered 2 times": [{"qid": "qaaaaaaaaaa", "meaning": "m1"}, {"qid": "qaaaaaaaaaa", "meaning": "m1"},
                             {"qid": "qbbbbbbbbbb", "meaning": "m3"}],
        "not in the chunk": [{"qid": "qaaaaaaaaaa", "meaning": "m1"}, {"qid": "qbbbbbbbbbb", "meaning": "m3"},
                             {"qid": "qcccccccccc", "meaning": "m1"}],
    }
    for i, (needle, ans) in enumerate(cases.items()):
        root, row = make_round(tmp_path / f"c{i}", "extract_lex", LEX_ITEMS, ans)
        rep = V.check_task(root, row)
        assert not rep["ok"] and any(needle in p for p in rep["problems"]), (needle, rep)


def test_extra_keys_wrong_types_and_bad_json_are_rejected(tmp_path):
    root, row = make_round(tmp_path / "a", "extract_lex", LEX_ITEMS,
                           [{"qid": "qaaaaaaaaaa", "meaning": "m1", "why": "x"}, {"qid": "qbbbbbbbbbb", "meaning": 3}])
    rep = V.check_task(root, row)
    assert not rep["ok"] and len(rep["problems"]) == 2
    root, row = make_round(tmp_path / "b", "extract_lex", LEX_ITEMS, "[{not json")
    assert "not JSON" in V.check_task(root, row)["problems"][0]
    root, row = make_round(tmp_path / "c", "extract_lex", LEX_ITEMS, {"qaaaaaaaaaa": "m1"})
    assert "array of objects" in V.check_task(root, row)["problems"][0]
    root, row = make_round(tmp_path / "d", "extract_lex", LEX_ITEMS, None)
    assert V.check_task(root, row)["problems"] == ["answer file missing"]


def test_g3h_reason_must_be_a_choice_or_none(tmp_path):
    items = [{"qid": "qaaaaaaaaaa", "text": "d", "schema": [
        {"field": "requester", "type": "name"},
        {"field": "reason", "type": "category", "choices": ["audit preparation", "month-end close"]}]}]
    ok = [{"qid": "qaaaaaaaaaa", "requester": "Ana Reyes", "reason": "month-end close"}]
    none = [{"qid": "qaaaaaaaaaa", "requester": "Ana Reyes", "reason": "NONE"}]
    bad = [{"qid": "qaaaaaaaaaa", "requester": "Ana Reyes", "reason": "month end close"}]
    blank = [{"qid": "qaaaaaaaaaa", "requester": " ", "reason": "month-end close"}]
    for i, (ans, good) in enumerate(((ok, True), (none, True), (bad, False), (blank, False))):
        root, row = make_round(tmp_path / f"g{i}", "extract_g3h", items, ans)
        assert V.check_task(root, row)["ok"] is good, ans


def test_author_lists_need_the_asked_count_of_nonempty_strings(tmp_path):
    items = [{"qid": "qaaaaaaaaaa", "brief": "a note; write 3 different texts", "register": "chat", "slots": {},
              "rules": []}]
    for i, (ans, good) in enumerate(((["a", "b", "c"], True), (["a", "b"], False), (["a", "b", ""], False),
                                     (["a", "b", 3], False), ("abc", False))):
        root, row = make_round(tmp_path / f"s{i}", "author_skin", items, [{"qid": "qaaaaaaaaaa", "texts": ans}])
        assert V.check_task(root, row)["ok"] is good, ans
    # the redo2 manifest states the count; a brief with how_many states it too
    root, row = make_round(tmp_path / "r", "author_wording", [{"qid": "qaaaaaaaaaa", "brief": {"how_many": 2},
                                                                "slots": {}, "rules": []}],
                           [{"qid": "qaaaaaaaaaa", "wordings": ["a", "b"]}], row_extra={"outputs_per_item": 2})
    assert V.check_task(root, row)["ok"]
    root, row = make_round(tmp_path / "t", "author_freeform", [{"qid": "qaaaaaaaaaa", "brief": "x", "register": "chat",
                                                                 "facts": {}, "rules": []}],
                           [{"qid": "qaaaaaaaaaa", "text": "  "}])
    assert not V.check_task(root, row)["ok"]


def test_pack_contract():
    good = {"org_name": "Stemwell Flora", "org_domain": "stemwellflora.example",
            "lookalike_domains": ["stemwell-flora.example", "stemwellflora.test"],
            "partner_domains": ["rootbarn.example", "chillcrate.example"], "target_prefix": "ORD",
            "people": ["A One", "B Two", "C Three", "D Four"]}
    assert V.check_pack(good) == []
    for key, val in (("target_prefix", "Ord"), ("org_domain", "stemwell.com"), ("people", ["A One"] * 4),
                     ("partner_domains", ["x.example"])):
        assert V.check_pack({**good, key: val}), key
    assert V.check_pack({k: v for k, v in good.items() if k != "people"})


def test_chunk_hash_mismatch_and_stray_files_are_reported(tmp_path):
    root, row = make_round(tmp_path, "extract_lex", LEX_ITEMS,
                           [{"qid": "qaaaaaaaaaa", "meaning": "m1"}, {"qid": "qbbbbbbbbbb", "meaning": "m3"}])
    chunk_p = root / "chunks" / "T29-test-000.json"
    chunk = json.loads(chunk_p.read_text())
    chunk["items"][0]["text"] = "changed after the manifest"
    chunk_p.write_text(json.dumps(chunk))
    assert "chunk on disk differs" in V.check_task(root, row)["problems"][0]
    (root / "answers" / "stray.json").write_text("[]")
    assert V.check_round("t", root)["stray_files"] == ["stray.json"]


# ------------------------------------------------------------------------------------------------ the real files
needs_answers = pytest.mark.skipif(not (REDO2_EX / "answers").is_dir(), reason="redo2 extraction not run yet")


@needs_answers
def test_every_real_answer_file_of_all_four_rounds_meets_its_contract():
    rep = V.check_all()
    assert rep["answer_files_invalid"] == 0 and rep["stray_files"] == {} and rep["all_valid"], rep
    assert {r["round"]: r["tasks"] for r in rep["rounds"]} == {"author": 33, "extract": 21, "redo2": 7,
                                                                "redo2/extract": 6}
    # the outputs are the counts the manifests expected (checked per file above)
    assert {r["round"]: r["outputs_valid"] for r in rep["rounds"]} == {"author": 1888, "extract": 908, "redo2": 169,
                                                                        "redo2/extract": 231}


@needs_answers
def test_redo2_extraction_votes_recount_without_the_kit():
    r = V.crosscheck_redo2_extract()
    assert r["forms_in_pool"] == r["forms_voted"] == r["forms_two_reads_both_agree"] == 78
    assert r["forms_any_disagreement"] == [] and r["forms_not_read_twice"] == []
    assert r["g3h"]["n"] == 75 and r["g3h"]["ok"] == 75
    assert all(d["ok"] / d["n"] >= 0.98 for d in r["g3h"]["by_register"].values())


# ------------------------------------------------------------------------------------------------ the supplement
needs_supp = pytest.mark.skipif(not (SUPP / "MANIFEST.json").is_file(), reason="redo2 admit not written yet")


def _jsonl(p: Path) -> list:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


@pytest.fixture(scope="module")
def supp():
    return json.loads((SUPP / "MANIFEST.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def merged_registry():
    return LX.LexiconRegistry.from_json(json.loads((SUPP / "lexicon_merged.json").read_text(encoding="utf-8")))


@needs_supp
def test_pool_freeze_targets_are_not_lowered():
    from families.T29 import pool_freeze as PF
    for k, v in FLOORS.items():
        assert PF.G0[k] >= v, k


@needs_supp
def test_v1_pools_are_untouched_and_the_supplement_is_bound_to_them(supp):
    v1 = json.loads((POOLS / "MANIFEST.json").read_text(encoding="utf-8"))
    assert supp["base_manifest_sha256"] == hashlib.sha256((POOLS / "MANIFEST.json").read_bytes()).hexdigest()
    for rel, d in v1["pool_files"].items():
        assert hashlib.sha256((POOLS / rel).read_bytes()).hexdigest() == d["sha256"], rel
    for rel, d in supp["pool_files"].items():
        assert hashlib.sha256((SUPP / rel).read_bytes()).hexdigest() == d["sha256"], rel
    assert supp["matches_plugin_G0_SHA256"] is True


@needs_supp
def test_merged_registry_passes_g_lex_with_the_required_distinct_extractors(merged_registry):
    reg = merged_registry
    gate = reg.gate()
    assert gate["pass"] and gate["not_admitted"] == {} and gate["status_counts"] == {"admitted": 470}
    v1_ids = {f["form_id"] for f in json.loads((POOLS / "lexicon.json").read_text(encoding="utf-8"))["forms"]}
    new_ids = set(reg.forms) - v1_ids
    assert len(v1_ids) == 392 and len(new_ids) == 78 and v1_ids <= set(reg.forms)
    for fid, f in reg.forms.items():
        need = 3 if f.kind == "precedence" else 2
        assert f.unit_ok and {s for _, s in f.extractions} == {f.sem_id}, fid
        assert len({e for e, _ in f.extractions}) >= need, fid
    # the new forms were read by two different tasks (glex-r1, glex-r2), never twice by one
    for fid in new_ids:
        ex = [e for e, _ in reg.forms[fid].extractions]
        assert len(ex) == len(set(ex)) == 2


@needs_supp
def test_supplement_ids_do_not_collide_with_v1_and_the_new_pieces_are_the_admitted_ones(merged_registry):
    new_words = _jsonl(SUPP / "wordings.jsonl")
    new_atk = _jsonl(SUPP / "attack_lines.jsonl")
    new_ff = _jsonl(SUPP / "freeform.jsonl")
    assert (len(new_words), len(new_atk), len(new_ff)) == (24, 16, 75)
    v1_words, v1_atk, v1_ff = (_jsonl(POOLS / n) for n in ("wordings.jsonl", "attack_lines.jsonl", "freeform.jsonl"))
    for new, old, key in ((new_words, v1_words, "form_id"), (new_atk, v1_atk, "attack_id"),
                          (new_ff, v1_ff, "doc_id")):
        assert not {r[key] for r in new} & {r[key] for r in old}, key
        assert len({r[key] for r in new}) == len(new)
    assert not {r["text_sha256"] for r in new_atk} & {r["text_sha256"] for r in v1_atk}
    assert not {r["text_sha256"] for r in new_ff} & {r["text_sha256"] for r in v1_ff}
    assert all(w["status"] == "admitted" and w["form_id"] in merged_registry.forms
               and merged_registry.status(w["form_id"]) == "admitted" and w["qform"] == "yn_not_forbidden"
               for w in new_words)
    assert all(d["g3h"] == "match" and not d["held_out"] for d in new_ff)
    assert _jsonl(SUPP / "quarantine.jsonl") == []


@needs_supp
def test_merged_pools_meet_every_g0_minimum_recounted_from_the_files(supp, merged_registry):
    reg = merged_registry
    skins, packs, acts = (_jsonl(POOLS / n) for n in ("skins.jsonl", "packs.jsonl", "actions.jsonl"))
    atk = _jsonl(POOLS / "attack_lines.jsonl") + _jsonl(SUPP / "attack_lines.jsonl")
    ff = _jsonl(POOLS / "freeform.jsonl") + _jsonl(SUPP / "freeform.jsonl")
    adm = [f for f in reg.forms.values() if reg.status(f.form_id) == "admitted"]
    kinds = Counter(f.kind for f in adm)
    q = [f for f in adm if f.kind == "question"]
    per_form = Counter(f.sem_id.split(".")[-1] for f in q if not f.held_out)
    from families.T29 import plugin as P
    got = {"packs": len(packs), "actions": len(acts),
           "skins_training": sum(not s["held_out"] for s in skins), "skins_held_out": sum(s["held_out"] for s in skins),
           "registers_training": len({s["register"] for s in skins if not s["held_out"]}),
           "registers_held_out": len({s["register"] for s in skins if s["held_out"]}),
           "attack_lines": len(atk), "freeform_training": sum(not d["held_out"] for d in ff),
           "lex_comparator": kinds["comparator"], "lex_precedence": kinds["precedence"],
           "lex_confirmation": kinds["confirmation"], "wordings_total": len(q),
           "wordings_training": sum(not f.held_out for f in q), "wordings_held_out": sum(f.held_out for f in q),
           "wordings_per_form_training": min(per_form.get(qf, 0) for qf in P.T29Plugin.V1_QFORMS)}
    short = {k: (got[k], FLOORS[k]) for k in FLOORS if got[k] < FLOORS[k]}
    assert short == {}, short
    assert supp["summary"]["shortfalls"] == []
    # every question form has training wordings, and every typed comparator the plugin uses has forms
    assert set(per_form) == set(P.T29Plugin.V1_QFORMS)       # yn_go_dneg has no wording yet (fix iteration 1, FIX-6)
    cmp_types = Counter(f"{f.sem_id}|{dict(f.slots).get('X')}" for f in adm if f.kind == "comparator")
    for need in ("cmp.gt|count", "cmp.ge|count", "cmp.lt|count", "cmp.le|count", "cmp.gt|cents", "cmp.ge|cents"):
        assert cmp_types[need] >= 5, need
    assert {f.sem_id for f in adm if f.kind == "confirmation"} == {"conf.t29.explicit", "conf.t29.mention"}


@needs_supp
def test_g3h_bar_holds_per_register_alone_and_combined_with_v1(supp):
    s = supp["summary"]
    assert s["g3h_redo2_quarantined"] == []
    for d in list(s["g3h_redo2_templates"].values()) + list(s["g3h_combined_with_v1"].values()):
        assert d["ok"] / d["n"] >= 0.98
