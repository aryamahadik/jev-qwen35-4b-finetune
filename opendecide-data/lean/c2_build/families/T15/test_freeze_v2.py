"""Tests for families/T15/freeze_v2.py (nothing is written to the repo; the freeze itself is never called here, only
refused against a temp folder).

  contract    validate_answer: one JSON list, exactly {qid, payload}, every expected qid once; every way to break it is
              rejected whole and the file is never touched; load_disk_batch detects a tampered prompt, chunk or key;
              an answer file named in AUDIT_FAILED_IGNORED is ignored
  R2 / R1     a Haiku text equal to a fixture text is a valid candidate, a duplicate of a pool candidate is not; a new
              form is dropped when it duplicates a form, fails its unit test or breaks another form's
  G-LEX       record_votes follows c2_kit.lexicon: 2/2 admits, a NONE / unlisted / other-sense vote rejects for good,
              one read stays pending, a precedence form needs 3/3, an extractor cannot vote twice
  build       (one full in-memory freeze-v2, ~1 min) every answer file of every round valid; freeze-v1 reproduced byte
              for byte and untouched; v1 reads and verdicts final; skins / attacks equal the interim pools/redo2; G0
              targets, G-LEX used-form gate, kit rules (distinct reads, no unread form used); pending forms never in
              wordings.json / comparators.json; sha256 map; the plugin runs on these pools (A == B); pools_v2/ on disk
              (when frozen) equals this build byte for byte
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T15/test_freeze_v2.py
"""
from __future__ import annotations

import copy
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
from families.T15 import fixtures as FX  # noqa: E402
from families.T15 import freeze_v2 as FV  # noqa: E402
from families.T15 import glex_admit as GA  # noqa: E402
from families.T15 import haiku_author as HA  # noqa: E402

G0_SHA256_AT_FREEZE = "c845ba9800174dabeb34ee23d038e9b12adb5d6d45a5247776fac1b5edddb300"   # G0 v1.2, pools_v2/MANIFEST.json

TID, PSHA = "tid", "0" * 64


# ------------------------------------------------------------------------------------------------ small batches
def _batch(payload_kind: str = "extract_lex", n: int = 3):
    if payload_kind == "extract_lex":
        items = [(f"internal-form-{i:03d}", {"text": f"text {i}", "choices": ["a", "b"]}) for i in range(n)]
    else:
        items = [(f"internal-item-{i:03d}", {"brief": f"b{i}", "meaning": "m", "slots": {"X": "x"}, "rules": []})
                 for i in range(n)]
    return chunker.make_batch(payload_kind, "T15", items, seed="seed", prompt="prompt text")


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
    r = FV.validate_answer(b, tid, p, "meaning")
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
    r = FV.validate_answer(b, b.chunks[0]["task_id"], p, "meaning")
    assert not r["ok"] and r["problems"] and r["answers"] == [], name
    assert p.read_bytes() == before                                           # never edited


def test_validate_answer_rejects_bad_files(tmp_path):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    good = json.dumps(_answers(b))
    for name, text in (("fenced", "```json\n" + good + "\n```"), ("text before", "Here you go: " + good),
                       ("two lists", good + good), ("NaN", good.replace('"a"', "NaN", 1)), ("empty file", ""),
                       ("not json", "[{"), ("BOM", "﻿" + good)):
        r = FV.validate_answer(b, tid, _write(tmp_path, "f.json", text), "meaning")
        assert not r["ok"] and r["answers"] == [], name
    r = FV.validate_answer(b, tid, tmp_path / "missing.json", "meaning")
    assert not r["ok"] and r["problems"] == ["answer file missing"]


def test_validate_answer_payload_types_and_redo_qid_subset(tmp_path):
    b = _batch("author_lexicon")
    qids = list(b.key)
    tid = b.chunks[0]["task_id"]
    ok = FV.validate_answer(b, tid, _write(tmp_path, "t.json", [{"qid": q, "text": "x"} for q in qids]), "text")
    assert ok["ok"]
    pk = FV.validate_answer(b, tid, _write(tmp_path, "p.json", [{"qid": q, "pack": {"programme": "A B"}}
                                                                for q in qids]), "pack")
    assert pk["ok"]
    bad_pk = FV.validate_answer(b, tid, _write(tmp_path, "p2.json", [{"qid": q, "pack": "A B"} for q in qids]), "pack")
    assert not bad_pk["ok"]
    nm = FV.validate_answer(b, tid, _write(tmp_path, "n.json", [{"qid": q, "names": ["Astrid"]} for q in qids]),
                            "names")
    assert nm["ok"]
    assert not FV.validate_answer(b, tid, _write(tmp_path, "n2.json", [{"qid": q, "names": []} for q in qids]),
                                  "names")["ok"]
    # a redo answer holds only its own qids: exactly that set, no more, no fewer
    sub = {qids[0]}
    assert FV.validate_answer(b, tid, _write(tmp_path, "r.json", [{"qid": qids[0], "text": "x"}]), "text",
                              expected=sub)["ok"]
    assert not FV.validate_answer(b, tid, _write(tmp_path, "r2.json", [{"qid": q, "text": "x"} for q in qids]),
                                  "text", expected=sub)["ok"]


def test_ignored_audit_failures_are_dropped(tmp_path, monkeypatch):
    b = _batch()
    tid = b.chunks[0]["task_id"]
    p = _write(tmp_path, f"{tid}.json", _answers(b))
    spec = FV.TaskSpec("redo2-a", tid, "r2a-A", b.kind, "meaning", p, b)
    monkeypatch.setattr(FV, "AUDIT_FAILED_IGNORED", (tid,))
    res, _ = FV.validate_all([spec])
    r = res[("redo2-a", tid)]
    assert not r["ok"] and r["audit_failed_ignored"] and r["answers"] == []
    monkeypatch.setattr(FV, "AUDIT_FAILED_IGNORED", ())
    res, _ = FV.validate_all([spec])
    assert res[("redo2-a", tid)]["ok"] and not res[("redo2-a", tid)]["audit_failed_ignored"]


def _write_batch(tmp_path: Path, b) -> None:
    for rel, text in b.files().items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")


def test_disk_batch_round_trip_and_tampering(tmp_path):
    b = _batch(n=4)
    _write_batch(tmp_path, b)
    got, probs = FV.load_disk_batch(tmp_path, b.batch_id)
    assert probs == [] and got.key == b.key and got.task_of == b.task_of and got.prompt_sha == b.prompt_sha
    # a changed item text: the chunk sha256 no longer matches its manifest
    cp = tmp_path / "chunks" / f"{b.chunks[0]['task_id']}.json"
    c = json.loads(cp.read_text(encoding="utf-8"))
    c["items"][0]["text"] = "tampered"
    cp.write_text(json.dumps(c), encoding="utf-8")
    assert any("chunk sha256" in p for p in FV.load_disk_batch(tmp_path, b.batch_id)[1])
    # a changed key entry: its opaque qid is not derived from the internal id any more
    _write_batch(tmp_path, b)
    kp = tmp_path / "key" / f"{b.batch_id}.json"
    k = json.loads(kp.read_text(encoding="utf-8"))
    q0 = next(iter(k["key"]))
    k["key"][q0] = "internal-form-099"
    kp.write_text(json.dumps(k), encoding="utf-8")
    probs = FV.load_disk_batch(tmp_path, b.batch_id)[1]
    assert any("not derived" in p for p in probs) and any("batch id derived" in p for p in probs)
    # a changed prompt
    _write_batch(tmp_path, b)
    (tmp_path / b.prompt_path()).write_text("another prompt", encoding="utf-8")
    assert any("prompt file" in p for p in FV.load_disk_batch(tmp_path, b.batch_id)[1])


def test_qid_derivation_matches_the_chunker():
    b = _batch(n=5)
    assert all(FV._qid(b.family, b.kind, b.seed, b.prompt_sha, iid) == q for q, iid in b.key.items())


# ------------------------------------------------------------------------------------------------ R2 and R1
def _fixture_wording(wid="W-ELIG-1"):
    w = next(x for x in FX.WORDINGS if x[0] == wid)
    return w[1], w[3], {"qform": w[1], "slots": dict(w[2]), "held_out": False}


def test_r2_fixture_copy_is_valid_but_a_pool_duplicate_is_not():
    q, text, meta = _fixture_wording()
    _, v = HA.check_wording("i", text, meta, TID, PSHA, set())
    assert v == [FV.DUP]                                                    # the v1 loader drops it
    seen = set()
    obj, v = FV.check_wording_r2("i", text, meta, TID, PSHA, seen)
    assert v == [] and obj[0] == q and text.lower() in seen
    obj, v = FV.check_wording_r2("j", text, meta, TID, PSHA, seen)           # now it IS a pool candidate
    assert v == [FV.DUP]
    # a fixture copy keeps every other check: an extra negation is still wrong
    bad = text.replace("eligible", "not eligible")
    _, v = FV.check_wording_r2("k", bad, meta, TID, PSHA, set())
    assert v and v != [FV.DUP]


def test_r2_comparators():
    meta = {"sem": "cmp.le", "slots": {"X": "cents"}}
    seen = set()
    _, v = HA.check_comparator("i", "at most {X}", meta, TID, PSHA, set())
    assert v == [FV.DUP]
    obj, v = FV.check_comparator_r2("i", "at most {X}", meta, TID, PSHA, seen)
    assert v == [] and obj[2] == "at most {X}"
    _, v = FV.check_comparator_r2("j", "at most {X}", meta, TID, PSHA, seen)
    assert v == [FV.DUP]
    _, v = FV.check_comparator_r2("k", "at most {X} dollars", meta, TID, PSHA, set())
    assert v and v != [FV.DUP]


def _mini_base():
    reg = LexiconRegistry("T15")
    reg.declare("cmp.le", "comparator", "less than or equal to the bound")
    reg.declare("cmp.lt", "comparator", "strictly less than the bound")
    reg.add("at most {X}", "cmp.le", slots={"X": "cents"})
    reg.add("below {X}", "cmp.lt", slots={"X": "cents"})
    reg.unit_test_all()
    return reg.to_json()


def _cand(text, sem="cmp.le", slot=("X", "cents")):
    return {"iid": f"i.{text}", "pool": "comparators", "origin": "t", "qform": None, "sem": sem, "kind": "comparator",
            "text": text, "slots": dict([slot]), "held_out": False, "tid": TID, "psha": PSHA, "expect_fid": None}


def test_accept_forms_keeps_good_and_drops_duplicates_and_unit_failures():
    base = _mini_base()
    # "below {X}." (another sense) spans the same text as the existing "below {X}" inside a sentence: it breaks that form
    good, dup, bad = _cand("no more than {X}"), _cand("AT  most {X}"), _cand("below {X}.")
    acc, dropped, reg = FV.accept_forms(base, [good, dup, bad])
    assert [a["iid"] for a in acc] == [good["iid"]]
    why = {c["iid"]: w for c, w in dropped}
    assert "duplicate form text" in why[dup["iid"]]
    assert why[bad["iid"]].startswith("unit test in the full registry") and "breaks" in why[bad["iid"]]
    assert all(reg.forms[a["form_id"]].unit_ok for a in acc) and len(reg.forms) == 3
    # the order of the candidates does not change who is accepted (canonical form-id order)
    acc2, _, reg2 = FV.accept_forms(base, [bad, dup, good])
    assert [a["form_id"] for a in acc2] == [a["form_id"] for a in acc] and reg2.sha256() == reg.sha256()


def test_canonical_registry_is_independent_of_the_candidate_order():
    base = _mini_base()
    c1, c2 = _cand("no more than {X}"), _cand("not over {X}")
    r1, _ = FV.canonical_registry(base, [c1, c2])
    r2, _ = FV.canonical_registry(base, [c2, c1])
    assert r1.sha256() == r2.sha256() and list(r1.forms) == sorted(r1.forms) == list(r2.forms)
    rt = LexiconRegistry.from_json(r1.to_json())                              # what a loader sees
    assert {f: x.unit_ok for f, x in rt.forms.items()} == {f: x.unit_ok for f, x in r1.forms.items()}


# ------------------------------------------------------------------------------------------------ G-LEX votes
def _vote_reg():
    reg = LexiconRegistry("T15")
    reg.declare("cmp.le", "comparator", "less than or equal to the bound")
    reg.declare("cmp.lt", "comparator", "strictly less than the bound")
    a = reg.add("at most {X}", "cmp.le", slots={"X": "cents"})
    b = reg.add("below {X}", "cmp.lt", slots={"X": "cents"})
    c = reg.add("under {X}", "cmp.lt", slots={"X": "cents"})
    reg.unit_test_all()
    return reg, a.form_id, b.form_id, c.form_id


LE, LT = "less than or equal to the bound", "strictly less than the bound"


def test_two_of_two_admits_and_any_other_pick_rejects_for_good():
    reg, a, b, c = _vote_reg()
    for ex in ("e1", "e2"):
        FV.record_votes(reg, ex, {a: {"meaning": LE}, b: {"meaning": LT if ex == "e1" else "NONE"},
                                  c: {"meaning": LE if ex == "e1" else "not a listed meaning"}})
    assert reg.status(a) == "admitted"
    assert reg.status(b) == "rejected" and reg.status(c) == "rejected"      # NONE / another sense / unlisted
    # no re-vote: a third read cannot undo a rejection
    FV.record_votes(reg, "e3", {b: {"meaning": LT}})
    assert reg.status(b) == "rejected"
    assert not reg.gate(used_form_ids=[a, b])["pass"] and reg.gate(used_form_ids=[a])["pass"]


def test_one_read_is_pending_and_an_extractor_cannot_vote_twice():
    reg, a, b, c = _vote_reg()
    cnt = FV.record_votes(reg, "e1", {a: {"meaning": LE}, "no-such-form": {"meaning": LE}})
    assert cnt == {"listed": 1, "form_not_in_registry": 1} and reg.status(a) == "pending"
    with pytest.raises(LexiconError):
        FV.record_votes(reg, "e1", {a: {"meaning": LE}})
    FV.record_votes(reg, "e2", {a: {"meaning": LE}})
    assert reg.status(a) == "admitted"


def test_a_precedence_form_needs_three_of_three():
    reg = LexiconRegistry("T15")
    reg.declare("prec.P1", "precedence", "deny rules beat allow rules")
    f = reg.add("deny beats allow", "prec.P1", slots={})
    reg.unit_test_all()
    assert f.required == 3
    for k, ex in enumerate(("e1", "e2", "e3"), 1):
        FV.record_votes(reg, ex, {f.form_id: {"meaning": "deny rules beat allow rules"}})
        assert reg.status(f.form_id) == ("admitted" if k == 3 else "pending")


# ------------------------------------------------------------------------------------------------ freeze guards
def test_freeze_refuses_an_existing_manifest_and_writes_nothing(tmp_path, monkeypatch):
    (tmp_path / "MANIFEST.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(FV, "POOLS_V2", tmp_path)
    with pytest.raises(SystemExit):
        FV.freeze({"files": {"x.json": "{}"}})
    assert sorted(p.name for p in tmp_path.iterdir()) == ["MANIFEST.json"]


def test_freeze_v1_and_the_interim_pools_are_untouched():
    assert FV.v1_integrity() == [] and FV.interim_integrity() == []


# ------------------------------------------------------------------------------------------------ the full build
@pytest.fixture(scope="module")
def built():
    return FV.build()


def test_every_answer_file_of_every_round_is_valid(built):
    rep = built["manifest"]["answer_files"]
    assert rep["by_round"] == {"author-v1|ok": 19, "extract-v1|ok": 10, "redo-v1|ok": 8, "redo2-a|ok": 4}
    assert all(f["ok"] and f["problems"] == [] and f["sha256"] for f in rep["files"])
    assert rep["audit_failed_ignored"] == []
    assert built["problems"] == []


def test_the_v1_baseline_is_reproduced_byte_for_byte(built):
    man = built["manifest"]
    assert man["v1_reproduced"] and all(man["v1_reproduced"].values()) and len(man["v1_reproduced"]) == 9
    assert man["problems"]["v1_integrity"] == [] and man["problems"]["interim_integrity"] == []
    assert man["g0"]["matches_plugin_pin"]


def test_v1_reads_and_verdicts_are_final(built):
    old = json.loads((FV.POOLS_V1 / "lexicon.json").read_text(encoding="utf-8"))
    new = {f["form_id"]: f for f in json.loads(built["files"]["lexicon.json"])["forms"]}
    assert len(new) == 297
    for f in old["forms"]:
        n = new[f["form_id"]]
        assert n["extractions"] == f["extractions"] and n["text"] == f["text"] and n["sem_id"] == f["sem_id"]
        assert n["status"] == f["status"], f["form_id"]                       # admitted / rejected / unit_fail stay


def test_skins_attacks_packs_names_match_the_earlier_merge(built):
    im = json.loads((FV.POOLS_INTERIM / "MANIFEST.json").read_text(encoding="utf-8"))["sha256"]
    v1 = json.loads((FV.POOLS_V1 / "MANIFEST.json").read_text(encoding="utf-8"))["sha256"]
    sha = built["manifest"]["sha256"]
    assert sha["skins.json"] == im["skins.json"] and sha["attacks.json"] == im["attacks.json"]
    for n in ("packs.json", "names.json", "documents.json"):
        assert sha[n] == v1[n]
    assert sha["skins.json"] != v1["skins.json"]                              # redo-v1 closed the skin gaps


def test_g0_targets_and_verdict_agree(built):
    c, man = built["counts"], built["manifest"]
    assert built["shortfalls"] == [] and man["verdict"] == "READY" and built["ready"]
    assert man["status"].startswith("FROZEN:")
    assert all(c["skins_by_register"][f"{r}|train"] == 40 for r in GA.TRAIN_REGISTERS)
    assert all(c["skins_by_register"][f"{r}|held"] == 30 for r in GA.HELD_REGISTERS)
    assert c["attacks_asked"] == 24 and c["attacks_held"] == 8
    assert c["wordings_candidates_asked"] >= 178 and c["wordings_candidates_held"] >= 44
    assert c["wordings_admitted_asked"] >= 78
    for q in HA.WORDING_PLAN:
        assert c["wordings_admitted_asked_by_form"][q] >= max(3, HA.ADMIT_TARGET.get(q, 0)), q
    assert all(n >= 12 for n in c["comparators_candidates_by_sense"].values())
    assert c["comparators_admitted_by_sense"] == {"cmp.ge": 12, "cmp.gt": 12, "cmp.le": 12, "cmp.lt": 12}
    assert built["manifest"]["targets_g0"] == GA.G0_TARGETS                    # never lowered
    assert all(n >= 1 for n in man["derived_requirements"]["admitted_held_out_per_qform"].values())


def test_glex_gate_and_kit_rules(built):
    man, st = built["manifest"], built["state"]
    reg = st["reg"]
    assert man["gates"]["G-LEX_used_forms"]["pass"] and man["gates"]["G-LEX_used_forms"]["n_forms"] == 244
    kit = man["gates"]["G-LEX_kit_rules"]
    assert kit["strict_kinds_in_registry"] == [] and kit["required_reads"] == {"2": 297}
    assert kit["admitted_with_fewer_distinct_reads"] == [] and kit["admitted_not_all_agreeing"] == []
    for fid, f in reg.forms.items():
        status = reg.status(fid)
        distinct = {e for e, _ in f.extractions}
        if status == "admitted":
            assert len(distinct) >= f.required and all(s == f.sem_id for _, s in f.extractions)
            assert f.unit_ok
        if status == "pending":
            assert len(distinct) < f.required and all(s == f.sem_id for _, s in f.extractions)


def test_only_admitted_forms_reach_the_pool_files(built):
    files = built["files"]
    lex = {f["form_id"]: f for f in json.loads(files["lexicon.json"])["forms"]}
    used = ({w["form_id"] for w in json.loads(files["wordings.json"])["wordings"]}
            | {c["form_id"] for c in json.loads(files["comparators.json"])["comparators"]})
    assert used == {fid for fid, f in lex.items() if f["status"] == "admitted"} and len(used) == 244
    assert all(lex[fid]["usable"] for fid in used)
    unused = set(lex) - used
    assert all(not lex[fid]["usable"] for fid in unused)
    pend = [fid for fid in unused if lex[fid]["status"] == "pending"]
    assert sorted(pend) == built["pending"]["forms"] and len(pend) == 45
    assert all(lex[fid]["extractions"] == [] for fid in pend)                 # nothing read them: no vote invented
    # the new reads came from the r2a stage only, for exactly the five re-entered forms
    new_reads = {fid: f["extractions"] for fid, f in lex.items() if f["extractions"]
                 and any(e.startswith("read-r2") for e, _ in f["extractions"])}
    assert len(new_reads) == 5 and all(sorted(e for e, _ in x) == ["read-r2a-A", "read-r2a-B"]
                                       for x in new_reads.values())


def test_candidate_counts_and_pending_are_reported_apart(built):
    c, pend = built["counts"], built["pending"]
    decided = c["wordings_candidates_asked"] - pend["wordings_asked"]
    assert pend["wordings_asked"] == 23 and pend["wordings_held"] == 2 and pend["comparators"] == 20
    assert decided == 160 == pend["wordings_candidates_asked_g_lex_decided"] and c["wordings_candidates_asked"] == 183
    dropped = built["manifest"]["folded"]["redo2"]["dropped"]
    assert [d["piece"] for d in dropped] == ["t15a.wording.yn_dneg_eligible.004"]


def test_the_sha256_map_covers_every_file(built):
    files, man = built["files"], built["manifest"]
    assert set(man["sha256"]) == set(files) - {"MANIFEST.json"}
    assert all(FV._sha(files[n]) == s for n, s in man["sha256"].items())
    assert json.loads(files["MANIFEST.json"]) == json.loads(GA._dump(man))
    q = json.loads(files["QUARANTINE.json"])["rows"]
    assert len(q) == man["quarantined"] and all("piece" in r and "stage" in r for r in q)


def test_the_plugin_runs_on_the_v2_pools(built):
    pools = FV.pools_from_texts(built["files"])
    assert len(pools.packs) == 60 and len(pools.lexicon.forms) == 297
    out = FV.smoke(pools, seeds=3)
    assert out["rows"] == 15
    ctx = FV.make_ctx(pools)
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording") == len(pools.wordings) == 196
    with pytest.raises(ValueError):                                           # a changed file is refused
        FV.pools_from_texts(dict(built["files"], **{"names.json": built["files"]["names.json"] + " "}))


def test_pools_v2_on_disk_equals_this_build(built):
    if not (FV.POOLS_V2 / "MANIFEST.json").is_file():
        pytest.skip("pools_v2/ is not frozen yet")
    on_disk = {p.name: p.read_text(encoding="utf-8") for p in sorted(FV.POOLS_V2.glob("*.json"))}
    # The pools were frozen under G0 v1.2; G0 v1.3 (pilot fix iteration 1: card text, placement, S20 plans) changed no
    # pool text, so the on-disk manifest keeps the v1.2 sha and a rebuild records the current pin; every other byte
    # of every pool file, and the rest of the manifest, is identical.
    g0_frozen = json.loads(on_disk["MANIFEST.json"])["g0"]
    assert g0_frozen == {"path": "families/T15/G0_SPEC.md", "sha256": G0_SHA256_AT_FREEZE, "matches_plugin_pin": True}
    rebuilt = json.loads(built["files"]["MANIFEST.json"])
    assert rebuilt["g0"]["sha256"] == FV.P.T15Plugin.G0_SHA256
    rebuilt["g0"], disk_man = g0_frozen, json.loads(on_disk["MANIFEST.json"])
    assert rebuilt == disk_man
    assert {k: v for k, v in on_disk.items() if k != "MANIFEST.json"} == {
        k: v for k, v in built["files"].items() if k != "MANIFEST.json"}
    FV.load_pools()                                                           # sha256 of every file checked
    assert FV.v1_integrity() == [] and FV.interim_integrity() == []
