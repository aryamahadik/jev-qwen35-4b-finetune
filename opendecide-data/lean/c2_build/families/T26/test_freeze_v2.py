"""c2_build/families/T26/test_freeze_v2.py: tests for freeze_v2.py (the T26 pools_v2 re-freeze).

Covers: the answer-file contract (a file that breaks it is rejected whole, an item that breaks it alone; nothing is
edited); the redo / redo2 task parsers; the effective author answers (redo replaces the original); the redo2 wording
lint and dedup; G-LEX vote recording (2/2 admits, a mismatch rejects for good, one read stays pending, held_out kept);
the G0 targets (pinned: never lowered) and the exact shortfalls; the whole freeze in memory over the real folders
(v1 reproduced byte for byte where redo2 cannot change it, v1 untouched, nothing written by `check`); the READY path with
simulated reads (in memory only: no read answer is ever written by a test); and, when pools_v2/ exists, its manifest.

Run (from lean/):  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
                   c2_build/families/T26/test_freeze_v2.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T26 import fixtures as FX  # noqa: E402
from families.T26 import freeze_v2 as FZ  # noqa: E402
from families.T26 import plugin as P  # noqa: E402


def cdef(kind, qids, **kw):
    return FZ.ChunkDef("T26-test-000", kind, "pool", list(qids), **kw)


def raw(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def text_ans(qids, **over):
    return [{"qid": q, "text": over.get(q, f"text for {q}")} for q in qids]


# ======================================================================================== the answer contract

def test_a_valid_text_file_is_accepted_in_full():
    cd = cdef("author_wording", ["qa", "qb"])
    r = FZ.validate_answer_bytes(raw(text_ans(["qb", "qa"])), cd)
    assert r["ok"] and r["n_valid_items"] == 2 and not r["file_problems"] and not r["item_problems"]


@pytest.mark.parametrize("answers, why", [
    ([{"qid": "qa", "text": "x", "extra": 1}, {"qid": "qb", "text": "y"}], "keys"),
    ([{"qid": "qa"}, {"qid": "qb", "text": "y"}], "keys"),
    ([{"qid": "qa", "txt": "x"}, {"qid": "qb", "text": "y"}], "keys"),
    ([{"qid": "qa", "text": "x"}, {"qid": "qa", "text": "y"}], "twice"),
    ([{"qid": "qa", "text": "x"}, {"qid": "qzz", "text": "y"}], "unknown"),
    ([{"qid": "qa", "text": "x"}], "objects"),
    ([{"qid": "qa", "text": "x"}, {"qid": "qb", "text": "y"}, {"qid": "qb", "text": "z"}], "objects"),
    ([{"qid": 1, "text": "x"}, {"qid": "qb", "text": "y"}], "qid"),
    (["qa", "qb"], "not an object"),
])
def test_a_contract_break_rejects_the_whole_file(answers, why):
    r = FZ.validate_answer_bytes(raw(answers), cdef("author_wording", ["qa", "qb"]))
    assert not r["ok"] and r["n_valid_items"] == 0 and r["file_problems"]
    assert why in " ".join(r["file_problems"])


@pytest.mark.parametrize("data", [
    b"", b"not json", b'```json\n[{"qid": "qa", "text": "x"}]\n```', b'{"answers": []}', b'"qa"',
    b'\xef\xbb\xbf[{"qid": "qa", "text": "x"}]', b"\xff\xfe", b'[{"qid": "qa", "qid": "qb", "text": "x"}]',
    b'[{"qid": "qa", "text": NaN}]'])
def test_unparseable_or_wrapped_files_are_rejected(data):
    r = FZ.validate_answer_bytes(data, cdef("author_wording", ["qa"]))
    assert not r["ok"] and r["file_problems"]


def test_item_level_breaks_reject_only_that_item():
    cd = cdef("author_wording", ["qa", "qb", "qc", "qd"], one_line=True)
    ans = [{"qid": "qa", "text": "fine?"}, {"qid": "qb", "text": "  "}, {"qid": "qc", "text": 5},
           {"qid": "qd", "text": "two\nlines?"}]
    r = FZ.validate_answer_bytes(raw(ans), cd)
    assert r["ok"] and r["n_valid_items"] == 1 and [i["qid"] for i in r["items"]] == ["qa"]
    assert len(r["item_problems"]) == 3
    # the same line break is fine when the task does not say one line (a skin or a document)
    r2 = FZ.validate_answer_bytes(raw([{"qid": "qd", "text": "two\nlines"}]), cdef("author_skin", ["qd"]))
    assert r2["ok"] and r2["n_valid_items"] == 1


def test_a_lex_read_must_pick_one_of_the_items_choices_or_none():
    cd = cdef("extract_lex", ["qa", "qb", "qc"], choices={"qa": ["m1", "m2"], "qb": ["m1", "m2"], "qc": ["m1", "m2"]})
    r = FZ.validate_answer_bytes(raw([{"qid": "qa", "meaning": "m1"}, {"qid": "qb", "meaning": "NONE"},
                                      {"qid": "qc", "meaning": "something else"}]), cd)
    assert r["ok"] and r["n_valid_items"] == 2 and len(r["item_problems"]) == 1
    assert {i["qid"] for i in r["items"]} == {"qa", "qb"}


def test_g3h_and_pack_contracts():
    g = cdef("extract_g3h", ["qa", "qb"])
    ok = [{"qid": "qa", "requester": "A B", "counterparty": "C D", "change": "x", "req_id": "BK-10000"},
          {"qid": "qb", "requester": "A B", "counterparty": None, "change": None, "req_id": "BK-10001"}]
    r = FZ.validate_answer_bytes(raw(ok), g)
    assert r["ok"] and r["n_valid_items"] == 2                         # null = "the text does not state it"
    ok[0]["req_id"] = ""
    assert FZ.validate_answer_bytes(raw(ok), g)["n_valid_items"] == 1
    short = [{"qid": "qa", "requester": "A B", "counterparty": "C D", "change": "x"}, ok[1]]
    assert not FZ.validate_answer_bytes(raw(short), g)["ok"]
    pk = cdef("author_pack", ["qa"])
    assert FZ.validate_answer_bytes(raw([{"qid": "qa", "counterparty": "Acme Freight", "domain_label": "acmefr"}]), pk)["ok"]
    assert not FZ.validate_answer_bytes(raw([{"qid": "qa", "counterparty": "Acme Freight"}]), pk)["ok"]


def test_validate_round_flags_missing_stray_and_never_edits(tmp_path):
    if paths.never_open(tmp_path):
        pytest.skip("pytest tmp folder is on the never-open list")
    defs = {"T-1": FZ.ChunkDef("T-1", "author_wording", "p", ["qa"]), "T-2": FZ.ChunkDef("T-2", "author_wording", "p", ["qb"]),
            "T-3": FZ.ChunkDef("T-3", "author_wording", "p", ["qc"])}
    good = raw([{"qid": "qa", "text": "x"}])
    bad = b"oops"
    (tmp_path / "T-1.json").write_bytes(good)
    (tmp_path / "T-2.json").write_bytes(bad)
    (tmp_path / "stray.json").write_bytes(good)
    (tmp_path / "notes.txt").write_bytes(b"hi")
    rep = FZ.validate_round("t", defs, tmp_path)
    assert rep["rejected"] == ["T-2"] and rep["missing"] == ["T-3"] and rep["stray"] == ["notes.txt", "stray.json"]
    assert list(FZ.accepted(rep)) == ["T-1"]
    assert hashlib.sha256((tmp_path / "T-2.json").read_bytes()).hexdigest() == rep["files"]["T-2"]["sha256"]
    assert (tmp_path / "T-2.json").read_bytes() == bad and (tmp_path / "T-1.json").read_bytes() == good
    slim = FZ.slim(rep)
    assert all("items" not in f for f in slim["files"].values())


def test_task_text_parsers_read_the_real_redo_and_redo2_tasks():
    r2 = json.loads((FZ.REDO2 / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    for t in r2:
        cd = FZ.def_from_task_text(Path(t["task_file"]), t["pool"])
        assert cd.task_id == Path(t["task_file"]).stem and cd.kind == "author_wording"
        assert len(cd.qids) == t["n_items"] == len(set(cd.qids)) and cd.one_line
        assert cd.answer_file == t["answer_file"]
    rd = json.loads((FZ.REDO / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    for t in rd:
        cd = FZ.def_from_task_text(Path(t["task_file"]), t["pool"])
        assert cd.task_id == Path(t["task_file"]).stem and cd.kind == "author_skin" and not cd.one_line
        assert len(cd.qids) == t["n_items"] and cd.answer_file == t["answer_file"]
        src = json.loads(Path(t["source_chunk"]).read_text(encoding="utf-8"))
        assert [i["qid"] for i in src["items"]] == cd.qids          # same items and opaque qids as the source chunk


def test_a_valid_redo_answer_replaces_the_original_and_a_bad_one_falls_back():
    def rep(files):
        return {"files": {t: {"ok": ok, "items": [{"qid": t}] if ok else [], "sha256": sha} for t, (ok, sha) in files.items()}}
    a = rep({"T1": (True, "a1"), "T2": (True, "a2"), "T3": (True, "a3")})
    r = rep({"T1": (True, "a1"), "T2": (True, "NEW"), "T3": (False, "bad")})
    raw_, src, notes = FZ.effective_author_answers(a, r)
    assert src == {"T1": "redo", "T2": "redo", "T3": "author"}
    assert any("T2" in n and "differs" in n for n in notes) and any("T3" in n and "rejected" in n for n in notes)
    # a redo task whose original is gone: the redo answer alone
    raw2, src2, _ = FZ.effective_author_answers(rep({}), rep({"T9": (True, "x")}))
    assert src2 == {"T9": "redo"}
    raw3, src3, notes3 = FZ.effective_author_answers(rep({"T4": (False, "x")}), rep({}))
    assert raw3 == {} and src3 == {}


# ======================================================================================== redo2 lint and dedup

def piece(iid, text, qf, held):
    return {"pool": "wording_heldout" if held else "wording", "internal_id": iid, "problems": [], "held_out": held,
            "answer": {"text": text}, "meta": {"qform": qf}}


def test_r2_dedup_against_stand_ins_first_pass_and_itself():
    stand_in = FX.WORDINGS[0][2]
    taken = {FZ.AI._norm("Does any listed check on its provided record fail for request {REQ_ID}?")}
    ps = [piece("t26|wording|yn_fails|100", stand_in, "yn_apply", False),
          piece("t26|wording|yn_fails|101", "Does any listed check on its provided record fail for request {REQ_ID}?",
                "yn_fails", False),
          piece("t26|wording_ho|yn_apply|000", "Should the agent apply the change in request {REQ_ID}?", "yn_apply", True),
          piece("t26|wording_ho|yn_apply|001", "Should the agent  apply the change in request {REQ_ID}?", "yn_apply", True),
          piece("t26|wording_ho|yn_apply|002", "By the card, should the agent apply the change in request {REQ_ID}?",
                "yn_apply", True)]
    FZ.r2_lint_dedup(ps, taken)
    probs = {p["internal_id"]: p["problems"] for p in ps}
    assert any("fixture stand-in" in x for x in probs["t26|wording|yn_fails|100"])
    assert any("first-pass" in x for x in probs["t26|wording|yn_fails|101"])
    # the second copy is the one dropped (training sorts before held-out, then by id); normalisation ignores spacing
    assert probs["t26|wording_ho|yn_apply|000"] == []
    assert any("repeats" in x for x in probs["t26|wording_ho|yn_apply|001"])
    assert probs["t26|wording_ho|yn_apply|002"] == []


def test_r2_same_text_under_two_question_forms_drops_every_redo2_copy():
    t = "Does every listed check whose record is provided pass for request {REQ_ID}?"
    ps = [piece("t26|wording|yn_fails|100", t, "yn_clears", False), piece("t26|wording_ho|yn_apply|000", t, "yn_apply", True)]
    FZ.r2_lint_dedup(ps, set())
    assert all(any("repeats" in x or "two question forms" in x for x in p["problems"]) for p in ps[1:])
    # the training copy (first by sort order) is kept by the repeat rule, then dropped by the ambiguity rule too
    assert any("two question forms" in x for x in ps[0]["problems"]) or ps[0]["problems"] == []


def test_r2_lint_is_the_unchanged_wording_lint():
    ps = [piece("t26|wording|yn_fails|100", "Does any listed check fail for request {REQ_ID}, when not verified?", "yn_fails", False),
          piece("t26|wording|yn_fails|101", "Does any listed check whose record is provided fail on request {REQ_ID}?",
                "yn_fails", False)]
    FZ.r2_lint_dedup(ps, set())
    assert ps[0]["problems"] and not ps[1]["problems"]          # negation / unverifiable wording is refused, the scoped one passes


# ======================================================================================== G-LEX votes

def mkreg():
    return P.declare_lexicon(LexiconRegistry(FZ.FAMILY))


def add(reg, text, qf, held=False):
    f = reg.add(text, question_sem(FZ.FAMILY, qf), slots={"REQ_ID": "id"}, source="haiku", family=FZ.FAMILY,
                haiku_task_id="T26-test-000", haiku_prompt_sha="0" * 64, held_out=held)
    assert reg.unit_test(f.form_id)
    return f.form_id


def reads_for(reg, batches, plan):
    """plan: {(read name, form id): meaning text | None (leave unanswered)} -> accepted raw {task id: items}."""
    out = {}
    for name, b in batches:
        for c in b.chunks:
            items = []
            for it in c["items"]:
                fid = b.key[it["qid"]]
                pick = plan.get((name, fid), "own")
                if pick is None:
                    continue
                if pick == "own":
                    pick = reg.sems[reg.forms[fid].sem_id].meaning
                items.append({"qid": it["qid"], "meaning": pick})
            out[c["task_id"]] = items
    return out


def test_glex_two_of_two_admits_a_mismatch_rejects_and_one_read_stays_pending(tmp_path):
    reg = mkreg()
    a = add(reg, "Does any listed check whose record is provided fail on request {REQ_ID}?", "yn_fails")
    b = add(reg, "For request {REQ_ID}, does any listed check on its provided record fail?", "yn_fails", held=True)
    c = add(reg, "Is any listed check on its provided record found to fail for request {REQ_ID}?", "yn_fails")
    d = add(reg, "Concerning request {REQ_ID}, does a listed check whose record is provided fail?", "yn_fails")
    batches = FZ.r2_read_batches(reg, [a, b, c, d], root=tmp_path / "x")
    assert [n for n, _ in batches] == ["glex-question-r2read1", "glex-question-r2read2"]
    decoy = reg.sems["q.t26.decoy_all_clear"].meaning
    plan = {("glex-question-r2read2", b): decoy,            # one disagreeing read rejects for good
            ("glex-question-r2read2", c): None,            # no second read: pending
            ("glex-question-r2read1", d): "NONE", ("glex-question-r2read2", d): "own"}
    out = FZ.record_reads(reg, batches, reads_for(reg, batches, plan))
    assert [o["read"] for o in out] == ["glex-question-r2read1", "glex-question-r2read2"]
    assert reg.status(a) == "admitted" and reg.status(b) == "rejected"
    assert reg.status(c) == "pending" and reg.status(d) == "rejected"
    assert reg.forms[b].held_out and not reg.forms[a].held_out
    assert reg.forms[a].required == 2
    assert {e for e, _ in reg.forms[a].extractions} == {"glex-question-r2read1", "glex-question-r2read2"}
    gate = reg.gate(used_form_ids=[a])
    assert gate["pass"] and not reg.gate(used_form_ids=[a, b, c])["pass"]


def test_each_read_is_a_separate_batch_with_the_unchanged_prompt_and_choices(tmp_path):
    reg = mkreg()
    fids = [add(reg, "Does any listed check whose record is provided fail on request {REQ_ID}?", "yn_fails"),
            add(reg, "Should the agent apply the requested change for request {REQ_ID}?", "yn_apply")]
    batches = FZ.r2_read_batches(reg, fids, root=tmp_path)
    (n1, b1), (n2, b2) = batches
    assert b1.batch_id != b2.batch_id and set(b1.task_of.values()).isdisjoint(b2.task_of.values())
    assert b1.prompt == b2.prompt == FZ.AI.LEX_PROMPT
    kinds = {s.meaning for s in reg.sems.values() if s.kind == "question"}
    for _, b in batches:
        for c in b.chunks:
            assert c["answer_file"].startswith(str(tmp_path / "answers"))
            for it in c["items"]:
                assert set(it["choices"]) == kinds and len(kinds) == 12     # 8 declared meanings + 4 decoys
                assert not any(iid in json.dumps(c) for iid in b.key.values())


# ======================================================================================== targets

def full_inputs(**over):
    kw = dict(packs_train=54, packs_ho=6, train_regs=list(FZ.AI.AT.TRAIN_REGISTERS), ho_regs=["it_chat", "forwarded_thread"],
              prec_n=26, train_by_form=dict(FZ.TARGET["wording_per_form"]), ho_by_form={f: 3 for f in FZ.FORMS},
              mode_t=465, mode_f=127)
    kw.update(over)
    return kw


def test_the_g0_targets_are_pinned_and_never_lowered():
    assert FZ.TARGET["wording_per_form"] == {"yn_apply": 9, "yn_hold": 6, "yn_not_apply": 4, "yn_dneg_apply": 2,
                                             "yn_fails": 6, "yn_clears": 5, "ch_verdict": 16, "ch_failing": 6}
    assert (FZ.TARGET["packs_training"], FZ.TARGET["packs_heldout"]) == (25, 6)
    assert (FZ.TARGET["skin_registers_training"], FZ.TARGET["skin_registers_heldout"]) == (8, 2)
    assert FZ.TARGET["precedence_admitted"] == 6 and FZ.TARGET["mode_f_max_share"] == 0.25
    assert FZ.HELD_OUT_PER_FORM == 3 and len(FZ.FORMS) == 8 and FZ.MODE_T_MIN_SHARE == 0.75


def test_targets_all_met_has_no_shortfall_and_each_miss_is_exact():
    targets, short = FZ.evaluate_targets(**full_inputs())
    assert short == [] and all(t["pass"] for g in targets.values() for t in g.values())
    _, short = FZ.evaluate_targets(**full_inputs(
        train_by_form={**FZ.TARGET["wording_per_form"], "yn_fails": 0}, ho_by_form={**{f: 3 for f in FZ.FORMS}, "yn_hold": 1},
        cand_train={"yn_fails": 16}, cand_ho={"yn_hold": 2}, packs_ho=5))
    by = {x["target"]: x for x in short}
    assert by["wording yn_fails (training)"]["short_by"] == 6 and by["wording yn_fails (training)"]["pending_reads"] == 16
    assert by["held-out wording yn_hold (sampler S5)"]["short_by"] == 2
    assert by["held-out wording yn_hold (sampler S5)"]["pending_reads"] == 2
    assert by["packs held-out"]["short_by"] == 1
    assert by["wording total, training (sum of per-form bars)"]["short_by"] == 6
    assert by["held-out wordings, all forms"]["short_by"] == 2
    _, short = FZ.evaluate_targets(**full_inputs(mode_t=300, mode_f=200))
    assert any(x["target"].startswith("Mode T / Mode F") for x in short)


# ======================================================================================== the freeze over the real folders

def tree(root: Path) -> dict:
    return {str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime_ns) for p in sorted(root.rglob("*")) if p.is_file()}


@pytest.fixture(scope="module")
def built():
    before_v1 = tree(FZ.V1_POOLS)
    before = tree(FZ.HERE)
    s = FZ.build()
    summary = FZ.summarize(s, write=False)
    assert tree(FZ.V1_POOLS) == before_v1                       # v1 untouched
    assert tree(FZ.HERE) == before                              # build + summarize wrote nothing at all
    return s, summary


def test_every_check_holds_and_the_answers_on_disk_are_what_the_rebuild_expects(built):
    s, summary = built
    assert summary["a38_frozen"] is True
    assert all(v in (True, None) for v in s.checks.values()), s.checks
    assert not s.missing_author
    assert set(s.rounds) >= {"author", "redo", "extract", "redo2_author", "redo2_extract"}
    for name in ("author", "redo", "extract", "redo2_author"):
        assert not s.rounds[name]["missing"], name


def test_v1_is_reproduced_wherever_redo2_cannot_change_it(built):
    s, summary = built
    cmp_ = summary["v1_comparison"]
    if not s.rounds["author"]["rejected"] and not s.rounds["extract"]["rejected"]:
        for rel in ("packs.json", "skins.json", "attack.json", "precedence.json", "documents.json"):
            assert cmp_[rel]["identical_to_v1"] and cmp_[rel]["v1_file_matches_its_manifest"], rel
        assert cmp_["wordings.json"]["every_v1_wording_kept_unchanged"]
        assert cmp_["lexicon.json"]["every_v1_form_kept_unchanged"]
        assert cmp_["quarantine.json"]["every_v1_entry_kept_unchanged"]
    v1_reads = json.loads((FZ.V1_POOLS / "quarantine.json").read_text(encoding="utf-8"))["reads"]
    mine = [r for r in s.v1_reads]
    assert [(r["read"], r["batch_id"], r["items"], r["outcomes"]) for r in v1_reads] == \
           [(r["read"], r["batch_id"], r["items"], r["outcomes"]) for r in mine]


def test_redo2_forms_are_registered_flagged_and_never_admitted_without_two_reads(built):
    s, _ = built
    ok = [p for p in s.p2 if not p["problems"]]
    assert ok and all("form_id" in p for p in ok)
    for p in ok:
        f = s.reg.forms[p["form_id"]]
        assert f.held_out == (p["pool"] == "wording_heldout") and f.kind == "question" and f.required == 2
        votes = {e for e, _ in f.extractions}
        if len(votes) >= 2 and all(m == f.sem_id for _, m in f.extractions):
            assert s.status[p["form_id"]] == "admitted"
        else:
            assert s.status[p["form_id"]] != "admitted"
    kept = s.kept["wording"]
    ho_tasks = {p["task_id"] for p in s.p2 + s.p3 if p["pool"] == "wording_heldout"}       # redo2 and redo3 held-out tasks
    assert ho_tasks and all(w["held_out"] == (w["task_id"] in ho_tasks) for w in kept)
    ho_texts = {FZ.AI._norm(w["text"]) for w in kept if w["held_out"]}
    tr_texts = {FZ.AI._norm(w["text"]) for w in kept if not w["held_out"]}
    assert not ho_texts & tr_texts
    assert all(p["pool"] != "wording_heldout" or p["held_out"] for p in s.p2)


def test_ready_matches_the_targets_and_gates(built):
    s, summary = built
    assert summary["ready"] == s.ready
    assert s.ready == (not s.shortfalls and s.gate_used["pass"] and s.g3h_pass and not s.missing_author)
    assert s.gate_used["pass"] and set(s.gate_used["status_counts"]) == {"admitted"}
    if s.ready:
        assert summary["status"].startswith("READY")
    else:
        assert summary["status"].startswith("SHORT") and s.shortfalls
    # every shortfall is a real miss of a G0 bar (none is invented, none lowered)
    for x in s.shortfalls:
        if x["short_by"] is not None:
            assert x["got"] + x["short_by"] == x["bar"]


def test_the_pool_documents_only_hold_admitted_forms(built):
    s, _ = built
    lex_forms = {f["form_id"]: f for f in s.docs["lexicon.json"]["registry"]["forms"]}
    assert all(f["status"] == "admitted" for f in lex_forms.values())
    for w in s.docs["wordings.json"]["items"] + s.docs["precedence.json"]["items"]:
        assert w["form_id"] in lex_forms
    pending_ids = {x["form_id"] for x in s.pending}
    assert not pending_ids & set(lex_forms)
    assert s.docs["quarantine.json"]["pending_reads"] == s.pending


def test_the_v1_folder_cannot_be_a_write_target():
    with pytest.raises(PermissionError):
        FZ.refuse_v1_path(FZ.V1_POOLS / "wordings.json")
    FZ.refuse_v1_path(FZ.POOLS_V2 / "wordings.json")
    assert FZ.POOLS_V2 != FZ.V1_POOLS and FZ.V1_POOLS not in FZ.POOLS_V2.parents


def test_diff_files_reports_missing_and_changed_files(tmp_path):
    (tmp_path / "a.txt").write_text("one", encoding="utf-8")
    out = FZ.diff_files({"a.txt": "one", "b.txt": "x"}, tmp_path)
    assert out == ["missing b.txt"]
    assert FZ.diff_files({"a.txt": "two"}, tmp_path) == ["differs a.txt"]


# ======================================================================================== the READY path (in memory)

def _simulated(s, plan_for):
    """Accepted raw read answers for the redo2 read tasks: plan_for(read name, form id) -> meaning | None."""
    out = {}
    for name, b in s.r2_read_batches:
        for c in b.chunks:
            items = []
            for it in c["items"]:
                fid = b.key[it["qid"]]
                m = plan_for(name, fid)
                if m == "own":
                    m = s.reg.sems[s.reg.forms[fid].sem_id].meaning
                if m is not None:
                    items.append({"qid": it["qid"], "meaning": m})
            out[c["task_id"]] = items
    return out


@pytest.fixture(scope="module")
def r2_issued():
    if not (FZ.R2X / "TASKS.json").exists():
        pytest.skip("the redo2 read tasks have not been written yet (freeze_v2 reads)")


def test_two_correct_reads_per_form_make_the_pools_ready(built, r2_issued):
    s0, _ = built
    if not s0.r2_need:
        pytest.skip("no redo2 forms to read")
    s1 = FZ.build({"r2extract": _simulated(s0, lambda n, f: "own")}, redo3=False)      # pre-redo3 state: redo2 alone closes it
    assert s1.ready and s1.shortfalls == [] and not s1.pending
    wc = s1.counts["wordings"]
    assert all(wc["admitted_heldout_by_qform"].get(f, 0) >= 3 for f in FZ.FORMS)
    assert wc["admitted_training_by_qform"]["yn_fails"] >= 6
    held = [w for w in s1.kept["wording"] if w["held_out"]]
    assert held and all(len(w["extractions"]) == 2 for w in held)
    assert s1.docs["wordings.json"]["held_out_count"] == len(held)
    assert all(s1.reg.forms[w["form_id"]].held_out for w in held)


def test_one_disagreeing_read_rejects_and_a_missing_read_leaves_the_form_pending(built, r2_issued):
    s0, _ = built
    if not s0.r2_need:
        pytest.skip("no redo2 forms to read")
    fails = {p["form_id"] for p in s0.p2 if "form_id" in p and p["meta"]["qform"] == "yn_fails" and not p["held_out"]}
    decoy = s0.reg.sems["q.t26.decoy_fail_or_unverified"].meaning
    s2 = FZ.build({"r2extract": _simulated(
        s0, lambda n, f: decoy if (f in fails and n.endswith("2")) else "own")}, redo3=False)   # redo2 alone (pre-redo3)
    assert s2.counts["wordings"]["admitted_training_by_qform"].get("yn_fails", 0) == 0
    assert not s2.ready and any(x["target"] == "wording yn_fails (training)" and x["short_by"] == 6 for x in s2.shortfalls)
    assert all(s2.status[f] == "rejected" for f in fails)
    q = {x["internal_id"] for x in s2.quarantine if x["stage"] == "G-LEX"}
    assert {p["internal_id"] for p in s2.p2 if p.get("form_id") in fails} <= q
    s3 = FZ.build({"r2extract": _simulated(s0, lambda n, f: "own" if n.endswith("1") else None)}, redo3=False)
    assert not s3.ready and s3.pending and all(x["reads_recorded"] == 1 for x in s3.pending)
    assert s3.counts["wordings"]["admitted_heldout_by_qform"] == {}


# ======================================================================================== the redo3 fold

@pytest.fixture(scope="module")
def r3_issued():
    if not (FZ.REDO3 / "TASKS.json").exists() or not (FZ.R3X / "TASKS.json").exists():
        pytest.skip("the redo3 task files do not exist")


def _simulated_r3(s, plan_for):
    """Accepted raw read answers for the redo3 read tasks (the reads of the NEW redo3 wordings, in memory)."""
    out = {}
    for name, b in s.r3_read_batches:
        for c in b.chunks:
            items = []
            for it in c["items"]:
                fid = b.key[it["qid"]]
                m = plan_for(name, fid)
                if m == "own":
                    m = s.reg.sems[s.reg.forms[fid].sem_id].meaning
                if m is not None:
                    items.append({"qid": it["qid"], "meaning": m})
            out[c["task_id"]] = items
    return out


def test_effective_read_answers_prefer_the_original_location_and_never_count_a_task_twice():
    prim = {"T1": [{"qid": "a", "meaning": "m"}], "T2": [{"qid": "b", "meaning": "m"}]}
    alt = {"T2": [{"qid": "b", "meaning": "OTHER"}], "T3": [{"qid": "c", "meaning": "m"}], "T1": prim["T1"]}
    raw_, src, notes = FZ.effective_read_answers(prim, alt)
    assert src == {"T1": "redo2/extract", "T2": "redo2/extract", "T3": "redo3"}
    assert raw_["T2"] == prim["T2"] and raw_["T3"] == alt["T3"] and len(raw_) == 3
    assert len(notes) == 1 and "T2" in notes[0] and "differ" in notes[0]          # an identical pair needs no note
    assert FZ.effective_read_answers({}, {}) == ({}, {}, [])
    only_alt = FZ.effective_read_answers({}, alt)
    assert set(only_alt[1].values()) == {"redo3"} and only_alt[2] == []


def test_the_redo3_task_defs_are_the_tasks_the_agents_saw(r3_issued):
    tasks = json.loads((FZ.REDO3 / "TASKS.json").read_text(encoding="utf-8"))
    defs, rows = FZ.redo3_defs(tasks)
    assert len(defs) == len(rows) == tasks["n_tasks"] == 6
    r2x = FZ.defs_from_chunks(FZ.R2X / "chunks")
    for tid, cd in defs.items():
        assert cd.answer_file == str(FZ.R3_ANSWERS / f"{tid}.json")
        if cd.kind == "extract_lex":
            assert tid in r2x and cd.qids == r2x[tid].qids and cd.choices == r2x[tid].choices
            assert all(len(v) == 12 for v in cd.choices.values())             # 8 meanings + 4 decoys
            assert not cd.one_line
        else:
            assert cd.kind == "author_wording" and cd.one_line and len(cd.qids) == len(set(cd.qids))
    assert sum(1 for c in defs.values() if c.kind == "extract_lex") == 4
    assert sum(len(c.qids) for c in defs.values() if c.kind == "author_wording") == 19      # 4 training + 15 held-out


def test_every_redo3_answer_file_validates_and_none_is_edited(built, r3_issued):
    s, _ = built
    for name, n in (("redo3", 6), ("redo3_reads", 2)):
        rep = s.rounds[name]
        assert rep["tasks"] == n and not rep["missing"] and not rep["stray"]
        assert not rep["rejected"] and not rep["item_rejects"], (name, rep["rejected"])
        for t, r in rep["files"].items():
            data = (FZ.HERE / r["file"]).read_bytes()
            assert hashlib.sha256(data).hexdigest() == r["sha256"] and len(data) == r["bytes"]


def test_the_redo3_reads_of_the_redo2_wordings_count_as_the_redo2_reads(built, r3_issued):
    s, summary = built
    assert s.redo3
    redo2_tasks = set(FZ.defs_from_chunks(FZ.R2X / "chunks"))
    assert set(s.r2_read_source) == redo2_tasks
    for tid, src in s.r2_read_source.items():
        has_orig = (FZ.R2X / "answers" / f"{tid}.json").exists()
        assert src == ("redo2/extract" if has_orig else "redo3")
    assert [r["read"] for r in s.r2_reads] == ["glex-question-r2read1", "glex-question-r2read2"]
    assert all(r["answered_tasks"] and not r["chunk_problems"] for r in s.r2_reads)
    assert not [p for p in s.answer_problems if "redo2_extract" in p]
    assert {t["answered_by"] for t in summary["redo2_reads"]["tasks"]} <= {"redo2/extract", "redo3"}
    counted = summary["validation"]["redo2_extract"]["answers_counted_from"]
    assert sum(counted.values()) == len(redo2_tasks) and set(counted) <= {"redo2/extract", "redo3"}


def test_redo3_wordings_are_ingested_like_redo2_and_read_twice(built, r3_issued):
    s, summary = built
    assert s.p3 and len(s.p3) == 19
    assert s.checks["redo3_task_files_match_disk"] and s.checks["redo3_read_files_match_disk"]
    assert s.checks["redo3_read_prompt_unchanged"]
    ok = [p for p in s.p3 if not p["problems"]]
    assert ok and all("form_id" in p for p in ok) and sorted(p["form_id"] for p in ok) == sorted(s.r3_need)
    texts = [FZ.AI._norm(FZ.AI._value(p)) for p in ok]
    others = {FZ.AI._norm(f.text) for fid, f in s.reg.forms.items() if fid not in s.r3_need}
    assert len(set(texts)) == len(texts) and not set(texts) & others            # no repeat of any earlier wording
    for p in ok:
        f = s.reg.forms[p["form_id"]]
        assert f.held_out == (p["pool"] == "wording_heldout") and f.required == 2 and f.kind == "question"
        votes = [e for e, _ in f.extractions]
        assert sorted(votes) == ["glex-question-r3read1", "glex-question-r3read2"]       # one vote per read, no more
        assert (s.status[p["form_id"]] == "admitted") == all(m == f.sem_id for _, m in f.extractions)
    names = [r["read"] for r in s.r3_reads]
    assert names == ["glex-question-r3read1", "glex-question-r3read2"]
    assert all(r["items"] == len(s.r3_need) and not r["chunk_problems"] for r in s.r3_reads)
    # the two reads are separate batches with disjoint qids (no agent reads a form twice)
    (_, b1), (_, b2) = s.r3_read_batches
    assert b1.batch_id != b2.batch_id and set(b1.task_of.values()).isdisjoint(b2.task_of.values())
    assert summary["redo3_reads"]["issued"] and summary["redo3_reads"]["n_tasks"] == 2
    assert s.counts["redo3_pieces"] == {"answered": 19, "lint_or_dedup_dropped": 0, "registered_for_reads": 19}
    # held-out and training stay apart in the pools
    kept = s.kept["wording"]
    ho = {FZ.AI._norm(w["text"]) for w in kept if w["held_out"]}
    tr = {FZ.AI._norm(w["text"]) for w in kept if not w["held_out"]}
    assert ho and tr and not ho & tr
    assert all(w["held_out"] == (w["task_id"] in {p["task_id"] for p in s.p2 + s.p3 if p["pool"] == "wording_heldout"})
               for w in kept)


def test_without_the_redo3_fold_the_state_is_the_a3_shortfall():
    s0 = FZ.build(redo3=False)
    assert not s0.redo3 and not s0.p3 and not s0.r3_reads and s0.rounds.keys().isdisjoint({"redo3", "redo3_reads"})
    got = {x["target"]: x for x in s0.shortfalls if x["short_by"] is not None}
    if (FZ.R2X / "answers").is_dir() and any((FZ.R2X / "answers").glob("*.json")):
        pytest.skip("haiku/redo2/extract/answers holds answers: the pre-redo3 state differs from the A3 report")
    assert got["wording yn_fails (training)"]["short_by"] == 6 and got["held-out wordings, all forms"]["short_by"] == 24
    assert len(s0.pending) == 69 and not s0.ready


def test_the_redo3_fold_closes_the_a3_shortfalls_and_ready_holds(built, r3_issued):
    s, summary = built
    wc = s.counts["wordings"]
    assert wc["admitted_training_by_qform"]["yn_fails"] >= FZ.TARGET["wording_per_form"]["yn_fails"]
    for qf in FZ.FORMS:
        assert wc["admitted_training_by_qform"].get(qf, 0) >= FZ.TARGET["wording_per_form"][qf], qf
        assert wc["admitted_heldout_by_qform"].get(qf, 0) >= FZ.HELD_OUT_PER_FORM, qf
    assert not s.pending and not s.missing_redo3_author and not s.missing_author
    assert s.gate_used["pass"] and s.g3h_pass
    assert s.ready == (not s.shortfalls and s.gate_used["pass"] and s.g3h_pass)
    assert FZ.next_steps(s)[0].startswith("no read is pending") if s.ready else FZ.next_steps(s)


def test_a_disagreeing_redo3_read_rejects_the_new_form_for_good_and_a_missing_read_leaves_it_pending(built, r3_issued):
    s0, _ = built
    train_new = {p["form_id"] for p in s0.p3 if "form_id" in p and not p["held_out"]}
    assert len(train_new) == 4
    decoy = s0.reg.sems["q.t26.decoy_fail_or_unverified"].meaning
    s1 = FZ.build({"r3extract": _simulated_r3(
        s0, lambda n, f: decoy if (f in train_new and n.endswith("2")) else "own")})
    assert all(s1.status[f] == "rejected" for f in train_new)
    assert all(f not in {w["form_id"] for w in s1.kept["wording"]} for f in train_new)
    q = {x["internal_id"] for x in s1.quarantine if x["stage"] == "G-LEX"}
    assert {p["internal_id"] for p in s1.p3 if p.get("form_id") in train_new} <= q
    assert s1.counts["wordings"]["admitted_training_by_qform"]["yn_fails"] == 16        # the 16 redo2 forms still stand
    assert s1.ready                                                                       # the floors never needed them
    s2 = FZ.build({"r3extract": _simulated_r3(s0, lambda n, f: "own" if n.endswith("1") else None)})
    assert s2.pending and {x["form_id"] for x in s2.pending} == set(s0.r3_need)
    assert all(x["reads_recorded"] == 1 for x in s2.pending)
    admitted = {w["form_id"] for w in s2.kept["wording"]}
    assert not admitted & set(s0.r3_need)                                                # never used without 2 reads
    assert all(f not in {x["form_id"] for x in s2.docs["lexicon.json"]["registry"]["forms"]} for f in s0.r3_need)


def test_a_missing_redo3_authoring_answer_blocks_ready(built, r3_issued):
    s1 = FZ.build({"r3author": {}})                         # no redo3 authoring answer at all
    assert s1.missing_redo3_author and len(s1.missing_redo3_author) == 2
    assert not s1.p3 or all("form_id" not in p for p in s1.p3)
    assert not s1.ready


def test_an_authoring_answer_changed_after_its_reads_were_issued_stops_the_freeze(built, r3_issued):
    """The G-LEX read tasks on disk are what the agents saw. If an authoring answer changed (so the rebuilt items differ),
    the freeze refuses instead of counting reads of other wordings. Nothing is written."""
    chunks = {c["task_id"]: c for b in FZ.load_build_redo3().build()[2].values() for c in b.chunks}
    mutated = {tid: json.loads((FZ.R3_ANSWERS / f"{tid}.json").read_text(encoding="utf-8")) for tid in chunks}
    victim = next(w for w in built[0].kept["wording"] if not w["held_out"] and w["qform"] == "yn_fails")
    first = sorted(mutated)[0]
    mutated[first][0]["text"] = victim["text"]              # a wording that repeats an admitted one: dedup drops it
    with pytest.raises(SystemExit, match="redo3 read tasks on disk differ"):
        FZ.build({"r3author": mutated})


def test_a_redo3_piece_is_linted_and_deduplicated_against_every_registered_form(built, r3_issued):
    s0, _ = built
    taken = {FZ.AI._norm(f.text) for f in s0.reg.forms.values()}          # what build() passes: any status, every round
    some_admitted = next(w for w in s0.kept["wording"] if w["qform"] == "yn_dneg_apply")
    some_rejected = next(f for fid, f in s0.reg.forms.items() if s0.status[fid] == "rejected" and f.kind == "question"
                         and f.sem_id == "q.t26.yn_dneg_apply")      # lint-clean for its form, so dedup is what decides
    ps = [piece("t26|wording_ho|yn_dneg_apply|900", some_admitted["text"], "yn_dneg_apply", True),
          piece("t26|wording_ho|yn_dneg_apply|901", some_rejected.text, "yn_dneg_apply", True)]
    FZ.r2_lint_dedup(ps, taken)
    assert all(any("repeats a first-pass wording" in x for x in p["problems"]) for p in ps)     # a rejected text is never re-read


def test_build_reads_still_derives_the_redo3_read_tasks_from_the_pre_redo3_state(r3_issued):
    import importlib.util
    spec = importlib.util.spec_from_file_location("t26_build_reads_test", FZ.REDO3 / "build_reads.py")
    br = importlib.util.module_from_spec(spec)
    sys.modules["t26_build_reads_test"] = br
    spec.loader.exec_module(br)
    st = br.build(json.loads((FZ.REDO3 / "TASKS.json").read_text(encoding="utf-8")))
    assert br.check_contract(st) == []
    assert FZ.diff_files(st.files, FZ.R3X) == []


# ======================================================================================== the frozen pools_v2 (if written)

def test_pools_v2_manifest_matches_its_files_when_written():
    man = FZ.POOLS_V2 / "MANIFEST.json"
    if not man.exists():
        pytest.skip("pools_v2 has not been frozen yet")
    m = json.loads(man.read_text(encoding="utf-8"))
    for rel, row in m["pool_files"].items():
        data = (FZ.POOLS_V2 / rel).read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"] and len(data) == row["bytes"], rel
        assert json.loads(data)["count"] == row["count"]
    v = (FZ.POOLS_V2 / "validation_report.json").read_bytes()
    assert hashlib.sha256(v).hexdigest() == m["validation_report"]["sha256"]
    assert m["family"] == "T26" and m["version"] == "freeze-v2"
    assert m["ready"] == m["status"].startswith("READY")
    assert m["supersedes"]["sha256"] == hashlib.sha256((FZ.V1_POOLS / "manifest.json").read_bytes()).hexdigest()
    assert m["g0"]["sha256"] == m["g0"]["pinned_in_plugin"]
    # pools_v2 holds only the same pool files as v1 plus the manifest and the validation report
    v1 = {p.name for p in FZ.V1_POOLS.iterdir()}
    assert {p.name for p in FZ.POOLS_V2.iterdir()} == (v1 - {"manifest.json"}) | {"MANIFEST.json", "validation_report.json"}
