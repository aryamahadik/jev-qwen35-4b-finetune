"""families/T25/test_freeze_v2.py: tests of freeze_v2.py (the T25 pool re-freeze, G0 v3 section 10).

G0 moved on to v4 at pilot fix iteration 1 (section 11: option display plan, card text and placement, 28 cards, wording
polarity); it changes no pool piece. pools_v2/ stays bound to G0 v3 (its MANIFEST records the v3 sha and freeze_v2.py's own
sha, so neither is edited): these tests point F.G0 / F.G0_PIN at the archived G0_SPEC_v3.md for the pool freeze and check
the family's current G0 (v4) separately.

Contracts      each answer-file shape (author packs / texts, G-LEX picks, G3-H extractions) accepts a valid file and
               rejects a missing, extra or repeated qid, a wrong key, a wrong type and an off-list meaning
Answer files   all 29 real answer files of the three rounds are valid; a tampered copy is rejected whole (never edited); a
               stray file is flagged; an audit-failed task is ignored and its pieces / reads / documents are absent
Rules          G-LEX reads: 2 for question forms, a different pick rejects for good; B1 / B2 / B3 outcomes on the real pools
               (memo noun, yn_claim#3fab6dc5, 61 admitted Mode F documents, 23 cut by the cap)
Freeze         verdict READY with no shortfall; freeze-v1 byte-identical; every v2 piece comes from v1; MANIFEST hashes
               match; pools_v2 on disk (when written) equals a rebuild; the writer never overwrites a different freeze
Consumer       load_pools_v2 verifies the MANIFEST; kit_ctx builds a KitCtx whose skins / wordings / lexicon run through
               pipeline.build_unit (in memory, nothing trained or written beyond the scratch folder, removed at the end)
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

from c2_kit import pipeline  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import freeze_v2 as F  # noqa: E402
from families.T25 import haiku_author as HA  # noqa: E402
from families.T25 import plugin as P  # noqa: E402
from families.T25 import stage6_admit as S6  # noqa: E402

Y = "q.t25.yn_claim#3fab6dc5"
SCRATCH = HERE / "_t_scratch_pools_v2"
G0_V3 = HERE / "G0_SPEC_v3.md"                    # the G0 the pool freeze was made under (kept byte for byte)
G0_V3_SHA = "8de68753f87b885d02b15ec6207fa3ce9d69ea971a4126dd0868335dfe7fdf11"


@pytest.fixture(scope="module", autouse=True)
def pool_freeze_g0():
    mp = pytest.MonkeyPatch()
    mp.setattr(F, "G0", G0_V3)
    mp.setattr(F, "G0_PIN", G0_V3_SHA)
    yield
    mp.undo()


@pytest.fixture(scope="module")
def built():
    return F.build()


@pytest.fixture(scope="module")
def scratch():
    shutil.rmtree(SCRATCH, ignore_errors=True)
    yield SCRATCH
    shutil.rmtree(SCRATCH, ignore_errors=True)


def files_of(built, name):
    return json.loads(built["files"][name])


# ------------------------------------------------------------------------------------------------ targets
def test_targets_not_lowered():
    for k, v in S6.TARGET.items():
        assert F.TARGET[k if k in F.TARGET else k.replace("mode_f_cap", "mode_f_register_cap")] >= v, k
    assert F.TARGET["attr_packs"] == 30 and F.TARGET["source_nouns"] == 40 and F.TARGET["tier_schemes"] == 8
    assert F.TARGET["wordings_total"] == 30 and F.TARGET["wordings_per_form"] == 4
    assert F.TARGET["registers"] == 8 and F.TARGET["registers_held_out"] == 2
    assert F.TARGET["mode_f_register_cap"] == 0.20 and F.TARGET["mode_f_rows_cap"] == 0.25
    assert F.TARGET["register_share_cap"] == 0.15 and F.TARGET["g3h_rate"] == 0.98


def test_g0_pin_is_v3_for_the_pool_freeze_and_v4_for_the_family():
    assert F.sha_file(F.G0) == F.G0_PIN == G0_V3_SHA          # the pool freeze: G0 v3, archived byte for byte
    assert F.G0_PIN != S6.G0_PIN                              # stage6_admit still pins G0 v2 and so refuses a re-freeze
    now = HERE / "G0_SPEC.md"                                 # the family's G0 is v4 (section 11), pinned by the plugin
    assert F.sha_file(now) == P.T25.G0_SHA256 != G0_V3_SHA
    assert "FROZEN v4" in now.read_text(encoding="utf-8").split("\n", 4)[3]
    assert man_g0_unchanged_for_pools()


def man_g0_unchanged_for_pools():
    """The pools on disk record G0 v3: v4 changes no pool piece (the loader checks every file against the MANIFEST)."""
    man = json.loads((F.POOLS_V2 / "MANIFEST.json").read_text(encoding="utf-8"))
    return man["binding"]["G0_SPEC_sha256"] == G0_V3_SHA and man["inputs"]["G0_SPEC.md"]["sha256"] == G0_V3_SHA


# ------------------------------------------------------------------------------------------------ contracts (pure)
def _chunk_qids(n=3):
    return [f"q{i:010d}" for i in range(n)]


VALID = {
    ("author_pack", "attrs"): lambda q: {"qid": q, "pack": {"attr": "late filing fee", "kind": "money", "unit": None,
                                                           "values": [1000, 2000, 3000, 4000, 5000, 6000]}},
    ("author_pack", "nouns"): lambda q: {"qid": q, "pack": {"labels": [f"page {i}" for i in range(12)]}},
    ("author_pack", "names"): lambda q: {"qid": q, "pack": {"names": [f"Name {i}" for i in range(6)]}},
    ("author_pack", "schemes"): lambda q: {"qid": q, "pack": {"ranks": ["scarlet", "teal", "ochre"]}},
    ("author_skin", "skins"): lambda q: {"qid": q, "text": "Hello {ASKER}"},
    ("author_skin", "attacks"): lambda q: {"qid": q, "text": "Note from {ASKER}"},
    ("author_freeform", "freeform"): lambda q: {"qid": q, "text": "Some note"},
    ("author_wording", "wordings"): lambda q: {"qid": q, "text": "What is it?"},
    ("extract_g3h", None): lambda q: {"qid": q, "asker": "Aiko Brandt", "org": None, "attr": "late fee"},
}


@pytest.mark.parametrize("kind,name", sorted(VALID, key=str))
def test_valid_answers_pass_and_broken_ones_fail(kind, name):
    qids = _chunk_qids()
    ok = [VALID[(kind, name)](q) for q in qids]
    assert F.answer_problems(kind, name, ok, qids) == []
    assert F.answer_problems(kind, name, ok[:-1], qids)                               # a qid unanswered
    assert F.answer_problems(kind, name, ok + [VALID[(kind, name)]("qextra")], qids)  # a qid outside the chunk
    assert F.answer_problems(kind, name, ok + [ok[0]], qids)                          # a qid twice
    assert F.answer_problems(kind, name, {"qid": 1}, qids)                            # not a list
    bad = copy.deepcopy(ok)
    bad[0]["unexpected"] = 1                                                          # an extra key
    assert F.answer_problems(kind, name, bad, qids)
    bad = copy.deepcopy(ok)
    del bad[1]["qid"]
    assert F.answer_problems(kind, name, bad, qids)
    assert F.answer_problems(kind, name, ["x"] * 3, qids)                             # items are objects


def test_pack_and_g3h_field_types_are_enforced():
    qids = _chunk_qids(1)
    q = qids[0]
    a = VALID[("author_pack", "attrs")](q)
    for mut in (lambda p: p.update(kind="percent"), lambda p: p.update(values="1,2"), lambda p: p.update(unit=5),
                lambda p: p.update(values=[1.5, 2, 3, 4, 5, 6]), lambda p: p.update(attr=""),
                lambda p: p.pop("unit")):
        b = copy.deepcopy(a)
        mut(b["pack"])
        assert F.answer_problems("author_pack", "attrs", [b], qids), mut
    d = copy.deepcopy(a)
    d["pack"].update(kind="date", values=[1])
    assert F.answer_problems("author_pack", "attrs", [d], qids)                       # a date pack has no values
    n = VALID[("author_pack", "nouns")](q)
    n["pack"]["labels"].append("extra page")
    assert F.answer_problems("author_pack", "nouns", [n], qids)                        # exactly 12 labels
    g = VALID[("extract_g3h", None)](q)
    g["asker"] = ""
    assert F.answer_problems("extract_g3h", None, [g], qids)                           # empty string is no value; null is
    g["asker"] = 7
    assert F.answer_problems("extract_g3h", None, [g], qids)


def test_lex_answers_are_closed_list_picks():
    qids = _chunk_qids()
    closed = {"m1", "m2", "m3"}
    ok = {q: "m1" for q in qids}
    assert F.answer_problems("extract_lex", None, ok, qids, closed) == []
    assert F.answer_problems("extract_lex", None, {**ok, qids[0]: "m4"}, qids, closed)            # off the printed list
    assert F.answer_problems("extract_lex", None, {**ok, qids[0]: 3}, qids, closed)               # not text
    assert F.answer_problems("extract_lex", None, {q: "m1" for q in qids[:2]}, qids, closed)      # unanswered
    assert F.answer_problems("extract_lex", None, {**ok, "qzz": "m1"}, qids, closed)              # outside the chunk
    assert F.answer_problems("extract_lex", None, [ok], qids, closed)                              # a list, not an object
    assert F.answer_problems("poll", None, [], qids)                                               # no contract for a kind


# ------------------------------------------------------------------------------------------------ the real answer files
def test_all_real_answer_files_are_valid():
    val = F.validate_answers()
    assert val["by_round"] == {"author": {"files": 21, "valid": 21, "usable": 21},
                               "extract": {"files": 6, "valid": 6, "usable": 6},
                               "redo2": {"files": 2, "valid": 2, "usable": 2}}
    assert val["invalid"] == [] and val["stray"] == [] and val["ignored"] == []
    assert len(val["usable"]) == 29
    assert all(f["sha256"] and f["problems"] == [] for f in val["files"])


def test_a_tampered_copy_is_rejected_whole_and_never_edited(tmp_path):
    root = tmp_path / "haiku"
    shutil.copytree(HERE / "haiku" / "redo2", root / "redo2", ignore=shutil.ignore_patterns("__pycache__", "*.py"))
    ans = sorted((root / "redo2" / "answers").glob("*.json"))
    tampered, kept = ans[0], ans[1]
    items = json.loads(tampered.read_text())
    tampered.write_text(json.dumps(items[:-1]))                                      # one item missing
    before = tampered.read_bytes()
    (root / "redo2" / "answers" / "notes.txt").write_text("stray")
    val = F.validate_answers(haiku_root=root)
    by = {f["task_id"]: f for f in val["files"]}
    assert not by[tampered.stem]["valid"] and "unanswered" in " ".join(by[tampered.stem]["problems"])
    assert by[kept.stem]["usable"] and tampered.stem not in val["usable"]
    assert val["invalid"] == [tampered.stem]
    assert [s["answer_file"] for s in val["stray"]] == ["redo2/answers/notes.txt"]
    assert tampered.read_bytes() == before                                           # never edited
    tampered.write_text("not json")
    assert F.validate_answers(haiku_root=root)["invalid"] == [tampered.stem]


def test_the_ambiguity_record_is_checked_against_its_own_contract(tmp_path):
    src = HERE / "haiku" / "ambiguity" / "amb_T25_points.json"
    assert F.ambiguity_problems(src) == []
    o = json.loads(src.read_text())
    bad = tmp_path / "amb.json"
    bad.write_text(json.dumps(dict(o, points=o["points"][:-1])))
    assert F.ambiguity_problems(bad)                                              # 38 points, wrong count and hash
    pts = [dict(p) for p in o["points"]]
    pts[0]["extra"] = 1
    bad.write_text(json.dumps(dict(o, points=pts)))
    assert F.ambiguity_problems(bad)
    bad.write_text("{")
    assert F.ambiguity_problems(bad)
    val = F.validate_answers()
    assert val["ambiguity"]["valid"] and val["ambiguity"]["problems"] == []


def test_an_audit_failed_task_is_ignored_not_edited():
    tid = "T25-extract_g3h-34177cc1-000"
    val = F.validate_answers(ignore=frozenset({tid}))
    f = next(x for x in val["files"] if x["task_id"] == tid)
    assert f["valid"] and f["ignored"] and not f["usable"]
    assert tid not in val["usable"] and val["ignored"] == [tid]


def test_hidden_author_files_drop_their_pieces_and_restore_the_loader():
    orig = HA.load_answers_for
    full, _ = HA.load_nouns()
    with F.author_files_hidden(frozenset({"T25-author_pack-acf53352-000"})):
        assert HA.load_answers_for is not orig
        nouns, probs = HA.load_nouns()
    assert HA.load_answers_for is orig
    assert nouns == [] and any("answer file rejected" in p for p in probs) and len(full) == 94


# ------------------------------------------------------------------------------------------------ G-LEX / G3-H (pure)
def _reg(n_forms=1):
    reg = LexiconRegistry("T25")
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem("T25", qf), "question", meaning)
    for i in range(n_forms):
        reg.add(f"Under the stated rules, what is the {{ATTR}} number {chr(97 + i)}?", question_sem("T25", "ch_value"),
                slots={"ATTR": "name"}, family="T25", source="haiku", haiku_task_id="t", haiku_prompt_sha="p")
    reg.unit_test_all()
    return reg


def _read(label, reg, pick):
    return {"read": label, "tid": f"t-{label}", "out": {fid: pick for fid in reg.forms}}


def test_glex_needs_two_independent_matching_reads():
    reg = _reg()
    own = FX.QUESTION_MEANINGS["ch_value"]
    fid = next(iter(reg.forms))
    assert reg.forms[fid].required == 2
    F.record_reads(reg, [_read("read1", reg, own)])
    assert reg.status(fid) == "pending"
    F.record_reads(reg, [_read("read2", reg, own)])
    assert reg.status(fid) == "admitted" and reg.gate()["pass"]


def test_glex_a_different_pick_rejects_for_good_and_a_repeat_read_raises():
    reg = _reg()
    fid = next(iter(reg.forms))
    F.record_reads(reg, [_read("read1", reg, FX.QUESTION_MEANINGS["ch_value"])])
    F.record_reads(reg, [_read("read2", reg, FX.QUESTION_MEANINGS["yn_claim"])])
    assert reg.status(fid) == "rejected" and not reg.gate()["pass"]
    with pytest.raises(Exception):
        F.record_reads(reg, [_read("read2", reg, FX.QUESTION_MEANINGS["ch_value"])])      # no re-vote by the same extractor
    assert reg.status(fid) == "rejected"


def test_glex_a_text_that_is_no_meaning_is_a_rejected_pick():
    reg = _reg()
    fid = next(iter(reg.forms))
    F.record_reads(reg, [_read("read1", reg, FX.QUESTION_MEANINGS["ch_value"]), _read("read2", reg, "no such meaning")])
    assert reg.status(fid) == "rejected"


def test_strict_kinds_need_three_reads_in_the_kit():
    reg = LexiconRegistry("T99")
    reg.declare("prec.P1", "precedence", "deny beats allow")
    f = reg.add("deny rules beat allow rules", "prec.P1")
    reg.unit_test_all()
    assert f.required == 3                                       # freeze_v2 admits by LexiconRegistry.status: 3/3 there
    reg.record_extraction(f.form_id, "a", "prec.P1")
    reg.record_extraction(f.form_id, "b", "prec.P1")
    assert reg.status(f.form_id) == "pending"
    reg.record_extraction(f.form_id, "c", "prec.P1")
    assert reg.status(f.form_id) == "admitted"


@pytest.fixture(scope="module")
def v1_docs():
    items = json.loads((F.POOLS_V1 / "documents_mode_f.json").read_text())["items"]
    skins = json.loads((F.POOLS_V1 / "skins_mode_t.json").read_text())["items"]
    return items, dict(Counter(s["register"] for s in skins))


def test_g3h_stage_on_the_real_answers(v1_docs):
    docs, mode_t = v1_docs
    usable = {"T25-extract_g3h-34177cc1-000", "T25-extract_g3h-34177cc1-001"}
    g = F.g3h_stage(docs, mode_t, usable)
    ev = g["ev"]
    assert g["batch_files_differ_from_disk"] == []
    assert (ev["n"], ev["pass"], ev["quarantined_g3h"], ev["answer_problems"]) == (84, 84, [], [])
    assert len(ev["admitted"]) == 61 and len(ev["cut_by_cap"]) == 23
    assert len(g["votes"]) == 84 and all(v["match"] and v["answered"] and v["extractor"] == "g3h-r1" for v in g["votes"])
    assert {v["task_id"] for v in g["votes"]} == usable
    for reg, c in ev["cap"].items():
        assert c["cap"] == c["mode_t"] // 4 and c["admitted"] <= c["cap"]
        assert c["mode_f_share"] <= 0.20


def test_g3h_an_unusable_answer_file_leaves_its_documents_unread(v1_docs):
    docs, mode_t = v1_docs
    g = F.g3h_stage(docs, mode_t, {"T25-extract_g3h-34177cc1-000"})                  # the other file is rejected or ignored
    ev = g["ev"]
    assert ev["answer_problems"] and ev["pass"] == 42 and len(ev["quarantined_g3h"]) == 42
    assert not any(v["answered"] for v in g["votes"] if v["task_id"].endswith("-001"))
    assert set(ev["admitted"]).isdisjoint(ev["quarantined_g3h"])


def test_g3h_a_changed_extraction_quarantines_the_document(v1_docs, monkeypatch):
    docs, mode_t = v1_docs
    BR = F.build_redo2()
    real = BR.chunker.load_answers

    def wrong_first(batch, raw):
        out, probs = real(batch, raw)
        first = sorted(out)[0]
        out[first] = dict(out[first], org="Somebody Else")
        return out, probs
    monkeypatch.setattr(BR.chunker, "load_answers", wrong_first, raising=True)
    monkeypatch.setattr(F.chunker, "load_answers", wrong_first, raising=True)
    g = F.g3h_stage(docs, mode_t, {"T25-extract_g3h-34177cc1-000", "T25-extract_g3h-34177cc1-001"})
    assert len(g["ev"]["quarantined_g3h"]) == 1 and g["ev"]["pass"] == 83


def test_h27_cross_lint_flags_a_tier_word_in_a_pack_string():
    tw = frozenset({"gold", "silver", "teal"})
    hits = F.h27_cross_lint({"attr_label": ["gold deposit", "late fee"], "asker": ["Teal Brandt"]}, tw)
    assert [(p, s) for p, s, _w in hits] == [("attr_label", "gold deposit"), ("asker", "Teal Brandt")]
    assert F.h27_cross_lint({"source_noun": ["help page"]}, tw) == []


# ------------------------------------------------------------------------------------------------ the freeze
def test_v1_state_is_untouched_and_g0_moved():
    v1 = F.v1_state()
    assert v1["unchanged"] and v1["files_changed"] == [] and v1["inputs_changed"] == [] and v1["extra_files"] == []
    assert v1["g0_v1_sha256"] == S6.G0_PIN and v1["g0_now_sha256"] == F.G0_PIN != v1["g0_v1_sha256"]


def test_verdict_is_ready_with_every_gate_met(built):
    s = built["summary"]
    assert built["verdict"] == "READY" and s["shortfalls"] == [] and s["issues"] == []
    hard = [r for r in s["table"] if r["kind"] in ("G0 target", "G0 cap", "gate")]
    assert hard and all(r["met"] for r in hard)
    assert any(r["item"].startswith("G-LEX") for r in hard)
    glex = next(r for r in hard if r["item"].startswith("G-LEX"))
    assert glex["got"] == {"admitted": 138} and "{2: 138}" in glex["note"]
    assert files_of(built, "MANIFEST.json")["verdict"] == "READY"


def test_every_g0_minimum_is_in_the_table_with_the_unlowered_target(built):
    t = {r["item"]: r for r in built["summary"]["table"]}
    assert t["attribute packs (one per card)"]["target"] == 30 and t["attribute packs (one per card)"]["got"] == 60
    assert t["source nouns (after B1)"]["target"] == 40 and t["source nouns (after B1)"]["got"] == 93
    assert t["tier schemes"]["target"] == 8 and t["question wordings admitted"]["target"] == 30
    for q in FX.QUESTION_MEANINGS:
        assert t[f"question wordings {q}"]["target"] == 4 and t[f"question wordings {q}"]["met"]
    assert t["training registers (Mode T)"]["got"] == 8 and t["held-out registers"]["got"] == 2
    assert t["yn_claim_dneg wordings (H12)"]["got"] >= 2


def test_rulings_b1_b2_b3(built):
    man = files_of(built, "MANIFEST.json")
    assert man["rulings"]["B1_nouns_quarantined"] == ["memo"]
    assert man["rulings"]["B2_wordings_quarantined"] == [Y]
    assert len(man["rulings"]["B3_documents_cut_by_cap"]) == 23 and man["rulings"]["B3_documents_quarantined_g3h"] == []
    rec = json.loads((HERE / "haiku" / "redo2" / "results" / "rulings_v3.json").read_text())
    assert rec["source_nouns_quarantine"] == ["memo"] and rec["wordings_quarantine"] == [Y]
    assert sorted(rec["documents_mode_f_cut_by_cap"]) == man["rulings"]["B3_documents_cut_by_cap"]
    nouns = files_of(built, "source_nouns.json")
    assert "memo" not in nouns["items"] and nouns["n"] == 93
    words = files_of(built, "wordings.json")
    assert words["n"] == 138 and Y not in {w["form_id"] for w in words["items"]}
    lex = files_of(built, "lexicon.json")
    assert Y not in {f["form_id"] for f in lex["forms"]} and len(lex["forms"]) == 138
    assert all(f["status"] == "admitted" and len({e[0] for e in f["extractions"]}) == 2 for f in lex["forms"])
    assert sorted(set(files_of(built, "documents_mode_f.json")["items"][0]) & {"g3h", "status"}) == ["g3h", "status"]
    q = files_of(built, "QUARANTINE.json")
    assert q["n"] == 67 and q["freeze_v1"] == 42 and q["freeze_v2"] == 25
    assert any(x["piece"] == Y and x["pool"] == "wordings" for x in q["items"])
    assert any(x["piece"] == "memo" and x["pool"] == "source_nouns" for x in q["items"])


def test_mode_f_cap_and_register_shares(built):
    docs = files_of(built, "documents_mode_f.json")["items"]
    skins = files_of(built, "skins_mode_t.json")["items"]
    f, t = Counter(d["register"] for d in docs), Counter(s["register"] for s in skins)
    assert sum(f.values()) == 61 and set(f) <= set(t)
    for r, n in f.items():
        assert n / (n + t[r]) <= 0.20 and n == min(n, t[r] // 4)
    assert sum(f.values()) / (sum(f.values()) + sum(t.values())) <= 0.25
    assert max(t.values()) / sum(t.values()) <= 0.15
    held = {s["register"] for s in skins if s["held_out"]}
    assert held == {"wiki_talk", "audit_note"} and len(set(t) - held) == 8
    assert all(not d["held_out"] or d["register"] in held for d in docs)


def test_v2_pieces_all_come_from_v1_unchanged(built):
    def v1(name):
        return json.loads((F.POOLS_V1 / name).read_text())["items"]
    v1_skins = {s["id"]: s for s in v1("skins_mode_t.json")}
    for s in files_of(built, "skins_mode_t.json")["items"]:
        o = v1_skins[s["id"]]
        assert all(s[k] == o[k] for k in o) and s["haiku_task_id"] and len(s["haiku_prompt_sha"]) == 64
    v1_att = {a["id"]: a for a in v1("attacks.json")}
    for a in files_of(built, "attacks.json")["items"]:
        assert all(a[k] == v1_att[a["id"]][k] for k in v1_att[a["id"]]) and a["haiku_task_id"]
    v1_doc = {d["id"]: d for d in v1("documents_mode_f.json")}
    for d in files_of(built, "documents_mode_f.json")["items"]:
        o = v1_doc[d["id"]]
        assert d["text"] == o["text"] and d["facts"] == o["facts"] and d["haiku_task_id"] and d["status"] == "admitted"
    for name in ("attr_packs", "organisations", "askers", "tier_schemes"):
        assert files_of(built, f"{name}.json")["items"] == v1(f"{name}.json")
    assert set(files_of(built, "source_nouns.json")["items"]) == set(v1("source_nouns.json")) - {"memo"}
    v1_w = {w["form_id"]: w for w in v1("wordings.json")}
    for w in files_of(built, "wordings.json")["items"]:
        assert all(w[k] == v1_w[w["form_id"]][k] for k in ("qform", "text", "slots", "haiku_task_id", "haiku_prompt_sha",
                                                          "extractions"))


def test_manifest_hashes_match_the_files_and_the_inputs(built):
    man = files_of(built, "MANIFEST.json")
    assert set(man["files"]) == set(built["files"]) - {"MANIFEST.json"}
    for r, meta in man["files"].items():
        assert F.sha_text(built["files"][r]) == meta["sha256"] and len(built["files"][r].encode()) == meta["bytes"]
    assert man["binding"]["G0_SPEC_sha256"] == F.G0_PIN and man["binding"]["G0_pin_match"]
    assert man["binding"]["v1_unchanged"] and man["binding"]["g0_moved_v2_to_v3"]
    assert man["binding"]["producer_script_sha256"] == F.sha_file(Path(F.__file__))
    for r, meta in man["inputs"].items():
        assert F.sha_file(F.G0 if r == "G0_SPEC.md" else HERE / r) == meta["sha256"], r
    assert "haiku/redo2/answers/T25-extract_g3h-34177cc1-000.json" in man["inputs"]
    assert "haiku/extract/answers/T25-extract_lex-0c8f84c6-000.json" in man["inputs"]
    assert man["loading"]["plugin_reads_pools"] is False
    assert "ohs" not in " ".join(built["files"]).lower() and "jev" not in " ".join(built["files"]).lower()


def test_no_label_or_gold_field_enters_the_pools(built):
    blob = " ".join(built["files"].values()).lower()
    for bad in ('"gold"', '"label"', '"answer"', '"expected"'):
        assert bad not in blob, bad
    assert "ANSWER_VALIDATION.json" in built["files"] and "g3h.json" in built["files"]


# ------------------------------------------------------------------------------------------------ writer, loader, consumer
def test_writer_is_write_once_and_the_loader_verifies(built, scratch):
    w = F.write_pools(built, scratch)
    assert set(w) == set(built["files"]) and (scratch / "MANIFEST.json").is_file()
    assert F.check_pools(built, scratch) == []
    assert F.write_pools(built, scratch) == w                                         # identical freeze: a no-op
    other = {"files": dict(built["files"], **{"askers.json": built["files"]["askers.json"] + " "}), "v1": built["v1"]}
    with pytest.raises(SystemExit):
        F.write_pools(other, scratch)                                                 # never overwrites a different freeze
    pools = F.load_pools_v2(scratch)
    assert pools["manifest"]["verdict"] == "READY" and pools["wordings"]["n"] == 138
    p = scratch / "askers.json"
    good = p.read_text()
    p.write_text(good.replace("Priya", "Priyu", 1) if "Priya" in good else good + " ")
    with pytest.raises(ValueError):
        F.load_pools_v2(scratch)
    assert F.check_pools(built, scratch) == ["askers.json"]
    p.write_text(good)
    assert F.check_pools(built, scratch) == []
    assert F.v1_state()["unchanged"]


def test_loader_refuses_a_short_freeze_unless_asked(built, scratch):
    man = json.loads(built["files"]["MANIFEST.json"])
    man["verdict"] = "SHORT"
    man["shortfalls"] = [{"item": "x"}]
    (scratch / "MANIFEST.json").write_text(json.dumps(man))
    with pytest.raises(ValueError):
        F.load_pools_v2(scratch)
    assert F.load_pools_v2(scratch, require_ready=False)["manifest"]["verdict"] == "SHORT"
    shutil.rmtree(scratch)
    F.write_pools(built, scratch)


def test_kit_ctx_runs_real_pools_through_the_pipeline(built, scratch):
    if not (scratch / "MANIFEST.json").is_file():
        F.write_pools(built, scratch)
    ctx = F.kit_ctx(F.load_pools_v2(scratch))
    kinds = Counter((s.kind, s.author_mode) for s in ctx.skins.values())
    assert kinds == {("skin", "T"): 334, ("skin", "F"): 61, ("attack", "T"): 45, ("wording", "T"): 138}
    assert ctx.lexicon.gate()["pass"] and len(ctx.lexicon.forms) == 138
    assert all(s.haiku_task_id and s.haiku_prompt_sha for s in ctx.skins.values())
    held = {s.register for s in ctx.skins.values() if s.kind == "skin" and s.held_out}
    assert held == {"wiki_talk", "audit_note"}
    assert ctx.pick("T25", "skin", "k", register="json").escape == "json"
    assert ctx.pick("T25", "skin", "k", register="yaml").escape == "yaml"
    plugin = P.T25(lexicon=ctx.lexicon)
    ok, bad = 0, []
    for smp in ("S1", "S2", "S3", "S4", "S5"):
        for seed in range(6):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed == 0))
            ok += res.ok
            if not res.ok:
                bad.append((smp, seed, res.problems[:1]))
    assert not bad, bad
    assert ok == 30


def test_wired_plugin_runs_all_pool_data_through_the_pipeline(built, scratch):
    if not (scratch / "MANIFEST.json").is_file():
        F.write_pools(built, scratch)
    pools = F.load_pools_v2(scratch)
    ctx = F.kit_ctx(pools)
    names = ("PACKS", "PACK_KEYS", "SCHEMES", "SCHEME_KEYS", "ORGS", "ASKERS", "SOURCE_NAMES")
    before = {k: getattr(P, k) for k in names}
    packs = F.plugin_packs(pools)
    assert len(packs) == 60 and all(isinstance(p, P.Pack) for p in packs.values())
    assert Counter(p.kind for p in packs.values()) == {"cents": 22, "date": 16, "count": 22}
    assert all(p.unit and p.unit[0] in {u[0] for u in HA.UNITS} for p in packs.values() if p.kind == "count")
    assert len(F.plugin_schemes(pools)) == 15
    with F.wired_plugin(pools):
        assert P.PACKS == packs and len(P.ORGS) == 60 and len(P.ASKERS) == 59 and len(P.SOURCE_NAMES) == 93
        assert "memo" not in P.SOURCE_NAMES
        plugin = P.T25(lexicon=ctx.lexicon)
        ok, bad, mode_f, rows = 0, [], 0, 0
        for smp in ("S1", "S2", "S3", "S4", "S5"):
            for seed in range(10):
                res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
                ok += res.ok
                if not res.ok:
                    bad.append((smp, seed, res.problems[:1]))
                for rr in res.rendered if res.ok else ():
                    rows += 1
                    mode_f += ctx.skin(rr.skin_id).author_mode == "F"
        assert not bad, bad
        assert ok == 50 and rows > 50 and 0 < mode_f < rows
    assert {k: getattr(P, k) for k in names} == before                                # every constant restored
    with pytest.raises(RuntimeError):
        with F.wired_plugin(pools):
            raise RuntimeError("boom")
    assert {k: getattr(P, k) for k in names} == before                                # also after an error


def test_pools_v2_on_disk_equals_a_rebuild_when_written(built):
    if not (F.POOLS_V2 / "MANIFEST.json").is_file():
        pytest.skip("pools_v2 is not written yet")
    assert F.check_pools(built) == []
    assert F.load_pools_v2()["manifest"]["verdict"] == "READY"
